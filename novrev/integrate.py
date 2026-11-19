"""Integra novrev/build/* em v2/ (backup em v2/previous/), sobe versão e atualiza catálogo."""
import json,hashlib,shutil,os
V='2.3.0'; L=['en','pt-BR','ja','zh']
cat=json.load(open('v2/catalog.json'))
for l in L:
    src=f'novrev/build/{l}-core-novrev.json'; dst=f'v2/{l}-core-v2.json'
    old=json.load(open(dst)); new=json.load(open(src))
    assert [e['id'] for e in old['entries']]==[e['id'] for e in new['entries']]
    assert [e['english_id'] for e in old['entries']]==[e['english_id'] for e in new['entries']]
    assert len({e['id'] for e in new['entries']})==len(new['entries'])
    bk=f"v2/previous/{l}-core-v2-{old['version']}.json"
    if not os.path.exists(bk): shutil.copy(dst,bk)
    new['version']=V
    new['notes'].append("2.3.0: NOVREV — 1.060 conceitos VCU14 reconstruídos (texto limpo, descrição nativa, antônimos por ID), campos novrev_status, user_hint (reservado, vazio) e novrev_flag.")
    raw=json.dumps(new,ensure_ascii=False,indent=1).encode()
    open(dst,'wb').write(raw)
    for p in cat['packages']:
        if p['id']==f'{l}-core-v2':
            p['version']=V; p['sha256']=hashlib.sha256(raw).hexdigest(); p['size_bytes']=len(raw); p['entry_count']=len(new['entries'])
cat['version']='1.3.1'
cat['notes'].append('1.3.1: core 2.3.0 — NOVREV VCU14 (1.060 conceitos) integrado em en/pt-BR/ja/zh; anteriores 2.2.1 em v2/previous/.')
open('v2/catalog.json','w').write(json.dumps(cat,ensure_ascii=False,indent=2))
print('ok')
