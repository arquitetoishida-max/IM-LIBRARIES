#!/usr/bin/env python3
"""Build and validate the optional schema-2 study_forms extension (issue #7)."""
import argparse
import copy
import json
import os
from pathlib import Path
import tempfile
import unicodedata


def text(value):
    return isinstance(value, str) and bool(value.strip())


def eligible(entry):
    return (entry.get("core_status") != "retired"
            and entry.get("kind") not in ("form", "example")
            and text(entry.get("text")))


def validate(package):
    """Reject broken identities and defaults. Legacy packages are accepted."""
    if package.get("schema_version") != 2 or package.get("package_type") != "ishida-monolingual":
        raise ValueError("expected an ishida-monolingual schema-2 package")
    if not text(package.get("package_id")) or not text(package.get("language")):
        raise ValueError("missing package identity or language")
    if package.get("study_forms_version") not in (None, 1):
        raise ValueError("unsupported study_forms_version")
    entries = package.get("entries")
    if not isinstance(entries, list):
        raise ValueError("entries must be an array")
    entry_ids, form_ids = set(), set()
    for entry in entries:
        if not isinstance(entry, dict) or not text(entry.get("id")):
            raise ValueError("entry without an identity")
        eid = entry["id"]
        if eid in entry_ids:
            raise ValueError("duplicate entry: " + eid)
        entry_ids.add(eid)
        if "study_forms" not in entry:
            if package.get("study_forms_version") == 1 and eligible(entry):
                raise ValueError("missing study_forms: " + eid)
            continue
        forms = entry["study_forms"]
        if not eligible(entry) or not isinstance(forms, list) or not forms:
            raise ValueError("invalid study_forms owner: " + eid)
        if package.get("study_forms_version") != 1:
            raise ValueError("study_forms require package study_forms_version=1")
        defaults, primary = 0, 0
        lexical_texts = set()
        for form in forms:
            if not isinstance(form, dict):
                raise ValueError("form must be an object: " + eid)
            fid = form.get("form_id")
            if not text(fid) or fid in form_ids or not fid.startswith(eid + ":sf:"):
                raise ValueError("duplicate or foreign form_id: " + str(fid))
            form_ids.add(fid)
            for field in ("entry_id", "english_id", "english_sense_id"):
                expected = eid if field == "entry_id" else entry.get(field)
                if form.get(field) != expected:
                    raise ValueError("incorrect " + field + ": " + fid)
            for field in ("text", "speech", "usage_en"):
                if not text(form.get(field)):
                    raise ValueError("missing " + field + ": " + fid)
            normalized = unicodedata.normalize("NFC", form["text"]).strip()
            if normalized in lexical_texts:
                raise ValueError("duplicate lexical form; use representations: " + fid)
            lexical_texts.add(normalized)
            for field in ("reading", "romanization", "context_en", "register", "study_tier"):
                if field in form and not text(form[field]):
                    raise ValueError("invalid " + field + ": " + fid)
            for field in ("region_tags", "sources"):
                if field in form and (not isinstance(form[field], list)
                                      or not form[field] or not all(text(v) for v in form[field])):
                    raise ValueError("invalid " + field + ": " + fid)
            if "legacy_entry_id" not in form and (not text(form.get("context_en")) or not form.get("sources")):
                raise ValueError("alternative requires context and sources: " + fid)
            for field in ("examples", "representations"):
                if field in form:
                    values = form[field]
                    if not isinstance(values, list) or not values:
                        raise ValueError("invalid " + field + ": " + fid)
                    for value in values:
                        if not isinstance(value, dict) or not text(value.get("text")):
                            raise ValueError("invalid " + field + ": " + fid)
                        if field == "representations" and not text(value.get("usage_en")):
                            raise ValueError("representation requires usage_en: " + fid)
                        if field == "examples":
                            translations = value.get("translations")
                            if (not isinstance(translations, dict) or not translations
                                    or not all(text(k) and text(v) for k, v in translations.items())):
                                raise ValueError("example requires locale translations: " + fid)
            for field in ("recommended", "include_by_default"):
                if not isinstance(form.get(field), bool):
                    raise ValueError("invalid " + field + ": " + fid)
            defaults += form["recommended"]
            if form["recommended"] and not form["include_by_default"]:
                raise ValueError("recommended form must be active by default: " + fid)
            if form.get("legacy_entry_id") is not None:
                primary += 1
                if (form["legacy_entry_id"] != eid or fid != eid + ":sf:0"
                        or form["text"] != entry["text"].split(";")[0].strip()):
                    raise ValueError("invalid primary/legacy link: " + fid)
            if package["language"] == "ja" and not text(form.get("reading")):
                raise ValueError("missing Japanese reading: " + fid)
            if package["language"] == "zh" and not text(form.get("romanization")):
                raise ValueError("missing Mandarin pinyin: " + fid)
            if "study_priority" in form and (type(form["study_priority"]) is not int or form["study_priority"] < 0):
                raise ValueError("invalid study priority: " + fid)
            if "age_band" in form and form["age_band"] not in (3, 5, 7, 10, 14):
                raise ValueError("invalid age band: " + fid)
            for field in ("grade", "history", "profile_id", "selected"):
                if field in form:
                    raise ValueError("private student state in package: " + fid)
        if defaults != 1 or primary != 1:
            raise ValueError("expected one recommendation and one primary: " + eid)
    return len(form_ids)


