# -*- coding: utf-8 -*-
"""
대한민국 중학교 2학년 수학（2022 개정）：도형과 측정・자료와 가능성の 8 単元
  iso   : 이등변삼각형의 성질과 직각삼각형의 합동 [9수03-09]
  center: 삼각형의 외심과 내심 [9수03-10]
  quad  : 사각형의 성질 [9수03-11]
  sim   : 도형의 닮음 [9수03-12] [9수03-13]
  ratio : 평행선과 선분의 길이의 비 [9수03-14]
  pyth  : 피타고라스 정리 [9수03-15]
  count : 경우의 수 [9수04-05]
  prob  : 확률 [9수04-06]
誤答は「이등변삼각형의 꼭지각과 밑각을 바꾼다」「외심과 내심의 성질을 바꾼다」「닮음비를 넓이의 비로 쓴다」
「빗변이 아닌 변을 c로 놓는다」「순서가 없는 경우에 순서를 센다」「‘또는’의 확률을 곱한다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_common import josa, Names, num, fr
from kr_mid import M, N, neg, par, dec, rt, unit, figure

R = random.Random(82810)
NM = Names(R)
G = "grade-8"


def deg(v):
    return "%s°" % neg(v)


def cm(v):
    return "%s cm" % neg(v)


def F(v):
    v = Fr(v)
    return neg(v)


# ------------------------------------------------------------------ 이등변삼각형
def iso_fig(top):
    pts = {"A": (2, 3.2), "B": (0, 0), "C": (4, 0)}
    return figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], label="AB = AC인 이등변삼각형", ticks=[("A", "B", 1), ("A", "C", 1)])


def is_angle(kinds=("base", "top", "ext", "bis")):
    def mk():
        how = R.choice(kinds)
        g = iso_fig(True)
        if how == "base":
            t = R.choice(range(20, 141, 2))
            v = Fr(180 - t, 2)
            return N("AB = AC인 이등변삼각형 ABC에서 ∠A = %d°일 때, ∠B의 크기는?%s" % (t, g), v, [180 - t, t, Fr(180 - t, 3), 90 - t if t < 90 else 2 * t - 90], "두 밑각의 크기는 같아요. (180° − %d°) ÷ 2 = <b>%s°</b>" % (t, F(v)), f=deg)
        if how == "top":
            b = R.choice(range(25, 86))
            return N("AB = AC인 이등변삼각형 ABC에서 ∠B = %d°일 때, ∠A의 크기는?%s" % (b, g), 180 - 2 * b, [180 - b, b, Fr(180 - b, 2), 90 - b], "∠C = ∠B = %d°이므로 180° − 2 × %d° = <b>%d°</b>" % (b, b, 180 - 2 * b), f=deg)
        if how == "ext":
            t = R.choice(range(20, 101, 2))
            v = 180 - Fr(180 - t, 2)
            return N("AB = AC인 이등변삼각형 ABC에서 ∠A = %d°일 때, ∠C의 외각의 크기는?" % t, v, [Fr(180 - t, 2), 180 - t, t + 90, 2 * t], "∠C = %s°이므로 외각은 180° − %s° = <b>%s°</b>" % (F(Fr(180 - t, 2)), F(Fr(180 - t, 2)), F(v)), f=deg)
        L = R.randint(6, 20)
        k = R.choice(["len", "ang"])
        if k == "len":
            return N("AB = AC인 이등변삼각형 ABC에서 꼭지각 ∠A의 이등분선이 BC와 만나는 점을 D라 해요. BC = %d cm일 때, BD의 길이는?" % (2 * L), L, [2 * L, Fr(L, 2), L + 2, 4 * L],
                     "꼭지각의 이등분선은 밑변을 수직이등분해요. <b>%d cm</b>" % L, f=cm)
        return N("AB = AC인 이등변삼각형 ABC에서 꼭지각 ∠A의 이등분선이 BC와 만나는 점을 D라 할 때, ∠ADB의 크기는? (BC = %d cm)" % (2 * L), 90, [45, 60, 180, 120],
                 "꼭지각의 이등분선은 밑변에 수직이에요. <b>90°</b>", f=deg)
    return mk


def is_chain():
    def mk():
        how = R.choice(["fold", "side", "ext2"])
        if how == "fold":
            a = R.choice(range(30, 76))
            return N("폭이 일정한 직사각형 모양의 종이테이프를 접었더니 겹친 부분에 삼각형이 생겼어요. 접은 선과 테이프의 한 변이 이루는 각이 %d°일 때, 이 삼각형에서 나머지 한 각의 크기는?" % a, 180 - 2 * a,
                     [a, 180 - a, 90 - a, 2 * a], "접은 각과 엇각이 같아 두 각이 %d°인 이등변삼각형이 생겨요. 180° − 2 × %d° = <b>%d°</b>" % (a, a, 180 - 2 * a), f=deg)
        if how == "side":
            b = R.choice(range(35, 80))
            k = R.randint(4, 15)
            return N("△ABC에서 ∠B = ∠C = %d°이고 AB = %d cm일 때, AC의 길이는?" % (b, k), k, [2 * k, Fr(k, 2), k + 1, b], "두 내각이 같으면 이등변삼각형이므로 AC = AB = <b>%d cm</b>" % k, f=cm)
        x = R.choice(range(20, 41))
        return N("AB = AC인 이등변삼각형 ABC에서 ∠C의 외각의 크기가 %d°일 때, ∠A의 크기는?" % (180 - x), 180 - 2 * x, [x, 180 - x, 2 * x, 90 - x], "∠C = %d°, ∠B = %d°이므로 ∠A = 180° − %d° = <b>%d°</b>" % (x, x, 2 * x, 180 - 2 * x), f=deg)
    return mk


def is_cond():
    F_ = [("두 내각의 크기가 같은 삼각형은?", "이등변삼각형", ["직각삼각형", "정삼각형", "둔각삼각형"], "두 내각의 크기가 같으면 <b>이등변삼각형</b>이에요."),
          ("이등변삼각형에서 꼭지각의 이등분선의 성질로 옳은 것은?", "밑변을 수직이등분해요", ["빗변과 평행해요", "꼭지각과 같은 크기예요", "밑각을 이등분해요"], "<b>밑변을 수직이등분해요</b>."),
          ("두 직각삼각형에서 빗변의 길이와 한 예각의 크기가 각각 같으면?", "RHA 합동이에요", ["RHS 합동이에요", "SSS 합동이에요", "합동이 아니에요"], "Right angle, Hypotenuse, Angle → <b>RHA 합동</b>"),
          ("두 직각삼각형에서 빗변의 길이와 다른 한 변의 길이가 각각 같으면?", "RHS 합동이에요", ["RHA 합동이에요", "ASA 합동이에요", "합동이 아니에요"], "Right angle, Hypotenuse, Side → <b>RHS 합동</b>"),
          ("각의 이등분선 위의 한 점에서 그 각의 두 변까지의 거리는?", "서로 같아요", ["서로 달라요", "항상 1 cm예요", "각의 크기에 따라 2배가 돼요"], "RHA 합동이므로 <b>서로 같아요</b>."),
          ("정삼각형은 이등변삼각형이라고 할 수 있을까요?", "네, 두 변의 길이가 같으므로 이등변삼각형이에요", ["아니요, 세 변이 같아서 아니에요", "아니요, 밑각이 없어요", "직각일 때만 그래요"], "정삼각형은 <b>이등변삼각형</b>이기도 해요."),
          ("∠B = ∠C인 △ABC에서 AB = 7 cm일 때, AC의 길이는?", "7 cm", ["14 cm", "3.5 cm", "알 수 없어요"], "두 밑각이 같으면 이등변삼각형이므로 <b>7 cm</b>예요.")]
    pool = F_[:]
    R.shuffle(pool)

    def mk():
        if pool and R.random() < 0.5:
            return M(*pool.pop())
        a, h = R.randint(3, 12), R.randint(3, 12)
        k = R.choice(["RHS", "RHA"])
        if k == "RHS":
            return M("∠C = ∠F = 90°인 두 직각삼각형 ABC, DEF에서 AB = DE = %d cm, AC = DF = %d cm예요. 두 삼각형의 합동 조건은?" % (a + h, a), "RHS 합동", ["RHA 합동", "SAS 합동", "SSS 합동"], "빗변과 다른 한 변의 길이가 같아요. <b>RHS 합동</b>")
        t = R.randint(20, 70)
        return M("∠C = ∠F = 90°인 두 직각삼각형 ABC, DEF에서 AB = DE = %d cm, ∠A = ∠D = %d°예요. 두 삼각형의 합동 조건은?" % (a + h, t), "RHA 합동", ["RHS 합동", "ASA 합동", "SSS 합동"], "빗변과 한 예각의 크기가 같아요. <b>RHA 합동</b>")
    return mk


# ------------------------------------------------------------------ 외심과 내심
def c_outer(kinds=("ang", "dist", "right", "sum")):
    def mk():
        how = R.choice(kinds)
        if how == "ang":
            a = R.randint(25, 80)
            k = R.choice(["BOC", "A"])
            if k == "BOC":
                return N("점 O가 △ABC의 외심이고 ∠A = %d°일 때, ∠BOC의 크기는?" % a, 2 * a, [a, 90 + Fr(a, 2), 180 - a, 180 - 2 * a], "∠BOC = 2∠A = <b>%d°</b>" % (2 * a), f=deg)
            return N("점 O가 △ABC의 외심이고 ∠BOC = %d°일 때, ∠A의 크기는?" % (2 * a), a, [2 * a, 4 * a if 4 * a < 180 else a + 10, 180 - 2 * a, 90 - a], "∠A = ½∠BOC = <b>%d°</b>" % a, f=deg)
        if how == "dist":
            r = R.randint(3, 12)
            return N("점 O가 △ABC의 외심이고 OA = %d cm일 때, OB + OC의 값은?" % r, 2 * r, [r, 3 * r, Fr(r, 2), r + 2], "외심에서 세 꼭짓점까지의 거리는 같아요. %d + %d = <b>%d cm</b>" % (r, r, 2 * r), f=cm)
        if how == "right":
            h = R.randint(4, 20) * 2
            return N("∠C = 90°인 직각삼각형 ABC에서 빗변 AB의 길이가 %d cm일 때, 외접원의 반지름의 길이는?" % h, h // 2, [h, h // 4, h // 2 + 1, 2 * h], "직각삼각형의 외심은 빗변의 중점이에요. <b>%d cm</b>" % (h // 2), f=cm)
        x, y = R.randint(15, 40), R.randint(15, 40)
        z = 90 - x - y
        if z <= 5:
            return None
        return N("점 O가 △ABC의 외심일 때, ∠OAB = %d°, ∠OBC = %d°이면 ∠OCA의 크기는?" % (x, y), z, [180 - x - y, x + y, 90 - x, 90 - y], "∠OAB + ∠OBC + ∠OCA = 90°예요. <b>%d°</b>" % z, f=deg)
    return mk


def c_inner(kinds=("ang", "sum", "area", "dist")):
    def mk():
        how = R.choice(kinds)
        if how == "ang":
            a = R.choice(range(20, 101, 2))
            k = R.choice(["BIC", "A"])
            if k == "BIC":
                v = 90 + Fr(a, 2)
                return N("점 I가 △ABC의 내심이고 ∠A = %d°일 때, ∠BIC의 크기는?" % a, v, [2 * a, 180 - a, 90 + a, 90 - Fr(a, 2)], "∠BIC = 90° + ½∠A = <b>%s°</b>" % F(v), f=deg)
            v = 90 + Fr(a, 2)
            return N("점 I가 △ABC의 내심이고 ∠BIC = %s°일 때, ∠A의 크기는?" % F(v), a, [Fr(v, 2), v - 90, 2 * v - 180 + 10, 180 - v], "90° + ½∠A = %s° → ∠A = <b>%d°</b>" % (F(v), a), f=deg)
        if how == "sum":
            x, y = R.randint(15, 40), R.randint(15, 40)
            z = 90 - x - y
            if z <= 5:
                return None
            return N("점 I가 △ABC의 내심일 때, ∠IAB = %d°, ∠IBC = %d°이면 ∠ICA의 크기는?" % (x, y), z, [180 - x - y, x + y, 2 * z, 90 - x], "∠IAB + ∠IBC + ∠ICA = 90°예요. <b>%d°</b>" % z, f=deg)
        if how == "area":
            r = R.randint(2, 6)
            a, b, c = R.choice([(5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17), (7, 24, 25), (12, 16, 20), (10, 24, 26)])
            r = Fr(a * b, a + b + c)
            k = R.choice(["r", "S"])
            if k == "r":
                return N("세 변의 길이가 %d cm, %d cm, %d cm인 직각삼각형의 내접원의 반지름의 길이는?" % (a, b, c), r, [Fr(c, 2), r * 2, Fr(a * b, 2 * (a + b + c)) if r * 2 != Fr(a * b, a + b + c) else r + 1, Fr(a + b - c, 1)],
                         "넓이 %d = ½ × r × (%d + %d + %d) → r = <b>%s cm</b>" % (a * b // 2, a, b, c, F(r)), f=cm)
            r = R.randint(2, 5)
            p = R.randint(20, 40)
            return N("△ABC의 내접원의 반지름의 길이가 %d cm이고, 둘레의 길이가 %d cm일 때, △ABC의 넓이는?" % (r, p), Fr(r * p, 2), [r * p, Fr(r * p, 3), r + p, r * r * p], "½ × %d × %d = <b>%s cm²</b>" % (r, p, F(Fr(r * p, 2))),
                     f=lambda v: "%s cm²" % neg(v))
        a, b, c = R.randint(5, 10), R.randint(5, 10), R.randint(5, 10)
        if not (max(a, b, c) < a + b + c - max(a, b, c)):
            return None
        s = Fr(a + b + c, 2)
        x = s - a
        return N("△ABC의 내접원이 변 AB, BC, CA와 만나는 점을 D, E, F라 해요. AB = %d cm, BC = %d cm, CA = %d cm일 때, BD의 길이는?" % (c, a, b), s - b, [s - a, s - c, s, Fr(c, 2)],
                 "AD = AF, BD = BE, CE = CF예요. BD = (AB + BC − CA) ÷ 2 = <b>%s cm</b>" % F(s - b), f=cm)
    return mk


def c_concept():
    T = [("외심", "세 변의 수직이등분선의 교점", "세 꼭짓점까지의 거리가 같아요"), ("내심", "세 내각의 이등분선의 교점", "세 변까지의 거리가 같아요")]
    Q = []
    for nm, a, b in T:
        other = [x for x in T if x[0] != nm][0]
        Q.append(("삼각형의 <b>%s</b>은 무엇의 교점일까요?" % nm, a, [other[1], "세 중선의 교점", "세 높이의 교점"], "<b>%s</b>" % a))
        Q.append(("삼각형의 <b>%s</b>의 성질로 옳은 것은?" % nm, b, [other[2], "세 변의 중점을 지나요", "항상 삼각형의 밖에 있어요"], "<b>%s</b>" % b))
    Q += [("둔각삼각형의 외심의 위치는?", "삼각형의 밖", ["삼각형의 안", "빗변 위", "한 꼭짓점"], "둔각삼각형의 외심은 <b>삼각형의 밖</b>에 있어요."),
          ("직각삼각형의 외심의 위치는?", "빗변의 중점", ["삼각형의 안", "삼각형의 밖", "직각인 꼭짓점"], "<b>빗변의 중점</b>이에요."),
          ("내심의 위치에 대한 설명으로 옳은 것은?", "항상 삼각형의 안에 있어요", ["둔각삼각형에서는 밖에 있어요", "빗변의 중점이에요", "꼭짓점과 일치할 수 있어요"], "내심은 <b>항상 삼각형의 안</b>에 있어요."),
          ("정삼각형의 외심과 내심은?", "일치해요", ["항상 달라요", "외심만 있어요", "내심만 있어요"], "정삼각형은 외심과 내심이 <b>일치해요</b>."),
          ("삼각형의 세 꼭짓점을 지나는 원을 무엇이라고 할까요?", "외접원", ["내접원", "동심원", "단위원"], "<b>외접원</b>이고 그 중심이 외심이에요."),
          ("삼각형의 세 변에 접하는 원을 무엇이라고 할까요?", "내접원", ["외접원", "동심원", "호"], "<b>내접원</b>이고 그 중심이 내심이에요.")]
    pool = Q[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        return M(*pool.pop())
    return mk


# ------------------------------------------------------------------ 사각형
def q_para(kinds=("ang", "side", "diag", "x")):
    def mk():
        how = R.choice(kinds)
        if how == "ang":
            a = R.randint(50, 130)
            if a == 90:
                return None
            k = R.choice(["B", "C"])
            if k == "C":
                return N("평행사변형 ABCD에서 ∠A = %d°일 때, ∠C의 크기는?" % a, a, [180 - a, 90 - a if a < 90 else a - 90, 360 - a], "대각의 크기는 같아요. <b>%d°</b>" % a, f=deg)
            return N("평행사변형 ABCD에서 ∠A = %d°일 때, ∠B의 크기는?" % a, 180 - a, [a, 360 - a, 90 + a if a < 90 else a - 90], "이웃한 두 각의 합은 180°예요. <b>%d°</b>" % (180 - a), f=deg)
        if how == "side":
            a, b = R.randint(4, 15), R.randint(4, 15)
            if a == b:
                return None
            return N("평행사변형 ABCD에서 AB = %d cm, BC = %d cm일 때, 둘레의 길이는?" % (a, b), 2 * (a + b), [a + b, a * b, 4 * a, 2 * a + b], "대변의 길이가 같아요. 2 × (%d + %d) = <b>%d cm</b>" % (a, b, 2 * (a + b)), f=cm)
        if how == "diag":
            p, q = R.randint(3, 15), R.randint(3, 15)
            return N("평행사변형 ABCD의 두 대각선의 교점을 O라 해요. AC = %d cm, BD = %d cm일 때, AO + BO의 값은?" % (2 * p, 2 * q), p + q, [2 * p + 2 * q, p * q, 2 * p + q, p + 2 * q], "두 대각선은 서로를 이등분해요. %d + %d = <b>%d cm</b>" % (p, q, p + q), f=cm)
        x = R.randint(3, 12)
        k = R.choice([2, 3])
        c = R.randint(1, 9)
        return N("평행사변형 ABCD에서 AB = (%dx − %d) cm, CD = (x + %d) cm일 때, x의 값은?" % (k, c, (k - 1) * x - c), x, [x + 1, (k - 1) * x, Fr(c, k), x * k - c],
                 "대변의 길이가 같으므로 %dx − %d = x + %d → x = <b>%d</b>" % (k, c, (k - 1) * x - c, x))
    return mk


QUADS = ["사다리꼴", "평행사변형", "직사각형", "마름모", "정사각형"]
PROPS = {"두 대각선의 길이가 같아요": ["직사각형", "정사각형"], "두 대각선이 서로 수직으로 만나요": ["마름모", "정사각형"],
         "두 대각선이 서로를 이등분해요": ["평행사변형", "직사각형", "마름모", "정사각형"], "네 각의 크기가 모두 같아요": ["직사각형", "정사각형"],
         "네 변의 길이가 모두 같아요": ["마름모", "정사각형"], "두 쌍의 대변이 각각 평행해요": ["평행사변형", "직사각형", "마름모", "정사각형"]}


def q_kind(kinds=("has", "hasnt", "cond", "inc")):
    def mk():
        how = R.choice(kinds)
        if how == "has":
            p = R.choice(sorted(PROPS))
            ok = R.choice(PROPS[p])
            bad = [q for q in QUADS if q not in PROPS[p]]
            if len(bad) < 3:
                bad += ["등변사다리꼴"] if "등변사다리꼴" not in bad and p != "두 대각선의 길이가 같아요" else ["일반 사각형"]
            if len(bad) < 3:
                bad += ["일반 사각형"]
            return M("다음 중 '<b>%s</b>'를 만족하는 사각형은?" % p, ok, bad, "%s 이 성질을 가져요. <b>%s</b>" % (josa(ok, "은/는"), ok))
        if how == "hasnt":
            p = R.choice(sorted(PROPS))
            bad = [q for q in QUADS if q not in PROPS[p]]
            ok = R.choice(bad)
            good = PROPS[p][:]
            while len(good) < 3:
                good.append("등변사다리꼴" if p == "두 대각선의 길이가 같아요" and "등변사다리꼴" not in good else "정사각형" if "정사각형" not in good else "직사각형")
                good = list(dict.fromkeys(good))
                if len(good) < 3:
                    return None
            return M("다음 중 '<b>%s</b>'를 항상 만족한다고 할 수 <b>없는</b> 사각형은?" % p, ok, good[:3], "<b>%s</b>은 항상 그렇지는 않아요." % ok)
        if how == "cond":
            C = [("평행사변형", "한 내각이 직각이면", "직사각형"), ("평행사변형", "두 대각선의 길이가 같으면", "직사각형"), ("평행사변형", "이웃한 두 변의 길이가 같으면", "마름모"),
                 ("평행사변형", "두 대각선이 수직이면", "마름모"), ("직사각형", "이웃한 두 변의 길이가 같으면", "정사각형"), ("마름모", "한 내각이 직각이면", "정사각형"),
                 ("직사각형", "두 대각선이 수직이면", "정사각형"), ("마름모", "두 대각선의 길이가 같으면", "정사각형")]
            a, c, b = R.choice(C)
            return M("<b>%s</b>에서 %s 어떤 사각형이 될까요?" % (a, c), b, [q for q in QUADS if q not in (a, b)][:3], "<b>%s</b>이 돼요." % b)
        F_ = [("정사각형은 직사각형이에요.", True), ("정사각형은 마름모예요.", True), ("직사각형은 평행사변형이에요.", True), ("마름모는 평행사변형이에요.", True),
              ("평행사변형은 사다리꼴이에요.", True), ("직사각형은 정사각형이에요.", False), ("마름모는 직사각형이에요.", False), ("사다리꼴은 평행사변형이에요.", False),
              ("평행사변형은 마름모예요.", False)]
        if R.random() < 0.5:
            ok = R.choice([x for x, v in F_ if v])
            return M("다음 중 항상 옳은 것은?", ok, R.sample([x for x, v in F_ if not v], 3), "<b>%s</b>" % ok)
        ok = R.choice([x for x, v in F_ if not v])
        return M("다음 중 항상 옳다고 할 수 <b>없는</b> 것은?", ok, R.sample([x for x, v in F_ if v], 3), "<b>%s</b> — 항상 그렇지는 않아요." % ok)
    return mk


def q_area():
    def mk():
        how = R.choice(["half", "quarter", "tri", "rhombus"])
        S = R.randint(4, 30) * 4
        if how == "half":
            return N("넓이가 %d cm²인 평행사변형 ABCD에서 대각선 AC로 나뉜 △ABC의 넓이는?" % S, S // 2, [S, S // 4, S // 3 if S % 3 == 0 else S // 2 + 2, 2 * S], "대각선은 평행사변형의 넓이를 이등분해요. <b>%d cm²</b>" % (S // 2),
                     f=lambda v: "%s cm²" % neg(v))
        if how == "quarter":
            return N("넓이가 %d cm²인 평행사변형 ABCD의 두 대각선의 교점을 O라 할 때, △OAB의 넓이는?" % S, S // 4, [S // 2, S // 8 if S % 8 == 0 else S // 4 + 1, S, S // 4 * 3], "두 대각선은 넓이를 4등분해요. <b>%d cm²</b>" % (S // 4),
                     f=lambda v: "%s cm²" % neg(v))
        if how == "tri":
            a, b = R.randint(3, 20), R.randint(3, 20)
            return N("평행사변형 ABCD의 내부의 한 점 P에 대하여 △PAB = %d cm², △PCD = %d cm²일 때, 평행사변형 ABCD의 넓이는?" % (a, b), 2 * (a + b), [a + b, a * b, 4 * (a + b), 2 * a + b],
                     "△PAB + △PCD = ½ □ABCD예요. 2 × (%d + %d) = <b>%d cm²</b>" % (a, b, 2 * (a + b)), f=lambda v: "%s cm²" % neg(v))
        p, q = R.randint(3, 16) * 2, R.randint(3, 16)
        return N("두 대각선의 길이가 %d cm, %d cm인 마름모의 넓이는?" % (p, q), p * q // 2, [p * q, p + q, p * q // 4 if p * q % 4 == 0 else p * q // 2 + 1, 2 * (p + q)], "(대각선) × (대각선) ÷ 2 = <b>%d cm²</b>" % (p * q // 2),
                 f=lambda v: "%s cm²" % neg(v))
    return mk


# ------------------------------------------------------------------ 닮음
def s_ratio(kinds=("side", "peri", "area", "vol", "ratio")):
    def mk():
        how = R.choice(kinds)
        m, n = R.choice([(1, 2), (2, 3), (3, 4), (2, 5), (3, 5), (1, 3), (4, 5)])
        k = R.randint(1, 5)
        if how == "side":
            a = m * k * R.choice([1, 2])
            b = a * n // m
            return N("△ABC ∽ △DEF이고 닮음비가 %d : %d예요. AB = %d cm일 때, DE의 길이는?" % (m, n, a), Fr(a * n, m), [Fr(a * m, n), a + n - m, a * n, Fr(a * n * n, m * m)],
                     "%d : %d = %d : DE → DE = <b>%s cm</b>" % (m, n, a, F(Fr(a * n, m))), f=cm)
        if how == "peri":
            P = m * R.randint(3, 10)
            return N("닮음비가 %d : %d인 두 삼각형에서 작은 삼각형의 둘레의 길이가 %d cm일 때, 큰 삼각형의 둘레의 길이는?" % (m, n, P), Fr(P * n, m), [Fr(P * n * n, m * m), P + n - m, Fr(P * m, n), P * n],
                     "둘레의 길이의 비도 닮음비와 같아요. <b>%s cm</b>" % F(Fr(P * n, m)), f=cm)
        if how == "area":
            S = m * m * R.randint(2, 8)
            v = Fr(S * n * n, m * m)
            return N("닮음비가 %d : %d인 두 도형에서 작은 도형의 넓이가 %d cm²일 때, 큰 도형의 넓이는?" % (m, n, S), v, [Fr(S * n, m), Fr(S * n ** 3, m ** 3), S + n * n - m * m, v + 1],
                     "넓이의 비는 %d² : %d² = %d : %d예요. <b>%s cm²</b>" % (m, n, m * m, n * n, F(v)), f=lambda x: "%s cm²" % neg(x))
        if how == "vol":
            V = m ** 3 * R.randint(1, 4)
            v = Fr(V * n ** 3, m ** 3)
            return N("닮음비가 %d : %d인 두 입체도형에서 작은 입체도형의 부피가 %d cm³일 때, 큰 입체도형의 부피는?" % (m, n, V), v, [Fr(V * n * n, m * m), Fr(V * n, m), v * 2, V * n],
                     "부피의 비는 %d³ : %d³ = %d : %d예요. <b>%s cm³</b>" % (m, n, m ** 3, n ** 3, F(v)), f=lambda x: "%s cm³" % neg(x))
        k = R.choice(["area", "vol"])
        if k == "area":
            return M("닮은 두 도형의 넓이의 비가 %d : %d일 때, 닮음비는?" % (m * m, n * n), "%d : %d" % (m, n), ["%d : %d" % (m * m, n * n), "%d : %d" % (m ** 3, n ** 3), "%d : %d" % (n, m)], "넓이의 비가 a² : b²이면 닮음비는 <b>%d : %d</b>" % (m, n))
        return M("닮은 두 입체도형의 겉넓이의 비가 %d : %d일 때, 부피의 비는?" % (m * m, n * n), "%d : %d" % (m ** 3, n ** 3), ["%d : %d" % (m * m, n * n), "%d : %d" % (m, n), "%d : %d" % (m ** 4, n ** 4)],
                 "닮음비 %d : %d → 부피의 비 <b>%d : %d</b>" % (m, n, m ** 3, n ** 3))
    return mk


def tri_sim_fig(a, b, k):
    """△ABC와 △ADE（DE ∥ BC）"""
    pts = {"A": (1.4, 3.0), "B": (0, 0), "C": (4, 0), "D": (1.4 - 1.4 * k, 3 - 3 * k), "E": (1.4 + 2.6 * k, 3 - 3 * k)}
    return pts


def s_cond(kinds=("cond", "find", "right")):
    def mk():
        how = R.choice(kinds)
        if how == "cond":
            C = [("세 쌍의 대응변의 길이의 비가 같아요", "SSS 닮음"), ("두 쌍의 대응변의 길이의 비가 같고 그 끼인각의 크기가 같아요", "SAS 닮음"), ("두 쌍의 대응각의 크기가 각각 같아요", "AA 닮음")]
            d, ok = R.choice(C)
            return M("두 삼각형에서 <b>%s</b>. 이때의 닮음 조건은?" % d, ok, [x for x in ("SSS 닮음", "SAS 닮음", "AA 닮음", "RHS 닮음") if x != ok], "<b>%s</b>" % ok)
        if how == "find":
            m, n = R.choice([(1, 2), (2, 3), (1, 3), (2, 5), (3, 4)])
            AD = m * R.randint(1, 4)
            AB = AD * n // m if AD * n % m == 0 else None
            if AB is None:
                return None
            BC = n * R.randint(2, 6)
            DE = Fr(BC * m, n)
            pts = {"A": (1.5, 3.2), "B": (0, 0), "C": (4.5, 0)}
            t = Fr(m, n)
            pts["D"] = (1.5 - 1.5 * float(t), 3.2 - 3.2 * float(t))
            pts["E"] = (1.5 + 3.0 * float(t), 3.2 - 3.2 * float(t))
            g = figure(pts, [("A", "B"), ("B", "C"), ("C", "A"), ("D", "E")], label="DE와 BC가 평행한 삼각형", sides=[("A", "D", "%d" % AD), ("D", "B", "%d" % (AB - AD)), ("B", "C", "%d" % BC), ("D", "E", "x")])
            return N("그림에서 DE ∥ BC일 때, x의 값은? (단위: cm)%s" % g, DE, [Fr(BC * (AB - AD), AB), Fr(BC * AD, AB - AD), BC - AD, DE + 1],
                     "△ADE ∽ △ABC (AA 닮음), %d : %d = x : %d → x = <b>%s</b>" % (AD, AB, BC, F(DE)))
        # 직각삼각형의 닮음: AB² = BH·BC 등
        p, q = R.choice([(1, 4), (4, 9), (1, 9), (2, 8), (9, 16), (4, 16), (3, 12), (1, 16)])
        k = R.choice(["h", "leg"])
        if k == "h":
            h = int(math.isqrt(p * q))
            return N("∠A = 90°인 직각삼각형 ABC에서 점 A에서 BC에 내린 수선의 발을 H라 해요. BH = %d cm, CH = %d cm일 때, AH의 길이는?" % (p, q), h, [Fr(p + q, 2), p * q, h + 1, abs(q - p)],
                     "AH² = BH × CH = %d → AH = <b>%d cm</b>" % (p * q, h), f=cm)
        L = int(math.isqrt(p * (p + q)))
        if L * L != p * (p + q):
            return None
        return N("∠A = 90°인 직각삼각형 ABC에서 점 A에서 BC에 내린 수선의 발을 H라 해요. BH = %d cm, CH = %d cm일 때, AB의 길이는?" % (p, q), L, [p + q, int(math.isqrt(p * q)), L + 1, Fr(p + q, 2)],
                 "AB² = BH × BC = %d × %d → AB = <b>%d cm</b>" % (p, p + q, L), f=cm)
    return mk


# ------------------------------------------------------------------ 평행선과 선분의 비
def r_tri(kinds=("side", "mid", "par3", "bis")):
    def mk():
        how = R.choice(kinds)
        if how == "side":
            a, b = R.randint(2, 8), R.randint(2, 8)
            c = R.randint(2, 8) * a
            d = Fr(c * b, a)
            if d.denominator != 1 or not 0.3 <= a / (a + b) <= 0.7:
                return None
            pts = {"A": (1.5, 3.2), "B": (0, 0), "C": (4.5, 0)}
            t = a / (a + b)
            pts["D"] = (1.5 - 1.5 * t, 3.2 - 3.2 * t)
            pts["E"] = (1.5 + 3.0 * t, 3.2 - 3.2 * t)
            g = figure(pts, [("A", "B"), ("B", "C"), ("C", "A"), ("D", "E")], label="DE와 BC가 평행한 삼각형", sides=[("A", "D", str(a)), ("D", "B", str(b)), ("A", "E", str(c)), ("E", "C", "x")])
            return N("그림에서 DE ∥ BC일 때, x의 값은? (단위: cm)%s" % g, d, [Fr(c * a, b), c + b - a, Fr(c * (a + b), a), d + 1], "AD : DB = AE : EC이므로 %d : %d = %d : x → x = <b>%s</b>" % (a, b, c, F(d)))
        if how == "mid":
            k = R.choice(["mn", "bc", "peri"])
            v = R.randint(3, 15)
            if k == "mn":
                return N("△ABC에서 두 변 AB, AC의 중점을 각각 M, N이라 해요. BC = %d cm일 때, MN의 길이는?" % (2 * v), v, [2 * v, Fr(v, 2), v + 2, 3 * v], "삼각형의 두 변의 중점을 연결한 선분은 나머지 변의 ½이에요. <b>%d cm</b>" % v, f=cm)
            if k == "bc":
                return N("△ABC에서 두 변 AB, AC의 중점을 각각 M, N이라 해요. MN = %d cm일 때, BC의 길이는?" % v, 2 * v, [v, Fr(v, 2), v + 2, 4 * v], "BC = 2MN = <b>%d cm</b>" % (2 * v), f=cm)
            a, b, c = R.randint(4, 14), R.randint(4, 14), R.randint(4, 14)
            if not (max(a, b, c) < a + b + c - max(a, b, c)):
                return None
            return N("세 변의 길이가 %d cm, %d cm, %d cm인 삼각형의 각 변의 중점을 연결하여 만든 삼각형의 둘레의 길이는?" % (a, b, c), Fr(a + b + c, 2), [a + b + c, Fr(a + b + c, 4), 2 * (a + b + c), Fr(a + b + c, 3)],
                     "각 변이 ½이 되므로 둘레도 ½이에요. <b>%s cm</b>" % F(Fr(a + b + c, 2)), f=cm)
        if how == "par3":
            a, b = R.randint(2, 9), R.randint(2, 9)
            c = R.randint(2, 6) * a
            d = Fr(c * b, a)
            if d.denominator != 1:
                return None
            return N("세 평행선 l, m, n이 두 직선과 만나서 생긴 선분의 길이가 다음과 같아요. 한 직선에서 %d cm, %d cm이고, 다른 직선에서 %d cm, x cm일 때, x의 값은?" % (a, b, c), d, [Fr(c * a, b), c + b - a, d + 2, Fr(c, 2) + b],
                     "평행선 사이의 선분의 길이의 비는 같아요. %d : %d = %d : x → x = <b>%s</b>" % (a, b, c, F(d)))
        a, b = R.randint(3, 12), R.randint(3, 12)
        if a == b:
            return None
        bc = R.randint(2, 4) * (a + b)
        bd = Fr(bc * a, a + b)
        return N("△ABC에서 ∠A의 이등분선이 BC와 만나는 점을 D라 해요. AB = %d cm, AC = %d cm, BC = %d cm일 때, BD의 길이는?" % (a, b, bc), bd, [Fr(bc * b, a + b), Fr(bc, 2), bd + 1, Fr(bc * a, b) if Fr(bc * a, b) < bc else bd - 1],
                 "AB : AC = BD : DC = %d : %d → BD = %d × %d/%d = <b>%s cm</b>" % (a, b, bc, a, a + b, F(bd)), f=cm)
    return mk


def r_centroid(kinds=("ag", "gd", "area", "concept")):
    def mk():
        how = R.choice(kinds)
        v = R.randint(2, 12)
        if how == "ag":
            return N("점 G가 △ABC의 무게중심이고 중선 AD의 길이가 %d cm일 때, AG의 길이는?" % (3 * v), 2 * v, [v, Fr(3 * v, 2), 3 * v, 2 * v + 1], "AG : GD = 2 : 1이므로 AG = ⅔ × %d = <b>%d cm</b>" % (3 * v, 2 * v), f=cm)
        if how == "gd":
            return N("점 G가 △ABC의 무게중심이고 AG = %d cm일 때, GD의 길이는? (AD는 중선)" % (2 * v), v, [2 * v, 4 * v, Fr(2 * v, 3), 3 * v], "AG : GD = 2 : 1이므로 GD = <b>%d cm</b>" % v, f=cm)
        if how == "area":
            S = 6 * R.randint(2, 15)
            k = R.choice([("△GAB", 3), ("△GBD", 6)])
            return N("점 G가 넓이가 %d cm²인 △ABC의 무게중심이고 D는 BC의 중점이에요. <b>%s</b>의 넓이는?" % (S, k[0]), S // k[1], [S // 2, S // (9 - k[1]), S // k[1] * 2, S // 4 if S % 4 == 0 else S // k[1] + 1],
                     "무게중심과 세 꼭짓점을 이은 선분은 넓이를 3등분, 중선까지 그으면 6등분해요. <b>%d cm²</b>" % (S // k[1]), f=lambda x: "%s cm²" % neg(x))
        F_ = [("삼각형의 무게중심은?", "세 중선의 교점", ["세 수선의 교점", "세 각의 이등분선의 교점", "세 변의 수직이등분선의 교점"], "<b>세 중선의 교점</b>이에요."),
              ("무게중심은 각 중선을 꼭짓점으로부터 어떤 비로 나눌까요?", "2 : 1", ["1 : 2", "1 : 1", "3 : 1"], "<b>2 : 1</b>로 나누어요."),
              ("정삼각형의 무게중심, 외심, 내심은?", "모두 일치해요", ["모두 달라요", "외심과 내심만 일치해요", "무게중심만 삼각형 밖에 있어요"], "정삼각형은 세 점이 <b>모두 일치해요</b>.")]
        return M(*R.choice(F_))
    return mk


# ------------------------------------------------------------------ 피타고라스 정리
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (12, 16, 20), (9, 40, 41), (15, 20, 25), (10, 24, 26), (12, 35, 37)]


def rtri_fig(a, b, c, unknown):
    pts = {"A": (0, a), "B": (0, 0), "C": (b, 0)}
    lab = {"a": str(a), "b": str(b), "c": str(c)}
    lab[unknown] = "x"
    return figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], label="직각삼각형", right=[("B", "A", "C")], sides=[("A", "B", lab["a"]), ("B", "C", lab["b"]), ("A", "C", lab["c"])])


def p_basic(kinds=("hyp", "leg", "surd")):
    def mk():
        how = R.choice(kinds)
        a, b, c = R.choice(TRIPLES)
        if R.random() < 0.5:
            a, b = b, a
        if how == "hyp":
            return N("그림의 직각삼각형에서 x의 값은? (단위: cm)%s" % rtri_fig(a, b, c, "c"), c, [a + b, abs(b - a) + 1, c + 1, (a * a + b * b) // 2 if (a * a + b * b) % 2 == 0 else c - 1],
                     "x² = %d² + %d² = %d → x = <b>%d</b>" % (a, b, c * c, c))
        if how == "leg":
            return N("그림의 직각삼각형에서 x의 값은? (단위: cm)%s" % rtri_fig(a, b, c, "a"), a, [c - b, c + b if c + b < 60 else a + 2, b, a + 1],
                     "x² = %d² − %d² = %d → x = <b>%d</b>" % (c, b, a * a, a))
        p, q = R.randint(1, 7), R.randint(1, 7)
        s = p * p + q * q
        return M("두 변의 길이가 %d cm, %d cm인 직각삼각형에서 빗변의 길이는? (%d cm, %d cm인 변이 직각을 낀 두 변)" % (p, q, p, q), "%s cm" % rt(s), ["%d cm" % (p + q), "%s cm" % rt(abs(q * q - p * p) or 2), "%s cm" % rt(s + 1), "%d cm" % s],
                 "x² = %d + %d = %d → x = <b>%s cm</b>" % (p * p, q * q, s, rt(s)))
    return mk


def p_is_right():
    def mk():
        how = R.choice(["is", "kind"])
        if how == "is":
            a, b, c = R.choice(TRIPLES)
            k = R.choice([1, 2])
            ok = "%d cm, %d cm, %d cm" % (a * k if k == 1 else a, b * k if k == 1 else b, c * k if k == 1 else c)
            bad = []
            for d in (1, -1, 2):
                bad.append("%d cm, %d cm, %d cm" % (a, b, c + d))
            return M("다음 중 직각삼각형의 세 변의 길이가 될 수 있는 것은?", ok, bad, "가장 긴 변의 제곱이 나머지 두 변의 제곱의 합과 같아야 해요. <b>%s</b>" % ok)
        a, b = R.randint(3, 9), R.randint(3, 9)
        c = R.randint(max(a, b) + 1, a + b - 1)
        s, t = c * c, a * a + b * b
        ok = "직각삼각형" if s == t else ("둔각삼각형" if s > t else "예각삼각형")
        return M("세 변의 길이가 %d cm, %d cm, %d cm인 삼각형은?" % (a, b, c), ok, [x for x in ("직각삼각형", "둔각삼각형", "예각삼각형", "이등변삼각형") if x != ok],
                 "%d² = %d, %d² + %d² = %d. <b>%s</b>" % (c, s, a, b, t, ok))
    return mk


def p_apply(kinds=("rect", "square", "coord", "ladder", "iso", "box")):
    def mk():
        how = R.choice(kinds)
        a, b, c = R.choice(TRIPLES)
        if how == "rect":
            return N("가로 %d cm, 세로 %d cm인 직사각형의 대각선의 길이는?" % (a, b), c, [a + b, c + 1, a * b // c if a * b % c == 0 else c - 1, 2 * c], "√(%d² + %d²) = <b>%d cm</b>" % (a, b, c), f=cm)
        if how == "square":
            s = R.randint(2, 12)
            return M("한 변의 길이가 %d cm인 정사각형의 대각선의 길이는?" % s, "%s cm" % rt(2 * s * s), ["%d cm" % (2 * s), "%s cm" % rt(s * s * 3), "%d cm" % (s * s)], "√2 × %d = <b>%s cm</b>" % (s, rt(2 * s * s)))
        if how == "coord":
            x1, y1 = R.randint(-4, 4), R.randint(-4, 4)
            dx, dy = a * R.choice([1, -1]), b * R.choice([1, -1])
            if a > 9 or b > 9:
                return None
            return N("좌표평면 위의 두 점 A(%s, %s), B(%s, %s) 사이의 거리는?" % (neg(x1), neg(y1), neg(x1 + dx), neg(y1 + dy)), c, [a + b, c + 1, abs(dx + dy) or c + 2, c * c],
                     "√(%d² + %d²) = <b>%d</b>" % (a, b, c))
        if how == "ladder":
            return N("길이가 %d m인 사다리를 벽에 기대어 세웠더니 사다리의 아래 끝이 벽에서 %d m 떨어져 있어요. 사다리의 위 끝은 바닥에서 몇 m 높이에 있을까요?" % (c, a), b, [c - a, c + a, b + 1, a], "√(%d² − %d²) = <b>%d m</b>" % (c, a, b), f=lambda v: "%s m" % neg(v))
        if how == "iso":
            base = 2 * a
            return N("두 변의 길이가 %d cm이고 밑변의 길이가 %d cm인 이등변삼각형의 높이는?" % (c, base), b, [c - a, base, b + 1, Fr(c, 2)], "밑변의 수직이등분선이 높이예요. √(%d² − %d²) = <b>%d cm</b>" % (c, a, b), f=cm)
        s = R.randint(2, 8)
        return M("한 변의 길이가 %d cm인 정삼각형의 높이는?" % (2 * s), "%s cm" % rt(3 * s * s), ["%s cm" % rt(2 * s * s), "%d cm" % (2 * s), "%s cm" % rt(5 * s * s)], "√((%d)² − %d²) = <b>%s cm</b>" % (2 * s, s, rt(3 * s * s)))
    return mk


# ------------------------------------------------------------------ 경우의 수
def n_basic(kinds=("or", "and", "dice", "coin", "path")):
    def mk():
        how = R.choice(kinds)
        if how == "or":
            a, b = R.randint(2, 7), R.randint(2, 7)
            what = R.choice([("버스 노선", "지하철 노선", "A역에서 B역까지 버스 또는 지하철로 가는"), ("과자", "음료", "과자 또는 음료 중 하나를 고르는"), ("빵", "떡", "빵 또는 떡 중 한 가지를 고르는")])
            return N("%s %d가지, %s %d가지가 있어요. %s 경우의 수는?" % (what[0], a, what[1], b, what[2]), a + b, [a * b, a + b + 1, max(a, b), a * b - 1], "두 사건이 동시에 일어나지 않으므로 더해요. <b>%d가지</b>" % (a + b),
                     f=lambda v: "%s가지" % neg(v))
        if how == "and":
            a, b = R.randint(2, 6), R.randint(2, 6)
            what = R.choice([("티셔츠", "바지", "티셔츠와 바지를 하나씩 골라 입는"), ("빵", "음료", "빵과 음료를 하나씩 고르는"), ("A 마을에서 B 마을로 가는 길", "B 마을에서 C 마을로 가는 길", "A에서 B를 거쳐 C로 가는")])
            return N("%s %d가지, %s %d가지가 있어요. %s 경우의 수는?" % (what[0], a, what[1], b, what[2]), a * b, [a + b, a * b + 1, a ** b if a ** b < 100 else a * b * 2, a * b - 1],
                     "두 사건이 동시에 일어나므로 곱해요. <b>%d가지</b>" % (a * b), f=lambda v: "%s가지" % neg(v))
        if how == "dice":
            k = R.choice(["sum", "diff", "odd"])
            if k == "sum":
                s = R.randint(3, 11)
                c = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s)
                return N("서로 다른 두 개의 주사위를 던질 때, 나오는 눈의 수의 합이 %d인 경우의 수는?" % s, c, [c + 1, c - 1 if c > 1 else c + 2, s, 36 // s], "순서쌍으로 세면 <b>%d가지</b>" % c, f=lambda v: "%s가지" % neg(v))
            if k == "diff":
                d = R.randint(1, 4)
                c = sum(1 for i in range(1, 7) for j in range(1, 7) if abs(i - j) == d)
                return N("서로 다른 두 개의 주사위를 던질 때, 나오는 눈의 수의 차가 %d인 경우의 수는?" % d, c, [c // 2, c + 2, 6 - d, c - 1], "(큰 수, 작은 수)와 그 반대를 모두 세요. <b>%d가지</b>" % c, f=lambda v: "%s가지" % neg(v))
            return N("한 개의 주사위를 두 번 던질 때, 두 번 모두 홀수의 눈이 나오는 경우의 수는?", 9, [6, 3, 18, 12], "3 × 3 = <b>9가지</b>", f=lambda v: "%s가지" % neg(v)) if R.random() < 0.3 else None
        if how == "coin":
            n = R.randint(2, 5)
            k = R.choice(["all", "dice"])
            if k == "all":
                return N("서로 다른 동전 %d개를 동시에 던질 때, 일어나는 모든 경우의 수는?" % n, 2 ** n, [2 * n, n * n, 2 ** n - 1, n + 2], "2를 %d번 곱해요. <b>%d가지</b>" % (n, 2 ** n), f=lambda v: "%s가지" % neg(v))
            m = R.randint(1, 3)
            return N("동전 %d개와 주사위 %d개를 동시에 던질 때, 일어나는 모든 경우의 수는?" % (m, 1), 2 ** m * 6, [2 * m + 6, 2 ** m + 6, 12 * m, 6 ** m], "%s × 6 = <b>%d가지</b>" % (" × ".join(["2"] * m), 2 ** m * 6), f=lambda v: "%s가지" % neg(v))
        a, b = R.randint(2, 5), R.randint(2, 5)
        from math import comb
        return N("가로 방향으로 %d칸, 세로 방향으로 %d칸인 바둑판 모양의 길에서 왼쪽 아래 끝에서 오른쪽 위 끝까지 최단 거리로 가는 경우의 수는?" % (a, b), comb(a + b, a), [a * b, a + b, comb(a + b, a) + 1, 2 ** (a + b) if 2 ** (a + b) < 200 else comb(a + b, a) * 2],
                 "→ %d번, ↑ %d번을 늘어놓는 방법: <b>%d가지</b>" % (a, b, comb(a + b, a)), f=lambda v: "%s가지" % neg(v))
    return mk


def n_arrange(kinds=("line", "pick", "num", "comm", "adj")):
    def mk():
        how = R.choice(kinds)
        n = R.randint(3, 8)
        if how == "line":
            return N("%d명의 학생을 한 줄로 세우는 경우의 수는?" % n, math.factorial(n), [n * n, n * (n - 1), math.factorial(n - 1), 2 ** n], "%s = <b>%d가지</b>" % (" × ".join(str(i) for i in range(n, 0, -1)), math.factorial(n)),
                     f=lambda v: "%s가지" % neg(v))
        if how == "pick":
            n = R.randint(4, 9)
            r = R.choice([2, 3])
            v = math.perm(n, r)
            return N("%d명의 후보 중 %s 뽑는 경우의 수는?" % (n, "회장과 부회장을 1명씩" if r == 2 else "회장, 부회장, 총무를 1명씩"), v, [math.comb(n, r), n * r, n ** r, v // 2 if r == 3 else v + n],
                     "자격이 다르면 순서가 있어요. %s = <b>%d가지</b>" % (" × ".join(str(n - i) for i in range(r)), v), f=lambda v: "%s가지" % neg(v))
        if how == "num":
            n = R.randint(4, 7)
            z = R.choice([True, False])
            if z:
                v = (n - 1) * (n - 1)
                return N("0, 1, 2, …, %d의 숫자가 적힌 %d장의 카드 중 2장을 뽑아 만들 수 있는 두 자리 자연수의 개수는?" % (n - 1, n), v, [n * (n - 1), n * n, (n - 1) * (n - 2), v + 1],
                         "십의 자리에는 0이 올 수 없어요. %d × %d = <b>%d개</b>" % (n - 1, n - 1, v), f=lambda v: "%s개" % neg(v))
            v = n * (n - 1)
            return N("1부터 %d까지의 숫자가 적힌 %d장의 카드 중 2장을 뽑아 만들 수 있는 두 자리 자연수의 개수는?" % (n, n), v, [n * n, math.comb(n, 2), (n - 1) * (n - 1), v + n], "%d × %d = <b>%d개</b>" % (n, n - 1, v),
                     f=lambda v: "%s개" % neg(v))
        if how == "comm":
            n = R.randint(4, 10)
            r = R.choice([2, 3])
            v = math.comb(n, r)
            return N("%d명의 학생 중 대표 %d명을 뽑는 경우의 수는?" % (n, r), v, [math.perm(n, r), n * r, v + 1, n ** 2 if r == 2 else v * 2], "자격이 같으면 순서가 없어요. %d ÷ %d = <b>%d가지</b>" % (math.perm(n, r), math.factorial(r), v),
                     f=lambda v: "%s가지" % neg(v))
        n = R.randint(4, 7)
        v = math.factorial(n - 1) * 2
        return N("%d명이 한 줄로 설 때, 특정한 두 사람 A, B가 이웃하여 서는 경우의 수는?" % n, v, [math.factorial(n - 1), math.factorial(n), v // 2 * 3, v + 2],
                 "A, B를 한 묶음으로 보고 %d명을 세운 뒤 A, B가 자리를 바꿔요. %d × 2 = <b>%d가지</b>" % (n - 1, math.factorial(n - 1), v), f=lambda v: "%s가지" % neg(v))
    return mk


# ------------------------------------------------------------------ 확률
def pfr(v):
    v = Fr(v)
    if v == 0:
        return "0"
    if v == 1:
        return "1"
    return fr(v.numerator, v.denominator)


def pr_basic(kinds=("bag", "dice", "coin", "card", "not")):
    def mk():
        how = R.choice(kinds)
        if how == "bag":
            r, b, y = R.randint(1, 8), R.randint(1, 8), R.randint(0, 5)
            t = r + b + y
            c = R.choice(["빨간 공", "파란 공"])
            k = r if c == "빨간 공" else b
            p = Fr(k, t)
            body = "빨간 공 %d개, 파란 공 %d개%s" % (r, b, ", 노란 공 %d개" % y if y else "")
            return M("주머니에 %s가 들어 있어요. 한 개를 꺼낼 때 <b>%s</b>일 확률은?" % (body, c), pfr(p), [pfr(Fr(t - k, t)), pfr(Fr(k, t + 1)), pfr(Fr(1, t)), pfr(Fr(k, t - k)) if t - k and Fr(k, t - k) <= 1 else pfr(Fr(k + 1, t))],
                     "%d ÷ %d = <b>%s</b>" % (k, t, pfr(p)))
        if how == "dice":
            k = R.choice(["mult", "sum", "prime"])
            if k == "mult":
                m = R.choice([2, 3, 4])
                c = 6 // m
                return M("한 개의 주사위를 던질 때, %d의 배수의 눈이 나올 확률은?" % m, pfr(Fr(c, 6)), [pfr(Fr(1, m + 1)), pfr(Fr(c + 1, 6)), pfr(Fr(c, 12)), pfr(Fr(6 - c, 6))], "%d가지 중 %d가지. <b>%s</b>" % (6, c, pfr(Fr(c, 6))))
            if k == "prime":
                return M("한 개의 주사위를 던질 때, 소수의 눈이 나올 확률은?", pfr(Fr(3, 6)), [pfr(Fr(2, 6)), pfr(Fr(4, 6)), pfr(Fr(1, 6)), pfr(Fr(5, 6))], "2, 3, 5의 3가지. <b>½</b>") if R.random() < 0.2 else None
            s = R.randint(3, 11)
            c = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s)
            return M("서로 다른 두 개의 주사위를 던질 때, 나오는 눈의 수의 합이 %d일 확률은?" % s, pfr(Fr(c, 36)), [pfr(Fr(c, 12)), pfr(Fr(c + 1, 36)), pfr(Fr(1, s)), pfr(Fr(c, 18))], "36가지 중 %d가지. <b>%s</b>" % (c, pfr(Fr(c, 36))))
        if how == "coin":
            n = R.choice([2, 3, 4])
            k = R.randint(0, n)
            c = math.comb(n, k)
            return M("동전 %d개를 동시에 던질 때, 앞면이 %d개 나올 확률은?" % (n, k), pfr(Fr(c, 2 ** n)), [pfr(Fr(1, 2 ** n)) if c != 1 else pfr(Fr(2, 2 ** n)), pfr(Fr(k + 1, 2 * n + 2)) if Fr(k + 1, 2 * n + 2) != Fr(c, 2 ** n) else pfr(Fr(c + 1, 2 ** n)), pfr(Fr(c, 2 * n)) if Fr(c, 2 * n) <= 1 else pfr(Fr(c + 2, 2 ** n)), pfr(Fr(k, n)) if k else pfr(Fr(1, n))],
                     "%d가지 중 %d가지. <b>%s</b>" % (2 ** n, c, pfr(Fr(c, 2 ** n))))
        if how == "card":
            n = R.choice([10, 12, 15, 20, 25, 30])
            m = R.choice([3, 4, 5, 6])
            c = n // m
            return M("1부터 %d까지의 수가 적힌 카드 %d장 중 한 장을 뽑을 때, %d의 배수가 나올 확률은?" % (n, n, m), pfr(Fr(c, n)), [pfr(Fr(1, m + 1)), pfr(Fr(c + 1, n)), pfr(Fr(n - c, n)), pfr(Fr(c, n - c)) if c < n - c else pfr(Fr(c - 1, n))],
                     "%d의 배수는 %d개. <b>%s</b>" % (m, c, pfr(Fr(c, n))))
        p = Fr(R.randint(1, 9), 10) if R.random() < 0.5 else Fr(R.randint(1, 7), 8)
        return M("어떤 사건 A가 일어날 확률이 %s일 때, 사건 A가 일어나지 <b>않을</b> 확률은?" % pfr(p), pfr(1 - p), [pfr(p), pfr(Fr(1, p.numerator)) if pfr(Fr(1, p.numerator)) != pfr(1 - p) else pfr(Fr(1, 2)) if 1 - p != Fr(1, 2) else "0", "1"],
                 "1 − %s = <b>%s</b>" % (pfr(p), pfr(1 - p)))
    return mk


def pr_comb(kinds=("or", "and", "rep", "norep", "atleast")):
    def mk():
        how = R.choice(kinds)
        if how == "or":
            n = R.choice([10, 12, 15, 20])
            a, b = R.choice([(3, 5), (2, 7), (4, 5)]) if n >= 15 else R.choice([(3, 5), (2, 7)])
            ca, cb = n // a, n // b
            both = n // (a * b)
            if both:
                return None
            v = Fr(ca + cb, n)
            return M("1부터 %d까지의 수가 적힌 카드 중 한 장을 뽑을 때, %d의 배수 <b>또는</b> %d의 배수가 나올 확률은?" % (n, a, b), pfr(v), [pfr(Fr(ca * cb, n * n)), pfr(Fr(ca, n)), pfr(Fr(ca + cb + 1, n)), pfr(Fr(ca + cb, 2 * n))],
                     "동시에 일어나지 않으므로 더해요. %s + %s = <b>%s</b>" % (pfr(Fr(ca, n)), pfr(Fr(cb, n)), pfr(v)))
        if how == "and":
            p, q = Fr(R.randint(1, 4), 5), Fr(R.randint(1, 3), 4)
            nm1, nm2 = NM.next(), NM.next()
            return M("%s 문제를 맞힐 확률은 %s, %s 맞힐 확률은 %s예요. 두 사람 모두 맞힐 확률은?" % (josa(nm1, "이/가"), pfr(p), josa(nm2, "이/가"), pfr(q)), pfr(p * q), [pfr(p + q) if p + q <= 1 else pfr(1 - p * q), pfr(Fr(1, 2)) if p * q != Fr(1, 2) else "0", pfr((1 - p) * (1 - q))],
                     "동시에 일어나므로 곱해요. %s × %s = <b>%s</b>" % (pfr(p), pfr(q), pfr(p * q)))
        if how in ("rep", "norep"):
            r, b = R.randint(2, 6), R.randint(2, 6)
            t = r + b
            if how == "rep":
                v = Fr(r, t) * Fr(r, t)
                w = Fr(r, t) * Fr(r - 1, t - 1)
                return M("빨간 공 %d개, 파란 공 %d개가 든 주머니에서 공을 한 개 꺼내 확인하고 <b>다시 넣은</b> 뒤 또 한 개를 꺼낼 때, 두 번 모두 빨간 공일 확률은?" % (r, b), pfr(v), [pfr(w), pfr(Fr(r, t)), pfr(Fr(2 * r, t)) if 2 * r < t else pfr(Fr(r * r, t)), pfr(Fr(r, t) * Fr(b, t))],
                         "%s × %s = <b>%s</b>" % (pfr(Fr(r, t)), pfr(Fr(r, t)), pfr(v)))
            w = Fr(r, t) * Fr(r - 1, t - 1)
            v = Fr(r, t) * Fr(r, t)
            return M("빨간 공 %d개, 파란 공 %d개가 든 주머니에서 공을 한 개씩 <b>다시 넣지 않고</b> 두 번 꺼낼 때, 두 번 모두 빨간 공일 확률은?" % (r, b), pfr(w), [pfr(v), pfr(Fr(r, t)), pfr(Fr(r - 1, t - 1)), pfr(Fr(r, t) * Fr(b, t - 1))],
                     "%s × %s = <b>%s</b>" % (pfr(Fr(r, t)), pfr(Fr(r - 1, t - 1)), pfr(w)))
        n = R.choice([2, 3, 4])
        k = R.choice(["coin", "q"])
        if k == "coin":
            v = 1 - Fr(1, 2 ** n)
            return M("동전 %d개를 동시에 던질 때, <b>적어도 한 개는</b> 앞면이 나올 확률은?" % n, pfr(v), [pfr(Fr(1, 2 ** n)), pfr(Fr(1, 2)), pfr(Fr(n, 2 ** n)), pfr(Fr(2 ** n - 2, 2 ** n))],
                     "1 − (모두 뒷면) = 1 − %s = <b>%s</b>" % (pfr(Fr(1, 2 ** n)), pfr(v)))
        p = R.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(1, 5), Fr(2, 5), Fr(3, 5), Fr(4, 5), Fr(1, 6), Fr(5, 6)])
        t = R.choice([2, 3])
        v = 1 - (1 - p) ** t
        return M("어떤 사수가 과녁을 맞힐 확률이 %s일 때, %d번 쏘아서 <b>적어도 한 번</b> 맞힐 확률은?" % (pfr(p), t), pfr(v), [pfr(p ** t), pfr((1 - p) ** t), pfr(t * p) if t * p < 1 else pfr(p), pfr(p * (1 - p))],
                 "1 − (%d번 모두 못 맞힘) = 1 − %s = <b>%s</b>" % (t, pfr((1 - p) ** t), pfr(v)))
    return mk


def pr_concept():
    F_ = [("어떤 사건이 반드시 일어날 때, 그 확률은?", "1", ["0", "½", "100"], "<b>1</b>이에요."),
          ("절대로 일어나지 않는 사건의 확률은?", "0", ["1", "−1", "½"], "<b>0</b>이에요."),
          ("어떤 사건 A의 확률 p의 범위는?", "0 ≤ p ≤ 1", ["0 &lt; p &lt; 1", "−1 ≤ p ≤ 1", "p ≥ 1"], "<b>0 ≤ p ≤ 1</b>"),
          ("주사위 한 개를 던질 때 7의 눈이 나올 확률은?", "0", ["1", "1/7", "1/6"], "일어날 수 없으므로 <b>0</b>이에요."),
          ("주사위 한 개를 던질 때 6 이하의 눈이 나올 확률은?", "1", ["0", "5/6", "1/6"], "반드시 일어나므로 <b>1</b>이에요."),
          ("동전을 여러 번 던질수록 앞면이 나오는 상대도수는 어떤 값에 가까워질까요?", "½", ["0", "1", "앞면이 나온 횟수"], "상대도수는 확률 <b>½</b>에 가까워져요.")]
    pool = F_[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        return M(*pool.pop())
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "iso":
        return unit(G, "isosceles-triangles", 10, "[9수03-09]", "이등변삼각형의 성질을 이해하고 설명할 수 있다.",
                    "이등변삼각형의 성질과 직각삼각형의 합동", "이등변삼각형",
                    "중학교 2학년 수학 이등변삼각형 문제: 두 밑각의 크기, 꼭지각과 외각, 꼭지각의 이등분선, 이등변삼각형이 되는 조건, 직각삼각형의 RHA·RHS 합동까지 100문제와 정답·해설.",
                    "이등변삼각형의 두 밑각은 같아요", "꼭지각의 이등분선은 밑변을 수직이등분해요.",
                    ["두 변의 길이가 같은 삼각형이 <b>이등변삼각형</b>이에요. 길이가 같은 두 변이 만나는 각이 꼭지각, 나머지 두 각이 밑각이에요.",
                     "이등변삼각형의 <b>두 밑각의 크기는 같아요</b>. 거꾸로 두 내각의 크기가 같으면 이등변삼각형이에요.",
                     "꼭지각의 이등분선은 밑변을 <b>수직이등분</b>해요.",
                     "두 직각삼각형은 빗변과 한 예각이 같으면 <b>RHA 합동</b>, 빗변과 다른 한 변이 같으면 <b>RHS 합동</b>이에요."],
                    [("∠A = 40°일 때 ∠B", ["(180° − 40°) ÷ 2"], "70°"), ("∠B = 65°일 때 ∠A", ["180° − 2 × 65°"], "50°")],
                    [("꼭지각과 밑각을 바꾸어 계산한다", "같은 두 변 사이의 각이 꼭지각이에요."),
                     ("RHS와 RHA를 바꾼다", "S는 변(Side), A는 각(Angle)이에요."),
                     ("빗변이 아닌 변이 같은 경우도 RHS라고 한다", "RHS는 빗변이 반드시 같아야 해요.")],
                    [("정삼각형도 이등변삼각형인가요?", "네. 두 변의 길이가 같으니 이등변삼각형의 성질을 모두 가져요."),
                     ("종이를 접은 문제는 어떻게 푸나요?", "접은 각과 엇각이 같아서 이등변삼각형이 생기는 경우가 많아요.")],
                    [("밑각과 꼭지각", [(is_angle(("base", "top")), 20)]),
                     ("외각과 이등분선", [(is_angle(("ext", "bis")), 20)]),
                     ("이등변삼각형의 성질과 조건", [(is_cond(), 12), (is_chain(), 8)]),
                     ("직각삼각형의 합동", [(is_cond(), 20)]),
                     ("섞어서 연습", [(is_angle(), 14), (is_cond(), 6)])], 82810)
    if which == "center":
        return unit(G, "circumcenter-and-incenter", 11, "[9수03-10]", "삼각형의 외심과 내심의 성질을 이해하고 설명할 수 있다.",
                    "삼각형의 외심과 내심", "외심과 내심",
                    "중학교 2학년 수학 삼각형의 외심과 내심 문제: 외심과 내심의 뜻과 위치, ∠BOC = 2∠A, ∠BIC = 90° + ½∠A, 각의 합 90°, 내접원의 반지름과 넓이, 접선의 길이까지 100문제와 정답·해설.",
                    "외심은 꼭짓점까지, 내심은 변까지 거리가 같아요", "∠BOC = 2∠A, ∠BIC = 90° + ½∠A",
                    ["<b>외심</b>(O)은 세 변의 수직이등분선의 교점이고, 세 꼭짓점까지의 거리가 같아요(외접원의 중심).",
                     "<b>내심</b>(I)은 세 내각의 이등분선의 교점이고, 세 변까지의 거리가 같아요(내접원의 중심).",
                     "외심: ∠BOC = 2∠A, ∠OAB + ∠OBC + ∠OCA = 90°. 직각삼각형의 외심은 빗변의 중점이에요.",
                     "내심: ∠BIC = 90° + ½∠A. 넓이 = ½ × r × (세 변의 길이의 합)"],
                    [("외심, ∠A = 50°", ["2 × 50°"], "∠BOC = 100°"), ("내심, ∠A = 60°", ["90° + 30°"], "∠BIC = 120°")],
                    [("외심과 내심의 성질을 바꾼다", "외(外)심은 바깥 원(외접원), 내(內)심은 안쪽 원(내접원)의 중심이에요."),
                     ("∠BIC = 2∠A라고 한다", "내심은 90° + ½∠A예요."),
                     ("내심이 삼각형 밖에 있을 수 있다고 한다", "내심은 항상 안에 있어요.")],
                    [("외심은 항상 삼각형 안에 있나요?", "예각삼각형은 안, 직각삼각형은 빗변의 중점, 둔각삼각형은 밖에 있어요."),
                     ("실생활 예는?", "세 마을에서 같은 거리에 있는 곳은 외심, 세 도로에서 같은 거리에 있는 곳은 내심이에요.")],
                    [("외심과 내심의 뜻", [(c_concept(), 10), (c_outer(("dist", "right")), 10)]),
                     ("외심과 각", [(c_outer(("ang", "sum")), 20)]),
                     ("내심과 각", [(c_inner(("ang", "sum")), 20)]),
                     ("내접원", [(c_inner(("area", "dist")), 20)]),
                     ("섞어서 연습", [(c_outer(), 10), (c_inner(), 10)])], 82811)
    if which == "quad":
        return unit(G, "properties-of-quadrilaterals", 12, "[9수03-11]", "사각형의 성질을 이해하고 설명할 수 있다.",
                    "평행사변형과 여러 가지 사각형의 성질", "사각형의 성질",
                    "중학교 2학년 수학 사각형의 성질 문제: 평행사변형의 대변·대각·대각선, 평행사변형이 되는 조건, 직사각형·마름모·정사각형의 대각선, 사각형 사이의 관계, 넓이까지 100문제와 정답·해설.",
                    "평행사변형: 대변·대각이 같고 대각선이 서로 이등분", "직사각형은 대각선의 길이가 같고, 마름모는 대각선이 수직이에요.",
                    ["<b>평행사변형</b>은 두 쌍의 대변이 각각 평행하고, 대변의 길이와 대각의 크기가 같으며, 두 대각선이 서로를 이등분해요.",
                     "<b>직사각형</b>은 네 각이 직각이고 두 대각선의 길이가 같아요. <b>마름모</b>는 네 변이 같고 두 대각선이 수직이에요.",
                     "<b>정사각형</b>은 직사각형과 마름모의 성질을 모두 가져요.",
                     "평행사변형의 넓이는 한 대각선으로 이등분, 두 대각선으로 4등분돼요."],
                    [("∠A = 110°인 평행사변형의 ∠B", ["180° − 110°"], "70°"), ("대각선 10 cm, 8 cm인 마름모의 넓이", ["10 × 8 ÷ 2"], "40 cm²")],
                    [("평행사변형의 대각선의 길이가 같다고 한다", "같은 것은 직사각형이에요. 평행사변형은 서로 이등분만 해요."),
                     ("마름모는 직사각형이라고 한다", "마름모의 각은 직각이 아닐 수 있어요."),
                     ("이웃한 두 각이 같다고 한다", "평행사변형은 대각이 같고, 이웃한 두 각의 합이 180°예요.")],
                    [("사각형 사이의 관계는?", "정사각형 ⊂ 직사각형, 마름모 ⊂ 평행사변형 ⊂ 사다리꼴이에요."),
                     ("등변사다리꼴의 성질은?", "아랫변의 양 끝 각이 같고, 두 대각선의 길이가 같아요.")],
                    [("평행사변형의 각과 변", [(q_para(("ang", "side")), 20)]),
                     ("평행사변형의 대각선", [(q_para(("diag", "x")), 20)]),
                     ("여러 가지 사각형", [(q_kind(("has", "hasnt")), 10), (q_kind(("cond", "inc")), 10)]),
                     ("넓이", [(q_area(), 20)]),
                     ("섞어서 연습", [(q_para(), 10), (q_area(), 10)])], 82812)
    if which == "sim":
        return unit(G, "similar-figures", 13, "[9수03-12] [9수03-13]", "도형의 닮음의 의미와 닮은 도형의 성질을 이해하고, 닮음비를 구할 수 있다. 삼각형의 닮음 조건을 이해하고, 이를 이용하여 두 삼각형이 닮음인지 판별할 수 있다.",
                    "도형의 닮음과 삼각형의 닮음 조건", "도형의 닮음",
                    "중학교 2학년 수학 도형의 닮음 문제: 닮음비와 대응변, 둘레·넓이·부피의 비, SSS·SAS·AA 닮음 조건, 평행선으로 만든 닮은 삼각형, 직각삼각형의 닮음까지 100문제와 정답·해설.",
                    "닮음비가 m : n이면 넓이의 비는 m² : n²", "부피의 비는 m³ : n³이에요.",
                    ["한 도형을 일정한 비율로 확대하거나 축소한 도형과 합동일 때 두 도형은 <b>닮음</b>(∽)이에요.",
                     "대응변의 길이의 비가 <b>닮음비</b>이고, 대응각의 크기는 같아요.",
                     "삼각형의 닮음 조건: <b>SSS</b>(세 변의 비), <b>SAS</b>(두 변의 비와 끼인각), <b>AA</b>(두 각)",
                     "닮음비가 m : n이면 둘레의 비는 m : n, 넓이의 비는 m² : n², 부피의 비는 m³ : n³이에요."],
                    [("닮음비 2 : 3, 작은 넓이 8", ["4 : 9 = 8 : x"], "18"), ("AA 닮음", ["두 각이 같음"], "닮음")],
                    [("넓이의 비를 닮음비와 같다고 한다", "넓이는 제곱의 비예요."),
                     ("대응하지 않는 변끼리 비를 세운다", "∽ 기호 앞뒤의 꼭짓점 순서대로 대응시켜요."),
                     ("부피의 비를 제곱으로 한다", "부피는 세제곱의 비예요.")],
                    [("합동과 닮음의 관계는?", "합동은 닮음비가 1 : 1인 닮음이에요."),
                     ("항상 닮은 도형은?", "두 원, 두 정사각형, 두 구처럼 모양이 하나로 정해진 도형은 항상 닮음이에요.")],
                    [("닮음비와 대응변", [(s_ratio(("side", "peri")), 20)]),
                     ("넓이와 부피의 비", [(s_ratio(("area", "vol", "ratio")), 20)]),
                     ("삼각형의 닮음 조건", [(s_cond(("cond", "find")), 20)]),
                     ("직각삼각형의 닮음", [(s_cond(("right",)), 8), (s_cond(("find",)), 12)]),
                     ("섞어서 연습", [(s_ratio(), 12), (s_cond(), 8)])], 82813)
    if which == "ratio":
        return unit(G, "parallel-lines-and-segment-ratios", 14, "[9수03-14]", "평행선 사이의 선분의 길이의 비를 구할 수 있다.",
                    "평행선과 선분의 길이의 비", "평행선과 선분의 비",
                    "중학교 2학년 수학 평행선과 선분의 길이의 비 문제: 삼각형에서 평행선과 선분의 비, 중점연결정리, 평행선 사이의 선분의 비, 각의 이등분선, 무게중심까지 100문제와 정답·해설.",
                    "DE ∥ BC이면 AD : DB = AE : EC", "두 변의 중점을 이은 선분은 나머지 변의 ½이에요.",
                    ["△ABC에서 DE ∥ BC이면 AD : AB = AE : AC = DE : BC, AD : DB = AE : EC예요.",
                     "삼각형의 두 변의 중점을 연결한 선분은 나머지 변과 평행하고, 길이는 그 <b>½</b>이에요.",
                     "세 개 이상의 평행선이 다른 두 직선과 만나서 생긴 선분의 길이의 비는 같아요.",
                     "삼각형의 무게중심은 세 중선의 교점이고, 중선을 꼭짓점으로부터 <b>2 : 1</b>로 나누어요."],
                    [("AD = 4, DB = 2, AE = 6", ["4 : 2 = 6 : x"], "EC = 3"), ("중선 AD = 12", ["⅔ × 12"], "AG = 8")],
                    [("AD : DB = DE : BC라고 한다", "DE : BC는 AD : AB와 같아요."),
                     ("무게중심이 중선을 1 : 2로 나눈다고 한다", "꼭짓점 쪽이 2예요."),
                     ("중점을 이은 선분의 길이를 나머지 변과 같다고 한다", "½이에요.")],
                    [("왜 비가 같나요?", "평행선 때문에 동위각이 같아 △ADE ∽ △ABC가 돼요."),
                     ("무게중심은 실생활에서?", "삼각형 모양 판을 한 점으로 받칠 때 균형이 잡히는 점이에요.")],
                    [("삼각형과 평행선", [(r_tri(("side",)), 20)]),
                     ("중점연결정리", [(r_tri(("mid",)), 20)]),
                     ("평행선과 각의 이등분선", [(r_tri(("par3", "bis")), 20)]),
                     ("무게중심", [(r_centroid(), 20)]),
                     ("섞어서 연습", [(r_tri(), 12), (r_centroid(), 8)])], 82814)
    if which == "pyth":
        return unit(G, "pythagorean-theorem", 15, "[9수03-15]", "피타고라스 정리를 이해하고 설명할 수 있다.",
                    "피타고라스 정리와 활용", "피타고라스 정리",
                    "중학교 2학년 수학 피타고라스 정리 문제: 빗변과 다른 변의 길이 구하기, 직각삼각형이 되는 조건, 예각·둔각삼각형 판별, 직사각형·정사각형의 대각선, 두 점 사이의 거리, 사다리, 정삼각형의 높이까지 100문제와 정답·해설.",
                    "a² + b² = c² (c는 빗변)", "가장 긴 변의 제곱 = 나머지 두 변의 제곱의 합이면 직각삼각형이에요.",
                    ["직각삼각형에서 직각을 낀 두 변의 길이를 a, b, 빗변의 길이를 c라 하면 <b>a² + b² = c²</b>이에요.",
                     "거꾸로 세 변의 길이가 a² + b² = c²을 만족하면 빗변이 c인 직각삼각형이에요.",
                     "c² &lt; a² + b²이면 예각삼각형, c² &gt; a² + b²이면 둔각삼각형이에요(c는 가장 긴 변).",
                     "직사각형의 대각선, 좌표평면 위의 두 점 사이의 거리도 피타고라스 정리로 구해요."],
                    [("6, 8인 직각삼각형의 빗변", ["36 + 64 = 100"], "10"), ("빗변 13, 한 변 5", ["169 − 25 = 144"], "12")],
                    [("빗변이 아닌 변을 c로 놓는다", "c는 직각의 맞은편, 가장 긴 변이에요."),
                     ("a + b = c로 계산한다", "제곱해서 더해요."),
                     ("√(a² + b²)를 a + b로 쓴다", "√(9 + 16) = 5이지 3 + 4 = 7이 아니에요.")],
                    [("√가 나오면 어떻게 하나요?", "√8 = 2√2처럼 간단히 나타내요. 3학년에서 자세히 배워요."),
                     ("피타고라스 수는?", "(3, 4, 5), (5, 12, 13), (8, 15, 17)처럼 자연수로 된 세 변이에요.")],
                    [("빗변의 길이", [(p_basic(("hyp", "surd")), 20)]),
                     ("다른 변의 길이", [(p_basic(("leg",)), 20)]),
                     ("직각삼각형이 되는 조건", [(p_is_right(), 20)]),
                     ("평면도형에서의 활용", [(p_apply(("rect", "square", "iso", "box")), 20)]),
                     ("실생활과 좌표에서의 활용", [(p_apply(("coord", "ladder")), 20)])], 82815)
    if which == "count":
        return unit(G, "counting", 16, "[9수04-05]", "경우의 수를 구할 수 있다.",
                    "경우의 수: 합의 법칙과 곱의 법칙", "경우의 수",
                    "중학교 2학년 수학 경우의 수 문제: 또는(합의 법칙)과 동시에(곱의 법칙), 주사위와 동전, 최단 거리, 한 줄로 세우기, 대표 뽑기, 자연수 만들기, 이웃하여 서기까지 100문제와 정답·해설.",
                    "'또는'은 더하고 '동시에'는 곱해요", "순서가 있으면 n × (n − 1), 없으면 그 값을 2로 나누어요.",
                    ["사건 A, B가 동시에 일어나지 않을 때 A <b>또는</b> B가 일어나는 경우의 수는 m + n이에요(합의 법칙).",
                     "A와 B가 <b>동시에</b> 일어나는 경우의 수는 m × n이에요(곱의 법칙).",
                     "n명을 한 줄로 세우는 경우의 수는 n × (n − 1) × … × 1이에요.",
                     "n명 중 자격이 다른 2명: n × (n − 1), 자격이 같은 2명: n × (n − 1) ÷ 2"],
                    [("티셔츠 3, 바지 2", ["3 × 2"], "6가지"), ("5명 중 대표 2명", ["5 × 4 ÷ 2"], "10가지")],
                    [("'또는'인데 곱한다", "동시에 일어나지 않으면 더해요."),
                     ("대표 2명을 n × (n − 1)로 센다", "자격이 같으면 순서가 없어 2로 나누어요."),
                     ("두 자리 수를 만들 때 0을 십의 자리에 둔다", "십의 자리에는 0이 올 수 없어요.")],
                    [("주사위 두 개는 서로 다른가요?", "서로 다른 주사위는 (1, 2)와 (2, 1)을 다르게 세요."),
                     ("나뭇가지 그림은 언제 쓰나요?", "경우를 빠짐없이, 중복 없이 셀 때 편해요.")],
                    [("합의 법칙과 곱의 법칙", [(n_basic(("or", "and")), 20)]),
                     ("주사위와 동전", [(n_basic(("dice", "coin")), 16), (n_basic(("path",)), 4)]),
                     ("한 줄로 세우기와 뽑기", [(n_arrange(("line", "adj", "pick")), 20)]),
                     ("대표 뽑기와 수 만들기", [(n_arrange(("num", "comm")), 20)]),
                     ("섞어서 연습", [(n_basic(("path",)), 6), (n_basic(("or", "and")), 14)])], 82816)
    if which == "prob":
        return unit(G, "probability", 17, "[9수04-06]", "확률의 개념과 그 기본 성질을 이해하고, 확률을 구할 수 있다.",
                    "확률의 뜻과 성질, 확률의 계산", "확률",
                    "중학교 2학년 수학 확률 문제: 확률의 뜻, 0과 1, 어떤 사건이 일어나지 않을 확률, 주머니·주사위·동전·카드, 또는과 동시에의 확률, 꺼낸 것을 다시 넣거나 넣지 않는 경우, 적어도 한 번까지 100문제와 정답·해설.",
                    "확률 = 사건의 경우의 수 ÷ 모든 경우의 수", "적어도 한 번 = 1 − (한 번도 일어나지 않을 확률)",
                    ["모든 경우가 같은 정도로 일어날 때, 사건 A가 일어날 확률은 (A가 일어나는 경우의 수) ÷ (모든 경우의 수)예요.",
                     "확률 p는 0 ≤ p ≤ 1이고, 반드시 일어나면 1, 절대 일어나지 않으면 0이에요.",
                     "A가 일어나지 않을 확률은 1 − p예요. '적어도 한 번'은 1 − (한 번도 일어나지 않을 확률)로 구해요.",
                     "동시에 일어나지 않는 두 사건의 '또는'은 더하고, 서로 영향을 주지 않는 두 사건이 '동시에' 일어날 확률은 곱해요."],
                    [("주사위에서 짝수", ["3 ÷ 6"], "½"), ("동전 2개, 적어도 한 개 앞면", ["1 − ¼"], "¾")],
                    [("'또는'의 확률을 곱한다", "동시에 일어나지 않으면 더해요."),
                     ("꺼낸 공을 다시 넣지 않았는데 분모를 그대로 둔다", "두 번째는 전체가 1개 줄어요."),
                     ("확률이 1보다 크게 나온다", "확률은 0 이상 1 이하예요. 계산을 다시 확인해요.")],
                    [("상대도수와 확률의 관계는?", "시행 횟수가 많아질수록 상대도수는 확률에 가까워져요."),
                     ("확률은 분수로 써야 하나요?", "보통 기약분수로 나타내요.")],
                    [("확률의 뜻", [(pr_basic(("bag", "card")), 14), (pr_concept(), 6)]),
                     ("주사위와 동전", [(pr_basic(("dice", "coin")), 20)]),
                     ("일어나지 않을 확률", [(pr_basic(("not",)), 10), (pr_comb(("atleast",)), 10)]),
                     ("또는과 동시에", [(pr_comb(("or", "and")), 20)]),
                     ("꺼내기와 섞어서 연습", [(pr_comb(("rep", "norep")), 14), (pr_basic(("bag",)), 6)])], 82817)
    raise ValueError(which)
