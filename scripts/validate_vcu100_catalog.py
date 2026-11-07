#!/usr/bin/env python3
"""Validate published VCU100 packages and their bilingual dependencies.

Checks integrity, per-package identity, schema-2 shape and semantic alignment.
Does not claim linguistic verification or Android runtime compatibility.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "v2" / "catalog.json"


def error(message: str) -> None:
    ERRORS.append(message)


def valid_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def run() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if catalog.get("schema_version") != 2:
        error("catalog: schema_version must be 2")
    specs = [
        pkg
        for pkg in catalog.get("packages", [])
        if pkg.get("vcu_family") == "VCU100"
    ]
    by_id = {pkg.get("id"): pkg for pkg in specs}
    loaded = {}
    total = 0

    if len(by_id) != len(specs):
        error("catalog: duplicate VCU100 package identifiers")

    for meta in specs:
        pid = meta.get("id", "")
        if not isinstance(pid, str) or not pid or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in pid):
            error(f"invalid package id: {pid!r}")
            continue
        path = ROOT / "v2" / "vcu100" / f"{pid}.json"
        if not path.is_file():
            error(f"{pid}: published file missing")
            continue
        data = path.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        if meta.get("sha256") != actual_hash:
            error(f"{pid}: SHA-256 mismatch")
        if meta.get("size_bytes") != len(data):
            error(f"{pid}: size_bytes mismatch")
        try:
            obj = json.loads(data.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            error(f"{pid}: invalid UTF-8/JSON: {exc}")
            continue
        loaded[pid] = obj
        for key, wanted in (
            ("schema_version", 2),
            ("package_id", pid),
            ("version", meta.get("version")),
            ("language", meta.get("language")),
            ("region", meta.get("region")),
            ("role", "specialized"),
            ("vcu_family", "VCU100"),
            ("package_type", "ishida-monolingual"),
        ):
            if obj.get(key) != wanted:
                error(f"{pid}: unexpected {key}: {obj.get(key)!r} != {wanted!r}")
        if meta.get("role") != "specialized" or meta.get("kind") != "ishida-monolingual":
            error(f"{pid}: invalid catalog role/kind")
        entries = obj.get("entries")
        if not isinstance(entries, list):
            error(f"{pid}: entries must be a list")
            continue
        total += len(entries)
        if meta.get("entry_count") != len(entries):
            error(f"{pid}: declared count differs from file")
        ids = set()
        meaning_keys = set()
        for i, entry in enumerate(entries, 1):
            if not isinstance(entry, dict):
                error(f"{pid}#{i}: entry not an object")
                continue
            for field in ("id", "text", "english_id", "english_sense_id", "description_en"):
                if not valid_text(entry.get(field)):
                    error(f"{pid}#{i}: missing {field}")
            if not isinstance(entry.get("topics"), list) or not entry["topics"]:
                error(f"{pid}#{i}: missing topics")
            if obj["language"] == "ja":
                if not valid_text(entry.get("reading")) or not valid_text(entry.get("romanization")):
                    error(f"{pid}#{i}: missing Japanese reading/romanization")
            if obj["language"] == "zh" and not valid_text(entry.get("romanization")):
                error(f"{pid}#{i}: missing Chinese pinyin")
            uid = entry.get("id")
            meaning = (entry.get("english_id"), entry.get("english_sense_id"))
            if uid in ids:
                error(f"{pid}#{i}: duplicate entry id {uid}")
            if meaning in meaning_keys:
                error(f"{pid}#{i}: duplicate meaning key {meaning}")
            ids.add(uid)
            meaning_keys.add(meaning)
        if meta.get("companion_package_id") and meta["companion_package_id"] not in by_id:
            error(f"{pid}: companion not found in VCU100 catalog")

    for meta in specs:
        pid = meta.get("id")
        obj = loaded.get(pid)
        if not obj:
            continue
        for partner_id in meta.get("requires", []):
            partner = loaded.get(partner_id)
            if not partner:
                error(f"{pid}: required companion {partner_id} missing")
                continue
            partner_keys = {
                (x.get("english_id"), x.get("english_sense_id"))
                for x in partner.get("entries", [])
                if isinstance(x, dict)
            }
            missing = [
                x.get("id")
                for x in obj.get("entries", [])
                if isinstance(x, dict)
                and (x.get("english_id"), x.get("english_sense_id")) not in partner_keys
            ]
            if missing:
                error(f"{pid}: {len(missing)} meanings unmatched in {partner_id} (first: {missing[:3]})")
    print(f"VCU100 catalog={catalog.get('version')} packages={len(specs)} entries={total}")
    for item in ERRORS:
        print("ERROR:", item, file=sys.stderr)
    if ERRORS:
        print(f"FAILED: {len(ERRORS)} errors", file=sys.stderr)
        return 1
    print("PASS: structure, IDs, hashes, sizes and declared bilingual links")
    print("NOTE: linguistic QA and Android end-to-end tests are separate gates")
    return 0


ERRORS: list[str] = []
if __name__ == "__main__":
    raise SystemExit(run())
