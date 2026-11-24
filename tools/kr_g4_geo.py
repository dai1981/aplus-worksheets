# -*- coding: utf-8 -*-
"""
대한민국 초등 4학년 수학：도형과 측정 の 8 単元
  angles    : 각도와 각도기, 예각과 둔각 [4수03-02] [4수03-24]
  anglesum  : 각도의 합과 차, 삼각형・사각형의 각의 합 [4수03-25]
  move      : 평면도형의 이동（밀기, 뒤집기, 돌리기）[4수03-04]
  position  : 평면에서 점의 이동（위치와 방향）[4수03-05]
  triangles : 이등변삼각형, 정삼각형, 예각・둔각삼각형 [4수03-08] [4수03-09]
  parallel  : 수직과 평행 [4수03-03]
  quads     : 여러 가지 사각형 [4수03-10]
  polygons  : 다각형, 정다각형, 대각선, 모양 채우기 [4수03-11] [4수03-12]
誤答は「각도기の 바깥쪽 눈금を読む（180° − x）」「뒤집기と돌리기の取り違え」「정사각형は 마름모ではない」「대각선 수を n(n−3) とする」から作る。
"""
import math
import random
from kr_common import mcq, unit, Names, josa, clock
from kr_pics import fig, svg_wrap, line, text, dot, lab, poly, PT, INK, RED, BLUE, LIGHT, GREEN
import gen_au_maths_y5_angles as AU

R = random.Random(82403)
NM = Names(R)
KIND = {"acute": "예각", "right": "직각", "obtuse": "둔각"}


def deg(v):
    return "%d°" % v


def akind(d):
    return "예각" if d < 90 else ("직각" if d == 90 else ("둔각" if d < 180 else "평각"))


def relabel(svg, label):
    import re
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)


# ---------------------------------------------------------------- 각도
def protractor():
    v = R.choice(list(range(15, 170, 5)))
    if v == 90:
        return None
    if R.random() < 0.5:
        pic = AU.protractor_svg([0, v], "각도기")
        e = "한 변이 오른쪽 0에 맞춰져 있으니 <b>안쪽 눈금</b>을 읽어요. <b>%s</b>" % deg(v)
    else:
        pic = AU.protractor_svg([180, 180 - v], "각도기")
        e = "한 변이 왼쪽 0에 맞춰져 있으니 <b>바깥쪽 눈금</b>을 읽어요. <b>%s</b>" % deg(v)
    pic = fig(relabel(pic, "각도기로 잰 각").replace("<svg ", "<svg data-pf='lg' ", 1))
    return mcq(pic + "각도기로 잰 빨간 두 변 사이의 각의 크기는 몇 도인가요?",
               deg(v), [deg(180 - v), deg(v + 10), deg(v - 10), deg(v + 5)], e + " 예각이면 90°보다 작고, 둔각이면 90°보다 커요.")


def classify():
    d = R.choice(list(range(10, 90, 5)) + [90, 90] + list(range(95, 180, 5)))
    ans = akind(d)
    return mcq("%s인 각은 예각, 직각, 둔각 중 어느 것인가요?" % deg(d), ans, [x for x in ("예각", "직각", "둔각", "평각") if x != ans],
               "0°보다 크고 90°보다 작은 각은 예각, 90°는 직각, 90°보다 크고 180°보다 작은 각은 둔각이에요. <b>%s</b>" % ans)


def estimate():
    d = R.choice([30, 45, 60, 120, 135, 150, 20, 160, 75, 105])
    rot = R.choice([0, 0, 10, 20, -10])
    pic = fig(relabel(AU.angle_fig(d, rot, "각"), "어림할 각").replace("<svg ", "<svg data-pf='lg' ", 1))
    w = [deg(x) for x in (180 - d, d + 40 if d + 40 < 180 else d - 40, d - 40 if d > 45 else d + 70) if x != d]
    return mcq(pic + "표시한 각의 크기를 어림한 것으로 가장 알맞은 것은?", deg(d), w,
               "직각(90°)과 비교해 보세요. 직각보다 %s 약 <b>%s</b>예요." % ("작으므로" if d < 90 else "크므로", deg(d)))


def clock_angle():
    h = R.choice([1, 2, 3, 4, 5, 7, 8, 9, 10, 11])
    a = (h % 12) * 30
    a = min(a, 360 - a)
    ans = akind(a)
    return mcq(clock(h, 0) + "%d시일 때 긴바늘과 짧은바늘이 이루는 작은 쪽의 각은 몇 도이고, 어떤 각인가요?" % h, "%s, %s" % (deg(a), ans),
               ["%s, %s" % (deg(a), akind(180 - a) if a != 90 else "둔각"), "%s, %s" % (deg(180 - a) if a != 90 else deg(60), akind(180 - a) if a != 90 else "예각"), "%s, %s" % (deg(a + 30), akind(a + 30))],
               "시계에서 숫자 한 칸은 30°예요. %d칸이니까 30° × %d = <b>%s</b>, %s이에요." % (min(h, 12 - h), min(h, 12 - h), deg(a), ans))


def add_sub():
    a, b = R.randint(15, 140), R.randint(15, 140)
    if R.random() < 0.5:
        if a + b > 360:
            return None
        return mcq("%s + %s =" % (deg(a), deg(b)), deg(a + b), [deg(a + b + 10), deg(abs(a - b)), deg(a + b - 10), deg(a + b + 100)],
                   "각도의 합은 자연수의 덧셈처럼 계산하고 °를 붙여요. <b>%s</b>" % deg(a + b))
    if a == b:
        return None
    a, b = max(a, b), min(a, b)
    return mcq("%s − %s =" % (deg(a), deg(b)), deg(a - b), [deg(a + b), deg(a - b + 10), deg(a - b - 10) if a - b > 10 else deg(a - b + 20), deg(180 - a + b)],
               "각도의 차는 자연수의 뺄셈처럼 계산하고 °를 붙여요. <b>%s</b>" % deg(a - b))


def tri_missing():
    a, b = R.randint(25, 100), R.randint(25, 100)
    c = 180 - a - b
    if c < 20:
        return None
    pic = fig(relabel(AU.shape_svg(AU.tri_pts(a, b), {0: deg(a), 1: deg(b), 2: "?"}, "삼각형", rights=()), "삼각형의 세 각").replace("<svg ", "<svg data-pf='lg' ", 1)) if 90 not in (a, b, c) else None
    if not pic:
        return None
    return mcq(pic + "삼각형에서 ?의 각도는 몇 도인가요?", deg(c), [deg(360 - a - b), deg(a + b), deg(c + 10), deg(180 - a)],
               "삼각형의 세 각의 크기의 합은 180°예요. 180° − %s − %s = <b>%s</b>" % (deg(a), deg(b), deg(c)))


def quad_missing():
    a, b, c = R.randint(60, 130), R.randint(60, 130), R.randint(60, 130)
    d = 360 - a - b - c
    if not 40 <= d <= 150:
        return None
    return mcq("사각형의 네 각 중 세 각의 크기가 %s, %s, %s예요. 나머지 한 각의 크기는 몇 도인가요?" % (deg(a), deg(b), deg(c)), deg(d),
               [deg(180 - (a + b + c) % 180) if (180 - (a + b + c) % 180) != d else deg(d + 20), deg(d + 10), deg(abs(180 - a - b)) or deg(d - 10), deg(360 - a - b)],
               "사각형의 네 각의 크기의 합은 360°예요. 360° − %s − %s − %s = <b>%s</b>" % (deg(a), deg(b), deg(c), deg(d)))


def straight():
    a = R.randint(20, 160)
    if a == 90:
        return None
    k = R.choice(["line", "tri_ext"])
    if k == "line":
        return mcq("직선 위의 한 점에서 그은 반직선이 직선과 %s의 각을 이루어요. 나머지 한 각은 몇 도인가요?" % deg(a), deg(180 - a), [deg(360 - a), deg(90 - a) if a < 90 else deg(a - 90), deg(a), deg(170 - a)],
                   "직선이 이루는 각은 180°예요. 180° − %s = <b>%s</b>" % (deg(a), deg(180 - a)))
    b = R.randint(20, 150 - a) if a < 130 else None
    if not b:
        return None
    return mcq("삼각형의 두 각이 %s와 %s예요. 나머지 한 각의 바깥쪽에 생기는 각(한 변을 늘였을 때 생기는 각)은 몇 도인가요?" % (deg(a), deg(b)), deg(a + b),
               [deg(180 - a - b), deg(360 - a - b), deg(a + b + 10)],
               "나머지 각은 180° − %s − %s = %s이고, 바깥쪽 각은 180° − %s = <b>%s</b>예요." % (deg(a), deg(b), deg(180 - a - b), deg(180 - a - b), deg(a + b)))


