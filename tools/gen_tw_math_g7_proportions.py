# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：比與比例式（108課綱 N-7-9）
  python3 tools/gen_tw_math_g7_proportions.py
比・比值・最簡整數比（文字を含む）、比例式 a：b＝c：d ⇔ ad＝bc（外項積＝內項積）、x を求める、連比 a：b：c、比例分配・應用。
誤答：外項と內項を取り違える（ac＝bd）、連比で共通項をそろえない、比例分配で全体を項數で割る。
"""
import random
from math import gcd
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g7 import sn, tidy_sets

R = random.Random(71019)
NM = Names(R)


def rs(*xs):
    return "：".join(sn(x) for x in xs)


def s1(seen):
    def mk():
        a, b = R.randint(1, 12), R.randint(1, 12)
        if a == b or gcd(a, b) != 1:
            return None
        k = R.choice([F(1, 2), F(1, 3), F(1, 4), F(3, 10), F(1, 5), 2, 3])
        A, B = a * F(k), b * F(k)
        q = "把 %s 化成最簡整數比。" % rs(A, B)
        return mcq(q, rs(a, b), [rs(b, a), rs(A * 10, B * 10) if (A * 10).denominator == 1 and (B * 10).denominator == 1 and A * 10 != a else rs(a + 1, b), rs(A.numerator, B.numerator) if rs(A.numerator, B.numerator) != rs(a, b) else rs(a, b + 1)],
                   "兩項同乘或同除同一個數，化成互質的整數：%s。" % rs(a, b))

    def val():
        a, b = R.randint(1, 20), R.randint(2, 20)
        if a == b:
            return None
        return mcq("%s 的比值是多少？" % rs(a, b), sn(F(a, b)), [sn(F(b, a)), sn(F(a, a + b)), sn(F(a, b) + 1)], "比值 ＝ 前項 ÷ 後項 ＝ %d ÷ %d ＝ %s。" % (a, b, sn(F(a, b))))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, val, 8, seen)


def s2(seen):
    def mk():
        a, b = R.randint(1, 12), R.randint(1, 12)
        k = R.randint(2, 9)
        c, d = a * k, b * k
        pos = R.randrange(4)
        vals = [a, b, c, d]
        ans = vals[pos]
        shown = ["x" if i == pos else sn(v) for i, v in enumerate(vals)]
        q = "解比例式：%s：%s ＝ %s：%s，x ＝ ？" % tuple(shown)
        ext = (vals[0], vals[3])
        w = [F(vals[1] * vals[2], vals[0]) if pos == 3 else None]
        wrong = []
        if pos == 3:
            wrong.append(F(vals[0] * vals[2], vals[1]))
        elif pos == 0:
            wrong.append(F(vals[1] * vals[3], vals[2]))
        elif pos == 1:
            wrong.append(F(vals[0] * vals[2], vals[3]))
        else:
            wrong.append(F(vals[0] * vals[1], vals[3]))
        wrong += [ans + k, ans * 2]
        return mcq(q, sn(ans), [sn(t) for t in wrong if t != ans] + [sn(ans + 1)], "外項乘積 ＝ 內項乘積：%s × %s ＝ %s × %s，解得 x ＝ %s。" % (shown[0], shown[3], shown[1], shown[2], sn(ans)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b, c = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
        k = R.randint(2, 6)
        # x：y ＝ a：b、y：z ＝ (b*k)：c'
        y1 = b
        m = R.randint(1, 9)
        y2 = m
        L = y1 * y2 // gcd(y1, y2)
        x_, y_, z_ = a * L // y1, L, c * L // y2
        g = gcd(gcd(x_, y_), z_)
        x_, y_, z_ = x_ // g, y_ // g, z_ // g
        if len({x_, y_, z_}) < 3 or b == m:
            return None
        q = "x：y ＝ %s，y：z ＝ %s，求 x：y：z。" % (rs(a, b), rs(m, c))
        ans = rs(x_, y_, z_)
        return mcq(q, ans, [rs(a, b, c), rs(a, b * m, c), rs(z_, y_, x_)], "把兩個比的 y 變成一樣（%d 和 %d 的最小公倍數 %d），得 %s。" % (b, m, L, ans))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def share():
        a, b = R.randint(1, 7), R.randint(1, 7)
        if a == b or gcd(a, b) != 1:
            return None
        tot = (a + b) * R.randint(20, 200)
        n1, n2 = NM.next(), NM.next()
        if n1 == n2:
            return None
        q = "%s和%s按 %s 分 %s 元，%s分到多少元？" % (n1, n2, rs(a, b), num(tot), n1)
        v = tot * a // (a + b)
        return mcq(q, "%s 元" % num(v), ["%s 元" % num(t) for t in (tot // 2, tot * b // (a + b), tot // a if tot % a == 0 and tot // a != v else v + a)], "全部分成 %d ＋ %d ＝ %d 份，%s占 %d 份：%s × %s ＝ %s（元）。" % (a, b, a + b, n1, a, num(tot), sn(F(a, a + b)), num(v)))

    def three():
        a, b, c = R.randint(1, 5), R.randint(1, 5), R.randint(1, 5)
        if len({a, b, c}) < 3:
            return None
        tot = (a + b + c) * R.randint(5, 30)
        q = "三角形三個內角的比是 %s，最大的角是幾度？" % rs(a, b, c) if (a + b + c) and 180 % (a + b + c) == 0 else None
        if not q:
            return None
        v = 180 * max(a, b, c) // (a + b + c)
        return mcq(q, "%d 度" % v, ["%d 度" % t for t in (180 * min(a, b, c) // (a + b + c), 60, v + 10)  if t != v], "內角和 180 度，分成 %d 份：180 × %s ＝ %d（度）。" % (a + b + c, sn(F(max(a, b, c), a + b + c)), v))
    return pick_unique(R, share, 12, seen) + pick_unique(R, three, 8, seen)


def s5(seen):
    def recipe():
        a, b = R.choice([(2, 3), (3, 5), (1, 4), (3, 4), (2, 5)])
        k = R.randint(2, 12)
        flour = a * 50 * k
        q = "做蛋糕時麵粉和糖的比是 %s。用了 %d 公克麵粉，要用多少公克糖？" % (rs(a, b), flour)
        v = b * 50 * k
        return mcq(q, "%d 公克" % v, ["%s 公克" % sn(t) for t in (F(flour * a, b), flour * b, v - flour // a)], ("%s ＝ %d：x，%dx ＝ %d × %d，x ＝ %d。" % (rs(a, b), flour, a, flour, b, v)) if a != 1 else ("%s ＝ %d：x，x ＝ %d × %d ＝ %d。" % (rs(a, b), flour, flour, b, v)))

    def map_():
        s = R.choice([10000, 20000, 25000, 50000])
        d = R.randint(2, 12)
        real = d * s // 100
        q = "地圖上 %d 公分代表實際 %s 公尺，地圖上 %d 公分代表實際多少公尺？" % (2, num(2 * s // 100), d)
        return mcq(q, "%s 公尺" % num(real), ["%s 公尺" % num(t) for t in (real * 2, real // 2 if real % 2 == 0 else real + 50, d * s)], "2：%s ＝ %d：x，2x ＝ %s，x ＝ %s。" % (num(2 * s // 100), d, num(d * 2 * s // 100), num(real)))

    def tf():
        a, b, c, d = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
        k = R.randint(2, 5)
        ok = R.random() < .5
        if ok:
            c, d = a * k, b * k
        elif a * d == b * c:
            return None
        q = "%s 和 %s 是不是相等的比？" % (rs(a, b), rs(c, d))
        return mcq(q, "是" if ok else "不是", ["不是" if ok else "是", "要看單位", "無法判斷"], "外項乘積 %d × %d ＝ %d，內項乘積 %d × %d ＝ %d，%s。" % (a, d, a * d, b, c, b * c, "相等，所以是相等的比" if ok else "不相等"))
    return pick_unique(R, recipe, 7, seen) + pick_unique(R, map_, 6, seen) + pick_unique(R, tf, 7, seen)


def main():
    seen = set()
    sets = [("比、比值與最簡整數比", s1(seen)), ("解比例式", s2(seen)), ("連比", s3(seen)),
            ("比例分配", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["比值 ＝ 前項 ÷ 後項。比值相等的兩個比叫相等的比，寫成<b>比例式</b> a：b ＝ c：d。",
         "比例式的性質：<b>外項乘積 ＝ 內項乘積</b>，a × d ＝ b × c。可以用來求未知數。",
         "<b>連比</b>：x：y ＝ 2：3、y：z ＝ 4：5，先把 y 化成一樣（12），得 x：y：z ＝ 8：12：15。",
         "<b>比例分配</b>：按 a：b 分，全部是 a ＋ b 份。"],
        [example("3：5 ＝ x：20", ["外項乘積 ＝ 內項乘積：3 × 20 ＝ 5x。", "5x ＝ 60。"], "x ＝ 12"),
         example("600 元按 2：3 分，多的一人分到多少？", ["共 5 份，600 × <span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span>。"], "360 元")],
        [("3：5 ＝ x：20 寫成 3x ＝ 5 × 20", "外項是 3 和 20：3 × 20 ＝ 5x"),
         ("連比直接把 2：3 和 4：5 接成 2：3：5", "先把共同的 y 化成一樣"),
         ("按 2：3 分 600 元，每人 300 元", "要按份數分：240 元和 360 元")])
    faq = [{"q": "比例式要怎麼解？",
            "a": "用「外項乘積 ＝ 內項乘積」：a：b ＝ c：d 時 a × d ＝ b × c，把未知數解出來。"},
           {"q": "連比怎麼合併？",
            "a": "找出兩個比中共同的那一項，把它化成相同的數（用最小公倍數），再把三項接起來。"},
           {"q": "七年級的比與比例式要學什麼？",
            "a": "108課綱 N-7-9：比、比例式、正比、反比和相關之基本運算與應用問題，教學情境應以有意義之比值為例。"}]
    make_unit(R, "grade-7", "ratio-and-proportion", "N-7-9",
              "比與比例式：比；比例式；正比；反比；相關之基本運算與應用問題，教學情境應以有意義之比值為例。",
              "比與比例式",
              "七年級數學 比例式 練習題｜外項乘積＝內項乘積・連比・比例分配 學習單（附解答）",
              "比與比例式",
              "國中七年級數學「比與比例式」免費學習單：比值與最簡整數比、用外項乘積等於內項乘積解比例式、連比、比例分配與食譜、地圖等應用題。100題線上練習馬上對答案，附可列印解答。",
              "外項乘積 ＝ 內項乘積",
              "連比要先把共同的一項化成一樣。",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
