# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：因式分解：提公因式與乘法公式（108課綱 A-8-4、A-8-5）
  python3 tools/gen_tw_math_g8_factoring.py
因式の意味（二次式の一次因式）、提公因式（數字と x）、平方差 a²－b²、完全平方式 a²±2ab＋b²、二段階（提公因式→公式）、因式の判定。
誤答：公因式を一部だけ出す、x²－9＝(x－3)²、x²＋9 を分解する、x²＋6x＋9＝(x＋9)²、分解の確認で展開しない。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from math import gcd
from tw_g8 import poly, pmul, sn, par, tidy_sets, pq

R = random.Random(81009)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def mono(k, d):
    return poly([k] + [0] * d)


def s1(seen):
    def mk():
        g = R.choice([2, 3, 4, 5, 6])
        a, b = nz(-6, 6), nz(-9, 9)
        if gcd(a, b) != 1:
            return None
        withx = R.random() < .6
        if withx:
            ex = [g * a, g * b, 0]
            ans = "%s（%s）" % (mono(g, 1), poly([a, b]))
            w = ["%d（%s）" % (g, poly([a, b, 0])), "x（%s）" % poly([g * a, g * b]), "%s（%s）" % (mono(g, 1), poly([a, g * b]))]
            e = "每一項都有 %d 和 x，提出 %dx：%s。" % (g, g, ans)
        else:
            c = nz(-9, 9)
            if gcd(gcd(a, b), c) != 1:
                return None
            ex = [g * a, g * b, g * c]
            ans = "%d（%s）" % (g, poly([a, b, c]))
            w = ["%d（%s）" % (g, poly([a, b, g * c])), "%d（%s）" % (g * 2 if all(x % 2 == 0 for x in (a, b, c)) else g, poly([a, b, c + 1])), "x（%s）" % poly([g * a, g * b, g * c])]
            e = "每一項都有因數 %d，提出來：%s。" % (g, ans)
        return mcq("因式分解：%s" % poly(ex), ans, w, e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(1, 6), R.randint(1, 12)
        if gcd(a, b) != 1:
            return None
        ex = [a * a, 0, -b * b]
        ans = "（%s）（%s）" % (poly([a, b]), poly([a, -b]))
        return mcq("因式分解：%s" % poly(ex), ans, ["（%s）<sup>2</sup>" % poly([a, -b]), "（%s）<sup>2</sup>" % poly([a, b]), "（%s）（%s）" % (poly([a, b * b]), poly([a, -1]))], "平方差：%s<sup>2</sup> － %d<sup>2</sup> ＝ %s。" % ("x" if a == 1 else "（%dx）" % a, b, ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(1, 5), nz(-9, 9)
        if gcd(a, b) != 1:
            return None
        ex = [a * a, 2 * a * b, b * b]
        ans = "（%s）<sup>2</sup>" % poly([a, b])
        return mcq("因式分解：%s" % poly(ex), ans, ["（%s）<sup>2</sup>" % poly([a, -b]), "（%s）<sup>2</sup>" % poly([a, b * b]), "（%s）（%s）" % (poly([a, b]), poly([a, -b])), "（%s）<sup>2</sup>" % poly([a * a, b]), "（%s）<sup>2</sup>" % poly([a, 2 * b])], "完全平方式：首、尾是平方，中間是 2 × %s × %s：%s。" % (poly([a, 0]), par(b), ans))

    def isfull():
        a, b = R.randint(1, 5), R.randint(1, 9)
        k = R.choice(["ok", "bad"])
        mid = 2 * a * b if k == "ok" else a * b
        q = "%s 是不是完全平方式？" % poly([a * a, mid, b * b])
        return mcq(q, "是" if k == "ok" else "不是", ["不是" if k == "ok" else "是", "只有 a ＝ 1 時才是", "無法判斷"], "完全平方式的中間項要是 2 × %s × %d ＝ %s。%s" % (poly([a, 0]), b, poly([2 * a * b, 0]), "" if k == "ok" else "這裡只有 %s，所以不是。" % poly([mid, 0])))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, isfull, 6, seen)


def s4(seen):
    def mk():
        g = R.choice([2, 3, 5])
        k = R.choice(["diff", "sq"])
        b = R.randint(1, 7)
        if k == "diff":
            ex = [g, 0, -g * b * b]
            ans = "%d（%s）（%s）" % (g, poly([1, b]), poly([1, -b]))
            w = ["%d（%s）" % (g, poly([1, 0, -b * b])), "（%s）（%s）" % (poly([g, b]), poly([g, -b])), "%d（%s）<sup>2</sup>" % (g, poly([1, -b]))]
            e = "先提公因式 %d：%d（%s），再用平方差：%s。分解要分到不能再分。" % (g, g, poly([1, 0, -b * b]), ans)
        else:
            s = R.choice([1, -1])
            ex = [g, 2 * g * b * s, g * b * b]
            ans = "%d（%s）<sup>2</sup>" % (g, poly([1, s * b]))
            w = ["%d（%s）" % (g, poly([1, 2 * b * s, b * b])), "（%s）<sup>2</sup>" % poly([g, s * b]), "%d（%s）<sup>2</sup>" % (g, poly([1, -s * b]))]
            e = "先提 %d，再用完全平方式：%s。" % (g, ans)
        return mcq("因式分解：%s" % poly(ex), ans, w, e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def isfac():
        a, b = nz(-7, 7), nz(-7, 7)
        if a == b:
            return None
        ex = pmul([1, a], [1, b])
        q = "下面哪一個是 %s 的因式？" % poly(ex)
        ans = poly([1, a])
        return mcq(q, ans, [x for x in (poly([1, -a]), poly([1, a + b]), poly([1, a * b]), poly([1, -b]), poly([1, a - b])) if x != poly([1, b])], "%s ＝（%s）（%s），所以 %s 是它的因式。" % (poly(ex), poly([1, a]), poly([1, b]), ans))

    def quick():
        a, b = R.choice([(51, 49), (102, 98), (75, 25), (68, 32), (125, 75), (99, 1)])
        q = "利用因式分解速算：%d<sup>2</sup> － %d<sup>2</sup>" % (a, b)
        return mcq(q, str((a + b) * (a - b)), [str((a - b) ** 2), str(a * a - b), str((a + b) * (a - b) + 100)], "平方差：（%d ＋ %d）（%d － %d）＝ %d × %d ＝ %d。" % (a, b, a, b, a + b, a - b, (a + b) * (a - b)))

    def area():
        a = R.randint(2, 9)
        q = "正方形面積是（%s）平方公分，邊長是多少公分？" % poly([1, 2 * a, a * a])
        return mcq(q, "（%s）公分" % poly([1, a]), ["（%s）公分" % poly([1, a * a]), "（%s）公分" % poly([1, 2 * a]), "（%s）公分" % poly([1, -a])], "%s ＝（%s）<sup>2</sup>，邊長是 %s。" % (poly([1, 2 * a, a * a]), poly([1, a]), poly([1, a])))
    return pick_unique(R, isfac, 8, seen) + pick_unique(R, quick, 6, seen) + pick_unique(R, area, 6, seen)


def main():
    seen = set()
    sets = [("提公因式", s1(seen)), ("平方差公式", s2(seen)), ("完全平方式", s3(seen)),
            ("先提公因式再用公式", s4(seen)), ("因式與應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>因式分解</b>：把多項式寫成幾個多項式的乘積。是乘法展開的反過程，分解完可以展開檢查。",
         "<b>提公因式</b>：每一項都有的因數（數字、x）提出來：6x<sup>2</sup> ＋ 9x ＝ 3x（2x ＋ 3）。",
         "<b>平方差</b>：a<sup>2</sup> － b<sup>2</sup> ＝（a ＋ b）（a － b）。<b>完全平方式</b>：a<sup>2</sup> ± 2ab ＋ b<sup>2</sup> ＝（a ± b）<sup>2</sup>。",
         "先提公因式，再看能不能用公式，一直分到不能再分。"],
        [example("x<sup>2</sup> － 25", ["x<sup>2</sup> － 5<sup>2</sup>。"], "（x ＋ 5）（x － 5）"),
         example("2x<sup>2</sup> － 12x ＋ 18", ["提 2：2（x<sup>2</sup> － 6x ＋ 9）。", "完全平方式。"], "2（x － 3）<sup>2</sup>")],
        [("x<sup>2</sup> － 9 ＝（x － 3）<sup>2</sup>", "平方差：（x ＋ 3）（x － 3）"),
         ("x<sup>2</sup> ＋ 6x ＋ 9 ＝（x ＋ 9）<sup>2</sup>", "（x ＋ 3）<sup>2</sup>"),
         ("2x<sup>2</sup> － 8 只寫成 2（x<sup>2</sup> － 4）", "還要再分：2（x ＋ 2）（x － 2）")])
    faq = [{"q": "因式分解要分到什麼程度？",
            "a": "要分到每個因式都不能再分為止。例如 3x² － 12 要寫成 3（x ＋ 2）（x － 2），不能停在 3（x² － 4）。"},
           {"q": "怎麼檢查因式分解對不對？",
            "a": "把分解的結果乘開，看是不是等於原來的多項式。"},
           {"q": "八年級的因式分解要學什麼？",
            "a": "108課綱 A-8-4、A-8-5：因式的意義（限制在二次多項式的一次因式），提公因式法、利用乘法公式與十字交乘法因式分解。"}]
    make_unit(R, "grade-8", "factoring", "A-8-5",
              "因式分解的方法：提公因式法；利用乘法公式與十字交乘法因式分解。",
              "因式分解：提公因式與乘法公式",
              "八年級數學 因式分解 練習題｜提公因式・平方差・完全平方式 學習單（附解答）",
              "因式分解（一）",
              "國中八年級數學「因式分解：提公因式與乘法公式」免費學習單：提公因式、平方差公式、完全平方式、先提公因式再用公式，以及判斷因式和速算應用。100題線上練習馬上對答案，附可列印解答。",
              "先提公因式，再用乘法公式",
              "a² － b² ＝（a ＋ b）（a － b）；分到不能再分為止。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
