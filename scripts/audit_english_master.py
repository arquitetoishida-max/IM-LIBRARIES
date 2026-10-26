#!/usr/bin/env python3
"""Complete deterministic audit of every English-master record.
This is an automated editorial check, NOT 3091 manual linguistic reviews.
"""
import json, pathlib, collections, re
p=pathlib.Path('master/en-master-v1.json')
d=json.loads(p.read_text(encoding='utf-8'))
entries=d['entries']
issues=collections.defaultdict(list)
ids=set();lex=set();heads=collections.defaultdict(list)
for n,e in enumerate(entries,1):
 id=e.get('english_id'); lid=e.get('lexeme_id'); head=e.get('headword')
 if not id:issues['missing_english_id'].append((n,head))
 elif id in ids:issues['duplicate_english_id'].append((n,head,id))
 ids.add(id)
 if not lid:issues['missing_lexeme_id'].append((n,head))
 elif lid in lex:issues['duplicate_lexeme_id'].append((n,head,lid))
 lex.add(lid)
 if not head or not isinstance(head,str):issues['invalid_headword'].append((n,head))
 else:heads[head.casefold()].append(id)
 defs=e.get('definitions_en') or []
 short=e.get('description_short_english')
 if not short:issues['missing_short_definition'].append((n,head))
 elif len(short.split())>12:issues['short_definition_over_12_words'].append((n,head))
 if not defs:issues['missing_definitions'].append((n,head))
 if e.get('category')=='common':
  if not e.get('senses') and e.get('definition_status')!='editorial-grammar-gloss':issues['no_wordnet_senses'].append((n,head))
  if e.get('cefr') not in {'A1','A2','B1','B2','C1','C2'}:issues['missing_cefr'].append((n,head))
 elif e.get('category')=='regional-colloquial':
  if not e.get('regions'):issues['slang_missing_regions'].append((n,head))
  if not e.get('english_gloss'):issues['slang_missing_gloss'].append((n,head))
 else:issues['unexpected_category'].append((n,head))
for head,items in heads.items():
 if len(items)>1:issues['duplicate_surface_form'].append((head,items))
counts=collections.Counter(e.get('category') for e in entries)
tiers=collections.Counter(e.get('cefr') for e in entries if e.get('category')=='common')
status='PASS' if not any(issues.values()) else 'REQUIRES_EDITORIAL_REVIEW'
out={'status':status,'audit_type':'automatic_record_by_record_not_manual','entry_count':len(entries),'category_counts':dict(counts),'cefr_counts':dict(tiers),'issues':{k:{'count':len(v),'examples':v[:30]} for k,v in sorted(issues.items())},'note':'WordNet first senses and regional labels were not individually verified; no assertion of human review.'}
path=pathlib.Path('docs/ENGLISH_QA_REPORT.json');path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'entry_count':len(entries),'issues':{k:len(v) for k,v in issues.items()}},ensure_ascii=False))
