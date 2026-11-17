# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：認識減法（108課綱 N-1-2、N-1-3）
  python3 tools/gen_tw_math_g1_subtraction_meaning.py
絵で劃掉（拿走型）、比較型（多幾個・少幾個）、算式を選ぶ、10 以內の減法、說故事算減法。
誤答：加法の式を選ぶ、拿走した數を答える、差を答えずに大きい數を答える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81203)
NM = Names(R)


def s1(seen):
    def mk():
        a = R.randint(3, 10)
        b = R.randint(1, a - 1)
        k = R.choice(P.KINDS)
        q = "有 %d %s%s，劃掉的被拿走了。還剩幾%s？" % (a, P.cl(k), P.nm(k), P.cl(k)) + P.crossed(a, k, b)
        return mcq(q, "%d %s" % (a - b, P.cl(k)), ["%d %s" % (x, P.cl(k)) for x in (b if b != a - b else a, a + b, a - b + 1)], "%d － %d ＝ %d。" % (a, b, a - b))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.sample(range(1, 10), 2)
        k1, k2 = R.sample(P.KINDS, 2)
        if P.cl(k1) != P.cl(k2):
            return None
        hi, lo = (k1, k2) if a > b else (k2, k1)
        q = "%s比%s多幾%s？" % (P.nm(hi), P.nm(lo), P.cl(k1)) + P.groups([(a, k1), (b, k2)])
        d = abs(a - b)
        return mcq(q, "%d %s" % (d, P.cl(k1)), ["%d %s" % (x, P.cl(k1)) for x in (a + b, max(a, b), d + 1)], "一個對一個排好，多出來的就是答案：%d － %d ＝ %d。" % (max(a, b), min(a, b), d))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a = R.randint(3, 10)
        b = R.randint(1, a - 1)
        k = R.choice(P.KINDS)
        q = "哪一個算式和圖一樣？（劃掉的拿走了）" + P.crossed(a, k, b)
        return mcq(q, "%d － %d ＝ %d" % (a, b, a - b), ["%d ＋ %d ＝ %d" % (a - b, b, a), "%d － %d ＝ %d" % (a, a - b, b) if a - b != b else "%d － %d ＝ %d" % (a, b, a - b + 1), "%d ＋ %d ＝ %d" % (a, b, a + b)], "原來 %d，拿走 %d，剩 %d：%d － %d ＝ %d。" % (a, b, a - b, a, b, a - b))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a = R.randint(1, 10)
        b = R.randint(0, a)
        q = "%d － %d ＝ ？" % (a, b)
        v = a - b
        return mcq(q, str(v), [str(x) for x in (a + b, v + 1, v - 1 if v > 0 else v + 2) if x != v] + [str(v + 3)], ("減 0 數不變。" if b == 0 else "減掉自己是 0。" if a == b else "從 %d 往回數 %d 個：%d。" % (a, b, v)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def take():
        a = R.randint(4, 10)
        b = R.randint(1, a - 1)
        who = NM.next()
        t = R.choice([("%s有 %d 顆糖，吃掉 %d 顆", "顆"), ("%s有 %d 個氣球，飛走 %d 個", "個"), ("%s有 %d 張貼紙，送給同學 %d 張", "張"), ("樹上有 %d 隻鳥，飛走 %d 隻", "隻")])
        txt = t[0] % ((who, a, b) if t[0].startswith("%s") else (a, b))
        q = "%s。還剩幾%s？" % (txt, t[1])
        return mcq(q, "%d %s" % (a - b, t[1]), ["%d %s" % (x, t[1]) for x in (a + b, b if b != a - b else a, a - b + 1)], "%d － %d ＝ %d。" % (a, b, a - b))

    def compare():
        a, b = R.sample(range(2, 11), 2)
        x, y = NM.next(), NM.next()
        q = "%s有 %d 本書，%s有 %d 本書。%s比%s多幾本？" % (x, a, y, b, x if a > b else y, y if a > b else x)
        d = abs(a - b)
        return mcq(q, "%d 本" % d, ["%d 本" % v for v in (a + b, max(a, b), d + 1)], "%d － %d ＝ %d。" % (max(a, b), min(a, b), d))
    return pick_unique(R, take, 12, seen) + pick_unique(R, compare, 8, seen)


def main():
    seen = set()
    sets = [("看圖拿走", s1(seen)), ("比一比多幾個", s2(seen)), ("選算式", s3(seen)),
            ("10 以內的減法", s4(seen)), ("說故事算減法", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>減法</b>：拿走、吃掉、飛走以後還剩多少，或是比一比多幾個、少幾個，用「－」。",
         "5 － 2 ＝ 3，讀作「5 減 2 等於 3」。" + P.crossed(5, "apple", 2),
         "比多少：一個對一個排好，多出來的就是差。"],
        [example("有 7 顆糖，吃掉 3 顆，還剩幾顆？", ["7 － 3。"], "4 顆"),
         example("小明 8 本書，小美 5 本，小明多幾本？", ["8 － 5。"], "3 本")],
        [("吃掉也用加法", "拿走、吃掉、飛走用減法"),
         ("答案寫拿走的數", "要寫「還剩」的數"),
         ("比多少時寫大的數", "要寫兩個數相差多少")])
    faq = [{"q": "減法有哪些題型？",
            "a": "108課綱 N-1-2 有「拿走型」（還剩多少）和「比較型」（多幾個、少幾個），一年級都會學。"},
           {"q": "比較型為什麼也用減法？",
            "a": "把兩堆一個對一個排好，配對後多出來的部分，就是大的數減小的數。"},
           {"q": "孩子分不清加法和減法怎麼辦？",
            "a": "用積木演一演：變多是加，變少或比較差多少是減，再把動作寫成算式。"}]
    make_unit(R, "grade-1", "subtraction-meaning", "N-1-2",
              "加法和減法：加法和減法的意義與應用。含「添加型」、「併加型」、「拿走型」、「比較型」等加減法問題。",
              "認識減法：拿走和比多少",
              "一年級數學 減法 練習題｜拿走型・比較型・10以內減法 學習單（附解答）",
              "認識減法",
              "國小一年級數學「認識減法」免費學習單：看圖拿走還剩多少、比一比多幾個、選算式、10 以內的減法、說故事算減法。100題線上練習，題目短、圖多，附可列印解答。",
              "拿走還剩多少、比多少，用減法",
              "5 － 2 ＝ 3；一個對一個排好，多出來的是差。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
