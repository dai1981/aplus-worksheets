# -*- coding: utf-8 -*-
"""
대한민국 고등학교 공통수학2（2022 개정）の 15 単元。build(key)：
  dist 두 점 사이의 거리와 내분점 / line 직선의 방정식 / pdist 점과 직선 사이의 거리 / circ 원의 방정식 / cl 원과 직선
  move 평행이동과 대칭이동 / sets 집합 / setop 집합의 연산 / prop 명제와 조건 / nec 충분조건과 필요조건 / absin 절대부등식
  func 함수 / comp 합성함수와 역함수 / rat 유리함수 / irr 무리함수
誤答は「내분점에서 m, n을 바꾼다」「기울기의 곱이 1이면 수직이라고 생각한다」「거리 공식의 절댓값·분모를 빠뜨린다」
「원의 반지름을 r²으로 답한다」「x축 대칭에서 x좌표의 부호를 바꾼다」「부분집합의 개수를 2n으로 센다」「역과 대우를 바꾼다」
「충분조건과 필요조건을 거꾸로 쓴다」「산술평균·기하평균에서 등호 조건을 빠뜨린다」「(f∘g)(x)를 g(f(x))로 계산한다」
「점근선에서 부호를 바꾸지 않는다」「무리함수의 정의역에서 부등호 방향을 거꾸로 쓴다」から作る。
"""
import math
import random
import re
from fractions import Fraction as Fr
from kr_m2a import poly2
from kr_hs import josa, M, N, neg, par, px, padd, pmul, peval, surd, sq_split, W, graph, num, fr, unit, BLUE, RED, GREEN

R = random.Random(83101)
G = "common-math-2"


def nz(lo=-6, hi=6):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def pt(x, y):
    return "(%s, %s)" % (neg(x), neg(y))


def gen(a, b, c):
    """ax + by + c = 0"""
    return poly2({(1, 0): a, (0, 1): b, (0, 0): c}, ("x", "y")) + " = 0"


def yeq(m, b):
    return "y = " + px([m, b])


def sqv(v):
    """√v (v는 유리수) → 간단히"""
    v = Fr(v)
    if v.denominator == 1:
        return surd(1, v.numerator)
    # √(p/q) = √(pq)/q
    return fr(surd(1, v.numerator * v.denominator), v.denominator) if surd(1, v.numerator * v.denominator) != "1" else fr(1, v.denominator)


def sq_or(v):
    """정수의 제곱근을 √ 꼴로"""
    return surd(1, v)


