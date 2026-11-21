"""T9: flexões/plurais sem lema na lista viram o próprio lema (infinitivo/singular) nos 4 idiomas; a forma antiga vai para o card."""
import json
L=['en','pt-BR','ja','zh']
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
idx={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
EN=idx['en']
def E(i,l): return idx[l]['en:'+i]
def setd(i,l,d):
    e=E(i,l); e['description']=d; e['nativeExplain']={l:d}
    if l=='en': e['description_en']=d
def lemma(i,pos,en,pt,ja,zh,d,key):
    old=E(i,'en')['text']
    for l in L:
        e=E(i,l); e['part_of_speech']=pos; e['core_status']=None; e.pop('inflection_of',None); e.pop('inflection_key',None); e['forms']=[]
    E(i,'en').update(text=en,alternatives=[]); E(i,'pt-BR').update(text=pt[0],alternatives=list(pt[1:]))
    E(i,'ja').update(text=ja[0],reading=ja[1],romanization=ja[2],alternatives=list(ja[3:]))
    E(i,'zh').update(text=zh[0],reading=zh[1],romanization=zh[1],alternatives=list(zh[2:]))
    for l,k in (('en','en'),('pt-BR','pt'),('ja','ja'),('zh','zh')): setd(i,l,d[k])
    if old.lower()!=en.lower():
        E(i,'en')['forms']=[{'form_id':f'en:{i}:f:{key}','lemma_id':'en:'+i,'grammatical_key':key,'text':old,'study_tier':'standard'}]
V=[('000000884','publish',('publicar',),('出版する','しゅっぱんする','shuppan suru'),('出版','chūbǎn'),('To print and sell a book or put news out for the public.','Lançar um livro ou texto para o público.','本などを作って世に出す。','把书等印出来让公众看到。')),
 ('000001123','announce',('anunciar',),('発表する','はっぴょうする','happyou suru'),('宣布','xuānbù'),('To tell people something officially.','Comunicar algo oficialmente.','みんなにおおやけに知らせる。','正式告诉大家。')),
 ('000001233','compare',('comparar',),('比べる','くらべる','kuraberu'),('比较','bǐjiào'),('To look at how things are alike or different.','Ver em que coisas se parecem ou diferem.','ちがいや同じところを見る。','看事物的相同和不同。')),
 ('000001425','be located',('ficar','localizar-se'),('位置する','いちする','ichi suru'),('位于','wèiyú'),('To be in a certain place.','Estar em determinado lugar.','ある場所にある。','在某个地方。')),
 ('000001818','discover',('descobrir',),('発見する','はっけんする','hakken suru','見つける'),('发现','fāxiàn'),('To find something for the first time.','Achar algo pela primeira vez.','はじめて見つける。','第一次找到。')),
 ('000001911','introduce',('apresentar',),('紹介する','しょうかいする','shoukai suru'),('介绍','jièshào'),('To tell someone another person\'s name when they first meet.','Fazer duas pessoas se conhecerem.','人と人を知り合わせる。','让人们互相认识。')),
 ('000001973','propose',('propor',),('提案する','ていあんする','teian suru'),('提议','tíyì'),('To suggest a plan or idea.','Sugerir um plano ou ideia.','考えや計画を出す。','提出计划或想法。')),
 ('000002007','intend',('pretender',),('〜つもりだ','〜つもりだ','~ tsumori da'),('打算','dǎsuan'),('To plan to do something.','Ter a intenção de fazer algo.','何かをしようと考えている。','计划做某事。')),
 ('000002089','select',('selecionar',),('選択する','せんたくする','sentaku suru'),('挑选','tiāoxuǎn','选择'),('To choose carefully from a group.','Escolher com cuidado dentro de um grupo.','いくつかの中からえらぶ。','从一些里面仔细挑。')),
 ('000002111','confirm',('confirmar',),('確認する','かくにんする','kakunin suru'),('确认','quèrèn'),('To say or check that something is true.','Dizer ou verificar que algo é certo.','本当かどうかたしかめる。','核实或说明某事是真的。')),
 ('000002229','reveal',('revelar',),('明らかにする','あきらかにする','akiraka ni suru'),('透露','tòulù'),('To make something secret known.','Tornar conhecido algo que era segredo.','かくれていたことを知らせる。','让秘密的事被知道。')),
 ('000002241','approve',('aprovar',),('承認する','しょうにんする','shounin suru'),('批准','pīzhǔn'),('To officially agree to something.','Dar acordo oficial a algo.','正式によいとみとめる。','正式同意。')),
 ('000002296','collect',('juntar','coletar','colecionar'),('集める','あつめる','atsumeru'),('收集','shōují'),('To bring things together.','Reunir coisas.','物をひとつに集める。','把东西聚在一起。')),
 ('000002302','elect',('eleger',),('選出する','せんしゅつする','senshutsu suru'),('选举','xuǎnjǔ'),('To choose someone by voting.','Escolher alguém por votação.','投票で人をえらぶ。','通过投票选人。')),
 ('000002421','refer to',('referir-se a','mencionar'),('言及する','げんきゅうする','genkyuu suru'),('提到','tídào'),('To talk about or mention something.','Falar de algo ou mencioná-lo.','あることについて話にだす。','说到某事。')),
 ('000002472','appoint',('nomear',),('任命する','にんめいする','ninmei suru'),('任命','rènmìng'),('To choose someone officially for a job.','Escolher alguém oficialmente para um cargo.','役目に正式につける。','正式让某人担任职务。')),
 ('000002629','define',('definir',),('定義する','ていぎする','teigi suru'),('定义','dìngyì'),('To say exactly what a word or idea means.','Dizer exatamente o que algo significa.','ことばの意味をはっきり決める。','说明词语的确切意思。')),
 ('000002682','declare',('declarar',),('宣言する','せんげんする','sengen suru'),('声明','shēngmíng'),('To say something officially and clearly.','Dizer algo de forma oficial e clara.','おおやけにはっきり言う。','正式而清楚地说。')),
 ('000002688','earn',('ganhar',),('稼ぐ','かせぐ','kasegu'),('挣','zhèng','赚'),('To get money for work.','Receber dinheiro pelo trabalho.','働いてお金をえる。','工作得到钱。')),
 ('000002765','refuse',('recusar',),('断る','ことわる','kotowaru'),('拒绝','jùjué'),('To say no to something.','Dizer não a algo.','いやだと言ってうけない。','不接受。')),
 ('000002876','suffer',('sofrer',),('苦しむ','くるしむ','kurushimu'),('受苦','shòukǔ'),('To feel pain or have problems.','Sentir dor ou passar por dificuldades.','いたみやつらさを感じる。','感到痛苦。')),
 ('000002787','depend',('depender',),('〜による','〜による','~ ni yoru','次第'),('取决于','qǔjué yú'),('To change according to something ("it depends").','Variar conforme algo ("depende").','あることによって変わる。','根据某事而变化。'))]
for i,en,pt,ja,zh,d in V: lemma(i,'v',en,pt,ja,zh,dict(zip(('en','pt','ja','zh'),d)),'PAST' if i!='000002787' else 'PRES.3SG')
N=[('000001176','worker',('trabalhador',),('労働者','ろうどうしゃ','roudousha'),('工人','gōngrén'),('A person who works.','Pessoa que trabalha.','はたらく人。','工作的人。')),
 ('000001282','resource',('recurso',),('資源','しげん','shigen'),('资源','zīyuán'),('Something useful that you can use, like water or money.','Algo útil que se pode usar, como água ou dinheiro.','役に立つもの（水やお金など）。','可以利用的东西，如水或钱。')),
 ('000001738','skill',('habilidade',),('技能','ぎのう','ginou','スキル'),('技能','jìnéng'),('The ability to do something well.','Capacidade de fazer algo bem.','うまくできる力。','把事情做好的能力。')),
 ('000001893','citizen',('cidadão',),('市民','しみん','shimin'),('公民','gōngmín'),('A person who belongs to a country or city.','Pessoa que pertence a um país ou cidade.','国や町に属する人。','属于一个国家或城市的人。')),
 ('000001999','element',('elemento',),('要素','ようそ','youso'),('要素','yàosù'),('One part of something.','Uma das partes de algo.','ものをつくる一つの部分。','组成事物的一部分。')),
 ('000002103','affair',('assunto',),('事柄','ことがら','kotogara'),('事务','shìwù'),('A matter or event.','Questão ou acontecimento.','ことがらやできごと。','事情或事件。')),
 ('000002136','relation',('relação',),('関係','かんけい','kankei'),('关系','guānxi'),('The way people or things are connected.','Forma como pessoas ou coisas se ligam.','人や物のつながり。','人或事物之间的联系。')),
 ('000002271','requirement',('requisito',),('必要条件','ひつようじょうけん','hitsuyou jouken'),('要求','yāoqiú'),('Something that is needed.','Algo que é necessário.','ひつようなこと。','需要的条件。')),
 ('000002272','resident',('morador',),('住民','じゅうみん','juumin'),('居民','jūmín'),('A person who lives in a place.','Pessoa que mora num lugar.','そこに住んでいる人。','住在某地的人。')),
 ('000002481','circumstance',('circunstância',),('状況','じょうきょう','joukyou'),('情况','qíngkuàng'),('A fact or condition around an event.','Condição que envolve um fato.','できごとのまわりのようす。','事情发生时的情况。')),
 ('000002544','institution',('instituição',),('機関','きかん','kikan'),('机构','jīgòu'),('A large organization, like a school or bank.','Grande organização, como escola ou banco.','学校や銀行のような大きな組織。','像学校或银行那样的大组织。')),
 ('000002762','politician',('político',),('政治家','せいじか','seijika'),('政治家','zhèngzhìjiā'),('A person who works in politics.','Pessoa que trabalha com política.','政治をする人。','从事政治的人。')),
 ('000002926','technique',('técnica',),('技術','ぎじゅつ','gijutsu'),('技巧','jìqiǎo'),('A special way of doing something.','Maneira especial de fazer algo.','何かをするための方法やわざ。','做事的特别方法。')),
 ('000002936','aspect',('aspecto',),('側面','そくめん','sokumen'),('方面','fāngmiàn'),('One part or side of a situation.','Um lado de uma situação.','ものごとの一つの面。','事情的一个方面。')),
 ('000002976','regulation',('regulamento','regra'),('規則','きそく','kisoku'),('规定','guīdìng'),('An official rule.','Regra oficial.','おおやけのきまり。','正式的规定。')),
 ('000001662','leaf',('folha',),('葉','は','ha','葉っぱ'),('叶子','yèzi'),('A flat green part of a plant.','Parte verde e achatada da planta.','植物の平たい緑の部分。','植物上扁平的绿色部分。'))]
for i,en,pt,ja,zh,d in N: lemma(i,'n',en,pt,ja,zh,dict(zip(('en','pt','ja','zh'),d)),'PL')
# duplicatas/flexões com lema existente
by={e['text'].lower():i for i,e in EN.items() if e.get('core_status') is None}
for i,b,k in (('000002595','happen','PAST'),('000002646','put','PAST'),('000002903','feed','PAST'),('000000118','go','ING'),('000000358','give','PTCP_PAST'),('000002807',None,None)):
    for l in L: E(i,l)['core_status']='search_only'
    if b and b in by:
        e=EN[by[b]]; fs=e.get('forms') or []
        t=E(i,'en')['text']
        if not any(f.get('text')==t for f in fs): fs.append({'form_id':f'{by[b]}:f:{k}:{t}','lemma_id':by[b],'grammatical_key':k,'text':t,'study_tier':'standard'})
        e['forms']=fs
for e in EN.values():
    for f in e.get('forms') or []:
        if f.get('text')=='am' and f.get('grammatical_key')=='PRES.3SG': f['grammatical_key']='PRES.1SG'
for l in L: json.dump(pk[l],open(f'v2/{l}-core-v2.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print('ok')
