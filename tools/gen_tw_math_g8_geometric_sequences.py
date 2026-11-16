# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：等比數列（108課綱 N-8-6）
  python3 tools/gen_tw_math_g8_geometric_sequences.py
公比（後項 ÷ 前項、負・分數も）、等比數列かどうか、一般項 aₙ ＝ a₁ × rⁿ⁻¹、第幾項・首項・中間の項、細胞分裂・紙を折る・ボールの跳ね返り。
誤答：公比を差で考える、指數を n にする、前項 ÷ 後項、負の公比の符號を落とす。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, num
from tw_g7 import sn, par, tidy_sets, pw

R = random.Random(81016)


def show(xs):
    return "，".join(sn(x) for x in xs)


def gs(a, r, n):
    return [F(a) * F(r) ** i for i in range(n)]


RS = [2, 3, 4, 5, -2, -3, F(1, 2), F(1, 3), F(-1, 2)]


def pick():
    while True:
        r = R.choice(RS)
        a = R.choice([1, 2, 3, 4, 5, 6, -1, -2, -3]) if F(r).denominator == 1 else R.choice([16, 32, 48, 64, 81, 162, 243, -64, 96])
        xs = gs(a, r, 5)
        if all(x.denominator == 1 for x in xs) and max(abs(x) for x in xs) <= 2000:
            return a, r, xs


def s1(seen):
    def ratio():
        a, r, xs = pick()
        q = "等比數列 %s，…… 的公比是多少？" % show(xs[:4])
        return mcq(q, sn(r), [sn(1 / F(r)), sn(-F(r)), sn(xs[1] - xs[0]), sn(F(r) * 2)], "公比 ＝ 後項 ÷ 前項：%s ÷ %s ＝ %s。" % (sn(xs[1]), par(xs[0]), sn(r)))

    def nxt():
        a, r, xs = pick()
        q = "依照規律，下一個數是多少？<br>%s，……" % show(xs[:4])
        d = xs[3] - xs[2]
        return mcq(q, sn(xs[4]), [sn(xs[3] + d), sn(-xs[4]), sn(xs[3] * 2) if r != 2 else sn(xs[3] * 3), sn(xs[3] + xs[2])], "每次都乘 %s：%s × %s ＝ %s。" % (sn(r), par(xs[3]), par(r), sn(xs[4])))
    return pick_unique(R, ratio, 10, seen) + pick_unique(R, nxt, 10, seen)


def s2(seen):
    def which():
        a, r, xs = pick()
        good = show(xs[:4])
        b = R.randint(2, 9)
        bads = [show([b + 3 * i for i in range(4)]), show([b * i for i in range(1, 5)]), show([b, 2 * b, 4 * b, 6 * b]), show([i * i for i in range(b, b + 4)])]
        R.shuffle(bads)
        L = "甲乙丙丁"
        ys = [good] + bads[:3]
        if len(set(ys)) < 4:
            return None
        R.shuffle(ys)
        k = ys.index(good)
        q = "下面哪一個是等比數列？<br>" + "<br>".join("%s　%s" % (L[i], y) for i, y in enumerate(ys))
        return mcq(q, L[k], [c for c in L if c != L[k]], "相鄰兩項的比（後 ÷ 前）都相同才是等比數列：%s 每次乘 %s。" % (good, sn(r)))

    def mid():
        a, r, xs = pick()
        if F(r) < 0:
            return None
        q = "等比數列 %s，□，%s，…… 中 □ 是多少？" % (sn(xs[0]), sn(xs[2]))
        return mcq(q, sn(xs[1]), [sn((xs[0] + xs[2]) / 2) if (xs[0] + xs[2]) % 2 == 0 else sn(xs[1] + 1), sn(-xs[1]), sn(xs[2] / 2) if xs[2] % 2 == 0 else sn(xs[1] * 2), sn(xs[0] * xs[2])],
                   "公比 r 滿足 %s × r<sup>2</sup> ＝ %s，r ＝ %s（取正），□ ＝ %s × %s ＝ %s。" % (sn(xs[0]), sn(xs[2]), sn(r), sn(xs[0]), sn(r), sn(xs[1])))
    return pick_unique(R, which, 10, seen) + pick_unique(R, mid, 10, seen)


