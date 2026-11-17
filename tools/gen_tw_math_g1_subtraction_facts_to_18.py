# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：20 以內的減法（破十法）（108課綱 N-1-3）
  python3 tools/gen_tw_math_g1_subtraction_facts_to_18.py
10 から引く、破十法（13 － 8 ＝ 10 － 8 ＋ 3）、退位のある 20 以內の減法、加減の關係（8 ＋ 5 ＝ 13 なら 13 － 5 ＝ 8）、文章題。
誤答：個位どうしを逆に引く（13 － 8 で 8 － 3 ＝ 5 は偶然正しくなるので避ける）、1 つずれる、加法をする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81205)
NM = Names(R)


def s1(seen):
    def mk():
        b = R.randint(1, 9)
        k = R.choice(["n", "pic"])
        q = ("10 － %d ＝ ？" % b) if k == "n" else ("10 個拿走 %d 個，還剩幾個？" % b + P.crossed(10, R.choice(P.KINDS), b))
        return mcq(q, str(10 - b), [str(x) for x in (b, 10 - b + 1, 10 - b - 1 if b < 9 else 3, 10 + b) if x != 10 - b], "%d 和 %d 合成 10，所以 10 － %d ＝ %d。" % (b, 10 - b, b, 10 - b))
    return pick_unique(R, mk, 18, seen) + [mcq("10 － 10 ＝ ？", "0", ["10", "1", "20"], "減掉自己是 0。"), mcq("10 － 0 ＝ ？", "10", ["0", "1", "9"], "減 0 數不變。")]


def s2(seen):
    def mk():
        o = R.randint(1, 8)
        b = R.randint(o + 1, 9)
        a = 10 + o
        q = "用破十法算 %d － %d：先算 10 － %d ＝ ？，再加 %d。" % (a, b, b, o)
        return mcq(q, "10 － %d ＝ %d，%d ＋ %d ＝ %d" % (b, 10 - b, 10 - b, o, a - b), ["10 － %d ＝ %d，%d ＋ %d ＝ %d" % (b, 10 - b, 10 - b, o, a - b + 1), "10 － %d ＝ %d，%d － %d ＝ %d" % (b, 10 - b, 10 - b, min(o, 10 - b), abs(10 - b - o)), "10 － %d ＝ %d，%d ＋ %d ＝ %d" % (b, 10 - b + 1, 10 - b + 1, o, a - b + 1)], "%d 分成 10 和 %d。10 － %d ＝ %d，再和 %d 合起來：%d。" % (a, o, b, 10 - b, o, a - b))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        o = R.randint(0, 8)
        b = R.randint(o + 1, 9)
        a = 10 + o
        q = "%d － %d ＝ ？" % (a, b)
        v = a - b
        return mcq(q, str(v), [str(x) for x in (v + 1, v - 1 if v > 1 else v + 2, b - o, a + b) if x != v][:3], "破十法：10 － %d ＝ %d，%d ＋ %d ＝ %d。" % (b, 10 - b, 10 - b, o, v))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, b = R.randint(3, 9), R.randint(3, 9)
        if a + b < 11:
            return None
        s = a + b
        q = "%d ＋ %d ＝ %d，那麼 %d － %d ＝ ？" % (a, b, s, s, b)
        return mcq(q, str(a), [str(b) if b != a else str(a + 1), str(s + b), str(a - 1)], "加法倒過來就是減法：%d 拿走 %d，剩 %d。" % (s, b, a))

    def missing():
        a, b = R.randint(3, 9), R.randint(3, 9)
        if a + b < 11:
            return None
        q = "%d ＋ □ ＝ %d，□ 是多少？" % (a, a + b)
        return mcq(q, str(b), [str(a + b + a), str(b + 1), str(b - 1)], "□ ＝ %d － %d ＝ %d。" % (a + b, a, b))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, missing, 10, seen)


