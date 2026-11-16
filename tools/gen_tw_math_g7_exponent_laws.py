# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：指數律（108課綱 N-7-7）
  python3 tools/gen_tw_math_g7_exponent_laws.py
同底數の乘法 aᵐ×aⁿ＝aᵐ⁺ⁿ、(aᵐ)ⁿ＝aᵐⁿ、(a×b)ⁿ＝aⁿ×bⁿ、除法 aᵐ÷aⁿ＝aᵐ⁻ⁿ（m≧n）、數字例での應用・大小比較。
誤答：aᵐ×aⁿ で指數を掛ける、(aᵐ)ⁿ で指數を足す、除法で指數を割る、底數を掛け合わせる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g7 import tidy_sets

R = random.Random(71014)
NM = Names(R)


def p(b, e):
    return str(b) if e == 1 else "%s<sup>%d</sup>" % (b, e)


def s1(seen):
    def mk():
        b = R.choice([2, 3, 5, 7, 10])
        m, n = R.randint(2, 9), R.randint(2, 9)
        q = "%s × %s ＝ ？" % (p(b, m), p(b, n))
        return mcq(q, p(b, m + n), [p(b, m * n), p(b * b, m + n), p(b, abs(m - n)) if m != n else p(b, m + n + 1)], "同底數相乘，指數相加：%d ＋ %d ＝ %d。" % (m, n, m + n))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        b = R.choice([2, 3, 5, 7, 10])
        m, n = R.randint(2, 6), R.randint(2, 5)
        q = "（%s）<sup>%d</sup> ＝ ？" % (p(b, m), n)
        return mcq(q, p(b, m * n), [p(b, m + n), p(b * n, m), p(b, m ** n) if m ** n != m * n and m ** n < 100 else p(b, m * n + 1), p(b * b, m * n), p(b, m * n - 1)], "次方的次方，指數相乘：%d × %d ＝ %d。" % (m, n, m * n))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def prod():
        a, b = R.sample([2, 3, 5, 7], 2)
        n = R.randint(2, 6)
        q = "（%d × %d）<sup>%d</sup> ＝ ？" % (a, b, n)
        return mcq(q, "%s × %s" % (p(a, n), p(b, n)), ["%s × %d" % (p(a, n), b), "%d × %s" % (a, p(b, n)), "%s × %s" % (p(a, n), p(b, 2 * n))], "積的次方，每個因數都做次方：%s × %s。" % (p(a, n), p(b, n)))

    def quick():
        a, b = R.choice([(2, 5), (4, 25), (5, 2), (25, 4), (8, 125), (125, 8)])
        n = R.randint(3, 9)
        q = "%s × %s ＝ ？" % (p(a, n), p(b, n))
        v = (a * b) ** n
        return mcq(q, num(v) if v < 10 ** 12 else p(a * b, n), [p(a + b, n), p(a * b, 2 * n), p(a * b, n + 1)], "%s × %s ＝（%d × %d）<sup>%d</sup> ＝ %s。" % (p(a, n), p(b, n), a, b, n, p(a * b, n)))
    return pick_unique(R, prod, 10, seen) + pick_unique(R, quick, 10, seen)


