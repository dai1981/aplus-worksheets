# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：兩步驟應用問題（108課綱 N-3-7）
  python3 tools/gen_tw_math_g3_two_step_word_problems.py
連乘、加與除、減與除の兩步驟應用問題（不含併式：一歩ずつ計算する）。
誤答：1歩目で止める、1つの数を使い忘れる、演算を取り違える。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(31007)
NM = Names(R)


def chain():   # 連乘
    T = [("一盒有 {a} 顆蛋，一箱裝 {b} 盒。{c} 箱一共有幾顆蛋？", "顆"),
         ("一排有 {a} 張椅子，一間教室排 {b} 排。{c} 間教室一共有幾張椅子？", "張"),
         ("一包有 {a} 塊餅乾，一盒裝 {b} 包。{c} 盒一共有幾塊餅乾？", "塊"),
         ("每輛車有 {a} 個輪子，一層停車場停 {b} 輛車。{c} 層一共有幾個輪子？", "個")]

    def mk():
        t, u = R.choice(T)
        a = 4 if "輪子" in t else R.randint(2, 9)
        b, c = R.randint(2, 9), R.randint(2, 6)
        if len({a, b, c}) < 3:
            return None
        ans = a * b * c
        w = [a * b, b * c, a * b + c, a + b + c, a * c, ans + a * b]
        return mcq(t.format(a=a, b=b, c=c), num(ans) + u, [num(x) + u for x in w if x != ans],
                   "先算一%s：%d × %d ＝ %d，再算 %d 份：%d × %d ＝ %s（%s）。" % (
                       "箱" if "箱" in t else "份", a, b, a * b, c, a * b, c, num(ans), u))
    return mk


