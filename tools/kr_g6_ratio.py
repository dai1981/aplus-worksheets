# -*- coding: utf-8 -*-
"""
대한민국 초등 6학년 수학：비와 비율・백분율・여러 가지 그래프・비례식・비례배분
  ratio : 비와 비율 [6수02-02] [6수02-03]
  pct   : 백분율 [6수02-03]
  graph : 띠그래프와 원그래프 [6수04-02] [6수04-03]
  prop  : 비의 성질과 비례식 [6수02-04]
  dist  : 비례배분 [6수02-05]
誤答は「기준량과 비교하는 양을 바꾼다」「백분율에 100을 곱하지 않는다」「비례배분에서 전체를 한쪽 수로 나눈다」から作る。
"""
import math
import random
from decimal import Decimal as D
from fractions import Fraction as F
from kr_common import mcq, unit, Names, josa, fr, ff, num, table
from kr_pics56 import strip_graph, pie_graph

R = random.Random(82604)
NM = Names(R)


def fs(v):
    return ff(F(v), mixed=True)


def dd(v):
    return format(D(v).normalize(), "f")


def fi(v):
    v = F(v)
    return fr(v.numerator, v.denominator) if v.denominator > 1 else str(v.numerator)


PAIRS = [("사과", "배", "개"), ("남학생", "여학생", "명"), ("빨간 구슬", "파란 구슬", "개"), ("강아지", "고양이", "마리"), ("장미", "튤립", "송이"), ("농구공", "축구공", "개")]


# ---------------------------------------------------------------- 비와 비율
def ratio_write():
    a_, b_, u = R.choice(PAIRS)
    a, b = R.randint(2, 15), R.randint(2, 15)
    if a == b:
        return None
    k = R.choice(["to", "base"])
    if k == "to":
        return mcq("%s %s %s %s 있어요. %s 수에 대한 %s 수의 비는?" % (a_, josa("%d%s" % (a, u), "과/와"), b_, josa("%d%s" % (b, u), "이/가"), b_, a_), "%d : %d" % (a, b),
                   ["%d : %d" % (b, a), "%d : %d" % (a, a + b), "%d : %d" % (b, a + b)],
                   "「△에 대한 □의 비」는 □ : △예요. 기준량 %s 수가 뒤에 와요. <b>%d : %d</b>" % (b_, a, b))
    return mcq("%s %s %s %s 있어요. 전체에 대한 %s 수의 비는?" % (a_, josa("%d%s" % (a, u), "과/와"), b_, josa("%d%s" % (b, u), "이/가"), a_), "%d : %d" % (a, a + b),
               ["%d : %d" % (a + b, a), "%d : %d" % (a, b), "%d : %d" % (b, a + b)], "전체는 %d + %d = %d. <b>%d : %d</b>" % (a, b, a + b, a, a + b))


def ratio_read():
    a, b = R.randint(1, 20), R.randint(2, 20)
    if a == b:
        return None
    k = R.choice(["base", "comp", "say"])
    if k == "base":
        return mcq("비 %d : %d에서 기준량은?" % (a, b), str(b), [str(a), str(a + b), str(abs(a - b)) if abs(a - b) not in (a, b) else str(a * b)],
                   "비 □ : △에서 기호 : 의 오른쪽에 있는 △가 기준량이에요. <b>%d</b>" % b)
    if k == "comp":
        return mcq("비 %d : %d에서 비교하는 양은?" % (a, b), str(a), [str(b), str(a + b), str(abs(a - b)) if abs(a - b) not in (a, b) else str(a * b)],
                   "기호 : 의 왼쪽에 있는 수가 비교하는 양이에요. <b>%d</b>" % a)
    opts = ["%d 대 %d" % (a, b), "%d의 %d에 대한 비" % (a, b), "%d에 대한 %d의 비" % (b, a), "%d와 %d의 비" % (a, b)]
    wrong = ["%d에 대한 %d의 비" % (a, b), "%d의 %d에 대한 비" % (b, a), "%d 대 %d" % (b, a)]
    good = R.choice(opts)
    return mcq("%d : %d를 바르게 읽은 것은?" % (a, b), good, wrong, "%d : %d는 %d 대 %d, %d의 %d에 대한 비, %d에 대한 %d의 비라고 읽어요." % (a, b, a, b, a, b, b, a))


def ratio_val():
    a, b = R.randint(1, 30), R.choice([2, 4, 5, 8, 10, 20, 25, 40, 50])
    if a == b:
        return None
    v = F(a, b)
    k = R.choice(["frac", "dec"])
    if k == "frac":
        return mcq("비 %d : %d를 비율로 나타내면? (분수)" % (a, b), fi(v), [fi(F(b, a)), fi(F(a, a + b)), fi(v + 1) if v < 5 else fi(v - 1)],
                   "(비율) = (비교하는 양) ÷ (기준량) = %d ÷ %d = <b>%s</b>" % (a, b, fi(v)))
    return mcq("비 %d : %d를 비율로 나타내면? (소수)" % (a, b), dd(D(a) / b), [dd(D(b) / a) if (D(b) / a) == (D(b) / a).quantize(D("0.001")) else dd(D(a) / b * 10), dd(D(a) / b * 10), dd(D(a) / (a + b)) if (D(a) / (a + b)) == (D(a) / (a + b)).quantize(D("0.001")) else dd(D(a) / b / 10)],
               "%d ÷ %d = <b>%s</b>" % (a, b, dd(D(a) / b)))


