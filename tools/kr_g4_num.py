# -*- coding: utf-8 -*-
"""
대한민국 초등 4학년 수학：수와 연산・변화와 관계 の 6 単元
  large    : 큰 수（만, 십만, 백만, 천만, 억, 조）[4수01-01]
  compare  : 큰 수의 뛰어 세기와 크기 비교 [4수01-02]
  mul      : (세 자리 수) × (두 자리 수) [4수01-04]
  div      : 나누는 수가 두 자리 수인 나눗셈 [4수01-07]
  patterns : 규칙 찾기（수의 배열・도형의 배열・계산식의 배열）[4수02-01] [4수02-02]
  equal    : 등호를 사용한 식 [4수02-03]
誤答は「자리를 하나 틀리게 센다」「만 단위로 끊지 않고 읽는다」「(×십)の 0 を落とす」「몫を一桁間違える」から作る。
"""
import random
from kr_common import mcq, num, unit, Names, josa, read_num
from kr_pics import fig, svg_wrap, text, line, INK, LIGHT, GREEN

R = random.Random(82401)
NM = Names(R)
PLACES = [(1, "일"), (10, "십"), (100, "백"), (1000, "천"), (10 ** 4, "만"), (10 ** 5, "십만"), (10 ** 6, "백만"), (10 ** 7, "천만"),
          (10 ** 8, "억"), (10 ** 9, "십억"), (10 ** 10, "백억"), (10 ** 11, "천억"), (10 ** 12, "조"), (10 ** 13, "십조")]


def mixed(n):
    """3억 2500만 처럼 만・억・조 단위로（숫자＋한글 단위）"""
    parts = []
    for big, u in ((10 ** 12, "조"), (10 ** 8, "억"), (10 ** 4, "만"), (1, "")):
        q = n // big % 10000
        if q:
            parts.append("%d%s" % (q, u))
    return " ".join(parts)


def big_number(lo_digits, hi_digits, zeros=True):
    d = R.randint(lo_digits, hi_digits)
    s = str(R.randint(1, 9)) + "".join(str(R.choice([0, 0, R.randint(1, 9)]) if zeros else R.randint(1, 9)) for _ in range(d - 1))
    return int(s)


