# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：三角形與四邊形的性質（108課綱 S-5-1）
  python3 tools/gen_tw_math_g5_triangle_and_quadrilateral_properties.py
三角形の內角和 180 度（第三の角）、等腰・正三角形・直角三角形での角、兩邊和大於第三邊、平行四邊形の對邊・對角、四邊形の內角和 360 度。
誤答：180 から 1 つしか引かない、兩邊和＝第三邊でも作れると思う、平行四邊形の隣の角を等しいとする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names

R = random.Random(51017)
NM = Names(R)
LET = "甲乙丙丁"


def s1(seen):
    def mk():
        a, b = R.randint(20, 110), R.randint(20, 110)
        c = 180 - a - b
        if c < 10:
            return None
        return mcq("三角形的兩個角是 %d 度和 %d 度，第三個角是幾度？" % (a, b), "%d 度" % c, ["%d 度" % x for x in (180 - a, 360 - a - b, 90 - a if a < 90 else c + 10, a + b) if x != c and x > 0],
                   "三角形三個內角的和是 180 度：180 － %d － %d ＝ %d（度）。" % (a, b, c))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def iso_top():
        base = R.randint(25, 80)
        top = 180 - 2 * base
        return mcq("等腰三角形的一個底角是 %d 度，頂角是幾度？" % base, "%d 度" % top, ["%d 度" % x for x in (180 - base, base, 90 - base, top + 10) if x != top and x > 0], "兩個底角一樣大：180 － %d × 2 ＝ %d（度）。" % (base, top))

    def iso_base():
        top = R.choice(range(20, 161, 2))
        b = (180 - top) // 2
        return mcq("等腰三角形的頂角是 %d 度，一個底角是幾度？" % top, "%d 度" % b, ["%d 度" % x for x in (180 - top, top, 90 - top if top < 90 else b + 10, b + 5) if x != b and x > 0], "（180 － %d）÷ 2 ＝ %d（度）。" % (top, b))

    def right():
        a = R.randint(10, 80)
        return mcq("直角三角形的一個銳角是 %d 度，另一個銳角是幾度？" % a, "%d 度" % (90 - a), ["%d 度" % x for x in (180 - a, 180 - 90 - a + 10, a, 270 - a) if x != 90 - a], "直角是 90 度，另外兩個角合起來是 90 度：90 － %d ＝ %d（度）。" % (a, 90 - a))

    def eq():
        return mcq("正三角形的每一個角是幾度？", "60 度", ["90 度", "45 度", "180 度"], "三個角一樣大：180 ÷ 3 ＝ 60（度）。")
    out = pick_unique(R, iso_top, 7, seen) + pick_unique(R, iso_base, 6, seen) + pick_unique(R, right, 6, seen)
    e = eq()
    seen.add(e["q"])
    return out + [e]


def s3(seen):
    def mk():
        a, b = R.randint(2, 12), R.randint(2, 12)
        kind = R.choice(["ok", "eq", "no", "ok"])
        if kind == "ok":
            c = R.randint(abs(a - b) + 1, a + b - 1)
        elif kind == "eq":
            c = a + b
        else:
            c = a + b + R.randint(1, 5)
        sides = sorted([a, b, c])
        can = sides[0] + sides[1] > sides[2]
        q = "三條邊長 %d 公分、%d 公分、%d 公分，能不能圍成三角形？" % tuple(R.sample([a, b, c], 3))
        return mcq(q, "能" if can else "不能", ["不能" if can else "能", "要看是什麼角", "只能圍成直角三角形"],
                   "看兩條短邊的和：%d ＋ %d ＝ %d，%s最長邊 %d，%s。（兩邊和要大於第三邊）" % (sides[0], sides[1], sides[0] + sides[1], "大於" if can else ("等於" if sides[0] + sides[1] == sides[2] else "小於"), sides[2], "能圍成" if can else "不能圍成"))

    def third():
        a, b = sorted(R.sample(range(3, 15), 2))
        q = "三角形兩邊長 %d 公分和 %d 公分，第三邊可能是幾公分？" % (a, b)
        good = R.randint(b - a + 1, a + b - 1)
        bads = [a + b, b - a, a + b + R.randint(1, 4)]
        return mcq(q, "%d 公分" % good, ["%d 公分" % x for x in bads if x > 0] + ["%d 公分" % (a + b + 5)], "第三邊要比 %d － %d ＝ %d 大，比 %d ＋ %d ＝ %d 小。" % (b, a, b - a, a, b, a + b))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, third, 8, seen)


