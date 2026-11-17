# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：認識加法（108課綱 N-1-2、N-1-3）
  python3 tools/gen_tw_math_g1_addition_meaning.py
絵で合わせる（兩堆合起來）、添加型（又來了幾隻）、併加型（兩種合起來）、算式を選ぶ、和 10 まで→18 まで、0 を加える。
誤答：減法の式を選ぶ、一つ多く／少なく數える、足す數と答えを取り違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81202)
NM = Names(R)


def s1(seen):
    def mk():
        a, b = R.randint(1, 6), R.randint(1, 6)
        k = R.choice(P.KINDS)
        q = "兩堆%s合起來，一共有幾%s？" % (P.nm(k), P.cl(k)) + P.groups([(a, k), (b, k)])
        return mcq(q, "%d %s" % (a + b, P.cl(k)), ["%d %s" % (x, P.cl(k)) for x in (a + b - 1, a + b + 1, abs(a - b) if a != b else a + b + 2)], "%d ＋ %d ＝ %d。" % (a, b, a + b))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def add_on():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a + b > 10:
            return None
        who = R.choice([("池塘裡有 %d 隻鴨子，又游來 %d 隻", "隻", "鴨子"), ("樹上有 %d 隻鳥，又飛來 %d 隻", "隻", "鳥"), ("盤子裡有 %d 顆草莓，媽媽又放了 %d 顆", "顆", "草莓"), ("公車上有 %d 個人，又上來 %d 個人", "個", "人")])
        q = "%s。現在有幾%s%s？" % (who[0] % (a, b), who[1], who[2])
        return mcq(q, "%d %s" % (a + b, who[1]), ["%d %s" % (x, who[1]) for x in (abs(a - b) if a != b else a + b + 1, a + b + 1, a + b - 1)], "原來的 %d，再加上又來的 %d：%d ＋ %d ＝ %d。" % (a, b, a, b, a + b))

    def put_together():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a + b > 10:
            return None
        t = R.choice([("紅色的花 %d 朵，黃色的花 %d 朵", "朵", "花"), ("男生 %d 人，女生 %d 人", "人", "人"), ("大球 %d 顆，小球 %d 顆", "顆", "球"), ("貓 %d 隻，狗 %d 隻", "隻", "動物")])
        q = "%s。一共有幾%s%s？" % (t[0] % (a, b), "個" if t[1] == "人" else t[1], t[2])
        u = "人" if t[1] == "人" else t[1]
        return mcq(q, "%d %s" % (a + b, u), ["%d %s" % (x, u) for x in (abs(a - b) if a != b else a + b + 1, a + b + 1, a + b - 1)], "兩種合起來：%d ＋ %d ＝ %d。" % (a, b, a + b))
    return pick_unique(R, add_on, 10, seen) + pick_unique(R, put_together, 10, seen)


def s3(seen):
    def mk():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a + b > 10:
            return None
        k = R.choice(P.KINDS)
        q = "哪一個算式和圖一樣？" + P.groups([(a, k), (b, k)])
        return mcq(q, "%d ＋ %d ＝ %d" % (a, b, a + b), ["%d － %d ＝ %d" % (max(a, b), min(a, b), abs(a - b)) if a != b else "%d ＋ %d ＝ %d" % (a, b, a + b + 1), "%d ＋ %d ＝ %d" % (a, b + 1, a + b + 1), "%d ＋ %d ＝ %d" % (a, b, a + b - 1)], "左邊 %d%s，右邊 %d%s，合起來 %d ＋ %d ＝ %d。" % (a, P.cl(k), b, P.cl(k), a, b, a + b))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, b = R.randint(0, 9), R.randint(0, 9)
        if a + b > 10 or (a == 0 and b == 0):
            return None
        q = "%d ＋ %d ＝ ？" % (a, b)
        return mcq(q, str(a + b), [str(x) for x in (a + b + 1, a + b - 1 if a + b > 0 else 2, abs(a - b) if abs(a - b) != a + b else a + b + 2)], ("%d 加 0 還是 %d。" % (max(a, b), a + b)) if 0 in (a, b) else "從 %d 往後數 %d 個：%d。" % (a, b, a + b))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a + b > 10:
            return None
        who = NM.next()
        t = R.choice([("有 %d 枝鉛筆，%s又買了 %d 枝", "枝", "鉛筆"), ("有 %d 張貼紙，%s又得到 %d 張", "張", "貼紙"), ("有 %d 本故事書，%s又借了 %d 本", "本", "書"), ("有 %d 顆彈珠，%s又撿到 %d 顆", "顆", "彈珠")])
        q = "%s。%s現在有幾%s%s？" % (who + t[0] % (a, who, b), who, t[1], t[2])
        return mcq(q, "%d %s" % (a + b, t[1]), ["%d %s" % (x, t[1]) for x in (abs(a - b) if a != b else a + b + 1, a + b + 1, b)], "%d ＋ %d ＝ %d。" % (a, b, a + b))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("看圖合起來", s1(seen)), ("又來了、合起來", s2(seen)), ("選算式", s3(seen)),
            ("10 以內的加法", s4(seen)), ("說故事算加法", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>加法</b>：把兩堆合起來，或是原來有的再多一些，用「＋」。",
         "3 ＋ 2 ＝ 5，讀作「3 加 2 等於 5」。" + P.groups([(3, "apple"), (2, "apple")]),
         "加 0，數不會變：4 ＋ 0 ＝ 4。"],
        [example("有 4 隻鴨子，又來 3 隻，現在有幾隻？", ["4 ＋ 3。"], "7 隻"),
         example("紅花 5 朵、黃花 2 朵，一共幾朵？", ["5 ＋ 2。"], "7 朵")],
        [("又來了也用減法", "又來了、合起來都用加法"),
         ("從 4 往後數 3，數成 4、5、6", "要從下一個開始數：5、6、7"),
         ("4 ＋ 0 ＝ 0", "加 0 數不變：4")])
    faq = [{"q": "一年級的加法要學什麼？",
            "a": "108課綱 N-1-2、N-1-3：認識加法的意思（添加型、併加型），用操作和圖來算一位數的加法。"},
           {"q": "孩子算加法要用手指嗎？",
            "a": "剛開始可以用手指或積木，慢慢改成「從大的數往後數」，再記住常用的加法。"},
           {"q": "怎麼知道要用加法？",
            "a": "題目說「又來了」「再買」「合起來」「一共」，通常是把東西變多，用加法。"}]
    make_unit(R, "grade-1", "addition-meaning", "N-1-2",
              "加法和減法：加法和減法的意義與應用。含「添加型」、「併加型」、「拿走型」、「比較型」等加減法問題。",
              "認識加法：合起來和又來了",
              "一年級數學 加法 練習題｜看圖加法・10以內加法 學習單（附解答）",
              "認識加法",
              "國小一年級數學「認識加法」免費學習單：看圖把兩堆合起來、又來了和合起來的加法、選算式、10 以內的加法、說故事算加法。100題線上練習，題目短、圖多，附可列印解答。",
              "合起來、又來了，用加法",
              "3 ＋ 2 ＝ 5；加 0 數不變。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
