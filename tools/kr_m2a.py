# -*- coding: utf-8 -*-
"""
대한민국 중학교 2학년 수학（2022 개정）：수와 연산・변화와 관계の 9 単元
  repdec : 유리수와 순환소수 [9수01-06]
  expo   : 지수법칙과 단항식의 계산 [9수02-08] [9수02-10]
  poly   : 다항식의 계산 [9수02-09] [9수02-10]
  ineq   : 일차부등식 [9수02-11] [9수02-12]
  sys    : 연립일차방정식 [9수02-13]
  sysw   : 연립일차방정식의 활용 [9수02-13]
  lf     : 일차함수와 그 그래프 [9수02-14] [9수02-15]
  lfg    : 일차함수의 그래프의 성질과 식 [9수02-16]
  lfe    : 일차함수와 일차방정식의 관계 [9수02-17] [9수02-18]
誤答は「유한소수를 분모의 소인수가 아니라 분자로 판단한다」「aᵐ × aⁿ = aᵐⁿ」「괄호 앞 − 를 뒤의 항에 곱하지 않는다」
「음수로 나눌 때 부등호의 방향을 바꾸지 않는다」「가감법에서 부호를 잘못 맞춘다」「기울기를 y의 변화량 ÷ x의 변화량이 아니라 거꾸로 한다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_common import josa, Names, num, fr
from kr_mid import M, N, neg, par, sg, dec, P, sup, unit, kosy, fig, svg_wrap, text, line, INK, RED, BLUE, GREEN

R = random.Random(82801)
NM = Names(R)
G = "grade-8"
DOT = "̇"


def svgf(W, H, body, label):
    return fig(svg_wrap(int(W), int(H), body, label).replace("<svg ", "<svg data-pf='lg' ", 1))


# ------------------------------------------------------------------ 순환소수
def rdot(cyc):
    if len(cyc) == 1:
        return cyc + DOT
    return cyc[0] + DOT + cyc[1:-1] + cyc[-1] + DOT


def rdec(ip, pre, cyc):
    """순환소수 표기：0.1̇2̇"""
    return "%s.%s%s" % (ip, pre, rdot(cyc))


def rlong(ip, pre, cyc, k=3):
    return "%s.%s%s…" % (ip, pre, cyc * k)


def rval(ip, pre, cyc):
    a = int(str(ip) + pre + cyc)
    b = int(str(ip) + pre)
    return Fr(a - b, 10 ** len(pre) * (10 ** len(cyc) - 1))


def to_rep(f):
    """분수 → (정수부, 비순환, 순환마디) 또는 유한소수면 (정수부, 소수부, '')"""
    f = Fr(f)
    ip = f.numerator // f.denominator
    r = f.numerator % f.denominator
    d = f.denominator
    seen = {}
    digs = ""
    while r and r not in seen:
        seen[r] = len(digs)
        r *= 10
        digs += str(r // d)
        r %= d
    if not r:
        return ip, digs, ""
    i = seen[r]
    return ip, digs[:i], digs[i:]


def finite(f):
    d = Fr(f).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def fstr(f):
    f = Fr(f)
    return neg(f)


def rd_notation():
    def mk():
        ip = R.choice([0, 0, 1, 2, 3])
        pre = R.choice(["", "", "", str(R.randint(1, 9))])
        L = R.choice([1, 2, 2, 3])
        cyc = "".join(str(R.randint(0, 9)) for _ in range(L))
        if len(set(cyc)) == 1 and L > 1 or cyc == "0" or cyc == "9" or (pre and pre[-1] == cyc[-1]):
            return None
        how = R.choice(["write", "cycle", "nth"])
        if how == "write":
            ok = rdec(ip, pre, cyc)
            w = [rdec(ip, pre, cyc + cyc[0]) if L < 3 else rdec(ip, pre, cyc[:2]), "%s.%s%s" % (ip, pre, cyc[0] + DOT + cyc[1:]) if L > 1 else rdec(ip, "", pre + cyc) if pre else None,
                 rdec(ip, "", (pre + cyc)) if pre else "%s.%s" % (ip, "".join(c + DOT for c in cyc)), "%s.%s%s" % (ip, pre, "".join(c + DOT for c in cyc))]
            return M("순환소수 <b>%s</b>를 순환마디에 점을 찍어 나타내면?" % rlong(ip, pre, cyc), ok, w, "순환마디는 %s이에요. 순환마디의 처음과 끝 숫자 위에 점을 찍어요. <b>%s</b>" % (cyc, ok))
        if how == "cycle":
            w = [cyc + cyc[0], pre + cyc if pre else cyc[::-1] if L > 1 else cyc + cyc, cyc[0] if L > 1 else cyc * 3, str(ip) + cyc]
            return M("순환소수 <b>%s</b>의 순환마디는?" % rlong(ip, pre, cyc), cyc, w, "되풀이되는 가장 짧은 부분이에요. <b>%s</b>" % cyc)
        if pre:
            return None
        n = R.choice([10, 20, 25, 30, 50, 100])
        d = cyc[(n - 1) % L]
        return N("순환소수 <b>%s</b>의 소수점 아래 %d번째 자리의 숫자는?" % (rdec(ip, "", cyc), n), int(d), [int(c) for c in cyc if c != d] + [int(cyc[n % L]), n % 10, (int(d) + 1) % 10],
                 "순환마디가 %d자리이므로 %d ÷ %d의 나머지 %d번째 숫자예요. <b>%s</b>" % (L, n, L, (n - 1) % L + 1, d))
    return mk


def rd_finite(kinds=tuple(["which", "which_not", "make"])):
    def mk():
        how = R.choice(kinds)
        if how == "make":
            p = R.choice([3, 7, 11, 13])
            d = p * R.choice([2, 4, 5, 8, 10, 20])
            a = R.randint(1, d - 1)
            if math.gcd(a, d) != 1:
                return None
            return N("<b>%s × a</b>가 유한소수가 되도록 하는 가장 작은 자연수 a는?" % fr(a, d), p, [d // p, d, 2, p * 2, 10],
                     "분모 %d = %d × %d에서 %d을 없애야 해요. <b>%d</b>" % (d, d // p, p, p, p))
        good, bad = [], []
        while len(good) < 4 or len(bad) < 4:
            dd = R.choice([6, 7, 8, 12, 14, 15, 16, 18, 20, 24, 25, 28, 30, 35, 40, 45, 50, 60, 75, 80])
            a = R.randint(1, dd * 2)
            f = Fr(a, dd)
            if f.denominator == 1 or a % dd == 0:
                continue
            s = fr(a, dd)
            (good if finite(f) else bad).append((s, f))
        if how == "which":
            ok, f = good[0]
            wr = [b[0] for b in bad[:3]]
            return M("다음 중 <b>유한소수</b>로 나타낼 수 있는 것은?", ok, wr, "기약분수로 고치면 %s이고 분모의 소인수가 2나 5뿐이에요. <b>%s</b>" % (fstr(f), ok))
        ok, f = bad[0]
        wr = [g[0] for g in good[:3]]
        return M("다음 중 유한소수로 나타낼 수 <b>없는</b> 것은?", ok, wr, "기약분수로 고치면 %s이고 분모에 2, 5 이외의 소인수가 있어요. <b>%s</b>" % (fstr(f), ok))
    return mk


def rd_tofrac():
    def mk():
        ip = R.choice([0, 0, 1, 2])
        pre = R.choice(["", "", str(R.randint(1, 9))])
        L = R.choice([1, 1, 2])
        cyc = "".join(str(R.randint(0, 9)) for _ in range(L))
        if cyc in ("0", "9", "00", "99") or (L == 2 and cyc[0] == cyc[1]) or (pre and pre[-1] == cyc[-1]):
            return None
        v = rval(ip, pre, cyc)
        a = int(str(ip) + pre + cyc)
        b = int(str(ip) + pre)
        den = 10 ** len(pre) * (10 ** L - 1)
        w = [Fr(a, den), Fr(a - b, 10 ** (len(pre) + L)), Fr(int(cyc), 10 ** L - 1) + ip, Fr(a, 10 ** (len(pre) + L)), Fr(a - b, den - 1 if den > 9 else 10)]
        return N("순환소수 <b>%s</b>를 기약분수로 나타내면?" % rdec(ip, pre, cyc), v, w,
                 "(%d − %d) ÷ %d = %s. <b>%s</b>" % (a, b, den, fr(a - b, den), fstr(v)))
    return mk


def rd_class():
    F = [("순환소수는 모두 유리수예요.", True), ("모든 유한소수는 유리수예요.", True), ("정수가 아닌 유리수는 유한소수 또는 순환소수로 나타낼 수 있어요.", True),
         ("무한소수는 모두 유리수예요.", False), ("순환소수 중에는 분수로 나타낼 수 없는 것도 있어요.", False), ("기약분수의 분모에 3이 있으면 유한소수예요.", False),
         ("0.9̇는 1과 같아요.", True), ("유리수 중에는 순환하지 않는 무한소수도 있어요.", False), ("분모의 소인수가 2나 5뿐인 기약분수는 유한소수로 나타낼 수 있어요.", True)]

    def mk():
        if R.random() < 0.5:
            t = [x for x, ok in F if ok]
            f = [x for x, ok in F if not ok]
            ok = R.choice(t)
            return M("다음 중 옳은 것은?", ok, R.sample(f, 3), "<b>%s</b>" % ok)
        t = [x for x, ok in F if ok]
        f = [x for x, ok in F if not ok]
        ok = R.choice(f)
        return M("다음 중 옳지 <b>않은</b> 것은?", ok, R.sample(t, 3), "<b>%s</b> — 이 설명은 틀렸어요." % ok)
    return mk


def rd_frac2dec():
    def mk():
        d = R.choice([3, 6, 7, 9, 11, 12, 15, 22, 27, 33, 37])
        a = R.randint(1, d - 1)
        if math.gcd(a, d) != 1:
            return None
        ip, pre, cyc = to_rep(Fr(a, d))
        if not cyc or len(cyc) > 3:
            return None
        ok = rdec(ip, pre, cyc)
        w = []
        if len(cyc) > 1:
            w.append(rdec(ip, pre, cyc[:-1]))
            w.append(rdec(ip, pre, cyc[1:] + cyc[0]))
        w.append(rdec(ip, "", pre + cyc) if pre else rdec(ip, cyc[0], cyc[1:] + cyc[0]) if len(cyc) > 1 else rdec(ip, cyc, cyc + "1"))
        w.append("%s.%s%s" % (ip, pre, cyc))
        w.append(rdec(ip, pre, str((int(cyc[0]) + 1) % 10) + cyc[1:]))
        return M("분수 <b>%s</b>를 순환소수로 나타내면?" % fr(a, d), ok, w, "%d ÷ %d = %s → <b>%s</b>" % (a, d, rlong(ip, pre, cyc, 2), ok))
    return mk


# ------------------------------------------------------------------ 지수법칙과 단항식
V = ["a", "b", "x", "y"]


def pw(v, e):
    if e == 0:
        return ""
    return v + ("" if e == 1 else sup(e))


def mono(c, ex):
    """c, {'x':2,'y':1} → 6x²y"""
    c = Fr(c)
    body = "".join(pw(v, ex[v]) for v in sorted(ex) if ex[v])
    if not body:
        return neg(c)
    if c == 1:
        return body
    if c == -1:
        return "−" + body
    return neg(c) + body


def e_law(kinds=tuple(["mul", "pow", "div", "div2", "prod"])):
    def mk():
        v = R.choice(V)
        m, n = R.randint(2, 7), R.randint(2, 6)
        how = R.choice(kinds)
        if how == "mul":
            return M("<b>%s × %s</b>를 간단히 하면?" % (pw(v, m), pw(v, n)), pw(v, m + n), [pw(v, m * n), pw(v, m + n + 1), "%d%s" % (2, pw(v, m + n)), pw(v, abs(m - n) or 1)],
                     "밑이 같으면 지수끼리 더해요. %d + %d = %d. <b>%s</b>" % (m, n, m + n, pw(v, m + n)))
        if how == "pow":
            return M("<b>(%s)%s</b>을 간단히 하면?" % (pw(v, m), sup(n)), pw(v, m * n), [pw(v, m + n), pw(v, m ** n) if m ** n < 100 else pw(v, m * n + 1), "%d%s" % (n, pw(v, m)), pw(v, m * n - 1)],
                     "거듭제곱의 거듭제곱은 지수끼리 곱해요. %d × %d = %d. <b>%s</b>" % (m, n, m * n, pw(v, m * n)))
        if how == "div":
            a, b = max(m, n) + R.randint(1, 3), min(m, n)
            return M("<b>%s ÷ %s</b>을 간단히 하면?" % (pw(v, a), pw(v, b)), pw(v, a - b), [pw(v, a + b), pw(v, a // b) if a % b == 0 and a // b != a - b else pw(v, a - b + 1), "1", "1/" + pw(v, a - b)],
                     "지수끼리 빼요. %d − %d = %d. <b>%s</b>" % (a, b, a - b, pw(v, a - b)))
        if how == "div2":
            a, b = min(m, n), max(m, n) + R.randint(1, 3)
            ok = "1/" + pw(v, b - a)
            return M("<b>%s ÷ %s</b>을 간단히 하면?" % (pw(v, a), pw(v, b)), fr(1, pw(v, b - a)), [pw(v, b - a), fr(1, pw(v, b + a)), "1", "−" + pw(v, b - a)],
                     "나누는 쪽의 지수가 더 크면 1/%s이 돼요. <b>%s</b>" % (pw(v, b - a), ok))
        u = R.choice([x for x in V if x != v])
        c = R.randint(2, 3)
        return M("<b>(%d%s%s)%s</b>을 간단히 하면?" % (c, pw(v, m), u, sup(n)) if n <= 4 else "<b>(%d%s%s)³</b>을 간단히 하면?" % (c, pw(v, m), u),
                 mono(c ** min(n, 3) if n > 4 else c ** n, {v: m * (n if n <= 4 else 3), u: n if n <= 4 else 3}),
                 [mono(c * (n if n <= 4 else 3), {v: m * (n if n <= 4 else 3), u: n if n <= 4 else 3}), mono(c ** (n if n <= 4 else 3), {v: m + (n if n <= 4 else 3), u: n if n <= 4 else 3}),
                  mono(c, {v: m * (n if n <= 4 else 3), u: n if n <= 4 else 3}), mono(c ** (n if n <= 4 else 3), {v: m * (n if n <= 4 else 3), u: 1})],
                 "괄호 안의 각 인수를 모두 거듭제곱해요. <b>%s</b>" % mono(c ** (n if n <= 4 else 3), {v: m * (n if n <= 4 else 3), u: n if n <= 4 else 3}))
    return mk


def e_box():
    def mk():
        how = R.choice(["mul", "pow", "num"])
        v = R.choice(V)
        if how == "mul":
            m, k = R.randint(2, 6), R.randint(2, 6)
            return N("<b>%s × %s<sup>□</sup> = %s</b>일 때, □ 안에 알맞은 수는?" % (pw(v, m), v, pw(v, m + k)), k, [m + k, m * k, k + 1, (m + k) // m if (m + k) % m == 0 else k - 1],
                     "%d + □ = %d. <b>%d</b>" % (m, m + k, k))
        if how == "pow":
            m, k = R.randint(2, 5), R.randint(2, 5)
            return N("<b>(%s<sup>□</sup>)%s = %s</b>일 때, □ 안에 알맞은 수는?" % (v, sup(k), pw(v, m * k)), m, [m * k - k, m * k, m + 1, k],
                     "□ × %d = %d. <b>%d</b>" % (k, m * k, m))
        b = R.choice([2, 3, 5])
        p, q = R.randint(2, 5), R.randint(2, 4)
        n = p * q
        bb = b ** p
        if bb > 300:
            return None
        return N("<b>%d%s = %d<sup>□</sup></b>일 때, □ 안에 알맞은 수는?" % (bb, sup(q), b, ), n, [p + q, q, bb * q if bb * q < 100 else n + 1, n - 1],
                 "%d = %d%s이므로 (%d%s)%s = %d%s. <b>%d</b>" % (bb, b, sup(p), b, sup(p), sup(q), b, sup(n), n))
    return mk


def mono_rand(vs=("x", "y")):
    c = R.choice([-6, -4, -3, -2, 2, 3, 4, 5, 6])
    ex = {v: R.randint(0, 3) for v in vs}
    if not any(ex.values()):
        ex[vs[0]] = 1
    return c, ex


def e_mono(kinds=tuple(["mul", "div", "mix"])):
    def mk():
        how = R.choice(kinds)
        vs = R.choice([("a", "b"), ("x", "y")])
        c1, e1 = mono_rand(vs)
        c2, e2 = mono_rand(vs)
        if how == "mul":
            ok = mono(c1 * c2, {v: e1[v] + e2[v] for v in vs})
            w = [mono(c1 + c2, {v: e1[v] + e2[v] for v in vs}), mono(c1 * c2, {v: e1[v] * e2[v] for v in vs}), mono(-c1 * c2, {v: e1[v] + e2[v] for v in vs}),
                 mono(c1 * c2, {v: e1[v] + e2[v] + 1 for v in vs})]
            return M("<b>%s × %s</b>를 계산하면?" % (par_m(c1, e1), par_m(c2, e2)), ok, w, "계수끼리, 문자끼리 곱해요. <b>%s</b>" % ok)
        if how == "div":
            q = Fr(c1 * c2, c2)
            big = {v: e1[v] + e2[v] for v in vs}
            ok = mono(c1, e1)
            w = [mono(c1 * c2 * c2, {v: big[v] + e2[v] for v in vs}), mono(-c1, e1), mono(c1, {v: big[v] for v in vs}), mono(c1 * c2 - c2, e1)]
            return M("<b>%s ÷ %s</b>를 계산하면?" % (par_m(c1 * c2, big), par_m(c2, e2)), ok, w, "계수끼리 나누고, 문자는 지수끼리 빼요. <b>%s</b>" % ok)
        c3, e3 = mono_rand(vs)
        if c1 * c2 % c3:
            return None
        ex = {v: e1[v] + e2[v] - e3[v] for v in vs}
        if min(ex.values()) < 0:
            return None
        ok = mono(Fr(c1 * c2, c3), ex)
        w = [mono(Fr(c1 * c2, c3), {v: e1[v] + e2[v] + e3[v] for v in vs}), mono(-Fr(c1 * c2, c3), ex), mono(c1 * c2 * c3, ex), mono(Fr(c1 * c2, c3), {v: e1[v] * e2[v] for v in vs})]
        return M("<b>%s × %s ÷ %s</b>를 계산하면?" % (par_m(c1, e1), par_m(c2, e2), par_m(c3, e3)), ok, w, "나눗셈은 역수의 곱셈으로 바꾸어 앞에서부터 계산해요. <b>%s</b>" % ok)
    return mk


def par_m(c, ex):
    s = mono(c, ex)
    return "(%s)" % s if c < 0 else s


def e_word():
    def mk():
        how = R.choice(["area", "vol", "digits"])
        if how == "area":
            a, b = R.randint(2, 5), R.randint(2, 5)
            p, q = R.randint(1, 3), R.randint(1, 3)
            return M("가로의 길이가 %s, 세로의 길이가 %s인 직사각형의 넓이는?" % (mono(a, {"a": p}), mono(b, {"b": q})), mono(a * b, {"a": p, "b": q}),
                     [mono(a + b, {"a": p, "b": q}), mono(2 * (a + b), {"a": p, "b": q}), mono(a * b, {"a": p + 1, "b": q})], "(가로) × (세로) = <b>%s</b>" % mono(a * b, {"a": p, "b": q}))
        if how == "vol":
            a = R.randint(2, 4)
            p = R.randint(1, 3)
            return M("한 모서리의 길이가 %s인 정육면체의 부피는?" % mono(a, {"x": p}), mono(a ** 3, {"x": 3 * p}), [mono(3 * a, {"x": 3 * p}), mono(a ** 3, {"x": p + 3}), mono(6 * a * a, {"x": 2 * p})],
                     "(%s)³ = <b>%s</b>" % (mono(a, {"x": p}), mono(a ** 3, {"x": 3 * p})))
        n = R.randint(3, 6)
        k = R.choice([2, 4, 8])
        e = {2: (1, "2"), 4: (2, "2²"), 8: (3, "2³")}[k]
        m = R.randint(2, 5)
        digits = len(str(2 ** (e[0] * m) * 5 ** (e[0] * m)))
        tot = e[0] * m
        return N("<b>%d%s × 5%s</b>은 몇 자리 자연수일까요?" % (k, sup(m), sup(tot)), tot + 1, [tot, tot + 2, m + 1, e[0] + m], "%d%s = 2%s이므로 (2 × 5)%s = 10%s. <b>%d자리</b>" % (k, sup(m), sup(tot), sup(tot), sup(tot), tot + 1),
                 f=lambda x: "%s자리" % neg(x))
    return mk


# ------------------------------------------------------------------ 다항식
def poly2(d, vs=("x", "y")):
    """{(ex, ey): c} → '3x² − 2xy + y − 5'"""
    items = sorted([(k, Fr(c)) for k, c in d.items() if c], key=lambda t: (-(t[0][0] + t[0][1]), -t[0][0]))
    if not items:
        return "0"
    out = []
    for (a, b), c in items:
        body = pw(vs[0], a) + pw(vs[1], b)
        ac = abs(c)
        if body:
            cs = "" if ac == 1 else (num(ac.numerator) if ac.denominator == 1 else fr(ac.numerator, ac.denominator))
            t = cs + body
        else:
            t = neg(ac)
        if not out:
            out.append(("−" if c < 0 else "") + t)
        else:
            out.append((" − " if c < 0 else " + ") + t)
    return "".join(out)


def padd(a, b, k=1):
    out = dict(a)
    for t, c in b.items():
        out[t] = out.get(t, 0) + k * c
    return {t: c for t, c in out.items() if c}


def pmul(a, b):
    out = {}
    for (p, q), c in a.items():
        for (r, s), d in b.items():
            out[(p + r, q + s)] = out.get((p + r, q + s), 0) + c * d
    return {t: c for t, c in out.items() if c}


def rp(terms, deg=1):
    """임의의 다항식"""
    pool = [(1, 0), (0, 1), (0, 0)] if deg == 1 else [(2, 0), (1, 0), (0, 0)]
    d = {}
    for t in pool[:terms]:
        d[t] = R.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
    return d


def p_addsub():
    def mk():
        deg = R.choice([1, 1, 2])
        A, B = rp(3, deg), rp(3, deg)
        op = R.choice(["+", "−"])
        k = 1 if op == "+" else -1
        ok = poly2(padd(A, B, k))
        w = [poly2(padd(A, B, -k)), poly2({t: (A.get(t, 0) - B.get(t, 0) if t == list(B)[0] else A.get(t, 0) + B.get(t, 0)) for t in set(A) | set(B)}) if k == -1 else poly2(padd(A, {t: -c for t, c in B.items()}, 1)),
             poly2({t: c for t, c in padd(A, B, k).items() if t != (0, 0)}), poly2(padd(A, B, 2 * k))]
        a2 = R.randint(2, 3)
        if R.random() < 0.4:
            ok = poly2(padd({t: a2 * c for t, c in A.items()}, B, k))
            w = [poly2(padd({t: a2 * c if t == list(A)[0] else c for t, c in A.items()}, B, k)), poly2(padd({t: a2 * c for t, c in A.items()}, B, -k)),
                 poly2(padd(A, B, k)), poly2(padd({t: a2 * c for t, c in A.items()}, {t: a2 * c for t, c in B.items()}, k))]
            return M("<b>%d(%s) %s (%s)</b>를 계산하면?" % (a2, poly2(A), op, poly2(B)), ok, w, "괄호를 풀고 동류항끼리 계산해요. <b>%s</b>" % ok)
        return M("<b>(%s) %s (%s)</b>를 계산하면?" % (poly2(A), op, poly2(B)), ok, w, "%s동류항끼리 계산해요. <b>%s</b>" % ("괄호 앞이 −이면 괄호 안의 모든 항의 부호를 바꾸고, " if k == -1 else "", ok))
    return mk


def p_muldiv(kinds=tuple(["mul", "div", "mul2"])):
    def mk():
        how = R.choice(kinds)
        c = R.choice([-4, -3, -2, 2, 3, 4, 5])
        m = {(1, 0): c} if R.random() < 0.5 else {(0, 1): c}
        A = rp(3)
        if how in ("mul", "mul2"):
            ok = poly2(pmul(m, A))
            w = [poly2(padd(pmul(m, {list(A)[0]: A[list(A)[0]]}), {t: v for t, v in A.items() if t != list(A)[0]})), poly2(pmul({k: -v for k, v in m.items()}, A)),
                 poly2(pmul({(0, 0): c}, A)), poly2({t: v * c for t, v in A.items()})]
            if how == "mul2":
                B = rp(2)
                ok = poly2(padd(pmul(m, A), B))
                w = [poly2(padd(pmul(m, A), B, -1)), poly2(padd(pmul({(0, 0): c}, A), B)), poly2(pmul(m, padd(A, B))), poly2(padd(pmul({k: -v for k, v in m.items()}, A), B))]
                return M("<b>%s(%s) + %s</b>를 간단히 하면?" % (poly2(m), poly2(A), poly2(B).replace(" + ", " + ") if not poly2(B).startswith("−") else "(%s)" % poly2(B)), ok, w,
                         "분배법칙으로 전개한 뒤 동류항끼리 계산해요. <b>%s</b>" % ok)
            return M("<b>%s(%s)</b>를 전개하면?" % (poly2(m) if c > 0 else "(%s)" % poly2(m), poly2(A)), ok, w, "단항식을 다항식의 각 항에 곱해요. <b>%s</b>" % ok)
        big = pmul(m, A)
        ok = poly2(A)
        w = [poly2({t: v for t, v in A.items() if t != (0, 0)}) + (" + 1" if (0, 0) in A else ""), poly2({k: -v for k, v in A.items()}), poly2(pmul(m, big)) if False else poly2(padd(A, {(0, 0): 1})),
             poly2({t: v * c for t, v in A.items()})]
        return M("<b>(%s) ÷ %s</b>를 계산하면?" % (poly2(big), poly2(m) if c > 0 else "(%s)" % poly2(m)), ok, w, "각 항을 %s로 나누어요. <b>%s</b>" % (poly2(m), ok))
    return mk


def p_value():
    def mk():
        x, y = R.choice([-3, -2, -1, 1, 2, 3, 4]), R.choice([-3, -2, -1, 1, 2, 3])
        A = rp(3)
        A[(1, 1)] = R.choice([-2, 1, 2]) if R.random() < 0.4 else 0
        A = {t: c for t, c in A.items() if c}
        v = sum(c * x ** a * y ** b for (a, b), c in A.items())
        w = [sum(c * y ** a * x ** b for (a, b), c in A.items()), sum(c * abs(x) ** a * abs(y) ** b for (a, b), c in A.items()), v + 2, v - 2]
        return N("x = %s, y = %s일 때, <b>%s</b>의 값은?" % (neg(x), neg(y), poly2(A)), v, w, "음수는 괄호를 써서 대입해요. <b>%s</b>" % neg(v))
    return mk


def p_solvefor():
    def mk():
        a, b, c = R.choice([2, 3, 4, 5, -2, -3]), R.choice([1, 2, 3, -1]), R.randint(1, 9)
        how = R.choice(["y", "x", "sub"])
        if how == "y":
            # ax + by = c → y = (c − ax)/b
            ok = "y = " + poly2({(1, 0): Fr(-a, b), (0, 0): Fr(c, b)})
            w = ["y = " + poly2({(1, 0): Fr(a, b), (0, 0): Fr(c, b)}), "y = " + poly2({(1, 0): Fr(-a, b), (0, 0): Fr(-c, b)}), "y = " + poly2({(1, 0): -a, (0, 0): c}) if b != 1 else "y = " + poly2({(1, 0): a, (0, 0): -c}),
                 "y = " + poly2({(1, 0): Fr(-b, a), (0, 0): Fr(c, a)})]
            return M("<b>%s = %d</b>를 y에 대하여 풀면?" % (poly2({(1, 0): a, (0, 1): b}), c), ok, w, "x항을 이항하고 양변을 %s로 나누어요. <b>%s</b>" % (neg(b), ok))
        if how == "x":
            k = R.choice([2, 3, 4])
            ok = "x = " + poly2({(0, 1): Fr(1, k), (0, 0): Fr(-c, k)})
            w = ["x = " + poly2({(0, 1): k, (0, 0): -c}), "x = " + poly2({(0, 1): Fr(1, k), (0, 0): Fr(c, k)}), "x = " + poly2({(0, 1): Fr(1, k), (0, 0): -c}), "x = " + poly2({(0, 1): k, (0, 0): c})]
            return M("<b>y = %dx + %d</b>를 x에 대하여 풀면?" % (k, c), ok, w, "y − %d = %dx → x = (y − %d) ÷ %d. <b>%s</b>" % (c, k, c, k, ok))
        p, q = R.randint(1, 4), R.randint(1, 4)
        # y = px + q 를 ax + by 에 대입
        A = {(1, 0): a + b * p, (0, 0): b * q}
        ok = poly2(A)
        w = [poly2({(1, 0): a + p, (0, 0): q}), poly2({(1, 0): a + b * p, (0, 0): q}), poly2({(1, 0): a - b * p, (0, 0): -b * q}), poly2({(1, 0): a * b * p, (0, 0): b * q})]
        return M("y = %s일 때, <b>%s</b>를 x에 대한 식으로 나타내면?" % (poly2({(1, 0): p, (0, 0): q}), poly2({(1, 0): a, (0, 1): b})), ok, w,
                 "y 자리에 (%s)를 넣고 정리해요. <b>%s</b>" % (poly2({(1, 0): p, (0, 0): q}), ok))
    return mk


# ------------------------------------------------------------------ 일차부등식
OPS = {"<": "&lt;", ">": "&gt;", "≤": "≤", "≥": "≥"}
FLIP = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}


def ineq_line(k, op):
    W, H = 360, 80
    u = 28
    X = lambda v: 180 + (v - k) * u
    s = [line(20, 46, W - 20, 46, INK, 2)]
    for v in range(k - 5, k + 6):
        s.append(line(X(v), 40, X(v), 52, INK, 1.5) + text(X(v), 72, neg(v), 13, weight=500))
    right = op in (">", "≥")
    s.append(line(X(k), 26, X(k), 46, BLUE, 2.5))
    s.append(line(X(k), 26, (W - 24) if right else 24, 26, BLUE, 2.5))
    s.append("<polygon points='%s' fill='%s'/>" % (("%d,20 %d,26 %d,32" % (W - 24, W - 14, W - 24)) if right else ("24,20 14,26 24,32"), BLUE))
    closed = op in ("≤", "≥")
    s.append("<circle cx='%.1f' cy='46' r='6' fill='%s' stroke='%s' stroke-width='2.5'/>" % (X(k), BLUE if closed else "#ffffff", BLUE))
    return svgf(W, H, "".join(s), "부등식의 해를 나타낸 수직선")


def i_prop():
    def mk():
        a, b = R.randint(-9, 9), R.randint(-9, 9)
        if a == b:
            return None
        lt = "&lt;" if a < b else "&gt;"
        k = R.choice([-4, -3, -2, 2, 3, 4])
        c = R.randint(1, 9)
        how = R.choice(["mul", "add", "lin"])
        if how == "mul":
            okop = lt if k > 0 else ("&gt;" if lt == "&lt;" else "&lt;")
            bad = "&gt;" if okop == "&lt;" else "&lt;"
            return M("a %s b일 때, %sa □ %sb의 □ 안에 알맞은 부등호는?" % (lt, neg(k), neg(k)), okop, [bad, "=", "≥" if okop == "&lt;" else "≤"],
                     "%s를 곱하면 부등호의 방향이 %s. <b>%s</b>" % (neg(k), "그대로예요" if k > 0 else "바뀌어요", okop))
        if how == "add":
            return M("a %s b일 때, a − %d □ b − %d의 □ 안에 알맞은 부등호는?" % (lt, c, c), lt, ["&gt;" if lt == "&lt;" else "&lt;", "=", "≥" if lt == "&lt;" else "≤"],
                     "양변에서 같은 수를 빼도 부등호의 방향은 그대로예요. <b>%s</b>" % lt)
        okop = lt if k > 0 else ("&gt;" if lt == "&lt;" else "&lt;")
        bad = "&gt;" if okop == "&lt;" else "&lt;"
        return M("a %s b일 때, %s □ %s의 □ 안에 알맞은 부등호는?" % (lt, poly2({(1, 0): k, (0, 0): c}, ("a", "_")), poly2({(1, 0): k, (0, 0): c}, ("b", "_"))), okop, [bad, "=", "≥" if okop == "&lt;" else "≤"],
                 "%s를 곱한 뒤 %d를 더해요. <b>%s</b>" % (neg(k), c, okop))
    return mk


def solve_ineq():
    # ax + b op cx + d, 해 x op' k
    k = R.randint(-6, 6)
    a = R.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6])
    cc = R.choice([-3, -2, -1, 0, 1, 2, 3])
    if a == cc:
        return None
    b = R.randint(-9, 9)
    d = (a - cc) * k + b
    op = R.choice(["<", ">", "≤", "≥"])
    lhs = poly2({(1, 0): a, (0, 0): b})
    rhs = poly2({(1, 0): cc, (0, 0): d})
    res = op if a - cc > 0 else FLIP[op]
    return lhs, rhs, op, k, res, a - cc


def i_solve():
    def mk():
        t = solve_ineq()
        if not t:
            return None
        lhs, rhs, op, k, res, co = t
        ok = "x %s %s" % (OPS[res], neg(k))
        w = ["x %s %s" % (OPS[FLIP[res]], neg(k)), "x %s %s" % (OPS[res], neg(-k)), "x %s %s" % (OPS[res.replace("≤", "<").replace("≥", ">") if "=" not in res and res in "≤≥" else {"<": "≤", ">": "≥", "≤": "<", "≥": ">"}[res]], neg(k)),
             "x %s %s" % (OPS[FLIP[res]], neg(-k))]
        return M("일차부등식 <b>%s %s %s</b>를 풀면?" % (lhs, OPS[op], rhs), ok, w,
                 "x항은 왼쪽, 상수항은 오른쪽으로 이항하면 %sx %s %s. %s<b>%s</b>" % (neg(co), OPS[op], neg(co * k), "음수로 나누므로 부등호의 방향이 바뀌어요. " if co < 0 else "", ok))
    return mk


def i_graph(kinds=tuple(["read", "solve"])):
    def mk():
        t = solve_ineq()
        if not t:
            return None
        lhs, rhs, op, k, res, co = t
        how = R.choice(kinds)
        g = ineq_line(k, res)
        if how == "read":
            ok = "x %s %s" % (OPS[res], neg(k))
            w = ["x %s %s" % (OPS[FLIP[res]], neg(k)), "x %s %s" % (OPS[{"<": "≤", ">": "≥", "≤": "<", "≥": ">"}[res]], neg(k)), "x %s %s" % (OPS[res], neg(k + 1))]
            return M("수직선 위에 나타낸 x의 값의 범위는?%s" % g, ok, w, "%s이고 %s쪽이에요. <b>%s</b>" % ("● (포함)" if res in "≤≥" else "○ (포함하지 않음)", "오른" if res in "> ≥" else "왼", ok))
        cnt = None
        if res in ("<", "≤"):
            n = k if res == "≤" else k - 1
            if n < 1:
                return None
            return N("일차부등식 <b>%s %s %s</b>를 만족하는 자연수 x의 개수는?" % (lhs, OPS[op], rhs), n, [n + 1, n - 1, k, abs(k) + 2],
                     "해는 %s이므로 자연수는 1부터 %d까지. <b>%d개</b>" % ("x %s %s" % (OPS[res], neg(k)), n, n), f=lambda v: "%s개" % neg(v))
        m = k + 1 if res == ">" else k
        if m < 1:
            m = 1
        return N("일차부등식 <b>%s %s %s</b>를 만족하는 가장 작은 정수 x는?" % (lhs, OPS[op], rhs), k + 1 if res == ">" else k, [k, k + 2 if res == ">" else k + 1, -k, k - 1],
                 "해는 x %s %s이에요. <b>%s</b>" % (OPS[res], neg(k), neg(k + 1 if res == ">" else k)))
    return mk


def i_word():
    def mk():
        how = R.choice(["buy", "avg", "rect", "walk", "phone", "more"])
        nm = NM.next()
        if how == "buy":
            p, q, b = R.choice([800, 1000, 1200, 1500]), R.choice([500, 600, 700]), R.choice([10000, 12000, 15000, 20000])
            n = R.randint(8, 15)
            if p * n >= b + 2000 or q * n > b:
                return None
            # 볼펜 p원 x개, 연필 q원 (n − x)개, 총 b원 이하
            mx = (b - q * n) // (p - q)
            if mx < 1 or mx >= n:
                return None
            return N("%s %d원짜리 볼펜과 %d원짜리 연필을 합하여 %d자루 사려고 해요. 전체 금액이 %s원 이하가 되게 하려면 볼펜은 최대 몇 자루까지 살 수 있을까요?" % (josa(nm, "은/는") + "", p, q, n, num(b)), mx,
                     [mx + 1, mx - 1, b // p, n - mx], "%dx + %d(%d − x) ≤ %s → x ≤ %s. <b>%d자루</b>" % (p, q, n, num(b), neg(Fr(b - q * n, p - q)), mx), f=lambda v: "%s자루" % neg(v))
        if how == "avg":
            s1, s2 = R.randint(70, 85), R.randint(70, 85)
            t = R.choice([80, 85, 90])
            need = 3 * t - s1 - s2
            if not 60 <= need <= 100:
                return None
            return N("%s 두 번의 시험에서 %d점, %d점을 받았어요. 세 번의 평균이 %d점 이상이 되려면 세 번째 시험에서 최소 몇 점을 받아야 할까요?" % (josa(nm, "은/는"), s1, s2, t), need,
                     [need - 1, t, need + 3, 2 * t - s1 - s2 + 60 if 2 * t - s1 - s2 + 60 != need else need + 5], "(%d + %d + x) ÷ 3 ≥ %d → x ≥ %d. <b>%d점</b>" % (s1, s2, t, need, need), f=lambda v: "%s점" % neg(v))
        if how == "rect":
            a = R.randint(5, 12)
            L = R.choice([40, 50, 60, 70])
            mx = L // 2 - a
            return N("가로의 길이가 %d cm인 직사각형의 둘레의 길이가 %d cm 이하가 되게 하려고 해요. 세로의 길이는 최대 몇 cm일까요?" % (a, L), mx, [L - a, L // 2, mx + 1, L - 2 * a],
                     "2(%d + x) ≤ %d → x ≤ %d. <b>%d cm</b>" % (a, L, mx, mx), f=lambda v: "%s cm" % neg(v))
        if how == "walk":
            v = R.choice([2, 3, 4])
            T = R.choice([2, 3])
            d = Fr(v * T, 2)
            return M("%s 산책을 하는데 갈 때와 올 때 모두 시속 %d km로 걸어요. 전체 %d시간 이내에 돌아오려면 최대 몇 km 떨어진 곳까지 갈 수 있을까요?" % (josa(nm, "은/는"), v, T), "%s km" % neg(d),
                     ["%s km" % neg(v * T), "%s km" % neg(d + 1), "%s km" % neg(Fr(T, v))], "x/%d + x/%d ≤ %d → x ≤ %s. <b>%s km</b>" % (v, v, T, neg(d), neg(d)))
        if how == "phone":
            a, b, pa, pb = R.choice([(10000, 2000, 20, 100), (5000, 2000, 50, 80), (12000, 3000, 30, 60), (15000, 5000, 10, 60)])
            # A 요금제: a + pa·x, B: b + pb·x → A가 유리: a + pa x < b + pb x → x > (a − b)/(pb − pa)
            k = Fr(a - b, pb - pa)
            n = math.floor(k) + 1
            return N("A 요금제는 기본요금 %s원에 1분마다 %d원, B 요금제는 기본요금 %s원에 1분마다 %d원이에요. A 요금제가 더 유리하려면 한 달에 최소 몇 분 넘게 통화해야 할까요? (자연수)" % (num(a), pa, num(b), pb), n,
                     [n - 1, n + 1, Fr(a, pb).__floor__(), n * 2], "%s + %dx &lt; %s + %dx → x &gt; %s. <b>%d분</b>" % (num(a), pa, num(b), pb, neg(k), n), f=lambda v: "%s분" % neg(v))
        e, n_ = R.choice([(1500, 1200), (2000, 1500), (3000, 2400)]) if False else R.choice([(1000, 1500, 700), (1200, 2000, 900), (2000, 3000, 1600)])[:2], 0
        a1, fee, a2 = R.choice([(1000, 1500, 700), (1200, 2000, 900), (2000, 3000, 1600)])
        k = Fr(fee, a1 - a2)
        n = math.floor(k) + 1
        return N("동네 가게에서 공책 한 권은 %s원이에요. 대형 마트에서는 한 권에 %s원이지만 왕복 교통비 %s원이 들어요. 공책을 몇 권 이상 살 때 대형 마트가 유리할까요?" % (num(a1), num(a2), num(fee)), n,
                 [n - 1, n + 1, fee // a2 + 1, fee // a1], "%sx &gt; %sx + %s → x &gt; %s. <b>%d권</b>" % (num(a1), num(a2), num(fee), neg(k), n), f=lambda v: "%s권" % neg(v))
    return mk


# ------------------------------------------------------------------ 연립일차방정식
def lin2(a, b, c):
    return "%s = %s" % (poly2({(1, 0): a, (0, 1): b}), neg(c))


def sys_make(sol=None):
    x, y = sol or (R.randint(-5, 6), R.randint(-5, 6))
    while True:
        a1, b1, a2, b2 = [R.choice([-3, -2, -1, 1, 2, 3, 4, 5]) for _ in range(4)]
        if a1 * b2 - a2 * b1 != 0:
            break
    return (a1, b1, a1 * x + b1 * y), (a2, b2, a2 * x + b2 * y), x, y


def ans_xy(x, y):
    return "x = %s, y = %s" % (neg(x), neg(y))


def sy_solve(kinds=tuple(["plain", "sub"])):
    def mk():
        e1, e2, x, y = sys_make()
        how = R.choice(kinds)
        if how == "sub":
            p, q = R.choice([-3, -2, 2, 3, 4]), y - 0
            q = y - p * x
            e1 = (0, 0, 0)
            first = "y = %s" % poly2({(1, 0): p, (0, 0): q})
            a2, b2 = R.choice([1, 2, 3]), R.choice([-2, -1, 1, 2, 3])
            if a2 + b2 * p == 0:
                return None
            sec = lin2(a2, b2, a2 * x + b2 * y)
            q_ = "<span class='sys'>%s<br>%s</span>" % (first, sec)
            how2 = "대입법: 첫째 식을 둘째 식에 대입해요."
        else:
            q_ = "<span class='sys'>%s<br>%s</span>" % (lin2(*e1), lin2(*e2))
            how2 = "가감법: 한 문자의 계수를 맞추어 없애요."
        if x == y:
            return None
        return M("연립방정식 %s 의 해는?" % q_, ans_xy(x, y), [ans_xy(y, x), ans_xy(-x, y), ans_xy(x, -y), ans_xy(x + 1, y - 1)], "%s <b>%s</b>" % (how2, ans_xy(x, y)))
    return mk


def sy_check(kinds=tuple(["is", "find", "nat"])):
    def mk():
        how = R.choice(kinds)
        if how == "is":
            a, b = R.choice([1, 2, 3]), R.choice([-2, -1, 1, 2, 3])
            x0, y0 = R.randint(-3, 4), R.randint(-3, 4)
            c = a * x0 + b * y0
            cands = [(x0 + b, y0 - a), (x0 + 1, y0), (x0, y0 + 1), (x0 - 1, y0 + 1), (y0, x0)]
            bad = ["(%s, %s)" % (neg(p), neg(q)) for p, q in cands if a * p + b * q != c]
            ok = "(%s, %s)" % (neg(x0), neg(y0))
            return M("다음 중 일차방정식 <b>%s</b>의 해인 것은? (x, y)" % lin2(a, b, c), ok, bad, "대입하면 %s × %s + %s × %s = %s. <b>%s</b>" % (a, par(x0), par(b), par(y0), neg(c), ok))
        if how == "find":
            x0, y0 = R.randint(-3, 5), R.randint(-3, 5)
            b = R.choice([-3, -2, 1, 2, 3])
            a = R.choice([-3, -2, 2, 3, 4])
            c = a * x0 + b * y0
            if x0 == 0:
                return None
            return N("x = %s, y = %s가 일차방정식 <b>ax %s %s = %s</b>의 해일 때, 상수 a의 값은?" % (neg(x0), neg(y0), "+" if b > 0 else "−", (str(abs(b)) if abs(b) != 1 else "") + "y", neg(c)), a,
                     [-a, Fr(c, x0), a + 1, Fr(c - b * y0, y0) if y0 else a - 1], "%s × a + %s × %s = %s → a = <b>%s</b>" % (par(x0), par(b), par(y0), neg(c), neg(a)))
        a, b = R.randint(1, 3), R.randint(1, 3)
        c = R.randint(8, 16)
        sols = [(x, (c - a * x) // b) for x in range(1, c) if (c - a * x) > 0 and (c - a * x) % b == 0]
        n = len(sols)
        if n < 1:
            return None
        return N("x, y가 자연수일 때, 일차방정식 <b>%s</b>의 해는 모두 몇 개일까요?" % lin2(a, b, c), n, [n + 1, n - 1 if n > 1 else n + 2, c, c // a], "해: %s. <b>%d개</b>" % (", ".join("(%d, %d)" % s for s in sols), n),
                 f=lambda v: "%s개" % neg(v))
    return mk


def sy_special():
    def mk():
        a, b, c = R.choice([1, 2, 3]), R.choice([-2, -1, 1, 2, 3]), R.randint(1, 9)
        k = R.choice([2, 3, -2])
        how = R.choice(["inf", "none", "one"])
        if how == "inf":
            e2 = (a * k, b * k, c * k)
        elif how == "none":
            e2 = (a * k, b * k, c * k + R.choice([1, 2, 3]))
        else:
            e2 = (a * k + 1, b * k, c * k)
        ok = {"inf": "해가 무수히 많아요", "none": "해가 없어요", "one": "해가 한 쌍이에요"}[how]
        return M("연립방정식 <span class='sys'>%s<br>%s</span> 의 해는?" % (lin2(a, b, c), lin2(*e2)), ok, [x for x in ("해가 무수히 많아요", "해가 없어요", "해가 한 쌍이에요", "해가 두 쌍이에요") if x != ok],
                 {"inf": "둘째 식은 첫째 식의 양변에 %s를 곱한 것과 같아요." % neg(k), "none": "x, y의 계수의 비는 같고 상수항의 비만 달라요.", "one": "x, y의 계수의 비가 달라요."}[how] + " <b>%s</b>" % ok)
    return mk


def sy_word(kinds=tuple(["price", "legs", "digit", "age", "speed", "score", "total"])):
    def mk():
        how = R.choice(kinds)
        nm = NM.next()
        if how == "price":
            p, q = R.choice([(700, 1200), (500, 900), (800, 1500), (1000, 1800)])
            x, y = R.randint(2, 9), R.randint(2, 9)
            n, t = x + y, p * x + q * y
            return N("%s 한 개에 %d원인 사탕과 한 개에 %s원인 과자를 합하여 %d개 사고 %s원을 냈어요. 사탕은 몇 개 샀을까요?" % (josa(nm, "이/가"), p, num(q), n, num(t)), x, [y, x + 1, x - 1, n - x + 1],
                     "x + y = %d, %dx + %sy = %s → x = %d, y = %d. <b>%d개</b>" % (n, p, num(q), num(t), x, y, x), f=lambda v: "%s개" % neg(v))
        if how == "legs":
            x, y = R.randint(3, 15), R.randint(3, 15)
            return N("닭과 돼지가 모두 %d마리 있고, 다리 수의 합이 %d개예요. 돼지는 몇 마리일까요?" % (x + y, 2 * x + 4 * y), y, [x, y + 1, (2 * x + 4 * y) // 4, y - 1],
                     "x + y = %d, 2x + 4y = %d → x = %d, y = %d. <b>%d마리</b>" % (x + y, 2 * x + 4 * y, x, y, y), f=lambda v: "%s마리" % neg(v))
        if how == "digit":
            a, b = R.randint(1, 8), R.randint(1, 9)
            if a >= b or a + b > 15:
                return None
            n = 10 * a + b
            return N("두 자리 자연수에서 각 자리 숫자의 합은 %d이고, 십의 자리 숫자와 일의 자리 숫자를 바꾼 수는 처음 수보다 %d만큼 커요. 처음 수는?" % (a + b, 9 * (b - a)), n, [10 * b + a, n + 9, n - 9, 10 * a + b + 1],
                     "x + y = %d, (10y + x) − (10x + y) = %d → x = %d, y = %d. <b>%d</b>" % (a + b, 9 * (b - a), a, b, n))
        if how == "age":
            c = R.randint(10, 15)
            p = c + R.randint(24, 32)
            s = p + c
            d = p - c
            return N("현재 아버지와 %s 나이의 합은 %d살이고, 차는 %d살이에요. %s 현재 나이는?" % (josa(nm, "의")[:-1] if False else nm, s, d, josa(nm, "의")), c, [p, c + 1, d, s // 2],
                     "x + y = %d, x − y = %d → x = %d, y = %d. <b>%d살</b>" % (s, d, p, c, c), f=lambda v: "%s살" % neg(v))
        if how == "speed":
            v1, v2 = R.choice([(2, 4), (3, 6), (4, 8), (3, 5), (2, 6)])
            t1, t2 = R.choice([Fr(1, 2), 1, Fr(3, 2), 2]), R.choice([Fr(1, 2), 1, Fr(3, 2)])
            d1, d2 = v1 * t1, v2 * t2
            D, T = d1 + d2, t1 + t2
            if Fr(D).denominator != 1 or Fr(T * 60).denominator != 1:
                return None
            return M("%s 집에서 %s km 떨어진 공원까지 가는데, 처음에는 시속 %d km로 걷다가 도중에 시속 %d km로 뛰어서 모두 %s시간이 걸렸어요. 걸어간 거리는?" % (josa(nm, "이/가"), neg(D), v1, v2, neg(T) if Fr(T).denominator == 1 else neg(T)),
                     "%s km" % neg(d1), ["%s km" % neg(d2), "%s km" % neg(d1 + 1), "%s km" % neg(t1)],
                     "x + y = %s, x/%d + y/%d = %s → <b>%s km</b>" % (neg(D), v1, v2, neg(T), neg(d1)))
        if how == "score":
            x, y = R.randint(3, 12), R.randint(1, 8)
            return N("농구 경기에서 %s 2점 슛과 3점 슛을 합하여 %d골을 넣어 %d점을 얻었어요. 3점 슛은 몇 골일까요?" % (josa(nm, "이/가"), x + y, 2 * x + 3 * y), y, [x, y + 1, (2 * x + 3 * y) // 3, y - 1 if y > 1 else y + 2],
                     "x + y = %d, 2x + 3y = %d → x = %d, y = %d. <b>%d골</b>" % (x + y, 2 * x + 3 * y, x, y, y), f=lambda v: "%s골" % neg(v))
        b, g = R.randint(10, 20), R.randint(10, 20)
        pb, pg = R.choice([(10, 20), (20, 10), (10, 30), (20, 30)])
        dif = Fr(pb, 100) * b + Fr(pg, 100) * g
        if Fr(dif).denominator != 1 or b == g:
            return None
        return N("어느 동아리의 학생은 %d명이에요. 이 중 남학생의 %d%%와 여학생의 %d%%가 안경을 쓰고, 안경을 쓴 학생은 %s명이에요. 남학생은 몇 명일까요?" % (b + g, pb, pg, neg(dif)), b, [g, b + 1, b + 5, (b + g) // 2],
                 "x + y = %d, %s·x + %s·y = %s → x = %d. <b>%d명</b>" % (b + g, dec(Fr(pb, 100)), dec(Fr(pg, 100)), neg(dif), b, b), f=lambda v: "%s명" % neg(v))
    return mk


# ------------------------------------------------------------------ 일차함수
def lin(a, b):
    return "y = " + poly2({(1, 0): a, (0, 0): b})


def f_func(kinds=tuple(["val", "is_func", "is_lin", "fa"])):
    def mk():
        how = R.choice(kinds)
        if how == "val":
            a, b, x = R.choice([-3, -2, 2, 3, 4, Fr(1, 2)]), R.randint(-6, 6), R.choice([-4, -2, -1, 2, 3, 4])
            v = a * x + b
            if Fr(v).denominator != 1:
                return None
            return N("일차함수 <b>f(x) = %s</b>에서 f(%s)의 값은?" % (poly2({(1, 0): a, (0, 0): b}), neg(x)), v, [a * (-x) + b, a * x - b, a + x + b, v + 1],
                     "x에 %s를 대입해요. <b>%s</b>" % (neg(x), neg(v)))
        if how == "fa":
            a, b, k = R.choice([-3, -2, 2, 3, 4]), R.randint(-6, 6), R.randint(-5, 9)
            x = Fr(k - b, a)
            if x.denominator != 1:
                return None
            return N("일차함수 f(x) = %s에서 f(p) = %d일 때, p의 값은?" % (poly2({(1, 0): a, (0, 0): b}), k), x, [a * k + b, Fr(k + b, a), -x, x + 1], "%s = %d → p = <b>%s</b>" % (poly2({(1, 0): a, (0, 0): b}, ("p", "_")), k, neg(x)))
        if how == "is_func":
            T = ["y = (자연수 x의 약수)", "y = (자연수 x보다 작은 소수)", "y = (절댓값이 x인 수)", "y = (자연수 x의 배수)"]
            F = ["y = (자연수 x를 3으로 나눈 나머지)", "y = (한 개에 500원인 빵 x개의 값)", "y = (자연수 x보다 1 큰 수)", "y = (시속 4 km로 x시간 걸은 거리)", "y = (x의 2배)"]
            ok = R.choice(F)
            w = R.sample(T, 3)
            return M("다음 중 y가 x의 <b>함수</b>인 것은?", ok, w, "x의 값 하나에 y의 값이 오직 하나 정해져야 함수예요. <b>%s</b>" % ok)
        a, b = R.choice([-3, -2, 2, 3, 5]), R.randint(-5, 5)
        ok = lin(a, b)
        w = ["y = " + poly2({(2, 0): 1, (1, 0): a}), "y = %s/x" % neg(a), "y = %d" % b if b else "y = 3", "y = x(x − %d) − x²" % 0 if False else "y = " + poly2({(2, 0): a, (0, 0): b}), "x + y = x + %d" % abs(b or 4)]
        return M("다음 중 y가 x에 대한 <b>일차함수</b>인 것은?", ok, w, "y = ax + b (a ≠ 0) 꼴이어야 해요. <b>%s</b>" % ok)
    return mk


def f_shift(kinds=tuple(["shift", "int", "slope2", "area"])):
    def mk():
        a, b = R.choice([-4, -3, -2, Fr(-1, 2), Fr(1, 2), 2, 3, 4]), R.randint(-6, 6)
        how = R.choice(kinds)
        if how == "shift":
            k = R.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            ok = lin(a, b + k)
            return M("일차함수 <b>%s</b>의 그래프를 y축의 방향으로 %s만큼 평행이동한 그래프의 식은?" % (lin(a, b), neg(k)), ok, [lin(a, b - k), lin(a + k, b), lin(a, k), lin(-a, b + k)],
                     "y절편에 %s를 더해요. <b>%s</b>" % (neg(k), ok))
        if how == "int":
            if a.__class__ is Fr and Fr(-b, a).denominator != 1 or Fr(-b, a).denominator != 1 or b == 0:
                return None
            xi = Fr(-b, a)
            k = R.choice(["x", "y"])
            if k == "x":
                return N("일차함수 <b>%s</b>의 그래프의 <b>x절편</b>은?" % lin(a, b), xi, [b, -xi, Fr(b, a), a], "y = 0을 대입하면 x = <b>%s</b>" % neg(xi))
            return N("일차함수 <b>%s</b>의 그래프의 <b>y절편</b>은?" % lin(a, b), b, [xi, -b, a, b + 1], "x = 0일 때 y의 값이에요. <b>%s</b>" % neg(b))
        if how == "slope2":
            x1, x2 = R.sample(range(-4, 6), 2)
            a = R.choice([-3, -2, -1, 1, 2, 3, Fr(1, 2), Fr(-1, 2), Fr(2, 3)])
            y1, y2 = a * x1 + b, a * x2 + b
            if Fr(y1).denominator != 1 or Fr(y2).denominator != 1:
                return None
            return N("두 점 (%s, %s), (%s, %s)를 지나는 일차함수의 그래프의 <b>기울기</b>는?" % (neg(x1), neg(y1), neg(x2), neg(y2)), a, [1 / Fr(a) if a else 1, -a, Fr(y2 + y1, x2 + x1) if x2 + x1 else a + 1, a + 1],
                     "(y의 값의 증가량) ÷ (x의 값의 증가량) = (%s) ÷ (%s) = <b>%s</b>" % (neg(y2 - y1), neg(x2 - x1), neg(a)))
        a = R.choice([-3, -2, -1, 1, 2, 3])
        b = R.choice([-6, -4, -3, 3, 4, 6])
        xi = Fr(-b, a)
        if xi.denominator != 1:
            return None
        A = abs(xi * b) / 2
        return N("일차함수 <b>%s</b>의 그래프와 x축, y축으로 둘러싸인 삼각형의 넓이는?" % lin(a, b), A, [abs(xi * b), abs(b) + abs(xi), A + 1, abs(b) * abs(b) / 2 if abs(b) != abs(xi) else A + 2],
                 "x절편 %s, y절편 %s → ½ × %s × %s = <b>%s</b>" % (neg(xi), neg(b), neg(abs(xi)), neg(abs(b)), neg(A)))
    return mk


def f_graph():
    def mk():
        a = R.choice([-3, -2, -1, 1, 2, 3, Fr(1, 2), Fr(-1, 2), Fr(2, 3), Fr(-2, 3), Fr(3, 2)])
        b = R.randint(-3, 3)
        ok = lin(a, b)
        g = kosy(lines=[(a, b, BLUE, "")], pts=[(0, b, "")], lo=-5, hi=5, label="일차함수의 그래프")
        w = [lin(-a, b), lin(a, -b), lin(1 / Fr(a), b), lin(a + 1 if a != -1 else 2, b), lin(b, a) if b else lin(a, 1)]
        if R.random() < 0.5:
            return M("그래프가 나타내는 일차함수의 식은?%s" % g, ok, w, "y절편 %s, 기울기 %s. <b>%s</b>" % (neg(b), neg(a), ok))
        k = R.choice(["slope", "inc"])
        if k == "slope":
            return N("그래프가 나타내는 일차함수의 기울기는?%s" % g, a, [-a, 1 / Fr(a), b if b != a else a + 1, a + 1], "오른쪽으로 %d만큼 가면 %s로 %d만큼 가요. <b>%s</b>" % (Fr(a).denominator, "위" if a > 0 else "아래", abs(Fr(a).numerator), neg(a)))
        ok = "x의 값이 증가하면 y의 값도 증가해요" if a > 0 else "x의 값이 증가하면 y의 값은 감소해요"
        bad = "x의 값이 증가하면 y의 값은 감소해요" if a > 0 else "x의 값이 증가하면 y의 값도 증가해요"
        return M("그래프에 대한 설명으로 옳은 것은?%s" % g, ok, [bad, "y절편은 %s예요" % neg(b + 1), "점 (0, %s)를 지나지 않아요" % neg(b)], "기울기가 %s이므로 <b>%s</b>." % ("양수" if a > 0 else "음수", ok))
    return mk


def g_equation(kinds=tuple(["ab", "pt", "two", "xint"])):
    def mk():
        how = R.choice(kinds)
        a = R.choice([-3, -2, -1, 1, 2, 3, 4, Fr(1, 2), Fr(-1, 2)])
        b = R.randint(-6, 6)
        ok = lin(a, b)
        w = [lin(-a, b), lin(a, -b), lin(b, a) if b and b != a else lin(a, b + 2), lin(1 / Fr(a), b)]
        if how == "ab":
            return M("기울기가 %s이고 y절편이 %s인 직선을 그래프로 하는 일차함수의 식은?" % (neg(a), neg(b)), ok, w, "y = ax + b에 그대로 넣어요. <b>%s</b>" % ok)
        if how == "pt":
            x0 = R.choice([-3, -2, -1, 1, 2, 3, 4])
            y0 = a * x0 + b
            if Fr(y0).denominator != 1:
                return None
            return M("기울기가 %s이고 점 (%s, %s)를 지나는 직선을 그래프로 하는 일차함수의 식은?" % (neg(a), neg(x0), neg(y0)), ok, w + [lin(a, y0)],
                     "y = %sx + b에 대입하면 b = %s. <b>%s</b>" % (neg(a) if a != 1 else "", neg(b), ok))
        if how == "two":
            x1, x2 = R.sample([-3, -2, -1, 0, 1, 2, 3, 4], 2)
            y1, y2 = a * x1 + b, a * x2 + b
            if Fr(y1).denominator != 1 or Fr(y2).denominator != 1:
                return None
            return M("두 점 (%s, %s), (%s, %s)를 지나는 직선을 그래프로 하는 일차함수의 식은?" % (neg(x1), neg(y1), neg(x2), neg(y2)), ok, w,
                     "기울기 = (%s) ÷ (%s) = %s, 한 점을 대입하면 y절편 %s. <b>%s</b>" % (neg(y2 - y1), neg(x2 - x1), neg(a), neg(b), ok))
        p = R.choice([-4, -3, -2, 2, 3, 4, 6])
        q = R.choice([-6, -4, -3, -2, 2, 3, 4, 6])
        a = Fr(-q, p)
        ok = lin(a, q)
        return M("x절편이 %s, y절편이 %s인 직선을 그래프로 하는 일차함수의 식은?" % (neg(p), neg(q)), ok, [lin(-a, q), lin(Fr(q, p), q), lin(Fr(-p, q), q), lin(a, p)],
                 "두 점 (%s, 0), (0, %s)를 지나므로 기울기는 %s. <b>%s</b>" % (neg(p), neg(q), neg(a), ok))
    return mk


def g_prop(kinds=tuple(["par", "same", "quad", "word"])):
    def mk():
        how = R.choice(kinds)
        a, b = R.choice([-3, -2, 2, 3, Fr(1, 2), Fr(-2, 3)]), R.randint(-5, 5)
        if how == "par":
            ok = lin(a, b + R.choice([-3, 2, 4]))
            return M("다음 중 일차함수 <b>%s</b>의 그래프와 <b>평행한</b> 것은?" % lin(a, b), ok, [lin(-a, b), lin(1 / Fr(a), b + 1), lin(a + 1, b), lin(-1 / Fr(a), b)],
                     "기울기가 같고 y절편이 다르면 평행해요. <b>%s</b>" % ok)
        if how == "same":
            k = R.choice([2, 3, -2])
            p, q = R.randint(-5, 5), R.choice([2, 3])
            return M("두 일차함수 y = ax %s와 y = %sx + b의 그래프가 <b>일치</b>할 때, a, b의 값은?" % (("+ %d" % p) if p > 0 else ("− %d" % -p) if p else "", neg(q)), "a = %s, b = %s" % (neg(q), neg(p)),
                     ["a = %s, b = %s" % (neg(p), neg(q)), "a = %s, b = %s" % (neg(-q), neg(p)), "a = %s, b = %s" % (neg(q), neg(-p))], "기울기와 y절편이 모두 같아야 해요. <b>a = %s, b = %s</b>" % (neg(q), neg(p)))
        if how == "quad":
            sa, sb = R.choice([1, -1]), R.choice([1, -1])
            q = {(1, 1): "제4사분면", (1, -1): "제2사분면", (-1, 1): "제3사분면", (-1, -1): "제1사분면"}[(sa, sb)]
            a, b = sa * R.choice([1, 2, 3]), sb * R.choice([1, 2, 3])
            return M("일차함수 <b>%s</b>의 그래프가 지나지 <b>않는</b> 사분면은?" % lin(a, b), q, [x for x in ("제1사분면", "제2사분면", "제3사분면", "제4사분면") if x != q],
                     "기울기 %s, y절편 %s이므로 %s 그래프예요. <b>%s</b>" % ("양수" if a > 0 else "음수", "양수" if b > 0 else "음수", "오른쪽 위로 향하는" if a > 0 else "오른쪽 아래로 향하는", q))
        T0 = R.choice([10, 15, 20, 25])
        r = R.choice([2, 3, 4, 5])
        t = R.choice([5, 8, 10, 12])
        nm = R.choice(["물을 데우는 주전자", "온도를 높이는 실험 용기"])
        return N("처음 온도가 %d°C인 물을 데우면 1분마다 온도가 %d°C씩 올라가요. %d분 후의 물의 온도는?" % (T0, r, t), T0 + r * t, [r * t, T0 * r, T0 + r + t, T0 + r * (t - 1)],
                 "y = %dx + %d에 x = %d를 대입해요. <b>%d°C</b>" % (r, T0, t, T0 + r * t), f=lambda v: "%s°C" % neg(v))
    return mk


def e_graph(kinds=tuple(["std", "vert", "cross", "count"])):
    def mk():
        how = R.choice(kinds)
        if how == "std":
            a, b = R.choice([1, 2, 3, 4, -2, -3]), R.choice([1, 2, 3, -1, -2])
            c = R.randint(-8, 8)
            sl, ic = Fr(-a, b), Fr(c, b)
            ok = lin(sl, ic)
            return M("일차방정식 <b>%s</b>의 그래프를 일차함수 꼴로 나타내면?" % lin2(a, b, c), ok, [lin(-sl, ic), lin(sl, -ic), lin(Fr(a, b), Fr(-c, b)), lin(Fr(-b, a), Fr(c, a))],
                     "y에 대하여 풀어요. <b>%s</b>" % ok)
        if how == "vert":
            p = R.choice([-4, -3, -2, 2, 3, 4, 5])
            k = R.choice(["x", "y"])
            if k == "x":
                return M("점 (%s, %s)를 지나고 <b>y축에 평행한</b> 직선의 방정식은?" % (neg(p), neg(R.randint(-4, 4))), "x = %s" % neg(p), ["y = %s" % neg(p), "x = %s" % neg(-p), "y = x + %s" % neg(p) if p > 0 else "y = x − %s" % neg(-p)],
                         "y축에 평행한 직선은 x = (일정)이에요. <b>x = %s</b>" % neg(p))
            q = R.randint(-4, 4) or 2
            return M("점 (%s, %s)를 지나고 <b>x축에 평행한</b> 직선의 방정식은?" % (neg(p), neg(q)), "y = %s" % neg(q), ["x = %s" % neg(p), "y = %s" % neg(p) if p != q else "y = 0", "x = %s" % neg(q)],
                     "x축에 평행한 직선은 y = (일정)이에요. <b>y = %s</b>" % neg(q))
        if how == "cross":
            x, y = R.randint(-3, 3), R.randint(-3, 3)
            a1, a2 = R.sample([-2, -1, 1, 2, Fr(1, 2), Fr(-1, 2), 3], 2)
            b1, b2 = y - a1 * x, y - a2 * x
            if Fr(b1).denominator != 1 or Fr(b2).denominator != 1 or abs(b1) > 5 or abs(b2) > 5 or x == y:
                return None
            g = kosy(lines=[(a1, b1, BLUE, ""), (a2, b2, RED, "")], pts=[(x, y, "")], lo=-5, hi=5, label="두 일차함수의 그래프")
            return M("두 일차방정식의 그래프가 그림과 같을 때, 연립방정식 <span class='sys'>%s<br>%s</span> 의 해는?%s" % (lin(a1, b1), lin(a2, b2), g), ans_xy(x, y),
                     [ans_xy(y, x), ans_xy(-x, y), ans_xy(x, -y), ans_xy(x + 1, y)], "두 그래프의 교점의 좌표가 해예요. <b>%s</b>" % ans_xy(x, y))
        a, b = R.choice([-3, -2, 2, 3]), R.randint(-4, 4)
        k = R.choice(["none", "inf", "one"])
        b2 = {"none": b + R.choice([-3, 2, 4]), "inf": b, "one": b}[k]
        a2 = a if k != "one" else a + R.choice([-1, 1, 2])
        ok = {"none": "해가 없어요", "inf": "해가 무수히 많아요", "one": "해가 한 쌍이에요"}[k]
        return M("두 일차함수 <b>%s</b>, <b>%s</b>의 그래프로 생각할 때, 두 식을 연립한 방정식의 해는?" % (lin(a, b), lin(a2, b2)), ok, [x for x in ("해가 없어요", "해가 무수히 많아요", "해가 한 쌍이에요", "해가 두 쌍이에요") if x != ok],
                 {"none": "기울기가 같고 y절편이 달라 평행해요.", "inf": "두 그래프가 일치해요.", "one": "기울기가 달라 한 점에서 만나요."}[k] + " <b>%s</b>" % ok)
    return mk


def e_area():
    def mk():
        # 두 직선과 x축(또는 y축)으로 둘러싸인 삼각형 넓이
        x, y = R.randint(-2, 3), R.randint(2, 5)
        a1, a2 = R.choice([1, 2, 3]), R.choice([-1, -2, -3])
        b1, b2 = y - a1 * x, y - a2 * x
        x1, x2 = Fr(-b1, a1), Fr(-b2, a2)
        A = abs(x2 - x1) * y / 2
        if Fr(x1).denominator != 1 or Fr(x2).denominator != 1 or abs(x1) > 6 or abs(x2) > 6:
            return None
        g = kosy(lines=[(a1, b1, BLUE, ""), (a2, b2, RED, "")], pts=[(x, y, "P")], lo=-6, hi=6, label="두 직선과 x축으로 둘러싸인 삼각형")
        return N("두 직선 %s, %s와 x축으로 둘러싸인 삼각형의 넓이는?%s" % (lin(a1, b1), lin(a2, b2), g), A, [abs(x2 - x1) * y, A + y, abs(x2 - x1) + y, A - 1],
                 "교점 P(%s, %s), x절편 %s, %s → ½ × %s × %s = <b>%s</b>" % (neg(x), neg(y), neg(x1), neg(x2), neg(abs(x2 - x1)), y, neg(A)))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "repdec":
        return unit(G, "repeating-decimals", 1, "[9수01-06]", "순환소수의 뜻을 알고, 유리수와 순환소수의 관계를 설명할 수 있다.",
                    "유리수와 순환소수", "순환소수",
                    "중학교 2학년 수학 유리수와 순환소수 문제: 순환마디와 순환소수의 표현, 유한소수로 나타낼 수 있는 분수, 분수를 순환소수로, 순환소수를 분수로 나타내기까지 100문제와 정답·해설.",
                    "분모의 소인수가 2, 5뿐이면 유한소수", "정수가 아닌 유리수는 유한소수 또는 순환소수예요.",
                    ["소수점 아래의 0이 아닌 숫자가 무한히 계속되는 소수를 <b>무한소수</b>라 하고, 같은 숫자의 배열이 한없이 되풀이되면 <b>순환소수</b>라고 해요.",
                     "되풀이되는 가장 짧은 부분을 <b>순환마디</b>라 하고, 순환마디의 처음과 끝 숫자 위에 점을 찍어 나타내요. 0.353535… = 0.3̇5̇",
                     "기약분수의 분모의 소인수가 <b>2나 5뿐</b>이면 유한소수, 그 외의 소인수가 있으면 순환소수가 돼요.",
                     "순환소수를 분수로: x = 0.3̇5̇이면 100x − x = 35, x = 35/99"],
                    [("7/12는 유한소수?", ["12 = 2² × 3", "3이 있음"], "순환소수"), ("0.4̇를 분수로", ["10x − x = 4"], "4/9")],
                    [("분자를 보고 유한소수인지 판단한다", "기약분수로 고친 뒤 분모의 소인수를 봐요."),
                     ("0.1̇2̇를 12/100으로 고친다", "순환마디가 두 자리이면 99로 나누어요. 12/99 = 4/33"),
                     ("순환소수는 유리수가 아니라고 한다", "순환소수는 모두 분수로 나타낼 수 있는 유리수예요.")],
                    [("0.999…는 왜 1인가요?", "x = 0.999…이면 10x − x = 9, x = 1이에요."),
                     ("6/15는 유한소수인가요?", "기약분수 2/5의 분모가 5뿐이므로 유한소수(0.4)예요.")],
                    [("순환소수의 표현", [(rd_notation(), 20)]),
                     ("유한소수로 나타낼 수 있는 분수", [(rd_finite(), 20)]),
                     ("분수를 순환소수로", [(rd_frac2dec(), 20)]),
                     ("순환소수를 분수로", [(rd_tofrac(), 20)]),
                     ("유리수와 소수의 관계", [(rd_class(), 2), (rd_tofrac(), 9), (rd_finite(), 9)])], 82801)
    if which == "expo":
        return unit(G, "exponent-laws-and-monomials", 2, "[9수02-08] [9수02-10]",
                    "지수법칙을 이해한다. 다항식의 곱셈과 단항식의 나눗셈의 원리를 이해하고, 그 계산을 할 수 있다.",
                    "지수법칙과 단항식의 곱셈·나눗셈", "지수법칙",
                    "중학교 2학년 수학 지수법칙과 단항식 문제: aᵐ × aⁿ, (aᵐ)ⁿ, aᵐ ÷ aⁿ, (ab)ⁿ, □ 안의 수, 단항식의 곱셈과 나눗셈, 활용까지 100문제와 정답·해설.",
                    "aᵐ × aⁿ = aᵐ⁺ⁿ, (aᵐ)ⁿ = aᵐⁿ", "나눗셈은 역수의 곱셈으로 바꾸어 계산해요.",
                    ["밑이 같은 거듭제곱의 곱셈은 지수끼리 <b>더해요</b>: aᵐ × aⁿ = aᵐ⁺ⁿ",
                     "거듭제곱의 거듭제곱은 지수끼리 <b>곱해요</b>: (aᵐ)ⁿ = aᵐⁿ",
                     "나눗셈은 지수끼리 빼요. m &gt; n이면 aᵐ⁻ⁿ, m = n이면 1, m &lt; n이면 1/aⁿ⁻ᵐ",
                     "(ab)ⁿ = aⁿbⁿ. 단항식의 곱셈은 계수끼리, 문자끼리 곱해요."],
                    [("x³ × x⁵", ["3 + 5"], "x⁸"), ("(2a²)³", ["2³ × a⁶"], "8a⁶")],
                    [("a³ × a⁴ = a¹²", "곱셈은 지수끼리 더해요. a⁷"),
                     ("(a²)³ = a⁵", "거듭제곱의 거듭제곱은 곱해요. a⁶"),
                     ("(3x)² = 3x²", "괄호 안의 계수도 제곱해요. 9x²")],
                    [("a⁰은 무엇인가요?", "중학교에서는 aᵐ ÷ aᵐ = 1처럼 나눗셈 결과로 다뤄요."),
                     ("음수의 거듭제곱은?", "(−2)³ = −8처럼 지수가 홀수이면 음수, 짝수이면 양수예요.")],
                    [("지수법칙", [(e_law(), 20)]),
                     ("□ 안에 알맞은 수", [(e_box(), 20)]),
                     ("단항식의 곱셈", [(e_mono(("mul",)), 20)]),
                     ("단항식의 나눗셈", [(e_mono(("div", "mix")), 20)]),
                     ("활용", [(e_word(), 10), (e_law(), 10)])], 82802)
    if which == "poly":
        return unit(G, "polynomial-operations", 3, "[9수02-09] [9수02-10]",
                    "다항식의 덧셈과 뺄셈의 원리를 이해하고, 그 계산을 할 수 있다. (단항식) × (다항식), (다항식) ÷ (단항식)과 같은 곱셈과 나눗셈의 원리를 이해하고, 그 계산을 할 수 있다.",
                    "다항식의 덧셈·뺄셈·곱셈·나눗셈", "다항식의 계산",
                    "중학교 2학년 수학 다항식의 계산 문제: 두 문자를 포함한 다항식과 이차식의 덧셈과 뺄셈, 단항식과 다항식의 곱셈, 다항식÷단항식, 식의 값, 등식의 변형까지 100문제와 정답·해설.",
                    "괄호 앞이 −이면 모든 항의 부호를 바꿔요", "단항식을 다항식의 각 항에 곱해요(분배법칙).",
                    ["다항식의 덧셈과 뺄셈은 괄호를 풀고 <b>동류항</b>끼리 계산해요.",
                     "괄호 앞이 −이면 괄호 안의 <b>모든 항</b>의 부호를 바꾸어요.",
                     "(단항식) × (다항식)은 분배법칙으로 전개하고, (다항식) ÷ (단항식)은 각 항을 나누어요.",
                     "식을 한 문자에 대하여 풀 때는 이항한 뒤 계수로 나누어요."],
                    [("(3x + 2y) − (x − 4y)", ["3x + 2y − x + 4y"], "2x + 6y"), ("−2x(3x − y)", ["−6x² + 2xy"], "−6x² + 2xy")],
                    [("(3x + 2y) − (x − 4y) = 2x − 2y", "−(−4y) = +4y예요. 2x + 6y"),
                     ("2x(x + 3) = 2x² + 3", "3에도 2x를 곱해요. 2x² + 6x"),
                     ("(6x² + 3x) ÷ 3x = 2x + 3x", "각 항을 나누어요. 2x + 1")],
                    [("이차식은 무엇인가요?", "차수가 가장 큰 항의 차수가 2인 다항식이에요."),
                     ("식의 값을 구할 때 주의할 점은?", "음수를 대입할 때는 반드시 괄호를 써요.")],
                    [("다항식의 덧셈과 뺄셈", [(p_addsub(), 20)]),
                     ("단항식과 다항식의 곱셈", [(p_muldiv(("mul", "mul2")), 20)]),
                     ("다항식의 나눗셈", [(p_muldiv(("div",)), 20)]),
                     ("식의 값", [(p_value(), 20)]),
                     ("식의 대입과 변형", [(p_solvefor(), 20)])], 82803)
    if which == "ineq":
        return unit(G, "linear-inequalities", 4, "[9수02-11] [9수02-12]",
                    "부등식과 그 해의 의미를 알고, 부등식의 성질을 설명할 수 있다. 일차부등식을 풀 수 있고, 이를 활용하여 문제를 해결할 수 있다.",
                    "일차부등식: 성질, 풀이, 활용", "일차부등식",
                    "중학교 2학년 수학 일차부등식 문제: 부등식의 성질, 일차부등식의 풀이, 해를 수직선에 나타내기, 자연수인 해, 물건 사기·평균·요금제 등 활용까지 100문제와 정답·해설.",
                    "음수를 곱하거나 나누면 부등호 방향이 바뀌어요", "●은 포함, ○은 포함하지 않아요.",
                    ["부등식의 양변에 같은 수를 더하거나 빼도 부등호의 방향은 그대로예요.",
                     "양변에 같은 <b>양수</b>를 곱하거나 나누면 그대로, <b>음수</b>를 곱하거나 나누면 부등호의 방향이 <b>바뀌어요</b>.",
                     "x항은 왼쪽, 상수항은 오른쪽으로 이항하여 ax &gt; b 꼴로 만든 뒤 a로 나누어요.",
                     "수직선에서 ≤, ≥는 ●(포함), &lt;, &gt;는 ○(포함하지 않음)으로 나타내요."],
                    [("−3x + 2 &lt; 11", ["−3x &lt; 9", "−3으로 나누면 방향 바뀜"], "x &gt; −3"), ("2x − 1 ≤ x + 4", ["x ≤ 5"], "x ≤ 5")],
                    [("−2x &lt; 6 → x &lt; −3", "음수로 나누면 방향이 바뀌어요. x &gt; −3"),
                     ("x ≤ 3을 ○으로 나타낸다", "≤는 3을 포함하므로 ●이에요."),
                     ("활용에서 '이상'과 '초과'를 바꾼다", "이상·이하는 ≥, ≤, 초과·미만은 &gt;, &lt;예요.")],
                    [("부등식의 해는 왜 하나가 아닌가요?", "부등식을 참이 되게 하는 값은 보통 범위로 무수히 많아요."),
                     ("활용 문제에서 답은 어떻게 고르나요?", "구한 범위에서 문제의 조건(자연수, 최대·최소)에 맞는 값을 골라요.")],
                    [("부등식의 성질", [(i_prop(), 20)]),
                     ("일차부등식의 풀이", [(i_solve(), 20)]),
                     ("해와 수직선", [(i_graph(), 20)]),
                     ("일차부등식의 활용", [(i_word(), 20)]),
                     ("섞어서 연습", [(i_solve(), 7), (i_graph(), 6), (i_word(), 7)])], 82804)
    if which == "sys":
        return unit(G, "systems-of-linear-equations", 5, "[9수02-13]",
                    "미지수가 2개인 연립일차방정식을 풀 수 있고, 이를 활용하여 문제를 해결할 수 있다.",
                    "연립일차방정식의 풀이: 가감법과 대입법", "연립일차방정식",
                    "중학교 2학년 수학 연립일차방정식 문제: 미지수가 2개인 일차방정식의 해, 자연수인 해의 개수, 가감법과 대입법, 해가 없거나 무수히 많은 경우까지 100문제와 정답·해설.",
                    "한 문자를 없애서 일차방정식으로", "가감법은 계수를 맞추어 더하거나 빼고, 대입법은 한 식을 다른 식에 넣어요.",
                    ["미지수가 2개인 일차방정식 ax + by = c의 해는 등식을 참이 되게 하는 (x, y)의 순서쌍이에요.",
                     "두 방정식을 동시에 만족하는 해를 구하는 것이 <b>연립방정식을 푸는 것</b>이에요.",
                     "<b>가감법</b>: 한 문자의 계수의 절댓값을 같게 만든 뒤 더하거나 빼요. <b>대입법</b>: y = (x의 식)을 다른 식에 대입해요.",
                     "두 식의 x, y의 계수의 비는 같고 상수항의 비가 다르면 해가 없고, 모두 같으면 해가 무수히 많아요."],
                    [("x + y = 5, x − y = 1", ["더하면 2x = 6"], "x = 3, y = 2"), ("y = 2x, x + y = 9", ["x + 2x = 9"], "x = 3, y = 6")],
                    [("가감법에서 한쪽 식에만 수를 곱하고 상수항은 그대로 둔다", "양변 전체에 곱해요."),
                     ("빼는 식의 부호를 모두 바꾸지 않는다", "빼면 둘째 식의 모든 항의 부호가 바뀌어요."),
                     ("x의 값만 구하고 끝낸다", "x를 대입해 y도 구해야 해요.")],
                    [("가감법과 대입법 중 무엇이 좋나요?", "y = …꼴이 있으면 대입법, 계수를 맞추기 쉬우면 가감법이 편해요."),
                     ("해를 검산하는 방법은?", "구한 x, y를 두 식에 모두 대입해서 참인지 확인해요.")],
                    [("일차방정식의 해", [(sy_check(), 20)]),
                     ("가감법", [(sy_solve(("plain",)), 20)]),
                     ("대입법", [(sy_solve(("sub",)), 20)]),
                     ("해가 특수한 연립방정식", [(sy_special(), 20)]),
                     ("섞어서 연습", [(sy_solve(), 10), (sy_check(), 5), (sy_special(), 5)])], 82805)
    if which == "sysw":
        return unit(G, "systems-of-equations-word-problems", 6, "[9수02-13]",
                    "미지수가 2개인 연립일차방정식을 풀 수 있고, 이를 활용하여 문제를 해결할 수 있다.",
                    "연립일차방정식의 활용", "연립방정식의 활용",
                    "중학교 2학년 수학 연립일차방정식의 활용 문제: 개수와 가격, 다리 수, 두 자리 자연수, 나이, 거리·속력·시간, 득점, 비율 문제를 연립방정식으로 세워 푸는 100문제와 정답·해설.",
                    "구하는 것 두 개를 x, y로", "조건 두 개로 식 두 개를 세워요.",
                    ["구하려는 두 양을 x, y로 놓아요.",
                     "문제의 조건 두 가지로 연립방정식을 세워요(합계, 금액, 거리 등).",
                     "연립방정식을 풀고, 답이 문제의 뜻에 맞는지(자연수, 단위) 확인해요.",
                     "(거리) = (속력) × (시간), 두 자리 수는 10x + y로 나타내요."],
                    [("사과 300원, 배 500원 합 7개, 2700원", ["x + y = 7", "300x + 500y = 2700"], "사과 4개, 배 3개"),
                     ("닭 x, 소 y 합 10마리, 다리 28개", ["x + y = 10", "2x + 4y = 28"], "소 4마리")],
                    [("두 자리 수를 x + y로 놓는다", "십의 자리 x, 일의 자리 y이면 10x + y예요."),
                     ("거리를 시간 × 속력이 아니라 속력 ÷ 시간으로 쓴다", "(시간) = (거리) ÷ (속력)이에요."),
                     ("구한 값을 문제에서 묻는 것과 다르게 답한다", "x, y 중 무엇을 묻는지 다시 확인해요.")],
                    [("왜 미지수가 두 개면 식이 두 개 필요한가요?", "식이 하나이면 해가 무수히 많아서 하나로 정해지지 않아요."),
                     ("분수가 있는 식은 어떻게 하나요?", "양변에 분모의 최소공배수를 곱해 정수 계수로 바꾸어요.")],
                    [("개수와 가격", [(sy_word(("price", "legs")), 20)]),
                     ("나이와 수", [(sy_word(("age", "digit")), 20)]),
                     ("거리·속력·시간", [(sy_word(("speed",)), 20)]),
                     ("득점과 비율", [(sy_word(("score", "total")), 20)]),
                     ("섞어서 연습", [(sy_word(), 20)])], 82806)
    if which == "lf":
        return unit(G, "linear-functions", 7, "[9수02-14] [9수02-15]",
                    "함수의 개념을 이해하고, 함숫값을 구할 수 있다. 일차함수의 의미를 이해하고, 그 그래프를 그릴 수 있다.",
                    "함수와 일차함수의 그래프", "일차함수",
                    "중학교 2학년 수학 일차함수 문제: 함수의 뜻과 함숫값, 일차함수 찾기, 평행이동, x절편과 y절편, 기울기, 그래프 읽기, 축과 둘러싸인 넓이까지 100문제와 정답·해설.",
                    "y = ax + b (a ≠ 0)", "기울기 a는 x가 1 늘 때 y의 증가량이에요.",
                    ["x의 값이 하나 정해지면 y의 값이 오직 하나 정해질 때 y를 x의 <b>함수</b>라 하고, y = f(x)로 나타내요.",
                     "y = ax + b (a ≠ 0)를 <b>일차함수</b>라고 해요. y = ax의 그래프를 y축의 방향으로 b만큼 평행이동한 직선이에요.",
                     "그래프가 x축과 만나는 점의 x좌표가 <b>x절편</b>, y축과 만나는 점의 y좌표가 <b>y절편</b>이에요.",
                     "<b>기울기</b> = (y의 값의 증가량) ÷ (x의 값의 증가량) = a"],
                    [("y = 2x − 4의 x절편", ["0 = 2x − 4"], "2"), ("(1, 3), (3, 7)의 기울기", ["(7 − 3) ÷ (3 − 1)"], "2")],
                    [("기울기를 x의 증가량 ÷ y의 증가량으로 구한다", "y의 증가량 ÷ x의 증가량이에요."),
                     ("x절편과 y절편을 바꾼다", "x절편은 y = 0일 때의 x의 값이에요."),
                     ("평행이동하면 기울기도 바뀐다고 한다", "y축 방향 평행이동은 y절편만 바뀌어요.")],
                    [("y = 3은 일차함수인가요?", "x항이 없으니 일차함수가 아니에요(상수함수)."),
                     ("그래프는 어떻게 그리나요?", "y절편과 x절편, 또는 y절편과 기울기로 두 점을 찍고 이어요.")],
                    [("함수와 함숫값", [(f_func(), 20)]),
                     ("일차함수와 평행이동", [(f_shift(("shift", "area")), 20)]),
                     ("절편과 기울기", [(f_shift(("int", "slope2")), 20)]),
                     ("그래프 읽기", [(f_graph(), 20)]),
                     ("섞어서 연습", [(f_func(), 6), (f_shift(), 7), (f_graph(), 7)])], 82807)
    if which == "lfg":
        return unit(G, "graphs-of-linear-functions", 8, "[9수02-16]",
                    "일차함수의 그래프의 성질을 이해하고, 이를 활용하여 문제를 해결할 수 있다.",
                    "일차함수의 그래프의 성질과 식 구하기", "일차함수의 그래프",
                    "중학교 2학년 수학 일차함수의 그래프 문제: 기울기와 y절편, 지나는 사분면, 평행과 일치, 기울기와 한 점·두 점·두 절편으로 식 구하기, 실생활 활용까지 100문제와 정답·해설.",
                    "기울기가 같으면 평행 또는 일치", "a &gt; 0이면 오른쪽 위로, a &lt; 0이면 오른쪽 아래로 향해요.",
                    ["a &gt; 0이면 x가 증가할 때 y도 증가(오른쪽 위로 향함), a &lt; 0이면 y는 감소(오른쪽 아래로 향함)해요.",
                     "기울기가 같고 y절편이 다르면 두 그래프는 <b>평행</b>, 기울기와 y절편이 모두 같으면 <b>일치</b>해요.",
                     "식 구하기: 기울기 a와 한 점 → y = ax + b에 대입해 b를 구해요. 두 점 → 먼저 기울기를 구해요.",
                     "x절편 p, y절편 q → 두 점 (p, 0), (0, q)를 지나므로 기울기는 −q/p예요."],
                    [("기울기 2, 점 (1, 5)", ["5 = 2 + b"], "y = 2x + 3"), ("(0, 1), (2, 5)", ["기울기 2", "y절편 1"], "y = 2x + 1")],
                    [("기울기만 같으면 항상 평행하다고 한다", "y절편도 같으면 일치해요."),
                     ("점을 대입할 때 x, y를 바꾼다", "점 (x, y)의 앞이 x좌표예요."),
                     ("두 절편으로 기울기를 q/p로 쓴다", "기울기는 −q/p예요.")],
                    [("일차함수를 실생활에서 쓰나요?", "물의 온도, 남은 양, 요금처럼 일정하게 변하는 양을 나타낼 때 써요."),
                     ("기울기가 0이면?", "y = b로 x축에 평행한 직선이고 일차함수는 아니에요.")],
                    [("그래프의 성질", [(g_prop(), 20)]),
                     ("기울기와 한 점으로 식 구하기", [(g_equation(("ab", "pt")), 20)]),
                     ("두 점으로 식 구하기", [(g_equation(("two", "xint")), 20)]),
                     ("그래프 읽기", [(f_graph(), 20)]),
                     ("섞어서 연습", [(g_prop(), 10), (g_equation(), 10)])], 82808)
    if which == "lfe":
        return unit(G, "linear-functions-and-equations", 9, "[9수02-17] [9수02-18]",
                    "일차함수와 미지수가 2개인 일차방정식의 관계를 이해한다. 두 일차함수의 그래프를 통하여 연립일차방정식의 해를 이해한다.",
                    "일차함수와 일차방정식의 관계", "일차함수와 일차방정식",
                    "중학교 2학년 수학 일차함수와 일차방정식 문제: ax + by + c = 0의 그래프, x = p와 y = q의 그래프, 두 그래프의 교점과 연립방정식의 해, 해의 개수, 넓이까지 100문제와 정답·해설.",
                    "교점의 좌표 = 연립방정식의 해", "평행하면 해가 없고, 일치하면 해가 무수히 많아요.",
                    ["일차방정식 ax + by + c = 0 (b ≠ 0)의 그래프는 일차함수 y = −(a/b)x − c/b의 그래프와 같아요.",
                     "x = p의 그래프는 y축에 평행한 직선, y = q의 그래프는 x축에 평행한 직선이에요.",
                     "두 일차방정식의 그래프의 <b>교점의 좌표</b>가 연립방정식의 해예요.",
                     "두 그래프가 평행하면 해가 없고, 일치하면 해가 무수히 많아요."],
                    [("2x + y = 4", ["y = −2x + 4"], "기울기 −2, y절편 4"), ("y = x + 1, y = −x + 3의 교점", ["x + 1 = −x + 3"], "(1, 2)")],
                    [("x = 3의 그래프를 x축에 평행하다고 한다", "x = 3은 y축에 평행해요."),
                     ("ax + by = c를 y에 대하여 풀 때 부호를 놓친다", "by = −ax + c이므로 y = −(a/b)x + c/b"),
                     ("평행한 두 직선의 연립방정식 해를 1개라고 한다", "만나지 않으니 해가 없어요.")],
                    [("x = 2는 함수인가요?", "x = 2일 때 y가 여러 개이므로 y는 x의 함수가 아니에요."),
                     ("그래프로 푸는 것이 왜 좋은가요?", "해의 개수와 위치를 한눈에 볼 수 있어요.")],
                    [("일차방정식의 그래프", [(e_graph(("std",)), 20)]),
                     ("축에 평행한 직선", [(e_graph(("vert",)), 20)]),
                     ("교점과 연립방정식", [(e_graph(("cross", "count")), 20)]),
                     ("그래프로 둘러싸인 넓이", [(e_area(), 20)]),
                     ("섞어서 연습", [(e_graph(), 12), (e_area(), 8)])], 82809)
    raise ValueError(which)
