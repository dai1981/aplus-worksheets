# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：立方公尺、容量與容積（108課綱 N-5-14、N-5-15）
  python3 tools/gen_tw_math_g5_volume_and_capacity.py
立方公尺の量感と計算、1 公升＝1000 立方公分・1 毫升＝1 立方公分、容器の容積（內部の長さ）、水位の上昇で物の體積を求める（排水法）、應用。
誤答：1 公升＝100 立方公分、外側の長さで容積を計算、水位差でなく水位そのものを使う。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, dnum

R = random.Random(51015)
NM = Names(R)


def s1(seen):
    SENSE = [("一間教室的空間", "立方公尺"), ("一顆骰子", "立方公分"), ("一個貨櫃", "立方公尺"), ("一塊橡皮擦", "立方公分"),
             ("一座游泳池裡的水", "立方公尺"), ("一個鉛筆盒", "立方公分"), ("一輛卡車的車廂", "立方公尺"), ("一盒面紙", "立方公分")]
    out = [mcq("%s的體積，用哪一個單位最合適？" % it, u, [x for x in ("立方公尺", "立方公分", "平方公尺", "公尺") if x != u], "大的用立方公尺，小的用立方公分：%s用「%s」。" % (it, u)) for it, u in SENSE]
    for o in out:
        seen.add(o["q"])

    def m3():
        a, b, c = R.randint(2, 12), R.randint(2, 10), R.randint(2, 6)
        a, b = max(a, b), min(a, b)
        q = "長 %d 公尺、寬 %d 公尺、高 %d 公尺的長方體空間，體積是多少立方公尺？" % (a, b, c)
        v = a * b * c
        return mcq(q, "%d 立方公尺" % v, ["%d 立方公尺" % x for x in (a * b, 2 * (a * b + b * c + a * c), a + b + c)] + ["%d 平方公尺" % v], "長 × 寬 × 高 ＝ %d × %d × %d ＝ %d（立方公尺）。" % (a, b, c, v))
    return out + pick_unique(R, m3, 12, seen)


def s2(seen):
    def mk():
        kind = R.choice(["L2cc", "cc2L", "ml"])
        if kind == "L2cc":
            n = R.randint(2, 30)
            return mcq("%d 公升 ＝ ___ 立方公分" % n, num(n * 1000), [num(n * 100), num(n * 10), num(n * 10000)], "1 公升 ＝ 1000 立方公分（邊長 10 公分的正方體），%d 公升 ＝ %s 立方公分。" % (n, num(n * 1000)))
        if kind == "cc2L":
            n = R.randint(11, 99) * 100
            return mcq("%s 立方公分 ＝ ___ 公升" % num(n), dnum(n / 1000, 1), [dnum(n / 100, 0), dnum(n / 10000, 2), num(n)], "1000 立方公分 ＝ 1 公升，%s ÷ 1000 ＝ %s。" % (num(n), dnum(n / 1000, 1)))
        n = R.randint(5, 900)
        return mcq("%d 毫升 ＝ ___ 立方公分" % n, str(n), [num(n * 10), num(n * 1000), dnum(n / 1000, 3)], "1 毫升 ＝ 1 立方公分，所以 %d 毫升 ＝ %d 立方公分。" % (n, n))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b, c = R.randint(10, 40), R.randint(10, 30), R.randint(10, 30)
        a, b = max(a, b), min(a, b)
        a, b = max(a, b), min(a, b)
        t = R.choice([1, 2])
        q = "一個長方體水箱，外面量長 %d 公分、寬 %d 公分、高 %d 公分，箱子的厚度是 %d 公分（上面沒有蓋子）。容積是多少立方公分？" % (a + 2 * t, b + 2 * t, c + t, t)
        v = a * b * c
        outer = (a + 2 * t) * (b + 2 * t) * (c + t)
        return mcq(q, "%s 立方公分" % num(v), ["%s 立方公分" % num(x) for x in (outer, a * b * (c - t), (a + t) * (b + t) * c)], "容積要用裡面的長度：長 %d、寬 %d、高 %d，%d × %d × %d ＝ %s（立方公分）。" % (a, b, c, a, b, c, num(v)))

    def liters():
        a, b, c = R.randint(2, 6) * 10, R.randint(2, 5) * 10, R.randint(2, 5) * 10
        a, b = max(a, b), min(a, b)
        q = "一個水族箱裡面長 %d 公分、寬 %d 公分、高 %d 公分，裝滿水是幾公升？" % (a, b, c)
        v = a * b * c
        return mcq(q, "%s 公升" % dnum(v / 1000, 1), ["%s 公升" % x for x in (num(v), dnum(v / 100, 0), dnum(v / 10000, 2))], "%d × %d × %d ＝ %s 立方公分 ＝ %s 公升。" % (a, b, c, num(v), dnum(v / 1000, 1)))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, liters, 10, seen)


