# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：三步驟問題併式與平均（108課綱 R-5-1）
  python3 tools/gen_tw_math_g5_three_step_problems_and_averages.py
三步驟問題を一つの算式（併式）に書く、四則混合の順序、平均＝總和÷個數、平均から總和・足りない數を求める、應用。
誤答：括號を忘れる、由左往右だけで計算、平均で個數を 1 少なく割る、總和を答える。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(51024)
NM = Names(R)


def s1(seen):
    def shop():
        a, p = R.randint(2, 6), R.choice([12, 15, 18, 25, 35])
        b, q = R.randint(2, 5), R.choice([20, 30, 45, 60])
        cost = a * p + b * q
        m = 500 if cost < 480 else 1000
        if cost >= m:
            return None
        who = NM.next()
        txt = "%s買 %d 枝原子筆，每枝 %d 元，又買 %d 本筆記本，每本 %d 元，付 %d 元，可以找回多少元？哪一個併式正確？" % (who, a, p, b, q, m)
        ans = "%d －（%d × %d ＋ %d × %d）" % (m, a, p, b, q)
        return mcq(txt, ans, ["%d － %d × %d ＋ %d × %d" % (m, a, p, b, q), "（%d － %d）× %d ＋ %d × %d" % (m, a, p, b, q), "%d －（%d ＋ %d）×（%d ＋ %d）" % (m, a, b, p, q)],
                   "先算總共花的錢 %d × %d ＋ %d × %d，再從 %d 元裡減掉，要加括號：%s ＝ %d（元）。" % (a, p, b, q, m, ans, m - cost))

    def share():
        box, per = R.randint(3, 8), R.choice([12, 18, 24, 30])
        ppl = R.choice([x for x in range(3, 13) if (box * per) % x == 0 and x != per])
        eat = R.randint(1, 3)
        if box * per // ppl <= eat:
            return None
        txt = "有 %d 盒餅乾，每盒 %d 片，平分給 %d 人，每人先吃掉 %d 片，每人還剩幾片？哪一個併式正確？" % (box, per, ppl, eat)
        ans = "%d × %d ÷ %d － %d" % (box, per, ppl, eat)
        return mcq(txt, ans, ["%d × %d ÷（%d － %d）" % (box, per, ppl, eat), "%d × %d － %d ÷ %d" % (box, per, eat, ppl), "%d × %d － %d × %d" % (box, per, ppl, eat)],
                   "總片數 %d × %d，平分 ÷ %d，再減 %d：%s ＝ %d（片）。" % (box, per, ppl, eat, ans, box * per // ppl - eat))

    def seats():
        rows, each, sold = R.randint(12, 30), R.randint(15, 30), R.randint(2, 9)
        txt = "禮堂有 %d 排椅子，每排 %d 張。已經坐滿 %d 排，另外還坐了 %d 人。還有幾張空椅子？哪一個併式正確？" % (rows, each, sold, each - 3)
        used = sold * each + each - 3
        ans = "%d × %d －（%d × %d ＋ %d）" % (rows, each, sold, each, each - 3)
        return mcq(txt, ans, ["%d × %d － %d × %d ＋ %d" % (rows, each, sold, each, each - 3), "（%d － %d）× %d ＋ %d" % (rows, sold, each, each - 3), "%d × %d － %d － %d" % (rows, each, sold, each - 3)],
                   "全部椅子 %d × %d，減去坐了的 %d × %d ＋ %d：%s ＝ %d（張）。" % (rows, each, sold, each, each - 3, ans, rows * each - used))
    return pick_unique(R, shop, 7, seen) + pick_unique(R, share, 7, seen) + pick_unique(R, seats, 6, seen)


def s2(seen):
    def mk():
        k = R.choice(["a+bc-d", "(a+b)c/d", "ab-cd", "a-(b+c)/d", "a/b+c*d"])
        if k == "a+bc-d":
            a, b, c = R.randint(20, 90), R.randint(3, 9), R.randint(4, 12)
            d = R.randint(5, a)
            v = a + b * c - d
            q = "%d ＋ %d × %d － %d" % (a, b, c, d)
            w = [(a + b) * c - d, a + b * (c - d) if c > d else v + b, a + b * c + d]
        elif k == "(a+b)c/d":
            d = R.choice([2, 3, 4, 5, 6])
            c = d * R.randint(2, 6)
            a, b = R.randint(10, 40), R.randint(5, 30)
            v = (a + b) * c // d
            q = "（%d ＋ %d）× %d ÷ %d" % (a, b, c, d)
            w = [a + b * c // d, (a + b) * c, (a + b) * d // c if ((a + b) * d) % c == 0 else v + c]
        elif k == "ab-cd":
            a, b, c, d = R.randint(12, 40), R.randint(3, 9), R.randint(10, 30), R.randint(2, 6)
            if a * b <= c * d:
                return None
            v = a * b - c * d
            q = "%d × %d － %d × %d" % (a, b, c, d)
            w = [(a * b - c) * d, a * (b - c * d) if b > c * d else v + d, a * b + c * d]
        elif k == "a-(b+c)/d":
            d = R.choice([3, 4, 5, 6, 8])
            b = R.randint(10, 60)
            c = d * R.randint(3, 15) - b % d
            if c <= 0:
                return None
            a = R.randint((b + c) // d + 20, 300)
            v = a - (b + c) // d
            q = "%d －（%d ＋ %d）÷ %d" % (a, b, c, d)
            w = [(a - b - c) // d if a > b + c and (a - b - c) % d == 0 else v + d, a - b - c // d if c % d == 0 else v - 1, a - b + c]
        else:
            b = R.choice([3, 4, 5, 6, 8, 9])
            a = b * R.randint(5, 30)
            c, d = R.randint(3, 9), R.randint(6, 15)
            v = a // b + c * d
            q = "%d ÷ %d ＋ %d × %d" % (a, b, c, d)
            w = [(a // b + c) * d, a // (b + c) * d if a % (b + c) == 0 else v + c, a // b + c + d]
        return mcq("計算：%s ＝ ？" % q, num(v), [num(x) for x in w if x >= 0 and x != v],
                   ("先算括號，再算乘除，最後算加減" if "（" in q else "先算乘除，再由左往右算加減") + "：%s ＝ %s。" % (q, num(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    CTX = [("數學小考", "分", 60, 100), ("一週每天跳繩", "下", 80, 200), ("五個人的身高", "公分", 128, 160),
           ("每天收集的寶特瓶", "個", 15, 60), ("一週每天的讀書時間", "分鐘", 20, 90), ("幾箱蘋果的重量", "公斤", 8, 20)]

    def mk():
        name, u, lo, hi = R.choice(CTX)
        n = R.randint(3, 6)
        if "一週" in name:
            n = 7
        if "五個人" in name:
            n = 5
        avg = R.randint(lo + 3, hi - 3)
        vals = [avg] * n
        for _ in range(n * 2):
            i, j = R.sample(range(n), 2)
            t = R.randint(1, max(2, (hi - lo) // 6))
            if lo <= vals[i] + t <= hi and lo <= vals[j] - t <= hi:
                vals[i] += t
                vals[j] -= t
        if len(set(vals)) < 3:
            return None
        s = sum(vals)
        q = "%s：%s（%s）。平均是多少%s？" % (name, "、".join(num(v) for v in vals), u, u)
        w = [s, s // (n - 1) if s % (n - 1) == 0 else avg + 2, (max(vals) + min(vals)) // 2 if (max(vals) + min(vals)) // 2 != avg else avg - 1, avg + 1]
        return mcq(q, "%s %s" % (num(avg), u), ["%s %s" % (num(x), u) for x in w if x != avg],
                   "平均 ＝ 總和 ÷ 個數：（%s）÷ %d ＝ %s ÷ %d ＝ %s（%s）。" % (" ＋ ".join(num(v) for v in vals), n, num(s), n, num(avg), u))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def total():
        n, avg = R.randint(3, 8), R.randint(62, 95)
        who = NM.next()
        q = "%s %d 次測驗的平均是 %d 分，%d 次一共得幾分？" % (who, n, avg, n)
        return mcq(q, "%d 分" % (n * avg), ["%d 分" % x for x in (avg, avg + n, n * avg + avg, n * avg - avg)],
                   "總和 ＝ 平均 × 個數：%d × %d ＝ %d（分）。" % (avg, n, n * avg))

    def missing():
        n = R.randint(4, 5)
        avg = R.randint(70, 90)
        vals = [avg + R.randint(-8, 8) for _ in range(n - 1)]
        last = n * avg - sum(vals)
        if not (55 <= last <= 100) or last in vals:
            return None
        who = NM.next()
        q = "%s %d 次考試的平均是 %d 分。前 %d 次是 %s 分，第 %d 次是幾分？" % (who, n, avg, n - 1, "、".join(map(str, vals)), n)
        return mcq(q, "%d 分" % last, ["%d 分" % x for x in (avg, (n - 1) * avg - sum(vals) + avg if False else n * avg - sum(vals[:-1]), last + n, sum(vals) // (n - 1))],
                   "%d 次總和 %d × %d ＝ %d，減去前 %d 次的 %d：%d － %d ＝ %d（分）。" % (n, avg, n, n * avg, n - 1, sum(vals), n * avg, sum(vals), last))

    def join():
        n, avg = R.randint(4, 9), R.randint(34, 45)
        new = avg + R.choice([-1, 1]) * (n + 1) * R.randint(1, 2)
        if not 28 <= new <= 55:
            return None
        navg = (n * avg + new) // (n + 1)
        if (n * avg + new) % (n + 1):
            return None
        q = "一組 %d 位同學的平均體重是 %d 公斤，再加入一位 %d 公斤的同學，新的平均是幾公斤？" % (n, avg, new)
        return mcq(q, "%d 公斤" % navg, ["%d 公斤" % x for x in ((avg + new) // 2, avg, navg + (1 if navg + 1 != avg else 2), n * avg + new) if x != navg],
                   "新總和 %d × %d ＋ %d ＝ %d，人數 %d：%d ÷ %d ＝ %d（公斤）。" % (avg, n, new, n * avg + new, n + 1, n * avg + new, n + 1, navg))
    return pick_unique(R, total, 7, seen) + pick_unique(R, missing, 7, seen) + pick_unique(R, join, 6, seen)


def s5(seen):
    def bus():
        cls, st = R.randint(4, 8), R.randint(26, 32)
        tch = cls
        seat = R.choice([40, 45])
        tot = cls * st + tch
        bus_n = -(-tot // seat)
        q = "五年級有 %d 班，每班 %d 人，每班再加 1 位老師。坐 %d 人座的遊覽車去校外教學，至少要幾輛車？" % (cls, st, seat)
        return mcq(q, "%d 輛" % bus_n, ["%d 輛" % x for x in (tot // seat if tot // seat != bus_n else bus_n + 1, bus_n + 1, -(-cls * st // seat) if -(-cls * st // seat) != bus_n else bus_n - 1, bus_n + 2) if x > 0],
                   "總人數 %d × %d ＋ %d ＝ %d，%d ÷ %d ＝ %d……%d，剩下的人也要坐車，所以要 %d 輛。" % (cls, st, tch, tot, tot, seat, tot // seat, tot % seat, bus_n) if tot % seat else
                   "總人數 %d × %d ＋ %d ＝ %d，%d ÷ %d ＝ %d（輛）。" % (cls, st, tch, tot, tot, seat, bus_n))

    def save():
        who = NM.next()
        have, wk, wkn = R.choice([120, 250, 380]), R.choice([50, 80, 120, 150]), R.randint(4, 10)
        price = have + wk * wkn + R.choice([-1, 1]) * R.choice([30, 60, 90])
        left = have + wk * wkn - price
        if left <= 0:
            q = "%s有 %d 元，以後每週存 %d 元，存 %d 週後，想買一台 %d 元的腳踏車，還差多少元？" % (who, have, wk, wkn, price)
            ans = -left
            w = [price - wk * wkn, price - have, ans + wk]
            e = "%d －（%d ＋ %d × %d）＝ %d（元）。" % (price, have, wk, wkn, ans)
        else:
            q = "%s有 %d 元，以後每週存 %d 元，存 %d 週後，買一台 %d 元的腳踏車，還剩多少元？" % (who, have, wk, wkn, price)
            ans = left
            w = [(have + wk) * wkn - price if (have + wk) * wkn > price else ans + wk, have + wk - price + wkn if have + wk + wkn > price else ans + 2 * wk, ans + have]
            e = "%d ＋ %d × %d － %d ＝ %d（元）。" % (have, wk, wkn, price, ans)
        return mcq(q, "%s 元" % num(ans), ["%s 元" % num(x) for x in w if x > 0 and x != ans], e)

    def avg_word():
        who = NM.next()
        d = R.choice([5, 6])
        a = R.randint(35, 60)
        rest = R.randint(70, 110)
        tot = a * d + rest
        if tot % (d + 1):
            return None
        q = "%s前 %d 天平均每天看 %d 頁書，第 %d 天看了 %d 頁。這 %d 天平均每天看幾頁？" % (who, d, a, d + 1, rest, d + 1)
        v = tot // (d + 1)
        return mcq(q, "%d 頁" % v, ["%d 頁" % x for x in ((a + rest) // 2, a * d + rest, v + 2, a) if x != v],
                   "總頁數 %d × %d ＋ %d ＝ %d，平均 %d ÷ %d ＝ %d（頁）。" % (a, d, rest, tot, tot, d + 1, v))
    return pick_unique(R, bus, 7, seen) + pick_unique(R, save, 7, seen) + pick_unique(R, avg_word, 6, seen)


def main():
    seen = set()
    sets = [("把三步驟問題寫成併式", s1(seen)), ("四則混合計算", s2(seen)), ("求平均", s3(seen)),
            ("用平均求總和和缺少的數", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["三步驟問題可以把每一步合成<b>一個算式（併式）</b>，該先算的部分要加<b>括號</b>。",
         "計算順序：<b>括號先算 → 再算乘除 → 最後加減</b>；同一級由左往右算。",
         "<b>平均 ＝ 總和 ÷ 個數</b>；反過來，<b>總和 ＝ 平均 × 個數</b>。"],
        [example("買 3 枝 15 元的筆和 2 本 30 元的簿子，付 200 元，找回多少元？", ["併式：200 －（3 × 15 ＋ 2 × 30）。", "＝ 200 －（45 ＋ 60）＝ 200 － 105。"], "95 元"),
         example("4 次考試 82、90、76、88 分，平均幾分？", ["總和 82 ＋ 90 ＋ 76 ＋ 88 ＝ 336。", "336 ÷ 4 ＝ 84。"], "84 分")],
        [("200 － 3 × 15 ＋ 2 × 30（忘了括號）", "全部花的錢要先算：200 －（3 × 15 ＋ 2 × 30）"),
         ("4 個數的總和除以 3", "有幾個數就除以幾"),
         ("知道平均就當成總和", "總和 ＝ 平均 × 個數")])
    faq = [{"q": "什麼是併式？",
            "a": "把好幾個步驟的算式合成一個算式，例如 200 －（3 × 15 ＋ 2 × 30）。108課綱 R-5-1 要求五年級養成用併式記錄三步驟問題的習慣，方便解題和驗算。"},
           {"q": "平均怎麼算？",
            "a": "把所有的數加起來得到總和，再除以個數。例如 82、90、76、88 的平均是 336 ÷ 4 ＝ 84。"},
           {"q": "知道平均，怎麼求缺少的數？",
            "a": "先用平均 × 個數算出總和，再減去已知的數，剩下的就是缺少的數。"}]
    make_unit(R, "grade-5", "three-step-problems-and-averages", "R-5-1",
              "三步驟問題併式：建立將計算步驟併式的習慣，以三步驟為主。介紹「平均」。與分配律連結。",
              "三步驟問題併式與平均",
              "五年級數學 併式與平均 練習題｜三步驟問題・四則混合・平均 學習單（附解答）",
              "併式與平均",
              "國小五年級數學「三步驟問題併式與平均」免費學習單：把三步驟問題寫成一個算式、四則混合計算順序、求平均、用平均求總和和缺少的數與應用題。100題線上練習馬上對答案，附可列印解答。",
              "平均 ＝ 總和 ÷ 個數",
              "三步驟問題寫成一個併式，先算的部分加括號。",
              body, faq, sets, 24)


if __name__ == "__main__":
    main()
