# -*- coding: utf-8 -*-
"""
대한민국 중학교 3학년 수학（2022 개정）：수와 연산・변화와 관계の 9 単元
  sqrt  : 제곱근과 그 성질 [9수01-07]
  real  : 무리수와 실수 [9수01-08] [9수01-09]
  rad   : 근호를 포함한 식의 계산 [9수01-10]
  mulp  : 다항식의 곱셈과 곱셈 공식 [9수02-19]
  fact  : 인수분해 [9수02-19]
  qeq   : 이차방정식 [9수02-20]
  qword : 이차방정식의 활용 [9수02-20]
  qf    : 이차함수 y = a(x − p)² + q [9수02-21] [9수02-22]
  qfg   : 이차함수 y = ax² + bx + c의 그래프 [9수02-22]
誤答は「√(a²) = a（a의 부호를 보지 않는다）」「√a + √b = √(a + b)」「(a + b)² = a² + b²」「인수분해에서 부호를 반대로 한다」
「x² = 4의 해를 x = 2만 쓴다」「꼭짓점 (p, q)에서 p의 부호를 반대로 읽는다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_common import josa, Names, num, fr
from kr_mid import M, N, neg, par, sg, dec, sup, unit, kurve, fig, BLUE, RED
from kr_m2a import poly2

R = random.Random(82901)
NM = Names(R)
G = "grade-9"


def sq_split(n):
    a, b = 1, n
    k = 2
    while k * k <= b:
        while b % (k * k) == 0:
            a *= k
            b //= k * k
        k += 1
    return a, b


def surd(c, n):
    """c√n（n은 제곱인수 없는 수로 정리）"""
    a, b = sq_split(n)
    c = Fr(c) * a
    if c == 0:
        return "0"
    if b == 1:
        return neg(c)
    if c == 1:
        return "√%d" % b
    if c == -1:
        return "−√%d" % b
    return neg(c) + "√%d" % b


def P1(coefs, v="x"):
    """[a2, a1, a0] → ax² + bx + c"""
    d = {}
    n = len(coefs) - 1
    for i, c in enumerate(coefs):
        if c:
            d[(n - i, 0)] = c
    return poly2(d, (v, "_")) if d else "0"


def P2(d, vs=("a", "b")):
    return poly2(d, vs)


# ------------------------------------------------------------------ 제곱근
def s_basic(kinds=("roots", "sqrt", "square", "abs", "nat")):
    def mk():
        how = R.choice(kinds)
        n = R.randint(2, 20)
        if how == "roots":
            v = n * n
            k = R.choice(["int", "frac", "dec"])
            if k == "int":
                return M("<b>%d</b>의 제곱근은?" % v, "±%d" % n, ["%d" % n, "−%d" % n, "±%d" % (v // 2) if v // 2 != n else "±%d" % (n + 1), "±√%d" % n], "제곱하여 %d가 되는 수는 %d와 −%d예요. <b>±%d</b>" % (v, n, n, n))
            if k == "frac":
                a, b = R.randint(1, 9), R.randint(2, 9)
                if math.gcd(a, b) != 1:
                    return None
                return M("<b>%s</b>의 제곱근은?" % fr(a * a, b * b), "±" + fr(a, b), [fr(a, b), "±" + fr(a * a, b), "±" + fr(a, b * b)], "<b>±%s</b>" % fr(a, b))
            a = R.randint(1, 9)
            return M("<b>%s</b>의 제곱근은?" % dec(Fr(a * a, 100)), "±%s" % dec(Fr(a, 10)), [dec(Fr(a, 10)), "±%s" % dec(Fr(a, 100)), "±%s" % dec(Fr(a * a, 10))], "(%s)² = %s. <b>±%s</b>" % (dec(Fr(a, 10)), dec(Fr(a * a, 100)), dec(Fr(a, 10))))
        if how == "sqrt":
            m = R.choice([2, 3, 5, 6, 7, 10, 11, 13, 15, 17])
            k = R.choice(["neg", "sq"])
            if k == "sq":
                return N("<b>(−√%d)²</b>의 값은?" % m, m, [-m, m * m, 2 * m, Fr(m, 2) if m % 2 == 0 else m + 1], "(−√a)² = a. <b>%d</b>" % m)
            return M("<b>%d의 음의 제곱근</b>은?" % m, "−√%d" % m, ["√%d" % m, "±√%d" % m, "−%d" % m], "음의 제곱근은 <b>−√%d</b>예요." % m)
        if how == "square":
            a, b = R.randint(2, 9), R.randint(2, 9)
            s1, s2 = R.choice([1, -1]), R.choice([1, -1])
            v = s1 * a + s2 * b
            t1 = "√(%d²)" % a if s1 > 0 else "−√(%d²)" % a
            t2 = "√((−%d)²)" % b
            v = s1 * a + b
            return N("<b>%s + %s</b>를 계산하면?" % (t1, t2), v, [s1 * a - b, -s1 * a - b, s1 * a * a + b * b, a + b if v != a + b else a - b], "√((−%d)²) = %d이에요. <b>%s</b>" % (b, b, neg(v)))
        if how == "abs":
            a = R.randint(1, 9)
            k = R.choice(["lt", "gt"])
            if k == "lt":
                return M("x &lt; %d일 때, <b>√((x − %d)²)</b>을 간단히 하면?" % (a, a), "−x + %d" % a, ["x − %d" % a, "x + %d" % a, "−x − %d" % a], "x − %d &lt; 0이므로 −(x − %d) = <b>−x + %d</b>" % (a, a, a))
            return M("x &gt; %d일 때, <b>√((x − %d)²)</b>을 간단히 하면?" % (a, a), "x − %d" % a, ["−x + %d" % a, "x + %d" % a, "−x − %d" % a], "x − %d &gt; 0이므로 <b>x − %d</b>" % (a, a))
        m = R.choice([12, 18, 20, 24, 27, 28, 40, 45, 48, 50, 54, 63, 72, 75, 80, 90, 98])
        a, b = sq_split(m)
        k = R.choice(["mul", "div"])
        if k == "mul":
            return N("<b>√(%dx)</b>가 자연수가 되도록 하는 가장 작은 자연수 x는?" % m, b, [m, a, b * 4, b + 1], "%d = %d² × %d이므로 x = <b>%d</b>" % (m, a, b, b))
        return N("<b>√(%d/x)</b>가 자연수가 되도록 하는 가장 작은 자연수 x는?" % m, b, [m, a * a, a, b * a * a if b * a * a != m else b + 1], "%d = %d² × %d이므로 %d로 나누면 %d². x = <b>%d</b>" % (m, a, b, b, a, b))
    return mk


def s_compare(kinds=("cmp", "between", "count")):
    def mk():
        how = R.choice(kinds)
        if how == "cmp":
            a = R.randint(2, 9)
            b = R.choice([x for x in range(a * a - 6, a * a + 7) if x > 0 and x != a * a])
            gt = b > a * a
            nega = R.random() < 0.4
            if nega:
                ok = "−√%d %s −%d" % (b, "&lt;" if gt else "&gt;", a)
                bad = "−√%d %s −%d" % (b, "&gt;" if gt else "&lt;", a)
                return M("두 수의 대소 관계로 옳은 것은?", ok, [bad, "−√%d = −%d" % (b, a), "알 수 없어요"], "%d = √%d이고, 음수는 절댓값이 클수록 작아요. <b>%s</b>" % (a, a * a, ok))
            ok = "√%d %s %d" % (b, "&gt;" if gt else "&lt;", a)
            bad = "√%d %s %d" % (b, "&lt;" if gt else "&gt;", a)
            return M("두 수 √%d와 %d의 대소 관계로 옳은 것은?" % (b, a), ok, [bad, "√%d = %d" % (b, a), "알 수 없어요"], "%d = √%d이므로 <b>%s</b>" % (a, a * a, ok))
        if how == "between":
            n = R.randint(5, 99)
            a = math.isqrt(n)
            if a * a == n:
                return None
            return M("<b>√%d</b>은 어느 두 정수 사이에 있을까요?" % n, "%d와 %d 사이" % (a, a + 1), ["%d와 %d 사이" % (a - 1, a), "%d와 %d 사이" % (a + 1, a + 2), "%d와 %d 사이" % (n // 2, n // 2 + 1) if n // 2 not in (a - 1, a, a + 1) else "%d와 %d 사이" % (a + 2, a + 3)],
                     "%d² = %d &lt; %d &lt; %d = %d²이므로 <b>%d와 %d 사이</b>" % (a, a * a, n, (a + 1) ** 2, a + 1, a, a + 1))
        a, b = R.randint(1, 6), R.randint(1, 6)
        if a >= b:
            return None
        c = b * b - a * a - 1
        return N("<b>%d &lt; √x &lt; %d</b>를 만족하는 자연수 x의 개수는?" % (a, b), c, [c + 1, c + 2, b - a, b * b - a * a], "%d &lt; x &lt; %d이므로 %d부터 %d까지 <b>%d개</b>" % (a * a, b * b, a * a + 1, b * b - 1, c), f=lambda v: "%s개" % neg(v))
    return mk


# ------------------------------------------------------------------ 무리수와 실수
SQ = [4, 9, 16, 25, 36, 49, 64, 81, 100]
NSQ = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15]


def r_irr(kinds=("which", "whichnot", "count", "concept")):
    def mk():
        how = R.choice(kinds)
        irr = ["√%d" % R.choice(NSQ), "π", "−√%d" % R.choice(NSQ), "%d + √%d" % (R.randint(1, 5), R.choice(NSQ)), "√%d/%d" % (R.choice(NSQ), R.randint(2, 5))]
        rat = ["√%d" % R.choice(SQ), "−√%d" % R.choice(SQ), "0.%ḋ" % R.randint(1, 9), R.choice([fr(1, 3), fr(2, 7), fr(5, 9), fr(3, 4), fr(4, 5), fr(7, 8)]), "√(%s)" % fr(1, R.choice([4, 9, 16, 25])), "%s" % dec(Fr(R.randint(1, 99), 10)), "−%d" % R.randint(1, 9)]
        if how == "which":
            ok = R.choice(irr)
            w = R.sample(rat, 3)
            al = w + [ok]
            R.shuffle(al)
            return M("%s 중 <b>무리수</b>인 것은?" % ", ".join(al), ok, w, "순환하지 않는 무한소수예요. <b>%s</b>" % ok)
        if how == "whichnot":
            ok = R.choice(rat)
            w = R.sample(irr, 3)
            al = w + [ok]
            R.shuffle(al)
            return M("%s 중 무리수가 <b>아닌</b> 것은?" % ", ".join(al), ok, w, "<b>%s</b>는 분수로 나타낼 수 있는 유리수예요." % ok)
        if how == "count":
            k = R.randint(1, 4)
            items = R.sample(irr, k) + R.sample(rat, 6 - k)
            R.shuffle(items)
            return N("다음 수 중 무리수는 몇 개일까요?<br>%s" % ", ".join(items), k, [6 - k, k + 1, k - 1 if k > 1 else k + 2, 6], "무리수: %s. <b>%d개</b>" % (", ".join(x for x in items if x in irr), k), f=lambda v: "%s개" % neg(v))
        F_ = [("유리수와 무리수를 통틀어 무엇이라고 할까요?", "실수", ["정수", "자연수", "소수"], "<b>실수</b>예요."),
              ("무리수에 대한 설명으로 옳은 것은?", "순환하지 않는 무한소수예요", ["분수로 나타낼 수 있어요", "유한소수예요", "순환소수예요"], "<b>순환하지 않는 무한소수</b>예요."),
              ("수직선에 대한 설명으로 옳은 것은?", "실수에 대응하는 점으로 완전히 메울 수 있어요", ["유리수만으로 완전히 메울 수 있어요", "무리수는 나타낼 수 없어요", "정수에 대응하는 점이 가장 많아요"], "<b>실수</b>로 수직선을 완전히 메울 수 있어요."),
              ("두 무리수의 합은 항상 무리수일까요?", "아니요, 유리수일 수도 있어요", ["네, 항상 무리수예요", "항상 0이에요", "항상 자연수예요"], "√2 + (−√2) = 0처럼 <b>유리수일 수도 있어요</b>."),
              ("√4는 무리수일까요?", "아니요, 2이므로 유리수예요", ["네, 근호가 있으므로 무리수예요", "음수예요", "실수가 아니에요"], "√4 = 2이므로 <b>유리수</b>예요.")]
        return M(*R.choice(F_))
    return mk


def r_line(kinds=("pt", "int", "frac", "order")):
    def mk():
        how = R.choice(kinds)
        if how == "pt":
            a = R.randint(-3, 3)
            s = R.choice([1, 2])
            n = 2 * s * s if s == 1 else R.choice([5, 10, 13])
            if s == 1:
                n = R.choice([2, 5, 8, 10, 13])
            p, q = {2: (1, 1), 5: (1, 2), 8: (2, 2), 10: (1, 3), 13: (2, 3)}[n]
            d = R.choice([1, -1])
            ok = "%s %s √%d" % (neg(a), "+" if d > 0 else "−", n) if a else ("√%d" % n if d > 0 else "−√%d" % n)
            ok = ok.replace("√8", "2√2")
            bad = ["%s %s √%d" % (neg(a), "−" if d > 0 else "+", n) if a else ("−√%d" % n if d > 0 else "√%d" % n), "%s" % neg(a + d * (p + q)), "%s %s √%d" % (neg(a + d), "+" if d > 0 else "−", n)]
            bad = [b.replace("√8", "2√2") for b in bad]
            return M("수직선 위의 점 %s를 한 꼭짓점으로 하고 가로 %d, 세로 %d인 직사각형의 대각선을 반지름으로 하는 원을 %s쪽으로 그렸어요. 원과 수직선이 만나는 점이 나타내는 수는?" % (neg(a), p, q, "오른" if d > 0 else "왼"),
                     ok, bad, "대각선의 길이는 √(%d² + %d²) = √%d이에요. <b>%s</b>" % (p, q, n, ok))
        if how == "int":
            n = R.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24])
            a = math.isqrt(n)
            k = R.choice(["int", "frac"])
            if k == "int":
                c = R.randint(1, 5)
                return N("<b>%d + √%d</b>의 정수 부분은?" % (c, n), c + a, [c + a + 1, a, c, c + a - 1], "%d &lt; √%d &lt; %d이므로 <b>%d</b>" % (a, n, a + 1, c + a))
            return M("<b>√%d</b>의 소수 부분은?" % n, "√%d − %d" % (n, a), ["√%d − %d" % (n, a + 1), "√%d + %d" % (n, a), "%d − √%d" % (a + 1, n)], "정수 부분이 %d이므로 <b>√%d − %d</b>" % (a, n, a))
        if how == "frac":
            a, b = R.randint(2, 8), R.choice([2, 3, 5, 6, 7])
            c = R.randint(1, 4)
            x = a - math.sqrt(b)
            ok = "&gt;" if a > c + math.sqrt(b) else "&lt;"
            if abs(a - c - math.sqrt(b)) < 0.05:
                return None
            return M("두 수 <b>%d − √%d</b>와 <b>%d</b>의 대소 관계는?" % (a, b, c), "%d − √%d %s %d" % (a, b, ok, c), ["%d − √%d %s %d" % (a, b, "&lt;" if ok == "&gt;" else "&gt;", c), "%d − √%d = %d" % (a, b, c), "알 수 없어요"],
                     "(%d − √%d) − %d = %d − √%d의 부호를 봐요. <b>%s</b>" % (a, b, c, a - c, b, ok))
        nums = R.sample([("√%d" % n, math.sqrt(n)) for n in NSQ] + [(str(k), k) for k in range(1, 5)] + [("−√%d" % n, -math.sqrt(n)) for n in NSQ[:5]], 4)
        if len(set(round(v, 4) for _, v in nums)) < 4:
            return None
        s = sorted(nums, key=lambda t: t[1])
        k = R.choice(["max", "min"])
        ok = s[-1][0] if k == "max" else s[0][0]
        return M("다음 중 가장 %s 수는? %s" % ("큰" if k == "max" else "작은", ", ".join(n for n, _ in nums)), ok, [n for n, _ in nums if n != ok], "제곱하거나 근삿값으로 비교해요. <b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 근호를 포함한 식
def d_muldiv(kinds=("mul", "div", "out", "in", "rat")):
    def mk():
        how = R.choice(kinds)
        a, b = R.choice(NSQ), R.choice(NSQ)
        if how == "mul":
            c, d = R.randint(1, 4), R.randint(1, 4)
            ok = surd(c * d, a * b)
            return M("<b>%s × %s</b>를 계산하면?" % (surd(c, a), surd(d, b)), ok, [surd(c + d, a * b), surd(c * d, a + b), surd(1, a * b * c * d) if surd(1, a * b * c * d) != ok else surd(c * d + 1, a * b), surd(c * d, a * b * 2)],
                     "계수끼리, 근호 안끼리 곱해요. <b>%s</b>" % ok)
        if how == "div":
            c = R.randint(1, 4)
            ok = surd(c, a)
            return M("<b>%s ÷ √%d</b>를 계산하면?" % (surd(c, a * b), b), ok, [surd(c, a * b * b), surd(c, a + b) if a + b != a else surd(c + 1, a), surd(1, a), surd(c * b, a)], "√(%d) ÷ √%d = √%d. <b>%s</b>" % (a * b, b, a, ok))
        if how == "out":
            n = R.choice([8, 12, 18, 20, 24, 27, 28, 32, 45, 48, 50, 54, 63, 72, 75, 80, 98])
            p, q = sq_split(n)
            ok = surd(1, n)
            return M("<b>√%d</b>를 a√b 꼴로 나타내면? (b는 가장 작은 자연수)" % n, ok, ["%d√%d" % (q, p * p) if q != 1 else "√%d" % n, "%d√%d" % (p * p, q), "%d√%d" % (p, q * 2), "%d√%d" % (p + 1, q)], "%d = %d² × %d이므로 <b>%s</b>" % (n, p, q, ok))
        if how == "in":
            p, q = R.randint(2, 6), R.choice([2, 3, 5, 6, 7])
            return M("<b>%d√%d</b>를 √a 꼴로 나타내면?" % (p, q), "√%d" % (p * p * q), ["√%d" % (p * q), "√%d" % (p * q * q), "√%d" % (p + q), "√%d" % (2 * p * q)], "%d = √%d이므로 √(%d × %d) = <b>√%d</b>" % (p, p * p, p * p, q, p * p * q))
        c = R.randint(1, 9)
        k = R.choice([1, 2, 3])
        b = R.choice([2, 3, 5, 6, 7])
        v = Fr(c, k * b)
        ok = (fr(v.numerator, v.denominator) if v.denominator != 1 else neg(v)) + "√%d" % b if v != 1 else "√%d" % b
        if v.numerator == 1 and v.denominator != 1:
            ok = fr("√%d" % b, v.denominator)
        elif v.denominator != 1:
            ok = fr("%d√%d" % (v.numerator, b), v.denominator)
        den = "√%d" % b if k == 1 else "%d√%d" % (k, b)
        return M("<b>%s</b>의 분모를 유리화하면?" % fr(c, den), ok, [fr("%d√%d" % (c, b), k) if k != 1 else "%d√%d" % (c, b), fr(c, "%d" % (k * b)), fr("√%d" % b, c * k) if c * k != v.denominator else fr("√%d" % (b + 1), c), "%s√%d" % (neg(c * b), b)],
                 "분모와 분자에 √%d를 곱해요. <b>%s</b>" % (b, ok))
    return mk


def d_addsub(kinds=("like", "simp", "dist", "mix")):
    def mk():
        how = R.choice(kinds)
        b = R.choice([2, 3, 5, 6, 7])
        if how == "like":
            a, c, d = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
            op1, op2 = R.choice([1, -1]), R.choice([1, -1])
            v = a + op1 * c + op2 * d
            s = "%d√%d %s %d√%d %s %d√%d" % (a, b, "+" if op1 > 0 else "−", c, b, "+" if op2 > 0 else "−", d, b)
            return M("<b>%s</b>를 계산하면?" % s, surd(v, b) if v else "0", [surd(a + c + d, b), surd(v, 3 * b), surd(v + 2, b) if v + 2 else "√%d" % b, neg(v * b) if v else "1"], "√%d의 계수끼리 계산해요. <b>%s</b>" % (b, surd(v, b) if v else "0"))
        if how == "simp":
            m1, m2 = R.sample([1, 2, 3, 4, 5], 2)
            s1, s2 = m1 * m1 * b, m2 * m2 * b
            op = R.choice([1, -1])
            v = m1 + op * m2
            q = "√%d %s √%d" % (s1, "+" if op > 0 else "−", s2)
            return M("<b>%s</b>를 계산하면?" % q, surd(v, b) if v else "0", ["√%d" % (s1 + op * s2) if s1 + op * s2 > 0 else "0" if False else "√%d" % (s1 + s2), surd(v, 2 * b), surd(m1 * m2, b), surd(-v, b) if v else "1"],
                     "%s = %s, %s = %s로 고친 뒤 계산해요. <b>%s</b>" % ("√%d" % s1, surd(1, s1), "√%d" % s2, surd(1, s2), surd(v, b) if v else "0"))
        if how == "dist":
            a, c = R.randint(1, 5), R.choice([2, 3, 5, 7])
            d = R.randint(1, 5)
            if c == b:
                return None
            # √b(a√b + d√c) = ab + d√(bc)
            ok = "%d + %s" % (a * b, surd(d, b * c))
            return M("<b>√%d(%s + %s)</b>를 계산하면?" % (b, surd(a, b), surd(d, c)), ok, ["%s + %s" % (surd(a, b * b), surd(d, b * c)), "%d + %s" % (a * b, surd(d, c)), "%d + %s" % (a, surd(d, b * c)), "%s" % surd(a + d, b * c)],
                     "분배법칙: √%d × %s = %d, √%d × %s = %s. <b>%s</b>" % (b, surd(a, b), a * b, b, surd(d, c), surd(d, b * c), ok))
        a = R.randint(1, 6)
        c = R.randint(1, 6)
        v = Fr(a) + Fr(c, b) * b
        q = "%d√%d + %s" % (a, b, fr(c * b, "√%d" % b))
        tot = a + c
        return M("<b>%s</b>를 계산하면?" % q, surd(tot, b), [surd(a + c * b, b), surd(tot, 2 * b), "%d√%d" % (a, b), surd(a * c, b)], "%s = %s이므로 <b>%s</b>" % (fr(c * b, "√%d" % b), surd(c, b), surd(tot, b)))
    return mk


# ------------------------------------------------------------------ 곱셈 공식
def m_formula(kinds=("sq+", "sq-", "conj", "xab", "axb")):
    def mk():
        how = R.choice(kinds)
        a, b = R.randint(1, 5), R.randint(1, 9)
        if how == "sq+":
            ok = P1([a * a, 2 * a * b, b * b])
            return M("<b>(%s)²</b>을 전개하면?" % P1([a, b]), ok, [P1([a * a, 0, b * b]), P1([a * a, a * b, b * b]), P1([a * a, 2 * a * b, 2 * b]), P1([2 * a, 2 * a * b, b * b]) if a != 1 else P1([a * a, -2 * a * b, b * b])],
                     "(A + B)² = A² + 2AB + B². <b>%s</b>" % ok)
        if how == "sq-":
            ok = P1([a * a, -2 * a * b, b * b])
            return M("<b>(%s)²</b>을 전개하면?" % P1([a, -b]), ok, [P1([a * a, 0, -b * b]), P1([a * a, -2 * a * b, -b * b]), P1([a * a, 2 * a * b, b * b]), P1([a * a, -a * b, b * b])],
                     "(A − B)² = A² − 2AB + B². <b>%s</b>" % ok)
        if how == "conj":
            ok = P1([a * a, 0, -b * b])
            return M("<b>(%s)(%s)</b>를 전개하면?" % (P1([a, b]), P1([a, -b])), ok, [P1([a * a, 0, b * b]), P1([a * a, -2 * a * b, -b * b]), P1([a, 0, -b]), P1([a * a, 2 * a * b, -b * b])],
                     "(A + B)(A − B) = A² − B². <b>%s</b>" % ok)
        if how == "xab":
            p, q = R.choice([-7, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]), R.choice([-6, -5, -3, -2, 1, 2, 3, 4, 5, 7])
            if p == q or p + q == 0:
                return None
            ok = P1([1, p + q, p * q])
            return M("<b>(%s)(%s)</b>를 전개하면?" % (P1([1, p]), P1([1, q])), ok, [P1([1, p * q, p + q]), P1([1, -(p + q), p * q]), P1([1, p + q, -p * q]), P1([1, 0, p * q])],
                     "(x + a)(x + b) = x² + (a + b)x + ab. <b>%s</b>" % ok)
        p, q, r, s = R.randint(1, 4), R.choice([-5, -3, -2, -1, 1, 2, 3, 4]), R.randint(2, 4), R.choice([-4, -3, -1, 1, 2, 3, 5])
        ok = P1([p * r, p * s + q * r, q * s])
        return M("<b>(%s)(%s)</b>를 전개하면?" % (P1([p, q]), P1([r, s])), ok, [P1([p * r, p * s - q * r, q * s]), P1([p * r, 0, q * s]), P1([p * r, p * r + q * s, q * s]), P1([p * r, p * s + q * r, -q * s])],
                 "(ax + b)(cx + d) = acx² + (ad + bc)x + bd. <b>%s</b>" % ok)
    return mk


def m_apply(kinds=("calc", "box", "val", "surd")):
    def mk():
        how = R.choice(kinds)
        if how == "calc":
            k = R.choice(["sq", "conj"])
            if k == "sq":
                n = R.choice([10, 20, 30, 50, 100]) + R.choice([-2, -1, 1, 2, 3])
                base = round(n, -1) if n < 100 else 100
                d = n - base
                return N("곱셈 공식을 이용하여 <b>%d²</b>을 계산하면?" % n, n * n, [base * base + d * d, base * base + 2 * base * d, n * n + 1, n * 2 * 10], "(%d %s %d)² = %d %s %d + %d = <b>%s</b>" % (base, "+" if d > 0 else "−", abs(d), base * base, "+" if d > 0 else "−", abs(2 * base * d), d * d, num(n * n)))
            base = R.choice([20, 30, 50, 100])
            d = R.randint(1, 4)
            return N("곱셈 공식을 이용하여 <b>%d × %d</b>를 계산하면?" % (base + d, base - d), base * base - d * d, [base * base + d * d, base * base, base * base - 2 * d, base * base - d], "(%d + %d)(%d − %d) = %d − %d = <b>%s</b>" % (base, d, base, d, base * base, d * d, num(base * base - d * d)))
        if how == "box":
            a, b = R.randint(1, 5), R.randint(1, 9)
            k = R.choice(["mid", "last"])
            if k == "mid":
                return N("(%dx + □)² = %s일 때, □ 안에 알맞은 양수는?" % (a, P1([a * a, 2 * a * b, b * b])), b, [b * b, 2 * b, Fr(b, 2), b + 1], "□² = %d이므로 <b>%d</b>" % (b * b, b))
            return N("(x + %d)(x + □) = %s일 때, □ 안에 알맞은 수는?" % (a, P1([1, a + b, a * b])), b, [a * b, a + b, b + 1, -b], "%d × □ = %d → <b>%d</b>" % (a, a * b, b))
        if how == "val":
            s, p = R.randint(2, 9), R.randint(1, 8)
            k = R.choice(["sum", "diff"])
            if s * s < 4 * p:
                return None
            if k == "sum":
                return N("a + b = %d, ab = %d일 때, a² + b²의 값은?" % (s, p), s * s - 2 * p, [s * s + 2 * p, s * s - p, s * s, s * s - 4 * p], "a² + b² = (a + b)² − 2ab = %d − %d = <b>%d</b>" % (s * s, 2 * p, s * s - 2 * p))
            if s * s < 4 * p:
                return None
            return N("a + b = %d, ab = %d일 때, (a − b)²의 값은?" % (s, p), s * s - 4 * p, [s * s - 2 * p, s * s + 4 * p, s * s, s * s - p], "(a − b)² = (a + b)² − 4ab = %d − %d = <b>%d</b>" % (s * s, 4 * p, s * s - 4 * p))
        a, b = R.randint(1, 4), R.choice([2, 3, 5, 6, 7])
        k = R.choice(["sq", "conj"])
        if k == "sq":
            ok = "%d + %s" % (a * a + b, surd(2 * a, b))
            return M("<b>(%d + √%d)²</b>을 계산하면?" % (a, b), ok, ["%d" % (a * a + b), "%d + %s" % (a * a + b, surd(a, b)), "%d + %s" % (a * a + b * b, surd(2 * a, b))], "%d + 2 × %d × √%d + %d = <b>%s</b>" % (a * a, a, b, b, ok))
        if a * a == b:
            return None
        return N("<b>(%d + √%d)(%d − √%d)</b>를 계산하면?" % (a, b, a, b), a * a - b, [a * a + b, a * a - b * b, a - b, a * a - 2 * b], "%d² − (√%d)² = <b>%s</b>" % (a, b, neg(a * a - b)))
    return mk


# ------------------------------------------------------------------ 인수분해
def f_factor(kinds=("common", "perfect", "diff", "trin", "atrin")):
    def mk():
        how = R.choice(kinds)
        if how == "common":
            c = R.randint(2, 6)
            a, b = R.randint(1, 5), R.choice([-7, -5, -3, -2, -1, 1, 2, 3, 4, 5])
            if math.gcd(a, b) != 1:
                return None
            ok = "%sx(%s)" % (neg(c) if c != 1 else "", P1([a, b]))
            q = P1([c * a, c * b, 0])
            return M("<b>%s</b>를 인수분해하면?" % q, ok, ["%s(%s)" % (neg(c), P1([a, b, 0])) if False else "x(%s)" % P1([c * a, c * b]), "%sx(%s)" % (neg(c), P1([a, -b])), "%s(%s)" % (neg(c), P1([a, b])), "%sx(%s)" % (neg(c), P1([a, b * c]))],
                     "공통인수 %sx로 묶어요. <b>%s</b>" % (neg(c), ok))
        if how == "perfect":
            a, b = R.randint(1, 4), R.choice([-7, -5, -4, -3, -2, -1, 1, 2, 3, 5, 6])
            ok = "(%s)²" % P1([a, b])
            return M("<b>%s</b>를 인수분해하면?" % P1([a * a, 2 * a * b, b * b]), ok, ["(%s)²" % P1([a, -b]), "(%s)(%s)" % (P1([a, b]), P1([a, -b])), "(%s)²" % P1([a, 2 * b]), "(%s)²" % P1([a * a, b])],
                     "A² ± 2AB + B² = (A ± B)². <b>%s</b>" % ok)
        if how == "diff":
            a, b = R.randint(1, 5), R.randint(1, 9)
            if math.gcd(a, b) != 1:
                return None
            ok = "(%s)(%s)" % (P1([a, b]), P1([a, -b]))
            return M("<b>%s</b>를 인수분해하면?" % P1([a * a, 0, -b * b]), ok, ["(%s)²" % P1([a, -b]), "(%s)²" % P1([a, b]), "(%s)(%s)" % (P1([a * a, b]), P1([1, -b])), "(%s)(%s)" % (P1([a, b * b]), P1([a, -1]))],
                     "A² − B² = (A + B)(A − B). <b>%s</b>" % ok)
        if how == "trin":
            p, q = R.choice([-8, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 7]), R.choice([-7, -6, -4, -3, -2, 1, 2, 3, 4, 6, 8])
            if p == q or p + q == 0:
                return None
            pq = lambda u, v: "(%s)(%s)" % (P1([1, max(u, v)]), P1([1, min(u, v)])) if u != v else "(%s)²" % P1([1, u])
            p, q = max(p, q), min(p, q)
            ok = pq(p, q)
            cands = [(-p, -q), (-p, q), (p, -q), (p * q, 1), (p + q, 1), (p - 1, q + 1)]
            wr = [pq(u, v) for u, v in cands if sorted((u, v)) != sorted((p, q))]
            return M("<b>%s</b>를 인수분해하면?" % P1([1, p + q, p * q]), ok, wr,
                     "곱이 %s, 합이 %s인 두 수는 %s, %s예요. <b>%s</b>" % (neg(p * q), neg(p + q), neg(p), neg(q), ok))
        a, c = R.choice([(2, 1), (3, 1), (2, 3), (3, 2), (4, 1), (5, 1), (2, 5)])
        b, d = R.choice([-5, -3, -2, -1, 1, 2, 3, 4]), R.choice([-4, -3, -1, 1, 2, 3, 5])
        if math.gcd(a, b) != 1 or math.gcd(c, d) != 1:
            return None
        ok = "(%s)(%s)" % (P1([a, b]), P1([c, d]))
        return M("<b>%s</b>를 인수분해하면?" % P1([a * c, a * d + b * c, b * d]), ok, ["(%s)(%s)" % (P1([a, d]), P1([c, b])), "(%s)(%s)" % (P1([a, -b]), P1([c, -d])), "(%s)(%s)" % (P1([a, b]), P1([c, -d])), "(%s)(%s)" % (P1([a * c, b]), P1([1, d]))],
                 "x²의 계수 %d, 상수항 %s를 나누어 대각선으로 곱해 더하면 %s예요. <b>%s</b>" % (a * c, neg(b * d), neg(a * d + b * c), ok))
    return mk


def f_apply(kinds=("box", "calc", "common2", "factor_of")):
    def mk():
        how = R.choice(kinds)
        if how == "box":
            k = R.choice(["mid", "last"])
            a = R.randint(1, 8)
            if k == "mid":
                return N("<b>x² + □x + %d</b>가 완전제곱식이 되도록 하는 양수 □는?" % (a * a), 2 * a, [a, a * a, 4 * a, 2 * a + 1], "(x + %d)² = x² + %dx + %d. <b>%d</b>" % (a, 2 * a, a * a, 2 * a))
            return N("<b>x² + %dx + □</b>가 완전제곱식이 되도록 하는 수 □는?" % (2 * a), a * a, [2 * a, a, 4 * a * a, a * a + 1], "(%d ÷ 2)² = <b>%d</b>" % (2 * a, a * a))
        if how == "calc":
            k = R.choice(["diff", "sq"])
            if k == "diff":
                a = R.randint(51, 99)
                b = R.choice([x for x in range(a - 10, a) if x > 0])
                return N("인수분해 공식을 이용하여 <b>%d² − %d²</b>을 계산하면?" % (a, b), a * a - b * b, [(a - b) ** 2, a - b, (a + b) * 2, a * a - b * b + 10], "(%d + %d)(%d − %d) = %d × %d = <b>%s</b>" % (a, b, a, b, a + b, a - b, num(a * a - b * b)))
            a = R.randint(2, 9)
            b = 10 - a
            return N("인수분해 공식을 이용하여 <b>%d² + 2 × %d × %d + %d²</b>을 계산하면?" % (a * 10 + 1, a * 10 + 1, b * 10 - 1, b * 10 - 1), 10000, [9999, 1000, 10001, 9801], "(%d + %d)² = 100² = <b>10,000</b>" % (a * 10 + 1, b * 10 - 1), f=num)
        if how == "common2":
            p, q = R.choice([-5, -3, -2, 2, 3, 4]), R.choice([-4, -3, -1, 1, 2, 5])
            ok = "(%s)(%s)" % (P1([1, p]), P1([1, q], "y").replace("x", "y"))
            return M("<b>xy %s %s %s</b>를 인수분해하면?" % ("+" if q > 0 else "−", (str(abs(q)) if abs(q) != 1 else "") + "x", ("+ %dy + %d" % (p, p * q) if p > 0 else "− %dy %s %d" % (-p, "+" if p * q > 0 else "−", abs(p * q)))),
                     "(%s)(%s)" % (P1([1, p]), "y %s %d" % ("+" if q > 0 else "−", abs(q))),
                     ["(%s)(%s)" % (P1([1, q]), "y %s %d" % ("+" if p > 0 else "−", abs(p))), "(%s)(%s)" % (P1([1, -p]), "y %s %d" % ("−" if q > 0 else "+", abs(q))), "(%s)(%s)" % (P1([1, -p]), "y %s %d" % ("+" if q > 0 else "−", abs(q)))],
                     "x로 묶을 수 있는 항과 y로 묶을 수 있는 항을 짝지어요. <b>(%s)(%s)</b>" % (P1([1, p]), "y %s %d" % ("+" if q > 0 else "−", abs(q))))
        p, q = R.choice([-6, -5, -4, -3, -2, 1, 2, 3, 4, 5]), R.choice([-5, -3, -2, -1, 2, 3, 4, 6])
        if p == q:
            return None
        ok = P1([1, p])
        return M("다음 중 <b>%s</b>의 인수인 것은?" % P1([1, p + q, p * q]), ok, [P1([1, -p]), P1([1, -q]), P1([1, p * q]) if p * q not in (p, q) else P1([1, p + q])],
                 "%s = (%s)(%s). <b>%s</b>" % (P1([1, p + q, p * q]), P1([1, p]), P1([1, q]), ok))
    return mk


# ------------------------------------------------------------------ 이차방정식
def roots_str(a, b):
    a, b = Fr(a), Fr(b)
    if a == b:
        return "x = %s (중근)" % neg(a)
    lo, hi = sorted([a, b])
    return "x = %s 또는 x = %s" % (neg(lo), neg(hi))


def q_solve(kinds=("fact", "sqrt", "formula", "double", "other")):
    def mk():
        how = R.choice(kinds)
        if how == "fact":
            p, q = R.randint(-7, 7), R.randint(-7, 7)
            if p == q or p == 0 and q == 0:
                return None
            a = R.choice([1, 1, 2])
            eq = "%s = 0" % P1([a, -a * (p + q), a * p * q])
            ok = roots_str(p, q)
            return M("이차방정식 <b>%s</b>을 풀면?" % eq, ok, [roots_str(-p, -q), roots_str(p, -q), roots_str(-p, q), roots_str(p * q, 1) if p * q != 1 else roots_str(0, 1)],
                     "(x %s %d)(x %s %d) = 0. <b>%s</b>" % ("−" if p >= 0 else "+", abs(p), "−" if q >= 0 else "+", abs(q), ok))
        if how == "sqrt":
            a = R.randint(-5, 5)
            k = R.choice([2, 3, 5, 6, 7, 4, 9, 16])
            s = math.isqrt(k)
            if s * s == k:
                ok = roots_str(a - s, a + s)
                bad = [roots_str(-a - s, -a + s), "x = %s" % neg(a + s), roots_str(a - k, a + k)]
            else:
                ok = "x = %s ± √%d" % (neg(a), k) if a else "x = ±√%d" % k
                bad = ["x = %s ± √%d" % (neg(-a), k) if a else "x = √%d" % k, "x = %s ± %d" % (neg(a), k), "x = %s + √%d" % (neg(a), k) if a else "x = −√%d" % k]
            eq = "(x %s %d)² = %d" % ("−" if a >= 0 else "+", abs(a), k) if a else "x² = %d" % k
            return M("이차방정식 <b>%s</b>을 풀면?" % eq, ok, bad, "x %s %d = ±√%d. <b>%s</b>" % ("−" if a >= 0 else "+", abs(a), k, ok) if a else "x = ±√%d. <b>%s</b>" % (k, ok))
        if how == "formula":
            a = R.choice([1, 1, 2, 3])
            b = R.randint(-7, 7)
            c = R.randint(-6, 6)
            D = b * b - 4 * a * c
            if D <= 0:
                return None
            s, t = sq_split(D)
            if t == 1:
                return None
            # x = (−b ± s√t) / 2a
            g = math.gcd(math.gcd(abs(b), s), 2 * a)
            nb, ns, den = -b // g, s // g, 2 * a // g
            num_ = ("%s ± %s" % (neg(nb), surd(ns, t))) if nb else ("±" + surd(ns, t))
            ok = "x = " + (fr(num_, den) if den != 1 else num_)
            wn = ("%s ± %s" % (neg(-nb), surd(ns, t))) if nb else ("±" + surd(ns, t))
            bad = ["x = " + (fr(wn, den) if den != 1 else wn), "x = " + (fr(num_, 2 * den) if True else ""), "x = " + (fr("%s ± √%d" % (neg(-b), b * b + 4 * a * c), 2 * a) if b * b + 4 * a * c > 0 else fr("%s ± √%d" % (neg(-b), D + 4), 2 * a))]
            return M("이차방정식 <b>%s = 0</b>을 근의 공식으로 풀면?" % P1([a, b, c]), ok, bad, "x = (−b ± √(b² − 4ac)) ÷ 2a, b² − 4ac = %d. <b>%s</b>" % (D, ok))
        if how == "double":
            a = R.choice([-8, -6, -4, -2, 2, 4, 6, 8, 10])
            k = a * a // 4
            return N("이차방정식 <b>x² %s %dx + k = 0</b>이 중근을 가질 때, 상수 k의 값은?" % ("+" if a > 0 else "−", abs(a)), k, [a * a, abs(a) // 2, -k, a * a // 2], "b² − 4ac = 0 → %d − 4k = 0, k = <b>%d</b>" % (a * a, k))
        p, q = R.randint(-6, 6), R.randint(-6, 6)
        if p == q or p == 0:
            return None
        s = -(p + q)
        return N("이차방정식 <b>x² %s ax %s %d = 0</b>의 한 근이 %s일 때, 다른 한 근은? (a는 상수)" % ("+", "+" if p * q >= 0 else "−", abs(p * q), neg(p)), q, [-q, p, p * q, -p], "x = %s를 대입해 a를 구하고 다시 풀면 두 근은 %s, %s. <b>%s</b>" % (neg(p), neg(p), neg(q), neg(q)))
    return mk


def q_count(kinds=("disc", "make")):
    def mk():
        how = R.choice(kinds)
        if how == "disc":
            a, b, c = R.choice([1, 2, 3]), R.randint(-6, 6), R.randint(-5, 5)
            D = b * b - 4 * a * c
            n = 2 if D > 0 else (1 if D == 0 else 0)
            ok = {2: "서로 다른 두 근", 1: "중근", 0: "근이 없어요"}[n]
            return M("이차방정식 <b>%s = 0</b>의 근은?" % P1([a, b, c]), ok, [x for x in ("서로 다른 두 근", "중근", "근이 없어요", "세 개의 근") if x != ok], "b² − 4ac = %s이므로 <b>%s</b>" % (neg(D), ok))
        p, q = R.randint(-6, 6), R.randint(-6, 6)
        if p == q:
            return None
        ok = "%s = 0" % P1([1, -(p + q), p * q])
        return M("두 근이 %s, %s이고 x²의 계수가 1인 이차방정식은?" % (neg(p), neg(q)), ok, ["%s = 0" % P1([1, p + q, p * q]), "%s = 0" % P1([1, -(p + q), -p * q]), "%s = 0" % P1([1, p * q, p + q])], "(x − %s)(x − %s) = 0을 전개해요. <b>%s</b>" % (par(p), par(q), ok))
    return mk


def q_word(kinds=("num", "rect", "ball", "path", "poly", "consec")):
    def mk():
        how = R.choice(kinds)
        if how == "num":
            n = R.randint(3, 15)
            k = R.choice(["sq", "sum"])
            if k == "sq":
                return N("어떤 자연수를 제곱한 수는 그 수의 %d배보다 %d만큼 커요. 이 자연수는?" % (n - 1, n), n, [n - 1, n + 1, n * n, 1], "x² = %dx + %d → (x − %d)(x + 1) = 0, x는 자연수이므로 <b>%d</b>" % (n - 1, n, n, n))
            return N("연속하는 두 자연수의 제곱의 합이 %d일 때, 두 수 중 작은 수는?" % (n * n + (n + 1) ** 2), n, [n + 1, n - 1, 2 * n, Fr(n * n + (n + 1) ** 2, 2) if False else n * 2 + 1], "x² + (x + 1)² = %d → x = <b>%d</b>" % (n * n + (n + 1) ** 2, n))
        if how == "consec":
            n = R.randint(2, 24)
            k = R.choice(["짝수", "홀수"])
            x = 2 * n if k == "짝수" else 2 * n + 1
            return N("연속하는 두 %s의 곱이 %d일 때, 두 수의 합은?" % (k, x * (x + 2)), 2 * x + 2, [x, x + 2, 2 * x, 2 * x + 4], "x(x + 2) = %d → x = %d. %d + %d = <b>%d</b>" % (x * (x + 2), x, x, x + 2, 2 * x + 2))
        if how == "rect":
            w = R.randint(3, 12)
            d = R.randint(2, 6)
            A = w * (w + d)
            return N("가로의 길이가 세로의 길이보다 %d cm 긴 직사각형의 넓이가 %d cm²일 때, 세로의 길이는?" % (d, A), w, [w + d, Fr(A, 2), w - 1, d], "x(x + %d) = %d → x = <b>%d cm</b>" % (d, A, w), f=lambda v: "%s cm" % neg(v))
        if how == "ball":
            v = R.choice([20, 30, 40])
            h = R.choice([t * (v - 5 * t) for t in range(1, v // 5) if t * (v - 5 * t) > 0])
            ts = sorted(t for t in range(1, v // 5 + 1) if t * (v - 5 * t) == h)
            ok = "%d초 후" % ts[0] if len(ts) == 1 else "%d초 후와 %d초 후" % (ts[0], ts[1])
            return M("지면에서 초속 %d m로 위로 쏘아 올린 공의 t초 후 높이가 (%dt − 5t²) m예요. 공의 높이가 %d m가 되는 것은 언제일까요?" % (v, v, h), ok, ["%d초 후" % (ts[-1] + 1), "%d초 후" % (v // 5), "%d초 후와 %d초 후" % (ts[0] + 1, v // 5 - ts[0] - 1) if len(ts) > 1 else "%d초 후와 %d초 후" % (ts[0], ts[0] + 1)],
                     "%dt − 5t² = %d → t² − %dt + %d = 0. <b>%s</b>" % (v, h, v // 5, h // 5, ok))
        if how == "path":
            W, H = R.choice([(20, 15), (30, 20), (25, 20), (16, 12), (24, 18)])
            x = R.randint(1, 4)
            A = (W - x) * (H - x)
            return N("가로 %d m, 세로 %d m인 직사각형 땅에 폭이 같은 길을 가로, 세로로 하나씩 내고 남은 땅의 넓이가 %d m²가 되게 하려고 해요. 길의 폭은?" % (W, H, A), x, [x + 1, W - H, Fr(W * H - A, W + H), 2 * x], "(%d − x)(%d − x) = %d → x = <b>%d m</b>" % (W, H, A, x), f=lambda v: "%s m" % neg(v))
        n = R.randint(5, 20)
        dgn = n * (n - 3) // 2
        return N("대각선의 개수가 %d개인 다각형은 몇 각형일까요?" % dgn, n, [n - 1, n + 1, dgn // 2, n + 3], "n(n − 3) ÷ 2 = %d → n = <b>%d</b>" % (dgn, n), f=lambda v: "%s각형" % neg(v))
    return mk


# ------------------------------------------------------------------ 이차함수
def vtx_form(a, p, q):
    s = "y = "
    a = Fr(a)
    c = "" if a == 1 else ("−" if a == -1 else neg(a))
    if p == 0:
        s += c + "x²"
    else:
        s += c + "(x %s %s)²" % ("−" if p > 0 else "+", neg(abs(p)))
    if q:
        s += " %s %s" % ("+" if q > 0 else "−", neg(abs(q)))
    return s


AS = [Fr(1, 3), Fr(1, 2), 1, 2, 3, Fr(-1, 2), -1, -2, -3, Fr(-1, 3), Fr(3, 2), Fr(-3, 2)]


def qf_basic(kinds=("is", "val", "width", "prop", "pt")):
    def mk():
        how = R.choice(kinds)
        if how == "is":
            a, b, c = R.choice([-3, -2, 1, 2, 3]), R.randint(-5, 5), R.randint(-5, 5)
            ok = "y = " + P1([a, b, c])
            bad = ["y = " + P1([b or 2, c or 1]), "y = %s/x²" % neg(a), "y = x(x + %d) − x²" % abs(b or 3), "y = 2x + 1"]
            return M("다음 중 y가 x에 대한 <b>이차함수</b>인 것은?", ok, bad, "y = ax² + bx + c (a ≠ 0) 꼴이에요. <b>%s</b>" % ok)
        a = R.choice(AS)
        if how == "val":
            x = R.choice([-6, -4, -3, -2, 2, 3, 4, 6])
            v = a * x * x
            if Fr(v).denominator != 1:
                return None
            return N("이차함수 <b>%s</b>에서 x = %s일 때 y의 값은?" % (vtx_form(a, 0, 0), neg(x)), v, [a * x, -v, a * x * 2, v + 1], "%s × (%s)² = <b>%s</b>" % (neg(a), neg(x), neg(v)))
        if how == "width":
            cand = R.sample(AS, 4)
            if len({abs(c) for c in cand}) < 4:
                return None
            k = R.choice(["wide", "narrow"])
            ok = min(cand, key=abs) if k == "wide" else max(cand, key=abs)
            return M("이차함수 %s 중 그래프의 폭이 가장 %s 것은?" % (", ".join(vtx_form(c, 0, 0) for c in cand), "넓은" if k == "wide" else "좁은"), vtx_form(ok, 0, 0), [vtx_form(c, 0, 0) for c in cand if c != ok],
                     "a의 절댓값이 %s수록 폭이 %s요. <b>%s</b>" % ("작을" if k == "wide" else "클", "넓어" if k == "wide" else "좁아", vtx_form(ok, 0, 0)))
        if how == "pt":
            x, y = R.choice([-3, -2, -1, 1, 2, 3]), R.choice([-18, -12, -8, -6, -4, -2, 2, 3, 4, 6, 8, 12, 18])
            a = Fr(y, x * x)
            return N("이차함수 y = ax²의 그래프가 점 (%s, %s)를 지날 때, 상수 a의 값은?" % (neg(x), neg(y)), a, [Fr(y, x), Fr(x * x, y), -a, y * x * x], "%s = a × %d → a = <b>%s</b>" % (neg(y), x * x, neg(a)))
        F_ = [("y = ax²의 그래프에서 a &gt; 0이면?", "아래로 볼록해요", ["위로 볼록해요", "직선이에요", "x축에 평행해요"], "<b>아래로 볼록</b>해요."),
              ("y = ax²의 그래프에서 a &lt; 0이면?", "위로 볼록해요", ["아래로 볼록해요", "원점을 지나지 않아요", "y축에 대칭이 아니에요"], "<b>위로 볼록</b>해요."),
              ("y = ax²의 그래프의 축은?", "y축 (x = 0)", ["x축 (y = 0)", "y = x", "x = a"], "<b>y축</b>에 대칭이에요."),
              ("y = 2x²과 y = −2x²의 그래프의 관계는?", "x축에 대하여 대칭이에요", ["y축에 대하여 대칭이에요", "일치해요", "원점에서만 만나지 않아요"], "a의 부호만 다르면 <b>x축에 대하여 대칭</b>이에요."),
              ("y = ax²의 그래프의 꼭짓점은?", "원점 (0, 0)", ["(a, 0)", "(0, a)", "(1, a)"], "<b>원점</b>이에요.")]
        return M(*R.choice(F_))
    return mk


def qf_shift(kinds=("vtx", "axis", "move", "dir")):
    def mk():
        how = R.choice(kinds)
        a = R.choice(AS)
        p, q = R.randint(-5, 5), R.randint(-6, 6)
        if how == "vtx":
            ok = "(%s, %s)" % (neg(p), neg(q))
            return M("이차함수 <b>%s</b>의 그래프의 꼭짓점의 좌표는?" % vtx_form(a, p, q), ok, ["(%s, %s)" % (neg(-p), neg(q)), "(%s, %s)" % (neg(p), neg(-q)), "(%s, %s)" % (neg(q), neg(p)) if p != q else "(%s, %s)" % (neg(-p), neg(-q))],
                     "y = a(x − p)² + q의 꼭짓점은 (p, q)예요. <b>%s</b>" % ok)
        if how == "axis":
            if p == 0:
                return None
            return M("이차함수 <b>%s</b>의 그래프의 축의 방정식은?" % vtx_form(a, p, q), "x = %s" % neg(p), ["x = %s" % neg(-p), "y = %s" % neg(q), "x = %s" % neg(q) if q != p else "y = %s" % neg(p)], "축은 꼭짓점을 지나는 세로선이에요. <b>x = %s</b>" % neg(p))
        if how == "move":
            ok = vtx_form(a, p, q)
            return M("이차함수 <b>%s</b>의 그래프를 x축의 방향으로 %s만큼, y축의 방향으로 %s만큼 평행이동한 그래프의 식은?" % (vtx_form(a, 0, 0), neg(p), neg(q)), ok, [vtx_form(a, -p, q), vtx_form(a, p, -q), vtx_form(a, q, p) if p != q else vtx_form(-a, p, q), vtx_form(-a, p, q)],
                     "x 대신 x − (%s), 상수항에 %s를 더해요. <b>%s</b>" % (neg(p), neg(q), ok))
        x0 = p + R.choice([-2, -1, 1, 2])
        y0 = a * (x0 - p) ** 2 + q
        if Fr(y0).denominator != 1:
            return None
        k = R.choice(["up", "x"])
        if k == "up":
            ok = "x &gt; %s" % neg(p) if a > 0 else "x &lt; %s" % neg(p)
            bad = "x &lt; %s" % neg(p) if a > 0 else "x &gt; %s" % neg(p)
            return M("이차함수 <b>%s</b>의 그래프에서 x의 값이 증가할 때 y의 값도 증가하는 x의 값의 범위는?" % vtx_form(a, p, q), ok, [bad, "x &gt; %s" % neg(q) if q != p else "x &gt; %s" % neg(-p), "x &lt; %s" % neg(-p) if p else "x &lt; 1"],
                     "%s 볼록이고 축이 x = %s예요. <b>%s</b>" % ("아래로" if a > 0 else "위로", neg(p), ok))
        return N("이차함수 <b>%s</b>에서 x = %s일 때 y의 값은?" % (vtx_form(a, p, q), neg(x0)), y0, [a * (x0 + p) ** 2 + q, a * (x0 - p) ** 2 - q, a * (x0 - p) + q, y0 + 1], "%s × (%s)² + (%s) = <b>%s</b>" % (neg(a), neg(x0 - p), neg(q), neg(y0)))
    return mk


def qf_graph(kinds=("read", "sign")):
    def mk():
        how = R.choice(kinds)
        a = R.choice([1, -1, 2, -2, Fr(1, 2), Fr(-1, 2)])
        p, q = R.randint(-3, 3), R.randint(-4, 4)
        f = lambda x, a=a, p=p, q=q: float(a) * (x - p) ** 2 + q
        g = kurve([(f, BLUE, "")], (-5, 5, 1), (-5, 5, 1), pts=[(p, q, "")], label="이차함수의 그래프", W=380, H=360)
        g = g.replace("<svg ", "<svg data-pf='lg' ", 1)
        if how == "read":
            ok = vtx_form(a, p, q)
            return M("그림은 x²의 계수가 %s인 이차함수의 그래프이고, 빨간 점이 꼭짓점이에요. 이 이차함수의 식은?%s" % (neg(a), fig(g)), ok, [vtx_form(a, -p, q), vtx_form(a, p, -q), vtx_form(-a, p, q), vtx_form(a, q, p) if p != q else vtx_form(a, p, q + 1)],
                     "꼭짓점 (%s, %s)이고 a = %s예요. <b>%s</b>" % (neg(p), neg(q), neg(a), ok))
        ok = ("a &gt; 0" if a > 0 else "a &lt; 0") + ", " + ("q &gt; 0" if q > 0 else ("q &lt; 0" if q < 0 else "q = 0"))
        if q == 0 or p == 0:
            return None
        bad = [("a &lt; 0" if a > 0 else "a &gt; 0") + ", " + ("q &gt; 0" if q > 0 else "q &lt; 0"), ("a &gt; 0" if a > 0 else "a &lt; 0") + ", " + ("q &lt; 0" if q > 0 else "q &gt; 0"), ("a &lt; 0" if a > 0 else "a &gt; 0") + ", " + ("q &lt; 0" if q > 0 else "q &gt; 0")]
        return M("이차함수 y = a(x − p)² + q의 그래프가 그림과 같을 때, a와 q의 부호로 옳은 것은?%s" % fig(g), ok, bad, "%s 볼록이고 꼭짓점이 x축 %s쪽에 있어요. <b>%s</b>" % ("아래로" if a > 0 else "위로", "위" if q > 0 else "아래", ok))
    return mk


def to_vtx(a, b, c):
    p = Fr(-b, 2 * a)
    q = c - Fr(b * b, 4 * a)
    return p, q


def qg_std(kinds=("vtx", "yint", "xint", "conv", "find")):
    def mk():
        how = R.choice(kinds)
        a = R.choice([1, -1, 2, -2, 3])
        p, q = R.randint(-4, 4), R.randint(-8, 8)
        b, c = -2 * a * p, a * p * p + q
        std = "y = " + P1([a, b, c])
        if how == "vtx":
            ok = "(%s, %s)" % (neg(p), neg(q))
            return M("이차함수 <b>%s</b>의 그래프의 꼭짓점의 좌표는?" % std, ok, ["(%s, %s)" % (neg(-p), neg(q)), "(%s, %s)" % (neg(p), neg(c)), "(%s, %s)" % (neg(-p), neg(-q)), "(%s, %s)" % (neg(b), neg(c))],
                     "%s로 고쳐요. <b>%s</b>" % (vtx_form(a, p, q), ok))
        if how == "conv":
            ok = vtx_form(a, p, q)
            return M("이차함수 <b>%s</b>를 y = a(x − p)² + q 꼴로 나타내면?" % std, ok, [vtx_form(a, -p, q), vtx_form(a, p, c), vtx_form(a, p, -q), vtx_form(1, p, q) if a != 1 else vtx_form(2, p, q)],
                     "x²의 계수로 묶고 완전제곱식을 만들어요. <b>%s</b>" % ok)
        if how == "yint":
            return N("이차함수 <b>%s</b>의 그래프가 y축과 만나는 점의 y좌표는?" % std, c, [q, b, -c, a], "x = 0을 대입해요. <b>%s</b>" % neg(c))
        if how == "xint":
            r1, r2 = R.sample(range(-5, 6), 2)
            a = R.choice([1, -1])
            b, c = -a * (r1 + r2), a * r1 * r2
            std = "y = " + P1([a, b, c])
            ok = "%s, %s" % (neg(min(r1, r2)), neg(max(r1, r2)))
            return M("이차함수 <b>%s</b>의 그래프가 x축과 만나는 점의 x좌표는?" % std, ok, ["%s, %s" % (neg(-max(r1, r2)), neg(-min(r1, r2))), "%s, %s" % (neg(min(r1, r2)), neg(-max(r1, r2))), "%s" % neg(c)],
                     "y = 0으로 놓고 인수분해해요. <b>%s</b>" % ok)
        x0 = p + R.choice([-2, -1, 1, 2])
        y0 = a * (x0 - p) ** 2 + q
        ok = vtx_form(a, p, q)
        return M("꼭짓점의 좌표가 (%s, %s)이고 점 (%s, %s)를 지나는 포물선을 그래프로 하는 이차함수의 식은?" % (neg(p), neg(q), neg(x0), neg(y0)), ok, [vtx_form(-a, p, q), vtx_form(a, -p, q), vtx_form(a + 1 if a != -1 else 2, p, q), vtx_form(a, p, -q)],
                 "y = a(x − %s)² + %s에 대입하면 a = %s. <b>%s</b>" % (par(p), par(q), neg(a), ok))
    return mk


def qg_coef(kinds=("sign", "maxmin")):
    def mk():
        how = R.choice(kinds)
        if how == "maxmin":
            a = R.choice([1, -1, 2, -2, 3, -3])
            p, q = R.randint(-4, 4), R.randint(-8, 8)
            b, c = -2 * a * p, a * p * p + q
            k = R.choice(["inc", "dec"])
            up = (a > 0) == (k == "inc")
            ok = "x &gt; %s" % neg(p) if up else "x &lt; %s" % neg(p)
            bad = ["x &lt; %s" % neg(p) if up else "x &gt; %s" % neg(p), "x &gt; %s" % neg(-p) if p else "x &gt; 1", "x &lt; %s" % neg(q) if q != p else "x &lt; %s" % neg(p + 1)]
            return M("이차함수 <b>y = %s</b>의 그래프에서 x의 값이 증가할 때 y의 값이 <b>%s</b>하는 x의 값의 범위는?" % (P1([a, b, c]), "증가" if k == "inc" else "감소"), ok, bad,
                     "%s로 고치면 축이 x = %s이고 %s 볼록이에요. <b>%s</b>" % (vtx_form(a, p, q), neg(p), "아래로" if a > 0 else "위로", ok))
        a = R.choice([1, -1, Fr(1, 2), Fr(-1, 2), 2, -2])
        p, q = R.choice([-2, -1, 1, 2]), R.randint(-4, 4)
        b = -2 * a * p
        c = a * p * p + q
        if c == 0 or abs(c) > 4:
            return None
        f = lambda x, a=a, p=p, q=q: float(a) * (x - p) ** 2 + q
        g = kurve([(f, BLUE, "")], (-5, 5, 1), (-5, 5, 1), label="이차함수 y = ax² + bx + c의 그래프", W=380, H=360).replace("<svg ", "<svg data-pf='lg' ", 1)
        sa, sb, sc = (">" if a > 0 else "<"), (">" if b > 0 else "<"), (">" if c > 0 else "<")
        T = {">": "&gt;", "<": "&lt;"}
        ok = "a %s 0, b %s 0, c %s 0" % (T[sa], T[sb], T[sc])
        flip = {">": "<", "<": ">"}
        bad = ["a %s 0, b %s 0, c %s 0" % (T[sa], T[flip[sb]], T[sc]), "a %s 0, b %s 0, c %s 0" % (T[flip[sa]], T[sb], T[sc]), "a %s 0, b %s 0, c %s 0" % (T[sa], T[sb], T[flip[sc]])]
        return M("이차함수 y = ax² + bx + c의 그래프가 그림과 같을 때, a, b, c의 부호는?%s" % fig(g), ok, bad,
                 "%s 볼록 → a %s 0, 축이 y축의 %s쪽 → a, b는 %s 부호, y절편 → c %s 0. <b>%s</b>" % ("아래로" if a > 0 else "위로", T[sa], "오른" if p > 0 else "왼", "다른" if p > 0 else "같은", T[sc], ok))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "sqrt":
        return unit(G, "square-roots", 1, "[9수01-07]", "제곱근의 뜻과 성질을 알고, 제곱근의 대소 관계를 판단할 수 있다.",
                    "제곱근의 뜻과 성질, 대소 관계", "제곱근",
                    "중학교 3학년 수학 제곱근 문제: 제곱근의 뜻, 양의 제곱근과 음의 제곱근, √(a²) = |a|, √(ax)가 자연수가 되는 조건, 제곱근의 대소 관계, 부등식을 만족하는 자연수까지 100문제와 정답·해설.",
                    "√(a²) = |a|", "양수 a의 제곱근은 ±√a, 0의 제곱근은 0이에요.",
                    ["x² = a일 때 x를 a의 <b>제곱근</b>이라고 해요. 양수의 제곱근은 양수와 음수 두 개예요(±√a).",
                     "(√a)² = (−√a)² = a, √(a²) = a (a ≥ 0), √(a²) = −a (a &lt; 0)",
                     "a, b가 양수일 때 a &lt; b이면 √a &lt; √b예요. 정수와 비교할 때는 정수를 √ 꼴로 바꾸어요.",
                     "√(ax)가 자연수가 되려면 ax가 제곱수가 되어야 해요. 소인수분해해서 지수를 짝수로 만들어요."],
                    [("16의 제곱근", ["4² = (−4)² = 16"], "±4"), ("√(12x)가 자연수", ["12 = 2² × 3"], "x = 3")],
                    [("16의 제곱근을 4라고만 한다", "음수 −4도 제곱하면 16이에요."),
                     ("√((−3)²) = −3이라고 한다", "√ 값은 항상 0 이상이에요. 3이에요."),
                     ("음수의 대소 비교에서 −√5 &gt; −2라고 한다", "−√5 &lt; −√4 = −2예요.")],
                    [("√ 기호는 어떻게 읽나요?", "√a는 '제곱근 a' 또는 '루트 a'라고 읽어요."),
                     ("음수의 제곱근은 있나요?", "제곱해서 음수가 되는 실수는 없으므로 음수의 제곱근은 실수 범위에서 없어요.")],
                    [("제곱근의 뜻", [(s_basic(("roots", "sqrt")), 20)]),
                     ("제곱근의 성질", [(s_basic(("square", "abs")), 20)]),
                     ("자연수가 되는 조건", [(s_basic(("nat",)), 14), (s_basic(("sqrt",)), 6)]),
                     ("제곱근의 대소 관계", [(s_compare(("cmp", "between")), 20)]),
                     ("부등식과 제곱근", [(s_compare(("count",)), 10), (s_compare(("between",)), 10)])], 82901)
    if which == "real":
        return unit(G, "irrational-and-real-numbers", 2, "[9수01-08] [9수01-09]", "무리수의 개념을 이해한다. 실수의 대소 관계를 판단할 수 있다.",
                    "무리수와 실수, 실수의 대소 관계", "무리수와 실수",
                    "중학교 3학년 수학 무리수와 실수 문제: 무리수 찾기, 유리수와 무리수의 구분, 실수와 수직선, 직사각형의 대각선으로 무리수를 수직선에 나타내기, 정수 부분과 소수 부분, 실수의 대소 비교까지 100문제와 정답·해설.",
                    "순환하지 않는 무한소수 = 무리수", "유리수와 무리수를 합쳐 실수라고 해요.",
                    ["소수로 나타내면 <b>순환하지 않는 무한소수</b>가 되는 수를 <b>무리수</b>라고 해요. √2, π 등이 있어요.",
                     "유리수와 무리수를 통틀어 <b>실수</b>라 하고, 모든 실수는 수직선 위의 점에 대응해요.",
                     "√2는 한 변이 1인 정사각형의 대각선의 길이로 수직선에 나타낼 수 있어요.",
                     "두 실수 a, b의 대소는 a − b의 부호로 비교해요. √n의 정수 부분은 n보다 작은 가장 큰 제곱수로 찾아요."],
                    [("√9, √7, 0.3̇ 중 무리수", ["√9 = 3", "0.3̇ = 1/3"], "√7"), ("√10의 정수 부분", ["3² &lt; 10 &lt; 4²"], "3")],
                    [("근호가 있으면 모두 무리수라고 한다", "√4 = 2처럼 유리수도 있어요."),
                     ("√5의 소수 부분을 0.5라고 한다", "√5 − 2예요."),
                     ("수직선에서 1 + √2의 위치를 1 + 2로 생각한다", "√2 ≈ 1.414예요.")],
                    [("π는 왜 무리수인가요?", "π = 3.14159…로 순환하지 않고 끝없이 이어지기 때문이에요."),
                     ("두 실수 사이에는 몇 개의 실수가 있나요?", "서로 다른 두 실수 사이에는 무수히 많은 실수가 있어요.")],
                    [("무리수 찾기", [(r_irr(("which", "whichnot")), 20)]),
                     ("무리수의 개수와 실수", [(r_irr(("count", "concept")), 20)]),
                     ("수직선과 무리수", [(r_line(("pt",)), 20)]),
                     ("정수 부분과 소수 부분", [(r_line(("int",)), 20)]),
                     ("실수의 대소 관계", [(r_line(("frac", "order")), 20)])], 82902)
    if which == "rad":
        return unit(G, "operations-with-radicals", 3, "[9수01-10]", "근호를 포함한 식의 사칙계산을 할 수 있다.",
                    "근호를 포함한 식의 곱셈·나눗셈·덧셈·뺄셈", "근호의 계산",
                    "중학교 3학년 수학 근호를 포함한 식의 계산 문제: 제곱근의 곱셈과 나눗셈, a√b 꼴로 나타내기, 분모의 유리화, 덧셈과 뺄셈, 분배법칙, 혼합 계산까지 100문제와 정답·해설.",
                    "√a × √b = √(ab)", "덧셈과 뺄셈은 근호 안의 수가 같은 것끼리만 해요.",
                    ["a, b가 양수일 때 √a × √b = √(ab), √a ÷ √b = √(a/b)이에요.",
                     "근호 안의 제곱인수는 밖으로 꺼내요. √12 = √(2² × 3) = 2√3",
                     "분모에 근호가 있으면 분모와 분자에 같은 수를 곱해 <b>분모를 유리화</b>해요.",
                     "m√a + n√a = (m + n)√a. 근호 안의 수가 다르면 먼저 a√b 꼴로 고쳐 봐요."],
                    [("√6 × √3", ["√18 = 3√2"], "3√2"), ("√12 + √27", ["2√3 + 3√3"], "5√3")],
                    [("√2 + √3 = √5라고 한다", "근호 안의 수가 다르면 더할 수 없어요."),
                     ("2√3 × 3√2 = 5√6이라고 한다", "계수끼리 곱해요. 6√6"),
                     ("분모의 유리화에서 분자에는 곱하지 않는다", "분모와 분자에 같은 수를 곱해요.")],
                    [("√8은 왜 2√2인가요?", "8 = 2² × 2이므로 √8 = √2² × √2 = 2√2예요."),
                     ("계산 순서는?", "괄호 → 곱셈·나눗셈 → 덧셈·뺄셈 순서로 계산해요.")],
                    [("곱셈과 나눗셈", [(d_muldiv(("mul", "div")), 20)]),
                     ("근호 안의 수 정리", [(d_muldiv(("out", "in")), 20)]),
                     ("분모의 유리화", [(d_muldiv(("rat",)), 20)]),
                     ("덧셈과 뺄셈", [(d_addsub(("like", "simp")), 20)]),
                     ("혼합 계산", [(d_addsub(("dist", "mix")), 20)])], 82903)
    if which == "mulp":
        return unit(G, "multiplying-polynomials", 4, "[9수02-19]", "다항식의 곱셈과 인수분해를 할 수 있다.",
                    "다항식의 곱셈과 곱셈 공식", "곱셈 공식",
                    "중학교 3학년 수학 다항식의 곱셈 문제: (a + b)², (a − b)², (a + b)(a − b), (x + a)(x + b), (ax + b)(cx + d) 전개, 곱셈 공식을 이용한 수의 계산, 식의 값, 근호가 있는 식까지 100문제와 정답·해설.",
                    "(a + b)² = a² + 2ab + b²", "(a + b)(a − b) = a² − b²",
                    ["(a + b)² = a² + 2ab + b², (a − b)² = a² − 2ab + b²",
                     "(a + b)(a − b) = a² − b²",
                     "(x + a)(x + b) = x² + (a + b)x + ab, (ax + b)(cx + d) = acx² + (ad + bc)x + bd",
                     "곱셈 공식은 102² = (100 + 2)², 99 × 101 = (100 − 1)(100 + 1)처럼 수의 계산에도 써요."],
                    [("(x + 3)²", ["x² + 6x + 9"], "x² + 6x + 9"), ("98 × 102", ["100² − 2²"], "9,996")],
                    [("(a + b)² = a² + b²", "가운데 2ab를 빠뜨리면 안 돼요."),
                     ("(x − 3)² = x² − 9", "x² − 6x + 9예요."),
                     ("(x + 2)(x − 5)의 상수항을 −3으로 쓴다", "상수항은 곱 2 × (−5) = −10이에요.")],
                    [("곱셈 공식을 외우는 요령은?", "넓이 그림(정사각형을 네 조각으로 나누기)으로 이해하면 오래 기억해요."),
                     ("a² + b²의 값은 어떻게 구하나요?", "(a + b)² − 2ab 또는 (a − b)² + 2ab로 구해요.")],
                    [("완전제곱식의 전개", [(m_formula(("sq+", "sq-")), 20)]),
                     ("합차 공식", [(m_formula(("conj",)), 12), (m_formula(("sq-",)), 8)]),
                     ("일차식의 곱", [(m_formula(("xab", "axb")), 20)]),
                     ("곱셈 공식의 활용", [(m_apply(("calc", "box", "val")), 20)]),
                     ("근호가 있는 식", [(m_apply(("surd",)), 20)])], 82904)
    if which == "fact":
        return unit(G, "factoring", 5, "[9수02-19]", "다항식의 곱셈과 인수분해를 할 수 있다.",
                    "인수분해와 인수분해 공식", "인수분해",
                    "중학교 3학년 수학 인수분해 문제: 공통인수로 묶기, 완전제곱식, a² − b², x² + (a + b)x + ab, acx² + (ad + bc)x + bd, 완전제곱식이 되는 조건, 수의 계산까지 100문제와 정답·해설.",
                    "인수분해는 곱셈 공식의 거꾸로", "먼저 공통인수가 있는지 확인해요.",
                    ["하나의 다항식을 두 개 이상의 다항식의 곱으로 나타내는 것을 <b>인수분해</b>라고 해요.",
                     "a² ± 2ab + b² = (a ± b)², a² − b² = (a + b)(a − b)",
                     "x² + px + q는 곱이 q, 합이 p인 두 수 a, b를 찾아 (x + a)(x + b)로 나타내요.",
                     "x² + ax + □가 완전제곱식이 되려면 □ = (a/2)²이에요."],
                    [("x² − 5x + 6", ["곱 6, 합 −5 → −2, −3"], "(x − 2)(x − 3)"), ("4x² − 9", ["(2x)² − 3²"], "(2x + 3)(2x − 3)")],
                    [("x² + 5x + 6을 (x − 2)(x − 3)으로 한다", "합이 +5이므로 (x + 2)(x + 3)이에요."),
                     ("x² + 9를 (x + 3)(x − 3)으로 한다", "합차 공식은 빼기(−)일 때만 써요."),
                     ("공통인수를 일부만 묶는다", "2x² + 4x = 2x(x + 2)처럼 남김없이 묶어요.")],
                    [("인수분해가 끝났는지 어떻게 아나요?", "각 인수를 더 이상 인수분해할 수 없을 때까지 해요."),
                     ("검산 방법은?", "인수분해한 식을 다시 전개해서 처음 식과 같은지 확인해요.")],
                    [("공통인수와 완전제곱식", [(f_factor(("common", "perfect")), 20)]),
                     ("합차 공식", [(f_factor(("diff",)), 20)]),
                     ("x² + (a + b)x + ab", [(f_factor(("trin",)), 20)]),
                     ("acx² + (ad + bc)x + bd", [(f_factor(("atrin",)), 20)]),
                     ("인수분해의 활용", [(f_apply(), 20)])], 82905)
    if which == "qeq":
        return unit(G, "quadratic-equations", 6, "[9수02-20]", "이차방정식을 풀 수 있고, 이를 활용하여 문제를 해결할 수 있다.",
                    "이차방정식의 풀이: 인수분해, 제곱근, 근의 공식", "이차방정식",
                    "중학교 3학년 수학 이차방정식 문제: 인수분해를 이용한 풀이, 제곱근을 이용한 풀이, 근의 공식, 중근이 되는 조건, 근의 개수, 두 근으로 이차방정식 만들기까지 100문제와 정답·해설.",
                    "AB = 0이면 A = 0 또는 B = 0", "근의 공식 x = (−b ± √(b² − 4ac)) ÷ 2a",
                    ["ax² + bx + c = 0 (a ≠ 0) 꼴의 방정식을 <b>이차방정식</b>이라고 해요.",
                     "인수분해되면 AB = 0 → A = 0 또는 B = 0으로 풀어요. (x − a)² = k이면 x = a ± √k예요.",
                     "<b>근의 공식</b>: x = (−b ± √(b² − 4ac)) ÷ 2a",
                     "b² − 4ac &gt; 0이면 서로 다른 두 근, = 0이면 중근, &lt; 0이면 근이 없어요."],
                    [("x² − x − 6 = 0", ["(x − 3)(x + 2) = 0"], "x = −2 또는 x = 3"), ("x² + 2x − 1 = 0", ["x = (−2 ± √8) ÷ 2"], "x = −1 ± √2")],
                    [("x² = 9의 해를 x = 3만 쓴다", "x = ±3이에요."),
                     ("(x − 2)(x + 5) = 0의 해를 x = −2, 5로 쓴다", "부호를 바꾸어 x = 2 또는 x = −5예요."),
                     ("근의 공식에서 −b의 부호를 놓친다", "b가 음수이면 −b는 양수예요.")],
                    [("x² = 2x는 양변을 x로 나누어도 되나요?", "x = 0이 사라지므로 안 돼요. x² − 2x = 0 → x(x − 2) = 0으로 풀어요."),
                     ("근의 공식은 언제 쓰나요?", "인수분해가 잘 되지 않을 때 써요.")],
                    [("인수분해를 이용한 풀이", [(q_solve(("fact",)), 20)]),
                     ("제곱근을 이용한 풀이", [(q_solve(("sqrt",)), 20)]),
                     ("근의 공식", [(q_solve(("formula",)), 20)]),
                     ("중근과 근의 개수", [(q_solve(("double",)), 8), (q_count(("disc",)), 12)]),
                     ("근과 이차방정식", [(q_solve(("other",)), 10), (q_count(("make",)), 10)])], 82906)
    if which == "qword":
        return unit(G, "quadratic-equation-word-problems", 7, "[9수02-20]", "이차방정식을 풀 수 있고, 이를 활용하여 문제를 해결할 수 있다.",
                    "이차방정식의 활용", "이차방정식의 활용",
                    "중학교 3학년 수학 이차방정식의 활용 문제: 수에 대한 문제, 연속하는 수, 도형의 넓이, 쏘아 올린 물체의 높이, 길의 폭, 다각형의 대각선의 개수를 이차방정식으로 세워 푸는 100문제와 정답·해설.",
                    "구한 해가 문제의 조건에 맞는지 확인", "길이·개수는 양수, 자연수만 답이 돼요.",
                    ["구하는 것을 x로 놓고, 조건에 맞게 이차방정식을 세워요.",
                     "방정식을 풀어 해를 구해요. 해가 두 개 나올 때가 많아요.",
                     "길이, 개수, 시간처럼 음수가 될 수 없는 것은 조건에 맞는 해만 답으로 해요.",
                     "물체의 높이처럼 같은 값이 두 번 나오는 경우(올라갈 때와 내려올 때)도 있어요."],
                    [("연속하는 두 자연수의 곱 56", ["x(x + 1) = 56", "x = 7 또는 −8"], "7, 8"), ("가로가 세로보다 3 긴 넓이 40", ["x(x + 3) = 40"], "세로 5")],
                    [("음수인 해도 답으로 쓴다", "길이나 개수는 양수만 답이에요."),
                     ("두 해 중 하나만 확인한다", "두 해가 모두 조건에 맞을 수도 있어요(공의 높이)."),
                     ("길을 낸 땅의 넓이에서 길의 겹친 부분을 생각하지 않는다", "남은 땅을 붙여 (가로 − x)(세로 − x)로 세우면 편해요.")],
                    [("식을 세우는 요령은?", "문제의 같은 양을 두 가지 방법으로 나타내서 등호로 이어요."),
                     ("답을 확인하는 방법은?", "구한 값을 처음 문장에 넣어서 맞는지 확인해요.")],
                    [("수에 대한 문제", [(q_word(("num", "consec")), 20)]),
                     ("도형의 넓이", [(q_word(("rect", "path")), 20)]),
                     ("쏘아 올린 물체와 다각형", [(q_word(("ball",)), 6), (q_word(("poly",)), 10), (q_word(("consec",)), 4)]),
                     ("여러 가지 활용", [(q_word(("num", "path", "rect")), 20)]),
                     ("섞어서 연습", [(q_word(), 20)])], 82907)
    if which == "qf":
        return unit(G, "quadratic-functions", 8, "[9수02-21] [9수02-22]", "이차함수의 의미를 이해한다. 이차함수의 그래프를 그릴 수 있고, 그 성질을 설명할 수 있다.",
                    "이차함수 y = ax²과 y = a(x − p)² + q의 그래프", "이차함수",
                    "중학교 3학년 수학 이차함수 문제: 이차함수의 뜻, y = ax²의 그래프와 폭, 평행이동, 꼭짓점과 축의 방정식, 증가·감소하는 범위, 그래프를 보고 식과 부호 구하기까지 100문제와 정답·해설.",
                    "y = a(x − p)² + q의 꼭짓점은 (p, q)", "|a|가 클수록 폭이 좁아요.",
                    ["y = ax² + bx + c (a ≠ 0)를 <b>이차함수</b>라 하고, 그 그래프를 <b>포물선</b>이라고 해요.",
                     "y = ax²의 그래프는 원점을 꼭짓점으로 하고 y축에 대칭이에요. a &gt; 0이면 아래로 볼록, a &lt; 0이면 위로 볼록이에요.",
                     "y = a(x − p)² + q는 y = ax²을 x축 방향으로 p, y축 방향으로 q만큼 평행이동한 그래프예요.",
                     "꼭짓점은 (p, q), 축의 방정식은 x = p예요."],
                    [("y = 2(x − 3)² + 1", ["p = 3, q = 1"], "꼭짓점 (3, 1)"), ("y = −(x + 2)² − 4", ["p = −2"], "축 x = −2")],
                    [("y = (x + 3)²의 꼭짓점을 (3, 0)이라고 한다", "x + 3 = x − (−3)이므로 (−3, 0)이에요."),
                     ("a가 음수이면 폭이 좁다고 한다", "폭은 a의 절댓값으로 비교해요."),
                     ("평행이동하면 a도 바뀐다고 한다", "평행이동은 모양(a)을 바꾸지 않아요.")],
                    [("포물선은 실생활 어디에 있나요?", "던진 공의 경로, 분수의 물줄기, 위성 안테나 모양 등이 포물선이에요."),
                     ("y = ax²과 y = −ax²의 관계는?", "x축에 대하여 서로 대칭이에요.")],
                    [("이차함수의 뜻", [(qf_basic(("is", "val", "pt")), 20)]),
                     ("y = ax²의 그래프", [(qf_basic(("width", "prop")), 20)]),
                     ("평행이동", [(qf_shift(("move",)), 20)]),
                     ("꼭짓점과 축", [(qf_shift(("vtx", "axis")), 20)]),
                     ("그래프 읽기", [(qf_graph(), 12), (qf_shift(("dir",)), 8)])], 82908)
    if which == "qfg":
        return unit(G, "graphs-of-quadratic-functions", 9, "[9수02-22]", "이차함수의 그래프를 그릴 수 있고, 그 성질을 설명할 수 있다.",
                    "이차함수 y = ax² + bx + c의 그래프", "이차함수의 그래프",
                    "중학교 3학년 수학 이차함수 y = ax² + bx + c의 그래프 문제: y = a(x − p)² + q 꼴로 고치기, 꼭짓점, y축·x축과 만나는 점, 꼭짓점과 한 점으로 식 구하기, a·b·c의 부호, 증가와 감소까지 100문제와 정답·해설.",
                    "완전제곱식으로 고치면 꼭짓점이 보여요", "꼭짓점 x좌표는 −b/2a예요.",
                    ["y = ax² + bx + c는 y = a(x + b/2a)² − (b² − 4ac)/4a 꼴로 고칠 수 있어요.",
                     "y축과 만나는 점의 y좌표는 c, x축과 만나는 점의 x좌표는 ax² + bx + c = 0의 해예요.",
                     "그래프로 부호 알기: 볼록한 방향 → a, 축의 위치 → a와 b의 부호가 같으면 왼쪽, 다르면 오른쪽, y절편 → c",
                     "축 x = p를 기준으로 a &gt; 0이면 왼쪽에서 감소·오른쪽에서 증가, a &lt; 0이면 그 반대예요."],
                    [("y = x² − 4x + 1", ["(x − 2)² − 3"], "꼭짓점 (2, −3)"), ("y = x² − x − 6과 x축", ["(x − 3)(x + 2) = 0"], "−2, 3")],
                    [("완전제곱식을 만들 때 더한 수를 빼지 않는다", "x² − 4x + 4 − 4처럼 더한 만큼 빼요."),
                     ("꼭짓점의 x좌표를 b/2a로 한다", "−b/2a예요."),
                     ("y절편을 꼭짓점의 y좌표로 착각한다", "y절편은 x = 0일 때의 값 c예요.")],
                    [("x축과 만나지 않는 경우는?", "ax² + bx + c = 0의 근이 없을 때(b² − 4ac &lt; 0)예요."),
                     ("세 점을 지나는 이차함수는?", "y = ax² + bx + c에 세 점을 대입해 연립방정식으로 구해요.")],
                    [("y = a(x − p)² + q 꼴로 고치기", [(qg_std(("conv",)), 20)]),
                     ("꼭짓점과 축과의 교점", [(qg_std(("vtx", "yint", "xint")), 20)]),
                     ("이차함수의 식 구하기", [(qg_std(("find",)), 20)]),
                     ("a, b, c의 부호", [(qg_coef(("sign",)), 20)]),
                     ("증가와 감소", [(qg_coef(("maxmin",)), 20)])], 82909)
    raise ValueError(which)