def s3(seen):
    def mk():
        a = R.choice([1, 2, 3, 5, -1, -2, -3])
        r = R.choice([2, 3, -2, -3, 2, 3])
        n = R.randint(4, 9)
        v = a * r ** (n - 1)
        if abs(v) > 50000:
            return None
        q = "首項 %s、公比 %s 的等比數列，第 %d 項是多少？" % (sn(a), sn(r), n)
        return mcq(q, sn(v), [sn(a * r ** n), sn(a + (n - 1) * r), sn((a * r) ** (n - 1)) if a not in (1, -1) else sn(-v), sn(-v)],
                   "a<sub>%d</sub> ＝ %s × %s ＝ %s × %s ＝ %s。" % (n, par(a), pw(r, n - 1), par(a), par(r ** (n - 1)), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def which_term():
        a = R.choice([1, 2, 3, 5, 7])
        r = R.choice([2, 3])
        n = R.randint(4, 10)
        v = a * r ** (n - 1)
        q = "等比數列 %s，%s，%s，…… 中，%s 是第幾項？" % (sn(a), sn(a * r), sn(a * r * r), num(v))
        return mcq(q, "第 %d 項" % n, ["第 %d 項" % x for x in (n - 1, n + 1, n + 2)], "%s × %s<sup>n－1</sup> ＝ %s，%s<sup>n－1</sup> ＝ %s ＝ %s，n － 1 ＝ %d，n ＝ %d。" % (sn(a), r, num(v), r, num(r ** (n - 1)), pw(r, n - 1), n - 1, n))

    def first():
        a = R.choice([1, 2, 3, 4, 5, 6])
        r = R.choice([2, 3, -2])
        m = R.randint(3, 6)
        v = a * r ** (m - 1)
        q = "等比數列的公比是 %s，第 %d 項是 %s，首項是多少？" % (sn(r), m, sn(v))
        return mcq(q, sn(a), [sn(F(v, r ** m)) if F(v, r ** m).denominator == 1 else sn(a * r), sn(v - (m - 1) * r), sn(-a), sn(a * abs(r))], "a<sub>1</sub> × %s ＝ %s，a<sub>1</sub> ＝ %s ÷ %s ＝ %s。" % (pw(r, m - 1), sn(v), sn(v), par(r ** (m - 1)), sn(a)))
    return pick_unique(R, which_term, 10, seen) + pick_unique(R, first, 10, seen)


def s5(seen):
    def cell():
        a = R.choice([1, 2, 3, 5, 10])
        h = R.randint(3, 8)
        q = "一種細菌每小時分裂一次，數量變成 2 倍。一開始有 %d 個，%d 小時後有幾個？" % (a, h)
        v = a * 2 ** h
        return mcq(q, "%s 個" % num(v), ["%s 個" % num(x) for x in (a * 2 ** (h - 1), a + 2 * h, a * 2 * h, a * 2 ** (h + 1))], "首項 %d、公比 2，%d 小時後是第 %d 項：%d × 2<sup>%d</sup> ＝ %s（個）。" % (a, h, h + 1, a, h, num(v)))

    def ball():
        H = R.choice([256, 320, 384, 512, 640, 128])
        k = R.randint(2, 4)
        v = F(H, 2 ** k)
        q = "一顆球從 %d 公分高落下，每次彈起的高度是落下高度的 <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>。第 %d 次彈起多高？" % (H, k)
        return mcq(q, "%s 公分" % sn(v), ["%s 公分" % sn(x) for x in (F(H, 2 ** (k - 1)), F(H, 2 ** (k + 1)), F(H, 2 * k), H - 2 * k)], "%d ×（<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>）<sup>%d</sup> ＝ %s（公分）。" % (H, k, sn(v)))

    def fold():
        k = R.randint(3, 7)
        q = "一張紙對折一次變成 2 層，再對折變成 4 層。對折 %d 次後有幾層？" % k
        v = 2 ** k
        return mcq(q, "%d 層" % v, ["%d 層" % x for x in (2 * k, 2 ** (k - 1), 2 ** (k + 1), k * k)], "每對折一次層數 × 2：2<sup>%d</sup> ＝ %d（層）。" % (k, v))
    return pick_unique(R, cell, 8, seen) + pick_unique(R, ball, 7, seen) + pick_unique(R, fold, 5, seen)


def main():
    seen = set()
    sets = [("公比和下一項", s1(seen)), ("認識等比數列", s2(seen)), ("求第 n 項", s3(seen)),
            ("第幾項和首項", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["相鄰兩項的比（後項 ÷ 前項）都一樣的數列叫<b>等比數列</b>，這個比叫<b>公比</b> r。公比可以是負數或分數，但不是 0。",
         "<b>一般項</b>：a<sub>n</sub> ＝ a<sub>1</sub> × r<sup>n－1</sup>。到第 n 項只乘了 n － 1 次公比。",
         "等差數列每次「加」同一個數，等比數列每次「乘」同一個數。"],
        [example("3，6，12，24，…… 的第 8 項？", ["公比 2。", "3 × 2<sup>7</sup> ＝ 3 × 128。"], "384"),
         example("2，－6，18，…… 的公比？", ["－6 ÷ 2 ＝ －3。"], "－3")],
        [("公比用相減", "等比要相除：後項 ÷ 前項"),
         ("第 8 項 ＝ 3 × 2<sup>8</sup>", "只乘 7 次：3 × 2<sup>7</sup>"),
         ("2，－6，18 的公比寫成 3", "正負交替，公比是負數 －3")])
    faq = [{"q": "等比數列和等差數列怎麼分？",
            "a": "相鄰兩項相減都一樣是等差，相除都一樣是等比。例如 2，4，6 是等差，2，4，8 是等比。"},
           {"q": "公比是分數會怎樣？",
            "a": "公比在 0 和 1 之間時，數列越來越小，例如 64，32，16，…… 的公比是 1/2，像球每次彈起的高度。"},
           {"q": "八年級的等比數列要學什麼？",
            "a": "108課綱 N-8-6：等比數列；給定首項、公比計算等比數列的一般項。"}]
    make_unit(R, "grade-8", "geometric-sequences", "N-8-6",
              "等比數列：等比數列；給定首項、公比計算等比數列的一般項。",
              "等比數列",
              "八年級數學 等比數列 練習題｜公比・一般項・細菌分裂 學習單（附解答）",
              "等比數列",
              "國中八年級數學「等比數列」免費學習單：公比和下一項、判斷等比數列、一般項 aₙ＝a₁×rⁿ⁻¹、求第幾項和首項、細菌分裂與球彈跳應用題。100題線上練習馬上對答案，附可列印解答。",
              "a<sub>n</sub> ＝ a<sub>1</sub> × r<sup>n－1</sup>",
              "公比 ＝ 後項 ÷ 前項；第 n 項只乘 n － 1 次。",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
