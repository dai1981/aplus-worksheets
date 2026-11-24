# -*- coding: utf-8 -*-
"""
대한민국 고등학교 대수（2022 개정）の 14 単元。build(key)：
  root 거듭제곱근 / expo 지수의 확장과 지수법칙 / log 로그 / clog 상용로그 / elf 지수함수와 로그함수
  eleq 지수·로그방정식과 부등식 / rad 일반각과 호도법 / trig 삼각함수 / tgraph 삼각함수의 그래프 / law 사인법칙과 코사인법칙
  arith 등차수열 / geo 등비수열 / sigma 수열의 합 / rec 수열의 귀납적 정의와 수학적 귀납법
誤答は「a^m × a^n = a^mn」「log(a + b) = log a + log b」「밑이 1보다 작을 때 부등호를 그대로 둔다」「진수 조건을 확인하지 않는다」
「호도법에서 180 대신 360을 쓴다」「사분면의 부호를 바꾼다」「주기를 2π·b로 쓴다」「Sₙ = n(a + l)으로 2를 빠뜨린다」
「등비수열의 합에서 rⁿ을 rⁿ⁻¹로 쓴다」「Σk를 n²/2로 쓴다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_hs import M, N, neg, par, px, surd, W, graph, num, fr, unit, BLUE, RED
from pc_common import pis, trig, vhtml

R = random.Random(83201)
G = "algebra"


def nz(lo=-6, hi=6):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def rt(n, a):
    """n제곱근 기호"""
    a = neg(a)
    if n == 2:
        return "√%s" % a if len(a) == 1 or a.isdigit() else "√(%s)" % a
    if n == 3:
        return "∛%s" % a
    if n == 4:
        return "∜%s" % a
    return "<sup>%d</sup>√%s" % (n, a)


def ex(f):
    """지수 Fraction → sup 안의 문자"""
    f = Fr(f)
    return neg(f) if f.denominator == 1 else ("−" if f < 0 else "") + "%d/%d" % (abs(f.numerator), f.denominator)


def pw(b, e):
    return "%s<sup>%s</sup>" % (b if isinstance(b, str) else (neg(b) if b >= 0 else par(b)), ex(e))


def lg(b, x):
    """log_b x"""
    bb = "" if b == 10 else "<sub>%s</sub>" % (b if isinstance(b, str) else neg(b))
    return "log%s %s" % (bb, x if isinstance(x, str) else neg(x))


def fv(v):
    return neg(Fr(v))


# ------------------------------------------------------------------ 거듭제곱근
def r_main(kinds=("eval", "count", "mul", "nest", "pow", "cmp")):
    def mk():
        how = R.choice(kinds)
        if how == "eval":
            n = R.choice([2, 3, 3, 4, 5])
            b = R.randint(2, {2: 15, 3: 6, 4: 4, 5: 3}[n])
            neg_ = n % 2 == 1 and R.random() < 0.4
            a = (-1 if neg_ else 1) * b ** n
            v = -b if neg_ else b
            return N("<b>%s</b>의 값은?" % rt(n, a), v, [-v, Fr(a, n), b ** (n - 1), v * 2], "%s<sup>%d</sup> = %s이므로 <b>%s</b>" % (par(v), n, neg(a), neg(v)))
        if how == "count":
            n = R.randint(2, 7)
            a = R.choice([-8, -4, -1, 1, 4, 8, 16, 27, -27, 0])
            if a == 0:
                c = 1
            elif n % 2:
                c = 1
            else:
                c = 2 if a > 0 else 0
            return N("%s의 %d제곱근 중 실수인 것의 개수는?" % (neg(a), n), c, [x for x in (0, 1, 2, n) if x != c], "%s일 때 x<sup>%d</sup> = %s의 실근은 <b>%d개</b>" % ("n이 홀수" if n % 2 else "n이 짝수", n, neg(a), c), f=lambda v: "%s개" % neg(v))
        if how == "mul":
            n = R.choice([2, 3, 4, 5])
            b = R.randint(2, {2: 8, 3: 5, 4: 3, 5: 2}[n])
            p = R.choice([v for v in range(2, b ** n) if (b ** n) % v == 0 and v != 1])
            q = b ** n // p
            return N("<b>%s × %s</b>의 값은?" % (rt(n, p), rt(n, q)), b, [b ** n, rt(n, p + q), b * n, b + 1] if False else [b ** n, n * b, b + 1, Fr(b ** n, n)], "ⁿ√a × ⁿ√b = ⁿ√(ab) = %s = <b>%d</b>" % (rt(n, b ** n), b))
        if how == "nest":
            m, n = R.choice([(2, 3), (3, 2), (2, 2), (2, 4), (3, 3), (2, 5)])
            b = R.choice([2, 3]) if m * n <= 6 else 2
            k = m * n
            a = b ** k
            return N("<b>%s</b>의 값은?" % ("√(%s)" % rt(n, a) if m == 2 else "∛(%s)" % rt(n, a)), b, [b ** (k // 2), a // (m + n), b * 2, k], "<sup>m</sup>√(<sup>n</sup>√a) = <sup>mn</sup>√a = %s = <b>%d</b>" % (rt(k, a), b))
        if how == "pow":
            n = R.choice([2, 3, 4])
            b = R.randint(2, 4)
            m = R.randint(2, 4)
            if b ** m > 300:
                return None
            a = b ** n
            v = b ** m
            return N("<b>(%s)<sup>%d</sup></b>의 값은?" % (rt(n, a), m), v, [a ** m if a ** m < 10000 else v + 1, b * m, a * m, v * b], "(ⁿ√a)<sup>m</sup> = ⁿ√(a<sup>m</sup>)이고 %s = %d이므로 %d<sup>%d</sup> = <b>%d</b>" % (rt(n, a), b, b, m, v))
        pairs = [(("√2", 2 ** Fr(1, 2)), ("∛3", 3 ** Fr(1, 3)), ("∜5", 5 ** 0.25)), (("√3", 3 ** 0.5), ("∛5", 5 ** (1 / 3)), ("∜8", 8 ** 0.25)), (("∛2", 2 ** (1 / 3)), ("∜3", 3 ** 0.25), ("<sup>6</sup>√5", 5 ** (1 / 6))),
                 (("√5", 5 ** 0.5), ("∛11", 11 ** (1 / 3)), ("∜24", 24 ** 0.25)), (("∛4", 4 ** (1 / 3)), ("√2", 2 ** 0.5), ("<sup>6</sup>√15", 15 ** (1 / 6)))]
        t = R.choice(pairs)
        k = R.choice(["max", "min"])
        srt = sorted(t, key=lambda u: float(u[1]))
        ok = (srt[-1] if k == "max" else srt[0])[0]
        return M("세 수 %s, %s, %s 중 가장 %s 수는?" % (t[0][0], t[1][0], t[2][0], "큰" if k == "max" else "작은"), ok, [u[0] for u in t if u[0] != ok] + ["모두 같아요"],
                 "모두 12제곱근(또는 공통인 거듭제곱근)으로 바꾸어 근호 안을 비교해요. <b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 지수
def e_main(kinds=("rat", "neg", "law", "simp", "eq", "sym")):
    def mk():
        how = R.choice(kinds)
        if how in ("rat", "neg"):
            b = R.randint(2, 10)
            n = R.choice([2, 2, 3])
            if b ** n > 1000:
                return None
            m = R.randint(1, 4) * (-1 if how == "neg" else 1)
            if abs(Fr(b) ** m) > 10000:
                return None
            base = b ** n
            if how == "rat" and m % n == 0:
                return None
            v = Fr(b) ** m
            return N("<b>%s</b>의 값은?" % pw(base, Fr(m, n)), v, [Fr(base * m, n), 1 / v if v != 1 else v + 1, Fr(b * m, 1), -v], "%d = %d<sup>%d</sup>이므로 %d<sup>%s</sup> = <b>%s</b>" % (base, b, n, b, neg(m), neg(v)))
        if how == "law":
            p, q = Fr(R.randint(1, 5), R.choice([2, 3, 4, 6])), Fr(R.randint(1, 5), R.choice([2, 3, 4, 6]))
            k = R.choice(["mul", "div", "pow"])
            if k == "mul":
                ok = pw("a", p + q)
                w = [pw("a", p * q), pw("a", p - q) if p != q else "1", pw("a", p + q + 1)]
                return M("a &gt; 0일 때, <b>%s × %s</b>를 간단히 하면?" % (pw("a", p), pw("a", q)), ok, w, "지수끼리 더해요: %s + %s = %s. <b>%s</b>" % (ex(p), ex(q), ex(p + q), ok))
            if k == "div":
                if p == q:
                    return None
                ok = pw("a", p - q)
                w = [pw("a", p / q), pw("a", p + q), pw("a", q - p)]
                return M("a &gt; 0일 때, <b>%s ÷ %s</b>를 간단히 하면?" % (pw("a", p), pw("a", q)), ok, w, "지수끼리 빼요: %s − %s = %s. <b>%s</b>" % (ex(p), ex(q), ex(p - q), ok))
            ok = pw("a", p * q)
            w = [pw("a", p + q), pw("a", p * q + 1), pw("a", p / q) if p != q else pw("a", 2 * p)]
            return M("a &gt; 0일 때, <b>(%s)<sup>%s</sup></b>를 간단히 하면?" % (pw("a", p), ex(q)), ok, w, "지수끼리 곱해요. <b>%s</b>" % ok)
        if how == "simp":
            b = R.choice([2, 3, 5])
            e1, e2, e3 = Fr(R.randint(1, 4), 2), Fr(R.randint(1, 4), 3), Fr(R.randint(1, 5), 6)
            tot = e1 + e2 - e3
            if e2 == e3 or tot.denominator != 1 or tot < 0 or b ** tot > 200:
                return None
            v = b ** int(tot)
            return N("<b>%s × %s ÷ %s</b>의 값은?" % (pw(b, e1), pw(b, e2), pw(b, e3)), v, [b ** int(e1 + e2 + e3) if b ** int(e1 + e2 + e3) < 10 ** 6 and (e1 + e2 + e3).denominator == 1 else v * b, v * b, Fr(v, b), b ** int(tot) + 1],
                     "지수: %s + %s − %s = %s. <b>%s</b>" % (ex(e1), ex(e2), ex(e3), neg(tot), neg(v)))
        if how == "eq":
            b = R.choice([2, 3])
            n = R.choice([2, 3, 4])
            m = R.randint(1, 5)
            ok = pw(b, Fr(m, n))
            return M("<b>%s</b>을 %d의 거듭제곱으로 나타내면?" % (rt(n, b ** m) if b ** m < 1000 else rt(n, "%d<sup>%d</sup>" % (b, m)), b), ok, [pw(b, Fr(n, m)), pw(b, m * n), pw(b, Fr(m, n) + 1), pw(b, Fr(-m, n))],
                     "ⁿ√(a<sup>m</sup>) = a<sup>m/n</sup>. <b>%s</b>" % ok)
        # sym: a^(1/2) + a^(−1/2) = k → a + a^(−1) = k² − 2
        k = R.randint(2, 7)
        v = k * k - 2
        return N("a &gt; 0이고 %s + %s = %d일 때, a + a<sup>−1</sup>의 값은?" % (pw("a", Fr(1, 2)), pw("a", Fr(-1, 2)), k), v, [k * k, k * k + 2, 2 * k, v - 1], "양변을 제곱하면 a + 2 + a<sup>−1</sup> = %d. <b>%d</b>" % (k * k, v))
    return mk


# ------------------------------------------------------------------ 로그
def lg_main(kinds=("def", "eval", "add", "sub", "chg", "pow", "cond")):
    def mk():
        how = R.choice(kinds)
        if how == "def":
            b = R.choice([2, 3, 5, 10])
            e = R.randint(-2, 4)
            if e in (0, 1):
                e = R.choice([2, 3, -1, -2])
            k = R.choice(["log", "exp"])
            v = Fr(b) ** e
            X = neg(v) if v.denominator == 1 else fr(1, v.denominator)
            if k == "log":
                ok = "%s = %s" % (lg(b, X), neg(e))
                w = ["%s = %s" % (lg(X, b), neg(e)), "%s = %s" % (lg(b, neg(e)), X), "%s = %s" % (lg(b, X), neg(-e)), "%s = %s" % (lg(neg(e), X), neg(b)) if e > 1 else "%s = %s" % (lg(b, X), neg(e + 1))]
                return M("<b>%s = %s</b>를 로그로 나타내면?" % (pw(b, e), X), ok, w, "a<sup>x</sup> = N ⇔ x = log<sub>a</sub> N. <b>%s</b>" % ok)
            return N("<b>%s = %s</b>일 때, x의 값은?" % (lg(b, "x"), neg(e)), v, [b * e, Fr(e, b), Fr(b) ** (e + 1), -v], "x = %d<sup>%s</sup> = <b>%s</b>" % (b, neg(e), neg(v)))
        if how == "eval":
            b = R.choice([2, 3, 4, 5, 8, 9, 10, 27])
            base = {2: 2, 3: 3, 4: 2, 5: 5, 8: 2, 9: 3, 10: 10, 27: 3}[b]
            pb = round(math.log(b, base))
            e = R.randint(-3, 6)
            x = Fr(base) ** e
            if x > 10 ** 5 or x < Fr(1, 1000):
                return None
            v = Fr(e, pb)
            xs = neg(x) if x.denominator == 1 else fr(1, x.denominator)
            return N("<b>%s</b>의 값은?" % lg(b, xs), v, [Fr(pb, e) if e else v + 1, Fr(x, b) if Fr(x, b) != v else v + 2, e, -v if v else 1], "%s = %d<sup>%s</sup>이므로 <b>%s</b>" % (xs, b, ex(v), neg(v)))
        if how == "add":
            b = R.choice([2, 3, 6, 10])
            tgt = R.randint(1, 3)
            P = b ** tgt
            divs = [d for d in range(2, P) if P % d == 0]
            if not divs:
                return None
            d = R.choice(divs)
            return N("<b>%s + %s</b>의 값은?" % (lg(b, d), lg(b, P // d)), tgt, [lg_val(b, d + P // d), tgt + 1, Fr(d * (P // d), b) if b > 1 else 0, tgt * 2], "log<sub>a</sub> M + log<sub>a</sub> N = log<sub>a</sub> MN = %s = <b>%d</b>" % (lg(b, P), tgt))
        if how == "sub":
            b = R.choice([2, 3, 5])
            tgt = R.randint(1, 3)
            d = R.randint(2, 7)
            if d % b == 0:
                return None
            M_ = d * b ** tgt
            return N("<b>%s − %s</b>의 값은?" % (lg(b, M_), lg(b, d)), tgt, [Fr(M_, d) if Fr(M_, d) != tgt else tgt + 2, tgt + 1, lg_val(b, M_ - d), -tgt], "log<sub>a</sub> M − log<sub>a</sub> N = log<sub>a</sub> (M/N) = %s = <b>%d</b>" % (lg(b, b ** tgt), tgt))
        if how == "chg":
            k = R.choice(["prod", "inv", "base"])
            a, b = R.sample([2, 3, 5], 2)
            if k == "prod":
                m, n = R.randint(1, 4), R.randint(1, 4)
                v = m * n
                return N("<b>%s × %s</b>의 값은?" % (lg(a, b ** m), lg(b, a ** n)), v, [m + n, Fr(m, n), m * n + 1, max(m, n)], "밑의 변환: (%d log b ÷ log a) × (%d log a ÷ log b) = <b>%d</b>" % (m, n, v))
            if k == "inv":
                return M("<b>%s × %s</b>의 값은?" % (lg(a, b), lg(b, a)), "1", ["0", neg(a * b), "%s" % lg(a * b, a * b)[:-1] + "2" if False else "2"] + [neg(a + b)], "log<sub>a</sub> b × log<sub>b</sub> a = <b>1</b>")
            e = R.randint(2, 4)
            return N("<b>%s</b>의 값은? (밑의 변환 공식을 이용하세요)" % lg(a ** e, a), Fr(1, e), [e, -e, Fr(e, a), Fr(1, e + 1)], "log<sub>a<sup>n</sup></sub> a = 1/n · log<sub>a</sub> a = <b>%s</b>" % neg(Fr(1, e)))
        if how == "pow":
            b = R.choice([2, 3, 5, 7])
            x = R.randint(2, 30)
            k = R.choice(["inv", "pow"])
            if k == "inv":
                return N("<b>%d<sup>%s</sup></b>의 값은?" % (b, lg(b, x)), x, [b * x, b ** 2, x + b, Fr(x, b) if Fr(x, b) != x else x + 1], "a<sup>log<sub>a</sub> N</sup> = N이에요. <b>%d</b>" % x)
            e = R.randint(2, 5)
            v = Fr(e)
            return N("<b>%s</b>의 값은?" % lg(b ** 2 if b ** 2 < 100 else b, "%d<sup>%d</sup>" % (b, e)), Fr(e, 2) if b ** 2 < 100 else e, [e, 2 * e, Fr(2, e), e + 2] if b ** 2 < 100 else [e + 1, Fr(e, 2), 2 * e, b * e],
                     "log<sub>a<sup>m</sup></sub> b<sup>n</sup> = (n/m) log<sub>a</sub> b. <b>%s</b>" % (neg(Fr(e, 2)) if b ** 2 < 100 else neg(e)))
        lo = R.randint(-3, 3)
        hi = lo + R.randint(4, 8)
        # log_(x − lo)(hi − x): 밑 x − lo > 0, ≠ 1 → x > lo, x ≠ lo + 1; 진수 hi − x > 0
        c = hi - lo - 2
        return N("<b>%s</b>가 정의되도록 하는 정수 x의 개수는?" % lg(px([1, -lo]), "(%s)" % px([-1, hi])), c, [c + 1, hi - lo, c - 1, hi - lo - 1 if hi - lo - 1 != c else c + 2],
                 "밑: %s &gt; 0, %s ≠ 1, 진수: %s &gt; 0. %s &lt; x &lt; %s, x ≠ %s인 정수는 <b>%d개</b>" % (px([1, -lo]), px([1, -lo]), px([-1, hi]), neg(lo), neg(hi), neg(lo + 1), c), f=lambda v: "%s개" % neg(v))
    return mk


def lg_val(b, x):
    v = math.log(x, b)
    return Fr(v).limit_denominator(12) if abs(v - round(v)) > 1e-9 else round(v)


# ------------------------------------------------------------------ 상용로그
L2, L3, L7 = Fr(3010, 10000), Fr(4771, 10000), Fr(8451, 10000)


def d4(v):
    return ("%.4f" % float(v)).replace("-", "−")


def cl_main(kinds=("calc", "digits", "first", "inv", "life")):
    def mk():
        how = R.choice(kinds)
        if how == "calc":
            a, b, c = R.randint(0, 4), R.randint(0, 3), R.randint(-2, 2)
            if a == b == 0:
                return None
            x = Fr(2) ** a * Fr(3) ** b * Fr(10) ** c
            v = a * L2 + b * L3 + c
            xs = neg(x) if x.denominator == 1 else ("%.6f" % float(x)).rstrip("0")
            if len(xs) > 8:
                return None
            return M("log 2 = 0.3010, log 3 = 0.4771일 때, <b>log %s</b>의 값은?" % xs, d4(v), [d4(a * L3 + b * L2 + c), d4(a * L2 * b * L3 + c) if a and b else d4(v + 1), d4(v - c + (1 if c <= 0 else -1)), d4(a * L2 + b * L3)],
                     "%s = %s이므로 %s. <b>%s</b>" % (xs, " × ".join([s for s in (("2<sup>%d</sup>" % a) if a > 1 else ("2" if a else ""), ("3<sup>%d</sup>" % b) if b > 1 else ("3" if b else ""), ("10<sup>%s</sup>" % neg(c)) if c not in (0, 1) else ("10" if c == 1 else "")) if s]),
                                                     " + ".join([s for s in (("%d log 2" % a) if a > 1 else ("log 2" if a else ""), ("%d log 3" % b) if b > 1 else ("log 3" if b else ""), neg(c) if c else "") if s]).replace("+ −", "− "), d4(v)))
        if how == "digits":
            b, L = R.choice([(2, L2), (3, L3), (7, L7)])
            n = R.randint(10, 60)
            v = n * L
            d = int(v) + 1
            return N("log %d = %s일 때, %d<sup>%d</sup>은 몇 자리의 정수일까요?" % (b, d4(L), b, n), d, [d - 1, d + 1, n, int(v)], "log %d<sup>%d</sup> = %d × %s = %s이므로 %d ≤ log &lt; %d. <b>%d자리</b>" % (b, n, n, d4(L), d4(v), int(v), int(v) + 1, d),
                     f=lambda t: "%s자리" % neg(t))
        if how == "first":
            b, L = R.choice([(2, L2), (3, L3)])
            n = R.randint(5, 40)
            v = n * L
            fr_ = v - int(v)
            # 최고자리 숫자: 10^frac
            dg = int(10 ** float(fr_) + 1e-9)
            return N("log 2 = 0.3010, log 3 = 0.4771일 때, %d<sup>%d</sup>의 최고 자리의 숫자는?" % (b, n), dg, [x for x in range(1, 10) if x != dg][:4], "log %d<sup>%d</sup> = %s의 소수 부분 %s는 log %d와 log %d 사이예요. <b>%d</b>" % (b, n, d4(v), d4(fr_), dg, dg + 1, dg)) if (dg not in (2, 3, 4, 6, 8, 9) or True) else None
        if how == "inv":
            a, b, c = R.randint(0, 3), R.randint(0, 2), R.randint(-2, 3)
            if a == b == 0:
                return None
            x = Fr(2) ** a * Fr(3) ** b * Fr(10) ** c
            v = a * L2 + b * L3 + c
            xs = neg(x) if x.denominator == 1 else ("%.6f" % float(x)).rstrip("0")
            if len(xs) > 8:
                return None
            w = [neg(x * 10) if (x * 10).denominator == 1 else ("%.6f" % float(x * 10)).rstrip("0"), neg(x / 10) if (x / 10).denominator == 1 else ("%.6f" % float(x / 10)).rstrip("0"), neg(Fr(3) ** a * Fr(2) ** b * Fr(10) ** c) if (Fr(3) ** a * Fr(2) ** b * Fr(10) ** c).denominator == 1 else "%.6f" % float(Fr(3) ** a * Fr(2) ** b * Fr(10) ** c)]
            w = [t.rstrip("0").rstrip(".") if "." in t else t for t in w]
            return M("log 2 = 0.3010, log 3 = 0.4771일 때, <b>log x = %s</b>를 만족하는 x의 값은?" % d4(v), xs, w + [neg(int(float(x)) + 1)],
                     "%s = %s이므로 <b>x = %s</b>" % (d4(v), " + ".join(s for s in (("%d log 2" % a) if a > 1 else ("log 2" if a else ""), ("%d log 3" % b) if b > 1 else ("log 3" if b else ""), neg(c) if c else "") if s).replace("+ −", "− "), xs))
        k = R.choice(["db", "ph", "mag"])
        if k == "db":
            n = R.randint(1, 8)
            v = 10 * n
            return N("소리의 세기가 I일 때 소리의 크기는 L = 10 log(I ÷ I<sub>0</sub>) (dB)이에요. 소리의 세기가 10<sup>%d</sup>배가 되면 소리의 크기는 몇 dB 커질까요?" % n, v, [n, 10 ** n if 10 ** n < 10 ** 5 else v * 10, v * 2, n + 10], "10 log 10<sup>%d</sup> = 10 × %d = <b>%d dB</b>" % (n, n, v), f=lambda t: "%s dB" % neg(t))
        if k == "ph":
            n = R.randint(1, 13)
            return N("수용액의 수소 이온 농도가 [H<sup>+</sup>] = 10<sup>−%d</sup>일 때, pH = −log [H<sup>+</sup>]의 값은?" % n, n, [-n, Fr(1, n), 10 - n if 10 - n != n else n + 1, n + 1], "−log 10<sup>−%d</sup> = <b>%d</b>" % (n, n))
        d = R.randint(1, 3)
        v = 10 ** (Fr(3, 2) * d)
        e = Fr(3, 2) * d
        return M("지진의 규모 M과 에너지 E 사이에 log E = 11.8 + 1.5M이 성립해요. 규모가 %d만큼 커지면 에너지는 몇 배가 될까요?" % d, "10<sup>%s</sup>배" % ex(e), ["%s배" % neg(10 ** d), "10<sup>%s</sup>배" % ex(e + 1), "%s배" % neg(e), "10<sup>%s</sup>배" % ex(Fr(2, 3) * d)],
                 "log E의 차가 1.5 × %d = %s이므로 <b>10<sup>%s</sup>배</b>" % (d, neg(e), ex(e)))
    return mk


# ------------------------------------------------------------------ 지수함수와 로그함수
def ef_main(kinds=("prop", "asym", "dom", "val", "cmp", "mm", "inv", "graph")):
    def mk():
        how = R.choice(kinds)
        a = R.choice([2, 3, Fr(1, 2), Fr(1, 3), 4, 5])
        p, q = R.randint(-3, 3), R.randint(-3, 3)
        A = neg(a) if a >= 1 else "(%s)" % neg(a)
        ef = "y = %s<sup>%s</sup>%s" % (A, px([1, -p]), (" + %d" % q) if q > 0 else (" − %d" % -q) if q < 0 else "")
        lf = "y = %s%s" % (lg(a if a >= 1 else neg(a), "(%s)" % px([1, -p]) if p else "x"), (" + %d" % q) if q > 0 else (" − %d" % -q) if q < 0 else "")
        if how == "prop":
            kind = R.choice(["exp", "log"])
            if kind == "exp":
                S_ = [("점 (0, 1)을 지나요", True), ("x의 값이 커지면 y의 값도 커져요", a > 1), ("x의 값이 커지면 y의 값은 작아져요", a < 1), ("x축이 점근선이에요", True), ("치역은 양의 실수 전체예요", True), ("점 (1, 0)을 지나요", False), ("y축이 점근선이에요", False), ("치역은 실수 전체예요", False)]
                f = "y = %s<sup>x</sup>" % A
            else:
                S_ = [("점 (1, 0)을 지나요", True), ("x의 값이 커지면 y의 값도 커져요", a > 1), ("x의 값이 커지면 y의 값은 작아져요", a < 1), ("y축이 점근선이에요", True), ("정의역은 양의 실수 전체예요", True), ("점 (0, 1)을 지나요", False), ("x축이 점근선이에요", False), ("정의역은 실수 전체예요", False)]
                f = "y = " + lg(a if a >= 1 else neg(a), "x")
            want = R.choice([True, False])
            right = [t for t, v in S_ if v == want]
            wrong = [t for t, v in S_ if v != want]
            R.shuffle(right)
            return M("함수 <b>%s</b>에 대한 설명으로 %s 것은?" % (f, "옳은" if want else "옳지 않은"), right[0], wrong, "<b>%s</b>" % right[0])
        if how == "asym":
            kind = R.choice(["exp", "log"])
            if kind == "exp":
                ok = "y = %s" % neg(q)
                return M("함수 <b>%s</b>의 그래프의 점근선의 방정식은?" % ef, ok, ["y = %s" % neg(-q) if q else "y = 1", "x = %s" % neg(p), "y = %s" % neg(p) if p != q else "x = %s" % neg(q), "x = %s" % neg(q) if p != q else "y = %s" % neg(q + 1)], ("y = a<sup>x</sup>의 점근선 y = 0을 y축 방향으로 %s만큼 옮겨요. <b>%s</b>" % (neg(q), ok)) if q else "y축 방향으로 평행이동하지 않았으므로 점근선은 x축 그대로예요. <b>%s</b>" % ok)
            ok = "x = %s" % neg(p)
            return M("함수 <b>%s</b>의 그래프의 점근선의 방정식은?" % lf, ok, ["x = %s" % neg(-p) if p else "x = 1", "y = %s" % neg(q), "x = %s" % neg(q) if p != q else "y = %s" % neg(p + 1), "y = %s" % neg(p) if p != q else "x = %s" % neg(p + 1)], ("y = log<sub>a</sub> x의 점근선 x = 0을 x축 방향으로 %s만큼 옮겨요. <b>%s</b>" % (neg(p), ok)) if p else "x축 방향으로 평행이동하지 않았으므로 점근선은 y축 그대로예요. <b>%s</b>" % ok)
        if how == "dom":
            ok = "x &gt; %s" % neg(p)
            return M("함수 <b>%s</b>의 정의역은?" % lf, ok, ["x &gt; %s" % neg(-p) if p else "x ≥ 0", "x ≥ %s" % neg(p), "y &gt; %s" % neg(q), "x &lt; %s" % neg(p)], "진수 %s &gt; 0. <b>%s</b>" % (px([1, -p]), ok))
        if how == "val":
            kind = R.choice(["exp", "log"])
            if kind == "exp":
                x = p + R.randint(-2, 3)
                v = Fr(a) ** (x - p) + q
                return N("함수 f(x) = %s에 대하여 f(%s)의 값은?" % (ef[4:], neg(x)), v, [Fr(a) ** (x + p) + q if abs(x + p) < 6 else v + 2, Fr(a) ** (x - p) - q if q else v + 1, Fr(a) * (x - p) + q, v * 2], "%s<sup>%s</sup> %s %s = <b>%s</b>" % (A, neg(x - p), "+" if q >= 0 else "−", abs(q), neg(v)))
            if a < 1:
                return None
            e = R.randint(0, 3)
            x = p + int(a) ** e
            v = e + q
            return N("함수 f(x) = %s에 대하여 f(%s)의 값은?" % (lf[4:], neg(x)), v, [e - q if q else v + 1, int(a) ** e + q, v + 1, e], "%s = %d이므로 <b>%s</b>" % (lg(a, int(a) ** e), e, neg(v)))
        if how == "cmp":
            T = [("2<sup>0.5</sup>, 4<sup>0.3</sup>, 8<sup>0.2</sup>", ["2<sup>0.5</sup>", "4<sup>0.3</sup>", "8<sup>0.2</sup>"], [0.5, 0.6, 0.6000001]),
                 ]
            b = R.choice([2, 3])
            e1, e2, e3 = R.sample([Fr(i, 10) for i in range(1, 10)], 3)
            nums = [(b, e1), (b ** 2, e2), (b ** 3, e3)]
            vals = [e1, 2 * e2, 3 * e3]
            if len(set(vals)) < 3:
                return None
            names = ["%d<sup>%s</sup>" % (bb, ("%.1f" % float(ee))) for bb, ee in nums]
            k = R.choice(["max", "min"])
            idx = vals.index(max(vals) if k == "max" else min(vals))
            ok = names[idx]
            return M("세 수 %s 중 가장 %s 수는?" % (", ".join(names), "큰" if k == "max" else "작은"), ok, [n_ for n_ in names if n_ != ok] + ["모두 같아요"],
                     "모두 %d의 거듭제곱으로 바꾸면 지수가 %s. 밑이 1보다 크므로 지수가 클수록 커요. <b>%s</b>" % (b, ", ".join(("%.1f" % float(v)).rstrip("0").rstrip(".") for v in vals), ok))
        if how == "mm":
            b = R.choice([2, 3, Fr(1, 2), Fr(1, 3)])
            lo = R.randint(-2, 1)
            hi = lo + R.randint(1, 3)
            kk = R.choice(["max", "min"])
            vs = [Fr(b) ** lo, Fr(b) ** hi]
            v = max(vs) if kk == "max" else min(vs)
            Bs = neg(b) if b >= 1 else "(%s)" % neg(b)
            return N("%s ≤ x ≤ %s에서 함수 y = %s<sup>x</sup>의 %s은?" % (neg(lo), neg(hi), Bs, "최댓값" if kk == "max" else "최솟값"), v, [min(vs) if kk == "max" else max(vs), Fr(b) ** (lo + hi), Fr(b) * hi, v + 1],
                     "밑이 1보다 %s x = %s일 때 %s. <b>%s</b>" % ("크므로" if b > 1 else "작으므로", neg(hi if (kk == "max") == (b > 1) else lo), "최대" if kk == "max" else "최소", neg(v)))
        if how == "inv":
            b = R.choice([2, 3, 5, 10, Fr(1, 2), Fr(1, 3)])
            B = neg(b) if b >= 1 else "(%s)" % neg(b)
            Lb = neg(b)
            if R.random() < 0.5:
                ok = "y = " + lg(Lb, "x")
                return M("함수 y = %s<sup>x</sup>의 역함수는?" % B, ok, ["y = " + lg("x", Lb), "y = x<sup>%s</sup>" % Lb, "y = %s<sup>−x</sup>" % B, "y = " + lg(Lb, "(−x)")], "x = %s<sup>y</sup>를 y에 대하여 풀면 <b>%s</b>" % (B, ok))
            ok = "y = %s<sup>x</sup>" % B
            return M("함수 y = %s의 역함수는?" % lg(Lb, "x"), ok, ["y = x<sup>%s</sup>" % Lb, "y = %s<sup>−x</sup>" % B, "y = " + lg("x", Lb), "y = %s · x" % Lb], "x = %s를 y에 대하여 풀면 y = %s<sup>x</sup>. <b>%s</b>" % (lg(Lb, "y"), B, ok))
        b = R.choice([2, Fr(1, 2)])
        p, q = R.randint(-2, 2), R.randint(-2, 2)
        kind = R.choice(["exp", "log"])
        if kind == "exp":
            fn = lambda x, b=b, p=p, q=q: float(b) ** (x - p) + q
            Bs = neg(b) if b >= 1 else "(%s)" % neg(b)
            mkf = lambda bb, pp, qq: "y = %s<sup>%s</sup>%s" % (neg(bb) if bb >= 1 else "(%s)" % neg(bb), px([1, -pp]), (" + %d" % qq) if qq > 0 else (" − %d" % -qq) if qq < 0 else "")
            ok = mkf(b, p, q)
            w = [mkf(1 / b, p, q), mkf(b, -p, q) if p else mkf(b, 1, q), mkf(b, p, -q) if q else mkf(b, p, 1), mkf(b, -p, -q) if p or q else mkf(b, 1, 1)]
            pts_ = [(p, 1 + q, "")]
        else:
            fn = lambda x, b=b, p=p, q=q: math.log(x - p, float(b)) + q
            mkf = lambda bb, pp, qq: "y = %s%s" % (lg(neg(bb) if bb >= 1 else neg(bb), "(%s)" % px([1, -pp]) if pp else "x"), (" + %d" % qq) if qq > 0 else (" − %d" % -qq) if qq < 0 else "")
            ok = mkf(b, p, q)
            w = [mkf(1 / b, p, q), mkf(b, -p, q) if p else mkf(b, 1, q), mkf(b, p, -q) if q else mkf(b, p, 1), mkf(b, -p, -q) if p or q else mkf(b, 1, 1)]
            pts_ = [(p + 1, q, "")]
        pic = graph([(fn, BLUE, "")], pts=pts_, label="함수의 그래프")
        if kind == "exp":
            X_ = lambda x: 34 + (x + 5) / 10 * (380 - 68)
            Y_ = lambda y: 360 - 34 + 6 - (y + 5) / 10 * (360 - 68)
            pic = pic.replace("</svg>", "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='6 5'/></svg>" % (X_(-5), Y_(q), X_(5), Y_(q), RED), 1)
        else:
            X_ = lambda x: 34 + (x + 5) / 10 * (380 - 68)
            Y_ = lambda y: 360 - 34 + 6 - (y + 5) / 10 * (360 - 68)
            pic = pic.replace("</svg>", "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='6 5'/></svg>" % (X_(p), Y_(-5), X_(p), Y_(5), RED), 1)
        return M("그래프가 다음과 같은 함수의 식은? (빨간 점선은 점근선, 빨간 점은 그래프 위의 점이에요)%s" % pic, ok, w,
                 "점근선과 지나는 점 %s, 증가·감소를 확인해요. <b>%s</b>" % ("(%s, %s)" % (neg(pts_[0][0]), neg(pts_[0][1])), ok))
    return mk


# ------------------------------------------------------------------ 지수·로그방정식과 부등식
def eq_main(kinds=("expeq", "sub", "logeq", "logsum", "expin", "login", "word")):
    def mk():
        how = R.choice(kinds)
        if how == "expeq":
            b = R.choice([2, 3])
            m, n = R.choice([(1, 2), (2, 1), (1, 3), (2, 3), (3, 2), (1, 1)])
            # (b^m)^(x + c) = (b^n)^k → m(x + c) = n k
            c = R.randint(-3, 3)
            k = R.randint(1, 4)
            x = Fr(n * k, m) - c
            L_, Rr = b ** m, b ** (n * k)
            return N("방정식 <b>%d<sup>%s</sup> = %s</b>의 해는?" % (L_, px([1, c]), neg(Rr)), x, [Fr(n * k, m) + c, Fr(k, 1) - c, x + 1, -x], "%d<sup>%s</sup> = %d<sup>%d</sup> → %s = %d. <b>x = %s</b>" % (b, px([m, m * c]), b, n * k, px([m, m * c]), n * k, neg(x)))
        if how == "sub":
            b = R.choice([2, 3])
            r1, r2 = sorted(R.sample([1, b, b * b, b ** 3], 2))
            # t² − (r1 + r2)t + r1 r2 = 0, t = b^x
            ok = " 또는 ".join("x = %s" % neg(round(math.log(r, b))) for r in (r1, r2))
            return M("방정식 <b>%d<sup>x</sup> − %d · %d<sup>x</sup> + %d = 0</b>의 해는?" % (b * b, r1 + r2, b, r1 * r2), ok, [" 또는 ".join("x = %d" % r for r in (r1, r2)), " 또는 ".join("x = %s" % neg(-round(math.log(r, b))) for r in (r1, r2) if r != 1) if r1 != 1 else "x = 0 또는 x = %s" % neg(-round(math.log(r2, b))), "x = %s" % neg(round(math.log(r2, b)))],
                     "%d<sup>x</sup> = t로 놓으면 t² − %dt + %d = 0, t = %d 또는 %d. <b>%s</b>" % (b, r1 + r2, r1 * r2, r1, r2, ok))
        if how == "logeq":
            b = R.choice([2, 3, 5])
            k = R.randint(1, 3)
            a_, c = R.choice([1, 2, 3]), R.randint(-5, 5)
            x = Fr(b ** k - c, a_)
            return N("방정식 <b>%s = %d</b>의 해는?" % (lg(b, "(%s)" % px([a_, c])), k), x, [Fr(b * k - c, a_), Fr(b ** k + c, a_), Fr(k ** b - c, a_) if k ** b != b ** k else x + 1, x + 1], "진수 %s = %d<sup>%d</sup> = %d. <b>x = %s</b>" % (px([a_, c]), b, k, b ** k, neg(x)))
        if how == "logsum":
            b = R.choice([2, 3])
            r = R.randint(2, 5)
            s = R.randint(1, 3)
            # log_b x + log_b (x − s) = log_b (r(r − s)), x > s
            P = r * (r - s)
            if r <= s or P <= 0:
                return None
            other = s - r  # 다른 근 (음수 또는 진수 조건 위반)
            return N("방정식 <b>%s + %s = %s</b>의 해는?" % (lg(b, "x"), lg(b, "(%s)" % px([1, -s])), lg(b, P)), r, [other, r + s, P, -r], "x(x − %d) = %d → x = %d 또는 x = %s. 진수 조건(x &gt; %d)으로 <b>x = %d</b>" % (s, P, r, neg(other), s, r))
        if how == "expin":
            b = R.choice([2, 3, Fr(1, 2), Fr(1, 3)])
            k = R.randint(-2, 4)
            B = neg(b) if b >= 1 else "(%s)" % neg(b)
            val = Fr(b) ** k
            sym = R.choice(["&gt;", "&lt;"])
            flip = b < 1
            res = sym if not flip else ("&lt;" if sym == "&gt;" else "&gt;")
            ok = "x %s %s" % (res, neg(k))
            other = "&lt;" if res == "&gt;" else "&gt;"
            vs = neg(val) if val.denominator == 1 else fr(val.numerator, val.denominator)
            return M("부등식 <b>%s<sup>x</sup> %s %s</b>의 해는?" % (B, sym, vs), ok, ["x %s %s" % (other, neg(k)), "x %s %s" % (res, neg(-k)) if k else "x %s 1" % res, "x %s %s" % (other, neg(-k)) if k else "x %s 1" % other],
                     "%s = %s<sup>%s</sup>이고 밑이 1보다 %s 부등호 방향이 %s. <b>%s</b>" % (vs, B, neg(k), "작으므로" if flip else "크므로", "바뀌어요" if flip else "그대로예요", ok))
        if how == "login":
            b = R.choice([2, 3, Fr(1, 2)])
            k = R.randint(1, 3)
            c = R.randint(-3, 3)
            Bb = neg(b)
            v = Fr(b) ** k
            lo = -c
            # log_b (x + c) < k
            if b > 1:
                ok = "%s &lt; x &lt; %s" % (neg(lo), neg(v + lo))
                w = ["x &lt; %s" % neg(v + lo), "x &gt; %s" % neg(v + lo), "%s &lt; x &lt; %s" % (neg(lo), neg(k + lo))]
                e = "진수 조건 x &gt; %s와 x + %s &lt; %s에서 <b>%s</b>" % (neg(lo), par(c), neg(v), ok)
            else:
                ok = "x &gt; %s" % neg(v + lo)
                w = ["%s &lt; x &lt; %s" % (neg(lo), neg(v + lo)), "x &lt; %s" % neg(v + lo), "x &gt; %s" % neg(lo)]
                e = "밑이 1보다 작으므로 x + %s &gt; %s. <b>%s</b>" % (par(c), neg(v), ok)
            return M("부등식 <b>%s &lt; %d</b>의 해는?" % (lg(Bb if b >= 1 else neg(b), "(%s)" % px([1, c]) if c else "x"), k), ok, w, e)
        k = R.choice(["bac", "half", "money"])
        if k == "bac":
            n0 = R.choice([100, 200, 500, 1000])
            t = R.choice([10, 15, 20, 30])
            m = R.randint(3, 8)
            return N("어떤 세균의 수가 %d분마다 2배가 돼요. 처음 %d마리였을 때 %d마리가 되는 데 걸리는 시간은 몇 분일까요?" % (t, n0, n0 * 2 ** m), t * m, [t * 2 ** m, m, t * (m + 1), t * m // 2], "%d × 2<sup>x/%d</sup> = %s → 2<sup>x/%d</sup> = 2<sup>%d</sup>. <b>%d분</b>" % (n0, t, neg(n0 * 2 ** m), t, m, t * m), f=lambda v: "%s분" % neg(v))
        if k == "half":
            h = R.choice([5, 8, 10, 20, 30])
            m = R.randint(2, 6)
            return N("반감기가 %d년인 물질이 처음 양의 1/%d이 되는 데 걸리는 시간은?" % (h, 2 ** m), h * m, [h * 2 ** m, h + m, m, h * (m - 1)], "(1/2)<sup>t/%d</sup> = (1/2)<sup>%d</sup>. <b>%d년</b>" % (h, m, h * m), f=lambda v: "%s년" % neg(v))
        r = R.choice([2, 3])
        n = R.randint(2, 4)
        return N("어떤 양이 매년 %d배씩 늘어나요. 처음 양의 %d배 이상이 되려면 최소 몇 년이 걸릴까요?" % (r, r ** n), n, [n + 1, n - 1, r ** n, r * n], "%d<sup>t</sup> ≥ %d<sup>%d</sup> → t ≥ %d. <b>%d년</b>" % (r, r, n, n, n), f=lambda v: "%s년" % neg(v))
    return mk


# ------------------------------------------------------------------ 일반각과 호도법
SPECIAL = [30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]


def rd_main(kinds=("d2r", "r2d", "quad", "cot", "arc", "area")):
    def mk():
        how = R.choice(kinds)
        if how == "d2r":
            d = R.choice(SPECIAL + [15, 72, 18, 36, 20, 40, 100, 540, 720, -60, -150])
            v = Fr(d, 180)
            ok = pis(v)
            return M("<b>%s°</b>를 호도법으로 나타내면?" % neg(d), ok, [pis(Fr(d, 360)), pis(Fr(d, 90)), pis(Fr(180, d)) if d else "π", pis(-v)], "1° = π/180이므로 <b>%s</b>" % ok)
        if how == "r2d":
            v = R.choice([Fr(n, d) for d in (2, 3, 4, 5, 6, 9, 10, 12) for n in range(1, 2 * d) if math.gcd(n, d) == 1])
            d = v * 180
            if d.denominator != 1:
                return None
            ok = "%s°" % neg(d)
            return M("<b>%s</b>를 육십분법으로 나타내면?" % pis(v), ok, ["%s°" % neg(v * 360), "%s°" % neg(v * 90), "%s°" % neg(180 - d) if d != 90 else "180°", "%s°" % neg(Fr(180, v)) if (180 / v).denominator == 1 else "%s°" % neg(d + 180)],
                     "π = 180°를 대입해요. <b>%s</b>" % ok)
        if how == "quad":
            base = R.choice([x for x in range(10, 360, 10) if x % 90])
            n = R.choice([-2, -1, 1, 2, 3])
            d = base + 360 * n
            q = base // 90 + 1
            ok = "제%d사분면" % q
            return M("<b>%s°</b>는 제몇 사분면의 각일까요?" % neg(d), ok, ["제%d사분면" % i for i in (1, 2, 3, 4) if i != q], "%s° = 360° × %s + %d°. <b>%s</b>" % (neg(d), par(n), base, ok))
        if how == "cot":
            base = R.choice([x for x in range(10, 360, 10)])
            n = R.choice([-2, -1, 1, 2, 3])
            d = base + 360 * n
            ok = "360° × n + %d°" % base
            return M("<b>%s°</b>를 나타내는 동경의 일반각은? (n은 정수)" % neg(d), ok, ["360° × n − %d°" % base, "180° × n + %d°" % base, "360° × n + %d°" % (360 - base), "360° × n + %s°" % neg(d) if abs(d) >= 360 else "90° × n + %d°" % base],
                     "%s° = 360° × %s + %d°. <b>%s</b>" % (neg(d), par(n), base, ok))
        r = R.randint(2, 12)
        th = R.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(5, 6), Fr(1, 1), Fr(3, 2)])
        if how == "arc":
            v = r * th
            ok = pis(v)
            return M("반지름의 길이가 %d이고 중심각의 크기가 %s인 부채꼴의 호의 길이는?" % (r, pis(th)), ok, [pis(r * r * th / 2), pis(2 * r * th), pis(th), pis(v / 2) if v != 0 else "1"], "l = rθ = %d × %s. <b>%s</b>" % (r, pis(th), ok))
        v = Fr(r * r, 2) * th
        ok = pis(v)
        return M("반지름의 길이가 %d이고 중심각의 크기가 %s인 부채꼴의 넓이는?" % (r, pis(th)), ok, [pis(r * th), pis(r * r * th), pis(v * 2 / r) if v * 2 / r != v else pis(v + 1), pis(Fr(r * r, 4) * th)], "S = ½r²θ = ½ × %d × %s. <b>%s</b>" % (r * r, pis(th), ok))
    return mk


# ------------------------------------------------------------------ 삼각함수
FN = {"sin": "sin", "cos": "cos", "tan": "tan"}


def tv(fn, deg):
    return vhtml(trig(fn, deg))


def t_main(kinds=("val", "sign", "find", "ident", "sumprod")):
    def mk():
        how = R.choice(kinds)
        if how == "val":
            d = R.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330, 390, 405, -30, -45, -60, -120, 480, -210])
            fn = R.choice(["sin", "cos", "tan"])
            if trig(fn, d) is None:
                return None
            ok = tv(fn, d)
            alts = set()
            for f2 in ("sin", "cos", "tan"):
                for d2 in (d, -d, 180 - d, d + 90):
                    t2 = trig(f2, d2)
                    if t2 is not None:
                        alts.add(vhtml(t2))
            alts.discard(ok)
            ang = pis(Fr(d, 180)) if d > 0 else "(%s)" % pis(Fr(d, 180))
            return M("<b>%s %s</b>의 값은?" % (fn, ang), ok, sorted(alts), "%s = %s°의 동경이 있는 사분면과 기준각으로 구해요. <b>%s</b>" % (pis(Fr(d, 180)), neg(d), ok))
        if how == "sign" and R.random() < 0.7:
            q = R.randint(1, 4)
            SG = {1: {"sin": 1, "cos": 1, "tan": 1}, 2: {"sin": 1, "cos": -1, "tan": -1}, 3: {"sin": -1, "cos": -1, "tan": 1}, 4: {"sin": -1, "cos": 1, "tan": -1}}
            f1, f2 = R.choice([("sin", "cos"), ("sin", "tan"), ("cos", "tan")])
            cond = "%s θ %s 0, %s θ %s 0" % (f1, "&gt;" if SG[q][f1] > 0 else "&lt;", f2, "&gt;" if SG[q][f2] > 0 else "&lt;")
            ok = "제%d사분면" % q
            return M("<b>%s</b>을 만족하는 각 θ는 제몇 사분면의 각일까요?" % cond, ok, ["제%d사분면" % i for i in (1, 2, 3, 4) if i != q], "제1사분면은 모두, 제2사분면은 sin, 제3사분면은 tan, 제4사분면은 cos만 양수예요. <b>%s</b>" % ok)
        if how == "sign":
            q = R.randint(1, 4)
            k = R.choice(["sin", "cos", "tan"])
            sgn = {1: {"sin": "+", "cos": "+", "tan": "+"}, 2: {"sin": "+", "cos": "−", "tan": "−"}, 3: {"sin": "−", "cos": "−", "tan": "+"}, 4: {"sin": "−", "cos": "+", "tan": "−"}}[q]
            ok = "sin θ %s 0, cos θ %s 0, tan θ %s 0" % tuple("&gt;" if sgn[f] == "+" else "&lt;" for f in ("sin", "cos", "tan"))
            alts = ["sin θ %s 0, cos θ %s 0, tan θ %s 0" % tuple("&gt;" if {1: {"sin": "+", "cos": "+", "tan": "+"}, 2: {"sin": "+", "cos": "−", "tan": "−"}, 3: {"sin": "−", "cos": "−", "tan": "+"}, 4: {"sin": "−", "cos": "+", "tan": "−"}}[qq][f] == "+" else "&lt;" for f in ("sin", "cos", "tan")) for qq in (1, 2, 3, 4) if qq != q]
            return M("θ가 제%d사분면의 각일 때, 삼각함수의 부호로 옳은 것은?" % q, ok, alts, "제%d사분면에서 양수인 것은 %s. <b>%s</b>" % (q, {1: "모두", 2: "sin", 3: "tan", 4: "cos"}[q], ok))
        if how == "find":
            a, b, c = R.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17), (7, 24, 25)])
            q = R.randint(1, 4)
            sx = 1 if q in (1, 4) else -1
            sy = 1 if q in (1, 2) else -1
            given = R.choice(["sin", "cos"])
            want = R.choice(["cos", "tan"] if given == "sin" else ["sin", "tan"])
            vals = {"sin": Fr(sy * b, c), "cos": Fr(sx * a, c), "tan": Fr(sy * b, sx * a)}
            v = vals[want]
            rng = {1: "0 &lt; θ &lt; π/2", 2: "π/2 &lt; θ &lt; π", 3: "π &lt; θ &lt; 3π/2", 4: "3π/2 &lt; θ &lt; 2π"}[q]
            return N("%s이고 %s θ = %s일 때, %s θ의 값은?" % (rng, given, neg(vals[given]), want), v, [-v, 1 / v if v else 1, Fr(abs(v.numerator), abs(v.denominator)) if v < 0 else Fr(a, c) if v != Fr(a, c) else -v * 2, vals["sin" if want != "sin" else "cos"]],
                     "sin²θ + cos²θ = 1과 사분면의 부호로 구해요. <b>%s</b>" % neg(v))
        if how == "ident":
            I = [("sin²θ + cos²θ의 값은?", "1", ["0", "2", "sin 2θ"]), ("tan θ와 같은 식은?", "sin θ ÷ cos θ", ["cos θ ÷ sin θ", "sin θ × cos θ", "1 ÷ sin θ"]),
                 ("(1 − cos²θ) ÷ sin θ를 간단히 하면? (sin θ ≠ 0)", "sin θ", ["cos θ", "1", "tan θ"]), ("(sin θ + cos θ)² + (sin θ − cos θ)²의 값은?", "2", ["1", "0", "4 sin θ cos θ"]),
                 ("1 + tan²θ와 같은 식은?", "1 ÷ cos²θ", ["1 ÷ sin²θ", "sin²θ", "cos²θ"]), ("sin θ ÷ tan θ를 간단히 하면? (cos θ ≠ 0, sin θ ≠ 0)", "cos θ", ["sin θ", "1", "tan θ"]),
                 ("cos²θ − sin²θ + 2sin²θ의 값은?", "1", ["0", "cos 2θ", "2"]), ("(1 + sin θ)(1 − sin θ)를 간단히 하면?", "cos²θ", ["sin²θ", "1", "tan²θ"]),
                 ("sin(−θ)와 같은 것은?", "−sin θ", ["sin θ", "cos θ", "−cos θ"]), ("cos(−θ)와 같은 것은?", "cos θ", ["−cos θ", "sin θ", "−sin θ"]),
                 ("sin(π − θ)와 같은 것은?", "sin θ", ["−sin θ", "cos θ", "−cos θ"]), ("cos(π + θ)와 같은 것은?", "−cos θ", ["cos θ", "sin θ", "−sin θ"]),
                 ("sin(π/2 − θ)와 같은 것은?", "cos θ", ["sin θ", "−cos θ", "tan θ"]), ("tan(π + θ)와 같은 것은?", "tan θ", ["−tan θ", "1 ÷ tan θ", "−1 ÷ tan θ"])]
            q, ok, w = R.choice(I)
            return M(q, ok, w, "sin²θ + cos²θ = 1, tan θ = sin θ ÷ cos θ와 각의 변환을 이용해요. <b>%s</b>" % ok)
        dd = R.randint(2, 7)
        s = Fr(R.randint(1, dd - 1), dd) * R.choice([1, 1, -1])
        k = R.choice(["prod", "cube", "diff"])
        if k == "diff":
            p = (s * s - 1) / 2
            v = 1 - 2 * p
            return N("sin θ + cos θ = %s일 때, (sin θ − cos θ)²의 값은?" % neg(s), v, [s * s, 1 + 2 * p, 2 - s * s + 1, v / 2], "sin θ cos θ = %s이므로 1 − 2sin θ cos θ = <b>%s</b>" % (neg(p), neg(v)))
        p = (s * s - 1) / 2
        if k == "prod":
            return N("sin θ + cos θ = %s일 때, sin θ cos θ의 값은?" % neg(s), p, [(s * s + 1) / 2, s * s - 1, -p, s * s / 2], "양변을 제곱하면 1 + 2sin θ cos θ = %s. <b>%s</b>" % (neg(s * s), neg(p)))
        v = s ** 3 - 3 * p * s
        return N("sin θ + cos θ = %s일 때, sin³θ + cos³θ의 값은?" % neg(s), v, [s ** 3, s * (1 + p), s ** 3 + 3 * p * s, v + Fr(1, 2)], "sin θ cos θ = %s이고 a³ + b³ = (a + b)³ − 3ab(a + b). <b>%s</b>" % (neg(p), neg(v)))
    return mk


# ------------------------------------------------------------------ 삼각함수의 그래프
def tg_main(kinds=("period", "mm", "val", "read", "tan", "eq", "ineq")):
    def mk():
        how = R.choice(kinds)
        a = R.choice([1, 2, 3, -2, Fr(1, 2)])
        b = R.choice([1, 2, 3, 4, Fr(1, 2)])
        c = R.randint(-3, 3)
        fn = R.choice(["sin", "cos"])
        A = "" if a == 1 else ("−" if a == -1 else neg(a))
        b = Fr(b)
        B = "x" if b == 1 else ("%sx" % neg(b) if b.denominator == 1 else fr("x", b.denominator))
        f = "y = %s%s %s%s" % (A, fn, B, (" + %d" % c) if c > 0 else (" − %d" % -c) if c < 0 else "")
        if how == "period":
            v = Fr(2) / b
            ok = pis(v)
            return M("함수 <b>%s</b>의 주기는?" % f, ok, [pis(2 * b), pis(1 / b) if 1 / b != v else pis(4 / b), pis(v * 2), neg(abs(a))], "주기는 2π ÷ |%s| = <b>%s</b>" % (neg(b), ok))
        if how == "mm":
            k = R.choice(["max", "min"])
            v = abs(a) + c if k == "max" else -abs(a) + c
            return N("함수 <b>%s</b>의 %s은?" % (f, "최댓값" if k == "max" else "최솟값"), v, [-v if v else 1, abs(a) * (1 if k == "max" else -1), a + c if a + c != v else c, v + 1, c], "최댓값 |a| + c = %s, 최솟값 −|a| + c = %s. <b>%s</b>" % (neg(abs(a) + c), neg(-abs(a) + c), neg(v)))
        if how == "val":
            d = R.choice([0, 30, 45, 60, 90, 120, 150, 180, 270])
            x = Fr(d, 180) / b
            tval = trig(fn, d)
            if tval is None:
                return None
            from pc_common import FLOAT
            fv_ = tval[0] * FLOAT[tval[1]] * float(a) + c
            if abs(fv_ - round(fv_)) > 1e-9 and tval[1] not in ("1/2",):
                return None
            v = Fr(tval[0]) * (Fr(1, 2) if tval[1] == "1/2" else Fr(int(FLOAT[tval[1]]))) * a + c if tval[1] in ("1/2", "1", "0") else None
            if v is None:
                return None
            return N("함수 f(x) = %s에 대하여 f(%s)의 값은?" % (f[4:], pis(x)), v, [-v if v else 1, v + 1, a + c, c], "%s %s = %s이므로 <b>%s</b>" % (fn, pis(Fr(d, 180)), vhtml(tval), neg(v)))
        if how == "tan":
            bb = R.choice([1, 2, 3, Fr(1, 2)])
            Bt = "x" if bb == 1 else ("%sx" % neg(bb) if Fr(bb).denominator == 1 else fr("x", 2))
            k = R.choice(["p", "asym"])
            if k == "p":
                v = Fr(1) / bb
                ok = pis(v)
                return M("함수 <b>y = tan %s</b>의 주기는?" % Bt, ok, [pis(2 / Fr(bb)), pis(Fr(bb)) if Fr(bb) != v else pis(v * 4), pis(v / 2)], "tan의 주기는 π ÷ |%s| = <b>%s</b>" % (neg(bb), ok))
            v = Fr(1, 2) / bb
            ok = "x = %s + %s (n은 정수)" % (pis(v), "nπ" if bb == 1 else pis(Fr(1) / bb).replace("π", "π") + "n" if False else "%sn" % (pis(Fr(1) / bb) if Fr(1) / bb != 1 else "π"))
            ok = "x = %s × n + %s" % (pis(Fr(1) / bb), pis(v)) if bb != 1 else "x = nπ + %s" % pis(v)
            w = ["x = nπ" if bb == 1 else "x = %s × n" % pis(Fr(1) / bb), "x = nπ + %s" % pis(v * 2) if bb == 1 else "x = %s × n + %s" % (pis(Fr(1) / bb), pis(v * 2)), "x = 2nπ + %s" % pis(v), "y = %s" % pis(v)]
            return M("함수 <b>y = tan %s</b>의 그래프의 점근선의 방정식은? (n은 정수)" % Bt, ok, w, "%s = π/2 + nπ일 때 정의되지 않아요. <b>%s</b>" % (Bt, ok))
        if how == "read":
            aa = R.choice([1, 2, 3])
            bb = R.choice([1, 2, Fr(1, 2)])
            cc = R.randint(-1, 1)
            fn2 = R.choice(["sin", "cos"])
            ffn = (lambda x, aa=aa, bb=bb, cc=cc: aa * math.sin(float(bb) * x) + cc) if fn2 == "sin" else (lambda x, aa=aa, bb=bb, cc=cc: aa * math.cos(float(bb) * x) + cc)
            def plab(k):
                n = round(k / (math.pi / 2))
                f_ = Fr(n, 2)
                if f_ == 0:
                    return "0"
                top = ("" if abs(f_.numerator) == 1 else str(abs(f_.numerator))) + "π"
                return ("−" if f_ < 0 else "") + (top if f_.denominator == 1 else top + "/2")
            pic = graph([(ffn, BLUE, "")], (-2 * math.pi, 2 * math.pi, math.pi / 2), (-4, 4, 1), label="삼각함수의 그래프", xlab=plab)
            # 눈금을 π 단위로: 라벨 교체
            for kk, lab in ((1.5708, "π/2"), (3.1416, "π"), (4.7124, "3π/2"), (6.2832, "2π")):
                pass
            mkf = lambda A_, B_, C_, F_: "y = %s%s %s%s" % ("" if A_ == 1 else neg(A_), F_, "x" if B_ == 1 else ("%sx" % neg(B_) if Fr(B_).denominator == 1 else fr("x", 2)), (" + %d" % C_) if C_ > 0 else (" − %d" % -C_) if C_ < 0 else "")
            ok = mkf(aa, bb, cc, fn2)
            other = "cos" if fn2 == "sin" else "sin"
            w = [mkf(aa, 2 * bb if bb != 2 else Fr(1, 2), cc, fn2), mkf(aa + 1 if aa < 3 else 1, bb, cc, fn2), mkf(aa, bb, cc, other), mkf(aa, bb, -cc if cc else 1, fn2)]
            return M("그래프가 다음과 같은 함수의 식은? (가로축의 눈금 한 칸은 π/2예요)%s" % pic, ok, w, "최댓값·최솟값에서 a와 c, 주기에서 b, x = 0에서의 값으로 sin과 cos을 구별해요. <b>%s</b>" % ok)
        if how == "eq":
            fn2 = R.choice(["sin", "cos", "tan"])
            H, R2, R3 = fr(1, 2), fr("√2", 2), fr("√3", 2)
            vals = {"sin": [(H, [30, 150], "2 sin x = 1"), (R2, [45, 135], "√2 sin x = 1"), (R3, [60, 120], "2 sin x = √3"), ("−" + H, [210, 330], "2 sin x = −1"), ("−" + R2, [225, 315], "√2 sin x = −1"), ("−" + R3, [240, 300], "2 sin x = −√3")],
                    "cos": [(H, [60, 300], "2 cos x = 1"), (R2, [45, 315], "√2 cos x = 1"), (R3, [30, 330], "2 cos x = √3"), ("−" + H, [120, 240], "2 cos x = −1"), ("−" + R2, [135, 225], "√2 cos x = −1"), ("−" + R3, [150, 210], "2 cos x = −√3")],
                    "tan": [("1", [45, 225], "tan x − 1 = 0"), ("√3", [60, 240], "tan x − √3 = 0"), (fr("√3", 3), [30, 210], "√3 tan x = 1"), ("−1", [135, 315], "tan x + 1 = 0"), ("−√3", [120, 300], "tan x + √3 = 0"), ("−" + fr("√3", 3), [150, 330], "√3 tan x = −1")]}[fn2]
            v, ds, alt_form = R.choice(vals)
            form = "%s x = %s" % (fn2, v) if R.random() < 0.5 else alt_form
            ok = "x = %s 또는 x = %s" % (pis(Fr(ds[0], 180)), pis(Fr(ds[1], 180)))
            sh = lambda d: d % 360
            w = ["x = %s" % pis(Fr(ds[0], 180)), "x = %s 또는 x = %s" % (pis(Fr(sh(180 - ds[0]), 180)), pis(Fr(sh(180 + ds[0]), 180))),
                 "x = %s 또는 x = %s" % (pis(Fr(sh(360 - ds[0]), 180)), pis(Fr(sh(ds[0] + 180), 180))), "x = %s 또는 x = %s" % (pis(Fr(sh(ds[0] + 90), 180)), pis(Fr(sh(ds[1] + 90), 180)))]
            w = [x for x in w if x != ok and x != "x = %s 또는 x = %s" % (pis(Fr(ds[1], 180)), pis(Fr(ds[0], 180)))]
            return M("0 ≤ x &lt; 2π일 때, 방정식 <b>%s</b>의 해는?" % form, ok, w, "%s x = %s가 되는 두 각을 단위원이나 그래프에서 찾아요. <b>%s</b>" % (fn2, v, ok))
        fn2 = R.choice(["sin", "cos"])
        strict = R.random() < 0.5
        lt, le = ("&lt;", "≤") if True else None
        o = "&lt;" if strict else "≤"
        if fn2 == "sin":
            v, (d1, d2) = R.choice([(fr(1, 2), (30, 150)), (fr("√2", 2), (45, 135)), (fr("√3", 2), (60, 120))])
        else:
            v, (d1, d2) = R.choice([(fr(1, 2), (60, 300)), (fr("√2", 2), (45, 315)), (fr("√3", 2), (30, 330))])
        big = R.choice([True, False])
        sym = ("&gt;" if strict else "≥") if big else ("&lt;" if strict else "≤")
        A_, B_ = pis(Fr(d1, 180)), pis(Fr(d2, 180))
        inner = "%s %s x %s %s" % (A_, o, o, B_)
        outer = "0 ≤ x %s %s 또는 %s %s x &lt; 2π" % ("≤" if not strict else "&lt;", A_, B_, "≤" if not strict else "&lt;")
        inside_big = fn2 == "sin"
        ok = inner if big == inside_big else outer
        alt = outer if ok == inner else inner
        o2 = "≤" if strict else "&lt;"
        w = [alt, ("%s %s x %s %s" % (A_, o2, o2, B_)) if ok == inner else "0 ≤ x %s %s 또는 %s %s x &lt; 2π" % (o2, A_, B_, o2),
             "%s %s x %s %s" % (pis(Fr(d1, 90)) if d1 * 2 < 360 else A_, o, o, pis(Fr(d2, 90)) if d2 * 2 < 360 else pis(Fr(d2 - 30, 180)))]
        return M("0 ≤ x &lt; 2π일 때, 부등식 <b>%s x %s %s</b>의 해는?" % (fn2, sym, v), ok, w, "y = %s x의 그래프가 직선 y = %s보다 %s 있는 범위예요%s. <b>%s</b>" % (fn2, v, "위에" if big else "아래에", "" if strict else "(만나는 점 포함)", ok))
    return mk


# ------------------------------------------------------------------ 사인법칙과 코사인법칙
def lw_main(kinds=("sin", "R", "cosside", "cosang", "area", "word")):
    def mk():
        how = R.choice(kinds)
        if how == "sin":
            A, B = R.sample([30, 45, 60, 90, 120, 135, 150], 2)
            if A + B >= 180:
                return None
            a = R.choice([2, 4, 6, 8, 10, 12])
            # b = a sinB / sinA
            from pc_common import FLOAT
            sA, sB = FLOAT[trig("sin", A)[1]], FLOAT[trig("sin", B)[1]]
            v = a * sB / sA
            # 표현: 정확값 surd
            def ex_(x):
                for k in range(1, 50):
                    for rr in (1, 2, 3, 6):
                        if abs(x - k * math.sqrt(rr)) < 1e-9:
                            return surd(k, rr)
                        if abs(x - k * math.sqrt(rr) / 2) < 1e-9:
                            return fr(surd(k, rr), 2)
                        if abs(x - k * math.sqrt(rr) / 3) < 1e-9:
                            return fr(surd(k, rr), 3)
                return None
            ok = ex_(v)
            if ok is None:
                return None
            w = [ex_(a * sA / sB), ex_(a * sB), ex_(v * 2), ex_(a * sA)]
            return M("삼각형 ABC에서 a = %d, A = %d°, B = %d°일 때, b의 값은?" % (a, A, B), ok, [x for x in w if x and x != ok] + ["%d" % (a + 1)], "a ÷ sin A = b ÷ sin B → b = %d × sin %d° ÷ sin %d°. <b>%s</b>" % (a, B, A, ok))
        if how == "R":
            A = R.choice([30, 45, 60, 90, 120, 135, 150])
            Rr = R.randint(1, 8)
            from pc_common import FLOAT
            v = 2 * Rr * FLOAT[trig("sin", A)[1]]
            m = {30: "%d" % Rr, 150: "%d" % Rr, 90: "%d" % (2 * Rr), 45: surd(Rr, 2), 135: surd(Rr, 2), 60: surd(Rr, 3), 120: surd(Rr, 3)}[A]
            k = R.choice(["a", "R"])
            if k == "a":
                return M("삼각형 ABC의 외접원의 반지름의 길이가 %d이고 A = %d°일 때, a의 값은?" % (Rr, A), m, [x for x in ("%d" % Rr, "%d" % (2 * Rr), surd(Rr, 2), surd(Rr, 3), surd(2 * Rr, 3), "%d" % (4 * Rr)) if x != m], "a = 2R sin A = 2 × %d × sin %d°. <b>%s</b>" % (Rr, A, m))
            return N("삼각형 ABC에서 a = %s, A = %d°일 때, 외접원의 반지름의 길이는?" % (m, A), Rr, [2 * Rr, Fr(Rr, 2), Rr + 1, Rr * 3], "2R = a ÷ sin A. <b>R = %d</b>" % Rr)
        if how == "cosside":
            C = R.choice([60, 90, 120])
            a, b = R.randint(2, 9), R.randint(2, 9)
            cosC = {60: Fr(1, 2), 90: 0, 120: Fr(-1, 2)}[C]
            c2 = a * a + b * b - 2 * a * b * cosC
            ok = surd(1, int(c2))
            w = [surd(1, int(a * a + b * b + 2 * a * b * cosC)) if a * a + b * b + 2 * a * b * cosC > 0 else "0", surd(1, a * a + b * b), neg(a + b), surd(1, int(c2) + 1)]
            return M("삼각형 ABC에서 a = %d, b = %d, C = %d°일 때, c의 값은?" % (a, b, C), ok, w, "c² = a² + b² − 2ab cos C = %d + %d − 2 × %d × %d × cos %d° = %d. <b>%s</b>" % (a * a, b * b, a, b, C, int(c2), ok))
        if how == "cosang":
            T = [(3, 5, 7, 120), (5, 8, 7, 60), (3, 8, 7, 60), (5, 3, 7, 120), (7, 8, 13, 120), (8, 15, 13, 60), (5, 21, 19, 60), (7, 15, 13, 60), (3, 5, 4, 90), (6, 10, 14, 120), (16, 10, 14, 60)]
            a, b, c, C = R.choice(T)
            ok = "%d°" % C
            return M("세 변의 길이가 %d, %d, %d인 삼각형에서 가장 긴 변의 대각의 크기는?" % (a, b, c) if c == max(a, b, c) else "삼각형 ABC에서 a = %d, b = %d, c = %d일 때, C의 크기는?" % (a, b, c), ok, ["%d°" % x for x in (30, 45, 60, 90, 120, 135, 150) if x != C][:4],
                     "cos C = (a² + b² − c²) ÷ 2ab = %s. <b>%s</b>" % (neg(Fr(a * a + b * b - c * c, 2 * a * b)), ok))
        if how == "area":
            C = R.choice([30, 45, 60, 90, 120, 135, 150])
            a, b = R.randint(2, 10), R.randint(2, 10)
            m = {30: Fr(1, 2), 150: Fr(1, 2), 90: 1}.get(C)
            if m is not None:
                v = Fr(a * b, 2) * m
                ok = neg(v)
            else:
                rr = 2 if C in (45, 135) else 3
                v = Fr(a * b, 4)
                ok = fr(surd(v.numerator, rr), v.denominator) if v.denominator > 1 else surd(v, rr)
            w = [neg(a * b), neg(Fr(a * b, 2)), neg(Fr(a * b, 4)) if ok != neg(Fr(a * b, 4)) else neg(a * b * 2), surd(a * b, 3)]
            return M("삼각형 ABC에서 a = %d, b = %d, C = %d°일 때, 삼각형의 넓이는?" % (a, b, C), ok, w, "S = ½ab sin C. <b>%s</b>" % ok)
        k = R.choice(["river", "tri"])
        if k == "river":
            d = R.choice([10, 20, 30, 40, 50, 60, 80, 100])
            A, B = R.choice([(45, 60), (30, 105), (60, 75), (45, 105), (30, 120), (60, 45)])
            Cc = 180 - A - B
            from pc_common import FLOAT
            if trig("sin", Cc) is None:
                return None
            try:
                sC = FLOAT[trig("sin", Cc)[1]]
            except Exception:
                return None
            sB = math.sin(math.radians(B))
            v = d * sB / sC
            return M("강 건너편 지점 C까지의 거리를 구하려고 해요. 이쪽의 두 지점 A, B 사이의 거리는 %d m이고 ∠CAB = %d°, ∠CBA = %d°예요. AC의 길이를 구하는 식은?" % (d, A, B), "%d × sin %d° ÷ sin %d°" % (d, B, Cc),
                     ["%d × sin %d° ÷ sin %d°" % (d, Cc, B), "%d × sin %d° ÷ sin %d°" % (d, A, Cc), "%d × cos %d° ÷ cos %d°" % (d, B, Cc)], "∠C = %d°이고 사인법칙 AC ÷ sin B = AB ÷ sin C. <b>%d × sin %d° ÷ sin %d°</b>" % (Cc, d, B, Cc))
        a, b = R.randint(3, 9) * 10, R.randint(3, 9) * 10
        C = R.choice([60, 120])
        c2 = a * a + b * b - 2 * a * b * Fr(1 if C == 60 else -1, 2)
        ok = surd(1, int(c2)) + " m"
        return M("호수의 양 끝 A, B 사이의 거리를 구하려고 해요. 한 지점 C에서 CA = %d m, CB = %d m, ∠ACB = %d°일 때 AB의 길이는?" % (a, b, C), ok, [surd(1, a * a + b * b) + " m", surd(1, int(a * a + b * b + (a * b if C == 60 else -a * b))) + " m", "%d m" % (a + b)],
                 "코사인법칙: AB² = %d + %d − 2 × %d × %d × cos %d° = %d. <b>%s</b>" % (a * a, b * b, a, b, C, int(c2), ok))
    return mk


# ------------------------------------------------------------------ 등차수열·등비수열
def ar_main(kinds=("term", "find", "ad", "sum", "sumf", "mean", "first")):
    def mk():
        how = R.choice(kinds)
        a, d = R.randint(-10, 10), nz(-5, 6)
        if how == "term":
            n = R.randint(8, 40)
            v = a + (n - 1) * d
            return N("첫째항이 %s, 공차가 %s인 등차수열의 제%d항은?" % (neg(a), neg(d), n), v, [a + n * d, a * d * (n - 1) if abs(a * d * (n - 1)) < 1000 else v + d, a + (n - 2) * d, (n - 1) * d], "a<sub>n</sub> = a + (n − 1)d = %s + %d × %s. <b>%s</b>" % (neg(a), n - 1, par(d), neg(v)))
        if how == "find":
            i, j = sorted(R.sample(range(2, 12), 2))
            ai, aj = a + (i - 1) * d, a + (j - 1) * d
            n = R.randint(12, 30)
            v = a + (n - 1) * d
            return N("등차수열 {a<sub>n</sub>}에서 a<sub>%d</sub> = %s, a<sub>%d</sub> = %s일 때, a<sub>%d</sub>의 값은?" % (i, neg(ai), j, neg(aj), n), v, [a + n * d, v - d, ai + (n - i) * (aj - ai), aj + (n - j) * d * 2],
                     "공차 = (%s − %s) ÷ %d = %s, 첫째항 = %s. <b>%s</b>" % (neg(aj), par(ai), j - i, neg(d), neg(a), neg(v)))
        if how == "ad":
            seq = [a + k * d for k in range(4)]
            k = R.choice(["d", "n"])
            if k == "d":
                return N("등차수열 %s, … 의 공차는?" % ", ".join(neg(x) for x in seq), d, [-d, seq[1] + seq[0], seq[2] // seq[0] if seq[0] and seq[2] % seq[0] == 0 else d + 1, d * 2], "이웃한 두 항의 차예요. <b>%s</b>" % neg(d))
            n = R.randint(10, 30)
            last = a + (n - 1) * d
            return N("등차수열 %s, …, %s의 항의 개수는?" % (", ".join(neg(x) for x in seq[:3]), neg(last)), n, [n - 1, n + 1, abs(last - a) // abs(d), abs(last)], "%s = %s + (n − 1) × %s → <b>n = %d</b>" % (neg(last), neg(a), par(d), n), f=lambda v: "%s개" % neg(v))
        if how == "sum":
            n = R.randint(8, 30)
            S = n * (2 * a + (n - 1) * d) // 2
            return N("첫째항이 %s, 공차가 %s인 등차수열의 첫째항부터 제%d항까지의 합은?" % (neg(a), neg(d), n), S, [n * (2 * a + (n - 1) * d), n * (a + (a + n * d)) // 2, S + d, n * a], "S<sub>n</sub> = n{2a + (n − 1)d} ÷ 2. <b>%s</b>" % neg(S))
        if how == "sumf":
            n = R.randint(10, 50)
            k = R.choice(["odd", "nat", "mult"])
            if k == "odd":
                return N("1부터 %d까지의 홀수의 합은?" % (2 * n - 1), n * n, [n * (n + 1), n * (2 * n - 1), (2 * n - 1) * n // 2 + 1, n * n - 1], "1 + 3 + … + %d = %d × (1 + %d) ÷ 2 = <b>%s</b>" % (2 * n - 1, n, 2 * n - 1, neg(n * n)))
            if k == "nat":
                return N("1부터 %d까지의 자연수의 합은?" % n, n * (n + 1) // 2, [n * n, n * (n - 1) // 2, n * (n + 1), n * (n + 1) // 2 + n], "%d × (1 + %d) ÷ 2 = <b>%s</b>" % (n, n, neg(n * (n + 1) // 2)))
            m = R.randint(3, 7)
            top = m * R.randint(10, 20)
            cnt = top // m
            v = m * cnt * (cnt + 1) // 2
            return N("%d 이하의 %d의 양의 배수의 합은?" % (top, m), v, [m * cnt * cnt, v - top, cnt * (cnt + 1) // 2, v + m], "%d + %d + … + %d (%d개)의 합. <b>%s</b>" % (m, 2 * m, top, cnt, neg(v)))
        if how == "mean":
            x, y = sorted(R.sample(range(-20, 30), 2))
            if (x + y) % 2:
                return None
            return N("세 수 %s, a, %s가 이 순서대로 등차수열을 이룰 때, a의 값은?" % (neg(x), neg(y)), (x + y) // 2, [y - x, (y - x) // 2, x + y, (x + y) // 2 + 1], "등차중항: 2a = %s + %s. <b>%s</b>" % (neg(x), par(y), neg((x + y) // 2)))
        a, d = R.randint(-60, -10), R.randint(2, 7)
        n = -a // d + 1 + (1 if -a % d == 0 else 0)
        while a + (n - 1) * d <= 0:
            n += 1
        while n > 1 and a + (n - 2) * d > 0:
            n -= 1
        return N("첫째항이 %s, 공차가 %d인 등차수열에서 처음으로 양수가 되는 항은 제몇 항일까요?" % (neg(a), d), n, [n - 1, n + 1, -a // d, n + 2], "a<sub>n</sub> = %s + (n − 1) × %d &gt; 0을 만족하는 가장 작은 n. <b>제%d항</b>" % (neg(a), d, n), f=lambda v: "제%s항" % neg(v))
    return mk


def ge_main(kinds=("term", "find", "r", "sum", "mean", "word", "inf")):
    def mk():
        how = R.choice(kinds)
        a = R.choice([1, 2, 3, -1, -2, 4, 5])
        r = R.choice([2, 3, -2, -3, Fr(1, 2), Fr(-1, 2), Fr(1, 3)])
        if how == "term":
            n = R.randint(4, 8)
            v = a * Fr(r) ** (n - 1)
            if abs(v) > 10 ** 5:
                return None
            return N("첫째항이 %s, 공비가 %s인 등비수열의 제%d항은?" % (neg(a), neg(r), n), v, [a * Fr(r) ** n, a * r * (n - 1), a * Fr(r) ** (n - 2), -v], "a<sub>n</sub> = ar<sup>n−1</sup> = %s × %s<sup>%d</sup>. <b>%s</b>" % (neg(a), par(r) if not isinstance(r, Fr) or r.denominator == 1 else "(%s)" % neg(r), n - 1, neg(v)))
        if how == "find":
            if not isinstance(r, int) or abs(r) < 2:
                return None
            i, j = R.choice([(2, 4), (2, 5), (3, 5), (1, 4), (3, 6)])
            ai, aj = a * r ** (i - 1), a * r ** (j - 1)
            n = j + R.randint(1, 3)
            v = a * r ** (n - 1)
            if abs(v) > 10 ** 6:
                return None
            return N("공비가 실수인 등비수열 {a<sub>n</sub>}에서 a<sub>%d</sub> = %s, a<sub>%d</sub> = %s일 때, a<sub>%d</sub>의 값은?%s" % (i, neg(ai), j, neg(aj), n, " (공비는 양수)" if (j - i) % 2 == 0 else ""), v, [a * r ** n, -v, aj * (n - j) * r, v // r],
                     "r<sup>%d</sup> = %s ÷ %s이므로 r = %s. <b>%s</b>" % (j - i, neg(aj), par(ai), neg(r), neg(v))) if (j - i) % 2 or r > 0 else None
        if how == "r":
            seq = [a * Fr(r) ** k for k in range(4)]
            return N("등비수열 %s, … 의 공비는?" % ", ".join(neg(x) for x in seq), r, [1 / Fr(r), -Fr(r), seq[1] - seq[0], Fr(r) * 2], "이웃한 두 항의 비 %s ÷ %s예요. <b>%s</b>" % (neg(seq[1]), par(seq[0]), neg(r)))
        if how == "sum":
            if not isinstance(r, int):
                r = R.choice([2, 3])
            n = R.randint(4, 9)
            S = a * (r ** n - 1) // (r - 1)
            if abs(S) > 10 ** 5:
                return None
            return N("첫째항이 %s, 공비가 %s인 등비수열의 첫째항부터 제%d항까지의 합은?" % (neg(a), neg(r), n), S, [a * (r ** (n - 1) - 1) // (r - 1), a * r ** (n - 1), a * (r ** (n + 1) - 1) // (r - 1), S + a], "S<sub>n</sub> = a(r<sup>n</sup> − 1) ÷ (r − 1). <b>%s</b>" % neg(S))
        if how == "mean":
            x = R.randint(1, 6)
            k = R.choice([2, 3, 4])
            y = x * k * k
            return M("세 양수 %d, a, %d가 이 순서대로 등비수열을 이룰 때, a의 값은?" % (x, y), neg(x * k), [neg((x + y) // 2) if (x + y) % 2 == 0 else neg(Fr(x + y, 2)), neg(x * y), neg(y - x), neg(x * k + 1)], "등비중항: a² = %d × %d = %d. <b>%d</b>" % (x, y, x * y, x * k))
        if how == "word":
            k = R.choice(["paper", "ball"])
            if k == "paper":
                n = R.randint(3, 10)
                return N("종이를 반으로 접을 때마다 두께가 2배가 돼요. 두께 0.1 mm인 종이를 %d번 접으면 몇 겹이 될까요?" % n, 2 ** n, [2 * n, 2 ** (n - 1), 2 ** (n + 1), n * n], "2<sup>%d</sup> = <b>%s겹</b>" % (n, neg(2 ** n)), f=lambda v: "%s겹" % neg(v))
            h = R.choice([81, 162, 243, 64, 128, 256])
            rr = Fr(2, 3) if h % 3 == 0 else Fr(1, 2)
            n = R.randint(2, 4)
            v = h * rr ** n
            if v.denominator != 1:
                return None
            return N("공을 %d m 높이에서 떨어뜨리면 떨어진 높이의 %s만큼 다시 튀어 올라요. %d번째로 튀어 오른 높이는?" % (h, neg(rr), n), v, [h * rr ** (n - 1), h * rr ** (n + 1) if (h * rr ** (n + 1)).denominator == 1 else v - 1, h - n * h * (1 - rr), v * 2], "%d × (%s)<sup>%d</sup> = <b>%s m</b>" % (h, neg(rr), n, neg(v)), f=lambda t: "%s m" % neg(t))
        # 등비수열의 합 공식의 응용: S_n 이 주어지면 a_n = S_n − S_{n−1}
        b = R.choice([2, 3])
        n = R.randint(3, 7)
        v = (b - 1) * b ** (n - 1)
        return N("수열 {a<sub>n</sub>}의 첫째항부터 제n항까지의 합이 S<sub>n</sub> = %d<sup>n</sup> − 1일 때, a<sub>%d</sub>의 값은?" % (b, n), v, [b ** n - 1, b ** (n - 1), b ** n, v + 1], "a<sub>%d</sub> = S<sub>%d</sub> − S<sub>%d</sub> = %d − %d. <b>%s</b>" % (n, n, n - 1, b ** n - 1, b ** (n - 1) - 1, neg(v)))
    return mk


# ------------------------------------------------------------------ 수열의 합
def sg(lo, hi, body):
    return "<span class='nowrap'>∑<sub>k=%d</sub><sup>%s</sup> %s</span>" % (lo, hi, body)


def sm_main(kinds=("const", "k", "k2", "lin", "prop", "tele", "k3")):
    def mk():
        how = R.choice(kinds)
        n = R.randint(5, 20)
        if how == "const":
            c = nz(-9, 9)
            return N("<b>%s</b>의 값은?" % sg(1, n, neg(c)), c * n, [c, c * n * (n + 1) // 2, c * (n - 1), c + n], "상수 c를 n번 더하면 cn. <b>%s</b>" % neg(c * n))
        if how == "k":
            return N("<b>%s</b>의 값은?" % sg(1, n, "k"), n * (n + 1) // 2, [n * n, n * (n + 1), n * (n - 1) // 2, n * n // 2], "n(n + 1) ÷ 2 = <b>%d</b>" % (n * (n + 1) // 2))
        if how == "k2":
            n = R.randint(4, 12)
            v = n * (n + 1) * (2 * n + 1) // 6
            return N("<b>%s</b>의 값은?" % sg(1, n, "k²"), v, [(n * (n + 1) // 2) ** 2, n * n * (n + 1) // 2, v - n * n, n ** 3 // 3], "n(n + 1)(2n + 1) ÷ 6 = <b>%s</b>" % neg(v))
        if how == "k3":
            n = R.randint(3, 10)
            v = (n * (n + 1) // 2) ** 2
            return N("<b>%s</b>의 값은?" % sg(1, n, "k³"), v, [n * (n + 1) * (2 * n + 1) // 6, n * (n + 1) // 2, n ** 4 // 4, v - n], "{n(n + 1) ÷ 2}² = <b>%s</b>" % neg(v))
        if how == "lin":
            a, b = nz(-4, 5), R.randint(-5, 5)
            v = a * n * (n + 1) // 2 + b * n
            return N("<b>%s</b>의 값은?" % sg(1, n, "(%s)" % px([a, b], "k")), v, [a * n * (n + 1) // 2 + b, a * n * n + b * n, a * n * (n + 1) // 2, v + b], "∑k = %d이므로 %s × %d %s %d × %d = <b>%s</b>" % (n * (n + 1) // 2, neg(a), n * (n + 1) // 2, "+" if b >= 0 else "−", abs(b), n, neg(v)))
        if how == "prop":
            p, q = R.randint(5, 40), R.randint(5, 40)
            a, b = nz(-3, 4), nz(-3, 4)
            v = a * p + b * q
            return N("∑<sub>k=1</sub><sup>%d</sup> a<sub>k</sub> = %d, ∑<sub>k=1</sub><sup>%d</sup> b<sub>k</sub> = %d일 때, <b>∑<sub>k=1</sub><sup>%d</sup> (%s)</b>의 값은?" % (n, p, n, q, n, px([a, b], "a<sub>k</sub>").replace("a<sub>k</sub>", "a<sub>k</sub>") if False else ("%sa<sub>k</sub> %s %sb<sub>k</sub>" % ("" if a == 1 else "−" if a == -1 else neg(a), "+" if b > 0 else "−", "" if abs(b) == 1 else abs(b)))),
                     v, [a * p + b * q * n, p + q, v + a, a * p - b * q], "%s × %d + %s × %d = <b>%s</b>" % (neg(a), p, par(b), q, neg(v)))
        k = R.choice(["frac", "frac2"])
        if k == "frac":
            v = Fr(n, n + 1)
            return N("<b>%s</b>의 값은?" % sg(1, n, fr(1, "k(k + 1)")), v, [Fr(1, n + 1), Fr(n + 1, n), Fr(n, n + 2), Fr(n - 1, n)], "1/k − 1/(k + 1)로 나누면 1 − 1/%d. <b>%s</b>" % (n + 1, neg(v)))
        v = Fr(n, 2 * n + 1)
        return N("<b>%s</b>의 값은?" % sg(1, n, fr(1, "(2k − 1)(2k + 1)")), v, [Fr(2 * n, 2 * n + 1), Fr(n, 2 * n - 1), Fr(1, 2 * n + 1), Fr(n + 1, 2 * n + 1)], "½{1/(2k − 1) − 1/(2k + 1)}로 나누면 ½(1 − 1/%d). <b>%s</b>" % (2 * n + 1, neg(v)))
    return mk


# ------------------------------------------------------------------ 귀납적 정의와 수학적 귀납법
def rc_main(kinds=("ar", "ge", "mix", "addn", "concept", "fib")):
    def mk():
        how = R.choice(kinds)
        a1 = R.randint(-5, 6)
        if how == "ar":
            d = nz(-5, 6)
            n = R.randint(5, 30)
            v = a1 + (n - 1) * d
            return N("a<sub>1</sub> = %s, a<sub>n+1</sub> = a<sub>n</sub> %s %d (n = 1, 2, 3, …)로 정의된 수열에서 a<sub>%d</sub>의 값은?" % (neg(a1), "+" if d > 0 else "−", abs(d), n), v, [a1 + n * d, a1 * d ** 2 if a1 * d ** 2 != v else v + 1, v - d, (n - 1) * d], "공차가 %s인 등차수열이에요. <b>%s</b>" % (neg(d), neg(v)))
        if how == "ge":
            r = R.choice([2, 3, -2])
            a1 = R.choice([1, 2, 3, -1])
            n = R.randint(4, 8)
            v = a1 * r ** (n - 1)
            return N("a<sub>1</sub> = %s, a<sub>n+1</sub> = %sa<sub>n</sub> (n = 1, 2, 3, …)로 정의된 수열에서 a<sub>%d</sub>의 값은?" % (neg(a1), neg(r), n), v, [a1 * r ** n, a1 + (n - 1) * r, -v, v // r if v % r == 0 else v + 1], "공비가 %s인 등비수열이에요. <b>%s</b>" % (neg(r), neg(v)))
        if how == "mix":
            p, q = R.choice([2, 3]), R.randint(-3, 3)
            n = R.randint(3, 5)
            seq = [a1]
            for _ in range(n - 1):
                seq.append(p * seq[-1] + q)
            v = seq[-1]
            return N("a<sub>1</sub> = %s, a<sub>n+1</sub> = %s (n = 1, 2, 3, …)로 정의된 수열에서 a<sub>%d</sub>의 값은?" % (neg(a1), px([p, q], "a<sub>n</sub>"), n), v, [seq[-2], p * v + q, v + q, a1 * p ** (n - 1)], "차례로 대입하면 %s. <b>%s</b>" % (", ".join(neg(x) for x in seq), neg(v)))
        if how == "addn":
            n = R.randint(5, 15)
            k = R.choice(["n", "2n"])
            if k == "n":
                v = a1 + n * (n - 1) // 2
                return N("a<sub>1</sub> = %s, a<sub>n+1</sub> = a<sub>n</sub> + n (n = 1, 2, 3, …)로 정의된 수열에서 a<sub>%d</sub>의 값은?" % (neg(a1), n), v, [a1 + n * (n + 1) // 2, a1 + n, v - 1, n * (n - 1) // 2], "a<sub>%d</sub> = a<sub>1</sub> + (1 + 2 + … + %d). <b>%s</b>" % (n, n - 1, neg(v)))
            v = a1 + 2 ** (n - 1) - 1
            if n > 12:
                return None
            return N("a<sub>1</sub> = %s, a<sub>n+1</sub> = a<sub>n</sub> + 2<sup>n−1</sup> (n = 1, 2, 3, …)로 정의된 수열에서 a<sub>%d</sub>의 값은?" % (neg(a1), n), v, [a1 + 2 ** n - 1, a1 + 2 ** (n - 1), v + 1, 2 ** (n - 1)], "a<sub>%d</sub> = a<sub>1</sub> + (1 + 2 + … + 2<sup>%d</sup>). <b>%s</b>" % (n, n - 2, neg(v)))
        if how == "fib":
            x, y = R.randint(1, 4), R.randint(1, 5)
            n = R.randint(5, 9)
            seq = [x, y]
            while len(seq) < n:
                seq.append(seq[-1] + seq[-2])
            v = seq[-1]
            return N("a<sub>1</sub> = %d, a<sub>2</sub> = %d, a<sub>n+2</sub> = a<sub>n+1</sub> + a<sub>n</sub> (n = 1, 2, 3, …)로 정의된 수열에서 a<sub>%d</sub>의 값은?" % (x, y, n), v, [seq[-2], v + seq[-3], seq[-1] + seq[-2], v - 1], "차례로 구하면 %s. <b>%d</b>" % (", ".join(map(str, seq)), v))
        C = [("수학적 귀납법으로 모든 자연수 n에 대하여 p(n)이 성립함을 보일 때, 먼저 보여야 하는 것은?", "n = 1일 때 p(1)이 성립", ["n = 0일 때 성립", "n = k일 때 성립", "n이 짝수일 때 성립"]),
             ("수학적 귀납법의 두 번째 단계로 옳은 것은?", "n = k일 때 성립하면 n = k + 1일 때도 성립", ["n = k + 1일 때 성립하면 n = k일 때도 성립", "모든 k에 대하여 성립", "n = 2일 때 성립"]),
             ("1 + 3 + 5 + … + (2n − 1) = n²의 증명에서 n = k + 1일 때 좌변에 더해지는 항은?", "2k + 1", ["2k − 1", "2k + 3", "k + 1"]),
             ("1 + 2 + … + n = n(n + 1)/2의 증명에서 n = k + 1일 때 좌변에 더해지는 항은?", "k + 1", ["k", "2k + 1", "k + 2"]),
             ("a<sub>1</sub>과 a<sub>n</sub>과 a<sub>n+1</sub> 사이의 관계식으로 수열을 정의하는 방법은?", "귀납적 정의", ["일반항", "수학적 귀납법", "점화법"]),
             ("a<sub>n+1</sub> − a<sub>n</sub> = d (일정)로 정의된 수열은?", "등차수열", ["등비수열", "계차수열", "조화수열"]),
             ("a<sub>n+1</sub> ÷ a<sub>n</sub> = r (일정, a<sub>n</sub> ≠ 0)로 정의된 수열은?", "등비수열", ["등차수열", "피보나치수열", "상수수열"]),
             ("2a<sub>n+1</sub> = a<sub>n</sub> + a<sub>n+2</sub>로 정의된 수열은?", "등차수열", ["등비수열", "피보나치수열", "상수수열"]),
             ("(a<sub>n+1</sub>)² = a<sub>n</sub>a<sub>n+2</sub> (a<sub>n</sub> ≠ 0)로 정의된 수열은?", "등비수열", ["등차수열", "계차수열", "피보나치수열"])]
        q, ok, w = R.choice(C)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ build
def build(which):
    U = {}
    U["root"] = ("radicals-and-roots", 1, "[12대수01-01]", "거듭제곱과 거듭제곱근의 뜻을 알고, 그 성질을 이용하여 계산할 수 있다.",
                 "거듭제곱근의 뜻과 성질", "거듭제곱근",
                 "고등학교 대수 거듭제곱근 문제: n제곱근의 뜻, 실수인 n제곱근의 개수, ∛, ∜의 값, ⁿ√a × ⁿ√b, ᵐ√(ⁿ√a), (ⁿ√a)ᵐ의 계산과 거듭제곱근의 대소 비교까지 100문제와 정답·해설.",
                 "xⁿ = a를 만족하는 x가 a의 n제곱근", "n이 홀수이면 실수인 n제곱근은 하나, 짝수이면 a > 0일 때 둘이에요.",
                 ["n이 2 이상의 정수일 때, xⁿ = a를 만족하는 x를 a의 <b>n제곱근</b>이라고 해요.",
                  "실수인 n제곱근: n이 홀수이면 하나(ⁿ√a), n이 짝수이면 a &gt; 0일 때 ±ⁿ√a, a = 0일 때 0, a &lt; 0일 때 없어요.",
                  "a &gt; 0, b &gt; 0일 때 ⁿ√a × ⁿ√b = ⁿ√(ab), (ⁿ√a)<sup>m</sup> = ⁿ√(a<sup>m</sup>), <sup>m</sup>√(ⁿ√a) = <sup>mn</sup>√a",
                  "대소 비교는 근호의 지수를 같게 맞추어 근호 안을 비교해요."],
                 [("∛(−27)", ["(−3)³ = −27"], "−3"), ("∜2 × ∜8", ["∜16"], "2")],
                 [("∜16 = ±2", "실수 ⁿ√a는 양수 하나를 나타내요. ±는 4제곱근 전체예요."), ("짝수 제곱근에 음수를 넣는다", "a &lt; 0이면 실수인 짝수제곱근이 없어요."), ("ⁿ√a × ᵐ√b를 바로 곱한다", "근호의 지수가 같을 때만 근호 안을 곱해요.")],
                 [("√는 몇 제곱근인가요?", "제곱근이에요. 지수 2를 생략한 것이에요."), ("−8의 세제곱근은 몇 개인가요?", "복소수 범위에서는 3개, 실수는 −2 하나예요.")],
                 [("거듭제곱근의 값", [(r_main(("eval",)), 20)]), ("실수인 n제곱근의 개수", [(r_main(("count",)), 20)]), ("거듭제곱근의 곱셈", [(r_main(("mul",)), 20)]),
                  ("거듭제곱근의 성질", [(r_main(("nest", "pow")), 20)]), ("대소 비교", [(r_main(("cmp",)), 5), (r_main(("eval", "mul", "nest", "pow")), 15)])], 83201)
    U["expo"] = ("exponents", 2, "[12대수01-02] [12대수01-03]", "지수가 유리수, 실수까지 확장될 수 있음을 이해하고, 이를 설명할 수 있다. 지수법칙을 이해하고, 이를 이용하여 식을 간단히 나타낼 수 있다.",
                 "지수의 확장과 지수법칙", "지수",
                 "고등학교 대수 지수 문제: 0과 음의 정수 지수, 유리수 지수, 거듭제곱근을 유리수 지수로 나타내기, 지수법칙으로 식 간단히 하기, a^(1/2) + a^(−1/2)를 이용한 식의 값까지 100문제와 정답·해설.",
                 "a^(m/n) = ⁿ√(aᵐ)", "a^x × a^y = a^(x+y), (a^x)^y = a^(xy)",
                 ["a ≠ 0일 때 a⁰ = 1, a<sup>−n</sup> = 1/aⁿ이에요.",
                  "a &gt; 0일 때 a<sup>m/n</sup> = ⁿ√(a<sup>m</sup>)으로 지수를 유리수까지 확장해요.",
                  "지수법칙: a<sup>x</sup>a<sup>y</sup> = a<sup>x+y</sup>, a<sup>x</sup> ÷ a<sup>y</sup> = a<sup>x−y</sup>, (a<sup>x</sup>)<sup>y</sup> = a<sup>xy</sup>, (ab)<sup>x</sup> = a<sup>x</sup>b<sup>x</sup>",
                  "밑을 같은 수로 맞추고 지수만 계산하면 편해요."],
                 [("8<sup>2/3</sup>", ["(2³)<sup>2/3</sup> = 2²"], "4"), ("a<sup>1/2</sup> × a<sup>1/3</sup>", ["1/2 + 1/3"], "a<sup>5/6</sup>")],
                 [("a<sup>x</sup> × a<sup>y</sup> = a<sup>xy</sup>", "곱하면 지수를 더해요."), ("a<sup>−2</sup> = −a²", "1/a²이에요."), ("8<sup>2/3</sup>을 8 × 2 ÷ 3으로 계산한다", "³√(8²) = 4예요.")],
                 [("밑이 음수이면 유리수 지수를 쓸 수 있나요?", "고등학교에서는 밑이 양수일 때만 유리수·실수 지수를 생각해요."), ("지수가 무리수이면?", "유리수 지수의 극한으로 정의하고 지수법칙이 그대로 성립해요.")],
                 [("유리수 지수", [(e_main(("rat",)), 20)]), ("음의 지수", [(e_main(("neg",)), 20)]), ("지수법칙", [(e_main(("law",)), 20)]),
                  ("거듭제곱근과 지수", [(e_main(("eq",)), 20)]), ("식의 값", [(e_main(("simp",)), 12), (e_main(("sym",)), 6), (e_main(("rat",)), 2)])], 83202)
    U["log"] = ("logarithms", 3, "[12대수01-04]", "로그의 뜻을 알고, 그 성질을 이용하여 계산할 수 있다.",
                "로그의 뜻과 성질", "로그",
                "고등학교 대수 로그 문제: 지수와 로그의 관계, 로그의 값, 밑과 진수의 조건, log M + log N, log M − log N, 밑의 변환 공식, a^(log_a N) = N까지 100문제와 정답·해설.",
                "aˣ = N ⇔ x = logₐ N", "밑은 1이 아닌 양수, 진수는 양수예요.",
                ["a &gt; 0, a ≠ 1, N &gt; 0일 때 a<sup>x</sup> = N이면 x = log<sub>a</sub> N이에요. a를 밑, N을 진수라고 해요.",
                 "log<sub>a</sub> 1 = 0, log<sub>a</sub> a = 1, log<sub>a</sub> MN = log<sub>a</sub> M + log<sub>a</sub> N, log<sub>a</sub> (M/N) = log<sub>a</sub> M − log<sub>a</sub> N",
                 "log<sub>a</sub> M<sup>k</sup> = k log<sub>a</sub> M, 밑의 변환: log<sub>a</sub> b = log<sub>c</sub> b ÷ log<sub>c</sub> a",
                 "a<sup>log<sub>a</sub> N</sup> = N, log<sub>a</sub> b × log<sub>b</sub> a = 1"],
                [("log<sub>2</sub> 32", ["2⁵ = 32"], "5"), ("log<sub>6</sub> 4 + log<sub>6</sub> 9", ["log<sub>6</sub> 36"], "2")],
                [("log (M + N) = log M + log N", "곱의 로그가 로그의 합이에요."), ("log<sub>a</sub> M ÷ log<sub>a</sub> N = log<sub>a</sub> (M/N)", "나눗셈은 밑의 변환이에요."), ("밑의 조건에서 a ≠ 1을 빠뜨린다", "밑은 1이 아닌 양수예요.")],
                [("log 뒤에 밑이 없으면?", "밑이 10인 상용로그예요."), ("로그는 왜 배우나요?", "아주 큰 수나 작은 수를 다루고, 지수방정식을 풀 때 써요.")],
                [("지수와 로그", [(lg_main(("def",)), 20)]), ("로그의 값", [(lg_main(("eval",)), 20)]), ("로그의 덧셈과 뺄셈", [(lg_main(("add", "sub")), 20)]),
                 ("밑의 변환", [(lg_main(("chg", "pow")), 20)]), ("밑과 진수의 조건", [(lg_main(("cond",)), 14), (lg_main(("eval", "add")), 6)])], 83203)
    U["clog"] = ("common-logarithms", 4, "[12대수01-05]", "상용로그를 이해하고, 이를 실생활과 연결하여 문제를 해결할 수 있다.",
                 "상용로그와 활용", "상용로그",
                 "고등학교 대수 상용로그 문제: log 2 = 0.3010, log 3 = 0.4771을 이용한 상용로그의 값, log x에서 x 구하기, 2ⁿ의 자릿수와 최고 자리의 숫자, 소리의 크기·pH·지진 규모까지 100문제와 정답·해설.",
                 "log 10ⁿ = n", "자릿수는 (log의 정수 부분) + 1이에요.",
                 ["밑이 10인 로그를 <b>상용로그</b>라 하고 log N으로 써요.",
                  "log 2 ≈ 0.3010, log 3 ≈ 0.4771로 여러 수의 상용로그를 구할 수 있어요. log 5 = 1 − log 2",
                  "log N의 정수 부분이 n이면 N은 n + 1자리의 정수예요(N ≥ 1).",
                  "소리의 크기(dB), pH, 지진의 규모처럼 범위가 넓은 양은 상용로그로 나타내요."],
                 [("log 6", ["log 2 + log 3"], "0.7781"), ("2<sup>30</sup>의 자릿수", ["30 × 0.3010 = 9.03"], "10자리")],
                 [("log 20 = 2 log 2", "log 20 = log 2 + 1이에요."), ("자릿수를 정수 부분 그대로 답한다", "정수 부분에 1을 더해요."), ("log 0.2를 −log 2로 쓴다", "log 2 − 1이에요.")],
                 [("log 2의 값은 정확히 0.3010인가요?", "근삿값이에요. 소수 다섯째 자리에서 반올림한 값이에요."), ("소수의 자릿수는?", "log의 정수 부분이 −n이면 소수점 아래 n째 자리에서 처음 0이 아닌 숫자가 나와요.")],
                 [("상용로그의 값", [(cl_main(("calc",)), 20)]), ("log x에서 x 구하기", [(cl_main(("inv",)), 20)]), ("자릿수", [(cl_main(("digits",)), 20)]),
                  ("최고 자리의 숫자", [(cl_main(("first",)), 12), (cl_main(("digits",)), 8)]), ("실생활 활용", [(cl_main(("life",)), 20)])], 83204)
    U["elf"] = ("exponential-and-logarithmic-functions", 5, "[12대수01-06] [12대수01-07]", "지수함수와 로그함수의 뜻을 알고, 이를 설명할 수 있다. 지수함수와 로그함수의 그래프를 그릴 수 있고, 그 성질을 설명할 수 있다.",
                "지수함수와 로그함수의 그래프", "지수함수와 로그함수",
                "고등학교 대수 지수함수와 로그함수 문제: y = aˣ와 y = logₐ x의 성질, 평행이동한 그래프의 점근선과 정의역, 함숫값, 대소 비교, 제한된 범위의 최대·최소, 역함수, 그래프 읽기까지 100문제와 정답·해설.",
                "y = aˣ와 y = logₐ x는 역함수", "밑이 1보다 크면 증가, 1보다 작으면 감소해요.",
                ["y = a<sup>x</sup> (a &gt; 0, a ≠ 1)는 점 (0, 1)을 지나고 x축이 점근선이며, 치역은 양의 실수예요.",
                 "y = log<sub>a</sub> x는 점 (1, 0)을 지나고 y축이 점근선이며, 정의역은 양의 실수예요.",
                 "a &gt; 1이면 증가함수, 0 &lt; a &lt; 1이면 감소함수예요.",
                 "y = a<sup>x</sup>와 y = log<sub>a</sub> x는 서로 역함수이고 직선 y = x에 대하여 대칭이에요."],
                [("y = 2<sup>x − 1</sup> + 3", ["y = 2<sup>x</sup>를 (1, 3)만큼 이동"], "점근선 y = 3"), ("y = log<sub>3</sub>(x + 2)", ["진수 x + 2 &gt; 0"], "정의역 x &gt; −2")],
                [("지수함수의 점근선을 x = q로 쓴다", "y = a<sup>x</sup>의 점근선은 x축(y = 0)이에요."), ("밑이 1보다 작아도 증가한다고 생각한다", "0 &lt; a &lt; 1이면 감소해요."), ("로그함수의 정의역에 경계값을 넣는다", "진수는 0보다 커야 해요.")],
                [("밑이 1이면?", "y = 1ˣ = 1이 되어 지수함수로 보지 않아요."), ("최대·최소는 어떻게 구하나요?", "증가함수는 오른쪽 끝, 감소함수는 왼쪽 끝에서 최댓값이에요.")],
                [("그래프의 성질", [(ef_main(("prop",)), 20)]), ("점근선과 정의역", [(ef_main(("asym", "dom")), 20)]), ("함숫값과 역함수", [(ef_main(("val",)), 15), (ef_main(("inv",)), 5)]),
                 ("대소 비교와 최대·최소", [(ef_main(("cmp", "mm")), 20)]), ("그래프 읽기", [(ef_main(("graph",)), 20)])], 83205)
    U["eleq"] = ("exponential-and-logarithmic-equations", 6, "[12대수01-08]", "지수함수, 로그함수를 활용하여 문제를 해결할 수 있다.",
                 "지수방정식·로그방정식과 부등식", "지수·로그방정식",
                 "고등학교 대수 지수방정식과 로그방정식 문제: 밑을 같게 하여 풀기, 치환으로 풀기, 진수 조건을 확인하는 로그방정식, 지수부등식과 로그부등식, 세균 증식·반감기 등 활용까지 100문제와 정답·해설.",
                 "밑을 같게 하고 지수끼리 비교", "밑이 1보다 작으면 부등호 방향이 바뀌어요.",
                 ["a<sup>f(x)</sup> = a<sup>g(x)</sup>이면 f(x) = g(x)예요. 밑을 같은 수로 맞추어요.",
                  "a<sup>x</sup>가 여러 번 나오면 a<sup>x</sup> = t (t &gt; 0)로 치환해요.",
                  "로그방정식은 진수 조건(진수 &gt; 0)을 반드시 확인해요.",
                  "부등식에서 밑이 1보다 크면 부등호 그대로, 0과 1 사이이면 방향이 바뀌어요."],
                 [("4<sup>x</sup> = 32", ["2<sup>2x</sup> = 2⁵"], "x = 5/2"), ("log<sub>2</sub>(x − 1) &lt; 3", ["x &gt; 1", "x − 1 &lt; 8"], "1 &lt; x &lt; 9")],
                 [("로그방정식에서 진수 조건을 확인하지 않는다", "구한 해 중 진수가 양수가 아닌 것은 버려요."), ("(1/2)<sup>x</sup> &gt; 4에서 x &gt; −2로 쓴다", "밑이 1보다 작으므로 x &lt; −2예요."), ("치환한 t의 범위를 잊는다", "t = a<sup>x</sup> &gt; 0이에요.")],
                 [("양변에 로그를 취할 때는?", "밑을 같게 만들기 어려울 때 양변에 같은 밑의 로그를 취해요."), ("반감기란?", "양이 처음의 절반이 되는 데 걸리는 시간이에요.")],
                 [("지수방정식", [(eq_main(("expeq",)), 14), (eq_main(("sub",)), 6)]), ("로그방정식", [(eq_main(("logeq", "logsum")), 20)]), ("지수부등식", [(eq_main(("expin",)), 20)]),
                  ("로그부등식", [(eq_main(("login",)), 20)]), ("활용", [(eq_main(("word",)), 16), (eq_main(("expeq", "logeq")), 4)])], 83206)
    U["rad"] = ("radians-and-general-angles", 7, "[12대수02-01]", "일반각과 호도법의 뜻을 알고, 그 관계를 설명할 수 있다.",
                "일반각과 호도법", "일반각과 호도법",
                "고등학교 대수 일반각과 호도법 문제: 동경과 일반각 360°n + α, 사분면의 각, 육십분법과 호도법의 변환, 부채꼴의 호의 길이 l = rθ와 넓이 S = ½r²θ까지 100문제와 정답·해설.",
                "π(라디안) = 180°", "부채꼴: l = rθ, S = ½r²θ",
                ["시초선 OX와 동경 OP가 이루는 각을 360° × n + α (n은 정수)로 나타낸 것을 <b>일반각</b>이라고 해요.",
                 "반지름과 호의 길이가 같을 때의 중심각을 1라디안이라 하고, π = 180°예요.",
                 "x°를 호도법으로 바꾸려면 π/180을 곱하고, 반대로 바꾸려면 180/π를 곱해요.",
                 "반지름 r, 중심각 θ(라디안)인 부채꼴의 호의 길이는 rθ, 넓이는 ½r²θ예요."],
                [("150°", ["150 × π/180"], "5π/6"), ("r = 6, θ = π/3", ["l = 6 × π/3", "S = ½ × 36 × π/3"], "l = 2π, S = 6π")],
                [("π = 360°로 계산한다", "π = 180°예요."), ("부채꼴 넓이를 r²θ로 쓴다", "½을 빠뜨리지 않아요."), ("−30°를 제4사분면이 아니라고 한다", "시계 방향으로 30° 돈 각이라 제4사분면이에요.")],
                [("라디안 단위는 왜 쓰나요?", "호의 길이·넓이 공식이 간단해지고 삼각함수 그래프를 그리기 편해요."), ("390°와 30°의 동경은?", "같아요. 360°만큼 차이 나요.")],
                [("육십분법 → 호도법", [(rd_main(("d2r",)), 20)]), ("호도법 → 육십분법", [(rd_main(("r2d",)), 20)]), ("사분면의 각", [(rd_main(("quad",)), 20)]),
                 ("일반각", [(rd_main(("cot",)), 20)]), ("부채꼴", [(rd_main(("arc", "area")), 20)])], 83207)
    U["trig"] = ("trigonometric-functions", 8, "[12대수02-02]", "삼각함수의 개념을 이해하여 사인함수, 코사인함수, 탄젠트함수의 그래프를 그리고, 그 성질을 설명할 수 있다.",
                 "삼각함수의 뜻과 값", "삼각함수",
                 "고등학교 대수 삼각함수 문제: 일반각에 대한 sin, cos, tan의 값, 사분면에 따른 부호, sin²θ + cos²θ = 1로 값 구하기, 삼각함수 사이의 관계와 각의 변환, sin θ + cos θ가 주어진 식의 값까지 100문제와 정답·해설.",
                 "sin²θ + cos²θ = 1", "tan θ = sin θ ÷ cos θ, 부호는 사분면으로 정해요.",
                 ["반지름이 r인 원 위의 점 P(x, y)에 대하여 sin θ = y/r, cos θ = x/r, tan θ = y/x예요.",
                  "제1사분면은 모두 양, 제2사분면은 sin, 제3사분면은 tan, 제4사분면은 cos만 양수예요.",
                  "sin²θ + cos²θ = 1, tan θ = sin θ ÷ cos θ를 이용해 나머지 값을 구해요.",
                  "sin(−θ) = −sin θ, cos(−θ) = cos θ, sin(π − θ) = sin θ처럼 각을 바꿀 수 있어요."],
                 [("sin 2π/3", ["120°, 제2사분면, 기준각 60°"], "√3/2"), ("sin θ = 3/5 (π/2 &lt; θ &lt; π)", ["cos θ = −4/5"], "tan θ = −3/4")],
                 [("제2사분면에서 cos θ를 양수로 둔다", "제2사분면에서는 sin만 양수예요."), ("sin²θ를 sin θ²으로 생각한다", "(sin θ)²이에요."), ("tan θ = cos θ ÷ sin θ", "sin θ ÷ cos θ예요.")],
                 [("기준각이란?", "동경과 x축이 이루는 예각이에요. 값의 크기를 정해요."), ("tan 90°는?", "cos 90° = 0이라 정의되지 않아요.")],
                 [("삼각함수의 값", [(t_main(("val",)), 20)]), ("삼각함수의 부호", [(t_main(("sign",)), 8), (t_main(("val",)), 12)]), ("값 구하기", [(t_main(("find",)), 20)]),
                  ("삼각함수 사이의 관계", [(t_main(("ident",)), 10), (t_main(("find",)), 10)]), ("식의 값", [(t_main(("sumprod",)), 20)])], 83208)
    U["tgraph"] = ("graphs-of-trigonometric-functions", 9, "[12대수02-02]", "삼각함수의 개념을 이해하여 사인함수, 코사인함수, 탄젠트함수의 그래프를 그리고, 그 성질을 설명할 수 있다.",
                   "삼각함수의 그래프와 방정식·부등식", "삼각함수의 그래프",
                   "고등학교 대수 삼각함수의 그래프 문제: y = a sin bx + c, y = a cos bx + c의 주기·최댓값·최솟값, y = tan bx의 주기와 점근선, 함숫값, 그래프 읽기, 삼각방정식과 삼각부등식까지 100문제와 정답·해설.",
                   "주기 2π ÷ |b| (tan은 π ÷ |b|)", "최댓값 |a| + c, 최솟값 −|a| + c",
                   ["y = sin x, y = cos x는 주기가 2π이고 −1 ≤ y ≤ 1이에요. y = tan x는 주기가 π이고 x = π/2 + nπ가 점근선이에요.",
                    "y = a sin bx + c는 최댓값 |a| + c, 최솟값 −|a| + c, 주기 2π/|b|예요.",
                    "삼각방정식은 단위원이나 그래프에서 해당하는 각을 모두 찾아요.",
                    "삼각부등식은 그래프가 직선보다 위(또는 아래)에 있는 범위를 구해요."],
                   [("y = 3 sin 2x + 1", ["주기 2π/2", "최대 3 + 1"], "주기 π, 최댓값 4, 최솟값 −2"), ("sin x = 1/2 (0 ≤ x &lt; 2π)", ["30°, 150°"], "x = π/6 또는 5π/6")],
                   [("주기를 2π × b로 쓴다", "2π ÷ |b|예요."), ("a가 음수일 때 최댓값을 a + c로 쓴다", "|a| + c예요."), ("삼각방정식에서 한 각만 답한다", "0 ≤ x &lt; 2π에서는 보통 두 개예요.")],
                   [("y = sin x와 y = cos x의 관계는?", "y = cos x는 y = sin x를 x축 방향으로 −π/2만큼 평행이동한 것이에요."), ("tan 그래프는 왜 끊기나요?", "cos x = 0인 곳에서 정의되지 않기 때문이에요.")],
                   [("주기", [(tg_main(("period",)), 14), (tg_main(("tan",)), 6)]), ("최댓값과 최솟값", [(tg_main(("mm",)), 20)]), ("그래프 읽기", [(tg_main(("read",)), 14), (tg_main(("val",)), 6)]),
                    ("삼각방정식", [(tg_main(("eq",)), 20)]), ("삼각부등식", [(tg_main(("ineq",)), 12), (tg_main(("eq", "tan")), 8)])], 83209)
    U["law"] = ("law-of-sines-and-cosines", 10, "[12대수02-03]", "사인법칙과 코사인법칙을 이해하고, 실생활 문제를 해결할 수 있다.",
                "사인법칙과 코사인법칙", "사인법칙과 코사인법칙",
                "고등학교 대수 사인법칙과 코사인법칙 문제: a/sin A = 2R, 외접원의 반지름, 두 변과 끼인각으로 나머지 변 구하기, 세 변으로 각 구하기, 삼각형의 넓이 ½ab sin C, 거리 측정 활용까지 100문제와 정답·해설.",
                "a ÷ sin A = 2R", "코사인법칙: c² = a² + b² − 2ab cos C",
                ["<b>사인법칙</b>: 삼각형 ABC의 외접원의 반지름을 R이라 하면 a/sin A = b/sin B = c/sin C = 2R이에요.",
                 "<b>코사인법칙</b>: c² = a² + b² − 2ab cos C, cos C = (a² + b² − c²) ÷ 2ab",
                 "한 변과 두 각을 알면 사인법칙, 두 변과 끼인각 또는 세 변을 알면 코사인법칙을 써요.",
                 "삼각형의 넓이는 ½ab sin C예요."],
                [("a = 3, b = 5, C = 120°", ["c² = 9 + 25 − 30 cos 120° = 49"], "c = 7"), ("a = 4, b = 6, C = 30°의 넓이", ["½ × 4 × 6 × ½"], "6")],
                [("코사인법칙에서 −2ab cos C의 부호를 바꾼다", "C가 둔각이면 cos C &lt; 0이라 더해져요."), ("사인법칙에서 a × sin A = b × sin B로 쓴다", "a ÷ sin A = b ÷ sin B예요."), ("넓이에 끼인각이 아닌 각을 쓴다", "두 변 사이의 끼인각이어야 해요.")],
                [("직각삼각형에서 코사인법칙은?", "C = 90°이면 cos C = 0이 되어 피타고라스 정리가 돼요."), ("어떤 상황에 쓰나요?", "직접 잴 수 없는 강 건너편이나 산 너머까지의 거리를 구할 때 써요.")],
                [("사인법칙", [(lw_main(("sin",)), 20)]), ("외접원의 반지름", [(lw_main(("R",)), 20)]), ("코사인법칙: 변", [(lw_main(("cosside",)), 20)]),
                 ("코사인법칙: 각과 넓이", [(lw_main(("cosang",)), 10), (lw_main(("area",)), 10)]), ("활용", [(lw_main(("word",)), 14), (lw_main(("area",)), 6)])], 83210)
    U["arith"] = ("arithmetic-sequences", 11, "[12대수03-01] [12대수03-02]", "수열의 뜻을 설명할 수 있다. 등차수열의 뜻을 알고, 일반항, 첫째항부터 제n항까지의 합을 구할 수 있다.",
                  "등차수열의 일반항과 합", "등차수열",
                  "고등학교 대수 등차수열 문제: 공차와 일반항 aₙ = a + (n − 1)d, 두 항이 주어진 등차수열, 항의 개수, 등차중항, 합 Sₙ = n(2a + (n − 1)d)/2, 처음으로 양수가 되는 항까지 100문제와 정답·해설.",
                  "aₙ = a + (n − 1)d", "Sₙ = n(a + l) ÷ 2 (l은 끝항)",
                  ["첫째항부터 차례로 일정한 수 d를 더해 만든 수열을 <b>등차수열</b>, d를 <b>공차</b>라고 해요.",
                   "일반항은 a<sub>n</sub> = a + (n − 1)d예요.",
                   "세 수 a, b, c가 이 순서대로 등차수열을 이루면 2b = a + c(등차중항)예요.",
                   "합은 S<sub>n</sub> = n(a + l) ÷ 2 = n{2a + (n − 1)d} ÷ 2예요."],
                  [("a = 3, d = 4, a<sub>10</sub>", ["3 + 9 × 4"], "39"), ("1 + 2 + … + 100", ["100 × 101 ÷ 2"], "5050")],
                  [("a<sub>n</sub> = a + nd로 쓴다", "제n항까지 공차를 n − 1번 더해요."), ("합에서 2로 나누지 않는다", "S<sub>n</sub> = n(a + l) ÷ 2예요."), ("항의 개수를 (끝 − 처음) ÷ d로 센다", "1을 더해야 해요.")],
                  [("수열이란?", "차례로 나열한 수의 열이에요. 각 수를 항이라고 해요."), ("등차수열의 그래프는?", "(n, a<sub>n</sub>)이 기울기가 d인 직선 위에 있어요.")],
                  [("일반항", [(ar_main(("term",)), 20)]), ("공차와 항의 개수", [(ar_main(("ad",)), 20)]), ("두 항이 주어진 등차수열", [(ar_main(("find",)), 14), (ar_main(("mean",)), 6)]),
                   ("등차수열의 합", [(ar_main(("sum",)), 20)]), ("합의 활용", [(ar_main(("sumf",)), 14), (ar_main(("first",)), 6)])], 83211)
    U["geo"] = ("geometric-sequences", 12, "[12대수03-03]", "등비수열의 뜻을 알고, 일반항, 첫째항부터 제n항까지의 합을 구할 수 있다.",
                "등비수열의 일반항과 합", "등비수열",
                "고등학교 대수 등비수열 문제: 공비와 일반항 aₙ = arⁿ⁻¹, 두 항이 주어진 등비수열, 등비중항, 합 Sₙ = a(rⁿ − 1)/(r − 1), Sₙ으로 aₙ 구하기, 튀어 오르는 공 등 활용까지 100문제와 정답·해설.",
                "aₙ = arⁿ⁻¹", "Sₙ = a(rⁿ − 1) ÷ (r − 1) (r ≠ 1)",
                ["첫째항부터 차례로 일정한 수 r을 곱해 만든 수열을 <b>등비수열</b>, r을 <b>공비</b>라고 해요.",
                 "일반항은 a<sub>n</sub> = ar<sup>n−1</sup>이에요.",
                 "세 수 a, b, c가 이 순서대로 등비수열을 이루면 b² = ac(등비중항)예요.",
                 "r ≠ 1일 때 S<sub>n</sub> = a(r<sup>n</sup> − 1) ÷ (r − 1), r = 1이면 S<sub>n</sub> = na예요."],
                [("a = 3, r = 2, a<sub>6</sub>", ["3 × 2⁵"], "96"), ("1 + 2 + 4 + … + 2⁹", ["(2<sup>10</sup> − 1) ÷ 1"], "1023")],
                [("a<sub>n</sub> = ar<sup>n</sup>으로 쓴다", "지수는 n − 1이에요."), ("공비를 이웃한 항의 차로 구한다", "비(나눗셈)로 구해요."), ("합에서 r<sup>n−1</sup>을 쓴다", "r<sup>n</sup> − 1이에요.")],
                [("공비가 음수이면?", "항의 부호가 번갈아 바뀌어요."), ("S<sub>n</sub>으로 a<sub>n</sub>을 구하려면?", "n ≥ 2일 때 a<sub>n</sub> = S<sub>n</sub> − S<sub>n−1</sub>이에요.")],
                [("일반항", [(ge_main(("term",)), 20)]), ("공비", [(ge_main(("r",)), 20)]), ("두 항과 등비중항", [(ge_main(("find",)), 12), (ge_main(("mean",)), 8)]),
                 ("등비수열의 합", [(ge_main(("sum",)), 14), (ge_main(("inf",)), 6)]), ("활용", [(ge_main(("word",)), 14), (ge_main(("sum",)), 6)])], 83212)
    U["sigma"] = ("sigma-notation", 13, "[12대수03-04] [12대수03-05]", "∑의 뜻과 성질을 이해하고, 이를 활용하여 문제를 해결할 수 있다. 여러 가지 수열의 첫째항부터 제n항까지의 합을 구하는 방법을 설명할 수 있다.",
                  "∑의 뜻과 여러 가지 수열의 합", "수열의 합",
                  "고등학교 대수 수열의 합 문제: ∑의 뜻과 성질, ∑k, ∑k², ∑k³ 공식, ∑(ak + b)의 계산, 분수 꼴 수열의 합(부분분수)까지 100문제와 정답·해설.",
                  "∑k = n(n + 1)/2", "∑k² = n(n + 1)(2n + 1)/6, ∑k³ = {n(n + 1)/2}²",
                  ["∑<sub>k=1</sub><sup>n</sup> a<sub>k</sub> = a<sub>1</sub> + a<sub>2</sub> + … + a<sub>n</sub>이에요.",
                   "∑(a<sub>k</sub> ± b<sub>k</sub>) = ∑a<sub>k</sub> ± ∑b<sub>k</sub>, ∑ca<sub>k</sub> = c∑a<sub>k</sub>, ∑c = cn",
                   "∑k = n(n + 1)/2, ∑k² = n(n + 1)(2n + 1)/6, ∑k³ = {n(n + 1)/2}²",
                   "1/(k(k + 1)) = 1/k − 1/(k + 1)처럼 나누면 대부분의 항이 지워져요."],
                  [("∑<sub>k=1</sub><sup>10</sup> (2k + 1)", ["2 × 55 + 10"], "120"), ("∑<sub>k=1</sub><sup>9</sup> 1/(k(k + 1))", ["1 − 1/10"], "9/10")],
                  [("∑a<sub>k</sub>b<sub>k</sub> = ∑a<sub>k</sub> × ∑b<sub>k</sub>", "곱은 나눌 수 없어요."), ("∑c = c로 계산한다", "c를 n번 더하므로 cn이에요."), ("∑k²을 (∑k)²으로 계산한다", "∑k³ = (∑k)²이에요.")],
                  [("∑의 아래·위 숫자는?", "아래는 시작하는 k, 위는 끝나는 k예요."), ("부분분수는 언제 쓰나요?", "분모가 연속한 두 식의 곱일 때 써요.")],
                  [("∑의 성질", [(sm_main(("const", "prop")), 20)]), ("∑k와 ∑k²", [(sm_main(("k", "k2")), 20)]), ("∑(ak + b)", [(sm_main(("lin",)), 20)]),
                   ("∑k³", [(sm_main(("k3",)), 8), (sm_main(("lin", "k2")), 12)]), ("분수 꼴 수열의 합", [(sm_main(("tele",)), 20)])], 83213)
    U["rec"] = ("recursive-sequences-and-induction", 14, "[12대수03-06] [12대수03-07]", "수열의 귀납적 정의를 설명할 수 있다. 수학적 귀납법의 원리를 이해하고, 이를 이용하여 명제를 증명할 수 있다.",
                "수열의 귀납적 정의와 수학적 귀납법", "수열의 귀납적 정의",
                "고등학교 대수 수열의 귀납적 정의 문제: aₙ₊₁ = aₙ + d, aₙ₊₁ = raₙ, aₙ₊₁ = paₙ + q, aₙ₊₁ = aₙ + f(n), 피보나치 수열의 항 구하기와 수학적 귀납법의 원리까지 100문제와 정답·해설.",
                "첫째항과 이웃한 항 사이의 관계", "수학적 귀납법: n = 1에서 성립 + k에서 k + 1로",
                ["첫째항과 이웃한 항들 사이의 관계식으로 수열을 정하는 것을 <b>귀납적 정의</b>라고 해요.",
                 "a<sub>n+1</sub> = a<sub>n</sub> + d는 등차수열, a<sub>n+1</sub> = ra<sub>n</sub>은 등비수열이에요.",
                 "a<sub>n+1</sub> = a<sub>n</sub> + f(n)이면 a<sub>n</sub> = a<sub>1</sub> + ∑<sub>k=1</sub><sup>n−1</sup> f(k)예요.",
                 "<b>수학적 귀납법</b>: ① n = 1일 때 성립, ② n = k일 때 성립하면 n = k + 1일 때도 성립함을 보여요."],
                [("a<sub>1</sub> = 2, a<sub>n+1</sub> = 3a<sub>n</sub> − 1", ["a<sub>2</sub> = 5, a<sub>3</sub> = 14"], "a<sub>4</sub> = 41"), ("a<sub>1</sub> = 1, a<sub>n+1</sub> = a<sub>n</sub> + n", ["a<sub>5</sub> = 1 + (1 + 2 + 3 + 4)"], "11")],
                [("a<sub>n+1</sub> = a<sub>n</sub> + n에서 n까지 더한다", "a<sub>n</sub>까지는 n − 1까지 더해요."), ("귀납법에서 n = 1을 확인하지 않는다", "출발점이 있어야 모든 자연수에서 성립해요."), ("a<sub>n+2</sub>를 구할 때 한 항만 쓴다", "앞의 두 항을 모두 써요.")],
                [("직접 대입하는 것도 괜찮나요?", "작은 n은 차례로 대입하는 것이 가장 확실해요."), ("귀납법은 도미노와 같나요?", "네, 첫 번째가 넘어지고 하나가 넘어지면 다음도 넘어지는 원리예요.")],
                [("등차·등비수열의 귀납적 정의", [(rc_main(("ar", "ge")), 20)]), ("a<sub>n+1</sub> = pa<sub>n</sub> + q", [(rc_main(("mix",)), 20)]), ("a<sub>n+1</sub> = a<sub>n</sub> + f(n)", [(rc_main(("addn",)), 20)]),
                 ("이웃한 세 항의 관계", [(rc_main(("fib",)), 20)]), ("수학적 귀납법", [(rc_main(("concept",)), 9), (rc_main(("ar", "ge", "mix")), 11)])], 83214)
    t = U[which]
    slug, sort, code, std, title, short, meta, kb, ks, think, ex_, mist, faq, spec, seed = t
    return unit(G, slug, sort, code, std, title, short, meta, kb, ks, think, ex_, mist, faq, spec, seed)
