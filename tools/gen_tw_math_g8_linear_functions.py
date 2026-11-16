# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：一次函數及其圖形（108課綱 F-8-1、F-8-2）
  python3 tools/gen_tw_math_g8_linear_functions.py
函數値（代入）、一次函數・常數函數の判斷、對應が函數かどうか、二點・表から y ＝ ax ＋ b、グラフを讀む（截距・通過する象限・點が上にあるか）、生活の應用。
誤答：a と b の取り違え、x 截距と y 截距の取り違え、常數函數を函數でないとする、x² を一次とする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table, num
from tw_g7 import sn, par, tidy_sets, lin
from tw_g7_grid import plane
from tw_common import BLUE

R = random.Random(81017)
NM = Names(R)
N = 6


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def yf(a, b):
    return "y ＝ " + lin(a, b)


def clip(a, b):
    """y＝ax＋b を [-N, N]² に切る"""
    ps = []
    for x in (-N, N):
        y = a * x + b
        if -N <= y <= N:
            ps.append((F(x), F(y)))
    if a:
        for y in (-N, N):
            x = F(y - b, 1) / a
            if -N <= x <= N:
                ps.append((x, F(y)))
    ps = sorted(set(ps))
    return ps[0], ps[-1]


def graph(a, b, pts=()):
    p, q = clip(F(a), F(b))
    return plane(N, pts, [((float(p[0]), float(p[1])), (float(q[0]), float(q[1])), BLUE)])


def s1(seen):
    def val():
        a, b = nz(-6, 6), R.randint(-12, 12)
        x = R.randint(-8, 8)
        v = a * x + b
        q = "一次函數 %s，當 x ＝ %s 時，y 是多少？" % (yf(a, b), sn(x))
        return mcq(q, sn(v), [sn(a * x - b), sn(a + x + b), sn(-a * x + b), sn(a * b + x)], "代入：y ＝ %s × %s%s ＝ %s。" % (sn(a), par(x), (" ＋ %d" % b) if b > 0 else (" － %d" % -b) if b else "", sn(v)))

    def tab():
        a, b = nz(-5, 5), R.randint(-9, 9)
        xs = [-1, 0, 1, 2, 3]
        k = R.randrange(5)
        row = [sn(a * x + b) if i != k else "□" for i, x in enumerate(xs)]
        t = table(["x"] + [sn(x) for x in xs], [["y"] + row])
        v = a * xs[k] + b
        q = "下表是 %s 的對應值，□ 是多少？" % yf(a, b) + t
        return mcq(q, sn(v), [sn(v + a), sn(v - a), sn(-v) if v else "1", sn(a * xs[k] - b)], "x ＝ %s 代入：%s × %s%s ＝ %s。" % (sn(xs[k]), sn(a), par(xs[k]), (" ＋ %d" % b) if b > 0 else (" － %d" % -b) if b else "", sn(v)))
    return pick_unique(R, val, 12, seen) + pick_unique(R, tab, 8, seen)


KINDS = [
    ("y ＝ %dx ＋ %d", "一次函數"), ("y ＝ %d", "常數函數"),
]


def s2(seen):
    def kind():
        t = R.choice(["lin", "const", "lin0", "no"])
        c = nz(-9, 9)
        a = nz(-6, 6)
        if t == "lin":
            f, ans = yf(a, c), "一次函數"
        elif t == "lin0":
            f, ans = yf(a, 0), "一次函數"
        elif t == "const":
            f, ans = "y ＝ %s" % sn(c), "常數函數"
        else:
            f, ans = R.choice(["y ＝ x<sup>2</sup>%s" % ((" ＋ %d" % c) if c > 0 else (" － %d" % -c)), "y ＝ <span class='fr'><span class='fn'>%d</span><span class='fd'>x</span></span>" % abs(c)]), "都不是"
        q = "%s 是哪一種函數？" % f
        return mcq(q, ans, ["一次函數", "常數函數", "都不是", "二元一次方程式，不是函數"],
                   {"一次函數": "可以寫成 y ＝ ax ＋ b，且 a ≠ 0，是一次函數。", "常數函數": "不管 x 是多少，y 都是 %s，是常數函數。" % sn(c), "都不是": "有 x<sup>2</sup> 或 x 在分母，不是一次函數也不是常數函數。"}[ans])

    PAIRS = [("正方形的邊長 x 和周長 y", True, "周長 ＝ 4 × 邊長，每個 x 只對應一個 y。"),
             ("一個人的年齡 x 和身高 y", False, "同一個年齡的人有很多種身高，一個 x 不只對應一個 y。"),
             ("買 x 枝 15 元的筆，總價 y 元", True, "y ＝ 15x，每個 x 只對應一個 y。"),
             ("圓的半徑 x 和周長 y", True, "y ＝ 2πx，每個 x 只對應一個 y。"),
             ("班上同學的座號 x 和數學成績 y", True, "每個座號只有一個成績。"),
             ("一個正數 x 和它的平方根 y", False, "正數有兩個平方根（正負），一個 x 對應兩個 y。"),
             ("身高 x 公分和同身高同學的體重 y 公斤", False, "同樣身高的同學體重可能不同。")]

    out = []
    for desc, ok, why in PAIRS:
        out.append(mcq("「%s」，y 是 x 的函數嗎？" % desc, "是" if ok else "不是", ["不是" if ok else "是", "只有 x 是整數時才是", "不能判斷"],
                       "函數：每一個 x 都只對應到一個 y。" + why))
    for b in out:
        seen.add(b["q"])
    return out + pick_unique(R, kind, 13, seen)


