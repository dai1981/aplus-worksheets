# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：二元一次聯立方程式的意義（108課綱 A-7-4）
  python3 tools/gen_tw_math_g7_systems_of_equations.py
二元一次方程式とその解（解は無數にある）、x を決めて y を求める、聯立方程式の解（兩式を同時に滿たす）、情境から聯立方程式を立てる。
誤答：一方の式だけ満たす組を解とする、x と y を逆に代入する、情境で係數と變數を取り違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import sn, par, tidy_sets, term, const

R = random.Random(71015)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def eq2(a, b, c):
    return "%s%s ＝ %s" % (term(a, "x", True), term(b, "y"), sn(c))


def pt(x, y):
    return "x ＝ %s、y ＝ %s" % (sn(x), sn(y))


def s1(seen):
    def mk():
        a, b = nz(-5, 5), nz(-5, 5)
        x, y = nz(-6, 6), nz(-6, 6)
        c = a * x + b * y
        q = "下面哪一組是二元一次方程式 %s 的解？" % eq2(a, b, c)
        cands = [(y, x), (x, -y), (-x, y), (x + 1, y)]
        w = [pt(u, v) for u, v in cands if a * u + b * v != c][:3]
        return mcq(q, pt(x, y), w, "代入檢查：%s × %s ＋ %s × %s ＝ %s，等號成立。" % (par(a), par(x), par(b), par(y), sn(c)))

    def many():
        a, b, c = R.randint(1, 5), R.randint(1, 5), R.randint(5, 30)
        q = "二元一次方程式 %s 有幾組解？" % eq2(a, b, c)
        return mcq(q, "無限多組", ["只有 1 組", "2 組", "沒有解"], "x 可以取任何數，每一個 x 都可以算出對應的 y，所以有無限多組解。")
    return pick_unique(R, mk, 16, seen) + pick_unique(R, many, 4, seen)


