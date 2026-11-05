"""Builds a CANDIDATE monolingual package (IM-LIBRARIES #2) from the active package plus a reviewed LEXICON delta.

Never touches v2/catalog.json nor the active v2/<lang>-core-v2.json: the candidate goes to
candidates/<lang>/<package>-<version>.json with a manifest (hashes, base for rollback, gate results).
Promotion to the catalog is a separate step that needs the owner's explicit authorization.

Delta format (produced by LEXICON review rounds, contract v1 / docs/UNIDADES_FORMATO_v1.md):
  {"language": "ja", "round_id": "JA-001", "entries": [patched or approved-new entries],
   "constructions": [...], "grammar_units": [...], "unit_aliases": {...}}
Entry rules: existing ids keep english_id and kind (identity gate); a patched entry replaces only the fields it
carries; new entries need "approved_new": true; nothing is ever deleted (retired entries stay, flagged).

usage: python scripts/build_candidate.py --lang ja --delta <delta.json> --lexicon <LEXICON checkout> [--out candidates]
"""
import argparse
import datetime
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENTITY = ('english_id', 'kind')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def merge(base, delta):
    """Returns (candidate dict, gate errors, report)."""
    errors = []
    entries = [dict(e) for e in base['entries']]
    by_id = {e['id']: e for e in entries}
    patched = added = 0
    for d in delta.get('entries', []):
        eid = d.get('id')
        if eid in by_id:
            cur = by_id[eid]
            for k in IDENTITY:
                # reclassifying an inflection as a form of an existing lemma keeps the id (and the grades)
                if k == 'kind' and d.get(k) == 'form' and d.get('lemma_id') in by_id and d.get('lemma_id') != eid:
                    continue
                if k in d and d[k] != cur.get(k):
                    errors.append('%s: %s changed (%r → %r); use a new id + alias' % (eid, k, cur.get(k), d[k]))
            cur.update({k: v for k, v in d.items() if k not in ('approved_new',)})
            patched += 1
        elif d.get('approved_new'):
            e = {k: v for k, v in d.items() if k != 'approved_new'}
            entries.append(e)
            by_id[eid] = e
            added += 1
        else:
            errors.append('%s: new entry without approved_new' % eid)
    cand = {k: v for k, v in base.items() if k != 'entries'}
    cand['entries'] = entries
    for k in ('constructions', 'grammar_units'):
        if delta.get(k):
            cand[k] = list(base.get(k, [])) + list(delta[k])
    if delta.get('unit_aliases'):
        cand['unit_aliases'] = dict(base.get('unit_aliases', {}), **delta['unit_aliases'])
    cand['grammatical_keys_version'] = 1
    missing = [e['id'] for e in base['entries'] if e['id'] not in by_id]
    if missing:
        errors.append('ids lost: %s' % missing[:10])
    report = {'base_entries': len(base['entries']), 'candidate_entries': len(entries), 'patched': patched, 'added': added}
    return cand, errors, report


def bump(version, round_id):
    parts = (version or '0.0.0').split('-')[0].split('.')
    while len(parts) < 3:
        parts.append('0')
    return '%s.%d.0-candidate.%s' % (parts[0], int(parts[1]) + 1, round_id or 'x')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--lang', required=True)
    ap.add_argument('--delta', required=True, action='append', help='repeatable: applied in order')
    ap.add_argument('--lexicon', required=True, help='LEXICON checkout (unit validators)')
    ap.add_argument('--base', help='active package (default v2/<lang>-core-v2.json)')
    ap.add_argument('--out', default=os.path.join(ROOT, 'candidates'))
    a = ap.parse_args(argv)
    sys.path.insert(0, a.lexicon)
    from ile.units import validate  # LEXICON contract v1 validators

    base_path = a.base or os.path.join(ROOT, 'v2', '%s-core-v2.json' % a.lang)
    raw = open(base_path, 'rb').read()
    base = json.loads(raw.decode('utf-8'))
    cand, gate_errors, report, rounds = base, [], {}, []
    for path in a.delta:
        delta = json.load(open(path, encoding='utf-8'))
        if delta.get('language') != base['language']:
            raise SystemExit('delta language %r != %r' % (delta.get('language'), base['language']))
        if delta.get('publication_status') == 'test-only' or delta.get('fixture'):
            raise SystemExit('refusing a test-only fixture as candidate content')
        cand, errs, rep = merge(cand, delta)
        gate_errors += errs
        report[delta.get('round_id') or path] = rep
        rounds.append(delta.get('round_id') or 'x')
    missing = [e['id'] for e in base['entries'] if e['id'] not in {x['id'] for x in cand['entries']}]
    if missing:
        gate_errors.append('ids lost vs active package: %s' % missing[:10])
    delta = {'round_id': '.'.join(rounds)}
    cand['version'] = bump(base.get('version'), delta.get('round_id'))
    cand['status'] = 'candidate'
    unit_errors, unit_warnings, counts = validate(cand)
    errors = gate_errors + unit_errors
    os.makedirs(os.path.join(a.out, a.lang), exist_ok=True)
    name = '%s-%s.json' % (base['package_id'], cand['version'])
    data = (json.dumps(cand, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    manifest = {
        'package_id': base['package_id'], 'candidate_version': cand['version'], 'round_id': delta.get('round_id'),
        'created': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'publication': 'not-published (needs owner authorization; catalog untouched)',
        'base': {'path': os.path.relpath(base_path, ROOT), 'version': base.get('version'), 'sha256': sha(raw), 'size_bytes': len(raw)},
        'candidate': {'file': name, 'sha256': sha(data), 'size_bytes': len(data)},
        'rollback': 'keep the base file/sha above in the catalog entry; promotion replaces url/sha/version only',
        'report': report, 'counts': counts, 'errors': errors, 'warnings': unit_warnings[:200],
        'gates_passed': not errors,
    }
    if not errors:
        open(os.path.join(a.out, a.lang, name), 'wb').write(data)
    with open(os.path.join(a.out, a.lang, 'manifest.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(json.dumps({k: manifest[k] for k in ('candidate_version', 'report', 'counts', 'gates_passed')}, ensure_ascii=False))
    for e in errors[:50]:
        print('ERROR', e)
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
