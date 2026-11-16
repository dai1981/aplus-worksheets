# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：根式的四則運算（108課綱 N-8-1）
  python3 tools/gen_tw_math_g8_operations_with_radicals.py
同類方根の加減（化簡してから合わせる）、√a×√b＝√ab、√a÷√b、分配律・乘法公式を使う根式計算、應用（周長・面積）。
誤答：√2＋√3＝√5、化簡せずに同類でないとする、2√3×3√3＝6√3、(√3＋1)²＝3＋1。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g8 import sn, tidy_sets, rt, simp

R = random.Random(81005)
NM = Names(R)


def s1(seen):
    def mk():
        m = R.choice([2, 3, 5, 6, 7])
        a, b = R.randint(1, 9), R.randint(1, 9)
        op = R.choice(["＋", "－"])
        v = a + b if op == "＋" else a - b
        if v == 0:
            return None
        q = "%s %s %s ＝" % (rt(a, m), op, rt(b, m))
        return mcq(q, rt(v, m), [rt(v, 2 * m) if v > 0 else rt(v, m * m), rt(a * b, m), "%s" % rt(-v, m)], "同類方根（根號裡一樣）才能合併，係數%s：%s。" % ("相加" if op == "＋" else "相減", rt(v, m)))

    def simp_add():
        m = R.choice([2, 3, 5])
        k1, k2 = R.randint(1, 5), R.randint(2, 5)
        n1, n2 = k1 * k1 * m, k2 * k2 * m
        if n1 == n2:
            return None
        q = "√%d ＋ √%d ＝" % (n1, n2)
        return mcq(q, rt(k1 + k2, m), ["√%d" % (n1 + n2), rt(k1 * k2, m), rt(k1 + k2, 2 * m)], "先化簡：√%d ＝ %s，√%d ＝ %s，再合併：%s。" % (n1, rt(k1, m), n2, rt(k2, m), rt(k1 + k2, m)))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, simp_add, 10, seen)


