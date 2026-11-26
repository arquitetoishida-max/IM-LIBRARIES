import json,collections
R='/home/claude/im-libraries/'
L=['en','pt-BR','ja','zh']
P={l:json.load(open(R+f'v2/{l}-core-v2.json'))['entries'] for l in L}
ids=[e['english_id'] for e in P['en']]
assert len(set(ids))==len(ids)
for l in L:
    assert set(e['english_id'] for e in P[l])==set(ids) and P[l][-1]['english_id']==ids[-1],l
    pr=[e['study_priority'] for e in P[l] if e.get('study_priority')]
    c=collections.Counter(pr); assert max(c.values())==1,(l,[k for k,v in c.items() if v>1][:3])
    for e in P[l]: assert e['text'] and e['description'],(l,e['id'])
print('ok',len(ids))
