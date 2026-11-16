# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：基準量與比較量（108課綱 N-6-8）
  python3 tools/gen_tw_math_g6_base_and_compared_quantities.py
「A 是 B 的幾倍」で B が基準量・A が比較量、比較量＝基準量×比值、基準量＝比較量÷比值、交換基準（倒數）、增加・減少後の量・折扣。
誤答：基準量と比較量を取り違える、基準量を求めるのに×にする、交換基準で同じ比值のままにする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff, num, dnum

R = random.Random(61008)
NM = Names(R)


def frs(v):
    return ff(v, mixed=False) if v.denominator != 1 else num(v.numerator)


def rv():
    return F(R.randint(1, 9), R.choice([2, 3, 4, 5, 8]))


def s1(seen):
    PAIRS = [("哥哥的身高", "弟弟的身高"), ("蘋果的重量", "橘子的重量"), ("甲班的人數", "乙班的人數"), ("今天的雨量", "昨天的雨量"), ("書包的價錢", "鉛筆盒的價錢"), ("紅繩的長度", "藍繩的長度")]

    def mk():
        a, b = R.choice(PAIRS)
        if R.random() < .5:
            a, b = b, a
        v = rv()
        if v == 1:
            return None
        ask = R.choice(["base", "comp"])
        q = "「%s是%s的 %s 倍」，%s是什麼？" % (a, b, frs(v), "基準量" if ask == "base" else "比較量")
        ans = b if ask == "base" else a
        return mcq(q, ans, [a if ans == b else b, frs(v), "%s和%s的和" % (a[:2], b[:2])],
                   "「是誰的幾倍」的「誰」是基準量（%s），拿來比的是比較量（%s）。" % (b, a))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        v = rv()
        base = v.denominator * R.randint(2, 30)
        comp = base * v
        if comp.denominator != 1 or v == 1:
            return None
        who = NM.next()
        q = "%s有 %d 張貼紙，妹妹的貼紙是%s的 %s 倍。妹妹有幾張？" % (who, base, who, frs(v))
        return mcq(q, "%d 張" % comp, ["%s 張" % ff(x) for x in (F(base) / v, base + v, F(base, 1) * v + v.denominator)  if x != comp and x.denominator == 1] + ["%d 張" % (comp + base)],
                   "比較量 ＝ 基準量 × 比值：%d × %s ＝ %d（張）。" % (base, frs(v), comp))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        v = rv()
        base = v.denominator * R.randint(2, 30)
        comp = base * v
        if comp.denominator != 1 or v == 1:
            return None
        thing = R.choice([("一條紅繩", "藍繩", "公尺"), ("一袋綠豆", "紅豆", "公克"), ("今年的收入", "去年的收入", "萬元")])
        q = "%s長 %d %s，是%s的 %s 倍。%s有多少%s？" % (thing[0], comp, thing[2], thing[1], frs(v), thing[1], thing[2]) if thing[2] == "公尺" else \
            "%s是 %d %s，是%s的 %s 倍。%s是多少%s？" % (thing[0], comp, thing[2], thing[1], frs(v), thing[1], thing[2])
        w = [comp * v, comp + v.denominator, base + v.numerator]
        return mcq(q, "%d %s" % (base, thing[2]), ["%s %s" % (ff(x), thing[2]) for x in w if x != base], "基準量 ＝ 比較量 ÷ 比值：%d ÷ %s ＝ %d（%s）。" % (comp, frs(v), base, thing[2]))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        v = rv()
        if v == 1:
            return None
        a, b = R.choice([("甲", "乙"), ("姐姐", "妹妹"), ("大盒", "小盒"), ("大瓶", "小瓶")])
        q = "%s的重量是%s的 %s 倍，那麼%s的重量是%s的幾倍？" % (a, b, frs(v), b, a)
        inv = 1 / v
        return mcq(q, "%s 倍" % frs(inv), ["%s 倍" % frs(x) for x in (v, 1 - v if v < 1 else v - 1, v + 1)  if x != inv and x > 0] + ["%s 倍" % frs(inv + 1)],
                   "交換基準，比值變成倒數：%s 的倒數是 %s。" % (frs(v), frs(inv)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def sale():
        price = R.randint(4, 40) * 50
        off = R.choice([9, 8, 85, 75, 7, 6])
        rate = F(off, 10) if off < 10 else F(off, 100)
        pay = price * rate
        if pay.denominator != 1:
            return None
        label = "%d 折" % off
        q = "一件外套原價 %s 元，打 %s，要付多少元？" % (num(price), label)
        return mcq(q, "%s 元" % num(int(pay)), ["%s 元" % num(int(x)) for x in (price - price * rate, price * (1 - rate) + price if False else price - off * 10, pay + price // 10)  if x != pay and x > 0],
                   "打%s是原價的 %s：%s × %s ＝ %s（元）。" % (label.replace(" ", ""), dnum(float(rate), 2), num(price), dnum(float(rate), 2), num(int(pay))))

    def orig():
        rate = R.choice([F(8, 10), F(9, 10), F(3, 4), F(7, 10), F(85, 100)])
        orig_ = R.randint(4, 30) * 100
        pay = orig_ * rate
        if pay.denominator != 1:
            return None
        q = "一雙球鞋打折後賣 %s 元，是原價的 %s。原價是多少元？" % (num(int(pay)), dnum(float(rate), 2))
        return mcq(q, "%s 元" % num(orig_), ["%s 元" % num(int(x)) for x in (pay * rate, pay + pay * (1 - rate), pay * 2 - orig_ * rate + 100)  if x != orig_ and x > 0],
                   "原價是基準量：%s ÷ %s ＝ %s（元）。" % (num(int(pay)), dnum(float(rate), 2), num(orig_)))

    def grow():
        base = R.randint(4, 30) * 10
        inc = F(R.randint(1, 3), R.choice([4, 5, 10]))
        new = base * (1 + inc)
        if new.denominator != 1:
            return None
        q = "學校去年有 %d 位新生，今年比去年多了 %s。今年有幾位新生？" % (base, frs(inc))
        return mcq(q, "%d 位" % new, ["%s 位" % ff(x) for x in (base * inc, base + inc.numerator, base * (1 - inc))  if x != new and x.denominator == 1] + ["%d 位" % (new + base * inc)],
                   "今年是去年的 1 ＋ %s ＝ %s：%d × %s ＝ %d（位）。" % (frs(inc), frs(1 + inc), base, frs(1 + inc), new))
    return pick_unique(R, sale, 7, seen) + pick_unique(R, orig, 7, seen) + pick_unique(R, grow, 6, seen)


def main():
    seen = set()
    sets = [("找出基準量和比較量", s1(seen)), ("求比較量", s2(seen)), ("求基準量", s3(seen)),
            ("交換基準", s4(seen)), ("折扣和增減", s5(seen))]
    body = lesson(
        ["「A 是 B 的幾倍」：<b>B 是基準量</b>（當作 1 的量），A 是比較量。",
         "<b>比較量 ＝ 基準量 × 比值</b>；<b>基準量 ＝ 比較量 ÷ 比值</b>。",
         "交換基準時，比值變成<b>倒數</b>：A 是 B 的 <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> 倍，B 就是 A 的 <span class='fr'><span class='fn'>4</span><span class='fd'>3</span></span> 倍。"],
        [example("紅繩長 12 公尺，是藍繩的 <span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> 倍，藍繩長幾公尺？", ["藍繩是基準量。", "12 ÷ <span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> ＝ 12 × <span class='fr'><span class='fn'>5</span><span class='fd'>3</span></span> ＝ 20。"], "20 公尺"),
         example("原價 800 元打 75 折，要付多少元？", ["75 折是原價的 <span class='fr'><span class='fn'>75</span><span class='fd'>100</span></span>。", "800 × 0.75 ＝ 600。"], "600 元")],
        [("求基準量用乘法", "基準量 ＝ 比較量 ÷ 比值"),
         ("A 是 B 的 3/4，以為 B 是 A 的 3/4", "交換基準要用倒數 4/3"),
         ("打 8 折就是少付 8 成", "打 8 折是付原價的 0.8，只少付 2 成")])
    faq = [{"q": "怎麼分辨基準量和比較量？",
            "a": "看「是誰的幾倍」，「誰」就是基準量，也就是被當作 1 的量；另一個是比較量。"},
           {"q": "打 8 折是什麼意思？",
            "a": "付原價的 8 成，也就是原價 × 0.8；打 75 折是原價 × 0.75。原價是基準量。"},
           {"q": "六年級的基準量與比較量要學什麼？",
            "a": "108課綱 N-6-8：比和比值的應用，用比較量 ＝ 基準量 × 比值解題，並理解交換基準時的關係。"}]
    make_unit(R, "grade-6", "base-and-compared-quantities", "N-6-8",
              "解題：基準量與比較量。比和比值的應用。含交換基準時之關係。",
              "基準量與比較量",
              "六年級數學 基準量與比較量 練習題｜比值・交換基準・打折 學習單（附解答）",
              "基準量與比較量",
              "國小六年級數學「基準量與比較量」免費學習單：找出基準量和比較量、求比較量、求基準量、交換基準（倒數）與打折、增加幾成的應用題。100題線上練習馬上對答案，附可列印解答。",
              "比較量 ＝ 基準量 × 比值",
              "「是誰的幾倍」的「誰」就是基準量。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
