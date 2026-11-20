"""Aplica novrev/t1/*.jsonl direto nos núcleos v2/ (correções T1: mesma palavra/significado nos 4 idiomas). Idempotente."""
import json,glob,sys,hashlib
sys.path.insert(0,'scripts')
L=['en','pt-BR','ja','zh']; K={'en':'en','pt-BR':'pt','ja':'ja','zh':'zh'}
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
idx={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
n=0
for f in sorted(glob.glob('novrev/t1/*.jsonl')):
    for line in open(f,encoding='utf8'):
        if not line.strip(): continue
        r=json.loads(line); cid='en:'+r['i']
        for l in L:
            e=idx[l][cid]; w=(r.get('w') or {}).get(l) or (r.get('w') or {}).get(K[l]) or {}
            if 't' in w: e['text']=w['t']
            if 'a' in w: e['alternatives']=w['a']
            if 'r' in w: e['reading']=w['r']
            if 'ro' in w: e['romanization']=w['ro']
            d=(r.get('d') or {}).get(K[l])
            if d:
                e['description']=d; ne=e.get('nativeExplain') if isinstance(e.get('nativeExplain'),dict) else {}
                ne[l]=d; e['nativeExplain']=ne
                if l=='en': e['description_en']=d
        n+=1
for l in L:
    open(f'v2/{l}-core-v2.json','w',encoding='utf8').write(json.dumps(pk[l],ensure_ascii=False,indent=1))
print('fixes aplicados',n)
