#!/usr/bin/env python3
"""ISHIDA MULTILANG — build every monolingual V2 package and the single V2 discovery catalog.

Pivot: master/en-master-v1.json (3043 English entries, stable english_id; never renumbered).
For each target language the word that corresponds to an english_id is chosen from:
  1. editorial overrides already curated in languages/<locale>.json (function words, slang), then
  2. English Wiktionary translation tables (kaikki.org extraction, CC BY-SA), matched by sense, then
  3. machine translation of the headword (Argos Translate, offline, MIT/CC models) as a last resort,
     explicitly flagged translation_confidence="machine".
English descriptions that came from an unrelated WordNet synset (e.g. "in" = inch, "be" = beryllium)
are replaced by the main Wiktionary sense of the same headword; inflected forms point to their lemma.
Each entry also receives, when available: reading/romanization (ja kana+romaji, zh pinyin, ko/ru/ar/hi
romanization), lexical frequency (wordfreq Zipf, in the entry's own language), CEFR-like learning band
(approximate, from the English master) and community JLPT level for Japanese (OpenJLPT).
Core packages of languages without built-in app UI carry an "ui" dictionary (machine translated) so the
language can also be used as interface language.

Every external step is optional: a missing tool or network failure degrades coverage, never IDs.
A JSON report is written to docs/V2_BUILD_REPORT.json.
"""
import collections, datetime, gzip, hashlib, io, json, os, pathlib, re, sys, time, unicodedata, urllib.request

R = pathlib.Path(".")
OUT = R / "v2"
OUT.mkdir(exist_ok=True)
RAW = "https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/v2/"
KAIKKI = os.environ.get("KAIKKI_URL", "https://kaikki.org/dictionary/English/kaikki.org-dictionary-English.jsonl")
KAIKKI_FILE = os.environ.get("KAIKKI_FILE")  # local copy (tests / cache)
VERSION = os.environ.get("PKG_VERSION", "1.1.1")
UA = {"User-Agent": "ishida-multilang-library-builder/2.0 (+https://github.com/arquitetoishida-max/IM-LIBRARIES)"}
T0 = time.time()

def log(*a):
    print(f"[{time.time() - T0:7.1f}s]", *a, flush=True)

# ---------------------------------------------------------------- languages
LANGS = {
    # code: (wiktionary codes, wordfreq code, argos code, flag, locale, native, en, pt, ja, script)
    "en":    ([],             "en", None, "🇺🇸", "en-US", "English", "English", "Inglês", "英語", "latin"),
    "pt-BR": (["pt"],         "pt", "pt", "🇧🇷", "pt-BR", "Português (Brasil)", "Portuguese (Brazil)", "Port. (Brasileiro)", "ポルトガル語（ブラジル）", "latin"),
    "pt-PT": (["pt"],         "pt", "pt", "🇵🇹", "pt-PT", "Português (Portugal)", "Portuguese (Portugal)", "Português (Portugal)", "ポルトガル語（ポルトガル）", "latin"),
    "ja":    (["ja"],         "ja", "ja", "🇯🇵", "ja-JP", "日本語", "Japanese", "Japonês", "日本語", "japanese"),
    "es":    (["es"],         "es", "es", "🇪🇸", "es-ES", "Español", "Spanish", "Espanhol", "スペイン語", "latin"),
    "fr":    (["fr"],         "fr", "fr", "🇫🇷", "fr-FR", "Français", "French", "Francês", "フランス語", "latin"),
    "it":    (["it"],         "it", "it", "🇮🇹", "it-IT", "Italiano", "Italian", "Italiano", "イタリア語", "latin"),
    "de":    (["de"],         "de", "de", "🇩🇪", "de-DE", "Deutsch", "German", "Alemão", "ドイツ語", "latin"),
    "zh":    (["cmn", "zh"],  "zh", "zh", "🇨🇳", "zh-CN", "中文（普通话）", "Mandarin Chinese", "Mandarim", "中国語（標準語）", "han"),
    "ko":    (["ko"],         "ko", "ko", "🇰🇷", "ko-KR", "한국어", "Korean", "Coreano", "韓国語", "hangul"),
    "ru":    (["ru"],         "ru", "ru", "🇷🇺", "ru-RU", "Русский", "Russian", "Russo", "ロシア語", "cyrillic"),
    "ar":    (["ar"],         "ar", "ar", "🇸🇦", "ar-SA", "العربية", "Arabic", "Árabe", "アラビア語", "arabic"),
    "hi":    (["hi"],         "hi", "hi", "🇮🇳", "hi-IN", "हिन्दी", "Hindi", "Hindi", "ヒンディー語", "devanagari"),
}
TARGETS = [c for c in LANGS if c != "en"]
UI_BUILTIN = {"en", "ja", "pt-BR", "pt-PT"}  # the app ships these interface languages itself

