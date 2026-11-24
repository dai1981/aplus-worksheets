# -*- coding: utf-8 -*-
"""
대한민국 초등 2학년 수학：도형과 규칙（2022 개정）の 3 単元
  shapes : 여러 가지 도형（삼각형・사각형・원・오각형・육각형、변과 꼭짓점）[2수03-03] [2수03-04] [2수03-05]  2-1
  cubes  : 쌓기나무（개수、층、위치와 방향）[2수03-02]                                                       2-1
  pattern: 규칙 찾기（무늬・쌓은 모양・덧셈표・곱셈표・생활）[2수02-01] [2수02-02]                              2-2
誤答は「곧은 선이 열려 있거나 굽은 선이 있어도 삼각형이라고 한다」「꼭짓점과 변의 수를 하나 더 / 덜 센다」
「원에도 꼭짓점이 있다고 한다」「보는 사람의 오른쪽과 쌓기나무의 오른쪽을 헷갈린다」「규칙의 반복 부분을 짧게 잡는다」から作る。
"""
import math
import random
from kr_common import mcq, unit, Names, josa
from kr_low import ko, LET, fig, cards
from kr_pics import poly
import k_pics as K
from f_common import pattern_svg
from ws_common import svg_wrap, text, INK, GREEN, RED, FILL

R = random.Random(82202)
NM = Names(R)
G = "grade-2"
PN = {3: "삼각형", 4: "사각형", 5: "오각형", 6: "육각형"}
FILLS = ["#f4c430", "#7fb3e6", "#f4a3a3", "#9fd3a7"]


def rand_poly(n, cx, cy, r, jit=0.14, rot=None, reg=False):
    rot = R.uniform(0, 2 * math.pi) if rot is None else rot
    while True:
        angs = sorted((rot + 2 * math.pi * i / n + (0 if reg else R.uniform(-jit, jit))) for i in range(n))
        rs = [r * (1 if reg else R.uniform(0.82, 1.0)) for _ in range(n)]
        pts = [(cx + rr * math.cos(a), cy + rr * math.sin(a)) for a, rr in zip(angs, rs)]
        ok = True
        for i in range(n):          # 볼록이고、꼭짓점마다 30도 이상 꺾이도록（변의 수를 셀 수 있게）
            ax, ay = pts[i]; bx, by = pts[(i + 1) % n]; cx2, cy2 = pts[(i + 2) % n]
            cr = (bx - ax) * (cy2 - by) - (by - ay) * (cx2 - bx)
            dt = (bx - ax) * (cx2 - bx) + (by - ay) * (cy2 - by)
            if cr <= 0 or math.degrees(math.atan2(cr, dt)) < 35:
                ok = False
        if ok:
            return pts


def shape_el(kind, cx, cy, r, col, reg=False):
    """kind: 3〜6（다각형）, 'circle', 'open3'（열린 삼각형）, 'curve3'（한 변이 굽은 도형）, 'oval'"""
    st = "fill='%s' stroke='%s' stroke-width='2.4'" % (col, INK)
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' %s/>" % (cx, cy, r * 0.85, st)
    if kind == "oval":
        return "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' %s/>" % (cx, cy, r, r * 0.55, st)
    if kind == "open3":
        p = rand_poly(3, cx, cy, r)
        g = (p[2][0] + (p[0][0] - p[2][0]) * 0.7, p[2][1] + (p[0][1] - p[2][1]) * 0.7)
        return "<polyline points='%s' fill='none' stroke='%s' stroke-width='2.6'/>" % (" ".join("%.1f,%.1f" % q for q in [p[0], p[1], p[2], g]), INK)
    if kind == "curve3":
        p = rand_poly(3, cx, cy, r)
        mx, my = (p[0][0] + p[1][0]) / 2, (p[0][1] + p[1][1]) / 2
        ox, oy = mx + (mx - cx) * 0.6, my + (my - cy) * 0.6
        return "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Z' %s/>" % (p[0][0], p[0][1], ox, oy, p[1][0], p[1][1], p[2][0], p[2][1], st)
    if kind == "curve4":
        p = rand_poly(4, cx, cy, r)
        mx, my = (p[0][0] + p[1][0]) / 2, (p[0][1] + p[1][1]) / 2
        ox, oy = mx + (mx - cx) * 0.6, my + (my - cy) * 0.6
        return "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f L%.1f %.1f Z' %s/>" % (p[0][0], p[0][1], ox, oy, p[1][0], p[1][1], p[2][0], p[2][1], p[3][0], p[3][1], st)
    p = rand_poly(kind, cx, cy, r, reg=reg)
    return "<polygon points='%s' %s/>" % (" ".join("%.1f,%.1f" % q for q in p), st)


def one(kind, col=None, r=58):
    W = int(2 * r + 40)
    return ko(svg_wrap(W, W, shape_el(kind, W / 2, W / 2, r, col or R.choice(FILLS)), "도형"), "도형")


