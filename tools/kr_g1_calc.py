# -*- coding: utf-8 -*-
"""
대한민국 초등 1학년 수학：덧셈과 뺄셈（2022 개정 [2수01-04]〜[2수01-08]）の 4 単元
  in9   : 덧셈과 뺄셈（모으기와 가르기、9까지）        1-1
  two   : 덧셈과 뺄셈(1)（받아올림・받아내림 없는 두 자리 수） 1-2
  three : 덧셈과 뺄셈(2)（세 수、10 만들기）            1-2
  in20  : 덧셈과 뺄셈(3)（받아올림・받아내림 있는 20까지） 1-2
誤答は「처음 수를 한 번 더 센다（±1）」「더하기와 빼기를 바꾼다」「몇을 십의 자리에 더한다（34 + 5 = 84）」
「일의 자리에서 큰 수에서 작은 수를 뺀다（13 − 5 = 12）」「10을 만들 때 가른 수를 잘못 찾는다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa
from kr_low import KINDS, nm, cw, cnt, row, tenframe, rods, bond, two, crossed, dice, near, ko, scatter
import k_pics as K

R = random.Random(82103)
NM = Names(R)
G = "grade-1"
TH = [("사탕", "개"), ("구슬", "개"), ("연필", "자루"), ("색종이", "장"), ("풍선", "개"), ("딸기", "개"), ("공책", "권"),
      ("쿠키", "개"), ("참새", "마리"), ("토끼", "마리"), ("귤", "개"), ("딱지", "장")]


def th():
    return R.choice(TH)


def S(x):
    return "%d" % x


def eq(a, op, b, c):
    return "%d %s %d = %d" % (a, op, b, c)


# ------------------------------------------------------------------ 9까지
def bond9(hi=9):
    def mk():
        w = R.randint(2, hi)
        a = R.randint(1, w - 1)
        b = w - a
        how = R.choice(["part", "part", "whole"])
        if how == "whole":
            return mcq("두 수를 모으기 했어요. ?에 알맞은 수는 무엇일까요?%s" % bond("?", a, b), S(w), [S(x) for x in near(w, 1, 10) + [abs(a - b)]],
                       "%d와 %d를 모으면 <b>%d</b>이에요." % (a, b, w))
        return mcq("<b>%d</b>를 두 수로 가르기 했어요. ?에 알맞은 수는 무엇일까요?%s" % (w, bond(w, a, "?")), S(b), [S(x) for x in near(b, 0, 9) + [w]],
                   "%d은 %d와 <b>%d</b>로 가를 수 있어요." % (w, a, b))
    return mk


def dice_sum():
    def mk():
        a, b = R.randint(1, 6), R.randint(1, 6)
        if a + b > 9:
            return None
        return mcq("두 주사위의 눈을 모으면 몇일까요?%s" % dice([a, b]), S(a + b), [S(x) for x in near(a + b, 1, 12)],
                   "%d와 %d를 모으면 <b>%d</b>이에요." % (a, b, a + b))
    return mk


def split_ways():
    def mk():
        w = R.randint(4, 9)
        a = R.randint(1, w - 1)
        ok = "%d와 %d" % (a, w - a)
        bad = ["%d와 %d" % (a, w - a + d) for d in (1, -1, 2) if 0 < w - a + d]
        return mcq("<b>%d</b>를 바르게 가른 것은 무엇일까요?" % w, ok, bad, "%d와 %d를 모으면 %d이 돼요. <b>%s</b>" % (a, w - a, w, ok))
    return mk


def add_pic():
    def mk():
        k = R.choice(KINDS)
        a, b = R.randint(1, 5), R.randint(1, 4)
        if a + b > 9:
            return None
        how = R.choice(["all", "eq"])
        pic = two(a, k, b, None, "+")
        if how == "all":
            return mcq("%s 모두 몇 %s일까요?%s" % (josa(nm(k), "은/는"), cw(k), pic), "%d%s" % (a + b, cw(k)),
                       ["%d%s" % (x, cw(k)) for x in near(a + b, 1) + [abs(a - b)]],
                       "%d와 %d를 모으면 %d이에요. %d + %d = <b>%d</b>" % (a, b, a + b, a, b, a + b))
        return mcq("그림을 덧셈식으로 바르게 나타낸 것은 무엇일까요?%s" % pic, eq(a, "+", b, a + b),
                   [eq(a, "+", b, a + b + 1), eq(a, "−", b, a - b) if a > b else eq(b, "−", a, b - a), eq(a, "+", b + 1, a + b + 1), eq(a, "+", b, a + b - 1)],
                   "%d%s와 %d%s를 더해요. <b>%s</b>" % (a, cw(k), b, cw(k), eq(a, "+", b, a + b)))
    return mk


def sub_pic():
    def mk():
        k = R.choice(KINDS)
        a = R.randint(3, 9)
        b = R.randint(1, a - 1)
        how = R.choice(["left", "eq", "more"])
        if how == "left":
            return mcq("지운 것을 빼면 남은 %s는 몇 %s일까요?%s" % (nm(k), cw(k), crossed(a, k, b)), "%d%s" % (a - b, cw(k)),
                       ["%d%s" % (x, cw(k)) for x in near(a - b, 0) + [b, a + b]],
                       "%d%s 중 %d%s를 지웠어요. %d − %d = <b>%d</b>" % (a, cw(k), b, cw(k), a, b, a - b))
        if how == "eq":
            return mcq("그림을 뺄셈식으로 바르게 나타낸 것은 무엇일까요?%s" % crossed(a, k, b), eq(a, "−", b, a - b),
                       [eq(a, "+", b, a + b), eq(a, "−", b, a - b + 1), eq(a, "−", a - b, b) if a - b != b else eq(a, "−", b, a - b - 1), eq(b, "−", a - b, abs(2 * b - a)) if 2 * b > a else None],
                       "%d%s에서 %d%s를 빼요. <b>%s</b>" % (a, cw(k), b, cw(k), eq(a, "−", b, a - b)))
        ka, kb = R.sample(KINDS, 2)
        x, y = R.sample(range(2, 10), 2)
        big, small = (ka, kb) if x > y else (kb, ka)
        d = abs(x - y)
        pic = ko(K.match_svg([(x, ka, "", None), (y, kb, "", None)]), "%s와 %s" % (cnt(ka, x), cnt(kb, y)))
        return mcq("%s %s보다 몇 개 더 많을까요?%s" % (josa(nm(big), "은/는"), nm(small), pic), "%d개" % d,
                   ["%d개" % v for v in near(d, 0) + [x + y]],
                   "하나씩 짝을 지으면 %d개가 남아요. %d − %d = <b>%d</b>" % (d, max(x, y), min(x, y), d))
    return mk


def calc9(op):
    def mk():
        if op == "+":
            a, b = R.randint(0, 9), R.randint(0, 9)
            if a + b > 9 or a + b == 0:
                return None
            c = a + b
            w = near(c, 0, 10) + [abs(a - b)]
            e = "%d에서 %d만큼 이어 세면 %d이에요. <b>%d</b>" % (a, b, c, c) if b else "어떤 수에 0을 더하면 그 수 그대로예요. <b>%d</b>" % c
        else:
            a = R.randint(1, 9)
            b = R.randint(0, a)
            c = a - b
            w = near(c, 0, 10) + [a + b]
            e = ("%d에서 %d만큼 거꾸로 세면 %d이에요. <b>%d</b>" % (a, b, c, c) if b and b != a else
                 "어떤 수에서 0을 빼면 그 수 그대로예요. <b>%d</b>" % c if b == 0 else "같은 수끼리 빼면 0이에요. <b>0</b>")
        return mcq("%d %s %d =" % (a, op, b), S(c), [S(x) for x in w if x <= 18], e)
    return mk


def biggest_expr():
    def mk():
        ex = []
        vals = set()
        while len(ex) < 4:
            if R.random() < 0.5:
                a, b = R.randint(1, 8), R.randint(1, 8)
                if a + b > 9:
                    continue
                v, t = a + b, "%d + %d" % (a, b)
            else:
                a = R.randint(2, 9)
                b = R.randint(1, a - 1)
                v, t = a - b, "%d − %d" % (a, b)
            if v in vals:
                continue
            vals.add(v)
            ex.append((v, t))
        big = R.random() < 0.6
        v, t = max(ex) if big else min(ex)
        return mcq("계산 결과가 가장 %s 식은 무엇일까요?" % ("큰" if big else "작은") + "<br>" + ", ".join(x[1] for x in ex), t, [x[1] for x in ex if x[1] != t],
                   "계산하면 %s이에요. 가장 %s 것은 <b>%s</b>예요." % (", ".join("%s = %d" % (x[1], x[0]) for x in ex), "큰" if big else "작은", t))
    return mk


def story9(kinds=("join", "add", "take", "comp")):
    def mk():
        t, c = th()
        k = R.choice(kinds)
        n1, n2 = NM.next(), NM.next()
        if k in ("join", "add"):
            a, b = R.randint(1, 6), R.randint(1, 5)
            if a + b > 9:
                return None
            if k == "join":
                q = "%s %s %d%s, %s %d%s 가지고 있어요. 두 사람이 가진 %s 모두 몇 %s일까요?" % (josa(n1, "은/는"), t, a, c, josa(n2, "은/는"), b, c, josa(t, "은/는"), c)
            else:
                q = "%s %d%s 있었어요. %d%s를 더 받았어요. %s 모두 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c)
            return mcq(q, "%d%s" % (a + b, c), ["%d%s" % (x, c) for x in near(a + b, 1) + [abs(a - b)]], "%d + %d = <b>%d</b>" % (a, b, a + b))
        a = R.randint(3, 9)
        b = R.randint(1, a - 1)
        if k == "take":
            q = "%s %d%s 있었어요. 그중에서 %d%s를 동생에게 주었어요. 남은 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c)
        else:
            q = "%s %s %d%s, %s %d%s 가지고 있어요. %s %s보다 몇 %s 더 많이 가지고 있을까요?" % (josa(n1, "은/는"), t, a, c, josa(n2, "은/는"), b, c, josa(n1, "은/는"), n2, c)
        return mcq(q, "%d%s" % (a - b, c), ["%d%s" % (x, c) for x in near(a - b, 0) + [a + b]], "%d − %d = <b>%d</b>" % (a, b, a - b))
    return mk


# ------------------------------------------------------------------ 두 자리 수（받아올림 없음）
def ones_ok(a, b, add):
    return (a % 10 + b % 10 <= 9) if add else (a % 10 >= b % 10)


def add2(kind):
    def mk():
        if kind == "tt1":           # 몇십몇 + 몇
            a, b = R.randint(11, 89), R.randint(1, 8)
        elif kind == "t1":          # 몇십 + 몇
            a, b = R.randint(1, 9) * 10, R.randint(1, 9)
        elif kind == "tt":          # 몇십 + 몇십
            a, b = R.randint(1, 8) * 10, R.randint(1, 8) * 10
        else:                       # 몇십몇 + 몇십몇
            a, b = R.randint(11, 78), R.randint(11, 78)
        if a + b > 99 or not ones_ok(a, b, True) or (kind == "tt" and a + b > 90):
            return None
        c = a + b
        w = [c + 10, c - 10, c + 1, c - 1]
        if b < 10:
            w.insert(0, a + 10 * b)
        elif kind == "tt2":
            w.insert(0, (a // 10 + b // 10) * 10 + abs(a % 10 - b % 10))
        pic = rods(a // 10, a % 10) if kind in ("tt1", "t1") and R.random() < 0.4 and a <= 59 else ""
        e = ("일의 자리끼리, 십의 자리끼리 더해요. <b>%d</b>" % c) if b >= 10 else "%d의 일의 자리 %d에 %d를 더해요. <b>%d</b>" % (a, a % 10, b, c)
        if kind == "tt":
            e = "10개씩 묶음 %d개와 %d개를 더하면 %d개예요. <b>%d</b>" % (a // 10, b // 10, c // 10, c)
        q = ("%d %s %d =" % (a, "+", b)) if not pic else "%d에 %d를 더하면 몇일까요?%s" % (a, b, pic)
        return mcq(q, S(c), [S(x) for x in w if 0 < x < 100 and x != c], e)
    return mk


def sub2(kind):
    def mk():
        if kind == "tt1":
            a, b = R.randint(11, 99), R.randint(1, 8)
        elif kind == "tt":
            a, b = R.randint(2, 9) * 10, R.randint(1, 8) * 10
        else:
            a, b = R.randint(21, 99), R.randint(11, 88)
        if b >= a or not ones_ok(a, b, False):
            return None
        c = a - b
        w = [c + 10, c - 10, c + 1, c - 1]
        if b < 10:
            w.insert(0, a - 10 * b)
        elif kind == "tt2":
            w.insert(0, a + b)
        e = ("일의 자리끼리, 십의 자리끼리 빼요. <b>%d</b>" % c) if b >= 10 else "%d의 일의 자리 %d에서 %d를 빼요. <b>%d</b>" % (a, a % 10, b, c)
        if kind == "tt":
            e = "10개씩 묶음 %d개에서 %d개를 빼면 %d개예요. <b>%d</b>" % (a // 10, b // 10, c // 10, c)
        return mcq("%d − %d =" % (a, b), S(c), [S(x) for x in w if 0 <= x < 100 and x != c], e)
    return mk


def story2():
    def mk():
        t, c = th()
        k = R.choice(["join", "add", "take", "comp"])
        n1, n2 = NM.next(), NM.next()
        if k in ("join", "add"):
            a, b = R.randint(11, 60), R.randint(2, 35)
            if a + b > 99 or not ones_ok(a, b, True):
                return None
            if k == "join":
                q = "%s %s %d%s, %s %d%s 가지고 있어요. 두 사람이 가진 %s 모두 몇 %s일까요?" % (josa(n1, "은/는"), t, a, c, josa(n2, "은/는"), b, c, josa(t, "은/는"), c)
            else:
                q = "%s %d%s 있었어요. %d%s를 더 샀어요. %s 모두 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c)
            r = a + b
            w = [r + 10, r - 10, r + 1, a - b if a > b else b - a]
            return mcq(q, "%d%s" % (r, c), ["%d%s" % (x, c) for x in w if x > 0], "%d + %d = <b>%d</b>" % (a, b, r))
        a, b = R.randint(25, 99), R.randint(2, 40)
        if b >= a or not ones_ok(a, b, False):
            return None
        if k == "take":
            q = "%s %d%s 있었어요. 그중에서 %d%s를 친구에게 주었어요. 남은 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c)
        else:
            q = "%s %s %d%s, %s %d%s 가지고 있어요. %s %s보다 몇 %s 더 많이 가지고 있을까요?" % (josa(n1, "은/는"), t, a, c, josa(n2, "은/는"), b, c, josa(n1, "은/는"), n2, c)
        r = a - b
        return mcq(q, "%d%s" % (r, c), ["%d%s" % (x, c) for x in (r + 10, r - 10, r + 1, a + b) if 0 < x], "%d − %d = <b>%d</b>" % (a, b, r))
    return mk


# ------------------------------------------------------------------ 세 수、10 만들기
def three_add():
    def mk():
        a, b, c = R.randint(1, 5), R.randint(1, 4), R.randint(1, 4)
        if a + b + c > 9:
            return None
        s = a + b + c
        return mcq("%d + %d + %d =" % (a, b, c), S(s), [S(x) for x in (a + b, b + c, s + 1, s - 1, a + c)],
                   "앞에서부터 두 수씩 차례로 더해요. %d + %d = %d, %d + %d = <b>%d</b>" % (a, b, a + b, a + b, c, s))
    return mk


def three_sub():
    def mk():
        a = R.randint(4, 9)
        b = R.randint(1, a - 2)
        c = R.randint(1, a - b - 1) if a - b > 1 else 1
        if a - b - c < 0:
            return None
        s = a - b - c
        return mcq("%d − %d − %d =" % (a, b, c), S(s), [S(x) for x in (a - b, a - (b - c) if b > c else None, s + 1, s + 2, a - c) if x is not None and x >= 0],
                   "앞에서부터 차례로 빼요. %d − %d = %d, %d − %d = <b>%d</b>" % (a, b, a - b, a - b, c, s))
    return mk


def three_mixed():
    def mk():
        a, b = R.randint(2, 7), R.randint(1, 5)
        if R.random() < 0.5:
            if a + b > 9:
                return None
            c = R.randint(1, a + b - 1)
            s = a + b - c
            t = "%d + %d − %d" % (a, b, c)
            st = "%d + %d = %d, %d − %d = <b>%d</b>" % (a, b, a + b, a + b, c, s)
        else:
            if b >= a:
                return None
            c = R.randint(1, 9 - (a - b))
            s = a - b + c
            t = "%d − %d + %d" % (a, b, c)
            st = "%d − %d = %d, %d + %d = <b>%d</b>" % (a, b, a - b, a - b, c, s)
        return mcq(t + " =", S(s), [S(x) for x in (s + 1, s - 1, s + 2, a + b + c) if 0 <= x], "앞에서부터 차례로 계산해요. " + st)
    return mk


def three_story():
    def mk():
        t, c = th()
        a, b, d = R.randint(2, 5), R.randint(1, 3), R.randint(1, 3)
        if R.random() < 0.5:
            if a + b + d > 9:
                return None
            q = "%s %d%s 있어요. 엄마가 %d%s, 아빠가 %d%s를 더 주셨어요. %s 모두 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, d, c, josa(t, "은/는"), c)
            return mcq(q, "%d%s" % (a + b + d, c), ["%d%s" % (x, c) for x in (a + b, a + d, a + b + d + 1, a + b + d - 1)],
                       "%d + %d + %d = <b>%d</b>" % (a, b, d, a + b + d))
        a = R.randint(6, 9)
        if a - b - d < 0:
            return None
        q = "%s %d%s 있었어요. 형에게 %d%s, 동생에게 %d%s를 주었어요. 남은 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, d, c, josa(t, "은/는"), c)
        return mcq(q, "%d%s" % (a - b - d, c), ["%d%s" % (x, c) for x in (a - b, a - d, a - b - d + 1, a - b - d + 2)],
                   "%d − %d − %d = <b>%d</b>" % (a, b, d, a - b - d))
    return mk


def make10():
    def mk():
        a = R.randint(1, 9)
        how = R.choice(["box", "frame", "pair"])
        if how == "box":
            return mcq("%d + □ = 10<br>□에 알맞은 수는 무엇일까요?" % a, S(10 - a), [S(x) for x in near(10 - a, 0, 10) + [a]],
                       "%d와 %d를 모으면 10이에요. <b>%d</b>" % (a, 10 - a, 10 - a))
        if how == "frame":
            k = R.choice(["dot", "apple", "star", "ball"])
            return mcq("10이 되도록 더하려면 몇을 더해야 할까요?%s" % tenframe(a, 1, k), S(10 - a), [S(x) for x in near(10 - a, 0, 10) + [a]],
                       "빈칸이 %d칸이에요. %d + %d = 10, <b>%d</b>" % (10 - a, a, 10 - a, 10 - a))
        b = 10 - a
        return mcq("<b>%d</b>와 더해서 10이 되는 수는 무엇일까요?" % a, S(b), [S(x) for x in near(b, 0, 10) + [a]], "%d + %d = 10, <b>%d</b>" % (a, b, b))
    return mk


def from10():
    def mk():
        b = R.randint(1, 9)
        k = R.choice(KINDS)
        if R.random() < 0.5:
            return mcq("10 − %d =" % b, S(10 - b), [S(x) for x in near(10 - b, 0, 10) + [b]],
                       "%d와 %d를 모으면 10이므로 10 − %d = <b>%d</b>" % (b, 10 - b, b, 10 - b))
        return mcq("%s 10%s 중에서 %d%s를 지웠어요. 남은 것은 몇 %s일까요?%s" % (nm(k), cw(k), b, cw(k), cw(k), crossed(10, k, b)), "%d%s" % (10 - b, cw(k)),
                   ["%d%s" % (x, cw(k)) for x in near(10 - b, 0, 10) + [b]], "10 − %d = <b>%d</b>" % (b, 10 - b))
    return mk


def ten_plus():
    def mk():
        a = R.randint(1, 9)
        c = R.randint(1, 9)
        if R.random() < 0.5:
            t = "%d + %d + %d" % (a, 10 - a, c)
            st = "앞의 두 수 %d + %d = 10을 먼저 계산해요. 10 + %d = <b>%d</b>" % (a, 10 - a, c, 10 + c)
        else:
            t = "%d + %d + %d" % (c, a, 10 - a)
            st = "뒤의 두 수 %d + %d = 10을 먼저 계산해요. %d + 10 = <b>%d</b>" % (a, 10 - a, c, 10 + c)
        return mcq(t + " =", S(10 + c), [S(x) for x in (10 + c + 1, 10 + c - 1, c, 20 + c if c else 21) if x != 10 + c], st)
    return mk


def ten_plus_story():
    def mk():
        t, c = th()
        a = R.randint(2, 8)
        d = R.randint(1, 8)
        q = "%s 바구니에 %d%s, 상자에 %d%s, 가방에 %d%s 있어요. %s 모두 몇 %s일까요?" % (josa(t, "이/가"), a, c, 10 - a, c, d, c, josa(t, "은/는"), c)
        return mcq(q, "%d%s" % (10 + d, c), ["%d%s" % (x, c) for x in (10 + d + 1, 10 + d - 1, 10, a + d)],
                   "%d + %d = 10을 먼저 만들어요. 10 + %d = <b>%d</b>" % (a, 10 - a, d, 10 + d))
    return mk


# ------------------------------------------------------------------ 20까지（받아올림・받아내림）
def carry_split():
    def mk():
        a, b = R.randint(5, 9), R.randint(3, 9)
        if a + b <= 10:
            return None
        k = 10 - a
        if R.random() < 0.5:
            return mcq("%d + %d에서 %d을 10으로 만들려고 해요.<br>%d + %d = %d + %d + □<br>□에 알맞은 수는 무엇일까요?" % (a, b, a, a, b, a, k, ),
                       S(b - k), [S(x) for x in (k, b, b - k + 1, b - k - 1 if b - k > 1 else b + 1)],
                       "%d를 %d와 %d로 갈라요. %d + %d = 10, 10 + %d = %d. <b>%d</b>" % (b, k, b - k, a, k, b - k, a + b, b - k))
        f = tenframe(a + b, 2, "dot")
        return mcq("10칸 상자를 보고 계산해요. %d + %d는 얼마일까요?%s" % (a, b, f), S(a + b), [S(x) for x in near(a + b, 10, 20) + [a + b - 10]],
                   "10칸을 먼저 채우고 남은 것을 세어요. 10과 %d → <b>%d</b>" % (a + b - 10, a + b))
    return mk


def carry_add():
    def mk():
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a + b <= 10:
            return None
        c = a + b
        return mcq("%d + %d =" % (a, b), S(c), [S(x) for x in (c + 1, c - 1, c - 10, 10 + abs(a - b) if 10 + abs(a - b) != c else c + 2)],
                   "%d에 %d를 더해 10을 만들고, 남은 %d를 더해요. <b>%d</b>" % (max(a, b), 10 - max(a, b), c - 10, c))
    return mk


def borrow_split():
    def mk():
        a = R.randint(11, 18)
        b = R.randint(a - 9, 9)
        if a % 10 >= b:
            return None
        if R.random() < 0.5:
            return mcq("%d − %d를 계산하려고 해요. %d를 10과 %d로 가르면<br>%d − %d = 10 − %d + □<br>□에 알맞은 수는 무엇일까요?" % (a, b, a, a - 10, a, b, b),
                       S(a - 10), [S(x) for x in (b, 10 - b, a - b, a - 10 + 1)],
                       "10에서 %d를 빼면 %d이에요. 남은 %d를 더하면 %d. <b>%d</b>" % (b, 10 - b, a - 10, a - b, a - 10))
        return mcq("%d − %d를 %d − %d − %d로 계산하려고 해요. 계산 결과는 얼마일까요?" % (a, b, a, a - 10, b - (a - 10)), S(a - b),
                   [S(x) for x in (10 + b - a % 10, a - b + 1, a - b - 1, 10) if x != a - b],
                   "%d − %d = 10, 10 − %d = <b>%d</b>" % (a, a - 10, b - (a - 10), a - b))
    return mk


def borrow_sub():
    def mk():
        a = R.randint(11, 18)
        b = R.randint(2, 9)
        if a % 10 >= b or a - b > 9:
            return None
        c = a - b
        return mcq("%d − %d =" % (a, b), S(c), [S(x) for x in (10 + b - a % 10, c + 1, c - 1, a + b - 10) if 0 <= x and x != c],
                   "일의 자리 %d에서 %d를 뺄 수 없어요. 10에서 %d를 빼고 %d를 더해요. <b>%d</b>" % (a % 10, b, b, a % 10, c))
    return mk


def story20():
    def mk():
        t, c = th()
        k = R.choice(["join", "add", "take", "comp"])
        n1, n2 = NM.next(), NM.next()
        if k in ("join", "add"):
            a, b = R.randint(3, 9), R.randint(3, 9)
            if a + b <= 10:
                return None
            if k == "join":
                q = "%s %s %d%s, %s %d%s 가지고 있어요. 두 사람이 가진 %s 모두 몇 %s일까요?" % (josa(n1, "은/는"), t, a, c, josa(n2, "은/는"), b, c, josa(t, "은/는"), c)
            else:
                q = "%s %d%s 있었어요. %d%s를 더 받았어요. %s 모두 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c)
            r = a + b
            return mcq(q, "%d%s" % (r, c), ["%d%s" % (x, c) for x in (r + 1, r - 1, abs(a - b), r - 10)], "%d + %d = <b>%d</b>" % (a, b, r))
        a = R.randint(11, 18)
        b = R.randint(2, 9)
        if a % 10 >= b or a - b > 9:
            return None
        if k == "take":
            q = "%s %d%s 있었어요. %d%s를 먹었어요. 남은 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c) if t in ("사탕", "딸기", "쿠키", "귤") else \
                "%s %d%s 있었어요. %d%s를 친구에게 주었어요. 남은 %s 몇 %s일까요?" % (josa(t, "이/가"), a, c, b, c, josa(t, "은/는"), c)
            if c == "마리":
                q = "%s %d마리 있었어요. %d마리가 날아갔어요. 남은 %s 몇 마리일까요?" % (josa(t, "이/가"), a, b, josa(t, "은/는")) if t == "참새" else \
                    "%s %d마리 있었어요. %d마리가 집으로 갔어요. 남은 %s 몇 마리일까요?" % (josa(t, "이/가"), a, b, josa(t, "은/는"))
        else:
            q = "%s %s %d%s, %s %d%s 가지고 있어요. %s %s보다 몇 %s 더 많이 가지고 있을까요?" % (josa(n1, "은/는"), t, a, c, josa(n2, "은/는"), b, c, josa(n1, "은/는"), n2, c)
            if c == "마리":
                return None
        r = a - b
        return mcq(q, "%d%s" % (r, c), ["%d%s" % (x, c) for x in (10 + b - a % 10, r + 1, r - 1, a + b) if x > 0 and x != r], "%d − %d = <b>%d</b>" % (a, b, r))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "in9":
        return unit(G, "addition-and-subtraction-within-9", 3, "[2수01-04] [2수01-05]",
                    "하나의 수를 두 수로 분해하고 두 수를 하나의 수로 합성하는 활동을 통하여 수 감각을 기른다. 덧셈과 뺄셈이 이루어지는 실생활 상황과 연결하여 덧셈과 뺄셈의 의미를 이해한다.",
                    "모으기와 가르기, 9까지의 덧셈과 뺄셈", "덧셈과 뺄셈",
                    "초등 1학년 1학기 덧셈과 뺄셈 학습지: 모으기와 가르기, 그림을 보고 덧셈식·뺄셈식 쓰기, 9까지의 덧셈과 뺄셈, 0이 있는 계산, 이야기 문제까지 100문제와 정답.",
                    "모으면 덧셈, 덜어 내면 뺄셈", "3과 2를 모으면 5 → 3 + 2 = 5",
                    ["두 수를 하나로 합치는 것을 <b>모으기</b>, 하나의 수를 두 수로 나누는 것을 <b>가르기</b>라고 해요.",
                     "모두 몇 개인지 알아볼 때는 <b>덧셈</b>을 해요. 3 + 2 = 5는 '3 더하기 2는 5와 같습니다'라고 읽어요.",
                     "남은 것이나 더 많은 것이 몇 개인지 알아볼 때는 <b>뺄셈</b>을 해요. 5 − 2 = 3은 '5 빼기 2는 3과 같습니다'라고 읽어요.",
                     "어떤 수에 0을 더하거나 빼면 그 수 그대로예요."],
                    [("사과 4개와 3개를 모으면?", ["4 + 3을 계산해요.", "4, 5, 6, 7 하고 이어 세요."], "7개"),
                     ("풍선 8개 중 3개가 터지면?", ["8 − 3을 계산해요."], "5개")],
                    [("4 + 3을 4, 5, 6으로 세어 6이라고 한다", "4 다음부터 5, 6, 7 하고 세어요."),
                     ("'몇 개 더 많은지'에 덧셈을 한다", "더 많은 것을 구할 때는 뺄셈을 해요."),
                     ("5 − 0을 0이라고 한다", "0을 빼면 그 수 그대로 5예요.")],
                    [("1학기 덧셈과 뺄셈에서는 무엇을 배우나요?", "9까지의 수를 모으고 가르고, 한 자리 수의 덧셈과 뺄셈을 배워요."),
                     ("손가락으로 세어도 되나요?", "처음에는 괜찮아요. 모으기와 가르기를 익히면 세지 않고도 바로 답을 떠올릴 수 있어요.")],
                    [("모으기와 가르기", [(bond9(), 12), (dice_sum(), 4), (split_ways(), 4)]),
                     ("덧셈하기", [(add_pic(), 20)]),
                     ("뺄셈하기", [(sub_pic(), 20)]),
                     ("계산하기", [(calc9("+"), 8), (calc9("−"), 8), (biggest_expr(), 4)]),
                     ("이야기 문제", [(story9(), 20)])], 82103)
    if which == "two":
        return unit(G, "two-digit-addition-and-subtraction", 7, "[2수01-05] [2수01-06]",
                    "덧셈과 뺄셈이 이루어지는 실생활 상황과 연결하여 덧셈과 뺄셈의 의미를 이해한다. 두 자리 수의 범위에서 덧셈과 뺄셈의 계산 원리를 이해하고 그 계산을 할 수 있다.",
                    "두 자리 수의 덧셈과 뺄셈(받아올림 없음)", "덧셈과 뺄셈(1)",
                    "초등 1학년 2학기 덧셈과 뺄셈(1) 학습지: (몇십몇)+(몇), (몇십)+(몇십), (몇십몇)+(몇십몇), 받아내림 없는 뺄셈, 이야기 문제까지 100문제와 정답.",
                    "일의 자리끼리, 십의 자리끼리", "34 + 5에서 5는 일의 자리 4에 더해요.",
                    ["두 자리 수는 10개씩 묶음(십의 자리)과 낱개(일의 자리)로 되어 있어요.",
                     "덧셈과 뺄셈은 <b>일의 자리끼리, 십의 자리끼리</b> 계산해요.",
                     "(몇십몇) + (몇)은 낱개끼리 더해요. 34 + 5 → 4 + 5 = 9 → 39",
                     "(몇십) − (몇십)은 10개씩 묶음끼리 빼요. 70 − 30 → 7 − 3 = 4 → 40"],
                    [("23 + 45", ["일의 자리: 3 + 5 = 8", "십의 자리: 2 + 4 = 6"], "68"),
                     ("58 − 3", ["일의 자리: 8 − 3 = 5", "십의 자리는 그대로 5"], "55")],
                    [("34 + 5를 84라고 한다", "5는 낱개예요. 일의 자리에 더해요: 39"),
                     ("47 − 3을 17이라고 한다", "3은 일의 자리 7에서 빼요: 44"),
                     ("40 + 30을 7이라고 한다", "10개씩 묶음이 7개이니 70이에요.")],
                    [("받아올림은 언제 배우나요?", "받아올림이 있는 두 자리 수의 덧셈은 2학년 1학기에 배워요."),
                     ("수 모형이 없으면 어떻게 하나요?", "빨대 10개를 고무줄로 묶어 10개씩 묶음을 만들어 써 보세요.")],
                    [("(몇십몇) + (몇)", [(add2("tt1"), 14), (add2("t1"), 6)]),
                     ("(몇십몇) + (몇십몇)", [(add2("tt"), 6), (add2("tt2"), 14)]),
                     ("(몇십몇) − (몇)", [(sub2("tt1"), 14), (sub2("tt"), 6)]),
                     ("(몇십몇) − (몇십몇)", [(sub2("tt2"), 20)]),
                     ("이야기 문제", [(story2(), 20)])], 82107)
    if which == "three":
        return unit(G, "adding-three-numbers-and-making-10", 8, "[2수01-04] [2수01-08]",
                    "하나의 수를 두 수로 분해하고 두 수를 하나의 수로 합성하는 활동을 통하여 수 감각을 기른다. 두 자리 수의 범위에서 세 수의 덧셈과 뺄셈을 할 수 있다.",
                    "세 수의 계산과 10 만들기", "덧셈과 뺄셈(2)",
                    "초등 1학년 2학기 덧셈과 뺄셈(2) 학습지: 세 수의 덧셈과 뺄셈, 10이 되는 더하기, 10에서 빼기, 10을 만들어 세 수 더하기, 이야기 문제까지 100문제와 정답.",
                    "더해서 10이 되는 두 수를 먼저", "7 + 3 + 5 → 10 + 5 = 15",
                    ["세 수의 계산은 <b>앞에서부터 두 수씩 차례로</b> 계산해요.",
                     "더해서 10이 되는 두 수: 1과 9, 2와 8, 3과 7, 4와 6, 5와 5",
                     "10에서 빼기: 10 − 3은 3과 몇을 모으면 10인지 생각해요. 3과 7 → 7",
                     "세 수 중 더해서 10이 되는 두 수를 먼저 더하면 쉬워요. 4 + 6 + 8 = 10 + 8 = 18"],
                    [("5 + 2 + 1", ["5 + 2 = 7", "7 + 1 = 8"], "8"),
                     ("6 + 3 + 7", ["3 + 7 = 10을 먼저", "6 + 10 = 16"], "16")],
                    [("8 − 3 − 2에서 뒤의 3 − 2를 먼저 한다", "앞에서부터 차례로: 8 − 3 = 5, 5 − 2 = 3"),
                     ("10 − 4를 5라고 한다", "4와 6을 모으면 10이에요. 답은 6"),
                     ("세 수 중 두 수만 더한다", "세 수를 모두 더했는지 확인해요.")],
                    [("10 만들기가 왜 중요한가요?", "받아올림이 있는 덧셈(8 + 5 = 8 + 2 + 3)에서 10을 먼저 만드는 데 꼭 필요해요."),
                     ("10이 되는 짝을 어떻게 외우나요?", "10칸 상자에 바둑돌을 채워 보며 빈칸 수를 세어 보세요.")],
                    [("세 수의 덧셈", [(three_add(), 14), (three_mixed(), 6)]),
                     ("세 수의 뺄셈", [(three_sub(), 14), (three_story(), 6)]),
                     ("10이 되는 더하기", [(make10(), 20)]),
                     ("10에서 빼기", [(from10(), 20)]),
                     ("10을 만들어 더하기", [(ten_plus(), 12), (ten_plus_story(), 8)])], 82108)
    if which == "in20":
        return unit(G, "addition-and-subtraction-within-20", 9, "[2수01-04] [2수01-06]",
                    "하나의 수를 두 수로 분해하고 두 수를 하나의 수로 합성하는 활동을 통하여 수 감각을 기른다. 두 자리 수의 범위에서 덧셈과 뺄셈의 계산 원리를 이해하고 그 계산을 할 수 있다.",
                    "받아올림·받아내림이 있는 20까지의 계산", "덧셈과 뺄셈(3)",
                    "초등 1학년 2학기 덧셈과 뺄셈(3) 학습지: 10을 만들어 더하기(8 + 5), 10을 이용한 빼기(13 − 5), 계산 연습, 이야기 문제까지 100문제와 정답.",
                    "8 + 5 = 8 + 2 + 3 = 13", "더할 때는 10을 만들고, 뺄 때는 10에서 빼요.",
                    ["(몇) + (몇)의 합이 10보다 크면 <b>10을 먼저 만들어요</b>. 8 + 5는 5를 2와 3으로 갈라 8 + 2 = 10, 10 + 3 = 13",
                     "(십몇) − (몇)에서 일의 자리끼리 뺄 수 없으면 <b>10에서 빼요</b>. 13 − 5는 13을 10과 3으로 갈라 10 − 5 = 5, 5 + 3 = 8",
                     "또는 빼는 수를 갈라서 뺄 수도 있어요. 13 − 5 = 13 − 3 − 2 = 10 − 2 = 8"],
                    [("7 + 6", ["6을 3과 3으로 갈라요.", "7 + 3 = 10, 10 + 3 = 13"], "13"),
                     ("15 − 7", ["15를 10과 5로 갈라요.", "10 − 7 = 3, 3 + 5 = 8"], "8")],
                    [("13 − 5를 12라고 한다(5 − 3을 계산)", "3에서 5를 뺄 수 없으니 10에서 빼요: 8"),
                     ("8 + 5를 3이라고 하거나 103이라고 쓴다", "10을 만들고 남은 3을 더하면 13이에요."),
                     ("10을 만들 때 가른 수를 잘못 쓴다", "8은 2가 있어야 10이 돼요. 5를 2와 3으로 갈라요.")],
                    [("받아올림이 있는 덧셈을 어려워해요.", "10이 되는 두 수(2와 8, 3과 7…)를 먼저 충분히 익히면 쉬워져요."),
                     ("2학년에서는 무엇을 배우나요?", "2학년 1학기에 받아올림이 있는 두 자리 수의 덧셈과 받아내림이 있는 뺄셈을 배워요.")],
                    [("10을 만들어 더하기", [(carry_split(), 20)]),
                     ("덧셈하기", [(carry_add(), 20)]),
                     ("10을 이용해 빼기", [(borrow_split(), 20)]),
                     ("뺄셈하기", [(borrow_sub(), 20)]),
                     ("이야기 문제", [(story20(), 20)])], 82109)
    raise ValueError(which)
