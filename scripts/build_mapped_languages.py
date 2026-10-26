#!/usr/bin/env python3
"""Generate approximate PT-BR and Japanese counterparts keyed to English master IDs.
OMW translations are synset-level; preserve evidence and confidence, no silent equivalence.
"""
import json, pathlib, hashlib, datetime, collections
from nltk.corpus import wordnet as wn
BASE=pathlib.Path("master/en-master-v1.json")
master=json.loads(BASE.read_text(encoding="utf-8"))
languages={"pt-BR":"por","ja":"jpn"}
# Carefully constrained function words and most common colloquial phrases.
overrides={
 "the":("o; a","その"),"a":("um; uma","一つの"),"an":("um; uma","一つの"),
 "and":("e","と"),"or":("ou","または"),"but":("mas","しかし"),
 "to":("para","へ"),"of":("de","の"),"in":("em","中に"),"on":("sobre","上に"),
 "at":("em","で"),"for":("para","ために"),"with":("com","と一緒に"),
 "from":("de","から"),"by":("por","によって"),"as":("como","として"),
 "if":("se","もし"),"because":("porque","なぜなら"),
 "that":("aquele; que","それ; あの"),"this":("este; isto","これ"),
 "you":("você","あなた"),"we":("nós","私たち"),"they":("eles; elas","彼ら"),
 "he":("ele","彼"),"she":("ela","彼女"),"i":("eu","私"),"me":("me; mim","私を"),
 "my":("meu; minha","私の"),"your":("seu; sua","あなたの"),
 "yes":("sim","はい"),"no":("não","いいえ"),"not":("não","ない"),
 "what":("o que","何"),"who":("quem","誰"),"when":("quando","いつ"),
 "where":("onde","どこ"),"why":("por quê","なぜ"),"how":("como","どう"),
 "is":("é; está","です"),"are":("são; estão","です"),"was":("era; estava","だった"),
 "were":("eram; estavam","だった"),"am":("sou; estou","です"),
 "have":("ter","持つ"),"has":("tem","持っている"),"had":("tinha; teve","持っていた"),
 "can":("poder","できる"),"will":("vai; irá","だろう"),"would":("iria","だろう"),
 "should":("deveria","すべき"),"could":("poderia","できた"),
 "do":("fazer","する"),"does":("faz","する"),"did":("fez","した"),
 "gonna":("vou; vai","するつもり"),"wanna":("querer","したい"),
 "y'all":("vocês","みんな"),"bucks":("dólares; grana","ドル"),
 "my bad":("foi mal; erro meu","私のミス"),"no worries":("sem problema","大丈夫"),
 "what's up?":("e aí?","元気？"),"hang out":("passar tempo junto","一緒に過ごす"),
 "grab a bite":("comer alguma coisa","軽く食べる"),"brb":("já volto","すぐ戻る"),
 "idk":("não sei","わからない"),"mate":("amigo; colega","友達"),
 "loo":("banheiro","トイレ"),"quid":("libra esterlina","ポンド"),
 "cheers":("valeu; obrigado","ありがとう")
}
outdir=pathlib.Path("languages");outdir.mkdir(exist_ok=True)
freqdir=pathlib.Path("frequency");freqdir.mkdir(exist_ok=True)
catalogfile=pathlib.Path("catalog.json")
catalog=json.loads(catalogfile.read_text(encoding="utf-8"))
catalog["packages"]=[p for p in catalog["packages"] if p.get("id") not in {"ishida-pt-BR-mapped-v1","ishida-ja-mapped-v1"}]
for locale,omw in languages.items():
 entries=[]; stats=collections.Counter()
 for src in master["entries"]:
  head=src["headword"]; english_id=src.get("english_id")
  if not english_id:continue
  candidates=[]; which=None
  # Synset alignments based on the English headword: approximate first-sense only.
  for sense in src.get("senses",[])[:8]:
   syn=sense.get("sense_id","").split(":wn:")[-1]
   try: ss=wn.synset(syn)
   except Exception:continue
   lemmas=ss.lemma_names(omw)
   if lemmas:
    candidates=[x.replace("_"," ").strip() for x in lemmas if x.strip()]
    which=sense.get("sense_id")
    break
  override=overrides.get(head.lower())
  if override:
   term=override[0 if locale=="pt-BR" else 1]
   method="editorial-example";confidence="approximate"
  elif candidates:
   term=candidates[0]
   method="open-multilingual-wordnet";confidence="approximate"
  else:
   stats["unmatched"]+=1;continue
  if not term:continue
  entry={
   "id":f"{locale}:{english_id}", "english_id":english_id,
   "english_headword":head, "english_sense_id":which,
   "locale":locale, "text":term,"alternatives":candidates[1:4] if method=="open-multilingual-wordnet" else [],
   "category":src.get("category"),"kind":src.get("kind"),
   "cefr_english_estimate":src.get("cefr"),
   "english_description":src.get("description_short_english") or src.get("short_description_en"),
   "source":method,"mapping_status":"approximate-unreviewed",
   "confidence":confidence,
   "regional_note":"Portuguese Open Multilingual WordNet is not specifically Brazilian" if locale=="pt-BR" and method!="editorial-example" else None,
   "english_slang_regions":src.get("regions",[]) if src.get("category")=="regional-colloquial" else [],
  }
  entries.append(entry);stats[method]+=1
 file=outdir/(locale+".json")
 payload={"schema_version":1,"id":f"ishida-{locale}-mapped-v1","language":locale,"kind":"english-id-mapped-vocabulary","english_master":"ishida-en-master-v1","version":"2026-10-26.1","status":"approximate-unreviewed","entries":entries,"stats":dict(stats),"notes":["All IDs refer to English entries; where a source word has multiple senses, the chosen synset is included.","An English-ID association is not a certified exact translation.","A language is studyable with another only if both have entries for the same English ID and compatible senses.","Regional slang labels from English do NOT describe usage of the translation.","This is a provisional functional dataset."]}
 file.write_text(json.dumps(payload,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
 catalog["packages"].append({"id":payload["id"],"name":f"Ishida {locale} mapped vocabulary (approximate)","kind":payload["kind"],"version":payload["version"],"language":locale,"languages":["en",locale],"entries":len(entries),"status":"approximate-unreviewed","verified_for_production":False,"url":f"https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/languages/{locale}.json","sha256":hashlib.sha256(file.read_bytes()).hexdigest(),"compatibility_note":"Requires English-ID mapping adapter; NOT the legacy card import schema."})
 print(locale,len(entries),dict(stats))
catalogfile.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
