# -*- coding: utf-8 -*-
"""Türkiye 4.〜6. sınıf の共通部品（tr_run.py から setup される）。tr_s3a の unit・cap・mi・dagit・kesir_oku・fr を使う。"""
import math
from fractions import Fraction as F
import tr_s3a as A
from tr_s3a import unit, cap, mi, named, dagit, kesir_oku, fr  # noqa: F401
from tr_common import (num, dec, tl, kurus, para, oku, mcq, M, NB, Kids, wrap, text, line, table,  # noqa: F401
                       basamak_tablosu, sayi_dogrusu, sutun_grafigi, cetele, alt_alta, INK, GREEN, FILL, RED, BLUE)

R = None
K = None


def setup(rnd):
    global R, K
    R = rnd
    K = Kids(rnd)


def ri(a, b):
    return R.randint(a, b)


def ch(xs):
    return R.choice(list(xs))


def sh(xs):
    xs = list(xs)
    R.shuffle(xs)
    return xs


def near(v, ds=(10, -10, 1, -1, 100, -100)):
    return [num(v + d) for d in ds if v + d >= 0]


def ff(x, mixed=False):
    """Fraction → HTML（tam sayılı kesir için mixed=True）"""
    x = F(x)
    if x.denominator == 1:
        return num(x.numerator)
    if mixed and x > 1:
        w = x.numerator // x.denominator
        r = x - w
        return "%s%s" % (num(w), fr(r.numerator, r.denominator))
    return fr(x.numerator, x.denominator)


def mf(w, a, b):
    """tam sayılı kesir 2 3/4"""
    return "%s%s" % (num(w), fr(a, b))


def dz(x, k=None):
    """ondalık gösterim: 2,5 / 0,75（Fraction veya float）"""
    if isinstance(x, F):
        x = float(x)
    return dec(x, k)


def pct(n):
    return "%%%s" % (dec(n) if not isinstance(n, int) else num(n))


def lg(svg):
    return svg.replace("<svg ", "<svg data-pf='lg' ", 1)


# ------------------------------------------------------------ çizimler
def grid_shape(cells, c=24, col="#a8d5ba", label="birim karelerden oluşan şekil", tri=()):
    """cells: (x, y) birim kareler. tri: yarım kareler (x, y, köşe 0..3)"""
    xs = [x for x, _ in cells] + [x for x, _, _ in tri]
    ys = [y for _, y in cells] + [y for _, y, _ in tri]
    W, H = (max(xs) + 3) * c, (max(ys) + 3) * c
    s = []
    for i in range(int(W / c) + 1):
        s.append(line(i * c, 0, i * c, H, "#d5dde3", 1))
    for j in range(int(H / c) + 1):
        s.append(line(0, j * c, W, j * c, "#d5dde3", 1))
    for x, y in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>" % ((x + 1) * c, (y + 1) * c, c, c, col, GREEN))
    for x, y, k in tri:
        X, Y = (x + 1) * c, (y + 1) * c
        P = [(X, Y), (X + c, Y), (X + c, Y + c), (X, Y + c)]
        P.pop(k)
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.4'/>" % (" ".join("%d,%d" % p for p in P), col, GREEN))
    return wrap(W, H, "".join(s), label)


