# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：數線與絕對值（108課綱 N-7-5）
  python3 tools/gen_tw_math_g7_number_line_and_absolute_value.py
含負數的數線で點を讀む・位置、絕對值（到原點的距離）、絕對值を使った大小比較、|a－b| で二點間距離、距離が k の點（二つの答え）。
誤答：|－5| を －5 とする、二點距離で絕對值を足す・引く方向を間違える、片方の答えだけにする、目盛りを 1 と決めつける。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, INK, RED
from tw_g7 import sn, par, opv, tidy_sets

R = random.Random(71002)
NM = Names(R)


def nl(lo, hi, step=1, marks=None, labels=True):
    """數線：marks = [(值, 名字)]"""
    n = (hi - lo) // step
    W = 40 + n * 34
    s = [line(14, 34, W - 6, 34, INK, 2), "<path d='M%d 29 l8 5 l-8 5' fill='none' stroke='%s' stroke-width='2'/>" % (W - 12, INK)]
    for i in range(n + 1):
        v = lo + i * step
        x = 22 + i * 34
        s.append(line(x, 28, x, 40, INK, 2 if v == 0 else 1.2))
        if labels or v == 0:
            s.append(text(x, 58, sn(v), 12))
    for v, name in marks or []:
        x = 22 + (F(v) - lo) / step * 34
        s.append("<circle cx='%.1f' cy='34' r='5' fill='%s'/>" % (x, RED))
        s.append(text(x, 20, name, 13, col=RED))
    return fig(svg_wrap(W, 66, "".join(s), "數線"))


def s1(seen):
    def mk():
        lo = R.randint(-8, -3)
        hi = lo + R.randint(8, 12)
        v = R.randint(lo + 1, hi - 1)
        if v == 0:
            return None
        g = nl(lo, hi, 1, [(v, "A")])
        return mcq("數線上 A 點表示的數是多少？" + g, sn(v), [sn(-v), sn(v + 1), sn(v - 1)], "從 0 往%s數 %d 格，A ＝ %s。" % ("右" if v > 0 else "左", abs(v), sn(v)))

    def step2():
        st = R.choice([2, 5, 10])
        lo = -st * R.randint(3, 5)
        hi = lo + st * R.randint(7, 9)
        k = R.randint(1, (hi - lo) // st - 1)
        v = lo + k * st
        if v == 0:
            return None
        g = nl(lo, hi, st, [(v, "B")], labels=False)
        q = "數線上每一格代表 %d。B 點表示的數是多少？" % st + g
        cells = v // st
        return mcq(q, sn(v), [sn(cells), sn(-v), sn(v + st)], "B 在 0 的%s邊 %d 格，%d × %d ＝ %d，B ＝ %s。" % ("右" if v > 0 else "左", abs(cells), abs(cells), st, abs(v), sn(v)))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, step2, 8, seen)


