"""python apply.py patch.jsonl a b  -> aplica patch (linhas JSON) e marca posicoes a..b como examinadas."""
import json,sys,hashlib,openpyxl
L=['en','pt-BR','ja','zh']; R='/home/claude/im-libraries/'
pk={l:json.load(open(R+f'v2/{l}-core-v2.json')) for l in L}
ix={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
n0={l:len(pk[l]['entries']) for l in L}
cnt=0
import collections
S=openpyxl.load_workbook(R+'novrev/NOVREV_pendencias.xlsx')
WS=S['Matriz atual']
st={r[0].value:r[14].value for r in WS.iter_rows(min_row=2)}
newrows=[]; delrows=[]
def elig_max():
    return max(e['study_priority'] for e in pk['en']['entries'] if st.get(e['english_id']) not in ('Pendente','Reservar') and e.get('study_priority'))
for line in open(sys.argv[1]):
    if not line.strip(): continue
    r=json.loads(line); cid='en:'+r['i']; cnt+=1
    if r.get('del'):
        for l in L:
            ent=[e for e in pk[l]['entries'] if e['english_id']==cid][0]; p=ent['study_priority']
            pk[l]['entries'].remove(ent); ix[l].pop(cid)
            for e in pk[l]['entries']:
                if e.get('study_priority') and e['study_priority']>p: e['study_priority']-=1
        st.pop(cid,None); delrows.append(cid); n0={l:n0[l]-1 for l in L}
        continue
    if r.get('new'):
        p=elig_max()+1
        for l in L:
            for e in pk[l]['entries']:
                if e.get('study_priority') and e['study_priority']>=p: e['study_priority']+=1
        for l in L:
            q=r[l]; e={'id':(cid if l=='en' else l+':'+cid),'english_id':cid,'english_sense_id':None,'text':q['t'],'kind':'word','description_en':r['de'],'level':r['lv'],'part_of_speech':r['pos'],'source_status':'editorial-reviewed','study_priority':p,'description':q['d'],'novrev_status':'reviewed','user_hint':'','nativeExplain':{l:q['d']},'antonyms':[]}
            if l!='en': e['translation_confidence']='editorial-reviewed'; e['alternatives']=q.get('a',[])
            if l in('ja','zh'): e['reading']=q['r']; e['romanization']=q.get('ro',q['r'])
            pk[l]['entries'].append(e); ix[l][cid]=e
        st[cid]='Examinado nos quatro idiomas'; newrows.append([cid,r['en']['t'],r['pt-BR']['t'],r['ja']['t'],r['zh']['t'],'Após matriz',p,p,p,p,None,None,None,None,'Examinado nos quatro idiomas',None,None,None,r['lv'],None,None])
        continue
    if 'de' in r:
        for l in L: ix[l][cid]['description_en']=r['de']
    for l in L:
        p=r.get(l)
        if not p: continue
        e=ix[l][cid]
        if 'd' in p: e['description']=p['d']; e.setdefault('nativeExplain',{})[ {'en':'en','pt-BR':'pt-BR','ja':'ja','zh':'zh'}[l] ]=p['d']
        if 't' in p: e['text']=p['t']
        if 'a' in p: e['alternatives']=p['a']
        if 'r' in p: e['reading']=p['r']
        if 'ro' in p: e['romanization']=p['ro']
for l in L:
    assert len(pk[l]['entries'])==n0[l]+len(newrows)
    open(R+f'v2/{l}-core-v2.json','w',encoding='utf8').write(json.dumps(pk[l],indent=1,ensure_ascii=False))
c=json.load(open(R+'v2/catalog.json'))
for p in c['packages']:
    if p['id'] in ('en-core-v2','pt-BR-core-v2','ja-core-v2','zh-core-v2'):
        p['entry_count']=len(pk[p['language'] if p['language']!='pt' else 'pt-BR']['entries'])
        b=open(R+f"v2/{p['id']}.json",'rb').read(); p['sha256']=hashlib.sha256(b).hexdigest(); p['size_bytes']=len(b)
open(R+'v2/catalog.json','w',encoding='utf8').write(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
a,b=int(sys.argv[2]),int(sys.argv[3])
m=list(openpyxl.load_workbook(R+'novrev/NOVREV_matriz.xlsx',read_only=True)['NOVREV'].iter_rows(values_only=True))[1:]
ids={r[1] for r in m[a-1:b]}
wb=S; ws=WS; k=0
for row in list(ws.iter_rows(min_row=2)):
    if row[0].value in delrows: ws.delete_rows(row[0].row)
for nr in newrows: ws.append(nr)
for row in ws.iter_rows(min_row=2):
    if row[0].value in ids and row[14].value=='Revisão de sentido em aberto': row[14].value='Examinado nos quatro idiomas'; k+=1
wb.save(R+'novrev/NOVREV_pendencias.xlsx'); print('patched',cnt,'marked',k)
