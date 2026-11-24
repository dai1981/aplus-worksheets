# -*- coding: utf-8 -*-
"""
대한민국 초등 2학년 수학：덧셈과 뺄셈（2022 개정 [2수01-05]〜[2수01-09]）の 4 単元（すべて 2-1）
  add  : 받아올림이 있는 두 자리 수의 덧셈
  sub  : 받아내림이 있는 두 자리 수의 뺄셈
  three: 세 수의 덧셈과 뺄셈
  rel  : 덧셈과 뺄셈의 관계, □가 있는 식
誤答は「받아올림을 하지 않는다（27 + 5 = 22）」「받아올림한 1을 더하지 않는다（38 + 25 = 53）」「일의 자리 합을 그대로 쓴다（38 + 25 = 513）」
「일의 자리에서 큰 수에서 작은 수를 뺀다（52 − 27 = 35）」「받아내림 후 십의 자리를 1 작게 하지 않는다（52 − 27 = 35）」
「□의 값을 구할 때 더하기와 빼기를 바꾼다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa, num
from kr_low import rods

R = random.Random(82204)
NM = Names(R)
G = "grade-2"
TH = [("구슬", "개"), ("색종이", "장"), ("사탕", "개"), ("딱지", "장"), ("스티커", "장"), ("연필", "자루"), ("귤", "개"), ("공책", "권"),
      ("붙임딱지", "장"), ("바둑돌", "개"), ("동화책", "권"), ("풍선", "개")]


def S(x):
    return str(x)


def no_carry_add(a, b):
    """각 자리의 합의 일의 자리만 쓴다"""
    s, p = 0, 1
    while a or b:
        s += (a % 10 + b % 10) % 10 * p
        a //= 10; b //= 10; p *= 10
    return s


def concat_add(a, b):
    """일의 자리 합을 그대로 쓴다：38 + 25 → 5|13 = 513"""
    o = a % 10 + b % 10
    t = a // 10 + b // 10
    return int("%d%d" % (t, o))


def big_minus_small(a, b):
    """각 자리에서 큰 수에서 작은 수를 뺀다：52 − 27 → 35"""
    s, p = 0, 1
    while a or b:
        s += abs(a % 10 - b % 10) * p
        a //= 10; b //= 10; p *= 10
    return s


def borrow_forget(a, b):
    """받아내림은 했지만 십의 자리를 1 작게 하지 않는다：52 − 27 → 35"""
    o = (a % 10 + 10 - b % 10) % 10
    t = a // 10 - b // 10
    return t * 10 + o


# ------------------------------------------------------------------ 덧셈
def add_mk(kind):
    def mk():
        if kind == "21":
            a, b = R.randint(11, 89), R.randint(2, 9)
            if a % 10 + b < 10 or a + b > 99:
                return None
        elif kind == "22":
            a, b = R.randint(11, 79), R.randint(11, 79)
            if a % 10 + b % 10 < 10 or a + b > 99:
                return None
        else:                   # 받아올림 두 번 or 십의 자리에서 받아올림
            a, b = R.randint(21, 98), R.randint(21, 98)
            if a + b < 100 or a + b > 198:
                return None
        c = a + b
        w = [no_carry_add(a, b), c - 10, c + 10, c + 1, concat_add(a, b) if a % 10 + b % 10 >= 10 else None]
        if c >= 100:
            w.append(c - 100)
        e = "일의 자리끼리 더해 10이 넘으면 십의 자리로 <b>1을 받아올림</b>해요."
        if kind == "21":
            e = "%d + %d = %d이므로 십의 자리로 1을 받아올림해요. %d + %d = <b>%d</b>" % (a % 10, b, a % 10 + b, a, b, c)
        elif kind == "22":
            e = "일의 자리: %d + %d = %d → 1을 받아올림. 십의 자리: 1 + %d + %d = %d. <b>%d</b>" % (a % 10, b % 10, a % 10 + b % 10, a // 10, b // 10, c // 10, c)
        else:
            co = 1 if a % 10 + b % 10 >= 10 else 0
            e = "일의 자리 %d + %d = %d%s, 십의 자리 %s%d + %d = %d → 백의 자리로 1을 받아올림. <b>%d</b>" % (
                a % 10, b % 10, a % 10 + b % 10, "(1을 받아올림)" if co else "", "1 + " if co else "", a // 10, b // 10, co + a // 10 + b // 10, c)
        return mcq("%d + %d =" % (a, b), S(c), [S(x) for x in w if x and x > 0 and x != c], e)
    return mk


def add_way():
    """여러 가지 방법：39 + 24 = 40 + 24 − 1"""
    def mk():
        a = R.choice([19, 29, 39, 49, 59, 18, 28, 38, 48, 58])
        b = R.randint(12, 39)
        if a + b > 99:
            return None
        k = 10 - a % 10 if a % 10 >= 8 else None
        r = a + k
        how = R.choice(["box", "val"])
        if how == "box":
            return mcq("%d + %d를 %d + %d − □로 계산했어요. □에 알맞은 수는 무엇일까요?" % (a, b, r, b), S(k), [S(x) for x in (a % 10, 10 - k, k + 1, 10)],
                       "%d은 %d보다 %d 작아요. %d을 더하고 %d을 빼요. <b>%d</b>" % (a, r, k, r, k, k))
        return mcq("%d + %d = %d + %d − %d를 계산하면 얼마일까요?" % (a, b, r, b, k), S(a + b), [S(x) for x in (r + b, a + b + 1, a + b - 10, r + b + k)],
                   "%d + %d = %d, %d − %d = <b>%d</b>" % (r, b, r + b, r + b, k, a + b))
    return mk


def add_pic():
    def mk():
        a, b = R.randint(11, 45), R.randint(3, 9)
        if a % 10 + b < 10:
            return None
        c = a + b
        return mcq("%d에 %d를 더하면 얼마일까요? (수 모형: %d)%s" % (a, b, a, rods(a // 10, a % 10)), S(c), [S(x) for x in (no_carry_add(a, b), c + 1, c - 1, c + 10)],
                   "낱개 %d개와 %d개를 모으면 %d개 → 10개를 묶음 1개로 바꿔요. <b>%d</b>" % (a % 10, b, a % 10 + b, c))
    return mk


def add_story():
    def mk():
        t, c = R.choice(TH)
        n1, n2 = NM.next(), NM.next()
        a, b = R.randint(15, 85), R.randint(15, 85)
        if a % 10 + b % 10 < 10 or a + b > 160:
            return None
        k = R.choice(["join", "add"])
        if k == "join":
            q = "%s %s %d%s, %s %d%s 가지고 있어요. 두 사람이 가진 %s 모두 몇 %s일까요?" % (josa(n1, "은/는"), t, a, c, josa(n2, "은/는"), b, c, josa(t, "은/는"), c)
        else:
            q = "%s %d%s 있었어요. %d%s를 더 샀어요. %s 모두 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c)
        r = a + b
        return mcq(q, "%d%s" % (r, c), ["%d%s" % (x, c) for x in (no_carry_add(a, b), r - 10, r + 10, abs(a - b)) if x >= 10 and x != r],
                   "%d + %d = <b>%d</b>" % (a, b, r))
    return mk


# ------------------------------------------------------------------ 뺄셈
def sub_mk(kind):
    def mk():
        if kind == "21":
            a, b = R.randint(11, 98), R.randint(2, 9)
            if a % 10 >= b:
                return None
        elif kind == "t2":       # 몇십 − 몇십몇
            a, b = R.randint(2, 9) * 10, R.randint(11, 89)
            if b >= a or b % 10 == 0:
                return None
        else:
            a, b = R.randint(31, 99), R.randint(12, 89)
            if a % 10 >= b % 10 or b >= a:
                return None
        c = a - b
        w = [big_minus_small(a, b), borrow_forget(a, b), c + 1, c - 1 if c > 1 else c + 2, c + 10]
        if kind == "21":
            e = "일의 자리 %d에서 %d를 뺄 수 없어요. 십의 자리에서 10을 받아내림해 %d − %d = %d. 십의 자리는 %d − 1 = %d. <b>%d</b>" % (
                a % 10, b, 10 + a % 10, b, 10 + a % 10 - b, a // 10, a // 10 - 1, c)
        else:
            e = "일의 자리 %d에서 %d를 뺄 수 없어서 10을 받아내림해요. %d − %d = %d, 십의 자리 %d − 1 − %d = %d. <b>%d</b>" % (
                a % 10, b % 10, 10 + a % 10, b % 10, 10 + a % 10 - b % 10, a // 10, b // 10, c // 10, c)
        return mcq("%d − %d =" % (a, b), S(c), [S(x) for x in w if x >= 0 and x != c], e)
    return mk


def sub_way():
    def mk():
        a = R.randint(41, 99)
        b = R.choice([19, 29, 39, 18, 28, 9, 8])
        if b >= a or a % 10 >= b % 10:
            return None
        k = 10 - b % 10
        r = b + k
        how = R.choice(["box", "val"])
        if how == "box":
            return mcq("%d − %d를 %d − %d + □로 계산했어요. □에 알맞은 수는 무엇일까요?" % (a, b, a, r), S(k), [S(x) for x in (b % 10, k + 1, 10, r)],
                       "%d을 빼면 %d을 더 뺀 것이에요. 다시 %d을 더해요. <b>%d</b>" % (r, k, k, k))
        return mcq("%d − %d = %d − %d + %d를 계산하면 얼마일까요?" % (a, b, a, r, k), S(a - b), [S(x) for x in (a - r, a - b + 1, a - b - 10, a - r - k)],
                   "%d − %d = %d, %d + %d = <b>%d</b>" % (a, r, a - r, a - r, k, a - b))
    return mk


def sub_story():
    def mk():
        t, c = R.choice(TH)
        n1, n2 = NM.next(), NM.next()
        a, b = R.randint(30, 99), R.randint(12, 59)
        if b >= a or a % 10 >= b % 10:
            return None
        k = R.choice(["take", "comp", "take"])
        if k == "take":
            q = "%s %d%s 있었어요. 그중에서 %d%s를 친구에게 주었어요. 남은 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c)
        else:
            q = "%s %s %d%s, %s %d%s 가지고 있어요. %s %s보다 몇 %s 더 많이 가지고 있을까요?" % (josa(n1, "은/는"), t, a, c, josa(n2, "은/는"), b, c, josa(n1, "은/는"), n2, c)
        r = a - b
        return mcq(q, "%d%s" % (r, c), ["%d%s" % (x, c) for x in (big_minus_small(a, b), borrow_forget(a, b), a + b, r + 1) if x > 0 and x != r],
                   "%d − %d = <b>%d</b>" % (a, b, r))
    return mk


# ------------------------------------------------------------------ 세 수
def three_mk(kind):
    def mk():
        if kind == "add":
            a, b, c = R.randint(11, 49), R.randint(5, 39), R.randint(3, 29)
            if a + b + c > 99:
                return None
            r = a + b + c
            t = "%d + %d + %d" % (a, b, c)
            st = "%d + %d = %d, %d + %d = <b>%d</b>" % (a, b, a + b, a + b, c, r)
            w = [a + b, b + c, r + 10, r - 10, no_carry_add(a + b, c)]
        elif kind == "sub":
            a = R.randint(50, 99)
            b, c = R.randint(5, 30), R.randint(5, 25)
            if a - b - c < 1:
                return None
            r = a - b - c
            t = "%d − %d − %d" % (a, b, c)
            st = "%d − %d = %d, %d − %d = <b>%d</b>" % (a, b, a - b, a - b, c, r)
            w = [a - b, a - (b - c) if b > c else a - c + b, r + 10, r - 10, r + 1]
        else:
            if R.random() < 0.5:
                a, b, c = R.randint(15, 60), R.randint(5, 35), R.randint(5, 30)
                if a + b > 99 or a + b - c < 1:
                    return None
                r = a + b - c
                t = "%d + %d − %d" % (a, b, c)
                st = "%d + %d = %d, %d − %d = <b>%d</b>" % (a, b, a + b, a + b, c, r)
                w = [a + b + c, a - (b - c) if b > c else r + 2, r + 10, r - 10, r + 1]
            else:
                a, b, c = R.randint(40, 90), R.randint(5, 35), R.randint(5, 30)
                if a - b < 1 or a - b + c > 99:
                    return None
                r = a - b + c
                t = "%d − %d + %d" % (a, b, c)
                st = "%d − %d = %d, %d + %d = <b>%d</b>" % (a, b, a - b, a - b, c, r)
                w = [a - (b + c), a + b - c, r + 10, r - 10, r + 1]
        return mcq(t + " =", S(r), [S(x) for x in w if x >= 0 and x != r], "앞에서부터 차례로 계산해요. " + st)
    return mk


def three_story():
    def mk():
        t, c = R.choice(TH)
        k = R.choice(["aaa", "ass", "asa"])
        if k == "aaa":
            a, b, d = R.randint(12, 40), R.randint(10, 30), R.randint(5, 25)
            if a + b + d > 99:
                return None
            q = "%s 월요일에 %d%s, 화요일에 %d%s, 수요일에 %d%s 모았어요. 모은 %s 모두 몇 %s일까요?" % (
                josa(NM.next(), "은/는"), a, c, b, c, d, c, josa(t, "은/는"), c)
            q = q.replace("월요일에", "%s 월요일에" % josa(t, "을/를"), 1)
            r = a + b + d
            w = [a + b, b + d, r + 10, r - 10]
            st = "%d + %d + %d = <b>%d</b>" % (a, b, d, r)
        elif k == "ass":
            a, b, d = R.randint(50, 95), R.randint(8, 30), R.randint(5, 25)
            if a - b - d < 1:
                return None
            q = "%s %d%s 있었어요. 형에게 %d%s, 동생에게 %d%s를 주었어요. 남은 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, d, c, josa(t, "은/는"), c)
            r = a - b - d
            w = [a - b, a - d, r + 10, r + 1]
            st = "%d − %d − %d = <b>%d</b>" % (a, b, d, r)
        else:
            a, b, d = R.randint(20, 60), R.randint(10, 30), R.randint(5, 25)
            if a + b > 99 or a + b - d < 1:
                return None
            q = "버스에 %d명이 타고 있었어요. 정류장에서 %d명이 더 타고 %d명이 내렸어요. 지금 버스에 탄 사람은 몇 명일까요?" % (a, b, d)
            r = a + b - d
            w = [a + b + d, a - b + d if a > b else r + 2, r + 10, r - 1]
            c = "명"
            st = "%d + %d − %d = <b>%d</b>" % (a, b, d, r)
        return mcq(q, "%d%s" % (r, c), ["%d%s" % (x, c) for x in w if x > 0 and x != r], st)
    return mk


# ------------------------------------------------------------------ 관계와 □
def rel_eq():
    def mk():
        a, b = R.randint(12, 59), R.randint(8, 39)
        c = a + b
        if c > 99:
            return None
        if R.random() < 0.5:
            ok = "%d − %d = %d" % (c, b, a)
            bad = ["%d − %d = %d" % (a, b, c), "%d − %d = %d" % (c, a, a), "%d + %d = %d" % (c, b, a + c), "%d − %d = %d" % (b, a, c)]
            q = "덧셈식 <b>%d + %d = %d</b>를 뺄셈식으로 바르게 나타낸 것은 무엇일까요?" % (a, b, c)
            e = "덧셈식의 합 %d에서 한 수를 빼면 다른 수가 돼요. <b>%s</b>" % (c, ok)
        else:
            ok = "%d + %d = %d" % (a, b, c)
            bad = ["%d + %d = %d" % (c, b, a), "%d + %d = %d" % (a, c, b), "%d − %d = %d" % (a, b, c), "%d + %d = %d" % (b, c, a)]
            q = "뺄셈식 <b>%d − %d = %d</b>를 덧셈식으로 바르게 나타낸 것은 무엇일까요?" % (c, b, a)
            e = "뺄셈식의 답 %d에 뺀 수 %d를 더하면 처음 수 %d이 돼요. <b>%s</b>" % (a, b, c, ok)
        return mcq(q, ok, bad, e)
    return mk


def rel_fam():
    """세 수로 덧셈식・뺄셈식 만들기"""
    def mk():
        a, b = R.randint(5, 49), R.randint(5, 49)
        if a == b or a + b > 99:
            return None
        c = a + b
        cands = ["%d + %d = %d" % (a, b, c), "%d + %d = %d" % (b, a, c), "%d − %d = %d" % (c, a, b), "%d − %d = %d" % (c, b, a)]
        good = R.choice(cands)
        bad = ["%d − %d = %d" % (a, c, b), "%d + %d = %d" % (c, a, b), "%d − %d = %d" % (b, a, c), "%d − %d = %d" % (a, b, c)]
        return mcq("세 수 <b>%d, %d, %d</b>로 만들 수 있는 식은 무엇일까요?" % (a, b, c), good, [x for x in bad if x != good],
                   "가장 큰 수 %d이 합이에요. %d + %d = %d, %d − %d = %d처럼 만들어요. <b>%s</b>" % (c, a, b, c, c, a, b, good))
    return mk


def box_add():
    def mk():
        a, b = R.randint(5, 59), R.randint(5, 39)
        c = a + b
        if c > 99:
            return None
        if R.random() < 0.5:
            q = "□ + %d = %d" % (b, c)
            e = "□ = %d − %d = <b>%d</b>" % (c, b, a)
        else:
            q = "%d + □ = %d" % (b, c)
            e = "□ = %d − %d = <b>%d</b>" % (c, b, a)
        return mcq("%s<br>□에 알맞은 수는 무엇일까요?" % q, S(a), [S(x) for x in (c + b, a + 1, a - 1, a + 10, big_minus_small(c, b)) if x > 0 and x != a], e)
    return mk


def box_sub():
    def mk():
        a, b = R.randint(15, 99), R.randint(5, 49)
        if b >= a:
            return None
        c = a - b
        if R.random() < 0.5:        # □ − b = c
            q = "□ − %d = %d" % (b, c)
            ans = a
            e = "□ = %d + %d = <b>%d</b>" % (c, b, a)
            w = [c - b if c > b else b - c, a + 10, a - 10, a + 1]
        else:                       # a − □ = c
            q = "%d − □ = %d" % (a, c)
            ans = b
            e = "□ = %d − %d = <b>%d</b>" % (a, c, b)
            w = [a + c, b + 1, b - 1, b + 10]
        return mcq("%s<br>□에 알맞은 수는 무엇일까요?" % q, S(ans), [S(x) for x in w if x > 0 and x != ans], e)
    return mk


def box_story():
    def mk():
        t, c = R.choice(TH)
        k = R.choice(["add", "sub", "unknown"])
        if k == "add":
            a, b = R.randint(12, 50), R.randint(8, 40)
            r = a + b
            if r > 99:
                return None
            q = "%s %d%s 있었어요. 몇 %s를 더 받았더니 %d%s가 되었어요. 더 받은 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, c, r, c, josa(t, "은/는"), c)
            ans, w, st = b, [a + r, b + 1, b - 1, b + 10], "%d + □ = %d, □ = %d − %d = <b>%d</b>" % (a, r, r, a, b)
        elif k == "sub":
            a, b = R.randint(30, 95), R.randint(8, 29)
            if b >= a:
                return None
            r = a - b
            q = "%s %d%s 있었어요. 친구에게 몇 %s를 주었더니 %d%s 남았어요. 친구에게 준 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, c, r, c, josa(t, "은/는"), c)
            ans, w, st = b, [a + r, b + 1, b - 1, b + 10], "%d − □ = %d, □ = %d − %d = <b>%d</b>" % (a, r, a, r, b)
        else:
            a, b = R.randint(30, 80), R.randint(8, 29)
            if b >= a:
                return None
            q = "어떤 수에서 %d를 뺐더니 %d이 되었어요. 어떤 수는 얼마일까요?" % (b, a - b)
            ans, w, st = a, [a - 2 * b, a + 1, a - 10, b], "□ − %d = %d, □ = %d + %d = <b>%d</b>" % (b, a - b, a - b, b, a)
            c = ""
        return mcq(q, "%d%s" % (ans, c), ["%d%s" % (x, c) for x in w if x > 0 and x != ans], st)
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "add":
        return unit(G, "adding-two-digit-numbers", 4, "[2수01-05] [2수01-06]",
                    "덧셈과 뺄셈이 이루어지는 실생활 상황과 연결하여 덧셈과 뺄셈의 의미를 이해한다. 두 자리 수의 범위에서 덧셈과 뺄셈의 계산 원리를 이해하고 그 계산을 할 수 있다.",
                    "받아올림이 있는 두 자리 수의 덧셈", "덧셈",
                    "초등 2학년 1학기 덧셈 학습지: (두 자리 수)+(한 자리 수), (두 자리 수)+(두 자리 수) 받아올림, 백의 자리로 받아올림, 여러 가지 방법, 이야기 문제까지 100문제와 정답.",
                    "일의 자리 합이 10을 넘으면 1을 올려요", "받아올림한 1을 십의 자리 위에 작게 써요.",
                    ["일의 자리끼리 더해 10이거나 10보다 크면 십의 자리로 <b>1을 받아올림</b>해요.",
                     "십의 자리는 받아올림한 1과 두 수의 십의 자리 숫자를 함께 더해요.",
                     "십의 자리끼리 더해 10이 넘으면 백의 자리로 1을 받아올림해요. 76 + 58 = 134",
                     "39 + 24는 40 + 24 − 1처럼 몇십을 만들어 더하면 편해요."],
                    [("38 + 25", ["일의 자리: 8 + 5 = 13 → 3을 쓰고 1을 받아올림", "십의 자리: 1 + 3 + 2 = 6"], "63"),
                     ("76 + 58", ["일의 자리: 6 + 8 = 14 → 1을 받아올림", "십의 자리: 1 + 7 + 5 = 13 → 백의 자리 1"], "134")],
                    [("27 + 5를 22라고 한다", "7 + 5 = 12의 1을 받아올려요: 32"),
                     ("38 + 25를 53이라고 한다", "받아올림한 1을 십의 자리에 더해요: 63"),
                     ("38 + 25를 513이라고 쓴다", "13 중 3만 쓰고 1은 십의 자리로 올려요.")],
                    [("받아올림을 자꾸 잊어요.", "세로셈으로 쓰고, 받아올림한 1을 십의 자리 위에 작게 써 보세요."),
                     ("세 자리 수의 덧셈은 언제 배우나요?", "3학년 1학기 「덧셈과 뺄셈」에서 배워요.")],
                    [("(두 자리 수) + (한 자리 수)", [(add_mk("21"), 14), (add_pic(), 6)]),
                     ("(두 자리 수) + (두 자리 수)", [(add_mk("22"), 20)]),
                     ("백의 자리로 받아올림", [(add_mk("big"), 20)]),
                     ("여러 가지 방법", [(add_way(), 12), (add_mk("22"), 8)]),
                     ("이야기 문제", [(add_story(), 20)])], 82204)
    if which == "sub":
        return unit(G, "subtracting-two-digit-numbers", 5, "[2수01-05] [2수01-06]",
                    "덧셈과 뺄셈이 이루어지는 실생활 상황과 연결하여 덧셈과 뺄셈의 의미를 이해한다. 두 자리 수의 범위에서 덧셈과 뺄셈의 계산 원리를 이해하고 그 계산을 할 수 있다.",
                    "받아내림이 있는 두 자리 수의 뺄셈", "뺄셈",
                    "초등 2학년 1학기 뺄셈 학습지: (두 자리 수)−(한 자리 수), (몇십)−(몇십몇), (두 자리 수)−(두 자리 수) 받아내림, 여러 가지 방법, 이야기 문제까지 100문제와 정답.",
                    "일의 자리를 뺄 수 없으면 10을 내려요", "받아내림한 십의 자리는 1 작아져요.",
                    ["일의 자리끼리 뺄 수 없으면 십의 자리에서 <b>10을 받아내림</b>해요.",
                     "받아내림하면 십의 자리 숫자는 1 작아지고, 일의 자리 수는 10 커져요.",
                     "52 − 27: 12 − 7 = 5, 십의 자리 4 − 2 = 2 → 25",
                     "52 − 29는 52 − 30 + 1처럼 몇십을 만들어 빼면 편해요."],
                    [("43 − 8", ["일의 자리: 3에서 8을 뺄 수 없어요.", "13 − 8 = 5, 십의 자리 4 − 1 = 3"], "35"),
                     ("60 − 24", ["10 − 4 = 6", "십의 자리 6 − 1 − 2 = 3"], "36")],
                    [("52 − 27을 35라고 한다(7 − 2를 계산)", "2에서 7을 뺄 수 없으니 받아내림해요: 25"),
                     ("받아내림 후 십의 자리를 그대로 둔다", "받아내림한 십의 자리는 1 작아져요."),
                     ("60 − 24를 44라고 한다", "0에서 4를 뺄 수 없어요. 10 − 4 = 6, 5 − 2 = 3 → 36")],
                    [("받아내림을 어려워해요.", "수 모형의 10개짜리 막대 하나를 낱개 10개로 바꿔 보는 활동을 먼저 해 보세요."),
                     ("계산이 맞는지 어떻게 확인하나요?", "뺄셈의 답에 뺀 수를 더해 처음 수가 나오는지 확인해요.")],
                    [("(두 자리 수) − (한 자리 수)", [(sub_mk("21"), 20)]),
                     ("(몇십) − (몇십몇)", [(sub_mk("t2"), 20)]),
                     ("(두 자리 수) − (두 자리 수)", [(sub_mk("22"), 20)]),
                     ("여러 가지 방법", [(sub_way(), 12), (sub_mk("22"), 8)]),
                     ("이야기 문제", [(sub_story(), 20)])], 82205)
    if which == "three":
        return unit(G, "adding-and-subtracting-three-numbers", 6, "[2수01-08]",
                    "두 자리 수의 범위에서 세 수의 덧셈과 뺄셈을 할 수 있다.",
                    "세 수의 덧셈과 뺄셈", "세 수의 계산",
                    "초등 2학년 1학기 세 수의 계산 학습지: 두 자리 수 세 수의 덧셈, 세 수의 뺄셈, 덧셈과 뺄셈이 섞인 계산, 이야기 문제까지 100문제와 정답.",
                    "앞에서부터 차례로 계산해요", "45 − 18 + 7 → 27 + 7 = 34",
                    ["세 수의 계산은 <b>앞에서부터 두 수씩 차례로</b> 계산해요.",
                     "덧셈과 뺄셈이 섞여 있어도 앞에서부터 차례로 계산해요.",
                     "뺄셈이 있으면 순서를 바꾸면 안 돼요. 50 − 20 − 10은 20이지만, 뒤의 20 − 10을 먼저 하면 40이 되어 틀려요."],
                    [("26 + 18 + 15", ["26 + 18 = 44", "44 + 15 = 59"], "59"),
                     ("72 − 25 + 9", ["72 − 25 = 47", "47 + 9 = 56"], "56")],
                    [("72 − 25 + 9에서 25 + 9를 먼저 계산한다", "앞에서부터 차례로: 47 + 9 = 56"),
                     ("세 수 중 두 수만 계산하고 끝낸다", "세 수를 모두 계산했는지 확인해요."),
                     ("받아올림, 받아내림을 빠뜨린다", "두 수씩 계산할 때마다 받아올림·받아내림을 확인해요.")],
                    [("세 수의 계산은 왜 앞에서부터 하나요?", "덧셈과 뺄셈이 섞이면 순서에 따라 답이 달라질 수 있어서 약속을 정해 두었어요."),
                     ("3학년에서는 무엇을 배우나요?", "세 자리 수의 덧셈과 뺄셈을 배워요.")],
                    [("세 수의 덧셈", [(three_mk("add"), 20)]),
                     ("세 수의 뺄셈", [(three_mk("sub"), 20)]),
                     ("덧셈과 뺄셈이 섞인 계산", [(three_mk("mix"), 20)]),
                     ("이야기 문제", [(three_story(), 20)]),
                     ("섞어서 연습", [(three_story(), 10), (three_mk("mix"), 10)])], 82206)
    if which == "rel":
        return unit(G, "addition-subtraction-relationship-and-missing-numbers", 7, "[2수01-07] [2수01-09]",
                    "덧셈과 뺄셈의 관계를 이해한다. □가 사용된 덧셈식과 뺄셈식을 만들고, □의 값을 구할 수 있다.",
                    "덧셈과 뺄셈의 관계, □의 값 구하기", "□가 있는 식",
                    "초등 2학년 1학기 덧셈과 뺄셈의 관계 학습지: 덧셈식을 뺄셈식으로, 뺄셈식을 덧셈식으로, 세 수로 식 만들기, □의 값 구하기, 모르는 수를 □로 나타낸 이야기 문제까지 100문제와 정답.",
                    "□ + 8 = 23 → □ = 23 − 8", "덧셈식은 뺄셈식으로, 뺄셈식은 덧셈식으로 바꿀 수 있어요.",
                    ["15 + 8 = 23은 뺄셈식 23 − 8 = 15, 23 − 15 = 8로 나타낼 수 있어요.",
                     "23 − 8 = 15는 덧셈식 15 + 8 = 23, 8 + 15 = 23으로 나타낼 수 있어요.",
                     "모르는 수는 <b>□</b>로 나타내요. □ + 8 = 23이면 □ = 23 − 8 = 15예요.",
                     "□ − 8 = 15이면 □ = 15 + 8 = 23이에요. 식을 바꾼 뒤 □에 넣어 확인해요."],
                    [("□ + 17 = 42", ["뺄셈식으로 바꿔요: □ = 42 − 17"], "25"),
                     ("50 − □ = 32", ["□ = 50 − 32"], "18")],
                    [("□ + 17 = 42에서 42 + 17을 계산한다", "덧셈식의 □는 빼서 구해요: 25"),
                     ("□ − 8 = 15에서 15 − 8을 계산한다", "뺄셈식의 처음 수는 더해서 구해요: 23"),
                     ("23 − 8 = 15를 8 − 15 = 23으로 바꾼다", "덧셈식으로 바꿀 때는 15 + 8 = 23이에요.")],
                    [("□가 있는 식은 왜 배우나요?", "모르는 수를 □로 나타내어 식을 세우면 문제를 쉽게 풀 수 있어요. 나중에 배우는 방정식의 기초예요."),
                     ("답을 확인하는 방법은요?", "구한 수를 □에 넣어 식이 맞는지 계산해 보세요.")],
                    [("덧셈식과 뺄셈식", [(rel_eq(), 20)]),
                     ("세 수로 식 만들기", [(rel_fam(), 20)]),
                     ("□가 있는 덧셈식", [(box_add(), 20)]),
                     ("□가 있는 뺄셈식", [(box_sub(), 20)]),
                     ("□를 사용한 이야기 문제", [(box_story(), 20)])], 82207)
    raise ValueError(which)
