# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：面積「平方公分」（108課綱 N-3-14）
  python3 tools/gen_tw_math_g3_area.py
1 平方公分的意義、數方格求面積、不規則圖形、比較面積、長方形排成幾排幾個、面積和周長的區別、量感。
誤答：周長と取り違える、1 列だけ数える、單位を「公分」にする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, FILL, INK, BLUE

R = random.Random(31014)
NM = Names(R)
C = 26   # 1 格


def grid_svg(cells, cols, rows, cells2=None, labels=None):
    s = []
    for (x, y) in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (10 + x * C, 10 + y * C, C, C, FILL))
    for (x, y) in (cells2 or ()):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#cfdcf0'/>" % (10 + x * C, 10 + y * C, C, C))
    for i in range(cols + 1):
        s.append("<line x1='%d' y1='10' x2='%d' y2='%d' stroke='#9aa' stroke-width='1'/>" % (10 + i * C, 10 + i * C, 10 + rows * C))
    for j in range(rows + 1):
        s.append("<line x1='10' y1='%d' x2='%d' y2='%d' stroke='#9aa' stroke-width='1'/>" % (10 + j * C, 10 + cols * C, 10 + j * C))
    for (x, y, t, col) in (labels or ()):
        s.append(text(10 + x * C + C / 2, 10 + y * C + C / 2 + 6, t, 17, col=col))
    return fig(svg_wrap(cols * C + 20, rows * C + 20, "".join(s), "方格紙上的圖形，1 格是 1 平方公分"))


def rect_cells(x0, y0, w, h):
    return [(x0 + i, y0 + j) for i in range(w) for j in range(h)]


def blob(n, maxw=7, maxh=5):
    cells = {(R.randint(1, maxw - 2), R.randint(1, maxh - 2))}
    while len(cells) < n:
        x, y = R.choice(sorted(cells))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nx, ny = x + dx, y + dy
        if 0 <= nx < maxw and 0 <= ny < maxh:
            cells.add((nx, ny))
    return sorted(cells)


def perim(cells):
    st = set(cells)
    return sum(1 for (x, y) in cells for d in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + d[0], y + d[1]) not in st)


def s1(seen):
    def mk():
        w, h = R.randint(2, 8), R.randint(2, 5)
        if w == h and R.random() < .5:
            return None
        a = w * h
        q = "1 格是 1 平方公分。塗色的長方形面積是多少？" + grid_svg(rect_cells(1, 1, w, h), w + 2, h + 2)
        return mcq(q, "%d 平方公分" % a, ["%d 平方公分" % x for x in (2 * (w + h), w + h, a + w, a - h)] + ["%d 公分" % a],
                   "%d 排，每排 %d 格，%d × %d ＝ %d，面積是 %d 平方公分。" % (h, w, w, h, a, a))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.randint(5, 14)
        cells = blob(n)
        p = perim(cells)
        if p == n:
            return None
        q = "1 格是 1 平方公分。塗色圖形的面積是多少？" + grid_svg(cells, 7, 5)
        return mcq(q, "%d 平方公分" % n, ["%d 平方公分" % x for x in (p, n + 1, n - 1, n + 2)],
                   "一格一格數，共有 %d 格，面積是 %d 平方公分。（%d 是周長的公分數，不是面積）" % (n, n, p))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(5, 12), R.randint(5, 12)
        ca = [(x, y) for (x, y) in blob(a, 5, 5)]
        cb = [(x + 6, y) for (x, y) in blob(b, 5, 5)]
        lab = [(min(ca)[0], min(ca, key=lambda c: c[1])[1], "", INK)]
        if R.random() < .5:
            if a == b:
                return None
            q = "甲（綠色）和乙（藍色），哪一個面積比較大？" + grid_svg(ca, 11, 5, cb)
            big = "甲" if a > b else "乙"
            return mcq(q, big, ["乙" if big == "甲" else "甲", "一樣大", "看起來比較長的那一個"],
                       "甲有 %d 格，乙有 %d 格，%s的面積比較大。" % (a, b, big))
        if a == b:
            return None
        q = "甲（綠色）和乙（藍色）的面積相差幾平方公分？（1 格是 1 平方公分）" + grid_svg(ca, 11, 5, cb)
        d = abs(a - b)
        return mcq(q, "%d 平方公分" % d, ["%d 平方公分" % x for x in (a + b, d + 1, d + 2, max(a, b))],
                   "甲 %d 格，乙 %d 格，%d － %d ＝ %d（平方公分）。" % (a, b, max(a, b), min(a, b), d))
    del_ = mk
    return pick_unique(R, del_, 20, seen)


def s4(seen):
    def rows():
        r, c = R.randint(3, 9), R.randint(3, 9)
        q = "一個長方形用 1 平方公分的方格排滿，排了 %d 排，每排 %d 個。面積是多少？" % (r, c)
        a = r * c
        return mcq(q, "%d 平方公分" % a, ["%d 平方公分" % x for x in (r + c, 2 * (r + c), a + c, a - r)],
                   "%d 排，每排 %d 個：%d × %d ＝ %d（平方公分）。" % (r, c, r, c, a))

    def which():
        cells = blob(R.randint(6, 12))
        n, p = len(cells), perim(cells)
        if n == p:
            return None
        ask = R.choice(["面積", "周長"])
        q = "1 格的邊長是 1 公分。這個圖形的<b>%s</b>是多少？" % ask + grid_svg(cells, 7, 5)
        if ask == "面積":
            return mcq(q, "%d 平方公分" % n, ["%d 公分" % p, "%d 平方公分" % p, "%d 公分" % n],
                       "面積是數裡面的格子：%d 格 ＝ %d 平方公分。" % (n, n))
        return mcq(q, "%d 公分" % p, ["%d 平方公分" % n, "%d 公分" % n, "%d 平方公分" % p],
                   "周長是數外圍的邊：共 %d 條邊，%d 公分。" % (p, p))
    return pick_unique(R, rows, 10, seen) + pick_unique(R, which, 10, seen)


