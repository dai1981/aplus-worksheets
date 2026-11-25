# -*- coding: utf-8 -*-
"""
Indonesia / Matematika / SMP Kelas 7–9 (Fase D, Kurikulum Merdeka CP 2025) の共通部品と実行。
python3 tools/id_smp.py 7|8|9 [番号…]
seed は 40000 + 100 × kelas + 番号。単元は id_smp7・id_smp8・id_smp9 の UNITS。
・負の数は「−」、負の数はかっこ（−5）。小数はコンマ、1.000 は点
・M() は負の数の選択肢も残す 4 択（誤答が 3 つそろわないと None で作り直し）
"""
import re
import random
import sys
from fractions import Fraction as Fr
import id_common as C
from id_common import num, NB, mix, lesson, example, table, make_unit, wrap, text, line, fig, svg_wrap, INK, GREEN, FILL, RED, BLUE, fr  # noqa: F401

MINUS = "−"
R = random.Random(0)


def ri(a, b):
    return R.randint(a, b)


def ch(x):
    return R.choice(list(x))


def nz(a, b):
    while True:
        v = R.randint(a, b)
        if v:
            return v


def sh(x):
    x = list(x)
    R.shuffle(x)
    return x


# ------------------------------------------------------------ numbers
def endlich(v):
    d = Fr(v).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def dz(v, k=None):
    """Fraction → 2,5 / −0,75（割り切れないと ValueError）。k で桁を固定（四捨五入）"""
    v = Fr(v)
    if k is not None:
        n = abs(v) * 10 ** k
        n = int(n + Fr(1, 2))
        s = MINUS if v < 0 and n else ""
        ip, fp = divmod(n, 10 ** k)
        return s + num(ip) + ("," + str(fp).rjust(k, "0") if k else "")
    if not endlich(v):
        raise ValueError(v)
    s = MINUS if v < 0 else ""
    v = abs(v)
    k = 0
    while (10 ** k) % v.denominator:
        k += 1
    n = v.numerator * 10 ** k // v.denominator
    ip, fp = divmod(n, 10 ** k)
    return s + num(ip) + ("," + str(fp).rjust(k, "0") if k else "")


def fq(v, mixed=False):
    """Fraction → HTML の分数（整数ならそのまま）"""
    if isinstance(v, float):
        raise ValueError("float %r" % v)
    v = Fr(v)
    s = MINUS if v < 0 else ""
    v = abs(v)
    if v.denominator == 1:
        return s + num(v.numerator)
    if mixed and v > 1:
        w, r = divmod(v.numerator, v.denominator)
        return s + "%s%s" % (num(w), fr(num(r), num(v.denominator)))
    return s + fr(num(v.numerator), num(v.denominator))


def sn(v):
    """数（Fraction も）→ 文字列"""
    if isinstance(v, float):
        raise ValueError("float %r" % v)
    v = Fr(v)
    return fq(v) if v.denominator != 1 else num(v.numerator)


def par(v):
    v = Fr(v)
    return "(%s)" % sn(v) if v < 0 else sn(v)


def pd(v):
    """小数の par"""
    v = Fr(v)
    return "(%s)" % dz(v) if v < 0 else dz(v)


def coef(k, var, first):
    k = Fr(k)
    a = abs(k)
    if var:
        body = ("" if a == 1 else sn(a)) + var
    else:
        body = sn(a)
    if first:
        return (MINUS if k < 0 else "") + body
    return " %s %s" % (MINUS if k < 0 else "+", body)


def expr(terms):
    """[(3, "x²"), (−2, "x"), (5, "")] → 3x² − 2x + 5"""
    out = ""
    for k, v in terms:
        if Fr(k) == 0:
            continue
        out += coef(k, v, out == "")
    return out or "0"


def lin(a, b, v="x"):
    return expr([(a, v), (b, "")])


def sup(n):
    return "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(c)] if c.isdigit() else ("⁻" if c in "-−" else c) for c in str(n))


def pw(base, e):
    """2⁵、(−3)⁴"""
    b = Fr(base)
    bs = "(%s)" % sn(b) if b < 0 or b.denominator != 1 else sn(b)
    return bs + sup(e)


def rp(n):
    return "Rp" + num(n)


def pct(x):
    x = Fr(x)
    return (dz(x) if endlich(x) else dz(x, 1)) + "%"


# ------------------------------------------------------------ questions
def M(q, correct, wrongs, e):
    correct = str(correct)
    seen = {correct, re.sub(r"\s+", "", correct)}
    pick = []
    for w in wrongs:
        if w is None:
            continue
        w = str(w)
        k = re.sub(r"\s+", "", w)
        if w in seen or k in seen or w == "":
            continue
        seen.add(w)
        seen.add(k)
        pick.append(w)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        return None
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def MN(q, v, wrongs, e, unit=""):
    """数の答え（Fraction / int）。単位を後ろに付ける"""
    if v is None:
        return None
    if unit == "rupiah":
        f = lambda x: None if x is None or Fr(x).denominator != 1 else (MINUS if x < 0 else "") + rp(abs(int(x)))
    elif unit.startswith("°"):
        f = lambda x: None if x is None else sn(x) + unit
    else:
        f = lambda x: None if x is None else sn(x) + (NB + unit if unit else "")
    return M(q, f(v), [f(w) for w in wrongs], e)


