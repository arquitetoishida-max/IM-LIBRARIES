"""Aplica novrev/t6/fix*.jsonl nos núcleos v2/ (revisão 100%). Idempotente."""
import json,glob
L=['en','pt-BR','ja','zh']; K={'en':'en','pt-BR':'pt','ja':'ja','zh':'zh'}
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
idx={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
n=bad=0
for f in sorted(glob.glob('novrev/t6/fix*.jsonl')):
    for ln,line in enumerate(open(f,encoding='utf8'),1):
        if not line.strip(): continue
        try: r=json.loads(line)
        except Exception as ex: print('JSON inválido',f,ln,ex); bad+=1; continue
        cid='en:'+str(r['i']).replace('en:','').zfill(9)
        if cid not in idx['en']: print('id inexistente',f,ln,cid); bad+=1; continue
        for l in L:
            e=idx[l][cid]
            if r.get('retire'): e['core_status']='search_only'; continue
            if r.get('pending'): e['core_status']='pending'; continue
            if r.get('pos'): e['part_of_speech']=r['pos']
            fx=(r.get('forms') or {}).get(K[l]) or (r.get('forms') or {}).get(l) or {}
            for f in e.get('forms') or []:
                key=f.get('grammatical_key') or f.get('form_id','').split(':')[-1]
                if key in fx:
                    v=fx[key]
                    if v.get('t'): f['text']=v['t']
                    if 'r' in v: f['reading']=v['r']
                    if 'ro' in v: f['romanization']=v['ro']
            w=(r.get('w') or {}).get(K[l]) or (r.get('w') or {}).get(l) or {}
            if w.get('t'): e['text']=w['t']
            if 'a' in w: e['alternatives']=[a for a in w['a'] if a and a!=e['text']]
            if 'r' in w: e['reading']=w['r']
            if 'ro' in w: e['romanization']=w['ro']
            d=(r.get('d') or {}).get(K[l]) or (r.get('d') or {}).get(l)
            if d:
                e['description']=d; ne=e.get('nativeExplain') if isinstance(e.get('nativeExplain'),dict) else {}
                ne[l]=d; e['nativeExplain']=ne
                if l=='en': e['description_en']=d
        n+=1
for l in L:
    open(f'v2/{l}-core-v2.json','w',encoding='utf8').write(json.dumps(pk[l],ensure_ascii=False,indent=1))
print('correções aplicadas',n,'inválidas',bad)
