"""T4: gírias/regionalismos fora do núcleo (search_only/retired) + correções enviadas pela comunidade (20/11). Idempotente."""
import json
L=['en','pt-BR','ja','zh']
pk={l:json.load(open(f'v2/{l}-core-v2.json')) for l in L}
idx={l:{e['english_id']:e for e in pk[l]['entries']} for l in L}
SLANG="3073 3066 3021 3081 3040 3022 3071 3004 3086 3072 3067 3038 3036 3005 3003 3065 3070 3077 3082 3088".split()
for s in SLANG:
    for l in L:
        e=idx[l].get('en:00000'+s)
        if e is not None: e['core_status']='search_only'
for l in L:  # jawn → あれ: par enganoso
    e=idx[l]['en:000003084']; e['core_status']='retired'
def setd(l,i,**kw):
    e=idx[l][i]
    for k,v in kw.items():
        if k=='description':
            e['description']=v; ne=e.get('nativeExplain') if isinstance(e.get('nativeExplain'),dict) else {}; ne[l]=v; e['nativeExplain']=ne
            if l=='en': e['description_en']=v
        else: e[k]=v
# its → それの (その é "aquele/esse")
setd('ja','en:000000073',text='それの',reading='それの',romanization='sore no',alternatives=['その'],description='それのもの。その物や動物のもの。')
# around → ごろ / ぐらい (o usuário pediu ぐらい: aproximadamente)
setd('ja','en:000003919',alternatives=['〜くらい','〜ぐらい'],description='だいたいの数や時刻。「〜ごろ」は時刻、「〜ぐらい」は数や量。')
# American (coisa) vs nacionalidade
setd('ja','en:000000293',description='アメリカの物やこと。人の国籍は「アメリカ人」。')
setd('en','en:000000293',description='Of or from the United States, for things. For a person\'s nationality see "American person".')
setd('pt-BR','en:000000293',description='Dos Estados Unidos, para coisas. A nacionalidade de uma pessoa é "americano/a" (アメリカ人).')
setd('zh','en:000000293',alternatives=[],description='美国的，指事物；人的国籍说"美国人"。')
for l in L:
    open(f'v2/{l}-core-v2.json','w',encoding='utf8').write(json.dumps(pk[l],ensure_ascii=False,indent=1))
print('ok')
