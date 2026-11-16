# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：四邊形（正方形、長方形、平行四邊形、菱形、梯形）（108課綱 S-4-8）
  python3 tools/gen_tw_math_g4_quadrilaterals.py
図で見分ける、特徴から名前を言う、平行・等しい邊・直角の数、包含関係（正方形は菱形でも長方形でもある）、周長の計算。
誤答：菱形を正方形とする（角を見ない）、梯形に平行な邊が2組あるとする、正方形は平行四邊形ではないと思う。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, FILL

R = random.Random(41019)
NM = Names(R)
LET = "甲乙丙丁"
NAME = {"square": "正方形", "rect": "長方形", "para": "平行四邊形", "rhombus": "菱形", "trap": "梯形"}


def quad(kind, x, y, s):
    if kind == "square":
        a = s * R.choice([.7, .8])
        return [(x, y), (x + a, y), (x + a, y + a), (x, y + a)]
    if kind == "rect":
        w, h = s, s * R.choice([.45, .55])
        return [(x, y + 10), (x + w, y + 10), (x + w, y + 10 + h), (x, y + 10 + h)]
    if kind == "rhombus":
        a = s * .45
        return [(x + a, y), (x + 2 * a, y + a * .7), (x + a, y + 1.4 * a), (x, y + a * .7)]
    if kind == "para":
        o = s * .28
        return [(x + o, y + 10), (x + s, y + 10), (x + s - o, y + 10 + s * .5), (x, y + 10 + s * .5)]
    o = s * R.choice([.15, .25])
    return [(x + o, y + 10), (x + s - o * 1.6, y + 10), (x + s, y + 10 + s * .55), (x, y + 10 + s * .55)]


def four(kinds):
    s = []
    for i, k in enumerate(kinds):
        x = 14 + i * 120
        pts = quad(k, x, 30, 96)
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN))
        s.append(text(x + 45, 20, LET[i], 16))
    return fig(svg_wrap(490, 130, "".join(s), "甲乙丙丁四個四邊形"))


def s1(seen):
    def mk():
        target = R.choice(list(NAME))
        pool = [k for k in NAME if k != target]
        if target == "rhombus":
            pool = [k for k in pool if k != "square"]
        if target == "para":
            pool = [k for k in pool if k not in ("rect", "rhombus", "square")] + ["trap"]
        if target == "rect":
            pool = [k for k in pool if k != "square"]
        others = R.sample(pool, 3) if len(set(pool)) >= 3 else None
        if not others or len(set(others)) < 3 and target != "para":
            return None
        kinds = others + [target]
        R.shuffle(kinds)
        k = kinds.index(target)
        q = "哪一個是<b>%s</b>？" % NAME[target] + four(kinds)
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], {
            "square": "正方形：4 邊一樣長，4 個直角。", "rect": "長方形：4 個直角，對邊一樣長。", "para": "平行四邊形：兩組對邊分別平行。",
            "rhombus": "菱形：4 邊一樣長，但角不一定是直角。", "trap": "梯形：只有一組對邊平行。"}[target])
    return pick_unique(R, mk, 20, seen)


DESC = [("4 條邊一樣長，4 個角都是直角", "正方形"), ("4 個角都是直角，對邊一樣長（相鄰兩邊不一樣長）", "長方形"),
        ("4 條邊一樣長，但沒有直角", "菱形"), ("兩組對邊分別平行，沒有直角，相鄰兩邊不一樣長", "平行四邊形"),
        ("只有一組對邊平行", "梯形"), ("兩組對邊平行，4 條邊一樣長，4 個角都是直角", "正方形"),
        ("兩組對邊平行，4 個角都是直角，長和寬不一樣", "長方形"), ("只有一組平行的邊，而且有兩個直角", "梯形")]


def s2(seen):
    def mk():
        d, ans = R.choice(DESC)
        pre = R.choice(["一個四邊形", "有一個四邊形", "這個四邊形"])
        q = "%s：%s。它是什麼圖形？" % (pre, d)
        return mcq(q, ans, [x for x in ("正方形", "長方形", "菱形", "平行四邊形", "梯形") if x != ans][:3] if ans != "梯形" else ["平行四邊形", "長方形", "菱形"],
                   "%s：%s。" % (ans, d))
    return pick_unique(R, mk, 20, seen)


PROP = {"正方形": (2, 4, "4 條"), "長方形": (2, 4, "對邊"), "菱形": (2, 0, "4 條"), "平行四邊形": (2, 0, "對邊"), "梯形": (1, 0, "不一定")}


