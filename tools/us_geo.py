# -*- coding: utf-8 -*-
"""
Drawing helpers for US Geometry figures (inline SVG, single-quoted attributes, no backslashes).
Coordinates are screen pixels (y grows downward). Build a figure with Canvas, add parts, then call
svg(label); the viewBox is fitted to everything that was added.
"""
import math
import re
from ws_common import INK, GREEN, RED, BLUE, FILL, FONT

SOFT = "#eef6f0"


def _u(ax, ay, bx, by):
    d = math.hypot(bx - ax, by - ay) or 1
    return (bx - ax) / d, (by - ay) / d


class Canvas:
    def __init__(self):
        self.el = []
        self.pts = []

    def _p(self, *ps):
        self.pts += [tuple(p) for p in ps]

    # ---------------------------------------------------- basic parts
    def poly(self, ps, fill=SOFT, col=INK, w=2.5):
        d = "M" + " L".join("%.1f %.1f" % p for p in ps) + " Z"
        self.el.append("<path d='%s' fill='%s' stroke='%s' stroke-width='%s' stroke-linejoin='round'/>" % (d, fill, col, w))
        self._p(*ps)

    def seg(self, a, b, col=INK, w=2.5, dash=False):
        self.el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'%s stroke-linecap='round'/>" % (
            a[0], a[1], b[0], b[1], col, w, " stroke-dasharray='6 5'" if dash else ""))
        self._p(a, b)

    def head(self, tip, frm, col=INK, size=10):
        ux, uy = _u(frm[0], frm[1], tip[0], tip[1])
        px, py = -uy, ux
        b1 = (tip[0] - ux * size + px * size * 0.5, tip[1] - uy * size + py * size * 0.5)
        b2 = (tip[0] - ux * size - px * size * 0.5, tip[1] - uy * size - py * size * 0.5)
        self.el.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>" % (tip[0], tip[1], b1[0], b1[1], b2[0], b2[1], col))
        self._p(tip)

    def ray(self, a, b, ext=40, col=INK, w=2.5):
        """from a through b and beyond, with an arrowhead"""
        ux, uy = _u(a[0], a[1], b[0], b[1])
        e = (b[0] + ux * ext, b[1] + uy * ext)
        self.seg(a, e, col, w)
        self.head(e, a, col)

    def fullline(self, a, b, ext=40, col=INK, w=2.5):
        ux, uy = _u(a[0], a[1], b[0], b[1])
        e1 = (a[0] - ux * ext, a[1] - uy * ext)
        e2 = (b[0] + ux * ext, b[1] + uy * ext)
        self.seg(e1, e2, col, w)
        self.head(e1, e2, col)
        self.head(e2, e1, col)
        return e1, e2

    def dot(self, p, r=4.5, col=INK, hollow=False):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (
            p[0], p[1], r, "#fff" if hollow else col, col))
        self._p(p)

    def circle(self, c, r, col=INK, w=2.5, fill="none"):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%s'/>" % (c[0], c[1], r, fill, col, w))
        self._p((c[0] - r, c[1] - r), (c[0] + r, c[1] + r))

    def path(self, d, col=INK, w=2.5, fill="none", pts=()):
        self.el.append("<path d='%s' fill='%s' stroke='%s' stroke-width='%s'/>" % (d, fill, col, w))
        self._p(*pts)

    def text(self, p, t, fs=16, col=INK, anchor="middle", italic=False, weight=700):
        plain = re.sub("<[^>]+>", "", t)
        t = t.replace("<i>", "<tspan font-style='italic'>").replace("</i>", "</tspan>")
        t = t.replace("<sup>", "<tspan font-size='%d' dy='-%d'>" % (fs * 0.7, fs * 0.35)).replace("</sup>", "</tspan>")
        self.el.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'%s>%s</text>" % (
            p[0], p[1] + fs * 0.35, fs, weight, col, anchor, " font-style='italic'" if italic else "", t))
        w = fs * 0.6 * len(plain.replace("&lt;", "<"))
        x0 = p[0] - (w / 2 if anchor == "middle" else (w if anchor == "end" else 0))
        self._p((x0, p[1] - fs * 0.6), (x0 + w, p[1] + fs * 0.6))

    # ---------------------------------------------------- labels and marks
    def vlabel(self, p, name, center, gap=16, fs=16, col=INK):
        ux, uy = _u(center[0], center[1], p[0], p[1])
        self.text((p[0] + ux * gap, p[1] + uy * gap), name, fs, col)

    def vlabels(self, ps, names, gap=16, fs=16):
        cx = sum(p[0] for p in ps) / len(ps)
        cy = sum(p[1] for p in ps) / len(ps)
        for p, n in zip(ps, names):
            if n:
                self.vlabel(p, n, (cx, cy), gap, fs)

    def side_label(self, a, b, t, center, gap=16, fs=15, col=INK, italic=False):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = -(b[1] - a[1]), b[0] - a[0]
        d = math.hypot(nx, ny) or 1
        nx, ny = nx / d, ny / d
        if (mx + nx - center[0]) ** 2 + (my + ny - center[1]) ** 2 < (mx - nx - center[0]) ** 2 + (my - ny - center[1]) ** 2:
            nx, ny = -nx, -ny
        self.text((mx + nx * gap, my + ny * gap), t, fs, col, italic=italic)

    def arc(self, v, a, b, r=26, col=GREEN, n=1, w=2):
        a1 = math.atan2(a[1] - v[1], a[0] - v[0])
        a2 = math.atan2(b[1] - v[1], b[0] - v[0])
        d = (a2 - a1) % (2 * math.pi)
        if d > math.pi:
            a1, a2 = a2, a1
            d = 2 * math.pi - d
        for k in range(n):
            rr = r + k * 5
            p1 = (v[0] + rr * math.cos(a1), v[1] + rr * math.sin(a1))
            p2 = (v[0] + rr * math.cos(a1 + d), v[1] + rr * math.sin(a1 + d))
            self.el.append("<path d='M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f' fill='none' stroke='%s' stroke-width='%s'/>" % (
                p1[0], p1[1], rr, rr, p2[0], p2[1], col, w))

    def angle_text(self, v, a, b, t, r=44, fs=14, col=INK, italic=False):
        a1 = math.atan2(a[1] - v[1], a[0] - v[0])
        a2 = math.atan2(b[1] - v[1], b[0] - v[0])
        d = (a2 - a1) % (2 * math.pi)
        if d > math.pi:
            a1, d = a2, 2 * math.pi - d
        m = a1 + d / 2
        rr = r + max(0, 22 - math.degrees(d)) * 1.2
        self.text((v[0] + rr * math.cos(m), v[1] + rr * math.sin(m)), t, fs, col, italic=italic)

    def angle(self, v, a, b, t="", r=24, n=1, col=GREEN, tr=None, fs=14, tcol=INK):
        self.arc(v, a, b, r, col, n)
        if t:
            self.angle_text(v, a, b, t, tr or r + 20, fs, tcol)

    def right(self, v, a, b, s=13, col=GREEN):
        ux, uy = _u(v[0], v[1], a[0], a[1])
        wx, wy = _u(v[0], v[1], b[0], b[1])
        p1 = (v[0] + ux * s, v[1] + uy * s)
        p2 = (p1[0] + wx * s, p1[1] + wy * s)
        p3 = (v[0] + wx * s, v[1] + wy * s)
        self.el.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>" % (
            p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], col))

    def ticks(self, a, b, n=1, col=RED, s=8):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ux, uy = _u(a[0], a[1], b[0], b[1])
        px, py = -uy, ux
        for k in range(n):
            o = (k - (n - 1) / 2) * 6
            cx, cy = mx + ux * o, my + uy * o
            self.el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (
                cx - px * s, cy - py * s, cx + px * s, cy + py * s, col))

    def chevrons(self, a, b, n=1, col=BLUE, s=8):
        """parallel marks (arrowheads) at the middle of a segment"""
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ux, uy = _u(a[0], a[1], b[0], b[1])
        px, py = -uy, ux
        for k in range(n):
            o = (k - (n - 1) / 2) * 8 + 4
            tx, ty = mx + ux * o, my + uy * o
            self.el.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (
                tx - ux * s + px * s * 0.7, ty - uy * s + py * s * 0.7, tx, ty, tx - ux * s - px * s * 0.7, ty - uy * s - py * s * 0.7, col))

    # ---------------------------------------------------- output
    def svg(self, label, pad=12, big=False):
        xs = [p[0] for p in self.pts]
        ys = [p[1] for p in self.pts]
        x0, y0 = min(xs) - pad, min(ys) - pad
        w, h = max(xs) - x0 + pad, max(ys) - y0 + pad
        return ("<svg xmlns='http://www.w3.org/2000/svg'%s viewBox='0 0 %.0f %.0f' width='%.0f' height='%.0f' role='img' "
                "aria-label='%s'><g font-family='%s' transform='translate(%.1f %.1f)'>%s</g></svg>" % (
                    " data-pf='lg'" if big else "", w, h, w, h, label, FONT, -x0, -y0, "".join(self.el)))


def pol(cx, cy, r, deg):
    """point at distance r and angle deg (counterclockwise from east, as on paper)"""
    t = math.radians(deg)
    return (cx + r * math.cos(t), cy - r * math.sin(t))


def deg(v):
    from ws_common import num
    return "%s°" % num(v)
