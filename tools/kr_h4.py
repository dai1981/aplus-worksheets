# -*- coding: utf-8 -*-
"""
대한민국 고등학교 미적분Ⅰ（2022 개정）の 12 単元。build(key)：
  lim 함수의 극한 / cont 함수의 연속 / deriv 미분계수와 도함수 / rules 미분법 / tan 접선과 평균값 정리
  inc 증가·감소와 극값 / graph 그래프와 최대·최소 / app 방정식·부등식과 속도 / indef 부정적분 / defi 정적분
  area 넓이 / vel 속도와 거리
誤答は「0/0 꼴을 그대로 0으로 둔다」「차수가 같을 때 상수항의 비를 쓴다」「좌극한과 우극한을 같게 둔다」
「(xⁿ)′ = nxⁿ로 지수를 줄이지 않는다」「곱의 미분을 미분끼리 곱한다」「접선의 기울기에 함숫값을 쓴다」「극값에서 x좌표를 답한다」
「적분상수 C를 빠뜨린다」「정적분에서 위끝·아래끝을 바꾼다」「넓이에서 x축 아래 부분을 음수로 더한다」「위치의 변화량과 움직인 거리를 같게 둔다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_m2a import poly2
from kr_hs import M, N, neg, par, px, padd, pmul, peval, surd, W, graph, num, fr, unit, BLUE, RED

R = random.Random(83301)
G = "calculus-1"


def nz(lo=-6, hi=6):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def lim(to, body, var="x"):
    return "lim<sub>%s→%s</sub> %s" % (var, to, body)


def der(p):
    n = len(p) - 1
    return [c * (n - i) for i, c in enumerate(p[:-1])] or [0]


def antider(p):
    n = len(p) - 1
    return [Fr(c, n - i + 1) for i, c in enumerate(p)] + [0]


def integ(p, a, b):
    F = antider(p)
    return peval(F, Fr(b)) - peval(F, Fr(a))


def I(a, b, body):
    return "<span class='nowrap'>∫<sub>%s</sub><sup>%s</sup> (%s) dx</span>" % (neg(a), neg(b), body)


def rnd_poly(deg, lo=-5, hi=5, lead=(1, 2, 3, -1, -2)):
    return [R.choice(lead)] + [R.randint(lo, hi) for _ in range(deg)]


# ------------------------------------------------------------------ 함수의 극한
def l_main(kinds=("sub", "fact", "root", "inf", "side", "const")):
    def mk():
        how = R.choice(kinds)
        if how == "sub":
            p = rnd_poly(R.choice([2, 3]))
            a = R.randint(-3, 3)
            v = peval(p, a)
            return N("<b>%s</b>의 값은?" % lim(neg(a), "(%s)" % px(p)), v, [peval(p, -a), p[-1], v + 1, peval(der(p), a)], "다항함수는 x = %s를 대입해요. <b>%s</b>" % (neg(a), neg(v)))
        if how == "fact":
            a = nz(-5, 5)
            b = R.randint(-5, 5)
            k = R.choice(["sq", "lin"])
            if k == "sq":
                # (x² − a²)/(x − a) → 2a  또는 (x² + (b − a)x − ab)/(x − a) → a + b
                num_ = pmul([1, -a], [1, b])
                v = a + b
                return N("<b>%s</b>의 값은?" % lim(neg(a), fr(px(num_), px([1, -a]))), v, [0, b, a - b if a - b != v else v + 1, peval(num_, 0)], "분자를 인수분해하면 (%s)(%s)이므로 약분하고 x = %s를 대입해요. <b>%s</b>" % (px([1, -a]), px([1, b]), neg(a), neg(v)))
            c = nz(-4, 4)
            num_ = pmul([1, -a], [1, 0, c])
            den = pmul([1, -a], [1, b])
            if peval([1, b], a) == 0:
                return None
            v = Fr(a * a + c, a + b)
            return N("<b>%s</b>의 값은?" % lim(neg(a), fr(px(num_), px(den))), v, [Fr(c, b) if b else v + 1, 0, Fr(a * a, a + b) if a * a != a * a + c else v + 2, -v], "분모·분자의 공통인수 %s로 약분하면 (%s) ÷ (%s). <b>%s</b>" % (px([1, -a]), px([1, 0, c]), px([1, b]), neg(v)))
        if how == "root":
            a = R.randint(1, 6)
            k = R.choice(["x", "x2"])
            if k == "x":
                v = Fr(1, 2 * a)
                return N("<b>%s</b>의 값은?" % lim("0", fr("√(x + %d) − %d" % (a * a, a), "x")), v, [Fr(1, a), 0, Fr(a, 2), 2 * a], "분자를 유리화하면 1 ÷ (√(x + %d) + %d) → 1/%d. <b>%s</b>" % (a * a, a, 2 * a, neg(v)))
            v = 2 * a
            return N("<b>%s</b>의 값은?" % lim(neg(a * a), fr("x − %d" % (a * a), "√x − %d" % a)), v, [a, Fr(1, 2 * a), 0, a * a], "x − %d = (√x − %d)(√x + %d)이므로 √x + %d → <b>%d</b>" % (a * a, a, a, a, v))
        if how == "inf":
            n = R.choice([1, 2, 3])
            m = n + R.choice([0, 0, 1, -1])
            if m < 1:
                m = n
            P = rnd_poly(n, lead=(1, 2, 3, 4, -2, -3))
            Q = rnd_poly(m, lead=(1, 2, 3, -1, 5))
            if n == m:
                v = Fr(P[0], Q[0])
                ok = neg(v)
            elif n < m:
                ok = "0"
            else:
                ok = "∞" if P[0] * Q[0] > 0 else "−∞"
            w = [neg(Fr(P[-1], Q[-1])) if Q[-1] else "1", "0", "∞", neg(Fr(P[0], Q[0])), "−∞", "1"]
            return M("<b>%s</b>의 값은?" % lim("∞", fr(px(P), px(Q))), ok, [x for x in w if x != ok],
                     "분모의 최고차항 x<sup>%d</sup>으로 분모·분자를 나누어요. <b>%s</b>" % (m, ok))
        if how == "side":
            k = R.choice(["abs", "piece"])
            if k == "abs":
                a = R.randint(-3, 3)
                s = R.choice(["+", "−"])
                v = 1 if s == "+" else -1
                return N("<b>%s</b>의 값은?" % lim("%s<sup>%s</sup>" % (neg(a), s), fr("|%s|" % px([1, -a]), px([1, -a]))), v, [-v, 0, 2, a], "x → %s<sup>%s</sup>이면 %s %s 0이므로 |%s| = %s. <b>%s</b>" % (neg(a), s, px([1, -a]), "&gt;" if s == "+" else "&lt;", px([1, -a]), px([1, -a]) if s == "+" else "−(%s)" % px([1, -a]), neg(v)))
            a = R.randint(-2, 3)
            p, q = [R.choice([1, 2, -1]), R.randint(-4, 4)], [R.choice([1, -1, 2]), R.randint(-4, 4)]
            s = R.choice(["+", "−"])
            L, Rr = peval(p, a), peval(q, a)
            v = Rr if s == "+" else L
            return N("함수 f(x) = { %s (x &lt; %s), %s (x ≥ %s) }에 대하여 <b>lim<sub>x→%s<sup>%s</sup></sub> f(x)</b>의 값은?" % (px(p), neg(a), px(q), neg(a), neg(a), s), v, [L if s == "+" else Rr, L + Rr, v + 1, p[-1] if s == "−" else q[-1]],
                     "x → %s<sup>%s</sup>이면 %s를 써요. <b>%s</b>" % (neg(a), s, "x ≥ %s 쪽 식 %s" % (neg(a), px(q)) if s == "+" else "x &lt; %s 쪽 식 %s" % (neg(a), px(p)), neg(v))) if L != Rr else None
        # const: lim (x² + ax + b)/(x − c) = k
        c = nz(-4, 4)
        k = R.randint(-6, 8)
        # x² + ax + b = (x − c)(x + d), c + d = k → d = k − c
        d = k - c
        a, b = d - c, -c * d
        kind = R.choice(["a", "b", "ab"])
        v = {"a": a, "b": b, "ab": a + b}[kind]
        return N("<b>%s = %s</b>일 때, 상수 %s의 값은? (a, b는 상수)" % (lim(neg(c), fr("x² + ax + b", px([1, -c]))), neg(k), {"a": "a", "b": "b", "ab": "a + b"}[kind]), v,
                 [{"a": -a, "b": -b, "ab": a - b}[kind], {"a": b, "b": a, "ab": -(a + b)}[kind], v + 1, k], "분모 → 0이므로 분자 → 0: %s = 0. 분자 = (%s)(x + d)로 놓으면 %s + d = %s. a = %s, b = %s. <b>%s</b>" % (poly2({(1, 0): c, (0, 1): 1, (0, 0): c * c}, ("a", "b")), px([1, -c]), neg(c), neg(k), neg(a), neg(b), neg(v)))
    return mk


# ------------------------------------------------------------------ 연속
def c_main(kinds=("k", "rat", "piece", "ivt", "concept")):
    def mk():
        how = R.choice(kinds)
        if how == "k":
            a = nz(-4, 4)
            b = R.randint(-4, 4)
            num_ = pmul([1, -a], [1, b])
            v = a + b
            return N("함수 f(x) = { %s (x ≠ %s), k (x = %s) }가 x = %s에서 연속일 때, 상수 k의 값은?" % (fr(px(num_), px([1, -a])), neg(a), neg(a), neg(a)), v, [0, b, -v, peval(num_, 0)],
                     "k = lim<sub>x→%s</sub> f(x) = %s + %s. <b>%s</b>" % (neg(a), neg(a), par(b), neg(v)))
        if how == "piece":
            a = R.randint(-2, 3)
            p = [R.choice([1, 2, -1]), R.randint(-4, 4)]
            m = R.choice([1, 2, 3, -1])
            # f = p (x<a), m x + k (x≥a)  → k = p(a) − m a
            k = peval(p, a) - m * a
            return N("함수 f(x) = { %s (x &lt; %s), %s + k (x ≥ %s) }가 실수 전체에서 연속일 때, 상수 k의 값은?" % (px(p), neg(a), px([m, 0]), neg(a)), k, [peval(p, a), -k, peval(p, a) + m * a, k + 1],
                     "x = %s에서 좌극한 %s = 함숫값 %s + k. <b>k = %s</b>" % (neg(a), neg(peval(p, a)), neg(m * a), neg(k)))
        if how == "rat":
            r1, r2 = R.sample(range(-5, 6), 2)
            den = pmul([1, -r1], [1, -r2])
            ok = "x = %s, x = %s" % (neg(min(r1, r2)), neg(max(r1, r2)))
            return M("함수 <b>f(x) = %s</b>가 불연속인 x의 값을 모두 구하면?" % fr(px([1, R.randint(-3, 3)]) if R.random() < 0.5 else "1", px(den)), ok,
                     ["x = %s, x = %s" % (neg(-max(r1, r2)), neg(-min(r1, r2))), "x = %s" % neg(min(r1, r2)), "없어요", "x = %s" % neg(den[-1])], "분모가 0이 되는 x에서 정의되지 않아 불연속이에요. <b>%s</b>" % ok)
        if how == "ivt":
            r = [R.randint(-4, 4) for _ in range(3)]
            if len(set(r)) < 3:
                return None
            P = pmul(pmul([1, -r[0]], [1, -r[1]]), [1, -r[2]])
            lo, hi = sorted(R.sample(range(-5, 6), 2))
            if lo in r or hi in r:
                return None
            fa, fb = peval(P, lo), peval(P, hi)
            n = sum(1 for x in r if lo < x < hi)
            if fa * fb < 0:
                ok = "참이에요"
                return M("f(x) = %s일 때, 'f(%s)f(%s) &lt; 0이므로 방정식 f(x) = 0은 열린구간 (%s, %s)에서 적어도 하나의 실근을 가진다'는 옳을까요?" % (px(P), neg(lo), neg(hi), neg(lo), neg(hi)), "옳아요", ["옳지 않아요", "f(x)가 불연속이라 알 수 없어요", "실근이 없어요"],
                         "f(%s) = %s, f(%s) = %s로 부호가 다르고 f는 연속이므로 사잇값 정리에 의해 <b>옳아요</b>" % (neg(lo), neg(fa), neg(hi), neg(fb)))
            return N("f(x) = %s일 때, f(%s) × f(%s)의 값은?" % (px(P), neg(lo), neg(hi)), fa * fb, [fa + fb, fa - fb, -fa * fb if fa * fb else 1, fa], "f(%s) = %s, f(%s) = %s. <b>%s</b>" % (neg(lo), neg(fa), neg(hi), neg(fb), neg(fa * fb)))
        C = [("함수 f(x)가 x = a에서 연속일 조건으로 옳은 것은?", "f(a)가 존재하고 lim<sub>x→a</sub> f(x) = f(a)", ["lim<sub>x→a</sub> f(x)만 존재", "f(a)만 존재", "좌극한과 우극한이 달라요"]),
             ("닫힌구간 [a, b]에서 연속인 함수는 이 구간에서 반드시 어떤 값을 가질까요?", "최댓값과 최솟값", ["최댓값만", "최솟값만", "극댓값과 극솟값"]),
             ("f(x)가 [a, b]에서 연속이고 f(a)f(b) &lt; 0이면 방정식 f(x) = 0은 (a, b)에서?", "적어도 하나의 실근을 가져요", ["실근이 없어요", "실근이 정확히 하나예요", "허근만 가져요"]),
             ("사잇값 정리를 쓰기 위해 꼭 필요한 조건은?", "닫힌구간에서 연속", ["미분가능", "증가함수", "다항함수"]),
             ("다항함수는 어떤 구간에서 연속일까요?", "실수 전체", ["양수인 구간만", "정수에서만", "닫힌구간에서만"]),
             ("두 함수 f, g가 x = a에서 연속일 때, x = a에서 항상 연속이라고 할 수 없는 것은?", "f(x) ÷ g(x)", ["f(x) + g(x)", "f(x)g(x)", "f(x) − g(x)"]),
             ("함수 f(x) = |x|는 x = 0에서?", "연속이에요", ["불연속이에요", "정의되지 않아요", "극한이 없어요"]),
             ("함수 f(x) = 1/x는 x = 0에서?", "불연속이에요", ["연속이에요", "미분가능해요", "극한값이 0이에요"]),
             ("좌극한과 우극한이 다르면?", "그 점에서 극한값이 존재하지 않아요", ["극한값은 두 값의 평균이에요", "연속이에요", "미분가능해요"])]
        q, ok, w = R.choice(C)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 미분계수와 도함수
def d_main(kinds=("avg", "def", "shift", "diffc", "concept")):
    def mk():
        how = R.choice(kinds)
        p = rnd_poly(R.choice([2, 3]), lo=-4, hi=4, lead=(1, 2, -1, 3))
        if how == "avg":
            a, b = sorted(R.sample(range(-3, 5), 2))
            v = Fr(peval(p, b) - peval(p, a), b - a)
            return N("함수 f(x) = %s에서 x의 값이 %s에서 %s까지 변할 때의 평균변화율은?" % (px(p), neg(a), neg(b)), v, [peval(p, b) - peval(p, a), Fr(peval(p, b) + peval(p, a), b - a), peval(der(p), b), v + 1],
                     "(f(%s) − f(%s)) ÷ (%s − %s) = (%s − %s) ÷ %d. <b>%s</b>" % (neg(b), neg(a), neg(b), par(a), neg(peval(p, b)), par(peval(p, a)), b - a, neg(v)))
        if how == "def":
            a = R.randint(-3, 3)
            v = peval(der(p), a)
            return N("함수 f(x) = %s에 대하여 <b>%s</b>의 값은?" % (px(p), lim("0", fr("f(%s + h) − f(%s)" % (neg(a), neg(a)), "h"), "h")), v, [peval(p, a), 2 * v, v + 1, -v], "미분계수 f′(%s)예요. f′(x) = %s이므로 <b>%s</b>" % (neg(a), px(der(p)), neg(v)))
        if how == "shift":
            a = R.randint(-2, 3)
            k, m = R.choice([(2, 1), (3, 1), (1, 2), (3, 2), (2, -1), (4, 1)])
            fp = peval(der(p), a)
            v = Fr(k, m) * fp
            sk = "" if k == 1 else str(k)
            return N("함수 f(x) = %s에 대하여 <b>%s</b>의 값은?" % (px(p), lim("0", fr("f(%s + %sh) − f(%s)" % (neg(a), sk, neg(a)), "%sh" % ("" if m == 1 else ("−" if m == -1 else m))), "h")), v, [fp, Fr(m, k) * fp if Fr(m, k) * fp != v else fp * 2, k * fp, v + 1],
                     "f′(%s) = %s이고 %s배가 돼요. <b>%s</b>" % (neg(a), neg(fp), neg(Fr(k, m)), neg(v)))
        if how == "diffc":
            C = [("함수 f(x) = |x|는 x = 0에서?", "연속이지만 미분가능하지 않아요", ["연속이고 미분가능해요", "불연속이지만 미분가능해요", "불연속이고 미분가능하지 않아요"]),
                 ("x = a에서 미분가능한 함수는 x = a에서?", "반드시 연속이에요", ["불연속일 수 있어요", "극값을 가져요", "f(a) = 0이에요"]),
                 ("x = a에서 연속인 함수는 x = a에서?", "미분가능하지 않을 수도 있어요", ["반드시 미분가능해요", "반드시 극값을 가져요", "반드시 불연속이에요"]),
                 ("그래프가 x = a에서 뾰족하게 꺾이면?", "x = a에서 미분가능하지 않아요", ["x = a에서 불연속이에요", "f′(a) = 0이에요", "x = a에서 미분가능해요"]),
                 ("f′(a)의 기하적 의미는?", "x = a에서의 접선의 기울기", ["x = a에서의 함숫값", "y절편", "평균변화율"]),
                 ("평균변화율의 기하적 의미는?", "두 점을 잇는 직선의 기울기", ["접선의 기울기", "곡선의 길이", "넓이"]),
                 ("f(x) = |x − 2|가 미분가능하지 않은 x의 값은?", "x = 2", ["x = 0", "x = −2", "없어요"]),
                 ("x = a에서 불연속인 함수는 x = a에서?", "미분가능하지 않아요", ["미분가능해요", "f′(a) = 0이에요", "극한값이 같아요"])]
            q, ok, w = R.choice(C)
            return M(q, ok, w, "<b>%s</b>" % ok)
        a = R.randint(-3, 3)
        k = R.choice(["fa", "eq"])
        if k == "fa":
            v = peval(der(p), a)
            ok = neg(v)
            return N("함수 f(x) = %s의 x = %s에서의 미분계수는?" % (px(p), neg(a)), v, [peval(p, a), v + 1, -v, peval(der(p), -a)], "f′(x) = %s, f′(%s) = <b>%s</b>" % (px(der(p)), neg(a), neg(v)))
        # 평균변화율 = 미분계수
        b2 = R.randint(1, 4)
        q2 = [1, R.randint(-4, 4), 0]
        # [0, b2]에서 평균변화율 = b2 + q2[1], f′(c) = 2c + q2[1] → c = b2/2
        v = Fr(b2, 2)
        return N("함수 f(x) = %s에서 x의 값이 0에서 %d까지 변할 때의 평균변화율과 x = c에서의 미분계수가 같을 때, c의 값은?" % (px(q2), b2), v, [b2, 0, Fr(b2, 4), v + 1], "평균변화율 %s = 2c %s %d. <b>c = %s</b>" % (neg(b2 + q2[1]), "+" if q2[1] >= 0 else "−", abs(q2[1]), neg(v)))
    return mk


# ------------------------------------------------------------------ 미분법
def r_main(kinds=("poly", "val", "prod", "find", "pow")):
    def mk():
        how = R.choice(kinds)
        if how == "poly":
            p = rnd_poly(R.choice([2, 3, 4]), lo=-6, hi=6, lead=(1, 2, 3, -1, -2, 4))
            ok = px(der(p))
            wrong1 = px([c * (len(p) - 1 - i) for i, c in enumerate(p)][:-1] + [0]) if False else px([c * (len(p) - 1 - i) for i, c in enumerate(p[:-1])] + [p[-1]]) if p[-1] else px([c for c in p[:-1]])
            w = [wrong1, px([c * (len(p) - 1 - i) for i, c in enumerate(p[:-1])] + [0]) if len(p) > 2 else "0", px(antider(p)[:-1]) if True else "", px([c for c in p[:-1]])]
            return M("함수 <b>f(x) = %s</b>의 도함수는?" % px(p), "f′(x) = " + ok, ["f′(x) = " + x for x in w if x != ok], "(xⁿ)′ = nxⁿ⁻¹, 상수의 미분은 0이에요. <b>f′(x) = %s</b>" % ok)
        if how == "val":
            p = rnd_poly(3, lo=-5, hi=5)
            a = R.randint(-3, 3)
            v = peval(der(p), a)
            return N("함수 f(x) = %s에 대하여 f′(%s)의 값은?" % (px(p), neg(a)), v, [peval(p, a), peval(der(der(p)), a), v - p[-2], v + 1], "f′(x) = %s. <b>%s</b>" % (px(der(p)), neg(v)))
        if how == "prod":
            P = [1, nz(-4, 4)]
            Q = [R.choice([1, 2]), R.randint(-3, 3), R.randint(-4, 4)]
            a = R.randint(-2, 2)
            k = R.choice(["val", "exp"])
            prod_d = padd(pmul(der(P), Q), pmul(P, der(Q)))
            if k == "exp":
                ok = px(prod_d)
                return M("함수 <b>f(x) = (%s)(%s)</b>의 도함수는?" % (px(P), px(Q)), "f′(x) = " + ok, ["f′(x) = " + px(pmul(der(P), der(Q))), "f′(x) = " + px(der(Q)), "f′(x) = " + px(padd(pmul(der(P), Q), pmul(P, der(Q)), -1)), "f′(x) = " + px(pmul(P, der(Q)))],
                         "{f(x)g(x)}′ = f′(x)g(x) + f(x)g′(x). <b>f′(x) = %s</b>" % ok)
            v = peval(prod_d, a)
            return N("함수 f(x) = (%s)(%s)에 대하여 f′(%s)의 값은?" % (px(P), px(Q), neg(a)), v, [peval(pmul(der(P), der(Q)), a), peval(pmul(P, Q), a), v + 1, -v], "f′(x) = (%s)′(%s) + (%s)(%s)′. <b>%s</b>" % (px(P), px(Q), px(P), px(Q), neg(v)))
        if how == "pow":
            a, b = R.choice([1, 2, 3]), R.randint(-3, 3)
            n = R.choice([2, 3])
            x0 = R.randint(-2, 2)
            base = [a, b]
            pw = [1]
            for _ in range(n):
                pw = pmul(pw, base)
            v = peval(der(pw), x0)
            return N("함수 f(x) = (%s)<sup>%d</sup>에 대하여 f′(%s)의 값은?" % (px(base), n, neg(x0)), v, [n * peval(base, x0) ** (n - 1), peval(pw, x0), v + a, a * n], "전개하거나 곱의 미분법으로 f′(x) = %d(%s)<sup>%s</sup> × %d. <b>%s</b>" % (n, px(base), "" if n == 2 else n - 1, a, neg(v)) if n > 1 else None)
        # find a, b: f(x) = x² + ax + b, f(1) = p, f′(1) = q
        a, b = R.randint(-5, 5), R.randint(-5, 5)
        x0 = R.randint(-2, 2)
        f = [1, a, b]
        fp = peval(der(f), x0)
        fv = peval(f, x0)
        kind = R.choice(["a", "b", "ab"])
        v = {"a": a, "b": b, "ab": a * b}[kind]
        return N("함수 f(x) = x² + ax + b에 대하여 f(%s) = %s, f′(%s) = %s일 때, %s의 값은? (a, b는 상수)" % (neg(x0), neg(fv), neg(x0), neg(fp), {"a": "a", "b": "b", "ab": "ab"}[kind]), v, [{"a": b, "b": a, "ab": a + b}[kind], -v if v else 1, v + 1, fp], "f′(x) = 2x + a이므로 a = %s, b = %s. <b>%s</b>" % (neg(a), neg(b), neg(v)))
    return mk


# ------------------------------------------------------------------ 접선과 평균값 정리
def t_main(kinds=("at", "slope", "outside", "mvt", "rolle")):
    def mk():
        how = R.choice(kinds)
        p = rnd_poly(R.choice([2, 3]), lo=-4, hi=4, lead=(1, -1, 2))
        if how == "at":
            a = R.randint(-2, 3)
            m, y0 = peval(der(p), a), peval(p, a)
            ok = "y = " + px([m, y0 - m * a])
            return M("곡선 y = %s 위의 점 (%s, %s)에서의 접선의 방정식은?" % (px(p), neg(a), neg(y0)), ok, ["y = " + px([y0, m - y0 * a]) if y0 != m else "y = " + px([m, y0]), "y = " + px([m, y0 + m * a]), "y = " + px([-Fr(1, m) if m else 1, y0 + (Fr(a, m) if m else 0)]), "y = " + px([m, y0])],
                     "기울기 f′(%s) = %s, y − %s = %s(x − %s). <b>%s</b>" % (neg(a), neg(m), par(y0), neg(m), par(a), ok))
        if how == "slope":
            q = [1, R.randint(-4, 4), R.randint(-4, 4)]
            m = R.randint(-5, 5)
            # 2x + q1 = m → x = (m − q1)/2
            x0 = Fr(m - q[1], 2)
            if x0.denominator != 1:
                return None
            y0 = peval(q, x0)
            ok = "y = " + px([m, y0 - m * x0])
            return M("곡선 y = %s에 접하고 기울기가 %s인 직선의 방정식은?" % (px(q), neg(m)), ok, ["y = " + px([m, y0 + m * x0]), "y = " + px([m, y0]), "y = " + px([m, -(y0 - m * x0)]) if y0 - m * x0 else "y = " + px([m, 1]), "y = " + px([-m, y0 + m * x0]) if m else "y = 1"],
                     "f′(x) = %s = %s에서 접점 (%s, %s). <b>%s</b>" % (px(der(q)), neg(m), neg(x0), neg(y0), ok))
        if how == "outside":
            # y = x² 위 접선이 (0, −k²) 지남 → 접점 (±k, k²), 기울기 ±2k
            k = R.randint(1, 4)
            ok = "y = %s, y = %s" % (px([2 * k, -k * k]), px([-2 * k, -k * k]))
            return M("점 (0, %s)에서 곡선 y = x²에 그은 접선의 방정식을 모두 구하면?" % neg(-k * k), ok, ["y = %s" % px([2 * k, -k * k]), "y = %s, y = %s" % (px([k, -k * k]), px([-k, -k * k])), "y = %s, y = %s" % (px([2 * k, k * k]), px([-2 * k, k * k]))],
                     "접점 (t, t²)에서 접선 y = 2tx − t²이 (0, %s)를 지나므로 t = ±%d. <b>%s</b>" % (neg(-k * k), k, ok))
        if how == "mvt":
            a, b = sorted(R.sample(range(-3, 6), 2))
            kind = R.choice(["quad", "cubic"])
            if kind == "quad":
                q = [R.choice([1, 2, -1]), R.randint(-4, 4), R.randint(-4, 4)]
                v = Fr(a + b, 2)
                return N("함수 f(x) = %s에 대하여 닫힌구간 [%s, %s]에서 평균값 정리를 만족하는 c의 값은?" % (px(q), neg(a), neg(b)), v, [Fr(b - a, 2), a, b, v + 1], "이차함수에서는 c가 구간의 가운데예요. (f(%s) − f(%s)) ÷ %d = f′(c). <b>c = %s</b>" % (neg(b), neg(a), b - a, neg(v)))
            # f = x³, [0, b] : b² = 3c² → c = b/√3
            bb = R.choice([3, 6, 9])
            c = surd(Fr(bb, 3), 3)
            return M("함수 f(x) = x³에 대하여 닫힌구간 [0, %d]에서 평균값 정리를 만족하는 c의 값은?" % bb, c, [neg(Fr(bb, 2)), surd(Fr(bb, 2), 2), neg(Fr(bb, 3)), surd(1, bb)], "%d² = 3c² → c = %d ÷ √3. <b>%s</b>" % (bb, bb, c))
        r1, r2 = sorted(R.sample(range(-4, 6), 2))
        q = [1, -(r1 + r2), r1 * r2]
        v = Fr(r1 + r2, 2)
        return N("함수 f(x) = %s에 대하여 닫힌구간 [%s, %s]에서 롤의 정리를 만족하는 c의 값은?" % (px(q), neg(r1), neg(r2)), v, [r1 + r2, Fr(r2 - r1, 2), r1 * r2, v + 1], "f(%s) = f(%s) = 0이므로 f′(c) = 2c − %s = 0. <b>c = %s</b>" % (neg(r1), neg(r2), par(r1 + r2), neg(v)))
    return mk


# ------------------------------------------------------------------ 증가·감소와 극값
def cubic(r1, r2, a=1, d=0):
    """f′(x) = 3a(x − r1)(x − r2)를 갖는 삼차함수 f(x) = a x³ − (3a/2)(r1 + r2) x² + 3a r1 r2 x + d"""
    return [a, Fr(-3 * a * (r1 + r2), 2), 3 * a * r1 * r2, d]


def i_main(kinds=("inc", "dec", "max", "min", "always", "ext_k")):
    def mk():
        how = R.choice(kinds)
        r1, r2 = sorted(R.sample(range(-4, 5), 2))
        if (r1 + r2) % 2:
            return None
        a = R.choice([1, -1, 2])
        d = R.randint(-5, 5)
        f = cubic(r1, r2, a, d)
        if how in ("inc", "dec"):
            inc_out = a > 0
            want_out = (how == "inc") == inc_out
            ok = ("x ≤ %s 또는 x ≥ %s" % (neg(r1), neg(r2))) if want_out else ("%s ≤ x ≤ %s" % (neg(r1), neg(r2)))
            alt = ("%s ≤ x ≤ %s" % (neg(r1), neg(r2))) if want_out else ("x ≤ %s 또는 x ≥ %s" % (neg(r1), neg(r2)))
            return M("함수 <b>f(x) = %s</b>가 %s하는 x의 값의 범위는?" % (px(f), "증가" if how == "inc" else "감소"), ok, [alt, "x ≤ %s 또는 x ≥ %s" % (neg(-r2), neg(-r1)), "%s ≤ x ≤ %s" % (neg(-r2), neg(-r1))],
                     "f′(x) = %s%s의 부호를 봐요. <b>%s</b>" % ("" if 3 * a == 1 else ("−" if 3 * a == -1 else neg(3 * a)), "".join("x" if r == 0 else "(%s)" % px([1, -r]) for r in (r1, r2)), ok))
        if how in ("max", "min"):
            xmax = r1 if a > 0 else r2
            xmin = r2 if a > 0 else r1
            x0 = xmax if how == "max" else xmin
            v = peval(f, x0)
            other = peval(f, xmin if how == "max" else xmax)
            return N("함수 <b>f(x) = %s</b>의 %s은?" % (px(f), "극댓값" if how == "max" else "극솟값"), v, [other, x0, v + a, d], "f′(x) = 0인 x = %s, %s 중 %s에서 %s. <b>%s</b>" % (neg(r1), neg(r2), neg(x0), "극대" if how == "max" else "극소", neg(v)))
        if how == "always":
            # f(x) = x³ + kx² + 3x 가 실수 전체에서 증가 → 3x² + 2kx + 3 ≥ 0 → k² ≤ 9 → −3 ≤ k ≤ 3
            aa, c = R.choice([(1, 3), (1, 12), (1, 27), (3, 1), (3, 4), (3, 9), (2, 6), (2, 24), (1, 48), (3, 12)])
            lim_ = math.isqrt(3 * aa * c)
            if lim_ * lim_ != 3 * aa * c:
                return None
            ok = "−%d ≤ k ≤ %d" % (lim_, lim_)
            return M("함수 f(x) = %s + kx² + %sx가 실수 전체에서 증가할 때, 상수 k의 값의 범위는?" % (px([aa, 0, 0, 0]), "" if c == 1 else c), ok, ["−%d &lt; k &lt; %d" % (lim_, lim_), "k ≤ −%d 또는 k ≥ %d" % (lim_, lim_), "−%d ≤ k ≤ %d" % (3 * aa * c, 3 * aa * c), "k ≥ %d" % lim_],
                     "f′(x) = %dx² + 2kx + %d ≥ 0이 항상 성립: D/4 = k² − %d ≤ 0. <b>%s</b>" % (3 * aa, c, 3 * aa * c, ok))
        # ext_k: f(x) = x³ − 3x + k 의 극댓값이 m → k
        s = R.randint(1, 3)
        k = R.randint(-6, 6)
        g = [1, 0, -3 * s * s, k]
        mxv = peval(g, -s)
        mnv = peval(g, s)
        kind = R.choice(["max", "min"])
        target = mxv if kind == "max" else mnv
        return N("함수 f(x) = %s + k의 %s이 %s일 때, 상수 k의 값은?" % (px([1, 0, -3 * s * s, 0]), "극댓값" if kind == "max" else "극솟값", neg(target)), k, [target, -k, mnv if kind == "max" else mxv, k + 2 * s ** 3],
                 "f′(x) = 3(x + %d)(x − %d), x = %s에서 %s: %s + k = %s. <b>k = %s</b>" % (s, s, neg(-s if kind == "max" else s), "극대" if kind == "max" else "극소", neg(target - k), neg(target), neg(k)))
    return mk


# ------------------------------------------------------------------ 그래프와 최대·최소
def g_main(kinds=("closed", "roots", "shape", "pic")):
    def mk():
        how = R.choice(kinds)
        r1, r2 = sorted(R.sample(range(-3, 4), 2))
        if (r1 + r2) % 2:
            return None
        a = R.choice([1, -1])
        d = R.randint(-4, 4)
        f = cubic(r1, r2, a, d)
        if how == "closed":
            lo = r1 - R.randint(0, 2)
            hi = r2 + R.randint(0, 2)
            k = R.choice(["max", "min"])
            vals = {x: peval(f, x) for x in (lo, hi, r1, r2)}
            v = max(vals.values()) if k == "max" else min(vals.values())
            return N("닫힌구간 [%s, %s]에서 함수 f(x) = %s의 %s은?" % (neg(lo), neg(hi), px(f), "최댓값" if k == "max" else "최솟값"), v, [x for x in vals.values() if x != v] + [v + 1, d],
                     "극값 f(%s) = %s, f(%s) = %s와 양 끝값 f(%s) = %s, f(%s) = %s를 비교해요. <b>%s</b>" % (neg(r1), neg(vals[r1]), neg(r2), neg(vals[r2]), neg(lo), neg(vals[lo]), neg(hi), neg(vals[hi]), neg(v)))
        if how == "roots":
            s = R.randint(1, 3)
            g = [1, 0, -3 * s * s, 0]
            M_, m_ = 2 * s ** 3, -2 * s ** 3
            k = R.choice([M_, m_, M_ + R.randint(1, 5), m_ - R.randint(1, 5), R.randint(m_ + 1, M_ - 1)])
            n = 3 if m_ < k < M_ else (2 if k in (m_, M_) else 1)
            return N("방정식 <b>%s = %s</b>의 서로 다른 실근의 개수는?" % (px(g), neg(k)), n, [x for x in (0, 1, 2, 3) if x != n], "y = %s의 극댓값 %d, 극솟값 %s와 직선 y = %s의 교점의 개수예요. <b>%d개</b>" % (px(g), M_, neg(m_), neg(k), n), f=lambda v: "%s개" % neg(v))
        if how == "shape":
            S_ = [("삼차함수 f(x)가 극값을 가질 조건은?", "f′(x) = 0이 서로 다른 두 실근을 가져요", ["f′(x) = 0이 중근을 가져요", "f(x) = 0이 실근을 가져요", "f′(x) &gt; 0이에요"]),
                  ("f′(a) = 0이고 x = a의 좌우에서 f′(x)의 부호가 양에서 음으로 바뀌면?", "x = a에서 극대", ["x = a에서 극소", "극값이 없어요", "x = a에서 불연속"]),
                  ("f′(a) = 0이지만 x = a의 좌우에서 f′(x)의 부호가 바뀌지 않으면?", "x = a에서 극값을 갖지 않아요", ["x = a에서 극대", "x = a에서 극소", "x = a에서 최댓값"]),
                  ("최고차항의 계수가 양수인 삼차함수의 그래프는 x → ∞일 때?", "y → ∞", ["y → −∞", "y → 0", "y → 1"]),
                  ("닫힌구간에서 연속인 함수의 최댓값은 어디에서 생길까요?", "극값 또는 구간의 양 끝", ["극댓값에서만", "구간의 양 끝에서만", "x = 0에서만"]),
                  ("f(x) = x³의 x = 0에서의 성질은?", "f′(0) = 0이지만 극값이 아니에요", ["극대예요", "극소예요", "미분가능하지 않아요"]),
                  ("삼차함수 f(x)의 극댓값과 극솟값의 곱이 음수이면 f(x) = 0의 실근은?", "서로 다른 세 실근", ["한 실근", "중근과 다른 한 근", "실근이 없어요"]),
                  ("삼차함수 f(x)의 극댓값과 극솟값의 곱이 0이면 f(x) = 0의 실근은?", "중근과 다른 한 실근", ["서로 다른 세 실근", "한 실근", "실근이 없어요"])]
            q, ok, w = R.choice(S_)
            return M(q, ok, w, "<b>%s</b>" % ok)
        if abs(peval(f, r1)) > 6 or abs(peval(f, r2)) > 6 or r2 - r1 > 4:
            return None
        pic = graph([(lambda x, f=f: float(peval(f, Fr(x).limit_denominator(1000))), BLUE, "")], (-5, 5, 1), (-6, 6, 1), pts=[(r1, peval(f, r1), ""), (r2, peval(f, r2), "")], label="삼차함수의 그래프")
        k = R.choice(["max", "min", "inc"])
        xmax, xmin = (r1, r2) if a > 0 else (r2, r1)
        if k == "inc":
            ok = ("x ≤ %s 또는 x ≥ %s" % (neg(r1), neg(r2))) if a > 0 else ("%s ≤ x ≤ %s" % (neg(r1), neg(r2)))
            alt = ("%s ≤ x ≤ %s" % (neg(r1), neg(r2))) if a > 0 else ("x ≤ %s 또는 x ≥ %s" % (neg(r1), neg(r2)))
            return M("그림은 삼차함수 y = f(x)의 그래프예요(빨간 점은 극값). f′(x) ≥ 0인 x의 값의 범위는?%s" % pic, ok, [alt, "x ≥ %s" % neg(r2), "x ≤ %s" % neg(r1)], "f(x)가 증가하는 범위예요. <b>%s</b>" % ok)
        x0 = xmax if k == "max" else xmin
        v = peval(f, x0)
        return N("그림은 삼차함수 y = f(x)의 그래프예요(빨간 점은 극값). f(x)의 %s은?%s" % ("극댓값" if k == "max" else "극솟값", pic), v, [x0, peval(f, xmin if k == "max" else xmax), v + 1, -v if v else 2], "%s인 점의 y좌표예요. <b>%s</b>" % ("극대" if k == "max" else "극소", neg(v)))
    return mk


# ------------------------------------------------------------------ 방정식·부등식·속도
def a_main(kinds=("count", "kroot", "ineq", "vel", "acc", "stop")):
    def mk():
        how = R.choice(kinds)
        if how == "count":
            s_ = R.randint(1, 3)
            c = R.randint(-6, 6)
            g = [2, -3 * s_, 0, c] if R.random() < 0.5 else [1, 0, -3 * s_ * s_, c]
            ext = [peval(g, 0), peval(g, s_)] if g[0] == 2 else [peval(g, -s_), peval(g, s_)]
            Mx, mn = max(ext), min(ext)
            n = 3 if mn < 0 < Mx else (2 if 0 in (Mx, mn) else 1)
            return N("방정식 <b>%s = 0</b>의 서로 다른 실근의 개수는?" % px(g), n, [x for x in (0, 1, 2, 3) if x != n], "극댓값 %s, 극솟값 %s의 부호를 봐요. <b>%d개</b>" % (neg(Mx), neg(mn), n), f=lambda v: "%s개" % neg(v))
        if how == "kroot":
            r1, r2 = sorted(R.sample(range(-3, 5), 2))
            aa = 1 if (r1 + r2) % 2 == 0 else 2
            h = cubic(r1, r2, aa, 0)
            Mx0, mn0 = peval(h, r1), peval(h, r2)
            if any(Fr(c).denominator != 1 for c in h):
                return None
            kind = R.choice(["three", "two"])
            if kind == "three":
                ok = "%s &lt; k &lt; %s" % (neg(-Mx0), neg(-mn0))
                return M("방정식 <b>%s + k = 0</b>이 서로 다른 세 실근을 갖도록 하는 실수 k의 값의 범위는?" % px(h), ok, ["%s ≤ k ≤ %s" % (neg(-Mx0), neg(-mn0)), "%s &lt; k &lt; %s" % (neg(mn0), neg(Mx0)), "k &lt; %s 또는 k &gt; %s" % (neg(-Mx0), neg(-mn0))],
                         "y = %s와 직선 y = −k가 세 점에서 만나야 하므로 %s &lt; −k &lt; %s. <b>%s</b>" % (px(h), neg(mn0), neg(Mx0), ok))
            ok = "k = %s 또는 k = %s" % (neg(-Mx0), neg(-mn0))
            return M("방정식 <b>%s + k = 0</b>이 서로 다른 두 실근을 갖도록 하는 실수 k의 값은?" % px(h), ok, ["k = %s 또는 k = %s" % (neg(Mx0), neg(mn0)), "k = %s" % neg(-Mx0), "%s &lt; k &lt; %s" % (neg(-Mx0), neg(-mn0))],
                     "직선 y = −k가 극대 또는 극소인 점을 지나야 해요(극댓값 %s, 극솟값 %s). <b>%s</b>" % (neg(Mx0), neg(mn0), ok))
        if how == "ineq":
            s_ = R.randint(1, 4)
            kind = R.choice(["c", "q", "p4"])
            if kind == "c":
                v = 2 * s_ ** 3
                return N("x ≥ 0인 모든 실수 x에 대하여 부등식 <b>%s + k ≥ 0</b>이 성립하도록 하는 실수 k의 최솟값은?" % px([1, 0, -3 * s_ * s_, 0]), v, [s_ ** 3, 3 * s_ * s_, -v, v + 1], "x ≥ 0에서 최솟값은 x = %d일 때 %s + k ≥ 0. <b>%d</b>" % (s_, neg(-v), v))
            if kind == "q":
                v = s_ ** 3
                return N("x ≥ 0인 모든 실수 x에 대하여 부등식 <b>%s + k ≥ 0</b>이 성립하도록 하는 실수 k의 최솟값은?" % px([2, -3 * s_, 0, 0]), v, [2 * s_ ** 3, 3 * s_, -v, v + 1], "x ≥ 0에서 최솟값은 x = %d일 때 %s + k ≥ 0. <b>%d</b>" % (s_, neg(-v), v))
            if s_ > 3:
                return None
            v = 3 * s_ ** 4
            return N("모든 실수 x에 대하여 부등식 <b>%s + k ≥ 0</b>이 성립하도록 하는 실수 k의 최솟값은?" % px([1, 0, 0, -4 * s_ ** 3, 0]), v, [s_ ** 4, 4 * s_ ** 3, -v, v + 1], "f′(x) = 4x³ − %d = 0에서 x = %d일 때 최소: %s + k ≥ 0. <b>%d</b>" % (4 * s_ ** 3, s_, neg(-v), v))
        # 위치 x(t) = t³ + bt² + ct
        r1, r2 = sorted(R.sample(range(1, 8), 2))
        aa = 1 if (r1 + r2) % 2 == 0 else 2
        pos = cubic(r1, r2, aa, 0)
        v_ = der(pos)
        a_ = der(v_)
        if how == "vel":
            t = R.randint(1, 6)
            v = peval(v_, t)
            return N("수직선 위를 움직이는 점 P의 시각 t에서의 위치가 x(t) = %s일 때, t = %d에서 점 P의 속도는?" % (px(pos, "t"), t), v, [peval(pos, t), peval(a_, t), v + 1, -v if v else 2], "v(t) = x′(t) = %s. <b>%s</b>" % (px(v_, "t"), neg(v)))
        if how == "acc":
            t = R.randint(1, 6)
            v = peval(a_, t)
            return N("수직선 위를 움직이는 점 P의 시각 t에서의 위치가 x(t) = %s일 때, t = %d에서 점 P의 가속도는?" % (px(pos, "t"), t), v, [peval(v_, t), peval(pos, t), v + 6, -v if v else 3], "a(t) = v′(t) = %s. <b>%s</b>" % (px(a_, "t"), neg(v)))
        ok = "t = %d, t = %d" % (r1, r2)
        return M("수직선 위를 움직이는 점 P의 시각 t에서의 위치가 x(t) = %s일 때, 점 P가 운동 방향을 바꾸는 시각은?" % px(pos, "t"), ok, ["t = %s" % neg(Fr(r1 + r2, 2)), "t = 0, t = %d" % r2, "t = %d" % (r1 * r2), "t = %d, t = %d" % (r1 + 1, r2 + 1)],
                 "v(t) = %d(t − %d)(t − %d) = 0이고 부호가 바뀌어요. <b>%s</b>" % (3 * aa, r1, r2, ok))
    return mk


# ------------------------------------------------------------------ 부정적분
def n_main(kinds=("basic", "val", "find", "deriv", "concept")):
    def mk():
        how = R.choice(kinds)
        p = rnd_poly(R.choice([1, 2, 3]), lo=-6, hi=6, lead=(1, 2, 3, 4, 6, -3))
        F = antider(p)
        if how == "basic":
            ok = px(F[:-1] + [0]) + " + C" if any(F) else "C"
            ok = (px(F) + " + C")
            w = [px(der(p)) + " + C", px(F), px([c * (len(p) - i) for i, c in enumerate(p)] + [0]) + " + C", px([c for c in p] + [0]) + " + C"]
            return M("<b>∫(%s) dx</b>를 구하면? (C는 적분상수)" % px(p), ok, [x for x in w if x != ok], "∫xⁿ dx = xⁿ⁺¹/(n + 1) + C. <b>%s</b>" % ok)
        if how == "val":
            c0 = R.randint(-5, 5)
            x0 = R.randint(-2, 3)
            Fc = F[:-1] + [c0]
            v = peval(Fc, x0)
            return N("F′(x) = %s이고 F(0) = %s일 때, F(%s)의 값은?" % (px(p), neg(c0), neg(x0)), v, [peval(F, x0), peval(der(p), x0) if len(p) > 1 else v + 2, v + 1, peval(p, x0)], "F(x) = %s. <b>%s</b>" % (px(Fc), neg(v)))
        if how == "find":
            x0 = R.randint(-2, 2)
            y0 = R.randint(-6, 6)
            Cc = y0 - peval(F, x0)
            Fc = F[:-1] + [Cc]
            ok = "f(x) = " + px(Fc)
            return M("f′(x) = %s이고 곡선 y = f(x)가 점 (%s, %s)를 지날 때, f(x)는?" % (px(p), neg(x0), neg(y0)), ok, ["f(x) = " + px(F[:-1] + [y0]), "f(x) = " + px(F[:-1] + [-Cc]) if Cc else "f(x) = " + px(F[:-1] + [1]), "f(x) = " + px(F), "f(x) = " + px(der(p) + [y0])],
                     "f(x) = %s + C, f(%s) = %s에서 C = %s. <b>%s</b>" % (px(F), neg(x0), neg(y0), neg(Cc), ok))
        if how == "deriv":
            x0 = R.randint(-3, 3)
            v = peval(p, x0)
            return N("<b>d/dx ∫(%s) dx</b>의 x = %s에서의 값은?" % (px(p), neg(x0)), v, [peval(F, x0), peval(der(p), x0) if len(p) > 1 else v + 1, 0, v + 1], "d/dx ∫f(x) dx = f(x)예요. f(%s) = <b>%s</b>" % (neg(x0), neg(v)))
        C = [("함수 F(x)의 도함수가 f(x)일 때 F(x)를 f(x)의 무엇이라고 할까요?", "부정적분", ["도함수", "미분계수", "평균변화율"]),
             ("∫f(x) dx = F(x) + C에서 C는?", "적분상수", ["미분계수", "최고차항의 계수", "기울기"]),
             ("∫k dx (k는 상수)는?", "kx + C", ["k + C", "0", "kx²/2 + C"]),
             ("∫{f(x) + g(x)} dx와 같은 것은?", "∫f(x) dx + ∫g(x) dx", ["∫f(x) dx × ∫g(x) dx", "f(x) + g(x)", "∫f(x)g(x) dx"]),
             ("∫x⁴ dx는?", "x⁵/5 + C", ["4x³ + C", "x⁵ + C", "x⁴/4 + C"]),
             ("∫(x + 1)(x − 1) dx는?", "x³/3 − x + C", ["x²/2 − 1 + C", "x³ − x + C", "(x²/2 + x)(x²/2 − x) + C"]),
             ("두 부정적분 F(x), G(x)가 같은 f(x)의 부정적분일 때 F(x) − G(x)는?", "상수", ["0이 아닌 일차식", "f(x)", "x"])]
        q, ok, w = R.choice(C)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 정적분
def df_main(kinds=("basic", "split", "rev", "sym", "ftc", "abs")):
    def mk():
        how = R.choice(kinds)
        p = rnd_poly(R.choice([1, 2, 2, 3]), lo=-5, hi=5, lead=(1, 2, 3, -1, 3, 6))
        a, b = sorted(R.sample(range(-3, 4), 2))
        if how == "basic":
            v = integ(p, a, b)
            return N("<b>%s</b>의 값은?" % I(a, b, px(p)), v, [integ(p, b, a), peval(p, b) - peval(p, a), v + 1, peval(antider(p), b)], "[%s]<sub>%s</sub><sup>%s</sup> = <b>%s</b>" % (px(antider(p)), neg(a), neg(b), neg(v)))
        if how == "split":
            c = R.randint(b + 1, b + 3)
            v = integ(p, a, c)
            return N("<b>%s + %s</b>의 값은?" % (I(a, b, px(p)), I(b, c, px(p))), v, [integ(p, a, b), integ(p, b, c), v + integ(p, a, b), -v], "∫<sub>a</sub><sup>b</sup> + ∫<sub>b</sub><sup>c</sup> = ∫<sub>a</sub><sup>c</sup>. <b>%s</b>" % neg(v))
        if how == "rev":
            v = integ(p, b, a)
            k = R.choice(["rev", "same"])
            if k == "same":
                return N("<b>%s</b>의 값은?" % I(a, a, px(p)), 0, [peval(p, a), peval(antider(p), a), 1, 2 * a], "위끝과 아래끝이 같으면 0이에요. <b>0</b>")
            return N("<b>%s</b>의 값은?" % I(b, a, px(p)), v, [-v, peval(p, a) - peval(p, b), v + 1, 0], "∫<sub>b</sub><sup>a</sup> = −∫<sub>a</sub><sup>b</sup>. <b>%s</b>" % neg(v))
        if how == "sym":
            k = R.randint(1, 3)
            q = [R.choice([1, 2, -1]), R.randint(-4, 4), R.randint(-4, 4), R.randint(-4, 4)]
            even = [0, q[1], 0, q[3]]
            v = integ(q, -k, k)
            return N("<b>%s</b>의 값은?" % I(-k, k, px(q)), v, [integ(q, 0, k), integ([q[0], 0, q[2], 0], 0, k) * 2 if integ([q[0], 0, q[2], 0], 0, k) * 2 != v else v + 1, 0 if v else 1, v * 2],
                     "홀수 차수의 항은 0, 짝수 차수의 항은 2∫<sub>0</sub><sup>%d</sup>. <b>%s</b>" % (k, neg(v)))
        if how == "ftc":
            kind = R.choice(["d", "find"])
            if kind == "d":
                x0 = R.randint(-3, 3)
                v = peval(p, x0)
                return N("함수 g(x) = ∫<sub>%s</sub><sup>x</sup> (%s) dt에 대하여 g′(%s)의 값은?" % (neg(a), px(p, "t"), neg(x0)), v, [integ(p, a, x0), peval(der(p), x0) if len(p) > 1 else v + 1, v + 1, peval(p, a)], "d/dx ∫<sub>a</sub><sup>x</sup> f(t) dt = f(x). <b>%s</b>" % neg(v))
            # ∫_1^x f(t) dt = x² + kx − 3 → k?: x = 1 대입 → 0 = 1 + k − 3
            c0 = R.randint(-6, 6)
            x0 = R.choice([1, 2, -1])
            k = Fr(-x0 * x0 - c0, x0)
            if k.denominator != 1:
                return None
            k = int(k)
            fx = "2x %s %d" % ("+" if k >= 0 else "−", abs(k)) if k else "2x"
            return N("모든 실수 x에 대하여 ∫<sub>%s</sub><sup>x</sup> f(t) dt = x² + kx %s %d일 때, 상수 k의 값은?" % (neg(x0), "+" if c0 >= 0 else "−", abs(c0)), k, [-k, c0, k + 1, x0 * x0 + c0],
                     "양변에 x = %s를 대입하면 좌변은 0이므로 %s = 0. k = %s이고, 양변을 미분하면 f(x) = %s. <b>%s</b>" % (neg(x0), poly2({(1, 0): x0, (0, 0): x0 * x0 + c0}, ("k", "_")), neg(k), fx, neg(k)))
        # abs: ∫_0^c |x − m| dx
        m = R.randint(1, 4)
        c = m + R.randint(1, 4)
        v = Fr(m * m, 2) + Fr((c - m) ** 2, 2)
        return N("<b>∫<sub>0</sub><sup>%d</sup> |x − %d| dx</b>의 값은?" % (c, m), v, [Fr(c * c, 2) - m * c, Fr((c - m) ** 2, 2), Fr(m * m, 2), v + 1], "x = %d를 기준으로 나누어 ∫<sub>0</sub><sup>%d</sup> (%d − x) dx + ∫<sub>%d</sub><sup>%d</sup> (x − %d) dx. <b>%s</b>" % (m, m, m, m, c, m, neg(v)))
    return mk


# ------------------------------------------------------------------ 넓이
def ar_main(kinds=("axis", "below", "pl", "pp", "cubic", "pic")):
    def mk():
        how = R.choice(kinds)
        if how == "axis":
            r1, r2 = sorted(R.sample(range(-4, 6), 2))
            a = R.choice([1, -1, 2, 3])
            f = pmul([a], pmul([1, -r1], [1, -r2]))
            v = Fr(abs(a) * (r2 - r1) ** 3, 6)
            return N("곡선 y = %s와 x축으로 둘러싸인 부분의 넓이는?" % px(f), v, [integ(f, r1, r2), v * 2, Fr(abs(a) * (r2 - r1) ** 3, 3), v + 1] if integ(f, r1, r2) != v else [v * 2, -v, Fr(abs(a) * (r2 - r1) ** 2, 2), v + 1],
                     "교점 x = %s, %s. |∫<sub>%s</sub><sup>%s</sup> f(x) dx| = <b>%s</b>" % (neg(r1), neg(r2), neg(r1), neg(r2), neg(v)))
        if how == "below":
            k = R.randint(1, 4)
            c = R.randint(1, 3)
            a = R.choice([1, 2, -1])
            top = k + c
            f = [a, 0, -a * k * k]
            part1 = abs(integ(f, 0, k))
            part2 = abs(integ(f, k, top))
            v = part1 + part2
            return N("곡선 y = %s와 x축 및 두 직선 x = 0, x = %d로 둘러싸인 부분의 넓이는?" % (px(f), top), v, [abs(integ(f, 0, top)), abs(part2 - part1) if part2 != part1 else v * 2, part2, v + 1],
                     "x = %d에서 부호가 바뀌어요. %s + %s = <b>%s</b>" % (k, neg(part1), neg(part2), neg(v)))
        if how == "pl":
            r1, r2 = sorted(R.sample(range(-3, 5), 2))
            m, c = r1 + r2, -r1 * r2
            v = Fr((r2 - r1) ** 3, 6)
            return N("곡선 y = x²과 직선 y = %s로 둘러싸인 부분의 넓이는?" % px([m, c]), v, [v * 2, Fr((r2 - r1) ** 2, 2), integ([1, -m, -c], r1, r2), v + 1] if integ([1, -m, -c], r1, r2) != v else [v * 2, -v, Fr((r2 - r1) ** 2, 2), v + 1],
                     "교점 x = %s, %s. ∫<sub>%s</sub><sup>%s</sup> {(%s) − x²} dx. <b>%s</b>" % (neg(r1), neg(r2), neg(r1), neg(r2), px([m, c]), neg(v)))
        if how == "pp":
            k = R.randint(1, 3)
            p0 = R.randint(-3, 3)
            q0 = p0 + 2 * k * k
            v = Fr(8 * k ** 3, 3)
            return N("두 곡선 y = %s, y = %s로 둘러싸인 부분의 넓이는?" % (px([1, 0, p0]), px([-1, 0, q0])), v, [Fr(4 * k ** 3, 3), Fr(16 * k ** 3, 3), 2 * k ** 3, v + 1], "교점 x = ±%d. ∫<sub>−%d</sub><sup>%d</sup> (%d − 2x²) dx = <b>%s</b>" % (k, k, k, 2 * k * k, neg(v)))
        if how == "cubic":
            k = R.randint(1, 3)
            a = R.choice([1, 2, -1])
            v = Fr(abs(a) * k ** 4, 2)
            return N("곡선 y = %s와 x축으로 둘러싸인 부분의 넓이는?" % px([a, 0, -a * k * k, 0]), v, [0, Fr(k ** 4, 4), k ** 4, v + 1], "x = −%d, 0, %d에서 만나요. 두 부분의 넓이가 같으므로 2|∫<sub>0</sub><sup>%d</sup> (%s) dx| = <b>%s</b>" % (k, k, k, px([a, 0, -a * k * k, 0]), neg(v)))
        r1, r2 = sorted(R.sample(range(-4, 5), 2))
        if r2 - r1 < 2:
            return None
        sgn = R.choice([1, -1])
        f = pmul([-sgn], pmul([1, -r1], [1, -r2]))
        top = abs(peval(f, Fr(r1 + r2, 2)))
        if top > 5:
            return None
        pic = graph([(lambda x, f=f: float(peval(f, Fr(x).limit_denominator(1000))), BLUE, "")], (-5, 5, 1), (-3, 6, 1) if sgn > 0 else (-6, 3, 1), pts=[(r1, 0, ""), (r2, 0, "")], label="곡선과 x축")
        v = Fr((r2 - r1) ** 3, 6)
        return N("그림은 곡선 y = %s예요. 이 곡선과 x축으로 둘러싸인 부분의 넓이는?%s" % (px(f), pic), v, [v * 2, Fr((r2 - r1) ** 2, 2), top * (r2 - r1), v + 1], "|∫<sub>%s</sub><sup>%s</sup> (%s) dx| = <b>%s</b>" % (neg(r1), neg(r2), px(f), neg(v)))
    return mk


# ------------------------------------------------------------------ 속도와 거리
def v_main(kinds=("pos", "change", "dist", "back", "up")):
    def mk():
        how = R.choice(kinds)
        if how in ("pos", "change", "dist", "back"):
            r = R.randint(1, 5)
            a = R.choice([1, 2, 3, 4])
            v = [a, -a * r]
            T = r + R.randint(1, 4)
            if how == "pos":
                x0 = R.randint(-5, 5)
                t = R.randint(1, 5)
                val = x0 + integ(v, 0, t)
                return N("수직선 위를 움직이는 점 P의 시각 t에서의 속도가 v(t) = %s이고 t = 0일 때 위치가 %s예요. t = %d에서 점 P의 위치는?" % (px(v, "t"), neg(x0), t), val, [integ(v, 0, t), val - 2 * x0 if x0 else val + 1, peval(v, t), val + 1],
                         "x(%d) = %s + ∫<sub>0</sub><sup>%d</sup> v(t) dt. <b>%s</b>" % (t, neg(x0), t, neg(val)))
            if how == "change":
                val = integ(v, 0, T)
                return N("속도가 v(t) = %s인 점 P의 t = 0에서 t = %d까지 위치의 변화량은?" % (px(v, "t"), T), val, [integ([abs(a), 0], 0, T) if a else val + 1, Fr(a * r * r, 2) + Fr(a * (T - r) ** 2, 2), peval(v, T), val + 1], "∫<sub>0</sub><sup>%d</sup> v(t) dt = <b>%s</b>" % (T, neg(val)))
            if how == "dist":
                val = Fr(a * r * r, 2) + Fr(a * (T - r) ** 2, 2)
                return N("속도가 v(t) = %s인 점 P가 t = 0에서 t = %d까지 움직인 거리는?" % (px(v, "t"), T), val, [integ(v, 0, T), Fr(a * (T - r) ** 2, 2), Fr(a * r * r, 2), val + 1] if integ(v, 0, T) != val else [-val, Fr(a * (T - r) ** 2, 2), Fr(a * r * r, 2), val + 1],
                         "t = %d에서 방향이 바뀌므로 ∫<sub>0</sub><sup>%d</sup> |v(t)| dt = %s + %s. <b>%s</b>" % (r, T, neg(Fr(a * r * r, 2)), neg(Fr(a * (T - r) ** 2, 2)), neg(val)))
            # back: 출발점으로 다시 돌아오는 시각: ∫_0^t v = 0 → a t²/2 − a r t = 0 → t = 2r
            return N("속도가 v(t) = %s인 점 P가 t = 0일 때 출발한 점을 다시 지나는 시각은? (t &gt; 0)" % px(v, "t"), 2 * r, [r, 4 * r, r * r, 2 * r + 1], "∫<sub>0</sub><sup>t</sup> v(s) ds = %s = 0. <b>t = %d</b>" % (px([Fr(a, 2), -a * r, 0], "t"), 2 * r))
        v0 = R.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 60])
        g = 10
        k = R.choice(["top", "h"])
        tt = Fr(v0, g)
        if k == "top":
            h = Fr(v0 * v0, 2 * g)
            return N("지면에서 초속 %d m로 똑바로 위로 던진 공의 t초 후의 속도가 v(t) = %d − 10t (m/s)일 때, 공이 최고 높이에 도달할 때의 높이는?" % (v0, v0), h, [v0 * tt, h * 2, tt, h + 5], "v(t) = 0인 t = %s. ∫<sub>0</sub><sup>%s</sup> (%d − 10t) dt = <b>%s m</b>" % (neg(tt), neg(tt), v0, neg(h)), f=lambda x: "%s m" % neg(x))
        t = R.randint(1, int(tt))
        h = v0 * t - 5 * t * t
        return N("지면에서 똑바로 위로 던진 공의 t초 후의 속도가 v(t) = %d − 10t (m/s)일 때, %d초 후의 높이는?" % (v0, t), h, [v0 * t, v0 - 10 * t, h + 5 * t * t if h + 5 * t * t != v0 * t else h + 5, h * 2], "∫<sub>0</sub><sup>%d</sup> (%d − 10t) dt = <b>%s m</b>" % (t, v0, neg(h)), f=lambda x: "%s m" % neg(x))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    U = {}
    U["lim"] = ("limits-of-functions", 1, "[12미적Ⅰ-01-01] [12미적Ⅰ-01-02]", "함수의 극한의 뜻을 알고, 이를 설명할 수 있다. 함수의 극한에 대한 성질을 이해하고, 함수의 극한값을 구할 수 있다.",
                "함수의 극한", "함수의 극한",
                "고등학교 미적분Ⅰ 함수의 극한 문제: 다항함수의 극한, 0/0 꼴의 인수분해와 유리화, ∞/∞ 꼴, 좌극한과 우극한, 극한값이 주어질 때 상수 구하기까지 100문제와 정답·해설.",
                "0/0 꼴은 약분하거나 유리화", "∞/∞ 꼴은 분모의 최고차항으로 나누어요.",
                ["x가 a에 한없이 가까워질 때 f(x)가 L에 가까워지면 lim<sub>x→a</sub> f(x) = L이라고 해요.",
                 "다항함수는 x = a를 대입해요. 0/0 꼴은 인수분해해서 약분하거나 근호가 있으면 유리화해요.",
                 "∞/∞ 꼴은 분모의 최고차항으로 분모·분자를 나누어요. 차수가 같으면 최고차항 계수의 비예요.",
                 "좌극한과 우극한이 같을 때만 극한값이 존재해요. 분모 → 0이고 극한값이 있으면 분자 → 0이에요."],
                [("lim<sub>x→2</sub> (x² − 4)/(x − 2)", ["(x + 2)(x − 2)/(x − 2)"], "4"), ("lim<sub>x→∞</sub> (3x² + 1)/(x² − 5)", ["최고차항 계수 3 ÷ 1"], "3")],
                [("0/0 꼴을 0이라고 답한다", "약분이나 유리화를 먼저 해요."), ("∞/∞에서 상수항의 비를 쓴다", "최고차항 계수의 비예요."), ("|x|/x의 극한이 x → 0에서 1이라고 한다", "좌극한 −1, 우극한 1로 극한이 없어요.")],
                [("극한값과 함숫값은 같나요?", "같지 않을 수도 있어요. 함숫값이 없어도 극한값은 있을 수 있어요."), ("∞는 수인가요?", "한없이 커지는 상태를 나타내는 기호예요.")],
                [("다항함수의 극한", [(l_main(("sub",)), 20)]), ("0/0 꼴", [(l_main(("fact", "root")), 20)]), ("∞/∞ 꼴", [(l_main(("inf",)), 20)]),
                 ("좌극한과 우극한", [(l_main(("side",)), 20)]), ("미정계수", [(l_main(("const",)), 14), (l_main(("fact",)), 6)])], 83301)
    U["cont"] = ("continuity", 2, "[12미적Ⅰ-01-03] [12미적Ⅰ-01-04]", "함수의 연속을 극한으로 탐구하고 이해한다. 연속함수의 성질을 이해하고, 이를 활용하여 문제를 해결할 수 있다.",
                 "함수의 연속과 사잇값 정리", "함수의 연속",
                 "고등학교 미적분Ⅰ 함수의 연속 문제: 연속의 뜻, 연속이 되도록 상수 정하기, 구간별로 정의된 함수의 연속, 유리함수의 불연속점, 최대·최소 정리와 사잇값 정리까지 100문제와 정답·해설.",
                 "lim f(x) = f(a)이면 x = a에서 연속", "f(a)f(b)가 음수이면 (a, b)에 실근이 있어요.",
                 ["함수 f(x)가 x = a에서 연속이려면 f(a)가 정의되고, 극한값이 존재하며, lim<sub>x→a</sub> f(x) = f(a)여야 해요.",
                  "다항함수는 실수 전체에서, 유리함수는 분모가 0이 아닌 곳에서 연속이에요.",
                  "<b>최대·최소 정리</b>: 닫힌구간에서 연속인 함수는 최댓값과 최솟값을 가져요.",
                  "<b>사잇값 정리</b>: f가 [a, b]에서 연속이고 f(a)f(b) &lt; 0이면 f(c) = 0인 c가 (a, b)에 있어요."],
                 [("f(x) = (x² − 1)/(x − 1) (x ≠ 1), k (x = 1)", ["lim = 2"], "k = 2"), ("f(x) = x³ − x − 1, f(1) = −1, f(2) = 5", ["부호가 다름"], "(1, 2)에 실근")],
                 [("극한값만 있으면 연속이라고 한다", "함숫값과 같아야 해요."), ("구간별 함수에서 한쪽 식만 본다", "경계에서 좌극한, 우극한, 함숫값을 모두 맞춰요."), ("f(a)f(b) &gt; 0이면 실근이 없다고 한다", "알 수 없을 뿐, 실근이 있을 수도 있어요.")],
                 [("불연속인 그래프는?", "끊어지거나 구멍이 있거나 뛰어오르는 그래프예요."), ("사잇값 정리로 근의 정확한 값을 알 수 있나요?", "존재만 알려 줘요. 값은 다른 방법으로 구해요.")],
                 [("연속이 되도록 하는 상수", [(c_main(("k",)), 20)]), ("구간별로 정의된 함수", [(c_main(("piece",)), 20)]), ("불연속점", [(c_main(("rat",)), 20)]),
                  ("사잇값 정리", [(c_main(("ivt",)), 20)]), ("연속함수의 성질", [(c_main(("concept",)), 9), (c_main(("k", "piece")), 11)])], 83302)
    U["deriv"] = ("derivatives", 3, "[12미적Ⅰ-02-01] [12미적Ⅰ-02-02]", "미분계수를 이해하고, 이를 구할 수 있다. 함수의 미분가능성과 연속성의 관계를 설명하고, 이를 활용할 수 있다.",
                  "평균변화율과 미분계수", "미분계수",
                  "고등학교 미적분Ⅰ 미분계수 문제: 평균변화율, 미분계수의 정의 lim (f(a + h) − f(a))/h, 변형된 극한식, 미분가능성과 연속성의 관계, 평균변화율과 미분계수가 같아지는 점까지 100문제와 정답·해설.",
                  "f′(a)는 x = a에서의 접선의 기울기", "미분가능하면 연속, 연속이라고 미분가능한 것은 아니에요.",
                  ["x가 a에서 b까지 변할 때의 평균변화율은 (f(b) − f(a)) ÷ (b − a)이고, 두 점을 잇는 직선의 기울기예요.",
                   "미분계수 f′(a) = lim<sub>h→0</sub> (f(a + h) − f(a)) ÷ h는 x = a에서의 접선의 기울기예요.",
                   "lim<sub>h→0</sub> (f(a + kh) − f(a)) ÷ h = k f′(a)처럼 분모를 맞추어 계산해요.",
                   "x = a에서 미분가능하면 연속이에요. |x|는 x = 0에서 연속이지만 미분가능하지 않아요."],
                  [("f(x) = x², x: 1 → 3의 평균변화율", ["(9 − 1) ÷ 2"], "4"), ("f(x) = x², lim (f(1 + 2h) − f(1))/h", ["2f′(1) = 2 × 2"], "4")],
                  [("평균변화율에서 b − a로 나누지 않는다", "함숫값의 차를 x의 차로 나눠요."), ("f(a + 2h) − f(a)의 극한을 f′(a)로 쓴다", "2를 곱해야 해요."), ("연속이면 미분가능하다고 한다", "뾰족한 점은 미분가능하지 않아요.")],
                  [("미분계수와 도함수의 차이는?", "미분계수는 한 점의 값, 도함수는 각 x에 미분계수를 대응시킨 함수예요."), ("h가 음수여도 되나요?", "h → 0이면 양쪽 모두에서 다가가요.")],
                  [("평균변화율", [(d_main(("avg",)), 20)]), ("미분계수의 정의", [(d_main(("def",)), 20)]), ("변형된 극한식", [(d_main(("shift",)), 20)]),
                   ("미분가능성과 연속성", [(d_main(("diffc",)), 8), (d_main(("concept",)), 12)]), ("섞어서 연습", [(d_main(("avg", "def", "shift")), 20)])], 83303)
    U["rules"] = ("rules-of-differentiation", 4, "[12미적Ⅰ-02-03] [12미적Ⅰ-02-04]", "함수 y = xⁿ (n은 양의 정수)의 도함수를 구할 수 있다. 함수의 실수배, 합, 차, 곱의 미분법을 알고, 다항함수의 도함수를 구할 수 있다.",
                  "도함수와 미분법", "미분법",
                  "고등학교 미적분Ⅰ 미분법 문제: (xⁿ)′ = nxⁿ⁻¹, 다항함수의 도함수, 미분계수의 값, 곱의 미분법, (ax + b)ⁿ의 미분, 조건으로 계수 구하기까지 100문제와 정답·해설.",
                  "(xⁿ)′ = nxⁿ⁻¹", "{f(x)g(x)}′ = f′(x)g(x) + f(x)g′(x)",
                  ["(xⁿ)′ = nxⁿ⁻¹, (상수)′ = 0이에요.",
                   "{kf(x)}′ = kf′(x), {f(x) ± g(x)}′ = f′(x) ± g′(x)예요.",
                   "곱의 미분법: {f(x)g(x)}′ = f′(x)g(x) + f(x)g′(x)",
                   "f′(a)는 도함수를 구한 뒤 x = a를 대입해요."],
                  [("f(x) = 2x³ − 5x + 1", ["6x² − 5"], "f′(x) = 6x² − 5"), ("f(x) = (x + 1)(x² − 3)", ["1 × (x² − 3) + (x + 1) × 2x"], "f′(x) = 3x² + 2x − 3")],
                  [("(x³)′ = 3x³", "지수를 하나 줄여서 3x²이에요."), ("곱의 미분을 f′(x)g′(x)로 한다", "f′g + fg′예요."), ("상수항을 그대로 남긴다", "상수의 미분은 0이에요.")],
                  [("미분은 어디에 쓰이나요?", "접선, 증가·감소, 극값, 속도처럼 순간의 변화율을 다룰 때 써요."), ("(ax + b)ⁿ은?", "n(ax + b)ⁿ⁻¹ × a예요(곱의 미분법을 거듭 써서 확인).")],
                  [("다항함수의 도함수", [(r_main(("poly",)), 20)]), ("미분계수의 값", [(r_main(("val",)), 20)]), ("곱의 미분법", [(r_main(("prod",)), 20)]),
                   ("(ax + b)ⁿ의 미분", [(r_main(("pow",)), 20)]), ("계수 구하기", [(r_main(("find",)), 20)])], 83304)
    U["tan"] = ("tangent-lines-and-mean-value-theorem", 5, "[12미적Ⅰ-02-05] [12미적Ⅰ-02-06]", "미분계수와 접선의 기울기의 관계를 이해하고, 접선의 방정식을 구할 수 있다. 함수에 대한 평균값 정리를 설명하고, 이를 활용할 수 있다.",
                "접선의 방정식과 평균값 정리", "접선과 평균값 정리",
                "고등학교 미적분Ⅰ 접선의 방정식과 평균값 정리 문제: 곡선 위의 점에서의 접선, 기울기가 주어진 접선, 곡선 밖의 점에서 그은 접선, 롤의 정리, 평균값 정리를 만족하는 c까지 100문제와 정답·해설.",
                "y − f(a) = f′(a)(x − a)", "평균값 정리: (f(b) − f(a)) ÷ (b − a) = f′(c)",
                ["곡선 y = f(x) 위의 점 (a, f(a))에서의 접선은 y − f(a) = f′(a)(x − a)예요.",
                 "기울기가 m인 접선은 f′(x) = m인 접점을 먼저 찾아요.",
                 "<b>롤의 정리</b>: f(a) = f(b)이면 f′(c) = 0인 c가 (a, b)에 있어요.",
                 "<b>평균값 정리</b>: (f(b) − f(a)) ÷ (b − a) = f′(c)인 c가 (a, b)에 있어요."],
                [("y = x² − 3x 위의 (1, −2)", ["f′(1) = −1"], "y = −x − 1"), ("f(x) = x², [1, 5]", ["(25 − 1) ÷ 4 = 2c"], "c = 3")],
                [("접선의 기울기에 f(a)를 쓴다", "기울기는 f′(a)예요."), ("곡선 밖의 점을 접점으로 생각한다", "접점 (t, f(t))를 놓고 그 점을 지나도록 해요."), ("평균값 정리에서 c를 구간 밖에서 고른다", "c는 열린구간 (a, b) 안에 있어요.")],
                [("평균값 정리의 그림 의미는?", "두 끝점을 잇는 직선과 평행한 접선이 있다는 뜻이에요."), ("법선이란?", "접점에서 접선에 수직인 직선이에요. 기울기는 −1/f′(a)예요.")],
                [("곡선 위의 점에서의 접선", [(t_main(("at",)), 20)]), ("기울기가 주어진 접선", [(t_main(("slope",)), 20)]), ("곡선 밖의 점에서 그은 접선", [(t_main(("outside",)), 4), (t_main(("at", "slope")), 16)]),
                 ("롤의 정리", [(t_main(("rolle",)), 20)]), ("평균값 정리", [(t_main(("mvt",)), 20)])], 83305)
    U["inc"] = ("increasing-decreasing-and-extrema", 6, "[12미적Ⅰ-02-07]", "함수의 증가와 감소, 극대와 극소를 판정하고 설명할 수 있다.",
                "함수의 증가·감소와 극대·극소", "증가·감소와 극값",
                "고등학교 미적분Ⅰ 함수의 증가와 감소, 극대와 극소 문제: f′(x)의 부호로 증가·감소 구간 찾기, 삼차함수의 극댓값과 극솟값, 실수 전체에서 증가할 조건, 극값으로 상수 구하기까지 100문제와 정답·해설.",
                "f′(x)의 부호로 증가·감소를 판단", "f′의 부호가 +에서 −로 바뀌면 극대, −에서 +이면 극소",
                ["어떤 구간에서 f′(x) &gt; 0이면 f(x)는 그 구간에서 증가하고, f′(x) &lt; 0이면 감소해요.",
                 "f′(a) = 0이고 x = a의 좌우에서 f′(x)의 부호가 양 → 음이면 극대, 음 → 양이면 극소예요.",
                 "극댓값·극솟값은 그 점의 함숫값(y좌표)이에요.",
                 "삼차함수가 실수 전체에서 증가하려면 f′(x) ≥ 0, 즉 f′(x) = 0의 판별식이 0 이하여야 해요."],
                [("f(x) = x³ − 3x", ["f′(x) = 3(x + 1)(x − 1)"], "극댓값 f(−1) = 2, 극솟값 f(1) = −2"), ("x³ + kx² + 3x가 증가", ["3x² + 2kx + 3 ≥ 0", "k² − 9 ≤ 0"], "−3 ≤ k ≤ 3")],
                [("극값으로 x좌표를 답한다", "극값은 함숫값이에요."), ("f′(a) = 0이면 항상 극값이라고 한다", "부호가 바뀌어야 극값이에요."), ("증가 조건에서 D &lt; 0만 쓴다", "D ≤ 0이에요(중근이어도 증가).")],
                [("증감표는 왜 그리나요?", "f′의 부호와 f의 변화를 한눈에 정리할 수 있어요."), ("극대와 최대는 같나요?", "극대는 근처에서 가장 큰 값, 최대는 전체에서 가장 큰 값이에요.")],
                [("증가하는 구간", [(i_main(("inc",)), 20)]), ("감소하는 구간", [(i_main(("dec",)), 20)]), ("극댓값과 극솟값", [(i_main(("max", "min")), 20)]),
                 ("증가할 조건", [(i_main(("always",)), 4), (i_main(("inc", "dec", "max", "min")), 16)]), ("극값과 상수", [(i_main(("ext_k",)), 20)])], 83306)
    U["graph"] = ("graphs-and-maximum-minimum", 7, "[12미적Ⅰ-02-08]", "함수의 그래프의 개형을 그릴 수 있다.",
                  "함수의 그래프와 최댓값·최솟값", "그래프와 최대·최소",
                  "고등학교 미적분Ⅰ 함수의 그래프 문제: 삼차함수 그래프의 개형, 그래프 읽기, 닫힌구간에서의 최댓값과 최솟값, 극값을 이용한 실근의 개수까지 100문제와 정답·해설.",
                  "최댓값·최솟값은 극값과 양 끝값을 비교", "극값의 위치와 x축과의 관계로 개형을 그려요.",
                  ["f′(x) = 0인 x와 증감표로 극값을 구하고 그래프의 개형을 그려요.",
                   "닫힌구간에서의 최댓값·최솟값은 극값과 구간의 양 끝값 중 가장 큰 값·작은 값이에요.",
                   "f(x) = k의 실근의 개수는 y = f(x)와 직선 y = k의 교점의 개수예요.",
                   "삼차함수에서 (극댓값) × (극솟값) &lt; 0이면 x축과 세 점에서 만나요."],
                  [("[−2, 3]에서 f(x) = x³ − 3x", ["극값 f(−1) = 2, f(1) = −2", "끝값 f(−2) = −2, f(3) = 18"], "최댓값 18, 최솟값 −2"), ("x³ − 3x = 1의 실근", ["극댓값 2 &gt; 1 &gt; 극솟값 −2"], "3개")],
                  [("구간의 양 끝값을 비교하지 않는다", "끝값이 더 클 수도 있어요."), ("극댓값을 최댓값으로 답한다", "닫힌구간에서는 끝값과 비교해요."), ("직선이 극값을 지날 때 교점을 3개로 센다", "접하면 2개예요.")],
                  [("사차함수의 개형은?", "f′(x) = 0의 근에 따라 W자 또는 U자 모양이에요."), ("그래프를 그리는 순서는?", "f′(x) = 0 → 증감표 → 극값 → 절편 순서로 해요.")],
                  [("닫힌구간에서의 최대·최소", [(g_main(("closed",)), 20)]), ("그래프 읽기", [(g_main(("pic",)), 20)]), ("실근의 개수", [(g_main(("roots",)), 20)]),
                   ("그래프의 개형", [(g_main(("shape",)), 8), (g_main(("closed", "roots")), 12)]), ("섞어서 연습", [(g_main(("closed", "roots", "pic")), 20)])], 83307)
    U["app"] = ("equations-inequalities-and-velocity", 8, "[12미적Ⅰ-02-09] [12미적Ⅰ-02-10]", "방정식과 부등식에 대한 문제를 해결할 수 있다. 미분을 속도와 가속도에 대한 문제에 활용하고, 그 유용성을 인식할 수 있다.",
                "방정식·부등식과 속도·가속도", "미분의 활용",
                "고등학교 미적분Ⅰ 미분의 활용 문제: 극값을 이용한 방정식의 실근의 개수, 세 실근을 가질 조건, 부등식이 항상 성립할 조건, 수직선 위를 움직이는 점의 속도와 가속도, 운동 방향이 바뀌는 시각까지 100문제와 정답·해설.",
                "v = x′(t), a = v′(t)", "운동 방향은 속도의 부호가 바뀔 때 바뀌어요.",
                ["f(x) = k의 실근의 개수는 y = f(x)와 y = k의 교점의 개수로 판단해요.",
                 "어떤 범위에서 f(x) ≥ 0이 성립하려면 그 범위에서의 최솟값이 0 이상이어야 해요.",
                 "위치 x(t)에서 속도 v(t) = x′(t), 가속도 a(t) = v′(t)예요.",
                 "v(t) = 0이고 그 전후로 부호가 바뀌면 운동 방향이 바뀌어요."],
                [("x(t) = t³ − 6t² + 9t", ["v(t) = 3t² − 12t + 9 = 3(t − 1)(t − 3)"], "t = 1, 3에서 방향이 바뀜"), ("x³ − 3x + k = 0이 세 실근", ["−2 &lt; −k &lt; 2"], "−2 &lt; k &lt; 2")],
                [("속도와 가속도를 바꾼다", "위치를 한 번 미분하면 속도, 두 번 미분하면 가속도예요."), ("v(t) = 0이면 항상 방향이 바뀐다고 한다", "부호가 바뀌어야 해요."), ("부등식에서 극솟값만 본다", "주어진 범위의 최솟값을 봐요(끝값 포함).")],
                [("속력과 속도의 차이는?", "속력은 속도의 크기 |v(t)|예요."), ("가속도가 0이면?", "그 순간 속도가 변하지 않아요.")],
                [("실근의 개수", [(a_main(("count",)), 20)]), ("세 실근을 가질 조건", [(a_main(("kroot",)), 20)]), ("실근과 부등식", [(a_main(("ineq",)), 6), (a_main(("count", "kroot")), 14)]),
                 ("속도와 가속도", [(a_main(("vel", "acc")), 20)]), ("운동 방향", [(a_main(("stop",)), 14), (a_main(("vel",)), 6)])], 83308)
    U["indef"] = ("indefinite-integrals", 9, "[12미적Ⅰ-03-01] [12미적Ⅰ-03-02]", "부정적분의 뜻을 알고, 이를 설명할 수 있다. 함수의 실수배, 합, 차의 부정적분을 알고, 다항함수의 부정적분을 구할 수 있다.",
                  "부정적분", "부정적분",
                  "고등학교 미적분Ⅰ 부정적분 문제: 부정적분의 뜻과 적분상수, ∫xⁿ dx, 다항함수의 부정적분, 조건을 만족하는 함수 구하기, 미분과 적분의 관계까지 100문제와 정답·해설.",
                  "∫xⁿ dx = xⁿ⁺¹/(n + 1) + C", "미분해서 f(x)가 되는 함수를 찾고 C를 붙여요.",
                  ["F′(x) = f(x)일 때 F(x)를 f(x)의 부정적분이라 하고 ∫f(x) dx = F(x) + C로 써요(C는 적분상수).",
                   "∫xⁿ dx = xⁿ⁺¹/(n + 1) + C (n은 0 이상의 정수), ∫k dx = kx + C",
                   "∫{f(x) ± g(x)} dx = ∫f(x) dx ± ∫g(x) dx, ∫kf(x) dx = k∫f(x) dx",
                   "한 점의 값이 주어지면 C를 정할 수 있어요."],
                  [("∫(3x² − 4x + 1) dx", ["x³ − 2x² + x"], "x³ − 2x² + x + C"), ("f′(x) = 2x, f(1) = 3", ["f(x) = x² + C", "1 + C = 3"], "f(x) = x² + 2")],
                  [("적분상수 C를 빠뜨린다", "부정적분에는 항상 C를 붙여요."), ("∫x³ dx = 3x² + C", "지수를 하나 올리고 그 수로 나눠요: x⁴/4 + C"), ("곱의 적분을 적분의 곱으로 한다", "먼저 전개해서 적분해요.")],
                  [("부정적분은 왜 하나가 아닌가요?", "상수는 미분하면 0이 되므로 C만큼 차이 나는 함수가 모두 답이에요."), ("미분과 적분의 관계는?", "d/dx ∫f(x) dx = f(x)예요.")],
                  [("부정적분의 계산", [(n_main(("basic",)), 20)]), ("부정적분의 뜻", [(n_main(("concept",)), 7), (n_main(("deriv",)), 13)]), ("함수 구하기", [(n_main(("find",)), 20)]),
                   ("F(a)의 값", [(n_main(("val",)), 20)]), ("섞어서 연습", [(n_main(("basic", "find", "val")), 20)])], 83309)
    U["defi"] = ("definite-integrals", 10, "[12미적Ⅰ-03-03] [12미적Ⅰ-03-04]", "정적분의 개념을 탐구하고, 그 성질을 이해한다. 부정적분과 정적분의 관계를 이해하고, 다항함수의 정적분을 구할 수 있다.",
                 "정적분의 계산과 성질", "정적분",
                 "고등학교 미적분Ⅰ 정적분 문제: 다항함수의 정적분, 구간을 나누고 합치기, 위끝과 아래끝 바꾸기, 우함수·기함수의 정적분, 절댓값이 있는 정적분, d/dx ∫ₐˣ f(t)dt = f(x)까지 100문제와 정답·해설.",
                 "∫ₐᵇ f(x) dx = F(b) − F(a)", "d/dx ∫ₐˣ f(t) dt = f(x)",
                 ["F′(x) = f(x)이면 ∫<sub>a</sub><sup>b</sup> f(x) dx = F(b) − F(a)예요.",
                  "∫<sub>a</sub><sup>a</sup> f(x) dx = 0, ∫<sub>b</sub><sup>a</sup> f(x) dx = −∫<sub>a</sub><sup>b</sup> f(x) dx, ∫<sub>a</sub><sup>c</sup> = ∫<sub>a</sub><sup>b</sup> + ∫<sub>b</sub><sup>c</sup>",
                  "∫<sub>−a</sub><sup>a</sup>에서 홀수 차수 항은 0, 짝수 차수 항은 2∫<sub>0</sub><sup>a</sup>이에요.",
                  "d/dx ∫<sub>a</sub><sup>x</sup> f(t) dt = f(x)예요."],
                 [("∫<sub>1</sub><sup>3</sup> (2x + 1) dx", ["[x² + x]<sub>1</sub><sup>3</sup> = 12 − 2"], "10"), ("∫<sub>−1</sub><sup>1</sup> (x³ + 3x²) dx", ["홀수 차수 0", "2∫<sub>0</sub><sup>1</sup> 3x² dx"], "2")],
                 [("F(a) − F(b)로 계산한다", "위끝에서 아래끝을 빼요."), ("|x − a|를 그대로 적분한다", "x = a에서 나누어 절댓값을 없애요."), ("대칭 구간에서 모든 항을 2배 한다", "홀수 차수 항은 0이에요.")],
                 [("정적분과 넓이는 같나요?", "f(x) ≥ 0일 때만 넓이와 같아요."), ("적분상수는?", "정적분에서는 서로 지워져서 필요 없어요.")],
                 [("정적분의 계산", [(df_main(("basic",)), 20)]), ("구간 나누기와 바꾸기", [(df_main(("split", "rev")), 20)]), ("대칭 구간", [(df_main(("sym",)), 20)]),
                  ("절댓값이 있는 정적분", [(df_main(("abs",)), 14), (df_main(("basic",)), 6)]), ("미분과 정적분", [(df_main(("ftc",)), 20)])], 83310)
    U["area"] = ("area-between-curves", 11, "[12미적Ⅰ-03-05]", "곡선으로 둘러싸인 도형의 넓이에 대한 문제를 해결할 수 있다.",
                 "곡선으로 둘러싸인 도형의 넓이", "넓이",
                 "고등학교 미적분Ⅰ 넓이 문제: 곡선과 x축으로 둘러싸인 넓이, x축 아래 부분이 있는 넓이, 곡선과 직선·두 곡선 사이의 넓이, 삼차함수와 x축 사이의 넓이까지 100문제와 정답·해설.",
                 "넓이 = ∫|f(x) − g(x)| dx", "x축 아래 부분은 부호를 바꾸어 더해요.",
                 ["곡선 y = f(x)와 x축, x = a, x = b로 둘러싸인 넓이는 ∫<sub>a</sub><sup>b</sup> |f(x)| dx예요.",
                  "f(x)가 음수인 구간은 −f(x)를 적분해서 더해요.",
                  "두 곡선 사이의 넓이는 교점을 구한 뒤 ∫(위 − 아래) dx예요.",
                  "이차함수 y = a(x − α)(x − β)와 x축 사이의 넓이는 |a|(β − α)³ ÷ 6이에요."],
                 [("y = x² − 2x와 x축", ["교점 0, 2", "−∫<sub>0</sub><sup>2</sup> (x² − 2x) dx"], "4/3"), ("y = x²과 y = x + 2", ["교점 −1, 2", "∫(x + 2 − x²) dx"], "9/2")],
                 [("x축 아래 부분을 음수 그대로 더한다", "넓이는 양수이므로 부호를 바꿔 더해요."), ("위아래를 바꾸어 적분한다", "(위 − 아래)로 적분해요."), ("교점을 구하지 않고 범위를 정한다", "교점이 적분 구간이에요.")],
                 [("|a|(β − α)³/6은 언제 쓰나요?", "이차함수와 직선(또는 x축)으로 둘러싸인 넓이에 쓸 수 있어요."), ("y축 방향으로 적분할 수도 있나요?", "고등학교 미적분Ⅰ에서는 주로 x에 대하여 적분해요.")],
                 [("곡선과 x축", [(ar_main(("axis",)), 20)]), ("x축 아래 부분이 있는 넓이", [(ar_main(("below",)), 20)]), ("곡선과 직선", [(ar_main(("pl",)), 20)]),
                  ("두 곡선 사이와 삼차함수", [(ar_main(("pp", "cubic")), 12), (ar_main(("axis",)), 8)]), ("그래프 보고 넓이 구하기", [(ar_main(("pic",)), 14), (ar_main(("pl",)), 6)])], 83311)
    U["vel"] = ("velocity-and-distance", 12, "[12미적Ⅰ-03-06]", "적분을 속도와 거리에 대한 문제에 활용하고, 그 유용성을 인식할 수 있다.",
                "속도와 거리", "속도와 거리",
                "고등학교 미적분Ⅰ 속도와 거리 문제: 속도를 적분해 위치 구하기, 위치의 변화량과 움직인 거리의 차이, 출발점으로 다시 돌아오는 시각, 위로 던진 공의 높이까지 100문제와 정답·해설.",
                "위치의 변화량 = ∫v(t) dt", "움직인 거리 = ∫|v(t)| dt",
                ["시각 t에서의 속도가 v(t)이고 t = 0에서의 위치가 x₀이면, 시각 t에서의 위치는 x₀ + ∫<sub>0</sub><sup>t</sup> v(s) ds예요.",
                 "t = a에서 t = b까지 위치의 변화량은 ∫<sub>a</sub><sup>b</sup> v(t) dt예요.",
                 "움직인 거리는 ∫<sub>a</sub><sup>b</sup> |v(t)| dt로, 방향이 바뀌는 시각에서 나누어 계산해요.",
                 "위로 던진 물체는 v(t) = 0일 때 가장 높이 올라가요."],
                 [("v(t) = 2t − 4, 0 ≤ t ≤ 3", ["변화량 ∫(2t − 4) dt = −3", "거리 4 + 1"], "변화량 −3, 거리 5"), ("v(t) = 20 − 10t", ["v = 0인 t = 2", "∫<sub>0</sub><sup>2</sup> (20 − 10t) dt"], "최고 높이 20 m")],
                [("움직인 거리를 ∫v(t) dt로 구한다", "방향이 바뀌면 |v(t)|를 적분해야 해요."), ("위치를 구할 때 처음 위치를 더하지 않는다", "x₀ + ∫v(t) dt예요."), ("최고 높이에서 가속도가 0이라고 한다", "속도가 0이에요.")],
                [("위치의 변화량이 0이면?", "처음 위치로 돌아왔다는 뜻이에요."), ("속력의 적분은?", "|v(t)|의 적분이 움직인 거리예요.")],
                [("위치", [(v_main(("pos",)), 20)]), ("위치의 변화량", [(v_main(("change",)), 20)]), ("움직인 거리", [(v_main(("dist",)), 20)]),
                 ("다시 돌아오는 시각", [(v_main(("back",)), 12), (v_main(("change", "dist")), 8)]), ("위로 던진 물체", [(v_main(("up",)), 20)])], 83312)
    t = U[which]
    slug, sort, code, std, title, short, meta, kb, ks, think, ex_, mist, faq, spec, seed = t
    return unit(G, slug, sort, code, std, title, short, meta, kb, ks, think, ex_, mist, faq, spec, seed)
