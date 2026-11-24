# -*- coding: utf-8 -*-
"""
대한민국 초등 5학년 수학：규칙과 대응・평균・가능성
  corr    : 규칙과 대응 [6수02-01]
  average : 평균 [6수04-01]
  chance  : 일이 일어날 가능성 [6수04-04] [6수04-05] [6수04-06]
誤答は「대응 관계를 덧셈으로만 본다」「평균을 자료의 수로 나누지 않는다」「가능성을 개수로 말한다」から作る。
"""
import random
from fractions import Fraction as F
from kr_common import mcq, unit, Names, josa, num, fr, table
from kr_pics import fig, svg_wrap, text, line, INK

R = random.Random(82518)
NM = Names(R)

THINGS = [("의자", "다리", 4), ("세발자전거", "바퀴", 3), ("오토바이", "바퀴", 2), ("문어", "다리", 8), ("거미", "다리", 8), ("개미", "다리", 6),
          ("자동차", "바퀴", 4), ("삼각형", "꼭짓점", 3), ("오각형", "변", 5), ("육각형", "변", 6)]


def tbl(head, xs, ys):
    return table(head, [[str(x) for x in xs], [str(y) for y in ys]]).replace("<thead>", "<tbody>", 0)


def corr_table():
    th, part, k = R.choice(THINGS)
    xs = sorted(R.sample(range(1, 12), 4))
    ys = [k * x for x in xs]
    i = R.randrange(4)
    shown = [str(y) if j != i else "□" for j, y in enumerate(ys)]
    t = table(["%s의 수" % th] + [str(x) for x in xs], [["%s의 수" % part] + shown])
    return mcq(t + "%s의 수와 %s의 수 사이의 대응 관계예요. □에 알맞은 수는?" % (th, part), str(ys[i]), [str(ys[i] + k), str(xs[i] + k), str(ys[i] - 1)],
               "%s의 수는 %s의 수의 %d배예요. %d × %d = <b>%d</b>" % (part, th, k, xs[i], k, ys[i]))


def corr_rule():
    kind = R.choice(["mul", "add", "sub"])
    k = R.randint(2, 9)
    xs = sorted(R.sample(range(1, 15), 4))
    if kind == "mul":
        ys = [x * k for x in xs]
        ans = "△ = □ × %d" % k
        alts = ["△ = □ + %d" % k, "□ = △ × %d" % k, "△ = □ ÷ %d" % k]
    elif kind == "add":
        ys = [x + k for x in xs]
        ans = "△ = □ + %d" % k
        alts = ["△ = □ × %d" % k, "□ = △ + %d" % k, "△ = □ − %d" % k]
    else:
        xs = [x + k for x in xs]
        ys = [x - k for x in xs]
        ans = "△ = □ − %d" % k
        alts = ["△ = □ + %d" % k, "□ = △ − %d" % k, "△ = □ ÷ %d" % k]
    t = table(["□"] + [str(x) for x in xs], [["△"] + [str(y) for y in ys]])
    return mcq(t + "□와 △ 사이의 대응 관계를 식으로 바르게 나타낸 것은?", ans, alts,
               "표의 모든 칸에서 성립하는 식을 찾아요. <b>%s</b>" % ans)


