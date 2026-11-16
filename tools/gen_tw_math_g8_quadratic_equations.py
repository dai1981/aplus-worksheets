# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：一元二次方程式與因式分解解法（108課綱 A-8-6、A-8-7）
  python3 tools/gen_tw_math_g8_quadratic_equations.py
一元二次方程式の判斷、解の確認（代入）、x(x－a)＝0、(x－a)(x－b)＝0（AB＝0 なら A＝0 或 B＝0）、十字交乘で解く、平方根法 x²＝k・(x＋a)²＝k、情境から式を立てる。
誤答：x²＝3x を x で割って解を一つ落とす、(x－2)(x＋3)＝0 の解を 2、3 とする、x²＝9 の解を 3 だけにする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g8 import poly, pmul, sn, tidy_sets, rt, simp
from tw_g7 import par

R = random.Random(81011)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def sol(a, b):
    a, b = sorted([a, b])
    return "x ＝ %s 或 %s" % (sn(a), sn(b)) if a != b else "x ＝ %s（重根）" % sn(a)


def s1(seen):
    def which():
        good = poly([nz(-5, 5), R.randint(-9, 9), R.randint(-9, 9)]) + " ＝ 0"
        bads = [poly([nz(-5, 5), nz(-9, 9)]) + " ＝ 0", poly([1, 0, 0, nz(-9, 9)]) + " ＝ 0", "x<sup>2</sup> ＋ %dx ＝ x<sup>2</sup> － %d" % (R.randint(2, 9), R.randint(1, 9)), "<span class='fr'><span class='fn'>1</span><span class='fd'>x<sup>2</sup></span></span> ＝ %d" % R.randint(1, 9)]
        R.shuffle(bads)
        eqs = [good] + bads[:3]
        R.shuffle(eqs)
        L = "甲乙丙丁"
        q = "下面哪一個是一元二次方程式？<br>" + "<br>".join("%s　%s" % (L[i], e) for i, e in enumerate(eqs))
        k = eqs.index(good)
        return mcq(q, L[k], [c for c in L if c != L[k]], "整理後只有一個未知數、最高次數是 2（x<sup>2</sup> 的係數不是 0）：%s。" % good)

    def isroot():
        a, b = nz(-7, 7), nz(-7, 7)
        ex = pmul([1, -a], [1, -b])
        q = "下面哪一個是 %s ＝ 0 的解？" % poly(ex)
        ws = ["x ＝ %s" % sn(x) for x in (-a, -b, a + b, a * b, a + 1, a - 1) if x not in (a, b)]
        sub = par(a) + "<sup>2</sup>" + ((" ＋ %s × %s" % (par(ex[1]), par(a))) if ex[1] else "") + " ＋ %s" % par(ex[2])
        return mcq(q, "x ＝ %s" % sn(a), ws, "代入 x ＝ %s：%s ＝ 0，等式成立，所以是解。" % (sn(a), sub))

    return pick_unique(R, which, 6, seen) + pick_unique(R, isroot, 14, seen)


def s2(seen):
    def mk():
        a, b = nz(-9, 9), nz(-9, 9)
        if a == b:
            return None
        q = "解方程式：（%s）（%s）＝ 0" % (poly([1, -a]), poly([1, -b]))
        return mcq(q, sol(a, b), [sol(-a, -b), sol(a, -b) if a != -b else sol(a + 1, b), "x ＝ %s" % sn(a)], "兩數相乘是 0，至少一個是 0：%s ＝ 0 或 %s ＝ 0，%s。" % (poly([1, -a]), poly([1, -b]), sol(a, b)))

    def common():
        a = nz(-9, 9)
        k = R.choice([1, 2, 3])
        q = "解方程式：%s ＝ %s" % (poly([k, 0, 0]), poly([k * a, 0]))
        return mcq(q, sol(0, a), ["x ＝ %s" % sn(a), sol(0, -a), "x ＝ 0"], "移項：%s ＝ 0，提公因式：%sx（x%s）＝ 0，%s。不能兩邊同除以 x，會漏掉 x ＝ 0。" % (poly([k, -k * a, 0]), "" if k == 1 else str(k), (" － %d" % a) if a > 0 else (" ＋ %d" % -a), sol(0, a)))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, common, 8, seen)