def s4(seen):
    def mk():
        a, b = R.randint(10, 30), R.randint(10, 25)
        a, b = max(a, b), min(a, b)
        h0 = R.randint(5, 15)
        rise = R.randint(1, 6)
        v = a * b * rise
        q = "長方體水箱裡面長 %d 公分、寬 %d 公分，水深 %d 公分。放進一塊石頭沉到底，水深變成 %d 公分。石頭的體積是多少立方公分？" % (a, b, h0, h0 + rise)
        return mcq(q, "%s 立方公分" % num(v), ["%s 立方公分" % num(x) for x in (a * b * (h0 + rise), a * b * h0, a * b + rise)], "水上升了 %d － %d ＝ %d 公分，石頭的體積 ＝ 上升的水：%d × %d × %d ＝ %s（立方公分）。" % (h0 + rise, h0, rise, a, b, rise, num(v)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def pool():
        a, b, d = R.randint(10, 25), R.randint(5, 12), R.choice([1, 2])
        q = "一座游泳池長 %d 公尺、寬 %d 公尺，放水深 %d 公尺，要放多少立方公尺的水？" % (a, b, d)
        v = a * b * d
        return mcq(q, "%d 立方公尺" % v, ["%d 立方公尺" % x for x in (a * b, (a + b) * 2 * d, v * 10)], "%d × %d × %d ＝ %d（立方公尺）。" % (a, b, d, v))

    def bottles():
        a, b, c = R.randint(2, 5) * 10, R.randint(2, 4) * 10, R.randint(2, 4) * 10
        a, b = max(a, b), min(a, b)
        bot = R.choice([500, 600, 1000, 2000])
        v = a * b * c
        if v % bot:
            return None
        q = "一個水箱裡面長 %d 公分、寬 %d 公分、高 %d 公分。用 %d 毫升的水瓶裝水，要倒幾瓶才裝滿？" % (a, b, c, bot)
        return mcq(q, "%d 瓶" % (v // bot), ["%d 瓶" % x for x in (v // bot * 10, v // 1000, v // bot + 1)], "容積 %s 立方公分 ＝ %s 毫升，%s ÷ %d ＝ %d（瓶）。" % (num(v), num(v), num(v), bot, v // bot))

    def drink():
        cc = R.choice([250, 300, 350, 400, 500])
        n = R.randint(4, 12)
        q = "一杯飲料 %d 立方公分，%d 杯一共幾公升？" % (cc, n)
        v = cc * n
        return mcq(q, "%s 公升" % dnum(v / 1000, 2), ["%s 公升" % x for x in (num(v), dnum(v / 100, 1), dnum(v / 10000, 3))], "%d × %d ＝ %s 立方公分 ＝ %s 毫升 ＝ %s 公升。" % (cc, n, num(v), num(v), dnum(v / 1000, 2)))
    return pick_unique(R, pool, 7, seen) + pick_unique(R, bottles, 6, seen) + pick_unique(R, drink, 7, seen)


def main():
    seen = set()
    sets = [("立方公尺", s1(seen)), ("公升、毫升和立方公分", s2(seen)), ("容積", s3(seen)), ("用排水法求體積", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["邊長 1 公尺的正方體，體積是 <b>1 立方公尺</b>，用來量房間、貨櫃這種大的空間。",
         "邊長 10 公分的正方體裝滿水是 1 公升，所以 <b>1 公升 ＝ 1000 立方公分</b>，<b>1 毫升 ＝ 1 立方公分</b>。",
         "<b>容積</b>是容器裡面能裝多少，要用<b>裡面的長、寬、高</b>（外面的長度減去厚度）。",
         "把東西放進水裡，水上升的體積就是東西的體積。"],
        [example("裡面長 30、寬 20、高 25 公分的水箱，能裝幾公升？", ["30 × 20 × 25 ＝ 15,000 立方公分。", "15,000 ÷ 1000 ＝ 15。"], "15 公升"),
         example("長 20、寬 15 公分的水箱，放入石頭後水上升 3 公分，石頭體積？", ["20 × 15 × 3 ＝ 900。"], "900 立方公分")],
        [("1 公升 ＝ 100 立方公分", "1 公升 ＝ 1000 立方公分"),
         ("用外面的長度算容積", "要扣掉厚度，用裡面的長度"),
         ("排水法用放石頭後的水深去算", "只算上升的那一段")])
    faq = [{"q": "1 公升等於幾立方公分？",
            "a": "1 公升 ＝ 1000 立方公分，1 毫升 ＝ 1 立方公分。邊長 10 公分的正方體容器剛好裝 1 公升的水。"},
           {"q": "容積和體積有什麼不同？",
            "a": "體積是物體本身佔的空間；容積是容器裡面能裝多少，要用內部的長、寬、高計算。"},
           {"q": "五年級的容積要學什麼？",
            "a": "108課綱 N-5-14、N-5-15：認識立方公尺，理解容量、容積和體積的關係，知道液體體積的意義。"}]
    make_unit(R, "grade-5", "volume-and-capacity", "N-5-15",
              "解題：容積。容量、容積和體積間的關係。知道液體體積的意義。（含 N-5-14 體積：「立方公尺」。）",
              "容積與立方公尺：公升和立方公分",
              "五年級數學 容積 練習題｜立方公尺・公升和立方公分・排水法 學習單（附解答）",
              "容積與立方公尺",
              "國小五年級數學「容積與立方公尺」免費學習單：立方公尺的量感和計算、公升毫升和立方公分的換算、容器的容積、用排水法求體積與應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 公升 ＝ 1000 立方公分",
              "容積用裡面的長、寬、高；水上升的體積就是物體的體積。",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