def lang_info(code):
    w, wf, ar, flag, loc, native, en, pt, ja, script = LANGS[code]
    return {"code": code, "flag": flag, "locale": loc, "name_native": native, "name_en": en, "name_pt": pt, "name_ja": ja, "script": script}

# ---------------------------------------------------------------- optional tools
try:
    from wordfreq import zipf_frequency
except Exception as exc:
    log("wordfreq unavailable:", exc); zipf_frequency = None
try:
    import pykakasi
    KKS = pykakasi.kakasi()
except Exception as exc:
    log("pykakasi unavailable:", exc); KKS = None
try:
    from pypinyin import pinyin as _pinyin, Style as _PStyle
except Exception as exc:
    log("pypinyin unavailable:", exc); _pinyin = None
try:
    import orjson
    loads = orjson.loads
except Exception:
    loads = json.loads

def zipf(text, code):
    if not zipf_frequency or not text:
        return None
    try:
        z = zipf_frequency(text, LANGS[code][1])
        return round(z, 2) if z > 0 else None
    except Exception:
        return None

def ja_reading(text):
    if not KKS or not text:
        return "", ""
    try:
        items = KKS.convert(text)
        return "".join(i["hira"] for i in items), "".join(i["hepburn"] for i in items)
    except Exception:
        return "", ""

def zh_pinyin(text):
    if not _pinyin or not text:
        return ""
    try:
        return " ".join(s[0] for s in _pinyin(text, style=_PStyle.TONE))
    except Exception:
        return ""

RU = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя", ["a","b","v","g","d","e","yo","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f","kh","ts","ch","sh","shch","","y","","e","yu","ya"]))
def ru_roman(text):
    return "".join(RU.get(ch.lower(), ch) for ch in text)

def strip_marks(text):
    """Remove Russian stress accents (combining acute) without touching other diacritics."""
    return unicodedata.normalize("NFC", "".join(ch for ch in unicodedata.normalize("NFD", text) if ch != "́"))

PREFIX = re.compile(r"^\s*(?:EN|PT|JA|ES|FR|IT|DE|ZH|KO|RU)(?:-[A-Z]{2})?\s*:\s+")
def clean_word(w):
    w = re.sub(r"\[[^\]]*\]|\{[^}]*\}", "", w or "")
    w = re.sub(r"\s*\([^)]*\)\s*", " ", w)
    w = PREFIX.sub("", w)
    w = re.sub(r"\s+", " ", w).strip(" ,;/.:!*–—-") if len(w) > 1 else w
    return w

def clean_gloss(g, limit=140):
    g = re.sub(r"\s+", " ", g or "").strip()
    g = re.sub(r"\s*;\s*;+", ";", g).strip(" ;")
    if len(g) > limit:
        cut = g[:limit].rsplit(" ", 1)[0]
        g = cut.rstrip(",;:") + "…"
    if g and g[0].islower():
        g = g[0].upper() + g[1:]
    if g and g[-1] not in ".!?…":
        g += "."
    return g

