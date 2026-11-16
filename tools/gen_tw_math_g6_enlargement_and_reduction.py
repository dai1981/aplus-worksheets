# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：放大圖與縮小圖（108課綱 S-6-1）
  python3 tools/gen_tw_math_g6_enlargement_and_reduction.py
幾倍放大圖・幾倍縮小圖、對應邊成比例・對應角相等、對應邊を求める、倍數を求める、周長も同じ倍數、方格紙の圖。
誤答：邊に同じ數を足す、對應角も倍にする、縮小圖で掛けてしまう、倍數を逆數にする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff, num, fig, svg_wrap, text, GREEN, FILL, INK, BLUE

R = random.Random(61009)
NM = Names(R)


def frs(v):
    return ff(v, mixed=False) if v.denominator != 1 else num(v.numerator)


def grid_pair(pts, k, lab_a="原圖", lab_b="放大圖"):
    """方格紙の上に原圖と k 倍の圖を並べる（pts は格子座標）"""
    C = 14
    w1 = max(x for x, y in pts)
    h1 = max(y for x, y in pts)
    k = F(k)
    W = int((w1 + w1 * k + 5) * C) + 20
    H = int((max(h1, h1 * k) + 3) * C) + 10
    s = []
    for i in range(0, int(W / C) + 1):
        s.append("<line x1='%d' y1='0' x2='%d' y2='%d' stroke='#e2e2e2' stroke-width='1'/>" % (i * C, i * C, H))
    for j in range(0, int(H / C) + 1):
        s.append("<line x1='0' y1='%d' x2='%d' y2='%d' stroke='#e2e2e2' stroke-width='1'/>" % (j * C, W, j * C))
    oy = (max(h1, h1 * k) + 2) * C
    p1 = " ".join("%.1f,%.1f" % (C + x * C, oy - y * C) for x, y in pts)
    ox2 = (w1 + 3) * C
    p2 = " ".join("%.1f,%.1f" % (ox2 + float(x * k) * C, oy - float(y * k) * C) for x, y in pts)
    s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (p1, FILL, GREEN))
    s.append("<polygon points='%s' fill='#dbe7f5' stroke='%s' stroke-width='2'/>" % (p2, BLUE))
    s.append(text(C + w1 * C / 2, oy + 16, lab_a, 12))
    s.append(text(ox2 + float(w1 * k) * C / 2, oy + 16, lab_b, 12))
    return fig(svg_wrap(W, int(oy + 24), "".join(s), "方格紙上的%s和%s" % (lab_a, lab_b)))


SHAPES = [[(0, 0), (2, 0), (2, 1), (0, 1)], [(0, 0), (3, 0), (0, 2)], [(0, 0), (2, 0), (2, 2), (0, 2)], [(0, 0), (3, 0), (2, 2), (1, 2)],
          [(0, 0), (2, 0), (3, 2), (1, 2)], [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (0, 2)], [(0, 0), (4, 0), (4, 1), (0, 1)], [(0, 0), (2, 0), (1, 3)]]


def s1(seen):
    def mk():
        pts = R.choice(SHAPES)
        k = R.choice([2, 3, F(3, 2)])
        g = grid_pair(pts, k)
        q = "右邊的藍色圖形是左邊綠色圖形的幾倍放大圖？" + g
        return mcq(q, "%s 倍" % frs(F(k)), ["%s 倍" % frs(x) for x in (F(k) + 1, 1 / F(k), F(k) * 2) if x != F(k)],
                   "對應邊的長度：藍色圖形都是綠色圖形的 %s 倍。" % frs(F(k)))

    def small():
        pts = [(x * 2, y * 2) for x, y in R.choice(SHAPES)]
        k = F(1, 2)
        g = grid_pair(pts, k, "原圖", "縮小圖")
        q = "右邊的藍色圖形是左邊綠色圖形的幾倍縮小圖？" + g
        return mcq(q, "%s 倍" % frs(k), ["2 倍", "%s 倍" % frs(F(1, 4)), "%s 倍" % frs(F(1, 3))], "對應邊都變成原來的一半：%s 倍縮小圖。" % frs(k))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, small, 6, seen)


