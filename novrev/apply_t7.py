"""T7: regras do dono (planilha 20/11): sem id para flexões/plurais; comparativos ficam; desambiguar sentidos e classes;
masculino padrão no pt; parentesco por idioma; duplicatas fora; antônimos só mesma classe e sentido. Idempotente por marcador."""
import json,re,copy
L=['en','pt-BR','ja','zh']
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
idx={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
EN=idx['en']
def E(i,l='en'): return idx[l]['en:'+i if not i.startswith('en:') else i]
def act(i): return E(i).get('core_status') is None
def setall(i,**kw):
    for l in L:
        for k,v in kw.items(): E(i,l)[k]=v
def desc(i,l,d):
    e=E(i,l); e['description']=d; ne=e.get('nativeExplain') if isinstance(e.get('nativeExplain'),dict) else {}; ne[l]=d; e['nativeExplain']=ne
    if l=='en': e['description_en']=d
def word(i,l,t=None,r=None,ro=None,a=None):
    e=E(i,l)
    if t is not None: e['text']=t
    if r is not None: e['reading']=r
    if ro is not None: e['romanization']=ro
    if a is not None: e['alternatives']=[x for x in a if x!=e['text']]
def ant(i,ids):
    for l in L: E(i,l)['antonyms']=['en:'+x for x in ids]
def addant(i,j):
    for a,b in ((i,j),(j,i)):
        cur=[x[3:] for x in E(a).get('antonyms') or []]
        if b not in cur: ant(a,cur+[b])
def delant(i,j):
    for a,b in ((i,j),(j,i)):
        cur=[x[3:] for x in E(a).get('antonyms') or []]
        if b in cur: ant(a,[x for x in cur if x!=b])
def retire(i,why='t7'):
    for l in L: E(i,l)['core_status']='search_only'
    for l in L:  # antônimos apontando para ele saem
        for e in pk[l]['entries']:
            if 'en:'+i in (e.get('antonyms') or []): e['antonyms']=[x for x in e['antonyms'] if x!='en:'+i]
TPL={l:E('000000774',l) for l in L}
KEEP=['kind','source_status','translation_confidence','study_tier','user_hint']
nxt=[max(int(i[3:]) for i in EN)+1]
def new(key,pos,en,pt,ja,zh,d,hide=(),level='A2'):
    # idempotente: procura por marcador t7_key
    for e in pk['en']['entries']:
        if e.get('t7_key')==key: return e['english_id'][3:]
    eid=f'en:{nxt[0]:09d}'; nxt[0]+=1
    for l in L:
        e={k:copy.deepcopy(TPL[l][k]) for k in KEEP if k in TPL[l]}
        e.update({'id':f'{l}:{eid}','english_id':eid,'english_sense_id':None,'part_of_speech':pos,'level':level,'antonyms':[],'novrev_status':'reviewed','t7_key':key,'study_priority':(TPL[l].get('study_priority') or 700)})
        e['description_en']=d['en']
        if l=='en': e.update(text=en[0],alternatives=list(en[1:]))
        if l=='pt-BR': e.update(text=pt[0],alternatives=list(pt[1:]))
        if l=='ja': e.update(text=ja[0],reading=ja[1],romanization=ja[2],alternatives=list(ja[3:]))
        if l=='zh': e.update(text=zh[0],reading=zh[1],romanization=zh[1],alternatives=list(zh[2:]))
        e['description']=d[{'pt-BR':'pt'}.get(l,l)]; e['nativeExplain']={l:e['description']}
        if l in hide: e['core_status']='search_only'
        pk[l]['entries'].append(e); idx[l][eid]=e
    return eid[3:]

# ---- desambiguação (respostas do dono) ----
desc('000000156','en','A part of a country with its own government.'); desc('000000156','pt-BR','Divisão de um país com governo próprio.')
desc('000000156','ja','国の中の、自分の政府をもつ地域。'); desc('000000156','zh','国家里有自己政府的一级行政区。')
st=new('state-condition','n',('state',),('estado','condição'),('状態','じょうたい','joutai'),('状态','zhuàngtài'),
 {'en':'The condition someone or something is in.','pt':'Condição em que alguém ou algo se encontra.','ja':'人や物がどんなようすかということ。','zh':'人或事物所处的样子。'})
delant('000000203','000001776'); desc('000000203','en','Costing nothing.'); desc('000000203','pt-BR','Que não custa nada.')
fr=new('free-notbusy','adj',('free',),('livre','desocupado'),('暇な','ひまな','hima na'),('有空','yǒu kòng'),
 {'en':'Not busy; having time.','pt':'Sem compromisso; com tempo livre.','ja':'することがなく時間があるようす。','zh':'没有事情做，有时间。'}); addant(fr,'000001776')
desc('000000263','en','Difficult; not easy.'); desc('000000263','pt-BR','Que não é fácil.')
delant('000000263','000002092'); addant('000000263','000000492')
hd=new('hard-solid','adj',('hard',),('duro',),('硬い','かたい','katai'),('硬','yìng'),
 {'en':'Firm and not soft to touch.','pt':'Firme, que não é mole ao toque.','ja':'さわると、やわらかくないようす。','zh':'摸起来不软。'}); addant(hd,'000002092')
delant('000000656','000000422'); desc('000000656','en','A gift.'); desc('000000656','pt-BR','Algo que se dá a alguém; um mimo.')
pr=new('present-now','n',('present',),('presente',),('現在','げんざい','genzai'),('现在','xiànzài'),
 {'en':'The time now.','pt':'O tempo de agora.','ja':'いまの時。','zh':'现在这个时候。'}); addant(pr,'000000422')
setall('000000658',part_of_speech='int'); desc('000000658','en','Said to apologize.'); desc('000000658','pt-BR','Usado para pedir desculpas.')
new('sorry-feel','adj',('sorry',),('com pena','sentir muito'),('気の毒に思う','きのどくにおもう','ki no doku ni omou'),('难过','nánguò','同情'),
 {'en':'Feeling sad for someone ("I\'m sorry to hear that").','pt':'Sentir tristeza pelo problema de alguém.','ja':'人のつらいことを聞いて、かわいそうに思うこと。','zh':'为别人的不幸感到难过。'})
delant('000000785','000001800'); addant('000000785','000000651')
lw=new('lower-verb','v',('lower',),('abaixar','baixar'),('下げる','さげる','sageru'),('降低','jiàngdī'),
 {'en':'To move something down or make it less.','pt':'Pôr mais para baixo ou diminuir.','ja':'物の位置や量を低くする。','zh':'使位置或数量变低。'}); addant(lw,'000001800')
delant('000000814','000004092')
df=new('defense','n',('defense',),('defesa',),('防御','ぼうぎょ','bougyo','守り'),('防守','fángshǒu','防御'),
 {'en':'Protecting yourself or something from attack.','pt':'Ato de proteger-se contra um ataque.','ja':'こうげきから守ること。','zh':'保护自己不受攻击。'}); addant(df,'000000814')
ak=new('attack-verb','v',('attack',),('atacar',),('攻撃する','こうげきする','kougeki suru'),('攻击','gōngjī'),
 {'en':'To try to hurt or defeat someone.','pt':'Tentar ferir ou vencer alguém.','ja':'相手をきずつけたり負かしたりしようとする。','zh':'想伤害或打败对方。'}); addant(ak,'000004092')
delant('000000981','000001421')
word('000000860','ja','すごい','すごい','sugoi',['超']); desc('000000860','ja','とてもいい、すばらしい（くだけた言い方）。'); desc('000000860','en','Very good; great (informal).')
v=E('000000102','ja'); v['alternatives']=list(dict.fromkeys((v.get('alternatives') or [])+['すごく']))
desc('000001309','en','To become bigger or older.'); desc('000001309','pt-BR','Ficar maior ou mais velho.')
setall('000001442',part_of_speech='adj'); 
for l,t in (('en',('broke',)),('pt-BR',('sem dinheiro','duro'))):
    word('000001442',l,t[0],a=list(t[1:]))
word('000001442','ja','金欠の','きんけつの','kinketsu no',['お金がない']); word('000001442','zh','没钱','méi qián',['穷'])
E('000001442','zh')['romanization']='méi qián'
for l,d in (('en','Having no money (informal).'),('pt-BR','Sem nenhum dinheiro (informal).'),('ja','お金がまったくないようす（くだけた言い方）。'),('zh','一点钱也没有（口语）。')): desc('000001442',l,d)
retire('000001555')
word('000001768','en','turn'); word('000001768','pt-BR','vez',a=[])
for l,d in (('en','Your chance to do something in order ("It\'s your turn").'),('pt-BR','Momento de alguém fazer algo, numa ordem.')): desc('000001768',l,d)
setall('000000904',core_status=None); desc('000000904','en','Polite way to address a man you serve, such as a customer.'); desc('000000904','pt-BR','Forma educada de se dirigir a um homem que se atende, como um cliente.')
desc('000000904','ja','店などで、客をていねいによぶ言い方。'); desc('000000904','zh','对男士（如顾客）的礼貌称呼。')
new('rare-meat','adj',('rare',),('mal passado',),('レア','レア','rea'),('三分熟','sān fēn shú'),
 {'en':'(Of meat) cooked only a little, still red inside.','pt':'(Carne) pouco cozida, ainda vermelha por dentro.','ja':'肉が少しだけ焼けていて、中が赤いようす。','zh':'（肉）只煎一点，里面还是红的。'})
new('rice-cooked','n',('rice',),('arroz',),('ご飯','ごはん','gohan'),('米饭','mǐfàn'),
 {'en':'Rice that has been cooked, eaten as food.','pt':'Arroz cozido, servido como comida.','ja':'たいたお米。','zh':'煮熟的米。'})
setall('000003634',core_status=None)
word('000003634','en','solar eclipse'); word('000003634','pt-BR','eclipse solar',a=[]); word('000003634','ja',a=[]); word('000003634','zh',a=[])
for l,d in (('en','When the moon hides the sun.'),('pt-BR','Quando a Lua encobre o Sol.'),('ja','月が太陽をかくすこと。'),('zh','月亮挡住太阳的现象。')): desc('000003634',l,d)
new('lunar-eclipse','n',('lunar eclipse',),('eclipse lunar',),('月食','げっしょく','gesshoku'),('月食','yuèshí'),
 {'en':'When the earth\'s shadow hides the moon.','pt':'Quando a sombra da Terra encobre a Lua.','ja':'地球のかげが月をかくすこと。','zh':'地球的影子挡住月亮的现象。'})
retire('000001117')
new('sound-adj','adj',('sound',),('são',),('無事な','ぶじな','buji na'),('完好','wánhǎo','安然无恙'),
 {'en':'Healthy and not hurt or damaged ("safe and sound").','pt':'Sem ferimento nem dano ("são e salvo").','ja':'けがやこわれたところがないようす。','zh':'没有受伤或损坏。'})
word('000001475','en','versus',a=['vs']); word('000001475','pt-BR','versus',a=['x','contra']); setall('000001475',part_of_speech='prep')
for i in ['000000900','000003155','000004009','000002315','000003436']: retire(i)
# antônimos de classe/sentido errados
delant('000001600','000000878'); addant('000001600','000000850')
delant('000002896','000001889')
delant('000003123','000001596')
en_=new('entrance','n',('entrance',),('entrada',),('入口','いりぐち','iriguchi'),('入口','rùkǒu'),
 {'en':'The way in.','pt':'Lugar por onde se entra.','ja':'中に入るところ。','zh':'进去的地方。'}); addant(en_,'000003123')
delant('000003194','000000394'); delant('000003216','000003217'); delant('000003887','000001161')
word('000001619','ja','どうやら','どうやら','douyara',['〜らしい'])
desc('000001668','en','The inner part of a person; also energy and enthusiasm.')
word('000001699','ja','誇らしい','ほこらしい','hokorashii',['誇りに思う'])
# ---- parentesco: id próprio; some no idioma que não tem palavra própria ----
for t in ['older brother','younger brother','older sister','younger sister']:
    i=[k for k,e in EN.items() if e['text']==t][0]
    for l in ('en','pt-BR'): idx[l][i]['core_status']='search_only'
C=[('older male cousin (father\'s side)','primo mais velho (lado do pai)','堂哥','táng gē'),('younger male cousin (father\'s side)','primo mais novo (lado do pai)','堂弟','táng dì'),
   ('older female cousin (father\'s side)','prima mais velha (lado do pai)','堂姐','táng jiě'),('younger female cousin (father\'s side)','prima mais nova (lado do pai)','堂妹','táng mèi'),
   ('older male cousin (mother\'s side)','primo mais velho (lado da mãe)','表哥','biǎo gē'),('younger male cousin (mother\'s side)','primo mais novo (lado da mãe)','表弟','biǎo dì'),
   ('older female cousin (mother\'s side)','prima mais velha (lado da mãe)','表姐','biǎo jiě'),('younger female cousin (mother\'s side)','prima mais nova (lado da mãe)','表妹','biǎo mèi')]
for en_t,pt_t,zh_t,py in C:
    new('cousin-'+zh_t,'n',(en_t,),(pt_t,),('いとこ','いとこ','itoko'),(zh_t,py),
        {'en':f'A cousin: {en_t}.','pt':f'Um primo ou prima: {pt_t}.','ja':'親のきょうだいの子ども。','zh':f'{zh_t}：'+('父亲兄弟的孩子' if zh_t[0]=='堂' else '母亲兄弟姐妹或父亲姐妹的孩子')+'。'},hide=('en','pt-BR','ja'))
for l in L: json.dump(pk[l],open(f'v2/{l}-core-v2.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print('ok, próximo id',nxt[0])
