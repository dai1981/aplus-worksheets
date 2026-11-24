# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：들이와 무게（2022 개정 [4수03-17]〜[4수03-23]）の 2 単元（3-2）
  cap: 1 L와 1 mL、L ↔ mL、어림、들이의 덧셈과 뺄셈
  wt : 1 kg과 1 g、1 t、kg ↔ g、저울 읽기、어림、무게의 덧셈과 뺄셈
誤答は「1 L = 100 mL」「1 kg = 100 g」「1 t = 100 kg」「받아올림을 10/100 で하는」から作る。
"""
import random
from kr_common import mcq, num, unit, Names, josa
from kr_pics import beaker, scale

R = random.Random(82316)
NM = Names(R)


def lml(ml):
    l, m = divmod(ml, 1000)
    if l and m:
        return "%d L %d mL" % (l, m)
    return "%d L" % l if l else "%d mL" % m


def kgg(g):
    k, r = divmod(g, 1000)
    if k and r:
        return "%d kg %d g" % (k, r)
    return "%d kg" % k if k else "%d g" % r


def conv(fmt, big, small, b_word):
    def mk():
        a, m = R.randint(1, 9), R.randint(10, 990)
        if m % 10:
            return None
        t = a * 1000 + m
        if R.random() < 0.5:
            return mcq("%d %s %d %s는 몇 %s인가요?" % (a, big, m, small, small), "%s %s" % (num(t), small),
                       ["%s %s" % (num(x), small) for x in (a * 100 + m, a + m, a * 10000 + m, a * 1000 + m * 10 if m < 100 else t + 1000)],
                       "1 %s = 1000 %s예요. %d %s = %s %s이니까 %s + %d = <b>%s %s</b>" % (big, small, a, big, num(a * 1000), small, num(a * 1000), m, num(t), small))
        return mcq("%s %s는 몇 %s 몇 %s인가요?" % (num(t), small, big, small), fmt(t), [fmt(t + 1000), "%d %s %d %s" % (t // 100, big, t % 100, small), fmt(t - 1000) if t > 2000 else fmt(t + 2000), "%d %s %d %s" % (a, big, m // 10, small)],
                   "1000 %s = 1 %s예요. <b>%s</b>" % (small, big, fmt(t)))
    return mk


def read_beaker():
    cap = R.choice([500, 1000, 2000])
    step = {500: 50, 1000: 100, 2000: 200}[cap]
    ml = R.randrange(step, cap, step)
    return mcq(beaker(ml, cap, step) + "그릇에 든 물의 양은 몇 mL인가요?", "%d mL" % ml,
               ["%d mL" % x for x in (ml + step, ml - step, ml + 2 * step, ml - 2 * step, ml // step * 10) if x != ml and x > 0 and x <= cap],
               "작은 눈금 한 칸은 %d mL예요. 물의 높이와 맞는 눈금을 읽어요. <b>%d mL</b>" % (step, ml))


def read_scale():
    cap = R.choice([1000, 2000, 4000])
    step = {1000: 50, 2000: 100, 4000: 200}[cap]
    every = {1000: 200, 2000: 500, 4000: 1000}[cap]
    g = R.randrange(step, cap, step)
    if cap > 1000:
        ans = kgg(g)
        w = [kgg(g + step), kgg(g - step), kgg(g + every)]
        q = "저울의 눈금이 가리키는 무게는 얼마인가요? (큰 숫자는 kg이에요)" if cap == 4000 else "저울의 눈금이 가리키는 무게는 얼마인가요?"
    else:
        ans = "%d g" % g
        w = ["%d g" % x for x in (g + step, g - step, g + 100) if x > 0]
        q = "저울의 눈금이 가리키는 무게는 몇 g인가요?"
    f = scale(g, cap, step, every)
    return mcq(f + q, ans, [x for x in w if x != ans],
               "작은 눈금 한 칸은 %d g이에요. 바늘이 가리키는 눈금을 읽어요. <b>%s</b>" % (step, ans))


EST_CAP = [("우유갑(작은 것)", "200 mL", ["200 L", "2 mL", "20 L"]), ("물병", "500 mL", ["500 L", "5 mL", "50 L"]),
           ("욕조", "200 L", ["200 mL", "2 L", "20 mL"]), ("숟가락", "15 mL", ["15 L", "150 L", "1500 mL"]),
           ("주전자", "2 L", ["2 mL", "200 L", "20 mL"]), ("컵", "250 mL", ["250 L", "25 L", "2 mL"]),
           ("어항", "30 L", ["30 mL", "3 mL", "300 mL"]), ("요구르트병", "65 mL", ["65 L", "650 L", "6 L"]),
           ("양동이", "10 L", ["10 mL", "100 mL", "1 mL"]), ("음료수 캔", "350 mL", ["350 L", "35 L", "3 mL"])]
EST_WT = [("사과 한 개", "300 g", ["300 kg", "3 kg", "3 t"]), ("3학년 학생", "30 kg", ["30 g", "30 t", "300 g"]),
          ("자동차", "1 t", ["1 kg", "1 g", "100 g"]), ("공책 한 권", "100 g", ["100 kg", "10 kg", "1 t"]),
          ("수박 한 통", "5 kg", ["5 g", "5 t", "50 g"]), ("코끼리", "5 t", ["5 kg", "50 kg", "5 g"]),
          ("동전 한 개", "5 g", ["5 kg", "50 kg", "5 t"]), ("쌀 한 포대", "20 kg", ["20 g", "20 t", "200 g"]),
          ("연필 한 자루", "5 g", ["5 kg", "500 g", "5 t"]), ("트럭에 실은 모래", "8 t", ["8 kg", "8 g", "80 g"])]


def est(table, word):
    def mk():
        t, a, w = R.choice(table)
        return mcq("%s의 %s로 가장 알맞은 것은?" % (t, word), a, w,
                   ("1 L는 큰 우유갑 하나, 1 mL는 아주 적은 양이에요. " if word == "들이" else "1 kg은 큰 우유갑 하나의 무게쯤, 1 t은 1000 kg이에요. ") + "%s는 <b>%s</b>쯤이에요." % (t, a))
    return mk


def calc(fmt, small, kind):
    def mk():
        a, b = R.randint(1100, 6900), R.randint(300, 3900)
        if a % 10 or b % 10 or a % 1000 == 0 or b % 1000 == 0:
            a, b = a // 10 * 10, b // 10 * 10
        if a % 1000 == 0 or b % 1000 == 0:
            return None
        if kind == "+":
            r = a + b
            carry = (a % 1000 + b % 1000) >= 1000
        else:
            if b >= a:
                return None
            r = a - b
            carry = a % 1000 < b % 1000
        if r % 1000 == 0 or not carry and R.random() < 0.6:
            return None
        op = "+" if kind == "+" else "−"
        w = [fmt(r + 1000), fmt(r - 1000) if r > 1000 else fmt(r + 2000), fmt(r + 100), fmt(r - 10) if r % 1000 > 10 else fmt(r + 10)]
        return mcq("%s %s %s =" % (fmt(a), op, fmt(b)), fmt(r), [x for x in w if x != fmt(r)],
                   "큰 단위는 큰 단위끼리, %s는 %s끼리 계산해요. %s끼리 1000이 넘거나 모자라면 1000 %s = 1로 받아올림, 받아내림해요. <b>%s</b>" % (small, small, small, small, fmt(r)))
    return mk


def story_cap():
    who = NM.next()
    a, b = R.randint(1100, 2900) // 10 * 10, R.randint(200, 900) // 10 * 10
    k = R.choice(["drink", "pour", "two"])
    if k == "drink":
        t = "주스 %s 중에서 %s 마셨어요. 남은 주스는 얼마인가요?" % (lml(a), josa(lml(b), "을/를"))
        r = a - b
    elif k == "pour":
        t = "물통에 물이 %s 들어 있었는데 %s 더 부었어요. 물통에 든 물은 모두 얼마인가요?" % (lml(a), josa(lml(b), "을/를"))
        r = a + b
    else:
        t = "%s 우유를 어제 %s, 오늘 %s 마셨어요. 이틀 동안 마신 우유는 모두 몇 mL인가요?" % (josa(who, "은/는"), lml(b), lml(b + R.randint(1, 20) * 10))
        import re as _re
        nums = [int(x) for x in _re.findall(r"(\d+) mL", t)]
        r = sum(nums)
        return mcq(t, "%d mL" % r, ["%d mL" % x for x in (r + 100, r - 100, r + 1000, abs(nums[0] - nums[1]) or r + 10)],
                   "%d + %d = <b>%d mL</b>" % (nums[0], nums[1], r))
    return mcq(t, lml(r), [lml(r + 1000), lml(r + 100), lml(abs(r - 100)), lml(a + b if k == "drink" else abs(a - b))],
               "L는 L끼리, mL는 mL끼리 계산해요. <b>%s</b>" % lml(r))


def story_wt():
    who = NM.next()
    k = R.choice(["bag", "box", "t"])
    if k == "t":
        t1 = R.randint(2, 9)
        kg = R.randint(1, 9) * 100
        t = "트럭 한 대에 짐을 %d t 실을 수 있어요. 지금 %s kg을 실었다면, 더 실을 수 있는 짐은 몇 kg인가요?" % (t1, num(t1 * 1000 - kg))
        r = kg
        return mcq(t, "%s kg" % num(r), ["%s kg" % num(x) for x in (r + 100, t1 * 1000 - kg, r * 10, r + 1000) if x != r],
                   "1 t = 1000 kg이니까 %d t = %s kg이에요. %s − %s = <b>%s kg</b>" % (t1, num(t1 * 1000), num(t1 * 1000), num(t1 * 1000 - kg), num(r)))
    a, b = R.randint(1100, 4900) // 10 * 10, R.randint(300, 2900) // 10 * 10
    if a % 1000 == 0 or b % 1000 == 0:
        return None
    if k == "bag":
        t = "%s 책가방의 무게는 %s이고, 필통을 넣으니 %s 늘어났어요. 필통을 넣은 책가방의 무게는 얼마인가요?" % (who + "의", kgg(a), kgg(b))
        r = a + b
    else:
        t = "물건이 든 상자의 무게는 %s이에요. 빈 상자의 무게가 %s이면 물건의 무게는 얼마인가요?" % (kgg(a + b), kgg(b))
        r = a
    return mcq(t, kgg(r), [kgg(r + 1000), kgg(r + 100), kgg(abs(r - 100)), kgg(a + 2 * b if k == "box" else abs(a - b))],
               "kg은 kg끼리, g은 g끼리 계산해요. 1 kg = 1000 g이에요. <b>%s</b>" % kgg(r))


def ton():
    t = R.randint(1, 9)
    if R.random() < 0.5:
        return mcq("%d t은 몇 kg인가요?" % t, "%s kg" % num(t * 1000), ["%s kg" % num(x) for x in (t * 100, t * 10, t * 10000)],
                   "1 t = 1000 kg이에요. %d t = <b>%s kg</b>" % (t, num(t * 1000)))
    return mcq("%s kg은 몇 t인가요?" % num(t * 1000), "%d t" % t, ["%d t" % x for x in (t * 10, t * 100, t + 1)],
               "1000 kg = 1 t이에요. <b>%d t</b>" % t)


def cmp(fmt, small):
    def mk():
        a = R.randint(1100, 8900) // 10 * 10
        b = a + R.choice([-90, -10, 20, 300, -300])
        if a % 1000 == 0:
            return None
        A, B = fmt(a), "%s %s" % (num(b), small)
        big = A if a > b else B
        return mcq("더 %s 것은? %s, %s" % ("많은" if small == "mL" else "무거운", A, B), big, [B if big == A else A, "같아요", "알 수 없어요"],
                   "단위를 같게 바꾸어 비교해요. %s = %s %s이에요. <b>%s</b>" % (A, num(a), small, big))
    return mk


def build(which):
    if which == "cap":
        return unit("grade-3", "capacity-liters-and-milliliters", 18, "[4수03-17] [4수03-18] [4수03-19]",
                    "들이 단위 1L와 1mL를 알고, 이를 이용하여 들이를 측정하고 어림하며 수학의 유용성을 인식할 수 있다. 1L와 1mL의 관계를 이해하고, 들이를 '몇 L 몇 mL'와 '몇 mL'로 표현할 수 있다. 실생활 문제 상황과 연결하여 들이의 덧셈과 뺄셈을 할 수 있다.",
                    "들이: 1 L와 1 mL", "들이 (L와 mL)",
                    "초등 3학년 2학기 들이 학습지: 1 L와 1 mL, 눈금 읽기, L와 mL 바꾸기, 들이 어림하기, 들이의 덧셈과 뺄셈, 문장제까지 100문제와 정답.",
                    "1 L = 1000 mL", "L는 L끼리, mL는 mL끼리 계산해요.",
                    ["그릇에 담을 수 있는 양을 <b>들이</b>라고 해요. 들이의 단위에는 <b>L(리터)</b>와 <b>mL(밀리리터)</b>가 있어요.",
                     "<b>1 L = 1000 mL</b>예요. 1 L 300 mL = 1300 mL",
                     "들이를 더하고 뺄 때는 L는 L끼리, mL는 mL끼리 계산해요. mL끼리 1000이 넘으면 1 L로 받아올림해요."],
                    [("2 L 700 mL + 1 L 500 mL =", ["mL끼리: 700 + 500 = 1200 mL = 1 L 200 mL", "L끼리: 2 + 1 + 1 = 4"], "4 L 200 mL"),
                     ("3 L 200 mL − 1 L 600 mL =", ["200에서 600을 뺄 수 없어요. 1 L = 1000 mL를 받아내림", "1200 − 600 = 600, 2 − 1 = 1"], "1 L 600 mL")],
                    [("1 L = 100 mL라고 생각한다", "1 L는 1000 mL예요."),
                     ("2 L 50 mL를 250 mL라고 한다", "2 L = 2000 mL이니까 2050 mL예요."),
                     ("mL끼리 더해 1000이 넘었는데 그대로 쓴다", "1000 mL = 1 L로 받아올림해요.")],
                    [("들이는 언제 배우나요?", "초등 3학년 2학기 「들이와 무게」 단원에서 L와 mL를 배워요."),
                     ("들이를 어림하는 방법은?", "1 L 우유갑이나 200 mL 우유갑을 떠올려 몇 개쯤 들어갈지 생각해 보세요.")],
                    [("눈금 읽기", [(read_beaker, 20)]),
                     ("L와 mL 바꾸기", [(conv(lml, "L", "mL", "들이"), 14), (cmp(lml, "mL"), 6)]),
                     ("들이 어림하기", [(est(EST_CAP, "들이"), 10), (cmp(lml, "mL"), 10)]),
                     ("들이의 덧셈과 뺄셈", [(calc(lml, "mL", "+"), 10), (calc(lml, "mL", "−"), 10)]),
                     ("문장제", [(story_cap, 20)])], 82318)
    return unit("grade-3", "weight-kilograms-and-grams", 19, "[4수03-20] [4수03-21] [4수03-22] [4수03-23]",
                "실생활에서 무게를 나타낼 때 사용하는 단위 1g과 1kg을 알고, 이를 이용하여 무게를 측정하고 어림하며 수학의 유용성을 인식할 수 있다. 1kg과 1g의 관계를 이해하고, 무게를 '몇 kg 몇 g'과 '몇 g'으로 표현할 수 있다. 실생활에서 무게를 나타낼 때 사용하는 단위 1t을 알고, 1t과 1kg의 관계를 이해한다. 실생활 문제 상황과 연결하여 무게의 덧셈과 뺄셈을 할 수 있다.",
                "무게: 1 kg, 1 g, 1 t", "무게 (kg과 g)",
                "초등 3학년 2학기 무게 학습지: 1 kg과 1 g, 1 t, 저울 눈금 읽기, kg과 g 바꾸기, 무게 어림하기, 무게의 덧셈과 뺄셈, 문장제까지 100문제와 정답.",
                "1 kg = 1000 g, 1 t = 1000 kg", "kg은 kg끼리, g은 g끼리 계산해요.",
                ["무게의 단위에는 <b>kg(킬로그램)</b>, <b>g(그램)</b>, <b>t(톤)</b>이 있어요.",
                 "<b>1 kg = 1000 g</b>, <b>1 t = 1000 kg</b>이에요. 1 kg 200 g = 1200 g",
                 "저울은 작은 눈금 한 칸이 몇 g인지 먼저 확인하고 읽어요.",
                 "무게를 더하고 뺄 때는 kg은 kg끼리, g은 g끼리 계산해요. g끼리 1000이 넘으면 1 kg으로 받아올림해요."],
                [("3 kg 600 g + 1 kg 700 g =", ["g끼리: 600 + 700 = 1300 g = 1 kg 300 g", "kg끼리: 3 + 1 + 1 = 5"], "5 kg 300 g"),
                 ("2 t은 몇 kg인가요?", ["1 t = 1000 kg"], "2000 kg")],
                [("1 kg = 100 g이라고 생각한다", "1 kg은 1000 g이에요."),
                 ("저울의 작은 눈금 한 칸을 1 g으로 읽는다", "큰 눈금 사이가 몇 칸으로 나뉘었는지 먼저 세요."),
                 ("1 t = 100 kg이라고 생각한다", "1 t은 1000 kg이에요.")],
                [("무게는 언제 배우나요?", "초등 3학년 2학기 「들이와 무게」 단원에서 kg, g, t을 배워요."),
                 ("1 kg은 어느 정도인가요?", "1 L 우유갑 하나의 무게가 약 1 kg이에요. 사과 3개쯤이에요.")],
                [("저울 읽기", [(read_scale, 20)]),
                 ("kg과 g 바꾸기", [(conv(kgg, "kg", "g", "무게"), 14), (cmp(kgg, "g"), 6)]),
                 ("무게 어림하기와 1 t", [(est(EST_WT, "무게"), 10), (ton, 10)]),
                 ("무게의 덧셈과 뺄셈", [(calc(kgg, "g", "+"), 10), (calc(kgg, "g", "−"), 10)]),
                 ("문장제", [(story_wt, 20)])], 82319)
