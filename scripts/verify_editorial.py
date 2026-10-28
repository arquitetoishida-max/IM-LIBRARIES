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
# Mandarin pinyin (tone marks) against pypinyin; neutral tones and erhua are expected differences.
import unicodedata
from pypinyin import pinyin, Style
def pnorm(x):
    x = unicodedata.normalize('NFC', x.lower())
    return re.sub(r"[\s…·'’\-（）()]", '', x)
zh = json.loads((R / 'v2/zh-core-v2.json').read_text(encoding='utf-8'))['entries']
zm = []
for e in zh:
    text = re.sub(r'（.*?）|…', '', e['text'])
    auto = ''.join(s[0] for s in pinyin(text, style=Style.TONE, heteronym=False, errors='ignore'))
    if pnorm(auto) != pnorm(e['reading']):
        zm.append({'id': e['english_id'], 'en': en[e['english_id']]['text'], 'zh': e['text'], 'pinyin': e['reading'], 'pypinyin': auto})
rep = {'checked': len(ja), 'reading_mismatches': len(mism), 'items': mism, 'zh_checked': len(zh), 'zh_mismatches': len(zm), 'zh_items': zm}
(R / 'docs/EDITORIAL_QA.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(ja), 'ja checked;', len(mism), 'mismatches;', len(zh), 'zh checked;', len(zm), 'zh mismatches')
