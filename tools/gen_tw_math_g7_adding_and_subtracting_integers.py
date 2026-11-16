# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：正負數的加減（108課綱 N-7-3）
  python3 tools/gen_tw_math_g7_adding_and_subtracting_integers.py
同號相加（絕對值相加・符號そのまま）、異號相加（絕對值相減・絕對值の大きい方の符號）、減法＝加上相反數、連加減、分數・小數の加減と應用。
誤答：異號で符號を取り違える、a－(－b) を a－b とする、絕對值を足してしまう。
"""
import random
from fractions import Fraction as F
from decimal import Decimal as D
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, dnum
from tw_g7 import sn, par, opv, tidy_sets

R = random.Random(71003)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def mk():
        sgn = R.choice([1, -1])
        a, b = sgn * R.randint(1, 60), sgn * R.randint(1, 60)
        v = a + b
        q = "（%s）＋（%s）＝" % (sn(a), sn(b)) if sgn < 0 else "%s ＋ %s ＝" % (sn(a), sn(b))
        if sgn > 0:
            a, b = -a, -b
            v = a + b
            q = "（%s）＋（%s）＝" % (sn(a), sn(b))
        return mcq(q, sn(v), [sn(-v), sn(a - b), sn(b - a)], "同號相加：絕對值相加 %d ＋ %d ＝ %d，符號不變：%s。" % (abs(a), abs(b), abs(v), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = nz(-60, 60), nz(-60, 60)
        if (a > 0) == (b > 0) or abs(a) == abs(b):
            return None
        v = a + b
        q = "%s%s ＝" % (sn(a), opv("＋", b))
        big = a if abs(a) > abs(b) else b
        return mcq(q, sn(v), [sn(-v), sn(abs(a) + abs(b)), sn(-(abs(a) + abs(b)))],
                   "異號相加：絕對值大減小 %d － %d ＝ %d，取絕對值大的 %s 的符號：%s。" % (max(abs(a), abs(b)), min(abs(a), abs(b)), abs(v), sn(big), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = nz(-50, 50), nz(-50, 50)
        v = a - b
        q = "%s%s ＝" % (sn(a), opv("－", b))
        return mcq(q, sn(v), [sn(a + b), sn(-v), sn(-a - b)], "減去一個數，等於加上它的相反數：%s%s ＝ %s。" % (sn(a), opv("＋", -b), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        xs = [nz(-30, 30) for _ in range(R.choice([3, 4]))]
        ops = [R.choice(["＋", "－"]) for _ in xs[1:]]
        v = xs[0]
        expr = sn(xs[0])
        for o, x in zip(ops, xs[1:]):
            v = v + x if o == "＋" else v - x
            expr += opv(o, x)
        alt = xs[0]
        for o, x in zip(ops, xs[1:]):
            alt = alt + abs(x) if o == "＋" else alt - abs(x)
        return mcq("%s ＝" % expr, sn(v), [sn(x) for x in (alt, -v, v + 2)  if x != v] + [sn(v - 2)],
                   "把減法都改成加上相反數，再把正數、負數分別加起來：%s。" % sn(v))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def frac():
        a = F(R.randint(1, 9), R.choice([2, 3, 4, 6])) * R.choice([1, -1])
        b = F(R.randint(1, 9), R.choice([2, 3, 4, 6])) * R.choice([1, -1])
        op = R.choice(["＋", "－"])
        v = a + b if op == "＋" else a - b
        if a.denominator == 1 or b.denominator == 1:
            return None
        return mcq("%s%s ＝" % (sn(a), opv(op, b)), sn(v), [sn(-v), sn(a - b if op == "＋" else a + b), sn(v + 1)], "先通分再計算：%s。" % sn(v))

    def dec():
        a = D(R.randint(-99, 99)) / 10
        b = D(R.randint(-99, 99)) / 10
        if a == 0 or b == 0:
            return None
        v = a - b
        f = lambda x: ("－" + dnum(float(-x))) if x < 0 else dnum(float(x))
        pf = lambda x: "（%s）" % f(x) if x < 0 else f(x)
        return mcq("%s －%s ＝" % (f(a), pf(b)), f(v), [f(a + b), f(-v), f(v + 1)], "%s ＋%s ＝ %s。" % (f(a), pf(-b), f(v)))

    def word():
        start = R.randint(-8, 5)
        up, down = R.randint(2, 12), R.randint(3, 15)
        v = start + up - down
        q = "早上氣溫 %s ℃，中午上升 %d ℃，晚上又下降 %d ℃。晚上的氣溫是幾度？" % (sn(start), up, down)
        return mcq(q, "%s ℃" % sn(v), ["%s ℃" % sn(x) for x in (start - up + down, start + up + down, -v)  if x != v] + ["%s ℃" % sn(v + 1)], "%s ＋ %d － %d ＝ %s（℃）。" % (sn(start), up, down, sn(v)))
    return pick_unique(R, frac, 7, seen) + pick_unique(R, dec, 7, seen) + pick_unique(R, word, 6, seen)


def main():
    seen = set()
    sets = [("同號相加", s1(seen)), ("異號相加", s2(seen)), ("減法：加上相反數", s3(seen)),
            ("連加減", s4(seen)), ("分數、小數和應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>同號相加</b>：絕對值相加，符號不變。（－3）＋（－5）＝ －8。",
         "<b>異號相加</b>：絕對值大的減小的，取絕對值較大那個數的符號。（－9）＋ 4 ＝ －5。",
         "<b>減去一個數 ＝ 加上它的相反數</b>：3 －（－7）＝ 3 ＋ 7 ＝ 10。"],
        [example("（－12）＋ 7", ["異號：12 － 7 ＝ 5。", "12 比較大，取負號。"], "－5"),
         example("－4 －（－9）", ["－4 ＋ 9。"], "5")],
        [("（－9）＋ 4 ＝ 5", "絕對值大的是 －9，答案取負號：－5"),
         ("3 －（－7）＝ 3 － 7", "減負數變成加：3 ＋ 7 ＝ 10"),
         ("（－3）＋（－5）＝ 8", "同號相加，符號不變：－8")])
    faq = [{"q": "正負數加法怎麼判斷答案的正負？",
            "a": "同號就用原來的符號；異號就看絕對值誰大，答案和絕對值大的那個同號。"},
           {"q": "為什麼減去負數會變成加？",
            "a": "減去一個數等於加上它的相反數，－7 的相反數是 7，所以 3 －（－7）＝ 3 ＋ 7。"},
           {"q": "七年級的加減要學什麼？",
            "a": "108課綱 N-7-3：負數與數的四則混合運算（含分數、小數），先從正負數的加減開始。"}]
    make_unit(R, "grade-7", "adding-and-subtracting-integers", "N-7-3",
              "負數與數的四則混合運算（含分數、小數）：使用「正、負」表徵生活中的量；相反數；數的四則混合運算。",
              "正負數的加減",
              "七年級數學 正負數加減 練習題｜同號・異號・減法變加法 學習單（附解答）",
              "正負數的加減",
              "國中七年級數學「正負數的加減」免費學習單：同號相加、異號相加、減去一個數等於加上相反數、連加減與分數、小數和氣溫應用題。100題線上練習馬上對答案，附可列印解答。",
              "減去一個數 ＝ 加上它的相反數",
              "同號相加符號不變；異號相加取絕對值大的符號。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
