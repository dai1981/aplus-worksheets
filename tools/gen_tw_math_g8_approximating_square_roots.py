# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：平方根的近似值（108課綱 N-8-2）
  python3 tools/gen_tw_math_g8_approximating_square_roots.py
√n の整數部分、十分逼近法（小數第一位を決める）、近似值（√2≈1.414、√3≈1.732）を使った計算、大小比較、應用（正方形の邊長・電腦の√鍵）。
誤答：整數部分を n÷2 とする、十分逼近で 2 乘して比べない、√(2×100)＝10√2 の換算を誤る。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, dnum
from tw_g8 import tidy_sets, rt, simp

R = random.Random(81006)
NM = Names(R)


def s1(seen):
    def mk():
        n = R.randint(2, 400)
        a = math.isqrt(n)
        if a * a == n:
            return None
        return mcq("√%d 的整數部分是多少？" % n, str(a), [str(a + 1), str(a - 1) if a > 1 else str(a + 2), str(n // 2) if n // 2 not in (a, a + 1, a - 1) else str(a + 3)], "%d<sup>2</sup> ＝ %d ＜ %d ＜ %d ＝ %d<sup>2</sup>，所以整數部分是 %d。" % (a, a * a, n, (a + 1) ** 2, a + 1, a))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.randint(2, 99)
        a = math.isqrt(n)
        if a * a == n:
            return None
        t = math.isqrt(n * 100)
        lo, hi = t / 10, (t + 1) / 10
        q = "用十分逼近法：√%d 介於哪兩個數之間？" % n
        ans = "%s 和 %s" % (dnum(lo), dnum(hi))
        return mcq(q, ans, ["%s 和 %s" % (dnum(lo - .1), dnum(lo)), "%s 和 %s" % (dnum(hi), dnum(hi + .1)), "%d 和 %d" % (a, a + 1)],
                   "%s<sup>2</sup> ＝ %s ＜ %d ＜ %s ＝ %s<sup>2</sup>。" % (dnum(lo), dnum(lo * lo, 2), n, dnum(hi * hi, 2), dnum(hi)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    APP = {2: 1.414, 3: 1.732, 5: 2.236}

    def mk():
        m = R.choice([2, 3, 5])
        k = R.choice([2, 3, 4, 5, 10])
        n = k * k * m
        v = k * APP[m]
        q = "已知 √%d ≈ %s，√%d ≈ ？" % (m, dnum(APP[m], 3), n)
        return mcq(q, dnum(v, 3), [dnum(APP[m] * k * k, 3), dnum(APP[m] + k, 3), dnum(v / 10, 4)], "√%d ＝ %s ≈ %d × %s ＝ %s。" % (n, rt(k, m), k, dnum(APP[m], 3), dnum(v, 3)))

    def frac():
        m = R.choice([2, 3])
        q = "已知 √%d ≈ %s，<span class='fr'><span class='fn'>1</span><span class='fd'>√%d</span></span> ≈ ？（四捨五入到小數第三位）" % (m, dnum(APP[m], 3), m)
        v = round(1 / math.sqrt(m), 3)
        return mcq(q, dnum(v, 3), [dnum(APP[m] * 2, 3), dnum(round(1 / APP[m] * 10, 3), 3), dnum(APP[m] / 4, 3)], "分母有理化：<span class='fr'><span class='fn'>√%d</span><span class='fd'>%d</span></span> ≈ %s ÷ %d ≈ %s。" % (m, m, dnum(APP[m], 3), m, dnum(v, 3)))

    def hund():
        m = R.choice([2, 3, 5])
        p = R.choice([100, 10000, 400, 900])
        q = "已知 √%d ≈ %s，√%d ≈ ？" % (m, dnum(APP[m], 3), m * p)
        v = APP[m] * math.isqrt(p)
        return mcq(q, dnum(v, 3), [dnum(APP[m] * p, 3), dnum(APP[m] * math.isqrt(p) / 10, 3), dnum(APP[m] * math.isqrt(p) * 10, 3)], "√%d ＝ √%d × √%d ＝ %d√%d ≈ %s。" % (m * p, m, p, math.isqrt(p), m, dnum(v, 3)))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, frac, 2, seen) + pick_unique(R, hund, 6, seen) + pick_unique(R, big3, 2, seen)


def big3():
    m = R.choice([2, 3, 5])
    k = R.randint(2, 9)
    q = "%d√%d 介於哪兩個連續整數之間？" % (k, m)
    v = k * k * m
    a = math.isqrt(v)
    return mcq(q, "%d 和 %d" % (a, a + 1), ["%d 和 %d" % (a - 1, a), "%d 和 %d" % (a + 1, a + 2), "%d 和 %d" % (k, k + 1)], "%d√%d ＝ √%d，%d<sup>2</sup> ＜ %d ＜ %d<sup>2</sup>。" % (k, m, v, a, v, a + 1))


def s4(seen):
    def mk():
        a, b = R.sample(range(2, 60), 2)
        q = "下面四個數由小到大排列：√%d、%d、√%d、%d" % (a * a + 1 if False else a, int(math.sqrt(a)) + 1, b, int(math.sqrt(b)))
        xs = [("√%d" % a, math.sqrt(a)), (str(int(math.sqrt(a)) + 1), int(math.sqrt(a)) + 1), ("√%d" % b, math.sqrt(b)), (str(int(math.sqrt(b))), int(math.sqrt(b)))]
        vals = [v for _, v in xs]
        if len(set(round(v, 6) for v in vals)) < 4:
            return None
        s = sorted(xs, key=lambda t: t[1])
        ans = " ＜ ".join(t[0] for t in s)
        w1 = " ＜ ".join(t[0] for t in sorted(xs, key=lambda t: -t[1]))
        w2 = " ＜ ".join(t[0] for t in sorted(xs, key=lambda t: (t[0].startswith("√"), t[1])))
        w3 = " ＜ ".join(t[0] for t in sorted(xs, key=lambda t: int(t[0].replace("√", ""))))
        return mcq(q, ans, [w for w in (w1, w2, w3) if w != ans] + [" ＜ ".join(t[0] for t in s[::-1][1:] + s[-1:])], "把整數平方或把根號化成近似值再比較：%s。" % ans)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def side():
        A = R.choice([10, 20, 30, 50, 60, 80, 90, 120, 150, 200])
        v = math.sqrt(A)
        q = "一塊正方形地面積 %d 平方公尺，邊長大約是幾公尺？（四捨五入到小數第一位）" % A
        return mcq(q, "%s 公尺" % dnum(round(v, 1)), ["%s 公尺" % dnum(x) for x in (A / 4, round(v, 1) + .1, A / 2)  if round(x, 1) != round(v, 1)], "邊長 ＝ √%d ≈ %s，四捨五入得 %s 公尺。" % (A, dnum(v, 3), dnum(round(v, 1))))

    def calc():
        n = R.choice([7, 11, 13, 17, 19, 23])
        q = "用計算機的 √ 鍵算 √%d，四捨五入到小數第二位是多少？" % n
        v = round(math.sqrt(n), 2)
        return mcq(q, dnum(v, 2), [dnum(v + .01, 2), dnum(n / 2, 2), dnum(round(math.sqrt(n), 1) + .1, 2)], "√%d ≈ %s，四捨五入到小數第二位是 %s。" % (n, dnum(math.sqrt(n), 4), dnum(v, 2)))
    return pick_unique(R, side, 10, seen) + pick_unique(R, calc, 6, seen) + pick_unique(R, big3, 4, seen)


def main():
    seen = set()
    sets = [("整數部分", s1(seen)), ("十分逼近法", s2(seen)), ("用近似值計算", s3(seen)),
            ("比較大小", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["找 √n 的<b>整數部分</b>：找兩個連續整數 a、a ＋ 1，使 a<sup>2</sup> ＜ n ＜（a ＋ 1）<sup>2</sup>。",
         "<b>十分逼近法</b>：再用 a.1、a.2、… 的平方去夾，找出小數第一位，依此類推。",
         "常用近似值：<b>√2 ≈ 1.414，√3 ≈ 1.732，√5 ≈ 2.236</b>。√200 ＝ 10√2 ≈ 14.14。"],
        [example("√30 的整數部分？", ["5<sup>2</sup> ＝ 25 ＜ 30 ＜ 36 ＝ 6<sup>2</sup>。"], "5"),
         example("√30 介於哪兩個一位小數之間？", ["5.4<sup>2</sup> ＝ 29.16，5.5<sup>2</sup> ＝ 30.25。"], "5.4 和 5.5")],
        [("√30 的整數部分是 15", "要找平方最接近的整數：5"),
         ("√200 ≈ 1.414 × 100", "√200 ＝ 10√2 ≈ 14.14"),
         ("十分逼近只猜不算", "要算出平方來比較")])
    faq = [{"q": "什麼是十分逼近法？",
            "a": "先找出 √n 介於哪兩個整數之間，再把這個範圍分成十等份，用平方去比，找出小數第一位；重複下去就能得到更精確的近似值。"},
           {"q": "√2、√3 的近似值要背嗎？",
            "a": "建議記住 √2 ≈ 1.414、√3 ≈ 1.732，很多計算和估算都會用到。"},
           {"q": "八年級的近似值要學什麼？",
            "a": "108課綱 N-8-2：二次方根的近似值、整數部分、十分逼近法，以及使用計算機的 √ 鍵。"}]
    make_unit(R, "grade-8", "approximating-square-roots", "N-8-2",
              "二次方根的近似值：二次方根的近似值；二次方根的整數部分；十分逼近法。使用計算機√鍵。",
              "平方根的近似值與十分逼近法",
              "八年級數學 平方根近似值 練習題｜整數部分・十分逼近法・√2≈1.414 學習單（附解答）",
              "平方根的近似值",
              "國中八年級數學「平方根的近似值與十分逼近法」免費學習單：求平方根的整數部分、十分逼近法、用 √2、√3 的近似值計算、比較大小與正方形邊長應用。100題線上練習馬上對答案，附可列印解答。",
              "a² ＜ n ＜（a ＋ 1）²，整數部分是 a",
              "√2 ≈ 1.414，√3 ≈ 1.732。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