def ratio_story():
    k = R.choice(["speed", "shoot", "map", "density"])
    if k == "speed":
        km, h = R.randint(60, 300), R.choice([2, 3, 4, 5])
        if km % h:
            return None
        return mcq("자동차가 %d km를 %d시간 동안 갔어요. 걸린 시간에 대한 간 거리의 비율은? (1시간에 간 거리)" % (km, h), "%d" % (km // h),
                   [fi(F(h, km)), str(km * h), str(km - h)], "(간 거리) ÷ (걸린 시간) = %d ÷ %d = <b>%d</b>" % (km, h, km // h))
    if k == "shoot":
        n = R.choice([10, 20, 25])
        g = R.randint(1, n - 1)
        who = NM.next()
        return mcq("%s 공을 %d번 던져 %d번 넣었어요. 던진 횟수에 대한 넣은 횟수의 비율을 소수로 나타내면?" % (josa(who, "은/는"), n, g), dd(D(g) / n),
                   [dd(D(n) / g) if (D(n) / g) == (D(n) / g).quantize(D("0.01")) else dd(D(g) / n * 10), dd(D(n - g) / n), dd(D(g) / n * 100)],
                   "%d ÷ %d = <b>%s</b>" % (g, n, dd(D(g) / n)))
    if k == "map":
        cm = R.randint(2, 9)
        s = R.choice([1000, 10000, 50000, 100000])
        real = cm * s // 100
        return mcq("실제 거리에 대한 지도에서 거리의 비율이 %s인 지도에서 %d cm는 실제로 몇 m인가요?" % (fr(1, s), cm), "%s m" % num(real),
                   ["%s m" % num(x) for x in (real * 100, real // 10 if real >= 10 else real * 10 + 1, cm * s)], "%d × %s = %s cm = <b>%s m</b>" % (cm, num(s), num(cm * s), num(real)))
    p = R.randint(2, 9) * 1000
    a = R.randint(2, 5)
    return mcq("넓이가 %d km²인 마을에 %s명이 살아요. 넓이에 대한 인구의 비율은? (1 km²에 사는 사람 수)" % (a, num(p * a)), "%s" % num(p),
               [num(p * a * a), fi(F(a, p * a)), num(p * a - a)], "%s ÷ %d = <b>%s</b>" % (num(p * a), a, num(p)))


# ---------------------------------------------------------------- 백분율
def pct_conv():
    k = R.choice(["f2p", "d2p", "p2d", "p2f"])
    if k == "f2p":
        d = R.choice([2, 4, 5, 10, 20, 25, 50])
        n = R.randint(1, d - 1)
        p = 100 * n // d
        return mcq("비율 %s를 백분율로 나타내면?" % fr(n, d), "%d%%" % p, ["%d%%" % x for x in (n, n * d if n * d != p else p + 5, p // 10 if p >= 10 else p + 10)],
                   "비율에 100을 곱하고 %%를 붙여요. %s × 100 = <b>%d%%</b>" % (fr(n, d), p))
    if k == "d2p":
        v = D(R.randint(1, 99)) / 100
        return mcq("비율 %s를 백분율로 나타내면?" % dd(v), "%s%%" % dd(v * 100), ["%s%%" % dd(v), "%s%%" % dd(v * 10), "%s%%" % dd(v * 1000)],
                   "%s × 100 = <b>%s%%</b>" % (dd(v), dd(v * 100)))
    p = R.randint(1, 99)
    if k == "p2d":
        return mcq("%d%%를 소수로 나타내면?" % p, dd(D(p) / 100), [dd(D(p) / 10), str(p), dd(D(p) / 1000)],
                   "%% 앞의 수를 100으로 나눠요. %d ÷ 100 = <b>%s</b>" % (p, dd(D(p) / 100)))
    return mcq("%d%%를 기약분수로 나타내면?" % p, fi(F(p, 100)), [fr(p, 10) if p < 10 else fi(F(p, 1000)), fi(F(100, p)) if p != 100 else "1", fr(p, 100) if F(p, 100).denominator != 100 else fi(F(p + 1, 100))],
                   "%d%% = %s = <b>%s</b>" % (p, fr(p, 100), fi(F(p, 100))))


def pct_of():
    p = R.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75])
    base = R.choice([200, 400, 500, 800, 1000, 1200, 2000, 4000])
    v = base * p // 100
    if base * p % 100:
        return None
    k = R.choice(["of", "back", "rate"])
    if k == "of":
        return mcq("%s의 %d%%는 얼마인가요?" % (num(base), p), num(v), [num(base * p // 10) if base * p % 10 == 0 else num(v * 10), num(base - v), num(v + p)],
                   "%s × %s = <b>%s</b>" % (num(base), fr(p, 100), num(v)))
    if k == "rate":
        return mcq("%s은 %s의 몇 %%인가요?" % (num(v), num(base)), "%d%%" % p, ["%d%%" % x for x in (100 - p, p * 2 if p * 2 <= 100 else p // 5, p + 10)],
                   "%s ÷ %s × 100 = <b>%d%%</b>" % (num(v), num(base), p))
    return mcq("어떤 수의 %d%%가 %s일 때, 어떤 수는?" % (p, num(v)), num(base), [num(v * p // 100) if v * p % 100 == 0 else num(base // 10), num(base * 2), num(v + 100)],
               "%s ÷ %s = <b>%s</b>" % (num(v), fr(p, 100), num(base)))


def pct_story():
    k = R.choice(["sale", "vote", "salt", "rate", "inc"])
    if k == "sale":
        p = R.choice([10, 20, 25, 30, 40])
        price = R.choice([8000, 12000, 15000, 20000, 24000, 30000])
        cut = price * p // 100
        return mcq("%s원짜리 옷을 %d%% 할인해서 팔아요. 할인된 가격은 얼마인가요?" % (num(price), p), "%s원" % num(price - cut),
                   ["%s원" % num(x) for x in (cut, price - p * 100, price - cut // 10)], "할인 금액 %s × %s = %s원. %s − %s = <b>%s원</b>" % (num(price), fr(p, 100), num(cut), num(price), num(cut), num(price - cut)))
    if k == "vote":
        n = R.choice([20, 25, 40, 50])
        g = R.randint(1, n - 1)
        if (g * 100) % n:
            return None
        p = g * 100 // n
        return mcq("반장 선거에서 %d명 중 %d명이 가 후보를 뽑았어요. 가 후보의 득표율은 몇 %%인가요?" % (n, g), "%d%%" % p, ["%d%%" % x for x in (g, 100 - p, p // 10 if p >= 10 else p + 10)],
                   "%d ÷ %d × 100 = <b>%d%%</b>" % (g, n, p))
    if k == "salt":
        w = R.choice([100, 200, 250, 400, 500])
        s = R.randint(5, 60)
        if s * 100 % (w + s):
            return None
        p = s * 100 // (w + s)
        return mcq("물 %d g에 소금 %d g을 녹였어요. 소금물에 대한 소금의 비율은 몇 %%인가요?" % (w, s), "%d%%" % p,
                   ["%s%%" % dd(D(s) * 100 / w) if (D(s) * 100 / w) == (D(s) * 100 / w).quantize(D("0.1")) else "%d%%" % (p + 2), "%d%%" % s, "%d%%" % (p * 2)],
                   "소금물은 %d + %d = %d g. %d ÷ %d × 100 = <b>%d%%</b>" % (w, s, w + s, s, w + s, p))
    if k == "rate":
        p = R.choice([1, 2, 3, 4, 5])
        m = R.choice([100000, 200000, 500000, 1000000])
        return mcq("%s원을 1년 동안 예금하면 이자율이 %d%%예요. 1년 뒤 받는 이자는 얼마인가요?" % (num(m), p), "%s원" % num(m * p // 100),
                   ["%s원" % num(x) for x in (m * p // 10, m + m * p // 100, m * p // 1000)], "%s × %s = <b>%s원</b>" % (num(m), fr(p, 100), num(m * p // 100)))
    a = R.choice([200, 400, 500, 800])
    p = R.choice([10, 20, 25, 50])
    return mcq("작년에 %d명이던 동아리 회원이 올해 %d%% 늘었어요. 올해 회원은 몇 명인가요?" % (a, p), "%d명" % (a + a * p // 100),
               ["%d명" % x for x in (a * p // 100, a + p, a - a * p // 100)], "늘어난 수 %d × %s = %d명. %d + %d = <b>%d명</b>" % (a, fr(p, 100), a * p // 100, a, a * p // 100, a + a * p // 100))


# ---------------------------------------------------------------- 띠그래프・원그래프
TOPICS = [("좋아하는 계절", ["봄", "여름", "가을", "겨울"]), ("좋아하는 과목", ["수학", "국어", "체육", "음악", "미술"]),
          ("가고 싶은 나라", ["미국", "영국", "프랑스", "일본", "호주"]), ("좋아하는 운동", ["축구", "야구", "농구", "수영"]),
          ("하루 생활", ["잠", "학교", "놀이", "식사", "기타"]), ("좋아하는 간식", ["떡볶이", "과자", "과일", "빵"])]


def pcts(k):
    while True:
        cut = sorted(R.sample(range(1, 20), k - 1))
        parts = [b - a for a, b in zip([0] + cut, cut + [20])]
        ps = [p * 5 for p in parts]
        if len(set(ps)) == k and min(ps) >= 5:
            return sorted(ps, reverse=True)


def gdata():
    title, cats = R.choice(TOPICS)
    ps = pcts(len(cats))
    return title, cats, ps


def graph_q(kind):
    def mk():
        title, cats, ps = gdata()
        pic = strip_graph(title, cats, ps) if kind == "strip" else pie_graph(title, cats, ps)
        k = R.choice(["read", "max", "times", "count", "diff"])
        i = R.randrange(len(cats))
        if k == "read":
            return mcq(pic + "%s의 비율은 몇 %%인가요?" % cats[i], "%d%%" % ps[i], ["%d%%" % x for x in set(ps + [ps[i] + 5]) - {ps[i]}],
                       "그래프에서 %s 부분을 읽어요. <b>%d%%</b>" % (cats[i], ps[i]))
        if k == "max":
            j = ps.index(max(ps))
            return mcq(pic + "가장 많은 비율을 차지하는 항목은?", cats[j], [c for c in cats if c != cats[j]][:3],
                       "가장 넓은 부분을 찾아요. <b>%s</b>" % cats[j])
        if k == "times":
            a, b = R.sample(range(len(cats)), 2)
            if ps[a] % ps[b] or ps[a] == ps[b]:
                return None
            t = ps[a] // ps[b]
            return mcq(pic + "%s의 비율은 %s의 비율의 몇 배인가요?" % (cats[a], cats[b]), "%d배" % t, ["%d배" % x for x in (t + 1, t - 1 if t > 2 else t + 2, ps[a] - ps[b])],
                       "%d ÷ %d = <b>%d배</b>" % (ps[a], ps[b], t))
        if k == "count":
            n = R.choice([200, 300, 400, 500, 600])
            v = n * ps[i] // 100
            if n * ps[i] % 100:
                return None
            return mcq(pic + "조사한 사람이 %d명이라면 %s 고른 사람은 몇 명인가요?" % (n, josa(cats[i], "을/를")), "%d명" % v, ["%d명" % x for x in (ps[i], v * 10, n - v)],
                       "%d × %s = <b>%d명</b>" % (n, fr(ps[i], 100), v))
        a, b = R.sample(range(len(cats)), 2)
        if ps[a] < ps[b]:
            a, b = b, a
        return mcq(pic + "%s %s보다 몇 %% 더 많은가요?" % (josa(cats[a], "은/는"), cats[b]), "%d%%" % (ps[a] - ps[b]), ["%d%%" % x for x in (ps[a] + ps[b], ps[a], ps[b]) if x != ps[a] - ps[b]] + ["%d%%" % (ps[a] - ps[b] + 5)],
                   "%d − %d = <b>%d%%</b>" % (ps[a], ps[b], ps[a] - ps[b]))
    return mk


def graph_make():
    title, cats = R.choice(TOPICS)
    n = R.choice([20, 40, 50, 25])
    ps = pcts(len(cats))
    vals = [n * p // 100 for p in ps]
    if any(n * p % 100 for p in ps):
        return None
    i = R.randrange(len(cats))
    t = table(["항목"] + cats + ["합계"], [["학생 수(명)"] + [str(v) for v in vals] + [str(n)]])
    return mcq(t + "표를 띠그래프로 나타낼 때 %s 전체의 몇 %%인가요?" % josa(cats[i], "은/는"), "%d%%" % ps[i], ["%d%%" % x for x in (vals[i], ps[i] + 5, 100 - ps[i]) if x != ps[i]],
               "%d ÷ %d × 100 = <b>%d%%</b>" % (vals[i], n, ps[i]))


CHOOSE = [("우리 반 학생들이 좋아하는 과목의 비율", "원그래프"), ("하루 동안의 기온 변화", "꺾은선그래프"), ("반별 학생 수 비교", "막대그래프"),
          ("우리나라 땅의 쓰임별 비율", "띠그래프"), ("강낭콩의 키가 자라는 변화", "꺾은선그래프"), ("마을별 쌀 생산량을 그림으로", "그림그래프"),
          ("한 달 용돈의 쓰임새별 비율", "원그래프"), ("나라별 금메달 수 비교", "막대그래프")]


def graph_choose():
    t, a = R.choice(CHOOSE)
    alts = [x for x in ("막대그래프", "꺾은선그래프", "그림그래프", "띠그래프", "원그래프") if x != a and not ({x, a} == {"띠그래프", "원그래프"})]
    return mcq("「%s」를 나타내기에 가장 알맞은 그래프는?" % t, a, R.sample(alts, 3),
               "전체에 대한 비율은 띠그래프・원그래프, 변화는 꺾은선그래프, 크기 비교는 막대그래프가 알맞아요. <b>%s</b>" % a)


# ---------------------------------------------------------------- 비례식
def ratio_eq():
    a, b = R.randint(1, 12), R.randint(1, 12)
    if math.gcd(a, b) > 1 or a == b:
        return None
    k = R.randint(2, 8)
    if R.random() < 0.5:
        return mcq("%d : %d와 비율이 같은 비는?" % (a, b), "%d : %d" % (a * k, b * k), ["%d : %d" % (a + k, b + k), "%d : %d" % (a * k, b), "%d : %d" % (b * k, a * k)],
                   "전항과 후항에 0이 아닌 같은 수를 곱해도 비율은 같아요. <b>%d : %d</b>" % (a * k, b * k))
    return mcq("%d : %d를 가장 간단한 자연수의 비로 나타내면?" % (a * k, b * k), "%d : %d" % (a, b), ["%d : %d" % (b, a), "%d : %d" % (a * k // math.gcd(k, 2) if k % 2 == 0 else a + 1, b * k // 2 if k % 2 == 0 else b + 1), "%d : %d" % (a * k - b * k if a > b else a, b)],
               "전항과 후항을 최대공약수 %d로 나눠요. <b>%d : %d</b>" % (k, a, b))


def ratio_simple():
    k = R.choice(["dec", "frac"])
    a, b = R.randint(1, 9), R.randint(1, 9)
    if math.gcd(a, b) > 1 or a == b:
        return None
    if k == "dec":
        x, y = D(a) / 10, D(b) / 10
        return mcq("%s : %s를 간단한 자연수의 비로 나타내면?" % (dd(x), dd(y)), "%d : %d" % (a, b), ["%d : %d" % (b, a), "%d : %d" % (a * 10, b), "%d : %d" % (a, b * 10)],
                   "전항과 후항에 10을 곱해요. <b>%d : %d</b>" % (a, b))
    d1, d2 = R.randint(2, 6), R.randint(2, 6)
    x, y = F(1, d1), F(1, d2)
    l = d1 * d2 // math.gcd(d1, d2)
    p, q = l // d1, l // d2
    g = math.gcd(p, q)
    p, q = p // g, q // g
    if p == q:
        return None
    return mcq("%s : %s를 간단한 자연수의 비로 나타내면?" % (fr(1, d1), fr(1, d2)), "%d : %d" % (p, q), ["%d : %d" % (d1, d2), "%d : %d" % (q, p), "%d : %d" % (p + 1, q)],
               "두 분모의 최소공배수 %d를 곱해요. <b>%d : %d</b>" % (l, p, q))


def prop_solve():
    a, b = R.randint(2, 12), R.randint(2, 12)
    if a == b:
        return None
    k = R.randint(2, 9)
    pos = R.randrange(4)
    terms = [a, b, a * k, b * k]
    ans = terms[pos]
    shown = [str(t) if i != pos else "□" for i, t in enumerate(terms)]
    e = "외항의 곱과 내항의 곱은 같아요. %d × %d = %d × %d이므로 □ = <b>%d</b>" % (a, b * k, b, a * k, ans)
    return mcq("비례식 %s : %s = %s : %s에서 □에 알맞은 수는?" % tuple(shown), str(ans), [str(ans + k), str(ans * k), str(abs(ans - k)) if ans != k else str(ans + 1)], e)


def prop_terms():
    a, b = R.randint(2, 9), R.randint(2, 9)
    k = R.randint(2, 5)
    c, d = a * k, b * k
    if a == b:
        return None
    w = R.choice(["외항", "내항"])
    ans = "%d, %d" % ((a, d) if w == "외항" else (b, c))
    return mcq("비례식 %d : %d = %d : %d에서 %s은?" % (a, b, c, d, w), ans, ["%d, %d" % ((b, c) if w == "외항" else (a, d)), "%d, %d" % (a, b), "%d, %d" % (c, d)],
               "바깥쪽에 있는 두 항이 외항, 안쪽에 있는 두 항이 내항이에요. <b>%s</b>" % ans)


def prop_story():
    k = R.choice(["recipe", "map", "price", "shadow"])
    if k == "recipe":
        a, b = R.randint(1, 5), R.randint(2, 6)
        if a == b:
            return None
        m = R.randint(2, 6)
        return mcq("밥을 지을 때 쌀과 물의 양의 비는 %d : %d예요. 쌀을 %d컵 넣으면 물은 몇 컵 넣어야 하나요?" % (a, b, a * m), "%d컵" % (b * m),
                   ["%d컵" % x for x in (a * m + b - a, b * a * m, b + m)], "%d : %d = %d : □, %d × □ = %d × %d, □ = <b>%d컵</b>" % (a, b, a * m, a, b, a * m, b * m))
    if k == "price":
        n, p = R.randint(2, 6), R.choice([1200, 1500, 1800, 2400, 3000])
        m = R.randint(3, 12)
        if p % n or m == n:
            return None
        return mcq("연필 %d자루가 %s원이에요. 같은 연필 %d자루는 얼마인가요?" % (n, num(p), m), "%s원" % num(p // n * m),
                   ["%s원" % num(x) for x in (p * m, p + (m - n) * 100, p // n * (m + 1))], "%d : %s = %d : □, □ = <b>%s원</b>" % (n, num(p), m, num(p // n * m)))
    if k == "shadow":
        h, s = R.randint(1, 3), R.randint(1, 4)
        H = R.randint(3, 15)
        if h == s:
            return None
        return mcq("같은 시각에 길이 %d m인 막대의 그림자가 %d m예요. 그림자가 %d m인 나무의 높이는 몇 m인가요?" % (h, s, H * s), "%d m" % (H * h),
                   ["%d m" % x for x in (H * s * s // h if (H * s * s) % h == 0 else H * s + 1, H * s, H * h + h)], "%d : %d = □ : %d, □ = <b>%d m</b>" % (h, s, H * s, H * h))
    s = R.choice([10000, 20000, 50000])
    cm = R.randint(2, 9)
    return mcq("축척이 1 : %s인 지도에서 %d cm는 실제로 몇 km인가요?" % (num(s), cm), "%s km" % dd(D(cm * s) / 100000),
               ["%s km" % dd(D(cm * s) / 10000), "%s km" % dd(D(cm * s) / 1000000), "%s km" % num(cm * s)], "%d × %s = %s cm = <b>%s km</b>" % (cm, num(s), num(cm * s), dd(D(cm * s) / 100000)))


# ---------------------------------------------------------------- 비례배분
def dist_q():
    a, b = R.randint(1, 9), R.randint(1, 9)
    if a == b or math.gcd(a, b) > 1:
        return None
    k = R.randint(2, 30)
    tot = (a + b) * k
    who = R.choice(["앞", "뒤"])
    ans = a * k if who == "앞" else b * k
    return mcq("%d를 %d : %d로 비례배분하면 %s의 수는?" % (tot, a, b, "앞" if who == "앞" else "뒤"), str(ans),
               [str(tot // a) if tot % a == 0 and tot // a != ans else str(ans + k), str((b if who == "앞" else a) * k), str(tot * (a if who == "앞" else b) // (a * b)) if tot * (a if who == "앞" else b) % (a * b) == 0 and tot * (a if who == "앞" else b) // (a * b) != ans else str(ans + 1)],
               "%d × %s = <b>%d</b>" % (tot, fr(a if who == "앞" else b, a + b), ans))


def dist_story():
    who1, who2 = NM.next(), NM.next()
    if who1 == who2:
        return None
    a, b = R.randint(1, 7), R.randint(1, 7)
    if a == b or math.gcd(a, b) > 1:
        return None
    k = R.choice(["candy", "money", "rect"])
    if k == "candy":
        m = R.randint(2, 8)
        tot = (a + b) * m
        return mcq("사탕 %d개를 %s와 %s가 %d : %d로 나누어 가졌어요. %s 몇 개를 가졌나요?" % (tot, who1, who2, a, b, josa(who1, "은/는")), "%d개" % (a * m),
                   ["%d개" % x for x in (b * m, tot // a if tot % a == 0 and tot // a != a * m else a * m + 1, a * m + b)],
                   "%d × %s = <b>%d개</b>" % (tot, fr(a, a + b), a * m))
    if k == "money":
        m = R.choice([1000, 2000, 500])
        tot = (a + b) * m
        return mcq("%s와 %s가 %d : %d로 돈을 내서 %s원짜리 선물을 샀어요. %s 낸 돈은 얼마인가요?" % (who1, who2, a, b, num(tot), josa(who2, "이/가")), "%s원" % num(b * m),
                   ["%s원" % num(x) for x in (a * m, tot // b if tot % b == 0 and tot // b != b * m else b * m + 100, tot - a)],
                   "%s × %s = <b>%s원</b>" % (num(tot), fr(b, a + b), num(b * m)))
    m = R.randint(2, 6)
    per = 2 * (a + b) * m
    return mcq("둘레가 %d cm인 직사각형의 가로와 세로의 비가 %d : %d예요. 가로는 몇 cm인가요?" % (per, a, b), "%d cm" % (a * m),
               ["%d cm" % x for x in (per * a // (a + b) if per * a % (a + b) == 0 else a * m + 2, b * m, a * m * 2)],
               "가로 + 세로 = %d ÷ 2 = %d cm. %d × %s = <b>%d cm</b>" % (per, per // 2, per // 2, fr(a, a + b), a * m))


def build(which):
    G = "grade-6"
    if which == "ratio":
        return unit(G, "ratios-and-rates", 4, "[6수02-02] [6수02-03]",
                    "두 양의 크기를 비교하는 상황을 통해 비의 개념을 이해하고, 두 양의 관계를 비로 나타낼 수 있다. 비율을 이해하고, 비율을 분수, 소수, 백분율로 나타낼 수 있다.",
                    "비와 비율", "비와 비율",
                    "초등 6학년 1학기 비와 비율 학습지: 비로 나타내기, 비 읽기, 기준량과 비교하는 양, 비율을 분수와 소수로, 속력・득표율・축척・인구 밀도 문장제까지 100문제와 정답.",
                    "비율 = 비교하는 양 ÷ 기준량", "□ : △에서 △가 기준량",
                    ["두 수를 나눗셈으로 비교하기 위해 기호 : 을 사용하여 나타낸 것을 <b>비</b>라고 해요. 3 : 5는 「3 대 5」라고 읽어요.",
                     "비 3 : 5에서 기호 : 의 오른쪽 5는 <b>기준량</b>, 왼쪽 3은 <b>비교하는 양</b>이에요.",
                     "기준량에 대한 비교하는 양의 크기를 <b>비율</b>이라고 해요. (비율) = (비교하는 양) ÷ (기준량)"],
                    [("남학생 12명, 여학생 15명일 때 여학생 수에 대한 남학생 수의 비율", ["비는 12 : 15", "12 ÷ 15 = 0.8"], "<span class='fr'><span class='fn'>4</span><span class='fd'>5</span></span> (0.8)")],
                    [("「여학생에 대한 남학생의 비」를 여학생 : 남학생으로 쓴다", "「~에 대한」 앞이 기준량으로 뒤에 와요."),
                     ("비 3 : 5와 5 : 3을 같다고 생각한다", "순서가 바뀌면 다른 비예요."),
                     ("비율을 기준량 ÷ 비교하는 양으로 구한다", "비교하는 양 ÷ 기준량이에요.")],
                    [("비와 비율은 언제 배우나요?", "초등 6학년 1학기 「비와 비율」 단원에서 배워요."),
                     ("뺄셈으로 비교하는 것과 무엇이 다른가요?", "뺄셈은 차이를, 비는 몇 배인지(상대적인 크기)를 비교해요.")],
                    [("비로 나타내기", [(ratio_write, 20)]),
                     ("비 읽기와 기준량", [(ratio_read, 20)]),
                     ("비율을 분수와 소수로", [(ratio_val, 20)]),
                     ("섞어서 연습", [(ratio_write, 7), (ratio_read, 6), (ratio_val, 7)]),
                     ("생활 속 비율", [(ratio_story, 20)])], 82604)
    if which == "pct":
        return unit(G, "percentages", 5, "[6수02-03]",
                    "비율을 이해하고, 비율을 분수, 소수, 백분율로 나타낼 수 있다.",
                    "백분율", "백분율",
                    "초등 6학년 1학기 백분율 학습지: 비율을 백분율로, 백분율을 소수와 분수로, 어떤 양의 몇 %, 할인 가격・득표율・소금물・이자 문장제까지 100문제와 정답.",
                    "비율 × 100 = 백분율(%)", "백분율은 기준량을 100으로 볼 때의 비율",
                    ["기준량을 100으로 할 때의 비율을 <b>백분율</b>이라고 하고 기호 %를 써요.",
                     "비율에 100을 곱하면 백분율이 돼요. 0.35 → 35%, <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> → 75%",
                     "백분율을 소수로 바꿀 때는 100으로 나눠요. 8% → 0.08",
                     "어떤 양의 □%는 (어떤 양) × <span class='fr'><span class='fn'>□</span><span class='fd'>100</span></span>예요."],
                    [("20000원짜리 물건을 15% 할인한 가격", ["할인 금액 20000 × 15/100 = 3000원", "20000 − 3000 = 17000"], "17000원")],
                    [("0.35를 3.5%로 쓴다", "100을 곱해요. 35%"),
                     ("할인된 가격을 할인 금액으로 답한다", "원래 가격에서 할인 금액을 빼요."),
                     ("소금물의 진하기를 물의 양으로 나눈다", "소금물 전체(물 + 소금)로 나눠요.")],
                    [("백분율은 어디에 쓰이나요?", "할인율, 득표율, 이자율, 타율 등 생활 곳곳에서 써요."),
                     ("100%보다 큰 백분율도 있나요?", "네. 비교하는 양이 기준량보다 크면 100%보다 커요.")],
                    [("비율을 백분율로", [(pct_conv, 20)]),
                     ("어떤 양의 몇 %", [(pct_of, 20)]),
                     ("백분율 바꾸기", [(pct_conv, 10), (pct_of, 10)]),
                     ("할인과 득표율", [(pct_story, 20)]),
                     ("섞어서 연습", [(pct_story, 10), (pct_of, 10)])], 82605)
    if which == "graph":
        return unit(G, "strip-and-circle-graphs", 6, "[6수04-02] [6수04-03]",
                    "자료를 수집하여 띠그래프나 원그래프로 나타내고 해석할 수 있다. 탐구 문제를 설정하고, 그에 맞는 자료를 수집, 정리하여 적절한 그래프로 나타내고 해석할 수 있다.",
                    "띠그래프와 원그래프", "띠그래프와 원그래프",
                    "초등 6학년 1학기 여러 가지 그래프 학습지: 띠그래프와 원그래프 읽기, 비율의 비교, 전체 수에서 항목의 수 구하기, 표를 비율로 나타내기, 알맞은 그래프 고르기까지 100문제와 정답.",
                    "전체에 대한 부분의 비율을 한눈에", "띠그래프는 띠, 원그래프는 원을 나눠요.",
                    ["전체에 대한 각 부분의 비율을 띠 모양에 나타낸 그래프를 <b>띠그래프</b>, 원 모양에 나타낸 그래프를 <b>원그래프</b>라고 해요.",
                     "각 항목의 백분율을 구해서 합계가 100%가 되도록 나타내요.",
                     "비율의 크기를 비교하거나 전체 수를 알면 항목의 수를 구할 수 있어요.",
                     "비율은 띠・원그래프, 변화는 꺾은선그래프, 크기 비교는 막대그래프가 알맞아요."],
                    [("400명 중 25%가 고른 항목의 사람 수", ["400 × 25/100 = 100"], "100명")],
                    [("백분율을 사람 수로 읽는다", "그래프의 %는 비율이에요. 전체 수를 곱해서 사람 수를 구해요."),
                     ("백분율의 합이 100%가 아닌데 그대로 그린다", "합계가 100%인지 확인해요."),
                     ("가장 많은 항목을 그래프에서 먼저 나온 것으로 고른다", "차지하는 넓이(길이)를 비교해요.")],
                    [("띠그래프와 원그래프는 언제 배우나요?", "초등 6학년 1학기 「여러 가지 그래프」 단원에서 배워요."),
                     ("두 그래프는 무엇이 다른가요?", "나타내는 모양만 다르고, 둘 다 전체에 대한 부분의 비율을 나타내요.")],
                    [("띠그래프 읽기", [(graph_q("strip"), 20)]),
                     ("원그래프 읽기", [(graph_q("pie"), 20)]),
                     ("표를 비율로", [(graph_make, 20)]),
                     ("알맞은 그래프", [(graph_choose, 8), (graph_q("pie"), 12)]),
                     ("섞어서 연습", [(graph_q("strip"), 10), (graph_make, 10)])], 82606)
    if which == "prop":
        return unit(G, "ratios-and-proportions", 11, "[6수02-04]",
                    "비례식을 알고, 그 성질을 이해하며, 이를 활용하여 간단한 비례식을 풀 수 있다.",
                    "비의 성질과 비례식", "비례식",
                    "초등 6학년 2학기 비례식 학습지: 비의 성질, 간단한 자연수의 비, 외항과 내항, 비례식의 성질로 □ 구하기, 요리・가격・그림자・축척 문장제까지 100문제와 정답.",
                    "외항의 곱 = 내항의 곱", "전항과 후항에 같은 수를 곱해도 비율은 같아요.",
                    ["비의 전항과 후항에 0이 아닌 같은 수를 곱하거나 나누어도 비율은 같아요.",
                     "비율이 같은 두 비를 기호 = 로 나타낸 식을 <b>비례식</b>이라고 해요. 2 : 3 = 4 : 6",
                     "비례식에서 바깥쪽 두 항을 <b>외항</b>, 안쪽 두 항을 <b>내항</b>이라고 해요. 외항의 곱과 내항의 곱은 같아요."],
                    [("3 : 4 = □ : 20", ["외항의 곱 = 내항의 곱", "3 × 20 = 4 × □", "□ = 15"], "15")],
                    [("전항에만 곱한다", "전항과 후항에 같은 수를 곱해요."),
                     ("외항과 내항을 바꿔 말한다", "바깥쪽이 외항, 안쪽이 내항이에요."),
                     ("소수의 비를 간단히 할 때 한쪽에만 10을 곱한다", "두 항 모두에 10을 곱해요.")],
                    [("비례식은 어디에 쓰나요?", "요리의 재료 양, 지도의 축척, 물건의 가격 등을 구할 때 써요."),
                     ("분수의 비는 어떻게 간단히 하나요?", "두 분모의 최소공배수를 곱해 자연수의 비로 바꿔요.")],
                    [("비의 성질", [(ratio_eq, 20)]),
                     ("간단한 자연수의 비", [(ratio_simple, 20)]),
                     ("외항과 내항", [(prop_terms, 8), (prop_solve, 12)]),
                     ("비례식 풀기", [(prop_solve, 20)]),
                     ("문장제", [(prop_story, 20)])], 82611)
    return unit(G, "proportional-distribution", 12, "[6수02-05]",
                "비례배분을 알고, 주어진 양을 비례배분 할 수 있다.",
                "비례배분", "비례배분",
                "초등 6학년 2학기 비례배분 학습지: 주어진 수를 비로 나누기, 사탕・돈・직사각형의 가로와 세로를 비례배분하는 문장제까지 100문제와 정답.",
                "전체 × (내 몫의 비 ÷ 비의 합)", "비의 합을 분모로 하는 분수를 곱해요.",
                ["전체를 주어진 비로 나누는 것을 <b>비례배분</b>이라고 해요.",
                 "전체를 □ : △로 나누면 앞의 양은 (전체) × <span class='fr'><span class='fn'>□</span><span class='fd'>□ + △</span></span>, 뒤의 양은 (전체) × <span class='fr'><span class='fn'>△</span><span class='fd'>□ + △</span></span>예요.",
                 "두 양을 더하면 전체가 되는지 확인해요."],
                [("35를 3 : 4로 비례배분", ["35 × 3/7 = 15", "35 × 4/7 = 20"], "15, 20")],
                [("전체를 앞의 수로 나눈다 (35 ÷ 3)", "비의 합 7을 분모로 해요."),
                 ("앞과 뒤의 몫을 바꾼다", "비의 순서대로 나눠 가져요."),
                 ("둘레를 그대로 비례배분한다", "가로 + 세로는 둘레의 반이에요.")],
                [("비례배분은 언제 배우나요?", "초등 6학년 2학기 「비례식과 비례배분」 단원에서 배워요."),
                 ("세 사람에게 나눌 수도 있나요?", "네. 2 : 3 : 5처럼 세 수의 비로도 나눌 수 있어요. 비의 합 10을 분모로 해요.")],
                [("비례배분하기", [(dist_q, 20)]),
                 ("앞과 뒤의 몫", [(dist_q, 20)]),
                 ("사탕과 돈 나누기", [(dist_story, 20)]),
                 ("섞어서 연습", [(dist_q, 10), (dist_story, 10)]),
                 ("문장제", [(dist_story, 20)])], 82612)
