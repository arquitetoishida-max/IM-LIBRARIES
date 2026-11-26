"""Tabela compacta (en|pos|amb|pt|pt_alt|pt_desc|ja|ja_alt|ja_leitura|ja_desc|zh|zh_alt|pinyin|zh_desc|en_desc; variantes com ;) → ops new."""
import json,sys
ENV={'clothes':'shopping','body':'body_health','school':'school_learning','time':'weather_emotion_time'}
out=[]
for r in open(sys.argv[1],encoding='utf-8'):
    f=r.rstrip('\n').split('|')
    if len(f)<15: continue
    assert len(f)==15,(len(f),r[:30])
    en,pos,env,pt,pta,ptd,ja,jaa,jar,jad,zh,zha,zhp,zhd,end=f
    A=lambda s:[x for x in s.split(';') if x]
    out.append(json.dumps({'op':'new','vcu14':[ENV.get(env,env)],'pos':pos,'level':'A2','en':{'text':en,'desc':end},
      'pt-BR':{'text':pt,'alt':A(pta),'desc':ptd},'ja':{'text':ja,'alt':A(jaa),'reading':jar,'desc':jad},
      'zh':{'text':zh,'alt':A(zha),'reading':zhp,'desc':zhd}},ensure_ascii=False))
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(out)+'\n'); print(len(out))
