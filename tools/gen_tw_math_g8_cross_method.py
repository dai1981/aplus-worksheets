# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：十字交乘法（108課綱 A-8-5）
  python3 tools/gen_tw_math_g8_cross_method.py
x²＋bx＋c（積が c・和が b の二數）、符號のパターン（c＞0 なら同號、c＜0 なら異號）、ax²＋bx＋c（a≠1）、提公因式との組合せ、應用（長方形の邊）。
誤答：積と和を取り違える、符號を逆にする、a≠1 で交叉の和を確かめない。
"""
import random
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g8 import poly, pmul, sn, par, tidy_sets

R = random.Random(81010)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def f2(p, q):
    return "（%s）（%s）" % (poly(p), poly(q))


def s1(seen):
    def mk():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a == b:
            return None
        ex = pmul([1, a], [1, b])
        return mcq("因式分解：%s" % poly(ex), f2([1, a], [1, b]), [f2([1, -a], [1, -b]), f2([1, a + b], [1, 1]) if a * b != a + b else f2([1, a * b], [1, 1]), f2([1, a], [1, -b])], "找兩數：積 %d、和 %d，是 %d 和 %d：%s。" % (a * b, a + b, a, b, f2([1, a], [1, b])))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = nz(-9, 9), nz(-9, 9)
        if a == b or (a > 0 and b > 0) or a == -b:
            return None
        ex = pmul([1, a], [1, b])
        return mcq("因式分解：%s" % poly(ex), f2([1, a], [1, b]), [f2([1, -a], [1, -b]), f2([1, a], [1, -b]), f2([1, -a], [1, b])],
                   "積 %s%s，和 %s：兩數是 %s 和 %s。" % (sn(a * b), "（異號）" if a * b < 0 else "（同號）", sn(a + b), sn(a), sn(b)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        p, r = R.choice([2, 3, 5, 2, 3]), 1
        q, s = nz(-7, 7), nz(-7, 7)
        if gcd(p, abs(q)) != 1:
            return None
        ex = pmul([p, q], [r, s])
        if ex[1] == 0:
            return None
        return mcq("因式分解：%s" % poly(ex), f2([p, q], [r, s]), [f2([p, s], [r, q]), f2([p, -q], [r, -s]), f2([p, q], [r, -s])],
                   "十字交乘：%s ＝ %s × x，常數 %s ＝ %s × %s；交叉相乘相加 %s × %s ＋ %s × x ＝ %s，是中間項。" % (poly([p, 0, 0]), poly([p, 0]), sn(q * s), sn(q), sn(s), poly([p, 0]), par(s), par(q), poly([ex[1], 0])))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        g = R.choice([2, 3, -1, -2])
        a, b = nz(-6, 6), nz(-6, 6)
        if a == b:
            return None
        inner = pmul([1, a], [1, b])
        ex = [g * c for c in inner]
        gs = sn(g) if g != -1 else "－"
        ans = "%s（%s）（%s）" % (gs, poly([1, a]), poly([1, b]))
        return mcq("因式分解：%s" % poly(ex), ans, ["%s（%s）" % (gs, poly(inner)), "（%s）（%s）" % (poly([g, a]), poly([1, b])), "%s（%s）（%s）" % (gs, poly([1, -a]), poly([1, -b]))],
                   "先提出 %s：%s（%s），再十字交乘：%s。" % (sn(g), gs, poly(inner), ans))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def rect():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a == b:
            return None
        ex = pmul([1, a], [1, b])
        q = "長方形的面積是（%s）平方公分，長比寬多 %d 公分。長是多少公分？" % (poly(ex), abs(a - b))
        big = max(a, b)
        return mcq(q, "（%s）公分" % poly([1, big]), ["（%s）公分" % poly([1, min(a, b)]), "（%s）公分" % poly([1, a + b]), "（%s）公分" % poly([1, a * b])], "%s ＝ %s，長比寬多 %d，長是 %s。" % (poly(ex), f2([1, a], [1, b]), abs(a - b), poly([1, big])))

    def which():
        a, b = nz(-8, 8), nz(-8, 8)
        ex = pmul([1, a], [1, b])
        q = "%s 可以分解成（x ＋ m）（x ＋ n），m ＋ n 和 mn 各是多少？" % poly(ex)
        ans = "m ＋ n ＝ %s，mn ＝ %s" % (sn(a + b), sn(a * b))
        return mcq(q, ans, ["m ＋ n ＝ %s，mn ＝ %s" % (sn(a * b), sn(a + b)), "m ＋ n ＝ %s，mn ＝ %s" % (sn(-(a + b)), sn(a * b)), "m ＋ n ＝ %s，mn ＝ %s" % (sn(a + b), sn(-a * b))], "展開（x ＋ m）（x ＋ n）＝ x<sup>2</sup> ＋（m ＋ n）x ＋ mn，對照係數。")
    return pick_unique(R, rect, 10, seen) + pick_unique(R, which, 10, seen)


def main():
    seen = set()
    sets = [("x² ＋ bx ＋ c（都是正的）", s1(seen)), ("有負號的情形", s2(seen)), ("首項係數不是 1", s3(seen)),
            ("先提公因式", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["x<sup>2</sup> ＋ bx ＋ c：找兩個數，<b>相乘是 c、相加是 b</b>，就能寫成（x ＋ m）（x ＋ n）。",
         "符號：c 是正的，兩數同號（和 b 同號）；c 是負的，兩數一正一負。",
         "首項係數不是 1：把首項和常數項各拆成兩個因數，<b>交叉相乘再相加</b>要等於中間項。",
         "有公因式先提出來。分解完可以展開檢查。"],
        [example("x<sup>2</sup> － x － 12", ["積 －12、和 －1：－4 和 3。"], "（x － 4）（x ＋ 3）"),
         example("2x<sup>2</sup> ＋ 7x ＋ 3", ["2x<sup>2</sup> ＝ 2x × x，3 ＝ 1 × 3。", "交叉：2x × 3 ＋ 1 × x ＝ 7x。"], "（2x ＋ 1）（x ＋ 3）")],
        [("x<sup>2</sup> ＋ 5x ＋ 6 ＝（x ＋ 1）（x ＋ 6）", "1 ＋ 6 ＝ 7 不是 5：（x ＋ 2）（x ＋ 3）"),
         ("x<sup>2</sup> － x － 12 ＝（x ＋ 4）（x － 3）", "和要是 －1：（x － 4）（x ＋ 3）"),
         ("2x<sup>2</sup> ＋ 7x ＋ 3 ＝（2x ＋ 3）（x ＋ 1）", "交叉相加是 5x，不是 7x")])
    faq = [{"q": "十字交乘法怎麼用？",
            "a": "把 x² 的係數和常數項各拆成兩個因數，交叉相乘後相加，如果等於一次項係數，就找到分解的方法。"},
           {"q": "怎麼判斷兩個數的正負？",
            "a": "常數項是正的，兩數同號，而且和一次項同號；常數項是負的，兩數一正一負，絕對值大的那個和一次項同號。"},
           {"q": "八年級的十字交乘要學什麼？",
            "a": "108課綱 A-8-5：提公因式法，以及利用乘法公式與十字交乘法因式分解。"}]
    make_unit(R, "grade-8", "cross-method", "A-8-5",
              "因式分解的方法：提公因式法；利用乘法公式與十字交乘法因式分解。",
              "因式分解：十字交乘法",
              "八年級數學 十字交乘法 練習題｜x²＋bx＋c・首項不是1 學習單（附解答）",
              "十字交乘法",
              "國中八年級數學「因式分解：十字交乘法」免費學習單：x² ＋ bx ＋ c 的分解、有負號的情形、首項係數不是 1、先提公因式再十字交乘與長方形應用。100題線上練習馬上對答案，附可列印解答。",
              "兩數相乘是 c，相加是 b",
              "交叉相乘再相加要等於中間項。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
