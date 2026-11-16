# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：正三角形的高與面積（108課綱 S-8-7）
  python3 tools/gen_tw_math_g8_equilateral_triangle_area.py
正三角形の高 √3/2 a、面積 √3/4 a²、高・面積から邊長、複合圖形（正六邊形・菱形・正三角形を切り取る）、近似値（√3 ≈ 1.732）。
誤答：高を a/2 にする、面積で ÷ 2 を忘れる（√3/2 a²）、a² を 2a にする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, fr, num
from tw_g7 import tidy_sets

R = random.Random(81022)


def r3(c):
    """c√3（c は Fraction）"""
    c = F(c)
    if c.denominator == 1:
        return "√3" if c == 1 else "%s√3" % num(c.numerator)
    return fr("%s√3" % ("" if c.numerator == 1 else num(c.numerator)), c.denominator)


def s1(seen):
    def mk():
        a = R.randint(2, 24)
        h = F(a, 2)
        q = "邊長 %d 公分的正三角形，高是多少公分？" % a
        return mcq(q, "%s 公分" % r3(h), ["%s 公分" % r3(a), "%s 公分" % (num(a // 2) if a % 2 == 0 else fr(a, 2)), "%s 公分" % r3(F(a, 4)), "%s 公分" % r3(F(a * a, 2))],
                   "高把底邊分成兩半，畢氏定理：高<sup>2</sup> ＝ %d<sup>2</sup> －（%s）<sup>2</sup>，高 ＝ <span class='fr'><span class='fn'>√3</span><span class='fd'>2</span></span> × %d ＝ %s。" % (a, num(a // 2) if a % 2 == 0 else fr(a, 2), a, r3(h)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a = R.randint(2, 28)
        A = F(a * a, 4)
        q = "邊長 %d 公分的正三角形，面積是多少平方公分？" % a
        return mcq(q, "%s 平方公分" % r3(A), ["%s 平方公分" % r3(F(a * a, 2)), "%s 平方公分" % r3(F(a, 2)), "%s 平方公分" % r3(a * a), "%s 平方公分" % r3(F(2 * a, 4))],
                   "面積 ＝ <span class='fr'><span class='fn'>√3</span><span class='fd'>4</span></span> × %d<sup>2</sup> ＝ %s（底 × 高 ÷ 2 ＝ %d × %s ÷ 2）。" % (a, r3(A), a, r3(F(a, 2))))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def from_h():
        a = R.randint(2, 20)
        q = "正三角形的高是 %s 公分，邊長是多少公分？" % r3(F(a, 2))
        return mcq(q, "%d 公分" % a, ["%s 公分" % x for x in (num(a // 2) if a % 2 == 0 else fr(a, 2), r3(a), str(a + 1), str(2 * a))], "高 ＝ <span class='fr'><span class='fn'>√3</span><span class='fd'>2</span></span> × 邊長，邊長 ＝ %s ÷ <span class='fr'><span class='fn'>√3</span><span class='fd'>2</span></span> ＝ %d。" % (r3(F(a, 2)), a))

    def from_a():
        a = R.randint(2, 20)
        A = F(a * a, 4)
        q = "正三角形的面積是 %s 平方公分，邊長是多少公分？" % r3(A)
        return mcq(q, "%d 公分" % a, ["%s 公分" % x for x in (str(a * a // 4) if a % 2 == 0 and a * a // 4 != a else str(a + 2), str(2 * a), str(a + 1), r3(a))], "<span class='fr'><span class='fn'>√3</span><span class='fd'>4</span></span> × 邊長<sup>2</sup> ＝ %s，邊長<sup>2</sup> ＝ %d，邊長 ＝ %d。" % (r3(A), a * a, a))
    return pick_unique(R, from_h, 10, seen) + pick_unique(R, from_a, 10, seen)


def s4(seen):
    def hexa():
        a = R.randint(2, 12)
        A = F(6 * a * a, 4)
        q = "邊長 %d 公分的正六邊形，面積是多少平方公分？（正六邊形可分成 6 個正三角形）" % a
        return mcq(q, "%s 平方公分" % r3(A), ["%s 平方公分" % r3(x) for x in (F(a * a, 4), F(6 * a * a, 2), F(3 * a * a, 4), 6 * a)], "6 × <span class='fr'><span class='fn'>√3</span><span class='fd'>4</span></span> × %d<sup>2</sup> ＝ %s。" % (a, r3(A)))

    def rhom():
        a = R.randint(2, 16)
        A = F(2 * a * a, 4)
        q = "菱形的邊長是 %d 公分，有一個內角是 60°，面積是多少平方公分？" % a
        return mcq(q, "%s 平方公分" % r3(A), ["%s 平方公分" % r3(x) for x in (F(a * a, 4), a * a, F(a, 2))] + ["%d 平方公分" % (a * a)], "連短對角線，菱形分成 2 個邊長 %d 的正三角形：2 × <span class='fr'><span class='fn'>√3</span><span class='fd'>4</span></span> × %d<sup>2</sup> ＝ %s。" % (a, a, r3(A)))

    def cut():
        b = R.randint(3, 9)
        a = 2 * b
        A = F(a * a, 4) - F(b * b, 4)
        q = "邊長 %d 公分的正三角形，從一個角剪掉邊長 %d 公分的小正三角形，剩下的面積是多少平方公分？" % (a, b)
        return mcq(q, "%s 平方公分" % r3(A), ["%s 平方公分" % r3(x) for x in (F(a * a, 4), F(b * b, 4), F(a * a - b * b, 2), F((a - b) ** 2, 4))], "%s － %s ＝ %s。" % (r3(F(a * a, 4)), r3(F(b * b, 4)), r3(A)))
    return pick_unique(R, hexa, 7, seen) + pick_unique(R, rhom, 7, seen) + pick_unique(R, cut, 6, seen)


def s5(seen):
    def approx():
        a = R.choice([2, 4, 6, 8, 10, 12, 14, 16, 20])
        k = R.choice(["h", "A"])
        c = F(a, 2) if k == "h" else F(a * a, 4)
        v = float(c) * 1.732
        ans = "%.1f" % (v + 1e-9)
        q = "邊長 %d 公分的正三角形，%s約是多少？（√3 ≈ 1.732，四捨五入到小數第一位）" % (a, "高" if k == "h" else "面積")
        unit = "公分" if k == "h" else "平方公分"
        return mcq(q, "%s %s" % (ans, unit), ["%.1f %s" % (x, unit) for x in (float(c) * 2 * 1.732, float(c), v + 1, float(c) * 1.414)], "%s × 1.732 ≈ %s。" % (num(c) if c.denominator == 1 else fr(c.numerator, c.denominator), ans))

    def sign():
        a = R.choice([30, 40, 50, 60, 80])
        A = F(a * a, 4)
        q = "一面正三角形的警告標誌，邊長 %d 公分，面積約是多少平方公分？（√3 ≈ 1.73，取整數）" % a
        v = round(float(A) * 1.73)
        return mcq(q, "%s 平方公分" % num(v), ["%s 平方公分" % num(x) for x in (round(float(A) * 2 * 1.73), a * a // 2, round(a * 1.73 / 2) * a // 2 * 2 + 1, v + a)], "%s × 1.73 ≈ %s。" % (r3(A), num(v)))
    return pick_unique(R, approx, 12, seen) + pick_unique(R, sign, 5, seen) + pick_unique(R, approx, 3, seen)


def main():
    seen = set()
    sets = [("正三角形的高", s1(seen)), ("正三角形的面積", s2(seen)), ("由高或面積求邊長", s3(seen)),
            ("複合圖形", s4(seen)), ("近似值與應用", s5(seen))]
    tidy_sets(sets)
    H = "<span class='fr'><span class='fn'>√3</span><span class='fd'>2</span></span>"
    Q = "<span class='fr'><span class='fn'>√3</span><span class='fd'>4</span></span>"
    body = lesson(
        ["正三角形的高把底邊分成兩半，用畢氏定理：高 ＝ %s × 邊長。" % H,
         "<b>正三角形面積 ＝ %s × 邊長<sup>2</sup></b>（就是底 × 高 ÷ 2）。" % Q,
         "正六邊形可分成 6 個正三角形；有 60° 內角的菱形可分成 2 個正三角形。"],
        [example("邊長 6 的正三角形的高和面積", ["高 ＝ %s × 6 ＝ 3√3。" % H, "面積 ＝ 6 × 3√3 ÷ 2 ＝ 9√3。"], "3√3、9√3"),
         example("面積 16√3 的正三角形邊長", ["%s × a<sup>2</sup> ＝ 16√3，a<sup>2</sup> ＝ 64。" % Q], "8")],
        [("高 ＝ 邊長的一半", "邊長的一半是底邊被分成的長度，高是 %s × 邊長" % H),
         ("面積 ＝ %s × 邊長<sup>2</sup>" % H, "還要 ÷ 2：%s × 邊長<sup>2</sup>" % Q),
         ("面積 ＝ %s × 2 × 邊長" % Q, "是邊長的平方")])
    faq = [{"q": "正三角形面積公式怎麼來的？",
            "a": "高 ＝ √3/2 × 邊長（畢氏定理），面積 ＝ 底 × 高 ÷ 2 ＝ 邊長 × √3/2 × 邊長 ÷ 2 ＝ √3/4 × 邊長²。"},
           {"q": "答案要寫根號還是小數？",
            "a": "題目沒說時寫根號（最簡根式）最準確；題目給 √3 ≈ 1.732 時才算成小數。"},
           {"q": "八年級的平面圖形面積要學什麼？",
            "a": "108課綱 S-8-7：正三角形的高與面積公式，以及相關的複合圖形面積。"}]
    make_unit(R, "grade-8", "equilateral-triangle-area", "S-8-7",
              "平面圖形的面積：正三角形的高與面積公式，及其相關之複合圖形的面積。",
              "正三角形的高與面積",
              "八年級數學 正三角形面積 練習題｜高・√3/4 a²・正六邊形 學習單（附解答）",
              "正三角形面積",
              "國中八年級數學「正三角形的高與面積」免費學習單：正三角形的高、面積公式 √3/4×邊長²、由高或面積求邊長、正六邊形和菱形等複合圖形、近似值應用。100題線上練習馬上對答案，附可列印解答。",
              "面積 ＝ %s × 邊長<sup>2</sup>" % Q,
              "高 ＝ √3/2 × 邊長；正六邊形 ＝ 6 個正三角形。",
              body, faq, sets, 22)


if __name__ == "__main__":
    main()
