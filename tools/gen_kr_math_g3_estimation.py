# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：어림셈（2022 개정 [4수01-08]）
몇십・몇백으로 어림하기、덧셈・뺄셈・곱셈・나눗셈의 어림셈、어림셈으로 판단하기（돈이 충분한가）。
誤答は「일의 자리를 버리지 않고 그대로 계산」「어림한 수를 잘못 고른다」から作る。
"""
import random
from kr_common import mcq, num, unit, Names, josa

R = random.Random(82321)
NM = Names(R)


def near(n, p):
    """가까운 몇십/몇백（5 이상は올림）"""
    return (n + p // 2) // p * p


def round_q():
    p = R.choice([10, 100])
    n = R.randint(12, 989) if p == 10 else R.randint(120, 9890)
    if n % p == 0 or n % p == p // 2:
        return None
    a = near(n, p)
    w = [a + p if a < n else a - p, n // p * p if a != n // p * p else n // p * p + p, a + 10 * p, a - p if a - p > 0 else a + 2 * p]
    return mcq("%s에 가장 가까운 몇%s은 얼마인가요?" % (num(n), "십" if p == 10 else "백"), num(a), [num(x) for x in w if x != a and x > 0],
               "%s은 %s와 %s 사이에 있고, %s에 더 가까워요. <b>%s</b>" % (num(n), num(n // p * p), num(n // p * p + p), num(a), num(a)))


def est_add():
    a, b = R.randint(110, 690), R.randint(110, 690)
    if a % 100 in (50,) or b % 100 in (50,):
        return None
    k = R.choice(["+", "−"])
    if k == "−" and a <= b:
        a, b = b, a
    if a == b:
        return None
    ea, eb = near(a, 100), near(b, 100)
    r = ea + eb if k == "+" else ea - eb
    if r <= 0:
        return None
    return mcq("%d %s %d를 몇백으로 어림하여 계산하면 얼마쯤인가요?" % (a, k, b), "약 %s" % num(r),
               ["약 %s" % num(x) for x in (r + 100, r - 100 if r > 100 else r + 200, (a + b if k == "+" else a - b), r + 1000) if x != r and x > 0],
               "%d는 약 %d, %d는 약 %d이니까 %d %s %d = <b>약 %s</b>" % (a, ea, b, eb, ea, k, eb, num(r)))


def est_mul():
    a, d = R.randint(21, 98), R.randint(2, 9)
    ea = near(a, 10)
    r = ea * d
    return mcq("%d × %d를 몇십 × (몇)으로 어림하면 얼마쯤인가요?" % (a, d), "약 %s" % num(r),
               ["약 %s" % num(x) for x in (r + 10 * d, r - 10 * d, a * d if a * d != r else r + 1, r * 10) if x != r and x > 0],
               "%d는 약 %d이니까 %d × %d = <b>약 %s</b>" % (a, ea, ea, d, num(r)))


def judge_money():
    who = NM.next()
    items = R.sample([("공책", 1450), ("연필", 780), ("지우개", 520), ("색연필", 2950), ("자", 1150), ("풀", 890), ("가위", 2480), ("필통", 3850)], 3)
    have = R.choice([3000, 4000, 5000, 6000, 7000, 8000])
    tot = sum(p for _, p in items)
    if abs(tot - have) < 300:
        return None
    ok = tot <= have
    t = "%s %s원을 가지고 있어요. %s을 사려고 해요. 돈이 충분한지 어림하여 판단하면?" % (josa(who, "은/는"), num(have), ", ".join("%s(%s원)" % (n, num(p)) for n, p in items))
    ans = "충분해요" if ok else "모자라요"
    est = sum(near(p, 100) for _, p in items)
    return mcq(t, ans, ["모자라요" if ok else "충분해요", "꼭 맞아요", "알 수 없어요"],
               "몇백으로 어림하면 %s = 약 %s원이에요. %s원과 비교하면 <b>%s</b>. (정확히는 %s원)" % (" + ".join(num(near(p, 100)) for _, p in items), num(est), num(have), ans, num(tot)))


def check_answer():
    a, b = R.randint(120, 890), R.randint(110, 880)
    k = R.choice(["+", "×"])
    if k == "+":
        true = a + b
        wrong = true + R.choice([-100, 100, 1000, -1000 if true > 1100 else 900])
    else:
        a, b = R.randint(21, 98), R.randint(3, 9)
        true = a * b
        wrong = true + R.choice([-100, 100, 200])
    show = R.choice([true, wrong])
    ok = show == true
    ea = near(a, 100 if k == "+" else 10)
    eb = near(b, 100) if k == "+" else b
    er = ea + eb if k == "+" else ea * eb
    t = "%s %d %s %d = %s라고 계산했어요. 어림셈으로 확인하면 이 답은 어떤가요?" % (josa(NM.next(), "이/가"), a, k, b, num(show))
    ans = "맞을 것 같아요" if ok else "틀렸어요"
    return mcq(t, ans, ["틀렸어요" if ok else "맞을 것 같아요", "어림으로는 알 수 없어요", "계산할 필요가 없어요"],
               "어림하면 %d %s %d = 약 %s예요. %s는 이 값과 %s. (정확한 답: %s)" % (ea, k, eb, num(er), num(show), "가까워요" if ok else "많이 달라요", num(true)))


def story():
    k = R.choice(["people", "bus", "pages"])
    if k == "people":
        a, b = R.randint(210, 490), R.randint(210, 490)
        t = "토요일에 %d명, 일요일에 %d명이 박물관에 왔어요. 이틀 동안 온 사람은 약 몇백 명인가요?" % (a, b)
        r = near(a, 100) + near(b, 100)
        return mcq(t, "약 %d명" % r, ["약 %d명" % x for x in (r + 100, r - 100, a + b, r + 1000) if x != r],
                   "%d → %d, %d → %d. %d + %d = <b>약 %d명</b>" % (a, near(a, 100), b, near(b, 100), near(a, 100), near(b, 100), r))
    if k == "bus":
        a, d = R.randint(28, 46), R.randint(3, 9)
        r = near(a, 10) * d
        t = "버스 한 대에 %d명씩 탔어요. 버스 %d대에 탄 사람은 약 몇 명인가요? (몇십으로 어림하세요)" % (a, d)
        return mcq(t, "약 %d명" % r, ["약 %d명" % x for x in (r + 10 * d, r - 10 * d, a * d, r * 10) if x != r],
                   "%d는 약 %d이니까 %d × %d = <b>약 %d명</b>" % (a, near(a, 10), near(a, 10), d, r))
    a, b = R.randint(310, 890), R.randint(110, 290)
    t = "%d쪽인 책을 %d쪽까지 읽었어요. 남은 쪽수는 약 몇백 쪽인가요?" % (a, b)
    r = near(a, 100) - near(b, 100)
    if r <= 0:
        return None
    return mcq(t, "약 %d쪽" % r, ["약 %d쪽" % x for x in (r + 100, r - 100 if r > 100 else r + 200, a - b, r + 1000) if x != r and x > 0],
               "%d → %d, %d → %d. %d − %d = <b>약 %d쪽</b>" % (a, near(a, 100), b, near(b, 100), near(a, 100), near(b, 100), r))


unit("grade-3", "estimation", 21, "[4수01-08]",
     "자연수의 덧셈, 뺄셈, 곱셈, 나눗셈과 관련한 여러 가지 상황에서 어림셈을 할 수 있다.",
     "어림셈", "어림셈",
     "초등 3학년 어림셈 학습지: 가까운 몇십, 몇백 찾기, 덧셈과 뺄셈의 어림셈, 곱셈의 어림셈, 돈이 충분한지 판단하기, 계산 결과 확인하기까지 100문제와 정답.",
     "가까운 몇십, 몇백으로 바꾸어 계산", "답이 맞는지 확인할 때도 어림셈을 써요.",
     ["정확한 값이 꼭 필요하지 않을 때는 <b>어림셈</b>을 해요. 수를 가까운 몇십이나 몇백으로 바꾸어 계산해요.",
      "382는 300과 400 사이에 있고 400에 더 가까워요. 그래서 382는 <b>약 400</b>이에요.",
      "382 + 219는 400 + 200 = 600쯤이에요. 계산한 답이 600과 많이 다르면 다시 계산해 봐요.",
      "돈이 충분한지 알아볼 때는 값을 조금 크게 어림하면 안전해요."],
     [("489 + 312를 몇백으로 어림하면?", ["489 → 500, 312 → 300", "500 + 300 = 800"], "약 800"),
      ("48 × 6을 몇십으로 어림하면?", ["48 → 50", "50 × 6 = 300"], "약 300")],
     [("어림한 값을 정확한 답이라고 쓴다", "어림셈의 답 앞에는 「약」을 붙여요."),
      ("382를 300으로 어림한다", "382는 300보다 400에 더 가까워요."),
      ("계산한 뒤 확인하지 않는다", "어림한 값과 비교하면 큰 실수를 찾을 수 있어요.")],
     [("어림셈은 왜 배우나요?", "물건을 살 때 돈이 충분한지 빨리 판단하거나, 계산한 답이 맞는지 확인할 때 쓸모가 있어요."),
      ("반올림과 어림셈은 같은가요?", "어림셈은 가까운 몇십, 몇백으로 바꾸어 대략 계산하는 것이에요. 올림, 버림, 반올림은 5학년에서 정확히 배워요.")],
     [("가까운 몇십, 몇백", [(round_q, 20)]),
      ("덧셈과 뺄셈의 어림셈", [(est_add, 20)]),
      ("곱셈의 어림셈", [(est_mul, 20)]),
      ("어림셈으로 판단하기", [(judge_money, 10), (check_answer, 10)]),
      ("문장제", [(story, 20)])],
     82321)
