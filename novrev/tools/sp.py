import json,sys
L=('en','pt-BR','ja','zh')
col=sys.argv[1]; a=int(sys.argv[2]); b=int(sys.argv[3]); thr=int(sys.argv[4])
R='/home/claude/im-libraries/'
d={l:{e['english_id']:e for e in json.load(open(R+f'v2/{l}-core-v2.json'))['entries']} for l in L}
en=sorted(d['en'].values(),key=lambda e:e.get('study_priority',9e9))
c=[e for e in en[:700] if len(d[col][e['english_id']]['description'])<thr]
print(len(c),'candidatos')
for e in c[a:b]:
    i=e['english_id']
    x=d[col][i]
    print(i[-5:],e['text'],e.get('part_of_speech'),'|',x['text'],'|',x['description'],'|',x.get('alternatives',''),'| en:',e['description_en'][:70] if col!='en' else '', '| pt:',d['pt-BR'][i]['text'] if col!='pt-BR' else '')
