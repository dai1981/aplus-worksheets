# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：認識錢幣（108課綱 N-1-4）
  python3 tools/gen_tw_math_g1_money.py
1 元・5 元・10 元・50 元硬幣と 100 元紙鈔、數錢（大きい方から數える）、換錢、ちょうど付ける、夠不夠、找錢（100 元以內）。
誤答：硬幣の個數を金額にする、5 元を 1 元として數える、找錢で足してしまう。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81208)
NM = Names(R)
ITEMS = [("鉛筆", 8), ("橡皮擦", 12), ("麵包", 25), ("果汁", 20), ("尺", 15), ("筆記本", 30), ("貼紙", 9), ("棒棒糖", 5), ("色鉛筆", 45), ("玩具車", 60), ("故事書", 85), ("彈珠", 6)]


def s1(seen):
    def mk():
        n10, n5, n1 = R.randint(0, 3), R.randint(0, 2), R.randint(0, 4)
        if n10 + n5 + n1 < 2:
            return None
        vals = [10] * n10 + [5] * n5 + [1] * n1
        t = sum(vals)
        q = "一共是多少元？" + P.money_svg(vals)
        return mcq(q, "%d 元" % t, ["%d 元" % x for x in (len(vals), n10 + n5 * 1 + n1 if n10 + n5 + n1 != t else t + 1, t + 5, t - 1 if t > 1 else t + 2) if x != t][:3], "%s：%d 元。" % (" ＋ ".join(str(v) for v in vals), t))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    PAIRS = [(5, 1), (10, 1), (10, 5), (50, 10), (50, 5), (100, 10), (100, 50)]

    def mk():
        big, small = R.choice(PAIRS)
        n = big // small
        k = R.choice([1, 2]) if big * 2 <= 100 else 1
        q = "%d %s %d 元可以換幾個 %d 元？" % (k, "張" if big == 100 else "個", big, small)
        v = n * k
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in (big, small, v + 1, v * 2) if x != v][:3], "%d 元是 %d 個 %d 元。" % (big * k, v, small))

    def rev():
        big, small = R.choice(PAIRS)
        n = big // small
        q = "幾個 %d 元可以換 1 %s %d 元？" % (small, "張" if big == 100 else "個", big)
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in (big, n + 1, n - 1 if n > 2 else n + 2) if x != n], "%d 個 %d 元合起來是 %d 元。" % (n, small, big))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, rev, 7, seen) + [mcq("100 元紙鈔可以換幾個 10 元？", "10 個", ["100 個", "1 個", "5 個"], "10 個 10 元是 100 元。")]


