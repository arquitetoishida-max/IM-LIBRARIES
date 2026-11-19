"""NOVREV: aplica novrev/patches/*.jsonl sobre os 4 núcleos e grava em novrev/build/.
Nunca altera v2/. IDs, ordem e quantidades são preservados; falha se algo divergir."""
import json,glob,sys,re
sys.path.insert(0,'scripts')
import kana_romaji as kr
L={'en':'en','pt-BR':'pt','ja':'ja','zh':'zh'}
KANA=re.compile(r'^[ぁ-ゖァ-ヺーー〜~・ ]+$')
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
idx={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
n=0
for f in sorted(glob.glob('novrev/patches/*.jsonl')):
    for line in open(f):
        if not line.strip(): continue
        r=json.loads(line); cid='en:'+r['i']
        for l,k in L.items():
            e=idx[l][cid]
            if r.get('d'): e['description']=r['d'][k]
            w=(r.get('w') or {}).get(l) or (r.get('w') or {}).get(k) or {}
            if 't' in w: e['text']=w['t']
            if 'a' in w: e['alternatives']=w['a']
            if 'r' in w: e['reading']=w['r']
            if 'ro' in w: e['romanization']=w['ro']
            if l=='ja' and not e.get('reading') and KANA.match(e['text']):
                e['reading']=e['text']; e['romanization']=kr.romaji(kr.to_hira(e['text'].replace('〜','')))
            if r.get('ant'): e['antonyms']=r['ant']
            e['novrev_status']='reviewed'
            if r.get('flag'): e['novrev_flag']=r['flag']
        n+=1
for l in L:
    pk[l]['entries']=[idx[l][e['english_id']] for e in pk[l]['entries']]
    json.dump(pk[l],open(f'novrev/build/{l}-core-novrev.json','w'),ensure_ascii=False,indent=1)
tot={l:len(pk[l]['entries']) for l in L}
done={l:sum(1 for e in pk[l]['entries'] if e.get('novrev_status')=='reviewed') for l in L}
print('conceitos revisados',n,tot,done)
