# -*- coding: utf-8 -*-
"""
대한민국 초등 4학년 수학：자료와 가능성
  bar  : 막대그래프 [4수04-01]
  line : 꺾은선그래프 [4수04-02] [4수04-03]
誤答は「눈금 한 칸을 1로 읽는다」「막대의 칸 수를 값으로 쓴다」「변화가 가장 큰 때를 값이 가장 큰 때로 고른다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa, num, unit_josa as J
from kr_pics import fig, svg_wrap, text, line, INK, RED, BLUE

R = random.Random(82409)
NM = Names(R)
GRID = "#cfd8d3"

TOPICS = [("좋아하는 과일", "과일", ["사과", "배", "포도", "귤", "딸기", "수박"], "명"),
          ("좋아하는 운동", "운동", ["축구", "야구", "농구", "수영", "줄넘기", "배구"], "명"),
          ("반별 학생 수", "반", ["1반", "2반", "3반", "4반", "5반"], "명"),
          ("마을별 나무 수", "마을", ["가 마을", "나 마을", "다 마을", "라 마을", "마 마을"], "그루"),
          ("좋아하는 계절", "계절", ["봄", "여름", "가을", "겨울"], "명"),
          ("요일별 도서관 방문자 수", "요일", ["월", "화", "수", "목", "금"], "명"),
          ("모둠별 모은 빈 병 수", "모둠", ["가", "나", "다", "라", "마"], "개"),
          ("좋아하는 동물", "동물", ["강아지", "고양이", "토끼", "햄스터", "앵무새"], "명")]


def bar_svg(title, cats, vals, step, u, horiz=False):
    top = max(vals)
    ncell = -(-top // step) + 1
    W, H = 520, 320
    s = [text(W / 2, 24, "%s (단위: %s)" % (title, u), 18)]
    if not horiz:
        x0, y0, x1, y1 = 70, 290, 500, 44
        ch = (y0 - y1) / float(ncell)
        for i in range(ncell + 1):
            y = y0 - i * ch
            s.append(line(x0, y, x1, y, GRID if i else INK, 1 if i else 2))
            if i % next(k for k in (1, 2, 5, 10, 20) if ncell / k <= 7) == 0:
                s.append(text(x0 - 10, y + 6, num(i * step), 17, anchor="end"))
        s.append(line(x0, y0, x0, y1, INK, 2))
        bw = (x1 - x0) / float(len(cats))
        for i, (c, v) in enumerate(zip(cats, vals)):
            bx = x0 + i * bw + bw * 0.22
            hgt = v / float(step) * ch
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#7cc2a0' stroke='%s' stroke-width='1.5'/>" % (bx, y0 - hgt, bw * 0.56, hgt, INK))
            s.append(text(bx + bw * 0.28, y0 + 26, c, 17))
        H = 320
    else:
        x0, y0, x1, y1 = 90, 50, 500, 50 + 40 * len(cats)
        cw = (x1 - x0) / float(ncell)
        for i in range(ncell + 1):
            x = x0 + i * cw
            s.append(line(x, y0, x, y1, GRID if i else INK, 1 if i else 2))
            if i % next(k for k in (1, 2, 5, 10, 20) if ncell / k <= 7) == 0:
                s.append(text(x, y1 + 24, num(i * step), 17))
        s.append(line(x0, y1, x1, y1, INK, 2))
        for i, (c, v) in enumerate(zip(cats, vals)):
            by = y0 + i * 40 + 9
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='22' fill='#7cc2a0' stroke='%s' stroke-width='1.5'/>" % (x0, by, v / float(step) * cw, INK))
            s.append(text(x0 - 10, by + 17, c, 17, anchor="end"))
        H = y1 + 38
    return fig(svg_wrap(W, H, "".join(s), title + " 막대그래프").replace("<svg ", "<svg data-pf='lg' ", 1))


def bar_data():
    title, axis, cats, u = R.choice(TOPICS)
    n = min(len(cats), R.choice([4, 5]))
    cats = cats[:n]
    step = R.choice([1, 2, 2, 5, 10])
    vals = R.sample(range(1, 14 if step < 10 else 10), n)
    vals = [v * step for v in vals]
    return title, axis, cats, vals, step, u


def bar_q():
    title, axis, cats, vals, step, u = bar_data()
    pic = bar_svg(title, cats, vals, step, u, horiz=R.random() < 0.35)
    k = R.choice(["read", "max", "min", "diff", "sum", "cell", "times"])
    i = R.randrange(len(cats))
    if k == "read":
        v = vals[i]
        return mcq(pic + "막대그래프에서 %s 몇 %s인가요?" % (josa(cats[i], "은/는"), u), "%s%s" % (num(v), u),
                   ["%s%s" % (num(v // step), u) if step > 1 else "%s%s" % (num(v + 1), u), "%s%s" % (num(v + step), u), "%s%s" % (num(v - step), u) if v > step else "%s%s" % (num(v + 2 * step), u)],
                   "눈금 한 칸은 %s. 막대가 %d칸이니까 <b>%s</b>%s." % (J(num(step) + u, "이에요/예요"), v // step, num(v) + u, J(num(v) + u, "이에요/예요")[len(num(v) + u):]))
    if k in ("max", "min"):
        j = vals.index(max(vals) if k == "max" else min(vals))
        return mcq(pic + "막대그래프에서 수량이 가장 %s %s 무엇인가요?" % ("많은" if k == "max" else "적은", J(axis, "은/는")), cats[j], [c for c in cats if c != cats[j]],
                   "막대의 길이가 가장 %s 것을 찾아요. <b>%s</b>" % ("긴" if k == "max" else "짧은", cats[j]))
    if k == "diff":
        a, b = R.sample(range(len(cats)), 2)
        if vals[a] < vals[b]:
            a, b = b, a
        d = vals[a] - vals[b]
        return mcq(pic + "%s %s보다 몇 %s 더 많은가요?" % (J(cats[a], "은/는"), cats[b], u), "%s%s" % (num(d), u),
                   ["%s%s" % (num(d // step), u) if step > 1 else "%s%s" % (num(d + 2), u), "%s%s" % (num(vals[a] + vals[b]), u), "%s%s" % (num(d + step), u)],
                   "%s − %s = <b>%s%s</b>" % (num(vals[a]), num(vals[b]), num(d), u))
    if k == "sum":
        t = sum(vals)
        return mcq(pic + "조사한 %s 모두 몇 %s인가요?" % ("수는", u), "%s%s" % (num(t), u), ["%s%s" % (num(t - vals[0]), u), "%s%s" % (num(t // step), u) if step > 1 else "%s%s" % (num(t + 1), u), "%s%s" % (num(t + step), u)],
                       "막대가 나타내는 수를 모두 더해요. %s = <b>%s%s</b>" % (" + ".join(num(v) for v in vals), num(t), u))
    if k == "cell":
        return mcq(pic + "눈금 한 칸은 몇 %s 나타내나요?" % J(u, "을/를"), "%s%s" % (num(step), u), ["%s%s" % (num(x), u) for x in (1 if step != 1 else 2, step * 2, 5 if step != 5 else 10)],
                   "눈금에 쓰인 수를 보면 한 칸은 <b>%s</b>%s." % (num(step) + u, J(num(step) + u, "이에요/예요")[len(num(step) + u):]))
    a, b = R.sample(range(len(cats)), 2)
    if vals[a] % vals[b] or vals[a] == vals[b]:
        return None
    t = vals[a] // vals[b]
    return mcq(pic + "%s %s의 몇 배인가요?" % (J(cats[a], "은/는"), cats[b]), "%d배" % t, ["%d배" % x for x in (t + 1, t - 1 if t > 2 else t + 2, vals[a] - vals[b])],
               "%s ÷ %s = <b>%d배</b>" % (num(vals[a]), num(vals[b]), t))


def bar_table():
    title, axis, cats, vals, step, u = bar_data()
    total = sum(vals)
    i = R.randrange(len(cats))
    cells = "".join("<td>%s</td>" % (num(v) if j != i else "□") for j, v in enumerate(vals))
    tb = "<div class='sn-tw'><table class='sn-table'><thead><tr><th>%s</th>%s<th>합계</th></tr></thead><tbody><tr><td>%s(%s)</td>%s<td>%s</td></tr></tbody></table></div>" % (
        axis, "".join("<th>%s</th>" % c for c in cats), u if u != "명" else "학생 수", u, cells, num(total))
    v = vals[i]
    if R.random() < 0.5:
        return mcq(tb + "표의 □에 알맞은 수는?", num(v), [num(total), num(v + step), num(abs(v - step)) if v != step else num(v + 2 * step)],
                   "합계에서 나머지를 빼요. %s − %s = <b>%s</b>" % (num(total), num(total - v), num(v)))
    return mcq(tb + "□의 값을 구해 막대그래프로 나타낼 때, 세로 눈금 한 칸이 %s%s이면 %s의 막대는 몇 칸인가요?" % (num(step), u, cats[i]), "%d칸" % (v // step),
               ["%d칸" % x for x in (v, v // step + 1, v // step - 1 if v // step > 1 else v // step + 2) if x != v // step],
               "□ = %s이고, %s ÷ %s = <b>%d칸</b>이에요." % (num(v), num(v), num(step), v // step))


BAR_FACTS = [("막대그래프는 조사한 자료의 수량을 막대의 길이로 나타낸 그래프예요.", "○"),
             ("막대그래프에서 막대의 길이가 길수록 수량이 많아요.", "○"),
             ("막대그래프는 시간에 따른 변화를 나타내기에 가장 알맞아요.", "×"),
             ("표는 각 항목의 수와 합계를 알기 쉬워요.", "○"),
             ("막대그래프는 항목별 크기를 한눈에 비교하기 쉬워요.", "○"),
             ("막대그래프의 눈금 한 칸은 항상 1을 나타내요.", "×"),
             ("가로 막대그래프와 세로 막대그래프는 나타내는 방법이 달라도 같은 자료를 나타낼 수 있어요.", "○")]


def bar_fact():
    t, a = R.choice(BAR_FACTS)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "자료에 따라 달라요"],
               "막대그래프는 수량을 막대 길이로 나타내어 크기 비교가 쉬워요. 변화는 꺾은선그래프가 알맞아요.")


# ---------------------------------------------------------------- 꺾은선그래프
SERIES = [("교실의 온도", "시각", ["오전 9시", "10시", "11시", "12시", "오후 1시", "2시"], "°C", 10, 30, 1),
          ("강낭콩의 키", "날짜", ["1일", "2일", "3일", "4일", "5일", "6일"], "cm", 0, 20, 1),
          ("월별 강수량", "월", ["3월", "4월", "5월", "6월", "7월", "8월"], "mm", 0, 300, 20),
          ("연도별 마을 인구", "연도", ["2019", "2020", "2021", "2022", "2023", "2024"], "명", 200, 400, 10),
          ("요일별 줄넘기 기록", "요일", ["월", "화", "수", "목", "금"], "회", 20, 80, 2),
          ("강아지의 무게", "월", ["1월", "2월", "3월", "4월", "5월", "6월"], "kg", 0, 12, 1)]


def series():
    title, axis, xs, u, lo, hi, step = R.choice(SERIES)
    n = len(xs)
    k = R.choice(["up", "mix"])
    base = R.randint(lo // step + 1, (lo + (hi - lo) // 3) // step)
    vals = [base]
    for i in range(n - 1):
        dv = R.randint(0, 4) if title in ("강낭콩의 키", "강아지의 무게") or k == "up" else R.randint(-3, 4)
        vals.append(max(lo // step + 1, vals[-1] + dv))
    vals = [v * step for v in vals]
    if len(set(vals)) < 3 or max(vals) > hi:
        return None
    return title, axis, xs, u, lo, step, vals


def line_svg(title, xs, vals, u, lo, step, wave=False):
    vmin = (min(vals) // step) * step if wave else lo
    vmax = max(vals)
    nc = (vmax - vmin) // step + 1
    W, H = 520, 330
    x0, y0, x1, y1 = 70, 290, 500, 44
    ch = (y0 - y1) / float(nc)
    s = [text(W / 2, 24, "%s (단위: %s)" % (title, u), 18)]
    lab_every = next(k for k in (1, 2, 5, 10, 20) if nc / k <= 7)
    for i in range(nc + 1):
        y = y0 - i * ch
        s.append(line(x0, y, x1, y, GRID if i else INK, 1 if i else 2))
        if i % lab_every == 0:
            s.append(text(x0 - 10, y + 6, num(vmin + i * step), 17, anchor="end"))
    s.append(line(x0, y0, x0, y1, INK, 2))
    if wave and vmin > 0:
        s.append("<path d='M%d %d q6 -6 12 0 t12 0' fill='none' stroke='%s' stroke-width='2'/>" % (x0 - 12, y0 - ch / 2, INK))
        s.append("<rect x='%d' y='%d' width='8' height='%d' fill='#fff'/>" % (x0 - 4, y0 - ch / 2 - 4, 8))
        s.append(line(x0, y0, x0, y0 - ch / 2 + 4, INK, 2) + line(x0, y0 - ch / 2 - 4, x0, y1, INK, 2))
    bw = (x1 - x0) / float(len(xs))
    pts = []
    for i, (c, v) in enumerate(zip(xs, vals)):
        x = x0 + bw * (i + 0.5)
        y = y0 - (v - vmin) / float(step) * ch
        pts.append((x, y))
        s.append(line(x, y0, x, y1, GRID, 1))
        s.append(text(x, y0 + 26, c, 16))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join("%.1f,%.1f" % p for p in pts), RED))
    for p in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (p[0], p[1], RED))
    return fig(svg_wrap(W, H, "".join(s), title + " 꺾은선그래프").replace("<svg ", "<svg data-pf='lg' ", 1))


def line_q():
    d = series()
    if not d:
        return None
    title, axis, xs, u, lo, step, vals = d
    wave = R.random() < 0.4 and min(vals) - lo > 3 * step
    pic = line_svg(title, xs, vals, u, lo, step, wave)
    k = R.choice(["read", "rise", "most", "fall", "diff", "mid", "max"])
    i = R.randrange(len(xs))
    us = lambda v: "%s%s" % (num(v), " " + u if u in ("cm", "mm", "kg") else u)
    if k == "read":
        v = vals[i]
        return mcq(pic + "%s의 %s 얼마인가요?" % (xs[i], josa(title.split()[-1], "은/는")),
                   us(v), [us(v + step), us(v - step) if v > step else us(v + 2 * step), us(vals[i - 1]) if vals[i - 1] != v else us(v + 3 * step)],
                   "세로 눈금 한 칸은 %s. <b>%s</b>" % (J(us(step), "이에요/예요"), us(v)))
    diffs = [vals[j + 1] - vals[j] for j in range(len(vals) - 1)]
    names = ["%s %s 사이" % (J(xs[j], "과/와"), xs[j + 1]) for j in range(len(vals) - 1)]
    if k == "most":
        m = max(diffs)
        if diffs.count(m) > 1 or m <= 0:
            return None
        j = diffs.index(m)
        others = [names[x] for x in range(len(names)) if x != j]
        return mcq(pic + "%s 가장 많이 늘어난 때는 언제인가요?" % josa(title.split()[-1], "이/가"), names[j], R.sample(others, min(3, len(others))),
                   "선이 가장 많이 기울어진 곳을 찾아요. %s 늘어난 <b>%s</b>예요." % (us(m), names[j]))
    if k == "fall":
        m = min(diffs)
        if m >= 0 or diffs.count(m) > 1:
            return None
        j = diffs.index(m)
        others = [names[x] for x in range(len(names)) if x != j]
        return mcq(pic + "%s 가장 많이 줄어든 때는 언제인가요?" % josa(title.split()[-1], "이/가"), names[j], R.sample(others, min(3, len(others))),
                   "선이 오른쪽 아래로 가장 많이 기울어진 곳이에요. <b>%s</b>" % names[j])
    if k in ("rise", "diff"):
        a, b = sorted(R.sample(range(len(xs)), 2))
        d = vals[b] - vals[a]
        if d == 0:
            return None
        word = ("올랐" if d > 0 else "내렸") if u == "°C" else ("늘었" if d > 0 else "줄었")
        return mcq(pic + "%s부터 %s까지 %s 몇 %s %s나요?" % (xs[a], xs[b], josa(title.split()[-1], "은/는"), u, word), us(abs(d)),
                   [us(vals[a] + vals[b]), us(abs(d) + step), us(abs(d) - step) if abs(d) > step else us(abs(d) + 2 * step)],
                   "%s − %s = <b>%s</b> %s어요." % (num(max(vals[a], vals[b])), num(min(vals[a], vals[b])), us(abs(d)), word))
    if k == "mid":
        j = R.randrange(len(xs) - 1)
        if (vals[j] + vals[j + 1]) % 2 or vals[j] == vals[j + 1]:
            return None
        m = (vals[j] + vals[j + 1]) // 2
        if title not in ("교실의 온도", "강낭콩의 키", "강아지의 무게"):
            return None
        return mcq(pic + "%s %s의 중간에는 %s 얼마였을까요? (두 점 사이가 고르게 변했다고 생각해요)" % (J(xs[j], "과/와"), xs[j + 1], josa(title.split()[-1], "이/가")), us(m),
                   [us(vals[j] + vals[j + 1]), us(m + step) if (m + step) != vals[j + 1] else us(m + 2 * step), us(max(vals[j], vals[j + 1]) + step)],
                   "두 점의 가운데 값을 읽어요. (%s + %s) ÷ 2 = <b>%s</b>" % (num(vals[j]), num(vals[j + 1]), us(m)))
    m = max(vals)
    if vals.count(m) > 1:
        return None
    j = vals.index(m)
    return mcq(pic + "%s 가장 큰 때는 언제인가요?" % josa(title.split()[-1], "이/가"), xs[j], [x for x in xs if x != xs[j]][:4],
               "점이 가장 높은 곳이에요. <b>%s</b>" % xs[j])


LINE_FACTS = [("꺾은선그래프는 시간에 따라 변하는 모양을 알아보기 쉬워요.", "○"),
              ("꺾은선그래프에서 선이 많이 기울어질수록 변화가 커요.", "○"),
              ("물결선은 필요 없는 부분을 줄여서 나타낼 때 써요.", "○"),
              ("반별 학생 수를 비교할 때는 꺾은선그래프가 가장 알맞아요.", "×"),
              ("하루 동안의 기온 변화는 꺾은선그래프로 나타내면 좋아요.", "○"),
              ("꺾은선그래프에서 선분이 오른쪽 아래로 내려가면 값이 늘어난 거예요.", "×"),
              ("꺾은선그래프로 조사하지 않은 중간 시각의 값을 어림할 수 있어요.", "○"),
              ("물결선을 쓰면 세로 눈금 한 칸의 크기를 작게 하여 변화를 더 잘 볼 수 있어요.", "○")]


def line_fact():
    t, a = R.choice(LINE_FACTS)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "자료에 따라 달라요"],
               "꺾은선그래프는 시간에 따른 변화를 선으로 나타내요. 물결선으로 필요 없는 부분을 줄일 수 있어요.")


CHOOSE = [("하루 동안 운동장의 기온 변화", "꺾은선그래프"), ("우리 반 학생들이 좋아하는 색깔", "막대그래프"), ("강낭콩이 날마다 자란 키", "꺾은선그래프"),
          ("반별 안경을 쓴 학생 수", "막대그래프"), ("월별 우리 집 전기 사용량의 변화", "꺾은선그래프"), ("나라별 금메달 수", "막대그래프"),
          ("1년 동안 내 몸무게의 변화", "꺾은선그래프"), ("마을별 쓰레기 배출량 비교", "막대그래프"), ("시각별 그림자 길이의 변화", "꺾은선그래프"),
          ("좋아하는 간식별 학생 수", "막대그래프")]


def choose_graph():
    t, a = R.choice(CHOOSE)
    return mcq("「%s」를 나타내기에 더 알맞은 그래프는?" % t, a, ["막대그래프" if a == "꺾은선그래프" else "꺾은선그래프", "그림그래프만 쓸 수 있어요", "그래프로 나타낼 수 없어요"],
               "항목끼리 크기를 비교하면 막대그래프, 시간에 따른 변화를 보면 꺾은선그래프가 알맞아요. <b>%s</b>" % a)


def build(which):
    G = "grade-4"
    if which == "bar":
        return unit(G, "bar-graphs", 9, "[4수04-01]",
                    "탐구 질문을 설정하여 자료를 수집하고, 자료를 막대그래프로 나타내고 해석할 수 있다.",
                    "막대그래프 읽고 나타내기", "막대그래프",
                    "초등 4학년 막대그래프 학습지: 눈금 한 칸의 크기, 막대그래프 읽기, 가장 많은 것과 적은 것, 차와 합, 표를 막대그래프로 나타내기까지 100문제와 정답.",
                    "눈금 한 칸의 크기부터 확인", "막대의 길이로 수량을 비교해요.",
                    ["<b>막대그래프</b>는 조사한 자료의 수량을 막대의 길이로 나타낸 그래프예요.",
                     "먼저 <b>눈금 한 칸이 얼마인지</b> 확인하고, 막대가 몇 칸인지 세어 값을 구해요.",
                     "막대의 길이를 비교하면 가장 많은 것과 가장 적은 것을 한눈에 알 수 있어요.",
                     "막대그래프로 나타낼 때는 가로와 세로에 무엇을 나타낼지 정하고, 가장 큰 값까지 나타낼 수 있게 눈금을 정해요."],
                    [("눈금 한 칸이 2명이고 막대가 7칸이면?", ["2 × 7 = 14"], "14명")],
                    [("눈금 한 칸을 1로 읽는다", "세로 눈금에 쓰인 수를 보고 한 칸의 크기를 먼저 구해요."),
                     ("막대의 칸 수를 그대로 답으로 쓴다", "칸 수 × 한 칸의 크기를 해요."),
                     ("차를 구할 때 두 값을 더한다", "몇 명 더 많은지는 뺄셈으로 구해요.")],
                    [("그림그래프와 막대그래프는 어떻게 다른가요?", "그림그래프는 그림의 크기와 개수로, 막대그래프는 막대의 길이로 수량을 나타내요."),
                     ("막대그래프는 언제 배우나요?", "초등 4학년 1학기 「막대그래프」 단원에서 배워요.")],
                    [("막대그래프 읽기", [(bar_q, 20)]),
                     ("비교하기", [(bar_q, 20)]),
                     ("표와 막대그래프", [(bar_table, 20)]),
                     ("막대그래프의 성질", [(bar_fact, 6), (bar_q, 14)]),
                     ("섞어서 연습", [(bar_q, 12), (bar_table, 8)])], 82409)
    return unit(G, "line-graphs", 19, "[4수04-02] [4수04-03]",
                "탐구 질문을 설정하여 자료를 수집하고, 자료를 꺾은선그래프로 나타내고 해석할 수 있다. 자료를 수집하여 탐구 질문에 맞는 그래프로 나타내고 해석할 수 있다.",
                "꺾은선그래프 읽고 해석하기", "꺾은선그래프",
                "초등 4학년 2학기 꺾은선그래프 학습지: 꺾은선그래프 읽기, 가장 많이 늘어난 때와 줄어든 때, 변화량, 중간값 어림, 물결선, 알맞은 그래프 고르기까지 100문제와 정답.",
                "선의 기울기로 변화를 읽어요", "변화는 꺾은선, 비교는 막대",
                ["<b>꺾은선그래프</b>는 수량을 점으로 찍고 그 점들을 선분으로 이은 그래프예요. 시간에 따른 변화를 알아보기 쉬워요.",
                 "선분이 많이 기울어질수록 변화가 커요. 오른쪽 위로 가면 늘어나고, 오른쪽 아래로 가면 줄어들어요.",
                 "필요 없는 부분은 <b>물결선</b>으로 줄여서 나타내면 변화를 더 잘 볼 수 있어요.",
                 "항목끼리 비교할 때는 막대그래프, 변화를 볼 때는 꺾은선그래프가 알맞아요."],
                [("오전 10시 18°C, 오전 11시 22°C이면 10시 30분의 온도는 약 몇 도?", ["두 점의 가운데", "(18 + 22) ÷ 2 = 20"], "약 20°C")],
                [("값이 가장 큰 때를 가장 많이 늘어난 때로 고른다", "변화량은 이웃한 두 점의 차로 구해요."),
                 ("물결선 아래의 눈금을 0부터 센다", "물결선이 있으면 세로 눈금에 쓰인 수를 확인해요."),
                 ("모든 자료를 꺾은선그래프로 나타낸다", "항목별 비교는 막대그래프가 알맞아요.")],
                [("꺾은선그래프는 언제 배우나요?", "초등 4학년 2학기 「꺾은선그래프」 단원에서 배워요."),
                 ("물결선은 왜 쓰나요?", "필요 없는 아래쪽 눈금을 줄여서 세로 눈금 한 칸을 작게 하면 변화가 더 잘 보여요.")],
                [("꺾은선그래프 읽기", [(line_q, 20)]),
                 ("변화 알아보기", [(line_q, 20)]),
                 ("꺾은선그래프의 성질", [(line_fact, 8), (line_q, 12)]),
                 ("알맞은 그래프", [(choose_graph, 10), (line_q, 10)]),
                 ("섞어서 연습", [(line_q, 20)])], 82419)