# ---------------------------------------------------------------- master
EN = json.loads((R / "master/en-master-v1.json").read_text(encoding="utf-8"))
MASTER = [e for e in EN["entries"] if e.get("english_id")]
log("master entries", len(MASTER))

def editorial(locale):
    p = R / "languages" / f"{locale}.json"
    if not p.exists():
        return {}
    out = {}
    for e in json.loads(p.read_text(encoding="utf-8"))["entries"]:
        if e.get("source") == "editorial-example" and e.get("text"):
            parts = [x.strip() for x in e["text"].split(";") if x.strip()]
            out[e["english_id"]] = parts
    return out

EDITORIAL = {"pt-BR": editorial("pt-BR"), "ja": editorial("ja")}
# European Portuguese shares most editorial function words; differences are handled by Wiktionary tags.
EDITORIAL["pt-PT"] = {k: [("tu" if x == "você" else x) for x in v] for k, v in EDITORIAL["pt-BR"].items()}

# ---------------------------------------------------------------- lemma candidates
heads = {e["headword"].lower() for e in MASTER}
def lemma_guesses(w):
    g = set()
    for suf, rep in (("ies", "y"), ("es", ""), ("s", ""), ("ied", "y"), ("ed", ""), ("ed", "e"), ("ing", ""), ("ing", "e"), ("er", ""), ("est", ""), ("ly", ""), ("'s", "")):
        if w.endswith(suf) and len(w) - len(suf) >= 2:
            g.add(w[: -len(suf)] + rep)
    if re.search(r"(.)\1(ed|ing)$", w):
        g.add(re.sub(r"(.)\1(ed|ing)$", r"\1", w))
    return g
wanted = set(heads)
for h in list(heads):
    wanted |= lemma_guesses(h)

# ---------------------------------------------------------------- Wiktionary (kaikki) pass
WCODES = {c for t in TARGETS for c in LANGS[t][0]}
BAD_POS = {"name", "symbol", "character", "letter", "prefix", "suffix", "infix", "affix", "interfix", "abbrev", "punct", "romanization"}
BAD_TAGS = {"obsolete", "archaic", "rare", "dialectal", "abbreviation", "initialism", "acronym", "symbol", "misspelling", "nonstandard", "dated", "historical", "proscribed"}
records = collections.defaultdict(list)

def keep_translation(t):
    code = t.get("lang_code") or t.get("code")
    if code not in WCODES:
        return None
    word = t.get("word") or ""
    if not word or len(word) > 60:
        return None
    return {"code": code, "word": word, "sense": t.get("sense") or "", "tags": t.get("tags") or [],
            "roman": t.get("roman") or "", "alt": t.get("alt") or "", "lang": t.get("lang") or ""}

def kaikki_lines():
    if KAIKKI_FILE:
        op = gzip.open if KAIKKI_FILE.endswith(".gz") else open
        with op(KAIKKI_FILE, "rb") as f:
            yield from f
        return
    req = urllib.request.Request(KAIKKI, headers=UA)
    with urllib.request.urlopen(req, timeout=300) as stream:
        src = gzip.GzipFile(fileobj=stream) if KAIKKI.endswith(".gz") else stream
        for line in io.BufferedReader(src, buffer_size=1 << 20):
            yield line