def s3(seen):
    def two():
        a, b = nz(-4, 4), R.randint(-8, 8)
        x1, x2 = sorted(R.sample(range(-5, 6), 2))
        y1, y2 = a * x1 + b, a * x2 + b
        q = "一次函數 y ＝ ax ＋ b 的圖形通過（%s，%s）和（%s，%s），這個函數是？" % (sn(x1), sn(y1), sn(x2), sn(y2))
        return mcq(q, yf(a, b), [yf(-a, b), yf(a, -b) if b else yf(a, 1), yf(b, a) if b else yf(a, 2), yf(a, y1)],
                   "a ＝（%s － %s）÷（%s － %s）＝ %s；代入（%s，%s）得 b ＝ %s，所以 %s。" % (sn(y2), par(y1), sn(x2), par(x1), sn(a), sn(x1), sn(y1), sn(b), yf(a, b)))

    def tb():
        a, b = nz(-5, 5), R.randint(-9, 9)
        xs = [0, 1, 2, 3]
        t = table(["x"] + [str(x) for x in xs], [["y"] + [sn(a * x + b) for x in xs]])
        q = "下表的 x、y 是一次函數關係，它是？" + t
        return mcq(q, yf(a, b), [yf(b, a) if b else yf(a, 1), yf(a, b + a), yf(-a, b), yf(a, -b) if b else yf(a, -1)],
                   "x ＝ 0 時 y ＝ %s，所以 b ＝ %s；x 每加 1，y 變化 %s，所以 a ＝ %s：%s。" % (sn(b), sn(b), sn(a), sn(a), yf(a, b)))
    return pick_unique(R, two, 10, seen) + pick_unique(R, tb, 10, seen)


def s4(seen):
    def read():
        a, b = R.choice([F(1), F(2), F(-1), F(-2), F(1, 2), F(-1, 2), F(3), F(-3)]), R.randint(-4, 4)
        g = graph(a, b)
        q = "下圖是哪一個一次函數的圖形？" + g
        return mcq(q, yf(a, b), [yf(-a, b), yf(a, -b) if b else yf(a, 1), yf(b, a) if b else yf(2 * a, 0), yf(a, b + 1)],
                   "看 y 軸：通過（0，%s），b ＝ %s；x 往右 %d 格，y 變化 %s，a ＝ %s。" % (sn(b), sn(b), F(a).denominator, sn(F(a) * F(a).denominator), sn(a)))

    def icpt():
        a, b = nz(-4, 4), nz(-8, 8)
        if F(-b, a).denominator != 1:
            return None
        xi = -b // a
        k = R.choice(["x", "y"])
        if k == "y":
            q = "%s 的圖形和 y 軸交於哪一點？" % yf(a, b)
            ans = "（0，%s）" % sn(b)
            w = ["（%s，0）" % sn(b), "（0，%s）" % sn(a), "（%s，0）" % sn(xi), "（0，%s）" % sn(-b)]
            e = "和 y 軸的交點 x ＝ 0：y ＝ %s，交點（0，%s）。" % (sn(b), sn(b))
        else:
            q = "%s 的圖形和 x 軸交於哪一點？" % yf(a, b)
            ans = "（%s，0）" % sn(xi)
            w = ["（0，%s）" % sn(b), "（%s，0）" % sn(b), "（%s，0）" % sn(-xi) if xi else "（1，0）", "（0，%s）" % sn(xi)]
            e = "和 x 軸的交點 y ＝ 0：%s ＝ 0，x ＝ %s，交點（%s，0）。" % (lin(a, b), sn(xi), sn(xi))
        return mcq(q, ans, w, e)

    def onl():
        a, b = nz(-4, 4), R.randint(-6, 6)
        x = R.randint(-5, 5)
        good = "（%s，%s）" % (sn(x), sn(a * x + b))
        bad = ["（%s，%s）" % (sn(x), sn(a * x + b + d)) for d in (1, -2, 3)] + ["（%s，%s）" % (sn(a * x + b), sn(x))]
        q = "下面哪一點在 %s 的圖形上？" % yf(a, b)
        bad = [p for p in bad if p != good]
        return mcq(q, good, bad, "把 x ＝ %s 代入，y ＝ %s，所以 %s 在圖形上。" % (sn(x), sn(a * x + b), good))
    return pick_unique(R, read, 8, seen) + pick_unique(R, icpt, 6, seen) + pick_unique(R, onl, 6, seen)


