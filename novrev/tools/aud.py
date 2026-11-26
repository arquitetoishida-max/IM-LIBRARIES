import json,sys,collections
a,b=int(sys.argv[1]),int(sys.argv[2])
d={l:json.load(open(f'v2/{l}-core-v2.json'))['entries'] for l in('en','pt-BR','ja','zh')}
ix={l:{e['english_id']:e for e in d[l]} for l in d}
by=collections.defaultdict(list)
for e in d['en']: by[e['text'].lower()].append(e['english_id'])
es=sorted(d['en'],key=lambda e:e['study_priority'])
seen=set();out=[]
for e in es:
    t=e['text'].lower()
    if t in seen: continue
    seen.add(t);out.append(t)
for t in out[a:b]:
    print('##',t)
    for i in by[t]:
        print('  ',i[3:],ix['en'][i]['part_of_speech'] if 'part_of_speech' in ix['en'][i] else '', '|',ix['en'][i]['description'][:55],'| pt:',ix['pt-BR'][i]['text'],'| ja:',ix['ja'][i]['text'],'| zh:',ix['zh'][i]['text'])
