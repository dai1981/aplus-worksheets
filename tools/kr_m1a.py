# -*- coding: utf-8 -*-
"""
대한민국 중학교 1학년 수학（2022 개정）：수와 연산・변화와 관계の 9 単元
  prime  : 소인수분해（소수와 합성수、거듭제곱、약수의 개수、최대공약수와 최소공배수）[9수01-01] [9수01-02]
  intrat : 정수와 유리수（수직선、절댓값、대소 관계）[9수01-03] [9수01-04]
  addsub : 정수와 유리수의 덧셈과 뺄셈 [9수01-05]
  muldiv : 정수와 유리수의 곱셈과 나눗셈 [9수01-05]
  expr   : 문자와 식（곱셈 기호 생략、식의 값、일차식의 계산）[9수02-01] [9수02-02]
  eq     : 일차방정식（등식의 성질、이항、풀이）[9수02-03] [9수02-04]
  eqword : 일차방정식의 활용 [9수02-04]
  coord  : 좌표평면과 그래프 [9수02-05] [9수02-06]
  prop   : 정비례와 반비례 [9수02-07]
誤答は「1을 소수라고 한다」「약수의 개수를 지수의 곱으로 센다」「부호를 빠뜨린다（−3 − 5 = −2）」「−2²과 (−2)²를 같다고 한다」
「분배법칙에서 뒤의 항에 곱하지 않는다」「이항할 때 부호를 바꾸지 않는다」「x좌표와 y좌표를 바꾼다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_common import josa, Names, num, fr
from kr_mid import M, N, neg, par, sg, dec, P, sup, unit, kosy, kurve, fig, svg_wrap, text, line, INK, RED, BLUE, GREEN

R = random.Random(82701)
NM = Names(R)
G = "grade-7"
PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def isprime(n):
    return n > 1 and all(n % p for p in range(2, int(n ** 0.5) + 1))


def fac(n):
    out = {}
    p = 2
    while n > 1:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    return out


def fstr(f):
    return " × ".join("%d%s" % (p, sup(e) if e > 1 else "") for p, e in sorted(f.items()))


def ndiv(f):
    r = 1
    for e in f.values():
        r *= e + 1
    return r


# ------------------------------------------------------------------ 소인수분해
def p_prime():
    def mk():
        how = R.choice(["pick", "pick", "count", "fact"])
        if how == "pick":
            a = R.choice([p for p in PR if p < 60])
            bad = R.sample([1, 9, 15, 21, 27, 33, 39, 49, 51, 57, 25, 35, 45, 55, 91, 87], 3)
            return M("다음 중 <b>소수</b>는 무엇일까요?<br>%s" % ", ".join(map(str, sorted(bad + [a]))), a, bad,
                     "%d은 1과 자기 자신만을 약수로 가져요. %s은 소수가 아니에요. <b>%d</b>" % (a, ", ".join(map(str, sorted(bad))), a))
        if how == "count":
            lo = R.randint(1, 40)
            hi = lo + R.randint(10, 25)
            c = sum(1 for n in range(lo, hi + 1) if isprime(n))
            return N("%d 이상 %d 이하의 자연수 중에서 소수는 모두 몇 개일까요?" % (lo, hi), c, [c + 1, c - 1, c + 2, hi - lo + 1 - c],
                     "소수: %s → <b>%d개</b>" % (", ".join(str(n) for n in range(lo, hi + 1) if isprime(n)), c), f=lambda v: "%s개" % neg(v))
        F = [("1은 소수일까요, 합성수일까요?", "소수도 합성수도 아니에요", ["소수예요", "합성수예요", "소수이면서 합성수예요"], "1은 약수가 1개뿐이라 소수도 합성수도 아니에요."),
             ("짝수인 소수는 몇 개일까요?", "1개(2)", ["없어요", "2개", "무수히 많아요"], "2만 짝수인 소수예요."),
             ("합성수의 약수는 몇 개일까요?", "3개 이상", ["2개", "1개", "4개 이상"], "합성수는 약수가 3개 이상이에요."),
             ("가장 작은 합성수는 무엇일까요?", "4", ["1", "2", "6"], "1, 2, 3은 합성수가 아니에요. <b>4</b>"),
             ("모든 자연수에 대해 바르게 말한 것은?", "1, 소수, 합성수 중 하나예요", ["소수 아니면 합성수예요", "홀수는 모두 소수예요", "소수는 모두 홀수예요"], "1은 소수도 합성수도 아니에요.")]
        q, a, b, e = R.choice(F)
        return M(q, a, b, e)
    return mk


def p_power():
    def mk():
        how = R.choice(["write", "val", "write"])
        if how == "val":
            a, e = R.choice([(2, R.randint(3, 6)), (3, R.randint(2, 4)), (5, 3), (10, R.randint(2, 4)), (Fr(1, 2), 3), (Fr(2, 3), 2)])
            v = Fr(a) ** e
            return N("%s의 값은 얼마일까요?" % ((str(a) if Fr(a).denominator == 1 else "(%s)" % neg(a)) + sup(e)), v, [Fr(a) * e, Fr(a) ** (e - 1), Fr(a) + e, v + 1],
                     "%s를 %d번 곱해요. <b>%s</b>" % (neg(a), e, neg(v)))
        ps = R.sample([2, 3, 5, 7], 2)
        es = [R.randint(2, 4), R.randint(1, 3)]
        f = dict(zip(ps, es))
        prod = " × ".join(" × ".join([str(p)] * e) for p, e in sorted(f.items()))
        ok = fstr(f)
        bad = [" × ".join("%d%s" % (p, sup(e + 1) if e > 0 else "") for p, e in sorted(f.items())),
               "%d%s" % (math.prod(ps), sup(sum(es))), " + ".join("%d%s" % (p, sup(e) if e > 1 else "") for p, e in sorted(f.items())),
               " × ".join("%d%s" % (e, sup(p)) for p, e in sorted(f.items()))]
        return M("<b>%s</b>를 거듭제곱을 사용하여 나타내면?" % prod, ok, bad, "같은 수를 곱한 횟수를 지수로 써요. <b>%s</b>" % ok)
    return mk


def rand_fac(maxn=600):
    while True:
        f = {}
        for p in R.sample([2, 3, 5, 7, 11], R.randint(2, 3)):
            f[p] = R.randint(1, 3 if p < 5 else 2)
        n = math.prod(p ** e for p, e in f.items())
        if 12 <= n <= maxn:
            return n, f


def p_factor():
    def mk():
        n, f = rand_fac()
        ok = fstr(f)
        bad = []
        ks = sorted(f)
        for i in range(3):
            g = dict(f)
            k = R.choice(ks)
            g[k] = g[k] + R.choice([1, -1]) if g[k] > 1 else g[k] + 1
            bad.append(fstr(g))
        a = min(ks)
        bad.append("%d × %d" % (a, n // a))
        bad.append(fstr({k: v for k, v in f.items() if k != max(ks)}) + " × %d" % (max(ks) ** f[max(ks)]) if f[max(ks)] > 1 else None)
        return M("<b>%d</b>을 소인수분해하면?" % n, ok, bad, "작은 소수부터 차례로 나누어요. %d = <b>%s</b>" % (n, ok))
    return mk


def p_divisors():
    def mk():
        n, f = rand_fac(400)
        how = R.choice(["count", "count", "square"])
        if how == "count":
            c = ndiv(f)
            pr = math.prod(f.values())
            q = "<b>%s</b>의 약수의 개수는?" % (fstr(f) if R.random() < 0.5 else str(n))
            return N(q, c, [pr, sum(f.values()), c - 1, c + 1, c * 2],
                     "%s → (%s) = <b>%d개</b>" % (fstr(f), " × ".join("(%d + 1)" % e for e in f.values()), c), f=lambda v: "%s개" % neg(v))
        need = math.prod(p for p, e in f.items() if e % 2)
        if need == 1:
            return None
        return N("<b>%d</b>에 가장 작은 자연수를 곱하여 어떤 자연수의 제곱이 되게 하려고 해요. 곱하는 수는?" % n, need,
                 [max(f), min(f), need * 2, n], "%d = %s. 지수가 모두 짝수가 되도록 %d을 곱해요. <b>%d</b>" % (n, fstr(f), need, need))
    return mk


def p_gcdlcm():
    def mk():
        g = R.choice([2, 3, 4, 6, 8, 12, 9, 5, 10, 14, 15])
        a, b = R.sample(range(2, 10), 2)
        if math.gcd(a, b) != 1:
            return None
        x, y = g * a, g * b
        L = g * a * b
        how = R.choice(["g", "l", "gf", "lf"])
        if how in ("gf", "lf"):
            fx, fy = fac(x), fac(y)
            gf = {p: min(fx.get(p, 0), fy.get(p, 0)) for p in set(fx) | set(fy)}
            gf = {p: e for p, e in gf.items() if e}
            lf = {p: max(fx.get(p, 0), fy.get(p, 0)) for p in set(fx) | set(fy)}
            if not gf:
                return None
            if how == "gf":
                return M("두 수 <b>%s</b>, <b>%s</b>의 최대공약수를 소인수의 곱으로 나타내면?" % (fstr(fx), fstr(fy)), fstr(gf), [fstr(lf), fstr({**gf, min(gf): gf[min(gf)] + 1}), str(math.prod(p ** e for p, e in gf.items()))],
                         "공통인 소인수를 지수가 작은 쪽으로 곱해요. <b>%s</b>" % fstr(gf))
            return M("두 수 <b>%s</b>, <b>%s</b>의 최소공배수를 소인수의 곱으로 나타내면?" % (fstr(fx), fstr(fy)), fstr(lf), [fstr(gf), fstr({**lf, min(lf): lf[min(lf)] + 1}), fstr({**lf, max(lf): max(1, lf[max(lf)] - 1)})],
                     "모든 소인수를 지수가 큰 쪽으로 곱해요. <b>%s</b>" % fstr(lf))
        if how == "g":
            return N("<b>%d</b>과 <b>%d</b>의 최대공약수는?" % (x, y), g, [L, g * 2, a * b, math.gcd(x, y) // 2 if g % 2 == 0 else g + 1],
                     "%d = %s, %d = %s → 최대공약수 <b>%d</b>" % (x, fstr(fac(x)), y, fstr(fac(y)), g))
        return N("<b>%d</b>과 <b>%d</b>의 최소공배수는?" % (x, y), L, [x * y, g, L * 2, L // 2], "%d = %s, %d = %s → 최소공배수 <b>%d</b>" % (x, fstr(fac(x)), y, fstr(fac(y)), L))
    return mk


def p_word():
    def mk():
        how = R.choice(["share", "bus", "tile", "gear"])
        g = R.choice([4, 6, 8, 9, 12, 15])
        a, b = R.sample(range(2, 8), 2)
        if math.gcd(a, b) != 1:
            return None
        x, y = g * a, g * b
        if how == "share":
            return N("사탕 %d개와 초콜릿 %d개를 최대한 많은 학생에게 남김없이 똑같이 나누어 주려고 해요. 몇 명에게 나누어 줄 수 있을까요?" % (x, y), g,
                     [g * a * b, a + b, g // 2 if g % 2 == 0 else g + 1, a * b], "%d과 %d의 최대공약수 <b>%d명</b>" % (x, y, g), f=lambda v: "%s명" % neg(v))
        if how == "bus":
            p, q = R.sample([6, 8, 10, 12, 15, 18, 20], 2)
            L = p * q // math.gcd(p, q)
            return N("두 버스가 오전 8시에 동시에 출발했어요. 한 버스는 %d분, 다른 버스는 %d분마다 출발해요. 처음으로 다시 동시에 출발하는 것은 몇 분 후일까요?" % (p, q), L,
                     [p * q, math.gcd(p, q), L * 2, p + q], "%d과 %d의 최소공배수 <b>%d분 후</b>" % (p, q, L), f=lambda v: "%s분 후" % neg(v))
        if how == "tile":
            return N("가로 %d cm, 세로 %d cm인 직사각형 바닥을 가능한 한 큰 정사각형 타일로 빈틈없이 덮으려고 해요. 타일의 한 변의 길이는?" % (x, y), g,
                     [g * a * b, g // 2 if g % 2 == 0 else g + 1, a * b, a + b], "%d과 %d의 최대공약수 <b>%d cm</b>" % (x, y, g), f=lambda v: "%s cm" % neg(v))
        p, q = R.sample([12, 16, 18, 20, 24, 30], 2)
        L = p * q // math.gcd(p, q)
        return N("톱니 %d개인 톱니바퀴와 톱니 %d개인 톱니바퀴가 맞물려 있어요. 처음 맞물린 톱니가 다시 맞물리려면 첫째 톱니바퀴는 몇 바퀴 돌아야 할까요?" % (p, q), L // p,
                 [L // q, L, math.gcd(p, q), L // p + 1], "최소공배수 %d개의 톱니가 지나야 해요. %d ÷ %d = <b>%d바퀴</b>" % (L, L, p, L // p), f=lambda v: "%s바퀴" % neg(v))
    return mk


# ------------------------------------------------------------------ 정수와 유리수
SIT = [("영상 %d °C", "영하 %d °C"), ("%d원 이익", "%d원 손해"), ("해발 %d m", "해저 %d m"), ("지상 %d층", "지하 %d층"), ("%d kg 증가", "%d kg 감소"), ("%d점 득점", "%d점 실점")]


def r_sign():
    def mk():
        p, n = R.choice(SIT)
        a, b = R.randint(2, 30), R.randint(2, 30)
        if R.random() < 0.5:
            return M("<b>%s</b> +%d로 나타낼 때, <b>%s</b> 부호를 사용하여 나타내면?" % (josa(p % a, "을/를"), a, josa(n % b, "을/를")), "−%d" % b, ["+%d" % b, "−%d" % a, neg(b - a) if b != a else "0"],
                     "반대되는 양은 음의 부호를 붙여요. <b>−%d</b>" % b)
        return M("<b>%s</b> −%d로 나타낼 때, <b>%s</b> 부호를 사용하여 나타내면?" % (josa(n % a, "을/를"), a, josa(p % b, "을/를")), "+%d" % b, ["−%d" % b, "+%d" % a, "−%d" % a],
                 "반대되는 양은 양의 부호를 붙여요. <b>+%d</b>" % b)
    return mk


def r_classify():
    def mk():
        nums = [Fr(R.randint(-9, -1)), Fr(0), Fr(R.randint(1, 9)), Fr(R.randint(1, 7), R.choice([2, 3, 4, 5])) * R.choice([1, -1]),
                Fr(R.choice([-15, -6, 8, 10]), 2), Fr(R.randint(1, 9), 10) * R.choice([1, -1])]
        nums = [x for x in nums if not (x.denominator != 1 and x.denominator == 1)]
        R.shuffle(nums)
        shown = ", ".join(neg(x) if x.denominator == 1 or x.denominator != 10 else dec(x) for x in nums)
        kind = R.choice(["int", "nonint", "neg", "posint"])
        f = {"int": lambda x: x.denominator == 1, "nonint": lambda x: x.denominator != 1, "neg": lambda x: x < 0, "posint": lambda x: x.denominator == 1 and x > 0}[kind]
        c = sum(1 for x in nums if f(x))
        nm = {"int": "정수", "nonint": "정수가 아닌 유리수", "neg": "음수", "posint": "양의 정수(자연수)"}[kind]
        return N("다음 수 중 <b>%s</b>는 모두 몇 개일까요?<br>%s" % (nm, shown), c, [c + 1, c - 1, len(nums) - c, c + 2],
                 "%s: %s → <b>%d개</b>" % (nm, ", ".join(neg(x) if x.denominator != 10 else dec(x) for x in nums if f(x)) or "없음", c), f=lambda v: "%s개" % neg(v))
    return mk


def nline(pts, lo=-5, hi=5):
    u = 44
    W = (hi - lo) * u + 60
    X = lambda v: 30 + (float(v) - lo) * u
    s = [line(X(lo) - 14, 60, X(hi) + 14, 60, INK, 2.2)]
    for k in range(lo, hi + 1):
        s.append(line(X(k), 52, X(k), 68, INK, 1.8) + text(X(k), 92, neg(k), 16, weight=600))
    for v, nm in pts:
        s.append("<circle cx='%.1f' cy='60' r='7' fill='%s'/>" % (X(v), RED) + text(X(v), 36, nm, 18, col=RED))
    return fig(svg_wrap(int(W), 104, "".join(s), "수직선").replace("<svg ", "<svg data-pf='lg' ", 1))


def r_line():
    def mk():
        d = R.choice([1, 1, 2, 3, 4])
        v = Fr(R.randint(-4 * d, 4 * d), d)
        if v.denominator != d and d > 1:
            return None
        ok = neg(v)
        w = [neg(-v) if v else neg(1), neg(v + Fr(1, d)), neg(v - Fr(1, d)), neg(v + 1)]
        return M("수직선 위의 점 A가 나타내는 수는?%s" % nline([(v, "A")]), ok, w, "0을 기준으로 %s쪽으로 %s만큼 떨어져 있어요. <b>%s</b>" % ("오른" if v > 0 else "왼", neg(abs(v)), ok) if v else "점 A는 원점이에요. <b>0</b>")
    return mk


def r_abs():
    def mk():
        how = R.choice(["val", "both", "count", "far"])
        if how == "val":
            v = Fr(R.randint(-15, 15), R.choice([1, 1, 2, 3]))
            return N("|%s|의 값은?" % neg(v), abs(v), [-abs(v), v if v > 0 else -v + 1, 0 if v else 1], "절댓값은 원점으로부터의 거리예요. <b>%s</b>" % neg(abs(v)))
        if how == "both":
            a = R.randint(1, 12)
            return M("절댓값이 <b>%d</b>인 수를 모두 구하면?" % a, "+%d, −%d" % (a, a), ["+%d" % a, "−%d" % a, "0, %d" % a], "원점에서 거리가 %d인 수는 2개예요. <b>+%d, −%d</b>" % (a, a, a))
        if how == "count":
            a = R.randint(1, 6)
            le = R.random() < 0.5
            c = 2 * a + 1 if le else 2 * a - 1
            return N("절댓값이 %d %s인 정수는 모두 몇 개일까요?" % (a, "이하" if le else "미만"), c, [a, 2 * a, c + 2, a + 1],
                     "−%d부터 %d까지 → <b>%d개</b>" % (a if le else a - 1, a if le else a - 1, c), f=lambda v: "%s개" % neg(v))
        xs = list({Fr(R.randint(-9, 9), R.choice([1, 2])) for _ in range(6)})[:4]
        if len(xs) < 4 or len({abs(x) for x in xs}) < 4:
            return None
        big = max(xs, key=abs)
        return M("다음 중 절댓값이 가장 큰 수는?<br>%s" % ", ".join(neg(x) for x in xs), neg(big), [neg(x) for x in xs if x != big],
                 "원점에서 가장 멀리 떨어진 수예요. <b>%s</b>" % neg(big))
    return mk


def r_order():
    def mk():
        how = R.choice(["min", "max", "cmp", "ineq"])
        if how in ("min", "max"):
            xs = set()
            while len(xs) < 4:
                xs.add(Fr(R.randint(-12, 12), R.choice([1, 2, 3, 4])))
            xs = list(xs)
            a = min(xs) if how == "min" else max(xs)
            return M("다음 중 가장 %s 수는?<br>%s" % ("작은" if how == "min" else "큰", ", ".join(neg(x) for x in xs)), neg(a), [neg(x) for x in xs if x != a],
                     "음수는 절댓값이 클수록 작아요. <b>%s</b>" % neg(a))
        if how == "cmp":
            a, b = Fr(-R.randint(1, 5), R.randint(2, 5)), Fr(-R.randint(1, 5), R.randint(2, 5))
            if a == b:
                return None
            lo, hi = min(a, b), max(a, b)
            ok = "%s &lt; %s" % (neg(lo), neg(hi))
            return M("두 수의 대소 관계를 바르게 나타낸 것은?<br><b>%s</b>, <b>%s</b>" % (neg(a), neg(b)), ok,
                     ["%s &lt; %s" % (neg(hi), neg(lo)), "%s = %s" % (neg(a), neg(b)), "%s &gt; %s" % (neg(lo), neg(hi))],
                     "두 음수는 절댓값이 큰 쪽이 더 작아요. |%s| &gt; |%s| → <b>%s</b>" % (neg(lo), neg(hi), ok))
        a = R.randint(-6, 0)
        b = R.randint(1, 6)
        k1, k2 = R.choice([("이상", "≤"), ("초과", "&lt;")]), R.choice([("이하", "≤"), ("미만", "&lt;")])
        ok = "%s %s x %s %s" % (neg(a), k1[1], k2[1], b)
        alt1 = "%s %s x %s %s" % (neg(a), "&lt;" if k1[1] == "≤" else "≤", k2[1], b)
        alt2 = "%s %s x %s %s" % (neg(a), k1[1], "&lt;" if k2[1] == "≤" else "≤", b)
        alt3 = "%s %s x %s %s" % (b, k1[1], k2[1], neg(a))
        return M("'x는 %s %s이고 %d %s이다'를 부등호로 나타내면?" % (neg(a), k1[0], b, k2[0]), ok, [alt1, alt2, alt3],
                 "이상·이하는 ≤, 초과·미만은 &lt;예요. <b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 덧셈과 뺄셈
def rnum(kind):
    if kind == "int":
        return Fr(R.choice([x for x in range(-15, 16) if x]))
    if kind == "frac":
        return Fr(R.choice([x for x in range(-7, 8) if x]), R.choice([2, 3, 4, 5, 6]))
    return Fr(R.choice([x for x in range(-45, 46) if x]), 10)


def show(v, kind):
    return dec(v) if kind == "dec" else neg(v)


def as_(v, kind):
    s = show(v, kind)
    return "(%s)" % s if v < 0 else "(+%s)" % s


def a_calc(op, kind):
    def mk():
        a, b = rnum(kind), rnum(kind)
        if op == "+":
            v = a + b
            w = [a - b, (abs(a) + abs(b)) * (1 if a + b >= 0 else -1), -(a + b), b - a]
            e = "부호가 같으면 절댓값의 합에 공통 부호, 다르면 절댓값의 차에 절댓값이 큰 쪽 부호를 붙여요."
        else:
            v = a - b
            w = [a + b, b - a, -(abs(a) + abs(b)) if v > 0 else abs(a) + abs(b), -a - b]
            e = "빼는 수의 부호를 바꾸어 더해요. %s − %s = %s + %s" % (as_(a, kind), as_(b, kind), as_(a, kind), as_(-b, kind))
        f = (lambda x: show(x, kind))
        return M("%s %s %s =" % (as_(a, kind), op, as_(b, kind)), f(v), [f(x) for x in w if x != v], e + " <b>%s</b>" % f(v))
    return mk


def a_mixed():
    def mk():
        xs = [Fr(R.choice([x for x in range(-12, 13) if x])) for _ in range(3)]
        ops = [R.choice("+−") for _ in range(2)]
        v = xs[0]
        for o, x in zip(ops, xs[1:]):
            v = v + x if o == "+" else v - x
        t = "%s %s %s %s %s" % (neg(xs[0]), ops[0], par(xs[1]), ops[1], par(xs[2]))
        w0 = xs[0]
        for o, x in zip(ops, xs[1:]):
            w0 = w0 + x
        return N(t + " =", v, [w0, -v, v + 2, v - 2], "빼기는 부호를 바꾼 수의 덧셈으로 고쳐 차례로 계산해요. <b>%s</b>" % neg(v))
    return mk


def a_word():
    def mk():
        how = R.choice(["temp", "floor", "score", "dist"])
        if how == "temp":
            a, b = R.randint(-10, 8), R.randint(3, 15)
            c = R.choice(["올랐", "내려갔"])
            v = a + b if c == "올랐" else a - b
            return N("아침 기온이 %s °C였어요. 낮에 %d °C %s어요. 낮 기온은 몇 °C일까요?" % (neg(a), b, c), v, [a - b if c == "올랐" else a + b, -v, b - a],
                     "%s %s %d = <b>%s</b>" % (neg(a), "+" if c == "올랐" else "−", b, neg(v)), f=lambda x: "%s °C" % neg(x))
        if how == "floor":
            a, b = R.randint(-3, 12), R.randint(2, 10)
            v = a - b
            if v == 0 or a == 0:
                return None
            fl = lambda x: ("지상 %d층" % x) if x > 0 else ("지하 %d층" % -x)
            return M("엘리베이터가 %s에서 %d개 층을 내려갔어요. 지상 1층의 아래층은 지하 1층이에요. 도착한 층을 +, −로 나타내면? (지상 n층은 +n, 지하 n층은 −n)" % (fl(a), b),
                     neg(v), [neg(a + b), neg(-v), neg(v + 1)], "%s − %d = <b>%s</b>" % (neg(a), b, neg(v)))
        if how == "score":
            xs = [R.randint(-5, 8) for _ in range(4)]
            v = sum(xs)
            return N("퀴즈에서 맞히면 +, 틀리면 − 점수를 받아요. %s 받은 점수가 %s일 때 점수의 합은?" % (josa(NM.next(), "이/가"), ", ".join(sg(x) for x in xs)), v,
                     [sum(abs(x) for x in xs), v + 2, -v, v - 2], "%s = <b>%s</b>" % (" + ".join(par(x) for x in xs), neg(v)), f=lambda x: "%s점" % neg(x))
        a, b = R.randint(-9, -1), R.randint(1, 9)
        return N("수직선 위의 두 수 %s와 %d 사이의 거리는?" % (neg(a), b), b - a, [b + a, abs(a), b], "%d − (%s) = <b>%d</b>" % (b, neg(a), b - a))
    return mk


# ------------------------------------------------------------------ 곱셈과 나눗셈
def m_calc(kind):
    def mk():
        if kind == "mul":
            a, b = rnum(R.choice(["int", "frac"])), rnum(R.choice(["int", "frac"]))
            v = a * b
            return N("%s × %s =" % (par(a), par(b)), v, [-v, a + b, abs(a) * abs(b) if v < 0 else -abs(v) + 1], "부호가 같으면 +, 다르면 −. <b>%s</b>" % neg(v))
        if kind == "div":
            b = rnum(R.choice(["int", "frac"]))
            v = rnum(R.choice(["int", "frac"]))
            a = v * b
            if a.denominator > 12:
                return None
            return N("%s ÷ %s =" % (par(a), par(b)), v, [-v, a * b, 1 / v if v else None, v * 2], "나누는 수의 역수를 곱해요. %s × %s = <b>%s</b>" % (par(a), par(1 / b), neg(v)))
        xs = [Fr(R.choice([x for x in range(-6, 7) if x])) for _ in range(3)]
        v = xs[0] * xs[1] * xs[2]
        c = sum(1 for x in xs if x < 0)
        return N("%s =" % " × ".join(par(x) for x in xs), v, [-v, sum(xs), v + 1],
                 "음수가 %d개(%s)이므로 부호는 %s예요. <b>%s</b>" % (c, "짝수" if c % 2 == 0 else "홀수", "+" if v > 0 else "−", neg(v)))
    return mk


def m_power():
    def mk():
        a = R.randint(2, 5)
        e = R.randint(2, 4)
        how = R.choice(["neg_par", "neg_no", "mix"])
        if how == "neg_par":
            v = Fr(-a) ** e
            return N("(−%d)%s의 값은?" % (a, sup(e)), v, [-v, -a * e, a * e], "−%d을 %d번 곱해요. 음수를 %s번 곱하면 %s. <b>%s</b>" % (a, e, "짝수" if e % 2 == 0 else "홀수", "+" if v > 0 else "−", neg(v)))
        if how == "neg_no":
            v = -Fr(a) ** e
            return N("−%d%s의 값은?" % (a, sup(e)), v, [-v, -a * e, Fr(-a) ** (e + 1)], "%d%s을 먼저 계산하고 −를 붙여요. <b>%s</b>" % (a, sup(e), neg(v)))
        k = R.randint(1, 9)
        v = Fr(-1) ** k
        n = R.randint(2, 9)
        tot = v * n
        return N("(−1)%s × %d의 값은?" % (sup(k), n), tot, [-tot, -n * k, n * k], "(−1)%s = %s → <b>%s</b>" % (sup(k), neg(v), neg(tot)))
    return mk


def m_order():
    def mk():
        a, b, c, d = R.randint(2, 4), R.choice([x for x in range(-6, 7) if x]), R.choice([2, 3, 4, 6]), R.choice([x for x in range(-5, 6) if x])
        how = R.choice([0, 1, 2])
        if how == 0:
            v = Fr(-2) ** a + Fr(b) * c
            t = "(−2)%s + %s × %d" % (sup(a), par(b), c)
            w = [(Fr(-2) ** a + b) * c, -Fr(2) ** a + b * c, v + 2]
            st = "거듭제곱 → 곱셈 → 덧셈 순서로: %s + %s = <b>%s</b>" % (neg(Fr(-2) ** a), par(Fr(b) * c), neg(v))
        elif how == 1:
            x = Fr(b) * c
            v = x / c - d
            t = "%s ÷ %d − %s" % (neg(x), c, par(d))
            w = [x / (c - d), x / c + d, -v]
            st = "나눗셈을 먼저: %s − %s = <b>%s</b>" % (neg(x / c), par(d), neg(v))
        else:
            v = Fr(b) - Fr(c) * (Fr(d) - 2)
            t = "%s − %d × (%s − 2)" % (neg(b), c, neg(d))
            w = [(Fr(b) - c) * (Fr(d) - 2), Fr(b) - c * d - 2, v + 4]
            st = "괄호 안 → 곱셈 → 뺄셈: %d × %s = %s, <b>%s</b>" % (c, par(Fr(d) - 2), neg(c * (Fr(d) - 2)), neg(v))
        return N(t + " =", v, w, st)
    return mk


def m_word():
    def mk():
        how = R.choice(["recip", "law", "temp"])
        if how == "recip":
            v = Fr(R.choice([x for x in range(-7, 8) if x]), R.randint(2, 7))
            return N("%s의 역수는?" % neg(v), 1 / v, [-1 / v, -v, v], "곱해서 1이 되는 수예요. 부호는 그대로. <b>%s</b>" % neg(1 / v))
        if how == "law":
            F = [("(−25) × 7 × 4를 계산할 때 쓰면 편한 법칙은?", "곱셈의 교환법칙과 결합법칙", ["분배법칙만", "덧셈의 교환법칙", "등식의 성질"], "(−25) × 4를 먼저 곱하면 −100이 돼요."),
                 ("99 × (−7)을 (100 − 1) × (−7)로 계산할 때 쓴 법칙은?", "분배법칙", ["교환법칙", "결합법칙", "역수의 성질"], "a × (b + c) = a × b + a × c")]
            q, a, b, e = R.choice(F)
            return M(q, a, b, e)
        a = R.randint(2, 6)
        h = R.randint(2, 8)
        v = -a * h
        return N("어느 산에서 높이가 1 km 높아질 때마다 기온이 %d °C씩 내려가요. 높이가 %d km 높아지면 기온의 변화는?" % (a, h), v, [-v, -a - h, a * h * 10], "(−%d) × %d = <b>%s °C</b>" % (a, h, neg(v)),
                 f=lambda x: "%s °C" % neg(x))
    return mk


# ------------------------------------------------------------------ 문자와 식
def e_notation():
    def mk():
        how = R.choice(["mul", "div", "neg1", "mix"])
        a = R.randint(2, 9)
        if how == "mul":
            ok = "%dab" % a
            return M("<b>b × %d × a</b>를 곱셈 기호를 생략하여 나타내면?" % a, ok, ["ab%d" % a, "%dba" % a, "%d + ab" % a], "수를 문자 앞에, 문자는 알파벳 순서로 써요. <b>%s</b>" % ok)
        if how == "div":
            ok = fr("x", a)
            return M("<b>x ÷ %d</b>를 나눗셈 기호를 생략하여 나타내면?" % a, ok, [fr(a, "x"), "%dx" % a, "x − %d" % a], "나눗셈은 분수로 나타내요. <b>%s</b>" % ok)
        if how == "neg1":
            ok = "−x" + sup(2) + "y"
            return M("<b>x × y × (−1) × x</b>를 곱셈 기호를 생략하여 나타내면?", ok, ["−1x" + sup(2) + "y", "x" + sup(2) + "y", "−2xy"], "1은 생략하고 같은 문자는 거듭제곱으로. <b>%s</b>" % ok)
        b = R.randint(2, 9)
        ok = "%da − %s" % (a, fr("b", b))
        return M("<b>a × %d − b ÷ %d</b>를 기호를 생략하여 나타내면?" % (a, b), ok, ["%da − %db" % (a, b), "a%d − %s" % (a, fr(b, "b")), "%s" % fr("%da − b" % a, b)],
                 "<b>%s</b>" % ok)
    return mk


def e_write():
    def mk():
        how = R.choice(["buy", "speed", "rect", "pct", "digit"])
        if how == "buy":
            p, q = R.randint(2, 5), R.randint(2, 4)
            ok = "(%da + %db)원" % (p, q)
            return M("한 개에 a원인 연필 %d자루와 한 권에 b원인 공책 %d권의 값을 식으로 나타내면?" % (p, q), ok, ["%dab원" % (p * q), "(a + b)원", "(%da + %db)원" % (q, p)], "<b>%s</b>" % ok)
        if how == "speed":
            h = R.randint(2, 5)
            ok = "%dx km" % h
            return M("시속 x km로 %d시간 동안 간 거리는?" % h, ok, [fr("x", h) + " km", "(x + %d) km" % h, fr(h, "x") + " km"], "거리 = 속력 × 시간. <b>%s</b>" % ok)
        if how == "rect":
            ok = "2(a + b) cm"
            return M("가로 a cm, 세로 b cm인 직사각형의 둘레는?", ok, ["ab cm", "(a + b) cm", "2ab cm"], "둘레 = 2 × (가로 + 세로). <b>%s</b>" % ok)
        if how == "pct":
            p = R.choice([10, 20, 30, 15, 25])
            ok = "%sx원" % dec(Fr(100 - p, 100))
            return M("정가 x원인 물건을 %d%% 할인한 가격은?" % p, ok, ["%sx원" % dec(Fr(p, 100)), "(x − %d)원" % p, "%sx원" % dec(Fr(100 + p, 100))],
                     "x − %s x = <b>%s</b>" % (dec(Fr(p, 100)), ok))
        ok = "10a + b"
        return M("십의 자리 숫자가 a, 일의 자리 숫자가 b인 두 자리 자연수는?", ok, ["ab", "a + b", "10b + a"], "<b>%s</b>" % ok)
    return mk


def e_value():
    def mk():
        x = R.choice([-3, -2, -1, 2, 3, Fr(1, 2), Fr(-1, 3)])
        a, b, c = R.randint(1, 4), R.choice([-5, -3, -2, 2, 3, 4]), R.randint(-6, 6)
        how = R.choice([0, 1, 2])
        if how == 0:
            v = a * Fr(x) ** 2 + b * Fr(x) + c
            t = P([(a, "x" + sup(2)), (b, "x"), (c, "")])
            w = [-a * Fr(x) ** 2 + b * Fr(x) + c, a * Fr(abs(x)) ** 2 + b * abs(Fr(x)) + c, (a * Fr(x)) ** 2 + b * Fr(x) + c]
        elif how == 1:
            y = R.choice([-2, -1, 1, 3])
            v = a * Fr(x) - b * y
            t = "%dx − %sy, y = %s" % (a, par(b) if b < 0 else str(b), neg(y))
            w = [a * Fr(x) + b * y, a * Fr(x) - b * (-y), -v]
        else:
            if Fr(x) == 0:
                return None
            c = c or 6
            v = Fr(c) / Fr(x)
            t = fr(c, "x") if c > 0 else "−" + fr(-c, "x")
            w = [Fr(c if c else 6) * Fr(x), -v, v + 1]
        return N("x = %s일 때, %s의 값은?" % (neg(x), t), v, w, "x 대신 %s를 넣어 계산해요(음수는 괄호). <b>%s</b>" % (par(x), neg(v)))
    return mk


def e_linear():
    def mk():
        how = R.choice(["dist", "combine", "sub", "frac"])
        a, b, c, d = R.choice([2, 3, 4, -2, -3]), R.choice([x for x in range(-6, 7) if x]), R.choice([2, 3, -2, -1]), R.choice([x for x in range(-5, 6) if x])
        if how == "dist":
            ok = P([(a * c, "x"), (a * d, "")])
            return M("%s(%s)를 간단히 하면?" % (neg(a), P([(c, "x"), (d, "")])), ok, [P([(a * c, "x"), (d, "")]), P([(-a * c, "x"), (a * d, "")]), P([(a * c, "x"), (-a * d, "")])],
                     "괄호 안의 각 항에 %s를 곱해요. <b>%s</b>" % (neg(a), ok))
        if how == "combine":
            p, q = R.choice([x for x in range(-7, 8) if x]), R.choice([x for x in range(-7, 8) if x])
            ok = P([(p + q, "x"), (b + d, "")])
            return M("%s + (%s)를 간단히 하면?" % (P([(p, "x"), (b, "")]), P([(q, "x"), (d, "")])), ok, [P([(p + q + b + d, "x")]), P([(p - q, "x"), (b - d, "")]), P([(p + q, "x"), (b - d, "")])],
                     "동류항끼리 모아요. <b>%s</b>" % ok)
        if how == "sub":
            ok = P([(a * c - 1, "x"), (a * d - b, "")])
            t = "%s(%s) − (%s)" % (neg(a), P([(c, "x"), (d, "")]), P([(1, "x"), (b, "")]))
            return M("%s를 간단히 하면?" % t, ok, [P([(a * c + 1, "x"), (a * d + b, "")]), P([(a * c - 1, "x"), (a * d + b, "")]), P([(a * c - 1, "x"), (d - b, "")])],
                     "빼는 식의 각 항의 부호를 바꾸어요. <b>%s</b>" % ok)
        k = R.choice([2, 3, 4])
        p = R.choice([1, 3, 5, -1])
        ok = P([(1, "x"), (Fr(p, k), "")])
        return M("(%s) ÷ %d를 간단히 하면?" % (P([(k, "x"), (p, "")]), k), ok,
                 [P([(k, "x"), (Fr(p, k), "")]), P([(1, "x"), (p, "")]), P([(Fr(1, k), "x"), (Fr(p, k), "")])], "각 항을 %d로 나누어요. <b>%s</b>" % (k, ok))
    return mk


def e_like():
    def mk():
        base = R.choice(["x", "a"])
        good = ["%d%s" % (R.randint(2, 7), base), "−%s" % base, fr(base, R.randint(2, 5))]
        cands = ["%d%s" % (R.randint(2, 7), base + sup(2)), "%d%sy" % (R.randint(2, 5), base), fr(R.randint(2, 5), base), "%d" % R.randint(2, 9)]
        g = R.choice(good)
        return M("<b>%s</b>와 동류항인 것은?" % P([(R.choice([-7, -5, -3, -2, 2, 3, 4, 6, 8]), base + (sup(2) if R.random() < 0.3 else ""))]).replace(sup(2), ""), g, R.sample(cands, 3),
                 "문자와 차수가 모두 같아야 동류항이에요. 상수항, 분모에 문자가 있는 항, %s², %sy는 동류항이 아니에요. <b>%s</b>" % (base, base, g))
    return mk


# ------------------------------------------------------------------ 일차방정식
def solve_kind(kind):
    """ax + b = cx + d 꼴：해 x"""
    while True:
        x = R.randint(-6, 6)
        if kind == "basic":
            a = R.choice([2, 3, 4, 5, -2, -3])
            b = R.randint(-9, 9)
            return x, "%s = %s" % (P([(a, "x"), (b, "")]), neg(a * x + b)), [x + 1, -x, Fr(a * x + b + b, a), Fr(a * x + b, a) + b], "%s = %s, x = <b>%s</b>" % (P([(a, "x")]), neg(a * x), neg(x))
        if kind == "both":
            a, c = R.sample([2, 3, 4, 5, -1, -2, 6], 2)
            b = R.randint(-9, 9)
            d = (a - c) * x + b
            if (a - c) == 0:
                continue
            return x, "%s = %s" % (P([(a, "x"), (b, "")]), P([(c, "x"), (d, "")])), [-x, Fr(d + b, a - c), Fr(d - b, a + c) if a + c else x + 2, x + 1], \
                "이항하면 %s = %s, x = <b>%s</b>" % (P([(a - c, "x")]), neg(d - b), neg(x))
        if kind == "paren":
            k = R.choice([2, 3, -2])
            p = R.randint(-5, 5)
            c = R.choice([1, 2, -1])
            rhs = k * (x + p) - c * x
            if k - c == 0:
                continue
            return x, "%s(x %s %d) = %s" % (neg(k), "+" if p >= 0 else "−", abs(p), P([(c, "x"), (rhs, "")])), [-x, x + p, Fr(rhs - p, k - c) if k != c else x + 1, x - 1], \
                "괄호를 풀어요: %s = %s → x = <b>%s</b>" % (P([(k, "x"), (k * p, "")]), P([(c, "x"), (rhs, "")]), neg(x))
        if kind == "frac":
            m = R.choice([2, 3, 4])
            n = R.choice([2, 3, 6])
            if m == n:
                continue
            # x/m + c = x/n  → x(1/m − 1/n) = −c
            co = Fr(1, m) - Fr(1, n)
            c = -co * x
            if c.denominator != 1 or c == 0 or x == 0:
                continue
            return x, "%s %s %s = %s" % (fr("x", m), "+" if c > 0 else "−", neg(abs(c)), fr("x", n)), [-x, x * 2, c, x + m], \
                "양변에 %d을 곱해 정수로 만들어요. x = <b>%s</b>" % (m * n // math.gcd(m, n), neg(x))
        if kind == "dec":
            a = Fr(R.choice([2, 3, 5]), 10)
            b = Fr(R.randint(-9, 9), 10)
            rhs = a * x + b
            return x, "%sx %s %s = %s" % (dec(a), "+" if b >= 0 else "−", dec(abs(b)), dec(rhs)), [x * 10, -x, Fr(x, 10), x + 1], \
                "양변에 10을 곱해요: %dx %s %d = %s → x = <b>%s</b>" % (int(a * 10), "+" if b >= 0 else "−", abs(int(b * 10)), neg(rhs * 10), neg(x))


def q_solve(kinds):
    def mk():
        x, eq, w, e = solve_kind(R.choice(kinds))
        return N("일차방정식 <b>%s</b>의 해는?" % eq, x, w, e, f=lambda v: "x = %s" % neg(v))
    return mk


def q_eqconcept():
    def mk():
        how = R.choice(["sol", "ident", "prop", "trans"])
        if how == "sol":
            x = R.randint(-4, 4)
            eqs = []
            a = R.choice([2, 3, -2])
            b = R.randint(-5, 5)
            good = "%s = %s" % (P([(a, "x"), (b, "")]), neg(a * x + b))
            for _ in range(6):
                a2, b2 = R.choice([2, 3, -1, 4]), R.randint(-5, 5)
                eqs.append("%s = %s" % (P([(a2, "x"), (b2, "")]), neg(a2 * x + b2 + R.choice([1, -1, 2]))))
            return M("x = %s가 해인 방정식은?" % neg(x), good, eqs, "x에 %s를 대입해 등식이 참인 것을 찾아요. <b>%s</b>" % (par(x), good))
        if how == "ident":
            a, b = R.randint(2, 5), R.randint(1, 6)
            ok = "%s = %s" % (P([(a, "x"), (a * b, "")]), "%d(x + %d)" % (a, b))
            return M("다음 중 <b>항등식</b>은?", ok, ["%s = %d" % (P([(a, "x"), (b, "")]), a + b), "%s = %s" % (P([(a, "x")]), P([(a, "x"), (1, "")])), "%s = %s" % (P([(1, "x"), (b, "")]), P([(2, "x")]))],
                     "x에 어떤 값을 넣어도 항상 참인 등식이에요. <b>%s</b>" % ok)
        if how == "prop":
            F = [("a = b이면 a + 3 = b + 3이다.", "옳아요"), ("a = b이면 a − 5 = b − 5이다.", "옳아요"), ("a = b이면 4a = 4b이다.", "옳아요"),
                 ("a = b이면 a ÷ 0 = b ÷ 0이다.", "옳지 않아요(0으로는 나눌 수 없어요)"), ("2a = 6b이면 a = 3b이다.", "옳아요"),
                 ("a = b이면 a + 1 = b − 1이다.", "옳지 않아요(양변에 같은 수를 더해야 해요)")]
            q, a = R.choice(F)
            return M("등식의 성질로 바르게 판단한 것은?<br>%s" % q, a, [x for x in ("옳아요", "옳지 않아요(0으로는 나눌 수 없어요)", "옳지 않아요(양변에 같은 수를 더해야 해요)", "옳지 않아요(곱셈은 할 수 없어요)") if x != a],
                     "등식의 양변에 같은 수를 더하거나 빼거나 곱하거나 0이 아닌 같은 수로 나누어도 등식은 성립해요. <b>%s</b>" % a)
        a, b, c = R.choice([2, 3, 5]), R.randint(1, 9), R.randint(-9, 9)
        ok = "%s = %s" % (P([(a, "x")]), neg(c - b))
        return M("<b>%s = %s</b>에서 %d를 이항하면?" % (P([(a, "x"), (b, "")]), neg(c), b), ok, ["%s = %s" % (P([(a, "x")]), neg(c + b)), "%s = %s" % (P([(a, "x")]), neg(b - c)), "x = %s" % neg(c - b)],
                 "한 변의 항을 부호를 바꾸어 다른 변으로 옮겨요. <b>%s</b>" % ok)
    return mk


def q_word(kinds=("num", "consec", "age", "price", "speed", "share")):
    def mk():
        how = R.choice(kinds)
        if how == "num":
            x = R.randint(3, 20)
            a, b = R.randint(2, 5), R.randint(1, 15)
            return N("어떤 수의 %d배에 %d을 더하면 %d이 돼요. 어떤 수는?" % (a, b, a * x + b), x, [Fr(a * x + b + b, a), x + 1, a * x, Fr(a * x + b, a)],
                     "%dx + %d = %d → x = <b>%d</b>" % (a, b, a * x + b, x))
        if how == "consec":
            n = R.choice([3])
            x = R.randint(5, 40)
            s = 3 * x + 3
            return N("연속하는 세 자연수의 합이 %d이에요. 가장 큰 수는?" % s, x + 2, [x, x + 1, x + 3], "x + (x + 1) + (x + 2) = %d → x = %d, 가장 큰 수는 <b>%d</b>" % (s, x, x + 2))
        if how == "age":
            c = R.randint(8, 14)
            p = R.randint(36, 46)
            k = R.choice([2, 3])
            y = (p - k * c)
            if y % (k - 1):
                return None
            y //= (k - 1)
            if y <= 0 or y > 30:
                return None
            return N("어머니는 %d살, 아들은 %d살이에요. 어머니의 나이가 아들 나이의 %d배가 되는 것은 몇 년 후일까요?" % (p, c, k), y, [y + 1, y - 1, p - c, k * c],
                     "%d + x = %d(%d + x) → x = <b>%d</b>년 후" % (p, k, c, y), f=lambda v: "%s년 후" % neg(v))
        if how == "price":
            a, b = R.choice([500, 600, 700, 800]), R.choice([1000, 1200, 1500])
            n = R.randint(6, 12)
            x = R.randint(1, n - 1)
            tot = a * (n - x) + b * x
            return N("한 개에 %d원인 과자와 %d원인 음료수를 합하여 %d개 사고 %s원을 냈어요. 음료수는 몇 개 샀을까요?" % (a, b, n, num(tot)), x, [n - x, x + 1, x - 1 if x > 1 else x + 2],
                     "%d(%d − x) + %dx = %d → x = <b>%d</b>" % (a, n, b, tot, x), f=lambda v: "%s개" % neg(v))
        if how == "speed":
            t = R.choice(["round", "meet", "catch"])
            if t == "round":
                who, v1, v2, d = R.choice([("걸었", 2, 3, 6), ("걸었", 3, 6, 6), ("걸었", 3, 6, 12), ("걸었", 4, 6, 12), ("자전거를 탔", 10, 15, 30),
                                           ("자전거를 탔", 12, 18, 36), ("자동차로 갔", 40, 60, 120), ("자동차로 갔", 60, 90, 180), ("자동차로 갔", 30, 60, 120)])
                tt = Fr(d, v1) + Fr(d, v2)
                return N("두 지점 사이를 갈 때는 시속 %d km, 올 때는 시속 %d km로 %s더니 모두 %s시간이 걸렸어요. 두 지점 사이의 거리는?" % (v1, v2, who, neg(tt)), d,
                         [d * 2, v1 * v2, tt * v1, Fr(d, 2)], "%s + %s = %s → x = <b>%d km</b>" % (fr("x", v1), fr("x", v2), neg(tt), d), f=lambda v: "%s km" % neg(v))
            if t == "meet":
                a1, b1 = R.choice([(60, 40), (70, 50), (80, 60), (50, 30), (65, 55)])
                m = R.randint(5, 20)
                D = (a1 + b1) * m
                return N("%s m 떨어진 두 사람이 서로를 향해 동시에 출발했어요. 한 사람은 분속 %d m, 다른 사람은 분속 %d m로 걸으면 몇 분 후에 만날까요?" % (num(D), a1, b1), m,
                         [Fr(D, a1 - b1), m + 2, Fr(D, a1), m * 2], "(%d + %d)x = %s → x = <b>%d분 후</b>" % (a1, b1, num(D), m), f=lambda v: "%s분 후" % neg(v) if Fr(v).denominator == 1 else None)
            a1, b1 = R.choice([(60, 80), (50, 70), (60, 90), (40, 60), (50, 75)])
            k = R.choice([5, 10, 15, 20])
            x = Fr(a1 * k, b1 - a1)
            if x.denominator != 1:
                return None
            return N("동생이 분속 %d m로 집을 나선 지 %d분 후에 형이 분속 %d m로 같은 길을 따라갔어요. 형은 출발한 지 몇 분 후에 동생을 만날까요?" % (a1, k, b1), x,
                     [x + k, Fr(a1 * k, b1 + a1), x * 2, k], "%d(x + %d) = %dx → x = <b>%s분 후</b>" % (a1, k, b1, neg(x)), f=lambda v: "%s분 후" % neg(v) if Fr(v).denominator == 1 else None)
        n = R.randint(5, 12)
        a = R.randint(3, 6)
        r = R.randint(1, 8)
        tot = a * n + r
        b = a + 1
        sh = b * n - tot
        if sh <= 0:
            return None
        return N("학생들에게 사탕을 %d개씩 나누어 주면 %d개가 남고, %d개씩 나누어 주면 %d개가 모자라요. 학생은 몇 명일까요?" % (a, r, b, sh), n, [n + 1, n - 1, tot, r + sh + 1],
                 "%dx + %d = %dx − %d → x = <b>%d</b>" % (a, r, b, sh, n), f=lambda v: "%s명" % neg(v))
    return mk


# ------------------------------------------------------------------ 좌표평면과 그래프
def c_read():
    def mk():
        x, y = R.randint(-4, 4), R.randint(-4, 4)
        if x == 0 or y == 0:
            return None
        ok = "(%s, %s)" % (neg(x), neg(y))
        return M("좌표평면 위의 점 P의 좌표는?%s" % kosy(pts=[(x, y, "P")]), ok, ["(%s, %s)" % (neg(y), neg(x)), "(%s, %s)" % (neg(-x), neg(y)), "(%s, %s)" % (neg(x), neg(-y))],
                 "x좌표를 먼저, y좌표를 나중에 써요. <b>%s</b>" % ok)
    return mk


def c_quad():
    def mk():
        how = R.choice(["pt", "sign", "sym"])
        Q = {(1, 1): "제1사분면", (-1, 1): "제2사분면", (-1, -1): "제3사분면", (1, -1): "제4사분면"}
        if how == "pt":
            x, y = R.choice([x for x in range(-9, 10) if x]), R.choice([x for x in range(-9, 10) if x])
            k = Q[(1 if x > 0 else -1, 1 if y > 0 else -1)]
            return M("점 (%s, %s)는 어느 사분면 위의 점일까요?" % (neg(x), neg(y)), k, [v for v in Q.values() if v != k], "x좌표 %s, y좌표 %s → <b>%s</b>" % ("양수" if x > 0 else "음수", "양수" if y > 0 else "음수", k))
        if how == "sign":
            sx, sy = R.choice(list(Q))
            k = Q[(-sx, sy)]
            return M("점 (a, b)가 %s 위의 점일 때, 점 (−a, b)는 어느 사분면 위의 점일까요?" % Q[(sx, sy)], k, [v for v in Q.values() if v != k],
                     "a는 %s, b는 %s → −a는 %s. <b>%s</b>" % ("양수" if sx > 0 else "음수", "양수" if sy > 0 else "음수", "음수" if sx > 0 else "양수", k))
        x, y = R.choice([x for x in range(-7, 8) if x]), R.choice([x for x in range(-7, 8) if x])
        ax = R.choice(["x축", "y축", "원점"])
        p = {"x축": (x, -y), "y축": (-x, y), "원점": (-x, -y)}[ax]
        ok = "(%s, %s)" % (neg(p[0]), neg(p[1]))
        alts = [(x, -y), (-x, y), (-x, -y), (y, x)]
        return M("점 (%s, %s)와 <b>%s</b>에 대하여 대칭인 점의 좌표는?" % (neg(x), neg(y), ax), ok, ["(%s, %s)" % (neg(a), neg(b)) for a, b in alts if (a, b) != p],
                 "%s에 대칭이면 %s의 부호가 바뀌어요. <b>%s</b>" % (ax, {"x축": "y좌표", "y축": "x좌표", "원점": "두 좌표 모두"}[ax], ok))
    return mk


def c_area():
    def mk():
        pts = [(R.randint(-4, -1), R.randint(-4, -1)), (R.randint(1, 4), R.randint(-4, -1)), (R.randint(-3, 3), R.randint(1, 4))]
        (x1, y1), (x2, y2), (x3, y3) = pts
        if y1 != y2:
            pts[1] = (x2, y1)
            y2 = y1
        A = Fr(abs((x2 - x1) * (y3 - y1)), 2)
        return N("세 점 A(%s, %s), B(%s, %s), C(%s, %s)를 꼭짓점으로 하는 삼각형 ABC의 넓이는?%s" % (neg(x1), neg(y1), neg(x2), neg(y2), neg(x3), neg(y3), kosy(pts=[(x1, y1, "A"), (x2, y2, "B"), (x3, y3, "C")])),
                 A, [A * 2, A + 1, abs(x2 - x1) + abs(y3 - y1)], "밑변 %d, 높이 %d → %s × %d × %d = <b>%s</b>" % (abs(x2 - x1), abs(y3 - y1), fr(1, 2), abs(x2 - x1), abs(y3 - y1), neg(A)))
    return mk


def c_graph():
    def mk():
        # 집에서 공원까지 갔다가 쉬고 돌아오는 그래프（시간-거리）
        t1 = R.choice([10, 15, 20])
        d = R.choice([800, 1000, 1200, 1500])
        rest = R.choice([10, 15, 20])
        t2 = t1 + rest
        t3 = t2 + R.choice([15, 20, 25])
        xs = [0, t1, t2, t3]
        ys = [0, d, d, 0]

        def f(t):
            for i in range(3):
                if xs[i] <= t <= xs[i + 1]:
                    return ys[i] + (ys[i + 1] - ys[i]) * (t - xs[i]) / (xs[i + 1] - xs[i])
            return None
        g = kurve([(f, BLUE, "")], (0, t3 + 5, 5), (0, d + 200, 200 if d <= 1000 else 300), label="시간과 거리의 그래프")
        how = R.choice(["rest", "far", "back", "speed"])
        if how == "rest":
            return N("지우가 집에서 공원에 갔다가 돌아왔어요. 그래프에서 x는 출발 후 시간(분), y는 집에서 떨어진 거리(m)예요. 공원에서 머문 시간은?%s" % g, rest,
                     [t1, t2, t3 - t2], "그래프가 수평인 구간이 머문 시간이에요. %d − %d = <b>%d분</b>" % (t2, t1, rest), f=lambda v: "%s분" % neg(v))
        if how == "far":
            return N("그래프에서 x는 출발 후 시간(분), y는 집에서 떨어진 거리(m)예요. 집에서 공원까지의 거리는?%s" % g, d, [d * 2, d // 2, t1 * 10],
                     "가장 높은 곳의 y좌표예요. <b>%s m</b>" % num(d), f=lambda v: "%s m" % num(v))
        if how == "back":
            return N("그래프에서 x는 출발 후 시간(분), y는 집에서 떨어진 거리(m)예요. 공원에서 집으로 돌아오는 데 걸린 시간은?%s" % g, t3 - t2,
                     [t3, t1, rest], "%d − %d = <b>%d분</b>" % (t3, t2, t3 - t2), f=lambda v: "%s분" % neg(v))
        sp = Fr(d, t1)
        return N("그래프에서 x는 출발 후 시간(분), y는 집에서 떨어진 거리(m)예요. 공원에 갈 때 1분에 몇 m씩 걸었을까요?%s" % g, sp,
                 [Fr(d, t3), sp * 2, Fr(d, t2)], "%s ÷ %d = <b>%s m</b>" % (num(d), t1, neg(sp)), f=lambda v: "%s m" % neg(v) if Fr(v).denominator == 1 else None)
    return mk


# ------------------------------------------------------------------ 정비례와 반비례
def pr_basic():
    def mk():
        how = R.choice(["dir", "inv", "which"])
        a = R.choice([x for x in range(-6, 7) if x and abs(x) != 1])
        if how == "dir":
            x0 = R.randint(1, 4) * R.choice([1, -1])
            x1 = R.choice([x for x in range(-6, 7) if x and x != x0])
            return N("y가 x에 정비례하고, x = %s일 때 y = %s이에요. x = %s일 때 y의 값은?" % (neg(x0), neg(a * x0), neg(x1)), a * x1,
                     [Fr(a * x0 * x0, x1), a * x1 + 1, -a * x1, a + x1], "y = %dx → y = <b>%s</b>" % (a, neg(a * x1)) if a > 0 else "y = −%dx → y = <b>%s</b>" % (-a, neg(a * x1)))
        if how == "inv":
            k = a * R.choice([2, 3, 4, 6])
            x0 = R.choice([d for d in range(1, 13) if k % d == 0]) * R.choice([1, -1])
            x1 = R.choice([d for d in range(1, 13) if k % d == 0 and d != abs(x0)]) * R.choice([1, -1])
            return N("y가 x에 반비례하고, x = %s일 때 y = %s이에요. x = %s일 때 y의 값은?" % (neg(x0), neg(Fr(k, x0)), neg(x1)), Fr(k, x1),
                     [Fr(k, x0) * x1 / x0, -Fr(k, x1), Fr(x1, k), Fr(k, x0) + x1], "y = %s → y = <b>%s</b>" % (fr(neg(k), "x") if k > 0 else "−" + fr(-k, "x"), neg(Fr(k, x1))))
        cands = [("y = %dx" % abs(a), "정비례"), ("y = %s" % fr(abs(a), "x"), "반비례"), ("y = x + %d" % abs(a), "둘 다 아님"), ("xy = %d" % abs(a * 2), "반비례"), ("y = %s" % fr("x", abs(a)), "정비례")]
        t, k = R.choice(cands)
        return M("<b>%s</b>에서 y는 x에 대해 어떤 관계일까요?" % t, k, [x for x in ("정비례", "반비례", "둘 다 아님", "y가 x의 제곱에 비례") if x != k],
                 "y = ax 꼴은 정비례, y = a/x(xy = a) 꼴은 반비례예요. <b>%s</b>" % k)
    return mk


def pr_graph():
    def mk():
        how = R.choice(["dir", "inv"])
        if how == "dir":
            a = R.choice([Fr(1, 2), 2, -1, -2, 3, Fr(-1, 2), Fr(3, 2), Fr(-2, 3)])
            a = Fr(a)
            px = a.denominator * R.choice([1, 2])
            if abs(a * px) > 5 or px > 5:
                px = a.denominator
            py = a * px
            if abs(py) > 5:
                return None
            g = kosy(lines=[(a, 0, BLUE, "")], pts=[(px, py, "")])
            ok = "y = %s" % P([(a, "x")])
            return M("그림과 같이 원점과 점 (%s, %s)를 지나는 직선을 그래프로 하는 식은?%s" % (neg(px), neg(py), g), ok,
                     ["y = %s" % P([(-a, "x")]), "y = %s" % P([(1 / a, "x")]) if a not in (1, -1) else "y = x + 1", "y = %s" % P([(a, "x"), (1, "")])],
                     "y = ax에 x = %s, y = %s를 넣으면 a = %s. <b>%s</b>" % (neg(px), neg(py), neg(a), ok))
        k = R.choice([2, 3, 4, 6, -2, -4, -6])
        x0 = R.choice([d for d in (1, 2, 3) if abs(k) % d == 0])
        y0 = Fr(k, x0)

        def f(x):
            return None if abs(x) < 0.2 else k / x
        g = kurve([(f, BLUE, "")], (-6, 6, 1), (-6, 6, 1), pts=[(x0, y0, "")], label="반비례 그래프")
        ok = "y = %s" % (fr(k, "x") if k > 0 else "−" + fr(-k, "x"))
        return M("그림과 같이 점 (%s, %s)를 지나는 반비례 그래프의 식은?%s" % (neg(x0), neg(y0), g), ok,
                 ["y = %s" % (fr(-k, "x") if k < 0 else "−" + fr(k, "x")), "y = %s" % P([(k, "x")]), "y = %s" % (fr(k * 2, "x") if k > 0 else "−" + fr(-2 * k, "x"))],
                 "y = a/x에 넣으면 a = %s × %s = %s. <b>%s</b>" % (neg(x0), par(y0), neg(k), ok))
    return mk


def pr_word():
    def mk():
        how = R.choice(["gas", "gear", "water", "speed"])
        if how == "gas":
            a = R.choice([12, 15, 16, 18])
            x = R.randint(3, 9)
            return N("휘발유 1 L로 %d km를 가는 자동차가 있어요. 휘발유 x L로 가는 거리를 y km라 할 때, x = %d이면 y는?" % (a, x), a * x, [a + x, Fr(a, x), a * (x + 1)],
                     "y = %dx (정비례) → y = <b>%d</b>" % (a, a * x))
        if how == "gear":
            a, b = R.choice([(30, 20), (24, 16), (36, 12), (20, 25)])
            ra = R.choice([2, 3, 4, 5])
            return N("톱니 %d개인 톱니바퀴 A가 1분에 %d바퀴 돌 때, 맞물린 톱니 x개인 톱니바퀴 B는 1분에 y바퀴 돌아요. x = %d일 때 y는?" % (a, ra, b), Fr(a * ra, b),
                     [Fr(b * ra, a), a * ra, Fr(a * ra, b) + 1], "xy = %d (반비례) → y = %d ÷ %d = <b>%s</b>" % (a * ra, a * ra, b, neg(Fr(a * ra, b))))
        if how == "water":
            V = R.choice([60, 72, 120, 90])
            x = R.choice([d for d in range(2, 13) if V % d == 0])
            return N("들이가 %d L인 물통에 1분에 x L씩 물을 넣으면 가득 차는 데 y분이 걸려요. x = %d일 때 y는?" % (V, x), Fr(V, x), [V * x, V - x, Fr(V, x) + 1],
                     "xy = %d (반비례) → y = <b>%s</b>" % (V, neg(Fr(V, x))), f=lambda v: "%s분" % neg(v))
        d = R.choice([120, 180, 240, 360])
        v = R.choice([x for x in (30, 40, 60, 80, 90, 120) if d % x == 0])
        return N("%d km 떨어진 곳을 시속 x km로 가면 y시간이 걸려요. x = %d일 때 y는?" % (d, v), Fr(d, v), [d * v, Fr(v, d), d - v],
                 "xy = %d (반비례) → y = <b>%s</b>" % (d, neg(Fr(d, v))), f=lambda z: "%s시간" % neg(z))
    return mk


def pr_table():
    def mk():
        inv = R.random() < 0.5
        if not inv:
            a = R.choice([2, 3, 4, -2, -3])
            xs = [1, 2, 3, 4]
            ys = [a * x for x in xs]
        else:
            k = R.choice([12, 24, 36, -12, -24])
            xs = [1, 2, 3, 4]
            ys = [Fr(k, x) for x in xs]
        i = R.randint(1, 3)
        rows = "<tr><th>x</th>%s</tr><tr><th>y</th>%s</tr>" % ("".join("<td>%d</td>" % x for x in xs), "".join("<td>%s</td>" % ("□" if j == i else neg(y)) for j, y in enumerate(ys)))
        tb = "<div class='sn-tw'><table class='sn-table'>%s</table></div>" % rows
        v = ys[i]
        return N("y가 x에 %s할 때, 표의 □에 알맞은 수는?%s" % ("반비례" if inv else "정비례", tb), v, [ys[0] * xs[i] if inv else Fr(ys[0], xs[i]), -v, v + ys[0], v * 2],
                 ("xy의 값이 일정해요(%s)." % neg(ys[0])) + " <b>%s</b>" % neg(v) if inv else "y ÷ x의 값이 일정해요(%s). <b>%s</b>" % (neg(ys[0]), neg(v)))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "prime":
        return unit(G, "prime-factorization", 1, "[9수01-01] [9수01-02]",
                    "소인수분해의 뜻을 알고, 자연수를 소인수분해 할 수 있다. 소인수분해를 이용하여 최대공약수와 최소공배수를 구할 수 있다.",
                    "소인수분해와 최대공약수·최소공배수", "소인수분해",
                    "중학교 1학년 수학 소인수분해 문제: 소수와 합성수, 거듭제곱, 소인수분해, 약수의 개수, 제곱수 만들기, 최대공약수와 최소공배수, 활용 문제까지 100문제와 정답·해설.",
                    "72 = 2³ × 3²", "공통 소인수의 작은 지수 → 최대공약수, 큰 지수 → 최소공배수",
                    ["1보다 큰 자연수 중 1과 자기 자신만을 약수로 가지는 수를 <b>소수</b>, 약수가 3개 이상인 수를 <b>합성수</b>라고 해요. 1은 둘 다 아니에요.",
                     "자연수를 소수들의 곱으로 나타내는 것을 <b>소인수분해</b>라고 해요. 같은 소수는 거듭제곱으로 써요. 72 = 2³ × 3²",
                     "a<sup>m</sup> × b<sup>n</sup>의 약수의 개수는 (m + 1)(n + 1)개예요.",
                     "최대공약수는 공통인 소인수를 <b>작은</b> 지수로, 최소공배수는 모든 소인수를 <b>큰</b> 지수로 곱해요."],
                    [("90을 소인수분해", ["90 = 2 × 45 = 2 × 3 × 15 = 2 × 3 × 3 × 5"], "2 × 3² × 5"),
                     ("2³ × 3, 2 × 3² × 5의 최대공약수", ["공통 소인수 2, 3", "작은 지수: 2¹, 3¹"], "2 × 3 = 6")],
                    [("1을 소수라고 한다", "1은 소수도 합성수도 아니에요."),
                     ("2³ × 3²의 약수의 개수를 3 × 2 = 6이라고 한다", "지수에 1씩 더해 곱해요: 4 × 3 = 12"),
                     ("최소공배수를 지수가 작은 쪽으로 곱한다", "최소공배수는 큰 지수, 최대공약수는 작은 지수예요.")],
                    [("소인수분해는 언제 배우나요?", "중학교 1학년 1학기 첫 단원에서 배워요."),
                     ("최대공약수를 빨리 구하는 방법은?", "두 수를 공통인 소수로 계속 나누는 방법(나눗셈)도 함께 익히면 좋아요.")],
                    [("소수와 합성수", [(p_prime(), 20)]),
                     ("거듭제곱", [(p_power(), 20)]),
                     ("소인수분해와 약수", [(p_factor(), 12), (p_divisors(), 8)]),
                     ("최대공약수와 최소공배수", [(p_gcdlcm(), 20)]),
                     ("활용 문제", [(p_word(), 20)])], 82701)
    if which == "intrat":
        return unit(G, "integers-and-rational-numbers", 2, "[9수01-03] [9수01-04]",
                    "다양한 상황을 이용하여 음수의 필요성을 인식하고, 양수와 음수, 정수와 유리수의 개념을 이해한다. 정수와 유리수의 대소 관계를 판단할 수 있다.",
                    "정수와 유리수: 수직선, 절댓값, 대소 관계", "정수와 유리수",
                    "중학교 1학년 수학 정수와 유리수 문제: 부호로 나타내기, 정수와 유리수의 분류, 수직선, 절댓값, 수의 대소 관계, 부등호로 나타내기까지 100문제와 정답·해설.",
                    "절댓값 = 원점으로부터의 거리", "음수는 절댓값이 클수록 작아요.",
                    ["서로 반대되는 성질의 양은 +, − 부호로 나타내요. 영상 3 °C는 +3, 영하 2 °C는 −2예요.",
                     "양의 정수, 0, 음의 정수를 <b>정수</b>, (정수)/(0이 아닌 정수)로 나타낼 수 있는 수를 <b>유리수</b>라고 해요.",
                     "수직선에서 원점으로부터 떨어진 거리를 <b>절댓값</b>이라 하고 |−3| = 3처럼 써요.",
                     "양수는 0보다 크고, 음수는 0보다 작아요. 음수끼리는 <b>절댓값이 클수록 작아요</b>."],
                    [("−3/4과 −2/3의 크기 비교", ["절댓값: 3/4 = 9/12, 2/3 = 8/12", "절댓값이 큰 −3/4이 더 작아요."], "−3/4 &lt; −2/3"),
                     ("절댓값이 2 이하인 정수", ["−2, −1, 0, 1, 2"], "5개")],
                    [("−5가 −2보다 크다고 한다", "음수는 절댓값이 클수록 작아요: −5 &lt; −2"),
                     ("0을 양수라고 한다", "0은 양수도 음수도 아닌 정수예요."),
                     ("절댓값이 3인 수를 3 하나만 쓴다", "+3과 −3, 두 개예요.")],
                    [("유리수는 왜 배우나요?", "음수와 분수를 하나로 묶어 계산 규칙을 세우면 방정식과 함수를 다룰 수 있어요."),
                     ("수직선을 꼭 그려야 하나요?", "처음에는 수직선에 점을 찍어 보면 대소 관계와 절댓값을 쉽게 이해할 수 있어요.")],
                    [("부호로 나타내기", [(r_sign(), 20)]),
                     ("정수와 유리수의 분류", [(r_classify(), 20)]),
                     ("수직선", [(r_line(), 20)]),
                     ("절댓값", [(r_abs(), 20)]),
                     ("수의 대소 관계", [(r_order(), 20)])], 82702)
    if which == "addsub":
        return unit(G, "adding-and-subtracting-integers-and-rational-numbers", 3, "[9수01-05]",
                    "정수와 유리수의 사칙계산의 원리를 이해하고, 그 계산을 할 수 있다.",
                    "정수와 유리수의 덧셈과 뺄셈", "덧셈과 뺄셈",
                    "중학교 1학년 수학 정수와 유리수의 덧셈과 뺄셈 문제: 정수, 분수, 소수의 덧셈과 뺄셈, 세 수의 계산, 기온·층·점수 활용 문제까지 100문제와 정답·해설.",
                    "빼기는 부호를 바꾼 수의 덧셈", "부호가 다르면 절댓값의 차에 큰 쪽 부호를 붙여요.",
                    ["부호가 같은 두 수의 합: 절댓값의 합에 <b>공통인 부호</b>를 붙여요. (−3) + (−5) = −8",
                     "부호가 다른 두 수의 합: 절댓값의 차에 <b>절댓값이 큰 수의 부호</b>를 붙여요. (−7) + (+4) = −3",
                     "뺄셈은 빼는 수의 <b>부호를 바꾸어 더해요</b>. (+2) − (−6) = (+2) + (+6) = 8",
                     "분수는 통분하고, 소수는 자리를 맞추어 계산해요."],
                    [("(−4) − (+9)", ["(−4) + (−9)", "부호가 같으니 −(4 + 9)"], "−13"),
                     ("(+1/2) + (−3/4)", ["통분: 2/4 − 3/4"], "−1/4")],
                    [("(−3) + (−5)를 2라고 한다", "부호가 같으면 절댓값을 더해요: −8"),
                     ("(+2) − (−6)을 −4라고 한다", "빼는 수의 부호를 바꾸어 더해요: 8"),
                     ("(−7) + (+4)를 −11이라고 한다", "부호가 다르면 절댓값의 차: −3")],
                    [("덧셈의 교환법칙과 결합법칙도 쓰나요?", "네. 양수끼리, 음수끼리 모아 계산하면 편해요."),
                     ("계산이 맞는지 확인하는 방법은?", "수직선에서 화살표로 움직여 보거나, 뺄셈의 답에 빼는 수를 더해 보세요.")],
                    [("정수의 덧셈", [(a_calc("+", "int"), 20)]),
                     ("정수의 뺄셈", [(a_calc("−", "int"), 20)]),
                     ("분수와 소수의 덧셈과 뺄셈", [(a_calc("+", "frac"), 6), (a_calc("−", "frac"), 6), (a_calc("+", "dec"), 4), (a_calc("−", "dec"), 4)]),
                     ("세 수의 계산", [(a_mixed(), 20)]),
                     ("활용 문제", [(a_word(), 20)])], 82703)
    if which == "muldiv":
        return unit(G, "multiplying-and-dividing-integers-and-rational-numbers", 4, "[9수01-05]",
                    "정수와 유리수의 사칙계산의 원리를 이해하고, 그 계산을 할 수 있다.",
                    "정수와 유리수의 곱셈과 나눗셈", "곱셈과 나눗셈",
                    "중학교 1학년 수학 정수와 유리수의 곱셈과 나눗셈 문제: 부호 정하기, 세 수의 곱, 거듭제곱(−2)³과 −2², 역수와 나눗셈, 혼합 계산 순서, 활용 문제까지 100문제와 정답·해설.",
                    "음수가 짝수 개면 +, 홀수 개면 −", "나눗셈은 역수의 곱셈으로 바꾸어요.",
                    ["두 수의 곱과 몫은 부호가 같으면 <b>+</b>, 다르면 <b>−</b>예요.",
                     "여러 수의 곱은 음수의 개수가 짝수이면 +, 홀수이면 −예요.",
                     "(−2)² = 4이지만 −2² = −4예요. 괄호가 있는지 꼭 확인해요.",
                     "혼합 계산은 거듭제곱 → 괄호 → 곱셈·나눗셈 → 덧셈·뺄셈 순서로 해요."],
                    [("(−3) × (+4) × (−2)", ["음수 2개 → +", "3 × 4 × 2 = 24"], "24"),
                     ("(−6) ÷ (−2/3)", ["역수를 곱해요: (−6) × (−3/2)"], "9")],
                    [("−3²을 9라고 한다", "3²을 먼저 계산해요: −9"),
                     ("(−8) ÷ 4/5를 (−8) × 4/5로 계산한다", "나누는 수의 역수 5/4를 곱해요: −10"),
                     ("2 + 3 × (−4)를 −20이라고 한다", "곱셈을 먼저: 2 + (−12) = −10")],
                    [("왜 음수 × 음수가 양수인가요?", "(−3) × (−2)는 '−3을 반대 방향으로 2번'으로 생각하거나, 분배법칙이 성립하도록 정하면 +6이 돼요."),
                     ("역수가 없는 수도 있나요?", "0은 어떤 수를 곱해도 1이 되지 않아 역수가 없어요.")],
                    [("곱셈", [(m_calc("mul"), 14), (m_calc("three"), 6)]),
                     ("거듭제곱", [(m_power(), 20)]),
                     ("나눗셈과 역수", [(m_calc("div"), 14), (m_word(), 6)]),
                     ("혼합 계산", [(m_order(), 20)]),
                     ("섞어서 연습", [(m_calc("three"), 6), (m_word(), 6), (m_order(), 8)])], 82704)
    if which == "expr":
        return unit(G, "algebraic-expressions", 5, "[9수02-01] [9수02-02]",
                    "다양한 상황을 문자를 사용한 식으로 나타내어 그 유용성을 인식하고, 식의 값을 구할 수 있다. 일차식의 덧셈과 뺄셈의 원리를 이해하고, 그 계산을 할 수 있다.",
                    "문자와 식: 식의 값과 일차식의 계산", "문자와 식",
                    "중학교 1학년 수학 문자와 식 문제: 곱셈·나눗셈 기호 생략, 문자를 사용한 식, 식의 값, 동류항, 일차식의 덧셈과 뺄셈까지 100문제와 정답·해설.",
                    "동류항끼리 모아서 계산", "음수를 대입할 때는 괄호를 꼭 써요.",
                    ["곱셈 기호는 생략하고 수를 문자 앞에 써요. b × 3 × a = 3ab, 나눗셈은 분수로 나타내요. x ÷ 4 = x/4",
                     "문자에 수를 넣어 계산한 결과를 <b>식의 값</b>이라고 해요. 음수는 괄호를 씌워 넣어요.",
                     "문자와 차수가 같은 항을 <b>동류항</b>이라 하고, 계수끼리 더하거나 빼요.",
                     "괄호 앞이 −이면 괄호 안의 모든 항의 부호를 바꾸어요."],
                    [("x = −2일 때 x² − 3x", ["(−2)² − 3 × (−2) = 4 + 6"], "10"),
                     ("3(2x − 1) − (x + 4)", ["6x − 3 − x − 4"], "5x − 7")],
                    [("x = −2일 때 x²을 −4라고 한다", "(−2)² = 4예요. 괄호를 씌워요."),
                     ("2(3x − 1)을 6x − 1이라고 한다", "뒤의 항에도 곱해요: 6x − 2"),
                     ("3x와 3x²을 동류항이라고 한다", "차수가 달라 동류항이 아니에요.")],
                    [("문자를 쓰면 무엇이 좋나요?", "여러 경우를 하나의 식으로 나타낼 수 있어 규칙을 한눈에 볼 수 있어요."),
                     ("일차식이란?", "차수가 가장 큰 항의 차수가 1인 다항식이에요. 2x + 3, −x 등.")],
                    [("곱셈·나눗셈 기호 생략", [(e_notation(), 12), (e_like(), 8)]),
                     ("문자를 사용한 식", [(e_write(), 20)]),
                     ("식의 값", [(e_value(), 20)]),
                     ("일차식의 계산", [(e_linear(), 20)]),
                     ("섞어서 연습", [(e_value(), 10), (e_linear(), 10)])], 82705)
    if which == "eq":
        return unit(G, "linear-equations", 6, "[9수02-03] [9수02-04]",
                    "방정식과 그 해의 뜻을 알고, 등식의 성질을 설명할 수 있다. 일차방정식을 풀 수 있다.",
                    "일차방정식: 등식의 성질과 풀이", "일차방정식",
                    "중학교 1학년 수학 일차방정식 문제: 방정식과 항등식, 해 확인, 등식의 성질, 이항, 괄호·분수·소수가 있는 일차방정식 풀이까지 100문제와 정답·해설.",
                    "이항하면 부호가 바뀌어요", "분수·소수는 양변에 같은 수를 곱해 정수로 바꾸어요.",
                    ["x의 값에 따라 참·거짓이 정해지는 등식을 <b>방정식</b>, 항상 참인 등식을 <b>항등식</b>이라고 해요.",
                     "등식의 양변에 같은 수를 더하거나 빼거나 곱하거나 0이 아닌 같은 수로 나누어도 등식은 성립해요.",
                     "한 변의 항을 부호를 바꾸어 다른 변으로 옮기는 것을 <b>이항</b>이라고 해요.",
                     "괄호는 먼저 풀고, 분수·소수는 양변에 최소공배수나 10을 곱해요."],
                    [("3x − 5 = x + 7", ["3x − x = 7 + 5", "2x = 12"], "x = 6"),
                     ("x/2 + 1 = x/3", ["양변 × 6: 3x + 6 = 2x"], "x = −6")],
                    [("이항할 때 부호를 바꾸지 않는다", "−5를 이항하면 +5가 돼요."),
                     ("x/2 + 1 = x/3에 6을 곱할 때 1에는 곱하지 않는다", "모든 항에 곱해요: 3x + 6 = 2x"),
                     ("2(x − 3) = 4를 2x − 3 = 4로 푼다", "괄호 안의 모든 항에 곱해요: 2x − 6 = 4")],
                    [("해를 구한 뒤 확인하는 방법은?", "구한 x를 처음 방정식에 넣어 양변이 같은지 확인해요."),
                     ("해가 없는 방정식도 있나요?", "0 × x = 3처럼 정리되면 해가 없어요. 1학년에서는 해가 하나인 일차방정식을 주로 다뤄요.")],
                    [("방정식과 등식의 성질", [(q_eqconcept(), 20)]),
                     ("간단한 일차방정식", [(q_solve(["basic"]), 20)]),
                     ("양변에 x가 있는 방정식", [(q_solve(["both"]), 20)]),
                     ("괄호가 있는 방정식", [(q_solve(["paren"]), 20)]),
                     ("분수·소수가 있는 방정식", [(q_solve(["frac"]), 10), (q_solve(["dec"]), 10)])], 82706)
    if which == "eqword":
        return unit(G, "linear-equation-word-problems", 7, "[9수02-04]",
                    "일차방정식을 풀 수 있고, 이를 활용하여 문제를 해결할 수 있다.",
                    "일차방정식의 활용 문제", "일차방정식의 활용",
                    "중학교 1학년 수학 일차방정식의 활용 문제: 어떤 수, 연속하는 수, 나이, 물건 값, 거리·속력·시간, 과부족 문제를 방정식으로 세워 푸는 100문제와 정답·해설.",
                    "구하는 것을 x로 놓고 식 세우기", "답을 구한 뒤 문제의 조건에 맞는지 확인해요.",
                    ["① 구하려는 것을 <b>x</b>로 놓아요.",
                     "② 문제의 뜻에 맞게 <b>방정식</b>을 세워요.",
                     "③ 방정식을 풀어 x의 값을 구해요.",
                     "④ 구한 값이 문제의 뜻에 맞는지(자연수인지, 단위는 맞는지) <b>확인</b>해요."],
                    [("어떤 수의 3배에서 4를 빼면 11", ["3x − 4 = 11"], "5"),
                     ("갈 때 시속 3 km, 올 때 시속 6 km, 모두 3시간", ["x/3 + x/6 = 3"], "6 km")],
                    [("x를 무엇으로 놓았는지 정하지 않는다", "구하는 것을 먼저 x로 정해요."),
                     ("거리 문제에서 시간을 거리 × 속력으로 쓴다", "시간 = 거리 ÷ 속력이에요."),
                     ("나이 문제에서 다른 사람의 나이는 그대로 둔다", "x년 후에는 두 사람 모두 x살 많아져요.")],
                    [("식 세우기가 어려워요.", "문장을 짧게 끊어 '무엇 = 무엇'이 되는 부분을 찾아보세요."),
                     ("답이 분수가 나오면?", "사람 수나 개수처럼 자연수여야 하는 경우는 식을 다시 확인해요.")],
                    [("어떤 수와 연속하는 수", [(q_word(("num", "consec")), 20)]),
                     ("나이와 물건 값", [(q_word(("age", "price")), 20)]),
                     ("거리·속력·시간", [(q_word(("speed",)), 20)]),
                     ("과부족 문제", [(q_word(("share",)), 20)]),
                     ("섞어서 연습", [(q_word(), 20)])], 82707)
    if which == "coord":
        return unit(G, "coordinates-and-graphs", 8, "[9수02-05] [9수02-06]",
                    "순서쌍과 좌표를 이해하고, 그 편리함을 인식할 수 있다. 다양한 상황을 그래프로 나타내고, 주어진 그래프를 해석할 수 있다.",
                    "좌표평면과 그래프 해석", "좌표평면과 그래프",
                    "중학교 1학년 수학 좌표평면과 그래프 문제: 점의 좌표, 사분면, 대칭인 점, 좌표평면 위 삼각형의 넓이, 시간과 거리의 그래프 해석까지 100문제와 정답·해설.",
                    "(x좌표, y좌표) 순서로", "x좌표와 y좌표의 부호로 사분면을 정해요.",
                    ["점의 위치를 (x좌표, y좌표)로 나타내요. 순서가 바뀌면 다른 점이에요.",
                     "좌표축은 어느 사분면에도 속하지 않아요. (+, +) 제1사분면, (−, +) 제2사분면, (−, −) 제3사분면, (+, −) 제4사분면",
                     "x축 대칭은 y좌표, y축 대칭은 x좌표, 원점 대칭은 두 좌표의 부호가 모두 바뀌어요.",
                     "그래프에서 수평인 부분은 변화가 없는 구간이에요."],
                    [("점 (3, −2)", ["x좌표 +, y좌표 −"], "제4사분면"),
                     ("(2, 5)와 x축에 대칭인 점", ["y좌표의 부호만 바꿔요."], "(2, −5)")],
                    [("(3, −2)를 x = −2, y = 3으로 읽는다", "앞이 x좌표, 뒤가 y좌표예요."),
                     ("x축 대칭에서 x좌표의 부호를 바꾼다", "x축 대칭은 y좌표의 부호가 바뀌어요."),
                     ("(0, 3)이 제1사분면 위의 점이라고 한다", "좌표축 위의 점은 사분면에 속하지 않아요.")],
                    [("좌표는 어디에 쓰이나요?", "지도, 게임 화면, 그래프처럼 위치를 수로 정확히 나타낼 때 써요."),
                     ("그래프 해석 문제는 어떻게 푸나요?", "x축과 y축이 무엇을 나타내는지 먼저 확인하고, 오르는 곳·평평한 곳·내려가는 곳의 뜻을 생각해요.")],
                    [("점의 좌표", [(c_read(), 20)]),
                     ("사분면과 대칭", [(c_quad(), 20)]),
                     ("좌표평면 위의 도형", [(c_area(), 20)]),
                     ("그래프 해석", [(c_graph(), 20)]),
                     ("섞어서 연습", [(c_quad(), 8), (c_read(), 6), (c_graph(), 6)])], 82708)
    if which == "prop":
        return unit(G, "direct-and-inverse-proportion", 9, "[9수02-07]",
                    "정비례, 반비례 관계를 이해하고, 그 관계를 표, 식, 그래프로 나타낼 수 있다.",
                    "정비례와 반비례: 표, 식, 그래프", "정비례와 반비례",
                    "중학교 1학년 수학 정비례와 반비례 문제: 관계 구별하기, 표 완성, 식 구하기, y = ax와 y = a/x의 그래프, 실생활 활용 문제까지 100문제와 정답·해설.",
                    "정비례 y = ax, 반비례 y = a/x", "정비례는 y/x, 반비례는 xy가 일정해요.",
                    ["x가 2배, 3배가 될 때 y도 2배, 3배가 되면 <b>정비례</b>, 식은 y = ax (a ≠ 0)예요.",
                     "x가 2배, 3배가 될 때 y는 1/2배, 1/3배가 되면 <b>반비례</b>, 식은 y = a/x (a ≠ 0)예요.",
                     "y = ax의 그래프는 원점을 지나는 직선, y = a/x의 그래프는 좌표축에 한없이 가까워지는 한 쌍의 곡선이에요.",
                     "한 점의 좌표를 식에 넣으면 a의 값을 구할 수 있어요."],
                    [("y = ax가 점 (2, −6)을 지날 때", ["−6 = 2a"], "a = −3"),
                     ("y = a/x가 점 (3, 4)를 지날 때", ["4 = a/3"], "a = 12")],
                    [("y = x + 3을 정비례라고 한다", "y = ax 꼴만 정비례예요."),
                     ("반비례에서 y/x가 일정하다고 한다", "반비례는 xy가 일정해요."),
                     ("y = −2x의 그래프가 오른쪽 위로 향한다고 한다", "a &lt; 0이면 오른쪽 아래로 향해요.")],
                    [("정비례와 반비례는 초등학교에서도 배웠나요?", "초등 6학년에서 비례식을 배우고, 중학교에서는 음수까지 넓혀 식과 그래프로 나타내요."),
                     ("2학년에서는 무엇을 배우나요?", "일차함수 y = ax + b와 그 그래프를 배워요.")],
                    [("정비례와 반비례 구별", [(pr_basic(), 20)]),
                     ("표 완성하기", [(pr_table(), 20)]),
                     ("그래프와 식", [(pr_graph(), 20)]),
                     ("활용 문제", [(pr_word(), 20)]),
                     ("섞어서 연습", [(pr_basic(), 8), (pr_graph(), 6), (pr_word(), 6)])], 82709)
    raise ValueError(which)