def two_set_squares():
    pairs = [(30, 45), (60, 45), (90, 45), (30, 90), (60, 90), (30, 60)]
    a, b = R.choice(pairs)
    if R.random() < 0.5:
        return mcq("두 삼각자를 겹치지 않게 붙여 %s와 %s의 각을 이어 붙였어요. 만들어진 각은 몇 도인가요?" % (deg(a), deg(b)), deg(a + b),
                   [deg(abs(a - b)) if a != b else deg(a + b + 15), deg(a + b + 15), deg(a + b - 15)], "두 각을 더해요. %s + %s = <b>%s</b>" % (deg(a), deg(b), deg(a + b)))
    return mcq("두 삼각자를 겹쳐서 %s의 각에서 %s의 각을 빼는 모양을 만들었어요. 만들어진 각은 몇 도인가요?" % (deg(max(a, b)), deg(min(a, b))), deg(abs(a - b)),
               [deg(a + b), deg(abs(a - b) + 15), deg(abs(a - b) - 5) if abs(a - b) > 5 else deg(abs(a - b) + 30)], "큰 각에서 작은 각을 빼요. <b>%s</b>" % deg(abs(a - b)))


# ---------------------------------------------------------------- 평면도형의 이동
SHAPES = [[(0, 0), (1, 0), (2, 0), (0, 1)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 0), (1, 0), (1, 1), (2, 1)],
          [(0, 0), (1, 0), (2, 0), (1, 1)], [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)], [(0, 0), (1, 0), (0, 1), (0, 2)],
          [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], [(1, 0), (0, 1), (1, 1), (1, 2), (2, 2)]]


def norm(cells):
    mx_, my_ = min(c[0] for c in cells), min(c[1] for c in cells)
    return sorted((x - mx_, y - my_) for x, y in cells)


def tf(cells, op):
    if op == "flipH":      # 오른쪽(왼쪽)으로 뒤집기
        return norm([(-x, y) for x, y in cells])
    if op == "flipV":      # 위쪽(아래쪽)으로 뒤집기
        return norm([(x, -y) for x, y in cells])
    if op == "r90":        # 시계 방향 90°（y は下向き）
        return norm([(-y, x) for x, y in cells])
    if op == "r180":
        return norm([(-x, -y) for x, y in cells])
    if op == "r270":
        return norm([(y, -x) for x, y in cells])
    return norm(cells)


def cells_svg(cells, ox, oy, c=18, col="#8fd0a8"):
    return "".join("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (ox + x * c, oy + y * c, c, c, col, INK) for x, y in cells)


def grid_box(ox, oy, n=4, c=18):
    s = ""
    for i in range(n + 1):
        s += line(ox + i * c, oy, ox + i * c, oy + n * c, "#cfd8d3", 1) + line(ox, oy + i * c, ox + n * c, oy + i * c, "#cfd8d3", 1)
    return s


def options_fig(base, opts):
    """처음 모양과 가〜라 4 つの 모양"""
    c = 18
    W = 120 + 4 * 100
    s = text(45, 16, "처음 모양", 13) + grid_box(10, 26) + cells_svg(base, 10, 26)
    s += line(108, 10, 108, 110, "#cfd8d3", 1.5)
    for i, sh in enumerate(opts):
        ox = 125 + i * 100
        s += text(ox + 36, 16, "가나다라"[i], 15) + grid_box(ox, 26) + cells_svg(sh, ox, 26)
    return fig(svg_wrap(W, 110, s, "처음 모양과 가, 나, 다, 라").replace("<svg ", "<svg data-pf='lg' ", 1))


OPNAME = {"flipH": "오른쪽으로 뒤집은", "flipV": "위쪽으로 뒤집은", "r90": "시계 방향으로 90°만큼 돌린", "r180": "시계 방향으로 180°만큼 돌린",
          "r270": "시계 반대 방향으로 90°만큼 돌린", "slide": "오른쪽으로 밀어서 옮긴"}


def move_pick(ops):
    def mk():
        base = norm(R.choice(SHAPES))
        op = R.choice(ops)
        ans = tf(base, op)
        others = []
        for o in ["flipH", "flipV", "r90", "r180", "r270", "slide"]:
            t = tf(base, o)
            if t != ans and t not in others:
                others.append(t)
        if len(others) < 3:
            return None
        opts = [ans] + R.sample(others, 3)
        R.shuffle(opts)
        k = opts.index(ans)
        letter = "가나다라"[k]
        return mcq(options_fig(base, opts) + "처음 모양을 %s 모양은 어느 것인가요?" % OPNAME[op], letter, [x for x in "가나다라" if x != letter],
                   {"flipH": "오른쪽이나 왼쪽으로 뒤집으면 왼쪽과 오른쪽이 서로 바뀌어요.", "flipV": "위쪽이나 아래쪽으로 뒤집으면 위쪽과 아래쪽이 서로 바뀌어요.",
                    "r90": "시계 방향으로 90° 돌리면 위쪽이 오른쪽으로 가요.", "r180": "180° 돌리면 위쪽은 아래쪽으로, 왼쪽은 오른쪽으로 가요.",
                    "r270": "시계 반대 방향으로 90° 돌리면 위쪽이 왼쪽으로 가요.", "slide": "밀기는 모양과 방향이 바뀌지 않아요."}[op] + " 답은 <b>%s</b>예요." % letter)
    return mk


FACTS = [("도형을 밀면 모양과 크기는 바뀌지 않아요.", "○"), ("도형을 오른쪽으로 뒤집으면 위쪽과 아래쪽이 바뀌어요.", "×"),
         ("도형을 위쪽으로 뒤집으면 위쪽과 아래쪽이 바뀌어요.", "○"), ("시계 방향으로 90°만큼 4번 돌리면 처음 모양이 돼요.", "○"),
         ("시계 방향으로 180°만큼 돌린 모양과 시계 반대 방향으로 180°만큼 돌린 모양은 같아요.", "○"),
         ("시계 방향으로 90°만큼 돌린 모양과 시계 반대 방향으로 90°만큼 돌린 모양은 항상 같아요.", "×"),
         ("오른쪽으로 2번 뒤집으면 처음 모양이 돼요.", "○"), ("도형을 밀면 방향이 바뀌어요.", "×"),
         ("시계 방향으로 270°만큼 돌린 모양은 시계 반대 방향으로 90°만큼 돌린 모양과 같아요.", "○"),
         ("위쪽으로 뒤집은 모양은 아래쪽으로 뒤집은 모양과 같아요.", "○"), ("오른쪽으로 뒤집은 모양은 왼쪽으로 뒤집은 모양과 달라요.", "×"),
         ("도형을 돌리면 크기가 바뀌어요.", "×")]


def move_fact():
    t, a = R.choice(FACTS)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "도형에 따라 달라요"],
               "밀기는 위치만, 뒤집기는 방향이 거울처럼, 돌리기는 돌린 방향과 각도만큼 바뀌어요. 모양과 크기는 그대로예요.")


def move_card():
    k = R.choice(["r180", "same"])
    if k == "r180":
        good = {"0": "0", "1": "1", "6": "9", "8": "8", "9": "6"}
        a, b = str(R.choice([1, 6, 8, 9])), str(R.choice([0, 1, 6, 8, 9]))
        s = a + b
        rot = "".join(good[ch] for ch in reversed(s))
        if rot[0] == "0":
            return None
        return mcq("숫자 카드 [%s]를 시계 방향으로 180°만큼 돌리면 어떤 수가 되나요?" % s, rot, [s, s[::-1], str(int(rot) + 1)],
                   "180° 돌리면 숫자의 순서도 바뀌고 각 숫자도 거꾸로 돼요. 6은 9, 9는 6이 돼요. <b>%s</b>" % rot)
    n = R.randint(2, 7)
    total = 90 * n
    r = total % 360
    ans = {0: "처음 모양", 90: "시계 방향으로 90°만큼 돌린 모양", 180: "시계 방향으로 180°만큼 돌린 모양", 270: "시계 반대 방향으로 90°만큼 돌린 모양"}[r]
    return mcq("도형을 시계 방향으로 90°만큼 %d번 돌린 모양과 같은 것은?" % n, ans,
               [x for x in ("처음 모양", "시계 방향으로 90°만큼 돌린 모양", "시계 방향으로 180°만큼 돌린 모양", "시계 반대 방향으로 90°만큼 돌린 모양") if x != ans],
               "90° × %d = %d°이고, 360°를 돌면 처음 모양이 돼요. %d°만큼 돌린 것과 같아요. <b>%s</b>" % (n, total, r, ans))


# ---------------------------------------------------------------- 위치와 방향
def gridpts(pts, n=8, c=32):
    """모눈과 점（pts = [(이름, x, y)]、y は上向き）"""
    W, H = n * c + 90, n * c + 30
    s = ""
    for i in range(n + 1):
        s += line(20 + i * c, 10, 20 + i * c, 10 + n * c, "#cfd8d3", 1) + line(20, 10 + i * c, 20 + n * c, 10 + i * c, "#cfd8d3", 1)
    for nm, x, y in pts:
        cx, cy = 20 + x * c, 10 + (n - y) * c
        s += dot(cx, cy, 7, RED if nm in ("ㄱ", "출발") else INK) + text(cx + 8, cy - 9, nm, 21, anchor="start")
    return fig(svg_wrap(W, H, s, "모눈 위의 점").replace("<svg ", "<svg data-pf='lg' ", 1))


