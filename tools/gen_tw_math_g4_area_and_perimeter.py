# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：正方形與長方形的周長和面積、平方公尺（108課綱 S-4-3、N-4-11）
  python3 tools/gen_tw_math_g4_area_and_perimeter.py
周長・面積の公式、辺の長さを逆算、簡單複合圖形（L字形）、平方公尺の量感と計算、應用問題。
誤答：周長を 長＋寬 にする、面積と周長の取り違え、單位（公分・平方公分）の取り違え、複合圖形で重なりを二重に数える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, FILL, INK

R = random.Random(41013)
NM = Names(R)


def rect_svg(w, h, u="公分"):
    sc = min(220 / w, 120 / h)
    W, H = w * sc, h * sc
    s = "<rect x='70' y='26' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='3'/>" % (W, H, FILL, GREEN)
    s += text(70 + W / 2, 18, "%d %s" % (w, u), 14) + text(62, 26 + H / 2 + 5, "%d %s" % (h, u), 14, anchor="end")
    return fig(svg_wrap(int(W + 90), int(H + 40), s, "長方形"))


def L_svg(W, H, cw, ch, u="公分"):
    """W×H の長方形から右上の cw×ch を切り取った L 字形"""
    sc = min(240 / W, 140 / H)
    pts = [(0, 0), (W - cw, 0), (W - cw, ch), (W, ch), (W, H), (0, H)]
    p = " ".join("%.1f,%.1f" % (80 + x * sc, 30 + y * sc) for x, y in pts)
    s = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='3'/>" % (p, FILL, GREEN)
    s += text(80 + (W - cw) * sc / 2, 22, "%d %s" % (W - cw, u), 13)
    s += text(72, 30 + H * sc / 2 + 5, "%d %s" % (H, u), 13, anchor="end")
    s += text(80 + W * sc / 2, 30 + H * sc + 18, "%d %s" % (W, u), 13)
    s += text(80 + W * sc + 6, 30 + (ch + H) * sc / 2 + 5, "%d %s" % (H - ch, u), 13, anchor="start")
    return fig(svg_wrap(int(W * sc + 150), int(H * sc + 56), s, "L 字形"))


