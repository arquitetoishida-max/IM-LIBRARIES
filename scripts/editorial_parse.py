"""Parses curation/editorial/batches/*.txt (one line per English id).

Kept:     N|pos|description_en|pt-BR main;alt;...|ja main;alt;...|reading[=spoken]
Excluded: N|-|reason            (reason 'infl:<lemma>' = regular inflection of <lemma>)
"""
import re, pathlib, json, sys
R = pathlib.Path(__file__).resolve().parents[1]
KANJI = re.compile(r'[一-鿿㐀-䶿々]')
KANA_ONLY = re.compile(r'^[぀-ヿ〜ー・、。！？\s]+$')

def load():
    rows = {}
    errs = []
    for f in sorted((R / 'curation/editorial/batches').glob('b*.txt')):
        for ln, line in enumerate(f.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip() or line.startswith('#'):
                continue
            p = line.split('|')
            try:
                n = int(p[0])
            except ValueError:
                errs.append(f'{f.name}:{ln} bad id'); continue
            if n in rows:
                errs.append(f'{f.name}:{ln} duplicate {n}')
            if p[1] == '-':
                rows[n] = {'keep': False, 'reason': '|'.join(p[2:])}
                continue
            if len(p) != 6:
                errs.append(f'{f.name}:{ln} {n} has {len(p)} fields'); continue
            pos, desc, pt, ja, rd = p[1:]
            pt_l = [x.strip() for x in pt.split(';') if x.strip()]
            ja_l = [x.strip() for x in ja.split(';') if x.strip()]
            reading, spoken = (rd.split('=', 1) + [None])[:2] if rd else ('', None)
            if ja_l:
                main = ja_l[0]
                if KANJI.search(main) and not reading:
                    errs.append(f'{f.name}:{ln} {n} kanji without reading: {main}')
                if KANJI.search(reading or ''):
                    errs.append(f'{f.name}:{ln} {n} reading has kanji')
            if not desc.strip():
                errs.append(f'{f.name}:{ln} {n} empty description')
            rows[n] = {'keep': True, 'pos': pos, 'desc': desc.strip(), 'pt': pt_l, 'ja': ja_l, 'reading': reading.strip(), 'spoken': (spoken or '').strip() or None}
    return rows, errs

if __name__ == '__main__':
    rows, errs = load()
    print(len(rows), 'rows;', sum(r['keep'] for r in rows.values()), 'kept')
    for e in errs: print('ERR', e)
