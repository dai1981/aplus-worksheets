# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：指數的意義（108課綱 N-7-6）
  python3 tools/gen_tw_math_g7_exponents.py
次方＝同じ數の連乘（底數・指數）、負數の次方（偶數次は正・奇數次は負）、（－3）² と －3² の違い、a⁰＝1（a≠0）、同底數の大小比較、指數を含む四則運算。
誤答：3⁴ を 3×4 とする、－3² を 9 とする、2⁰ を 0 とする、0＜底數＜1 で指數が大きいほど大きいとする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, num
from tw_g7 import sn, par, opv, tidy_sets, pw

R = random.Random(71007)
NM = Names(R)


def s1(seen):
    def mk():
        b, e = R.randint(2, 9), R.randint(2, 5)
        if b ** e > 100000:
            return None
        k = R.choice(["write", "val"])
        if k == "write":
            q = "%s 表示什麼？" % pw(b, e)
            ans = " × ".join([str(b)] * e)
            return mcq(q, ans, ["%d × %d" % (b, e), " ＋ ".join([str(b)] * e), " × ".join([str(e)] * b) if b <= 6 else "%d × %d" % (e, b)], "%s 是 %d 個 %d 相乘，%d 是底數，%d 是指數。" % (pw(b, e), e, b, b, e))
        return mcq("%s ＝ ？" % pw(b, e), num(b ** e), [num(b * e), num(e ** b) if e ** b != b ** e and e ** b < 10 ** 6 else num(b ** (e + 1)), num(b ** (e - 1))], "%s ＝ %s ＝ %s。" % (pw(b, e), " × ".join([str(b)] * e), num(b ** e)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        b, e = R.randint(2, 6), R.randint(2, 5)
        v = (-b) ** e
        if abs(v) > 10000:
            return None
        return mcq("%s ＝ ？" % pw(-b, e), sn(v), [sn(-v), sn(-b * e), sn(b * e)], "%d 個（－%d）相乘，負數有%s個，答案是%s：%s。" % (e, b, "偶數" if e % 2 == 0 else "奇數", "正" if v > 0 else "負", sn(v)))

    def frac():
        n, d = R.randint(1, 4), R.randint(2, 5)
        if n >= d or F(n, d).denominator != d:
            return None
        e = R.choice([2, 3])
        sg = R.choice([1, -1])
        base = F(n, d) * sg
        v = base ** e
        b = "（%s）" % sn(base)
        return mcq("%s ＝ ？" % pw(b, e), sn(v), [sn(-v), sn(F(n ** e, d)), sn(base * e)], "分子、分母各自乘 %d 次：%s。" % (e, sn(v)))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, frac, 6, seen)


def s3(seen):
    def mk():
        b = R.randint(2, 9)
        e = R.choice([2, 4]) if R.random() < .7 else 3
        if b ** e > 1000:
            return None
        k = R.choice(["a", "b"])
        if k == "a":
            q = "－%s ＝ ？" % pw(str(b), e)
            v = -(b ** e)
            e2 = "－%s 是「%s 的相反數」，只有 %d 做次方：－%s ＝ %s。" % (pw(str(b), e), pw(str(b), e), b, pw(str(b), e), sn(v))
        else:
            q = "%s ＝ ？" % pw(-b, e)
            v = (-b) ** e
            e2 = "（－%d）整個做次方：%s。" % (b, sn(v))
        return mcq(q, sn(v), [sn(-v), sn(-b * e), sn(b * e)], e2)

    def zero():
        b = R.choice([2, 5, 7, 10, 100, 2026]) * R.choice([1, -1])
        if R.random() < .4:
            b = F(R.randint(1, 5), R.randint(6, 9))
        q = "%s ＝ ？" % pw(par(b) if F(b).denominator == 1 else "（%s）" % sn(b), 0)
        return mcq(q, "1", ["0", sn(b), "沒有意義"], "任何不是 0 的數的 0 次方都等於 1。")
    return pick_unique(R, mk, 14, seen) + pick_unique(R, zero, 6, seen)


def s4(seen):
    def mk():
        b = R.choice([2, 3, 5, 7, F(1, 2), F(2, 3), F(1, 3)])
        e1, e2 = R.sample(range(2, 9), 2)
        bs = str(b) if F(b).denominator == 1 else "（%s）" % sn(b)
        big = max(e1, e2) if F(b) > 1 else min(e1, e2)
        q = "%s 和 %s，哪一個比較大？" % (pw(bs, e1), pw(bs, e2))
        ans = pw(bs, big)
        oth = pw(bs, e1 if big == e2 else e2)
        e = "底數大於 1，指數越大越大。" if F(b) > 1 else "底數在 0 和 1 之間，乘越多次越小，指數越小反而越大。"
        return mcq(q, ans, [oth, "一樣大", "無法比較"], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        a, b = R.randint(2, 5), R.randint(2, 4)
        c = R.randint(1, 9) * R.choice([1, -1])
        e = R.choice([2, 3])
        k = R.choice([1, 2, 3])
        if k == 1:
            v = (-a) ** e + c * b
            q = "%s%s × %d ＝" % (pw(-a, e), opv("＋", c), b)
            w = [-(a ** e) + c * b, ((-a) ** e + c) * b, (-a) * e + c * b]
            ex = "先算次方 %s ＝ %s，再乘 %s × %d ＝ %s，最後相加：%s。" % (pw(-a, e), sn((-a) ** e), par(c), b, sn(c * b), sn(v))
        elif k == 2:
            v = -(a ** 2) - (-b) ** 3
            q = "－%s －%s ＝" % (pw(str(a), 2), pw(-b, 3))
            w = [a ** 2 + b ** 3, -(a ** 2) + (-b) ** 3, a ** 2 - b ** 3]
            ex = "－%s ＝ %s，%s ＝ %s，%s －（%s）＝ %s。" % (pw(str(a), 2), sn(-(a ** 2)), pw(-b, 3), sn(-(b ** 3)), sn(-(a ** 2)), sn(-(b ** 3)), sn(v))
        else:
            if abs(c - a) < 2:
                return None
            v = (c - a) ** 2
            q = "%s ＝" % pw("（%s%s）" % (sn(c), opv("－", a)), 2)
            w = [c ** 2 - a ** 2, -v, (c - a) * 2]
            ex = "先算括號 %s%s ＝ %s，再平方：%s。" % (sn(c), opv("－", a), sn(c - a), sn(v))
        return mcq(q, sn(v), [sn(x) for x in w if x != v] + [sn(v + 1)], ex)
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("次方的意義", s1(seen)), ("負數和分數的次方", s2(seen)), ("（－a）ⁿ 和 －aⁿ、0 次方", s3(seen)),
            ("比較大小", s4(seen)), ("含次方的四則運算", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["2<sup>4</sup> ＝ 2 × 2 × 2 × 2 ＝ 16：2 是<b>底數</b>，4 是<b>指數</b>，表示 4 個 2 相乘。",
         "負數的次方：<b>偶數次方是正，奇數次方是負</b>。（－2）<sup>3</sup> ＝ －8。",
         "注意 <b>（－3）<sup>2</sup> ＝ 9</b>，但 <b>－3<sup>2</sup> ＝ －9</b>（只有 3 做平方）。",
         "a ≠ 0 時，<b>a<sup>0</sup> ＝ 1</b>。計算順序：次方 → 乘除 → 加減。"],
        [example("（－2）<sup>5</sup>", ["5 個 －2 相乘，奇數個負數。", "2<sup>5</sup> ＝ 32。"], "－32"),
         example("－4<sup>2</sup> ＋（－4）<sup>2</sup>", ["－16 ＋ 16。"], "0")],
        [("3<sup>4</sup> ＝ 3 × 4 ＝ 12", "是 4 個 3 相乘：81"),
         ("－3<sup>2</sup> ＝ 9", "只有 3 平方，再加負號：－9"),
         ("5<sup>0</sup> ＝ 0", "不是 0 的數的 0 次方都是 1")])
    faq = [{"q": "（－3）² 和 －3² 有什麼不同？",
            "a": "（－3）² 是 －3 整個平方，等於 9；－3² 是先算 3² ＝ 9 再取負號，等於 －9。"},
           {"q": "為什麼 a⁰ ＝ 1？",
            "a": "看 2³ ＝ 8、2² ＝ 4、2¹ ＝ 2，指數每少 1 就除以 2，所以 2⁰ ＝ 2 ÷ 2 ＝ 1。"},
           {"q": "七年級的指數要學什麼？",
            "a": "108課綱 N-7-6：指數為非負整數的次方、a≠0 時 a⁰＝1、同底數的大小比較和指數的運算。"}]
    make_unit(R, "grade-7", "exponents", "N-7-6",
              "指數的意義：指數為非負整數的次方；a≠0時 a⁰＝1；同底數的大小比較；指數的運算。",
              "指數的意義：次方與 0 次方",
              "七年級數學 指數 練習題｜次方・（－3）²與－3²・0次方 學習單（附解答）",
              "指數的意義",
              "國中七年級數學「指數的意義」免費學習單：次方的意義、負數和分數的次方、（－3）² 和 －3² 的不同、0 次方、同底數比較大小與含次方的四則運算。100題線上練習馬上對答案，附可列印解答。",
              "aⁿ 是 n 個 a 相乘",
              "負數的偶數次方是正，奇數次方是負；a⁰ ＝ 1。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
