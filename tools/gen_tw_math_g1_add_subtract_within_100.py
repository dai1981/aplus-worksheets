# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：100 以內的加減（整十和不進位）（108課綱 N-1-1、N-1-2）
  python3 tools/gen_tw_math_g1_add_subtract_within_100.py
整十 ± 整十、二位數 ＋ 一位數（不進位）、二位數 － 一位數（不退位）、二位數 ± 整十、積木の絵、文章題。
誤答：十位と個位をそろえずに足す（34 ＋ 5 ＝ 84）、整十の 0 を落とす（30 ＋ 20 ＝ 5）、十位を動かしてしまう。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81206)
NM = Names(R)


def s1(seen):
    def mk():
        a, b = R.randint(1, 9), R.randint(1, 9)
        op = R.choice(["＋", "－"])
        if op == "＋" and a + b > 10:
            return None
        if op == "－" and a <= b:
            return None
        v = 10 * (a + b) if op == "＋" else 10 * (a - b)
        q = "%d %s %d ＝ ？" % (10 * a, op, 10 * b)
        return mcq(q, str(v), [str(v // 10), str(v + 10), str(v - 10) if v > 10 else str(v + 20)], "%d 個十 %s %d 個十 ＝ %d 個十，是 %d。" % (a, op, b, v // 10, v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        t, o = R.randint(1, 9), R.randint(0, 8)
        b = R.randint(1, 9 - o)
        a = 10 * t + o
        q = "%d ＋ %d ＝ ？" % (a, b)
        v = a + b
        return mcq(q, str(v), [str(a + 10 * b) if a + 10 * b <= 100 else str(v + 10), str(v - 1), str(v + 1)], "個位 %d ＋ %d ＝ %d，十位不變：%d。" % (o, b, o + b, v))

    def pic():
        t, o = R.randint(1, 5), R.randint(0, 4)
        b = R.randint(1, 9 - o)
        if b > 5:
            return None
        a = 10 * t + o
        q = "%d 再加 %d 個，是多少？" % (a, b) + P.rods(t, o)
        return mcq(q, str(a + b), [str(a + 10 * b) if a + 10 * b <= 100 else str(a + b + 10), str(a + b + 1), str(t + o + b)], "%d 個十不變，個位 %d ＋ %d ＝ %d：%d。" % (t, o, b, o + b, a + b))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, pic, 6, seen)


def s3(seen):
    def mk():
        t, o = R.randint(1, 9), R.randint(1, 9)
        b = R.randint(1, o)
        a = 10 * t + o
        q = "%d － %d ＝ ？" % (a, b)
        v = a - b
        return mcq(q, str(v), [str(a - 10 * b) if a - 10 * b > 0 else str(v + 10), str(v + 1), str(v - 1) if v - 1 >= 0 else str(v + 2)], "個位 %d － %d ＝ %d，十位不變：%d。" % (o, b, o - b, v))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        t, o = R.randint(1, 8), R.randint(1, 9)
        k = R.randint(1, 9)
        op = R.choice(["＋", "－"])
        a = 10 * t + o
        if op == "＋" and t + k > 9:
            return None
        if op == "－" and k >= t:
            return None
        v = a + 10 * k if op == "＋" else a - 10 * k
        q = "%d %s %d ＝ ？" % (a, op, 10 * k)
        return mcq(q, str(v), [str(a + k) if op == "＋" else str(a - k), str(v + 1), str(v + 10) if v + 10 <= 100 else str(v - 1)], "個位不變，十位 %d %s %d ＝ %d：%d。" % (t, op, k, t + k if op == "＋" else t - k, v))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def buy():
        a = R.randint(2, 8) * 10
        b = R.randint(1, 9)
        who = NM.next()
        q = "%s有 %d 元，又存了 %d 元，現在有多少元？" % (who, a, b)
        return mcq(q, "%d 元" % (a + b), ["%d 元" % x for x in (a + 10 * b if a + 10 * b <= 100 else a + b + 10, a - b, a + b + 1)], "%d ＋ %d ＝ %d。" % (a, b, a + b))

    def page():
        t, o = R.randint(2, 9), R.randint(3, 9)
        b = R.randint(1, o)
        a = 10 * t + o
        who = NM.next()
        if R.random() >= .5 and a > 40:
            return None
        q = "一本書有 %d 頁，%s已經看了 %d 頁，還有幾頁沒看？" % (a, who, b) if R.random() < .5 else "一盒雞蛋有 %d 顆，打破了 %d 顆，還有幾顆好的？" % (a, b)
        return mcq(q, str(a - b) + (" 頁" if "書" in q else " 顆"), [str(x) + (" 頁" if "書" in q else " 顆") for x in (a + b, a - 10 * b if a - 10 * b > 0 else a - b + 1, a - b + 1)], "%d － %d ＝ %d。" % (a, b, a - b))

    def tens():
        a, b = R.randint(2, 6), R.randint(1, 3)
        q = "一盒彩色筆有 10 枝。哥哥有 %d 盒，妹妹有 %d 盒，一共有幾枝？" % (a, b)
        return mcq(q, "%d 枝" % (10 * (a + b)), ["%d 枝" % x for x in (a + b, 10 * (a + b) + 10, 10 * abs(a - b) if a != b else 10)], "%d ＋ %d ＝ %d 盒，%d 盒是 %d 枝。" % (a, b, a + b, a + b, 10 * (a + b)))
    return pick_unique(R, buy, 7, seen) + pick_unique(R, page, 8, seen) + pick_unique(R, tens, 5, seen)


def main():
    seen = set()
    sets = [("整十加減", s1(seen)), ("二位數加一位數", s2(seen)), ("二位數減一位數", s3(seen)),
            ("加減整十", s4(seen)), ("說故事算一算", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>整十加減</b>：30 ＋ 20 是 3 個十加 2 個十，是 5 個十，就是 50。",
         "<b>加減一位數</b>：個位和個位算，十位不變。34 ＋ 5 ＝ 39。",
         "<b>加減整十</b>：十位和十位算，個位不變。34 ＋ 20 ＝ 54。"],
        [example("46 － 3", ["個位 6 － 3 ＝ 3，十位不變。"], "43"),
         example("52 ＋ 30", ["十位 5 ＋ 3 ＝ 8，個位不變。"], "82")],
        [("34 ＋ 5 ＝ 84", "5 要加在個位：39"),
         ("30 ＋ 20 ＝ 5", "3 個十加 2 個十是 5 個十：50"),
         ("52 ＋ 30 ＝ 55", "30 是 3 個十，要加在十位：82")])
    faq = [{"q": "為什麼要分十位和個位來算？",
            "a": "十位表示幾個十，個位表示幾個一，同樣單位的才能直接相加減，這是二年級學直式的基礎。"},
           {"q": "一年級會學進位嗎？",
            "a": "一年級主要是湊十的進位（例如 8 ＋ 5），二位數的進位、退位加減和直式在二年級學。"},
           {"q": "怎麼幫孩子分清十位和個位？",
            "a": "用一捆捆的吸管當「十」、一根根當「一」，加減時先看要動的是捆還是根。"}]
    make_unit(R, "grade-1", "add-subtract-within-100", "N-1-1",
              "一百以內的數：含操作活動。用數表示多少與順序。結合數數、位值表徵、位值表。位值單位「個」和「十」。",
              "100 以內的加減：整十和不進位",
              "一年級數學 100以內加減 練習題｜整十加減・二位數加減一位數 學習單（附解答）",
              "100 以內的加減",
              "國小一年級數學「100 以內的加減」免費學習單：整十加減、二位數加減一位數（不進位）、加減整十、存錢和看書應用題。100題線上練習，附可列印解答。",
              "個位和個位算，十位和十位算",
              "34 ＋ 5 ＝ 39；34 ＋ 20 ＝ 54。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
