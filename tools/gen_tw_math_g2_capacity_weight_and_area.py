# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：容量、重量、面積的比較（108課綱 N-2-12）
  python3 tools/gen_tw_math_g2_capacity_weight_and_area.py
容量（杯數で比べる、移し替え）、重量（天秤・積木の個數）、面積（重ねる、方格の數）、個別單位の注意（同じ單位で比べる）、間接比較。
誤答：高さだけで容量を判斷する、大きさだけで重さを判斷する、單位が違うのに數だけで比べる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, INK
from tw_g7 import tidy_sets

R = random.Random(81313)
NM = Names(R)
L3 = "甲乙丙"


def grid_shape(cells, label):
    u = 22
    xs = [c for c, r in cells]
    ys = [r for c, r in cells]
    W = (max(xs) + 1) * u + 16
    H = (max(ys) + 1) * u + 16
    s = []
    for c, r in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#bfe0c6' stroke='%s' stroke-width='1.2'/>" % (8 + c * u, 8 + r * u, u, u, INK))
    return fig(svg_wrap(W, H, "".join(s), label))


def blob(n, seed):
    rnd = random.Random(seed)
    cells = {(0, 0)}
    while len(cells) < n:
        c, r = rnd.choice(sorted(cells))
        dc, dr = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nc, nr = c + dc, r + dr
        if 0 <= nc < 6 and 0 <= nr < 4:
            cells.add((nc, nr))
    return sorted(cells)


