#!/usr/bin/env python3
"""Build installable ISHIDA MULTILANG library packages from public, licensed sources.

Pipeline per source: download -> parse (source-specific adapter) -> map languages ->
normalize -> validate -> deduplicate -> attach wordfreq frequency (Zipf, in the language of
the studied word) -> keep the most frequent N -> write package JSON + catalog.json.

Only packages that were actually built are listed in catalog.json, so the app never offers a
language without real data. Every adapter is optional: a failing source is reported and skipped.
"""
import datetime
import gzip
import io
import json
import pathlib
import re
import sys
import urllib.request

OUT = pathlib.Path("packages")
OUT.mkdir(exist_ok=True)
TODAY = datetime.date.today().isoformat()
REPO_DL = "https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/packages/"
TOP_N = 2000
UA = {"User-Agent": "ishida-multilang-package-builder/1.0 (+https://github.com/arquitetoishida-max/ISHIDA-NIHONGO)"}

try:
    from wordfreq import zipf_frequency
except Exception as exc:  # pragma: no cover
    print("wordfreq unavailable:", exc)
    zipf_frequency = None


def zipf(word, lang):
    if not zipf_frequency or not word:
        return 0.0
    try:
        return round(zipf_frequency(word, lang), 2)
    except Exception:
        return 0.0


def open_url(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=120)


PREFIX = re.compile(r"^\s*([A-Za-z]{2})(?:-[A-Za-z]{2})?\s*:\s+")


def clean(text):
    """Remove stray language tags ("EN: ...") and collapse whitespace."""
    text = re.sub(r"\s+", " ", text or "").strip()
    m = PREFIX.match(text)
    if m and m.group(1).lower() in {"en", "pt", "ja", "zh", "es", "fr", "it", "de", "ko", "ru"}:
        text = text[m.end():]
    return text[:300]


# ---------- pinyin tone numbers -> tone marks ----------
TONES = {"a": "āáǎàa", "e": "ēéěèe", "i": "īíǐìi", "o": "ōóǒòo", "u": "ūúǔùu", "ü": "ǖǘǚǜü"}


def pinyin_marks(syllables):
    out = []
    for syl in syllables.split():
        syl = syl.replace("u:", "ü").replace("v", "ü")
        m = re.match(r"^([A-Za-zü]+)([1-5])$", syl)
        if not m:
            out.append(syl)
            continue
        base, tone = m.group(1), int(m.group(2))
        low = base.lower()
        idx = -1
        if "a" in low:
            idx = low.index("a")
        elif "e" in low:
            idx = low.index("e")
        elif "ou" in low:
            idx = low.index("o")
        else:
            for i in range(len(low) - 1, -1, -1):
                if low[i] in TONES:
                    idx = i
                    break
        if idx >= 0:
            v = low[idx]
            mark = TONES[v][tone - 1]
            if base[idx].isupper():
                mark = mark.upper()
            base = base[:idx] + mark + base[idx + 1:]
        out.append(base)
    return " ".join(out)


# ---------- adapters ----------
def build_cedict():
    url = "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz"
    raw = open_url(url).read()
    text = gzip.decompress(raw).decode("utf-8")
    line_re = re.compile(r"^(\S+) (\S+) \[([^\]]+)\] /(.+)/$")
    best = {}
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        m = line_re.match(line)
        if not m:
            continue
        trad, simp, pin, defs = m.groups()
        senses = [clean(d) for d in defs.split("/") if d and not d.startswith(("CL:", "variant of", "old variant", "see ", "surname "))]
        if not senses:
            continue
        key = (simp, pin.lower())
        if key in best:
            continue
        best[key] = {"zh": simp, "zh-TW": trad, "zh_reading": pinyin_marks(pin), "en": "; ".join(senses[:3])}
    entries = []
    for (simp, pin), e in best.items():
        z = zipf(simp, "zh")
        if z <= 0:
            continue
        e["zipf"] = z
        e["id"] = "cedict:" + simp + ":" + pin.replace(" ", "")
        e["record_type"] = "word"
        entries.append(e)
    entries.sort(key=lambda e: -e["zipf"])
    entries = entries[:TOP_N]
    return {
        "id": "cedict-zh",
        "name": "CC-CEDICT 中文",
        "language": "zh",
        "license": "CC BY-SA 4.0 (CC-CEDICT, MDBG)",
        "source": "https://www.mdbg.net/chinese/dictionary?page=cc-cedict",
        "frequency": "wordfreq (Zipf), CC BY-SA 4.0",
        "version": TODAY,
        "entries": entries,
    }


KAIKKI = {
    # language code: Wiktionary language name used by kaikki.org (English-Wiktionary extraction)
    "it": "Italian",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ko": "Korean",
    "ru": "Russian",
    "ja": "Japanese",
    "pt": "Portuguese",
}


