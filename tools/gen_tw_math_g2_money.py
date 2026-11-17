# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：錢幣（100 元、500 元、1000 元）（108課綱 N-2-5）
  python3 tools/gen_tw_math_g2_money.py
紙鈔と硬幣を數える（1000 元以內）、換錢（1000 ＝ 2 張 500 ＝ 10 張 100）、ちょうど付ける最少の枚數、買い物の合計と找錢。
誤答：枚數を金額にする、500 元を 100 元として數える、找錢で足してしまう。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81306)
NM = Names(R)
ITEMS = [("故事書", 180), ("書包", 450), ("球鞋", 690), ("玩具", 320), ("便當", 85), ("帽子", 250), ("雨傘", 199), ("水壺", 365), ("拼圖", 275), ("文具組", 128), ("外套", 780), ("桌遊", 560)]


def s1(seen):
    def mk():
        vals = [500] * R.randint(0, 1) + [100] * R.randint(0, 4) + [50] * R.randint(0, 1) + [10] * R.randint(0, 3) + [5] * R.randint(0, 1) + [1] * R.randint(0, 3)
        t = sum(vals)
        if len(vals) < 4 or t > 1000 or len(vals) > 9:
            return None
        q = "一共是多少元？" + P.money_svg(vals)
        return mcq(q, "%d 元" % t, ["%d 元" % x for x in (len(vals), t - 100 if t > 100 else t + 50, t + 100, t + 10)][:3], "先數大的：%s，一共 %d 元。" % ("、".join(str(v) for v in vals), t))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    PAIRS = [(1000, 500), (1000, 100), (500, 100), (500, 50), (100, 10), (100, 50), (1000, 50)]

    def mk():
        big, small = R.choice(PAIRS)
        k = R.randint(1, 3) if big < 1000 else 1
        if big * k > 1000:
            return None
        n = big * k // small
        cw = lambda v: "張" if v >= 100 else "個"
        q = "%d %s %d 元可以換幾%s %d 元？" % (k, cw(big), big, cw(small), small)
        return mcq(q, "%d %s" % (n, cw(small)), ["%d %s" % (x, cw(small)) for x in (big // 10 if big // 10 != n else n + 5, n + 1, n * 2) if x != n], "%d 元是 %d %s %d 元。" % (big * k, n, cw(small), small))
    def rev():
        big, small = R.choice(PAIRS)
        n = big // small
        cw = lambda v: "張" if v >= 100 else "個"
        q = "幾%s %d 元可以換 1 %s %d 元？" % (cw(small), small, cw(big), big)
        return mcq(q, "%d %s" % (n, cw(small)), ["%d %s" % (x, cw(small)) for x in (n + 1, n * 2, n - 1 if n > 2 else n + 3)], "%d 個 %d 元合起來是 %d 元。" % (n, small, big))
    return pick_unique(R, mk, 13, seen) + pick_unique(R, rev, 7, seen)


def s3(seen):
    def mk():
        p = R.randint(110, 990)
        parts = []
        r = p
        for v, w in ((500, "張"), (100, "張"), (50, "個"), (10, "個"), (5, "個"), (1, "個")):
            c, r = divmod(r, v)
            if c:
                parts.append("%d %s %d 元" % (c, w, v))
        q = "要剛好付 %d 元，用最少張數（個數）的錢，要怎麼拿？" % p
        ans = "、".join(parts)
        w = ["%d 張 100 元、%d 個 1 元" % (p // 100, p % 100) if p % 100 else "%d 個 10 元" % (p // 10), ("%d 張 100 元、%d 個 10 元、%d 個 1 元" % (p // 100, p % 100 // 10, p % 10)).replace("、0 個 1 元", "").replace("、0 個 10 元", ""), "%d 張 500 元" % (p // 500 + 1)]
        return mcq(q, ans, [x for x in w if x != ans] + ["%d 張 100 元" % (p // 100 + 1)], "先拿最大的：%s。" % ans)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def two():
        (a, pa), (b, pb) = R.sample(ITEMS, 2)
        if pa + pb > 1000:
            return None
        q = "買一個%s %d 元和一個%s %d 元，一共要多少元？" % (a, pa, b, pb)
        s = pa + pb
        return mcq(q, "%d 元" % s, ["%d 元" % x for x in (abs(pa - pb), s + 100, s - 10)], "%d ＋ %d ＝ %d。" % (pa, pb, s))

    def enough():
        (a, pa), (b, pb) = R.sample(ITEMS, 2)
        money = R.choice([500, 1000])
        s = pa + pb
        if s == money:
            return None
        who = NM.next()
        q = "%s帶了 %d 元，想買%s（%d 元）和%s（%d 元），錢夠嗎？" % (who, money, a, pa, b, pb)
        ok = s <= money
        return mcq(q, "夠" if ok else "不夠", ["不夠" if ok else "夠", "剛好", "不知道"], "%d ＋ %d ＝ %d，%d %s %d，所以%s。" % (pa, pb, s, s, "＜" if ok else "＞", money, "夠" if ok else "不夠"))
    return pick_unique(R, two, 10, seen) + pick_unique(R, enough, 10, seen)


def s5(seen):
    def mk():
        it, p = R.choice(ITEMS)
        paid = 100 if p < 100 else 500 if p < 500 else 1000
        if R.random() < .4 and p < 500:
            paid = 1000
        k = 1
        if p * k > paid:
            return None
        who = NM.next()
        q = "%s買 %d %s%s，每%s %d 元，付了 %d 元，要找回多少元？" % (who, k, "個" if it not in ("故事書", "雨傘") else "本" if it == "故事書" else "把", it, "個" if it not in ("故事書", "雨傘") else "本" if it == "故事書" else "把", p, paid) if k > 1 else "%s買%s %d 元，付了 %d 元，要找回多少元？" % (who, it, p, paid)
        cost = p * k
        v = paid - cost
        return mcq(q, "%d 元" % v, ["%d 元" % x for x in (paid - p if k > 1 else paid + p, v + 100, v + 10)], ("%d ＋ %d ＝ %d，" % (p, p, cost) if k > 1 else "") + "%d － %d ＝ %d。" % (paid, cost, v))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("數錢", s1(seen)), ("換錢", s2(seen)), ("怎麼付最少張", s3(seen)),
            ("買東西", s4(seen)), ("找錢", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["紙鈔有 <b>100 元、500 元、1000 元</b>。" + P.money_svg([1000, 500, 100]),
         "<b>1000 元 ＝ 2 張 500 元 ＝ 10 張 100 元</b>；500 元 ＝ 5 張 100 元。",
         "數錢先數大的；付錢先拿大的；找錢 ＝ 付的錢 － 價錢。"],
        [example("1 張 500 元、2 張 100 元、3 個 10 元", ["500、600、700、710、720、730。"], "730 元"),
         example("買 365 元的水壺，付 500 元，找多少？", ["500 － 365。"], "135 元")],
        [("5 張紙鈔就是 5 元", "看每張是多少元"),
         ("找錢用加法", "找錢用減法：付的 － 價錢"),
         ("付 280 元拿 28 張 10 元", "先拿大的：2 張 100 元、1 個 50 元、3 個 10 元")])
    faq = [{"q": "二年級要認識哪些錢？",
            "a": "108課綱 N-2-5：100 元、500 元、1000 元，以操作為主兼及計算，學數錢、換錢、找錢。"},
           {"q": "為什麼付錢要先拿大的？",
            "a": "先拿大面額，張數和個數最少，也比較不容易數錯。"},
           {"q": "怎麼練找錢？",
            "a": "玩商店遊戲，孩子當店員，用「從價錢往上數到付的錢」或減法找錢。"}]
    make_unit(R, "grade-2", "money", "N-2-5",
              "解題：100元、500元、1000元。以操作活動為主兼及計算。數錢、換錢、找錢。",
              "錢幣：100 元、500 元、1000 元",
              "二年級數學 錢幣 練習題｜100元500元1000元・換錢找錢 學習單（附解答）",
              "錢幣",
              "國小二年級數學「錢幣」免費學習單：數紙鈔和硬幣、1000 元和 500 元換錢、用最少張數付錢、買東西夠不夠、找錢。100題線上練習，附可列印解答。",
              "1000 元 ＝ 2 張 500 元 ＝ 10 張 100 元",
              "付錢先拿大的；找錢 ＝ 付的錢 － 價錢。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
