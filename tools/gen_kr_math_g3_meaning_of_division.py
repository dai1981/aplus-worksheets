# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：나눗셈의 뜻（2022 개정 [4수01-05]）
똑같이 나누기（등분제）、몇 번 덜어 내기（포함제）、곱셈과 나눗셈의 관계、곱셈구구로 몫 구하기。
誤答は「나누는 수와 몫を取り違える」「곱한다」「뺄셈と混同」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa
from kr_pics import groups, row, array, KO, KINDS

R = random.Random(82304)
NM = Names(R)


def pick():
    d, q = R.randint(2, 9), R.randint(2, 9)
    return d, q, d * q


def read_eq():
    d, q, n = pick()
    k = R.choice(["read", "name_q", "name_d"])
    if k == "read":
        return mcq("나눗셈식 %d ÷ %d = %d를 바르게 읽은 것은?" % (n, d, q), "%d 나누기 %d는 %d와 같습니다" % (n, d, q),
                   ["%d 나누기 %d는 %d와 같습니다" % (d, n, q), "%d 곱하기 %d는 %d와 같습니다" % (n, d, q), "%d 빼기 %d는 %d와 같습니다" % (n, d, q)],
                   "÷는 「나누기」라고 읽어요. <b>%d 나누기 %d는 %d와 같습니다</b>." % (n, d, q))
    if k == "name_q":
        return mcq("나눗셈식 %d ÷ %d = %d에서 몫은 얼마인가요?" % (n, d, q), str(q), [str(n), str(d), str(n - d)],
                   "나눗셈의 결과 %d를 %d를 %d로 나눈 <b>몫</b>이라고 해요." % (q, n, d))
    return mcq("나눗셈식 %d ÷ %d = %d에서 %d는 무엇을 나눈 수인가요?" % (n, d, q, n), "나누어지는 수", ["나누는 수", "몫", "곱"],
               "%d는 똑같이 나누어지는 수, %d는 나누는 수, %d는 몫이에요." % (n, d, q))


def share():
    """똑같이 나누기（등분제）"""
    d, q, n = pick()
    kind = R.choice(["apple", "ball", "button", "flower", "cup"])
    nm, cnt = KO[kind]
    pic = row(n, kind, per_row=min(10, max(d, 5))) if n <= 40 else ""
    q_ = pic + "%s %d%s를 %d명에게 똑같이 나누어 주려고 해요. 한 명에게 몇 %s씩 줄 수 있나요?" % (nm, n, cnt, d, cnt)
    return mcq(q_, "%d%s" % (q, cnt), ["%d%s" % (x, cnt) for x in (d, n - d, n + d, q + 1) if x != q and x > 0],
               "%d를 %d로 똑같이 나누면 <b>%d ÷ %d = %d</b>(%s)씩이에요." % (n, d, n, d, q, cnt))


def scoop():
    """몇 번 덜어 내기（포함제）"""
    d, q, n = pick()
    thing, c, box = R.choice([("구슬", "개", "주머니"), ("쿠키", "개", "봉지"), ("연필", "자루", "필통"), ("딸기", "개", "접시"),
                              ("사탕", "개", "봉지"), ("색종이", "장", "묶음")])
    q_ = "%s %d%s를 한 %s에 %d%s씩 담으려고 해요. %s는 몇 개 필요한가요?" % (thing, n, c, box, d, c, box)
    return mcq(q_, "%d개" % q, ["%d개" % x for x in (d, n - d, n * d if n * d < 100 else q + 2, q + 1) if x != q and x > 0],
               "%d에서 %d씩 %d번 덜어 낼 수 있어요. <b>%d ÷ %d = %d</b>(개)" % (n, d, q, n, d, q))


