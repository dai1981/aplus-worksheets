# -*- coding: utf-8 -*-
"""
대한민국 초등 5학년 수학：약분과 통분・분수의 크기 비교・분수의 덧셈과 뺄셈・분수의 곱셈・소수의 곱셈
  simplify : 크기가 같은 분수, 약분과 통분 [6수01-06]
  compare  : 분모가 다른 분수의 크기 비교, 분수와 소수 [6수01-07] [6수01-12]
  fadd     : 분모가 다른 분수의 덧셈과 뺄셈 [6수01-08]
  fmul     : 분수의 곱셈 [6수01-09]
  dmul     : 소수의 곱셈 [6수01-13]
答えは기약분수（대분수）。誤答は「분모끼리 더한다」「분자에만 곱한다」「약분을 덜 한다」「소수점 위치를 잘못 찍는다」から作る。
"""
import math
import random
from decimal import Decimal as D
from fractions import Fraction as F
from kr_common import mcq, unit, Names, josa, fr, ff, num
from kr_pics import frac_bar

R = random.Random(82504)
NM = Names(R)


def fs(v):
    return ff(F(v), mixed=True)


def fi(v):
    """가분수 그대로（기약）"""
    v = F(v)
    return fr(v.numerator, v.denominator) if v.denominator > 1 else str(v.numerator)


def dd(v):
    return format(D(v).normalize(), "f")


# ---------------------------------------------------------------- 약분과 통분
def equiv():
    d = R.randint(2, 9)
    n = R.randint(1, d - 1)
    if math.gcd(n, d) > 1:
        return None
    k = R.randint(2, 6)
    if R.random() < 0.5:
        return mcq("%s와 크기가 같은 분수는?" % fr(n, d), fr(n * k, d * k), [fr(n * k, d), fr(n + k, d + k), fr(n, d * k)],
                   "분모와 분자에 0이 아닌 같은 수를 곱하면 크기가 같아요. %s = <b>%s</b>" % (fr(n, d), fr(n * k, d * k)))
    return mcq("%s = %s 에서 □에 알맞은 수는?" % (fr(n, d), fr("□", d * k)), str(n * k), [str(n + k), str(n * k + 1), str(d * k - n)],
               "분모에 %d를 곱했으니 분자에도 %d를 곱해요. %d × %d = <b>%d</b>" % (k, k, n, k, n * k))


