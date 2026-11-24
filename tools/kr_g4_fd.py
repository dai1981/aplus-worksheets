# -*- coding: utf-8 -*-
"""
대한민국 초등 4학년 수학：분수의 덧셈과 뺄셈・소수 두 자리 수와 세 자리 수・소수의 덧셈과 뺄셈
  fadd  : 분모가 같은 분수의 덧셈과 뺄셈 [4수01-15]
  dec   : 소수 두 자리 수와 세 자리 수, 크기 비교 [4수01-13] [4수01-14]
  dadd  : 소수의 덧셈과 뺄셈 [4수01-16]
誤答は「분모끼리도 더한다」「받아내림을 하지 않는다」「소수점 자리를 맞추지 않는다」「자릿수가 많으면 큰 수라고 생각한다」から作る。
"""
import random
from decimal import Decimal as D
from fractions import Fraction as F
from kr_common import mcq, unit, Names, josa, fr, ff
from kr_pics import frac_bar, number_line, fig, svg_wrap, text, INK

R = random.Random(82413)
NM = Names(R)


def dd(v):
    """Decimal → 문자열（불필요한 0 없음）"""
    v = D(v)
    s = format(v.normalize(), "f")
    return s


def fs(v, d):
    """약분하지 않는 대분수（4학년은 약분을 배우지 않음）。분모は d"""
    v = F(v)
    n = v * d
    assert n.denominator == 1
    n = int(n)
    w, r = divmod(n, d)
    if r == 0:
        return str(w)
    return ("%d" % w if w else "") + fr(r, d)


# ---------------------------------------------------------------- 분수의 덧셈과 뺄셈
def proper_add():
    d = R.randint(4, 15)
    a, b = R.randint(1, d - 2), R.randint(1, d - 2)
    s = F(a + b, d)
    pic = frac_bar(a, d) if d <= 12 and R.random() < 0.3 else ""
    return mcq(pic + "%s + %s =" % (fr(a, d), fr(b, d)), fs(s, d), [fr(a + b, 2 * d), fr(a + b, d) if a + b > d else fs(s + F(1, d), d), fs(s - F(1, d), d) if a + b > 1 else fr(a * b, d), fr(a + b + 1, d)],
               "분모는 그대로 두고 분자끼리 더해요. %d + %d = %d이니까 %s%s" % (a, b, a + b, fr(a + b, d), " = <b>%s</b>" % fs(s, d) if a + b >= d else "이에요. <b>%s</b>" % fr(a + b, d)))


def proper_sub():
    d = R.randint(4, 15)
    a = R.randint(2, d - 1)
    b = R.randint(1, a - 1)
    return mcq("%s − %s =" % (fr(a, d), fr(b, d)), fr(a - b, d), [fr(a - b, 2 * d), fr(a + b, d), fr(a - b + 1, d), fr(a - b, d - 1) if d - 1 > a - b else fr(a - b + 2, d)],
               "분모는 그대로 두고 분자끼리 빼요. %d − %d = %d → <b>%s</b>" % (a, b, a - b, fr(a - b, d)))


def one_minus():
    d = R.randint(3, 15)
    n = R.randint(1, d - 1)
    w = R.randint(1, 5)
    if w == 1:
        return mcq("1 − %s =" % fr(n, d), fr(d - n, d), [fr(1 - n, d) if n < 1 else fr(n, d) if n != d - n else fr(n + 1, d), fr(d - n, d + 1) if d - n < d + 1 else fr(d, d), fr(d + n, d), fr(d - n + 1, d)],
                   "1을 %s로 바꾸어 빼요. %s − %s = <b>%s</b>" % (fr(d, d), fr(d, d), fr(n, d), fr(d - n, d)))
    return mcq("%d − %s =" % (w, fr(n, d)), fs(F(w * d - n, d), d), [fs(F(w * d - n, d) + 1, d), "%d%s" % (w, fr(d - n, d)), "%d%s" % (w - 1, fr(n, d)) if n != d - n else fs(F(w * d - n + 1, d), d), fs(F(w * d - n, d) - 1, d) if w > 1 else None],
               "%d을 %d%s로 바꾸어 계산해요. %d%s − %s = <b>%s</b>" % (w, w - 1, fr(d, d), w - 1, fr(d, d), fr(n, d), fs(F(w * d - n, d), d)))


