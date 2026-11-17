# -*- coding: utf-8 -*-
"""
プレビュー画像（preview.png / pin.png）用の中国語フォントを作る。
Noto Sans TC（SIL OFL）から、台湾版で実際に使う文字だけを抜き出して
site/worksheets/assets/fonts/NotoSansTC-{Bold,Regular}.otf に書く（数百KB）。

  python3 tools/build_cjk_font.py

台湾の単元を足したら毎回実行する（新しい漢字が増えるため）。
check.py はフォントに無い文字があると WARN を出す。
"""
import glob, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "site", "worksheets", "assets", "fonts")
SRC = "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/SubsetOTF/TC/NotoSansTC-%s.otf"
CACHE = os.environ.get("CJK_FONT_CACHE", "/tmp/noto-tc")
LANGS = ("zh",)          # catalog の lang がこれで始まる国が対象


def chars():
    cat = json.load(open(os.path.join(ROOT, "content", "catalog.json"), encoding="utf-8"))
    codes = [c["code"] for c in cat["countries"] if c["lang"].startswith(LANGS)]
    text = json.dumps([c for c in cat["countries"] if c["code"] in codes], ensure_ascii=False)
    text += json.dumps([x for x in cat["subjects"] + cat["grades"] if x["country"] in codes], ensure_ascii=False)
    for code in codes:
        for p in glob.glob(os.path.join(ROOT, "content", code, "**", "*.json"), recursive=True):
            text += open(p, encoding="utf-8").read()
    for p in ("inc/core.php", "inc/preview.php", "inc/topics.php"):
        text += open(os.path.join(ROOT, "site", "worksheets", p), encoding="utf-8").read()
    text = re.sub(r"<[^>]+>", " ", text)
    s = set(text)
    s.update(chr(c) for c in range(0x20, 0x7f))                       # ASCII
    s.update("，。、；：？！「」『』（）《》〈〉…—～・　＋－×÷＝＜＞％／℃°′″·①②③④⑤⑥⑦⑧⑨⑩□☐○△")
    s.update("０１２３４５６７８９")
    return "".join(sorted(c for c in s if c >= " "))


def main():
    from fontTools import subset
    os.makedirs(CACHE, exist_ok=True)
    want = chars()
    for w in ("Bold", "Regular"):
        src = os.path.join(CACHE, "NotoSansTC-%s.otf" % w)
        if not os.path.exists(src) or os.path.getsize(src) < 1000000:
            print("download", w)
            urllib.request.urlretrieve(SRC % w, src)
        out = os.path.join(OUT, "NotoSansTC-%s.otf" % w)
        opt = subset.Options()
        opt.name_IDs = ["*"]
        opt.notdef_outline = True
        opt.layout_features = ["*"]
        f = subset.load_font(src, opt)
        sub = subset.Subsetter(opt)
        sub.populate(text=want)
        sub.subset(f)
        subset.save_font(f, out, opt)
        print("wrote", os.path.relpath(out, ROOT), os.path.getsize(out) // 1024, "KB,", len(want), "chars")
    lic = os.path.join(OUT, "LICENSE-NotoSansTC.txt")
    if not os.path.exists(lic):
        open(lic, "w", encoding="utf-8").write(
            "Noto Sans TC (subset). Copyright 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'.\n"
            "Licensed under the SIL Open Font License, Version 1.1. https://openfontlicense.org\n"
            "Source: https://github.com/notofonts/noto-cjk\n")


if __name__ == "__main__":
    sys.exit(main())