def add_div():
    def mk():
        d = R.randint(2, 9)
        tot = d * R.randint(4, 12)
        x = R.randint(5, tot - 5)
        y = tot - x
        who = NM.next()
        q = "%s有 %d 張卡片，媽媽又給了 %d 張。把全部的卡片平分給 %d 個朋友，每人分到幾張？" % (who, x, y, d)
        ans = tot // d
        w = [tot, x // d if x % d == 0 else x + y - d, ans + 1, y // d if y % d == 0 else ans - 1, ans * 2]
        return mcq(q, "%d張" % ans, ["%d張" % v for v in w if v != ans and v > 0],
                   "先合起來：%d ＋ %d ＝ %d（張）。再平分：%d ÷ %d ＝ %d（張）。" % (x, y, tot, tot, d, ans))
    return mk


def sub_div():
    def mk():
        d = R.randint(2, 9)
        left = d * R.randint(3, 12)
        used = R.randint(4, 40)
        tot = left + used
        q = "班上有 %d 顆氣球，破了 %d 顆，剩下的平均分給 %d 組，每組幾顆？" % (tot, used, d)
        ans = left // d
        w = [left, tot // d if tot % d == 0 else ans + 2, ans + 1, ans - 1, (tot + used) // d]
        return mcq(q, "%d顆" % ans, ["%d顆" % v for v in w if v != ans and v > 0],
                   "先算剩下：%d － %d ＝ %d（顆）。再平分：%d ÷ %d ＝ %d（顆）。" % (tot, used, left, left, d, ans))
    return mk


def div_add():
    def mk():
        d = R.randint(2, 9)
        q1 = R.randint(3, 12)
        tot = d * q1
        more = R.randint(2, 20)
        who = NM.next()
        q = "%d 顆草莓平分給 %d 人，%s又自己買了 %d 顆。%s現在有幾顆草莓？" % (tot, d, who, more, who)
        ans = q1 + more
        w = [tot + more, q1, (tot + more) // d, ans + d, abs(more - q1) or ans + 1]
        return mcq(q, "%d顆" % ans, ["%d顆" % v for v in w if v != ans and v > 0],
                   "先算每人分到：%d ÷ %d ＝ %d（顆）。再加上買的：%d ＋ %d ＝ %d（顆）。" % (tot, d, q1, q1, more, ans))
    return mk


def money():
    def mk():
        p = R.randint(12, 95)
        n = R.randint(2, 9)
        cost = p * n
        have = min(x for x in (100, 500, 1000) if x > cost) if R.random() < .6 else (cost // 100 + 1) * 100
        if have <= cost:
            return None
        item = R.choice(["色筆", "筆記本", "果汁", "彈珠汽水", "橡皮擦"])
        q = "一%s%s %d 元，買 %d %s，付 %d 元，要找回多少元？" % (
            "瓶" if item in ("果汁", "彈珠汽水") else ("本" if item == "筆記本" else "個" if item == "橡皮擦" else "盒"),
            item, p, n, "瓶" if item in ("果汁", "彈珠汽水") else ("本" if item == "筆記本" else "個" if item == "橡皮擦" else "盒"), have)
        ans = have - cost
        w = [cost, have - p, have + cost, ans + 10, ans - 10]
        return mcq(q, "%d元" % ans, ["%d元" % v for v in w if v != ans and v > 0],
                   "先算要付的錢：%d × %d ＝ %d（元）。再算找回：%d － %d ＝ %d（元）。" % (p, n, cost, have, cost, ans))
    return mk


def first_step():
    def mk():
        d = R.randint(3, 8)
        tot = d * R.randint(4, 9)
        x = R.randint(5, tot - 5)
        y = tot - x
        q = "「書架上有 %d 本書，又放上 %d 本，再平均放到 %d 層，每層幾本？」第一步要先算什麼？" % (x, y, d)
        ans = "%d ＋ %d，先算全部有幾本" % (x, y)
        w = ["%d ÷ %d，先算每層幾本" % (x, d), "%d × %d，先算 %d 層有幾本" % (y, d, d), "%d － %d，先算差幾本" % (max(x, y), min(x, y))]
        return mcq(q, ans, w, "要先知道「全部」有幾本：%d ＋ %d ＝ %d；再平分：%d ÷ %d ＝ %d。" % (x, y, tot, tot, d, tot // d))
    return mk


def main():
    seen = set()
    sets = [
        ("連乘", pick_unique(R, chain(), 20, seen)),
        ("先加再除", pick_unique(R, add_div(), 20, seen)),
        ("先減再除", pick_unique(R, sub_div(), 20, seen)),
        ("先除再加、買東西找錢", pick_unique(R, div_add(), 10, seen) + pick_unique(R, money(), 10, seen)),
        ("綜合：想好第一步", pick_unique(R, first_step(), 6, seen) + pick_unique(R, chain(), 4, seen)
                           + pick_unique(R, sub_div(), 5, seen) + pick_unique(R, add_div(), 5, seen)),
    ]
    body = lesson(
        ["兩步驟的題目要<b>一步一步算</b>：先找「要先知道的數」，再算問題要的答案。",
         "<b>連乘</b>：一盒幾顆 × 幾盒 ＝ 一箱幾顆，再 × 幾箱。",
         "<b>加與除</b>：先合起來（＋），再平分（÷）。<b>減與除</b>：先算剩下（－），再平分（÷）。",
         "每一步都寫算式和單位，最後看答案合不合理。"],
        [example("一盒有 6 顆蛋，一箱裝 4 盒。3 箱一共有幾顆蛋？", ["一箱：6 × 4 ＝ 24（顆）。", "3 箱：24 × 3 ＝ 72（顆）。"], "72 顆"),
         example("有 35 顆氣球，破了 5 顆，剩下的平分給 6 組，每組幾顆？", ["剩下：35 － 5 ＝ 30（顆）。", "每組：30 ÷ 6 ＝ 5（顆）。"], "5 顆")],
        [("只算第一步就當答案", "再讀一次問題：問的是「每組幾顆」還是「一共幾顆」"),
         ("35 顆直接 ÷ 6", "要先減掉破掉的 5 顆，再平分"),
         ("連乘只乘兩個數", "題目裡的三個數都要用到")])
    faq = [{"q": "三年級的兩步驟應用問題有哪些類型？",
            "a": "108課綱 N-3-7 包含連乘、加與除、減與除的應用問題，三年級不用寫成一個併式，可以分兩步算。"},
           {"q": "孩子不知道要先算什麼，怎麼辦？",
            "a": "先問「問題要的答案需要知道什麼？」，例如要平分，就要先知道全部有幾個，先算全部，再除。"},
           {"q": "可以印出來在家練習嗎？",
            "a": "可以，本頁有A4學習單（附解答）可免費列印，也可以線上做100題。"}]
    make_unit(R, "grade-3", "two-step-word-problems", "N-3-7",
              "解題：兩步驟應用問題（加減與除、連乘）。連乘、加與除、減與除之應用解題。不含併式。",
              "兩步驟應用問題：連乘、加與除、減與除",
              "三年級數學 兩步驟應用題 練習題｜連乘・先加再除・先減再除 學習單（附解答）",
              "兩步驟應用問題",
              "國小三年級數學「兩步驟應用問題」免費學習單：連乘、加與除、減與除、買東西找錢，練習想好第一步再算。100題線上練習馬上對答案，附可列印解答。",
              "先算要先知道的數，再算答案",
              "連乘、先加再除、先減再除：每一步寫算式和單位。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
