# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：分裝與平分（108課綱 N-2-8）
  python3 tools/gen_tw_math_g2_sharing_and_grouping.py
包含除（幾個一份、可以分成幾份）と等分除（平分給幾人、每人幾個）を絵と乘法で考える、餘り（剩下幾個）、文章題。÷ 記號は三年級なので使わない。
誤答：份數と每份の數の取り違え、引き算で考える、餘りを答える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81309)
NM = Names(R)


def s1(seen):
    def mk():
        per, n = R.randint(2, 5), R.randint(2, 5)
        k = R.choice(P.KINDS)
        tot = per * n
        q = "有 %d %s%s，每 %d %s裝一盒，可以裝成幾盒？" % (tot, P.cl(k), P.nm(k), per, P.cl(k)) + P.row(tot, k, per_row=per * 2 if per * 2 <= 10 else per)
        return mcq(q, "%d 盒" % n, ["%d 盒" % x for x in (per, tot - per, n + 1) if x != n] + ["%d 盒" % (n + 2)], "%d 個一數，數了 %d 次：%d × %d ＝ %d，所以是 %d 盒。" % (per, n, per, n, tot, n))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        per, n = R.randint(2, 6), R.randint(2, 5)
        k = R.choice(P.KINDS)
        tot = per * n
        q = "%d %s%s平分給 %d 個人，每人分到幾%s？" % (tot, P.cl(k), P.nm(k), n, P.cl(k)) + P.row(tot, k)
        return mcq(q, "%d %s" % (per, P.cl(k)), ["%d %s" % (x, P.cl(k)) for x in (n, tot - n, per + 1) if x != per] + ["%d %s" % (per + 2, P.cl(k))], "一人一個輪流分，每人分到 %d %s：%d × %d ＝ %d。" % (per, P.cl(k), per, n, tot))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        per, n = R.randint(2, 9), R.randint(2, 9)
        tot = per * n
        k = R.choice(["group", "share"])
        if k == "group":
            q = "%d 顆糖，每 %d 顆一包，可以裝幾包？" % (tot, per)
            return mcq(q, "%d 包" % n, ["%d 包" % x for x in (per, tot - per, n + 1) if x != n] + ["%d 包" % (n + 2)], "想 %d × □ ＝ %d：%d × %d ＝ %d，所以是 %d 包。" % (per, tot, per, n, tot, n))
        q = "%d 張貼紙平分給 %d 人，每人幾張？" % (tot, n)
        return mcq(q, "%d 張" % per, ["%d 張" % x for x in (n, tot - n, per + 1) if x != per] + ["%d 張" % (per + 2)], "想 □ × %d ＝ %d：%d × %d ＝ %d，每人 %d 張。" % (n, tot, per, n, tot, per))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        per, n = R.randint(2, 6), R.randint(2, 5)
        r = R.randint(1, per - 1)
        tot = per * n + r
        q = "%d 個蘋果，每 %d 個裝一袋，可以裝滿幾袋？還剩幾個？" % (tot, per)
        return mcq(q, "%d 袋，剩 %d 個" % (n, r), ["%d 袋，剩 %d 個" % (n + 1, 0), "%d 袋，剩 %d 個" % (n, per - r) if per - r != r else "%d 袋，剩 %d 個" % (n - 1, r + per), "%d 袋，剩 %d 個" % (r, n)], "%d × %d ＝ %d，%d － %d ＝ %d，剩下的不夠再裝一袋。" % (per, n, per * n, tot, per * n, r))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        per, n = R.randint(2, 9), R.randint(2, 9)
        tot = per * n
        who = NM.next()
        t = R.choice([("%d 位小朋友，每 %d 人坐一輛車，要幾輛車？", "輛", "group"), ("%s把 %d 顆草莓平分在 %d 個盤子，每盤幾顆？", "顆", "share"),
                      ("%d 公尺長的繩子，每 %d 公尺剪一段，可以剪幾段？", "段", "group"), ("老師把 %d 枝筆平分給 %d 組，每組幾枝？", "枝", "share")])
        if t[2] == "group":
            q = t[0] % (tot, per)
            ans, w = n, [per, tot - per, n + 1]
            e = "%d × %d ＝ %d，所以是 %d %s。" % (per, n, tot, n, t[1])
        else:
            q = t[0] % ((who, tot, n) if "%s" in t[0] else (tot, n))
            ans, w = per, [n, tot - n, per + 1]
            e = "%d × %d ＝ %d，所以每份 %d %s。" % (per, n, tot, per, t[1])
        return mcq(q, "%d %s" % (ans, t[1]), ["%d %s" % (x, t[1]) for x in w if x != ans] + ["%d %s" % (ans + 2, t[1])], e)
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("幾個裝一份", s1(seen)), ("平分給幾人", s2(seen)), ("用乘法想分裝和平分", s3(seen)),
            ("分不完剩下幾個", s4(seen)), ("生活中的分裝與平分", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>分裝</b>：每幾個裝一份，可以裝幾份？12 個，每 3 個一盒：3、6、9、12，數了 4 次，是 4 盒。",
         "<b>平分</b>：平平的分給幾個人，每人幾個？12 個平分給 3 人，每人 4 個。" + P.circles([4, 4, 4], "apple"),
         "可以用乘法想：3 × □ ＝ 12，□ ＝ 4。分不完的就是「剩下」的。"],
        [example("15 個，每 5 個一袋", ["5 × 3 ＝ 15。"], "3 袋"),
         example("14 個，每 4 個一袋", ["4 × 3 ＝ 12，剩 2 個。"], "3 袋，剩 2 個")],
        [("分裝把每份的數當答案", "問「幾份」答份數；問「每人幾個」答每份的數"),
         ("12 個平分給 3 人用 12 － 3", "平分要想 □ × 3 ＝ 12"),
         ("剩下的也算一袋", "裝不滿的不算一袋")])
    faq = [{"q": "二年級會學除法嗎？",
            "a": "108課綱 N-2-8：二年級先用操作學「分裝」和「平分」，作為除法的前置經驗，三年級才用 ÷ 記號。"},
           {"q": "分裝和平分有什麼不同？",
            "a": "分裝知道每份幾個、求有幾份；平分知道有幾份、求每份幾個。兩種都可以用乘法來想。"},
           {"q": "在家怎麼練？",
            "a": "分點心、分玩具時，請孩子實際分一分，再說出「每人幾個」或「可以分幾份」。"}]
    make_unit(R, "grade-2", "sharing-and-grouping", "N-2-8",
              "解題：分裝與平分。以操作活動為主。除法前置經驗。理解分裝與平分之意義與方法。引導學生在解題過程，發現問題和乘法模式的關連。",
              "分裝與平分",
              "二年級數學 分裝與平分 練習題｜每幾個一份・平分給幾人 學習單（附解答）",
              "分裝與平分",
              "國小二年級數學「分裝與平分」免費學習單：每幾個裝一份、平分給幾人、用乘法想分裝和平分、分不完剩下幾個、生活中的分裝與平分。100題線上練習，圖多，附可列印解答。",
              "分裝求幾份，平分求每份幾個",
              "用乘法想：3 × □ ＝ 12，□ ＝ 4。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
