# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：平面圖形和立體形體（108課綱 S-2-1、S-2-2、S-2-4）
  python3 tools/gen_tw_math_g2_shapes.py
三角形・四邊形・圓形の判別（形や向きが違っても）、邊と頂點の數、立體（正方體・長方體・圓柱・球）の名前と面、邊長を合わせた長さ（周長の前置き）。
誤答：傾いた正方形を別の形とする、曲線のある形を三角形とする、頂點の數を間違える、邊長を一辺忘れる。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, fig, svg_wrap, text, INK, BLUE
from tw_g7 import tidy_sets
import k_pics as K
import tw_pics as P

R = random.Random(81316)
NAMES = {3: "三角形", 4: "四邊形", 0: "圓形"}


def poly_pts(n, seed):
    rnd = random.Random(seed)
    base = rnd.uniform(0, 2 * math.pi)
    ang = sorted(base + 2 * math.pi * i / n + rnd.uniform(-0.35, 0.35) for i in range(n))
    return [(60 + 46 * rnd.uniform(0.7, 1.0) * math.cos(a), 60 + 46 * rnd.uniform(0.7, 1.0) * math.sin(a)) for a in ang]


def poly_fig(pts, labels=None, col="#bfe0c6", label="圖形"):
    pts = [(x + 30, y + 14) for x, y in pts]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col, INK)]
    if labels:
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        for i, t in enumerate(labels):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = mx - cx, my - cy
            d = math.hypot(dx, dy) or 1
            s.append(text(mx + 24 * dx / d, my + 20 * dy / d + 5, t, 13, col=BLUE))
    return fig(svg_wrap(180, 150, "".join(s), label))


def curvy():
    return fig(svg_wrap(130, 125, "<path d='M20,100 L110,100 Q110,20 60,20 Q20,30 20,100 Z' fill='#bfe0c6' stroke='%s' stroke-width='2'/>" % INK, "有彎曲邊的圖形"))


