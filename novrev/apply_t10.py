"""T10: flexões do inglês dentro do card de cada verbo (passado, particípio, 3ª pessoa, -ing) e feminino do pt como variante (masculino padrão)."""
import json,re
L=['en','pt-BR','ja','zh']
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
IRR="""be was/were been; have had had; do did done; go went gone; come came come; see saw seen; take took taken; make made made; say said said; get got gotten;
give gave given; know knew known; think thought thought; tell told told; find found found; leave left left; feel felt felt; keep kept kept; bring brought brought;
buy bought bought; begin began begun; write wrote written; run ran run; hold held held; stand stood stood; hear heard heard; meet met met; pay paid paid; sit sat sat;
speak spoke spoken; lose lost lost; send sent sent; build built built; understand understood understood; become became become; fall fell fallen; grow grew grown;
draw drew drawn; break broke broken; choose chose chosen; eat ate eaten; drive drove driven; win won won; teach taught taught; catch caught caught; fight fought fought;
lead led led; mean meant meant; read read read; spend spent spent; sell sold sold; show showed shown; throw threw thrown; wear wore worn; wake woke woken; forget forgot forgotten;
fly flew flown; sing sang sung; swim swam swum; sleep slept slept; put put put; cut cut cut; let let let; set set set; hit hit hit; hurt hurt hurt; cost cost cost; shut shut shut;
quit quit quit; spread spread spread; bet bet bet; drink drank drunk; ring rang rung; rise rose risen; ride rode ridden; hide hid hidden; bite bit bitten; shake shook shaken;
steal stole stolen; freeze froze frozen; feed fed fed; lay laid laid; lie lay lain; light lit lit; shoot shot shot; slide slid slid; stick stuck stuck; strike struck struck;
swear swore sworn; tear tore torn; bend bent bent; lend lent lent; build built built; deal dealt dealt; dig dug dug; hang hung hung; seek sought sought; sink sank sunk;
blow blew blown; bear bore born; beat beat beaten; forgive forgave forgiven; undergo underwent undergone; withdraw withdrew withdrawn; arise arose arisen; burn burned burned;
learn learned learned; dream dreamed dreamed; smell smelled smelled; spell spelled spelled; can could -; will would -; may might -; shall should -; must - -"""
irr={}
for part in IRR.replace('\n',' ').split(';'):
    p=part.split()
    if len(p)==4 or len(p)==3: 
        v,pa,pp=p[0],p[1],p[2]; irr[v]=(pa,pp)
def past_reg(v):
    if v.endswith('e'): return v+'d'
    if re.search(r'[^aeiou]y$',v): return v[:-1]+'ied'
    if re.search(r'^[^aeiou]*[aeiou][^aeiouwxy]$',v): return v+v[-1]+'ed'
    return v+'ed'
def s3(v):
    if v in ('be',): return 'is'
    if v=='have': return 'has'
    if v in ('do','go'): return v+'es'
    if re.search(r'(s|sh|ch|x|z|o)$',v): return v+'es'
    if re.search(r'[^aeiou]y$',v): return v[:-1]+'ies'
    return v+'s'
def ing(v):
    if v in ('be','see','agree','free','flee'): return v+'ing'
    if v.endswith('ie'): return v[:-2]+'ying'
    if v.endswith('e') and not v.endswith('ee'): return v[:-1]+'ing'
    if re.search(r'^[^aeiou]*[aeiou][^aeiouwxy]$',v): return v+v[-1]+'ing'
    return v+'ing'
n=0
for e in pk['en']['entries']:
    if e.get('core_status') is not None or e.get('part_of_speech')!='v': continue
    t=e['text'].strip()
    if not re.fullmatch(r'[a-z]+( [a-z]+)?',t): continue
    head,_,rest=t.partition(' '); rest=(' '+rest) if rest else ''
    if head in ('can','will','may','shall','must','could','would','should','might'): continue
    pa,pp=irr.get(head,(past_reg(head),past_reg(head)))
    want=[('PRES.3SG',s3(head)+rest),('PAST',pa.split('/')[0]+rest),('PTCP_PAST',pp+rest),('ING',ing(head)+rest)]
    if head=='be': want=[('PRES.1SG','am'),('PRES.3SG','is'),('PRES.NON3SG','are'),('PAST','was / were'),('PTCP_PAST','been'),('ING','being')]
    fs=[f for f in (e.get('forms') or []) if f.get('grammatical_key')]
    keys={f['grammatical_key'] for f in fs}
    for k,x in want:
        if k in keys: continue
        fs.append({'form_id':f"{e['english_id']}:f:{k}",'lemma_id':e['english_id'],'grammatical_key':k,'text':x,'study_tier':'standard'}); n+=1
    order={'PRES.1SG':0,'PRES.3SG':1,'PRES.NON3SG':2,'PAST':3,'PTCP_PAST':4,'ING':5}
    e['forms']=sorted(fs,key=lambda f:order.get(f['grammatical_key'],9))
print('formas en',n)
# pt: feminino é variante (forms FEM), nunca sinônimo
def fem(t):
    for a,b in (('ão','ã'),('ão','ona'),('or','ora'),('ês','esa'),('o','a'),('eu','eia')):
        if t.endswith(a): yield t[:-len(a)]+b
    yield t+'a'
m=0
for e in pk['pt-BR']['entries']:
    t=e['text']; alts=e.get('alternatives') or []
    fs=set(fem(t)); hit=[a for a in alts if a in fs]
    if not hit: continue
    e['alternatives']=[a for a in alts if a not in hit]
    forms=e.get('forms') or []
    for h in hit:
        if not any(f.get('text')==h for f in forms):
            forms.append({'form_id':f"{e['english_id']}:f:FEM",'lemma_id':e['english_id'],'grammatical_key':'FEM','text':h,'study_tier':'standard'})
    e['forms']=forms; m+=1
print('pt feminino → variante',m)
for l in L: json.dump(pk[l],open(f'v2/{l}-core-v2.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
