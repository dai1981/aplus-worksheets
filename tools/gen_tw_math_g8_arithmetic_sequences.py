# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：數列與等差數列（108課綱 N-8-3、N-8-4）
  python3 tools/gen_tw_math_g8_arithmetic_sequences.py
規律から次の項、公差、等差數列かどうか、一般項 aₙ ＝ a₁ ＋（n － 1）d、第幾項・首項・公差を逆算、圖形の規律と生活の應用。
誤答：aₙ ＝ a₁ ＋ nd（n－1 にしない）、公差を後ろ引く前（a₁ － a₂）にする、首項を求めるときに符號を間違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, line, text
from tw_g7 import sn, par, tidy_sets

R = random.Random(81014)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def seq(a, d, n):
    return [a + i * d for i in range(n)]


def show(xs):
    return "，".join(sn(x) for x in xs)


def sticks(k):
    """正方形を一列に k 個（マッチ棒 3k ＋ 1 本）"""
    u = 26
    s = []
    for i in range(k):
        x = 6 + i * u
        s.append(line(x, 6, x + u, 6, "#b5651d", 3))
        s.append(line(x, 6 + u, x + u, 6 + u, "#b5651d", 3))
    for i in range(k + 1):
        x = 6 + i * u
        s.append(line(x, 6, x, 6 + u, "#b5651d", 3))
    return svg_wrap(12 + k * u, 12 + u, "".join(s), "%d 個正方形" % k)


def s1(seen):
    def nxt():
        a, d = R.randint(-20, 30), nz(-9, 12)
        xs = seq(a, d, 5)
        q = "依照規律，下一個數是多少？<br>%s，……" % show(xs[:4])
        return mcq(q, sn(xs[4]), [sn(xs[3] - d), sn(xs[3] + 2 * d), sn(xs[3] + d + 1), sn(xs[3] * 2)], "每次都%s %d：%s %s %d ＝ %s。" % ("加" if d > 0 else "減", abs(d), sn(xs[3]), "＋" if d > 0 else "－", abs(d), sn(xs[4])))

    def pic():
        k = R.randint(4, 9)
        q = "用火柴棒排正方形：1 個用 4 根，2 個用 7 根，3 個用 10 根。<div class='qfig'>%s　%s　%s</div>排 %d 個正方形要幾根？" % (sticks(1), sticks(2), sticks(3), k)
        v = 3 * k + 1
        return mcq(q, "%d 根" % v, ["%d 根" % x for x in (4 * k, 3 * k, v + 3, 4 + 3 * k)], "每多 1 個正方形多 3 根，是首項 4、公差 3 的等差數列：4 ＋（%d － 1）× 3 ＝ %d（根）。" % (k, v))
    return pick_unique(R, nxt, 14, seen) + pick_unique(R, pic, 6, seen)


def s2(seen):
    def diff():
        a, d = R.randint(-30, 40), nz(-12, 12)
        xs = seq(a, d, 5)
        q = "等差數列 %s，…… 的公差是多少？" % show(xs[:4])
        return mcq(q, sn(d), [sn(-d), sn(xs[1]), sn(2 * d), sn(d + 1)], "公差 ＝ 後項 － 前項：%s － %s ＝ %s。" % (sn(xs[1]), par(xs[0]), sn(d)))

    def which():
        a, d = R.randint(-10, 20), nz(-8, 8)
        good = show(seq(a, d, 5))
        b = R.randint(1, 9)
        bads = [show([b * (2 ** i) for i in range(5)]), show([i * i + b for i in range(1, 6)]), show([b, b + 2, b + 5, b + 7, b + 10]), show([b, b + 3, b + 6, b + 8, b + 11])]
        R.shuffle(bads)
        L = "甲乙丙丁"
        xs = [good] + bads[:3]
        R.shuffle(xs)
        k = xs.index(good)
        q = "下面哪一個是等差數列？<br>" + "<br>".join("%s　%s" % (L[i], x) for i, x in enumerate(xs))
        return mcq(q, L[k], [c for c in L if c != L[k]], "相鄰兩項的差都相同才是等差數列：%s 每次差 %s。" % (good, sn(d)))
    return pick_unique(R, diff, 12, seen) + pick_unique(R, which, 8, seen)


