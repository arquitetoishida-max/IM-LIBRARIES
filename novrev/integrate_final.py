"""Integração final NOVREV: 4 idiomas com o mesmo conjunto de conceitos (3609), 6 conceitos incompletos suspensos nos 4."""
import json,hashlib,shutil,os
V='2.4.0'; L=['en','pt-BR','ja','zh']
SUSP={'en:000000001','en:000000028','en:000003192','en:000003198','en:000003199','en:000003926'}
cat=json.load(open('v2/catalog.json'))
new={}
for l in L:
    d=json.load(open(f'novrev/build/{l}-core-novrev.json'))
    d['entries']=[e for e in d['entries'] if e['english_id'] not in SUSP]
    new[l]=d
ids=[[e['english_id'] for e in new[l]['entries']] for l in L]
assert all(sorted(x)==sorted(ids[0]) for x in ids), 'conjuntos diferentes'
for l in L:
    assert len({e['id'] for e in new[l]['entries']})==len(new[l]['entries'])
    dst=f'v2/{l}-core-v2.json'; old=json.load(open(dst))
    bk=f"v2/previous/{l}-core-v2-{old['version']}.json"
    if not os.path.exists(bk): shutil.copy(dst,bk)
    d=new[l]; d['version']=V
    d['notes'].append("2.4.0: NOVREV completo — 3.609 conceitos iguais nos 4 idiomas (mesmo ID), descrição nativa, antônimos por ID, user_hint reservado vazio, novrev_status; 6 conceitos incompletos suspensos nos 4 idiomas.")
    raw=json.dumps(d,ensure_ascii=False,indent=1).encode()
    open(dst,'wb').write(raw)
    for p in cat['packages']:
        if p['id']==f'{l}-core-v2':
            p['version']=V; p['sha256']=hashlib.sha256(raw).hexdigest(); p['size_bytes']=len(raw); p['entry_count']=len(d['entries'])
    print(l,len(d['entries']))
cat['version']='1.4.0'
cat['notes'].append('1.4.0: core 2.4.0 — NOVREV completo, 4 idiomas iguais (3.609 conceitos); anterior 2.3.0 em v2/previous/.')
open('v2/catalog.json','w').write(json.dumps(cat,ensure_ascii=False,indent=2))
