# -*- coding: utf-8 -*-
"""
中国 高中 必修第二册（平面向量、解三角形、复数、立体几何初步、统计、概率）と
选择性必修第一册（空间向量、直线、圆、椭圆、双曲线、抛物线）。問題はすべて自前（cn_hsu の部品）。
  python3 tools/cn_hsb.py required-2|elective-1 [slug…]
"""
import math
import random
from fractions import Fraction as F
import cn_hsu as U
from cn_hsu import mcq, S, P, poly, lin, rt, pis, iv, dec, M, C
from cn_common import run_grade, lesson
from ws_common import fr

STD_G = "理解平面向量的线性运算、坐标表示和数量积，会用正弦定理、余弦定理解三角形；理解复数的代数形式和四则运算；认识基本立体图形，会求表面积和体积，理解空间点、直线、平面的位置关系"
STD_S = "会用简单随机抽样和分层抽样，会用频率分布直方图、百分位数、平均数和方差估计总体；理解古典概型、互斥事件、对立事件和相互独立事件的概率"
STD_A = "理解空间向量的坐标运算，会用空间向量求夹角和距离；掌握直线的方程和圆的方程，会判断直线与圆的位置关系；掌握椭圆、双曲线、抛物线的定义、标准方程和简单几何性质"

UNITS = {"required-2": {}, "elective-1": {}}


def Un(g, slug, **kw):
    UNITS[g][slug] = kw


def L(think, ex, mist):
    return lesson(think, ex, mist)


def vec(v):
    return "(%s)" % ", ".join(S(x) for x in v)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


# ================================================================== 平面向量
def pvec(kind):
    def mk():
        r = U.R
        a = (r.randint(-5, 5), r.randint(-5, 5))
        b = (r.randint(-5, 5), r.randint(-5, 5))
        if a == (0, 0) or b == (0, 0) or a == b:
            return None
        if kind == "coord":
            m, n = U.nz(-3, 3), U.nz(-3, 3)
            v = (m * a[0] + n * b[0], m * a[1] + n * b[1])
            ex = "%sa %s %sb" % ("" if m == 1 else (M if m == -1 else S(m)), "＋" if n > 0 else "－", "" if abs(n) == 1 else abs(n))
            return mcq("已知 a ＝ %s，b ＝ %s，求 %s。" % (vec(a), vec(b), ex), vec(v),
                       [vec((m * a[0] - n * b[0], m * a[1] - n * b[1])), vec((m * a[0] + n * b[1], m * a[1] + n * b[0])), vec((v[1], v[0])), vec((a[0] + b[0], a[1] + b[1]))],
                       "按坐标分别计算：x ＝ %s，y ＝ %s，所以是 <b>%s</b>。" % (S(v[0]), S(v[1]), vec(v)))
        if kind == "dot":
            v = dot(a, b)
            return mcq("已知 a ＝ %s，b ＝ %s，求 a · b。" % (vec(a), vec(b)), S(v), [S(x) for x in (a[0] * b[1] + a[1] * b[0], a[0] * b[0] - a[1] * b[1], -v, v + 1)],
                       "a · b ＝ x₁x₂ ＋ y₁y₂ ＝ %s × %s ＋ %s × %s ＝ <b>%s</b>。" % (S(a[0]), P(b[0]), P(a[1]), P(b[1]), S(v)))
        if kind == "mod":
            x, y, c = r.choice(U.TRIPLES)
            x, y = x * r.choice([1, -1]), y * r.choice([1, -1])
            b2 = (r.randint(-4, 4), r.randint(-4, 4))
            a2 = (x - b2[0], y - b2[1])
            return mcq("已知 a ＝ %s，b ＝ %s，求 |a ＋ b|。" % (vec(a2), vec(b2)), str(c), [str(x) for x in (abs(x) + abs(y), c * c, c + 1)] + [rt(a2[0] ** 2 + a2[1] ** 2 + b2[0] ** 2 + b2[1] ** 2)],
                       "a ＋ b ＝ %s，|a ＋ b| ＝ √(%s² ＋ %s²) ＝ <b>%d</b>。" % (vec((x, y)), P(x), P(y), c))
        if kind == "param":
            p, q = U.nz(-5, 5), U.nz(-5, 5)
            if r.random() < 0.5:
                # a ＝ (1, m)，b ＝ (p, q)，a ⊥ b：p ＋ mq ＝ 0
                m = F(-p, q)
                return mcq("已知 a ＝ (1, m)，b ＝ %s，a ⊥ b，m ＝ ？" % vec((p, q)), S(m), [S(x) for x in (F(q, p), -m, F(p, q))],
                           "a ⊥ b ⇔ a · b ＝ 0：%s ＋ %sm ＝ 0，<b>m ＝ %s</b>。" % (S(p), S(q) if q != 1 else "", S(m)))
            m = F(q, p)
            return mcq("已知 a ＝ (1, m)，b ＝ %s，a ∥ b，m ＝ ？" % vec((p, q)), S(m), [S(x) for x in (F(-p, q), -m, F(p, q))],
                       "a ∥ b ⇔ x₁y₂ － x₂y₁ ＝ 0：1 × %s － %s × m ＝ 0，<b>m ＝ %s</b>。" % (P(q), P(p), S(m)))
        # 夹角
        ang = r.choice([(1, 0, 1, 1, "45°"), (1, 0, -1, 1, "135°"), (1, 1, 1, -1, "90°"), (1, 2, -2, 1, "90°"), (3, 4, -4, 3, "90°"), (1, 0, 0, 1, "90°"),
                        (2, 0, 1, 1, "45°"), (1, 3, 2, 1, "45°"), (3, 1, 1, 2, "45°"), (1, 2, 3, -1, "45°"), (2, 1, 1, 3, "45°"), (1, -2, -1, 3, "135°"),
                        (3, 0, -1, 1, "135°"), (1, 0, 1, 0, "0°"), (2, 4, -1, -2, "180°"), (4, 2, 1, 3, "45°")])
        k1, k2 = r.randint(1, 3), r.randint(1, 3)
        a, b = (ang[0] * k1, ang[1] * k1), (ang[2] * k2, ang[3] * k2)
        v = dot(a, b)
        opts = ["0°", "45°", "90°", "135°", "180°", "60°", "120°", "30°"]
        return mcq("已知 a ＝ %s，b ＝ %s，a 与 b 的夹角是多少？" % (vec(a), vec(b)), ang[4], [x for x in opts if x != ang[4]][:3] if ang[4] != "0°" else ["45°", "90°", "180°"],
                   "cos θ ＝ a · b ÷ (|a||b|)，a · b ＝ %s，计算得夹角是 <b>%s</b>。" % (S(v), ang[4]))
    return mk


Un("required-2", "plane-vectors", sort=1, dom="G", std=STD_G, seed=202101,
   title="平面向量：坐标运算、数量积、模和夹角", short="平面向量",
   meta="高中数学必修第二册“平面向量”练习题：向量的坐标运算，数量积，向量的模，向量的垂直与平行，向量的夹角，100题在线练习，附可打印答案。",
   kb="a · b ＝ x₁x₂ ＋ y₁y₂，a ⊥ b ⇔ a · b ＝ 0", ks="a ∥ b ⇔ x₁y₂ － x₂y₁ ＝ 0；|a| ＝ √(x² ＋ y²)；cos θ ＝ a · b ÷ (|a||b|)。",
   body=L(["向量的<b>坐标运算</b>：a ± b ＝ (x₁ ± x₂, y₁ ± y₂)，λa ＝ (λx₁, λy₁)。",
           "<b>数量积</b>：a · b ＝ |a||b| cos θ ＝ x₁x₂ ＋ y₁y₂。模 |a| ＝ √(a · a)。",
           "<b>垂直</b>：a · b ＝ 0；<b>平行</b>（共线）：x₁y₂ － x₂y₁ ＝ 0。夹角 θ ∈ [0, π]。"],
          [("a ＝ (1, 2)，b ＝ (3, －1)，求 a · b", ["1 × 3 ＋ 2 × (－1)"], "1"), ("a ＝ (1, m)，b ＝ (2, 4)，a ∥ b", ["1 × 4 － 2m ＝ 0"], "m ＝ 2")],
          [("把平行的条件写成 x₁x₂ ＋ y₁y₂ ＝ 0", "那是垂直的条件；平行是 x₁y₂ － x₂y₁ ＝ 0。"),
           ("求模时忘了开方", "|a| ＝ √(x² ＋ y²)。"),
           ("认为 a · b ＜ 0 时夹角就是钝角", "还要排除两个向量反向（夹角 180°）的情况。")]),
   faq=[("向量的数量积是向量吗？", "不是。数量积 a · b 是一个实数。")],
   spec=lambda: [("坐标运算", [(pvec("coord"), 20)]), ("数量积", [(pvec("dot"), 20)]), ("向量的模", [(pvec("mod"), 20)]),
                 ("垂直与平行", [(pvec("param"), 20)]), ("向量的夹角", [(pvec("angle"), 20)])])


# ================================================================== 解三角形
SIN = {30: F(1, 2), 90: F(1)}
SINS = {30: "1/2", 45: "√2/2", 60: "√3/2", 90: "1", 120: "√3/2", 135: "√2/2", 150: "1/2"}


def tri(kind):
    def mk():
        r = U.R
        if kind == "sines":
            A_, B_ = r.sample([30, 45, 60, 90, 120, 135], 2)
            if A_ + B_ >= 180:
                return None
            a = r.choice([2, 3, 4, 6, 8, 10, 12])
            # b ＝ a sinB/sinA を厳密に（√2・√3 を含む）
            val = {30: (1, 2, 1), 45: (1, 2, 2), 60: (1, 2, 3), 90: (1, 1, 1), 120: (1, 2, 3), 135: (1, 2, 2), 150: (1, 2, 1)}

            def sv(d):
                n, dd, root = val[d]
                return n, dd, root
            nB, dB, rB = sv(B_)
            nA, dA, rA = sv(A_)
            # b ＝ a·(nB/dB)√rB ÷ ((nA/dA)√rA) ＝ a·nB·dA/(dB·nA) · √(rB/rA) ＝ k·√(rB·rA)/rA
            k = F(a * nB * dA, dB * nA) / rA
            ans = rt(rB * rA, 1)
            # k·√(rB rA)
            kk, rad = U.surd(rB * rA)
            tot = k * kk
            if tot.denominator != 1:
                return None
            ans = S(tot) if rad == 1 else ("" if tot == 1 else S(tot)) + "√%d" % rad
            wrong = []
            for x in (k * kk * 2, k * kk / 2, k * kk + 1):
                if x.denominator == 1:
                    wrong.append(S(x) if rad == 1 else ("" if x == 1 else S(x)) + "√%d" % rad)
            wrong.append(str(a * 2) if rad != 1 else rt(2, a))
            return mcq("在 △ABC 中，A ＝ %d°，B ＝ %d°，a ＝ %d，求 b。" % (A_, B_, a), ans, wrong,
                       "正弦定理：b ＝ a sin B ÷ sin A ＝ %d × %s ÷ %s ＝ <b>%s</b>。" % (a, SINS[B_], SINS[A_], ans))
        if kind == "cosines":
            Cc = r.choice([60, 120, 90])
            a, b = r.randint(2, 10), r.randint(2, 10)
            c2 = a * a + b * b - {60: a * b, 120: -a * b, 90: 0}[Cc]
            ans = rt(c2)
            return mcq("在 △ABC 中，a ＝ %d，b ＝ %d，C ＝ %d°，求 c。" % (a, b, Cc), ans, [rt(a * a + b * b + {60: a * b, 120: -a * b, 90: a * b}[Cc]), rt(a * a + b * b - 2 * a * b) if a != b else "0", str(a + b), rt(a * a + b * b)],
                       "余弦定理：c² ＝ a² ＋ b² － 2ab cos C ＝ %d ＋ %d %s ＝ %d，c ＝ <b>%s</b>。" % (a * a, b * b, {60: "－ %d" % (a * b), 120: "＋ %d" % (a * b), 90: "－ 0"}[Cc], c2, ans))
        if kind == "angle":
            while True:
                a, b = r.randint(2, 15), r.randint(2, 15)
                for Cc, c2 in ((60, a * a + b * b - a * b), (120, a * a + b * b + a * b)):
                    c = math.isqrt(c2)
                    if c * c == c2 and r.random() < 0.7:
                        return mcq("在 △ABC 中，a ＝ %d，b ＝ %d，c ＝ %d，求角 C。" % (a, b, c), "%d°" % Cc, ["%d°" % x for x in (30, 45, 60, 90, 120, 135, 150) if x != Cc][:3] if Cc == 60 else ["60°", "135°", "150°"],
                                   "cos C ＝ (a² ＋ b² － c²) ÷ 2ab ＝ (%d ＋ %d － %d) ÷ %d ＝ %s，所以 <b>C ＝ %d°</b>。" % (a * a, b * b, c * c, 2 * a * b, S(F(a * a + b * b - c * c, 2 * a * b)), Cc))
        if kind == "area":
            Cc = r.choice([30, 45, 60, 90, 120, 135, 150])
            a, b = r.randint(2, 12), r.randint(2, 12)
            n = {30: (1, 1), 45: (2, 1), 60: (3, 1), 90: (1, 2), 120: (3, 1), 135: (2, 1), 150: (1, 1)}[Cc]
            k = F(a * b, 4) * n[1]
            if n[0] == 1:
                ans = S(F(a * b, 2) * {30: F(1, 2), 150: F(1, 2), 90: 1}[Cc])
                w = [S(a * b), S(F(a * b, 4)) if Cc == 90 else S(F(a * b, 2)), S(F(a * b, 2) * (2 if Cc != 90 else F(1, 2)) + 1)]
            else:
                if k.denominator != 1:
                    ans = fr("%s√%d" % ("" if k.numerator == 1 else k.numerator, n[0]), k.denominator)
                else:
                    ans = ("" if k == 1 else S(k)) + "√%d" % n[0]
                w = [S(F(a * b, 2)), S(F(a * b, 4)), ("" if a * b == 1 else str(a * b)) + "√%d" % n[0]]
            return mcq("在 △ABC 中，a ＝ %d，b ＝ %d，C ＝ %d°，求 △ABC 的面积。" % (a, b, Cc), ans, w,
                       "S ＝ ½ab sin C ＝ ½ × %d × %d × %s ＝ <b>%s</b>。" % (a, b, SINS[Cc], ans))
        sides = sorted(r.sample(range(2, 20), 3))
        a, b, c = sides
        if a + b <= c:
            return None
        d = a * a + b * b - c * c
        ans = "锐角三角形" if d > 0 else "直角三角形" if d == 0 else "钝角三角形"
        r.shuffle(sides)
        return mcq("三边长为 %d、%d、%d 的三角形是什么三角形？" % tuple(sides), ans, [x for x in ("锐角三角形", "直角三角形", "钝角三角形", "等腰三角形") if x != ans],
                   "看最大边 %d：%d² ＋ %d² － %d² ＝ %d，%s 0，最大角是%s，所以是<b>%s</b>。" % (c, a, b, c, d, "＞" if d > 0 else ("＝" if d == 0 else "＜"), "锐角" if d > 0 else ("直角" if d == 0 else "钝角"), ans))
    return mk


