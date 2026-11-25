# -*- coding: utf-8 -*-
"""
中国 高中 必修第一册（人教A版 2019 の章の順）：集合、常用逻辑用语、一元二次函数・方程和不等式、函数的概念与性质、
指数与对数、指数函数与对数函数、三角函数（3 単元）。問題はすべて自前（cn_hsu の部品）。
  python3 tools/cn_hsa.py [slug…]
"""
import math
import random
from fractions import Fraction as F
import cn_hsu as U
from cn_hsu import mcq, ch, S, P, poly, lin, sup, rt, pis, iv, setstr, dec, M
from cn_common import run_grade, lesson
from ws_common import fr

G = "required-1"
STD_P = "理解集合的含义和基本关系，会进行集合的交、并、补运算；理解充分条件、必要条件、充要条件，全称量词与存在量词及其否定；掌握基本不等式，会解一元二次不等式"
STD_F = "理解函数的概念、单调性、奇偶性；掌握指数幂和对数的运算，理解指数函数、对数函数的图象和性质，会用二分法求零点的近似值"
STD_T = "理解任意角和弧度制，三角函数的定义、诱导公式和同角三角函数关系；掌握两角和与差、二倍角的公式；理解 y ＝ A sin(ωx ＋ φ) 的图象和性质"

UNITS = {}


def Un(slug, **kw):
    UNITS[slug] = kw


def L(think, ex, mist):
    return lesson(think, ex, mist)


# ================================================================== 1 集合
def sets(kind):
    def mk():
        r = U.R
        if kind == "list":
            a, b = r.sample([x for x in range(-6, 8) if x], 2)
            a, b = min(a, b), max(a, b)
            q = "用列举法表示集合 A ＝ {x | %s ＝ 0}。" % poly([1, -(a + b), a * b])
            return mcq(q, setstr([a, b]), [setstr([-b, -a]), setstr([a + b, a * b]) if a + b != a * b else setstr([a, b, 0]), setstr([a]), setstr([a, b, a + b])],
                       "解方程 %s ＝ 0，得 x ＝ %s 或 x ＝ %s，所以 <b>A ＝ %s</b>。" % (poly([1, -(a + b), a * b]), S(a), S(b), setstr([a, b])))
        if kind == "subsets":
            n = r.randint(2, 6)
            els = sorted(r.sample(range(0, 20), n))
            t = r.randint(0, 2)
            name = ["子集", "真子集", "非空真子集"][t]
            v = [2 ** n, 2 ** n - 1, 2 ** n - 2][t]
            return mcq("集合 %s 的%s有多少个？" % (setstr(els), name), "%d 个" % v,
                       ["%d 个" % x for x in (2 ** n, 2 ** n - 1, 2 ** n - 2, 2 * n, n, n * n) if x != v],
                       "含有 %d 个元素的集合有 2%s ＝ %d 个子集，真子集要去掉它本身，非空真子集还要去掉 ∅：<b>%d 个</b>。" % (n, sup(n), 2 ** n, v))
        if kind == "ops":
            U0 = list(range(1, 11))
            A_ = sorted(r.sample(U0, r.randint(3, 5)))
            B_ = sorted(r.sample(U0, r.randint(3, 5)))
            I, Un_ = sorted(set(A_) & set(B_)), sorted(set(A_) | set(B_))
            if not I or I == A_ or I == B_:
                return None
            if r.random() < 0.5:
                return mcq("已知 A ＝ %s，B ＝ %s，则 A ∩ B ＝ ？" % (setstr(A_), setstr(B_)), setstr(I), [setstr(Un_), setstr(sorted(set(A_) - set(B_))) if set(A_) - set(B_) else "∅", "∅", setstr(I + [Un_[-1]]) if Un_[-1] not in I else setstr(I[:-1])],
                           "A ∩ B 是两个集合的公共元素：<b>%s</b>。" % setstr(I))
            return mcq("已知 A ＝ %s，B ＝ %s，则 A ∪ B ＝ ？" % (setstr(A_), setstr(B_)), setstr(Un_), [setstr(I), setstr(sorted(set(A_) ^ set(B_))), setstr(A_), setstr(B_)],
                       "A ∪ B 是两个集合的所有元素（重复的只写一次）：<b>%s</b>。" % setstr(Un_))
        if kind == "comp":
            n = r.randint(6, 9)
            U0 = list(range(1, n + 1))
            A_ = sorted(r.sample(U0, r.randint(2, 4)))
            B_ = sorted(r.sample(U0, r.randint(2, 4)))
            t = r.randint(0, 2)
            if t == 0:
                ans = sorted(set(U0) - set(A_))
                return mcq("全集 U ＝ %s，A ＝ %s，则 ∁<sub>U</sub>A ＝ ？" % (setstr(U0), setstr(A_)), setstr(ans), [setstr(A_), setstr(ans[1:]) if len(ans) > 1 else "∅", setstr(U0)],
                           "∁<sub>U</sub>A 是 U 中不属于 A 的元素：<b>%s</b>。" % setstr(ans))
            if t == 1:
                ans = sorted(set(U0) - (set(A_) | set(B_)))
                if not ans:
                    return None
                return mcq("全集 U ＝ %s，A ＝ %s，B ＝ %s，则 ∁<sub>U</sub>(A ∪ B) ＝ ？" % (setstr(U0), setstr(A_), setstr(B_)), setstr(ans),
                           [setstr(sorted(set(U0) - (set(A_) & set(B_)))), setstr(sorted(set(A_) | set(B_))), setstr(sorted(set(U0) - set(A_)))],
                           "先求 A ∪ B ＝ %s，再求补集：<b>%s</b>。" % (setstr(sorted(set(A_) | set(B_))), setstr(ans)))
            ans = sorted((set(U0) - set(A_)) & set(B_))
            if not ans:
                return None
            return mcq("全集 U ＝ %s，A ＝ %s，B ＝ %s，则 (∁<sub>U</sub>A) ∩ B ＝ ？" % (setstr(U0), setstr(A_), setstr(B_)), setstr(ans),
                       [setstr(sorted(set(A_) & set(B_))) if set(A_) & set(B_) else "∅", setstr(sorted(set(U0) - set(A_))), setstr(B_)],
                       "∁<sub>U</sub>A ＝ %s，与 B 的公共元素是 <b>%s</b>。" % (setstr(sorted(set(U0) - set(A_))), setstr(ans)))
        if kind == "interval":
            a, b = sorted(r.sample(range(-6, 8), 2))
            c = r.randint(a + 1, b + 5)
            if c == b:
                return None
            # A ＝ {x | a ≤ x < b}，B ＝ {x | x > c'}
            cc = r.randint(a - 3, b - 1)
            if cc == a:
                return None
            A_ = "{x | %s ≤ x ＜ %s}" % (S(a), S(b))
            B_ = "{x | x ＞ %s}" % S(cc)
            if r.random() < 0.5:
                lo = max(a, cc)
                closed = a > cc
                ans = "{x | %s %s x ＜ %s}" % (S(lo), "≤" if closed else "＜", S(b))
                return mcq("已知 A ＝ %s，B ＝ %s，则 A ∩ B ＝ ？" % (A_, B_), ans,
                           ["{x | %s %s x ＜ %s}" % (S(lo), "＜" if closed else "≤", S(b)), "{x | x ＞ %s}" % S(min(a, cc)), "{x | %s ≤ x ＜ %s}" % (S(a), S(b)) if lo != a else "{x | x ＜ %s}" % S(b)],
                           "在数轴上画出两个集合，取公共部分：<b>%s</b>。" % ans)
            lo = min(a, cc)
            closed = a < cc
            ans = "{x | x %s %s}" % ("≥" if closed else "＞", S(lo))
            return mcq("已知 A ＝ %s，B ＝ %s，则 A ∪ B ＝ ？" % (A_, B_), ans,
                       ["{x | x %s %s}" % ("＞" if closed else "≥", S(lo)), "{x | %s %s x ＜ %s}" % (S(max(a, cc)), "≤" if a > cc else "＜", S(b)), "{x | x ＞ %s}" % S(max(a, cc))],
                       "在数轴上画出两个集合，合在一起：<b>%s</b>。" % ans)
        return None
    return mk


Un("sets", sort=1, dom="P", std=STD_P, seed=201101,
   title="集合：集合的表示、基本关系和基本运算", short="集合",
   meta="高中数学必修第一册“集合”练习题：列举法和描述法，子集和真子集的个数，交集和并集，补集，用数轴求集合的运算，100题在线练习，附可打印答案。",
   kb="含有 n 个元素的集合有 2ⁿ 个子集", ks="A ∩ B 取公共部分，A ∪ B 合在一起，∁ᵤA 取 U 中不属于 A 的部分。",
   body=L(["集合中的元素是<b>确定的、互异的、无序的</b>。表示方法有列举法 {1, 2, 3} 和描述法 {x | x ＞ 2}。",
           "A 的每个元素都是 B 的元素，A 叫 B 的<b>子集</b>，记作 A ⊆ B。含有 n 个元素的集合有 2ⁿ 个子集、2ⁿ － 1 个真子集。",
           "<b>交集</b> A ∩ B 是公共元素，<b>并集</b> A ∪ B 是全部元素，<b>补集</b> ∁ᵤA 是全集 U 中不属于 A 的元素。不等式表示的集合用数轴求。"],
          [("A ＝ {1, 2, 3}，B ＝ {2, 3, 4}，求 A ∩ B 和 A ∪ B", ["公共元素 2, 3", "全部元素 1, 2, 3, 4"], "{2, 3}，{1, 2, 3, 4}"),
           ("{a, b, c} 有几个真子集？", ["2³ ＝ 8 个子集", "去掉它本身"], "7 个")],
          [("忘了空集是任何集合的子集", "数子集时要算上 ∅。"),
           ("并集里重复写相同的元素", "集合的元素是互异的，相同的元素只写一次。"),
           ("数轴上端点的空心、实心弄错", "“≤”“≥”的端点属于集合，用实心点。")]),
   faq=[("∅ 和 {0} 一样吗？", "不一样。∅ 是没有元素的集合，{0} 有一个元素 0。"),
        ("A ⊆ B 和 A ⊊ B 有什么区别？", "A ⊆ B 允许 A ＝ B；A ⊊ B（真子集）要求 B 中至少有一个元素不属于 A。")],
   spec=lambda: [("列举法", [(sets("list"), 20)]), ("子集的个数", [(sets("subsets"), 20)]), ("交集和并集", [(sets("ops"), 20)]),
                 ("补集", [(sets("comp"), 20)]), ("用数轴求集合的运算", [(sets("interval"), 20)])])


# ================================================================== 2 常用逻辑用语
COND = ["充分不必要条件", "必要不充分条件", "充要条件", "既不充分也不必要条件"]


def _cond(pq, qp):
    return COND[0] if pq and not qp else COND[1] if qp and not pq else COND[2] if pq and qp else COND[3]