def s3(seen):
    def mk():
        vals = []
        if R.random() < .5:
            vals.append(50)
        vals += [10] * R.randint(0, 3) + [5] * R.randint(0, 1) + [1] * R.randint(0, 4)
        if R.random() < .3 and sum(vals) <= 60:
            vals = [100] + vals[:3]
        t = sum(vals)
        if len(vals) < 4 or t > 150:
            return None
        q = "一共是多少元？（先數大的）" + P.money_svg(vals)
        return mcq(q, "%d 元" % t, ["%d 元" % x for x in (len(vals), t - 10, t + 10, t + 1)], "從大的開始數：%s，一共 %d 元。" % ("、".join(str(v) for v in vals), t))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def enough():
        it, p = R.choice(ITEMS)
        vals = sorted([R.choice([1, 5, 10, 50]) for _ in range(R.randint(2, 5))], reverse=True)
        t = sum(vals)
        if t == p:
            return None
        q = "%s %d 元。下面的錢夠不夠買？" % (it, p) + P.money_svg(vals)
        ans = "夠" if t >= p else "不夠"
        return mcq(q, ans, ["不夠" if ans == "夠" else "夠", "剛好一樣", "不知道"], "錢一共 %d 元，%d %s %d，所以%s。" % (t, t, "＞" if t > p else "＜", p, ans))

    def pay():
        it, p = R.choice(ITEMS)
        f, r = divmod(p, 10)
        fives, ones = divmod(r, 5)
        parts = []
        if f >= 5:
            parts.append("1 個 50 元")
            f -= 5
        if f:
            parts.append("%d 個 10 元" % f)
        if fives:
            parts.append("1 個 5 元")
        if ones:
            parts.append("%d 個 1 元" % ones)
        ans = "、".join(parts)
        q = "%s %d 元。剛好付 %d 元，可以怎麼拿？" % (it, p, p)
        w = ["%d 個 10 元" % (p // 10 + 1), "%d 個 5 元" % (p // 5 + 1), "%d 個 1 元、%d 個 10 元" % (p % 10 + 1, p // 10) if p >= 10 else "%d 個 1 元" % (p + 1)]
        return mcq(q, ans, w, "%s，合起來剛好 %d 元。" % (ans, p))
    return pick_unique(R, enough, 10, seen) + pick_unique(R, pay, 10, seen)


def s5(seen):
    def change():
        it, p = R.choice(ITEMS)
        paid = 10 if p < 10 else 50 if p < 50 else 100
        if R.random() < .3 and p < 50:
            paid = 100
        who = NM.next()
        q = "%s買%s %d 元，付了 %d 元，要找回多少元？" % (who, it, p, paid)
        v = paid - p
        return mcq(q, "%d 元" % v, ["%d 元" % x for x in (paid + p if paid + p <= 200 else v + 10, v + 10, v - 1 if v > 1 else v + 1)], "%d － %d ＝ %d。" % (paid, p, v))

    def two():
        (a, pa), (b, pb) = R.sample(ITEMS, 2)
        if pa + pb > 100:
            return None
        q = "買一個%s %d 元和一個%s %d 元，一共要付多少元？" % (a, pa, b, pb)
        return mcq(q, "%d 元" % (pa + pb), ["%d 元" % x for x in (abs(pa - pb) if pa != pb else pa, pa + pb + 10, pa + pb - 1)], "%d ＋ %d ＝ %d。" % (pa, pb, pa + pb))
    return pick_unique(R, change, 12, seen) + pick_unique(R, two, 8, seen)


def main():
    seen = set()
    sets = [("數硬幣", s1(seen)), ("換錢", s2(seen)), ("數一數有多少錢", s3(seen)),
            ("付錢", s4(seen)), ("買東西和找錢", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["台灣的錢有 <b>1 元、5 元、10 元、50 元</b>硬幣，和 <b>100 元</b>紙鈔。" + P.money_svg([1, 5, 10, 50, 100]),
         "數錢時<b>先數大的</b>：50、60、65、66 ……",
         "<b>換錢</b>：1 個 10 元 ＝ 2 個 5 元 ＝ 10 個 1 元；1 個 50 元 ＝ 5 個 10 元。",
         "<b>找錢</b>：付的錢 － 東西的價錢。"],
        [example("1 個 10 元、2 個 5 元、3 個 1 元", ["10、15、20、21、22、23。"], "23 元"),
         example("麵包 25 元，付 50 元，找多少？", ["50 － 25。"], "25 元")],
        [("3 個硬幣就是 3 元", "要看每個硬幣是幾元"),
         ("5 元硬幣當 1 元數", "5 元要一次數 5"),
         ("找錢時用加法", "找錢是付的錢減價錢")])
    faq = [{"q": "一年級要認識哪些錢？",
            "a": "108課綱 N-1-4：1 元、5 元、10 元、50 元、100 元，以操作為主，學數錢、換錢、找錢。"},
           {"q": "怎麼在家練習？",
            "a": "準備真的硬幣玩買賣遊戲：先數大的，再換錢、付錢、找錢，孩子很快就會熟。"},
           {"q": "為什麼要先數大的錢？",
            "a": "先數大的，數的次數少、不容易出錯，例如 50 元先數，再 10 元、5 元、1 元。"}]
    make_unit(R, "grade-1", "money", "N-1-4",
              "解題：1元、5元、10元、50元、100元。以操作活動為主。數錢、換錢、找錢。",
              "認識錢幣：數錢、換錢、找錢",
              "一年級數學 認識錢幣 練習題｜1元5元10元50元・找錢 學習單（附解答）",
              "認識錢幣",
              "國小一年級數學「認識錢幣」免費學習單：數 1 元、5 元、10 元、50 元硬幣和 100 元紙鈔，換錢、付錢、夠不夠、買東西找錢。100題線上練習，題目短、圖多，附可列印解答。",
              "數錢先數大的",
              "1 個 10 元 ＝ 2 個 5 元 ＝ 10 個 1 元。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