Un("required-2", "solving-triangles", sort=2, dom="G", std=STD_G, seed=202102,
   title="解三角形：正弦定理、余弦定理和三角形的面积", short="解三角形",
   meta="高中数学必修第二册“解三角形”练习题：用正弦定理求边，用余弦定理求边和角，三角形的面积公式，判断三角形的形状，100题在线练习，附可打印答案。",
   kb="a/sin A ＝ b/sin B ＝ c/sin C ＝ 2R", ks="余弦定理：c² ＝ a² ＋ b² － 2ab cos C；面积 S ＝ ½ab sin C。",
   body=L(["<b>正弦定理</b>：a/sin A ＝ b/sin B ＝ c/sin C ＝ 2R。已知两角和一边，或两边和其中一边的对角时使用。",
           "<b>余弦定理</b>：c² ＝ a² ＋ b² － 2ab cos C，cos C ＝ (a² ＋ b² － c²) ÷ 2ab。已知三边或两边和夹角时使用。",
           "<b>面积</b>：S ＝ ½ab sin C。判断形状时看最大边：a² ＋ b² 与 c² 比大小。"],
          [("a ＝ 3，b ＝ 5，c ＝ 7，求 C", ["cos C ＝ (9 ＋ 25 － 49) ÷ 30 ＝ －1/2"], "120°"), ("a ＝ 4，b ＝ 6，C ＝ 30°，求面积", ["½ × 4 × 6 × ½"], "6")],
          [("用余弦定理时把 －2ab cos C 的符号弄错", "C 是钝角时 cos C ＜ 0，－2ab cos C 变成加。"),
           ("正弦定理求角时漏掉一个解", "已知 sin B 求 B 时，B 可能是锐角也可能是钝角，要用“大边对大角”检验。"),
           ("面积公式用了不夹的角", "½ab sin C 中的 C 必须是 a、b 的夹角。")]),
   faq=[("什么时候用正弦定理，什么时候用余弦定理？", "已知两角一边用正弦定理；已知三边或两边及夹角用余弦定理。")],
   spec=lambda: [("正弦定理", [(tri("sines"), 20)]), ("余弦定理求边", [(tri("cosines"), 20)]), ("余弦定理求角", [(tri("angle"), 20)]),
                 ("三角形的面积", [(tri("area"), 20)]), ("判断三角形的形状", [(tri("shape"), 20)])])


# ================================================================== 复数
def cx(a, b):
    a, b = F(a), F(b)
    if b == 0:
        return S(a)
    bi = ("" if abs(b) == 1 else S(abs(b))) + "i"
    if a == 0:
        return (M if b < 0 else "") + bi
    return "%s %s %s" % (S(a), "－" if b < 0 else "＋", bi)


def cplx(kind):
    def mk():
        r = U.R
        a, b, c, d = [U.nz(-6, 6) for _ in range(4)]
        if kind == "mul":
            re_, im = a * c - b * d, a * d + b * c
            return mcq("计算：(%s)(%s) ＝ ？" % (cx(a, b), cx(c, d)), cx(re_, im), [cx(a * c + b * d, a * d + b * c), cx(a * c, b * d), cx(re_, -im), cx(a * c - b * d, a * d - b * c)],
                       "按多项式乘法展开，i² ＝ －1：实部 %s，虚部 %s，结果 <b>%s</b>。" % (S(re_), S(im), cx(re_, im)))
        if kind == "div":
            # (a ＋ bi)(c ＋ di) ÷ (c ＋ di) の形で割り切れる問題
            re_, im = a * c - b * d, a * d + b * c
            return mcq("计算：(%s) ÷ (%s) ＝ ？" % (cx(re_, im), cx(c, d)), cx(a, b), [cx(a, -b), cx(b, a), cx(-a, b), cx(F(re_, c), F(im, d))],
                       "分子分母同乘分母的共轭复数 %s，化简得 <b>%s</b>。" % (cx(c, -d), cx(a, b)))
        if kind == "mod":
            x, y, z = r.choice(U.TRIPLES)
            x, y = x * r.choice([1, -1]), y * r.choice([1, -1])
            if r.random() < 0.5:
                return mcq("复数 z ＝ %s 的模 |z| ＝ ？" % cx(x, y), str(z), [str(abs(x) + abs(y)), str(z * z), rt(abs(x * y))],
                           "|z| ＝ √(%s² ＋ %s²) ＝ <b>%d</b>。" % (P(x), P(y), z))
            k = U.nz(-3, 3)
            return mcq("复数 z ＝ %s，|z̄| ＝ ？" % cx(x, y), str(z), [str(abs(x) + abs(y)), str(z * z), rt(z * z + 1)],
                       "共轭复数的模和原复数相同：|z̄| ＝ |z| ＝ <b>%d</b>。" % z)
        if kind == "conj":
            names = ["第一象限", "第二象限", "第三象限", "第四象限"]
            q = {(1, 1): 0, (-1, 1): 1, (-1, -1): 2, (1, -1): 3}
            if r.random() < 0.5:
                qd = q[(1 if a > 0 else -1, -1 if b > 0 else 1)]
                return mcq("复数 z ＝ %s 的共轭复数 z̄ 在复平面内对应的点在第几象限？" % cx(a, b), names[qd], [x for x in names if x != names[qd]],
                           "z̄ ＝ %s，对应点 (%s, %s)，在<b>%s</b>。" % (cx(a, -b), S(a), S(-b), names[qd]))
            re_, im = a * c - b * d, a * d + b * c
            if re_ == 0 or im == 0:
                return None
            qd = q[(1 if re_ > 0 else -1, 1 if im > 0 else -1)]
            return mcq("复数 z ＝ (%s)(%s) 在复平面内对应的点在第几象限？" % (cx(a, b), cx(c, d)), names[qd], [x for x in names if x != names[qd]],
                       "z ＝ %s，对应点 (%s, %s)，在<b>%s</b>。" % (cx(re_, im), S(re_), S(im), names[qd]))
        p, q2 = r.sample(range(-5, 6), 2)
        re_s = poly([1, -(p + q2), p * q2], "m")
        if r.random() < 0.5:
            # 虚部 m － p：m ＝ p は虚部 0 なので m ＝ q2
            im_s = lin(1, -p, "m")
            return mcq("复数 z ＝ (%s) ＋ (%s)i 是纯虚数，实数 m ＝ ？" % (re_s, im_s), S(q2), [S(p), S(p + q2), "%s 或 %s" % (S(min(p, q2)), S(max(p, q2)))],
                       "纯虚数：实部 ＝ 0 且虚部 ≠ 0。实部为 0 得 m ＝ %s 或 m ＝ %s；m ＝ %s 时虚部为 0，舍去。所以 <b>m ＝ %s</b>。" % (S(p), S(q2), S(p), S(q2)))
        k = U.nz(-6, 6, (p, q2))
        im_s = lin(1, -k, "m")
        return mcq("复数 z ＝ (%s) ＋ (%s)i 是实数，实数 m ＝ ？" % (re_s, im_s), S(k), [S(p), S(q2), S(-k)],
                   "实数：虚部 ＝ 0，m － %s ＝ 0，<b>m ＝ %s</b>。" % (P(k), S(k)))
    return mk


Un("required-2", "complex-numbers", sort=3, dom="G", std=STD_G, seed=202103,
   title="复数：四则运算、模、共轭复数和复平面", short="复数",
   meta="高中数学必修第二册“复数”练习题：复数的乘法和除法，复数的模，共轭复数，复数在复平面内对应的点，纯虚数的条件，100题在线练习，附可打印答案。",
   kb="i² ＝ －1，z ＝ a ＋ bi 的模 |z| ＝ √(a² ＋ b²)", ks="z ＝ a ＋ bi 的共轭复数 z̄ ＝ a － bi；除法要把分母实数化（分子分母同乘分母的共轭复数）。",
   body=L(["复数 z ＝ a ＋ bi（a、b ∈ R）：a 是实部，b 是虚部。b ＝ 0 时是实数；a ＝ 0 且 b ≠ 0 时是<b>纯虚数</b>。",
           "<b>运算</b>：加减实部虚部分别加减；乘法按多项式展开，把 i² 换成 －1；除法分子分母同乘分母的共轭复数。",
           "复数 a ＋ bi 对应复平面内的点 (a, b)，模 |z| ＝ √(a² ＋ b²) 是点到原点的距离。"],
          [("(1 ＋ 2i)(3 － i)", ["3 － i ＋ 6i － 2i²", "＝ 5 ＋ 5i"], "5 ＋ 5i"), ("(5 ＋ 5i) ÷ (3 － i)", ["同乘 3 ＋ i", "(10 ＋ 20i) ÷ 10"], "1 ＋ 2i")],
          [("把 i² 当成 1", "i² ＝ －1。"),
           ("纯虚数只看实部为 0", "还要虚部不为 0。"),
           ("把虚部写成 bi", "z ＝ a ＋ bi 的虚部是 b，不是 bi。")]),
   faq=[("两个复数能比较大小吗？", "两个都是实数时才能比较大小；虚数不能比较大小，但可以比较模的大小。")],
   spec=lambda: [("复数的乘法", [(cplx("mul"), 20)]), ("复数的除法", [(cplx("div"), 20)]), ("复数的模", [(cplx("mod"), 20)]),
                 ("共轭复数和复平面", [(cplx("conj"), 20)]), ("纯虚数", [(cplx("pure"), 20)])])