def s3(seen):
    def mk():
        name = R.choice(list(PROP))
        par, ra, eq = PROP[name]
        ask = R.choice(["par", "ra"])
        if ask == "par":
            q = "%s有幾組平行的邊？" % name
            return mcq(q, "%d 組" % par, ["%d 組" % x for x in (0, 1, 2, 4) if x != par][:3], "%s：%s。" % (name, "兩組對邊都平行" if par == 2 else "只有一組對邊平行"))
        q = "%s%s有幾個直角？" % ("" if name in ("正方形", "長方形") else "一般的", name)
        return mcq(q, "%d 個" % ra, ["%d 個" % x for x in (0, 1, 2, 4) if x != ra][:3], "%s%s。" % (name, "的 4 個角都是直角" if ra == 4 else "的角一般不是直角"))

    def eq():
        name = R.choice(["正方形", "長方形", "菱形", "平行四邊形"])
        q = "%s的邊有什麼特徵？" % name
        ans = "4 條邊都一樣長" if PROP[name][2] == "4 條" else "相對的兩條邊一樣長"
        w = ["4 條邊都一樣長", "相對的兩條邊一樣長", "4 條邊都不一樣長", "只有兩條邊一樣長，而且是相鄰的"]
        return mcq(q, ans, [x for x in w if x != ans], "%s：%s。" % (name, ans))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, eq, 4, seen) + extra(seen)


def extra(seen):
    F = [("梯形和平行四邊形最大的不同是什麼？", "梯形只有一組平行的邊", ["梯形沒有直角", "梯形的邊都一樣長", "梯形有 5 條邊"], "平行四邊形兩組對邊平行，梯形只有一組。"),
         ("菱形和正方形最大的不同是什麼？", "菱形的角不一定是直角", ["菱形的邊不一樣長", "菱形沒有平行的邊", "菱形有 3 條邊"], "兩個都是 4 邊等長，正方形的 4 個角都是直角。"),
         ("長方形和平行四邊形都有的特徵是什麼？", "兩組對邊分別平行", ["4 個角都是直角", "4 條邊一樣長", "只有一組平行的邊"], "長方形也是平行四邊形，都有兩組平行的對邊。"),
         ("正方形和菱形都有的特徵是什麼？", "4 條邊一樣長", ["4 個角都是直角", "只有一組平行的邊", "沒有平行的邊"], "正方形和菱形都是 4 邊等長。"),
         ("正方形和長方形都有的特徵是什麼？", "4 個角都是直角", ["4 條邊一樣長", "只有一組平行的邊", "沒有平行的邊"], "正方形和長方形的 4 個角都是直角。"),
         ("下面哪一個四邊形一定有直角？", "長方形", ["菱形", "平行四邊形", "梯形"], "長方形 4 個角都是直角。")]
    out = []
    for f in F:
        it = mcq(*f)
        if it["q"] not in seen:
            seen.add(it["q"])
            out.append(it)
    return out


TRUE = ["正方形也是長方形。", "正方形也是菱形。", "長方形也是平行四邊形。", "菱形也是平行四邊形。", "梯形只有一組平行的邊。", "正方形的兩組對邊都平行。"]
FALSE = ["正方形不是平行四邊形。", "菱形的 4 個角一定都是直角。", "梯形有兩組平行的邊。", "長方形的 4 條邊一定一樣長。", "平行四邊形一定有直角。", "菱形不是平行四邊形。"]


