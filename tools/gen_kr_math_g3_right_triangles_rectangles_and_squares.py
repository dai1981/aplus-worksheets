# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：직각삼각형, 직사각형, 정사각형（2022 개정 [4수03-09] [4수03-10]）
誤答は「정사각형は 직사각형ではない」「기울어진 정사각형は 정사각형ではない」「직각이 하나라도 있으면 직사각형」から作る。
"""
import random
from kr_common import mcq, unit, josa
from kr_pics import grid_poly, poly, PT, fig, svg_wrap, line, text, INK, LIGHT

R = random.Random(82303)


def shape_kind():
    """모눈종이의 도형 → 이름"""
    k = R.choice(["rt", "rect", "sq", "sq_tilt", "tri", "quad"])
    x, y = R.randint(0, 2), R.randint(0, 2)
    if k == "rt":
        a, b = R.randint(2, 6), R.randint(2, 5)
        cells = R.choice([[(x, y), (x, y + b), (x + a, y + b)], [(x, y), (x + a, y), (x, y + b)], [(x + a, y), (x + a, y + b), (x, y + b)]])
        ans = "직각삼각형"
    elif k == "rect":
        a, b = R.randint(3, 7), R.randint(2, 4)
        if a == b:
            return None
        cells = [(x, y), (x + a, y), (x + a, y + b), (x, y + b)]
        ans = "직사각형"
    elif k == "sq":
        a = R.randint(2, 5)
        cells = [(x, y), (x + a, y), (x + a, y + a), (x, y + a)]
        ans = "정사각형"
    elif k == "sq_tilt":
        a, b = R.randint(1, 3), R.randint(1, 3)
        cells = [(x + a, y), (x + a + b, y + a), (x + b, y + a + b), (x, y + b)]
        ans = "정사각형"
    elif k == "tri":
        a, b = R.randint(3, 6), R.randint(2, 4)
        cells = [(x + R.randint(1, a - 1), y), (x + a, y + b), (x, y + b)]
        ans = "삼각형"
    else:
        a, b = R.randint(3, 6), R.randint(2, 4)
        d = R.randint(1, 2)
        cells = [(x + d, y), (x + a, y), (x + a + d, y + b), (x, y + b)]
        ans = "사각형"
    q = grid_poly(cells) + "모눈종이에 그린 도형의 이름으로 가장 알맞은 것은?"
    e = {"직각삼각형": "한 각이 직각인 삼각형이라 <b>직각삼각형</b>이에요.",
         "직사각형": "네 각이 모두 직각인 사각형이라 <b>직사각형</b>이에요. 네 변의 길이가 모두 같지는 않아요.",
         "정사각형": "네 각이 모두 직각이고 네 변의 길이가 모두 같아서 <b>정사각형</b>이에요." + (" 기울어져 있어도 정사각형이에요." if k == "sq_tilt" else ""),
         "삼각형": "직각이 없는 삼각형이에요. 그냥 <b>삼각형</b>이에요.",
         "사각형": "네 각이 모두 직각이 아니라서 직사각형이 아닌 <b>사각형</b>이에요."}[ans]
    w = {"직각삼각형": ["삼각형", "직사각형", "정사각형"], "직사각형": ["정사각형", "직각삼각형", "삼각형"],
         "정사각형": ["직사각형", "사각형", "직각삼각형"], "삼각형": ["직각삼각형", "직사각형", "사각형"],
         "사각형": ["직사각형", "정사각형", "직각삼각형"]}[ans]
    return mcq(q, ans, w, e)


FACTS = [("직사각형은 네 각이 모두 직각이에요.", True), ("정사각형은 네 변의 길이가 모두 같아요.", True),
         ("정사각형은 직사각형이라고 할 수 있어요.", True), ("직사각형은 정사각형이라고 할 수 있어요.", False),
         ("직각삼각형에는 직각이 2개 있어요.", False), ("직사각형은 마주 보는 두 변의 길이가 같아요.", True),
         ("직각삼각형은 직각이 1개인 삼각형이에요.", True), ("정사각형에는 직각이 2개 있어요.", False),
         ("직사각형은 꼭짓점이 4개예요.", True), ("직각이 1개만 있는 사각형도 직사각형이에요.", False),
         ("정사각형의 네 각은 모두 직각이에요.", True), ("삼각형에는 직각이 2개 있을 수 있어요.", False),
         ("기울어진 정사각형은 정사각형이 아니에요.", False), ("직사각형의 네 변의 길이는 항상 모두 같아요.", False)]


def fact():
    t, ok = R.choice(FACTS)
    q = "다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t
    why = {"정사각형은 직사각형이라고 할 수 있어요.": "정사각형은 네 각이 모두 직각이라서 직사각형이라고 할 수 있어요.",
           "직사각형은 정사각형이라고 할 수 있어요.": "직사각형은 네 변의 길이가 모두 같지 않을 수 있어서 정사각형이라고 할 수 없어요.",
           "기울어진 정사각형은 정사각형이 아니에요.": "놓인 방향과 상관없이 네 각이 직각이고 네 변이 같으면 정사각형이에요."}.get(t, "직각삼각형은 직각 1개, 직사각형은 직각 4개, 정사각형은 직각 4개와 같은 길이의 네 변을 가져요.")
    return mcq(q, "○" if ok else "×", ["×" if ok else "○", "알 수 없어요", "도형에 따라 달라요"], why)


def sides():
    k = R.choice(["sq", "rect"])
    if k == "sq":
        a = R.randint(3, 15)
        labs = R.sample(PT, 4)
        f = poly([(60, 30), (180, 30), (180, 150), (60, 150)], labs, right=(0, 1, 2, 3), H=190, W=240,
                 extra=text(120, 22, "%d cm" % a, 18))
        if R.random() < 0.5:
            return mcq(f + "정사각형 %s의 변 %s%s의 길이는 몇 cm인가요?" % ("".join(labs), labs[2], labs[3]), "%d cm" % a,
                       ["%d cm" % x for x in (a * 2, a * 4, a + 1, a - 1) if x > 0],
                       "정사각형은 네 변의 길이가 모두 같아요. <b>%d cm</b>" % a)
        return mcq(f + "정사각형 %s의 네 변의 길이를 모두 더하면 몇 cm인가요?" % "".join(labs), "%d cm" % (a * 4),
                   ["%d cm" % x for x in (a * 2, a, a * 3, a + 4)],
                   "네 변의 길이가 모두 %d cm이니까 %d + %d + %d + %d = <b>%d</b>(cm)" % (a, a, a, a, a, a * 4))
    a, b = R.randint(5, 15), R.randint(2, 9)
    if a == b:
        return None
    labs = R.sample(PT, 4)
    f = poly([(30, 40), (210, 40), (210, 140), (30, 140)], labs, right=(0, 1, 2, 3), H=180, W=240,
             extra=text(120, 32, "%d cm" % a, 18) + text(228, 95, "%d cm" % b, 18, anchor="start"))
    f = f.replace("viewBox='0 0 240 180' width='240'", "viewBox='0 0 290 180' width='290'")
    if R.random() < 0.5:
        return mcq(f + "직사각형 %s에서 변 %s%s의 길이는 몇 cm인가요?" % ("".join(labs), labs[3], labs[2]), "%d cm" % a,
                   ["%d cm" % x for x in (b, a + b, a * 2, a - b) if x > 0],
                   "직사각형은 마주 보는 두 변의 길이가 같아요. 변 %s%s은 변 %s%s과 마주 보니까 <b>%d cm</b>" % (labs[3], labs[2], labs[0], labs[1], a))
    return mcq(f + "직사각형 %s의 네 변의 길이를 모두 더하면 몇 cm인가요?" % "".join(labs), "%d cm" % (2 * (a + b)),
               ["%d cm" % x for x in (a + b, a * b, 2 * a + b, 4 * a)],
               "마주 보는 변의 길이가 같아요. %d + %d + %d + %d = <b>%d</b>(cm)" % (a, b, a, b, 2 * (a + b)))


def count_rects():
    n = R.randint(2, 5)
    w = 60
    W = 20 + n * w + 20
    s = "<rect x='20' y='20' width='%d' height='70' fill='%s' stroke='%s' stroke-width='3'/>" % (n * w, LIGHT, INK)
    for i in range(1, n):
        s += line(20 + i * w, 20, 20 + i * w, 90, INK, 3)
    ans = n * (n + 1) // 2
    q = fig(svg_wrap(W, 110, s, "작은 직사각형 %d개로 나눈 큰 직사각형" % n)) + "큰 직사각형을 작은 직사각형 %d개로 나누었어요. 그림에서 찾을 수 있는 직사각형은 모두 몇 개인가요?" % n
    return mcq(q, "%d개" % ans, ["%d개" % x for x in (n, n + 1, ans + 1, ans - 1) if x != ans and x > 0],
               "작은 것 %d개, 두 칸짜리 %d개 …처럼 크기별로 세어 더해요. %s = <b>%d</b>(개)" % (n, n - 1, " + ".join(str(n - i) for i in range(n)), ans))


def cut_squares():
    c = R.choice([2, 3, 4, 5])
    m, k = R.randint(2, 6), R.randint(1, 4)
    a, b = c * m, c * k
    if a == b:
        return None
    ans = m * k
    q = "가로 %d cm, 세로 %d cm인 직사각형 모양 종이를 남는 부분 없이 잘라 한 변이 %d cm인 정사각형을 만들려고 해요. 정사각형을 몇 개 만들 수 있나요?" % (a, b, c)
    return mcq(q, "%d개" % ans, ["%d개" % x for x in (m + k, m, k, ans * 2) if x != ans and x > 0],
               "가로로 %d ÷ %d = %d개, 세로로 %d ÷ %d = %d줄 만들 수 있어요. %d × %d = <b>%d</b>(개)" % (a, c, m, b, c, k, m, k, ans))


def square_from_rect():
    a = R.randint(5, 16)
    b = R.randint(2, a - 1)
    q = "가로 %d cm, 세로 %d cm인 직사각형 모양 종이를 한 번 잘라서 가장 큰 정사각형을 만들었어요. 이 정사각형의 한 변은 몇 cm인가요?" % (a, b)
    return mcq(q, "%d cm" % b, ["%d cm" % x for x in (a, a - b, a + b, b + 1) if x != b and x > 0],
               "정사각형은 네 변이 모두 같아야 하므로, 짧은 변 %d cm에 맞추어 잘라요. 한 변은 <b>%d cm</b>이고 남는 부분은 가로 %d cm예요." % (b, b, a - b))


unit("grade-3", "right-triangles-rectangles-and-squares", 3, "[4수03-09] [4수03-10]",
     "여러 가지 모양의 삼각형에 대한 분류 활동을 통하여 직각삼각형, 예각삼각형, 둔각삼각형을 이해한다. 여러 가지 모양의 사각형에 대한 분류 활동을 통하여 직사각형, 정사각형, 사다리꼴, 평행사변형, 마름모를 이해하고, 그 성질을 탐구하고 설명할 수 있다.",
     "직각삼각형, 직사각형, 정사각형", "직각삼각형, 직사각형, 정사각형",
     "초등 3학년 평면도형 학습지: 직각삼각형, 직사각형, 정사각형 찾기, 성질 ○× 문제, 변의 길이, 직사각형 세기, 종이 자르기 문제까지 100문제와 정답.",
     "직각이 몇 개이고 변이 같은가", "정사각형은 직사각형이라고 할 수 있어요.",
     ["한 각이 직각인 삼각형은 <b>직각삼각형</b>이에요.",
      "네 각이 모두 직각인 사각형은 <b>직사각형</b>이에요. 마주 보는 두 변의 길이가 같아요.",
      "네 각이 모두 직각이고 네 변의 길이가 모두 같은 사각형은 <b>정사각형</b>이에요.",
      "정사각형은 네 각이 모두 직각이라서 <b>직사각형이라고 할 수 있어요</b>. 하지만 직사각형을 모두 정사각형이라고 할 수는 없어요."],
     [("가로 8 cm, 세로 5 cm인 직사각형의 네 변의 길이의 합은?", ["마주 보는 변의 길이가 같아요.", "8 + 5 + 8 + 5 = 26"], "26 cm"),
      ("한 변이 7 cm인 정사각형의 네 변의 길이의 합은?", ["네 변이 모두 7 cm예요.", "7 + 7 + 7 + 7 = 28"], "28 cm")],
     [("기울여 놓은 정사각형은 정사각형이 아니라고 한다", "놓인 방향과 상관없이 네 각과 네 변을 확인해요."),
      ("정사각형은 직사각형이 아니라고 한다", "정사각형도 네 각이 모두 직각이니까 직사각형이에요."),
      ("직각이 하나 있는 사각형을 직사각형이라고 한다", "직사각형은 네 각이 모두 직각이어야 해요.")],
     [("정사각형과 직사각형은 어떻게 다른가요?", "둘 다 네 각이 모두 직각이에요. 정사각형은 네 변의 길이가 모두 같고, 직사각형은 마주 보는 두 변의 길이만 같으면 돼요."),
      ("직각인지 어떻게 확인하나요?", "종이를 반듯하게 두 번 접어 만든 직각이나 삼각자의 직각 부분을 대어 보세요. 꼭 맞으면 직각이에요.")],
     [("도형의 이름", [(shape_kind, 20)]),
      ("도형의 성질 ○×", [(fact, 14), (shape_kind, 6)]),
      ("변의 길이", [(sides, 20)]),
      ("직사각형 세기와 정사각형 만들기", [(count_rects, 4), (cut_squares, 10), (square_from_rect, 6)]),
      ("문장제", [(sides, 6), (cut_squares, 8), (square_from_rect, 6)])],
     82303)