# ================================================================== 立体几何初步
TRUE_S = ["平行于同一条直线的两条直线互相平行", "垂直于同一个平面的两条直线互相平行", "垂直于同一条直线的两个平面互相平行",
          "如果一条直线垂直于一个平面内的两条相交直线，那么这条直线垂直于这个平面", "如果平面外一条直线与平面内的一条直线平行，那么这条直线与这个平面平行",
          "如果一个平面经过另一个平面的一条垂线，那么这两个平面互相垂直", "如果两个平行平面同时和第三个平面相交，那么它们的交线平行",
          "过不在一条直线上的三点，有且只有一个平面", "如果两个平面有一个公共点，那么它们有且只有一条过该点的公共直线"]
FALSE_S = ["垂直于同一条直线的两条直线互相平行", "平行于同一个平面的两条直线互相平行", "垂直于同一个平面的两个平面互相平行",
           "如果一条直线垂直于平面内的无数条直线，那么这条直线垂直于这个平面", "如果一条直线平行于一个平面，那么它平行于这个平面内的所有直线",
           "过三点有且只有一个平面", "平行于同一条直线的两个平面互相平行", "如果两条直线和一个平面所成的角相等，那么这两条直线平行",
           "空间中两条不相交的直线一定平行", "一个平面内的两条直线分别平行于另一个平面，那么这两个平面平行"]


def solid(kind):
    def mk():
        r = U.R
        if kind == "prism":
            t = r.randint(0, 2)
            if t == 0:
                a, b, h = r.randint(2, 9), r.randint(2, 9), r.randint(2, 12)
                return mcq("正四棱锥的底面边长是 %d，高是 %d，体积是多少？" % (a, h), S(F(a * a * h, 3)), [S(a * a * h), S(F(a * a * h, 2)), S(F(a * h, 3))],
                           "V ＝ ⅓Sh ＝ ⅓ × %d² × %d ＝ <b>%s</b>。" % (a, h, S(F(a * a * h, 3))))
            if t == 1:
                a, b, h = r.randint(2, 9), r.randint(2, 9), r.randint(2, 12)
                return mcq("长方体的长、宽、高分别是 %d、%d、%d，表面积是多少？" % (a, b, h), str(2 * (a * b + a * h + b * h)), [str(a * b * h), str(a * b + a * h + b * h), str(2 * (a * b + a * h) + b * h)],
                           "S ＝ 2(ab ＋ ah ＋ bh) ＝ <b>%d</b>。" % (2 * (a * b + a * h + b * h)))
            a, h = r.randint(2, 8), r.randint(2, 10)
            return mcq("直三棱柱的底面是直角边为 %d 和 %d 的直角三角形，高是 %d，体积是多少？" % (a, a + 1, h), S(F(a * (a + 1) * h, 2)), [S(a * (a + 1) * h), S(F(a * (a + 1) * h, 6)), S(F(a * (a + 1) * h, 3))],
                       "V ＝ Sh ＝ ½ × %d × %d × %d ＝ <b>%s</b>。" % (a, a + 1, h, S(F(a * (a + 1) * h, 2))))
        if kind == "round":
            rr_, h = r.randint(1, 8), r.randint(2, 12)
            t = r.randint(0, 2)
            if t == 0:
                return mcq("圆锥的底面半径是 %d，高是 %d，体积是多少？" % (rr_, h), pis(F(rr_ * rr_ * h, 3)), [pis(F(rr_ * rr_ * h)), pis(F(rr_ * rr_ * h, 2)), pis(F(2 * rr_ * h, 3))],
                           "V ＝ ⅓πr²h ＝ ⅓π × %d² × %d ＝ <b>%s</b>。" % (rr_, h, pis(F(rr_ * rr_ * h, 3))))
            if t == 1:
                return mcq("圆柱的底面半径是 %d，高是 %d，表面积是多少？" % (rr_, h), pis(2 * rr_ * h + 2 * rr_ * rr_), [pis(2 * rr_ * h), pis(2 * rr_ * h + rr_ * rr_), pis(rr_ * rr_ * h)],
                           "S ＝ 2πrh ＋ 2πr² ＝ <b>%s</b>。" % pis(2 * rr_ * h + 2 * rr_ * rr_))
            a, b, l = r.choice(U.TRIPLES)
            return mcq("圆锥的底面半径是 %d，母线长是 %d，侧面积是多少？" % (a, l), pis(a * l), [pis(2 * a * l), pis(a * a + a * l), pis(F(a * a * b, 3))],
                       "S侧 ＝ πrl ＝ π × %d × %d ＝ <b>%s</b>。" % (a, l, pis(a * l)))
        if kind == "sphere":
            t = r.randint(0, 2)
            R_ = r.randint(1, 9)
            if t == 0:
                return mcq("球的半径是 %d，表面积和体积分别是多少？" % R_, "%s，%s" % (pis(4 * R_ * R_), pis(F(4 * R_ ** 3, 3))),
                           ["%s，%s" % (pis(2 * R_ * R_), pis(F(4 * R_ ** 3, 3))), "%s，%s" % (pis(4 * R_ * R_), pis(4 * R_ ** 3)), "%s，%s" % (pis(R_ * R_), pis(F(R_ ** 3, 3)))],
                           "S ＝ 4πR²，V ＝ ⁴⁄₃πR³，<b>%s，%s</b>。" % (pis(4 * R_ * R_), pis(F(4 * R_ ** 3, 3))))
            if t == 1:
                a = r.randint(1, 8)
                return mcq("棱长为 %d 的正方体的顶点都在一个球面上，这个球的表面积是多少？" % a, pis(3 * a * a), [pis(4 * a * a), pis(2 * a * a), pis(a * a)],
                           "外接球的直径是正方体的体对角线 %s，R² ＝ %s，S ＝ 4πR² ＝ <b>%s</b>。" % (rt(3 * a * a), S(F(3 * a * a, 4)), pis(3 * a * a)))
            a, b, c = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
            d2 = a * a + b * b + c * c
            return mcq("长方体的长、宽、高分别是 %d、%d、%d，它的外接球的表面积是多少？" % (a, b, c), pis(d2), [pis(4 * d2), pis(2 * d2), pis(F(d2, 2))],
                       "外接球直径 2R ＝ √(%d² ＋ %d² ＋ %d²)，4R² ＝ %d，S ＝ 4πR² ＝ <b>%s</b>。" % (a, b, c, d2, pis(d2)))
        if kind == "frustum":
            r1, r2, h = r.randint(1, 4), r.randint(5, 9), r.randint(2, 9)
            if r.random() < 0.5:
                S1, S2 = r1 * r1, r2 * r2
                v = F(h, 3) * (S1 + S2 + r1 * r2)
                return mcq("圆台的上、下底面半径分别是 %d 和 %d，高是 %d，体积是多少？" % (r1, r2, h), pis(v), [pis(F(h, 3) * (S1 + S2)), pis(F(h, 2) * (S1 + S2)), pis(h * (S1 + S2 + r1 * r2))],
                           "V ＝ ⅓πh(r² ＋ rR ＋ R²) ＝ ⅓π × %d × (%d ＋ %d ＋ %d) ＝ <b>%s</b>。" % (h, S1, r1 * r2, S2, pis(v)))
            a, b = r.randint(1, 4), r.randint(5, 9)
            v = F(h, 3) * (a * a + b * b + a * b)
            return mcq("正四棱台的上、下底面边长分别是 %d 和 %d，高是 %d，体积是多少？" % (a, b, h), S(v), [S(F(h, 3) * (a * a + b * b)), S(F(h, 2) * (a * a + b * b)), S(h * (a * a + b * b + a * b))],
                       "V ＝ ⅓h(S ＋ √(SS′) ＋ S′) ＝ ⅓ × %d × (%d ＋ %d ＋ %d) ＝ <b>%s</b>。" % (h, a * a, a * b, b * b, S(v)))
        good = r.random() < 0.5
        c = r.choice(TRUE_S if good else FALSE_S)
        st = [c] + r.sample(FALSE_S if good else TRUE_S, 3)
        r.shuffle(st)
        labs = ["①", "②", "③", "④"]
        ans = labs[st.index(c)]
        q = "下列关于空间直线和平面的说法中，%s的是哪一个？<br>%s" % ("正确" if good else "错误", "<br>".join("%s %s" % (l, x) for l, x in zip(labs, st)))
        return mcq(q, ans, [l for l in labs if l != ans], "%s %s，这是%s的。%s" % (ans, c, "正确" if good else "错误", "其他说法都能在正方体中找到反例。" if good else "其他说法都是定理或公理。"))
    return mk


Un("required-2", "solid-geometry", sort=4, dom="G", std=STD_G, seed=202104,
   title="立体几何初步：表面积、体积和空间的位置关系", short="立体几何初步",
   meta="高中数学必修第二册“立体几何初步”练习题：棱柱和棱锥的体积，圆柱、圆锥的表面积和体积，球和外接球，台体的体积，空间直线和平面的位置关系，100题在线练习，附可打印答案。",
   kb="V柱 ＝ Sh，V锥 ＝ ⅓Sh，V球 ＝ ⁴⁄₃πR³，S球 ＝ 4πR²", ks="长方体（正方体）的外接球直径等于体对角线。线面垂直的判定要用平面内两条相交直线。",
   body=L(["<b>体积</b>：柱体 V ＝ Sh，锥体 V ＝ ⅓Sh，台体 V ＝ ⅓h(S ＋ √(SS′) ＋ S′)，球 V ＝ ⁴⁄₃πR³。",
           "<b>表面积</b>：圆柱 2πr² ＋ 2πrh，圆锥 πr² ＋ πrl（l 是母线），球 4πR²。",
           "<b>位置关系</b>：线面平行、面面平行、线面垂直、面面垂直都有判定定理和性质定理，判断说法对错时可以在正方体中找反例。"],
          [("棱长 2 的正方体的外接球表面积", ["2R ＝ 2√3，R ＝ √3", "4π × 3"], "12π"), ("底面半径 3、高 4 的圆锥体积", ["⅓π × 9 × 4"], "12π")],
          [("锥体体积忘了乘 ⅓", "同底等高的锥体体积是柱体的三分之一。"),
           ("圆锥侧面积用高代替母线", "侧面积 πrl 中的 l 是母线长，不是高。"),
           ("以为垂直于同一直线的两条直线平行", "在空间中，它们可能相交，也可能异面。")]),
   faq=[("什么是异面直线？", "不同在任何一个平面内的两条直线，既不平行也不相交。")],
   spec=lambda: [("棱柱和棱锥", [(solid("prism"), 20)]), ("圆柱和圆锥", [(solid("round"), 20)]), ("球和外接球", [(solid("sphere"), 20)]),
                 ("台体的体积", [(solid("frustum"), 20)]), ("空间的位置关系", [(solid("position"), 20)])])


