# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：數的計算規律（108課綱 R-6-1）
  python3 tools/gen_tw_math_g6_calculation_rules.py
整數・小數・分數で同じ規律：交換律・結合律（0.25×4、1/3×3 を作る）、分配律（分數・小數）、除以一數＝乘以倒數（乘除一體）、簡便計算。
誤答：分配律で片方だけ掛ける、÷ を × に変えて倒數にしない、減法・除法で交換してしまう。
"""
import random
from fractions import Fraction as F
from decimal import Decimal as D
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff, num

R = random.Random(61014)
NM = Names(R)


def ds(x):
    x = D(x).normalize()
    t = format(x, "f")
    if "." in t:
        i, f = t.split(".")
        return num(int(i)) + "." + f
    return num(int(t))


def frs(v):
    return ff(v)


def s1(seen):
    def dec():
        a, b = R.choice([("0.25", 4), ("2.5", 4), ("1.25", 8), ("0.5", 2), ("0.125", 8), ("12.5", 8), ("0.2", 5), ("2.5", 40)])
        c = D(R.randint(3, 99)) / R.choice([1, 10])
        a = D(a)
        q = "用簡便方法算：%s × %s × %d" % (ds(a), ds(c), b)
        v = a * c * b
        return mcq(q, ds(v), [ds(x) for x in (v * 10, v / 10, a * c + b)], "交換和結合：%s × %d ＝ %s，再 × %s ＝ %s。" % (ds(a), b, ds(a * b), ds(c), ds(v)))

    def frac():
        d = R.choice([3, 4, 5, 6, 7, 8, 9])
        n = R.randint(1, d - 1)
        if F(n, d).denominator != d:
            return None
        k = R.randint(2, 9)
        x = R.randint(2, 30)
        q = "用簡便方法算：%s × %d × %d" % (fr(n, d), x, d * k)
        v = F(n, d) * x * d * k
        return mcq(q, frs(v), [frs(x_) for x_ in (v * d, F(n, d) * x + d * k, v + x)], "先算 %s × %d ＝ %d，再乘以 %d：%d × %d ＝ %s。" % (fr(n, d), d * k, n * k, x, n * k, x, frs(v)))
    return pick_unique(R, dec, 10, seen) + pick_unique(R, frac, 10, seen)


def s2(seen):
    def frac():
        d = R.choice([4, 5, 6, 7, 8, 9, 12])
        a = R.randint(1, d - 1)
        b = d - a
        if F(a, d).denominator != d or F(b, d).denominator != d:
            return None
        x = R.randint(3, 60)
        q = "用簡便方法算：%d × %s ＋ %d × %s" % (x, fr(a, d), x, fr(b, d))
        return mcq(q, str(x), [frs(F(x * a, d) + b), str(x * 2), frs(F(x, d))], "%d ×（%s ＋ %s）＝ %d × 1 ＝ %d。" % (x, fr(a, d), fr(b, d), x, x))

    def dec():
        a = D(R.randint(11, 99)) / 10
        b, c = R.choice([(D("3.7"), D("6.3")), (D("1.25"), D("8.75")), (D("4.6"), D("5.4")), (D("0.8"), D("9.2")), (D("2.5"), D("7.5")), (D("13.6"), D("6.4"))])
        tot = b + c
        q = "用簡便方法算：%s × %s ＋ %s × %s" % (ds(a), ds(b), ds(a), ds(c))
        v = a * tot
        return mcq(q, ds(v), [ds(x) for x in (a * b + c, v / 10, v + a)], "%s ×（%s ＋ %s）＝ %s × %s ＝ %s。" % (ds(a), ds(b), ds(c), ds(a), ds(tot), ds(v)))

    def mix():
        d = R.choice([3, 4, 5, 6, 8])
        n = R.randint(1, d - 1)
        if F(n, d).denominator != d:
            return None
        k = R.randint(2, 9)
        q = "%s ×（%d ＋ %s）＝" % (fr(n, d), d * k, fr(d, n) if F(d, n).denominator == n else fr(d * 2, n))
        y = F(d, n) if F(d, n).denominator == n else F(2 * d, n)
        v = F(n, d) * (d * k + y)
        return mcq(q, frs(v), [frs(x) for x in (F(n, d) * d * k + y, v + 1, F(n, d) + d * k + y)], "分配律：%s × %d ＋ %s × %s ＝ %d ＋ %s ＝ %s。" % (fr(n, d), d * k, fr(n, d), frs(y), n * k, frs(F(n, d) * y), frs(v)))
    return pick_unique(R, frac, 7, seen) + pick_unique(R, dec, 7, seen) + pick_unique(R, mix, 6, seen)


def s3(seen):
    def mk():
        kind = R.choice(["int", "frac", "dec"])
        if kind == "int":
            a, b = R.randint(12, 200), R.randint(2, 9)
            q = "%d ÷ %d 和下面哪一個算式相等？" % (a, b)
            ans = "%d × %s" % (a, fr(1, b))
            w = ["%d × %d" % (a, b), "%d ÷ %s" % (a, fr(1, b)), "%s × %d" % (fr(1, a), b)]
        elif kind == "frac":
            n, d = R.randint(1, 8), R.randint(2, 9)
            if n == d or F(n, d).denominator != d:
                return None
            a = R.randint(2, 30)
            q = "%d ÷ %s 和下面哪一個算式相等？" % (a, fr(n, d))
            ans = "%d × %s" % (a, fr(d, n) if n != 1 else str(d))
            w = ["%d × %s" % (a, fr(n, d)), "%s × %d" % (fr(d, n) if n != 1 else str(d), 1) if False else "%d ÷ %s" % (a, fr(d, n) if n != 1 else str(d)), "%s ÷ %d" % (fr(n, d), a)]
        else:
            b = R.choice(["0.5", "0.25", "0.2", "0.1", "0.125"])
            a = R.randint(3, 40)
            inv = int(1 / D(b))
            q = "%d ÷ %s 和下面哪一個算式相等？" % (a, b)
            ans = "%d × %d" % (a, inv)
            w = ["%d ÷ %d" % (a, inv), "%d × %s" % (a, b), "%d ＋ %d" % (a, inv)]
        return mcq(q, ans, w, "除以一個數，等於乘以它的倒數。乘法和除法其實是一體的。")
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    TRUE = ["%s × %s ＝ %s × %s", "（%s ＋ %s）＋ %s ＝ %s ＋（%s ＋ %s）"]

    def mk():
        a = R.choice([D("0.6"), D("1.2"), D("2.5"), D("3.4")])
        b = R.choice([fr(1, 2), fr(3, 4), fr(2, 5), fr(5, 6)])
        c = R.randint(2, 9)
        ok_list = ["%s × %s ＝ %s × %s" % (ds(a), b, b, ds(a)),
                   "%s ×（%s ＋ %d）＝ %s × %s ＋ %s × %d" % (b, ds(a), c, b, ds(a), b, c),
                   "%s ÷ %d ＝ %s × %s" % (ds(a), c, ds(a), fr(1, c))]
        bad_list = ["%s － %d ＝ %d － %s" % (ds(a), c, c, ds(a)),
                    "%s ÷ %d ＝ %d ÷ %s" % (ds(a), c, c, ds(a)),
                    "%s ×（%s ＋ %d）＝ %s × %s ＋ %d" % (b, ds(a), c, b, ds(a), c),
                    "%s ÷ %d ＝ %s × %d" % (ds(a), c, ds(a), c)]
        if R.random() < .5:
            ans = R.choice(ok_list)
            opts = R.sample(bad_list, 3)
            q = "下面哪一個等式<b>一定成立</b>？"
            e = "成立的是：%s。交換律、結合律、分配律對整數、小數、分數都一樣適用；減法和除法不能交換。" % ans
        else:
            ans = R.choice(bad_list)
            opts = R.sample(ok_list, 3)
            q = "下面哪一個等式<b>不成立</b>？"
            e = "不成立的是：%s。減法和除法不能交換；分配律要把每一項都乘到；除以一個數要乘以它的倒數。" % ans
        st = opts + [ans]
        R.shuffle(st)
        L = "甲乙丙丁"
        k = st.index(ans)
        q += "<br>" + "<br>".join("%s：%s" % (L[i], t) for i, t in enumerate(st))
        return mcq(q, L[k], [x for x in L if x != L[k]], L[k] + "。" + e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def price():
        p = D(R.choice(["1.25", "2.5", "0.75", "1.5", "3.2", "2.4"]))
        n1, n2 = R.randint(3, 9), R.randint(3, 9)
        q = "一包麵粉重 %s 公斤。甲買 %d 包，乙買 %d 包。兩人一共買了幾公斤？" % (ds(p), n1, n2)
        v = p * (n1 + n2)
        return mcq(q, "%s 公斤" % ds(v), ["%s 公斤" % ds(x) for x in (p * n1 + n2, v / 10, v + p)], "%s × %d ＋ %s × %d ＝ %s ×（%d ＋ %d）＝ %s × %d ＝ %s（公斤）。" % (ds(p), n1, ds(p), n2, ds(p), n1, n2, ds(p), n1 + n2, ds(v)))

    def cake():
        d = R.choice([3, 4, 5, 6, 8])
        n = R.randint(1, d - 1)
        if F(n, d).denominator != d:
            return None
        k = R.randint(2, 6)
        who = NM.next()
        q = "%s每天吃 %s 個麵包，%d 週（每週 7 天）要吃幾個麵包？" % (who, fr(n, d), d * k if False else k)
        v = F(n, d) * 7 * k
        return mcq(q, "%s 個" % frs(v), ["%s 個" % frs(x) for x in (F(n, d) * 7 + k, F(n, d) * k, v + 1)], "%s × 7 × %d ＝ %s × %d ＝ %s（個）。" % (fr(n, d), k, frs(F(n * 7, d)), k, frs(v)))

    def area():
        L = D(R.randint(21, 79)) / 10
        w1, w2 = R.choice([(D("3.6"), D("6.4")), (D("2.5"), D("7.5")), (D("1.8"), D("8.2")), (D("4.3"), D("5.7"))])
        q = "兩塊長方形菜園的長都是 %s 公尺，寬分別是 %s 公尺和 %s 公尺。兩塊一共多少平方公尺？" % (ds(L), ds(w1), ds(w2))
        v = L * (w1 + w2)
        return mcq(q, "%s 平方公尺" % ds(v), ["%s 平方公尺" % ds(x) for x in (L * w1 + w2, (L + w1 + w2) * 2, v / 10)], "%s ×（%s ＋ %s）＝ %s × 10 ＝ %s（平方公尺）。" % (ds(L), ds(w1), ds(w2), ds(L), ds(v)))
    return pick_unique(R, price, 7, seen) + pick_unique(R, cake, 6, seen) + pick_unique(R, area, 7, seen)


def main():
    seen = set()
    sets = [("交換律和結合律", s1(seen)), ("分配律", s2(seen)), ("乘除一體：乘以倒數", s3(seen)),
            ("判斷等式成不成立", s4(seen)), ("應用", s5(seen))]
    body = lesson(
        ["整數、小數、分數<b>都是數</b>，計算規律一樣：交換律、結合律、分配律都可以用。",
         "找能湊成整數的數先算：0.25 × 4 ＝ 1，<span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> × 3 ＝ 2。",
         "<b>除以一個數，等於乘以它的倒數</b>：12 ÷ 4 ＝ 12 × <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>。乘法和除法是一體的。",
         "減法和除法不能交換順序。"],
        [example("2.5 × 7.3 × 4", ["2.5 × 4 ＝ 10。", "10 × 7.3 ＝ 73。"], "73"),
         example("18 × <span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> ＋ 18 × <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>", ["18 ×（<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> ＋ <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>）＝ 18 × 1。"], "18")],
        [("<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> ×（8 ＋ 6）＝ 4 ＋ 6", "6 也要乘：4 ＋ 3 ＝ 7"),
         ("12 ÷ 3 ＝ 3 ÷ 12", "除法不能交換"),
         ("6 ÷ <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> ＝ 6 × <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span>", "要乘以倒數 <span class='fr'><span class='fn'>3</span><span class='fd'>2</span></span>")])
    faq = [{"q": "分數和小數也能用交換律、分配律嗎？",
            "a": "可以。整數、小數、分數都是數，享有一樣的計算規律，例如 2.5 × 7.3 × 4 ＝ 2.5 × 4 × 7.3 ＝ 73。"},
           {"q": "什麼是「乘除一體」？",
            "a": "除以一個數就等於乘以它的倒數，所以除法可以改寫成乘法，例如 15 ÷ 0.5 ＝ 15 × 2。"},
           {"q": "六年級的計算規律要學什麼？",
            "a": "108課綱 R-6-1：認識整數、小數、分數都是數，享有一樣的計算規律，並逐漸體會乘法和除法的計算實為一體。"}]
    make_unit(R, "grade-6", "calculation-rules", "R-6-1",
              "數的計算規律：小學最後應認識（1）整數、小數、分數都是數，享有一樣的計算規律。（2）整數乘除計算及規律，因分數運算更容易理解。（3）逐漸體會乘法和除法的計算實為一體。併入其他教學活動。",
              "數的計算規律：交換律、結合律、分配律",
              "六年級數學 計算規律 練習題｜分數小數的簡便計算・乘以倒數 學習單（附解答）",
              "數的計算規律",
              "國小六年級數學「數的計算規律」免費學習單：分數和小數的交換律、結合律、分配律，除以一數等於乘以倒數，判斷等式成不成立與簡便計算應用題。100題線上練習馬上對答案，附可列印解答。",
              "整數、小數、分數的計算規律都一樣",
              "除以一個數，等於乘以它的倒數。",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
