# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：整數、分數、小數的四則應用問題（108課綱 N-6-5）
  python3 tools/gen_tw_math_g6_word_problems.py
分數の「剩下的幾分之幾」、小數の單價・總價、分數と小數の混合計算、概數で見積もる、二〜三步驟の綜合題。
誤答：「剩下的 1/3」を全体の 1/3 とする、單位をそろえない、概數で切り捨て・切り上げを場面に合わせない。
"""
import random
from fractions import Fraction as F
from decimal import Decimal as D
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff, num

R = random.Random(61005)
NM = Names(R)


def ds(x):
    x = D(x).normalize()
    t = format(x, "f")
    if "." in t:
        i, f = t.split(".")
        return num(int(i)) + "." + f
    return num(int(t))


def s1(seen):
    def rest():
        a, b = R.choice([(1, 3), (1, 4), (2, 5), (1, 5), (3, 8), (1, 6), (2, 7)]), R.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
        tot = a[1] * b[1] * R.randint(2, 12)
        used1 = tot * a[0] // a[1]
        left1 = tot - used1
        used2 = left1 * b[0] // b[1]
        left = left1 - used2
        who = NM.next()
        q = "%s有 %d 元，買書用掉全部的 %s，再用剩下的 %s 買文具。還剩多少元？" % (who, tot, fr(*a), fr(*b))
        wrong1 = tot - used1 - tot * b[0] // b[1] if tot - used1 - tot * b[0] // b[1] > 0 else left + used2 // 2 + 1
        return mcq(q, "%s 元" % num(left), ["%s 元" % num(x) for x in (wrong1, left1, used2, left + used1 // 2) if x != left and x > 0],
                   "先用掉 %d × %s ＝ %d，剩 %d；再用掉 %d × %s ＝ %d，剩 %d 元。「剩下的 %s」是剩下的錢的 %s，不是全部的。" % (tot, fr(*a), used1, left1, left1, fr(*b), used2, left, fr(*b), fr(*b)))

    def part():
        p = F(R.randint(1, 4), R.choice([5, 6, 8, 9]))
        if p.denominator == 1 or p >= 1:
            return None
        n = p.numerator * R.randint(3, 15)
        tot = n / p
        if tot.denominator != 1:
            return None
        q = "班上 %s 的同學喜歡打籃球，有 %d 人。全班有幾人？" % (fr(p.numerator, p.denominator), n)
        return mcq(q, "%d 人" % tot, ["%s 人" % ff(x) for x in (n * p, tot - n, tot + p.denominator)], "全班 × %s ＝ %d，全班 ＝ %d ÷ %s ＝ %d（人）。" % (fr(p.numerator, p.denominator), n, n, fr(p.numerator, p.denominator), tot))
    return pick_unique(R, rest, 12, seen) + pick_unique(R, part, 8, seen)


def s2(seen):
    def shop():
        item, p1 = R.choice([("雞肉", 160), ("雞肉", 180), ("豬肉", 220), ("豬肉", 240), ("牛肉", 480), ("牛肉", 550)])
        p1, k1 = D(p1), D(R.randint(5, 25)) / 10
        p2, n2 = R.choice([15, 25, 35, 18]), R.randint(2, 6)
        t1 = p1 * k1
        if t1 != t1.to_integral_value():
            return None
        tot = t1 + p2 * n2
        pay = next(x for x in (500, 1000, 2000) if x > tot)
        q = "%s 1 公斤 %d 元，媽媽買了 %s 公斤，又買了 %d 盒 %d 元的豆腐，付 %d 元，找回多少元？" % (item, p1, ds(k1), n2, p2, pay)
        ans = pay - tot
        return mcq(q, "%s 元" % ds(ans), ["%s 元" % ds(x) for x in (pay - t1, pay - p1 * k1 - p2, ans + p2) if x != ans and x > 0] + ["%s 元" % ds(tot)],
                   "%d －（%d × %s ＋ %d × %d）＝ %d －（%s ＋ %d）＝ %s（元）。" % (pay, p1, ds(k1), p2, n2, pay, ds(t1), p2 * n2, ds(ans)))

    def fuel():
        km = D(R.randint(80, 160)) / 10
        L = D(R.randint(15, 60))
        tot = km * L
        dist = D(R.randint(5, 30)) * 10
        if dist >= tot:
            return None
        q = "一輛車每公升汽油可以跑 %s 公里。加了 %s 公升，跑了 %s 公里後，剩下的油還能跑幾公里？" % (ds(km), ds(L), ds(dist))
        ans = tot - dist
        return mcq(q, "%s 公里" % ds(ans), ["%s 公里" % ds(x) for x in (tot, ans - km, ans + km * 2) if x != ans],
                   "%s × %s － %s ＝ %s － %s ＝ %s（公里）。" % (ds(km), ds(L), ds(dist), ds(tot), ds(dist), ds(ans)))
    return pick_unique(R, shop, 10, seen) + pick_unique(R, fuel, 10, seen)


def s3(seen):
    def mk():
        a = F(R.randint(1, 7), R.choice([2, 4, 5, 8]))
        b = D(R.randint(1, 30)) / 10
        if a.denominator == 1:
            return None
        op = R.choice(["＋", "－", "×"])
        bf = F(str(b))
        v = a + bf if op == "＋" else (a - bf if op == "－" else a * bf)
        if v <= 0:
            return None
        ad = D(a.numerator) / D(a.denominator)
        q = "%s %s %s ＝" % (fr(a.numerator, a.denominator), op, ds(b))
        vd = D(v.numerator) / D(v.denominator)
        if vd.as_tuple().exponent < -3:
            return None
        dd = v.denominator
        while dd % 2 == 0:
            dd //= 2
        while dd % 5 == 0:
            dd //= 5
        ans = ds(vd) if dd == 1 else ff(v)
        wrong = [ds(vd + D("0.1")), ds(vd * 10), ds(abs(D(a.numerator) / 10 + b) if op == "＋" else vd + 1)]
        return mcq(q, ans, [x for x in wrong if x != ans],
                   "%s ＝ %s，再算：%s %s %s ＝ %s。" % (fr(a.numerator, a.denominator), ds(ad), ds(ad), op, ds(b), ans))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def bus():
        n = R.randint(121, 389)
        seat = R.choice([40, 43, 45])
        ans = -(-n // seat)
        q = "%d 位同學去校外教學，每輛遊覽車坐 %d 人，至少要幾輛車？" % (n, seat)
        return mcq(q, "%d 輛" % ans, ["%d 輛" % x for x in (n // seat, ans + 1, round(n / seat) if round(n / seat) != ans else ans - 2) if x != ans],
                   "%d ÷ %d ＝ %d……%d，剩下的人也要坐車，要無條件進位：%d 輛。" % (n, seat, n // seat, n % seat, ans) if n % seat else "%d ÷ %d ＝ %d（輛）。" % (n, seat, ans))

    def box():
        n = R.randint(200, 900)
        per = R.choice([12, 15, 24, 30])
        ans = n // per
        if n % per == 0:
            return None
        q = "%d 顆蘋果，每 %d 顆裝一盒，最多可以裝滿幾盒？" % (n, per)
        return mcq(q, "%d 盒" % ans, ["%d 盒" % x for x in (ans + 1, round(n / per, -1) if round(n / per, -1) not in (ans, ans + 1) else ans + 2, n % per)],
                   "%d ÷ %d ＝ %d……%d，剩下的不夠一盒，要無條件捨去：%d 盒。" % (n, per, ans, n % per, ans))

    def est():
        a, b, c = R.randint(1, 9) * 100 + R.randint(-40, 40), R.randint(1, 9) * 100 + R.randint(-40, 40), R.randint(1, 9) * 100 + R.randint(-40, 40)
        tot = a + b + c
        ra = round(a, -2) + round(b, -2) + round(c, -2)
        q = "用四捨五入到百位估算：%d ＋ %d ＋ %d 大約是多少？" % (a, b, c)
        return mcq(q, "約 %s" % num(ra), ["約 %s" % num(x) for x in (ra + 100, ra - 100, round(tot, -1) if round(tot, -1) != ra else ra + 200)],
                   "%d ≈ %d，%d ≈ %d，%d ≈ %d，合起來約 %s。" % (a, round(a, -2), b, round(b, -2), c, round(c, -2), num(ra)))
    return pick_unique(R, bus, 7, seen) + pick_unique(R, box, 7, seen) + pick_unique(R, est, 6, seen)


def s5(seen):
    def paint():
        area = R.randint(6, 30) * 4
        k = F(R.randint(1, 3), 4)
        use = area * k
        can = R.choice([3, 4, 5, 6])
        cans = -(-int(use) // can) if use.denominator == 1 else None
        if not cans or use % can == 0:
            return None
        q = "牆面有 %d 平方公尺，每平方公尺用 %s 公升油漆。油漆一罐 %d 公升，至少要買幾罐？" % (area, fr(k.numerator, k.denominator), can)
        return mcq(q, "%d 罐" % cans, ["%d 罐" % x for x in (cans - 1, cans + 1, int(area / can))  if x != cans and x > 0],
                   "用油：%d × %s ＝ %s（公升）；%s ÷ %d ＝ %d……%d，不夠的也要買一罐：%d 罐。" % (area, fr(k.numerator, k.denominator), ff(use), ff(use), can, int(use) // can, int(use) % can, cans))

    def walk():
        who = NM.next()
        d = D(R.randint(12, 48)) / 10
        days = R.randint(5, 7)
        weeks = R.randint(2, 4)
        tot = d * days * weeks
        q = "%s每天跑步 %s 公里，每週跑 %d 天。%d 週一共跑幾公里？" % (who, ds(d), days, weeks)
        return mcq(q, "%s 公里" % ds(tot), ["%s 公里" % ds(x) for x in (d * days, d * (days + weeks), tot + d)], "%s × %d × %d ＝ %s（公里）。" % (ds(d), days, weeks, ds(tot)))

    def share():
        cake = R.choice([2, 3, 4])
        each = F(1, R.choice([6, 8, 9, 10, 12]))
        eat = R.randint(3, 8)
        tot_pieces = cake / each
        left = tot_pieces - eat
        if left <= 0:
            return None
        q = "有 %d 個蛋糕，每 %s 個切成一塊。分給 %d 位小朋友每人一塊後，還剩幾塊？" % (cake, fr(1, each.denominator), eat)
        return mcq(q, "%d 塊" % left, ["%d 塊" % x for x in (cake * each.denominator, left + 1, eat)  if x != left], "%d ÷ %s ＝ %d（塊），%d － %d ＝ %d（塊）。" % (cake, fr(1, each.denominator), tot_pieces, tot_pieces, eat, left))
    return pick_unique(R, paint, 7, seen) + pick_unique(R, walk, 7, seen) + pick_unique(R, share, 6, seen)


def main():
    seen = set()
    sets = [("分數的應用", s1(seen)), ("小數的應用", s2(seen)), ("分數和小數混合計算", s3(seen)),
            ("概數：進位、捨去、估算", s4(seen)), ("綜合應用", s5(seen))]
    body = lesson(
        ["先讀懂題目：誰是<b>全部</b>、誰是<b>剩下的</b>，再一步一步列式，最好寫成併式。",
         "分數和小數一起算時，可以都化成小數或都化成分數（<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> ＝ 0.75）。",
         "看情境決定概數：坐車、買罐子要<b>無條件進位</b>；裝滿幾盒要<b>無條件捨去</b>。"],
        [example("有 240 元，用掉 <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>，再用掉剩下的 <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>，還剩多少元？",
                 ["240 × <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> ＝ 80，剩 160。", "160 × <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span> ＝ 40，剩 120。"], "120 元"),
         example("130 人坐 45 人座的車，至少幾輛？", ["130 ÷ 45 ＝ 2……40。", "剩 40 人也要坐車。"], "3 輛")],
        [("「剩下的 1/4」用全部去乘", "要用剩下的量去乘"),
         ("坐車問題把餘數捨去", "還有人沒車坐，要進位"),
         ("分數和小數直接相加", "先化成同一種表示法")])
    faq = [{"q": "「剩下的幾分之幾」怎麼算？",
            "a": "先算出第一次之後剩下多少，再用剩下的量乘以那個分數，不是用全部的量。"},
           {"q": "什麼時候進位、什麼時候捨去？",
            "a": "東西一定要夠用（坐車、買罐子、裝箱子裝完）就無條件進位；問最多能做幾個完整的（裝滿幾盒）就無條件捨去。"},
           {"q": "六年級的應用問題要學什麼？",
            "a": "108課綱 N-6-5：整數、分數、小數的二到三步驟四則應用問題，也包含用概數協助解題。"}]
    make_unit(R, "grade-6", "word-problems", "N-6-5",
              "解題：整數、分數、小數的四則應用問題。二到三步驟的應用解題。含使用概數協助解題。",
              "整數、分數、小數的應用問題",
              "六年級數學 四則應用問題 練習題｜分數・小數・概數 學習單（附解答）",
              "四則應用問題",
              "國小六年級數學「整數、分數、小數的應用問題」免費學習單：剩下的幾分之幾、單價和總價、分數和小數混合計算、無條件進位和捨去、估算與二到三步驟的綜合應用題。100題線上練習馬上對答案，附可列印解答。",
              "先找全部和剩下的，再一步一步列式",
              "坐車要進位，裝滿幾盒要捨去。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