# ================================================================== 统计
def stats(kind):
    def mk():
        r = U.R
        if kind == "strat":
            parts = [r.randint(2, 9) * 100 for _ in range(3)]
            N = sum(parts)
            n = r.choice([d for d in (20, 30, 40, 50, 60, 80, 100, 120) if all((p * d) % N == 0 for p in parts)] or [0])
            if not n:
                return None
            names = r.choice([("高一", "高二", "高三"), ("A 厂", "B 厂", "C 厂"), ("老年人", "中年人", "青年人")])
            i = r.randint(0, 2)
            ans = parts[i] * n // N
            return mcq("某校%s分别有 %d、%d、%d 人（%s），用分层抽样抽取 %d 人，应从%s中抽取多少人？" % ("、".join(names), parts[0], parts[1], parts[2], "共 %d 人" % N, n, names[i]),
                       "%d 人" % ans, ["%d 人" % x for x in (n // 3, ans + 2, parts[i] // 10, n - ans) if x != ans],
                       "按比例抽取：%d × %d ÷ %d ＝ <b>%d 人</b>。" % (n, parts[i], N, ans))
        if kind == "hist":
            d = r.choice([5, 10, 20])
            k = r.randint(4, 6)
            while True:
                cs = [r.randint(1, 8) for _ in range(k)]
                if sum(cs) == 20:
                    break
            hs = [F(c, 20 * d) for c in cs]
            i = r.randint(0, k - 1)
            show = [dec(float(h), 4) for h in hs]
            missing = show[i]
            show[i] = "a"
            return mcq("频率分布直方图中，组距是 %d，各小矩形的高从左到右依次是 %s。a ＝ ？" % (d, "，".join(show)), missing,
                       [dec(float(hs[i] * d), 4), dec(float(hs[i] * 2), 4), dec(float(hs[i] / 2), 4), dec(float(hs[i] + F(1, 100 * d)), 4)],
                       "各组频率 ＝ 高 × 组距，频率之和为 1：(%s) × %d ＝ 1，<b>a ＝ %s</b>。" % (" ＋ ".join(show), d, missing))
        if kind == "pct":
            n = r.choice([8, 10, 12, 15, 20])
            data = sorted(r.randint(10, 99) for _ in range(n))
            p = r.choice([25, 50, 75, 80, 90, 60, 40, 30, 70])
            i = F(n * p, 100)
            if i.denominator == 1:
                i = int(i)
                v = F(data[i - 1] + data[i], 2)
                e = "%d × %d%% ＝ %d 是整数，取第 %d、%d 个数的平均数" % (n, p, i, i, i + 1)
            else:
                j = math.ceil(i)
                v = F(data[j - 1])
                e = "%d × %d%% ＝ %s 不是整数，取第 %d 个数" % (n, p, dec(float(i), 2), j)
            vs = dec(float(v), 1)
            w = [dec(float(x), 1) for x in (data[min(n - 1, int(i))], data[max(0, int(i) - 2)], F(sum(data), n), v + 1)]
            return mcq("数据（已从小到大排列）：%s。这组数据的第 %d 百分位数是多少？" % ("，".join(map(str, data)), p), vs, w, "%s：<b>%s</b>。" % (e, vs))
        if kind == "var":
            m = r.randint(3, 20)
            devs = r.choice([(-2, -1, 0, 1, 2), (-3, -1, 0, 1, 3), (-4, -2, 0, 2, 4), (-1, -1, 0, 1, 1), (-3, 0, 0, 0, 3), (-2, -2, 0, 2, 2), (-5, -1, 1, 2, 3)])
            data = sorted(m + x for x in devs)
            v = F(sum(x * x for x in devs), 5)
            if r.random() < 0.5:
                return mcq("数据 %s 的方差是多少？" % "，".join(map(str, data)), dec(float(v), 2), [dec(float(F(sum(x * x for x in devs), 4)), 2), str(sum(x * x for x in devs)), dec(math.sqrt(float(v)), 2), str(m)],
                           "平均数 %d，方差 ＝ 离差平方和 ÷ 5 ＝ %d ÷ 5 ＝ <b>%s</b>。" % (m, sum(x * x for x in devs), dec(float(v), 2)))
            a, b = r.randint(2, 4), r.randint(-5, 9)
            return mcq("数据 x₁, x₂, …, xₙ 的平均数是 %d，方差是 %s。数据 %dx₁ %s %d, …, %dxₙ %s %d 的平均数和方差分别是多少？" % (m, dec(float(v), 2), a, "＋" if b >= 0 else "－", abs(b), a, "＋" if b >= 0 else "－", abs(b)),
                       "%d，%s" % (a * m + b, dec(float(v * a * a), 2)), ["%d，%s" % (a * m + b, dec(float(v * a), 2)), "%d，%s" % (a * m, dec(float(v * a * a), 2)), "%d，%s" % (a * m + b, dec(float(v * a * a + b), 2))],
                       "平均数变成 %d × %d ＋ %s ＝ %d；方差只受倍数影响，乘 %d² ＝ %d：<b>%d，%s</b>。" % (a, m, P(b), a * m + b, a, a * a, a * m + b, dec(float(v * a * a), 2)))
        d = r.choice([10, 20])
        start = r.choice([40, 50, 60])
        k = r.randint(4, 5)
        while True:
            fs = [r.randint(1, 5) for _ in range(k)]
            if sum(fs) == 10:
                break
        mids = [start + d * i + d // 2 for i in range(k)]
        mean = F(sum(m * f for m, f in zip(mids, fs)), 10)
        groups = "，".join("[%d, %d) 的频率 %s" % (start + d * i, start + d * (i + 1), dec(f / 10, 1)) for i, f in enumerate(fs))
        return mcq("样本数据分组：%s。估计这组数据的平均数。" % groups, dec(float(mean), 1), [dec(float(mean - d / 2), 1), dec(float(sum(mids) / k), 1), dec(float(mean + d / 2), 1)],
                   "用各组中点值 × 频率再求和：<b>%s</b>。" % dec(float(mean), 1))
    return mk


Un("required-2", "statistics", sort=5, dom="S", std=STD_S, seed=202105,
   title="统计：分层抽样、频率分布直方图、百分位数和方差", short="统计",
   meta="高中数学必修第二册“统计”练习题：分层抽样，频率分布直方图中求未知的高，百分位数，方差和数据变换，用频率分布直方图估计平均数，100题在线练习，附可打印答案。",
   kb="频率分布直方图中，频率 ＝ 小矩形的高 × 组距，频率之和为 1", ks="第 p 百分位数：计算 i ＝ n × p%，i 是整数取第 i、i ＋ 1 个数的平均数，不是整数取后一个数。",
   body=L(["<b>分层抽样</b>：每一层抽取的个数 ＝ 样本容量 × 该层个数 ÷ 总体个数。",
           "<b>频率分布直方图</b>：纵轴是频率/组距，小矩形的面积是频率，所有面积之和为 1。估计平均数用“组中值 × 频率”求和。",
           "<b>百分位数</b>：先排序，算 i ＝ n × p%。<b>方差</b> s² ＝ (1/n)Σ(xᵢ － x̄)²；数据都乘 a 再加 b，平均数变成 ax̄ ＋ b，方差变成 a²s²。"],
          [("10 个数据的第 75 百分位数", ["10 × 75% ＝ 7.5", "取第 8 个数"], "第 8 个数"), ("组距 10，高 0.02 的组的频率", ["0.02 × 10"], "0.2")],
          [("把直方图的高当成频率", "高是频率/组距，要乘组距才是频率。"),
           ("求百分位数前没排序", "一定要先从小到大排列。"),
           ("数据加上常数后方差也变了", "加上常数方差不变，乘 a 方差变成 a² 倍。")]),
   faq=[("中位数是第几百分位数？", "中位数就是第 50 百分位数。")],
   spec=lambda: [("分层抽样", [(stats("strat"), 20)]), ("频率分布直方图", [(stats("hist"), 20)]), ("百分位数", [(stats("pct"), 20)]),
                 ("方差", [(stats("var"), 20)]), ("用样本估计总体", [(stats("mean"), 20)])])


# ================================================================== 概率
def prob(kind):
    def mk():
        r = U.R
        if kind == "dice":
            t = r.randint(0, 3)
            if t == 0:
                s_ = r.randint(2, 12)
                n = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s_)
                return mcq("同时掷两枚质地均匀的骰子，点数之和为 %d 的概率是多少？" % s_, S(F(n, 36)), [S(F(n, 6)), S(F(1, 11)), S(F(n + 1, 36)), S(F(n, 12))],
                           "共 36 种等可能结果，和为 %d 的有 %d 种，P ＝ <b>%s</b>。" % (s_, n, S(F(n, 36))))
            if t == 1:
                s_ = r.randint(3, 12)
                m = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= s_)
                return mcq("同时掷两枚质地均匀的骰子，点数之和不小于 %d 的概率是多少？" % s_, S(F(m, 36)), [S(F(36 - m, 36)), S(F(m, 30)), S(F(m + 1, 36))],
                           "共 36 种结果，和 ≥ %d 的有 %d 种，P ＝ <b>%s</b>。" % (s_, m, S(F(m, 36))))
            if t == 2:
                pr = r.choice([x for x in range(1, 37) if any(a * b == x for a in range(1, 7) for b in range(1, 7))])
                n = sum(1 for a in range(1, 7) for b in range(1, 7) if a * b == pr)
                return mcq("同时掷两枚质地均匀的骰子，点数之积为 %d 的概率是多少？" % pr, S(F(n, 36)), [S(F(n, 6)), S(F(n + 1, 36)), S(F(n, 18)) if F(n, 18) != F(n, 36) else S(F(1, 9))],
                           "共 36 种结果，积为 %d 的有 %d 种，P ＝ <b>%s</b>。" % (pr, n, S(F(n, 36))))
            v = r.randint(1, 6)
            return mcq("同时掷两枚质地均匀的骰子，至少有一枚的点数是 %d 的概率是多少？" % v, S(F(11, 36)), [S(F(1, 3)), S(F(1, 6)), S(F(25, 36))],
                       "对立事件是“两枚都不是 %d”：1 － (5/6)² ＝ <b>11/36</b>。" % v) if r.random() < 0.3 else \
                mcq("同时掷两枚质地均匀的骰子，点数之差的绝对值为 %d 的概率是多少？" % (v - 1), S(F(sum(1 for a in range(1, 7) for b in range(1, 7) if abs(a - b) == v - 1), 36)),
                    [S(F(sum(1 for a in range(1, 7) for b in range(1, 7) if abs(a - b) == v - 1), 18)), S(F(1, 6)) if v != 1 else S(F(1, 3)), S(F(7 - v, 36)) if v != 1 else S(F(1, 12))],
                    "共 36 种结果，差的绝对值为 %d 的有 %d 种，P ＝ <b>%s</b>。" % (v - 1, sum(1 for a in range(1, 7) for b in range(1, 7) if abs(a - b) == v - 1), S(F(sum(1 for a in range(1, 7) for b in range(1, 7) if abs(a - b) == v - 1), 36))))
        if kind == "balls":
            red, white = r.randint(2, 6), r.randint(1, 6)
            n = red + white
            t = r.randint(0, 2)
            if t == 0:
                v = F(C(red, 2), C(n, 2))
                return mcq("袋中有 %d 个红球和 %d 个白球，从中任取 2 个，都是红球的概率是多少？" % (red, white), S(v), [S(F(red, n) ** 2), S(F(red, n)), S(1 - v), S(F(C(white, 2), C(n, 2))) if white >= 2 else S(F(1, n))],
                           "共 C(%d, 2) ＝ %d 种取法，都是红球有 C(%d, 2) ＝ %d 种，P ＝ <b>%s</b>。" % (n, C(n, 2), red, C(red, 2), S(v)))
            if t == 1:
                v = F(red * white, C(n, 2))
                return mcq("袋中有 %d 个红球和 %d 个白球，从中任取 2 个，恰好一红一白的概率是多少？" % (red, white), S(v), [S(F(red * white, n * n)), S(F(2 * red * white, n * n)), S(F(red * white, n * (n - 1)))],
                           "一红一白有 %d × %d ＝ %d 种，共 %d 种，P ＝ <b>%s</b>。" % (red, white, red * white, C(n, 2), S(v)))
            v = 1 - F(C(white, 2), C(n, 2)) if white >= 2 else F(1)
            if v == 1:
                return None
            return mcq("袋中有 %d 个红球和 %d 个白球，从中任取 2 个，至少有 1 个红球的概率是多少？" % (red, white), S(v), [S(F(C(white, 2), C(n, 2))), S(F(C(red, 2), C(n, 2))), S(F(red, n))],
                       "对立事件是“都是白球”：P ＝ 1 － C(%d, 2) ÷ C(%d, 2) ＝ <b>%s</b>。" % (white, n, S(v)))
        if kind == "exclusive":
            a, b = F(r.randint(1, 5), 10), F(r.randint(1, 4), 10)
            if a + b >= 1:
                return None
            if r.random() < 0.5:
                return mcq("事件 A、B 互斥，P(A) ＝ %s，P(B) ＝ %s，P(A ∪ B) ＝ ？" % (dec(float(a), 1), dec(float(b), 1)), dec(float(a + b), 1), [dec(float(a * b), 2), dec(float(a + b - a * b), 2), dec(float(1 - a - b), 1)],
                           "互斥事件不会同时发生：P(A ∪ B) ＝ P(A) ＋ P(B) ＝ <b>%s</b>。" % dec(float(a + b), 1))
            return mcq("射击时命中 10 环的概率是 %s，命中 9 环的概率是 %s。射击一次，命中环数小于 9 环的概率是多少？" % (dec(float(a), 2), dec(float(b), 2)), dec(float(1 - a - b), 2),
                       [dec(float(a + b), 2), dec(float(1 - a), 2), dec(float(1 - a * b), 2)],
                       "“小于 9 环”与“9 环或 10 环”是对立事件：1 － (%s ＋ %s) ＝ <b>%s</b>。" % (dec(float(a), 2), dec(float(b), 2), dec(float(1 - a - b), 2)))
        if kind == "indep":
            a, b = F(r.randint(5, 9), 10), F(r.randint(4, 9), 10)
            t = r.randint(0, 2)
            name, v = [("两人都击中", a * b), ("至少一人击中", 1 - (1 - a) * (1 - b)), ("恰有一人击中", a * (1 - b) + (1 - a) * b)][t]
            return mcq("甲、乙两人独立射击，击中目标的概率分别是 %s 和 %s。%s的概率是多少？" % (dec(float(a), 1), dec(float(b), 1), name), dec(float(v), 2),
                       [dec(float(x), 2) for x in (a * b, 1 - (1 - a) * (1 - b), a * (1 - b) + (1 - a) * b, a + b - 1 if a + b > 1 else (a + b) / 2) if x != v],
                       "相互独立事件同时发生的概率等于各自概率的积。%s：<b>%s</b>。" % (name, dec(float(v), 2)))
        n = r.randint(2, 5)
        k = r.randint(0, n)
        if r.random() < 0.5:
            v = F(C(n, k), 2 ** n)
            return mcq("抛掷一枚质地均匀的硬币 %d 次，恰好出现 %d 次正面的概率是多少？" % (n, k), S(v), [S(F(1, 2 ** n)), S(F(k, n)) if F(k, n) != v else S(F(1, n + 1)), S(F(C(n, k), 2 ** (n + 1)))],
                       "共 2%s ＝ %d 种等可能结果，恰好 %d 次正面有 %d 种，P ＝ <b>%s</b>。" % (U.sup(n), 2 ** n, k, C(n, k), S(v)))
        if k == 0:
            return None
        v = F(sum(C(n, j) for j in range(k, n + 1)), 2 ** n)
        return mcq("抛掷一枚质地均匀的硬币 %d 次，至少出现 %d 次正面的概率是多少？" % (n, k), S(v), [S(F(C(n, k), 2 ** n)), S(1 - v) if 1 - v != v else S(F(1, 4)), S(F(k, n)) if F(k, n) != v else S(F(1, 3))],
                   "把正面出现 %d 次到 %d 次的情况加起来：%d 种 ÷ %d ＝ <b>%s</b>。" % (k, n, sum(C(n, j) for j in range(k, n + 1)), 2 ** n, S(v)))
    return mk


Un("required-2", "probability", sort=6, dom="S", std=STD_S, seed=202106,
   title="概率：古典概型、互斥事件和相互独立事件", short="概率",
   meta="高中数学必修第二册“概率”练习题：掷骰子的古典概型，摸球问题，互斥事件和对立事件，相互独立事件，抛硬币，100题在线练习，附可打印答案。",
   kb="古典概型 P(A) ＝ A 包含的样本点个数 ÷ 样本点总数", ks="互斥事件 P(A ∪ B) ＝ P(A) ＋ P(B)；对立事件 P(Ā) ＝ 1 － P(A)；相互独立事件 P(AB) ＝ P(A)P(B)。",
   body=L(["<b>古典概型</b>：样本点有限且等可能，P(A) ＝ k ÷ n。两枚骰子共 36 个样本点。",
           "<b>互斥事件</b>不能同时发生，P(A ∪ B) ＝ P(A) ＋ P(B)；<b>对立事件</b>必有一个发生，P(A) ＋ P(Ā) ＝ 1。“至少”问题常用对立事件。",
           "<b>相互独立事件</b>：一个发生不影响另一个，P(AB) ＝ P(A)P(B)。"],
          [("两枚骰子点数和为 7 的概率", ["(1,6)…(6,1) 共 6 种", "6 ÷ 36"], "1/6"), ("甲 0.8、乙 0.7 独立，至少一人中", ["1 － 0.2 × 0.3"], "0.94")],
          [("把互斥和独立弄混", "互斥是不能同时发生；独立是互不影响，可以同时发生。"),
           ("掷两枚骰子时把 (1, 2) 和 (2, 1) 当成一种", "两枚骰子要区分，共 36 种。"),
           ("“至少一个”直接相加", "先求对立事件“一个都没有”，再用 1 减。")]),
   faq=[("频率和概率有什么关系？", "试验次数很多时，频率会稳定在概率附近，可以用频率估计概率。")],
   spec=lambda: [("掷骰子", [(prob("dice"), 20)]), ("摸球", [(prob("balls"), 20)]), ("互斥事件和对立事件", [(prob("exclusive"), 20)]),
                 ("相互独立事件", [(prob("indep"), 20)]), ("抛硬币", [(prob("coin"), -20), (prob("dice"), None)])])


# ================================================================== 空间向量
def svec(kind):
    def mk():
        r = U.R
        a = tuple(r.randint(-4, 4) for _ in range(3))
        b = tuple(r.randint(-4, 4) for _ in range(3))
        if not any(a) or not any(b) or a == b:
            return None
        if kind == "coord":
            m, n = U.nz(-3, 3), U.nz(-3, 3)
            v = tuple(m * x + n * y for x, y in zip(a, b))
            if r.random() < 0.5:
                ex = "%sa %s %sb" % ("" if m == 1 else (M if m == -1 else S(m)), "＋" if n > 0 else "－", "" if abs(n) == 1 else abs(n))
                return mcq("已知 a ＝ %s，b ＝ %s，求 %s。" % (vec(a), vec(b), ex), vec(v), [vec(tuple(m * x - n * y for x, y in zip(a, b))), vec(v[::-1]), vec(tuple(x + y for x, y in zip(a, b)))],
                           "按坐标分别计算，得 <b>%s</b>。" % vec(v))
            s2 = sum(x * x for x in a)
            return mcq("已知 a ＝ %s，|a| ＝ ？" % vec(a), rt(s2), [rt(s2 + 1), str(sum(abs(x) for x in a)), str(s2)],
                       "|a| ＝ √(%s) ＝ <b>%s</b>。" % (" ＋ ".join("%s²" % P(x) for x in a), rt(s2)))
        if kind == "perp":
            # a ＝ (1, m, k)，b ＝ (p, q, s)：p ＋ mq ＋ ks ＝ 0
            p, q, s, k = U.nz(-4, 4), U.nz(-4, 4), r.randint(-4, 4), r.randint(-3, 3)
            m = F(-(p + k * s), q)
            if m.denominator != 1:
                return None
            return mcq("已知 a ＝ (1, m, %s)，b ＝ %s，a ⊥ b，m ＝ ？" % (S(k), vec((p, q, s))), S(m), [S(-m), S(m + 1), S(F(p + k * s, 1))],
                       "a · b ＝ %s ＋ %sm ＋ %s ＝ 0，<b>m ＝ %s</b>。" % (S(p), P(q), P(k * s), S(m)))
        if kind == "angle":
            base = r.choice([((1, 0, 0), (1, 1, 0), "45°"), ((1, 0, 0), (0, 1, 0), "90°"), ((1, 1, 0), (0, 1, 1), "60°"), ((1, 0, 1), (-1, 1, 0), "120°"),
                             ((1, 1, 1), (1, -1, 0), "90°"), ((1, 0, 0), (-1, 1, 0), "135°"), ((1, 1, 0), (1, 0, 1), "60°"), ((0, 1, 1), (1, 0, -1), "120°"),
                             ((1, 2, 2), (2, 1, -2), "90°"), ((2, 1, 2), (2, 2, 1), None)])
            u, v, ang = base
            k1, k2 = r.randint(1, 3), r.randint(1, 3)
            u, v = tuple(k1 * x for x in u), tuple(k2 * x for x in v)
            perm = r.sample(range(3), 3)
            u, v = tuple(u[i] for i in perm), tuple(v[i] for i in perm)
            if ang is None:
                cv = F(dot(u, v), k1 * k2 * 9)
                return mcq("已知 a ＝ %s，b ＝ %s，cos〈a, b〉 ＝ ？" % (vec(u), vec(v)), S(cv), [S(-cv), S(F(1, 2)), S(F(dot(u, v), 9))],
                           "cos〈a, b〉 ＝ a · b ÷ (|a||b|) ＝ %d ÷ %d ＝ <b>%s</b>。" % (dot(u, v), k1 * k2 * 9, S(cv)))
            return mcq("已知 a ＝ %s，b ＝ %s，a 与 b 的夹角是多少？" % (vec(u), vec(v)), ang, [x for x in ("30°", "45°", "60°", "90°", "120°", "135°", "150°") if x != ang][:3],
                       "cos〈a, b〉 ＝ a · b ÷ (|a||b|) ＝ %s，所以夹角是 <b>%s</b>。" % (S(F(dot(u, v)) / F(math.isqrt(sum(x * x for x in u) * sum(x * x for x in v)) or 1)) if math.isqrt(sum(x * x for x in u) * sum(x * x for x in v)) ** 2 == sum(x * x for x in u) * sum(x * x for x in v) else "%d ÷ √%d" % (dot(u, v), sum(x * x for x in u) * sum(x * x for x in v)), ang))
        if kind == "normal":
            n = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
            if not any(n):
                return None
            g = math.gcd(math.gcd(abs(n[0]), abs(n[1])), abs(n[2]))
            n = tuple(x // g for x in n)
            w1 = (n[0], -n[1], n[2]) if n[1] else (n[0] + 1, n[1], n[2])
            w2 = (n[1], n[0], n[2]) if n[0] != n[1] else (n[0], n[1], -n[2]) if n[2] else (n[0], n[1] + 1, n[2])
            w3 = tuple(x + y for x, y in zip(a, b))
            return mcq("平面 α 内有两个不共线的向量 a ＝ %s，b ＝ %s，下列哪个向量是平面 α 的一个法向量？" % (vec(a), vec(b)), vec(n), [vec(w1), vec(w2), vec(w3)],
                       "法向量 n 满足 n · a ＝ 0 且 n · b ＝ 0。检验 %s：与 a、b 的数量积都是 0。所以是 <b>%s</b>。" % (vec(n), vec(n)))
        # 点到平面距离：平面过原点、法向量 n、点 P
        x, y, z = r.choice([(1, 2, 2), (2, 1, 2), (2, 2, 1), (2, 3, 6), (1, 4, 8), (4, 4, 7), (1, 0, 0), (0, 3, 4), (3, 0, 4)])
        perm = r.sample(range(3), 3)
        nn = [ (x, y, z)[i] * r.choice([1, -1]) for i in perm]
        L_ = math.isqrt(sum(t * t for t in nn))
        Pp = tuple(r.randint(-4, 4) for _ in range(3))
        d = F(abs(dot(Pp, nn)), L_)
        if d == 0:
            return None
        return mcq("平面 α 经过原点 O，法向量 n ＝ %s，点 P%s 到平面 α 的距离是多少？" % (vec(nn), vec(Pp)), S(d), [S(abs(dot(Pp, nn))), S(d * 2), S(F(abs(dot(Pp, nn)), L_ * L_))],
                   "d ＝ |OP · n| ÷ |n| ＝ %d ÷ %d ＝ <b>%s</b>。" % (abs(dot(Pp, nn)), L_, S(d)))
    return mk


Un("elective-1", "space-vectors", sort=1, dom="G", std=STD_A, seed=203101,
   title="空间向量与立体几何：坐标运算、夹角、法向量和距离", short="空间向量与立体几何",
   meta="高中数学选择性必修第一册“空间向量与立体几何”练习题：空间向量的坐标运算和模，空间向量的垂直，夹角，平面的法向量，点到平面的距离，100题在线练习，附可打印答案。",
   kb="a · b ＝ x₁x₂ ＋ y₁y₂ ＋ z₁z₂，a ⊥ b ⇔ a · b ＝ 0", ks="平面的法向量与平面内两个不共线向量都垂直；点 P 到平面的距离 d ＝ |AP · n| ÷ |n|。",
   body=L(["空间向量的坐标运算和平面向量一样，只是多了 z 坐标。|a| ＝ √(x² ＋ y² ＋ z²)。",
           "<b>法向量</b>：设 n ＝ (x, y, z)，由 n · a ＝ 0、n · b ＝ 0 列方程组求出一个非零解。",
           "<b>夹角与距离</b>：两条直线的夹角用方向向量求；点到平面的距离 d ＝ |AP · n| ÷ |n|（A 是平面内一点）。"],
          [("a ＝ (1, 2, 2)，|a|", ["√(1 ＋ 4 ＋ 4)"], "3"), ("n ＝ (1, 2, 2)，P(3, 0, 0)，过原点的平面到 P 的距离", ["|3| ÷ 3"], "1")],
          [("法向量算成 a ＋ b", "法向量要和 a、b 都垂直，用数量积为 0 检验。"),
           ("距离公式忘了除以 |n|", "d ＝ |AP · n| ÷ |n|。"),
           ("线面角直接取向量夹角", "直线与平面所成角的正弦等于方向向量与法向量夹角余弦的绝对值。")]),
   faq=[("法向量是唯一的吗？", "不是。一个平面的法向量有无数个，它们互相平行，取一个方便计算的即可。")],
   spec=lambda: [("坐标运算和模", [(svec("coord"), 20)]), ("向量的垂直", [(svec("perp"), 20)]), ("向量的夹角", [(svec("angle"), 20)]),
                 ("平面的法向量", [(svec("normal"), 20)]), ("点到平面的距离", [(svec("dist"), 20)])])


# ================================================================== 直线
ANG = {F(0): "0°", F(1): "45°", F(-1): "135°"}


def gen_line(a, b, c):
    s = poly([a, 0], "x")[:-0 or None]
    parts = []
    for coef, v in ((a, "x"), (b, "y")):
        if coef:
            parts.append((coef, v))
    out = ""
    for i, (coef, v) in enumerate(parts):
        t = ("" if abs(coef) == 1 else str(abs(coef))) + v
        out += ((M if coef < 0 else "") + t) if i == 0 else ((" － " if coef < 0 else " ＋ ") + t)
    if c:
        out += (" － " if c < 0 else " ＋ ") + str(abs(c))
    return out + " ＝ 0"


def lines(kind):
    def mk():
        r = U.R
        if kind == "slope":
            x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
            t = r.choice([F(1), F(-1), F(0), "sqrt3", "-sqrt3", F(2), F(-1, 2), F(3)])
            dx = r.randint(1, 5) * r.choice([1, -1])
            if isinstance(t, F):
                x2, y2 = x1 + dx, y1 + t * dx
                if y2.denominator != 1:
                    return None
                ang = ANG.get(t)
                if ang:
                    return mcq("经过 A(%s, %s)、B(%s, %s) 两点的直线的倾斜角是多少？" % (S(x1), S(y1), S(x2), S(y2)), ang, [x for x in ("0°", "45°", "90°", "135°", "60°") if x != ang][:3],
                               "斜率 k ＝ (%s － %s) ÷ (%s － %s) ＝ %s，倾斜角 <b>%s</b>。" % (S(y2), P(y1), S(x2), P(x1), S(t), ang))
                return mcq("经过 A(%s, %s)、B(%s, %s) 两点的直线的斜率是多少？" % (S(x1), S(y1), S(x2), S(y2)), S(t), [S(-t), S(1 / t) if t else "1", S(F(dx, y2 - y1)) if y2 != y1 else "0"],
                           "k ＝ (y₂ － y₁) ÷ (x₂ － x₁) ＝ <b>%s</b>。" % S(t))
            ang = "60°" if t == "sqrt3" else "120°"
            k = "√3" if t == "sqrt3" else "－√3"
            return mcq("直线的斜率是 %s，它的倾斜角是多少？" % k, ang, [x for x in ("30°", "60°", "120°", "150°") if x != ang],
                       "tan α ＝ %s，α ∈ [0°, 180°)，所以 <b>α ＝ %s</b>。" % (k, ang))
        if kind == "eq":
            x0, y0 = r.randint(-5, 5), r.randint(-5, 5)
            k = F(U.nz(-4, 4), r.choice([1, 1, 2, 3]))
            # y － y0 ＝ k(x － x0) → 一般式
            a, b, c = k.numerator, -k.denominator, -(k.numerator * x0) + k.denominator * y0
            if a < 0:
                a, b, c = -a, -b, -c
            return mcq("经过点 (%s, %s)、斜率为 %s 的直线方程（一般式）是什么？" % (S(x0), S(y0), S(k)), gen_line(a, b, c),
                       [gen_line(a, b, -c), gen_line(b, a, c) if a != b else gen_line(a, -b, c), gen_line(a, -b, c)],
                       "点斜式 y － %s ＝ %s(x － %s)，整理得 <b>%s</b>。" % (P(y0), S(k), P(x0), gen_line(a, b, c)))
        if kind == "pp":
            a1, b1 = U.nz(-5, 5), U.nz(-5, 5)
            if r.random() < 0.5:
                # l1: a1 x ＋ b1 y ＋ 1 ＝ 0，l2: m x ＋ 2y － 3 ＝ 0，垂直：a1 m ＋ 2b1 ＝ 0
                m = F(-2 * b1, a1)
                if m.denominator != 1:
                    return None
                return mcq("直线 l₁：%s 与 l₂：mx ＋ 2y － 3 ＝ 0 垂直，m ＝ ？" % gen_line(a1, b1, 1), S(m), [S(-m), S(F(2 * a1, b1)) if F(2 * a1, b1) != m else "0", S(F(a1, b1))],
                           "A₁A₂ ＋ B₁B₂ ＝ 0：%sm ＋ %s × 2 ＝ 0，<b>m ＝ %s</b>。" % (S(a1), P(b1), S(m)))
            m = F(2 * a1, b1)
            if m.denominator != 1:
                return None
            return mcq("直线 l₁：%s 与 l₂：mx ＋ 2y － 3 ＝ 0 平行，m ＝ ？" % gen_line(a1, b1, 1), S(m), [S(-m), S(F(-2 * b1, a1)) if F(-2 * b1, a1) != m else "1", S(F(a1, b1))],
                       "A₁B₂ － A₂B₁ ＝ 0：%s × 2 － %sm ＝ 0，<b>m ＝ %s</b>，且两直线不重合。" % (S(a1), P(b1), S(m)))
        if kind == "dist":
            a, b, c_ = r.choice(U.TRIPLES[:5])
            a, b = a * r.choice([1, -1]), b * r.choice([1, -1])
            x0, y0 = r.randint(-5, 5), r.randint(-5, 5)
            c = r.randint(-15, 15)
            num = abs(a * x0 + b * y0 + c)
            if num == 0:
                return None
            d = F(num, c_)
            return mcq("点 P(%s, %s) 到直线 %s 的距离是多少？" % (S(x0), S(y0), gen_line(a, b, c)), S(d), [S(num), S(F(num, c_ * c_)), S(d + 1)],
                       "d ＝ |Ax₀ ＋ By₀ ＋ C| ÷ √(A² ＋ B²) ＝ %d ÷ %d ＝ <b>%s</b>。" % (num, c_, S(d)))
        a, b, c_ = r.choice(U.TRIPLES[:5])
        b = b * r.choice([1, -1])
        c1, c2 = r.sample(range(-20, 21), 2)
        d = F(abs(c1 - c2), c_)
        k = r.choice([1, 2])
        return mcq("两条平行直线 %s 与 %s 之间的距离是多少？" % (gen_line(a, b, c1), gen_line(a * k, b * k, c2 * k)), S(d), [S(abs(c1 - c2)), S(F(abs(c1 + c2), c_)) if c1 + c2 else "1", S(F(abs(c1 - k * c2), c_)) if k == 2 else S(d * 2)],
                   "先把系数化成相同：%s，d ＝ |C₁ － C₂| ÷ √(A² ＋ B²) ＝ %d ÷ %d ＝ <b>%s</b>。" % (gen_line(a, b, c2), abs(c1 - c2), c_, S(d)))
    return mk


Un("elective-1", "lines", sort=2, dom="G", std=STD_A, seed=203102,
   title="直线和方程：斜率、倾斜角、平行和垂直、距离", short="直线的方程",
   meta="高中数学选择性必修第一册“直线的方程”练习题：斜率和倾斜角，求直线方程，两条直线的平行和垂直，点到直线的距离，两条平行直线间的距离，100题在线练习，附可打印答案。",
   kb="点 (x₀, y₀) 到直线 Ax ＋ By ＋ C ＝ 0 的距离 d ＝ |Ax₀ ＋ By₀ ＋ C| ÷ √(A² ＋ B²)", ks="l₁ ⊥ l₂ ⇔ A₁A₂ ＋ B₁B₂ ＝ 0；l₁ ∥ l₂ ⇔ A₁B₂ － A₂B₁ ＝ 0（且不重合）。",
   body=L(["<b>斜率</b> k ＝ tan α ＝ (y₂ － y₁) ÷ (x₂ － x₁)，倾斜角 α ∈ [0°, 180°)。α ＝ 90° 时斜率不存在。",
           "<b>直线方程</b>：点斜式 y － y₀ ＝ k(x － x₀)，斜截式 y ＝ kx ＋ b，一般式 Ax ＋ By ＋ C ＝ 0。",
           "<b>距离</b>：点到直线 d ＝ |Ax₀ ＋ By₀ ＋ C| ÷ √(A² ＋ B²)；两条平行线 d ＝ |C₁ － C₂| ÷ √(A² ＋ B²)（系数要先化成相同）。"],
          [("点 (1, 2) 到 3x ＋ 4y － 1 ＝ 0 的距离", ["|3 ＋ 8 － 1| ÷ 5"], "2"), ("过 (1, 1)、斜率 2 的直线", ["y － 1 ＝ 2(x － 1)"], "2x － y － 1 ＝ 0")],
          [("平行线距离公式中两个方程的系数不同", "先把 x、y 的系数化成相同，再用公式。"),
           ("只用斜率判断平行，漏掉斜率不存在的情况", "用一般式的条件 A₁B₂ － A₂B₁ ＝ 0 更全面。"),
           ("倾斜角写成负角", "倾斜角的范围是 [0°, 180°)。")]),
   faq=[("斜率为 －1 的直线倾斜角是多少？", "tan α ＝ －1，α ＝ 135°。")],
   spec=lambda: [("斜率和倾斜角", [(lines("slope"), 20)]), ("求直线方程", [(lines("eq"), 20)]), ("平行和垂直", [(lines("pp"), 20)]),
                 ("点到直线的距离", [(lines("dist"), 20)]), ("两条平行直线间的距离", [(lines("pdist"), 20)])])


# ================================================================== 圆
def sq_txt(a, v):
    return "%s²" % v if a == 0 else "(%s %s %d)²" % (v, "－" if a > 0 else "＋", abs(a))


def circles(kind):
    def mk():
        r = U.R
        a, b = r.randint(-6, 6), r.randint(-6, 6)
        rad = r.randint(1, 8)
        if kind == "std":
            eq = "%s ＋ %s ＝ %d" % (sq_txt(a, "x"), sq_txt(b, "y"), rad * rad)
            return mcq("圆 %s 的圆心和半径分别是什么？" % eq, "(%s, %s)，%d" % (S(a), S(b), rad),
                       ["(%s, %s)，%d" % (S(-a), S(-b), rad), "(%s, %s)，%d" % (S(a), S(b), rad * rad), "(%s, %s)，%d" % (S(b), S(a), rad) if a != b else "(%s, %s)，%d" % (S(-a), S(b), rad * rad)],
                       "标准方程 (x － a)² ＋ (y － b)² ＝ r²，圆心 (a, b)，半径 r：<b>(%s, %s)，%d</b>。" % (S(a), S(b), rad))
        if kind == "gen":
            D, E, Fc = -2 * a, -2 * b, a * a + b * b - rad * rad
            eq = "x² ＋ y²" + ("" if not D else (" ＋ %dx" % D if D > 0 else " － %dx" % -D)) + ("" if not E else (" ＋ %dy" % E if E > 0 else " － %dy" % -E)) + ("" if not Fc else (" ＋ %d" % Fc if Fc > 0 else " － %d" % -Fc)) + " ＝ 0"
            return mcq("圆 %s 的圆心和半径分别是什么？" % eq, "(%s, %s)，%d" % (S(a), S(b), rad),
                       ["(%s, %s)，%d" % (S(-a), S(-b), rad), "(%s, %s)，%d" % (S(D), S(E), rad), "(%s, %s)，%s" % (S(a), S(b), rt(abs(Fc)) if Fc else "1")],
                       "配方：%s ＋ %s ＝ %d，圆心 (－D/2, －E/2)，<b>(%s, %s)，%d</b>。" % (sq_txt(a, "x"), sq_txt(b, "y"), rad * rad, S(a), S(b), rad))
        if kind == "pos":
            A_, B_, c_ = r.choice(U.TRIPLES[:5])
            B_ = B_ * r.choice([1, -1])
            dnum = c_ * r.choice([rad - 1, rad, rad + 1, rad + 2]) if rad > 1 else c_ * r.choice([rad, rad + 1])
            C_ = dnum - A_ * a - B_ * b
            d = F(abs(A_ * a + B_ * b + C_), c_)
            ans = "相交" if d < rad else "相切" if d == rad else "相离"
            return mcq("直线 %s 与圆 %s ＋ %s ＝ %d 的位置关系是什么？" % (gen_line(A_, B_, C_), sq_txt(a, "x"), sq_txt(b, "y"), rad * rad), ans, [x for x in ("相交", "相切", "相离", "无法确定") if x != ans],
                       "圆心 (%s, %s) 到直线的距离 d ＝ %s，r ＝ %d，d %s r，所以<b>%s</b>。" % (S(a), S(b), S(d), rad, "＜" if d < rad else ("＝" if d == rad else "＞"), ans))
        if kind == "chord":
            h, k2, R_ = r.choice(U.TRIPLES[:5])
            A_, B_, c_ = r.choice(U.TRIPLES[:5])
            # 距離 d ＝ h（または k2）、半径 R_、弦長 2·另一边
            d, half = (h, k2) if r.random() < 0.5 else (k2, h)
            if d % c_ and (d * c_) % c_:
                pass
            C_ = d * c_ - A_ * a - B_ * b
            return mcq("圆 %s ＋ %s ＝ %d 被直线 %s 截得的弦长是多少？" % (sq_txt(a, "x"), sq_txt(b, "y"), R_ * R_, gen_line(A_, B_, C_)), str(2 * half), [str(half), str(2 * d), rt(R_ * R_ + d * d, 2)],
                       "圆心到直线的距离 d ＝ %d，弦长 ＝ 2√(r² － d²) ＝ 2√(%d － %d) ＝ <b>%d</b>。" % (d, R_ * R_, d * d, 2 * half))
        r1, r2 = r.randint(1, 6), r.randint(1, 6)
        x, y, dd = r.choice(U.TRIPLES[:5])
        if dd > r1 + r2 + 3:
            return None
        ans = "外离" if dd > r1 + r2 else "外切" if dd == r1 + r2 else "相交" if dd > abs(r1 - r2) else "内切" if dd == abs(r1 - r2) else "内含"
        return mcq("圆 x² ＋ y² ＝ %d 与圆 %s ＋ %s ＝ %d 的位置关系是什么？" % (r1 * r1, sq_txt(x, "x"), sq_txt(y, "y"), r2 * r2), ans, [z for z in ("外离", "外切", "相交", "内切", "内含") if z != ans][:3],
                   "圆心距 d ＝ %d，r₁ ＋ r₂ ＝ %d，|r₁ － r₂| ＝ %d，所以<b>%s</b>。" % (dd, r1 + r2, abs(r1 - r2), ans))
    return mk


Un("elective-1", "equations-of-circles", sort=3, dom="G", std=STD_A, seed=203103,
   title="圆的方程：标准方程、一般方程和位置关系", short="圆的方程",
   meta="高中数学选择性必修第一册“圆的方程”练习题：圆的标准方程和一般方程，直线与圆的位置关系，弦长，圆与圆的位置关系，100题在线练习，附可打印答案。",
   kb="(x － a)² ＋ (y － b)² ＝ r² 的圆心是 (a, b)，半径是 r", ks="直线与圆：比较圆心到直线的距离 d 和半径 r；弦长 ＝ 2√(r² － d²)。",
   body=L(["<b>标准方程</b> (x － a)² ＋ (y － b)² ＝ r²；<b>一般方程</b> x² ＋ y² ＋ Dx ＋ Ey ＋ F ＝ 0，用配方化成标准方程，圆心 (－D/2, －E/2)。",
           "<b>直线与圆</b>：d ＜ r 相交，d ＝ r 相切，d ＞ r 相离。弦长 ＝ 2√(r² － d²)。",
           "<b>圆与圆</b>：比较圆心距 d 与 r₁ ＋ r₂、|r₁ － r₂|：外离、外切、相交、内切、内含。"],
          [("x² ＋ y² － 4x ＋ 6y － 3 ＝ 0", ["(x － 2)² ＋ (y ＋ 3)² ＝ 16"], "圆心 (2, －3)，半径 4"), ("r ＝ 5，d ＝ 3 时弦长", ["2√(25 － 9)"], "8")],
          [("圆心坐标的符号弄反", "(x － 2)² 对应的圆心横坐标是 2，(x ＋ 2)² 对应 －2。"),
           ("把 r² 当成 r", "等号右边是半径的平方。"),
           ("弦长忘了乘 2", "2√(r² － d²) 是整条弦，√(r² － d²) 只是半条。")]),
   faq=[("x² ＋ y² ＋ Dx ＋ Ey ＋ F ＝ 0 一定表示圆吗？", "不一定。D² ＋ E² － 4F ＞ 0 时才表示圆。")],
   spec=lambda: [("圆的标准方程", [(circles("std"), 20)]), ("圆的一般方程", [(circles("gen"), 20)]), ("直线与圆的位置关系", [(circles("pos"), 20)]),
                 ("弦长", [(circles("chord"), 20)]), ("圆与圆的位置关系", [(circles("two"), 20)])])


# ================================================================== 圆锥曲线
def fq(n, d):
    """分母が 1 なら分数にしない"""
    return str(n) if d == 1 else fr(n, d)


def frs(a, b):
    """x²/a ＋ … の分数"""
    return fr("x²", a), fr("y²", b)


ELL = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12), (10, 8, 6), (10, 6, 8), (17, 15, 8), (17, 8, 15), (25, 24, 7), (25, 7, 24), (3, 2, None), (2, 1, None), (4, 2, None), (3, 1, None), (6, 4, None)]