def logic(kind):
    def mk():
        r = U.R
        if kind == "cond":
            t = r.randint(0, 3)
            a, b = r.sample(range(-5, 8), 2)
            if t == 0:
                p, q, pq, qp = "x ＞ %s" % S(a), "x ＞ %s" % S(b), a >= b, b >= a
            elif t == 1:
                a = abs(a) or 2
                p, q, pq, qp = "x ＝ %d" % a, "x² ＝ %d" % (a * a), True, False
            elif t == 2:
                a = abs(a) or 3
                p, q, pq, qp = "|x| ＜ %d" % a, "x ＜ %d" % a, True, False
            else:
                a = abs(a) or 2
                p, q, pq, qp = "x² ＞ %d" % (a * a), "x ＞ %d" % a, False, True
            if r.random() < 0.5:
                p, q, pq, qp = q, p, qp, pq
            ans = _cond(pq, qp)
            return mcq("“%s”是“%s”的什么条件？" % (p, q), ans, [c for c in COND if c != ans],
                       "%s ⇒ %s %s成立，%s ⇒ %s %s成立，所以是<b>%s</b>。" % (p, q, "" if pq else "不", q, p, "" if qp else "不", ans))
        if kind == "neg":
            cs = [1, r.randint(-6, 6), r.randint(-6, 6)]
            f = poly(cs)
            op = r.choice(["＞", "≥", "＜", "≤"])
            nop = {"＞": "≤", "≥": "＜", "＜": "≥", "≤": "＞"}[op]
            if r.random() < 0.5:
                p = "∀x ∈ R，%s %s 0" % (f, op)
                ans = "∃x ∈ R，%s %s 0" % (f, nop)
                w = ["∀x ∈ R，%s %s 0" % (f, nop), "∃x ∈ R，%s %s 0" % (f, op), "∃x ∉ R，%s %s 0" % (f, nop)]
                e = "全称量词命题的否定是存在量词命题：∀ 改成 ∃，结论 “%s” 改成 “%s”。" % (op, nop)
            else:
                p = "∃x ∈ R，%s %s 0" % (f, op)
                ans = "∀x ∈ R，%s %s 0" % (f, nop)
                w = ["∃x ∈ R，%s %s 0" % (f, nop), "∀x ∈ R，%s %s 0" % (f, op), "∀x ∉ R，%s %s 0" % (f, nop)]
                e = "存在量词命题的否定是全称量词命题：∃ 改成 ∀，结论 “%s” 改成 “%s”。" % (op, nop)
            return mcq("命题 p：%s 的否定是什么？" % p, ans, w, e + "<b>%s</b>" % ans)
        if kind == "truth":
            b, c = r.randint(-6, 6), r.randint(-9, 9)
            D = b * b - 4 * c
            f = poly([1, b, c])
            if r.random() < 0.5:
                tv = D < 0
                p = "∀x ∈ R，%s ＞ 0" % f
                e = "Δ ＝ %s² － 4 × %s ＝ %d，%s。" % (P(b), P(c), D, "Δ ＜ 0，抛物线全在 x 轴上方，是真命题" if tv else "Δ ≥ 0，存在 x 使 %s ≤ 0，是假命题" % f)
            else:
                tv = D >= 0
                p = "∃x ∈ R，%s ＝ 0" % f
                e = "Δ ＝ %s² － 4 × %s ＝ %d，%s。" % (P(b), P(c), D, "Δ ≥ 0，方程有实数根，是真命题" if tv else "Δ ＜ 0，方程没有实数根，是假命题")
            ans = "真命题" if tv else "假命题"
            return mcq("命题“%s”是真命题还是假命题？" % p, ans, ["假命题" if tv else "真命题", "x ＞ 0 时才是真命题", "无法判断"], e + "<b>%s</b>" % ans)
        if kind == "param":
            k = r.randint(1, 9)
            b = 2 * k * r.choice([1, -1])
            thr = k * k
            bt = "%s %dx" % ("＋" if b > 0 else "－", abs(b))
            t = r.randint(0, 3)
            if t == 0:
                q, ans, w, e = "∀x ∈ R，x² %s ＋ a ＞ 0" % bt, "a ＞ %d" % thr, ["a ≥ %d" % thr, "a ＜ %d" % thr, "a ＞ %d" % abs(b)], "Δ ＝ %d － 4a ＜ 0" % (b * b)
            elif t == 1:
                q, ans, w, e = "∀x ∈ R，x² %s ＋ a ≥ 0" % bt, "a ≥ %d" % thr, ["a ＞ %d" % thr, "a ≤ %d" % thr, "a ≥ %d" % abs(b)], "Δ ＝ %d － 4a ≤ 0" % (b * b)
            elif t == 2:
                q, ans, w, e = "∃x ∈ R，x² %s ＋ a ＝ 0" % bt, "a ≤ %d" % thr, ["a ＜ %d" % thr, "a ≥ %d" % thr, "a ≤ %d" % abs(b)], "Δ ＝ %d － 4a ≥ 0" % (b * b)
            else:
                q, ans, w, e = "∃x ∈ R，x² %s ＋ a ＜ 0" % bt, "a ＜ %d" % thr, ["a ≤ %d" % thr, "a ＞ %d" % thr, "a ＜ %d" % abs(b)], "Δ ＝ %d － 4a ＞ 0" % (b * b)
            return mcq("命题“%s”是真命题，实数 a 的取值范围是什么？" % q, ans, w, "%s，所以 <b>%s</b>。" % (e, ans))
        a, b = sorted(r.sample(range(-5, 9), 2))
        c, d = sorted(r.sample(range(-5, 9), 2))
        if (a, b) == (c, d):
            return None
        pq = c <= a and b <= d
        qp = a <= c and d <= b
        ans = _cond(pq, qp)
        return mcq("A ＝ {x | %s ＜ x ＜ %s}，B ＝ {x | %s ＜ x ＜ %s}。“x ∈ A”是“x ∈ B”的什么条件？" % (S(a), S(b), S(c), S(d)), ans, [x for x in COND if x != ans],
                   "小范围能推出大范围。%s，所以是<b>%s</b>。" % ("A ⊊ B" if pq else ("B ⊊ A" if qp else "A、B 互不包含"), ans))
    return mk


Un("logic", sort=2, dom="P", std=STD_P, seed=201102,
   title="常用逻辑用语：充要条件和全称量词、存在量词", short="常用逻辑用语",
   meta="高中数学必修第一册“常用逻辑用语”练习题：充分条件、必要条件、充要条件，全称量词命题和存在量词命题的否定，判断命题的真假，由命题真假求参数，100题在线练习，附可打印答案。",
   kb="小范围 ⇒ 大范围：小范围是大范围的充分条件", ks="全称量词命题的否定是存在量词命题，存在量词命题的否定是全称量词命题，只否定结论。",
   body=L(["若 p ⇒ q，则 p 是 q 的<b>充分条件</b>，q 是 p 的<b>必要条件</b>；p ⇔ q 时 p 是 q 的<b>充要条件</b>。",
           "用集合来想：p 对应的集合 A，q 对应的集合 B。A ⊊ B 时 p 是 q 的充分不必要条件。",
           "“∀x ∈ M，p(x)”的否定是“∃x ∈ M，¬p(x)”；“∃x ∈ M，p(x)”的否定是“∀x ∈ M，¬p(x)”。"],
          [("“x ＞ 3”是“x ＞ 1”的什么条件？", ["x ＞ 3 ⇒ x ＞ 1", "x ＞ 1 推不出 x ＞ 3"], "充分不必要条件"),
           ("“∀x ∈ R，x² ≥ 0”的否定", ["∀ 改成 ∃", "≥ 改成 ＜"], "∃x ∈ R，x² ＜ 0")],
          [("否定时把量词留着不改", "全称量词和存在量词要互换。"),
           ("把“＞”的否定写成“＜”", "“＞”的否定是“≤”，要包括等于。"),
           ("把充分和必要弄反", "先写出 p ⇒ q 是否成立，再判断。")]),
   faq=[("命题的否定和否命题一样吗？", "不一样。命题的否定只否定结论；高中新教材主要学习全称量词命题和存在量词命题的否定。")],
   spec=lambda: [("充分条件与必要条件", [(logic("cond"), 20)]), ("用集合判断条件", [(logic("setcond"), 20)]), ("命题的否定", [(logic("neg"), 20)]),
                 ("判断命题的真假", [(logic("truth"), 20)]), ("由命题真假求参数", [(logic("param"), 20)])])


