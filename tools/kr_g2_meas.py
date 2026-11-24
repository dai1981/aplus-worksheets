# -*- coding: utf-8 -*-
"""
대한민국 초등 2학년 수학：측정（2022 개정）の 4 単元
  cm      : 길이 재기（1 cm、자로 재기、약 몇 cm、어림하기）[2수03-10] [2수03-12]  2-1
  m       : 길이 재기（1 m、몇 m 몇 cm、길이의 합과 차）[2수03-11] [2수03-13]      2-2
  time    : 시각과 시간（몇 시 몇 분、몇 분 전、1시간 = 60분、오전・오후）[2수03-07] [2수03-08]  2-2
  calendar: 달력（1주일・1개월・1년）[2수03-09]                                      2-2
誤答は「자의 0이 아닌 곳에서 시작했는데 끝 눈금을 읽는다」「눈금 칸이 아니라 눈금 수를 센다（+1）」「2 m 5 cm를 25 cm라고 한다」
「긴바늘이 가리키는 숫자를 그대로 분으로 읽는다（4 → 4분）」「1시간을 100분으로 계산한다」「모든 달이 30일이라고 생각한다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa, clock
from kr_pics import ruler
from kr_low import fig
from ws_common import svg_wrap, text, INK, GREEN, RED, FILL

R = random.Random(82208)
NM = Names(R)
G = "grade-2"
OBJ = ["막대", "연필", "리본", "크레파스", "색 테이프", "빨대", "지우개", "끈"]
DAYS = ["일", "월", "화", "수", "목", "금", "토"]
MDAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def S(x):
    return str(x)


def cm(x):
    return "%d cm" % x


# ------------------------------------------------------------------ cm
def r0():
    def mk():
        L = R.randint(2, 11)
        o = R.choice(OBJ)
        return mcq("%s의 길이는 몇 cm일까요?%s" % (o, ruler(0, L * 10, max(L + 2, 8), o)), cm(L), [cm(x) for x in (L + 1, L - 1, L + 2) if x > 0],
                   "0에서 시작해 1 cm가 %d번이에요. <b>%d cm</b>" % (L, L))
    return mk


def rs():
    def mk():
        s = R.randint(1, 6)
        L = R.randint(2, 8)
        o = R.choice(OBJ)
        return mcq("%s의 길이는 몇 cm일까요? (자의 %d에서 시작해요)%s" % (o, s, ruler(s * 10, (s + L) * 10, s + L + 2, o)) if R.random() < 0.3 else
                   "%s의 길이는 몇 cm일까요?%s" % (o, ruler(s * 10, (s + L) * 10, s + L + 2, o)),
                   cm(L), [cm(x) for x in (s + L, L + 1, L - 1 if L > 2 else L + 2, s)],
                   "%d부터 %d까지 1 cm가 %d번이에요. %d − %d = %d. <b>%d cm</b>" % (s, s + L, L, s + L, s, L, L))
    return mk


def rabout():
    def mk():
        s = R.choice([0, 0, 1, 2, 3])
        L = R.randint(3, 9)
        off = R.choice([2, 3, 7, 8])
        end = (s + L) * 10 + off
        ans = L + (1 if off >= 5 else 0)
        o = R.choice(OBJ)
        return mcq("%s의 길이는 약 몇 cm일까요?%s" % (o, ruler(s * 10, end, s + L + 3, o)), "약 %d cm" % ans,
                   ["약 %d cm" % x for x in (ans + 1, ans - 1, s + ans, ans + 2) if x > 0 and x != ans],
                   "끝이 %d cm와 %d cm 사이에서 %d cm에 더 가까워요. <b>약 %d cm</b>" % (s + L, s + L + 1, s + ans, ans) if s else
                   "끝이 %d cm와 %d cm 사이에서 %d cm에 더 가까워요. <b>약 %d cm</b>" % (L, L + 1, ans, ans))
    return mk


def unit_len():
    """단위길이：뼘・클립・지우개로 재기"""
    def mk():
        how = R.choice(["who", "which", "cm"])
        if how == "who":
            n1, n2 = NM.next(), NM.next()
            if n1 == n2:
                return None
            a, b = R.sample(range(5, 12), 2)
            thing = R.choice(["책상의 긴 쪽", "칠판의 긴 쪽", "사물함의 높이", "식탁의 긴 쪽"])
            longer = n1 if a < b else n2
            return mcq("%s %s 뼘으로 재었더니 %s %d뼘, %s %d뼘이었어요. 누구의 한 뼘이 더 길까요?" % ("두 사람이", thing, josa(n1, "은/는"), a, josa(n2, "은/는"), b),
                       longer, [n2 if longer == n1 else n1, "두 사람이 같아요", "알 수 없어요"],
                       "같은 길이를 잴 때 단위가 길수록 잰 횟수가 적어요. 횟수가 적은 <b>%s</b>의 뼘이 더 길어요." % longer)
        if how == "which":
            us = R.sample([("클립", 3), ("지우개", 5), ("풀", 9), ("연필", 15), ("크레파스", 7)], 3)
            L = 45
            ok = max(us, key=lambda u: u[1])[0]
            txt = ", ".join("%s %d번" % (josa(u[0], "으로/로"), L // u[1]) for u in us)
            return mcq("같은 끈의 길이를 여러 물건으로 재었어요: %s<br>가장 긴 물건은 무엇일까요?" % txt, ok, [u[0] for u in us if u[0] != ok] + ["모두 같아요"],
                       "잰 횟수가 가장 적은 것이 가장 긴 단위예요. <b>%s</b>" % ok)
        k = R.randint(3, 12)
        return mcq("1 cm로 <b>%d번</b> 잰 길이는 몇 cm일까요?" % k, cm(k), [cm(x) for x in (k + 1, k - 1, 10 * k, 1)],
                   "1 cm가 %d번이면 <b>%d cm</b>예요." % (k, k))
    return mk


EST = [("연필 한 자루의 길이", 15), ("지우개의 긴 쪽", 5), ("새끼손가락의 너비", 1), ("공책의 긴 쪽", 25), ("칫솔의 길이", 18), ("숟가락의 길이", 20),
       ("크레파스 한 개의 길이", 8), ("100원짜리 동전의 너비", 2), ("교과서의 짧은 쪽", 19), ("스마트폰의 긴 쪽", 15), ("가위의 길이", 14),
       ("풀(딱풀)의 길이", 9), ("엄지손가락의 길이", 6)]


def estimate():
    pool = EST[:]
    R.shuffle(pool)

    def mk():
        how = R.choice(["fact", "fact", "diff"])
        if how == "fact" and pool:
            o, v = pool.pop()
            return mcq("<b>%s</b> 약 몇 cm일까요?" % josa(o, "은/는"),
                       "약 %d cm" % v, ["약 %d cm" % x for x in (v * 10, v * 3 if v > 1 else 10, max(1, v // 3) if v > 3 else v + 20, v + 40) if x != v],
                       "1 cm는 새끼손가락의 너비쯤이에요. %s 약 <b>%d cm</b>예요." % (josa(o, "은/는"), v))
        L = R.randint(8, 25)
        n1, n2 = NM.next(), NM.next()
        if n1 == n2:
            return None
        a, b = L + R.choice([-3, -2, 2, 3, 4]), L + R.choice([-1, 1])
        if R.random() < 0.5:
            a, b = b, a
        o = R.choice(OBJ)
        best = n1 if abs(a - L) < abs(b - L) else n2
        return mcq("%s의 길이를 %s 약 %d cm, %s 약 %d cm로 어림했어요. 자로 재었더니 %d cm였어요. 누가 더 가깝게 어림했을까요?" % (o, josa(n1, "은/는"), a, josa(n2, "은/는"), b, L),
                   best, [n2 if best == n1 else n1, "두 사람이 같아요", "알 수 없어요"],
                   "어림한 길이와 잰 길이의 차이: %s %d cm, %s %d cm. 차이가 작은 <b>%s</b>" % (n1, abs(a - L), n2, abs(b - L), best))
    return mk


# ------------------------------------------------------------------ m
def m_conv():
    def mk():
        how = R.choice(["m2cm", "cm2m", "mix2cm", "cm2mix"])
        a = R.randint(1, 9)
        if how == "m2cm":
            return mcq("%d m = □ cm<br>□에 알맞은 수는 무엇일까요?" % a, S(a * 100), [S(x) for x in (a * 10, a * 1000, a + 100, a)],
                       "1 m = 100 cm이므로 %d m = <b>%d cm</b>예요." % (a, a * 100))
        if how == "cm2m":
            return mcq("%d cm = □ m<br>□에 알맞은 수는 무엇일까요?" % (a * 100), S(a), [S(x) for x in (a * 10, a * 100, a + 1)],
                       "100 cm = 1 m이므로 %d cm = <b>%d m</b>예요." % (a * 100, a))
        c = R.choice([R.randint(1, 9), R.randint(10, 99)])
        if how == "mix2cm":
            n = a * 100 + c
            return mcq("%d m %d cm = □ cm<br>□에 알맞은 수는 무엇일까요?" % (a, c), S(n), [S(x) for x in (a * 10 + c if c < 10 else int("%d%d" % (a, c)) * 10, int("%d%d" % (a, c)) if c < 10 else n + 100, a * 1000 + c, a + c) if x != n],
                       "%d m = %d cm, %d cm + %d cm = <b>%d cm</b>" % (a, a * 100, a * 100, c, n))
        n = a * 100 + c
        ok = "%d m %d cm" % (a, c)
        bad = ["%d m %d cm" % (a, c * 10) if c < 10 else "%d m %d cm" % (a * 10 + c // 10, c % 10), "%d m %d cm" % (n // 10, n % 10), "%d m %d cm" % (a + 1, c)]
        return mcq("<b>%d cm</b>는 몇 m 몇 cm일까요?" % n, ok, bad, "%d cm = %d cm + %d cm = <b>%s</b>" % (n, a * 100, c, ok))
    return mk


def m_unit():
    F = [("교실 문의 높이", "약 2 m", ["약 2 cm", "약 20 m", "약 20 cm"]),
         ("양팔을 벌린 길이", "약 1 m 20 cm", ["약 12 cm", "약 12 m", "약 120 m"]),
         ("버스의 길이", "약 10 m", ["약 10 cm", "약 100 m", "약 1 m"]),
         ("2학년 친구의 키", "약 125 cm", ["약 12 cm", "약 125 m", "약 25 cm"]),
         ("칠판의 긴 쪽", "약 4 m", ["약 4 cm", "약 40 m", "약 40 cm"]),
         ("침대의 긴 쪽", "약 2 m", ["약 2 cm", "약 20 m", "약 20 cm"]),
         ("운동장 한쪽 끝에서 다른 끝까지", "약 80 m", ["약 80 cm", "약 8 cm", "약 8 m"]),
         ("자동차의 길이", "약 4 m", ["약 4 cm", "약 40 cm", "약 40 m"])]
    pool = F[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        o, a, b = pool.pop()
        return mcq("<b>%s</b>%s 얼마쯤일까요?" % (o, "는" if not (ord(o[-1]) - 0xAC00) % 28 else "은"), a, b,
                   "1 m는 약 100 cm, 어른의 한 걸음보다 조금 더 길어요. <b>%s</b>" % a)
    return mk


def m_add(op):
    def mk():
        a1, b1 = R.randint(1, 6), R.randint(10, 80)
        a2, b2 = R.randint(1, 4), R.randint(5, 60)
        if op == "+":
            if b1 + b2 >= 100:
                return None
            ra, rb = a1 + a2, b1 + b2
            q = "%d m %d cm + %d m %d cm =" % (a1, b1, a2, b2)
            bad = ["%d m %d cm" % (ra, rb + 10), "%d m %d cm" % (ra + 1, rb), "%d m %d cm" % (ra - 1, rb)]
            st = "m는 m끼리, cm는 cm끼리 더해요. %d + %d = %d(m), %d + %d = %d(cm). <b>%d m %d cm</b>" % (a1, a2, ra, b1, b2, rb, ra, rb)
        else:
            if a1 <= a2 or b1 < b2:
                return None
            ra, rb = a1 - a2, b1 - b2
            q = "%d m %d cm − %d m %d cm =" % (a1, b1, a2, b2)
            bad = ["%d m %d cm" % (ra, rb + 10), "%d m %d cm" % (ra + 1, rb), "%d m %d cm" % (a1 + a2, rb)]
            st = "m는 m끼리, cm는 cm끼리 빼요. %d − %d = %d(m), %d − %d = %d(cm). <b>%d m %d cm</b>" % (a1, a2, ra, b1, b2, rb, ra, rb)
        return mcq(q, "%d m %d cm" % (ra, rb), bad, st)
    return mk


def m_story():
    def mk():
        how = R.choice(["join", "cut", "comp"])
        a1, b1 = R.randint(1, 5), R.randint(10, 80)
        a2, b2 = R.randint(1, 3), R.randint(5, 70)
        if how == "join":
            if b1 + b2 >= 100:
                return None
            q = "%d m %d cm인 색 테이프와 %d m %d cm인 색 테이프를 겹치지 않게 이었어요. 이은 색 테이프의 길이는 몇 m 몇 cm일까요?" % (a1, b1, a2, b2)
            ra, rb = a1 + a2, b1 + b2
        else:
            if a1 <= a2 or b1 < b2:
                return None
            ra, rb = a1 - a2, b1 - b2
            if how == "cut":
                q = "끈 %d m %d cm 중에서 %d m %d cm를 잘라 썼어요. 남은 끈은 몇 m 몇 cm일까요?" % (a1, b1, a2, b2)
            else:
                n1, n2 = NM.next(), NM.next()
                if n1 == n2:
                    return None
                q = "%s 털실 %d m %d cm, %s 털실 %d m %d cm를 가지고 있어요. %s %s보다 몇 m 몇 cm 더 많이 가지고 있을까요?" % (josa(n1, "은/는"), a1, b1, josa(n2, "은/는"), a2, b2, josa(n1, "은/는"), n2)
        ok = "%d m %d cm" % (ra, rb)
        return mcq(q, ok, ["%d m %d cm" % (ra, rb + 10), "%d m %d cm" % (ra + 1, rb), "%d m %d cm" % (a1 + a2 if how != "join" else ra - 1, rb)],
                   "m는 m끼리, cm는 cm끼리 계산해요. <b>%s</b>" % ok)
    return mk


def m_compare():
    def mk():
        a, c = R.randint(1, 4), R.randint(1, 99)
        n = a * 100 + c
        d = R.choice([-30, -12, -5, 5, 12, 30, 90])
        o = n + d
        if o <= 100:
            return None
        txt1 = "%d m %d cm" % (a, c)
        txt2 = "%d cm" % o
        big = txt1 if n > o else txt2
        return mcq("더 긴 길이는 무엇일까요?<br><b>%s</b>, <b>%s</b>" % (txt1, txt2), big, [txt2 if big == txt1 else txt1, "길이가 같아요", "알 수 없어요"],
                   "%s = %d cm예요. %d cm와 %d cm를 비교하면 <b>%s</b>%s 더 길어요." % (txt1, n, n, o, big, "가"))
    return mk


# ------------------------------------------------------------------ 시각과 시간
def tm(h, m):
    return "%d시 %d분" % (h, m) if m else "%d시" % h


def read5():
    def mk():
        h, m = R.randint(1, 12), R.choice(range(5, 60, 5))
        nx = h % 12 + 1
        return mcq("시계가 나타내는 시각은 몇 시 몇 분일까요?%s" % clock(h, m, 170), tm(h, m),
                   [tm(h, m // 5) if m // 5 != m else tm(h, m + 5), tm(nx, m), tm(h, m + 5 if m < 55 else m - 10), tm(m // 5 if m // 5 else 12, h * 5 % 60) if m // 5 != h else tm(h, m - 5)],
                   "긴바늘이 %d을 가리키면 %d분이에요(숫자 1칸이 5분). 짧은바늘은 %d과 %d 사이 → <b>%s</b>" % (m // 5, m, h, nx, tm(h, m)))
    return mk


def read1():
    def mk():
        h, m = R.randint(1, 12), R.randint(1, 59)
        if m % 5 == 0:
            return None
        nx = h % 12 + 1
        return mcq("시계가 나타내는 시각은 몇 시 몇 분일까요?%s" % clock(h, m, 180), tm(h, m),
                   [tm(h, m + 1 if m < 59 else m - 2), tm(h, m - 1), tm(nx, m), tm(h, (m + 5) % 60 or 5)],
                   "긴바늘이 %d분 눈금을 지나 작은 눈금 %d칸을 더 갔어요. <b>%s</b>" % (m // 5 * 5, m % 5, tm(h, m)))
    return mk


def before():
    def mk():
        h = R.randint(1, 12)
        k = R.choice([5, 10, 15])
        m = 60 - k
        nx = h % 12 + 1
        if R.random() < 0.5:
            ok = "%d시 %d분 전" % (nx, k)
            return mcq("<b>%d시 %d분</b>은 몇 시 몇 분 전일까요?" % (h, m), ok, ["%d시 %d분 전" % (h, k), "%d시 %d분 전" % (nx, m), "%d시 %d분 전" % (nx, k + 5)],
                       "%d분이 더 지나면 %d시예요. <b>%s</b>" % (k, nx, ok))
        return mcq("<b>%d시 %d분 전</b>은 몇 시 몇 분일까요?" % (nx, k), tm(h, m), [tm(nx, k), tm(nx, m), tm(h, k)],
                   "%d시에서 %d분 전이면 <b>%s</b>이에요." % (nx, k, tm(h, m)))
    return mk


def hour_min():
    def mk():
        how = R.choice(["h2m", "m2h", "elapsed", "elapsed"])
        if how == "h2m":
            a, b = R.randint(1, 3), R.choice([10, 15, 20, 25, 30, 40, 45, 50])
            n = 60 * a + b
            return mcq("%d시간 %d분 = □분<br>□에 알맞은 수는 무엇일까요?" % (a, b), S(n), [S(x) for x in (100 * a + b, a * 10 + b, n + 10, n - 10)],
                       "1시간 = 60분이에요. %d시간 = %d분, %d분 + %d분 = <b>%d분</b>" % (a, 60 * a, 60 * a, b, n))
        if how == "m2h":
            n = R.choice([70, 75, 80, 90, 100, 110, 130, 150])
            ok = "%d시간 %d분" % (n // 60, n % 60)
            return mcq("<b>%d분</b>은 몇 시간 몇 분일까요?" % n, ok, ["%d시간 %d분" % (n // 100, n % 100) if n >= 100 else "%d시간 %d분" % (n // 10, n % 10),
                                                         "%d시간 %d분" % (n // 60 + 1, n % 60), "%d시간 %d분" % (n // 60, n % 60 + 10)],
                       "60분 = 1시간이에요. %d분 = 60분 + %d분%s = <b>%s</b>" % (n, n - 60, "" if n < 120 else "", ok))
        h1, m1 = R.randint(7, 10), R.choice([0, 10, 20, 30, 40])
        d = R.choice([30, 40, 50, 60, 70, 80, 90, 100, 110])
        t2 = h1 * 60 + m1 + d
        h2, m2 = t2 // 60, t2 % 60
        ok = "%d시간 %d분" % (d // 60, d % 60) if d >= 60 and d % 60 else ("%d시간" % (d // 60) if d % 60 == 0 else "%d분" % d)
        bad = ["%d분" % (100 * (h2 - h1) + m2 - m1) if 100 * (h2 - h1) + m2 - m1 > 0 else None, "%d시간 %d분" % (d // 60 + 1, d % 60) if d % 60 else "%d분" % d,
               "%d분" % (d + 10), "%d시간 %d분" % (d // 60, d % 60 + 10) if d >= 60 else "%d분" % (d - 10)]
        if ok in bad:
            return None
        return mcq("오전 %s에 시작한 놀이가 오전 %s에 끝났어요. 놀이를 한 시간은 얼마일까요?" % (tm(h1, m1), tm(h2, m2)), ok, bad,
                   "%s부터 %s까지 %d분이에요. 60분 = 1시간이므로 <b>%s</b>" % (tm(h1, m1), tm(h2, m2), d, ok))
    return mk


def ampm():
    def mk():
        how = R.choice(["dur", "day", "noon", "conv"])
        if how == "dur":
            a = R.randint(7, 11)
            b = R.randint(1, 6)
            d = 12 - a + b
            return mcq("오전 %d시부터 오후 %d시까지는 몇 시간일까요?" % (a, b), "%d시간" % d, ["%d시간" % x for x in (b - a + 12 + 1, abs(b - a), d - 1, 12 + b) if x != d and x > 0],
                       "오전 %d시부터 낮 12시까지 %d시간, 낮 12시부터 오후 %d시까지 %d시간. %d + %d = <b>%d시간</b>" % (a, 12 - a, b, b, 12 - a, b, d))
        if how == "day":
            k = R.randint(2, 4)
            return mcq("하루는 24시간이에요. <b>%d일</b>은 몇 시간일까요?" % k, "%d시간" % (24 * k), ["%d시간" % x for x in (12 * k, 24 + k, 24 * k + 24, 60 * k)],
                       "24 × %d = <b>%d시간</b>" % (k, 24 * k)) if k <= 3 else \
                mcq("<b>%d시간</b>은 며칠일까요?" % (24 * k), "%d일" % k, ["%d일" % x for x in (k + 1, k - 1, 2 * k)], "24시간이 %d번이에요. <b>%d일</b>" % (k, k))
        if how == "noon":
            F = [("낮 12시부터 밤 12시까지를 무엇이라고 할까요?", "오후", ["오전", "하루", "1주일"], "낮 12시부터 밤 12시까지는 <b>오후</b>예요."),
                 ("전날 밤 12시부터 낮 12시까지를 무엇이라고 할까요?", "오전", ["오후", "하루", "1시간"], "밤 12시부터 낮 12시까지는 <b>오전</b>이에요."),
                 ("짧은바늘은 하루에 시계를 몇 바퀴 돌까요?", "2바퀴", ["1바퀴", "12바퀴", "24바퀴"], "짧은바늘은 12시간에 한 바퀴, 하루에 <b>2바퀴</b> 돌아요."),
                 ("긴바늘이 한 바퀴 도는 데 걸리는 시간은?", "1시간(60분)", ["1분", "12시간", "100분"], "긴바늘이 한 바퀴 돌면 <b>60분</b>이 지나요.")]
            return mcq(*R.choice(F))
        a = R.randint(6, 10)
        b = R.randint(6, 9)
        d = 12 - b + a
        return mcq("어제 오후 %d시에 잠들어 오늘 오전 %d시에 일어났어요. 잠을 잔 시간은 몇 시간일까요?" % (b, a), "%d시간" % d,
                   ["%d시간" % x for x in (abs(a - b), d + 1, d - 1, a + b) if x != d and x > 0],
                   "오후 %d시부터 밤 12시까지 %d시간, 밤 12시부터 오전 %d시까지 %d시간. <b>%d시간</b>" % (b, 12 - b, a, a, d))
    return mk


# ------------------------------------------------------------------ 달력
def cal_svg(month, first, marks=()):
    """first：1일의 요일（0=일요일）"""
    n = MDAYS[month - 1]
    cw, ch = 46, 34
    W, H = 7 * cw + 10, ch * 7 + 46
    s = [text(W / 2, 26, "%d월" % month, 20)]
    for i, d in enumerate(DAYS):
        s.append(text(5 + cw * i + cw / 2, 56, d, 15, col=RED if i == 0 else BLUE_ if i == 6 else INK))
    for day in range(1, n + 1):
        idx = first + day - 1
        r, c = idx // 7, idx % 7
        x, y = 5 + c * cw, 66 + r * ch
        if day in marks:
            s.append("<circle cx='%.1f' cy='%.1f' r='15' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x + cw / 2, y + ch / 2, FILL, GREEN))
        s.append(text(x + cw / 2, y + ch / 2 + 6, str(day), 16, col=RED if c == 0 else BLUE_ if c == 6 else INK, weight=400))
    rows = (first + n + 6) // 7
    return fig(svg_wrap(W, 66 + rows * ch + 6, "".join(s), "%d월 달력" % month))


BLUE_ = "#1f5fa8"


def cal_read():
    def mk():
        mo = R.randint(1, 12)
        first = R.randint(0, 6)
        how = R.choice(["dow", "nth", "count"])
        pic = cal_svg(mo, first)
        n = MDAYS[mo - 1]
        if how == "dow":
            d = R.randint(2, n)
            w = (first + d - 1) % 7
            return mcq("%d월 %d일은 무슨 요일일까요?%s" % (mo, d, pic), DAYS[w] + "요일", [DAYS[(w + k) % 7] + "요일" for k in (1, -1, 2)],
                       "달력에서 %d일이 있는 줄의 맨 위를 봐요. <b>%s요일</b>" % (d, DAYS[w]))
        if how == "nth":
            w = R.randint(0, 6)
            k = R.randint(2, 4)
            day1 = (w - first) % 7 + 1
            d = day1 + 7 * (k - 1)
            return mcq("이달의 <b>%s %s요일</b>은 며칠일까요?%s" % (["", "첫째", "둘째", "셋째", "넷째"][k], DAYS[w], pic), "%d일" % d,
                       ["%d일" % x for x in (d + 7, d - 7, d + 1, d - 1) if 1 <= x <= n and x != d],
                       "첫째 %s요일은 %d일, 7일씩 더하면 %s %s요일은 <b>%d일</b>이에요." % (DAYS[w], day1, ["", "첫째", "둘째", "셋째", "넷째"][k], DAYS[w], d))
        w = R.randint(0, 6)
        c = sum(1 for d in range(1, n + 1) if (first + d - 1) % 7 == w)
        return mcq("이달에 <b>%s요일</b>은 모두 몇 번 있을까요?%s" % (DAYS[w], pic), "%d번" % c, ["%d번" % x for x in (3, 4, 5, 6) if x != c],
                   "%s요일인 날을 세어 보면 <b>%d번</b>이에요." % (DAYS[w], c))
    return mk


def mdays():
    def mk():
        how = R.choice(["month", "which", "which31"])
        if how == "month":
            mo = R.randint(1, 12)
            v = MDAYS[mo - 1]
            ok = "%d일" % v if mo != 2 else "28일(또는 29일)"
            return mcq("<b>%d월</b>은 며칠까지 있을까요?" % mo, ok, [x for x in ("30일", "31일", "28일(또는 29일)", "29일", "32일") if x != ok],
                       "주먹을 쥐고 손등의 튀어나온 곳은 31일, 들어간 곳은 30일(2월은 28일이나 29일)이에요. <b>%s</b>" % ok)
        if how == "which":
            m30 = [4, 6, 9, 11]
            m31 = [1, 3, 5, 7, 8, 10, 12]
            a = R.choice(m30)
            return mcq("날수가 <b>30일</b>인 달은 무엇일까요?", "%d월" % a, ["%d월" % x for x in R.sample(m31, 2) + [2]],
                       "날수가 30일인 달은 4월, 6월, 9월, 11월이에요. <b>%d월</b>" % a)
        m31 = [1, 3, 5, 7, 8, 10, 12]
        a = R.choice(m31)
        return mcq("날수가 <b>31일</b>인 달은 무엇일까요?", "%d월" % a, ["%d월" % x for x in R.sample([4, 6, 9, 11], 2) + [2]],
                   "날수가 31일인 달은 1, 3, 5, 7, 8, 10, 12월이에요. <b>%d월</b>" % a)
    return mk


def year_month():
    def mk():
        how = R.choice(["y2m", "m2y", "w2d", "d2w"])
        if how == "y2m":
            a, b = R.randint(1, 3), R.randint(1, 11)
            n = 12 * a + b
            return mcq("%d년 %d개월 = □개월<br>□에 알맞은 수는 무엇일까요?" % (a, b), S(n), [S(x) for x in (10 * a + b, 100 * a + b, n + 12, n - 1)],
                       "1년 = 12개월이에요. %d년 = %d개월, %d + %d = <b>%d개월</b>" % (a, 12 * a, 12 * a, b, n))
        if how == "m2y":
            n = R.randint(13, 40)
            if n % 12 == 0:
                return None
            ok = "%d년 %d개월" % (n // 12, n % 12)
            return mcq("<b>%d개월</b>은 몇 년 몇 개월일까요?" % n, ok, ["%d년 %d개월" % (n // 10, n % 10), "%d년 %d개월" % (n // 12 + 1, n % 12), "%d년 %d개월" % (n // 12, n % 12 + 1)],
                       "12개월 = 1년이에요. <b>%s</b>" % ok)
        if how == "w2d":
            a, b = R.randint(1, 4), R.randint(1, 6)
            n = 7 * a + b
            return mcq("%d주일 %d일은 며칠일까요?" % (a, b), "%d일" % n, ["%d일" % x for x in (10 * a + b, 7 * a, n + 7, n - 1)],
                       "1주일 = 7일. %d주일 = %d일, %d + %d = <b>%d일</b>" % (a, 7 * a, 7 * a, b, n))
        n = R.randint(8, 30)
        if n % 7 == 0:
            return None
        ok = "%d주일 %d일" % (n // 7, n % 7)
        return mcq("<b>%d일</b>은 몇 주일 몇 일일까요?" % n, ok, ["%d주일 %d일" % (n // 10, n % 10) if n // 10 else "%d주일 %d일" % (n // 7 + 1, n % 7),
                                                     "%d주일 %d일" % (n // 7 + 1, n % 7), "%d주일 %d일" % (n // 7, n % 7 + 1)],
                   "7일 = 1주일이에요. <b>%s</b>" % ok)
    return mk


def date_calc():
    def mk():
        how = R.choice(["same", "after", "span"])
        mo = R.randint(1, 12)
        n = MDAYS[mo - 1]
        if how == "same":
            d = R.randint(1, 10)
            w = R.randint(0, 6)
            k = R.choice([7, 14, 21])
            if d + k > n:
                return None
            return mcq("%d월 %d일이 %s요일이에요. 같은 달 %d일은 무슨 요일일까요?" % (mo, d, DAYS[w], d + k), DAYS[w] + "요일",
                       [DAYS[(w + x) % 7] + "요일" for x in (1, -1, k % 6 or 2)],
                       "7일마다 같은 요일이 돌아와요. %d일은 %d일의 %d주일 뒤예요. <b>%s요일</b>" % (d + k, d, k // 7, DAYS[w]))
        if how == "after":
            d = R.randint(1, 15)
            w = R.randint(0, 6)
            k = R.choice([2, 3, 4, 5, 9, 10])
            if d + k > n:
                return None
            return mcq("오늘은 %d월 %d일 %s요일이에요. %d일 뒤는 무슨 요일일까요?" % (mo, d, DAYS[w], k), DAYS[(w + k) % 7] + "요일",
                       [DAYS[(w + k + x) % 7] + "요일" for x in (1, -1, 2)],
                       "%d일 뒤는 %d월 %d일이에요. 요일을 하나씩 세면 <b>%s요일</b>이에요." % (k, mo, d + k, DAYS[(w + k) % 7]))
        d1 = R.randint(18, n)
        d2 = R.randint(3, 20)
        mo2 = mo % 12 + 1
        span = n - d1 + 1 + d2
        return mcq("%d월 %d일부터 %d월 %d일까지 도서관에서 책 잔치가 열려요. 책 잔치는 모두 며칠 동안 열릴까요? (첫날과 마지막 날도 셉니다)" % (mo, d1, mo2, d2), "%d일" % span,
                   ["%d일" % x for x in (span - 1, span + 1, 30 - d1 + 1 + d2 if n != 30 else 31 - d1 + 1 + d2) if x != span and x > 0],
                   "%d월은 %d일까지예요. %d월에 %d일, %d월에 %d일 → <b>%d일</b>" % (mo, n, mo, n - d1 + 1, mo2, d2, span))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "cm":
        return unit(G, "measuring-length-in-cm", 8, "[2수03-10] [2수03-12]",
                    "길이 단위 1cm와 1m를 알고, 이를 이용하여 주변 사물의 길이를 측정할 수 있다. 여러 가지 물건의 길이를 어림하고, 길이에 대한 양감을 기른다.",
                    "길이 재기: 1 cm와 자로 재기", "길이 재기(cm)",
                    "초등 2학년 1학기 길이 재기 학습지: 여러 가지 단위로 재기, 1 cm, 자로 길이 재기, 0이 아닌 눈금에서 재기, 약 몇 cm, 길이 어림하기까지 100문제와 정답.",
                    "1 cm가 몇 번인지 세어요", "자의 눈금 0에 한쪽 끝을 맞추어 재요.",
                    ["뼘이나 클립처럼 사람마다, 물건마다 길이가 다르면 잰 결과가 달라요. 그래서 <b>1 cm</b>(1 센티미터)라는 같은 단위를 써요.",
                     "자로 잴 때는 물건의 한쪽 끝을 <b>눈금 0</b>에 맞추고, 다른 쪽 끝의 눈금을 읽어요.",
                     "0이 아닌 곳에서 시작했으면 1 cm가 몇 번인지 세어요. 3부터 8까지는 5 cm예요.",
                     "끝이 눈금 사이에 있으면 가까운 쪽 눈금을 읽고 '약 몇 cm'라고 말해요."],
                    [("2에서 시작해 9에서 끝난 연필", ["1 cm가 9 − 2 = 7번"], "7 cm"),
                     ("끝이 6과 7 사이, 6에 더 가까워요", ["가까운 눈금 6"], "약 6 cm")],
                    [("0이 아닌 눈금에서 시작했는데 끝 눈금만 읽는다", "1 cm가 몇 번인지 세거나, 끝 − 시작으로 구해요."),
                     ("눈금 칸이 아니라 눈금 선의 수를 센다", "눈금 사이의 칸(1 cm)을 세어요."),
                     ("잰 횟수가 많으면 단위도 길다고 생각한다", "같은 길이를 잴 때 단위가 짧을수록 횟수가 많아요.")],
                    [("mm는 언제 배우나요?", "3학년 1학기 「길이와 시간」에서 1 mm와 1 km를 배워요."),
                     ("집에서 어떻게 연습하나요?", "숟가락, 연필 같은 물건의 길이를 먼저 어림하고 자로 재어 비교해 보세요.")],
                    [("자로 길이 재기", [(r0(), 16), (unit_len(), 4)]),
                     ("0이 아닌 눈금에서 재기", [(rs(), 20)]),
                     ("약 몇 cm", [(rabout(), 20)]),
                     ("여러 가지 단위로 재기", [(unit_len(), 20)]),
                     ("길이 어림하기", [(estimate(), 20)])], 82208)
    if which == "m":
        return unit(G, "length-in-meters-and-centimeters", 13, "[2수03-11] [2수03-13]",
                    "1m와 1cm의 관계를 이해하고, 길이를 ‘몇 m 몇 cm’와 ‘몇 cm’로 표현할 수 있다. 실생활 문제 상황과 연결하여 길이의 덧셈과 뺄셈을 할 수 있다.",
                    "길이 재기: 1 m와 길이의 합과 차", "길이 재기(m)",
                    "초등 2학년 2학기 길이 재기 학습지: 1 m = 100 cm, 몇 m 몇 cm와 몇 cm 바꾸기, 길이 비교, 길이의 합과 차, 1 m 어림하기, 이야기 문제까지 100문제와 정답.",
                    "1 m = 100 cm", "m는 m끼리, cm는 cm끼리 계산해요.",
                    ["100 cm를 <b>1 m</b>(1 미터)라고 해요. 1 m = 100 cm",
                     "130 cm는 100 cm + 30 cm = <b>1 m 30 cm</b>예요. 반대로 2 m 5 cm는 205 cm예요.",
                     "길이를 더하거나 뺄 때는 <b>m는 m끼리, cm는 cm끼리</b> 계산해요.",
                     "교실 문의 높이는 약 2 m, 양팔을 벌린 길이는 약 1 m쯤이에요."],
                    [("2 m 5 cm는 몇 cm?", ["2 m = 200 cm", "200 + 5"], "205 cm"),
                     ("1 m 40 cm + 2 m 35 cm", ["m끼리: 1 + 2 = 3", "cm끼리: 40 + 35 = 75"], "3 m 75 cm")],
                    [("2 m 5 cm를 25 cm라고 한다", "2 m는 200 cm예요: 205 cm"),
                     ("340 cm를 34 m라고 한다", "100 cm가 1 m예요: 3 m 40 cm"),
                     ("m와 cm를 섞어서 더한다", "같은 단위끼리 계산해요.")],
                    [("1 m는 어떻게 느껴 볼 수 있나요?", "1 m 줄자로 몸의 여러 부분(양팔, 걸음)을 재어 보면 양감이 생겨요."),
                     ("받아올림이 있는 길이 계산은요?", "100 cm가 넘으면 1 m로 바꾸어요. 3학년에서 더 많이 연습해요.")],
                    [("1 m = 100 cm", [(m_conv(), 20)]),
                     ("길이 비교와 어림", [(m_compare(), 12), (m_unit(), 8)]),
                     ("길이의 합", [(m_add("+"), 20)]),
                     ("길이의 차", [(m_add("−"), 20)]),
                     ("이야기 문제", [(m_story(), 20)])], 82213)
    if which == "time":
        return unit(G, "telling-time-to-the-minute", 14, "[2수03-07] [2수03-08]",
                    "시계를 보고 시각을 ‘몇 시 몇 분’까지 읽을 수 있다. 1시간과 1분의 관계를 이해하고, 시간을 ‘시간’, ‘분’으로 표현할 수 있다.",
                    "시각과 시간: 몇 시 몇 분, 1시간 = 60분", "시각과 시간",
                    "초등 2학년 2학기 시각과 시간 학습지: 5분 단위와 1분 단위로 시각 읽기, 몇 시 몇 분 전, 1시간 = 60분, 걸린 시간, 오전과 오후, 하루 24시간까지 100문제와 정답.",
                    "긴바늘의 숫자 1칸은 5분", "1시간 = 60분, 하루 = 24시간",
                    ["긴바늘이 1을 가리키면 5분, 2를 가리키면 10분, … 숫자 1칸은 <b>5분</b>이에요. 작은 눈금 1칸은 1분이에요.",
                     "2시 50분은 3시가 되기 10분 전이므로 <b>3시 10분 전</b>이라고도 해요.",
                     "긴바늘이 한 바퀴 돌면 <b>60분 = 1시간</b>이 지나요. 80분 = 1시간 20분",
                     "낮 12시 전은 <b>오전</b>, 낮 12시 후는 <b>오후</b>예요. 하루는 24시간이에요."],
                    [("긴바늘이 7, 짧은바늘이 4와 5 사이", ["7 × 5 = 35분"], "4시 35분"),
                     ("오전 10시부터 오후 2시까지", ["10시 → 12시: 2시간", "12시 → 2시: 2시간"], "4시간")],
                    [("긴바늘이 4를 가리키면 4분이라고 읽는다", "숫자 1칸이 5분이므로 20분이에요."),
                     ("1시간 20분을 120분이라고 한다", "1시간 = 60분이에요: 80분"),
                     ("오전 10시부터 오후 2시까지를 8시간이라고 한다", "낮 12시를 기준으로 나누어 세어요.")],
                    [("디지털시계만 보는데 괜찮을까요?", "바늘 시계로 '몇 분 전', '몇 시간 뒤'를 이해하는 것이 시간 계산의 기초가 돼요."),
                     ("초는 언제 배우나요?", "3학년 1학기 「길이와 시간」에서 1초와 시간의 계산을 배워요.")],
                    [("몇 시 몇 분(5분 단위)", [(read5(), 20)]),
                     ("몇 시 몇 분(1분 단위)", [(read1(), 20)]),
                     ("몇 시 몇 분 전", [(before(), 20)]),
                     ("1시간 = 60분", [(hour_min(), 20)]),
                     ("오전과 오후, 하루", [(ampm(), 20)])], 82214)
    if which == "calendar":
        return unit(G, "calendar-days-weeks-months-and-years", 15, "[2수03-09]",
                    "실생활 문제 상황과 연결하여 1분, 1시간, 1일, 1주일, 1개월, 1년 사이의 관계를 이해한다.",
                    "달력 알아보기: 1주일, 1개월, 1년", "달력",
                    "초등 2학년 2학기 달력 학습지: 달력에서 요일과 날짜 읽기, 각 달의 날수, 1주일 = 7일, 1년 = 12개월, 날짜와 요일 계산, 기간 구하기까지 100문제와 정답.",
                    "1주일 = 7일, 1년 = 12개월", "7일마다 같은 요일이 돌아와요.",
                    ["1주일은 일, 월, 화, 수, 목, 금, 토요일의 <b>7일</b>이에요. 같은 요일은 7일마다 돌아와요.",
                     "1년은 1월부터 12월까지 <b>12개월</b>이에요.",
                     "각 달의 날수: 31일인 달은 1, 3, 5, 7, 8, 10, 12월, 30일인 달은 4, 6, 9, 11월, 2월은 28일(또는 29일)이에요.",
                     "달력에서 아래 칸으로 내려가면 날짜가 7씩 커져요."],
                    [("5월 3일이 월요일이면 5월 17일은?", ["17 − 3 = 14 = 7 × 2", "2주일 뒤 같은 요일"], "월요일"),
                     ("1년 5개월은 몇 개월?", ["1년 = 12개월", "12 + 5"], "17개월")],
                    [("모든 달이 30일이라고 생각한다", "주먹으로 31일인 달과 30일인 달을 확인해요."),
                     ("1년 5개월을 15개월이라고 한다", "1년은 12개월이에요: 17개월"),
                     ("기간을 셀 때 첫날을 빼먹는다", "첫날과 마지막 날을 모두 세는지 확인해요.")],
                    [("달력 공부는 어떻게 하면 좋을까요?", "가족 생일, 방학 같은 날을 달력에 표시하고 며칠 남았는지 함께 세어 보세요."),
                     ("윤년도 배우나요?", "2학년에서는 2월이 28일 또는 29일이라는 것만 알면 돼요.")],
                    [("달력 읽기", [(cal_read(), 20)]),
                     ("각 달의 날수", [(mdays(), 14), (cal_read(), 6)]),
                     ("1주일과 1년", [(year_month(), 20)]),
                     ("날짜와 요일 계산", [(date_calc(), 20)]),
                     ("섞어서 연습", [(year_month(), 8), (date_calc(), 6), (cal_read(), 6)])], 82215)
    raise ValueError(which)