def ellipse(kind):
    def mk():
        r = U.R
        a, b, c = r.choice(ELL)
        if c and r.random() < 0.4:
            a, b, c = 2 * a, 2 * b, 2 * c
        c2 = a * a - b * b
        cs = str(c) if c else rt(c2)
        onx = r.random() < 0.6
        X, Y = (a * a, b * b) if onx else (b * b, a * a)
        eq = "%s ＋ %s ＝ 1" % (fq("x²", X), fq("y²", Y))
        if kind == "elem":
            return mcq("椭圆 %s 的焦点坐标是什么？" % eq, ("(±%s, 0)" if onx else "(0, ±%s)") % cs,
                       [("(0, ±%s)" if onx else "(±%s, 0)") % cs, ("(±%d, 0)" if onx else "(0, ±%d)") % a, ("(±%s, 0)" if onx else "(0, ±%s)") % rt(a * a + b * b)],
                       "a² ＝ %d，b² ＝ %d，c² ＝ a² － b² ＝ %d，焦点在 %s 轴上：<b>%s</b>。" % (a * a, b * b, c2, "x" if onx else "y", ("(±%s, 0)" if onx else "(0, ±%s)") % cs))
        if kind == "ecc":
            e = (S(F(c, a)) if c else fq(cs, a))
            return mcq("椭圆 %s 的离心率是多少？" % eq, e, [S(F(b, a)), (S(F(a, c)) if c else fq(a, cs)), (S(F(c, b)) if c else fq(cs, b)), S(F(c2, a * a))],
                       "e ＝ c/a ＝ %s ÷ %d ＝ <b>%s</b>。" % (cs, a, e))
        if kind == "eq":
            if not c:
                return None
            return mcq("椭圆的焦点在 %s 轴上，长轴长为 %d，焦距为 %d，它的标准方程是什么？" % ("x" if onx else "y", 2 * a, 2 * c), eq,
                       ["%s ＋ %s ＝ 1" % (fq("x²", Y), fq("y²", X)), "%s ＋ %s ＝ 1" % (fq("x²", a * a if onx else c * c), fq("y²", c * c if onx else a * a)), "%s ＋ %s ＝ 1" % (fq("x²", 4 * X), fq("y²", 4 * Y))],
                       "2a ＝ %d，2c ＝ %d，a ＝ %d，c ＝ %d，b² ＝ a² － c² ＝ %d：<b>%s</b>。" % (2 * a, 2 * c, a, c, b * b, eq))
        if kind == "tri":
            if not c:
                return None
            return mcq("椭圆 %s 的两个焦点为 F₁、F₂，P 是椭圆上一点，△PF₁F₂ 的周长是多少？" % eq, str(2 * a + 2 * c), [str(2 * a), str(4 * a), str(2 * a + 2 * b)],
                       "|PF₁| ＋ |PF₂| ＝ 2a ＝ %d，|F₁F₂| ＝ 2c ＝ %d，周长 <b>%d</b>。" % (2 * a, 2 * c, 2 * a + 2 * c))
        p, q = sorted(r.sample(range(-4, 12), 2))
        mid = F(p + q, 2)
        # x²/(m － p) ＋ y²/(q － m) ＝ 1 表示焦点在 x 轴上的椭圆：m － p ＞ q － m ＞ 0
        if mid.denominator != 1:
            return None
        return mcq("方程 %s ＋ %s ＝ 1 表示焦点在 x 轴上的椭圆，m 的取值范围是什么？" % (fq("x²", lin(1, -p, "m")), fq("y²", "%s － m" % S(q))),
                   "%s ＜ m ＜ %s" % (S(mid), S(q)), ["%s ＜ m ＜ %s" % (S(p), S(q)), "%s ＜ m ＜ %s" % (S(p), S(mid)), "m ＞ %s" % S(mid)],
                   "要 m － %s ＞ %s － m ＞ 0，得 <b>%s ＜ m ＜ %s</b>。" % (P(p), S(q), S(mid), S(q)))
    return mk


