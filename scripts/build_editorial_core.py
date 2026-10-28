"""Builds the editorially reviewed en / pt-BR / ja core packages (v2 schema) from
curation/editorial/batches/*.txt, keeping English ids as the semantic pivot.

- English: headword unchanged; description_en = short everyday sense chosen by the review;
  level / frequency / vcu14_rank / environments preserved from the previous package.
- pt-BR and ja: translation of THAT sense (same english_id); old entries are not reused.
- Excluded ids (proper names, letter names, fragments, vague senses, regular inflections) are
  removed from the three packages; ids are never reassigned.
- ja: reading in kana (display), romanization (Hepburn) from the spoken form, and `speech`
  (kana sent to text-to-speech) when the particle pronunciation differs (は→わ, へ→え).
Run after build_monolingual_v2.py; updates v2/catalog.json hashes and counts.
"""
import json, hashlib, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from editorial_parse import load
from kana_romaji import romaji, to_hira

R = pathlib.Path(__file__).resolve().parents[1]
V2 = R / 'v2'
VERSION = '2.0.0'
KANA_ONLY = re.compile(r'^[぀-ヿ〜ー・、。！？\s（）]+$')
SPOKEN = {26: 'またわ', 53: 'それわだ', 292: 'じつわ', 719: 'ふつうわ', 2375: 'ふつうわ', 2594: 'ふつうわ', 1907: 'こんにちわ'}

rows, errs = load()
if errs:
    sys.exit('\n'.join(errs))

def pkg(name):
    return json.loads((V2 / f'{name}-core-v2.json').read_text(encoding='utf-8'))

en, pt, ja = pkg('en'), pkg('pt-BR'), pkg('ja')
num = lambda eid: int(eid.split(':')[-1])
old_pt = {num(e['english_id']): e for e in pt['entries']}
old_ja = {num(e['english_id']): e for e in ja['entries']}
missing = [e['id'] for e in en['entries'] if num(e['id']) not in rows]
if missing:
    sys.exit(f'not reviewed: {missing[:20]}')

stats = {'kept': 0, 'excluded': 0, 'pt': 0, 'ja': 0}
en_out, pt_out, ja_out = [], [], []
for e in en['entries']:
    n = num(e['id'])
    r = rows[n]
    if not r['keep']:
        stats['excluded'] += 1
        continue
    stats['kept'] += 1
    ne = {k: v for k, v in e.items() if k not in ('regional_senses',)}
    ne['description_en'] = r['desc']
    ne['part_of_speech'] = r['pos']
    ne['source_status'] = 'editorial-reviewed'
    if r['pos'] == 'exp':
        ne['kind'] = 'expression'
    en_out.append(ne)
    base = {'english_id': e['id'], 'english_sense_id': None, 'kind': ne['kind'], 'description_en': r['desc'],
            'level': e.get('level'), 'part_of_speech': r['pos'], 'source_status': 'editorial-reviewed', 'translation_confidence': 'editorial-reviewed'}
    if e.get('vcu14_rank'):
        base['vcu14_rank'] = e['vcu14_rank']
    if e.get('environments'):
        base['environments'] = e['environments']
    if r['pt']:
        o = old_pt.get(n, {})
        p = {'id': f'pt-BR:{e["id"]}', **base, 'text': r['pt'][0], 'alternatives': r['pt'][1:]}
        if o.get('text') == r['pt'][0] and o.get('frequency'):
            p['frequency'] = o['frequency']
        elif e.get('frequency'):
            p['frequency'] = {**e['frequency'], 'source': 'english-pivot'}
        pt_out.append(p)
        stats['pt'] += 1
    if r['ja']:
        o = old_ja.get(n, {})
        main = r['ja'][0]
        reading = to_hira(main) if KANA_ONLY.match(main) else r['reading']
        if KANA_ONLY.match(main):
            reading = main  # keep katakana words in katakana
        if main.startswith('〜') and not reading.startswith('〜'):
            reading = '〜' + reading
        spoken = r['spoken'] or SPOKEN.get(n)
        if spoken == reading:
            spoken = None
        if not spoken and len(reading) > 1 and reading.endswith('へ'):
            spoken = reading[:-1] + 'え'  # directional particle
        j = {'id': f'ja:{e["id"]}', **base, 'text': main, 'alternatives': r['ja'][1:], 'reading': reading,
             'romanization': romaji(spoken or reading)}
        if spoken:
            j['speech'] = spoken
        if o.get('text') == main:
            if o.get('classifications'):
                j['classifications'] = o['classifications']
            if o.get('frequency'):
                j['frequency'] = o['frequency']
        if 'frequency' not in j and e.get('frequency'):
            j['frequency'] = {**e['frequency'], 'source': 'english-pivot'}
        ja_out.append(j)
        stats['ja'] += 1

NOTE = ('Editorial review 2.0 (2026-10-27): every English entry reviewed one by one from the pivot; one everyday sense and a '
        'short explanation per id; pt-BR and ja translated from that sense; vague entries, proper names, letter names, '
        'fragments and regular inflections removed (ids never reused). Source: curation/editorial/batches.')
for p, rows_out in ((en, en_out), (pt, pt_out), (ja, ja_out)):
    p['entries'] = rows_out
    p['version'] = VERSION
    p['status'] = 'editorial-reviewed'
    p['notes'] = [NOTE] + [x for x in p.get('notes', []) if 'Editorial review' not in x]

out = {}
for name, p in (('en', en), ('pt-BR', pt), ('ja', ja)):
    text = json.dumps(p, ensure_ascii=False, separators=(',', ':'))
    (V2 / f'{name}-core-v2.json').write_text(text, encoding='utf-8')
    out[f'{name}-core-v2'] = (hashlib.sha256(text.encode('utf-8')).hexdigest(), len(p['entries']), len(text.encode('utf-8')))

cat_path = V2 / 'catalog.json'
cat = json.loads(cat_path.read_text(encoding='utf-8'))
for c in cat.get('packages', []):
    if c.get('id') in out:
        sha, count, size = out[c['id']]
        c['sha256'], c['entry_count'], c['version'], c['size_bytes'] = sha, count, VERSION, size
cat_path.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(stats), {k: v[1] for k, v in out.items()})