# ---------------------------------------------------------------- 큰 수
def read_q():
    n = big_number(5, 13)
    if R.random() < 0.5:
        w = read_num(n * 10), read_num(n // 10) if n // 10 >= 10000 else read_num(n * 100), read_num(n + 10 ** (len(str(n)) - 2))
        return mcq("%s을 읽으면?" % num(n), read_num(n), list(w),
                   "오른쪽에서부터 네 자리씩 끊어 만, 억, 조를 붙여 읽어요. <b>%s</b>" % read_num(n))
    w = [num(n * 10), num(n // 10), num(n + 10 ** (len(str(n)) - 1)) if len(str(n)) < 14 else num(n - 10 ** (len(str(n)) - 2))]
    return mcq("「%s」%s 수로 쓰면?" % (read_num(n), josa(read_num(n), "을/를")[len(read_num(n)):]), num(n), w, "네 자리씩 끊어 생각해요. %s = <b>%s</b>" % (mixed(n), num(n)))


def place_q():
    n = big_number(6, 13, zeros=False)
    s = str(n)
    i = R.randrange(len(s) - 1)
    p = len(s) - 1 - i
    digit = int(s[i])
    val = digit * 10 ** p
    name = dict((b, u) for b, u in PLACES)[10 ** p]
    if R.random() < 0.5:
        others = [u for b, u in PLACES if b != 10 ** p and b <= 10 ** (len(s) - 1)]
        near = [dict(PLACES).get(10 ** (p + 1)), dict(PLACES).get(10 ** (p - 1)) if p else None, dict(PLACES).get(10 ** (p + 4))]
        return mcq("%s에서 숫자 %d은 어느 자리 숫자인가요? (왼쪽에서 %d번째)" % (num(n), digit, i + 1), "%s의 자리" % name,
                   ["%s의 자리" % u for u in near + others if u],
                   "오른쪽에서부터 일, 십, 백, 천, 만, … 순서로 세어요. <b>%s의 자리</b>" % name)
    return mcq("%s에서 왼쪽에서 %d번째 숫자 %d이 나타내는 값은?" % (num(n), i + 1, digit), num(val),
               [num(val * 10), num(val // 10) if val >= 10 else num(val * 100), str(digit), num(val * 10000)],
               "%d은 %s의 자리 숫자이므로 <b>%s</b>을 나타내요." % (digit, name, num(val)))


def unit_q():
    k = R.choice(["man", "eok", "jo"])
    if k == "man":
        a = R.choice([9000, 9900, 9990, 9999])
        b = 10000 - a
        return mcq("10000은 %s보다 몇만큼 더 큰 수인가요?" % num(a), num(b), [num(b * 10), num(b + 1), num(10 - b % 10 if b < 10 else b // 10)],
                   "10000 − %s = <b>%s</b>" % (num(a), num(b)))
    if k == "eok":
        m = R.choice([10, 100, 1000])
        return mcq("1억은 %s만의 몇 배인가요?" % num(10000 // m), "%d배" % m, ["%d배" % x for x in (m * 10, m // 10 if m > 10 else 1000, 10000)],
                   "1억 = 10000만이에요. 10000만 ÷ %s만 = <b>%d배</b>" % (num(10000 // m), m))
    n = R.randint(2, 9)
    c = R.choice(["억", "조"])
    if c == "억":
        return mcq("1000억이 %d개인 수는?" % (n * 10), "%d조" % n, ["%d조" % (n * 10), "%d000억" % n, "%d억" % (n * 10)],
                   "1000억이 10개이면 1조예요. 1000억이 %d개이면 <b>%d조</b>" % (n * 10, n))
    return mcq("1만이 %d개인 수는?" % (n * 10000), "%d억" % n, ["%d천만" % n, "%d조" % n, "%d억" % (n * 10)],
               "1만이 10000개이면 1억이에요. <b>%d억</b>" % n)


def count_q():
    """만 원짜리・천 원짜리 지폐 세기"""
    a, b, c = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
    total = a * 10000 + b * 1000 + c * 100
    who = NM.next()
    return mcq("%s 만 원짜리 지폐 %d장, 천 원짜리 지폐 %d장, 백 원짜리 동전 %d개를 가지고 있어요. 모두 얼마인가요?" % (josa(who, "은/는"), a, b, c),
               "%s원" % num(total), ["%s원" % num(x) for x in (a * 1000 + b * 100 + c * 10, total + 10000, a * 10000 + b * 100 + c * 1000, total + 1000) if x != total],
               "%s + %s + %s = <b>%s원</b>" % (num(a * 10000), num(b * 1000), num(c * 100), num(total)))


# ---------------------------------------------------------------- 뛰어 세기, 비교
def skip_q():
    step = R.choice([10 ** k for k in range(4, 12)])
    start = big_number(6, 12) // step * step + R.randint(1, 9) * (step // 10 if step >= 10 else 1)
    seq = [start + step * i for i in range(5)]
    hide = R.randrange(1, 5)
    show = [num(x) if i != hide else "□" for i, x in enumerate(seq)]
    ans = seq[hide]
    sname = mixed(step)
    return mcq("%s씩 뛰어 세었어요. □에 알맞은 수는?<br>%s" % (sname, ", ".join(show)), num(ans),
               [num(ans + step), num(ans - step // 10), num(ans + step * 10), num(ans - step * 10) if ans > step * 10 else num(ans + step // 10)],
               "%s씩 뛰어 세면 %s의 자리 숫자가 1씩 커져요. <b>%s</b>" % (sname, dict(PLACES)[step], num(ans)))


def cmp_q():
    a = big_number(6, 12, zeros=False)
    k = R.choice(["digits", "same"])
    if k == "digits":
        b = big_number(len(str(a)) - 1, len(str(a)) - 1, zeros=False)
        b = int(str(9) + str(b)[1:]) if len(str(b)) > 1 else b
    else:
        s = list(str(a))
        i = R.randrange(1, len(s))
        s[i] = str((int(s[i]) + R.choice([1, 2, 3, 7, 8])) % 10)
        b = int("".join(s))
    if a == b:
        return None
    big = max(a, b)
    return mcq("더 큰 수는? %s, %s" % (num(a), num(b)), num(big), [num(min(a, b)), "두 수가 같아요", "알 수 없어요"],
               ("자리 수가 많은 쪽이 더 커요." if len(str(a)) != len(str(b)) else "자리 수가 같으면 높은 자리부터 차례로 비교해요.") + " <b>%s</b>" % num(big))


def cmp_mixed():
    n = R.randint(1, 999) * 10 ** 8 + R.randint(1, 9999) * 10 ** 4
    m = n + R.choice([-1, 1]) * R.randint(1, 9) * 10 ** R.randint(5, 8)
    if m <= 0 or m == n:
        return None
    a, b = mixed(n), num(m)
    big = a if n > m else b
    return mcq("더 큰 수는? %s, %s" % (a, b), big, [b if big == a else a, "두 수가 같아요", "알 수 없어요"],
               "%s 수로 쓰면 %s예요. 높은 자리부터 비교해요. <b>%s</b>" % (josa(a, "을/를"), num(n), big))


def times10():
    n = R.randint(12, 980) * 10000
    k = R.choice([10, 100, 1000])
    t = "10배" if k == 10 else ("100배" if k == 100 else "1000배")
    return mcq("%s의 %s인 수는?" % (num(n), t), num(n * k), [num(n * k * 10), num(n * k // 10), num(n + k)],
               "10배 할 때마다 0이 하나씩 늘어요. <b>%s</b>" % num(n * k))


# ---------------------------------------------------------------- (세 자리 수) × (두 자리 수)
def mul_q(kind):
    def mk():
        if kind == "h0":
            a, b = R.randint(1, 9) * 100, R.randint(2, 9) * 10
        elif kind == "x0":
            a, b = R.randint(112, 989), R.randint(2, 9) * 10
        else:
            a, b = R.randint(112, 989), R.randint(12, 98)
            if b % 10 == 0:
                return None
        p = a * b
        bt, bo = b // 10, b % 10
        w = [p // 10, p + 1000, p - 100, a * bo + a * bt if bo else p * 10, p + 10]
        e = ("%d × %d = %s, %d × %d = %s, 더하면 <b>%s</b>" % (a, bo, num(a * bo), a, bt * 10, num(a * bt * 10), num(p)) if bo
             else "%d × %d = %s에 0을 하나 붙여요. <b>%s</b>" % (a, bt, num(a * bt), num(p)))
        return mcq("%d × %d =" % (a, b), num(p), [num(x) for x in w if x != p and x > 0], e)
    return mk


def mul_story():
    a, b = R.randint(120, 950), R.randint(12, 60)
    t, u = R.choice([("한 상자에 %d개씩 들어 있는 과자가 %d상자 있어요. 과자는 모두 몇 개인가요?", "개"),
                     ("한 권에 %d원인 공책을 %d권 사려면 모두 얼마가 필요한가요?", "원"),
                     ("하루에 %d m씩 %d일 동안 걸었어요. 모두 몇 m를 걸었나요?", " m"),
                     ("한 대에 %d kg인 짐을 %d대의 수레에 실었어요. 짐은 모두 몇 kg인가요?", " kg"),
                     ("한 상자에 %d장씩 들어 있는 색종이가 %d상자 있어요. 색종이는 모두 몇 장인가요?", "장")])
    if "과자" in t:
        a = R.randint(120, 300)
    if u == "원":
        a = a // 10 * 10
    p = a * b
    return mcq(t % (a, b), "%s%s" % (num(p), u), ["%s%s" % (num(x), u) for x in (p // 10, a + b, p + 1000, p - 100)],
               "%d × %d = <b>%s</b>(%s)" % (a, b, num(p), u.strip()))


# ---------------------------------------------------------------- 나누는 수가 두 자리 수
def qr(q, r):
    return "%d … %d" % (q, r) if r else str(q)


def div_q(kind):
    def mk():
        d = R.randint(11, 59) if kind != "tens" else R.randint(2, 9) * 10
        q = R.randint(2, 9) if kind in ("tens", "one") else R.randint(11, 49)
        r = R.randint(0, d - 1) if kind != "exact" else 0
        if kind == "exact":
            q = R.randint(2, 39)
        n = d * q + r
        if n >= 1000:
            return None
        ans = qr(q, r)
        w = [qr(q + 1, r) if r < d else qr(q + 1, 0), qr(q - 1, r + d), qr(q, r + 1) if r + 1 < d else qr(q, r - 1 if r else 1), qr(q * 10, r) if q < 10 else qr(q // 10, r)]
        return mcq("%d ÷ %d =" % (n, d), ans, [x for x in w if x != ans],
                   "%d에 몫을 어림해서 곱해 봐요. %d × %d = %d%s. 나머지는 나누는 수 %d보다 작아야 해요. <b>%s</b>" % (d, d, q, d * q, (", %d − %d = %d" % (n, d * q, r)) if r else "", d, ans))
    return mk


def div_story():
    d = R.randint(12, 45)
    q = R.randint(3, 25)
    r = R.randint(1, d - 1)
    n = d * q + r
    if n >= 1000:
        return None
    k = R.choice(["box", "left", "bus"])
    if k == "box":
        t = "귤 %d개를 한 상자에 %d개씩 담으려고 해요. 몇 상자가 되고, 몇 개가 남나요?" % (n, d)
        ans, w = "%d상자, %d개 남아요" % (q, r), ["%d상자, %d개 남아요" % (q + 1, r), "%d상자, %d개 남아요" % (r, q), "%d상자, %d개 남아요" % (q - 1, r + d)]
    elif k == "left":
        t = "색종이 %d장을 학생 %d명에게 똑같이 나누어 주면 한 명에게 몇 장씩 주고 몇 장이 남나요?" % (n, d)
        ans, w = "%d장씩, %d장 남아요" % (q, r), ["%d장씩, %d장 남아요" % (q + 1, r), "%d장씩, %d장 남아요" % (r, q), "%d장씩, %d장 남아요" % (q, r + 1) if r + 1 < d else "%d장씩, %d장 남아요" % (q, r - 1)]
    else:
        t = "학생 %d명이 한 대에 %d명씩 탈 수 있는 버스를 타려고 해요. 버스는 적어도 몇 대 필요한가요?" % (n, d)
        ans, w = "%d대" % (q + 1), ["%d대" % q, "%d대" % r, "%d대" % (q + 2)]
    return mcq(t, ans, w, "%d ÷ %d = %d … %d예요. <b>%s</b>" % (n, d, q, r, ans))


def div_check():
    d, q = R.randint(12, 48), R.randint(3, 30)
    r = R.randint(1, d - 1)
    n = d * q + r
    if R.random() < 0.5:
        return mcq("%d ÷ %d = %d … %d를 바르게 확인한 식은?" % (n, d, q, r), "%d × %d + %d = %d" % (d, q, r, n),
                   ["%d × %d − %d = %d" % (d, q, r, d * q - r), "%d × %d + %d = %d" % (d, r, q, d * r + q), "%d × %d = %d" % (d, q, d * q)],
                   "나누는 수 × 몫 + 나머지 = 나누어지는 수예요.")
    return mcq("어떤 수를 %d로 나누었을 때 나올 수 있는 나머지 중 가장 큰 수는?" % d, str(d - 1), [str(d), str(d + 1), str(d - 2)],
               "나머지는 나누는 수 %d보다 작아야 해요. <b>%d</b>" % (d, d - 1))


# ---------------------------------------------------------------- 규칙 찾기
def seq_q():
    k = R.choice(["add", "sub", "mul", "two"])
    a = R.randint(100, 5000)
    if k == "add":
        d = R.choice([10, 100, 1000, 11, 101, 110, 1001])
        s = [a + d * i for i in range(6)]
        rule = "%s씩 커지는" % num(d)
    elif k == "sub":
        d = R.choice([10, 100, 1000, 110, 1010])
        a = R.randint(6000, 9900)
        s = [a - d * i for i in range(6)]
        rule = "%s씩 작아지는" % num(d)
    elif k == "mul":
        a = R.randint(1, 9)
        m = R.choice([2, 3, 10])
        s = [a * m ** i for i in range(6)]
        rule = "%d배씩 커지는" % m
    else:
        a = R.randint(1, 20)
        s = [a]
        for i in range(5):
            s.append(s[-1] + i + 1)
        rule = "1, 2, 3, …씩 커지는"
    hide = R.randrange(2, 6)
    show = [num(x) if i != hide else "□" for i, x in enumerate(s)]
    ans = s[hide]
    return mcq("규칙에 따라 □에 알맞은 수는?<br>%s" % ", ".join(show), num(ans),
               [num(x) for x in (ans + 1, ans - 1, ans + 10, s[hide - 1] * 2 if k != "mul" else ans + s[hide - 1], ans + (s[1] - s[0])) if x != ans and x > 0],
               "앞의 수와 비교하면 %s 규칙이에요. <b>%s</b>" % (rule, num(ans)))


def table_q():
    """수 배열표：가로로 a씩, 세로로 b씩"""
    a, b = R.choice([1, 10, 100, 11]), R.choice([100, 1000, 10, 110])
    if a == b:
        return None
    s = R.randint(100, 3000)
    cells = [[s + a * c + b * r for c in range(4)] for r in range(3)]
    hr, hc = R.randrange(1, 3), R.randrange(1, 4)
    ans = cells[hr][hc]
    rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % ("□" if (r, c) == (hr, hc) else num(cells[r][c])) for c in range(4)) for r in range(3))
    t = "<div class='sn-tw'><table class='sn-table'><tbody>%s</tbody></table></div>" % rows
    return mcq(t + "수 배열표의 규칙을 찾아 □에 알맞은 수를 구하세요. (가로 첫 줄은 %s부터 시작해요)" % num(s), num(ans),
               [num(x) for x in (ans + a, ans - a, ans + b, ans - b) if x != ans and x > 0],
               "오른쪽으로 %s씩, 아래로 %s씩 커지는 규칙이에요. <b>%s</b>" % (num(a), num(b), num(ans)))


def shape_q():
    """도형의 배열：바둑돌 수"""
    k = R.choice(["line", "square", "tri"])
    n = R.randint(5, 9)
    if k == "line":
        f = lambda i: 2 * i + 1
        rule = "2개씩 늘어나는"
    elif k == "square":
        f = lambda i: i * i
        rule = "1×1, 2×2, 3×3, …인"
    else:
        f = lambda i: i * (i + 1) // 2
        rule = "2, 3, 4, …개씩 늘어나는"
    seq = [f(i) for i in range(1, 5)]
    s = ""
    x = 10
    for i in range(1, 5):
        cnt = f(i)
        if k == "square":
            for r in range(i):
                for c in range(i):
                    s += "<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (x + c * 15 + 7, 75 - r * 15, INK)
            x += i * 15 + 20
        elif k == "tri":
            for r in range(i):
                for c in range(r + 1):
                    s += "<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (x + c * 15 + 7 + (i - 1 - r) * 7, 75 - (i - 1 - r) * 15, INK)
            x += i * 15 + 20
        else:
            for c in range(cnt):
                s += "<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (x + (c % 3) * 15 + 7, 75 - (c // 3) * 15, INK)
            x += 3 * 15 + 20
    W = x
    q = fig(svg_wrap(W, 90, s, "바둑돌 배열")) + "바둑돌을 규칙에 따라 늘어놓았어요(첫째: %d개, 둘째: %d개, 셋째: %d개, 넷째: %d개). %d째에 놓을 바둑돌은 몇 개인가요?" % (
        seq[0], seq[1], seq[2], seq[3], n)
    names = {5: "다섯", 6: "여섯", 7: "일곱", 8: "여덟", 9: "아홉"}
    q = q.replace("%d째" % n, "%s째" % names[n])
    ans = f(n)
    return mcq(q, "%d개" % ans, ["%d개" % x for x in (f(n - 1), f(n + 1), ans + 1, ans + n) if x != ans],
               "%s 규칙이에요. %s째에는 <b>%d개</b>예요." % (rule, names[n], ans))


def calc_q():
    """계산식의 배열"""
    k = R.choice(["11", "add", "mul"])
    if k == "11":
        x0 = R.randint(12, 40)
        lines = ["%d × 11 = %d" % (x, x * 11) for x in range(x0, x0 + 4)]
        n = x0 + 4
        ans = "%d × 11 = %d" % (n, n * 11)
        return mcq("계산식의 규칙을 찾아 다음에 올 식을 고르세요.<br>%s" % "<br>".join(lines), ans,
                   ["%d × 11 = %d" % (n, n * 11 + 10), "%d × 11 = %d" % (n, n * 10), "%d × 12 = %d" % (n, n * 12)],
                   "곱해지는 수가 1씩 커지면 곱은 11씩 커져요. <b>%s</b>" % ans)
    if k == "add":
        a = R.choice([101, 201, 301, 1001])
        b = R.choice([100, 200, 1000])
        lines = ["%d + %d = %d" % (a + 10 * i, b + 10 * i, a + b + 20 * i) for i in range(4)]
        i = 4
        ans = "%d + %d = %d" % (a + 10 * i, b + 10 * i, a + b + 20 * i)
        return mcq("계산식의 규칙을 찾아 다섯째 식을 고르세요.<br>%s" % "<br>".join(lines), ans,
                   ["%d + %d = %d" % (a + 10 * i, b + 10 * i, a + b + 10 * i), "%d + %d = %d" % (a + 10 * i, b + 10 * i, a + b + 20 * i + 10), "%d + %d = %d" % (a + 40, b + 30, a + b + 70)],
                   "두 수가 각각 10씩 커지면 합은 20씩 커져요. <b>%s</b>" % ans)
    base = R.choice([1, 11, 111])
    lines = ["%d × %d = %d" % (base, 9 * k2 + 0, base * 9 * k2) for k2 in range(1, 5)]
    k2 = 5
    ans = "%d × %d = %d" % (base, 9 * k2, base * 9 * k2)
    return mcq("계산식의 규칙을 찾아 다섯째 식을 고르세요.<br>%s" % "<br>".join(lines), ans,
               ["%d × %d = %d" % (base, 9 * k2, base * 9 * k2 + 9), "%d × %d = %d" % (base, 9 * k2 + 1, base * 9 * k2), "%d × %d = %d" % (base, 50, base * 50)],
               "곱하는 수가 9씩 커지면 곱은 %d씩 커져요. <b>%s</b>" % (base * 9, ans))


# ---------------------------------------------------------------- 등호
def eq_true():
    a, b = R.randint(12, 90), R.randint(12, 90)
    k = R.choice(["swap", "split", "mul", "wrong"])
    if k == "swap":
        lhs, rhs, ok = "%d + %d" % (a, b), "%d + %d" % (b, a), True
    elif k == "split":
        c = R.randint(1, b - 1)
        lhs, rhs, ok = "%d + %d" % (a, b), "%d + %d" % (a + c, b - c), True
    elif k == "mul":
        x, y = R.randint(2, 9), R.randint(2, 9)
        lhs, rhs, ok = "%d × %d" % (x, y * 2), "%d × %d" % (x * 2, y), True
    else:
        c = R.randint(1, 9)
        lhs, rhs, ok = "%d − %d" % (a + b, b), "%d − %d" % (a + b + c, b - c) if b > c else "%d + %d" % (a, c), False
    return mcq("다음 식이 옳으면 ○, 옳지 않으면 ×를 고르세요.<br>%s = %s" % (lhs, rhs), "○" if ok else "×", ["×" if ok else "○", "알 수 없어요", "계산할 수 없어요"],
               "등호(=) 양쪽의 크기가 같으면 옳은 식이에요. %s" % ("양쪽이 같아요." if ok else "양쪽의 크기가 달라요."))


def eq_box():
    k = R.choice(["add", "sub", "mul", "comp"])
    if k == "add":
        a, b, c = R.randint(20, 90), R.randint(10, 60), R.randint(1, 15)
        return mcq("%d + %d = %d + □에서 □에 알맞은 수는?" % (a, b, a + c), str(b - c) if b > c else None, [str(x) for x in (b + c, a + b, c, b - c + 1) if x > 0],
                   "%d가 %d로 %d만큼 커졌으니 □는 %d보다 %d만큼 작아야 해요. <b>%d</b>" % (a, a + c, c, b, c, b - c)) if b > c else None
    if k == "sub":
        a, b, c = R.randint(50, 99), R.randint(10, 40), R.randint(1, 9)
        return mcq("%d − %d = %d − □에서 □에 알맞은 수는?" % (a, b, a + c), str(b + c), [str(x) for x in (b - c, a - b, c, b + c + 1)],
                   "빼지는 수가 %d만큼 커졌으니 빼는 수도 %d만큼 커져야 차가 같아요. <b>%d</b>" % (c, c, b + c))
    if k == "mul":
        x, y = R.randint(2, 9), R.randint(2, 6)
        m = R.choice([2, 3])
        return mcq("%d × %d = %d × □에서 □에 알맞은 수는?" % (x * m, y, x), str(y * m), [str(t) for t in (y, y + m, x * y, y * m + 1)],
                   "%d가 %d의 %d배이니 □는 %d의 %d배예요. <b>%d</b>" % (x * m, x, m, y, m, y * m))
    a, b = R.randint(10, 80), R.randint(10, 80)
    s = a + b
    c = R.randint(5, s - 5)
    return mcq("%d + %d = □ + %d에서 □에 알맞은 수는?" % (a, b, c), str(s - c), [str(t) for t in (s, s + c, c, abs(a - c) or s - c + 1)],
               "왼쪽은 %d예요. □ + %d = %d이니까 <b>%d</b>" % (s, c, s, s - c))


def eq_story():
    w1, w2 = NM.next(), NM.next()
    a, b = R.randint(10, 40), R.randint(10, 40)
    c = R.randint(1, 9)
    t = "%s 구슬을 빨간 것 %d개, 파란 것 %d개 가지고 있고, %s 빨간 것 %d개와 파란 것 몇 개를 가지고 있어요. 두 사람의 구슬 수가 같을 때, 이것을 등호를 사용한 식으로 바르게 나타낸 것은?" % (
        josa(w1, "은/는"), a, b, josa(w2, "은/는"), a + c)
    ans = "%d + %d = %d + □" % (a, b, a + c)
    return mcq(t, ans, ["%d + %d = %d" % (a, b, a + c), "%d + □ = %d + %d" % (a, a + c, b), "%d − %d = %d − □" % (a, b, a + c)],
               "%s의 구슬 수 %d + %d와 %s의 구슬 수 %d + □가 같아요. 파란 구슬은 %d개예요." % (w1, a, b, w2, a + c, b - c))


def build(which):
    G = "grade-4"
    if which == "large":
        return unit(G, "large-numbers", 1, "[4수01-01]",
                    "큰 수의 필요성을 인식하면서 10000 이상의 큰 수에 대한 자릿값과 위치적 기수법을 이해하고, 수를 읽고 쓸 수 있다.",
                    "큰 수: 만, 억, 조", "큰 수",
                    "초등 4학년 큰 수 학습지: 만, 십만, 백만, 천만, 억, 조 읽고 쓰기, 자릿값, 숫자가 나타내는 값, 돈 세기까지 100문제와 정답.",
                    "네 자리씩 끊어 만, 억, 조", "1000이 10개 → 만, 1000만이 10개 → 억",
                    ["1000이 10개이면 <b>10000(만)</b>, 1000만이 10개이면 <b>1억</b>, 1000억이 10개이면 <b>1조</b>예요.",
                     "큰 수는 <b>오른쪽에서부터 네 자리씩</b> 끊고, 만, 억, 조를 붙여 읽어요.",
                     "같은 숫자라도 어느 자리에 있느냐에 따라 나타내는 값이 달라요. 352000000에서 5는 5000만을 나타내요."],
                    [("2억 3050만 400을 수로 쓰면?", ["억: 2", "만: 3050", "일: 0400"], "230,500,400"),
                     ("4,060,000,000,000을 읽으면?", ["4 0600 0000 0000 → 4조 600억"], "사조 육백억")],
                    [("네 자리씩 끊지 않고 왼쪽부터 끊는다", "오른쪽 일의 자리부터 네 자리씩 끊어요."),
                     ("0인 자리를 빼고 수를 쓴다", "읽지 않는 자리에는 0을 꼭 써요."),
                     ("숫자와 숫자가 나타내는 값을 헷갈린다", "만의 자리 숫자 3은 30000을 나타내요.")],
                    [("큰 수는 몇 학년에서 배우나요?", "초등 4학년 1학기 첫 단원에서 만, 억, 조를 배워요."),
                     ("큰 수를 쉽게 읽는 방법은?", "오른쪽에서부터 네 자리씩 표시를 하고, 왼쪽 묶음부터 조, 억, 만을 붙여 읽어요.")],
                    [("만 알아보기", [(unit_q, 8), (count_q, 12)]),
                     ("큰 수 읽기", [(read_q, 20)]),
                     ("자릿값", [(place_q, 20)]),
                     ("억과 조", [(unit_q, 6), (read_q, 14)]),
                     ("돈과 큰 수", [(count_q, 8), (place_q, 12)])], 82401)
    if which == "compare":
        return unit(G, "comparing-large-numbers", 2, "[4수01-02]",
                    "다섯 자리 이상의 수의 범위에서 수의 계열을 이해하고, 수의 크기를 비교하며 그 방법을 설명할 수 있다.",
                    "큰 수의 뛰어 세기와 크기 비교", "큰 수의 크기 비교",
                    "초등 4학년 큰 수 학습지: 만씩, 억씩, 조씩 뛰어 세기, 10배 한 수, 큰 수의 크기 비교까지 100문제와 정답.",
                    "자리 수부터, 같으면 높은 자리부터", "10배 할 때마다 0이 하나씩 늘어요.",
                    ["<b>뛰어 세기</b>: 10만씩 뛰어 세면 십만의 자리 숫자가 1씩 커져요.",
                     "수의 크기를 비교할 때는 먼저 <b>자리 수</b>를 비교해요. 자리 수가 많은 쪽이 커요.",
                     "자리 수가 같으면 <b>가장 높은 자리부터</b> 차례로 같은 자리의 숫자를 비교해요.",
                     "어떤 수를 10배 하면 0이 하나 늘어나요."],
                    [("3억 2000만과 302,000,000 중 더 큰 수는?", ["3억 2000만 = 320,000,000", "천만의 자리: 2 > 0"], "3억 2000만")],
                    [("숫자가 큰 쪽이 무조건 크다고 생각한다", "자리 수를 먼저 비교해요."),
                     ("10만씩 뛰어 세는데 만의 자리를 바꾼다", "어느 자리 숫자가 바뀌는지 확인해요."),
                     ("10배 하면서 0을 두 개 붙인다", "10배는 0 하나, 100배는 0 두 개예요.")],
                    [("큰 수의 크기는 어떻게 비교하나요?", "자리 수를 비교하고, 같으면 가장 높은 자리부터 숫자를 비교해요."),
                     ("뛰어 세기를 왜 배우나요?", "수가 커지는 규칙을 알고, 큰 수의 자릿값을 이해하는 데 도움이 돼요.")],
                    [("뛰어 세기", [(skip_q, 20)]),
                     ("10배, 100배 한 수", [(times10, 20)]),
                     ("크기 비교", [(cmp_q, 20)]),
                     ("만, 억으로 쓴 수와 비교", [(cmp_mixed, 20)]),
                     ("섞어서 연습", [(skip_q, 7), (cmp_q, 7), (times10, 6)])], 82402)
    if which == "mul":
        return unit(G, "multiply-three-digit-by-two-digit", 5, "[4수01-04]",
                    "곱하는 수가 한 자리 수 또는 두 자리 수인 곱셈의 계산 원리를 이해하고 그 계산을 할 수 있다.",
                    "(세 자리 수) × (두 자리 수)", "(세 자리 수) × (두 자리 수)",
                    "초등 4학년 곱셈 학습지: (몇백)×(몇십), (세 자리 수)×(몇십), (세 자리 수)×(두 자리 수) 세로셈, 문장제까지 100문제와 정답.",
                    "곱하는 수를 몇십과 몇으로 나눠요", "324 × 26 = 324 × 6 + 324 × 20",
                    ["(몇백) × (몇십)은 (몇) × (몇)을 계산하고 0의 개수만큼 0을 붙여요. 300 × 40 = 12000",
                     "(세 자리 수) × (몇십)은 (세 자리 수) × (몇)에 0을 하나 붙여요.",
                     "(세 자리 수) × (두 자리 수)는 곱하는 수를 <b>몇십과 몇으로 나누어</b> 곱하고 더해요. 십의 자리 곱은 한 칸 왼쪽에 써요."],
                    [("254 × 36 =", ["254 × 6 = 1524", "254 × 30 = 7620", "1524 + 7620 = 9144"], "9144")],
                    [("십의 자리를 곱한 값을 일의 자리에 맞추어 쓴다", "254 × 3은 실제로 254 × 30 = 7620이에요."),
                     ("0의 개수를 잘못 센다", "곱하는 두 수의 끝에 있는 0을 모두 세요."),
                     ("올림한 수를 더하지 않는다", "자리마다 올림을 작게 써 두어요.")],
                    [("4학년 곱셈은 3학년과 무엇이 다른가요?", "3학년은 (두 자리 수) × (두 자리 수)까지, 4학년은 (세 자리 수) × (두 자리 수)를 배워요."),
                     ("어림으로 확인하는 방법은?", "254 × 36은 250 × 40 = 10000 가까이 나와야 해요.")],
                    [("(몇백) × (몇십)", [(mul_q("h0"), 20)]),
                     ("(세 자리 수) × (몇십)", [(mul_q("x0"), 20)]),
                     ("(세 자리 수) × (두 자리 수) 1", [(mul_q("xx"), 20)]),
                     ("(세 자리 수) × (두 자리 수) 2", [(mul_q("xx"), 20)]),
                     ("문장제", [(mul_story, 20)])], 82405)
    if which == "div":
        return unit(G, "divide-by-two-digit-numbers", 6, "[4수01-07]",
                    "나누는 수가 두 자리 수인 나눗셈의 계산 원리를 이해하고 그 계산을 할 수 있다.",
                    "나누는 수가 두 자리 수인 나눗셈", "(세 자리 수) ÷ (두 자리 수)",
                    "초등 4학년 나눗셈 학습지: (세 자리 수)÷(몇십), 몫이 한 자리 수, 두 자리 수인 나눗셈, 나머지와 확인, 문장제까지 100문제와 정답.",
                    "몫을 어림하고 곱해서 확인해요", "나머지는 나누는 수보다 작아요.",
                    ["나누는 수가 두 자리 수이면 <b>몫을 어림</b>해요. 158 ÷ 32는 160 ÷ 30처럼 생각하면 몫은 5쯤이에요.",
                     "어림한 몫을 곱해 보고, 나누어지는 수보다 크면 몫을 1 작게, 나머지가 나누는 수보다 크면 몫을 1 크게 고쳐요.",
                     "나누어지는 수의 앞 두 자리가 나누는 수보다 크거나 같으면 몫은 두 자리 수예요.",
                     "확인: 나누는 수 × 몫 + 나머지 = 나누어지는 수"],
                    [("196 ÷ 28 =", ["200 ÷ 30 → 몫은 6이나 7", "28 × 7 = 196"], "7"),
                     ("845 ÷ 36 =", ["84 ÷ 36 = 2 … 12", "125 ÷ 36 = 3 … 17"], "23 … 17")],
                    [("어림한 몫을 고치지 않는다", "곱한 값이 나누어지는 수보다 크면 몫을 줄여요."),
                     ("나머지가 나누는 수보다 크다", "나머지가 나누는 수보다 크면 몫을 1 크게 해요."),
                     ("몫의 자리를 잘못 쓴다", "앞 두 자리를 나눌 수 있으면 몫은 두 자리 수예요.")],
                    [("나누는 수가 두 자리 수인 나눗셈은 언제 배우나요?", "초등 4학년 1학기 「곱셈과 나눗셈」 단원에서 배워요."),
                     ("몫을 쉽게 어림하는 방법은?", "나누는 수를 몇십으로 생각해 보세요. 32는 30, 47은 50처럼요.")],
                    [("(세 자리 수) ÷ (몇십)", [(div_q("tens"), 20)]),
                     ("몫이 한 자리 수인 나눗셈", [(div_q("one"), 20)]),
                     ("나누어떨어지는 나눗셈", [(div_q("exact"), 20)]),
                     ("몫이 두 자리 수인 나눗셈", [(div_q("two"), 14), (div_check, 6)]),
                     ("문장제", [(div_story, 20)])], 82406)
    if which == "patterns":
        return unit(G, "number-patterns", 11, "[4수02-01] [4수02-02]",
                    "다양한 변화 규칙을 찾아 설명하고, 그 규칙을 수나 식으로 나타낼 수 있다. 계산식의 배열에서 규칙을 찾고, 계산 결과를 추측할 수 있다.",
                    "규칙 찾기", "규칙 찾기",
                    "초등 4학년 규칙 찾기 학습지: 수의 배열, 수 배열표, 도형의 배열, 계산식의 배열에서 규칙을 찾아 다음 수와 식 구하기까지 100문제와 정답.",
                    "앞의 수와 비교해 변화를 찾아요", "가로, 세로, 대각선으로도 살펴봐요.",
                    ["수의 배열에서는 <b>앞의 수와 뒤의 수를 비교</b>해 몇씩 커지는지, 몇 배가 되는지 찾아요.",
                     "수 배열표에서는 <b>가로, 세로</b> 방향의 규칙을 따로 찾아요.",
                     "도형의 배열에서는 모양이 하나씩 늘어날 때 <b>몇 개씩 늘어나는지</b> 세어요.",
                     "계산식의 배열에서는 바뀌는 수와 결과가 바뀌는 규칙을 찾아 다음 식을 추측해요."],
                    [("1205, 1305, 1405, □, 1605", ["100씩 커지는 규칙"], "1505")],
                    [("처음 두 수만 보고 규칙을 정한다", "여러 수를 비교해서 규칙이 맞는지 확인해요."),
                     ("늘어나는 수가 커지는 규칙을 놓친다", "1, 3, 6, 10처럼 늘어나는 수가 1씩 커지기도 해요."),
                     ("계산식의 결과만 보고 식을 고른다", "식의 수와 결과가 함께 규칙에 맞는지 봐요.")],
                    [("규칙 찾기는 왜 배우나요?", "규칙을 찾아 다음을 추측하는 힘은 나중에 배우는 식과 함수의 바탕이 돼요."),
                     ("수 배열표에서 규칙이 둘 이상일 수 있나요?", "네. 가로와 세로의 규칙이 다를 수 있어요. 둘 다 확인하세요.")],
                    [("수의 배열", [(seq_q, 20)]),
                     ("수 배열표", [(table_q, 20)]),
                     ("도형의 배열", [(shape_q, 15), (seq_q, 5)]),
                     ("계산식의 배열", [(calc_q, 8), (table_q, 12)]),
                     ("섞어서 연습", [(seq_q, 10), (table_q, 6), (calc_q, 4)])], 82411)
    return unit(G, "equal-sign-and-equations", 12, "[4수02-03]",
                "등호를 사용하여 크기가 같은 두 양의 관계를 식으로 나타낼 수 있다.",
                "등호를 사용한 식", "등호(=)와 식",
                "초등 4학년 학습지: 등호(=)의 뜻, 옳은 식 찾기, 크기가 같은 두 양을 식으로 나타내기, □에 알맞은 수까지 100문제와 정답.",
                "등호 양쪽의 크기가 같아요", "25 + 37 = 30 + 32",
                ["등호(=)는 <b>양쪽의 크기가 같다</b>는 뜻이에요. 계산 결과를 쓰라는 기호만은 아니에요.",
                 "25 + 37 = 30 + 32처럼 양쪽에 식이 있어도 크기가 같으면 옳은 식이에요.",
                 "더하는 한 수가 커진 만큼 다른 수가 작아지면 합이 같아요. 빼는 식에서는 두 수가 같이 커져야 차가 같아요."],
                [("48 + 27 = 50 + □", ["48이 50으로 2만큼 커졌어요.", "27보다 2만큼 작은 수: 25"], "25")],
                [("등호 뒤에는 계산 결과만 와야 한다고 생각한다", "등호 양쪽에 식이 와도 크기가 같으면 돼요."),
                 ("48 + 27 = 50 + □에서 □를 75라고 한다", "75는 왼쪽의 값이에요. 50에 더해서 75가 되는 수를 찾아요."),
                 ("뺄셈에서 빼는 수를 반대로 바꾼다", "빼지는 수가 커지면 빼는 수도 같은 만큼 커져야 해요.")],
                [("등호는 언제 배우나요?", "2022 개정 교육과정에서 초등 4학년 「규칙과 관계」에서 등호를 사용해 같은 두 양을 식으로 나타내요."),
                 ("□를 빨리 구하는 방법은?", "양쪽의 수가 어떻게 바뀌었는지 비교하면 계산하지 않고도 구할 수 있어요.")],
                [("옳은 식 찾기", [(eq_true, 20)]),
                 ("□에 알맞은 수 1", [(eq_box, 20)]),
                 ("□에 알맞은 수 2", [(eq_box, 20)]),
                 ("식으로 나타내기", [(eq_story, 14), (eq_true, 6)]),
                 ("섞어서 연습", [(eq_box, 10), (eq_true, 10)])], 82412)
