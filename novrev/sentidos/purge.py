import json,sys
L=['en','pt-BR','ja','zh']
R={f'en:{int(x):09d}' for x in sys.argv[1].split(',')}
for l in L:
    p=f'v2/{l}-core-v2.json'; d=json.load(open(p))
    n=len(d['entries']); d['entries']=[e for e in d['entries'] if e['english_id'] not in R]
    refs=0
    for e in d['entries']:
        a=e.get('antonyms')
        if isinstance(a,list):
            b=[x for x in a if not (isinstance(x,str) and any(x.endswith(r) for r in R)) and not (isinstance(x,dict) and any(str(v).endswith(r) for v in x.values() for r in R))]
            if len(b)!=len(a): refs+=1; e['antonyms']=b
    for k in ('constructions',):
        if isinstance(d.get(k),list): d[k]=[c for c in d[k] if not any(c.get('lemma_id','').endswith(r) for r in R)]
    json.dump(d,open(p,'w'),ensure_ascii=False,indent=1)
    print(l,n,'->',len(d['entries']),'antonym refs cleaned',refs)