def mv(dx, dy):
    parts = []
    if dx:
        parts.append("%s으로 %d칸" % ("오른쪽" if dx > 0 else "왼쪽", abs(dx)))
    if dy:
        parts.append("%s으로 %d칸" % ("위쪽" if dy > 0 else "아래쪽", abs(dy)))
    return ", ".join(parts)


def pos_where():
    x, y = R.randint(1, 4), R.randint(1, 4)
    dx, dy = R.choice([-1, 1]) * R.randint(1, 3), R.choice([-1, 1]) * R.randint(1, 3)
    tx, ty = x + dx, y + dy
    if not (0 <= tx <= 8 and 0 <= ty <= 8):
        return None
    wrong = [(x - dx, y + dy), (x + dx, y - dy), (x + dy, y + dx)]
    cand = [(tx, ty)] + [w for w in wrong if w != (tx, ty) and 0 <= w[0] <= 8 and 0 <= w[1] <= 8]
    if len(set(cand)) < 4:
        return None
    cand = list(dict.fromkeys(cand))[:4]
    R.shuffle(cand)
    names = "가나다라"
    pts = [("ㄱ", x, y)] + [(names[i], p[0], p[1]) for i, p in enumerate(cand)]
    ans = names[cand.index((tx, ty))]
    return mcq(gridpts(pts) + "점 ㄱ을 %s 이동한 위치에 있는 점은?" % mv(dx, dy), ans, [n for n in names if n != ans],
               "점 ㄱ에서 먼저 %s 가요. 도착한 점은 <b>%s</b>예요." % (mv(dx, dy), ans))


def pos_how():
    x, y = R.randint(1, 4), R.randint(1, 4)
    dx, dy = R.choice([-1, 1]) * R.randint(1, 4), R.choice([-1, 1]) * R.randint(1, 4)
    tx, ty = x + dx, y + dy
    if not (0 <= tx <= 8 and 0 <= ty <= 8):
        return None
    pts = [("ㄱ", x, y), ("ㄴ", tx, ty)]
    return mcq(gridpts(pts) + "점 ㄱ을 점 ㄴ의 위치로 이동하려면 어떻게 이동해야 하나요?", mv(dx, dy),
               [mv(-dx, dy), mv(dx, -dy), mv(dy, dx) if abs(dx) != abs(dy) else mv(dx + (1 if dx > 0 else -1), dy)],
               "가로로 몇 칸, 세로로 몇 칸 떨어져 있는지 세어요. <b>%s</b>" % mv(dx, dy))


def pos_cm():
    a, b = R.randint(2, 9), R.randint(2, 9)
    d1, d2 = R.choice(["오른쪽", "왼쪽"]), R.choice(["위쪽", "아래쪽"])
    k = R.choice(["dist", "back"])
    if k == "dist":
        return mcq("모눈 한 칸이 1 cm예요. 점을 %s으로 %d cm, %s으로 %d cm 이동했어요. 가로와 세로로 이동한 거리를 합하면 몇 cm인가요?" % (d1, a, d2, b), "%d cm" % (a + b),
                   ["%d cm" % x for x in (abs(a - b) or a + b + 2, a * b, a + b + 1)], "%d + %d = <b>%d cm</b>" % (a, b, a + b))
    op = {"오른쪽": "왼쪽", "왼쪽": "오른쪽", "위쪽": "아래쪽", "아래쪽": "위쪽"}
    ans = "%s으로 %d cm, %s으로 %d cm" % (op[d1], a, op[d2], b)
    return mcq("점을 %s으로 %d cm, %s으로 %d cm 이동했어요. 다시 처음 위치로 돌아가려면 어떻게 이동해야 하나요?" % (d1, a, d2, b), ans,
               ["%s으로 %d cm, %s으로 %d cm" % (d1, a, d2, b), "%s으로 %d cm, %s으로 %d cm" % (op[d1], b, op[d2], a), "%s으로 %d cm, %s으로 %d cm" % (d1, a, op[d2], b)],
               "이동한 방향과 반대 방향으로 같은 거리만큼 움직여요. <b>%s</b>" % ans)


def pos_map():
    places = R.sample(["학교", "도서관", "공원", "우체국", "병원", "문구점", "놀이터", "소방서"], 4)
    coords = []
    while len(coords) < 4:
        p = (R.randint(0, 7), R.randint(0, 7))
        if p not in coords:
            coords.append(p)
    s0 = (R.randint(0, 7), R.randint(0, 7))
    if s0 in coords:
        return None
    i = R.randrange(4)
    dx, dy = coords[i][0] - s0[0], coords[i][1] - s0[1]
    if dx == 0 or dy == 0:
        return None
    pts = [("출발", s0[0], s0[1])] + [(places[j], coords[j][0], coords[j][1]) for j in range(4)]
    return mcq(gridpts(pts) + "출발 점에서 %s 이동하면 어느 곳에 도착하나요?" % mv(dx, dy), places[i], [p for p in places if p != places[i]],
               "출발 점에서 %s 가면 <b>%s</b>에 도착해요." % (mv(dx, dy), places[i]))


# ---------------------------------------------------------------- 삼각형
def tri_kind_angle():
    a, b = R.randint(20, 120), R.randint(20, 120)
    c = 180 - a - b
    if c < 10:
        return None
    big = max(a, b, c)
    ans = "예각삼각형" if big < 90 else ("직각삼각형" if big == 90 else "둔각삼각형")
    return mcq("세 각이 %s, %s, %s인 삼각형은 어떤 삼각형인가요?" % (deg(a), deg(b), deg(c)), ans, [x for x in ("예각삼각형", "직각삼각형", "둔각삼각형", "정삼각형") if x != ans],
               "세 각이 모두 예각이면 예각삼각형, 한 각이 직각이면 직각삼각형, 한 각이 둔각이면 둔각삼각형이에요. <b>%s</b>" % ans)


def tri_two_angles():
    a, b = R.randint(15, 110), R.randint(15, 110)
    c = 180 - a - b
    if c < 10:
        return None
    big = max(a, b, c)
    ans = "예각삼각형" if big < 90 else ("직각삼각형" if big == 90 else "둔각삼각형")
    return mcq("삼각형의 두 각이 %s, %s예요. 이 삼각형은 어떤 삼각형인가요?" % (deg(a), deg(b)), ans, [x for x in ("예각삼각형", "직각삼각형", "둔각삼각형") if x != ans] + ["알 수 없어요"],
               "나머지 한 각은 180° − %s − %s = %s예요. <b>%s</b>" % (deg(a), deg(b), deg(c), ans))


