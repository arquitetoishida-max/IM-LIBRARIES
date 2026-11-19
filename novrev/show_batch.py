import json,sys
L=['en','pt-BR','ja','zh']
D={l:{e['english_id']:e for e in json.load(open(f'v2/{l}-core-v2.json'))['entries']} for l in L}
ids=[i for i in D['en'] if all(i in D[l] and D[l][i].get('vcu14_rank') for l in L)]
ids.sort(key=lambda i:D['en'][i]['vcu14_rank'])
a,b=int(sys.argv[1]),int(sys.argv[2])
def w(e):
    s=e['text']
    if e.get('alternatives'): s+=' ['+','.join(e['alternatives'])+']'
    if e.get('reading') and e.get('reading')!=e['text']: s+=' ('+e['reading']+')'
    return s
for n,i in enumerate(ids[a:b],a+1):
    print(n,i[3:],'|',D['en'][i]['text'],'—',D['en'][i]['description_en'],'|',w(D['pt-BR'][i]),'|',w(D['ja'][i]),'|',w(D['zh'][i]),'|',D['en'][i].get('part_of_speech'))
