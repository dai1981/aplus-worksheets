# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：分數除以整數（108課綱 N-5-7）
  python3 tools/gen_tw_math_g5_dividing_fractions.py
分數÷整數＝分數×（整数分之1）、分子が割り切れる場合、帶分數÷整數、圖で理解、應用問題。
誤答：分子だけ割って割り切れないまま、分母に掛けずに分子に掛ける、帶分數の整数部分だけ割る。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, mx, ff

R = random.Random(51008)
NM = Names(R)


def pf(a, b):
    return F(a, b).denominator == b


def s1(seen):
    def mk():
        n = R.randint(2, 6)
        b = R.randint(3, 12)
        a = n * R.randint(1, (b - 1) // n) if (b - 1) // n >= 1 else None
        if not a or not pf(a, b):
            return None
        v = F(a, b) / n
        return mcq("%s ÷ %d ＝" % (fr(a, b), n), ff(v), [ff(F(a * n, b)), fr(a // n, b * n), ff(F(a, b // n)) if b % n == 0 else ff(v + F(1, b))],
                   "分子 %d 剛好能被 %d 整除：%s ÷ %d ＝ %s。" % (a, n, fr(a, b), n, ff(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.randint(2, 9)
        b = R.randint(2, 12)
        a = R.randint(1, b - 1)
        if not pf(a, b) or a % n == 0:
            return None
        v = F(a, b) / n
        return mcq("%s ÷ %d ＝" % (fr(a, b), n), ff(v), [ff(F(a * n, b)), ff(F(a, b + n)), ff(F(n, a * b)) if F(n, a * b) != v else ff(v * 2)],
                   "除以 %d 就是乘以 %s：%s × %s ＝ %s。" % (n, fr(1, n), fr(a, b), fr(1, n), ff(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        n = R.randint(2, 6)
        w = R.randint(1, 6)
        b = R.randint(2, 8)
        a = R.randint(1, b - 1)
        if not pf(a, b):
            return None
        x = w + F(a, b)
        v = x / n
        return mcq("%s ÷ %d ＝" % (mx(w, a, b), n), ff(v), [ff(F(w, n) + F(a, b)), ff(x * n), ff(v + F(1, v.denominator))],
                   "先化成假分數：%s ＝ %s，再乘以 %s：%s。" % (mx(w, a, b), fr(x.numerator, x.denominator), fr(1, n), ff(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def which():
        n = R.randint(2, 9)
        b = R.randint(2, 9)
        a = R.randint(1, b - 1)
        if not pf(a, b):
            return None
        q = "%s ÷ %d 和下面哪一個算式的答案一樣？" % (fr(a, b), n)
        return mcq(q, "%s × %s" % (fr(a, b), fr(1, n)), ["%s × %d" % (fr(a, b), n), ("%s × %s" % (fr(b, a), fr(1, n)) if a > 1 else "%s × %d" % (fr(1, n), b)), "%s ÷ %s" % (fr(a, b), fr(1, n))],
                   "除以一個整數，等於乘以這個整數分之一：%s ÷ %d ＝ %s × %s。" % (fr(a, b), n, fr(a, b), fr(1, n)))

    def compare():
        n = R.randint(2, 9)
        b = R.randint(2, 9)
        a = R.randint(1, b - 1)
        if not pf(a, b):
            return None
        q = "不用算，%s ÷ %d 的答案比 %s 大還是小？" % (fr(a, b), n, fr(a, b))
        return mcq(q, "比 %s 小" % fr(a, b), ["比 %s 大" % fr(a, b), "一樣大", "要算出來才知道"], "平分成 %d 份，每份比原來小。" % n)
    return pick_unique(R, which, 12, seen) + pick_unique(R, compare, 8, seen)


def s5(seen):
    def mk():
        n = R.randint(2, 8)
        b = R.choice([2, 3, 4, 5, 6, 8, 10])
        a = R.randint(1, 3 * b)
        if not pf(a, b) or a == b:
            return None
        x = F(a, b)
        kind = R.choice([("公升的果汁平分給 %d 人，每人幾公升？", "公升"), ("公斤的糖平分成 %d 包，每包幾公斤？", "公斤"), ("公尺的緞帶剪成一樣長的 %d 段，每段幾公尺？", "公尺")])
        q = ("%s " % ff(x)) + kind[0] % n
        u = kind[1]
        v = x / n
        return mcq(q, ff(v) + " " + u, [ff(x * n) + " " + u, ff(F(x.numerator, x.denominator + n)) + " " + u, ff(v + F(1, v.denominator)) + " " + u],
                   "%s ÷ %d ＝ %s × %s ＝ %s（%s）。" % (ff(x), n, ff(x), fr(1, n), ff(v), u))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("分子能整除", s1(seen)), ("乘以整數分之一", s2(seen)), ("帶分數除以整數", s3(seen)),
            ("除法和乘法的關係", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["分數除以整數，就是把分數<b>平分</b>成幾份。",
         "分子剛好能整除時：%s ÷ 3 ＝ %s。不能整除時：<b>除以 n 就是乘以 %s</b>：%s ÷ 3 ＝ %s × %s ＝ %s。" % (fr(6, 7), fr(2, 7), fr(1, "n"), fr(2, 5), fr(2, 5), fr(1, 3), fr(2, 15)),
         "帶分數先化成假分數再算，答案約成最簡分數。"],
        [example("%s ÷ 4 ＝" % fr(3, 5), ["除以 4 就是乘以 %s。" % fr(1, 4), "%s × %s ＝ %s。" % (fr(3, 5), fr(1, 4), fr(3, 20))], fr(3, 20)),
         example("%s ÷ 3 ＝" % mx(2, 1, 4), ["%s ＝ %s。" % (mx(2, 1, 4), fr(9, 4)), "%s × %s ＝ %s。" % (fr(9, 4), fr(1, 3), fr(3, 4))], fr(3, 4))],
        [("%s ÷ 4 ＝ %s（乘到分子去）" % (fr(3, 5), fr(12, 5)), "除以 4 是乘以 %s：%s" % (fr(1, 4), fr(3, 20))),
         ("%s ÷ 2 只把整數 2 除以 2" % mx(2, 1, 3), "先化成假分數 %s，再除以 2：%s" % (fr(7, 3), fr(7, 6))),
         ("除完答案比原來大", "平分後每份一定比原來小")])
    faq = [{"q": "分數除以整數怎麼算？",
            "a": "把除以整數 n 變成乘以 1/n，例如 3/5 ÷ 4 ＝ 3/5 × 1/4 ＝ 3/20。分子剛好能整除時，也可以直接用分子除。"},
           {"q": "為什麼除以 4 等於乘以 1/4？",
            "a": "除以 4 是平分成 4 份，取其中 1 份，就是原來的 1/4，所以等於乘以 1/4。"},
           {"q": "五年級的分數除法要學什麼？",
            "a": "108課綱 N-5-7：分數除以整數的意義，最後轉化為乘以單位分數。分數除以分數在六年級學。"}]
    make_unit(R, "grade-5", "dividing-fractions", "N-5-7",
              "分數除以整數：分數除以整數的意義。最後將問題轉化為乘以單位分數。",
              "分數除以整數",
              "五年級數學 分數除以整數 練習題｜乘以單位分數・帶分數除法 學習單（附解答）",
              "分數除以整數",
              "國小五年級數學「分數除以整數」免費學習單：分子能整除的除法、除以n就是乘以n分之一、帶分數除以整數、除法和乘法的關係與應用題。100題線上練習馬上對答案，附可列印解答。",
              "除以 n，就是乘以 n 分之 1",
              "帶分數先化成假分數再算。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
