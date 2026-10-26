#!/usr/bin/env python3
"""Build an English-first master; ids are immutable, ranking is independent.
English surface forms are NOT asserted to be disambiguated international concepts.
"""
import json, pathlib, re, datetime, hashlib
from wordfreq import top_n_list, zipf_frequency
ROOT=pathlib.Path("master"); ROOT.mkdir(exist_ok=True)
PATH=ROOT/"en-master-v1.json"
TARGET=3000
old=json.loads(PATH.read_text(encoding="utf-8")) if PATH.exists() else {"entries":[]}
existing={e["headword"].casefold():e for e in old.get("entries",[]) if e.get("headword") and e.get("category")=="common"}
taken_ids={e["concept_id"] for e in old.get("entries",[])}
next_num=max([int(x.split(":")[-1]) for x in taken_ids] or [0])+1
def new_id():
 global next_num
 n=next_num;next_num+=1
 return f"imc:{n:09d}"
def valid(s):
 return bool(re.fullmatch(r"[a-z]+(?:['-][a-z]+)*",s)) and len(s)>1 and len(s)<=35
words=[]
for w in top_n_list("en",10000):
 w=w.strip().lower()
 if valid(w) and w not in words:words.append(w)
 if len(words)>=TARGET:break
if len(words)<TARGET:raise RuntimeError(f"Only {len(words)} candidates")
for idx,w in enumerate(words,1):
 e=existing.get(w)
 if e is None:
  e={"concept_id":new_id(),"headword":w,"category":"common","kind":"word","language":"en","senses":[],"definitions_en":[],"cefr":None,"cefr_status":"unclassified","variants":[],"mapping_status":"lexical-headword-unresolved"}
  existing[w]=e
 e["frequency"]={"rank":idx,"zipf":round(zipf_frequency(w,"en"),2),"language":"en","source":"wordfreq","frequency_scope":"mixed"}
 e["initial_rank"]=e.get("initial_rank",idx)
 e["learning_band"]=("core" if idx<=500 else "high-frequency" if idx<=1500 else "extended")
 e["lexeme_id"]=e.get("lexeme_id",f"iml:en:{e['concept_id'].split(':')[1]}")
 # Concept ids are reserved as draft slots pending word-sense disambiguation.
# Every colloquial form below receives a separate lexeme id; linkage is editorial,
# tentative, and may need splitting for pragmatics or near synonyms.
slang=[
 ("bucks","dollars","US",["US"],"Informal term for dollars."),
 ("quid","pound sterling","UK",["GB"],"Informal term for a pound."),
 ("y'all","you all","US South",["US-TX","US-South"],"Informal plural form of you."),
 ("hella","very","Northern California",["US-CA"],"Intensifier meaning very or a lot."),
 ("wicked","very","New England",["US-MA","US-New-England"],"Regional intensifier meaning very."),
 ("mate","friend","UK / Australia",["GB","AU"],"Friendly informal form of address."),
 ("loo","toilet","UK",["GB"],"Informal word for toilet."),
 ("cheers","thanks","UK / Australia",["GB","AU"],"Casual expression of thanks."),
 ("gonna","going to","English-speaking",["US","GB","AU"],"Informal spoken form of going to."),
 ("wanna","want to","English-speaking",["US","GB","AU"],"Informal spoken form of want to."),
 ("no worries","it's okay","Australia / global",["AU","GB","US"],"Reassures someone that everything is fine."),
 ("what's up?","how are you?","US / global",["US","GB"],"Very informal way to greet someone."),
 ("hang out","spend time together","English-speaking",["US","GB","AU"],"Spend relaxed time with other people."),
 ("grab a bite","eat something","US / global",["US","GB"],"Have something quick to eat."),
 ("I'm beat","I'm exhausted","US",["US"],"Means feeling extremely tired."),
 ("my bad","my mistake","US / global",["US","GB"],"Casual admission of a mistake."),
 ("awesome","excellent","US / global",["US","GB","AU"],"Enthusiastic positive evaluation."),
 ("dodgy","suspicious","UK / Australia",["GB","AU"],"Suspicious or not very reliable."),
 ("gutted","very disappointed","UK",["GB"],"Very disappointed about a setback."),
 ("chuffed","pleased","UK",["GB"],"Very pleased or proud."),
 ("bodega","corner shop","New York",["US-NY"],"Small neighborhood convenience store."),
 ("finna","about to","US, African American English",["US"],"Indicates an action is about to occur."),
 ("ain't","is not / are not / has not","Various English dialects",["US","GB"],"Nonstandard contraction with several meanings."),
 ("brb","be right back","Online English",["internet"],"Short message meaning be right back."),
 ("idk","I don't know","Online English",["internet"],"Short message meaning I don't know."),
]
out=list(existing.values())
for i,(phrase,gloss,where,regions,definition) in enumerate(slang,1):
 key="slang:"+phrase
 # Separate entries with their own ids; equivalence to common headword not auto-assumed.
 prev=next((e for e in old.get("entries",[]) if e.get("slug")==key),None)
 out.append(prev or {"concept_id":new_id(),"lexeme_id":f"iml:en:slang:{i:06d}","slug":key,"headword":phrase,"category":"regional-colloquial","kind":"expression" if " " in phrase or "'" in phrase else "word","language":"en","definitions_en":[definition],"english_gloss":gloss,"register":"slang-or-informal","regions":regions,"regional_note":where,"cefr":None,"cefr_status":"unclassified","frequency":None,"mapping_status":"provisional-not-sense-verified","related_english_form":gloss,"source_review":"requires regional evidence review"})
out.sort(key=lambda e:(0 if e.get("category")=="common" else 1,(e.get("frequency") or {}).get("rank",100000),e.get("headword","")))
# immutable IDs, top-level ordering can change by rank
result={"schema_version":1,"id":"ishida-en-master-v1","created_at":old.get("created_at",datetime.date.today().isoformat()),"version":datetime.date.today().isoformat(),"language":"en","pivot":"English first, but concepts may exist without English","status":"draft-unreviewed","counts":{"common":sum(e.get("category")=="common" for e in out),"slang":sum(e.get("category")=="regional-colloquial" for e in out)},"warnings":["Common entries are lexemes, NOT yet disambiguated into certified international senses.","CEFR is blank until an evidence-supported assignment.","Regional slang tags are provisional pending sources and human review.","Do not offer as verified cross-language dictionary."],"entries":out}
PATH.write_text(json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
catpath=pathlib.Path("catalog.json")
cat=json.loads(catpath.read_text(encoding="utf-8"))
pkgs=[p for p in cat["packages"] if p.get("id")!="ishida-en-master-v1"]
pkgs.append({"id":"ishida-en-master-v1","version":result["version"],"name":"Ishida English Master — 3000 common + regional expressions (DRAFT)","kind":"lexical-master","language":"en","languages":["en"],"entries":len(out),"status":"draft-unreviewed","verified_for_production":False,"url":"https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/master/en-master-v1.json","sha256":hashlib.sha256(PATH.read_bytes()).hexdigest(),"description":"English pivot entries, ranks, provisional slang region tags; not certified cross-language sense mappings."})
cat["packages"]=pkgs
catpath.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Built",len(out),"entries (",result["counts"],")")
