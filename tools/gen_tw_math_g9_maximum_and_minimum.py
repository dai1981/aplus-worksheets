# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：二次函數的最大值與最小值（108課綱 F-9-2）
  python3 tools/gen_tw_math_g9_maximum_and_minimum.py
頂點形の最大値・最小値とそのときの x、一般式を配方して極値、開口方向で最大か最小か、圍籬面積・投球高度・利潤の應用。
誤答：a ＞ 0 で最大値とする、極値を h にする、x の値と y の値を取り違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, num
from tw_g7 import tidy_sets, sn
from tw_g8 import poly
from tw_g9 import vform

R = random.Random(81114)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def mk():
        a, h, k = nz(-5, 5), R.randint(-8, 8), R.randint(-12, 12)
        kind = "最小值" if a > 0 else "最大值"
        q = "%s 有最大值還是最小值？是多少？" % vform(a, h, k)
        ans = "%s %s" % (kind, sn(k))
        other = "最大值" if a > 0 else "最小值"
        return mcq(q, ans, ["%s %s" % (other, sn(k)), "%s %s" % (kind, sn(h)), "%s %s" % (kind, sn(-k)) if k else "%s %s" % (kind, sn(a))], "a ＝ %s %s 0，開口向%s，頂點是%s點：x ＝ %s 時有%s %s。" % (sn(a), "＞" if a > 0 else "＜", "上" if a > 0 else "下", "最低" if a > 0 else "最高", sn(h), kind, sn(k)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, h, k = nz(-5, 5), nz(-8, 8), R.randint(-12, 12)
        kind = "最小值" if a > 0 else "最大值"
        q = "%s，當 x 是多少時有%s？" % (vform(a, h, k), kind)
        return mcq(q, "x ＝ %s" % sn(h), ["x ＝ %s" % sn(-h), "x ＝ %s" % sn(k) if k != h else "x ＝ 0", "x ＝ %s" % sn(a) if a != h else "x ＝ %s" % sn(h + 1)], "頂點（%s，%s），x ＝ %s 時有%s %s。" % (sn(h), sn(k), sn(h), kind, sn(k)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        h, k = nz(-6, 6), R.randint(-15, 15)
        a = R.choice([1, 1, -1, 2, -2, 3])
        cs = [a, -2 * a * h, a * h * h + k]
        kind = "最小值" if a > 0 else "最大值"
        q = "y ＝ %s 的%s是多少？" % (poly(cs), kind)
        return mcq(q, sn(k), [sn(cs[2]), sn(h), sn(-k) if k else "1", sn(k + a * h * h) if a * h * h else sn(k + 1)], "配方：%s，%s是 %s（x ＝ %s 時）。" % (vform(a, h, k), kind, sn(k), sn(h)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def fence():
        P = R.randint(5, 30) * 4
        h = P // 4
        q = "用 %d 公尺長的籬笆圍成長方形，面積最大是多少平方公尺？" % P
        return mcq(q, "%s 平方公尺" % num(h * h), ["%s 平方公尺" % num(x) for x in ((P // 2) ** 2 // 4 * 2, h * (h + 1), P * P // 4)], "寬 x，長 %d － x，面積 y ＝ x（%d － x）＝ －（x － %d）<sup>2</sup> ＋ %d，x ＝ %d 時最大 %s。（正方形）" % (P // 2, P // 2, h, h * h, h, num(h * h)))

    def wall():
        L = R.randint(5, 30) * 4
        q = "靠著一面長牆，用 %d 公尺籬笆圍三邊做成長方形菜園，面積最大是多少平方公尺？" % L
        x = L // 4
        A = x * (L - 2 * x)
        return mcq(q, "%s 平方公尺" % num(A), ["%s 平方公尺" % num(v) for v in ((L // 4) ** 2, (L // 3) ** 2 if L % 3 == 0 else A // 2, A * 2)], "垂直牆的邊 x，平行牆的邊 %d － 2x，y ＝ x（%d － 2x）＝ －2（x － %d）<sup>2</sup> ＋ %s，最大 %s。" % (L, L, x, num(A), num(A)))
    return pick_unique(R, fence, 10, seen) + pick_unique(R, wall, 10, seen)


def s5(seen):
    def ball():
        h = R.randint(1, 3)
        k = 5 * h * h + R.choice([0, 1, 2, 3])
        q = "球被往上丟，t 秒後高度 y ＝ －5（t － %d）<sup>2</sup> ＋ %d 公尺。球最高到多少公尺？那時是幾秒？" % (h, k)
        return mcq(q, "%d 公尺，%d 秒" % (k, h), ["%d 公尺，%d 秒" % (h, k), "%d 公尺，%d 秒" % (k - 5, h), "%d 公尺，%d 秒" % (k, h * 2)], "a ＝ －5 ＜ 0，頂點（%d，%d）是最高點：%d 秒時最高 %d 公尺。" % (h, k, h, k))

    def profit():
        p0, q0 = R.choice([(50, 100), (40, 200), (60, 120), (80, 100)])
        d = R.choice([2, 5, 10])
        c = R.randint(1, 4) * 10
        # 每漲 1 元，少賣 d 個；利潤 = (p0 + x - c)(q0 - d x)
        A, B = -d, q0 - d * (p0 - c)
        if B % (2 * d):
            return None
        x = B // (2 * d)
        if x <= 0 or q0 - d * x <= 0:
            return None
        P = (p0 + x - c) * (q0 - d * x)
        q = "一件商品成本 %d 元，售價 %d 元時每天賣 %d 件；售價每漲 1 元，每天少賣 %d 件。售價定多少元時利潤最大？" % (c, p0, q0, d)
        return mcq(q, "%d 元" % (p0 + x), ["%d 元" % v for v in (p0, p0 + 2 * x, p0 + x // 2 if x // 2 != x else p0 + x + 5)], "漲 x 元，利潤 y ＝（%d ＋ x）（%d － %dx），配方得 x ＝ %d 時最大（每天利潤 %s 元），售價 %d 元。" % (p0 - c, q0, d, x, num(P), p0 + x))
    return pick_unique(R, ball, 10, seen) + pick_unique(R, profit, 10, seen)


def main():
    seen = set()
    sets = [("最大值或最小值", s1(seen)), ("何時有最大、最小值", s2(seen)), ("配方求最大、最小值", s3(seen)),
            ("圍籬面積", s4(seen)), ("生活應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["y ＝ a（x － h）<sup>2</sup> ＋ k：<b>a ＞ 0 有最小值 k</b>（頂點是最低點），<b>a ＜ 0 有最大值 k</b>（頂點是最高點），都發生在 x ＝ h。",
         "一般式先配方，化成頂點式再看。",
         "應用題：先設未知數列出二次函數，再配方找頂點，最後檢查答案合不合情境。"],
        [example("y ＝ －2（x － 3）<sup>2</sup> ＋ 7", ["a ＜ 0，頂點（3，7）是最高點。"], "x ＝ 3 時最大值 7"),
         example("周長 40 公尺的長方形，面積最大？", ["y ＝ x（20 － x）＝ －（x － 10）<sup>2</sup> ＋ 100。"], "100 平方公尺")],
        [("a ＞ 0 時有最大值", "開口向上，只有最小值"),
         ("最大值是 h", "最大、最小值是 y 的值 k；h 是那時的 x"),
         ("一般式的常數 c 就是最小值", "要先配方")])
    faq = [{"q": "為什麼開口向上只有最小值？",
            "a": "開口向上的拋物線往兩邊無限升高，沒有最高點，只有頂點是最低點。"},
           {"q": "周長固定時，為什麼正方形面積最大？",
            "a": "面積 y ＝ x（半周長 － x），配方後頂點在 x ＝ 半周長 ÷ 2，也就是長寬相等的正方形。"},
           {"q": "九年級的二次函數極值要學什麼？",
            "a": "108課綱 F-9-2：已配方好之二次函數的最大值與最小值，以及最高點、最低點等名詞。"}]
    make_unit(R, "grade-9", "maximum-and-minimum", "F-9-2",
              "二次函數的圖形與極值：二次函數的相關名詞（對稱軸、頂點、最低點、最高點、開口向上、開口向下、最大值、最小值）；已配方好之二次函數的最大值與最小值。",
              "二次函數的最大值與最小值",
              "九年級數學 二次函數最大值最小值 練習題｜配方・圍籬面積・應用 學習單（附解答）",
              "最大值與最小值",
              "國中九年級數學「二次函數的最大值與最小值」免費學習單：判斷最大值或最小值、何時發生、配方求極值、圍籬面積最大、球的最高點與利潤應用題。100題線上練習馬上對答案，附可列印解答。",
              "a ＞ 0 有最小值，a ＜ 0 有最大值",
              "y ＝ a（x － h）<sup>2</sup> ＋ k 的極值是 k，發生在 x ＝ h。",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
