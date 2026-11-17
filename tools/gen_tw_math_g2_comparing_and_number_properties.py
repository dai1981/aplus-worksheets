# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：大小關係與運算規律（108課綱 R-2-1、R-2-4）
  python3 tools/gen_tw_math_g2_comparing_and_number_properties.py
＞・＜ を算式の比較に使う（計算せずに判斷も）、遞移律（甲 ＞ 乙、乙 ＞ 丙 なら 甲 ＞ 丙）、加法交換律・結合律、乘法交換律、□ に入る數。
誤答：記號の向きを逆にする、計算しないで見た目で決める、遞移律で順番を取り違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets

R = random.Random(81317)
NM = Names(R)


def sym(a, b):
    return "＞" if a > b else "＜" if a < b else "＝"


def s1(seen):
    def mk():
        a, b = R.randint(100, 999), R.randint(100, 999)
        if a == b:
            return None
        q = "%d ○ %d，○ 裡要填什麼？" % (a, b)
        s = sym(a, b)
        return mcq(q, s, [x for x in ("＞", "＜", "＝") if x != s] + ["＋"], "%d %s %d。開口對著大的數。" % (a, s, b))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(10, 90), R.randint(10, 90)
        c, d = R.randint(10, 90), R.randint(10, 90)
        op1, op2 = R.choice(["＋", "－"]), R.choice(["＋", "－"])
        L = a + b if op1 == "＋" else a - b
        Rr = c + d if op2 == "＋" else c - d
        if L < 0 or Rr < 0:
            return None
        q = "%d %s %d ○ %d %s %d，○ 裡要填什麼？" % (a, op1, b, c, op2, d)
        s = sym(L, Rr)
        return mcq(q, s, [x for x in ("＞", "＜", "＝") if x != s] + ["＋"], "左邊 %d，右邊 %d，%d %s %d。" % (L, Rr, L, s, Rr))

    def nocalc():
        a, b = R.randint(100, 500), R.randint(10, 99)
        k = R.randint(1, 9)
        op = R.choice(["add", "sub"])
        if op == "add":
            q = "不用算出答案：%d ＋ %d ○ %d ＋ %d，○ 裡要填什麼？" % (a, b, a, b + k)
            s = "＜"
            e = "%d 一樣，%d 比 %d 小，所以左邊比較小。" % (a, b, b + k)
        else:
            q = "不用算出答案：%d － %d ○ %d － %d，○ 裡要填什麼？" % (a, b, a, b + k)
            s = "＞"
            e = "%d 一樣，減掉的 %d 比較少，剩下的比較多。" % (a, b)
        return mcq(q, s, [x for x in ("＞", "＜", "＝") if x != s] + ["不能比"], e)
    return pick_unique(R, mk, 12, seen) + pick_unique(R, nocalc, 8, seen)


def s3(seen):
    def mk():
        x, y, z = R.sample(["甲", "乙", "丙"], 3)
        who = R.choice([("身高", "高", "最高", "最矮"), ("繩子", "長", "最長", "最短"), ("書包", "重", "最重", "最輕")])
        k = R.choice([2, 3])
        q = "比%s：%s比%s%s，%s比%s%s。誰%s？" % (who[0], x, y, who[1], y, z, who[1], who[2] if k == 2 else who[3])
        ans = x if k == 2 else z
        return mcq(q, ans, [v for v in (x, y, z) if v != ans] + ["不知道"], "%s ＞ %s，%s ＞ %s，所以 %s ＞ %s ＞ %s，%s%s。" % (x, y, y, z, x, y, z, ans, who[2] if k == 2 else who[3]))

    def num():
        a = R.randint(100, 900)
        b = a - R.randint(5, 50)
        c = b - R.randint(5, 50)
        q = "□ ＞ %d，%d ＞ %d。下面哪一句一定對？" % (b, b, c)
        return mcq(q, "□ ＞ %d" % c, ["□ ＜ %d" % c, "□ ＝ %d" % b, "□ ＜ %d" % b], "□ 比 %d 大，%d 又比 %d 大，所以 □ 也比 %d 大。" % (b, b, c, c))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, num, 8, seen)


