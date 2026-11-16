# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：四則計算規律（加減混合、乘除混合、運算性質）（108課綱 R-4-2）
  python3 tools/gen_tw_math_g4_calculation_rules.py
交換律・結合律（加法・乘法）、a－b－c＝a－(b＋c)、a＋b－c＝a－c＋b、a×b÷c＝a÷c×b、a÷b÷c＝a÷(b×c)、くふうした計算（25×4、125×8）。
誤答：a－b－c＝a－(b－c)、a÷b÷c＝a÷(b÷c)、減法・除法で交換してしまう。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(41021)
NM = Names(R)


def s1(seen):
    def mk():
        k = R.choice(["add", "mul"])
        if k == "add":
            a, b, c = R.randint(12, 199), R.randint(12, 199), R.randint(12, 199)
            q = "下面哪一個算式和 %d ＋ %d ＋ %d 的答案一樣？" % (a, b, c)
            ans = "%d ＋（%d ＋ %d）" % (a, b, c)
            w = ["%d －（%d ＋ %d）" % (a, b, c), "%d ＋ %d － %d" % (a, b, c), "（%d ＋ %d）× %d" % (a, b, c)]
            return mcq(q, ans, w, "加法可以換順序、換組合（交換律、結合律），答案不變。")
        a, b, c = R.randint(2, 30), R.randint(2, 9), R.randint(2, 9)
        q = "下面哪一個算式和 %d × %d × %d 的答案一樣？" % (a, b, c)
        ans = "%d ×（%d × %d）" % (a, b, c)
        w = ["%d ×（%d ＋ %d）" % (a, b, c), "%d × %d ＋ %d" % (a, b, c), "%d ＋ %d × %d" % (a, b, c)]
        return mcq(q, ans, w, "乘法可以換順序、換組合（交換律、結合律），答案不變。")

    def swap():
        k = R.choice(["sub", "div", "add", "mul"])
        a, b = R.randint(20, 90), R.randint(2, 9)
        if k == "sub":
            q = "%d － %d 和 %d － %d 一樣嗎？" % (a, b, b, a)
            return mcq(q, "不一樣，減法不能交換", ["一樣，可以交換", "不一樣，加法也不能交換", "要算了才知道，有時一樣"], "減法交換後答案不同（%d － %d ＝ %d，%d － %d 不夠減）。" % (a, b, a - b, b, a))
        if k == "div":
            q = "%d ÷ %d 和 %d ÷ %d 一樣嗎？" % (a * b, b, b, a * b)
            return mcq(q, "不一樣，除法不能交換", ["一樣，可以交換", "不一樣，乘法也不能交換", "要算了才知道，有時一樣"], "除法交換後答案不同。")
        if k == "add":
            q = "%d ＋ %d 和 %d ＋ %d 一樣嗎？" % (a, b, b, a)
            return mcq(q, "一樣，加法可以交換", ["不一樣，加法不能交換", "不一樣，大的要放前面", "要算了才知道，有時不一樣"], "加法交換律：%d ＋ %d ＝ %d ＋ %d。" % (a, b, b, a))
        q = "%d × %d 和 %d × %d 一樣嗎？" % (a, b, b, a)
        return mcq(q, "一樣，乘法可以交換", ["不一樣，乘法不能交換", "不一樣，大的要放前面", "要算了才知道，有時不一樣"], "乘法交換律：%d × %d ＝ %d × %d。" % (a, b, b, a))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, swap, 8, seen)


def s2(seen):
    def subsub():
        a = R.randint(200, 900)
        b = R.randint(11, 99)
        c = R.choice([x for x in range(11, 99) if (b + x) % 10 == 0 or (b + x) % 50 == 0] or [100 - b])
        if b + c >= a:
            return None
        q = "%d － %d － %d 可以怎麼算比較快？" % (a, b, c)
        ans = "%d －（%d ＋ %d）＝ %s" % (a, b, c, num(a - b - c))
        w = ["%d －（%d － %d）＝ %s" % (a, max(b, c), min(b, c), num(a - abs(b - c))), "%d － %d ＋ %d ＝ %s" % (a, b, c, num(a - b + c)), "（%d － %d）× %d" % (a, b, c)]
        return mcq(q, ans, w, "連續減兩個數，等於減去它們的和：%d ＋ %d ＝ %d，%d － %d ＝ %s。" % (b, c, b + c, a, b + c, num(a - b - c)))

    def addsub():
        a, b = R.randint(100, 500), R.randint(11, 99)
        c = a % 100 + R.choice([0, 100]) if a % 100 else 100
        if c >= a or c == 0:
            return None
        q = "%d ＋ %d － %d 可以怎麼算比較快？" % (a, b, c)
        v = a + b - c
        ans = "%d － %d ＋ %d ＝ %s" % (a, c, b, num(v))
        w = ["%d －（%d ＋ %d）＝ %s" % (a, c, b, num(a - c - b)) if a - c - b > 0 else "%d ＋（%d ＋ %d）＝ %s" % (a, b, c, num(a + b + c)), "%d ＋（%d ＋ %d）＝ %s" % (a, b, c, num(a + b + c)), "%d － %d － %d ＝ %s" % (a, c, b, num(a - c - b)) if a - c - b > 0 else "%d ＋ %d ＋ %d ＝ %s" % (a, c, b, num(a + c + b))]
        return mcq(q, ans, w, "加減混合可以換順序（數字帶著前面的符號一起移動）：先算 %d － %d ＝ %d，再 ＋ %d ＝ %s。" % (a, c, a - c, b, num(v)))
    return pick_unique(R, subsub, 10, seen) + pick_unique(R, addsub, 10, seen)