def hyper(kind):
    def mk():
        r = U.R
        a, b, c = r.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17), (15, 8, 17), (1, 1, None), (2, 2, None), (1, 2, None), (2, 1, None), (1, 3, None), (3, 1, None)])
        if c and r.random() < 0.4:
            a, b, c = 2 * a, 2 * b, 2 * c
        c2 = a * a + b * b
        cs = str(c) if c else rt(c2)
        onx = r.random() < 0.6
        eq = ("%s － %s ＝ 1" % (fq("x²", a * a), fq("y²", b * b))) if onx else ("%s － %s ＝ 1" % (fq("y²", a * a), fq("x²", b * b)))
        if kind == "elem":
            return mcq("双曲线 %s 的焦点坐标是什么？" % eq, ("(±%s, 0)" if onx else "(0, ±%s)") % cs,
                       [("(0, ±%s)" if onx else "(±%s, 0)") % cs, ("(±%d, 0)" if onx else "(0, ±%d)") % a, ("(±%s, 0)" if onx else "(0, ±%s)") % rt(abs(a * a - b * b)) if a != b else "(±1, 0)"],
                       "c² ＝ a² ＋ b² ＝ %d，焦点在 %s 轴上：<b>%s</b>。" % (c2, "x" if onx else "y", ("(±%s, 0)" if onx else "(0, ±%s)") % cs))
        if kind == "asym":
            k = F(b, a) if onx else F(a, b)
            ks = S(k)
            return mcq("双曲线 %s 的渐近线方程是什么？" % eq, "y ＝ ±%sx" % ("" if k == 1 else ks), ["y ＝ ±%sx" % ("" if k == 1 else S(1 / k)) if k != 1 else "y ＝ ±2x", "y ＝ ±%sx" % S(F(b * b, a * a)) if a != b else "y ＝ ±x/2", "x ＝ ±%sy" % ("" if k == 1 else ks)],
                       "把右边的 1 换成 0：%s，所以 <b>y ＝ ±%sx</b>。" % ("x/%d ± y/%d ＝ 0" % (a, b) if onx else "y/%d ± x/%d ＝ 0" % (a, b), "" if k == 1 else ks))
        if kind == "ecc":
            e = S(F(c, a)) if c else fq(cs, a)
            return mcq("双曲线 %s 的离心率是多少？" % eq, e, [S(F(b, a)), S(F(a, c)) if c else fq(a, cs), fq(rt(abs(a * a - b * b)), a) if a != b else "2", S(F(c2, a * a))],
                       "e ＝ c/a ＝ %s ÷ %d ＝ <b>%s</b>。" % (cs, a, e))
        if kind == "eq":
            if not c:
                return None
            return mcq("双曲线的焦点在 %s 轴上，实轴长为 %d，焦距为 %d，它的标准方程是什么？" % ("x" if onx else "y", 2 * a, 2 * c), eq,
                       [eq.replace("－", "＋"), ("%s － %s ＝ 1" % (fq("x²", a * a), fq("y²", c * c))) if onx else ("%s － %s ＝ 1" % (fq("y²", a * a), fq("x²", c * c))),
                        ("%s － %s ＝ 1" % (fq("y²", a * a), fq("x²", b * b))) if onx else ("%s － %s ＝ 1" % (fq("x²", a * a), fq("y²", b * b)))],
                       "a ＝ %d，c ＝ %d，b² ＝ c² － a² ＝ %d：<b>%s</b>。" % (a, c, b * b, eq))
        if not c:
            return None
        d1 = r.randint(c - a + 1, c + 9) if c - a + 1 > 0 else r.randint(1, 9)
        d2 = d1 + 2 * a
        if r.random() < 0.5:
            d1, d2 = d2, d1
        return mcq("双曲线 %s 上一点 P 到焦点 F₁ 的距离是 %d，且 |PF₂| %s |PF₁|，|PF₂| ＝ ？" % (eq, d1, "＞" if d2 > d1 else "＜"), str(d2), [str(abs(d1 - a)), str(d1 + a), str(abs(d1 - 2 * c))],
                   "||PF₁| － |PF₂|| ＝ 2a ＝ %d，所以 <b>|PF₂| ＝ %d</b>。" % (2 * a, d2))
    return mk