def isosceles_angle():
    k = R.choice(["base", "top"])
    if k == "base":
        t = R.randrange(20, 140, 2)
        b = (180 - t) // 2
        return mcq("이등변삼각형에서 길이가 같은 두 변 사이의 각이 %s예요. 나머지 두 각 중 한 각은 몇 도인가요?" % deg(t), deg(b),
                   [deg(180 - t), deg(t), deg(b + 10), deg(90 - t // 2) if 90 - t // 2 != b else deg(b - 5)],
                   "이등변삼각형은 두 각의 크기가 같아요. (180° − %s) ÷ 2 = <b>%s</b>" % (deg(t), deg(b)))
    b = R.randint(20, 85)
    t = 180 - 2 * b
    return mcq("이등변삼각형의 크기가 같은 두 각 중 한 각이 %s예요. 나머지 한 각은 몇 도인가요?" % deg(b), deg(t),
               [deg(180 - b), deg(b), deg(t + 10) if t + 10 < 180 else deg(t - 10)],
               "크기가 같은 두 각이 %s씩이에요. 180° − %s − %s = <b>%s</b>" % (deg(b), deg(b), deg(b), deg(t)))


def tri_sides():
    k = R.choice(["eq_per", "iso_side", "iso_per", "eq_side"])
    if k == "eq_per":
        s = R.randint(3, 25)
        return mcq("한 변이 %d cm인 정삼각형의 세 변의 길이의 합은 몇 cm인가요?" % s, "%d cm" % (3 * s), ["%d cm" % x for x in (2 * s, 4 * s, s + 3)],
                   "정삼각형은 세 변의 길이가 모두 같아요. %d × 3 = <b>%d cm</b>" % (s, 3 * s))
    if k == "eq_side":
        s = R.randint(3, 25)
        return mcq("세 변의 길이의 합이 %d cm인 정삼각형의 한 변은 몇 cm인가요?" % (3 * s), "%d cm" % s, ["%d cm" % x for x in (3 * s, s * 2, s + 3)],
                   "%d ÷ 3 = <b>%d cm</b>" % (3 * s, s))
    a, b = R.randint(4, 15), R.randint(3, 20)
    if a == b or b >= 2 * a:
        return None
    if k == "iso_per":
        return mcq("길이가 같은 두 변이 각각 %d cm이고, 나머지 한 변이 %d cm인 이등변삼각형의 세 변의 길이의 합은?" % (a, b), "%d cm" % (2 * a + b),
                   ["%d cm" % x for x in (a + 2 * b, a + b, 3 * a)], "%d + %d + %d = <b>%d cm</b>" % (a, a, b, 2 * a + b))
    p = 2 * a + b
    return mcq("세 변의 길이의 합이 %d cm인 이등변삼각형에서 다른 한 변이 %d cm이고, 나머지 두 변의 길이가 같아요. 길이가 같은 한 변은 몇 cm인가요?" % (p, b), "%d cm" % a,
               ["%d cm" % x for x in (p - b, (p - a) // 2 if (p - a) // 2 != a else a + 2, a + 1)], "(%d − %d) ÷ 2 = <b>%d cm</b>" % (p, b, a))


TRI_FACTS = [("정삼각형은 이등변삼각형이라고 할 수 있어요.", "○"), ("이등변삼각형은 모두 정삼각형이에요.", "×"),
             ("정삼각형의 한 각의 크기는 60°예요.", "○"), ("둔각삼각형에는 둔각이 2개 있을 수 있어요.", "×"),
             ("직각삼각형의 나머지 두 각은 모두 예각이에요.", "○"), ("예각삼각형은 세 각이 모두 예각이에요.", "○"),
             ("이등변삼각형은 두 각의 크기가 같아요.", "○"), ("정삼각형은 둔각삼각형이 될 수 있어요.", "×"),
             ("한 각이 예각이면 예각삼각형이에요.", "×"), ("직각이면서 이등변삼각형인 삼각형이 있어요.", "○")]


def tri_fact():
    t, a = R.choice(TRI_FACTS)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "삼각형에 따라 달라요"],
               "정삼각형은 세 변과 세 각(60°)이 같아요. 예각삼각형은 세 각이 모두 예각, 둔각삼각형은 한 각만 둔각이에요.")


# ---------------------------------------------------------------- 수직과 평행
def para_count():
    cases = [("직사각형", 2, 4), ("정사각형", 2, 4), ("평행사변형", 2, 0), ("사다리꼴(평행한 변이 한 쌍)", 1, 0),
             ("마름모", 2, 0), ("정육각형", 3, 0), ("직각삼각형", 0, 1), ("정삼각형", 0, 0), ("정팔각형", 4, 0)]
    nm, p, r = R.choice(cases)
    if R.random() < 0.6:
        return mcq("%s에서 서로 평행한 변은 몇 쌍인가요?" % nm, "%d쌍" % p, ["%d쌍" % x for x in (p + 1, p - 1 if p else 2, p * 2 if p else 3, 4 if p != 4 else 6) if x != p and x >= 0],
                   "평행한 두 직선은 아무리 늘여도 만나지 않아요. %s에서 서로 평행한 변은 <b>%d쌍</b>이에요." % (nm, p))
    if nm in ("평행사변형", "마름모", "사다리꼴(평행한 변이 한 쌍)", "정육각형", "정팔각형", "정삼각형"):
        return None
    return mcq("%s에서 서로 수직인 변은 몇 쌍인가요?" % nm, "%d쌍" % r, ["%d쌍" % x for x in (r + 1, r + 2, r - 1 if r else 3) if x != r and x >= 0],
               "두 변이 만나서 이루는 각이 직각이면 서로 수직이에요. 직각의 수만큼 있어요. <b>%d쌍</b>" % r)


def para_pic():
    k = R.choice(["trap", "para", "rect", "hex", "rtrap"])
    if k == "trap":
        a = R.randint(50, 110); b = R.randint(170, 220); h = R.randint(70, 100); o = R.randint(20, 60)
        pts = [(30 + o, 20), (30 + o + a, 20), (30 + b, 20 + h), (30, 20 + h)]; p, r = 1, 0
    elif k == "rtrap":
        a = R.randint(80, 140); b = R.randint(170, 220); h = R.randint(70, 100)
        pts = [(30, 20), (30 + a, 20), (30 + b, 20 + h), (30, 20 + h)]; p, r = 1, 2
    elif k == "para":
        o = R.randint(30, 60); w = R.randint(120, 160); h = R.randint(70, 100)
        pts = [(30 + o, 20), (30 + o + w, 20), (30 + w, 20 + h), (30, 20 + h)]; p, r = 2, 0
    elif k == "rect":
        w, h = R.randint(120, 200), R.randint(60, 110)
        pts = [(30, 20), (30 + w, 20), (30 + w, 20 + h), (30, 20 + h)]; p, r = 2, 4
    else:
        rr = R.randint(60, 80)
        pts = [(130 + rr * math.cos(math.pi * i / 3), 20 + rr + rr * math.sin(math.pi * i / 3)) for i in range(6)]; p, r = 3, 0
    H = int(max(q[1] for q in pts)) + 30
    rights = {"rect": (0, 1, 2, 3), "rtrap": (0, 3)}.get(k, ())
    f = poly(pts, list(PT[:len(pts)]), right=rights, W=270, H=H)
    if R.random() < 0.6 or r == 0:
        return mcq(f + "이 도형에서 서로 평행한 변은 몇 쌍인가요?", "%d쌍" % p, ["%d쌍" % x for x in (p + 1, p - 1 if p > 1 else 4, p + 2, 0) if x != p],
                   "늘여도 만나지 않는 변끼리 짝을 지어 세어요. <b>%d쌍</b>" % p)
    return mcq(f + "이 도형에서 서로 수직인 변은 몇 쌍인가요? (직각 표시를 보세요)", "%d쌍" % r, ["%d쌍" % x for x in (r + 1, r - 1, r + 2, 0) if x != r and x >= 0],
               "직각 표시가 있는 꼭짓점마다 수직인 변이 한 쌍씩 있어요. <b>%d쌍</b>" % r)


def para_dist():
    k = R.choice(["dist", "angle", "two"])
    if k == "dist":
        a, b = R.randint(2, 12), R.randint(2, 12)
        return mcq("직선 가와 직선 나는 서로 평행하고 그 사이의 거리는 %d cm예요. 직선 나와 직선 다도 평행하고 그 사이의 거리는 %d cm예요. 직선 가와 직선 다 사이의 거리는 몇 cm인가요? (직선 나가 가운데에 있어요)" % (a, b),
                   "%d cm" % (a + b), ["%d cm" % x for x in (abs(a - b) or a + b + 1, a * b, a + b + 2)],
                   "평행선 사이의 거리는 수선의 길이예요. %d + %d = <b>%d cm</b>" % (a, b, a + b))
    if k == "angle":
        a = R.randint(15, 75)
        return mcq("직선 가와 직선 나는 서로 수직이에요. 두 직선이 만나는 점에서 그은 반직선이 직선 가와 %s의 각을 이루며 두 직선 사이에 있어요. 반직선과 직선 나가 이루는 작은 각은 몇 도인가요?" % deg(a),
                   deg(90 - a), [deg(180 - a), deg(a), deg(90 + a)], "수직인 두 직선이 이루는 각은 90°예요. 90° − %s = <b>%s</b>" % (deg(a), deg(90 - a)))
    return mcq("한 직선에 수직인 두 직선은 서로 어떤 관계인가요? (예: 직선 가 ⊥ 직선 다, 직선 나 ⊥ 직선 다, 거리 %d cm)" % R.randint(2, 9), "서로 평행해요",
               ["서로 수직이에요", "한 점에서 만나요", "알 수 없어요"], "한 직선에 수직인 두 직선은 서로 만나지 않아요. <b>서로 평행해요</b>.")


PERP_FACTS = [("두 직선이 만나서 이루는 각이 직각일 때 두 직선은 서로 수직이에요.", "○"), ("평행한 두 직선은 아무리 늘여도 만나지 않아요.", "○"),
              ("평행선 사이의 거리는 어디에서 재어도 같아요.", "○"), ("평행선 사이에 그은 선분 중 가장 짧은 것은 수선이에요.", "○"),
              ("한 점을 지나고 한 직선에 평행한 직선은 셀 수 없이 많이 그을 수 있어요.", "×"), ("수선은 한 직선에 대하여 수직인 직선이에요.", "○"),
              ("서로 수직인 두 직선은 평행해요.", "×"), ("직사각형의 마주 보는 두 변은 서로 수직이에요.", "×")]


def perp_fact():
    t, a = R.choice(PERP_FACTS)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "그림을 보아야 해요"],
               "수직: 만나서 직각을 이룸. 평행: 서로 만나지 않음. 평행선 사이의 거리는 수선의 길이로, 어디서 재어도 같아요.")


def para_fig():
    """두 평행선과 수선의 길이 고르기"""
    d = R.randint(2, 6)
    c = 30
    s = line(20, 30, 300, 30, INK, 3) + line(20, 30 + d * c, 300, 30 + d * c, INK, 3)
    s += text(310, 35, "가", 16, anchor="start") + text(310, 35 + d * c, "나", 16, anchor="start")
    x0 = R.randint(70, 120)
    s += line(x0, 30, x0, 30 + d * c, RED, 2.5) + text(x0 - 6, 22, "ㄱ", 15)
    s += line(x0 + 120, 30, x0 + 60, 30 + d * c, BLUE, 2.5) + text(x0 + 120, 22, "ㄴ", 15)
    f = fig(svg_wrap(340, 60 + d * c, s, "평행선과 선분"))
    return mcq(f + "직선 가와 직선 나는 평행해요. 빨간 선분 ㄱ은 두 직선에 수직이고 길이가 %d cm예요. 파란 선분 ㄴ과 평행선 사이의 거리를 바르게 말한 것은?" % d,
               "평행선 사이의 거리는 %d cm예요" % d, ["평행선 사이의 거리는 파란 선분의 길이예요", "평행선 사이의 거리는 %d cm보다 길어요" % d, "평행선 사이의 거리는 잴 수 없어요"],
               "평행선 사이의 거리는 두 직선에 <b>수직인 선분</b>의 길이예요. 비스듬한 파란 선분은 더 길어요. <b>%d cm</b>" % d)


# ---------------------------------------------------------------- 사각형
QUAD_FACTS = [("정사각형은 마름모라고 할 수 있어요.", "○"), ("마름모는 모두 정사각형이에요.", "×"), ("직사각형은 평행사변형이라고 할 수 있어요.", "○"),
              ("평행사변형은 모두 직사각형이에요.", "×"), ("사다리꼴은 평행한 변이 한 쌍이라도 있는 사각형이에요.", "○"),
              ("평행사변형은 사다리꼴이라고 할 수 있어요.", "○"), ("마름모는 네 변의 길이가 모두 같아요.", "○"),
              ("평행사변형은 마주 보는 두 각의 크기가 같아요.", "○"), ("마름모의 두 대각선은 서로 수직으로 만나요.", "○"),
              ("직사각형의 네 변의 길이는 항상 같아요.", "×"), ("사다리꼴은 모두 평행사변형이에요.", "×"), ("정사각형은 직사각형이면서 마름모예요.", "○")]


def quad_fact():
    t, a = R.choice(QUAD_FACTS)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "모양에 따라 달라요"],
               "사다리꼴 ⊃ 평행사변형 ⊃ 직사각형, 마름모 ⊃ 정사각형이에요. 정사각형은 직사각형이면서 마름모예요.")