def pic_groups():
    d, q, n = pick()
    if n > 40:
        return None
    kind = R.choice(KINDS)
    nm, cnt = KO[kind]
    if R.random() < 0.5:
        f = groups([(q, kind)] * d)
        return mcq(f + "%s %d%s를 %d묶음으로 똑같이 나누었어요. 이것을 나눗셈식으로 바르게 나타낸 것은?" % (nm, n, cnt, d),
                   "%d ÷ %d = %d" % (n, d, q), ["%d ÷ %d = %d" % (n, q, d) if q != d else "%d × %d = %d" % (d, q, n), "%d − %d = %d" % (n, d, n - d), "%d + %d = %d" % (q, d, q + d)],
                   "%d개를 %d묶음으로 나누면 한 묶음에 %d개예요. <b>%d ÷ %d = %d</b>" % (n, d, q, n, d, q))
    f = groups([(d, kind)] * q)
    return mcq(f + "%s %d%s를 %d%s씩 묶었어요. 몇 묶음인가요?" % (nm, n, cnt, d, cnt), "%d묶음" % q,
               ["%d묶음" % x for x in (d, n - d, q + 1, q - 1) if x != q and x > 0],
               "%d씩 묶으면 <b>%d ÷ %d = %d</b>(묶음)이에요." % (d, n, d, q))


def relation():
    d, q, n = pick()
    k = R.choice(["mul2div", "div2mul", "pair"])
    if k == "mul2div":
        return mcq("곱셈식 %d × %d = %d를 나눗셈식으로 바르게 나타낸 것은?" % (d, q, n), "%d ÷ %d = %d" % (n, d, q),
                   ["%d ÷ %d = %d" % (d, q, n), "%d ÷ %d = %d" % (q, n, d), "%d ÷ %d = %d" % (n, d, n - d)],
                   "곱셈식 %d × %d = %d는 나눗셈식 %d ÷ %d = %d, %d ÷ %d = %d로 나타낼 수 있어요." % (d, q, n, n, d, q, n, q, d))
    if k == "div2mul":
        return mcq("나눗셈식 %d ÷ %d = %d를 곱셈식으로 바르게 나타낸 것은?" % (n, d, q), "%d × %d = %d" % (d, q, n),
                   ["%d × %d = %d" % (n, d, q), "%d × %d = %d" % (n, q, d), "%d × %d = %d" % (q, q, q * q) if q * q != n else "%d + %d = %d" % (d, q, d + q)],
                   "몫 %d와 나누는 수 %d를 곱하면 나누어지는 수 %d가 돼요. <b>%d × %d = %d</b>" % (q, d, n, d, q, n))
    return mcq("%d × □ = %d를 이용하여 %d ÷ %d의 몫을 구하면?" % (d, n, n, d), str(q), [str(x) for x in (d, n - d, q + 1, q - 1) if x != q and x > 0],
               "%d × <b>%d</b> = %d이니까 %d ÷ %d = <b>%d</b>예요." % (d, q, n, n, d, q))


def times_table():
    d, q, n = pick()
    return mcq("%d ÷ %d =" % (n, d), str(q), [str(x) for x in (q + 1, q - 1, d, n - d, q + 2) if x != q and x > 0],
               "%d단 곱셈구구에서 곱이 %d인 것을 찾아요. %d × %d = %d → <b>%d</b>" % (d, n, d, q, n, q))


def missing():
    d, q, n = pick()
    if R.random() < 0.5:
        return mcq("□ ÷ %d = %d에서 □에 알맞은 수는?" % (d, q), str(n), [str(x) for x in (q, d + q, n + d, n - d) if x != n and x > 0],
                   "□ = %d × %d = <b>%d</b>예요." % (d, q, n))
    return mcq("%d ÷ □ = %d에서 □에 알맞은 수는?" % (n, q), str(d), [str(x) for x in (n * q if n * q < 100 else n + q, n - q, d + 1, q) if x != d and x > 0],
               "%d × %d = %d이니까 □ = <b>%d</b>예요." % (q, d, n, d))