def s4(seen):
    def comm():
        a, b = R.randint(10, 500), R.randint(10, 400)
        if a + b > 999:
            return None
        q = "%d ＋ %d ＝ %d，那麼 %d ＋ %d ＝ ？" % (a, b, a + b, b, a)
        return mcq(q, str(a + b), [str(abs(a - b)), str(a + b + 10), str(a + b - 1)], "兩數相加，交換位置答案不變（加法交換律）。")

    def assoc():
        a = R.randint(10, 90)
        b = R.choice([x for x in range(10, 99) if (a + x) % 10 == 0])
        c = R.randint(10, 300)
        q = "（%d ＋ %d）＋ %d 和 %d ＋（%d ＋ %d）的答案一樣嗎？" % (c, a, b, c, a, b)
        return mcq(q, "一樣，都是 %d" % (a + b + c), ["不一樣，左邊比較大", "不一樣，右邊比較大", "一樣，都是 %d" % (a + b + c + 10)], "三數相加，先加哪兩個答案都一樣（加法結合律），先算 %d ＋ %d ＝ %d 比較簡單。" % (a, b, a + b))

    def mul():
        a, b = R.sample(range(2, 10), 2)
        q = "%d × %d ＝ %d，那麼 %d × %d ＝ ？" % (a, b, a * b, b, a)
        return mcq(q, str(a * b), [str(a + b), str(a * b + a), str(a * b - b)], "兩數相乘，交換位置答案不變（乘法交換律）。")
    return pick_unique(R, comm, 7, seen) + pick_unique(R, assoc, 6, seen) + pick_unique(R, mul, 7, seen)


def s5(seen):
    def mk():
        a = R.randint(100, 800)
        b = R.randint(10, 150)
        k = R.choice(["gt", "lt"])
        if k == "gt":
            q = "%d ＋ □ ＞ %d，□ 裡最小可以填多少？（填整數）" % (a, a + b)
            return mcq(q, str(b + 1), [str(b), str(b - 1), str(a + b + 1)], "%d ＋ %d ＝ %d 是相等，要大於，□ 至少是 %d。" % (a, b, a + b, b + 1))
        q = "%d ＋ □ ＜ %d，□ 裡最大可以填多少？（填整數）" % (a, a + b)
        return mcq(q, str(b - 1), [str(b), str(b + 1), str(a + b - 1)], "%d ＋ %d ＝ %d 是相等，要小於，□ 最多是 %d。" % (a, b, a + b, b - 1))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("比大小", s1(seen)), ("算式比大小", s2(seen)), ("誰最大、誰最小", s3(seen)),
            ("交換和結合", s4(seen)), ("□ 裡可以填多少", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>＞ 大於、＜ 小於</b>：開口對著大的數。算式也可以比大小，先算出兩邊再比。",
         "<b>遞移</b>：甲比乙高、乙比丙高，所以甲比丙高，甲最高。",
         "加法和乘法可以<b>交換位置</b>：25 ＋ 38 ＝ 38 ＋ 25，6 × 4 ＝ 4 × 6；三個數相加可以先加任兩個（先湊整十）。"],
        [example("45 ＋ 28 ○ 45 ＋ 31", ["45 一樣，28 比 31 小。"], "＜"),
         example("甲比乙重，乙比丙重，誰最輕？", ["甲 ＞ 乙 ＞ 丙。"], "丙")],
        [("8 ＜ 5", "開口對大的數：8 ＞ 5"),
         ("45 － 18 ○ 45 － 25，減得多的比較大", "減掉的越多，剩下越少"),
         ("□ ＋ 30 ＞ 50，□ 填 20", "等於 50 不行，□ 至少 21")])
    faq = [{"q": "二年級為什麼要學 ＞ 和 ＜？",
            "a": "108課綱 R-2-1：認識 ＞、＜ 在算式中的意義，和大小的遞移關係，是學不等式的基礎。"},
           {"q": "什麼是交換律、結合律？",
            "a": "108課綱 R-2-4：加法和乘法交換位置答案不變（交換律），三數相加先加哪兩個都一樣（結合律），可以讓計算更簡單。"},
           {"q": "減法也可以交換嗎？",
            "a": "不行。10 － 3 ＝ 7，但 3 － 10 不一樣，交換律只用在加法和乘法。"}]
    make_unit(R, "grade-2", "comparing-and-number-properties", "R-2-1",
              "大小關係與遞移律：「>」與「<」符號在算式中的意義，大小的遞移關係。",
              "大小關係與運算規律",
              "二年級數學 大於小於 練習題｜算式比大小・交換律結合律 學習單（附解答）",
              "大小關係與運算規律",
              "國小二年級數學「大小關係與運算規律」免費學習單：用大於小於比大小、算式比大小、誰最大誰最小（遞移）、加法和乘法交換律、加法結合律、□ 裡可以填多少。100題線上練習，附可列印解答。",
              "＞、＜ 開口對著大的數",
              "加法、乘法可以交換位置，答案不變。",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