def MD(q, v, wrongs, e, unit=""):
    """小数の答え"""
    if v is None:
        return None
    places = lambda t: len(t.split(",")[1]) if "," in t else 0
    lim = max(2, places(dz(v)))

    def f(x):
        if x is None:
            return None
        try:
            t = dz(x)
        except ValueError:
            return None
        if places(t) > lim:
            return None
        return t + (NB + unit if unit else "")
    return M(q, f(v), [f(w) for w in wrongs], e)


def near(v, *ds):
    return [v + d for d in ds]


# ------------------------------------------------------------ pictures
def relabel(svg, label):
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)


def kosy(lines=(), pts=(), lo=-5, hi=5, label="bidang koordinat"):
    from de_k8 import kosy as K
    return relabel(K(lines=lines, pts=pts, lo=lo, hi=hi, label=label), label)


def kurve(fs, xr, yr, pts=(), label="grafik"):
    from de_k10 import kurve as K
    return relabel(K(fs, xr, yr, pts=pts, label=label), label)


def figure(pts, segs, sides=(), right=(), W=340, H=230, label="gambar bangun", ticks=(), dashed=()):
    from fr_c4 import figure as F
    return relabel(F(pts, segs, sides=sides, right=right, W=W, H=H, label=label, ticks=ticks, dashed=dashed), label)


def numline(lo, hi, marks=(), label="garis bilangan", step=1, every=1):
    """整数の数直線。marks: [(値, 文字)]"""
    n = (hi - lo) // step
    W = 480
    u = (W - 60) / float(n)
    X = lambda v: 30 + (v - lo) / float(step) * u
    y = 50
    s = [line(18, y, W - 14, y, INK, 2), "<path d='M%d %d l-9 -5 v10 z' fill='%s'/>" % (W - 10, y, INK)]
    for i in range(n + 1):
        v = lo + i * step
        s.append(line(X(v), y - 7, X(v), y + 7, INK, 1.6))
        if (v - lo) % (every * step) == 0 or v == 0:
            s.append(text(X(v), y + 27, num(v), 15, weight=600 if v == 0 else 400))
    for v, t in marks:
        s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (X(v), y, RED))
        s.append(text(X(v), y - 15, t, 17, col=RED, weight=700))
    return wrap(W, 90, "".join(s), label)


def bars(data, label="diagram batang", unit="", step=1, horiz=False):
    """data: [(nama, nilai)]"""
    from id_common import diagram_batang
    return relabel(diagram_batang(data, unit, label, step), label)


def pie(data, label="diagram lingkaran"):
    """data: [(nama, persen)] → diagram lingkaran dengan label persen"""
    import math
    cols = ["#5b8def", "#f2a541", "#5fbf77", "#e86a6a", "#a77fd8", "#4cc3c9"]
    cx, cy, r = 120, 120, 100
    s = []
    a0 = -90.0
    for i, (nm, p) in enumerate(data):
        a1 = a0 + 360.0 * float(p) / 100
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        big = 1 if a1 - a0 > 180 else 0
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='white' stroke-width='2'/>" % (cx, cy, x0, y0, r, r, big, x1, y1, cols[i % 6]))
        am = math.radians((a0 + a1) / 2)
        s.append(text(cx + r * 0.62 * math.cos(am), cy + r * 0.62 * math.sin(am) + 5, "%s%%" % dz(Fr(p)) if p else "", 14, weight=700, col="#fff"))
        a0 = a1
    for i, (nm, p) in enumerate(data):
        y = 40 + i * 28
        s.append("<rect x='250' y='%d' width='16' height='16' fill='%s'/>" % (y - 13, cols[i % 6]))
        s.append(text(274, y, nm, 15, anchor="start"))
    return wrap(400, 245, "".join(s), label)


def tab(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return "<table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (h, b)


def poly_ang(pts, angs, label="segitiga", names=None, W=320, H=220, sides=()):
    """多角形と内角の文字。pts: [(x, y)]（数学の座標）、angs: 各頂点の文字（"" なら描かない）"""
    import math
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    m = 30
    sc = min((W - 2 * m) / float(max(xs) - min(xs) or 1), (H - 2 * m) / float(max(ys) - min(ys) or 1))
    ox = (W - (max(xs) - min(xs)) * sc) / 2.0
    oy = (H - (max(ys) - min(ys)) * sc) / 2.0
    P = [(ox + (x - min(xs)) * sc, H - oy - (y - min(ys)) * sc) for x, y in pts]
    cx = sum(p[0] for p in P) / len(P)
    cy = sum(p[1] for p in P) / len(P)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (" ".join("%.1f,%.1f" % p for p in P), FILL, INK)]
    n = len(P)
    for i, (x, y) in enumerate(P):
        a, b = P[i - 1], P[(i + 1) % n]
        ux, uy = a[0] - x, a[1] - y
        vx, vy = b[0] - x, b[1] - y
        lu, lv = math.hypot(ux, uy), math.hypot(vx, vy)
        bx, by = ux / lu + vx / lv, uy / lu + vy / lv
        lb = math.hypot(bx, by) or 1
        if angs[i]:
            d = 30 if len(angs[i]) < 5 else 38
            s.append(text(x + bx / lb * d, y + by / lb * d + 5, angs[i], 14, col=BLUE, weight=700))
        if names:
            dx, dy = x - cx, y - cy
            ld = math.hypot(dx, dy) or 1
            s.append(text(x + dx / ld * 14, y + dy / ld * 14 + 5, names[i], 15))
    for i, j, t in sides:
        (x1, y1), (x2, y2) = P[i], P[j]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = mx - cx, my - cy
        ld = math.hypot(dx, dy) or 1
        s.append(text(mx + dx / ld * 16, my + dy / ld * 16 + 5, t, 14, col=BLUE))
    return wrap(W, H, "".join(s), label)


