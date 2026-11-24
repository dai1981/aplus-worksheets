# -*- coding: utf-8 -*-
"""
대한민국 초등 6학년 수학：분수의 나눗셈・소수의 나눗셈
  fw : (자연수) ÷ (자연수)의 몫을 분수로, (분수) ÷ (자연수) [6수01-10] [6수01-11]
  ff : (분수) ÷ (분수) [6수01-11]
  dw : (소수) ÷ (자연수), (자연수) ÷ (자연수)의 몫을 소수로 [6수01-14] [6수01-15]
  dd : (소수) ÷ (소수), 몫의 반올림과 나머지 [6수01-15]
誤答は「나누는 수를 분자에 곱한다」「역수를 나누어지는 수에 쓴다」「소수점을 옮기지 않는다」「나머지의 소수점을 처음 자리에 찍지 않는다」から作る。
"""
import math
import random
from decimal import Decimal as D
from fractions import Fraction as F
from kr_common import mcq, unit, Names, josa, fr, ff, num

R = random.Random(82601)
NM = Names(R)


def fs(v):
    return ff(F(v), mixed=True)


def fi(v):
    v = F(v)
    return fr(v.numerator, v.denominator) if v.denominator > 1 else str(v.numerator)


def dd(v):
    return format(D(v).normalize(), "f")


def eq(raw, ans):
    return "<b>%s</b>" % ans if raw == ans else "%s = <b>%s</b>" % (raw, ans)


def rf(maxd=9, proper=True):
    while True:
        d = R.randint(2, maxd)
        n = R.randint(1, d - 1 if proper else 3 * d)
        if math.gcd(n, d) == 1 and n % d:
            return F(n, d)


# ---------------------------------------------------------------- (분수) ÷ (자연수)
def nn_frac():
    a, b = R.randint(1, 20), R.randint(2, 12)
    if a % b == 0:
        return None
    ans = F(a, b)
    return mcq("%d ÷ %d의 몫을 분수로 나타내면?" % (a, b), fs(ans), [fs(F(b, a)) if a else None, fs(ans + 1), fs(F(a, b * 2))],
               "(자연수) ÷ (자연수)의 몫은 나누어지는 수를 분자, 나누는 수를 분모로 해요. %d ÷ %d = %s" % (a, b, eq(fr(a, b), fs(ans))))


