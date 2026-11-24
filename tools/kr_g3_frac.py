# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：분수와 소수（2022 개정 [4수01-09]〜[4수01-12]、[4수01-14]）の 5 単元
  fractions      : 분수의 뜻（3-1）
  decimals       : 소수 한 자리 수（3-1）
  kinds          : 단위분수, 진분수, 가분수, 대분수（3-2）
  compare        : 분수의 크기 비교（3-2）
  of_number      : 분수만큼은 얼마인가요（3-2）
誤答は「분자と분모を逆にする」「색칠하지 않은 부분を数える」「분모が大きいほど大きい（단위분수）」「0.1 × 10 = 0.10」から作る。
"""
import random
from fractions import Fraction as F
from kr_common import mcq, unit, Names, josa, fr, ff, dnum, num
from kr_pics import frac_bar, frac_circle, number_line, groups, fig, svg_wrap, INK, LIGHT

R = random.Random(82308)
NM = Names(R)


def pic(n, d):
    return frac_circle(n, d) if d <= 8 and R.random() < 0.5 else frac_bar(n, d)


# ---------------------------------------------------------------- 분수의 뜻
def shaded():
    d = R.randint(2, 10)
    n = R.randint(1, d - 1)
    k = R.choice(["shade", "unshaded"])
    if k == "shade":
        return mcq(pic(n, d) + "색칠한 부분은 전체의 얼마인가요?", fr(n, d), [fr(d, n), fr(d - n, d) if d - n != n else fr(n, d + 1), fr(n, d + 1) if d - n != n else fr(n + 1, d)],
                   "전체를 똑같이 %d로 나눈 것 중의 %d이에요. <b>%d분의 %d</b>" % (d, n, d, n))
    return mcq(pic(n, d) + "색칠하지 않은 부분은 전체의 얼마인가요?", fr(d - n, d), [fr(n, d) if n != d - n else fr(n, d + 1), fr(d, d - n), fr(d - n, d + 1)],
               "색칠하지 않은 부분은 %d칸 중 %d칸이에요. <b>%d분의 %d</b>" % (d, d - n, d, d - n))


def read_frac():
    d = R.randint(2, 12)
    n = R.randint(1, d - 1)
    if R.random() < 0.5:
        return mcq("분수 %s를 바르게 읽은 것은?" % fr(n, d), "%d분의 %d" % (d, n), ["%d분의 %d" % (n, d), "%d의 %d" % (d, n), "%d분의 %d" % (d, n + 1)],
                   "분모를 먼저, 분자를 나중에 읽어요. <b>%d분의 %d</b>" % (d, n))
    k = R.choice(["분모", "분자"])
    return mcq("분수 %s에서 %s는 얼마인가요?" % (fr(n, d), k), str(d if k == "분모" else n), [str(n if k == "분모" else d), str(d + n), str((d if k == "분모" else n) + 1)],
               "가로선 아래에 있는 수가 분모(%d), 위에 있는 수가 분자(%d)예요." % (d, n))


def equal_parts():
    """똑같이 나누었나요?"""
    d = R.choice([2, 3, 4, 6])
    ok = R.random() < 0.5
    W = 300
    s = ""
    if ok:
        w = (W - 20) / float(d)
        cuts = [10 + w * i for i in range(d + 1)]
    else:
        cuts = sorted([10, W - 10] + R.sample(range(40, W - 40, 30), d - 1))
        widths = [cuts[i + 1] - cuts[i] for i in range(d)]
        if max(widths) - min(widths) < 25:
            return None
    for i in range(d):
        s += "<rect x='%.1f' y='10' width='%.1f' height='50' fill='%s' stroke='%s' stroke-width='2'/>" % (cuts[i], cuts[i + 1] - cuts[i], LIGHT, INK)
    f = fig(svg_wrap(W, 70, s, "%d조각으로 나눈 막대" % d))
    if ok:
        return mcq(f + "막대를 %d조각으로 나누었어요. 똑같이 나누었나요? (조각 하나는 전체의 %s)" % (d, fr(1, d)), "똑같이 나누었어요", ["똑같이 나누지 않았어요", "조각이 너무 많아요", "알 수 없어요"],
                   "조각의 크기와 모양이 모두 같아요. 조각 하나는 전체의 <b>%d분의 1</b>이에요." % d)
    return mcq(f + "막대를 %d조각으로 나누었어요. 조각 하나를 전체의 %s이라고 할 수 있나요?" % (d, fr(1, d)), "없어요. 똑같이 나누지 않았어요",
               ["있어요. 조각이 %d개예요" % d, "있어요. 막대를 나누었어요", "조각을 세어 봐야 해요"],
               "조각의 크기가 서로 달라요. 분수는 전체를 <b>똑같이</b> 나누었을 때만 쓸 수 있어요.")


def rest():
    d = R.randint(3, 12)
    n = R.randint(1, d - 2)
    thing = R.choice(["피자", "케이크", "떡", "초콜릿", "수박"])
    who = NM.next()
    return mcq("%s %s 한 판을 똑같이 %d조각으로 나누어 그중 %d조각을 먹었어요. 남은 %s는 전체의 얼마인가요?" % (josa(who, "은/는"), thing, d, n, thing),
               fr(d - n, d), [fr(n, d), fr(d, d - n), fr(d - n, n) if n > 1 else fr(d - n, d + 1)],
               "%d조각 중 %d조각이 남았어요. <b>%d분의 %d</b>" % (d, d - n, d, d - n))


# ---------------------------------------------------------------- 소수
def dec_pic():
    n = R.randint(1, 9)
    w = R.random() < 0.3
    whole = R.randint(1, 3) if w else 0
    val = whole + n / 10.0
    s = ""
    for b in range(whole + 1):
        for i in range(10):
            on = b < whole or i < n
            s += "<rect x='%d' y='%d' width='26' height='34' fill='%s' stroke='%s' stroke-width='1.5'/>" % (10 + i * 26, 10 + b * 44, "#8fd0a8" if on else "#fff", INK)
    f = fig(svg_wrap(280, 20 + (whole + 1) * 44, s, "색칠한 칸"))
    ans = dnum(val)
    return mcq(f + "한 줄이 1이에요. 색칠한 부분을 소수로 나타내면?", ans, [dnum(whole + n / 100.0) if True else "", str(whole * 10 + n) if whole else str(n), dnum(val + 0.1), dnum(whole + (10 - n) / 10.0) if n != 5 else dnum(val + 0.2)],
               "1을 똑같이 10칸으로 나눈 한 칸은 0.1이에요. %s0.1이 %d개이니까 <b>%s</b>" % ("1이 %d개, " % whole if whole else "", n, ans))


def dec_frac():
    n = R.randint(1, 9)
    if R.random() < 0.5:
        return mcq("%s을 소수로 나타내면?" % fr(n, 10), "0.%d" % n, ["0.%d" % (10 - n) if n != 5 else "0.4", "%d.1" % n, "1.%d" % n],
                   "%s = 0.%d이에요. 분모가 10인 분수는 소수 한 자리 수로 나타낼 수 있어요." % (fr(n, 10), n))
    return mcq("0.%d를 분수로 나타내면?" % n, fr(n, 10), [fr(1, n) if n > 1 else fr(10, n), fr(n, 100), fr(10, n)],
               "0.%d는 0.1이 %d개예요. <b>%s</b>" % (n, n, fr(n, 10)))


def dec_count():
    a, b = R.randint(0, 9), R.randint(1, 9)
    v = a + b / 10.0
    k = R.choice(["count", "make"])
    if k == "count":
        t = a * 10 + b
        return mcq("%s는 0.1이 몇 개인 수인가요?" % dnum(v), "%d개" % t, ["%d개" % x for x in (b, t + 1, a + b, t * 10) if x != t],
                   "1은 0.1이 10개예요. %s는 0.1이 <b>%d개</b>예요." % (dnum(v), t))
    t = a * 10 + b
    return mcq("0.1이 %d개인 수는?" % t, dnum(v), [dnum(t / 100.0) if t < 100 else dnum(v + 1), str(t), dnum(v + 0.1)],
               "0.1이 10개이면 1이에요. 0.1이 %d개이면 <b>%s</b>예요." % (t, dnum(v)))


def dec_cm():
    c, m = R.randint(0, 15), R.randint(1, 9)
    if R.random() < 0.5:
        return mcq("%s를 cm로 나타내면 몇 cm인가요?" % ("%d cm %d mm" % (c, m) if c else "%d mm" % m), "%s cm" % dnum(c + m / 10.0),
                   ["%s cm" % x for x in (dnum(c + m / 100.0), "%d%d" % (c, m) if c else "%d" % m, dnum(m + c / 10.0) if c < 10 else dnum(c + 1 + m / 10.0))],
                   "1 mm = 0.1 cm예요. %d mm = 0.%d cm이니까 <b>%s cm</b>" % (m, m, dnum(c + m / 10.0)))
    return mcq("%s cm는 몇 cm 몇 mm인가요?" % dnum(c + m / 10.0), "%d cm %d mm" % (c, m) if c else "%d mm" % m,
               ["%d cm %d mm" % (m, c) if c else "%d cm" % m, "%d cm %d mm" % (c + 1, m), "%d mm" % (c * 100 + m)],
               "0.1 cm = 1 mm예요. 소수점 아래 숫자 %d는 %d mm예요." % (m, m))


def dec_line():
    a = R.randint(0, 4)
    n = R.randint(1, 9)
    lab = {0: str(a), 10: str(a + 1)}
    f = number_line(a, a + 1, 10, [(n, "?")], lab)
    v = a + n / 10.0
    return mcq(f + "?에 알맞은 소수는?", dnum(v), [dnum(a + n / 100.0), dnum(v + 0.1), dnum(a + 1 + n / 10.0)],
               "%d과 %d 사이를 10칸으로 나눈 한 칸은 0.1이에요. %d칸이니까 <b>%s</b>" % (a, a + 1, n, dnum(v)))


def dec_cmp():
    a, b = R.randint(1, 99), R.randint(1, 99)
    if a == b or a % 10 == 0 or b % 10 == 0:
        return None
    x, y = a / 10.0, b / 10.0
    big = dnum(max(x, y))
    return mcq("더 큰 수는? %s, %s" % (dnum(x), dnum(y)), big, [dnum(min(x, y)), "두 수가 같아요", "알 수 없어요"],
               "자연수 부분을 먼저 비교하고, 같으면 소수 부분을 비교해요. <b>%s</b>가 더 커요." % big)


# ---------------------------------------------------------------- 진분수, 가분수, 대분수
def kind_name():
    d = R.randint(2, 9)
    k = R.choice(["unit", "proper", "improper", "mixed", "improper_eq"])
    if k == "unit":
        x, ans = fr(1, d), "단위분수"
    elif k == "proper":
        n = R.randint(2, d - 1) if d > 2 else 1
        x, ans = fr(n, d), "진분수" if n > 1 else "단위분수"
    elif k == "improper":
        n = R.randint(d + 1, d * 3)
        x, ans = fr(n, d), "가분수"
    elif k == "improper_eq":
        x, ans = fr(d, d), "가분수"
    else:
        x, ans = "%d%s" % (R.randint(1, 4), fr(R.randint(1, d - 1), d)), "대분수"
    return mcq("%s는 어떤 분수인가요?" % x, ans, [y for y in ("단위분수", "진분수", "가분수", "대분수") if y != ans],
               {"단위분수": "분자가 1인 분수는 <b>단위분수</b>예요.", "진분수": "분자가 분모보다 작은 분수는 <b>진분수</b>예요.",
                "가분수": "분자가 분모와 같거나 분모보다 큰 분수는 <b>가분수</b>예요.", "대분수": "자연수와 진분수로 이루어진 분수는 <b>대분수</b>예요."}[ans])


def to_mixed(kind):
    d = R.randint(2, 9)
    w, r = R.randint(1, 5), R.randint(1, d - 1)
    n = w * d + r
    if kind == "i2m":
        return mcq("가분수 %s를 대분수로 나타내면?" % fr(n, d), "%d%s" % (w, fr(r, d)), ["%d%s" % (r, fr(w, d)) if w < d else "%d%s" % (w + 1, fr(r, d)), "%d%s" % (w - 1, fr(r + d, d)) if w > 1 else "%d%s" % (w, fr(r, d + 1)), "%d%s" % (w, fr(d - r, d)) if d - r != r else "%d%s" % (w + 1, fr(r, d))],
                   "%d ÷ %d = %d … %d이에요. 자연수 %d와 %s로 나타내요. <b>%d%s</b>" % (n, d, w, r, w, fr(r, d), w, fr(r, d)))
    return mcq("대분수 %d%s를 가분수로 나타내면?" % (w, fr(r, d)), fr(n, d), [fr(w + r, d), fr(w * r + d, d) if w * r + d != n else fr(n + 1, d), fr(n, d + 1)],
               "%d = %s이니까 %d%s = %s + %s = <b>%s</b>" % (w, fr(w * d, d), w, fr(r, d), fr(w * d, d), fr(r, d), fr(n, d)))


def whole_as_frac():
    d, w = R.randint(2, 9), R.randint(1, 4)
    return mcq("자연수 %d를 분모가 %d인 가분수로 나타내면?" % (w, d), fr(w * d, d), [fr(w, d), fr(d, w) if d != w else fr(w + d, d), fr(w + d, d)],
               "1 = %s이니까 %d = <b>%s</b>예요." % (fr(d, d), w, fr(w * d, d)))


def count_units():
    d = R.randint(3, 9)
    n = R.randint(2, d * 3)
    return mcq("%s는 %s이 몇 개인 수인가요?" % (fr(n, d), fr(1, d)), "%d개" % n, ["%d개" % x for x in (d, n + d, n - 1, n + 1) if x != n and x > 0],
               "%s는 %s이 <b>%d개</b>예요." % (fr(n, d), fr(1, d), n))


# ---------------------------------------------------------------- 크기 비교
def cmp_same_den():
    d = R.randint(3, 12)
    a, b = R.sample(range(1, d * 2), 2)
    big = fr(max(a, b), d)
    return mcq("더 큰 분수는? %s, %s" % (fr(a, d), fr(b, d)), big, [fr(min(a, b), d), "두 분수가 같아요", "알 수 없어요"],
               "분모가 같으면 <b>분자가 클수록</b> 큰 분수예요. %d와 %d를 비교해요." % (a, b))


def cmp_unit():
    a, b = R.sample(range(2, 13), 2)
    big = fr(1, min(a, b))
    return mcq("더 큰 분수는? %s, %s" % (fr(1, a), fr(1, b)), big, [fr(1, max(a, b)), "두 분수가 같아요", "분모가 큰 쪽"],
               "단위분수는 <b>분모가 작을수록</b> 커요. 피자를 적게 나눌수록 한 조각이 크니까요. <b>%s</b>" % big)


def cmp_mixed():
    d = R.randint(3, 9)
    k = R.choice(["mix_imp", "mix_mix"])
    if k == "mix_imp":
        w, r = R.randint(1, 4), R.randint(1, d - 1)
        n = w * d + r + R.choice([-2, -1, 1, 2])
        if n <= d or n == w * d + r:
            return None
        x, y = "%d%s" % (w, fr(r, d)), fr(n, d)
        big = x if w * d + r > n else y
        return mcq("더 큰 분수는? %s, %s" % (x, y), big, [y if big == x else x, "두 분수가 같아요", "알 수 없어요"],
                   "%s를 가분수로 바꾸면 %s예요. 분자 %d와 %d를 비교해요. <b>%s</b>" % (x, fr(w * d + r, d), w * d + r, n, big))
    w1, w2 = R.randint(1, 5), R.randint(1, 5)
    r1, r2 = R.randint(1, d - 1), R.randint(1, d - 1)
    if (w1, r1) == (w2, r2):
        return None
    x, y = "%d%s" % (w1, fr(r1, d)), "%d%s" % (w2, fr(r2, d))
    big = x if (w1, r1) > (w2, r2) else y
    return mcq("더 큰 분수는? %s, %s" % (x, y), big, [y if big == x else x, "두 분수가 같아요", "알 수 없어요"],
               "대분수는 자연수 부분을 먼저 비교하고, 같으면 분수 부분을 비교해요. <b>%s</b>" % big)


def order():
    d = R.randint(5, 12)
    ns = R.sample(range(1, d * 2), 4)
    xs = [fr(n, d) for n in ns]
    big = fr(max(ns), d)
    small = fr(min(ns), d)
    if R.random() < 0.5:
        return mcq("가장 큰 분수는? %s" % ", ".join(xs), big, [x for x in xs if x != big], "분모가 같으니 분자가 가장 큰 <b>%s</b>예요." % big)
    return mcq("가장 작은 분수는? %s" % ", ".join(xs), small, [x for x in xs if x != small], "분모가 같으니 분자가 가장 작은 <b>%s</b>예요." % small)


def cmp_story():
    a, b = R.sample(range(2, 10), 2)
    w1, w2 = NM.next(), NM.next()
    big = w1 if a < b else w2
    t = "같은 크기의 피자를 %s %d조각으로, %s %d조각으로 똑같이 나누어 한 조각씩 먹었어요. 더 많이 먹은 사람은 누구인가요?" % (josa(w1, "은/는"), a, josa(w2, "은/는"), b)
    return mcq(t, big, [w2 if big == w1 else w1, "똑같이 먹었어요", "알 수 없어요"],
               "%s과 %s 중 분모가 작은 %s이 더 커요. <b>%s</b>" % (fr(1, a), fr(1, b), fr(1, min(a, b)), big))


# ---------------------------------------------------------------- 분수만큼은 얼마
def of_num():
    d = R.choice([2, 3, 4, 5, 6, 8])
    k = R.randint(2, 6)
    total = d * k
    n = R.randint(1, d - 1)
    kind = R.choice(["apple", "star", "button", "flower", "heart", "ball"])
    from kr_pics import KO
    nm, c = KO[kind]
    f = groups([(k, kind)] * d) if total <= 30 else ""
    return mcq(f + "%s %d%s의 %s은 몇 %s인가요?" % (nm, total, c, fr(n, d), c), "%d%s" % (k * n, c),
               ["%d%s" % x for x in ((k, c), (total - k * n, c), (n * d, c), (k * n + k, c)) if x[0] != k * n and x[0] > 0],
               "%d을 똑같이 %d묶음으로 나누면 한 묶음은 %d이에요. %s은 %d묶음이니까 %d × %d = <b>%d</b>" % (total, d, k, fr(n, d), n, k, n, k * n))


def of_part():
    d = R.choice([2, 3, 4, 5, 6])
    k = R.randint(2, 8)
    n = R.randint(1, d - 1)
    total = d * k
    k2 = R.choice(["m", "cm", "시간"])
    if k2 == "시간":
        if 60 % d:
            return None
        m = 60 // d * n
        return mcq("1시간의 %s은 몇 분인가요?" % fr(n, d), "%d분" % m,
                   ["%d분" % x for x in (60 // d, 60 - m, n * 10, m + 5) if x != m and x > 0],
                   "1시간 = 60분이에요. 60 ÷ %d × %d = <b>%d분</b>" % (d, n, m))
    u = k2
    return mcq("%d %s의 %s은 몇 %s인가요?" % (total, u, fr(n, d), u), "%d %s" % (k * n, u),
               ["%d %s" % (x, u) for x in (k, total - k * n, total * n, k * n + 1) if x != k * n and x > 0],
               ("%d을 %d로 나누면 <b>%d %s</b>" % (total, d, k, u)) if n == 1 else "%d을 %d로 나누면 %d, %s은 그것의 %d배이니까 <b>%d %s</b>" % (total, d, k, fr(n, d), n, k * n, u))


def of_story():
    d = R.choice([2, 3, 4, 5, 6])
    k = R.randint(2, 9)
    n = R.randint(1, d - 1)
    total = d * k
    who = NM.next()
    t = R.choice(["%s 색종이 %d장 중 %s을 사용했어요. 사용한 색종이는 몇 장인가요?", "%s 구슬 %d개의 %s을 동생에게 주었어요. 동생에게 준 구슬은 몇 개인가요?",
                  "%s 딸기 %d개 중 %s을 먹었어요. 먹은 딸기는 몇 개인가요?"])
    u = "장" if "색종이" in t else "개"
    return mcq(t % (josa(who, "은/는"), total, fr(n, d)), "%d%s" % (k * n, u),
               ["%d%s" % (x, u) for x in (k, total - k * n, n * d, k * n + n) if x != k * n and x > 0],
               "%d을 %d묶음으로 똑같이 나누면 한 묶음은 %d. %s은 %d × %d = <b>%d%s</b>" % (total, d, k, fr(n, d), k, n, k * n, u))


def build(which):
    if which == "fractions":
        return unit("grade-3", "fractions", 8, "[4수01-09]",
                    "양의 등분할을 통하여 분수의 필요성을 인식하고, 분수를 이해하고 읽고 쓸 수 있다.",
                    "분수의 뜻", "분수",
                    "초등 3학년 분수 학습지: 똑같이 나누기, 색칠한 부분을 분수로 나타내기, 분수 읽기와 분모·분자, 남은 부분, 문장제까지 100문제와 정답.",
                    "전체를 똑같이 나눈 것 중의 몇", "3/4은 4분의 3이라고 읽어요.",
                    ["전체를 <b>똑같이</b> 4로 나눈 것 중의 1을 <b>4분의 1</b>이라고 하고 1/4로 써요.",
                     "똑같이 4로 나눈 것 중의 3은 <b>4분의 3</b>, 3/4이에요. 아래의 수 4는 <b>분모</b>, 위의 수 3은 <b>분자</b>예요.",
                     "크기가 다르게 나누었으면 분수로 나타낼 수 없어요."],
                    [("피자를 똑같이 8조각으로 나누어 3조각을 먹었어요. 먹은 피자는 전체의 얼마인가요?", ["똑같이 8로 나눈 것 중의 3이에요."], "8분의 3"),
                     ("남은 피자는 전체의 얼마인가요?", ["8조각 중 5조각이 남았어요."], "8분의 5")],
                    [("분모와 분자를 바꾸어 쓴다", "전체를 나눈 수가 분모(아래), 부분의 수가 분자(위)예요."),
                     ("크기가 다른 조각도 분수로 나타낸다", "분수는 똑같이 나누었을 때만 쓸 수 있어요."),
                     ("4분의 3을 3분의 4라고 읽는다", "분모를 먼저 읽어요. 3/4은 4분의 3이에요.")],
                    [("분수는 언제 처음 배우나요?", "초등 3학년 1학기 「분수와 소수」 단원에서 처음 배워요. 2학기에 진분수, 가분수, 대분수와 분수의 크기 비교를 배워요."),
                     ("분모와 분자는 무엇인가요?", "가로선 아래의 수가 분모로 전체를 똑같이 나눈 수이고, 위의 수가 분자로 그중 몇 개인지를 나타내요.")],
                    [("색칠한 부분", [(shaded, 20)]),
                     ("분수 읽기와 분모, 분자", [(read_frac, 20)]),
                     ("똑같이 나누었나요?", [(equal_parts, 10), (shaded, 10)]),
                     ("남은 부분", [(rest, 12), (shaded, 8)]),
                     ("문장제", [(rest, 12), (read_frac, 8)])], 82308)
    if which == "decimals":
        return unit("grade-3", "decimals", 9, "[4수01-12] [4수01-14]",
                    "분모가 10인 진분수와 연결하여 소수 한 자리 수를 이해하고 읽고 쓸 수 있다. 소수의 크기를 비교하고 그 방법을 설명할 수 있다.",
                    "소수 한 자리 수", "소수",
                    "초등 3학년 소수 학습지: 0.1의 뜻, 분모가 10인 분수와 소수, 0.1이 몇 개인 수, cm와 mm를 소수로, 수직선, 소수의 크기 비교까지 100문제와 정답.",
                    "1/10 = 0.1, 0.1이 10개면 1", "1 mm = 0.1 cm",
                    ["1을 똑같이 10으로 나눈 것 중의 1은 1/10이고, 소수로 <b>0.1</b>이라 쓰고 「영점 일」이라고 읽어요.",
                     "0.1이 3개이면 0.3, 0.1이 10개이면 1, 0.1이 23개이면 2.3이에요.",
                     "2.3처럼 쓴 수를 소수라 하고, 「.」을 <b>소수점</b>이라고 해요.",
                     "소수의 크기는 <b>자연수 부분을 먼저</b>, 같으면 소수 부분을 비교해요."],
                    [("4 cm 7 mm는 몇 cm인가요?", ["1 mm = 0.1 cm이니까 7 mm = 0.7 cm", "4 + 0.7 = 4.7"], "4.7 cm"),
                     ("2.6과 3.1 중 더 큰 수는?", ["자연수 부분 2 < 3"], "3.1")],
                    [("0.1이 12개인 수를 0.12라고 한다", "0.1이 10개이면 1이에요. 0.1이 12개이면 1.2예요."),
                     ("2.9보다 2.10이 크다고 생각한다", "소수 한 자리 수끼리 비교해요. 0.1이 몇 개인지 생각해요."),
                     ("5 mm를 5 cm라고 한다", "5 mm = 0.5 cm예요.")],
                    [("소수는 언제 처음 배우나요?", "초등 3학년 1학기에 분모가 10인 분수와 함께 소수 한 자리 수를 배워요. 소수 두 자리, 세 자리 수는 4학년에서 배워요."),
                     ("0.5는 어떻게 읽나요?", "「영점 오」라고 읽어요. 2.5는 「이점 오」예요.")],
                    [("그림과 소수", [(dec_pic, 20)]),
                     ("분수와 소수", [(dec_frac, 14), (dec_count, 6)]),
                     ("0.1이 몇 개", [(dec_count, 14), (dec_line, 6)]),
                     ("cm와 mm, 수직선", [(dec_cm, 12), (dec_line, 8)]),
                     ("소수의 크기 비교", [(dec_cmp, 20)])], 82309)
    if which == "kinds":
        return unit("grade-3", "proper-improper-and-mixed-fractions", 16, "[4수01-10]",
                    "단위분수, 진분수, 가분수, 대분수를 알고, 그 관계를 이해한다.",
                    "진분수, 가분수, 대분수", "진분수, 가분수, 대분수",
                    "초등 3학년 2학기 분수 학습지: 단위분수, 진분수, 가분수, 대분수 구별하기, 가분수를 대분수로, 대분수를 가분수로 바꾸기까지 100문제와 정답.",
                    "분자가 분모보다 작으면 진분수", "같거나 크면 가분수, 자연수 + 진분수는 대분수",
                    ["분자가 1인 분수는 <b>단위분수</b>, 분자가 분모보다 작은 분수는 <b>진분수</b>예요.",
                     "분자가 분모와 같거나 분모보다 큰 분수는 <b>가분수</b>예요. 4/4 = 1이에요.",
                     "1과 3/4처럼 자연수와 진분수로 이루어진 분수는 <b>대분수</b>예요.",
                     "가분수 → 대분수: 분자 ÷ 분모의 몫이 자연수, 나머지가 분자예요. 11/4 = 2와 3/4"],
                    [("13/5를 대분수로 나타내면?", ["13 ÷ 5 = 2 … 3"], "2와 5분의 3"),
                     ("3과 2/7을 가분수로 나타내면?", ["3 = 21/7", "21/7 + 2/7 = 23/7"], "7분의 23")],
                    [("5/5를 진분수라고 한다", "분자와 분모가 같으면 가분수예요. 5/5 = 1이에요."),
                     ("2와 3/4을 가분수로 바꿀 때 2 + 3 = 5로 분자를 5라고 한다", "2 = 8/4이에요. 8 + 3 = 11, 11/4예요."),
                     ("11/4을 대분수로 바꿀 때 몫과 나머지를 바꾸어 쓴다", "몫 2가 자연수, 나머지 3이 분자예요.")],
                    [("가분수와 대분수는 언제 배우나요?", "초등 3학년 2학기 「분수」 단원에서 배워요. 1학기에 배운 분수의 뜻을 넓혀요."),
                     ("가분수를 대분수로 바꾸는 쉬운 방법은?", "분자를 분모로 나누세요. 몫은 자연수, 나머지는 분자가 되고 분모는 그대로예요.")],
                    [("분수의 종류", [(kind_name, 20)]),
                     ("단위분수가 몇 개", [(count_units, 14), (kind_name, 6)]),
                     ("가분수와 자연수", [(whole_as_frac, 10), (count_units, 10)]),
                     ("가분수를 대분수로", [(lambda: to_mixed("i2m"), 20)]),
                     ("대분수를 가분수로", [(lambda: to_mixed("m2i"), 20)])], 82314)
    if which == "compare":
        return unit("grade-3", "comparing-fractions", 17, "[4수01-11]",
                    "분모가 같은 분수끼리, 단위분수끼리 크기를 비교하고 그 방법을 설명할 수 있다.",
                    "분수의 크기 비교", "분수의 크기 비교",
                    "초등 3학년 분수의 크기 비교 학습지: 분모가 같은 분수, 단위분수, 가분수와 대분수의 크기 비교, 가장 큰 분수 찾기, 문장제까지 100문제와 정답.",
                    "분모가 같으면 분자가 큰 쪽이 커요", "단위분수는 분모가 작을수록 커요.",
                    ["<b>분모가 같은 분수</b>는 분자가 클수록 커요. 5/8 > 3/8",
                     "<b>단위분수</b>는 분모가 작을수록 커요. 1/3 > 1/5 (적게 나눌수록 한 조각이 커요.)",
                     "가분수와 대분수를 비교할 때는 <b>한 가지 모양으로 바꾸어</b> 비교해요.",
                     "대분수끼리는 자연수 부분을 먼저 비교하고, 같으면 분수 부분을 비교해요."],
                    [("2와 1/4과 10/4 중 더 큰 수는?", ["2와 1/4 = 9/4", "9/4 < 10/4"], "10/4"),
                     ("1/6과 1/9 중 더 큰 수는?", ["단위분수는 분모가 작을수록 커요."], "1/6")],
                    [("1/9가 1/6보다 크다고 한다", "9조각으로 나눈 한 조각이 6조각으로 나눈 한 조각보다 작아요."),
                     ("분모가 다른 분수를 분자만 보고 비교한다", "3학년에서는 분모가 같거나 단위분수일 때 비교해요."),
                     ("대분수와 가분수를 그대로 비교한다", "가분수를 대분수로(또는 반대로) 바꾸어 비교해요.")],
                    [("분모가 다른 분수도 비교할 수 있나요?", "단위분수끼리는 3학년에서 비교해요. 분모가 다른 일반적인 분수의 비교는 5학년에서 통분을 배운 뒤에 해요."),
                     ("단위분수는 왜 분모가 작을수록 클까요?", "똑같은 피자를 3조각과 5조각으로 나누면 3조각으로 나눈 한 조각이 더 크기 때문이에요.")],
                    [("분모가 같은 분수", [(cmp_same_den, 20)]),
                     ("단위분수", [(cmp_unit, 20)]),
                     ("가분수와 대분수", [(cmp_mixed, 20)]),
                     ("가장 큰 분수, 가장 작은 분수", [(order, 20)]),
                     ("문장제", [(cmp_story, 12), (cmp_unit, 8)])], 82315)
    return unit("grade-3", "fraction-of-a-number", 15, "[4수01-09] [4수01-10]",
                "양의 등분할을 통하여 분수의 필요성을 인식하고, 분수를 이해하고 읽고 쓸 수 있다. 단위분수, 진분수, 가분수, 대분수를 알고, 그 관계를 이해한다.",
                "분수만큼은 얼마인가요", "분수만큼은 얼마",
                "초등 3학년 2학기 분수 학습지: 묶음으로 분수 알기, 12의 3/4은 얼마인지 구하기, m와 시간의 분수만큼, 문장제까지 100문제와 정답.",
                "똑같이 묶고, 분자만큼 세어요", "12의 3/4 → 12 ÷ 4 × 3 = 9",
                ["12를 똑같이 4묶음으로 나누면 한 묶음은 3이에요. 그래서 <b>12의 1/4은 3</b>이에요.",
                 "12의 3/4은 1/4이 3개이니까 3 × 3 = <b>9</b>예요.",
                 "<b>전체 ÷ 분모 × 분자</b>로 구할 수 있어요."],
                [("20의 2/5는 얼마인가요?", ["20 ÷ 5 = 4", "4 × 2 = 8"], "8"),
                 ("1시간의 1/4은 몇 분인가요?", ["60 ÷ 4 = 15"], "15분")],
                [("12의 3/4을 12 ÷ 3으로 구한다", "분모 4로 나누고 분자 3을 곱해요."),
                 ("한 묶음의 수를 답으로 쓴다", "분자만큼 묶음을 세어야 해요."),
                 ("남은 것과 가진 것을 헷갈린다", "문제에서 묻는 부분이 분자인지, 나머지 부분인지 확인해요.")],
                [("분수만큼은 얼마인지 어떻게 구하나요?", "전체를 분모만큼 똑같이 묶어 한 묶음의 수를 구하고, 분자만큼 더해요(곱해요)."),
                 ("언제 배우나요?", "초등 3학년 2학기 「분수」 단원의 첫 부분에서 배워요.")],
                [("그림으로 알아보기", [(of_num, 20)]),
                 ("분수만큼은 얼마", [(of_num, 20)]),
                 ("길이와 시간", [(of_part, 20)]),
                 ("문장제 1", [(of_story, 20)]),
                 ("문장제 2", [(of_story, 12), (of_part, 8)])], 82320)
