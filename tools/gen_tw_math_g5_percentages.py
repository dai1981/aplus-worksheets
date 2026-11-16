# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：比率與百分率（含「折」、「成」）（108課綱 N-5-10）
  python3 tools/gen_tw_math_g5_percentages.py
比率（分數・小數）、百分率との互換、「打幾折」「幾成」、比率の計算（部分÷全体）、折扣・成數の應用。
誤答：打8折を8%引きとする、8折＝20%引きを80%引きとする、全体と部分を逆に割る、7成を7%とする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff, num, dnum

R = random.Random(51011)
NM = Names(R)


def s1(seen):
    def mk():
        tot = R.choice([20, 25, 40, 50, 80, 100, 200])
        part = R.randint(1, tot - 1)
        v = F(part, tot)
        if (v * 100).denominator != 1:
            return None
        who = R.choice(["%s %d 人，有 %d 人戴眼鏡" % ("全班" if tot <= 30 else "全年級", tot, part), "投籃 %d 次，進了 %d 球" % (tot, part), "種了 %d 棵樹苗，活了 %d 棵" % (tot, part)])
        q = "%s。比率是多少？（用小數表示）" % who
        return mcq(q, dnum(float(v), 2), [dnum(float(F(tot, part)), 2) if tot % part == 0 else dnum(float(1 - v), 2), dnum(float(v) * 10, 2) if v < .1 else dnum(float(1 - v), 2) if 1 - v != v else dnum(float(v) + .1, 2), str(part)],
                   "比率 ＝ 部分 ÷ 全部 ＝ %d ÷ %d ＝ %s。" % (part, tot, dnum(float(v), 2)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        p = R.choice(list(range(1, 100)) + [120, 150, 5, 10, 25, 75])
        kind = R.choice(["d2p", "p2d", "f2p"])
        if kind == "d2p":
            return mcq("%s 寫成百分率是多少？" % dnum(p / 100, 2), "%d%%" % p, ["%s%%" % dnum(p / 10, 1), "%d%%" % (p * 10), "%s%%" % dnum(p / 100, 2)], "比率 × 100%%：%s ＝ %d%%。" % (dnum(p / 100, 2), p))
        if kind == "p2d":
            return mcq("%d%% 寫成小數是多少？" % p, dnum(p / 100, 2), [dnum(p / 10, 1), str(p), dnum(p / 1000, 3)], "百分率 ÷ 100：%d%% ＝ %s。" % (p, dnum(p / 100, 2)))
        b = R.choice([2, 4, 5, 10, 20, 25, 50])
        a = R.randint(1, b - 1)
        v = F(a, b) * 100
        if v.denominator != 1 or F(a, b).denominator != b:
            return None
        return mcq("%s 寫成百分率是多少？" % fr(a, b), "%d%%" % v, ["%d%%" % x for x in (a * 10, a, 100 - v)] if 100 - v != v else ["%d%%" % x for x in (a * 10 if a * 10 != v else a + 1, a, v + 5)],
                   "%s ＝ %s ＝ %d%%。" % (fr(a, b), fr(int(v), 100), v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def zhe():
        k = R.choice([5, 6, 7, 75, 8, 85, 88, 9, 95])
        rate = k / 10 if k < 10 else k / 100
        name = "%d 折" % k
        if R.random() < .5:
            return mcq("打 %s，是原價的百分之幾？" % name, "%d%%" % round(rate * 100), ["%d%%" % x for x in (100 - round(rate * 100), k if k > 9 else k * 1, round(rate * 100) + 10)],
                       "打 %s就是原價的 %s ＝ %d%%。" % (name, dnum(rate, 2), round(rate * 100)))
        return mcq("打 %s，比原價便宜百分之幾？" % name, "%d%%" % (100 - round(rate * 100)), ["%d%%" % x for x in (round(rate * 100), k, 100 - round(rate * 100) + 10)],
                   "付原價的 %d%%，便宜了 100%% － %d%% ＝ %d%%。" % (round(rate * 100), round(rate * 100), 100 - round(rate * 100)))

    def cheng():
        k = R.randint(1, 9)
        if R.random() < .5:
            return mcq("「%d 成」是百分之幾？" % k, "%d%%" % (k * 10), ["%d%%" % x for x in (k, 100 - k * 10, k * 10 + 5)] if 100 - k * 10 != k * 10 else ["%d%%" % x for x in (k, k * 10 + 10, k * 10 + 5)],
                       "1 成是 10%%，%d 成是 %d%%。" % (k, k * 10))
        return mcq("%d%% 是幾成？" % (k * 10), "%d 成" % k, ["%d 成" % x for x in (k * 10, 10 - k, k + 1)] if 10 - k != k else ["%d 成" % x for x in (k * 10, k + 1, k - 1)], "10%% 是 1 成，%d%% 是 %d 成。" % (k * 10, k))
    return pick_unique(R, zhe, 12, seen) + pick_unique(R, cheng, 8, seen)


def s4(seen):
    def price():
        p = R.choice([100, 200, 250, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000])
        k = R.choice([5, 6, 7, 75, 8, 85, 9])
        rate = F(k, 10) if k < 10 else F(k, 100)
        v = p * rate
        if v.denominator != 1:
            return None
        mw, it = R.choice([("雙", "球鞋"), ("件", "外套"), ("個", "書包"), ("組", "積木"), ("副", "耳機")])
        q = "一%s%s原價 %s 元，打 %d 折後賣多少元？" % (mw, it, num(p), k)
        return mcq(q, "%s 元" % num(int(v)), ["%s 元" % num(x) for x in (p - int(v), p - k if p - k > 0 else p + k, int(v) + 10, p * k)], "%s × %s ＝ %s（元）。" % (num(p), dnum(float(rate), 2), num(int(v))))

    def pct_of():
        tot = R.choice([20, 40, 50, 60, 80, 120, 200, 300, 500])
        p = R.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
        v = F(tot * p, 100)
        if v.denominator != 1:
            return None
        q = "%d 的 %d%% 是多少？" % (tot, p)
        return mcq(q, num(int(v)), [num(x) for x in (tot - int(v), tot * p, int(v) * 10, tot + p)], "%d × %d%% ＝ %d × %s ＝ %d。" % (tot, p, tot, dnum(p / 100, 2), int(v)))
    return pick_unique(R, price, 10, seen) + pick_unique(R, pct_of, 10, seen)


def s5(seen):
    def survey():
        tot = R.choice([20, 25, 40, 50])
        part = R.randint(1, tot - 1)
        v = F(part, tot) * 100
        if v.denominator != 1:
            return None
        q = "%s %d 人，有 %d 人喜歡打籃球。喜歡打籃球的人佔百分之幾？" % ("全班" if tot <= 30 else "全年級", tot, part)
        return mcq(q, "%d%%" % v, ["%d%%" % x for x in (part, 100 - v, F(tot, part) * 100 if (F(tot, part) * 100).denominator == 1 else v + 10)] if 100 - v != v else ["%d%%" % x for x in (part, v + 10, v - 10)],
                   "%d ÷ %d ＝ %s ＝ %d%%。" % (part, tot, dnum(float(v) / 100, 2), v))

    def win():
        n = R.choice([20, 25, 40, 50])
        w = R.randint(1, n - 1)
        r = F(w, n) * 10
        if r.denominator != 1:
            return None
        q = "比賽 %d 場贏了 %d 場，勝率是幾成？" % (n, w)
        return mcq(q, "%d 成" % r, ["%d 成" % x for x in (w, 10 - r if 10 - r != r else r + 1, r * 10)], "勝率 ＝ %d ÷ %d ＝ %s，是 %d 成。" % (w, n, dnum(float(r) / 10, 1), r))

    def save():
        p = R.choice([300, 500, 800, 1000, 1200, 1500])
        k = R.choice([7, 75, 8, 85, 9])
        rate = F(k, 10) if k < 10 else F(k, 100)
        v = p * (1 - rate)
        if v.denominator != 1:
            return None
        q = "原價 %s 元的電子鍋打 %d 折，可以省下多少元？" % (num(p), k)
        return mcq(q, "%s 元" % num(int(v)), ["%s 元" % num(x) for x in (int(p * rate), k * 10, int(v) + 10)], "打 %d 折付 %s，省下 1 － %s ＝ %s：%s × %s ＝ %s（元）。" % (k, dnum(float(rate), 2), dnum(float(rate), 2), dnum(float(1 - rate), 2), num(p), dnum(float(1 - rate), 2), num(int(v))))
    return pick_unique(R, survey, 7, seen) + pick_unique(R, win, 6, seen) + pick_unique(R, save, 7, seen)


def main():
    seen = set()
    sets = [("比率", s1(seen)), ("百分率", s2(seen)), ("折和成", s3(seen)), ("打折和百分之幾", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>比率</b> ＝ 部分 ÷ 全部，可以寫成分數或小數。",
         "比率 × 100%% 就是<b>百分率</b>：0.35 ＝ 35%%。",
         "<b>打 8 折</b>是付原價的 0.8（80%%），便宜了 20%%。<b>7 成</b>是 70%%。"],
        [example("全班 25 人，有 9 人戴眼鏡，佔百分之幾？", ["9 ÷ 25 ＝ 0.36。", "0.36 ＝ 36%%。"], "36%%"),
         example("原價 600 元打 8 折，賣多少元？", ["打 8 折是原價的 0.8。", "600 × 0.8 ＝ 480。"], "480 元")],
        [("打 8 折是便宜 80%%", "打 8 折是付 80%%，便宜 20%%"),
         ("7 成 ＝ 7%%", "1 成是 10%%，7 成是 70%%"),
         ("比率用全部 ÷ 部分", "比率 ＝ 部分 ÷ 全部")])
    body = body.replace("%%", "%")
    faq = [{"q": "打折和百分率怎麼換？",
            "a": "打 8 折是原價的 80%（0.8）；打 75 折是 75%（0.75）。省下的部分是 100% 減去它。"},
           {"q": "「成」是什麼意思？",
            "a": "1 成是十分之一，也就是 10%。勝率 6 成就是 60%。"},
           {"q": "五年級的比率要學什麼？",
            "a": "108課綱 N-5-10：整數相除的應用，認識比率、百分率，以及生活中的「折」和「成」。"}]
    make_unit(R, "grade-5", "percentages", "N-5-10",
              "解題：比率與應用。整數相除的應用。含「百分率」、「折」、「成」。",
              "比率與百分率：折和成",
              "五年級數學 百分率 練習題｜比率・打折・幾成 學習單（附解答）",
              "比率與百分率",
              "國小五年級數學「比率與百分率」免費學習單：比率、百分率的互換、打折和幾成、算打折後的價錢與應用題。100題線上練習馬上對答案，附可列印解答。",
              "比率 ＝ 部分 ÷ 全部",
              "打 8 折是付 80%，7 成是 70%。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