def s3(seen):
    def mk():
        a, d = R.randint(-20, 30), nz(-9, 9)
        n = R.randint(8, 60)
        v = a + (n - 1) * d
        q = "首項 %s、公差 %s 的等差數列，第 %d 項是多少？" % (sn(a), sn(d), n)
        return mcq(q, sn(v), [sn(a + n * d), sn(a * n), sn(n * d), sn(a + (n - 1) * -d)], "a<sub>%d</sub> ＝ %s ＋（%d － 1）× %s ＝ %s。" % (n, sn(a), n, par(d), sn(v)))

    def from_list():
        a, d = R.randint(-20, 30), nz(-9, 9)
        n = R.randint(10, 50)
        xs = seq(a, d, 3)
        v = a + (n - 1) * d
        q = "等差數列 %s，…… 的第 %d 項是多少？" % (show(xs), n)
        return mcq(q, sn(v), [sn(a + n * d), sn(a + (n - 2) * d), sn(n * d), sn(a + (n - 1) * -d)], "公差 %s，a<sub>%d</sub> ＝ %s ＋ %d × %s ＝ %s。" % (sn(d), n, sn(a), n - 1, par(d), sn(v)))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, from_list, 10, seen)


def s4(seen):
    def nth():
        a, d = R.randint(-10, 20), nz(-7, 9)
        n = R.randint(10, 40)
        v = a + (n - 1) * d
        q = "等差數列 %s，…… 中，%s 是第幾項？" % (show(seq(a, d, 3)), sn(v))
        return mcq(q, "第 %d 項" % n, ["第 %d 項" % x for x in (n - 1, n + 1, abs(v // d) if abs(v // d) not in (n, n - 1, n + 1, 0) else n + 2)], "%s ＋（n － 1）× %s ＝ %s，n － 1 ＝ %d，n ＝ %d。" % (sn(a), par(d), sn(v), n - 1, n))

    def first():
        a, d = R.randint(-15, 25), nz(-8, 8)
        m = R.randint(5, 20)
        v = a + (m - 1) * d
        q = "等差數列的公差是 %s，第 %d 項是 %s，首項是多少？" % (sn(d), m, sn(v))
        return mcq(q, sn(a), [sn(v + (m - 1) * d), sn(v - m * d), sn(a + d), sn(-a) if a else "1"], "a<sub>1</sub> ＋（%d － 1）× %s ＝ %s，a<sub>1</sub> ＝ %s － %s ＝ %s。" % (m, par(d), sn(v), sn(v), par((m - 1) * d), sn(a)))

    def twoterms():
        a, d = R.randint(-15, 25), nz(-8, 8)
        i, j = sorted(R.sample(range(2, 16), 2))
        ai, aj = a + (i - 1) * d, a + (j - 1) * d
        q = "等差數列的第 %d 項是 %s，第 %d 項是 %s，公差是多少？" % (i, sn(ai), j, sn(aj))
        return mcq(q, sn(d), [sn(-d), sn((aj - ai) // (j - i + 1)) if (aj - ai) % (j - i + 1) == 0 else sn(d + 1), sn(aj - ai), sn(2 * d)], "從第 %d 項到第 %d 項加了 %d 次公差：（%s － %s）÷ %d ＝ %s。" % (i, j, j - i, sn(aj), par(ai), j - i, sn(d)))
    return pick_unique(R, nth, 7, seen) + pick_unique(R, first, 7, seen) + pick_unique(R, twoterms, 6, seen)


def s5(seen):
    def seats():
        a, d, n = R.randint(12, 24), R.randint(1, 3), R.randint(10, 30)
        q = "禮堂第 1 排有 %d 個座位，之後每排比前一排多 %d 個。第 %d 排有幾個座位？" % (a, d, n)
        v = a + (n - 1) * d
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in (a + n * d, a * n, n * d, v - 1)], "%d ＋（%d － 1）× %d ＝ %d（個）。" % (a, n, d, v))

    def save():
        who = NM.next()
        a, d = R.choice([50, 100, 120, 200]), R.choice([10, 20, 30, 50])
        n = R.randint(8, 20)
        v = a + (n - 1) * d
        q = "%s第 1 週存 %d 元，以後每週比前一週多存 %d 元。第 %d 週要存多少元？" % (who, a, d, n)
        return mcq(q, "%d 元" % v, ["%d 元" % x for x in (a + n * d, a * n, v - d * 2, a + d * n * 2)], "%d ＋（%d － 1）× %d ＝ %d（元）。" % (a, n, d, v))

    def temp():
        a = R.randint(20, 28)
        d = R.choice([6, 5])
        k = R.randint(2, 5)
        q = "高度每上升 1 公里，氣溫約下降 %d°C。地面氣溫 %d°C，%d 公里高的氣溫約是多少？" % (d, a, k)
        v = a - d * k
        return mcq(q, "%s°C" % sn(v), ["%s°C" % sn(x) for x in (a - d * (k - 1), a + d * k, -v if v else 1, v - d)], "首項 %d、公差 －%d：%d － %d × %d ＝ %s（°C）。" % (a, d, a, d, k, sn(v)))
    return pick_unique(R, seats, 8, seen) + pick_unique(R, save, 7, seen) + pick_unique(R, temp, 5, seen)


def main():
    seen = set()
    sets = [("找規律", s1(seen)), ("公差和認識等差數列", s2(seen)), ("求第 n 項", s3(seen)),
            ("第幾項、首項、公差", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["依規律排成一列的數叫<b>數列</b>。相鄰兩項的差（後項 － 前項）都一樣，叫<b>等差數列</b>，這個差叫<b>公差</b> d。",
         "<b>一般項</b>：a<sub>n</sub> ＝ a<sub>1</sub> ＋（n － 1）d。到第 n 項只加了 n － 1 次公差。",
         "已知兩項求公差：兩項的差 ÷ 中間加了幾次公差。"],
        [example("3，7，11，15，…… 的第 20 項？", ["公差 4。", "3 ＋（20 － 1）× 4 ＝ 79。"], "79"),
         example("等差數列第 4 項是 10，第 10 項是 28，公差？", ["從第 4 項到第 10 項加了 6 次公差。", "（28 － 10）÷ 6 ＝ 3。"], "3")],
        [("第 20 項 ＝ 3 ＋ 20 × 4", "只加 19 次公差：3 ＋ 19 × 4"),
         ("公差用前項 － 後項", "公差 ＝ 後項 － 前項，遞減時公差是負數"),
         ("第 4 項到第 10 項加了 7 次", "10 － 4 ＝ 6 次")])
    faq = [{"q": "等差數列的公差可以是負數嗎？",
            "a": "可以。數列越來越小時公差是負數，例如 20，17，14，…… 的公差是 －3。"},
           {"q": "怎麼判斷是不是等差數列？",
            "a": "把每兩個相鄰的數相減（後 － 前），所有的差都相同就是等差數列。"},
           {"q": "八年級的數列要學什麼？",
            "a": "108課綱 N-8-3、N-8-4：認識生活中和圖形中的數列規律，等差數列，給定首項和公差求一般項。"}]
    make_unit(R, "grade-8", "arithmetic-sequences", "N-8-4",
              "等差數列：等差數列；給定首項、公差計算等差數列的一般項。",
              "數列與等差數列",
              "八年級數學 等差數列 練習題｜公差・一般項・找規律 學習單（附解答）",
              "等差數列",
              "國中八年級數學「數列與等差數列」免費學習單：找規律、公差、判斷等差數列、一般項 aₙ＝a₁＋(n－1)d、求第幾項和首項、座位與存錢應用題。100題線上練習馬上對答案，附可列印解答。",
              "a<sub>n</sub> ＝ a<sub>1</sub> ＋（n － 1）d",
              "第 n 項只加了 n － 1 次公差。",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
