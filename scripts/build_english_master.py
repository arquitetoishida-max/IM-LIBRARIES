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
 # WordNet covers content words; frequent grammatical words need curated glosses.
 function_words={
 "the":"Definite article referring to a particular person or thing.",
 "a":"Indefinite article introducing a nonspecific person or thing.",
 "an":"Indefinite article used before a vowel sound.",
 "and":"Connects words, phrases or clauses.",
 "or":"Introduces an alternative or choice.",
 "but":"Introduces contrast or an exception.",
 "to":"Marks an infinitive or indicates direction.",
 "of":"Expresses a relationship, origin or belonging.",
 "in":"Inside something or within a period.",
 "on":"Touching or supported by a surface.",
 "at":"Specifies a place, time or point.",
 "for":"Indicates purpose, benefit or duration.",
 "with":"Indicates accompaniment, possession or means.",
 "from":"Indicates an origin or starting point.",
 "by":"Identifies an agent, means or proximity.",
 "as":"Indicates a role, comparison or manner.",
 "if":"Introduces a condition.",
 "because":"Introduces a reason or cause.",
 "that":"Introduces a clause or identifies something.",
 "this":"Points to something near or currently discussed.",
 "these":"Plural form of this.",
 "those":"Plural form of that.",
 "it":"Refers to something already mentioned.",
 "its":"Possessive form of it.",
 "you":"Refers to the person or people addressed.",
 "your":"Belonging to the person addressed.",
 "we":"Refers to the speaker and others.",
 "our":"Belonging to the speaker and others.",
 "they":"Refers to people or things mentioned.",
 "their":"Belonging to them.",
 "he":"Refers to a male person or animal.",
 "she":"Refers to a female person or animal.",
 "i":"The person speaking or writing.",
 "me":"The speaker as an object.",
 "my":"Belonging to the speaker.",
 "who":"Asks about or identifies a person.",
 "what":"Asks about an identity, thing or action.",
 "when":"Asks about or indicates time.",
 "where":"Asks about or indicates place.",
 "why":"Asks about or indicates a reason.",
 "how":"Asks about or indicates manner or extent.",
 "not":"Expresses negation.",
 "no":"Expresses refusal or absence.",
 "yes":"Expresses agreement or affirmation.",
 "can":"Expresses ability or possibility.",
 "will":"Expresses future intention or prediction.",
 "would":"Expresses conditional or hypothetical meaning.",
 "should":"Expresses advice, expectation or obligation.",
 "could":"Expresses possibility or past ability.",
 "may":"Expresses permission or possibility.",
 "might":"Expresses uncertain possibility.",
 "do":"Performs an action; also forms questions.",
 "does":"Third-person singular present form of do.",
 "did":"Past tense of do.",
 "is":"Third-person singular present form of be.",
 "am":"First-person singular present form of be.",
 "are":"Present plural or second-person form of be.",
 "was":"Past singular form of be.",
 "were":"Past plural or second-person form of be.",
 "been":"Past participle form of be.",
 "have":"Possess; also forms perfect verb tenses.",
 "has":"Third-person singular present form of have.",
 "had":"Past tense or past participle of have.",
 "than":"Introduces the second term of a comparison.",
 "then":"Indicates what happens next or afterward.",
 "also":"Adds information or another item.",
 "very":"Intensifies an adjective or adverb.",
 "too":"Means excessively or in addition.",
 "so":"Indicates degree, consequence or emphasis.",
 "up":"Toward a higher position.",
 "down":"Toward a lower position."
 }
 # Compact editorial definitions for common grammatical contractions.
 function_words.update({
 "his":"Belonging to a male person or animal.",
 "her":"Belonging to or referring to a female person.",
 "him":"Refers to a male person as an object.",
 "them":"Refers to people or things as objects.",
 "which":"Identifies or asks about one among alternatives.",
 "into":"Moving toward the inside of something.",
 "something":"A thing not specifically named.",
 "anything":"Any thing, regardless of which.",
 "everything":"All things in a particular group.",
 "everyone":"Every person.",
 "others":"Other people or things.",
 "since":"From a past time or because.",
 "during":"Throughout part or all of a period.",
 "without":"Not having or using something.",
 "against":"Opposing or touching something.",
 "until":"Up to a specified time.",
 "per":"For each; according to.",
 "whose":"Belonging to which person.",
 "whose":"Asks or states to whom something belongs.",
 "anyone":"Any person.",
 "someone":"An unspecified person.",
 "nobody":"No person.",
 "somewhere":"An unspecified place.",
 "anywhere":"Any place.",
 "everywhere":"In all places.",
 "therefore":"For that reason; consequently.",
 "however":"Introduces contrast or qualification.",
 "although":"Introduces a contrasting statement.",
 "unless":"Except when a condition holds.",
 "whether":"Introduces alternatives or uncertainty.",
 "within":"Inside a place, range or time limit.",
 "between":"In the space separating two things.",
 "among":"In or within a group.",
 "through":"From one side to another.",
 "throughout":"In every part or during the whole period.",
 "onto":"Moving to a position on a surface.",
 "upon":"On; often more formal.",
 "either":"One of two alternatives.",
 "neither":"Not one nor the other.",
 "both":"The two people or things together.",
 "each":"Every individual member of a group.",
 "every":"All members considered individually.",
 "several":"More than two but not many.",
 "many":"A large number of.",
 "much":"A large quantity or degree.",
 "few":"A small number.",
 "less":"A smaller amount.",
 "fewer":"A smaller number.",
 "enough":"As much or as many as needed.",
 "another":"One more or a different one.",
 "else":"Other than what was mentioned.",
 "yet":"Up to now or nevertheless.",
 "already":"Before now or earlier than expected.",
 "still":"Continuing up to the present.",
 "almost":"Very nearly, but not completely.",
 "perhaps":"Possibly; maybe.",
 "maybe":"Possibly, without certainty.",
 "rather":"To a degree or instead.",
 "quite":"To a considerable or complete degree.",
 "okay":"Used to express agreement or acceptability.",
 "ok":"Informal spelling of okay.",
 })
 contractions={
 "it's":"It is, or it has.",
 "don't":"Do not.",
 "i'm":"I am.",
 "you're":"You are.",
 "that's":"That is, or that has.",
 "can't":"Cannot.",
 "i've":"I have.",
 "didn't":"Did not.",
 "he's":"He is, or he has.",
 "there's":"There is, or there has.",
 "doesn't":"Does not.",
 "they're":"They are.",
 "i'll":"I will, or I shall.",
 "we're":"We are.",
 "we've":"We have.",
 "we'll":"We will.",
 "she's":"She is, or she has.",
 "isn't":"Is not.",
 "aren't":"Are not.",
 "wasn't":"Was not.",
 "weren't":"Were not.",
 "won't":"Will not.",
 "wouldn't":"Would not.",
 "shouldn't":"Should not.",
 "couldn't":"Could not.",
 "haven't":"Have not.",
 "hasn't":"Has not.",
 "hadn't":"Had not.",
 "let's":"Let us.",
 "what's":"What is, or what has.",
 "who's":"Who is, or who has.",
 "where's":"Where is, or where has.",
 "how's":"How is, or how has.",
 "they've":"They have.",
 "they'll":"They will.",
 "you've":"You have.",
 "you'll":"You will.",
 "i'd":"I would, or I had.",
 "you'd":"You would, or you had.",
 "we'd":"We would, or we had.",
 "he'd":"He would, or he had.",
 "she'd":"She would, or she had.",
 "they'd":"They would, or they had.",
 "could've":"Could have.",
 "should've":"Should have.",
 "would've":"Would have.",
 }
 function_words.update(contractions)
  function_words.update({
 "myself":"The speaker, used reflexively or for emphasis.","yourself":"The person addressed, used reflexively or emphatically.",
 "himself":"A male person, used reflexively or emphatically.","herself":"A female person, used reflexively or emphatically.",
 "itself":"The same thing or animal, reflexively.","themselves":"The same people or things, reflexively.",
 "ourselves":"The speaker and others, used reflexively.","yourselves":"More than one person addressed, reflexively.",
 "hey":"Informal greeting or call for attention.","cannot":"Am not able to; can not.",
 "towards":"In the direction of.","etc":"And other similar things.",
 "shall":"Used for future intentions, offers or obligations.","via":"By way of or through.",
 "whom":"Refers to a person as grammatical object.","everybody":"Every person.",
 "somebody":"An unspecified person.","nobody":"Not any person.",
 "here's":"Here is; used when presenting something.","there're":"There are.",
 "gonna":"Informal spoken form of going to.","wanna":"Informal spoken form of want to.",
 "gotta":"Informal form meaning have got to.","kinda":"Informal spoken form of kind of.",
 "sorta":"Informal spoken form of sort of.","lemme":"Informal spoken form of let me.",
 "gimme":"Informal spoken form of give me.","dunno":"Informal way to say don't know.",
 "ain't":"Nonstandard form of is not, are not or have not.",
 "lol":"Online abbreviation meaning laughing out loud.","omg":"Online abbreviation expressing surprise.",
 "brb":"Online abbreviation meaning be right back.","idk":"Online abbreviation meaning I don't know.",
 "app":"An application, especially software on a device.",
 "dr":"Abbreviation for doctor; context may determine other meanings.",
 "st":"Abbreviation for street or saint; context dependent.",
 "pre":"Prefix meaning before, often used independently in informal text.",
 "mr":"Title used before a man's surname.",
 "mrs":"Title traditionally used before a married woman's surname.",
 "ms":"Title used before a woman's surname without marital specification.",
 "vs":"Abbreviation of versus, indicating opposition or comparison.",
 "tv":"Television.","uk":"Abbreviation for the United Kingdom.",
 "usa":"Abbreviation for the United States of America.",
 "online":"Connected to or available through the internet.",
 "email":"Messages sent electronically over computer networks.",
 "website":"A collection of related web pages.",
 "google":"Name of a technology company and search engine.",
 "facebook":"Name of an online social networking platform.",
 "youtube":"Online platform for sharing and watching videos.",
 "instagram":"Online photo and video sharing service.",
 "twitter":"Name formerly used by a social networking platform.",
 "william":"A masculine given name.","richard":"A masculine given name.",
 "chris":"A given name, often short for Christopher or Christine.",
 "obama":"A surname associated with former US president Barack Obama.",
 "san":"Spanish element meaning saint in many place names.",
 "los":"Spanish element meaning the, common in some place names.",
 "de":"Preposition in several languages, often appearing in names.",
 "la":"Article or syllable occurring in names and expressions.",
 "etc.":"Abbreviation meaning and so forth.",
 })
 if not synsets and w in function_words:
  e["short_description_en"]=function_words[w]
  e["definitions_en"]=[function_words[w]]
  e["definition_status"]="editorial-grammar-gloss"
 if not e["short_description_en"]:
  e["short_description_en"]=None
 e["short_description_status"]="provided" if e["short_description_en"] else "needs-review"
 e["description_short_english"]=(" ".join(e["short_description_en"].split()[:12]) if e["short_description_en"] else None)
 # CEFR tier here is a clearly marked starting estimate from rank, NOT an official CEFR list.
 e["cefr"]=("A1" if idx<=500 else "A2" if idx<=1100 else "B1" if idx<=1800 else "B2" if idx<=2400 else "C1" if idx<=2850 else "C2")
 e["cefr_status"]="approximate-learning-band-by-frequency"
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
 # If the standard dictionary already contains the identical spelling, attach the
 # regional/colloquial sense to that lexeme instead of duplicating the headword.
 if phrase.casefold() in existing:
  standard=existing[phrase.casefold()]
  alt={"kind":"regional-colloquial-sense","gloss_en":gloss,"definition_en":definition,"regions":regions,"region_note":where,"status":"needs-review"}
  variants=standard.setdefault("regional_senses",[])
  if not any(v.get("gloss_en")==gloss for v in variants):variants.append(alt)
  continue
 out.append(prev or {"concept_id":new_id(),"lexeme_id":f"iml:en:slang:{i:06d}","slug":key,"headword":phrase,"category":"regional-colloquial","kind":"expression" if " " in phrase or "'" in phrase else "word","language":"en","definitions_en":[definition],"english_gloss":gloss,"register":"slang-or-informal","regions":regions,"regional_note":where,"cefr":None,"cefr_status":"unclassified","frequency":None,"mapping_status":"provisional-not-sense-verified","related_english_form":gloss,"source_review":"requires regional evidence review"})
