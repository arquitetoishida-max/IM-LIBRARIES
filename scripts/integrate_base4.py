"""Integrates the BASE4 editorial review (LEXICON editorial/reviews/BASE4/resultados/*) into the four base
dictionaries (en, pt-BR, ja, zh) and promotes them to v2 (package version 2.2.0).

Alternatives are not added automatically: a reviewer's 'alt' list mixes synonyms with related words, and an
alternative is an accepted answer.
Rules (owner authorization, 09/11/2026 — integrate and publish; preserve ids and students' progress):
  * ids are never renamed or removed; excluded senses stay in the package with core_status 'retired'
    (hidden from study, kept for history/progress); vulgar/restricted ones get 'search_only'.
  * a text is replaced only when a reviewer row says 'ajustar' and the proposal parses to a clean form; the
    previous text becomes an alternative.  'alt' forms of any reviewed row are added as alternatives.
  * pending ambiguities get a short pt-BR sense hint (nativeExplain) when it does not reveal an answer;
    unresolved spurious ids stay retired.
  * ids of the manifest that a package lacks are added when the review includes them and the text is known;
    new senses (cand:* and DS-002 source rows marked 'novo') receive ids from ALLOC-006 (en:000003917+).
  * every entry receives study_tier / study_priority (LEXICON #21, MULTILANG #48).
Previous files are kept under v2/previous/ for rollback.

usage: python scripts/integrate_base4.py --lexicon <LEXICON> --nlp <dir with pykakasi+pypinyin> [--dry-run]
"""
import argparse
import collections
import csv
import glob
import hashlib
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import kana_romaji  # noqa: E402

LANGS = {'en': 'EN-US', 'pt-BR': 'PT-BR', 'ja': 'JA', 'zh': 'ZH'}
BASES = {
    'en': 'candidates/en/en-core-v2-2.2.0-candidate.EN-003.R137.HINTS.json',
    'ja': 'candidates/ja/ja-core-v2-2.2.0-candidate.JA-001.R137.JA-UNITS.HINTS.json',
    'pt-BR': 'v2/pt-BR-core-v2.json',
    'zh': 'v2/zh-core-v2.json',
}
VERSION = '2.2.0'
INCLUDE = {'incluir', 'vincular', 'temático', 'proposta contextual', 'reconciliar antes de exportar', 'proposta de sentido',
           'requer reconciliação', 'fora do núcleo'}
DOUBT = ('duplicata', 'divergentes', 'incerto', 'espúri', 'sem sentido', 'desconhecido')
TIERS = {'inicial': 0, 'cedo': 1, 'intermediário': 2, 'herdado': 2, 'tardio': 3, 'temático': 4, 'temático (Slang)': 4,
         'pendente': 3, 'restrito': 5}


def tier_rank(t):
    if t in TIERS:
        return TIERS[t]
    t = t.lower()
    if 'inicial' in t or 'núcleo' in t or 'básic' in t:
        return 0
    if 'estrutur' in t or 'cedo' in t or 'rotina' in t:
        return 1
    if 'tard' in t or 'avanç' in t:
        return 3
    return 2


def clean(a):
    return bool(a) and len(a) <= 40 and not re.search(r'[=:"“”?]|\.\.\.|…|\bNÃO\b|\bsem\b', a) and len(a.split()) <= 4


def parse(p):
    """'text [reading]; alt x, y (note)' → (primary, alternatives, reading) or None."""
    p = (p or '').strip()
    if not p or p.lower().startswith(('sem ', 'id sem', 'herdado', 'vincular')):
        return None
    p = p.split(' — ')[0]
    segs = [s.strip() for s in p.split(';')]
    first = segs[0]
    if re.search(r' = |:|→|\bNÃO\b|\?|\bé só\b', first):
        return None
    reading = None
    m = re.search(r'\[([^\]]+)\]', first)
    if m:
        reading = m.group(1).split('/')[0].strip()
        first = first.replace(m.group(0), '')
    first = re.sub(r'\([^)]*\)', '', first).strip()
    parts = [x.strip() for x in re.split(r'\s/\s|/', first) if x.strip()]
    if not parts or not clean(parts[0]):
        return None
    alts = parts[1:]
    for s in segs[1:]:
        if s.startswith('alt '):
            alts += [re.sub(r'\([^)]*\)', '', a).strip() for a in s[4:].split(',')]
    return parts[0], [a for a in alts if clean(a) and a != parts[0]], reading


