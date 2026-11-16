# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：科學記號（108課綱 N-7-8）
  python3 tools/gen_tw_math_g7_scientific_notation.py
a×10ⁿ（1≦a＜10）、大きい數→科學記號、小さい數（負の指數）→科學記號、科學記號→ふつうの數、大小比較、生活の數（距離・細菌・人口）。
誤答：a を 10 以上にする（23×10⁴）、指數を桁數にする、小さい數で指數の符號を正にする、指數だけで比較しない。
"""
import random
from decimal import Decimal as D
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets

R = random.Random(71008)
NM = Names(R)


def e10(n):
    return "10<sup>%s</sup>" % (("－%d" % -n) if n < 0 else str(n))


def sci(a, n):
    return "%s × %s" % (fmt(a), e10(n))


def fmt(x):
    x = D(x).normalize()
    t = format(x, "f")
    if "." in t:
        i, f = t.split(".")
        return "{:,}".format(int(i)) + "." + f if abs(int(i)) >= 10000 else i + "." + f
    return "{:,}".format(int(t)) if abs(int(t)) >= 10000 else t


def mant():
    d = R.choice([1, 2, 3])
    return D(R.randint(10 ** (d - 1), 10 ** d - 1)) / D(10 ** (d - 1))


def s1(seen):
    def mk():
        a = mant()
        if a < 1 or a >= 10:
            return None
        n = R.randint(3, 9)
        v = a * D(10) ** n
        if v != v.to_integral_value():
            return None
        q = "把 %s 寫成科學記號。" % fmt(v)
        ans = sci(a, n)
        return mcq(q, ans, [sci(a * 10, n - 1), sci(a, n + 1), sci(a, n - 1)], "小數點往左移 %d 位，使前面的數在 1 和 10 之間：%s。" % (n, ans))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a = mant()
        if a < 1 or a >= 10:
            return None
        n = -R.randint(2, 8)
        v = a * D(10) ** n
        q = "把 %s 寫成科學記號。" % fmt(v)
        ans = sci(a, n)
        return mcq(q, ans, [sci(a, -n), sci(a, n + 1), sci(a / 10, n + 1)], "小數點往右移 %d 位到第一個不是 0 的數字後面，指數是負的：%s。" % (-n, ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a = mant()
        if a < 1 or a >= 10:
            return None
        n = R.choice([R.randint(3, 8), -R.randint(2, 6)])
        v = a * D(10) ** n
        q = "%s 等於多少？" % sci(a, n)
        return mcq(q, fmt(v), [fmt(v * 10), fmt(v / 10), fmt(a * D(10) ** -n)], "%s：小數點往%s移 %d 位，得 %s。" % (sci(a, n), "右" if n > 0 else "左", abs(n), fmt(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a1, a2 = mant(), mant()
        n1 = R.choice([R.randint(2, 9), -R.randint(2, 8)])
        n2 = n1 + R.choice([-1, 0, 0, 1, 2])
        if a1 < 1 or a2 < 1 or (n1 == n2 and a1 == a2) or n2 in (0, 1, -1):
            return None
        v1, v2 = a1 * D(10) ** n1, a2 * D(10) ** n2
        A, B = sci(a1, n1), sci(a2, n2)
        ans = A if v1 > v2 else B
        oth = B if ans == A else A
        e = "指數不同時，指數大的比較大。" if n1 != n2 else "指數一樣時，比較前面的數。"
        return mcq("%s 和 %s，哪一個比較大？" % (A, B), ans, [oth, "一樣大", "無法比較"], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    FACTS = [("地球到太陽的平均距離約 150,000,000 公里，用科學記號表示是？", D("1.5"), 8, "公里"),
             ("光每秒約走 300,000 公里，用科學記號表示是？", D("3"), 5, "公里"),
             ("台灣人口約 23,000,000 人，用科學記號表示是？", D("2.3"), 7, "人"),
             ("一個細菌長約 0.000002 公尺，用科學記號表示是？", D("2"), -6, "公尺"),
             ("一根頭髮直徑約 0.00007 公尺，用科學記號表示是？", D("7"), -5, "公尺"),
             ("地球的質量約 5,970,000,000,000,000,000,000,000 公斤，用科學記號表示是？", D("5.97"), 24, "公斤"),
             ("一張紙的厚度約 0.0001 公尺，用科學記號表示是？", D("1"), -4, "公尺"),
             ("月球到地球的平均距離約 384,000 公里，用科學記號表示是？", D("3.84"), 5, "公里"),
             ("一粒沙的質量約 0.00065 公克，用科學記號表示是？", D("6.5"), -4, "公克"),
             ("台北 101 大樓的高度約 508 公尺，用科學記號表示是？", D("5.08"), 2, "公尺")]
    out = []
    for q, a, n, u in FACTS:
        ans = sci(a, n) + " " + u
        out.append(mcq(q, ans, [sci(a, -n) + " " + u, sci(a, n + 1) + " " + u, sci(a * 10, n - 1) + " " + u], "前面的數要在 1 和 10 之間：%s。" % ans))
    for o in out:
        seen.add(o["q"])

    def mul():
        a, b = R.choice([(2, 3), (3, 3), (2, 4), (1.5, 2), (4, 2), (2.5, 4), (1.2, 5)])
        n, m = R.randint(2, 6), R.randint(2, 6)
        p = D(str(a)) * D(str(b))
        k = n + m
        if p >= 10:
            p, k = p / 10, k + 1
        q = "（%s）×（%s）＝？（用科學記號）" % (sci(D(str(a)), n), sci(D(str(b)), m))
        ans = sci(p, k)
        return mcq(q, ans, [sci(p, n * m), sci(D(str(a)) + D(str(b)), n + m), sci(p * 10, k - 1), sci(p, k + 1), sci(p, k - 1)], "前面的數相乘、10 的次方指數相加：%s。" % ans)
    return out + pick_unique(R, mul, 10, seen)


def main():
    seen = set()
    sets = [("很大的數", s1(seen)), ("很小的數", s2(seen)), ("還原成一般的數", s3(seen)),
            ("比較大小", s4(seen)), ("生活中的科學記號", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>科學記號</b>：a × 10<sup>n</sup>，其中 <b>1 ≦ a ＜ 10</b>。",
         "很大的數：小數點往左移幾位，n 就是幾（正數）。350,000 ＝ 3.5 × 10<sup>5</sup>。",
         "很小的數：小數點往右移幾位，n 就是負幾。0.0042 ＝ 4.2 × 10<sup>－3</sup>。",
         "比大小：先比指數，指數大的比較大；指數一樣再比 a。"],
        [example("把 72,000,000 寫成科學記號。", ["小數點往左移 7 位。"], "7.2 × 10<sup>7</sup>"),
         example("把 0.00056 寫成科學記號。", ["小數點往右移 4 位。"], "5.6 × 10<sup>－4</sup>")],
        [("72,000,000 ＝ 72 × 10<sup>6</sup>", "a 要在 1 和 10 之間：7.2 × 10<sup>7</sup>"),
         ("0.00056 ＝ 5.6 × 10<sup>4</sup>", "小於 1 的數，指數是負的：10<sup>－4</sup>"),
         ("9 × 10<sup>3</sup> 比 1 × 10<sup>4</sup> 大", "先比指數：10<sup>4</sup> 比較大")])
    faq = [{"q": "為什麼要用科學記號？",
            "a": "很大或很小的數有很多個 0，不好讀也容易寫錯。科學記號可以一眼看出數的大小，例如地球到太陽約 1.5 × 10⁸ 公里。"},
           {"q": "科學記號的 a 一定要在 1 和 10 之間嗎？",
            "a": "是的，1 ≦ a ＜ 10，例如 35 × 10⁴ 要改成 3.5 × 10⁵。"},
           {"q": "七年級的科學記號要學什麼？",
            "a": "108課綱 N-7-8：以科學記號表達正數，可以是很大的數（次方為正整數），也可以是很小的數（次方為負整數）。"}]
    make_unit(R, "grade-7", "scientific-notation", "N-7-8",
              "科學記號：以科學記號表達正數，此數可以是很大的數（次方為正整數），也可以是很小的數（次方為負整數）。",
              "科學記號",
              "七年級數學 科學記號 練習題｜很大的數・很小的數・負指數 學習單（附解答）",
              "科學記號",
              "國中七年級數學「科學記號」免費學習單：把很大的數和很小的數寫成 a × 10ⁿ、還原成一般的數、比較大小，以及地球距離、細菌大小等生活中的科學記號。100題線上練習馬上對答案，附可列印解答。",
              "a × 10ⁿ，1 ≦ a ＜ 10",
              "很小的數，指數是負的。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
