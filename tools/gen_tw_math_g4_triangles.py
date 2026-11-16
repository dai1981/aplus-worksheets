# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：三角形（108課綱 S-4-7）
  python3 tools/gen_tw_math_g4_triangles.py
邊で分類（正三角形・等腰三角形）、角で分類（銳角・直角・鈍角三角形）、図から見分ける、正三角形・等腰三角形の性質と周長、性質の正誤。
誤答：1 つでも銳角があれば銳角三角形とする、正三角形は等腰三角形ではないと思う、等腰の周長で腰を 1 本しか数えない。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, GREEN, FILL

R = random.Random(41018)
NM = Names(R)
LET = "甲乙丙丁"


def tri_svg(A, B):
    """底邊を水平にして、底角 A、B（度）の三角形"""
    base = 180
    a, b = math.radians(A), math.radians(B)
    # 頂点：左 (0,0)、右 (base,0)、上 = 左から角 A、右から角 B の交点
    t = base * math.sin(b) / math.sin(a + b)
    x, y = t * math.cos(a), t * math.sin(a)
    pts = [(0, 0), (base, 0), (x, y)]
    minx = min(p[0] for p in pts)
    maxx = max(p[0] for p in pts)
    sc = min(1.0, 220 / (maxx - minx))
    H = y * sc
    P = " ".join("%.1f,%.1f" % ((px - minx) * sc + 12, H - py * sc + 12) for px, py in pts)
    return fig(svg_wrap(int((maxx - minx) * sc + 24), int(H + 24), "<polygon points='%s' fill='%s' stroke='%s' stroke-width='3'/>" % (P, FILL, GREEN), "三角形"))


def s1(seen):
    def mk():
        kind = R.choice(["eq", "iso", "iso", "sca"])
        if kind == "eq":
            a = R.randint(3, 15)
            L = (a, a, a)
        elif kind == "iso":
            a, b = R.randint(4, 15), R.randint(3, 15)
            if a == b or 2 * a <= b:
                return None
            L = tuple(R.sample([a, a, b], 3))
        else:
            L = tuple(R.sample(range(3, 16), 3))
            if sorted(L)[0] + sorted(L)[1] <= sorted(L)[2]:
                return None
        ans = {"eq": "正三角形", "iso": "等腰三角形", "sca": "三邊都不一樣長的三角形"}[kind]
        q = "三條邊長是 %d 公分、%d 公分、%d 公分的三角形是什麼三角形？" % L
        return mcq(q, ans, [x for x in ("正三角形", "等腰三角形", "三邊都不一樣長的三角形", "直角三角形") if x != ans][:3],
                   {"eq": "三條邊都一樣長，是正三角形（也是特別的等腰三角形）。", "iso": "有兩條邊一樣長，是等腰三角形。", "sca": "三條邊都不一樣長。"}[kind])
    return pick_unique(R, mk, 20, seen)


def angles(kind):
    for _ in range(100):
        if kind == "直角三角形":
            a = R.randint(20, 70)
            t = (90, a, 90 - a)
        elif kind == "鈍角三角形":
            o = R.randint(95, 150)
            a = R.randint(10, 180 - o - 10)
            t = (o, a, 180 - o - a)
        else:
            a = R.randint(35, 85)
            b = R.randint(max(35, 95 - a), 85)
            c = 180 - a - b
            if not (0 < c < 90):
                continue
            t = (a, b, c)
        return tuple(R.sample(t, 3))


