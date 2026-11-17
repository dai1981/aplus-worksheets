# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：三數加減與兩步驟問題（108課綱 N-2-9、R-2-2）
  python3 tools/gen_tw_math_g2_two_step_problems.py
三數の加減（由左往右、湊十・湊百で工夫）、加減兩步驟、乘法と加減の兩步驟（分步列式、併式は使わない）、文章題。
誤答：途中の答えを最後の答えにする、順序を無視して右から計算する、乘法を加法にする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets

R = random.Random(81310)
NM = Names(R)


def s1(seen):
    def mk():
        a, b, c = R.randint(10, 300), R.randint(10, 300), R.randint(10, 300)
        ops = R.choice([("＋", "＋"), ("＋", "－"), ("－", "＋"), ("－", "－")])
        m = a + b if ops[0] == "＋" else a - b
        v = m + c if ops[1] == "＋" else m - c
        if m < 0 or v < 0 or v > 999 or m > 999:
            return None
        q = "%d %s %d %s %d ＝ ？" % (a, ops[0], b, ops[1], c)
        right = (b + c if ops[1] == "＋" else b - c)
        wrong_rtl = a + right if ops[0] == "＋" else a - right
        w = [m, wrong_rtl if wrong_rtl != v and wrong_rtl >= 0 else v + 10, v + 10, v - 10 if v > 10 else v + 1]
        return mcq(q, str(v), [str(x) for x in w if x != v][:3], "由左往右算：%d %s %d ＝ %d，%d %s %d ＝ %d。" % (a, ops[0], b, m, m, ops[1], c, v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a = R.randint(10, 90)
        b = R.choice([x for x in range(10, 99) if (a + x) % 10 == 0])
        c = R.randint(10, 400)
        if a + b + c > 999:
            return None
        q = "用簡單的方法算：%d ＋ %d ＋ %d" % (a, c, b)
        v = a + b + c
        return mcq(q, str(v), [str(v + 10), str(v - 10), str(a + c)], "先把 %d 和 %d 湊成 %d，再加 %d：%d。" % (a, b, a + b, c, v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b, c = R.randint(20, 300), R.randint(10, 200), R.randint(10, 200)
        who = NM.next()
        k = R.choice(["buy_spend", "bus", "two_add"])
        if k == "buy_spend":
            if a + b - c <= 0:
                return None
            q = "%s有 %d 元，媽媽又給 %d 元，買文具花了 %d 元。還剩多少元？" % (who, a, b, c)
            v, mid = a + b - c, a + b
            e = "先算有多少：%d ＋ %d ＝ %d；再算剩多少：%d － %d ＝ %d。" % (a, b, mid, mid, c, v)
        elif k == "bus":
            a2, b2, c2 = a % 60 + 20, b % 20 + 3, c % 20 + 3
            q = "公車上有 %d 人，到站下車 %d 人，又上車 %d 人。現在車上有幾人？" % (a2, b2, c2)
            v, mid = a2 - b2 + c2, a2 - b2
            e = "%d － %d ＝ %d，%d ＋ %d ＝ %d。" % (a2, b2, mid, mid, c2, v)
        else:
            q = "學校種了 %d 棵樹，第一天澆了 %d 棵，第二天澆了 %d 棵。還有幾棵沒澆？" % (a + b + c, a, b)
            v, mid = c, a + b
            e = "已經澆了 %d ＋ %d ＝ %d 棵，%d － %d ＝ %d。" % (a, b, mid, a + b + c, mid, v)
        return mcq(q, str(v), [str(x) for x in (mid, v + 10, v - 10 if v > 10 else v + 1) if x != v] + [str(v + 1)], e)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, n = R.randint(2, 9), R.randint(2, 9)
        c = R.randint(5, 60)
        who = NM.next()
        k = R.choice(["add", "sub", "pay"])
        p = a * n
        if k == "add":
            q = "%s買了 %d 盒彩色筆，每盒 %d 枝，原來還有 %d 枝。現在一共有幾枝？" % (who, n, a, c)
            v = p + c
            e = "先算買的：%d × %d ＝ %d；再加原來的：%d ＋ %d ＝ %d。" % (a, n, p, p, c, v)
        elif k == "sub":
            if c >= p:
                return None
            q = "有 %d 盤餅乾，每盤 %d 塊，吃掉了 %d 塊。還剩幾塊？" % (n, a, c)
            v = p - c
            e = "先算一共：%d × %d ＝ %d；再減吃掉的：%d － %d ＝ %d。" % (a, n, p, p, c, v)
        else:
            money = R.choice([50, 100])
            if p >= money:
                return None
            q = "一枝鉛筆 %d 元，%s買了 %d 枝，付了 %d 元，要找回多少元？" % (a, who, n, money)
            v = money - p
            e = "先算價錢：%d × %d ＝ %d；再算找錢：%d － %d ＝ %d。" % (a, n, p, money, p, v)
        return mcq(q, str(v), [str(x) for x in (p, a + n + c, v + a) if x != v] + [str(v + 1)], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        a, n, m = R.randint(2, 9), R.randint(2, 9), R.randint(2, 9)
        x, y = NM.next(), NM.next()
        k = R.choice(["two_mul", "times_more"])
        if k == "two_mul":
            q = "一隻雞 2 隻腳，一隻兔子 4 隻腳。籠子裡有 %d 隻雞和 %d 隻兔子，一共有幾隻腳？" % (n, m)
            v = 2 * n + 4 * m
            e = "雞 2 × %d ＝ %d，兔子 4 × %d ＝ %d，%d ＋ %d ＝ %d。" % (n, 2 * n, m, 4 * m, 2 * n, 4 * m, v)
            w = [2 * n, 4 * m, (n + m) * 4]
        else:
            q = "%s有 %d 張卡片，%s的卡片是%s的 %d 倍。兩人一共有幾張？" % (x, a, y, x, n)
            v = a + a * n
            e = "%s有 %d × %d ＝ %d 張，一共 %d ＋ %d ＝ %d 張。" % (y, a, n, a * n, a, a * n, v)
            w = [a * n, a + n, a * n * 2]
        return mcq(q, str(v), [str(t) for t in w if t != v] + [str(v + 2)], e)
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("三數加減", s1(seen)), ("湊十、湊百的簡單算法", s2(seen)), ("加減兩步驟問題", s3(seen)),
            ("乘法和加減的兩步驟", s4(seen)), ("挑戰：兩步驟問題", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["三個數加減，<b>由左往右</b>算：45 － 18 ＋ 30 ＝ 27 ＋ 30 ＝ 57。",
         "只有加法時，可以先把能湊成整十、整百的加起來：36 ＋ 85 ＋ 64 ＝ 100 ＋ 85 ＝ 185。",
         "<b>兩步驟問題</b>：先算第一步、寫下來，再用它算第二步。不要把第一步的答案當最後答案。"],
        [example("有 50 元，又得到 30 元，花了 45 元", ["50 ＋ 30 ＝ 80。", "80 － 45 ＝ 35。"], "剩 35 元"),
         example("3 盒、每盒 6 個，原來有 5 個", ["6 × 3 ＝ 18。", "18 ＋ 5 ＝ 23。"], "23 個")],
        [("45 － 18 ＋ 30，先算 18 ＋ 30", "由左往右：先算 45 － 18"),
         ("算出第一步就停下來", "要看題目最後問什麼"),
         ("3 盒每盒 6 個寫成 6 ＋ 3", "一樣多的幾份用乘法：6 × 3")])
    faq = [{"q": "二年級的兩步驟問題要用併式嗎？",
            "a": "108課綱 N-2-9：二年級的兩步驟問題（加、減、乘）分步列式就好，不要求併式；三年級才學併式和括號。"},
           {"q": "三個數相加為什麼可以換順序？",
            "a": "只有加法時，換順序或先加哪兩個，答案都一樣（加法交換律、結合律），所以可以先湊整十、整百。"},
           {"q": "孩子兩步驟題常錯怎麼辦？",
            "a": "請孩子先說「要先知道什麼」，把第一步的結果寫在旁邊，再算題目真正要問的。"}]
    make_unit(R, "grade-2", "two-step-problems", "N-2-9",
              "解題：兩步驟應用問題（加、減、乘）。加減混合、加與乘、減與乘之應用解題。不含併式。不含連乘。",
              "三數加減與兩步驟問題",
              "二年級數學 兩步驟問題 練習題｜三數加減・加減乘應用題 學習單（附解答）",
              "兩步驟問題",
              "國小二年級數學「三數加減與兩步驟問題」免費學習單：三數加減由左往右、湊十湊百的簡單算法、加減兩步驟問題、乘法和加減的兩步驟問題。100題線上練習，附可列印解答。",
              "先算第一步，再算第二步",
              "三數加減由左往右；只有加法可以先湊整十、整百。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
