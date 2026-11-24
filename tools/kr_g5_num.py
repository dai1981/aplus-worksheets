# -*- coding: utf-8 -*-
"""
대한민국 초등 5학년 수학：자연수의 혼합 계산・약수와 배수・수의 범위와 어림하기
  order   : 자연수의 혼합 계산 [6수01-01]
  factors : 약수와 배수 [6수01-04] [6수01-05]
  gcflcm  : 최대공약수와 최소공배수 [6수01-04] [6수01-05]
  range   : 이상, 이하, 초과, 미만 [6수01-02]
  round   : 올림, 버림, 반올림 [6수01-03]
誤答は「앞에서부터 차례로 계산한다」「약수에 1과 자기 자신을 빼먹는다」「공약수를 최대공약수로 착각한다」「이상과 초과를 헷갈린다」「반올림할 자리를 잘못 본다」から作る。
"""
import math
import random
from kr_common import mcq, unit, Names, josa, num
from kr_pics56 import range_line

R = random.Random(82501)
NM = Names(R)


# ---------------------------------------------------------------- 혼합 계산
def ev(expr):
    return eval(expr.replace("×", "*").replace("÷", "//"))


def ltr(tokens):
    """앞에서부터 차례로 계산（よくある間違い）"""
    v = tokens[0]
    for op, x in zip(tokens[1::2], tokens[2::2]):
        if op == "+":
            v += x
        elif op == "−":
            v -= x
        elif op == "×":
            v *= x
        else:
            if x == 0 or v % x:
                return None
            v //= x
    return v


