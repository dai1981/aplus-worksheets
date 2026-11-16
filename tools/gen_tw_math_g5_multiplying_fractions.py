# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：分數的乘法（108課綱 N-5-5）
  python3 tools/gen_tw_math_g5_multiplying_fractions.py
整數×分數、分數×分數、帶分數の乘法、先に約分、積は被乘數より大きいとは限らない、交換律、應用問題。
誤答：分母にも整数を掛ける、帶分數を整数部分だけ掛ける、約分しない、「かけ算は必ず大きくなる」。
"""
import random
from fractions import Fraction as F
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, mx, ff, num

R = random.Random(51006)
NM = Names(R)


def pf(a, b):
    return F(a, b).denominator == b


def s1(seen):
    def mk():
        b = R.randint(2, 12)
        a = R.randint(1, b - 1)
        n = R.randint(2, 30)
        if not pf(a, b):
            return None
        v = n * F(a, b)
        order = R.random() < .5
        q = ("%d × %s ＝" % (n, fr(a, b))) if order else ("%s × %d ＝" % (fr(a, b), n))
        return mcq(q, ff(v), [ff(F(n * a, n * b)), ff(F(a, b * n)), ff(v + 1), fr(n * a, b) if F(n * a, b).denominator != b else ff(v + F(1, b))],
                   "整數乘以分子，分母不變：%d × %d ＝ %d，%s ＝ %s。" % (n, a, n * a, fr(n * a, b), ff(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        b, d = R.randint(2, 12), R.randint(2, 12)
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if not (pf(a, b) and pf(c, d)):
            return None
        v = F(a, b) * F(c, d)
        q = "%s × %s ＝" % (fr(a, b), fr(c, d))
        g = F(a * c, b * d)
        return mcq(q, ff(v), [fr(a * c, b + d) if b + d != v.denominator else ff(v * 2), ff(F(a * d, b * c)) if F(a * d, b * c) != v else ff(v + F(1, b * d)), fr(a * c, b * d) if g.denominator != b * d else ff(v + F(1, b * d)), fr(a + c, b * d)],
                   ("分子乘分子、分母乘分母：%s ＝ %s。可以先約分再乘，比較好算。" % (fr(a * c, b * d), ff(v))) if gcd(a * c, b * d) > 1 else "分子乘分子、分母乘分母：%s。" % ff(v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        w = R.randint(1, 4)
        b = R.randint(2, 8)
        a = R.randint(1, b - 1)
        if not pf(a, b):
            return None
        if R.random() < .5:
            n = R.randint(2, 9)
            other, ov = str(n), F(n)
        else:
            d = R.randint(2, 9)
            c = R.randint(1, d - 1)
            if not pf(c, d):
                return None
            other, ov = fr(c, d), F(c, d)
        x = w + F(a, b)
        v = x * ov
        q = "%s × %s ＝" % (mx(w, a, b), other)
        wrong = w * ov + F(a, b) * (ov if ov.denominator == 1 else 1)
        return mcq(q, ff(v), [ff(w * ov + F(a, b)), ff(w * ov + F(a, b) * ov + 1), ff(v + F(1, v.denominator)), ff(w + F(a, b) * ov)],
                   "先把帶分數化成假分數：%s ＝ %s，再乘：%s。" % (mx(w, a, b), fr(x.numerator, x.denominator), ff(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def bigger():
        b = R.randint(2, 9)
        a = R.randint(1, 2 * b)
        if a == b or not pf(a, b):
            return None
        n = R.randint(10, 99)
        x = F(a, b)
        q = "不用算出答案，%d × %s 的積比 %d 大還是小？" % (n, ff(x), n)
        ans = "比 %d 大" % n if x > 1 else "比 %d 小" % n
        return mcq(q, ans, ["比 %d 小" % n if x > 1 else "比 %d 大" % n, "一樣大", "要算出來才知道"],
                   "乘以比 1 大的數，積變大；乘以比 1 小的數，積變小。%s %s 1。" % (ff(x), ">" if x > 1 else "<"))

    def comm():
        b, d = R.randint(2, 9), R.randint(2, 9)
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if not (pf(a, b) and pf(c, d)) or F(a, b) == F(c, d):
            return None
        q = "下面哪一個算式和 %s × %s 的答案一樣？" % (fr(a, b), fr(c, d))
        return mcq(q, "%s × %s" % (fr(c, d), fr(a, b)), ["%s ＋ %s" % (fr(a, b), fr(c, d)), "%s × %s" % (fr(b, a), fr(c, d)), "%s × %s" % (fr(a, d), fr(c, b)) if F(a, d) * F(c, b) != F(a, b) * F(c, d) else "%s － %s" % (fr(c, d), fr(a, b))],
                   "乘法交換律在分數也成立：%s × %s ＝ %s × %s。" % (fr(a, b), fr(c, d), fr(c, d), fr(a, b)))
    return pick_unique(R, bigger, 12, seen) + pick_unique(R, comm, 8, seen)


def s5(seen):
    def part():
        tot = R.choice([24, 30, 36, 40, 48, 60, 72, 120])
        b = R.choice([d for d in (2, 3, 4, 5, 6, 8, 10, 12) if tot % d == 0])
        a = R.randint(1, b - 1)
        if not pf(a, b):
            return None
        who = NM.next()
        q = "%s有 %d 元，用掉了 %s，用掉多少元？" % (who, tot, fr(a, b))
        v = tot * a // b
        return mcq(q, "%d 元" % v, ["%d 元" % x for x in (tot - v, tot // b, tot * b // a if (tot * b) % a == 0 else v + 1)], "%d × %s ＝ %d（元）。" % (tot, fr(a, b), v))

    def area():
        b, d = R.randint(2, 6), R.randint(2, 6)
        a, c = R.randint(1, b * 2), R.randint(1, d * 2)
        if a == b or c == d or not (pf(a, b) and pf(c, d)):
            return None
        q = "長方形菜園長 %s 公尺、寬 %s 公尺，面積是多少平方公尺？" % (ff(F(a, b)), ff(F(c, d)))
        v = F(a, b) * F(c, d)
        return mcq(q, ff(v) + " 平方公尺", [ff((F(a, b) + F(c, d)) * 2) + " 平方公尺", ff(F(a, b) + F(c, d)) + " 平方公尺", ff(v + F(1, v.denominator)) + " 平方公尺"],
                   "面積 ＝ 長 × 寬 ＝ %s × %s ＝ %s（平方公尺）。" % (ff(F(a, b)), ff(F(c, d)), ff(v)))

    def of_of():
        b, d = R.choice([2, 3, 4, 5]), R.choice([2, 3, 4, 5])
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if not (pf(a, b) and pf(c, d)):
            return None
        q = "一塊蛋糕，%s吃了 %s，剩下的 %s 給了弟弟。弟弟拿到整塊蛋糕的幾分之幾？" % (NM.next(), fr(a, b), fr(c, d))
        rem = 1 - F(a, b)
        v = rem * F(c, d)
        return mcq(q, ff(v), [ff(F(c, d)), ff(F(a, b) * F(c, d)), ff(rem - F(c, d)) if rem > F(c, d) else ff(v + F(1, 12))],
                   "剩下 1 － %s ＝ %s，%s × %s ＝ %s。" % (fr(a, b), ff(rem), ff(rem), fr(c, d), ff(v)))
    return pick_unique(R, part, 8, seen) + pick_unique(R, area, 6, seen) + pick_unique(R, of_of, 6, seen)


def main():
    seen = set()
    sets = [("整數 × 分數", s1(seen)), ("分數 × 分數", s2(seen)), ("帶分數的乘法", s3(seen)),
            ("積會變大還是變小", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>整數 × 分數</b>：整數乘以分子，分母不變。<b>分數 × 分數</b>：分子乘分子，分母乘分母。",
         "<b>可以先約分再乘</b>，數字小比較好算；答案要是最簡分數。帶分數先化成假分數再乘。",
         "乘以比 1 小的數，積會變小；乘以比 1 大的數，積才變大。「一個數的幾分之幾」就用乘法。"],
        [example("%s × %s ＝" % (fr(3, 4), fr(2, 9)), ["先約分：3 和 9 約成 1 和 3，2 和 4 約成 1 和 2。", "%s × %s ＝ %s。" % (fr(1, 2), fr(1, 3), fr(1, 6))], fr(1, 6)),
         example("%s × 6 ＝" % mx(1, 2, 3), ["%s ＝ %s。" % (mx(1, 2, 3), fr(5, 3)), "%s × 6 ＝ 10。" % fr(5, 3)], "10")],
        [("%s × 4 ＝ %s" % (fr(2, 3), fr(8, 12)), "整數只乘分子：%s" % ff(F(8, 3))),
         ("%s × 2 ＝ 2%s（只乘整數部分）" % (mx(1, 1, 2), fr(1, 2)), "先化成假分數：%s × 2 ＝ 3" % fr(3, 2)),
         ("乘法的答案一定比原來大", "乘以真分數，答案會變小")])
    faq = [{"q": "分數乘以分數怎麼算？",
            "a": "分子乘分子、分母乘分母，能先約分就先約分。例如 3/4 × 2/9 ＝ 1/6。"},
           {"q": "為什麼乘法的答案會變小？",
            "a": "乘以 1/2 就是取一半，所以會變小。乘以比 1 小的數，積比原來小；乘以比 1 大的數，積才比原來大。"},
           {"q": "五年級的分數乘法要學什麼？",
            "a": "108課綱 N-5-5：整數乘以分數、分數乘以分數的意義，用約分簡化計算，知道積不一定比被乘數大，以及乘法交換律在分數也成立。"}]
    make_unit(R, "grade-5", "multiplying-fractions", "N-5-5",
              "分數的乘法：整數乘以分數、分數乘以分數的意義。知道用約分簡化乘法計算。處理乘積一定比被乘數大的錯誤類型。透過分數計算的公式，知道乘法交換律在分數也成立。",
              "分數的乘法",
              "五年級數學 分數乘法 練習題｜整數乘分數・分數乘分數・帶分數 學習單（附解答）",
              "分數的乘法",
              "國小五年級數學「分數的乘法」免費學習單：整數乘以分數、分數乘以分數、帶分數的乘法、積會變大還是變小與應用題。100題線上練習馬上對答案，附可列印解答。",
              "分子乘分子，分母乘分母",
              "先約分再乘；乘以真分數，積會變小。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