WORD_RE = re.compile(rb'"word": ?"((?:[^"\\]|\\.)*)"')
kaikki_ok = False
try:
    n = 0
    for line in kaikki_lines():
        n += 1
        if n % 200000 == 0:
            log("kaikki lines", n, "matched words", len(records))
        # cheap prefilter on the word field before a full parse
        hit = False
        for m in WORD_RE.finditer(line):
            try:
                if json.loads(b'"' + m.group(1) + b'"').lower() in wanted:
                    hit = True
                    break
            except Exception:
                continue
        if not hit:
            continue
        d = loads(line)
        if d.get("lang_code", "en") != "en" or (d.get("word") or "").lower() not in wanted:
            continue
        senses = []
        trans = []
        for t in d.get("translations") or []:
            k = keep_translation(t)
            if k: trans.append(k)
        for s in d.get("senses") or []:
            gl = s.get("glosses") or s.get("raw_glosses") or []
            senses.append({"gloss": gl[-1] if gl else "", "tags": s.get("tags") or [],
                           "form_of": [f.get("word") for f in (s.get("form_of") or []) + (s.get("alt_of") or []) if f.get("word")]})
            for t in s.get("translations") or []:
                k = keep_translation(t)
                if k:
                    k["sense"] = k["sense"] or (gl[-1] if gl else "")
                    trans.append(k)
        records[d["word"].lower()].append({"word": d["word"], "pos": d.get("pos") or "", "senses": senses, "trans": trans})
    kaikki_ok = len(records) >= int(os.environ.get("KAIKKI_MIN", "1000"))
    log("kaikki done, lines", n, "words", len(records))
except Exception as exc:
    log("kaikki failed:", repr(exc))

def usable_senses(rec):
    return [s for s in rec["senses"] if s["gloss"] and not (set(s["tags"]) & BAD_TAGS)]

def main_record(head):
    """First usable record in page order, preferring exact case and lemma (non form-of) senses."""
    recs = [r for r in records.get(head.lower(), []) if r["pos"] not in BAD_POS and usable_senses(r)]
    if not recs:
        return None
    exact = [r for r in recs if r["word"] == head] or recs
    lemma = [r for r in exact if any(not s["form_of"] for s in usable_senses(r))]
    return (lemma or exact)[0]

def resolve(head, depth=0):
    """Return (record, sense, lemma_word) for a headword, following form-of links once."""
    rec = main_record(head)
    if not rec:
        return None, None, None
    us = usable_senses(rec)
    if us and not us[0]["form_of"]:
        return rec, us[0], None
    lemma = us[0]["form_of"][0] if us and us[0]["form_of"] else None
    if lemma and depth == 0:
        lrec, lsense, _ = resolve(lemma, 1)
        if lrec:
            return lrec, lsense, lemma
    return rec, us[0] if us else None, None

SCRIPT = {"ja": r"[\u3040-\u30ff\u4e00-\u9fff]", "zh": r"[\u4e00-\u9fff]", "ko": r"[\uac00-\ud7af]", "ru": r"[\u0400-\u04ff]",
          "ar": r"[\u0600-\u06ff]", "hi": r"[\u0900-\u097f]"}
NOTE = re.compile(r"\b(imperative|implied|literally|see|used|plural|singular|form of|abbreviation|informal|formal)\b", re.I)
ARTICLELESS = {"zh", "ko", "ru", "hi", "ar"}

def valid_for(locale, w, english=""):
    """Reject affixes, notes, wrong scripts, untranslated English and junk symbols."""
    if not w or len(w) > 50 or w[0] in "-–—" or w.endswith("-") or any(c in w for c in "#*…") or "..." in w:
        return False
    if re.fullmatch(r"(.{1,3})\1{2,}", w.replace(" ", "")) or re.fullmatch(r"(\S+)( \1)+", w):  # "ママママ", "엄마 엄마"
        return False
    if english and w.strip().lower() == english.strip().lower() and locale not in ("pt-BR", "pt-PT", "es", "fr", "it", "de"):
        return False
    pat = SCRIPT.get(locale)
    if pat:
        if not re.search(pat, w) or re.search(r"[A-Za-z]", w):
            return False
        if locale == "zh" and re.search(r"[\u0400-\u04ff\U00020000-\U0002ffff]", w):
            return False
    else:
        if not re.search(r"[A-Za-zÀ-ÿ]", w) or NOTE.search(w) or re.search(r"[\u0400-\u04ff\u3040-\u9fff]", w):
            return False
    return True

TOKEN = re.compile(r"[a-z]+")
STOP = set("a an the of to or and in on for with by as is be that this which something someone from at into".split())
def overlap(a, b):
    ta = {t for t in TOKEN.findall(a.lower()) if t not in STOP}
    tb = {t for t in TOKEN.findall(b.lower()) if t not in STOP}
    return len(ta & tb)