def mixed_add(carry=False):
    def mk():
        d = R.randint(3, 12)
        a, b = R.randint(1, 5), R.randint(1, 5)
        n1, n2 = R.randint(1, d - 1), R.randint(1, d - 1)
        if carry != (n1 + n2 > d) or n1 + n2 == d:
            return None
        s = F(a * d + n1, d) + F(b * d + n2, d)
        nc = "%d%s" % (a + b, fr(n1 + n2, d))
        cands = [nc if carry else fs(s + 1, d), "%d%s" % (a + b, fr(n1 + n2, 2 * d)), fs(s - 1, d), fs(s + F(1, d), d)]
        e = "자연수는 자연수끼리, 분수는 분수끼리 더해요. %d + %d = %d, %s + %s = %s" % (a, b, a + b, fr(n1, d), fr(n2, d), fr(n1 + n2, d))
        if carry:
            e += "이고, %s = 1%s이므로 받아올림해요" % (fr(n1 + n2, d), fr(n1 + n2 - d, d))
        return mcq("%d%s + %d%s =" % (a, fr(n1, d), b, fr(n2, d)), fs(s, d), cands, e + ". <b>%s</b>" % fs(s, d))
    return mk


def mixed_sub(borrow=False):
    def mk():
        d = R.randint(3, 12)
        a = R.randint(2, 7)
        b = R.randint(1, a - 1)
        n1, n2 = R.randint(1, d - 1), R.randint(1, d - 1)
        if borrow != (n1 < n2) or n1 == n2:
            return None
        s = F(a * d + n1, d) - F(b * d + n2, d)
        if s <= 0:
            return None
        wrong = "%d%s" % (a - b, fr(abs(n1 - n2), d))  # 큰 분자에서 작은 분자를 뺌
        cands = [wrong if borrow else fs(s + 1, d), fs(s + 1, d) if borrow else fs(s - F(1, d), d), fs(s + F(1, d), d), fs(s - 1, d) if s > 1 else fr(abs(n1 - n2) + 1, d)]
        if borrow:
            e = "%s에서 %s를 뺄 수 없으니 자연수에서 1을 받아내림해요. %d%s = %d%s. %d%s − %d%s = <b>%s</b>" % (
                fr(n1, d), fr(n2, d), a, fr(n1, d), a - 1, fr(n1 + d, d), a - 1, fr(n1 + d, d), b, fr(n2, d), fs(s, d))
        else:
            e = "자연수끼리, 분수끼리 빼요. %d − %d = %d, %s − %s = %s. <b>%s</b>" % (a, b, a - b, fr(n1, d), fr(n2, d), fr(n1 - n2, d), fs(s, d))
        return mcq("%d%s − %d%s =" % (a, fr(n1, d), b, fr(n2, d)), fs(s, d), cands, e)
    return mk


def mixed_minus_improper():
    d = R.randint(3, 9)
    a = R.randint(2, 6)
    n1 = R.randint(1, d - 1)
    m = R.randint(d + 1, 2 * d - 1)
    s = F(a * d + n1, d) - F(m, d)
    if s <= 0:
        return None
    return mcq("%d%s − %s =" % (a, fr(n1, d), fr(m, d)), fs(s, d), [fs(s + 1, d), fs(s - F(1, d), d), "%d%s" % (a, fr(abs(n1 - m), d)) if n1 != m else None, fs(s + F(1, d), d)],
               "대분수를 가분수로 바꾸면 %s예요. %s − %s = %s = <b>%s</b>" % (fr(a * d + n1, d), fr(a * d + n1, d), fr(m, d), fr(a * d + n1 - m, d), fs(s, d)))


FOODS = [("우유", "L"), ("주스", "L"), ("물", "L"), ("밀가루", "kg"), ("설탕", "kg"), ("끈", "m"), ("리본", "m"), ("철사", "m")]


