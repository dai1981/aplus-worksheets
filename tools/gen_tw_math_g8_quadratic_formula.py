# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：配方法與公式解（108課綱 A-8-7）
  python3 tools/gen_tw_math_g8_quadratic_formula.py
配方（x² ＋ bx ＋ □ ＝（x ＋ □）²）、配方法で解く、判別式 b² － 4ac と解の個數、公式解、計算機で近似値。
誤答：配方で b を 2 で割らずに二乗、公式の －b の符號を落とす、分母を 2a でなく 2 にする、判別式を b² ＋ 4ac とする。
"""
import random
from math import gcd
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, fr
from tw_g8 import poly, sn, tidy_sets, rt, simp, qroots
from tw_g7 import par

R = random.Random(81012)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def mk():
        h = nz(-9, 9)
        b = 2 * h
        q = "配方：%s ＋ □ ＝（x %s □）<sup>2</sup>，兩個 □ 依序是？" % (poly([1, b, 0]), "＋" if h > 0 else "－")
        A = abs(h)
        return mcq(q, "%d、%d" % (A * A, A), ["%d、%d" % (b * b, abs(b)), "%d、%d" % (A, A), "%d、%d" % (A * A, abs(b)), "%d、%d" % (2 * A, A)],
                   "加上 x 係數一半的平方：（%s ÷ 2）<sup>2</sup> ＝ %d，%s ＋ %d ＝（%s）<sup>2</sup>。" % (par(b), A * A, poly([1, b, 0]), A * A, poly([1, h])))

    def to_form():
        h, k = nz(-8, 8), R.randint(-20, 20)
        c = h * h + k
        q = "把 %s 寫成（x ＋ p）<sup>2</sup> ＋ q 的形式，結果是？" % poly([1, 2 * h, c])
        ans = "（%s）<sup>2</sup>%s" % (poly([1, h]), (" ＋ %d" % k) if k > 0 else (" － %d" % -k) if k < 0 else "")
        w = ["（%s）<sup>2</sup>%s" % (poly([1, h]), (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else ""),
             "（%s）<sup>2</sup>%s" % (poly([1, 2 * h]), (" ＋ %d" % k) if k > 0 else (" － %d" % -k) if k < 0 else ""),
             "（%s）<sup>2</sup>%s" % (poly([1, -h]), (" ＋ %d" % k) if k > 0 else (" － %d" % -k) if k < 0 else ""),
             "（%s）<sup>2</sup>%s" % (poly([1, h]), (" ＋ %d" % (c + h * h)) if c + h * h > 0 else (" － %d" % -(c + h * h)))]
        return mcq(q, ans, w, "%s ＝（%s）<sup>2</sup> － %d ＋ %s ＝ %s。" % (poly([1, 2 * h, c]), poly([1, h]), h * h, par(c), ans))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, to_form, 10, seen)


def s2(seen):
    def mk():
        h = nz(-6, 6)
        k = R.choice([R.randint(1, 10) ** 2, R.choice([2, 3, 5, 6, 7, 8, 10, 12, 13, 18, 20])])
        c = h * h - k
        if c == 0:
            return None
        ans = qroots(1, 2 * h, c)
        kk, m = simp(k)
        rk = rt(kk, m)
        q = "用配方法解：%s ＝ 0" % poly([1, 2 * h, c])
        w = [qroots(1, -2 * h, c), "x ＝ %s ± %s" % (sn(-h), rt(kk * 2, m) if m > 1 else sn(2 * kk)) if m > 1 else qroots(1, 2 * h, c - 2 * h - 1),
             "x ＝ %s ＋ %s" % (sn(-h), rk), qroots(1, 2 * h, -c) or "無解"]
        return mcq(q, ans, w, "移項：%s ＝ %s，兩邊加 %d：（%s）<sup>2</sup> ＝ %d，%s ＝ ±%s，%s。" % (poly([1, 2 * h, 0]), sn(-c), h * h, poly([1, h]), k, poly([1, h]), rk, ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def disc():
        a, b, c = nz(-5, 5), R.randint(-9, 9), nz(-9, 9)
        D = b * b - 4 * a * c
        q = "方程式 %s ＝ 0 的判別式 b<sup>2</sup> － 4ac 是多少？" % poly([a, b, c])
        return mcq(q, sn(D), [sn(b * b + 4 * a * c), sn(b - 4 * a * c), sn(-D), sn(b * b - 2 * a * c), sn(D + 1)],
                   "a ＝ %s，b ＝ %s，c ＝ %s：%s<sup>2</sup> － 4 ×%s×%s ＝ %s。" % (sn(a), sn(b), sn(c), par(b), par(a), par(c), sn(D)))

    def count():
        a = nz(-4, 4)
        t = R.choice(["two", "one", "none"])
        if t == "one":
            h = nz(-6, 6)
            a = R.choice([1, 1, 4, 9]) if R.random() < .5 else 1
            s = R.choice([1, 2, 3])
            cs = [s * s, 2 * s * h, h * h]
        else:
            b, c = R.randint(-9, 9), nz(-9, 9)
            cs = [a, b, c]
        D = cs[1] ** 2 - 4 * cs[0] * cs[2]
        if (t == "two" and D <= 0) or (t == "none" and D >= 0):
            return None
        lab = {"two": "兩個相異的解", "one": "兩個相等的解（重根）", "none": "沒有解"}
        ans = lab["two" if D > 0 else "one" if D == 0 else "none"]
        q = "方程式 %s ＝ 0 有幾個解？" % poly(cs)
        return mcq(q, ans, [v for v in lab.values()] + ["無限多個解"],
                   "判別式 %s<sup>2</sup> － 4 × %s × %s ＝ %s，%s 0，所以%s。" % (par(cs[1]), par(cs[0]), par(cs[2]), sn(D), "＞" if D > 0 else "＝" if D == 0 else "＜", ans))
    return pick_unique(R, disc, 10, seen) + pick_unique(R, count, 10, seen)


def s4(seen):
    def mk():
        a = R.choice([1, 1, 2, 2, 3])
        b, c = R.randint(-9, 9), nz(-9, 9)
        D = b * b - 4 * a * c
        if D <= 0 or gcd(gcd(a, abs(b)), abs(c)) > 1:
            return None
        ans = qroots(a, b, c)
        kk, m = simp(D)
        rad = rt(kk, m)
        if m == 1:
            x1, x2 = sorted([F(-b + kk, a), F(-b - kk, a)])
            w = [qroots(a, -b, c), qroots(a, b, -c), "x ＝ %s 或 %s" % (sn(x1), sn(x2)), "x ＝ %s" % sn(F(-b + kk, 2 * a))]
        else:
            w = [qroots(a, -b, c), "x ＝ " + fr("%s ± %s" % (sn(-b), rad), sn(a)) if a > 1 else "x ＝ %s ± %s" % (sn(-b), rad),
                 qroots(a, b, -c), "x ＝ " + fr("%s ＋ %s" % (sn(-b), rad), 2 * a)]
        raw = "x ＝ " + fr("%s ± √%d" % (sn(-b), D), 2 * a)
        tail = "" if raw == ans else "，%s" % ans
        q = "用公式解：%s ＝ 0" % poly([a, b, c])
        return mcq(q, ans, w, "a ＝ %s，b ＝ %s，c ＝ %s，b<sup>2</sup> － 4ac ＝ %s，%s%s。" % (sn(a), sn(b), sn(c), sn(D), raw, tail))
    return pick_unique(R, mk, 20, seen)


SQ = {2: 1.414, 3: 1.732, 5: 2.236, 6: 2.449, 7: 2.646, 10: 3.162, 11: 3.317, 13: 3.606}


def s5(seen):
    def approx():
        h = nz(-5, 5)
        m = R.choice(list(SQ))
        c = h * h - m
        if c == 0:
            return None
        v = -h + SQ[m]
        if v <= 0:
            return None
        q = "方程式 %s ＝ 0 的正數解約是多少？（√%d ≈ %s，四捨五入到小數第一位）" % (poly([1, 2 * h, c]), m, SQ[m])
        ans = "%.1f" % (v + 1e-9)
        return mcq(q, ans, ["%.1f" % (h + SQ[m]) if h + SQ[m] > 0 else "%.1f" % (SQ[m] + 1), "%.1f" % SQ[m], "%.1f" % (v + 1), "%.1f" % (abs(-h - SQ[m]))],
                   "配方：（%s）<sup>2</sup> ＝ %d，x ＝ %s ± √%d，正數解 %s ＋ %s ≈ %s。" % (poly([1, h]), m, sn(-h), m, sn(-h), SQ[m], ans))

    def area():
        w = R.randint(4, 20)
        d = R.randint(2, 9)
        A = w * (w + d)
        q = "一塊長方形菜園，長比寬多 %d 公尺，面積 %d 平方公尺。用公式解 x<sup>2</sup> ＋ %dx － %d ＝ 0，寬是多少公尺？" % (d, A, d, A)
        return mcq(q, "%d 公尺" % w, ["%d 公尺" % x for x in (w + d, w - 1, w + 1, d)], "判別式 %d<sup>2</sup> ＋ 4 × %d ＝ %d ＝ %d<sup>2</sup>，x ＝ %s，寬取正數 %d 公尺。" % (d, A, d * d + 4 * A, 2 * w + d, fr("－%d ± %d" % (d, 2 * w + d), 2), w))

    def throw_():
        v = R.choice([10, 15, 20, 25])
        q = "球以每秒 %d 公尺往上丟，t 秒後高度是（%dt － 5t<sup>2</sup>）公尺。球幾秒後回到地面（高度 0）？" % (v, v)
        T = v // 5
        return mcq(q, "%d 秒" % T, ["%d 秒" % x for x in (T * 2 if T * 2 != T else T + 1, v, T // 2 if T // 2 not in (0, T) else T + 2, T + 1)],
                   "%dt － 5t<sup>2</sup> ＝ 0，5t（%d － t）＝ 0，t ＝ 0（剛丟出）或 %d，所以 %d 秒後落地。" % (v, T, T, T))
    return pick_unique(R, approx, 8, seen) + pick_unique(R, area, 8, seen) + pick_unique(R, throw_, 4, seen)


def main():
    seen = set()
    sets = [("配方", s1(seen)), ("配方法解方程式", s2(seen)), ("判別式和解的個數", s3(seen)),
            ("公式解", s4(seen)), ("近似值與應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>配方</b>：x<sup>2</sup> ＋ bx 加上（<span class='fr'><span class='fn'>b</span><span class='fd'>2</span></span>）<sup>2</sup>，就變成（x ＋ <span class='fr'><span class='fn'>b</span><span class='fd'>2</span></span>）<sup>2</sup>。",
         "<b>配方法</b>：移項 → 兩邊加同一個數配成平方 → 開平方（記得 ±）。",
         "<b>公式解</b>：ax<sup>2</sup> ＋ bx ＋ c ＝ 0 的解是 x ＝ <span class='fr'><span class='fn'>－b ± √（b<sup>2</sup> － 4ac）</span><span class='fd'>2a</span></span>。",
         "<b>判別式</b> b<sup>2</sup> － 4ac：＞ 0 有兩個相異解，＝ 0 有重根，＜ 0 沒有解。"],
        [example("用配方法解 x<sup>2</sup> ＋ 6x ＋ 2 ＝ 0", ["x<sup>2</sup> ＋ 6x ＝ －2，兩邊加 9：（x ＋ 3）<sup>2</sup> ＝ 7。", "x ＋ 3 ＝ ±√7。"], "x ＝ －3 ± √7"),
         example("用公式解 2x<sup>2</sup> － 3x － 1 ＝ 0", ["a ＝ 2，b ＝ －3，c ＝ －1，b<sup>2</sup> － 4ac ＝ 9 ＋ 8 ＝ 17。"], "x ＝ " + fr("3 ± √17", 4))],
        [("x<sup>2</sup> ＋ 6x 加上 36 配方", "加的是（6 ÷ 2）<sup>2</sup> ＝ 9"),
         ("公式中的 －b 寫成 b", "b ＝ －3 時，－b ＝ 3"),
         ("分母寫成 2", "分母是 2a，a ＝ 2 時分母是 4")])
    faq = [{"q": "什麼時候用因式分解，什麼時候用公式解？",
            "a": "能很快分解的先用因式分解；不容易分解或答案有根號時，用配方法或公式解，公式解一定能用。"},
           {"q": "判別式小於 0 是什麼意思？",
            "a": "表示找不到任何數的平方是負數，所以方程式沒有解（國中範圍）。"},
           {"q": "八年級的配方法和公式解要學什麼？",
            "a": "108課綱 A-8-7：用因式分解、配方法、公式解解一元二次方程式，做應用問題，並用計算機算根的近似值。"}]
    make_unit(R, "grade-8", "quadratic-formula", "A-8-7",
              "一元二次方程式的解法與應用：利用因式分解、配方法、公式解一元二次方程式；應用問題；使用計算機計算一元二次方程式根的近似值。",
              "配方法與公式解",
              "八年級數學 配方法與公式解 練習題｜判別式・一元二次方程式 學習單（附解答）",
              "配方法與公式解",
              "國中八年級數學「配方法與公式解」免費學習單：配方、用配方法解一元二次方程式、判別式和解的個數、公式解、近似值與應用題。100題線上練習馬上對答案，附可列印解答。",
              "x ＝ <span class='fr'><span class='fn'>－b ± √（b<sup>2</sup> － 4ac）</span><span class='fd'>2a</span></span>",
              "先看判別式 b² － 4ac：＞ 0 兩解，＝ 0 重根，＜ 0 無解。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
