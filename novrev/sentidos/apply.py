"""Aplica edições de sentidos (JSON lines) nos 4 núcleos. Uso: python novrev/sentidos/apply.py ARQ.jsonl [...]
vcu14: lista de ambientes (ex.: ["home"]) põe o ID novo no VCU14 com o próximo rank.
ops: alt+ / alt- (v: lista), text, desc (v: str), drop (tira o ID só desse idioma),
new: {"op":"new","pos":"n","level":"A2","en":{"text","desc"},"pt-BR":{...},"ja":{"text","reading","desc"},"zh":{"text","reading","desc"}} (alt opcional)
Idempotente: alt+ não duplica; new com o mesmo en.text+desc não recria."""
import json,sys,glob
sys.path.insert(0,'scripts')
from kana_romaji import romaji as k2r
L=['en','pt-BR','ja','zh']
P={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
E={l:{e['english_id']:e for e in P[l]['entries']} for l in L}
def nid():
    m=0
    for f in glob.glob('v2/*-core-v2.json'):
        for e in json.load(open(f))['entries']: m=max(m,int(e['english_id'][3:]))
    return m+1
NEXT=[None]; NR=[None]
for f in sys.argv[1:]:
    for ln in open(f,encoding='utf-8'):
        ln=ln.strip()
        if not ln or ln.startswith('#'): continue
        o=json.loads(ln); op=o['op']
        if op=='new':
            if any(e['text']==o['en']['text'] and e['description']==o['en']['desc'] for e in E['en'].values()): continue
            if NEXT[0] is None: NEXT[0]=nid()
            i=f'en:{NEXT[0]:09d}'; NEXT[0]+=1
            for l in L:
                if l not in o: continue
                x=o[l]; e={'id':i if l=='en' else f'{l}:{i}','english_id':i,'kind':'word','description_en':o['en']['desc'],
                   'level':o.get('level','A2'),'part_of_speech':o['pos'],'source_status':'editorial-reviewed','text':x['text'],
                   'alternatives':x.get('alt',[]),'study_tier':'cedo','study_priority':max(x.get('study_priority') or 0 for x in P[l]['entries'])+1,'user_hint':'','description':x['desc'],
                   'novrev_status':'reviewed','antonyms':[]}
                if l=='en': e.pop('alternatives') if not x.get('alt') else None
                else: e['english_sense_id']=None; e['translation_confidence']='editorial-reviewed'
                if l=='ja': e['reading']=x['reading']; e['romanization']=k2r(x['reading'])
                if l=='zh': e['reading']=e['romanization']=x['reading']
                if o.get('vcu14'):
                    if NR[0] is None: NR[0]=max(x.get('vcu14_rank') or 0 for x in P['en']['entries'])+1
                    e.update(vcu14_rank=NR[0],vcu14_status='provisional-editorial',environments=o['vcu14'],study_tier='fala cotidiana inicial')
                P[l]['entries'].append(e); E[l][i]=e
            if o.get('vcu14'): NR[0]+=1
            continue
        l=o['l']; i=f"en:{int(o['id']):09d}"; e=E[l].get(i)
        if e is None: print('sem id',l,i); continue
        if op=='alt+': e['alternatives']=list(dict.fromkeys((e.get('alternatives') or [])+[v for v in o['v'] if v!=e['text']]))
        elif op=='alt-': e['alternatives']=[a for a in e.get('alternatives') or [] if a not in o['v']]
        elif op=='text': e['text']=o['v']
        elif op=='desc': e['description']=o['v']
        elif op=='drop': P[l]['entries']=[x for x in P[l]['entries'] if x['english_id']!=i]; E[l].pop(i)
for l in L: json.dump(P[l],open(f'v2/{l}-core-v2.json','w'),ensure_ascii=False,indent=1)
print('ok')
