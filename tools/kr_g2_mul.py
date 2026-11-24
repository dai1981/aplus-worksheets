# -*- coding: utf-8 -*-
"""
대한민국 초등 2학년 수학：곱셈（2022 개정 [2수01-10] [2수01-11]）
  meaning: 곱셈（묶어 세기、몇의 몇 배、곱셈식）   2-1
  tables : 곱셈구구（2〜9단、1단、0의 곱、곱셈표） 2-2
誤答は「곱셈을 덧셈으로 한다（3 × 4 = 7）」「한 묶음 더 / 덜 센다（3 × 4 = 9, 15）」「몇씩과 몇 묶음을 바꾸어 말한다」
「0의 곱을 그 수라고 한다（0 × 5 = 5）」「1단을 1이라고 한다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa
from kr_low import KINDS, nm, cw, ko, near
import k_pics as K

R = random.Random(82210)
NM = Names(R)
G = "grade-2"
GRP = [("쿠키", "개", "접시", "담았어요"), ("사탕", "개", "봉지", "담았어요"), ("연필", "자루", "묶음", "묶었어요"), ("달걀", "개", "줄", "놓았어요"),
       ("꽃", "송이", "꽃병", "꽂았어요"), ("구슬", "개", "상자", "담았어요"), ("귤", "개", "바구니", "담았어요"), ("색종이", "장", "묶음", "묶었어요"),
       ("딸기", "개", "그릇", "담았어요"), ("만두", "개", "접시", "담았어요")]


def S(x):
    return str(x)


def groups(n, k, kind):
    return ko(K.groups_svg([(n, kind)] * k, 22), "%s %d%s씩 %d묶음" % (nm(kind), n, cw(kind), k))


def arr(r, c, kind):
    return ko(K.array_svg(r, c, kind), "%s %d줄, 한 줄에 %d%s씩" % (nm(kind), r, c, cw(kind)))


# ------------------------------------------------------------------ 곱셈의 뜻
def count_groups():
    def mk():
        n, k = R.randint(2, 5), R.randint(2, 5)
        kind = R.choice(KINDS)
        how = R.choice(["say", "all"])
        pic = groups(n, k, kind)
        if how == "say":
            ok = "%d씩 %d묶음" % (n, k)
            return mcq("%s 몇씩 몇 묶음일까요?%s" % (josa(nm(kind), "은/는"), pic), ok,
                       ["%d씩 %d묶음" % (k, n) if n != k else "%d씩 %d묶음" % (n, k + 1), "%d씩 %d묶음" % (n, k - 1 if k > 2 else k + 2), "%d씩 %d묶음" % (n + 1, k)],
                       "한 묶음에 %d%s씩, %d묶음이에요. <b>%s</b>" % (n, cw(kind), k, ok))
        return mcq("%s 모두 몇 %s일까요? (%d씩 뛰어 세어 보세요)%s" % (josa(nm(kind), "은/는"), cw(kind), n, pic), "%d%s" % (n * k, cw(kind)),
                   ["%d%s" % (x, cw(kind)) for x in (n + k, n * (k + 1), n * (k - 1), n * k + 1)],
                   "%s → <b>%d%s</b>" % (", ".join(str(n * i) for i in range(1, k + 1)), n * k, cw(kind)))
    return mk


def regroup():
    """같은 수를 여러 가지로 묶기：12는 2씩 6묶음, 3씩 4묶음…"""
    def mk():
        tot = R.choice([6, 8, 10, 12, 15, 16, 18, 20])
        ds = [d for d in range(2, 10) if tot % d == 0 and tot // d >= 2]
        d = R.choice(ds)
        ok = "%d씩 %d묶음" % (d, tot // d)
        bad = ["%d씩 %d묶음" % (x, y) for x in range(2, 10) for y in range(2, 10) if 0 < abs(x * y - tot) <= 2]
        R.shuffle(bad)
        kind = R.choice(KINDS)
        return mcq("%s %d%s를 똑같이 묶으려고 해요. 남는 것 없이 바르게 묶은 것은 무엇일까요?" % (nm(kind), tot, cw(kind)), ok, bad,
                   "%d씩 %d묶음은 %d이에요. <b>%s</b>" % (d, tot // d, tot, ok))
    return mk


def times_of():
    def mk():
        n, k = R.randint(2, 9), R.randint(2, 6)
        how = R.choice(["say", "val", "tower"])
        if how == "say":
            return mcq("<b>%d씩 %d묶음</b>은 %d의 몇 배일까요?" % (n, k, n), "%d배" % k, ["%d배" % x for x in (n, k + 1, k - 1 if k > 2 else k + 2, n * k)],
                       "%d씩 %d묶음은 %d의 <b>%d배</b>예요." % (n, k, n, k))
        if how == "val":
            return mcq("%d의 %d배는 얼마일까요?" % (n, k), S(n * k), [S(x) for x in (n + k, n * (k + 1), n * (k - 1), n * k + 1)],
                       "%d의 %d배는 %s = <b>%d</b>" % (n, k, " + ".join([str(n)] * k), n * k))
        a = R.randint(1, 3)
        b = a * k
        if b > 9:
            return None
        pic = ko(K.towers_svg([a, b], ["가", "나"]), "쌓기나무 탑")
        return mcq("나 탑의 높이는 가 탑의 높이의 몇 배일까요?%s" % pic, "%d배" % k, ["%d배" % x for x in (b, k + 1, b - a, k - 1 if k > 2 else k + 2) if x != k],
                   "가 탑 %d칸을 %d번 쌓으면 나 탑 %d칸이 돼요. <b>%d배</b>" % (a, k, b, k))
    return mk


def mul_expr():
    def mk():
        n, k = R.randint(2, 9), R.randint(2, 6)
        how = R.choice(["add", "read", "times"])
        if how == "add":
            ok = "%d × %d = %d" % (n, k, n * k)
            return mcq("<b>%s</b>를 곱셈식으로 나타낸 것은 무엇일까요?" % " + ".join([str(n)] * k), ok,
                       ["%d × %d = %d" % (n, k + 1, n * (k + 1)), "%d + %d = %d" % (n, k, n + k), "%d × %d = %d" % (k, k, k * k) if n != k else "%d × %d = %d" % (n, n + 1, n * (n + 1))],
                       "%d을 %d번 더했어요. <b>%s</b>" % (n, k, ok))
        if how == "read":
            ok = "%d 곱하기 %d" % (n, k)
            return mcq("<b>%d × %d</b>를 바르게 읽은 것은 무엇일까요?" % (n, k), ok, ["%d 더하기 %d" % (n, k), "%d 곱하기 %d" % (k, n) if n != k else "%d 곱하기 %d" % (n, k + 1), "%d 빼기 %d" % (n, k)],
                       "×는 '곱하기'라고 읽어요. <b>%s</b>" % ok)
        ok = "%d × %d" % (n, k)
        return mcq("<b>%d의 %d배</b>를 곱셈식으로 나타내면 무엇일까요?" % (n, k), ok, ["%d + %d" % (n, k), "%d × %d" % (n, n) if n != k else "%d × %d" % (n, k + 1), "%d × %d" % (n * k, k)],
                   "%d의 %d배는 <b>%s</b>예요." % (n, k, ok))
    return mk


def pic_expr():
    def mk():
        r, c = R.randint(2, 5), R.randint(2, 6)
        kind = R.choice(KINDS)
        how = R.choice(["arr", "grp"])
        if how == "arr":
            pic = arr(r, c, kind)
            ok = "%d × %d = %d" % (c, r, r * c)
            bad = ["%d + %d = %d" % (c, r, c + r), "%d × %d = %d" % (c, r + 1, c * (r + 1)), "%d × %d = %d" % (c, r, r * c + c)]
            return mcq("한 줄에 %d%s씩 %d줄 있어요. 알맞은 곱셈식은 무엇일까요?%s" % (c, cw(kind), r, pic), ok, bad,
                       "%d씩 %d줄이므로 %d의 %d배예요. <b>%s</b>" % (c, r, c, r, ok))
        pic = groups(r, c, kind)
        ok = "%d × %d = %d" % (r, c, r * c)
        return mcq("그림에 알맞은 곱셈식은 무엇일까요?%s" % pic, ok,
                   ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, c - 1, r * (c - 1)), "%d × %d = %d" % (r, c, r * c - 1)],
                   "%d씩 %d묶음이에요. <b>%s</b>" % (r, c, ok))
    return mk


def group_story(maxk=6):
    def mk():
        t, c, box, vb = R.choice(GRP)
        n, k = R.randint(2, 9), R.randint(2, maxk)
        q = "한 %s에 %s %d%s씩 %s %d%s의 %s 모두 몇 %s일까요?" % (box, josa(t, "을/를"), n, c, vb, k, box, josa(t, "은/는"), c)
        return mcq(q, "%d%s" % (n * k, c), ["%d%s" % (x, c) for x in (n + k, n * (k + 1), n * (k - 1), n * k + n // 2 + 1)],
                   "%d의 %d배예요. %d × %d = <b>%d</b>" % (n, k, n, k, n * k))
    return mk


# ------------------------------------------------------------------ 곱셈구구
def fact(tables, b_lo=1, b_hi=9):
    def mk():
        a = R.choice(tables)
        b = R.randint(b_lo, b_hi)
        p = a * b
        how = R.random()
        if how < 0.55:
            q = "%d × %d =" % (a, b)
        elif how < 0.8:
            q = "%d × □ = %d<br>□에 알맞은 수는 무엇일까요?" % (a, p)
            return mcq(q, S(b), [S(x) for x in (b + 1, b - 1, p - a, a)], "%d단에서 곱이 %d인 것은 %d × %d예요. <b>%d</b>" % (a, p, a, b, b))
        else:
            q = "%d의 %d배는 얼마일까요?" % (a, b)
        w = [a * (b + 1), a * (b - 1), a + b, (a + 1) * b, p + 1]
        if a == 0 or b == 0:
            w = [a + b, 1, 10, max(a, b) + 1]
        return mcq(q, S(p), [S(x) for x in w if x >= 0 and x != p],
                   ("%d단은 %d씩 커져요. %d × %d = <b>%d</b>" % (a, a, a, b, p)) if a > 1 else "%d × %d = <b>%d</b>" % (a, b, p))
    return mk


def skip_table(tables):
    def mk():
        a = R.choice(tables)
        st = R.randint(1, 5)
        seq = [a * i for i in range(st, st + 5)]
        p = R.randint(1, 4)
        ans = seq[p]
        shown = ", ".join(str(x) if i != p else "□" for i, x in enumerate(seq))
        return mcq("%d단 곱셈구구의 곱을 차례로 썼어요. □에 알맞은 수는 무엇일까요?<br><b>%s</b>" % (a, shown), S(ans),
                   [S(x) for x in (ans + 1, ans - 1, ans + a, ans - a, ans + 10) if x > 0 and x != ans],
                   "%d단의 곱은 %d씩 커져요. <b>%d</b>" % (a, a, ans))
    return mk


def zero_one():
    def mk():
        how = R.choice(["one", "zero", "zero2", "story"])
        b = R.randint(2, 9)
        if how == "one":
            return mcq("1 × %d =" % b, S(b), [S(x) for x in (1, b + 1, 1 + b, 10 + b, 0)], "1과 어떤 수의 곱은 항상 그 수예요. <b>%d</b>" % b)
        if how == "zero":
            return mcq("0 × %d =" % b, "0", [S(x) for x in (b, 1, b + 1)], "0과 어떤 수의 곱은 항상 0이에요. <b>0</b>")
        if how == "zero2":
            return mcq("%d × 0 =" % b, "0", [S(x) for x in (b, 1, b - 1 if b > 2 else 10)], "어떤 수와 0의 곱은 항상 0이에요. <b>0</b>")
        t, c, box, vb = R.choice(GRP)
        return mcq("%d개의 %s 모두 비어 있어요. %s 모두 몇 %s일까요?" % (b, box, josa(t, "은/는"), c), "0%s" % c, ["%d%s" % (x, c) for x in (b, 1, b + 1)],
                   "한 %s에 0%s씩 %d%s이에요. 0 × %d = <b>0</b>" % (box, c, b, box, b))
    return mk


def table_rule():
    def mk():
        how = R.choice(["step", "same", "cell", "count"])
        if how == "step":
            a = R.randint(2, 9)
            return mcq("곱셈표에서 <b>%d단</b>의 곱은 몇씩 커질까요?" % a, "%d씩" % a, ["%d씩" % x for x in (a + 1, a - 1, 10, 1) if x != a and x > 0],
                       "%d단은 곱하는 수가 1 커질 때마다 곱이 %d씩 커져요." % (a, a))
        if how == "same":
            a, b = R.sample(range(2, 10), 2)
            ok = "%d × %d" % (b, a)
            return mcq("<b>%d × %d</b>와 곱이 같은 곱셈은 무엇일까요?" % (a, b), ok, ["%d × %d" % (a, b + 1), "%d × %d" % (b, b), "%d × %d" % (a + 1, b)],
                       "곱하는 두 수의 순서를 바꾸어도 곱은 같아요. %d × %d = %d × %d = %d. <b>%s</b>" % (a, b, b, a, a * b, ok))
        if how == "cell":
            a, b = R.randint(2, 9), R.randint(2, 9)
            rows = "".join("<tr><th>%d</th>%s</tr>" % (r, "".join("<td>%s</td>" % ("□" if (r, cc) == (a, b) else r * cc) for cc in range(max(2, b - 2), min(9, b + 2) + 1)))
                           for r in range(max(2, a - 1), min(9, a + 1) + 1))
            head = "<tr><th>×</th>%s</tr>" % "".join("<th>%d</th>" % cc for cc in range(max(2, b - 2), min(9, b + 2) + 1))
            tb = "<div class='sn-tw'><table class='sn-table'>%s%s</table></div>" % (head, rows)
            return mcq("곱셈표의 일부예요. □에 알맞은 수는 무엇일까요?%s" % tb, S(a * b), [S(x) for x in (a * (b + 1), a * (b - 1), (a + 1) * b, a + b)],
                       "%d단의 %d → %d × %d = <b>%d</b>" % (a, b, a, b, a * b))
        p = R.choice([12, 16, 18, 24, 36, 8, 6])
        c = sum(1 for x in range(1, 10) for y in range(1, 10) if x * y == p)
        return mcq("곱셈표(1단〜9단)에서 곱이 <b>%d</b>인 칸은 모두 몇 칸일까요?" % p, "%d칸" % c, ["%d칸" % x for x in (c + 1, c - 1, c + 2, 1) if x > 0 and x != c],
                   "곱이 %d인 곱셈: %s. <b>%d칸</b>" % (p, ", ".join("%d × %d" % (x, y) for x in range(1, 10) for y in range(1, 10) if x * y == p), c))
    return mk


def table_story():
    def mk():
        how = R.choice(["grp", "grp", "legs", "week", "rest"])
        if how == "grp":
            return group_story(9)()
        if how == "legs":
            an, legs = R.choice([("강아지", 4), ("닭", 2), ("거미", 8), ("오리", 2), ("고양이", 4), ("문어", 8), ("개미", 6)])
            k = R.randint(2, 9)
            return mcq("%s 한 마리의 다리는 %d개예요. %s %d마리의 다리는 모두 몇 개일까요?" % (an, legs, an, k), "%d개" % (legs * k),
                       ["%d개" % x for x in (legs + k, legs * (k + 1), legs * (k - 1), legs * k + 2)], "%d × %d = <b>%d</b>" % (legs, k, legs * k))
        if how == "week":
            k = R.randint(2, 9)
            return mcq("1주일은 7일이에요. %d주일은 며칠일까요?" % k, "%d일" % (7 * k), ["%d일" % x for x in (7 + k, 7 * (k + 1), 7 * (k - 1), 7 * k + 1)],
                       "7 × %d = <b>%d</b>" % (k, 7 * k))
        a, b = R.randint(3, 9), R.randint(3, 9)
        extra = R.randint(1, a - 1)
        t, c, box, vb = R.choice(GRP)
        q = "%s 한 %s에 %d%s씩 %d%s 있고, 낱개로 %d%s가 더 있어요. %s 모두 몇 %s일까요?" % (josa(t, "이/가"), box, a, c, b, box, extra, c, josa(t, "은/는"), c)
        r = a * b + extra
        return mcq(q, "%d%s" % (r, c), ["%d%s" % (x, c) for x in (a * b, a * (b + 1) + extra, a + b + extra, r + 1)],
                   "%d × %d = %d, %d + %d = <b>%d</b>" % (a, b, a * b, a * b, extra, r))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "meaning":
        return unit(G, "meaning-of-multiplication", 10, "[2수01-10]",
                    "곱셈이 이루어지는 실생활 상황과 연결하여 곱셈의 의미를 이해한다.",
                    "곱셈의 뜻: 묶어 세기와 몇의 몇 배", "곱셈",
                    "초등 2학년 1학기 곱셈 학습지: 묶어 세기, 몇씩 몇 묶음, 몇의 몇 배, 곱셈식 쓰고 읽기, 그림을 보고 곱셈식 만들기, 이야기 문제까지 100문제와 정답.",
                    "3씩 4묶음 = 3의 4배 = 3 × 4", "같은 수를 여러 번 더하는 것을 곱셈으로 나타내요.",
                    ["물건을 2씩, 3씩, 5씩 <b>묶어 세면</b> 빠르게 셀 수 있어요.",
                     "3씩 4묶음은 3의 <b>4배</b>예요. 3 + 3 + 3 + 3 = 12",
                     "3의 4배를 <b>3 × 4</b>라고 쓰고 '3 곱하기 4'라고 읽어요. 3 × 4 = 12는 '3 곱하기 4는 12와 같습니다'예요.",
                     "한 줄에 5개씩 3줄이면 5 × 3이에요."],
                    [("한 접시에 쿠키 4개씩 3접시", ["4씩 3묶음 → 4의 3배", "4 + 4 + 4 = 12"], "4 × 3 = 12"),
                     ("6의 2배", ["6 + 6"], "12")],
                    [("3 × 4를 3 + 4 = 7로 계산한다", "3을 4번 더해요: 12"),
                     ("4씩 3묶음을 3씩 4묶음이라고 한다", "한 묶음에 몇 개인지 먼저 말해요."),
                     ("몇의 몇 배를 덧셈으로만 한다", "곱셈식으로 나타내 보아요.")],
                    [("곱셈구구는 언제 배우나요?", "2학년 2학기 「곱셈구구」 단원에서 2단부터 9단까지 배워요."),
                     ("곱셈을 처음 배울 때 무엇이 중요한가요?", "'몇씩 몇 묶음'을 말로 표현하고, 같은 수를 여러 번 더하는 것과 연결하는 것이 중요해요.")],
                    [("묶어 세기", [(count_groups(), 14), (regroup(), 6)]),
                     ("몇의 몇 배", [(times_of(), 20)]),
                     ("곱셈식 알기", [(mul_expr(), 20)]),
                     ("그림을 보고 곱셈식 만들기", [(pic_expr(), 20)]),
                     ("이야기 문제", [(group_story(), 20)])], 82210)
    if which == "tables":
        return unit(G, "multiplication-tables", 12, "[2수01-11]",
                    "곱셈구구를 이해하고, 한 자리 수의 곱셈을 할 수 있다.",
                    "곱셈구구: 2단부터 9단까지", "곱셈구구",
                    "초등 2학년 2학기 곱셈구구 학습지: 2단·5단, 3단·6단, 4단·8단, 7단·9단, 1단과 0의 곱, 곱셈표의 규칙, 이야기 문제까지 100문제와 정답.",
                    "□단은 □씩 커져요", "곱하는 두 수의 순서를 바꾸어도 곱은 같아요.",
                    ["2단은 2씩, 5단은 5씩 커져요. <b>몇 단의 곱은 그 수만큼씩</b> 커져요.",
                     "6단은 3단의 곱의 2배, 8단은 4단의 곱의 2배예요. 3 × 4 = 12이면 6 × 4 = 24",
                     "1과 어떤 수의 곱은 그 수, <b>0과 어떤 수의 곱은 0</b>이에요.",
                     "곱셈표에서 3 × 7과 7 × 3처럼 두 수의 순서를 바꾸어도 곱은 같아요."],
                    [("7 × 6", ["7 × 5 = 35", "35 + 7 = 42"], "42"),
                     ("0 × 8", ["0을 8번 더해도 0"], "0")],
                    [("8 × 7을 54라고 외운다", "8 × 7 = 56. 8 × 5 = 40에 8을 두 번 더해 확인해요."),
                     ("0 × 5를 5라고 한다", "0과 어떤 수의 곱은 0이에요."),
                     ("1 × 6을 1이라고 한다", "1과 어떤 수의 곱은 그 수, 6이에요.")],
                    [("곱셈구구를 쉽게 외우는 방법은요?", "2단, 5단처럼 쉬운 단부터 소리 내어 외우고, 곱셈표에서 규칙(같은 곱, 몇씩 커지는지)을 찾아보세요."),
                     ("3학년에서는 무엇을 배우나요?", "곱셈구구를 이용해 (두 자리 수) × (한 자리 수)와 나눗셈을 배워요.")],
                    [("2단과 5단", [(fact([2, 5], 1, 9), 14), (skip_table([2, 5]), 6)]),
                     ("3단과 6단", [(fact([3, 6], 1, 9), 14), (skip_table([3, 6]), 6)]),
                     ("4단과 8단", [(fact([4, 8], 1, 9), 14), (skip_table([4, 8]), 6)]),
                     ("7단, 9단, 1단과 0의 곱", [(fact([7, 9], 1, 9), 12), (skip_table([7, 9]), 2), (zero_one(), 6)]),
                     ("곱셈표와 이야기 문제", [(table_rule(), 10), (table_story(), 10)])], 82212)
    raise ValueError(which)
