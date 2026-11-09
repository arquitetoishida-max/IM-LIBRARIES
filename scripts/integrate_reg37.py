"""MULTILANG #37 / LEXICON REG37: part_of_speech for the BASE4 new entries in the four cores and coherent Japanese
plain/polite forms: new verbs/adjectives get forms; entries whose JA text was corrected in 2.2.0 get forms of the new
text (stale forms/constructions of the old text are removed); the copula です loses invalid progressive constructions.
Only these fields change; ids, texts, statuses and order are untouched.  Packages → 2.2.1.

usage: python scripts/integrate_reg37.py --lexicon <LEXICON> --units <japanese_units full output json>
"""
import argparse
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
VERSION = '2.2.1'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--lexicon', required=True)
    ap.add_argument('--units', required=True)
    a = ap.parse_args(argv)
    units = json.load(open(a.units, encoding='utf-8'))
    uf = {e['id']: e for e in units['entries']}
    cat_path = os.path.join(ROOT, 'v2/catalog.json')
    cat = json.load(open(cat_path, encoding='utf-8'))
    rep = {}
    for l in ('en', 'pt-BR', 'ja', 'zh'):
        path = os.path.join(ROOT, 'v2/%s-core-v2.json' % l)
        pk = json.load(open(path, encoding='utf-8'))
        delta = json.load(open(os.path.join(a.lexicon, 'editorial/candidates/%s-REG37.delta.json' % l), encoding='utf-8'))
        by = {e['id']: e for e in pk['entries']}
        n = 0
        for d in delta['entries']:
            e = by.get(d['id'])
            if e is not None and e.get('part_of_speech') is None:
                e['part_of_speech'] = d['part_of_speech']
                n += 1
        r = {'pos': n}
        if l == 'ja':
            prev = {e['id']: e for e in json.load(open(os.path.join(ROOT, 'candidates/ja/ja-core-v2-2.2.0-candidate.JA-001.R137.JA-UNITS.HINTS.json'), encoding='utf-8'))['entries']}
            changed = {i for i, e in by.items() if i in prev and prev[i]['text'] != e['text']}
            renew = changed | {d['id'] for d in delta['entries']}
            copula = {i for i, e in by.items() if e['text'] in ('です', 'だ')}
            # the copula is not a godan verb: its register pairs are だ/です (form ids kept, texts corrected)
            COP = {'NP.PLAIN.POS': ('だ', 'da'), 'NP.POLITE.POS': ('です', 'desu'), 'NP.PLAIN.NEG': ('じゃない', 'ja nai'),
                   'NP.POLITE.NEG': ('じゃありません', 'ja arimasen'), 'PAST.PLAIN.POS': ('だった', 'datta'), 'PAST.POLITE.POS': ('でした', 'deshita'),
                   'PAST.PLAIN.NEG': ('じゃなかった', 'ja nakatta'), 'PAST.POLITE.NEG': ('じゃありませんでした', 'ja arimasen deshita'), 'TE': ('で', 'de')}
            for i in copula:
                e = by[i]
                if not e.get('forms'):
                    continue
                have = {f['grammatical_key']: f for f in e['forms']}
                for key, (t, rom) in COP.items():
                    f = have.get(key) or {'form_id': '%s:f:%s' % (i, key), 'lemma_id': i, 'grammatical_key': key, 'study_tier': 'essential'}
                    f.update(text=t, reading=t, romanization=rom, verb_class='copula')
                    have[key] = f
                e['forms'] = [have[k] for k in COP]
                e['part_of_speech'] = 'copula'
                r['copula_fixed'] = r.get('copula_fixed', 0) + 1
            # a JA word that is exactly an inflected form of a JA lemma (EN form ids such as said → 言った) becomes a
            # kind=form of that lemma (same id and grades), so the hourglass and the register tabs work (#37)
            form_text = {}
            for x in by.values():
                if x.get('kind') == 'word' and not x.get('core_status'):
                    for f in x.get('forms', []):
                        form_text.setdefault(f['text'], (x['id'], f['grammatical_key']))
            retyped = 0
            for x in by.values():
                if x.get('kind') == 'word' and x.get('part_of_speech') == 'v' and not x.get('forms') and x['text'] in form_text:
                    lemma, key = form_text[x['text']]
                    if lemma != x['id']:
                        x.update(kind='form', lemma_id=lemma, grammatical_key=key, lexical_type='form', key_pending=False)
                        retyped += 1
            r['retyped_as_form'] = retyped
            for i in renew:
                e = by.get(i)
                if e is None or e.get('core_status'):
                    continue
                f = (uf.get(i) or {}).get('forms') or []
                if f or e.get('forms'):
                    e['forms'] = f
                    if not f:
                        e.pop('forms')
            before = len(pk['constructions'])
            pk['constructions'] = [c for c in pk['constructions'] if c['lemma_id'] not in renew and not (c['lemma_id'] in copula and c['grammatical_key'].startswith('PROG'))]
            removed = before - len(pk['constructions'])
            add = [c for c in units['constructions'] if c['lemma_id'] in renew and c['lemma_id'] not in copula and not by[c['lemma_id']].get('core_status')]
            pk['constructions'] += add
            r.update(text_changed=len(changed), forms_renewed=sum(1 for i in renew if by.get(i, {}).get('forms')), constructions_removed=removed, constructions_added=len(add))
        pk['version'] = VERSION
        pk.setdefault('notes', []).append('2.2.1: REG37 — part_of_speech for BASE4 entries; JA plain/polite forms for new and corrected entries; invalid copula progressives removed (MULTILANG #37).')
        b = json.dumps(pk, ensure_ascii=False, indent=1).encode('utf-8')
        open(path, 'wb').write(b)
        for c in cat['packages']:
            if c['id'] == '%s-core-v2' % l:
                c.update(sha256=hashlib.sha256(b).hexdigest(), size_bytes=len(b), version=VERSION, entry_count=len(pk['entries']))
        rep[l] = r
    cat['version'] = '1.2.1'
    cat['notes'].append('1.2.1: core 2.2.1 — REG37 part-of-speech and Japanese register forms (MULTILANG #37).')
    open(cat_path, 'w', encoding='utf-8').write(json.dumps(cat, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(rep, ensure_ascii=False))


if __name__ == '__main__':
    main()
