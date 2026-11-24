# -*- coding: utf-8 -*-
"""
대한민국 초등 5학년 수학：도형과 측정
  perimeter : 평면도형의 둘레 [6수03-11]
  area      : 넓이 단위와 직사각형・정사각형의 넓이 [6수03-12] [6수03-13]
  area2     : 평행사변형, 삼각형, 사다리꼴, 마름모의 넓이 [6수03-14]
  congruent : 합동 [6수03-01]
  symmetry  : 선대칭도형과 점대칭도형 [6수03-02]
  cuboid    : 직육면체와 정육면체, 겨냥도와 전개도 [6수03-03] [6수03-04]
誤答は「둘레를 넓이로 계산한다」「단위 환산을 100배로 한다」「삼각형에서 ÷ 2를 빠뜨린다」「높이 대신 빗변을 쓴다」「대응변을 잘못 찾는다」から作る。
"""
import math
import random
from kr_common import mcq, unit, Names, josa, num
from kr_pics import fig, svg_wrap, text, line, poly, lab, PT, INK, RED, BLUE, LIGHT
from kr_pics56 import box_svg, sym_grid, lg

R = random.Random(82508)
NM = Names(R)


def side_labels(pts, labs, fs=18):
    """辺の外側に長さ（辺の法線の向きで文字の寄せ方を決める）"""
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    out = ""
    for i, t in enumerate(labs):
        if not t:
            continue
        a, b = pts[i], pts[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ex, ey = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ex, ey) or 1
        nx, ny = -ey / L, ex / L
        if nx * (mx - cx) + ny * (my - cy) < 0:
            nx, ny = -nx, -ny
        if abs(nx) > 0.6:
            out += text(mx + nx * 10, my + 6, t, fs, anchor="start" if nx > 0 else "end")
        else:
            out += text(mx + nx * 16, my + ny * 16 + (12 if ny > 0 else -2), t, fs)
    return out


def shape(pts, labs, right=(), W=300, H=220, extra=""):
    halo = extra.replace("<text ", "<text stroke='#fff' stroke-width='5' paint-order='stroke' ")
    return poly(pts, None, right=right, W=W, H=H, extra=side_labels(pts, labs) + halo).replace("<svg ", "<svg data-pf='lg' ", 1)


# ---------------------------------------------------------------- 둘레
def per_rect():
    a, b = R.randint(3, 25), R.randint(2, 20)
    if a == b:
        return None
    s = 140.0 / max(a, b)
    w, h = a * s, b * s
    pic = shape([(50, 30), (50 + w, 30), (50 + w, 30 + h), (50, 30 + h)], ["%d cm" % a, "%d cm" % b, "", ""], right=(0, 1, 2, 3), W=int(w) + 140, H=int(h) + 70)
    return mcq(pic + "직사각형의 둘레는 몇 cm인가요?", "%d cm" % (2 * (a + b)), ["%d cm" % x for x in (a + b, a * b, 2 * a + b)],
               "(가로 + 세로) × 2 = (%d + %d) × 2 = <b>%d cm</b>" % (a, b, 2 * (a + b)))


