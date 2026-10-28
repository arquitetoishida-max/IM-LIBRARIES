"""Writing (stroke-order) packs, separate from the dictionaries and linked by Unicode character.

ja: KanjiVG (CC BY-SA 3.0) — kanji + kana appearing in v2/ja-core-v2.json.
zh: hanzi-writer-data (Make Me a Hanzi; Arphic Public License / LGPL) — hanzi in v2/zh-core-v2.json.
Each character = ordered strokes; each stroke = centerline polyline, flat [x0,y0,x1,y1,...] in 0..1000,
origin top-left (y down). Usage: python scripts/build_writing_packs.py <kanjivg_dir> <hanzi_writer_data_dir>
"""
import json, re, sys, math, hashlib, pathlib
R = pathlib.Path(__file__).resolve().parents[1]
V2 = R / 'v2'
OUT = V2 / 'writing'
OUT.mkdir(exist_ok=True)
POINTS = 16

def chars_of(pkg, test):
    d = json.loads((V2 / pkg).read_text(encoding='utf-8'))
    s = set()
    for e in d['entries']:
        for t in [e['text'], *e.get('alternatives', [])]:
            s.update(c for c in t if test(c))
    return sorted(s)

is_cjk = lambda c: '一' <= c <= '鿿' or '㐀' <= c <= '䶿'
is_kana = lambda c: 'ぁ' <= c <= 'ゖ' or 'ァ' <= c <= 'ヺ'

def resample(pts, n=POINTS):
    if len(pts) < 2:
        return pts * 2
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg) or 1e-9
    out, acc, i = [pts[0]], 0.0, 0
    for k in range(1, n - 1):
        target = total * k / (n - 1)
        while i < len(seg) - 1 and acc + seg[i] < target:
            acc += seg[i]; i += 1
        t = (target - acc) / (seg[i] or 1e-9)
        a, b = pts[i], pts[i + 1]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    out.append(pts[-1])
    return out

def flat(pts, scale_x, scale_y, off_y=0.0, flip=False):
    r = []
    for x, y in pts:
        X = round(x * scale_x)
        Y = round(((off_y - y) if flip else y) * scale_y)
        r += [max(0, min(1000, X)), max(0, min(1000, Y))]
    return r

