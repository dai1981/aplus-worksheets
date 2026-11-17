# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：九九乘法（十十乘法）（108課綱 N-2-7）
  python3 tools/gen_tw_math_g2_multiplication_tables.py
2・5・10 の段、3・4 の段、6・7 の段、8・9 の段、□ を求める（4 × □ ＝ 28）、交換律（3 × 7 ＝ 7 × 3）、文章題。
誤答：隣の答え（7 × 8 で 48 や 63）、足し算（7 ＋ 8）、6 × 7 と 6 × 8 の取り違え。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table
from tw_g7 import tidy_sets

R = random.Random(81308)
NM = Names(R)


def fact(tables, seen, n):
    def mk():
        a = R.choice(tables)
        b = R.randint(1, 10)
        if R.random() < .5:
            a, b = b, a
        p = a * b
        q = "%d × %d ＝ ？" % (a, b)
        w = [p + a, p - a if p - a > 0 else p + 2 * a, p + b if b != a else p + 1, a + b, p - b if p - b > 0 else p + 3]
        return mcq(q, str(p), [str(x) for x in w if x != p][:3] + [str(p + 2)], "%d × %d ＝ %d。也可以想 %d × %d ＝ %d，再%s一個 %d。" % (a, b, p, a, b - 1, a * (b - 1), "加", a) if b > 1 else "%d × 1 ＝ %d。" % (a, a))
    return pick_unique(R, mk, n, seen)


def s1(seen):
    return fact([2, 5, 10], seen, 20)


def s2(seen):
    return fact([3, 4], seen, 20)


def s3(seen):
    return fact([6, 7], seen, 20)


def s4(seen):
    out = fact([8, 9], seen, 12)

    def miss():
        a, b = R.randint(2, 9), R.randint(2, 9)
        q = "%d × □ ＝ %d，□ 是多少？" % (a, a * b)
        return mcq(q, str(b), [str(b + 1), str(b - 1), str(a * b - a)], "想 %d 的乘法：%d × %d ＝ %d，□ ＝ %d。" % (a, a, b, a * b, b))

    def swap():
        a, b = R.sample(range(2, 10), 2)
        q = "%d × %d ＝ %d，那麼 %d × %d ＝ ？" % (a, b, a * b, b, a)
        return mcq(q, str(a * b), [str(a + b), str(a * b + b), str(a * b - a)], "兩個數交換位置相乘，答案一樣：%d。" % (a * b))
    return out + pick_unique(R, miss, 5, seen) + pick_unique(R, swap, 3, seen)


def s5(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(2, 9)
        who = NM.next()
        t = R.choice([("一盒鉛筆有 %d 枝，%s買了 %d 盒。一共有幾枝？", "枝"), ("每張桌子坐 %d 人，有 %d 張桌子。一共可以坐幾人？", "人"),
                      ("一星期有 7 天，%d 個星期是幾天？", "天"), ("一包餅乾 %d 元，%s買 %d 包要多少元？", "元"), ("每頁貼 %d 張貼紙，貼了 %d 頁。一共貼了幾張？", "張")])
        if "星期" in t[0]:
            a = 7
            q = "一星期有 7 天，%d 個星期是幾天？" % b
        elif "%s" in t[0]:
            q = t[0] % (a, who, b)
        else:
            q = t[0] % (a, b)
        return mcq(q, "%d %s" % (a * b, t[1]), ["%d %s" % (x, t[1]) for x in (a + b, a * b + a, a * b - b)], "%d × %d ＝ %d。" % (a, b, a * b))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("2、5、10 的乘法", s1(seen)), ("3、4 的乘法", s2(seen)), ("6、7 的乘法", s3(seen)),
            ("8、9 的乘法和 □", s4(seen)), ("乘法應用", s5(seen))]
    tidy_sets(sets)
    rows = [[str(a)] + [str(a * b) for b in range(1, 11)] for a in (2, 5)]
    body = lesson(
        ["九九乘法要背熟。先背簡單的 <b>2、5、10</b>，再背 3、4，最後 6、7、8、9。",
         "忘了可以從前一個加：7 × 6 ＝ 7 × 5 ＋ 7 ＝ 35 ＋ 7 ＝ 42。" + table(["×"] + [str(b) for b in range(1, 11)], rows),
         "兩個數交換位置相乘，答案一樣：3 × 8 ＝ 8 × 3 ＝ 24。"],
        [example("6 × 7", ["6 × 6 ＝ 36，再加 6。"], "42"),
         example("4 × □ ＝ 32", ["4 × 8 ＝ 32。"], "□ ＝ 8")],
        [("7 × 8 ＝ 48", "6 × 8 ＝ 48，7 × 8 ＝ 56"),
         ("6 × 7 寫成 6 ＋ 7 ＝ 13", "乘法是 7 個 6：42"),
         ("9 × 1 ＝ 1", "任何數乘以 1 都是它自己：9")])
    faq = [{"q": "九九乘法什麼時候要背熟？",
            "a": "108課綱 N-2-7：二年級的十十乘法要以熟練為目標，它是三年級乘除直式的基礎。"},
           {"q": "背不起來的幾個怎麼辦？",
            "a": "用交換（7 × 3 想成 3 × 7）、從前一個加、或 9 的技巧（9 × 6：十位比 6 少 1 是 5，兩位相加是 9，所以 54）。"},
           {"q": "每天要練多久？",
            "a": "每天 5 分鐘短時間練習，比一次練很久有效，可以用這裡的題目線上對答案。"}]
    make_unit(R, "grade-2", "multiplication-tables", "N-2-7",
              "十十乘法：乘除直式計算的基礎，以熟練為目標。",
              "九九乘法：2 到 10 的乘法",
              "二年級數學 九九乘法 練習題｜九九乘法表・十十乘法 學習單（附解答）",
              "九九乘法",
              "國小二年級數學「九九乘法」免費學習單：2、5、10 的乘法，3、4 的乘法，6、7 的乘法，8、9 的乘法和 □ 是多少，乘法應用題。100題線上練習，附可列印解答。",
              "九九乘法要背熟",
              "忘了就從前一個加：7 × 6 ＝ 35 ＋ 7 ＝ 42。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