def parab(kind):
    def mk():
        r = U.R
        p = r.choice([F(1), F(2), F(3), F(4), F(6), F(8), F(1, 2), F(5), F(10), F(12)])
        form = r.choice(["y²＝", "y²＝－", "x²＝", "x²＝－"])
        coef = 2 * p
        eq = {"y²＝": "y² ＝ %sx", "y²＝－": "y² ＝ －%sx", "x²＝": "x² ＝ %sy", "x²＝－": "x² ＝ －%sy"}[form] % ("" if coef == 1 else S(coef))
        h = p / 2
        focus = {"y²＝": "(%s, 0)" % S(h), "y²＝－": "(%s, 0)" % S(-h), "x²＝": "(0, %s)" % S(h), "x²＝－": "(0, %s)" % S(-h)}[form]
        dire = {"y²＝": "x ＝ %s" % S(-h), "y²＝－": "x ＝ %s" % S(h), "x²＝": "y ＝ %s" % S(-h), "x²＝－": "y ＝ %s" % S(h)}[form]
        if kind == "focus":
            wf = {"y²＝": "(0, %s)" % S(h), "y²＝－": "(%s, 0)" % S(h), "x²＝": "(%s, 0)" % S(h), "x²＝－": "(0, %s)" % S(h)}[form]
            return mcq("抛物线 %s 的焦点坐标是什么？" % eq, focus, [wf, focus.replace(S(h), S(p)) if p != h else "(1, 0)", focus.replace(S(h), S(2 * p))],
                       "%s ＝ 2p，p ＝ %s，焦点到顶点的距离是 p/2 ＝ %s：<b>%s</b>。" % (S(coef), S(p), S(h), focus))
        if kind == "dir":
            return mcq("抛物线 %s 的准线方程是什么？" % eq, dire, [dire.replace(S(-h), S(h)) if S(-h) in dire else dire.replace(S(h), S(-h)), dire.replace(S(h).lstrip(M), S(p)) if p != h else dire + " ＋ 1", dire.replace("x", "#").replace("y", "x").replace("#", "y")],
                       "准线和焦点关于顶点对称，到顶点的距离是 p/2 ＝ %s：<b>%s</b>。" % (S(h), dire))
        if kind == "eq":
            cs_ = "" if coef == 1 else S(coef)
            other = {"y²＝": "x² ＝ %sy", "y²＝－": "x² ＝ －%sy", "x²＝": "y² ＝ %sx", "x²＝－": "y² ＝ －%sx"}[form] % cs_
            flip = {"y²＝": "y² ＝ －%sx", "y²＝－": "y² ＝ %sx", "x²＝": "x² ＝ －%sy", "x²＝－": "x² ＝ %sy"}[form] % cs_
            half = eq.replace(cs_ + ("x" if form.startswith("y") else "y"), ("" if p == 1 else S(p)) + ("x" if form.startswith("y") else "y")) if cs_ else eq.replace("x", "2x").replace("y ", "2y ")
            return mcq("焦点为 %s 的抛物线的标准方程是什么？" % focus, eq, [other, flip, half],
                       "焦点到顶点的距离 p/2 ＝ %s，p ＝ %s，2p ＝ %s：<b>%s</b>。" % (S(h), S(p), S(coef), eq))
        if kind == "dist":
            if form != "y²＝":
                return None
            x0 = r.randint(1, 12)
            return mcq("抛物线 %s 上一点 P 的横坐标是 %d，P 到焦点的距离是多少？" % (eq, x0), S(x0 + h), [S(x0 + p), S(x0), S(x0 + 2 * p)],
                       "抛物线上的点到焦点的距离等于到准线 x ＝ %s 的距离：%d ＋ %s ＝ <b>%s</b>。" % (S(-h), x0, S(h), S(x0 + h)))
        if form != "y²＝":
            return None
        x1, x2 = r.randint(1, 9), r.randint(1, 9)
        return mcq("过抛物线 %s 的焦点的直线交抛物线于 A、B 两点，A、B 的横坐标分别是 %d 和 %d，|AB| ＝ ？" % (eq, x1, x2), S(x1 + x2 + p), [S(x1 + x2), S(x1 + x2 + 2 * p), S(x1 + x2 + h)],
                   "焦点弦长 |AB| ＝ x₁ ＋ x₂ ＋ p ＝ %d ＋ %d ＋ %s ＝ <b>%s</b>。" % (x1, x2, S(p), S(x1 + x2 + p)))
    return mk