def lettered(kinds, r=36):
    sp = 2 * r + 30
    s = []
    for i, k in enumerate(kinds):
        cx = 15 + sp / 2 + i * sp
        s.append(shape_el(k, cx, r + 14, r, FILLS[i % 4]))
        s.append(text(cx, 2 * r + 46, LET[i], 18, col=GREEN))
    return ko(svg_wrap(int(30 + sp * len(kinds)), 2 * r + 56, "".join(s), "도형 가부터 %s까지" % LET[len(kinds) - 1]), "도형")


# ------------------------------------------------------------------ 여러 가지 도형
def sh_name():
    def mk():
        k = R.choice([3, 3, 4, 4, "circle"])
        nm_ = PN[k] if k != "circle" else "원"
        return mcq("이 도형의 이름은 무엇일까요?%s" % one(k), nm_, [x for x in ("삼각형", "사각형", "원", "오각형") if x != nm_],
                   {"삼각형": "곧은 선 3개로 둘러싸여 있어요.", "사각형": "곧은 선 4개로 둘러싸여 있어요.", "원": "어느 쪽에서 봐도 똑같이 동그란 모양이에요."}[nm_] + " <b>%s</b>" % nm_)
    return mk


def sh_which():
    def mk():
        tgt = R.choice([3, 4, "circle"])
        nm_ = PN[tgt] if tgt != "circle" else "원"
        bad = {3: ["open3", "curve3", 4, 5], 4: ["curve4", 3, 5, 6], "circle": ["oval", 6, 5, "curve3"]}[tgt]
        ks = [tgt] + R.sample(bad, 3)
        R.shuffle(ks)
        a = LET[ks.index(tgt)]
        why = {3: "곧은 선 3개로 <b>끊어진 곳 없이</b> 둘러싸인 도형이 삼각형이에요.", 4: "곧은 선 4개로 둘러싸인 도형이 사각형이에요.",
               "circle": "길쭉하지 않고 어느 쪽에서 봐도 똑같이 동그란 도형이 원이에요."}[tgt]
        return mcq("<b>%s</b>은 어느 것일까요?%s" % (nm_, lettered(ks)), a, [LET[i] for i in range(4) if LET[i] != a], why + " <b>%s</b>" % a)
    return mk


def sh_count_parts():
    def mk():
        k = R.choice([3, 4, 5, 6, "circle"])
        part = R.choice(["변", "꼭짓점"])
        v = 0 if k == "circle" else k
        nm_ = PN[k] if k != "circle" else "원"
        a = "%d개" % v if v else "없어요"
        return mcq("이 도형의 %s 몇 개일까요?%s" % (josa(part, "은/는"), one(k)), a, [x for x in ("3개", "4개", "5개", "6개", "없어요", "2개") if x != a][:4],
                   ("%s의 %s 모두 %d개예요." % (nm_, josa(part, "은/는"), v)) if v else "원에는 곧은 선이 없어서 변과 꼭짓점이 <b>없어요</b>.")
    return mk