def para_angle():
    a = R.randint(40, 140)
    if a == 90:
        return None
    k = R.choice(["adj", "opp", "rh"])
    nm = "평행사변형" if k != "rh" else "마름모"
    if k == "opp":
        return mcq("%s의 한 각이 %s예요. 이 각과 마주 보는 각은 몇 도인가요?" % (nm, deg(a)), deg(a), [deg(180 - a), deg(360 - a), deg(90 - a) if a < 90 else deg(a - 90)],
                   "%s은 마주 보는 두 각의 크기가 같아요. <b>%s</b>" % (nm, deg(a)))
    return mcq("%s의 한 각이 %s예요. 이 각과 이웃한 각은 몇 도인가요?" % (nm, deg(a)), deg(180 - a), [deg(a), deg(360 - a), deg(90 + a) if 90 + a < 180 else deg(a - 90)],
               "%s에서 이웃한 두 각의 크기의 합은 180°예요. 180° − %s = <b>%s</b>" % (nm, deg(a), deg(180 - a)))


def para_side():
    k = R.choice(["para", "rh", "para2"])
    if k == "para":
        a, b = R.randint(4, 15), R.randint(3, 12)
        if a == b:
            return None
        return mcq("평행사변형의 이웃한 두 변이 %d cm, %d cm예요. 네 변의 길이의 합은 몇 cm인가요?" % (a, b), "%d cm" % (2 * (a + b)), ["%d cm" % x for x in (a + b, a * b, 4 * a)],
                   "마주 보는 두 변의 길이가 같아요. (%d + %d) × 2 = <b>%d cm</b>" % (a, b, 2 * (a + b)))
    if k == "rh":
        s = R.randint(3, 20)
        return mcq("마름모의 네 변의 길이의 합이 %d cm예요. 한 변은 몇 cm인가요?" % (4 * s), "%d cm" % s, ["%d cm" % x for x in (2 * s, 4 * s, s + 4)],
                   "마름모는 네 변의 길이가 모두 같아요. %d ÷ 4 = <b>%d cm</b>" % (4 * s, s))
    a, p = R.randint(4, 15), None
    b = R.randint(3, 12)
    if a == b:
        return None
    p = 2 * (a + b)
    return mcq("평행사변형의 네 변의 길이의 합이 %d cm이고 한 변이 %d cm예요. 이 변과 이웃한 변은 몇 cm인가요?" % (p, a), "%d cm" % b,
               ["%d cm" % x for x in (p - a, p // 2, p - 2 * a)], "(%d − %d × 2) ÷ 2 = <b>%d cm</b>" % (p, a, b))


def quad_name():
    cases = [("마주 보는 두 쌍의 변이 서로 평행하고 네 변의 길이가 모두 같으며 네 각이 모두 직각인 사각형", "정사각형"),
             ("평행한 변이 한 쌍만 있는 사각형", "사다리꼴"), ("네 변의 길이가 모두 같지만 네 각이 직각이 아닌 사각형", "마름모"),
             ("마주 보는 두 쌍의 변이 서로 평행하지만 네 각이 직각이 아니고 이웃한 변의 길이가 다른 사각형", "평행사변형"),
             ("네 각이 모두 직각이지만 네 변의 길이가 모두 같지는 않은 사각형", "직사각형")]
    d, a = R.choice(cases)
    return mcq("%s의 이름으로 가장 알맞은 것은?" % d, a,
               [x for x in ("사다리꼴", "평행사변형", "마름모", "직사각형", "정사각형") if x != a], "<b>%s</b>%s." % (a, josa(a, "이에요/예요")[len(a):]))


def quad_pic():
    k = R.choice(["trap", "para", "rh", "rect", "sq"])
    if k == "trap":
        a = R.randint(40, 120); b = R.randint(160, 230); h = R.randint(70, 110)
        pts = [(30 + a // 3, 20), (30 + a // 3 + a, 20), (30 + b, 20 + h), (30, 20 + h)]
        ans = "사다리꼴"
    elif k == "para":
        s = R.randint(30, 60); w = R.randint(120, 160); h = R.randint(70, 100)
        pts = [(30 + s, 20), (30 + s + w, 20), (30 + w, 20 + h), (30, 20 + h)]
        ans = "평행사변형"
    elif k == "rh":
        w = R.randint(70, 100); h = R.randint(50, 80)
        pts = [(130, 15), (130 + w, 15 + h), (130, 15 + 2 * h), (130 - w, 15 + h)]
        ans = "마름모"
    elif k == "rect":
        w, h = R.randint(130, 200), R.randint(60, 100)
        pts = [(30, 20), (30 + w, 20), (30 + w, 20 + h), (30, 20 + h)]
        ans = "직사각형"
    else:
        w = R.randint(80, 120)
        pts = [(60, 15), (60 + w, 15), (60 + w, 15 + w), (60, 15 + w)]
        ans = "정사각형"
    H = max(p[1] for p in pts) + 30
    f = poly(pts, R.sample(PT, 4), right=(0, 1, 2, 3) if k in ("rect", "sq") else (), W=270, H=H)
    ticks = " (네 변의 길이가 모두 같아요)" if k in ("rh", "sq") else ""
    return mcq(f + "이 사각형의 이름으로 <b>가장</b> 알맞은 것은?%s" % ticks, ans, [x for x in ("사다리꼴", "평행사변형", "마름모", "직사각형", "정사각형") if x != ans],
               "평행한 변의 수, 변의 길이, 직각인지를 차례로 확인해요. <b>%s</b>" % ans)


# ---------------------------------------------------------------- 다각형
PNAME = {3: "삼각형", 4: "사각형", 5: "오각형", 6: "육각형", 7: "칠각형", 8: "팔각형", 9: "구각형", 10: "십각형", 12: "십이각형"}


def poly_name():
    n = R.choice([5, 6, 7, 8, 9, 10])
    rr = 80
    pts = [(110 + rr * math.cos(2 * math.pi * i / n - math.pi / 2) * R.uniform(0.75, 1.0), 100 + rr * math.sin(2 * math.pi * i / n - math.pi / 2) * R.uniform(0.75, 1.0)) for i in range(n)]
    f = poly(pts, W=220, H=200)
    return mcq(f + "이 다각형의 이름은? (변을 세어 보세요)", PNAME[n], [PNAME[x] for x in (n - 1, n + 1 if n + 1 in PNAME else n - 2, n + 2 if n + 2 in PNAME else n - 3)],
               "변이 %d개인 다각형은 <b>%s</b>이에요." % (n, PNAME[n]))


def regular():
    n = R.choice([3, 4, 5, 6, 8, 10])
    s = R.randint(2, 15)
    k = R.choice(["per", "side"])
    nm = "정" + PNAME[n]
    if k == "per":
        return mcq("한 변이 %d cm인 %s의 모든 변의 길이의 합은 몇 cm인가요?" % (s, nm), "%d cm" % (n * s), ["%d cm" % x for x in ((n - 1) * s, (n + 1) * s, n + s)],
                   "%s은 변이 %d개이고 길이가 모두 같아요. %d × %d = <b>%d cm</b>" % (nm, n, s, n, n * s))
    return mcq("모든 변의 길이의 합이 %d cm인 %s의 한 변은 몇 cm인가요?" % (n * s, nm), "%d cm" % s, ["%d cm" % x for x in (n * s // (n - 1) if n * s % (n - 1) == 0 else s + 1, s * 2, n)],
               "%d ÷ %d = <b>%d cm</b>" % (n * s, n, s))


def diagonals():
    n = R.choice([4, 5, 6, 7, 8, 9, 10])
    d = n * (n - 3) // 2
    k = R.choice(["all", "one", "rev"])
    if k == "one":
        return mcq("%s의 한 꼭짓점에서 그을 수 있는 대각선은 몇 개인가요?" % PNAME[n], "%d개" % (n - 3), ["%d개" % x for x in (n - 1, n - 2, n, d) if x != n - 3],
                   "자기 자신과 이웃한 두 꼭짓점을 빼면 %d − 3 = <b>%d개</b>예요." % (n, n - 3))
    if k == "rev":
        return mcq("대각선이 모두 %d개인 다각형은 무엇인가요?" % d, PNAME[n], [PNAME[x] for x in (n - 1, n + 1 if n + 1 in PNAME else n - 2, n + 2 if n + 2 in PNAME else n - 3)],
                   "%s은 한 꼭짓점에서 %d개씩, %d × %d ÷ 2 = %d개예요. <b>%s</b>" % (PNAME[n], n - 3, n, n - 3, d, PNAME[n]))
    return mcq("%s의 대각선은 모두 몇 개인가요?" % PNAME[n], "%d개" % d, ["%d개" % x for x in (n * (n - 3), n - 3, n, d + 1) if x != d],
               "한 꼭짓점에서 이웃하지 않는 꼭짓점 %d개로 대각선을 그을 수 있어요. 겹치는 것을 빼면 %d × %d ÷ 2 = <b>%d개</b>" % (n - 3, n, n - 3, d))


POLY_FACTS = [("정다각형은 변의 길이가 모두 같고 각의 크기가 모두 같아요.", "○"), ("마름모는 정다각형이에요.", "×"), ("직사각형은 정다각형이에요.", "×"),
              ("정사각형은 정다각형이에요.", "○"), ("삼각형에는 대각선이 없어요.", "○"), ("원도 다각형이에요.", "×"),
              ("다각형은 선분으로만 둘러싸인 도형이에요.", "○"), ("사각형의 대각선은 2개예요.", "○"),
              ("정사각형의 두 대각선은 길이가 같고 서로 수직으로 만나요.", "○"), ("직사각형의 두 대각선은 항상 수직으로 만나요.", "×")]


def poly_fact():
    t, a = R.choice(POLY_FACTS)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "도형에 따라 달라요"],
               "다각형은 선분으로만 둘러싸인 도형, 정다각형은 변의 길이와 각의 크기가 모두 같은 다각형이에요.")


def fill_shapes():
    cases = [("정육각형", "", "정삼각형", "", 6), ("정육각형", "", "마름모", "정삼각형 2개", 3), ("정육각형", "", "사다리꼴", "정삼각형 3개", 2),
             ("사다리꼴", "정삼각형 3개", "정삼각형", "", 3), ("평행사변형", "정삼각형 2개", "정삼각형", "", 2), ("큰 정삼각형", "한 변이 작은 정삼각형 2개", "작은 정삼각형", "", 4),
             ("큰 정삼각형", "한 변이 작은 정삼각형 3개", "작은 정삼각형", "", 9), ("직사각형", "정사각형 2개", "직각삼각형", "정사각형의 반", 4),
             ("정사각형", "", "직각삼각형", "정사각형의 반", 2), ("큰 정사각형", "한 변이 작은 정사각형 3개", "작은 정사각형", "", 9)]
    big, bd, small, sd, n = R.choice(cases)
    J = lambda w, d, pair: josa(w, pair) if not d else "%s(%s)%s" % (w, d, josa(w, pair)[len(w):])
    return mcq("%s %s 빈틈없이 채우려면 %s 몇 개 필요한가요?" % (J(big, bd, "을/를"), J(small, sd, "으로/로"), josa(small, "이/가")), "%d개" % n,
               ["%d개" % x for x in (n + 1, n - 1 if n > 1 else n + 2, n * 2) if x != n],
               "작은 도형을 큰 도형 안에 겹치지 않게 놓아 세어요. <b>%d개</b>" % n)


def build(which):
    G = "grade-4"
    if which == "angles":
        return unit(G, "measuring-angles", 3, "[4수03-02] [4수03-24]",
                    "각과 직각을 이해하고, 직각과 비교하는 활동을 통하여 예각과 둔각을 구별할 수 있다. 각의 크기의 단위인 1도(°)를 알고, 각도기를 이용하여 각의 크기를 측정하고 어림할 수 있다.",
                    "각도와 각도기, 예각과 둔각", "각도",
                    "초등 4학년 각도 학습지: 각도기로 각 재기(안쪽 눈금과 바깥쪽 눈금), 예각, 직각, 둔각 구별, 각도 어림하기, 시계의 각, 각도의 합과 차까지 100문제와 정답.",
                    "0에 맞춘 쪽의 눈금을 읽어요", "직각보다 작으면 예각, 크면 둔각",
                    ["직각을 똑같이 90으로 나눈 하나를 <b>1도(1°)</b>라고 해요. 직각은 90°예요.",
                     "각도기의 중심을 꼭짓점에, 밑금을 한 변에 맞추고, <b>0에서 시작하는 눈금</b>을 따라 읽어요. 오른쪽 0이면 안쪽 눈금, 왼쪽 0이면 바깥쪽 눈금이에요.",
                     "0°보다 크고 직각보다 작은 각은 <b>예각</b>, 직각보다 크고 180°보다 작은 각은 <b>둔각</b>이에요.",
                     "각도의 합과 차는 자연수처럼 계산하고 °를 붙여요."],
                    [("4시에 긴바늘과 짧은바늘이 이루는 작은 각은?", ["숫자 한 칸은 30°", "4칸이니까 30° × 4 = 120°"], "120°, 둔각")],
                    [("바깥쪽과 안쪽 눈금을 바꾸어 읽는다", "한 변이 맞춰진 0에서 시작하는 눈금을 읽어요. 50°와 130°를 헷갈리지 않게 예각인지 먼저 봐요."),
                     ("변이 길면 각도도 크다고 생각한다", "각의 크기는 두 변이 벌어진 정도예요."),
                     ("90°도 예각이라고 한다", "90°는 직각이에요. 예각은 90°보다 작아요.")],
                    [("각도기 읽는 법이 헷갈려요.", "먼저 각이 예각인지 둔각인지 보세요. 예각인데 120°로 읽었다면 반대쪽 눈금을 읽은 거예요."),
                     ("각도는 몇 학년에서 배우나요?", "초등 4학년 1학기 「각도」 단원에서 각도기와 예각, 둔각, 삼각형과 사각형의 각의 합을 배워요.")],
                    [("각도기로 재기", [(protractor, 20)]),
                     ("예각, 직각, 둔각", [(classify, 20)]),
                     ("각도 어림하기", [(estimate, 10), (protractor, 10)]),
                     ("시계와 각", [(clock_angle, 10), (classify, 10)]),
                     ("각도의 합과 차", [(add_sub, 14), (two_set_squares, 6)])], 82403)
    if which == "anglesum":
        return unit(G, "angle-sums-of-triangles-and-quadrilaterals", 4, "[4수03-25]",
                    "여러 가지 방법으로 삼각형과 사각형의 내각의 크기의 합을 추론하고, 자신의 추론 과정을 설명할 수 있다.",
                    "삼각형과 사각형의 각의 크기의 합", "삼각형・사각형의 각의 합",
                    "초등 4학년 각도 학습지: 삼각형의 세 각의 합 180°, 사각형의 네 각의 합 360°, 모르는 각 구하기, 직선의 각, 삼각자의 각, 각도의 합과 차까지 100문제와 정답.",
                    "삼각형 180°, 사각형 360°", "사각형은 삼각형 2개로 나눌 수 있어요.",
                    ["삼각형의 세 각을 잘라 붙이면 직선이 돼요. <b>삼각형의 세 각의 크기의 합은 180°</b>예요.",
                     "사각형은 대각선으로 삼각형 2개로 나눌 수 있어요. <b>사각형의 네 각의 크기의 합은 360°</b>예요.",
                     "모르는 각은 합에서 아는 각을 빼서 구해요.",
                     "직선이 이루는 각은 180°예요."],
                    [("삼각형의 두 각이 55°, 70°일 때 나머지 한 각은?", ["180° − 55° − 70° = 55°"], "55°"),
                     ("사각형의 세 각이 80°, 100°, 75°일 때 나머지 한 각은?", ["360° − 80° − 100° − 75° = 105°"], "105°")],
                    [("사각형의 각의 합을 180°로 계산한다", "사각형은 삼각형 2개이므로 360°예요."),
                     ("두 각을 더한 값을 답으로 쓴다", "합에서 아는 각을 빼야 해요."),
                     ("삼각형이 크면 각의 합도 크다고 생각한다", "크기와 상관없이 항상 180°예요.")],
                    [("삼각형의 각의 합이 왜 180°인가요?", "세 각을 잘라서 꼭짓점을 한 점에 모으면 일직선이 되기 때문이에요."),
                     ("오각형의 각의 합도 구할 수 있나요?", "오각형은 삼각형 3개로 나눌 수 있어서 540°예요. 다각형의 각의 합은 5학년 이후에 더 배워요.")],
                    [("각도의 합과 차", [(add_sub, 14), (two_set_squares, 6)]),
                     ("삼각형의 나머지 각", [(tri_missing, 20)]),
                     ("사각형의 나머지 각", [(quad_missing, 20)]),
                     ("직선과 각", [(straight, 20)]),
                     ("섞어서 연습", [(tri_missing, 8), (quad_missing, 8), (straight, 4)])], 82404)
    if which == "move":
        return unit(G, "sliding-flipping-and-turning-shapes", 7, "[4수03-04]",
                    "구체물이나 평면도형의 밀기, 뒤집기, 돌리기 활동을 통하여 그 변화를 이해한다.",
                    "평면도형의 이동: 밀기, 뒤집기, 돌리기", "밀기, 뒤집기, 돌리기",
                    "초등 4학년 평면도형의 이동 학습지: 밀기, 오른쪽・위쪽으로 뒤집기, 90°・180° 돌리기 한 모양 찾기, 숫자 카드 돌리기까지 100문제와 정답.",
                    "밀기는 그대로, 뒤집기는 거울, 돌리기는 회전", "시계 방향 270° = 시계 반대 방향 90°",
                    ["<b>밀기</b>: 도형을 어느 방향으로 밀어도 모양과 방향은 그대로이고 위치만 바뀌어요.",
                     "<b>뒤집기</b>: 오른쪽(왼쪽)으로 뒤집으면 왼쪽과 오른쪽이, 위쪽(아래쪽)으로 뒤집으면 위쪽과 아래쪽이 바뀌어요.",
                     "<b>돌리기</b>: 시계 방향으로 90° 돌리면 위쪽이 오른쪽으로 가요. 360° 돌리면 처음 모양이에요.",
                     "같은 방향으로 2번 뒤집으면 처음 모양이 돼요."],
                    [("시계 방향으로 90°만큼 3번 돌리면?", ["90° × 3 = 270°", "시계 반대 방향으로 90° 돌린 것과 같아요."], "시계 반대 방향으로 90° 돌린 모양")],
                    [("오른쪽으로 뒤집기와 시계 방향 90° 돌리기를 헷갈린다", "뒤집기는 거울에 비친 모양, 돌리기는 바퀴처럼 도는 모양이에요."),
                     ("밀기를 하면 모양이 바뀐다고 생각한다", "밀기는 위치만 바뀌어요."),
                     ("180° 돌리기를 위쪽으로 뒤집기와 같다고 생각한다", "180° 돌리면 위아래와 왼쪽 오른쪽이 모두 바뀌어요.")],
                    [("평면도형의 이동은 언제 배우나요?", "초등 4학년 1학기 「평면도형의 이동」 단원에서 배워요."),
                     ("집에서 연습하는 방법은?", "글자나 숫자를 쓴 투명 종이를 직접 밀고, 뒤집고, 돌려 보세요.")],
                    [("밀기와 뒤집기", [(move_pick(["slide", "flipH", "flipV"]), 20)]),
                     ("돌리기", [(move_pick(["r90", "r180", "r270"]), 20)]),
                     ("여러 가지 이동", [(move_pick(["flipH", "flipV", "r90", "r180", "r270"]), 20)]),
                     ("이동의 성질", [(move_fact, 12), (move_card, 8)]),
                     ("섞어서 연습", [(move_pick(["flipH", "r90", "r180", "flipV", "r270", "slide"]), 14), (move_card, 6)])], 82407)
    if which == "position":
        return unit(G, "position-and-direction", 8, "[4수03-05]",
                    "평면에서 점의 이동에 대해 위치와 방향을 이용하여 설명할 수 있다.",
                    "평면에서 점의 이동: 위치와 방향", "위치와 방향",
                    "초등 4학년 학습지: 모눈 위에서 점을 오른쪽, 왼쪽, 위쪽, 아래쪽으로 몇 칸 이동하기, 이동 방법 설명하기, 지도에서 길 찾기까지 100문제와 정답.",
                    "방향과 거리로 이동을 말해요", "오른쪽으로 3칸, 위쪽으로 2칸",
                    ["평면에서 점의 이동은 <b>방향</b>(오른쪽, 왼쪽, 위쪽, 아래쪽)과 <b>거리</b>(몇 칸, 몇 cm)로 설명해요.",
                     "가로 방향과 세로 방향으로 나누어 차례로 세어요.",
                     "처음 위치로 돌아가려면 반대 방향으로 같은 거리만큼 이동해요."],
                    [("점 ㄱ에서 점 ㄴ으로 가려면?", ["가로: 오른쪽으로 4칸", "세로: 아래쪽으로 2칸"], "오른쪽으로 4칸, 아래쪽으로 2칸")],
                    [("오른쪽과 왼쪽을 바꾸어 말한다", "그림을 보는 사람 기준으로 오른쪽, 왼쪽을 말해요."),
                     ("점이 아닌 칸을 센다", "점이 움직인 눈금의 칸 수를 세요."),
                     ("가로와 세로 칸 수를 바꾼다", "가로 → 세로 순서로 나누어 세요.")],
                    [("이 단원은 언제 배우나요?", "2022 개정 교육과정에서 새로 들어온 내용으로, 초등 4학년에서 평면에서 점의 이동을 위치와 방향으로 설명해요."),
                     ("좌표를 배우는 건가요?", "4학년에서는 방향과 거리로 설명해요. 좌표평면은 중학교에서 배워요.")],
                    [("이동한 위치 찾기", [(pos_where, 20)]),
                     ("이동 방법 설명하기", [(pos_how, 20)]),
                     ("지도에서 이동하기", [(pos_map, 20)]),
                     ("거리와 되돌아가기", [(pos_cm, 20)]),
                     ("섞어서 연습", [(pos_where, 7), (pos_how, 7), (pos_map, 6)])], 82408)
    if which == "triangles":
        return unit(G, "triangles", 14, "[4수03-08] [4수03-09]",
                    "여러 가지 모양의 삼각형에 대한 분류 활동을 통하여 이등변삼각형, 정삼각형을 이해하고, 그 성질을 탐구하고 설명할 수 있다. 여러 가지 모양의 삼각형에 대한 분류 활동을 통하여 직각삼각형, 예각삼각형, 둔각삼각형을 이해한다.",
                    "이등변삼각형, 정삼각형, 예각・둔각삼각형", "삼각형",
                    "초등 4학년 2학기 삼각형 학습지: 이등변삼각형과 정삼각형의 성질, 변의 길이와 각의 크기, 예각삼각형・직각삼각형・둔각삼각형 분류까지 100문제와 정답.",
                    "변으로 한 번, 각으로 한 번 분류", "정삼각형의 세 각은 모두 60°",
                    ["두 변의 길이가 같은 삼각형은 <b>이등변삼각형</b>이에요. 길이가 같은 두 변과 함께 있는 두 각의 크기도 같아요.",
                     "세 변의 길이가 같은 삼각형은 <b>정삼각형</b>이에요. 세 각은 모두 60°예요. 정삼각형은 이등변삼각형이라고 할 수 있어요.",
                     "세 각이 모두 예각이면 <b>예각삼각형</b>, 한 각이 둔각이면 <b>둔각삼각형</b>, 한 각이 직각이면 <b>직각삼각형</b>이에요."],
                    [("이등변삼각형에서 크기가 같은 두 각이 각각 50°일 때 나머지 한 각은?", ["180° − 50° − 50° = 80°"], "80°"),
                     ("세 각이 40°, 35°, 105°인 삼각형은?", ["105°는 둔각"], "둔각삼각형")],
                    [("한 각이 예각이면 예각삼각형이라고 한다", "세 각이 모두 예각이어야 예각삼각형이에요."),
                     ("이등변삼각형은 정삼각형이라고 한다", "정삼각형이 이등변삼각형인 것이지, 거꾸로는 아니에요."),
                     ("두 각만 보고 분류한다", "나머지 각을 구해서 가장 큰 각을 확인해요.")],
                    [("삼각형은 몇 가지로 분류하나요?", "변의 길이로 이등변삼각형・정삼각형, 각의 크기로 예각・직각・둔각삼각형으로 분류해요."),
                     ("이등변삼각형이면서 직각삼각형인 것도 있나요?", "네. 두 각이 45°이고 한 각이 90°인 직각이등변삼각형이 있어요.")],
                    [("이등변삼각형의 각", [(isosceles_angle, 20)]),
                     ("변의 길이", [(tri_sides, 20)]),
                     ("각으로 분류하기", [(tri_kind_angle, 20)]),
                     ("두 각으로 알아보기", [(tri_two_angles, 20)]),
                     ("삼각형의 성질 ○×", [(tri_fact, 10), (isosceles_angle, 5), (tri_sides, 5)])], 82414)
    if which == "parallel":
        return unit(G, "perpendicular-and-parallel-lines", 17, "[4수03-03]",
                    "직선의 수직 관계와 평행 관계를 이해한다.",
                    "수직과 평행, 평행선 사이의 거리", "수직과 평행",
                    "초등 4학년 2학기 학습지: 수직과 수선, 평행과 평행선, 평행선 사이의 거리, 도형에서 평행한 변과 수직인 변 찾기까지 100문제와 정답.",
                    "만나서 직각이면 수직, 만나지 않으면 평행", "평행선 사이의 거리는 수선의 길이",
                    ["두 직선이 만나서 이루는 각이 직각일 때 두 직선은 서로 <b>수직</b>이라고 하고, 한 직선을 다른 직선에 대한 <b>수선</b>이라고 해요.",
                     "서로 만나지 않는 두 직선을 <b>평행</b>하다고 하고, 평행한 두 직선을 <b>평행선</b>이라고 해요.",
                     "평행선의 한 직선에서 다른 직선에 그은 수선의 길이를 <b>평행선 사이의 거리</b>라고 해요. 어디서 재어도 같아요."],
                    [("직사각형에서 서로 평행한 변은 몇 쌍인가요?", ["마주 보는 변끼리 평행해요."], "2쌍")],
                    [("비스듬한 선분의 길이를 평행선 사이의 거리라고 한다", "수직인 선분의 길이가 거리예요."),
                     ("수직인 두 직선이 평행하다고 한다", "수직은 만나고, 평행은 만나지 않아요."),
                     ("그림에서 짧게 그려진 직선은 만나지 않으니 평행하다고 한다", "직선을 늘였을 때 만나는지 생각해요.")],
                    [("수직과 평행은 언제 배우나요?", "초등 4학년 2학기 「수직과 평행」(사각형) 단원에서 배워요."),
                     ("평행선을 어떻게 그리나요?", "삼각자 두 개를 이용해 한 삼각자를 다른 삼각자에 대고 밀면서 그려요.")],
                    [("수직과 평행의 뜻", [(perp_fact, 8), (para_fig, 12)]),
                     ("도형에서 찾기", [(para_count, 8), (para_pic, 12)]),
                     ("평행선 사이의 거리", [(para_dist, 20)]),
                     ("수선과 각", [(para_dist, 10), (para_fig, 10)]),
                     ("섞어서 연습", [(para_pic, 10), (para_dist, 10)])], 82417)
    if which == "quads":
        return unit(G, "quadrilaterals", 18, "[4수03-10]",
                    "여러 가지 모양의 사각형에 대한 분류 활동을 통하여 직사각형, 정사각형, 사다리꼴, 평행사변형, 마름모를 이해하고, 그 성질을 탐구하고 설명할 수 있다.",
                    "사다리꼴, 평행사변형, 마름모", "여러 가지 사각형",
                    "초등 4학년 2학기 사각형 학습지: 사다리꼴, 평행사변형, 마름모, 직사각형, 정사각형의 뜻과 성질, 사각형 사이의 관계, 각과 변의 길이 구하기까지 100문제와 정답.",
                    "평행한 변, 변의 길이, 직각으로 구별", "정사각형은 직사각형이면서 마름모예요.",
                    ["평행한 변이 한 쌍이라도 있는 사각형은 <b>사다리꼴</b>이에요.",
                     "마주 보는 두 쌍의 변이 서로 평행한 사각형은 <b>평행사변형</b>이에요. 마주 보는 변의 길이와 마주 보는 각의 크기가 같고, 이웃한 두 각의 합은 180°예요.",
                     "네 변의 길이가 모두 같은 사각형은 <b>마름모</b>예요.",
                     "정사각형은 사다리꼴, 평행사변형, 마름모, 직사각형의 성질을 모두 가져요."],
                    [("평행사변형의 한 각이 65°일 때 이웃한 각은?", ["이웃한 두 각의 합은 180°", "180° − 65° = 115°"], "115°")],
                    [("마름모를 모두 정사각형이라고 한다", "마름모는 네 각이 직각이 아닐 수 있어요."),
                     ("평행사변형에서 이웃한 각이 같다고 생각한다", "마주 보는 각이 같고, 이웃한 각은 합이 180°예요."),
                     ("사다리꼴은 평행한 변이 꼭 한 쌍이어야 한다고 생각한다", "한 쌍 이상이면 사다리꼴이라서 평행사변형도 사다리꼴이에요.")],
                    [("사각형 사이의 관계를 쉽게 기억하는 방법은?", "사다리꼴 → 평행사변형 → 직사각형・마름모 → 정사각형 순서로 조건이 늘어난다고 생각하세요."),
                     ("정사각형은 왜 마름모인가요?", "네 변의 길이가 모두 같기 때문이에요.")],
                    [("사각형의 이름", [(quad_pic, 20)]),
                     ("뜻으로 알아보기", [(quad_name, 5), (quad_fact, 12), (quad_pic, 3)]),
                     ("평행사변형과 마름모의 각", [(para_angle, 20)]),
                     ("변의 길이", [(para_side, 20)]),
                     ("섞어서 연습", [(para_angle, 8), (para_side, 8), (quad_pic, 4)])], 82418)
    return unit(G, "polygons", 20, "[4수03-11] [4수03-12]",
                "다각형과 정다각형을 이해한다. 주어진 도형을 이용하여 여러 가지 모양을 만들거나 채우고 설명할 수 있다.",
                "다각형, 정다각형, 대각선", "다각형",
                "초등 4학년 2학기 다각형 학습지: 다각형의 이름, 정다각형의 변의 길이, 대각선의 수, 다각형의 성질, 모양 만들기와 채우기까지 100문제와 정답.",
                "선분으로만 둘러싸인 도형이 다각형", "변의 길이와 각의 크기가 모두 같으면 정다각형",
                ["선분으로만 둘러싸인 도형을 <b>다각형</b>이라고 하고, 변의 수에 따라 오각형, 육각형, …이라고 불러요.",
                 "변의 길이가 모두 같고 각의 크기가 모두 같은 다각형은 <b>정다각형</b>이에요.",
                 "서로 이웃하지 않는 두 꼭짓점을 이은 선분을 <b>대각선</b>이라고 해요. 삼각형에는 대각선이 없어요.",
                 "여러 도형을 겹치지 않게 이어 붙여 다른 모양을 만들거나 채울 수 있어요."],
                [("육각형의 대각선은 몇 개?", ["한 꼭짓점에서 3개", "6 × 3 ÷ 2 = 9"], "9개"),
                 ("한 변이 5 cm인 정팔각형의 모든 변의 길이의 합은?", ["5 × 8 = 40"], "40 cm")],
                [("대각선을 셀 때 같은 선분을 두 번 센다", "꼭짓점마다 센 수를 2로 나눠요."),
                 ("직사각형을 정다각형이라고 한다", "직사각형은 변의 길이가 모두 같지 않을 수 있어요."),
                 ("원을 다각형이라고 한다", "다각형은 선분으로만 둘러싸여야 해요.")],
                [("다각형은 언제 배우나요?", "초등 4학년 2학기 「다각형」 단원에서 다각형, 정다각형, 대각선을 배워요."),
                 ("대각선의 수를 빨리 구하는 방법은?", "(꼭짓점의 수) × (꼭짓점의 수 − 3) ÷ 2로 구할 수 있어요.")],
                [("다각형의 이름", [(poly_name, 20)]),
                 ("정다각형", [(regular, 20)]),
                 ("대각선", [(diagonals, 10), (poly_fact, 10)]),
                 ("모양 만들기와 채우기", [(fill_shapes, 10), (regular, 10)]),
                 ("섞어서 연습", [(diagonals, 4), (regular, 8), (poly_name, 8)])], 82420)