def s2(seen):
    def mk():
        a, b = R.randint(1, 6), R.randint(1, 6)
        m, n = R.choice([(2, 3), (2, 6), (3, 6), (2, 8), (3, 12), (5, 10), (2, 18), (3, 3), (5, 5), (7, 7)])
        prod = m * n
        k, r = simp(prod)
        v = (a * b * k, r)
        q = "%s × %s ＝" % (rt(a, m), rt(b, n))
        return mcq(q, rt(*v), [rt(a * b, prod) if r != prod or a * b != v[0] else rt(a + b, prod), rt(a + b, prod), rt(a * b * k, r * 2) if r > 1 else str(a * b * k + 1)], "係數相乘 %d × %d，根號裡相乘 √%d ＝ %s，答案 %s。" % (a, b, prod, rt(k, r), rt(*v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = R.choice([1, 2, 3, 4, 6])
        m = R.choice([2, 3, 5])
        n = m * R.choice([4, 9, 2, 3])
        q = "√%d ÷ √%d ＝" % (n, m)
        kk, r = simp(n // m)
        return mcq(q, rt(kk, r), ["√%d" % (n - m), rt(kk + 1, r) if r > 1 else str(kk + 1), "√%d" % (n * m)], ("√%d ÷ √%d ＝ √（%d ÷ %d）＝ √%d ＝ %s。" % (n, m, n, m, n // m, rt(kk, r))) if rt(kk, r) != "√%d" % (n // m) else ("√%d ÷ √%d ＝ √（%d ÷ %d）＝ √%d。" % (n, m, n, m, n // m)))

    def dist():
        a, b = R.randint(1, 5), R.randint(1, 9)
        m = R.choice([2, 3, 5])
        q = "√%d（%s ＋ √%d）＝" % (m, rt(a, m), b * b * m if False else m) if False else "√%d（%d ＋ √%d）＝" % (m, b, m)
        ans = "%s ＋ %d" % (rt(b, m), m)
        return mcq(q, ans, ["%s ＋ √%d" % (rt(b, m), m), "%s" % rt(b, m), "%d ＋ %d" % (b, m)], "分配律：√%d × %d ＋ √%d × √%d ＝ %s ＋ %d。" % (m, b, m, m, rt(b, m), m))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, dist, 10, seen)


def s4(seen):
    def mk():
        m = R.choice([2, 3, 5, 6, 7])
        a = R.randint(1, 6)
        k = R.choice(["sq+", "sq-", "pm"])
        if k == "sq+":
            q = "（√%d ＋ %d）<sup>2</sup> ＝" % (m, a)
            ans = "%d ＋ %s" % (m + a * a, rt(2 * a, m))
            w = ["%d" % (m + a * a), "%d ＋ %s" % (m + a * a, rt(a, m)), "%d ＋ %s" % (m + a, rt(2 * a, m))]
            e = "（√%d）<sup>2</sup> ＋ 2 × %d × √%d ＋ %d<sup>2</sup> ＝ %s。" % (m, a, m, a, ans)
        elif k == "sq-":
            q = "（√%d － %d）<sup>2</sup> ＝" % (m, a)
            ans = "%d － %s" % (m + a * a, rt(2 * a, m))
            w = ["%d" % (m + a * a), "%d － %s" % (m - a * a, rt(2 * a, m)) if m != a * a else "%d" % (m - a * a), "%d ＋ %s" % (m + a * a, rt(2 * a, m))]
            e = "（√%d）<sup>2</sup> － 2 × %d × √%d ＋ %d<sup>2</sup> ＝ %s。" % (m, a, m, a, ans)
        else:
            q = "（√%d ＋ %d）（√%d － %d）＝" % (m, a, m, a)
            v = m - a * a
            ans = sn(v)
            w = [sn(m + a * a), sn(m - a), sn(-v) if v else "1"]
            e = "平方差：（√%d）<sup>2</sup> － %d<sup>2</sup> ＝ %d － %d ＝ %s。" % (m, a, m, a * a, ans)
        return mcq(q, ans, w, e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def rect():
        a, b = R.choice([(2, 8), (3, 12), (2, 18), (5, 20), (3, 27), (2, 32)])
        q = "長方形的長是 √%d 公分，寬是 √%d 公分。面積是多少平方公分？" % (b, a)
        k, r = simp(a * b)
        return mcq(q, "%s 平方公分" % rt(k, r), ["%s 平方公分" % x for x in ("√%d" % (a + b), rt(*simp(a)) + " ＋ " + rt(*simp(b)), str(a * b))], "√%d × √%d ＝ √%d ＝ %s。" % (b, a, a * b, rt(k, r)))

    def per():
        m = R.choice([2, 3, 5])
        k1, k2 = R.randint(1, 4), R.randint(1, 4)
        n1, n2 = k1 * k1 * m, k2 * k2 * m
        q = "長方形的長是 √%d 公分，寬是 √%d 公分。周長是多少公分？" % (n1, n2)
        return mcq(q, "%s 公分" % rt(2 * (k1 + k2), m), ["%s 公分" % x for x in (rt(k1 + k2, m), "√%d" % (2 * (n1 + n2)), rt(2 * k1 * k2, m))], "√%d ＝ %s，√%d ＝ %s，周長 2 ×（%s ＋ %s）＝ %s。" % (n1, rt(k1, m), n2, rt(k2, m), rt(k1, m), rt(k2, m), rt(2 * (k1 + k2), m)))

    def sq():
        n = R.choice([8, 12, 18, 20, 27, 32, 45, 50])
        k, r = simp(n)
        q = "正方形的面積是 %d 平方公分，周長是多少公分？" % n
        return mcq(q, "%s 公分" % rt(4 * k, r), ["%s 公分" % x for x in (rt(k, r), str(4 * n), rt(2 * k, r))], "邊長 √%d ＝ %s，周長 4 × %s ＝ %s。" % (n, rt(k, r), rt(k, r), rt(4 * k, r)))
    return pick_unique(R, rect, 6, seen) + pick_unique(R, per, 8, seen) + pick_unique(R, sq, 6, seen)


def main():
    seen = set()
    sets = [("根式的加減", s1(seen)), ("根式的乘法", s2(seen)), ("除法與分配律", s3(seen)),
            ("用乘法公式計算", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["加減：只有<b>同類方根</b>（化簡後根號裡一樣）才能合併：2√3 ＋ 5√3 ＝ 7√3；√2 ＋ √3 不能再合併。",
         "乘法：<b>√a × √b ＝ √ab</b>；係數和係數乘，根號和根號乘，再化簡。",
         "除法：√a ÷ √b ＝ √（a ÷ b）。",
         "乘法公式照樣能用：（√3 ＋ 1）<sup>2</sup> ＝ 3 ＋ 2√3 ＋ 1 ＝ 4 ＋ 2√3。"],
        [example("√12 ＋ √27", ["2√3 ＋ 3√3。"], "5√3"),
         example("2√3 × 3√6", ["2 × 3 ＝ 6，√18 ＝ 3√2。"], "18√2")],
        [("√2 ＋ √3 ＝ √5", "根號裡不一樣不能合併"),
         ("2√3 × 3√3 ＝ 6√3", "√3 × √3 ＝ 3：答案 18"),
         ("（√3 ＋ 1）<sup>2</sup> ＝ 3 ＋ 1", "漏了中間項 2√3")])
    faq = [{"q": "什麼是同類方根？",
            "a": "化成最簡根式後，根號裡的數一樣，例如 √12 ＝ 2√3 和 √27 ＝ 3√3 是同類方根，可以合併成 5√3。"},
           {"q": "為什麼 √2 ＋ √3 不等於 √5？",
            "a": "√2 ＋ √3 約是 1.41 ＋ 1.73 ＝ 3.14，而 √5 約是 2.24，兩者不相等。"},
           {"q": "八年級的根式運算要學什麼？",
            "a": "108課綱 N-8-1：二次方根的意義、根式的化簡及四則運算。"}]
    make_unit(R, "grade-8", "operations-with-radicals", "N-8-1",
              "二次方根：二次方根的意義；根式的化簡及四則運算。",
              "根式的四則運算",
              "八年級數學 根式運算 練習題｜同類方根・根式乘除・乘法公式 學習單（附解答）",
              "根式的運算",
              "國中八年級數學「根式的四則運算」免費學習單：同類方根的加減、根式的乘法和除法、分配律、用乘法公式計算根式與面積、周長應用。100題線上練習馬上對答案，附可列印解答。",
              "只有同類方根才能合併",
              "√a × √b ＝ √ab，算完要化成最簡根式。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
