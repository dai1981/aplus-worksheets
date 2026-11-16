# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：代數式與一次式的化簡（108課綱 A-7-1）
  python3 tools/gen_tw_math_g7_algebraic_expressions.py
文字で情境を表す（省略記號：3x、x÷2＝x/2）、同類項、一次式の化簡（合併同類項・去括號・分配律）、代入求值、應用。
誤答：3x＋2 を 5x とする、－(2x－3) の後ろの項の符號を變えない、x×x と 2x を混同、代入時に負數を括弧に入れない。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr
from tw_g7 import sn, par, opv, tidy_sets, lin, term, const

R = random.Random(71011)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    CTX = [("一枝筆 x 元，買 %d 枝要付多少元？", lambda k: "%dx 元" % k, lambda k: ["（x ＋ %d）元" % k, "%d ÷ x 元" % k, "x%d 元" % k]),
           ("小明今年 x 歲，%d 年後幾歲？", lambda k: "（x ＋ %d）歲" % k, lambda k: ["%dx 歲" % k, "（x － %d）歲" % k, "（%d － x）歲" % k]),
           ("有 x 顆糖，平分給 %d 人，每人幾顆？", lambda k: "<span class='fr'><span class='fn'>x</span><span class='fd'>%d</span></span> 顆" % k, lambda k: ["%dx 顆" % k, "（x － %d）顆" % k, "<span class='fr'><span class='fn'>%d</span><span class='fd'>x</span></span> 顆" % k]),
           ("長方形的長是 x 公分，寬比長少 %d 公分，寬是多少公分？", lambda k: "（x － %d）公分" % k, lambda k: ["（%d － x）公分" % k, "（x ＋ %d）公分" % k, "%dx 公分" % k]),
           ("一個數 x 的 %d 倍再加 5，怎麼表示？", lambda k: "%dx ＋ 5" % k, lambda k: ["%d（x ＋ 5）" % k, "%dx ＋ 5x" % k, "x ＋ %d ＋ 5" % k]),
           ("正方形的邊長是 x 公分，周長是多少公分？", lambda k: "4x 公分", lambda k: ["x<sup>2</sup> 公分", "（x ＋ 4）公分", "2x 公分"])]

    def mk():
        t, a, w = R.choice(CTX)
        k = R.randint(2, 9)
        q = t % k if "%d" in t else t
        return mcq(q, a(k), w(k), "用符號記錄：%s。數字和文字相乘時，數字寫在前面，乘號可以省略。" % a(k))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b, c = nz(-9, 9), nz(-9, 9), nz(-9, 9)
        d = nz(-9, 9)
        expr = term(a, "x", True) + const(c) + term(b, "x") + const(d)
        ans = lin(a + b, c + d)
        if a + b == 0:
            return None
        return mcq("化簡：%s" % expr, ans, [lin(a + b + c + d, 0) if a + b + c + d else lin(a + b, -(c + d)), lin(a - b, c + d) if a != b else lin(a + b, c - d), lin(a + b, -(c + d)) if c + d else lin(a + b, 1)],
                   "合併同類項：x 項 %s%s ＝ %s，常數 %s%s ＝ %s，答案 %s。" % (sn(a), opv("＋", b), sn(a + b), sn(c), opv("＋", d), sn(c + d), ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = R.choice([2, 3, 4, 5, 6, -2, -3, -4, -5, -6])
        a, b = nz(-6, 6), nz(-9, 9)
        e = nz(-9, 9)
        sign = R.choice(["＋", "－"])
        s = 1 if sign == "＋" else -1
        inner = lin(a, b)
        q = "化簡：%s %s %s（%s）" % (lin(0, e) if False else const(e, True), sign, str(abs(k)) if abs(k) != 1 else "", inner)
        kk = s * abs(k)
        ans = lin(kk * a, kk * b + e)
        w = [lin(kk * a, b + e), lin(kk * a, -kk * b + e), lin(kk * a + e, kk * b)]
        if kk * a == 0:
            return None
        return mcq(q, ans, w, "分配律去括號：%s%d ×（%s）＝ %s，再和 %s 合併：%s。" % ("－" if sign == "－" else "", abs(k), inner, lin(kk * a, kk * b), sn(e), ans))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, b = nz(-9, 9), nz(-12, 12)
        x = nz(-6, 6)
        v = a * x + b
        q = "當 x ＝ %s 時，%s 的值是多少？" % (sn(x), lin(a, b))
        return mcq(q, sn(v), [sn(a * (-x) + b), sn(a + x + b), sn(-a * x + b) if -a * x + b != a * (-x) + b else sn(v + 1), sn(v - b - b) if b else sn(v + 2)],
                   "代入：%s ×%s%s ＝ %s%s ＝ %s。負數代入要加括號。" % (sn(a), " " + par(x) if x > 0 else par(x), opv("＋", b), sn(a * x), opv("＋", b), sn(v)))

    def two():
        a, b, x, y = nz(-5, 5), nz(-5, 5), nz(-4, 4), nz(-4, 4)
        v = a * x + b * y
        q = "當 x ＝ %s、y ＝ %s 時，%s 的值是多少？" % (sn(x), sn(y), term(a, "x", True) + term(b, "y"))
        return mcq(q, sn(v), [sn(a * y + b * x) if a * y + b * x != v else sn(v + 2), sn(-v) if v else "1", sn(a + x + b + y) if a + x + b + y != v else sn(v - 1)], "%s ×%s ＋ %s ×%s ＝ %s。" % (sn(a), par(x), sn(b), par(y), sn(v)))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, two, 8, seen)


def s5(seen):
    def rect():
        a, b = R.randint(2, 6), R.randint(1, 9)
        q = "長方形的長是（%s）公分，寬是 x 公分。周長是多少公分？" % lin(a, b)
        ans = "（%s）公分" % lin(2 * a + 2, 2 * b)
        return mcq(q, ans, ["（%s）公分" % lin(a + 1, b), "（%s）公分" % lin(2 * a + 2, b), "（%s）公分" % lin(2 * a, 2 * b)], "周長 ＝ 2 ×（%s ＋ x）＝ 2 ×（%s）＝ %s。" % (lin(a, b), lin(a + 1, b), lin(2 * a + 2, 2 * b)))

    def ticket():
        a, c = R.choice([(250, 150), (300, 180), (200, 120), (350, 200)])
        n = R.randint(3, 10)
        q = "全票 %d 元，半票 %d 元。一共買了 %d 張票，其中全票 x 張，總共多少元？" % (a, c, n)
        ans = "%s 元" % lin(a - c, c * n)
        return mcq(q, ans, ["%s 元" % lin(a + c, c * n), "%s 元" % lin(a, c * n), "%s 元" % lin(a - c, a * n)], "全票 %dx 元，半票（%d － x）張是 %d(%d － x) 元，合起來：%dx ＋ %d － %dx ＝ %s。" % (a, n, c, n, a, c * n, c, lin(a - c, c * n)))

    def age():
        k = R.randint(2, 4)
        d = R.randint(3, 10)
        q = "弟弟 x 歲，哥哥的年齡是弟弟的 %d 倍少 %d 歲。兩人年齡和是多少？" % (k, d)
        ans = "（%s）歲" % lin(k + 1, -d)
        return mcq(q, ans, ["（%s）歲" % lin(k + 1, d), "（%s）歲" % lin(k, -d), "（%s）歲" % lin(k * 2, -d)], "哥哥 %s，和 ＝ x ＋ %s ＝ %s。" % (lin(k, -d), lin(k, -d), lin(k + 1, -d)))
    return pick_unique(R, rect, 7, seen) + pick_unique(R, ticket, 6, seen) + pick_unique(R, age, 7, seen)


def main():
    seen = set()
    sets = [("用符號表示", s1(seen)), ("合併同類項", s2(seen)), ("去括號化簡", s3(seen)),
            ("代入求值", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["用文字（如 x）代表數：3 × x 寫成 <b>3x</b>，x ÷ 2 寫成 <span class='fr'><span class='fn'>x</span><span class='fd'>2</span></span>，1 × x 寫成 x。",
         "<b>同類項</b>：文字部分完全一樣的項，才能合併：3x ＋ 5x ＝ 8x；3x 和 5 不能合併。",
         "去括號用分配律：－2（x － 3）＝ －2x ＋ 6，每一項都要乘、都要變號。",
         "代入求值：負數代入要加括號。"],
        [example("化簡 3x ＋ 4 － 5x ＋ 2", ["x 項：3x － 5x ＝ －2x。", "常數：4 ＋ 2 ＝ 6。"], "－2x ＋ 6"),
         example("化簡 7 － 2（3x － 1）", ["－2 × 3x ＝ －6x，－2 ×（－1）＝ ＋2。", "7 ＋ 2 ＝ 9。"], "－6x ＋ 9")],
        [("3x ＋ 2 ＝ 5x", "3x 和 2 不是同類項，不能合併"),
         ("－（2x － 3）＝ －2x － 3", "每一項都變號：－2x ＋ 3"),
         ("x ＝ －2 代入 3x：3 － 2", "要寫成 3 ×（－2）＝ －6")])
    faq = [{"q": "什麼是同類項？",
            "a": "文字部分完全相同的項，例如 3x 和 －5x；常數項之間也是同類項。不同文字或常數和文字項都不能合併。"},
           {"q": "代數式代入負數要注意什麼？",
            "a": "把負數加上括號再代入，例如 x ＝ －3 時，2x ＝ 2 ×（－3）＝ －6。"},
           {"q": "七年級的代數式要學什麼？",
            "a": "108課綱 A-7-1：以代數符號表徵交換律、分配律、結合律，一次式的化簡及同類項，以符號記錄生活中的情境問題。"}]
    make_unit(R, "grade-7", "algebraic-expressions", "A-7-1",
              "代數符號：以代數符號表徵交換律、分配律、結合律；一次式的化簡及同類項；以符號記錄生活中的情境問題。",
              "代數式與一次式的化簡",
              "七年級數學 一次式化簡 練習題｜同類項・去括號・代入求值 學習單（附解答）",
              "一次式的化簡",
              "國中七年級數學「代數式與一次式的化簡」免費學習單：用符號表示生活情境、合併同類項、用分配律去括號、代入求值與周長、票價、年齡應用題。100題線上練習馬上對答案，附可列印解答。",
              "只有同類項才能合併",
              "去括號時每一項都要乘；括號前是負號，每一項都變號。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