def poly(pts, side_labels=(), vlabels=(), unit_="cm", label="şekil", fill=FILL, ticks=(), rights=(), dashed=()):
    """Çokgen: side_labels[i] i. kenar (pts[i]→pts[i+1]); vlabels köşe harfleri; ticks: (kenar, çizgi sayısı)"""
    n = len(pts)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    ox, oy = 50 - min(xs), 30 - min(ys)
    P = [(x + ox, y + oy) for x, y in pts]
    W, H = max(xs) - min(xs) + 100, max(ys) - min(ys) + 60
    cx, cy = sum(p[0] for p in P) / n, sum(p[1] for p in P) / n
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4' stroke-linejoin='round'/>" % (" ".join("%.1f,%.1f" % p for p in P), fill, GREEN)]
    for a, b in dashed:
        s.append(line(P[a][0], P[a][1], P[b][0], P[b][1], RED, 1.8, " stroke-dasharray='6 4'"))
    for i, lab in enumerate(side_labels):
        if lab is None or lab == "":
            continue
        a, b = P[i], P[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
        nx, ny = b[1] - a[1], a[0] - b[0]
        d = math.hypot(nx, ny) or 1
        nx, ny = nx / d, ny / d
        if (mx + nx - cx) ** 2 + (my + ny - cy) ** 2 < (mx - cx) ** 2 + (my - cy) ** 2:
            nx, ny = -nx, -ny
        t = "%s%s%s" % (lab, NB, unit_) if unit_ else lab
        off = 12 + 4.2 * len(t) * abs(nx)
        s.append(text(mx + nx * off, my + ny * off + 5, t, 13, col=BLUE))
    for i, k in ticks:
        a, b = P[i], P[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        for j in range(k):
            o = (j - (k - 1) / 2.0) * 5
            px, py = mx + ux * o, my + uy * o
            s.append(line(px - uy * 7, py + ux * 7, px + uy * 7, py - ux * 7, INK, 1.8))
    for i in rights:
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        u = ((a[0] - b[0]), (a[1] - b[1]))
        v = ((c[0] - b[0]), (c[1] - b[1]))
        lu, lv = math.hypot(*u), math.hypot(*v)
        u = (u[0] / lu * 12, u[1] / lu * 12)
        v = (v[0] / lv * 12, v[1] / lv * 12)
        s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.6'/>"
                 % (b[0] + u[0], b[1] + u[1], b[0] + u[0] + v[0], b[1] + u[1] + v[1], b[0] + v[0], b[1] + v[1], INK))
    for i, lab in enumerate(vlabels):
        if not lab:
            continue
        x, y = P[i]
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy) or 1
        s.append(text(x + dx / d * 15, y + dy / d * 15 + 5, lab, 14))
    return wrap(W, H, "".join(s), label)


def circle_fig(r_lab=None, kind="r", label="çember", W=220, H=200):
    cx, cy, r = W / 2.0, H / 2.0, 78
    s = ["<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.4'/>" % (cx, cy, r, FILL, GREEN),
         "<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (cx, cy, INK), text(cx - 10, cy - 8, "O", 14)]
    if kind == "r":
        s.append(line(cx, cy, cx + r, cy, RED, 2.4))
        if r_lab:
            s.append(text(cx + r / 2.0, cy + 20, r_lab, 14, col=BLUE))
    elif kind == "d":
        s.append(line(cx - r, cy, cx + r, cy, RED, 2.4))
        if r_lab:
            s.append(text(cx + r / 2.0, cy + 20, r_lab, 14, col=BLUE))
    return wrap(W, H, "".join(s), label)


def pie_chart(cats, vals, cols=("#7fb3d5", "#f4a261", "#a8d5ba", "#e9c46a", "#e07a5f", "#b8a9d9"), label="daire grafiği"):
    tot = float(sum(vals))
    cx, cy, r = 110, 110, 96
    s = []
    a = -math.pi / 2
    for i, v in enumerate(vals):
        b = a + 2 * math.pi * v / tot
        big = 1 if b - a > math.pi else 0
        if v == tot:
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx, cy, r, cols[i], INK))
        else:
            s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (cx, cy, cx + r * math.cos(a), cy + r * math.sin(a), r, r, big, cx + r * math.cos(b), cy + r * math.sin(b), cols[i], INK))
        a = b
    for i, c in enumerate(cats):
        y = 30 + i * 26
        s.append("<rect x='232' y='%d' width='16' height='16' fill='%s' stroke='%s'/>" % (y - 13, cols[i], INK))
        s.append(text(256, y, c, 14, anchor="start", weight=600))
    return wrap(400, max(224, 30 + len(cats) * 26), "".join(s), label)


