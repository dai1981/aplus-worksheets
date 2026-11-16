# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：多項式的乘除（108課綱 A-8-3）
  python3 tools/gen_tw_math_g8_polynomial_multiplication_and_division.py
單項式×多項式、多項式×多項式（積は三次まで）、二次多項式÷一次多項式（商と餘式）、單項式で割る、驗算（被除式＝除式×商式＋餘式）。
誤答：分配で後ろの項に掛け忘れる、x×x を 2x とする、除法で餘式の符號を誤る、商式と餘式を取り違える。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g8 import poly, pmul, padd, sn, par, tidy_sets, pq

R = random.Random(81003)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def mk():
        k = nz(-6, 6)
        cs = [nz(-6, 6), R.randint(-9, 9), nz(-9, 9)]
        mono = [k, 0]
        r = pmul(mono, cs)
        q = "%s（%s）＝" % (poly(mono), poly(cs))
        w = [poly(pmul([k], cs)), poly(r[:-1] + [r[-1] + cs[-1] - r[-1]] if False else [r[0], r[1], r[2], cs[-1]]), poly([-x for x in r])]
        return mcq(q, poly(r), w + [poly(pmul([k, 0], [cs[0], cs[1]]) + [0])], "分配律：%s 乘以括號裡的每一項，x × x<sup>2</sup> ＝ x<sup>3</sup>：%s。" % (poly(mono), poly(r)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a = [nz(-4, 4), nz(-6, 6)]
        b = [nz(-4, 4), R.randint(-6, 6), nz(-6, 6)] if R.random() < .5 else [nz(-4, 4), nz(-6, 6)]
        r = pmul(a, b)
        q = "%s（%s）＝" % (pq(a[0], a[1]), poly(b))
        wrong1 = padd(pmul([a[0], 0], b), [a[1]])
        wrong2 = [x for x in r]
        wrong2[-2] = wrong2[-2] + 1 if len(wrong2) > 2 else wrong2[-2]
        return mcq(q, poly(r), [poly(wrong1), poly([-x for x in r]), poly(padd(r, [2 * a[1] * b[-1]]))] + [poly(wrong2)], "每一項都要乘到再合併同類項：%s。" % poly(r))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        d = [R.randint(1, 3), nz(-6, 6)]
        qt = [nz(-4, 4), R.randint(-6, 6)]
        rem = R.choice([0, nz(-9, 9)])
        n = padd(pmul(d, qt), [rem])
        if n[0] == 0:
            return None
        q = "（%s）÷（%s），商式和餘式各是什麼？" % (poly(n), poly(d))
        ans = "商式 %s，餘式 %s" % (poly(qt), sn(rem))
        return mcq(q, ans, ["商式 %s，餘式 %s" % (poly(qt), sn(-rem)) if rem else "商式 %s，餘式 %s" % (poly(qt), sn(d[1])),
                            "商式 %s，餘式 %s" % (poly([qt[0], -qt[1]]) if qt[1] else poly([qt[0], 1]), sn(rem)),
                            "商式 %s，餘式 %s" % (sn(rem) if rem else "1", poly(qt))],
                   "用直式除：（%s）×（%s）%s ＝ %s，所以商式 %s、餘式 %s。" % (poly(d), poly(qt), (" ＋ %s" % par(rem)) if rem else "", poly(n), poly(qt), sn(rem)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mono():
        k = R.choice([2, 3, 4, -2, -3])
        cs = [k * nz(-4, 4), k * R.randint(-5, 5), k * R.randint(-5, 5)]
        if cs[1] == 0:
            return None
        q = "（%s）÷ %s ＝" % (poly(cs + [0]), poly([k, 0]) if k > 0 else "（%s）" % poly([k, 0]))
        r = [c // k for c in cs]
        return mcq(q, poly(r), [poly(r + [0]), poly([-c for c in r]), poly([cs[0] // k, cs[1], cs[2]]), poly([r[0], r[1], cs[2]])], "每一項都除以 %s：%s。" % (poly([k, 0]), poly(r)))

    def check():
        d = [1, nz(-6, 6)]
        qt = [nz(-4, 4), R.randint(-6, 6)]
        rem = nz(-9, 9)
        n = padd(pmul(d, qt), [rem])
        q = "某多項式除以 %s，得商式 %s、餘式 %s。這個多項式是？" % (poly(d), poly(qt), sn(rem))
        return mcq(q, poly(n), [poly(pmul(d, qt)), poly(padd(pmul(d, qt), [-rem])), poly(padd(padd(d, qt), [rem]))], "被除式 ＝ 除式 × 商式 ＋ 餘式 ＝（%s）（%s）＋%s ＝ %s。" % (poly(d), poly(qt), par(rem) if rem < 0 else " %s" % sn(rem), poly(n)))
    return pick_unique(R, mono, 10, seen) + pick_unique(R, check, 10, seen)


def s5(seen):
    def area():
        a, b = [1, R.randint(1, 8)], [1, R.randint(1, 8)]
        k = R.choice([2, 3])
        a = [k, a[1]]
        q = "長方形的長是（%s）公分，寬是（%s）公分。面積是多少平方公分？" % (poly(a), poly(b))
        r = pmul(a, b)
        return mcq(q, "（%s）平方公分" % poly(r), ["（%s）平方公分" % poly(padd(a, b)), "（%s）平方公分" % poly([r[0], 0, r[2]]), "（%s）平方公分" % poly([2 * x for x in padd(a, b)])], "（%s）（%s）＝ %s。" % (poly(a), poly(b), poly(r)))

    def box():
        x = R.randint(2, 5)
        a, b = [1, R.randint(1, 4)], [1, R.randint(1, 4)]
        q = "長方體的長是（%s）、寬是（%s）、高是 x。體積是？" % (poly(a), poly(b))
        r = pmul(pmul(a, b), [1, 0])
        return mcq(q, poly(r), [poly(pmul(a, b)), poly(padd(padd(a, b), [1, 0])), poly([1, a[1] + b[1], a[1] * b[1], 0][1:])], "（%s）（%s）× x ＝ %s。" % (poly(a), poly(b), poly(r)))

    def width():
        w = [1, R.randint(1, 9)]
        L = [R.randint(1, 3), nz(-5, 9)]
        A = pmul(w, L)
        q = "長方形的面積是（%s），寬是（%s）。長是多少？" % (poly(A), poly(w))
        return mcq(q, poly(L), [poly(padd(A, w, -1)), poly([L[0], -L[1]]), poly([L[0] + 1, L[1]])], "長 ＝ 面積 ÷ 寬：（%s）÷（%s）＝ %s。" % (poly(A), poly(w), poly(L)))
    return pick_unique(R, area, 7, seen) + pick_unique(R, box, 6, seen) + pick_unique(R, width, 7, seen)


def main():
    seen = set()
    sets = [("單項式乘多項式", s1(seen)), ("多項式乘多項式", s2(seen)), ("多項式除以一次式", s3(seen)),
            ("除以單項式與驗算", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["乘法：用分配律，每一項都乘到，再合併同類項。x × x ＝ x<sup>2</sup>，x × x<sup>2</sup> ＝ x<sup>3</sup>。",
         "除法用直式：先用除式的最高次項去除被除式的最高次項，得到商的第一項，乘回去相減，再繼續。",
         "<b>被除式 ＝ 除式 × 商式 ＋ 餘式</b>，可以用來驗算。"],
        [example("（2x ＋ 3）（x<sup>2</sup> － x ＋ 4）", ["2x<sup>3</sup> － 2x<sup>2</sup> ＋ 8x ＋ 3x<sup>2</sup> － 3x ＋ 12。"], "2x<sup>3</sup> ＋ x<sup>2</sup> ＋ 5x ＋ 12"),
         example("（x<sup>2</sup> ＋ 5x ＋ 8）÷（x ＋ 2）", ["商 x，乘回去 x<sup>2</sup> ＋ 2x，剩 3x ＋ 8。", "商 3，乘回去 3x ＋ 6，剩 2。"], "商式 x ＋ 3，餘式 2")],
        [("2x（x ＋ 3）＝ 2x<sup>2</sup> ＋ 3", "3 也要乘：2x<sup>2</sup> ＋ 6x"),
         ("x × x ＝ 2x", "x × x ＝ x<sup>2</sup>"),
         ("驗算時忘了加餘式", "除式 × 商式 ＋ 餘式")])
    faq = [{"q": "多項式的除法怎麼算？",
            "a": "和整數直式除法一樣：用除式的最高次項去除被除式的最高次項得到商的一項，乘回去相減，重複到餘式的次數比除式低。"},
           {"q": "怎麼驗算多項式除法？",
            "a": "算除式 × 商式 ＋ 餘式，結果要等於被除式。"},
           {"q": "八年級的多項式乘除要學什麼？",
            "a": "108課綱 A-8-3：直式的多項式乘法（乘積最高至三次），以及被除式為二次之多項式的除法運算。"}]
    make_unit(R, "grade-8", "polynomial-multiplication-and-division", "A-8-3",
              "多項式的四則運算：直式、橫式的多項式加法與減法；直式的多項式乘法（乘積最高至三次）；被除式為二次之多項式的除法運算。",
              "多項式的乘法與除法",
              "八年級數學 多項式乘除 練習題｜分配律・直式除法・商式餘式 學習單（附解答）",
              "多項式的乘除",
              "國中八年級數學「多項式的乘法與除法」免費學習單：單項式乘多項式、多項式乘多項式、二次多項式除以一次式求商式和餘式、驗算與面積、體積應用。100題線上練習馬上對答案，附可列印解答。",
              "被除式 ＝ 除式 × 商式 ＋ 餘式",
              "乘法每一項都要乘到；x × x ＝ x²。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