def corr_story():
    k = R.choice(["age", "cut", "price", "water"])
    who = NM.next()
    if k == "age":
        d = R.randint(25, 35)
        x = R.randint(6, 13)
        y = x + d
        return mcq("%s 어머니의 나이는 항상 %d살 차이가 나요. %s 나이가 %d살이 되면 어머니는 몇 살인가요?" % (josa(who, "과/와"), d, who + "의", x), "%d살" % y,
                   ["%d살" % v for v in (x * 3, d, y + 1)], "(어머니의 나이) = (%s의 나이) + %d. %d + %d = <b>%d살</b>" % (who, d, x, d, y))
    if k == "cut":
        n = R.randint(3, 15)
        return mcq("끈을 한 번 자르면 2도막, 두 번 자르면 3도막이 돼요. %d번 자르면 몇 도막이 되나요?" % n, "%d도막" % (n + 1),
                   ["%d도막" % v for v in (n, 2 * n, n + 2)], "(도막의 수) = (자른 횟수) + 1. %d + 1 = <b>%d도막</b>" % (n, n + 1))
    if k == "price":
        p = R.choice([300, 400, 500, 700, 800, 1200])
        n = R.randint(3, 12)
        return mcq("공책 한 권이 %s원이에요. 공책 수를 □, 값을 △라고 할 때 □ = %d이면 △는 얼마인가요?" % (num(p), n), "%s원" % num(p * n),
                   ["%s원" % num(v) for v in (p + n, p * (n + 1), p * n // 10)], "△ = □ × %d. %d × %s = <b>%s원</b>" % (p, n, num(p), num(p * n)))
    a = R.randint(2, 9)
    m = R.randint(5, 20)
    return mcq("물통에 1분마다 물이 %d L씩 일정하게 들어가요. 물을 %d분 동안 받으면 물은 몇 L인가요?" % (a, m), "%d L" % (a * m),
               ["%d L" % v for v in (a + m, a * (m - 1), a * m + a)], "(물의 양) = (시간) × %d. %d × %d = <b>%d L</b>" % (a, m, a, a * m))


def corr_pattern():
    n = R.randint(4, 15)
    k = R.choice(["tri", "sq"])
    if k == "tri":
        return mcq("성냥개비로 정삼각형을 옆으로 이어 붙여요. 정삼각형 1개에 3개, 2개에 5개, 3개에 7개가 필요해요. 정삼각형 %d개를 만들려면 성냥개비는 몇 개 필요한가요?" % n,
                   "%d개" % (2 * n + 1), ["%d개" % v for v in (3 * n, 2 * n, 2 * n + 2)], "(성냥개비 수) = (삼각형 수) × 2 + 1. %d × 2 + 1 = <b>%d개</b>" % (n, 2 * n + 1))
    return mcq("성냥개비로 정사각형을 옆으로 이어 붙여요. 정사각형 1개에 4개, 2개에 7개, 3개에 10개가 필요해요. 정사각형 %d개를 만들려면 성냥개비는 몇 개 필요한가요?" % n,
               "%d개" % (3 * n + 1), ["%d개" % v for v in (4 * n, 3 * n, 3 * n + 2)], "(성냥개비 수) = (사각형 수) × 3 + 1. %d × 3 + 1 = <b>%d개</b>" % (n, 3 * n + 1))


# ---------------------------------------------------------------- 평균
def data(n, lo, hi):
    while True:
        xs = [R.randint(lo, hi) for _ in range(n)]
        if sum(xs) % n == 0 and len(set(xs)) > 2:
            return xs


def avg_q():
    n = R.randint(3, 6)
    xs = data(n, 10, 60)
    m = sum(xs) // n
    return mcq("%s의 평균은?" % ", ".join(map(str, xs)), str(m), [str(sum(xs)), str((max(xs) + min(xs)) // 2) if (max(xs) + min(xs)) // 2 != m else str(m + 1), str(sum(xs) // (n - 1)) if sum(xs) // (n - 1) != m else str(m + 2)],
               "(자료의 값을 모두 더한 수) ÷ (자료의 수) = %d ÷ %d = <b>%d</b>" % (sum(xs), n, m))


SUBJ = [("턱걸이 기록", "회"), ("줄넘기 기록", "번"), ("읽은 책 수", "권"), ("받은 칭찬 스티커", "장"), ("오래 매달리기 기록", "초")]


def avg_table():
    th, u = R.choice(SUBJ)
    n = R.randint(4, 5)
    names = []
    while len(names) < n:
        x = NM.next()
        if x not in names:
            names.append(x)
    xs = data(n, 5, 45)
    m = sum(xs) // n
    t = table(["이름"] + names, [["%s(%s)" % (th, u)] + [str(x) for x in xs]])
    if R.random() < 0.6:
        return mcq(t + "%s의 평균은 몇 %s인가요?" % (th, u), "%d%s" % (m, u), ["%d%s" % (v, u) for v in (sum(xs), m + 1, m - 1)],
                   "%d ÷ %d = <b>%d%s</b>" % (sum(xs), n, m, u))
    above = [nm for nm, x in zip(names, xs) if x > m]
    return mcq(t + "%s 평균보다 많은 사람은 모두 몇 명인가요?" % josa(th, "이/가"), "%d명" % len(above), ["%d명" % v for v in {0, 1, 2, 3, 4, 5} - {len(above)}],
               "평균은 %s. %d%s보다 많은 사람은 <b>%d명</b>이에요." % (josa("%d%s" % (m, u), "이에요/예요"), m, u, len(above)))


def avg_missing():
    n = R.randint(4, 5)
    m = R.randint(10, 40)
    xs = [m + R.randint(-8, 8) for _ in range(n - 1)]
    last = m * n - sum(xs)
    if last <= 0 or last > 99:
        return None
    return mcq("%d개 자료의 평균이 %d예요. 그중 %d개가 %s일 때, 나머지 한 자료는?" % (n, m, n - 1, ", ".join(map(str, xs))), str(last),
               [str(m), str(m * (n - 1) - sum(xs)) if m * (n - 1) - sum(xs) > 0 else str(last + n), str(last + 1)],
               "평균 × 자료의 수 = %d × %d = %d. %d − (%s) = <b>%d</b>" % (m, n, m * n, m * n, " + ".join(map(str, xs)), last))


def avg_compare():
    a_n, b_n = R.randint(3, 5), R.randint(3, 5)
    a = data(a_n, 20, 60)
    b = data(b_n, 20, 60)
    ma, mb = sum(a) // a_n, sum(b) // b_n
    if ma == mb:
        return None
    w = "가 모둠" if ma > mb else "나 모둠"
    return mcq("가 모둠 %d명의 기록은 %s, 나 모둠 %d명의 기록은 %s예요. 평균이 더 높은 모둠은?" % (a_n, ", ".join(map(str, a)), b_n, ", ".join(map(str, b))), w,
               ["나 모둠" if w == "가 모둠" else "가 모둠", "같아요", "비교할 수 없어요"],
               "가 모둠 %d ÷ %d = %d, 나 모둠 %d ÷ %d = %d. <b>%s</b>" % (sum(a), a_n, ma, sum(b), b_n, mb, w))


def avg_story():
    k = R.choice(["add", "need", "days"])
    if k == "need":
        n = R.randint(3, 4)
        target = R.randint(80, 92)
        xs = [target + R.randint(-10, 6) for _ in range(n)]
        need = target * (n + 1) - sum(xs)
        if not 60 <= need <= 100:
            return None
        return mcq("수학 시험을 %d번 봤고 점수는 %s점이에요. 다음 시험까지 %d번의 평균이 %d점이 되려면 다음 시험에서 몇 점을 받아야 하나요?" % (n, ", ".join(map(str, xs)), n + 1, target),
                   "%d점" % need, ["%d점" % v for v in (target, need + 5, need - 5)],
                   "%d × %d = %d, %d − %d = <b>%d점</b>" % (target, n + 1, target * (n + 1), target * (n + 1), sum(xs), need))
    if k == "days":
        d = R.randint(5, 7)
        m = R.randint(20, 60)
        return mcq("하루 평균 %d쪽씩 %d일 동안 책을 읽었어요. 모두 몇 쪽을 읽었나요?" % (m, d), "%d쪽" % (m * d), ["%d쪽" % v for v in (m + d, m * (d - 1), m)],
                   "(평균) × (날수) = %d × %d = <b>%d쪽</b>" % (m, d, m * d))
    n = R.randint(4, 6)
    m = R.randint(30, 50)
    x = R.randint(m - 20, m + 30)
    newm = F(m * n + x, n + 1)
    if newm.denominator != 1:
        return None
    return mcq("%d명의 몸무게 평균이 %d kg이에요. 몸무게가 %d kg인 학생 1명이 더 들어오면 평균은 몇 kg이 되나요?" % (n, m, x), "%d kg" % newm,
               ["%d kg" % v for v in ((m + x) // 2, m, int(newm) + 1)], "(%d × %d + %d) ÷ %d = <b>%d kg</b>" % (m, n, x, n + 1, newm))


# ---------------------------------------------------------------- 가능성
WORDS = ["불가능하다", "~ 아닐 것 같다", "반반이다", "~일 것 같다", "확실하다"]
EVENTS = [("내일 아침에 해가 서쪽에서 뜰 것입니다.", 0), ("1부터 6까지 적힌 주사위를 굴리면 7이 나올 것입니다.", 0), ("동전을 던지면 그림면이 나올 것입니다.", 2),
          ("12월 다음에는 1월이 올 것입니다.", 4), ("주사위를 굴리면 짝수가 나올 것입니다.", 2), ("주사위를 굴리면 6 이하의 수가 나올 것입니다.", 4),
          ("빨간 공만 들어 있는 주머니에서 공을 꺼내면 빨간 공일 것입니다.", 4), ("빨간 공만 들어 있는 주머니에서 공을 꺼내면 파란 공일 것입니다.", 0),
          ("월요일 다음 날은 화요일일 것입니다.", 4), ("주사위를 굴리면 홀수가 나올 것입니다.", 2)]


def ch_word():
    t, v = R.choice(EVENTS)
    return mcq("「%s」 일이 일어날 가능성을 말로 나타내면?" % t, WORDS[v], R.sample([w for i, w in enumerate(WORDS) if i != v], 3),
               "일이 일어날 가능성은 불가능하다, ~ 아닐 것 같다, 반반이다, ~일 것 같다, 확실하다로 나타내요. <b>%s</b>" % WORDS[v])


def ch_num():
    t, v = R.choice(EVENTS)
    val = {0: "0", 2: fr(1, 2), 4: "1"}[v]
    return mcq("「%s」 일이 일어날 가능성을 수로 나타내면?" % t, val, [x for x in ("0", fr(1, 2), "1", "2") if x != val],
               "불가능하다는 0, 반반이다는 %s, 확실하다는 1로 나타내요. <b>%s</b>" % (fr(1, 2), val))


def ch_bag():
    r, b = R.randint(0, 6), R.randint(0, 6)
    if r + b == 0:
        return None
    if r == 0:
        v = 0
    elif b == 0:
        v = 4
    elif r == b:
        v = 2
    elif r > b:
        v = 3
    else:
        v = 1
    have = "빨간 공 %d개와 파란 공 %d개가" % (r, b) if r and b else ("파란 공만 %d개가" % b if b else "빨간 공만 %d개가" % r)
    s = "주머니에 %s 있어요. 공 1개를 꺼낼 때 빨간 공일 가능성을 말로 나타내면?" % have
    word = WORDS[v].replace("~ 아닐 것 같다", "빨간 공이 아닐 것 같다").replace("~일 것 같다", "빨간 공일 것 같다")
    alts = [w.replace("~ 아닐 것 같다", "빨간 공이 아닐 것 같다").replace("~일 것 같다", "빨간 공일 것 같다") for i, w in enumerate(WORDS) if i != v]
    return mcq(s, word, alts, "빨간 공 %d개, 파란 공 %d개이므로 <b>%s</b>." % (r, b, word))


def wordof(f, t):
    return WORDS[0 if f == 0 else 4 if f == t else 2 if 2 * f == t else 3 if 2 * f > t else 1]


def ch_dice():
    n = R.randint(1, 7)
    k = R.choice(["이상", "이하", "초과", "미만"])
    good = [x for x in range(1, 7) if (x >= n if k == "이상" else x <= n if k == "이하" else x > n if k == "초과" else x < n)]
    w = wordof(len(good), 6)
    return mcq("1부터 6까지 적힌 주사위를 굴릴 때 %d %s인 수가 나올 가능성을 말로 나타내면?" % (n, k), w, R.sample([x for x in WORDS if x != w], 3),
               ("%d %s인 수는 %s로 6개 중 %d개예요. <b>%s</b>" % (n, k, ", ".join(map(str, good)), len(good), w)) if good else "%d %s인 수는 주사위에 없어요. <b>%s</b>" % (n, k, w))


def ch_card():
    t = R.choice([4, 6, 8, 10])
    k = R.choice(["짝수", "홀수", "배수", "이하"])
    if k == "짝수":
        good = [x for x in range(1, t + 1) if x % 2 == 0]
        cond = "짝수"
    elif k == "홀수":
        good = [x for x in range(1, t + 1) if x % 2]
        cond = "홀수"
    elif k == "배수":
        m = R.randint(2, 5)
        good = [x for x in range(1, t + 1) if x % m == 0]
        cond = "%d의 배수" % m
    else:
        m = R.randint(1, t + 2)
        good = [x for x in range(1, t + 1) if x <= m]
        cond = "%d 이하인 수" % m
    w = wordof(len(good), t)
    return mcq("1부터 %d까지의 수 카드 %d장 중에서 한 장을 뽑을 때 %s가 나올 가능성을 말로 나타내면?" % (t, t, cond), w, R.sample([x for x in WORDS if x != w], 3),
               "%s는 %d장 중 %d장이에요. <b>%s</b>" % (cond, t, len(good), w))


def ch_compare():
    sp = R.choice([(4, 1), (4, 2), (4, 3), (8, 1), (8, 3), (8, 5), (6, 1), (6, 2)])
    n, k = sp
    return mcq("%d칸으로 똑같이 나뉜 회전판 중 %d칸이 빨간색이에요. 회전판을 돌렸을 때 화살이 빨간색에 멈출 가능성과 파란색(나머지)에 멈출 가능성 중 더 큰 것은?" % (n, k),
               "빨간색" if 2 * k > n else ("파란색" if 2 * k < n else "같아요"), ["빨간색", "파란색", "같아요", "알 수 없어요"],
               "칸이 더 많은 색에 멈출 가능성이 커요. 빨간색 %d칸, 파란색 %d칸." % (k, n - k))


def build(which):
    G = "grade-5"
    if which == "corr":
        return unit(G, "rules-and-correspondence", 4, "[6수02-01]",
                    "한 양이 변할 때 다른 양이 그에 종속하여 변하는 대응 관계를 나타낸 표에서 규칙을 찾아 설명하고, □, △ 등을 사용하여 식으로 나타낼 수 있다.",
                    "규칙과 대응", "규칙과 대응",
                    "초등 5학년 1학기 규칙과 대응 학습지: 대응 관계를 표로 나타내기, □와 △를 사용한 식, 성냥개비 규칙, 나이・가격・도막 수 문장제까지 100문제와 정답.",
                    "한 양이 변하면 다른 양도 변해요", "□와 △로 대응 관계를 식으로",
                    ["한 양이 변할 때 다른 양이 그에 따라 변하는 관계를 <b>대응 관계</b>라고 해요.",
                     "표에서 두 양 사이의 규칙을 찾고, □, △ 같은 기호로 식을 만들어요. 예: △ = □ × 4",
                     "식을 만들면 표에 없는 큰 수도 쉽게 구할 수 있어요."],
                    [("의자 수(□)와 다리 수(△)의 식", ["의자 1개 → 다리 4개", "의자 2개 → 다리 8개"], "△ = □ × 4")],
                    [("첫 두 칸만 보고 규칙을 정한다", "표의 모든 칸에서 맞는지 확인해요."),
                     ("□와 △의 자리를 바꿔 쓴다", "어느 양이 어느 양에 따라 변하는지 생각해요."),
                     ("끈을 n번 자르면 n도막이라고 한다", "자른 횟수 + 1이 도막 수예요.")],
                    [("규칙과 대응은 언제 배우나요?", "초등 5학년 1학기 「규칙과 대응」 단원에서 배워요."),
                     ("중학교의 어떤 내용과 이어지나요?", "중학교의 정비례와 함수로 이어져요.")],
                    [("표에서 대응 관계 찾기", [(corr_table, 20)]),
                     ("대응 관계를 식으로", [(corr_rule, 20)]),
                     ("모양의 규칙", [(corr_pattern, 10), (corr_table, 10)]),
                     ("섞어서 연습", [(corr_rule, 10), (corr_table, 10)]),
                     ("문장제", [(corr_story, 20)])], 82518)
    if which == "average":
        return unit(G, "averages", 18, "[6수04-01]",
                    "평균의 의미를 알고, 자료를 수집하여 평균을 구하고 해석할 수 있다.",
                    "평균 구하기와 해석하기", "평균",
                    "초등 5학년 2학기 평균 학습지: 평균 구하기, 표에서 평균 구하기, 평균보다 많은 자료, 모르는 자료 구하기, 두 모둠의 평균 비교, 문장제까지 100문제와 정답.",
                    "평균 = 자료의 합 ÷ 자료의 수", "평균으로 두 모둠을 공정하게 비교해요.",
                    ["자료의 값을 모두 더해 자료의 수로 나눈 값을 <b>평균</b>이라고 해요.",
                     "평균은 자료를 고르게 했을 때의 값이에요. 많은 것에서 적은 것으로 옮겨 맞추어 볼 수도 있어요.",
                     "(자료의 합) = (평균) × (자료의 수)를 이용하면 모르는 자료를 구할 수 있어요.",
                     "모둠의 사람 수가 달라도 평균으로 비교할 수 있어요."],
                    [("12, 15, 9, 20의 평균", ["12 + 15 + 9 + 20 = 56", "56 ÷ 4 = 14"], "14")],
                    [("합만 구하고 나누지 않는다", "자료의 수로 나눠야 평균이에요."),
                     ("가장 큰 값과 가장 작은 값의 중간을 평균으로 쓴다", "모든 자료를 더해서 나눠요."),
                     ("사람 수가 다른 모둠을 합으로 비교한다", "평균으로 비교해야 공정해요.")],
                    [("평균은 언제 배우나요?", "초등 5학년 2학기 「평균과 가능성」 단원에서 배워요."),
                     ("평균이 자료에 없는 값일 수도 있나요?", "네. 평균은 자료에 없는 값일 수도 있어요.")],
                    [("평균 구하기", [(avg_q, 20)]),
                     ("표에서 평균", [(avg_table, 20)]),
                     ("모르는 자료 구하기", [(avg_missing, 20)]),
                     ("평균 비교하기", [(avg_compare, 20)]),
                     ("문장제", [(avg_story, 20)])], 82519)
    return unit(G, "likelihood", 19, "[6수04-04] [6수04-05] [6수04-06]",
                "사건이 일어날 가능성을 말로 표현하고 비교할 수 있다. 사건이 일어날 가능성을 수로 나타낼 수 있다. 자료를 이용하여 가능성을 예상하고, 가능성에 근거하여 적절한 판단을 내릴 수 있다.",
                "일이 일어날 가능성", "가능성",
                "초등 5학년 2학기 가능성 학습지: 불가능하다・반반이다・확실하다로 말하기, 가능성을 0, 1/2, 1로 나타내기, 주머니와 회전판의 가능성 비교까지 100문제와 정답.",
                "불가능 0, 반반 1/2, 확실 1", "가능성은 0부터 1 사이의 수로 나타내요.",
                ["일이 일어날 가능성은 <b>불가능하다</b>, ~ 아닐 것 같다, <b>반반이다</b>, ~일 것 같다, <b>확실하다</b>로 말할 수 있어요.",
                 "수로 나타내면 불가능하다는 0, 반반이다는 <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>, 확실하다는 1이에요.",
                 "주머니의 공이나 회전판의 칸이 많을수록 그것이 나올 가능성이 커요."],
                [("동전을 던져 숫자면이 나올 가능성", ["그림면과 숫자면 두 가지 중 하나"], "반반이다, <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>")],
                [("가능성을 개수로 말한다", "가능성은 0부터 1 사이의 수로 나타내요."),
                 ("확실한 일의 가능성을 2로 쓴다", "확실하다는 1이에요."),
                 ("칸 수가 같으면 가능성이 다르다고 생각한다", "칸 수가 같으면 가능성도 같아요.")],
                [("가능성은 언제 배우나요?", "초등 5학년 2학기 「평균과 가능성」 단원에서 배워요."),
                 ("확률과 같은가요?", "가능성을 수로 나타낸 것이 중학교에서 배우는 확률이에요.")],
                [("말로 나타내기", [(ch_word, 6), (ch_bag, 14)]),
                 ("수로 나타내기", [(ch_num, 6), (ch_dice, 14)]),
                 ("주머니의 공", [(ch_bag, 20)]),
                 ("가능성 비교하기", [(ch_compare, 8), (ch_card, 12)]),
                 ("섞어서 연습", [(ch_word, 4), (ch_num, 4), (ch_dice, 6), (ch_card, 6)])], 82520)
