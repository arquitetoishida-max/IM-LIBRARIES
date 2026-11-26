"""Grava o campo `articles` ("o,os", "a,as", "os,os", "as,as", "o/a,os/as") nos substantivos de v2/pt-BR-core-v2.json.

Decisão do proprietário (25/11/2026, LEXICON #90): uma coluna só, artigo do singular e do plural separados por vírgula;
só o português por enquanto. Regras + listas de exceção revisadas em novrev/pt_articles.py; a revisão está em
novrev/articles_pt-BR.tsv. Idempotente: pode rodar de novo depois de qualquer integração (IDs novos recebem o campo pelas
mesmas regras; os que caem fora das regras ficam sem o campo e são listados para revisão). Nomes próprios, números e
itens que não são substantivo comum ficam sem o campo (desconhecido ≠ chute).

Uso: python novrev/apply_articles.py [--check]
"""
import json, sys
sys.path.insert(0, 'novrev')
from pt_articles import articles_for

PATH = 'v2/pt-BR-core-v2.json'
pk = json.load(open(PATH, encoding='utf-8'))
review, changed, total = [], 0, 0
for e in pk['entries']:
    if e.get('part_of_speech') != 'n':
        if 'articles' in e:
            del e['articles']; changed += 1
        continue
    a = articles_for(e)
    if a == 'REVIEW':
        review.append(e['english_id'] + ' ' + e['text']); a = None
    if a:
        total += 1
        if e.get('articles') != a:
            e['articles'] = a; changed += 1
    elif 'articles' in e:
        del e['articles']; changed += 1
print(f'substantivos com artigos: {total}; alterados: {changed}; para revisar: {len(review)}')
for r in review: print('  REVIEW', r)
if '--check' in sys.argv:
    sys.exit(1 if changed or review else 0)
json.dump(pk, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # mesmo formato do arquivo publicado