def s5(seen):
    def take():
        o = R.randint(1, 8)
        b = R.randint(o + 1, 9)
        a = 10 + o
        who = NM.next()
        t = R.choice([("%s有 %d 顆彈珠，送給弟弟 %d 顆", "顆"), ("%s有 %d 元，買了一枝 %d 元的鉛筆", "元"), ("停車場有 %d 輛車，開走 %d 輛", "輛"), ("%s有 %d 張貼紙，用掉 %d 張", "張")])
        txt = t[0] % ((who, a, b) if t[0].startswith("%s") else (a, b))
        q = "%s。還剩%s？" % (txt, "多少元" if t[1] == "元" else "幾" + t[1])
        return mcq(q, "%d %s" % (a - b, t[1]), ["%d %s" % (x, t[1]) for x in (a + b, a - b + 1, b - o)], "%d － %d ＝ %d。" % (a, b, a - b))

    def cmp():
        a = R.randint(11, 18)
        b = R.randint(3, 9)
        x, y = NM.next(), NM.next()
        q = "%s跳繩跳了 %d 下，%s跳了 %d 下。%s多跳幾下？" % (x, a, y, b, x)
        return mcq(q, "%d 下" % (a - b), ["%d 下" % v for v in (a + b, a - b + 1, a - b - 1)], "%d － %d ＝ %d。" % (a, b, a - b))
    return pick_unique(R, take, 12, seen) + pick_unique(R, cmp, 8, seen)


def main():
    seen = set()
    sets = [("10 減幾", s1(seen)), ("破十法", s2(seen)), ("20 以內的減法", s3(seen)),
            ("加法和減法", s4(seen)), ("說故事算減法", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["先記熟 <b>10 減幾</b>：10 － 1 ＝ 9、10 － 2 ＝ 8 ……",
         "<b>破十法</b>：13 － 8，把 13 分成 10 和 3。10 － 8 ＝ 2，2 ＋ 3 ＝ 5。",
         "加法和減法是一家人：8 ＋ 5 ＝ 13，所以 13 － 5 ＝ 8、13 － 8 ＝ 5。"],
        [example("14 － 9", ["10 － 9 ＝ 1。", "1 ＋ 4 ＝ 5。"], "5"),
         example("6 ＋ □ ＝ 15", ["□ ＝ 15 － 6。"], "9")],
        [("13 － 8，用 8 － 3 算", "個位 3 不夠減 8，要從 10 裡拿"),
         ("破十後忘了加回 3", "10 － 8 ＝ 2，還要加 3"),
         ("還剩多少用加法", "拿走、用掉用減法")])
    faq = [{"q": "什麼是破十法？",
            "a": "被減數拆成 10 和幾，先用 10 去減，再把結果和剩下的數合起來，例如 12 － 7 ＝ 3 ＋ 2 ＝ 5，是台灣一年級常用的方法。"},
           {"q": "還有其他算法嗎？",
            "a": "也可以「連減」：13 － 8 ＝ 13 － 3 － 5 ＝ 5，或想加法：8 加幾等於 13。"},
           {"q": "一年級的減法要學到哪裡？",
            "a": "108課綱 N-1-3：基本加減法的反向減法，也就是 18 以內減一位數，要能熟練。"}]
    make_unit(R, "grade-1", "subtraction-facts-to-18", "N-1-3",
              "基本加減法：以操作活動為主。以熟練為目標。指1到10之數與1到10之數的加法，及反向的減法計算。",
              "20 以內的減法：破十法",
              "一年級數學 破十法 減法練習題｜10減幾・20以內退位減法 學習單（附解答）",
              "20 以內的減法",
              "國小一年級數學「20 以內的減法：破十法」免費學習單：10 減幾、破十法、18 以內的退位減法、加法和減法的關係、說故事算減法。100題線上練習，附可列印解答。",
              "破十：先用 10 去減，再加剩下的",
              "13 － 8：10 － 8 ＝ 2，2 ＋ 3 ＝ 5。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
