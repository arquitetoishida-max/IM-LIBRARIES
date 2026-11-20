"""Confere o japonês de cada conceito contra o JMdict (glosses em inglês). Uso: python3 -I novrev/verify_ja.py <jamdict.db>"""
import json,sqlite3,re,sys,csv,collections
db=sqlite3.connect(sys.argv[1])
gl=collections.defaultdict(set)
for sid,t in db.execute("select s.idseq,g.text from SenseGloss g join Sense s on s.ID=g.sid where g.lang='eng'"):
    gl[t.lower().strip()].add(sid)
forms=collections.defaultdict(set)
for i,t in db.execute("select idseq,text from Kanji"): forms[i].add(t)
for i,t in db.execute("select idseq,text from Kana"): forms[i].add(t)
def norm_en(t):
    t=re.sub(r'\(.*?\)','',t).strip().lower()
    return [t, re.sub(r'^to ','',t)]
def norm_ja(t): return re.sub(r'[〜～ ]|する$|な$','',t)
D={e['english_id']:e for e in json.load(open('v2/ja-core-v2.json'))['entries']}
E={e['english_id']:e for e in json.load(open('v2/en-core-v2.json'))['entries']}
out=[];ok=0;nogloss=0
for i,e in D.items():
    if e.get('core_status'): continue
    cands=set()
    for k in norm_en(E[i]['text']):
        for s in gl.get(k,()): cands|=forms[s]
    if not cands: nogloss+=1; out.append((i,E[i]['text'],e['text'],e.get('reading'),'sem_gloss_en_no_JMdict')); continue
    mine={norm_ja(x) for x in [e['text'],e.get('reading') or '',*e.get('alternatives',[])]}
    cn={norm_ja(x) for x in cands}
    if mine&cn: ok+=1
    else: out.append((i,E[i]['text'],e['text'],e.get('reading'),'divergente'))
print('ok',ok,'sem gloss',nogloss,'divergentes',sum(1 for o in out if o[4]=='divergente'))
csv.writer(open('novrev/verify_ja.csv','w',newline='',encoding='utf8')).writerows([('english_id','en','ja','leitura','status'),*out])