def s5(seen):
    SENSE = [("一個手指甲的面積大約是多少？", "1 平方公分", ["1 平方公尺", "100 平方公分", "1 公分"], "手指甲大約 1 公分 × 1 公分，約 1 平方公分。"),
             ("一張郵票的面積大約是多少？", "6 平方公分", ["6 平方公尺", "600 平方公分", "6 公分"], "郵票大約長 3 公分、寬 2 公分，約 6 平方公分。"),
             ("「平方公分」是用來量什麼的單位？", "面積（平面的大小）", ["長度", "重量", "容量"], "公分量長度，平方公分量面的大小。"),
             ("1 平方公分是怎樣的正方形？", "邊長 1 公分的正方形", ["邊長 1 毫米的正方形", "周長 1 公分的正方形", "邊長 10 公分的正方形"], "邊長 1 公分的正方形，面積是 1 平方公分。")]
    out = [mcq(*x) for x in SENSE]
    for b in out:
        seen.add(b["q"])

    def word():
        who = NM.next()
        kind = R.choice(["sticker", "tile", "two"])
        if kind == "sticker":
            r, c = R.randint(3, 8), R.randint(4, 9)
            q = "%s用 1 平方公分的正方形貼紙，把一張卡片貼滿：排了 %d 排，每排 %d 張。卡片的面積是多少？" % (who, r, c)
            a = r * c
            return mcq(q, "%d 平方公分" % a, ["%d 平方公分" % x for x in (r + c, 2 * (r + c), a + r)], "%d × %d ＝ %d（平方公分）。" % (r, c, a))
        if kind == "tile":
            a = R.randint(20, 60)
            used = R.randint(5, a - 5)
            q = "一張卡片的面積是 %d 平方公分，已經貼了 %d 平方公分的貼紙，還有多少平方公分沒有貼？" % (a, used)
            d = a - used
            return mcq(q, "%d 平方公分" % d, ["%d 平方公分" % x for x in (a + used, d + 1, d - 1, d + 10)], "%d － %d ＝ %d（平方公分）。" % (a, used, d))
        a, b = R.randint(12, 40), R.randint(12, 40)
        if a == b:
            return None
        o = NM.next()
        if o == who:
            return None
        q = "%s的書籤面積是 %d 平方公分，%s的書籤面積是 %d 平方公分。兩張合起來是多少平方公分？" % (who, a, o, b)
        return mcq(q, "%d 平方公分" % (a + b), ["%d 平方公分" % x for x in (abs(a - b), a + b + 10, a + b - 1)] + ["%d 公分" % (a + b)],
                   "%d ＋ %d ＝ %d（平方公分）。" % (a, b, a + b))
    return out + pick_unique(R, word, 16, seen)


def main():
    seen = set()
    sets = [("數方格：長方形", s1(seen)), ("數方格：不規則圖形", s2(seen)), ("比較面積", s3(seen)),
            ("幾排幾個、面積和周長", s4(seen)), ("量感和應用問題", s5(seen))]
    demo = grid_svg(rect_cells(1, 1, 4, 3), 6, 5)
    body = lesson(
        ["<b>面積</b>是一個面的大小。邊長 1 公分的正方形，面積是 <b>1 平方公分</b>。",
         "數一數圖形裡有幾個 1 平方公分的方格，就是面積。",
         "長方形可以看成<b>幾排、每排幾個</b>，用乘法算比較快。",
         "<b>周長</b>是外圍一圈的長度（公分），<b>面積</b>是裡面的大小（平方公分），不一樣。"],
        [example("塗色長方形的面積是多少？" + demo, ["排了 3 排，每排 4 格。", "3 × 4 ＝ 12。"], "12 平方公分"),
         example("排了 5 排，每排 6 個 1 平方公分的方格，面積是多少？", ["5 × 6 ＝ 30。"], "30 平方公分")],
        [("把周長當成面積", "面積數裡面的格子，周長數外圍的邊"),
         ("單位寫成「公分」", "面積的單位是「平方公分」"),
         ("只數第一排", "要算全部的排：幾排 × 每排幾個")])
    faq = [{"q": "平方公分和公分有什麼不同？",
            "a": "公分量長度（一條線多長），平方公分量面積（一個面多大）。邊長 1 公分的正方形面積是 1 平方公分。"},
           {"q": "三年級的面積要學到公式嗎？",
            "a": "108課綱 N-3-14 在三年級以數方格、實測和估測為主；長方形面積公式（長 × 寬）在四年級正式學習。"},
           {"q": "孩子常把面積和周長弄混，怎麼辦？",
            "a": "在方格紙上用兩種顏色：一種塗裡面（面積），一種描外框（周長），讓孩子看到它們數的東西不一樣。"}]
    make_unit(R, "grade-3", "area-square-centimeters", "N-3-14",
              "面積：「平方公分」。實測、量感、估測與計算。",
              "面積：平方公分",
              "三年級數學 面積 練習題｜平方公分・數方格・面積和周長 學習單（附解答）",
              "面積（平方公分）",
              "國小三年級數學「面積」免費學習單：認識1平方公分、數方格求面積、不規則圖形、比較面積、面積和周長的區別與應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 格 1 平方公分，數有幾格",
              "長方形：幾排 × 每排幾個。面積的單位是平方公分。",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