Un("elective-1", "ellipses", sort=4, dom="G", std=STD_A, seed=203104,
   title="椭圆：标准方程、焦点和离心率", short="椭圆",
   meta="高中数学选择性必修第一册“椭圆”练习题：椭圆的焦点坐标，离心率，求标准方程，焦点三角形的周长，由方程表示椭圆求参数，100题在线练习，附可打印答案。",
   kb="椭圆：|PF₁| ＋ |PF₂| ＝ 2a，a² ＝ b² ＋ c²", ks="焦点在分母较大的那一项对应的轴上；离心率 e ＝ c/a，0 ＜ e ＜ 1。",
   body=L(["平面内到两个定点 F₁、F₂ 的距离之和等于常数 2a（2a ＞ |F₁F₂|）的点的轨迹叫<b>椭圆</b>。",
           "焦点在 x 轴上的标准方程 x²/a² ＋ y²/b² ＝ 1（a ＞ b ＞ 0），c² ＝ a² － b²，焦点 (±c, 0)。",
           "长轴长 2a，短轴长 2b，焦距 2c，<b>离心率</b> e ＝ c/a，e 越接近 1 椭圆越扁。"],
          [("x²/25 ＋ y²/16 ＝ 1 的焦点", ["c² ＝ 25 － 16 ＝ 9"], "(±3, 0)"), ("同上的离心率", ["e ＝ 3/5"], "3/5")],
          [("把 c² ＝ a² － b² 写成 a² ＋ b²", "椭圆是减，双曲线才是加。"),
           ("焦点放错轴", "看哪个分母大，焦点就在哪个轴上。"),
           ("周长只算 2a", "焦点三角形的周长 ＝ 2a ＋ 2c。")]),
   faq=[("椭圆的离心率有什么意义？", "e 越大椭圆越扁，越小越接近圆。")],
   spec=lambda: [("焦点坐标", [(ellipse("elem"), 20)]), ("离心率", [(ellipse("ecc"), 20)]), ("求标准方程", [(ellipse("eq"), 20)]),
                 ("焦点三角形", [(ellipse("tri"), 20)]), ("方程表示椭圆的条件", [(ellipse("param"), 20)])])

Un("elective-1", "hyperbolas", sort=5, dom="G", std=STD_A, seed=203105,
   title="双曲线：标准方程、渐近线和离心率", short="双曲线",
   meta="高中数学选择性必修第一册“双曲线”练习题：双曲线的焦点坐标，渐近线方程，离心率，求标准方程，双曲线的定义，100题在线练习，附可打印答案。",
   kb="双曲线：||PF₁| － |PF₂|| ＝ 2a，c² ＝ a² ＋ b²", ks="x²/a² － y²/b² ＝ 1 的渐近线是 y ＝ ±(b/a)x；离心率 e ＝ c/a ＞ 1。",
   body=L(["平面内到两个定点的距离之差的绝对值等于常数 2a（2a ＜ |F₁F₂|）的点的轨迹叫<b>双曲线</b>。",
           "x²/a² － y²/b² ＝ 1 的焦点在 x 轴上，c² ＝ a² ＋ b²；正号在哪个变量前，焦点就在哪个轴上。",
           "<b>渐近线</b>：把方程右边的 1 换成 0 就得到渐近线方程。"],
          [("x²/9 － y²/16 ＝ 1 的焦点和渐近线", ["c² ＝ 9 ＋ 16 ＝ 25", "y ＝ ±4x/3"], "(±5, 0)，y ＝ ±(4/3)x"), ("同上的离心率", ["e ＝ 5/3"], "5/3")],
          [("用 c² ＝ a² － b²", "双曲线是 c² ＝ a² ＋ b²。"),
           ("焦点在 y 轴上时渐近线写成 y ＝ ±(b/a)x", "y²/a² － x²/b² ＝ 1 的渐近线是 y ＝ ±(a/b)x。"),
           ("定义里漏掉绝对值", "距离之差的绝对值是 2a，要看点在哪一支上。")]),
   faq=[("等轴双曲线是什么？", "a ＝ b 的双曲线，渐近线是 y ＝ ±x，离心率是 √2。")],
   spec=lambda: [("焦点坐标", [(hyper("elem"), 20)]), ("渐近线", [(hyper("asym"), 20)]), ("离心率", [(hyper("ecc"), 20)]),
                 ("求标准方程", [(hyper("eq"), 20)]), ("双曲线的定义", [(hyper("def"), 20)])])

Un("elective-1", "parabolas", sort=6, dom="G", std=STD_A, seed=203106,
   title="抛物线：标准方程、焦点和准线", short="抛物线",
   meta="高中数学选择性必修第一册“抛物线”练习题：抛物线的焦点坐标，准线方程，由焦点求标准方程，抛物线上的点到焦点的距离，焦点弦长，100题在线练习，附可打印答案。",
   kb="y² ＝ 2px 的焦点是 (p/2, 0)，准线是 x ＝ －p/2", ks="抛物线上的点到焦点的距离等于它到准线的距离；焦点弦长 |AB| ＝ x₁ ＋ x₂ ＋ p。",
   body=L(["平面内到定点 F 和定直线 l（F 不在 l 上）的距离相等的点的轨迹叫<b>抛物线</b>。",
           "四种标准方程：y² ＝ ±2px，x² ＝ ±2py（p ＞ 0）。一次项是哪个变量，焦点就在哪个轴上，符号决定开口方向。",
           "<b>焦半径</b>：y² ＝ 2px 上的点 P(x₀, y₀) 到焦点的距离 |PF| ＝ x₀ ＋ p/2。"],
          [("y² ＝ 8x 的焦点和准线", ["2p ＝ 8，p/2 ＝ 2"], "(2, 0)，x ＝ －2"), ("y² ＝ 4x 上横坐标为 3 的点到焦点的距离", ["3 ＋ 1"], "4")],
          [("把 2p 当成 p", "y² ＝ 8x 中 2p ＝ 8，p ＝ 4，焦点 (2, 0)。"),
           ("x² ＝ 4y 的焦点写在 x 轴上", "一次项是 y，焦点在 y 轴上：(0, 1)。"),
           ("焦半径忘了加 p/2", "到焦点的距离 ＝ 到准线的距离 ＝ x₀ ＋ p/2。")]),
   faq=[("抛物线的离心率是多少？", "抛物线的离心率 e ＝ 1。")],
   spec=lambda: [("焦点坐标", [(parab("focus"), 20)]), ("准线方程", [(parab("dir"), 20)]), ("求标准方程", [(parab("eq"), 20)]),
                 ("焦半径", [(parab("dist"), 20)]), ("焦点弦", [(parab("chord"), 20)])])


if __name__ == "__main__":
    import sys
    g = sys.argv[1]
    run_grade(g, UNITS[g], lambda r: U.setup(random.Random(r.random())), sys.argv[2:] or None)