def frac_story():
    food, u = R.choice(FOODS)
    d = R.randint(3, 10)
    a, b = R.randint(1, 4), R.randint(0, 3)
    n1, n2 = R.randint(1, d - 1), R.randint(1, d - 1)
    x, y = F(a * d + n1, d), F(b * d + n2, d)
    who = NM.next()
    k = R.choice(["add", "sub", "left"])
    if k == "add":
        s = x + y
        return mcq("%s %s %s %s 있었는데 %s %s 더 샀어요. %s 모두 몇 %s인가요?" % (josa(who, "은/는"), food, fs(x, d), u, fs(y, d), u, josa(food, "은/는"), u),
                   "%s %s" % (fs(s, d), u), ["%s %s" % (fs(abs(x - y), d) if x != y else fs(s + 1, d), u), "%s %s" % (fs(s + 1, d), u), "%s %s" % (fs(s - F(1, d), d), u)],
                   "모두 → 덧셈. %s + %s = <b>%s %s</b>" % (fs(x, d), fs(y, d), fs(s, d), u))
    if x <= y:
        x, y = y, x
    if x == y:
        return None
    s = x - y
    if k == "sub":
        return mcq("%s %s %s %s 중에서 %s %s 썼어요. 남은 %s 몇 %s인가요?" % (josa(who, "은/는"), food, fs(x, d), u, fs(y, d), u, josa(food, "은/는"), u),
                   "%s %s" % (fs(s, d), u), ["%s %s" % (fs(x + y, d), u), "%s %s" % (fs(s + 1, d), u), "%s %s" % (fs(s + F(1, d), d), u)],
                   "남은 양 → 뺄셈. %s − %s = <b>%s %s</b>" % (fs(x, d), fs(y, d), fs(s, d), u))
    return mcq("가 그릇에 %s %s %s, 나 그릇에 %s %s 있어요. 어느 그릇에 몇 %s 더 많이 있나요?" % (food, fs(x, d), u, fs(y, d), u, u),
               "가 그릇, %s %s" % (fs(s, d), u), ["나 그릇, %s %s" % (fs(s, d), u), "가 그릇, %s %s" % (fs(x + y, d), u), "가 그릇, %s %s" % (fs(s + 1, d), u)],
               "큰 수에서 작은 수를 빼요. %s − %s = <b>%s %s</b>" % (fs(x, d), fs(y, d), fs(s, d), u))


def frac_missing():
    d = R.randint(4, 12)
    a, b = R.randint(1, d - 1), R.randint(1, d - 1)
    if a + b >= d:
        return None
    if R.random() < 0.5:
        return mcq("%s + □ = %s 에서 □에 알맞은 분수는?" % (fr(a, d), fr(a + b, d)), fr(b, d), [fr(a + b + a, d), fr(b, 2 * d) if 2 * d > b else None, fr(b + 1, d), fr(a, d) if a != b else fr(b + 2, d)],
                       "□ = %s − %s = <b>%s</b>" % (fr(a + b, d), fr(a, d), fr(b, d)))
    return mcq("□ − %s = %s 에서 □에 알맞은 분수는?" % (fr(a, d), fr(b, d)), fr(a + b, d), [fr(abs(a - b), d) if a != b else fr(a + b + 1, d), fr(a + b, 2 * d), fr(a + b - 1, d) if a + b - 1 not in (0,) else None, fr(a + b + 2, d)],
                   "□ = %s + %s = <b>%s</b>" % (fr(b, d), fr(a, d), fr(a + b, d)))


# ---------------------------------------------------------------- 소수 두 자리 수, 세 자리 수
READ = "영일이삼사오육칠팔구"


def read_dec(s):
    w, f = s.split(".")
    from kr_common import read_num
    return "%s 점 %s" % (read_num(int(w)) if int(w) else "영", "".join(READ[int(c)] for c in f))


def rand_dec(places, hi=9):
    n = R.randint(1, hi * 10 ** places + 10 ** places - 1)
    if n % 10 == 0:
        n += R.randint(1, 9)
    return D(n).scaleb(-places)


def dec_read():
    v = rand_dec(R.choice([2, 3]), 20)
    s = dd(v)
    ans = read_dec(s)
    w, f = s.split(".")
    from kr_common import read_num
    bad1 = "%s 점 %s" % (read_num(int(w)) if int(w) else "영", read_num(int(f)))
    bad2 = "%s 점 %s" % (read_num(int(w)) if int(w) else "영", "".join(READ[int(c)] for c in f[::-1])) if f != f[::-1] else None
    if R.random() < 0.5:
        return mcq("%s를 바르게 읽은 것은?" % s, ans, [bad1, bad2, "%s 점 %s" % (read_num(int(w) + 1), "".join(READ[int(c)] for c in f))],
                   "소수점 아래는 숫자를 하나씩 읽어요. <b>%s</b>" % ans)
    return mcq("「%s」를 소수로 쓰면?" % ans, s, [s.replace(".", "") if len(s) < 8 else None, dd(v * 10), dd(v / 10), dd(v + D(1).scaleb(-len(f)))],
               "소수점 아래 숫자를 차례로 써요. <b>%s</b>" % s)


