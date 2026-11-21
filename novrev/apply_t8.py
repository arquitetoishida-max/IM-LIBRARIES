"""T8: flexões e plurais não têm id próprio (regra do dono). A entrada flexionada sai do núcleo e a forma entra no card do lema (en forms).
Comparativos/superlativos e palavras que viraram outro sentido (building, broken, news, parents, people, cards...) ficam."""
import json,re
L=['en','pt-BR','ja','zh']
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
idx={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
EN=idx['en']; act={i:e for i,e in EN.items() if e.get('core_status') is None}
byt={}
for i,e in act.items(): byt.setdefault(e['text'].lower(),[]).append(i)
IRR={'was':'be','were':'be','been':'be','is':'be','are':'be','am':'be','has':'have','had':'have','does':'do','did':'do','said':'say','made':'make','got':'get','found':'find','told':'tell','seen':'see','took':'take','came':'come','went':'go','saw':'see','taken':'take','heard':'hear','gave':'give','held':'hold','knew':'know','brought':'bring','sent':'send','became':'become','felt':'feel','paid':'pay','led':'lead','met':'meet','written':'write','began':'begin','built':'build','wrote':'write','spent':'spend','kept':'keep','sold':'sell','meant':'mean','bought':'buy','caught':'catch','shown':'show','ran':'run','showed':'show','fell':'fall','grew':'grow','taught':'teach','sat':'sit','forgot':'forget','chosen':'choose','spoke':'speak','understood':'understand','stood':'stand','chose':'choose','driven':'drive','drawn':'draw','won':'win','given':'give','women':'woman','men':'man','children':'child','feet':'foot','teeth':'tooth','broke':'break'}
KEEP_PL={'people','parents','news','goods','times','cards','heads','groceries','authorities','values','arts','thanks','others','besides','lots'}
ret=[]; forms={}
for i,e in act.items():
    t=e['text']; tl=t.lower(); pos=e.get('part_of_speech'); d=(e.get('description') or e.get('description_en') or '')
    if ' ' in t or tl in KEEP_PL: continue
    base=None; key=None
    if pos=='v' and re.match(r"(Past|Simple past|Past participle|Third-person|A form of|The present form|Past and past-participle|Past form|Past of)",d):
        if tl in IRR: base=IRR[tl]
        else:
            for c in ([tl[:-3]+'y'] if tl.endswith('ied') else [])+[tl[:-2],tl[:-1],tl[:-3] if len(tl)>4 and tl[-3]==tl[-4] else '']+([tl[:-1]] if tl.endswith('s') else [])+([tl[:-2]] if tl.endswith('es') else []):
                if c and c in byt: base=c; break
        key='PTCP_PAST' if re.match(r'Past participle',d) else ('PRES.3SG' if re.match(r'(Third-person|A form of|The present form)',d) else 'PAST')
        if re.match(r'Past and past-participle',d): key='PAST'
    elif pos=='n' and re.search(r'(plural|Plural)',d):
        if tl in IRR: base=IRR[tl]
        else:
            for c in ([tl[:-3]+'y'] if tl.endswith('ies') else [])+([tl[:-3]+'f'] if tl.endswith('ves') else [])+[tl[:-1],tl[:-2]]:
                if c in byt: base=c; break
        key='PL'
    if not base: continue
    if base not in byt: continue
    bid=[b for b in byt[base] if (EN[b].get('part_of_speech')==('n' if key=='PL' else 'v'))] or byt[base]
    ret.append((i,t,bid[0],key))
    forms.setdefault(bid[0],[]).append((key,t,d))
print(len(ret))
for r in sorted(ret,key=lambda r:r[0]): print(r[0][3:],r[1],'->',EN[r[2]]['text'],r[3])
for i,t,b,k in ret:
    for l in L: idx[l][i]['core_status']='search_only'; idx[l][i]['inflection_of']=b; idx[l][i]['inflection_key']=k
    for l in L:
        for e in pk[l]['entries']:
            if i in (e.get('antonyms') or []): e['antonyms']=[x for x in e['antonyms'] if x!=i]
for b,fl in forms.items():
    e=EN[b]; fs=e.get('forms') or []
    for k,t,d in fl:
        if any(f.get('text')==t for f in fs): continue
        fs.append({'form_id':f'{b}:f:{k}:{t}','lemma_id':b,'grammatical_key':k,'text':t,'study_tier':'standard','description_en':d})
    e['forms']=[f for f in fs if f.get('grammatical_key')]
json.dump(forms and None,open('/dev/null','w'))
for l in L: json.dump(pk[l],open(f'v2/{l}-core-v2.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
