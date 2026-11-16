# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：平方根與根式的化簡（108課綱 N-8-1）
  python3 tools/gen_tw_math_g8_square_roots.py
平方根の意味（正の數の平方根は二つ、±）、√ の値（完全平方數・分數・小數）、√ab＝√a×√b による化簡（√72＝6√2）、最簡根式の判斷、分母の有理化。
誤答：25 の平方根を 5 だけにする、√(－4) を －2 とする、√72＝2√18 で止める、√(a²＋b²)＝a＋b とする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, num
from tw_g8 import sn, tidy_sets, rt, simp

R = random.Random(81004)
NM = Names(R)


def s1(seen):
    def mk():
        a = R.randint(2, 20)
        n = a * a
        k = R.choice(["sqrt", "root"])
        if k == "root":
            return mcq("%d 的平方根是什麼？" % n, "%d 和 －%d" % (a, a), ["%d" % a, "－%d" % a, "%d 和 －%d" % (n // 2, n // 2) if n % 2 == 0 else "%d 和 －%d" % (a + 1, a + 1)], "%d<sup>2</sup> ＝ %d，（－%d）<sup>2</sup> ＝ %d，正數有兩個平方根，互為相反數。" % (a, n, a, n))
        return mcq("√%d ＝ ？" % n, str(a), ["±%d" % a, str(n // 2) if n % 2 == 0 else str(a + 1), str(a * 2)], "√%d 表示 %d 的<b>正</b>平方根：%d。" % (n, n, a))

    def frac():
        a, b = R.randint(1, 12), R.randint(2, 15)
        if a == b:
            return None
        if R.random() < .5:
            return mcq("√（<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>）＝ ？" % (a * a, b * b), fr(a, b), [fr(a * a, b), fr(a, b * b), fr(b, a)], "分子、分母分別開方：%s。" % fr(a, b))
        d = R.choice([10, 100])
        v = F(a, d)
        sq = v * v
        def dn(x):
            return ("%.6f" % float(x)).rstrip("0").rstrip(".")
        return mcq("√%s ＝ ？" % dn(sq), dn(v), [dn(v * 10), dn(v / 10), dn(sq * 2) if sq * 2 != v else dn(v + F(1, d))], "%s × %s ＝ %s，所以 √%s ＝ %s。" % (dn(v), dn(v), dn(sq), dn(sq), dn(v)))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, frac, 8, seen)


def s2(seen):
    def mk():
        k = R.randint(2, 10)
        m = R.choice([2, 3, 5, 6, 7, 10, 11])
        n = k * k * m
        if n > 500:
            return None
        part = [d for d in range(2, k) if k % d == 0]
        w = [rt(k, m)]
        if part:
            d = part[0]
            w.append(rt(d, n // (d * d)))
        w += [rt(m, k * k), rt(k * k, m), rt(k * 2, m)]
        return mcq("化簡 √%d" % n, rt(k, m), [x for x in w[1:] if x != rt(k, m)], "%d ＝ %d<sup>2</sup> × %d，√%d ＝ %d√%d，根號裡不能再有平方數。" % (n, k, m, n, k, m))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def which():
        good = R.choice([2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22])
        bads = R.sample([8, 12, 18, 20, 24, 27, 28, 32, 45, 50, 48, 75], 3)
        opts = ["√%d" % good] + ["√%d" % b for b in bads]
        return mcq("下面哪一個是<b>最簡根式</b>？（%s）" % "、".join(sorted(opts, key=lambda s: int(s[1:]))), "√%d" % good, ["√%d" % b for b in bads],
                   "最簡根式：根號裡沒有平方數因數。%s。" % "、".join("√%d ＝ %s" % (b, rt(*simp(b))) for b in bads[:2]))

    def rat():
        a = R.randint(1, 9)
        m = R.choice([2, 3, 5, 6, 7])
        g = F(a, m)
        q = "把 <span class='fr'><span class='fn'>%d</span><span class='fd'>√%d</span></span> 的分母有理化。" % (a, m)
        if g.denominator == 1:
            ans = rt(int(g), m)
        else:
            ans = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (rt(g.numerator, m), g.denominator)
        return mcq(q, ans, ["<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (rt(a, m), m * m) if True else "", "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, m), rt(a, m)],
                   "分子、分母同乘 √%d：<span class='fr'><span class='fn'>%d√%d</span><span class='fd'>%d</span></span>%s。" % (m, a, m, m, "，再約分" if g.denominator != m else ""))
    return pick_unique(R, which, 10, seen) + pick_unique(R, rat, 10, seen)


def s4(seen):
    def mk():
        a, b = R.choice([(3, 4), (6, 8), (5, 12), (9, 12), (8, 15), (1, 1), (2, 3), (1, 3)])
        s = a * a + b * b
        k, m = simp(s)
        q = "√（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ ？" % (a, b)
        return mcq(q, rt(k, m), [str(a + b), rt(*simp(a * a)) if False else "√%d ＋ √%d" % (a * a, b * b), rt(k + 1, m) if m > 1 else str(k + 1)], ("先算根號裡：%d ＋ %d ＝ %d，√%d ＝ %s。不能拆成 %d ＋ %d。" % (a * a, b * b, s, s, rt(k, m), a, b)) if rt(k, m) != "√%d" % s else ("先算根號裡：%d ＋ %d ＝ %d，答案是 √%d。不能拆成 %d ＋ %d。" % (a * a, b * b, s, s, a, b)))

    def neg():
        n = R.choice([4, 9, 16, 25, 36])
        F_ = [("（－%d）的平方根存在嗎？" % n, "不存在（負數沒有平方根）", ["存在，是 －%d" % int(n ** .5), "存在，是 ±%d" % int(n ** .5), "存在，是 %d" % int(n ** .5)], "任何數平方都不會是負數，所以負數沒有平方根。"),
              ("√（（－%d）<sup>2</sup>）＝ ？" % int(n ** .5), str(int(n ** .5)), ["－%d" % int(n ** .5), "±%d" % int(n ** .5), str(n)], "（－%d）<sup>2</sup> ＝ %d，√%d ＝ %d（√ 的結果一定不是負數）。" % (int(n ** .5), n, n, int(n ** .5))),
              ("0 的平方根是？", "0", ["沒有", "±1", "1"], "只有 0 的平方是 0。")]
        return mcq(*R.choice(F_))
    return pick_unique(R, mk, 8, seen) + pick_unique(R, neg, 7, seen) + pick_unique(R, area, 5, seen)


def area():
    n = R.choice([18, 20, 27, 32, 45, 48, 50, 72, 75, 98])
    k, m = simp(n)
    q = "一個正方形的面積是 %d 平方公分，邊長是多少公分？（化成最簡根式）" % n
    return mcq(q, "%s 公分" % rt(k, m), ["%s 公分" % x for x in ("√%d" % (n // 2), rt(m, k), str(n // 4) if n % 4 == 0 else str(n // 2))], "邊長 ＝ √%d ＝ %s（公分）。" % (n, rt(k, m)))


def s5(seen):
    def between():
        n = R.randint(2, 150)
        a = int(n ** .5)
        if a * a == n:
            return None
        q = "√%d 介於哪兩個連續整數之間？" % n
        return mcq(q, "%d 和 %d" % (a, a + 1), ["%d 和 %d" % (a - 1, a) if a > 1 else "%d 和 %d" % (a + 1, a + 2), "%d 和 %d" % (a + 1, a + 2), "%d 和 %d" % (n // 2, n // 2 + 1) if n // 2 not in (a, a - 1, a + 1) else "%d 和 %d" % (a + 2, a + 3)], "%d<sup>2</sup> ＝ %d ＜ %d ＜ %d ＝ %d<sup>2</sup>。" % (a, a * a, n, (a + 1) ** 2, a + 1))

    def comp():
        a, m = R.randint(2, 6), R.choice([2, 3, 5])
        b = R.randint(2, 12)
        v1, v2 = a * a * m, b * b
        if v1 == v2:
            return None
        q = "%s 和 %d，哪一個比較大？" % (rt(a, m), b)
        ans = rt(a, m) if v1 > v2 else str(b)
        return mcq(q, ans, [str(b) if ans != str(b) else rt(a, m), "一樣大", "無法比較"], "都化成根號裡比：%s ＝ √%d，%d ＝ √%d。" % (rt(a, m), v1, b, v2))
    return pick_unique(R, between, 10, seen) + pick_unique(R, comp, 10, seen)


def main():
    seen = set()
    sets = [("平方根的意義", s1(seen)), ("化簡根式", s2(seen)), ("最簡根式與分母有理化", s3(seen)),
            ("易錯觀念", s4(seen)), ("比較大小", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["若 a<sup>2</sup> ＝ b，a 就是 b 的平方根。正數有<b>兩個</b>平方根，互為相反數；0 的平方根是 0；負數沒有平方根。",
         "<b>√b</b> 表示 b 的<b>正</b>平方根：√25 ＝ 5，不是 ±5。",
         "化簡：√（a<sup>2</sup> × b）＝ a√b，例如 √72 ＝ √（36 × 2）＝ 6√2。",
         "分母有根號時，分子分母同乘那個根號（分母有理化）。"],
        [example("化簡 √75", ["75 ＝ 25 × 3。"], "5√3"),
         example("<span class='fr'><span class='fn'>6</span><span class='fd'>√3</span></span> 分母有理化", ["同乘 √3：<span class='fr'><span class='fn'>6√3</span><span class='fd'>3</span></span>。"], "2√3")],
        [("25 的平方根是 5", "有兩個：5 和 －5"),
         ("√72 ＝ 2√18", "還能化簡：6√2"),
         ("√（3<sup>2</sup> ＋ 4<sup>2</sup>）＝ 3 ＋ 4", "先算裡面：√25 ＝ 5")])
    faq = [{"q": "「25 的平方根」和「√25」有什麼不同？",
            "a": "25 的平方根有兩個：5 和 －5；√25 只表示正的那一個，等於 5。"},
           {"q": "什麼是最簡根式？",
            "a": "根號裡沒有能開得盡的平方數因數，而且分母沒有根號，例如 3√2、√15。"},
           {"q": "八年級的平方根要學什麼？",
            "a": "108課綱 N-8-1：二次方根的意義、根式的化簡及四則運算。"}]
    make_unit(R, "grade-8", "square-roots", "N-8-1",
              "二次方根：二次方根的意義；根式的化簡及四則運算。",
              "平方根與根式的化簡",
              "八年級數學 平方根 練習題｜根式化簡・最簡根式・分母有理化 學習單（附解答）",
              "平方根與根式",
              "國中八年級數學「平方根與根式的化簡」免費學習單：平方根的意義、√ 的值、化簡根式、最簡根式和分母有理化、易錯觀念與比較大小。100題線上練習馬上對答案，附可列印解答。",
              "√b 是 b 的正平方根",
              "正數有兩個平方根；√（a² × b）＝ a√b。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