def s2(seen):
    def mk():
        a, b = R.randint(2, 12), R.randint(2, 12)
        if a == b:
            return None
        k = R.choice([2, 3, 4, 5, F(1, 2), F(3, 2), F(5, 2)])
        k = F(k)
        if (a * k).denominator != 1 or (b * k).denominator != 1:
            return None
        kind = "放大圖" if k > 1 else "縮小圖"
        q = "一個長方形長 %d 公分、寬 %d 公分。畫它的 %s 倍%s，長和寬各是幾公分？" % (max(a, b), min(a, b), frs(k), kind)
        L, W = max(a, b) * k, min(a, b) * k
        ans = "長 %s 公分、寬 %s 公分" % (frs(L), frs(W))
        add = k - 1 if k > 1 else 0
        w = ["長 %s 公分、寬 %s 公分" % (frs(max(a, b) + k), frs(min(a, b) + k)), "長 %s 公分、寬 %s 公分" % (frs(L), frs(F(min(a, b)))), "長 %s 公分、寬 %s 公分" % (frs(max(a, b) / k), frs(min(a, b) / k))]
        return mcq(q, ans, w, "每一條邊都乘以 %s：%d × %s ＝ %s，%d × %s ＝ %s。" % (frs(k), max(a, b), frs(k), frs(L), min(a, b), frs(k), frs(W)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def angle():
        A = R.choice([30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80])
        k = R.choice([2, 3, 4, F(1, 2), F(1, 3)])
        kind = "放大圖" if F(k) > 1 else "縮小圖"
        q = "一個三角形有一個角是 %d 度。畫它的 %s 倍%s，對應的角是幾度？" % (A, frs(F(k)), kind)
        wrong = A * F(k)
        return mcq(q, "%d 度" % A, ["%s 度" % frs(x) for x in (wrong, A + 10, 180 - A) if x != A], "放大或縮小時，對應角的大小不變：還是 %d 度。" % A)

    def tf():
        T = [("放大圖和原圖的對應角相等。", True), ("縮小圖的對應邊長是原圖的同樣幾倍。", True), ("放大 2 倍後，每個角也變成 2 倍。", False),
             ("把每條邊都加長 2 公分，就是放大圖。", False), ("正方形的放大圖還是正方形。", True), ("長方形的 3 倍放大圖，周長也是原來的 3 倍。", True),
             ("縮小圖的角比原圖的角小。", False), ("把長方形的長變 2 倍、寬不變，就是 2 倍放大圖。", False)]
        st, ok = R.choice(T)
        return mcq("判斷對錯：%s" % st, "對" if ok else "錯", ["錯" if ok else "對", "不一定", "要量了才知道"],
                   "放大圖和縮小圖：對應角相等，對應邊都乘以同一個倍數。" + ("" if ok else "這句話是錯的。"))
    return pick_unique(R, angle, 12, seen) + pick_unique(R, tf, 8, seen)


def s4(seen):
    def find_k():
        a = R.randint(2, 15)
        k = F(R.choice([2, 3, 4, 5, F(1, 2), F(1, 3), F(3, 2), F(2, 3)]))
        b = a * k
        if b.denominator != 1 or b == a:
            return None
        q = "原圖的一條邊長 %d 公分，在新圖中對應的邊長 %s 公分。新圖是原圖的幾倍%s？" % (a, frs(b), "放大圖" if k > 1 else "縮小圖")
        return mcq(q, "%s 倍" % frs(k), ["%s 倍" % frs(x) for x in (1 / k, b - a if b > a else a - b, k + 1)  if x != k and x > 0], "倍數 ＝ 新圖的邊 ÷ 原圖的對應邊：%s ÷ %d ＝ %s。" % (frs(b), a, frs(k)))

    def other():
        a, c = R.randint(3, 12), R.randint(3, 12)
        k = F(R.choice([2, 3, F(3, 2), F(5, 2), F(1, 2)]))
        b, d = a * k, c * k
        if b.denominator != 1 or d.denominator != 1 or a == c:
            return None
        q = "三角形甲的兩邊長是 %d 公分和 %d 公分；三角形乙是甲的放大或縮小圖，%d 公分的對應邊是 %s 公分。%d 公分的對應邊是幾公分？" % (a, c, a, frs(b), c)
        return mcq(q, "%s 公分" % frs(d), ["%s 公分" % frs(x) for x in (c + (b - a), c / k, c * k + k) if x != d and x > 0], "倍數：%s ÷ %d ＝ %s；%d × %s ＝ %s（公分）。" % (frs(b), a, frs(k), c, frs(k), frs(d)))
    return pick_unique(R, find_k, 10, seen) + pick_unique(R, other, 10, seen)


def s5(seen):
    def photo():
        a, b = R.choice([(4, 6), (5, 7), (6, 8), (3, 5), (8, 10)])
        k = R.choice([2, 3, F(5, 2)])
        k = F(k)
        if (a * k).denominator != 1 or (b * k).denominator != 1:
            return None
        who = NM.next()
        q = "%s把一張長 %d 公分、寬 %d 公分的照片放大 %s 倍。放大後的周長是幾公分？" % (who, b, a, frs(k))
        P = (a + b) * 2 * k
        return mcq(q, "%s 公分" % frs(P), ["%s 公分" % frs(x) for x in ((a + b) * 2, (a + k + b + k) * 2, a * b * k * k)  if x != P], "長和寬都乘以 %s，周長也變成 %s 倍：（%d ＋ %d）× 2 × %s ＝ %s（公分）。" % (frs(k), frs(k), a, b, frs(k), frs(P)))

    def model():
        real = R.randint(20, 90) * 10
        k = R.choice([10, 20, 50])
        q = "一座建築模型是實物的 %s 倍縮小圖。實物高 %d 公分，模型高幾公分？" % (fr(1, k), real)
        m = F(real, k)
        return mcq(q, "%s 公分" % frs(m) if m.denominator == 1 else "%s 公分" % ff(m), ["%s 公分" % num(x) for x in (real * k, real - k)] + ["%s 公分" % ff(m * 10)], "%d × %s ＝ %s（公分）。" % (real, fr(1, k), ff(m)))

    def which():
        a, b = R.randint(2, 6), R.randint(3, 9)
        if a >= b:
            return None
        k = R.randint(2, 4)
        ans = "長 %d、寬 %d" % (b * k, a * k)
        w = ["長 %d、寬 %d" % (b + k, a + k), "長 %d、寬 %d" % (b * k, a), "長 %d、寬 %d" % (b * k + 1, a * k)]
        return mcq("一個長方形長 %d 公分、寬 %d 公分。下面哪一個是它的放大圖？" % (b, a), ans, w, "長和寬都乘以 %d：長 %d、寬 %d，對應邊成比例。" % (k, b * k, a * k))
    return pick_unique(R, photo, 7, seen) + pick_unique(R, model, 6, seen) + pick_unique(R, which, 7, seen)


def main():
    seen = set()
    sets = [("認識放大圖和縮小圖", s1(seen)), ("畫放大圖和縮小圖", s2(seen)), ("對應角相等", s3(seen)),
            ("求倍數和對應邊", s4(seen)), ("應用", s5(seen))]
    body = lesson(
        ["把圖形每一條邊都乘以 2，叫做 <b>2 倍放大圖</b>；都乘以 <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>，叫做 <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> 倍<b>縮小圖</b>。",
         "放大或縮小時：<b>對應角相等</b>，<b>對應邊成比例</b>（都乘以同一個數）。形狀不變，大小改變。",
         "倍數 ＝ 新圖的邊 ÷ 原圖的對應邊。"],
        [example("長 6 公分、寬 4 公分的長方形，畫 <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> 倍縮小圖。", ["6 × <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> ＝ 3，4 × <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> ＝ 2。"], "長 3 公分、寬 2 公分"),
         example("一個角 50 度，放大 3 倍後是幾度？", ["對應角不變。"], "50 度")],
        [("每條邊都加 2 公分", "要乘以同一個倍數"),
         ("放大 2 倍，角也變 2 倍", "對應角大小不變"),
         ("只放大長，寬不變", "長和寬都要乘以同一個數")])
    faq = [{"q": "怎樣才是放大圖或縮小圖？",
            "a": "新圖的每一條邊都是原圖對應邊的同樣幾倍，而且對應角相等。只改一邊或每邊加一樣長都不是。"},
           {"q": "放大 2 倍，周長和面積會變幾倍？",
            "a": "周長也是 2 倍；面積是 2 × 2 ＝ 4 倍，因為長和寬都變成 2 倍。"},
           {"q": "六年級的放大與縮小要學什麼？",
            "a": "108課綱 S-6-1：比例思考的應用，認識幾倍放大圖、幾倍縮小圖，知道縮放時對應角相等、對應邊成比例。"}]
    make_unit(R, "grade-6", "enlargement-and-reduction", "S-6-1",
              "放大與縮小：比例思考的應用。「幾倍放大圖」、「幾倍縮小圖」。知道縮放時，對應角相等，對應邊成比例。",
              "放大圖與縮小圖",
              "六年級數學 放大圖與縮小圖 練習題｜對應邊成比例・對應角相等 學習單（附解答）",
              "放大與縮小",
              "國小六年級數學「放大圖與縮小圖」免費學習單：在方格紙上認識幾倍放大圖和縮小圖、畫出對應邊、對應角相等、求倍數和對應邊與照片、模型等應用題。100題線上練習馬上對答案，附可列印解答。",
              "對應邊成比例，對應角相等",
              "每一條邊都乘以同一個倍數，形狀不變。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