def build(package, registry):
    """Only explicit registry alternatives become independently trainable forms."""
    validate(package)
    if registry.get("version") != 1 or not isinstance(registry.get("packages"), dict):
        raise ValueError("invalid registry")
    rules = registry["packages"].get(package["package_id"], {})
    if not isinstance(rules, dict):
        raise ValueError("invalid package registry")
    result = copy.deepcopy(package)
    entries = {e["id"]: e for e in result["entries"]}
    unknown = set(rules) - set(entries)
    if unknown:
        raise ValueError("unknown registry entries: " + ", ".join(sorted(unknown)))
    for eid, entry in entries.items():
        if not eligible(entry):
            if eid in rules:
                raise ValueError("registry targets an ineligible entry: " + eid)
            entry.pop("study_forms", None)
            continue
        if not text(entry.get("description_en")) or not text(entry.get("english_id")):
            raise ValueError("missing meaning: " + eid)
        primary = {
            "form_id": eid + ":sf:0", "entry_id": eid,
            "english_id": entry["english_id"],
            "english_sense_id": entry.get("english_sense_id"),
            "text": entry["text"].split(";")[0].strip(),
            "speech": entry.get("speech") or entry["text"].split(";")[0].strip(),
            "usage_en": entry["description_en"],
            "recommended": True, "include_by_default": True,
            "legacy_entry_id": eid,
        }
        for key in ("reading", "romanization", "study_priority", "study_tier"):
            if entry.get(key) is not None:
                primary[key] = entry[key]
        forms = [primary]
        if not isinstance(rules.get(eid, []), list):
            raise ValueError("registry alternatives must be an array: " + eid)
        for alternative in rules.get(eid, []):
            if (not isinstance(alternative, dict) or alternative.get("approved") is not True
                    or not alternative.get("sources") or not alternative.get("context_en")):
                raise ValueError("unreviewed alternative: " + eid)
            form = copy.deepcopy(alternative)
            form.pop("approved")
            recommended = form.get("recommended", False)
            form.update(entry_id=eid, english_id=entry["english_id"],
                        english_sense_id=entry.get("english_sense_id"),
                        recommended=recommended, include_by_default=recommended)
            # No inherited reading, register or age for a different lexical form.
            forms.append(form)
        if any(form.get("recommended") is True for form in forms[1:]):
            primary["recommended"] = False
            primary["include_by_default"] = False
        old = {f["form_id"] for f in entry.get("study_forms", [])}
        if old - {f["form_id"] for f in forms}:
            raise ValueError("published form removed; preserve its identity: " + eid)
        entry["study_forms"] = forms
    result["study_forms_version"] = 1
    validate(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    package = json.loads(args.input.read_text(encoding="utf-8"))
    if args.output:
        if args.output.resolve() == args.input.resolve():
            parser.error("use a separate candidate output path")
        registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry else {"version": 1, "packages": {}}
        package = build(package, registry)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        # A failed write leaves the previous candidate intact.
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=args.output.parent, delete=False) as stream:
            temp = Path(stream.name)
            try:
                json.dump(package, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            except BaseException:
                temp.unlink(missing_ok=True)
                raise
        try:
            os.replace(temp, args.output)
        finally:
            temp.unlink(missing_ok=True)
    count = validate(package)
    print(json.dumps({"package_id": package["package_id"], "entries": len(package["entries"]), "study_forms": count}))


if __name__ == "__main__":
    main()
