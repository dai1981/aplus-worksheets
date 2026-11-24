# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：자료의 정리와 그림그래프（2022 개정 [4수04-01]）
誤答は「큰 그림과 작은 그림を同じ数として数える」「합계を間違える」「가장 많은 것と적은 것の取り違え」から作る。
"""
import random
from kr_common import mcq, unit, num, josa
from kr_pics import pic_graph
from kr_common import table

R = random.Random(82320)

SCENES = [("마을별 사과 생산량", ["가 마을", "나 마을", "다 마을", "라 마을"], "상자", 100, 10, "상자"),
          ("반별 모은 빈 병의 수", ["1반", "2반", "3반", "4반"], "병", 10, 1, "개"),
          ("마을별 학생 수", ["햇빛 마을", "별빛 마을", "달빛 마을", "바람 마을"], "명", 100, 10, "명"),
          ("목장별 우유 생산량", ["푸른 목장", "하늘 목장", "들판 목장", "숲속 목장"], "L", 100, 10, "L"),
          ("가게별 하루 동안 팔린 붕어빵 수", ["가 가게", "나 가게", "다 가게", "라 가게"], "개", 10, 1, "개"),
          ("과수원별 귤 생산량", ["동쪽 과수원", "서쪽 과수원", "남쪽 과수원", "북쪽 과수원"], "상자", 10, 1, "상자"),
          ("동네별 도서관 이용자 수", ["가 동", "나 동", "다 동", "라 동"], "명", 100, 10, "명")]


def scene():
    title, names, u1, big, small, u = R.choice(SCENES)
    vals = []
    for _ in range(4):
        v = R.randint(1, 4) * big + R.randint(0, 9) * small
        vals.append(v)
    if len(set(vals)) < 4:
        return None
    rows = list(zip(names, vals))
    return title, rows, big, small, u


def unit_word(u):
    return "" if u == "L" else ""


def fmt(v, u):
    return "%s %s" % (num(v), u) if u == "L" else "%s%s" % (num(v), u)


def read_one():
    sc = scene()
    if not sc:
        return None
    title, rows, big, small, u = sc
    nm, v = R.choice(rows)
    f = pic_graph(rows, big, small, " " + u if u == "L" else u, title)
    nb, ns = divmod(v, big)
    ns //= small
    return mcq(f + "%s %s?" % (josa(nm, "은/는"), "몇 " + u + "인가요" if u != "L" else "몇 L인가요"), fmt(v, u),
               [fmt(nb + ns, u), fmt(nb * big + ns * small * 10, u) if ns else fmt(v + big, u), fmt(v + small, u), fmt(ns * big + nb * small, u) if ns else fmt(v + 2 * small, u)],
               "큰 그림은 %s, 작은 그림은 %s이에요. 큰 그림 %d개, 작은 그림 %d개이니까 <b>%s</b>" % (fmt(big, u), fmt(small, u), nb, ns, fmt(v, u)))


def most_least():
    sc = scene()
    if not sc:
        return None
    title, rows, big, small, u = sc
    f = pic_graph(rows, big, small, " " + u if u == "L" else u, title)
    k = R.choice(["most", "least"])
    srt = sorted(rows, key=lambda x: x[1])
    ans = srt[-1][0] if k == "most" else srt[0][0]
    return mcq(f + "그림그래프에서 %s 곳은 어디인가요?" % ("가장 많은" if k == "most" else "가장 적은"), ans, [r[0] for r in rows if r[0] != ans],
               "큰 그림의 수를 먼저 비교하고, 같으면 작은 그림의 수를 비교해요. <b>%s</b>" % ans)


def total_diff():
    sc = scene()
    if not sc:
        return None
    title, rows, big, small, u = sc
    f = pic_graph(rows, big, small, " " + u if u == "L" else u, title)
    k = R.choice(["total", "diff", "two"])
    if k == "total":
        t = sum(v for _, v in rows)
        return mcq(f + "네 곳을 모두 합하면 얼마인가요?", fmt(t, u), [fmt(t + big, u), fmt(t - small, u), fmt(t + small * 10, u) if small * 10 != big else fmt(t + 2 * big, u)],
                   "각각 %s이에요. 모두 더하면 <b>%s</b>" % (", ".join(fmt(v, u) for _, v in rows), fmt(t, u)))
    (a, va), (b, vb) = R.sample(rows, 2)
    if k == "diff":
        d = abs(va - vb)
        more = a if va > vb else b
        return mcq(f + "%s %s보다 얼마나 더 많은가요?" % (josa(more, "은/는"), b if more == a else a), fmt(d, u),
                   [fmt(d + big, u), fmt(va + vb, u), fmt(d + small, u)],
                   "%s − %s = <b>%s</b>" % (fmt(max(va, vb), u), fmt(min(va, vb), u), fmt(d, u)))
    return mcq(f + "%s %s를 합하면 얼마인가요?" % (josa(a, "과/와"), b), fmt(va + vb, u), [fmt(va + vb + big, u), fmt(abs(va - vb), u), fmt(va + vb - small, u)],
               "%s + %s = <b>%s</b>" % (fmt(va, u), fmt(vb, u), fmt(va + vb, u)))


def draw():
    """값을 그림으로 나타내려면 큰 그림과 작은 그림을 몇 개씩?"""
    big, small = R.choice([(100, 10), (10, 1)])
    v = R.randint(1, 5) * big + R.randint(1, 9) * small
    nb, ns = divmod(v, big)
    ns //= small
    return mcq("큰 그림은 %d, 작은 그림은 %d을 나타내는 그림그래프에 %d을 그리려고 해요. 큰 그림과 작은 그림을 몇 개씩 그려야 하나요?" % (big, small, v),
               "큰 그림 %d개, 작은 그림 %d개" % (nb, ns), ["큰 그림 %d개, 작은 그림 %d개" % (ns, nb) if ns != nb else "큰 그림 %d개, 작은 그림 %d개" % (nb + 1, ns),
                                                       "큰 그림 %d개, 작은 그림 %d개" % (nb, ns + 1), "큰 그림 %d개, 작은 그림 %d개" % (nb - 1 if nb > 1 else nb + 2, ns + 10 if ns < 5 else ns - 1)],
               "%d = %d × %d + %d × %d이니까 <b>큰 그림 %d개, 작은 그림 %d개</b>" % (v, big, nb, small, ns, nb, ns))


def from_table():
    names = R.sample(["딸기", "포도", "바나나", "수박", "복숭아", "사과", "귤", "배"], 4)
    vals = [R.randint(2, 15) for _ in names]
    if len(set(vals)) < 4:
        return None
    t = table(["과일"] + names + ["합계"], [["학생 수(명)"] + [str(v) for v in vals] + ["?"]])
    k = R.choice(["total", "most", "diff"])
    if k == "total":
        s = sum(vals)
        return mcq(t + "좋아하는 과일별 학생 수를 조사했어요. 조사한 학생은 모두 몇 명인가요?", "%d명" % s, ["%d명" % x for x in (s + 1, s - 2, s + 10, max(vals))],
                   "%s = <b>%d</b>(명)" % (" + ".join(map(str, vals)), s))
    if k == "most":
        i = vals.index(max(vals))
        return mcq(t + "가장 많은 학생이 좋아하는 과일은?", names[i], [n for n in names if n != names[i]],
                   "학생 수가 가장 많은 것은 %d명인 <b>%s</b>예요." % (vals[i], names[i]))
    i, j = R.sample(range(4), 2)
    if vals[i] < vals[j]:
        i, j = j, i
    d = vals[i] - vals[j]
    return mcq(t + "%s 좋아하는 학생은 %s 좋아하는 학생보다 몇 명 더 많나요?" % (josa(names[i], "을/를"), josa(names[j], "을/를")), "%d명" % d,
               ["%d명" % x for x in (d + 1, vals[i] + vals[j], d + 2, d - 1) if x != d and x > 0], "%d − %d = <b>%d</b>(명)" % (vals[i], vals[j], d))


unit("grade-3", "picture-graphs", 20, "[4수04-01]",
     "자료를 수집하여 그림그래프나 막대그래프로 나타내고 해석할 수 있다.",
     "자료의 정리와 그림그래프", "그림그래프",
     "초등 3학년 2학기 자료의 정리 학습지: 표로 정리하기, 그림그래프 읽기, 가장 많은 것과 적은 것, 합과 차, 그림그래프로 나타내기까지 100문제와 정답.",
     "큰 그림과 작은 그림이 나타내는 수부터", "큰 그림 3개, 작은 그림 4개 → 340",
     ["조사한 자료는 <b>표</b>로 정리하면 합계와 크기를 한눈에 알 수 있어요.",
      "<b>그림그래프</b>는 조사한 수를 그림으로 나타낸 그래프예요. 보통 큰 그림은 10이나 100, 작은 그림은 1이나 10을 나타내요.",
      "그림그래프를 읽을 때는 <b>큰 그림과 작은 그림이 각각 얼마인지</b> 먼저 확인해요.",
      "가장 많은 것을 찾을 때는 큰 그림의 수를 먼저 비교하고, 같으면 작은 그림의 수를 비교해요."],
     [("큰 그림이 100상자, 작은 그림이 10상자일 때 큰 그림 2개, 작은 그림 5개는?", ["100 × 2 + 10 × 5 = 250"], "250상자")],
     [("큰 그림과 작은 그림을 모두 1개씩으로 센다", "큰 그림 1개는 10이나 100이에요. 범례를 먼저 확인해요."),
      ("그림이 크게 그려진 줄을 많다고 생각한다", "그림의 수와 크기를 함께 보고 수로 바꾸어 비교해요."),
      ("표의 합계를 빠뜨리고 더한다", "모든 칸을 빠짐없이 더했는지 확인해요.")],
     [("그림그래프는 언제 배우나요?", "초등 3학년 2학기 「자료의 정리」 단원에서 배워요. 막대그래프는 4학년, 꺾은선그래프는 4학년 2학기에 배워요."),
      ("그림그래프의 좋은 점은?", "그림의 크기와 수로 많고 적음을 한눈에 비교할 수 있어요. 큰 수도 적은 그림으로 나타낼 수 있어요.")],
     [("표로 정리하기", [(from_table, 20)]),
      ("그림그래프 읽기", [(read_one, 20)]),
      ("가장 많은 것과 적은 것", [(most_least, 20)]),
      ("합과 차", [(total_diff, 20)]),
      ("그림그래프로 나타내기", [(draw, 12), (read_one, 8)])],
     82320)
