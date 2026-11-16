# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：等值分數（108課綱 N-4-6）
  python3 tools/gen_tw_math_g4_equivalent_fractions.py
等值分數（圖・分子分母同乘同除）、□ を求める、簡單異分母の比較・加減（一方の分母が他方の倍數）、分數⇔小數。
誤答：分子だけ（分母だけ）に掛ける、分子分母に同じ数を足す、分母同士も足す、1/4 を 0.4 とする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, mx, fig, svg_wrap, dnum, GREEN, FILL

R = random.Random(41007)
NM = Names(R)


def bar(k, n, w=300):
    seg = w / n
    s = "".join("<rect x='%.1f' y='6' width='%.1f' height='34' fill='%s' stroke='%s' stroke-width='2'/>" % (6 + i * seg, seg, FILL if i < k else "#fff", GREEN) for i in range(n))
    return s


def two_bars(a, b, c, d):
    s = bar(a, b) + "<g transform='translate(0 46)'>%s</g>" % bar(c, d)
    return fig(svg_wrap(312, 88, s, "兩條一樣長的長條"))


def fv(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    w, r = divmod(v.numerator, v.denominator)
    return mx(w, r, v.denominator) if w else fr(r, v.denominator)


def s1(seen):
    def pic():
        b = R.choice([2, 3, 4, 5])
        a = R.randint(1, b - 1)
        k = R.choice([2, 3]) if b <= 4 else 2
        if b * k < 6:
            return None
        q = "上下兩條一樣長。上面塗了 %s，下面要塗幾格才一樣多？" % fr(a, b) + two_bars(a, b, 0, b * k)
        return mcq(q, "%d 格（%s）" % (a * k, fr(a * k, b * k)), ["%d 格（%s）" % (x, fr(x, b * k)) for x in (a, a + k, a * k + 1, a * k - 1, b * k - a * k, a * k + 2) if 0 < x < b * k and x != a * k],
                   "每 1 格分成 %d 小格，%d 格變成 %d 小格：%s ＝ %s。" % (k, a, a * k, fr(a, b), fr(a * k, b * k)))

    def which():
        b = R.randint(2, 9)
        a = R.randint(1, b - 1)
        k = R.randint(2, 6)
        q = "下面哪一個分數和 %s 一樣大？" % fr(a, b)
        return mcq(q, fr(a * k, b * k), [fr(a + k, b + k), fr(a * k, b), fr(a, b * k), fr(a * k, b * k + 1)],
                   "分子和分母<b>同時乘以 %d</b>：%s ＝ %s。" % (k, fr(a, b), fr(a * k, b * k)))
    return pick_unique(R, pic, 8, seen) + pick_unique(R, which, 12, seen)


def s2(seen):
    def mk():
        b = R.randint(2, 10)
        a = R.randint(1, b - 1)
        k = R.randint(2, 8)
        if b * k > 60:
            return None
        if R.random() < .5:
            q = "%s ＝ %s，□ 是多少？" % (fr(a, b), fr("□", b * k))
            return mcq(q, str(a * k), [str(a + b * k - b), str(a), str(a * k + 1), str(b * k - a)],
                       "分母 %d × %d ＝ %d，分子也要 × %d：%d × %d ＝ %d。" % (b, k, b * k, k, a, k, a * k))
        q = "%s ＝ %s，□ 是多少？" % (fr(a * k, b * k), fr(a, "□"))
        return mcq(q, str(b), [str(b * k - a * k + a), str(b * k), str(b + 1), str(b * k // a) if b * k % a == 0 and b * k // a != b else str(b + 2)],
                   "分子 %d ÷ %d ＝ %d，分母也要 ÷ %d：%d ÷ %d ＝ %d。" % (a * k, k, a, k, b * k, k, b))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        b = R.choice([2, 3, 4, 5])
        k = R.choice([2, 3, 4])
        d = b * k
        if d > 20:
            return None
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if F(a, b) == F(c, d) or F(a, b).denominator != b:
            return None
        sign = ">" if F(a, b) > F(c, d) else "<"
        L = [(fr(a, b), fr(c, d)), (fr(c, d), fr(a, b))][R.randint(0, 1)]
        real = ">" if (F(a, b) > F(c, d)) == (L[0] == fr(a, b)) else "<"
        return mcq("%s ○ %s，○ 裡要填什麼？" % L, real, ["<" if real == ">" else ">", "=", "無法比較"],
                   "把 %s 化成分母 %d：%s。再比分子：%s 和 %s。" % (fr(a, b), d, fr(a * k, d), fr(a * k, d), fr(c, d)))
    return pick_unique(R, mk, 20, seen)


def over(n, d):
    """分母 d のまま（約分しない）：14/12 → 1又2/12"""
    w, r = divmod(n, d)
    return str(w) if r == 0 else (mx(w, r, d) if w else fr(r, d))


def s4(seen):
    def mk():
        b = R.choice([2, 3, 4, 5])
        k = R.choice([2, 3, 4])
        d = b * k
        if d > 20:
            return None
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if F(a, b).denominator != b:
            return None
        op = R.choice(["＋", "－"])
        A = a * k
        if op == "＋":
            n = A + c
            q = "%s ＋ %s ＝" % (fr(a, b), fr(c, d))
        else:
            if A == c:
                return None
            n = abs(A - c)
            q = "%s － %s ＝" % ((fr(a, b), fr(c, d)) if A > c else (fr(c, d), fr(a, b)))
        nd = a + c if op == "＋" else abs(a - c)
        w = [fr(nd, b + d) if nd else fr(1, b + d), over(nd, d) if nd != n else over(n + 1, d), over(n + 1, d), over(n - 1, d) if n > 1 else over(n + 2, d)]
        return mcq(q, over(n, d), w, "把 %s 化成 %s，分母一樣再%s：%s。" % (fr(a, b), fr(A, d), "相加" if op == "＋" else "相減", over(n, d)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    PAIRS = [(1, 2, "0.5"), (1, 4, "0.25"), (3, 4, "0.75"), (1, 5, "0.2"), (2, 5, "0.4"), (3, 5, "0.6"), (4, 5, "0.8")]

    def f2d():
        if R.random() < .45:
            a, b, dv = R.choice(PAIRS)
            w = {"0.25": ["0.4", "0.14", "2.5"], "0.75": ["0.34", "0.7", "7.5"], "0.5": ["0.2", "0.12", "5"]}.get(dv, ["0.%d" % b, "%d.%d" % (a, b), dnum(a / b * 10)])
            return mcq("%s 寫成小數是多少？" % fr(a, b), dv, w, "%s ＝ %s ＝ %s。" % (fr(a, b), fr(int(float(dv) * 100), 100) if len(dv) == 4 else fr(int(float(dv) * 10), 10), dv))
        d = R.choice([10, 100])
        a = R.randint(1, d - 1)
        if a % 10 == 0 and d == 100:
            return None
        dv = dnum(a / d, 2)
        w = [dnum(a / (d * 10), 3), dnum(a / d * 10, 1) if d == 100 else str(a), "%d.%d" % (a, d) if d == 10 else "0.%d" % (a * 10) if a < 10 else dnum(a / 1000, 3)]
        return mcq("%s 寫成小數是多少？" % fr(a, d), dv, [x for x in w if x != dv] + [dnum(a / d + 0.1, 2)], "%s 就是 %d 個 %s，是 %s。" % (fr(a, d), a, "0.1" if d == 10 else "0.01", dv))

    def d2f():
        a = R.randint(1, 99)
        if a % 10 == 0:
            return None
        dv = dnum(a / 100, 2)
        return mcq("%s 寫成分數是多少？" % dv, fr(a, 100), [fr(a, 10), fr(a, 1000), fr(100, a)], "%s 是 %d 個 0.01，就是 %s。" % (dv, a, fr(a, 100)))
    return pick_unique(R, f2d, 12, seen) + pick_unique(R, d2f, 8, seen)


def main():
    seen = set()
    sets = [("看圖找等值分數", s1(seen)), ("求 □", s2(seen)), ("簡單異分母的比較", s3(seen)),
            ("簡單異分母的加減", s4(seen)), ("分數和小數", s5(seen))]
    body = lesson(
        ["大小一樣的分數叫做<b>等值分數</b>：%s ＝ %s ＝ %s。" % (fr(1, 2), fr(2, 4), fr(3, 6)),
         "分子和分母<b>同時乘以</b>（或同時除以）同一個數，分數的大小不變。",
         "分母不一樣時，先化成<b>同分母</b>，再比較或加減。",
         "分母是 10、100 的分數可以寫成小數：%s ＝ 0.3，%s ＝ 0.27；%s ＝ 0.5，%s ＝ 0.25。" % (fr(3, 10), fr(27, 100), fr(1, 2), fr(1, 4))],
        [example("%s ＝ %s，□ 是多少？" % (fr(2, 3), fr("□", 12)), ["分母 3 × 4 ＝ 12。", "分子也 × 4：2 × 4 ＝ 8。"], "8"),
         example("%s ＋ %s ＝" % (fr(1, 2), fr(1, 4)), ["%s ＝ %s。" % (fr(1, 2), fr(2, 4)), "%s ＋ %s ＝ %s。" % (fr(2, 4), fr(1, 4), fr(3, 4))], fr(3, 4))],
        [("%s ＝ %s（分子分母都加 1）" % (fr(1, 2), fr(2, 3)), "要同時乘以同一個數：%s ＝ %s" % (fr(1, 2), fr(2, 4))),
         ("%s ＋ %s ＝ %s" % (fr(1, 2), fr(1, 4), fr(2, 6)), "先化成同分母：%s ＋ %s ＝ %s" % (fr(2, 4), fr(1, 4), fr(3, 4))),
         ("%s ＝ 0.4" % fr(1, 4), "%s ＝ %s ＝ 0.25" % (fr(1, 4), fr(25, 100)))])
    faq = [{"q": "什麼是等值分數？",
            "a": "表示一樣大小的分數，例如 1/2、2/4、3/6。分子和分母同時乘以或除以同一個數，就得到等值分數。"},
           {"q": "四年級的異分母分數要學到哪裡？",
            "a": "108課綱 N-4-6：用等值分數做簡單的異分母分數比較和加減（例如 1/2 和 1/4），一般的通分和約分在五年級學。"},
           {"q": "分數怎麼化成小數？",
            "a": "先化成分母 10 或 100 的分數：3/5 ＝ 6/10 ＝ 0.6，1/4 ＝ 25/100 ＝ 0.25。"}]
    make_unit(R, "grade-4", "equivalent-fractions", "N-4-6",
              "等值分數：由操作活動中理解等值分數的意義。簡單異分母分數的比較、加、減的意義。簡單分數與小數的互換。",
              "等值分數：簡單異分母與分數小數互換",
              "四年級數學 等值分數 練習題｜異分母比較・加減・分數化小數 學習單（附解答）",
              "等值分數",
              "國小四年級數學「等值分數」免費學習單：看圖找等值分數、求□、簡單異分母分數的比較和加減、分數和小數的互換。100題線上練習馬上對答案，附可列印解答。",
              "分子分母同乘同除，大小不變",
              "分母不一樣，先化成同分母再比較、加減。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