def reduce_q():
    d = R.randint(3, 12)
    n = R.randint(1, d - 1)
    if math.gcd(n, d) > 1:
        return None
    k = R.randint(2, 6)
    N, Dd = n * k, d * k
    divs = [x for x in range(2, k) if k % x == 0]
    half = fr(N // divs[0], Dd // divs[0]) if divs else fr(N, Dd // 1 + 1)
    return mcq("%s를 기약분수로 나타내면?" % fr(N, Dd), fr(n, d), [half, fr(n, Dd), fr(N, d) if N < d else fr(n + 1, d)],
               "분모와 분자의 최대공약수 %d로 나누어요. <b>%s</b>" % (k, fr(n, d)))


def is_irr():
    d = R.randint(4, 15)
    good = R.choice([n for n in range(1, d) if math.gcd(n, d) == 1])
    bads = [n for n in range(1, d) if math.gcd(n, d) > 1]
    if len(bads) < 3:
        return None
    if R.random() < 0.5:
        b = R.choice(bads)
        goods = [n for n in range(1, d) if math.gcd(n, d) == 1]
        return mcq("분모가 %d인 분수 중 기약분수가 <b>아닌</b> 것은?" % d, fr(b, d), [fr(g, d) for g in R.sample(goods, 3)],
                   "%d과 %d은 공약수 %d로 약분할 수 있어요. <b>%s</b>" % (b, d, math.gcd(b, d), fr(b, d)))
    return mcq("분모가 %d인 분수 중 기약분수는?" % d, fr(good, d), [fr(b, d) for b in R.sample(bads, 3)],
               "분모와 분자의 공약수가 1뿐인 분수가 기약분수예요. <b>%s</b>" % fr(good, d))


def common_den():
    while True:
        a, b = R.sample(range(2, 13), 2)
        if a * b // math.gcd(a, b) <= 60:
            break
    na, nb = R.randint(1, a - 1), R.randint(1, b - 1)
    if math.gcd(na, a) > 1 or math.gcd(nb, b) > 1:
        return None
    l = a * b // math.gcd(a, b)
    if R.random() < 0.5:
        return mcq("%s와 %s를 분모의 최소공배수로 통분하면?" % (fr(na, a), fr(nb, b)),
                   "(%s, %s)" % (fr(na * l // a, l), fr(nb * l // b, l)),
                   ["(%s, %s)" % (fr(na, l), fr(nb, l)), "(%s, %s)" % (fr(na * b, a * b), fr(nb * a, a * b)) if a * b != l else "(%s, %s)" % (fr(na * 2 * l // a, 2 * l), fr(nb * l // b, l)),
                    "(%s, %s)" % (fr(na * l // a, l), fr(nb, l))],
                   "%d과 %d의 최소공배수 %d를 공통분모로 해요. <b>(%s, %s)</b>" % (a, b, l, fr(na * l // a, l), fr(nb * l // b, l)))
    return mcq("%s와 %s를 통분할 때 공통분모가 될 수 <b>없는</b> 수는?" % (fr(na, a), fr(nb, b)), str(l + a if (l + a) % b else l + 1),
               [str(l), str(2 * l), str(3 * l)], "공통분모는 두 분모의 공배수 %d, %d, %d, … 예요." % (l, 2 * l, 3 * l))


# ---------------------------------------------------------------- 크기 비교
def two(maxd=12):
    while True:
        a, b = R.sample(range(2, maxd + 1), 2)
        na, nb = R.randint(1, a - 1), R.randint(1, b - 1)
        if F(na, a) != F(nb, b) and math.gcd(na, a) == 1 and math.gcd(nb, b) == 1:
            return na, a, nb, b


def cmp2():
    na, a, nb, b = two()
    ans = ">" if F(na, a) > F(nb, b) else "<"
    l = a * b // math.gcd(a, b)
    return mcq("두 분수의 크기를 비교하세요. %s ○ %s" % (fr(na, a), fr(nb, b)), ans, ["<" if ans == ">" else ">", "=", "비교할 수 없어요"],
               "통분하면 %s, %s이므로 <b>%s</b>" % (fr(na * l // a, l), fr(nb * l // b, l), ans))


def biggest():
    vals = set()
    while len(vals) < 4:
        d = R.randint(2, 12)
        n = R.randint(1, d - 1)
        if math.gcd(n, d) == 1:
            vals.add(F(n, d))
    vals = sorted(vals)
    big = R.random() < 0.5
    ans = vals[-1] if big else vals[0]
    show = list(vals)
    R.shuffle(show)
    return mcq("%s 중에서 가장 %s 분수는?" % (", ".join(fi(v) for v in show), "큰" if big else "작은"), fi(ans), [fi(v) for v in vals if v != ans],
               "통분하거나 소수로 바꾸어 비교해요. <b>%s</b>" % fi(ans))


def f2d():
    d = R.choice([2, 4, 5, 10, 20, 25, 50])
    n = R.randint(1, d - 1)
    if math.gcd(n, d) > 1:
        return None
    v = D(n) / D(d)
    if R.random() < 0.5:
        return mcq("%s를 소수로 나타내면?" % fr(n, d), dd(v), [dd(v * 10), dd(D(n) / 10), "%d.%d" % (n, d) if n < 10 else dd(v / 10)],
                   "분모를 10, 100으로 고쳐요. %s = <b>%s</b>" % (fr(n, d), dd(v)))
    k = len(dd(v).split(".")[1])
    P = 10 ** k
    m = int(v * P)
    g = math.gcd(m, P)
    return mcq("%s를 기약분수로 나타내면?" % dd(v), fr(m // g, P // g), [fr(m, P) if g > 1 else fr(m, P * 10), fr(m // g, P // g + 1), fr(m, 10)],
               "%s = %s = <b>%s</b>" % (dd(v), fr(m, P), fr(m // g, P // g)))


def fd_cmp():
    d = R.choice([2, 4, 5, 8, 10, 20, 25])
    n = R.randint(1, d - 1)
    v = D(n) / D(d)
    w = v + D(R.choice([-1, 1]) * R.choice([1, 5, 10, 15])) / 100
    if w <= 0 or w >= 1:
        return None
    ans = ">" if v > w else "<"
    return mcq("두 수의 크기를 비교하세요. %s ○ %s" % (fr(n, d), dd(w)), ans, ["<" if ans == ">" else ">", "=", "비교할 수 없어요"],
               "%s = %s이므로 <b>%s</b>" % (fr(n, d), dd(v), ans))


# ---------------------------------------------------------------- 덧셈과 뺄셈
def fadd(kind):
    def mk():
        na, a, nb, b = two(12)
        x, y = F(na, a), F(nb, b)
        wa = wb = 0
        if kind in ("mixadd", "mixsub"):
            wa, wb = R.randint(1, 5), R.randint(1, 4)
        X, Y = x + wa, y + wb
        l = a * b // math.gcd(a, b)
        if kind in ("sub", "mixsub"):
            if X <= Y:
                X, Y, x, y, a, b, na, nb, wa, wb = Y, X, y, x, b, a, nb, na, wb, wa
            if X == Y:
                return None
            ans = X - Y
            op = "−"
            wrong = F(abs(na - nb), a + b) if na != nb else F(1, a + b)
        else:
            ans = X + Y
            op = "+"
            wrong = F(na + nb, a + b)
        sx = ("%d" % wa if wa else "") + fr(na, a)
        sy = ("%d" % wb if wb else "") + fr(nb, b)
        cands = [fs(wrong + (wa + wb if op == "+" else max(0, wa - wb))), fs(ans + F(1, l)), fs(ans + 1) if ans + 1 != ans else None, fs(ans - F(1, l)) if ans > F(1, l) else fs(ans + 2)]
        e = "%d과 %d의 최소공배수 %d로 통분해서 계산해요. " % (a, b, l)
        e += "%s %s %s = <b>%s</b>" % (("%d" % wa if wa else "") + fr(na * l // a, l), op, ("%d" % wb if wb else "") + fr(nb * l // b, l), fs(ans))
        return mcq("%s %s %s =" % (sx, op, sy), fs(ans), cands, e)
    return mk


FOOD = [("우유", "L"), ("주스", "L"), ("물", "L"), ("밀가루", "kg"), ("설탕", "kg"), ("리본", "m"), ("끈", "m")]


def fadd_story():
    th, u = R.choice(FOOD)
    na, a, nb, b = two(10)
    x, y = F(na, a) + R.randint(0, 3), F(nb, b) + R.randint(0, 2)
    who = NM.next()
    k = R.choice(["add", "sub"])
    if k == "add":
        s = x + y
        return mcq("%s %s 어제 %s %s, 오늘 %s %s 사용했어요. 이틀 동안 사용한 %s 모두 몇 %s인가요?" % (josa(who, "은/는"), josa(th, "을/를"), fs(x), u, fs(y), u, josa(th, "은/는"), u),
                   "%s %s" % (fs(s), u), ["%s %s" % (fs(abs(x - y)) if x != y else fs(s + 1), u), "%s %s" % (fs(s + 1), u), "%s %s" % (fs(F(na + nb, a + b) + int(x) + int(y)), u)],
                   "%s + %s = <b>%s %s</b>" % (fs(x), fs(y), fs(s), u))
    if x <= y:
        x, y = y, x
    if x == y:
        return None
    s = x - y
    return mcq("%s %s %s 중에서 %s %s 사용했어요. 남은 %s 몇 %s인가요?" % (th, fs(x), u, fs(y), u, josa(th, "은/는"), u), "%s %s" % (fs(s), u),
               ["%s %s" % (fs(x + y), u), "%s %s" % (fs(s + 1), u), "%s %s" % (fs(s + F(1, a * b)), u)],
               "%s − %s = <b>%s %s</b>" % (fs(x), fs(y), fs(s), u))


# ---------------------------------------------------------------- 분수의 곱셈
def fmul(kind):
    def mk():
        d = R.randint(2, 12)
        n = R.randint(1, d - 1)
        if math.gcd(n, d) > 1:
            return None
        x = F(n, d)
        if kind == "fw":       # 분수 × 자연수
            w = R.randint(2, 12)
            ans = x * w
            return mcq("%s × %d =" % (fr(n, d), w), fs(ans), [fs(F(n, d * w)), fs(F(n * w, d * w)) if w > 1 else None, fs(ans + 1), fs(ans + F(1, d))],
                       "분자와 자연수를 곱해요. %s = <b>%s</b>" % (fr(n * w, d), fs(ans)))
        if kind == "wf":       # 자연수 × 분수
            w = R.randint(2, 30)
            ans = w * x
            return mcq("%d × %s =" % (w, fr(n, d)), fs(ans), [fs(F(w * d, n)) if n > 0 else None, fs(F(w + n, d)), fs(ans + 1), fs(ans + F(1, d))],
                       "%d × %s = %s = <b>%s</b>" % (w, fr(n, d), fr(w * n, d), fs(ans)))
        if kind == "ff":       # 진분수 × 진분수
            d2 = R.randint(2, 10)
            n2 = R.randint(1, d2 - 1)
            y = F(n2, d2)
            ans = x * y
            return mcq("%s × %s =" % (fr(n, d), fr(n2, d2)), fs(ans), [fs(F(n * n2, d + d2)), fs(F(n + n2, d * d2)), fs(F(n * d2, d * n2)), fs(ans + F(1, d * d2))],
                       "분자끼리, 분모끼리 곱해요. %s" % (("%s = <b>%s</b>" % (fr(n * n2, d * d2), fs(ans))) if ans.denominator != d * d2 else "<b>%s</b>" % fs(ans)))
        if kind == "unit":
            a, b = R.randint(2, 9), R.randint(2, 9)
            return mcq("%s × %s =" % (fr(1, a), fr(1, b)), fr(1, a * b), [fr(1, a + b), fr(2, a * b), fr(1, max(a, b))],
                       "단위분수끼리의 곱은 분모끼리 곱해요. <b>%s</b>" % fr(1, a * b))
        # 대분수의 곱셈
        w = R.randint(1, 3)
        X = x + w
        d2 = R.randint(2, 6)
        n2 = R.randint(1, d2 - 1)
        w2 = R.randint(0, 2)
        Y = F(n2, d2) + w2
        ans = X * Y
        sy = ("%d" % w2 if w2 else "") + fr(n2, d2)
        wrong = w * w2 + x * F(n2, d2)
        return mcq("%d%s × %s =" % (w, fr(n, d), sy), fs(ans), [fs(wrong) if wrong != ans else fs(ans + 2), fs(ans + 1), fs(ans + F(1, d * d2)), fs(ans - F(1, d * d2)) if ans > 1 else None],
                   "대분수를 가분수로 바꾸어 곱해요. %s × %s = <b>%s</b>" % (fi(X), fi(Y), fs(ans)))
    return mk


def fmul_story():
    k = R.choice(["part", "length", "of"])
    who = NM.next()
    if k == "of":
        d = R.choice([3, 4, 5, 6, 8, 10])
        n = R.randint(1, d - 1)
        tot = d * R.randint(3, 12)
        a = tot * n // d
        return mcq("우리 반 학생 %d명 중에서 %s는 안경을 썼어요. 안경을 쓴 학생은 몇 명인가요?" % (tot, fr(n, d)), "%d명" % a,
                   ["%d명" % x for x in (tot - a, tot // d, a + n)], "%d × %s = <b>%d명</b>" % (tot, fr(n, d), a))
    if k == "length":
        d = R.choice([2, 3, 4, 5, 6, 8])
        n = R.randint(1, d - 1)
        w = R.randint(2, 9)
        ans = F(n, d) * w
        return mcq("한 개의 길이가 %s m인 리본 %d개를 겹치지 않게 이었어요. 전체 길이는 몇 m인가요?" % (fr(n, d), w), "%s m" % fs(ans),
                   ["%s m" % fs(F(n, d * w)), "%s m" % fs(F(n + w, d)), "%s m" % fs(ans + 1)], "%s × %d = <b>%s m</b>" % (fr(n, d), w, fs(ans)))
    d, d2 = R.choice([2, 3, 4, 5]), R.choice([2, 3, 4, 5])
    n, n2 = R.randint(1, d - 1), R.randint(1, d2 - 1)
    ans = F(n, d) * F(n2, d2)
    return mcq("%s 주스 1 L의 %s를 마셨어요. 마신 주스의 %s는 사과 맛이었어요. 사과 맛 주스는 몇 L 마셨나요?" % (josa(who, "은/는"), fr(n, d), fr(n2, d2)),
               "%s L" % fs(ans), ["%s L" % fs(F(n, d) + F(n2, d2)), "%s L" % fs(F(n * n2, d + d2)), "%s L" % fs(abs(F(n, d) - F(n2, d2)) or ans + F(1, 2))],
               "%s × %s = <b>%s L</b>" % (fr(n, d), fr(n2, d2), fs(ans)))


# ---------------------------------------------------------------- 소수의 곱셈
def rdec(places, lo=1, hi=99):
    n = R.randint(lo, hi)
    if n % 10 == 0:
        return None
    return D(n).scaleb(-places)


def dmul(kind):
    def mk():
        if kind == "dw":
            a = rdec(R.choice([1, 2]), 2, 99)
            w = R.randint(2, 9)
            if a is None:
                return None
            ans = a * w
            k = -a.as_tuple().exponent
        elif kind == "dd1":
            a, b = rdec(1, 2, 99), rdec(1, 2, 9)
            if a is None or b is None:
                return None
            ans = a * b
            k = 2
        elif kind == "dd2":
            a, b = rdec(2, 101, 999), rdec(1, 2, 99)
            if a is None or b is None:
                return None
            ans = a * b
            k = 3
        else:    # 10, 100, 1000 곱하기
            a = rdec(R.choice([1, 2, 3]), 101, 9999)
            if a is None:
                return None
            w = R.choice([10, 100, 1000, D("0.1"), D("0.01")])
            ans = a * w
            return mcq("%s × %s =" % (dd(a), dd(w)), dd(ans), [dd(a * w * 10), dd(a * w / 10), dd(a * w * 100) if w >= 10 else dd(a * w / 100)],
                       "곱하는 수의 0의 개수(또는 소수점 아래 자리 수)만큼 소수점을 옮겨요. <b>%s</b>" % dd(ans))
        if kind == "dw":
            x, y = dd(a), str(w)
        else:
            x, y = dd(a), dd(b)
        raw = int(D(x.replace(".", "")) * D(y.replace(".", "")))
        return mcq("%s × %s =" % (x, y), dd(ans), [dd(ans * 10), dd(ans / 10), str(raw) if str(raw) != dd(ans) else dd(ans * 100)],
                   "자연수처럼 곱한 %d에서, 곱하는 두 수의 소수점 아래 자리 수만큼 소수점을 옮겨요. <b>%s</b>" % (raw, dd(ans)))
    return mk


def dmul_story():
    k = R.choice(["price", "len", "area"])
    if k == "price":
        p = R.choice([1200, 2500, 3000, 4800, 6000, 8500])
        kg = rdec(1, 11, 59)
        if kg is None:
            return None
        ans = D(p) * kg
        if ans != ans.to_integral():
            return None
        return mcq("1 kg에 %s원인 고기를 %s kg 샀어요. 고기값은 얼마인가요?" % (num(p), dd(kg)), "%s원" % num(int(ans)),
                   ["%s원" % num(int(ans * 10)), "%s원" % num(int(ans / 10)), "%s원" % num(p + int(kg * 10))], "%s × %s = <b>%s원</b>" % (num(p), dd(kg), num(int(ans))))
    if k == "len":
        a = rdec(2, 41, 89)
        w = R.randint(3, 9)
        if a is None:
            return None
        return mcq("한 걸음이 %s m인 걸음으로 %d걸음 걸었어요. 모두 몇 m를 걸었나요?" % (dd(a), w), "%s m" % dd(a * w),
                   ["%s m" % dd(a * w * 10), "%s m" % dd(a + w), "%s m" % dd(a * w / 10)], "%s × %d = <b>%s m</b>" % (dd(a), w, dd(a * w)))
    a, b = rdec(1, 11, 99), rdec(1, 11, 49)
    if a is None or b is None:
        return None
    return mcq("가로 %s m, 세로 %s m인 직사각형 모양 꽃밭의 넓이는 몇 m²인가요?" % (dd(a), dd(b)), "%s m²" % dd(a * b),
               ["%s m²" % dd((a + b) * 2), "%s m²" % dd(a * b * 10), "%s m²" % dd(a * b / 10)], "%s × %s = <b>%s m²</b>" % (dd(a), dd(b), dd(a * b)))


def dmul_point():
    a = R.randint(11, 99)
    b = R.randint(11, 99)
    p = a * b
    pa, pb = R.choice([(1, 1), (1, 2), (2, 1), (2, 2), (0, 2), (2, 0)])
    x, y = D(a).scaleb(-pa), D(b).scaleb(-pb)
    if (pa and a % 10 == 0) or (pb and b % 10 == 0):
        return None
    return mcq("%d × %d = %s 입니다. %s × %s의 값은?" % (a, b, num(p), dd(x), dd(y)), dd(x * y),
               [dd(x * y * 10), dd(x * y / 10), dd(x * y * 100)], "소수점 아래 자리 수가 모두 %d개이므로 <b>%s</b>" % (pa + pb, dd(x * y)))


def build(which):
    G = "grade-5"
    if which == "simplify":
        return unit(G, "simplifying-and-common-denominators", 5, "[6수01-06]",
                    "크기가 같은 분수를 만드는 방법을 이해하고, 분수를 약분, 통분할 수 있다.",
                    "크기가 같은 분수, 약분과 통분", "약분과 통분",
                    "초등 5학년 1학기 약분과 통분 학습지: 크기가 같은 분수 만들기, 기약분수로 나타내기, 분모의 곱과 최소공배수로 통분하기까지 100문제와 정답.",
                    "분모와 분자에 같은 수를 곱하거나 나눠요", "약분은 나누기, 통분은 분모를 같게",
                    ["분모와 분자에 0이 아닌 같은 수를 곱하거나 나누면 크기가 같은 분수가 돼요.",
                     "분모와 분자를 공약수로 나누어 간단히 하는 것을 <b>약분</b>, 더 이상 약분할 수 없는 분수를 <b>기약분수</b>라고 해요.",
                     "분모를 같게 하는 것을 <b>통분</b>, 그 분모를 <b>공통분모</b>라고 해요. 보통 두 분모의 최소공배수로 해요."],
                    [("<span class='fr'><span class='fn'>18</span><span class='fd'>24</span></span>를 기약분수로", ["18과 24의 최대공약수 6으로 나눠요."],
                      "<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>")],
                    [("분모에만 곱한다", "분모와 분자에 똑같이 곱해야 해요."),
                     ("분모와 분자에 같은 수를 더한다", "더하면 크기가 달라져요. 곱하거나 나눠야 해요."),
                     ("약분을 한 번만 하고 끝낸다", "최대공약수로 나누면 한 번에 기약분수가 돼요.")],
                    [("약분과 통분은 언제 배우나요?", "초등 5학년 1학기 「약분과 통분」 단원에서 배워요."),
                     ("공통분모는 꼭 최소공배수여야 하나요?", "두 분모의 공배수면 모두 공통분모가 될 수 있어요. 최소공배수가 계산이 가장 간단해요.")],
                    [("크기가 같은 분수", [(equiv, 20)]),
                     ("약분", [(reduce_q, 20)]),
                     ("기약분수", [(is_irr, 10), (reduce_q, 10)]),
                     ("통분", [(common_den, 20)]),
                     ("섞어서 연습", [(equiv, 6), (reduce_q, 7), (common_den, 7)])], 82504)
    if which == "compare":
        return unit(G, "comparing-fractions-and-decimals", 6, "[6수01-07] [6수01-12]",
                    "분모가 다른 분수의 크기를 비교하고 그 방법을 설명할 수 있다. 분수와 소수의 관계를 이해하고 크기를 비교하며 그 방법을 설명할 수 있다.",
                    "분수의 크기 비교, 분수와 소수", "분수와 소수의 크기 비교",
                    "초등 5학년 1학기 학습지: 분모가 다른 분수의 크기 비교(통분), 여러 분수 중 가장 큰 수, 분수를 소수로, 소수를 기약분수로, 분수와 소수의 크기 비교까지 100문제와 정답.",
                    "통분하거나 소수로 바꿔서 비교", "분모가 10, 100인 분수는 소수로 쉽게 바꿔요.",
                    ["분모가 다른 분수는 <b>통분</b>해서 분자의 크기를 비교해요.",
                     "분수를 소수로 바꿀 때는 분모를 10, 100, 1000으로 고쳐요.",
                     "분수와 소수를 비교할 때는 같은 형태로 바꾸어 비교해요."],
                    [("<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span>와 0.65 비교", ["3/5 = 6/10 = 0.6", "0.6 < 0.65"], "<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> &lt; 0.65")],
                    [("분모가 큰 분수가 더 크다고 생각한다", "분자가 같으면 분모가 작을수록 커요. 통분해서 비교해요."),
                     ("분자끼리만 비교한다", "분모가 다르면 먼저 통분해요."),
                     ("3/4을 0.34로 쓴다", "3/4 = 75/100 = 0.75")],
                    [("통분하지 않고 비교하는 방법도 있나요?", "분자를 같게 만들거나, 1/2과 비교하는 방법도 있어요."),
                     ("분수와 소수는 몇 학년에서 비교하나요?", "2022 개정 교육과정에서는 5~6학년군에서 배워요.")],
                    [("두 분수 비교", [(cmp2, 20)]),
                     ("여러 분수 비교", [(biggest, 20)]),
                     ("분수와 소수", [(f2d, 20)]),
                     ("분수와 소수의 크기 비교", [(fd_cmp, 20)]),
                     ("섞어서 연습", [(cmp2, 7), (biggest, 6), (f2d, 7)])], 82505)
    if which == "fadd":
        return unit(G, "adding-and-subtracting-fractions", 7, "[6수01-08]",
                    "분모가 다른 분수의 덧셈과 뺄셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                    "분모가 다른 분수의 덧셈과 뺄셈", "분수의 덧셈과 뺄셈",
                    "초등 5학년 1학기 학습지: 분모가 다른 진분수와 대분수의 덧셈과 뺄셈, 통분과 약분, 받아올림과 받아내림, 문장제까지 100문제와 정답.",
                    "통분한 뒤 분자끼리 계산", "답은 기약분수로 나타내요.",
                    ["분모가 다른 분수는 먼저 <b>통분</b>해서 분모를 같게 해요.",
                     "분모는 그대로 두고 분자끼리 더하거나 빼요. 답은 약분해서 기약분수로 나타내요.",
                     "대분수는 자연수끼리, 분수끼리 계산하거나 가분수로 바꾸어 계산해요."],
                    [("<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span> + <span class='fr'><span class='fn'>5</span><span class='fd'>6</span></span>",
                      ["통분: 3/12 + 10/12", "= 13/12 = 1 1/12"], "1<span class='fr'><span class='fn'>1</span><span class='fd'>12</span></span>")],
                    [("분모끼리, 분자끼리 더한다 (1/4 + 5/6 = 6/10)", "통분한 뒤 분자끼리만 더해요."),
                     ("통분할 때 분자에 곱하지 않는다", "분모에 곱한 수를 분자에도 곱해요."),
                     ("답을 약분하지 않는다", "기약분수로 나타내요.")],
                    [("분모의 곱과 최소공배수 중 무엇으로 통분하나요?", "어느 쪽이든 맞아요. 최소공배수로 하면 수가 작아 계산이 쉬워요."),
                     ("대분수 뺄셈에서 분수끼리 뺄 수 없으면?", "자연수에서 1을 받아내리거나 가분수로 바꾸어 계산해요.")],
                    [("진분수의 덧셈", [(fadd("add"), 20)]),
                     ("진분수의 뺄셈", [(fadd("sub"), 20)]),
                     ("대분수의 덧셈", [(fadd("mixadd"), 20)]),
                     ("대분수의 뺄셈", [(fadd("mixsub"), 20)]),
                     ("문장제", [(fadd_story, 20)])], 82506)
    if which == "fmul":
        return unit(G, "multiplying-fractions", 13, "[6수01-09]",
                    "분수의 곱셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                    "분수의 곱셈", "분수의 곱셈",
                    "초등 5학년 2학기 분수의 곱셈 학습지: (분수) × (자연수), (자연수) × (분수), 진분수의 곱셈, 단위분수의 곱셈, 대분수의 곱셈, 문장제까지 100문제와 정답.",
                    "분자끼리, 분모끼리 곱해요", "대분수는 가분수로 바꾸어 곱해요.",
                    ["(분수) × (자연수)는 분자와 자연수를 곱해요.",
                     "(분수) × (분수)는 <b>분자끼리, 분모끼리</b> 곱해요. 곱하기 전에 약분하면 계산이 쉬워요.",
                     "대분수가 있으면 <b>가분수</b>로 바꾸어 곱해요.",
                     "1보다 작은 수를 곱하면 결과는 처음 수보다 작아져요."],
                    [("1<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> × <span class='fr'><span class='fn'>4</span><span class='fd'>9</span></span>",
                      ["3/2 × 4/9", "약분하면 1/1 × 2/3"], "<span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span>")],
                    [("(분수) × (자연수)에서 분모에 곱한다", "분자에 곱해요. 2/5 × 3 = 6/5"),
                     ("대분수를 그대로 자연수끼리, 분수끼리 곱한다", "가분수로 바꾸어 곱해요."),
                     ("곱하면 항상 커진다고 생각한다", "진분수를 곱하면 작아져요.")],
                    [("분수의 곱셈은 언제 배우나요?", "초등 5학년 2학기 「분수의 곱셈」 단원에서 배워요."),
                     ("약분은 언제 하나요?", "곱하기 전에 분자와 분모를 약분하면 계산이 간단해요.")],
                    [("(분수) × (자연수)", [(fmul("fw"), 20)]),
                     ("(자연수) × (분수)", [(fmul("wf"), 20)]),
                     ("진분수의 곱셈", [(fmul("unit"), 8), (fmul("ff"), 12)]),
                     ("대분수의 곱셈", [(fmul("mixed"), 20)]),
                     ("문장제", [(fmul_story, 20)])], 82513)
    return unit(G, "multiplying-decimals", 16, "[6수01-13]",
                "소수의 곱셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                "소수의 곱셈", "소수의 곱셈",
                "초등 5학년 2학기 소수의 곱셈 학습지: (소수) × (자연수), (소수) × (소수), 10・100・1000과 0.1・0.01을 곱할 때 소수점 옮기기, 곱의 소수점 위치, 문장제까지 100문제와 정답.",
                "자연수처럼 곱하고 소수점을 찍어요", "소수점 아래 자리 수를 더한 만큼",
                ["소수의 곱셈은 먼저 <b>자연수처럼</b> 곱해요.",
                 "곱하는 두 수의 소수점 아래 자리 수를 더한 만큼 곱의 소수점 아래 자리가 생겨요.",
                 "10, 100, 1000을 곱하면 소수점이 오른쪽으로, 0.1, 0.01을 곱하면 왼쪽으로 옮겨져요."],
                [("2.4 × 1.3", ["24 × 13 = 312", "소수점 아래 자리 수 1 + 1 = 2", "3.12"], "3.12")],
                [("소수점을 한 수에만 맞춰 찍는다 (2.4 × 1.3 = 31.2)", "두 수의 자리 수를 더해 2자리: 3.12"),
                 ("곱셈에서도 소수점을 세로로 맞춘다", "덧셈과 달리 곱셈은 자연수처럼 오른쪽 끝을 맞춰 곱해요."),
                 ("0.1을 곱하면 커진다고 생각한다", "0.1을 곱하면 10분의 1이 돼요.")],
                [("소수의 곱셈은 언제 배우나요?", "초등 5학년 2학기 「소수의 곱셈」 단원에서 배워요."),
                 ("답이 맞는지 확인하는 방법은?", "어림해 보세요. 2.4 × 1.3은 약 2 × 1 = 2보다 조금 크니 3.12가 알맞아요.")],
                [("(소수) × (자연수)", [(dmul("dw"), 20)]),
                 ("(소수) × (소수)", [(dmul("dd1"), 20)]),
                 ("곱의 소수점의 위치", [(dmul("p10"), 12), (dmul_point, 8)]),
                 ("자리 수가 많은 소수", [(dmul("dd2"), 20)]),
                 ("문장제", [(dmul_story, 20)])], 82516)
