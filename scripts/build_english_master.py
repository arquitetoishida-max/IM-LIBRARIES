#!/usr/bin/env python3
"""Build an English-first master; ids are immutable, ranking is independent.
English surface forms are NOT asserted to be disambiguated international concepts.
"""
import json, pathlib, re, datetime, hashlib
from wordfreq import top_n_list, zipf_frequency
from nltk.corpus import wordnet as wn
FREQ_PATH=pathlib.Path("frequency/en.json")
FREQ_PATH.parent.mkdir(exist_ok=True)
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
frequency_entries=[]
for idx,w in enumerate(words,1):
 e=existing.get(w)
 if e is None:
  e={"concept_id":new_id(),"headword":w,"category":"common","kind":"word","language":"en","senses":[],"definitions_en":[],"cefr":None,"cefr_status":"unclassified","variants":[],"mapping_status":"lexical-headword-unresolved"}
  existing[w]=e
 e.pop("frequency",None)
 frequency_entries.append({"english_id":e.get("english_id",f"en:{e['concept_id'].split(':')[-1]}"),"word":w,"rank":idx,"zipf":round(zipf_frequency(w,"en"),2)})
 e["english_id"]=e.get("english_id",f"en:{e['concept_id'].split(':')[-1]}")
 e["frequency_reference"]="frequency/en.json"
 e["frequency_initial_rank"]=idx
 # Retain all attested WordNet senses separately; never mark headword as one universal sense.
 synsets=wn.synsets(w)
 e["senses"]=[{"sense_id":e["english_id"]+":wn:"+x.name(),"pos":x.pos(),"definition_en":x.definition(),"source":"Princeton WordNet 3.0","status":"dictionary-sense-not-translation-reviewed"} for x in synsets[:12]]
 e["definitions_en"]=[x.definition() for x in synsets[:3]]
 e["short_description_en"]=(synsets[0].definition() if synsets else None)
 e["definition_status"]="wordnet-attested" if synsets else "missing-dictionary-definition"
 # CEFR tier here is a clearly marked starting estimate from rank, NOT an official CEFR list.
 e["cefr"]=("A1" if idx<=500 else "A2" if idx<=1100 else "B1" if idx<=1800 else "B2" if idx<=2400 else "C1")
 e["cefr_status"]="heuristic-frequency-only-unreviewed"
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
 ["take a rain check","postpone an invitation","US / widespread",["US","GB"],"Politely postpone an invitation or plan."],
 ["spill the tea","share gossip","US / online",["US","internet"],"Share gossip or revealing information."],
 ["low-key","somewhat; discreetly","US / online",["US","internet"],"Describes something understated or discreet."],
 ["high-key","openly; strongly","US / online",["US","internet"],"Expresses something openly or strongly."],
 ["ghost someone","suddenly stop replying","Online / widespread",["US","GB","internet"],"Suddenly stop communicating without explanation."],
 ["flex","show off","US / online",["US","internet"],"Show off an achievement or possession."],
 ["salty","resentful or annoyed","US / online",["US","internet"],"Feeling bitter or irritated about something."],
 ["legit","genuine; really good","US / widespread",["US","GB"],"Genuine, credible or impressively good."],
 ["sick","excellent","US / youth slang",["US"],"Informal praise for something impressive."],
 ["lit","exciting","US / online",["US","internet"],"Very exciting, lively or enjoyable."],
 ["sus","suspicious","Online / gaming",["internet","US"],"Short informal form of suspicious."],
 ["cap","lie or exaggeration","US / online",["US","internet"],"A lie or exaggerated claim."],
 ["no cap","seriously; no lie","US / online",["US","internet"],"Emphasizes that something is truthful."],
 ["bet","okay; agreed","US / youth slang",["US"],"Informal way to express agreement."],
 ["fam","close friends or family","UK / US",["GB","US"],"Informal address for close associates."],
 ["bro","male friend","Widespread English",["US","GB","AU"],"Casual address to a friend."],
 ["dude","person or friend","US / widespread",["US","GB"],"Very informal address to someone."],
 ["hangry","irritable from hunger","Widespread English",["US","GB","AU"],"Irritable because of being hungry."],
 ["crash at","sleep at someone's place","US / widespread",["US","GB"],"Stay overnight somewhere informally."],
 ["hit the road","leave; depart","Widespread English",["US","GB","AU"],"Set off or begin a journey."],
 ["piece of cake","very easy","Widespread English",["US","GB","AU"],"Something that is very easy."],
 ["break a leg","good luck","Widespread English",["US","GB"],"Wish someone success before a performance."],
 ["under the weather","feeling unwell","Widespread English",["US","GB","AU"],"Feeling mildly ill or unwell."],
 ["give me a sec","wait a moment","Widespread English",["US","GB"],"Ask someone to wait briefly."],
 ["my treat","I'll pay","Widespread English",["US","GB","AU"],"Offer to pay for another person."],
 ["on the house","free from the business","Hospitality / widespread",["US","GB","AU"],"Provided free by a business."],
 ["grab a coffee","have coffee together","Widespread English",["US","GB","AU"],"Meet or stop for coffee."],
 ["takeaway","food to take out","UK / Australia",["GB","AU"],"Prepared food eaten away from its shop."],
 ["takeout","food to take out","US",["US"],"Prepared food intended to eat elsewhere."],
 ["cuppa","cup of tea","UK / Australia",["GB","AU"],"Informal term for a cup of tea."],
 ["knackered","exhausted","UK",["GB"],"Extremely tired or worn out."],
 ["skint","having no money","UK",["GB"],"Having very little or no money."],
 ["faff","waste time fussing","UK",["GB"],"Spend time on unnecessary fussing."],
 ["bloke","man","UK / Australia",["GB","AU"],"Casual word for a man."],
 ["uni","university","UK / Australia",["GB","AU"],"Informal abbreviation of university."],
 ["rubbish","nonsense; trash","UK",["GB"],"Rubbish can mean nonsense or garbage."],
 ["cheeky","playfully bold","UK / Australia",["GB","AU"],"Playfully impudent or slightly bold."],
 ["proper","very; genuinely","UK informal",["GB"],"Informal intensifier meaning very or genuinely."],
 ["innit","isn't it; agreement tag","UK",["GB"],"Informal question tag seeking agreement."],
 ["peng","attractive; excellent","UK urban slang",["GB"],"Describes someone attractive or something excellent."],
 ["bare","a lot of; very","UK urban slang",["GB"],"Informal intensifier meaning many or very."],
 ["mandem","group of male friends","UK urban slang",["GB"],"Informal term for a male friend group."],
 ["banger","excellent song","UK / widespread",["GB","US"],"A particularly popular or enjoyable song."],
 ["bucks for the bang","value for money","US",["US"],"Relates a purchase to perceived value."],
 ["youse","plural you","US regional / Ireland / Australia",["US","IE","AU"],"Nonstandard plural form of you."],
 ["fixin' to","about to","US South",["US-South","US-TX"],"Regional expression meaning about to do something."],
 ["howdy","hello","US South / West",["US-TX","US-South"],"Friendly informal greeting."],
 ["all y'all","all of you","US South",["US-TX","US-South"],"Emphatic plural address to a group."],
 ["pop","soft drink","US regional",["US-Midwest","US-North"],"Regional word for a carbonated soft drink."],
 ["soda","soft drink","US regional",["US"],"Common term for a carbonated soft drink."],
 ["the L","elevated train or Chicago rail","Chicago",["US-IL-Chicago"],"Local nickname for Chicago's rail system."],
 ["the T","Boston public transit","Boston",["US-MA-Boston"],"Local nickname for Boston's transit system."],
 ["the Tube","London Underground","London",["GB-London"],"Informal name for London's subway system."],
 ["the subway","urban underground railway","US / Canada",["US","CA"],"Name for a rapid urban rail system."],
 ["metro","urban rapid transit","US / Europe",["US","GB"],"Term for an urban rail network."],
 ["deadass","seriously","New York / online",["US-NY","internet"],"Emphasizes sincerity or seriousness."],
 ["brick","very cold","New York regional",["US-NY"],"Regional slang for extremely cold weather."],
 ["mad","very; a lot","New York / US",["US-NY","US"],"Colloquial intensifier meaning very."],
 ["jawn","thing; person; place","Philadelphia",["US-PA-Philadelphia"],"Versatile regional noun for almost anything."],
 ["yinz","plural you","Pittsburgh",["US-PA-Pittsburgh"],"Regional plural form of you."],
 ["hella good","very good","Northern California",["US-CA"],"Very good, using California slang."],
 ["the 405","Interstate 405 freeway","Southern California",["US-CA"],"Informal reference to the I-405 freeway."],
 ["the 101","U.S. Route 101","California",["US-CA"],"Colloquial reference to the 101 highway."],
 ["no biggie","not a problem","US / widespread",["US","GB"],"Means something is not a problem."],
 ["rain check","postponement","US / widespread",["US","GB"],"Promise to accept an offer later."],
 ["cash out","withdraw money; finish","US / online",["US","internet"],"Withdraw funds or conclude a transaction."],
]
out=list(existing.values())
rank_lookup={w:i for i,w in enumerate(words,1)}
for i,(phrase,gloss,where,regions,definition) in enumerate(slang,1):
 key="slang:"+phrase
 # Separate entries with their own ids; equivalence to common headword not auto-assumed.
 prev=next((e for e in old.get("entries",[]) if e.get("slug")==key),None)
 out.append(prev or {"concept_id":new_id(),"lexeme_id":f"iml:en:slang:{i:06d}","slug":key,"headword":phrase,"category":"regional-colloquial","kind":"expression" if " " in phrase or "'" in phrase else "word","language":"en","definitions_en":[definition],"english_gloss":gloss,"register":"slang-or-informal","regions":regions,"regional_note":where,"cefr":None,"cefr_status":"unclassified","frequency":None,"mapping_status":"provisional-not-sense-verified","related_english_form":gloss,"source_review":"requires regional evidence review"})
