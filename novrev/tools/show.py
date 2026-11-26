import json,sys,openpyxl
L=['en','pt-BR','ja','zh']
import collections
R='/home/claude/im-libraries/'
D={l:{e['english_id']:e for e in json.load(open(R+f'v2/{l}-core-v2.json'))['entries']} for l in L}
m=list(openpyxl.load_workbook(R+'novrev/NOVREV_matriz.xlsx',read_only=True)['NOVREV'].iter_rows(values_only=True))[1:]
pend=list(openpyxl.load_workbook(R+'novrev/NOVREV_pendencias.xlsx',read_only=True)['Matriz atual'].iter_rows(values_only=True))[1:]
st={r[0]:r[14] for r in pend}
H=collections.defaultdict(list)
for k,v in D['en'].items(): H[v['text'].lower()].append(k)
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in m[a-1:b]:
    i=r[1]
    if st.get(i)!='Revisão de sentido em aberto': print(r[0],i,'SKIP',st.get(i)); continue
    e=D['en'][i]
    print(f"## {r[0]} {i} [{e.get('part_of_speech')} {e.get('level')} {e.get('region_tags') or ''}] {e['text']} — {e['description_en']}")
    for l in L[1:]:
        x=D[l][i]; print(f"  {l}: {x['text']} {x.get('alternatives') or ''} {x.get('reading','') if l!='pt-BR' else ''} | {x.get('description')}")
    o=[k[3:]+':'+D['en'][k]['description_en'][:40] for k in H[e['text'].lower()] if k!=i]
    if o: print('  homonyms:',o)
    if e.get('description')!=e['description_en']: print('  en.desc:',e.get('description'))
