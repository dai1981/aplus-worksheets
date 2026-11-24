# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：세 자리 수의 덧셈과 뺄셈（2022 개정 [4수01-03]）
  python3 tools/gen_kr_math_g3_add_and_subtract_three_digit_numbers.py
誤答は「받아올림을 잊는다」「큰 수에서 작은 수를 뺀다（받아내림をしない）」「받아내림한 1을 빼지 않는다」から作る。
"""
import random
from kr_common import mcq, num, unit, Names, josa

R = random.Random(82301)
NM = Names(R)


def no_carry_add(a, b):
    s, p = 0, 1
    while a or b:
        s += ((a % 10 + b % 10) % 10) * p
        a //= 10; b //= 10; p *= 10
    return s


def no_borrow_sub(a, b):
    s, p = 0, 1
    while a or b:
        s += abs(a % 10 - b % 10) * p
        a //= 10; b //= 10; p *= 10
    return s


def carries(a, b):
    c = n = 0
    while a or b:
        c = 1 if a % 10 + b % 10 + c >= 10 else 0
        n += c
        a //= 10; b //= 10
    return n


def borrows(a, b):
    c = n = 0
    while a or b:
        d = a % 10 - c - b % 10
        c = 1 if d < 0 else 0
        n += c
        a //= 10; b //= 10
    return n


def add(need, lo=100, hi=899):
    def mk():
        a, b = R.randint(lo, hi), R.randint(100, 899)
        if a + b > 1998 or carries(a, b) != need:
            return None
        s = a + b
        w = [no_carry_add(a, b), s - 10, s + 10, s - 100, s + 100]
        return mcq("%d + %d =" % (a, b), num(s), [num(x) for x in w if x != s and x > 0],
                   "일의 자리부터 더해요. 같은 자리의 합이 10이거나 10보다 크면 바로 윗자리로 1을 받아올림해요. %d + %d = <b>%d</b>" % (a, b, s))
    return mk


def sub(need, zero=False):
    def mk():
        if zero:
            a = R.randint(2, 9) * 100 + R.choice([0, R.randint(1, 9)])
            b = R.randint(101, a - 1)
        else:
            a = R.randint(200, 999)
            b = R.randint(100, a - 1)
        if borrows(a, b) != need or (zero and a % 100 >= 10):
            return None
        d = a - b
        w = [no_borrow_sub(a, b), d + 10, d - 10, d + 100, d - 100]
        return mcq("%d − %d =" % (a, b), num(d), [num(x) for x in w if x != d and x > 0],
                   "일의 자리부터 빼요. 빼는 수가 더 크면 바로 윗자리에서 10을 받아내림해요. %d − %d = <b>%d</b> (확인: %d + %d = %d)" % (a, b, d, d, b, a))
    return mk


def missing():
    a, b = R.randint(120, 600), R.randint(110, 380)
    s = a + b
    if carries(a, b) == 0:
        return None
    if R.random() < 0.5:
        return mcq("□ + %d = %d 일 때, □에 알맞은 수는?" % (b, s), num(a), [num(x) for x in (s + b, a + 10, a - 10, no_borrow_sub(s, b))],
                   "□ = %d − %d = <b>%d</b>예요. 덧셈과 뺄셈의 관계를 이용해요." % (s, b, a))
    return mcq("%d − □ = %d 일 때, □에 알맞은 수는?" % (s, a), num(b), [num(x) for x in (s + a, b + 10, b - 10, no_borrow_sub(s, a))],
               "□ = %d − %d = <b>%d</b>예요." % (s, a, b))


def story_add():
    who = NM.next()
    a, b = R.randint(150, 600), R.randint(120, 390)
    if carries(a, b) == 0:
        return None
    s = a + b
    k = R.choice([("줄넘기를 어제 %d번, 오늘 %d번 했어요. 이틀 동안 모두 몇 번 했나요?", "번"),
                  ("책을 지난주에 %d쪽, 이번 주에 %d쪽 읽었어요. 모두 몇 쪽 읽었나요?", "쪽"),
                  ("색종이를 %d장 가지고 있었는데 친구가 %d장을 더 주었어요. 색종이는 모두 몇 장인가요?", "장"),
                  ("구슬을 빨간 상자에 %d개, 파란 상자에 %d개 담았어요. 구슬은 모두 몇 개인가요?", "개")])
    q = josa(who, "은/는") + " " + k[0] % (a, b)
    u = k[1]
    return mcq(q, "%d%s" % (s, u), ["%d%s" % (x, u) for x in (no_carry_add(a, b), abs(a - b), s + 100, s - 10) if x != s and x > 0],
               "모두 몇인지 구할 때는 덧셈을 해요. %d + %d = <b>%d</b>(%s)" % (a, b, s, u))


def story_sub():
    who = NM.next()
    a = R.randint(400, 950)
    b = R.randint(120, a - 100)
    if borrows(a, b) == 0:
        return None
    d = a - b
    k = R.choice([("%d원짜리 공책을 사려고 %d원을 냈어요. 거스름돈은 얼마인가요?", "원", True),
                  ("우리 학교 학생은 %d명이고, 그중 %d명이 남학생이에요. 여학생은 몇 명인가요?", "명", False),
                  ("밭에서 감자를 %d개 캤는데 %d개를 이웃에게 나누어 주었어요. 남은 감자는 몇 개인가요?", "개", False),
                  ("%d쪽인 동화책을 %d쪽까지 읽었어요. 남은 쪽수는 몇 쪽인가요?", "쪽", False)])
    if k[2]:
        q = josa(who, "이/가") + " " + k[0] % (b, a)
    else:
        q = k[0] % (a, b)
    u = k[1]
    return mcq(q, "%d%s" % (d, u), ["%d%s" % (x, u) for x in (a + b, no_borrow_sub(a, b), d + 10, d - 100) if x != d and x > 0],
               "남은 것, 차이를 구할 때는 뺄셈을 해요. %d − %d = <b>%d</b>(%s)" % (a, b, d, u))


def story_cmp():
    a, b = R.randint(300, 900), R.randint(150, 600)
    if a <= b or borrows(a, b) == 0:
        return None
    w1, w2 = NM.next(), NM.next()
    d = a - b
    q = "%s 줄넘기 기록은 %d번, %s 기록은 %d번이에요. %s %s보다 몇 번 더 많이 했나요?" % (w1 + "의", a, w2 + "의", b, josa(w1, "이/가"), w2)
    return mcq(q, "%d번" % d, ["%d번" % x for x in (a + b, no_borrow_sub(a, b), d + 10, d - 10) if x != d and x > 0],
               "두 수의 차이는 큰 수에서 작은 수를 빼요. %d − %d = <b>%d</b>(번)" % (a, b, d))


unit("grade-3", "add-and-subtract-three-digit-numbers", 1, "[4수01-03]",
     "세 자리 수의 덧셈과 뺄셈의 계산 원리를 이해하고 그 계산을 할 수 있다.",
     "세 자리 수의 덧셈과 뺄셈", "세 자리 수의 덧셈과 뺄셈",
     "초등 3학년 세 자리 수의 덧셈과 뺄셈 학습지: 받아올림, 받아내림, 0이 있는 뺄셈, □ 구하기, 문장제까지 100문제와 정답.",
     "같은 자리끼리, 일의 자리부터", "10이 넘으면 받아올림, 모자라면 받아내림해요.",
     ["세로로 쓸 때는 <b>일의 자리는 일의 자리끼리</b> 맞추어 써요.",
      "<b>덧셈</b>: 일의 자리부터 더해요. 같은 자리의 합이 10이거나 10보다 크면 바로 윗자리로 <b>1을 받아올림</b>해요.",
      "<b>뺄셈</b>: 빼는 수가 더 크면 바로 윗자리에서 <b>10을 받아내림</b>해요. 받아내림한 자리는 1 작아져요.",
      "뺄셈의 답은 <b>답 + 빼는 수 = 빼지는 수</b>로 확인해요."],
     [("456 + 378 =", ["일의 자리: 6 + 8 = 14 → 4를 쓰고 1을 받아올림", "십의 자리: 1 + 5 + 7 = 13 → 3을 쓰고 1을 받아올림", "백의 자리: 1 + 4 + 3 = 8"], "834"),
      ("703 − 258 =", ["일의 자리 3에서 8을 뺄 수 없어요. 십의 자리가 0이라 백의 자리에서 받아내림해요.", "703 = 6백 + 9십 + 13으로 생각해요.", "13 − 8 = 5, 9 − 5 = 4, 6 − 2 = 4"], "445")],
     [("받아올림한 1을 더하지 않는다", "받아올림한 1은 윗자리 숫자 위에 작게 써 두어요."),
      ("3 − 8을 할 수 없어서 8 − 3을 한다", "윗자리에서 10을 받아내림해서 13 − 8을 해요."),
      ("받아내림한 자리의 숫자를 그대로 쓴다", "받아내림한 자리는 1 작아져요. 0이면 다시 윗자리에서 받아내림해요.")],
     [("세 자리 수의 덧셈과 뺄셈은 언제 배우나요?", "2022 개정 교육과정 [4수01-03]으로, 초등 3학년 1학기 첫 단원에서 배워요. 받아올림과 받아내림이 여러 번 있는 계산까지 익혀요."),
      ("뺄셈 답이 맞는지 어떻게 확인하나요?", "답에 빼는 수를 더해 보세요. 빼지는 수가 나오면 맞은 거예요. 예: 703 − 258 = 445 → 445 + 258 = 703")],
     [("받아올림이 한 번 있는 덧셈", [(add(1), 20)]),
      ("받아올림이 두 번 있는 덧셈", [(add(2), 15), (add(3, 300, 899), 5)]),
      ("받아내림이 있는 뺄셈", [(sub(1), 14), (sub(2), 6)]),
      ("0이 있는 뺄셈과 □ 구하기", [(sub(2, zero=True), 10), (missing, 10)]),
      ("문장제", [(story_add, 7), (story_sub, 7), (story_cmp, 6)])],
     82301)
