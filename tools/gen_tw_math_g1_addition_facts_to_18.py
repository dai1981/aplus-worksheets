# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：20 以內的加法（湊十）（108課綱 N-1-3）
  python3 tools/gen_tw_math_g1_addition_facts_to_18.py
10 の合成（幾和幾合成 10）、十格板で湊十、和が 11〜18 の基本加法、交換して同じ、文章題。
誤答：湊十で分ける數を間違える、答えを 1 つ少なく數える、十位を落として個位だけ書く。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81204)
NM = Names(R)


def s1(seen):
    def mk():
        a = R.randint(1, 9)
        k = R.choice(["fill", "pic"])
        if k == "pic":
            q = "十格板裡有 %d 個，還要幾個才湊成 10？" % a + P.tenframe(a)
        else:
            q = "%d 和幾合成 10？" % a
        return mcq(q, str(10 - a), [str(x) for x in (a, 10 - a + 1, 10 - a - 1 if 10 - a > 1 else 3) if x != 10 - a] + [str(10)], "%d ＋ %d ＝ 10。" % (a, 10 - a))
    return pick_unique(R, mk, 18, seen)


def s2(seen):
    def mk():
        a = R.randint(6, 9)
        b = R.randint(10 - a + 1, 9)
        need = 10 - a
        q = "算 %d ＋ %d：先把 %d 分成 %d 和幾，湊成 10？" % (a, b, b, need)
        return mcq(q, "%d 和 %d" % (need, b - need), ["%d 和 %d" % (b - need, need) if b - need != need else "%d 和 %d" % (need, b - need + 1), "%d 和 %d" % (need, b), "%d 和 %d" % (a, b - a) if b > a else "%d 和 %d" % (need + 1, b - need - 1)], "%d 還差 %d 湊 10，%d ＝ %d ＋ %d：%d ＋ %d ＝ 10，10 ＋ %d ＝ %d。" % (a, need, b, need, b - need, a, need, b - need, a + b))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a + b < 11:
            return None
        q = "%d ＋ %d ＝ ？" % (a, b)
        s = a + b
        return mcq(q, str(s), [str(s - 1), str(s + 1), str(s - 10)], "湊十：%d ＋ %d ＝ 10，再加 %d：%d。" % (max(a, b), 10 - max(a, b), s - 10, s))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def pic():
        a, b = R.randint(5, 9), R.randint(2, 9)
        if a + b < 11:
            return None
        q = "上面 %d 個、下面 %d 個，一共有幾個？" % (a, b) + P.tenframe(a + b, 2)
        return mcq(q, str(a + b), [str(a + b - 1), str(a + b + 1), str(a + b - 10)], "一個十格板滿了是 10，另一個有 %d 個：10 ＋ %d ＝ %d。" % (a + b - 10, a + b - 10, a + b))

    def swap():
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a == b or a + b < 11:
            return None
        q = "%d ＋ %d ＝ %d，那麼 %d ＋ %d ＝ ？" % (a, b, a + b, b, a)
        return mcq(q, str(a + b), [str(a - b) if a > b else str(b - a), str(a + b + 1), str(a + b - 1)], "兩個數交換位置相加，答案一樣：%d。" % (a + b))
    return pick_unique(R, pic, 12, seen) + pick_unique(R, swap, 8, seen)


def s5(seen):
    def mk():
        a, b = R.randint(3, 9), R.randint(3, 9)
        if a + b < 11:
            return None
        who = NM.next()
        t = R.choice([("%s摺了 %d 隻紙鶴，又摺了 %d 隻", "隻"), ("%s有 %d 張卡片，哥哥又給她 %d 張", "張"), ("%s上午看了 %d 頁書，下午看了 %d 頁", "頁"), ("籃子裡有 %d 顆橘子，%s又放進 %d 顆", "顆")])
        txt = t[0] % ((who, a, b) if t[0].startswith("%s") else (a, who, b))
        q = "%s。一共有幾%s？" % (txt, t[1])
        return mcq(q, "%d %s" % (a + b, t[1]), ["%d %s" % (x, t[1]) for x in (a + b - 1, a + b + 1, abs(a - b) if a != b else a + b - 10)], "%d ＋ %d ＝ %d。" % (a, b, a + b))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    first = s1(seen)
    extra = [mcq("5 和幾合成 10？", "5", ["4", "6", "10"], "5 ＋ 5 ＝ 10。"), mcq("0 和幾合成 10？", "10", ["0", "9", "1"], "0 ＋ 10 ＝ 10。"), mcq("10 可以分成 6 和幾？", "4", ["6", "3", "5"], "6 ＋ 4 ＝ 10。"), mcq("10 可以分成 2 和幾？", "8", ["2", "7", "9"], "2 ＋ 8 ＝ 10。")]
    first = [x for x in first if x["q"] not in ("5 和幾合成 10？",)]
    first = (first + extra)[:20]
    sets = [("合成 10", first), ("湊十的方法", s2(seen)), ("20 以內的加法", s3(seen)),
            ("看圖和交換", s4(seen)), ("說故事算加法", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["先記熟<b>合成 10</b>：1 和 9、2 和 8、3 和 7、4 和 6、5 和 5。",
         "<b>湊十法</b>：8 ＋ 5，8 還差 2 湊 10，把 5 分成 2 和 3：8 ＋ 2 ＝ 10，10 ＋ 3 ＝ 13。" + P.tenframe(13, 2),
         "兩個數交換位置相加，答案不變：8 ＋ 5 ＝ 5 ＋ 8。"],
        [example("9 ＋ 4", ["9 還差 1 湊 10，4 分成 1 和 3。", "10 ＋ 3。"], "13"),
         example("7 ＋ 6", ["7 還差 3，6 分成 3 和 3。", "10 ＋ 3。"], "13")],
        [("8 ＋ 5 寫成 3", "超過 10 時，要寫 13"),
         ("湊十時分錯數", "看大的數還差幾個到 10"),
         ("往後數時數成 8、9、10 少一個", "從下一個數開始數")])
    faq = [{"q": "什麼是湊十法？",
            "a": "把其中一個數分成兩部分，先湊成 10，再加剩下的，例如 9 ＋ 4 ＝ 9 ＋ 1 ＋ 3 ＝ 13，是台灣一年級常用的方法。"},
           {"q": "一年級要背哪些加法？",
            "a": "108課綱 N-1-3：一位數加一位數的基本加法（和到 18），要能熟練，二年級學直式時才會順。"},
           {"q": "孩子湊十很慢怎麼辦？",
            "a": "先用十格板和積木把「合成 10」玩熟，熟了以後湊十就會變快。"}]
    make_unit(R, "grade-1", "addition-facts-to-18", "N-1-3",
              "基本加減法：以操作活動為主。以熟練為目標。指1到10之數與1到10之數的加法，及反向的減法計算。",
              "20 以內的加法：湊十法",
              "一年級數學 湊十法 加法練習題｜合成10・20以內進位加法 學習單（附解答）",
              "20 以內的加法",
              "國小一年級數學「20 以內的加法：湊十法」免費學習單：合成 10、湊十的方法、和到 18 的加法、十格板看圖、交換相加、說故事算加法。100題線上練習，附可列印解答。",
              "湊十：先湊成 10，再加剩下的",
              "8 ＋ 5 ＝ 8 ＋ 2 ＋ 3 ＝ 13。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
