# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：時間的乘除（108課綱 N-5-16）
  python3 tools/gen_tw_math_g5_time_calculations.py
時間量×整数、時間量÷整数、分數・小數の時間（3/4 小時、0.6 小時）、分鐘⇔小時の分數表示、應用。
誤答：60 進位でなく 100 進位で繰り上がり、0.5 小時＝50 分鐘、3/4 小時＝34 分鐘。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff, dnum

R = random.Random(51016)
NM = Names(R)


def du(m, u=("小時", "分鐘")):
    a, b = divmod(m, 60)
    if a and b:
        return "%d %s %d %s" % (a, u[0], b, u[1])
    return "%d %s" % (a, u[0]) if a else "%d %s" % (b, u[1])


def s1(seen):
    def mk():
        t = R.randint(1, 3) * 60 + R.randint(1, 11) * 5 if R.random() < .6 else R.randint(5, 55)
        n = R.randint(2, 9)
        v = t * n
        a, b = divmod(t, 60)
        wrong = "%d 小時 %d 分鐘" % (a * n, b * n) if b * n >= 60 and a else du(v + 60)
        q = "%s × %d ＝" % (du(t), n)
        return mcq(q, du(v), [wrong, du(v + 60), du(v - 60) if v > 60 else du(v + 120), du(v + 40) if b * n >= 60 else du(v + 10)],
                   "全部換成分鐘：%d × %d ＝ %d 分鐘 ＝ %s。" % (t, n, v, du(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.randint(2, 9)
        per = R.randint(3, 50) * (1 if R.random() < .5 else 5)
        if per > 150:
            return None
        t = per * n
        q = "%s ÷ %d ＝" % (du(t), n)
        a, b = divmod(t, 60)
        w = ["%d 小時 %d 分鐘" % (a // n, b // n) if a % n == 0 and b % n == 0 and t >= 60 else du(per + 10), du(per + 5), du(per * 2), du(t // 100 * 60 // n) if t >= 100 and (t // 100 * 60) % n == 0 and t // 100 * 60 // n != per else du(per - 5) if per > 5 else du(per + 15)]
        return mcq(q, du(per), w, "換成分鐘：%s ＝ %d 分鐘，%d ÷ %d ＝ %d 分鐘%s。" % (du(t), t, t, n, per, "（%s）" % du(per) if per >= 60 else ""))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def f2m():
        d = R.choice([2, 3, 4, 5, 6, 10, 12, 15, 20])
        a = R.randint(1, d - 1)
        if F(a, d).denominator != d:
            return None
        m = 60 * a // d
        return mcq("%s 小時是幾分鐘？" % fr(a, d), "%d 分鐘" % m, ["%d 分鐘" % x for x in (int("%d%d" % (a, d)) if int("%d%d" % (a, d)) < 100 else a * 10, 100 * a // d, m + 5)],
                   "1 小時 ＝ 60 分鐘，60 × %s ＝ %d（分鐘）。" % (fr(a, d), m))

    def d2m():
        x = R.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 0.8, 0.9, 1.5, 1.2, 2.5])
        m = int(round(x * 60))
        return mcq("%s 小時是幾分鐘？" % dnum(x, 2), du(m), [du(int(round(x * 100))), du(m + 10), "%d 分鐘" % int(round(x * 10))] if int(round(x * 100)) != m else [du(m + 10), du(m - 5), "%d 分鐘" % int(round(x * 10))],
                   "60 × %s ＝ %d（分鐘）。小時換分鐘要乘以 60，不是 100。" % (dnum(x, 2), m))

    def m2f():
        m = R.choice([5, 10, 12, 15, 20, 24, 30, 36, 40, 45, 48, 50])
        v = F(m, 60)
        return mcq("%d 分鐘是幾分之幾小時？（最簡分數）" % m, ff(v), [fr(m, 100), ff(F(60, m)), fr(m, 60) if F(m, 60).denominator != 60 else ff(v + F(1, 60))], "%d ÷ 60 ＝ %s ＝ %s（小時）。" % (m, fr(m, 60), ff(v)))
    return pick_unique(R, f2m, 7, seen) + pick_unique(R, d2m, 7, seen) + pick_unique(R, m2f, 6, seen)


def s4(seen):
    def mk():
        kind = R.choice(["frac_mul", "dec_mul"])
        if kind == "frac_mul":
            d = R.choice([2, 3, 4, 5, 6])
            a = R.randint(1, d - 1)
            n = R.randint(2, 9)
            if F(a, d).denominator != d:
                return None
            v = 60 * a * n // d
            if (60 * a * n) % d:
                return None
            q = "每天練琴 %s 小時，%d 天一共練了多少時間？" % (fr(a, d), n)
        else:
            x = R.choice([0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8])
            n = R.randint(2, 9)
            v = int(round(x * 60 * n))
            q = "每天跑步 %s 小時，%d 天一共跑了多少時間？" % (dnum(x, 2), n)
        return mcq(q, du(v), [du(v + 60), du(int(v * 100 / 60)) if int(v * 100 / 60) != v else du(v + 30), du(v // n) if v // n != v else du(v + 15)],
                   "先算一天幾分鐘，再乘以天數：一共 %d 分鐘%s。" % (v, "，就是 " + du(v) if v >= 60 else ""))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        kind = R.choice(["laps", "pages", "make"])
        if kind == "laps":
            per = R.randint(65, 290)
            if per % 60 == 0:
                return None
            n = R.randint(3, 10)
            q = "%s跑一圈要 %s，照這樣跑 %d 圈要多久？" % (NM.next(), du(per, ("分鐘", "秒")), n)
            v = per * n
            return mcq(q, du(v, ("分鐘", "秒")), [du(v + 60, ("分鐘", "秒")), "%d 分鐘 %d 秒" % (per // 60 * n, per % 60 * n) if per % 60 * n >= 60 else du(v + 30, ("分鐘", "秒")), du(per + n, ("分鐘", "秒"))],
                       "%d 秒 × %d ＝ %d 秒 ＝ %s。" % (per, n, v, du(v, ("分鐘", "秒"))))
        if kind == "pages":
            tot = R.randint(2, 4) * 60 + R.choice([0, 30])
            n = R.choice([5, 6, 10, 15, 30])
            if tot % n:
                return None
            q = "%s看完一本 %d 頁的書用了 %s，平均每頁看幾分鐘？" % (NM.next(), n * R.randint(2, 4) if False else tot // (tot // n), du(tot)) if False else "做 %d 個手工藝品一共用了 %s，平均做一個要幾分鐘？" % (n, du(tot))
            v = tot // n
            return mcq(q, du(v), [du(v + 5), du((tot // 60 * 100 + tot % 60) // n) if (tot // 60 * 100 + tot % 60) % n == 0 and (tot // 60 * 100 + tot % 60) // n != v else du(v + 10), du(v * 2)],
                       "%s ＝ %d 分鐘，%d ÷ %d ＝ %d（分鐘）。" % (du(tot), tot, tot, n, v))
        per = R.choice([15, 20, 25, 30, 40, 45])
        tot = R.randint(2, 5) * 60
        if tot % per:
            return None
        q = "烤一盤餅乾要 %d 分鐘，%d 小時最多可以烤幾盤（一盤接一盤）？" % (per, tot // 60)
        v = tot // per
        return mcq(q, "%d 盤" % v, ["%d 盤" % x for x in (tot // 60 * 100 // per if tot // 60 * 100 // per != v else v + 1, v - 1, v * 2)], "%d 小時 ＝ %d 分鐘，%d ÷ %d ＝ %d（盤）。" % (tot // 60, tot, tot, per, v))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("時間 × 整數", s1(seen)), ("時間 ÷ 整數", s2(seen)), ("分數和小數的時間", s3(seen)), ("分數、小數時間的乘法", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["時間的乘除，先<b>全部換成分鐘（或秒）</b>再算，算完再換回幾小時幾分鐘。",
         "1 小時 ＝ 60 分鐘，是 60 進位：%s 小時 ＝ 60 × %s ＝ 45 分鐘；0.5 小時 ＝ 30 分鐘（不是 50 分鐘）。" % (fr(3, 4), fr(3, 4)),
         "分鐘換成小時：除以 60，例如 40 分鐘 ＝ %s 小時。" % fr(2, 3)],
        [example("1 小時 25 分鐘 × 3 ＝", ["1 小時 25 分鐘 ＝ 85 分鐘。", "85 × 3 ＝ 255 分鐘 ＝ 4 小時 15 分鐘。"], "4 小時 15 分鐘"),
         example("0.75 小時是幾分鐘？", ["60 × 0.75 ＝ 45。"], "45 分鐘")],
        [("1 小時 25 分鐘 × 3 ＝ 3 小時 75 分鐘", "滿 60 分鐘要進位：4 小時 15 分鐘"),
         ("0.5 小時 ＝ 50 分鐘", "60 × 0.5 ＝ 30 分鐘"),
         ("%s 小時 ＝ 34 分鐘" % fr(3, 4), "60 × %s ＝ 45 分鐘" % fr(3, 4))])
    faq = [{"q": "時間怎麼做乘除？",
            "a": "先把時間全部換成分鐘，再乘或除，最後換回幾小時幾分鐘。時間是 60 進位，不能像小數一樣用 100 進位。"},
           {"q": "0.5 小時是幾分鐘？",
            "a": "60 × 0.5 ＝ 30 分鐘。小時換分鐘要乘以 60，所以 0.1 小時 ＝ 6 分鐘、0.25 小時 ＝ 15 分鐘。"},
           {"q": "五年級的時間計算要學什麼？",
            "a": "108課綱 N-5-16：在分數和小數學習的範圍內，解決和時間有關的乘除問題。"}]
    make_unit(R, "grade-5", "time-calculations", "N-5-16",
              "解題：時間的乘除問題。在分數和小數學習的範圍內，解決與時間相關的乘除問題。",
              "時間的乘除：分數和小數的時間",
              "五年級數學 時間乘除 練習題｜分數小時・小數小時・時間乘除 學習單（附解答）",
              "時間的乘除",
              "國小五年級數學「時間的乘除」免費學習單：時間乘以整數、時間除以整數、分數和小數的小時換成分鐘、時間的應用題。100題線上練習馬上對答案，附可列印解答。",
              "先換成分鐘，再乘除",
              "1 小時 ＝ 60 分鐘：0.5 小時是 30 分鐘。",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