# ------------------------------------------------------------------ 두 점 사이의 거리와 내분점
def d_main(kinds=("dist", "div", "mid", "cent", "line1", "find")):
    def mk():
        how = R.choice(kinds)
        x1, y1, x2, y2 = (R.randint(-6, 6) for _ in range(4))
        if (x1, y1) == (x2, y2):
            return None
        if how == "dist":
            d2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
            ok = sq_or(d2)
            w = [sq_or(abs(x2 - x1) + abs(y2 - y1)) if abs(x2 - x1) + abs(y2 - y1) != d2 else None, neg(d2), sq_or((x2 + x1) ** 2 + (y2 + y1) ** 2) if (x2 + x1) ** 2 + (y2 + y1) ** 2 else "0",
                 neg(abs(x2 - x1) + abs(y2 - y1)), sq_or(d2 + 1)]
            return M("두 점 A%s, B%s 사이의 거리는?" % (pt(x1, y1), pt(x2, y2)), ok, w, "AB = √(%s² + %s²) = %s<b>%s</b>" % (par(x2 - x1), par(y2 - y1), ("√%d = " % d2) if ok != "√%d" % d2 else "", ok))
        if how in ("div", "mid"):
            m, n = (1, 1) if how == "mid" else R.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])
            px_, py_ = Fr(m * x2 + n * x1, m + n), Fr(m * y2 + n * y1, m + n)
            if how == "div" and (px_.denominator != 1 or py_.denominator != 1):
                return None
            ok = pt(px_, py_)
            sw = pt(Fr(n * x2 + m * x1, m + n), Fr(n * y2 + m * y1, m + n))
            w = [sw, pt(Fr(x1 + x2, 2), Fr(y1 + y2, 2)) if how == "div" else pt(x2 - x1, y2 - y1), pt(Fr(m * x2 - n * x1, m + n), Fr(m * y2 - n * y1, m + n)), pt(x1 + x2, y1 + y2), pt(py_, px_)]
            if how == "mid":
                return M("두 점 A%s, B%s를 이은 선분 AB의 중점의 좌표는?" % (pt(x1, y1), pt(x2, y2)), ok, w, "((x₁ + x₂)/2, (y₁ + y₂)/2) = <b>%s</b>" % ok)
            return M("두 점 A%s, B%s에 대하여 선분 AB를 %d : %d로 내분하는 점의 좌표는?" % (pt(x1, y1), pt(x2, y2), m, n), ok, w,
                     "((%d × %s + %d × %s)/%d, (%d × %s + %d × %s)/%d) = <b>%s</b>" % (m, par(x2), n, par(x1), m + n, m, par(y2), n, par(y1), m + n, ok))
        if how == "cent":
            x3, y3 = R.randint(-6, 6), R.randint(-6, 6)
            sx, sy = x1 + x2 + x3, y1 + y2 + y3
            if sx % 3 or sy % 3:
                return None
            ok = pt(sx // 3, sy // 3)
            return M("세 점 A%s, B%s, C%s를 꼭짓점으로 하는 삼각형 ABC의 무게중심의 좌표는?" % (pt(x1, y1), pt(x2, y2), pt(x3, y3)), ok, [pt(sx, sy), pt(Fr(sx, 2), Fr(sy, 2)), pt(sy // 3, sx // 3), pt(sx // 3 + 1, sy // 3)],
                     "세 꼭짓점의 좌표의 평균이에요. <b>%s</b>" % ok)
        if how == "line1":
            a, b = sorted(R.sample(range(-9, 10), 2))
            m, n = R.choice([(1, 2), (2, 1), (1, 3), (3, 1), (3, 2), (2, 3), (1, 4)])
            v = Fr(m * b + n * a, m + n)
            return N("수직선 위의 두 점 A(%s), B(%s)에 대하여 선분 AB를 %d : %d로 내분하는 점의 좌표는?" % (neg(a), neg(b), m, n), v, [Fr(n * b + m * a, m + n), Fr(a + b, 2), Fr(m * b - n * a, m + n), v + 1],
                     "(%d × %s + %d × %s) ÷ %d = <b>%s</b>" % (m, par(b), n, par(a), m + n, neg(v)))
        k = nz(-6, 6)
        # A(x1, y1), B(x2, k) 거리 d가 주어질 때 k?  → 같은 x좌표에서 거리
        dx = R.choice([3, 4, 5, 6, 8, 12])
        dy = {3: 4, 4: 3, 5: 12, 6: 8, 8: 6, 12: 5}[dx]
        d = int(math.hypot(dx, dy))
        y2 = y1 + dy
        return N("두 점 A%s, B(%s, a) 사이의 거리가 %d이고 a &gt; %s일 때, a의 값은?" % (pt(x1, y1), neg(x1 + dx), d, neg(y1)), y2, [y1 - dy, dy, y1 + d, y2 + 1],
                 "%d² + (a − %s)² = %d² → a − %s = ±%d. a &gt; %s이므로 <b>a = %s</b>" % (dx, par(y1), d, par(y1), dy, neg(y1), neg(y2)))
    return mk


# ------------------------------------------------------------------ 직선의 방정식
def l_main(kinds=("pt_slope", "two", "par", "perp", "kpar", "kperp", "int")):
    def mk():
        how = R.choice(kinds)
        x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
        m = R.choice([Fr(v) for v in (-3, -2, -1, 1, 2, 3)] + [Fr(1, 2), Fr(-1, 2), Fr(2, 3), Fr(-3, 2)])
        b = y1 - m * x1
        if how == "pt_slope":
            ok = yeq(m, b)
            return M("점 %s를 지나고 기울기가 %s인 직선의 방정식은?" % (pt(x1, y1), neg(m)), ok, [yeq(m, y1 + m * x1), yeq(m, y1), yeq(-m, y1 + m * x1), yeq(1 / m, b)],
                     "y − %s = %s(x − %s). <b>%s</b>" % (par(y1), neg(m), par(x1), ok))
        if how == "two":
            x2 = x1 + R.choice([1, 2, 3, -1, -2])
            y2 = y1 + m * (x2 - x1)
            if y2.denominator != 1:
                return None
            ok = yeq(m, b)
            return M("두 점 %s, %s를 지나는 직선의 방정식은?" % (pt(x1, y1), pt(x2, y2)), ok, [yeq(1 / m, y1 - x1 / m), yeq(-m, y1 + m * x1), yeq(m, -b) if b else yeq(m, 1), yeq(m, y2)],
                     "기울기 = (%s − %s) ÷ (%s − %s) = %s. <b>%s</b>" % (neg(y2), par(y1), neg(x2), par(x1), neg(m), ok))
        if how in ("par", "perp"):
            m0 = m if how == "par" else -1 / m
            c0 = R.randint(-6, 6)
            ok = yeq(m0, y1 - m0 * x1)
            w = [yeq(-1 / m0, y1 + x1 / m0), yeq(m0, c0) if c0 != y1 - m0 * x1 else None, yeq(-m0, y1 + m0 * x1), yeq(1 / m0, y1 - x1 / m0)]
            return M("점 %s를 지나고 직선 %s에 %s 직선의 방정식은?" % (pt(x1, y1), yeq(m, c0), "평행한" if how == "par" else "수직인"), ok, w,
                     "%s 직선의 기울기는 %s예요. <b>%s</b>" % ("평행한" if how == "par" else "수직인", neg(m0), ok))
        a, bb = nz(-5, 5), nz(-5, 5)
        if how == "kpar":
            # ax + by + 1 = 0  ∥  kx + 2y − 3 = 0 → a/k = b/2 → k = 2a/b
            c2 = R.choice([2, 3, 4, -2])
            k = Fr(a * c2, bb)
            if k.denominator != 1 or k == 0:
                return None
            return N("두 직선 %s, %s가 평행할 때, 상수 k의 값은?" % (gen(a, bb, 1), "kx " + px([c2, 0], "y").replace("y", "y", 1).join(["", ""]) if False else "kx %s %sy − 3 = 0" % ("+" if c2 > 0 else "−", abs(c2) if abs(c2) != 1 else "")), k,
                     [-k, Fr(bb * c2, a) if Fr(bb * c2, a) != k else k + 1, Fr(-bb * c2, a), k + 2], "기울기가 같아야 해요. %s/k = %s/%s → <b>k = %s</b>" % (neg(a), neg(bb), neg(c2), neg(k)))
        if how == "kperp":
            c2 = R.choice([1, 2, 3, -1, -2])
            # a·k + b·c2 = 0
            k = Fr(-bb * c2, a)
            if k.denominator != 1:
                return None
            return N("두 직선 %s, %s가 수직일 때, 상수 k의 값은?" % (gen(a, bb, 1), "kx %s %sy + 2 = 0" % ("+" if c2 > 0 else "−", abs(c2) if abs(c2) != 1 else "")), k,
                     [-k, Fr(a * c2, bb) if Fr(a * c2, bb) != k else k + 1, Fr(bb * c2, a) + 1 if Fr(bb * c2, a) + 1 != k else k - 1, k + 2], "aa′ + bb′ = 0 → %s × k + %s × %s = 0. <b>k = %s</b>" % (neg(a), par(bb), par(c2), neg(k)))
        # 교점
        m1, m2 = R.sample([-3, -2, -1, 1, 2, 3], 2)
        X, Y = R.randint(-4, 4), R.randint(-4, 4)
        ok = pt(X, Y)
        return M("두 직선 %s와 %s의 교점을 지나고 기울기가 %s인 직선의 y절편은?" % (yeq(m1, Y - m1 * X), yeq(m2, Y - m2 * X), neg(m)), neg(Y - m * X), [neg(Y + m * X), neg(X - m * Y), neg(Y), neg(Y - m * X + 1)],
                 "교점은 %s이므로 y = %s(x − %s) + %s. y절편 <b>%s</b>" % (ok, neg(m), par(X), par(Y), neg(Y - m * X)))
    return mk


# ------------------------------------------------------------------ 점과 직선 사이의 거리
TRIP = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (1, 1, None), (1, 2, None), (2, 1, None), (1, 3, None)]


def p_main(kinds=("pd", "origin", "par", "area", "k")):
    def mk():
        how = R.choice(kinds)
        a, b, h = R.choice(TRIP)
        a, b = a * R.choice([1, -1]), b * R.choice([1, -1])
        c = R.randint(-15, 15)
        hh = a * a + b * b
        den = h if h else None
        def dist(v):
            v = abs(v)
            return Fr(v, h) if h else (fr(surd(v, hh), hh) if v % hh else surd(Fr(v, hh), hh)) if v else 0
        def show(v):
            return neg(v) if isinstance(v, Fr) or isinstance(v, int) else v
        if how in ("pd", "origin"):
            x0, y0 = (0, 0) if how == "origin" else (R.randint(-5, 5), R.randint(-5, 5))
            v = a * x0 + b * y0 + c
            if v == 0:
                return None
            ok = show(dist(v))
            w = [neg(abs(v)), show(dist(v + 2 * c)) if v + 2 * c else "0", neg(Fr(abs(v), hh)), show(dist(abs(a * x0 + b * y0))) if a * x0 + b * y0 else neg(Fr(abs(v), h or 2))]
            if not h:
                w.append(sq_or(abs(v)))
            return M("%s 직선 %s 사이의 거리는?" % ("원점과" if how == "origin" else "점 %s와" % pt(x0, y0), gen(a, b, c)), ok, w,
                     "|%s| ÷ √%d = <b>%s</b>" % (neg(v), hh, ok))
        if how == "par":
            c2 = c + R.choice([-1, 1]) * R.randint(2, 20)
            ok = show(dist(c - c2))
            return M("평행한 두 직선 %s, %s 사이의 거리는?" % (gen(a, b, c), gen(a, b, c2)), ok, [neg(abs(c - c2)), show(dist(abs(c) + abs(c2))) if abs(c) + abs(c2) != abs(c - c2) else neg(Fr(abs(c - c2), 2)), neg(Fr(abs(c - c2), hh)), show(dist(c - c2 + 1))],
                     "한 직선 위의 점에서 다른 직선까지의 거리: |%s − (%s)| ÷ √%d = <b>%s</b>" % (neg(c), neg(c2), hh, ok))
        if how == "area":
            # 원점, 직선 위 두 점 — 넓이 = (밑변 × 높이)/2
            if not h:
                return None
            X1 = R.randint(-6, 6)
            # 직선 위 정수점 두 개
            pts_ = [(x, Fr(-(a * x + c), b)) for x in range(-12, 13)]
            pts_ = [(x, y) for x, y in pts_ if y.denominator == 1]
            if len(pts_) < 2 or c == 0:
                return None
            P, Q = R.sample(pts_[:8], 2)
            base = math.hypot(P[0] - Q[0], P[1] - Q[1])
            area = Fr(abs(P[0] * Q[1] - P[1] * Q[0]), 2)
            return N("원점 O와 두 점 A%s, B%s를 꼭짓점으로 하는 삼각형 OAB의 넓이는? (두 점 A, B는 직선 %s 위에 있어요)" % (pt(*P), pt(*Q), gen(a, b, c)), area, [area * 2, Fr(abs(c), h), area + 1, Fr(abs(c), 2)],
                     "AB = %s, 원점과 직선 사이의 거리 = %s. 넓이 = <b>%s</b>" % (neg(Fr(base).limit_denominator(100)) if base == int(base) else "√%d" % round(base * base), neg(Fr(abs(c), h)), neg(area)))
        # k : 점 (x0,y0)와 직선 a x + b y + k = 0 사이 거리가 d
        if not h:
            return None
        x0, y0 = R.randint(-4, 4), R.randint(-4, 4)
        d = R.randint(1, 4)
        s0 = a * x0 + b * y0
        k1, k2 = d * h - s0, -d * h - s0
        ok = "k = %s 또는 k = %s" % (neg(min(k1, k2)), neg(max(k1, k2)))
        return M("점 %s와 직선 %s + k = 0 사이의 거리가 %d일 때, 상수 k의 값은?" % (pt(x0, y0), gen(a, b, 0)[:-4], d), ok,
                 ["k = %s" % neg(max(k1, k2)), "k = %s 또는 k = %s" % (neg(d - s0), neg(-d - s0)), "k = %s 또는 k = %s" % (neg(-max(k1, k2)), neg(-min(k1, k2)))],
                 "|%s + k| ÷ %d = %d → %s + k = ±%d. <b>%s</b>" % (neg(s0), h, d, neg(s0), d * h, ok))
    return mk


# ------------------------------------------------------------------ 원의 방정식
def cq(a, b, r2):
    X = "x²" if a == 0 else "(%s)²" % px([1, -a])
    Y = "y²" if b == 0 else "(%s)²" % px([1, -b], "y")
    return "%s + %s = %s" % (X, Y, neg(r2))


def c_main(kinds=("read", "write", "gen", "diam", "tan", "k")):
    def mk():
        how = R.choice(kinds)
        a, b = R.randint(-5, 5), R.randint(-5, 5)
        r = R.randint(1, 6)
        if how == "read":
            k = R.choice(["c", "r"])
            if k == "c":
                ok = pt(a, b)
                return M("원 <b>%s</b>의 중심의 좌표는?" % cq(a, b, r * r), ok, [pt(-a, -b), pt(b, a) if a != b else pt(a, -b), pt(a, -b) if b else pt(a + 1, b), pt(-a, b) if a else pt(a, b + 1)], "(x − a)² + (y − b)² = r²의 중심은 (a, b)예요. <b>%s</b>" % ok)
            return N("원 <b>%s</b>의 반지름의 길이는?" % cq(a, b, r * r), r, [r * r, 2 * r, r + 1, Fr(r * r, 2)], "r² = %d이므로 <b>%d</b>" % (r * r, r))
        if how == "write":
            ok = cq(a, b, r * r)
            return M("중심이 %s이고 반지름의 길이가 %d인 원의 방정식은?" % (pt(a, b), r), ok, [cq(-a, -b, r * r), cq(a, b, r), cq(a, b, 2 * r), cq(b, a, r * r) if a != b else cq(a, -b, r * r)], "(x − a)² + (y − b)² = r². <b>%s</b>" % ok)
        if how == "gen":
            # x² + y² + Ax + By + C = 0
            A, B, C = -2 * a, -2 * b, a * a + b * b - r * r
            eq = poly2({(2, 0): 1, (0, 2): 1, (1, 0): A, (0, 1): B, (0, 0): C}, ("x", "y")) + " = 0"
            k = R.choice(["c", "r"])
            if k == "c":
                ok = pt(a, b)
                return M("원 <b>%s</b>의 중심의 좌표는?" % eq, ok, [pt(-a, -b), pt(A, B), pt(b, a) if a != b else pt(a, -b), pt(-A, -B)], "완전제곱식으로 고치면 %s. <b>%s</b>" % (cq(a, b, r * r), ok))
            return N("원 <b>%s</b>의 반지름의 길이는?" % eq, r, [r * r, abs(C) if abs(C) != r else r + 2, r + 1, 2 * r], "%s으로 고치면 r = <b>%d</b>" % (cq(a, b, r * r), r))
        if how == "diam":
            x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
            x2, y2 = x1 + 2 * R.randint(-3, 3), y1 + 2 * R.randint(-3, 3)
            if (x1, y1) == (x2, y2):
                return None
            cx_, cy_ = (x1 + x2) // 2, (y1 + y2) // 2
            r2 = (x1 - cx_) ** 2 + (y1 - cy_) ** 2
            ok = cq(cx_, cy_, r2)
            return M("두 점 A%s, B%s를 지름의 양 끝으로 하는 원의 방정식은?" % (pt(x1, y1), pt(x2, y2)), ok, [cq(cx_, cy_, 4 * r2), cq(-cx_, -cy_, r2), cq(x1, y1, r2), cq(cx_, cy_, 2 * r2)],
                     "중심은 AB의 중점 %s, 반지름은 AB의 절반 √%d. <b>%s</b>" % (pt(cx_, cy_), r2, ok))
        if how == "tan":
            k = R.choice(["x", "y"])
            if (a == 0 and k == "y") or (b == 0 and k == "x"):
                return None
            rr = abs(b) if k == "x" else abs(a)
            ok = cq(a, b, rr * rr)
            return M("중심이 %s이고 %s축에 접하는 원의 방정식은?" % (pt(a, b), k), ok, [cq(a, b, (abs(a) if k == "x" else abs(b)) ** 2) if abs(a) != abs(b) else cq(a, b, 2 * rr * rr), cq(a, b, rr), cq(-a, -b, rr * rr), cq(a, b, 2 * rr * rr)],
                     "%s축에 접하면 반지름 = |중심의 %s좌표| = %d. <b>%s</b>" % (k, "y" if k == "x" else "x", rr, ok))
        # 원이 되기 위한 k 범위: x² + y² + Ax + By + k = 0 → A²/4 + B²/4 − k > 0
        A, B = 2 * nz(-4, 4), 2 * nz(-4, 4)
        lim = (A * A + B * B) // 4
        eq = poly2({(2, 0): 1, (0, 2): 1, (1, 0): A, (0, 1): B}, ("x", "y")) + " + k = 0"
        ok = "k &lt; %d" % lim
        return M("방정식 <b>%s</b>이 원을 나타낼 때, 상수 k의 값의 범위는?" % eq, ok, ["k &gt; %d" % lim, "k ≤ %d" % lim, "k &lt; %d" % (A * A + B * B), "k &gt; −%d" % lim],
                 "(x %s %d)² + (y %s %d)² = %d − k에서 %d − k &gt; 0. <b>%s</b>" % ("+" if A > 0 else "−", abs(A) // 2, "+" if B > 0 else "−", abs(B) // 2, lim, lim, ok))
    return mk


def circle_pic(a, b, r, lines=(), label="원과 직선"):
    fs = [(lambda x, a=a, b=b, r=r: b + math.sqrt(r * r - (x - a) ** 2), BLUE, ""), (lambda x, a=a, b=b, r=r: b - math.sqrt(r * r - (x - a) ** 2), BLUE, "")]
    for m_, c_ in lines:
        fs.append((lambda x, m_=m_, c_=c_: m_ * x + c_, RED, ""))
    return graph(fs, (-6, 6, 1), (-6, 6, 1), label=label)


# ------------------------------------------------------------------ 원과 직선
def cl_main(kinds=("pos", "count", "k", "tline", "chord", "tlen")):
    def mk():
        how = R.choice(kinds)
        if how in ("pos", "count"):
            r2 = R.choice([1, 2, 4, 5, 8, 9, 10, 13, 16, 18, 20, 25])
            m, c = nz(-3, 3), R.randint(-8, 8)
            # 원 x² + y² = r², 직선 y = mx + c: D/4 = m²c²... 판별: d = |c|/√(m²+1) vs r ⇔ c² vs r²(m²+1)
            L, Rr = c * c, r2 * (m * m + 1)
            rel = "서로 다른 두 점에서 만나요" if L < Rr else ("한 점에서 만나요(접해요)" if L == Rr else "만나지 않아요")
            pic = circle_pic(0, 0, math.sqrt(r2), [(m, c)], "원 x² + y² = %d와 직선" % r2) if how == "pos" and r2 <= 25 and R.random() < 0.5 else ""
            if how == "count":
                n = 2 if L < Rr else (1 if L == Rr else 0)
                return N("원 x² + y² = %d와 직선 %s의 교점의 개수는?" % (r2, yeq(m, c)), n, [x for x in (0, 1, 2, 3) if x != n], "원의 중심과 직선 사이의 거리 d와 반지름을 비교해요. <b>%d개</b>" % n, f=lambda v: "%s개" % neg(v))
            return M("원 x² + y² = %d와 직선 %s의 위치 관계는?%s" % (r2, yeq(m, c), pic), rel, [x for x in ("서로 다른 두 점에서 만나요", "한 점에서 만나요(접해요)", "만나지 않아요", "원의 중심을 지나요") if x != rel],
                     "d = |%s| ÷ √%d, d² = %s와 r² = %d를 비교해요. <b>%s</b>" % (neg(c), m * m + 1, neg(Fr(c * c, m * m + 1)), r2, rel))
        if how == "k":
            m = nz(-3, 3)
            r2 = R.choice([1, 2, 4, 5, 9, 10, 20])
            kind = R.choice(["meet", "tan", "none"])
            lim = r2 * (m * m + 1)
            rt = sq_or(lim)
            ok = {"meet": "−%s &lt; k &lt; %s", "tan": "k = ±%s", "none": "k &lt; −%s 또는 k &gt; %s"}[kind] % ((rt, rt) if kind != "tan" else (rt,))
            alt = ["−%s &lt; k &lt; %s" % (rt, rt), "k = ±%s" % rt, "k &lt; −%s 또는 k &gt; %s" % (rt, rt), "−%s ≤ k ≤ %s" % (rt, rt), "k = ±%s" % sq_or(r2)]
            nm = {"meet": "서로 다른 두 점에서 만날", "tan": "접할", "none": "만나지 않을"}[kind]
            return M("원 x² + y² = %d와 직선 %s + k가 %s 때, 상수 k의 값의 범위(또는 값)는?" % (r2, "y = " + px([m, 0]), nm), ok, [x for x in alt if x != ok],
                     "d = |k| ÷ √%d을 반지름 √%d와 비교해요. |k| %s %s. <b>%s</b>" % (m * m + 1, r2, {"meet": "&lt;", "tan": "=", "none": "&gt;"}[kind], rt, ok))
        if how == "tline":
            x1, y1 = R.choice([(3, 4), (4, 3), (-3, 4), (3, -4), (1, 2), (2, 1), (-1, 2), (1, 1), (2, -1), (5, 12), (-4, 3), (1, -3), (-2, 1), (-1, -1), (2, 3), (-3, -1), (1, 4), (-2, -3), (3, 1), (-4, -3)])
            r2 = x1 * x1 + y1 * y1
            ok = gen(x1, y1, 0)[:-4] + " = %d" % r2
            ok = poly2({(1, 0): x1, (0, 1): y1}, ("x", "y")) + " = %d" % r2
            w = [poly2({(1, 0): y1, (0, 1): x1}, ("x", "y")) + " = %d" % r2, poly2({(1, 0): x1, (0, 1): y1}, ("x", "y")) + " = %s" % sq_or(r2), poly2({(1, 0): x1, (0, 1): -y1}, ("x", "y")) + " = %d" % r2, poly2({(1, 0): x1, (0, 1): y1}, ("x", "y")) + " = 0"]
            return M("원 x² + y² = %d 위의 점 %s에서의 접선의 방정식은?" % (r2, pt(x1, y1)), ok, w, "x₁x + y₁y = r²에 대입해요. <b>%s</b>" % ok)
        if how == "chord":
            r = R.choice([5, 10, 13, 15, 17, 25])
            d = {5: [3, 4], 10: [6, 8], 13: [5, 12], 15: [9, 12], 17: [8, 15], 25: [7, 15, 20, 24]}[r]
            d = R.choice(d)
            half = math.isqrt(r * r - d * d)
            return N("반지름의 길이가 %d인 원의 중심에서 거리가 %d인 직선이 원과 만나서 생기는 현의 길이는?" % (r, d), 2 * half, [half, r - d, 2 * (r - d), 2 * r - d], "(현의 절반)² = %d² − %d² → 현의 절반은 %d. <b>%d</b>" % (r, d, half, 2 * half))
        # 접선의 길이: 원 밖의 점에서 그은 접선의 길이
        a, b = R.randint(-3, 3), R.randint(-3, 3)
        r = R.randint(1, 4)
        px0, py0 = a + R.choice([4, 5, 6, -4, -5]), b + R.choice([3, 4, -3, 2])
        d2 = (px0 - a) ** 2 + (py0 - b) ** 2
        t2 = d2 - r * r
        ok = sq_or(t2)
        return M("점 P%s에서 원 %s에 그은 접선의 길이는?" % (pt(px0, py0), cq(a, b, r * r)), ok, [sq_or(d2), sq_or(d2 + r * r), sq_or(t2 + 1), neg(t2)],
                 "(접선의 길이)² = (중심까지의 거리)² − r² = %d − %d. <b>%s</b>" % (d2, r * r, ok))
    return mk


# ------------------------------------------------------------------ 평행이동과 대칭이동
def mv_main(kinds=("ptmove", "linemove", "circmove", "ptref", "lineref", "circref", "find")):
    REF = [("x축", lambda x, y: (x, -y)), ("y축", lambda x, y: (-x, y)), ("원점", lambda x, y: (-x, -y)), ("직선 y = x", lambda x, y: (y, x))]

    def mk():
        how = R.choice(kinds)
        x, y = R.randint(-6, 6), R.randint(-6, 6)
        p, q = nz(-5, 5), nz(-5, 5)
        if how == "ptmove":
            ok = pt(x + p, y + q)
            return M("점 %s를 x축의 방향으로 %s만큼, y축의 방향으로 %s만큼 평행이동한 점의 좌표는?" % (pt(x, y), neg(p), neg(q)), ok, [pt(x - p, y - q), pt(x + q, y + p), pt(x + p, y - q), pt(p, q)],
                     "(x + %s, y + %s). <b>%s</b>" % (par(p), par(q), ok))
        if how == "linemove":
            m, c = nz(-3, 3), R.randint(-5, 5)
            # y − q = m(x − p) + c
            ok = yeq(m, c + q - m * p)
            return M("직선 %s를 x축의 방향으로 %s만큼, y축의 방향으로 %s만큼 평행이동한 직선의 방정식은?" % (yeq(m, c), neg(p), neg(q)), ok, [yeq(m, c - q + m * p), yeq(m, c + q + m * p), yeq(m, c + p + q), yeq(m, c + q)],
                     "x 대신 x − %s, y 대신 y − %s를 넣어요. <b>%s</b>" % (par(p), par(q), ok))
        if how == "circmove":
            a, b, r = R.randint(-4, 4), R.randint(-4, 4), R.randint(1, 5)
            ok = cq(a + p, b + q, r * r)
            return M("원 %s를 x축의 방향으로 %s만큼, y축의 방향으로 %s만큼 평행이동한 원의 방정식은?" % (cq(a, b, r * r), neg(p), neg(q)), ok, [cq(a - p, b - q, r * r), cq(a + q, b + p, r * r) if p != q else cq(a + p, b - q, r * r), cq(a + p, b + q, (r + 1) ** 2), cq(p, q, r * r) if (p, q) != (a + p, b + q) else cq(-p, -q, r * r)],
                     "중심 %s가 %s로 옮겨지고 반지름은 그대로예요. <b>%s</b>" % (pt(a, b), pt(a + p, b + q), ok))
        nm, f = R.choice(REF)
        if how == "ptref":
            if x == 0 or y == 0 or x == y:
                return None
            ok = pt(*f(x, y))
            w = [pt(*g(x, y)) for n2, g in REF if n2 != nm]
            return M("점 %s를 %s에 대하여 대칭이동한 점의 좌표는?" % (pt(x, y), nm), ok, w, "%s에 대한 대칭이동. <b>%s</b>" % (nm, ok))
        if how == "lineref":
            a, b, c = nz(-4, 4), nz(-4, 4), R.randint(-6, 6)
            if abs(a) == abs(b):
                return None
            T = {"x축": (a, -b, c), "y축": (-a, b, c), "원점": (-a, -b, c), "직선 y = x": (b, a, c)}
            nrm = lambda t: (t if t[0] > 0 or (t[0] == 0 and t[1] > 0) else tuple(-v for v in t))
            ok = gen(*nrm(T[nm]))
            w = [gen(*nrm(v)) for k2, v in T.items() if k2 != nm]
            return M("직선 %s를 %s에 대하여 대칭이동한 직선의 방정식은?" % (gen(*nrm((a, b, c))), nm), ok, w,
                     "%s 대신 넣어요. <b>%s</b>" % ({"x축": "y에 −y를", "y축": "x에 −x를", "원점": "x에 −x, y에 −y를", "직선 y = x": "x와 y를 서로 바꾸어"}[nm], ok))
        if how == "circref":
            a, b, r = nz(-4, 4), nz(-4, 4), R.randint(1, 5)
            if abs(a) == abs(b):
                return None
            ok = cq(*f(a, b), r * r)
            w = [cq(*g(a, b), r * r) for n2, g in REF if n2 != nm]
            return M("원 %s를 %s에 대하여 대칭이동한 원의 방정식은?" % (cq(a, b, r * r), nm), ok, w, "중심 %s만 대칭이동하면 %s. <b>%s</b>" % (pt(a, b), pt(*f(a, b)), ok))
        # find: 점 (x,y)를 평행이동 (p,q)하여 (x2,y2)가 되었을 때, 직선 y = mx + c를 같은 평행이동
        x2, y2 = x + p, y + q
        a2 = R.randint(-5, 5)
        return N("평행이동 (x, y) → (x + a, y + b)에 의하여 점 %s가 점 %s로 옮겨질 때, a + b의 값은?" % (pt(x, y), pt(x2, y2)), p + q, [-(p + q), p - q, x2 + y2, x + y], "a = %s, b = %s. <b>%s</b>" % (neg(p), neg(q), neg(p + q)))
    return mk


# ------------------------------------------------------------------ 집합
def S(xs):
    xs = sorted(set(xs))
    return "{%s}" % ", ".join(neg(x) for x in xs) if xs else "∅"


def st_main(kinds=("elem", "n", "sub", "count", "rel", "builder")):
    def mk():
        how = R.choice(kinds)
        if how == "elem":
            k = R.choice(["div", "mul", "odd", "sq"])
            n = R.randint(6, 30)
            if k == "div":
                A = [d for d in range(1, n + 1) if n % d == 0]
                txt = "%d의 양의 약수" % n
            elif k == "mul":
                m = R.randint(2, 7)
                A = list(range(m, n + 1, m))
                txt = "%d 이하인 %d의 양의 배수" % (n, m)
            elif k == "odd":
                A = list(range(1, min(n, 15) + 1, 2))
                txt = "%d 이하인 홀수인 자연수" % min(n, 15)
            else:
                A = [i * i for i in range(1, 8) if i * i <= n * 3]
                txt = "%d 이하인 제곱수인 자연수" % (n * 3)
            if len(A) < 2:
                return None
            ok = S(A)
            w = [S(A[:-1]), S(A + [A[-1] + (A[-1] - A[-2])]), S([a for a in range(1, max(A) + 1) if a not in A][:len(A)]) if len(A) < max(A) else S(A[1:]), S(A[1:])]
            return M("%s의 집합을 원소나열법으로 나타내면?" % txt, ok, w, "조건을 만족하는 원소를 빠짐없이 써요. <b>%s</b>" % ok)
        if how in ("n", "sub"):
            A = sorted(R.sample(range(1, 20), R.randint(3, 7)))
            k = "n" if how == "n" else R.choice(["sub", "proper"])
            nA = len(A)
            if k == "n":
                return N("집합 A = %s에 대하여 n(A)의 값은?" % S(A), nA, [nA + 1, max(A), sum(A) % 10 + 1 if sum(A) % 10 + 1 != nA else nA - 1, 2 ** nA], "원소의 개수예요. <b>%d</b>" % nA)
            if k == "sub":
                return N("집합 A = %s의 부분집합의 개수는?" % S(A), 2 ** nA, [2 * nA, 2 ** nA - 1, nA ** 2, 2 ** (nA - 1)], "2<sup>%d</sup> = <b>%d</b>" % (nA, 2 ** nA), f=lambda v: "%s개" % neg(v))
            return N("집합 A = %s의 진부분집합의 개수는?" % S(A), 2 ** nA - 1, [2 ** nA, 2 * nA - 1, 2 ** nA - 2, nA ** 2], "자기 자신을 제외해요. 2<sup>%d</sup> − 1 = <b>%d</b>" % (nA, 2 ** nA - 1), f=lambda v: "%s개" % neg(v))
        if how == "count":
            n = R.randint(4, 8)
            A = list(range(1, n + 1))
            inc = R.randint(1, 2)
            exc = R.randint(0, 2)
            if inc + exc >= n:
                return None
            ins, outs = A[:inc], A[inc:inc + exc]
            v = 2 ** (n - inc - exc)
            cond = "%s%s" % ("%s를 반드시 원소로 갖고" % ", ".join(map(str, ins)), (" %s를 원소로 갖지 않는" % ", ".join(map(str, outs))) if outs else "")
            cond = cond.rstrip("고") + ("는" if not outs else "") if not outs else cond
            return N("집합 A = %s의 부분집합 중 %s 부분집합의 개수는?" % (S(A), cond), v, [2 ** n - v if 2 ** n - v != v else v * 2, 2 ** (n - inc), 2 ** n, v * 2 if v * 2 != 2 ** (n - inc) else v + 1],
                     "정해진 원소를 빼고 남은 %d개의 원소로 만든 부분집합의 개수예요. 2<sup>%d</sup> = <b>%d</b>" % (n - inc - exc, n - inc - exc, v), f=lambda t: "%s개" % neg(t))
        if how == "rel":
            A = sorted(R.sample(range(1, 10), R.randint(2, 4)))
            B = sorted(set(A) | set(R.sample(range(1, 10), 2)))
            x = R.choice([v for v in range(1, 10) if v not in B])
            items = [("%d ∈ A" % A[0], True), ("%d ∈ B" % x, False), ("A ⊂ B", True), ("B ⊂ A", B == A), ("∅ ⊂ A", True), ("%d ∉ A" % A[-1], False), ("{%d} ∈ A" % A[0], False), ("{%d} ⊂ A" % A[0], True)]
            R.shuffle(items)
            want = R.choice([True, False])
            right = [t for t, v in items if v == want]
            wrong = [t for t, v in items if v != want]
            if not right or len(wrong) < 3:
                return None
            return M("A = %s, B = %s일 때, %s 것은?" % (S(A), S(B), "옳은" if want else "옳지 않은"), right[0], wrong, "원소에는 ∈, 집합 사이에는 ⊂를 써요. <b>%s</b>" % right[0])
        if how == "builder":
            n = R.randint(2, 5)
            m = R.randint(3, 6)
            A = [n * k for k in range(1, m + 1)]
            ok = "{x | x = %dk, k는 %d 이하의 자연수}" % (n, m)
            return M("집합 %s를 조건제시법으로 나타낸 것은?" % S(A), ok, ["{x | x = %dk, k는 %d 이하의 자연수}" % (n, m + 1), "{x | x = k + %d, k는 %d 이하의 자연수}" % (n, m), "{x | x는 %d 이하의 자연수}" % (n * m), "{x | x = %dk, k는 %d 이하의 자연수}" % (n + 1, m)],
                     "원소가 %d의 배수 %d개예요. <b>%s</b>" % (n, m, ok))
        # cond: A ⊂ B 가 되도록 a
        a = R.randint(1, 6)
        B = sorted({a + 2, 2 * a + 1, a + 5, 3})
        A = [a + 2, 3]
        if len(set(A)) < 2:
            return None
        return N("두 집합 A = {3, a + 2}, B = %s에 대하여 A ⊂ B일 때, B의 원소 중 가장 큰 수는? (a는 자연수 %d)" % (S(B), a), max(B), [min(B), a + 2, 3, max(B) + 1], "B의 가장 큰 원소는 <b>%d</b>" % max(B)) if False else None
    return mk


# ------------------------------------------------------------------ 집합의 연산
def so_main(kinds=("cup", "cap", "comp", "diff", "ncup", "word", "dem")):
    def mk():
        how = R.choice(kinds)
        U = list(range(1, R.randint(8, 12) + 1))
        A = set(R.sample(U, R.randint(3, 6)))
        B = set(R.sample(U, R.randint(3, 6)))
        if A == B or not (A & B) or A <= B or B <= A:
            return None
        ops = {"cup": (A | B, "A ∪ B"), "cap": (A & B, "A ∩ B"), "diff": (A - B, "A − B"), "comp": (set(U) - A, "A<sup>C</sup>"), "dem": (set(U) - (A | B), "(A ∪ B)<sup>C</sup>")}
        if how in ops:
            res, nm = ops[how]
            if not res:
                return None
            ok = S(res)
            w = [S(v) for k2, (v, _) in ops.items() if k2 != how and v != res and v]
            w += [S(B - A), S(set(U) - B)]
            pre = "전체집합 U = %s의 두 부분집합 " % S(U) if how in ("comp", "dem") else ""
            return M("%sA = %s, B = %s에 대하여 <b>%s</b>는?" % (pre, S(A), S(B), nm), ok, w,
                     {"cup": "A 또는 B에 속하는 원소", "cap": "A와 B에 모두 속하는 원소", "diff": "A에는 속하고 B에는 속하지 않는 원소", "comp": "U에서 A의 원소를 뺀 것", "dem": "드모르간의 법칙: A<sup>C</sup> ∩ B<sup>C</sup>와 같아요"}[how] + ". <b>%s</b>" % ok)
        if how == "ncup":
            a, b = R.randint(8, 30), R.randint(8, 30)
            c = R.randint(2, min(a, b) - 1)
            k = R.choice(["cup", "cap"])
            if k == "cup":
                return N("n(A) = %d, n(B) = %d, n(A ∩ B) = %d일 때, n(A ∪ B)의 값은?" % (a, b, c), a + b - c, [a + b, a + b + c, a + b - 2 * c, a - c], "n(A) + n(B) − n(A ∩ B) = <b>%d</b>" % (a + b - c))
            u = a + b - c
            return N("n(A) = %d, n(B) = %d, n(A ∪ B) = %d일 때, n(A ∩ B)의 값은?" % (a, b, u), c, [a + b + u, u - a, u - b if u - b != c else c + 1, a + b - u + 1], "n(A) + n(B) − n(A ∪ B) = <b>%d</b>" % c)
        # word
        T = R.randint(30, 40)
        a, b = R.randint(12, 25), R.randint(12, 25)
        both = R.randint(max(1, a + b - T + 1), min(a, b) - 2)
        k = R.choice(["none", "only"])
        if k == "none":
            v = T - (a + b - both)
            return N("학생 %d명 중 수학을 좋아하는 학생이 %d명, 과학을 좋아하는 학생이 %d명, 둘 다 좋아하는 학생이 %d명이에요. 둘 다 좋아하지 않는 학생은 몇 명일까요?" % (T, a, b, both), v,
                     [T - a - b if T - a - b > 0 else v + both, T - both, a + b - both, v + 1], "%d − (%d + %d − %d) = <b>%d명</b>" % (T, a, b, both, v), f=lambda t: "%s명" % neg(t))
        v = a - both
        return N("학생 %d명 중 수학을 좋아하는 학생이 %d명, 과학을 좋아하는 학생이 %d명, 둘 다 좋아하는 학생이 %d명이에요. 수학만 좋아하는 학생은 몇 명일까요?" % (T, a, b, both), v,
                 [a, b - both, a + b - both, v + 1], "n(A − B) = n(A) − n(A ∩ B) = <b>%d명</b>" % v, f=lambda t: "%s명" % neg(t))
    return mk


# ------------------------------------------------------------------ 명제와 조건
def pr_main(kinds=("truth", "neg", "quant", "conv", "tf")):
    NEG = [("x &gt; 3", "x ≤ 3"), ("x ≥ −2", "x &lt; −2"), ("x = 1", "x ≠ 1"), ("x는 짝수이다", "x는 홀수이다"), ("x &lt; 0 또는 x &gt; 5", "0 ≤ x ≤ 5"),
           ("−1 &lt; x ≤ 4", "x ≤ −1 또는 x &gt; 4"), ("x &gt; 0이고 y &gt; 0", "x ≤ 0 또는 y ≤ 0"), ("x = 0 또는 y = 0", "x ≠ 0이고 y ≠ 0"), ("x² = 4", "x² ≠ 4"), ("a ≤ 2", "a &gt; 2"), ("x ≤ −1 또는 x ≥ 3", "−1 &lt; x &lt; 3"), ("x &lt; 7", "x ≥ 7"), ("x ≠ 5", "x = 5"), ("x는 3의 배수이다", "x는 3의 배수가 아니다"), ("2 ≤ x &lt; 6", "x &lt; 2 또는 x ≥ 6")]

    def mk():
        how = R.choice(kinds)
        if how == "truth":
            n = R.randint(8, 12)
            U = list(range(1, n + 1))
            k = R.choice(["prime", "div", "ineq", "sq"])
            if k == "prime":
                P = [x for x in U if x > 1 and all(x % d for d in range(2, x))]
                c = "x는 소수이다"
            elif k == "div":
                m = R.choice([12, 16, 18, 20, 24, 30, 36])
                P = [x for x in U if m % x == 0]
                c = "x는 %d의 약수이다" % m
            elif k == "ineq":
                a, b = sorted(R.sample(range(1, n + 1), 2))
                P = [x for x in U if a < x <= b]
                c = "%d &lt; x ≤ %d" % (a, b)
            else:
                a = R.randint(2, 5)
                P = [x for x in U if x * x - (a + 2 * a) * x + 2 * a * a <= 0]
                c = "%s ≤ 0" % px([1, -3 * a, 2 * a * a])
            if not P:
                return None
            ok = S(P)
            w = [S([x for x in U if x not in P]), S(P[:-1]) if len(P) > 1 else S(P + [P[0] + 1]), S(P + [P[-1] + 1]) if P[-1] + 1 <= n else S(P[1:]) if len(P) > 1 else "∅", S(P[1:]) if len(P) > 1 else "∅"]
            return M("전체집합 U = %s에서 조건 'p: %s'의 진리집합은?" % (S(U), c), ok, w, "U의 원소 중 조건을 참이 되게 하는 원소의 집합이에요. <b>%s</b>" % ok)
        if how == "neg":
            p, np_ = R.choice(NEG)
            ok = np_
            w = [p, np_.replace("또는", "이고") if "또는" in np_ else np_.replace("이고", "또는") if "이고" in np_ else None,
                 p.replace("&gt;", "&lt;").replace("≥", "≤") if ("&gt;" in p or "≥" in p) else None, p.replace("=", "≠").replace("≠ ", "≠ ", 1) + "" if "=" in p and "≠" not in np_[:0] and p != np_ else None,
                 "x ≥ 3" if p == "x &gt; 3" else "x &lt; 3", "x는 소수이다"]
            return M("조건 '%s'의 부정은?" % p, ok, [x for x in w if x and x != ok], "'또는'의 부정은 '이고', 부등호는 등호까지 생각해서 바꿔요. <b>%s</b>" % ok)
        if how == "quant":
            Q = [("모든 실수 x에 대하여 x² ≥ 0이다.", "참"), ("어떤 실수 x에 대하여 x² &lt; 0이다.", "거짓"), ("모든 실수 x에 대하여 x² &gt; 0이다.", "거짓"), ("어떤 자연수 x에 대하여 x + 1 = 3이다.", "참"),
                 ("모든 자연수 x에 대하여 2x ≥ x이다.", "참"), ("어떤 실수 x에 대하여 x² − 2x + 1 = 0이다.", "참"), ("모든 실수 x에 대하여 x² + 1 &gt; 0이다.", "참"), ("어떤 정수 x에 대하여 2x = 5이다.", "거짓"),
                 ("모든 소수는 홀수이다.", "거짓"), ("어떤 짝수는 소수이다.", "참"), ("모든 정사각형은 직사각형이다.", "참"), ("모든 마름모는 정사각형이다.", "거짓"), ("어떤 실수 x에 대하여 x² = −1이다.", "거짓"), ("모든 자연수 n에 대하여 n² ≥ n이다.", "참"), ("어떤 실수 x에 대하여 x² = x이다.", "참"), ("모든 실수 x에 대하여 |x| ≥ x이다.", "참"), ("모든 실수 x에 대하여 x² ≥ x이다.", "거짓"), ("어떤 자연수 n에 대하여 n + 5 = 2이다.", "거짓"), ("모든 직사각형은 평행사변형이다.", "참"), ("어떤 홀수는 3의 배수이다.", "참")]
            neg_ = [("모든 실수 x에 대하여 x² ≥ 0이다.", "어떤 실수 x에 대하여 x² &lt; 0이다."), ("어떤 실수 x에 대하여 x &gt; 2이다.", "모든 실수 x에 대하여 x ≤ 2이다."), ("모든 자연수 n은 홀수이다.", "어떤 자연수 n은 짝수이다."),
                    ("어떤 학생은 안경을 썼다.", "모든 학생은 안경을 쓰지 않았다."), ("모든 실수 x에 대하여 x + 1 &gt; x이다.", "어떤 실수 x에 대하여 x + 1 ≤ x이다."), ("어떤 정수 x에 대하여 x² = 2이다.", "모든 정수 x에 대하여 x² ≠ 2이다."), ("모든 실수 x에 대하여 x² + 1 &gt; 0이다.", "어떤 실수 x에 대하여 x² + 1 ≤ 0이다."), ("어떤 자연수 n에 대하여 n² = 5이다.", "모든 자연수 n에 대하여 n² ≠ 5이다."), ("모든 학생은 휴대 전화를 가지고 있다.", "어떤 학생은 휴대 전화를 가지고 있지 않다."), ("어떤 실수 x에 대하여 x ≤ 0이다.", "모든 실수 x에 대하여 x &gt; 0이다.")]
            if R.random() < 0.6:
                s_, v = R.choice(Q)
                return M("명제 '%s'의 참, 거짓을 판별하면?" % s_, v, ["참" if v == "거짓" else "거짓", "명제가 아니에요", "알 수 없어요"], "'모든'은 하나라도 반례가 있으면 거짓, '어떤'은 하나라도 있으면 참이에요. <b>%s</b>" % v)
            s_, n_ = R.choice(neg_)
            flip = lambda t: t.replace("모든", "@").replace("어떤", "모든").replace("@", "어떤")
            return M("명제 '%s'의 부정은?" % s_, n_, [flip(s_), s_.replace("이다.", "이 아니다.") if "이다." in s_ else flip(n_), flip(n_)], "'모든'은 '어떤'으로, '어떤'은 '모든'으로 바꾸고 결론을 부정해요. <b>%s</b>" % n_)
        PQ = [("x = 2", "x² = 4"), ("x &gt; 3", "x &gt; 1"), ("x가 4의 배수", "x가 2의 배수"), ("a = 0", "ab = 0"), ("x² = 9", "x = 3"), ("x &lt; 1", "x &lt; 5"), ("사각형이 정사각형", "사각형이 마름모"),
              ("x + y &gt; 2", "x &gt; 1 또는 y &gt; 1"), ("x = 1이고 y = 2", "x + y = 3"), ("n이 6의 약수", "n이 12의 약수"),
              ("x = −1", "x² = 1"), ("x &gt; 2", "x² &gt; 4"), ("x = 0", "x² = 0"), ("x² &lt; 1", "x &lt; 1"), ("x ≥ 3", "x ≥ 2")]
        NP = {"x = 2": "x ≠ 2", "x² = 4": "x² ≠ 4", "x &gt; 3": "x ≤ 3", "x &gt; 1": "x ≤ 1", "x가 4의 배수": "x가 4의 배수가 아님", "x가 2의 배수": "x가 2의 배수가 아님", "a = 0": "a ≠ 0", "ab = 0": "ab ≠ 0",
              "x² = 9": "x² ≠ 9", "x = 3": "x ≠ 3", "x &lt; 1": "x ≥ 1", "x &lt; 5": "x ≥ 5", "사각형이 정사각형": "사각형이 정사각형이 아님", "사각형이 마름모": "사각형이 마름모가 아님",
              "x + y &gt; 2": "x + y ≤ 2", "x &gt; 1 또는 y &gt; 1": "x ≤ 1이고 y ≤ 1", "x = 1이고 y = 2": "x ≠ 1 또는 y ≠ 2", "x + y = 3": "x + y ≠ 3", "n이 6의 약수": "n이 6의 약수가 아님", "n이 12의 약수": "n이 12의 약수가 아님",
              "x = −1": "x ≠ −1", "x² = 1": "x² ≠ 1", "x² &gt; 4": "x² ≤ 4", "x = 0": "x ≠ 0", "x² = 0": "x² ≠ 0", "x² &lt; 1": "x² ≥ 1", "x ≥ 3": "x &lt; 3", "x ≥ 2": "x &lt; 2", "x &gt; 2": "x ≤ 2"}
        p, q = R.choice(PQ)
        form = lambda a, b: "%s %s" % (a[:-2] + "아니면" if a.endswith(" 아님") else a + "이면", b[:-2] + "아니다" if b.endswith(" 아님") else b + "이다")
        if how == "conv":
            k = R.choice(["역", "대우"])
            ok = form(q, p) if k == "역" else form(NP[q], NP[p])
            w = [form(q, p), form(NP[p], NP[q]), form(NP[q], NP[p]), form(p, NP[q])]
            return M("명제 '%s'의 %s?" % (form(p, q), josa(k, "은/는")), ok, [x for x in w if x != ok],
                     "역은 가정과 결론을 바꾸고, 대우는 바꾼 뒤 둘 다 부정해요. <b>%s</b>" % ok)
        TRUE = {("x = 2", "x² = 4"): True, ("x &gt; 3", "x &gt; 1"): True, ("x가 4의 배수", "x가 2의 배수"): True, ("a = 0", "ab = 0"): True, ("x² = 9", "x = 3"): False, ("x &lt; 1", "x &lt; 5"): True,
                ("사각형이 정사각형", "사각형이 마름모"): True, ("x + y &gt; 2", "x &gt; 1 또는 y &gt; 1"): True, ("x = 1이고 y = 2", "x + y = 3"): True, ("n이 6의 약수", "n이 12의 약수"): True,
                ("x = −1", "x² = 1"): True, ("x &gt; 2", "x² &gt; 4"): True, ("x = 0", "x² = 0"): True, ("x² &lt; 1", "x &lt; 1"): True, ("x ≥ 3", "x ≥ 2"): True}
        t = TRUE[(p, q)]
        k = R.choice(["원래 명제", "대우", "역"])
        conv_true = {("x = 2", "x² = 4"): False, ("x &gt; 3", "x &gt; 1"): False, ("x가 4의 배수", "x가 2의 배수"): False, ("a = 0", "ab = 0"): False, ("x² = 9", "x = 3"): True, ("x &lt; 1", "x &lt; 5"): False,
                     ("사각형이 정사각형", "사각형이 마름모"): False, ("x + y &gt; 2", "x &gt; 1 또는 y &gt; 1"): False, ("x = 1이고 y = 2", "x + y = 3"): False, ("n이 6의 약수", "n이 12의 약수"): False,
                     ("x = −1", "x² = 1"): False, ("x &gt; 2", "x² &gt; 4"): False, ("x = 0", "x² = 0"): True, ("x² &lt; 1", "x &lt; 1"): False, ("x ≥ 3", "x ≥ 2"): False}
        v = t if k != "역" else conv_true[(p, q)]
        stmt = form(p, q) if k == "원래 명제" else (form(NP[q], NP[p]) if k == "대우" else form(q, p))
        ans = "참" if v else "거짓"
        return M("명제 '%s'의 참, 거짓을 판별하면? (x, y, a, b, n은 실수 또는 자연수)" % stmt, ans, ["참" if not v else "거짓", "명제가 아니에요", "알 수 없어요"],
                 "%s<b>%s</b>" % ("명제와 그 대우는 참, 거짓이 같아요. " if k == "대우" else "", ans))
    return mk


# ------------------------------------------------------------------ 충분조건과 필요조건
NS = ["충분조건이지만 필요조건은 아니에요", "필요조건이지만 충분조건은 아니에요", "필요충분조건이에요", "아무 조건도 아니에요"]


def ns_main(kinds=("intv", "set", "k", "proof")):
    def mk():
        how = R.choice(kinds)
        if how == "intv":
            a, b = sorted(R.sample(range(-6, 8), 2))
            kind = R.choice([0, 1, 2, 3])
            if kind == 0:
                c, d = a - R.randint(0, 2), b + R.randint(1, 3)
            elif kind == 1:
                c, d = a + R.randint(0, 1), b - R.randint(1, 2)
                if c >= d:
                    return None
            elif kind == 2:
                c, d = a, b
            else:
                c, d = b + R.randint(0, 2), b + R.randint(3, 5)
            P, Q = (a, b), (c, d)
            sub = lambda X, Y: Y[0] <= X[0] and X[1] <= Y[1]
            pq, qp = sub(P, Q), sub(Q, P)
            ok = NS[2] if pq and qp else NS[0] if pq else NS[1] if qp else NS[3]
            if kind == 2:
                p_txt, q_txt = "%d &lt; x &lt; %d" % P, "|%s| &lt; %s" % (px([1, -Fr(a + b, 2)]), neg(Fr(b - a, 2)))
            else:
                p_txt, q_txt = "%d &lt; x &lt; %d" % P, "%d &lt; x &lt; %d" % Q
            p_txt, q_txt = p_txt.replace("-", "−"), q_txt.replace("-", "−")
            return M("두 조건 p: %s, q: %s에 대하여 p는 q이기 위한 어떤 조건일까요?" % (p_txt, q_txt), ok, [x for x in NS if x != ok],
                     "진리집합 P, Q의 포함 관계를 봐요. %s. <b>%s</b>" % ("P ⊂ Q이고 Q ⊂ P" if pq and qp else "P ⊂ Q" if pq else "Q ⊂ P" if qp else "포함 관계가 없어요", ok))
        if how == "set":
            S_ = [("x = 1", "x² = 1", 0), ("x² = 1", "x = 1", 1), ("x &gt; 2", "x &gt; 0", 0), ("x &gt; 0", "x &gt; 2", 1), ("x² = 2x", "x = 0 또는 x = 2", 2), ("|x| = 3", "x = ±3", 2),
                  ("x는 6의 배수", "x는 3의 배수", 0), ("x가 2의 배수", "x는 6의 배수", 1), ("xy = 0", "x = 0", 1), ("x = 0", "xy = 0", 0), ("x &gt; 1", "x &lt; 1", 3), ("x &lt; 0", "x² &gt; 0", 0),
                  ("x² &gt; 0", "x ≠ 0", 2), ("x² + y² = 0", "x = 0이고 y = 0", 2), ("x + y = 0", "x = 0이고 y = 0", 1), ("삼각형이 정삼각형", "삼각형이 이등변삼각형", 0), ("x² &lt; 4", "x &lt; 2", 0), ("x ≥ 1", "x² ≥ 1", 0)]
            p, q, k = R.choice(S_)
            ok = NS[k]
            return M("p: %s, q: %s일 때, p는 q이기 위한 어떤 조건일까요? (x, y는 실수 또는 자연수)" % (p, q), ok, [x for x in NS if x != ok],
                     "p → q와 q → p가 각각 참인지 확인해요. <b>%s</b>" % ok)
        if how == "k":
            a = R.randint(-3, 3)
            b = R.randint(1, 4)
            kind = R.choice(["suf", "nec"])
            if kind == "suf":
                # p: |x − a| ≤ b, q: x ≤ k (p → q): k ≥ a + b
                return N("두 조건 p: |%s| ≤ %d, q: x ≤ k에 대하여 p가 q이기 위한 충분조건일 때, 실수 k의 최솟값은?" % (px([1, -a]), b), a + b, [a - b, b, a + b + 1, a], "P = {x | %s ≤ x ≤ %s} ⊂ Q이어야 하므로 k ≥ %s. <b>%s</b>" % (neg(a - b), neg(a + b), neg(a + b), neg(a + b)))
            return N("두 조건 p: |%s| ≤ %d, q: x ≥ k에 대하여 q가 p이기 위한 필요조건일 때, 실수 k의 최댓값은?" % (px([1, -a]), b), a - b, [a + b, -b, a - b - 1, a], "P ⊂ Q이어야 하므로 k ≤ %s. <b>%s</b>" % (neg(a - b), neg(a - b)))
        P_ = [("명제 'p → q'를 증명할 때, 대우 '~q → ~p'가 참임을 보이는 방법은?", "대우를 이용한 증명법", ["귀류법", "수학적 귀납법", "반례 찾기"]),
              ("결론을 부정하여 모순이 생김을 보이는 증명 방법은?", "귀류법", ["대우를 이용한 증명법", "직접 증명법", "반례 찾기"]),
              ("√2가 무리수임을 증명할 때 주로 쓰는 방법은?", "귀류법", ["대우를 이용한 증명법", "산술평균과 기하평균", "조립제법"]),
              ("'n²이 짝수이면 n은 짝수이다'를 증명할 때 편리한 방법은?", "대우를 이용한 증명법", ["귀류법", "반례 찾기", "판별식"]),
              ("명제 p → q가 참일 때, 항상 참인 명제는?", "~q → ~p", ["q → p", "~p → ~q", "p → ~q"]),
              ("p ⇒ q이고 q ⇒ p일 때, p는 q이기 위한 무엇일까요?", "필요충분조건", ["충분조건", "필요조건", "아무 조건도 아님"]),
              ("p ⇒ q일 때, q는 p이기 위한 무엇일까요?", "필요조건", ["충분조건", "필요충분조건", "아무 조건도 아님"]),
              ("p ⇒ q일 때, p는 q이기 위한 무엇일까요?", "충분조건", ["필요조건", "필요충분조건", "아무 조건도 아님"]),
              ("진리집합 P, Q에 대하여 P ⊂ Q일 때 참인 명제는?", "p → q", ["q → p", "~p → q", "p → ~q"]),
              ("명제가 거짓임을 보일 때 쓰는 것은?", "반례", ["대우", "역", "귀류법"])]
        q, ok, w = R.choice(P_)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 절대부등식
def ab_main(kinds=("amgm", "prod", "sum", "lin", "concept", "eq")):
    def mk():
        how = R.choice(kinds)
        if how == "amgm":
            a = R.randint(1, 9)
            b = R.choice([v for v in range(1, 50) if math.isqrt(a * v) ** 2 == a * v])
            v = 2 * math.isqrt(a * b)
            X = Fr(math.isqrt(a * b), a)
            ax = px([a, 0])
            return N("x &gt; 0일 때, <b>%s + %s</b>의 최솟값은?" % (ax, fr(b, "x")), v, [a + b, math.isqrt(a * b), 2 * (a + b), v + 1], "산술평균 ≥ 기하평균: %s + %s ≥ 2√(%d) = %d (등호는 x = %s). <b>%d</b>" % (ax, fr(b, "x"), a * b, v, neg(X), v))
        if how == "eq":
            a = R.randint(1, 9)
            b = R.choice([v for v in range(1, 50) if math.isqrt(a * v) ** 2 == a * v])
            X = Fr(math.isqrt(a * b), a)
            return N("x &gt; 0일 때, <b>%s + %s</b>가 최솟값을 갖는 x의 값은?" % (px([a, 0]), fr(b, "x")), X, [2 * math.isqrt(a * b), Fr(a, b), Fr(b, a), X + 1], "등호는 %s = %s일 때, 즉 x² = %s. <b>x = %s</b>" % (px([a, 0]), fr(b, "x"), neg(Fr(b, a)), neg(X)))
        if how == "prod":
            P = R.randint(2, 64)
            ok = surd(2, P)
            return M("x &gt; 0, y &gt; 0이고 xy = %d일 때, x + y의 최솟값은?" % P, ok, [neg(P), surd(1, P), neg(2 * P), surd(4, P), neg(P + 1)], "x + y ≥ 2√(xy) = 2√%d. <b>%s</b>" % (P, ok))
        if how == "sum":
            S_ = R.randint(3, 30)
            v = Fr(S_ * S_, 4)
            return N("x &gt; 0, y &gt; 0이고 x + y = %d일 때, xy의 최댓값은?" % S_, v, [S_ * S_, S_ * S_ // 2, S_, v - 1], "%d = x + y ≥ 2√(xy) → xy ≤ %s. <b>%s</b>" % (S_, neg(v), neg(v)))
        if how == "lin":
            a, b = R.randint(1, 5), R.randint(1, 5)
            S_ = 2 * a * b * R.randint(1, 3)
            v = Fr(S_ * S_, 4 * a * b)
            return N("x &gt; 0, y &gt; 0이고 %s = %d일 때, xy의 최댓값은?" % (poly2({(1, 0): a, (0, 1): b}, ("x", "y")), S_), v, [Fr(S_ * S_, 4), Fr(S_ * S_, 2 * a * b), Fr(S_, a * b), v + 1],
                     "%d ≥ 2√(%dxy) → xy ≤ %s. <b>%s</b>" % (S_, a * b, neg(v), neg(v)))
        C = [("모든 실수 a, b에 대하여 항상 성립하는 부등식은?", "a² + b² ≥ 2ab", ["a + b ≥ 2ab", "a² + b² &gt; 2ab", "a² ≥ b²"]),
             ("a &gt; 0, b &gt; 0일 때 항상 성립하는 부등식은?", "(a + b)/2 ≥ √(ab)", ["(a + b)/2 ≤ √(ab)", "a + b ≥ ab", "√(ab) ≥ a + b"]),
             ("a &gt; 0, b &gt; 0일 때, (a + b)/2 ≥ √(ab)에서 등호가 성립하는 경우는?", "a = b", ["a = 0", "a = 2b", "a + b = 1"]),
             ("모든 실수 x에 대하여 항상 성립하는 부등식은?", "x² − 2x + 1 ≥ 0", ["x² − 2x + 1 &gt; 0", "x² &gt; x", "x + 1 &gt; 0"]),
             ("|a| + |b|와 |a + b|의 관계로 옳은 것은?", "|a| + |b| ≥ |a + b|", ["|a| + |b| ≤ |a + b|", "|a| + |b| = |a + b|", "|a| + |b| &lt; |a + b|"]),
             ("부등식 a² + b² + c² ≥ ab + bc + ca의 등호가 성립하는 경우는?", "a = b = c", ["a + b + c = 0", "abc = 0", "a = b"]),
             ("문자에 어떤 실수를 넣어도 항상 성립하는 부등식을 무엇이라고 할까요?", "절대부등식", ["조건부등식", "항등식", "방정식"]),
             ("a &gt; 0, b &gt; 0일 때, a/b + b/a의 최솟값은?", "2", ["1", "4", "0"]),
             ("a &gt; b &gt; 0일 때, √a − √b와 √(a − b)의 대소 관계는?", "√a − √b &lt; √(a − b)", ["√a − √b &gt; √(a − b)", "√a − √b = √(a − b)", "알 수 없어요"])]
        q, ok, w = R.choice(C)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 함수
def f_main(kinds=("val", "range", "count", "kind", "isf", "eq")):
    def mk():
        how = R.choice(kinds)
        if how == "val":
            a, b, c = R.choice([1, 2, -1, 3]), R.randint(-5, 5), R.randint(-6, 6)
            x = R.randint(-4, 4)
            f = [a, b, c]
            return N("함수 f(x) = %s에 대하여 f(%s)의 값은?" % (px(f), neg(x)), peval(f, x), [peval(f, -x), a * x + b + c, peval(f, x) + 1, c], "x = %s를 대입해요. <b>%s</b>" % (neg(x), neg(peval(f, x))))
        if how == "range":
            X = sorted(R.sample(range(-3, 5), R.randint(3, 4)))
            k = R.choice(["lin", "sq", "abs"])
            if k == "lin":
                a, b = nz(-3, 3), R.randint(-3, 3)
                f = lambda x: a * x + b
                t = px([a, b])
            elif k == "sq":
                f = lambda x: x * x
                t = "x²"
            else:
                f = lambda x: abs(x)
                t = "|x|"
            Y = sorted({f(x) for x in X})
            ok = S(Y)
            w = [S(X), S([f(x) for x in X][:-1]) if len(Y) > 1 else S(Y + [99]), S(sorted({-f(x) for x in X})) if any(Y) else S([1]), S(Y + [max(Y) + 1])]
            return M("정의역이 X = %s인 함수 f(x) = %s의 치역은?" % (S(X), t), ok, w, "정의역의 각 원소의 함숫값을 모아요. <b>%s</b>" % ok)
        if how == "count":
            m, n = R.randint(2, 4), R.randint(2, 5)
            k = R.choice(["all", "inj", "const", "bij"])
            if k == "all":
                v = n ** m
                return N("n(X) = %d, n(Y) = %d일 때, X에서 Y로의 함수의 개수는?" % (m, n), v, [m ** n, m * n, math.perm(n, m) if n >= m else v + 1, v - 1], "X의 각 원소마다 %d가지씩. %d<sup>%d</sup> = <b>%d</b>" % (n, n, m, v), f=lambda t: "%s개" % neg(t))
            if k == "inj":
                if m > n:
                    return None
                v = math.perm(n, m)
                return N("n(X) = %d, n(Y) = %d일 때, X에서 Y로의 일대일함수의 개수는?" % (m, n), v, [n ** m, math.comb(n, m), m * n, v + 1], "<sub>%d</sub>P<sub>%d</sub> = <b>%d</b>" % (n, m, v), f=lambda t: "%s개" % neg(t))
            if k == "const":
                return N("n(X) = %d, n(Y) = %d일 때, X에서 Y로의 상수함수의 개수는?" % (m, n), n, [m, 1, n ** m, m * n], "모든 원소를 Y의 한 원소에 대응시켜요. <b>%d</b>" % n, f=lambda t: "%s개" % neg(t))
            v = math.factorial(n)
            return N("X = Y이고 n(X) = %d일 때, X에서 X로의 일대일대응의 개수는?" % n, v, [n ** n, n, n * n, v // 2], "%d! = <b>%d</b>" % (n, v), f=lambda t: "%s개" % neg(t))
        if how == "kind":
            K = [("f(x) = 2x + 1 (실수 전체에서 실수 전체로)", "일대일대응"), ("f(x) = x² (실수 전체에서 실수 전체로)", "일대일함수도 아닌 함수"), ("f(x) = 3 (실수 전체에서 실수 전체로)", "상수함수"),
                 ("f(x) = x (실수 전체에서 실수 전체로)", "항등함수"), ("f(x) = −x + 4 (실수 전체에서 실수 전체로)", "일대일대응"), ("f(x) = |x| (실수 전체에서 실수 전체로)", "일대일함수도 아닌 함수"),
                 ("f(x) = −5 (실수 전체에서 실수 전체로)", "상수함수"), ("f(x) = x³ (실수 전체에서 실수 전체로)", "일대일대응"), ("f(x) = x² + 1 (실수 전체에서 실수 전체로)", "일대일함수도 아닌 함수"), ("f(x) = −x (실수 전체에서 실수 전체로)", "일대일대응")]
            t, ok = R.choice(K)
            return M("함수 %s는 어떤 함수일까요?" % t, ok, [x for x in ("일대일대응", "항등함수", "상수함수", "일대일함수도 아닌 함수") if x != ok], "<b>%s</b>" % ok)
        if how == "isf":
            Q = [("X의 한 원소에 Y의 원소가 두 개 대응하면 함수일까요?", "함수가 아니에요", ["함수예요", "일대일함수예요", "상수함수예요"]),
                 ("X의 원소 중 대응하는 Y의 원소가 없는 것이 있으면?", "함수가 아니에요", ["함수예요", "항등함수예요", "일대일대응이에요"]),
                 ("함수 f: X → Y에서 Y를 무엇이라고 할까요?", "공역", ["정의역", "치역", "함숫값"]),
                 ("함수 f: X → Y에서 함숫값 전체의 집합을 무엇이라고 할까요?", "치역", ["공역", "정의역", "대응"]),
                 ("일대일대응의 조건으로 옳은 것은?", "일대일함수이고 치역과 공역이 같아요", ["치역이 공역보다 작아요", "모든 원소가 같은 값에 대응해요", "정의역과 치역이 같아요"]),
                 ("그래프가 x축에 평행한 직선과 두 번 이상 만나면?", "일대일함수가 아니에요", ["일대일함수예요", "함수가 아니에요", "항등함수예요"]),
                 ("x축에 수직인 직선과 그래프가 두 점에서 만나면?", "함수의 그래프가 아니에요", ["일대일함수예요", "상수함수예요", "일대일대응이에요"]),
                 ("항등함수 I(x)의 식은?", "I(x) = x", ["I(x) = 1", "I(x) = 0", "I(x) = −x"])]
            q, ok, w = R.choice(Q)
            return M(q, ok, w, "<b>%s</b>" % ok)
        # eq: f(x) = ax + b, f(1) = p, f(2) = q
        a, b = nz(-4, 4), R.randint(-5, 5)
        x1, x2 = R.sample(range(-3, 4), 2)
        y1, y2 = a * x1 + b, a * x2 + b
        x3 = R.randint(-5, 5)
        return N("일차함수 f(x)에 대하여 f(%s) = %s, f(%s) = %s일 때, f(%s)의 값은?" % (neg(x1), neg(y1), neg(x2), neg(y2), neg(x3)), a * x3 + b, [-a * x3 + b, a * x3 - b, a + b, a * x3 + b + a], "f(x) = %s이므로 <b>%s</b>" % (px([a, b]), neg(a * x3 + b)))
    return mk


# ------------------------------------------------------------------ 합성함수와 역함수
def cp_main(kinds=("cval", "cexp", "inv", "invval", "mix", "find")):
    def mk():
        how = R.choice(kinds)
        a, b = nz(-4, 4), R.randint(-5, 5)
        c, d = nz(-3, 3), R.randint(-5, 5)
        f, g = [a, b], [c, d]
        if how == "cval":
            x = R.randint(-4, 4)
            q = R.choice([1, 2])
            if q == 2:
                g2 = [1, 0, d]
                v = peval(f, peval(g2, x))
                return N("f(x) = %s, g(x) = %s일 때, (f ∘ g)(%s)의 값은?" % (px(f), px(g2), neg(x)), v, [peval(g2, peval(f, x)), peval(f, x) + peval(g2, x), peval(f, x) * peval(g2, x), v + a],
                         "g(%s) = %s, f(%s) = <b>%s</b>" % (neg(x), neg(peval(g2, x)), neg(peval(g2, x)), neg(v)))
            v = peval(f, peval(g, x))
            return N("f(x) = %s, g(x) = %s일 때, (f ∘ g)(%s)의 값은?" % (px(f), px(g), neg(x)), v, [peval(g, peval(f, x)), peval(f, x) + peval(g, x), peval(f, x) * peval(g, x), v + 1],
                     "먼저 g(%s) = %s, 다음 f(%s) = <b>%s</b>" % (neg(x), neg(peval(g, x)), neg(peval(g, x)), neg(v)))
        if how == "cexp":
            k = R.choice(["fg", "gf"])
            fg = [a * c, a * d + b]
            gf = [c * a, c * b + d]
            ok = px(fg) if k == "fg" else px(gf)
            alt = px(gf) if k == "fg" else px(fg)
            if ok == alt:
                return None
            return M("f(x) = %s, g(x) = %s일 때, <b>(%s)(x)</b>는?" % (px(f), px(g), "f ∘ g" if k == "fg" else "g ∘ f"), ok, [alt, px([a * c, b + d]), px([a + c, b + d]), px(pmul(f, g)) if a * c else px([1, 0])],
                     "%s. <b>%s</b>" % ("f(g(x)) = %s(%s) %s %d" % (neg(a), px(g), "+" if b >= 0 else "−", abs(b)) if k == "fg" else "g(f(x)) = %s(%s) %s %d" % (neg(c), px(f), "+" if d >= 0 else "−", abs(d)), ok))
        if how == "inv":
            ok = "f<sup>−1</sup>(x) = " + px([Fr(1, a), Fr(-b, a)])
            return M("함수 f(x) = %s의 역함수는?" % px(f), ok, ["f<sup>−1</sup>(x) = " + px([Fr(1, a), Fr(b, a)]), "f<sup>−1</sup>(x) = " + px([a, -b]) if a != 1 or b else "f<sup>−1</sup>(x) = " + px([-1, 0]), "f<sup>−1</sup>(x) = " + px([Fr(-1, a), Fr(b, a)]), "f<sup>−1</sup>(x) = " + px([Fr(1, a), -b])],
                     "y = %s를 x에 대하여 풀고 x와 y를 바꿔요. <b>%s</b>" % (px(f), ok))
        if how == "invval":
            k = R.randint(-5, 5)
            v = a * k + b
            return N("함수 f(x) = %s에 대하여 f<sup>−1</sup>(%s)의 값은?" % (px(f), neg(v)), k, [a * v + b, Fr(v + b, a), -k, k + 1], "f(k) = %s인 k를 찾아요. %s = %s → <b>%s</b>" % (neg(v), px([a, b], "k"), neg(v), neg(k)))
        if how == "mix":
            k = R.randint(-4, 4)
            v = peval(g, k)
            # (f⁻¹ ∘ g)(k) = f⁻¹(g(k))
            r_ = Fr(v - b, a)
            return N("f(x) = %s, g(x) = %s일 때, (f<sup>−1</sup> ∘ g)(%s)의 값은?" % (px(f), px(g), neg(k)), r_, [peval(f, v), Fr(v + b, a), peval(g, Fr(k - b, a)), r_ + 1],
                     "g(%s) = %s, f<sup>−1</sup>(%s) = <b>%s</b>" % (neg(k), neg(v), neg(v), neg(r_)))
        # find: f(x) = ax + b, f⁻¹(p) = q, f(r) = s
        p, q = R.randint(-5, 5), R.randint(-5, 5)
        # f(q) = p and f(0) = b
        if q == 0:
            return None
        a2 = Fr(p - b, q)
        if a2.denominator != 1 or a2 == 0:
            return None
        return N("함수 f(x) = ax %s %d에 대하여 f<sup>−1</sup>(%s) = %s일 때, 상수 a의 값은?" % ("+" if b >= 0 else "−", abs(b), neg(p), neg(q)), a2, [Fr(q - b, p) if p else a2 + 1, -a2, Fr(p + b, q), a2 + 1],
                 "f(%s) = %s이므로 %s = %s. <b>a = %s</b>" % (neg(q), neg(p), px([q, b], "a"), neg(p), neg(a2)))
    return mk


# ------------------------------------------------------------------ 유리함수
def rf(k, p, q):
    """y = k/(x − p) + q → (qx + k − qp)/(x − p)"""
    num_ = px([q, k - q * p]) if q else neg(k)
    return fr(num_, px([1, -p]))


def rs(k, p, q):
    """k/(x − p) ± q"""
    return fr(neg(k), px([1, -p])) + ((" + %d" % q) if q > 0 else (" − %d" % -q) if q < 0 else "")


def ra_main(kinds=("asym", "center", "dom", "val", "trans", "expr", "graph")):
    def mk():
        how = R.choice(kinds)
        k, p, q = nz(-6, 6), R.randint(-4, 4), R.randint(-4, 4)
        if how == "asym":
            ok = "x = %s, y = %s" % (neg(p), neg(q))
            return M("유리함수 <b>y = %s</b>의 점근선의 방정식은?" % rf(k, p, q), ok, ["x = %s, y = %s" % (neg(-p), neg(q)), "x = %s, y = %s" % (neg(q), neg(p)) if p != q else "x = %s, y = %s" % (neg(p), neg(-q - 1)), "x = %s, y = %s" % (neg(-p), neg(-q)), "x = %s, y = %s" % (neg(p), neg(k))],
                     "y = %s 꼴로 고치면 점근선은 x = %s, y = %s. <b>%s</b>" % (rs(k, p, q), neg(p), neg(q), ok))
        if how == "center":
            ok = pt(p, q)
            return M("유리함수 <b>y = %s</b>의 그래프는 어떤 점에 대하여 대칭일까요?" % rs(k, p, q), ok,
                     [pt(-p, q), pt(q, p) if p != q else pt(p, -q - 1), pt(-p, -q), pt(p, k)], "두 점근선의 교점 %s에 대하여 대칭이에요. <b>%s</b>" % (ok, ok))
        if how == "dom":
            kk = R.choice(["d", "r"])
            ok = ("x ≠ %s인 실수 전체" if kk == "d" else "y ≠ %s인 실수 전체") % neg(p if kk == "d" else q)
            alt = ["x ≠ %s인 실수 전체" % neg(-p), "y ≠ %s인 실수 전체" % neg(-q), "x ≠ %s인 실수 전체" % neg(q), "y ≠ %s인 실수 전체" % neg(p), "실수 전체"]
            return M("유리함수 <b>y = %s</b>의 %s은?" % (rf(k, p, q), "정의역" if kk == "d" else "치역"), ok, [x for x in alt if x != ok],
                     "점근선이 x = %s, y = %s예요. <b>%s</b>" % (neg(p), neg(q), ok))
        if how == "val":
            x = R.choice([v for v in range(-6, 7) if v != p and k % (v - p) == 0])
            v = Fr(k, x - p) + q
            return N("유리함수 f(x) = %s에 대하여 f(%s)의 값은?" % (rf(k, p, q), neg(x)), v, [Fr(k, x + p) + q if x + p else v + 2, Fr(k, x - p) - q if q else v - 1, Fr(k + q, x - p), v + 1], "대입하면 <b>%s</b>" % neg(v))
        if how == "trans":
            if p == 0 or q == 0:
                return None
            ok = "y = " + rf(k, p, q)
            return M("유리함수 y = %s의 그래프를 x축의 방향으로 %s만큼, y축의 방향으로 %s만큼 평행이동한 그래프의 식은?" % (fr(neg(k), "x"), neg(p), neg(q)), ok, ["y = " + rf(k, -p, q), "y = " + rf(k, q, p), "y = " + rf(k, -p, -q), "y = " + rf(-k, p, q)],
                     "x 대신 x − %s, y 대신 y − %s. y = %s. <b>%s</b>" % (par(p), par(q), rs(k, p, q), ok))
        if how == "graph":
            if abs(k) > 4:
                return None
            pic = graph([(lambda x, k=k, p=p, q=q: k / (x - p) + q, BLUE, "")], label="유리함수의 그래프")
            X_ = lambda x: 34 + (x + 5) / 10 * (380 - 68)
            Y_ = lambda y: 360 - 34 + 6 - (y + 5) / 10 * (360 - 68)
            dash = "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='6 5'/>"
            pic = pic.replace("</svg>", (dash % (X_(p), Y_(-5), X_(p), Y_(5), RED)) + (dash % (X_(-5), Y_(q), X_(5), Y_(q), RED)) + "</svg>", 1)
            mkf = lambda kk, pp, qq: "y = " + rs(kk, pp, qq)
            ok = mkf(k, p, q)
            return M("그래프가 다음과 같은 유리함수의 식은? (빨간 점선은 점근선이에요)%s" % pic, ok, [mkf(k, -p, q), mkf(-k, p, q), mkf(k, p, -q) if q else mkf(k, p, 1), mkf(k, -p, -q)],
                     "점근선은 x = %s, y = %s이고, 그래프가 지나는 점으로 k = %s. <b>%s</b>" % (neg(p), neg(q), neg(k), ok))
        a = R.randint(1, 6)
        kk = R.choice(["simp", "add"])
        if kk == "simp":
            ok = px([1, a])
            return M("<b>%s</b>를 간단히 하면? (x ≠ %d)" % (fr(px([1, 0, -a * a]), px([1, -a])), a), ok, [px([1, -a]), px([1, 0]), px([1, a * a]), px([1, 2 * a])], "x² − %d = (x + %d)(x − %d)로 약분해요. <b>%s</b>" % (a * a, a, a, ok))
        ok = fr("2x", px([1, 0, -a * a]))
        return M("<b>%s + %s</b>를 계산하면?" % (fr(1, px([1, -a])), fr(1, px([1, a]))), ok, [fr(2, px([1, 0, -a * a])), fr(2 * a, px([1, 0, -a * a])), fr("2x", "x²"), fr("2x", px([1, 0, a * a]))], "통분하면 분자는 (x + %d) + (x − %d) = 2x. <b>%s</b>" % (a, a, ok))
    return mk


# ------------------------------------------------------------------ 무리함수
def sqf(a, p, q, s=1):
    """y = s√(a(x − p)) + q"""
    inner = px([a, -a * p])
    t = ("−" if s < 0 else "") + "√(%s)" % inner if (a, p) != (1, 0) else ("−" if s < 0 else "") + "√x"
    if (a, p) == (-1, 0):
        t = ("−" if s < 0 else "") + "√(−x)"
    return "y = " + t + ((" + %d" % q) if q > 0 else (" − %d" % -q) if q < 0 else "")


def ir_main(kinds=("dom", "rng", "start", "val", "trans", "real", "rat", "graph")):
    def mk():
        how = R.choice(kinds)
        a = R.choice([1, 2, 3, -1, -2])
        p, q = R.randint(-4, 4), R.randint(-4, 4)
        s = R.choice([1, 1, -1])
        f = sqf(a, p, q, s)
        if how == "dom":
            ok = ("x ≥ %s" if a > 0 else "x ≤ %s") % neg(p)
            return M("무리함수 <b>%s</b>의 정의역은?" % f, ok, [("x ≤ %s" if a > 0 else "x ≥ %s") % neg(p), ("x ≥ %s" if a > 0 else "x ≤ %s") % neg(-p), "y ≥ %s" % neg(q), ("x ≥ %s" if a > 0 else "x ≤ %s") % neg(q) if q != p else "실수 전체"],
                     "근호 안이 0 이상이어야 해요: %s ≥ 0. <b>%s</b>" % (px([a, -a * p]), ok))
        if how == "rng":
            ok = ("y ≥ %s" if s > 0 else "y ≤ %s") % neg(q)
            return M("무리함수 <b>%s</b>의 치역은?" % f, ok, [("y ≤ %s" if s > 0 else "y ≥ %s") % neg(q), ("y ≥ %s" if s > 0 else "y ≤ %s") % neg(-q) if q else "실수 전체", ("y ≥ %s" if s > 0 else "y ≤ %s") % neg(p) if p != q else "y ≥ 0", ("x ≥ %s" if a > 0 else "x ≤ %s") % neg(p)],
                     "√ 부분은 0 이상이므로 %s. <b>%s</b>" % ("√(…)%s ≥ %s" % (" %s %d" % ("+" if q > 0 else "−", abs(q)) if q else "", neg(q)) if s > 0 else "−√(…)%s ≤ %s" % (" %s %d" % ("+" if q > 0 else "−", abs(q)) if q else "", neg(q)), ok))
        if how == "start":
            ok = pt(p, q)
            return M("무리함수 <b>%s</b>의 그래프가 시작하는 점의 좌표는?" % f, ok, [pt(-p, q), pt(q, p) if p != q else pt(p, -q - 1), pt(-p, -q), pt(p, 0) if q else pt(0, q + 1)], "근호 안이 0이 되는 x = %s에서 y = %s. <b>%s</b>" % (neg(p), neg(q), ok))
        if how == "val":
            t = R.randint(0, 5)
            if a < 0:
                x = p - Fr(t * t, -a)
            else:
                x = p + Fr(t * t, a)
            if x.denominator != 1:
                return None
            v = s * t + q
            return N("무리함수 f(x) = %s에 대하여 f(%s)의 값은?" % (f[4:], neg(x)), v, [-s * t + q, s * t - q if q else v + 1, t * t + q, v + 2], "근호 안이 %d이므로 √%d = %d. <b>%s</b>" % (t * t, t * t, t, neg(v)))
        if how == "trans":
            if p == 0 or q == 0:
                return None
            base = "y = %s√%s" % ("−" if s < 0 else "", "x" if a == 1 else ("(%s)" % px([a, 0])))
            ok = f
            return M("무리함수 %s의 그래프를 x축의 방향으로 %s만큼, y축의 방향으로 %s만큼 평행이동한 그래프의 식은?" % (base, neg(p), neg(q)), ok, [sqf(a, -p, q, s), sqf(a, q, p, s) if p != q else sqf(a, p, -q, s), sqf(a, -p, -q, s), sqf(a, p, q, -s)],
                     "x 대신 x − %s, y 대신 y − %s를 넣어요. <b>%s</b>" % (par(p), par(q), ok))
        if how == "real":
            a1, b1 = sorted(R.sample(range(-5, 9), 2))
            ok = "%s ≤ x ≤ %s" % (neg(a1), neg(b1))
            return M("<b>√(%s) + √(%s)</b>의 값이 실수가 되기 위한 x의 값의 범위는?" % (px([1, -a1]), px([-1, b1])), ok, ["%s &lt; x &lt; %s" % (neg(a1), neg(b1)), "x ≤ %s 또는 x ≥ %s" % (neg(a1), neg(b1)), "%s ≤ x ≤ %s" % (neg(-b1), neg(-a1)), "x ≥ %s" % neg(a1)],
                     "%s ≥ 0이고 %s ≥ 0. <b>%s</b>" % (px([1, -a1]), px([-1, b1]), ok))
        if how == "graph":
            if s < 0 or abs(a) > 2 or q > 1 or q < -3 or (a > 0 and p > 1) or (a < 0 and p < -1):
                return None
            pic = graph([(lambda x, a=a, p=p, q=q: math.sqrt(a * (x - p)) + q, BLUE, "")], pts=[(p, q, "")], label="무리함수의 그래프")
            ok = f
            return M("그래프가 다음과 같은 무리함수의 식은?%s" % pic, ok, [sqf(a, -p, q, s), sqf(a, p, -q, s) if q else sqf(a, p, 1, s), sqf(-a, p, q, s), sqf(a, q, p, s) if p != q else sqf(a, -p, -q, s)],
                     "시작점 %s와 그래프가 뻗는 방향을 봐요. <b>%s</b>" % (pt(p, q), ok))
        n_ = R.randint(1, 8)
        kk = R.choice(["add", "sub"])
        ok = "√%d − √%d" % (n_ + 1, n_) if n_ > 1 else "√2 − 1"
        if n_ + 1 in (4, 9):
            ok = "%d − √%d" % (math.isqrt(n_ + 1), n_)
        if n_ in (4, 9):
            ok = "√%d − %d" % (n_ + 1, math.isqrt(n_))
        rt = lambda v: str(math.isqrt(v)) if math.isqrt(v) ** 2 == v else "√%d" % v
        okk = "%s − %s" % (rt(n_ + 1), rt(n_))
        w = ["%s + %s" % (rt(n_ + 1), rt(n_)), "%s − %s" % (rt(n_), rt(n_ + 1)), fr("%s − %s" % (rt(n_ + 1), rt(n_)), 2 * n_ + 1)]
        return M("<b>%s</b>의 분모를 유리화하면?" % fr(1, "%s + %s" % (rt(n_ + 1), rt(n_))), okk, w, "분모와 분자에 %s − %s를 곱하면 분모는 %d − %d = 1. <b>%s</b>" % (rt(n_ + 1), rt(n_), n_ + 1, n_, okk))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    U = {}
    U["dist"] = ("distance-and-internal-division", 1, "[10공수2-01-01]", "선분의 내분을 이해하고, 내분점의 좌표를 계산할 수 있다.",
                 "두 점 사이의 거리와 선분의 내분점", "거리와 내분점",
                 "고등학교 공통수학2 두 점 사이의 거리와 내분점 문제: 좌표평면 위의 두 점 사이의 거리, 수직선과 좌표평면에서 선분의 내분점, 중점, 삼각형의 무게중심, 거리 조건으로 좌표 구하기까지 100문제와 정답·해설.",
                 "내분점의 x좌표 (mx₂ + nx₁)/(m + n)", "거리는 피타고라스 정리, 무게중심은 세 꼭짓점 좌표의 평균이에요.",
                 ["두 점 A(x₁, y₁), B(x₂, y₂) 사이의 거리는 AB = √((x₂ − x₁)² + (y₂ − y₁)²)이에요.",
                  "선분 AB를 m : n으로 내분하는 점의 좌표는 ((mx₂ + nx₁)/(m + n), (my₂ + ny₁)/(m + n))이에요.",
                  "m = n = 1이면 중점 ((x₁ + x₂)/2, (y₁ + y₂)/2)예요.",
                  "삼각형의 무게중심은 ((x₁ + x₂ + x₃)/3, (y₁ + y₂ + y₃)/3)이에요."],
                 [("A(1, 2), B(4, 6) 사이의 거리", ["√(3² + 4²)"], "5"), ("A(1, 2), B(7, 5)를 2 : 1로 내분", ["((2·7 + 1·1)/3, (2·5 + 1·2)/3)"], "(5, 4)")],
                 [("내분점에서 m을 x₁에 곱한다", "m은 B 쪽(x₂)에 곱해요."), ("거리에서 제곱을 하지 않고 더한다", "가로·세로 차를 제곱해서 더한 뒤 √를 씌워요."), ("무게중심을 2로 나눈다", "세 점의 평균이므로 3으로 나눠요.")],
                 [("내분점은 A와 B 중 어느 쪽에 가깝나요?", "m &lt; n이면 A에 더 가까워요."), ("거리가 같은 점은 어떻게 구하나요?", "거리의 제곱이 같다는 식을 세워 풀어요.")],
                 [("두 점 사이의 거리", [(d_main(("dist",)), 20)]), ("수직선 위의 내분점", [(d_main(("line1",)), 20)]), ("좌표평면 위의 내분점", [(d_main(("div",)), 20)]),
                  ("중점과 무게중심", [(d_main(("mid",)), 10), (d_main(("cent",)), 10)]), ("거리 조건", [(d_main(("find",)), 10), (d_main(("dist", "div")), 10)])], 83101)
    U["line"] = ("equations-of-lines", 2, "[10공수2-01-02]", "두 직선의 평행 조건과 수직 조건을 탐구하고 이해한다.",
                 "직선의 방정식과 평행·수직 조건", "직선의 방정식",
                 "고등학교 공통수학2 직선의 방정식 문제: 한 점과 기울기, 두 점을 지나는 직선, 평행한 직선과 수직인 직선, 평행·수직 조건으로 미지수 구하기, 두 직선의 교점까지 100문제와 정답·해설.",
                 "평행: 기울기 같음, 수직: 기울기 곱 −1", "y − y₁ = m(x − x₁)로 직선을 세워요.",
                 ["점 (x₁, y₁)을 지나고 기울기가 m인 직선은 y − y₁ = m(x − x₁)이에요.",
                  "두 점을 지나는 직선의 기울기는 (y₂ − y₁) ÷ (x₂ − x₁)이에요.",
                  "두 직선 y = mx + n, y = m′x + n′은 m = m′, n ≠ n′이면 평행, mm′ = −1이면 수직이에요.",
                  "ax + by + c = 0, a′x + b′y + c′ = 0이 수직이면 aa′ + bb′ = 0이에요."],
                 [("(1, 2)를 지나고 기울기 3", ["y − 2 = 3(x − 1)"], "y = 3x − 1"), ("y = 2x + 1에 수직, 원점을 지남", ["기울기 −1/2"], "y = −x/2")],
                 [("수직 조건을 기울기의 곱 1로 쓴다", "곱이 −1이에요."), ("평행한 직선의 기울기를 역수로 쓴다", "평행하면 기울기가 같아요."), ("y − y₁ = m(x − x₁)에서 부호를 바꾼다", "x₁, y₁을 빼요.")],
                 [("기울기가 없는 직선은?", "x = a 꼴의 직선은 y축에 평행하고 기울기가 정의되지 않아요."), ("일반형에서 기울기는?", "ax + by + c = 0의 기울기는 −a/b예요.")],
                 [("한 점과 기울기", [(l_main(("pt_slope",)), 20)]), ("두 점을 지나는 직선", [(l_main(("two",)), 20)]), ("평행한 직선과 수직인 직선", [(l_main(("par", "perp")), 20)]),
                  ("평행·수직 조건", [(l_main(("kpar", "kperp")), 20)]), ("교점을 지나는 직선", [(l_main(("int",)), 12), (l_main(("par", "perp")), 8)])], 83102)
    U["pdist"] = ("distance-from-a-point-to-a-line", 3, "[10공수2-01-03]", "점과 직선 사이의 거리를 구하고, 관련된 문제를 해결할 수 있다.",
                  "점과 직선 사이의 거리", "점과 직선 사이의 거리",
                  "고등학교 공통수학2 점과 직선 사이의 거리 문제: 점과 직선 사이의 거리 공식, 원점과 직선 사이의 거리, 평행한 두 직선 사이의 거리, 삼각형의 넓이, 거리 조건으로 미지수 구하기까지 100문제와 정답·해설.",
                  "|ax₁ + by₁ + c| ÷ √(a² + b²)", "평행한 두 직선 사이의 거리는 한 점에서 다른 직선까지의 거리예요.",
                  ["점 (x₁, y₁)과 직선 ax + by + c = 0 사이의 거리는 |ax₁ + by₁ + c| ÷ √(a² + b²)이에요.",
                   "원점과의 거리는 |c| ÷ √(a² + b²)예요.",
                   "평행한 두 직선 ax + by + c = 0, ax + by + c′ = 0 사이의 거리는 |c − c′| ÷ √(a² + b²)예요.",
                   "삼각형의 넓이는 (밑변) × (꼭짓점에서 밑변까지의 거리) ÷ 2로 구해요."],
                  [("(1, 2)와 3x + 4y − 1 = 0", ["|3 + 8 − 1| ÷ 5"], "2"), ("3x + 4y + 1 = 0, 3x + 4y − 9 = 0", ["|1 − (−9)| ÷ 5"], "2")],
                  [("절댓값을 빠뜨린다", "거리는 항상 0 이상이에요."), ("분모를 a² + b²로 쓴다", "√(a² + b²)예요."), ("일반형으로 바꾸지 않고 대입한다", "ax + by + c = 0 꼴로 먼저 고쳐요.")],
                  [("y = mx + n 꼴이면?", "mx − y + n = 0으로 고쳐서 공식을 써요."), ("거리가 주어지면 해가 두 개인 이유는?", "절댓값 방정식이라 양쪽에 하나씩 있어요.")],
                  [("점과 직선 사이의 거리", [(p_main(("pd",)), 20)]), ("원점과 직선", [(p_main(("origin",)), 20)]), ("평행한 두 직선", [(p_main(("par",)), 20)]),
                   ("삼각형의 넓이", [(p_main(("area",)), 12), (p_main(("pd",)), 8)]), ("거리 조건", [(p_main(("k",)), 20)])], 83103)
    U["circ"] = ("equations-of-circles", 4, "[10공수2-01-04]", "원의 방정식을 구하고, 그래프를 그릴 수 있다.",
                 "원의 방정식", "원의 방정식",
                 "고등학교 공통수학2 원의 방정식 문제: (x − a)² + (y − b)² = r²의 중심과 반지름, 원의 방정식 세우기, 일반형을 표준형으로 고치기, 지름의 양 끝이 주어진 원, 축에 접하는 원, 원이 될 조건까지 100문제와 정답·해설.",
                 "(x − a)² + (y − b)² = r²", "일반형은 완전제곱식으로 고쳐 중심과 반지름을 찾아요.",
                 ["중심이 (a, b), 반지름의 길이가 r인 원의 방정식은 (x − a)² + (y − b)² = r²이에요.",
                  "x² + y² + Ax + By + C = 0은 완전제곱식으로 고쳐 중심 (−A/2, −B/2)와 반지름을 구해요.",
                  "지름의 양 끝이 주어지면 중심은 중점, 반지름은 지름의 절반이에요.",
                  "x축에 접하면 반지름 = |중심의 y좌표|, y축에 접하면 반지름 = |중심의 x좌표|예요."],
                 [("x² + y² − 4x + 6y − 3 = 0", ["(x − 2)² + (y + 3)² = 16"], "중심 (2, −3), 반지름 4"), ("중심 (1, −2), 반지름 3", ["(x − 1)² + (y + 2)² = 9"], "")],
                 [("반지름을 r²으로 답한다", "우변의 제곱근이 반지름이에요."), ("(x + 2)²에서 중심의 x좌표를 2로 읽는다", "x − (−2)이므로 −2예요."), ("x축에 접하는 원의 반지름을 x좌표로 정한다", "y좌표의 절댓값이에요.")],
                 [("원이 되지 않는 경우는?", "완전제곱식으로 고쳤을 때 우변이 0 이하이면 원이 아니에요."), ("세 점을 지나는 원은?", "일반형에 세 점을 대입해 A, B, C를 구해요.")],
                 [("중심과 반지름 읽기", [(c_main(("read",)), 20)]), ("원의 방정식 세우기", [(c_main(("write",)), 20)]), ("일반형", [(c_main(("gen",)), 20)]),
                  ("지름과 접하는 원", [(c_main(("diam", "tan")), 20)]), ("원이 될 조건", [(c_main(("k",)), 10), (c_main(("gen", "diam")), 10)])], 83104)
    U["cl"] = ("circles-and-lines", 5, "[10공수2-01-05]", "좌표평면에서 원과 직선의 위치 관계를 판단하고, 이를 활용하여 문제를 해결할 수 있다.",
               "원과 직선의 위치 관계", "원과 직선",
               "고등학교 공통수학2 원과 직선의 위치 관계 문제: 중심과 직선 사이의 거리와 반지름 비교, 교점의 개수, 접할 조건, 원 위의 점에서의 접선, 현의 길이, 접선의 길이까지 100문제와 정답·해설.",
               "d와 r을 비교해요", "d가 r보다 작으면 두 점, 같으면 접하고, 크면 만나지 않아요.",
               ["원의 중심과 직선 사이의 거리 d와 반지름 r을 비교해요. d &lt; r이면 두 점에서 만나고, d = r이면 접하고, d &gt; r이면 만나지 않아요.",
                "직선의 식을 원의 방정식에 대입한 이차방정식의 판별식으로도 판단할 수 있어요.",
                "원 x² + y² = r² 위의 점 (x₁, y₁)에서의 접선은 x₁x + y₁y = r²이에요.",
                "현의 절반, 중심까지의 거리, 반지름은 직각삼각형을 이루어요."],
               [("x² + y² = 5와 y = 2x + 5", ["d = 5 ÷ √5 = √5"], "접해요"), ("x² + y² = 25 위의 (3, 4)에서의 접선", ["3x + 4y = 25"], "")],
               [("d를 구할 때 절댓값을 빠뜨린다", "거리는 0 이상이에요."), ("접선을 x₁x + y₁y = r로 쓴다", "우변은 r²이에요."), ("현의 길이를 절반만 답한다", "피타고라스로 구한 값의 2배예요.")],
               [("판별식과 거리 중 어느 것이 편한가요?", "원의 중심이 원점이 아니면 거리 공식이 더 간단할 때가 많아요."), ("접선의 길이는?", "중심까지 거리의 제곱에서 r²을 빼고 √를 씌워요.")],
               [("위치 관계", [(cl_main(("pos",)), 20)]), ("교점의 개수", [(cl_main(("count",)), 20)]), ("접할 조건과 만날 조건", [(cl_main(("k",)), 20)]),
                ("원 위의 점에서의 접선", [(cl_main(("tline",)), 15), (cl_main(("k",)), 5)]), ("현과 접선의 길이", [(cl_main(("chord", "tlen")), 20)])], 83105)
    U["move"] = ("translations-and-reflections", 6, "[10공수2-01-06] [10공수2-01-07]", "평행이동을 탐구하고, 실생활과 연결하여 문제를 해결할 수 있다. 원점, x축, y축, 직선 y = x에 대한 대칭이동을 탐구하고, 실생활과 연결하여 문제를 해결할 수 있다.",
                 "평행이동과 대칭이동", "평행이동과 대칭이동",
                 "고등학교 공통수학2 평행이동과 대칭이동 문제: 점·직선·원의 평행이동, x축·y축·원점·직선 y = x에 대한 대칭이동, 평행이동의 규칙 찾기까지 100문제와 정답·해설.",
                 "도형의 평행이동은 x → x − a, y → y − b", "x축 대칭은 y를 −y, y = x 대칭은 x와 y를 바꿔요.",
                 ["점 (x, y)를 x축 방향으로 a, y축 방향으로 b만큼 평행이동하면 (x + a, y + b)예요.",
                  "도형 f(x, y) = 0의 평행이동은 f(x − a, y − b) = 0이에요.",
                  "x축 대칭: (x, −y), y축 대칭: (−x, y), 원점 대칭: (−x, −y), 직선 y = x 대칭: (y, x)",
                  "원을 이동할 때는 중심만 이동하고 반지름은 그대로예요."],
                 [("y = 2x + 1을 (1, 3)만큼 평행이동", ["y − 3 = 2(x − 1) + 1"], "y = 2x + 2"), ("(2, −5)를 y = x에 대칭", ["x, y 바꾸기"], "(−5, 2)")],
                 [("도형의 평행이동에서 x + a를 넣는다", "점은 더하고, 도형의 식에는 x − a를 넣어요."), ("x축 대칭에서 x좌표의 부호를 바꾼다", "y좌표의 부호를 바꿔요."), ("원의 반지름도 바꾼다", "이동해도 반지름은 그대로예요.")],
                 [("평행이동과 대칭이동을 함께 하면?", "주어진 순서대로 한 번씩 해요. 순서가 바뀌면 결과가 달라질 수 있어요."), ("대칭이동하면 모양이 바뀌나요?", "모양과 크기는 그대로예요.")],
                 [("점의 평행이동", [(mv_main(("ptmove",)), 12), (mv_main(("find",)), 8)]), ("도형의 평행이동", [(mv_main(("linemove", "circmove")), 20)]), ("점의 대칭이동", [(mv_main(("ptref",)), 20)]),
                  ("도형의 대칭이동", [(mv_main(("lineref", "circref")), 20)]), ("섞어서 연습", [(mv_main(), 20)])], 83106)
    U["sets"] = ("sets", 7, "[10공수2-02-01] [10공수2-02-02]", "집합의 개념을 이해하고, 집합을 표현할 수 있다. 두 집합 사이의 포함관계를 판단할 수 있다.",
                 "집합의 뜻과 포함 관계", "집합",
                 "고등학교 공통수학2 집합 문제: 원소나열법과 조건제시법, 원소의 개수 n(A), ∈와 ⊂, 부분집합과 진부분집합의 개수, 특정한 원소를 포함하거나 포함하지 않는 부분집합까지 100문제와 정답·해설.",
                 "원소가 n개인 집합의 부분집합은 2ⁿ개", "원소에는 ∈, 집합 사이에는 ⊂를 써요.",
                 ["대상이 분명한 것들의 모임을 <b>집합</b>, 그 대상을 <b>원소</b>라고 해요. a가 A의 원소이면 a ∈ A예요.",
                  "원소를 모두 쓰는 원소나열법, 조건으로 나타내는 조건제시법 {x | 조건}이 있어요.",
                  "A의 모든 원소가 B에 속하면 A ⊂ B(부분집합)이고, ∅는 모든 집합의 부분집합이에요.",
                  "원소가 n개인 집합의 부분집합은 2ⁿ개, 진부분집합은 2ⁿ − 1개예요."],
                 [("A = {1, 2, 3}의 부분집합", ["2³"], "8개"), ("1을 포함하는 {1, 2, 3, 4}의 부분집합", ["2³"], "8개")],
                 [("부분집합의 개수를 2n으로 센다", "2ⁿ이에요."), ("{1} ∈ A라고 쓴다", "{1}은 집합이므로 {1} ⊂ A예요."), ("∅를 부분집합에서 빠뜨린다", "∅도 부분집합이에요.")],
                 [("∅와 {0}은 같나요?", "아니에요. {0}은 원소 0을 가진 집합이에요."), ("A ⊂ B이고 B ⊂ A이면?", "두 집합은 서로 같아요(A = B).")],
                 [("원소나열법", [(st_main(("elem",)), 20)]), ("조건제시법과 원소의 개수", [(st_main(("builder",)), 8), (st_main(("n",)), 12)]), ("포함 관계", [(st_main(("rel",)), 20)]),
                  ("부분집합의 개수", [(st_main(("sub",)), 20)]), ("조건이 있는 부분집합", [(st_main(("count",)), 20)])], 83107)
    U["setop"] = ("set-operations", 8, "[10공수2-02-03]", "집합의 연산을 수행하고, 벤 다이어그램을 이용하여 나타낼 수 있다.",
                  "합집합, 교집합, 여집합, 차집합", "집합의 연산",
                  "고등학교 공통수학2 집합의 연산 문제: 합집합·교집합·차집합·여집합 구하기, 드모르간의 법칙, n(A ∪ B) = n(A) + n(B) − n(A ∩ B), 벤 다이어그램을 이용한 문장제까지 100문제와 정답·해설.",
                  "합집합의 원소 수는 겹친 만큼 빼요", "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)",
                  ["A ∪ B는 A 또는 B에 속하는 원소, A ∩ B는 A와 B에 모두 속하는 원소의 집합이에요.",
                   "A − B는 A에는 속하고 B에는 속하지 않는 원소, A<sup>C</sup>는 U − A예요.",
                   "드모르간의 법칙: (A ∪ B)<sup>C</sup> = A<sup>C</sup> ∩ B<sup>C</sup>, (A ∩ B)<sup>C</sup> = A<sup>C</sup> ∪ B<sup>C</sup>",
                   "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)"],
                  [("A = {1, 2, 3}, B = {2, 3, 4}", ["A ∪ B = {1, 2, 3, 4}", "A ∩ B = {2, 3}"], "A − B = {1}"), ("n(A) = 10, n(B) = 8, n(A ∩ B) = 3", ["10 + 8 − 3"], "n(A ∪ B) = 15")],
                  [("n(A ∪ B) = n(A) + n(B)로 계산한다", "겹치는 부분을 한 번 빼요."), ("A − B와 B − A를 같게 생각한다", "순서가 바뀌면 다른 집합이에요."), ("(A ∪ B)ᶜ = Aᶜ ∪ Bᶜ로 쓴다", "∪는 ∩로 바뀌어요.")],
                  [("벤 다이어그램은 왜 쓰나요?", "겹치는 부분과 겹치지 않는 부분을 한눈에 볼 수 있어요."), ("서로소란?", "A ∩ B = ∅인 두 집합이에요.")],
                  [("합집합과 교집합", [(so_main(("cup", "cap")), 20)]), ("차집합과 여집합", [(so_main(("diff", "comp")), 20)]), ("드모르간의 법칙", [(so_main(("dem",)), 20)]),
                   ("원소의 개수", [(so_main(("ncup",)), 20)]), ("문장제", [(so_main(("word",)), 20)])], 83108)
    U["prop"] = ("propositions-and-conditions", 9, "[10공수2-02-04] [10공수2-02-05]", "명제와 조건의 뜻을 알고, '모든', '어떤'을 포함한 명제를 이해하고 설명할 수 있다. 명제의 역과 대우를 이해하고 설명할 수 있다.",
                 "명제와 조건, 역과 대우", "명제와 조건",
                 "고등학교 공통수학2 명제와 조건 문제: 진리집합, 조건의 부정, '모든'과 '어떤'을 포함한 명제의 참·거짓과 부정, 명제의 역과 대우, 대우를 이용한 참·거짓 판별까지 100문제와 정답·해설.",
                 "명제와 그 대우는 참·거짓이 같아요", "역은 가정과 결론을 바꾼 것, 대우는 바꾸고 둘 다 부정한 것이에요.",
                 ["참, 거짓을 판별할 수 있는 문장이나 식을 <b>명제</b>, 변수에 따라 참·거짓이 정해지는 것을 <b>조건</b>이라고 해요.",
                  "조건을 참이 되게 하는 원소의 집합을 <b>진리집합</b>이라고 해요. 부정 ~p의 진리집합은 P<sup>C</sup>예요.",
                  "'모든 x에 대하여 p'의 부정은 '어떤 x에 대하여 ~p', '어떤 x에 대하여 p'의 부정은 '모든 x에 대하여 ~p'예요.",
                  "p → q의 역은 q → p, 대우는 ~q → ~p이고, 명제와 대우는 참·거짓이 같아요."],
                 [("'x = 2이면 x² = 4이다'의 역", ["가정과 결론을 바꿈"], "x² = 4이면 x = 2이다 (거짓)"), ("'x &gt; 3'의 부정", ["부등호 반대, 등호 포함"], "x ≤ 3")],
                 [("'x &gt; 3'의 부정을 'x &lt; 3'으로 쓴다", "x = 3도 포함해 x ≤ 3이에요."), ("'또는'의 부정을 '또는'으로 쓴다", "'이고'로 바뀌어요."), ("역과 대우를 바꾼다", "대우는 바꾸고 둘 다 부정해요.")],
                 [("역이 참이면 원래 명제도 참인가요?", "아니에요. 대우만 참·거짓이 같아요."), ("반례는 무엇인가요?", "가정은 만족하지만 결론을 만족하지 않는 예예요.")],
                 [("진리집합", [(pr_main(("truth",)), 20)]), ("조건의 부정", [(pr_main(("neg",)), 10), (pr_main(("truth",)), 10)]), ("'모든'과 '어떤'", [(pr_main(("quant",)), 20)]),
                  ("역과 대우", [(pr_main(("conv",)), 20)]), ("참, 거짓 판별", [(pr_main(("tf",)), 20)])], 83109)
    U["nec"] = ("necessary-and-sufficient-conditions", 10, "[10공수2-02-06] [10공수2-02-07]", "충분조건과 필요조건을 이해하고 판단할 수 있다. 대우를 이용한 증명법과 귀류법을 이해하고 관련된 명제를 증명할 수 있다.",
                "충분조건과 필요조건, 증명법", "충분조건과 필요조건",
                "고등학교 공통수학2 충분조건과 필요조건 문제: 진리집합의 포함 관계로 충분조건·필요조건·필요충분조건 판단하기, 조건을 만족하는 상수의 범위, 대우를 이용한 증명법과 귀류법까지 100문제와 정답·해설.",
                "p ⇒ q이면 p는 충분, q는 필요조건", "진리집합 P ⊂ Q이면 p ⇒ q예요.",
                ["p → q가 참일 때 p ⇒ q로 쓰고, p는 q이기 위한 <b>충분조건</b>, q는 p이기 위한 <b>필요조건</b>이에요.",
                 "p ⇒ q이고 q ⇒ p이면 p는 q이기 위한 <b>필요충분조건</b>이에요.",
                 "진리집합으로 판단해요: P ⊂ Q이면 p ⇒ q예요.",
                 "대우를 이용한 증명법은 ~q → ~p를 보이고, 귀류법은 결론을 부정해서 모순을 이끌어요."],
                [("p: x = 1, q: x² = 1", ["p ⇒ q (참)", "q ⇒ p (x = −1이 반례)"], "충분조건"), ("p: |x − 1| ≤ 2, q: x ≤ k", ["P = {x | −1 ≤ x ≤ 3} ⊂ Q"], "k ≥ 3")],
                [("충분조건과 필요조건을 반대로 쓴다", "화살표가 나가는 쪽(p)이 충분조건이에요."), ("한쪽만 확인하고 필요충분조건이라고 한다", "양쪽 방향을 모두 확인해요."), ("포함 관계를 반대로 쓴다", "p ⇒ q이면 P ⊂ Q예요.")],
                [("귀류법은 언제 쓰나요?", "'~가 아니다', '무리수이다'처럼 직접 보이기 어려운 결론에 많이 써요."), ("필요충분조건의 예는?", "x² = 0과 x = 0처럼 진리집합이 같을 때예요.")],
                [("구간으로 판단하기", [(ns_main(("intv",)), 20)]), ("여러 가지 조건", [(ns_main(("set",)), 18), (ns_main(("intv",)), 2)]), ("상수의 범위", [(ns_main(("k",)), 20)]),
                 ("증명법", [(ns_main(("proof",)), 10), (ns_main(("intv", "k")), 10)]), ("섞어서 연습", [(ns_main(("intv", "k")), 20)])], 83110)
    U["absin"] = ("absolute-inequalities", 11, "[10공수2-02-08]", "절대부등식의 뜻을 알고, 간단한 절대부등식을 증명할 수 있다.",
                  "절대부등식과 산술평균·기하평균", "절대부등식",
                  "고등학교 공통수학2 절대부등식 문제: 절대부등식의 뜻, a² + b² ≥ 2ab, 산술평균과 기하평균의 관계, 합이나 곱이 일정할 때의 최댓값과 최솟값, 등호가 성립하는 조건까지 100문제와 정답·해설.",
                  "(a + b)/2 ≥ √(ab) (a, b > 0)", "등호는 a = b일 때 성립해요.",
                  ["문자에 어떤 실수를 대입해도 항상 성립하는 부등식을 <b>절대부등식</b>이라고 해요.",
                   "a² + b² ≥ 2ab, |a| + |b| ≥ |a + b|는 모든 실수에서 성립해요.",
                   "a &gt; 0, b &gt; 0일 때 (a + b)/2 ≥ √(ab)(산술평균 ≥ 기하평균)이고 등호는 a = b일 때예요.",
                   "곱이 일정하면 합의 최솟값을, 합이 일정하면 곱의 최댓값을 구할 수 있어요."],
                  [("x &gt; 0, x + 9/x", ["≥ 2√9 = 6", "등호 x = 3"], "최솟값 6"), ("x + y = 10, xy", ["10 ≥ 2√(xy)"], "최댓값 25")],
                  [("등호 조건을 확인하지 않는다", "등호가 성립하는 x가 있어야 최솟값이에요."), ("음수에도 산술·기하평균을 쓴다", "a, b가 양수일 때만 써요."), ("최솟값을 √(ab)로 답한다", "a + b ≥ 2√(ab)이므로 2배예요.")],
                  [("절대부등식은 어떻게 증명하나요?", "(좌변) − (우변)이 완전제곱식 등으로 0 이상임을 보여요."), ("조건부등식이란?", "x &gt; 2처럼 특정한 값에서만 성립하는 부등식이에요.")],
                  [("절대부등식의 뜻", [(ab_main(("concept",)), 9), (ab_main(("prod", "sum")), 11)]), ("x + a/x의 최솟값", [(ab_main(("amgm",)), 20)]), ("등호 조건", [(ab_main(("eq",)), 20)]),
                   ("합과 곱이 일정할 때", [(ab_main(("prod", "sum")), 20)]), ("ax + by가 일정할 때", [(ab_main(("lin",)), 20)])], 83111)
    U["func"] = ("functions", 12, "[10공수2-03-01]", "함수의 개념을 설명하고, 그 그래프를 이해한다.",
                 "함수의 뜻과 그래프", "함수",
                 "고등학교 공통수학2 함수 문제: 함수의 뜻, 정의역·공역·치역, 함숫값, 일대일함수·일대일대응·항등함수·상수함수, 함수의 개수까지 100문제와 정답·해설.",
                 "X의 각 원소에 Y의 원소가 하나씩", "치역은 공역의 부분집합이에요.",
                 ["X의 각 원소에 Y의 원소가 오직 하나씩 대응하면 이 대응을 X에서 Y로의 <b>함수</b>라고 해요.",
                  "X를 정의역, Y를 공역, 함숫값 전체의 집합을 치역이라고 해요.",
                  "서로 다른 원소에 서로 다른 함숫값이 대응하면 일대일함수, 여기에 치역 = 공역이면 일대일대응이에요.",
                  "n(X) = m, n(Y) = n일 때 함수의 개수는 nᵐ, 일대일함수는 <sub>n</sub>P<sub>m</sub>개예요."],
                 [("X = {1, 2, 3}, f(x) = 2x − 1", ["f(1) = 1, f(2) = 3, f(3) = 5"], "치역 {1, 3, 5}"), ("n(X) = 2, n(Y) = 3", ["3²"], "함수 9개")],
                 [("함수의 개수를 mⁿ으로 센다", "공역의 원소 수를 지수만큼 곱해요: nᵐ"), ("치역과 공역을 같다고 생각한다", "치역은 공역의 부분집합이에요."), ("f(x) = x²을 일대일함수라고 한다", "f(1) = f(−1)이므로 아니에요.")],
                 [("그래프로 함수인지 어떻게 알아요?", "y축에 평행한 직선과 한 점에서만 만나면 함수의 그래프예요."), ("두 함수가 같다는 것은?", "정의역과 공역이 같고, 모든 x에서 함숫값이 같은 것이에요.")],
                 [("함숫값", [(f_main(("val",)), 12), (f_main(("eq",)), 8)]), ("치역", [(f_main(("range",)), 20)]), ("함수의 뜻", [(f_main(("isf",)), 8), (f_main(("kind",)), 10), (f_main(("val",)), 2)]),
                  ("함수의 개수", [(f_main(("count",)), 20)]), ("섞어서 연습", [(f_main(("val", "range", "count", "eq")), 20)])], 83112)
    U["comp"] = ("composite-and-inverse-functions", 13, "[10공수2-03-02] [10공수2-03-03]", "함수의 합성을 설명하고, 합성함수를 구할 수 있다. 역함수의 개념을 설명하고, 역함수를 구할 수 있다.",
                 "합성함수와 역함수", "합성함수와 역함수",
                 "고등학교 공통수학2 합성함수와 역함수 문제: (f ∘ g)(x)의 값과 식, f ∘ g와 g ∘ f의 차이, 일차함수의 역함수, f⁻¹(a)의 값, (f⁻¹ ∘ g)(a), 역함수 조건으로 미지수 구하기까지 100문제와 정답·해설.",
                 "(f ∘ g)(x) = f(g(x))", "f⁻¹(b) = a ⇔ f(a) = b",
                 ["(f ∘ g)(x) = f(g(x))는 먼저 g를, 다음에 f를 적용해요. 일반적으로 f ∘ g ≠ g ∘ f예요.",
                  "함수 f가 일대일대응일 때, f(a) = b이면 f<sup>−1</sup>(b) = a예요.",
                  "역함수는 y = f(x)를 x에 대하여 푼 뒤 x와 y를 바꾸어 구해요.",
                  "y = f(x)와 y = f<sup>−1</sup>(x)의 그래프는 직선 y = x에 대하여 대칭이에요."],
                 [("f(x) = 2x + 1, g(x) = x − 3, (f ∘ g)(5)", ["g(5) = 2", "f(2) = 5"], "5"), ("f(x) = 3x − 6의 역함수", ["x = (y + 6)/3"], "f⁻¹(x) = x/3 + 2")],
                 [("(f ∘ g)(x)를 g(f(x))로 계산한다", "안쪽 g부터 계산해요."), ("f⁻¹(x)를 1/f(x)로 생각한다", "역함수는 역수가 아니에요."), ("역함수를 구할 때 x, y를 바꾸지 않는다", "x에 대해 푼 뒤 x와 y를 바꿔요.")],
                 [("역함수가 존재할 조건은?", "일대일대응이어야 해요."), ("(f ∘ f⁻¹)(x)는?", "항등함수 x예요.")],
                 [("합성함수의 값", [(cp_main(("cval",)), 20)]), ("합성함수의 식", [(cp_main(("cexp",)), 20)]), ("역함수 구하기", [(cp_main(("inv",)), 20)]),
                  ("역함수의 값", [(cp_main(("invval",)), 12), (cp_main(("find",)), 8)]), ("합성함수와 역함수", [(cp_main(("mix",)), 20)])], 83113)
    U["rat"] = ("rational-functions", 14, "[10공수2-03-04]", "유리함수 y = (ax + b)/(cx + d)의 그래프를 그릴 수 있고, 그 그래프의 성질을 탐구할 수 있다.",
                "유리식과 유리함수의 그래프", "유리함수",
                "고등학교 공통수학2 유리함수 문제: 유리식의 계산, y = k/(x − p) + q의 점근선과 대칭의 중심, 정의역과 치역, 평행이동, 그래프를 보고 식 구하기, 함숫값까지 100문제와 정답·해설.",
                "점근선은 x = p, y = q", "그래프는 점 (p, q)에 대하여 대칭이에요.",
                ["분모에 문자가 있는 식을 유리식이라 하고, 분수처럼 약분·통분해서 계산해요.",
                 "y = k/(x − p) + q는 y = k/x를 x축 방향으로 p, y축 방향으로 q만큼 평행이동한 그래프예요.",
                 "점근선은 x = p, y = q이고, 정의역은 x ≠ p, 치역은 y ≠ q인 실수 전체예요.",
                 "y = (ax + b)/(cx + d)는 분자를 분모로 나누어 y = k/(x − p) + q 꼴로 고쳐요."],
                [("y = (2x + 1)/(x − 1)", ["2 + 3/(x − 1)"], "점근선 x = 1, y = 2"), ("1/(x − 1) + 1/(x + 1)", ["(x + 1 + x − 1)/(x² − 1)"], "2x/(x² − 1)")],
                [("점근선을 x = −p로 읽는다", "x − p = 0이 되는 x = p예요."), ("정의역에서 점근선 값을 포함한다", "분모가 0이 되는 값은 제외해요."), ("평행이동에서 x + p를 넣는다", "x 대신 x − p를 넣어요.")],
                [("k의 부호는 무엇을 정하나요?", "k &gt; 0이면 그래프가 제1·3사분면 쪽, k &lt; 0이면 제2·4사분면 쪽에 있어요."), ("다항함수도 유리함수인가요?", "네, 분모가 상수인 유리함수예요.")],
                [("유리식의 계산", [(ra_main(("expr",)), 12), (ra_main(("val",)), 8)]), ("점근선", [(ra_main(("asym",)), 20)]), ("대칭의 중심과 정의역·치역", [(ra_main(("center", "dom")), 20)]),
                 ("평행이동", [(ra_main(("trans",)), 20)]), ("그래프와 함숫값", [(ra_main(("graph",)), 12), (ra_main(("val",)), 8)])], 83114)
    U["irr"] = ("irrational-functions", 15, "[10공수2-03-05]", "무리함수 y = √(ax + b) + c의 그래프를 그릴 수 있고, 그 그래프의 성질을 탐구할 수 있다.",
                "무리식과 무리함수의 그래프", "무리함수",
                "고등학교 공통수학2 무리함수 문제: 무리식이 실수가 될 조건, 분모의 유리화, y = √(a(x − p)) + q의 정의역과 치역, 시작점, 평행이동, 그래프를 보고 식 구하기까지 100문제와 정답·해설.",
                "근호 안은 0 이상", "y = √(a(x − p)) + q는 점 (p, q)에서 시작해요.",
                ["근호 안에 문자가 있는 식을 무리식이라 하고, 근호 안이 0 이상일 때 실수가 돼요.",
                 "y = √(a(x − p)) + q는 y = √(ax)를 x축 방향으로 p, y축 방향으로 q만큼 평행이동한 그래프예요.",
                 "a &gt; 0이면 정의역은 x ≥ p, a &lt; 0이면 x ≤ p예요.",
                 "√ 앞이 +이면 치역은 y ≥ q, −이면 y ≤ q예요."],
                [("y = √(2x − 4) + 1", ["2x − 4 ≥ 0"], "정의역 x ≥ 2, 치역 y ≥ 1"), ("1/(√3 + √2)", ["(√3 − √2)/(3 − 2)"], "√3 − √2")],
                [("a &lt; 0인데 정의역을 x ≥ p로 쓴다", "근호 안 a(x − p) ≥ 0에서 부등호 방향이 바뀌어요."), ("치역을 정의역과 같게 쓴다", "치역은 y의 범위로 q에서 시작해요."), ("유리화에서 분모만 곱한다", "분모와 분자에 같은 식을 곱해요.")],
                [("무리함수의 그래프 모양은?", "포물선의 절반 모양이에요."), ("y = √x와 y = x²의 관계는?", "x ≥ 0에서 y = x²의 역함수가 y = √x예요.")],
                [("무리식", [(ir_main(("real", "rat")), 20)]), ("정의역과 치역", [(ir_main(("dom", "rng")), 20)]), ("시작점과 함숫값", [(ir_main(("start", "val")), 20)]),
                 ("평행이동", [(ir_main(("trans",)), 20)]), ("그래프 읽기", [(ir_main(("graph",)), 14), (ir_main(("dom", "rng")), 6)])], 83115)
    t = U[which]
    slug, sort, code, std, title, short, meta, kb, ks, think, ex, mist, faq, spec, seed = t
    return unit(G, slug, sort, code, std, title, short, meta, kb, ks, think, ex, mist, faq, spec, seed)