def s4(seen):
    def mk():
        b = R.choice([2, 3, 5, 7, 10])
        n = R.randint(2, 6)
        m = n + R.randint(0, 8)
        q = "%s ÷ %s ＝ ？" % (p(b, m), p(b, n))
        ans = p(b, m - n) if m != n else "1"
        w = [p(b, m // n) if m % n == 0 and m // n != m - n else p(b, m + n), p(b, m + n), "0" if m == n else p(b, m)]
        return mcq(q, ans, w + [p(b, m - n + 1)], "同底數相除，指數相減：%d － %d ＝ %d%s。" % (m, n, m - n, "，b<sup>0</sup> ＝ 1" if m == n else ""))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mixed():
        b = R.choice([2, 3, 5])
        a, c, d = R.randint(2, 5), R.randint(2, 4), R.randint(1, 6)
        top = a * c + d
        e = R.randint(1, top - 1)
        q = "（%s）<sup>%d</sup> × %s ÷ %s ＝ ？" % (p(b, a), c, p(b, d), p(b, e))
        v = top - e
        return mcq(q, p(b, v), [p(b, a + c + d - e) if a + c + d - e >= 0 else p(b, a * c + d), p(b, a * c * d // e if (a * c * d) % e == 0 else v + 1), p(b, top + e), p(b, v + 1), p(b, v + 2)], "%d × %d ＋ %d － %d ＝ %d，答案 %s。" % (a, c, d, e, v, p(b, v)))

    def comp():
        k = R.choice([(2, 3, 3, 2), (2, 4, 4, 2), (2, 6, 3, 3), (3, 4, 9, 2), (4, 3, 8, 2), (2, 10, 4, 5), (8, 2, 2, 6)])
        b1, e1, b2, e2 = k
        m = R.randint(2, 5)
        e1, e2 = e1 * m, e2 * m
        v1, v2 = b1 ** e1, b2 ** e2
        A, B = p(b1, e1), p(b2, e2)
        if v1 == v2:
            ans = "一樣大"
            w = [A, B, "無法比較"]
        else:
            ans = A if v1 > v2 else B
            w = [B if ans == A else A, "一樣大", "無法比較"]
        return mcq("%s 和 %s，哪一個比較大？" % (A, B), ans, w, "化成同底數再比：%s ＝ %s，%s ＝ %s。" % (A, conv(b1, e1), B, conv(b2, e2)))
    return pick_unique(R, mixed, 12, seen) + pick_unique(R, comp, 8, seen)


def conv(b, e):
    for base, k in ((2, {2: 1, 4: 2, 8: 3}), (3, {3: 1, 9: 2})):
        if b in k:
            return p(base, k[b] * e)
    return p(b, e)


def main():
    seen = set()
    sets = [("同底數相乘", s1(seen)), ("次方的次方", s2(seen)), ("積的次方", s3(seen)),
            ("同底數相除", s4(seen)), ("綜合與比較", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>同底數相乘，指數相加</b>：2<sup>3</sup> × 2<sup>4</sup> ＝ 2<sup>7</sup>。",
         "<b>次方的次方，指數相乘</b>：（2<sup>3</sup>）<sup>4</sup> ＝ 2<sup>12</sup>。",
         "<b>積的次方</b>：（2 × 3）<sup>4</sup> ＝ 2<sup>4</sup> × 3<sup>4</sup>。",
         "<b>同底數相除，指數相減</b>：2<sup>7</sup> ÷ 2<sup>3</sup> ＝ 2<sup>4</sup>；2<sup>3</sup> ÷ 2<sup>3</sup> ＝ 2<sup>0</sup> ＝ 1。"],
        [example("（3<sup>2</sup>）<sup>3</sup> × 3<sup>4</sup> ÷ 3<sup>5</sup>", ["（3<sup>2</sup>）<sup>3</sup> ＝ 3<sup>6</sup>。", "6 ＋ 4 － 5 ＝ 5。"], "3<sup>5</sup>"),
         example("2<sup>10</sup> × 5<sup>10</sup>", ["＝（2 × 5）<sup>10</sup> ＝ 10<sup>10</sup>。"], "10<sup>10</sup>")],
        [("2<sup>3</sup> × 2<sup>4</sup> ＝ 2<sup>12</sup>", "相乘時指數相加：2<sup>7</sup>"),
         ("（2<sup>3</sup>）<sup>4</sup> ＝ 2<sup>7</sup>", "次方的次方指數相乘：2<sup>12</sup>"),
         ("2<sup>8</sup> ÷ 2<sup>2</sup> ＝ 2<sup>4</sup>", "指數相減，不是相除：2<sup>6</sup>")])
    faq = [{"q": "為什麼同底數相乘指數要相加？",
            "a": "2³ × 2⁴ 是 3 個 2 乘 4 個 2，一共 7 個 2 相乘，所以是 2⁷。"},
           {"q": "（2³）⁴ 和 2³ × 2⁴ 有什麼不同？",
            "a": "（2³）⁴ 是 4 個 2³ 相乘，共 12 個 2，是 2¹²；2³ × 2⁴ 只有 7 個 2，是 2⁷。"},
           {"q": "七年級的指數律要學什麼？",
            "a": "108課綱 N-7-7：以數字例表示同底數的乘法指數律和除法指數律（m、n 為非負整數，除法 m ≧ n）。"}]
    make_unit(R, "grade-7", "exponent-laws", "N-7-7",
              "指數律：以數字例表示「同底數的乘法指數律」（aᵐ×aⁿ=aᵐ⁺ⁿ、(aᵐ)ⁿ=aᵐⁿ、(a×b)ⁿ=aⁿ×bⁿ，其中 m,n 為非負整數）；以數字例表示「同底數的除法指數律」（aᵐ÷aⁿ=aᵐ⁻ⁿ，其中 m≥n 且 m,n 為非負整數）。",
              "指數律",
              "七年級數學 指數律 練習題｜同底數相乘相除・次方的次方 學習單（附解答）",
              "指數律",
              "國中七年級數學「指數律」免費學習單：同底數相乘指數相加、次方的次方指數相乘、積的次方、同底數相除指數相減與綜合比較大小。100題線上練習馬上對答案，附可列印解答。",
              "同底數相乘，指數相加",
              "次方的次方，指數相乘；同底數相除，指數相減。",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
