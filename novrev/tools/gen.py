import json,sys,pykakasi,pypinyin
K=pykakasi.kakasi()
def ro(s): return ' '.join(x['hepburn'] for x in K.convert(s))
def py(s): return ' '.join(a[0] for a in pypinyin.pinyin(s,style=pypinyin.Style.TONE))
def lines(rows,start):
    out=[];n=start;meta=[]
    for r in rows:
        lv,pos,et,ed,pt,pd,jt,jr,jd,zt,zd,iss=r
        out.append(json.dumps({"new":1,"i":"%09d"%n,"de":ed,"lv":lv,"pos":pos,"en":{"t":et,"d":ed},"pt-BR":{"t":pt,"d":pd},"ja":{"t":jt,"r":jr,"ro":ro(jr),"d":jd},"zh":{"t":zt,"r":py(zt),"d":zd}},ensure_ascii=False))
        meta.append((n,iss)); n+=1
    return out,meta