def s2(seen):
    def mk():
        v = F(R.choice([R.randint(-40, -1), R.randint(1, 40)]))
        if R.random() < .25:
            v = F(R.randint(1, 9), R.choice([2, 3, 4])) * R.choice([-1, 1])
            if v.denominator == 1:
                return None
        k = R.choice(["abs", "neg"])
        if k == "abs":
            q = "｜%s｜ ＝ ？" % sn(v)
            ans = sn(abs(v))
            w = [sn(-abs(v)), sn(v) if v > 0 else "0", sn(abs(v) + 1)]
            if v > 0:
                w = [sn(-v), sn(1 / v) if v.denominator == 1 else "0", sn(v + 1)]
            return mcq(q, ans, w, "絕對值是到原點的距離，一定不是負數：｜%s｜ ＝ %s。" % (sn(v), ans))
        q = "－｜%s｜ ＝ ？" % sn(v)
        ans = sn(-abs(v))
        return mcq(q, ans, [sn(abs(v)), sn(v) if sn(v) != ans else sn(-v), "0"], "先算 ｜%s｜ ＝ %s，再加負號：%s。" % (sn(v), sn(abs(v)), ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def which():
        a, b = R.sample(range(1, 30), 2)
        q = "－%d 和 －%d，哪一個比較大？" % (a, b)
        ans = "－%d" % min(a, b)
        return mcq(q, ans, ["－%d" % max(a, b), "一樣大", "無法比較"], "兩個負數比大小：絕對值大的反而小。｜－%d｜ ＜ ｜－%d｜，所以 －%d 比較大。" % (min(a, b), max(a, b), min(a, b)))

    def absval():
        x = R.randint(1, 15)
        q = "絕對值是 %d 的數有哪些？" % x
        return mcq(q, "%d 和 －%d" % (x, x), ["只有 %d" % x, "只有 －%d" % x, "0 和 %d" % x], "到原點距離是 %d 的點，在原點左右各一個：%d 和 －%d。" % (x, x, x))

    def cnt():
        x = R.randint(2, 9)
        q = "絕對值小於 %d 的整數有幾個？" % x
        v = 2 * x - 1
        return mcq(q, "%d 個" % v, ["%d 個" % t for t in (x - 1, 2 * x - 2, 2 * x + 1)], "從 －%d 到 %d，正的 %d 個、負的 %d 個，再加上 0：%d 個。" % (x - 1, x - 1, x - 1, x - 1, v))
    return pick_unique(R, which, 8, seen) + pick_unique(R, absval, 6, seen) + pick_unique(R, cnt, 6, seen)


def s4(seen):
    def mk():
        a, b = R.sample(range(-20, 21), 2)
        if a * b >= 0 and R.random() < .6:
            return None
        d = abs(a - b)
        q = "數線上 A（%s）和 B（%s）兩點的距離是多少？" % (sn(a), sn(b))
        return mcq(q, str(d), [str(x) for x in (abs(abs(a) - abs(b)), abs(a + b) if abs(a + b) != d else d + 2, d + 1)  if x != d] + [str(d + 2)],
                   "距離 ＝ ｜a － b｜ ＝ ｜%s%s｜ ＝ ｜%s｜ ＝ %d。" % (sn(a), opv("－", b), sn(a - b), d))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def two():
        a = R.randint(-10, 10)
        k = R.randint(2, 9)
        q = "數線上和 %s 的距離是 %d 的點是哪些數？" % (sn(a), k)
        ans = "%s 和 %s" % (sn(a - k), sn(a + k))
        return mcq(q, ans, ["只有 %s" % sn(a + k), "%s 和 %s" % (sn(-k), sn(k)), "%s 和 %s" % (sn(a - k + 1), sn(a + k - 1))], "往左 %d：%s，往右 %d：%s，共有兩個。" % (k, sn(a - k), k, sn(a + k)))

    def mid():
        a, b = R.sample(range(-20, 21), 2)
        if (a + b) % 2:
            return None
        m = (a + b) // 2
        q = "數線上 %s 和 %s 正中間的點是多少？" % (sn(a), sn(b))
        return mcq(q, sn(m), [sn(x) for x in ((b - a) // 2, -m, m + 1)  if x != m] + [sn(m - 1)], "（%s%s）÷ 2 ＝ %s。" % (sn(a), opv("＋", b), sn(m)))

    def move():
        a = R.randint(-10, 10)
        r, l = R.randint(2, 12), R.randint(2, 12)
        v = a + r - l
        q = "數線上一點從 %s 出發，先向右移動 %d 單位，再向左移動 %d 單位，最後停在哪個數？" % (sn(a), r, l)
        return mcq(q, sn(v), [sn(x) for x in (a - r + l, a + r + l, v + 1)  if x != v] + [sn(v - 1)], "向右加、向左減：%s ＋ %d － %d ＝ %s。" % (sn(a), r, l, sn(v)))
    return pick_unique(R, two, 7, seen) + pick_unique(R, mid, 7, seen) + pick_unique(R, move, 6, seen)


def main():
    seen = set()
    sets = [("讀數線上的點", s1(seen)), ("絕對值", s2(seen)), ("用絕對值比較大小", s3(seen)),
            ("數線上兩點的距離", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["數線向右延伸是正數，向左延伸是負數，中間是原點 0。越右邊的數越大。",
         "<b>絕對值</b> ｜a｜ 是 a 到原點的距離，一定 ≥ 0：｜－5｜ ＝ 5，｜5｜ ＝ 5。",
         "兩個負數比大小：<b>絕對值大的反而小</b>。",
         "數線上 a、b 兩點的距離 ＝ <b>｜a － b｜</b>。"],
        [example("A（－3）和 B（5）的距離？", ["｜－3 － 5｜ ＝ ｜－8｜。"], "8"),
         example("和 2 距離 5 的點？", ["2 － 5 ＝ －3，2 ＋ 5 ＝ 7。"], "－3 和 7")],
        [("｜－5｜ ＝ －5", "絕對值是距離，不會是負數：5"),
         ("－3 和 5 的距離是 5 － 3 ＝ 2", "｜－3 － 5｜ ＝ 8"),
         ("和 2 距離 5 的點只寫 7", "左右各一個：－3 和 7")])
    faq = [{"q": "絕對值是什麼意思？",
            "a": "一個數在數線上到原點的距離。距離不會是負的，所以絕對值一定大於或等於 0。"},
           {"q": "數線上兩點的距離怎麼算？",
            "a": "用大的數減小的數，或直接算 ｜a － b｜。例如 －4 和 6 的距離是 ｜－4 － 6｜ ＝ 10。"},
           {"q": "七年級的數線要學什麼？",
            "a": "108課綱 N-7-5：擴充至含負數的數線、比較數的大小、絕對值的意義，以 ｜a－b｜ 表示數線上兩點 a、b 的距離。"}]
    make_unit(R, "grade-7", "number-line-and-absolute-value", "N-7-5",
              "數線：擴充至含負數的數線；比較數的大小；絕對值的意義；以｜a－b｜表示數線上兩點a、b的距離。",
              "數線與絕對值",
              "七年級數學 數線與絕對值 練習題｜比較大小・兩點距離 學習單（附解答）",
              "數線與絕對值",
              "國中七年級數學「數線與絕對值」免費學習單：讀含負數的數線、絕對值、用絕對值比較大小、數線上兩點的距離 ｜a－b｜ 與距離為 k 的點、中點和移動。100題線上練習馬上對答案，附可列印解答。",
              "｜a｜ 是 a 到原點的距離",
              "兩點距離 ＝ ｜a － b｜；兩個負數比大小，絕對值大的反而小。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