def parallel_fig(theta, labels, vals=None, label="iki paralel doğru ve bir kesen"):
    """d1 // d2 yatay; kesen açısı theta (derece, 0–180). labels: {köşe kodu: metin}.
    Köşe kodları: 1 sağ üst, 2 sol üst, 3 sol alt, 4 sağ alt (üst kesişim); 5–8 aynı sırayla alt kesişim."""
    W, H = 360, 230
    y1, y2 = 70, 160
    t = math.radians(theta)
    ux, uy = math.cos(t), -math.sin(t)
    x1 = 190 + (115 - y1) / math.tan(t) if abs(math.tan(t)) > 1e-6 else 190
    x2 = 190 + (115 - y2) / math.tan(t) if abs(math.tan(t)) > 1e-6 else 190
    s = [line(20, y1, W - 20, y1, INK, 2.2), line(20, y2, W - 20, y2, INK, 2.2),
         text(W - 12, y1 - 8, "d<tspan font-size='10' dy='3'>1</tspan>", 14, anchor="end"),
         text(W - 12, y2 - 8, "d<tspan font-size='10' dy='3'>2</tspan>", 14, anchor="end")]
    L = 95
    s.append(line(x1 + ux * L, y1 + uy * L, x2 - ux * L, y2 - uy * L, GREEN, 2.4))
    for (X, Y, base) in ((x1, y1, 1), (x2, y2, 5)):
        dirs = {0: 0.0, 1: theta, 2: 180.0, 3: theta + 180.0}
        # bölgeler: 1 sağ üst (0..theta), 2 sol üst (theta..180), 3 sol alt (180..theta+180), 4 sağ alt
        regions = [(0.0, theta), (theta, 180.0), (180.0, theta + 180.0), (theta + 180.0, 360.0)]
        for k, (a0, a1) in enumerate(regions):
            code = base + k
            if code not in labels:
                continue
            m = math.radians((a0 + a1) / 2.0)
            rr = 30 if a1 - a0 > 50 else 40
            s.append(text(X + rr * math.cos(m), Y - rr * math.sin(m) + 5, labels[code], 14, col=RED))
    return wrap(W, H, "".join(s), label)


def stem_leaf(data):
    st = {}
    for v in sorted(data):
        st.setdefault(v // 10, []).append(v % 10)
    rows = [[str(k), " ".join(str(x) for x in st.get(k, []))] for k in range(min(st), max(st) + 1)]
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>Gövde</th><th>Yaprak</th></tr></thead><tbody>%s</tbody></table>"
            % "".join("<tr><td style='text-align:center'>%s</td><td style='letter-spacing:4px'>%s</td></tr>" % (a, b) for a, b in rows))


def freq_table(head, cats, vals):
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>%s</th><th>Sıklık</th></tr></thead><tbody>%s</tbody></table>"
            % (head, "".join("<tr><td>%s</td><td style='text-align:center'>%s</td></tr>" % (c, num(v)) for c, v in zip(cats, vals))))


def dot_plot(lo, hi, data, label="nokta grafiği"):
    step = 34
    W = 40 + (hi - lo) * step + 20
    cnt = {v: data.count(v) for v in range(lo, hi + 1)}
    H = 50 + max(cnt.values()) * 18
    y0 = H - 30
    s = [line(20, y0, W - 10, y0, INK, 2)]
    for v in range(lo, hi + 1):
        x = 40 + (v - lo) * step
        s.append(line(x, y0, x, y0 + 6, INK, 1.5) + text(x, y0 + 22, str(v), 13))
        for k in range(cnt[v]):
            s.append("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x, y0 - 12 - k * 18, BLUE, INK))
    return wrap(W, H, "".join(s), label, lg=True)


def withopts(d, lead):
    """seçenekleri soru metnine ekler: '12, 15, 21 ve 27 sayılarından hangisi …'"""
    if not d:
        return d
    import re as _re
    def key(c):
        t = _re.sub(r"<[^>]+>", "", c).replace(".", "").replace(",", ".")
        m = _re.match(r"^\d+(\.\d+)?", t)
        return (0, float(m.group(0))) if m else (1, t)
    cs = sorted(d["c"], key=key)
    d = dict(d)
    d["q"] = lead % (", ".join(cs[:-1]) + " ve " + cs[-1]) + " " + d["q"]
    return d
