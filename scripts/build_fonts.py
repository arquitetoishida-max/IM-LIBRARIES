"""CJK display fonts for the app (cards and writing trainer): subsets of SIL OFL fonts, renamed.

Sources (OFL 1.1): Klee One SemiBold (Fontworks / Klee Project, Google Fonts), M PLUS Rounded 1c Bold
(Rounded M+ Project, Google Fonts), LXGW WenKai Regular (LXGW, github.com/lxgw/LxgwWenKai).
Subsetting to the characters used by the dictionaries/phrases makes a Modified Version: the family is renamed
("IM Ja Klee", "IM Ja Rounded", "IM Zh Kai") because LXGW reserves its font names (OFL clause 3).
Usage: python scripts/build_fonts.py <dir with the original .ttf files> <chars-ja.txt> <chars-zh.txt>
"""
import sys, os, json, hashlib, pathlib
from fontTools.ttLib import TTFont
from fontTools import subset
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'v2' / 'fonts'
JOBS = [('KleeOne-SemiBold.ttf', 'im-font-ja-klee', 'IM Ja Klee', 'ja', 'Klee One (Fontworks, Klee Project) — SIL OFL 1.1', 'OFL-Klee.txt'),
        ('MPLUSRounded1c-Bold.ttf', 'im-font-ja-rounded', 'IM Ja Rounded', 'ja', 'M PLUS Rounded 1c (Rounded M+ Project) — SIL OFL 1.1', 'OFL-MPLUS-Rounded.txt'),
        ('LXGWWenKai-Regular.ttf', 'im-font-zh-kai', 'IM Zh Kai', 'zh', 'LXGW WenKai 霞鹜文楷 (LXGW) — SIL OFL 1.1', 'OFL-LXGW-WenKai.txt')]

def build(src_dir, chars):
    for src, pid, fam, lang, _, _ in JOBS:
        t = TTFont(os.path.join(src_dir, src))
        o = subset.Options(); o.name_IDs = ['*']; o.name_languages = ['*']; o.layout_features = ['*']; o.notdef_outline = True; o.drop_tables += ['DSIG']
        s = subset.Subsetter(o); s.populate(text=chars[lang]); s.subset(t)
        names = {1: fam, 16: fam, 21: fam, 4: fam + ' Regular', 18: fam + ' Regular', 6: fam.replace(' ', '') + '-Regular', 3: pid + ';ishida-multilang'}
        for rec in t['name'].names:
            if rec.nameID in names:
                rec.string = names[rec.nameID]
        t.save(OUT / f'{pid}.ttf')

def catalog():
    cat_path = R / 'v2' / 'catalog.json'
    cat = json.loads(cat_path.read_text(encoding='utf-8'))
    entries = []
    for _, pid, fam, lang, lic, lic_file in JOBS:
        b = (OUT / f'{pid}.ttf').read_bytes()
        entries.append({'id': pid, 'name': fam, 'family': fam, 'language': lang, 'region': None, 'role': 'font', 'kind': 'ishida-font', 'schema_version': 1,
                        'available': True, 'version': '1.0.0', 'license': lic, 'license_url': f'https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/v2/fonts/{lic_file}',
                        'url': f'https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/v2/fonts/{pid}.ttf',
                        'sha256': hashlib.sha256(b).hexdigest(), 'size_bytes': len(b)})
    cat['packages'] = [p for p in cat['packages'] if p.get('kind') != 'ishida-font'] + entries
    cat_path.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    if len(sys.argv) > 3:
        build(sys.argv[1], {'ja': open(sys.argv[2], encoding='utf-8').read(), 'zh': open(sys.argv[3], encoding='utf-8').read()})
    catalog()
