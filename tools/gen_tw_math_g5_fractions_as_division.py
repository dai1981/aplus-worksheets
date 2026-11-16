# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：整數相除的分數表示（108課綱 N-5-6）
  python3 tools/gen_tw_math_g5_fractions_as_division.py
a÷b＝a/b、分數→除法、平分（每人幾個）・分裝（幾倍）の意味、帶分數で答える、應用問題。
誤答：被除數と除數を逆にする（3÷4＝4/3）、帶分數の整数部分を忘れる、約分しない。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff

R = random.Random(51007)
NM = Names(R)


def s1(seen):
    def mk():
        a, b = R.randint(1, 20), R.randint(2, 12)
        if a % b == 0 or a == b:
            return None
        v = F(a, b)
        return mcq("%d ÷ %d ＝（用分數表示）" % (a, b), ff(v), [ff(F(b, a)), fr(a, b) if v.denominator != b else ff(v + F(1, v.denominator)), ff(F(a, b + 1)), str(a // b) if a > b else fr(1, a)],
                   "整數相除，被除數當分子、除數當分母：%d ÷ %d ＝ %s%s。" % (a, b, fr(a, b), " ＝ " + ff(v) if fr(a, b) != ff(v) else ""))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        b = R.randint(2, 12)
        a = R.randint(1, 3 * b)
        if a % b == 0 or F(a, b).denominator != b:
            return None
        return mcq("%s 可以寫成哪一個除法？" % fr(a, b), "%d ÷ %d" % (a, b), ["%d ÷ %d" % (b, a), "%d × %d" % (a, b), "%d － %d" % (max(a, b), min(a, b))],
                   "分數 %s 就是 %d ÷ %d。" % (fr(a, b), a, b))

    def blank():
        a, b = R.randint(1, 15), R.randint(2, 15)
        if a == b or F(a, b).denominator != b:
            return None
        if R.random() < .5:
            return mcq("%d ÷ □ ＝ %s，□ 是多少？" % (a, fr(a, b)), str(b), [str(a), str(a * b), str(b + 1)], "分母是除數：□ ＝ %d。" % b)
        return mcq("□ ÷ %d ＝ %s，□ 是多少？" % (b, fr(a, b)), str(a), [str(b), str(a * b), str(a + 1)], "分子是被除數：□ ＝ %d。" % a)
    return pick_unique(R, mk, 10, seen) + pick_unique(R, blank, 10, seen)


def s3(seen):
    def share():
        a, b = R.randint(1, 15), R.randint(2, 9)
        if a % b == 0:
            return None
        it = R.choice([("塊蛋糕", "塊"), ("條吐司", "條"), ("個披薩", "個"), ("公升果汁", "公升")])
        q = "把 %d %s平分給 %d 人，每人分到幾%s？" % (a, it[0], b, it[1])
        v = F(a, b)
        return mcq(q, ff(v) + " " + it[1], [ff(F(b, a)) + " " + it[1], ff(F(1, b)) + " " + it[1] if F(1, b) != v else ff(v * 2) + " " + it[1], ff(F(a, b * a)) + " " + it[1] if F(a, b * a) != v else ff(v + 1) + " " + it[1]],
                   "平分用除法：%d ÷ %d ＝ %s（%s）。" % (a, b, ff(v), it[1]))
    return pick_unique(R, share, 20, seen)


def s4(seen):
    def times():
        a, b = R.randint(2, 30), R.randint(2, 30)
        if a % b == 0 or b % a == 0:
            return None
        p1, p2 = NM.next(), NM.next()
        if p1 == p2:
            return None
        q = "%s有 %d 張卡片，%s有 %d 張。%s的卡片是%s的幾倍？" % (p1, a, p2, b, p1, p2)
        v = F(a, b)
        return mcq(q, ff(v) + " 倍", [ff(F(b, a)) + " 倍", str(a - b if a > b else b - a) + " 倍", ff(v + F(1, v.denominator)) + " 倍"],
                   "求幾倍用除法：%d ÷ %d ＝ %s（倍）。%s" % (a, b, ff(v), "比 1 小也可以說是幾倍。" if v < 1 else ""))

    def length():
        a, b = R.randint(2, 30), R.randint(2, 10)
        if a % b == 0:
            return None
        q = "一條 %d 公尺的繩子，每 %d 公尺剪一段，可以剪成幾段？（用分數表示，剩下的也算）" % (a, b)
        v = F(a, b)
        return mcq(q, ff(v) + " 段", [ff(F(b, a)) + " 段", "%d 段" % (a // b) if a > b else ff(v * 2) + " 段", ff(v + 1) + " 段"], "看 %d 裡有幾個 %d：%d ÷ %d ＝ %s（段）。" % (a, b, a, b, ff(v)))
    return pick_unique(R, times, 10, seen) + pick_unique(R, length, 10, seen)


def s5(seen):
    def mk():
        kind = R.choice(["rice", "juice", "walk", "time"])
        if kind == "rice":
            a, b = R.randint(3, 25), R.randint(2, 9)
            if a % b == 0:
                return None
            q = "%d 公斤的米平均裝成 %d 袋，每袋幾公斤？" % (a, b)
            v, u = F(a, b), "公斤"
        elif kind == "juice":
            a, b = R.randint(2, 9), R.randint(3, 12)
            if a % b == 0:
                return None
            q = "%d 公升的果汁平分到 %d 個杯子，每杯幾公升？" % (a, b)
            v, u = F(a, b), "公升"
        elif kind == "walk":
            a, b = R.randint(2, 12), R.randint(3, 8)
            if a % b == 0:
                return None
            q = "%s %d 天走了 %d 公里，平均每天走幾公里？" % (NM.next(), b, a)
            v, u = F(a, b), "公里"
        else:
            a, b = R.randint(5, 50), 60
            if a % 60 == 0:
                return None
            q = "%d 分鐘是幾小時？（用分數表示）" % a
            v, u = F(a, b), "小時"
        return mcq(q, ff(v) + " " + u, [ff(F(v.denominator, v.numerator)) + " " + u, ff(v + 1) + " " + u, ff(v + F(1, v.denominator)) + " " + u],
                   "%d ÷ %d ＝ %s（%s）。" % (a, b, ff(v), u))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("整數相除寫成分數", s1(seen)), ("分數和除法", s2(seen)), ("平分：每人分到多少", s3(seen)),
            ("幾倍和分裝", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["整數相除的結果可以用分數表示：<b>a ÷ b ＝ %s</b>，被除數當分子，除數當分母。" % fr("a", "b"),
         "平分：3 個披薩平分給 4 人，每人 3 ÷ 4 ＝ %s 個。" % fr(3, 4),
         "求幾倍：5 是 8 的 5 ÷ 8 ＝ %s 倍。答案是假分數時，可以化成帶分數，能約分要約分。" % fr(5, 8)],
        [example("7 ÷ 3 ＝（用分數表示）", ["被除數 7 當分子，除數 3 當分母：%s。" % fr(7, 3)], ff(F(7, 3))),
         example("5 公升果汁平分到 8 杯，每杯幾公升？", ["5 ÷ 8 ＝ %s。" % fr(5, 8)], fr(5, 8) + " 公升")],
        [("3 ÷ 4 ＝ %s" % fr(4, 3), "被除數是分子：%s" % fr(3, 4)),
         ("7 ÷ 3 只寫 2（忘了餘下的）", "寫成分數：%s" % ff(F(7, 3))),
         ("答案 %s 沒有約分" % fr(6, 8), "約成 %s" % fr(3, 4))])
    faq = [{"q": "整數相除為什麼可以寫成分數？",
            "a": "3 ÷ 4 是把 3 平分成 4 份，每份是 3 個 1/4，也就是 3/4。所以 a ÷ b ＝ a/b。"},
           {"q": "五年級的「整數相除的分數表示」要學什麼？",
            "a": "108課綱 N-5-6：從平分和分裝（測量）的觀點，理解整數相除可以用分數表示及其道理。"},
           {"q": "除不盡的時候怎麼辦？",
            "a": "可以寫成分數（或帶分數），例如 7 ÷ 3 ＝ 2又1/3，比寫「2……1」更能表示每份有多少。"}]
    make_unit(R, "grade-5", "fractions-as-division", "N-5-6",
              "整數相除之分數表示：從分裝（測量）和平分的觀點，分別說明整數相除為分數之意義與合理性。",
              "整數相除的分數表示",
              "五年級數學 整數相除 練習題｜除法寫成分數・平分・幾倍 學習單（附解答）",
              "整數相除寫成分數",
              "國小五年級數學「整數相除的分數表示」免費學習單：整數相除寫成分數、分數和除法的關係、平分每人分到多少、幾倍和分裝與應用題。100題線上練習馬上對答案，附可列印解答。",
              "a ÷ b ＝ b 分之 a",
              "被除數當分子，除數當分母。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
