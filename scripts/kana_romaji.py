"""Hiragana/katakana → romaji (Hepburn, long vowels written as in the existing packages: ou, uu, aa)."""
D = {}
base = {
 'あ':'a','い':'i','う':'u','え':'e','お':'o','か':'ka','き':'ki','く':'ku','け':'ke','こ':'ko','さ':'sa','し':'shi','す':'su','せ':'se','そ':'so',
 'た':'ta','ち':'chi','つ':'tsu','て':'te','と':'to','な':'na','に':'ni','ぬ':'nu','ね':'ne','の':'no','は':'ha','ひ':'hi','ふ':'fu','へ':'he','ほ':'ho',
 'ま':'ma','み':'mi','む':'mu','め':'me','も':'mo','や':'ya','ゆ':'yu','よ':'yo','ら':'ra','り':'ri','る':'ru','れ':'re','ろ':'ro','わ':'wa','を':'o','ん':'n',
 'が':'ga','ぎ':'gi','ぐ':'gu','げ':'ge','ご':'go','ざ':'za','じ':'ji','ず':'zu','ぜ':'ze','ぞ':'zo','だ':'da','ぢ':'ji','づ':'zu','で':'de','ど':'do',
 'ば':'ba','び':'bi','ぶ':'bu','べ':'be','ぼ':'bo','ぱ':'pa','ぴ':'pi','ぷ':'pu','ぺ':'pe','ぽ':'po','ゔ':'vu',
 'ぁ':'a','ぃ':'i','ぅ':'u','ぇ':'e','ぉ':'o','ゃ':'ya','ゅ':'yu','ょ':'yo','ゎ':'wa'}
yoon = {'ゃ':'a','ゅ':'u','ょ':'o'}
special = {'しゃ':'sha','しゅ':'shu','しょ':'sho','ちゃ':'cha','ちゅ':'chu','ちょ':'cho','じゃ':'ja','じゅ':'ju','じょ':'jo','ぢゃ':'ja','ぢゅ':'ju','ぢょ':'jo',
 'てぃ':'ti','でぃ':'di','ふぁ':'fa','ふぃ':'fi','ふぇ':'fe','ふぉ':'fo','うぃ':'wi','うぇ':'we','うぉ':'wo','しぇ':'she','ちぇ':'che','じぇ':'je','とぅ':'tu','どぅ':'du','ゔぁ':'va','ゔぃ':'vi','ゔぇ':'ve','ゔぉ':'vo'}

def to_hira(s):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)

def romaji(s):
    s = to_hira(s)
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        two = s[i:i+2]
        if two in special:
            out.append(special[two]); i += 2; continue
        if i + 1 < len(s) and s[i+1] in yoon and c in base and c not in yoon and base[c].endswith('i'):
            out.append(base[c][:-1] + 'y' + yoon[s[i+1]]); i += 2; continue
        if c == 'っ':
            nxt = romaji(s[i+1:i+3])[:1] if i + 1 < len(s) else ''
            out.append('t' if nxt == 'c' else nxt); i += 1; continue
        if c == 'ー':
            prev = ''.join(out)
            v = next((ch for ch in reversed(prev) if ch in 'aeiou'), '')
            out.append(v); i += 1; continue
        if c == 'ん':
            nxt = s[i+1:i+2]
            out.append("n'" if nxt and nxt in 'あいうえおやゆよ' else 'n'); i += 1; continue
        if c in base:
            out.append(base[c])
        elif c in '〜～':
            pass
        elif c in ' 、・':
            out.append(' ')
        elif c in '！？。':
            pass
        else:
            out.append(c)
        i += 1
    return ''.join(out).strip()

if __name__ == '__main__':
    for t in ['こんにちわ', 'がっこう', 'きょうだい', 'しんぱい', 'ちょっとまって', 'らーめん', 'コンピューター', 'げんいん', 'ちゃんねる', 'ぱーてぃー', 'まっちゃ']:
        print(t, romaji(t))
