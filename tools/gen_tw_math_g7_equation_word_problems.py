# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：一元一次方程式的應用（108課綱 A-7-2、A-7-3）
  python3 tools/gen_tw_math_g7_equation_word_problems.py
情境から方程式を立てる（式を選ぶ）、連續整數、年齡、買い物（二種類の個數）、分配（盈虧）、行程、打折・利潤。
誤答：未知數の設定と式の向きが合わない、盈虧で多い・少ないの符號を逆にする、年齡で兩方に年數を足し忘れる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g7 import sn, tidy_sets

R = random.Random(71013)
NM = Names(R)


def s1(seen):
    def mk():
        k = R.choice(["buy", "age", "share", "sum"])
        if k == "buy":
            p, n, extra = R.choice([15, 20, 25, 35]), R.randint(3, 9), R.choice([10, 20, 30, 50])
            tot = p * n + extra
            q = "買 x 枝筆，每枝 %d 元，再買一本 %d 元的筆記本，共付 %d 元。哪一個方程式正確？" % (p, extra, tot)
            ans = "%dx ＋ %d ＝ %d" % (p, extra, tot)
            w = ["%d（x ＋ %d）＝ %d" % (p, extra, tot), "%dx ＝ %d ＋ %d" % (p, tot, extra), "x ＋ %d ＝ %d" % (p + extra, tot)]
        elif k == "age":
            a, y = R.randint(3, 5), R.randint(3, 10)
            q = "爸爸的年齡是兒子的 %d 倍。兒子 x 歲，%d 年後兩人年齡和是 %d 歲。哪一個方程式正確？" % (a, y, (a + 1) * R.randint(8, 12) + 2 * y)
            tot = int(q.split("是 ")[-1].split(" 歲")[0])
            ans = "x ＋ %dx ＋ %d ＝ %d" % (a, 2 * y, tot)
            w = ["x ＋ %dx ＋ %d ＝ %d" % (a, y, tot), "%dx ＋ %d ＝ %d" % (a, 2 * y, tot), "x ＋ %dx ＝ %d ＋ %d" % (a, tot, 2 * y)]
        elif k == "share":
            a, b, c, d = R.randint(3, 6), R.randint(2, 9), 0, R.randint(2, 9)
            c = a + 1
            q = "一些糖果分給 x 位小朋友，每人 %d 顆會剩 %d 顆；每人 %d 顆會少 %d 顆。哪一個方程式正確？" % (a, b, c, d)
            ans = "%dx ＋ %d ＝ %dx － %d" % (a, b, c, d)
            w = ["%dx － %d ＝ %dx ＋ %d" % (a, b, c, d), "%dx ＋ %d ＝ %dx ＋ %d" % (a, b, c, d), "%dx ＋ %dx ＝ %d ＋ %d" % (a, c, b, d)]
        else:
            n = R.randint(3, 4)
            x = R.randint(5, 40)
            tot = sum(x + i for i in range(n))
            q = "%d 個連續整數的和是 %d，最小的數是 x。哪一個方程式正確？" % (n, tot)
            ans = " ＋ ".join(["x"] + ["（x ＋ %d）" % i for i in range(1, n)]) + " ＝ %d" % tot
            w = ["%dx ＝ %d" % (n, tot), " ＋ ".join(["x"] + ["（x ＋ %d）" % (2 * i) for i in range(1, n)]) + " ＝ %d" % tot, "x ＋ %d ＝ %d" % (n, tot)]
        return mcq(q, ans, w, "找出等量關係，兩邊表示同一個量：%s。" % ans)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def consec():
        n = R.choice([3, 4, 5])
        step = R.choice([1, 2])
        x = R.randint(5, 60) if step == 1 else R.randrange(5, 60, 2)
        tot = sum(x + step * i for i in range(n))
        kind = "連續整數" if step == 1 else ("連續奇數" if x % 2 else "連續偶數")
        q = "%d 個%s的和是 %d，最大的數是多少？" % (n, kind, tot)
        big = x + step * (n - 1)
        return mcq(q, str(big), [str(t) for t in (x, tot // n, big + step)  if t != big] + [str(big - step)], "設最小的是 x：%dx ＋ %d ＝ %d，x ＝ %d，最大是 %d。" % (n, sum(step * i for i in range(n)), tot, x, big))

    def age():
        son = R.randint(6, 14)
        m = R.choice([3, 4])
        dad = son * m
        y = R.randint(2, 10)
        tot = son + dad + 2 * y
        q = "爸爸的年齡是兒子的 %d 倍，%d 年後兩人年齡和是 %d 歲。兒子今年幾歲？" % (m, y, tot)
        return mcq(q, "%d 歲" % son, ["%d 歲" % t for t in ((tot - y) // (m + 1) if (tot - y) % (m + 1) == 0 and (tot - y) // (m + 1) != son else son + 1, tot // (m + 1) if tot // (m + 1) != son else son + 2, dad)], "x ＋ %dx ＋ %d ＝ %d，%dx ＝ %d，x ＝ %d。兩個人都要加 %d 歲。" % (m, 2 * y, tot, m + 1, tot - 2 * y, son, y))
    return pick_unique(R, consec, 10, seen) + pick_unique(R, age, 10, seen)


def s3(seen):
    def buy():
        n = R.randint(8, 20)
        a = R.randint(1, n - 1)
        names, (p1, p2) = R.choice([(("原子筆", "鉛筆", "枝"), R.choice([(12, 8), (15, 10), (20, 12)])), (("大杯飲料", "小杯飲料", "杯"), R.choice([(50, 35), (60, 45), (40, 25)])), (("全票", "半票", "張"), R.choice([(250, 150), (300, 180), (200, 120)]))])
        mw = names[2]
        tot = p1 * a + p2 * (n - a)
        q = "%s每%s %d 元，%s每%s %d 元。兩種共買 %d %s，付了 %d 元。%s買了幾%s？" % (names[0], mw, p1, names[1], mw, p2, n, mw, tot, names[0], mw)
        return mcq(q, "%d %s" % (a, mw), ["%d %s" % (t, mw) for t in (n - a, tot // p1, a + 1)  if t != a], ("設%s x " + mw + "：%dx ＋ %d（%d － x）＝ %d，%dx ＝ %d，x ＝ %d。") % (names[0], p1, p2, n, tot, p1 - p2, tot - p2 * n, a))

    def share():
        x = R.randint(5, 15)
        a = R.randint(3, 6)
        b = R.randint(2, 9)
        d = R.randint(1, 9)
        c = a + 1
        if c * x - d != a * x + b:
            x = b + d
        candy = a * x + b
        q = "一些糖果分給小朋友，每人 %d 顆會剩 %d 顆；每人 %d 顆會少 %d 顆。有幾位小朋友？糖果有幾顆？" % (a, b, c, d)
        ans = "%d 位，%d 顆" % (x, candy)
        return mcq(q, ans, ["%d 位，%d 顆" % (abs(b - d), a * abs(b - d) + b) if b != d else "%d 位，%d 顆" % (x + 1, a * (x + 1) + b), "%d 位，%d 顆" % (x, candy + b), "%d 位，%d 顆" % (x + 2, candy + 2 * a)],
                   "設 x 人：%dx ＋ %d ＝ %dx － %d，x ＝ %d；糖果 %d × %d ＋ %d ＝ %d 顆。" % (a, b, c, d, x, a, x, b, candy))
    return pick_unique(R, buy, 10, seen) + pick_unique(R, share, 10, seen)


def s4(seen):
    def chase():
        v1, v2 = R.choice([(60, 80), (50, 75), (70, 90), (60, 100), (40, 60)])
        t0 = R.choice([5, 10, 15])
        t = v1 * t0 // (v2 - v1)
        if v1 * t0 % (v2 - v1):
            return None
        n1, n2 = NM.next(), NM.next()
        if n1 == n2:
            return None
        q = "%s以分速 %d 公尺從家出發，%d 分鐘後%s以分速 %d 公尺沿同一條路去追。%s出發後幾分鐘追上？" % (n1, v1, t0, n2, v2, n2)
        return mcq(q, "%d 分鐘" % t, ["%d 分鐘" % x for x in (t + t0, v1 * t0 // v2 if v1 * t0 // v2 not in (t, t + t0) else t + 2, t0)  if x != t], "%dx ＝ %d（x ＋ %d），%dx ＝ %d，x ＝ %d。" % (v2, v1, t0, v2 - v1, v1 * t0, t))

    def meet():
        v1, v2 = R.choice([(60, 90), (70, 80), (50, 100), (65, 85)])
        t = R.randint(4, 15)
        d = (v1 + v2) * t
        q = "甲、乙兩地相距 %s 公尺，兩人同時從兩地出發，相向而行，分速分別是 %d 公尺和 %d 公尺。幾分鐘後相遇？" % (num(d), v1, v2)
        return mcq(q, "%d 分鐘" % t, ["%d 分鐘" % x for x in (d // (v2 - v1) if d % (v2 - v1) == 0 else t * 2, t + 2, d // v2 if d % v2 == 0 and d // v2 != t else t - 1)  if x != t and x > 0], "%dx ＋ %dx ＝ %s，%dx ＝ %s，x ＝ %d。" % (v1, v2, num(d), v1 + v2, num(d), t))
    return pick_unique(R, chase, 10, seen) + pick_unique(R, meet, 10, seen)


def s5(seen):
    def discount():
        orig = R.randint(4, 30) * 100
        off = R.choice([8, 7, 75, 85, 9])
        rate = off / 10 if off < 10 else off / 100
        pay = int(orig * rate)
        q = "一件外套打 %d 折後賣 %s 元，原價是多少元？" % (off, num(pay))
        return mcq(q, "%s 元" % num(orig), ["%s 元" % num(x) for x in (int(pay * rate), pay + int(orig * (1 - rate)) + 100, pay * 2)  if x != orig], "設原價 x 元：%sx ＝ %s，x ＝ %s。" % (("%.1f" % rate).rstrip("0").rstrip(".") if off < 10 else "%.2f" % rate, num(pay), num(orig)))

    def coins():
        n = R.randint(10, 30)
        a = R.randint(1, n - 1)
        tot = 10 * a + 5 * (n - a)
        q = "撲滿裡有 10 元和 5 元硬幣共 %d 枚，合計 %d 元。10 元硬幣有幾枚？" % (n, tot)
        return mcq(q, "%d 枚" % a, ["%d 枚" % t for t in (n - a, tot // 10, a + 2)  if t != a], "10x ＋ 5（%d － x）＝ %d，5x ＝ %d，x ＝ %d。" % (n, tot, tot - 5 * n, a))

    def rect():
        w = R.randint(3, 20)
        d = R.randint(2, 10)
        P = 2 * (w + w + d)
        q = "長方形的長比寬多 %d 公分，周長是 %d 公分。寬是幾公分？" % (d, P)
        return mcq(q, "%d 公分" % w, ["%d 公分" % t for t in (w + d, P // 4, (P - d) // 2 if (P - d) // 2 != w else w + 1)  if t != w], "2（x ＋ x ＋ %d）＝ %d，4x ＋ %d ＝ %d，x ＝ %d。" % (d, P, 2 * d, P, w))
    return pick_unique(R, discount, 6, seen) + pick_unique(R, coins, 7, seen) + pick_unique(R, rect, 7, seen)


def main():
    seen = set()
    sets = [("列出方程式", s1(seen)), ("連續整數和年齡", s2(seen)), ("買東西和分配", s3(seen)),
            ("行程問題", s4(seen)), ("綜合應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["解應用題四步驟：<b>設未知數 → 找等量關係列式 → 解方程式 → 驗算並回答</b>。",
         "設要問的量為 x，其他的量都用 x 表示。",
         "常見等量：總價、總人數、兩種方式分配同一堆東西（盈虧）、追上時兩人走的距離相等。"],
        [example("糖果分給小朋友，每人 3 顆剩 5 顆，每人 4 顆少 2 顆，有幾人？", ["設 x 人：3x ＋ 5 ＝ 4x － 2。", "x ＝ 7。"], "7 人"),
         example("3 個連續整數的和是 72，最小的是？", ["x ＋（x ＋ 1）＋（x ＋ 2）＝ 72。", "3x ＋ 3 ＝ 72，x ＝ 23。"], "23")],
        [("盈虧問題寫成 3x － 5 ＝ 4x ＋ 2", "剩下的要加，不夠的要減：3x ＋ 5 ＝ 4x － 2"),
         ("幾年後只幫一個人加歲數", "兩個人都要加"),
         ("解出 x 就停", "要驗算，並回答題目問的量")])
    faq = [{"q": "應用題怎麼找等量關係？",
            "a": "找題目中「同一個量的兩種說法」，例如糖果總數用兩種分法表示、兩人走的距離相等、總價等於各部分的和。"},
           {"q": "未知數要設哪一個？",
            "a": "通常設題目要問的量；如果另一個量比較好表示其他量，也可以設它，最後再換算成答案。"},
           {"q": "七年級的方程式應用要學什麼？",
            "a": "108課綱 A-7-2、A-7-3：在具體情境中列出一元一次方程式，用等量公理、移項法則解題並驗算。"}]
    make_unit(R, "grade-7", "equation-word-problems", "A-7-3",
              "一元一次方程式的解法與應用：等量公理；移項法則；驗算；應用問題。",
              "一元一次方程式的應用",
              "七年級數學 方程式應用題 練習題｜連續整數・年齡・盈虧・行程 學習單（附解答）",
              "方程式的應用",
              "國中七年級數學「一元一次方程式的應用」免費學習單：列出方程式、連續整數和年齡問題、買東西和盈虧分配、追趕和相遇的行程問題與打折、硬幣、周長綜合應用。100題線上練習馬上對答案，附可列印解答。",
              "設未知數 → 列式 → 解 → 驗算",
              "找出同一個量的兩種表示法，用等號連起來。",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
