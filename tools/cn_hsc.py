# -*- coding: utf-8 -*-
"""
中国 高中 选择性必修第二册（数列、导数、导数的应用）と选择性必修第三册（计数原理、二项式定理、随机变量及其分布、
条件概率与正态分布、成对数据的统计分析）。問題はすべて自前（cn_hsu の部品）。
  python3 tools/cn_hsc.py elective-2|elective-3 [slug…]
"""
import math
import random
from fractions import Fraction as F
import cn_hsu as U
from cn_hsu import mcq, S, P, poly, lin, sup, rt, pis, dec, M, C, A
from cn_common import run_grade, lesson
from ws_common import fr

STD_D = "理解等差数列、等比数列的通项公式和前 n 项和公式；理解导数的概念和几何意义，会求基本初等函数的导数，会用导数求切线、单调区间、极值和最值"
STD_C = "理解分类加法计数原理和分步乘法计数原理，排列与组合，二项式定理；理解离散型随机变量的分布列、均值和方差，二项分布、超几何分布、正态分布；理解条件概率和全概率公式；会用相关系数、一元线性回归模型和独立性检验分析成对数据"

UNITS = {"elective-2": {}, "elective-3": {}}


def Un(g, slug, **kw):
    UNITS[g][slug] = kw


def L(think, ex, mist):
    return lesson(think, ex, mist)


SUBT = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def sub(name, i):
    return "%s%s" % (name, str(i).translate(SUBT))


