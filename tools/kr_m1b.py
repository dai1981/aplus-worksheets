# -*- coding: utf-8 -*-
"""
대한민국 중학교 1학년 수학（2022 개정）：도형과 측정・자료와 가능성の 9 単元
  basic : 기본 도형（점・선・면・각、맞꼭지각、위치 관계、평행선의 동위각・엇각）[9수03-01] [9수03-02]
  cong  : 작도와 합동 [9수03-03] [9수03-04]
  poly  : 다각형（대각선、내각과 외각）[9수03-05]
  sector: 원과 부채꼴 [9수03-06]
  solid : 다면체와 회전체 [9수03-07]
  area  : 입체도형의 겉넓이와 부피 [9수03-08]
  rep   : 대푯값（평균・중앙값・최빈값）[9수04-01]
  freq  : 줄기와 잎 그림・도수분포표・히스토그램 [9수04-02]
  rel   : 상대도수 [9수04-03]
誤答は「맞꼭지각을 보각으로 본다」「엇각과 동위각을 헷갈린다」「대각선의 수를 n(n − 3)으로 센다」「내각의 합을 180° × n으로 한다」
「부채꼴의 넓이에 반지름 대신 지름을 쓴다」「원뿔의 부피에 1/3을 곱하지 않는다」「짝수 개 자료의 중앙값을 하나만 고른다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_common import josa, Names, num, fr, table
from kr_mid import M, N, neg, P, sup, dec, unit, figure, fig, svg_wrap, text, line, INK, RED, BLUE, GREEN, FILL

R = random.Random(82710)
NM = Names(R)
G = "grade-7"


_D = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


def kn(n):
    """3 → 삼, 12 → 십이, 24 → 이십사（다각형 이름）"""
    n = int(Fr(n))
    t, o = divmod(n, 10)
    return ("" if t == 0 else ("" if t == 1 else _D[t]) + "십") + _D[o]


def deg(v):
    return "%s°" % neg(v)


def pi(v, u=""):
    """계수 × π：6π, 9/2π"""
    v = Fr(v)
    if v == 0:
        return "0"
    c = "" if v == 1 else (num(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator))
    return c + "π" + ((" " + u) if u else "")


def svgf(W, H, body, label, lg=True):
    s = svg_wrap(int(W), int(H), body, label)
    if lg:
        s = s.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(s)


# ------------------------------------------------------------------ 그림
def cross_svg(a, labels):
    """두 직선이 만나는 그림：a = 한 각（도）, labels = {0..3: 문자열}（오른쪽 위부터 반시계）"""
    cx, cy, Lr = 160, 110, 120
    s = []
    t1 = 0.0
    t2 = math.radians(a)
    for t in (t1, t2):
        s.append(line(cx - Lr * math.cos(t), cy + Lr * math.sin(t), cx + Lr * math.cos(t), cy - Lr * math.sin(t), INK, 2.4))
    mids = [a / 2, a + (180 - a) / 2, 180 + a / 2, 180 + a + (180 - a) / 2]
    for i, m in enumerate(mids):
        if i in labels:
            r = 42 if len(labels[i]) <= 4 else 62
            s.append(text(cx + r * math.cos(math.radians(m)), cy - r * math.sin(math.radians(m)) + 6, labels[i], 17, col=BLUE if "°" in labels[i] else RED))
    return svgf(320, 220, "".join(s), "두 직선이 만나서 생긴 각")


def parallel_svg(a, labels):
    """평행선 l, m과 한 직선 n：a = 직선 n과 l이 이루는 각（오른쪽 위）. labels = {(위/아래, 0..3): 문자열}"""
    W, H = 340, 250
    y1, y2 = 70, 180
    t = math.radians(a)
    x1 = 150
    x2 = x1 - (y2 - y1) / math.tan(t)
    s = [line(20, y1, W - 40, y1, INK, 2.4), line(20, y2, W - 40, y2, INK, 2.4), text(W - 26, y1 + 6, "l", 18, italic=True), text(W - 26, y2 + 6, "m", 18, italic=True)]
    ext = 50
    dx, dy = math.cos(t), -math.sin(t)
    s.append(line(x2 - dx * ext, y2 - dy * ext, x1 + dx * ext, y1 + dy * ext, INK, 2.4))
    mids = [a / 2, a + (180 - a) / 2, 180 + a / 2, 180 + a + (180 - a) / 2]
    for (row, i), lab in labels.items():
        cx, cy = (x1, y1) if row == 0 else (x2, y2)
        m = math.radians(mids[i])
        s.append(text(cx + 34 * math.cos(m), cy - 34 * math.sin(m) + 6, lab, 16, col=BLUE if "°" in lab else RED))
    return svgf(W, H, "".join(s), "평행선과 한 직선이 만나서 생긴 각")


# ------------------------------------------------------------------ 기본 도형
def b_count():
    def mk():
        how = R.choice(["solid", "line", "seg"])
        if how == "solid":
            n = R.randint(3, 10)
            k = R.choice(["prism", "pyramid"])
            if k == "prism":
                v, e = 2 * n, 3 * n
                nm = "%s각기둥" % kn(n)
            else:
                v, e = n + 1, 2 * n
                nm = "%s각뿔" % kn(n)
            ask = R.choice(["교점", "교선"])
            a = v if ask == "교점" else e
            return N("<b>%s</b>에서 %s의 개수는?" % (nm, ask), a, [e if ask == "교점" else v, a + 1, a - n], "입체도형에서 교점의 개수는 꼭짓점의 수, 교선의 개수는 모서리의 수와 같아요. <b>%d개</b>" % a, f=lambda x: "%s개" % neg(x))
        n = R.randint(3, 6)
        if how == "line":
            c = n * (n - 1) // 2
            return N("어느 세 점도 한 직선 위에 있지 않은 서로 다른 %d개의 점 중 두 점을 지나는 <b>직선</b>은 모두 몇 개일까요?" % n, c, [n * (n - 1), n, c + 1],
                     "두 점마다 직선이 하나씩: %d × %d ÷ 2 = <b>%d개</b>" % (n, n - 1, c), f=lambda x: "%s개" % neg(x))
        c = n * (n - 1) // 2
        k = R.choice(["직선", "반직선", "선분"])
        v = {"직선": 1, "반직선": 2 * (n - 1), "선분": c}[k]
        return N("한 직선 위에 있는 서로 다른 %d개의 점 중 두 점으로 만들 수 있는 서로 다른 <b>%s</b>은 몇 개일까요?" % (n, k), v,
                 [c, 2 * (n - 1) if k != "반직선" else c, n, n * (n - 1)], "한 직선 위의 점이므로 직선 1개, 반직선 %d개, 선분 %d개예요. <b>%d개</b>" % (2 * (n - 1), c, v), f=lambda x: "%s개" % neg(x))
    return mk


def b_vertical():
    def mk():
        a = R.choice([40, 50, 55, 60, 65, 70, 75, 80, 110, 120, 130])
        how = R.choice(["vert", "supp", "expr"])
        if how == "vert":
            return N("두 직선이 만나서 생긴 각이에요. ∠x의 크기는?%s" % cross_svg(a, {0: deg(a), 2: "x"}), a, [180 - a, 90 - a if a < 90 else a - 90, 360 - a],
                     "맞꼭지각의 크기는 같아요. <b>%d°</b>" % a, f=deg)
        if how == "supp":
            return N("두 직선이 만나서 생긴 각이에요. ∠x의 크기는?%s" % cross_svg(a, {0: deg(a), 1: "x"}), 180 - a, [a, 360 - a, 90 - a if a < 90 else 270 - a],
                     "평각은 180°예요. 180° − %d° = <b>%d°</b>" % (a, 180 - a), f=deg)
        x = R.randint(10, 30)
        k = R.choice([2, 3])
        b = R.randint(5, 30)
        a = k * x + b
        if a >= 170:
            return None
        return N("맞꼭지각인 두 각의 크기가 (%dx + %d)°와 %d°일 때, x의 값은?%s" % (k, b, a, cross_svg(a, {0: "(%dx+%d)°" % (k, b), 2: deg(a)})), x,
                 [Fr(180 - a - b, k), Fr(a + b, k), x + 5], "맞꼭지각이므로 %dx + %d = %d, x = <b>%d</b>" % (k, b, a, x))
    return mk


def b_parallel():
    def mk():
        a = R.choice([45, 50, 55, 60, 65, 70, 75, 110, 115, 120, 125, 130])
        how = R.choice(["corr", "alt", "co", "ask"])
        if how == "corr":
            return N("두 직선 l, m이 평행할 때, ∠x의 크기는?%s" % parallel_svg(a, {(0, 0): deg(a), (1, 0): "x"}), a, [180 - a, 90 - a if a < 90 else a - 90, 2 * a if a < 90 else 360 - a],
                     "l ∥ m이면 동위각의 크기는 같아요. <b>%d°</b>" % a, f=deg)
        if how == "alt":
            return N("두 직선 l, m이 평행할 때, ∠x의 크기는?%s" % parallel_svg(a, {(0, 2): deg(a), (1, 0): "x"}), a, [180 - a, 90 - a if a < 90 else a - 90, 360 - a],
                     "l ∥ m이면 엇각의 크기는 같아요. <b>%d°</b>" % a, f=deg)
        if how == "co":
            return N("두 직선 l, m이 평행할 때, ∠x의 크기는?%s" % parallel_svg(a, {(0, 0): deg(a), (1, 1): "x"}), 180 - a, [a, 90 + a if a < 90 else a - 90, 360 - a],
                     "동위각 %d°와 ∠x는 한 직선 위에서 평각을 이뤄요. 180° − %d° = <b>%d°</b>" % (a, a, 180 - a), f=deg)
        pos = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
        p = R.choice([(0, 2), (0, 3)])
        kind = R.choice(["동위각", "엇각"])
        if kind == "동위각":
            tgt = (1, p[1])
        else:
            tgt = (1, {2: 0, 3: 1}[p[1]])
        names = "abcdefgh"
        labels = {q: names[i] for i, q in enumerate(pos)}
        ok = names[pos.index(tgt)]
        bad = [names[i] for i, q in enumerate(pos) if q not in (tgt, p) and q[0] == 1] + [names[pos.index((0, (p[1] + 2) % 4))]]
        return M("그림에서 ∠%s의 <b>%s</b>은?%s" % (names[pos.index(p)], kind, parallel_svg(a, labels)), "∠" + ok, ["∠" + b for b in bad],
                 "%s은 %s. <b>∠%s</b>" % (kind, "같은 위치에 있는 각이에요" if kind == "동위각" else "엇갈린 위치(두 직선 사이)에 있는 각이에요", ok))
    return mk


def b_position():
    F = [("직육면체 ABCD-EFGH에서 모서리 AB와 꼬인 위치에 있는 모서리는 모두 몇 개일까요?", "4개", ["2개", "3개", "6개"], "만나지도 않고 평행하지도 않은 모서리: CG, DH, EH, FG → <b>4개</b>"),
         ("직육면체에서 한 모서리와 평행한 모서리는 모두 몇 개일까요?", "3개", ["2개", "4개", "1개"], "한 모서리와 평행한 모서리는 <b>3개</b>예요."),
         ("직육면체에서 한 모서리와 수직으로 만나는 모서리는 모두 몇 개일까요?", "4개", ["2개", "3개", "8개"], "양 끝점에서 2개씩 → <b>4개</b>"),
         ("공간에서 두 직선의 위치 관계가 아닌 것은?", "한 점에서 만나면서 평행하다", ["한 점에서 만난다", "평행하다", "꼬인 위치에 있다"], "두 직선은 만나거나, 평행하거나, 꼬인 위치에 있어요."),
         ("꼬인 위치에 대한 설명으로 옳은 것은?", "공간에서 만나지도 않고 평행하지도 않다", ["평면에서도 생긴다", "한 점에서 만난다", "평행하다"], "꼬인 위치는 공간에서만 생겨요."),
         ("직육면체에서 한 면과 평행한 면은 몇 개일까요?", "1개", ["2개", "4개", "0개"], "마주 보는 면 <b>1개</b>예요."),
         ("직육면체에서 한 면과 수직인 면은 몇 개일까요?", "4개", ["2개", "1개", "5개"], "옆에 있는 면 <b>4개</b>예요."),
         ("직육면체에서 한 면과 평행한 모서리는 몇 개일까요?", "4개", ["2개", "8개", "1개"], "마주 보는 면의 모서리 <b>4개</b>예요."),
         ("한 평면 위에 있는 두 직선이 만나지 않으면 두 직선은?", "평행하다", ["꼬인 위치에 있다", "수직이다", "일치한다"], "평면에서 만나지 않는 두 직선은 <b>평행</b>해요."),
         ("점 A에서 직선 l에 내린 수선의 발을 H라 할 때, 점 A와 직선 l 사이의 거리는?", "선분 AH의 길이", ["선분 AH의 길이의 2배", "직선 l의 길이", "점 H에서 l까지의 거리"], "수선의 발까지의 거리예요.")]
    pool = F[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        return M(*pool.pop())
    return mk


def b_angle_sum():
    def mk():
        how = R.choice(["right", "straight", "ratio"])
        if how == "right":
            a = R.randint(15, 70)
            return N("∠AOB = 90°이고 ∠AOC = %d°일 때, ∠COB의 크기는? (점 C는 ∠AOB의 안쪽)" % a, 90 - a, [180 - a, a, 90 + a], "90° − %d° = <b>%d°</b>" % (a, 90 - a), f=deg)
        if how == "straight":
            a, b = R.randint(20, 70), R.randint(20, 70)
            return N("한 직선 위에서 세 각의 크기가 %d°, ∠x, %d°예요. ∠x의 크기는?" % (a, b), 180 - a - b, [360 - a - b, 90 - a if a < 90 else 10, a + b], "평각 180°에서 빼요. <b>%d°</b>" % (180 - a - b), f=deg)
        p, q, r = R.choice([(1, 2, 3), (2, 3, 4), (1, 3, 5), (2, 3, 5), (1, 4, 5)])
        k = R.choice(["가장 큰", "가장 작은"])
        v = 180 * (r if k == "가장 큰" else p) // (p + q + r)
        if 180 * (r if k == "가장 큰" else p) % (p + q + r):
            return None
        return N("평각을 세 각으로 나누었더니 크기의 비가 %d : %d : %d예요. %s 각의 크기는?" % (p, q, r, k), v, [180 * q // (p + q + r), v + 10, 360 * (r if k == "가장 큰" else p) // (p + q + r)],
                 "180° × %d/%d = <b>%d°</b>" % (r if k == "가장 큰" else p, p + q + r, v), f=deg)
    return mk


# ------------------------------------------------------------------ 작도와 합동
def g_construct():
    F = [("작도할 때 쓰는 도구는?", "눈금 없는 자와 컴퍼스", ["눈금 있는 자와 각도기", "각도기와 컴퍼스", "삼각자와 각도기"], "작도는 <b>눈금 없는 자와 컴퍼스</b>만 써요."),
         ("작도에서 컴퍼스의 역할은?", "원을 그리거나 선분의 길이를 옮긴다", ["두 점을 이어 선분을 그린다", "각의 크기를 잰다", "길이를 잰다"], "선분은 자로, 길이 옮기기와 원은 <b>컴퍼스</b>로 해요."),
         ("작도에서 눈금 없는 자의 역할은?", "두 점을 지나는 선분을 그린다", ["길이를 잰다", "원을 그린다", "각의 크기를 잰다"], "눈금 없는 자로는 <b>선분을 긋기만</b> 해요."),
         ("크기가 같은 각의 작도에 쓰이는 성질은?", "세 변의 길이가 같은 삼각형은 합동이다", ["두 각의 크기가 같으면 합동이다", "맞꼭지각의 크기는 같다", "평행선의 동위각은 같다"],
          "같은 반지름의 원으로 만든 두 삼각형이 SSS 합동이에요."),
         ("평행선의 작도에 쓰이는 성질은?", "동위각(또는 엇각)의 크기가 같으면 두 직선은 평행하다", ["맞꼭지각은 같다", "삼각형의 내각의 합은 180°", "SSS 합동"], "크기가 같은 각을 작도해 평행선을 그려요.")]
    pool = F[:]
    R.shuffle(pool)

    def mk():
        if pool and R.random() < 0.4:
            return M(*pool.pop())
        how = R.choice(["sides", "given"])
        if how == "sides":
            a, b = R.sample(range(3, 10), 2)
            lo, hi = abs(a - b) + 1, a + b - 1
            ok = R.randint(lo, hi)
            bad = [a + b, abs(a - b), a + b + R.randint(1, 3)]
            return N("두 변의 길이가 %d cm, %d cm인 삼각형을 그리려고 해요. 나머지 한 변의 길이가 될 수 있는 것은?" % (a, b), ok, bad,
                     "(두 변의 차) &lt; (나머지 한 변) &lt; (두 변의 합): %d &lt; x &lt; %d. <b>%d cm</b>" % (abs(a - b), a + b, ok), f=lambda x: "%s cm" % neg(x))
        if R.random() < 0.6:
            OK, NO, CANT = "하나로 정해져요", "하나로 정해지지 않아요", "삼각형을 그릴 수 없어요"
            k = R.choice(["SSS", "SSSx", "SAS", "ASA", "ASAx", "AAA", "SSA"])
            a, b, c = R.randint(3, 9), R.randint(3, 9), R.randint(3, 9)
            p_, q_ = R.randint(30, 80), R.randint(30, 80)
            if k == "SSS":
                if not (max(a, b, c) < a + b + c - max(a, b, c)):
                    return None
                d, ans, why = "AB = %d cm, BC = %d cm, CA = %d cm" % (a, b, c), OK, "세 변의 길이가 주어졌고 가장 긴 변이 나머지 두 변의 합보다 짧아요."
            elif k == "SSSx":
                c = a + b + R.randint(0, 2)
                d, ans, why = "AB = %d cm, BC = %d cm, CA = %d cm" % (a, b, c), CANT, "%d ≥ %d + %d이므로 삼각형이 되지 않아요." % (c, a, b)
            elif k == "SAS":
                d, ans, why = "AB = %d cm, BC = %d cm, ∠B = %d°" % (a, b, p_), OK, "두 변과 그 끼인각이 주어졌어요."
            elif k == "ASA":
                d, ans, why = "BC = %d cm, ∠B = %d°, ∠C = %d°" % (a, p_, q_), OK, "한 변과 그 양 끝 각이 주어졌어요."
            elif k == "ASAx":
                q_ = 180 - p_ + R.randint(0, 20)
                d, ans, why = "BC = %d cm, ∠B = %d°, ∠C = %d°" % (a, p_, q_), CANT, "두 각의 합이 180° 이상이라 삼각형이 되지 않아요."
            elif k == "AAA":
                d, ans, why = "∠A = %d°, ∠B = %d°, ∠C = %d°" % (p_, q_, 180 - p_ - q_), NO, "세 각만으로는 크기가 다른 삼각형이 많이 생겨요."
                if 180 - p_ - q_ <= 0:
                    return None
            else:
                d, ans, why = "AB = %d cm, BC = %d cm, ∠A = %d°" % (a, b, p_), NO, "∠A는 두 변 AB, BC의 끼인각이 아니에요."
            return M("△ABC에서 <b>%s</b>가 주어질 때, 삼각형은?" % d, ans, [x for x in (OK, NO, CANT, "항상 정삼각형이 돼요") if x != ans], "%s <b>%s</b>" % (why, ans))
        G_ = [("세 변의 길이", True), ("두 변의 길이와 그 끼인각의 크기", True), ("한 변의 길이와 그 양 끝 각의 크기", True),
              ("두 변의 길이와 끼인각이 아닌 한 각의 크기", False), ("세 각의 크기", False), ("한 변의 길이와 한 각의 크기", False)]
        good = [g for g, ok in G_ if ok]
        bad = [g for g, ok in G_ if not ok]
        if R.random() < 0.5:
            a = R.choice(good)
            return M("삼각형이 하나로 정해지는 조건은?", a, R.sample(bad, 3), "세 변 / 두 변과 끼인각 / 한 변과 양 끝 각이 주어지면 하나로 정해져요. <b>%s</b>" % a)
        a = R.choice(bad)
        return M("삼각형이 하나로 정해지지 <b>않는</b> 경우는?", a, R.sample(good, 3), "세 각만 같으면 크기가 다른 삼각형이 많아요. <b>%s</b>" % a)
    return mk


def tri_fig(names, sides=(), angles=()):
    A, B, C = names
    pts = {A: (1.6, 3.2), B: (0, 0), C: (4.2, 0)}
    return figure(pts, [(A, B), (B, C), (C, A)], label="삼각형 %s%s%s" % (A, B, C), sides=sides)


def g_cong():
    def mk():
        how = R.choice(["cond", "corr", "len"])
        if how == "cond":
            k = R.choice(["SSS", "SAS", "ASA"])
            desc = {"SSS": "AB = DE, BC = EF, CA = FD", "SAS": "AB = DE, BC = EF, ∠B = ∠E", "ASA": "BC = EF, ∠B = ∠E, ∠C = ∠F"}[k]
            return M("△ABC와 △DEF에서 <b>%s</b>일 때, 두 삼각형은 어떤 합동 조건으로 합동일까요?" % desc, "%s 합동" % k, ["%s 합동" % x for x in ("SSS", "SAS", "ASA", "AAA") if x != k],
                     {"SSS": "세 변의 길이가 같아요.", "SAS": "두 변의 길이와 끼인각이 같아요.", "ASA": "한 변의 길이와 양 끝 각이 같아요."}[k] + " <b>%s 합동</b>" % k)
        if how == "corr":
            pairs = [("변 AB", "변 DE"), ("변 BC", "변 EF"), ("변 CA", "변 FD"), ("∠A", "∠D"), ("∠B", "∠E"), ("∠C", "∠F")]
            x, y = R.choice(pairs)
            others = [b for a, b in pairs if b != y and b[0] == y[0]]
            return M("△ABC ≡ △DEF일 때, <b>%s</b>의 대응%s?" % (x, "변은" if x.startswith("변") else "각은"), y, others + ["변 AC" if y.startswith("변") else "∠A"],
                     "합동 기호 ≡ 앞뒤의 꼭짓점 순서대로 대응해요. <b>%s</b>" % y)
        a, b = R.randint(4, 12), R.randint(30, 80)
        x = R.choice(["DE", "EF"])
        v = a
        return N("△ABC ≡ △DEF이고 AB = %d cm, BC = %d cm, ∠B = %d°일 때, %s의 길이는?" % (a if x == "DE" else a + 1, a if x == "EF" else a + 2, b, x),
                 a if x == "DE" else a, [a + 1 if x == "DE" else a + 2, b, a + 3], "%s의 대응변은 %s예요. <b>%d cm</b>" % (x, "AB" if x == "DE" else "BC", a), f=lambda z: "%s cm" % neg(z))
    return mk


# ------------------------------------------------------------------ 다각형
def pg_calc(kinds=("diag", "diag1", "sum", "each", "ext", "inv")):
    def mk():
        n = R.randint(5, 24)
        how = R.choice(kinds)
        if how == "diag":
            v = n * (n - 3) // 2
            return N("<b>%s각형</b>의 대각선의 개수는?" % kn(n), v, [n * (n - 3), n - 3, n * (n - 1) // 2], "n(n − 3)/2 = %d × %d ÷ 2 = <b>%d개</b>" % (n, n - 3, v), f=lambda x: "%s개" % neg(x))
        if how == "diag1":
            return N("<b>%s각형</b>의 한 꼭짓점에서 그을 수 있는 대각선의 개수는?" % kn(n), n - 3, [n - 2, n, n * (n - 3) // 2], "자기 자신과 이웃한 두 꼭짓점을 빼요. %d − 3 = <b>%d개</b>" % (n, n - 3), f=lambda x: "%s개" % neg(x))
        if how == "sum":
            v = 180 * (n - 2)
            return N("<b>%s각형</b>의 내각의 크기의 합은?" % kn(n), v, [180 * n, 180 * (n - 3), 360 * (n - 2)], "180° × (%d − 2) = <b>%s°</b>" % (n, num(v)), f=lambda x: "%s°" % num(x))
        if how == "each":
            n = R.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
            v = Fr(180 * (n - 2), n)
            return N("<b>정%s각형</b>의 한 내각의 크기는?" % kn(n), v, [Fr(360, n), Fr(180 * n, n - 2), 180 - Fr(180, n)], "180° × (%d − 2) ÷ %d = <b>%s°</b>" % (n, n, neg(v)), f=lambda x: "%s°" % neg(x))
        if how == "ext":
            n = R.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
            return N("<b>정%s각형</b>의 한 외각의 크기는?" % kn(n), Fr(360, n), [Fr(180, n), 180 - Fr(360, n), Fr(720, n)], "외각의 합은 360°예요. 360° ÷ %d = <b>%s°</b>" % (n, neg(Fr(360, n))), f=lambda x: "%s°" % neg(x))
        n = R.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
        e = 360 // n
        k = R.choice(["ext", "sum"])
        if k == "ext":
            return N("한 외각의 크기가 <b>%d°</b>인 정다각형은?" % e, n, [n + 1, 180 // e, n - 2], "360° ÷ %d° = %d → <b>정%s각형</b>" % (e, n, kn(n)), f=lambda x: "정%s각형" % kn(x))
        s = 180 * (n - 2)
        return N("내각의 크기의 합이 <b>%s°</b>인 다각형은?" % num(s), n, [n - 2, n + 2, n - 1], "180° × (n − 2) = %s°, n = %d → <b>%s각형</b>" % (num(s), n, kn(n)), f=lambda x: "%s각형" % kn(x))
    return mk


def pg_tri():
    def mk():
        how = R.choice(["ext", "inner", "x"])
        a, b = R.randint(30, 80), R.randint(30, 80)
        if how == "ext":
            return N("삼각형의 두 내각의 크기가 %d°, %d°일 때, 나머지 한 내각의 외각의 크기는?" % (a, b), a + b, [180 - a - b, 360 - a - b, abs(a - b)],
                     "한 외각의 크기는 이웃하지 않는 두 내각의 합과 같아요. %d° + %d° = <b>%d°</b>" % (a, b, a + b), f=deg)
        if how == "inner":
            return N("삼각형의 두 내각의 크기가 %d°, %d°일 때, 나머지 한 내각의 크기는?" % (a, b), 180 - a - b, [a + b, 360 - a - b, 90 - a if a < 90 else 10], "180° − %d° − %d° = <b>%d°</b>" % (a, b, 180 - a - b), f=deg)
        x = R.randint(15, 35)
        k = R.choice([2, 3])
        c = 180 - (k + 1) * x
        if c <= 10:
            return None
        return N("삼각형의 세 내각의 크기가 x°, %dx°, %d°일 때, x의 값은?" % (k, c), x, [Fr(180 + c, k + 1), Fr(180 - c, k), x + 5], "x + %dx + %d = 180, %dx = %d, x = <b>%d</b>" % (k, c, k + 1, 180 - c, x))
    return mk


# ------------------------------------------------------------------ 원과 부채꼴
def sec_calc(kinds=("arc", "area", "peri", "area_l")):
    def mk():
        r = R.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
        th = R.choice([30, 36, 40, 45, 60, 72, 90, 120, 135, 150, 180, 240, 270])
        L = Fr(2 * r * th, 360)
        A = Fr(r * r * th, 360)
        how = R.choice(kinds)
        if how == "arc":
            return M("반지름이 %d cm, 중심각이 %d°인 부채꼴의 <b>호의 길이</b>는?" % (r, th), pi(L, "cm"), [pi(A, "cm"), pi(L * 2, "cm"), pi(Fr(r * th, 360), "cm")],
                     "2π × %d × %d/360 = <b>%s</b>" % (r, th, pi(L, "cm")))
        if how == "area":
            return M("반지름이 %d cm, 중심각이 %d°인 부채꼴의 <b>넓이</b>는?" % (r, th), pi(A, "cm²"), [pi(L, "cm²"), pi(A * 2, "cm²"), pi(Fr(4 * r * r * th, 360), "cm²")],
                     "π × %d² × %d/360 = <b>%s</b>" % (r, th, pi(A, "cm²")))
        if how == "peri":
            ok = "(%s + %d) cm" % (pi(L), 2 * r)
            return M("반지름이 %d cm, 중심각이 %d°인 부채꼴의 <b>둘레의 길이</b>는?" % (r, th), ok, ["%s cm" % pi(L), "(%s + %d) cm" % (pi(L), r), "(%s + %d) cm" % (pi(A), 2 * r)],
                     "호의 길이 %s에 반지름 2개를 더해요. <b>%s</b>" % (pi(L, "cm"), ok))
        return M("반지름이 %d cm이고 호의 길이가 %s인 부채꼴의 넓이는?" % (r, pi(L, "cm")), pi(L * r / 2, "cm²"), [pi(L * r, "cm²"), pi(L * r * r / 2, "cm²"), pi(L / 2, "cm²")],
                 "넓이 = ½ × 반지름 × 호의 길이 = ½ × %d × %s = <b>%s</b>" % (r, pi(L), pi(L * r / 2, "cm²")))
    return mk


def sec_ratio():
    def mk():
        how = R.choice(["arc", "angle", "area", "fact"])
        a = R.choice([20, 30, 40, 45, 60])
        k = R.choice([2, 3, 4])
        L = R.randint(3, 9)
        if how == "arc":
            return N("한 원에서 중심각이 %d°인 부채꼴의 호의 길이가 %d cm예요. 중심각이 %d°인 부채꼴의 호의 길이는?" % (a, L, a * k), L * k, [L * k * k, L + k, Fr(L, k)],
                     "호의 길이는 중심각의 크기에 정비례해요. %d × %d = <b>%d cm</b>" % (L, k, L * k), f=lambda x: "%s cm" % neg(x))
        if how == "angle":
            return N("한 원에서 호의 길이가 %d cm인 부채꼴의 중심각이 %d°예요. 호의 길이가 %d cm인 부채꼴의 중심각은?" % (L, a, L * k), a * k, [a * k * k, a + k, Fr(a, k)],
                     "중심각은 호의 길이에 정비례해요. %d° × %d = <b>%d°</b>" % (a, k, a * k), f=deg)
        if how == "area":
            S = R.randint(4, 12)
            return N("한 원에서 중심각이 %d°인 부채꼴의 넓이가 %d cm²예요. 중심각이 %d°인 부채꼴의 넓이는?" % (a, S, a * k), S * k, [S * k * k, S + k, Fr(S, k)],
                     "넓이도 중심각에 정비례해요. <b>%d cm²</b>" % (S * k), f=lambda x: "%s cm²" % neg(x))
        F = [("한 원에서 중심각의 크기가 2배가 되면 현의 길이는?", "2배보다 짧아요", ["정확히 2배가 돼요", "변하지 않아요", "4배가 돼요"], "현의 길이는 중심각에 정비례하지 않아요."),
             ("한 원에서 크기가 같은 중심각에 대한 호의 길이는?", "서로 같아요", ["항상 달라요", "중심각에 반비례해요", "현의 길이의 2배예요"], "중심각이 같으면 호의 길이, 현의 길이, 넓이가 모두 같아요.")]
        q, a_, b, e = R.choice(F)
        return M(q, a_, b, e)
    return mk


def circ_calc():
    def mk():
        r = R.randint(2, 12)
        how = R.choice(["c", "a", "d"])
        if how == "c":
            return M("반지름이 %d cm인 원의 둘레의 길이는?" % r, pi(2 * r, "cm"), [pi(r * r, "cm"), pi(r, "cm"), pi(4 * r, "cm")], "2πr = <b>%s</b>" % pi(2 * r, "cm"))
        if how == "a":
            return M("반지름이 %d cm인 원의 넓이는?" % r, pi(r * r, "cm²"), [pi(2 * r, "cm²"), pi(4 * r * r, "cm²"), pi(r * r * 2, "cm²")], "πr² = <b>%s</b>" % pi(r * r, "cm²"))
        return M("지름이 %d cm인 원의 넓이는?" % (2 * r), pi(r * r, "cm²"), [pi(4 * r * r, "cm²"), pi(2 * r, "cm²"), pi(r * r * 2, "cm²")], "반지름은 %d cm. π × %d² = <b>%s</b>" % (r, r, pi(r * r, "cm²")))
    return mk


# ------------------------------------------------------------------ 다면체와 회전체
def so_poly():
    def mk():
        n = R.randint(3, 10)
        k = R.choice(["기둥", "뿔", "뿔대"])
        F, E, V = {"기둥": (n + 2, 3 * n, 2 * n), "뿔": (n + 1, 2 * n, n + 1), "뿔대": (n + 2, 3 * n, 2 * n)}[k]
        what = R.choice(["면", "모서리", "꼭짓점"])
        v = {"면": F, "모서리": E, "꼭짓점": V}[what]
        nm = "%s각%s" % (kn(n), k)
        return N("<b>%s</b>의 %s의 개수는?" % (nm, what), v, [F, E, V, v + 1, v - 1], "%s: 면 %d개, 모서리 %d개, 꼭짓점 %d개. <b>%d개</b>" % (nm, F, E, V, v), f=lambda x: "%s개" % neg(x))
    return mk


def so_which(kinds=("faces", "regular", "name")):
    def mk():
        how = R.choice(kinds)
        if how == "faces":
            n = R.randint(5, 20)
            k = R.choice(["각기둥", "각뿔"])
            m = n - 2 if k == "각기둥" else n - 1
            return N("면의 개수가 <b>%d개</b>인 %s은?" % (n, k), m, [n, m + 1, m - 1, m + 2, m - 2], "n%s의 면은 %s개. n = %d → <b>%s%s</b>" % (k, "n + 2" if k == "각기둥" else "n + 1", m, kn(m), k), f=lambda x: "%s%s" % (kn(x), k))
        RG = [("정사면체", "정삼각형", 3, 4), ("정육면체", "정사각형", 3, 8), ("정팔면체", "정삼각형", 4, 6), ("정십이면체", "정오각형", 3, 20), ("정이십면체", "정삼각형", 5, 12)]
        if how == "regular":
            nm, face, m, v = R.choice(RG)
            ask = R.choice(["face", "meet", "vert"])
            if ask == "face":
                return M("<b>%s</b>의 면의 모양은?" % nm, face, [x for x in ("정삼각형", "정사각형", "정오각형", "정육각형") if x != face], "<b>%s</b>" % face)
            if ask == "meet":
                return N("<b>%s</b>에서 한 꼭짓점에 모인 면의 개수는?" % nm, m, [x for x in (3, 4, 5, 6) if x != m], "<b>%d개</b>" % m, f=lambda x: "%s개" % neg(x))
            return N("<b>%s</b>의 꼭짓점의 개수는?" % nm, v, [x for x in (4, 6, 8, 12, 20) if x != v][:3], "<b>%d개</b>" % v, f=lambda x: "%s개" % neg(x))
        F = [("정다면체의 종류는 모두 몇 가지일까요?", "5가지", ["4가지", "6가지", "무수히 많아요"], "정사면체, 정육면체, 정팔면체, 정십이면체, 정이십면체 <b>5가지</b>예요."),
             ("면의 모양이 정육각형인 정다면체가 없는 이유는?", "한 꼭짓점에 모인 각의 합이 360°가 되어 입체가 되지 않아요", ["정육각형은 작도할 수 없어요", "정육각형은 대각선이 없어요", "변이 너무 많아요"],
              "120° × 3 = 360°라서 평평해져요."),
             ("다면체가 <b>아닌</b> 것은?", "원기둥", ["삼각기둥", "사각뿔", "정팔면체"], "원기둥은 곡면이 있어 다면체가 아니에요(회전체예요)."),
             ("각뿔대의 두 밑면에 대한 설명으로 옳은 것은?", "평행하고 모양은 닮았지만 크기가 달라요", ["합동이에요", "수직이에요", "옆면과 같은 모양이에요"], "각뿔을 밑면에 평행하게 자른 것이에요."),
             ("각기둥의 옆면의 모양은?", "직사각형", ["삼각형", "사다리꼴", "원"], "각기둥의 옆면은 모두 <b>직사각형</b>이에요."),
             ("각뿔의 옆면의 모양은?", "삼각형", ["직사각형", "사다리꼴", "오각형"], "각뿔의 옆면은 모두 <b>삼각형</b>이에요."),
             ("각뿔대의 옆면의 모양은?", "사다리꼴", ["직사각형", "삼각형", "평행사변형"], "각뿔대의 옆면은 모두 <b>사다리꼴</b>이에요.")]
        return M(*R.choice(F))
    return mk


ROT = [("직사각형", "한 변을 회전축으로", "원기둥"), ("직각삼각형", "직각을 낀 한 변을 회전축으로", "원뿔"), ("반원", "지름을 회전축으로", "구"),
       ("사다리꼴(두 밑변에 수직인 변을 축으로)", "회전축에 수직인 변이 두 개인 쪽을 축으로", "원뿔대")]


def so_rot():
    def mk():
        how = R.choice(["make", "cut", "which"])
        if how == "make":
            a, h, s_ = R.choice(ROT)
            return M("<b>%s</b>을 %s 한 바퀴 돌리면 어떤 회전체가 될까요?" % (a, h), s_, [x for x in ("원기둥", "원뿔", "구", "원뿔대") if x != s_], "<b>%s</b>" % s_)
        if how == "cut":
            s_ = R.choice(["원기둥", "원뿔", "구", "원뿔대"])
            ax = {"원기둥": "직사각형", "원뿔": "이등변삼각형", "구": "원", "원뿔대": "사다리꼴"}[s_]
            if R.random() < 0.5:
                return M("<b>%s</b>을 회전축을 포함하는 평면으로 자를 때 생기는 단면의 모양은?" % s_, ax, [x for x in ("직사각형", "이등변삼각형", "원", "사다리꼴") if x != ax],
                         "회전축을 포함하는 평면으로 자르면 회전축에 대해 선대칭인 도형이 생겨요. <b>%s</b>" % ax)
            return M("<b>%s</b>을 회전축에 수직인 평면으로 자를 때 생기는 단면의 모양은?" % s_, "원", ["직사각형", "이등변삼각형", "사다리꼴"], "회전축에 수직인 평면으로 자르면 항상 <b>원</b>이 생겨요.")
        if R.random() < 0.5:
            bad = R.choice(["삼각뿔", "정육면체", "오각기둥", "사각뿔대", "정팔면체", "육각기둥", "삼각기둥"])
            good = R.sample(["원기둥", "원뿔", "구", "원뿔대", "반구"], 3)
            return M("다음 중 회전체가 <b>아닌</b> 것은? (%s)" % bad, bad, good, "회전체는 평면도형을 한 직선을 축으로 회전시켜 만든 입체예요. <b>%s</b>는 다면체예요." % bad)
        r, h = R.randint(2, 9), R.randint(3, 12)
        k = R.choice(["원기둥", "원뿔"])
        if k == "원기둥":
            return N("가로 %d cm, 세로 %d cm인 직사각형을 세로를 회전축으로 한 바퀴 돌려 만든 원기둥을 회전축을 포함하는 평면으로 자른 단면의 넓이는?" % (r, h), 2 * r * h, [r * h, 4 * r * h, 2 * r + 2 * h],
                     "단면은 가로 %d cm, 세로 %d cm인 직사각형이에요. <b>%d cm²</b>" % (2 * r, h, 2 * r * h), f=lambda x: "%s cm²" % neg(x))
        return N("밑변 %d cm, 높이 %d cm인 직각삼각형을 높이를 회전축으로 한 바퀴 돌려 만든 원뿔을 회전축을 포함하는 평면으로 자른 단면의 넓이는?" % (r, h), r * h, [Fr(r * h, 2), 2 * r * h, r + h],
                 "단면은 밑변 %d cm, 높이 %d cm인 이등변삼각형이에요. ½ × %d × %d = <b>%d cm²</b>" % (2 * r, h, 2 * r, h, r * h), f=lambda x: "%s cm²" % neg(x))
    return mk


# ------------------------------------------------------------------ 겉넓이와 부피
def vol_calc(kinds=("prism", "cyl_v", "cyl_s", "pyr", "cone_v", "sph_v", "sph_s", "cone_s")):
    def mk():
        how = R.choice(kinds)
        if how == "prism":
            a, b, h = R.randint(2, 9), R.randint(2, 9), R.randint(3, 12)
            k = R.choice(["v", "s"])
            if k == "v":
                v = Fr(a * b, 2) * h
                return N("밑면이 밑변 %d cm, 높이 %d cm인 삼각형이고 높이가 %d cm인 삼각기둥의 부피는?" % (a, b, h), v, [a * b * h, v * Fr(1, 3), a + b + h], "(밑넓이) × (높이) = %s × %d = <b>%s cm³</b>" % (neg(Fr(a * b, 2)), h, neg(v)),
                         f=lambda x: "%s cm³" % neg(x))
            s = 2 * (a * b + b * h + a * h)
            return N("가로 %d cm, 세로 %d cm, 높이 %d cm인 직육면체의 겉넓이는?" % (a, b, h), s, [a * b + b * h + a * h, a * b * h, 2 * a * b + 4 * h],
                     "2 × (%d + %d + %d) = <b>%d cm²</b>" % (a * b, b * h, a * h, s), f=lambda x: "%s cm²" % neg(x))
        r, h = R.randint(2, 8), R.randint(3, 12)
        if how in ("sph_v", "sph_s"):
            r = R.randint(1, 12)
        if how == "cyl_v":
            return M("밑면의 반지름이 %d cm, 높이가 %d cm인 원기둥의 부피는?" % (r, h), pi(r * r * h, "cm³"), [pi(2 * r * h, "cm³"), pi(Fr(r * r * h, 3), "cm³"), pi(4 * r * r * h, "cm³")],
                     "π × %d² × %d = <b>%s</b>" % (r, h, pi(r * r * h, "cm³")))
        if how == "cyl_s":
            s = 2 * r * r + 2 * r * h
            return M("밑면의 반지름이 %d cm, 높이가 %d cm인 원기둥의 겉넓이는?" % (r, h), pi(s, "cm²"), [pi(r * r + 2 * r * h, "cm²"), pi(2 * r * h, "cm²"), pi(r * r * h, "cm²")],
                     "밑넓이 2개 + 옆넓이: 2 × π × %d² + 2π × %d × %d = <b>%s</b>" % (r, r, h, pi(s, "cm²")))
        if how == "pyr":
            a, h = R.randint(2, 9), R.randint(3, 12)
            v = Fr(a * a * h, 3)
            return N("밑면이 한 변 %d cm인 정사각형이고 높이가 %d cm인 사각뿔의 부피는?" % (a, h), v, [a * a * h, Fr(a * a * h, 2), 4 * a * h], "⅓ × %d × %d = <b>%s cm³</b>" % (a * a, h, neg(v)),
                     f=lambda x: "%s cm³" % neg(x))
        if how == "cone_v":
            return M("밑면의 반지름이 %d cm, 높이가 %d cm인 원뿔의 부피는?" % (r, h), pi(Fr(r * r * h, 3), "cm³"), [pi(r * r * h, "cm³"), pi(Fr(2 * r * h, 3), "cm³"), pi(Fr(r * r * h, 2), "cm³")],
                     "⅓ × π × %d² × %d = <b>%s</b>" % (r, h, pi(Fr(r * r * h, 3), "cm³")))
        if how == "cone_s":
            l = r + R.randint(2, 8)
            s = r * r + r * l
            return M("밑면의 반지름이 %d cm, 모선의 길이가 %d cm인 원뿔의 겉넓이는?" % (r, l), pi(s, "cm²"), [pi(r * l, "cm²"), pi(r * r + 2 * r * l, "cm²"), pi(r * r * l, "cm²")],
                     "밑넓이 + 옆넓이 = π × %d² + π × %d × %d = <b>%s</b>" % (r, r, l, pi(s, "cm²")))
        if how == "sph_v":
            return M("반지름이 %d cm인 구의 부피는?" % r, pi(Fr(4 * r ** 3, 3), "cm³"), [pi(4 * r * r, "cm³"), pi(r ** 3, "cm³"), pi(Fr(4 * r * r, 3), "cm³")],
                     "⁴⁄₃ × π × %d³ = <b>%s</b>" % (r, pi(Fr(4 * r ** 3, 3), "cm³")))
        return M("반지름이 %d cm인 구의 겉넓이는?" % r, pi(4 * r * r, "cm²"), [pi(2 * r * r, "cm²"), pi(Fr(4 * r ** 3, 3), "cm²"), pi(r * r, "cm²")], "4π × %d² = <b>%s</b>" % (r, pi(4 * r * r, "cm²")))
    return mk


def vol_ratio():
    def mk():
        how = R.choice(["cone_cyl", "sph_cyl", "half"])
        r = R.randint(2, 6)
        if how == "cone_cyl":
            V = R.randint(4, 20) * 3
            return N("밑면과 높이가 각각 같은 원기둥의 부피가 %d cm³일 때, 원뿔의 부피는?" % V, V // 3, [V * 3, V // 2, V], "원뿔의 부피는 원기둥의 부피의 ⅓이에요. <b>%d cm³</b>" % (V // 3), f=lambda x: "%s cm³" % neg(x))
        if how == "sph_cyl":
            return M("원기둥 안에 꼭 맞는 구, 원뿔이 있어요. 원뿔 : 구 : 원기둥의 부피의 비는?", "1 : 2 : 3", ["1 : 3 : 2", "1 : 2 : 4", "1 : 1 : 3"], "<b>1 : 2 : 3</b>이에요.")
        return M("반지름이 %d cm인 반구의 부피는?" % r, pi(Fr(2 * r ** 3, 3), "cm³"), [pi(Fr(4 * r ** 3, 3), "cm³"), pi(2 * r * r, "cm³"), pi(Fr(r ** 3, 3), "cm³")],
                 "구의 부피의 반: ½ × ⁴⁄₃π × %d³ = <b>%s</b>" % (r, pi(Fr(2 * r ** 3, 3), "cm³")))
    return mk


# ------------------------------------------------------------------ 대푯값
def data_list(n, lo, hi):
    return [R.randint(lo, hi) for _ in range(n)]


def st_rep(kinds=("med_odd", "med_even", "mode", "mean", "unk")):
    def mk():
        how = R.choice(kinds)
        if how in ("med_odd", "med_even"):
            n = R.choice([5, 7, 9]) if how == "med_odd" else R.choice([6, 8, 10])
            xs = data_list(n, 10, 40)
            s = sorted(xs)
            med = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
            w = [Fr(xs[n // 2]), Fr(sum(xs), n), Fr(s[n // 2]) if n % 2 == 0 else Fr(s[n // 2 - 1]), Fr(s[n // 2 - 1]) if n % 2 == 0 else Fr(s[n // 2 + 1])]
            return N("다음 자료의 <b>중앙값</b>은?<br>%s" % ", ".join(map(str, xs)), med, w,
                     "작은 값부터 늘어놓으면 %s. %s <b>%s</b>" % (", ".join(map(str, s)), "가운데 값" if n % 2 else "가운데 두 값의 평균", neg(med) if med.denominator == 1 else dec(med)), f=lambda v: neg(v) if Fr(v).denominator == 1 else dec(v))
        if how == "mode":
            base = R.sample(range(1, 10), 4)
            m = R.choice(base)
            xs = base + [m, m] + R.sample([b for b in base if b != m], 1)
            R.shuffle(xs)
            return N("다음 자료의 <b>최빈값</b>은?<br>%s" % ", ".join(map(str, xs)), m, [b for b in base if b != m] + [Fr(sum(xs), len(xs))],
                     "가장 많이 나타난 값이에요. <b>%d</b>" % m, f=lambda v: neg(v) if Fr(v).denominator == 1 else str(round(float(v), 1)))
        if how == "mean":
            n = R.randint(4, 6)
            xs = data_list(n - 1, 50, 95)
            tot = sum(xs)
            last = (-tot) % n + n * R.randint(5, 9)
            if last > 100:
                return None
            xs.append(last)
            R.shuffle(xs)
            m = Fr(sum(xs), n)
            return N("다음 자료의 <b>평균</b>은?<br>%s" % ", ".join(map(str, xs)), m, [sorted(xs)[n // 2], m + 1, Fr(sum(xs), n - 1) if Fr(sum(xs), n - 1).denominator == 1 else m - 2],
                     "(%s) ÷ %d = <b>%s</b>" % (" + ".join(map(str, xs)), n, neg(m)))
        n = R.randint(4, 5)
        m = R.randint(60, 85)
        xs = data_list(n - 1, 55, 95)
        x = m * n - sum(xs)
        if not 40 <= x <= 100:
            return None
        return N("%d명의 점수가 %s, x점이고 평균이 %d점일 때, x의 값은?" % (n, ", ".join(map(str, xs)), m), x, [x + n, x - 5, sum(xs) // (n - 1)],
                 "합계 = %d × %d = %d → x = %d − %d = <b>%d</b>" % (m, n, m * n, m * n, sum(xs), x))
    return mk


def st_choose():
    F = [("자료에 극단적인 값(매우 크거나 작은 값)이 있을 때 대푯값으로 적절한 것은?", "중앙값", ["평균", "가장 큰 값", "자료의 개수"], "극단적인 값의 영향을 덜 받는 <b>중앙값</b>이 적절해요."),
         ("가게에서 가장 많이 팔린 신발 치수를 알아볼 때 적절한 대푯값은?", "최빈값", ["평균", "중앙값", "가장 작은 값"], "가장 많이 나타난 값인 <b>최빈값</b>이 적절해요."),
         ("좋아하는 운동 종목처럼 수가 아닌 자료의 대푯값으로 적절한 것은?", "최빈값", ["평균", "중앙값", "총합"], "수가 아닌 자료는 <b>최빈값</b>만 구할 수 있어요."),
         ("자료가 고르게 퍼져 있고 극단적인 값이 없을 때 많이 쓰는 대푯값은?", "평균", ["최빈값", "가장 큰 값", "가장 작은 값"], "자료 전체를 반영하는 <b>평균</b>을 많이 써요."),
         ("자료의 값 중 하나가 매우 크게 바뀌었을 때 반드시 같이 바뀌는 것은?", "평균", ["중앙값", "최빈값", "자료의 개수"], "평균은 모든 값의 합으로 구하므로 <b>바뀌어요</b>."),
         ("최빈값에 대해 옳은 것은?", "2개 이상일 수도 있어요", ["항상 1개예요", "항상 평균보다 커요", "수가 아닌 자료에서는 구할 수 없어요"], "가장 많이 나타난 값이 여럿이면 <b>모두 최빈값</b>이에요.")]
    pool = F[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        return M(*pool.pop())
    return mk


# ------------------------------------------------------------------ 줄기와 잎, 도수분포표, 히스토그램
def stem_leaf(xs):
    st = {}
    for x in sorted(xs):
        st.setdefault(x // 10, []).append(x % 10)
    rows = "".join("<tr><td>%d</td><td style='text-align:left'>%s</td></tr>" % (k, " ".join(map(str, v))) for k, v in sorted(st.items()))
    return "<div class='sn-tw'><table class='sn-table'><tr><th>줄기</th><th>잎</th></tr>%s</table></div><p>(1 | 3은 13)</p>" % rows


def f_stem():
    def mk():
        n = R.randint(12, 16)
        xs = sorted(R.sample(range(10, 50), n))
        tb = stem_leaf(xs)
        how = R.choice(["count", "max", "stem", "rank"])
        if how == "count":
            k = R.choice(sorted({x // 10 for x in xs}))
            c = sum(1 for x in xs if x // 10 == k)
            return N("줄기와 잎 그림에서 줄기가 %d인 잎의 개수는?%s" % (k, tb), c, [c + 1, c - 1, k, n], "줄기 %d의 잎을 세면 <b>%d개</b>" % (k, c), f=lambda v: "%s개" % neg(v))
        if how == "max":
            return N("줄기와 잎 그림에서 가장 큰 값과 가장 작은 값의 차는?%s" % tb, xs[-1] - xs[0], [xs[-1], xs[-1] - xs[0] + 1, xs[-1] // 10 - xs[0] // 10], "%d − %d = <b>%d</b>" % (xs[-1], xs[0], xs[-1] - xs[0]))
        if how == "stem":
            t = R.randint(20, 40)
            c = sum(1 for x in xs if x >= t)
            return N("줄기와 잎 그림에서 %d 이상인 자료는 몇 개일까요?%s" % (t, tb), c, [c + 1, c - 1, n - c], "<b>%d개</b>" % c, f=lambda v: "%s개" % neg(v))
        k = R.randint(2, 4)
        return N("줄기와 잎 그림에서 %d번째로 큰 값은?%s" % (k, tb), xs[-k], [xs[-k + 1] if k > 1 else xs[-1] + 1, xs[-k - 1], xs[k - 1]], "큰 값부터 세면 <b>%d</b>" % xs[-k])
    return mk


def freq_table():
    w = R.choice([5, 10])
    start = R.choice([40, 50]) if w == 10 else R.choice([10, 15, 20])
    k = 5
    fs = [R.randint(1, 9) for _ in range(k)]
    return w, start, fs


def ftab(w, start, fs, hide=None, unit_="점"):
    rows = "".join("<tr><td>%d 이상 ~ %d 미만</td><td>%s</td></tr>" % (start + i * w, start + (i + 1) * w, "x" if i == hide else f) for i, f in enumerate(fs))
    return "<div class='sn-tw'><table class='sn-table'><tr><th>점수(%s)</th><th>학생 수(명)</th></tr>%s<tr><th>합계</th><th>%d</th></tr></table></div>" % (unit_, rows, sum(fs))


def hist_svg(w, start, fs, poly=False):
    k = len(fs)
    m = max(fs)
    u, hgt = 50, 24
    W, H = 60 + u * (k + 2), 40 + hgt * (m + 1) + 30
    X = lambda i: 40 + u * (i + 1)
    Y = lambda v: H - 34 - v * hgt
    s = [line(40, Y(0), W - 10, Y(0), INK, 2), line(40, Y(0), 40, 12, INK, 2)]
    for v in range(1, m + 1):
        s.append(line(40, Y(v), W - 10, Y(v), "#dddddd", 1) + text(32, Y(v) + 5, str(v), 13, anchor="end", weight=400))
    for i, f in enumerate(fs):
        if not poly:
            s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='#bfe0c6' stroke='%s' stroke-width='1.5'/>" % (X(i), Y(f), u, f * hgt, GREEN))
    for i in range(k + 1):
        s.append(text(X(i), Y(0) + 18, str(start + i * w), 13, weight=400))
    if poly:
        pts = [(X(-1) + u / 2, Y(0))] + [(X(i) + u / 2, Y(f)) for i, f in enumerate(fs)] + [(X(k) + u / 2, Y(0))]
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in pts), BLUE))
        for p in pts:
            s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (p[0], p[1], BLUE))
    s.append(text(W - 14, Y(0) + 30, "(점)", 12, anchor="end", weight=400) + text(46, 12, "(명)", 12, anchor="start", weight=400))
    return svgf(W, H, "".join(s), "도수분포다각형" if poly else "히스토그램")


def f_table():
    def mk():
        w, start, fs = freq_table()
        how = R.choice(["hide", "class", "most", "below"])
        if how == "hide":
            i = R.randrange(5)
            return N("도수분포표에서 x의 값은?%s" % ftab(w, start, fs, i), fs[i], [fs[i] + 1, sum(fs) - fs[i], fs[i] - 1 if fs[i] > 1 else fs[i] + 2],
                     "합계에서 나머지 도수를 빼요. <b>%d</b>" % fs[i])
        tb = ftab(w, start, fs)
        if how == "class":
            return N("도수분포표에서 계급의 크기는?%s" % tb, w, [w * 5, sum(fs), start], "계급의 양 끝 값의 차예요. <b>%d점</b>" % w, f=lambda v: "%s점" % neg(v))
        if how == "most":
            m = max(fs)
            if fs.count(m) > 1:
                return None
            i = fs.index(m)
            ok = "%d점 이상 %d점 미만" % (start + i * w, start + (i + 1) * w)
            return M("도수가 가장 큰 계급은?%s" % tb, ok, ["%d점 이상 %d점 미만" % (start + j * w, start + (j + 1) * w) for j in range(5) if j != i], "도수 %d명. <b>%s</b>" % (m, ok))
        t = R.randint(1, 4)
        c = sum(fs[:t])
        return N("%d점 미만인 학생은 몇 명일까요?%s" % (start + t * w, tb), c, [c + fs[t], c - fs[t - 1], sum(fs) - c], "<b>%d명</b>" % c, f=lambda v: "%s명" % neg(v))
    return mk


def f_hist():
    def mk():
        w, start, fs = freq_table()
        poly = R.random() < 0.4
        g = hist_svg(w, start, fs, poly)
        how = R.choice(["total", "area", "class", "pct"])
        nm = "도수분포다각형" if poly else "히스토그램"
        if how == "total":
            return N("%s으로 나타낸 학생 수는 모두 몇 명일까요?%s" % (nm, g), sum(fs), [max(fs), sum(fs) + 1, len(fs)], "도수를 모두 더해요. <b>%d명</b>" % sum(fs), f=lambda v: "%s명" % neg(v))
        if how == "area":
            if poly:
                return N("도수분포다각형과 가로축으로 둘러싸인 부분의 넓이는? (가로 단위 1점, 세로 단위 1명)%s" % g, w * sum(fs), [sum(fs), w * max(fs), 2 * w * sum(fs)],
                         "히스토그램의 직사각형 넓이의 합과 같아요. %d × %d = <b>%d</b>" % (w, sum(fs), w * sum(fs)))
            return N("히스토그램의 직사각형의 넓이의 합은? (가로 단위 1점, 세로 단위 1명)%s" % g, w * sum(fs), [sum(fs), w * max(fs), 5 * sum(fs) if w == 10 else 10 * sum(fs)],
                     "(계급의 크기) × (도수의 총합) = %d × %d = <b>%d</b>" % (w, sum(fs), w * sum(fs)))
        if how == "class":
            i = R.randrange(5)
            return N("%s에서 %d점 이상 %d점 미만인 계급의 도수는?%s" % (nm, start + i * w, start + (i + 1) * w, g), fs[i], [fs[i] + 1, fs[i] - 1 if fs[i] > 1 else fs[i] + 2, sum(fs)],
                     "<b>%d명</b>" % fs[i], f=lambda v: "%s명" % neg(v))
        t = R.randint(3, 4)
        c = sum(fs[t:])
        tot = sum(fs)
        p = Fr(c * 100, tot)
        if p.denominator != 1:
            return None
        return N("%s에서 %d점 이상인 학생은 전체의 몇 %%일까요?%s" % (nm, start + t * w, g), p, [Fr(c * 100, tot) + 10, Fr((tot - c) * 100, tot), c],
                 "%d ÷ %d × 100 = <b>%s%%</b>" % (c, tot, neg(p)), f=lambda v: "%s%%" % neg(v))
    return mk


# ------------------------------------------------------------------ 상대도수
def r_calc(kinds=("rel", "freq", "total", "pct")):
    def mk():
        how = R.choice(kinds)
        tot = R.choice([20, 25, 40, 50])
        f = R.randint(1, tot // 2)
        r = Fr(f, tot)
        if how == "rel":
            return M("전체 도수가 %d인 자료에서 어떤 계급의 도수가 %d일 때, 이 계급의 상대도수는?" % (tot, f), dec(r), [dec(Fr(tot, f)) if Fr(tot, f).denominator in (1, 2, 4, 5, 10, 20, 25, 50) else str(f), dec(Fr(f, 100)), dec(r * 10)],
                     "(상대도수) = (도수) ÷ (전체 도수) = %d ÷ %d = <b>%s</b>" % (f, tot, dec(r)))
        if how == "freq":
            return N("전체 도수가 %d인 자료에서 어떤 계급의 상대도수가 %s일 때, 이 계급의 도수는?" % (tot, dec(r)), f, [f + 1, tot - f, Fr(tot, 1) * 10 * r / 10 + 2], "%d × %s = <b>%d</b>" % (tot, dec(r), f))
        if how == "total":
            return N("어떤 계급의 도수가 %d이고 상대도수가 %s일 때, 전체 도수는?" % (f, dec(r)), tot, [f * 10, tot + f, tot * 2], "%d ÷ %s = <b>%d</b>" % (f, dec(r), tot))
        return N("상대도수가 %s인 계급은 전체의 몇 %%일까요?" % dec(r), r * 100, [r * 10, r * 1000 if r * 1000 <= 100 else r * 100 + 10, 100 - r * 100], "%s × 100 = <b>%s%%</b>" % (dec(r), neg(r * 100)),
                 f=lambda v: "%s%%" % neg(v))
    return mk


def r_table():
    def mk():
        tot = R.choice([20, 25, 40, 50])
        fs = []
        rest = tot
        for i in range(4):
            v = R.randint(1, max(1, rest - (4 - i)))
            fs.append(v)
            rest -= v
        fs.append(rest)
        if rest <= 0:
            return None
        rows = "".join("<tr><td>%d 이상 ~ %d 미만</td><td>%s</td><td>%s</td></tr>" % (140 + 5 * i, 145 + 5 * i, f, dec(Fr(f, tot))) for i, f in enumerate(fs))
        i = R.randrange(5)
        rows_h = "".join("<tr><td>%d 이상 ~ %d 미만</td><td>%s</td><td>%s</td></tr>" % (140 + 5 * j, 145 + 5 * j, f, "A" if j == i else dec(Fr(f, tot))) for j, f in enumerate(fs))
        tb = "<div class='sn-tw'><table class='sn-table'><tr><th>키(cm)</th><th>도수(명)</th><th>상대도수</th></tr>%s<tr><th>합계</th><th>%d</th><th>1</th></tr></table></div>" % (rows_h, tot)
        r = Fr(fs[i], tot)
        if R.random() < 0.5:
            return M("상대도수의 분포표에서 A의 값은?%s" % tb, dec(r), [dec(Fr(fs[i], 100)), str(fs[i]), dec(1 - r)], "%d ÷ %d = <b>%s</b>" % (fs[i], tot, dec(r)))
        return M("상대도수의 분포표에 대해 옳은 것은?%s" % tb.replace(">A<", ">%s<" % dec(r)), "상대도수의 합은 항상 1이에요", ["상대도수의 합은 전체 도수와 같아요", "상대도수는 1보다 클 수 있어요", "도수가 클수록 상대도수는 작아요"],
                 "상대도수의 합은 <b>항상 1</b>이고, 도수에 정비례해요.")
    return mk


def r_compare():
    def mk():
        t1, t2 = R.choice([(20, 25), (25, 40), (40, 50), (20, 50)])
        f1 = R.randint(2, t1 // 2)
        f2 = R.randint(2, t2 // 2)
        r1, r2 = Fr(f1, t1), Fr(f2, t2)
        if r1 == r2:
            return None
        a, b = NM.next() + "네 반", "옆 반"
        ok = "A반" if r1 > r2 else "B반"
        return M("A반 %d명 중 %d명, B반 %d명 중 %d명이 안경을 써요. 안경을 쓴 학생의 <b>비율</b>이 더 높은 반은?" % (t1, f1, t2, f2), ok, ["B반" if ok == "A반" else "A반", "두 반이 같아요", "학생 수가 많은 반"],
                 "상대도수로 비교해요. A반 %s, B반 %s → <b>%s</b>" % (dec(r1, 3), dec(r2, 3), ok))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "basic":
        return unit(G, "points-lines-planes-and-angles", 10, "[9수03-01] [9수03-02]",
                    "점, 선, 면, 각을 이해하고, 실생활 상황과 연결하여 점, 직선, 평면의 위치 관계를 설명할 수 있다. 평행선에서 동위각과 엇각의 성질을 이해하고 설명할 수 있다.",
                    "기본 도형: 맞꼭지각, 위치 관계, 평행선의 성질", "기본 도형",
                    "중학교 1학년 수학 기본 도형 문제: 교점과 교선, 직선·반직선·선분, 맞꼭지각, 직육면체의 위치 관계와 꼬인 위치, 평행선의 동위각과 엇각까지 100문제와 정답·해설.",
                    "맞꼭지각은 같고, 평행선의 동위각·엇각도 같아요", "두 직선이 만나서 생긴 이웃한 두 각의 합은 180°예요.",
                    ["선과 선 또는 선과 면이 만나는 점을 <b>교점</b>, 면과 면이 만나서 생기는 선을 <b>교선</b>이라고 해요.",
                     "두 직선이 만날 때 서로 마주 보는 각을 <b>맞꼭지각</b>이라 하고, 맞꼭지각의 크기는 같아요.",
                     "공간에서 만나지도 않고 평행하지도 않은 두 직선은 <b>꼬인 위치</b>에 있다고 해요.",
                     "두 직선이 평행하면 <b>동위각</b>(같은 위치의 각)과 <b>엇각</b>(엇갈린 위치의 각)의 크기가 각각 같아요."],
                    [("맞꼭지각 65°의 이웃한 각", ["평각 180°"], "115°"),
                     ("l ∥ m, 동위각이 70°", ["동위각은 같아요."], "70°")],
                    [("맞꼭지각을 서로 더해 180°라고 한다", "맞꼭지각은 크기가 같아요. 이웃한 각의 합이 180°예요."),
                     ("엇각과 동위각을 바꾸어 찾는다", "동위각은 같은 쪽 같은 위치, 엇각은 두 직선 사이에서 엇갈린 위치예요."),
                     ("평면에서도 꼬인 위치가 생긴다고 한다", "꼬인 위치는 공간에서만 생겨요.")],
                    [("평행선 성질의 역도 성립하나요?", "네. 동위각이나 엇각의 크기가 같으면 두 직선은 평행해요."),
                     ("직육면체에서 꼬인 위치는 어떻게 찾나요?", "한 모서리와 만나는 모서리, 평행한 모서리를 지우고 남은 것을 세어요.")],
                    [("점, 선, 면", [(b_count(), 20)]),
                     ("맞꼭지각과 각의 크기", [(b_vertical(), 12), (b_angle_sum(), 8)]),
                     ("위치 관계", [(b_position(), 8), (b_count(), 12)]),
                     ("평행선의 성질", [(b_parallel(), 20)]),
                     ("섞어서 연습", [(b_parallel(), 10), (b_vertical(), 6), (b_angle_sum(), 4)])], 82710)
    if which == "cong":
        return unit(G, "constructions-and-congruent-triangles", 11, "[9수03-03] [9수03-04]",
                    "삼각형을 작도하고, 그 과정을 설명할 수 있다. 삼각형의 합동 조건을 이해하고, 이를 이용하여 두 삼각형이 합동인지 판별할 수 있다.",
                    "작도와 삼각형의 합동 조건", "작도와 합동",
                    "중학교 1학년 수학 작도와 합동 문제: 작도 도구, 삼각형의 세 변의 길이 조건, 삼각형이 하나로 정해지는 조건, SSS·SAS·ASA 합동, 대응변과 대응각까지 100문제와 정답·해설.",
                    "SSS, SAS, ASA 합동", "가장 긴 변 &lt; 나머지 두 변의 합이어야 삼각형이 돼요.",
                    ["눈금 없는 자와 컴퍼스만으로 도형을 그리는 것을 <b>작도</b>라고 해요.",
                     "세 변의 길이가 주어질 때 (가장 긴 변) &lt; (나머지 두 변의 합)이어야 삼각형을 그릴 수 있어요.",
                     "삼각형은 세 변 / 두 변과 그 끼인각 / 한 변과 그 양 끝 각이 주어지면 하나로 정해져요.",
                     "두 삼각형은 <b>SSS, SAS, ASA</b> 중 하나를 만족하면 합동이에요. △ABC ≡ △DEF는 꼭짓점 순서대로 대응해요."],
                    [("3 cm, 5 cm와 나머지 한 변", ["5 − 3 &lt; x &lt; 5 + 3"], "2 &lt; x &lt; 8"),
                     ("AB = DE, ∠B = ∠E, BC = EF", ["두 변과 끼인각"], "SAS 합동")],
                    [("세 각의 크기가 같으면 합동이라고 한다", "세 각이 같아도 크기가 다를 수 있어요."),
                     ("끼인각이 아닌 각으로 SAS 합동이라고 한다", "SAS는 두 변 사이의 각이어야 해요."),
                     ("2 cm, 3 cm, 5 cm로 삼각형을 그릴 수 있다고 한다", "5 = 2 + 3이라 삼각형이 되지 않아요.")],
                    [("작도할 때 각도기를 쓰면 안 되나요?", "작도는 길이와 각을 재지 않고 그리는 약속이에요. 각도기와 눈금 있는 자는 쓰지 않아요."),
                     ("합동 증명은 언제 배우나요?", "2학년 이등변삼각형과 사각형의 성질에서 합동 조건을 이용해 성질을 설명해요.")],
                    [("작도", [(g_construct(), 20)]),
                     ("삼각형이 되는 조건", [(g_construct(), 20)]),
                     ("합동 조건", [(g_cong(), 20)]),
                     ("대응변과 대응각", [(g_cong(), 20)]),
                     ("섞어서 연습", [(g_cong(), 10), (g_construct(), 10)])], 82711)
    if which == "poly":
        return unit(G, "polygons", 12, "[9수03-05]",
                    "다각형의 성질을 이해하고 설명할 수 있다.",
                    "다각형: 대각선, 내각과 외각의 크기", "다각형",
                    "중학교 1학년 수학 다각형 문제: 대각선의 개수, 삼각형의 내각과 외각, n각형의 내각의 합, 외각의 합 360°, 정다각형의 한 내각과 외각까지 100문제와 정답·해설.",
                    "내각의 합 = 180° × (n − 2)", "외각의 합은 항상 360°예요.",
                    ["n각형의 한 꼭짓점에서 그을 수 있는 대각선은 (n − 3)개, 대각선의 총 개수는 <b>n(n − 3)/2</b>개예요.",
                     "삼각형의 한 외각의 크기는 이웃하지 않는 두 내각의 크기의 합과 같아요.",
                     "n각형의 내각의 크기의 합은 <b>180° × (n − 2)</b>예요.",
                     "다각형의 외각의 크기의 합은 항상 <b>360°</b>예요. 정n각형의 한 외각은 360° ÷ n이에요."],
                    [("정팔각형의 한 내각", ["180° × 6 ÷ 8"], "135°"),
                     ("십각형의 대각선의 개수", ["10 × 7 ÷ 2"], "35개")],
                    [("대각선의 수를 n(n − 3)으로 센다", "한 대각선을 두 번 세었으니 2로 나누어요."),
                     ("내각의 합을 180° × n으로 한다", "삼각형으로 나누면 (n − 2)개예요."),
                     ("외각의 합이 변의 수에 따라 커진다고 한다", "외각의 합은 항상 360°예요.")],
                    [("왜 내각의 합이 180° × (n − 2)인가요?", "한 꼭짓점에서 대각선을 그으면 n각형이 (n − 2)개의 삼각형으로 나뉘어요."),
                     ("정다각형의 한 외각을 먼저 구하면 편한가요?", "네. 360° ÷ n으로 외각을 구하고 180°에서 빼면 한 내각이에요.")],
                    [("대각선", [(pg_calc(("diag", "diag1")), 20)]),
                     ("삼각형의 내각과 외각", [(pg_tri(), 20)]),
                     ("내각의 합", [(pg_calc(("sum",)), 12), (pg_calc(("inv",)), 8)]),
                     ("정다각형", [(pg_calc(("each", "ext")), 20)]),
                     ("섞어서 연습", [(pg_tri(), 8), (pg_calc(("diag", "sum", "each", "ext", "inv")), 12)])], 82712)
    if which == "sector":
        return unit(G, "circles-and-sectors", 13, "[9수03-06]",
                    "부채꼴의 중심각과 호의 관계를 이해하고, 이를 이용하여 부채꼴의 호의 길이와 넓이를 구할 수 있다.",
                    "원과 부채꼴: 호의 길이와 넓이", "원과 부채꼴",
                    "중학교 1학년 수학 원과 부채꼴 문제: 원의 둘레와 넓이(π 사용), 중심각과 호의 길이·넓이의 비례, 부채꼴의 호의 길이·넓이·둘레까지 100문제와 정답·해설.",
                    "호의 길이 = 2πr × (중심각/360)", "부채꼴의 넓이 = ½ × r × (호의 길이)",
                    ["반지름이 r인 원의 둘레는 <b>2πr</b>, 넓이는 <b>πr²</b>이에요.",
                     "한 원에서 부채꼴의 호의 길이와 넓이는 <b>중심각의 크기에 정비례</b>해요. 현의 길이는 정비례하지 않아요.",
                     "중심각이 x°인 부채꼴: 호의 길이 l = 2πr × x/360, 넓이 S = πr² × x/360",
                     "S = ½rl로도 넓이를 구할 수 있어요."],
                    [("r = 6, 중심각 120°", ["l = 2π × 6 × 120/360", "S = π × 36 × 120/360"], "4π, 12π"),
                     ("r = 4, l = 3π의 넓이", ["½ × 4 × 3π"], "6π")],
                    [("지름을 반지름처럼 쓴다", "공식은 반지름 r을 써요."),
                     ("부채꼴의 둘레에 반지름을 더하지 않는다", "둘레 = 호의 길이 + 반지름 × 2"),
                     ("현의 길이도 중심각에 정비례한다고 한다", "현은 정비례하지 않아요.")],
                    [("π는 3.14로 계산하나요?", "중학교에서는 π를 그대로 남겨 답을 써요."),
                     ("부채꼴과 활꼴의 차이는?", "부채꼴은 두 반지름과 호, 활꼴은 현과 호로 둘러싸인 도형이에요.")],
                    [("원의 둘레와 넓이", [(circ_calc(), 20)]),
                     ("중심각과 호", [(sec_ratio(), 20)]),
                     ("호의 길이", [(sec_calc(("arc", "peri")), 20)]),
                     ("부채꼴의 넓이", [(sec_calc(("area", "area_l")), 20)]),
                     ("섞어서 연습", [(sec_calc(), 12), (sec_ratio(), 8)])], 82713)
    if which == "solid":
        return unit(G, "polyhedra-and-solids-of-revolution", 14, "[9수03-07]",
                    "구체적인 모형이나 공학 도구를 이용하여 다면체와 회전체의 성질을 탐구하고, 이를 설명할 수 있다.",
                    "다면체와 회전체", "다면체와 회전체",
                    "중학교 1학년 수학 다면체와 회전체 문제: 각기둥·각뿔·각뿔대의 면·모서리·꼭짓점, 정다면체 5가지, 회전체 만들기, 회전체의 단면까지 100문제와 정답·해설.",
                    "정다면체는 5가지뿐", "회전축에 수직으로 자른 단면은 항상 원이에요.",
                    ["다각형인 면으로만 둘러싸인 입체를 <b>다면체</b>라고 해요. n각기둥은 면 n + 2개, n각뿔은 면 n + 1개예요.",
                     "모든 면이 합동인 정다각형이고 각 꼭짓점에 모인 면의 수가 같은 다면체가 <b>정다면체</b>예요. 정사면체, 정육면체, 정팔면체, 정십이면체, 정이십면체 5가지예요.",
                     "평면도형을 한 직선을 축으로 한 바퀴 돌려 만든 입체가 <b>회전체</b>예요(원기둥, 원뿔, 구, 원뿔대).",
                     "회전체를 회전축에 수직인 평면으로 자르면 원, 회전축을 포함하는 평면으로 자르면 선대칭 도형이 생겨요."],
                    [("육각뿔의 모서리", ["2 × 6"], "12개"),
                     ("직각삼각형을 한 변을 축으로 회전", ["원뿔"], "원뿔")],
                    [("오각뿔의 면을 5개라고 한다", "옆면 5개 + 밑면 1개 = 6개예요."),
                     ("정다면체가 무수히 많다고 한다", "5가지뿐이에요."),
                     ("원기둥을 다면체라고 한다", "곡면이 있으니 회전체예요.")],
                    [("정다면체가 5가지뿐인 이유는?", "한 꼭짓점에 모인 각의 합이 360°보다 작아야 입체가 되는데, 그런 경우가 5가지뿐이에요."),
                     ("집에서 어떻게 확인하나요?", "전개도를 접어 보거나, 종이를 막대에 붙여 돌려 보면 회전체를 쉽게 상상할 수 있어요.")],
                    [("다면체의 구성 요소", [(so_poly(), 20)]),
                     ("다면체의 종류", [(so_which(("faces", "name")), 20)]),
                     ("정다면체", [(so_which(("regular",)), 15), (so_which(("faces",)), 5)]),
                     ("회전체", [(so_rot(), 20)]),
                     ("섞어서 연습", [(so_poly(), 8), (so_rot(), 12)])], 82714)
    if which == "area":
        return unit(G, "surface-area-and-volume", 15, "[9수03-08]",
                    "입체도형의 겉넓이와 부피를 구할 수 있다.",
                    "입체도형의 겉넓이와 부피", "겉넓이와 부피",
                    "중학교 1학년 수학 입체도형의 겉넓이와 부피 문제: 각기둥과 원기둥, 각뿔과 원뿔, 구의 겉넓이와 부피, 원뿔·구·원기둥의 부피의 비까지 100문제와 정답·해설.",
                    "뿔의 부피 = ⅓ × (밑넓이) × (높이)", "구: 겉넓이 4πr², 부피 ⁴⁄₃πr³",
                    ["기둥의 부피 = (밑넓이) × (높이), 겉넓이 = (밑넓이) × 2 + (옆넓이)",
                     "원기둥의 옆넓이는 직사각형으로 펼치면 2πr × h예요.",
                     "뿔의 부피는 같은 밑면과 높이를 가진 기둥 부피의 <b>⅓</b>이에요. 원뿔의 옆넓이는 πrl(l은 모선)이에요.",
                     "반지름이 r인 구의 겉넓이는 <b>4πr²</b>, 부피는 <b>⁴⁄₃πr³</b>이에요."],
                    [("r = 3, h = 5 원기둥의 부피", ["π × 9 × 5"], "45π cm³"),
                     ("r = 3, h = 4 원뿔의 부피", ["⅓ × π × 9 × 4"], "12π cm³")],
                    [("원뿔의 부피에 ⅓을 곱하지 않는다", "뿔은 항상 ⅓을 곱해요."),
                     ("원기둥의 겉넓이에 밑넓이를 한 번만 더한다", "밑면은 위아래 2개예요."),
                     ("구의 겉넓이를 πr²으로 쓴다", "구의 겉넓이는 4πr²이에요.")],
                    [("원뿔의 옆넓이는 어떻게 구하나요?", "펼치면 반지름이 모선 l인 부채꼴이 되고, 넓이는 ½ × l × 2πr = πrl이에요."),
                     ("단위는 어떻게 쓰나요?", "넓이는 cm², 부피는 cm³을 써요.")],
                    [("기둥의 겉넓이와 부피", [(vol_calc(("prism", "cyl_v", "cyl_s")), 20)]),
                     ("뿔의 겉넓이와 부피", [(vol_calc(("pyr", "cone_v", "cone_s")), 20)]),
                     ("구의 겉넓이와 부피", [(vol_calc(("sph_v", "sph_s")), 14), (vol_ratio(), 6)]),
                     ("겉넓이와 부피 비교", [(vol_ratio(), 6), (vol_calc(), 14)]),
                     ("섞어서 연습", [(vol_calc(), 20)])], 82715)
    if which == "rep":
        return unit(G, "representative-values", 16, "[9수04-01]",
                    "중앙값, 최빈값의 뜻을 알고, 자료의 특성에 따라 적절한 대푯값을 선택하여 구할 수 있다.",
                    "대푯값: 평균, 중앙값, 최빈값", "대푯값",
                    "중학교 1학년 수학 대푯값 문제: 평균, 홀수·짝수 개 자료의 중앙값, 최빈값, 모르는 값 구하기, 자료에 알맞은 대푯값 고르기까지 100문제와 정답·해설.",
                    "중앙값은 크기순으로 한가운데", "극단적인 값이 있으면 중앙값이 대푯값으로 좋아요.",
                    ["자료 전체의 특징을 대표하는 값을 <b>대푯값</b>이라 하고, 평균, 중앙값, 최빈값이 있어요.",
                     "<b>중앙값</b>은 자료를 크기순으로 늘어놓았을 때 한가운데 값이에요. 자료가 짝수 개이면 가운데 두 값의 평균이에요.",
                     "<b>최빈값</b>은 가장 많이 나타난 값이에요. 여러 개일 수도 있어요.",
                     "극단적인 값이 있으면 평균보다 중앙값, 수가 아닌 자료는 최빈값이 알맞아요."],
                    [("3, 8, 5, 10, 7, 4의 중앙값", ["3, 4, 5, 7, 8, 10", "(5 + 7) ÷ 2"], "6"),
                     ("2, 5, 5, 7, 9, 5의 최빈값", ["5가 3번"], "5")],
                    [("크기순으로 늘어놓지 않고 가운데 값을 고른다", "먼저 작은 값부터 늘어놓아요."),
                     ("짝수 개 자료에서 가운데 값 하나만 고른다", "가운데 두 값의 평균이에요."),
                     ("최빈값은 항상 1개라고 한다", "가장 많이 나온 값이 여럿이면 모두 최빈값이에요.")],
                    [("평균은 초등학교에서도 배웠죠?", "네. 중학교에서는 중앙값과 최빈값을 더해 상황에 맞는 대푯값을 골라요."),
                     ("3학년에서는 무엇을 배우나요?", "자료가 흩어진 정도를 나타내는 분산과 표준편차, 상자그림을 배워요.")],
                    [("평균", [(st_rep(("mean",)), 20)]),
                     ("중앙값", [(st_rep(("med_odd", "med_even")), 20)]),
                     ("최빈값", [(st_rep(("mode",)), 20)]),
                     ("모르는 값과 알맞은 대푯값", [(st_rep(("unk",)), 14), (st_choose(), 6)]),
                     ("섞어서 연습", [(st_rep(), 20)])], 82716)
    if which == "freq":
        return unit(G, "frequency-distributions-and-histograms", 17, "[9수04-02]",
                    "자료를 줄기와 잎 그림, 도수분포표, 히스토그램, 도수분포다각형으로 나타내고 해석할 수 있다.",
                    "줄기와 잎 그림, 도수분포표, 히스토그램", "자료의 정리",
                    "중학교 1학년 수학 자료의 정리 문제: 줄기와 잎 그림 읽기, 도수분포표의 계급과 도수, 히스토그램과 도수분포다각형 읽기, 넓이와 비율까지 100문제와 정답·해설.",
                    "계급의 크기 × 도수의 합 = 히스토그램의 넓이", "도수분포다각형의 넓이도 히스토그램과 같아요.",
                    ["<b>줄기와 잎 그림</b>은 십의 자리를 줄기, 일의 자리를 잎으로 나타내어 자료를 그대로 볼 수 있어요.",
                     "자료를 몇 개의 구간(<b>계급</b>)으로 나누고 각 계급의 자료 수(<b>도수</b>)를 나타낸 표가 <b>도수분포표</b>예요.",
                     "계급의 크기를 가로, 도수를 세로로 하는 직사각형으로 나타낸 그래프가 <b>히스토그램</b>이에요.",
                     "히스토그램의 각 직사각형 윗변의 중점을 이은 그래프가 <b>도수분포다각형</b>이고, 넓이는 히스토그램과 같아요."],
                    [("계급 60 이상 70 미만의 크기", ["70 − 60"], "10"),
                     ("계급의 크기 10, 도수의 합 30인 히스토그램의 넓이", ["10 × 30"], "300")],
                    [("70점인 학생을 60 이상 70 미만에 넣는다", "70은 70 이상 80 미만 계급이에요."),
                     ("계급의 크기를 계급의 개수로 쓴다", "계급의 크기는 구간의 폭이에요."),
                     ("도수분포다각형의 넓이를 히스토그램의 절반이라고 한다", "두 넓이는 같아요.")],
                    [("줄기와 잎 그림의 장점은?", "원래 자료의 값을 그대로 알 수 있고 분포도 함께 볼 수 있어요."),
                     ("계급은 몇 개로 나누나요?", "보통 5~15개 정도로 나누어요.")],
                    [("줄기와 잎 그림", [(f_stem(), 20)]),
                     ("도수분포표", [(f_table(), 20)]),
                     ("히스토그램", [(f_hist(), 20)]),
                     ("도수분포다각형과 넓이", [(f_hist(), 20)]),
                     ("섞어서 연습", [(f_table(), 10), (f_hist(), 10)])], 82717)
    if which == "rel":
        return unit(G, "relative-frequency", 18, "[9수04-03]",
                    "상대도수를 구하고, 상대도수의 분포를 표나 그래프로 나타내고 해석할 수 있다.",
                    "상대도수와 그 분포", "상대도수",
                    "중학교 1학년 수학 상대도수 문제: 상대도수 구하기, 도수와 전체 도수 구하기, 상대도수의 분포표, 백분율, 전체 도수가 다른 두 집단의 비교까지 100문제와 정답·해설.",
                    "상대도수 = 도수 ÷ 전체 도수", "상대도수의 합은 항상 1이에요.",
                    ["각 계급의 도수를 전체 도수로 나눈 값을 <b>상대도수</b>라고 해요.",
                     "(도수) = (전체 도수) × (상대도수), (전체 도수) = (도수) ÷ (상대도수)",
                     "상대도수의 합은 항상 <b>1</b>이고, 상대도수 × 100은 백분율(%)이에요.",
                     "전체 도수가 다른 두 집단은 도수가 아니라 <b>상대도수</b>로 비교해요."],
                    [("전체 40명 중 10명인 계급", ["10 ÷ 40"], "0.25"),
                     ("상대도수 0.2, 도수 8", ["8 ÷ 0.2"], "40")],
                    [("상대도수를 전체 도수 ÷ 도수로 구한다", "도수 ÷ 전체 도수예요."),
                     ("학생 수가 다른 두 반을 도수로 비교한다", "상대도수(비율)로 비교해요."),
                     ("상대도수의 합이 전체 도수라고 한다", "상대도수의 합은 항상 1이에요.")],
                    [("상대도수는 어디에 쓰이나요?", "학교·지역마다 인원이 다른 자료를 공정하게 비교할 때 써요."),
                     ("상대도수의 분포를 나타내는 그래프는?", "히스토그램이나 도수분포다각형 모양으로 나타내요.")],
                    [("상대도수 구하기", [(r_calc(("rel", "pct")), 20)]),
                     ("도수와 전체 도수", [(r_calc(("freq", "total")), 20)]),
                     ("상대도수의 분포표", [(r_table(), 20)]),
                     ("두 집단 비교하기", [(r_compare(), 20)]),
                     ("섞어서 연습", [(r_calc(), 10), (r_table(), 5), (r_compare(), 5)])], 82718)
    raise ValueError(which)