def story():
    d, q, n = pick()
    who = NM.next()
    k = R.choice(["share", "scoop", "legs", "team"])
    if k == "share":
        t = "%s 사탕 %d개를 친구 %d명에게 똑같이 나누어 주었어요. 한 명이 받은 사탕은 몇 개인가요?" % (josa(who, "은/는"), n, d)
        a, u = q, "개"
    elif k == "scoop":
        t = "꽃 %d송이를 꽃병 한 개에 %d송이씩 꽂으려고 해요. 꽃병은 몇 개 필요한가요?" % (n, d)
        a, u = q, "개"
    elif k == "legs":
        legs = R.choice([2, 4])
        an = "닭" if legs == 2 else "강아지"
        n = legs * q
        t = "농장에 있는 %s의 다리를 세어 보니 모두 %d개였어요. %s 몇 마리인가요?" % (an, n, josa(an, "은/는"))
        a, u, d = q, "마리", legs
    else:
        t = "학생 %d명이 한 모둠에 %d명씩 모둠을 만들었어요. 모둠은 몇 개인가요?" % (n, d)
        a, u = q, "개"
    return mcq(t, "%d%s" % (a, u), ["%d%s" % (x, u) for x in (d, n - d, n + d, a + 1) if x != a and x > 0],
               "나눗셈으로 구해요. <b>%d ÷ %d = %d</b>(%s)" % (n, d, a, u))


unit("grade-3", "meaning-of-division", 4, "[4수01-05]",
     "나눗셈이 이루어지는 실생활 상황과 연결하여 나눗셈의 의미를 알고, 곱셈과 나눗셈의 관계를 이해한다.",
     "나눗셈의 뜻과 곱셈과의 관계", "나눗셈의 뜻",
     "초등 3학년 나눗셈 학습지: 똑같이 나누기, 몇 번 덜어 내기, 나눗셈식 읽기, 곱셈과 나눗셈의 관계, 곱셈구구로 몫 구하기, 문장제까지 100문제와 정답.",
     "곱셈구구로 몫을 찾아요", "□ × 4 = 24 → 24 ÷ 4 = 6",
     ["<b>똑같이 나누기</b>: 사과 12개를 3명에게 똑같이 나누면 한 명에게 4개씩이에요. 12 ÷ 3 = 4",
      "<b>몇 번 덜어 내기</b>: 사과 12개를 3개씩 덜어 내면 4번 덜어 낼 수 있어요. 이것도 12 ÷ 3 = 4예요.",
      "12 ÷ 3 = 4에서 4를 12를 3으로 나눈 <b>몫</b>이라고 해요.",
      "곱셈과 나눗셈은 관계가 있어요. 3 × 4 = 12이면 12 ÷ 3 = 4, 12 ÷ 4 = 3이에요. 그래서 <b>곱셈구구로 몫을 구할 수 있어요</b>."],
     [("35 ÷ 7 =", ["7단 곱셈구구에서 곱이 35인 것을 찾아요.", "7 × 5 = 35"], "5"),
      ("귤 24개를 한 봉지에 6개씩 담으면 몇 봉지가 되나요?", ["24에서 6씩 덜어 내요.", "24 ÷ 6 = 4"], "4봉지")],
     [("나누는 수와 몫을 바꾸어 쓴다", "24 ÷ 6 = 4에서 6은 나누는 수, 4는 몫이에요."),
      ("나눗셈 문제를 곱셈으로 푼다", "「똑같이 나누면」「몇 개씩 담으면」은 나눗셈이에요."),
      ("몫을 구하려고 계속 빼다가 횟수를 잘못 센다", "곱셈구구에서 곱이 나누어지는 수가 되는 수를 찾으면 빨라요.")],
     [("나눗셈은 언제 처음 배우나요?", "초등 3학년 1학기에 나눗셈의 뜻을 배워요. 곱셈구구를 이용해 몫을 구하고, 2학기에 몫과 나머지가 있는 나눗셈을 배워요."),
      ("똑같이 나누기와 덜어 내기는 무엇이 다른가요?", "똑같이 나누기는 몇 명(몇 묶음)에게 나눌지 알 때, 덜어 내기는 몇 개씩 나눌지 알 때예요. 둘 다 나눗셈식으로 나타내요.")],
     [("나눗셈식 읽기와 그림", [(read_eq, 10), (pic_groups, 10)]),
      ("똑같이 나누기와 덜어 내기", [(share, 10), (scoop, 10)]),
      ("곱셈과 나눗셈의 관계", [(relation, 20)]),
      ("곱셈구구로 몫 구하기", [(times_table, 14), (missing, 6)]),
      ("문장제", [(story, 14), (share, 3), (scoop, 3)])],
     82304)
