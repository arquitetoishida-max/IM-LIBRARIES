import json,sys
# uso: find.py en:turn on,quarter ...  ou pt-BR:sala  -> ids cujo texto/alternativa bate, com os 4 idiomas
L=['en','pt-BR','ja','zh']
D={x:{e['english_id']:e for e in json.load(open(f'v2/{x}-core-v2.json'))['entries']} for x in L}
for q in ' '.join(sys.argv[1:]).split('|'):
    l,ws=q.strip().split(':',1)
    for w in ws.split(','):
        w=w.strip()
        hit=[i for i,e in D[l].items() if e['text']==w or w in (e.get('alternatives') or [])]
        print(f'{l}:{w} ->',' ; '.join(f"{int(i[3:])} "+' / '.join(D[x][i]['text'] if i in D[x] else '-' for x in L) for i in hit) or 'NADA')
