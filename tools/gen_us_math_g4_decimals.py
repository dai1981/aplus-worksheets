# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Decimals, Tenths and Hundredths (4.NF.C.5, 4.NF.C.6, 4.NF.C.7)
  python3 tools/gen_us_math_g4_decimals.py
All amounts are kept as whole numbers of hundredths (47 = 0.47), so no float rounding can creep in.
Every 10 x 10 grid is drawn from that number: full columns are tenths, the next column is filled from the top.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
LINE = "#2b2b2b"
THIN = "#8a8a8a"      # lines between small squares
RED = "#d6453b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def D(h, places=None):
    """Decimal text for h hundredths. places: 1 or 2 (default: 1 if h is whole tenths, else 2)."""
    if places is None:
        places = 1 if h % 10 == 0 else 2
    if places == 1:
        assert h % 10 == 0, h
        return "%d.%d" % (h // 100, (h % 100) // 10)
    return "%d.%02d" % (h // 100, h % 100)


NUM = re.compile(r"^\$?(\d+\.\d+|\d+)( \w+)?$")


def value(c):
    """Numeric value of a plain decimal choice like '0.30', '$0.3' or '0.3 m' (None if not a number)."""
    m = NUM.match(c)
    return (float(m.group(1)), m.group(2)) if m else None


def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    vc = value(correct)
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        v = value(c)
        if vc and v and v[1] == vc[1] and abs(v[0] - vc[0]) < 1e-9:      # 0.3 and 0.30 are both right
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, ai, e):
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def squ(n):
    return "1 square" if n == 1 else "%d squares" % n


def tenths_words(t):
    return "1 tenth" if t == 1 else "%d tenths" % t


def hund_words(h):
    return "1 hundredth" if h == 1 else "%d hundredths" % h


# ------------------------------------------------------------ pictures
def grid_body(k, ox, oy, cell):
    """10 x 10 grid at (ox, oy) with k squares shaded: full columns first, then from the top of the next column."""
    assert 0 <= k <= 100
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (ox + c * cell, oy + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox + i * cell, oy, ox + i * cell, oy + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox, oy + i * cell, ox + 10 * cell, oy + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (ox, oy, 10 * cell, 10 * cell, LINE))
    return "".join(s)


def grid_svg(k, cell=18):
    pad = 4
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, grid_body(k, pad, pad, cell), "hundredths grid with %s shaded" % squ(k))


def grids_svg(ks, labels=None, cell=17):
    """Several hundredths grids in a row, optional label under each."""
    pad, gap = 4, 22
    g = 10 * cell
    W = 2 * pad + len(ks) * g + (len(ks) - 1) * gap
    H = 2 * pad + g + (30 if labels else 0)
    s = []
    for i, k in enumerate(ks):
        x0 = pad + i * (g + gap)
        s.append(grid_body(k, x0, pad, cell))
        if labels:
            s.append("<text x='%d' y='%d' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x0 + g // 2, pad + g + 25, LINE, labels[i]))
    return svg_wrap(W, H, "".join(s), "hundredths grids with %s shaded" % " and ".join(squ(k) for k in ks))


def bar_svg(k, W=300, H=44):
    """Tenths bar: 10 equal parts, first k shaded."""
    s = []
    for i in range(10):
        s.append("<rect x='%d' y='6' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (6 + i * W // 10, W // 10, H, FILL if i < k else "#fff", LINE))
    return svg_wrap(W + 12, H + 12, "".join(s), "tenths bar split into 10 equal parts with %d shaded" % k)


def line_svg(a, b, spaces, dot=None, letters=None, labels=None, W=None):
    """Number line from a to b hundredths with `spaces` equal spaces.
    dot: hundredths value for a red dot. letters: {hundredths: letter}. labels: hundredths values to write under the line."""
    W = W or 380
    L, R, Y = 26, W - 26, 66 if letters else 30
    step = (b - a) / float(spaces)
    assert step == int(step)
    step = int(step)

    def X(v):
        return L + (R - L) * (v - a) / float(b - a)
    labels = labels if labels is not None else [a, b]
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(spaces + 1):
        v = a + i * step
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (13 if big else 8), X(v), Y + (13 if big else 8), LINE, "2.5" if big else "1.8"))
    for v in labels:
        txt = str(v // 100) if v % 100 == 0 and step >= 10 else D(v)
        s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X(v), Y + 36, LINE, txt))
    if dot is not None:
        assert (dot - a) % step == 0 and a <= dot <= b
        s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(dot), Y, RED))
    prev, up = None, False
    for v, ch in sorted((letters or {}).items()):
        assert (v - a) % step == 0 and a <= v <= b
        up = (not up) if prev is not None and v - prev == step else False      # neighbours: lift every other letter
        prev = v
        s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (X(v), Y, RED))
        if up:
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2'/>" % (X(v), Y - 8, X(v), Y - 32, LINE))
        s.append("<text x='%.1f' y='%d' font-size='18' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
                 % (X(v), Y - (38 if up else 18), LINE, ch))
    H = Y + 46
    return svg_wrap(W, H, "".join(s), "number line from %s to %s split into %d equal spaces" % (D(a), D(b), spaces))