def sejajar(theta, marks, label="dua garis sejajar dipotong garis lain"):
    """garis g ∥ h dipotong garis k. marks: {posisi: teks}. posisi 1–4 di titik atas
    (1 kanan atas, 2 kiri atas, 3 kiri bawah, 4 kanan bawah), 5–8 sama di titik bawah"""
    import math
    W, H = 380, 220
    y1, y2 = 70, 160
    t = math.radians(theta)
    ux, uy = math.cos(t), -math.sin(t)
    xm = W / 2
    xa = xm + (y2 - y1) / 2 / math.tan(t)
    xb = xm - (y2 - y1) / 2 / math.tan(t)
    s = [line(20, y1, W - 20, y1, INK, 2), line(20, y2, W - 20, y2, INK, 2),
         line(xb - ux * 60, y2 - uy * 60, xa + ux * 60, y1 + uy * 60, INK, 2),
         text(W - 14, y1 - 8, "g", 16, italic=True), text(W - 14, y2 - 8, "h", 16, italic=True),
         text(xa + ux * 60 + 10, y1 + uy * 60 + 4, "k", 16, italic=True)]
    dirs = {1: ((1, 0), (ux, uy)), 2: ((-1, 0), (ux, uy)), 3: ((-1, 0), (-ux, -uy)), 4: ((1, 0), (-ux, -uy))}
    for p, tx in marks.items():
        cx_, cy_ = (xa, y1) if p <= 4 else (xb, y2)
        (ax, ay), (bx, by) = dirs[(p - 1) % 4 + 1]
        vx, vy = ax + bx, ay + by
        lv = math.hypot(vx, vy)
        d = 30 if len(tx) < 4 else 40
        s.append(text(cx_ + vx / lv * d, cy_ + vy / lv * d + 5, tx, 15, col=RED if tx[0].isalpha() else BLUE, weight=700))
    return wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ units
def unit(slug, dom, sort, title, short, std, meta, kb, ks, sets, think, ex, mist, faq):
    return dict(slug=slug, dom=dom, sort=sort, title=title, short=short, std=std, meta=meta, kb=kb, ks=ks,
                sets=sets, think=think, ex=ex, mist=mist, faq=faq)


FASE = {7: "Fase D", 8: "Fase D", 9: "Fase D", 10: "Fase E", 11: "Fase F", 12: "Fase F"}


def modname(lv):
    """Kelas 7–9: id_smpN、Kelas 10–12: id_smaN"""
    return ("id_smp%d" if lv <= 9 else "id_sma%d") % lv


def mat(rows, det=False):
    """matriks (det=True: determinan dengan garis tegak)"""
    n = len(rows[0])
    cells = "".join("<span>%s</span>" % (c if isinstance(c, str) else sn(c)) for row in rows for c in row)
    return "<span class='mx%s m%d'>%s</span>" % (" det" if det else "", n, cells)


def build(lv, i):
    global R
    mod = __import__(modname(lv))
    R = random.Random(40000 + 100 * lv + i)
    mod.S.R = R
    d = mod.UNITS[i - 1]()
    seen = set()
    sets = []
    for t, parts in d["sets"]:
        try:
            sets.append((t, mix(R, seen, parts)))
        except AssertionError as e:
            raise AssertionError("%s / %s / %s: %s" % (d["slug"], t, [m.__name__ for m, _ in parts], e))
    body = lesson(d["think"], [example(*x) for x in d["ex"]], d["mist"])
    faq = [{"q": a, "a": b} for a, b in d["faq"]]
    make_unit(R, d["slug"], d["dom"], d["std"] + " (Capaian Pembelajaran %s)" % FASE[lv], d["title"], d["short"], d["meta"],
              d["kb"], d["ks"], body, faq, sets, d["sort"], grade="kelas-%d" % lv, fase=FASE[lv])
    return d["slug"]


if __name__ == "__main__":
    lv = int(sys.argv[1])
    want = sys.argv[2:]
    mod = __import__(modname(lv))
    for i in range(1, len(mod.UNITS) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(lv, i), flush=True)
