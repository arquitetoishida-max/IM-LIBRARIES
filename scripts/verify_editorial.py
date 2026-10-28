"""Independent check of the editorial ja readings with pykakasi; writes docs/EDITORIAL_QA.json."""
import json, re, sys, pathlib
import pykakasi
R = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
from kana_romaji import to_hira
kk = pykakasi.kakasi()
norm = lambda s: re.sub(r'[〜～・、。！？\s（）()]', '', to_hira(s))
ja = json.loads((R / 'v2/ja-core-v2.json').read_text(encoding='utf-8'))['entries']
en = {e['id']: e for e in json.loads((R / 'v2/en-core-v2.json').read_text(encoding='utf-8'))['entries']}
mism = []
for e in ja:
    auto = ''.join(x['hira'] for x in kk.convert(e['text']))
    if norm(auto) != norm(e['reading']):
        mism.append({'id': e['english_id'], 'en': en[e['english_id']]['text'], 'ja': e['text'], 'reading': e['reading'], 'pykakasi': auto})
rep = {'checked': len(ja), 'reading_mismatches': len(mism), 'items': mism}
(R / 'docs/EDITORIAL_QA.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(ja), 'checked;', len(mism), 'mismatches')