def build_kaikki(code, name):
    url = f"https://kaikki.org/dictionary/{name}/kaikki.org-dictionary-{name}.jsonl"
    words = {}
    with open_url(url) as stream:
        for raw in io.TextIOWrapper(stream, encoding="utf-8"):
            try:
                d = json.loads(raw)
            except Exception:
                continue
            word = d.get("word", "").strip()
            if not word or " " in word and len(word.split()) > 4:
                continue
            if any(t in (d.get("pos") or "") for t in ("name", "character", "symbol", "suffix", "prefix", "affix", "letter", "abbrev")):
                continue
            glosses = []
            for s in d.get("senses", []):
                tags = s.get("tags", [])
                if "form-of" in tags or "alt-of" in tags or "obsolete" in tags or "archaic" in tags:
                    continue
                for g in s.get("glosses", [])[:1]:
                    g = clean(g)
                    if g.lower().startswith(("the name of the", "abbreviation of", "initialism of", "misspelling of")):
                        continue
                    if g and g not in glosses:
                        glosses.append(g)
            if not glosses:
                continue
            key = word.lower()
            entry = words.setdefault(key, {"word": word, "glosses": [], "reading": ""})
            for g in glosses:
                if len(entry["glosses"]) < 3 and g not in entry["glosses"]:
                    entry["glosses"].append(g)
            if code in ("ru", "ko") and not entry["reading"]:
                for f in d.get("forms", []):
                    if "romanization" in f.get("tags", []):
                        entry["reading"] = f.get("form", "")
                        break
    entries = []
    for key, e in words.items():
        z = zipf(e["word"], code)
        if z <= 0:
            continue
        item = {"id": f"kaikki-{code}:{key}", "record_type": "expression" if " " in e["word"].strip() else "word", code: e["word"], "en": "; ".join(e["glosses"]), "zipf": z}
        if e["reading"]:
            item[code + "_reading"] = e["reading"]
        entries.append(item)
    entries.sort(key=lambda e: -e["zipf"])
    entries = entries[:TOP_N]
    return {
        "id": f"kaikki-{code}",
        "name": f"Wiktionary {name} (kaikki.org)",
        "language": code,
        "license": "CC BY-SA 4.0 / GFDL (Wiktionary, via kaikki.org)",
        "source": f"https://kaikki.org/dictionary/{name}/",
        "frequency": "wordfreq (Zipf), CC BY-SA 4.0",
        "version": TODAY,
        "entries": entries,
    }


def validate(pkg):
    lang = pkg["language"]
    seen = set()
    good = []
    for e in pkg["entries"]:
        if e["id"] in seen or not e.get(lang) or not e.get("en"):
            continue
        if any(PREFIX.match(str(v)) and str(v)[:2].lower() in {"en", "pt", "ja"} for k, v in e.items() if k not in ("id", "zipf", "record_type")):
            continue
        seen.add(e["id"])
        good.append(e)
    pkg["entries"] = good
    if len(good) < 100:
        raise RuntimeError(f"{pkg['id']}: only {len(good)} valid entries")
    return pkg


def main():
    jobs = [("cedict-zh", build_cedict)] + [(f"kaikki-{c}", (lambda c=c, n=n: build_kaikki(c, n))) for c, n in KAIKKI.items()]
    only = set(sys.argv[1:])
    catalog = []
    old = OUT / "catalog.json"
    for pid, job in jobs:
        if only and pid not in only:
            continue
        try:
            pkg = validate(job())
        except Exception as exc:
            print(f"[skip] {pid}: {exc}")
            continue
        data = json.dumps(pkg, ensure_ascii=False, separators=(",", ":"))
        (OUT / f"{pid}.json").write_text(data, encoding="utf-8")
        bands = [0] * 5
        for e in pkg["entries"]:
            z = e["zipf"]
            bands[0 if z >= 5 else 1 if z >= 4 else 2 if z >= 3 else 3 if z >= 2 else 4] += 1
        print(f"[ok] {pid}: {len(pkg['entries'])} entries, {len(data) // 1024} KB, zipf bands {bands}")
        langs = sorted({k for e in pkg["entries"] for k in e if k not in ("id", "zipf", "record_type") and not k.endswith("_reading")})
        catalog.append({
            "id": pid,
            "name": pkg["name"],
            "language": pkg["language"],
            "languages": langs,
            "entries": len(pkg["entries"]),
            "record_types": {"words": sum(e.get("record_type") == "word" for e in pkg["entries"]), "expressions": sum(e.get("record_type") == "expression" for e in pkg["entries"])},
            "semantic_ids": "source-scoped; NOT cross-language concept IDs",
            "license": pkg["license"],
            "source": pkg["source"],
            "frequency": pkg.get("frequency"),
            "version": pkg["version"],
            "url": REPO_DL + f"{pid}.json",
            "bytes": len(data.encode("utf-8")),
        })
    old.write_text(json.dumps({"generated": TODAY, "packages": catalog}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("catalog:", [c["id"] for c in catalog])


if __name__ == "__main__":
    main()
