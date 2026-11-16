# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：整數、小數除以整數（商為小數）（108課綱 N-5-9）
  python3 tools/gen_tw_math_g5_dividing_decimals.py
整數÷整數で商が小數、小數÷整數の直式、除不盡は四捨五入で概數、分母 2・4・5・8 の分數を小數に、應用問題。
誤答：商の小數點の位置ずれ、商の 0（0.0x）を落とす、餘數で止める、1/8 を 0.8 とする。
"""
import random
from decimal import Decimal as Dm, ROUND_HALF_UP
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, num

R = random.Random(51010)
NM = Names(R)


def D(x):
    s = format(Dm(x).normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    i, _, f = s.partition(".")
    return num(int(i)) + ("." + f if f else "")


def term(a, b):
    return Dm(a) / Dm(b)


def s1(seen):
    def mk():
        b = R.choice([2, 4, 5, 8, 20, 25])
        a = R.randint(1, 60)
        if a % b == 0:
            return None
        v = term(a, b)
        q = "%d ÷ %d ＝（算到除盡）" % (a, b)
        w = [D(v * 10), D(v / 10), "%d……%d" % (a // b, a % b), D(Dm(a // b) + Dm(a % b) / 10)]
        return mcq(q, D(v), [x for x in w if x != D(v)] + [D(v + 1)], "除到個位還有餘數，就在被除數後面補 0 繼續除，商要點上小數點：%d ÷ %d ＝ %s。" % (a, b, D(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.randint(2, 9)
        q_ = Dm(R.randint(11, 999)) / Dm(100) if R.random() < .6 else Dm(R.randint(11, 99)) / Dm(10)
        x = q_ * n
        v = q_
        if (x * 100) % 1:
            return None
        q = "%s ÷ %d ＝" % (D(x), n)
        w = [D(v * 10), D(v / 10), D(v + Dm("0.1"))]
        s_ = str(v)
        if "0" in s_.split(".")[-1][:1] or (v < 1 and "." in s_):
            w.append(D(Dm(s_.replace(".0", "."))) if ".0" in s_ else D(v + Dm("0.01")))
        return mcq(q, D(v), w, "直式除法：商的小數點要和被除數的小數點對齊：%s ÷ %d ＝ %s。" % (D(x), n, D(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(1, 50), R.choice([3, 6, 7, 9, 11, 12])
        if a % b == 0 or term(a, b).as_tuple().exponent > -6 and (Dm(a) * 1000 / b) % 1 == 0:
            return None
        place = R.choice([("十分位", "0.1"), ("百分位", "0.01")])
        v = term(a, b).quantize(Dm(place[1]), rounding=ROUND_HALF_UP)
        down = (term(a, b) / Dm(place[1])).to_integral_value(rounding="ROUND_DOWN") * Dm(place[1])
        q = "%d ÷ %d 除不盡，用四捨五入法取到<b>%s</b>，商是多少？" % (a, b, place[0])
        w = [D(down) if down != v else D(v + Dm(place[1])), D(term(a, b).quantize(Dm("0.001"), rounding=ROUND_HALF_UP)), D(v * 10), D(v + Dm(place[1]))]
        return mcq(q, D(v), [x for x in w if x != D(v)], "多除一位再四捨五入：%d ÷ %d ＝ %s…，取到%s是 %s。" % (a, b, D(term(a, b).quantize(Dm("0.0001"), rounding="ROUND_DOWN")), place[0], D(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    PAIRS = [(1, 2, "0.5"), (1, 4, "0.25"), (3, 4, "0.75"), (1, 5, "0.2"), (2, 5, "0.4"), (3, 5, "0.6"), (4, 5, "0.8"),
             (1, 8, "0.125"), (3, 8, "0.375"), (5, 8, "0.625"), (7, 8, "0.875")]

    def mk():
        a, b, d = R.choice(PAIRS)
        if R.random() < .5:
            w = {"0.125": ["0.8", "0.18", "1.25"], "0.375": ["0.38", "3.8", "0.83"], "0.625": ["0.58", "6.25", "0.65"], "0.875": ["0.78", "8.75", "0.87"],
                 "0.25": ["0.4", "0.14", "2.5"], "0.75": ["0.34", "0.7", "7.5"], "0.5": ["0.2", "0.12", "5"]}.get(d, ["0.%d" % b, "%d.%d" % (a, b), D(Dm(d) * 10)])
            return mcq("%s 化成小數是多少？" % fr(a, b), d, w, "%s ＝ %d ÷ %d ＝ %s。" % (fr(a, b), a, b, d))
        return mcq("%s 化成最簡分數是多少？" % d, fr(a, b), [fr(int(Dm(d) * 100), 100) if len(d) == 4 else fr(int(Dm(d) * 1000), 1000) if len(d) == 5 else fr(int(Dm(d) * 10), 10), fr(b, a) if a > 1 else fr(1, b + 1), fr(a, b * 10)],
                   "%s 化成分數再約分：%s。" % (d, fr(a, b)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        kind = R.choice(["share", "avg", "price"])
        n = R.choice([4, 5, 8]) if kind != "price" else R.choice([3, 6, 7])
        if kind == "share":
            a = R.randint(3, 30)
            if a % n == 0:
                return None
            q = "%d 公升的水平均倒進 %d 個水壺，每壺幾公升？" % (a, n)
            v = term(a, n)
            u = "公升"
            e = "%d ÷ %d ＝ %s（公升）。" % (a, n, D(v))
        elif kind == "avg":
            x = Dm(R.randint(11, 99)) / 10 + Dm(R.randint(0, 9)) / 100
            x = x * n
            v = x / n
            if (v * 100) % 1:
                return None
            q = "%s %d 天一共跑了 %s 公里，平均每天跑幾公里？" % (NM.next(), n, D(x))
            u = "公里"
            e = "%s ÷ %d ＝ %s（公里）。" % (D(x), n, D(v))
        else:
            tot = R.randint(100, 500)
            if tot % n == 0:
                return None
            q = "%d 個一樣的麵包一共 %d 元，一個大約多少元？（四捨五入取到整數）" % (n, tot)
            v = term(tot, n).quantize(Dm("1"), rounding=ROUND_HALF_UP)
            u = "元"
            e = "%d ÷ %d ＝ %s…，四捨五入取到整數是 %s 元。" % (tot, n, D(term(tot, n).quantize(Dm("0.01"), rounding="ROUND_DOWN")), D(v))
        return mcq(q, D(v) + " " + u, [D(v * 10) + " " + u, D(v / 10) + " " + u, D(v + 1) + " " + u], e)
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("整數 ÷ 整數，商是小數", s1(seen)), ("小數 ÷ 整數", s2(seen)), ("除不盡取概數", s3(seen)),
            ("分數化成小數", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["整數除以整數有餘數時，可以在被除數後面<b>補 0 繼續除</b>，商就是小數：7 ÷ 4 ＝ 1.75。",
         "小數除以整數：直式中，<b>商的小數點和被除數的小數點對齊</b>。不夠商 1 的位要寫 0。",
         "除不盡時，用<b>四捨五入</b>取到需要的位數：要取到十分位，就算到百分位再四捨五入。",
         "記住常用的：%s ＝ 0.5，%s ＝ 0.25，%s ＝ 0.2，%s ＝ 0.125。" % (fr(1, 2), fr(1, 4), fr(1, 5), fr(1, 8))],
        [example("7 ÷ 4 ＝", ["7 ÷ 4 ＝ 1……3，補 0：30 ÷ 4 ＝ 7……2。", "再補 0：20 ÷ 4 ＝ 5。"], "1.75"),
         example("0.36 ÷ 4 ＝", ["36 ÷ 4 ＝ 9，小數點對齊。", "十分位不夠商，寫 0。"], "0.09")],
        [("7 ÷ 4 只寫 1……3", "要求小數時，補 0 繼續除：1.75"),
         ("0.36 ÷ 4 ＝ 0.9", "十分位要寫 0：0.09"),
         ("%s ＝ 0.8" % fr(1, 8), "%s ＝ 1 ÷ 8 ＝ 0.125" % fr(1, 8))])
    faq = [{"q": "整數除以整數怎麼得到小數？",
            "a": "除到個位還有餘數時，在被除數後面補 0 繼續除，商的個位後面點上小數點。例如 7 ÷ 4 ＝ 1.75。"},
           {"q": "除不盡怎麼辦？",
            "a": "用四捨五入取概數。要取到十分位，就先算到百分位，再看百分位四捨五入。"},
           {"q": "五年級的小數除法要學什麼？",
            "a": "108課綱 N-5-9：整數除以整數（商為小數）、小數除以整數，用概數處理除不盡，並熟悉分母是 2、4、5、8 的分數對應的小數。"}]
    make_unit(R, "grade-5", "dividing-decimals", "N-5-9",
              "整數、小數除以整數（商為小數）：整數除以整數（商為小數）、小數除以整數的意義。教師用位值的概念說明直式計算的合理性。能用概數協助處理除不盡的情況。熟悉分母為 2、4、5、8 之真分數所對應的小數。",
              "小數除以整數：商是小數",
              "五年級數學 小數除法 練習題｜商是小數・除不盡取概數・分數化小數 學習單（附解答）",
              "小數除以整數",
              "國小五年級數學「小數除以整數」免費學習單：整數除以整數商是小數、小數除以整數的直式、除不盡取概數、分數化成小數與應用題。100題線上練習馬上對答案，附可列印解答。",
              "商的小數點和被除數對齊",
              "除不盡時，多算一位再四捨五入。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
