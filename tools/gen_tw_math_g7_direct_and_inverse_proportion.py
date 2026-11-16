# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：正比與反比（108課綱 N-7-9）
  python3 tools/gen_tw_math_g7_direct_and_inverse_proportion.py
正比 y＝kx（y÷x が一定）、反比 xy＝k（積が一定）、表から判斷、k を求めて值を求める、生活の例（速さ・時間・價格・人數と日數）。
誤答：一方が増えれば他方も増える＝正比と決めつける（y＝x＋3 は正比ではない）、反比で比を使う、k を逆數で求める。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table, num
from tw_g7 import sn, tidy_sets

R = random.Random(71020)
NM = Names(R)
K3 = ["正比", "反比", "都不是"]


def s1(seen):
    def mk():
        k = R.choice(["dir", "inv", "none"])
        xs = sorted(R.sample([1, 2, 3, 4, 5, 6, 8, 10, 12], 4))
        if k == "dir":
            c = R.randint(2, 9)
            ys = [c * x for x in xs]
            e = "y ÷ x 都是 %d，是正比（y ＝ %dx）。" % (c, c)
        elif k == "inv":
            c = 120
            ys = [F(c, x) for x in xs]
            if any(y.denominator != 1 for y in ys):
                return None
            e = "x × y 都是 %d，是反比（xy ＝ %d）。" % (c, c)
        else:
            c = R.randint(1, 9)
            ys = [x + c for x in xs]
            e = "y ÷ x 不固定、x × y 也不固定（y ＝ x ＋ %d），都不是。" % c
        tb = table(["x"] + [str(x) for x in xs], [["y"] + [sn(y) for y in ys]])
        ans = {"dir": "正比", "inv": "反比", "none": "都不是"}[k]
        return mcq("表中 x 和 y 是正比、反比，還是都不是？" + tb, ans, [t for t in K3 if t != ans] + ["無法判斷"], e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        k = R.choice(["dir", "inv"])
        x1 = R.randint(2, 12)
        if k == "dir":
            c = R.randint(2, 9)
            y1 = c * x1
            x2 = R.randint(2, 15)
            v = c * x2
            q = "y 和 x 成正比，當 x ＝ %d 時 y ＝ %d。x ＝ %d 時，y ＝ ？" % (x1, y1, x2)
            w = [F(x1 * y1, x2), y1 + (x2 - x1), v + c]
            e = "y ＝ kx，k ＝ %d ÷ %d ＝ %d，y ＝ %d × %d ＝ %d。" % (y1, x1, c, c, x2, v)
        else:
            c = R.choice([24, 36, 48, 60, 72, 120])
            divs = [d for d in range(2, c) if c % d == 0]
            x1, x2 = R.sample(divs, 2)
            y1 = c // x1
            v = c // x2
            q = "y 和 x 成反比，當 x ＝ %d 時 y ＝ %d。x ＝ %d 時，y ＝ ？" % (x1, y1, x2)
            w = [F(y1 * x2, x1), y1 - (x2 - x1) if y1 - (x2 - x1) > 0 else y1 + 1, c]
            e = "xy ＝ k，k ＝ %d × %d ＝ %d，y ＝ %d ÷ %d ＝ %d。" % (x1, y1, c, c, x2, v)
        return mcq(q, sn(v), [sn(t) for t in w if t != v] + [sn(v + 1)], e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = R.choice(["dir", "inv", "none1", "none2"])
        c = R.randint(2, 9)
        if k == "dir":
            eq, ans = R.choice(["y ＝ %dx" % c, "y ＝ <span class='fr'><span class='fn'>x</span><span class='fd'>%d</span></span>" % c, "<span class='fr'><span class='fn'>y</span><span class='fd'>x</span></span> ＝ %d" % c]), "正比"
        elif k == "inv":
            eq, ans = R.choice(["xy ＝ %d" % (c * 6), "y ＝ <span class='fr'><span class='fn'>%d</span><span class='fd'>x</span></span>" % (c * 6)]), "反比"
        elif k == "none1":
            eq, ans = "y ＝ %dx ＋ %d" % (c, R.randint(1, 9)), "都不是"
        else:
            eq, ans = "x ＋ y ＝ %d" % (c * 5), "都不是"
        return mcq("關係式 %s 中，y 和 x 是什麼關係？" % eq, ans, [t for t in K3 if t != ans] + ["無法判斷"], {"正比": "可以寫成 y ＝ kx（k 不為 0），是正比。", "反比": "可以寫成 xy ＝ k（k 不為 0），是反比。", "都不是": "不能寫成 y ＝ kx，也不能寫成 xy ＝ k，所以都不是。"}[ans])
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    LIFE = [("固定單價下，買的數量和總價", "正比"), ("固定速度下，行走的時間和距離", "正比"), ("固定距離下，速度和所需時間", "反比"),
            ("工作總量固定時，人數和完成的天數", "反比"), ("正方形的邊長和周長", "正比"), ("面積固定的長方形，長和寬", "反比"),
            ("一個人的年齡和身高", "都不是"), ("正方形的邊長和面積", "都不是"), ("固定總價下，每人分攤的錢和人數", "反比"),
            ("每天存一樣多的錢，存的天數和存款總額（一開始是 0）", "正比"), ("搭計程車的距離和車資（有起跳價）", "都不是"), ("圓的半徑和圓周長", "正比")]
    out = []
    for it, ans in LIFE:
        out.append(mcq("「%s」是正比、反比，還是都不是？" % it, ans, [t for t in K3 if t != ans] + ["無法判斷"],
                       {"正比": "一個變成幾倍，另一個也變成幾倍，比值固定。", "反比": "一個變成幾倍，另一個就變成幾分之一，乘積固定。", "都不是": "比值和乘積都不固定。"}[ans]))
    for o in out:
        seen.add(o["q"])

    def more():
        p = R.choice([15, 25, 35, 45])
        n = R.randint(2, 20)
        q = "一枝筆 %d 元，買 x 枝要付 y 元。x ＝ %d 時 y ＝ ？y 和 x 是什麼關係？" % (p, n)
        ans = "y ＝ %d，正比" % (p * n)
        return mcq(q, ans, ["y ＝ %d，反比" % (p * n), "y ＝ %d，正比" % (p + n), "y ＝ %d，都不是" % (p * n)], "y ＝ %dx，y ÷ x 固定，是正比；%d × %d ＝ %d。" % (p, p, n, p * n))
    return out + pick_unique(R, more, 8, seen)


def s5(seen):
    def work():
        p, d = R.choice([(6, 10), (8, 15), (12, 20), (10, 12), (5, 24), (9, 16)])
        p2 = R.choice([x for x in range(2, 31) if (p * d) % x == 0 and x != p])
        v = p * d // p2
        q = "%d 個人做一件工作要 %d 天。每人效率一樣，%d 個人要幾天？" % (p, d, p2)
        return mcq(q, "%d 天" % v, ["%s 天" % sn(t) for t in (F(d * p2, p), d + p - p2 if d + p - p2 > 0 else d + 1, p * d)  if t != v], "人數和天數成反比：%d × %d ＝ %d，%d ÷ %d ＝ %d（天）。" % (p, d, p * d, p * d, p2, v))

    def speed():
        v1, t1 = R.choice([(60, 3), (80, 2), (40, 6), (50, 4), (90, 2)])
        v2 = R.choice([x for x in (30, 40, 45, 60, 80, 90, 120) if (v1 * t1 * 60) % x == 0 and x != v1])
        tot = v1 * t1
        t2 = F(tot, v2)
        q = "以時速 %d 公里開車要 %d 小時。改用時速 %d 公里，要幾小時？" % (v1, t1, v2)
        return mcq(q, "%s 小時" % sn(t2), ["%s 小時" % sn(t) for t in (F(t1 * v2, v1), t1 + F(v1 - v2, 10), F(tot))  if t != t2], "距離固定，速度和時間成反比：%d × %d ＝ %d，%d ÷ %d ＝ %s（小時）。" % (v1, t1, tot, tot, v2, sn(t2)))

    def gas():
        L, km = R.choice([(5, 60), (4, 50), (8, 120), (6, 90)])
        L2 = R.randint(10, 40)
        v = F(km * L2, L)
        if v.denominator != 1:
            return None
        q = "一輛車用 %d 公升汽油可以跑 %d 公里。用 %d 公升可以跑幾公里？" % (L, km, L2)
        return mcq(q, "%d 公里" % v, ["%s 公里" % sn(t) for t in (F(km * L, L2), km + L2 - L, v + km)  if t != v], "油量和距離成正比：%d：%d ＝ %d：x，x ＝ %d。" % (L, km, L2, v))
    return pick_unique(R, work, 7, seen) + pick_unique(R, speed, 6, seen) + pick_unique(R, gas, 7, seen)


def main():
    seen = set()
    sets = [("從表格判斷", s1(seen)), ("求另一個值", s2(seen)), ("從關係式判斷", s3(seen)),
            ("生活中的正比和反比", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>正比</b>：y ＝ kx（k ≠ 0），<b>y ÷ x 固定</b>。x 變成 2 倍，y 也變成 2 倍。",
         "<b>反比</b>：xy ＝ k（k ≠ 0），<b>x × y 固定</b>。x 變成 2 倍，y 變成一半。",
         "注意：x 變大 y 也變大，不一定是正比，例如 y ＝ x ＋ 3 就都不是。",
         "解題：先用一組數求出 k，再求另一個值。"],
        [example("y 和 x 成正比，x ＝ 4 時 y ＝ 12，x ＝ 7 時 y ＝ ？", ["k ＝ 12 ÷ 4 ＝ 3。", "y ＝ 3 × 7。"], "21"),
         example("6 人做一件事要 10 天，15 人要幾天？", ["反比：6 × 10 ＝ 60。", "60 ÷ 15 ＝ 4。"], "4 天")],
        [("y ＝ x ＋ 3 是正比", "y ÷ x 不固定，不是正比"),
         ("反比用 6：10 ＝ 15：x", "反比是乘積固定：6 × 10 ＝ 15 × x"),
         ("正方形邊長和面積成正比", "面積 ＝ 邊長²，比值不固定")])
    faq = [{"q": "怎麼判斷是正比還是反比？",
            "a": "算每一組的 y ÷ x，都一樣就是正比；算每一組的 x × y，都一樣就是反比；兩個都不固定就都不是。"},
           {"q": "生活中常見的反比有哪些？",
            "a": "距離固定時速度和時間、工作量固定時人數和天數、面積固定時長方形的長和寬。"},
           {"q": "七年級的正比和反比要學什麼？",
            "a": "108課綱 N-7-9：比、比例式、正比、反比，以及相關的基本運算與應用問題。"}]
    make_unit(R, "grade-7", "direct-and-inverse-proportion", "N-7-9",
              "比與比例式：比；比例式；正比；反比；相關之基本運算與應用問題，教學情境應以有意義之比值為例。",
              "正比與反比",
              "七年級數學 正比與反比 練習題｜y＝kx・xy＝k・工作天數 學習單（附解答）",
              "正比與反比",
              "國中七年級數學「正比與反比」免費學習單：從表格和關係式判斷正比、反比、都不是，求另一個值，生活中的正比和反比與工作天數、速度時間應用題。100題線上練習馬上對答案，附可列印解答。",
              "正比：y ÷ x 固定；反比：x × y 固定",
              "x 變大 y 也變大，不一定是正比。",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