def s1(seen):
    def mk():
        k = R.choice([3, 4, 0, "curve"])
        if k == 0:
            q = "這是什麼形狀？" + fig(svg_wrap(130, 125, "<ellipse cx='65' cy='62' rx='48' ry='48' fill='#bfe0c6' stroke='%s' stroke-width='2'/>" % INK, "圓形"))
            return mcq(q, "圓形", ["三角形", "四邊形", "都不是"], "圓圓的，沒有直直的邊和角，是圓形。")
        if k == "curve":
            q = "這個圖形是三角形嗎？" + curvy()
            return mcq(q, "不是，因為有一條邊是彎的", ["是，因為有 3 個角", "是，因為很尖", "不是，因為太大"], "三角形是 3 條直直的邊圍成的，彎的邊不行。")
        seed = R.randint(1, 99999)
        q = "這是什麼形狀？" + poly_fig(poly_pts(k, seed))
        return mcq(q, NAMES[k], [NAMES[x] for x in (3, 4, 0) if x != k] + ["都不是"], "數一數有 %d 條直直的邊，是%s。形狀歪歪的、轉個方向也一樣。" % (k, NAMES[k]))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.choice([3, 4, 5, 6])
        what = R.choice(["邊", "頂點"])
        q = "這個圖形有幾個%s？" % what + poly_fig(poly_pts(n, R.randint(1, 99999)))
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in (n - 1, n + 1, 2 * n)], "直直的邊有 %d 條，兩條邊相交的點（頂點）也有 %d 個。" % (n, n))
    FACTS = [("三角形有幾個頂點？", "3 個", ["4 個", "2 個", "0 個"], "三角形有 3 條邊、3 個頂點。"),
             ("四邊形有幾條邊？", "4 條", ["3 條", "5 條", "8 條"], "四邊形有 4 條邊、4 個頂點。"),
             ("圓形有幾個頂點？", "沒有頂點", ["1 個", "4 個", "很多個"], "圓形沒有直直的邊，也沒有頂點。"),
             ("正方形和長方形都是什麼形？", "四邊形", ["三角形", "圓形", "立體"], "它們都有 4 條邊，都是四邊形。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])
    return out + pick_unique(R, mk, 16, seen)


def cuboid_fig():
    s = "<polygon points='20,50 120,50 120,110 20,110' fill='#f7d774' stroke='%s' stroke-width='1.6'/><polygon points='20,50 50,25 150,25 120,50' fill='#fbe7a1' stroke='%s' stroke-width='1.6'/><polygon points='120,50 150,25 150,85 120,110' fill='#e8c24f' stroke='%s' stroke-width='1.6'/>" % (INK, INK, INK)
    return s


def solids(kind):
    if kind == "cuboid":
        return fig(svg_wrap(170, 120, cuboid_fig(), "長方體"))
    return fig(svg_wrap(110, 110, K.solid(kind, 55, 55, 34, R.choice(["yellow", "red", "blue", "green"])), "立體"))


SOL = {"cube": "正方體", "cuboid": "長方體", "cylinder": "圓柱", "sphere": "球"}


def s3(seen):
    def mk():
        k = R.choice(list(SOL))
        q = "這個立體叫什麼？" + solids(k)
        why = {"cube": "6 個面都是一樣大的正方形，是正方體。", "cuboid": "6 個面都是長方形（或有正方形），長寬高不一樣，是長方體。", "cylinder": "上下兩個面是圓形，側面是彎的，是圓柱。", "sphere": "整個圓圓的，怎麼放都會滾，是球。"}[k]
        return mcq(q, SOL[k], [v for x, v in SOL.items() if x != k], why)
    return pick_unique(R, mk, 8, seen) + [mcq(*f) for f in [
        ("正方體有幾個面？", "6 個", ["4 個", "8 個", "12 個"], "正方體有上下、前後、左右 6 個面。"),
        ("正方體的每個面是什麼形狀？", "正方形", ["長方形", "三角形", "圓形"], "正方體 6 個面都是一樣大的正方形。"),
        ("長方體有幾個面？", "6 個", ["4 個", "8 個", "5 個"], "長方體也有 6 個面。"),
        ("圓柱有幾個平平的面？", "2 個", ["1 個", "3 個", "0 個"], "圓柱上下各有 1 個圓形的平面，側面是彎的。"),
        ("球有幾個平平的面？", "沒有", ["1 個", "2 個", "6 個"], "球整個都是彎的，沒有平面。"),
        ("哪一個立體可以滾，也可以立著疊高？", "圓柱", ["球", "正方體", "長方體"], "圓柱躺著會滾，立著可以疊。"),
        ("哪一個立體怎麼放都會滾？", "球", ["圓柱", "正方體", "長方體"], "球每一邊都是彎的。"),
        ("面紙盒最像哪一種立體？", "長方體", ["正方體", "圓柱", "球"], "面紙盒長、寬、高不一樣，像長方體。"),
        ("骰子最像哪一種立體？", "正方體", ["長方體", "圓柱", "球"], "骰子每個面一樣大，像正方體。"),
        ("罐頭最像哪一種立體？", "圓柱", ["球", "正方體", "長方體"], "罐頭上下是圓，像圓柱。"),
        ("籃球最像哪一種立體？", "球", ["圓柱", "正方體", "長方體"], "籃球圓圓的，是球。"),
        ("用正方體蓋印章，會印出什麼形狀？", "正方形", ["圓形", "三角形", "長方形"], "正方體每個面都是正方形。")]]


def s5(seen):
    def mk():
        n = R.choice([3, 4, 4])
        ls = [R.randint(3, 15) for _ in range(n)]
        if n == 3 and max(ls) * 2 >= sum(ls):
            return None
        pts = poly_pts(n, R.randint(1, 99999))
        q = "把這個%s所有邊的長度合起來，一共是幾公分？" % NAMES[n] + poly_fig(pts, ["%d 公分" % x for x in ls])
        t = sum(ls)
        return mcq(q, "%d 公分" % t, ["%d 公分" % x for x in (t - ls[-1], t + ls[0], max(ls) * n if max(ls) * n != t else t + 1)], "%s ＝ %d 公分。" % (" ＋ ".join(map(str, ls)), t))

    def sq():
        a = R.randint(2, 20)
        k = R.choice(["正方形", "正三角形"])
        n = 4 if k == "正方形" else 3
        q = "一個%s每條邊都是 %d 公分，所有邊合起來是幾公分？" % (k, a)
        return mcq(q, "%d 公分" % (a * n), ["%d 公分" % x for x in (a, a * (n - 1), a + n)], "%d 條邊一樣長：%d × %d ＝ %d 公分。" % (n, a, n, a * n))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, sq, 8, seen)


def main():
    seen = set()
    s4_items = []

    def rect_q():
        a, b = R.sample(range(2, 15), 2)
        q = "長方形的長是 %d 公分、寬是 %d 公分，4 條邊合起來是幾公分？" % (max(a, b), min(a, b))
        t = 2 * (a + b)
        return mcq(q, "%d 公分" % t, ["%d 公分" % x for x in (a + b, a * b, 2 * a + b)], "長方形對邊一樣長：%d ＋ %d ＋ %d ＋ %d ＝ %d。" % (max(a, b), min(a, b), max(a, b), min(a, b), t))

    def draw_q():
        n = R.choice([3, 4])
        q = "在點子圖上，用直尺把 %d 個點依序連起來（最後連回第一點），會畫出幾條邊的圖形？" % n
        return mcq(q, "%d 條邊的%s" % (n, NAMES[n]), ["%d 條邊的%s" % (m, NAMES[m]) for m in (3, 4) if m != n] + ["%d 條邊" % (n + 1), "圓形"], "連 %d 個點、最後連回起點，有 %d 條邊，是%s。" % (n, n, NAMES[n]))
    sets = [("認識平面圖形", s1(seen)), ("邊和頂點", s2(seen)), ("認識立體", s3(seen)),
            ("長方形的邊長和畫線", pick_unique(R, rect_q, 16, seen) + pick_unique(R, draw_q, 2, seen) + [mcq("用直尺畫一條 5 公分的線，要從尺上的哪裡開始畫？", "從 0 開始畫到 5", ["從 1 開始畫到 5", "從 5 開始畫到 10", "哪裡都可以，不用看刻度"], "從 0 畫到 5 是 5 公分；從 1 畫到 5 只有 4 公分。"), mcq("用直尺連接兩點畫線，要注意什麼？", "尺要壓好，筆沿著尺邊畫", ["不用尺也可以畫直", "畫快一點就好", "尺要放斜斜的"], "壓好尺、沿著尺邊畫，線才會直。")]),
            ("邊長合起來", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>三角形</b>：3 條直直的邊、3 個頂點；<b>四邊形</b>：4 條邊、4 個頂點；<b>圓形</b>沒有邊和頂點。圖形歪了或轉了方向，名字不會變。",
         "立體：" + P.solids_row([("cube", "yellow"), ("cylinder", "blue"), ("sphere", "red")], ["正方體", "圓柱", "球"]) + "還有<b>長方體</b>（像面紙盒）。正方體、長方體都有 6 個面。",
         "把圖形每條邊的長度加起來，就是繞圖形一圈的長度（三年級叫周長）。"],
        [example("三條邊 5、6、7 公分的三角形", ["5 ＋ 6 ＋ 7。"], "18 公分"),
         example("長 8、寬 3 的長方形", ["8 ＋ 3 ＋ 8 ＋ 3。"], "22 公分")],
        [("轉了方向的正方形不是正方形", "轉方向形狀不變"),
         ("有彎邊的也是三角形", "三角形的邊都是直的"),
         ("長方形只加兩條邊", "4 條邊都要加")])
    faq = [{"q": "二年級要認識哪些圖形？",
            "a": "108課綱 S-2-1、S-2-2：三角形、四邊形、圓形，以及正方體、長方體、圓柱體、球體，能辨認、描述和分類。"},
           {"q": "什麼是頂點？",
            "a": "兩條邊相交的點叫頂點，多邊形有幾條邊就有幾個頂點。"},
           {"q": "為什麼要學邊長合起來？",
            "a": "108課綱 S-2-4：平面圖形的邊長，是三年級學「周長」的前置經驗。"}]
    make_unit(R, "grade-2", "shapes", "S-2-2",
              "簡單幾何形體：以操作活動為主。包含平面圖形與立體形體。辨認與認識三角形、四邊形、圓形、正方體、長方體、圓柱體、球體。",
              "平面圖形和立體形體",
              "二年級數學 圖形 練習題｜三角形四邊形・正方體長方體・邊長 學習單（附解答）",
              "平面圖形和立體",
              "國小二年級數學「平面圖形和立體形體」免費學習單：認識三角形、四邊形、圓形，數邊和頂點，認識正方體、長方體、圓柱、球，長方形邊長和邊長合起來。100題線上練習，圖多，附可列印解答。",
              "三角形 3 條邊，四邊形 4 條邊",
              "圖形轉了方向名字不變；正方體、長方體都有 6 個面。",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
