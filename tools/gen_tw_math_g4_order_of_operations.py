# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：兩步驟問題併式與四則混合計算（108課綱 R-4-1）
  python3 tools/gen_tw_math_g4_order_of_operations.py
由左往右算、先乘除後加減、括號先算、文章題を併式で書く・解く（逐次減項を含む）。
誤答：左から順に計算して乘除を後回しにしない、括號を無視、a−b−c を a−(b−c) とする。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(41020)
NM = Names(R)


def s1(seen):
    def mk():
        kind = R.choice(["as", "md"])
        if kind == "as":
            a, b, c = R.randint(30, 200), R.randint(5, 60), R.randint(5, 60)
            if R.random() < .5:
                if a - b <= 0:
                    return None
                v = a - b + c
                w = a - (b + c)
                q = "%d － %d ＋ %d ＝" % (a, b, c)
            else:
                if a - b - c <= 0:
                    return None
                v = a - b - c
                w = a - (b - c) if b > c else a - b + c
                q = "%d － %d － %d ＝" % (a, b, c)
            return mcq(q, num(v), [num(x) for x in (w, v + 10, v - 10 if v > 10 else v + 20, a + b + c) if x != v and x > 0],
                       "只有加減，<b>由左往右</b>算：%s ＝ %s。" % (q.rstrip(" ＝"), num(v)))
        b, c = R.randint(2, 9), R.randint(2, 9)
        a = b * c * R.randint(2, 12)
        if R.random() < .5:
            v = a // b * c
            w = a // (b * c)
            q = "%d ÷ %d × %d ＝" % (a, b, c)
        else:
            v = a // b // c
            w = a // (b // c) if b % c == 0 and b // c else a * c // b if (a * c) % b == 0 else v + c
            q = "%d ÷ %d ÷ %d ＝" % (a, b, c)
        return mcq(q, num(v), [num(x) for x in (w, v + 1, v * 2, v + c) if x != v and x > 0], "只有乘除，<b>由左往右</b>算：%s ＝ %s。" % (q.rstrip(" ＝"), num(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        k = R.choice(["a+bc", "a-bc", "ab+c", "a+b/c", "ab-cd"])
        a, b, c, d = R.randint(5, 60), R.randint(2, 9), R.randint(2, 12), R.randint(2, 9)
        if k == "a+bc":
            q, v, w = "%d ＋ %d × %d ＝" % (a, b, c), a + b * c, (a + b) * c
            st = "先算 %d × %d ＝ %d，再算 %d ＋ %d ＝ %d" % (b, c, b * c, a, b * c, v)
        elif k == "a-bc":
            a = R.randint(b * c + 1, b * c + 80)
            q, v, w = "%d － %d × %d ＝" % (a, b, c), a - b * c, (a - b) * c
            st = "先算 %d × %d ＝ %d，再算 %d － %d ＝ %d" % (b, c, b * c, a, b * c, v)
        elif k == "ab+c":
            q, v, w = "%d × %d ＋ %d ＝" % (b, c, a), b * c + a, b * (c + a)
            st = "先算 %d × %d ＝ %d，再算 %d ＋ %d ＝ %d" % (b, c, b * c, b * c, a, v)
        elif k == "a+b/c":
            bb = b * c
            q, v, w = "%d ＋ %d ÷ %d ＝" % (a, bb, b), a + c, (a + bb) // b if (a + bb) % b == 0 else a + bb + b
            st = "先算 %d ÷ %d ＝ %d，再算 %d ＋ %d ＝ %d" % (bb, b, c, a, c, v)
        else:
            q, v, w = "%d × %d － %d × %d ＝" % (a, b, c, d), a * b - c * d, (a * b - c) * d
            st = "先算兩個乘法：%d 和 %d，再算 %d － %d ＝ %d" % (a * b, c * d, a * b, c * d, v)
            if v <= 0 or w <= 0:
                return None
        return mcq(q, num(v), [num(x) for x in (w, v + b, v - 1, v + 10) if x != v and x > 0], "<b>先乘除，後加減</b>：%s。" % st)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = R.choice(["(a+b)c", "(a-b)c", "a(b+c)", "a/(b+c)", "(a+b)/c", "a-(b+c)"])
        a, b, c = R.randint(3, 40), R.randint(2, 30), R.randint(2, 9)
        if k == "(a+b)c":
            q, v, w = "（%d ＋ %d）× %d ＝" % (a, b, c), (a + b) * c, a + b * c
        elif k == "(a-b)c":
            if a <= b:
                return None
            q, v, w = "（%d － %d）× %d ＝" % (a, b, c), (a - b) * c, a - b * c if a - b * c > 0 else a * c - b
        elif k == "a(b+c)":
            q, v, w = "%d ×（%d ＋ %d）＝" % (c, a, b), c * (a + b), c * a + b
        elif k == "a/(b+c)":
            s_ = R.randint(2, 9)
            b1 = R.randint(1, s_ - 1)
            c1 = s_ - b1
            a1 = s_ * R.randint(3, 20)
            q, v, w = "%d ÷（%d ＋ %d）＝" % (a1, b1, c1), a1 // s_, a1 // b1 + c1 if a1 % b1 == 0 else a1 // s_ + 1
        elif k == "(a+b)/c":
            t = c * R.randint(3, 20)
            a1 = R.randint(1, t - 1)
            q, v, w = "（%d ＋ %d）÷ %d ＝" % (a1, t - a1, c), t // c, a1 + (t - a1) // c if (t - a1) % c == 0 else t // c + 2
        else:
            a = R.randint(60, 300)
            b, c = R.randint(5, 40), R.randint(5, 40)
            q, v, w = "%d －（%d ＋ %d）＝" % (a, b, c), a - b - c, a - b + c
        return mcq(q, num(v), [num(x) for x in (w, v + c, v - 1 if v > 1 else v + 2, v * 2) if x != v and x > 0], "<b>括號裡先算</b>，再算括號外面：答案是 %s。" % num(v))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        k = R.choice(["buy", "share", "left", "two"])
        who = NM.next()
        if k == "buy":
            p, n, m = R.randint(15, 60), R.randint(2, 9), R.choice([500, 1000])
            q = "%s帶 %d 元，買了 %d 盒 %d 元的牛奶，還剩多少元？哪一個併式正確？" % (who, m, n, p)
            ans = "%d － %d × %d" % (m, p, n)
            w = ["（%d － %d）× %d" % (m, p, n), "%d × %d － %d" % (m, n, p), "%d － %d ＋ %d" % (m, p, n)]
        elif k == "share":
            a, b, c = R.randint(20, 60), R.randint(10, 40), R.randint(3, 9)
            q = "%s有 %d 張貼紙，又買了 %d 張，全部平分給 %d 人。哪一個併式正確？" % (who, a, b, c)
            ans = "（%d ＋ %d）÷ %d" % (a, b, c)
            w = ["%d ＋ %d ÷ %d" % (a, b, c), "%d ÷ %d ＋ %d" % (a, c, b), "（%d ＋ %d）× %d" % (a, b, c)]
        elif k == "left":
            a, b, c = R.randint(200, 500), R.randint(20, 90), R.randint(20, 90)
            q = "書有 %d 頁，%s第一天看了 %d 頁，第二天看了 %d 頁，還剩幾頁？哪一個併式正確？" % (a, who, b, c)
            ans = "%d －（%d ＋ %d）" % (a, b, c)
            w = ["%d －（%d － %d）" % (a, b, c), "%d － %d ＋ %d" % (a, b, c), "%d ＋ %d － %d" % (a, b, c)]
        else:
            p1, n1, p2, n2 = R.randint(10, 40), R.randint(2, 6), R.randint(10, 40), R.randint(2, 6)
            q = "買 %d 枝 %d 元的筆和 %d 本 %d 元的筆記本，一共多少元？哪一個併式正確？" % (n1, p1, n2, p2)
            ans = "%d × %d ＋ %d × %d" % (p1, n1, p2, n2)
            w = ["（%d ＋ %d）×（%d ＋ %d）" % (p1, p2, n1, n2), "%d × %d ＋ %d ＋ %d" % (p1, n1, p2, n2), "（%d × %d ＋ %d）× %d" % (p1, n1, p2, n2)]
        return mcq(q, ans, w, "先想第一步要算什麼，需要先算的部分用括號或乘除，寫成一個算式：%s。" % ans)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        k = R.choice(["buy", "share", "left", "group"])
        who = NM.next()
        if k == "buy":
            p, n = R.randint(15, 60), R.randint(2, 9)
            m = R.choice([500, 1000])
            v = m - p * n
            q = "%s帶 %d 元，買了 %d 個 %d 元的麵包，還剩多少元？" % (who, m, n, p)
            e = "%d － %d × %d ＝ %d － %d ＝ %d（元）" % (m, p, n, m, p * n, v)
            w = [(m - p) * n, m - p - n, v + p]
        elif k == "share":
            c = R.randint(3, 9)
            t = c * R.randint(8, 30)
            a = R.randint(5, t - 5)
            b = t - a
            v = t // c
            q = "%s有 %d 顆彈珠，又贏了 %d 顆，全部平分給 %d 個朋友，每人幾顆？" % (who, a, b, c)
            e = "（%d ＋ %d）÷ %d ＝ %d ÷ %d ＝ %d（顆）" % (a, b, c, t, c, v)
            w = [a + b // c if b % c == 0 else v + 2, t, v + 1]
        elif k == "left":
            a, b, c = R.randint(200, 500), R.randint(20, 90), R.randint(20, 90)
            v = a - b - c
            q = "一捆緞帶長 %d 公分，剪下 %d 公分和 %d 公分各一段，還剩幾公分？" % (a, b, c)
            e = "%d － %d － %d ＝ %d －（%d ＋ %d）＝ %d（公分）" % (a, b, c, a, b, c, v)
            w = [a - b + c, a - abs(b - c), v + 10]
        else:
            g, per, extra = R.randint(3, 9), R.randint(4, 9), R.randint(1, 9)
            v = g * per + extra
            q = "全班分成 %d 組，每組 %d 人，還有 %d 人當小老師。全班有幾人？" % (g, per, extra)
            e = "%d × %d ＋ %d ＝ %d（人）" % (g, per, extra, v)
            w = [g * (per + extra), g + per + extra, v - extra]
        return mcq(q, num(v), [num(x) for x in w if x != v and x > 0] + [num(v + 2)], "列成併式：%s。" % e)
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("由左往右算", s1(seen)), ("先乘除後加減", s2(seen)), ("括號先算", s3(seen)),
            ("列出併式", s4(seen)), ("用併式解題", s5(seen))]
    body = lesson(
        ["把兩步驟的算式寫成一個式子，叫做<b>併式</b>。",
         "計算的約定：① <b>括號先算</b>；② <b>先乘除，後加減</b>；③ 同一級的由<b>左往右</b>算。",
         "連續減兩個數，可以先把要減的加起來：100 － 25 － 35 ＝ 100 －（25 ＋ 35）。"],
        [example("50 － 6 × 4 ＝", ["先乘：6 × 4 ＝ 24。", "再減：50 － 24 ＝ 26。"], "26"),
         example("帶 500 元，買 3 盒 85 元的餅乾，剩多少元？", ["併式：500 － 85 × 3。", "＝ 500 － 255 ＝ 245。"], "245 元")],
        [("50 － 6 × 4 先算 50 － 6", "先乘除，後加減：先算 6 × 4"),
         ("（12 ＋ 8）× 3 算成 12 ＋ 24", "括號裡的要先算：20 × 3 ＝ 60"),
         ("100 － 25 － 35 ＝ 100 －（25 － 35）", "連減時是把減數加起來：100 －（25 ＋ 35）")])
    faq = [{"q": "四則混合計算的順序是什麼？",
            "a": "括號先算；沒有括號時先乘除、後加減；同一級的運算由左往右算。"},
           {"q": "什麼是併式？",
            "a": "把兩步驟的算式合寫成一個算式，例如先乘再減寫成 500 － 85 × 3。108課綱 R-4-1 說明併式是學代數的重要基礎。"},
           {"q": "孩子寫併式時括號常常漏掉，怎麼辦？",
            "a": "請孩子先說出「第一步要算什麼」，如果第一步是加減、後面要乘除，就一定要用括號把第一步括起來。"}]
    make_unit(R, "grade-4", "order-of-operations", "R-4-1",
              "兩步驟問題併式：併式是代數學習的重要基礎。含四則混合計算的約定（由左往右算、先乘除後加減、括號先算）。學習逐次減項計算。",
              "併式與四則混合計算",
              "四年級數學 四則運算 練習題｜先乘除後加減・括號先算・併式 學習單（附解答）",
              "併式與四則運算",
              "國小四年級數學「併式與四則混合計算」免費學習單：由左往右算、先乘除後加減、括號先算、列出併式和用併式解應用題。100題線上練習馬上對答案，附可列印解答。",
              "括號先算，先乘除後加減",
              "同一級的運算由左往右算。",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
