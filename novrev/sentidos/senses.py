"""Confere a lista de sentidos de cada palavra (senses_LANG.txt: `palavra: glosa1, glosa2, 123`, glosa = texto em inglês
de um ID, ou o número do ID). Para cada sentido: se o ID existe e a palavra não está nele (texto/variante) → alt+ gravado
em edits_auto_LANG.jsonl; se não existe ID → lista FALTA. Uso: senses.py LANG"""
import json,sys
l=sys.argv[1]; L=['en','pt-BR','ja','zh']
D={x:{e['english_id']:e for e in json.load(open(f'v2/{x}-core-v2.json'))['entries']} for x in L}
def ids(g):
    g=g.strip()
    if g.isdigit(): i=f'en:{int(g):09d}'; return [i] if i in D['en'] else []
    return [i for i,e in D['en'].items() if e['text']==g] or [i for i,e in D['en'].items() if g in (e.get('alternatives') or [])]
out=[];falta=[];amb=[]
for ln in open(f'novrev/sentidos/senses_{l}.txt',encoding='utf-8'):
    if ':' not in ln or ln.startswith('#'): continue
    w,gs=ln.split(':',1); w=w.strip()
    for g in gs.split(','):
        if not g.strip(): continue
        h=[i for i in ids(g) if i in D[l]]
        if not h: falta.append(f'{w}: {g.strip()}'); continue
        if len(h)>1:
            hit=[i for i in h if D[l][i]['text']==w or w in (D[l][i].get('alternatives') or [])]
            if hit: continue
            amb.append(f'{w}: {g.strip()} -> '+' ; '.join(f"{int(i[3:])} {D[l][i]['text']}" for i in h)); continue
        e=D[l][h[0]]
        if e['text']!=w and w not in (e.get('alternatives') or []):
            out.append(json.dumps({'op':'alt+','l':l,'id':int(h[0][3:]),'v':[w]},ensure_ascii=False)+f"  # {e['text']}")
open(f'novrev/sentidos/edits_auto_{l}.jsonl','w').write('\n'.join(x.split('  #')[0] for x in out)+'\n')
print('LIGAR',len(out)); [print(' ',x) for x in out]
print('AMBIGUO',len(amb)); [print(' ',x) for x in amb]
print('FALTA',len(falta)); [print(' ',x) for x in falta]
