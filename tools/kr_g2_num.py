# -*- coding: utf-8 -*-
"""
대한민국 초등 2학년 수학：세 자리 수・네 자리 수（2022 개정 [2수01-02] [2수01-03]）
  three: 세 자리 수   2-1
  four : 네 자리 수   2-2
誤答は「0인 자리를 빠뜨린다（오백육 → 56）」「읽은 대로 쓴다（오백육 → 5006）」「자리의 숫자와 자리의 값을 헷갈린다（472의 7 → 7）」
「뛰어 세기에서 다른 자리를 바꾼다」「높은 자리부터 비교하지 않는다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa, read_num, num
from kr_low import blocks, money, cards, near

R = random.Random(82201)
NM = Names(R)
G = "grade-2"
PLACE = {1000: "천", 100: "백", 10: "십", 1: "일"}


def S(x):
    return str(x)


def digits_place(n):
    out = []
    for p in (1000, 100, 10, 1):
        if n >= p or p == 1:
            out.append((p, n // p % 10))
    return out


# ------------------------------------------------------------------ 백・천
def hundred(big=100):
    F100 = [("99보다 1 큰 수는 무엇일까요?", "100", ["98", "101", "990"], "99 다음 수는 <b>100</b>이에요."),
            ("90보다 10 큰 수는 무엇일까요?", "100", ["91", "190", "80"], "90에서 10을 더 세면 <b>100</b>이에요."),
            ("10이 10개인 수는 무엇일까요?", "100", ["20", "1010", "110"], "10이 10개이면 <b>100</b>이에요."),
            ("100을 바르게 읽은 것은 무엇일까요?", "백", ["십", "일백영", "천"], "100은 <b>백</b>이라고 읽어요."),
            ("100은 80보다 몇 큰 수일까요?", "20", ["10", "2", "180"], "80, 90, 100으로 10씩 2번이에요. <b>20</b>")]
    F1000 = [("999보다 1 큰 수는 무엇일까요?", "1000", ["998", "1001", "9990"], "999 다음 수는 <b>1000</b>이에요."),
             ("900보다 100 큰 수는 무엇일까요?", "1000", ["901", "910", "1900"], "900에서 100을 더 세면 <b>1000</b>이에요."),
             ("100이 10개인 수는 무엇일까요?", "1000", ["110", "10000", "200"], "100이 10개이면 <b>1000</b>이에요."),
             ("1000을 바르게 읽은 것은 무엇일까요?", "천", ["백", "일천영", "만"], "1000은 <b>천</b>이라고 읽어요."),
             ("990보다 10 큰 수는 무엇일까요?", "1000", ["991", "1090", "980"], "990에서 10을 더 세면 <b>1000</b>이에요."),
             ("1000은 700보다 몇 큰 수일까요?", "300", ["30", "3", "1700"], "700, 800, 900, 1000으로 100씩 3번이에요. <b>300</b>")]
    pool = (F100 if big == 100 else F1000)[:]

    def mk():
        if not pool:
            return None
        return mcq(*pool.pop(0))
    return mk


def many(p):
    """몇백・몇천"""
    def mk():
        k = R.randint(2, 9)
        n = k * p
        how = R.choice(["read", "count", "write", "money"])
        nm_ = PLACE[p]
        if how == "read":
            return mcq("<b>%s</b>를 바르게 읽은 것은 무엇일까요?" % num(n), read_num(n),
                       [read_num(n + p) if k < 9 else read_num(n - p), read_num(k * p // 10), "%s영영" % read_num(k) + ("영" if p == 1000 else "")],
                       "%s이 %d개이면 <b>%s</b>이에요." % (num(p), k, read_num(n)))
        if how == "write":
            return mcq("'%s'을 수로 쓰면 무엇일까요?" % read_num(n), num(n), [num(x) for x in (k * p // 10, k * p * 10, n + p, n - p) if 0 < x],
                       "%s이 %d개 → <b>%s</b>" % (num(p), k, num(n)))
        if how == "money":
            coin = 100 if p == 100 else 1000
            return mcq("%d원짜리가 %d%s 있으면 모두 얼마일까요?" % (coin, k, "개" if coin == 100 else "장"), "%s원" % num(n),
                       ["%s원" % num(x) for x in (k * coin // 10, k * coin * 10, n + coin)], "%d원이 %d%s이면 <b>%s원</b>이에요." % (coin, k, "개" if coin == 100 else "장", num(n)))
        return mcq("%s이 <b>%d개</b>인 수는 무엇일까요?" % (num(p), k), num(n), [num(x) for x in (k * p // 10, k * p * 10, n + p, k)],
                   "%s이 %d개이면 <b>%s</b>이에요." % (num(p), k, num(n)))
    return mk


# ------------------------------------------------------------------ 수 쓰기・읽기
def make_n(nd, zeros=None):
    while True:
        n = R.randint(10 ** (nd - 1), 10 ** nd - 1)
        z = str(n).count("0")
        if zeros is None or (zeros and z >= 1) or (not zeros and z == 0):
            return n


def wrong_write(n):
    """오백육 → 5006(읽은 대로), 56(0 빠뜨림)"""
    w = []
    w.append(int("".join(str(d) for _, d in digits_place(n) if d)))       # 0 を落とす
    lit = ""
    for p, d in digits_place(n):
        if d:
            lit += str(d) + ("0" * (len(str(p)) - 1))
    w.append(int(lit) if lit else n)
    w.append(int(str(n)[::-1].lstrip("0") or "1"))
    return [x for x in w if x != n]


def read_write(nd):
    def mk():
        n = make_n(nd, R.random() < 0.5)
        if R.random() < 0.5:
            return mcq("%s 수로 쓰면 무엇일까요?" % josa("'%s'" % read_num(n), "을/를"),
                       num(n), [str(x) for x in wrong_write(n) + near(n, 1, 9999, (10, -10, 100, 1))],
                       "자리마다 숫자를 써요. 없는 자리에는 0을 써요. <b>%s</b>" % num(n))
        bad = [read_num(x) for x in near(n, 1, 9999, (10, 100, -10, 1, -1))]
        if "0" in str(n):
            bad.insert(0, read_num(n).replace(" ", ""))
        swp = int(str(n)[0] + str(n)[2] + str(n)[1] + str(n)[3:]) if len(str(n)) >= 3 else None
        if swp and swp != n and str(swp)[0] != "0":
            bad.insert(0, read_num(swp))
        return mcq("<b>%s</b>를 바르게 읽은 것은 무엇일까요?" % num(n), read_num(n), [b for b in bad if b != read_num(n)],
                   "%s는 <b>%s</b>라고 읽어요. 0인 자리는 읽지 않아요." % (num(n), read_num(n)))
    return mk


def model_q(nd):
    def mk():
        th = R.randint(1, 4) if nd == 4 else 0
        h, t, o = R.randint(0 if nd == 4 else 1, 9 if nd == 3 else 5), R.randint(0, 9), R.randint(0, 9)
        if nd == 3 and h > 5:
            h = R.randint(1, 5)
        n = th * 1000 + h * 100 + t * 10 + o
        w = [th * 1000 + o * 100 + t * 10 + h, n + 10, n + 100, n - 10, n + 1]
        w.append(int("".join(str(d) for d in (th, h, t, o) if d)))
        return mcq("수 모형이 나타내는 수는 무엇일까요?%s" % blocks(th, h, t, o), num(n), [num(x) for x in w if 0 < x != n],
                   "%s백 모형 %d개, 십 모형 %d개, 일 모형 %d개이므로 <b>%s</b>이에요." % ("천 모형 %d개, " % th if th else "", h, t, o, num(n)))
    return mk


def money_q(nd):
    def mk():
        if nd == 3:
            h, t = R.randint(1, 5), R.randint(0, 6)
            vals = [100] * h + [10] * t
            n = 100 * h + 10 * t
        else:
            th, h, t = R.randint(1, 4), R.randint(0, 5), R.randint(0, 5)
            vals = [1000] * th + [100] * h + [10] * t
            n = 1000 * th + 100 * h + 10 * t
        if len(vals) > 12:
            return None
        return mcq("모두 얼마일까요?%s" % money(vals), "%s원" % num(n), ["%s원" % num(x) for x in near(n, 10, None, (10, -10, 100, -100, 1000)) if x != n],
                   "같은 돈끼리 묶어서 세어요. <b>%s원</b>" % num(n))
    return mk


# ------------------------------------------------------------------ 자릿값
def place_value(nd):
    def mk():
        n = make_n(nd, False)
        ps = digits_place(n)
        p, d = R.choice(ps[:-1] if R.random() < 0.8 else ps)
        how = R.choice(["value", "digit", "which"])
        if how == "value":
            return mcq("<b>%s</b>에서 숫자 %d이 나타내는 값은 얼마일까요?" % (num(n), d), num(d * p),
                       [num(d * q) for q, _ in ps if q != p] + [str(d)], "%d은 %s의 자리 숫자이므로 <b>%s</b>을 나타내요." % (d, PLACE[p], num(d * p)))
        if how == "digit":
            return mcq("<b>%s</b>에서 %s의 자리 숫자는 무엇일까요?" % (num(n), PLACE[p]), str(d), [str(dd) for q, dd in ps if q != p] + [num(d * p)],
                       "%s의 각 자리: %s. %s의 자리 숫자는 <b>%d</b>이에요." % (num(n), ", ".join("%s %d" % (PLACE[q], dd) for q, dd in ps), PLACE[p], d))
        tgt = R.randint(1, 9)
        q_ = R.choice([q for q, _ in ps if q > 1]) if nd > 1 else 10
        cands = set()
        while len(cands) < 4:
            m = make_n(nd, False)
            cands.add(m)
        cands = list(cands)
        good = [m for m in cands if m // q_ % 10 == tgt]
        if len(good) != 1:
            return None
        return mcq("%s의 자리 숫자가 <b>%d</b>인 수는 무엇일까요?" % (PLACE[q_], tgt), num(good[0]), [num(m) for m in cands if m != good[0]],
                   "각 수의 %s의 자리를 봐요. <b>%s</b>" % (PLACE[q_], num(good[0])))
    return mk


def decompose(nd):
    def mk():
        n = make_n(nd, R.random() < 0.3)
        parts = [d * p for p, d in digits_place(n) if d]
        ok = " + ".join(num(x) for x in parts)
        bad = []
        ds = [d for _, d in digits_place(n)]
        bad.append(" + ".join(str(d) for d in ds if d))
        sh = [num(x * 10) if i == len(parts) - 1 else num(x) for i, x in enumerate(parts)]
        bad.append(" + ".join(sh))
        if len(parts) >= 2:
            bad.append(" + ".join(num(x // 10) if i == 0 else num(x) for i, x in enumerate(parts)))
        return mcq("<b>%s</b>를 각 자리의 값의 합으로 바르게 나타낸 것은 무엇일까요?" % num(n), ok, bad + [ok.replace(" + ", " + 0", 1)],
                   "%s = <b>%s</b>" % (num(n), ok))
    return mk


# ------------------------------------------------------------------ 뛰어 세기
def skip(nd):
    steps = (1, 10, 100) if nd == 3 else (1, 10, 100, 1000)

    def mk():
        st = R.choice(steps)
        top = 1000 if nd == 3 else 10000
        a = R.randint(10 ** (nd - 1), top - 1 - 5 * st)
        down = R.random() < 0.3
        sq = [a + st * i for i in range(5)]
        if down:
            sq = sq[::-1]
        p = R.randint(2, 4)
        ans = sq[p]
        shown = [num(x) if i != p else "?" for i, x in enumerate(sq)]
        w = [x for x in (ans + 1, ans - 1, ans + 10, ans - 10, ans + 100, ans - 100, ans + 1000) if x != ans and x > 0 and abs(x - ans) != st]
        return mcq("%d씩 %s 뛰어 세었어요. ?에 알맞은 수는 무엇일까요?%s" % (st, "거꾸로" if down else "", cards(shown, 70 if nd == 3 else 80)), num(ans),
                   [num(x) for x in w],
                   "%d씩 뛰어 세면 %s의 자리 숫자가 1씩 %s져요. <b>%s</b>" % (st, PLACE[st], "작아" if down else "커", num(ans)))
    return mk


def skip_more(nd):
    def mk():
        st = R.choice((10, 100) if nd == 3 else (10, 100, 1000))
        top = 1000 if nd == 3 else 10000
        n = R.randint(10 ** (nd - 1), top - 1 - st)
        up = R.random() < 0.5
        if not up and n - st < 10 ** (nd - 1) // 1:
            return None
        a = n + st if up else n - st
        return mcq("<b>%s</b>보다 %s %s 수는 무엇일까요?" % (num(n), num(st), "큰" if up else "작은"), num(a),
                   [num(x) for x in (n - st if up else n + st, n + (st // 10 if st > 1 else 1) * (1 if up else -1), a + st if up else a - st, n + 1) if x > 0 and x != a],
                   "%s의 자리 숫자가 1 %s져요. <b>%s</b>" % (PLACE[st], "커" if up else "작아", num(a)))
    return mk


# ------------------------------------------------------------------ 크기 비교
def compare(nd):
    def mk():
        a = make_n(nd)
        k = R.choice(range(nd))
        s = list(str(a))
        if k == 0:
            pass
        d = int(s[k])
        nd_ = R.choice([x for x in range(10) if x != d and not (k == 0 and x == 0)])
        s[k] = str(nd_)
        b = int("".join(s))
        if R.random() < 0.4:                 # 아래 자리를 크게
            s2 = list(str(b))
            for i in range(k + 1, nd):
                s2[i] = str(R.randint(0, 9))
            b = int("".join(s2))
        if a == b:
            return None
        lt = a < b
        ok = "%s < %s" % (num(a), num(b)) if lt else "%s > %s" % (num(a), num(b))
        bad = ["%s > %s" % (num(a), num(b)) if lt else "%s < %s" % (num(a), num(b)), "%s = %s" % (num(a), num(b)),
               "%s %s %s" % (num(b), "<" if lt else ">", num(a))]
        place = ["천", "백", "십", "일"][4 - nd + [i for i in range(nd) if str(a)[i] != str(b)[i]][0]]
        return mcq("두 수의 크기를 바르게 비교한 것은 무엇일까요?<br><b>%s</b>, <b>%s</b>" % (num(a), num(b)), ok, bad,
                   "높은 자리부터 비교해요. %s의 자리에서 크기가 달라요. <b>%s</b>" % (place, ok))
    return mk


def biggest(nd):
    def mk():
        base = make_n(nd)
        xs = {base}
        while len(xs) < 4:
            s = list(str(base))
            i = R.randrange(1, nd)
            s[i] = str(R.randint(0, 9))
            xs.add(int("".join(s)))
        xs = list(xs)
        big = R.random() < 0.6
        a = max(xs) if big else min(xs)
        return mcq("%s 수는 무엇일까요?%s" % ("가장 큰" if big else "가장 작은", cards([num(x) for x in xs], 70 if nd == 3 else 82)), num(a),
                   [num(x) for x in xs if x != a], "높은 자리부터 차례로 비교해요. <b>%s</b>" % num(a))
    return mk


def card_make(nd):
    from itertools import permutations

    def mk():
        ds = R.sample(range(0, 10), nd)
        big = R.random() < 0.5
        perms = sorted({int("".join(map(str, p))) for p in permutations(ds) if p[0] != 0}, reverse=big)
        a = perms[0]
        w = perms[1:3] + [perms[-1]]
        if not big and 0 in ds:
            w.insert(0, int("".join(map(str, sorted(ds)[1:]))))         # 0 を落とした数
        return mcq("수 카드 %d장을 한 번씩 써서 만들 수 있는 %s 자리 수 중 가장 %s 수는 무엇일까요?%s" % (nd, "세" if nd == 3 else "네", "큰" if big else "작은", cards(ds)),
                   num(a), [num(x) for x in w if x != a],
                   ("큰 숫자부터 높은 자리에 놓아요." if big else "0은 맨 앞에 올 수 없어요. 0이 아닌 가장 작은 숫자를 맨 앞에 놓고, 나머지는 작은 숫자부터 놓아요." if 0 in ds else "작은 숫자부터 높은 자리에 놓아요.") + " <b>%s</b>" % num(a))
    return mk


def story(nd):
    TH = [("구슬", "개"), ("색종이", "장"), ("스티커", "장"), ("사탕", "개"), ("딱지", "장")]

    def mk():
        t, c = R.choice(TH)
        n1, n2 = NM.next(), NM.next()
        if n1 == n2:
            return None
        a, b = make_n(nd), make_n(nd)
        if a == b:
            return None
        more = R.random() < 0.5
        ans = n1 if (a > b) == more else n2
        return mcq("%s %s %s%s, %s %s%s 모았어요. 누가 더 %s 모았을까요?" % (josa(n1, "은/는"), t, num(a), c, josa(n2, "은/는"), num(b), c, "많이" if more else "적게"),
                   ans, [n2 if ans == n1 else n1, "두 사람이 같아요", "알 수 없어요"],
                   "%s %s를 비교하면 %s %s. <b>%s</b>" % (num(a), num(b), num(max(a, b)), "더 커요", ans))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "three":
        return unit(G, "three-digit-numbers", 1, "[2수01-02] [2수01-03]",
                    "일, 십, 백, 천의 자릿값과 위치적 기수법을 이해하고, 네 자리 이하의 수를 읽고 쓸 수 있다. 네 자리 이하의 수의 범위에서 수의 계열을 이해하고, 수의 크기를 비교할 수 있다.",
                    "세 자리 수: 자릿값·뛰어 세기·크기 비교", "세 자리 수",
                    "초등 2학년 1학기 세 자리 수 학습지: 백과 몇백, 수 모형과 돈으로 세 자리 수 알기, 읽고 쓰기, 자릿값, 뛰어 세기, 크기 비교까지 100문제와 정답.",
                    "347 = 300 + 40 + 7", "백의 자리, 십의 자리, 일의 자리의 숫자가 나타내는 값을 알아요.",
                    ["10이 10개이면 <b>100</b>(백)이에요. 100이 3개이면 300(삼백)이에요.",
                     "100이 3개, 10이 4개, 1이 7개이면 <b>347</b>이에요. 삼백사십칠이라고 읽어요.",
                     "347에서 3은 300, 4는 40, 7은 7을 나타내요. 숫자가 같아도 자리가 다르면 나타내는 값이 달라요.",
                     "두 수의 크기는 백의 자리부터 비교하고, 같으면 십의 자리, 일의 자리 순서로 비교해요."],
                    [("오백육을 수로 쓰기", ["백의 자리 5, 십의 자리 0, 일의 자리 6"], "506"),
                     ("358과 361의 크기 비교", ["백의 자리가 3으로 같아요.", "십의 자리: 5 < 6"], "358 < 361")],
                    [("오백육을 5006이나 56으로 쓴다", "없는 자리에는 0을 써요: 506"),
                     ("472에서 7이 나타내는 값을 7이라고 한다", "7은 십의 자리 숫자라서 70이에요."),
                     ("298과 312를 일의 자리부터 비교한다", "백의 자리부터 비교해요: 298 < 312")],
                    [("세 자리 수는 언제 배우나요?", "초등 2학년 1학기 「세 자리 수」 단원에서 배워요."),
                     ("수 모형이 없으면 어떻게 하나요?", "100원, 10원 동전으로 세어 보면 자릿값을 쉽게 익힐 수 있어요.")],
                    [("백과 몇백", [(hundred(100), 5), (many(100), 15)]),
                     ("세 자리 수 쓰고 읽기", [(model_q(3), 8), (money_q(3), 4), (read_write(3), 8)]),
                     ("자릿값", [(place_value(3), 14), (decompose(3), 6)]),
                     ("뛰어 세기", [(skip(3), 14), (skip_more(3), 6)]),
                     ("크기 비교", [(compare(3), 8), (biggest(3), 5), (card_make(3), 4), (story(3), 3)])], 82201)
    if which == "four":
        return unit(G, "four-digit-numbers", 11, "[2수01-02] [2수01-03]",
                    "일, 십, 백, 천의 자릿값과 위치적 기수법을 이해하고, 네 자리 이하의 수를 읽고 쓸 수 있다. 네 자리 이하의 수의 범위에서 수의 계열을 이해하고, 수의 크기를 비교할 수 있다.",
                    "네 자리 수: 천·자릿값·뛰어 세기·크기 비교", "네 자리 수",
                    "초등 2학년 2학기 네 자리 수 학습지: 천과 몇천, 네 자리 수 읽고 쓰기, 자릿값, 1000씩·100씩·10씩 뛰어 세기, 수의 크기 비교, 수 카드로 수 만들기까지 100문제와 정답.",
                    "3507 = 3000 + 500 + 7", "천의 자리부터 차례로 읽고 비교해요.",
                    ["100이 10개이면 <b>1000</b>(천)이에요. 1000이 4개이면 4000(사천)이에요.",
                     "1000이 3개, 100이 5개, 10이 0개, 1이 7개이면 <b>3507</b>이에요. 삼천오백칠이라고 읽어요.",
                     "1000씩 뛰어 세면 천의 자리 숫자가, 100씩 뛰어 세면 백의 자리 숫자가 1씩 커져요.",
                     "두 수의 크기는 천의 자리부터 차례로 비교해요."],
                    [("이천삼십오를 수로 쓰기", ["천 2, 백 0, 십 3, 일 5"], "2035"),
                     ("4296과 4310의 크기 비교", ["천의 자리 같음", "백의 자리: 2 < 3"], "4296 < 4310")],
                    [("이천삼십오를 200035로 쓴다", "자리마다 숫자 하나: 2035"),
                     ("6824에서 8이 나타내는 값을 8이라고 한다", "8은 백의 자리 숫자라서 800이에요."),
                     ("가장 작은 네 자리 수를 만들 때 0을 맨 앞에 놓는다", "0은 맨 앞에 올 수 없어요.")],
                    [("네 자리 수는 언제 배우나요?", "초등 2학년 2학기 「네 자리 수」 단원에서 배워요."),
                     ("만(10000)은 언제 배우나요?", "4학년 1학기 「큰 수」에서 배워요.")],
                    [("천과 몇천", [(hundred(1000), 6), (many(1000), 14)]),
                     ("네 자리 수 쓰고 읽기", [(model_q(4), 6), (money_q(4), 6), (read_write(4), 8)]),
                     ("자릿값", [(place_value(4), 14), (decompose(4), 6)]),
                     ("뛰어 세기", [(skip(4), 14), (skip_more(4), 6)]),
                     ("크기 비교", [(compare(4), 8), (biggest(4), 5), (card_make(4), 4), (story(4), 3)])], 82211)
    raise ValueError(which)
