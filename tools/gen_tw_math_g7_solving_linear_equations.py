# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：一元一次方程式的解法（108課綱 A-7-2、A-7-3）
  python3 tools/gen_tw_math_g7_solving_linear_equations.py
方程式の解の意味（代入して確かめる）、等量公理、移項法則（符號を変える）、兩邊に x がある式、括號・分數を含む式、驗算。
誤答：移項で符號を変えない、兩邊を割るとき片方だけ割る、分數の分母を払うとき全項に掛けない、去括號で後ろに掛け忘れる。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr
from tw_g7 import sn, par, opv, tidy_sets, lin, term, const

R = random.Random(71012)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def xs(v):
    return "x ＝ %s" % sn(v)


def s1(seen):
    def mk():
        a, x = nz(-6, 6), nz(-8, 8)
        b = nz(-12, 12)
        c = a * x + b
        q = "下面哪一個是方程式 %s ＝ %s 的解？" % (lin(a, b), sn(c))
        return mcq(q, xs(x), [xs(-x), xs(x + 1), xs(F(c, a) if F(c, a).denominator == 1 and F(c, a) != x else x - 1)],
                   "把 x ＝ %s 代入：%s ×%s%s ＝ %s，等號兩邊相等。" % (sn(x), sn(a), " " + par(x) if x > 0 else par(x), opv("＋", b), sn(c)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        x = nz(-12, 12)
        k = R.choice(["add", "mul", "div"])
        if k == "add":
            b = nz(-15, 15)
            c = x + b
            q = "解方程式：x%s ＝ %s" % (opv("＋", b), sn(c))
            return mcq(q, xs(x), [xs(c + b), xs(-x), xs(b - c)], "兩邊同減 %s（移項要變號）：x ＝ %s%s ＝ %s。" % (sn(b), sn(c), opv("－", b), sn(x)))
        if k == "mul":
            a = R.choice([2, 3, 4, 5, 6, 7, 8, 9, -2, -3, -4, -5, -6])
            q = "解方程式：%s ＝ %s" % (term(a, "x", True), sn(a * x))
            return mcq(q, xs(x), [xs(-x), xs(a * x - a), xs(a * x * a) if abs(a * x * a) < 500 else xs(x + 1)], "兩邊同除以 %s：x ＝ %s ÷ %s ＝ %s。" % (sn(a), sn(a * x), par(a), sn(x)))
        a = R.choice([2, 3, 4, 5, -2, -3])
        q = "解方程式：<span class='fr'><span class='fn'>x</span><span class='fd'>%d</span></span> ＝ %s" % (abs(a), sn(x)) if a > 0 else "解方程式：－<span class='fr'><span class='fn'>x</span><span class='fd'>%d</span></span> ＝ %s" % (abs(a), sn(-x))
        ans = x * abs(a)
        if a > 0:
            return mcq(q, xs(ans), [xs(F(x, abs(a))), xs(-ans), xs(x + abs(a))], "兩邊同乘以 %d：x ＝ %s × %d ＝ %s。" % (abs(a), par(x), abs(a), sn(ans)))
        return mcq(q, xs(ans), [xs(-ans), xs(F(-x, abs(a))), xs(-x - abs(a))], "兩邊同乘以 －%d：x ＝ %s ×（－%d）＝ %s。" % (abs(a), par(-x), abs(a), sn(ans)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        x = nz(-10, 10)
        a, c = nz(-9, 9), nz(-9, 9)
        if a == c:
            return None
        b = nz(-15, 15)
        d = a * x + b - c * x
        q = "解方程式：%s ＝ %s" % (lin(a, b), lin(c, d))
        wrong1 = F(d + b, a - c) if a != c else None
        wrong2 = F(d - b, a + c) if a + c else None
        return mcq(q, xs(x), [xs(w) for w in (wrong1, wrong2) if w is not None and w != x] + [xs(-x), xs(x + 1)],
                   ("移項：x 項移到左邊、常數移到右邊，%s ＝ %s，所以 x ＝ %s。" % (lin(a - c, 0), sn(d - b), sn(x))) if a - c != 1 else ("移項：x 項移到左邊、常數移到右邊，x ＝ %s%s ＝ %s。" % (sn(d), opv("－", b), sn(x))))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def paren():
        x = nz(-8, 8)
        k, a, b = R.choice([2, 3, 4, 5, -2, -3]), nz(-5, 5), nz(-9, 9)
        e = nz(-9, 9)
        rhs = k * (a * x + b) + e
        q = "解方程式：%s（%s）%s ＝ %s" % (sn(k), lin(a, b), const(e), sn(rhs))
        w = F(rhs - e - b, k * a) if k * a else None
        return mcq(q, xs(x), [xs(t) for t in (w, F(rhs + e - k * b, k * a), -x) if t is not None and t != x] + [xs(x + 2)],
                   "去括號：%s%s ＝ %s，移項：%s ＝ %s，x ＝ %s。" % (lin(k * a, k * b), const(e), sn(rhs), lin(k * a, 0), sn(rhs - e - k * b), sn(x)))

    def frac():
        d1, d2 = R.choice([(2, 3), (3, 4), (2, 5), (4, 6), (3, 6), (2, 4)])
        L = d1 * d2 // __import__("math").gcd(d1, d2)
        x = R.choice(range(-12, 13, 1))
        if x == 0:
            return None
        a = R.randint(1, 3)
        rhs = F(x, d1) + F(a * x, d2)
        if rhs.denominator != 1:
            return None
        q = "解方程式：<span class='fr'><span class='fn'>x</span><span class='fd'>%d</span></span> ＋ <span class='fr'><span class='fn'>%sx</span><span class='fd'>%d</span></span> ＝ %s" % (d1, "" if a == 1 else a, d2, sn(rhs))
        coef = F(1, d1) + F(a, d2)
        return mcq(q, xs(x), [xs(rhs * (d1 + d2) / (1 + a)) if rhs * (d1 + d2) / (1 + a) != x else xs(x + 1), xs(-x), xs(rhs / coef * 2)],
                   "兩邊同乘以分母的最小公倍數 %d：%dx ＋ %dx ＝ %s，%dx ＝ %s，x ＝ %s。" % (L, L // d1, a * L // d2, sn(rhs * L), L // d1 + a * L // d2, sn(rhs * L), sn(x)))
    return pick_unique(R, paren, 12, seen) + pick_unique(R, frac, 8, seen)


def s5(seen):
    def check():
        x = nz(-8, 8)
        a, b = nz(-6, 6), nz(-9, 9)
        c = a * x + b
        wrong = x + R.choice([1, -1, 2])
        who = NM.next()
        q = "%s解 %s ＝ %s 得到 x ＝ %s。用驗算檢查，答案對嗎？" % (who, lin(a, b), sn(c), sn(wrong))
        back = a * wrong + b
        return mcq(q, "不對，正確是 x ＝ %s" % sn(x), ["對", "不對，正確是 x ＝ %s" % sn(-x), "不對，正確是 x ＝ %s" % sn(x + 3)],
                   "代入 x ＝ %s：左邊 ＝ %s，不等於 %s；正確解是 x ＝ %s。" % (sn(wrong), sn(back), sn(c), sn(x)))

    def step():
        a, b, c = R.randint(2, 9), nz(-12, 12), nz(-20, 20)
        q = "解 %s ＝ %s 時，第一步「移項」後應該是哪一個？" % (lin(a, b), sn(c))
        ans = "%dx ＝ %s%s" % (a, sn(c), opv("－", b))
        return mcq(q, ans, ["%dx ＝ %s%s" % (a, sn(c), opv("＋", b)), "x ＝ %s%s" % (sn(c), opv("－", b)), "%dx ＝ %s%s" % (a, sn(b), opv("－", c))],
                   "把 %s 從左邊移到右邊要變號，變成 %s。" % (const(b, True), sn(-b)))
    return pick_unique(R, check, 10, seen) + pick_unique(R, step, 10, seen)


def main():
    seen = set()
    sets = [("方程式的解", s1(seen)), ("一步驟的方程式", s2(seen)), ("兩邊都有 x", s3(seen)),
            ("含括號和分數", s4(seen)), ("移項與驗算", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["使方程式等號兩邊相等的 x 值叫做<b>解</b>。代進去兩邊一樣，就是解。",
         "<b>等量公理</b>：等號兩邊同加、同減、同乘、同除以（不為 0 的）同一個數，等式仍成立。",
         "<b>移項</b>：把一項從等號一邊移到另一邊，<b>要變號</b>（＋變－，－變＋）。",
         "有括號先去括號；有分數先兩邊同乘分母的最小公倍數。解完要<b>驗算</b>。"],
        [example("5x － 7 ＝ 2x ＋ 8", ["移項：5x － 2x ＝ 8 ＋ 7。", "3x ＝ 15。"], "x ＝ 5"),
         example("3（x － 2）＝ 2x ＋ 1", ["去括號：3x － 6 ＝ 2x ＋ 1。", "3x － 2x ＝ 1 ＋ 6。"], "x ＝ 7")],
        [("x ＋ 5 ＝ 12 移項成 x ＝ 12 ＋ 5", "移項要變號：x ＝ 12 － 5"),
         ("3x ＝ 12，x ＝ 12 － 3", "兩邊同除以 3：x ＝ 4"),
         ("分數方程式只把左邊乘以公分母", "等號兩邊每一項都要乘")])
    faq = [{"q": "移項為什麼要變號？",
            "a": "移項其實是等號兩邊同加或同減一個數。例如 x ＋ 5 ＝ 12 兩邊同減 5，得到 x ＝ 12 － 5，看起來就像 5 移過去變成 －5。"},
           {"q": "怎麼驗算方程式的解？",
            "a": "把解代回原來的方程式，分別算左邊和右邊，兩邊相等就對了。"},
           {"q": "七年級的一元一次方程式要學什麼？",
            "a": "108課綱 A-7-2、A-7-3：一元一次方程式及其解的意義，用等量公理、移項法則解方程式，並驗算和解應用問題。"}]
    make_unit(R, "grade-7", "solving-linear-equations", "A-7-3",
              "一元一次方程式的解法與應用：等量公理；移項法則；驗算；應用問題。",
              "一元一次方程式的解法",
              "七年級數學 一元一次方程式 練習題｜等量公理・移項・驗算 學習單（附解答）",
              "一元一次方程式",
              "國中七年級數學「一元一次方程式的解法」免費學習單：方程式的解、等量公理、移項法則、兩邊都有 x、含括號和分數的方程式與驗算。100題線上練習馬上對答案，附可列印解答。",
              "移項要變號",
              "等號兩邊同加、同減、同乘、同除，等式仍成立。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
