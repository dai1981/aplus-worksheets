# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：分配律與乘除混合計算（108課綱 R-5-2）
  python3 tools/gen_tw_math_g5_distributive_property.py
乘法對加法・減法の分配律、□を求める、簡化計算（99・101・25×4 など）、乘除混合の規律、應用。
誤答：a×(b+c) を a×b+c とする、99 の簡算で 1 回だけ引き忘れる、÷ の順を入れ替えて分母を間違える。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(51025)
NM = Names(R)


def s1(seen):
    def mk():
        a, b, c = R.randint(3, 19), R.randint(5, 40), R.randint(2, 30)
        op = R.choice(["＋", "－"])
        if op == "－" and b <= c:
            b, c = c + R.randint(2, 9), b
        side = R.choice(["fwd", "back"])
        if side == "fwd":
            q = "%d ×（%d %s %d）和下面哪一個算式相等？" % (a, b, op, c)
            ans = "%d × %d %s %d × %d" % (a, b, op, a, c)
            w = ["%d × %d %s %d" % (a, b, op, c), "%d × %d × %d" % (a, b, c), "%d ＋ %d %s %d ＋ %d" % (a, b, op, a, c), "%d × %d %s %d × %d" % (a, b, "－" if op == "＋" else "＋", a, c)]
            e = "分配律：%d 要分別乘 %d 和 %d，%s。" % (a, b, c, ans)
        else:
            q = "%d × %d %s %d × %d 和下面哪一個算式相等？" % (b, a, op, c, a)
            ans = "（%d %s %d）× %d" % (b, op, c, a)
            w = ["（%d %s %d）× %d × %d" % (b, op, c, a, a), "%d %s %d × %d" % (b, op, c, a), "（%d %s %d）× %d" % (b, "－" if op == "＋" else "＋", c, a), "%d ×（%d %s %d）× %d" % (a, b, op, c, a)]
            e = "兩項都乘 %d，可以合起來：%s。" % (a, ans)
        return mcq(q, ans, w, e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b, c = R.randint(4, 25), R.randint(6, 30), R.randint(3, 20)
        k = R.choice([0, 1, 2, 3])
        if k == 0:
            q = "%d ×（%d ＋ %d）＝ %d × %d ＋ %d × □，□ 是多少？" % (a, b, c, a, b, a)
            v, w = c, [a, b, a * c]
        elif k == 1:
            q = "%d × %d ＋ %d × %d ＝ □ ×（%d ＋ %d），□ 是多少？" % (b, a, c, a, b, c)
            v, w = a, [b + c, a * 2, b]
        elif k == 2:
            if b <= c:
                return None
            q = "（%d － %d）× %d ＝ %d × %d － □ × %d，□ 是多少？" % (b, c, a, b, a, a)
            v, w = c, [b - c, a, a * c]
        else:
            q = "%d × □ ＋ %d × %d ＝ %d ×（%d ＋ %d），□ 是多少？" % (a, a, c, a, b, c)
            v, w = b, [c, a, b + c]
        return mcq(q, str(v), [str(x) for x in w + [v + 1, v + 2] if x != v], "等號兩邊都是同一個數乘兩個數的%s，對照一下：□ ＝ %d。" % ("差" if "－" in q else "和", v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def near():
        a = R.randint(12, 89)
        m = R.choice([99, 101, 98, 102, 999, 1001])
        base = 100 if m < 500 else 1000
        d = m - base
        v = a * m
        if d < 0:
            q = "用簡便方法算：%d × %d" % (a, m)
            e = "%d × %d ＝ %d ×（%d － %d）＝ %s － %d ＝ %s。" % (a, m, a, base, -d, num(a * base), a * -d, num(v))
            w = [a * base - (-d), a * base - a, v + a]
        else:
            q = "用簡便方法算：%d × %d" % (a, m)
            e = "%d × %d ＝ %d ×（%d ＋ %d）＝ %s ＋ %d ＝ %s。" % (a, m, a, base, d, num(a * base), a * d, num(v))
            w = [a * base + d, a * base + a * d + a, v - a]
        return mcq(q, num(v), [num(x) for x in w if x != v], e)

    def combine():
        a = R.choice([25, 36, 48, 125, 17, 64])
        b = R.randint(11, 89)
        c = (100 - b) if R.random() < .6 else (b - R.choice([10, 20, 30]) if b > 40 else 100 - b)
        op = "＋" if b + c in (100,) else "－"
        if op == "－":
            c = b - R.choice([10, 20, 30])
            if c <= 0:
                return None
        s = b + c if op == "＋" else b - c
        v = a * s
        q = "用簡便方法算：%d × %d %s %d × %d" % (a, b, op, a, c)
        e = "＝ %d ×（%d %s %d）＝ %d × %d ＝ %s。" % (a, b, op, c, a, s, num(v))
        return mcq(q, num(v), [num(x) for x in (a * s + a, a * b + c if op == "＋" else a * b - c, v - 10 * a, v + 10)], e)
    return pick_unique(R, near, 10, seen) + pick_unique(R, combine, 10, seen)


def s4(seen):
    def md():
        c = R.choice([3, 4, 5, 6, 7, 8, 9, 12, 15])
        a = c * R.randint(4, 30)
        b = R.randint(3, 25)
        k = R.choice(["swap", "dd", "mul"])
        if k == "swap":
            q = "%d × %d ÷ %d 和下面哪一個算式的答案一樣？" % (b, a, c)
            ans = "%d ÷ %d × %d" % (a, c, b)
            w = ["%d ÷（%d × %d）" % (a, c, b), "%d × %d × %d" % (b, a, c), "%d ÷ %d ÷ %d" % (b, a, c) if False else "%d ×（%d ＋ %d）" % (b, a, c)]
            e = "乘除混合可以交換乘數和除數的位置：%d × %d ÷ %d ＝ %d ÷ %d × %d ＝ %s。" % (b, a, c, a, c, b, num(a * b // c))
        elif k == "dd":
            d = R.choice([2, 3, 4, 5])
            a2 = c * d * R.randint(2, 12)
            q = "%d ÷ %d ÷ %d 和下面哪一個算式的答案一樣？" % (a2, c, d)
            ans = "%d ÷（%d × %d）" % (a2, c, d)
            w = ["%d ÷（%d ÷ %d）" % (a2, c, d), "%d ÷ %d × %d" % (a2, c, d), "%d ×（%d ÷ %d）" % (a2, c, d)]
            e = "連續除以兩個數，等於除以它們的積：%d ÷ %d ÷ %d ＝ %d ÷ %d ＝ %d。" % (a2, c, d, a2, c * d, a2 // (c * d))
        else:
            q = "計算：%d × %d ÷ %d ＝ ？" % (b, a, c)
            v = a * b // c
            return mcq(q, num(v), [num(x) for x in (b * c, a * b, v + b, (a // c) + b) if x != v],
                       "先算 %d ÷ %d ＝ %d 比較簡單，再乘 %d：%d × %d ＝ %s。" % (a, c, a // c, b, a // c, b, num(v)))
        return mcq(q, ans, w, e)
    return pick_unique(R, md, 20, seen)


def s5(seen):
    def outfit():
        n = R.randint(6, 25)
        p, q2 = R.choice([(350, 250), (420, 180), (275, 225), (199, 101), (480, 320), (365, 135)])
        q = "學校買 %d 套運動服，每件上衣 %d 元、每件褲子 %d 元。一共要付多少元？" % (n, p, q2)
        v = n * (p + q2)
        return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in (n * p + q2, (p + q2) * (n - 1), n * p, v + p)],
                   "用分配律：%d × %d ＋ %d × %d ＝ %d ×（%d ＋ %d）＝ %d × %d ＝ %s（元）。" % (n, p, n, q2, n, p, q2, n, p + q2, num(v)))

    def rect():
        h = R.randint(8, 25)
        a, b = R.randint(12, 40), R.randint(5, 30)
        q = "一塊長方形菜園寬 %d 公尺，分成長 %d 公尺和長 %d 公尺的兩塊。整塊菜園的面積是多少平方公尺？" % (h, a, b)
        v = h * (a + b)
        return mcq(q, "%s 平方公尺" % num(v), ["%s 平方公尺" % num(x) for x in (h * a + b, 2 * (h + a + b), h * a, v + h)],
                   "%d × %d ＋ %d × %d ＝ %d ×（%d ＋ %d）＝ %s（平方公尺）。" % (h, a, h, b, h, a, b, num(v)))

    def ticket():
        price = R.choice([99, 199, 299, 98, 49])
        n = R.randint(12, 45)
        who = NM.next()
        base = (price // 100 + 1) * 100 if price % 100 else price
        d = base - price
        v = n * price
        q = "%s的班上有 %d 人，每人買一張 %d 元的門票。一共要付多少元？" % (who, n, price)
        return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in (n * base - d, n * base, v + n, v - d * n + n) if x != v],
                   "%d × %d ＝ %d ×（%d － %d）＝ %s － %d ＝ %s（元）。" % (n, price, n, base, d, num(n * base), n * d, num(v)))
    return pick_unique(R, outfit, 7, seen) + pick_unique(R, rect, 7, seen) + pick_unique(R, ticket, 6, seen)


def main():
    seen = set()
    sets = [("認識分配律", s1(seen)), ("用分配律求□", s2(seen)), ("簡便計算", s3(seen)),
            ("乘除混合計算", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>分配律</b>：a ×（b ＋ c）＝ a × b ＋ a × c；a ×（b － c）＝ a × b － a × c。",
         "反過來，兩項都乘同一個數，可以合起來：25 × 37 ＋ 25 × 63 ＝ 25 ×（37 ＋ 63）。",
         "接近整百的數可以拆開：46 × 99 ＝ 46 ×（100 － 1）。",
         "乘除混合：a × b ÷ c ＝ a ÷ c × b；a ÷ b ÷ c ＝ a ÷（b × c）。"],
        [example("25 × 37 ＋ 25 × 63", ["兩項都乘 25：25 ×（37 ＋ 63）。", "＝ 25 × 100。"], "2500"),
         example("46 × 99", ["46 ×（100 － 1）＝ 4600 － 46。"], "4554")],
        [("8 ×（20 ＋ 3）＝ 8 × 20 ＋ 3", "3 也要乘 8：8 × 20 ＋ 8 × 3 ＝ 184"),
         ("46 × 99 ＝ 4600 － 1", "要減 46 個 1：4600 － 46"),
         ("120 ÷ 4 ÷ 2 ＝ 120 ÷（4 ÷ 2）", "連續除，要除以它們的積：120 ÷（4 × 2）")])
    faq = [{"q": "什麼是分配律？",
            "a": "一個數乘兩數的和（或差），等於這個數分別乘這兩個數再相加（或相減），例如 8 ×（20 ＋ 3）＝ 8 × 20 ＋ 8 × 3。"},
           {"q": "分配律有什麼用？",
            "a": "可以讓計算變簡單，例如 46 × 99 ＝ 4600 － 46、25 × 37 ＋ 25 × 63 ＝ 2500。108課綱 R-5-2 要求五年級把計算規律用在簡化混合計算。"},
           {"q": "連續除以兩個數可以怎麼算？",
            "a": "可以先把兩個除數相乘，再一次除，例如 360 ÷ 4 ÷ 9 ＝ 360 ÷ 36 ＝ 10。"}]
    make_unit(R, "grade-5", "distributive-property", "R-5-2",
              "四則計算規律（Ⅱ）：乘除混合計算。「乘法對加法或減法的分配律」。將計算規律應用於簡化混合計算。熟練整數四則混合計算。",
              "分配律與乘除混合計算",
              "五年級數學 分配律 練習題｜簡便計算・乘除混合 學習單（附解答）",
              "分配律",
              "國小五年級數學「分配律與乘除混合計算」免費學習單：乘法對加法和減法的分配律、用分配律求□、99 和 101 的簡便計算、乘除混合計算的規律與應用題。100題線上練習馬上對答案，附可列印解答。",
              "a ×（b ＋ c）＝ a × b ＋ a × c",
              "兩項都乘同一個數，可以合起來算，讓計算變簡單。",
              body, faq, sets, 25)


if __name__ == "__main__":
    main()
