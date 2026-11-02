# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Triangles (MOE 2021 Primary Mathematics Syllabus, Standard; Primary 5: Geometry)
  python3 tools/gen_sg_maths_p5_triangles.py
Properties of isosceles, equilateral and right-angled triangles (tick marks, right-angle marks),
the angle sum of a triangle (180°), base angles of an isosceles triangle, 60° in an equilateral triangle,
the two acute angles of a right-angled triangle (90° together), and unknown angles in figures with straight lines.

Every figure is drawn to its data and checked in code: each angle written on a figure is the real angle of the
drawing, tick marks and right-angle marks are computed from the coordinates, and sides that look equal are equal.
Wrong answers come from real student mistakes: subtracting from 360° or 90°, subtracting only one known angle,
forgetting the right angle, not halving (or halving wrongly) in an isosceles triangle, choosing the wrong pair of
equal angles, a right-angled triangle with two right angles, and taking the exterior angle as the interior angle.
HTML attributes use single quotes (no backslashes in the JSON). Singapore (British) English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
BARFILL = "#9fd3b4"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
FS = 15


# ------------------------------------------------------------ helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {plain(correct)}
    pick = []
    for c in cands:
        c = str(c)
        if not c or plain(c) in seen:
            continue
        seen.add(plain(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D). The answer position is not moved later."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def balance(sets, rnd):
    """Spread the correct answers evenly (5 per position per set). Fixed-order questions stay as they are."""
    for s in sets:
        cnt, free = [0] * 4, []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        targets = []
        for p in range(4):
            assert cnt[p] <= 5, (s["title"], cnt)
            targets += [p] * (5 - cnt[p])
        assert len(targets) == len(free)
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]


class Spots:
    """Answer letters for A-D picture questions: each letter used about equally often."""
    def __init__(self, rnd):
        self.rnd, self.left = rnd, []

    def next(self):
        if not self.left:
            self.left = [0, 1, 2, 3]
            self.rnd.shuffle(self.left)
        return self.left.pop()


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def D(x):
    return "%d°" % x


# Arial Bold advance widths (per 1000 units of font size), for laying out text without a browser
AW = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611,
                                              611, 389, 556, 333, 611, 556, 778, 556, 556, 500]))
AW.update(dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778, 667,
                                                  778, 722, 667, 611, 722, 667, 944, 667, 667, 611])))
AW.update({c: 556 for c in "0123456789"})
AW.update({" ": 278, ".": 278, "°": 400, "?": 611, ",": 278, "∠": 720, "-": 333})


def tw(t, fs):
    """Width of bold Arial text, plus 5% for safety."""
    return sum(AW[c] for c in t) * fs / 1000.0 * 1.05


def svg_text(x, y, t, fs=FS, color=INK, anchor="middle"):
    """One text element. A single small letter (an unknown angle such as x) is written in italics."""
    inner = "<tspan font-style='italic'>%s</tspan>" % t if re.fullmatch(r"[a-z]", t) else t
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, color, anchor, inner))


def text_box(x, y, t, fs=FS, color=INK):
    """Text centred on (x, y). Returns the element and its box."""
    w = tw(t, fs)
    return svg_text(x, y + 0.36 * fs, t, fs, color), (x - w / 2, y - 0.37 * fs - 1, x + w / 2, y + 0.37 * fs + 1)


# ------------------------------------------------------------ geometry
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def angle_at(v, a, b):
    u1, u2 = norm(sub(a, v)), norm(sub(b, v))
    return math.degrees(math.acos(max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))))


def seg_dist(p, a, b):
    ab, ap = sub(b, a), sub(p, a)
    L2 = ab[0] ** 2 + ab[1] ** 2
    t = max(0.0, min(1.0, (ap[0] * ab[0] + ap[1] * ab[1]) / L2)) if L2 else 0.0
    return dist(p, (a[0] + ab[0] * t, a[1] + ab[1] * t))


def inside(p, poly):
    n = len(poly)
    sg = [cross(sub(poly[(i + 1) % n], poly[i]), sub(p, poly[i])) for i in range(n)]
    return all(x > 0 for x in sg) or all(x < 0 for x in sg)


def box_pts(b):
    x0, y0, x1, y1 = b
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    return [(x0, y0), (x1, y0), (x0, y1), (x1, y1), (xm, y0), (xm, y1), (x0, ym), (x1, ym)]


def boxes_apart(a, b, gap=2):
    return a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1]


def groups_of(L):
    groups = []
    for i, x in enumerate(L):
        for g in groups:
            if close(L[g[0]], x):
                g.append(i)
                break
        else:
            groups.append([i])
    return groups


def tri_ang(a, b, base=120.0):
    """Triangle (y down) with angle a at vertex 0 (left end of the base), angle b at vertex 1 (right end), top vertex 2."""
    c = 180 - a - b
    assert c > 0
    side = base * math.sin(math.radians(b)) / math.sin(math.radians(c))
    t = math.radians(a)
    return [(0.0, 0.0), (float(base), 0.0), (side * math.cos(t), -side * math.sin(t))]


def tri_sides(base, right, left):
    """Triangle with the given base, right side (vertex 1 to the top) and left side (vertex 0 to the top)."""
    x = (base ** 2 + left ** 2 - right ** 2) / (2.0 * base)
    y = math.sqrt(left ** 2 - x ** 2)
    return [(0.0, 0.0), (float(base), 0.0), (x, -y)]


def tri_kind(pts):
    """'equilateral' | 'right isosceles' | 'isosceles' | 'right' | 'other', from the coordinates."""
    L = [dist(pts[(i + 1) % 3], pts[i]) for i in range(3)]
    A = [angle_at(pts[i], pts[i - 1], pts[(i + 1) % 3]) for i in range(3)]
    big = max(len(g) for g in groups_of(L))
    right = any(abs(a - 90) < 1e-6 for a in A)
    if big == 3:
        return "equilateral"
    if right:
        return "right isosceles" if big == 2 else "right"
    return "isosceles" if big == 2 else "other"