def s3(seen):
    def mk():
        a, b = nz(-9, 9), nz(-9, 9)
        p = R.choice([1, 1, 2])
        if p == 2:
            if a % 2 == 0:
                return None
            ex = pmul([2, -a], [1, -b])
            if a % 2:
                ans = "x ＝ %s 或 %s" % (sn(b), "<span class='fr'><span class='fn'>%s</span><span class='fd'>2</span></span>" % sn(a) if a > 0 else "－<span class='fr'><span class='fn'>%d</span><span class='fd'>2</span></span>" % -a)
            else:
                ans = sol(a // 2, b)
            q = "解方程式：%s ＝ 0" % poly(ex)
            return mcq(q, ans, [sol(-b, a), sol(a, b) if a != b else sol(a, b + 1), "x ＝ %s" % sn(b), sol(-b, -a)], "十字交乘：（%s）（%s）＝ 0，%s。" % (poly([2, -a]), poly([1, -b]), ans))
        if a == b:
            return None
        ex = pmul([1, -a], [1, -b])
        q = "解方程式：%s ＝ 0" % poly(ex)
        return mcq(q, sol(a, b), [sol(-a, -b), sol(-a, b), sol(a, -b), "x ＝ %s" % sn(a)], "因式分解：（%s）（%s）＝ 0，%s。" % (poly([1, -a]), poly([1, -b]), sol(a, b)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        k = R.choice(["sq", "shift"])
        if k == "sq":
            n = R.randint(1, 15)
            sq = R.random() < .7
            v = n * n if sq else R.choice([2, 3, 5, 7, 8, 12, 18, 20])
            q = "解方程式：x<sup>2</sup> ＝ %d" % v
            if sq:
                ans = "x ＝ ±%d" % n
                w = ["x ＝ %d" % n, "x ＝ ±%d" % (v // 2) if v > 2 else "x ＝ ±%d" % (n + 1), "x ＝ %d" % v]
            else:
                kk, m = simp(v)
                ans = "x ＝ ±%s" % rt(kk, m)
                w = ["x ＝ %s" % rt(kk, m), "x ＝ ±%d" % (v // 2), "x ＝ ±%d" % v]
            return mcq(q, ans, w, "x 是 %d 的平方根，有正負兩個：%s。" % (v, ans))
        a, n = nz(-6, 6), R.randint(1, 8)
        q = "解方程式：（%s）<sup>2</sup> ＝ %d" % (poly([1, a]), n * n)
        return mcq(q, sol(-a + n, -a - n), [sol(a + n, a - n), "x ＝ %s" % sn(-a + n), sol(n - a, n + a) if n != 0 else "x ＝ 0"], "%s ＝ ±%d，x ＝ %s ± %d，%s。" % (poly([1, a]), n, sn(-a), n, sol(-a + n, -a - n)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def num_():
        a = R.randint(2, 12)
        k = R.choice(["sq", "consec"])
        if k == "sq":
            q = "一個正數的平方等於它的 %d 倍。這個數是多少？" % a
            return mcq(q, str(a), ["0", str(a * a), str(a // 2) if a % 2 == 0 else str(a + 1)], "x<sup>2</sup> ＝ %dx，x（x － %d）＝ 0，x ＝ 0 或 %d；題目說正數，所以是 %d。" % (a, a, a, a))
        n = R.randint(3, 20)
        q = "兩個連續正整數的積是 %d，較小的數是多少？" % (n * (n + 1))
        return mcq(q, str(n), [str(n + 1), str(-(n + 1)), str(n * (n + 1) // 2)], "x（x ＋ 1）＝ %d，x<sup>2</sup> ＋ x － %d ＝ 0，（x ＋ %d）（x － %d）＝ 0，正整數 x ＝ %d。" % (n * (n + 1), n * (n + 1), n + 1, n, n))

    def rect():
        w = R.randint(3, 15)
        d = R.randint(1, 8)
        A = w * (w + d)
        q = "長方形的長比寬多 %d 公分，面積是 %d 平方公分。寬是多少公分？" % (d, A)
        return mcq(q, "%d 公分" % w, ["%d 公分" % x for x in (w + d, A // d if A % d == 0 and A // d not in (w, w + d) else w + 2, w - 1)], "x（x ＋ %d）＝ %d，（x ＋ %d）（x － %d）＝ 0，寬是正數 %d 公分。" % (d, A, w + d, w, w))
    return pick_unique(R, num_, 10, seen) + pick_unique(R, rect, 10, seen)


def main():
    seen = set()
    sets = [("認識一元二次方程式", s1(seen)), ("AB ＝ 0 和提公因式", s2(seen)), ("用因式分解解", s3(seen)),
            ("平方根法", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["整理後是 ax<sup>2</sup> ＋ bx ＋ c ＝ 0（a ≠ 0）的方程式叫<b>一元二次方程式</b>，最多有兩個解。",
         "<b>A × B ＝ 0，則 A ＝ 0 或 B ＝ 0</b>：先移項使右邊為 0，再因式分解。",
         "<b>平方根法</b>：x<sup>2</sup> ＝ k（k ＞ 0），x ＝ ±√k；（x ＋ a）<sup>2</sup> ＝ k，x ＋ a ＝ ±√k。",
         "不要把兩邊同除以 x，會漏掉 x ＝ 0 這個解。"],
        [example("x<sup>2</sup> － 5x ＋ 6 ＝ 0", ["（x － 2）（x － 3）＝ 0。"], "x ＝ 2 或 3"),
         example("（x － 1）<sup>2</sup> ＝ 16", ["x － 1 ＝ ±4。"], "x ＝ 5 或 －3")],
        [("x<sup>2</sup> ＝ 3x，兩邊除以 x 得 x ＝ 3", "移項提公因式：x ＝ 0 或 3"),
         ("（x － 2）（x ＋ 3）＝ 0，x ＝ 2 或 3", "x ＋ 3 ＝ 0，x ＝ －3"),
         ("x<sup>2</sup> ＝ 9，x ＝ 3", "還有 －3：x ＝ ±3")])
    faq = [{"q": "一元二次方程式為什麼常有兩個解？",
            "a": "因為可以分解成兩個一次式相乘等於 0，每個一次式為 0 都會得到一個解；兩個一樣時叫重根。"},
           {"q": "解應用題時，為什麼有時候只取一個解？",
            "a": "要看題目意思，例如長度、人數必須是正數，負的解就不合，要捨去。"},
           {"q": "八年級的一元二次方程式要學什麼？",
            "a": "108課綱 A-8-6、A-8-7：一元二次方程式及其解的意義，利用因式分解、配方法、公式解來解一元二次方程式和應用問題。"}]
    make_unit(R, "grade-8", "quadratic-equations", "A-8-6",
              "一元二次方程式的意義：一元二次方程式及其解，具體情境中列出一元二次方程式。",
              "一元二次方程式：因式分解解法",
              "八年級數學 一元二次方程式 練習題｜因式分解解法・平方根法 學習單（附解答）",
              "一元二次方程式（一）",
              "國中八年級數學「一元二次方程式：因式分解解法」免費學習單：認識一元二次方程式和解、AB＝0 的解法、用因式分解解方程式、平方根法與數字、長方形應用題。100題線上練習馬上對答案，附可列印解答。",
              "A × B ＝ 0，則 A ＝ 0 或 B ＝ 0",
              "先移項使右邊為 0，再因式分解；不要除以 x。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