# ================================================================== 数列
def seq(kind):
    def mk():
        r = U.R
        a1, d = r.randint(-10, 15), U.nz(-6, 6)
        if kind == "an":
            n = r.randint(5, 30)
            t = r.randint(0, 1)
            if t == 0:
                v = a1 + (n - 1) * d
                return mcq("等差数列 {aₙ} 中，a₁ ＝ %s，公差 d ＝ %s，%s ＝ ？" % (S(a1), S(d), sub("a", n)), S(v), [S(a1 + n * d), S(a1 + (n - 2) * d), S(n * d)],
                           "aₙ ＝ a₁ ＋ (n － 1)d ＝ %s ＋ %d × %s ＝ <b>%s</b>。" % (S(a1), n - 1, P(d), S(v)))
            m, k = sorted(r.sample(range(2, 12), 2))
            am, ak = a1 + (m - 1) * d, a1 + (k - 1) * d
            return mcq("等差数列 {aₙ} 中，%s ＝ %s，%s ＝ %s，公差 d ＝ ？" % (sub("a", m), S(am), sub("a", k), S(ak)), S(d), [S(-d), S(F(ak - am, k - m + 1)), S(ak - am)],
                       "d ＝ (%s － %s) ÷ (%d － %d) ＝ <b>%s</b>。" % (sub("a", k), sub("a", m), k, m, S(d)))
        if kind == "sn":
            n = r.randint(5, 20)
            v = n * a1 + n * (n - 1) * d // 2
            if r.random() < 0.5:
                return mcq("等差数列 {aₙ} 中，a₁ ＝ %s，d ＝ %s，前 %d 项和 %s ＝ ？" % (S(a1), S(d), n, sub("S", n)), S(v), [S(n * a1 + n * n * d // 2), S(a1 + (n - 1) * d), S(n * a1 + (n + 1) * n * d // 2)],
                           "Sₙ ＝ na₁ ＋ n(n － 1)d/2 ＝ %d × %s ＋ %d × %s ＝ <b>%s</b>。" % (n, P(a1), n * (n - 1) // 2, P(d), S(v)))
            n = r.choice([9, 11, 13, 15, 17])
            mid = r.randint(-8, 12)
            return mcq("等差数列 {aₙ} 中，%s ＝ %s，前 %d 项和 %s ＝ ？" % (sub("a", (n + 1) // 2), S(mid), n, sub("S", n)), S(n * mid), [S((n - 1) * mid), S(n * mid // 2) if mid % 2 == 0 else S(n * mid + n), S(2 * n * mid)],
                       "%s ＝ n(a₁ ＋ aₙ)/2 ＝ %d × %s ＝ <b>%s</b>（a₁ ＋ %s ＝ 2%s）。" % (sub("S", n), n, sub("a", (n + 1) // 2), S(n * mid), sub("a", n), sub("a", (n + 1) // 2)))
        if kind == "gn":
            a1 = r.choice([1, 2, 3, -1, -2, 4, 5])
            q = r.choice([2, 3, -2, -3, F(1, 2), F(-1, 2), F(1, 3)])
            n = r.randint(3, 7)
            v = a1 * F(q) ** (n - 1)
            if abs(v) > 5000:
                return None
            if r.random() < 0.6:
                return mcq("等比数列 {aₙ} 中，a₁ ＝ %s，公比 q ＝ %s，%s ＝ ？" % (S(a1), S(q), sub("a", n)), S(v), [S(a1 * F(q) ** n), S(a1 * F(q) ** (n - 2)), S(-v)],
                           "aₙ ＝ a₁qⁿ⁻¹ ＝ %s × %s%s ＝ <b>%s</b>。" % (S(a1), P(q), sup(n - 1), S(v)))
            a2, a5 = a1 * F(q), a1 * F(q) ** 4
            return mcq("等比数列 {aₙ} 中，a₂ ＝ %s，a₅ ＝ %s，公比 q ＝ ？" % (S(a2), S(a5)), S(q), [S(-q), S(F(q) ** 2), S(1 / F(q))],
                       "q³ ＝ a₅ ÷ a₂ ＝ %s，<b>q ＝ %s</b>。" % (S(F(q) ** 3), S(q)))
        if kind == "gs":
            a1 = r.choice([1, 2, 3, 4, 5])
            q = r.choice([2, 3, F(1, 2), -2])
            n = r.randint(3, 8)
            v = a1 * (1 - F(q) ** n) / (1 - F(q))
            if abs(v) > 20000:
                return None
            return mcq("等比数列 {aₙ} 中，a₁ ＝ %s，q ＝ %s，前 %d 项和 %s ＝ ？" % (S(a1), S(q), n, sub("S", n)), S(v), [S(a1 * (1 - F(q) ** (n + 1)) / (1 - F(q))), S(a1 * F(q) ** (n - 1)), S(a1 * (1 - F(q) ** (n - 1)) / (1 - F(q)))],
                       "Sₙ ＝ a₁(1 － qⁿ) ÷ (1 － q) ＝ <b>%s</b>。" % S(v))
        t = r.randint(0, 2)
        if t == 0:
            # Sₙ ＝ An² ＋ Bn → aₙ ＝ Sₙ － Sₙ₋₁ ＝ 2An － A ＋ B
            Aa, Bb = U.nz(-4, 4), r.randint(-6, 6)
            n = r.randint(3, 15)
            v = Aa * (2 * n - 1) + Bb
            return mcq("数列 {aₙ} 的前 n 项和 Sₙ ＝ %s，%s ＝ ？" % (poly([Aa, Bb, 0], "n"), sub("a", n)), S(v), [S(Aa * n * n + Bb * n), S(Aa * (2 * n + 1) + Bb), S(2 * Aa * n + Bb)],
                       "aₙ ＝ Sₙ － Sₙ₋₁：%s ＝ %s － %s ＝ <b>%s</b>。" % (sub("a", n), sub("S", n), sub("S", n - 1), S(v)))
        if t == 1:
            a1, k = r.randint(1, 5), r.randint(1, 4)
            a = a1
            for _ in range(4):
                a = 2 * a + k
            return mcq("数列 {aₙ} 满足 a₁ ＝ %d，aₙ₊₁ ＝ 2aₙ ＋ %d，a₅ ＝ ？" % (a1, k), str(a), [str(a - k), str(a1 * 16), str(2 * a + k)],
                       "依次计算 a₂、a₃、a₄、a₅，得 <b>a₅ ＝ %d</b>。" % a)
        a1 = r.randint(1, 6)
        n = r.randint(4, 8)
        v = a1 + n * (n - 1) // 2
        return mcq("数列 {aₙ} 满足 a₁ ＝ %d，aₙ₊₁ ＝ aₙ ＋ n，%s ＝ ？" % (a1, sub("a", n)), str(v), [str(a1 + n * (n + 1) // 2), str(a1 + (n - 1) * (n - 2) // 2), str(a1 * n)],
                   "累加：aₙ ＝ a₁ ＋ (1 ＋ 2 ＋ … ＋ (n － 1)) ＝ %d ＋ %d ＝ <b>%d</b>。" % (a1, n * (n - 1) // 2, v))
    return mk


Un("elective-2", "sequences", sort=1, dom="F", std=STD_D, seed=204101,
   title="数列：等差数列和等比数列的通项与求和", short="数列",
   meta="高中数学选择性必修第二册“数列”练习题：等差数列的通项公式和前 n 项和，等比数列的通项公式和前 n 项和，由 Sₙ 求 aₙ，递推数列，100题在线练习，附可打印答案。",
   kb="等差 aₙ ＝ a₁ ＋ (n － 1)d，等比 aₙ ＝ a₁qⁿ⁻¹", ks="等差 Sₙ ＝ n(a₁ ＋ aₙ)/2；等比 Sₙ ＝ a₁(1 － qⁿ)/(1 － q)（q ≠ 1）；aₙ ＝ Sₙ － Sₙ₋₁（n ≥ 2）。",
   body=L(["<b>等差数列</b>：aₙ ＝ a₁ ＋ (n － 1)d，Sₙ ＝ n(a₁ ＋ aₙ)/2 ＝ na₁ ＋ n(n － 1)d/2。若 m ＋ n ＝ p ＋ q，则 aₘ ＋ aₙ ＝ aₚ ＋ a_q。",
           "<b>等比数列</b>：aₙ ＝ a₁qⁿ⁻¹，q ≠ 1 时 Sₙ ＝ a₁(1 － qⁿ)/(1 － q)。",
           "已知 Sₙ 求 aₙ：n ＝ 1 时 a₁ ＝ S₁，n ≥ 2 时 aₙ ＝ Sₙ － Sₙ₋₁。递推数列可以依次计算，或用累加、累乘。"],
          [("a₁ ＝ 3，d ＝ 2，求 a₁₀", ["3 ＋ 9 × 2"], "21"), ("a₁ ＝ 1，q ＝ 2，求 S₅", ["(1 － 32) ÷ (1 － 2)"], "31")],
          [("通项公式写成 a₁ ＋ nd", "是 a₁ ＋ (n － 1)d，第 1 项时 n － 1 ＝ 0。"),
           ("等比求和忘了 q ＝ 1 的情况", "q ＝ 1 时 Sₙ ＝ na₁。"),
           ("由 Sₙ 求 aₙ 时忘了检验 n ＝ 1", "要检验 a₁ 是否满足 n ≥ 2 时的式子。")]),
   faq=[("等差中项和等比中项是什么？", "a、A、b 成等差数列时 A ＝ (a ＋ b)/2；a、G、b 成等比数列时 G² ＝ ab。")],
   spec=lambda: [("等差数列的通项", [(seq("an"), 20)]), ("等差数列的前 n 项和", [(seq("sn"), 20)]), ("等比数列的通项", [(seq("gn"), 20)]),
                 ("等比数列的前 n 项和", [(seq("gs"), 20)]), ("由 Sₙ 求 aₙ 和递推数列", [(seq("rec"), 20)])])


# ================================================================== 导数
def dpoly(cs):
    n = len(cs) - 1
    return [c * (n - i) for i, c in enumerate(cs[:-1])]


def peval(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def deriv(kind):
    def mk():
        r = U.R
        if kind == "rate":
            a, b, c = U.nz(-3, 3), r.randint(-5, 5), r.randint(-5, 5)
            x1, x2 = sorted(r.sample(range(-3, 5), 2))
            f = [a, b, c]
            v = F(peval(f, x2) - peval(f, x1), x2 - x1)
            return mcq("函数 f(x) ＝ %s 在区间 [%s, %s] 上的平均变化率是多少？" % (poly(f), S(x1), S(x2)), S(v), [S(peval(f, x2) - peval(f, x1)), S(peval(dpoly(f), x1)), S(-v) if v else "1"],
                       "平均变化率 ＝ [f(%s) － f(%s)] ÷ (%s － %s) ＝ (%s － %s) ÷ %d ＝ <b>%s</b>。" % (S(x2), S(x1), S(x2), P(x1), S(peval(f, x2)), P(peval(f, x1)), x2 - x1, S(v)))
        if kind == "basic":
            t = r.randint(0, 1)
            if t == 0:
                cs = [r.randint(-4, 4) for _ in range(4)]
                cs[0] = U.nz(-4, 4)
                d = dpoly(cs)
                return mcq("f(x) ＝ %s，f′(x) ＝ ？" % poly(cs), poly(d), [poly(d + [cs[-1]]) if cs[-1] else poly([d[0], d[1], d[2] + 1]), poly([cs[0], cs[1], cs[2]]), poly([x * 2 for x in d])],
                           "(xⁿ)′ ＝ nxⁿ⁻¹，常数的导数是 0：<b>%s</b>。" % poly(d))
            POOL = [("√x", fr(1, "2√x"), ["2√x", fr(1, "√x"), fr("√x", 2)]), (fr(1, "x"), M + fr(1, "x²"), [fr(1, "x²"), "ln x", M + fr(1, "x")]),
                    ("sin x", "cos x", ["－cos x", "－sin x", "sin x"]), ("cos x", "－sin x", ["sin x", "cos x", "－cos x"]),
                    ("eˣ", "eˣ", ["xeˣ⁻¹", "eˣ⁻¹", "ln x"]), ("ln x", fr(1, "x"), ["eˣ", M + fr(1, "x"), "x ln x"]), ("2ˣ", "2ˣ ln 2", ["x · 2ˣ⁻¹", "2ˣ", fr("2ˣ", "ln 2")]),
                    ("log₂x", fr(1, "x ln 2"), [fr(1, "x"), fr("ln 2", "x"), "x ln 2"]), ("3ˣ", "3ˣ ln 3", ["x · 3ˣ⁻¹", "3ˣ", fr("3ˣ", "ln 3")]),
                    ("x⁻²", "－2x⁻³", ["－2x⁻¹", "2x⁻³", "－x⁻³"]), ("x<sup>3/2</sup>", fr(3, 2) + "x<sup>1/2</sup>", [fr(3, 2) + "x<sup>5/2</sup>", fr(2, 3) + "x<sup>1/2</sup>", "x<sup>1/2</sup>"]),
                    ("∛x", fr(1, "3∛(x²)"), [fr(1, "3∛x"), "3∛(x²)", fr(1, "∛(x²)")]), ("x⁵", "5x⁴", ["x⁴", "5x⁵", "4x⁵"]), ("x¹⁰", "10x⁹", ["x⁹", "9x¹⁰", "10x¹¹"])]
            f, d, w = r.choice(POOL)
            return mcq("f(x) ＝ %s，f′(x) ＝ ？" % f, d, w, "基本初等函数的导数公式：(%s)′ ＝ <b>%s</b>。" % (f, d))
        if kind == "rules":
            t = r.randint(0, 4)
            a = r.randint(2, 6)
            b = r.randint(-5, 5)
            if t == 0:
                return mcq("f(x) ＝ x²eˣ，f′(x) ＝ ？", "(x² ＋ 2x)eˣ", ["2xeˣ", "x²eˣ", "(x² － 2x)eˣ"], "乘积的导数：(uv)′ ＝ u′v ＋ uv′ ＝ 2xeˣ ＋ x²eˣ ＝ <b>(x² ＋ 2x)eˣ</b>。") if r.random() < 0.2 else \
                    mcq("f(x) ＝ %sx ln x，f′(x) ＝ ？" % ("" if a == 1 else a), "%s(ln x ＋ 1)" % a, ["%s ln x" % a, "%s/x" % a, "%s(ln x － 1)" % a],
                        "(x ln x)′ ＝ ln x ＋ x · 1/x ＝ ln x ＋ 1，所以 f′(x) ＝ <b>%d(ln x ＋ 1)</b>。" % a)
            if t == 1:
                ins = lin(a, b)
                return mcq("f(x) ＝ ln(%s)，f′(x) ＝ ？" % ins, fr(a, ins), [fr(1, ins), fr(a, "x"), "%d ln(%s)" % (a, ins)],
                           "复合函数求导：[ln u]′ ＝ u′/u，u′ ＝ %d，f′(x) ＝ <b>%s</b>。" % (a, fr(a, ins)))
            if t == 2:
                fn = r.choice(["sin", "cos"])
                ins = lin(a, b)
                d = ("%dcos(%s)" % (a, ins)) if fn == "sin" else ("－%dsin(%s)" % (a, ins))
                return mcq("f(x) ＝ %s(%s)，f′(x) ＝ ？" % (fn, ins), d,
                           ["cos(%s)" % ins if fn == "sin" else "－sin(%s)" % ins, ("－%dcos(%s)" % (a, ins)) if fn == "sin" else ("%dsin(%s)" % (a, ins)), ("%dsin(%s)" % (a, ins)) if fn == "sin" else ("%dcos(%s)" % (a, ins))],
                           "复合函数求导：外层求导再乘内层的导数 %d，<b>%s</b>。" % (a, d))
            if t == 3:
                return mcq("f(x) ＝ e<sup>%s</sup>，f′(x) ＝ ？" % lin(a, b), "%de<sup>%s</sup>" % (a, lin(a, b)), ["e<sup>%s</sup>" % lin(a, b), "%se<sup>%s</sup>" % (lin(a, b), lin(a, b - 1) if b != 1 else "%dx" % a), "%de<sup>%s</sup>" % (a, lin(a, b - 1)) if b != 1 else "%de<sup>%dx</sup>" % (a, a)],
                           "(eᵘ)′ ＝ eᵘ · u′ ＝ <b>%de<sup>%s</sup></b>。" % (a, lin(a, b)))
            return mcq("f(x) ＝ %s，f′(x) ＝ ？" % fr("x", lin(1, a)), fr(a, "(%s)²" % lin(1, a)), [fr(1, "(%s)²" % lin(1, a)), fr(-a if False else "x", "(%s)²" % lin(1, a)), fr(2 * a, "(%s)²" % lin(1, a))],
                       "商的导数：(u/v)′ ＝ (u′v － uv′)/v² ＝ (x ＋ %d － x)/(x ＋ %d)² ＝ <b>%s</b>。" % (a, a, fr(a, "(%s)²" % lin(1, a))))
        if kind == "tangent":
            cs = [r.choice([1, -1, 2]), r.randint(-3, 3), r.randint(-4, 4), r.randint(-4, 4)]
            if r.random() < 0.5:
                cs = cs[1:]
                if cs[0] == 0:
                    cs[0] = 1
            x0 = r.randint(-2, 2)
            y0 = peval(cs, x0)
            k = peval(dpoly(cs), x0)
            b = y0 - k * x0
            ans = "y ＝ %s" % (lin(k, b) if k else S(b))
            return mcq("曲线 y ＝ %s 在点 (%s, %s) 处的切线方程是什么？" % (poly(cs), S(x0), S(y0)), ans,
                       ["y ＝ %s" % (lin(k, -b) if k else S(-b)), "y ＝ %s" % (lin(k + 1, b - x0) if k + 1 else S(b - x0)), "y ＝ %s" % lin(y0 if y0 else 1, -k * x0 if x0 else k)],
                       "f′(x) ＝ %s，斜率 k ＝ f′(%s) ＝ %s，切线 y － %s ＝ %s(x － %s)，即 <b>%s</b>。" % (poly(dpoly(cs)), S(x0), S(k), P(y0), S(k), P(x0), ans))
        cs = [r.randint(-3, 3) for _ in range(4)]
        cs[0] = U.nz(-3, 3)
        x0 = r.randint(-3, 3)
        v = peval(dpoly(cs), x0)
        return mcq("f(x) ＝ %s，f′(%s) ＝ ？" % (poly(cs), S(x0)), S(v), [S(peval(cs, x0)), S(v + cs[-1] if cs[-1] else v + 1), S(-v) if v else "1"],
                   "f′(x) ＝ %s，f′(%s) ＝ <b>%s</b>。" % (poly(dpoly(cs)), S(x0), S(v)))
    return mk


Un("elective-2", "derivatives", sort=2, dom="F", std=STD_D, seed=204102,
   title="导数：平均变化率、导数公式、运算法则和切线", short="导数及其运算",
   meta="高中数学选择性必修第二册“导数及其运算”练习题：平均变化率，基本初等函数的导数公式，导数的运算法则和复合函数求导，切线方程，求导数值，100题在线练习，附可打印答案。",
   kb="f′(x₀) 是曲线 y ＝ f(x) 在点 (x₀, f(x₀)) 处切线的斜率", ks="(xⁿ)′ ＝ nxⁿ⁻¹，(sin x)′ ＝ cos x，(eˣ)′ ＝ eˣ，(ln x)′ ＝ 1/x；(uv)′ ＝ u′v ＋ uv′。",
   body=L(["<b>导数</b> f′(x₀) ＝ lim[f(x₀ ＋ Δx) － f(x₀)]/Δx，是瞬时变化率，也是切线的斜率。",
           "<b>运算法则</b>：(u ± v)′ ＝ u′ ± v′，(uv)′ ＝ u′v ＋ uv′，(u/v)′ ＝ (u′v － uv′)/v²。复合函数 y ＝ f(g(x)) 的导数 y′ ＝ f′(g(x)) · g′(x)。",
           "<b>切线方程</b>：先求斜率 k ＝ f′(x₀)，再写 y － f(x₀) ＝ k(x － x₀)。"],
          [("y ＝ x³ 在 (1, 1) 处的切线", ["y′ ＝ 3x²，k ＝ 3", "y － 1 ＝ 3(x － 1)"], "y ＝ 3x － 2"), ("(sin 2x)′", ["cos 2x × 2"], "2cos 2x")],
          [("复合函数求导忘了乘内层的导数", "(sin 2x)′ ＝ 2cos 2x，不是 cos 2x。"),
           ("把 (uv)′ 写成 u′v′", "乘积的导数是 u′v ＋ uv′。"),
           ("切线方程用 f′(x) 而不是 f′(x₀)", "斜率是导函数在切点处的值。")]),
   faq=[("“在点 P 处的切线”和“过点 P 的切线”有什么不同？", "“在点 P 处”P 是切点；“过点 P”P 不一定是切点，要先设切点。")],
   spec=lambda: [("平均变化率", [(deriv("rate"), 20)]), ("基本初等函数的导数", [(deriv("basic"), 20)]), ("导数的运算法则", [(deriv("rules"), 20)]),
                 ("切线方程", [(deriv("tangent"), 20)]), ("求导数值", [(deriv("value"), 20)])])


def app(kind):
    def mk():
        r = U.R
        p, q = sorted(r.sample(range(-4, 6), 2))
        if (p + q) % 2:
            return None
        # f(x) ＝ x³ － (3/2)(p ＋ q)x² ＋ 3pq x ＋ c，f′ ＝ 3(x － p)(x － q)
        c = r.randint(-5, 5)
        cs = [1, F(-3 * (p + q), 2), 3 * p * q, c]
        f = poly(cs)
        if kind == "mono":
            if r.random() < 0.5:
                return mcq("函数 f(x) ＝ %s 的单调递减区间是什么？" % f, "(%s, %s)" % (S(p), S(q)), ["(－∞, %s)" % S(p), "(%s, ＋∞)" % S(q), "(%s, %s)" % (S(-q), S(-p))],
                           "f′(x) ＝ 3(x － %s)(x － %s)，f′(x) ＜ 0 得 %s ＜ x ＜ %s：<b>(%s, %s)</b>。" % (P(p), P(q), S(p), S(q), S(p), S(q)))
            return mcq("函数 f(x) ＝ %s 的单调递增区间是什么？" % f, "(－∞, %s) 和 (%s, ＋∞)" % (S(p), S(q)), ["(%s, %s)" % (S(p), S(q)), "(－∞, %s) 和 (%s, ＋∞)" % (S(-q), S(-p)), "(%s, ＋∞)" % S(p)],
                       "f′(x) ＝ 3(x － %s)(x － %s) ＞ 0，x ＜ %s 或 x ＞ %s：<b>(－∞, %s) 和 (%s, ＋∞)</b>。" % (P(p), P(q), S(p), S(q), S(p), S(q)))
        if kind == "ext":
            vp, vq = peval(cs, p), peval(cs, q)
            if r.random() < 0.5:
                return mcq("函数 f(x) ＝ %s 的极大值是多少？" % f, S(vp), [S(vq), S(p), S(peval(cs, 0)) if peval(cs, 0) != vp else S(vp + 1)],
                           "f′(x) ＝ 3(x － %s)(x － %s)，x ＝ %s 左增右减，是极大值点，极大值 f(%s) ＝ <b>%s</b>。" % (P(p), P(q), S(p), S(p), S(vp)))
            return mcq("函数 f(x) ＝ %s 的极小值是多少？" % f, S(vq), [S(vp), S(q), S(peval(cs, 0)) if peval(cs, 0) != vq else S(vq - 1)],
                       "x ＝ %s 左减右增，是极小值点，极小值 f(%s) ＝ <b>%s</b>。" % (S(q), S(q), S(vq)))
        if kind == "maxmin":
            lo, hi = p - r.randint(1, 2), q + r.randint(1, 2)
            vals = {x: peval(cs, x) for x in (lo, p, q, hi)}
            mx, mn = max(vals.values()), min(vals.values())
            if r.random() < 0.5:
                return mcq("函数 f(x) ＝ %s 在区间 [%s, %s] 上的最大值是多少？" % (f, S(lo), S(hi)), S(mx), [S(x) for x in set(vals.values()) if x != mx][:2] + [S(mx + 1)],
                           "比较极值 f(%s) ＝ %s、f(%s) ＝ %s 和端点值 f(%s) ＝ %s、f(%s) ＝ %s，最大值是 <b>%s</b>。" % (S(p), S(vals[p]), S(q), S(vals[q]), S(lo), S(vals[lo]), S(hi), S(vals[hi]), S(mx)))
            return mcq("函数 f(x) ＝ %s 在区间 [%s, %s] 上的最小值是多少？" % (f, S(lo), S(hi)), S(mn), [S(x) for x in set(vals.values()) if x != mn][:2] + [S(mn - 1)],
                       "比较极值和端点值：f(%s) ＝ %s、f(%s) ＝ %s、f(%s) ＝ %s、f(%s) ＝ %s，最小值是 <b>%s</b>。" % (S(lo), S(vals[lo]), S(p), S(vals[p]), S(q), S(vals[q]), S(hi), S(vals[hi]), S(mn)))
        if kind == "param":
            k = U.nz(-5, 5)
            t = r.randint(0, 4)
            if t == 0:
                a = -3 * k * k
                return mcq("函数 f(x) ＝ x³ ＋ ax 在 x ＝ %s 处取得极值，a ＝ ？" % S(k), S(a), [S(-a), S(-3 * k), S(-k * k)],
                           "f′(x) ＝ 3x² ＋ a，f′(%s) ＝ %d ＋ a ＝ 0，<b>a ＝ %s</b>。" % (S(k), 3 * k * k, S(a)))
            if t == 1:
                a = F(-3 * k, 2)
                return mcq("函数 f(x) ＝ x³ ＋ ax² 在 x ＝ %s 处取得极值，a ＝ ？" % S(k), S(a), [S(-a), S(-3 * k), S(F(3 * k, 2) * 2)],
                           "f′(x) ＝ 3x² ＋ 2ax，f′(%s) ＝ %d ＋ %sa ＝ 0，<b>a ＝ %s</b>。" % (S(k), 3 * k * k, S(2 * k), S(a)))
            if t == 2:
                m = abs(k)
                return mcq("函数 f(x) ＝ x³ ＋ ax² ＋ %dx 在 R 上单调递增，a 的取值范围是什么？" % (3 * m * m), "%s ≤ a ≤ %d" % (S(-3 * m), 3 * m),
                           ["%s ＜ a ＜ %d" % (S(-3 * m), 3 * m), "a ≤ %s 或 a ≥ %d" % (S(-3 * m), 3 * m), "%s ≤ a ≤ %d" % (S(-m), m)],
                           "f′(x) ＝ 3x² ＋ 2ax ＋ %d ≥ 0 恒成立，Δ ＝ 4a² － %d ≤ 0，<b>%s ≤ a ≤ %d</b>。" % (3 * m * m, 36 * m * m, S(-3 * m), 3 * m))
            m = abs(k)
            if t == 3:
                return mcq("函数 f(x) ＝ x³ － ax 在区间 [%d, ＋∞) 上单调递增，a 的取值范围是什么？" % m, "a ≤ %d" % (3 * m * m), ["a ＜ %d" % (3 * m * m), "a ≥ %d" % (3 * m * m), "a ≤ %d" % (m * m)],
                           "f′(x) ＝ 3x² － a ≥ 0 在 [%d, ＋∞) 上恒成立，a ≤ 3x² 的最小值 %d：<b>a ≤ %d</b>。" % (m, 3 * m * m, 3 * m * m))
            return mcq("函数 f(x) ＝ x² － ax 在区间 [%d, ＋∞) 上单调递增，a 的取值范围是什么？" % m, "a ≤ %d" % (2 * m), ["a ＜ %d" % (2 * m), "a ≥ %d" % (2 * m), "a ≤ %d" % m],
                       "f′(x) ＝ 2x － a ≥ 0 在 [%d, ＋∞) 上恒成立，a ≤ 2x 的最小值 %d：<b>a ≤ %d</b>。" % (m, 2 * m, 2 * m))
        t = r.randint(0, 3)
        if t == 2:
            Pm = 4 * r.randint(2, 30)
            return mcq("周长为 %d 米的矩形，面积的最大值是多少平方米？" % Pm, "%d 平方米" % (Pm * Pm // 16), ["%d 平方米" % x for x in (Pm * Pm // 8, Pm * Pm // 4, Pm * Pm // 32)],
                       "设一边长 x 米，S ＝ x(%d － x)，S′ ＝ %d － 2x ＝ 0，x ＝ %d 时 S 最大，<b>%d 平方米</b>。" % (Pm // 2, Pm // 2, Pm // 4, Pm * Pm // 16))
        if t == 3:
            x0 = r.randint(3, 30)
            c = r.randint(10, 200)
            b = 4 * x0
            mx = -2 * x0 * x0 + b * x0 - c
            if mx <= 0:
                return None
            return mcq("某产品的利润 L(x) ＝ －2x² ＋ %dx － %d（万元），x 是产量（千件）。产量是多少时利润最大？" % (b, c), "%d 千件" % x0, ["%d 千件" % x for x in (2 * x0, x0 // 2 if x0 > 2 else x0 + 2, b)],
                       "L′(x) ＝ －4x ＋ %d ＝ 0，x ＝ %d，最大利润 %d 万元。<b>%d 千件</b>" % (b, x0, mx, x0))
        Lh = r.choice([6, 12, 18, 24, 30, 36, 48, 60])
        if t == 0:
            x = F(Lh, 6)
            V = x * (Lh - 2 * x) ** 2
            return mcq("用边长为 %d 厘米的正方形铁皮，在四角各剪去一个边长为 x 厘米的小正方形，做成无盖的盒子。x 为多少时盒子的容积最大？" % Lh, "%s 厘米" % S(x),
                       ["%s 厘米" % S(y) for y in (F(Lh, 4), F(Lh, 3), F(Lh, 8))],
                       "V ＝ x(%d － 2x)²，V′ ＝ (%d － 2x)(%d － 6x) ＝ 0，x ＝ %s 时取最大值 %s 立方厘米。<b>%s 厘米</b>" % (Lh, Lh, Lh, S(x), S(V), S(x)))
        Lf = Lh * 2
        return mcq("用长为 %d 米的篱笆靠墙围成一个矩形菜园（靠墙的一边不用篱笆），菜园的最大面积是多少平方米？" % Lf, "%d 平方米" % (Lf * Lf // 8),
                   ["%d 平方米" % x for x in (Lf * Lf // 16, Lf * Lf // 4, Lf * Lf // 9)],
                   "设垂直于墙的边长 x 米，S ＝ x(%d － 2x)，S′ ＝ %d － 4x ＝ 0，x ＝ %s，最大面积 <b>%d 平方米</b>。" % (Lf, Lf, S(F(Lf, 4)), Lf * Lf // 8))
    return mk


Un("elective-2", "applications-of-derivatives", sort=3, dom="F", std=STD_D, seed=204103,
   title="导数的应用：单调性、极值、最值和优化问题", short="导数的应用",
   meta="高中数学选择性必修第二册“导数的应用”练习题：用导数求单调区间，极大值和极小值，闭区间上的最值，含参数的问题，最优化问题，100题在线练习，附可打印答案。",
   kb="f′(x) ＞ 0 的区间上 f(x) 单调递增，f′(x) ＜ 0 的区间上单调递减", ks="闭区间上的最值：比较极值和两个端点的函数值。f′(x₀) ＝ 0 是取极值的必要条件，不是充分条件。",
   body=L(["<b>单调性</b>：在某区间上 f′(x) ＞ 0，f(x) 单调递增；f′(x) ＜ 0，单调递减。",
           "<b>极值</b>：f′(x₀) ＝ 0，且左增右减是极大值，左减右增是极小值。",
           "<b>最值</b>：求出区间内的极值和端点值，最大的是最大值，最小的是最小值。实际问题先列函数，注意定义域。"],
          [("f(x) ＝ x³ － 3x 的单调递减区间", ["f′(x) ＝ 3x² － 3 ＜ 0"], "(－1, 1)"), ("同上的极大值", ["x ＝ －1 左增右减", "f(－1) ＝ 2"], "2")],
          [("把 f′(x₀) ＝ 0 的点都当成极值点", "f(x) ＝ x³ 在 x ＝ 0 处 f′ ＝ 0，但不是极值点。"),
           ("求最值时漏掉端点", "闭区间上的最值可能在端点取到。"),
           ("两个单调区间用“∪”连接", "单调区间之间用“和”或逗号隔开，不能用“∪”。")]),
   faq=[("极值和最值有什么区别？", "极值是局部的（在附近最大或最小），最值是整个区间上的最大或最小。")],
   spec=lambda: [("单调区间", [(app("mono"), 20)]), ("极值", [(app("ext"), 20)]), ("闭区间上的最值", [(app("maxmin"), 20)]),
                 ("含参数的问题", [(app("param"), 20)]), ("最优化问题", [(app("opt"), 20)])])


# ================================================================== 计数原理
def count(kind):
    def mk():
        r = U.R
        if kind == "princ":
            t = r.randint(0, 2)
            if t == 0:
                a, b, c = r.randint(2, 6), r.randint(2, 6), r.randint(1, 5)
                return mcq("从甲地到乙地，一天中有 %d 班火车、%d 班汽车、%d 班轮船。从甲地到乙地共有多少种不同的走法？" % (a, b, c), "%d 种" % (a + b + c), ["%d 种" % x for x in (a * b * c, a * b + c, a + b)],
                           "分类加法计数原理：%d ＋ %d ＋ %d ＝ <b>%d 种</b>。" % (a, b, c, a + b + c))
            if t == 1:
                a, b, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 5)
                return mcq("有 %d 件上衣、%d 条裤子、%d 双鞋，各选一件搭配，共有多少种不同的搭配？" % (a, b, c), "%d 种" % (a * b * c), ["%d 种" % x for x in (a + b + c, a * b + c, a * b)],
                           "分步乘法计数原理：%d × %d × %d ＝ <b>%d 种</b>。" % (a, b, c, a * b * c))
            n = r.randint(3, 6)
            k = r.randint(2, min(4, n))
            if r.random() < 0.5:
                return mcq("用 1 到 %d 这 %d 个数字组成 %d 位数，数字可以重复，共能组成多少个？" % (n, n, k), "%d 个" % n ** k, ["%d 个" % x for x in (A(n, k), k ** n, n * k)],
                           "每一位都有 %d 种选法：%d%s ＝ <b>%d 个</b>。" % (n, n, sup(k), n ** k))
            return mcq("用 1 到 %d 这 %d 个数字组成没有重复数字的 %d 位数，共能组成多少个？" % (n, n, k), "%d 个" % A(n, k), ["%d 个" % x for x in (n ** k, C(n, k), n * k) if x != A(n, k)],
                       "A(%d, %d) ＝ <b>%d 个</b>。" % (n, k, A(n, k)))
        if kind == "perm":
            n = r.randint(4, 9)
            k = r.randint(2, min(5, n))
            if r.random() < 0.5:
                return mcq("计算：A<sub>%d</sub><sup>%d</sup> ＝ ？" % (n, k), str(A(n, k)), [str(x) for x in (C(n, k), n ** k, A(n, k - 1))],
                           "A<sub>n</sub><sup>m</sup> ＝ n(n － 1)…(n － m ＋ 1)，<b>%d</b>。" % A(n, k))
            return mcq("从 %d 名同学中选出 %d 人，分别担任 %d 种不同的职务，共有多少种不同的选法？" % (n, k, k), "%d 种" % A(n, k), ["%d 种" % x for x in (C(n, k), n ** k, A(n, k) // 2)],
                       "职务不同，与顺序有关，是排列：A(%d, %d) ＝ <b>%d 种</b>。" % (n, k, A(n, k)))
        if kind == "comb":
            n = r.randint(4, 12)
            k = r.randint(2, min(5, n - 1))
            if r.random() < 0.5:
                return mcq("计算：C<sub>%d</sub><sup>%d</sup> ＝ ？" % (n, k), str(C(n, k)), [str(x) for x in (A(n, k), C(n, k - 1) if C(n, k - 1) != C(n, k) else C(n, k) + 1, n * k)],
                           "C<sub>n</sub><sup>m</sup> ＝ A<sub>n</sub><sup>m</sup> ÷ m!，<b>%d</b>。" % C(n, k))
            return mcq("从 %d 名同学中选出 %d 人参加比赛，共有多少种不同的选法？" % (n, k), "%d 种" % C(n, k), ["%d 种" % x for x in (A(n, k), n ** k, C(n, k) * 2)],
                       "只选人，与顺序无关，是组合：C(%d, %d) ＝ <b>%d 种</b>。" % (n, k, C(n, k)))
        if kind == "adj":
            n = r.randint(4, 9)
            t = r.randint(0, 4)
            fa = math.factorial
            if t == 0:
                v = 2 * fa(n - 1)
                return mcq("%d 个人站成一排，其中甲、乙两人必须相邻，共有多少种不同的排法？" % n, "%d 种" % v, ["%d 种" % x for x in (fa(n - 1), fa(n) - v, fa(n))],
                           "捆绑法：把甲乙看成一个整体，A(%d, %d) × 2 ＝ <b>%d 种</b>。" % (n - 1, n - 1, v))
            if t == 1:
                v = fa(n - 2) * A(n - 1, 2)
                return mcq("%d 个人站成一排，其中甲、乙两人不相邻，共有多少种不同的排法？" % n, "%d 种" % v, ["%d 种" % x for x in (2 * fa(n - 1), fa(n), fa(n - 2) * C(n - 1, 2))],
                           "插空法：先排其余 %d 人有 %d 种，再把甲乙插入 %d 个空位 A(%d, 2) ＝ %d 种，共 <b>%d 种</b>。" % (n - 2, fa(n - 2), n - 1, n - 1, A(n - 1, 2), v))
            if t == 2:
                k = r.randint(3, min(4, n - 1))
                v = fa(k) * fa(n - k + 1)
                return mcq("%d 个人站成一排，其中指定的 %d 个人必须站在一起，共有多少种不同的排法？" % (n, k), "%d 种" % v, ["%d 种" % x for x in (fa(n - k + 1), fa(k) * fa(n - k), fa(n))],
                           "捆绑法：%d 人看成一个整体，A(%d, %d) × A(%d, %d) ＝ <b>%d 种</b>。" % (k, n - k + 1, n - k + 1, k, k, v))
            if t == 3:
                v = 2 * fa(n - 1)
                return mcq("%d 个人站成一排，甲必须站在两端，共有多少种不同的排法？" % n, "%d 种" % v, ["%d 种" % x for x in (fa(n - 1), fa(n) - v, fa(n))],
                           "甲有 2 种站法，其余 %d 人全排列：2 × %d ＝ <b>%d 种</b>。" % (n - 1, fa(n - 1), v))
            v = (n - 1) * fa(n - 1)
            return mcq("%d 个人站成一排，甲不站在排头，共有多少种不同的排法？" % n, "%d 种" % v, ["%d 种" % x for x in (fa(n - 1), fa(n), (n - 2) * fa(n - 1))],
                       "间接法：A(%d, %d) － A(%d, %d) ＝ %d － %d ＝ <b>%d 种</b>。" % (n, n, n - 1, n - 1, fa(n), fa(n - 1), v))
        b, g = r.randint(3, 7), r.randint(2, 5)
        k = r.randint(2, min(4, b + g - 1))
        if r.random() < 0.5:
            v = C(b + g, k) - C(b, k)
            return mcq("从 %d 名男生和 %d 名女生中选出 %d 人，至少有 1 名女生的选法有多少种？" % (b, g, k), "%d 种" % v, ["%d 种" % x for x in (C(b + g, k), g * C(b + g - 1, k - 1), C(b, k))],
                       "间接法：C(%d, %d) － C(%d, %d) ＝ %d － %d ＝ <b>%d 种</b>。" % (b + g, k, b, k, C(b + g, k), C(b, k), v))
        k1 = r.randint(1, min(3, b))
        k2 = r.randint(1, min(3, g))
        v = C(b, k1) * C(g, k2)
        return mcq("从 %d 名男生和 %d 名女生中选出 %d 名男生和 %d 名女生，共有多少种选法？" % (b, g, k1, k2), "%d 种" % v, ["%d 种" % x for x in (C(b, k1) + C(g, k2), C(b + g, k1 + k2), A(b, k1) * A(g, k2))],
                   "分步：C(%d, %d) × C(%d, %d) ＝ <b>%d 种</b>。" % (b, k1, g, k2, v))
    return mk


Un("elective-3", "counting-principles", sort=1, dom="S", std=STD_C, seed=205101,
   title="计数原理：分类加法、分步乘法、排列与组合", short="计数原理",
   meta="高中数学选择性必修第三册“计数原理”练习题：分类加法计数原理和分步乘法计数原理，排列数，组合数，相邻和不相邻问题（捆绑法、插空法），“至少”问题，100题在线练习，附可打印答案。",
   kb="与顺序有关用排列 A(n, m)，与顺序无关用组合 C(n, m)", ks="完成一件事有几类方法用加法，分几步完成用乘法。相邻用捆绑，不相邻用插空，“至少”用间接法。",
   body=L(["<b>分类加法计数原理</b>：每一类都能独立完成，N ＝ m₁ ＋ m₂ ＋ …；<b>分步乘法计数原理</b>：每一步都完成才算完成，N ＝ m₁ × m₂ × …。",
           "<b>排列数</b> A(n, m) ＝ n!/(n － m)!；<b>组合数</b> C(n, m) ＝ n!/(m!(n － m)!)，C(n, m) ＝ C(n, n － m)。",
           "<b>相邻</b>：捆绑看成一个整体；<b>不相邻</b>：先排其他元素，再插空；<b>至少</b>：总数减去对立情况。"],
          [("5 人排成一排，甲乙相邻", ["捆绑：A(4, 4) × 2"], "48 种"), ("从 6 人中选 2 人", ["C(6, 2)"], "15 种")],
          [("选人当成排列", "只是选出几个人（不分职务）与顺序无关，用组合。"),
           ("捆绑后忘了内部排列", "甲乙捆在一起后，内部还有 2 种顺序。"),
           ("“至少一个”直接分类时重复", "用总数减去“一个也没有”更不容易出错。")]),
   faq=[("0! 等于多少？", "规定 0! ＝ 1，所以 C(n, 0) ＝ C(n, n) ＝ 1。")],
   spec=lambda: [("两个计数原理", [(count("princ"), 20)]), ("排列", [(count("perm"), 20)]), ("组合", [(count("comb"), 20)]),
                 ("相邻与不相邻", [(count("adj"), 20)]), ("组合的应用", [(count("mix"), 20)])])


# ================================================================== 二项式定理
def binom(kind):
    def mk():
        r = U.R
        n = r.randint(4, 9)
        a = r.choice([1, 2, 3, -1, -2])
        if kind == "coef":
            k = r.randint(1, n - 1)
            # (x ＋ a)ⁿ 的 xᵏ 系数 ＝ C(n, k) a^(n－k)
            v = C(n, k) * a ** (n - k)
            return mcq("(x %s %d)%s 的展开式中 x%s 的系数是多少？" % ("＋" if a > 0 else "－", abs(a), sup(n), sup(k) if k > 1 else ""), S(v),
                       [S(C(n, k)), S(C(n, k) * a ** k), S(-v), S(C(n, k + 1) * a ** (n - k))],
                       "通项 T<sub>r＋1</sub> ＝ C(%d, r)x<sup>%d－r</sup>(%s)<sup>r</sup>，令 %d － r ＝ %d，r ＝ %d，系数 C(%d, %d) × %s%s ＝ <b>%s</b>。" % (n, n, S(a), n, k, n - k, n, n - k, P(a), sup(n - k), S(v)))
        if kind == "const":
            n = r.choice([4, 6, 8, 3, 6, 9, 10, 12])
            t = r.randint(0, 2)
            if t == 2:
                if n % 3:
                    return None
                r_ = n // 3
                v = C(n, r_) * a ** r_
                return mcq("(x %s %s)%s 的展开式中的常数项是多少？" % ("＋" if a > 0 else "－", fr(abs(a), "x²"), sup(n)), S(v), [S(C(n, r_)), S(-v), S(C(n, 2 * r_) * a ** (2 * r_))],
                           "通项 C(%d, r)x<sup>%d－3r</sup>(%s)<sup>r</sup>，%d － 3r ＝ 0，r ＝ %d，常数项 <b>%s</b>。" % (n, n, S(a), n, r_, S(v)))
            if t == 0 and n % 2 == 0:
                r_ = n // 2
                v = C(n, r_) * a ** r_
                return mcq("(x %s %s)%s 的展开式中的常数项是多少？" % ("＋" if a > 0 else "－", fr(abs(a), "x"), sup(n)), S(v), [S(C(n, r_)), S(-v), S(C(n, r_ - 1) * a ** (r_ - 1))],
                           "通项 C(%d, r)x<sup>%d－2r</sup>(%s)<sup>r</sup>，%d － 2r ＝ 0，r ＝ %d，常数项 <b>%s</b>。" % (n, n, S(a), n, r_, S(v)))
            if n % 3:
                return None
            r_ = 2 * n // 3
            v = C(n, r_) * (-1) ** r_ * abs(a) ** r_
            if v == 0:
                return None
            return mcq("(x² － %s)%s 的展开式中的常数项是多少？" % (fr(abs(a), "x"), sup(n)), S(v), [S(C(n, r_)), S(-v), S(C(n, n // 3) * abs(a) ** (n // 3))],
                       "通项 C(%d, r)x<sup>2(%d－r)</sup>(－%d/x)<sup>r</sup>，指数 %d － 3r ＝ 0，r ＝ %d，常数项 <b>%s</b>。" % (n, n, abs(a), 2 * n, r_, S(v)))
        if kind == "sum":
            t = r.randint(0, 2)
            if t == 0:
                return mcq("(a ＋ b)%s 的展开式中各项的二项式系数之和是多少？" % sup(n), str(2 ** n), [str(2 ** (n - 1)), str(n + 1), str(n * n)],
                           "C(n, 0) ＋ C(n, 1) ＋ … ＋ C(n, n) ＝ 2ⁿ ＝ <b>%d</b>。" % 2 ** n)
            if t == 1:
                p, q = r.randint(1, 4), r.choice([1, -1, 2, -2, 3])
                v = (p + q) ** n
                return mcq("(%dx %s %d)%s 的展开式中各项系数之和是多少？" % (p, "＋" if q > 0 else "－", abs(q), sup(n)), S(v), [S(2 ** n), S((p - q) ** n), S(p ** n)],
                           "令 x ＝ 1：(%d %s %d)%s ＝ <b>%s</b>。" % (p, "＋" if q > 0 else "－", abs(q), sup(n), S(v)))
            return mcq("(a ＋ b)%s 的展开式中奇数项的二项式系数之和是多少？" % sup(n), str(2 ** (n - 1)), [str(2 ** n), str(2 ** (n - 2)), str((n + 1) // 2)],
                       "奇数项与偶数项的二项式系数之和相等，都是 2ⁿ⁻¹ ＝ <b>%d</b>。" % 2 ** (n - 1))
        if kind == "term":
            k = r.randint(2, n)
            r_ = k - 1
            v = C(n, r_) * a ** r_
            pw = n - r_
            term = (S(v) if v not in (1, -1) else (M if v == -1 else "")) + ("x" + (sup(pw) if pw > 1 else "") if pw else "")
            if pw == 0:
                term = S(v)
            wrong = [(S(C(n, r_ + 1) * a ** (r_ + 1)) + "x" + (sup(pw - 1) if pw - 1 > 1 else "")) if pw - 1 > 0 else S(C(n, r_ + 1) * a ** (r_ + 1)),
                     S(C(n, r_)) + ("x" + (sup(pw) if pw > 1 else "") if pw else ""), S(-v) + ("x" + (sup(pw) if pw > 1 else "") if pw else "")]
            return mcq("(x %s %d)%s 的展开式的第 %d 项是什么？" % ("＋" if a > 0 else "－", abs(a), sup(n), k), term, wrong,
                       "第 %d 项是 T<sub>%d</sub>，r ＝ %d：C(%d, %d)x<sup>%d</sup>(%s)<sup>%d</sup> ＝ <b>%s</b>。" % (k, k, r_, n, r_, pw, S(a), r_, term))
        if n % 2 == 0:
            ans = "第 %d 项" % (n // 2 + 1)
            w = ["第 %d 项" % x for x in (n // 2, n // 2 + 2, n + 1)]
            e = "n ＝ %d 是偶数，中间一项 T<sub>%d</sub> 的二项式系数最大。" % (n, n // 2 + 1)
        else:
            ans = "第 %d 项和第 %d 项" % ((n + 1) // 2, (n + 3) // 2)
            w = ["第 %d 项" % ((n + 1) // 2), "第 %d 项" % ((n + 3) // 2), "第 %d 项和第 %d 项" % ((n - 1) // 2, (n + 1) // 2)]
            e = "n ＝ %d 是奇数，中间两项的二项式系数相等且最大。" % n
        return mcq("(a ＋ b)%s 的展开式中，二项式系数最大的项是哪一项？" % sup(n), ans, w, e + "<b>%s</b>" % ans)
    return mk


Un("elective-3", "binomial-theorem", sort=2, dom="S", std=STD_C, seed=205102,
   title="二项式定理：通项、常数项和系数之和", short="二项式定理",
   meta="高中数学选择性必修第三册“二项式定理”练习题：求展开式中指定项的系数，常数项，二项式系数之和与各项系数之和，求第 k 项，二项式系数最大的项，100题在线练习，附可打印答案。",
   kb="通项 Tᵣ₊₁ ＝ C(n, r)aⁿ⁻ʳbʳ", ks="二项式系数之和为 2ⁿ；求各项系数之和令 x ＝ 1。二项式系数和项的系数不一定相同。",
   body=L(["<b>二项式定理</b>：(a ＋ b)ⁿ ＝ C(n, 0)aⁿ ＋ C(n, 1)aⁿ⁻¹b ＋ … ＋ C(n, n)bⁿ。",
           "<b>通项</b> T<sub>r＋1</sub> ＝ C(n, r)aⁿ⁻ʳbʳ 是第 r ＋ 1 项。求某一项先写通项，再令 x 的指数等于要求的数。",
           "二项式系数之和 2ⁿ，奇数项与偶数项的二项式系数之和都是 2ⁿ⁻¹；n 为偶数时中间一项的二项式系数最大。"],
          [("(x ＋ 2)⁵ 中 x³ 的系数", ["C(5, 2) × 2²"], "40"), ("(x ＋ 1/x)⁶ 的常数项", ["6 － 2r ＝ 0，r ＝ 3", "C(6, 3)"], "20")],
          [("把第 r 项写成 C(n, r)…", "通项 T<sub>r＋1</sub> 是第 r ＋ 1 项。"),
           ("把二项式系数当成项的系数", "(x ＋ 2)⁵ 中 x³ 项的二项式系数是 10，系数是 40。"),
           ("负号没有放进幂里", "(x － 2)ⁿ 的通项中是 (－2)ʳ。")]),
   faq=[("杨辉三角和二项式系数有什么关系？", "杨辉三角第 n 行的数就是 (a ＋ b)ⁿ 展开式的二项式系数。")],
   spec=lambda: [("指定项的系数", [(binom("coef"), 20)]), ("常数项", [(binom("const"), 20)]), ("系数之和", [(binom("sum"), 20)]),
                 ("求第 k 项", [(binom("term"), 20)]), ("二项式系数最大的项", [(binom("max"), -16), (binom("coef"), None)])])


# ================================================================== 随机变量及其分布
def rv(kind):
    def mk():
        r = U.R
        if kind == "dist":
            xs = sorted(r.sample(range(-1, 6), 3))
            ps = [F(r.randint(1, 5), 10), F(r.randint(1, 4), 10)]
            p3 = 1 - sum(ps)
            if p3 <= 0:
                return None
            ps.append(p3)
            i = r.randint(0, 2)
            shown = [dec(float(p), 1) for p in ps]
            shown[i] = "a"
            E = sum(x * p for x, p in zip(xs, ps))
            tbl = "X 的分布列：%s" % "，".join("P(X ＝ %s) ＝ %s" % (S(x), s_) for x, s_ in zip(xs, shown))
            return mcq("%s。求 E(X)。" % tbl, dec(float(E), 2), [dec(float(sum(xs)) / 3, 2), dec(float(E + F(1, 10)), 2), dec(float(sum(x * x * p for x, p in zip(xs, ps))), 2)],
                       "先由概率之和为 1 得 a ＝ %s，E(X) ＝ Σxᵢpᵢ ＝ <b>%s</b>。" % (dec(float(ps[i]), 1), dec(float(E), 2)))
        if kind == "binom":
            n = r.choice([5, 6, 8, 10, 12, 20, 25, 50, 100])
            p = r.choice([F(1, 2), F(1, 3), F(1, 4), F(1, 5), F(2, 5), F(3, 4), F(2, 3)])
            E, D = n * p, n * p * (1 - p)
            if r.random() < 0.5:
                return mcq("X ～ B(%d, %s)，E(X) ＝ ？" % (n, S(p)), S(E), [S(D), S(n * (1 - p)), S(E * 2)],
                           "二项分布 E(X) ＝ np ＝ %d × %s ＝ <b>%s</b>。" % (n, S(p), S(E)))
            return mcq("X ～ B(%d, %s)，D(X) ＝ ？" % (n, S(p)), S(D), [S(E), S(n * p * p), S(D * 2)],
                       "二项分布 D(X) ＝ np(1 － p) ＝ %d × %s × %s ＝ <b>%s</b>。" % (n, S(p), S(1 - p), S(D)))
        if kind == "linear":
            E, D = r.randint(-3, 8), r.randint(1, 9)
            a, b = U.nz(-4, 4), r.randint(-6, 6)
            if r.random() < 0.5:
                return mcq("已知 E(X) ＝ %s，D(X) ＝ %d，求 E(%s)。" % (S(E), D, lin(a, b, "X")), S(a * E + b), [S(a * E), S(E + b), S(a * a * E + b)],
                           "E(aX ＋ b) ＝ aE(X) ＋ b ＝ <b>%s</b>。" % S(a * E + b))
            return mcq("已知 E(X) ＝ %s，D(X) ＝ %d，求 D(%s)。" % (S(E), D, lin(a, b, "X")), S(a * a * D), [S(a * D), S(a * a * D + b), S(a * D + b)],
                       "D(aX ＋ b) ＝ a²D(X) ＝ %d × %d ＝ <b>%s</b>。" % (a * a, D, S(a * a * D)))
        if kind == "hyper":
            N = r.randint(8, 12)
            Mm = r.randint(3, N - 3)
            n = r.randint(2, 4)
            k = r.randint(max(0, n - (N - Mm)), min(n, Mm))
            v = F(C(Mm, k) * C(N - Mm, n - k), C(N, n))
            return mcq("%d 件产品中有 %d 件次品，从中任取 %d 件，恰有 %d 件次品的概率是多少？" % (N, Mm, n, k), S(v),
                       [S(F(C(n, k), 2 ** n)), S(F(C(n, k) * Mm ** k * (N - Mm) ** (n - k), N ** n)), S(F(C(Mm, k), C(N, n))) if F(C(Mm, k), C(N, n)) != v else S(1 - v)],
                       "超几何分布：C(%d, %d)C(%d, %d) ÷ C(%d, %d) ＝ <b>%s</b>。" % (Mm, k, N - Mm, n - k, N, n, S(v)))
        n = r.randint(3, 6)
        p = r.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4)])
        k = r.randint(0, n)
        v = C(n, k) * p ** k * (1 - p) ** (n - k)
        return mcq("某人每次投篮命中的概率是 %s，独立投篮 %d 次，恰好命中 %d 次的概率是多少？" % (S(p), n, k), S(v), [S(p ** k * (1 - p) ** (n - k)), S(C(n, k) * p ** k), S(F(k, n))],
                   "X ～ B(%d, %s)，P(X ＝ %d) ＝ C(%d, %d) × %s%s × %s%s ＝ <b>%s</b>。" % (n, S(p), k, n, k, P(p), sup(k), P(1 - p), sup(n - k), S(v)))
    return mk


Un("elective-3", "random-variables", sort=3, dom="S", std=STD_C, seed=205103,
   title="随机变量及其分布：均值、方差、二项分布和超几何分布", short="随机变量及其分布",
   meta="高中数学选择性必修第三册“随机变量及其分布”练习题：由分布列求均值，二项分布的均值和方差，E(aX ＋ b) 和 D(aX ＋ b)，超几何分布，二项分布的概率，100题在线练习，附可打印答案。",
   kb="X ～ B(n, p)：E(X) ＝ np，D(X) ＝ np(1 － p)", ks="E(aX ＋ b) ＝ aE(X) ＋ b，D(aX ＋ b) ＝ a²D(X)。不放回抽取用超几何分布，独立重复试验用二项分布。",
   body=L(["<b>分布列</b>：各概率非负，和为 1。<b>均值</b> E(X) ＝ Σxᵢpᵢ，<b>方差</b> D(X) ＝ Σ(xᵢ － E(X))²pᵢ。",
           "<b>二项分布</b> X ～ B(n, p)：n 次独立重复试验中成功的次数，P(X ＝ k) ＝ C(n, k)pᵏ(1 － p)ⁿ⁻ᵏ。",
           "<b>超几何分布</b>：N 件中有 M 件次品，不放回取 n 件，P(X ＝ k) ＝ C(M, k)C(N － M, n － k) ÷ C(N, n)。"],
          [("X ～ B(10, 0.3) 的均值和方差", ["np ＝ 3", "np(1 － p) ＝ 2.1"], "3，2.1"), ("D(X) ＝ 2，求 D(3X ＋ 1)", ["3² × 2"], "18")],
          [("D(aX ＋ b) 写成 aD(X) ＋ b", "常数 b 不影响方差，系数 a 要平方。"),
           ("不放回抽取用了二项分布", "不放回时每次的概率会变，用超几何分布。"),
           ("二项分布概率忘了乘 C(n, k)", "恰好 k 次成功可以出现在不同的位置。")]),
   faq=[("均值和平均数有什么关系？", "均值是随机变量取值的加权平均（权是概率），反映取值的平均水平。")],
   spec=lambda: [("分布列和均值", [(rv("dist"), 20)]), ("二项分布的均值和方差", [(rv("binom"), 20)]), ("均值和方差的性质", [(rv("linear"), 20)]),
                 ("超几何分布", [(rv("hyper"), 20)]), ("二项分布的概率", [(rv("bprob"), 20)])])


# ================================================================== 条件概率与正态分布
def cond(kind):
    def mk():
        r = U.R
        if kind == "cond":
            pa = F(r.randint(3, 8), 10)
            pab = F(r.randint(1, int(pa * 10) - 1), 10)
            v = pab / pa
            return mcq("已知 P(A) ＝ %s，P(AB) ＝ %s，求 P(B|A)。" % (dec(float(pa), 1), dec(float(pab), 1)), S(v), [S(pab * pa), S(pa / pab) if pa / pab < 10 else "1", S(pab)],
                       "P(B|A) ＝ P(AB) ÷ P(A) ＝ %s ÷ %s ＝ <b>%s</b>。" % (dec(float(pab), 1), dec(float(pa), 1), S(v)))
        if kind == "draw":
            red, white = r.randint(2, 7), r.randint(2, 7)
            n = red + white
            if r.random() < 0.5:
                v = F(red - 1, n - 1)
                return mcq("袋中有 %d 个红球、%d 个白球，不放回地依次取 2 个。已知第 1 次取到红球，第 2 次也取到红球的概率是多少？" % (red, white), S(v), [S(F(red, n)), S(F(red * (red - 1), n * (n - 1))), S(F(red - 1, n))],
                           "第 1 次取走 1 个红球后，剩下 %d 个球中有 %d 个红球：<b>%s</b>。" % (n - 1, red - 1, S(v)))
            v = F(red * (red - 1), n * (n - 1))
            return mcq("袋中有 %d 个红球、%d 个白球，不放回地依次取 2 个，两次都取到红球的概率是多少？" % (red, white), S(v), [S(F(red, n) ** 2), S(F(red - 1, n - 1)), S(F(red, n))],
                       "乘法公式：P(A₁A₂) ＝ P(A₁)P(A₂|A₁) ＝ %s × %s ＝ <b>%s</b>。" % (S(F(red, n)), S(F(red - 1, n - 1)), S(v)))
        if kind == "total":
            s1 = F(r.randint(3, 7), 10)
            d1, d2 = F(r.randint(1, 5), 100), F(r.randint(1, 5), 100)
            v = s1 * d1 + (1 - s1) * d2
            if r.random() < 0.6:
                return mcq("甲、乙两厂生产同一种零件，分别占总产量的 %d%% 和 %d%%，次品率分别是 %d%% 和 %d%%。任取一件是次品的概率是多少？" % (s1 * 100, (1 - s1) * 100, d1 * 100, d2 * 100), dec(float(v), 4),
                           [dec(float(d1 + d2) / 2, 4), dec(float(d1 * d2), 4), dec(float(s1 * d1), 4)],
                           "全概率公式：%s × %s ＋ %s × %s ＝ <b>%s</b>。" % (dec(float(s1), 1), dec(float(d1), 2), dec(float(1 - s1), 1), dec(float(d2), 2), dec(float(v), 4)))
            b = s1 * d1 / v
            return mcq("甲、乙两厂生产同一种零件，分别占总产量的 %d%% 和 %d%%，次品率分别是 %d%% 和 %d%%。任取一件是次品，它来自甲厂的概率是多少？" % (s1 * 100, (1 - s1) * 100, d1 * 100, d2 * 100), S(b),
                       [S(s1), S(F(d1, d1 + d2)), S(1 - b)],
                       "贝叶斯公式：P(甲|次) ＝ %s ÷ %s ＝ <b>%s</b>。" % (dec(float(s1 * d1), 4), dec(float(v), 4), S(b)))
        if kind == "normal":
            mu = r.randint(-2, 100)
            sg = r.randint(1, 10)
            a = r.randint(1, 3) * sg
            p = F(r.randint(1, 30), 100)
            t = r.randint(0, 1)
            if t == 0:
                return mcq("X ～ N(%d, %d²)，P(X ＞ %d) ＝ %s，求 P(%d ＜ X ＜ %d)。" % (mu, sg, mu + a, dec(float(p), 2), mu - a, mu + a), dec(float(1 - 2 * p), 2),
                           [dec(float(1 - p), 2), dec(float(F(1, 2) - p), 2), dec(float(2 * p), 2)],
                           "正态曲线关于 x ＝ %d 对称，P(X ＜ %d) ＝ P(X ＞ %d) ＝ %s，所以 1 － 2 × %s ＝ <b>%s</b>。" % (mu, mu - a, mu + a, dec(float(p), 2), dec(float(p), 2), dec(float(1 - 2 * p), 2)))
            return mcq("X ～ N(%d, %d²)，P(X ＜ %d) ＝ %s，求 P(X ＞ %d)。" % (mu, sg, mu - a, dec(float(p), 2), mu + a), dec(float(p), 2),
                       [dec(float(1 - p), 2), dec(float(F(1, 2) - p), 2), dec(float(1 - 2 * p), 2)],
                       "关于 x ＝ %d 对称，P(X ＞ %d) ＝ P(X ＜ %d) ＝ <b>%s</b>。" % (mu, mu + a, mu - a, dec(float(p), 2)))
        mu = r.choice([70, 80, 100, 170, 50, 60])
        sg = r.choice([5, 10, 2, 4])
        k = r.choice([1, 2, 3])
        pv = {1: "0.6827", 2: "0.9545", 3: "0.9973"}[k]
        return mcq("X ～ N(%d, %d²)，P(%d ≤ X ≤ %d) 约等于多少？（参考：P(μ － kσ ≤ X ≤ μ ＋ kσ) ≈ 0.6827、0.9545、0.9973，k ＝ 1、2、3）" % (mu, sg, mu - k * sg, mu + k * sg), pv,
                   [x for x in ("0.6827", "0.9545", "0.9973", "0.5") if x != pv],
                   "区间是 [μ － %dσ, μ ＋ %dσ]，概率约为 <b>%s</b>。" % (k, k, pv))
    return mk


Un("elective-3", "conditional-probability-and-normal-distribution", sort=4, dom="S", std=STD_C, seed=205104,
   title="条件概率、全概率公式和正态分布", short="条件概率与正态分布",
   meta="高中数学选择性必修第三册练习题：条件概率，不放回抽取的乘法公式，全概率公式和贝叶斯公式，正态分布的对称性，3σ 原则，100题在线练习，附可打印答案。",
   kb="P(B|A) ＝ P(AB) ÷ P(A)", ks="全概率公式 P(B) ＝ ΣP(Aᵢ)P(B|Aᵢ)；正态曲线关于 x ＝ μ 对称。",
   body=L(["<b>条件概率</b>：事件 A 发生的条件下 B 发生的概率 P(B|A) ＝ P(AB) ÷ P(A)。乘法公式 P(AB) ＝ P(A)P(B|A)。",
           "<b>全概率公式</b>：A₁、A₂、… 互斥且并为全体，P(B) ＝ ΣP(Aᵢ)P(B|Aᵢ)；<b>贝叶斯公式</b> P(Aᵢ|B) ＝ P(Aᵢ)P(B|Aᵢ) ÷ P(B)。",
           "<b>正态分布</b> N(μ, σ²)：曲线关于 x ＝ μ 对称；P(μ － σ ≤ X ≤ μ ＋ σ) ≈ 0.6827，2σ ≈ 0.9545，3σ ≈ 0.9973。"],
          [("P(A) ＝ 0.5，P(AB) ＝ 0.2，求 P(B|A)", ["0.2 ÷ 0.5"], "0.4"), ("X ～ N(2, σ²)，P(X ＞ 4) ＝ 0.1，求 P(0 ＜ X ＜ 4)", ["1 － 2 × 0.1"], "0.8")],
          [("把 P(B|A) 和 P(A|B) 弄混", "竖线后面是已经发生的条件。"),
           ("把条件概率当成 P(AB)", "P(B|A) 要除以 P(A)。"),
           ("正态分布用错对称轴", "对称轴是均值 μ，不是 0。")]),
   faq=[("σ 越大，正态曲线怎样变化？", "σ 越大，曲线越“矮胖”，数据越分散；σ 越小越“瘦高”，数据越集中。")],
   spec=lambda: [("条件概率", [(cond("cond"), 20)]), ("不放回抽取", [(cond("draw"), 20)]), ("全概率公式和贝叶斯公式", [(cond("total"), 20)]),
                 ("正态分布的对称性", [(cond("normal"), 20)]), ("3σ 原则", [(cond("sigma"), -20), (cond("normal"), None)])])


# ================================================================== 成对数据的统计分析
def dlin(b, a):
    """ŷ ＝ 1.2x － 3.5（小数）"""
    t = "%sx" % dec(float(b), 1)
    if a:
        t += (" ＋ %s" if a > 0 else " － %s") % dec(abs(float(a)), 1)
    return t


def paired(kind):
    def mk():
        r = U.R
        if kind == "corr":
            rs = sorted(r.sample([-0.95, -0.87, -0.72, -0.45, -0.18, 0.12, 0.33, 0.56, 0.78, 0.91, 0.98, -0.66, 0.05], 4), key=abs)
            if r.random() < 0.5:
                ans = dec(rs[-1], 2)
                return mcq("四组数据的样本相关系数分别是 %s，线性相关程度最强的是哪一组？" % "、".join(dec(x, 2) for x in r.sample(rs, 4)), "r ＝ %s" % ans, ["r ＝ %s" % dec(x, 2) for x in rs[:3]],
                           "|r| 越接近 1，线性相关程度越强。|%s| 最大，所以 <b>r ＝ %s</b>。" % (ans, ans))
            x = r.choice(rs)
            ans = "正相关" if x > 0 else "负相关"
            return mcq("两个变量的样本相关系数 r ＝ %s，它们是什么关系？" % dec(x, 2), ans + ("，较强" if abs(x) >= 0.75 else "，较弱"),
                       [("负相关" if x > 0 else "正相关") + ("，较强" if abs(x) >= 0.75 else "，较弱"), ans + ("，较弱" if abs(x) >= 0.75 else "，较强"), "不相关"],
                       "r %s 0 是%s；|r| %s 0.75，相关程度%s。<b>%s</b>" % ("＞" if x > 0 else "＜", ans, "≥" if abs(x) >= 0.75 else "＜", "较强" if abs(x) >= 0.75 else "较弱", ans + ("，较强" if abs(x) >= 0.75 else "，较弱")))
        if kind == "reg":
            xb = r.randint(2, 10)
            b = F(r.randint(-30, 40), 10)
            a = F(r.randint(-50, 80), 10)
            yb = b * xb + a
            if r.random() < 0.5:
                return mcq("由样本数据求得 x̄ ＝ %d，ȳ ＝ %s，经验回归方程 ŷ ＝ b̂x ＋ â 中 b̂ ＝ %s，â ＝ ？" % (xb, dec(float(yb), 1), dec(float(b), 1)), dec(float(a), 1),
                           [dec(float(yb + b * xb), 1), dec(float(yb - b), 1), dec(float(b * xb), 1)],
                           "回归直线经过 (x̄, ȳ)：â ＝ ȳ － b̂x̄ ＝ %s － %s × %d ＝ <b>%s</b>。" % (dec(float(yb), 1), ("（%s）" if b < 0 else "%s") % dec(float(b), 1), xb, dec(float(a), 1)))
            x0 = r.randint(1, 20)
            return mcq("经验回归方程是 ŷ ＝ %s，当 x ＝ %d 时，预测值 ŷ 是多少？" % (dlin(b, a), x0), dec(float(b * x0 + a), 1),
                       [dec(float(b * x0), 1), dec(float(b + a * x0), 1), dec(float(b * x0 - a), 1)],
                       "代入 x ＝ %d：ŷ ＝ <b>%s</b>。" % (x0, dec(float(b * x0 + a), 1)))
        if kind == "bhat":
            n = 5
            xs = [1, 2, 3, 4, 5]
            b = r.randint(-3, 5)
            a = r.randint(-5, 10)
            ys = [b * x + a + r.choice([-1, 0, 1]) for x in xs]
            xb, yb = F(sum(xs), n), F(sum(ys), n)
            sxy = sum(x * y for x, y in zip(xs, ys)) - n * xb * yb
            sxx = sum(x * x for x in xs) - n * xb * xb
            bh = sxy / sxx
            return mcq("x：1，2，3，4，5；y：%s。已知 Σxᵢyᵢ ＝ %s，Σxᵢ² ＝ 55，b̂ ＝ ？" % ("，".join(S(y) for y in ys), S(sum(x * y for x, y in zip(xs, ys)))), dec(float(bh), 2),
                       [dec(float(F(sum(x * y for x, y in zip(xs, ys)), 55)), 2), dec(float(bh + 1), 2), dec(float(yb / xb), 2)],
                       "x̄ ＝ 3，ȳ ＝ %s，b̂ ＝ (Σxᵢyᵢ － 5x̄ȳ) ÷ (Σxᵢ² － 5x̄²) ＝ %s ÷ 10 ＝ <b>%s</b>。" % (dec(float(yb), 2), dec(float(sxy), 2), dec(float(bh), 2)))
        if kind == "resid":
            b = F(r.randint(5, 40), 10)
            a = F(r.randint(-30, 50), 10)
            x0 = r.randint(1, 12)
            yh = b * x0 + a
            y0 = yh + F(r.randint(-20, 20), 10)
            e = y0 - yh
            return mcq("经验回归方程是 ŷ ＝ %s，样本点 (%d, %s) 的残差是多少？" % (dlin(b, a), x0, dec(float(y0), 1)), dec(float(e), 1), [dec(float(-e), 1), dec(float(yh), 1), dec(float(y0), 1)],
                       "残差 ＝ 观测值 － 预测值 ＝ %s － %s ＝ <b>%s</b>。" % (dec(float(y0), 1), dec(float(yh), 1), dec(float(e), 1)))
        crit = r.choice([(0.05, 3.841), (0.01, 6.635), (0.001, 10.828)])
        chi = round(r.uniform(0.5, 15), 3)
        if abs(chi - crit[1]) < 0.2:
            return None
        big = chi >= crit[1]
        ans = "认为两个变量不独立（有关联）" if big else "没有充分证据认为两个变量有关联"
        return mcq("根据 2 × 2 列联表计算得 χ² ≈ %s。依据小概率值 α ＝ %s 的独立性检验（x<sub>α</sub> ＝ %s），结论是什么？" % (dec(chi, 3), dec(crit[0], 3), dec(crit[1], 3)), ans,
                   ["没有充分证据认为两个变量有关联" if big else "认为两个变量不独立（有关联）", "两个变量一定有因果关系", "两个变量一定独立"],
                   "χ² ＝ %s %s %s，所以<b>%s</b>。" % (dec(chi, 3), "≥" if big else "＜", dec(crit[1], 3), ans))
    return mk


Un("elective-3", "paired-data", sort=5, dom="S", std=STD_C, seed=205105,
   title="成对数据的统计分析：相关系数、回归方程和独立性检验", short="成对数据的统计分析",
   meta="高中数学选择性必修第三册“成对数据的统计分析”练习题：样本相关系数，经验回归方程和预测，求 b̂，残差，独立性检验，100题在线练习，附可打印答案。",
   kb="经验回归直线 ŷ ＝ b̂x ＋ â 经过样本中心点 (x̄, ȳ)", ks="|r| 越接近 1 线性相关越强；独立性检验中 χ² 不小于临界值时认为两个变量有关联。",
   body=L(["<b>样本相关系数</b> r：r ＞ 0 正相关，r ＜ 0 负相关；|r| 越接近 1，线性相关程度越强。",
           "<b>经验回归方程</b> ŷ ＝ b̂x ＋ â：b̂ ＝ (Σxᵢyᵢ － nx̄ȳ) ÷ (Σxᵢ² － nx̄²)，â ＝ ȳ － b̂x̄。残差 ＝ 观测值 － 预测值。",
           "<b>独立性检验</b>：由 2 × 2 列联表算出 χ²，与临界值 x<sub>α</sub> 比较（α ＝ 0.05 时 3.841，0.01 时 6.635）。"],
          [("x̄ ＝ 4，ȳ ＝ 10，b̂ ＝ 2，求 â", ["10 － 2 × 4"], "2"), ("χ² ≈ 7.2，α ＝ 0.01", ["7.2 ≥ 6.635"], "认为有关联")],
          [("把残差算成预测值 － 观测值", "残差是观测值减预测值。"),
           ("认为 r ＝ 0 时两个变量没有任何关系", "r ＝ 0 只说明没有线性相关，可能有其他关系。"),
           ("独立性检验的结论说成“一定有关”", "结论是在犯错概率不超过 α 的前提下推断，不是绝对的。")]),
   faq=[("回归方程的预测值一定准确吗？", "不一定。预测值是估计值，实际值会在它附近波动。")],
   spec=lambda: [("样本相关系数", [(paired("corr"), 20)]), ("经验回归方程", [(paired("reg"), 20)]), ("求回归系数", [(paired("bhat"), 20)]),
                 ("残差", [(paired("resid"), 20)]), ("独立性检验", [(paired("chi"), 20)])])


if __name__ == "__main__":
    import sys
    g = sys.argv[1]
    run_grade(g, UNITS[g], lambda r: U.setup(random.Random(r.random())), sys.argv[2:] or None)
