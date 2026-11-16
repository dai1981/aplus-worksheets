# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：正方體和長方體的體積與表面積（108課綱 S-5-5）
  python3 tools/gen_tw_math_g5_volume_and_surface_area.py
體積公式（長×寬×高、邊長×邊長×邊長）、表面積（6 面の和）、逆算（高さ）、体積と表面積の区別、複合（2 つの直方体）、應用。
誤答：表面積で 3 面しか足さない、體積と表面積の取り違え、單位（平方公分・立方公分）の取り違え。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, FILL, INK

R = random.Random(51021)
NM = Names(R)


def box_svg(a, b, c):
    """長 a、寬 b、高 c の斜投影図"""
    s = 120 / max(a, b * .6, c)
    W, D, H = a * s, b * s * .5, c * s
    ox, oy = 40, 20 + D
    front = [(ox, oy), (ox + W, oy), (ox + W, oy + H), (ox, oy + H)]
    top = [(ox, oy), (ox + D, oy - D), (ox + W + D, oy - D), (ox + W, oy)]
    side = [(ox + W, oy), (ox + W + D, oy - D), (ox + W + D, oy + H - D), (ox + W, oy + H)]
    P = lambda pts: " ".join("%.1f,%.1f" % p for p in pts)
    g = "".join("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (P(f), c_, GREEN) for f, c_ in ((front, FILL), (top, "#e3f2e7"), (side, "#bcdcc5")))
    g += text(ox + W / 2, oy + H + 18, "%s 公分" % a, 13) + text(ox + W + D + 6, oy + H / 2 - D / 2, "%s 公分" % c, 13, anchor="start")
    g += text(ox + W + D / 2 + 4, oy - D / 2 + 14, "%s 公分" % b, 12, anchor="start")
    return fig(svg_wrap(int(ox + W + D + 80), int(oy + H + 28), g, "長方體"))


def s1(seen):
    def mk():
        a, b, c = R.randint(3, 15), R.randint(2, 12), R.randint(2, 12)
        a, b = max(a, b), min(a, b)
        cube = R.random() < .25
        if cube:
            b = c = a
        q = "這個%s的體積是多少？" % ("正方體" if cube else "長方體") + box_svg(a, b, c)
        v = a * b * c
        S = 2 * (a * b + b * c + a * c)
        return mcq(q, "%s 立方公分" % num(v), ["%s 立方公分" % num(x) for x in (S, a * b, a + b + c) if x != v] + ["%s 平方公分" % num(v)],
                   "體積 ＝ 長 × 寬 × 高 ＝ %d × %d × %d ＝ %s（立方公分）。" % (a, b, c, num(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b, c = R.randint(2, 12), R.randint(2, 10), R.randint(2, 10)
        a, b = max(a, b), min(a, b)
        cube = R.random() < .3
        if cube:
            b = c = a
        q = "%s的表面積是多少？" % ("邊長 %d 公分的正方體" % a if cube else "長 %d 公分、寬 %d 公分、高 %d 公分的長方體" % (a, b, c))
        S = 2 * (a * b + b * c + a * c)
        half = a * b + b * c + a * c
        v = a * b * c
        return mcq(q, "%s 平方公分" % num(S), ["%s 平方公分" % num(x) for x in (half, v, a * a * 4 if cube else 4 * (a + b + c)) if x != S],
                   ("正方體 6 個面都一樣：%d × %d × 6 ＝ %s（平方公分）。" % (a, a, num(S))) if cube else "上下、前後、左右各 2 面：（%d × %d ＋ %d × %d ＋ %d × %d）× 2 ＝ %s（平方公分）。" % (a, b, b, c, a, c, num(S)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def h():
        a, b, c = R.randint(3, 15), R.randint(2, 12), R.randint(2, 15)
        a, b = max(a, b), min(a, b)
        v = a * b * c
        q = "長方體的體積是 %s 立方公分，長 %d 公分、寬 %d 公分，高是幾公分？" % (num(v), a, b)
        return mcq(q, "%d 公分" % c, ["%d 公分" % x for x in (v - a - b if v - a - b < 500 else c * 2, v // a if v // a < 300 else c + 1, c + 2) if x != c], "高 ＝ 體積 ÷（長 × 寬）＝ %s ÷ %d ＝ %d（公分）。" % (num(v), a * b, c))

    def cube_edge():
        a = R.randint(2, 10)
        q = "正方體的體積是 %s 立方公分，邊長是幾公分？" % num(a ** 3)
        return mcq(q, "%d 公分" % a, ["%d 公分" % x for x in (a ** 3 // 3 if a ** 3 // 3 != a else a + 3, a * a, a + 1)], "哪個數乘三次是 %s？%d × %d × %d ＝ %s。" % (num(a ** 3), a, a, a, num(a ** 3)))

    def cube_from_sa():
        a = R.randint(2, 10)
        q = "正方體的表面積是 %d 平方公分，一個面的面積是多少？邊長是多少？" % (6 * a * a)
        return mcq(q, "一面 %d 平方公分，邊長 %d 公分" % (a * a, a), ["一面 %d 平方公分，邊長 %d 公分" % x for x in ((a * a * 6 // 4, a + 1), (a * a, a * 2), (a * a * 3, a * 3))],
                   "6 個面一樣：%d ÷ 6 ＝ %d，%d × %d ＝ %d，邊長 %d 公分。" % (6 * a * a, a * a, a, a, a * a, a))
    return pick_unique(R, h, 8, seen) + pick_unique(R, cube_edge, 6, seen) + pick_unique(R, cube_from_sa, 6, seen)


def s4(seen):
    def which():
        a, b, c = R.randint(3, 10), R.randint(2, 8), R.randint(2, 8)
        a, b = max(a, b), min(a, b)
        ask = R.choice(["vol", "sa"])
        if ask == "vol":
            q = "一個長 %d 公分、寬 %d 公分、高 %d 公分的紙盒，裡面最多能放幾個 1 立方公分的小正方體？" % (a, b, c)
            v = a * b * c
            return mcq(q, "%d 個" % v, ["%d 個" % x for x in (2 * (a * b + b * c + a * c), a * b, a + b + c) if x != v], "這是在算體積：%d × %d × %d ＝ %d（個）。" % (a, b, c, v))
        q = "要用紙把一個長 %d 公分、寬 %d 公分、高 %d 公分的盒子完全包住（不重疊），至少要多少平方公分的紙？" % (a, b, c)
        S = 2 * (a * b + b * c + a * c)
        return mcq(q, "%d 平方公分" % S, ["%d 平方公分" % x for x in (a * b * c, a * b + b * c + a * c, 4 * (a + b + c)) if x != S], "包住外面是在算表面積：（%d × %d ＋ %d × %d ＋ %d × %d）× 2 ＝ %d（平方公分）。" % (a, b, b, c, a, c, S))

    def compose():
        a, b, c = R.randint(4, 10), R.randint(2, 6), R.randint(2, 6)
        a, b = max(a, b), min(a, b)
        a2, c2 = R.randint(2, a - 1), R.randint(2, 6)
        q = "一個積木由兩個長方體疊成：下面長 %d、寬 %d、高 %d 公分，上面長 %d、寬 %d、高 %d 公分。體積是多少？" % (a, b, c, a2, b, c2)
        v = a * b * c + a2 * b * c2
        return mcq(q, "%d 立方公分" % v, ["%d 立方公分" % x for x in (a * b * (c + c2), a * b * c, (a + a2) * b * (c + c2)) if x != v], "分成兩塊：%d × %d × %d ＋ %d × %d × %d ＝ %d（立方公分）。" % (a, b, c, a2, b, c2, v))
    return pick_unique(R, which, 12, seen) + pick_unique(R, compose, 8, seen)


def s5(seen):
    def tank():
        a, b, c = R.choice([30, 40, 50, 60]), R.choice([20, 25, 30, 40]), R.choice([20, 30, 40, 50])
        q = "一個長方體魚缸裡面長 %d 公分、寬 %d 公分、高 %d 公分，裝滿水是幾公升？" % (a, b, c)
        v = a * b * c
        return mcq(q, "%s 公升" % num(v // 1000) if v % 1000 == 0 else "%s 公升" % (v / 1000), ["%s 公升" % num(x) for x in (v, v // 100, v // 10000 if v // 10000 else v // 10)], "%d × %d × %d ＝ %s 立方公分 ＝ %s 公升。" % (a, b, c, num(v), num(v // 1000) if v % 1000 == 0 else v / 1000))

    def paint():
        a, b, c = R.randint(3, 8), R.randint(3, 8), R.randint(2, 4)
        a, b = max(a, b), min(a, b)
        q = "一間長 %d 公尺、寬 %d 公尺、高 %d 公尺的房間，要油漆四面牆和天花板（不漆地板），要漆多少平方公尺？" % (a, b, c)
        S = 2 * (a * c + b * c) + a * b
        return mcq(q, "%d 平方公尺" % S, ["%d 平方公尺" % x for x in (2 * (a * b + b * c + a * c), 2 * (a * c + b * c), a * b * c) if x != S], "四面牆（%d × %d ＋ %d × %d）× 2 ＝ %d，天花板 %d × %d ＝ %d，合計 %d（平方公尺）。" % (a, c, b, c, 2 * (a * c + b * c), a, b, a * b, S))

    def cubes():
        n = R.randint(2, 5)
        q = "用邊長 1 公分的小正方體，堆成邊長 %d 公分的大正方體，需要幾個？" % n
        return mcq(q, "%d 個" % n ** 3, ["%d 個" % x for x in (n * n, n * 6, n * n * 6) if x != n ** 3], "%d × %d × %d ＝ %d（個）。" % (n, n, n, n ** 3))
    return pick_unique(R, tank, 7, seen) + pick_unique(R, paint, 9, seen) + pick_unique(R, cubes, 4, seen)


def main():
    seen = set()
    sets = [("長方體和正方體的體積", s1(seen)), ("表面積", s2(seen)), ("反過來求邊長", s3(seen)), ("體積還是表面積", s4(seen)), ("應用問題", s5(seen))]
    demo = box_svg(8, 5, 4)
    body = lesson(
        ["<b>長方體體積 ＝ 長 × 寬 × 高</b>；<b>正方體體積 ＝ 邊長 × 邊長 × 邊長</b>。單位是立方公分。",
         "<b>表面積</b>是 6 個面的面積和：長方體上下、前後、左右各一對，<b>（長×寬 ＋ 寬×高 ＋ 長×高）× 2</b>；正方體是 邊長 × 邊長 × 6。單位是平方公分。",
         "「能裝多少、佔多少空間」算體積；「包裝紙、油漆外面」算表面積。"],
        [example("體積和表面積各是多少？" + demo, ["體積：8 × 5 × 4 ＝ 160。", "表面積：（8 × 5 ＋ 5 × 4 ＋ 8 × 4）× 2 ＝ 184。"], "160 立方公分、184 平方公分"),
         example("體積 120 立方公分，長 6、寬 4 公分，高是多少？", ["120 ÷（6 × 4）＝ 5。"], "5 公分")],
        [("表面積只加 3 個面", "相對的面一樣大，3 個面加起來要 × 2"),
         ("體積寫平方公分", "體積是立方公分，表面積是平方公分"),
         ("包裝紙的題目算體積", "包住外面是表面積")])
    faq = [{"q": "長方體的體積和表面積怎麼算？",
            "a": "體積 ＝ 長 × 寬 × 高；表面積 ＝（長 × 寬 ＋ 寬 × 高 ＋ 長 × 高）× 2。正方體體積 ＝ 邊長³，表面積 ＝ 邊長 × 邊長 × 6。"},
           {"q": "體積和表面積有什麼不同？",
            "a": "體積是物體佔多少空間（立方公分），表面積是所有面加起來的大小（平方公分）。"},
           {"q": "五年級的長方體要學什麼？",
            "a": "108課綱 S-5-5：計算正方體和長方體的體積與表面積，並理解體積公式。"}]
    make_unit(R, "grade-5", "volume-and-surface-area", "S-5-5",
              "正方體和長方體：計算正方體和長方體的體積與表面積。正方體與長方體的體積公式。",
              "正方體和長方體的體積與表面積",
              "五年級數學 體積表面積 練習題｜長方體體積・正方體表面積 學習單（附解答）",
              "體積與表面積",
              "國小五年級數學「正方體和長方體」免費學習單：長方體和正方體的體積公式、表面積、反過來求邊長、分辨體積和表面積與應用題。100題線上練習馬上對答案，附可列印解答。",
              "長方體體積 ＝ 長 × 寬 × 高",
              "表面積是 6 個面加起來。",
              body, faq, sets, 21)


if __name__ == "__main__":
    main()