for e in out:
 if e.get("category")=="regional-colloquial":
  e["english_id"]=e.get("english_id",f"en:{e['concept_id'].split(':')[-1]}")
  e["short_description_en"]=e["definitions_en"][0] if e.get("definitions_en") else None
  e["description_short_english"]=" ".join(e["short_description_en"].split()[:12]) if e.get("short_description_en") else None
  e["cefr_status"]="not-applicable-regional-expression"
  e["frequency_reference"]="frequency/en.json"
out.sort(key=lambda e:(0 if e.get("category")=="common" else 1,rank_lookup.get(e.get("headword"),100000),e.get("headword","")))
FREQ_PATH.write_text(json.dumps({"schema_version":1,"language":"en","source":"wordfreq","frequency_scope":"mixed","independent_of_id":True,"entries":frequency_entries},ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
# immutable IDs, top-level ordering can change by rank
result={"schema_version":1,"id":"ishida-en-master-v1","created_at":old.get("created_at",datetime.date.today().isoformat()),"version":datetime.date.today().isoformat(),"language":"en","pivot":"English first, but concepts may exist without English","status":"draft-unreviewed","counts":{"common":sum(e.get("category")=="common" for e in out),"slang":sum(e.get("category")=="regional-colloquial" for e in out)},"warnings":["English monolingual dictionary, not bilingual translations.","WordNet senses identify English meanings; cross-language translation mapping is NOT done.","CEFR is an approximate learning tier based on word frequency, not an exam-certified word list.","Regional slang tags are provisional and require source review."],"entries":out}
PATH.write_text(json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
catpath=pathlib.Path("catalog.json")
cat=json.loads(catpath.read_text(encoding="utf-8"))
pkgs=[p for p in cat["packages"] if p.get("id") not in ("ishida-en-master-v1","ishida-en-frequency-v1")]
pkgs.append({"id":"ishida-en-master-v1","version":result["version"],"name":"Ishida English Master — 3000 common + regional expressions (DRAFT)","kind":"lexical-master","language":"en","languages":["en"],"entries":len(out),"status":"usable-monolingual-draft","verified_for_production":False,"url":"https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/master/en-master-v1.json","sha256":hashlib.sha256(PATH.read_bytes()).hexdigest(),"description":"Monolingual English entries with attested WordNet senses, provisional CEFR estimates and slang tags; NOT cross-language mappings."})
pkgs.append({"id":"ishida-en-frequency-v1","version":result["version"],"name":"English frequency rankings","kind":"frequency","language":"en","languages":["en"],"entries":len(frequency_entries),"status":"source-ranked","verified_for_production":False,"url":"https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/frequency/en.json","sha256":hashlib.sha256(FREQ_PATH.read_bytes()).hexdigest()})
cat["packages"]=pkgs
catpath.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Built",len(out),"entries (",result["counts"],")")
