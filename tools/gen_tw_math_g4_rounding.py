# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：概數（四捨五入、無條件進入、無條件捨去）（108課綱 N-4-4）
  python3 tools/gen_tw_math_g4_rounding.py
四捨五入・無條件進入・無條件捨去で概數を作る、情境で方法を選ぶ、概數で估算（≈）、概數から元の數の範囲。
誤答：取る位の 1 つ下ではなく 2 つ下を見る、進位で上の位を変え忘れる、方法の取り違え。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(41005)
NM = Names(R)
PL = {100: "百位", 1000: "千位", 10000: "萬位", 100000: "十萬位"}


def rnd(n, k):
    return (n + k // 2) // k * k


def up(n, k):
    return -(-n // k) * k


def down(n, k):
    return n // k * k


def s1(seen):
    def mk():
        k = R.choice([100, 1000, 1000, 10000, 10000, 100000])
        n = R.randint(k * 2, k * 100 - 1) if k < 100000 else R.randint(200001, 9999999)
        if n % k < k // 10 or (n % k) // (k // 10) == 5 and R.random() < .5:
            return None
        a = rnd(n, k)
        other = up(n, k) if a == down(n, k) else down(n, k)
        k2 = k // 10
        return mcq("用四捨五入法，把 %s 取概數到<b>%s</b>是多少？" % (num(n), PL[k]), num(a),
                   [num(x) for x in (other, rnd(n, k2) if k2 >= 10 else a + k, rnd(n, k * 10), a + k, a - k, a + 2 * k) if x > 0],
                   "看%s的下一位（%s）是 %d，%s，所以是 %s。" % (
                       PL[k], PL.get(k2, "十位"), (n % k) // k2, "4 以下捨去" if (n % k) // k2 < 5 else "5 以上進位", num(a)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        k = R.choice([100, 1000, 10000])
        n = R.randint(k + 1, k * 100 - 1)
        if n % k == 0 or n % k < k // 10:
            return None
        way = R.choice(["無條件進入法", "無條件捨去法"])
        a = up(n, k) if way == "無條件進入法" else down(n, k)
        o = down(n, k) if way == "無條件進入法" else up(n, k)
        return mcq("用<b>%s</b>，把 %s 取概數到%s是多少？" % (way, num(n), PL[k]), num(a),
                   [num(x) for x in (o, rnd(n, k) if rnd(n, k) != a else a + k, a + k if way == "無條件進入法" else a - k, up(n, k // 10) if way == "無條件進入法" else down(n, k // 10), a + 2 * k, a - 2 * k) if x > 0],
                   "%s：%s後面的數%s，所以是 %s。" % (way, PL[k], "不管多少都進 1" if way == "無條件進入法" else "不管多少都捨去", num(a)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        kind = R.choice(["box", "bus", "buy", "pack", "money"])
        who = NM.next()
        if kind == "box":
            per = R.choice([12, 24, 36, 50, 100])
            n = R.randint(per + 1, per * 30)
            if n % per == 0:
                return None
            v = up(n, per) // per
            q = "每箱可以裝 %d 個蘋果，要把 %s 個蘋果全部裝箱，至少要幾箱？" % (per, num(n))
            right, way = "%d 箱" % v, "無條件進入法"
            w = ["%d 箱" % (v - 1), "%d 箱" % (v + 1), "%d 箱" % (v + 2)]
        elif kind == "bus":
            per = R.choice([40, 42, 45])
            n = R.randint(per * 2 + 1, per * 9)
            if n % per == 0:
                return None
            v = n // per + 1
            q = "%d 位學生去遠足，每輛車坐 %d 人，至少要幾輛車？" % (n, per)
            right, way = "%d 輛" % v, "無條件進入法"
            w = ["%d 輛" % (v - 1), "%d 輛" % (v + 1), "%d 輛" % (v + 2)]
        elif kind == "buy":
            p = R.choice([25, 35, 45, 120, 150])
            m = R.randint(p * 3 + 1, p * 30)
            if m % p == 0:
                return None
            v = m // p
            q = "%s有 %d 元，一個便當 %d 元，最多可以買幾個？" % (who, m, p)
            right, way = "%d 個" % v, "無條件捨去法"
            w = ["%d 個" % (v + 1), "%d 個" % (v - 1), "%d 個" % (v + 2)]
        elif kind == "pack":
            per = R.choice([6, 8, 12])
            n = R.randint(per * 5 + 1, per * 40)
            if n % per == 0:
                return None
            v = n // per
            q = "%d 顆雞蛋，每 %d 顆裝一盒賣，可以裝滿幾盒？" % (n, per)
            right, way = "%d 盒" % v, "無條件捨去法"
            w = ["%d 盒" % (v + 1), "%d 盒" % (v - 1), "%d 盒" % (v + 2)]
        else:
            n = R.randint(1001, 99999)
            if n % 1000 == 0:
                return None
            q = "%s的存款有 %s 元，要換成 1000 元鈔票，最多可以換幾張？" % (who, num(n))
            v = n // 1000
            right, way = "%d 張" % v, "無條件捨去法"
            w = ["%d 張" % (v + 1), "%d 張" % (v - 1) if v > 1 else "%d 張" % (v + 2), "%d 張" % (v + 2)]
        return mcq(q, right, w, "這裡要用%s：%s，答案是 %s。" % (way, "不夠的部分也要多一個才裝得下" if way == "無條件進入法" else "不夠一整個的部分不能算", right))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def add():
        a, b = R.randint(1100, 9900), R.randint(1100, 9900)
        if a % 1000 // 100 == 5 or b % 1000 // 100 == 5:
            return None
        op = R.choice(["＋", "－"])
        if op == "－" and a < b + 1000:
            return None
        ea, eb = rnd(a, 1000), rnd(b, 1000)
        e = ea + eb if op == "＋" else ea - eb
        if e <= 0:
            return None
        q = "用四捨五入法取概數到千位來估算：%s %s %s ≈ ？" % (num(a), op, num(b))
        w = [down(a, 1000) + down(b, 1000) if op == "＋" else down(a, 1000) - down(b, 1000), e + 1000, e - 1000, a + b if op == "＋" else a - b]
        return mcq(q, num(e), [num(x) for x in w if x > 0 and x != e],
                   "%s ≈ %s，%s ≈ %s，%s %s %s ＝ %s。「≈」讀作「約等於」。" % (num(a), num(ea), num(b), num(eb), num(ea), op, num(eb), num(e)))

    def mul():
        a, b = R.randint(110, 980), R.randint(11, 98)
        if a % 100 // 10 == 5 or b % 10 == 5:
            return None
        ea, eb = rnd(a, 100), rnd(b, 10)
        e = ea * eb
        q = "用四捨五入法，把 %d 取到百位、%d 取到十位來估算：%d × %d ≈ ？" % (a, b, a, b)
        return mcq(q, num(e), [num(x) for x in (down(a, 100) * down(b, 10), e * 10, e // 10, a * b) if x != e and x > 0],
                   "%d ≈ %d，%d ≈ %d，%d × %d ＝ %s。（真正的答案是 %s）" % (a, ea, b, eb, ea, eb, num(e), num(a * b)))
    return pick_unique(R, add, 12, seen) + pick_unique(R, mul, 8, seen)


def s5(seen):
    def range_q():
        k = R.choice([100, 1000, 10000])
        a = R.randint(2, 9) * k * R.choice([1, 10]) if k < 10000 else R.randint(2, 99) * k
        lo, hi = a - k // 2, a + k // 2 - 1
        ask = R.choice(["lo", "hi"])
        q = "一個整數用四捨五入法取概數到%s是 %s，這個數%s是多少？" % (PL[k], num(a), "最小" if ask == "lo" else "最大")
        v = lo if ask == "lo" else hi
        w = [lo - 1, hi + 1, a - k, a + k - 1, a - k // 2 + 1, a + k // 2] if ask == "lo" else [hi + 1, a + k // 2 - 2, lo, a + k - 1, a + k // 2]
        return mcq(q, num(v), [num(x) for x in w if x != v and x > 0],
                   "%s 到 %s 取概數都是 %s。%s是 %s。" % (num(lo), num(hi), num(a), "最小" if ask == "lo" else "最大", num(v)))

    def which():
        k = R.choice([1000, 10000])
        a = R.randint(2, 9) * k
        good = R.randint(a - k // 2, a + k // 2 - 1)
        bads = [a - k // 2 - R.randint(1, k // 4), a + k // 2 + R.randint(0, k // 4), a + k + R.randint(1, k // 3)]
        q = "下面哪一個數用四捨五入法取概數到%s是 %s？" % (PL[k], num(a))
        return mcq(q, num(good), [num(x) for x in bads], "%s 的%s下一位四捨五入後是 %s。" % (num(good), PL[k], num(a)))
    return pick_unique(R, range_q, 10, seen) + pick_unique(R, which, 10, seen)


def main():
    seen = set()
    sets = [("四捨五入法", s1(seen)), ("無條件進入法、無條件捨去法", s2(seen)), ("生活中要用哪一種？", s3(seen)),
            ("用概數估算", s4(seen)), ("原來的數是多少？", s5(seen))]
    body = lesson(
        ["取概數到某一位，看<b>下一位</b>：",
         "<b>四捨五入法</b>：下一位是 0〜4 就捨去，5〜9 就進 1。<b>無條件進入法</b>：後面只要不是 0 就進 1。<b>無條件捨去法</b>：後面全部捨去。",
         "東西要全部裝得下、人要全部坐得下 → 無條件進入；錢夠買幾個、能裝滿幾盒 → 無條件捨去。",
         "概數的計算用「≈」（約等於）。"],
        [example("把 38,462 取概數到千位", ["千位的下一位是百位 4。", "四捨五入：4 捨去 → 38,000。無條件進入 → 39,000。"], "38,000（四捨五入）"),
         example("每輛車坐 45 人，200 人至少要幾輛？", ["200 ÷ 45 ＝ 4……20。", "剩下 20 人也要坐車，用無條件進入。"], "5 輛")],
        [("取到千位卻看十位的數", "只看千位的下一位：百位"),
         ("38,962 取到千位寫成 38,000", "百位是 9，要進 1：39,000"),
         ("買東西的題目也進位", "錢不夠買一整個，要用無條件捨去")])
    faq = [{"q": "四捨五入、無條件進入、無條件捨去有什麼不同？",
            "a": "都是取概數的方法。四捨五入看下一位是否 5 以上；無條件進入只要後面不是 0 就進 1；無條件捨去不論後面是多少都捨去。"},
           {"q": "什麼時候用無條件進入法？",
            "a": "要「全部裝得下、坐得下」的時候，例如需要幾個箱子、幾輛車，不夠的部分也要再多一個。"},
           {"q": "四年級的概數要學什麼？",
            "a": "108課綱 N-4-4：在生活情境中對大數取概數，認識四捨五入、無條件進入、無條件捨去和約等於符號「≈」，並用概數估算。"}]
    make_unit(R, "grade-4", "rounding", "N-4-4",
              "解題：對大數取概數。具體生活情境。四捨五入法、無條件進入、無條件捨去。含運用概數做估算。近似符號「≈」的使用。",
              "概數：四捨五入、無條件進入、無條件捨去",
              "四年級數學 概數 練習題｜四捨五入・無條件進入・無條件捨去 學習單（附解答）",
              "概數",
              "國小四年級數學「概數」免費學習單：四捨五入法、無條件進入法、無條件捨去法，生活中要用哪一種、用概數估算和原來的數的範圍。100題線上練習馬上對答案，附可列印解答。",
              "取到哪一位，就看它的下一位",
              "裝得下、坐得下用進入；夠買幾個用捨去。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