def load_reviews(lex):
    base, lang, tier, order = {}, collections.defaultdict(dict), {}, []
    for d in sorted(glob.glob(os.path.join(lex, 'editorial/reviews/BASE4/resultados/*'))):
        f = os.path.join(d, 'sentidos.tsv')
        if os.path.exists(f):
            for r in csv.DictReader(open(f, encoding='utf-8'), delimiter='\t'):
                k = r['chave']
                if r['idioma'] == 'BASE':
                    base[k] = (r['decisao'], r['proposta'])
                    order.append(k)
                else:
                    lang[k][r['idioma']] = (r['decisao'], r['proposta'])
        f = os.path.join(d, 'ordem.tsv')
        if os.path.exists(f):
            for r in csv.DictReader(open(f, encoding='utf-8'), delimiter='\t'):
                tier.setdefault(r['chave'], r['decisao'])
    return base, lang, tier, order


def leaks(hint, answers):
    h = hint.lower()
    return any(a and len(a) > 1 and re.search(r'(?<![\w])' + re.escape(a.lower()) + r'(?![\w])', h) for a in answers)


def short_sense(s):
    s = re.sub(r'^(ID sem registro EN no núcleo v2; |sentido alocado \(ALLOC-001\)[^—]*— )', '', s)
    s = re.split(r' — |; |\. ', s)[0].strip()
    if re.match(r'(gloss|forma|provável|particípio|contração|plural|comparativo|superlativo|nome próprio)', s):
        return None
    return s if 3 <= len(s) <= 60 else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--lexicon', required=True)
    ap.add_argument('--nlp', required=True)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args(argv)
    sys.path.insert(0, a.nlp)
    import pykakasi
    from pypinyin import Style, pinyin
    kks = pykakasi.kakasi()

    READ = {'男の人': 'おとこのひと', '通った': 'とおった', 'アマゾン川': 'アマゾンがわ', '出どころ': 'でどころ', '女の人': 'おんなのひと'}

    def ja_reading(t):
        if t in READ:
            return READ[t]
        kata = re.compile(r'^[\u30a0-\u30ffー]+$')
        return ''.join(x['orig'] if kata.match(x['orig']) else x['hira'] for x in kks.convert(t))

    def zh_reading(t):
        return ''.join(x[0] for x in pinyin(t, style=Style.TONE))

    base, lang, tier, order = load_reviews(a.lexicon)
    U = {r['ID']: r for r in csv.DictReader(open(os.path.join(a.lexicon, 'editorial/00_master_index/DS-002.union.proposed.tsv'), encoding='utf-8'), delimiter='\t')}
    four = {}
    for r in csv.DictReader(open(os.path.join(a.lexicon, 'editorial/reviews/DS-002/four-pass.tsv'), encoding='utf-8'), delimiter='\t'):
        four.setdefault(r['ID fonte'], r)
    hints_file = os.path.join(a.lexicon, 'editorial/hints/pt-BR-sense-hints.tsv')
    hinted = set()
    for line in open(hints_file, encoding='utf-8'):
        if '\t' in line:
            hinted.add('en:%09d' % int(line.split('\t')[0]))

    pk = {l: json.load(open(os.path.join(ROOT, p), encoding='utf-8')) for l, p in BASES.items()}
    by = {l: {e['english_id']: e for e in pk[l]['entries']} for l in pk}
    rep = collections.Counter()

    # --- ids for new senses (ALLOC-006) --------------------------------------------------------------------------
    alloc_path = os.path.join(a.lexicon, 'editorial/allocations/ALLOC-006.json')
    if os.path.exists(alloc_path):
        alloc = json.load(open(alloc_path))['allocations']
    else:
        nxt = 3917
        alloc = {}
        for k in order:
            dec = base[k][0]
            if k.startswith('cand:') or (not k.startswith('en:') and dec == 'novo'):
                alloc[k] = 'en:%09d' % nxt
                nxt += 1
    links = {k: base[k][1].split(':', 1)[0].replace('vincular a ', '') for k in order if not k.startswith(('en:', 'cand:')) and base[k][0] == 'vincular'}

    def texts_for(k):
        out = {}
        for l, col in LANGS.items():
            d, p = lang.get(k, {}).get(col, ('', ''))
            if d in ('sem equivalente', 'restrito'):
                continue
            r = parse(p)
            if r is None and k in U and U[k].get(col):
                r = (U[k][col].split(';')[0].strip(), [], None)
            if r is None and k in four:
                src = four[k][{'EN-US': 'EN', 'PT-BR': 'PT'}.get(col, col)]
                r = (src.strip(), [], None) if src.strip() else None
            if r:
                out[l] = r
        return out

    # --- global order ---------------------------------------------------------------------------------------------
    def num(k):
        return int(k[3:]) if k.startswith('en:') else 0
    keys = [k for k in order if k.startswith('en:')] + list(alloc)
    prio = {}
    for i, k in enumerate(sorted(keys, key=lambda k: (tier_rank(tier.get(k, 'cedo')), num(k) or 4000 + keys.index(k)))):
        prio[alloc.get(k, k)] = i + 1
    tiers_of = {alloc.get(k, k): tier.get(k, 'cedo') for k in keys}

    def new_entry(l, eid, t, kind):
        prim, alts, reading = t
        e = {'id': eid if l == 'en' else '%s:%s' % (l, eid), 'english_id': eid, 'english_sense_id': None, 'kind': kind,
             'description_en': '', 'text': prim, 'alternatives': [], 'source_status': 'base4-reviewed',
             'translation_confidence': 'editorial-reviewed'}
        if l == 'ja':
            e['reading'] = reading or ja_reading(prim)
            e['romanization'] = kana_romaji.romaji(e['reading'])
        if l == 'zh':
            e['reading'] = e['romanization'] = zh_reading(prim)
        return e

    def set_text(l, e, prim, reading):
        # the replaced text was judged wrong or weaker by the reviewer: it is not kept as an accepted answer
        e['text'] = prim
        e['alternatives'] = [x for x in e.get('alternatives', []) if x != prim]
        if l == 'ja':
            e['reading'] = reading or ja_reading(prim)
            e['romanization'] = kana_romaji.romaji(e['reading'])
            e.pop('speech', None)
        if l == 'zh':
            e['reading'] = e['romanization'] = zh_reading(prim)

    for k in keys:
        eid = alloc.get(k, k)
        dec, prop = base.get(k, ('incluir', ''))
        missing_doubt = prop.startswith('ID sem registro EN') and any(w in prop for w in DOUBT)
        status = None
        if dec in ('excluir',) or missing_doubt or (dec == 'vincular' and prop.startswith('ID sem registro EN')):
            status = 'retired'
        elif dec == 'restrito':
            status = 'search_only'
        texts = texts_for(k)
        kind_new = 'expression' if len(texts.get('en', ('',))[0].split()) > 1 else 'word'
        for l, col in LANGS.items():
            e = by[l].get(eid)
            ldec = lang.get(k, {}).get(col, ('', ''))[0]
            if e is None:
                if status or dec not in INCLUDE | {'pendente', 'candidato novo', 'novo'} or l not in texts or 'en' not in texts or len(texts) < 3:
                    continue
                if dec == 'pendente' and k.startswith('en:') and not prop.startswith('ID sem registro EN'):
                    pass
                e = new_entry(l, eid, texts[l], kind_new)
                pk[l]['entries'].append(e)
                by[l][eid] = e
                rep['added_' + l] += 1
            else:
                if status and e.get('core_status') != status:
                    e['core_status'] = status
                    rep['status_' + status] += 1
                elif ldec == 'sem equivalente' and dec == 'vincular' and l != 'en' and not e.get('core_status'):
                    e['core_status'] = 'retired'
                    rep['retired_no_equivalent'] += 1
                p = lang.get(k, {}).get(col, ('', ''))[1]
                r = parse(p)
                if r:
                    prim, alts, reading = r
                    if ldec == 'ajustar' and prim != e['text'] and not prim.endswith('-'):
                        set_text(l, e, prim, reading)
                        rep['text_' + l] += 1
            e['study_tier'] = tiers_of[eid]
            e['study_priority'] = prio[eid]
        # sense hint for ambiguous senses (pt-BR natives)
        if dec in ('pendente', 'proposta de sentido', 'requer reconciliação') and eid not in hinted and not status:
            h = short_sense(prop)
            answers = [x for l in ('en', 'ja', 'zh') for e in [by[l].get(eid)] if e for x in [e['text'], *e.get('alternatives', [])]]
            if h and not leaks(h, answers):
                for l in ('en', 'ja', 'zh'):
                    e = by[l].get(eid)
                    if e is not None and 'pt-BR' not in (e.get('nativeExplain') or {}):
                        e.setdefault('nativeExplain', {})['pt-BR'] = h
                rep['hints'] += 1

    # entries outside the manifest keep their place after the reviewed ones
    for l in pk:
        for e in pk[l]['entries']:
            e.setdefault('study_priority', 100000 + int(re.sub(r'\D', '', e['english_id'])[-6:] or 0))
        pk[l]['version'] = VERSION
        pk[l]['status'] = 'published'
        pk[l].setdefault('notes', []).append('2.2.0: BASE4 review integrated (LEXICON #22): core_status retired/search_only, study_tier/study_priority, alternatives, sense hints, ALLOC-006 new senses.')

    print(json.dumps(rep, ensure_ascii=False, sort_keys=True))
    print('alloc', len(alloc), 'links', len(links))
    if a.dry_run:
        return
    alloc_doc = {'format': 'ishida-id-allocation', 'id': 'ALLOC-006', 'source': 'BASE4 cand:* and DS-002 P01/P02 rows marked novo',
                 'allocations': alloc, 'links': links}
    json.dump(alloc_doc, open(alloc_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(ROOT, 'v2/previous'), exist_ok=True)
    cat_path = os.path.join(ROOT, 'v2/catalog.json')
    cat = json.load(open(cat_path, encoding='utf-8'))
    for l in pk:
        dst = os.path.join(ROOT, 'v2/%s-core-v2.json' % l)
        prev = os.path.join(ROOT, 'v2/previous/%s-core-v2-2.1.1.json' % l)
        if not os.path.exists(prev):
            shutil.copy(dst, prev)
        b = json.dumps(pk[l], ensure_ascii=False, indent=1).encode('utf-8')
        open(dst, 'wb').write(b)
        for c in cat['packages']:
            if c['id'] == '%s-core-v2' % l:
                c.update({'sha256': hashlib.sha256(b).hexdigest(), 'size_bytes': len(b), 'version': VERSION,
                          'entry_count': len(pk[l]['entries'])})
    cat['version'] = '1.2.0'
    cat['notes'].append('1.2.0: en/pt-BR/ja/zh core 2.2.0 — BASE4 review integrated; previous 2.1.1 files in v2/previous/ for rollback.')
    open(cat_path, 'w', encoding='utf-8').write(json.dumps(cat, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
