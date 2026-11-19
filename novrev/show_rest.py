"""Lista os conceitos ainda não revisados (presentes nos 4 idiomas), por ordem de english_id."""
import json,sys,re
L=['en','pt-BR','ja','zh']
D={l:{e['english_id']:e for e in json.load(open(f'v2/{l}-core-v2.json'))['entries']} for l in L}
import glob
done=set()
for f in glob.glob('novrev/patches/*.jsonl'):
    for l in open(f):
        if l.strip(): done.add('en:'+json.loads(l)['i'])
ids=sorted(i for i in D['en'] if all(i in D[l] for l in L) and i not in done and D['en'][i].get('novrev_status')!='reviewed' and not D['en'][i].get('core_status'))
a,b=int(sys.argv[1]),int(sys.argv[2])
print('restantes',len(ids)); 
def w(e):
    s=e['text']
    if e.get('alternatives'): s+=' ['+','.join(e['alternatives'])+']'
    r=e.get('reading')
    if r and r!=e['text']: s+=' ('+r+')'
    return s
for n,i in enumerate(ids[a:b],a+1):
    e=D['en'][i]
    print(n,i[3:],'|',e['text'],'—',(e.get('description_en') or '')[:70],'|',w(D['pt-BR'][i]),'|',w(D['ja'][i]),'|',w(D['zh'][i]),'|',e.get('part_of_speech'),e.get('core_status') or '')