def dec_place():
    v = rand_dec(3, 9)
    s = dd(v)
    if len(s.split(".")[1]) < 3 or len(set(s.replace(".", ""))) < 4:
        return None
    w, f = s.split(".")
    pos = R.choice([0, 1, 2])
    names = ["소수 첫째 자리", "소수 둘째 자리", "소수 셋째 자리"]
    dig = f[pos]
    val = D(int(dig)).scaleb(-(pos + 1))
    if R.random() < 0.5:
        return mcq("%s에서 %s 숫자는?" % (s, names[pos]), dig, [f[(pos + 1) % 3], f[(pos + 2) % 3], w],
                   "소수점 바로 오른쪽부터 첫째, 둘째, 셋째 자리예요. <b>%s</b>" % dig)
    if dig == "0":
        return None
    return mcq("%s에서 숫자 %s가 나타내는 수는?" % (s, dig), dd(val), [dd(val * 10), dd(val / 10), dig],
               "%s는 %s 숫자이므로 <b>%s</b>를 나타내요." % (dig, names[pos], dd(val)))


def dec_count():
    k = R.choice([2, 3])
    v = rand_dec(k, 9)
    s = dd(v)
    if len(s.split(".")[1]) != k:
        return None
    unitv = "0.01" if k == 2 else "0.001"
    n = int(v.scaleb(k))
    if R.random() < 0.5:
        return mcq("%s는 %s이 몇 개인 수인가요?" % (s, unitv), "%d개" % n, ["%d개" % x for x in (n // 10, n * 10, int(s.split(".")[1]))],
                   "%s는 %s이 <b>%d개</b>예요." % (s, unitv, n))
    return mcq("%s이 %d개인 수는?" % (unitv, n), s, [dd(v * 10), dd(v / 10), str(n)],
               "%s이 %d개이면 <b>%s</b>예요." % (unitv, n, s))


def dec_tenfold():
    v = rand_dec(R.choice([1, 2]), 9)
    if R.random() < 0.5:
        k = R.choice([10, 100])
        ans = v * k
        return mcq("%s의 %d배는?" % (dd(v), k), dd(ans), [dd(v * (10 if k == 100 else 100)), dd(v / k), dd(v + k)],
                   "%d배 하면 소수점이 오른쪽으로 %d칸 옮겨져요. <b>%s</b>" % (k, 1 if k == 10 else 2, dd(ans)))
    k = R.choice([10, 100])
    ans = v / k
    return mcq("%s의 %s는?" % (dd(v), fr(1, k)), dd(ans), [dd(v * k), dd(v / (100 if k == 10 else 10)), dd(v - D(k) / 100) if v > D(k) / 100 else dd(ans * 1000)],
               "%s로 하면 소수점이 왼쪽으로 %d칸 옮겨져요. <b>%s</b>" % (fr(1, k), 1 if k == 10 else 2, dd(ans)))


def dec_cmp():
    a = rand_dec(R.choice([1, 2, 3]), 9)
    b = rand_dec(R.choice([1, 2, 3]), 9)
    if a == b or abs(a - b) > 1:
        b = a + D(R.choice([-1, 1]) * R.choice([1, 2, 5, 11, 30])).scaleb(-R.choice([2, 3]))
        if b <= 0 or a == b:
            return None
    ans = ">" if a > b else "<"
    return mcq("두 수의 크기를 비교하세요. %s ○ %s" % (dd(a), dd(b)), ans, ["<" if ans == ">" else ">", "=", "비교할 수 없어요"],
               "자연수 부분부터 소수 첫째, 둘째, 셋째 자리 순서로 비교해요. 자릿수가 많다고 큰 수가 아니에요. <b>%s</b>" % ans)


def dec_max():
    base = R.randint(1, 8)
    vals = set()
    while len(vals) < 4:
        p = R.choice([1, 2, 3])
        vals.add(D(base) + D(R.randint(1, 10 ** p - 1)).scaleb(-p))
    vals = sorted(vals)
    big = R.random() < 0.5
    ans = vals[-1] if big else vals[0]
    longest = max(vals, key=lambda x: len(dd(x)))
    return mcq("가장 %s 수는? %s" % ("큰" if big else "작은", ", ".join(dd(x) for x in R.sample(vals, 4))), dd(ans), [dd(x) for x in vals if x != ans],
               "자연수 부분이 같으니 소수 첫째 자리부터 비교해요. <b>%s</b>" % dd(ans))


def dec_zero():
    v = rand_dec(R.choice([1, 2]), 9)
    s = dd(v)
    z = s + "0"
    return mcq("%s와 크기가 같은 수는?" % s, z, [s.replace(".", ".0", 1), dd(v * 10), dd(v / 10)],
               "소수의 오른쪽 끝에 0을 붙여도 크기는 같아요. %s = <b>%s</b>" % (s, z))


UNITS = [("cm", "m", 100), ("m", "km", 1000), ("g", "kg", 1000), ("mL", "L", 1000)]


def dec_units():
    small, big, k = R.choice(UNITS)
    n = R.randint(1, 3 * k - 1)
    if n % 10 == 0:
        n += R.randint(1, 9)
    v = D(n) / k
    if R.random() < 0.5:
        return mcq("%d %s는 몇 %s인가요?" % (n, small, big), "%s %s" % (dd(v), big), ["%s %s" % (dd(v * 10), big), "%s %s" % (dd(v / 10), big), "%d %s" % (n, big)],
                   "1 %s = %s %s이므로 %d %s = <b>%s %s</b>" % (small, dd(D(1) / k), big, n, small, dd(v), big))
    return mcq("%s %s는 몇 %s인가요?" % (dd(v), big, small), "%d %s" % (n, small), ["%d %s" % (n * 10, small), "%s %s" % (dd(D(n) / 10), small), "%s %s" % (dd(v), small)],
               "1 %s = %d %s이므로 %s %s = <b>%d %s</b>" % (big, k, small, dd(v), big, n, small))


def dec_line():
    a = D(R.randint(10, 89)) / 10
    k = R.randint(1, 9)
    v = a + D(k) / 100
    lab = {0: dd(a), 10: dd(a + D(1) / 10)}
    pic = number_line(0, 1, 10, marks=[(k, "?")], labels=lab)
    return mcq(pic + "수직선에서 ?가 나타내는 수는?", dd(v), [dd(a + D(k) / 10), dd(a + D(k) / 1000), dd(v + D(1) / 100)],
               "%s와 %s 사이가 10칸이니 한 칸은 0.01이에요. %s에서 %d칸 → <b>%s</b>" % (dd(a), dd(a + D(1) / 10), dd(a), k, dd(v)))


# ---------------------------------------------------------------- 소수의 덧셈과 뺄셈
def dec_add(p1, p2):
    def mk():
        a = rand_dec(p1, 9)
        b = rand_dec(p2, 9)
        s = a + b
        # 소수점을 맞추지 않고 끝을 맞춘 오답
        sa, sb = dd(a), dd(b)
        wrong = None
        if len(sa.split(".")[1]) != len(sb.split(".")[1]):
            ia, ib = int(sa.replace(".", "")), int(sb.replace(".", ""))
            pl = max(len(sa.split(".")[1]), len(sb.split(".")[1]))
            wrong = dd(D(ia + ib).scaleb(-pl))
        return mcq("%s + %s =" % (sa, sb), dd(s), [wrong, dd(s + D(1)), dd(s - D(1).scaleb(-max(p1, p2))), dd(s + D(1) / 10)],
                   "소수점의 자리를 맞추어 세로로 쓰고, 같은 자리 수끼리 더해요. <b>%s</b>" % dd(s))
    return mk


def dec_sub(p1, p2):
    def mk():
        a = rand_dec(p1, 9)
        b = rand_dec(p2, 9)
        if a <= b:
            a, b = b, a
        if a == b:
            return None
        s = a - b
        sa, sb = dd(a), dd(b)
        wrong = None
        la, lb = len(sa.split(".")[1]), len(sb.split(".")[1])
        if la != lb:
            ia, ib = int(sa.replace(".", "")), int(sb.replace(".", ""))
            if ia > ib:
                wrong = dd(D(ia - ib).scaleb(-max(la, lb)))
        return mcq("%s − %s =" % (sa, sb), dd(s), [wrong, dd(a + b), dd(s + D(1) / 10), dd(s + D(1).scaleb(-max(p1, p2)))],
                   "소수점의 자리를 맞추고, 빈자리는 0으로 생각해서 같은 자리끼리 빼요. <b>%s</b>" % dd(s))
    return mk


def int_minus_dec():
    w = R.randint(1, 10)
    b = rand_dec(R.choice([1, 2]), 0 if w == 1 else w - 1)
    if b >= w:
        return None
    s = D(w) - b
    sb = dd(b)
    return mcq("%d − %s =" % (w, sb), dd(s), [dd(D(w) + b), dd(s + 1), dd(s + D(1) / 10), dd(s - D(1) / 10) if s > D(1) / 10 else None],
               "%d을 %s으로 생각해서 소수점을 맞추어 빼요. <b>%s</b>" % (w, str(D(w).quantize(b)), dd(s)))


THINGS = [("물", "L"), ("우유", "L"), ("주스", "L"), ("끈", "m"), ("리본", "m"), ("쌀", "kg"), ("감자", "kg"), ("고구마", "kg")]


def dec_story():
    th, u = R.choice(THINGS)
    a = rand_dec(R.choice([1, 2]), 4)
    b = rand_dec(R.choice([1, 2]), 4)
    who = NM.next()
    k = R.choice(["add", "sub", "diff"])
    if k == "add":
        s = a + b
        return mcq("%s %s %s %s와 %s %s를 가지고 있어요. 모두 몇 %s인가요?" % (josa(who, "은/는"), th, dd(a), u, dd(b), u, u), "%s %s" % (dd(s), u),
                   ["%s %s" % (dd(abs(a - b)) if a != b else dd(s + 1), u), "%s %s" % (dd(s + D(1) / 10), u), "%s %s" % (dd(s + 1), u)],
                   "%s + %s = <b>%s %s</b>" % (dd(a), dd(b), dd(s), u))
    if a <= b:
        a, b = b, a
    if a == b:
        return None
    s = a - b
    if k == "sub":
        return mcq("%s %s %s %s 중에서 %s %s를 썼어요. 남은 %s 몇 %s인가요?" % (josa(who, "은/는"), th, dd(a), u, dd(b), u, josa(th, "은/는"), u), "%s %s" % (dd(s), u),
                   ["%s %s" % (dd(a + b), u), "%s %s" % (dd(s + D(1) / 10), u), "%s %s" % (dd(s + 1), u)],
                   "%s − %s = <b>%s %s</b>" % (dd(a), dd(b), dd(s), u))
    other = NM.next()
    if other == who:
        return None
    return mcq("%s %s %s %s, %s %s %s 모았어요. 누가 몇 %s 더 많이 모았나요?" % (josa(who, "은/는"), th, dd(a), u, josa(other, "은/는"), dd(b), u, u),
               "%s, %s %s" % (who, dd(s), u), ["%s, %s %s" % (other, dd(s), u), "%s, %s %s" % (who, dd(a + b), u), "%s, %s %s" % (who, dd(s + D(1) / 10), u)],
               "%s − %s = %s이므로 <b>%s</b>가 %s %s 더 많아요." % (dd(a), dd(b), dd(s), who, dd(s), u))


def dec_missing():
    a = rand_dec(2, 5)
    b = rand_dec(R.choice([1, 2]), 5)
    s = a + b
    if R.random() < 0.5:
        return mcq("%s + □ = %s 에서 □에 알맞은 수는?" % (dd(a), dd(s)), dd(b), [dd(s + a), dd(b + D(1) / 10), dd(b + D(1) / 100)],
                   "□ = %s − %s = <b>%s</b>" % (dd(s), dd(a), dd(b)))
    return mcq("□ − %s = %s 에서 □에 알맞은 수는?" % (dd(b), dd(a)), dd(s), [dd(abs(a - b)) if a != b else dd(s + 1), dd(s + D(1) / 10), dd(s - D(1) / 100)],
               "□ = %s + %s = <b>%s</b>" % (dd(a), dd(b), dd(s)))


def build(which):
    G = "grade-4"
    if which == "fadd":
        return unit(G, "adding-and-subtracting-fractions", 13, "[4수01-15]",
                    "분모가 같은 분수의 덧셈과 뺄셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                    "분모가 같은 분수의 덧셈과 뺄셈", "분수의 덧셈과 뺄셈",
                    "초등 4학년 2학기 분수의 덧셈과 뺄셈 학습지: 분모가 같은 진분수, 대분수의 덧셈과 뺄셈, 받아올림과 받아내림, 1에서 빼기, 문장제까지 100문제와 정답.",
                    "분모는 그대로, 분자끼리 계산", "대분수는 자연수끼리, 분수끼리 계산해요.",
                    ["분모가 같은 분수는 단위분수의 개수로 생각해요. <span class='fr'><span class='fn'>2</span><span class='fd'>7</span></span>은 <span class='fr'><span class='fn'>1</span><span class='fd'>7</span></span>이 2개예요.",
                     "그래서 <b>분모는 그대로 두고 분자끼리</b> 더하거나 빼요. 결과가 가분수이면 대분수로 바꿔요.",
                     "대분수는 자연수끼리, 분수끼리 계산해요. 분수끼리 더해서 1이 넘으면 받아올림해요.",
                     "분수끼리 뺄 수 없으면 자연수에서 1을 받아내림하거나, 대분수를 가분수로 바꾸어 계산해요."],
                    [("3<span class='fr'><span class='fn'>1</span><span class='fd'>5</span></span> − 1<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span>",
                      ["1/5에서 3/5을 뺄 수 없어요.", "3 1/5 = 2 6/5", "2 6/5 − 1 3/5 = 1 3/5"], "1<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span>")],
                    [("분모끼리도 더한다 (2/7 + 3/7 = 5/14)", "분모는 그대로 두고 분자끼리만 더해요. 5/7"),
                     ("받아내림을 하지 않고 큰 분자에서 작은 분자를 뺀다", "분수 부분을 뺄 수 없으면 자연수에서 1을 받아내림해요."),
                     ("1 − 3/8을 3/8로 쓴다", "1 = 8/8로 바꾸어 빼요. 5/8")],
                    [("분모가 다른 분수의 덧셈은 언제 배우나요?", "초등 5학년에서 통분을 배운 뒤에 계산해요. 4학년에서는 분모가 같은 분수만 다뤄요."),
                     ("답을 가분수로 써도 되나요?", "계산 결과는 보통 대분수로 나타내요. 이 학습지의 정답도 대분수로 썼어요.")],
                    [("진분수의 덧셈과 뺄셈", [(proper_add, 10), (proper_sub, 10)]),
                     ("1과 자연수에서 빼기", [(one_minus, 12), (frac_missing, 8)]),
                     ("대분수의 덧셈", [(mixed_add(False), 10), (mixed_add(True), 10)]),
                     ("대분수의 뺄셈", [(mixed_sub(False), 8), (mixed_sub(True), 8), (mixed_minus_improper, 4)]),
                     ("문장제", [(frac_story, 20)])], 82413)
    if which == "dec":
        return unit(G, "decimals-hundredths-and-thousandths", 15, "[4수01-13] [4수01-14]",
                    "분모가 100, 1000인 분수를 소수로 나타내고 읽고 쓸 수 있다. 소수의 크기를 비교할 수 있다.",
                    "소수 두 자리 수와 소수 세 자리 수", "소수 두・세 자리 수",
                    "초등 4학년 2학기 소수 학습지: 0.01과 0.001, 소수 두 자리 수와 세 자리 수 읽고 쓰기, 자릿값, 크기 비교, 10배와 1/10, 단위 바꾸기까지 100문제와 정답.",
                    "0.01은 1/100, 0.001은 1/1000", "자연수 부분부터 차례로 비교해요.",
                    ["분수 <span class='fr'><span class='fn'>1</span><span class='fd'>100</span></span>을 <b>0.01</b>, <span class='fr'><span class='fn'>1</span><span class='fd'>1000</span></span>을 <b>0.001</b>이라고 써요.",
                     "2.47은 「이 점 사칠」이라고 읽어요. 소수점 아래는 숫자를 하나씩 읽어요.",
                     "크기를 비교할 때는 자연수 부분, 소수 첫째 자리, 둘째 자리, 셋째 자리 순서로 비교해요.",
                     "어떤 수를 10배 하면 소수점이 오른쪽으로 한 칸, <span class='fr'><span class='fn'>1</span><span class='fd'>10</span></span>로 하면 왼쪽으로 한 칸 옮겨져요."],
                    [("3.408에서 숫자 8이 나타내는 수는?", ["8은 소수 셋째 자리 숫자", "0.008을 나타내요."], "0.008"),
                     ("0.7과 0.65 중 더 큰 수는?", ["소수 첫째 자리: 7 > 6"], "0.7")],
                    [("자릿수가 많은 소수가 크다고 생각한다 (0.65 > 0.7)", "소수 첫째 자리부터 비교해요. 0.7 > 0.65"),
                     ("2.05를 2.5와 같다고 생각한다", "2.05는 0.01이 205개, 2.5는 0.01이 250개예요."),
                     ("소수점 아래를 자연수처럼 읽는다 (사십칠)", "소수점 아래는 숫자만 하나씩 읽어요.")],
                    [("소수 두 자리 수는 몇 학년에서 배우나요?", "3학년에서 소수 한 자리 수를 배우고, 4학년 2학기에 소수 두 자리 수와 세 자리 수를 배워요."),
                     ("소수 끝의 0은 왜 생략할 수 있나요?", "0.50은 0.01이 50개, 0.5는 0.1이 5개로 크기가 같기 때문이에요.")],
                    [("소수 읽고 쓰기", [(dec_read, 12), (dec_count, 8)]),
                     ("자릿값", [(dec_place, 14), (dec_line, 6)]),
                     ("크기 비교", [(dec_cmp, 12), (dec_max, 8)]),
                     ("10배와 1/10", [(dec_tenfold, 14), (dec_zero, 6)]),
                     ("단위와 소수", [(dec_units, 20)])], 82415)
    return unit(G, "adding-and-subtracting-decimals", 16, "[4수01-16]",
                "소수의 덧셈과 뺄셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.",
                "소수의 덧셈과 뺄셈", "소수의 덧셈과 뺄셈",
                "초등 4학년 2학기 소수의 덧셈과 뺄셈 학습지: 소수 한 자리 수, 두 자리 수의 덧셈과 뺄셈, 자릿수가 다른 소수의 계산, 자연수에서 소수 빼기, 문장제까지 100문제와 정답.",
                "소수점을 맞추어 세로로 계산", "빈자리는 0이 있다고 생각해요.",
                ["소수의 덧셈과 뺄셈은 <b>소수점의 자리를 맞추어</b> 세로로 써서 계산해요.",
                 "같은 자리 수끼리 더하거나 빼고, 받아올림과 받아내림은 자연수와 같아요.",
                 "자릿수가 다르면 빈자리에 0이 있다고 생각해요. 3.4 − 1.25는 3.40 − 1.25예요.",
                 "답의 소수점은 위의 소수점에 맞추어 찍어요."],
                [("3.4 − 1.25", ["3.40 − 1.25", "소수점을 맞추어 빼면 2.15"], "2.15"),
                 ("0.8 + 0.47", ["0.80 + 0.47 = 1.27"], "1.27")],
                [("끝자리를 맞추어 계산한다 (0.8 + 0.47 = 0.55)", "소수점을 맞추면 0.80 + 0.47 = 1.27이에요."),
                 ("빈자리에서 받아내림하지 않는다", "빈자리를 0으로 생각하고 받아내림해요."),
                 ("자연수 5를 0.5로 생각한다", "5 = 5.0이에요. 5 − 1.2 = 3.8")],
                [("소수의 곱셈과 나눗셈은 언제 배우나요?", "5학년에서 소수의 곱셈, 6학년에서 소수의 나눗셈을 배워요."),
                 ("계산이 맞는지 확인하는 방법은?", "어림해 보세요. 3.4 − 1.25는 약 3 − 1 = 2이니 2.15가 알맞아요.")],
                [("소수 한 자리 수", [(dec_add(1, 1), 10), (dec_sub(1, 1), 10)]),
                 ("소수 두 자리 수", [(dec_add(2, 2), 10), (dec_sub(2, 2), 10)]),
                 ("자릿수가 다른 소수", [(dec_add(1, 2), 10), (dec_sub(2, 1), 5), (dec_sub(1, 2), 5)]),
                 ("자연수와 소수, □ 구하기", [(int_minus_dec, 10), (dec_missing, 10)]),
                 ("문장제", [(dec_story, 20)])], 82416)