def s1(seen):
    def mk():
        cups = R.sample(range(3, 15), 3)
        what = R.choice(["水壺", "水瓶", "鍋子", "桶子"])
        k = R.choice(["多", "少"])
        i = cups.index(max(cups) if k == "多" else min(cups))
        q = "用同樣的杯子裝水：甲%s倒出 %d 杯，乙%s倒出 %d 杯，丙%s倒出 %d 杯。哪一個裝得最%s？" % (what, cups[0], what, cups[1], what, cups[2], k)
        return mcq(q, L3[i], [x for x in L3 if x != L3[i]] + ["一樣多"], "用一樣的杯子量，杯數%s的裝得%s：%s %d 杯。" % ("最多" if k == "多" else "最少", k, L3[i], cups[i]))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.sample(range(3, 20), 2)
        x, y = R.sample(["蘋果", "書包", "字典", "西瓜", "水壺", "鉛筆盒", "玩具車", "芭樂"], 2)
        k = R.choice(["blocks", "diff"])
        if k == "blocks":
            q = "用一樣的積木秤重，%s和 %d 個積木一樣重，%s和 %d 個積木一樣重。哪一個比較重？" % (x, a, y, b)
            ans = x if a > b else y
            return mcq(q, ans, [y if ans == x else x, "一樣重", "不能比"], "積木越多越重：%d %s %d。" % (a, "＞" if a > b else "＜", b))
        q = "用一樣的積木秤重，%s和 %d 個積木一樣重，%s和 %d 個積木一樣重。%s比%s重幾個積木？" % (x, max(a, b), y, min(a, b), x, y)
        return mcq(q, "%d 個" % (abs(a - b)), ["%d 個" % v for v in (a + b, max(a, b), abs(a - b) + 1)], "%d － %d ＝ %d。" % (max(a, b), min(a, b), abs(a - b)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        n1, n2 = R.sample(range(5, 15), 2)
        g1 = grid_shape(blob(n1, R.randint(1, 99999)), "甲")
        g2 = grid_shape(blob(n2, R.randint(1, 99999)), "乙")
        q = "每一格一樣大。甲和乙哪一個面積比較大？大幾格？<p>甲</p>%s<p>乙</p>%s" % (g1, g2)
        ans = "甲" if n1 > n2 else "乙"
        d = abs(n1 - n2)
        return mcq(q, "%s，大 %d 格" % (ans, d), ["%s，大 %d 格" % ("乙" if ans == "甲" else "甲", d), "%s，大 %d 格" % (ans, n1 + n2), "一樣大"], "數格子：甲 %d 格，乙 %d 格，%s大 %d 格。" % (n1, n2, ans, d))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    FACTS = [("高的瓶子一定裝得比較多嗎？", "不一定，要倒出來比", ["一定比較多", "一定比較少", "一樣多"], "瓶子的高矮、胖瘦都會影響容量，要用一樣的杯子倒出來比。"),
             ("大的東西一定比較重嗎？", "不一定，要用秤或天秤比", ["一定比較重", "一定比較輕", "一樣重"], "大的氣球很輕，小的鐵球很重，要實際秤才知道。"),
             ("天秤往哪一邊傾斜，表示哪一邊比較重？", "往下的那一邊比較重", ["往上的那一邊比較重", "兩邊一樣重", "看不出來"], "重的那邊會往下沉。"),
             ("兩張紙怎麼直接比哪一張面積大？", "把它們疊在一起，看哪一張蓋住另一張", ["比哪一張比較長", "比哪一張比較厚", "比顏色"], "疊起來，能完全蓋住另一張的面積比較大。"),
             ("小明用大杯子量是 5 杯，小美用小杯子量是 8 杯，可以說小美的水比較多嗎？", "不能，杯子不一樣大", ["可以，8 比 5 多", "可以，小杯比較準", "不能，要用手摸"], "用的單位（杯子）不一樣，不能只看杯數比。"),
             ("天秤兩邊一樣高，表示什麼？", "兩邊一樣重", ["左邊比較重", "右邊比較重", "天秤壞了"], "天秤平衡表示兩邊一樣重。"),
             ("兩個瓶子裝的水，怎麼間接比較誰多？", "分別倒進一樣的杯子，比杯數", ["看瓶子的顏色", "比瓶子的高度", "用手掂掂看"], "用一樣的杯子當單位，數杯數就能比較。"),
             ("用方格紙比兩個圖形的面積，要注意什麼？", "格子要一樣大", ["格子越大越好", "圖形要一樣長", "只要數邊"], "用一樣大的格子當單位，數幾格才能比。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def bal():
        x, y = R.sample(["蘋果", "柳丁", "梨子", "芭樂", "番茄", "奇異果"], 2)
        a = R.randint(2, 9)
        q = "天秤一邊放 1 個%s，另一邊放 %d 個一樣的積木，天秤平衡。2 個%s和幾個積木一樣重？" % (x, a, x)
        return mcq(q, "%d 個" % (2 * a), ["%d 個" % v for v in (a, a + 2, 2 * a + 1)], "1 個%s ＝ %d 個積木，2 個就是 %d ＋ %d ＝ %d 個。" % (x, a, a, a, 2 * a))
    return out + pick_unique(R, bal, 12, seen)


def s5(seen):
    def mk():
        who = NM.next()
        k = R.choice(["pour", "total"])
        if k == "pour":
            a = R.randint(6, 15)
            b = R.randint(2, a - 1)
            q = "一壺水可以倒滿 %d 杯，%s倒出 %d 杯喝掉了，壺裡還能倒幾杯？" % (a, who, b)
            return mcq(q, "%d 杯" % (a - b), ["%d 杯" % v for v in (a + b, b, a - b + 1)], "%d － %d ＝ %d。" % (a, b, a - b))
        a, b = R.randint(3, 9), R.randint(3, 9)
        q = "甲桶倒出 %d 杯水，乙桶倒出 %d 杯水（用一樣的杯子）。兩桶一共倒出幾杯？" % (a, b)
        return mcq(q, "%d 杯" % (a + b), ["%d 杯" % v for v in (abs(a - b) if a != b else a, a + b + 1, a * b)], "%d ＋ %d ＝ %d。" % (a, b, a + b))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("比容量", s1(seen)), ("比重量", s2(seen)), ("比面積", s3(seen)),
            ("怎麼比才公平", s4(seen)), ("應用問題", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>容量</b>：用一樣的杯子倒水，杯數多的裝得多。",
         "<b>重量</b>：用天秤比，往下沉的比較重；也可以看和幾個一樣的積木一樣重。",
         "<b>面積</b>：疊起來比，或數有幾個一樣大的格子。" + grid_shape(blob(8, 7), "方格"),
         "用個別單位比較時，<b>單位要一樣</b>。"],
        [example("甲倒出 8 杯、乙倒出 5 杯", ["用一樣的杯子，8 比 5 多 3。"], "甲多 3 杯"),
         example("蘋果和 6 個積木一樣重，梨和 9 個一樣重", ["9 比 6 多。"], "梨比較重")],
        [("高的瓶子裝得比較多", "要倒出來比"),
         ("大杯 5 杯比小杯 8 杯少", "杯子不一樣大不能比"),
         ("天秤高的那邊比較重", "往下沉的比較重")])
    faq = [{"q": "二年級為什麼還不學公升、公斤？",
            "a": "108課綱 N-2-12：二年級先用操作做直接比較、間接比較和個別單位，三年級再學公升、毫升、公斤、公克等普遍單位。"},
           {"q": "什麼是間接比較？",
            "a": "兩個東西不能直接放在一起比時，用第三個東西（例如杯子、積木、繩子）當中間的工具來比。"},
           {"q": "在家怎麼練？",
            "a": "用同一個杯子量家裡不同的水壺，用衣架做簡單的天秤比水果，用拼圖片比兩張紙的大小。"}]
    make_unit(R, "grade-2", "capacity-weight-and-area", "N-2-12",
              "容量、重量、面積：以操作活動為主。此階段量的教學應包含初步認識、直接比較、間接比較（含個別單位）。",
              "比容量、重量和面積",
              "二年級數學 容量重量面積 練習題｜直接比較・個別單位 學習單（附解答）",
              "容量、重量、面積",
              "國小二年級數學「比容量、重量和面積」免費學習單：用杯子比容量、用天秤和積木比重量、數方格比面積、怎麼比才公平、應用問題。100題線上練習，附可列印解答。",
              "用一樣的單位比：杯子、積木、格子",
              "高的不一定裝得多，大的不一定重。",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
