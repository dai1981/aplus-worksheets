# -*- coding: utf-8 -*-
"""
대한민국 고등학교 공통수학1（2022 개정）の 16 単元。build(key)：
  poly 다항식의 연산 / rem 항등식과 나머지정리 / fact 인수분해 / cplx 복소수 / disc 판별식 / coef 근과 계수의 관계
  qfun 이차방정식과 이차함수 / maxmin 이차함수의 최대·최소 / cubic 삼차방정식과 사차방정식 / simq 연립이차방정식
  lin 연립일차부등식과 절댓값 / qineq 이차부등식 / count 경우의 수 / perm 순열 / comb 조합 / mat 행렬
誤答は「빼기에서 괄호 뒤 부호를 놓친다」「나머지정리에서 x = −a를 대입한다」「i² = 1」「판별식을 b² + 4ac로 쓴다」
「두 근의 합을 b/a로 쓴다」「부등식에서 음수로 나누고 방향을 그대로 둔다」「순열과 조합을 바꾼다」「행렬의 곱을 성분끼리 곱한다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_m2a import poly2
from kr_hs import M, N, neg, par, sg, px, padd, pmul, peval, pdiv, cx, surd, sq_split, mx, roots, W, graph, josa, Names, num, fr, unit, BLUE, RED

R = random.Random(83001)
NM = Names(R)
G = "common-math-1"
NZ = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]


def nz(lo=-6, hi=6):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


# ------------------------------------------------------------------ 다항식의 연산
def p_ops(kinds=("add", "sub", "mul", "expand", "cube")):
    def mk():
        how = R.choice(kinds)
        A = [R.choice([1, 2, 3, -1, -2]), R.randint(-6, 6), R.randint(-7, 7)]
        B = [R.choice([1, 2, -1, -3]), R.randint(-6, 6), R.randint(-7, 7)]
        if how in ("add", "sub"):
            k = 1 if how == "add" else -1
            ok = px(padd(A, B, k))
            w = [px(padd(A, B, -k)), px(padd(A, [B[0], -B[1], -B[2]], k)), px(padd(A, [B[0], B[1], -B[2]], k)), px(padd(A, B, 2 * k)), px(padd(A, [-B[0], B[1], B[2]], k))]
            return M("A = %s, B = %s일 때, <b>A %s B</b>를 계산하면?" % (px(A), px(B), "+" if k == 1 else "−"), ok, w, "동류항끼리 계산해요%s. <b>%s</b>" % (". 빼기는 B의 모든 항의 부호를 바꾸어 더해요" if k < 0 else "", ok))
        if how == "mul":
            P = [1, nz(-5, 5)]
            Q = [R.choice([1, 2, -1]), nz(), R.randint(-5, 5)]
            ok = px(pmul(P, Q))
            w = [px(pmul([1, -P[1]], Q)), px(padd(pmul([1, 0], Q), [Q[2] * P[1]])), px(pmul(P, [Q[0], -Q[1], Q[2]])), px(padd(pmul(P, Q), [1]))]
            return M("<b>(%s)(%s)</b>를 전개하면?" % (px(P), px(Q)), ok, w, "분배법칙으로 각 항을 모두 곱해요. <b>%s</b>" % ok)
        if how == "expand":
            p_, q_ = nz(-4, 4), nz(-5, 5)
            ex = lambda P, Q, k: poly2({(2, 0): 1, (0, 2): P * P, (0, 0): Q * Q, (1, 1): 2 * P * k, (0, 1): 2 * P * Q * k, (1, 0): 2 * Q}, ("x", "y"))
            t = poly2({(1, 0): 1, (0, 1): p_, (0, 0): q_}, ("x", "y"))
            ok = ex(p_, q_, 1)
            w = [poly2({(2, 0): 1, (0, 2): p_ * p_, (0, 0): q_ * q_}, ("x", "y")),
                 poly2({(2, 0): 1, (0, 2): p_ * p_, (0, 0): q_ * q_, (1, 1): p_, (0, 1): p_ * q_, (1, 0): q_}, ("x", "y")),
                 poly2({(2, 0): 1, (0, 2): p_ * p_, (0, 0): q_ * q_, (1, 1): -2 * p_, (0, 1): 2 * p_ * q_, (1, 0): 2 * q_}, ("x", "y")),
                 poly2({(2, 0): 1, (0, 2): p_ * p_, (0, 0): q_ * q_, (1, 1): 2 * p_, (0, 1): -2 * p_ * q_, (1, 0): 2 * q_}, ("x", "y"))]
            return M("<b>(%s)²</b>을 전개하면?" % t, ok, w, "(a + b + c)² = a² + b² + c² + 2ab + 2bc + 2ca를 이용해요. <b>%s</b>" % ok)
        c_ = R.choice([1, 1, 2, 3])
        k = nz(-4, 4)
        if math.gcd(c_, abs(k)) != 1:
            return None
        base = [c_, k]
        ok = px(pmul(pmul(base, base), base))
        w = [px([c_ ** 3, 0, 0, k ** 3]), px([c_ ** 3, 3 * c_ * c_ * k, 3 * c_ * k, k ** 3]), px([c_ ** 3, c_ * c_ * k, c_ * k * k, k ** 3]), px(pmul(pmul([c_, -k], [c_, -k]), [c_, -k]))]
        return M("<b>(%s)³</b>을 전개하면?" % px(base), ok, w, "(a + b)³ = a³ + 3a²b + 3ab² + b³. <b>%s</b>" % ok)
    return mk


def p_div(kinds=("q", "r", "val")):
    def mk():
        how = R.choice(kinds)
        d = [1, nz(-4, 4)]
        Q = [R.choice([1, 2, -1, 3]), R.randint(-5, 5), R.randint(-5, 5)]
        r = R.randint(-6, 6)
        A = padd(pmul(d, Q), [r])
        if how == "q":
            ok = px(Q)
            return M("<b>(%s) ÷ (%s)</b>의 몫은?" % (px(A), px(d)), ok, [px([Q[0], -Q[1], Q[2]]), px(padd(Q, [1])), px([Q[0], Q[1], -Q[2]]) if Q[2] else px(padd(Q, [-1])), px([Q[0], Q[1] + 1, Q[2]])],
                     "직접 나누거나 조립제법을 써요. 몫 <b>%s</b>, 나머지 %s" % (ok, neg(r)))
        if how == "r":
            return N("<b>(%s) ÷ (%s)</b>의 나머지는?" % (px(A), px(d)), r, [-r, peval(A, d[1]), r + 1, A[-1]], "나머지 = (x = %s를 대입한 값) = <b>%s</b>" % (neg(-d[1]), neg(r)))
        B = [1, nz(-4, 4)]
        S = [R.choice([1, 2]), R.randint(-4, 4)]
        rr = R.randint(-5, 5)
        Aa = padd(pmul(B, S), [rr])
        return M("다항식 A를 %s로 나누었더니 몫이 %s, 나머지가 %s였어요. A는?" % (px(B), px(S), neg(rr)), px(Aa), [px(pmul(B, S)), px(padd(pmul(B, S), [-rr])), px(padd(pmul(B, [S[0], -S[1]]), [rr])), px(padd(pmul([1, -B[1]], S), [rr]))],
                 "A = (나누는 식) × (몫) + (나머지). <b>%s</b>" % px(Aa))
    return mk


# ------------------------------------------------------------------ 항등식과 나머지정리
def r_main(kinds=("rem", "factor", "ident", "twodiv", "synth")):
    def mk():
        how = R.choice(kinds)
        if how == "rem":
            A = [R.choice([1, 2, -1]), R.randint(-4, 4), R.randint(-5, 5), R.randint(-6, 6)]
            a = nz(-3, 3)
            k = R.choice([1, 2])
            if k == 2:
                a2 = Fr(nz(-3, 3), 2)
                v = peval(A, a2)
                return N("다항식 %s를 %s로 나눈 나머지는?" % (px(A), px([2, -2 * a2])), v, [peval(A, -a2), peval(A, 2 * a2), v * 2, A[-1]],
                         "2x %s %s = 0에서 x = %s를 대입해요. <b>%s</b>" % ("−" if a2 > 0 else "+", neg(abs(2 * a2)), neg(a2), neg(v)))
            v = peval(A, a)
            return N("다항식 P(x) = %s를 %s로 나눈 나머지는?" % (px(A), px([1, -a])), v, [peval(A, -a), A[-1], v + 1, sum(A)], "나머지정리: P(%s) = <b>%s</b>" % (neg(a), neg(v)))
        if how == "factor":
            a = nz(-3, 3)
            A = [1, R.randint(-4, 4), R.randint(-5, 5)]
            rest = peval(A + [0], a)
            # x³ + px² + qx + k 가 (x − a)로 나누어떨어지도록 k
            k = -peval(A + [0], a)
            P = A + [k]
            return N("다항식 %s + k가 %s로 나누어떨어질 때, 상수 k의 값은?" % (px(A + [0]), px([1, -a])), k, [-k, peval(A + [0], -a), k + 1, rest], "P(%s) = 0이 되어야 해요. <b>k = %s</b>" % (neg(a), neg(k)))
        if how == "ident":
            p, q = nz(-5, 5), nz(-5, 5)
            # (x + p)(x + q) = x² + ax + b  → a+b?
            a, b = p + q, p * q
            k = R.choice(["a", "b", "ab"])
            v = {"a": a, "b": b, "ab": a + b}[k]
            return N("등식 (x %s %d)(x %s %d) = x² + ax + b가 x에 대한 항등식일 때, <b>%s</b>의 값은?" % ("+" if p > 0 else "−", abs(p), "+" if q > 0 else "−", abs(q), {"a": "a", "b": "b", "ab": "a + b"}[k]), v,
                     [{"a": -a, "b": -b, "ab": -(a + b)}[k], {"a": b, "b": a, "ab": a - b}[k], v + 1, p - q], "좌변을 전개해 계수를 비교하면 a = %s, b = %s. <b>%s</b>" % (neg(a), neg(b), neg(v)))
        if how == "twodiv":
            a, b = R.sample([-3, -2, -1, 1, 2, 3], 2)
            r1, r2 = R.randint(-8, 8), R.randint(-8, 8)
            # R(x) = px + q, p·a + q = r1, p·b + q = r2
            p = Fr(r1 - r2, a - b)
            q = r1 - p * a
            if p.denominator != 1 or q.denominator != 1:
                return None
            ok = px([p, q])
            return M("다항식 P(x)를 %s로 나눈 나머지는 %s, %s로 나눈 나머지는 %s예요. P(x)를 (%s)(%s)로 나눈 나머지는?" % (px([1, -a]), neg(r1), px([1, -b]), neg(r2), px([1, -a]), px([1, -b])), ok,
                     [px([-p, q]), px([p, -q]), px([q, p]) if q else px([p, 1]), px([r1, r2])], "나머지를 px + q로 놓으면 %s = %s, %s = %s. <b>%s</b>" % (px([a, 1], "p").replace("+ 1", "+ q").replace("− 1", "+ q") if False else (px([a, 0], "p") + " + q"), neg(r1), px([b, 0], "p") + " + q", neg(r2), ok))
        A = [1, R.randint(-4, 4), R.randint(-5, 5), R.randint(-6, 6)]
        a = nz(-3, 3)
        Q, r = pdiv(A, [1, -a])
        return M("조립제법으로 %s를 %s로 나눈 몫은?" % (px(A), px([1, -a])), px(Q), [px(pdiv(A, [1, a])[0]), px(padd(Q, [1])), px([Q[0], -Q[1], Q[2]]) if Q[1] else px([Q[0], 1, Q[2]]), px(A[:3])],
                 "%s를 쓰고 내려 곱하고 더해요. 몫 <b>%s</b>, 나머지 %s" % (neg(a), px(Q), neg(r[0])))
    return mk


# ------------------------------------------------------------------ 인수분해
def pq(u, v):
    """(x + u)(x + v)：u ≥ v"""
    u, v = max(u, v), min(u, v)
    if u == v:
        return "(%s)²" % px([1, u])
    return "(%s)(%s)" % (px([1, u]), px([1, v]))


def f_main(kinds=("cube", "sum3", "sub", "quart", "cubic", "biq")):
    def mk():
        how = R.choice(kinds)
        if how == "cube":
            c_ = R.choice([1, 1, 2, 3])
            a = R.randint(1, 6)
            if math.gcd(c_, a) != 1:
                return None
            sg_ = R.choice([1, -1])
            X = "x" if c_ == 1 else "%dx" % c_
            S, T = ("+", "−") if sg_ > 0 else ("−", "+")
            ok = "(%s %s %d)(%s %s %sx + %d)" % (X, S, a, px([c_ * c_, 0, 0]), T, (str(c_ * a) if c_ * a != 1 else ""), a * a)
            bad = "(%s %s %d)(%s %s %sx + %d)" % (X, S, a, px([c_ * c_, 0, 0]), S, (str(c_ * a) if c_ * a != 1 else ""), a * a)
            return M("<b>%s</b>을 인수분해하면?" % px([c_ ** 3, 0, 0, sg_ * a ** 3]), ok, [bad, "(%s %s %d)³" % (X, S, a), "(%s %s %d)(%s + %d)" % (X, S, a, px([c_ * c_, 0, 0]), a * a)],
                     "a³ %s b³ = (a %s b)(a² %s ab + b²)에서 a = %s, b = %d. <b>%s</b>" % (S, S, T, X, a, ok))
        if how == "sum3":
            a = R.randint(1, 6)
            s = R.choice([1, -1])
            q = px([1, 3 * s * a, 3 * a * a, s * a ** 3])
            ok = "(%s)³" % px([1, s * a])
            return M("<b>%s</b>을 인수분해하면?" % q, ok, ["(%s)³" % px([1, -s * a]), "(%s)(%s)²" % (px([1, s * a]), px([1, -s * a])), "(%s)³" % px([1, s * 3 * a])], "a³ + 3a²b + 3ab² + b³ = (a + b)³. <b>%s</b>" % ok)
        if how == "sub":
            p, q = sorted(R.sample([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6], 2), reverse=True)
            k = R.randint(1, 4)
            irr = lambda c: k * k - 4 * c < 0 or math.isqrt(k * k - 4 * c) ** 2 != k * k - 4 * c
            if p + q == 0 or not (irr(p) and irr(q)):
                return None
            X = px([1, k, 0])
            t = "(%s)²%s" % (X, px([1, p + q, p * q], "T")[2:].replace("T", "(%s)" % X))
            ok = "(%s)(%s)" % (px([1, k, p]), px([1, k, q]))
            bad = "(%s)(%s)" % (px([1, k, -p]), px([1, k, -q]))
            return M("<b>%s</b>을 인수분해하면?" % t, ok, [bad, "(%s)²" % X, "(%s)(%s)" % (px([1, p]), px([1, q])), "(%s)(%s)" % (px([1, -k, p]), px([1, -k, q]))],
                     "%s = t로 놓으면 %s = (%s)(%s). <b>%s</b>" % (X, px([1, p + q, p * q], "t"), px([1, p], "t"), px([1, q], "t"), ok))
        if how == "quart":
            a, b = R.sample([1, 2, 3, 4, 5, 6], 2)
            # x⁴ − (a²+b²)x² + a²b² = (x+a)(x−a)(x+b)(x−b)
            a, b = min(a, b), max(a, b)
            ok = "(x + %d)(x − %d)(x + %d)(x − %d)" % (a, a, b, b)
            return M("<b>%s</b>을 인수분해하면?" % px([1, 0, -(a * a + b * b), 0, a * a * b * b]), ok, ["(x² − %d)(x² − %d)" % (a, b), "(x + %d)²(x − %d)²" % (a, b), "(x² + %d)(x² − %d)" % (a * a, b * b)],
                     "x² = t로 놓으면 (t − %d)(t − %d)이고 각각 다시 인수분해해요. <b>%s</b>" % (a * a, b * b, ok))
        if how == "diff4":
            a = R.randint(1, 6)
            ok = "(x + %d)(x − %d)(x² + %d)" % (a, a, a * a)
            return M("<b>%s</b>을 인수분해하면?" % px([1, 0, 0, 0, -a ** 4]), ok, ["(x² + %d)(x² − %d)" % (a * a, a * a), "(x + %d)²(x − %d)²" % (a, a), "(x − %d)⁴" % a, "(x + %d)(x − %d)(x² − %d)" % (a, a, a * a)],
                     "A² − B² = (A + B)(A − B)를 두 번 써요. <b>%s</b>" % ok)
        if how == "biq":
            a = R.randint(1, 5)
            # x⁴ + 4a⁴ 대신 x⁴ + a²x² + a⁴ = (x² + ax + a²)(x² − ax + a²)
            ok = "(x² + %sx + %d)(x² − %sx + %d)" % (("" if a == 1 else a), a * a, ("" if a == 1 else a), a * a)
            return M("<b>%s</b>을 인수분해하면?" % px([1, 0, a * a, 0, a ** 4]), ok, ["(x² + %d)²" % (a * a), "(x² + %d)(x² − %d)" % (a * a, a * a), "(x² + %sx − %d)(x² − %sx − %d)" % (("" if a == 1 else a), a * a, ("" if a == 1 else a), a * a)],
                     "(x² + %d)² − %sx²으로 고쳐 A² − B² 꼴로 만들어요. <b>%s</b>" % (a * a, "" if a == 1 else str(a * a), ok))
        r1, r2, r3 = R.sample([-3, -2, -1, 1, 2, 3, 4], 3)
        P = pmul(pmul([1, -r1], [1, -r2]), [1, -r3])
        rs = sorted([-r1, -r2, -r3], reverse=True)
        ok = "(%s)(%s)(%s)" % tuple(px([1, v]) for v in rs)
        bad = "(%s)(%s)(%s)" % tuple(px([1, -v]) for v in sorted([-r1, -r2, -r3]))
        return M("<b>%s</b>을 인수분해하면?" % px(P), ok, [bad, "(%s)(%s)(%s)" % (px([1, rs[0]]), px([1, -rs[1]]), px([1, rs[2]])), "(%s)(%s)" % (px([1, rs[0]]), px(pmul([1, rs[1]], [1, -rs[2]])))],
                 "P(%s) = 0이므로 인수정리와 조립제법으로 나누어요. <b>%s</b>" % (neg(r1), ok))
    return mk


# ------------------------------------------------------------------ 복소수
def c_ops(kinds=("add", "mul", "div", "ipow", "conj", "eq")):
    def mk():
        how = R.choice(kinds)
        a, b, c, d = R.randint(-6, 6), nz(), R.randint(-6, 6), nz()
        if how == "add":
            s = R.choice([1, -1])
            ok = cx(a + s * c, b + s * d)
            return M("<b>(%s) %s (%s)</b>를 계산하면?" % (cx(a, b), "+" if s > 0 else "−", cx(c, d)), ok, [cx(a - s * c, b - s * d), cx(a + s * c, b - s * d), cx(b + s * d, a + s * c) if a + s * c else cx(a + s * c + 1, b + s * d), cx(a + s * c, -(b + s * d)), cx(a + c * s, b + d)],
                     "실수부분끼리, 허수부분끼리 계산해요. <b>%s</b>" % ok)
        if how == "mul":
            ok = cx(a * c - b * d, a * d + b * c)
            return M("<b>(%s)(%s)</b>를 계산하면?" % (cx(a, b), cx(c, d)), ok, [cx(a * c + b * d, a * d + b * c), cx(a * c, b * d), cx(a * c - b * d, a * d - b * c), cx(a * c + b * d, -(a * d + b * c))],
                     "i² = −1을 이용해요. <b>%s</b>" % ok)
        if how == "div":
            p, q = R.randint(-5, 5), nz(-5, 5)
            c, d = R.randint(1, 3), nz(-3, 3)
            # (p + qi)(c + di) / (c + di) 이 되도록 분자 만들기
            n_re, n_im = p * c - q * d, p * d + q * c
            ok = cx(p, q)
            return M("<b>(%s) ÷ (%s)</b>를 계산하면?" % (cx(n_re, n_im), cx(c, d)), ok, [cx(p, -q), cx(-p, q), cx(Fr(n_re, c), Fr(n_im, d)), cx(q, p) if p else cx(q, 1)],
                     "분모와 분자에 켤레복소수 %s를 곱해요. <b>%s</b>" % (cx(c, -d), ok))
        if how == "ipow":
            n = R.randint(5, 103)
            v = [(1, 0), (0, 1), (-1, 0), (0, -1)][n % 4]
            ok = cx(*v)
            return M("<b>i<sup>%d</sup></b>의 값은?" % n, ok, [x for x in ("1", "i", "−1", "−i") if x != ok], "i⁴ = 1이므로 %d을 4로 나눈 나머지 %d를 봐요. <b>%s</b>" % (n, n % 4, ok))
        if how == "conj":
            k = R.choice(["sum", "prod"])
            if k == "sum":
                return N("z = %s일 때, z와 켤레복소수 z̄의 합 z + z̄의 값은?" % cx(a, b), 2 * a, [2 * b, 0, a, 2 * a + 2 * b], "z + z̄ = 2 × (실수부분) = <b>%s</b>" % neg(2 * a))
            return N("z = %s일 때, z z̄의 값은?" % cx(a, b), a * a + b * b, [a * a - b * b, 2 * a, a * a, -(a * a + b * b)], "z z̄ = a² + b² = <b>%s</b>" % neg(a * a + b * b))
        x, y = R.randint(-6, 6), R.randint(-6, 6)
        p, q = nz(-3, 3), nz(-3, 3)
        return M("등식 (x %s %d) + (y %s %d)i = %s를 만족하는 실수 x, y의 값은?" % ("+" if p > 0 else "−", abs(p), "+" if q > 0 else "−", abs(q), cx(x + p, y + q)), "x = %s, y = %s" % (neg(x), neg(y)),
                 ["x = %s, y = %s" % (neg(x + 2 * p), neg(y + 2 * q)), "x = %s, y = %s" % (neg(y), neg(x)), "x = %s, y = %s" % (neg(x + p), neg(y + q))], "실수부분과 허수부분이 각각 같아요. <b>x = %s, y = %s</b>" % (neg(x), neg(y)))
    return mk


def c_concept():
    F_ = [("i의 정의로 옳은 것은?", "i² = −1", ["i² = 1", "i = −1", "i = √1"], "제곱하여 −1이 되는 수를 i로 나타내요."),
          ("√−4를 i를 사용하여 나타내면?", "2i", ["−2", "4i", "−2i"], "√−4 = √4 i = <b>2i</b>"),
          ("√−2 × √−3의 값은?", "−√6", ["√6", "√6 i", "−√6 i"], "√2 i × √3 i = √6 i² = <b>−√6</b>"),
          ("복소수 a + bi (a, b는 실수)가 순허수일 조건은?", "a = 0, b ≠ 0", ["a ≠ 0, b = 0", "a = b", "a = 0, b = 0"], "실수부분이 0이고 허수부분이 0이 아니어야 해요."),
          ("복소수 3 − 2i의 켤레복소수는?", "3 + 2i", ["−3 + 2i", "−3 − 2i", "2 − 3i"], "허수부분의 부호만 바꿔요. <b>3 + 2i</b>"),
          ("음수 −9의 제곱근은?", "±3i", ["±3", "3i", "−3"], "x² = −9의 해는 <b>±3i</b>예요.")]
    pool = F_[:]
    R.shuffle(pool)

    def mk():
        return M(*pool.pop()) if pool else None
    return mk


# ------------------------------------------------------------------ 판별식과 근과 계수의 관계
def d_main(kinds=("kind", "k_double", "k_real", "k_none", "formula")):
    def mk():
        how = R.choice(kinds)
        if how == "kind":
            a, b, c = R.choice([1, 2, 3, -1]), R.randint(-7, 7), R.randint(-6, 6)
            D = b * b - 4 * a * c
            ok = "서로 다른 두 실근" if D > 0 else ("중근" if D == 0 else "서로 다른 두 허근")
            return M("이차방정식 <b>%s = 0</b>의 근을 판별하면?" % px([a, b, c]), ok, [x for x in ("서로 다른 두 실근", "중근", "서로 다른 두 허근", "실근 하나와 허근 하나") if x != ok], "D = b² − 4ac = %s. <b>%s</b>" % (neg(D), ok))
        A = R.choice([1, 1, 2, 3])
        b = nz(-10, 10)
        k0 = Fr(b * b, 4 * A)
        qf = "%s %s %sx + k = 0" % (px([A, 0, 0]), "+" if b > 0 else "−", "" if abs(b) == 1 else abs(b))
        if how == "k_double":
            return N("이차방정식 <b>%s</b>이 중근을 가질 때, 상수 k의 값은?" % qf, k0, [b * b, Fr(b * b, 4), -k0, Fr(b, 2 * A), k0 + 1], "D = %d − %dk = 0 → k = <b>%s</b>" % (b * b, 4 * A, neg(k0)))
        if how == "k_real":
            return M("이차방정식 <b>%s</b>이 실근을 가질 때, 상수 k의 값의 범위는?" % qf, "k ≤ %s" % neg(k0), ["k ≥ %s" % neg(k0), "k &lt; %s" % neg(k0), "k ≤ %s" % neg(-k0), "k ≤ %s" % neg(Fr(b * b, 4) if A > 1 else b * b)],
                     "D ≥ 0 → %d − %dk ≥ 0. <b>k ≤ %s</b>" % (b * b, 4 * A, neg(k0)))
        if how == "k_none":
            return M("이차방정식 <b>%s</b>이 허근을 가질 때, 상수 k의 값의 범위는?" % qf, "k &gt; %s" % neg(k0), ["k ≥ %s" % neg(k0), "k &lt; %s" % neg(k0), "k &gt; %s" % neg(-k0), "k &gt; %s" % neg(Fr(b * b, 4) if A > 1 else b * b)],
                     "D &lt; 0 → %d − %dk &lt; 0. <b>k &gt; %s</b>" % (b * b, 4 * A, neg(k0)))
        a, b, c = 1, R.randint(-6, 6), R.randint(2, 9)
        D = b * b - 4 * c
        if D >= 0:
            return None
        s, t = sq_split(-D)
        g = math.gcd(math.gcd(abs(b), s), 2)
        num_ = "%s ± %s" % (neg(Fr(-b, g)), surd(Fr(s, g), t) + "i") if b else "±" + surd(Fr(s, g), t) + "i"
        ok = "x = " + (fr(num_, 2 // g) if 2 // g != 1 else num_)
        num2 = "%s ± %s" % (neg(Fr(b, g)), surd(Fr(s, g), t) + "i") if b else "±" + surd(Fr(s, g), t)
        return M("이차방정식 <b>%s = 0</b>을 풀면?" % px([1, b, c]), ok, ["x = " + (fr(num2, 2 // g) if 2 // g != 1 else num2), "x = " + (fr(num_.replace("i", ""), 2 // g) if 2 // g != 1 else num_.replace("i", "")), "해가 없어요"],
                 "D = %s &lt; 0이므로 허근이에요. 근의 공식으로 <b>%s</b>" % (neg(D), ok))
    return mk


def k_coef(kinds=("sum", "prod", "sym", "make", "find")):
    def mk():
        how = R.choice(kinds)
        a, b, c = R.choice([1, 2, 3, -1]), R.randint(-9, 9), nz(-9, 9)
        S, P = Fr(-b, a), Fr(c, a)
        if how == "sum":
            return N("이차방정식 <b>%s = 0</b>의 두 근의 합은?" % px([a, b, c]), S, [-S, P, Fr(b, 1), Fr(-c, a)], "α + β = −b/a = <b>%s</b>" % neg(S))
        if how == "prod":
            return N("이차방정식 <b>%s = 0</b>의 두 근의 곱은?" % px([a, b, c]), P, [-P, S, Fr(c, 1) if a != 1 else -S, Fr(-b, c)], "αβ = c/a = <b>%s</b>" % neg(P))
        if how == "sym":
            k = R.choice(["sq", "inv", "diff"])
            if k == "sq":
                v = S * S - 2 * P
                return N("이차방정식 <b>%s = 0</b>의 두 근을 α, β라 할 때, α² + β²의 값은?" % px([a, b, c]), v, [S * S + 2 * P, S * S, S * S - P, v + 2], "(α + β)² − 2αβ = %s − %s = <b>%s</b>" % (neg(S * S), neg(2 * P), neg(v)))
            if k == "inv":
                v = S / P
                return N("이차방정식 <b>%s = 0</b>의 두 근을 α, β라 할 때, 1/α + 1/β의 값은?" % px([a, b, c]), v, [P / S if S else v + 1, -v, S * P, 1 / S if S else v - 1], "(α + β) ÷ αβ = <b>%s</b>" % neg(v))
            v = S * S - 4 * P
            return N("이차방정식 <b>%s = 0</b>의 두 근을 α, β라 할 때, (α − β)²의 값은?" % px([a, b, c]), v, [S * S - 2 * P, S * S + 4 * P, S * S, v + 4], "(α + β)² − 4αβ = <b>%s</b>" % neg(v))
        if how == "make":
            p, q = R.randint(-6, 6), R.randint(-6, 6)
            if p == q:
                return None
            ok = px([1, -(p + q), p * q]) + " = 0"
            return M("두 수 %s, %s를 근으로 하고 x²의 계수가 1인 이차방정식은?" % (neg(p), neg(q)), ok, [px([1, p + q, p * q]) + " = 0", px([1, -(p + q), -p * q]) + " = 0", px([1, p * q, p + q]) + " = 0"],
                     "x² − (두 근의 합)x + (두 근의 곱) = 0. <b>%s</b>" % ok)
        r = nz(-5, 5)
        k = nz(-6, 6)
        # x² + kx + c 의 한 근이 r, 다른 근 s: r + s = −k
        s = -k - r
        c = r * s
        if s == r:
            return None
        return N("이차방정식 <b>x² %s %sx %s %d = 0</b>의 한 근이 %s일 때, 다른 한 근은?" % ("+" if k > 0 else "−", "" if abs(k) == 1 else abs(k), "+" if c > 0 else "−", abs(c), neg(r)), s, [-s, r, c, -k], "두 근의 곱이 %s이므로 %s × β = %s. <b>%s</b>" % (neg(c), par(r), neg(c), neg(s)))
    return mk


# ------------------------------------------------------------------ 이차방정식과 이차함수
def q_graph(kinds=("xint", "count", "k", "line", "tangent")):
    def mk():
        how = R.choice(kinds)
        if how == "xint":
            p, q = R.sample(range(-5, 6), 2)
            a = R.choice([1, -1, 2])
            f = pmul([a], pmul([1, -p], [1, -q]))
            g = graph([(lambda x, f=f: float(peval(f, x)), BLUE, "")], label="이차함수의 그래프") if max(abs(p), abs(q)) <= 5 and abs(f[2]) <= 5 and R.random() < 0.4 else ""
            ok = "%s, %s" % (neg(min(p, q)), neg(max(p, q)))
            return M("이차함수 <b>y = %s</b>의 그래프가 x축과 만나는 점의 x좌표는?%s" % (px(f), g), ok, ["%s, %s" % (neg(-max(p, q)), neg(-min(p, q))), "%s" % neg(f[2]), "%s, %s" % (neg(min(p, q)), neg(-max(p, q)))],
                     "이차방정식 %s = 0의 실근이 x좌표예요. <b>%s</b>" % (px(f), ok))
        if how == "count":
            a, b, c = R.choice([1, -1, 2]), R.randint(-6, 6), R.randint(-5, 5)
            D = b * b - 4 * a * c
            n = 2 if D > 0 else (1 if D == 0 else 0)
            return N("이차함수 <b>y = %s</b>의 그래프와 x축의 교점의 개수는?" % px([a, b, c]), n, [x for x in (0, 1, 2, 3) if x != n], "D = %s → <b>%d개</b>" % (neg(D), n), f=lambda v: "%s개" % neg(v))
        if how == "k":
            b = nz(-10, 10)
            k0 = Fr(b * b, 4)
            kind = R.choice(["meet2", "touch", "none"])
            ok = {"meet2": "k &lt; %s", "touch": "k = %s", "none": "k &gt; %s"}[kind] % neg(k0)
            nm = {"meet2": "서로 다른 두 점에서 만날", "touch": "접할", "none": "만나지 않을"}[kind]
            return M("이차함수 <b>y = %s + k</b>의 그래프가 x축과 %s 때, 상수 k의 조건은?" % (px([1, b, 0]), nm), ok, [x % neg(k0) for x in ("k &lt; %s", "k = %s", "k &gt; %s", "k ≥ %s") if x % neg(k0) != ok],
                     "D = %d − 4k의 부호로 판단해요. <b>%s</b>" % (b * b, ok))
        a, b, c = 1, R.randint(-5, 5), R.randint(-5, 5)
        m, n = R.randint(-4, 4), R.randint(-6, 6)
        D = (b - m) ** 2 - 4 * (c - n)
        if how == "line":
            ok = "서로 다른 두 점에서 만나요" if D > 0 else ("접해요" if D == 0 else "만나지 않아요")
            return M("이차함수 y = %s의 그래프와 직선 y = %s의 위치 관계는?" % (px([1, b, c]), px([m, n])), ok, [x for x in ("서로 다른 두 점에서 만나요", "접해요", "만나지 않아요", "세 점에서 만나요") if x != ok],
                     "%s = %s, 즉 %s = 0의 판별식 D = %s. <b>%s</b>" % (px([1, b, c]), px([m, n]), px([1, b - m, c - n]), neg(D), ok))
        bb = nz(-6, 6)
        m = nz(-4, 4)
        if bb == m:
            return None
        # x² + bb x + k = m x + 0  → x² + (bb − m)x + k = 0 접 → k = (bb − m)²/4
        k = Fr((bb - m) ** 2, 4)
        return N("이차함수 y = %s + k의 그래프가 직선 y = %s에 접할 때, 상수 k의 값은?" % (px([1, bb, 0]), px([m, 0])), k, [Fr((bb + m) ** 2, 4), (bb - m) ** 2, -k, k + 1],
                 "%s + k = %s에서 %s + k = 0의 D = 0 → k = <b>%s</b>" % (px([1, bb, 0]), px([m, 0]), px([1, bb - m, 0]), neg(k)))
    return mk


def mm_main(kinds=("std", "range", "word", "find")):
    def mk():
        how = R.choice(kinds)
        a = R.choice([1, -1, 2, -2])
        p, q = R.randint(-4, 4), R.randint(-8, 8)
        f = [a, -2 * a * p, a * p * p + q]
        if how == "std":
            k = "최솟값" if a > 0 else "최댓값"
            return N("이차함수 <b>y = %s</b>의 %s은?" % (px(f), k), q, [-q, f[2], p, q + a], "y = %s(x %s %d)² %s %d로 고치면 꼭짓점의 y좌표가 %s이에요. <b>%s</b>" % (neg(a) if abs(a) != 1 else ("" if a == 1 else "−"), "−" if p >= 0 else "+", abs(p), "+" if q >= 0 else "−", abs(q), k, neg(q)))
        if how == "range":
            a = R.choice([1, -1, 2, -2])
            p, q = R.randint(-3, 3), R.randint(-6, 6)
            f = [a, -2 * a * p, a * p * p + q]
            lo = p - R.randint(-2, 3)
            hi = lo + R.randint(2, 5)
            F = lambda x: a * (x - p) ** 2 + q
            vals = [F(x) for x in range(lo, hi + 1)]
            k = R.choice(["max", "min"])
            v = max(vals) if k == "max" else min(vals)
            inside = lo <= p <= hi
            w = W(q, F(lo), F(hi), min(vals) if k == "max" else max(vals), F(lo + 1), F(hi - 1), -v, v + abs(a))
            return N("%s ≤ x ≤ %s에서 이차함수 <b>y = %s</b>의 %s은?" % (neg(lo), neg(hi), px(f), "최댓값" if k == "max" else "최솟값"), v, w,
                     ("꼭짓점의 x좌표 %s가 범위 안에 있으므로 꼭짓점의 y좌표 %s와 양 끝값 %s, %s를 비교해요. <b>%s</b>" % (neg(p), neg(q), neg(F(lo)), neg(F(hi)), neg(v))) if inside else
                     ("꼭짓점의 x좌표 %s가 범위 밖에 있으므로 양 끝값 %s, %s를 비교해요. <b>%s</b>" % (neg(p), neg(F(lo)), neg(F(hi)), neg(v))))
        if how == "word":
            k = R.choice(["rect", "fence", "sum", "ball", "price"])
            if k == "rect":
                L = R.choice([12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 60])
                v = (L // 4) ** 2
                return N("둘레의 길이가 %d m인 직사각형 모양의 꽃밭을 만들려고 해요. 꽃밭의 넓이의 최댓값은?" % L, v, [L * L // 8, (L // 2) ** 2, v - 1, L // 4 * (L // 4 + 1)], "가로 x m이면 넓이 x(%d − x)는 x = %d일 때 최대. <b>%d m²</b>" % (L // 2, L // 4, v), f=lambda t: "%s m²" % neg(t))
            if k == "fence":
                L = R.choice([8, 12, 16, 20, 24, 28, 32, 36, 40, 48])
                v = L * L // 8
                return N("길이 %d m인 철망으로 벽에 붙은 직사각형 울타리(벽 쪽에는 철망을 두르지 않음)를 만들 때, 넓이의 최댓값은?" % L, v, [(L // 4) ** 2, L * L // 4, v + L, v - L // 4], "벽과 수직인 변을 x m라 하면 x(%d − 2x)는 x = %s일 때 최대. <b>%d m²</b>" % (L, neg(Fr(L, 4)), v),
                         f=lambda t: "%s m²" % neg(t))
            if k == "sum":
                S = R.choice([6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30])
                v = (S // 2) ** 2
                return N("합이 %d인 두 실수의 곱의 최댓값은?" % S, v, [S * S, S * S // 2, v - 1, S], "한 수를 x라 하면 x(%d − x) = −(x − %d)² + %d. <b>%d</b>" % (S, S // 2, v, v))
            if k == "ball":
                v0 = R.choice([10, 20, 30, 40])
                h0 = R.choice([0, 5, 10, 15, 20])
                t = Fr(v0, 10)
                hmax = h0 + Fr(v0 * v0, 20)
                return N("지면에서 %s m 높이에서 쏘아 올린 공의 t초 후의 높이가 h = −5t² + %dt + %d (m)일 때, 공의 최고 높이는?" % (h0, v0, h0) if h0 else "지면에서 쏘아 올린 공의 t초 후의 높이가 h = −5t² + %dt (m)일 때, 공의 최고 높이는?" % v0,
                         hmax, [h0 + Fr(v0 * v0, 10), Fr(v0 * v0, 20), t, hmax + 5], "h = −5(t − %s)² + %s이므로 t = %s일 때 최고. <b>%s m</b>" % (neg(t), neg(hmax), neg(t), neg(hmax)), f=lambda x: "%s m" % neg(x))
            p0 = R.choice([1000, 2000, 3000, 5000])
            n0 = R.choice([100, 200, 300, 400])
            d = R.choice([100, 200])
            m = R.choice([5, 10, 20])
            # 가격을 d원 올릴 때마다 m개 덜 팔림. x번 올리면 (p0 + dx)(n0 − mx)
            # 최대: x = (n0 d − m p0)/(2 m d)
            x = Fr(n0 * d - m * p0, 2 * m * d)
            if x <= 0 or x.denominator != 1:
                return None
            best = p0 + d * x
            return N("어떤 물건을 %s원에 팔면 하루에 %d개가 팔리고, 값을 %d원 올릴 때마다 %d개씩 덜 팔려요. 하루 판매 금액이 가장 클 때 물건의 값은?" % (num(p0), n0, d, m), best, [p0, best + d, best - d, p0 + d * n0 // m // 2 if p0 + d * n0 // m // 2 != best else best + 2 * d],
                     "x번 올리면 (%s + %dx)(%d − %dx)이고, x = %s일 때 최대. <b>%s원</b>" % (num(p0), d, n0, m, neg(x), num(best)), f=lambda t: "%s원" % num(t))
        c = R.randint(-5, 5)
        b = R.choice([-6, -4, -2, 2, 4, 6])
        v = c - b * b // 4
        return N("이차함수 y = x² %s %dx + k의 최솟값이 %s일 때, 상수 k의 값은?" % ("+" if b > 0 else "−", abs(b), neg(c)), c + b * b // 4, [c - b * b // 4, c + b * b // 2, -c, c + b], "y = (x %s %d)² + k − %d → k − %d = %s. <b>k = %s</b>" % ("+" if b > 0 else "−", abs(b) // 2, b * b // 4, b * b // 4, neg(c), neg(c + b * b // 4)))
    return mk


# ------------------------------------------------------------------ 삼차·사차방정식, 연립이차방정식
def h_main(kinds=("cubic", "fact", "biq", "omega", "other")):
    def mk():
        how = R.choice(kinds)
        if how == "cubic":
            r1, r2, r3 = R.sample([-4, -3, -2, -1, 0, 1, 2, 3, 4, 5], 3)
            P = pmul(pmul([1, -r1], [1, -r2]), [1, -r3])
            ok = roots(r1, r2, r3)
            return M("삼차방정식 <b>%s = 0</b>을 풀면?" % px(P), ok, [roots(-r1, -r2, -r3), roots(r1, r2, -r3), roots(r1, -r2, r3)], "인수정리로 한 근을 찾고 조립제법으로 나누어요. <b>%s</b>" % ok)
        if how == "fact":
            r = nz(-3, 3)
            b = R.randint(1, 5)
            # (x − r)(x² + b) = 0 → x = r, ±√b i
            P = pmul([1, -r], [1, 0, b])
            ok = "x = %s 또는 x = ±%si" % (neg(r), surd(1, b) if b > 1 else "")
            ok = ok.replace("±i", "±i")
            return M("삼차방정식 <b>%s = 0</b>의 근은?" % px(P), ok, ["x = %s 또는 x = ±%s" % (neg(r), surd(1, b)), "x = %s 또는 x = ±%si" % (neg(-r), surd(1, b) if b > 1 else ""), "x = %s" % neg(r)],
                     "(x %s %d)(x² + %d) = 0. <b>%s</b>" % ("−" if r > 0 else "+", abs(r), b, ok))
        if how == "biq":
            a, b = sorted(R.sample([-9, -4, -1, 1, 2, 3, 4, 5, 9, 16], 2))
            P = pmul([1, 0, -a], [1, 0, -b])
            rt = lambda t: "x = ±%s" % surd(1, t) if t > 0 else "x = ±%si" % (surd(1, -t) if t != -1 else "")
            ok = "%s 또는 %s" % (rt(a), rt(b))
            w = ["%s 또는 %s" % (rt(-a), rt(-b)), "x² = %s 또는 x² = %s" % (neg(a), neg(b)), "%s 또는 %s" % (rt(a * a) if a * a < 300 else rt(a + 1), rt(b * b) if b * b < 300 else rt(b + 1)), "%s 또는 %s" % (rt(a), rt(-b))]
            return M("사차방정식 <b>%s = 0</b>을 풀면?" % px(P), ok, [x for x in w if x != ok],
                     "x² = t로 놓으면 (t %s %d)(t %s %d) = 0, t = %s 또는 t = %s. <b>%s</b>" % ("−" if a > 0 else "+", abs(a), "−" if b > 0 else "+", abs(b), neg(a), neg(b), ok))
        if how == "omega":
            n = R.randint(4, 40)
            k = R.choice(["pow", "sum"])
            if k == "pow":
                ok = ["1", "ω", "ω²"][n % 3]
                return M("방정식 x³ = 1의 한 허근을 ω라 할 때, <b>ω<sup>%d</sup></b>의 값은?" % n, ok, [x for x in ("1", "ω", "ω²", "−1") if x != ok], "ω³ = 1이므로 %d을 3으로 나눈 나머지 %d를 봐요. <b>%s</b>" % (n, n % 3, ok))
            return M("방정식 x³ = 1의 한 허근을 ω라 할 때, <b>ω² + ω + 1</b>의 값은?", "0", ["1", "−1", "3"], "x³ − 1 = (x − 1)(x² + x + 1)이므로 ω² + ω + 1 = <b>0</b>") if R.random() < 0.15 else None
        a = R.randint(-4, 4)
        r1, r2 = R.sample([-3, -2, -1, 1, 2, 3], 2)
        if a in (r1, r2):
            return None
        P = pmul(pmul([1, -a], [1, -r1]), [1, -r2])
        # x = a 가 근일 때 나머지 두 근의 합
        return N("삼차방정식 <b>%s = 0</b>의 한 근이 %s일 때, 나머지 두 근의 합은?" % (px(P), neg(a)), r1 + r2, [r1 * r2, -(r1 + r2), r1 + r2 + a, a], "조립제법으로 나누면 %s = 0이 남아요. <b>%s</b>" % (px(pmul([1, -r1], [1, -r2])), neg(r1 + r2)))
    return mk


import re


def hy(r):
    if r:
        f = lambda t: re.sub(r"(?<![\w])-(\d)", "−\\1", t)
        r = dict(r, q=f(r["q"]), c=[f(c) for c in r["c"]], e=f(r["e"]))
    return r


def s_main(kinds=("lin", "fact", "word")):
    def mk():
        how = R.choice(kinds)
        if how == "lin":
            x, y = R.randint(-7, 7), R.randint(-7, 7)
            s = x + y
            q = x * x + y * y
            x2, y2 = s - x, s - y  # 대칭 해 (y, x)
            sols = sorted({(x, y), (y, x)})
            ok = " 또는 ".join("x = %s, y = %s" % (neg(a), neg(b)) for a, b in sols)
            if x == y:
                return None
            return M("연립방정식 <span class='sys'>x + y = %s<br>x² + y² = %s</span> 의 해는?" % (neg(s), neg(q)), ok, ["x = %s, y = %s" % (neg(x), neg(y)), " 또는 ".join("x = %s, y = %s" % (neg(-a), neg(-b)) for a, b in sols),
                                                                                                       "x = %s, y = %s 또는 x = %s, y = %s" % (neg(x), neg(-y), neg(-y), neg(x))],
                     "y = %s − x를 대입해 이차방정식을 풀어요. <b>%s</b>" % (neg(s), ok))
        if how == "fact":
            k = R.choice([2, 3, 4])
            y = R.randint(1, 5)
            case = R.choice(["k", "1"])
            x = k * y if case == "k" else y
            q = x * x + y * y
            ok = "x = %d, y = %d 또는 x = %d, y = %d" % (-x, -y, x, y)
            cond = "x = %dy" % k if case == "k" else "x = y"
            return hy(M("연립방정식 <span class='sys'>x² − %dxy + %dy² = 0<br>x² + y² = %d</span> 의 해 중 %s인 경우의 해는?" % (k + 1, k, q, cond), ok,
                     ["x = %d, y = %d" % (x, y), "x = %d, y = %d 또는 x = %d, y = %d" % (-y, -x, y, x) if x != y else "x = %d, y = %d 또는 x = %d, y = %d" % (-x, y, x, -y), "x = %d, y = %d 또는 x = %d, y = %d" % (x, -y, -x, y) if x != y else "x = %d, y = %d" % (-x, -y)],
                     "(x − y)(x − %dy) = 0에서 %s를 대입하면 %dy² = %d. <b>%s</b>" % (k, cond, (k * k + 1) if case == "k" else 2, q, ok)))
        a, b = R.sample(range(3, 13), 2)
        a, b = max(a, b), min(a, b)
        return M("둘레의 길이가 %d cm이고 넓이가 %d cm²인 직사각형의 긴 변의 길이는?" % (2 * (a + b), a * b), "%d cm" % a, ["%d cm" % b, "%d cm" % (a + b), "%d cm" % (a + 1)], "x + y = %d, xy = %d → t² − %dt + %d = 0. <b>%d cm</b>" % (a + b, a * b, a + b, a * b, a))
    return mk


# ------------------------------------------------------------------ 부등식
OPS = {"<": "&lt;", ">": "&gt;", "≤": "≤", "≥": "≥"}


def l_main(kinds=("sys", "abs1", "abs2", "count", "absx")):
    def mk():
        how = R.choice(kinds)
        if how == "sys":
            a, b = sorted(R.sample(range(-6, 8), 2))
            # 2x − 2a > 0 꼴로 숨기기
            p, q = R.choice([2, 3]), R.choice([1, 2, 3])
            ok = "%s &lt; x ≤ %s" % (neg(a), neg(b))
            return M("연립부등식 <span class='sys'>%s &gt; %s<br>%s ≤ %s</span> 의 해는?" % (px([p, 0]), neg(p * a), px([q, 0]), neg(q * b)), ok,
                     ["%s ≤ x &lt; %s" % (neg(a), neg(b)), "x &lt; %s 또는 x ≥ %s" % (neg(a), neg(b)), "%s &lt; x &lt; %s" % (neg(a), neg(b)), "%s &lt; x ≤ %s" % (neg(-b), neg(-a))],
                     "각각 풀면 x &gt; %s, x ≤ %s. 공통 범위 <b>%s</b>" % (neg(a), neg(b), ok))
        a = R.randint(-5, 5)
        b = R.randint(1, 6)
        if how == "abs1":
            ok = "%s &lt; x &lt; %s" % (neg(a - b), neg(a + b))
            return M("부등식 <b>|x %s %d| &lt; %d</b>의 해는?" % ("−" if a >= 0 else "+", abs(a), b), ok, ["x &lt; %s 또는 x &gt; %s" % (neg(a - b), neg(a + b)), "%s &lt; x &lt; %s" % (neg(-a - b), neg(-a + b)), "x &lt; %s" % neg(a + b)],
                     "−%d &lt; x %s %d &lt; %d. <b>%s</b>" % (b, "−" if a >= 0 else "+", abs(a), b, ok))
        if how == "abs2":
            ok = "x ≤ %s 또는 x ≥ %s" % (neg(a - b), neg(a + b))
            return M("부등식 <b>|x %s %d| ≥ %d</b>의 해는?" % ("−" if a >= 0 else "+", abs(a), b), ok, ["%s ≤ x ≤ %s" % (neg(a - b), neg(a + b)), "x ≤ %s 또는 x ≥ %s" % (neg(-a - b), neg(-a + b)), "x ≥ %s" % neg(a + b)],
                     "x %s %d ≤ −%d 또는 x %s %d ≥ %d. <b>%s</b>" % ("−" if a >= 0 else "+", abs(a), b, "−" if a >= 0 else "+", abs(a), b, ok))
        if how == "count":
            c = 2 * b - 1
            return N("부등식 <b>|x %s %d| &lt; %d</b>를 만족하는 정수 x의 개수는?" % ("−" if a >= 0 else "+", abs(a), b), c, [c + 2, 2 * b, b, c - 1 if c > 1 else c + 1], "%s &lt; x &lt; %s인 정수는 <b>%d개</b>" % (neg(a - b), neg(a + b), c), f=lambda v: "%s개" % neg(v))
        p = R.randint(1, 4)
        k = R.randint(p + 1, p + 6)
        # |x − p| + |x| ... simpler: |2x − 2p| ≤ x + k?   use |x − p| ≤ 2x − ... keep: |x| + |x − 2p| < 2k?  → p−k < x < p+k
        ok = "%s &lt; x &lt; %s" % (neg(p - k), neg(p + k))
        if k <= p:
            return None
        return M("부등식 <b>|x| + |x − %d| &lt; %d</b>의 해는?" % (2 * p, 2 * k), ok, ["%s &lt; x &lt; %s" % (neg(-k), neg(k)), "x &lt; %s 또는 x &gt; %s" % (neg(p - k), neg(p + k)), "0 &lt; x &lt; %d" % (2 * p)],
                 "x &lt; 0, 0 ≤ x &lt; %d, x ≥ %d로 나누어 풀어요. <b>%s</b>" % (2 * p, 2 * p, ok))
    return mk


def qi_main(kinds=("lt", "gt", "all", "sys", "k")):
    def mk():
        how = R.choice(kinds)
        p, q = sorted(R.sample(range(-6, 7), 2))
        f = pmul([1, -p], [1, -q])
        if how == "lt":
            ok = "%s &lt; x &lt; %s" % (neg(p), neg(q))
            return M("이차부등식 <b>%s &lt; 0</b>의 해는?" % px(f), ok, ["x &lt; %s 또는 x &gt; %s" % (neg(p), neg(q)), "%s &lt; x &lt; %s" % (neg(-q), neg(-p)), "%s ≤ x ≤ %s" % (neg(p), neg(q))], "그래프가 x축 아래에 있는 범위예요. <b>%s</b>" % ok)
        if how == "gt":
            ok = "x ≤ %s 또는 x ≥ %s" % (neg(p), neg(q))
            return M("이차부등식 <b>%s ≥ 0</b>의 해는?" % px(f), ok, ["%s ≤ x ≤ %s" % (neg(p), neg(q)), "x ≤ %s 또는 x ≥ %s" % (neg(-q), neg(-p)), "x &lt; %s 또는 x &gt; %s" % (neg(p), neg(q))], "그래프가 x축보다 위에 있거나 x축과 만나는 범위예요. <b>%s</b>" % ok)
        if how == "all":
            b, c = R.randint(-5, 5), R.randint(-3, 9)
            D = b * b - 4 * c
            kind = R.choice(["gt", "lt"])
            if kind == "gt":
                ok = "모든 실수" if D < 0 else ("x ≠ %s인 모든 실수" % neg(Fr(-b, 2)) if D == 0 else None)
            else:
                ok = "해가 없어요" if D <= 0 else None
            if ok is None:
                return None
            return M("이차부등식 <b>%s %s 0</b>의 해는?" % (px([1, b, c]), "&gt;" if kind == "gt" else "&lt;"), ok, [x for x in ("모든 실수", "해가 없어요", "x = %s" % neg(Fr(-b, 2)), "x ≠ %s인 모든 실수" % neg(Fr(-b, 2))) if x != ok],
                     "D = %s이므로 그래프가 %s. <b>%s</b>" % (neg(D), "x축과 만나지 않아요" if D < 0 else "x축에 접해요", ok))
        if how == "sys":
            a = R.randint(p + 1, q + 3) if q - p > 1 else None
            if a is None or a == q:
                return None
            # p<x<q 와 x ≥ a
            lo, hi = max(p, a), q
            if lo >= hi:
                return None
            ok = "%s ≤ x &lt; %s" % (neg(lo), neg(hi)) if a > p else "%s &lt; x &lt; %s" % (neg(p), neg(q))
            return M("연립부등식 <span class='sys'>%s &lt; 0<br>x ≥ %s</span> 의 해는?" % (px(f), neg(a)), ok, ["%s &lt; x &lt; %s" % (neg(p), neg(q)), "%s ≤ x &lt; %s" % (neg(p), neg(a)), "x ≥ %s" % neg(a)],
                     "%s &lt; x &lt; %s와 x ≥ %s의 공통 범위. <b>%s</b>" % (neg(p), neg(q), neg(a), ok))
        b = nz(-10, 10)
        k0 = Fr(b * b, 4)
        return M("모든 실수 x에 대하여 이차부등식 <b>%s + k &gt; 0</b>이 성립할 때, 상수 k의 값의 범위는?" % px([1, b, 0]), "k &gt; %s" % neg(k0), ["k ≥ %s" % neg(k0), "k &lt; %s" % neg(k0), "k &gt; %s" % neg(b * b)],
                 "D = %d − 4k &lt; 0. <b>k &gt; %s</b>" % (b * b, neg(k0)))
    return mk


# ------------------------------------------------------------------ 경우의 수
def n_main(kinds=("sumlaw", "prodlaw", "divisors", "path", "coins")):
    def mk():
        how = R.choice(kinds)
        if how == "sumlaw":
            s = R.randint(3, 10)
            k = R.choice([2, 3, 4, 5])
            c = sum(1 for i in range(1, 7) for j in range(1, 7) if (i + j) in (s, s + k) )
            if s + k > 12 or k == 0:
                return None
            return N("서로 다른 두 개의 주사위를 던질 때, 나오는 눈의 수의 합이 %d 또는 %d인 경우의 수는?" % (s, s + k), c, [c + 1, c - 1, sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s) * sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s + k), 2 * s],
                     "두 사건은 동시에 일어나지 않으므로 합의 법칙. <b>%d</b>" % c)
        if how == "prodlaw":
            a, b, c = R.randint(2, 5), R.randint(2, 5), R.randint(2, 4)
            return N("(a + b)(x + y + z)를 전개할 때와 같은 방법으로, (%s)(%s)(%s)를 전개하면 서로 다른 항은 몇 개일까요?" % (" + ".join("abcde"[:a]), " + ".join("pqrst"[:b]), " + ".join("xyzw"[:c])), a * b * c, [a + b + c, a * b + c, a * b * c - 1, a * b],
                     "각 괄호에서 하나씩 골라 곱하므로 %d × %d × %d = <b>%d</b>" % (a, b, c, a * b * c), f=lambda v: "%s개" % neg(v))
        if how == "divisors":
            p = R.choice([2, 3])
            e = {2: R.randint(1, 5), 3: R.randint(1, 3)}
            e2, e3 = R.randint(1, 5), R.randint(1, 3)
            e5 = R.randint(0, 2)
            n = 2 ** e2 * 3 ** e3 * 5 ** e5
            c = (e2 + 1) * (e3 + 1) * (e5 + 1)
            return N("<b>%s</b>의 양의 약수의 개수는?" % num(n), c, [e2 * e3 * max(e5, 1), (e2 + e3 + e5) + 1, c - 1, c * 2], "%s = 2%s × 3%s%s. (%d + 1)(%d + 1)%s = <b>%d</b>" % (num(n), sup_(e2), sup_(e3), (" × 5" + sup_(e5)) if e5 else "", e2, e3, "(%d + 1)" % e5 if e5 else "", c),
                     f=lambda v: "%s개" % neg(v))
        if how == "path":
            a, b, c = R.randint(2, 4), R.randint(2, 4), R.randint(1, 3)
            d = R.randint(1, 3)
            v = a * b + c * d
            return N("A에서 B로 가는 길이 %d가지, B에서 C로 가는 길이 %d가지, A에서 D로 가는 길이 %d가지, D에서 C로 가는 길이 %d가지예요. A에서 C로 가는 경우의 수는? (B와 D는 이어지지 않아요)" % (a, b, c, d), v,
                     [a * b * c * d, a + b + c + d, a * b + c, v + 1], "A→B→C %d가지 + A→D→C %d가지 = <b>%d</b>" % (a * b, c * d, v))
        a, b, c = R.randint(1, 4), R.randint(1, 3), R.randint(1, 3)
        v = (a + 1) * (b + 1) * (c + 1) - 1
        return N("100원짜리 동전 %d개, 50원짜리 동전 %d개, 10원짜리 동전 %d개의 일부 또는 전부를 써서 지불하는 방법의 수는? (0원은 제외)" % (a, b, c), v, [v + 1, a * b * c, (a + 1) * (b + 1) * (c + 1) - 2, a + b + c], "(%d + 1)(%d + 1)(%d + 1) − 1 = <b>%d</b>" % (a, b, c, v), f=lambda t: "%s가지" % neg(t))
    return mk


def sup_(e):
    return "⁰¹²³⁴⁵⁶⁷⁸⁹"[e] if e < 10 else str(e)


def perm_main(kinds=("npr", "line", "adj", "nonadj", "num", "eq")):
    def mk():
        how = R.choice(kinds)
        if how == "npr":
            n = R.randint(4, 9)
            r = R.randint(2, min(4, n))
            v = math.perm(n, r)
            return N("<b><sub>%d</sub>P<sub>%d</sub></b>의 값은?" % (n, r), v, [math.comb(n, r), n ** r, v // r, math.perm(n, r - 1)], "%s = <b>%s</b>" % (" × ".join(str(n - i) for i in range(r)), num(v)))
        if how == "line":
            n = R.randint(4, 12)
            r = R.randint(2, min(4, n - 1))
            return N("%d명의 학생 중 %d명을 뽑아 한 줄로 세우는 경우의 수는?" % (n, r), math.perm(n, r), [math.comb(n, r), n ** r, math.factorial(n), math.perm(n, r) // 2], "<sub>%d</sub>P<sub>%d</sub> = <b>%s</b>" % (n, r, num(math.perm(n, r))))
        if how == "adj":
            k = R.choice(["grp", "grp", "two", "ends", "first"])
            if k == "grp":
                g, b = R.randint(2, 4), R.randint(2, 5)
                v = math.factorial(b + 1) * math.factorial(g)
                return N("남학생 %d명, 여학생 %d명이 한 줄로 설 때, 여학생끼리 모두 이웃하여 서는 경우의 수는?" % (b, g), v, [math.factorial(b + g), math.factorial(b + 1), v * 2, math.factorial(b) * math.factorial(g), math.factorial(b + 1) * g],
                         "여학생 %d명을 한 묶음으로 보면 (%d + 1)! × %d! = <b>%s</b>" % (g, b, g, num(v)))
            n = R.randint(4, 8)
            if k == "two":
                v = math.factorial(n - 1) * 2
                return N("%d명이 한 줄로 설 때, 특정한 두 사람 A, B가 이웃하여 서는 경우의 수는?" % n, v, [math.factorial(n - 1), math.factorial(n), math.factorial(n) - v, v * 2], "A, B를 한 묶음으로 보면 %d! × 2! = <b>%s</b>" % (n - 1, num(v)))
            if k == "ends":
                v = math.factorial(n - 2) * 2
                return N("%d명이 한 줄로 설 때, 특정한 두 사람 A, B가 양 끝에 서는 경우의 수는?" % n, v, [math.factorial(n - 2), math.factorial(n - 1) * 2, math.factorial(n), v * 3], "양 끝에 A, B를 세우는 2가지, 가운데 %d명을 세우는 %d!가지. <b>%s</b>" % (n - 2, n - 2, num(v)))
            v = math.factorial(n - 1)
            return N("%d명이 한 줄로 설 때, A가 맨 앞에 서는 경우의 수는?" % n, v, [math.factorial(n), math.factorial(n - 2), n - 1, v * 2], "A를 맨 앞에 세우고 나머지 %d명을 세워요. %d! = <b>%s</b>" % (n - 1, n - 1, num(v)))
        if how == "nonadj":
            k = R.choice(["grp", "grp", "two", "alt"])
            if k == "grp":
                b, g = R.randint(2, 6), R.randint(2, 4)
                if g > b + 1:
                    return None
                v = math.factorial(b) * math.perm(b + 1, g)
                return N("남학생 %d명, 여학생 %d명이 한 줄로 설 때, 여학생끼리 이웃하지 않게 서는 경우의 수는?" % (b, g), v, [math.factorial(b + g) - math.factorial(b + 1) * math.factorial(g), math.factorial(b) * math.comb(b + 1, g), math.factorial(b + g), v * 2],
                         "남학생을 먼저 세우고(%d!) 사이와 양 끝 %d자리에 여학생을 세워요(<sub>%d</sub>P<sub>%d</sub>). <b>%s</b>" % (b, b + 1, b + 1, g, num(v)))
            if k == "two":
                n = R.randint(4, 8)
                v = math.factorial(n) - 2 * math.factorial(n - 1)
                return N("%d명이 한 줄로 설 때, 특정한 두 사람 A, B가 이웃하지 않게 서는 경우의 수는?" % n, v, [2 * math.factorial(n - 1), math.factorial(n), math.factorial(n) - math.factorial(n - 1), v // 2],
                         "전체 %d!에서 이웃하는 경우 %d! × 2를 빼요. <b>%s</b>" % (n, n - 1, num(v)))
            n = R.randint(2, 5)
            v = 2 * math.factorial(n) ** 2
            return N("남학생 %d명과 여학생 %d명이 남녀 교대로 한 줄로 서는 경우의 수는?" % (n, n), v, [math.factorial(n) ** 2, math.factorial(2 * n), 2 * math.factorial(n), v * 2], "남녀남… 또는 여남여… 2가지 × %d! × %d! = <b>%s</b>" % (n, n, num(v)))
        if how == "num":
            n = R.randint(4, 7)
            r = R.choice([3, 4]) if n >= 5 else 3
            rn = "세" if r == 3 else "네"
            k = R.choice(["zero", "even", "odd"])
            if k == "zero":
                v = (n - 1) * math.perm(n - 1, r - 1)
                return N("%s의 숫자 중 서로 다른 %d개를 사용하여 만들 수 있는 %s 자리 자연수의 개수는?" % (", ".join(str(i) for i in range(n)), r, rn), v, [math.perm(n, r), n ** r, v + math.perm(n - 1, r - 1), math.perm(n - 1, r)],
                         "맨 앞자리에는 0이 올 수 없어요. %d × <sub>%d</sub>P<sub>%d</sub> = <b>%s</b>" % (n - 1, n - 1, r - 1, num(v)), f=lambda t: "%s개" % num(t))
            par_ = [d for d in range(1, n + 1) if d % 2 == (0 if k == "even" else 1)]
            v = len(par_) * math.perm(n - 1, r - 1)
            return N("%s의 숫자 중 서로 다른 %d개를 사용하여 만들 수 있는 %s 자리 %s의 개수는?" % (", ".join(str(i) for i in range(1, n + 1)), r, rn, "짝수" if k == "even" else "홀수"), v, [math.perm(n, r) - v if math.perm(n, r) - v != v else v + 1, math.perm(n, r), len(par_) * n ** (r - 1), v * 2],
                     "일의 자리에 %s %d가지, 나머지 자리 <sub>%d</sub>P<sub>%d</sub>. <b>%s</b>" % ("짝수" if k == "even" else "홀수", len(par_), n - 1, r - 1, num(v)), f=lambda t: "%s개" % num(t))
        n = R.randint(5, 9)
        v = n * (n - 1)
        return N("<sub>n</sub>P<sub>2</sub> = %d를 만족하는 자연수 n의 값은?" % v, n, [n - 1, n + 1, v // 2, n * 2], "n(n − 1) = %d → <b>n = %d</b>" % (v, n))
    return mk


def comb_main(kinds=("ncr", "pick", "both", "atleast", "geo", "eq")):
    def mk():
        how = R.choice(kinds)
        if how == "ncr":
            n = R.randint(5, 15)
            r = R.randint(2, 4)
            v = math.comb(n, r)
            return N("<b><sub>%d</sub>C<sub>%d</sub></b>의 값은?" % (n, r), v, [math.perm(n, r), v * 2, math.comb(n, r - 1), n * r], "<sub>%d</sub>P<sub>%d</sub> ÷ %d! = <b>%s</b>" % (n, r, r, num(v)))
        if how == "pick":
            n = R.randint(6, 12)
            r = R.randint(2, 4)
            v = math.comb(n, r)
            return N("%d명 중 대표 %d명을 뽑는 경우의 수는?" % (n, r), v, [math.perm(n, r), n * r, v - 1, n ** r if n ** r < 2000 else v * 3], "순서가 없으므로 <sub>%d</sub>C<sub>%d</sub> = <b>%s</b>" % (n, r, num(v)))
        if how == "both":
            b, g = R.randint(3, 7), R.randint(3, 6)
            rb, rg = R.randint(1, 3), R.randint(1, 3)
            v = math.comb(b, rb) * math.comb(g, rg)
            return N("남학생 %d명, 여학생 %d명 중 남학생 %d명, 여학생 %d명을 뽑는 경우의 수는?" % (b, g, rb, rg), v, [math.comb(b, rb) + math.comb(g, rg), math.comb(b + g, rb + rg), v * 2, math.perm(b, rb) * math.perm(g, rg)],
                     "<sub>%d</sub>C<sub>%d</sub> × <sub>%d</sub>C<sub>%d</sub> = <b>%s</b>" % (b, rb, g, rg, num(v)))
        if how == "atleast":
            b, g = R.randint(3, 6), R.randint(3, 6)
            r = R.randint(2, 4)
            v = math.comb(b + g, r) - math.comb(b, r)
            return N("남학생 %d명, 여학생 %d명 중 %d명을 뽑을 때, 여학생이 적어도 한 명 포함되는 경우의 수는?" % (b, g, r), v, [math.comb(b + g, r), math.comb(g, r), g * math.comb(b + g - 1, r - 1), v + 1],
                     "(전체) − (남학생만 뽑는 경우) = <sub>%d</sub>C<sub>%d</sub> − <sub>%d</sub>C<sub>%d</sub> = <b>%s</b>" % (b + g, r, b, r, num(v)))
        if how == "geo":
            n = R.randint(4, 12)
            k = R.choice(["line", "tri", "diag"])
            if k == "line":
                v = math.comb(n, 2)
                return N("원 위의 서로 다른 %d개의 점 중 두 점을 이어 만들 수 있는 선분의 개수는?" % n, v, [math.perm(n, 2), n, v - n, v + n], "<sub>%d</sub>C<sub>2</sub> = <b>%d</b>" % (n, v), f=lambda t: "%s개" % neg(t))
            if k == "tri":
                v = math.comb(n, 3)
                return N("원 위의 서로 다른 %d개의 점 중 세 점을 꼭짓점으로 하는 삼각형의 개수는?" % n, v, [math.perm(n, 3), math.comb(n, 2), v * 2, n * 3], "<sub>%d</sub>C<sub>3</sub> = <b>%d</b>" % (n, v), f=lambda t: "%s개" % neg(t))
            v = math.comb(n, 2) - n
            return N("%s각형의 대각선의 개수는?" % kn(n), v, [math.comb(n, 2), n * (n - 3), v + n // 2, n - 3], "<sub>%d</sub>C<sub>2</sub> − %d = <b>%d</b>" % (n, n, v), f=lambda t: "%s개" % neg(t))
        n = R.randint(5, 10)
        v = math.comb(n, 2)
        return N("<sub>n</sub>C<sub>2</sub> = %d를 만족하는 자연수 n의 값은?" % v, n, [n - 1, n + 1, v // 2, 2 * n], "n(n − 1) ÷ 2 = %d → <b>n = %d</b>" % (v, n))
    return mk


_D = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


def kn(n):
    t, o = divmod(n, 10)
    return ("" if t == 0 else ("" if t == 1 else _D[t]) + "십") + _D[o]


def pc_concept():
    F_ = [("<sub>n</sub>P<sub>r</sub>과 <sub>n</sub>C<sub>r</sub>의 관계로 옳은 것은?", "<sub>n</sub>P<sub>r</sub> = <sub>n</sub>C<sub>r</sub> × r!", ["<sub>n</sub>C<sub>r</sub> = <sub>n</sub>P<sub>r</sub> × r!", "<sub>n</sub>P<sub>r</sub> = <sub>n</sub>C<sub>r</sub>", "<sub>n</sub>P<sub>r</sub> = <sub>n</sub>C<sub>r</sub> + r"], "뽑은 r개를 일렬로 세우는 r!가지가 곱해져요."),
          ("0!의 값은?", "1", ["0", "정의되지 않아요", "−1"], "0! = <b>1</b>로 정해요."),
          ("<sub>n</sub>C<sub>r</sub>과 같은 값은?", "<sub>n</sub>C<sub>n−r</sub>", ["<sub>n</sub>C<sub>r−1</sub>", "<sub>n−1</sub>C<sub>r</sub>", "<sub>n</sub>P<sub>r</sub>"], "r개를 뽑는 것은 남길 n − r개를 고르는 것과 같아요."),
          ("<sub>n</sub>C<sub>r</sub> = <sub>n−1</sub>C<sub>r−1</sub> + □에서 □는?", "<sub>n−1</sub>C<sub>r</sub>", ["<sub>n</sub>C<sub>r−1</sub>", "<sub>n−1</sub>C<sub>r−1</sub>", "<sub>n+1</sub>C<sub>r</sub>"], "특정한 하나를 포함하는 경우와 포함하지 않는 경우로 나누어요."),
          ("<sub>n</sub>P<sub>n</sub>의 값은?", "n!", ["n", "1", "n²"], "n개를 모두 일렬로 세우는 경우예요."),
          ("순서를 생각하여 뽑는 것은?", "순열", ["조합", "합의 법칙", "여사건"], "<b>순열</b>은 순서를 생각해요.")]
    pool = F_[:]
    R.shuffle(pool)

    def mk():
        return M(*pool.pop()) if pool else None
    return mk


# ------------------------------------------------------------------ 행렬
def rmat(r=2, c=2, lo=-5, hi=6):
    return [[R.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def m_main(kinds=("entry", "size", "add", "scal", "mul", "power", "eq", "life")):
    def mk():
        how = R.choice(kinds)
        if how == "entry":
            r, c = R.choice([(2, 2), (2, 3), (3, 2), (3, 3)])
            A = rmat(r, c)
            i, j = R.randint(1, r), R.randint(1, c)
            v = A[i - 1][j - 1]
            alt = A[j - 1][i - 1] if j <= r and i <= c else None
            w = W(alt, A[0][0], A[-1][-1], sum(A[i - 1]), v + 1)
            return N("행렬 A = %s에서 (%d, %d) 성분은?" % (mx(A), i, j), v, [x for x in w if x != v], "%d행 %d열의 성분이에요. <b>%s</b>" % (i, j, neg(v)))
        if how == "size":
            r, c = R.choice([(2, 3), (3, 2), (1, 3), (3, 1), (2, 2)])
            A = rmat(r, c)
            ok = "%d × %d 행렬" % (r, c)
            return M("행렬 %s의 꼴은?" % mx(A), ok, [x for x in ("%d × %d 행렬" % (c, r), "%d × %d 행렬" % (r * c, 1), "%d × %d 행렬" % (r, r), "%d × %d 행렬" % (c, c)) if x != ok], "행이 %d개, 열이 %d개예요. <b>%s</b>" % (r, c, ok))
        A, B = rmat(), rmat()
        if how == "add":
            s = R.choice([1, -1])
            C = [[A[i][j] + s * B[i][j] for j in range(2)] for i in range(2)]
            Cw = [[A[i][j] - s * B[i][j] for j in range(2)] for i in range(2)]
            return M("A = %s, B = %s일 때, <b>A %s B</b>는?" % (mx(A), mx(B), "+" if s > 0 else "−"), mx(C), [mx(Cw), mx([[C[0][0], C[1][0]], [C[0][1], C[1][1]]]) if C[0][1] != C[1][0] else mx([[C[0][0] + 1, C[0][1]], C[1]]), mx(mm(A, B))],
                     "같은 위치의 성분끼리 계산해요. <b>%s</b>" % mx(C))
        if how == "scal":
            k, l = R.choice([2, 3, -1, -2]), R.choice([1, 2, -1, 3])
            C = [[k * A[i][j] + l * B[i][j] for j in range(2)] for i in range(2)]
            return M("A = %s, B = %s일 때, <b>%sA %s %sB</b>는?" % (mx(A), mx(B), neg(k) if abs(k) != 1 else ("−" if k < 0 else ""), "+" if l > 0 else "−", abs(l) if abs(l) != 1 else ""), mx(C),
                     [mx([[k * A[i][j] - l * B[i][j] for j in range(2)] for i in range(2)]), mx([[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]), mx([[k * A[i][j] + B[i][j] for j in range(2)] for i in range(2)])],
                     "각 성분에 실수를 곱한 뒤 더해요. <b>%s</b>" % mx(C))
        if how == "mul":
            k = R.choice(["2x2", "vec"])
            if k == "vec":
                v = [[R.randint(-4, 4)], [R.randint(-4, 4)]]
                C = mm(A, v)
                return M("<b>%s%s</b>를 계산하면?" % (mx(A), mx(v)), mx(C), [mx([[A[0][0] * v[0][0]], [A[1][1] * v[1][0]]]), mx(mm([[A[0][0], A[1][0]], [A[0][1], A[1][1]]], v)), mx([[C[0][0] + 1], [C[1][0]]])],
                         "(행) × (열)로 곱해 더해요. <b>%s</b>" % mx(C))
            C = mm(A, B)
            Cw = [[A[i][j] * B[i][j] for j in range(2)] for i in range(2)]
            return M("A = %s, B = %s일 때, <b>AB</b>는?" % (mx(A), mx(B)), mx(C), [mx(Cw), mx(mm(B, A)) if mm(B, A) != C else mx([[C[0][0] + 1, C[0][1]], C[1]]), mx([[C[0][0], C[1][0]], [C[0][1], C[1][1]]]) if C[0][1] != C[1][0] else mx([[C[0][0], C[0][1] - 1], C[1]])],
                     "AB의 (i, j) 성분 = A의 i행과 B의 j열의 곱의 합. <b>%s</b>" % mx(C))
        if how == "power":
            a = R.randint(1, 4)
            n = R.randint(2, 9)
            A2 = [[1, a], [0, 1]]
            C = [[1, a * n], [0, 1]]
            return M("A = %s일 때, <b>A<sup>%d</sup></b>은?" % (mx(A2), n), mx(C), [mx([[1, a ** n], [0, 1]]), mx([[n, a * n], [0, n]]), mx([[1, a + n], [0, 1]])], "A², A³을 구해 보면 (1, 2) 성분이 %d씩 늘어요. <b>%s</b>" % (a, mx(C)))
        if how == "eq":
            x, y = R.randint(-5, 5), R.randint(-5, 5)
            p, q = R.randint(1, 3), R.randint(1, 3)
            return M("<b>%s = %s</b>일 때, x, y의 값은?" % (mx([[x + p, 2], [3, "y − %d" % q if q else "y"]]), mx([[x + p if False else neg(x + p), 2], [3, neg(y - q)]])), "x = %s, y = %s" % (neg(x), neg(y)),
                     ["x = %s, y = %s" % (neg(x + 2 * p), neg(y - 2 * q)), "x = %s, y = %s" % (neg(y), neg(x)), "x = %s, y = %s" % (neg(x + p), neg(y - q))], "같은 위치의 성분이 같아요. <b>x = %s, y = %s</b>" % (neg(x), neg(y))) if False else \
                M("두 행렬 %s, %s가 서로 같을 때, x + y의 값은?" % (mx([["x %s %d" % ("+" if p else "", p), 2], [3, "y − %d" % q]]), mx([[neg(x + p), 2], [3, neg(y - q)]])), neg(x + y), [neg(x + y + p - q), neg(x - y), neg(x + y + 2 * p), neg(x + p + y - q)],
                  "x + %d = %s, y − %d = %s이므로 x = %s, y = %s. <b>%s</b>" % (p, neg(x + p), q, neg(y - q), neg(x), neg(y), neg(x + y)))
        a, b = R.randint(3, 9), R.randint(3, 9)
        p1, p2 = R.choice([(1000, 1500), (800, 1200), (500, 900)])
        c, d = R.randint(2, 8), R.randint(2, 8)
        P = [[a, b], [c, d]]
        Q = [[p1], [p2]]
        C = mm(P, Q)
        return N("두 가게의 빵과 우유 판매량을 행렬 %s(1행: 가게 A, 2행: 가게 B, 1열: 빵, 2열: 우유)로, 가격을 %s(원)로 나타냈어요. 가게 B의 매출은 몇 원일까요?" % (mx(P), mx(Q)), C[1][0], [C[0][0], c * p1, d * p2, C[1][0] + p1],
                 "행렬의 곱 %s의 2행 성분: %d × %d + %d × %d = <b>%s원</b>" % (mx(C), c, p1, d, p2, num(C[1][0])), f=lambda v: "%s원" % num(v))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    U = {}
    U["poly"] = ("polynomial-operations", 1, "[10공수1-01-01]", "다항식의 사칙연산의 원리를 설명하고, 그 계산을 할 수 있다.",
                 "다항식의 덧셈·뺄셈·곱셈·나눗셈", "다항식의 연산",
                 "고등학교 공통수학1 다항식의 연산 문제: 다항식의 덧셈과 뺄셈, 곱셈 공식((a + b + c)², (a + b)³), 다항식의 나눗셈과 몫·나머지, A = BQ + R까지 100문제와 정답·해설.",
                 "A = BQ + R", "곱셈 공식과 나눗셈은 인수분해·나머지정리의 기초예요.",
                 ["다항식의 덧셈과 뺄셈은 동류항끼리 계산해요. 빼기는 괄호 안의 모든 항의 부호를 바꾸어 더해요.",
                  "곱셈은 분배법칙으로 전개해요. (a + b)³ = a³ + 3a²b + 3ab² + b³, (a + b + c)² = a² + b² + c² + 2ab + 2bc + 2ca",
                  "다항식 A를 B로 나눈 몫을 Q, 나머지를 R이라 하면 <b>A = BQ + R</b>이고, R의 차수는 B의 차수보다 작아요.",
                  "일차식으로 나눌 때는 조립제법을 쓰면 빨라요."],
                 [("(x + 2)³", ["x³ + 3·x²·2 + 3·x·4 + 8"], "x³ + 6x² + 12x + 8"), ("(x² + 3x + 5) ÷ (x + 1)", ["몫 x + 2", "나머지 3"], "x² + 3x + 5 = (x + 1)(x + 2) + 3")],
                 [("A − B에서 B의 첫째 항만 부호를 바꾼다", "B의 모든 항의 부호를 바꾸어요."), ("(a + b)³ = a³ + b³", "3a²b + 3ab²을 빠뜨리지 않아요."), ("나머지의 차수를 나누는 식과 같게 둔다", "나머지의 차수는 나누는 식보다 낮아요.")],
                 [("다항식의 나눗셈은 언제 끝나나요?", "나머지의 차수가 나누는 식의 차수보다 작아질 때까지 해요."), ("곱셈 공식을 꼭 외워야 하나요?", "전개해서 확인할 수 있지만, 인수분해에서 거꾸로 쓰이므로 익혀 두면 편해요.")],
                 [("다항식의 덧셈과 뺄셈", [(p_ops(("add", "sub")), 20)]), ("다항식의 곱셈", [(p_ops(("mul",)), 20)]), ("곱셈 공식", [(p_ops(("expand", "cube")), 20)]),
                  ("몫과 나머지", [(p_div(("q", "r")), 20)]), ("A = BQ + R", [(p_div(("val",)), 10), (p_div(("q", "r")), 10)])], 83001)
    U["rem"] = ("identities-and-remainder-theorem", 2, "[10공수1-01-02]", "항등식의 성질과 나머지정리를 이해하고, 이를 활용하여 문제를 해결할 수 있다.",
                "항등식과 나머지정리, 인수정리", "나머지정리",
                "고등학교 공통수학1 항등식과 나머지정리 문제: 항등식의 계수 비교, 나머지정리, 일차식 ax + b로 나눈 나머지, 인수정리, 이차식으로 나눈 나머지, 조립제법까지 100문제와 정답·해설.",
                "P(x)를 x − a로 나눈 나머지 = P(a)", "P(a) = 0이면 x − a는 P(x)의 인수예요(인수정리).",
                ["x에 어떤 값을 넣어도 성립하는 등식을 <b>항등식</b>이라 하고, 양변의 같은 차수의 계수가 같아요.",
                 "<b>나머지정리</b>: 다항식 P(x)를 x − a로 나눈 나머지는 P(a), ax + b로 나눈 나머지는 P(−b/a)예요.",
                 "<b>인수정리</b>: P(a) = 0이면 P(x)는 x − a로 나누어떨어져요.",
                 "이차식으로 나눈 나머지는 px + q로 놓고 두 근을 대입해요."],
                [("x³ − 2x + 5를 x − 2로 나눈 나머지", ["P(2) = 8 − 4 + 5"], "9"), ("x³ + kx − 6이 x − 1로 나누어떨어짐", ["P(1) = 1 + k − 6 = 0"], "k = 5")],
                [("x + 2로 나눈 나머지에 x = 2를 대입한다", "x + 2 = 0이 되는 x = −2를 대입해요."), ("항등식에서 한 계수만 비교한다", "모든 차수의 계수를 비교하거나 수를 대입해요."), ("이차식으로 나눈 나머지를 상수로 놓는다", "나머지는 일차 이하이므로 px + q로 놓아요.")],
                [("조립제법은 언제 쓰나요?", "일차식 x − a로 나눌 때 몫과 나머지를 빠르게 구할 수 있어요."), ("나머지정리는 왜 성립하나요?", "P(x) = (x − a)Q(x) + R에 x = a를 넣으면 P(a) = R이 돼요.")],
                [("나머지정리", [(r_main(("rem",)), 20)]), ("인수정리", [(r_main(("factor",)), 20)]), ("항등식", [(r_main(("ident",)), 20)]),
                 ("조립제법", [(r_main(("synth",)), 20)]), ("이차식으로 나눈 나머지", [(r_main(("twodiv",)), 12), (r_main(("rem", "factor")), 8)])], 83002)
    U["fact"] = ("factoring", 3, "[10공수1-01-03]", "다항식의 인수분해를 할 수 있다.",
                 "인수분해: 세제곱 공식, 치환, 인수정리", "인수분해",
                 "고등학교 공통수학1 인수분해 문제: a³ ± b³, (a ± b)³ 꼴, 치환을 이용한 인수분해, 복이차식, 인수정리와 조립제법을 이용한 삼차식의 인수분해까지 100문제와 정답·해설.",
                 "세제곱 공식·치환·인수정리", "a³ + b³ = (a + b)(a² − ab + b²)",
                 ["곱셈 공식을 거꾸로 써요. a³ + b³ = (a + b)(a² − ab + b²), a³ − b³ = (a − b)(a² + ab + b²)",
                  "공통부분이 있으면 한 문자로 <b>치환</b>하여 인수분해한 뒤 되돌려요.",
                  "x⁴ + ax² + b 꼴은 x² = t로 치환하거나, A² − B² 꼴로 바꾸어요.",
                  "삼차 이상의 식은 P(a) = 0이 되는 a를 찾아 조립제법으로 나누어요(인수정리)."],
                 [("x³ − 8", ["a = x, b = 2"], "(x − 2)(x² + 2x + 4)"), ("x³ − 2x² − 5x + 6", ["P(1) = 0", "(x − 1)(x² − x − 6)"], "(x − 1)(x + 2)(x − 3)")],
                 [("x³ + 8 = (x + 2)(x² + 2x + 4)", "가운데 항의 부호는 반대예요. (x + 2)(x² − 2x + 4)"), ("치환한 뒤 원래 식으로 되돌리지 않는다", "t를 다시 x의 식으로 바꾸고 더 인수분해되는지 확인해요."), ("인수분해를 중간에서 멈춘다", "각 인수가 더 이상 인수분해되지 않을 때까지 해요.")],
                 [("P(a) = 0이 되는 a는 어떻게 찾나요?", "상수항의 약수를 최고차항 계수의 약수로 나눈 수 중에서 찾아요."), ("인수분해가 되지 않는 이차식은?", "실수 범위에서 판별식이 음수이면 더 인수분해할 수 없어요.")],
                 [("세제곱 공식", [(f_main(("cube", "sum3")), 20)]), ("치환을 이용한 인수분해", [(f_main(("sub",)), 20)]), ("복이차식", [(f_main(("quart", "biq", "diff4")), 20)]),
                  ("인수정리를 이용한 인수분해", [(f_main(("cubic",)), 20)]), ("섞어서 연습", [(f_main(), 20)])], 83003)
    U["cplx"] = ("complex-numbers", 4, "[10공수1-02-01]", "복소수의 뜻과 성질을 설명하고, 사칙연산을 수행할 수 있다.",
                 "복소수의 뜻과 사칙연산", "복소수",
                 "고등학교 공통수학1 복소수 문제: 허수단위 i, 복소수의 뜻과 켤레복소수, 복소수가 서로 같을 조건, 덧셈·뺄셈·곱셈·나눗셈, i의 거듭제곱, 음수의 제곱근까지 100문제와 정답·해설.",
                 "i² = −1", "나눗셈은 분모의 켤레복소수를 분모·분자에 곱해요.",
                 ["제곱하여 −1이 되는 수를 <b>i</b>로 나타내고, a + bi (a, b는 실수) 꼴의 수를 <b>복소수</b>라고 해요.",
                  "a + bi의 켤레복소수는 a − bi이고, 두 복소수는 실수부분과 허수부분이 각각 같을 때 서로 같아요.",
                  "덧셈·뺄셈은 실수부분끼리, 허수부분끼리 계산하고, 곱셈은 i² = −1을 이용해요.",
                  "a &gt; 0일 때 √−a = √a i예요. i⁴ = 1이므로 i의 거듭제곱은 4개씩 되풀이돼요."],
                 [("(2 + 3i)(1 − i)", ["2 − 2i + 3i − 3i²"], "5 + i"), ("(1 + 3i) ÷ (1 + i)", ["(1 + 3i)(1 − i) ÷ 2"], "2 + i")],
                 [("i² = 1로 계산한다", "i² = −1이에요."), ("√−2 × √−3 = √6", "√2 i × √3 i = −√6이에요."), ("나눗셈에서 분모에만 켤레복소수를 곱한다", "분모와 분자에 모두 곱해요.")],
                 [("복소수는 크기를 비교할 수 있나요?", "허수는 대소 관계를 정하지 않아요."), ("실수도 복소수인가요?", "b = 0인 복소수가 실수예요.")],
                 [("복소수의 뜻", [(c_concept(), 6), (c_ops(("eq", "conj")), 14)]), ("덧셈과 뺄셈", [(c_ops(("add",)), 20)]), ("곱셈", [(c_ops(("mul",)), 20)]),
                  ("나눗셈", [(c_ops(("div",)), 20)]), ("i의 거듭제곱", [(c_ops(("ipow",)), 12), (c_ops(("mul", "div")), 8)])], 83004)
    U["disc"] = ("discriminant", 5, "[10공수1-02-02]", "이차방정식의 실근과 허근을 이해하고, 판별식을 이용하여 이차방정식의 근을 판별할 수 있다.",
                 "이차방정식의 판별식", "판별식",
                 "고등학교 공통수학1 이차방정식의 판별식 문제: 실근과 허근, 판별식 D = b² − 4ac로 근 판별하기, 중근·실근·허근을 가질 조건, 허근을 가지는 이차방정식 풀기까지 100문제와 정답·해설.",
                 "D = b² − 4ac", "D가 양수면 두 실근, 0이면 중근, 음수면 두 허근이에요.",
                 ["이차방정식 ax² + bx + c = 0의 근은 x = (−b ± √(b² − 4ac)) ÷ 2a예요.",
                  "<b>D = b² − 4ac</b>를 판별식이라 하고, 근호 안의 부호로 근을 판별해요.",
                  "D &gt; 0이면 서로 다른 두 실근, D = 0이면 중근, D &lt; 0이면 서로 다른 두 허근이에요.",
                  "실근을 가질 조건은 D ≥ 0이에요."],
                 [("x² − 4x + 7 = 0", ["D = 16 − 28 = −12"], "서로 다른 두 허근"), ("x² + 6x + k = 0이 중근", ["36 − 4k = 0"], "k = 9")],
                 [("D = b² + 4ac로 계산한다", "b² − 4ac예요."), ("실근을 가질 조건을 D &gt; 0으로 쓴다", "중근도 실근이므로 D ≥ 0이에요."), ("허근을 '근이 없다'고 한다", "복소수 범위에서는 서로 다른 두 허근이 있어요.")],
                 [("짝수 판별식은?", "b = 2b′이면 D/4 = b′² − ac로 계산하면 편해요."), ("계수에 문자가 있으면?", "a ≠ 0인지 먼저 확인하고 판별식을 세워요.")],
                 [("근의 판별", [(d_main(("kind",)), 20)]), ("중근을 가질 조건", [(d_main(("k_double",)), 20)]), ("실근을 가질 조건", [(d_main(("k_real",)), 20)]),
                  ("허근을 가질 조건", [(d_main(("k_none",)), 20)]), ("허근 구하기", [(d_main(("formula",)), 20)])], 83005)
    U["coef"] = ("roots-and-coefficients", 6, "[10공수1-02-03]", "이차방정식의 근과 계수의 관계를 설명할 수 있다.",
                 "이차방정식의 근과 계수의 관계", "근과 계수의 관계",
                 "고등학교 공통수학1 근과 계수의 관계 문제: 두 근의 합과 곱, α² + β², 1/α + 1/β, (α − β)², 두 수를 근으로 하는 이차방정식, 한 근이 주어질 때 다른 근까지 100문제와 정답·해설.",
                 "α + β = −b/a, αβ = c/a", "두 근을 몰라도 대칭식의 값을 구할 수 있어요.",
                 ["ax² + bx + c = 0의 두 근을 α, β라 하면 <b>α + β = −b/a, αβ = c/a</b>예요.",
                  "α² + β² = (α + β)² − 2αβ, (α − β)² = (α + β)² − 4αβ, 1/α + 1/β = (α + β) ÷ αβ",
                  "두 수 α, β를 근으로 하고 x²의 계수가 1인 이차방정식은 x² − (α + β)x + αβ = 0이에요.",
                  "근이 허수여도 관계식은 그대로 성립해요."],
                 [("x² − 5x + 3 = 0의 α² + β²", ["25 − 6"], "19"), ("두 근 2, −3", ["합 −1, 곱 −6"], "x² + x − 6 = 0")],
                 [("두 근의 합을 b/a로 쓴다", "−b/a예요."), ("α² + β² = (α + β)²", "−2αβ를 빼야 해요."), ("이차방정식을 만들 때 합의 부호를 그대로 쓴다", "x² − (합)x + (곱) = 0이에요.")],
                 [("근을 직접 구하지 않아도 되나요?", "대칭식은 합과 곱만으로 구할 수 있어 계산이 빨라요."), ("삼차방정식에도 있나요?", "α + β + γ = −b/a 등 비슷한 관계가 있어요.")],
                 [("두 근의 합과 곱", [(k_coef(("sum", "prod")), 20)]), ("대칭식의 값", [(k_coef(("sym",)), 20)]), ("이차방정식 만들기", [(k_coef(("make",)), 20)]),
                  ("한 근과 다른 근", [(k_coef(("find",)), 20)]), ("섞어서 연습", [(k_coef(), 20)])], 83006)
    U["qfun"] = ("quadratic-equations-and-functions", 7, "[10공수1-02-04] [10공수1-02-05]", "이차방정식과 이차함수를 연결하여 그 관계를 설명할 수 있다. 이차함수의 그래프와 직선의 위치 관계를 판단할 수 있다.",
                 "이차방정식과 이차함수, 직선과의 위치 관계", "이차방정식과 이차함수",
                 "고등학교 공통수학1 이차방정식과 이차함수 문제: 그래프와 x축의 교점, 교점의 개수와 판별식, x축에 접할 조건, 이차함수의 그래프와 직선의 위치 관계, 접할 조건까지 100문제와 정답·해설.",
                 "x축과의 교점 = 이차방정식의 실근", "직선과의 위치 관계는 f(x) = mx + n의 판별식으로 판단해요.",
                 ["이차함수 y = ax² + bx + c의 그래프와 x축의 교점의 x좌표는 ax² + bx + c = 0의 실근이에요.",
                  "D &gt; 0이면 두 점에서 만나고, D = 0이면 접하고, D &lt; 0이면 만나지 않아요.",
                  "그래프와 직선 y = mx + n의 위치 관계는 ax² + (b − m)x + c − n = 0의 판별식으로 판단해요.",
                  "접할 조건은 판별식 D = 0이에요."],
                 [("y = x² − 2x − 3과 x축", ["(x − 3)(x + 1) = 0"], "x = −1, 3"), ("y = x² + 2와 y = 2x", ["x² − 2x + 2 = 0", "D = −4"], "만나지 않아요")],
                 [("직선과의 위치 관계에서 원래 식의 판별식을 본다", "두 식을 같게 놓은 이차방정식의 판별식을 봐요."), ("접하는 조건을 D &gt; 0으로 쓴다", "접하면 D = 0이에요."), ("교점의 x좌표와 y절편을 바꾼다", "y절편은 c이고, x축과의 교점은 방정식의 근이에요.")],
                 [("그래프로 방정식을 푸는 장점은?", "근의 개수와 위치를 한눈에 볼 수 있어요."), ("직선이 그래프 위에 있는지 아래에 있는지는?", "부등식 단원에서 f(x) − g(x)의 부호로 판단해요.")],
                 [("x축과의 교점", [(q_graph(("xint",)), 20)]), ("교점의 개수", [(q_graph(("count",)), 20)]), ("x축과의 위치 관계", [(q_graph(("k",)), 20)]),
                  ("직선과의 위치 관계", [(q_graph(("line",)), 20)]), ("접할 조건", [(q_graph(("tangent",)), 20)])], 83007)
    U["maxmin"] = ("maximum-and-minimum-of-quadratic-functions", 8, "[10공수1-02-06]", "이차함수의 최대, 최소를 탐구하고, 이를 실생활과 연결하여 유용성을 인식할 수 있다.",
                   "이차함수의 최대와 최소", "이차함수의 최대·최소",
                   "고등학교 공통수학1 이차함수의 최대·최소 문제: 꼭짓점으로 최댓값·최솟값 구하기, 제한된 범위에서의 최대·최소, 최솟값으로 미지수 구하기, 울타리·넓이 등 실생활 활용까지 100문제와 정답·해설.",
                   "범위가 있으면 꼭짓점과 양 끝값을 비교", "a가 양수면 꼭짓점에서 최솟값, 음수면 최댓값이에요.",
                   ["y = a(x − p)² + q로 고치면 a &gt; 0일 때 최솟값 q, a &lt; 0일 때 최댓값 q예요.",
                    "x의 범위가 정해지면 꼭짓점의 x좌표가 범위 안에 있는지 확인해요.",
                    "범위 안에 있으면 꼭짓점과 양 끝값을, 밖에 있으면 양 끝값만 비교해요.",
                    "실생활 문제는 구하는 양을 이차함수로 나타내고, 변수의 범위를 꼭 확인해요."],
                   [("y = x² − 4x + 1", ["(x − 2)² − 3"], "최솟값 −3"), ("0 ≤ x ≤ 3, y = −x² + 2x", ["꼭짓점 (1, 1)", "끝값 0, −3"], "최댓값 1, 최솟값 −3")],
                   [("범위가 있어도 꼭짓점만 본다", "양 끝값도 반드시 비교해요."), ("최솟값을 꼭짓점의 x좌표로 답한다", "최솟값은 y좌표예요."), ("실생활 문제에서 변수의 범위를 생각하지 않는다", "길이는 양수 등 조건을 확인해요.")],
                   [("최댓값과 최솟값이 모두 있는 경우는?", "x의 범위가 닫힌 구간일 때는 둘 다 존재해요."), ("이차함수의 최대·최소는 어디에 쓰이나요?", "넓이, 이익, 높이처럼 가장 크거나 작은 값을 찾을 때 써요.")],
                   [("최댓값과 최솟값", [(mm_main(("std",)), 20)]), ("제한된 범위", [(mm_main(("range",)), 20)]), ("미지수 구하기", [(mm_main(("find",)), 20)]),
                    ("실생활 활용", [(mm_main(("word",)), 12), (mm_main(("range",)), 8)]), ("섞어서 연습", [(mm_main(("std", "range", "find")), 20)])], 83008)
    U["cubic"] = ("cubic-and-quartic-equations", 9, "[10공수1-02-07]", "간단한 삼차방정식과 사차방정식을 풀 수 있다.",
                  "삼차방정식과 사차방정식", "삼차·사차방정식",
                  "고등학교 공통수학1 삼차방정식과 사차방정식 문제: 인수정리와 조립제법으로 삼차방정식 풀기, 허근을 가지는 삼차방정식, 복이차방정식, 한 근이 주어질 때 나머지 근, x³ = 1의 허근 ω의 성질까지 100문제와 정답·해설.",
                  "인수정리로 한 근을 찾고 차수를 낮춰요", "x³ = 1의 허근 ω는 ω³ = 1, ω² + ω + 1 = 0",
                  ["삼차방정식은 P(a) = 0인 a를 찾아 조립제법으로 나누어 (x − a)(이차식) = 0으로 바꾸어요.",
                   "사차방정식 x⁴ + ax² + b = 0은 x² = t로 치환해요.",
                   "x³ = 1의 한 허근을 ω라 하면 ω³ = 1, ω² + ω + 1 = 0이에요.",
                   "실수 계수 방정식에서 허근은 켤레로 함께 나와요."],
                  [("x³ − 7x + 6 = 0", ["P(1) = 0", "(x − 1)(x² + x − 6)"], "x = −3, 1, 2"), ("x⁴ − 5x² + 4 = 0", ["(x² − 1)(x² − 4)"], "x = ±1, ±2")],
                  [("인수정리로 찾은 근만 답한다", "나머지 이차방정식의 근도 구해요."), ("x² = t에서 t의 값을 답으로 쓴다", "t = x²이므로 x를 구해요."), ("ω³ = −1로 생각한다", "x³ = 1의 근이므로 ω³ = 1이에요.")],
                  [("근을 찾을 후보는?", "상수항의 약수(±)부터 대입해 봐요."), ("삼차방정식의 근은 몇 개인가요?", "복소수 범위에서 중근을 포함해 3개예요.")],
                  [("삼차방정식", [(h_main(("cubic",)), 20)]), ("허근을 가지는 삼차방정식", [(h_main(("fact",)), 20)]), ("사차방정식", [(h_main(("biq",)), 20)]),
                   ("한 근과 나머지 근", [(h_main(("other",)), 20)]), ("ω의 성질", [(h_main(("omega",)), 12), (h_main(("cubic",)), 8)])], 83009)
    U["simq"] = ("simultaneous-quadratic-equations", 10, "[10공수1-02-08]", "미지수가 2개인 연립이차방정식을 풀 수 있다.",
                 "연립이차방정식", "연립이차방정식",
                 "고등학교 공통수학1 연립이차방정식 문제: 일차식과 이차식으로 된 연립방정식, 인수분해되는 이차식이 있는 연립방정식, 합과 곱을 이용한 풀이, 직사각형의 둘레와 넓이 등 활용까지 100문제와 정답·해설.",
                 "일차식을 한 문자에 대해 풀어 대입", "인수분해되는 식은 두 일차식으로 나누어 각각 풀어요.",
                 ["일차방정식과 이차방정식으로 된 연립방정식은 일차식을 y = …로 풀어 이차식에 대입해요.",
                  "두 식이 모두 이차식이면 인수분해되는 식을 찾아 두 개의 일차식으로 나누어요.",
                  "x + y = s, xy = p를 알면 x, y는 t² − st + p = 0의 두 근이에요.",
                  "해는 순서쌍으로 쓰고, 여러 쌍이 나올 수 있어요."],
                 [("x + y = 5, x² + y² = 13", ["y = 5 − x", "x² − 5x + 6 = 0"], "(2, 3), (3, 2)"), ("x + y = 7, xy = 12", ["t² − 7t + 12 = 0"], "(3, 4), (4, 3)")],
                 [("해를 한 쌍만 쓴다", "대입하면 보통 두 쌍이 나와요."), ("x만 구하고 y를 구하지 않는다", "구한 x를 일차식에 넣어 y도 구해요."), ("x + y와 xy로 만든 방정식의 근을 x만으로 생각한다", "두 근이 각각 x, y예요.")],
                 [("검산은 어떻게 하나요?", "구한 순서쌍을 두 식에 모두 대입해 확인해요."), ("그래프로 보면?", "원과 직선, 포물선과 직선의 교점이 해예요.")],
                 [("일차식과 이차식", [(s_main(("lin",)), 20)]), ("인수분해를 이용한 풀이", [(s_main(("fact",)), 10), (s_main(("lin",)), 10)]), ("합과 곱의 이용", [(s_main(("word",)), 10), (s_main(("lin",)), 10)]),
                  ("활용", [(s_main(("word",)), 10), (s_main(("fact",)), 10)]), ("섞어서 연습", [(s_main(), 20)])], 83010)
    U["lin"] = ("linear-inequalities-and-absolute-values", 11, "[10공수1-02-09] [10공수1-02-10]", "미지수가 1개인 연립일차부등식을 풀 수 있다. 절댓값을 포함한 일차부등식을 풀 수 있다.",
                "연립일차부등식과 절댓값을 포함한 부등식", "연립일차부등식",
                "고등학교 공통수학1 연립일차부등식 문제: 연립일차부등식의 해, 절댓값을 포함한 일차부등식, 정수인 해의 개수, 절댓값이 두 개인 부등식까지 100문제와 정답·해설.",
                "절댓값은 경계에서 범위를 나누어요", "연립부등식은 각각 풀고 공통 범위를 구해요.",
                ["연립일차부등식은 각 부등식을 풀고 <b>공통 범위</b>를 구해요.",
                 "a &gt; 0일 때 |x| &lt; a는 −a &lt; x &lt; a, |x| &gt; a는 x &lt; −a 또는 x &gt; a예요.",
                 "절댓값이 두 개 이상이면 절댓값 안이 0이 되는 값을 기준으로 범위를 나누어 풀어요.",
                 "음수를 곱하거나 나누면 부등호의 방향이 바뀌어요."],
                [("|x − 2| &lt; 3", ["−3 &lt; x − 2 &lt; 3"], "−1 &lt; x &lt; 5"), ("2x &gt; 4, 3x ≤ 15", ["x &gt; 2", "x ≤ 5"], "2 &lt; x ≤ 5")],
                [("|x − 2| &gt; 3을 −3 &lt; x − 2 &lt; 3으로 푼다", "&gt;이면 '또는'으로 두 범위예요."), ("공통 범위가 아니라 합친 범위를 답한다", "연립부등식은 동시에 만족하는 범위예요."), ("범위를 나눌 때 경계값을 빠뜨린다", "각 범위에 경계를 한쪽만 포함시켜요.")],
                [("해가 없는 경우는?", "공통 범위가 없으면 해가 없어요."), ("A &lt; B &lt; C 꼴은?", "A &lt; B와 B &lt; C를 연립하여 풀어요.")],
                [("연립일차부등식", [(l_main(("sys",)), 20)]), ("|x − a| &lt; b", [(l_main(("abs1",)), 20)]), ("|x − a| ≥ b", [(l_main(("abs2",)), 20)]),
                 ("정수인 해", [(l_main(("count",)), 20)]), ("절댓값이 두 개인 부등식", [(l_main(("absx",)), 14), (l_main(("sys",)), 6)])], 83011)
    U["qineq"] = ("quadratic-inequalities", 12, "[10공수1-02-11]", "이차부등식과 이차함수를 연결하여 그 관계를 설명하고, 이차부등식과 연립이차부등식을 풀 수 있다.",
                  "이차부등식과 연립이차부등식", "이차부등식",
                  "고등학교 공통수학1 이차부등식 문제: 이차함수의 그래프를 이용한 이차부등식의 풀이, 판별식이 0 이하인 경우, 항상 성립할 조건, 연립이차부등식까지 100문제와 정답·해설.",
                  "해는 그래프가 x축의 위인지 아래인지로", "음수가 되는 범위는 두 근 사이, 양수는 두 근의 바깥쪽이에요.",
                  ["이차부등식 f(x) &gt; 0의 해는 y = f(x)의 그래프가 x축보다 위에 있는 x의 범위예요.",
                   "α &lt; β일 때 (x − α)(x − β) &lt; 0의 해는 α &lt; x &lt; β, (x − α)(x − β) &gt; 0의 해는 x &lt; α 또는 x &gt; β예요.",
                   "D &lt; 0이면 x² + bx + c &gt; 0의 해는 모든 실수, x² + bx + c &lt; 0의 해는 없어요.",
                   "모든 실수 x에 대하여 x² + bx + c &gt; 0이 성립하려면 D &lt; 0이에요."],
                  [("x² − x − 6 &lt; 0", ["(x − 3)(x + 2) &lt; 0"], "−2 &lt; x &lt; 3"), ("x² − 4x + 4 &gt; 0", ["(x − 2)² &gt; 0"], "x ≠ 2인 모든 실수")],
                  [("&lt; 0인데 '또는'으로 답한다", "그래프가 x축 아래인 두 근 사이예요."), ("x² 계수가 음수인데 그대로 푼다", "양변에 −1을 곱해 부등호 방향을 바꿔요."), ("(x − 2)² &gt; 0의 해를 모든 실수라고 한다", "x = 2에서는 0이므로 x ≠ 2예요.")],
                  [("이차부등식을 그래프로 생각하는 이유는?", "x축 위·아래로 해의 범위를 한눈에 볼 수 있어요."), ("연립이차부등식은?", "각각 풀고 공통 범위를 구해요.")],
                  [("&lt; 0인 이차부등식", [(qi_main(("lt",)), 20)]), ("≥ 0인 이차부등식", [(qi_main(("gt",)), 20)]), ("판별식이 0 이하인 경우", [(qi_main(("all",)), 20)]),
                   ("항상 성립할 조건", [(qi_main(("k",)), 6), (qi_main(("lt", "gt")), 14)]), ("연립이차부등식", [(qi_main(("sys",)), 20)])], 83012)
    U["count"] = ("counting-principles", 13, "[10공수1-03-01]", "합의 법칙과 곱의 법칙을 이해하고, 적절한 전략을 사용하여 경우의 수와 관련된 문제를 해결할 수 있다.",
                  "합의 법칙과 곱의 법칙", "경우의 수",
                  "고등학교 공통수학1 경우의 수 문제: 합의 법칙과 곱의 법칙, 주사위 눈의 합, 전개식의 항의 개수, 약수의 개수, 길의 경우의 수, 지불 방법까지 100문제와 정답·해설.",
                  "동시에 일어나지 않으면 더하고, 잇달아 일어나면 곱해요", "약수의 개수 = (지수 + 1)의 곱",
                  ["두 사건 A, B가 동시에 일어나지 않을 때 A 또는 B가 일어나는 경우의 수는 m + n이에요(<b>합의 법칙</b>).",
                   "A가 일어나는 각 경우마다 B가 일어나면 경우의 수는 m × n이에요(<b>곱의 법칙</b>).",
                   "N = pᵃqᵇrᶜ의 양의 약수의 개수는 (a + 1)(b + 1)(c + 1)이에요.",
                   "빠짐없이, 중복 없이 세기 위해 표나 수형도를 그려요."],
                  [("72의 양의 약수", ["72 = 2³ × 3²"], "(3 + 1)(2 + 1) = 12개"), ("두 주사위 합이 4 또는 10", ["3가지 + 3가지"], "6가지")],
                  [("동시에 일어나는데 더한다", "잇달아 일어나면 곱해요."), ("약수의 개수를 지수의 곱으로 센다", "각 지수에 1을 더해서 곱해요."), ("지불 방법에서 0원을 빼지 않는다", "모두 0개인 경우는 지불이 아니므로 1을 빼요.")],
                  [("수형도는 언제 쓰나요?", "경우가 적고 조건이 복잡할 때 빠짐없이 셀 수 있어요."), ("지불 방법과 지불 금액의 수가 다를 수 있나요?", "큰 동전을 작은 동전으로 만들 수 있으면 금액의 수가 줄어요.")],
                  [("합의 법칙", [(n_main(("sumlaw",)), 20)]), ("곱의 법칙", [(n_main(("prodlaw",)), 20)]), ("약수의 개수", [(n_main(("divisors",)), 20)]),
                   ("길과 지불 방법", [(n_main(("path", "coins")), 20)]), ("섞어서 연습", [(n_main(), 20)])], 83013)
    U["perm"] = ("permutations", 14, "[10공수1-03-02]", "순열의 개념을 이해하고, 순열의 수를 구하는 방법을 설명할 수 있다.",
                 "순열과 순열의 수", "순열",
                 "고등학교 공통수학1 순열 문제: nPr의 계산, n명 중 r명을 일렬로 세우기, 이웃하여 서는 경우와 이웃하지 않는 경우, 자연수 만들기, nPr에 대한 방정식까지 100문제와 정답·해설.",
                 "nPr = n!/(n − r)!", "이웃하면 묶어서, 이웃하지 않으면 사이사이에 세워요.",
                 ["서로 다른 n개에서 r개를 택하여 일렬로 나열하는 것을 <b>순열</b>이라 하고, 그 수를 <sub>n</sub>P<sub>r</sub>로 나타내요.",
                  "<sub>n</sub>P<sub>r</sub> = n(n − 1)(n − 2) × … × (n − r + 1) = n!/(n − r)!, <sub>n</sub>P<sub>n</sub> = n!, 0! = 1",
                  "이웃하는 것은 한 묶음으로 보고 세운 뒤, 묶음 안에서 자리를 바꾸는 경우를 곱해요.",
                  "이웃하지 않는 것은 나머지를 먼저 세우고 그 사이와 양 끝에 세워요."],
                 [("₅P₃", ["5 × 4 × 3"], "60"), ("1, 2, 3, 4로 세 자리 수", ["₄P₃"], "24개")],
                 [("₅P₃ = 5 × 3으로 계산한다", "5부터 하나씩 줄여 3개를 곱해요."), ("이웃하는 경우에 묶음 안의 순서를 곱하지 않는다", "묶음 안의 순서도 바뀔 수 있어요."), ("0이 있는 수 만들기에서 맨 앞에 0을 둔다", "맨 앞자리에는 0이 올 수 없어요.")],
                 [("순열과 조합의 차이는?", "순열은 순서를 생각하고, 조합은 순서를 생각하지 않아요."), ("n!은 어떻게 읽나요?", "'n 팩토리얼'이라고 읽어요.")],
                 [("순열의 수", [(perm_main(("npr", "eq")), 20)]), ("일렬로 세우기", [(perm_main(("line",)), 20)]), ("이웃하는 경우", [(perm_main(("adj",)), 20)]),
                  ("이웃하지 않는 경우", [(perm_main(("nonadj",)), 14), (pc_concept(), 6)]), ("자연수 만들기", [(perm_main(("num",)), 20)])], 83014)
    U["comb"] = ("combinations", 15, "[10공수1-03-03]", "조합의 개념을 이해하고, 조합의 수를 구하는 방법을 설명할 수 있다.",
                 "조합과 조합의 수", "조합",
                 "고등학교 공통수학1 조합 문제: nCr의 계산과 성질, 대표 뽑기, 남학생과 여학생을 나누어 뽑기, 적어도 한 명 포함되는 경우, 선분·삼각형·대각선의 개수까지 100문제와 정답·해설.",
                 "nCr = nPr ÷ r!", "nCr = nCn−r, 적어도 하나는 전체에서 빼요.",
                 ["서로 다른 n개에서 순서를 생각하지 않고 r개를 택하는 것을 <b>조합</b>이라 하고, 그 수를 <sub>n</sub>C<sub>r</sub>로 나타내요.",
                  "<sub>n</sub>C<sub>r</sub> = <sub>n</sub>P<sub>r</sub> ÷ r! = n!/(r!(n − r)!), <sub>n</sub>C<sub>r</sub> = <sub>n</sub>C<sub>n−r</sub>",
                  "'적어도 하나'는 전체 경우의 수에서 하나도 없는 경우의 수를 빼요.",
                  "도형의 개수는 점을 고르는 조합으로 세요(일직선 위의 점에 주의)."],
                 [("₇C₃", ["7 × 6 × 5 ÷ 6"], "35"), ("8명 중 대표 2명", ["₈C₂"], "28가지")],
                 [("조합인데 순열로 센다", "자격이 같으면 순서가 없어요."), ("₁₀C₈을 직접 계산한다", "₁₀C₂로 바꾸면 쉬워요."), ("'적어도 하나'를 직접 나누어 세다가 빠뜨린다", "여사건을 이용해요.")],
                 [("ₙC₀은 얼마인가요?", "아무것도 뽑지 않는 1가지이므로 1이에요."), ("파스칼의 삼각형은?", "ₙCᵣ = ₙ₋₁Cᵣ₋₁ + ₙ₋₁Cᵣ를 배열한 것이에요.")],
                 [("조합의 수", [(comb_main(("ncr", "eq")), 20)]), ("대표 뽑기", [(comb_main(("pick",)), 20)]), ("나누어 뽑기", [(comb_main(("both",)), 20)]),
                  ("적어도 한 명", [(comb_main(("atleast",)), 14), (pc_concept(), 6)]), ("도형의 개수", [(comb_main(("geo",)), 20)])], 83015)
    U["mat"] = ("matrices", 16, "[10공수1-04-01] [10공수1-04-02]", "행렬의 뜻을 알고, 실생활 상황을 행렬로 표현할 수 있다. 행렬의 연산을 수행하고, 관련된 문제를 해결할 수 있다.",
                "행렬의 뜻과 연산", "행렬",
                "고등학교 공통수학1 행렬 문제: 행렬의 뜻과 (i, j) 성분, m × n 행렬, 서로 같은 행렬, 덧셈·뺄셈·실수배, 행렬의 곱셈, 거듭제곱, 실생활 자료를 행렬로 나타내기까지 100문제와 정답·해설.",
                "AB의 (i, j) 성분 = A의 i행 · B의 j열", "행렬의 곱셈은 교환법칙이 성립하지 않아요(AB ≠ BA).",
                ["수나 문자를 직사각형 모양으로 배열하여 괄호로 묶은 것을 <b>행렬</b>이라 하고, i행 j열의 수를 (i, j) 성분이라고 해요.",
                 "같은 꼴의 두 행렬은 같은 위치의 성분끼리 더하거나 빼요. 실수배는 모든 성분에 곱해요.",
                 "AB의 (i, j) 성분은 A의 i행과 B의 j열의 성분을 차례로 곱하여 더한 값이에요.",
                 "행렬의 곱셈에서는 일반적으로 AB ≠ BA예요."],
                [("(1 2; 3 4)(1 0; 1 1)", ["(1 + 2, 0 + 2)", "(3 + 4, 0 + 4)"], "(3 2; 7 4)"), ("2A − B의 성분", ["2a₁₁ − b₁₁ …"], "성분별로 계산")],
                [("행렬의 곱셈을 성분끼리 곱한다", "행과 열을 곱해 더해요."), ("(i, j) 성분에서 행과 열을 바꾼다", "앞의 수가 행, 뒤의 수가 열이에요."), ("AB = BA라고 생각한다", "일반적으로 성립하지 않아요.")],
                [("곱할 수 있는 조건은?", "앞 행렬의 열의 개수와 뒤 행렬의 행의 개수가 같아야 해요."), ("행렬은 어디에 쓰이나요?", "판매량과 가격, 연결 관계처럼 표로 된 자료를 계산할 때 써요.")],
                [("행렬의 뜻", [(m_main(("entry", "size")), 20)]), ("덧셈과 뺄셈", [(m_main(("add", "eq")), 20)]), ("실수배", [(m_main(("scal",)), 20)]),
                 ("행렬의 곱셈", [(m_main(("mul",)), 20)]), ("거듭제곱과 활용", [(m_main(("power",)), 8), (m_main(("life",)), 12)])], 83016)
    t = U[which]
    slug, sort, code, std, title, short, meta, kb, ks, think, ex, mist, faq, spec, seed = t
    return unit(G, slug, sort, code, std, title, short, meta, kb, ks, think, ex, mist, faq, spec, seed)