def s1(seen):
    def mk():
        w, h = R.randint(4, 30), R.randint(2, 20)
        if w <= h:
            return None
        sq = R.random() < .3
        if sq:
            h = w
        ask = R.choice(["周長", "面積"])
        q = "這個%s的<b>%s</b>是多少？" % ("正方形" if sq else "長方形", ask) + rect_svg(w, h)
        P, A = 2 * (w + h), w * h
        if ask == "周長":
            return mcq(q, "%d 公分" % P, ["%d 公分" % (w + h), "%d 平方公分" % A, "%d 公分" % A if A != P else "%d 公分" % (P + 2), "%d 平方公分" % P],
                       "周長 ＝（長 ＋ 寬）× 2 ＝（%d ＋ %d）× 2 ＝ %d（公分）。" % (w, h, P))
        return mcq(q, "%d 平方公分" % A, ["%d 平方公分" % P if P != A else "%d 平方公分" % (A + w), "%d 公分" % A, "%d 平方公分" % (w + h), "%d 平方公分" % (A + h)],
                   "面積 ＝ 長 × 寬 ＝ %d × %d ＝ %d（平方公分）。" % (w, h, A))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def side_area():
        w, h = R.randint(3, 25), R.randint(2, 15)
        A = w * h
        q = "長方形的面積是 %d 平方公分，寬是 %d 公分，長是幾公分？" % (A, h)
        return mcq(q, "%d 公分" % w, ["%d 公分" % x for x in (A - h, A * h if A * h < 2000 else A + h, A // 2 - h if A // 2 - h > 0 and A // 2 - h != w else w + 2, w + 1)],
                   "長 ＝ 面積 ÷ 寬 ＝ %d ÷ %d ＝ %d（公分）。" % (A, h, w))

    def side_per():
        w, h = R.randint(4, 30), R.randint(2, 20)
        if w == h:
            return None
        P = 2 * (w + h)
        q = "長方形的周長是 %d 公分，長是 %d 公分，寬是幾公分？" % (P, w)
        return mcq(q, "%d 公分" % h, ["%d 公分" % x for x in (P - w, P // 2, P - 2 * w, h + 2) if x > 0 and x != h],
                   "長 ＋ 寬 ＝ %d ÷ 2 ＝ %d，寬 ＝ %d － %d ＝ %d（公分）。" % (P, P // 2, P // 2, w, h))

    def square():
        a = R.randint(3, 20)
        if R.random() < .5:
            q = "正方形的周長是 %d 公分，面積是多少？" % (4 * a)
            return mcq(q, "%d 平方公分" % (a * a), ["%d 平方公分" % x for x in (4 * a, (4 * a) ** 2 if (4 * a) ** 2 < 2000 else a * 4 + a, 2 * a * a, (a + 1) * (a + 1)) if x != a * a],
                       "邊長 ＝ %d ÷ 4 ＝ %d（公分），面積 ＝ %d × %d ＝ %d（平方公分）。" % (4 * a, a, a, a, a * a))
        q = "正方形的面積是 %d 平方公分，邊長是幾公分？" % (a * a)
        return mcq(q, "%d 公分" % a, ["%d 公分" % x for x in (a * a // 4 if a * a // 4 != a else a + 2, a * a // 2, a + 1, a - 1, a * a, a + 3)],
                   "哪個數自己乘自己是 %d？%d × %d ＝ %d，邊長 %d 公分。" % (a * a, a, a, a * a, a))
    return pick_unique(R, side_area, 7, seen) + pick_unique(R, side_per, 7, seen) + pick_unique(R, square, 6, seen)


def s3(seen):
    def mk():
        W, H = R.randint(8, 20), R.randint(6, 15)
        cw, ch = R.randint(2, W - 3), R.randint(2, H - 3)
        ask = R.choice(["面積", "周長"])
        q = "這個圖形的<b>%s</b>是多少？（每個角都是直角）" % ask + L_svg(W, H, cw, ch)
        A = W * H - cw * ch
        P = 2 * (W + H)
        if ask == "面積":
            return mcq(q, "%d 平方公分" % A, ["%d 平方公分" % x for x in (W * H, W * H + cw * ch, A - ch, P) if x != A],
                       "用大長方形減去缺的那一塊：%d × %d － %d × %d ＝ %d（平方公分）。" % (W, H, cw, ch, A))
        return mcq(q, "%d 公分" % P, ["%d 公分" % x for x in (P - 2 * cw if P - 2 * cw != P else P - 2, P - cw - ch, P + 2 * ch, A) if x != P],
                   "把凹進去的邊移出去，周長和大長方形一樣：（%d ＋ %d）× 2 ＝ %d（公分）。" % (W, H, P))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    SENSE = [("一間教室的地板面積", "70", "平方公尺"), ("一張郵票的面積", "6", "平方公分"), ("一張書桌桌面的面積", "1", "平方公尺"),
             ("一個籃球場的面積", "420", "平方公尺"), ("一本數學課本封面的面積", "520", "平方公分"), ("一張悠遊卡的面積", "46", "平方公分")]
    out = []
    for it, n, u in SENSE:
        out.append(mcq("%s大約是 %s ___，填哪一個單位最合適？" % (it, n), u, [x for x in ("平方公尺", "平方公分", "公尺", "公分") if x != u],
                       "想一想實際有多大：%s大約 %s %s。" % (it, n, u)))
    for b in out:
        seen.add(b["q"])

    def room():
        w, h = R.randint(3, 15), R.randint(2, 10)
        what = R.choice(["教室", "客廳", "菜園", "停車位", "游泳池"])
        if what == "停車位":
            w, h = R.choice([(5, 2), (6, 3), (5, 3)])
            what = "停車位（長 %d 公尺、寬 %d 公尺）" % (w, h)
            q = "一個%s的面積是幾平方公尺？" % what
        else:
            q = "一塊長方形的%s，長 %d 公尺、寬 %d 公尺，面積是幾平方公尺？" % (what, w, h)
        A = w * h
        return mcq(q, "%d 平方公尺" % A, ["%d 平方公尺" % (2 * (w + h)) if 2 * (w + h) != A else "%d 平方公尺" % (A + w), "%d 公尺" % A, "%d 平方公分" % A, "%d 平方公尺" % (w + h)],
                   "面積 ＝ 長 × 寬 ＝ %d × %d ＝ %d（平方公尺）。邊長用公尺，面積就用平方公尺。" % (w, h, A))
    return out + pick_unique(R, room, 14, seen)


def s5(seen):
    def fence():
        w, h = R.randint(5, 30), R.randint(3, 20)
        if w == h:
            return None
        q = "長 %d 公尺、寬 %d 公尺的長方形菜園，四周要圍上籬笆，籬笆要幾公尺？" % (w, h)
        P = 2 * (w + h)
        return mcq(q, "%d 公尺" % P, ["%d 公尺" % (w + h), "%d 公尺" % (w * h) if w * h != P else "%d 公尺" % (P + 2), "%d 平方公尺" % (w * h), "%d 公尺" % (2 * w + h)],
                   "籬笆圍一圈是周長：（%d ＋ %d）× 2 ＝ %d（公尺）。" % (w, h, P))

    def tiles():
        w, h = R.randint(3, 9), R.randint(2, 8)
        k = R.choice([1, 4])
        q = "用邊長 1 公尺的正方形地墊，鋪滿長 %d 公尺、寬 %d 公尺的地板，要幾塊？" % (w, h)
        return mcq(q, "%d 塊" % (w * h), ["%d 塊" % x for x in (2 * (w + h), w + h, w * h + w, w * h - h) if x != w * h],
                   "1 塊是 1 平方公尺，地板面積 %d × %d ＝ %d 平方公尺，要 %d 塊。" % (w, h, w * h, w * h))

    def wire():
        P = R.choice([20, 24, 28, 32, 36, 40, 44, 48])
        a = P // 4
        q = "用一條 %d 公分的鐵絲圍成一個正方形，面積是多少？" % P
        return mcq(q, "%d 平方公分" % (a * a), ["%d 平方公分" % x for x in (P, (P // 2) ** 2, a * 2, a * a + a, P * a)],
                   "邊長 %d ÷ 4 ＝ %d（公分），面積 %d × %d ＝ %d（平方公分）。" % (P, a, a, a, a * a))
    return pick_unique(R, fence, 8, seen) + pick_unique(R, tiles, 7, seen) + pick_unique(R, wire, 5, seen)


def main():
    seen = set()
    sets = [("周長和面積的公式", s1(seen)), ("求邊長", s2(seen)), ("簡單複合圖形", s3(seen)),
            ("平方公尺", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["長方形：<b>周長 ＝（長 ＋ 寬）× 2</b>，<b>面積 ＝ 長 × 寬</b>。正方形：周長 ＝ 邊長 × 4，面積 ＝ 邊長 × 邊長。",
         "周長的單位是公分、公尺；面積的單位是<b>平方公分</b>、<b>平方公尺</b>。邊長 1 公尺的正方形，面積是 1 平方公尺。",
         "知道面積和一邊，求另一邊用除法；知道周長和一邊，先 ÷ 2 再減。",
         "複合圖形：切成幾個長方形，或用大長方形減去缺的部分。"],
        [example("長 12 公分、寬 5 公分的長方形，周長和面積是多少？", ["周長：（12 ＋ 5）× 2 ＝ 34（公分）。", "面積：12 × 5 ＝ 60（平方公分）。"], "周長 34 公分，面積 60 平方公分"),
         example("周長 30 公分的長方形，長 9 公分，寬是多少？", ["長 ＋ 寬 ＝ 30 ÷ 2 ＝ 15。", "寬 ＝ 15 － 9 ＝ 6。"], "6 公分")],
        [("周長 ＝ 長 ＋ 寬", "長和寬各有 2 條：（長 ＋ 寬）× 2"),
         ("面積的單位寫成公分", "面積要寫平方公分或平方公尺"),
         ("複合圖形把重疊的部分算兩次", "畫線切開，每一塊只算一次")])
    faq = [{"q": "長方形的周長和面積公式是什麼？",
            "a": "周長 ＝（長 ＋ 寬）× 2；面積 ＝ 長 × 寬。正方形周長 ＝ 邊長 × 4，面積 ＝ 邊長 × 邊長。"},
           {"q": "四年級的面積要學什麼？",
            "a": "108課綱 S-4-3、N-4-11：理解正方形和長方形的周長與面積公式並應用，算簡單複合圖形，並認識平方公尺。"},
           {"q": "平方公尺有多大？",
            "a": "邊長 1 公尺的正方形就是 1 平方公尺，大約是一張書桌的桌面。一間教室大約 60〜70 平方公尺。"}]
    make_unit(R, "grade-4", "area-and-perimeter", "S-4-3",
              "正方形與長方形的面積與周長：理解邊長與周長或面積的關係，並能理解其公式與應用。簡單複合圖形。",
              "周長和面積：公式、複合圖形、平方公尺",
              "四年級數學 周長和面積 練習題｜長方形公式・複合圖形・平方公尺 學習單（附解答）",
              "周長和面積",
              "國小四年級數學「周長和面積」免費學習單：長方形和正方形的周長與面積公式、求邊長、簡單複合圖形、平方公尺與應用題。100題線上練習馬上對答案，附可列印解答。",
              "周長 ＝（長 ＋ 寬）× 2，面積 ＝ 長 × 寬",
              "周長用公分，面積用平方公分。",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