def fw(kind):
    def mk():
        w = R.randint(2, 9)
        if kind == "div":      # 분자가 나누어떨어짐
            d = R.randint(3, 12)
            k = R.randint(1, max(1, (d - 1) // w))
            n = w * k
            if n >= d:
                return None
            x = F(n, d)
            if x.denominator != d:
                return None
            ans = x / w
            return mcq("%s ÷ %d =" % (fr(n, d), w), fs(ans), [fs(F(n * w, d)), fs(F(n, d * w * w)), fs(F(n, d + w))],
                       "분자가 %d로 나누어떨어지므로 분자를 나눠요. %s ÷ %d = <b>%s</b>" % (w, fr(n, d), w, fs(ans)))
        if kind == "prop":     # 진분수 ÷ 자연수
            x = rf(9)
            ans = x / w
            return mcq("%s ÷ %d =" % (fi(x), w), fs(ans), [fs(x * w), fs(F(x.numerator, x.denominator + w)), fs(ans * 2)],
                       "÷ %d를 × %s로 바꾸어 계산해요. %s × %s = <b>%s</b>" % (w, fr(1, w), fi(x), fr(1, w), fs(ans)))
        if kind == "imp":      # 가분수 ÷ 자연수
            d = R.randint(2, 8)
            n = R.randint(d + 1, 4 * d)
            if math.gcd(n, d) > 1:
                return None
            ans = F(n, d) / w
            return mcq("%s ÷ %d =" % (fr(n, d), w), fs(ans), [fs(F(n * w, d)), fs(F(n, d) - w) if F(n, d) > w else fs(ans + 1), fs(ans * w * w) if ans * w * w != ans else None, fs(ans + F(1, d * w))],
                       "%s × %s = <b>%s</b>" % (fr(n, d), fr(1, w), fs(ans)))
        x = rf(6) + R.randint(1, 4)      # 대분수 ÷ 자연수
        ans = x / w
        whole = int(x)
        frac = x - whole
        wrong = F(whole, w) + frac
        return mcq("%d%s ÷ %d =" % (whole, fi(frac), w), fs(ans), [fs(wrong) if wrong != ans else fs(ans + 1), fs(x * w), fs(ans + F(1, frac.denominator * w))],
                   "대분수를 가분수 %s로 바꾸어 계산해요. %s × %s = <b>%s</b>" % (fi(x), fi(x), fr(1, w), fs(ans)))
    return mk


THINGS = [("주스", "L"), ("우유", "L"), ("리본", "m"), ("철사", "m"), ("밀가루", "kg"), ("찰흙", "kg")]


def fw_story():
    th, u = R.choice(THINGS)
    w = R.randint(2, 6)
    x = rf(9, proper=R.random() < 0.6)
    ans = x / w
    return mcq("%s %s %s를 %d명이 똑같이 나누어 가지려고 해요. 한 사람이 몇 %s씩 가질 수 있나요?" % (th, fs(x), u, w, u), "%s %s" % (fs(ans), u),
               ["%s %s" % (fs(x * w), u), "%s %s" % (fs(x - w) if x > w else fs(ans + F(1, 2)), u), "%s %s" % (fs(F(w, 1) / x), u)],
               "%s ÷ %d = <b>%s %s</b>" % (fs(x), w, fs(ans), u))


# ---------------------------------------------------------------- (분수) ÷ (분수)
def ff_q(kind):
    def mk():
        if kind == "same":     # 분모가 같은 분수
            d = R.randint(3, 15)
            a, b = R.randint(1, d - 1), R.randint(1, d - 1)
            if a == b:
                return None
            ans = F(a, b)
            return mcq("%s ÷ %s =" % (fr(a, d), fr(b, d)), fs(ans), [fs(F(a, b * d)), fs(F(b, a)), fs(F(a * b, d * d))],
                       "분모가 같으면 분자끼리 나눠요. %d ÷ %d = %s" % (a, b, eq(fr(a, b) if b > 1 else str(a), fs(ans))))
        if kind == "diff":
            x, y = rf(9), rf(9)
            if x == y:
                return None
            ans = x / y
            return mcq("%s ÷ %s =" % (fi(x), fi(y)), fs(ans), [fs(x * y), fs(y / x), fs(F(x.numerator * y.numerator, x.denominator * y.denominator)) if x * y != F(x.numerator * y.numerator, x.denominator * y.denominator) else fs(ans + 1)],
                       "나누는 분수의 분모와 분자를 바꾸어 곱해요. %s × %s = <b>%s</b>" % (fi(x), fr(y.denominator, y.numerator), fs(ans)))
        if kind == "wf":       # 자연수 ÷ 분수
            w = R.randint(2, 15)
            y = rf(9)
            ans = w / y
            return mcq("%d ÷ %s =" % (w, fi(y)), fs(ans), [fs(w * y), fs(y / w), fs(ans + 1)],
                       "%d × %s = <b>%s</b>" % (w, fr(y.denominator, y.numerator), fs(ans)))
        x = rf(6) + R.randint(1, 3)
        y = rf(6) + R.randint(0, 2)
        if x == y:
            return None
        ans = x / y
        sx = "%d%s" % (int(x), fi(x - int(x)))
        sy = ("%d" % int(y) if int(y) else "") + fi(y - int(y))
        return mcq("%s ÷ %s =" % (sx, sy), fs(ans), [fs(x * y), fs(y / x), fs(ans + 1)],
                   "가분수로 바꾸어 계산해요. %s ÷ %s = %s × %s = <b>%s</b>" % (fi(x), fi(y), fi(x), fr(y.denominator, y.numerator), fs(ans)))
    return mk


def ff_story():
    k = R.choice(["count", "per", "len"])
    if k == "count":
        d = R.choice([2, 3, 4, 5, 6, 8])
        n = R.randint(1, d - 1)
        if math.gcd(n, d) > 1:
            return None
        tot = F(n * R.randint(2, 9), d)
        cnt = tot / F(n, d)
        return mcq("주스 %s L를 한 컵에 %s L씩 나누어 담으려고 해요. 몇 컵에 담을 수 있나요?" % (fs(tot), fr(n, d)), "%d컵" % cnt,
                   ["%s컵" % fs(tot * F(n, d)), "%d컵" % (cnt + 1), "%d컵" % (cnt * d)], "%s ÷ %s = <b>%d컵</b>" % (fs(tot), fr(n, d), cnt))
    if k == "per":
        x, y = rf(8, False), rf(5)
        ans = x / y
        return mcq("%s km를 가는 데 휘발유 %s L가 들어요. 휘발유 1 L로 몇 km를 갈 수 있나요?" % (fs(x), fs(y)), "%s km" % fs(ans),
                   ["%s km" % fs(x * y), "%s km" % fs(y / x), "%s km" % fs(ans + 1)], "%s ÷ %s = <b>%s km</b>" % (fs(x), fs(y), fs(ans)))
    a = rf(8, False)
    b = rf(6)
    ans = a / b
    return mcq("넓이가 %s m²인 직사각형의 세로가 %s m예요. 가로는 몇 m인가요?" % (fs(a), fs(b)), "%s m" % fs(ans),
               ["%s m" % fs(a * b), "%s m" % fs(b / a), "%s m" % fs(ans + F(1, 2))], "(가로) = (넓이) ÷ (세로) = %s ÷ %s = <b>%s m</b>" % (fs(a), fs(b), fs(ans)))


# ---------------------------------------------------------------- (소수) ÷ (자연수)
def rdec(places, lo, hi):
    n = R.randint(lo, hi)
    if n % 10 == 0:
        return None
    return D(n).scaleb(-places)


def dw(kind):
    def mk():
        w = R.randint(2, 9)
        if kind == "exact":
            q = rdec(R.choice([1, 2]), 11, 999)
            if q is None:
                return None
            a = q * w
        elif kind == "lt1":    # 몫이 1보다 작은
            q = rdec(2, 11, 99)
            if q is None or q >= 1:
                return None
            a = q * w
        elif kind == "zero":   # 몫의 소수 첫째 자리에 0
            q = D(R.randint(1, 9)) + D(R.randint(1, 9)) / 100
            a = q * w
        else:                  # (자연수) ÷ (자연수) → 소수
            w = R.choice([2, 4, 5, 8, 20, 25])
            a = D(R.randint(1, 30))
            q = a / w
            if q == q.to_integral() or len(dd(q).split(".")[-1]) > 3:
                return None
            inv = D(w) / a
            return mcq("%s ÷ %d의 몫을 소수로 나타내면?" % (dd(a), w), dd(q), [dd(q * 10), dd(q / 10), dd(inv) if inv == inv.quantize(D("0.001")) else dd(q + 1)],
                       "나누어떨어지지 않으면 0을 내려 계속 나눠요. <b>%s</b>" % dd(q))
        if (a * 100) != (a * 100).to_integral():
            return None
        return mcq("%s ÷ %d =" % (dd(a), w), dd(q), [dd(q * 10), dd(q / 10), dd(q + D(1) / 10)],
                   "자연수의 나눗셈처럼 계산하고, 몫의 소수점은 나누어지는 수의 소수점 위치에 맞추어 찍어요. <b>%s</b>" % dd(q))
    return mk


def dw_story():
    k = R.choice(["share", "speed", "side"])
    if k == "share":
        w = R.randint(2, 8)
        q = rdec(2, 11, 299)
        if q is None:
            return None
        a = q * w
        return mcq("우유 %s L를 %d명이 똑같이 나누어 마셨어요. 한 사람이 마신 우유는 몇 L인가요?" % (dd(a), w), "%s L" % dd(q),
                   ["%s L" % dd(a * w), "%s L" % dd(q * 10), "%s L" % dd(q / 10)], "%s ÷ %d = <b>%s L</b>" % (dd(a), w, dd(q)))
    if k == "speed":
        w = R.randint(2, 6)
        q = rdec(1, 11, 199)
        if q is None:
            return None
        return mcq("%d시간 동안 %s km를 일정한 빠르기로 걸었어요. 1시간에 몇 km를 걸었나요?" % (w, dd(q * w)), "%s km" % dd(q),
                   ["%s km" % dd(q * w * w), "%s km" % dd(q * 10), "%s km" % dd(q + 1)], "%s ÷ %d = <b>%s km</b>" % (dd(q * w), w, dd(q)))
    n = R.choice([3, 4, 5, 6, 8])
    q = rdec(1, 11, 99)
    if q is None:
        return None
    nm = {3: "정삼각형", 4: "정사각형", 5: "정오각형", 6: "정육각형", 8: "정팔각형"}[n]
    return mcq("둘레가 %s cm인 %s의 한 변은 몇 cm인가요?" % (dd(q * n), nm), "%s cm" % dd(q), ["%s cm" % dd(q * 10), "%s cm" % dd(q / 10), "%s cm" % dd(q * n * 2)],
               "%s ÷ %d = <b>%s cm</b>" % (dd(q * n), n, dd(q)))


# ---------------------------------------------------------------- (소수) ÷ (소수)
def dd_q(kind):
    def mk():
        if kind == "same":     # 자리 수가 같은 소수
            b = rdec(1, 2, 99)
            q = R.randint(2, 30)
            if b is None:
                return None
            a = b * q
            return mcq("%s ÷ %s =" % (dd(a), dd(b)), str(q), [dd(D(q) / 10), str(q * 10), dd(D(q) / 100)],
                       "나누는 수와 나누어지는 수의 소수점을 똑같이 오른쪽으로 옮겨 자연수의 나눗셈으로 바꿔요. <b>%d</b>" % q)
        if kind == "diff":     # 자리 수가 다른 소수
            b = rdec(1, 2, 49)
            q = rdec(1, 11, 99)
            if b is None or q is None:
                return None
            a = b * q
            return mcq("%s ÷ %s =" % (dd(a), dd(b)), dd(q), [dd(q * 10), dd(q / 10), dd(q + D(1) / 10)],
                       "나누는 수가 자연수가 되도록 두 수의 소수점을 똑같이 옮겨요. <b>%s</b>" % dd(q))
        if kind == "wd":       # (자연수) ÷ (소수)
            b = rdec(R.choice([1, 2]), 2, 99)
            if b is None:
                return None
            q = R.randint(2, 60)
            a = b * q
            if a != a.to_integral():
                return None
            return mcq("%s ÷ %s =" % (dd(a), dd(b)), str(q), [dd(D(q) / 10), str(q * 10), str(q * 100)],
                       "나누는 수의 소수점을 옮긴 만큼 자연수 뒤에 0을 붙여요. <b>%d</b>" % q)
        if kind == "round":    # 몫을 반올림
            a, b = rdec(1, 101, 999), rdec(1, 11, 99)
            if a is None or b is None:
                return None
            p = R.choice([1, 2])
            q = (a / b).quantize(D(1).scaleb(-p), rounding="ROUND_HALF_UP")
            down = (a / b).quantize(D(1).scaleb(-p), rounding="ROUND_DOWN")
            nm = {1: "소수 첫째 자리", 2: "소수 둘째 자리"}[p]
            return mcq("%s ÷ %s의 몫을 반올림하여 %s까지 나타내면?" % (dd(a), dd(b), nm), format(q, "f"),
                       [format(down, "f") if down != q else format(q + D(1).scaleb(-p), "f"), format(q * 10, "f"), format((a / b).quantize(D(1).scaleb(-p - 1), rounding="ROUND_HALF_UP"), "f")],
                       "%s 바로 아래 자리까지 몫을 구한 뒤 반올림해요. <b>%s</b>" % (nm, format(q, "f")))
        # 나머지
        b = R.randint(2, 9)
        a = rdec(1, 101, 999)
        if a is None:
            return None
        q = int(a // b)
        r = a - b * q
        if r == 0:
            return None
        return mcq("%s를 %d씩 나누면 몫은 자연수로 몇이고 남는 양은 얼마인가요? (%s ÷ %d)" % (dd(a), b, dd(a), b), "몫 %d, 나머지 %s" % (q, dd(r)),
                   ["몫 %d, 나머지 %s" % (q, dd(r * 10)), "몫 %d, 나머지 %s" % (q + 1, dd(r)), "몫 %d, 나머지 %s" % (q, dd(r / 10))],
                   "%d × %d = %d, %s − %d = %s. 나머지의 소수점은 나누어지는 수의 소수점 자리에 맞춰 찍어요. <b>몫 %d, 나머지 %s</b>" % (b, q, b * q, dd(a), b * q, dd(r), q, dd(r)))
    return mk


def dd_story():
    k = R.choice(["bottle", "rope", "rate"])
    if k == "bottle":
        b = rdec(1, 3, 15)
        n = R.randint(3, 20)
        if b is None:
            return None
        a = b * n
        return mcq("물 %s L를 %s L짜리 병에 가득 나누어 담으려고 해요. 병은 몇 개 필요한가요?" % (dd(a), dd(b)), "%d개" % n,
                   ["%d개" % (n * 10), "%s개" % dd(D(n) / 10), "%d개" % (n + 1)], "%s ÷ %s = <b>%d개</b>" % (dd(a), dd(b), n))
    if k == "rope":
        a = rdec(1, 101, 499)
        b = rdec(1, 11, 39)
        if a is None or b is None:
            return None
        n = int(a // b)
        r = a - b * n
        if n < 2 or r == 0:
            return None
        return mcq("끈 %s m를 %s m씩 잘라 리본을 만들려고 해요. 리본은 최대 몇 개 만들 수 있고, 남는 끈은 몇 m인가요?" % (dd(a), dd(b)), "%d개, %s m" % (n, dd(r)),
                   ["%d개, %s m" % (n, dd(r * 10)), "%d개, %s m" % (n + 1, dd(r)), "%d개, %s m" % (n - 1, dd(r + b))],
                   "%s ÷ %s = %d … %s. <b>%d개, %s m</b>" % (dd(a), dd(b), n, dd(r), n, dd(r)))
    b = rdec(1, 11, 49)
    q = rdec(1, 11, 99)
    if b is None or q is None:
        return None
    a = b * q
    return mcq("철근 %s m의 무게가 %s kg이에요. 철근 1 m의 무게는 몇 kg인가요?" % (dd(b), dd(a)), "%s kg" % dd(q),
               ["%s kg" % dd(a * b), "%s kg" % dd(b / q) if (b / q) == (b / q).quantize(D("0.01")) else "%s kg" % dd(q * 10), "%s kg" % dd(q / 10)],
               "%s ÷ %s = <b>%s kg</b>" % (dd(a), dd(b), dd(q)))


def build(which):
    G = "grade-6"
    if which == "fw":
        return unit(G, "dividing-fractions-by-whole-numbers", 1, "[6수01-10] [6수01-11]",
                    "‘(자연수)÷(자연수)’에서 나눗셈의 몫을 분수로 나타낼 수 있다. 분수의 나눗셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                    "(분수) ÷ (자연수)", "(분수) ÷ (자연수)",
                    "초등 6학년 1학기 분수의 나눗셈 학습지: (자연수) ÷ (자연수)의 몫을 분수로, (진분수・가분수・대분수) ÷ (자연수), 문장제까지 100문제와 정답.",
                    "÷ (자연수)는 × (1/자연수)", "대분수는 가분수로 바꾸어 계산해요.",
                    ["(자연수) ÷ (자연수)의 몫은 분수로 나타낼 수 있어요. 3 ÷ 4 = <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>",
                     "분자가 자연수로 나누어떨어지면 분자를 나눠요.",
                     "나누어떨어지지 않으면 ÷ (자연수)를 × <span class='fr'><span class='fn'>1</span><span class='fd'>자연수</span></span>로 바꾸어 계산해요.",
                     "대분수는 먼저 가분수로 바꿔요."],
                    [("1<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> ÷ 4", ["8/5 ÷ 4", "= 8/5 × 1/4 = 8/20 = 2/5"], "<span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>")],
                    [("÷ 4를 × 4로 계산한다", "÷ 4는 × 1/4이에요."),
                     ("분모를 나눈다", "분자가 나누어떨어질 때만 분자를 나누고, 아니면 1/자연수를 곱해요."),
                     ("대분수의 자연수만 나눈다", "대분수는 가분수로 바꾸어 계산해요.")],
                    [("분수의 나눗셈은 언제 배우나요?", "초등 6학년 1학기에 (분수) ÷ (자연수), 2학기에 (분수) ÷ (분수)를 배워요."),
                     ("몫이 맞는지 확인하는 방법은?", "몫에 나누는 수를 곱해서 처음 수가 되는지 확인해요.")],
                    [("몫을 분수로", [(nn_frac, 20)]),
                     ("분자가 나누어떨어지는 나눗셈", [(fw("div"), 20)]),
                     ("(진분수) ÷ (자연수)", [(fw("prop"), 12), (fw("imp"), 8)]),
                     ("(대분수) ÷ (자연수)", [(fw("mix"), 20)]),
                     ("문장제", [(fw_story, 20)])], 82601)
    if which == "ff":
        return unit(G, "dividing-fractions", 8, "[6수01-11]",
                    "분수의 나눗셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                    "(분수) ÷ (분수)", "(분수) ÷ (분수)",
                    "초등 6학년 2학기 분수의 나눗셈 학습지: 분모가 같은 분수의 나눗셈, 분모가 다른 분수의 나눗셈, (자연수) ÷ (분수), 대분수의 나눗셈, 문장제까지 100문제와 정답.",
                    "나누는 분수를 뒤집어 곱해요", "분모가 같으면 분자끼리 나눠요.",
                    ["분모가 같은 분수의 나눗셈은 <b>분자끼리</b> 나눠요.",
                     "분모가 다르면 통분해서 분자끼리 나누거나, 나누는 분수의 <b>분모와 분자를 바꾸어 곱해요</b>.",
                     "(자연수) ÷ (분수)도 분수의 분모와 분자를 바꾸어 곱해요.",
                     "대분수는 가분수로 바꾸어 계산해요."],
                    [("<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> ÷ <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>",
                      ["3/4 × 5/2 = 15/8"], "1<span class='fr'><span class='fn'>7</span><span class='fd'>8</span></span>")],
                    [("나누어지는 분수를 뒤집는다", "나누는 분수(÷ 뒤의 분수)를 뒤집어요."),
                     ("뒤집기만 하고 나눗셈을 그대로 둔다", "뒤집은 다음 곱해요."),
                     ("분모끼리, 분자끼리 나누다가 나누어떨어지지 않아서 멈춘다", "통분하거나 뒤집어 곱해요.")],
                    [("왜 뒤집어 곱하나요?", "÷ 2/5는 1/5이 2개인 것으로 나누는 것이라 ÷ 2 × 5와 같아요. 그래서 × 5/2가 돼요."),
                     ("1보다 작은 분수로 나누면 몫은?", "나누어지는 수보다 커져요.")],
                    [("분모가 같은 분수", [(ff_q("same"), 20)]),
                     ("분모가 다른 분수", [(ff_q("diff"), 20)]),
                     ("(자연수) ÷ (분수)", [(ff_q("wf"), 20)]),
                     ("대분수의 나눗셈", [(ff_q("mix"), 20)]),
                     ("문장제", [(ff_story, 20)])], 82608)
    if which == "dw":
        return unit(G, "dividing-decimals-by-whole-numbers", 3, "[6수01-14] [6수01-15]",
                    "‘(자연수)÷(자연수)’에서 나눗셈의 몫을 소수로 나타낼 수 있다. 소수의 나눗셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                    "(소수) ÷ (자연수)", "(소수) ÷ (자연수)",
                    "초등 6학년 1학기 소수의 나눗셈 학습지: (소수) ÷ (자연수), 몫이 1보다 작은 나눗셈, 몫의 소수 첫째 자리에 0이 있는 나눗셈, (자연수) ÷ (자연수)의 몫을 소수로, 문장제까지 100문제와 정답.",
                    "몫의 소수점은 위의 소수점에 맞춰요", "나누어떨어지지 않으면 0을 내려 계속 나눠요.",
                    ["자연수의 나눗셈처럼 계산하고, 몫의 소수점은 <b>나누어지는 수의 소수점 위치</b>에 맞추어 찍어요.",
                     "몫이 1보다 작으면 일의 자리에 0을 써요. 2.24 ÷ 4 = 0.56",
                     "나눌 수 없는 자리는 몫에 0을 쓰고 다음 자리를 내려요. 6.24 ÷ 6 = 1.04",
                     "(자연수) ÷ (자연수)도 0을 내려 나누면 몫을 소수로 나타낼 수 있어요. 3 ÷ 4 = 0.75"],
                    [("7.35 ÷ 5", ["735 ÷ 5 = 147", "소수점을 맞추면 1.47"], "1.47")],
                    [("몫의 소수점을 빠뜨린다 (147)", "나누어지는 수의 소수점 위치에 맞춰 찍어요."),
                     ("몫의 0을 빠뜨린다 (6.24 ÷ 6 = 1.4)", "나눌 수 없는 자리에는 0을 써요: 1.04"),
                     ("3 ÷ 4를 나눌 수 없다고 한다", "3을 3.00으로 생각하고 나눠요.")],
                    [("소수의 나눗셈은 언제 배우나요?", "초등 6학년 1학기에 (소수) ÷ (자연수), 2학기에 (소수) ÷ (소수)를 배워요."),
                     ("어림으로 확인하는 방법은?", "7.35 ÷ 5는 약 7 ÷ 5 = 1.4이니 1.47이 알맞아요.")],
                    [("(소수) ÷ (자연수)", [(dw("exact"), 20)]),
                     ("몫이 1보다 작은 나눗셈", [(dw("lt1"), 20)]),
                     ("몫에 0이 있는 나눗셈", [(dw("zero"), 20)]),
                     ("몫을 소수로 나타내기", [(dw("nn"), 20)]),
                     ("문장제", [(dw_story, 20)])], 82603)
    return unit(G, "dividing-decimals", 9, "[6수01-15]",
                "소수의 나눗셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                "(소수) ÷ (소수)", "(소수) ÷ (소수)",
                "초등 6학년 2학기 소수의 나눗셈 학습지: 자리 수가 같은・다른 (소수) ÷ (소수), (자연수) ÷ (소수), 몫을 반올림하기, 나누어 주고 남는 양, 문장제까지 100문제와 정답.",
                "나누는 수를 자연수로 만들어요", "두 수의 소수점을 똑같이 옮겨요.",
                ["나누는 수가 자연수가 되도록 나누는 수와 나누어지는 수의 소수점을 <b>똑같이</b> 오른쪽으로 옮겨요.",
                 "옮긴 뒤에는 (소수) ÷ (자연수)처럼 계산해요.",
                 "몫이 나누어떨어지지 않으면 구하려는 자리 바로 아래까지 구해서 반올림해요.",
                 "나누어 주고 남는 양의 소수점은 처음 나누어지는 수의 소수점 자리에 찍어요."],
                [("3.12 ÷ 0.4", ["소수점을 한 칸씩 옮기면 31.2 ÷ 4", "= 7.8"], "7.8")],
                [("나누는 수만 소수점을 옮긴다", "두 수를 똑같이 옮겨야 몫이 같아요."),
                 ("남는 양의 소수점을 옮긴 자리에 찍는다", "남는 양은 처음 소수점 자리에 맞춰요."),
                 ("반올림할 자리까지만 구한다", "한 자리 더 구해야 반올림할 수 있어요.")],
                [("왜 소수점을 똑같이 옮겨도 되나요?", "나누는 수와 나누어지는 수에 같은 수를 곱하면 몫이 변하지 않기 때문이에요."),
                 ("몫이 처음 수보다 커질 수도 있나요?", "1보다 작은 수로 나누면 몫이 커져요.")],
                [("자리 수가 같은 소수", [(dd_q("same"), 20)]),
                 ("자리 수가 다른 소수", [(dd_q("diff"), 20)]),
                 ("(자연수) ÷ (소수)", [(dd_q("wd"), 20)]),
                 ("몫의 반올림과 남는 양", [(dd_q("round"), 10), (dd_q("rem"), 10)]),
                 ("문장제", [(dd_story, 20)])], 82609)