def s3(seen):
    def divdiv():
        b, c = R.randint(2, 9), R.randint(2, 9)
        a = b * c * R.randint(3, 30)
        q = "%d ÷ %d ÷ %d 和下面哪一個算式答案一樣？" % (a, b, c)
        ans = "%d ÷（%d × %d）" % (a, b, c)
        w = ["%d ÷（%d ÷ %d）" % (a, b, c) if b % c == 0 else "%d ÷（%d ＋ %d）" % (a, b, c), "%d × %d ÷ %d" % (a, b, c), "%d ÷ %d × %d" % (a, b, c)]
        return mcq(q, ans, w, "連續除以兩個數，等於除以它們的積：%d ÷ %d ＝ %d。" % (a, b * c, a // (b * c)))

    def muldiv():
        a, c = R.randint(2, 30), R.randint(2, 9)
        a = a * c
        b = R.randint(2, 15)
        q = "%d × %d ÷ %d 可以怎麼算比較快？" % (a, b, c)
        v = a * b // c
        ans = "%d ÷ %d × %d ＝ %s" % (a, c, b, num(v))
        w = ["%d ÷（%d × %d）" % (a, c, b), "%d ×（%d ÷ %d）" % (a, c, b) if c % b == 0 else "%d × %d × %d" % (a, b, c), "%d ÷ %d ÷ %d" % (a, c, b)]
        return mcq(q, ans, w, "乘除混合可以換順序：先算 %d ÷ %d ＝ %d，再 × %d ＝ %s。" % (a, c, a // c, b, num(v)))
    return pick_unique(R, divdiv, 10, seen) + pick_unique(R, muldiv, 10, seen)


def s4(seen):
    PAIRS = [(25, 4, 100), (125, 8, 1000), (50, 2, 100), (20, 5, 100), (250, 4, 1000), (125, 4, 500), (25, 8, 200)]

    def mk():
        a, b, p = R.choice(PAIRS)
        x = R.randint(3, 99)
        if x in (a, b):
            return None
        order = R.choice([(a, x, b), (x, a, b), (a, b, x)])
        q = "用簡便的方法算：%d × %d × %d ＝" % order
        v = a * b * x
        return mcq(q, num(v), [num(v * 10), num(v // 10) if v % 10 == 0 else num(v + p), num(p + x), num(v + p)],
                   "先算 %d × %d ＝ %d，再算 %d × %d ＝ %s。" % (a, b, p, p, x, num(v)))

    def sum10():
        a, b = R.randint(11, 89), R.randint(11, 89)
        c = (100 - a % 100) % 100
        if c < 11:
            return None
        q = "用簡便的方法算：%d ＋ %d ＋ %d ＝" % (a, b, c)
        v = a + b + c
        return mcq(q, num(v), [num(v + 10), num(v - 10), num(v + 100), num(a + b - c) if a + b > c else num(v + 1)], "先算 %d ＋ %d ＝ %d，再加 %d：%s。" % (a, c, a + c, b, num(v)))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, sum10, 8, seen)


def s5(seen):
    def shop():
        who = NM.next()
        a, b, c = R.randint(200, 900), R.randint(20, 99), R.randint(20, 99)
        q = "%s有 %d 元，先買了 %d 元的書，又買了 %d 元的筆。用哪一個算式算剩下的錢最簡便？" % (who, a, b, c)
        ans = "%d －（%d ＋ %d）" % (a, b, c)
        return mcq(q, ans, ["%d －（%d － %d）" % (a, max(b, c), min(b, c)), "%d ＋ %d － %d" % (a, b, c), "（%d － %d）× %d" % (a, b, c)],
                   "兩次花的錢先加起來，再從 %d 元裡減：%d －（%d ＋ %d）＝ %s（元）。" % (a, a, b, c, num(a - b - c)))

    def boxes():
        n, b, c = R.randint(2, 9), R.randint(2, 6), R.randint(2, 5)
        t = n * b * c * R.randint(2, 5)
        q = "%d 顆糖果平分給 %d 班，每班再平分給 %d 組。用哪一個算式算每組幾顆？" % (t, b, c)
        return mcq(q, "%d ÷（%d × %d）" % (t, b, c), ["%d ÷（%d ＋ %d）" % (t, b, c), "%d ÷ %d × %d" % (t, b, c), "%d × %d ÷ %d" % (t, b, c)],
                   "平分兩次，等於除以 %d × %d ＝ %d：%d ÷ %d ＝ %d（顆）。" % (b, c, b * c, t, b * c, t // (b * c)))

    def total():
        p, n = R.choice([(25, 4), (25, 8), (125, 8), (50, 2), (20, 5)])
        k = R.randint(3, 12)
        q = "每盒 %d 元，一次買 %d 盒，買了 %d 次，一共多少元？" % (p, n, k)
        v = p * n * k
        return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in (p * n + k, p + n + k, v * 10, p * k)], "%d × %d × %d ＝（%d × %d）× %d ＝ %d × %d ＝ %s（元）。" % (p, n, k, p, n, k, p * n, k, num(v)))
    return pick_unique(R, shop, 7, seen) + pick_unique(R, boxes, 7, seen) + pick_unique(R, total, 6, seen)


def main():
    seen = set()
    sets = [("交換律和結合律", s1(seen)), ("加減混合的規律", s2(seen)), ("乘除混合的規律", s3(seen)),
            ("簡便計算", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["加法和乘法可以<b>換順序</b>、<b>換組合</b>，答案不變。減法和除法不能交換。",
         "<b>連減</b>：a － b － c ＝ a －（b ＋ c）。<b>連除</b>：a ÷ b ÷ c ＝ a ÷（b × c）。",
         "加減混合、乘除混合可以換順序，數字要帶著前面的符號一起移動：250 ＋ 37 － 50 ＝ 250 － 50 ＋ 37。",
         "記住好算的組合：25 × 4 ＝ 100，125 × 8 ＝ 1000。"],
        [example("486 － 57 － 43 ＝", ["57 ＋ 43 ＝ 100。", "486 － 100 ＝ 386。"], "386"),
         example("25 × 37 × 4 ＝", ["先算 25 × 4 ＝ 100。", "100 × 37 ＝ 3700。"], "3700")],
        [("486 － 57 － 43 ＝ 486 －（57 － 43）", "連減要把減數加起來：486 －（57 ＋ 43）"),
         ("720 ÷ 8 ÷ 2 ＝ 720 ÷（8 ÷ 2）", "連除要把除數乘起來：720 ÷（8 × 2）"),
         ("換順序時把減號丟掉", "數字要帶著前面的符號一起移動")])
    faq = [{"q": "四年級的計算規律要學什麼？",
            "a": "108課綱 R-4-2：兩步驟的計算規則，包括加減混合、乘除混合，以及在四則混合計算中運用交換律、結合律等運算性質。"},
           {"q": "為什麼 a － b － c ＝ a －（b ＋ c）？",
            "a": "先拿走 b 再拿走 c，和一次拿走 b ＋ c 是一樣的。例如 100 元先花 30 元、再花 20 元，等於一次花 50 元。"},
           {"q": "簡便計算有什麼用？",
            "a": "湊成整十、整百或 100、1000 再算，可以算得又快又不容易錯，例如 25 × 4 ＝ 100、125 × 8 ＝ 1000。"}]
    make_unit(R, "grade-4", "calculation-rules", "R-4-2",
              "四則計算規律（I）：兩步驟計算規則。加減混合計算、乘除混合計算。在四則混合計算中運用數的運算性質。",
              "四則計算規律：交換律、結合律與簡便計算",
              "四年級數學 計算規律 練習題｜交換律・結合律・連減連除・簡便計算 學習單（附解答）",
              "計算規律與簡便計算",
              "國小四年級數學「四則計算規律」免費學習單：加法和乘法的交換律、結合律，連減和連除，加減混合、乘除混合換順序和簡便計算。100題線上練習馬上對答案，附可列印解答。",
              "連減：減數先加起來；連除：除數先乘起來",
              "加法、乘法可以換順序；數字帶著符號一起移動。",
              body, faq, sets, 21)


if __name__ == "__main__":
    main()
