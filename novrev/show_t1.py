import json,sys
L=['en','pt-BR','ja','zh']
D={l:{e['english_id']:e for e in json.load(open(f'v2/{l}-core-v2.json'))['entries']} for l in L}
ids=[i for i in sorted(D['en']) if all(not D[l][i].get('core_status') for l in L)]
a,b=int(sys.argv[1]),int(sys.argv[2])
print('total',len(ids))
for n,i in enumerate(ids[a:b],a):
    en,pt,ja,zh=(D[l][i] for l in L)
    print(n,i[-6:],'|',en['text'],'|',pt['text'],'|',ja['text']+('('+ja['reading']+')' if ja.get('reading') and ja['reading']!=ja['text'] else ''),'|',zh['text'],'|',(en.get('part_of_speech') or '')[:4],'|',(en.get('description') or '')[:34])