# ------------------------------------------------------------ figure engine
class Fig:
    """A figure from named points (model coordinates, y down). Filled triangles get automatic tick marks for equal
    sides and right-angle marks; angle labels are placed inside their angle, vertex letters outside the lines.
    Every number written on the figure is checked against the drawing."""

    def __init__(self, P):
        self.P = dict(P)
        self.polys, self.segs, self.angs, self.sides, self.letters = [], [], [], [], []

    def poly(self, names, ticks=True, rights=True):
        self.polys.append((names, ticks, rights))
        return self

    def seg(self, a, b):
        self.segs.append((a, b))
        return self

    def ang(self, v, a, b, text, value=None):
        """Angle a-v-b labelled with text ('65°', 'x', '?'). value is its size in degrees (needed for x and ?)."""
        if value is None:
            value = int(text.rstrip("°"))
        self.angs.append((v, a, b, text, value))
        return self

    def side(self, a, b, text):
        self.sides.append((a, b, text))
        return self

    def letter(self, *names):
        self.letters += list(names)
        return self

    def build(self, bw, bh, rot=0, sw=3.0):
        """Elements and bounding box, with the figure scaled into bw x bh around (0, 0)."""
        t = math.radians(rot)
        R = {k: (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t)) for k, p in self.P.items()}
        xs, ys = [p[0] for p in R.values()], [p[1] for p in R.values()]
        k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
        mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        P = {n: ((p[0] - mx) * k, (p[1] - my) * k) for n, p in R.items()}
        Q = lambda ps: " ".join("%.1f,%.1f" % p for p in ps)
        el, marks, texts, segs, boxes, extent = [], [], [], [], [], list(P.values())
        mk = "stroke='%s' stroke-width='2' fill='none' stroke-linecap='round'" % INK
        polys = []
        right_at = set()
        for names, ticks, rights in self.polys:
            pts = [P[n] for n in names]
            polys.append(pts)
            n = len(pts)
            el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (Q(pts), FILL, GREEN, sw))
            segs += [(pts[i], pts[(i + 1) % n]) for i in range(n)]
            L = [dist(pts[(i + 1) % n], pts[i]) for i in range(n)]
            G = groups_of(L)
            if ticks:
                for g1 in G:
                    for g2 in G:
                        if g1 is not g2:
                            a, b = L[g1[0]], L[g2[0]]
                            assert abs(a - b) / max(a, b) > 0.09, L          # sides that look equal must be equal
                for g in G:
                    if len(g) < 2:
                        continue
                    for i in g:
                        a, b = pts[i], pts[(i + 1) % n]
                        d = norm(sub(b, a))
                        nr = (-d[1], d[0])
                        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                        p1, p2 = (m[0] - nr[0] * 6, m[1] - nr[1] * 6), (m[0] + nr[0] * 6, m[1] + nr[1] * 6)
                        marks.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' %s/>" % (p1 + p2 + (mk,)))
                        segs.append((p1, p2))
                        extent += [p1, p2]
            for i in range(n):
                v = pts[i]
                A = angle_at(v, pts[i - 1], pts[(i + 1) % n])
                if abs(A - 90) < 1e-6:
                    if rights:
                        right_at.add(names[i])
                        u1, u2 = norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % n], v))
                        kk = min(11, 0.2 * min(L[i - 1], L[i]))
                        q1 = (v[0] + u1[0] * kk, v[1] + u1[1] * kk)
                        q2 = (q1[0] + u2[0] * kk, q1[1] + u2[1] * kk)
                        q3 = (v[0] + u2[0] * kk, v[1] + u2[1] * kk)
                        marks.append("<polyline points='%s' %s/>" % (Q([q1, q2, q3]), mk.replace("stroke-width='2'", "stroke-width='1.6'")))
                        segs += [(q1, q2), (q2, q3)]
                else:
                    assert abs(A - 90) >= 10, (names, A)                  # nothing that looks like a right angle but is not
        for a, b in self.segs:
            el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'/>"
                      % (P[a] + P[b] + (GREEN, sw)))
            segs.append((P[a], P[b]))
        # side labels, outside the polygon
        for a, b, t in self.sides:
            pa, pb = P[a], P[b]
            m = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
            d = norm(sub(pb, pa))
            nr = (-d[1], d[0])
            probe = (m[0] + nr[0] * 3, m[1] + nr[1] * 3)
            if any(inside(probe, pl) for pl in polys):
                nr = (-nr[0], -nr[1])
            w, hh = tw(t, FS) / 2, 0.37 * FS + 1
            off = abs(nr[0]) * w + abs(nr[1]) * hh + 5
            e, bx = text_box(m[0] + nr[0] * off, m[1] + nr[1] * off, t)
            texts.append(e)
            boxes.append(bx)
        # angle labels: arc + text inside the angle
        order = sorted(self.angs, key=lambda x: -angle_at(P[x[0]], P[x[1]], P[x[2]]))
        arcs = []
        for v, a, b, t, val in order:
            pv, pa, pb = P[v], P[a], P[b]
            A = angle_at(pv, pa, pb)
            assert abs(A - val) < 1e-6, (v, a, b, t, val, A)
            assert v not in right_at
            u1, u2 = norm(sub(pa, pv)), norm(sub(pb, pv))
            cr = cross(u1, u2)
            r_arc = 15
            a1, a2 = (pv[0] + u1[0] * r_arc, pv[1] + u1[1] * r_arc), (pv[0] + u2[0] * r_arc, pv[1] + u2[1] * r_arc)
            marks.append("<path d='M%.1f,%.1f A%d,%d 0 0 %d %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
                         % (a1[0], a1[1], r_arc, r_arc, 1 if cr > 0 else 0, a2[0], a2[1], RED))
            th1 = math.atan2(u1[1], u1[0])
            dth = math.atan2(cr, u1[0] * u2[0] + u1[1] * u2[1])
            arc_pts = [(pv[0] + math.cos(th1 + dth * f / 12.0) * r_arc, pv[1] + math.sin(th1 + dth * f / 12.0) * r_arc) for f in range(13)]
            arcs.append(arc_pts)
            extent += arc_pts
            mid = th1 + dth * 0.5
            near = (pv[0] + math.cos(mid) * 6, pv[1] + math.sin(mid) * 6)
            region = [pl for pl in polys if inside(near, pl)]
            fracs = sorted([f / 20.0 for f in range(3, 18)], key=lambda f: abs(f - 0.5))
            found = None
            max_r = 46 + int(max(0, 50 - A) * 4)     # stay close to the vertex, or the label reads as another angle
            for r in range(18, max_r):
                for f in fracs:
                    th = th1 + dth * f
                    p = (pv[0] + math.cos(th) * r, pv[1] + math.sin(th) * r)
                    e, bx = text_box(p[0], p[1], t, color=RED)
                    probe = box_pts(bx)
                    if region and not all(inside(q, region[0]) for q in probe):
                        continue
                    ok = True
                    for q in probe:
                        w = sub(q, pv)
                        if cross(u1, w) * cr <= 0 or cross(w, u2) * cr <= 0:
                            ok = False
                            break
                    if not ok:
                        continue
                    if min(seg_dist(q, s0, s1) for q in probe for s0, s1 in segs) < 3:
                        continue
                    if min(dist(q, pv) for q in probe) < r_arc + 3:
                        continue
                    if not all(boxes_apart(bx, o, 4) for o in boxes):
                        continue
                    found = (e, bx)
                    break
                if found:
                    break
            assert found, ("no room for angle label", t, A)
            texts.append(found[0])
            boxes.append(found[1])
        arc_segs = [(ap[i], ap[i + 1]) for ap in arcs for i in range(len(ap) - 1)]
        # vertex letters, outside the lines
        for n in self.letters:
            p = P[n]
            nb = []
            for names, _, _ in self.polys:
                if n in names:
                    i = names.index(n)
                    nb += [P[names[i - 1]], P[names[(i + 1) % len(names)]]]
            for a, b in self.segs:
                if a == n:
                    nb.append(P[b])
                if b == n:
                    nb.append(P[a])
            sx = sum(norm(sub(q, p))[0] for q in nb)
            sy = sum(norm(sub(q, p))[1] for q in nb)
            base = math.atan2(-sy, -sx) if math.hypot(sx, sy) > 1e-6 else -math.pi / 2
            found = None
            for r in range(10, 36):
                for dd in [0] + [s * k for k in range(10, 180, 10) for s in (1, -1)]:
                    th = base + math.radians(dd)
                    q = (p[0] + math.cos(th) * r, p[1] + math.sin(th) * r)
                    e, bx = text_box(q[0], q[1], n)
                    probe = box_pts(bx)
                    if any(inside(z, pl) for z in probe for pl in polys):
                        continue
                    if min(seg_dist(z, s0, s1) for z in probe for s0, s1 in segs + arc_segs) < 2.5:
                        continue
                    if not all(boxes_apart(bx, o, 3) for o in boxes):
                        continue
                    found = (e, bx)
                    break
                if found:
                    break
            assert found, ("no room for letter", n)
            texts.append(found[0])
            boxes.append(found[1])
        for bx in boxes:
            extent += [(bx[0], bx[1]), (bx[2], bx[3])]
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                assert boxes_apart(boxes[i], boxes[j]), "labels overlap"
        pad = sw / 2.0 + 1
        bb = (min(p[0] for p in extent) - pad, min(p[1] for p in extent) - pad,
              max(p[0] for p in extent) + pad, max(p[1] for p in extent) + pad)
        return el + marks + texts, bb

    def svg(self, bw=140, bh=95, rot=0, label="triangle"):
        for grow in (1.0, 1.12, 1.25, 1.4, 1.6, 1.8, 2.0):
            try:
                el, bb = self.build(bw * grow, bh * grow, rot)
                break
            except AssertionError as err:
                if "no room" not in str(err) or grow == 2.0:
                    raise
        pad = 5
        W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
        if W == H:
            W += 1                                       # keep figures out of the larger 'square' print size
        dx = (W - (bb[2] - bb[0])) / 2 - bb[0]
        dy = (H - (bb[3] - bb[1])) / 2 - bb[1]
        return svg_wrap(W, H, "<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, "".join(el)), label)


def tri_fig(model, names="ABC", ticks=True, angs=(), sides=(), letters=False):
    """Fig of one triangle. model points are given for names[0], names[1], names[2] (base left, base right, top)."""
    f = Fig(dict(zip(names, model))).poly(list(names), ticks=ticks)
    for a in angs:
        f.ang(*a)
    for s in sides:
        f.side(*s)
    if letters:
        f.letter(*names)
    return f


CELL = 118


def grid_svg(models, label="four triangles labelled A to D"):
    """2 x 2 grid of triangles (model, rot) labelled A-D. Square picture (printed large)."""
    el = []
    W = H = 2 * CELL
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY))
    el.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY))
    for k, (model, rot) in enumerate(models):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        cx, cy = x0 + 67, y0 + 62
        e, bb = tri_fig(model).build(78, 78, rot, sw=2.6)
        assert bb[0] + cx >= x0 + 20 and bb[1] + cy >= y0 + 4 and bb[2] + cx <= x0 + CELL - 3 and bb[3] + cy <= y0 + CELL - 3, bb
        el.append("<g transform='translate(%d,%d)'>%s</g>" % (cx, cy, "".join(e)))
        el.append(svg_text(x0 + 6, y0 + 22, "ABCD"[k], 18, INK, "start"))
    return svg_wrap(W, H, "".join(el), label)