def s2(seen):
    def mk():
        a, b = nz(-6, 6), R.choice([1, -1, 2, -2, 3])
        x, y = nz(-6, 6), nz(-8, 8)
        c = a * x + b * y
        q = "在 %s 中，當 x ＝ %s 時，y ＝ ？" % (eq2(a, b, c), sn(x))
        return mcq(q, sn(y), [sn(-y), sn(y + 1), sn(c - a * x)] if b != 1 else [sn(-y), sn(y + 1), sn(c + a * x)], "代入 x：%s × %s ＋ %s ＝ %s，解出 y ＝ %s。" % (par(a), par(x), term(b, "y", True), sn(c), sn(y)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        x, y = nz(-6, 6), nz(-6, 6)
        a1, b1, a2, b2 = nz(-4, 4), nz(-4, 4), nz(-4, 4), nz(-4, 4)
        if a1 * b2 == a2 * b1:
            return None
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        q = "下面哪一組是聯立方程式 ｛%s；%s｝ 的解？" % (eq2(a1, b1, c1), eq2(a2, b2, c2))
        bad = []
        for u, v in [(y, x), (x, -y), (-x, y), (x + 1, y), (x, y + 1), (x - 1, y + 1)]:
            if (u, v) != (x, y) and not (a1 * u + b1 * v == c1 and a2 * u + b2 * v == c2):
                bad.append(pt(u, v))
        return mcq(q, pt(x, y), bad[:3], "代入兩個式子都要成立：%s 時，兩式都成立。" % pt(x, y))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        k = R.choice(["ticket", "animal", "coin", "pen"])
        if k == "ticket":
            p1, p2 = R.choice([(250, 150), (300, 180), (200, 100)])
            n, t = R.randint(5, 12), None
            a = R.randint(1, n - 1)
            t = p1 * a + p2 * (n - a)
            q = "全票 %d 元、半票 %d 元，共買 %d 張，付 %d 元。設全票 x 張、半票 y 張，哪一組聯立方程式正確？" % (p1, p2, n, t)
            ans = "｛x ＋ y ＝ %d；%dx ＋ %dy ＝ %d｝" % (n, p1, p2, t)
            w = ["｛x ＋ y ＝ %d；%dx ＋ %dy ＝ %d｝" % (t, p1, p2, n), "｛x ＋ y ＝ %d；%dx ＋ %dy ＝ %d｝" % (n, p2, p1, t), "｛%dx ＋ %dy ＝ %d；x － y ＝ %d｝" % (p1, p2, t, n)]
        elif k == "animal":
            h = R.randint(10, 35)
            r = R.randint(1, h - 1)
            legs = 2 * (h - r) + 4 * r
            q = "雞和兔共 %d 隻，腳共 %d 隻。設雞 x 隻、兔 y 隻，哪一組聯立方程式正確？" % (h, legs)
            ans = "｛x ＋ y ＝ %d；2x ＋ 4y ＝ %d｝" % (h, legs)
            w = ["｛x ＋ y ＝ %d；4x ＋ 2y ＝ %d｝" % (h, legs), "｛x ＋ y ＝ %d；2x ＋ 4y ＝ %d｝" % (legs, h), "｛2x ＋ 4y ＝ %d；x － y ＝ %d｝" % (h, legs)]
        elif k == "coin":
            n = R.randint(8, 25)
            a = R.randint(1, n - 1)
            t = 10 * a + 5 * (n - a)
            q = "10 元和 5 元硬幣共 %d 枚，合計 %d 元。設 10 元 x 枚、5 元 y 枚，哪一組聯立方程式正確？" % (n, t)
            ans = "｛x ＋ y ＝ %d；10x ＋ 5y ＝ %d｝" % (n, t)
            w = ["｛x ＋ y ＝ %d；5x ＋ 10y ＝ %d｝" % (n, t), "｛x ＋ y ＝ %d；10x ＋ 5y ＝ %d｝" % (t, n), "｛10x ＋ 5y ＝ %d；x ＝ y ＋ %d｝" % (t, n)]
        else:
            s_, d = R.randint(20, 60), R.randint(2, 10)
            if (s_ + d) % 2:
                return None
            q = "兩數的和是 %d，差是 %d（x 比 y 大）。哪一組聯立方程式正確？" % (s_, d)
            ans = "｛x ＋ y ＝ %d；x － y ＝ %d｝" % (s_, d)
            w = ["｛x ＋ y ＝ %d；y － x ＝ %d｝" % (s_, d), "｛x － y ＝ %d；x ＋ y ＝ %d｝" % (s_, d), "｛x ＋ y ＝ %d；xy ＝ %d｝" % (s_, d)]
        return mcq(q, ans, w, "找出兩個等量關係，各寫成一個方程式：%s。" % ans)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def check():
        x, y = R.randint(1, 15), R.randint(1, 15)
        who = NM.next()
        a1, b1, a2, b2 = R.randint(1, 4), R.randint(1, 4), R.randint(1, 4), -R.randint(1, 4)
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        u, v = x + R.choice([1, -1]), y
        ok1 = a1 * u + b1 * v == c1
        ok2 = a2 * u + b2 * v == c2
        q = "%s說 %s 是 ｛%s；%s｝ 的解。對嗎？" % (who, pt(u, v), eq2(a1, b1, c1), eq2(a2, b2, c2))
        ans = "不對，兩式都要成立才是解"
        return mcq(q, ans, ["對", "對，只要一個式子成立就好", "無法判斷"], "代入第一式得 %s、第二式得 %s，和右邊不一樣，所以不是解。正確解是 %s。" % (sn(a1 * u + b1 * v), sn(a2 * u + b2 * v), pt(x, y)))

    def find_k():
        x, y = nz(-5, 5), nz(-5, 5)
        a, k = nz(-5, 5), nz(-6, 6)
        c = a * x + k * y
        q = "x ＝ %s、y ＝ %s 是 %sx ＋ ky ＝ %s 的解，k ＝ ？" % (sn(x), sn(y), sn(a) if abs(a) != 1 else ("－" if a < 0 else ""), sn(c))
        return mcq(q, sn(k), [sn(-k), sn(k + 1), sn(c - a * x)], "代入：%s × %s ＋ k × %s ＝ %s，解得 k ＝ %s。" % (par(a), par(x), par(y), sn(c), sn(k)))
    return pick_unique(R, check, 8, seen) + pick_unique(R, find_k, 12, seen)


def main():
    seen = set()
    sets = [("二元一次方程式的解", s1(seen)), ("已知 x 求 y", s2(seen)), ("聯立方程式的解", s3(seen)),
            ("列出聯立方程式", s4(seen)), ("判斷與求未知係數", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["含有兩個未知數、次數都是 1 的方程式，叫做<b>二元一次方程式</b>，例如 2x ＋ y ＝ 7。它有<b>無限多組解</b>。",
         "把兩個二元一次方程式合在一起，就是<b>二元一次聯立方程式</b>。",
         "聯立方程式的解：<b>同時讓兩個式子都成立</b>的 x、y。",
         "情境題：找出<b>兩個</b>等量關係（例如總個數、總金額），各寫一個方程式。"],
        [example("x ＝ 2、y ＝ 3 是不是 ｛x ＋ y ＝ 5；2x － y ＝ 1｝ 的解？", ["2 ＋ 3 ＝ 5 成立。", "2 × 2 － 3 ＝ 1 成立。"], "是")],
        [("只代入一個式子成立就說是解", "兩個式子都要成立"),
         ("x ＝ 2、y ＝ 3 代成 x ＝ 3、y ＝ 2", "x、y 不能代反"),
         ("雞兔問題寫 4x ＋ 2y（x 是雞）", "雞 2 隻腳：2x ＋ 4y")])
    faq = [{"q": "二元一次方程式為什麼有無限多組解？",
            "a": "因為 x 可以任意選，每選一個 x 就能算出一個 y，所以有無限多組。加上第二個方程式，才會限制到只有一組解。"},
           {"q": "怎麼判斷一組數是不是聯立方程式的解？",
            "a": "把 x、y 代入兩個方程式，兩個都成立才是解。"},
           {"q": "七年級的二元一次聯立方程式要學什麼？",
            "a": "108課綱 A-7-4：二元一次方程式及其解的意義，二元一次聯立方程式及其解的意義，並在具體情境中列出方程式。"}]
    make_unit(R, "grade-7", "systems-of-equations", "A-7-4",
              "二元一次聯立方程式的意義：二元一次方程式及其解的意義；具體情境中列出二元一次方程式；二元一次聯立方程式及其解的意義；具體情境中列出二元一次聯立方程式。",
              "二元一次聯立方程式的意義",
              "七年級數學 二元一次聯立方程式 練習題｜解的意義・列式 學習單（附解答）",
              "二元一次聯立方程式",
              "國中七年級數學「二元一次聯立方程式的意義」免費學習單：二元一次方程式的解、已知 x 求 y、聯立方程式的解、用票價、雞兔、硬幣列出聯立方程式與求未知係數。100題線上練習馬上對答案，附可列印解答。",
              "聯立方程式的解要讓兩個式子都成立",
              "二元一次方程式有無限多組解。",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