def s4(seen):
    def para():
        a = R.randint(40, 140)
        if a == 90:
            return None
        kind = R.choice(["opp", "adj"])
        if kind == "opp":
            return mcq("平行四邊形的一個角是 %d 度，它的對角是幾度？" % a, "%d 度" % a, ["%d 度" % x for x in (180 - a, 360 - a, 90)], "平行四邊形的對角相等：%d 度。" % a)
        return mcq("平行四邊形的一個角是 %d 度，和它相鄰的角是幾度？" % a, "%d 度" % (180 - a), ["%d 度" % x for x in (a, 360 - a, 90 - a if a < 90 else a - 90)], "平行四邊形相鄰的兩個角合起來是 180 度：180 － %d ＝ %d（度）。" % (a, 180 - a))

    def side():
        a, b = R.randint(3, 20), R.randint(3, 20)
        if a == b:
            return None
        q = "平行四邊形相鄰兩邊是 %d 公分和 %d 公分，周長是幾公分？" % (a, b)
        return mcq(q, "%d 公分" % (2 * (a + b)), ["%d 公分" % x for x in (a + b, a * b, 4 * a)], "平行四邊形對邊相等：（%d ＋ %d）× 2 ＝ %d（公分）。" % (a, b, 2 * (a + b)))

    def quad():
        a, b, c = R.randint(60, 120), R.randint(60, 120), R.randint(60, 120)
        d = 360 - a - b - c
        if not 30 < d < 170:
            return None
        return mcq("四邊形的三個角是 %d 度、%d 度、%d 度，第四個角是幾度？" % (a, b, c), "%d 度" % d, ["%d 度" % x for x in (180 - (a + b + c) % 180, d + 10, 360 - a - b, abs(180 - a - b - c) + 10) if x != d and x > 0],
                       "四邊形可以分成兩個三角形，內角和是 360 度：360 － %d － %d － %d ＝ %d（度）。" % (a, b, c, d))
    return pick_unique(R, para, 8, seen) + pick_unique(R, side, 5, seen) + pick_unique(R, quad, 7, seen)


TRUE = ["三角形三個內角的和是 180 度。", "三角形任意兩邊的和大於第三邊。", "平行四邊形的對邊相等。", "平行四邊形的對角相等。", "四邊形四個內角的和是 360 度。", "一個三角形最多只有一個直角。"]
FALSE = ["三角形可以有兩個鈍角。", "長 3、4、7 公分的三條邊可以圍成三角形。", "平行四邊形相鄰的兩個角一定相等。", "三角形越大，內角和越大。", "四邊形的內角和是 180 度。", "等腰三角形的頂角一定等於底角。"]


def s5(seen):
    def mk():
        ok = R.random() < .5
        ans = R.choice(TRUE if ok else FALSE)
        st = R.sample(FALSE if ok else TRUE, 3) + [ans]
        R.shuffle(st)
        k = st.index(ans)
        q = "下面哪一句話是<b>%s</b>的？<br>%s" % ("對" if ok else "錯", "<br>".join("%s：%s" % (LET[i], t) for i, t in enumerate(st)))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s：%s三角形內角和 180 度、兩邊和大於第三邊；平行四邊形對邊相等、對角相等；四邊形內角和 360 度。" % (LET[k], ans))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("三角形的內角和", s1(seen)), ("特別三角形的角", s2(seen)), ("兩邊和大於第三邊", s3(seen)), ("平行四邊形和四邊形", s4(seen)), ("性質的判斷", s5(seen))]
    body = lesson(
        ["<b>三角形三個內角的和是 180 度</b>（把三個角剪下來拼在一起，剛好是一個平角）。",
         "<b>三角形任意兩邊的和大於第三邊</b>，不然圍不起來。",
         "<b>平行四邊形</b>：對邊相等、對角相等，相鄰兩角合起來 180 度。<b>四邊形</b>內角和是 360 度。"],
        [example("三角形兩個角是 48 度和 75 度，第三個角？", ["180 － 48 － 75 ＝ 57。"], "57 度"),
         example("3、4、8 公分能圍成三角形嗎？", ["3 ＋ 4 ＝ 7，比 8 小。"], "不能")],
        [("第三個角 ＝ 180 － 一個角", "兩個已知的角都要減"),
         ("3、4、7 公分可以圍成三角形", "3 ＋ 4 ＝ 7，等於第三邊，會壓成一直線，不能圍成"),
         ("平行四邊形相鄰的角相等", "是對角相等；相鄰兩角合起來 180 度")])
    faq = [{"q": "為什麼三角形內角和是 180 度？",
            "a": "把三角形的三個角剪下來，頂點對在一起拼起來，剛好成一直線，也就是一個平角 180 度。"},
           {"q": "怎麼判斷三條線段能不能圍成三角形？",
            "a": "看兩條較短的邊加起來是否大於最長的邊；大於才能圍成，等於或小於都不行。"},
           {"q": "五年級的三角形、四邊形性質要學什麼？",
            "a": "108課綱 S-5-1：三角形三內角和為 180 度、任意兩邊和大於第三邊，以及平行四邊形對邊相等、對角相等。"}]
    make_unit(R, "grade-5", "triangle-and-quadrilateral-properties", "S-5-1",
              "三角形與四邊形的性質：操作活動與簡單推理。含三角形三內角和為 180 度。三角形任意兩邊和大於第三邊。平行四邊形的對邊相等、對角相等。",
              "三角形與四邊形的性質：內角和",
              "五年級數學 三角形內角和 練習題｜180度・兩邊和大於第三邊・平行四邊形 學習單（附解答）",
              "內角和與三角形的性質",
              "國小五年級數學「三角形與四邊形的性質」免費學習單：三角形內角和180度、等腰和直角三角形的角、兩邊和大於第三邊、平行四邊形對邊對角和四邊形內角和360度。100題線上練習馬上對答案，附可列印解答。",
              "三角形內角和 180 度",
              "兩邊和大於第三邊；四邊形內角和 360 度。",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