def strip_svg(items, label, cw=140, top=118):
    """Lesson figure: a row of figures with a caption under each. items: (Fig, rot, caption, bw, bh)."""
    el = []
    for k, (f, rot, cap, bw, bh) in enumerate(items):
        cx, cy = k * cw + cw / 2.0, top / 2.0
        e, bb = f.build(bw, bh, rot, sw=2.8)
        assert bb[0] + cx >= k * cw + 2 and bb[2] + cx <= (k + 1) * cw - 2 and bb[1] + cy >= 2 and bb[3] + cy <= top - 2, (cap, bb)
        assert tw(cap, 15) <= cw - 4, cap
        el.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (cx, cy, "".join(e)))
        el.append(svg_text(cx, top + 16, cap, 15))
    return svg_wrap(int(cw * len(items)), top + 24, "".join(el), label)


def bar2_svg(top_units, bot_units, total, top_lab, bot_lab, ask_row):
    """Two-row bar model: top_lab has top_units units, bot_lab has bot_units units; a bracket on the right shows the total.
    The row named by ask_row ('top' or 'bot') gets a bracket and a red '?' (above the top bar or below the bottom bar)."""
    unit, L, bh = 46, 52, 32
    y_top = 40 if ask_row == "top" else 10
    y_bot = y_top + bh + 14
    s = []
    rows = {"top": (top_lab, top_units, y_top), "bot": (bot_lab, bot_units, y_bot)}
    for lab, n, y in rows.values():
        s.append(svg_text(L - 10, y + 22, lab, 15, INK, "end"))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (L, y, n * unit, bh, BARFILL))
        for i in range(1, n):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (L + i * unit, y, L + i * unit, y + bh, INK))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (L, y, n * unit, bh, INK))
    R = L + max(top_units, bot_units) * unit + 10
    s.append("<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2'/>"
             % (R, y_top, R + 8, y_top, R + 8, y_bot + bh, R, y_bot + bh, INK))
    s.append(svg_text(R + 14, (y_top + y_bot + bh) / 2.0 + 5, total, 16, INK, "start"))
    lab, n, y = rows[ask_row]
    xa, xb = L, L + n * unit
    if ask_row == "top":
        s.append("<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, y - 4, xa, y - 11, xb, y - 11, xb, y - 4, RED))
        s.append(svg_text((xa + xb) / 2.0, y - 17, "?", 18, RED))
        H = y_bot + bh + 6
    else:
        yb = y + bh
        s.append("<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, yb + 4, xa, yb + 11, xb, yb + 11, xb, yb + 4, RED))
        s.append(svg_text((xa + xb) / 2.0, yb + 32, "?", 18, RED))
        H = yb + 40
    W = int(R + 14 + tw(total, 16) + 8)
    return svg_wrap(W, H, "".join(s), "bar model: %s is %d units, %s is %d units, %s in all" % (top_lab, top_units, bot_lab, bot_units, total))


# ------------------------------------------------------------ triangles used in pictures
EQUI = tri_ang(60, 60)
ISO_AC = tri_ang(70, 70)
ISO_AC2 = tri_ang(65, 65)
ISO_RT = tri_ang(45, 45)
ISO_OB = tri_ang(30, 30)
ISO_OB2 = tri_ang(25, 25)
SCA_AC = tri_ang(50, 72)
SCA_AC2 = tri_ang(40, 62)
SCA_RT = tri_ang(90, 35)
SCA_RT2 = tri_ang(58, 90)
SCA_OB = tri_ang(25, 42)

NAMES = ["isosceles triangle", "equilateral triangle", "right-angled triangle", "right-angled isosceles triangle"]
KIND_NAME = {"isosceles": NAMES[0], "equilateral": NAMES[1], "right": NAMES[2], "right isosceles": NAMES[3]}
KIND_E = {
    "isosceles": "Two sides have tick marks, so exactly 2 sides are equal. It has no right angle. It is an isosceles triangle.",
    "equilateral": "All 3 sides have tick marks, so all 3 sides are equal. It is an equilateral triangle.",
    "right": "The small square marks a right angle (90°). No sides are equal, so it is a right-angled triangle.",
    "right isosceles": "It has a right angle (the small square) and 2 equal sides (tick marks), so it is a right-angled isosceles triangle.",
}


# ------------------------------------------------------------ set 1: classify triangles
def set_classify(rnd, spots):
    its = []
    q = "Which is the best name for this triangle?"
    pics = [
        (ISO_AC, 0, "isosceles", "The base has no tick mark."),
        (EQUI, 180, "equilateral", "Pointing down does not change its name."),
        (SCA_RT, 0, "right", ""),
        (ISO_RT, 0, "right isosceles", "The 2 equal sides are the arms of the right angle."),
        (ISO_OB, 90, "isosceles", "It lies on its side, but 2 sides still have tick marks. Turning a triangle never changes its name."),
        (SCA_RT2, 160, "right", "It is turned, but the small square still shows the right angle."),
        (ISO_RT, 135, "right isosceles", "It is turned, but the marks do not change."),
        (EQUI, 90, "equilateral", "It is turned on its side, but all 3 sides are still equal."),
    ]
    for model, rot, kind, extra in pics:
        assert tri_kind(model) == kind
        svg = tri_fig(model).svg(120, 85, rot, label="triangle with marks")
        its.append(mcq_fixed(fig(svg) + q, NAMES, KIND_NAME[kind], (KIND_E[kind] + " " + extra).strip()))
    # lengths written on the picture (drawn to scale)
    lens = [
        ((6, 6, 4), 0, "isosceles", "Two sides are 6 cm, so exactly 2 sides are equal. The equal sides do not have to be the slanted ones."),
        ((5, 5, 5), 0, "equilateral", "All 3 sides are 5 cm."),
        ((4, 7.5, 7.5), 180, "isosceles", "Two sides are 7.5 cm. It points down, but it is still isosceles."),
    ]
    for (b, r, l), rot, kind, e in lens:
        model = tri_sides(b, r, l)
        assert tri_kind(model) == kind
        fmt = lambda x: ("%g" % x) + " cm"
        svg = tri_fig(model, ticks=False, sides=[("A", "B", fmt(b)), ("B", "C", fmt(r)), ("C", "A", fmt(l))]).svg(
            120, 80, rot, label="triangle with side lengths")
        its.append(mcq_fixed(fig(svg) + q, NAMES, KIND_NAME[kind], e))
    # A-D pictures
    grids = [
        ("Which triangle is an isosceles triangle?", (ISO_AC, 200), [(SCA_AC2, 0), (SCA_RT, 0), (SCA_OB, 0)], "isosceles",
         "has tick marks on 2 sides, so it is isosceles, even though it points down. The other triangles have no equal sides."),
        ("Which triangle is a right-angled triangle?", (SCA_RT, 120), [(SCA_AC, 0), (ISO_OB, 0), (EQUI, 0)], "right",
         "has a small square in one corner, so one angle is 90°. It is turned, but it is still right-angled."),
        ("Which triangle is an equilateral triangle?", (EQUI, 90), [(ISO_AC2, 0), (ISO_OB2, 0), (ISO_RT, 0)], "equilateral",
         "has tick marks on all 3 sides. The other triangles have only 2 equal sides."),
    ]
    for q2, good, others, kind, why in grids:
        assert tri_kind(good[0]) == kind
        for m, _ in others:
            assert tri_kind(m) != kind
        if kind == "isosceles":
            assert all(tri_kind(m) == "other" or tri_kind(m) == "right" for m, _ in others)
        if kind == "right":
            assert all("right" not in tri_kind(m) for m, _ in others)
        p = spots.next()
        cells = others[:]
        rnd.shuffle(cells)
        cells.insert(p, good)
        its.append(mcq_fixed(fig(grid_svg(cells)) + q2, ["A", "B", "C", "D"], "ABCD"[p], "Triangle %s %s" % ("ABCD"[p], why)))
    words = [
        ("A triangle has sides of 8 cm, 8 cm and 5 cm. What type of triangle is it?", "isosceles triangle",
         ["equilateral triangle", "right-angled triangle", "right-angled isosceles triangle"],
         "Two sides are 8 cm, so exactly 2 sides are equal. It is an isosceles triangle."),
        ("What do the tick marks on the sides of a triangle show?", "the sides are equal",
         ["the angles are 90°", "the sides are long", "the sides are parallel"],
         "Sides with the same tick marks have the same length. A small square, not a tick mark, shows a right angle."),
        ("An equilateral triangle has a perimeter of 27 cm. How long is each side?", "9 cm",
         ["13.5 cm", "24 cm", "81 cm"], "All 3 sides are equal: 27 ÷ 3 = 9 cm. (13.5 cm is 27 ÷ 2, and 81 cm is 27 × 3.)"),
        ("An isosceles triangle has a perimeter of 20 cm. Its two equal sides are 7 cm each. How long is the third side?", "6 cm",
         ["13 cm", "7 cm", "10 cm"], "7 + 7 = 14 cm. 20 − 14 = 6 cm. (13 cm takes away only one of the 7 cm sides.)"),
        ("Hui Min says a right-angled triangle can also be an isosceles triangle. Is she correct?",
         "Yes, if 2 sides are equal", ["No, it can only have one name", "No, it must have 3 equal sides", "Yes, every one is isosceles"],
         "A right-angled triangle with 2 equal sides is a right-angled isosceles triangle, like half of a square cut along a diagonal."),
        ("Ethan says a triangle is isosceles only if it points up. Is he correct?", "No, it can point any way",
         ["Yes, it must point up", "Yes, or it is equilateral", "No, it must point down"],
         "The name depends only on the sides. Turning an isosceles triangle does not change its 2 equal sides."),
    ]
    for q2, ans, wrong, e in words:
        its.append(mcq(q2, ans, wrong, e, rnd))
    assert 27 / 3 == 9 and 20 - 14 == 6
    assert len(its) == 20, len(its)
    return {"title": "Types of triangles", "items": its}


# ------------------------------------------------------------ set 2: angle sum 180°
def find_x(a, b):
    """explanation for x = 180 − a − b"""
    return "The angles of a triangle add up to 180°. %d° + %d° = %d°, and 180° − %d° = <b>%d°</b>." % (a, b, a + b, a + b, 180 - a - b)


def set_sum(rnd):
    its = []
    its.append(mcq("The three angles of any triangle add up to", "180°", ["360°", "90°", "270°"],
                   "The angles of every triangle add up to 180°. (360° is the total for a four-sided figure such as a square.)", rnd))
    figs = [
        # (angle at A, angle at B, which vertex is x (0=A, 1=B, 2=C), rot, wrong answers)
        (50, 60, 2, 0, ["110°", "250°", "130°"]),
        (35, 75, 1, 0, None),
        (40, 25, 0, 0, None),
        (64, 72, 2, 0, None),
        (45, 105, 2, 160, None),
        (55, 48, 1, 180, None),
    ]
    for a, b, xi, rot, wrong in figs:
        A = [a, b, 180 - a - b]
        x = A[xi]
        known = [A[i] for i in range(3) if i != xi]
        if wrong is None:
            wrong = [D(sum(known)), D(360 - sum(known)), D(180 - known[0]), D(180 - known[1])]
        model = tri_ang(a, b)
        angs = []
        for i, n in enumerate("ABC"):
            o = "ABC"[i - 1], "ABC"[(i + 1) % 3]
            angs.append((n, o[0], o[1], "x" if i == xi else D(A[i]), A[i]))
        svg = tri_fig(model, ticks=False, angs=angs).svg(150, 100, rot, label="triangle with an unknown angle x")
        e = find_x(known[0], known[1])
        if D(180 - known[0]) in wrong[:3] or D(180 - known[1]) in wrong[:3]:
            e += " Subtract both known angles, not just one."
        its.append(mcq(fig(svg) + "Find ∠<i>x</i>.", D(x), wrong, e, rnd))
    # figures with vertex letters: find ∠ABC etc.
    lettered = [
        # (names in model order: base left, base right, top), angles at them, ask vertex, rot
        ("PQR", (48, 62), "R", 0),
        ("KLM", (100, 34), "K", 0),
        ("DEF", (57, 71), "E", 200),
    ]
    for names, (a, b), ask, rot in lettered:
        A = [a, b, 180 - a - b]
        i = names.index(ask)
        o1, o2 = sorted([names[i - 1], names[(i + 1) % 3]])
        known = [A[j] for j in range(3) if j != i]
        angs = [(names[j], names[j - 1], names[(j + 1) % 3], "?" if j == i else D(A[j]), A[j]) for j in range(3)]
        svg = tri_fig(tri_ang(a, b), names=names, ticks=False, angs=angs, letters=True).svg(150, 100, rot, label="triangle %s" % names)
        nm = "∠%s%s%s" % (o1, ask, o2)
        its.append(mcq(fig(svg) + "Find %s." % nm, D(A[i]), [D(sum(known)), D(360 - sum(known)), D(180 - max(known)), D(180 - min(known))],
                       find_x(known[0], known[1]), rnd))
    words = [
        ("In triangle PQR, ∠P = 47° and ∠Q = 68°. Find ∠R.", 47, 68, None),
        ("In triangle ABC, ∠A = 112° and ∠B = 29°. Find ∠C.", 112, 29, None),
        ("In triangle XYZ, ∠X = 38° and ∠Z = 85°. Find ∠Y.", 38, 85, None),
        ("Two angles of a triangle are 73° and 54°. What is the third angle?", 73, 54, None),
        ("Two angles of a triangle are 26° and 19°. What is the third angle?", 26, 19, None),
    ]
    for q, a, b, _ in words:
        c = 180 - a - b
        its.append(mcq(q, D(c), [D(a + b), D(360 - a - b), D(180 - a), D(180 - b)], find_x(a, b), rnd))
    f = lambda t: "%d°, %d°, %d°" % t
    pick = [
        ("Which set of angles can be the three angles of a triangle?", (50, 60, 70), [(50, 60, 80), (90, 45, 55), (100, 50, 40)]),
        ("Which set of angles can be the three angles of a triangle?", (35, 65, 80), [(35, 65, 90), (60, 60, 70), (120, 30, 40)]),
    ]
    for q, good, bad in pick:
        assert sum(good) == 180 and all(sum(x) != 180 for x in bad)
        why = "; ".join("%s add up to %d°" % (f(x), sum(x)) for x in bad)
        its.append(mcq(q, f(good), [f(x) for x in bad],
                       "%d° + %d° + %d° = 180°, so these angles work. The others do not add up to 180°: %s." % (good + (why,)), rnd))
    facts = [
        ("Ryan draws a big triangle and a small triangle. He says the angles of the big triangle add up to more. Is he correct?",
         "No, both add up to 180°", ["Yes, its angles are bigger", "Yes, they add up to 360°", "No, the small one has more"],
         "The angles of every triangle add up to 180°, big or small. A bigger triangle has longer sides, not bigger angles."),
        ("Chloe tears off the 3 corners of a paper triangle and puts them together, point to point. What do they make?",
         "a straight line, 180°", ["a right angle, 90°", "a full turn, 360°", "a small acute angle"],
         "The 3 angles of a triangle add up to 180°, so the 3 corners fit together to make a straight line."),
        ("Can a triangle have angles of 95° and 85°?", "No, nothing is left",
         ["Yes, 95° is a big angle", "Yes, any sizes work", "No, 95° is too small"],
         "95° + 85° = 180°. That leaves 0° for the third angle, so these cannot be two angles of a triangle."),
    ]
    for q, ans, wrong, e in facts:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angle sum of a triangle (180°)", "items": its}


# ------------------------------------------------------------ set 3: isosceles triangles
def set_isosceles(rnd):
    its = []
    # top angle given -> find a base angle (halve)
    for top, rot in [(40, 0), (50, 180), (110, 0), (36, 90)]:
        base = (180 - top) // 2
        assert 2 * base + top == 180
        model = tri_ang(base, base)
        angs = [("A", "C", "B", "x", base), ("C", "A", "B", D(top))]
        svg = tri_fig(model, angs=angs).svg(140, 100, rot, label="isosceles triangle with an unknown angle x")
        its.append(mcq(fig(svg) + "The triangle is an isosceles triangle. Find ∠<i>x</i>.", D(base),
                       [D(180 - top), D(top), D(180 - 2 * top) if top < 90 else D((360 - top) // 2), D((360 - top) // 2)],
                       "The tick marks show 2 equal sides, so the 2 angles at the ends of the third side are equal. "
                       "180° − %d° = %d°, and %d° ÷ 2 = <b>%d°</b>. (%d° forgets to divide by 2.)" % (top, 180 - top, 180 - top, base, 180 - top), rnd))
    # one base angle given -> find the top angle
    for base, rot in [(70, 0), (35, 0), (52, 180), (38, 0)]:
        top = 180 - 2 * base
        model = tri_ang(base, base)
        angs = [("A", "C", "B", D(base), base), ("C", "A", "B", "x", top)]
        svg = tri_fig(model, angs=angs).svg(140, 100, rot, label="isosceles triangle with an unknown angle x")
        its.append(mcq(fig(svg) + "The triangle is an isosceles triangle. Find ∠<i>x</i>.", D(top),
                       [D(180 - base), D(base), D((180 - base) // 2) if (180 - base) % 2 == 0 else D(360 - 2 * base), D(360 - 2 * base)],
                       "The 2 base angles are equal, so the other base angle is also %d°. "
                       "180° − %d° − %d° = <b>%d°</b>. (%d° subtracts only one base angle.)" % (base, base, base, top, 180 - base), rnd))
    # one base angle given -> find the other base angle
    for base, rot in [(64, 0), (28, 180)]:
        top = 180 - 2 * base
        model = tri_ang(base, base)
        angs = [("A", "C", "B", D(base), base), ("B", "A", "C", "x", base)]
        svg = tri_fig(model, angs=angs).svg(140, 100, rot, label="isosceles triangle with an unknown angle x")
        its.append(mcq(fig(svg) + "The triangle is an isosceles triangle. Find ∠<i>x</i>.", D(base),
                       [D(top), D(180 - base), D((180 - base) // 2), D(90 - base)],
                       "The tick marks show the 2 equal sides. The angles opposite them, at the ends of the third side, are equal. "
                       "So ∠<i>x</i> = <b>%d°</b>. (%d° is the angle at the top.)" % (base, top), rnd))
    # which angles are equal (lettered)
    lettered = [
        ("PQR", "PQ = PR", "R", "∠PQR and ∠PRQ", ["∠QPR and ∠PQR", "∠QPR and ∠PRQ", "all three angles"], 72, 0),
        ("XYZ", "XY = XZ", "X", "∠XYZ and ∠XZY", ["∠YXZ and ∠XYZ", "∠YXZ and ∠XZY", "all three angles"], 40, 200),
    ]
    for names, eq, _, ans, wrong, base, rot in lettered:
        # model order: base left, base right, top -> names[1], names[2], names[0]
        top_n, l_n, r_n = names[0], names[1], names[2]
        model = tri_ang(base, base)
        f = Fig({l_n: model[0], r_n: model[1], top_n: model[2]}).poly([l_n, r_n, top_n]).letter(l_n, r_n, top_n)
        svg = f.svg(140, 100, rot, label="isosceles triangle %s" % names)
        its.append(mcq(fig(svg) + "In triangle %s, %s. Which two angles are equal?" % (names, eq), ans, wrong,
                       "The equal sides %s and %s meet at %s. The 2 equal angles are at the other two corners, %s and %s: <b>%s</b>."
                       % (eq[:2], eq[-2:], top_n, l_n, r_n, ans), rnd))
    words = [
        ("In triangle ABC, AB = AC and ∠BAC = 40°. Find ∠ABC.", "70°", ["140°", "40°", "100°"],
         "AB = AC, so ∠ABC = ∠ACB. 180° − 40° = 140°, and 140° ÷ 2 = <b>70°</b>."),
        ("In triangle XYZ, XY = XZ and ∠XYZ = 64°. Find ∠YXZ.", "52°", ["116°", "64°", "58°"],
         "XY = XZ, so ∠XZY = ∠XYZ = 64°. 180° − 64° − 64° = <b>52°</b>. (116° subtracts only one 64° angle.)"),
        ("One angle of an isosceles triangle is 100°. Find each of the other two angles.", "40°", ["100°", "80°", "20°"],
         "Two angles of 100° would add up to more than 180°, so 100° is the angle at the top. 180° − 100° = 80°, and 80° ÷ 2 = <b>40°</b>."),
        ("The two equal angles of an isosceles triangle add up to 130°. What is the third angle?", "50°", ["65°", "130°", "230°"],
         "180° − 130° = <b>50°</b>. (65° is each equal angle, not the third angle.)"),
        ("In an isosceles triangle, the angle at the top is 3 times the size of each base angle. Find a base angle.", "36°",
         ["60°", "45°", "108°"],
         "Base + base + top = 1 unit + 1 unit + 3 units = 5 units = 180°. 1 unit = 180° ÷ 5 = <b>36°</b>. (The top angle is 108°.)"),
        ("Each base angle of an isosceles triangle is 45°. Find the angle at the top.", "90°", ["135°", "45°", "100°"],
         "180° − 45° − 45° = <b>90°</b>. So it is a right-angled isosceles triangle. (135° subtracts only one 45° angle.)"),
        ("In triangle DEF, DE = DF and ∠EDF = 90°. Find ∠DEF.", "45°", ["90°", "60°", "30°"],
         "DE = DF, so ∠DEF = ∠DFE. 180° − 90° = 90°, and 90° ÷ 2 = <b>45°</b>. (90° forgets to divide by 2.)"),
        ("Which set of angles can be the three angles of an isosceles triangle?", "110°, 35°, 35°",
         ["110°, 40°, 40°", "100°, 35°, 35°", "70°, 70°, 50°"],
         "110° + 35° + 35° = 180°, and two angles are equal. The others add up to 190°, 170° and 190°."),
    ]
    assert 110 + 70 == 180 and 110 + 80 == 190 and 100 + 70 == 170 and 140 + 50 == 190
    assert (180 - 40) / 2 == 70 and 180 - 128 == 52 and (180 - 100) / 2 == 40 and 180 - 130 == 50 and 180 / 5 == 36
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Isosceles triangles: equal base angles", "items": its}


# ------------------------------------------------------------ set 4: equilateral and right-angled triangles
def set_equi_right(rnd):
    its = []
    its.append(mcq("What is the size of each angle of an equilateral triangle?", "60°", ["90°", "120°", "180°"],
                   "The 3 angles are equal and add up to 180°: 180° ÷ 3 = <b>60°</b>. (120° comes from 360° ÷ 3.)", rnd))
    for rot in (0, 180):
        f = tri_fig(EQUI, angs=[("A", "C", "B", "x", 60)])
        svg = f.svg(120, 100, rot, label="equilateral triangle with an unknown angle x")
        its.append(mcq(fig(svg) + "The triangle is an equilateral triangle. Find ∠<i>x</i>.", "60°", ["90°", "120°", "45°"],
                       "All 3 sides are equal, so all 3 angles are equal. 180° ÷ 3 = <b>60°</b>.", rnd))
    f = tri_fig(EQUI, ticks=True, sides=[("A", "B", "7 cm")])
    its.append(mcq(fig(f.svg(120, 100, 0, label="equilateral triangle with one side 7 cm")) +
                   "The triangle is an equilateral triangle. Find its perimeter.", "21 cm", ["14 cm", "7 cm", "49 cm"],
                   "All 3 sides are 7 cm. 3 × 7 = <b>21 cm</b>. (14 cm counts only 2 sides.)", rnd))
    # right-angled: find x
    rts = [(90, 34, 2, 0), (90, 52, 1, 0), (61, 90, 2, 180), (90, 27, 2, 0)]
    for a, b, xi, rot in rts:
        A = [a, b, 180 - a - b]
        known = [v for i, v in enumerate(A) if i != xi and v != 90][0]
        x = A[xi]
        angs = []
        for i, n in enumerate("ABC"):
            if A[i] == 90:
                continue
            angs.append((n, "ABC"[i - 1], "ABC"[(i + 1) % 3], "x" if i == xi else D(A[i]), A[i]))
        svg = tri_fig(tri_ang(a, b), ticks=False, angs=angs).svg(150, 100, rot, label="right-angled triangle with an unknown angle x")
        its.append(mcq(fig(svg) + "Find ∠<i>x</i>.", D(x), [D(180 - known), D(known), D(270 - known), D(90 + known)],
                       "The small square is a right angle, 90°. 180° − 90° − %d° = <b>%d°</b>. (%d° forgets the right angle.)"
                       % (known, x, 180 - known), rnd))
    f = tri_fig(ISO_RT, angs=[("A", "C", "B", "x", 45)])
    its.append(mcq(fig(f.svg(140, 90, 0, label="right-angled isosceles triangle with an unknown angle x")) + "Find ∠<i>x</i>.", "45°",
                   ["90°", "60°", "30°"],
                   "It is a right-angled isosceles triangle, so the other 2 angles are equal. 180° − 90° = 90°, and 90° ÷ 2 = <b>45°</b>.", rnd))
    f = tri_fig(tri_ang(90, 40), names="PQR", ticks=False, angs=[("Q", "P", "R", "40°")], letters=True)
    its.append(mcq(fig(f.svg(150, 100, 0, label="right-angled triangle PQR")) + "Find ∠PRQ.", "50°",
                   ["140°", "40°", "90°"],
                   "∠QPR is a right angle (90°). ∠PRQ = 180° − 90° − 40° = <b>50°</b>. (140° forgets the right angle.)", rnd))
    words = [
        ("Kumar says a triangle with angles of 60°, 60° and 60° must have 3 equal sides. Is he correct?", "Yes, it is equilateral",
         ["No, the sides can differ", "No, it is right-angled", "Yes, but only if it is small"],
         "Equal angles go with equal sides. A triangle with three 60° angles is an <b>equilateral triangle</b>, whatever its size."),
        ("In triangle ABC, ∠ABC = 90° and ∠BAC = 38°. Find ∠ACB.", "52°", ["142°", "38°", "62°"],
         "180° − 90° − 38° = <b>52°</b>. (142° forgets the right angle.)"),
        ("The two angles of a right-angled triangle that are not right angles add up to", "90°", ["180°", "270°", "45°"],
         "All 3 angles add up to 180°, and the right angle takes 90°. 180° − 90° = <b>90°</b> is left for the other two."),
        ("What is the greatest number of right angles a triangle can have?", "1", ["2", "3", "0"],
         "Two right angles already make 90° + 90° = 180°. That leaves 0° for the third angle, so a triangle has at most <b>1</b> right angle."),
        ("Ali draws a right-angled triangle. He says it has a right angle at each end of the base. Is he correct?",
         "No, it has only 1", ["Yes, there are 2", "Yes, like a square", "No, it has 3"],
         "90° + 90° = 180° leaves nothing for the third angle. A right-angled triangle has exactly <b>1</b> right angle."),
        ("Can a triangle have one right angle and one angle of 100°?", "No, they add up to over 180°",
         ["Yes, if it is large", "Yes, if it is isosceles", "No, 100° is too small"],
         "90° + 100° = 190°, which is already more than 180°."),
        ("Siti folds a square piece of paper along a diagonal. What triangle does she get?", "right-angled isosceles triangle",
         ["equilateral triangle", "right-angled triangle with no equal sides", "isosceles triangle with no right angle"],
         "The corner of the square is 90°, and two sides of the square are equal. So it is a <b>right-angled isosceles triangle</b> (angles 90°, 45°, 45°)."),
        ("An equilateral triangle has sides of 12 cm. What is the size of each angle?", "60°", ["12°", "36°", "120°"],
         "Every equilateral triangle has three 60° angles (180° ÷ 3), whatever the length of its sides. "
         "(12° mixes up the side length with the angle, and 36° is the perimeter.)"),
        ("An equilateral triangle has a perimeter of 45 cm. How long is each side?", "15 cm", ["22.5 cm", "42 cm", "135 cm"],
         "45 ÷ 3 = <b>15 cm</b>. (22.5 cm is 45 ÷ 2, and 135 cm is 45 × 3.)"),
        ("In a right-angled triangle, one acute angle is 2 times the size of the other acute angle. Find the smaller acute angle.",
         "30°", ["45°", "60°", "90°"],
         "The two angles add up to 90°. 2 units + 1 unit = 3 units = 90°, so 1 unit = 90° ÷ 3 = <b>30°</b>. (60° is the larger angle.)"),
    ]
    assert 180 - 90 - 38 == 52 and 45 / 3 == 15 and 90 / 3 == 30
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equilateral (60°) and right-angled triangles", "items": its}


# ------------------------------------------------------------ set 5: unknown angles with straight lines, word problems
def ext_fig(b, c, ext=60.0, left=False):
    """Triangle ABC (B base left, C base right, A top) with the base produced past C to D (and past B to E if left)."""
    m = tri_ang(b, c)
    P = {"B": m[0], "C": m[1], "A": m[2], "D": (m[1][0] + ext, 0.0)}
    f = Fig(P).poly(["B", "C", "A"], ticks=(b == c)).seg("C", "D")
    if left:
        f.P["E"] = (m[0][0] - ext, 0.0)
        f.seg("E", "B")
    return f


def cevian_fig(b, c, t):
    """Triangle ABC with D on BC and AD drawn, so that ∠ADB = t."""
    m = tri_ang(b, c, base=160.0)
    ax, ay = m[2]
    dx = ax + (-ay) / math.tan(math.radians(t))
    assert 25 < dx < 135, dx
    P = {"B": m[0], "C": m[1], "A": m[2], "D": (dx, 0.0)}
    assert abs(angle_at(P["D"], P["A"], P["B"]) - t) < 1e-6
    return Fig(P).poly(["B", "C", "A"], ticks=(b == c)).seg("A", "D")


def set_lines(rnd):
    its = []
    Q = "BCD is a straight line. "
    # 1 exterior angle given -> interior
    f = ext_fig(60, 65).ang("C", "D", "A", "115°").ang("C", "A", "B", "x", 65).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 95, label="triangle ABC with BCD a straight line")) + Q + "Find ∠<i>x</i>.", "65°",
                   ["115°", "245°", "25°"],
                   "Angles on a straight line add up to 180°. ∠<i>x</i> = 180° − 115° = <b>65°</b>. (245° uses 360°.)", rnd))
    # 2 interior given -> exterior
    f = ext_fig(70, 58).ang("C", "A", "B", "58°").ang("C", "D", "A", "x", 122).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 95, label="triangle ABC with BCD a straight line")) + Q + "Find ∠<i>x</i>.", "122°",
                   ["58°", "302°", "32°"],
                   "∠<i>x</i> and 58° are angles on a straight line. 180° − 58° = <b>122°</b>.", rnd))
    # 3 exterior + top -> base angle
    f = ext_fig(55, 50).ang("C", "D", "A", "130°").ang("A", "B", "C", "75°").ang("B", "C", "A", "x", 55).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 95, label="triangle ABC with BCD a straight line")) + Q + "Find ∠<i>x</i>.", "55°",
                   ["50°", "105°", "205°"],
                   "∠ACB = 180° − 130° = 50° (straight line). ∠<i>x</i> = 180° − 75° − 50° = <b>55°</b>. (50° is ∠ACB, not ∠<i>x</i>.)", rnd))
    # 4 two interior -> exterior
    f = ext_fig(48, 65).ang("B", "C", "A", "48°").ang("A", "B", "C", "67°").ang("C", "D", "A", "x", 115).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 95, label="triangle ABC with BCD a straight line")) + Q + "Find ∠<i>x</i>.", "115°",
                   ["65°", "245°", "19°"],
                   "∠ACB = 180° − 48° − 67° = 65°. On the straight line, ∠<i>x</i> = 180° − 65° = <b>115°</b>. (65° is ∠ACB.)", rnd))
    # 5 isosceles, exterior -> top
    f = ext_fig(70, 70).ang("C", "D", "A", "110°").ang("A", "B", "C", "x", 40).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 100, label="isosceles triangle ABC with BCD a straight line")) + "AB = AC and " + Q +
                   "Find ∠<i>x</i>.", "40°", ["70°", "110°", "55°"],
                   "∠ACB = 180° − 110° = 70°. AB = AC, so ∠ABC = 70° too. ∠<i>x</i> = 180° − 70° − 70° = <b>40°</b>.", rnd))
    # 6 isosceles, top -> exterior
    f = ext_fig(72, 72).ang("A", "B", "C", "36°").ang("C", "D", "A", "x", 108).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 135, label="isosceles triangle ABC with BCD a straight line")) + "AB = AC and " + Q +
                   "Find ∠<i>x</i>.", "108°", ["72°", "144°", "252°"],
                   "180° − 36° = 144°, and 144° ÷ 2 = 72°, so ∠ACB = 72°. On the straight line, ∠<i>x</i> = 180° − 72° = <b>108°</b>.", rnd))
    # 7 right angle at B, exterior -> top
    f = ext_fig(90, 35).ang("C", "D", "A", "145°").ang("A", "B", "C", "x", 55).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 110, label="right-angled triangle ABC with BCD a straight line")) + Q + "Find ∠<i>x</i>.", "55°",
                   ["35°", "145°", "125°"],
                   "∠ACB = 180° − 145° = 35°. ∠<i>x</i> = 180° − 90° − 35° = <b>55°</b>. (35° is ∠ACB.)", rnd))
    # 8 both ends produced
    f = ext_fig(60, 50, ext=50, left=True).ang("B", "E", "A", "120°").ang("C", "D", "A", "130°").ang("A", "B", "C", "x", 70)
    f.letter("A", "B", "C", "D", "E")
    its.append(mcq(fig(f.svg(230, 95, label="triangle ABC with EBCD a straight line")) + "EBCD is a straight line. Find ∠<i>x</i>.",
                   "70°", ["110°", "10°", "250°"],
                   "∠ABC = 180° − 120° = 60° and ∠ACB = 180° − 130° = 50°. ∠<i>x</i> = 180° − 60° − 50° = <b>70°</b>.", rnd))
    # 9 cevian: find ∠DAC
    f = cevian_fig(60, 45, 75).ang("D", "C", "A", "105°").ang("C", "A", "D", "45°").ang("A", "D", "C", "x", 30)
    f.letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 100, label="triangle ABC with D on BC")) + "D is a point on BC. Find ∠<i>x</i>.", "30°",
                   ["75°", "135°", "60°"],
                   "In triangle ADC: ∠<i>x</i> = 180° − 105° − 45° = <b>30°</b>.", rnd))
    # 10 cevian: straight line at D
    f = cevian_fig(55, 50, 70).ang("D", "A", "B", "70°").ang("D", "C", "A", "x", 110).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 100, label="triangle ABC with D on BC")) + "BDC is a straight line. Find ∠<i>x</i>.", "110°",
                   ["70°", "290°", "20°"],
                   "∠ADB and ∠<i>x</i> are angles on a straight line. 180° − 70° = <b>110°</b>.", rnd))
    # 11 cevian: two steps
    f = cevian_fig(50, 25, 70).ang("B", "C", "A", "50°").ang("D", "C", "A", "110°").ang("A", "B", "D", "x", 60).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 100, label="triangle ABC with D on BC")) + "BDC is a straight line. Find ∠<i>x</i>.", "60°",
                   ["20°", "70°", "130°"],
                   "∠ADB = 180° − 110° = 70° (straight line). In triangle ABD: ∠<i>x</i> = 180° − 50° − 70° = <b>60°</b>. "
                   "(20° uses 110° inside triangle ABD.)", rnd))
    # 12 cevian in an isosceles triangle
    f = cevian_fig(65, 65, 100).ang("D", "C", "A", "80°").ang("C", "A", "D", "65°").ang("A", "D", "C", "x", 35).letter("A", "B", "C", "D")
    its.append(mcq(fig(f.svg(200, 135, label="isosceles triangle ABC with D on BC")) + "AB = AC and D is a point on BC. Find ∠<i>x</i>.",
                   "35°", ["15°", "50°", "100°"],
                   "In triangle ADC: ∠<i>x</i> = 180° − 80° − 65° = <b>35°</b>. (50° is the whole ∠BAC.)", rnd))
    # word problems in Singapore settings
    words = [
        ("A ladder leans against the wall of an HDB block. The wall makes a right angle with the ground. "
         "The ladder makes an angle of 72° with the ground. What angle does it make with the wall?", "18°", ["108°", "72°", "288°"],
         "The ladder, the wall and the ground form a right-angled triangle. 180° − 90° − 72° = <b>18°</b>. (108° forgets the right angle.)"),
        ("The roof of a sheltered walkway near a void deck is an isosceles triangle. The angle at the top is 120°. "
         "Find each of the other two angles.", "30°", ["60°", "120°", "240°"],
         "180° − 120° = 60°, shared by 2 equal angles: 60° ÷ 2 = <b>30°</b>. (60° forgets to divide by 2.)"),
        ("For National Day, Priya cuts triangle flags for bunting. Each flag is an isosceles triangle with a 40° angle at the bottom tip. "
         "Find each of the two equal angles.", "70°", ["140°", "40°", "100°"],
         "180° − 40° = 140°, and 140° ÷ 2 = <b>70°</b>."),
        ("Mr Tan cuts a rectangular garden plot into two triangles along a diagonal. One angle in each triangle is 35°. "
         "What are the other two angles?", "90° and 55°", ["90° and 35°", "55° and 55°", "145° and 0°"],
         "Each triangle keeps a corner of the rectangle, so one angle is 90°. 180° − 90° − 35° = <b>55°</b>."),
        ("A sail on a boat at East Coast Park is a right-angled triangle. One of its angles is 64°. Find the third angle.", "26°",
         ["116°", "64°", "36°"], "180° − 90° − 64° = <b>26°</b>. (116° forgets the right angle.)"),
        ("At a playground, the ladder of a slide stands upright, at 90° to the ground. The slide makes an angle of 40° with the ground. "
         "The ladder, the slide and the ground form a triangle. Find the angle between the ladder and the slide at the top.", "50°",
         ["140°", "40°", "230°"], "180° − 90° − 40° = <b>50°</b>. (140° forgets the right angle, and 230° uses 360°.)"),
    ]
    assert 180 - 90 - 72 == 18 and (180 - 120) / 2 == 30 and (180 - 40) / 2 == 70 and 180 - 90 - 64 == 26
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    # bar model problems
    svg = bar2_svg(3, 1, "100°", "∠A", "∠B", "bot")
    its.append(mcq(fig(svg) + "In triangle ABC, ∠C = 80°. ∠A is 3 times the size of ∠B. Find ∠B.", "25°",
                   ["75°", "20°", "100°"],
                   "∠A + ∠B = 180° − 80° = 100°. 4 units = 100°, so 1 unit = 100° ÷ 4 = <b>25°</b>. (75° is ∠A.)", rnd))
    svg = bar2_svg(2, 1, "135°", "∠P", "∠Q", "top")
    its.append(mcq(fig(svg) + "In triangle PQR, ∠R = 45°. ∠P is 2 times the size of ∠Q. Find ∠P.", "90°",
                   ["45°", "135°", "270°"],
                   "∠P + ∠Q = 180° − 45° = 135°. 3 units = 135°, so 1 unit = 45°. ∠P = 2 units = <b>90°</b>. (45° is ∠Q.)", rnd))
    assert (180 - 80) / 4 == 25 and (180 - 45) / 3 * 2 == 90
    # check the straight-line answers
    assert 180 - 115 == 65 and 180 - 58 == 122 and 180 - 75 - 50 == 55 and 180 - (180 - 48 - 67) == 115
    assert 180 - 140 == 40 and 180 - 72 == 108 and 180 - 90 - 35 == 55 and 180 - 60 - 50 == 70
    assert 180 - 105 - 45 == 30 and 180 - 70 == 110 and 180 - 50 - 70 == 60 and 180 - 80 - 65 == 35
    assert len(its) == 20, len(its)
    return {"title": "Unknown angles with straight lines and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    kinds = strip_svg([(tri_fig(ISO_AC), 0, "isosceles", 96, 84), (tri_fig(EQUI), 0, "equilateral", 96, 84),
                       (tri_fig(SCA_RT), 0, "right-angled", 110, 84), (tri_fig(ISO_RT), 0, "right-angled isosceles", 120, 60)],
                      "isosceles, equilateral, right-angled and right-angled isosceles triangles with their marks", cw=176, top=104)
    summ = tri_fig(tri_ang(50, 60), ticks=False, angs=[("A", "C", "B", "50°"), ("B", "A", "C", "60°"), ("C", "B", "A", "x", 70)]).svg(
        150, 100, 0, label="triangle with angles 50°, 60° and x")
    iso = tri_fig(ISO_AC, angs=[("A", "C", "B", "x", 70), ("B", "A", "C", "y", 70), ("C", "A", "B", "40°")]).svg(
        140, 120, 0, label="isosceles triangle with a top angle of 40°")
    line = ext_fig(55, 50).ang("C", "D", "A", "130°").ang("A", "B", "C", "75°").ang("B", "C", "A", "x", 55).letter("A", "B", "C", "D").svg(
        200, 95, label="triangle ABC with BCD a straight line")
    model = bar2_svg(3, 1, "100°", "∠A", "∠B", "bot")
    return (
        "<h2>Types of triangles</h2>"
        "<p>Tick marks show equal sides. A small square shows a right angle (90°).</p>" +
        table(["Triangle", "What to look for", "Angles"], [
            ["Isosceles", "2 equal sides", "the 2 base angles are equal"],
            ["Equilateral", "3 equal sides", "every angle is 60°"],
            ["Right-angled", "1 right angle", "the other 2 angles add up to 90°"],
        ]) +
        "<figure class='sn-fig'>" + kinds +
        "<figcaption>A triangle can be turned any way. Its name stays the same.</figcaption></figure>"
        "<h2>The angles add up to 180°</h2>"
        "<p>The 3 angles of every triangle add up to 180°, big or small. To find an unknown angle, subtract the two known angles from 180°.</p>"
        "<figure class='sn-fig'>" + summ +
        "<figcaption>50° + 60° = 110°, and 180° − 110° = 70°. So ∠<i>x</i> = 70°.</figcaption></figure>" +
        ex("Example 1", "In triangle PQR, ∠P = 47° and ∠Q = 68°. Find ∠R.",
           "47° + 68° = 115°. 180° − 115° = 65°.", "∠R = 65°") +
        "<h2>Isosceles triangles</h2>"
        "<p>The 2 equal sides meet at the top. The 2 angles at the ends of the third side (the base angles) are equal.</p>"
        "<figure class='sn-fig'>" + iso +
        "<figcaption>180° − 40° = 140°, and 140° ÷ 2 = 70°. So ∠<i>x</i> = ∠<i>y</i> = 70°.</figcaption></figure>" +
        ex("Example 2", "In triangle XYZ, XY = XZ and ∠XYZ = 64°. Find ∠YXZ.",
           "XY = XZ, so ∠XZY = 64° too. 180° − 64° − 64° = 52°.", "∠YXZ = 52°") +
        "<h2>Equilateral and right-angled triangles</h2>"
        "<p>An equilateral triangle has three 60° angles (180° ÷ 3). A right-angled triangle has exactly one right angle, "
        "so its other two angles add up to 90°.</p>"
        "<h2>Straight lines</h2>"
        "<p>Angles on a straight line add up to 180°. Use this first, then the angle sum of the triangle.</p>"
        "<figure class='sn-fig'>" + line +
        "<figcaption>∠ACB = 180° − 130° = 50°. ∠<i>x</i> = 180° − 75° − 50° = 55°.</figcaption></figure>" +
        ex("Example 3", "In triangle ABC, ∠C = 80°. ∠A is 3 times the size of ∠B. Find ∠B.",
           "∠A + ∠B = 180° − 80° = 100°. Draw a model: ∠A is 3 units and ∠B is 1 unit. 4 units = 100°, so 1 unit = 25°.", "∠B = 25°") +
        "<figure class='sn-fig'>" + model + "<figcaption>4 units = 100°, 1 unit = 25°.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Subtracting from 360°", "The angles of a triangle add up to 180°. 360° is for four-sided figures"],
            ["Subtracting only one known angle", "Subtract both known angles from 180°"],
            ["Isosceles: forgetting to divide by 2", "180° − top angle, then ÷ 2 for each base angle"],
            ["Isosceles: choosing the wrong equal angles", "The equal angles are at the ends of the side without tick marks"],
            ["A right-angled triangle with 2 right angles", "It has exactly 1. The other 2 angles add up to 90°"],
            ["Taking the angle outside the triangle as the one inside", "Use the straight line: 180° − outside angle"],
        ])
    )