def s2(seen):
    def mk():
        kind = R.choice(["銳角三角形", "直角三角形", "鈍角三角形"])
        t = angles(kind)
        if not t or min(t) < 10 or t == (60, 60, 60):
            return None
        q = "用角來分，三個角是 %d 度、%d 度、%d 度的三角形是什麼三角形？" % t
        return mcq(q, kind, [k for k in ("銳角三角形", "直角三角形", "鈍角三角形", "正三角形") if k != kind][:3],
                   "%s。" % {"銳角三角形": "三個角都是銳角（比 90 度小），是銳角三角形", "直角三角形": "有一個角是 90 度，是直角三角形",
                            "鈍角三角形": "有一個角比 90 度大，是鈍角三角形"}[kind])
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        kind = R.choice(["銳角三角形", "直角三角形", "鈍角三角形"])
        t = angles(kind)
        if not t:
            return None
        A, B = sorted(t)[:2] if kind != "鈍角三角形" else (min(t), sorted(t)[1])
        if kind == "直角三角形":
            A, B = R.choice([(90, min(t)), (min(t), 90), (sorted(t)[1], min(t))])
        if kind == "鈍角三角形" and R.random() < .5:
            A, B = max(t), min(t)
        q = "用角來分，這個三角形是什麼三角形？（用三角板的直角比一比）" + tri_svg(A, B)
        return mcq(q, kind, [k for k in ("銳角三角形", "直角三角形", "鈍角三角形") if k != kind] + ["不能判斷"],
                   "看最大的那個角：%s，是%s。" % ({"銳角三角形": "比直角小", "直角三角形": "剛好是直角", "鈍角三角形": "比直角大"}[kind], kind))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def eq_p():
        a = R.randint(3, 25)
        if R.random() < .5:
            q = "正三角形的一條邊是 %d 公分，周長是幾公分？" % a
            return mcq(q, "%d 公分" % (3 * a), ["%d 公分" % x for x in (2 * a, 4 * a, a + 3)], "正三角形三邊一樣長：%d × 3 ＝ %d（公分）。" % (a, 3 * a))
        q = "正三角形的周長是 %d 公分，一條邊是幾公分？" % (3 * a)
        return mcq(q, "%d 公分" % a, ["%d 公分" % x for x in (3 * a // 2 if (3 * a) % 2 == 0 else a + 2, a + 1, 3 * a // 4 if (3 * a) % 4 == 0 and 3 * a // 4 != a else a - 1)], "%d ÷ 3 ＝ %d（公分）。" % (3 * a, a))

    def iso_p():
        a, b = R.randint(5, 20), R.randint(3, 20)
        if a == b or 2 * a <= b:
            return None
        if R.random() < .5:
            q = "等腰三角形兩條一樣長的邊（腰）各是 %d 公分，另一條邊（底）是 %d 公分，周長是幾公分？" % (a, b)
            P = 2 * a + b
            return mcq(q, "%d 公分" % P, ["%d 公分" % x for x in (a + b, a + 2 * b, 3 * a)], "兩條腰 ＋ 底：%d ＋ %d ＋ %d ＝ %d（公分）。" % (a, a, b, P))
        P = 2 * a + b
        q = "等腰三角形的周長是 %d 公分，底是 %d 公分，一條腰是幾公分？" % (P, b)
        return mcq(q, "%d 公分" % a, ["%d 公分" % x for x in (P - b, (P - b) // 3 if (P - b) // 3 != a else a + 1, P // 3 if P // 3 != a else a + 2)],
                   "兩條腰共 %d － %d ＝ %d（公分），一條腰 %d ÷ 2 ＝ %d（公分）。" % (P, b, P - b, P - b, a))

    def ang():
        F = [("正三角形的每一個角是幾度？", "60 度", ["90 度", "45 度", "30 度"], "正三角形三個角一樣大，每個都是 60 度。"),
             ("等腰三角形的兩個底角有什麼關係？", "一樣大", ["一個大一個小", "加起來 90 度", "一定都是直角"], "等腰三角形兩條腰一樣長，兩個底角也一樣大。")]
        return mcq(*R.choice(F))

    def iso_ang():
        b = R.choice([30, 40, 45, 50, 55, 65, 70, 75])
        q = "等腰三角形的一個底角是 %d 度，另一個底角是幾度？" % b
        return mcq(q, "%d 度" % b, ["%d 度" % x for x in (180 - 2 * b, 90 - b, 180 - b)], "等腰三角形兩個底角一樣大：%d 度。" % b)
    return pick_unique(R, eq_p, 7, seen) + pick_unique(R, iso_p, 7, seen) + pick_unique(R, ang, 2, seen) + pick_unique(R, iso_ang, 4, seen)


TRUE = ["正三角形也是等腰三角形。", "直角三角形只有一個直角。", "鈍角三角形有一個角比 90 度大。", "銳角三角形的三個角都比 90 度小。",
        "正三角形的三個角一樣大。", "有些直角三角形也是等腰三角形。"]
FALSE = ["有一個銳角的三角形就是銳角三角形。", "一個三角形可以有兩個直角。", "正三角形不是等腰三角形。", "鈍角三角形的三個角都比 90 度大。",
         "等腰三角形的三條邊一定都一樣長。", "直角三角形不可能是等腰三角形。"]


def s5(seen):
    def mk():
        ok = R.random() < .5
        ans = R.choice(TRUE if ok else FALSE)
        st = R.sample(FALSE if ok else TRUE, 3) + [ans]
        R.shuffle(st)
        k = st.index(ans)
        q = "下面哪一句話是<b>%s</b>的？<br>%s" % ("對" if ok else "錯", "<br>".join("%s：%s" % (LET[i], t) for i, t in enumerate(st)))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s：%s每個三角形都至少有兩個銳角；看最大的角決定是銳角、直角還是鈍角三角形。正三角形三邊相等，也是等腰三角形。" % (LET[k], ans))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("用邊來分類", s1(seen)), ("用角來分類", s2(seen)), ("看圖分類", s3(seen)),
            ("正三角形和等腰三角形", s4(seen)), ("三角形的性質", s5(seen))]
    body = lesson(
        ["<b>用邊分</b>：三條邊都一樣長是<b>正三角形</b>；兩條邊一樣長是<b>等腰三角形</b>。正三角形也是等腰三角形。",
         "<b>用角分</b>：三個角都是銳角是<b>銳角三角形</b>；有一個直角是<b>直角三角形</b>；有一個鈍角是<b>鈍角三角形</b>。",
         "每個三角形至少有兩個銳角，所以要看<b>最大的那個角</b>來分。",
         "正三角形三個角都是 60 度；等腰三角形兩個底角一樣大。"],
        [example("三邊 6、6、9 公分的三角形是什麼三角形？周長多少？", ["有兩邊一樣長：等腰三角形。", "6 ＋ 6 ＋ 9 ＝ 21。"], "等腰三角形，周長 21 公分"),
         example("三個角 30 度、40 度、110 度是什麼三角形？", ["最大的角 110 度比 90 度大。"], "鈍角三角形")],
        [("有一個銳角就說是銳角三角形", "三個角都是銳角才是銳角三角形"),
         ("正三角形不是等腰三角形", "正三角形至少有兩邊一樣長，也是等腰三角形"),
         ("等腰三角形周長只加一條腰", "兩條腰都要加：腰 × 2 ＋ 底")])
    faq = [{"q": "三角形怎麼分類？",
            "a": "用邊分：正三角形、等腰三角形；用角分：銳角三角形、直角三角形、鈍角三角形。一個三角形可以同時是兩種，例如直角等腰三角形。"},
           {"q": "四年級的三角形要學什麼？",
            "a": "108課綱 S-4-7：以邊與角的特徵認識正三角形、等腰三角形、直角三角形、銳角三角形、鈍角三角形，並能畫出來。"},
           {"q": "怎麼判斷銳角、直角、鈍角三角形？",
            "a": "找出最大的那個角，用三角板的直角比一比：比直角小是銳角三角形，剛好是直角三角形，比直角大是鈍角三角形。"}]
    make_unit(R, "grade-4", "triangles", "S-4-7",
              "三角形：以邊與角的特徵認識特殊三角形並能作圖。如正三角形、等腰三角形、直角三角形、銳角三角形、鈍角三角形。",
              "三角形：正三角形、等腰三角形與角的分類",
              "四年級數學 三角形 練習題｜等腰三角形・正三角形・銳角直角鈍角三角形 學習單（附解答）",
              "三角形的分類",
              "國小四年級數學「三角形」免費學習單：用邊和角分類三角形、看圖判斷、正三角形和等腰三角形的周長與角、三角形的性質。100題線上練習馬上對答案，附可列印解答。",
              "看最大的角，分銳角、直角、鈍角三角形",
              "正三角形三邊相等，也是等腰三角形。",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