TOK = re.compile(r'[MmCcSsLlHhVvZz]|-?\d*\.?\d+(?:e-?\d+)?')
def svg_path_points(d):
    """Samples an SVG path (M/C/S/L/H/V, absolute or relative) into a polyline."""
    toks = TOK.findall(d)
    pts, cur, start, last_ctrl, cmd, i = [], (0.0, 0.0), (0.0, 0.0), None, None, 0
    def num():
        nonlocal i
        v = float(toks[i]); i += 1; return v
    def cubic(p0, p1, p2, p3):
        for k in range(1, 9):
            t = k / 8
            mt = 1 - t
            pts.append((mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0],
                        mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1]))
    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]):
            cmd = toks[i]; i += 1
            if cmd in 'Zz':
                cur = start; pts.append(cur); continue
        rel = cmd.islower()
        c = cmd.upper()
        ox, oy = cur if rel else (0.0, 0.0)
        if c == 'M':
            cur = (ox + num(), oy + num()); start = cur; pts.append(cur); last_ctrl = None
            cmd = 'l' if rel else 'L'
        elif c == 'L':
            cur = (ox + num(), oy + num()); pts.append(cur); last_ctrl = None
        elif c == 'H':
            cur = ((cur[0] if rel else 0) + num(), cur[1]); pts.append(cur); last_ctrl = None
        elif c == 'V':
            cur = (cur[0], (cur[1] if rel else 0) + num()); pts.append(cur); last_ctrl = None
        elif c == 'C':
            p1 = (ox + num(), oy + num()); p2 = (ox + num(), oy + num()); p3 = (ox + num(), oy + num())
            cubic(cur, p1, p2, p3); last_ctrl = p2; cur = p3
        elif c == 'S':
            p1 = (2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_ctrl else cur
            p2 = (ox + num(), oy + num()); p3 = (ox + num(), oy + num())
            cubic(cur, p1, p2, p3); last_ctrl = p2; cur = p3
        else:
            i += 1
    return pts

def kanjivg(dirpath, chars):
    out, missing = {}, []
    base = pathlib.Path(dirpath)
    for ch in chars:
        f = base / f'{ord(ch):05x}.svg'
        if not f.exists():
            missing.append(ch); continue
        svg = f.read_text(encoding='utf-8')
        paths = re.findall(r'<path[^>]*\sid="kvg:[0-9a-f]+-s(\d+)"[^>]*\sd="([^"]+)"', svg)
        if not paths:
            paths = [(m[1], m[0]) for m in re.findall(r'<path[^>]*\sd="([^"]+)"[^>]*\sid="kvg:[0-9a-f]+-s(\d+)"', svg)]
        strokes = [flat(resample(svg_path_points(d)), 1000 / 109, 1000 / 109) for _, d in sorted(paths, key=lambda p: int(p[0]))]
        if strokes:
            out[ch] = strokes
        else:
            missing.append(ch)
    return out, missing

def hanziwriter(dirpath, chars):
    out, missing = {}, []
    base = pathlib.Path(dirpath)
    for ch in chars:
        f = base / f'{ch}.json'
        if not f.exists():
            missing.append(ch); continue
        d = json.loads(f.read_text(encoding='utf-8'))
        strokes = [flat(resample([tuple(p) for p in m]), 1000 / 1024, 1000 / 1024, off_y=900, flip=True) for m in d.get('medians', [])]
        if strokes:
            out[ch] = strokes
        else:
            missing.append(ch)
    return out, missing

def save(pid, lang, name, chars, license_, source, missing):
    pack = {'schema_version': 1, 'package_type': 'ishida-writing', 'package_id': pid, 'language': lang, 'name': name, 'version': '1.0.0',
            'license': license_, 'source': source, 'format': 'strokes: ordered centerline polylines, flat [x,y,...] 0..1000, y down',
            'missing': ''.join(missing), 'chars': chars}
    text = json.dumps(pack, ensure_ascii=False, separators=(',', ':'))
    (OUT / f'{pid}.json').write_text(text, encoding='utf-8')
    return {'id': pid, 'name': name, 'language': lang, 'region': None, 'role': 'writing', 'kind': 'ishida-writing', 'schema_version': 1,
            'available': True, 'entry_count': len(chars), 'version': '1.0.0', 'license': license_,
            'url': f'https://raw.githubusercontent.com/arquitetoishida-max/IM-LIBRARIES/main/v2/writing/{pid}.json',
            'sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(), 'size_bytes': len(text.encode('utf-8'))}

ja_chars = chars_of('ja-core-v2.json', lambda c: is_cjk(c) or is_kana(c))
zh_chars = chars_of('zh-core-v2.json', is_cjk)
ja, ja_miss = kanjivg(sys.argv[1], ja_chars)
zh, zh_miss = hanziwriter(sys.argv[2], zh_chars)
entries = [
    save('ja-writing-kanjivg', 'ja', 'Japanese writing — KanjiVG stroke order', ja, 'CC BY-SA 3.0 (KanjiVG, Ulrich Apel)', 'https://kanjivg.tagaini.net', ja_miss),
    save('zh-writing-hanziwriter', 'zh', 'Mandarin writing — Hanzi Writer stroke data', zh, 'Arphic Public License / LGPL (Make Me a Hanzi via hanzi-writer-data)', 'https://github.com/chanind/hanzi-writer-data', zh_miss),
]
cat_path = V2 / 'catalog.json'
cat = json.loads(cat_path.read_text(encoding='utf-8'))
cat['packages'] = [p for p in cat['packages'] if p.get('kind') != 'ishida-writing'] + entries
cat_path.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('ja', len(ja), 'missing', len(ja_miss), '| zh', len(zh), 'missing', len(zh_miss))
