# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: partes comuns.
d (Fraction → decimal brasileiro: vírgula, ponto nos milhares, sinal −), expr/fq (fr_c4), P2 (ax² + bx + c), sq (√ simplificada),
M (mcq que aceita negativos e tira respostas erradas iguais à certa), figure (fr_c4), kosy (de_k8), unit (make_unit com grade 9-ano).
"""
import math
from fractions import Fraction as Fr
from br_common import mcq, num, relabel, fig, make_unit, NB  # noqa: F401
import fr_c4
import de_k8

MINUS = "−"


def d(x, places=None, keep=False):
    """Fraction/int/float → «1.234,5», «−0,25»; places arredonda a essas casas (sem zeros no fim, a não ser com keep=True)"""
    x = Fr(x) if not isinstance(x, float) else Fr(str(x))
    neg = x < 0
    x = abs(x)
    if places is None:
        for p in range(0, 7):
            if (x * 10 ** p).denominator == 1:
                places = p
                break
        else:
            raise ValueError("dízima")
    v = int(x * 10 ** places + Fr(1, 2))
    ip, fp = divmod(v, 10 ** places) if places else (v, 0)
    fs = str(fp).rjust(places, "0") if places else ""
    if not keep:
        fs = fs.rstrip("0")
    s = num(ip) + ("," + fs if fs else "")
    return (MINUS if neg and v else "") + s


def fq(x):
    """Fraction → HTML (inteiro quando der)"""
    x = Fr(x)
    if x.denominator == 1:
        return d(x)
    return fr_c4.fq(x)


def coef(k, var, first):
    k = Fr(k)
    a = abs(k)
    sign = (MINUS if k < 0 else "") if first else (" %s " % MINUS if k < 0 else " + ")
    if var and a == 1:
        body = var
    else:
        body = (d(a) if a.denominator == 1 else fr_c4.fq(a)) + var
    return sign + body


def expr(terms):
    out = ""
    for k, v in terms:
        if Fr(k) == 0:
            continue
        out += coef(k, v, out == "")
    return out or "0"


def P2(a, b, c, x="x"):
    return expr([(a, x + "²"), (b, x), (c, "")])


def par(x):
    return "(%s)" % d(x) if Fr(x) < 0 else d(x)


def sq(n):
    """√n simplificada: 12 → 2√3, 9 → 3"""
    k, m = 1, n
    for p in range(2, math.isqrt(n) + 1):
        while m % (p * p) == 0:
            m //= p * p
            k *= p
    if m == 1:
        return str(k)
    return ("" if k == 1 else str(k)) + "√" + str(m)


def M(q, a, w, e):
    """mcq com negativos; tira respostas erradas iguais à certa ou repetidas"""
    a = str(a)
    seen, ww = {a}, []
    for x in w:
        x = str(x)
        if x not in seen and x != "None":
            seen.add(x)
            ww.append(x)
    return mcq(q, a, ww, e, neg=True)


def figure(*a, **k):
    k.setdefault("label", "figura geométrica")
    return fr_c4.figure(*a, **k)


def kosy(lines=(), pts=(), lo=-5, hi=5, label="plano cartesiano"):
    return de_k8.kosy(lines, pts, lo, hi, label=label)


def unit(R, slug, dom, codes, std, title, short, meta, kb, ks, body, faq, sets, sort):
    make_unit(R, slug, dom, codes, std, title, short, meta, kb, ks, body, faq, sets, sort, grade="9-ano")


# ---------- figuras de geometria (SVG próprio) ----------
import math as _m
INK, BLUE, RED, GRN = "#222", "#1f5fbf", "#c0392b", "#2e7d32"


def _t(x, y, s, size=16, col=INK, bold=True, anchor="middle"):
    return "<text x='%.1f' y='%.1f' font-size='%d' text-anchor='%s' fill='%s'%s font-family='sans-serif'>%s</text>" % (x, y, size, anchor, col, " font-weight='700'" if bold else "", s)


def _ln(x1, y1, x2, y2, col=INK, w=2):
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>" % (x1, y1, x2, y2, col, w)


def _arc(cx, cy, r, a1, a2, col=BLUE):
    """arco de a1 a a2 graus (sentido anti-horário, eixo y para cima)"""
    x1, y1 = cx + r * _m.cos(_m.radians(a1)), cy - r * _m.sin(_m.radians(a1))
    x2, y2 = cx + r * _m.cos(_m.radians(a2)), cy - r * _m.sin(_m.radians(a2))
    big = 1 if (a2 - a1) % 360 > 180 else 0
    return "<path d='M%.1f %.1f A%.1f %.1f 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>" % (x1, y1, r, r, big, x2, y2, col)


def _svg(W, H, body, label):
    return fig("<svg data-pf='lg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' aria-label='%s'>%s</svg>" % (W, H, W, H, label, body))


POS = {"tr": (0, 1), "tl": (1, 2), "bl": (2, 3), "br": (3, 0)}


def paralelas(alpha, marks, label="retas paralelas r e s cortadas por uma transversal t"):
    """alpha: ângulo agudo entre a transversal e as paralelas (graus); marks: {(0 ou 1, 'tr'|'tl'|'bl'|'br'): texto}.
    0 = cruzamento de cima (reta r), 1 = de baixo (reta s)"""
    W, H = 420, 240
    ys = [70, 170]
    k = 1 / _m.tan(_m.radians(alpha))
    xs = [230 + 50 * k, 230 - 50 * k]
    s = [_ln(20, ys[0], W - 20, ys[0]), _ln(20, ys[1], W - 20, ys[1]), _t(W - 12, ys[0] - 8, "r", 17, anchor="end"), _t(W - 12, ys[1] - 8, "s", 17, anchor="end")]
    xa, xb = xs[0] + 55 * k, xs[1] - 55 * k
    s.append(_ln(xa, ys[0] - 55, xb, ys[1] + 55, INK, 2))
    s.append(_t(xa + 12, ys[0] - 42, "t", 17))
    rays = [0, alpha, 180, 180 + alpha]
    cnt = {}
    for (i, p), txt in sorted(marks.items()):
        cnt[i] = cnt.get(i, 0) + 1
        a1, a2 = rays[POS[p][0]], rays[POS[p][1]] if POS[p][1] else 360
        cx, cy = xs[i], ys[i]
        s.append(_arc(cx, cy, 14 + 6 * cnt[i], a1, a2, RED if txt.startswith(("x", "y", "?")) else BLUE))
        mid = _m.radians((a1 + a2) / 2)
        rr = 40 if (a2 - a1) < 70 else 32
        s.append(_t(cx + rr * _m.cos(mid), cy - rr * _m.sin(mid) + 6, txt, 15, RED if txt.startswith(("x", "y", "?")) else BLUE))
    return _svg(W, H, "".join(s), label)


def circulo(pts, segs, center=True, arcs=(), label="circunferência de centro O", texts=()):
    """pts: {nome: ângulo em graus na circunferência} ou (x, y) relativo ao centro (raio 1); segs: [(A, B)];
    arcs: [(vértice, A, B, texto)] marca o ângulo no vértice entre VA e VB; texts: [(x, y, texto)] relativos"""
    W, H, r = 300, 270, 100
    cx, cy = 150, 135
    P = {}
    for k, v in pts.items():
        if isinstance(v, tuple):
            P[k] = (cx + r * v[0], cy - r * v[1])
        else:
            P[k] = (cx + r * _m.cos(_m.radians(v)), cy - r * _m.sin(_m.radians(v)))
    if center:
        P["O"] = (cx, cy)
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2'/>" % (cx, cy, r, INK)]
    for a, b in segs:
        s.append(_ln(P[a][0], P[a][1], P[b][0], P[b][1], INK, 2))
    omid = None
    for v, a, b, txt in arcs:
        vx, vy = P[v]
        t1 = _m.degrees(_m.atan2(vy - P[a][1], P[a][0] - vx)) % 360
        t2 = _m.degrees(_m.atan2(vy - P[b][1], P[b][0] - vx)) % 360
        if (t2 - t1) % 360 > 180:
            t1, t2 = t2, t1
        span = (t2 - t1) % 360
        s.append(_arc(vx, vy, 22, t1, t1 + span, RED if txt.startswith(("x", "?")) else BLUE))
        mid = _m.radians(t1 + span / 2)
        if v == "O":
            omid = mid
        s.append(_t(vx + 42 * _m.cos(mid), vy - 42 * _m.sin(mid) + 6, txt, 15, RED if txt.startswith(("x", "?")) else BLUE))
    for k, (x, y) in P.items():
        s.append("<circle cx='%.1f' cy='%.1f' r='3.2' fill='%s'/>" % (x, y, INK))
        dx, dy = x - cx, y - cy
        n = _m.hypot(dx, dy) or 1
        if k != "O":
            ox, oy = dx / n * 16, dy / n * 16
        elif omid is None:
            ox, oy = -12, 14
        else:
            ox, oy = -16 * _m.cos(omid), 16 * _m.sin(omid) - 2
        s.append(_t(x + ox, y + oy + 6, k, 16))
    for x, y, txt in texts:
        s.append(_t(cx + r * x, cy - r * y, txt, 15, BLUE))
    return _svg(W, H, "".join(s), label)


def formas(shapes, W=420, H=220, label="figuras geométricas", extra=""):
    """shapes: [{'pts': {nome: (x, y)} em pixels (y para baixo), 'poly': 'ABC' (ordem), 'sides': [(A, B, texto)],
    'right': [(V, A, B)], 'angles': [(V, A, B, texto)], 'segs': [(A, B)]}] — rótulos para fora de cada figura"""
    s = []
    for sh in shapes:
        P = sh["pts"]
        cx = sum(p[0] for p in P.values()) / len(P)
        cy = sum(p[1] for p in P.values()) / len(P)
        poly = sh.get("poly", "")
        if poly:
            s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (" ".join("%.1f,%.1f" % P[k] for k in poly), sh.get("fill", "#eef4fb"), INK))
        for a, b in sh.get("segs", ()):
            s.append(_ln(P[a][0], P[a][1], P[b][0], P[b][1], INK, 2))
        for v, a, b in sh.get("right", ()):
            (vx, vy), (ax, ay), (bx, by) = P[v], P[a], P[b]
            da, db = _m.hypot(ax - vx, ay - vy), _m.hypot(bx - vx, by - vy)
            ux, uy = (ax - vx) / da * 11, (ay - vy) / da * 11
            wx, wy = (bx - vx) / db * 11, (by - vy) / db * 11
            s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.6'/>" % (vx + ux, vy + uy, vx + ux + wx, vy + uy + wy, vx + wx, vy + wy, INK))
        for v, a, b, txt in sh.get("angles", ()):
            vx, vy = P[v]
            t1 = _m.degrees(_m.atan2(vy - P[a][1], P[a][0] - vx)) % 360
            t2 = _m.degrees(_m.atan2(vy - P[b][1], P[b][0] - vx)) % 360
            if (t2 - t1) % 360 > 180:
                t1, t2 = t2, t1
            span = (t2 - t1) % 360
            col = RED if txt.startswith(("x", "?")) else BLUE
            s.append(_arc(vx, vy, 18, t1, t1 + span, col))
            mid = _m.radians(t1 + span / 2)
            s.append(_t(vx + 34 * _m.cos(mid), vy - 34 * _m.sin(mid) + 5, txt, 14, col))
        for a, b, txt in sh.get("sides", ()):
            mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
            dx, dy = P[b][0] - P[a][0], P[b][1] - P[a][1]
            L_ = _m.hypot(dx, dy)
            nx, ny = -dy / L_, dx / L_
            ref = sh.get("ref", (cx, cy))
            if (mx + nx - ref[0]) ** 2 + (my + ny - ref[1]) ** 2 < (mx - ref[0]) ** 2 + (my - ref[1]) ** 2:
                nx, ny = -nx, -ny
            anc = "middle" if abs(nx) < 0.6 else ("start" if nx > 0 else "end")
            col = RED if txt.startswith(("x", "?", "h", "y")) else BLUE
            s.append(_t(mx + nx * (16 if anc == "middle" else 8), my + ny * 16 + 5, txt, 14, col, anchor=anc))
        for k, (x, y) in P.items():
            dx, dy = x - cx, y - cy
            L_ = _m.hypot(dx, dy) or 1
            s.append(_t(x + dx / L_ * 14, y + dy / L_ * 14 + 5, k, 15))
    return _svg(W, H, "".join(s) + extra, label)


def tri_pts(a, b, c, x0, y0, sc):
    """triângulo com lados BC = a, CA = b, AB = c: B em (x0, y0), C à direita, A em cima (pixels)"""
    xa = (a * a + c * c - b * b) / (2.0 * a)
    ya = _m.sqrt(max(c * c - xa * xa, 0))
    return {"B": (x0, y0), "C": (x0 + a * sc, y0), "A": (x0 + xa * sc, y0 - ya * sc)}