def s4(seen):
    def mk():
        ok = R.random() < .5
        ans = R.choice(TRUE if ok else FALSE)
        st = R.sample(FALSE if ok else TRUE, 3) + [ans]
        R.shuffle(st)
        k = st.index(ans)
        q = "下面哪一句話是<b>%s</b>的？<br>%s" % ("對" if ok else "錯", "<br>".join("%s：%s" % (LET[i], t) for i, t in enumerate(st)))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s：%s正方形、長方形、菱形都有兩組平行的對邊，都是特別的平行四邊形；梯形只有一組平行的邊。" % (LET[k], ans))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def rh():
        a = R.randint(3, 25)
        if R.random() < .5:
            return mcq("菱形的一條邊是 %d 公分，周長是幾公分？" % a, "%d 公分" % (4 * a), ["%d 公分" % x for x in (2 * a, 3 * a, a * a if a * a != 4 * a else a + 4)], "菱形 4 邊一樣長：%d × 4 ＝ %d（公分）。" % (a, 4 * a))
        return mcq("菱形的周長是 %d 公分，一條邊是幾公分？" % (4 * a), "%d 公分" % a, ["%d 公分" % x for x in (2 * a, a + 4, 4 * a // 3 if (4 * a) % 3 == 0 else a + 1)], "%d ÷ 4 ＝ %d（公分）。" % (4 * a, a))

    def pa():
        a, b = R.randint(5, 25), R.randint(3, 20)
        if a == b:
            return None
        if R.random() < .5:
            P = 2 * (a + b)
            return mcq("平行四邊形相鄰的兩條邊是 %d 公分和 %d 公分，周長是幾公分？" % (a, b), "%d 公分" % P, ["%d 公分" % x for x in (a + b, a * b if a * b != P else P + 2, 2 * a + b)],
                       "對邊一樣長：（%d ＋ %d）× 2 ＝ %d（公分）。" % (a, b, P))
        P = 2 * (a + b)
        return mcq("平行四邊形的周長是 %d 公分，一條邊是 %d 公分，相鄰的另一條邊是幾公分？" % (P, a), "%d 公分" % b, ["%d 公分" % x for x in (P - a, P // 2, P - 2 * a if P - 2 * a > 0 and P - 2 * a != b else b + 2)],
                   "%d ÷ 2 ＝ %d，%d － %d ＝ %d（公分）。" % (P, P // 2, P // 2, a, b))

    def tr():
        a, b, c, d = R.randint(4, 12), R.randint(8, 20), R.randint(4, 12), R.randint(4, 12)
        q = "梯形的上底 %d 公分、下底 %d 公分，兩條斜邊是 %d 公分和 %d 公分，周長是幾公分？" % (a, b, c, d)
        P = a + b + c + d
        return mcq(q, "%d 公分" % P, ["%d 公分" % x for x in (a + b, 2 * (a + b), P + c, P - d)], "4 條邊加起來：%d ＋ %d ＋ %d ＋ %d ＝ %d（公分）。" % (a, b, c, d, P))
    return pick_unique(R, rh, 7, seen) + pick_unique(R, pa, 7, seen) + pick_unique(R, tr, 6, seen)


def main():
    seen = set()
    sets = [("看圖認四邊形", s1(seen)), ("從特徵說名稱", s2(seen)), ("四邊形的特徵", s3(seen)),
            ("四邊形之間的關係", s4(seen)), ("周長的計算", s5(seen))]
    body = lesson(
        ["<b>平行四邊形</b>：兩組對邊分別平行，對邊一樣長。<b>梯形</b>：只有一組對邊平行。",
         "<b>長方形</b>：4 個直角的平行四邊形。<b>菱形</b>：4 邊一樣長的平行四邊形。<b>正方形</b>：4 邊一樣長、4 個直角。",
         "正方形既是長方形，也是菱形；長方形、菱形、正方形都是平行四邊形。"],
        [example("4 邊都是 5 公分，但沒有直角的四邊形是什麼？周長多少？", ["4 邊等長、沒有直角：菱形。", "5 × 4 ＝ 20。"], "菱形，周長 20 公分"),
         example("平行四邊形相鄰兩邊 8 公分和 5 公分，周長多少？", ["對邊一樣長。", "（8 ＋ 5）× 2 ＝ 26。"], "26 公分")],
        [("4 邊一樣長就是正方形", "還要 4 個直角；沒有直角的是菱形"),
         ("梯形有兩組平行的邊", "梯形只有一組平行的邊"),
         ("正方形不是平行四邊形", "正方形兩組對邊都平行，是特別的平行四邊形")])
    faq = [{"q": "正方形、長方形、菱形、平行四邊形、梯形怎麼分？",
            "a": "先看平行：一組平行是梯形，兩組平行是平行四邊形。平行四邊形中，有直角的是長方形，4 邊等長的是菱形，兩個都符合的是正方形。"},
           {"q": "四年級的四邊形要學什麼？",
            "a": "108課綱 S-4-8：以邊與角的特徵（含平行）認識正方形、長方形、平行四邊形、菱形、梯形，並能畫出來。"},
           {"q": "為什麼正方形也是菱形？",
            "a": "菱形的條件是 4 條邊一樣長；正方形 4 邊一樣長，所以也是菱形，只是角剛好都是直角。"}]
    make_unit(R, "grade-4", "quadrilaterals", "S-4-8",
              "四邊形：以邊與角的特徵（含平行）認識特殊四邊形並能作圖。如正方形、長方形、平行四邊形、菱形、梯形。",
              "四邊形：平行四邊形、菱形、梯形",
              "四年級數學 四邊形 練習題｜平行四邊形・菱形・梯形・正方形 學習單（附解答）",
              "四邊形的分類",
              "國小四年級數學「四邊形」免費學習單：看圖認出正方形、長方形、平行四邊形、菱形、梯形，從特徵說名稱，四邊形之間的關係和周長。100題線上練習馬上對答案，附可列印解答。",
              "先看有幾組平行的邊",
              "正方形既是長方形，也是菱形，都是平行四邊形。",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
