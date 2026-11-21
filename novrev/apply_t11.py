"""T11: respostas do dono (exceções 20/11)."""
import json,copy
L=['en','pt-BR','ja','zh']
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
idx={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
EN=idx['en']
def E(i,l): return idx[l]['en:'+i]
def setd(i,l,d):
    e=E(i,l); e['description']=d; e['nativeExplain']={l:d}
    if l=='en': e['description_en']=d
def W(i,l,t,r=None,ro=None,a=()):
    e=E(i,l); e['text']=t; e['alternatives']=list(a)
    if r is not None: e['reading']=r
    if ro is not None: e['romanization']=ro
def st(i,s,langs=L):
    for l in langs: E(i,l)['core_status']=s
TPL={l:E('000000184',l) for l in L}
KEEP=['kind','source_status','translation_confidence','study_tier','user_hint','part_of_speech','level']
nxt=[max(int(i[3:]) for i in EN)+1]
def new(key,en,pt,ja,zh,d):
    for e in pk['en']['entries']:
        if e.get('t7_key')==key: return e['english_id'][3:]
    eid=f'en:{nxt[0]:09d}'; nxt[0]+=1
    for l in L:
        e={k:copy.deepcopy(TPL[l][k]) for k in KEEP if k in TPL[l]}
        e.update(id=f'{l}:{eid}',english_id=eid,english_sense_id=None,antonyms=[],novrev_status='reviewed',t7_key=key,description_en=d['en'])
        if l=='en': e.update(text=en[0],alternatives=list(en[1:]))
        if l=='pt-BR': e.update(text=pt[0],alternatives=list(pt[1:]))
        if l=='ja': e.update(text=ja[0],reading=ja[1],romanization=ja[2],alternatives=list(ja[3:]))
        if l=='zh': e.update(text=zh[0],reading=zh[1],romanization=zh[1],alternatives=list(zh[2:]))
        e['description']=d[{'pt-BR':'pt'}.get(l,l)]; e['nativeExplain']={l:e['description']}
        pk[l]['entries'].append(e); idx[l][eid]=e
    return eid[3:]
# títulos: desambiguados em inglês; ja espelha (〜さん) em ids próprios
st('000001337',None)
W('000000184','pt-BR','Sr.',a=['senhor']); W('000002129','pt-BR','Sra.',a=['senhora']); W('000001337','pt-BR','Sra.',a=['senhora'])
for i,d in (('000000184',('Title before a man\'s name (Mr. Smith).','Título antes do nome de um homem (Sr. Silva).','男の人の名前のあとにつける呼び方。','用在男士姓名前的称呼（如：王先生）。')),
            ('000002129',('Title before a woman\'s name, married or not (Ms. Smith).','Título antes do nome de uma mulher, casada ou não.','女の人の名前のあとにつける呼び方。','用于女士姓名前，不论是否已婚。')),
            ('000001337',('Title before a married woman\'s name (Mrs. Smith).','Título antes do nome de uma mulher casada.','結婚している女の人の名前のあとにつける呼び方。','用在已婚女士的姓前（如：王太太）。'))):
    for l,x in zip(L,d): setd(i,l,x)
new('title-miss',('Miss',),('Srta.','senhorita'),('〜さん','〜さん','~ san'),('小姐','xiǎojiě'),
 {'en':'Title before an unmarried woman\'s name (Miss Smith).','pt':'Título antes do nome de uma mulher solteira.','ja':'結婚していない女の人の名前のあとにつける呼び方。','zh':'用在未婚女子的姓前（如：李小姐）。'})
W('000000550','pt-BR','Dr.',a=['doutor']); W('000000550','zh','医生','yīshēng',a=['博士'])
# identidade
st('000002409',None)
W('000002409','en','ID',a=['identity card','identity']); W('000002409','pt-BR','identidade',a=['RG','carteira de identidade'])
W('000002409','ja','身分証明書','みぶんしょうめいしょ','mibun shoumeisho',['身分証']); W('000002409','zh','身份证','shēnfènzhèng')
for l,x in zip(L,('A card that shows who you are.','Documento que mostra quem você é.','自分がだれかを示すカード。','证明自己身份的证件。')): setd('000002409',l,x)
# favor: お願い mantido; explicação no card
setd('000002537','ja','人のためにしてあげる親切なこと。「お願いがあります」のように頼むときにも使う。')
# describe ≠ explain
W('000002632','ja','描写する','びょうしゃする','byousha suru',['述べる']); W('000002632','zh','描述','miáoshù',a=['描写'])
setd('000002632','ja','ものや人がどんなようすかを言葉で表す。「説明する」はわけを話すこと。')
# retirement: só 定年退職; 退職 explicado
setd('000002816','ja','年をとって仕事をやめること。「退職」は理由に関係なく仕事をやめること。')
setd('000002816','pt-BR','Deixar de trabalhar por causa da idade. (Em japonês, 退職 é sair do emprego por qualquer motivo; 定年退職 é a aposentadoria.)')
# well-being = happiness
h='000003864'
for l in L: E(h,l)['alternatives']=list(dict.fromkeys((E(h,l).get('alternatives') or [])+[E('000003865',l)['text']]))
E(h,'ja')['alternatives']=[x for x in E(h,'ja')['alternatives'] if x!='ウェルビーイング']+['幸福']
st('000003865','search_only')
# fair = feira em todos
st('000003974',None)
W('000003974','ja','フェア','フェア','fea',['市']); W('000003974','zh','集市','jíshì',a=['博览会'])
for l,x in zip(L,('An event with stalls where things are shown or sold.','Evento com barracas para mostrar ou vender coisas.','店がならび、物を見せたり売ったりする催し。','摆摊展示或出售东西的活动。')): setd('000003974',l,x)
# swear = xingar
st('000004055',None)
W('000004055','ja','ののしる','ののしる','nonoshiru',['悪態をつく']); W('000004055','zh','骂人','mà rén',a=['说脏话'])
E('000004055','ja')['forms']=[]
setd('000004055','ja','ひどい言葉で人を悪く言う。「悪口を言う」はその人がいないところで悪く言うこと。')
setd('000004055','pt-BR','Usar palavrões ou ofender alguém com palavras. (Falar mal de alguém pelas costas é outra coisa: maldizer, fofocar.)')
# expressões unidirecionais: só no idioma de origem (en); a tradução é explicação
UNI=['000003226','000003334','000003455','000003469','000003497']
UNI+=[i[3:] for i,e in EN.items() if e.get('kind')=='expression' and e['text'] in ('piece of cake','under the weather','hit the road','no worries','on the house','my treat',"what's up?",'give me a sec','grab a bite','grab a coffee','cash out','hang out')]
for i in UNI:
    for l in ('pt-BR','ja','zh'): E(i,l)['core_status']='search_only'
    for l in L: E(i,l).pop('vcu14_rank',None); E(i,l)['kind']='expression'
for l in L: json.dump(pk[l],open(f'v2/{l}-core-v2.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print('ok',len(UNI))
