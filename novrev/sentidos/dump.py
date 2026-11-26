import json,sys
# uso: dump.py LANG START N  -> palavras do idioma por prioridade VCU14, com todos os IDs que as usam
l,s,n=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
POS=set(sys.argv[4].split(',')) if len(sys.argv)>4 else None
L=['en','pt-BR','ja','zh']
D={x:{e['english_id']:e for e in json.load(open(f'v2/{x}-core-v2.json'))['entries']} for x in L}
words={}
for i,e in D[l].items():
    if POS and e.get('part_of_speech') not in POS: continue
    r=e.get('vcu14_rank') or e.get('study_priority') or 99999
    for w in [e['text']]+(e.get('alternatives') or []):
        w=w.strip()
        if w: words.setdefault(w,[99999,set()]); words[w][0]=min(words[w][0],r); words[w][1].add(i)
order=sorted(words,key=lambda w:(words[w][0],w))
for w in order[s:s+n]:
    print(f'# {w}')
    for i in sorted(words[w][1]):
        e=D[l][i]; en=D['en'].get(i,{}).get('text','-')
        print(f"  {int(i[3:])} {e.get('part_of_speech')} [{en}] {e['text']} {'/'.join(e.get('alternatives') or [])} :: {e.get('description','')[:70]}")