FAQ = [
    {"q": "What do P5 students learn about triangles?",
     "a": "In Primary 5, students learn the properties of isosceles, equilateral and right-angled triangles, that the angles of a triangle add up to 180°, and how to find unknown angles in figures."},
    {"q": "How do I find the unknown angle in an isosceles triangle?",
     "a": "The two base angles are equal. If you know the top angle, subtract it from 180° and divide by 2; if you know a base angle, subtract two base angles from 180°."},
    {"q": "What is the most common mistake with angles of a triangle?",
     "a": "Subtracting from 360° instead of 180°, or subtracting only one of the known angles. In isosceles triangles, many students forget to divide by 2."},
    {"q": "Is this topic in the MOE syllabus and the PSLE?",
     "a": "Yes. Triangles and unknown angles are part of Geometry in the MOE Primary 5 syllabus, and unknown-angle questions in figures also appear in the PSLE at the end of Primary 6."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(65814)
    spots = Spots(rnd)
    sets = [set_classify(rnd, spots), set_sum(rnd), set_isosceles(rnd), set_equi_right(rnd), set_lines(rnd)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen or "<svg" in it["q"], it["q"]
            seen.add(k)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "triangles", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Triangles: Properties and Unknown Angles",
        "seo_title": "P5 Triangles Worksheets: Free Primary 5 Maths on Angles of a Triangle with Answers (MOE Syllabus)",
        "short_title": "Triangles",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 5: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Properties of isosceles, equilateral and right-angled triangles; angle sum of a triangle; finding unknown angles",
        "meta_desc": "Free P5 maths practice: isosceles, equilateral and right-angled triangles, the 180° angle sum and unknown angles. 100 questions with answers.",
        "key_big": "The 3 angles of a triangle always add up to 180°.",
        "key_sub": "Two angles are 50° and 60°: the third angle is 180° − 50° − 60° = 70°.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "four triangles labelled A to D")
    mark_large(u, "bar model")
    mark_large(u, "triangle ABC with")
    mark_large(u, "isosceles triangle ABC with")
    mark_large(u, "right-angled triangle ABC with")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