def pick_translation(rec_list, sense_gloss, locale):
    """Choose a translation for `locale` from translation tables, preferring the table whose sense matches."""
    codes = LANGS[locale][0]
    for rec in rec_list:
        groups = collections.OrderedDict()
        for t in rec["trans"]:
            if t["code"] in codes:
                groups.setdefault(t["sense"], []).append(t)
        if not groups:
            continue
        sizes = collections.Counter(t["sense"] for t in rec["trans"])
        ranked = sorted(enumerate(groups.items()), key=lambda it: (-overlap(it[1][0], sense_gloss), -min(sizes[it[1][0]], 12), it[0]))
        _, (sense, items) = ranked[0]
        def score(t):
            tags = {x.lower() for x in t["tags"]}
            s = 0
            if tags & {"obsolete", "archaic", "rare", "dated", "vulgar", "derogatory", "offensive"}: s += 10
            if locale == "pt-BR":
                if "portugal" in tags or "european-portuguese" in tags: s += 5
                if "brazil" in tags or "brazilian-portuguese" in tags: s -= 2
            if locale == "pt-PT":
                if "brazil" in tags or "brazilian-portuguese" in tags: s += 5
                if "portugal" in tags or "european-portuguese" in tags: s -= 2
            if locale == "zh":
                if any("traditional" in x for x in tags): s += 3
                if t["code"] != "cmn" and t["lang"] not in ("Mandarin", "Chinese Mandarin", "Chinese"): s += 4
            return s
        items = sorted(items, key=score)
        words, seen = [], set()
        best = None
        for t in items:
            w = clean_word(t["word"])
            if locale == "ru":
                w = strip_marks(w)
            if locale == "zh" and "/" in w:
                w = w.split("/")[-1].strip()  # "Traditional / Simplified" → simplified
            if not valid_for(locale, w) or w.lower() in seen:
                continue
            seen.add(w.lower())
            if best is None:
                best = t
            words.append(w)
        if words:
            return words[0], words[1:4], best, sense
    return None, [], None, None

# ---------------------------------------------------------------- machine translation fallback (Argos)
ARGOS = {}
def argos_translator(code):
    if code in ARGOS:
        return ARGOS[code]
    ARGOS[code] = None
    if os.environ.get("NO_ARGOS"):
        return None
    try:
        import argostranslate.package as ap, argostranslate.translate as at
        if not getattr(argos_translator, "_index", False):
            ap.update_package_index(); argos_translator._index = True
        tgt = LANGS[code][2]
        installed = [l.code for l in at.get_installed_languages()]
        if tgt not in installed:
            pkg = next((p for p in ap.get_available_packages() if p.from_code == "en" and p.to_code == tgt), None)
            if pkg is None:
                log("argos: no model en->" + tgt); return None
            ap.install_from_path(pkg.download())
        tr = at.get_translation_from_codes("en", tgt)
        ARGOS[code] = tr
        log("argos ready en->" + tgt)
    except Exception as exc:
        log("argos unavailable for", code, repr(exc))
    return ARGOS[code]

def mt(text, code):
    tr = argos_translator(code)
    if not tr:
        return None
    try:
        out = tr.translate(text).strip()
        return out or None
    except Exception:
        return None

# ---------------------------------------------------------------- OpenJLPT (community JLPT levels)
JLPT = {}
try:
    for lv in ("n5", "n4", "n3", "n2", "n1"):
        url = f"https://raw.githubusercontent.com/evanclan/OpenJLPT/main/data/json/vocab/{lv}.json"
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as s:
            for row in json.load(s):
                for key in (row.get("word"), row.get("reading")):
                    if key and key not in JLPT:
                        JLPT[key] = lv.upper()
    log("OpenJLPT terms", len(JLPT))
except Exception as exc:
    log("OpenJLPT unavailable:", repr(exc))