def per_regular():
    n = R.choice([3, 4, 5, 6, 8])
    a = R.randint(3, 20)
    nm = {3: "정삼각형", 4: "정사각형", 5: "정오각형", 6: "정육각형", 8: "정팔각형"}[n]
    if R.random() < 0.6:
        return mcq("한 변이 %d cm인 %s의 둘레는 몇 cm인가요?" % (a, nm), "%d cm" % (a * n), ["%d cm" % x for x in (a * (n - 1), a + n, a * a)],
                   "%s은 변이 %d개이고 길이가 모두 같아요. %d × %d = <b>%d cm</b>" % (nm, n, a, n, a * n))
    return mcq("둘레가 %d cm인 %s의 한 변은 몇 cm인가요?" % (a * n, nm), "%d cm" % a, ["%d cm" % x for x in (a * n // 2 if a * n % 2 == 0 else a + 1, a * n - n, a + 2)],
               "%d ÷ %d = <b>%d cm</b>" % (a * n, n, a))


def per_para():
    k = R.choice(["para", "rh"])
    a, b = R.randint(4, 18), R.randint(3, 15)
    if k == "rh":
        b = a
    o = 40
    s = 140.0 / max(a, b)
    w, h = a * s, b * s * 0.8
    pts = [(30 + o, 30), (30 + o + w, 30), (30 + w, 30 + h), (30, 30 + h)]
    nm = "평행사변형" if k == "para" else "마름모"
    pic = shape(pts, ["%d cm" % a, "%d cm" % b, "", ""], W=int(w + o) + 110, H=int(h) + 70)
    return mcq(pic + "%s의 둘레는 몇 cm인가요?" % nm, "%d cm" % (2 * (a + b)), ["%d cm" % x for x in (a + b, a * b, 4 * a if a != b else 2 * a)],
               ("마주 보는 두 변의 길이가 같아요. (%d + %d) × 2 = <b>%d cm</b>" % (a, b, 2 * (a + b))) if k == "para" else
               ("네 변의 길이가 모두 같아요. %d × 4 = <b>%d cm</b>" % (a, 4 * a)))


def per_back():
    a = R.randint(4, 20)
    b = R.randint(3, 15)
    if a == b:
        return None
    p = 2 * (a + b)
    return mcq("둘레가 %d cm인 직사각형의 가로가 %d cm예요. 세로는 몇 cm인가요?" % (p, a), "%d cm" % b, ["%d cm" % x for x in (p - a, p // 2, p - 2 * a)],
               "가로 + 세로 = %d ÷ 2 = %d, 세로 = %d − %d = <b>%d cm</b>" % (p, p // 2, p // 2, a, b))


def per_L():
    a, b = R.randint(8, 16), R.randint(6, 12)
    c, d = R.randint(2, a - 3), R.randint(2, b - 3)
    s = 12.0
    A, B, C, Dd = a * s, b * s, c * s, d * s
    pts = [(40, 30), (40 + C, 30), (40 + C, 30 + Dd), (40 + A, 30 + Dd), (40 + A, 30 + B), (40, 30 + B)]
    pic = shape(pts, ["", "", "", "%d cm" % (b - d), "%d cm" % a, "%d cm" % b], right=(0, 1, 3, 4, 5), W=int(A) + 120, H=int(B) + 80)
    return mcq(pic + "도형의 둘레는 몇 cm인가요? (모든 각은 직각이에요)", "%d cm" % (2 * (a + b)),
               ["%d cm" % x for x in (a + b + (b - d) + a, 2 * (a + b) - c, a * b)],
               "변을 옮기면 가로 %d cm, 세로 %d cm인 직사각형의 둘레와 같아요. (%d + %d) × 2 = <b>%d cm</b>" % (a, b, a, b, 2 * (a + b)))


# ---------------------------------------------------------------- 넓이 단위, 직사각형
def area_rect():
    a, b = R.randint(3, 25), R.randint(2, 20)
    u = R.choice(["cm", "m"])
    sq = a == b
    if sq:
        return mcq("한 변이 %d %s인 정사각형의 넓이는 몇 %s²인가요?" % (a, u, u), "%d %s²" % (a * a, u), ["%d %s²" % (x, u) for x in (4 * a, 2 * a, a * a + a)],
                   "(한 변) × (한 변) = %d × %d = <b>%d %s²</b>" % (a, a, a * a, u))
    s = 140.0 / max(a, b)
    w, h = a * s, b * s
    pic = shape([(50, 30), (50 + w, 30), (50 + w, 30 + h), (50, 30 + h)], ["%d %s" % (a, u), "%d %s" % (b, u), "", ""], right=(0, 1, 2, 3), W=int(w) + 140, H=int(h) + 70)
    return mcq(pic + "직사각형의 넓이는 몇 %s²인가요?" % u, "%d %s²" % (a * b, u), ["%d %s²" % (x, u) for x in (2 * (a + b), a + b, a * b + a)],
               "(가로) × (세로) = %d × %d = <b>%d %s²</b>" % (a, b, a * b, u))


def area_unit():
    k = R.choice(["m2cm", "cm2m", "km2m", "m2km"])
    if k == "m2cm":
        n = R.randint(2, 30)
        return mcq("%d m²는 몇 cm²인가요?" % n, "%s cm²" % num(n * 10000), ["%s cm²" % num(n * x) for x in (100, 1000, 100000)],
                   "1 m² = 100 cm × 100 cm = 10,000 cm²예요. <b>%s cm²</b>" % num(n * 10000))
    if k == "cm2m":
        n = R.randint(2, 30)
        return mcq("%s cm²는 몇 m²인가요?" % num(n * 10000), "%d m²" % n, ["%s m²" % num(x) for x in (n * 100, n * 10, n * 1000)],
                   "10,000 cm² = 1 m²예요. <b>%d m²</b>" % n)
    if k == "km2m":
        n = R.randint(2, 30)
        return mcq("%d km²는 몇 m²인가요?" % n, "%s m²" % num(n * 1000000), ["%s m²" % num(n * x) for x in (1000, 10000, 100000)],
                   "1 km² = 1000 m × 1000 m = 1,000,000 m²예요. <b>%s m²</b>" % num(n * 1000000))
    n = R.randint(2, 30)
    return mcq("%s m²는 몇 km²인가요?" % num(n * 1000000), "%d km²" % n, ["%s km²" % num(x) for x in (n * 1000, n * 100, n * 10)],
               "1,000,000 m² = 1 km²예요. <b>%d km²</b>" % n)


def area_big():
    a, b = R.randint(2, 9), R.randint(2, 9)
    if R.random() < 0.5:
        return mcq("가로 %d km, 세로 %d km인 직사각형 모양 땅의 넓이는 몇 km²인가요?" % (a, b), "%d km²" % (a * b), ["%d km²" % x for x in (2 * (a + b), a + b, a * b * 1000)],
                   "%d × %d = <b>%d km²</b>" % (a, b, a * b))
    a, b = R.randint(100, 900) // 100 * 100, R.randint(2, 9)
    return mcq("가로 %d cm, 세로 %d m인 직사각형의 넓이는 몇 m²인가요?" % (a, b), "%d m²" % (a // 100 * b), ["%s m²" % num(x) for x in (a * b, a * b // 10, a // 100 + b)],
               "%d cm = %d m로 단위를 맞추어요. %d × %d = <b>%d m²</b>" % (a, a // 100, a // 100, b, a // 100 * b))


def area_back():
    a = R.randint(3, 20)
    b = R.randint(2, 15)
    return mcq("넓이가 %d cm²인 직사각형의 가로가 %d cm예요. 세로는 몇 cm인가요?" % (a * b, a), "%d cm" % b, ["%d cm" % x for x in (a * b - a, b + 1, (a * b) // 2 - a if (a * b) // 2 > a else b + 2)],
               "(세로) = (넓이) ÷ (가로) = %d ÷ %d = <b>%d cm</b>" % (a * b, a, b))


def area_L():
    a, b = R.randint(8, 16), R.randint(6, 12)
    c, d = R.randint(2, a - 3), R.randint(2, b - 3)
    s = 12.0
    A, B, C, Dd = a * s, b * s, c * s, d * s
    pts = [(40, 30), (40 + C, 30), (40 + C, 30 + Dd), (40 + A, 30 + Dd), (40 + A, 30 + B), (40, 30 + B)]
    pic = shape(pts, ["%d cm" % c, "%d cm" % d, "", "", "%d cm" % a, "%d cm" % b], right=(0, 1, 3, 4, 5), W=int(A) + 120, H=int(B) + 80)
    ar = a * b - (a - c) * d
    return mcq(pic + "도형의 넓이는 몇 cm²인가요? (모든 각은 직각이에요)", "%d cm²" % ar, ["%d cm²" % x for x in (a * b, 2 * (a + b), a * b - c * d)],
               "큰 직사각형에서 빈 부분을 빼요. %d × %d − %d × %d = <b>%d cm²</b>" % (a, b, a - c, d, ar))


# ---------------------------------------------------------------- 여러 가지 도형의 넓이
def area_shape(kind):
    def mk():
        if kind == "para":
            b, h = R.randint(4, 16), R.randint(3, 12)
            sl = R.randint(h + 1, h + 4)
            s = 150.0 / max(b + 3, h)
            o = 45
            pts = [(30 + o, 30), (30 + o + b * s, 30), (30 + b * s, 30 + h * s), (30, 30 + h * s)]
            ex = line(30 + o, 30, 30 + o, 30 + h * s, RED, 2, " stroke-dasharray='6 4'") + text(30 + o + 8, 30 + h * s / 2 + 6, "%d cm" % h, 17, col=RED, anchor="start")
            pic = shape(pts, ["", "%d cm" % sl, "%d cm" % b, ""], W=int(b * s + o) + 90, H=int(h * s) + 70, extra=ex)
            ans = b * h
            return mcq(pic + "평행사변형의 넓이는 몇 cm²인가요?", "%d cm²" % ans, ["%d cm²" % x for x in (b * sl, ans // 2 if ans % 2 == 0 else ans + b, 2 * (b + sl))],
                       "(밑변) × (높이) = %d × %d = <b>%d cm²</b>. 비스듬한 변이 아니라 높이를 곱해요." % (b, h, ans))
        if kind == "tri":
            b, h = R.randint(4, 18), R.randint(3, 14)
            if b * h % 2:
                return None
            s = 150.0 / max(b, h)
            apx = R.uniform(0.2, 0.8) * b * s
            pts = [(30, 30 + h * s), (30 + b * s, 30 + h * s), (30 + apx, 30)]
            ex = line(30 + apx, 30, 30 + apx, 30 + h * s, RED, 2, " stroke-dasharray='6 4'") + text(30 + apx + 8, 30 + h * s / 2, "%d cm" % h, 17, col=RED, anchor="start")
            pic = shape(pts, ["%d cm" % b, "", ""], W=int(b * s) + 100, H=int(h * s) + 70, extra=ex)
            ans = b * h // 2
            return mcq(pic + "삼각형의 넓이는 몇 cm²인가요?", "%d cm²" % ans, ["%d cm²" % x for x in (b * h, b + h, ans + b)],
                       "(밑변) × (높이) ÷ 2 = %d × %d ÷ 2 = <b>%d cm²</b>" % (b, h, ans))
        if kind == "trap":
            a, b, h = R.randint(3, 10), R.randint(6, 16), R.randint(3, 10)
            if a >= b or (a + b) * h % 2:
                return None
            s = 150.0 / max(b, h)
            o = (b - a) * s * R.uniform(0.2, 0.8)
            pts = [(30 + o, 30), (30 + o + a * s, 30), (30 + b * s, 30 + h * s), (30, 30 + h * s)]
            ex = line(30 + o, 30, 30 + o, 30 + h * s, RED, 2, " stroke-dasharray='6 4'") + text(30 + o + 8, 30 + h * s / 2 + 6, "%d cm" % h, 17, col=RED, anchor="start")
            pic = shape(pts, ["%d cm" % a, "", "%d cm" % b, ""], W=int(b * s) + 90, H=int(h * s) + 70, extra=ex)
            ans = (a + b) * h // 2
            return mcq(pic + "사다리꼴의 넓이는 몇 cm²인가요?", "%d cm²" % ans, ["%d cm²" % x for x in ((a + b) * h, a * b * h // 2 if a * b * h % 2 == 0 else ans + h, b * h)],
                       "((윗변) + (아랫변)) × (높이) ÷ 2 = (%d + %d) × %d ÷ 2 = <b>%d cm²</b>" % (a, b, h, ans))
        p, q = R.randint(4, 16), R.randint(4, 16)
        if p * q % 2:
            return None
        s = 130.0 / max(p, q)
        cx, cy = 30 + p * s / 2, 25 + q * s / 2
        pts = [(cx, 25), (30 + p * s, cy), (cx, 25 + q * s), (30, cy)]
        ex = line(30, cy, 30 + p * s, cy, RED, 2, " stroke-dasharray='6 4'") + line(cx, 25, cx, 25 + q * s, BLUE, 2, " stroke-dasharray='6 4'")
        ex += text(cx + p * s / 4, cy - 8, "%d cm" % p, 16, col=RED) + text(cx + 8, cy + q * s / 4 + 8, "%d cm" % q, 16, col=BLUE, anchor="start")
        pic = shape(pts, ["", "", "", ""], W=int(p * s) + 70, H=int(q * s) + 55, extra=ex)
        ans = p * q // 2
        return mcq(pic + "두 대각선이 %d cm, %d cm인 마름모의 넓이는 몇 cm²인가요?" % (p, q), "%d cm²" % ans, ["%d cm²" % x for x in (p * q, p + q, 2 * (p + q))],
                   "(한 대각선) × (다른 대각선) ÷ 2 = %d × %d ÷ 2 = <b>%d cm²</b>" % (p, q, ans))
    return mk


def area_back2():
    k = R.choice(["tri", "para", "trap"])
    if k == "tri":
        b, h = R.randint(4, 18), R.randint(3, 14)
        if b * h % 2:
            return None
        A = b * h // 2
        return mcq("넓이가 %d cm²이고 밑변이 %d cm인 삼각형의 높이는 몇 cm인가요?" % (A, b), "%d cm" % h, ["%d cm" % x for x in (A // b if A // b != h else h + 1, A - b, h * 2)],
                   "(높이) = (넓이) × 2 ÷ (밑변) = %d × 2 ÷ %d = <b>%d cm</b>" % (A, b, h))
    if k == "para":
        b, h = R.randint(4, 18), R.randint(3, 14)
        return mcq("넓이가 %d cm²이고 높이가 %d cm인 평행사변형의 밑변은 몇 cm인가요?" % (b * h, h), "%d cm" % b, ["%d cm" % x for x in (b * 2, b * h - h, b + 1)],
                   "(밑변) = (넓이) ÷ (높이) = %d ÷ %d = <b>%d cm</b>" % (b * h, h, b))
    a, c, h = R.randint(3, 10), R.randint(6, 16), R.randint(3, 10)
    if a >= c or (a + c) * h % 2:
        return None
    A = (a + c) * h // 2
    return mcq("넓이가 %d cm²이고 윗변이 %d cm, 아랫변이 %d cm인 사다리꼴의 높이는 몇 cm인가요?" % (A, a, c), "%d cm" % h,
               ["%d cm" % x for x in (A // (a + c) if A // (a + c) != h else h + 1, h * 2, A - a - c if A - a - c > 0 else h + 3)],
               "(높이) = (넓이) × 2 ÷ ((윗변) + (아랫변)) = %d × 2 ÷ %d = <b>%d cm</b>" % (A, a + c, h))


def area_same():
    b, h = R.randint(3, 12), R.randint(3, 12)
    k = R.choice(["tri", "para"])
    return mcq("모양이 서로 다른 %s 3개의 밑변이 모두 %d cm, 높이가 모두 %d cm예요. 세 도형의 넓이는 어떤가요?" % ("삼각형" if k == "tri" else "평행사변형", b, h),
               "모두 같아요", ["모두 달라요", "가장 길쭉한 것이 넓어요", "알 수 없어요"],
               "밑변과 높이가 같으면 모양이 달라도 넓이는 <b>모두 같아요</b>.")


# ---------------------------------------------------------------- 합동
def tri_pair():
    while True:
        a, b, c = R.randint(4, 14), R.randint(4, 14), R.randint(4, 14)
        if a + b > c and b + c > a and a + c > b and len({a, b, c}) == 3:
            return a, b, c


def tri_pts(a, b, c, ox, oy, s):
    # 변 ㄴㄷ = a（아래）、ㄱㄴ = c、ㄱㄷ = b
    x = (c * c - b * b + a * a) / (2.0 * a)
    y = math.sqrt(max(c * c - x * x, 1))
    return [(ox + x * s, oy), (ox, oy + y * s), (ox + a * s, oy + y * s)]


def cong_fig(a, b, c, flip=False):
    s = 110.0 / max(a, b, c)
    base = tri_pts(a, b, c, 0, 0, s)
    mnx = min(p[0] for p in base)
    base = [(x - mnx, y) for x, y in base]
    w = max(p[0] for p in base)
    p1 = [(60 + x, 34 + y) for x, y in base]
    q = [(w - x, y) for x, y in base] if flip else base
    p2 = [(60 + w + 110 + x, 34 + y) for x, y in q]
    W = int(60 + w + 110 + w + 60)
    H = int(max(p[1] for p in p1 + p2)) + 50
    body = ""
    for pts, names in ((p1, "ㄱㄴㄷ"), (p2, "ㄹㅁㅂ")):
        body += "<polygon points='%s' fill='%s' stroke='%s' stroke-width='3'/>" % (" ".join("%.1f,%.1f" % p for p in pts), LIGHT, INK)
        cx, cy = sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3
        for p, t in zip(pts, names):
            dx, dy = p[0] - cx, p[1] - cy
            d = math.hypot(dx, dy) or 1
            body += lab(p[0] + dx / d * 18, p[1] + dy / d * 18, t)
    body += side_labels(p1, ["%d cm" % c, "%d cm" % a, "%d cm" % b], 16)
    return fig(lg(svg_wrap(W, H, body, "합동인 두 삼각형")))


def cong_side():
    a, b, c = tri_pair()
    flip = R.random() < 0.5
    pic = cong_fig(a, b, c, flip)
    sides = {"ㅁㅂ": a, "ㄹㅂ": b, "ㄹㅁ": c}
    k = R.choice(list(sides))
    return mcq(pic + "두 삼각형은 서로 합동이에요. 변 %s의 길이는 몇 cm인가요?" % k, "%d cm" % sides[k], ["%d cm" % v for v in set(sides.values()) if v != sides[k]] + ["%d cm" % (sides[k] + 1)],
               "변 %s의 대응변은 변 %s이에요. 합동인 도형에서 대응변의 길이는 같아요. <b>%d cm</b>" % (k, {"ㅁㅂ": "ㄴㄷ", "ㄹㅂ": "ㄱㄷ", "ㄹㅁ": "ㄱㄴ"}[k], sides[k]))


def cong_corr():
    k = R.choice(["pt", "side", "ang"])
    pts = {"ㄱ": "ㄹ", "ㄴ": "ㅁ", "ㄷ": "ㅂ"}
    if k == "pt":
        p = R.choice(list(pts))
        return mcq("삼각형 ㄱㄴㄷ과 삼각형 ㄹㅁㅂ은 합동이에요(ㄱ↔ㄹ, ㄴ↔ㅁ, ㄷ↔ㅂ). 점 %s의 대응점은?" % p, "점 " + pts[p], ["점 " + v for v in pts.values() if v != pts[p]] + ["점 " + p],
                   "겹쳤을 때 완전히 겹치는 점이 대응점이에요. <b>점 %s</b>" % pts[p])
    if k == "side":
        a, b = R.sample(list(pts), 2)
        ans = "변 " + pts[a] + pts[b]
        others = ["변 %s%s" % (pts[x], pts[y]) for x, y in (("ㄱ", "ㄴ"), ("ㄴ", "ㄷ"), ("ㄱ", "ㄷ")) if {x, y} != {a, b}]
        return mcq("삼각형 ㄱㄴㄷ과 삼각형 ㄹㅁㅂ은 합동이에요(ㄱ↔ㄹ, ㄴ↔ㅁ, ㄷ↔ㅂ). 변 %s%s의 대응변은?" % (a, b), ans, others + ["변 %s%s" % (a, b)],
                   "대응점끼리 이어요. %s→%s, %s→%s이므로 <b>%s</b>" % (a, pts[a], b, pts[b], ans))
    x, y = R.randint(30, 80), R.randint(30, 80)
    z = 180 - x - y
    if z < 20:
        return None
    return mcq("삼각형 ㄱㄴㄷ과 삼각형 ㄹㅁㅂ은 합동이에요(ㄱ↔ㄹ, ㄴ↔ㅁ, ㄷ↔ㅂ). 각 ㄱㄴㄷ = %d°, 각 ㄴㄷㄱ = %d°일 때 각 ㅁㄹㅂ은 몇 도인가요?" % (x, y), "%d°" % z,
               ["%d°" % v for v in (x, y, 180 - z)], "각 ㅁㄹㅂ의 대응각은 각 ㄴㄱㄷ이에요. 180° − %d° − %d° = <b>%d°</b>" % (x, y, z))


COND = [("세 변의 길이가 각각 같은 두 삼각형", "항상 합동이에요"), ("세 각의 크기가 각각 같은 두 삼각형", "합동이 아닐 수도 있어요"),
        ("두 변의 길이와 그 사이에 있는 각의 크기가 같은 두 삼각형", "항상 합동이에요"), ("한 변의 길이와 그 양 끝 각의 크기가 같은 두 삼각형", "항상 합동이에요"),
        ("넓이가 같은 두 직사각형", "합동이 아닐 수도 있어요"), ("둘레가 같은 두 정사각형", "항상 합동이에요"), ("둘레가 같은 두 직사각형", "합동이 아닐 수도 있어요"),
        ("반지름이 같은 두 원", "항상 합동이에요"), ("한 변의 길이가 같은 두 정삼각형", "항상 합동이에요"), ("한 변의 길이가 같은 두 마름모", "합동이 아닐 수도 있어요")]


def cong_cond():
    t, a = R.choice(COND)
    return mcq("「%s」는 서로 합동인가요?" % t, a,
               ["항상 합동이에요" if a != "항상 합동이에요" else "합동이 아닐 수도 있어요", "절대 합동이 아니에요", "넓이만 같아요"],
               "모양과 크기가 같아서 포개었을 때 완전히 겹쳐야 합동이에요. <b>%s</b>." % a)


def cong_per():
    a, b, c = tri_pair()
    return mcq("삼각형 ㄱㄴㄷ과 삼각형 ㄹㅁㅂ은 합동이에요. 변 ㄱㄴ = %d cm, 변 ㄴㄷ = %d cm, 변 ㄱㄷ = %d cm일 때 삼각형 ㄹㅁㅂ의 둘레는 몇 cm인가요?" % (c, a, b),
               "%d cm" % (a + b + c), ["%d cm" % x for x in ((a + b + c) * 2, a + b, a * 3)], "합동이면 둘레도 같아요. %d + %d + %d = <b>%d cm</b>" % (a, b, c, a + b + c))


# ---------------------------------------------------------------- 대칭
LINE_AX = {"정삼각형": 3, "정사각형": 4, "직사각형": 2, "마름모": 2, "정오각형": 5, "정육각형": 6, "원": "셀 수 없이 많아요", "이등변삼각형": 1, "정팔각형": 8}
POINT = {"정사각형": True, "직사각형": True, "평행사변형": True, "마름모": True, "정육각형": True, "원": True, "정삼각형": False, "정오각형": False, "이등변삼각형": False, "사다리꼴": False}


def ax_count():
    nm = R.choice([k for k, v in LINE_AX.items() if v != "셀 수 없이 많아요"])
    v = LINE_AX[nm]
    return mcq("%s의 대칭축은 모두 몇 개인가요?" % nm, "%d개" % v, ["%d개" % x for x in (v + 1, v - 1 if v > 1 else v + 2, v * 2)],
               "접었을 때 완전히 겹치는 직선을 모두 세요. <b>%d개</b>" % v)


def pt_which():
    want = R.random() < 0.5
    good = [k for k, v in POINT.items() if v == want]
    bad = [k for k, v in POINT.items() if v != want]
    if len(bad) < 3:
        return None
    a = R.choice(good)
    opts = R.sample(bad, 3)
    show = opts + [a]
    R.shuffle(show)
    return mcq("%s 중에서 점대칭도형%s 것은?" % (", ".join(show), "인" if want else "이 <b>아닌</b>"), a, opts,
               "한 점을 중심으로 180° 돌렸을 때 처음 도형과 완전히 겹치면 점대칭도형이에요. <b>%s</b>" % a)


LETTERS = {"A": ("선", False), "B": ("선", False), "C": ("선", False), "D": ("선", False), "E": ("선", False), "H": ("둘 다", True), "I": ("둘 다", True),
           "M": ("선", False), "N": ("점", True), "O": ("둘 다", True), "S": ("점", True), "T": ("선", False), "U": ("선", False), "V": ("선", False),
           "W": ("선", False), "X": ("둘 다", True), "Z": ("점", True), "F": ("없음", False), "G": ("없음", False), "L": ("없음", False), "P": ("없음", False), "R": ("없음", False)}
NAMES = {"선": "선대칭도형", "점": "점대칭도형", "둘 다": "선대칭도형이면서 점대칭도형", "없음": "둘 다 아니에요"}


def letter_q():
    ch = R.choice(list(LETTERS))
    a = NAMES[LETTERS[ch][0]]
    return mcq("알파벳 「<b>%s</b>」는 어떤 도형인가요? (글자는 반듯한 직선과 곡선으로 그렸다고 생각해요)" % ch, a, [v for v in NAMES.values() if v != a],
               "선을 따라 접어 겹치면 선대칭, 180° 돌려 겹치면 점대칭이에요. <b>%s</b>" % a)


def grow(start, n, x0, x1, y0, y1):
    cells = set(start)
    while len(cells) < n:
        x, y = R.choice(sorted(cells))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        if x0 <= x + dx <= x1 and y0 <= y + dy <= y1:
            cells.add((x + dx, y + dy))
    return cells


def grid_shape():
    """8×8 칸、가운데 세로선 대칭인 도형 또는 아닌 도형"""
    sym = R.random() < 0.6
    left = grow({(3, R.randint(2, 5))}, R.randint(4, 7), 1, 3, 1, 6)
    cells = set(left) | {(7 - i, j) for i, j in left}
    if not sym:
        c = R.choice(sorted(cells))
        cells.discard(c)
        if (7 - c[0], c[1]) not in cells:
            return None
    pic = sym_grid(sorted(cells), axis="v", label="빨간 점선을 그은 도형")
    a = "선대칭도형이에요" if sym else "선대칭도형이 아니에요"
    return mcq(pic + "빨간 점선을 따라 접으면 이 도형은 어떤가요?", a, ["선대칭도형이 아니에요" if sym else "선대칭도형이에요", "점대칭도형이에요", "알 수 없어요"],
               "점선의 왼쪽과 오른쪽 칸이 짝을 이루는지 확인해요. <b>%s</b>." % a)


def grid_pt():
    sym = R.random() < 0.6
    half = grow({(3, 3), (4, 3)}, R.randint(4, 7), 1, 6, 1, 3)
    cells = set(half) | {(7 - i, 7 - j) for i, j in half}
    if not sym:
        c = R.choice(sorted(cells))
        cells.discard(c)
        if (7 - c[0], 7 - c[1]) not in cells:
            return None
    pic = sym_grid(sorted(cells), center=(4, 4), label="빨간 점이 있는 도형")
    a = "점대칭도형이에요" if sym else "점대칭도형이 아니에요"
    return mcq(pic + "빨간 점을 중심으로 180° 돌리면 이 도형은 어떤가요?", a, ["점대칭도형이 아니에요" if sym else "점대칭도형이에요", "선대칭도형이에요", "알 수 없어요"],
               "빨간 점을 지나 반대쪽 같은 거리에 짝이 되는 칸이 있는지 확인해요. <b>%s</b>." % a)


def sym_prop():
    k = R.choice(["line", "point", "ang"])
    d = R.randint(3, 15)
    if k == "line":
        return mcq("선대칭도형에서 대응점 ㄱ과 ㄴ을 이은 선분이 대칭축과 만나는 점을 ㄷ이라고 해요. 선분 ㄱㄷ이 %d cm이면 선분 ㄱㄴ은 몇 cm인가요?" % d, "%d cm" % (2 * d),
                   ["%d cm" % x for x in (d, d + 2, d // 2 if d % 2 == 0 else d + 1)], "대칭축은 대응점을 이은 선분을 둘로 똑같이 나눠요. %d × 2 = <b>%d cm</b>" % (d, 2 * d))
    if k == "point":
        return mcq("점대칭도형에서 대응점 ㄱ과 ㄴ을 이은 선분의 길이가 %d cm예요. 대칭의 중심에서 점 ㄱ까지는 몇 cm인가요?" % (2 * d), "%d cm" % d,
                   ["%d cm" % x for x in (2 * d, 4 * d, d + 1)], "대칭의 중심은 대응점을 이은 선분을 둘로 똑같이 나눠요. %d ÷ 2 = <b>%d cm</b>" % (2 * d, d))
    a = R.randint(30, 150)
    return mcq("선대칭도형에서 한 각이 %d°일 때, 그 각의 대응각은 몇 도인가요?" % a, "%d°" % a, ["%d°" % x for x in (180 - a, 360 - a, a // 2)] if a != 90 else ["45°", "180°", "270°"],
               "대응각의 크기는 서로 같아요. <b>%d°</b>" % a)


# ---------------------------------------------------------------- 직육면체
def cub_count():
    k = R.choice(["면", "모서리", "꼭짓점"])
    nm = R.choice(["직육면체", "정육면체"])
    v = {"면": 6, "모서리": 12, "꼭짓점": 8}[k]
    return mcq("%s의 %s 몇 개인가요?" % (nm, josa(k, "은/는")), "%d개" % v, ["%d개" % x for x in {6, 8, 12, 4} - {v}],
               "%s는 면 6개, 모서리 12개, 꼭짓점 8개예요. <b>%d개</b>" % (nm, v))


def cub_more():
    k = R.choice(["sum", "back", "cnt"])
    a = R.randint(2, 15)
    if k == "sum":
        return mcq("한 모서리가 %d cm인 정육면체의 모든 모서리의 길이의 합은 몇 cm인가요?" % a, "%d cm" % (12 * a), ["%d cm" % x for x in (6 * a, 8 * a, 4 * a)],
                   "정육면체의 모서리 12개는 길이가 모두 같아요. %d × 12 = <b>%d cm</b>" % (a, 12 * a))
    if k == "back":
        return mcq("모든 모서리의 길이의 합이 %d cm인 정육면체의 한 모서리는 몇 cm인가요?" % (12 * a), "%d cm" % a, ["%d cm" % x for x in (2 * a, 12 * a // 8 if 12 * a % 8 == 0 else a + 1, 12 * a // 6)],
                   "%d ÷ 12 = <b>%d cm</b>" % (12 * a, a))
    b, c = R.randint(2, 12), R.randint(2, 12)
    return mcq("가로 %d cm, 세로 %d cm, 높이 %d cm인 직육면체에서 길이가 %d cm인 모서리는 몇 개인가요?" % (a, b, c, a), "%d개" % (4 * ([a, b, c].count(a))),
               ["%d개" % x for x in {2, 4, 6, 8, 12} - {4 * [a, b, c].count(a)}], "같은 방향의 모서리 4개씩 길이가 같아요. <b>%d개</b>" % (4 * [a, b, c].count(a)))


def cub_sketch():
    a, b, c = R.randint(3, 12), R.randint(2, 9), R.randint(2, 9)
    k = R.choice(["hidden", "seen", "vhid", "sum"])
    pic = box_svg(a, b, c)
    if k == "hidden":
        return mcq(pic + "직육면체의 겨냥도에서 보이지 않는 모서리는 몇 개인가요?", "3개", ["9개", "4개", "2개"], "보이지 않는 모서리는 점선으로 그리고 <b>3개</b>예요.")
    if k == "seen":
        return mcq(pic + "직육면체의 겨냥도에서 보이는 모서리는 몇 개인가요?", "9개", ["12개", "3개", "6개"], "모서리 12개 중 보이지 않는 3개를 빼면 <b>9개</b>예요.")
    if k == "vhid":
        return mcq(pic + "직육면체의 겨냥도에서 보이지 않는 꼭짓점은 몇 개인가요?", "1개", ["3개", "7개", "2개"], "점선 3개가 만나는 꼭짓점 <b>1개</b>가 보이지 않아요.")
    return mcq(pic + "이 직육면체의 모든 모서리의 길이의 합은 몇 cm인가요?", "%d cm" % (4 * (a + b + c)), ["%d cm" % x for x in (a + b + c, 2 * (a + b + c), a * b * c)],
               "같은 길이의 모서리가 4개씩 있어요. (%d + %d + %d) × 4 = <b>%d cm</b>" % (a, b, c, 4 * (a + b + c)))


CUB_FACTS = [("직육면체에서 서로 마주 보는 면은 평행해요.", "○"), ("직육면체에서 한 면과 수직인 면은 4개예요.", "○"), ("정육면체는 직육면체라고 할 수 있어요.", "○"),
             ("직육면체는 정육면체라고 할 수 있어요.", "×"), ("직육면체의 면은 모두 정사각형이에요.", "×"), ("정육면체의 모서리의 길이는 모두 같아요.", "○"),
             ("직육면체에서 한 꼭짓점에서 만나는 면은 3개예요.", "○"), ("직육면체에서 평행한 면은 모두 2쌍이에요.", "×")]


def cub_fact():
    t, a = R.choice(CUB_FACTS)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "크기에 따라 달라요"],
               "직육면체: 직사각형 6개, 마주 보는 면 3쌍이 평행, 한 면과 수직인 면 4개. 정육면체는 정사각형 6개로 된 직육면체예요.")


def roll(state, d):
    Bt, T, N, S, E, W = state
    if d == "E":
        return (E, W, N, S, T, Bt)
    if d == "W":
        return (W, E, N, S, Bt, T)
    if d == "N":
        return (N, S, T, Bt, E, W)
    return (S, N, Bt, T, E, W)


def faces(cells):
    cells = set(cells)
    start = min(cells)
    seen = {start: (0, 1, 2, 3, 4, 5)}
    todo = [start]
    while todo:
        c = todo.pop()
        x, y = c
        for d, (dx, dy) in (("E", (1, 0)), ("W", (-1, 0)), ("N", (0, -1)), ("S", (0, 1))):
            n = (x + dx, y + dy)
            if n in cells and n not in seen:
                seen[n] = roll(seen[c], d)
                todo.append(n)
    if len(seen) == 6 and len({s[0] for s in seen.values()}) == 6:
        return {c: s[0] for c, s in seen.items()}
    return None


def hexomino():
    cells = {(0, 0)}
    while len(cells) < 6:
        x, y = R.choice(sorted(cells))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        cells.add((x + dx, y + dy))
    mx, my = min(c[0] for c in cells), min(c[1] for c in cells)
    cells = frozenset((x - mx, y - my) for x, y in cells)
    if max(c[0] for c in cells) > 3 or max(c[1] for c in cells) > 3:
        return None
    return cells


def net_pic(nets, labels="가나다라", q=22, marks=None):
    s = []
    for i, cells in enumerate(nets):
        ox = 10 + i * 112
        for (x, y) in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#e8f3ec' stroke='%s' stroke-width='1.6'/>" % (ox + x * q, 10 + y * q, q, q, INK))
            if marks and (x, y) in marks:
                s.append(text(ox + x * q + q / 2, 10 + y * q + q / 2 + 6, marks[(x, y)], 15))
        if labels:
            s.append(text(ox + 44, 10 + 4 * q + 20, labels[i], 17))
    rows = max(y for cells in nets for _, y in cells) + 1
    return fig(lg(svg_wrap(10 + len(nets) * 112 if labels else 20 + 4 * q, 20 + rows * q + (26 if labels else 0), "".join(s), "정육면체의 전개도")))


def net_q():
    good, bad = [], []
    for _ in range(300):
        h = hexomino()
        if h:
            (good if faces(h) else bad).append(h)
    good, bad = list(dict.fromkeys(good)), list(dict.fromkeys(bad))
    want = R.random() < 0.6
    if want:
        ans, others = R.choice(good), R.sample(bad, 3)
    else:
        ans, others = R.choice(bad), R.sample(good, 3)
    nets = others + [ans]
    R.shuffle(nets)
    k = "가나다라"[nets.index(ans)]
    return mcq(net_pic(nets) + ("정육면체의 전개도인 것은?" if want else "정육면체의 전개도가 <b>아닌</b> 것은?"), k, [x for x in "가나다라" if x != k],
               ("접었을 때 6개의 면이 모두 다른 자리에 오는 것은 <b>%s</b>예요." if want else "<b>%s</b>는 접었을 때 두 면이 겹쳐요.") % k)


def net_opp():
    for _ in range(50):
        h = hexomino()
        if h and faces(h):
            break
    else:
        return None
    f = faces(h)
    cells = sorted(h)
    names = "ㄱㄴㄷㄹㅁㅂ"
    marks = {c: names[i] for i, c in enumerate(cells)}
    c0 = R.choice(cells)
    opp = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}[f[c0]]
    ans = [c for c in cells if f[c] == opp][0]
    return mcq(net_pic([h], labels=None, q=30, marks=marks) + "전개도를 접어서 정육면체를 만들 때, 면 %s과 마주 보는 면은?" % marks[c0], "면 " + marks[ans],
               ["면 " + marks[c] for c in cells if c not in (c0, ans)],
               "전개도에서 한 줄로 이어진 세 면 중 양 끝 면이 마주 봐요. <b>면 %s</b>" % marks[ans])


def build(which):
    G = "grade-5"
    if which == "perimeter":
        return unit(G, "perimeter-of-polygons", 8, "[6수03-11]",
                    "평면도형의 둘레를 이해하고, 기본적인 평면도형의 둘레를 구할 수 있다.",
                    "평면도형의 둘레", "도형의 둘레",
                    "초등 5학년 1학기 다각형의 둘레 학습지: 정다각형, 직사각형, 평행사변형, 마름모의 둘레, 둘레로 변의 길이 구하기, 직각으로 꺾인 도형의 둘레까지 100문제와 정답.",
                    "둘레는 모든 변의 길이의 합", "직사각형의 둘레 = (가로 + 세로) × 2",
                    ["도형의 <b>둘레</b>는 도형을 한 바퀴 돈 길이, 즉 모든 변의 길이의 합이에요.",
                     "정다각형의 둘레 = (한 변의 길이) × (변의 수)",
                     "직사각형과 평행사변형의 둘레 = (두 변의 길이의 합) × 2, 마름모의 둘레 = (한 변) × 4"],
                    [("가로 8 cm, 세로 5 cm인 직사각형의 둘레", ["(8 + 5) × 2 = 26"], "26 cm")],
                    [("둘레를 가로 × 세로로 구한다", "둘레는 길이의 합이에요. 곱하면 넓이예요."),
                     ("두 변만 더하고 2를 곱하지 않는다", "마주 보는 변도 더해야 해요."),
                     ("꺾인 도형에서 모르는 변을 빼먹는다", "변을 옮겨 직사각형으로 생각해요.")],
                    [("둘레와 넓이는 어떻게 다른가요?", "둘레는 길이(cm), 넓이는 평면의 크기(cm²)예요."),
                     ("둘레는 몇 학년에서 배우나요?", "2022 개정 교육과정에서는 초등 5학년 「다각형의 둘레와 넓이」 단원에서 배워요.")],
                    [("정다각형의 둘레", [(per_regular, 20)]),
                     ("직사각형의 둘레", [(per_rect, 20)]),
                     ("평행사변형과 마름모", [(per_para, 20)]),
                     ("둘레로 변의 길이 구하기", [(per_back, 12), (per_regular, 8)]),
                     ("꺾인 도형의 둘레", [(per_L, 20)])], 82508)
    if which == "area":
        return unit(G, "area-units-and-rectangles", 9, "[6수03-12] [6수03-13]",
                    "넓이 단위 1 cm², 1 m², 1 km²를 알며, 그 관계를 이해한다. 직사각형과 정사각형의 넓이를 구하는 방법을 이해하고, 이를 구할 수 있다.",
                    "넓이 단위와 직사각형의 넓이", "직사각형의 넓이",
                    "초등 5학년 1학기 학습지: 1 cm², 1 m², 1 km²의 관계, 직사각형과 정사각형의 넓이, 넓이로 변의 길이 구하기, 복잡한 도형의 넓이까지 100문제와 정답.",
                    "직사각형의 넓이 = 가로 × 세로", "1 m² = 10,000 cm², 1 km² = 1,000,000 m²",
                    ["한 변이 1 cm인 정사각형의 넓이가 <b>1 cm²</b>(1 제곱센티미터)예요.",
                     "직사각형의 넓이 = (가로) × (세로), 정사각형의 넓이 = (한 변) × (한 변)",
                     "1 m² = 100 cm × 100 cm = 10,000 cm², 1 km² = 1000 m × 1000 m = 1,000,000 m²",
                     "복잡한 도형은 직사각형으로 나누거나, 큰 직사각형에서 빈 곳을 빼서 구해요."],
                    [("가로 3 m, 세로 50 cm인 직사각형의 넓이", ["단위를 맞춰요: 50 cm = 0.5 m", "3 × 0.5 = 1.5"], "1.5 m² (= 15000 cm²)")],
                    [("1 m² = 100 cm²로 생각한다", "가로와 세로 모두 100배이므로 10000배예요."),
                     ("단위를 맞추지 않고 곱한다", "가로와 세로의 단위를 같게 한 뒤 곱해요."),
                     ("넓이를 (가로 + 세로) × 2로 구한다", "그것은 둘레예요.")],
                    [("넓이 단위는 언제 배우나요?", "2022 개정 교육과정에서는 초등 5학년 「다각형의 둘레와 넓이」 단원에서 배워요."),
                     ("1 km²는 얼마나 넓은가요?", "가로와 세로가 1 km인 땅의 넓이로, 축구장 약 140개 정도예요.")],
                    [("직사각형과 정사각형의 넓이", [(area_rect, 20)]),
                     ("넓이 단위의 관계", [(area_unit, 20)]),
                     ("넓이로 변의 길이 구하기", [(area_back, 20)]),
                     ("큰 넓이", [(area_big, 20)]),
                     ("복잡한 도형의 넓이", [(area_L, 20)])], 82509)
    if which == "area2":
        return unit(G, "area-of-parallelograms-triangles-trapezoids-and-rhombuses", 10, "[6수03-14]",
                    "평행사변형, 삼각형, 사다리꼴, 마름모의 넓이를 구하는 방법을 다양하게 추론하고, 이와 관련된 문제를 해결할 수 있다.",
                    "평행사변형, 삼각형, 사다리꼴, 마름모의 넓이", "여러 가지 도형의 넓이",
                    "초등 5학년 1학기 학습지: 평행사변형, 삼각형, 사다리꼴, 마름모의 넓이 공식, 넓이로 밑변과 높이 구하기까지 100문제와 정답.",
                    "밑변과 높이를 찾아 공식에 넣어요", "삼각형・사다리꼴・마름모는 ÷ 2",
                    ["평행사변형의 넓이 = (밑변) × (높이). 잘라서 옮기면 직사각형이 돼요.",
                     "삼각형의 넓이 = (밑변) × (높이) ÷ 2. 똑같은 삼각형 2개로 평행사변형을 만들 수 있어요.",
                     "사다리꼴의 넓이 = ((윗변) + (아랫변)) × (높이) ÷ 2",
                     "마름모의 넓이 = (한 대각선) × (다른 대각선) ÷ 2"],
                    [("밑변 10 cm, 높이 6 cm인 삼각형의 넓이", ["10 × 6 ÷ 2 = 30"], "30 cm²")],
                    [("높이 대신 비스듬한 변의 길이를 곱한다", "높이는 밑변에 수직인 선분의 길이예요."),
                     ("삼각형에서 ÷ 2를 빠뜨린다", "삼각형은 평행사변형의 반이에요."),
                     ("사다리꼴에서 윗변과 아랫변을 곱한다", "윗변과 아랫변을 더해요.")],
                    [("높이는 어떻게 찾나요?", "밑변에 수직으로 그은 선분의 길이예요. 도형 밖에 있을 수도 있어요."),
                     ("공식을 외우지 않고 구할 수 있나요?", "잘라 붙이거나 두 배로 만들어 직사각형・평행사변형으로 바꾸면 구할 수 있어요.")],
                    [("평행사변형의 넓이", [(area_shape("para"), 20)]),
                     ("삼각형의 넓이", [(area_shape("tri"), 16), (area_same, 4)]),
                     ("사다리꼴의 넓이", [(area_shape("trap"), 20)]),
                     ("마름모의 넓이", [(area_shape("rh"), 20)]),
                     ("넓이로 길이 구하기", [(area_back2, 20)])], 82510)
    if which == "congruent":
        return unit(G, "congruent-figures", 14, "[6수03-01]",
                    "도형의 합동을 이해하고, 합동인 도형의 성질을 탐구하고 설명할 수 있다.",
                    "도형의 합동과 대응점, 대응변, 대응각", "합동",
                    "초등 5학년 2학기 합동 학습지: 합동의 뜻, 대응점・대응변・대응각 찾기, 합동인 도형의 변의 길이와 각의 크기, 합동이 되는 조건까지 100문제와 정답.",
                    "포개었을 때 완전히 겹치면 합동", "대응변의 길이와 대응각의 크기가 같아요.",
                    ["모양과 크기가 같아서 포개었을 때 완전히 겹치는 두 도형을 서로 <b>합동</b>이라고 해요.",
                     "겹치는 점을 <b>대응점</b>, 겹치는 변을 <b>대응변</b>, 겹치는 각을 <b>대응각</b>이라고 해요.",
                     "합동인 두 도형에서 대응변의 길이와 대응각의 크기는 각각 같아요."],
                    [("삼각형 ㄱㄴㄷ ≡ 삼각형 ㄹㅁㅂ, 변 ㄴㄷ = 7 cm일 때 변 ㅁㅂ", ["ㄴ↔ㅁ, ㄷ↔ㅂ이므로 대응변"], "7 cm")],
                    [("이름의 순서를 무시하고 대응변을 찾는다", "대응점끼리 짝지어 대응변을 찾아요."),
                     ("모양만 같으면 합동이라고 한다", "크기도 같아야 합동이에요."),
                     ("세 각이 같으면 항상 합동이라고 한다", "크기가 다를 수 있어요.")],
                    [("합동과 닮음은 어떻게 다른가요?", "합동은 모양과 크기가 같고, 닮음은 모양만 같아요. 닮음은 중학교에서 배워요."),
                     ("뒤집어도 합동인가요?", "네. 뒤집어서 완전히 겹치면 합동이에요.")],
                    [("합동인 도형의 변", [(cong_side, 20)]),
                     ("대응점, 대응변, 대응각", [(cong_corr, 20)]),
                     ("합동인 도형의 성질", [(cong_side, 10), (cong_per, 10)]),
                     ("합동인 조건", [(cong_cond, 10), (cong_corr, 10)]),
                     ("섞어서 연습", [(cong_side, 8), (cong_corr, 6), (cong_per, 6)])], 82514)
    if which == "symmetry":
        return unit(G, "line-and-point-symmetry", 15, "[6수03-02]",
                    "실생활과 연결하여 선대칭도형과 점대칭도형을 이해하고 그릴 수 있다.",
                    "선대칭도형과 점대칭도형", "선대칭과 점대칭",
                    "초등 5학년 2학기 대칭 학습지: 선대칭도형과 대칭축, 점대칭도형과 대칭의 중심, 대칭축의 수, 알파벳의 대칭, 대응점과 거리의 성질까지 100문제와 정답.",
                    "접어서 겹치면 선대칭, 180° 돌려서 겹치면 점대칭", "대칭축・대칭의 중심은 대응점을 이은 선분을 이등분",
                    ["한 직선을 따라 접어서 완전히 겹치는 도형을 <b>선대칭도형</b>, 그 직선을 <b>대칭축</b>이라고 해요.",
                     "한 점을 중심으로 180° 돌렸을 때 처음 도형과 완전히 겹치는 도형을 <b>점대칭도형</b>, 그 점을 <b>대칭의 중심</b>이라고 해요.",
                     "대응점을 이은 선분은 대칭축과 수직으로 만나고, 대칭축(대칭의 중심)이 그 선분을 둘로 똑같이 나눠요."],
                    [("정사각형의 대칭축의 수", ["가로・세로 가운데 2개", "대각선 2개"], "4개")],
                    [("직사각형의 대각선도 대칭축이라고 한다", "대각선으로 접으면 겹치지 않아요. 대칭축은 2개예요."),
                     ("평행사변형을 선대칭도형이라고 한다", "평행사변형은 점대칭도형이지만 선대칭도형은 아니에요."),
                     ("점대칭은 90° 돌려서 겹치는 것이라고 생각한다", "180° 돌려서 겹쳐야 해요.")],
                    [("선대칭과 점대칭은 언제 배우나요?", "초등 5학년 2학기 「합동과 대칭」 단원에서 배워요."),
                     ("둘 다인 도형도 있나요?", "정사각형, 직사각형, 마름모, 원, 정육각형은 선대칭도형이면서 점대칭도형이에요.")],
                    [("선대칭도형", [(grid_shape, 20)]),
                     ("대칭축의 수", [(ax_count, 8), (letter_q, 12)]),
                     ("점대칭도형", [(pt_which, 10), (grid_pt, 10)]),
                     ("대칭의 성질", [(sym_prop, 20)]),
                     ("섞어서 연습", [(letter_q, 8), (grid_shape, 6), (sym_prop, 6)])], 82515)
    return unit(G, "cuboids-and-cubes", 17, "[6수03-03] [6수03-04]",
                "직육면체와 정육면체를 이해하고, 구성 요소와 성질을 탐구하고 설명할 수 있다. 직육면체와 정육면체의 겨냥도와 전개도를 그릴 수 있다.",
                "직육면체와 정육면체, 겨냥도와 전개도", "직육면체",
                "초등 5학년 2학기 직육면체 학습지: 면・모서리・꼭짓점의 수, 겨냥도에서 보이지 않는 모서리, 평행한 면과 수직인 면, 정육면체의 전개도, 마주 보는 면까지 100문제와 정답.",
                "면 6, 모서리 12, 꼭짓점 8", "마주 보는 면은 평행, 이웃한 면은 수직",
                ["직사각형 6개로 둘러싸인 도형을 <b>직육면체</b>, 정사각형 6개로 둘러싸인 도형을 <b>정육면체</b>라고 해요.",
                 "직육면체는 면 6개, 모서리 12개, 꼭짓점 8개예요. 마주 보는 면 3쌍은 평행하고, 한 면과 수직인 면은 4개예요.",
                 "<b>겨냥도</b>는 보이는 모서리를 실선, 보이지 않는 모서리 3개를 점선으로 그려요.",
                 "<b>전개도</b>는 모서리를 잘라서 펼친 그림이에요. 접었을 때 겹치는 면이 없어야 해요."],
                [("가로 5 cm, 세로 3 cm, 높이 4 cm인 직육면체의 모든 모서리의 합", ["같은 길이가 4개씩", "(5 + 3 + 4) × 4 = 48"], "48 cm")],
                [("보이지 않는 모서리를 4개라고 한다", "점선으로 그리는 모서리는 3개예요."),
                 ("직육면체를 정육면체라고 한다", "정육면체가 직육면체에 포함되고, 거꾸로는 아니에요."),
                 ("전개도에서 이웃한 면을 마주 보는 면으로 생각한다", "한 줄의 세 면 중 양 끝 면이 마주 봐요.")],
                [("직육면체는 언제 배우나요?", "초등 5학년 2학기 「직육면체」 단원에서 배워요. 6학년에서 겉넓이와 부피를 배워요."),
                 ("정육면체의 전개도는 몇 가지인가요?", "모두 11가지예요.")],
                [("면, 모서리, 꼭짓점", [(cub_count, 6), (cub_fact, 6), (cub_more, 8)]),
                 ("겨냥도", [(cub_sketch, 20)]),
                 ("정육면체의 전개도", [(net_q, 20)]),
                 ("마주 보는 면", [(net_opp, 20)]),
                 ("섞어서 연습", [(cub_sketch, 8), (net_q, 6), (net_opp, 6)])], 82517)
