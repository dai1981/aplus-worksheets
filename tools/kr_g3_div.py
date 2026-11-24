# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：나눗셈（2022 개정 [4수01-06]）の 2 単元（3-2）
  rem  : (몇십) ÷ (몇)、(두 자리 수) ÷ (한 자리 수)、몫과 나머지
  three: (세 자리 수) ÷ (한 자리 수)
나머지は「29 ÷ 4 = 7 … 1」と書く。誤答は「나머지가 나누는 수보다 크다」「몫과 나머지を逆にする」「몫의 0を落とす（312 ÷ 3 = 14）」から作る。
"""
import random
from kr_common import mcq, num, unit, Names, josa

R = random.Random(82312)
NM = Names(R)


def qr(q, r):
    return "%d … %d" % (q, r) if r else str(q)


def tens_div():
    d = R.randint(2, 9)
    n = R.randint(2, 9) * 10
    if n % d:
        return None
    q = n // d
    if q % 10 == 0:
        e = "%d ÷ %d = %d이니까 %d ÷ %d = <b>%d</b>예요." % (n // 10, d, q // 10, n, d, q)
    else:
        e = "십의 자리부터 나누고 남은 수는 일의 자리로 내려요. %d ÷ %d = <b>%d</b> (확인: %d × %d = %d)" % (n, d, q, d, q, n)
    return mcq("%d ÷ %d =" % (n, d), str(q), [str(x) for x in (q + 10, q - 1, q + 1, n - d, q * 10) if x != q and x > 0 and x < 200], e)


def no_rem(regroup):
    def mk():
        d = R.randint(2, 9)
        q = R.randint(11, 49)
        n = d * q
        if n >= 100:
            return None
        t = n // 10
        if regroup != (t % d != 0):
            return None
        return mcq("%d ÷ %d =" % (n, d), str(q), [str(x) for x in (q + 1, q - 1, q + 10, t // d * 10 + (n % 10) // d) if x != q and x > 0],
                   "십의 자리부터 나누어요. %s %d ÷ %d = <b>%d</b> (확인: %d × %d = %d)"
                   % ("십의 자리에서 남은 수는 일의 자리로 내려서 함께 나누어요." if regroup else "", n, d, q, d, q, n))
    return mk


def with_rem(two=True):
    def mk():
        d = R.randint(2, 9)
        q = R.randint(2, 9) if not two else R.randint(10, 32)
        r = R.randint(1, d - 1) if d > 1 else 0
        n = d * q + r
        if n >= 100 or n < 10:
            return None
        ans = qr(q, r)
        w = [qr(q - 1, r + d), qr(r, q) if r != q else qr(q + 1, r), qr(q + 1, r), qr(q, r + 1) if r + 1 < d else qr(q, r - 1)]
        return mcq("%d ÷ %d =" % (n, d), ans, [x for x in w if x != ans],
                   "%d × %d = %d이고 %d − %d = %d예요. 나머지 %d는 나누는 수 %d보다 작아야 해요. <b>%s</b>" % (d, q, d * q, n, d * q, r, r, d, ans))
    return mk


def rem_check():
    d = R.randint(3, 9)
    q = R.randint(2, 15)
    r = R.randint(1, d - 1)
    n = d * q + r
    k = R.choice(["verify", "max", "which"])
    if k == "verify":
        return mcq("%d ÷ %d = %d … %d를 바르게 확인한 식은?" % (n, d, q, r), "%d × %d + %d = %d" % (d, q, r, n),
                   ["%d × %d − %d = %d" % (d, q, r, d * q - r), "%d × %d + %d = %d" % (d, r, q, d * r + q), "%d + %d × %d = %d" % (q, r, d, q + r * d)],
                   "나누는 수 × 몫 + 나머지 = 나누어지는 수예요. %d × %d + %d = <b>%d</b>" % (d, q, r, n))
    if k == "max":
        return mcq("어떤 수를 %d로 나누었을 때 나올 수 있는 나머지 중 가장 큰 수는?" % d, str(d - 1), [str(d), str(d + 1), str(d - 2) if d > 2 else "0"],
                   "나머지는 나누는 수보다 작아야 해요. %d보다 작은 수 중 가장 큰 수는 <b>%d</b>예요." % (d, d - 1))
    m = d * q + R.randint(0, d - 1)
    return mcq("□ ÷ %d = %d … %d에서 □에 알맞은 수는?" % (d, q, r), str(n), [str(x) for x in (d * q, d * q - r, n + d, q * r + d) if x != n and x > 0],
               "□ = %d × %d + %d = <b>%d</b>" % (d, q, r, n))


def three(kind):
    def mk():
        d = R.randint(2, 9)
        if kind == "hund":
            q = R.randint(1, 4) * 100 + R.choice([0, R.randint(1, 9) * 10])
            r = 0
        elif kind == "zero":
            q = R.randint(1, 3) * 100 + R.randint(1, 9)        # 몫の十の位が 0
            r = R.randint(0, d - 1)
        elif kind == "norem":
            q = R.randint(21, 199)
            r = 0
        else:
            q = R.randint(21, 199)
            r = R.randint(1, d - 1)
        n = d * q + r
        if not 100 <= n <= 999:
            return None
        ans = qr(q, r)
        w = [qr(q + 10, r), qr(q - 1, r + d) if q > 1 else qr(q + 1, r), qr(q + 1, r), qr(q, (r + 1) % d) if d > 2 else qr(q + 2, r)]
        if kind == "zero":
            qs = str(q)
            w.insert(0, qr(int(qs[0] + qs[2]), r))
        return mcq("%d ÷ %d =" % (n, d), ans, [x for x in w if x != ans],
                   "백의 자리부터 차례로 나누어요. 나눌 수 없는 자리는 몫에 0을 써요. <b>%s</b> (확인: %d × %d%s = %d)" % (ans, d, q, " + %d" % r if r else "", n))
    return mk


def story(big=False):
    def mk():
        d = R.randint(3, 9)
        q = R.randint(3, 9) if not big else R.randint(12, 120)
        r = R.randint(1, d - 1)
        n = d * q + r
        if (big and not 100 <= n <= 999) or (not big and n >= 100):
            return None
        who = NM.next()
        k = R.choice(["left", "boxes", "need", "each"])
        if k == "left":
            t = "%s 구슬 %d개를 친구 %d명에게 똑같이 나누어 주려고 해요. 한 명에게 몇 개씩 줄 수 있고, 몇 개가 남나요?" % (josa(who, "은/는"), n, d)
            ans = "%d개씩, %d개 남아요" % (q, r)
            w = ["%d개씩, %d개 남아요" % (q + 1, r), "%d개씩, %d개 남아요" % (r, q), "%d개씩, %d개 남아요" % (q - 1, r + d)]
            e = "%d ÷ %d = %d … %d예요." % (n, d, q, r)
        elif k == "boxes":
            t = "사과 %d개를 한 상자에 %d개씩 담으려고 해요. 사과를 모두 담으려면 상자는 적어도 몇 개 필요한가요?" % (n, d)
            ans = "%d개" % (q + 1)
            w = ["%d개" % q, "%d개" % r, "%d개" % (q + 2)]
            e = "%d ÷ %d = %d … %d예요. 남은 사과 %d개도 담아야 하니까 상자는 %d + 1 = %d개 필요해요." % (n, d, q, r, r, q, q + 1)
        elif k == "need":
            t = "학생 %d명이 한 대에 %d명씩 탈 수 있는 보트를 타려고 해요. 모두 타려면 보트는 적어도 몇 대 필요한가요?" % (n, d)
            ans = "%d대" % (q + 1)
            w = ["%d대" % q, "%d대" % r, "%d대" % (q + 2)]
            e = "%d ÷ %d = %d … %d예요. 남은 %d명도 타야 하니까 %d대가 필요해요." % (n, d, q, r, r, q + 1)
        else:
            t = "끈 %d cm를 %d cm씩 자르려고 해요. %d cm짜리 끈은 몇 개가 되고, 몇 cm가 남나요?" % (n, d, d)
            ans = "%d개, %d cm 남아요" % (q, r)
            w = ["%d개, %d cm 남아요" % (q + 1, r), "%d개, %d cm 남아요" % (r, q), "%d개, %d cm 남아요" % (q, r + d)]
            e = "%d ÷ %d = %d … %d예요." % (n, d, q, r)
        return mcq(t, ans, w, e + " <b>%s</b>" % ans)
    return mk


def build(which):
    if which == "rem":
        return unit("grade-3", "division-with-remainders", 12, "[4수01-06]",
                    "나누는 수가 한 자리 수인 나눗셈의 계산 원리를 이해하고 그 계산을 할 수 있으며, 나눗셈에서 몫과 나머지의 의미를 안다.",
                    "(두 자리 수) ÷ (한 자리 수)와 나머지", "몫과 나머지",
                    "초등 3학년 2학기 나눗셈 학습지: (몇십)÷(몇), 나머지가 없는 (두 자리 수)÷(한 자리 수), 몫과 나머지, 계산 확인, 문장제까지 100문제와 정답.",
                    "나머지는 나누는 수보다 작아요", "확인: 나누는 수 × 몫 + 나머지",
                    ["(몇십) ÷ (몇)은 (몇) ÷ (몇)의 몫에 0을 붙여요. 60 ÷ 3 = 20",
                     "(두 자리 수) ÷ (한 자리 수)는 <b>십의 자리부터</b> 나누고, 남은 수는 일의 자리로 내려서 다시 나누어요.",
                     "29 ÷ 4 = 7 … 1에서 7은 <b>몫</b>, 1은 <b>나머지</b>예요. 나머지가 0이면 나누어떨어진다고 해요.",
                     "나머지는 언제나 <b>나누는 수보다 작아야</b> 해요. 확인: 4 × 7 + 1 = 29"],
                    [("57 ÷ 4 =", ["십의 자리: 5 ÷ 4 = 1 … 1", "일의 자리로 내려서 17 ÷ 4 = 4 … 1"], "14 … 1"),
                     ("72 ÷ 3 =", ["7 ÷ 3 = 2 … 1, 12 ÷ 3 = 4"], "24")],
                    [("나머지가 나누는 수보다 크다", "나머지가 나누는 수보다 크거나 같으면 몫을 1 크게 해요."),
                     ("몫과 나머지를 바꾸어 쓴다", "몇 번 들어가는지가 몫, 남은 수가 나머지예요."),
                     ("남은 것도 담아야 하는데 몫만 답한다", "「적어도 몇 개 필요한가요?」는 몫 + 1이에요.")],
                    [("나머지가 있는 나눗셈은 언제 배우나요?", "초등 3학년 2학기 「나눗셈」 단원에서 배워요. 1학기에는 나머지가 없는 나눗셈의 뜻을 배웠어요."),
                     ("계산이 맞는지 어떻게 확인하나요?", "나누는 수 × 몫 + 나머지가 나누어지는 수와 같은지 보세요.")],
                    [("(몇십) ÷ (몇)", [(tens_div, 13), (no_rem(False), 7)]),
                     ("나머지가 없는 나눗셈", [(no_rem(False), 6), (no_rem(True), 14)]),
                     ("몫과 나머지 (한 자리 몫)", [(with_rem(False), 20)]),
                     ("몫과 나머지 (두 자리 몫)", [(with_rem(True), 14), (rem_check, 6)]),
                     ("문장제", [(story(False), 16), (rem_check, 4)])], 82312)
    return unit("grade-3", "divide-three-digit-by-one-digit", 13, "[4수01-06]",
                "나누는 수가 한 자리 수인 나눗셈의 계산 원리를 이해하고 그 계산을 할 수 있으며, 나눗셈에서 몫과 나머지의 의미를 안다.",
                "(세 자리 수) ÷ (한 자리 수)", "(세 자리 수) ÷ (한 자리 수)",
                "초등 3학년 2학기 나눗셈 학습지: (몇백몇십)÷(몇), 나머지가 없는, 있는 (세 자리 수)÷(한 자리 수), 몫에 0이 있는 나눗셈, 문장제까지 100문제와 정답.",
                "백의 자리부터 차례로 나누어요", "나눌 수 없는 자리의 몫은 0이에요.",
                ["(세 자리 수) ÷ (한 자리 수)는 <b>백의 자리부터</b> 나누어요. 남은 수는 다음 자리로 내려요.",
                 "백의 자리 숫자가 나누는 수보다 작으면, 백의 자리와 십의 자리를 함께 나누어요. 몫은 두 자리 수가 돼요.",
                 "나눌 수 없는 자리가 있으면 그 자리의 몫에 <b>0</b>을 써요. 621 ÷ 3 = 207",
                 "확인: 나누는 수 × 몫 + 나머지 = 나누어지는 수"],
                [("624 ÷ 3 =", ["6 ÷ 3 = 2", "2 ÷ 3은 나눌 수 없으므로 몫 0, 24 ÷ 3 = 8"], "208"),
                 ("259 ÷ 4 =", ["25 ÷ 4 = 6 … 1", "19 ÷ 4 = 4 … 3"], "64 … 3")],
                [("몫의 0을 빠뜨린다", "624 ÷ 3에서 십의 자리 몫 0을 써야 208이 돼요."),
                 ("나머지가 나누는 수보다 크다", "나머지는 나누는 수보다 작아야 해요."),
                 ("백의 자리를 나눌 수 없는데 몫의 백의 자리에 0을 쓴다", "259 ÷ 4의 몫은 064가 아니라 64예요.")],
                [("(세 자리 수) ÷ (한 자리 수)에서 몫이 몇 자리 수인지 어떻게 알 수 있나요?", "백의 자리 숫자가 나누는 수보다 크거나 같으면 몫은 세 자리 수, 작으면 두 자리 수예요."),
                 ("어림으로 확인하려면?", "259 ÷ 4는 240 ÷ 4 = 60과 280 ÷ 4 = 70 사이여야 해요.")],
                [("(몇백몇십) ÷ (몇)", [(three("hund"), 20)]),
                 ("나머지가 없는 나눗셈", [(three("norem"), 20)]),
                 ("나머지가 있는 나눗셈", [(three("rem"), 20)]),
                 ("몫에 0이 있는 나눗셈", [(three("zero"), 20)]),
                 ("문장제", [(story(True), 20)])], 82313)
