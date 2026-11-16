# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：正負數的乘除（108課綱 N-7-3）
  python3 tools/gen_tw_math_g7_multiplying_and_dividing_integers.py
同號相乘除は正、異號は負、多個數相乘の符號（負數の個數）、分數・小數の乘除（倒數）、應用（每小時下降・平均變化）。
誤答：（－）×（－）を負にする、負數が偶數個でも負にする、除法で倒數にしない、0 で割る。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import sn, par, opv, tidy_sets

R = random.Random(71004)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def mk():
        a, b = nz(-15, 15), nz(-15, 15)
        if a > 0 and b > 0:
            return None
        v = a * b
        return mcq("%s × %s ＝" % (par(a), par(b)), sn(v), [sn(-v), sn(a + b), sn(-(a + b)) if a + b else sn(v + 1)],
                   "%s：%d × %d ＝ %d，答案是 %s。" % ("同號相乘得正" if v > 0 else "異號相乘得負", abs(a), abs(b), abs(v), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        b, q_ = nz(-12, 12), nz(-15, 15)
        a = b * q_
        if a > 0 and b > 0:
            return None
        return mcq("%s ÷ %s ＝" % (par(a), par(b)), sn(q_), [sn(-q_), sn(a * b) if abs(a * b) < 1000 else sn(q_ + 1), sn(a - b)],
                   "%s：%d ÷ %d ＝ %d，答案是 %s。" % ("同號相除得正" if q_ > 0 else "異號相除得負", abs(a), abs(b), abs(q_), sn(q_)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        xs = [nz(-6, 6) for _ in range(R.choice([3, 4, 5]))]
        neg = sum(1 for x in xs if x < 0)
        v = 1
        for x in xs:
            v *= x
        q = " × ".join(par(x) for x in xs) + " ＝"
        return mcq(q, sn(v), [sn(-v), sn(sum(xs)), sn(v * 2)], "負數有 %d 個（%s數個），答案是%s：%s。" % (neg, "偶" if neg % 2 == 0 else "奇", "正" if v > 0 else "負", sn(v)))

    def sign():
        n = R.randint(2, 9)
        p = R.randint(1, 5)
        q = "%d 個負數和 %d 個正數相乘（都不是 0），結果是正數還是負數？" % (n, p)
        ans = "正數" if n % 2 == 0 else "負數"
        return mcq(q, ans, ["負數" if ans == "正數" else "正數", "0", "無法判斷"], "負數有 %d 個，是%s數個，所以積是%s。" % (n, "偶" if n % 2 == 0 else "奇", ans))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, sign, 6, seen)


def s4(seen):
    def mk():
        a = F(R.randint(1, 9), R.choice([2, 3, 4, 5, 6])) * R.choice([1, -1])
        b = F(R.randint(1, 9), R.choice([2, 3, 4, 5, 6])) * R.choice([1, -1])
        if a.denominator == 1 or b.denominator == 1:
            return None
        op = R.choice(["×", "÷"])
        v = a * b if op == "×" else a / b
        e = ("分子乘分子、分母乘分母，再定符號：%s。" % sn(v)) if op == "×" else ("除以一個數等於乘以它的倒數：%s × %s ＝ %s。" % (par(a), par(1 / b), sn(v)))
        return mcq("%s %s %s ＝" % (par(a), op, par(b)), sn(v), [sn(-v), sn(a / b if op == "×" else a * b), sn(1 / v)], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def drop():
        r = R.randint(2, 6)
        h = R.randint(2, 8)
        start = R.randint(-5, 15)
        v = start - r * h
        q = "某地氣溫是 %s ℃，之後每小時下降 %d ℃。%d 小時後是幾度？" % (sn(start), r, h)
        return mcq(q, "%s ℃" % sn(v), ["%s ℃" % sn(x) for x in (start + r * h, -r * h, v + r)], "變化量 (－%d) × %d ＝ %s，%s%s ＝ %s（℃）。" % (r, h, sn(-r * h), sn(start), opv("＋", -r * h), sn(v)))

    def avg():
        xs = [nz(-9, 9) for _ in range(5)]
        s = sum(xs)
        if s % 5:
            return None
        q = "五天的股價變化（元）是 %s。平均每天變化多少元？" % "、".join(sn(x) for x in xs)
        v = s // 5
        return mcq(q, "%s 元" % sn(v), ["%s 元" % sn(x) for x in (sum(abs(x) for x in xs) // 5 if sum(abs(x) for x in xs) // 5 != v else v + 2, -v if v else 1, s)  if x != v] + ["%s 元" % sn(v + 1)], "總和 %s ÷ 5 ＝ %s（元）。" % (sn(s), sn(v)))

    def dive():
        d = R.randint(2, 9)
        t = R.randint(3, 12)
        q = "潛水員每分鐘下潛 %d 公尺（記作 －%d），%d 分鐘後的位置是海平面下多少？用正負數表示。" % (d, d, t)
        return mcq(q, "%s 公尺" % sn(-d * t), ["%s 公尺" % sn(x) for x in (d * t, -d - t, -d * (t - 1))], "(－%d) × %d ＝ %s（公尺）。" % (d, t, sn(-d * t)))
    return pick_unique(R, drop, 7, seen) + pick_unique(R, avg, 7, seen) + pick_unique(R, dive, 6, seen)


def main():
    seen = set()
    sets = [("正負數的乘法", s1(seen)), ("正負數的除法", s2(seen)), ("多個數相乘的符號", s3(seen)),
            ("分數的乘除", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>同號相乘除得正，異號相乘除得負</b>：（－3）×（－4）＝ 12，（－12）÷ 3 ＝ －4。",
         "很多個數相乘：負數有<b>偶數個</b>，積是正；有<b>奇數個</b>，積是負。有 0 就是 0。",
         "除以一個數等於乘以它的倒數；0 不能當除數。"],
        [example("（－2）×（－3）×（－5）", ["負數有 3 個，答案是負。", "2 × 3 × 5 ＝ 30。"], "－30"),
         example("（－<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>）÷ <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>", ["乘以倒數 2。", "異號得負。"], "－<span class='fr'><span class='fn'>3</span><span class='fd'>2</span></span>")],
        [("（－3）×（－4）＝ －12", "同號相乘得正：12"),
         ("（－1）×（－1）×（－1）＝ 1", "負數 3 個（奇數），答案是 －1"),
         ("÷ <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> 直接乘 <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>", "要乘以倒數 2")])
    faq = [{"q": "為什麼負負得正？",
            "a": "可以想成「相反的相反」：－3 表示 3 的相反，再乘以 －1 又反過來一次，就回到正的。"},
           {"q": "很多數相乘時，怎麼快速判斷正負？",
            "a": "數一數負數的個數：偶數個就是正，奇數個就是負；只要有 0，積就是 0。"},
           {"q": "七年級的乘除要學什麼？",
            "a": "108課綱 N-7-3：負數與數的四則混合運算（含分數、小數），包含正負數的乘法和除法。"}]
    make_unit(R, "grade-7", "multiplying-and-dividing-integers", "N-7-3",
              "負數與數的四則混合運算（含分數、小數）：使用「正、負」表徵生活中的量；相反數；數的四則混合運算。",
              "正負數的乘除",
              "七年級數學 正負數乘除 練習題｜負負得正・符號判斷 學習單（附解答）",
              "正負數的乘除",
              "國中七年級數學「正負數的乘除」免費學習單：正負數的乘法和除法、多個數相乘的符號判斷、分數的乘除與氣溫下降、潛水等應用題。100題線上練習馬上對答案，附可列印解答。",
              "同號得正，異號得負",
              "負數有偶數個，積是正；奇數個，積是負。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
