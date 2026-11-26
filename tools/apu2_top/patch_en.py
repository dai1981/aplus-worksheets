"""us/uk/au/ca/sg のトップと About（手で作ったページ）の言語メニュー・hreflang・フッターをそろえる。
使い方: python3 patch_en.py 元のファイル... （canonical から国とページを判断し、out/{国}/ に書く）"""
import os, re, sys
from top_data import SEL as _SEL, HREFLANG

CC = ["us", "uk", "au", "ca", "sg"]
SEL = [(k, n) for k, n in _SEL if k not in CC]
EN = {"us": "English (US)", "uk": "English (UK)", "au": "English (AU)", "ca": "English (CA)", "sg": "English (SG)"}
HL = {"us": "en-us", "uk": "en-gb", "au": "en-au", "ca": "en-ca", "sg": "en-sg"}
FOOT = {"us": "Math · US", "uk": "Maths · UK", "au": "Maths · Australia", "ca": "Math · Canada", "sg": "Maths · Singapore"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

def patch(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r'<link rel="canonical" href="https://www\.apu2\.com/(us|uk|au|ca|sg)/(about\.html)?">', s)
    if not m:
        return None
    c, page = m.group(1), m.group(2) or ""
    # 言語メニュー
    opts = "".join('<option value="/%s%s" data-l="%s">%s</option>' % ("" if k == "en" else k + "/", page, k, n) for k, n in SEL)
    opts += "".join('<option value="/%s/%s" data-l="%s"%s>%s</option>' % (k, page, k, " selected" if k == c else "", EN[k]) for k in CC)
    s, n1 = re.subn(r'(<select id="langSel"[^>]*>).*?(</select>)', lambda x: x.group(1) + opts + x.group(2), s, flags=re.S)
    # hreflang（英語の国別ページどうし）
    alt = "".join('<link rel="alternate" hreflang="%s" href="https://www.apu2.com/%s/%s">\n' % (HL[k], k, page) for k in CC)
    alt += '<link rel="alternate" hreflang="x-default" href="https://www.apu2.com/%s">\n' % page
    s, n2 = re.subn(r'(<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n)+', alt, s, count=1)
    # フッター：ほかの国 → International → ほかの言語
    langs = "".join('<a href="/%s/">%s</a>' % (k, FOOT[k]) for k in CC if k != c)
    langs += '<a href="/">aplus (International)</a>'
    langs += "".join('<a href="/%s/" lang="%s">%s</a>' % (k, HREFLANG[k], n) for k, n in SEL if k != "en")
    s, n3 = re.subn(r'<div class="langs">.*?</div>', '<div class="langs">%s</div>' % langs, s, count=1)
    assert (n1, n2, n3) == (1, 1, 1), (path, n1, n2, n3)
    os.makedirs(os.path.join(OUT, c), exist_ok=True)
    dst = os.path.join(OUT, c, page or "index.html")
    open(dst, "w", encoding="utf-8").write(s)
    return dst

if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = patch(p)
        if r: print(r)