def sh_facts():
    F = [("곧은 선을 무엇이라고 할까요? (도형에서)", "변", ["꼭짓점", "원", "꼭지"], "도형에서 곧은 선을 <b>변</b>이라고 해요."),
         ("두 곧은 선이 만나는 점을 무엇이라고 할까요?", "꼭짓점", ["변", "중심", "모서리"], "두 변이 만나는 점을 <b>꼭짓점</b>이라고 해요."),
         ("변이 3개, 꼭짓점이 3개인 도형은 무엇일까요?", "삼각형", ["사각형", "원", "오각형"], "<b>삼각형</b>이에요."),
         ("변이 4개, 꼭짓점이 4개인 도형은 무엇일까요?", "사각형", ["삼각형", "오각형", "원"], "<b>사각형</b>이에요."),
         ("변이 5개인 도형은 무엇일까요?", "오각형", ["사각형", "육각형", "원"], "변이 5개, 꼭짓점이 5개인 도형은 <b>오각형</b>이에요."),
         ("꼭짓점이 6개인 도형은 무엇일까요?", "육각형", ["오각형", "사각형", "삼각형"], "변이 6개, 꼭짓점이 6개인 도형은 <b>육각형</b>이에요."),
         ("변과 꼭짓점이 없는 도형은 무엇일까요?", "원", ["삼각형", "사각형", "육각형"], "<b>원</b>은 굽은 선으로 되어 있어요."),
         ("원에 대해 바르게 말한 것은 무엇일까요?", "어느 쪽에서 봐도 똑같이 동그래요", ["꼭짓점이 1개 있어요", "길쭉한 것도 원이에요", "변이 1개 있어요"],
          "원은 길쭉하거나 찌그러진 곳이 없고 <b>어느 쪽에서 봐도 똑같이 동그래요</b>."),
         ("삼각형과 사각형의 같은 점은 무엇일까요?", "곧은 선으로 둘러싸여 있어요", ["꼭짓점이 3개예요", "변이 4개예요", "굽은 선이 있어요"],
          "두 도형 모두 <b>곧은 선으로 둘러싸여 있어요</b>."),
         ("사각형의 변의 수와 꼭짓점의 수를 더하면 얼마일까요?", "8", ["4", "6", "16"], "변 4개 + 꼭짓점 4개 = <b>8</b>"),
         ("칠교판의 조각 중 삼각형은 몇 개일까요?", "5개", ["2개", "7개", "4개"], "칠교판은 삼각형 <b>5개</b>, 사각형 2개로 되어 있어요."),
         ("칠교판의 조각 중 사각형은 몇 개일까요?", "2개", ["5개", "7개", "1개"], "칠교판은 삼각형 5개, 사각형 <b>2개</b>로 되어 있어요.")]
    pool = F[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        return mcq(*pool.pop())
    return mk


def sh_poly():
    def mk():
        how = R.choice(["name", "name", "count"])
        if how == "name":
            k = R.choice([5, 6, 5, 6, 4, 3])
            return mcq("이 도형의 이름은 무엇일까요? (변을 세어 보세요)%s" % one(k), PN[k], [PN[x] for x in (3, 4, 5, 6) if x != k],
                       "변이 %d개, 꼭짓점이 %d개예요. <b>%s</b>" % (k, k, PN[k]))
        ks = [R.choice([3, 4, 5, 6]) for _ in range(R.randint(2, 3))]
        part = R.choice(["변", "꼭짓점"])
        tot = sum(ks)
        names = " ".join(PN[k] for k in ks)
        return mcq("<b>%s</b>의 %s의 수를 모두 더하면 몇 개일까요?" % (names.replace(" ", ", "), part), "%d개" % tot, ["%d개" % x for x in (tot + 1, tot - 1, tot + 2, len(ks))],
                   "%s → <b>%d개</b>" % (" + ".join(str(k) for k in ks), tot))
    return mk


def sh_count():
    def mk():
        n = R.randint(6, 9)
        kinds = [R.choice([3, 4, 5, 6, "circle"]) for _ in range(n)]
        cols = 5
        sp = 84
        s = []
        for i, k in enumerate(kinds):
            cx, cy = 10 + sp / 2 + (i % cols) * sp, 10 + sp / 2 + (i // cols) * sp
            s.append(shape_el(k, cx, cy, 34, FILLS[i % 4], reg=True))
        pic = ko(svg_wrap(20 + cols * sp, 20 + ((n - 1) // cols + 1) * sp, "".join(s), "여러 가지 도형"), "여러 가지 도형")
        t = R.choice([3, 4, 5, 6, "circle"])
        c = kinds.count(t)
        if c == 0:
            return None
        nm_ = PN[t] if t != "circle" else "원"
        return mcq("<b>%s</b> 몇 개일까요?%s" % (josa(nm_, "은/는"), pic), "%d개" % c, ["%d개" % x for x in (c + 1, c - 1, c + 2, n) if x > 0 and x != c],
                   "변(곧은 선)의 수를 세어 %s만 찾아요. <b>%d개</b>" % (nm_, c) if t != "circle" else "동그란 도형만 세어요. <b>%d개</b>" % c)
    return mk


def sh_dots():
    """점 종이에서 점을 이으면"""
    def mk():
        k = R.choice([3, 4, 5, 6])
        how = R.choice(["make", "cut"])
        if how == "make":
            return mcq("점 종이에서 한 줄 위에 있지 않은 점 <b>%d개</b>를 곧은 선으로 차례로 이어 둘러쌌어요. 어떤 도형이 될까요?" % k, PN[k], [PN[x] for x in (3, 4, 5, 6) if x != k],
                       "꼭짓점이 %d개인 도형이에요. <b>%s</b>" % (k, PN[k]))
        return mcq("사각형의 마주 보는 두 꼭짓점을 곧은 선으로 이어 잘랐어요. 어떤 도형이 2개 생길까요?", "삼각형", ["사각형", "원", "오각형"],
                   "사각형을 마주 보는 꼭짓점끼리 이어 자르면 <b>삼각형</b> 2개가 생겨요.")
    return mk


# ------------------------------------------------------------------ 쌓기나무
C30, S30 = math.cos(math.pi / 6), math.sin(math.pi / 6)
TOP, RIGHT, LEFT = "#d9f0de", "#9fd3a7", "#bfe5c7"


def iso(cells, colors=None, A=30):
    colors = colors or {}

    def P(x, y, z):
        return ((x - y) * A * C30, (x + y) * A * S30 - z * A)
    pts = [P(x + dx, y + dy, z + dz) for (x, y, z) in cells for dx in (0, 1) for dy in (0, 1) for dz in (0, 1)]
    mx_ = max(c[0] for c in cells) + 1
    my_ = max(c[1] for c in cells) + 1
    fx_, fy_ = P(mx_ / 2.0, my_, 0.5)
    lx_, ly_ = fx_ - C30 * 60, fy_ + S30 * 60
    pts += [(lx_ - 14, ly_ + 10), (lx_ + 14, ly_ + 10)]
    minx, miny = min(p[0] for p in pts) - 10, min(p[1] for p in pts) - 10
    W, H = max(p[0] for p in pts) - minx + 10, max(p[1] for p in pts) - miny + 10

    def Q(x, y, z):
        px, py = P(x, y, z)
        return "%.1f,%.1f" % (px - minx, py - miny)
    SH = {"red": ("#f6b3ad", "#e05a4f", "#ec8a82"), "yellow": ("#fbe7a1", "#e9c24f", "#f4d675"), "blue": ("#c7dcf4", "#6c9fd8", "#9bbfe8")}
    s = []
    for (x, y, z) in sorted(cells, key=lambda c: (c[0] + c[1], c[2])):
        t, rr, ll = SH.get(colors.get((x, y, z)), (TOP, RIGHT, LEFT))
        for f, col in (([Q(x, y, z + 1), Q(x + 1, y, z + 1), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)], t),
                       ([Q(x + 1, y, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x + 1, y, z + 1)], rr),
                       ([Q(x, y + 1, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)], ll)):
            s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.4'/>" % (" ".join(f), col, GREEN))
    ax, ay = lx_ - minx, ly_ - miny
    tx, ty = fx_ - minx - C30 * 14, fy_ - miny + S30 * 14
    s.append(text(ax, ay + 8, "앞", 17))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (ax + C30 * 14, ay - S30 * 14, tx, ty, RED))
    a_ = math.atan2(ty - (ay - S30 * 14), tx - (ax + C30 * 14))
    s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (tx, ty, tx - 10 * math.cos(a_ - 0.45), ty - 10 * math.sin(a_ - 0.45),
                                                                            tx - 10 * math.cos(a_ + 0.45), ty - 10 * math.sin(a_ + 0.45), RED))
    return fig(svg_wrap(int(W), int(H), "".join(s), "쌓기나무로 쌓은 모양").replace("<svg ", "<svg data-pf='lg' ", 1))


def row_build(maxlen=5, maxh=3):
    """한 줄（y = 0）로 쌓은 모양：모든 쌓기나무가 보여요"""
    L = R.randint(2, maxlen)
    hs = [R.randint(1, maxh) for _ in range(L)]
    cells = [(x, 0, z) for x, h in enumerate(hs) for z in range(h)]
    # 앞에 1층짜리를 하나 놓을 수도 있음（뒤쪽 기둥이 1층일 때만）
    if R.random() < 0.4:
        cand = [x for x, h in enumerate(hs) if h == 1]
        if cand:
            cells.append((R.choice(cand), 1, 0))
    return cells


def cube_count():
    def mk():
        cells = row_build(5, R.choice([1, 2, 3]))
        n = len(cells)
        return mcq("쌓기나무는 모두 몇 개일까요?%s" % iso(cells), "%d개" % n, ["%d개" % x for x in (n + 1, n - 1, n + 2, len({c[0] for c in cells})) if x > 0 and x != n],
                   "아래층부터 차례로 세어 보면 <b>%d개</b>예요." % n)
    return mk


def cube_layer():
    def mk():
        cells = row_build(5, 3)
        top = max(c[2] for c in cells) + 1
        if top < 2:
            return None
        k = R.randint(1, top)
        c = sum(1 for x in cells if x[2] == k - 1)
        return mcq("<b>%d층</b>에 있는 쌓기나무는 몇 개일까요?%s" % (k, iso(cells)), "%d개" % c, ["%d개" % x for x in (c + 1, c - 1, len(cells), c + 2) if x > 0 and x != c],
                   "%d층(%s)에 있는 쌓기나무만 세면 <b>%d개</b>예요." % (k, "맨 아래" if k == 1 else "아래에서 %d번째" % k, c))
    return mk


DIRS = {(1, 0, 0): "오른쪽", (-1, 0, 0): "왼쪽", (0, 0, 1): "위", (0, 1, 0): "앞"}


def cube_pos():
    def mk():
        L = R.randint(3, 4)
        hs = [R.randint(1, 2) for _ in range(L)]
        cells = [(x, 0, z) for x, h in enumerate(hs) for z in range(h)]
        red = R.choice([c for c in cells if c[2] == 0])
        opts = []
        for d, word in DIRS.items():
            nb = (red[0] + d[0], red[1] + d[1], red[2] + d[2])
            if nb in cells:
                opts.append((nb, word))
            elif d == (0, 1, 0) and hs[red[0]] == 1:
                opts.append((nb, word))
            elif d == (0, 0, 1) and nb not in cells:
                pass
        if not opts:
            return None
        nb, word = R.choice(opts)
        if nb not in cells:
            cells.append(nb)
        pic = iso(cells, {red: "red", nb: "yellow"})
        return mcq("노란색 쌓기나무는 빨간색 쌓기나무의 어느 쪽에 있을까요? (앞에서 볼 때)%s" % pic, word, [w for w in ("오른쪽", "왼쪽", "위", "앞") if w != word],
                   "앞에서 보면 노란색 쌓기나무는 빨간색 쌓기나무의 <b>%s</b>에 있어요." % word)
    return mk


def cube_describe():
    def mk():
        how = R.choice(["layers", "row"])
        if how == "layers":
            a, b = R.randint(2, 5), R.randint(1, 3)
            c = R.randint(0, min(b, 2))
            if b > a:
                return None
            n = a + b + c
            q = "쌓기나무를 1층에 %d개, 2층에 %d개%s 쌓았어요. 사용한 쌓기나무는 모두 몇 개일까요?" % (a, b, ", 3층에 %d개" % c if c else "")
            return mcq(q, "%d개" % n, ["%d개" % x for x in (n + 1, n - 1, a + b if c else a, a * 2)], "%s = <b>%d개</b>" % (" + ".join(str(x) for x in (a, b, c) if x), n))
        hs = [R.randint(1, 3) for _ in range(R.randint(3, 4))]
        n = sum(hs)
        desc = "왼쪽부터 %s" % ", ".join("%d층" % h for h in hs)
        return mcq("쌓기나무를 옆으로 한 줄로 놓고 %s으로 쌓았어요. 쌓기나무는 모두 몇 개일까요?" % desc, "%d개" % n,
                   ["%d개" % x for x in (n + 1, n - 1, len(hs), max(hs) * len(hs)) if x != n],
                   "%s = <b>%d개</b>" % (" + ".join(map(str, hs)), n))
    return mk


def cube_change():
    def mk():
        a = row_build(4, 2)
        b = row_build(4, 3)
        if len(a) == len(b):
            return None
        sp = "%s%s" % (iso(a).replace("<div class='qfig'>", "").replace("</div>", ""), iso(b).replace("<div class='qfig'>", "").replace("</div>", ""))
        pic = "<div class='qfig'>%s</div>" % sp
        d = len(b) - len(a)
        if d > 0:
            q = "왼쪽 모양(%d개)을 오른쪽 모양으로 바꾸려면 쌓기나무가 몇 개 더 필요할까요?%s" % (len(a), pic)
        else:
            q = "왼쪽 모양(%d개)을 오른쪽 모양으로 바꾸려면 쌓기나무를 몇 개 빼야 할까요?%s" % (len(a), pic)
        v = abs(d)
        return mcq(q, "%d개" % v, ["%d개" % x for x in (v + 1, v - 1, len(b), len(a)) if x > 0 and x != v],
                   "왼쪽은 %d개, 오른쪽은 %d개예요. %d − %d = <b>%d개</b>" % (len(a), len(b), max(len(a), len(b)), min(len(a), len(b)), v))
    return mk


# ------------------------------------------------------------------ 규칙 찾기
COLN = {"red": "빨간색", "blue": "파란색", "yellow": "노란색", "green": "초록색"}
SHN = {"circle": "○", "triangle": "△", "square": "□"}


def p_tile():
    def mk():
        p = R.choice(["ABC", "ABB", "AABB", "ABCB", "AAB"])
        items = sorted(set(p))
        how = R.choice(["shape", "both"])
        sh = R.sample(list(SHN), len(items))
        cs = R.sample(list(COLN), len(items))
        mp = {ch: (sh[i] if how == "shape" else sh[i], cs[i] if how == "both" else "blue") for i, ch in enumerate(items)}
        L = len(p) * 2 + R.randint(1, len(p) - 1)
        seq = [mp[p[i % len(p)]] for i in range(L + 1)]
        ans = seq[-1]
        say = lambda v: ("%s %s" % (COLN[v[1]], SHN[v[0]])) if how == "both" else SHN[v[0]]
        pic = ko(pattern_svg([("shape", k, c) for k, c in seq[:-1]], 1), "규칙에 따라 놓은 모양")
        others = list({say(v) for v in mp.values() if v != ans})
        extra = ["%s %s" % (COLN[c], SHN[k]) for k in SHN for c in COLN] if how == "both" else list(SHN.values())
        return mcq("규칙에 따라 모양을 놓았어요. ?에 알맞은 것은 무엇일까요?%s" % pic, say(ans), others + [x for x in extra if x != say(ans) and x not in others],
                   "%s 반복돼요. <b>%s</b>" % (josa(", ".join(say(mp[c]) for c in p), "이/가"), say(ans)))
    return mk


def p_stack():
    def mk():
        a = R.randint(1, 4)
        d = R.randint(1, 3)
        hs = [a + d * i for i in range(3)]
        far = R.random() < 0.5
        nxt = hs[-1] + d * (2 if far else 1)
        if nxt > 12:
            return None
        pic = ko(K.towers_svg(hs, ["첫째", "둘째", "셋째"]), "쌓은 상자")
        return mcq("규칙에 따라 상자를 쌓았어요. %s에 쌓을 상자는 몇 개일까요?%s" % ("다섯째" if far else "넷째", pic), "%d개" % nxt, ["%d개" % x for x in (nxt + 1, nxt - 1, hs[-1] + 1 if d != 1 else nxt + 2, hs[-1] * 2) if x != nxt],
                   "상자가 %d개씩 늘어나요. %s<b>%d개</b>" % (d, "넷째 %d개, 다섯째 " % (hs[-1] + d) if far else "%d + %d = " % (hs[-1], d), nxt))
    return mk


def addtab(r0, c0, nr=3, nc=4, mul=False, target=None):
    op = "×" if mul else "+"
    head = "<tr><th>%s</th>%s</tr>" % (op, "".join("<th>%d</th>" % (c0 + j) for j in range(nc)))
    body = ""
    for i in range(nr):
        cells = ""
        for j in range(nc):
            v = (r0 + i) * (c0 + j) if mul else (r0 + i) + (c0 + j)
            cells += "<td>%s</td>" % ("□" if (i, j) == target else v)
        body += "<tr><th>%d</th>%s</tr>" % (r0 + i, cells)
    return "<div class='sn-tw'><table class='sn-table'>%s%s</table></div>" % (head, body)


def p_addtab():
    def mk():
        how = R.choice(["cell", "rule", "diag"])
        r0, c0 = R.randint(1, 6), R.randint(1, 5)
        if how == "cell":
            ti, tj = R.randint(0, 2), R.randint(0, 3)
            v = (r0 + ti) + (c0 + tj)
            return mcq("덧셈표의 일부예요. □에 알맞은 수는 무엇일까요?%s" % addtab(r0, c0, target=(ti, tj)), str(v), [str(x) for x in (v + 1, v - 1, v + 2, (r0 + ti) * (c0 + tj))],
                       "%d + %d = <b>%d</b>" % (r0 + ti, c0 + tj, v))
        if how == "rule":
            return mcq("덧셈표에서 → 방향으로 가면 수가 어떻게 변할까요?%s" % addtab(r0, c0), "1씩 커져요", ["2씩 커져요", "1씩 작아져요", "10씩 커져요"],
                       "더하는 수가 1씩 커지니 합도 <b>1씩 커져요</b>.")
        return mcq("덧셈표에서 ↘ 방향(오른쪽 아래)으로 가면 수가 어떻게 변할까요?%s" % addtab(r0, c0), "2씩 커져요", ["1씩 커져요", "같아요", "3씩 커져요"],
                   "오른쪽으로 1, 아래로 1 커지니 <b>2씩 커져요</b>.")
    return mk


def p_multab():
    def mk():
        how = R.choice(["cell", "rule", "five", "even"])
        r0, c0 = R.randint(2, 7), R.randint(2, 6)
        if how == "cell":
            ti, tj = R.randint(0, 2), R.randint(0, 3)
            v = (r0 + ti) * (c0 + tj)
            return mcq("곱셈표의 일부예요. □에 알맞은 수는 무엇일까요?%s" % addtab(r0, c0, mul=True, target=(ti, tj)), str(v),
                       [str(x) for x in (v + r0 + ti, v - (r0 + ti), (r0 + ti) + (c0 + tj), v + 1)], "%d × %d = <b>%d</b>" % (r0 + ti, c0 + tj, v))
        if how == "rule":
            a = r0
            return mcq("곱셈표의 <b>%d단</b>에서 → 방향으로 가면 곱이 몇씩 커질까요?" % a, "%d씩" % a, ["%d씩" % x for x in (a + 1, a - 1, 1, 10) if x != a and x > 0],
                       "%d단의 곱은 <b>%d씩</b> 커져요." % (a, a))
        if how == "five":
            return mcq("5단 곱셈구구의 곱(5, 10, 15, 20, …)에서 일의 자리 숫자는 어떤 규칙이 있을까요?", "5와 0이 반복돼요", ["1씩 커져요", "모두 5예요", "0, 1, 2가 반복돼요"],
                       "5, 10, 15, 20, 25…의 일의 자리는 <b>5와 0이 반복돼요</b>.")
        a = R.choice([2, 4, 6, 8])
        return mcq("<b>%d단</b> 곱셈구구의 곱은 모두 어떤 수일까요?" % a, "짝수", ["홀수", "짝수와 홀수가 번갈아 나와요", "10보다 큰 수"],
                   "%d단의 곱(%s…)은 모두 <b>짝수</b>예요." % (a, ", ".join(str(a * i) for i in range(1, 5))))
    return mk


def p_life():
    def mk():
        how = R.choice(["cal", "bus", "seat", "lift"])
        if how == "cal":
            d = R.randint(1, 10)
            k = R.randint(1, 3)
            w = R.choice(["월", "화", "수", "목", "금"])
            return mcq("달력에서 %d일은 %s요일이에요. 같은 달에서 %d주일 뒤의 %s요일은 며칠일까요?" % (d, w, k, w),
                       "%d일" % (d + 7 * k), ["%d일" % x for x in (d + k, d + 7 * k + 1, d + 6 * k, d + 10 * k) if x != d + 7 * k],
                       "달력에서 아래로 한 칸 가면 7일 뒤, 같은 요일이에요. %d + 7 × %d = <b>%d일</b>" % (d, k, d + 7 * k))
        if how == "bus":
            st = R.choice([10, 15, 20, 30])
            h = R.randint(7, 9)
            ts = [(h * 60 + st * i) for i in range(4)]
            fmt = lambda t: "%d시 %02d분" % (t // 60, t % 60) if t % 60 else "%d시" % (t // 60)
            nxt = ts[-1] + st
            return mcq("버스가 %s에 출발해요. 다음 버스는 몇 시 몇 분에 출발할까요?" % ", ".join(fmt(t) for t in ts), fmt(nxt),
                       [fmt(x) for x in (nxt + 10, nxt - 5, ts[-1] + 60, nxt + 5) if x != nxt], "%d분마다 출발해요. <b>%s</b>" % (st, fmt(nxt)))
        if how == "seat":
            per = R.choice([8, 9, 10])
            r = R.randint(2, 5)
            c = R.randint(1, per)
            n = (r - 1) * per + c
            return mcq("공연장 의자에 한 줄에 %d개씩 번호가 1번부터 차례로 붙어 있어요. <b>%d번째 줄 %d번째</b> 의자의 번호는 몇 번일까요?" % (per, r, c), "%d번" % n,
                       ["%d번" % x for x in (n + per, n - 1, r * 10 + c, n + 1) if x != n and x > 0],
                       "한 줄에 %d개씩이니 아래로 한 줄 가면 %d씩 커져요. %d × %d + %d = <b>%d번</b>" % (per, per, per, r - 1, c, n))
        st = R.choice([3, 4, 5])
        b = R.randint(1, 3)
        seq = [b + st * i for i in range(4)]
        return mcq("엘리베이터 버튼이 위로 %s층처럼 놓여 있어요. 그 위의 버튼은 몇 층일까요?" % ", ".join(map(str, seq)), "%d층" % (seq[-1] + st),
                   ["%d층" % x for x in (seq[-1] + 1, seq[-1] + st + 1, seq[-1] + 2 * st)], "%d씩 커지는 규칙이에요. <b>%d층</b>" % (st, seq[-1] + st))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "shapes":
        return unit(G, "triangles-quadrilaterals-and-circles", 2, "[2수03-03] [2수03-04] [2수03-05]",
                    "삼각형, 사각형, 원의 모양을 찾고, 이를 이용하여 여러 가지 모양을 만들 수 있다. 삼각형, 사각형, 원을 직관적으로 이해하고, 그 모양을 그릴 수 있다. 삼각형, 사각형에서 각각의 공통점을 찾아 말할 수 있다.",
                    "삼각형, 사각형, 원과 오각형, 육각형", "여러 가지 도형",
                    "초등 2학년 1학기 여러 가지 도형 학습지: 삼각형·사각형·원 알기, 변과 꼭짓점, 오각형과 육각형, 칠교판, 도형 세기, 점을 이어 도형 만들기까지 100문제와 정답.",
                    "변 3개 삼각형, 변 4개 사각형", "곧은 선은 변, 두 변이 만나는 점은 꼭짓점이에요.",
                    ["곧은 선 3개로 둘러싸인 도형을 <b>삼각형</b>, 곧은 선 4개로 둘러싸인 도형을 <b>사각형</b>이라고 해요.",
                     "도형의 곧은 선을 <b>변</b>, 두 변이 만나는 점을 <b>꼭짓점</b>이라고 해요.",
                     "변과 꼭짓점이 5개면 <b>오각형</b>, 6개면 <b>육각형</b>이에요.",
                     "어느 쪽에서 봐도 똑같이 동그란 도형을 <b>원</b>이라고 해요. 원에는 변과 꼭짓점이 없어요."],
                    [("변이 6개인 도형", ["변 6개, 꼭짓점 6개"], "육각형"),
                     ("삼각형의 변과 꼭짓점의 수의 합", ["3 + 3"], "6")],
                    [("끊어진 곳이 있어도 삼각형이라고 한다", "곧은 선으로 끊어진 곳 없이 둘러싸여야 해요."),
                     ("한 변이 굽은 도형을 사각형이라고 한다", "변은 모두 곧은 선이어야 해요."),
                     ("길쭉한 동그라미도 원이라고 한다", "원은 어느 쪽에서 봐도 똑같이 동그래요.")],
                    [("1학년의 □, △, ○ 모양과 무엇이 다른가요?", "2학년에서는 변과 꼭짓점을 알고, 삼각형·사각형·원이라는 이름으로 정확하게 구별해요."),
                     ("칠교판은 무엇인가요?", "큰 정사각형을 삼각형 5조각과 사각형 2조각으로 나눈 퍼즐이에요. 여러 가지 모양을 만들어 볼 수 있어요.")],
                    [("삼각형, 사각형, 원", [(sh_name(), 10), (sh_which(), 10)]),
                     ("변과 꼭짓점", [(sh_count_parts(), 16), (sh_facts(), 4)]),
                     ("오각형과 육각형", [(sh_poly(), 20)]),
                     ("도형의 특징", [(sh_facts(), 8), (sh_dots(), 4), (sh_which(), 8)]),
                     ("도형 세기", [(sh_count(), 20)])], 82202)
    if which == "cubes":
        return unit(G, "stacking-cubes", 3, "[2수03-02]",
                    "쌓기나무를 이용하여 여러 가지 입체도형의 모양을 만들고, 그 모양에 대해 위치나 방향을 이용하여 말할 수 있다.",
                    "쌓기나무: 개수, 층, 위치와 방향", "쌓기나무",
                    "초등 2학년 1학기 쌓기나무 학습지: 쌓은 쌓기나무의 개수, 층별 개수, 오른쪽·왼쪽·위·앞으로 위치 말하기, 설명대로 쌓기, 모양 바꾸기까지 100문제와 정답.",
                    "1층부터 차례로 세어요", "위치는 앞에서 보는 사람을 기준으로 말해요.",
                    ["쌓기나무의 개수는 <b>1층부터 차례로</b> 세면 빠뜨리지 않아요.",
                     "맨 아래가 1층, 그 위가 2층, 3층이에요.",
                     "위치는 <b>앞에서 보았을 때</b>를 기준으로 오른쪽, 왼쪽, 위, 앞, 뒤로 말해요.",
                     "모양을 바꿀 때는 처음 개수와 나중 개수의 차를 구해요."],
                    [("1층 3개, 2층 2개, 3층 1개", ["3 + 2 + 1"], "6개"),
                     ("빨간 쌓기나무 바로 위의 쌓기나무", ["빨간 쌓기나무보다 한 층 위"], "위")],
                    [("같은 쌓기나무를 두 번 센다", "층별로 나누어 세어요."),
                     ("보는 사람의 왼쪽과 오른쪽을 반대로 말한다", "앞에서 볼 때를 기준으로 해요."),
                     ("층과 개수를 헷갈린다", "2층은 아래에서 두 번째 칸이에요.")],
                    [("쌓기나무가 없으면 어떻게 하나요?", "주사위나 각설탕처럼 같은 크기의 정육면체 물건으로 쌓아 보세요."),
                     ("6학년 쌓기나무와 무엇이 다른가요?", "2학년은 위치와 방향 말하기, 6학년은 위·앞·옆에서 본 모양과 개수 구하기를 배워요.")],
                    [("쌓기나무의 개수", [(cube_count(), 20)]),
                     ("층별 개수", [(cube_layer(), 20)]),
                     ("위치와 방향", [(cube_pos(), 20)]),
                     ("설명대로 쌓기", [(cube_describe(), 20)]),
                     ("모양 바꾸기", [(cube_change(), 20)])], 82203)
    if which == "pattern":
        return unit(G, "patterns", 17, "[2수02-01] [2수02-02]",
                    "물체, 무늬, 수 등의 배열에서 규칙을 찾아 여러 가지 방법으로 표현할 수 있다. 자신이 정한 규칙에 따라 물체, 무늬, 수 등을 배열할 수 있다.",
                    "규칙 찾기: 무늬·쌓은 모양·덧셈표·곱셈표", "규칙 찾기",
                    "초등 2학년 2학기 규칙 찾기 학습지: 무늬의 규칙, 쌓은 모양의 규칙, 덧셈표와 곱셈표의 규칙, 달력·버스 시간표·좌석 번호처럼 생활 속 규칙까지 100문제와 정답.",
                    "되풀이되거나 일정하게 커지는 것", "덧셈표 → 1씩, 곱셈표 □단 → □씩 커져요.",
                    ["무늬에서 <b>되풀이되는 부분</b>을 찾으면 다음에 올 모양과 색을 알 수 있어요.",
                     "쌓은 모양은 몇 개씩 늘어나는지 살펴봐요.",
                     "덧셈표에서 → 방향과 ↓ 방향은 1씩, ↘ 방향은 2씩 커져요.",
                     "곱셈표에서 □단은 □씩 커져요. 달력에서는 아래로 한 칸 가면 7 커져요."],
                    [("1, 3, 5개로 쌓은 다음 모양", ["2개씩 늘어나요."], "7개"),
                     ("4단 곱셈구구 12 다음", ["4씩 커져요."], "16")],
                    [("반복되는 부분을 짧게 잡는다", "여러 번 반복되는지 끝까지 확인해요."),
                     ("덧셈표의 ↘ 방향을 1씩이라고 한다", "오른쪽 1, 아래 1이 함께 커지니 2씩이에요."),
                     ("달력의 아래 칸을 1 큰 수라고 한다", "아래 칸은 7일 뒤예요.")],
                    [("규칙 찾기가 왜 중요한가요?", "규칙을 찾는 힘은 곱셈구구, 4학년의 규칙과 대응, 나중의 함수로 이어져요."),
                     ("집에서 어떻게 연습하나요?", "달력, 엘리베이터 버튼, 아파트 호수처럼 생활 속 수의 규칙을 함께 찾아 보세요.")],
                    [("무늬의 규칙", [(p_tile(), 20)]),
                     ("쌓은 모양의 규칙", [(p_stack(), 15), (p_life(), 5)]),
                     ("덧셈표의 규칙", [(p_addtab(), 20)]),
                     ("곱셈표의 규칙", [(p_multab(), 20)]),
                     ("생활 속 규칙", [(p_life(), 20)])], 82217)
    raise ValueError(which)