# ---------------------------------------------------------------- English core
report = {"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "kaikki": kaikki_ok, "languages": {}}
resolved = {}
fixed_desc = 0
en_rows = []
for e in MASTER:
    head = e["headword"]
    eid = e["english_id"]
    curated = e.get("definition_status") == "editorial-grammar-gloss" or e.get("category") == "regional-colloquial"
    desc = e.get("description_short_english") or e.get("short_description_en") or ""
    rec, sense, lemma = resolve(head) if kaikki_ok else (None, None, None)
    resolved[eid] = (rec, sense, lemma)
    if not curated and sense and sense["gloss"]:
        g = clean_gloss(sense["gloss"])
        desc = (f"Form of “{lemma}”: " + g) if lemma else g
        fixed_desc += 1
    row = {"id": eid, "english_id": eid, "text": head, "kind": "expression" if e.get("category") == "regional-colloquial" else "word",
           "description_en": desc or clean_gloss(head), "level": e.get("cefr"), "region_tags": e.get("regions", []),
           "regional_senses": e.get("regional_senses", []),
           "source_status": "editorial" if curated else ("wiktionary-sense" if sense else e.get("mapping_status", "lexical-headword-unresolved"))}
    if lemma:
        row["lemma"] = lemma
    z = zipf(head, "en")
    if z:
        row["frequency"] = {"zipf": z, "source": "wordfreq"}
    en_rows.append(row)
# Preserve editorial VCU14 metadata on all future catalog rebuilds.
# This overlay is independent of original English IDs and never adds unreviewed headwords.
vcu14_file = R / "curation/VCU14_EN_CANDIDATES_V3.json"
if vcu14_file.exists():
    vcu14 = json.loads(vcu14_file.read_text(encoding="utf-8"))
    vcu14_by_id = {r["id"]: r for r in vcu14.get("entries", []) if r.get("id")}
    vcu14_tagged = 0
    for row in en_rows:
        tag = vcu14_by_id.get(row["english_id"])
        if tag:
            row["vcu14_rank"] = int(tag["rank"])
            row["environments"] = sorted(set(tag.get("topics", [])))
            row["vcu14_status"] = "provisional-editorial"
            vcu14_tagged += 1
    report["vcu14_tagged_existing"] = vcu14_tagged

report["english_descriptions_replaced"] = fixed_desc
EN_BY_ID = {r["english_id"]: r for r in en_rows}

# ---------------------------------------------------------------- target languages
def build_language(locale):
    rows, stats = [], collections.Counter()
    for e in MASTER:
        eid = e["english_id"]
        head = e["headword"]
        rec, sense, lemma = resolved.get(eid, (None, None, None))
        en_row = EN_BY_ID[eid]
        text, alts, conf, src, roman_hint, alt_hint, tsense = None, [], None, None, "", "", None
        ed = EDITORIAL.get(locale, {}).get(eid)
        if ed:
            text, alts, conf, src = ed[0], ed[1:4], "editorial", "editorial"
        elif rec and not (locale in ARTICLELESS and head.lower() in ("the", "a", "an")):
            pool = [rec] + [r for r in records.get(head.lower(), []) if r is not rec and r["pos"] not in BAD_POS]
            text, alts, best, tsense = pick_translation(pool, sense["gloss"] if sense else "", locale)
            if text:
                conf, src = "approximate", "wiktionary"
                roman_hint, alt_hint = best.get("roman", ""), best.get("alt", "")
        if not text and not (locale in ARTICLELESS and head.lower() in ("the", "a", "an")):
            m = mt(lemma or head, locale)
            m = clean_word(m) if m else None
            if m and valid_for(locale, m, lemma or head):
                text, conf, src = m, "machine", "argos-translate"
        if not text:
            stats["missing"] += 1
            continue
        stats[src] += 1
        row = {"id": f"{locale}:{eid}", "english_id": eid, "english_sense_id": None, "text": text,
               "kind": en_row["kind"], "description_en": en_row["description_en"], "level": e.get("cefr"),
               "alternatives": [a for a in alts if a and a != text], "source_status": src,
               "translation_confidence": conf}
        if tsense:
            row["sense_note_en"] = tsense[:120]
        if locale == "ja":
            kana = alt_hint if alt_hint and re.fullmatch(r"[぀-ヿー・\s]+", alt_hint) else ""
            if not kana and re.fullmatch(r"[぀-ヿー]+", text):
                kana = text
            hira, hep = ja_reading(text)
            row["reading"] = kana or hira or ""
            rom = ja_reading(row["reading"])[1] if row["reading"] else ""
            row["romanization"] = rom or hep or roman_hint or ""
            lv = JLPT.get(text) or (JLPT.get(row["reading"]) if row["reading"] and row["reading"] != text and not re.search(r"[一-鿿]", text) else None)
            if lv:
                row["classifications"] = [{"system": "JLPT", "level": lv, "status": "community", "source": "OpenJLPT (CC BY-SA 4.0)"}]
                stats["jlpt"] += 1
        elif locale == "zh":
            row["reading"] = roman_hint or zh_pinyin(text)
        elif locale == "ru":
            row["reading"] = roman_hint or ru_roman(text)
        elif locale in ("ko", "ar", "hi") and roman_hint:
            row["reading"] = roman_hint
        z = zipf(text, locale)
        if z:
            row["frequency"] = {"zipf": z, "source": "wordfreq"}
            stats["frequency"] += 1
        rows.append(row)
    return rows, stats

# ---------------------------------------------------------------- UI dictionaries
UI_SRC = json.loads((R / "ui/strings.json").read_text(encoding="utf-8")) if (R / "ui/strings.json").exists() else {}
def ui_for(locale):
    if locale in UI_BUILTIN or not UI_SRC:
        return None
    tr = argos_translator(locale)
    if not tr:
        return None
    out = {}
    for key, v in UI_SRC.items():
        en = v.get("en") or ""
        if not en.strip():
            continue
        core = en.strip()
        caps = core.isupper() and len(core) > 3
        try:
            t = tr.translate(core.capitalize() if caps else core).strip()
        except Exception:
            continue
        if caps:
            t = t.upper()
        if not t:
            continue
        lead = en[: len(en) - len(en.lstrip())]
        trail = en[len(en.rstrip()):]
        if core.endswith(":") and not t.endswith((":", "：")):
            t += ":"
        out[key] = lead + t + trail
    return out

# ---------------------------------------------------------------- write packages + catalog
catalog = []
def save(pid, name, lang, rows, region=None, role="core", ui=None, sources=None, license_=None):
    payload = {"schema_version": 2, "package_id": pid, "package_type": "ishida-monolingual", "language": lang, "region": region,
               "name": name, "version": VERSION, "english_explanations": True, "status": "approximate-functional",
               "language_info": lang_info(lang), "role": role,
               "license": license_ or "CC BY-SA 4.0 (Wiktionary via kaikki.org; WordNet-derived English master; wordfreq data)",
               "sources": sources or ["ISHIDA English master v1", "English Wiktionary translation tables (kaikki.org)", "wordfreq (Zipf)"],
               "notes": ["Approximate learning levels. Word pairs are matched by english_id and may be approximate.",
                         "translation_confidence: editorial (curated), approximate (dictionary), machine (Argos Translate fallback)."],
               "entries": rows}
    if ui:
        payload["ui"] = ui
        payload["ui_status"] = "machine-translated"
    path = OUT / f"{pid}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    info = lang_info(lang)
    catalog.append({"id": pid, "name": name, "language": lang, "region": region, "role": role,
                    "kind": "ishida-monolingual", "schema_version": 2, "available": len(rows) > 0,
                    "entry_count": len(rows), "has_ui": bool(ui), "flag": info["flag"], "locale": info["locale"],
                    "name_native": info["name_native"], "name_en": info["name_en"], "name_pt": info["name_pt"], "name_ja": info["name_ja"],
                    "url": RAW + f"{pid}.json", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "version": VERSION})

NAMES = {"en": "English — core and expressions", "pt-BR": "Português brasileiro — vocabulário", "pt-PT": "Português europeu — vocabulário",
         "ja": "日本語 — 語彙", "es": "Español — vocabulario", "fr": "Français — vocabulaire", "it": "Italiano — vocabolario",
         "de": "Deutsch — Wortschatz", "zh": "中文 — 词汇", "ko": "한국어 — 어휘", "ru": "Русский — лексика", "ar": "العربية — مفردات", "hi": "हिन्दी — शब्दावली"}

save("en-core-v2", NAMES["en"], "en", en_rows)
report["languages"]["en"] = {"entries": len(en_rows), "frequency": sum(1 for r in en_rows if r.get("frequency"))}
only = set(sys.argv[1:])
for loc in TARGETS:
    if only and loc not in only:
        continue
    rows, stats = build_language(loc)
    min_rows = 300 if kaikki_ok else 1
    if len(rows) < min_rows and loc not in ("pt-BR", "ja"):
        log(f"[skip] {loc}: only {len(rows)} rows"); report["languages"][loc] = {"skipped": len(rows), **stats}; continue
    ui = ui_for(loc)
    save(f"{loc}-core-v2", NAMES[loc], loc, rows, ui=ui,
         sources=["ISHIDA English master v1 (english_id pivot)", "English Wiktionary translation tables (kaikki.org, CC BY-SA)",
                  "Argos Translate (fallback, marked machine)", "wordfreq (Zipf)"] + (["OpenJLPT (community JLPT levels)", "pykakasi readings"] if loc == "ja" else []))
    sample = rows[:: max(1, len(rows) // 40)][:40]
    report["languages"][loc] = {"entries": len(rows), "ui_strings": len(ui or {}), **stats,
                                "sample": [f"{EN_BY_ID[r['english_id']]['text']} → {r['text']} ({r['translation_confidence']})" for r in sample]}
    log(loc, len(rows), dict(stats))

# Regional packs: content packs of an existing language (ids unchanged from the first V2 generation).
regions = {"en-US-NY": ("New York — slang and expressions", ["US-NY"]), "en-US-CA": ("California — slang and expressions", ["US-CA"]),
           "en-US-TX": ("Texas — slang and expressions", ["US-TX"]), "en-GB": ("United Kingdom — slang and expressions", ["GB"])}
for tag, (name, codes) in regions.items():
    rows = []
    for e in en_rows:
        if e["kind"] == "expression" and any(c in e.get("region_tags", []) for c in codes):
            rows.append(dict(e, region_tags=codes))
        for s in e.get("regional_senses", []):
            if any(c in s.get("regions", []) for c in codes):
                rows.append({"id": e["id"] + ":regional:" + str(len(rows)), "english_id": e["english_id"], "text": e["text"], "kind": "expression",
                             "description_en": s["definition_en"], "region_tags": s["regions"], "source_status": "regional-provisional"})
    if rows:
        save(tag + "-slang-v2", name, "en", rows, region=tag, role="regional")

manifest = {"schema_version": 2, "format": "ishida-monolingual-only", "version": VERSION,
            "discovery_rule": "available == true and kind == ishida-monolingual and schema_version == 2",
            "packages": catalog,
            "notes": ["Only these downloadable monolingual packages are supported.",
                      "English explanations (description_en) are translated on demand by the app into the native language.",
                      "Word cards require the same english_id in both languages; meanings are approximate.",
                      "Regional packs are content packs of an existing language, not new language codes.",
                      "Packages with has_ui=true also provide interface translations (machine translated)."]}
(OUT / "catalog.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(R / "docs").mkdir(exist_ok=True)
(R / "docs/V2_BUILD_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
log("catalog", [(c["id"], c["entry_count"]) for c in catalog])
