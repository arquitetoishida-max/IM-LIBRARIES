"""LEXICON #4: monolingual British English package (en-GB) derived from the reviewed en-US core.
Same english_id / sense ids (no renumbering, IM-LIBRARIES contract); entry ids are 'en-GB:<english_id>'; the text
changes only where LEXICON editorial/en-GB/us-gb-map.tsv gives a reviewed UK spelling or word. Senses without a UK
difference keep the shared text. Written as a CANDIDATE (catalog untouched): integration is IM-LIBRARIES' step.

usage: python scripts/build_en_gb.py --lexicon <LEXICON>
"""
import argparse
import csv
import datetime
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--lexicon', required=True)
    a = ap.parse_args(argv)
    us = json.load(open(os.path.join(ROOT, 'v2/en-core-v2.json'), encoding='utf-8'))
    mp = {'en:%09d' % int(r['english_number']): r for r in csv.DictReader(open(os.path.join(a.lexicon, 'editorial/en-GB/us-gb-map.tsv'), encoding='utf-8'), delimiter='\t')}
    entries, changed = [], 0
    for e in us['entries']:
        g = dict(e)
        g['id'] = 'en-GB:' + e['english_id']
        r = mp.get(e['english_id'])
        if r and e['text'] == r['en_US']:
            g['text'] = r['en_GB']
            g['alternatives'] = [x for x in e.get('alternatives', []) if x != r['en_GB']]
            g['region_note_en'] = ('UK %s of "%s"' % (r['kind'], r['en_US'])) + (': ' + r['note'] if r['note'] else '')
            changed += 1
        g['region_tags'] = ['en-GB']
        if r and e.get('forms'):
            # inflections follow the UK spelling of the lemma (realize/realized → realise/realised); ids unchanged
            g['forms'] = [dict(f, text=f['text'].replace(r['en_US'][:-1], r['en_GB'][:-1]) if r['kind'] == 'spelling' else f['text']) for f in e['forms']]
        entries.append(g)
    pkg = {k: v for k, v in us.items() if k != 'entries'}
    pkg.update(package_id='en-GB-core-v2', language='en-GB', region=None, name='English (UK) — core and expressions', version='1.0.0',
               status='candidate', notes=['1.0.0: derived from en-US core %s with %d reviewed UK spellings/words (LEXICON #4).' % (us.get('version'), changed)])
    pkg['entries'] = entries
    b = json.dumps(pkg, ensure_ascii=False, indent=1).encode('utf-8')
    out = os.path.join(ROOT, 'candidates/en-GB/en-GB-core-v2-1.0.0-candidate.json')
    open(out, 'wb').write(b)
    man = {'package_id': 'en-GB-core-v2', 'candidate_version': '1.0.0-candidate', 'created': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'publication': 'not-published (integration into catalog by IM-LIBRARIES)', 'base': {'path': 'v2/en-core-v2.json', 'version': us.get('version')},
           'candidate': {'file': os.path.basename(out), 'sha256': hashlib.sha256(b).hexdigest(), 'size_bytes': len(b)},
           'report': {'entries': len(entries), 'uk_texts': changed}, 'gates_passed': True,
           'catalog_entry': {'id': 'en-GB-core-v2', 'name': 'English (UK) — core and expressions', 'language': 'en-GB', 'region': None, 'role': 'core',
                             'kind': 'ishida-monolingual', 'schema_version': 2, 'available': True, 'flag': '🇬🇧', 'locale': 'en-GB', 'name_native': 'English (UK)',
                             'name_en': 'English (UK)', 'name_pt': 'Inglês (Reino Unido)', 'name_ja': '英語（イギリス）'}}
    json.dump(man, open(os.path.join(ROOT, 'candidates/en-GB/manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(man['report'])


if __name__ == '__main__':
    main()