# ============================================================ set 1: grids and bars
def grid_dec_wrong(k):
    if k < 10:
        return ["0.%d" % k, "%d" % k, "0.%d" % (100 - k)]
    return ["%d.%d" % (k // 10, k % 10), "0.%02d" % (100 - k), "%d" % k]


def grid_dec_e(k):
    t, h = k // 10, k % 10
    if t == 0:
        return ("The grid has 100 equal squares, so each square is 1 hundredth. Only <b>%s</b> shaded and there is no full column, "
                "so there are 0 tenths. %s = %s = <b>%s</b>." % ("1 square is" if k == 1 else "%d squares are" % k, hund_words(k), fr(k, 100), D(k)))
    return ("The grid has 100 equal squares, so each square is 1 hundredth and each full column is 1 tenth. "
            "<b>%s</b> and <b>%s</b> are shaded: %s and %s. That is %s = <b>%s</b>."
            % ("1 full column" if t == 1 else "%d full columns" % t, squ(h), tenths_words(t), hund_words(h), fr(k, 100), D(k)))


def set_grids(rnd):
    its = []
    for k in [47, 8, 62, 15, 3, 91, 56]:
        its.append(mcq(fig(grid_svg(k)) + "What decimal names the shaded part of the grid?",
                       D(k), grid_dec_wrong(k), grid_dec_e(k), rnd))

    for k in [30, 24, 9]:
        wrong = [fr(k // 10, 100), fr(100 - k, 100), fr(k, 10)] if k % 10 == 0 else [fr(k, 10), fr(100 - k, 100), fr(k, 100 - k)]
        e = ("Count the shaded squares: %s out of 100 equal squares. The fraction is %s. "
             "The bottom number is all 100 squares, not the white ones." % (squ(k), fr(k, 100)))
        if k % 10 == 0:
            e += " (It is also %s, because %d full columns are shaded.)" % (fr(k // 10, 10), k // 10)
        its.append(mcq(fig(grid_svg(k)) + "What fraction of the grid is shaded? Use hundredths.", fr(k, 100), wrong, e, rnd))

    for k, ask in [(7, "dec"), (3, "dec"), (9, "frac"), (4, "frac")]:
        if ask == "dec":
            e = ("The bar has 10 equal parts, so each part is 1 tenth. %d parts are shaded: %s = <b>%s</b>. "
                 "One digit after the point means tenths." % (k, fr(k, 10), D(k * 10)))
            its.append(mcq(fig(bar_svg(k)) + "The whole bar is 1. What decimal is shaded?", D(k * 10),
                           ["0.0%d" % k, "%d.10" % k, "0.%d" % (10 - k)], e, rnd))
        else:
            e = "The bar has <b>10 equal parts</b> and %d are shaded, so the shaded part is %s (%s)." % (k, fr(k, 10), D(k * 10))
            its.append(mcq(fig(bar_svg(k)) + "The whole bar is 1. What fraction is shaded?", fr(k, 10),
                           [fr(k, 100), fr(10 - k, 10), fr(k, 10 - k)], e, rnd))

    for k in [25, 6]:
        e = ("Each grid is 1 whole. The first grid is all shaded: <b>1 whole</b>. The second grid has %s = %s. "
             "Together: 1 and %s = <b>%s</b>." % (hund_words(k), D(k), hund_words(k), D(100 + k)))
        wrong = ["0.%02d" % k, "%d.%d" % ((100 + k) // 10, k % 10), "1.%02d" % (100 - k)] if k >= 10 else \
                ["1.%d" % k, "0.%02d" % k, "1.%02d" % (100 - k)]
        its.append(mcq(fig(grids_svg([100, k])) + "Each grid is 1 whole. What decimal names the shaded part?",
                       D(100 + k), wrong, e, rnd))

    shade = [(40, ["4 squares", "60 squares", "6 squares"]),
             (35, ["5 squares", "65 squares", "3 squares"]),
             (9, ["90 squares", "91 squares", "9 columns"]),
             (72, ["7 squares", "28 squares", "7 columns"])]
    for h, wrong in shade:
        e = ("A hundredths grid has 100 squares, so you need the number of <b>hundredths</b>. %s = %s, so shade <b>%s</b>."
             % (D(h), fr(h, 100), squ(h)))
        if h % 10 == 0:
            e += " %s tenths is the same as %d hundredths: %d full columns." % (h // 10, h, h // 10)
        if h < 10:
            e += " The 0 in the tenths place means no full column."
        its.append(mcq("How many squares of a hundredths grid should you shade to show <b>%s</b>?" % D(h),
                       squ(h), wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read hundredths grids and tenths bars", "items": its}


# ============================================================ set 2: fractions, decimals and place value
def set_place(rnd):
    its = []
    for n in [7, 45, 3, 80, 16]:
        if n < 10:
            wrong = ["0.%d" % n, "%d.100" % n, "%d.0" % n]
            e = ("%s means %s. Hundredths need <b>two digits</b> after the point, so write a 0 in the tenths place: <b>%s</b>. "
                 "(0.%d would be %d tenths.)" % (fr(n, 100), hund_words(n), D(n), n, n))
        elif n % 10 == 0:
            wrong = ["0.0%d" % (n // 10), "%d.0" % (n // 10), "%d.100" % n]
            e = ("%s = %s, because %d hundredths is the same as %d tenths. Both name the same point: %s = %s."
                 % (fr(n, 100), D(n, 1), n, n // 10, D(n, 2), D(n, 1)))
        else:
            wrong = ["%d.%d" % (n // 10, n % 10), "%d.100" % n, "0.0%d" % n]
            e = ("%s means %d hundredths: %s and %s. The hundredths digit goes in the second place after the point: <b>%s</b>."
                 % (fr(n, 100), n, tenths_words(n // 10), hund_words(n % 10), D(n)))
        its.append(mcq("Write %s as a decimal." % fr(n, 100), D(n), wrong, e, rnd))

    dec_frac = [(60, [fr(6, 100), fr(1, 6), fr(6, 1)]),
                (9, [fr(9, 10), fr(90, 100), fr(1, 9)]),
                (32, [fr(32, 10), fr(3, 10), fr(2, 100)]),
                (5, [fr(5, 10), fr(50, 100), fr(1, 5)])]
    for h, wrong in dec_frac:
        if h % 10 == 0:
            right = fr(h // 10, 10)
            e = "%s has one digit after the point, so it means %s: %s." % (D(h), tenths_words(h // 10), right)
        else:
            right = fr(h, 100)
            e = ("%s has two digits after the point, so it means hundredths. %s = %s, which is %s."
                 % (D(h), D(h), hund_words(h), right))
        its.append(mcq("Which fraction is equal to <b>%s</b>?" % D(h), right, wrong, e, rnd))

    for t in [3, 7, 5]:
        q = "%s = <span class='fr'><span class='fn'><b>?</b></span><span class='fd'>100</span></span>" % fr(t, 10)
        e = ("To go from tenths to hundredths, cut each tenth into 10 hundredths. Multiply the top and bottom by 10: "
             "%s = %s. The bottom number grew by ×10, so the top number must too." % (fr(t, 10), fr(t * 10, 100)))
        its.append(mcq(q, str(t * 10), [str(t), str(t + 90), str(t * 100)], e, rnd))
    its.append(mcq("Which decimal is equal to <b>0.7</b>?", "0.70", ["0.07", "7.0", "0.17"],
                   "0.7 is 7 tenths. 7 tenths = 70 hundredths, so 0.7 = <b>0.70</b>. A 0 at the end does not change the value. "
                   "A 0 right after the point does: 0.07 is only 7 hundredths.", rnd))

    pv = [("0.58", "8", "8 hundredths", ["8 tenths", "8 tens", "8 ones"],
           "The 8 is the <b>second</b> digit after the point, the hundredths place. Its value is 8 hundredths (0.08)."),
          ("4.63", "6", "6 tenths", ["6 tens", "6 hundredths", "6 ones"],
           "The 6 is the <b>first</b> digit after the point, the tenths place. Its value is 6 tenths (0.6). "
           "Tens are on the left of the ones; tenths are on the right of the point.")]
    for num, dg, right, wrong, e in pv:
        its.append(mcq("What is the value of the <b>%s</b> in %s?" % (dg, num), right, wrong, e, rnd))
    its.append(mcq("Which digit is in the <b>hundredths</b> place in 17.35?", "5", ["3", "1", "7"],
                   "Places after the point: tenths first (3), then <b>hundredths</b> (5). The 1 is in the tens place, "
                   "not the hundreds place.", rnd))
    its.append(mcq("Which digit is in the <b>tenths</b> place in 52.86?", "8", ["6", "5", "2"],
                   "The tenths place is the <b>first</b> digit after the point: 8. The 5 is in the tens place, on the other side of the point.", rnd))

    words = [("thirty-six hundredths", "0.36", ["3.6", "36.0", "0.036"],
              "Hundredths means two digits after the point: 36 hundredths = %s = <b>0.36</b>." % fr(36, 100)),
             ("two and five tenths", "2.5", ["2.05", "0.25", "25.0"],
              "“And” marks the decimal point. 2 wholes and 5 tenths: <b>2.5</b>. (2.05 would be 5 hundredths.)"),
             ("four and seven hundredths", "4.07", ["4.7", "0.47", "7.04"],
              "4 wholes, then the point. 7 hundredths needs two places, so put a 0 in the tenths place: <b>4.07</b>.")]
    for w, right, wrong, e in words:
        its.append(mcq("Which decimal is <b>%s</b>?" % w, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fractions, decimals and place value", "items": its}


# ============================================================ set 3: number lines
def set_lines(rnd):
    its = []
    for k in [7, 3, 6, 9, 2, 4, 8, 1]:
        wrong = ["0.0%d" % k, "0.%d" % (k + 1) if k < 9 else "1.0", "0.%d" % (10 - k)]
        if k == 5:
            wrong[2] = "5"
        e = ("From 0 to 1 there are <b>10 equal spaces</b>, so each space is 1 tenth (0.1). The dot is %d %s from 0: "
             "%s = <b>%s</b>. Count spaces, not tick marks." % (k, "space" if k == 1 else "spaces", fr(k, 10), D(10 * k)))
        its.append(mcq(fig(line_svg(0, 100, 10, dot=10 * k)) + "What decimal is at the red dot?", D(10 * k), wrong, e, rnd))

    for k in [4, 7, 2, 9]:
        v = 100 + 10 * k
        wrong = ["0.%d" % k, "1.0%d" % k, "2.%d" % k]
        e = ("The line starts at <b>1</b>, not 0. Each space is 1 tenth. The dot is %d %s past 1: 1 and %s = <b>%s</b>."
             % (k, "space" if k == 1 else "spaces", tenths_words(k), D(v)))
        its.append(mcq(fig(line_svg(100, 200, 10, dot=v)) + "What decimal is at the red dot?", D(v), wrong, e, rnd))

    zoom = [(30, 36), (70, 72), (10, 18), (50, 55)]
    for a, v in zoom:
        k = v - a
        wrong = ["0.0%d" % k, D(v + 1), "%d.%d" % (v // 10, v % 10)]
        e = ("This line goes from %s to %s, which is 1 tenth. It is cut into <b>10 equal spaces</b>, so each space is "
             "1 hundredth. %s = %s. The dot is %d %s past %s: <b>%s</b>."
             % (D(a), D(a + 10), D(a, 1), D(a, 2), k, "space" if k == 1 else "spaces", D(a, 2), D(v)))
        its.append(mcq(fig(line_svg(a, a + 10, 10, dot=v)) + "What decimal is at the red dot?", D(v), wrong, e, rnd))

    # letters go left to right; the right point lands on A, B, C and D once each
    pts = [(0, 100, 10, 30, [20, 40, 70], [0, 100]),
           (0, 100, 10, 60, [40, 50, 70], [0, 100]),
           (0, 200, 20, 180, [80, 120, 170], [0, 100, 200]),
           (0, 200, 20, 80, [90, 120, 180], [0, 100, 200])]
    for a, b, sp, good, bads, labs in pts:
        order = sorted(bads + [good])
        letters = {v: "ABCD"[i] for i, v in enumerate(order)}
        L = letters[good]
        ai = "ABCD".index(L)
        if good > 100:
            e = ("Find 1 first, then count %d %s past it. Each space is 1 tenth, so %s is at point <b>%s</b>. "
                 "(%s, without the whole, would be %d spaces from 0.)" % ((good - 100) // 10, "space" if good == 110 else "spaces",
                                                                          D(good), L, D(good - 100), (good - 100) // 10))
        else:
            e = ("Each space is 1 tenth. %s is %s, so count %d spaces from 0. That is point <b>%s</b>."
                 % (D(good), tenths_words(good // 10), good // 10, L))
        its.append(mcq_fixed(fig(line_svg(a, b, sp, letters=letters, labels=labs)) + "Which point is at <b>%s</b>?" % D(good),
                             ["A", "B", "C", "D"], ai, e))
    assert len(its) == 20, len(its)
    return {"title": "Decimals on a number line", "items": its}


# ============================================================ set 4: add tenths and hundredths, compare
def cmp_choices(x, y, sign):
    a, b = D(x), D(y)
    lt, gt, eq = "%s &lt; %s" % (a, b), "%s &gt; %s" % (a, b), "%s = %s" % (a, b)
    return {"<": lt, ">": gt, "=": eq}[sign], [lt, gt, eq, "You can’t compare"]


def set_add_compare(rnd):
    its = []
    for t, h in [(3, 45), (2, 6), (5, 31), (6, 18), (4, 9)]:
        s = 10 * t + h
        e = ("You can only add parts of the <b>same size</b>. Change tenths to hundredths: %s = %s. "
             "Then add: %s + %s = <b>%s</b>. Never add the bottom numbers." % (fr(t, 10), fr(10 * t, 100), fr(10 * t, 100), fr(h, 100), fr(s, 100)))
        its.append(mcq("%s + %s = ?" % (fr(t, 10), fr(h, 100)), fr(s, 100),
                       [fr(t + h, 110), fr(t + h, 100), fr(t + h, 10)], e, rnd))
    for t, h in [(4, 25), (7, 45)]:
        s = 10 * t + h
        e = ("%s = %s, so %s + %s = %s = <b>%s</b>." % (fr(t, 10), fr(10 * t, 100), fr(10 * t, 100), fr(h, 100), fr(s, 100), D(s)))
        if s > 100:
            e += " That is more than 1 whole, because 100 hundredths make 1."
        wrong = ["0.%d" % (t + h), "0.%d%d" % (t, h), "%d.%d" % (s // 10, s % 10)]
        its.append(mcq("Add. Write the sum as a decimal.<br>%s + %s = ?" % (fr(t, 10), fr(h, 100)), D(s), wrong, e, rnd))

    pairs = [(50, 45, "long"), (30, 28, "long"), (7, 70, "zero"), (90, 89, "long"), (42, 40, "x"),
             (130, 95, "whole"), (25, 30, "x"), (60, 60, "eq")]
    for x, y, kind in pairs:
        sign = "<" if x < y else (">" if x > y else "=")
        if kind == "eq":
            right, ch = "0.6 = 0.60", ["0.6 &lt; 0.60", "0.6 &gt; 0.60", "0.6 = 0.60", "You can’t compare"]
            e = "0.6 is 6 tenths, and 6 tenths = 60 hundredths = 0.60. A 0 at the end does not change the value, so they are <b>equal</b>."
        else:
            right, ch = cmp_choices(x, y, sign)
            big, small = max(x, y), min(x, y)
            tens = [v for v in (x, y) if v % 10 == 0]
            e = ("Write %s with hundredths: %s. Now compare %s and %s: %s."
                 % (D(tens[0]), "%s = %s" % (D(tens[0]), D(tens[0], 2)), hund_words(x), hund_words(y), right))
            if kind == "long":
                e += " A longer number is not always bigger: compare the tenths first."
            if kind == "zero":
                e += " 0.07 has 0 tenths; 0.7 has 7 tenths."
            if kind == "whole":
                e = "Compare the ones first: %s has 1 whole and %s has 0 wholes, so %s." % (D(x), D(y), right)
        its.append(mcq("Compare the decimals.", right, ch, e, rnd))

    its.append(mcq(fig(grids_svg([50, 45], ["A", "B"])) + "Grid A shows 0.5. Grid B shows 0.45. Which is true?",
                   "0.5 &gt; 0.45", ["0.5 &lt; 0.45", "0.5 = 0.45", "You can’t compare"],
                   "Count squares: A has 50 shaded and B has 45. More of grid A is shaded, so 0.5 &gt; 0.45, "
                   "even though 45 is bigger than 5.", rnd))

    its.append(mcq("Which decimal is the <b>greatest</b>?", "0.6", ["0.45", "0.38", "0.09"],
                   "Compare the tenths first: 0.6 has 6 tenths, while 0.45, 0.38 and 0.09 have 4, 3 and 0 tenths. "
                   "<b>0.6</b> is the greatest, even though it has fewer digits.", rnd))
    its.append(mcq("Which decimal is the <b>smallest</b>?", "0.05", ["0.5", "0.15", "0.51"],
                   "Compare the tenths first: 0.05 has <b>0 tenths</b>, while 0.5, 0.15 and 0.51 have 5, 1 and 5 tenths. "
                   "So 0.05 is the smallest.", rnd))
    its.append(mcq("Order from <b>least to greatest</b>.", "0.09, 0.4, 0.62",
                   ["0.4, 0.09, 0.62", "0.62, 0.4, 0.09", "0.09, 0.62, 0.4"],
                   "Write them all as hundredths: 0.09 = 9, 0.4 = 40, 0.62 = 62 hundredths. "
                   "9 &lt; 40 &lt; 62, so the order is 0.09, 0.4, 0.62.", rnd))
    its.append(mcq("Order from <b>greatest to least</b>.", "1.2, 0.8, 0.75",
                   ["0.75, 0.8, 1.2", "0.75, 1.2, 0.8", "0.8, 0.75, 1.2"],
                   "1.2 has a whole, so it is the greatest. Then 0.8 = 0.80 is more than 0.75. "
                   "The order is 1.2, 0.8, 0.75.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Add tenths and hundredths, compare decimals", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    its = []
    P = People(rnd)

    for d, p, wrong in [(3, 4, ["$0.07", "$3.04", "$0.43"]), (5, 0, ["$0.05", "$5.00", "$5.10"]), (1, 8, ["$0.09", "$1.08", "$0.81"])]:
        n, he, his = P.next()
        coins = []
        if d:
            coins.append("1 dime" if d == 1 else "%d dimes" % d)
        if p:
            coins.append("1 penny" if p == 1 else "%d pennies" % p)
        right = "$" + D(10 * d + p, 2)
        q = ("A dime is %s of a dollar and a penny is %s of a dollar. %s has %s. "
             "How much money does %s have?" % (fr(1, 10), fr(1, 100), n, " and ".join(coins), he))
        parts = []
        if d:
            parts.append("%d %s = %s" % (d, "dime" if d == 1 else "dimes", fr(d, 10)))
        if p:
            parts.append("%d %s = %s" % (p, "penny" if p == 1 else "pennies", fr(p, 100)))
        if d and p:
            e = "%s. In all: %s of a dollar = <b>%s</b>." % (", ".join(parts), fr(10 * d + p, 100), right)
        else:
            e = "%s = %s of a dollar = <b>%s</b>." % (parts[0], fr(10 * d + p, 100), right)
        if p == 0:
            e += " 5 tenths = 50 hundredths, which is 50 cents."
        if d and p:
            e += " Count the value, not the number of coins."
        its.append(mcq(q, right, wrong, e, rnd))

    n, he, his = P.next()
    its.append(mcq("%s wants to pay $0.85 with only dimes and pennies, using the fewest coins. Which coins does %s use?" % (n, he),
                   "8 dimes, 5 pennies", ["5 dimes, 8 pennies", "85 dimes", "85 pennies"],
                   "$0.85 = 8 tenths and 5 hundredths. A dime is a tenth and a penny is a hundredth: "
                   "<b>8 dimes and 5 pennies</b>. 85 pennies is also $0.85, but it uses many more coins.", rnd))

    n, he, his = P.next()
    its.append(mcq("%s has 4 dimes. %s finds 25 pennies. How much money does %s have now?" % (n, cap(he), he),
                   "$0.65", ["$0.29", "$4.25", "$0.425"],
                   "4 dimes = %s = %s. Add the pennies: %s + %s = %s = <b>$0.65</b>. Do not add 4 and 25: "
                   "a dime is worth 10 pennies." % (fr(4, 10), fr(40, 100), fr(40, 100), fr(25, 100), fr(65, 100)), rnd))

    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s has 6 dimes. %s has 5 dimes and 8 pennies. Who has more money?" % (a, b), a,
                   [b, "They have the same", "You can’t tell"],
                   "%s has $0.60. %s has $0.58. 60 cents is more than 58 cents, so <b>%s</b> has more, "
                   "even though %s has more coins." % (a, b, a, b), rnd))

    its.append(mcq("How many pennies make <b>0.3</b> of a dollar?", "30 pennies", ["3 pennies", "70 pennies", "300 pennies"],
                   "0.3 = %s = %s. A penny is 1 hundredth of a dollar, so you need <b>30 pennies</b> (30 cents)."
                   % (fr(3, 10), fr(30, 100)), rnd))

    n, he, his = P.next()
    its.append(mcq("A plant grew 0.3 meter in spring and 0.25 meter in summer. How much did it grow in all?",
                   "0.55 m", ["0.28 m", "0.325 m", "5.5 m"],
                   "0.3 = %s. Add hundredths to hundredths: %s + %s = %s = <b>0.55 m</b>. "
                   "Line up the tenths with the tenths." % (fr(30, 100), fr(30, 100), fr(25, 100), fr(55, 100)), rnd))

    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s jumped 1.4 meters. %s jumped 1.35 meters. Who jumped farther?" % (a, b), a,
                   [b, "They jumped the same", "You can’t tell"],
                   "Both jumped 1 whole meter. Compare the tenths: 1.4 has 4 tenths, 1.35 has 3 tenths. "
                   "1.4 = 1.40 &gt; 1.35, so <b>%s</b> jumped farther. More digits does not mean bigger." % a, rnd))

    its.append(mcq("Three pencils are 0.15 m, 0.2 m and 0.12 m long. Which pencil is the <b>shortest</b>?",
                   "0.12 m", ["0.2 m", "0.15 m", "They are equal"],
                   "Write all as hundredths: 0.15 = 15, 0.2 = 20, 0.12 = 12 hundredths. The shortest is <b>0.12 m</b>. "
                   "0.2 is not the shortest: 2 tenths is 20 hundredths.", rnd))

    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s ate 0.5 of a small pizza. %s ate 0.4 of a large pizza. %s says %s ate more because 0.5 &gt; 0.4. "
                   "Is %s right?" % (a, b, a, ah, ah),
                   "Not sure: wholes differ", ["Yes, 0.5 &gt; 0.4", "No, 0.4 &gt; 0.5", "Yes, 5 &gt; 4"],
                   "You can compare decimals only when they are parts of the <b>same whole</b>. Half of a small pizza "
                   "can be less than 0.4 of a large pizza, so %s cannot be sure." % a, rnd))

    its.append(mcq("Two water bottles are the same size. One is 0.8 full. The other is 0.75 full. Which has more water?",
                   "The 0.8 bottle", ["The 0.75 bottle", "They are the same", "You can’t tell"],
                   "The bottles are the same size, so you can compare. 0.8 = 0.80, and 80 hundredths &gt; 75 hundredths. "
                   "The <b>0.8 bottle</b> has more.", rnd))

    its.append(mcq("A garden has 100 equal plots. Tomatoes grow in 23 of them. What decimal names the part with tomatoes?",
                   "0.23", ["2.3", "0.77", "23.0"],
                   "23 out of 100 equal plots is %s = <b>0.23</b>." % fr(23, 100), rnd))

    its.append(mcq("A class has 10 students. 7 of them walk to school. What decimal names the part of the class that walks?",
                   "0.7", ["0.07", "7.10", "0.3"],
                   "7 out of 10 students is %s. Tenths have one digit after the point: <b>0.7</b>. (0.3 is the part that does not walk.)"
                   % fr(7, 10), rnd))

    n, he, his = P.next()
    its.append(mcq("A recipe needs 0.5 liter of milk and 0.25 liter of cream. How much is that in all?",
                   "0.75 L", ["0.30 L", "0.525 L", "7.5 L"],
                   "0.5 = %s = %s. Then %s + %s = %s = <b>0.75 L</b>. Add tenths to tenths and hundredths to hundredths."
                   % (fr(5, 10), fr(50, 100), fr(50, 100), fr(25, 100), fr(75, 100)), rnd))

    its.append(mcq("A meter has 100 centimeters. A crayon is 9 centimeters long. How long is it in meters?",
                   "0.09 m", ["0.9 m", "9 m", "0.91 m"],
                   "Each centimeter is %s of a meter. 9 centimeters = %s = <b>0.09 m</b>. "
                   "(0.9 m would be 90 centimeters.)" % (fr(1, 100), fr(9, 100)), rnd))

    n, he, his = P.next()
    its.append(mcq("%s says 0.3 = 0.30. Is %s right?" % (n, he), "Yes, they are equal",
                   ["No, 0.30 is bigger", "No, 0.3 is bigger", "Only for money"],
                   "0.3 is 3 tenths. 3 tenths = 30 hundredths = 0.30. A 0 at the end does not change the value, "
                   "so %s is <b>right</b>." % n, rnd))

    n, he, his = P.next()
    its.append(mcq("A board 1 meter long is cut into 10 equal pieces. %s uses 4 pieces. How many meters of board does %s use?" % (n, he),
                   "0.4 m", ["0.04 m", "4 m", "0.6 m"],
                   "Each piece is %s of a meter. 4 pieces = %s = <b>0.4 m</b>." % (fr(1, 10), fr(4, 10)), rnd))

    n, he, his = P.next()
    its.append(mcq("A trail has a sign every tenth of a mile. %s walks past the 1-mile sign and then 3 more signs. "
                   "How far has %s walked?" % (n, he), "1.3 miles", ["0.3 mile", "1.03 miles", "4 miles"],
                   "1 mile, then 3 tenths more: 1 + 0.3 = <b>1.3 miles</b>. Each sign is 0.1 mile, not 0.01.", rnd))

    n, he, his = P.next()
    its.append(mcq("A rope is 0.6 meter long. %s adds a piece that is 0.08 meter long. How long is the rope now?" % n,
                   "0.68 m", ["0.14 m", "0.608 m", "1.4 m"],
                   "0.6 = %s. Then %s + %s = %s = <b>0.68 m</b>. The 8 is hundredths, so it goes in the second place."
                   % (fr(60, 100), fr(60, 100), fr(8, 100), fr(68, 100)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Money and measurement word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_grid = grid_svg(47, cell=22)
    f_same = svg_wrap(400, 222, "".join([
        "".join("<rect x='%d' y='%d' width='18' height='180' fill='%s' stroke='%s' stroke-width='2'/>"
                % (6 + i * 18, 6, FILL if i < 3 else "#fff", LINE) for i in range(10)),
        "<text x='96' y='214' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>3 tenths</text>" % LINE,
        grid_body(30, 214, 6, 18),
        "<text x='304' y='214' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>30 hundredths</text>" % LINE,
    ]), "a tenths bar with 3 parts shaded and a hundredths grid with 30 squares shaded: the same amount")
    f_cmp = grids_svg([50, 45], ["0.5", "0.45"], cell=18)
    f_line = line_svg(0, 100, 10, dot=60)
    return (
        "<h2>Tenths and hundredths</h2>"
        "<p>Cut 1 whole into <b>10 equal parts</b>: each part is one <b>tenth</b>, " + fr(1, 10) + " = 0.1. "
        "Cut it into <b>100 equal parts</b>: each part is one <b>hundredth</b>, " + fr(1, 100) + " = 0.01.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>The whole grid is 1. 4 full columns (4 tenths) and 7 more squares (7 hundredths) are shaded: "
        + fr(47, 100) + " = 0.47.</figcaption></figure>"
        "<h2>Tenths are hundredths too</h2>"
        "<p>Each tenth is 10 hundredths. Multiply the top and bottom by 10 to write tenths as hundredths.</p>"
        "<figure class='sn-fig'>" + f_same +
        "<figcaption>" + fr(3, 10) + " = " + fr(30, 100) + ", so 0.3 = 0.30. A 0 at the end does not change the value.</figcaption></figure>"
        + ex("Example", "Add " + fr(3, 10) + " + " + fr(45, 100) + ".",
             "Make the parts the same size first: " + fr(3, 10) + " = " + fr(30, 100) + ". Then " + fr(30, 100) + " + "
             + fr(45, 100) + " = " + fr(75, 100) + ".", fr(75, 100) + " = 0.75")
        + "<h2>Place value after the point</h2>"
        + table(["Number", "Ones", ".", "Tenths", "Hundredths", "Fraction"], [
            ["0.47", "0", ".", "4", "7", fr(47, 100)],
            ["0.07", "0", ".", "0", "7", fr(7, 100)],
            ["0.7", "0", ".", "7", "", fr(7, 10)],
            ["2.05", "2", ".", "0", "5", "2 and " + fr(5, 100)],
        ]) +
        "<p>The first place after the point is tenths. The second place is hundredths. "
        "Use a 0 to hold a place: " + fr(7, 100) + " is 0.07, not 0.7.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>From 0 to 1 there are 10 equal spaces, so each space is 0.1. The dot is 6 spaces from 0: 0.6.</figcaption></figure>"
        "<h2>Comparing decimals</h2>"
        "<p>Compare the ones, then the tenths, then the hundredths. Or write both numbers in hundredths.</p>"
        "<figure class='sn-fig'>" + f_cmp +
        "<figcaption>0.5 = 50 hundredths and 0.45 = 45 hundredths, so 0.5 &gt; 0.45.</figcaption></figure>"
        "<p>Compare decimals only when they are parts of the <b>same whole</b>. 0.5 of a small pizza can be less than "
        "0.4 of a large pizza.</p>"
        + ex("Example", "Which is greater: 0.8 or 0.75?",
             "Write 0.8 as 0.80. 80 hundredths is more than 75 hundredths.", "0.8 is greater")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing " + fr(7, 100) + " as 0.7", "Hundredths use two places: 0.07"],
            ["Thinking 0.45 &gt; 0.5 because 45 &gt; 5", "Compare tenths first, or write 0.5 as 0.50"],
            ["Adding " + fr(3, 10) + " + " + fr(45, 100) + " to get " + fr(48, 110), "Change tenths to hundredths, then add the tops only"],
            ["Writing " + fr(7, 10) + " as 7.10", "The bottom number is not written. " + fr(7, 10) + " = 0.7"],
            ["Comparing parts of different wholes", "Check that both decimals name parts of the same whole"],
        ])
    )


FAQ = [
    {"q": "How do you explain tenths and hundredths to 4th graders?",
     "a": "Use one whole cut into 10 equal parts (tenths) and into 100 equal parts (hundredths). On a hundredths grid, one column is 1 tenth (0.1) and one small square is 1 hundredth (0.01)."},
    {"q": "How do you write a fraction with a denominator of 10 or 100 as a decimal?",
     "a": "Tenths use one place after the point and hundredths use two: 3/10 = 0.3 and 45/100 = 0.45. If the top number is less than 10, add a 0: 7/100 = 0.07."},
    {"q": "How do you add 3/10 and 45/100?",
     "a": "First change the tenths to hundredths: 3/10 = 30/100. Then add the top numbers: 30/100 + 45/100 = 75/100, or 0.75."},
    {"q": "Why is 0.5 bigger than 0.45?",
     "a": "0.5 is 5 tenths, which is 50 hundredths, and 0.45 is 45 hundredths. 50 hundredths is more, so 0.5 is bigger even though it has fewer digits."},
]


def gen_decimals():
    rnd = random.Random(107)
    sets = [set_grids(rnd), set_place(rnd), set_lines(rnd), set_add_compare(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "decimals-tenths-hundredths", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Decimals: Tenths and Hundredths",
        "seo_title": "Grade 4 Decimals Worksheets: Tenths and Hundredths, Decimal Fractions, Number Lines and Comparing Decimals",
        "short_title": "Decimals",
        "domain": "Number and Operations—Fractions",
        "standard_code": "4.NF.C.5–7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NF/C/6/",
        "standard_text": "Express a fraction with denominator 10 as an equivalent fraction with denominator 100, and use this technique to add two fractions with respective denominators 10 and 100. Use decimal notation for fractions with denominators 10 or 100. Compare two decimals to hundredths by reasoning about their size, recognizing that comparisons are valid only when the two decimals refer to the same whole.",
        "meta_desc": "Free Grade 4 decimals worksheets with hundredths grids: write tenths and hundredths as fractions and decimals, place decimals on a number line, add 3/10 + 45/100 and compare decimals like 0.5 and 0.45. 100 practice questions with answers.",
        "key_big": "Tenths use one place after the point; hundredths use two. 7/10 = 0.7 and 7/100 = 0.07.",
        "key_sub": "1 tenth = 10 hundredths, so 0.3 = 0.30. To compare or add, write both in hundredths: 0.5 = 0.50 is more than 0.45, and 3/10 + 45/100 = 30/100 + 45/100 = 75/100.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundredths grids, number lines) so squares and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_decimals()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "decimals-tenths-hundredths.json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "(hundredths grid|number line)")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