def s5(seen):
    def taxi():
        base, per = R.choice([(85, 5), (70, 5), (100, 5)]), None
        b, a = base
        n = R.randint(4, 30)
        q = "計程車起跳 %d 元，之後每 200 公尺加 %d 元。設加了 x 次 200 公尺，車資 y 元，y ＝ %dx ＋ %d。加 %d 次要付多少元？" % (b, a, a, b, n)
        v = a * n + b
        return mcq(q, "%d 元" % v, ["%d 元" % x for x in (b * n + a, a * n, v + a, (a + b) * n)], "y ＝ %d × %d ＋ %d ＝ %d（元）。" % (a, n, b, v))

    def candle():
        L = R.choice([20, 24, 30])
        r = R.choice([2, 3])
        t = R.randint(2, L // r - 1)
        q = "一根蠟燭長 %d 公分，點燃後每小時短 %d 公分。點了 x 小時後剩 y 公分，y 和 x 的關係是？點 %d 小時後剩多少？" % (L, r, t)
        v = L - r * t
        return mcq(q, "y ＝ %d － %dx，剩 %d 公分" % (L, r, v), ["y ＝ %d ＋ %dx，剩 %d 公分" % (L, r, L + r * t), "y ＝ %dx － %d，剩 %d 公分" % (L, r, L * t - r), "y ＝ %d － %dx，剩 %d 公分" % (r, L, r * t)],
                   "每小時少 %d，y ＝ %d － %dx；x ＝ %d，y ＝ %d。" % (r, L, r, t, v))

    def phone():
        b = R.choice([99, 199, 299])
        a = R.choice([2, 3, 5])
        y = b + a * R.randint(10, 60)
        x = (y - b) // a
        q = "手機月租 %d 元，每通話 1 分鐘再加 %d 元。這個月付了 %d 元，通話幾分鐘？" % (b, a, y)
        return mcq(q, "%d 分鐘" % x, ["%d 分鐘" % v for v in (y // a, x + 1, (y + b) // a, x - 1)], "y ＝ %dx ＋ %d，%d ＝ %dx ＋ %d，x ＝ %d。" % (a, b, y, a, b, x))
    return pick_unique(R, taxi, 7, seen) + pick_unique(R, candle, 7, seen) + pick_unique(R, phone, 6, seen)


def main():
    seen = set()
    sets = [("函數值", s1(seen)), ("認識函數", s2(seen)), ("求一次函數", s3(seen)),
            ("一次函數的圖形", s4(seen)), ("生活中的一次函數", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["每一個 x 都只對應到一個 y，就說 <b>y 是 x 的函數</b>。",
         "<b>一次函數</b>：y ＝ ax ＋ b（a ≠ 0），圖形是一條斜直線。<b>常數函數</b>：y ＝ c，圖形是水平線。",
         "<b>b</b> 是圖形和 y 軸交點的 y 坐標；<b>a</b> 是 x 增加 1 時 y 的變化量，a ＞ 0 往右上，a ＜ 0 往右下。",
         "和 x 軸的交點：令 y ＝ 0；和 y 軸的交點：令 x ＝ 0。"],
        [example("y ＝ 2x － 3，x ＝ 4 時 y？", ["2 × 4 － 3 ＝ 5。"], "5"),
         example("圖形通過（0，1）和（2，7），求一次函數", ["b ＝ 1。", "x 加 2，y 加 6，a ＝ 3。"], "y ＝ 3x ＋ 1")],
        [("把 y ＝ 5 當成不是函數", "y ＝ 5 是常數函數，也是函數"),
         ("y ＝ 2x － 3 和 y 軸交於（－3，0）", "和 y 軸交點 x ＝ 0：（0，－3）"),
         ("y ＝ x<sup>2</sup> ＋ 1 是一次函數", "有 x<sup>2</sup>，不是一次函數")])
    faq = [{"q": "函數和方程式有什麼不同？",
            "a": "函數強調對應：給一個 x 就得到唯一的 y。像 y ＝ 2x ＋ 1 可以看成函數，也可以看成二元一次方程式，圖形都是同一條直線。"},
           {"q": "怎麼看一次函數的圖形是往上還是往下？",
            "a": "看 x 的係數 a：a ＞ 0 時 x 越大 y 越大（往右上），a ＜ 0 時往右下。"},
           {"q": "八年級的函數要學什麼？",
            "a": "108課綱 F-8-1、F-8-2：透過對應關係認識函數、常數函數 y ＝ c、一次函數 y ＝ ax ＋ b，以及它們的圖形。"}]
    make_unit(R, "grade-8", "linear-functions", "F-8-1",
              "一次函數：透過對應關係認識函數（不要出現 f(x) 的抽象型式）、常數函數（y ＝ c）、一次函數（y ＝ ax ＋ b）。",
              "一次函數及其圖形",
              "八年級數學 一次函數 練習題｜函數值・常數函數・圖形與截距 學習單（附解答）",
              "一次函數",
              "國中八年級數學「一次函數及其圖形」免費學習單：函數值、認識函數與常數函數、用兩點或表格求 y＝ax＋b、讀一次函數的圖形和交點、計程車與蠟燭應用題。100題線上練習馬上對答案，附可列印解答。",
              "y ＝ ax ＋ b",
              "b 是和 y 軸交點的 y 坐標；a 是 x 加 1 時 y 的變化。",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
