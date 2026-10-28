"""Builds the editorially reviewed en / pt-BR / ja core packages (v2 schema) from
curation/editorial/batches/*.txt, keeping English ids as the semantic pivot.

- English: headword unchanged; description_en = short everyday sense chosen by the review;
  level / vcu14_rank / environments / vcu14_status preserved from the previous package; imported frequency
  data, machine-translated UI strings and old third-party metadata are dropped.
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
VERSION = '2.1.0'
KANA_ONLY = re.compile(r'^[぀-ヿ〜ー・、。！？\s（）]+$')
SPOKEN = {26: 'またわ', 53: 'それわだ', 292: 'じつわ', 719: 'ふつうわ', 2375: 'ふつうわ', 2594: 'ふつうわ', 1907: 'こんにちわ'}

rows, errs = load()
if errs:
    sys.exit('\n'.join(errs))

def pkg(name):
    return json.loads((V2 / f'{name}-core-v2.json').read_text(encoding='utf-8'))

en, pt, ja, zh = pkg('en'), pkg('pt-BR'), pkg('ja'), pkg('zh')
num = lambda eid: int(eid.split(':')[-1])
old_pt = {num(e['english_id']): e for e in pt['entries']}
old_ja = {num(e['english_id']): e for e in ja['entries']}
missing = [e['id'] for e in en['entries'] if num(e['id']) not in rows]
if missing:
    sys.exit(f'not reviewed: {missing[:20]}')

stats = {'kept': 0, 'excluded': 0, 'pt': 0, 'ja': 0, 'zh': 0}
en_out, pt_out, ja_out, zh_out = [], [], [], []
# Mandarin (simplified): curation/editorial/zh/z*.txt — N|hanzi;alternatives|pinyin (tone marks); empty = no equivalent
ZH = {}
for f in sorted((R / 'curation/editorial/zh').glob('z*.txt')):
    for line in f.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        n, hz, py = line.split('|')
        ZH[int(n)] = ([x.strip() for x in hz.split(';') if x.strip()], py.strip())
old_zh = {num(e['english_id']): e for e in zh['entries']}
for e in en['entries']:
    n = num(e['id'])
    r = rows[n]
    if not r['keep']:
        stats['excluded'] += 1
        continue
    stats['kept'] += 1
    ne = {k: v for k, v in e.items() if k not in ('regional_senses', 'frequency', 'zipf')}
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
    if e.get('vcu14_status'):
        base['vcu14_status'] = e['vcu14_status']
    if r['pt']:
        o = old_pt.get(n, {})
        p = {'id': f'pt-BR:{e["id"]}', **base, 'text': r['pt'][0], 'alternatives': r['pt'][1:]}
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
        ja_out.append(j)
        stats['ja'] += 1
    if n not in ZH:
        sys.exit(f'zh missing for {n}')
    hz, py = ZH[n]
    if hz:
        o = old_zh.get(n, {})
        z = {'id': f'zh:{e["id"]}', **base, 'text': hz[0], 'alternatives': hz[1:], 'reading': py, 'romanization': py}
        zh_out.append(z)
        stats['zh'] += 1

NOTE = ('ISHIDA MULTILANG editorial dictionary 2.0 (2026-10): every English pivot entry reviewed one by one; one everyday '
        'sense and a short English explanation per id; pt-BR, ja and zh written from that sense. Ids are stable and never reused. '
        'Source of truth: curation/editorial (batches, zh). Old imported definitions, machine translations and frequency data are not used.')
OWN_LICENSE = 'ISHIDA MULTILANG editorial content, (c) 2026 ISHIDA MULTILANG. Use and redistribution under the project terms (legal/terms.html).'
LEVEL_NOTE = ('level = approximate CEFR-style learning band (A1-C2), originally estimated from the headword list rank at selection time; '
              'JLPT/HSK/CEFR are didactic references only, not official certification lists. No frequency values are distributed.')
THIRD = {'ja': ['JLPT levels (classifications field): OpenJLPT community lists, CC BY-SA 4.0 — approximate, not official.']}
for p, rows_out in ((en, en_out), (pt, pt_out), (ja, ja_out), (zh, zh_out)):
    p['entries'] = rows_out
    p['version'] = VERSION
    p['status'] = 'editorial-reviewed'
    p['license'] = OWN_LICENSE
    p['sources'] = ['ISHIDA MULTILANG editorial review 2.0 (English pivot ids)', 'VCU14 everyday-vocabulary ranking and environments (ISHIDA MULTILANG)']
    p['notes'] = [NOTE, LEVEL_NOTE]
    tp = THIRD.get(p['language'])
    if tp:
        p['third_party'] = tp
    else:
        p.pop('third_party', None)
    for k in ('english_explanations_source', 'frequency_source', 'ui', 'ui_status'):
        p.pop(k, None)

out = {}
for name, p in (('en', en), ('pt-BR', pt), ('ja', ja), ('zh', zh)):
    text = json.dumps(p, ensure_ascii=False, separators=(',', ':'))
    (V2 / f'{name}-core-v2.json').write_text(text, encoding='utf-8')
    out[f'{name}-core-v2'] = (hashlib.sha256(text.encode('utf-8')).hexdigest(), len(p['entries']), len(text.encode('utf-8')))

cat_path = V2 / 'catalog.json'
cat = json.loads(cat_path.read_text(encoding='utf-8'))
for c in cat.get('packages', []):
    if c.get('id') in out:
        sha, count, size = out[c['id']]
        c['sha256'], c['entry_count'], c['version'], c['size_bytes'] = sha, count, VERSION, size
        c['has_ui'] = False
cat_path.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(stats), {k: v[1] for k, v in out.items()})