for e in out:
 if e.get("category")=="regional-colloquial":
  e["english_id"]=e.get("english_id",f"en:{e['concept_id'].split(':')[-1]}")
  e["short_description_en"]=e["definitions_en"][0] if e.get("definitions_en") else None
  e["cefr_status"]="not-applicable-regional-expression"
  e["frequency_reference"]="frequency/en.json"
out.sort(key=lambda e:(0 if e.get("category")=="common" else 1,rank_lookup.get(e.get("headword"),100000),e.get("headword","")))
FREQ_PATH.write_text(json.dumps({"schema_version":1,"language":"en","source":"wordfreq","frequency_scope":"mixed","independent_of_id":True,"entries":frequency_entries},ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
# immutable IDs, top-level ordering can change by rank
result={"schema_version":1,"id":"ishida-en-master-v1","created_at":old.get("created_at",datetime.date.today().isoformat()),"version":datetime.date.today().isoformat(),"language":"en","pivot":"English first, but concepts may exist without English","status":"draft-unreviewed","counts":{"common":sum(e.get("category")=="common" for e in out),"slang":sum(e.get("category")=="regional-colloquial" for e in out)},"warnings":["English monolingual dictionary, not bilingual translations.","WordNet senses identify English meanings; cross-language translation mapping is NOT done.","CEFR is only a frequency-based preliminary estimate, not a validated CEFR word list.","Regional slang tags are provisional and require source review."],"entries":out}
PATH.write_text(json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
catpath=pathlib.Path("catalog.json")
cat=json.loads(catpath.read_text(encoding="utf-8"))
pkgs=[p for p in cat["packages"] if p.get("id") not in ("ishida-en-master-v1","ishida-en-frequency-v1")]
pkgs.append({"id":"ishida-en-master-v1","version":result["version"],"name":"Ishida English Master — 3000 common + regional expressions (DRAFT)","kind":"lexical-master","language":"en","languages":["en"],"entries":len(out),"status":"draft-unreviewed","verified_for_production":False,"url":"https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/master/en-master-v1.json","sha256":hashlib.sha256(PATH.read_bytes()).hexdigest(),"description":"Monolingual English entries with attested WordNet senses, provisional CEFR estimates and slang tags; NOT cross-language mappings."})
pkgs.append({"id":"ishida-en-frequency-v1","version":result["version"],"name":"English frequency rankings","kind":"frequency","language":"en","languages":["en"],"entries":len(frequency_entries),"status":"source-ranked","verified_for_production":False,"url":"https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/frequency/en.json","sha256":hashlib.sha256(FREQ_PATH.read_bytes()).hexdigest()})
cat["packages"]=pkgs
catpath.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Built",len(out),"entries (",result["counts"],")")