# ================================================================== 3 一元二次函数、方程和不等式
def quad(kind):
    def mk():
        r = U.R
        if kind == "basic":
            t = r.randint(0, 2)
            if t == 0:
                a, b = r.choice([(1, k * k) for k in range(1, 7)] + [(4, 9), (9, 4), (4, 1), (9, 16), (16, 9), (4, 25), (1, 36)])
                v = 2 * int(math.isqrt(a * b))
                return mcq("当 x ＞ 0 时，%s ＋ %s 的最小值是多少？" % (term(a, "x"), fr(b, "x")), str(v), [str(x) for x in (v // 2, a + b, 2 * (a + b), v + 1) if x != v],
                           "由基本不等式，%s ＋ %s ≥ 2√(%d × %d) ＝ %d，当 %s ＝ %s 时取等号。最小值是 <b>%d</b>。" % (term(a, "x"), fr(b, "x"), a, b, v, term(a, "x"), fr(b, "x"), v))
            if t == 1:
                s = r.randint(2, 20)
                v = F(s * s, 4)
                return mcq("已知 x ＞ 0，y ＞ 0，x ＋ y ＝ %d，则 xy 的最大值是多少？" % s, S(v), [S(x) for x in (F(s * s, 2), s, F(s, 2), v + 1)],
                           "xy ≤ ((x ＋ y)/2)² ＝ %s，当 x ＝ y ＝ %s 时取等号。最大值是 <b>%s</b>。" % (S(v), S(F(s, 2)), S(v)))
            p = r.randint(2, 30)
            v = 2 * math.isqrt(p) if math.isqrt(p) ** 2 == p else None
            if v is None:
                return mcq("已知 x ＞ 0，y ＞ 0，xy ＝ %d，则 x ＋ y 的最小值是多少？" % p, rt(4 * p), [rt(p), str(2 * p), str(p), rt(2 * p)],
                           "x ＋ y ≥ 2√(xy) ＝ 2√%d ＝ <b>%s</b>，当 x ＝ y 时取等号。" % (p, rt(4 * p)))
            return mcq("已知 x ＞ 0，y ＞ 0，xy ＝ %d，则 x ＋ y 的最小值是多少？" % p, str(v), [str(x) for x in (v // 2, 2 * p, p, v + 2) if x != v],
                       "x ＋ y ≥ 2√(xy) ＝ 2√%d ＝ <b>%d</b>，当 x ＝ y ＝ %d 时取等号。" % (p, v, v // 2))
        if kind == "solve":
            a, b = sorted(r.sample(range(-7, 9), 2))
            lead = r.choice([1, 1, -1])
            f = poly([lead, -lead * (a + b), lead * a * b])
            op = r.choice(["＜", "＞", "≤", "≥"])
            inside = (op in "＜≤") == (lead > 0)
            closed = op in "≤≥"
            ins = "{x | %s %s x %s %s}" % (S(a), "≤" if closed else "＜", "≤" if closed else "＜", S(b))
            out = "{x | x %s %s 或 x %s %s}" % ("≤" if closed else "＜", S(a), "≥" if closed else "＞", S(b))
            ans, w1 = (ins, out) if inside else (out, ins)
            alt = "{x | %s %s x %s %s}" % (S(-b), "≤" if closed else "＜", "≤" if closed else "＜", S(-a))
            alt2 = ins.replace("≤", "#").replace("＜", "≤").replace("#", "＜") if inside else out.replace("≤", "#").replace("＜", "≤").replace("#", "＜").replace("≥", "@").replace("＞", "≥").replace("@", "＞")
            return mcq("不等式 %s %s 0 的解集是什么？" % (f, op), ans, [w1, alt, alt2],
                       "%s的两个根是 %s 和 %s，%s，所以解集是 <b>%s</b>。" % (
                           "" if lead > 0 else "两边乘 －1 变成 %s %s 0，" % (poly([1, -(a + b), a * b]), {"＜": "＞", "＞": "＜", "≤": "≥", "≥": "≤"}[op]),
                           S(a), S(b), "取两根之间" if inside else "取两根之外", ans))
        if kind == "vieta":
            x1, x2 = r.randint(-6, 7), r.randint(-6, 7)
            b, c = -(x1 + x2), x1 * x2
            if c == 0:
                return None
            t = r.randint(0, 2)
            f = poly([1, b, c])
            if t == 0:
                v, name, e = x1 * x1 + x2 * x2, "x₁² ＋ x₂²", "(x₁ ＋ x₂)² － 2x₁x₂ ＝ %s² － 2 × %s" % (P(-b), P(c))
                w = [b * b + 2 * c, b * b, -b]
            elif t == 1:
                v, name, e = F(-b, c), "1/x₁ ＋ 1/x₂", "(x₁ ＋ x₂) ÷ x₁x₂ ＝ %s ÷ %s" % (S(-b), P(c))
                w = [F(c, -b) if b else F(1), F(b, c), -b + c]
            else:
                v, name, e = (x1 - x2) ** 2, "(x₁ － x₂)²", "(x₁ ＋ x₂)² － 4x₁x₂ ＝ %s² － 4 × %s" % (P(-b), P(c))
                w = [b * b + 4 * c, b * b - 2 * c, abs(x1 - x2)]
            return mcq("x₁、x₂ 是方程 %s ＝ 0 的两个根，%s ＝ ？" % (f, name), S(v), [S(x) for x in w],
                       "x₁ ＋ x₂ ＝ %s，x₁x₂ ＝ %s，%s ＝ %s ＝ <b>%s</b>。" % (S(-b), S(c), name, e, S(v)))
        if kind == "always":
            if r.random() < 0.6:
                c = r.randint(1, 40)
                bd = rt(4 * c)
                return mcq("不等式 x² ＋ ax ＋ %d ＞ 0 对一切实数 x 恒成立，a 的取值范围是什么？" % c, "%s%s ＜ a ＜ %s" % (M, bd, bd),
                           ["%s%s ≤ a ≤ %s" % (M, bd, bd), "a ＜ %s%s 或 a ＞ %s" % (M, bd, bd), "%s%s ＜ a ＜ %s" % (M, rt(c), rt(c))],
                           "开口向上，Δ ＝ a² － %d ＜ 0，a² ＜ %d，得 <b>%s%s ＜ a ＜ %s</b>。" % (4 * c, 4 * c, M, bd, bd))
            m = r.randint(1, 12)
            return mcq("不等式 x² － %dx ＋ m ≥ 0 对一切实数 x 恒成立，m 的取值范围是什么？" % (2 * m), "m ≥ %d" % (m * m),
                       ["m ＞ %d" % (m * m), "m ≤ %d" % (m * m), "m ≥ %d" % (2 * m)],
                       "Δ ＝ %d － 4m ≤ 0，得 <b>m ≥ %d</b>。" % (4 * m * m, m * m))
        a, b = sorted(r.sample(range(-6, 9), 2))
        B, Cc = -(a + b), a * b
        return mcq("不等式 x² ＋ bx ＋ c ＜ 0 的解集是 {x | %s ＜ x ＜ %s}，b、c 的值分别是多少？" % (S(a), S(b)), "b ＝ %s，c ＝ %s" % (S(B), S(Cc)),
                   ["b ＝ %s，c ＝ %s" % (S(-B), S(Cc)), "b ＝ %s，c ＝ %s" % (S(B), S(-Cc)), "b ＝ %s，c ＝ %s" % (S(Cc), S(B))],
                   "%s 和 %s 是方程 x² ＋ bx ＋ c ＝ 0 的两个根：b ＝ －(%s ＋ %s) ＝ %s，c ＝ %s × %s ＝ %s。<b>b ＝ %s，c ＝ %s</b>" % (S(a), S(b), S(a), P(b), S(B), S(a), P(b), S(Cc), S(B), S(Cc)))
    return mk


def term(c, v):
    return U.term(c, v)


Un("quadratic-inequalities", sort=3, dom="P", std=STD_P, seed=201103,
   title="一元二次函数、方程和不等式：基本不等式和一元二次不等式", short="一元二次函数、方程和不等式",
   meta="高中数学必修第一册“一元二次函数、方程和不等式”练习题：用基本不等式求最值，解一元二次不等式，根与系数的关系，不等式恒成立，由解集求系数，100题在线练习，附可打印答案。",
   kb="a ＞ 0，b ＞ 0 时，a ＋ b ≥ 2√(ab)，当 a ＝ b 时取等号", ks="解一元二次不等式：先求方程的根，再根据抛物线的开口，取两根之间或两根之外。",
   body=L(["<b>基本不等式</b>：a ＞ 0，b ＞ 0 时，(a ＋ b)/2 ≥ √(ab)。用它求最值要满足“一正、二定、三相等”。",
           "解<b>一元二次不等式</b> ax² ＋ bx ＋ c ＞ 0（a ＞ 0）：求出方程的两个根 x₁ ＜ x₂，“大于取两边，小于取中间”。",
           "<b>根与系数的关系</b>：x₁ ＋ x₂ ＝ －b/a，x₁x₂ ＝ c/a。不等式的解集的端点就是对应方程的根。"],
          [("解不等式 x² － x － 6 ＜ 0", ["方程的根是 －2 和 3", "小于取中间"], "{x | －2 ＜ x ＜ 3}"),
           ("x ＞ 0 时，x ＋ 4/x 的最小值", ["x ＋ 4/x ≥ 2√4 ＝ 4", "x ＝ 2 时取等号"], "4")],
          [("二次项系数是负数时直接套用口诀", "先两边乘 －1 化成二次项系数为正，同时改变不等号方向。"),
           ("用基本不等式时忘了检验能否取等号", "等号成立的条件必须能满足，否则取不到最值。"),
           ("恒成立问题写成 Δ ≤ 0", "要求严格大于 0 时，Δ ＜ 0；要求 ≥ 0 时才是 Δ ≤ 0。")]),
   faq=[("“一正、二定、三相等”是什么意思？", "两个数都是正数；和或积是定值；两个数能相等。三个条件都满足才能用基本不等式求最值。")],
   spec=lambda: [("基本不等式", [(quad("basic"), 20)]), ("解一元二次不等式", [(quad("solve"), 20)]), ("根与系数的关系", [(quad("vieta"), 20)]),
                 ("不等式恒成立", [(quad("always"), 20)]), ("由解集求系数", [(quad("coef"), 20)])])


# ================================================================== 4 函数的概念与性质
MONO = [("y ＝ 2x ＋ 1", 1, 1), ("y ＝ －3x ＋ 2", -1, -1), ("y ＝ x²", -1, 1), ("y ＝ －x²", 1, -1), ("y ＝ " + fr(1, "x"), -1, -1),
        ("y ＝ " + M + fr(1, "x"), 1, 1), ("y ＝ x³", 1, 1), ("y ＝ √x", 0, 1), ("y ＝ |x|", -1, 1), ("y ＝ －|x|", 1, -1),
        ("y ＝ (x － 1)²", -1, 0), ("y ＝ 2ˣ", 1, 1), ("y ＝ (" + fr(1, 2) + ")ˣ", -1, -1), ("y ＝ " + fr(2, "x"), -1, -1), ("y ＝ x² ＋ 2x", 0, 1)]
# (式, (−∞,0) での単調性, (0,＋∞) での単調性)：1 増、－1 減、0 どちらでもない／定義されない


def func(kind):
    def mk():
        r = U.R
        if kind == "domain":
            a, b = r.sample(range(-6, 8), 2)
            t = r.randint(0, 3)
            if t == 0:
                if b <= a:
                    return None
                f = "√(x %s %d) ＋ %s" % ("－" if a >= 0 else "＋", abs(a), fr(1, lin(1, -b)))
                ans = "[%s, %s) ∪ (%s, ＋∞)" % (S(a), S(b), S(b))
                w = [iv(a, None, True), "(%s, ＋∞)" % S(a), "[%s, %s]" % (S(a), S(b))]
                e = "x %s %d ≥ 0 且 %s ≠ 0，得 x ≥ %s 且 x ≠ %s。" % ("－" if a >= 0 else "＋", abs(a), lin(1, -b), S(a), S(b))
            elif t == 1:
                f = "√(%d － x)" % a if a >= 0 else "√(－%d － x)" % -a
                ans = iv(None, a, False, True)
                w = [iv(None, a), iv(a, None, True), iv(-a, None, True)]
                e = "%s － x ≥ 0，得 x ≤ %s。" % (S(a), S(a))
            elif t == 2:
                f = fr(1, "√(%s)" % lin(1, -a))
                ans = iv(a, None)
                w = [iv(a, None, True), iv(None, a), "R"]
                e = "被开方数大于 0（分母不能为 0）：x ＞ %s。" % S(a)
            else:
                c = abs(a) + 1
                f = fr(1, "x² － %d" % (c * c))
                ans = "{x | x ≠ ±%d}" % c
                w = ["{x | x ≠ %d}" % c, "{x | %s ＜ x ＜ %d}" % (S(-c), c), "R"]
                e = "分母 x² － %d ≠ 0，x ≠ ±%d。" % (c * c, c)
            return mcq("函数 f(x) ＝ %s 的定义域是什么？" % f, ans, w, e + "定义域是 <b>%s</b>。" % ans)
        if kind == "piece":
            a, b, c = r.randint(1, 3), r.randint(-4, 4), r.randint(1, 4)
            k = r.randint(-4, 4)

            def f(x):
                return x * x + a if x <= 0 else c * x + b
            fs = "f(x) ＝ <span class='sys'>x² ＋ %d，x ≤ 0<br>%s，x ＞ 0</span>" % (a, lin(c, b))
            if r.random() < 0.5:
                v = f(k)
                return mcq("已知 %s，求 f(%s)。" % (fs, S(k)), S(v), [S(x) for x in (k * k + a if k > 0 else c * k + b, v + 1, -v if v else 2, k * k)],
                           "%s %s 0，用 %s：f(%s) ＝ <b>%s</b>。" % (S(k), "≤" if k <= 0 else "＞", "x² ＋ %d" % a if k <= 0 else lin(c, b), S(k), S(v)))
            v1 = f(k)
            v = f(v1)
            return mcq("已知 %s，求 f(f(%s))。" % (fs, S(k)), S(v), [S(x) for x in (v1, f(-k) if f(-k) != v else v + 2, v - 1, k * k + a)],
                       "先求 f(%s) ＝ %s，再求 f(%s) ＝ <b>%s</b>。" % (S(k), S(v1), S(v1), S(v)))
        if kind == "mono":
            t = r.randint(0, 3)
            OPT = ["单调递增", "单调递减", "先减后增", "先增后减"]
            if t == 0:
                k, b = U.nz(-6, 6), r.randint(-6, 6)
                lo, hi = sorted(r.sample(range(-5, 6), 2))
                f, ans = "y ＝ %s" % lin(k, b), OPT[0 if k > 0 else 1]
                e = "一次函数 k ＝ %s %s 0" % (S(k), "＞" if k > 0 else "＜")
            elif t == 1:
                k = U.nz(-8, 8)
                lo, hi = sorted(r.sample(range(1, 9), 2))
                if r.random() < 0.5:
                    lo, hi = -hi, -lo
                f, ans = "y ＝ %s" % fr(S(k), "x"), OPT[1 if k > 0 else 0]
                e = "反比例函数 k ＝ %s %s 0，在每个象限内单调递%s" % (S(k), "＞" if k > 0 else "＜", "减" if k > 0 else "增")
            else:
                h = r.randint(-4, 4)
                a = 1 if t == 2 else -1
                lo, hi = sorted(r.sample(range(-6, 7), 2))
                f = "y ＝ %s" % poly([a, -2 * a * h, a * h * h + r.randint(-3, 3)])
                if hi <= h:
                    ans = OPT[1] if a > 0 else OPT[0]
                elif lo >= h:
                    ans = OPT[0] if a > 0 else OPT[1]
                else:
                    ans = OPT[2] if a > 0 else OPT[3]
                e = "对称轴是 x ＝ %s，开口向%s" % (S(h), "上" if a > 0 else "下")
            return mcq("函数 %s 在区间 [%s, %s] 上是怎样变化的？" % (f, S(lo), S(hi)), ans, [x for x in OPT if x != ans],
                       "%s，所以在 [%s, %s] 上<b>%s</b>。" % (e, S(lo), S(hi), ans))
        if kind == "parity":
            a, b = r.randint(1, 6), r.randint(1, 6)
            t = r.randint(0, 6)
            fs, ans = [("x³ ＋ %dx" % a, "奇函数"), ("x² ＋ %d" % a, "偶函数"), ("x² ＋ %dx" % a, "非奇非偶函数"), ("|x| ＋ %d" % a, "偶函数"),
                       ("%dx³ － %dx" % (a, b), "奇函数"), ("x⁴ － %dx²" % a, "偶函数"), ("x³ ＋ %d" % a, "非奇非偶函数")][t]
            return mcq("函数 f(x) ＝ %s 是哪一种函数？" % fs, ans, [x for x in ("奇函数", "偶函数", "非奇非偶函数", "既是奇函数又是偶函数") if x != ans],
                       "定义域关于原点对称，求 f(－x)：%s，所以是<b>%s</b>。" % ({"奇函数": "f(－x) ＝ －f(x)", "偶函数": "f(－x) ＝ f(x)"}.get(ans, "f(－x) 既不等于 f(x)，也不等于 －f(x)"), ans))
        if kind == "oddval":
            a = r.randint(-5, 5)
            k = r.randint(1, 5)
            v = k * k + a * k
            if r.random() < 0.5:
                return mcq("f(x) 是 R 上的奇函数，当 x ＞ 0 时，f(x) ＝ %s。求 f(%s)。" % (poly([1, a, 0]), S(-k)), S(-v), [S(v), S(k * k - a * k), S(-(k * k - a * k))],
                           "奇函数 f(%s) ＝ －f(%d) ＝ －(%s) ＝ <b>%s</b>。" % (S(-k), k, S(v), S(-v)))
            return mcq("f(x) 是 R 上的偶函数，当 x ＞ 0 时，f(x) ＝ %s。求 f(%s)。" % (poly([1, a, 0]), S(-k)), S(v), [S(-v), S(k * k - a * k), S(-(k * k - a * k))],
                       "偶函数 f(%s) ＝ f(%d) ＝ <b>%s</b>。" % (S(-k), k, S(v)))
        # 幂函数 y ＝ x^α が点を通る
        base, al, yv = r.choice([(4, F(1, 2), F(2)), (9, F(1, 2), F(3)), (16, F(1, 2), F(4)), (8, F(1, 3), F(2)), (27, F(1, 3), F(3)), (16, F(1, 4), F(2)),
                                 (2, F(3), F(8)), (3, F(2), F(9)), (2, F(-1), F(1, 2)), (4, F(-1, 2), F(1, 2)), (2, F(-2), F(1, 4)), (5, F(2), F(25)),
                                 (3, F(3), F(27)), (3, F(-1), F(1, 3)), (9, F(-1, 2), F(1, 3)), (25, F(1, 2), F(5)), (4, F(3, 2), F(8)), (8, F(2, 3), F(4))])
        return mcq("幂函数 y ＝ x<sup>α</sup> 的图象经过点 (%d, %s)，α ＝ ？" % (base, S(yv)), S(al), [S(-al), S(1 / al), S(al + 1), S(al * 2)],
                   "%d<sup>α</sup> ＝ %s，所以 <b>α ＝ %s</b>。" % (base, S(yv), S(al)))
    return mk


Un("functions", sort=4, dom="F", std=STD_F, seed=201104,
   title="函数的概念与性质：定义域、单调性和奇偶性", short="函数的概念与性质",
   meta="高中数学必修第一册“函数的概念与性质”练习题：求函数的定义域，分段函数求值，函数的单调性，奇偶性的判断，由奇偶性求函数值，幂函数，100题在线练习，附可打印答案。",
   kb="奇函数 f(－x) ＝ －f(x)，偶函数 f(－x) ＝ f(x)", ks="判断奇偶性先看定义域是否关于原点对称；奇函数的图象关于原点对称，偶函数的图象关于 y 轴对称。",
   body=L(["求<b>定义域</b>：分母不为 0，偶次根号下的式子 ≥ 0，二者同时满足取交集。",
           "<b>单调性</b>：在区间 D 上，x₁ ＜ x₂ 时 f(x₁) ＜ f(x₂) 叫单调递增。一次函数看 k，二次函数看对称轴，反比例函数在每个区间上单调。",
           "<b>奇偶性</b>：定义域关于原点对称，f(－x) ＝ －f(x) 是奇函数，f(－x) ＝ f(x) 是偶函数。"],
          [("f(x) ＝ √(x － 1) ＋ 1/(x － 3) 的定义域", ["x － 1 ≥ 0 且 x － 3 ≠ 0"], "[1, 3) ∪ (3, ＋∞)"),
           ("判断 f(x) ＝ x³ － x 的奇偶性", ["f(－x) ＝ －x³ ＋ x ＝ －f(x)"], "奇函数")],
          [("求定义域时漏掉分母不为 0", "每一个限制条件都要写出来，再取交集。"),
           ("说 y ＝ 1/x 在定义域上单调递减", "它在 (－∞, 0) 和 (0, ＋∞) 上分别单调递减，但不能合起来说。"),
           ("没看定义域就判断奇偶性", "定义域不关于原点对称的函数是非奇非偶函数。")]),
   faq=[("分段函数求 f(f(a)) 要注意什么？", "从里往外算：先求 f(a)，再看这个值在哪一段，用那一段的式子。")],
   spec=lambda: [("函数的定义域", [(func("domain"), 20)]), ("分段函数求值", [(func("piece"), 20)]), ("函数的单调性", [(func("mono"), 20)]),
                 ("函数的奇偶性", [(func("parity"), 12), (func("oddval"), 8)]), ("奇偶性的应用和幂函数", [(func("oddval"), 10), (func("power"), 10)])])


# ================================================================== 5 指数与对数的运算
POW = [(4, 2), (8, 3), (9, 2), (16, 2), (16, 4), (25, 2), (27, 3), (32, 5), (64, 2), (64, 3), (64, 6), (81, 2), (81, 4), (125, 3), (100, 2), (1000, 3)]


def explog(kind):
    def mk():
        r = U.R
        if kind == "pow":
            n, k = r.choice(POW)
            root = round(n ** (1 / k))
            m = r.choice([1, 2, 3, -1, -2])
            if m < 0 and abs(m) > 2:
                return None
            v = F(root) ** m
            ef = F(abs(m), k)
            es = (M if m < 0 else "") + (str(ef.numerator) if ef.denominator == 1 else "%d/%d" % (ef.numerator, ef.denominator))
            return mcq("计算：%d<sup>%s</sup> ＝ ？" % (n, es), S(v), [S(x) for x in (F(n) * F(m, k), -v, F(root) ** (-m), v * root)],
                       "%d ＝ %d<sup>%d</sup>，所以 %d<sup>%s</sup> ＝ %d<sup>%s</sup> ＝ <b>%s</b>。" % (n, root, k, n, es, root, S(m), S(v)))
        if kind == "simp":
            a, b, c = F(r.randint(1, 5), r.choice([2, 3, 4])), F(r.randint(1, 5), r.choice([2, 3, 6])), F(r.randint(1, 5), r.choice([2, 3, 4, 6]))
            v = a + b - c

            def e(x):
                return "<sup>%s</sup>" % (("%d" % x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)) if x != 1 else ""

            def ex(x):
                return "a" + ("<sup>%s%d/%d</sup>" % ("－" if x < 0 else "", abs(x.numerator), x.denominator) if x.denominator != 1 else ("<sup>%s%d</sup>" % ("－" if x < 0 else "", abs(x.numerator)) if x != 1 else "")) if x != 0 else "1"
            return mcq("化简：a%s · a%s ÷ a%s（a ＞ 0）" % (e(a), e(b), e(c)), ex(v), [ex(a * b / c) if a * b / c != v else ex(v + 1), ex(a + b + c), ex(a - b + c) if a - b + c != v else ex(v - 1)],
                       "同底数幂相乘指数相加，相除指数相减：%s ＋ %s － %s ＝ %s，所以是 <b>%s</b>。" % (S(a), S(b), S(c), S(v), ex(v)))
        if kind == "log":
            b = r.choice([2, 3, 5, 10, 4, 9])
            k = r.randint(-3, 5)
            arg = F(b) ** k
            name = "lg" if b == 10 else "log<sub>%d</sub>" % b
            return mcq("计算：%s %s ＝ ？" % (name, S(arg)), S(k), [S(x) for x in (-k, arg / b if arg / b != k else k + 1, k + 1, b * k)],
                       "%s ＝ %d<sup>%s</sup>，所以 %s %s ＝ <b>%s</b>。" % (S(arg), b, S(k), name, S(arg), S(k)))
        if kind == "rules":
            b = r.choice([2, 3, 5, 10, 6])
            t = r.randint(0, 2)
            name = "lg" if b == 10 else "log<sub>%d</sub>" % b
            k = r.randint(1, 4)
            tot = b ** k
            divs = [d for d in range(2, tot) if tot % d == 0 and d != b and tot // d != b]
            if not divs:
                return None
            m = r.choice(divs)
            n = tot // m
            if t == 0:
                return mcq("计算：%s %d ＋ %s %d ＝ ？" % (name, m, name, n), str(k), [str(x) for x in (k + 1, m + n, k - 1 if k > 1 else k + 2)],
                           "%s %d ＋ %s %d ＝ %s %d ＝ <b>%d</b>。" % (name, m, name, n, name, tot, k))
            if t == 1:
                return mcq("计算：%s %d － %s %d ＝ ？" % (name, tot * m, name, m), str(k), [str(x) for x in (k + 1, tot * m - m, k * m)],
                           "%s %d － %s %d ＝ %s %d ＝ <b>%d</b>。" % (name, tot * m, name, m, name, tot, k))
            c = r.randint(2, 6)
            if b ** 2 % c:
                return None
            return mcq("计算：2%s %d － %s %d ＝ ？" % (name, c * b, name, c * c), "2", ["1", "0", str(c), "4"],
                       "2%s %d ＝ %s %d，%s %d － %s %d ＝ %s %d ＝ <b>2</b>。" % (name, c * b, name, c * c * b * b, name, c * c * b * b, name, c * c, name, b * b))
        if kind == "base":
            t = r.randint(0, 1)
            if t == 0:
                a, b = r.choice([(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (2, 7), (3, 7)])
                k = r.randint(2, 4)
                return mcq("计算：log<sub>%d</sub> %d · log<sub>%d</sub> %d ＝ ？" % (a, b, b, a ** k), str(k), [str(x) for x in (k + 1, a * k, b ** k, 1) if x != k],
                           "换底公式：log<sub>%d</sub> %d · log<sub>%d</sub> %d ＝ log<sub>%d</sub> %d ＝ <b>%d</b>。" % (a, b, b, a ** k, a, a ** k, k))
            i, j = r.randint(0, 4), r.randint(0, 3)
            n = 2 ** i * 3 ** j
            if n < 4:
                return None
            ans = (("%sa" % ("" if i == 1 else i)) if i else "") + ((" ＋ " if i else "") + ("%sb" % ("" if j == 1 else j)) if j else "")
            w = ["%da%s" % (i * j or 1, "b" if j else ""), ("%sa ＋ %sb" % (j or "", i or "")).replace(" 1a", " a"), "%d(a ＋ b)" % (i + j)]
            return mcq("已知 lg 2 ＝ a，lg 3 ＝ b，用 a、b 表示 lg %d。" % n, ans, w,
                       "%d ＝ %s，lg %d ＝ %s ＝ <b>%s</b>。" % (n, " × ".join(["2"] * i + ["3"] * j), n, " ＋ ".join(["lg 2"] * i + ["lg 3"] * j), ans))
        return None
    return mk


Un("exponents-and-logarithms", sort=5, dom="F", std=STD_F, seed=201105,
   title="指数与对数的运算：分数指数幂和对数的运算性质", short="指数与对数的运算",
   meta="高中数学必修第一册“指数与对数”练习题：分数指数幂的计算，指数幂的运算性质，求对数的值，对数的运算性质，换底公式，100题在线练习，附可打印答案。",
   kb="aᵇ ＝ N ⇔ b ＝ logₐN（a ＞ 0，a ≠ 1，N ＞ 0）", ks="logₐM ＋ logₐN ＝ logₐ(MN)，logₐM － logₐN ＝ logₐ(M/N)，换底公式 logₐb ＝ log_c b ÷ log_c a。",
   body=L(["<b>分数指数幂</b>：a<sup>m/n</sup> ＝ ⁿ√(aᵐ)，a<sup>－m/n</sup> ＝ 1 ÷ a<sup>m/n</sup>。运算性质：aʳ·aˢ ＝ aʳ⁺ˢ，(aʳ)ˢ ＝ aʳˢ。",
           "<b>对数</b>：若 aᵇ ＝ N，则 b ＝ logₐN。以 10 为底记作 lg N，以 e 为底记作 ln N。",
           "运算性质：logₐ(MN) ＝ logₐM ＋ logₐN，logₐ(M/N) ＝ logₐM － logₐN，logₐMⁿ ＝ n logₐM。"],
          [("8<sup>2/3</sup>", ["8 ＝ 2³", "(2³)<sup>2/3</sup> ＝ 2²"], "4"), ("lg 4 ＋ lg 25", ["＝ lg 100"], "2")],
          [("把 logₐ(M ＋ N) 写成 logₐM ＋ logₐN", "对数的性质是积变和，不是和变和。"),
           ("负指数当成负数", "2<sup>－2</sup> ＝ 1/4，是正数。"),
           ("忘了对数的真数要大于 0", "logₐN 中 N ＞ 0，底数 a ＞ 0 且 a ≠ 1。")]),
   faq=[("lg 2 和 lg 5 有什么关系？", "lg 2 ＋ lg 5 ＝ lg 10 ＝ 1，所以 lg 5 ＝ 1 － lg 2。")],
   spec=lambda: [("分数指数幂", [(explog("pow"), 20)]), ("指数幂的运算", [(explog("simp"), 20)]), ("求对数的值", [(explog("log"), 20)]),
                 ("对数的运算性质", [(explog("rules"), 20)]), ("换底公式", [(explog("base"), 20)])])


# ================================================================== 6 指数函数与对数函数
def expfn(kind):
    def mk():
        r = U.R
        if kind == "fixed":
            m, n = r.randint(-4, 4), r.randint(-4, 4)
            if r.random() < 0.5:
                f = "y ＝ a<sup>x %s %d</sup> %s %d" % ("－" if m >= 0 else "＋", abs(m), "＋" if n >= 0 else "－", abs(n))
                ans = "(%s, %s)" % (S(m), S(1 + n))
                w = ["(%s, %s)" % (S(-m), S(1 + n)), "(%s, %s)" % (S(m), S(n)), "(0, %s)" % S(1 + n)]
                e = "a⁰ ＝ 1，令 x %s %d ＝ 0，x ＝ %s，y ＝ 1 ＋ %s ＝ %s。" % ("－" if m >= 0 else "＋", abs(m), S(m), P(n), S(1 + n))
            else:
                f = "y ＝ log<sub>a</sub>(x %s %d) %s %d" % ("－" if m >= 0 else "＋", abs(m), "＋" if n >= 0 else "－", abs(n))
                ans = "(%s, %s)" % (S(m + 1), S(n))
                w = ["(%s, %s)" % (S(m), S(n)), "(%s, %s)" % (S(m + 1), S(n + 1)), "(1, %s)" % S(n)]
                e = "logₐ1 ＝ 0，令 x %s %d ＝ 1，x ＝ %s，y ＝ %s。" % ("－" if m >= 0 else "＋", abs(m), S(m + 1), S(n))
            return mcq("函数 %s（a ＞ 0，a ≠ 1）的图象一定经过哪个点？" % f, ans, w, e + "定点是 <b>%s</b>。" % ans)
        if kind == "cmp":
            p = r.choice([2, 3, 5])
            q = F(r.randint(1, 9), 10)
            k = r.choice([2, 3])
            vals = {"a": "%d<sup>%s</sup>" % (p, dec(float(q), 1)), "b": "%s<sup>%d</sup>" % (dec(float(q), 1), k), "c": "log<sub>%d</sub> %s" % (p, dec(float(q), 1))}
            # a ＞ 1，0 ＜ b ＜ 1，c ＜ 0
            names = ["a", "b", "c"]
            r.shuffle(names)
            lab = dict(zip(["big", "mid", "neg"], names))
            q_ = "设 %s，比较大小。" % "，".join("%s ＝ %s" % (lab[x], vals[{"big": "a", "mid": "b", "neg": "c"}[x]]) for x in ("big", "mid", "neg"))
            ans = "%s ＞ %s ＞ %s" % (lab["big"], lab["mid"], lab["neg"])
            w = ["%s ＞ %s ＞ %s" % (lab["mid"], lab["big"], lab["neg"]), "%s ＞ %s ＞ %s" % (lab["big"], lab["neg"], lab["mid"]), "%s ＞ %s ＞ %s" % (lab["neg"], lab["mid"], lab["big"])]
            return mcq(q_, ans, w, "用 0 和 1 作中间量：%s ＞ 1，0 ＜ %s ＜ 1，%s ＜ 0。所以 <b>%s</b>。" % (vals["a"], vals["b"], vals["c"], ans))
        if kind == "ineq":
            t = r.randint(0, 3)
            a, b = r.randint(-4, 5), r.randint(-3, 4)
            if t == 0:
                return mcq("解不等式 2<sup>x %s %d</sup> ＞ %s。" % ("－" if a >= 0 else "＋", abs(a), S(F(2) ** b)), "x ＞ %s" % S(a + b),
                           ["x ＜ %s" % S(a + b), "x ＞ %s" % S(b - a), "x ＞ %s" % S(b)],
                           "%s ＝ 2<sup>%s</sup>，y ＝ 2ˣ 是增函数，x %s %d ＞ %s，<b>x ＞ %s</b>。" % (S(F(2) ** b), S(b), "－" if a >= 0 else "＋", abs(a), S(b), S(a + b)))
            if t == 1:
                return mcq("解不等式 (%s)<sup>x</sup> ＞ %s。" % (fr(1, 2), S(F(1, 2) ** b)), "x ＜ %s" % S(b), ["x ＞ %s" % S(b), "x ＜ %s" % S(-b) if b else "x ＞ 1", "x ＞ %s" % S(-b) if b else "x ＜ 1"],
                           "y ＝ (1/2)ˣ 是减函数，所以 <b>x ＜ %s</b>。" % S(b))
            if t == 2:
                k = r.randint(1, 5)
                return mcq("解不等式 log<sub>2</sub> x ＜ %d。" % k, "0 ＜ x ＜ %d" % 2 ** k, ["x ＜ %d" % 2 ** k, "x ＞ %d" % 2 ** k, "0 ＜ x ＜ %d" % (2 * k)],
                           "y ＝ log₂x 是增函数，且真数 x ＞ 0：<b>0 ＜ x ＜ %d</b>。" % 2 ** k)
            k = r.randint(1, 4)
            return mcq("解不等式 log<sub>%s</sub> x ＞ %d。" % ("1/2", k), "0 ＜ x ＜ %s" % S(F(1, 2 ** k)), ["x ＞ %s" % S(F(1, 2 ** k)), "x ＜ %s" % S(F(1, 2 ** k)), "0 ＜ x ＜ %d" % 2 ** k],
                       "y ＝ log<sub>1/2</sub>x 是减函数，且 x ＞ 0：<b>0 ＜ x ＜ %s</b>。" % S(F(1, 2 ** k)))
        if kind == "zero":
            k = r.randint(3, 40)
            f = lambda x: 2 ** x + x - k
            n = 0
            while f(n + 1) < 0:
                n += 1
            if f(n) == 0 or f(n + 1) == 0:
                return None
            return mcq("函数 f(x) ＝ 2ˣ ＋ x － %d 的零点所在的区间是哪一个？" % k, "(%d, %d)" % (n, n + 1), ["(%d, %d)" % (x, x + 1) for x in (n - 1, n + 1, n + 2) if x >= 0] + ["(%d, %d)" % (n + 3, n + 4)],
                       "f(x) 是增函数，f(%d) ＝ %s ＜ 0，f(%d) ＝ %s ＞ 0，由零点存在定理，零点在 <b>(%d, %d)</b> 内。" % (n, S(f(n)), n + 1, S(f(n + 1)), n, n + 1))
        a = r.choice([100, 200, 500, 1000, 50, 300])
        t = r.randint(2, 6)
        if r.random() < 0.5:
            return mcq("某种细菌每小时分裂一次（个数变成原来的 2 倍）。开始有 %d 个，%d 小时后有多少个？" % (a, t), "%d 个" % (a * 2 ** t),
                       ["%d 个" % x for x in (a * 2 * t, a * 2 ** (t - 1), a + 2 ** t, a * t * t)],
                       "y ＝ %d × 2ˣ，x ＝ %d 时 y ＝ %d × 2<sup>%d</sup> ＝ <b>%d 个</b>。" % (a, t, a, t, a * 2 ** t))
        h = r.choice([2, 3, 5, 8, 10])
        m = a * 2 ** t
        return mcq("某放射性物质的半衰期是 %d 年。原有 %d 克，经过 %d 年后还剩多少克？" % (h, m, h * t), "%d 克" % a,
                   ["%d 克" % x for x in (m // 2, m // (2 * t), m - a, m // t) if x != a],
                   "每过 %d 年减少一半，经过 %d 个半衰期：%d × (1/2)<sup>%d</sup> ＝ <b>%d 克</b>。" % (h, t, m, t, a))
    return mk


Un("exponential-and-logarithmic-functions", sort=6, dom="F", std=STD_F, seed=201106,
   title="指数函数与对数函数：图象、性质和函数的零点", short="指数函数与对数函数",
   meta="高中数学必修第一册“指数函数与对数函数”练习题：图象过定点，比较大小，解指数不等式和对数不等式，零点存在定理，指数增长和衰减模型，100题在线练习，附可打印答案。",
   kb="a ＞ 1 时 y ＝ aˣ 和 y ＝ logₐx 都是增函数；0 ＜ a ＜ 1 时都是减函数", ks="y ＝ aˣ 的图象过 (0, 1)，y ＝ logₐx 的图象过 (1, 0)。比较大小常用 0 和 1 作中间量。",
   body=L(["<b>指数函数</b> y ＝ aˣ（a ＞ 0，a ≠ 1）：定义域 R，值域 (0, ＋∞)，图象过 (0, 1)。",
           "<b>对数函数</b> y ＝ logₐx：定义域 (0, ＋∞)，值域 R，图象过 (1, 0)。它和 y ＝ aˣ 互为反函数。",
           "<b>零点存在定理</b>：f(x) 在 [a, b] 上连续，且 f(a)·f(b) ＜ 0，则在 (a, b) 内至少有一个零点。"],
          [("比较 2<sup>0.3</sup>、0.3²、log₂0.3", ["2<sup>0.3</sup> ＞ 1，0 ＜ 0.3² ＜ 1，log₂0.3 ＜ 0"], "2<sup>0.3</sup> ＞ 0.3² ＞ log₂0.3"),
           ("解 log₂x ＜ 3", ["增函数", "x ＞ 0"], "0 ＜ x ＜ 8")],
          [("解对数不等式时忘了真数大于 0", "log₂x ＜ 3 的解是 0 ＜ x ＜ 8，不是 x ＜ 8。"),
           ("底数小于 1 时不等号方向没变", "0 ＜ a ＜ 1 时函数是减函数，去掉底数后不等号要反向。"),
           ("零点区间只看一个端点", "要看两个端点函数值的符号是否相反。")]),
   faq=[("二分法是什么？", "在零点所在的区间中取中点，看函数值的符号，把区间一分为二，不断缩小范围，得到零点的近似值。")],
   spec=lambda: [("图象过定点", [(expfn("fixed"), 20)]), ("比较大小", [(expfn("cmp"), 20)]), ("解指数不等式和对数不等式", [(expfn("ineq"), 20)]),
                 ("函数的零点", [(expfn("zero"), 20)]), ("增长和衰减模型", [(expfn("model"), 20)])])


# ================================================================== 7〜9 三角函数
SPV = {0: ("0", "1", "0"), 30: ("1/2", "√3/2", "√3/3"), 45: ("√2/2", "√2/2", "1"), 60: ("√3/2", "1/2", "√3"), 90: ("1", "0", None),
       120: ("√3/2", "－1/2", "－√3"), 135: ("√2/2", "－√2/2", "－1"), 150: ("1/2", "－√3/2", "－√3/3"), 180: ("0", "－1", "0"),
       210: ("－1/2", "－√3/2", "√3/3"), 225: ("－√2/2", "－√2/2", "1"), 240: ("－√3/2", "－1/2", "√3"), 270: ("－1", "0", None),
       300: ("－√3/2", "1/2", "－√3"), 315: ("－√2/2", "√2/2", "－1"), 330: ("－1/2", "√3/2", "－√3/3")}


def H(s):
    """“－√3/2” → HTML の分数"""
    if s is None:
        return "不存在"
    neg = s.startswith("－")
    s = s.lstrip("－")
    if "/" in s:
        a, b = s.split("/")
        s = fr(a, b)
    return (M if neg else "") + s


def trig1(kind):
    def mk():
        r = U.R
        if kind == "rad":
            d = r.choice([15, 18, 20, 30, 36, 40, 45, 60, 72, 75, 90, 105, 120, 135, 150, 210, 225, 240, 270, 300, 315, 330, 360, 405, 480, 540]) * r.choice([1, 1, -1])
            q = F(d, 180)
            if r.random() < 0.5:
                return mcq("把 %s° 化成弧度。" % S(d), pis(q), [pis(F(d, 360)), pis(q * 2), pis(-q), pis(F(180, d)) if d else "π"],
                           "1° ＝ π/180，%s° ＝ %s × π/180 ＝ <b>%s</b>。" % (S(d), S(d), pis(q)))
            return mcq("把 %s 化成角度。" % pis(q), "%s°" % S(d), ["%s°" % S(x) for x in (2 * d, d // 2 if d % 2 == 0 else d + 30, -d, d + 180)],
                       "π ＝ 180°，%s ＝ <b>%s°</b>。" % (pis(q), S(d)))
        if kind == "quad":
            d = r.randint(-720, 720)
            if d % 90 == 0:
                return None
            m = d % 360
            qd = m // 90 + 1
            names = ["第一象限", "第二象限", "第三象限", "第四象限"]
            if r.random() < 0.5:
                return mcq("%s° 角是第几象限的角？" % S(d), names[qd - 1], [x for x in names if x != names[qd - 1]],
                           "%s° ＝ %s° ＋ %d × 360°，%d° 是%s的角，所以 %s° 也是<b>%s</b>的角。" % (S(d), m, (d - m) // 360, m, names[qd - 1], S(d), names[qd - 1]))
            return mcq("与 %s° 角终边相同的最小正角是多少？" % S(d), "%d°" % m, ["%d°" % x for x in (360 - m, abs(d) % 180 if abs(d) % 180 != m else m + 90, (m + 180) % 360, abs(d)) if x != m],
                       "%s° ＝ %d° ＋ %s × 360°，最小正角是 <b>%d°</b>。" % (S(d), m, P((d - m) // 360), m))
        if kind == "point":
            a, b, c = r.choice(U.TRIPLES)
            x, y = a * r.choice([1, -1]), b * r.choice([1, -1])
            if r.random() < 0.5:
                x, y = y, x
            fn = r.choice(["sin", "cos", "tan"])
            v = {"sin": F(y, c), "cos": F(x, c), "tan": F(y, x)}[fn]
            w = [F(x, c), F(y, c), F(y, x), F(x, y), -v]
            return mcq("角 α 的终边经过点 P(%s, %s)，%s α ＝ ？" % (S(x), S(y), fn), S(v), [S(t) for t in w if t != v],
                       "r ＝ √(%s² ＋ %s²) ＝ %d，%s α ＝ %s ＝ <b>%s</b>。" % (P(x), P(y), c, fn, {"sin": "y/r", "cos": "x/r", "tan": "y/x"}[fn], S(v)))
        if kind == "same":
            a, b, c = r.choice(U.TRIPLES)
            qd = r.randint(1, 4)
            sx, sy = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}[qd]
            sv, cv = F(sy * b, c), F(sx * a, c)
            names = ["第一", "第二", "第三", "第四"]
            if r.random() < 0.5:
                return mcq("已知 sin α ＝ %s，α 是%s象限角，cos α ＝ ？" % (S(sv), names[qd - 1]), S(cv), [S(-cv), S(sv), S(F(sy * b, sx * a))],
                           "sin²α ＋ cos²α ＝ 1，cos²α ＝ %s，α 在%s象限，cos α %s 0，<b>cos α ＝ %s</b>。" % (S(cv * cv), names[qd - 1], "＞" if cv > 0 else "＜", S(cv)))
            tv = sv / cv
            return mcq("已知 cos α ＝ %s，α 是%s象限角，tan α ＝ ？" % (S(cv), names[qd - 1]), S(tv), [S(-tv), S(1 / tv), S(sv)],
                       "sin α ＝ %s，tan α ＝ sin α ÷ cos α ＝ <b>%s</b>。" % (S(sv), S(tv)))
        base = r.choice([d for d in SPV if d % 90])
        k = r.choice([-1, 0, 1, 2])
        d = base + 360 * k
        fn = r.randint(0, 2)
        v = SPV[base][fn]
        if v is None:
            return None
        name = ["sin", "cos", "tan"][fn]
        w = {SPV[x][fn] for x in SPV if SPV[x][fn] and SPV[x][fn] != v}
        w = sorted(w, key=lambda s_: (s_.lstrip("－") != v.lstrip("－"), s_))[:3]
        return mcq("计算：%s %s° ＝ ？" % (name, S(d)), H(v), [H(x) for x in w],
                   "%s° 的终边与 %d° 相同，用诱导公式化成锐角：%s %s° ＝ <b>%s</b>。" % (S(d), base, name, S(d), H(v)))
    return mk


Un("angles-and-trigonometric-functions", sort=7, dom="F", std=STD_T, seed=201107,
   title="三角函数：任意角、弧度制、三角函数的定义和诱导公式", short="三角函数的概念",
   meta="高中数学必修第一册“三角函数”练习题：角度和弧度的互化，象限角和终边相同的角，用终边上的点求三角函数值，同角三角函数的基本关系，诱导公式，100题在线练习，附可打印答案。",
   kb="sin²α ＋ cos²α ＝ 1，tan α ＝ sin α ÷ cos α", ks="终边上一点 P(x, y)，r ＝ √(x² ＋ y²)：sin α ＝ y/r，cos α ＝ x/r，tan α ＝ y/x。",
   body=L(["<b>弧度制</b>：π ＝ 180°。角度化弧度乘 π/180，弧度化角度乘 180/π。",
           "<b>三角函数的定义</b>：角 α 终边上一点 P(x, y)，r ＝ |OP|，sin α ＝ y/r，cos α ＝ x/r，tan α ＝ y/x。符号口诀“一全正、二正弦、三正切、四余弦”。",
           "<b>诱导公式</b>：“奇变偶不变，符号看象限”。例如 sin(π － α) ＝ sin α，cos(π ＋ α) ＝ －cos α。"],
          [("150° 化成弧度", ["150 × π/180"], "5π/6"), ("sin α ＝ 3/5，α 在第二象限，求 cos α", ["cos²α ＝ 1 － 9/25 ＝ 16/25", "第二象限 cos α ＜ 0"], "－4/5")],
          [("同角关系开方后忘了判断符号", "先看角在哪个象限，再决定正负。"),
           ("把 r 当成 1", "只有在单位圆上 r ＝ 1；一般要先算 r ＝ √(x² ＋ y²)。"),
           ("弧度和角度混用", "写弧度时不带“°”，写角度时一定带“°”。")]),
   faq=[("“奇变偶不变，符号看象限”是什么意思？", "k·π/2 ± α 中，k 是奇数时函数名改变（sin ↔ cos），偶数时不变；符号按把 α 看成锐角时原函数值的符号来定。")],
   spec=lambda: [("弧度制", [(trig1("rad"), 20)]), ("象限角和终边相同的角", [(trig1("quad"), 20)]), ("三角函数的定义", [(trig1("point"), 20)]),
                 ("同角三角函数的基本关系", [(trig1("same"), 20)]), ("诱导公式", [(trig1("induce"), 20)])])


def trig2(kind):
    def mk():
        r = U.R
        (a1, b1, c1), (a2, b2, c2) = r.choice(U.TRIPLES), r.choice(U.TRIPLES)
        if r.random() < 0.5:
            a1, b1 = b1, a1
        if r.random() < 0.5:
            a2, b2 = b2, a2
        sa, ca = F(b1, c1), F(a1, c1)
        sb, cb = F(b2, c2), F(a2, c2)
        if kind == "sum":
            t = r.randint(0, 3)
            name, v = [("cos(α ＋ β)", ca * cb - sa * sb), ("cos(α － β)", ca * cb + sa * sb), ("sin(α ＋ β)", sa * cb + ca * sb), ("sin(α － β)", sa * cb - ca * sb)][t]
            w = [ca * cb + sa * sb, ca * cb - sa * sb, sa * cb + ca * sb, sa * cb - ca * sb, -v]
            return mcq("α、β 都是锐角，sin α ＝ %s，cos β ＝ %s，%s ＝ ？" % (S(sa), S(cb), name), S(v), [S(x) for x in w if x != v],
                       "cos α ＝ %s，sin β ＝ %s，代入两角和与差的公式：%s ＝ <b>%s</b>。" % (S(ca), S(sb), name, S(v)))
        if kind == "double":
            q2 = r.choice([1, 2])
            s, c = (sa, ca) if q2 == 1 else (sa, -ca)
            t = r.randint(0, 2)
            name, v = [("sin 2α", 2 * s * c), ("cos 2α", 1 - 2 * s * s), ("tan 2α", 2 * (s / c) / (1 - (s / c) ** 2))][t]
            w = [2 * s * c, 1 - 2 * s * s, -v, 2 * s, s * s - c * c]
            return mcq("已知 sin α ＝ %s，α 是第%s象限角，%s ＝ ？" % (S(s), "一" if q2 == 1 else "二", name), S(v), [S(x) for x in w if x != v],
                       "cos α ＝ %s，%s ＝ <b>%s</b>（sin 2α ＝ 2 sin α cos α，cos 2α ＝ 1 － 2sin²α，tan 2α ＝ 2tan α ÷ (1 － tan²α)）。" % (S(c), name, S(v)))
        if kind == "tan":
            p, q = F(r.randint(-5, 5), r.choice([1, 1, 2, 3])), F(r.randint(-5, 5), r.choice([1, 2, 3]))
            if p * q == 1 or p * q == -1 or p == 0 or q == 0 or p == q:
                return None
            if r.random() < 0.5:
                v = (p + q) / (1 - p * q)
                return mcq("tan α ＝ %s，tan β ＝ %s，tan(α ＋ β) ＝ ？" % (S(p), S(q)), S(v), [S(x) for x in ((p + q) / (1 + p * q), (p - q) / (1 + p * q), p + q, -v)],
                           "tan(α ＋ β) ＝ (tan α ＋ tan β) ÷ (1 － tan α tan β) ＝ <b>%s</b>。" % S(v))
            v = (p - q) / (1 + p * q)
            return mcq("tan α ＝ %s，tan β ＝ %s，tan(α － β) ＝ ？" % (S(p), S(q)), S(v), [S(x) for x in ((p - q) / (1 - p * q), (p + q) / (1 - p * q), p - q, -v)],
                       "tan(α － β) ＝ (tan α － tan β) ÷ (1 ＋ tan α tan β) ＝ <b>%s</b>。" % S(v))
        if kind == "aux":
            t = r.randint(0, 3)
            k = r.randint(1, 4)
            if t == 3:
                wv = r.randint(1, 4)
                kk = "" if k == 1 else str(k)
                ws = "" if wv == 1 else str(wv)
                return mcq("函数 y ＝ %s√3 sin %sx － %scos %sx 的最小正周期和最大值分别是多少？" % (kk, ws, kk, ws), "%s，%d" % (pis(F(2, wv)), 2 * k),
                           ["%s，%d" % (pis(F(1, wv)), 2 * k), "%s，%s" % (pis(F(2, wv)), rt(3, k)), "%s，%d" % (pis(F(2, wv)), 4 * k)],
                           "原式 ＝ %d sin(%sx － π/6)，T ＝ 2π/%d ＝ %s，最大值 %d。<b>%s，%d</b>" % (2 * k, ws, wv, pis(F(2, wv)), 2 * k, pis(F(2, wv)), 2 * k))
            if t == 0:
                a, b, c = r.choice(U.TRIPLES)
                b = b * r.choice([1, -1])
                ftxt = "%dsin x %s %dcos x" % (a, "＋" if b > 0 else "－", abs(b))
                return mcq("函数 y ＝ %s 的最大值是多少？" % ftxt, str(c), [str(a + abs(b)), str(max(a, abs(b))), str(c * c)],
                           "a sin x ＋ b cos x ＝ √(a² ＋ b²) sin(x ＋ φ)，最大值是 √(%d ＋ %d) ＝ <b>%d</b>。" % (a * a, b * b, c))
            if t == 1:
                kk = "" if k == 1 else str(k)
                return mcq("函数 y ＝ %ssin x ＋ %s√3 cos x 的最大值是多少？" % (kk, kk), str(2 * k), [rt(3, k), str(4 * k), str(k), rt(2, 2 * k)],
                           "原式 ＝ %d sin(x ＋ π/3)，最大值是 <b>%d</b>。" % (2 * k, 2 * k))
            w = r.choice([1, 2, 3, 4])
            return mcq("函数 y ＝ sin %sx ＋ cos %sx 的最小正周期和最大值分别是多少？" % ("" if w == 1 else w, "" if w == 1 else w), "%s，√2" % pis(F(2, w)),
                       ["%s，2" % pis(F(2, w)), "%s，√2" % pis(F(1, w)), "%s，2" % pis(F(1, w))],
                       "y ＝ √2 sin(%sx ＋ π/4)，T ＝ 2π/%d ＝ %s，最大值 √2。答案是 <b>%s，√2</b>。" % ("" if w == 1 else w, w, pis(F(2, w)), pis(F(2, w))))
        th = r.choice([15, 22.5, 30, 60, 75, 67.5, 45, 105, 165])
        t = r.randint(0, 2)
        D = {30: ("1/2", "√3/2"), 45: ("√2/2", "√2/2"), 60: ("√3/2", "1/2"), 90: ("1", "0"), 120: ("√3/2", "－1/2"), 135: ("√2/2", "－√2/2"),
             150: ("1/2", "－√3/2"), 210: ("－1/2", "－√3/2"), 330: ("－1/2", "√3/2")}
        d2 = int(2 * th)
        if d2 not in D:
            return None
        ts = ("%g" % th)
        if t == 0:
            s2 = D[d2][0]
            v = s2 + "÷2"
            num = {"1/2": "1/4", "√3/2": "√3/4", "√2/2": "√2/4", "1": "1/2", "－1/2": "－1/4"}[s2]
            return mcq("计算：sin %s° cos %s° ＝ ？" % (ts, ts), H(num), [H(x) for x in ("1/4", "√3/4", "√2/4", "1/2", "√3/2", "√2/2") if x != num][:4],
                       "sin θ cos θ ＝ ½ sin 2θ ＝ ½ sin %d° ＝ <b>%s</b>。" % (d2, H(num)))
        c2 = D[d2][1]
        if t == 1:
            return mcq("计算：cos²%s° － sin²%s° ＝ ？" % (ts, ts), H(c2), [H(x) for x in ("1/2", "√3/2", "√2/2", "－1/2", "－√3/2", "0", "1") if x != c2][:4],
                       "cos²θ － sin²θ ＝ cos 2θ ＝ cos %d° ＝ <b>%s</b>。" % (d2, H(c2)))
        return mcq("计算：2cos²%s° － 1 ＝ ？" % ts, H(c2), [H(x) for x in ("1/2", "√3/2", "√2/2", "－1/2", "－√3/2", "0", "1") if x != c2][1:5],
                   "2cos²θ － 1 ＝ cos 2θ ＝ cos %d° ＝ <b>%s</b>。" % (d2, H(c2)))
    return mk


Un("trigonometric-identities", sort=8, dom="F", std=STD_T, seed=201108,
   title="三角恒等变换：两角和与差、二倍角和辅助角公式", short="三角恒等变换",
   meta="高中数学必修第一册“三角恒等变换”练习题：两角和与差的正弦、余弦公式，二倍角公式，两角和与差的正切公式，辅助角公式求最值，化简求值，100题在线练习，附可打印答案。",
   kb="sin(α ± β) ＝ sin α cos β ± cos α sin β", ks="cos(α ± β) ＝ cos α cos β ∓ sin α sin β；sin 2α ＝ 2 sin α cos α，cos 2α ＝ cos²α － sin²α。",
   body=L(["<b>两角和与差</b>：cos(α － β) ＝ cos α cos β ＋ sin α sin β，sin(α ＋ β) ＝ sin α cos β ＋ cos α sin β，tan(α ＋ β) ＝ (tan α ＋ tan β) ÷ (1 － tan α tan β)。",
           "<b>二倍角</b>：sin 2α ＝ 2 sin α cos α，cos 2α ＝ cos²α － sin²α ＝ 2cos²α － 1 ＝ 1 － 2sin²α。",
           "<b>辅助角公式</b>：a sin x ＋ b cos x ＝ √(a² ＋ b²) sin(x ＋ φ)，最大值是 √(a² ＋ b²)。"],
          [("sin 15° cos 15°", ["＝ ½ sin 30°"], "1/4"), ("sin x ＋ √3 cos x 的最大值", ["＝ 2 sin(x ＋ π/3)"], "2")],
          [("cos(α ＋ β) 中间用了加号", "cos(α ＋ β) ＝ cos α cos β － sin α sin β，中间是减号。"),
           ("求 cos α 时没判断符号", "先由 α 的范围判断 cos α 的正负。"),
           ("辅助角公式的最大值写成 a ＋ b", "最大值是 √(a² ＋ b²)，不是 a ＋ b。")]),
   faq=[("二倍角公式有哪些常用变形？", "降幂公式：cos²α ＝ (1 ＋ cos 2α)/2，sin²α ＝ (1 － cos 2α)/2。")],
   spec=lambda: [("两角和与差的正弦、余弦", [(trig2("sum"), 20)]), ("二倍角公式", [(trig2("double"), 20)]), ("两角和与差的正切", [(trig2("tan"), 20)]),
                 ("辅助角公式", [(trig2("aux"), 20)]), ("化简求值", [(trig2("simp"), -20), (trig2("sum"), None)])])


def trig3(kind):
    def mk():
        r = U.R
        A_ = r.choice([1, 2, 3, 4, -2]) if kind != "trans" else 1
        w = r.choice([F(1, 2), 1, 2, 3, 4])
        ph = r.choice([F(1, 6), F(1, 3), F(1, 4), F(-1, 6), F(-1, 3), F(-1, 4), F(1, 2), F(2, 3)])
        B = r.randint(-2, 3)
        wtxt = "" if w == 1 else ("x/2" if w == F(1, 2) else "%dx" % w)
        arg = ("%s" % ("x" if w == 1 else wtxt)) + (" ＋ " if ph > 0 else " － ") + pis(abs(ph))
        Atxt = "" if A_ == 1 else (M if A_ == -1 else S(A_))
        f = "y ＝ %ssin(%s)%s" % (Atxt, arg, ("" if B == 0 else (" ＋ %d" % B if B > 0 else " － %d" % -B)))
        if kind == "period":
            T = F(2) / F(w)
            if r.random() < 0.3:
                return mcq("函数 y ＝ tan(%s) 的最小正周期是多少？" % arg, pis(1 / F(w)), [pis(T), pis(F(w)), pis(F(1, 2) / F(w))],
                           "y ＝ tan(ωx ＋ φ) 的周期 T ＝ π/|ω| ＝ <b>%s</b>。" % pis(1 / F(w)))
            return mcq("函数 %s 的最小正周期是多少？" % f, pis(T), [pis(T / 2), pis(T * 2), pis(F(w)) if F(w) != T else pis(4 * T)],
                       "T ＝ 2π/|ω| ＝ 2π/%s ＝ <b>%s</b>。" % (S(w), pis(T)))
        if kind == "max":
            mx, mn = abs(A_) + B, -abs(A_) + B
            if r.random() < 0.5:
                return mcq("函数 %s 的最大值是多少？" % f, S(mx), [S(x) for x in (A_ + B if A_ + B != mx else mx + 1, mn, abs(A_), mx * 2 if mx else 1)],
                           "sin(…) 的最大值是 1，所以最大值是 |A| ＋ B ＝ %d ＋ %s ＝ <b>%s</b>。" % (abs(A_), P(B), S(mx)))
            return mcq("函数 %s 的最小值是多少？" % f, S(mn), [S(x) for x in (mx, -abs(A_), B - 1 if B - 1 != mn else B, mn - 1)],
                       "sin(…) 的最小值是 －1，所以最小值是 －|A| ＋ B ＝ <b>%s</b>。" % S(mn))
        if kind == "axis":
            # ωx ＋ φ ＝ π/2 ＋ kπ → x ＝ (1/2 ＋ k － φ)/ω
            k = r.randint(-1, 1)
            x0 = (F(1, 2) + k - ph) / F(w)
            bad = [(F(k) - ph) / F(w), (F(1, 2) + k + ph) / F(w), (F(1, 4) + k - ph) / F(w)]
            return mcq("下列直线中，哪一条是函数 %s 图象的对称轴？" % f, "x ＝ %s" % pis(x0), ["x ＝ %s" % pis(b) for b in bad if b != x0],
                       "对称轴满足 %s ＝ π/2 ＋ kπ，取 k ＝ %d，得 <b>x ＝ %s</b>。" % (arg, k, pis(x0)))
        if kind == "trans":
            s = r.choice([F(1, 3), F(1, 6), F(1, 4), F(1, 2), F(2, 3), F(1, 12), F(1, 8)])
            left = r.random() < 0.5
            wv = r.choice([2, 3, 4])
            sg = " ＋ " if left else " － "
            if r.random() < 0.5:
                ans = "y ＝ sin(%dx%s%s)" % (wv, sg, pis(s * wv))
                return mcq("把 y ＝ sin %dx 的图象向%s平移 %s 个单位，得到哪个函数的图象？" % (wv, "左" if left else "右", pis(s)), ans,
                           ["y ＝ sin(%dx%s%s)" % (wv, sg, pis(s)), "y ＝ sin(%dx%s%s)" % (wv, " － " if left else " ＋ ", pis(s * wv)), "y ＝ sin(%dx%s%s)" % (wv, sg, pis(s / wv))],
                           "x 换成 x %s %s：sin %d(x%s%s) ＝ <b>%s</b>。" % ("＋" if left else "－", pis(s), wv, sg, pis(s), ans[4:]))
            ans = "y ＝ sin(%dx%s%s)" % (wv, sg, pis(s))
            return mcq("把 y ＝ sin x 的图象向%s平移 %s 个单位，再把所有点的横坐标缩短到原来的 1/%d（纵坐标不变），得到哪个函数的图象？" % ("左" if left else "右", pis(s), wv), ans,
                       ["y ＝ sin(%dx%s%s)" % (wv, sg, pis(s * wv)), "y ＝ sin(%dx%s%s)" % (wv, " － " if left else " ＋ ", pis(s)), "y ＝ sin(%sx%s%s)" % (fr(1, wv), sg, pis(s))],
                       "平移后得 y ＝ sin(x%s%s)；横坐标缩短到 1/%d，x 换成 %dx：<b>%s</b>。" % (sg, pis(s), wv, wv, ans))
        # 値
        A2 = r.choice([1, 2, 3])
        wv = r.choice([1, 2])
        p2 = r.choice([F(1, 6), F(1, 3), F(-1, 6), F(1, 4)])
        x = r.choice([F(0), F(1, 6), F(1, 4), F(1, 3), F(1, 2), F(1, 12), F(5, 12)])
        ang = (wv * x + p2) * 180
        if ang % 30 and ang % 45:
            return None
        d = int(ang) % 360
        if d not in SPV and d != 0:
            return None
        sv = SPV.get(d, SPV[0])[0]
        vv = {"0": 0, "1/2": F(1, 2), "1": 1, "－1/2": F(-1, 2), "－1": -1}.get(sv)
        if vv is None:
            return None
        v = A2 * vv
        g = "f(x) ＝ %ssin(%s%s%s)" % ("" if A2 == 1 else A2, "x" if wv == 1 else "%dx" % wv, " ＋ " if p2 > 0 else " － ", pis(abs(p2)))
        return mcq("已知 %s，求 f(%s)。" % (g, pis(x)), S(v), [S(t) for t in (-v, A2, v + F(1, 2), F(A2, 2) if F(A2, 2) != v else -A2)],
                   "f(%s) ＝ %ssin %s ＝ <b>%s</b>。" % (pis(x), "" if A2 == 1 else A2, pis(F(d, 180)), S(v)))
    return mk


Un("graphs-of-trigonometric-functions", sort=9, dom="F", std=STD_T, seed=201109,
   title="三角函数的图象与性质：周期、最值、对称轴和图象变换", short="三角函数的图象与性质",
   meta="高中数学必修第一册“三角函数的图象与性质”练习题：y ＝ A sin(ωx ＋ φ) 的周期，最大值和最小值，对称轴，图象的平移和伸缩，求函数值，100题在线练习，附可打印答案。",
   kb="y ＝ A sin(ωx ＋ φ) 的周期 T ＝ 2π/|ω|", ks="最大值 |A|，最小值 －|A|；对称轴满足 ωx ＋ φ ＝ π/2 ＋ kπ，对称中心满足 ωx ＋ φ ＝ kπ。",
   body=L(["y ＝ A sin(ωx ＋ φ)（A ＞ 0，ω ＞ 0）：<b>振幅</b> A，<b>周期</b> T ＝ 2π/ω，<b>初相</b> φ。y ＝ tan x 的周期是 π。",
           "求单调区间、对称轴、最值时，把 ωx ＋ φ 看作一个整体 t，用 y ＝ sin t 的性质。",
           "<b>图象变换</b>：先平移再伸缩时，向左平移 φ 得 sin(x ＋ φ)，横坐标变为 1/ω 得 sin(ωx ＋ φ)；先伸缩再平移时，平移量是 φ/ω。"],
          [("y ＝ 2sin(2x ＋ π/6) 的周期和最大值", ["T ＝ 2π/2 ＝ π", "最大值 2"], "π，2"),
           ("y ＝ sin(2x ＋ π/6) 的一条对称轴", ["2x ＋ π/6 ＝ π/2", "x ＝ π/6"], "x ＝ π/6")],
          [("先伸缩再平移时平移量没除以 ω", "y ＝ sin 2x 向左平移 π/6 得 y ＝ sin 2(x ＋ π/6) ＝ sin(2x ＋ π/3)。"),
           ("周期写成 π/ω", "正弦、余弦的周期是 2π/ω，正切才是 π/ω。"),
           ("A 是负数时最大值写成 A", "最大值是 |A| 加上平移的常数。")]),
   faq=[("“五点法”怎么画图？", "令 ωx ＋ φ 分别等于 0、π/2、π、3π/2、2π，求出对应的 x 和 y，描点连线。")],
   spec=lambda: [("周期", [(trig3("period"), 20)]), ("最大值和最小值", [(trig3("max"), 20)]), ("对称轴", [(trig3("axis"), 20)]),
                 ("图象变换", [(trig3("trans"), 20)]), ("求函数值", [(trig3("value"), 20)])])


if __name__ == "__main__":
    import sys
    run_grade(G, UNITS, lambda r: U.setup(random.Random(r.random())), sys.argv[1:] or None)
