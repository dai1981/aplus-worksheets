# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：算式與符號（108課綱 R-1-1）
  python3 tools/gen_tw_math_g1_number_sentences.py
＋・－・＝ の讀み方と意味、□ の數（加數・被減數・減數）、等號の兩邊が同じ（3 ＋ 4 ＝ 5 ＋ □）、＞＜＝ で比べる、故事から算式を選ぶ。
誤答：□ に答えの數を入れる、等號の右を答えと思う（3 ＋ 4 ＝ 5 ＋ 7）、減數の □ で足してしまう。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets

R = random.Random(81207)
NM = Names(R)


def s1(seen):
    FACTS = [("「＋」讀作什麼？", "加", ["減", "等於", "大於"], "＋ 讀作「加」。"),
             ("「－」讀作什麼？", "減", ["加", "等於", "小於"], "－ 讀作「減」。"),
             ("「＝」讀作什麼？", "等於", ["加", "減", "大於"], "＝ 讀作「等於」，表示兩邊一樣多。"),
             ("「＞」讀作什麼？", "大於", ["小於", "等於", "加"], "＞ 讀作「大於」，開口對著大的數。"),
             ("「＜」讀作什麼？", "小於", ["大於", "等於", "減"], "＜ 讀作「小於」，尖尖的一邊對著小的數。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def read():
        a, b = R.randint(2, 9), R.randint(1, 9)
        op = R.choice(["＋", "－"])
        if op == "－" and b >= a:
            return None
        v = a + b if op == "＋" else a - b
        w = "加" if op == "＋" else "減"
        q = "「%d %s %d ＝ %d」怎麼讀？" % (a, op, b, v)
        return mcq(q, "%d %s %d 等於 %d" % (a, w, b, v), ["%d %s %d 等於 %d" % (a, "減" if w == "加" else "加", b, v), "%d 等於 %d %s %d" % (a, b, w, v), "%d %s %d 大於 %d" % (a, w, b, v)], "%s 讀作「%s」，＝ 讀作「等於」。" % (op, w))
    return out + pick_unique(R, read, 15, seen)


def s2(seen):
    def mk():
        a, b = R.randint(1, 9), R.randint(1, 9)
        s = a + b
        k = R.choice(["first", "second", "sub_a", "sub_b"])
        if k == "first":
            q, v = "□ ＋ %d ＝ %d，□ 是多少？" % (b, s), a
        elif k == "second":
            q, v = "%d ＋ □ ＝ %d，□ 是多少？" % (a, s), b
        elif k == "sub_a":
            q, v = "□ － %d ＝ %d，□ 是多少？" % (b, a), s
        else:
            q, v = "%d － □ ＝ %d，□ 是多少？" % (s, a), b
        w = {"first": [s, s + b, a + 1], "second": [s, s + a, b + 1], "sub_a": [a - b if a > b else a + 1, b, s + 1], "sub_b": [s + a, a, b + 1]}[k]
        e = {"first": "%d － %d ＝ %d，所以 %d ＋ %d ＝ %d。" % (s, b, a, a, b, s), "second": "%d － %d ＝ %d。" % (s, a, b),
             "sub_a": "拿走 %d 還剩 %d，原來是 %d ＋ %d ＝ %d。" % (b, a, a, b, s), "sub_b": "%d － %d ＝ %d。" % (s, a, b)}[k]
        return mcq(q, str(v), [str(x) for x in w if x != v] + [str(v + 2)], e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(1, 9), R.randint(1, 9)
        c = R.randint(1, a + b - 1) if a + b > 1 else 1
        d = a + b - c
        if d < 1 or c == a or c == b:
            return None
        q = "%d ＋ %d ＝ %d ＋ □，□ 是多少？" % (a, b, c)
        return mcq(q, str(d), [str(a + b), str(a + b + c), str(d + 1)], "等號兩邊要一樣多：%d ＋ %d ＝ %d，%d ＋ %d ＝ %d。" % (a, b, a + b, c, d, a + b))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, b = R.randint(1, 9), R.randint(1, 9)
        c = R.randint(2, 18)
        L = a + b
        sym = "＞" if L > c else "＜" if L < c else "＝"
        q = "%d ＋ %d ○ %d，○ 裡要填什麼？" % (a, b, c)
        return mcq(q, sym, [x for x in ["＞", "＜", "＝"] if x != sym] + ["＋"], "%d ＋ %d ＝ %d，%d %s %d。" % (a, b, L, L, sym, c))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(1, 9)
        who = NM.next()
        k = R.choice(["add", "sub"])
        if k == "add":
            q = "%s有 %d 個餅乾，媽媽又給%s %d 個。哪一個算式可以算出現在有幾個？" % (who, a, who, b)
            ans = "%d ＋ %d ＝ □" % (a, b)
            w = ["%d － %d ＝ □" % (max(a, b), min(a, b)) if a != b else "%d － %d ＝ □" % (a, 1), "%d ＋ %d ＝ □" % (a, a) if a != b else "%d ＋ %d ＝ □" % (a, a + 1), "%d ＋ □ ＝ %d" % (a, b)]
        else:
            if b >= a:
                return None
            q = "%s有 %d 個餅乾，吃掉 %d 個。哪一個算式可以算出還剩幾個？" % (who, a, b)
            ans = "%d － %d ＝ □" % (a, b)
            w = ["%d ＋ %d ＝ □" % (a, b), "□ － %d ＝ %d" % (b, a), "%d ＋ %d ＝ □" % (a, a)]
        return mcq(q, ans, w, "又給是變多，用加法；吃掉是變少，用減法。")
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("認識符號", s1(seen)), ("□ 是多少", s2(seen)), ("等號兩邊一樣多", s3(seen)),
            ("比大小", s4(seen)), ("看故事選算式", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["算式中，<b>＋ 讀作加、－ 讀作減、＝ 讀作等於</b>。",
         "<b>＝ 表示兩邊一樣多</b>：3 ＋ 4 ＝ 5 ＋ 2，兩邊都是 7。",
         "<b>＞ 大於、＜ 小於</b>：開口對著大的數。",
         "□ 是不知道的數，可以用加減法的關係找出來。"],
        [example("6 ＋ □ ＝ 13", ["13 － 6 ＝ 7。"], "7"),
         example("4 ＋ 5 ＝ 6 ＋ □", ["4 ＋ 5 ＝ 9。", "6 ＋ 3 ＝ 9。"], "3")],
        [("4 ＋ 5 ＝ 6 ＋ □，□ 填 9", "等號兩邊要一樣多：□ 是 3"),
         ("□ － 3 ＝ 5，□ 填 2", "拿走 3 還剩 5，原來是 8"),
         ("＞ 的開口對小的數", "開口對大的數：8 ＞ 5")])
    faq = [{"q": "等號只是「答案在後面」的意思嗎？",
            "a": "不是。等號表示左右兩邊一樣多，所以 7 ＝ 3 ＋ 4、3 ＋ 4 ＝ 5 ＋ 2 都是對的算式。"},
           {"q": "一年級的算式要學什麼？",
            "a": "108課綱 R-1-1：加減算式中的數、加號、減號、等號，透過說、讀、做、寫、算的活動學習。"},
           {"q": "□ 的題目怎麼教？",
            "a": "把算式說成故事，例如「6 加多少等於 13」，再想加法和減法的關係：13 － 6。"}]
    make_unit(R, "grade-1", "number-sentences", "R-1-1",
              "算式與符號：含加減算式中的數、加號、減號、等號。以說、讀、做、寫、算的活動為主。",
              "算式與符號：加號、減號、等號",
              "一年級數學 算式與等號 練習題｜□是多少・大於小於 學習單（附解答）",
              "算式與符號",
              "國小一年級數學「算式與符號」免費學習單：認識加號、減號、等號和大於小於、□ 是多少、等號兩邊一樣多、比大小、看故事選算式。100題線上練習，附可列印解答。",
              "＝ 表示兩邊一樣多",
              "3 ＋ 4 ＝ 5 ＋ 2，兩邊都是 7。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
