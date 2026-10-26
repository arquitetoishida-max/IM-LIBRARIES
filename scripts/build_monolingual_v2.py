#!/usr/bin/env python3
"""Produce the only supported Ishida V2 discovery catalog.
All downloadable items are monolingual packages, including region packs.
Legacy packs stay on disk but are NEVER advertised in catalog-v2.json.
"""
import json, pathlib, hashlib, datetime
R=pathlib.Path(".");O=R/"v2";O.mkdir(exist_ok=True)
EN=json.loads((R/"master/en-master-v1.json").read_text(encoding="utf-8"))
def save(pid,name,lang,rows,region=None):
 path=O/(pid+".json")
 # shared english reference is cross-language foreign key, not identity for a local form.
 payload={"schema_version":2,"package_id":pid,"package_type":"ishida-monolingual",
          "language":lang,"region":region,"name":name,"version":"1.0.0",
          "english_explanations":True,"status":"approximate-functional",
          "entries":rows}
 path.write_text(json.dumps(payload,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
 catalog.append({"id":pid,"name":name,"language":lang,"region":region,
  "kind":"ishida-monolingual","schema_version":2,"available":True,
  "entry_count":len(rows),"url":f"https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/v2/{pid}.json",
  "sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"version":"1.0.0"})
catalog=[]
enrows=[]
for e in EN["entries"]:
 desc=e.get("description_short_english") or e.get("short_description_en")
 if not desc:continue
 enrows.append({"id":e["english_id"],"english_id":e["english_id"],"text":e["headword"],"kind":"expression" if e.get("category")=="regional-colloquial" else "word",
 "description_en":desc,"level":e.get("cefr"),"region_tags":e.get("regions",[]),
 "regional_senses":e.get("regional_senses",[]),"source_status":e.get("mapping_status","editorial")})
save("en-core-v2","English — core and expressions","en",enrows)
for locale in ("pt-BR","ja"):
 src=json.loads((R/"languages"/(locale+".json")).read_text(encoding="utf-8"))
 rows=[]
 for e in src["entries"]:
  if not e.get("english_id") or not e.get("text") or not e.get("english_description"):continue
  rows.append({"id":e["id"],"english_id":e["english_id"],"english_sense_id":e.get("english_sense_id"),
   "text":e["text"],"kind":e.get("kind") or "word","description_en":e["english_description"],
   "level":e.get("cefr_english_estimate"),"alternatives":e.get("alternatives",[]),
   "source_status":e.get("mapping_status"),"translation_confidence":e.get("confidence")})
 save(locale+"-core-v2",{"pt-BR":"Português brasileiro — vocabulário","ja":"日本語 — 語彙"}[locale],locale,rows)
# A region-only library is an independent selectable package, not an independent language.
# Only attested English regions present in source data. No unsupported Brazilian slang invented.
regions={
 "en-US-NY":("New York — slang and expressions",["US-NY"]),
 "en-US-CA":("California — slang and expressions",["US-CA"]),
 "en-US-TX":("Texas — slang and expressions",["US-TX"]),
 "en-GB":("United Kingdom — slang and expressions",["GB"])}
for tag,(name,codes) in regions.items():
 rows=[]
 for e in enrows:
  if e["kind"]=="expression" and any(c in e.get("region_tags",[]) for c in codes):
   rows.append(dict(e,region_tags=codes))
  for sense in e.get("regional_senses",[]):
   if any(c in sense.get("regions",[]) for c in codes):
    rows.append({"id":e["id"]+":regional:"+str(len(rows)),"english_id":e["english_id"],
      "text":e["text"],"kind":"expression","description_en":sense["definition_en"],
      "region_tags":sense["regions"],"source_status":"regional-provisional"})
 if rows:save(tag+"-slang-v2",name,"en",rows,tag)
manifest={"schema_version":2,"format":"ishida-monolingual-only","version":"1.0.0",
 "discovery_rule":"available == true and kind == ishida-monolingual and schema_version == 2",
 "packages":catalog,
 "notes":["Only these downloadable monolingual packages are supported.",
 "Expressional descriptions in English may be translated on demand to native language.",
 "Word cards require the same english_id in both installed language sets AND compatible meaning; unknown sense may be approximate.",
 "Regional packs are content packs for an existing language, not new language codes.",
 "Portuguese and Japanese are approximate lexical drafts."]}
(O/"catalog.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"packages":len(catalog),"counts":{x["id"]:x["entry_count"] for x in catalog}},ensure_ascii=False))