def mixed(kind):
    def mk():
        if kind == "as":       # 덧셈・뺄셈・괄호
            a, b, c = R.randint(20, 90), R.randint(5, 40), R.randint(5, 40)
            if b + c >= a:
                return None
            q = "%d − (%d + %d)" % (a, b, c)
            ans, wrong = a - b - c, a - b + c
            e = "괄호 안을 먼저 계산해요. %d + %d = %d, %d − %d = <b>%d</b>" % (b, c, b + c, a, b + c, ans)
        elif kind == "md":     # 곱셈・나눗셈
            b = R.randint(2, 9)
            c = R.randint(2, 9)
            a = b * c * R.randint(2, 6)
            q = "%d ÷ (%d × %d)" % (a, b, c)
            ans, wrong = a // (b * c), a // b * c
            e = "괄호 안을 먼저 계산해요. %d × %d = %d, %d ÷ %d = <b>%d</b>" % (b, c, b * c, a, b * c, ans)
        elif kind == "am":     # 덧셈・뺄셈・곱셈
            a, b, c = R.randint(10, 60), R.randint(2, 9), R.randint(2, 9)
            if R.random() < 0.5:
                q = "%d + %d × %d" % (a, b, c)
                ans, wrong = a + b * c, (a + b) * c
                e = "곱셈을 먼저 해요. %d × %d = %d, %d + %d = <b>%d</b>" % (b, c, b * c, a, b * c, ans)
            else:
                a = R.randint(b * c + 1, b * c + 60)
                q = "%d − %d × %d" % (a, b, c)
                ans, wrong = a - b * c, (a - b) * c
                e = "곱셈을 먼저 해요. %d × %d = %d, %d − %d = <b>%d</b>" % (b, c, b * c, a, b * c, ans)
        elif kind == "ad":     # 덧셈・뺄셈・나눗셈
            b, c = R.randint(2, 9), R.randint(2, 12)
            a = R.randint(10, 60)
            q = "%d + %d ÷ %d" % (a, b * c, b)
            ans, wrong = a + c, (a + b * c) // b if (a + b * c) % b == 0 else a + b * c - b
            e = "나눗셈을 먼저 해요. %d ÷ %d = %d, %d + %d = <b>%d</b>" % (b * c, b, c, a, c, ans)
        elif kind == "par":    # 괄호가 있는 곱셈
            a, b, c = R.randint(10, 40), R.randint(2, 20), R.randint(2, 9)
            if R.random() < 0.5:
                q = "(%d + %d) × %d" % (a, b, c)
                ans, wrong = (a + b) * c, a + b * c
                e = "괄호 안을 먼저 계산해요. %d + %d = %d, %d × %d = <b>%d</b>" % (a, b, a + b, a + b, c, ans)
            else:
                if b >= a:
                    return None
                q = "(%d − %d) × %d" % (a, b, c)
                ans, wrong = (a - b) * c, a - b * c
                e = "괄호 안을 먼저 계산해요. %d − %d = %d, %d × %d = <b>%d</b>" % (a, b, a - b, a - b, c, ans)
        else:                  # 다섯 가지 섞인 식
            b, c = R.randint(2, 6), R.randint(2, 9)
            d = R.randint(2, 5)
            a = R.randint(30, 80)
            inner = b * c
            f = R.randint(1, inner - 1)
            if (inner - f) % d:
                return None
            q = "%d + (%d × %d − %d) ÷ %d" % (a, b, c, f, d)
            ans = a + (inner - f) // d
            wrong = (a + inner - f) // d if (a + inner - f) % d == 0 else a + inner - f // d if f % d == 0 else a + inner - f
            e = "괄호 안의 곱셈 → 괄호 안의 뺄셈 → 나눗셈 → 덧셈 순서예요. %d × %d = %d, %d − %d = %d, %d ÷ %d = %d, %d + %d = <b>%d</b>" % (
                b, c, inner, inner, f, inner - f, inner - f, d, (inner - f) // d, a, (inner - f) // d, ans)
        if wrong == ans or wrong is None or wrong < 0:
            wrong = ans + 10
        return mcq(q + " =", num(ans), [num(wrong), num(ans + 1), num(ans - 1) if ans > 1 else num(ans + 2), num(ans + 10)], e)
    return mk


SHOP = [("연필", 600), ("지우개", 400), ("공책", 900), ("자", 700), ("볼펜", 800), ("색연필", 1200)]


def mixed_story():
    who = NM.next()
    k = R.choice(["buy", "share", "change"])
    if k == "buy":
        (a, pa), (b, pb) = R.sample(SHOP, 2)
        na, nb = R.randint(2, 5), R.randint(2, 5)
        m = R.choice([5000, 10000])
        tot = pa * na + pb * nb
        if tot >= m:
            return None
        return mcq("%s %s원짜리 %s %d개와 %s원짜리 %s %d개를 사고 %s원을 냈어요. 거스름돈은 얼마인가요?" % (josa(who, "은/는"), num(pa), a, na, num(pb), b, nb, num(m)),
                   "%s원" % num(m - tot), ["%s원" % num(x) for x in (m - pa - pb, m - (pa + pb) * na, m - tot + 100)],
                   "%s − (%s × %d + %s × %d) = <b>%s원</b>" % (num(m), num(pa), na, num(pb), nb, num(m - tot)))
    if k == "share":
        n = R.randint(3, 8)
        per = R.randint(3, 9)
        extra = R.randint(2, 9)
        tot = n * per
        return mcq("사탕 %d개를 친구 %d명이 똑같이 나누어 가졌어요. %s 자기 몫에 %d개를 더 받았다면 %s 가진 사탕은 몇 개인가요?" % (
                       tot, n, josa(who, "은/는"), extra, josa(who, "이/가")),
                   "%d개" % (per + extra), ["%d개" % x for x in ((tot + extra) // n if (tot + extra) % n == 0 else per + extra + 1, tot + extra, per)],
                   "%d ÷ %d + %d = %d + %d = <b>%d개</b>" % (tot, n, extra, per, extra, per + extra))
    p = R.choice([1200, 1500, 2000, 2400, 3000])
    k2 = R.choice([2, 3, 4])
    n = R.randint(2, 7)
    m = 10000
    tot = p // k2 * n
    if p % k2 or n == k2:
        return None
    return mcq("%d개에 %s원인 빵을 %d개 샀어요. %s원을 내면 거스름돈은 얼마인가요?" % (k2, num(p), n, num(m)), "%s원" % num(m - tot),
               ["%s원" % num(x) for x in (m - p * n, m - p // k2, m - tot - 100)],
               "빵 1개는 %s ÷ %d = %s원. %s − %s ÷ %d × %d = <b>%s원</b>" % (num(p), k2, num(p // k2), num(m), num(p), k2, n, num(m - tot)))


ORDER_FACTS = [("곱셈과 나눗셈이 섞인 식은 앞에서부터 차례로 계산해요.", "○"), ("덧셈과 곱셈이 섞인 식은 앞에서부터 차례로 계산해요.", "×"),
               ("( )가 있으면 ( ) 안을 가장 먼저 계산해요.", "○"), ("덧셈, 뺄셈, 곱셈이 섞인 식에서는 곱셈을 먼저 해요.", "○"),
               ("나눗셈보다 뺄셈을 먼저 계산해요.", "×")]


def order_step():
    a, b, c, d = R.randint(10, 50), R.randint(2, 9), R.randint(2, 9), R.randint(1, 9)
    q = "%d + %d × %d − %d" % (a, b, c, d)
    return mcq("%s 에서 가장 먼저 계산해야 하는 것은?" % q, "%d × %d" % (b, c), ["%d + %d" % (a, b), "%d − %d" % (c, d), "%d + %d" % (a, b * c)],
               "덧셈, 뺄셈, 곱셈이 섞여 있으면 <b>곱셈</b>을 먼저 계산해요.")


# ---------------------------------------------------------------- 약수와 배수
def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def dv_list():
    n = R.choice([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 72])
    ds = divisors(n)
    s = ", ".join(map(str, ds))
    w1 = ", ".join(map(str, ds[1:-1]))
    w2 = ", ".join(map(str, [d for d in ds if d % 2 == 0]))
    w3 = ", ".join(map(str, [n * k for k in range(1, 5)]))
    return mcq("%d의 약수를 모두 구한 것은?" % n, s, [w1, w2 if w2 != s else w1 + ", " + str(n), w3],
               "%d을 나누어떨어지게 하는 수를 모두 찾아요. 1과 자기 자신도 약수예요. <b>%s</b>" % (n, s))


def dv_count():
    n = R.randint(12, 99)
    k = len(divisors(n))
    return mcq("%d의 약수는 모두 몇 개인가요?" % n, "%d개" % k, ["%d개" % x for x in (k - 2, k + 1, k - 1 if k > 2 else k + 2)],
               "%d의 약수는 %s로 <b>%d개</b>예요." % (n, ", ".join(map(str, divisors(n))), k))


def dv_which():
    n = R.choice([24, 30, 36, 40, 42, 45, 48, 54, 56, 60, 72, 84, 90, 96])
    ds = divisors(n)
    good = R.choice([d for d in ds if 2 < d < n])
    bad = [x for x in range(3, n) if n % x and x not in ds]
    if R.random() < 0.5:
        b = R.choice(bad)
        return mcq("%d의 약수가 <b>아닌</b> 것은?" % n, str(b), [str(x) for x in R.sample([d for d in ds if 1 < d < n], 3)],
                   "%d ÷ %d은 나누어떨어지지 않아요. <b>%d</b>" % (n, b, b))
    return mcq("%d의 약수인 것은?" % n, str(good), [str(x) for x in R.sample(bad, 3)], "%d ÷ %d = %d로 나누어떨어져요. <b>%d</b>" % (n, good, n // good, good))


def mul_nth():
    n = R.randint(3, 25)
    k = R.randint(4, 15)
    if R.random() < 0.5:
        return mcq("%d의 배수 중에서 %d번째 수는?" % (n, k), num(n * k), [num(n * (k - 1)), num(n * (k + 1)), num(n + k)],
                   "%d의 배수는 %d × 1, %d × 2, …예요. %d번째 수는 %d × %d = <b>%s</b>" % (n, n, n, k, n, k, num(n * k)))
    lo, hi = R.randint(10, 60), None
    hi = lo + R.randint(20, 60)
    cnt = hi // n - (lo - 1) // n
    return mcq("%d부터 %d까지의 수 중에서 %d의 배수는 몇 개인가요?" % (lo, hi, n), "%d개" % cnt, ["%d개" % x for x in (hi // n, cnt + 1, cnt - 1 if cnt > 1 else cnt + 2)],
               "%d까지 %d개, %d까지 %d개이므로 %d − %d = <b>%d개</b>" % (hi, hi // n, lo - 1, (lo - 1) // n, hi // n, (lo - 1) // n, cnt))


def relation():
    a = R.randint(2, 12)
    k = R.randint(2, 9)
    b = a * k
    if k == a:
        return None
    if R.random() < 0.5:
        return mcq("%d = %d × %d 입니다. 옳은 것은?" % (b, a, k), "%d는 %d의 배수예요" % (b, a),
                   ["%d는 %d의 약수예요" % (b, a), "%d는 %d의 배수예요" % (a, b), "%d는 %d의 배수예요" % (k, b)],
                   "%d = %d × %d이면 %d는 %d와 %d의 배수이고, %d와 %d는 %d의 약수예요." % (b, a, k, b, a, k, a, k, b))
    c = R.randint(2, 12)
    if b % c == 0 or c == a:
        return None
    return mcq("두 수가 약수와 배수의 관계인 것은?", "%d, %d" % (a, b), ["%d, %d" % (c, b), "%d, %d" % (a, b + 1), "%d, %d" % (c, b + c + 1) if (b + c + 1) % c else "%d, %d" % (c, b + 2)],
               "큰 수가 작은 수로 나누어떨어지면 약수와 배수의 관계예요. %d ÷ %d = %d. <b>%d, %d</b>" % (b, a, k, a, b))


# ---------------------------------------------------------------- 최대공약수와 최소공배수
def pair(mx=60):
    while True:
        g = R.randint(2, 12)
        a, b = R.randint(2, 9), R.randint(2, 9)
        if math.gcd(a, b) == 1 and a != b and g * max(a, b) <= mx:
            return g * a, g * b


def gcf_q():
    x, y = pair(72)
    g = math.gcd(x, y)
    com = [d for d in divisors(g)]
    sec = com[-2] if len(com) > 1 else 1
    return mcq("%d과 %d의 최대공약수는?" % (x, y), str(g), [str(sec), str(x * y // g), str(min(x, y)) if min(x, y) != g else str(g * 2)],
               "두 수의 공약수 %s 중에서 가장 큰 수는 <b>%d</b>예요." % (", ".join(map(str, com)), g))


def lcm_q():
    x, y = pair(48)
    g = math.gcd(x, y)
    l = x * y // g
    return mcq("%d과 %d의 최소공배수는?" % (x, y), num(l), [num(x * y) if x * y != l else num(l * 2), num(g), num(l * 2)],
               "%d의 배수와 %d의 배수 중 가장 작은 공통인 수예요. %d × %d ÷ %d = <b>%s</b>" % (x, y, x, y, g, num(l)))


def common_div():
    x, y = pair(90)
    g = math.gcd(x, y)
    com = divisors(g)
    s = ", ".join(map(str, com))
    return mcq("%d과 %d의 공약수를 모두 구한 것은?" % (x, y), s, [", ".join(map(str, com[1:])) or "없어요", ", ".join(map(str, divisors(x)[:len(com) + 1])),
                                                       str(g)],
               "공약수는 최대공약수 %d의 약수와 같아요. <b>%s</b>" % (g, s))


def common_mul():
    x, y = pair(30)
    l = x * y // math.gcd(x, y)
    k = R.randint(2, 4)
    return mcq("%d과 %d의 공배수 중에서 %d번째로 작은 수는?" % (x, y, k), num(l * k), [num(x * y * k) if x * y != l else num(l * k + l), num(l * (k + 1)), num(l + k)],
               "공배수는 최소공배수 %s의 배수예요. %s × %d = <b>%s</b>" % (num(l), num(l), k, num(l * k)))


def gl_story():
    k = R.choice(["share", "meet", "square", "tile"])
    if k == "share":
        x, y = pair(60)
        g = math.gcd(x, y)
        return mcq("사과 %d개와 귤 %d개를 남김없이 최대한 많은 사람에게 똑같이 나누어 주려고 해요. 몇 명에게 나누어 줄 수 있나요?" % (x, y), "%d명" % g,
                   ["%d명" % v for v in (x * y // g, divisors(g)[-2] if g > 2 else g + 1, x + y)],
                   "똑같이 남김없이 → 공약수, 최대한 많이 → 최대공약수. <b>%d명</b>" % g)
    if k == "meet":
        x, y = R.sample([4, 6, 8, 9, 10, 12, 15], 2)
        l = x * y // math.gcd(x, y)
        return mcq("버스 가는 %d분마다, 버스 나는 %d분마다 출발해요. 오전 9시에 두 버스가 동시에 출발했다면, 다음에 동시에 출발하는 것은 몇 분 후인가요?" % (x, y),
                   "%d분 후" % l, ["%d분 후" % v for v in (x * y if x * y != l else l * 2, math.gcd(x, y), x + y)],
                   "두 수의 최소공배수를 구해요. <b>%d분 후</b>" % l)
    if k == "square":
        x, y = pair(40)
        l = x * y // math.gcd(x, y)
        return mcq("가로 %d cm, 세로 %d cm인 직사각형 종이를 겹치지 않게 늘어놓아 가장 작은 정사각형을 만들려고 해요. 정사각형의 한 변은 몇 cm인가요?" % (x, y),
                   "%d cm" % l, ["%d cm" % v for v in (math.gcd(x, y), x * y if x * y != l else l * 2, x + y)],
                   "한 변은 %d과 %d의 공배수여야 하고, 가장 작으니까 최소공배수예요. <b>%d cm</b>" % (x, y, l))
    x, y = pair(72)
    g = math.gcd(x, y)
    return mcq("가로 %d cm, 세로 %d cm인 직사각형을 크기가 같은 가장 큰 정사각형으로 남김없이 자르려고 해요. 정사각형의 한 변은 몇 cm인가요?" % (x, y),
               "%d cm" % g, ["%d cm" % v for v in (x * y // g, divisors(g)[-2] if g > 2 else g + 1, abs(x - y) if abs(x - y) != g else g + 2)],
               "한 변은 %d과 %d의 공약수여야 하고, 가장 크니까 최대공약수예요. <b>%d cm</b>" % (x, y, g))


def prime_way():
    x, y = pair(90)
    g = math.gcd(x, y)
    l = x * y // g
    if R.random() < 0.5:
        return mcq("%d = %d × %d, %d = %d × %d 일 때 %d과 %d의 최대공약수는?" % (x, g, x // g, y, g, y // g, x, y), str(g),
                   [str(l), str(x // g * y // g), str(g * 2)], "두 수에 공통으로 들어 있는 곱 %d가 최대공약수예요. <b>%d</b>" % (g, g))
    return mcq("%d = %d × %d, %d = %d × %d 일 때 %d과 %d의 최소공배수는?" % (x, g, x // g, y, g, y // g, x, y), num(l),
               [str(g), num(x * y), num(g * (x // g + y // g))], "%d × %d × %d = <b>%s</b>" % (g, x // g, y // g, num(l)))


# ---------------------------------------------------------------- 수의 범위
WORD = {"ge": "이상", "le": "이하", "gt": "초과", "lt": "미만"}


def rng_in():
    k = R.choice(list(WORD))
    a = R.randint(20, 80)
    if k == "ge":
        good = a + R.choice([0, 0, 1, 2, 4, 6])
        bads = [a - 1, a - 2, a - R.randint(3, 9)]
    elif k == "gt":
        good = a + R.randint(1, 6)
        bads = [a, a - 1, a - R.randint(2, 9)]
    elif k == "le":
        good = a - R.choice([0, 0, 1, 2, 4, 6])
        bads = [a + 1, a + 2, a + R.randint(3, 9)]
    else:
        good = a - R.randint(1, 6)
        bads = [a, a + 1, a + R.randint(2, 9)]
    desc = {"ge": "%d와 같거나 %d보다 큰 수", "le": "%d와 같거나 %d보다 작은 수", "gt": "%d보다 큰 수(%d는 포함하지 않아요)", "lt": "%d보다 작은 수(%d는 포함하지 않아요)"}[k] % (a, a)
    return mcq("%d %s인 수는?" % (a, WORD[k]), str(good), [str(b) for b in bads],
               "%d %s %s예요. <b>%d</b>" % (a, josa(WORD[k], "은/는"), desc, good))


def rng_count():
    a = R.randint(10, 40)
    b = a + R.randint(5, 20)
    ka, kb = R.choice(["ge", "gt"]), R.choice(["le", "lt"])
    lo = a if ka == "ge" else a + 1
    hi = b if kb == "le" else b - 1
    cnt = hi - lo + 1
    return mcq("%d %s %d %s인 자연수는 모두 몇 개인가요?" % (a, WORD[ka], b, WORD[kb]), "%d개" % cnt,
               ["%d개" % x for x in (b - a + 1, b - a - 1, b - a) if x != cnt],
               "%d부터 %d까지의 수예요. %d − %d + 1 = <b>%d개</b>" % (lo, hi, hi, lo, cnt))


def rng_line():
    lo = R.randint(1, 20)
    a = lo + R.randint(1, 3)
    b = a + R.randint(2, 4)
    ca, cb = R.random() < 0.5, R.random() < 0.5
    pic = range_line(lo, lo + 8, a, b, ca, cb)
    ans = "%d %s %d %s인 수" % (a, "이상" if ca else "초과", b, "이하" if cb else "미만")
    alts = ["%d %s %d %s인 수" % (a, x, b, y) for x in ("이상", "초과") for y in ("이하", "미만")]
    return mcq(pic + "수직선에 나타낸 수의 범위는?", ans, [x for x in alts if x != ans],
               "●은 그 수를 포함하고, ○은 포함하지 않아요. <b>%s</b>" % ans)


def rng_story():
    k = R.choice(["ride", "weight", "age"])
    if k == "ride":
        a = R.choice([110, 120, 130, 140])
        h = [a - R.randint(1, 9), a, a + R.randint(1, 15), a - R.randint(10, 20)]
        who = [NM.next() for _ in range(4)]
        if len(set(who)) < 4:
            return None
        can = [w for w, x in zip(who, h) if x >= a]
        q = "키가 %d cm 이상이어야 탈 수 있는 놀이 기구가 있어요. %s 탈 수 있는 사람을 모두 고르면?" % (
            a, " ".join("%s %d cm," % (w, x) for w, x in zip(who, h)).rstrip(",") + ".")
        ans = ", ".join(can)
        wrong = [", ".join([w for w, x in zip(who, h) if x > a]), ", ".join(who[:3]), ", ".join([w for w, x in zip(who, h) if x <= a])]
        return mcq(q, ans, wrong, "%d cm 이상은 %d cm도 포함해요. <b>%s</b>" % (a, a, ans))
    if k == "weight":
        lim = R.choice([2, 3, 5])
        w = lim + R.choice([0, 1, -1])
        fee = {True: "추가 요금이 있어요", False: "추가 요금이 없어요"}
        over = w > lim
        return mcq("무게가 %d kg 초과인 짐은 추가 요금을 내요. 무게가 %d kg인 짐은?" % (lim, w), fee[over], [fee[not over], "짐을 보낼 수 없어요", "요금을 낼 필요가 없어요" if over else "요금이 두 배예요"],
                   "%d kg 초과는 %d kg보다 무거운 것이에요. %d kg은 %s" % (lim, lim, w, "<b>추가 요금이 있어요</b>." if over else "<b>추가 요금이 없어요</b>."))
    a = R.randint(7, 12)
    ages = sorted(R.sample(range(5, 16), 5))
    cnt = len([x for x in ages if x < a])
    return mcq("%d세 미만은 어린이 요금이에요. 나이가 %s세인 사람 중에서 어린이 요금을 내는 사람은 몇 명인가요?" % (a, ", ".join(map(str, ages))), "%d명" % cnt,
               ["%d명" % x for x in (len([v for v in ages if v <= a]), cnt + 1, 5 - cnt) if x != cnt],
               "%d세 미만은 %d세를 포함하지 않아요. <b>%d명</b>" % (a, a, cnt))


# ---------------------------------------------------------------- 어림하기
PL = {10: "십의 자리", 100: "백의 자리", 1000: "천의 자리"}


def rd(n, p, how):
    if how == "up":
        return -(-n // p) * p
    if how == "down":
        return n // p * p
    return (n + p // 2) // p * p


HOW = {"up": "올림", "down": "버림", "half": "반올림"}


def round_q(how):
    def mk():
        p = R.choice([10, 100, 1000])
        n = R.randint(p + 1, p * 100 - 1)
        if n % p == 0 or len(str(n)) <= len(str(p)) - 1:
            return None
        ans = rd(n, p, how)
        others = [rd(n, p, h) for h in HOW if h != how]
        cands = [num(x) for x in others if x != ans] + [num(rd(n, p * 10 if p < 1000 else p // 10, how)), num(ans + p), num(ans - p) if ans > p else None]
        return mcq("%s를 %s하여 %s까지 나타내면?" % (num(n), HOW[how], PL[p]), num(ans), cands,
                   {"up": "%s 아래 수를 올려서 나타내요." % PL[p], "down": "%s 아래 수를 버려서 0으로 나타내요." % PL[p],
                    "half": "%s 바로 아래 숫자가 0〜4이면 버리고, 5〜9이면 올려요." % PL[p]}[how] + " <b>%s</b>" % num(ans))
    return mk


def round_story():
    k = R.choice(["box", "bill", "rope"])
    if k == "box":
        per = R.choice([10, 100])
        n = R.randint(per + 1, per * 9)
        if n % per == 0:
            return None
        return mcq("귤 %s개를 한 상자에 %d개씩 담아 모두 상자에 넣으려고 해요. 상자는 적어도 몇 개 필요한가요?" % (num(n), per), "%d개" % -(-n // per),
                   ["%d개" % x for x in (n // per, -(-n // per) + 1, (n + per // 2) // per if (n + per // 2) // per != -(-n // per) else n // per - 1)],
                   "남은 귤도 담아야 하니까 <b>올림</b>해요. <b>%d개</b>" % -(-n // per))
    if k == "bill":
        n = R.randint(1100, 9900)
        if n % 1000 == 0:
            return None
        return mcq("%s원짜리 물건을 1000원짜리 지폐로만 사려고 해요. 1000원짜리 지폐를 적어도 몇 장 내야 하나요?" % num(n), "%d장" % -(-n // 1000),
                   ["%d장" % x for x in (n // 1000, -(-n // 1000) + 1, (n + 500) // 1000 if (n + 500) // 1000 != -(-n // 1000) else n // 1000 - 1)],
                   "모자라면 살 수 없으니 <b>올림</b>해요. <b>%d장</b>" % -(-n // 1000))
    n = R.randint(110, 990)
    if n % 100 == 0:
        return None
    return mcq("끈 %d cm를 100 cm씩 잘라 리본을 만들려고 해요. 리본은 최대 몇 개 만들 수 있나요?" % n, "%d개" % (n // 100),
               ["%d개" % x for x in (-(-n // 100), n // 100 - 1 if n // 100 > 1 else n // 100 + 2, n // 10)],
               "100 cm가 안 되는 나머지로는 리본을 만들 수 없으니 <b>버림</b>해요. <b>%d개</b>" % (n // 100))


def round_range():
    p = R.choice([10, 100])
    v = R.randint(2, 9) * p
    lo, hi = v - p // 2, v + p // 2
    ans = "%s 이상 %s 미만" % (num(lo), num(hi))
    return mcq("반올림하여 %s까지 나타내면 %s이 되는 자연수의 범위는?" % (PL[p], num(v)), ans,
               ["%s 이상 %s 이하" % (num(lo), num(hi)), "%s 초과 %s 미만" % (num(lo), num(hi)), "%s 이상 %s 미만" % (num(v - p), num(v))],
               "%s 이상 %s 미만인 수가 반올림하면 %s이 돼요. <b>%s</b>" % (num(lo), num(hi), num(v), ans))


def build(which):
    G = "grade-5"
    if which == "order":
        return unit(G, "order-of-operations", 1, "[6수01-01]",
                    "덧셈, 뺄셈, 곱셈, 나눗셈의 혼합 계산에서 계산하는 순서를 알고, 혼합 계산을 할 수 있다.",
                    "자연수의 혼합 계산", "혼합 계산",
                    "초등 5학년 1학기 자연수의 혼합 계산 학습지: 덧셈・뺄셈・곱셈・나눗셈과 괄호가 섞인 식의 계산 순서, 하나의 식으로 나타내 푸는 문장제까지 100문제와 정답.",
                    "( ) → ×, ÷ → +, − 순서", "같은 순위끼리는 앞에서부터 계산해요.",
                    ["<b>( )</b>가 있으면 ( ) 안을 가장 먼저 계산해요.",
                     "곱셈과 나눗셈은 덧셈과 뺄셈보다 <b>먼저</b> 계산해요.",
                     "덧셈과 뺄셈끼리, 곱셈과 나눗셈끼리는 <b>앞에서부터</b> 차례로 계산해요.",
                     "문장제는 하나의 식으로 쓴 뒤에 순서대로 계산해요."],
                    [("40 + (18 × 3 − 6) ÷ 4", ["18 × 3 = 54", "54 − 6 = 48", "48 ÷ 4 = 12", "40 + 12 = 52"], "52")],
                    [("20 + 5 × 3을 25 × 3 = 75로 계산한다", "곱셈을 먼저 해요. 20 + 15 = 35"),
                     ("( )를 무시하고 계산한다", "( ) 안을 가장 먼저 계산해요."),
                     ("48 ÷ 4 × 2를 48 ÷ 8로 계산한다", "곱셈과 나눗셈은 앞에서부터: 12 × 2 = 24")],
                    [("혼합 계산은 몇 학년에서 배우나요?", "2022 개정 교육과정에서는 초등 5학년 1학기 첫 단원에서 배워요."),
                     ("계산 순서를 쉽게 기억하는 방법은?", "괄호 → 곱셈・나눗셈 → 덧셈・뺄셈. 식에서 먼저 할 곳에 밑줄을 그어 보세요.")],
                    [("덧셈・뺄셈과 괄호", [(mixed("as"), 10), (order_step, 10)]),
                     ("곱셈・나눗셈과 괄호", [(mixed("md"), 10), (mixed("par"), 10)]),
                     ("덧셈・뺄셈・곱셈", [(mixed("am"), 20)]),
                     ("덧셈・뺄셈・나눗셈", [(mixed("ad"), 12), (mixed("all"), 8)]),
                     ("문장제", [(mixed_story, 20)])], 82501)
    if which == "factors":
        return unit(G, "factors-and-multiples", 2, "[6수01-04] [6수01-05]",
                    "약수, 공약수, 최대공약수를 이해하고 구할 수 있다. 배수, 공배수, 최소공배수를 이해하고 구할 수 있다.",
                    "약수와 배수", "약수와 배수",
                    "초등 5학년 1학기 약수와 배수 학습지: 약수 구하기, 약수의 개수, 배수 구하기, 몇 번째 배수, 약수와 배수의 관계까지 100문제와 정답.",
                    "나누어떨어지게 하는 수가 약수", "몇 배 한 수가 배수",
                    ["어떤 수를 나누어떨어지게 하는 수를 그 수의 <b>약수</b>라고 해요. 1과 자기 자신은 항상 약수예요.",
                     "어떤 수를 1배, 2배, 3배, … 한 수를 그 수의 <b>배수</b>라고 해요.",
                     "12 = 3 × 4이면 12는 3과 4의 배수이고, 3과 4는 12의 약수예요."],
                    [("18의 약수를 모두 구하세요.", ["1 × 18, 2 × 9, 3 × 6", "곱해서 18이 되는 두 수를 찾아요."], "1, 2, 3, 6, 9, 18")],
                    [("1과 자기 자신을 빼먹는다", "1과 그 수 자신도 약수예요."),
                     ("약수와 배수를 반대로 말한다", "작은 수가 약수, 큰 수가 배수예요."),
                     ("배수를 셀 때 0부터 센다", "첫 번째 배수는 자기 자신이에요.")],
                    [("약수와 배수는 언제 배우나요?", "초등 5학년 1학기에 배워요. 다음 단원 약분과 통분의 기초가 돼요."),
                     ("약수를 빠짐없이 찾는 방법은?", "곱해서 그 수가 되는 두 수를 작은 수부터 짝지어 찾아요.")],
                    [("약수 구하기", [(dv_list, 12), (dv_which, 8)]),
                     ("약수의 개수", [(dv_count, 20)]),
                     ("배수", [(mul_nth, 20)]),
                     ("약수와 배수의 관계", [(relation, 20)]),
                     ("섞어서 연습", [(dv_which, 8), (mul_nth, 6), (relation, 6)])], 82502)
    if which == "gcflcm":
        return unit(G, "gcf-and-lcm", 3, "[6수01-04] [6수01-05]",
                    "약수, 공약수, 최대공약수를 이해하고 구할 수 있다. 배수, 공배수, 최소공배수를 이해하고 구할 수 있다.",
                    "최대공약수와 최소공배수", "최대공약수와 최소공배수",
                    "초등 5학년 1학기 학습지: 공약수와 최대공약수, 공배수와 최소공배수 구하기, 곱셈식으로 구하기, 나누어 주기・동시에 출발하기 문장제까지 100문제와 정답.",
                    "공약수 중 가장 큰 수, 공배수 중 가장 작은 수", "공약수는 최대공약수의 약수예요.",
                    ["두 수의 공통인 약수를 <b>공약수</b>, 그중 가장 큰 수를 <b>최대공약수</b>라고 해요.",
                     "두 수의 공통인 배수를 <b>공배수</b>, 그중 가장 작은 수를 <b>최소공배수</b>라고 해요.",
                     "공약수는 최대공약수의 약수이고, 공배수는 최소공배수의 배수예요.",
                     "똑같이 나누어 주기 → 최대공약수, 동시에 다시 만나기 → 최소공배수."],
                    [("12와 18의 최대공약수와 최소공배수", ["12 = 6 × 2, 18 = 6 × 3", "최대공약수 6", "최소공배수 6 × 2 × 3 = 36"], "6, 36")],
                    [("공약수 중 아무거나 최대공약수라고 한다", "가장 큰 공약수를 찾아요."),
                     ("최소공배수를 두 수의 곱으로 쓴다", "12와 18의 곱 216은 공배수지만 가장 작지 않아요. 36"),
                     ("문장제에서 최대공약수와 최소공배수를 바꿔 쓴다", "나누기는 최대공약수, 만나기는 최소공배수예요.")],
                    [("최대공약수를 빨리 구하는 방법은?", "두 수를 공통으로 나누는 수로 계속 나누고, 나눈 수를 곱해요."),
                     ("최소공배수는 왜 필요한가요?", "분모가 다른 분수를 통분할 때 공통분모로 써요.")],
                    [("공약수와 최대공약수", [(common_div, 8), (gcf_q, 12)]),
                     ("공배수와 최소공배수", [(common_mul, 8), (lcm_q, 12)]),
                     ("곱셈식으로 구하기", [(prime_way, 20)]),
                     ("섞어서 연습", [(gcf_q, 10), (lcm_q, 10)]),
                     ("문장제", [(gl_story, 20)])], 82503)
    if which == "range":
        return unit(G, "range-of-numbers", 11, "[6수01-02]",
                    "실생활과 연결하여 이상, 이하, 초과, 미만의 의미와 쓰임을 알고, 이를 활용하여 수의 범위를 나타낼 수 있다.",
                    "수의 범위: 이상, 이하, 초과, 미만", "수의 범위",
                    "초등 5학년 2학기 수의 범위 학습지: 이상, 이하, 초과, 미만의 뜻, 수직선에 나타내기, 범위에 있는 자연수의 개수, 놀이 기구와 요금 문장제까지 100문제와 정답.",
                    "이상・이하는 포함, 초과・미만은 포함 안 함", "수직선에서 ●은 포함, ○은 포함하지 않음",
                    ["10 <b>이상</b>은 10과 같거나 큰 수, 10 <b>이하</b>는 10과 같거나 작은 수예요.",
                     "10 <b>초과</b>는 10보다 큰 수, 10 <b>미만</b>은 10보다 작은 수예요. 10은 들어가지 않아요.",
                     "수직선에서 ●은 그 수를 포함하고, ○은 포함하지 않아요."],
                    [("15 초과 20 이하인 자연수는?", ["15는 빼고 20은 넣어요."], "16, 17, 18, 19, 20 (5개)")],
                    [("초과에 경계의 수를 넣는다", "15 초과에 15는 들어가지 않아요."),
                     ("이하와 미만을 헷갈린다", "이하는 그 수를 포함, 미만은 포함하지 않아요."),
                     ("범위의 개수를 두 수의 차로 쓴다", "양 끝이 포함되는지 보고 세어요.")],
                    [("이상, 이하는 언제 배우나요?", "초등 5학년 2학기 「수의 범위와 어림하기」 단원에서 배워요."),
                     ("생활에서 어디에 쓰나요?", "놀이 기구 키 제한, 요금표, 체급 등에서 써요.")],
                    [("이상과 이하", [(rng_in, 20)]),
                     ("수직선에 나타내기", [(rng_line, 20)]),
                     ("자연수의 개수", [(rng_count, 20)]),
                     ("섞어서 연습", [(rng_in, 10), (rng_line, 10)]),
                     ("생활 속 수의 범위", [(rng_story, 20)])], 82511)
    return unit(G, "rounding-up-down-and-off", 12, "[6수01-03]",
                "어림값을 구하기 위한 방법으로 올림, 버림, 반올림의 의미와 필요성을 알고, 이를 실생활에 활용함으로써 수학의 유용성을 인식할 수 있다.",
                "어림하기: 올림, 버림, 반올림", "올림, 버림, 반올림",
                "초등 5학년 2학기 어림하기 학습지: 올림, 버림, 반올림으로 십・백・천의 자리까지 나타내기, 반올림한 수의 범위, 상자와 지폐 문장제까지 100문제와 정답.",
                "어느 자리까지 나타낼지 먼저 봐요", "반올림은 바로 아래 자리가 5 이상이면 올려요.",
                ["<b>올림</b>: 구하려는 자리 아래 수를 올려서 나타내요. 532 → 600 (백의 자리)",
                 "<b>버림</b>: 구하려는 자리 아래 수를 버려서 나타내요. 587 → 500 (백의 자리)",
                 "<b>반올림</b>: 구하려는 자리 바로 아래 숫자가 0〜4이면 버리고, 5〜9이면 올려요.",
                 "모두 담아야 하면 올림, 다 채운 것만 세면 버림을 써요."],
                [("3472를 반올림하여 백의 자리까지", ["백의 자리 바로 아래 숫자는 7", "7은 5 이상 → 올려요."], "3500")],
                [("올림할 때 아래 자리가 0이 아닌데 그대로 둔다", "아래 자리에 0이 아닌 수가 있으면 올려요."),
                 ("반올림에서 맨 끝 숫자를 본다", "구하려는 자리의 바로 아래 숫자만 봐요."),
                 ("상자 수를 버림으로 구한다", "남는 물건도 담아야 하니까 올림해요.")],
                [("올림, 버림, 반올림은 언제 배우나요?", "초등 5학년 2학기 「수의 범위와 어림하기」 단원에서 배워요."),
                 ("어떤 상황에서 무엇을 쓰나요?", "모자라면 안 될 때 올림, 다 채운 것만 셀 때 버림, 가까운 값을 구할 때 반올림을 써요.")],
                [("올림", [(round_q("up"), 20)]),
                 ("버림", [(round_q("down"), 20)]),
                 ("반올림", [(round_q("half"), 20)]),
                 ("반올림한 수의 범위", [(round_range, 8), (round_q("half"), 6), (round_q("up"), 6)]),
                 ("생활 속 어림하기", [(round_story, 20)])], 82512)
