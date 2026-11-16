# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：正負數的四則混合運算（108課綱 N-7-3）
  python3 tools/gen_tw_math_g7_mixed_operations.py
先乘除後加減・括號優先を負數で、分數・小數を含む混合計算、－3² と （－3）² の區別（指數は次單元で詳しく）を除き、應用（得點・收支）。
誤答：左から順に計算する、負號を落とす、括號の前の負號を中に配らない。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import sn, par, opv, tidy_sets

R = random.Random(71005)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def mk():
        a, b, c = nz(-20, 20), nz(-9, 9), nz(-9, 9)
        o = R.choice(["＋", "－"])
        v = a + b * c if o == "＋" else a - b * c
        q = "%s%s ×%s ＝" % (sn(a), opv(o, b), " " + par(c) if c > 0 else par(c))
        wrong = (a + b) * c if o == "＋" else (a - b) * c
        return mcq(q, sn(v), [sn(wrong), sn(-v), sn(a + b * c if o == "－" else a - b * c)], "先乘：%s ×%s ＝ %s，再%s：%s。" % (par(b), " " + par(c) if c > 0 else par(c), sn(b * c), "加" if o == "＋" else "減", sn(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        b = nz(-6, 6)
        c = nz(-8, 8)
        a = b * c
        d = nz(-15, 15)
        k = R.choice([1, 2])
        if k == 1:
            q = "%s ÷%s%s ＝" % (par(a), " " + par(b) if b > 0 else par(b), opv("－", d))
            v = c - d
            w = [a // (b - d) if (b - d) and a % (b - d) == 0 else c + d, c + d, -v]
            e = "先除：%s ÷ %s ＝ %s，再減：%s%s ＝ %s。" % (par(a), par(b), sn(c), sn(c), opv("－", d), sn(v))
        else:
            inner = "%s%s" % (sn(d), opv("＋", c))
            q = (("［%s］" if "（" in inner else "（%s）") % inner) + "×%s ＝" % (" " + par(b) if b > 0 else par(b))
            v = (d + c) * b
            w = [d + c * b, -v, (d - c) * b]
            e = "先算括號：%s%s ＝ %s，再乘：%s ×%s ＝ %s。" % (sn(d), opv("＋", c), sn(d + c), par(d + c), " " + par(b) if b > 0 else par(b), sn(v))
        return mcq(q, sn(v), [sn(x) for x in w], e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a = F(R.randint(1, 5), R.choice([2, 3, 4])) * R.choice([1, -1])
        b = F(R.randint(1, 5), R.choice([2, 3, 4, 6])) * R.choice([1, -1])
        c = nz(-6, 6)
        if a.denominator == 1 or b.denominator == 1:
            return None
        v = a + b * c
        q = "%s%s ×%s ＝" % (sn(a), opv("＋", b), " " + par(c) if c > 0 else par(c))
        return mcq(q, sn(v), [sn((a + b) * c), sn(-v), sn(a - b * c)], "先乘：%s × %s ＝ %s，再加 %s：%s。" % (par(b), par(c), sn(b * c), par(a), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, b, c, d = nz(-12, 12), nz(-5, 5), nz(-12, 12), nz(-6, 6)
        v = F(a) - F(b) * (c - d)
        if v.denominator != 1:
            return None
        inner = "%s%s" % (sn(c), opv("－", d))
        q = "%s －%s ×%s ＝" % (sn(a), " " + par(b) if b > 0 else par(b), ("［%s］" if "（" in inner else "（%s）") % inner)
        return mcq(q, sn(v), [sn((a - b) * (c - d)), sn(a + b * (c - d)), sn(a - b * c - d)],
                   "括號：%s%s ＝ %s；乘：%s × %s ＝ %s；最後：%s%s ＝ %s。" % (sn(c), opv("－", d), sn(c - d), par(b), par(c - d), sn(b * (c - d)), sn(a), opv("－", b * (c - d)), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def quiz():
        n = R.choice([10, 15, 20])
        right = R.randint(n // 2, n)
        wrong_ = R.randint(1, n - right) if n > right else 0
        blank = n - right - wrong_
        sc = right * 4 + wrong_ * (-2) + blank * 0
        q = "測驗共 %d 題，答對一題 ＋4 分，答錯一題 －2 分，不答 0 分。%s答對 %d 題、答錯 %d 題，其餘不答，得幾分？" % (n, NM.next(), right, wrong_)
        return mcq(q, "%s 分" % sn(sc), ["%s 分" % sn(x) for x in (right * 4 + wrong_ * 2, right * 4, (right - wrong_) * 4)  if x != sc] + ["%s 分" % sn(sc + 2)], "%d × 4 ＋ %d ×（－2）＝ %d ＋（%s）＝ %s（分）。" % (right, wrong_, right * 4, sn(-2 * wrong_), sn(sc)) if wrong_ else "%d × 4 ＝ %d（分）。" % (right, sc))

    def money():
        inc = R.randint(200, 900)
        days = R.randint(3, 6)
        spend = R.randint(100, 300)
        v = inc - spend * days
        q = "%s這週收入 %d 元，每天支出 %d 元，共 %d 天。收支結果是多少元？（收入記正、支出記負）" % (NM.next(), inc, spend, days)
        return mcq(q, "%s 元" % sn(v), ["%s 元" % sn(x) for x in (inc + spend * days, (inc - spend) * days, -v)], "%d ＋（－%d）× %d ＝ %d － %d ＝ %s（元）。" % (inc, spend, days, inc, spend * days, sn(v)))
    return pick_unique(R, quiz, 10, seen) + pick_unique(R, money, 10, seen)


def main():
    seen = set()
    sets = [("先乘除後加減", s1(seen)), ("括號和除法", s2(seen)), ("含分數的混合計算", s3(seen)),
            ("三步驟的混合計算", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["計算順序和小學一樣：<b>括號 → 乘除 → 加減</b>；同一級由左往右。",
         "每一步都要注意符號，負數放進算式要加括號：5 ×（－3）。",
         "減去一個負數等於加上正數；有分數時，先算乘除再通分加減。"],
        [example("－8 ＋ 3 ×（－4）", ["先乘：3 ×（－4）＝ －12。", "－8 ＋（－12）＝ －20。"], "－20"),
         example("（－6 ＋ 2）×（－5）", ["括號：－4。", "（－4）×（－5）＝ 20。"], "20")],
        [("－8 ＋ 3 ×（－4）先算 －8 ＋ 3", "先乘除後加減"),
         ("5 －（－2）× 3 ＝ 3 × 3", "先乘：（－2）× 3 ＝ －6，5 －（－6）＝ 11"),
         ("（－4）×（－5）＝ －20", "同號相乘得正：20")])
    faq = [{"q": "有負數的四則運算，順序和小學一樣嗎？",
            "a": "一樣：先算括號，再算乘除，最後算加減。不同的是每一步都要判斷正負號。"},
           {"q": "怎麼減少符號錯誤？",
            "a": "把負數加上括號，減法改成加上相反數，每一步只做一件事，最後再檢查一次符號。"},
           {"q": "七年級的四則混合要學什麼？",
            "a": "108課綱 N-7-3：負數與數的四則混合運算，包含分數和小數。"}]
    make_unit(R, "grade-7", "mixed-operations", "N-7-3",
              "負數與數的四則混合運算（含分數、小數）：使用「正、負」表徵生活中的量；相反數；數的四則混合運算。",
              "正負數的四則混合運算",
              "七年級數學 四則混合運算 練習題｜負數・分數・計算順序 學習單（附解答）",
              "四則混合運算",
              "國中七年級數學「正負數的四則混合運算」免費學習單：先乘除後加減、括號和除法、含分數的混合計算、三步驟計算與得分、收支應用題。100題線上練習馬上對答案，附可列印解答。",
              "括號 → 乘除 → 加減",
              "每一步都要判斷正負號；負數放進算式要加括號。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
