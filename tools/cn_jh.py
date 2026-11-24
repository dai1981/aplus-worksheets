# -*- coding: utf-8 -*-
"""
中国 初中（七〜九年级）の自前の問題：立方根、不等式组、分式、方差、旋转和中心对称、反比例函数、锐角三角函数、投影。
台湾版にない内容を補う。setup(R) してから使う。負の数は台湾版と同じ「－」。
"""
import math
import random
from fractions import Fraction as F
from ws_common import fr, svg_wrap, text, fig, INK, RED, BLUE
from tw_g7 import sn, par
from cn_common import mcq, Names

R = random.Random(0)
NM = Names(R)
M = "－"


def setup(rnd):
    global R, NM
    R = rnd
    NM = Names(rnd)


def fs(v):
    """Fraction → HTML（整数はそのまま、負は －）"""
    return sn(F(v))


def ch(kinds):
    return R.choice(kinds) if isinstance(kinds, (list, tuple)) else kinds


# ------------------------------------------------------------------ 实数：平方根・立方根（七年级下）
def roots(kinds=("sqrt", "arith", "cbrt", "est")):
    def mk():
        k = ch(kinds)
        if k == "sqrt":
            a = R.randint(2, 20)
            if R.random() < 0.3:
                b = R.choice([2, 3, 5, 7])
                if F(a, b).denominator == 1:
                    return None
                v = F(a, b)
                return mcq("%s 的平方根是什么？" % fs(v * v), "±%s" % fs(v), [fs(v), fs(v * v / 2) if (v * v) % 2 == 0 else fs(v + 1), "±%s" % fs(v * v / 4) if v * v != 4 else "±1"],
                           "因为（±%s）² ＝ %s，所以平方根是 <b>±%s</b>。正数有两个平方根，它们互为相反数。" % (fs(v), fs(v * v), fs(v)))
            return mcq("%d 的平方根是什么？" % (a * a), "±%d" % a, [str(a), "%s%d" % (M, a), "±%d" % (a * a // 2 if a * a % 2 == 0 else a + 1)],
                       "因为（±%d）² ＝ %d，所以 %d 的平方根是 <b>±%d</b>。" % (a, a * a, a * a, a))
        if k == "arith":
            a = R.randint(2, 25)
            n = a * a
            return mcq("%d 的算术平方根是什么？" % n, str(a), ["±%d" % a, "%s%d" % (M, a), str(n // 2)],
                       "正数的正的平方根叫算术平方根：√%d ＝ <b>%d</b>。" % (n, a))
        if k == "cbrt" and R.random() < 0.35:
            a = F(R.choice([1, 2, 3, 4, -1, -2, -3]), R.choice([2, 3, 4, 5, 10]))
            if a.denominator == 1:
                return None
            n = a ** 3
            if a.denominator == 10:
                return mcq("%s 的立方根是什么？" % ("%g" % float(n)).replace("-", M), ("%g" % float(a)).replace("-", M), [("%g" % float(-a)).replace("-", M), "±%g" % abs(float(a)), ("%g" % (float(a) * 10)).replace("-", M)],
                           "因为（%s）³ ＝ %s，所以立方根是 <b>%s</b>。" % (("%g" % float(a)).replace("-", M), ("%g" % float(n)).replace("-", M), ("%g" % float(a)).replace("-", M)))
            return mcq("%s 的立方根是什么？" % fs(n), fs(a), [fs(-a), "±%s" % fs(abs(a)), fs(n * 3) if n * 3 != a else fs(a * a)],
                       "因为（%s）³ ＝ %s，所以立方根是 <b>%s</b>。" % (fs(a), fs(n), fs(a)))
        if k == "cbrt":
            a = R.choice([x for x in range(-10, 11) if x not in (0, 1, -1)])
            n = a ** 3
            return mcq("%s 的立方根是什么？" % sn(n), sn(a), [sn(-a), "±%d" % abs(a), sn(n // 3 if n % 3 == 0 else a * a)],
                       "因为（%s）³ ＝ %s，所以 ∛%s ＝ <b>%s</b>。负数的立方根是负数，一个数只有一个立方根。" % (sn(a), sn(n), par(n), sn(a)))
        n = R.randint(2, 150)
        r = int(math.isqrt(n))
        if r * r == n:
            return None
        return mcq("√%d 在哪两个相邻的整数之间？" % n, "%d 和 %d 之间" % (r, r + 1),
                   ["%d 和 %d 之间" % (r - 1, r) if r > 1 else "%d 和 %d 之间" % (r + 2, r + 3), "%d 和 %d 之间" % (r + 1, r + 2), "%d 和 %d 之间" % (n // 2, n // 2 + 1) if n // 2 not in (r, r + 1, r - 1) else "%d 和 %d 之间" % (r + 3, r + 4)],
                   "%d² ＝ %d，%d² ＝ %d，%d ＜ %d ＜ %d，所以 %d ＜ √%d ＜ %d，答案是<b>%d 和 %d 之间</b>。" % (r, r * r, r + 1, (r + 1) ** 2, r * r, n, (r + 1) ** 2, r, n, r + 1, r, r + 1))
    return mk


# ------------------------------------------------------------------ 不等式组（七年级下）
def _ineq(a, b, c, op):
    """ax + b op c の式と解（x op' t）"""
    t = F(c - b, a)
    if t.denominator != 1:
        return None
    flip = a < 0
    o = {"＞": "＜", "≥": "≤"}.get(op, "＞") if flip else op
    if flip:
        o = {"＞": "＜", "≥": "≤", "＜": "＞", "≤": "≥"}[op]
    lhs = ("%sx" % ("" if a == 1 else (M if a == -1 else sn(a)))) + (" ＋ %d" % b if b > 0 else (" %s %d" % (M, -b) if b < 0 else ""))
    return "%s %s %s" % (lhs, op, sn(c)), o, int(t)


def ineq_sys(kinds=("solve", "int", "count", "none")):
    def mk():
        k = ch(kinds)
        lo = R.randint(-5, 3)
        hi = lo + R.randint(2, 6)
        a1 = R.choice([1, 2, 3, -1, -2])
        b1 = R.randint(-6, 6)
        a2 = R.choice([1, 2, 3, -1])
        b2 = R.randint(-6, 6)
        incl1, incl2 = R.random() < 0.5, R.random() < 0.5
        if k == "none":
            lo, hi = hi, lo
        # 1 本目：x > lo（≥）、2 本目：x < hi（≤）になるように作る
        op1 = "≥" if incl1 else "＞"
        op2 = "≤" if incl2 else "＜"
        if a1 < 0:
            op1 = {"≥": "≤", "＞": "＜"}[op1]
        if a2 < 0:
            op2 = {"≤": "≥", "＜": "＞"}[op2]
        e1 = _ineq(a1, b1, a1 * lo + b1, op1)
        e2 = _ineq(a2, b2, a2 * hi + b2, op2)
        if not e1 or not e2:
            return None
        s1, o1, t1 = e1
        s2, o2, t2 = e2
        L = "%s %s x" % (sn(lo), "≤" if incl1 else "＜")
        Rr = "x %s %s" % ("≤" if incl2 else "＜", sn(hi))
        sysh = "<span class='sys'>%s<br>%s</span>" % (s1, s2)
        if k == "none":
            ok = "无解"
            return mcq("解不等式组 %s" % sysh, ok, ["%s %s x %s %s" % (sn(hi), "≤" if incl1 else "＜", "≤" if incl2 else "＜", sn(lo)), "x %s %s" % ("≥" if incl1 else "＞", sn(lo)), "x %s %s" % ("≤" if incl2 else "＜", sn(hi))],
                       "第一个不等式得 x %s %s，第二个得 x %s %s。大大小小找不到（没有公共部分），所以<b>无解</b>。" % ("≥" if incl1 else "＞", sn(lo), "≤" if incl2 else "＜", sn(hi)))
        ok = "%s %s x %s %s" % (sn(lo), "≤" if incl1 else "＜", "≤" if incl2 else "＜", sn(hi))
        ints = [x for x in range(lo, hi + 1) if (x > lo or incl1) and (x < hi or incl2)]
        if k == "solve":
            return mcq("解不等式组 %s" % sysh, ok, ["%s %s x %s %s" % (sn(lo), "＜" if incl1 else "≤", "＜" if incl2 else "≤", sn(hi)), "x %s %s" % ("≥" if incl1 else "＞", sn(lo)), "无解", "%s %s x %s %s" % (sn(-hi), "≤" if incl1 else "＜", "≤" if incl2 else "＜", sn(-lo))],
                       "分别解两个不等式：x %s %s，x %s %s。取公共部分，<b>%s</b>。注意系数是负数时，不等号方向要改变。" % ("≥" if incl1 else "＞", sn(lo), "≤" if incl2 else "＜", sn(hi), ok))
        if k == "count":
            n = len(ints)
            return mcq("不等式组 %s 的整数解有几个？" % sysh, "%d 个" % n, ["%d 个" % x for x in (n + 1, n - 1 if n > 1 else n + 2, hi - lo + 1 if hi - lo + 1 != n else n + 3)],
                       "解集是 %s，整数解是 %s，共 <b>%d 个</b>。" % (ok, "、".join(sn(x) for x in ints), n))
        if not ints:
            return None
        return mcq("不等式组 %s 的最小整数解是多少？" % sysh, sn(ints[0]), [sn(x) for x in (ints[0] - 1, ints[-1], lo if lo != ints[0] else lo + 1, ints[0] + 1)],
                   "解集是 %s，最小的整数解是 <b>%s</b>。" % (ok, sn(ints[0])))
    return mk


def ineq_word():
    def mk():
        n = NM.next()
        k = R.randint(0, 2)
        if k == 0:
            total = R.choice([100, 120, 150, 200])
            p1, p2 = R.choice([(5, 8), (6, 10), (4, 7), (3, 5)])
            m = R.randint(12, 25)
            # 买 m 件，单价 p1 或 p2，费用不超过 total，最多买几件贵的
            if p1 * m > total:
                return None
            x = (total - p1 * m) // (p2 - p1)
            if x < 1 or x >= m:
                return None
            return mcq("%s用不超过 %d 元买笔记本和笔共 %d 件，笔记本每本 %d 元，笔每支 %d 元。笔记本最多买几本？" % (n, total, m, p2, p1), "%d 本" % x,
                       ["%d 本" % v for v in (x + 1, total // p2, x - 1 if x > 1 else x + 2, m - x)],
                       "设买笔记本 x 本，%dx ＋ %d(%d － x) ≤ %d，解得 x ≤ %s，所以最多买 <b>%d 本</b>。" % (p2, p1, m, total, fs(F(total - p1 * m, p2 - p1)), x))
        if k == 1:
            q = R.randint(10, 25)
            right, wrong = 5, R.choice([1, 2])
            need = R.choice([60, 70, 75, 80])
            x = -(-(need + wrong * q) // (right + wrong))
            if x > q:
                return None
            return mcq("知识竞赛有 %d 道题，答对一题得 %d 分，答错或不答扣 %d 分。要得分不少于 %d 分，至少要答对几道？" % (q, right, wrong, need), "%d 道" % x,
                       ["%d 道" % v for v in (x - 1, x + 1, -(-need // right), q - x) if v > 0],
                       "设答对 x 道，%dx － %d(%d － x) ≥ %d，%dx ≥ %d，x ≥ %s，至少答对 <b>%d 道</b>。" % (right, wrong, q, need, right + wrong, need + wrong * q, fs(F(need + wrong * q, right + wrong)), x))
        a = R.randint(2, 6)
        b = R.randint(1, 15)
        c = R.randint(20, 60)
        x = (c - b) // a if (c - b) % a else (c - b) // a - 1
        if x < 1:
            return None
        return mcq("一个数的 %d 倍加上 %d 小于 %d，这个数最大是几（整数）？" % (a, b, c), str(x), [str(v) for v in (x + 1, x - 1, (c + b) // a, c // a) if v != x],
                   "%dx ＋ %d ＜ %d，x ＜ %s，最大的整数是 <b>%d</b>。" % (a, b, c, fs(F(c - b, a)), x))
    return mk


# ------------------------------------------------------------------ 分式（八年级上）
def _lin(a, b, v="x"):
    s = ("%s%s" % ("" if a == 1 else (M if a == -1 else str(a)), v)) if a else ""
    if b:
        s += (" ＋ %d" % b if b > 0 else " %s %d" % (M, -b)) if s else sn(b)
    return s or "0"


def fraction_alg(kinds=("mean", "zero", "simp", "addsub", "muldiv", "eq", "word")):
    def mk():
        k = ch(kinds)
        if k == "mean":
            a, b = R.randint(-9, 9), R.randint(1, 3)
            if a == 0:
                return None
            num = _lin(1, R.randint(-5, 5) or 1)
            den = _lin(b, -a * b)
            return mcq("当 x 满足什么条件时，分式 %s 有意义？" % fr(num, den), "x ≠ %s" % sn(a), ["x ≠ %s" % sn(-a), "x ＝ %s" % sn(a), "x ≠ 0"],
                       "分式有意义，分母不能为 0：%s ≠ 0，所以 <b>x ≠ %s</b>。" % (den, sn(a)))
        if k == "zero":
            a = R.randint(-8, 8)
            b = R.randint(-8, 8)
            if a == b or a == 0:
                return None
            return mcq("分式 %s 的值为 0，x 等于多少？" % fr(_lin(1, -a), _lin(1, -b)), sn(a), [sn(b), sn(-a), "0"],
                       "分子为 0 且分母不为 0：x － %s ＝ 0 得 x ＝ %s，此时分母 %s ≠ 0。所以 <b>x ＝ %s</b>。" % (par(a), sn(a), sn(a - b), sn(a)))
        if k == "simp":
            t = R.randint(0, 2)
            if t == 0:
                a = R.randint(1, 9)
                return mcq("约分：%s ＝ ？" % fr("x² － %d" % (a * a), "x ＋ %d" % a), "x － %d" % a, ["x ＋ %d" % a, "x － %d" % (a * a), fr("1", "x ＋ %d" % a)],
                           "分子用平方差公式分解：x² － %d ＝ (x ＋ %d)(x － %d)，约去 x ＋ %d，得 <b>x － %d</b>。" % (a * a, a, a, a, a))
            if t == 1:
                p, q = R.randint(2, 6), R.randint(2, 6)
                g = math.gcd(p, q)
                return mcq("约分：%s ＝ ？" % fr("%da²b" % (p * 2), "%dab²" % (q * 2)), fr("%sa" % ("" if p // g == 1 else p // g), "%sb" % ("" if q // g == 1 else q // g)),
                           [fr("%sa²" % ("" if p // g == 1 else p // g), "%sb²" % ("" if q // g == 1 else q // g)), fr("a", "b"), fr("%da" % (p * 2), "%db" % (q * 2))],
                           "分子分母同时除以公因式 %dab，得 <b>%s</b>。" % (2 * g, fr("%sa" % ("" if p // g == 1 else p // g), "%sb" % ("" if q // g == 1 else q // g))))
            a = R.randint(1, 8)
            return mcq("约分：%s ＝ ？" % fr("x² ＋ %dx ＋ %d" % (2 * a, a * a), "x² － %d" % (a * a)), fr("x ＋ %d" % a, "x － %d" % a),
                       [fr("x － %d" % a, "x ＋ %d" % a), "x ＋ %d" % a, fr("%dx ＋ %d" % (2 * a, a * a), "－%d" % (a * a))],
                       "分子 ＝ (x ＋ %d)²，分母 ＝ (x ＋ %d)(x － %d)，约去 x ＋ %d，得 <b>%s</b>。" % (a, a, a, a, fr("x ＋ %d" % a, "x － %d" % a)))
        if k == "addsub":
            t = R.randint(0, 2)
            if t == 0:
                p, q = R.randint(1, 9), R.randint(1, 9)
                return mcq("计算：%s ＋ %s ＝ ？" % (fr(p, "x"), fr(q, "x")), fr(p + q, "x"), [fr(p + q, "2x"), fr(p * q, "x"), fr(p + q, "x²")],
                           "同分母分式相加，分母不变，分子相加：<b>%s</b>。" % fr(p + q, "x"))
            if t == 1:
                return mcq("计算：%s － %s ＝ ？" % (fr("a", "a － b"), fr("b", "a － b")), "1", ["0", fr("a ＋ b", "a － b"), "a － b"],
                           "分子相减：a － b，与分母相同，结果是 <b>1</b>。")
            p, q = R.randint(1, 5), R.randint(1, 5)
            if p == q:
                return None
            return mcq("计算：%s ＋ %s ＝ ？" % (fr(p, "x"), fr(q, "2x")), fr(2 * p + q, "2x"), [fr(p + q, "3x"), fr(p + q, "2x"), fr(p + q, "x")],
                       "通分，最简公分母是 2x：%s ＋ %s ＝ <b>%s</b>。" % (fr(2 * p, "2x"), fr(q, "2x"), fr(2 * p + q, "2x")))
        if k == "muldiv":
            p, q = R.randint(2, 9), R.randint(2, 9)
            if R.random() < 0.5:
                return mcq("计算：%s · %s ＝ ？" % (fr("%dx" % p, "y"), fr("y²", "%dx²" % q)), fr("%sy" % ("" if p // math.gcd(p, q) == 1 else p // math.gcd(p, q)), "%sx" % ("" if q // math.gcd(p, q) == 1 else q // math.gcd(p, q))),
                           [fr("%dy²" % p, "%dx²" % q), fr("y", "x"), fr("%dxy" % p, "%d" % q)],
                           "分子乘分子、分母乘分母，再约分：<b>%s</b>。" % fr("%sy" % ("" if p // math.gcd(p, q) == 1 else p // math.gcd(p, q)), "%sx" % ("" if q // math.gcd(p, q) == 1 else q // math.gcd(p, q))))
            a = R.randint(1, 6)
            return mcq("计算：%s ÷ %s ＝ ？" % (fr("x ＋ %d" % a, "x"), fr("x ＋ %d" % a, "x²")), "x", ["1", fr("1", "x"), "x²"],
                       "除以一个分式，等于乘它的倒数：%s · %s ＝ <b>x</b>。" % (fr("x ＋ %d" % a, "x"), fr("x²", "x ＋ %d" % a)))
        if k == "eq":
            x = R.randint(1, 12)
            if R.random() < 0.5:
                a = R.choice([v for v in range(-6, 9) if v and x + v != 0])
                d = R.randint(1, 9)
                if (d * (x + a)) % x:
                    return None
                c = d * (x + a) // x
                if c <= 0 or c == d:
                    return None
                den = _lin(1, a)
                return mcq("解分式方程：%s ＝ %s，x ＝ ？" % (fr(c, den), fr(d, "x")), str(x), [sn(v) for v in (x + a, -x, x + 1, a) if v != x],
                           "两边同乘最简公分母 x(%s)：%dx ＝ %d(%s)，解得 x ＝ %d。检验：x(%s) ≠ 0，所以 <b>x ＝ %d</b>。" % (den, c, d, den, x, den, x))
            p_ = R.randint(1, 9)
            q = R.randint(2, 5)
            if x == p_:
                return None
            m = q * (x - p_) - x
            num = _lin(1, m)
            den = _lin(1, -p_)
            return mcq("解分式方程：%s ＝ %d，x ＝ ？" % (fr(num, den), q), str(x), [sn(v) for v in (p_, x + 1, -x, q * x) if v != x],
                       "两边同乘 %s：%s ＝ %d(%s)，解得 x ＝ %d。检验：%s ≠ 0，所以 <b>x ＝ %d</b>。" % (den, num, q, den, x, sn(x - p_), x))
        # word：工程・行程
        t = R.randint(0, 1)
        if t == 0:
            v = R.choice([30, 40, 50, 60, 70, 80, 90, 100])
            dv = R.choice([10, 15, 20, 30])
            d1 = v * R.choice([2, 3, 4, 5])
            d2 = (v + dv) * (d1 // v)
            return mcq("甲车行驶 %d 千米和乙车行驶 %d 千米所用的时间相同，乙车每小时比甲车多行 %d 千米。甲车的速度是多少？" % (d1, d2, dv), "%d 千米/时" % v,
                       ["%d 千米/时" % x for x in (v + dv, v - dv, d1 // 2, (d1 + d2) // 4) if x != v],
                       "设甲车速度为 x 千米/时，%s ＝ %s，解得 x ＝ %d，经检验符合题意。<b>%d 千米/时</b>" % (fr(d1, "x"), fr(d2, "x ＋ %d" % dv), v, v))
        if R.random() < 0.4:
            p = R.choice([2, 3, 4, 5, 6, 8, 10])
            n1 = R.choice([60, 80, 100, 120, 150, 180, 200, 240, 300])
            n2 = n1 * R.choice([2, 3])
            if (n2 - n1) % p:
                pass
            # 甲每小时比乙多做 p 个，甲做 n2 个和乙做 n1 个用时相同
            # n2/(x+p) = n1/x → x = n1 p/(n2 - n1)
            xx = F(n1 * p, n2 - n1)
            if xx.denominator != 1:
                return None
            return mcq("甲每小时比乙多做 %d 个零件，甲做 %d 个零件与乙做 %d 个零件所用的时间相同。乙每小时做多少个？" % (p, n2, n1), "%d 个" % xx,
                       ["%d 个" % v for v in (xx + p, xx * 2, n1 // p, xx + 1) if v != xx],
                       "设乙每小时做 x 个，%s ＝ %s，解得 x ＝ %d，经检验符合题意。<b>%d 个</b>" % (fr(n2, "x ＋ %d" % p), fr(n1, "x"), xx, xx))
        a = R.choice([4, 6, 8, 10, 12, 15, 20, 24, 30])
        b = R.choice([x for x in (6, 10, 12, 15, 20, 24, 30, 40, 60) if x != a])
        t = F(a * b, a + b)
        if t.denominator != 1:
            return None
        return mcq("一项工程，甲队单独做 %d 天完成，乙队单独做 %d 天完成。两队合做几天完成？" % (a, b), "%d 天" % t,
                   ["%d 天" % x for x in ((a + b) // 2, a + b, abs(a - b), t + 1) if x != t and x > 0],
                   "把工作总量看作 1，合做的工作效率是 %s ＋ %s ＝ %s，所以需要 1 ÷ %s ＝ <b>%d 天</b>。" % (fr(1, a), fr(1, b), fs(F(1, a) + F(1, b)), fs(F(1, a) + F(1, b)), t))
    return mk


# ------------------------------------------------------------------ 数据的分析：加权平均数・方差（八年级下）
def variance(kinds=("wmean", "var", "stable", "change")):
    def mk():
        k = ch(kinds)
        if k == "wmean":
            sc = [R.randint(70, 98) for _ in range(3)]
            w = R.choice([(2, 3, 5), (3, 3, 4), (1, 2, 2), (4, 3, 3), (2, 2, 1)])
            tot = sum(s * x for s, x in zip(sc, w))
            m = F(tot, sum(w))
            if m.denominator not in (1, 2, 5, 10):
                return None
            ok = ("%.1f" % float(m)).rstrip("0").rstrip(".")
            simple = F(sum(sc), 3)
            return mcq("某同学笔试 %d 分、面试 %d 分、实践 %d 分，三项按 %d ∶ %d ∶ %d 计算总成绩。他的总成绩是多少分？" % (sc[0], sc[1], sc[2], w[0], w[1], w[2]), "%s 分" % ok,
                       ["%s 分" % ("%.1f" % float(simple)).rstrip("0").rstrip("."), "%d 分" % tot, "%d 分" % max(sc), "%s 分" % ("%.1f" % float(m + 1)).rstrip("0").rstrip(".")],
                       "加权平均数：(%d × %d ＋ %d × %d ＋ %d × %d) ÷ (%d ＋ %d ＋ %d) ＝ <b>%s 分</b>。" % (sc[0], w[0], sc[1], w[1], sc[2], w[2], w[0], w[1], w[2], ok))
        if k == "var":
            m = R.randint(3, 12)
            devs = R.choice([(-2, -1, 0, 1, 2), (-3, -1, 0, 1, 3), (-2, 0, 0, 0, 2), (-4, -1, 1, 2, 2), (-3, -3, 1, 2, 3), (-1, -1, 0, 1, 1)])
            if sum(devs) != 0:
                return None
            data = sorted(m + d for d in devs)
            v = F(sum(d * d for d in devs), 5)
            ok = fs(v) if v.denominator == 1 else ("%.1f" % float(v)).rstrip("0")
            return mcq("一组数据 %s 的方差是多少？" % "，".join(map(str, data)), ok,
                       [("%.1f" % float(F(sum(d * d for d in devs), 4))).rstrip("0").rstrip("."), str(sum(d * d for d in devs)), str(m), ("%.1f" % float(math.sqrt(v))).rstrip("0").rstrip(".") if v != 1 else "2"],
                       "平均数是 %d，方差 ＝ [%s] ÷ 5 ＝ <b>%s</b>。" % (m, " ＋ ".join("(%d － %d)²" % (x, m) for x in data), ok))
        if k == "stable":
            a, b = NM.next(), NM.next()
            if a == b:
                return None
            va, vb = R.sample([0.8, 1.2, 1.5, 2.1, 2.6, 3.4, 4.2, 0.6], 2)
            m = R.randint(80, 92)
            win = a if va < vb else b
            return mcq("%s和%s各射击 10 次，平均成绩都是 %d 环，方差分别是 %s 和 %s。谁的成绩更稳定？" % (a, b, m, va, vb), win,
                       [b if win == a else a, "一样稳定", "无法判断"],
                       "平均数相同时，方差越小，数据越稳定。%s 的方差更小，所以 <b>%s</b> 更稳定。" % ("%.1f" % min(va, vb), win))
        m = R.randint(5, 15)
        v = R.randint(2, 9)
        c = R.randint(2, 10)
        t = R.randint(0, 1)
        if t == 0:
            return mcq("一组数据的平均数是 %d，方差是 %d。每个数都加上 %d，新数据的平均数和方差分别是多少？" % (m, v, c), "%d，%d" % (m + c, v),
                       ["%d，%d" % (m + c, v + c), "%d，%d" % (m, v), "%d，%d" % (m, v + c)],
                       "每个数都加上同一个数，平均数也加上这个数，波动不变，方差不变：<b>%d，%d</b>。" % (m + c, v))
        c = R.randint(2, 4)
        return mcq("一组数据的平均数是 %d，方差是 %d。每个数都乘 %d，新数据的平均数和方差分别是多少？" % (m, v, c), "%d，%d" % (m * c, v * c * c),
                   ["%d，%d" % (m * c, v * c), "%d，%d" % (m, v * c * c), "%d，%d" % (m * c, v)],
                   "每个数都乘 %d，平均数乘 %d，方差乘 %d² ＝ %d：<b>%d，%d</b>。" % (c, c, c, c * c, m * c, v * c * c))
    return mk


# ------------------------------------------------------------------ 旋转和中心对称（九年级上）
SHAPES = [("线段", True, True), ("等边三角形", False, True), ("平行四边形", True, False), ("矩形", True, True), ("菱形", True, True),
          ("正方形", True, True), ("等腰梯形", False, True), ("正五边形", False, True), ("正六边形", True, True), ("圆", True, True),
          ("等腰三角形", False, True), ("直角三角形", False, False), ("正八边形", True, True)]


def rotation(kinds=("point", "central", "shape", "angle", "both")):
    def mk():
        k = ch(kinds)
        if k in ("point", "central"):
            a, b = R.randint(-7, 7), R.randint(-7, 7)
            if a == 0 or b == 0 or abs(a) == abs(b):
                return None
            P = "P(%s, %s)" % (sn(a), sn(b))
            if k == "central":
                return mcq("点 %s 关于原点对称的点的坐标是什么？" % P, "(%s, %s)" % (sn(-a), sn(-b)),
                           ["(%s, %s)" % (sn(-a), sn(b)), "(%s, %s)" % (sn(a), sn(-b)), "(%s, %s)" % (sn(b), sn(a))],
                           "关于原点对称的两个点，横坐标、纵坐标都互为相反数：<b>(%s, %s)</b>。" % (sn(-a), sn(-b)))
            cw = R.random() < 0.5
            ans = (b, -a) if cw else (-b, a)
            return mcq("把点 %s 绕原点%s旋转 90°，得到的点的坐标是什么？" % (P, "顺时针" if cw else "逆时针"), "(%s, %s)" % tuple(map(sn, ans)),
                       ["(%s, %s)" % tuple(map(sn, (-ans[0], -ans[1]))), "(%s, %s)" % tuple(map(sn, (-a, -b))), "(%s, %s)" % tuple(map(sn, (b, a)))],
                       "%s旋转 90°：(x, y) → %s。所以是 <b>(%s, %s)</b>。" % ("顺时针" if cw else "逆时针", "(y, －x)" if cw else "(－y, x)", sn(ans[0]), sn(ans[1])))
        if k == "shape":
            yes = [s_ for s_ in SHAPES if s_[1]]
            no = [s_ for s_ in SHAPES if not s_[1]]
            if R.random() < 0.5:
                c = R.choice(yes)
                w = R.sample(no, 3)
                opts = [c[0]] + [x[0] for x in w]
                R.shuffle(opts)
                return mcq("在%s中，哪一个是中心对称图形？" % "、".join(opts), c[0], [x[0] for x in w],
                           "绕某一点旋转 180° 后能和原来的图形重合的图形是中心对称图形。<b>%s</b>是中心对称图形。" % c[0])
            c = R.choice(no)
            w = R.sample(yes, 3)
            opts = [c[0]] + [x[0] for x in w]
            R.shuffle(opts)
            return mcq("在%s中，哪一个<b>不是</b>中心对称图形？" % "、".join(opts), c[0], [x[0] for x in w],
                       "%s绕任何一点旋转 180° 都不能和自身重合，所以<b>不是</b>中心对称图形。" % c[0])
        if k == "angle":
            n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
            nm = {3: "等边三角形", 4: "正方形", 12: "正十二边形"}.get(n) or "正%s边形" % "零一二三四五六七八九十"[n]
            ok = 360 // n
            if R.random() < 0.3:
                return mcq("%s绕它的中心至少旋转多少度，才能和原来的图形重合？" % nm, "%d°" % ok, ["%d°" % x for x in (180, 360, (n - 2) * 180 // n, ok * 2) if x != ok],
                           "%d 条边均匀分布，360° ÷ %d ＝ <b>%d°</b>。" % (n, n, ok))
            t = R.choice(range(30, 360, 15))
            yes = t % ok == 0
            a = "能" if yes else "不能"
            return mcq("%s绕它的中心旋转 %d°，能和原来的图形重合吗？" % (nm, t), a, ["不能" if yes else "能", "只有旋转 360° 才能", "无法判断"],
                       "%s绕中心每旋转 %d° 就和自身重合一次。%d° %s %d° 的倍数，所以<b>%s</b>。" % (nm, ok, t, "是" if yes else "不是", ok, a))
        c = R.choice([s_ for s_ in SHAPES if s_[1] and s_[2]])
        w = R.sample([s_[0] for s_ in SHAPES if not (s_[1] and s_[2])], 3)
        opts = [c[0]] + w
        R.shuffle(opts)
        return mcq("在%s中，既是轴对称图形又是中心对称图形的是哪一个？" % "、".join(opts), c[0], w,
                   "<b>%s</b>既能沿直线对折重合，又能绕中心旋转 180° 重合。" % c[0])
    return mk


# ------------------------------------------------------------------ 反比例函数（九年级下）
def inverse_fn(kinds=("k", "value", "quad", "trend", "word")):
    def mk():
        k = ch(kinds)
        kk = R.choice([x for x in range(-12, 13) if x not in (0, 1, -1)])
        f = "y ＝ %s" % fr(sn(kk), "x")
        if k == "k":
            xs = [d for d in range(-12, 13) if d and kk % d == 0 and abs(d) != 1]
            x = R.choice(xs)
            y = kk // x
            return mcq("反比例函数 y ＝ %s 的图象经过点 (%s, %s)，k 等于多少？" % (fr("k", "x"), sn(x), sn(y)), sn(kk), [sn(-kk), sn(x + y), fs(F(y, x)) if y % x else sn(y - x)],
                       "把点代入：k ＝ xy ＝ %s × %s ＝ <b>%s</b>。" % (sn(x), par(y), sn(kk)))
        if k == "value":
            xs = [d for d in range(-12, 13) if d and kk % d == 0]
            x = R.choice(xs)
            return mcq("对于反比例函数 %s，当 x ＝ %s 时，y 等于多少？" % (f, sn(x)), sn(kk // x), [sn(-kk // x), sn(kk * x), sn(kk - x) if kk - x != kk // x else sn(kk + x)],
                       "y ＝ %s ÷ %s ＝ <b>%s</b>。" % (sn(kk), par(x), sn(kk // x)))
        if k == "quad":
            ok = "第一、三象限" if kk > 0 else "第二、四象限"
            return mcq("反比例函数 %s 的图象在哪两个象限？" % f, ok, ["第二、四象限" if kk > 0 else "第一、三象限", "第一、二象限", "第三、四象限"],
                       "k ＝ %s %s 0，图象在<b>%s</b>。" % (sn(kk), "＞" if kk > 0 else "＜", ok))
        if k == "trend":
            ok = "y 随 x 的增大而减小" if kk > 0 else "y 随 x 的增大而增大"
            return mcq("反比例函数 %s，在每个象限内，y 怎样变化？" % f, ok, ["y 随 x 的增大而增大" if kk > 0 else "y 随 x 的增大而减小", "y 不变", "先增大后减小"],
                       "k %s 0 时，在每个象限内<b>%s</b>。" % ("＞" if kk > 0 else "＜", ok))
        t = R.randint(0, 2)
        if t == 0:
            s = R.choice([60, 80, 90, 120, 180, 240])
            v = R.choice([d for d in (20, 30, 40, 45, 60, 80) if s % d == 0])
            return mcq("A、B 两地相距 %d 千米，汽车从 A 地开到 B 地。速度 v（千米/时）与时间 t（小时）的关系式是什么？当 v ＝ %d 时，t 是多少？" % (s, v), "v ＝ %s，t ＝ %d" % (fr(s, "t"), s // v),
                       ["v ＝ %dt，t ＝ %d" % (s, s // v), "v ＝ %s，t ＝ %d" % (fr("t", s), s // v + 1), "v ＝ %s，t ＝ %d" % (fr(s, "t"), s // v + 1)],
                       "路程一定，vt ＝ %d，v ＝ %s，t ＝ %d ÷ %d ＝ <b>%d</b>。" % (s, fr(s, "t"), s, v, s // v))
        if t == 1:
            S = R.choice([12, 18, 24, 36, 48])
            x = R.choice([d for d in range(2, 13) if S % d == 0])
            return mcq("面积是 %d 平方厘米的矩形，长 y 厘米和宽 x 厘米成反比例。当宽为 %d 厘米时，长是多少厘米？" % (S, x), "%d 厘米" % (S // x),
                       ["%d 厘米" % v for v in (S * x, S - x, S // 2, S // x + 1) if v != S // x],
                       "xy ＝ %d，y ＝ %d ÷ %d ＝ <b>%d 厘米</b>。" % (S, S, x, S // x))
        P = R.choice([600, 800, 1200, 1500, 2400])
        V = R.choice([d for d in (20, 30, 40, 50, 60, 80, 100, 120, 150) if P % d == 0])
        return mcq("一定质量的气体，体积 V 和密度 ρ 满足 ρV ＝ %d。当 V ＝ %d 时，ρ 等于多少？" % (P, V), str(P // V),
                   [str(x) for x in (P * V, P - V, P // V + 2, P // (2 * V) if P % (2 * V) == 0 else P // V - 1) if x != P // V and x > 0],
                "ρ ＝ %d ÷ %d ＝ <b>%d</b>。" % (P, V, P // V))
    return mk


# ------------------------------------------------------------------ 锐角三角函数（九年级下）
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29)]
SP = {30: ("1/2", "√3/2", "√3/3"), 45: ("√2/2", "√2/2", "1"), 60: ("√3/2", "1/2", "√3")}


def _rt_svg(a, b, c):
    """直角三角形 ABC（∠C ＝ 90°）。BC ＝ a（A の対辺）、AC ＝ b"""
    s = 200.0 / max(a, b)
    W, H = 60 + b * s, 50 + a * s
    Cx, Cy = 30, 20 + a * s
    Ax, Ay = 30 + b * s, Cy
    Bx, By = 30, 20
    t = ["<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (Ax, Ay, Bx, By, Cx, Cy, INK),
         "<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s'/>" % (Cx, Cy - 12, Cx + 12, Cy - 12, Cx + 12, Cy, INK),
         text(Ax + 10, Ay + 6, "A", 14), text(Bx - 12, By + 4, "B", 14), text(Cx - 12, Cy + 12, "C", 14),
         text(Cx - 16, (By + Cy) / 2 + 4, str(a), 13, col=BLUE), text((Cx + Ax) / 2, Cy + 18, str(b), 13, col=BLUE),
         text((Ax + Bx) / 2 + 14, (Ay + By) / 2 - 4, str(c), 13, col=BLUE)]
    return fig(svg_wrap(W, H + 6, "".join(t), "直角三角形 ABC"))


def trig(kinds=("ratio", "special", "solve", "height")):
    FN = {"sin": "正弦", "cos": "余弦", "tan": "正切"}

    def mk():
        k = ch(kinds)
        if k == "ratio":
            a, b, c = R.choice(TRIPLES)
            if R.random() < 0.5:
                a, b = b, a
            fn = R.choice(["sin", "cos", "tan"])
            ang = R.choice(["A", "B"])
            opp, adj = (a, b) if ang == "A" else (b, a)
            val = {"sin": (opp, c), "cos": (adj, c), "tan": (opp, adj)}[fn]
            g = math.gcd(*val)
            ok = fr(val[0] // g, val[1] // g)
            cands = [(opp, c), (adj, c), (opp, adj), (adj, opp)]
            w = [fr(x // math.gcd(x, y), y // math.gcd(x, y)) for x, y in cands if (x, y) != val]
            return mcq("在 Rt△ABC 中，∠C ＝ 90°，BC ＝ %d，AC ＝ %d，AB ＝ %d。%s %s 等于多少？%s" % (a, b, c, fn, ang, _rt_svg(a, b, c)), ok, w,
                       "%s %s ＝ %s：%s ＝ <b>%s</b>。" % (fn, ang, {"sin": "对边 ÷ 斜边", "cos": "邻边 ÷ 斜边", "tan": "对边 ÷ 邻边"}[fn], fr(val[0], val[1]), ok))
        if k == "special":
            d = R.choice([30, 45, 60])
            fn = R.choice(["sin", "cos", "tan"])
            v = SP[d][["sin", "cos", "tan"].index(fn)]
            allv = sorted({x for t in SP.values() for x in t} | {"√3/3"})
            w = [x for x in allv if x != v]
            R.shuffle(w)

            def h(s):
                if "/" in s:
                    p, q = s.split("/")
                    return fr(p, q)
                return s
            return mcq("%s %d° 的值是多少？" % (fn, d), h(v), [h(x) for x in w],
                       "特殊角：sin 30° ＝ ½，sin 45° ＝ cos 45° ＝ √2/2，sin 60° ＝ cos 30° ＝ √3/2，tan 30° ＝ √3/3，tan 45° ＝ 1，tan 60° ＝ √3。<b>%s %d° ＝ %s</b>" % (fn, d, v))
        if k == "solve":
            d = R.choice([30, 60])
            c = R.choice([4, 6, 8, 10, 12, 14, 16, 20])
            if R.random() < 0.5:
                return mcq("在 Rt△ABC 中，∠C ＝ 90°，∠A ＝ %d°，斜边 AB ＝ %d。BC 等于多少？" % (d, c), str(c // 2) if d == 30 else "%d√3" % (c // 2),
                           ["%d√3" % (c // 2) if d == 30 else str(c // 2), str(c), "%d√2" % (c // 2)],
                           "BC 是 ∠A 的对边，BC ＝ AB · sin %d° ＝ %d × %s ＝ <b>%s</b>。" % (d, c, SP[d][0], str(c // 2) if d == 30 else "%d√3" % (c // 2)))
            a = R.choice([2, 3, 4, 5, 6, 8, 10])
            return mcq("在 Rt△ABC 中，∠C ＝ 90°，∠A ＝ 45°，BC ＝ %d。AB 等于多少？" % a, "%d√2" % a, [str(a), str(2 * a), "%d√3" % a],
                       "∠A ＝ 45°，△ABC 是等腰直角三角形，AB ＝ BC ÷ sin 45° ＝ <b>%d√2</b>。" % a)
        d = R.choice([30, 45, 60])
        L = R.choice([10, 12, 15, 20, 24, 30])
        v = {30: "%d√3/3" % L if L % 3 else "%d√3" % (L // 3), 45: str(L), 60: "%d√3" % L}[d]
        h = R.choice([1.5, 1.6]) if R.random() < 0.3 else 0
        if h:
            ok = "(%s ＋ %s) 米" % (v, ("%.1f" % h))
        else:
            ok = "%s 米" % v
        q = "在离旗杆 %d 米的地方，测得旗杆顶端的仰角为 %d°%s。旗杆高多少米？" % (L, d, "，测角仪高 %.1f 米" % h if h else "")
        w = []
        for dd in (30, 45, 60):
            if dd != d:
                vv = {30: "%d√3/3" % L if L % 3 else "%d√3" % (L // 3), 45: str(L), 60: "%d√3" % L}[dd]
                w.append("(%s ＋ %.1f) 米" % (vv, h) if h else "%s 米" % vv)
        w.append("%d 米" % (L * 2))
        return mcq(q, ok, w, "高 ＝ 水平距离 × tan %d° ＝ %d × %s%s，所以是 <b>%s</b>。" % (d, L, SP[d][2], "，再加上测角仪的高" if h else "", ok))
    return mk


# ------------------------------------------------------------------ 投影（九年级下）
def projection(kinds=("shadow", "lamp", "concept")):
    CON = [("太阳光下物体的影子属于哪一种投影？", "平行投影", ["中心投影", "正投影", "不是投影"]),
           ("路灯下物体的影子属于哪一种投影？", "中心投影", ["平行投影", "正投影", "不是投影"]),
           ("手电筒照射下物体的影子属于哪一种投影？", "中心投影", ["平行投影", "正投影", "不是投影"]),
           ("同一时刻，太阳光下两根竖直的木杆，杆越高影子就怎样？", "越长", ["越短", "一样长", "无法确定"]),
           ("一天中，太阳光下物体的影子什么时候最短？", "中午", ["早上", "傍晚", "一样长"]),
           ("人从路灯下走远时，影子会怎样变化？", "越来越长", ["越来越短", "不变", "先长后短"]),
           ("投射线垂直于投影面的平行投影叫什么？", "正投影", ["中心投影", "斜投影", "三视图"]),
           ("三视图中，主视图和俯视图要满足什么关系？", "长对正", ["高平齐", "宽相等", "完全相同"]),
           ("三视图中，主视图和左视图要满足什么关系？", "高平齐", ["长对正", "宽相等", "完全相同"]),
           ("三视图中，俯视图和左视图要满足什么关系？", "宽相等", ["长对正", "高平齐", "完全相同"]),
           ("一个球的三视图都是什么图形？", "圆", ["正方形", "三角形", "矩形"]),
           ("圆柱的主视图和俯视图分别是什么？（圆柱竖直放置）", "矩形和圆", ["圆和矩形", "两个圆", "两个矩形"]),
           ("圆锥的主视图和俯视图分别是什么？（圆锥竖直放置）", "三角形和圆", ["圆和三角形", "两个三角形", "三角形和矩形"]),
           ("正方体的三视图都是什么图形？", "正方形", ["长方形", "三角形", "圆"]),
           ("早上太阳在东方，物体的影子朝哪个方向？", "西方", ["东方", "南方", "北方"])]

    def mk():
        k = ch(kinds)
        if k == "concept":
            q, a, w = R.choice(CON)
            return mcq(q, a, w, "答案是<b>%s</b>。" % a)
        if k == "shadow":
            h1 = R.choice([1, 1.5, 1.6, 2])
            s1 = R.choice([1.2, 2, 2.4, 3, 0.8])
            s2 = R.choice([6, 8, 9, 12, 15, 18])
            H = h1 * s2 / s1
            if H != round(H, 1):
                return None
            hs = ("%.1f" % H).rstrip("0").rstrip(".")
            f = lambda x: ("%.1f" % x).rstrip("0").rstrip(".")
            return mcq("同一时刻，身高 %s 米的小明影长 %s 米，旁边一棵树的影长 %d 米。这棵树高多少米？" % (f(h1), f(s1), s2), "%s 米" % hs,
                       ["%s 米" % f(x) for x in (s1 * s2 / h1, s2 - s1 + h1, H + 1, s2 / 2) if f(x) != hs],
                       "同一时刻，物高与影长成正比例：树高 ＝ %s × %d ÷ %s ＝ <b>%s 米</b>。" % (f(h1), s2, f(s1), hs))
        Hl = R.choice([4, 4.8, 6, 6.4, 8])
        h = R.choice([1.6, 1.5, 2])
        d = R.choice([2, 3, 4, 5, 6])
        s = h * d / (Hl - h)
        if abs(s - round(s, 1)) > 1e-9:
            return None
        f = lambda x: ("%.1f" % x).rstrip("0").rstrip(".")
        return mcq("路灯高 %s 米，身高 %s 米的人站在离灯杆底部 %d 米处。他的影长是多少米？" % (f(Hl), f(h), d), "%s 米" % f(s),
                   ["%s 米" % f(x) for x in (h * d / Hl, d * Hl / h, s + 1, d - s if d - s > 0 else s + 2) if f(x) != f(s)],
                   "设影长为 x 米，由相似三角形：%s ∶ %s ＝ x ∶ (x ＋ %d)，解得 x ＝ <b>%s 米</b>。" % (f(h), f(Hl), d, f(s)))
    return mk


# ------------------------------------------------------------------ 一元一次方程的应用（七年级上）
def lin_word(kinds=("profit", "work", "transfer", "number")):
    def mk():
        k = ch(kinds)
        if k == "profit":
            cost = R.choice([80, 100, 120, 150, 200, 240])
            up = R.choice([30, 40, 50, 60])
            z = R.choice([8, 9, 7.5, 8.5])
            price = cost * (100 + up) / 100
            sell = price * z / 10
            if sell != int(sell) or price != int(price):
                return None
            prof = int(sell - cost)
            if prof <= 0:
                return None
            zz = ("%g" % z)
            return mcq("一件商品按成本价提高 %d%% 标价，再打%s折出售，售价是 %d 元。这件商品的成本价是多少元？" % (up, zz, sell), "%d 元" % cost,
                       ["%d 元" % x for x in (int(price), int(sell - prof * 2) if sell - prof * 2 > 0 else cost + 20, cost + 10, int(sell * 10 / z)) if x != cost],
                       "设成本价为 x 元，(1 ＋ %d%%)x × %s%% ＝ %d，解得 x ＝ <b>%d 元</b>。" % (up, ("%g" % (z * 10)), sell, cost))
        if k == "work":
            a, b = R.choice([(10, 15), (12, 24), (6, 12), (20, 30), (8, 24), (15, 10)])
            d = R.randint(2, 4)
            rest = F(1) - F(d, a)
            x = rest / (F(1, a) + F(1, b))
            if x.denominator != 1:
                return None
            return mcq("一项工作，甲单独做要 %d 天，乙单独做要 %d 天。甲先做 %d 天，剩下的由甲、乙合做，还要几天完成？" % (a, b, d), "%d 天" % x,
                       ["%d 天" % v for v in (x + 1, x - 1 if x > 1 else x + 2, F(a * b, a + b) if F(a * b, a + b).denominator == 1 else x + 3, (a + b) // 2 - d) if v != x and v > 0],
                       "设还要 x 天，%s ＋ (%s ＋ %s)x ＝ 1，解得 x ＝ <b>%d 天</b>。" % (fs(F(d, a)), fs(F(1, a)), fs(F(1, b)), x))
        if k == "transfer":
            a, b = R.randint(20, 60), R.randint(10, 40)
            m = R.choice([2, 3])
            # 从乙调 x 人到甲，使甲是乙的 m 倍
            x = F(m * b - a, m + 1)
            if x.denominator != 1 or x <= 0 or x >= b:
                return None
            return mcq("甲组有 %d 人，乙组有 %d 人。从乙组调多少人到甲组，才能使甲组人数是乙组的 %d 倍？" % (a, b, m), "%d 人" % x,
                       ["%d 人" % v for v in (x + 1, x - 1 if x > 1 else x + 2, abs(m * b - a), (b - a // m) if b - a // m > 0 else x + 3) if v != x and v > 0],
                       "设调 x 人，%d ＋ x ＝ %d(%d － x)，解得 x ＝ <b>%d 人</b>。" % (a, m, b, x))
        n = R.randint(3, 40)
        t = R.randint(0, 1)
        if t == 0:
            s = 3 * n + 3
            return mcq("三个连续整数的和是 %d，最小的数是多少？" % s, str(n), [str(v) for v in (n + 1, n - 1, s // 3 + 1)],
                       "设最小的数是 x，x ＋ (x ＋ 1) ＋ (x ＋ 2) ＝ %d，解得 x ＝ <b>%d</b>。" % (s, n))
        s = 3 * (2 * n) + 6
        return mcq("三个连续偶数的和是 %d，最大的数是多少？" % s, str(2 * n + 4), [str(v) for v in (2 * n, 2 * n + 2, 2 * n + 6)],
                   "设中间的数是 x，(x － 2) ＋ x ＋ (x ＋ 2) ＝ %d，x ＝ %d，最大的数是 <b>%d</b>。" % (s, 2 * n + 2, 2 * n + 4))
    return mk


# ------------------------------------------------------------------ 用频率估计概率（九年级上）
def freq_prob():
    def mk():
        t = R.randint(0, 1)
        if t == 0:
            n = R.choice([200, 400, 500, 800, 1000, 2000])
            p = F(R.choice([1, 2, 3, 4, 7, 9]), R.choice([5, 10, 20, 25]))
            if p >= 1:
                return None
            m = p * n
            if m.denominator != 1:
                return None
            ok = ("%g" % float(p))
            return mcq("在同样条件下做 %d 次摸球试验，摸到红球 %d 次。估计摸到红球的概率约是多少？" % (n, m), ok,
                       [("%g" % float(1 - p)), str(m), ("%g" % float(p / 10)) if p / 10 != p else "0.5", ("%g" % float(p * 2)) if p * 2 < 1 else "1"],
                       "大量重复试验时，用频率估计概率：%d ÷ %d ＝ <b>%s</b>。" % (m, n, ok))
        total = R.choice([20, 30, 40, 50, 60, 80, 100])
        p = F(R.choice([1, 1, 2, 3]), R.choice([4, 5, 10]))
        r = p * total
        if r.denominator != 1 or r == 0:
            return None
        return mcq("袋中有红球和白球共 %d 个，多次摸球试验后发现摸到红球的频率稳定在 %s 左右。估计袋中有红球多少个？" % (total, "%g" % float(p)), "%d 个" % r,
                   ["%d 个" % v for v in (total - r, r + 2, total // 2 if total // 2 != r else r + 5, int(float(p) * 100)) if v != r and v > 0],
                   "红球个数约为 %d × %s ＝ <b>%d 个</b>。" % (total, "%g" % float(p), r))
    return mk
