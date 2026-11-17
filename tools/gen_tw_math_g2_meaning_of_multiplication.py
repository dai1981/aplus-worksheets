# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：認識乘法（108課綱 N-2-6）
  python3 tools/gen_tw_math_g2_meaning_of_multiplication.py
同じ數ずつ（幾個一數）、累加と乘法の式（3 ＋ 3 ＋ 3 ＋ 3 ＝ 3 × 4）、排列（幾排每排幾個）、「倍」（5 的 3 倍）、乘法の式を選ぶ、文章題。
誤答：被乘數と乘數を逆に読む（每盤 3 個、4 盤 → 4 × 3 でも答えは同じだが意味を確認）、足し算と取り違える（3 ＋ 4）。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81307)
NM = Names(R)


def s1(seen):
    def mk():
        a, n = R.randint(2, 5), R.randint(2, 5)
        k = R.choice(P.KINDS)
        q = "每一堆有 %d %s，有 %d 堆。一共有幾%s？" % (a, P.cl(k), n, P.cl(k)) + P.circles([a] * n, k)
        return mcq(q, "%d %s" % (a * n, P.cl(k)), ["%d %s" % (x, P.cl(k)) for x in (a + n, a * n + a, a * n - 1)], "%d 個 %d：%s ＝ %d × %d ＝ %d。" % (n, a, " ＋ ".join([str(a)] * n), a, n, a * n))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, n = R.randint(2, 9), R.randint(2, 6)
        k = R.choice(["to_mul", "to_add"])
        if k == "to_mul":
            q = "%s 可以寫成哪一個乘法算式？" % " ＋ ".join([str(a)] * n)
            return mcq(q, "%d × %d" % (a, n), ["%d ＋ %d" % (a, n), "%d × %d" % (a, a) if a != n else "%d × %d" % (a, n + 1), "%d × %d" % (n, n) if a != n else "%d × %d" % (a + 1, n)], "%d 加了 %d 次，就是 %d × %d。" % (a, n, a, n))
        q = "%d × %d 的意思是？" % (a, n)
        return mcq(q, "%d 個 %d 加起來" % (n, a), ["%d 加 %d" % (a, n), "%d 個 %d 加起來" % (a, a) if a != n else "%d 個 %d 加起來" % (n + 1, a), "%d 減 %d" % (max(a, n), min(a, n))], "%d × %d 表示 %d 個 %d：%s。" % (a, n, n, a, " ＋ ".join([str(a)] * n)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        r, c = R.randint(2, 5), R.randint(2, 6)
        k = R.choice(P.KINDS)
        q = "排成 %d 排，每排 %d %s。一共有幾%s？" % (r, c, P.cl(k), P.cl(k)) + P.array(r, c, k)
        return mcq(q, "%d %s" % (r * c, P.cl(k)), ["%d %s" % (x, P.cl(k)) for x in (r + c, r * c + c, r * c - r)], "每排 %d 個，%d 排：%d × %d ＝ %d。" % (c, r, c, r, r * c))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, n = R.randint(2, 9), R.randint(2, 9)
        k = R.choice(["times", "rev"])
        if k == "times":
            q = "%d 的 %d 倍是多少？" % (a, n)
            return mcq(q, str(a * n), [str(a + n), str(a * n + a), str(a * n - a)], "%d 的 %d 倍就是 %d 個 %d：%d × %d ＝ %d。" % (a, n, n, a, a, n, a * n))
        x, y = NM.next(), NM.next()
        q = "%s有 %d 張貼紙，%s的貼紙是%s的 %d 倍。%s有幾張？" % (x, a, y, x, n, y)
        return mcq(q, "%d 張" % (a * n), ["%d 張" % v for v in (a + n, a * n + a, a * n - 1)], "%d 的 %d 倍：%d × %d ＝ %d。" % (a, n, a, n, a * n))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        a, n = R.randint(2, 9), R.randint(2, 9)
        who = NM.next()
        t = R.choice([("一盒蛋糕有 %d 個，%s買了 %d 盒", "個"), ("一輛車有 %d 個輪子，停車場有 %d 輛這樣的車", "個"), ("一包糖有 %d 顆，%s買了 %d 包", "顆"),
                      ("每個花瓶插 %d 朵花，有 %d 個花瓶", "朵"), ("一隻螃蟹有 %d 隻腳……一盤有 %d 隻螃蟹", "隻")])
        if "螃蟹" in t[0]:
            a = 10
            txt = "一隻螃蟹有 10 隻腳，一盤有 %d 隻螃蟹" % n
            unit = "隻腳"
        elif "輪子" in t[0]:
            a = 4
            txt = t[0] % (a, n)
            unit = "個輪子"
        else:
            txt = t[0] % ((a, who, n) if "%s" in t[0] else (a, n))
            unit = t[1]
        q = "%s。一共有幾%s？哪一個算式對？" % (txt, unit)
        return mcq(q, "%d × %d ＝ %d" % (a, n, a * n), ["%d ＋ %d ＝ %d" % (a, n, a + n), "%d × %d ＝ %d" % (a, n, a * n + a), "%d － %d ＝ %d" % (max(a, n), min(a, n), abs(a - n))], "每份 %d，有 %d 份：%d × %d ＝ %d。" % (a, n, a, n, a * n))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("幾個幾", s1(seen)), ("加法和乘法", s2(seen)), ("排列", s3(seen)),
            ("幾倍", s4(seen)), ("生活中的乘法", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["一樣多的東西有好幾份時，可以用<b>乘法</b>。每盤 3 個、有 4 盤：3 ＋ 3 ＋ 3 ＋ 3 ＝ 3 × 4 ＝ 12。" + P.circles([3, 3, 3, 3], "apple"),
         "3 × 4 讀作「3 乘以 4」，表示 <b>4 個 3</b>。",
         "<b>倍</b>：5 的 3 倍就是 3 個 5，5 × 3 ＝ 15。"],
        [example("每排 6 張椅子，5 排", ["6 × 5。"], "30 張"),
         example("4 的 2 倍", ["4 × 2。"], "8")],
        [("每盤 3 個、4 盤，寫成 3 ＋ 4", "一樣多的有 4 份，用乘法 3 × 4"),
         ("3 × 4 是 3 個 4", "台灣的寫法是「每份 × 份數」：4 個 3"),
         ("5 的 3 倍 ＝ 8", "3 倍是 3 個 5：15")])
    faq = [{"q": "為什麼先教「幾個幾」？",
            "a": "108課綱 N-2-6：先從一樣多的累加理解乘法的意思，再逐步發展「倍」的概念，之後才背九九乘法。"},
           {"q": "3 × 4 和 4 × 3 有什麼不同？",
            "a": "答案一樣是 12。台灣二年級的寫法通常是「每份的數 × 份數」，3 × 4 表示 4 個 3，列式時要說得出意思。"},
           {"q": "怎麼判斷要用乘法？",
            "a": "題目裡有「每盒、每排、每個」一樣多，又問「一共」時，就可以用乘法。"}]
    make_unit(R, "grade-2", "meaning-of-multiplication", "N-2-6",
              "乘法：乘法的意義與應用。在學習乘法過程，逐步發展「倍」的概念，作為統整乘法應用情境的語言。",
              "認識乘法：幾個幾和倍",
              "二年級數學 認識乘法 練習題｜幾個幾・累加・幾倍 學習單（附解答）",
              "認識乘法",
              "國小二年級數學「認識乘法」免費學習單：看圖幾個幾、加法和乘法的關係、排列、幾倍、生活中的乘法。100題線上練習，圖多，附可列印解答。",
              "一樣多的有幾份，用乘法",
              "3 × 4 表示 4 個 3；5 的 3 倍 ＝ 5 × 3。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
