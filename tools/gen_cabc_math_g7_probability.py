# -*- coding: utf-8 -*-
"""
BC Grade 7 Math: Probability of Two Independent Events
(BC Mathematics Curriculum, Grade 7: Data and probability, experimental probability with two independent events)
  python3 tools/gen_cabc_math_g7_probability.py
Sample spaces with outcome tables and tree diagrams (coin and number cube, two spinners, two number cubes),
theoretical probability of two independent events as a fraction, decimal and percent, experimental probability
from results tables, comparing experimental and theoretical probability (more trials get closer, expected counts,
predictions) and word problems in BC contexts (school fun fair, field trip draw, lacrosse practice, board games).
Wrong answers come from real student mistakes: adding the probabilities of the two events (1/2 + 1/6 = 4/6 instead
of 1/12), adding the outcomes instead of multiplying (2 + 6 = 8), treating HT and TH as one outcome, treating the
11 sums of two number cubes as equally likely, part-to-part instead of part-to-whole, using the count as a percent,
expecting an experiment to match the theory exactly, and the gambler's fallacy.
Helpers (spinners, tree diagrams, outcome and frequency tables) are adapted from gen_caon_math_g6_probability.py.
Every answer is checked in code with fractions.Fraction. Canadian English. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
GREEN = "#006633"
HEAD = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
COL = {"red": "#f08a80", "blue": "#8db4ee", "yellow": "#f7dc6f", "green": "#8fd19e",
       "purple": "#c9aef0", "white": "#ffffff", "grey": "#e4e4e4"}
INIT = {"red": "R", "blue": "B", "yellow": "Y", "green": "G", "purple": "P", "white": "W"}
NUMFILL = ["#f7dc6f", "#8db4ee", "#8fd19e", "#f08a80", "#c9aef0", "#ffd3a6", "#bfe3ef", "#e4e4e4"]


NB = " "


# ------------------------------------------------------------ helpers
def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


FRX = re.compile(r"<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>")


def val(s):
    """Numeric value of a choice (fraction, decimal or percentage), or None for words."""
    t = re.sub(r"<[^>]+>", "", FRX.sub(r"\1/\2", str(s))).replace(NB, "").strip()
    if re.match(r"^\d+/\d+$", t):
        n, d = t.split("/")
        return F(int(n), int(d))
    if re.match(r"^\d*\.?\d+%$", t):
        return F(t[:-1]) / 100
    if re.match(r"^\d*\.?\d+$", t):
        return F(t)
    return None


def mcq(q, correct, wrong, e, ans=None, same_ok=False):
    """4 choices: correct first + 3 wrong; positions are set later by balance().
    Numeric choices must all have different values (unless same_ok); ans checks the correct value."""
    ch = [str(correct)] + [str(x) for x in wrong]
    assert len(ch) == 4, (q, ch)
    plain = [re.sub(r"<[^>]+>", " ", x).strip() for x in ch]
    assert len(set(plain)) == 4, (q, ch)
    vals = [val(x) for x in ch]
    nums = [v for v in vals if v is not None]
    if not same_ok:
        assert len(set(nums)) == len(nums), ("two equal values", q, ch)
    if ans is not None:
        assert vals[0] == F(ans), (q, vals[0], ans)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcq_fixed(q, choices, ai, e):
    """Picture labels A, B, C, D stay in this order."""
    assert len(choices) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "fixed": True}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each). Fixed items keep their order."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fixed"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("fixed", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=True):
    return len(t) * fs * (0.62 if bold else 0.56)


def text(x, y, t, fs=15, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def reorder(its, order):
    assert sorted(order) == list(range(len(its))), order
    return [its[i] for i in order]


# ------------------------------------------------------------ pictures
def secs_of(spec):
    """spec: list of (label, fraction, fill-name or colour). Fractions must add up to 1."""
    assert sum(F(f) for _, f, _ in spec) == 1, spec
    return [(l, F(f), c) for l, f, c in spec]


def label_fits(R, f, t, fs):
    """Will text t fit horizontally inside a section of size f at 0.6R? (chord check, generous margins)"""
    r = R * 0.64
    ang = 2 * math.pi * float(f)
    chord = 2 * r * math.sin(min(ang, math.pi) / 2) if ang < 2 * math.pi else 2 * R
    return tw(t, fs) + 6 <= chord and r + fs / 2 + 2 <= R


def spinner_body(cx, cy, R, spec, fs=15, initials=False, pointer=True):
    """Spinner drawn to its exact fractions, starting at 12 o'clock and going clockwise."""
    s = []
    a0 = F(0)
    labels = []
    for lab, f, c in spec:
        fill = COL.get(c, c)
        a1 = a0 + f
        t0 = 2 * math.pi * float(a0) - math.pi / 2
        t1 = 2 * math.pi * float(a1) - math.pi / 2
        if f == 1:
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, R, fill, LINE))
        else:
            x0, y0 = cx + R * math.cos(t0), cy + R * math.sin(t0)
            x1, y1 = cx + R * math.cos(t1), cy + R * math.sin(t1)
            big = 1 if f > F(1, 2) else 0
            s.append("<path d='M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2' "
                     "stroke-linejoin='round'/>" % (cx, cy, x0, y0, R, R, big, x1, y1, fill, LINE))
        if lab:
            tm = (t0 + t1) / 2 if f < 1 else -math.pi / 2
            rr = R * 0.64 if f < 1 else R * 0.5
            t = INIT.get(lab, lab) if initials else lab
            assert label_fits(R, f, t, fs), (t, f, R)
            labels.append(text(cx + rr * math.cos(tm), cy + rr * math.sin(tm) + fs * 0.35, t, fs))
        a0 = a1
    s += labels
    if pointer:
        L = R * 0.28
        ang = math.radians(-50)
        tx, ty = cx + L * math.cos(ang), cy + L * math.sin(ang)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                 % (cx, cy, tx, ty, LINE))
        h1 = ang + math.radians(150)
        h2 = ang - math.radians(150)
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                 % (tx + 3 * math.cos(ang), ty + 3 * math.sin(ang), tx + 8 * math.cos(h1), ty + 8 * math.sin(h1),
                    tx + 8 * math.cos(h2), ty + 8 * math.sin(h2), LINE))
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (cx, cy, LINE))
    return "".join(s)


def key_line(names):
    return ",  ".join("%s = %s" % (INIT[n], n) for n in names)


def colours_in(spec):
    out = []
    for lab, _, _ in spec:
        if lab in INIT and lab not in out:
            out.append(lab)
    return out


def spinner_svg(spec, R=66, label="spinner"):
    spec = secs_of(spec)
    words = all(not l or label_fits(R, f, l, 14) for l, f, _ in spec)
    W = 2 * R + 12
    H = 2 * R + 12
    body = spinner_body(W / 2, R + 6, R, spec, fs=14 if words else 15, initials=not words)
    if not words:
        k = key_line(colours_in(spec))
        W = int(max(W, tw(k, 14, False) + 12))
        body = spinner_body(W / 2, R + 6, R, spec, initials=True)
        body += text(W / 2, 2 * R + 30, k, 14, weight=400)
        H = 2 * R + 38
    return svg_wrap(int(W), int(H), body, label)


def spinners4_svg(specs, label="four spinners"):
    """Spinners A, B, C, D in one row, initials and one key."""
    R = 44
    gap = 22
    cell = 2 * R + gap
    names = []
    for sp in specs:
        for n in colours_in(sp):
            if n not in names:
                names.append(n)
    W = 4 * cell
    s = []
    for i, sp in enumerate(specs):
        cx = gap / 2 + R + i * cell
        s.append(spinner_body(cx, R + 4, R, secs_of(sp), fs=15, initials=True))
        s.append(text(cx, 2 * R + 26, "ABCD"[i], 17))
    k = key_line(names)
    s.append(text(W / 2, 2 * R + 50, k, 15, weight=400))
    return svg_wrap(int(W), 2 * R + 58, "".join(s), label)


def bag_svg(counts, label="bag of marbles"):
    """A jar of marbles; each marble is coloured and carries its initial. counts: list of (colour, n)."""
    marbles = [c for c, n in counts for _ in range(n)]
    n = len(marbles)
    per = min(6, n) if n <= 12 else 7
    rows = (n + per - 1) // per
    r = 13
    d = 2 * r + 4
    jw = per * d + 16
    jh = rows * d + 18
    W = int(jw + 20)
    s = ["<path d='M 10 14 L 10 %.1f Q 10 %.1f 22 %.1f L %.1f %.1f Q %.1f %.1f %.1f %.1f L %.1f 14' fill='#f7f7f2' "
         "stroke='%s' stroke-width='2'/>" % (14 + jh - 12, 14 + jh, 14 + jh, 10 + jw - 12, 14 + jh, 10 + jw, 14 + jh,
                                             10 + jw, 14 + jh - 12, 10 + jw, LINE),
         "<rect x='4' y='6' width='%.1f' height='10' rx='3' fill='%s' stroke='%s' stroke-width='2'/>" % (jw + 12, "#d9cbb0", LINE)]
    # fill from the bottom row up so the jar looks natural
    for i, c in enumerate(marbles):
        row = rows - 1 - i // per
        inrow = min(per, n - (i // per) * per)
        x0 = 10 + (jw - inrow * d) / 2 + d / 2
        cx = x0 + (i % per) * d
        cy = 22 + row * d + d / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, r, COL[c], LINE))
        s.append(text(cx, cy + 5, INIT[c], 14))
    k = key_line([c for c, _ in counts])
    H = 14 + jh + 26
    W = int(max(W, tw(k, 14, False) + 12))
    if W > jw + 20:  # centre the jar under a wide key
        s = ["<g transform='translate(%.1f 0)'>" % ((W - jw - 20) / 2)] + s + ["</g>"]
    s.append(text(W / 2, H - 6, k, 14, weight=400))
    return svg_wrap(W, int(H), "".join(s), label)


def tally_marks(x, cy, v):
    s = []
    for g in range(v // 5):
        for k in range(4):
            xx = x + k * 6
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, LINE))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x - 3, cy + 6, x + 21, cy - 6, LINE))
        x += 30
    for k in range(v % 5):
        xx = x + k * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, LINE))
    return "".join(s)


def tally_width(v):
    return (v // 5) * 30 + (v % 5) * 6


def freq_svg(title, head, cats, vals, tally=True, label="frequency table"):
    fs, rh = 15, 28
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs)) + 20)
    cols = [c1]
    if tally:
        cols.append(int(max(max(tally_width(v) for v in vals) + 26, 70)))
    cols.append(int(tw("Frequency", fs) + 20))
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16) + 16))
    x0 = (W - tot) / 2
    s = [text(W / 2, 19, title, 16)]
    top = 28
    rows = [(head, None)] + list(zip(cats, vals))
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        x = x0
        for k, cw in enumerate(cols):
            hd = r == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, HEAD if hd or k == 0 else "#ffffff", GREEN))
            last = k == len(cols) - 1
            if k == 0:
                s.append(text(x + 10, y + 19, c, fs, anchor="start"))
            elif hd:
                s.append(text(x + cw / 2 if last else x + 10, y + 19, "Frequency" if last else "Tally", fs,
                              anchor="middle" if last else "start"))
            elif last:
                s.append(text(x + cw / 2, y + 19, v, fs))
            else:
                s.append(tally_marks(x + 14, y + rh / 2, v))
            x += cw
    H = top + len(rows) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def part(spec, name):
    return sum((f for l, f, _ in secs_of(spec) if l == name), F(0))


def scale_svg(den, marks, tick_labels, words=False, label="probability scale"):
    """Probability scale from 0 to 1 with ticks every 1/den. marks: (value, letter or '') arrows above the line."""
    W, x0, L, ly = 440, 28, 384, 56

    def X(v):
        return x0 + L * float(v)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, ly, x0 + L, ly, LINE)]
    for k in range(den + 1):
        v = F(k, den)
        h = 10 if v in (0, F(1, 2), 1) else 6
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), ly - h, X(v), ly + h, LINE))
    for v, t in tick_labels:
        s.append(text(X(v), ly + 28, t, 15))
    xs = sorted(X(v) for v, _ in marks)
    assert all(b - a >= 30 for a, b in zip(xs, xs[1:])), marks
    for v, lab in marks:
        x = X(v)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (x, ly - 30, x, ly - 12, GREEN))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (x - 6, ly - 14, x + 6, ly - 14, x, ly - 3, GREEN))
        if lab:
            s.append(text(x, ly - 34, lab, 16, col=GREEN))
    H = ly + 36
    if words:
        s.append(text(4, ly + 50, "impossible", 14, anchor="start", weight=400))
        s.append(text(X(F(1, 2)), ly + 50, "equally likely", 14, weight=400))
        s.append(text(W - 4, ly + 50, "certain", 14, anchor="end", weight=400))
        s.append(text(X(F(1, 4)), ly + 50, "unlikely", 14, weight=400))
        s.append(text(X(F(3, 4)), ly + 50, "likely", 14, weight=400))
        H = ly + 58
    return svg_wrap(W, H, "".join(s), label)


TENTHS = [(F(0), "0"), (F(1, 2), "0.5"), (F(1), "1")]
ENDS = [(F(0), "0"), (F(1), "1")]


def spinners_row_svg(specs, names, R=50, label="two spinners"):
    """A few spinners in one row with names under them (word labels inside the sections)."""
    gap = 30
    cell = 2 * R + gap
    W = len(specs) * cell
    s = []
    for i, sp in enumerate(specs):
        cx = gap / 2 + R + i * cell
        s.append(spinner_body(cx, R + 4, R, secs_of(sp), fs=15, initials=False))
        s.append(text(cx, 2 * R + 28, names[i], 16))
    return svg_wrap(int(W), 2 * R + 36, "".join(s), label)


def tree_svg(first, second, label="tree diagram", h1="Coin", h2="Spinner"):
    """Tree diagram: first event (e.g. coin: H, T), then every outcome of the second event on each branch."""
    k = len(second)
    gap = 24
    top = 34
    rows = len(first) * k
    H = top + rows * gap + 4
    xr, xa, xb, xo = 14, 112, 214, 300
    s = [text(xa, 18, h1, 15), text(xb + 26, 18, h2, 15), text(xo + 34, 18, "Outcome", 15)]
    ry = top + rows * gap / 2
    s.append("<circle cx='%d' cy='%.1f' r='4' fill='%s'/>" % (xr, ry, LINE))
    w2 = max(tw(c, 15) for c in second)
    assert xb + 6 + w2 < xo - 6, w2
    for i, a in enumerate(first):
        ay = top + (i * k + k / 2) * gap
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xr, ry, xa - 14, ay, THIN))
        s.append(text(xa, ay + 6, a, 17, col=GREEN))
        for j, b in enumerate(second):
            by = top + (i * k + j + 0.5) * gap
            s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xa + 12, ay, xb - 2, by, THIN))
            s.append(text(xb + 4, by + 5, b, 15, anchor="start"))
            s.append(text(xo, by + 5, a + ", " + b, 15, anchor="start", weight=400))
    W = int(max(xo + max(tw(a + ", " + b, 15, False) for a in first for b in second) + 10,
                xo + 34 + tw("Outcome", 15) / 2 + 6))
    return svg_wrap(W, int(H), "".join(s), label)


def outcome_table_svg(rows, cols, top_title, label="outcome table"):
    """Outcome table: rows = first event (words), columns = second event; each cell shows the pair."""
    fs, rh = 15, 28
    c1 = int(max(tw(r, fs) for r in rows) + 18)
    cw = int(max(max(tw(r[0] + c, fs) for r in rows for c in cols) + 14, 40))
    W = c1 + cw * len(cols) + 8
    s = [text(4 + c1 + cw * len(cols) / 2, 17, top_title, 15)]
    y0 = 24
    for r in range(len(rows) + 1):
        for k in range(len(cols) + 1):
            x = 4 + (0 if k == 0 else c1 + (k - 1) * cw)
            w = c1 if k == 0 else cw
            y = y0 + r * rh
            hd = r == 0 or k == 0
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, w, rh, HEAD if hd else "#ffffff", GREEN))
            if r == 0 and k > 0:
                s.append(text(x + w / 2, y + 19, cols[k - 1], fs))
            elif k == 0 and r > 0:
                s.append(text(x + 8, y + 19, rows[r - 1], fs, anchor="start"))
            elif r > 0:
                s.append(text(x + w / 2, y + 19, rows[r - 1][0].upper() + cols[k - 1], fs, weight=400))
    H = y0 + (len(rows) + 1) * rh + 4
    return svg_wrap(int(W), int(H), "".join(s), label)



def outcomes(a, b):
    return [(x, y) for x in a for y in b]



def table_svg(title, head, rows, label="results table"):
    """A small table drawn as SVG (header row + data rows)."""
    fs, rh = 15, 28
    ncol = len(head)
    cols = [int(max(tw(str(r[k]), fs) for r in [head] + rows) + 22) for k in range(ncol)]
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16) + 16))
    x0 = (W - tot) / 2
    s = [text(W / 2, 19, title, 16)]
    top = 28
    for r, row in enumerate([head] + rows):
        y = top + r * rh
        x = x0
        for k, cw in enumerate(cols):
            hd = r == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, HEAD if hd else "#ffffff", GREEN))
            s.append(text(x + cw / 2, y + 19, str(row[k]), fs, weight=700 if hd else 400))
            x += cw
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def sums_svg(label="sum table for two number cubes"):
    """6 × 6 table of the sums of two number cubes."""
    c, fs = 32, 15
    x0, y0 = 30, 26
    W = x0 + 7 * c + 6
    s = [text(x0 + c + 3 * c, 17, "Second number cube", 15)]
    s.append("<text x='16' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle' "
             "transform='rotate(-90 16 %.1f)'>First number cube</text>" % (y0 + c + 3 * c, LINE, y0 + c + 3 * c))
    for r in range(7):
        for k in range(7):
            x, y = x0 + k * c, y0 + r * c
            hd = r == 0 or k == 0
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, c, c, HEAD if hd else "#ffffff", GREEN))
            if r == 0 and k == 0:
                t = "+"
            elif r == 0:
                t = str(k)
            elif k == 0:
                t = str(r)
            else:
                t = str(r + k)
            s.append(text(x + c / 2, y + 21, t, fs, weight=700 if hd else 400))
    H = y0 + 7 * c + 4
    return svg_wrap(int(W), int(H), "".join(s), label)


CUBE = [str(k) for k in range(1, 7)]
EQ3 = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 3), "yellow")]
A2 = [("red", F(1, 2), "red"), ("blue", F(1, 2), "blue")]
B4 = [(str(k), F(1, 4), NUMFILL[k - 1]) for k in range(1, 5)]
RED34 = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]


def TABLE12():
    return fig(outcome_table_svg(["heads", "tails"], CUBE, "Number cube", label="outcome table coin and number cube"))


def TREE3():
    return fig(tree_svg(["H", "T"], ["red", "blue", "yellow"], label="tree diagram coin then spinner red blue yellow"))


def TREE4():
    return fig(tree_svg(["H", "T"], ["1", "2", "3", "4"], label="tree diagram coin then spinner 1 to 4"))


def TWO():
    return fig(spinners_row_svg([A2, B4], ["Spinner A", "Spinner B"], label="two spinners A and B"))


def SUMS():
    return fig(sums_svg())


O12 = outcomes("HT", range(1, 7))
O6 = outcomes("HT", ["red", "blue", "yellow"])
O8 = outcomes(["red", "blue"], range(1, 5))
O4 = outcomes("HT", "HT")
O36 = outcomes(range(1, 7), range(1, 7))
O9 = outcomes(["red", "blue", "yellow"], ["red", "blue", "yellow"])


def P(space, cond):
    return F(sum(1 for o in space if cond(*o)), len(space))


def cnt(space, cond):
    return sum(1 for o in space if cond(*o))


# ============================================================ set 1: sample spaces
def set_sample_spaces():
    its = []
    its.append(mcq("You toss a coin and spin a spinner with 2 equal sections, red and blue. "
                   "Which list shows all the outcomes? (H = heads, T = tails, R = red, B = blue)",
                   "HR, HB, TR, TB", ["H, T, R, B", "HR, TB", "HR, HB, TR, TB, HT"],
                   "Pair each coin face with each colour: 2 × 2 = 4 outcomes, <b>HR, HB, TR, TB</b>. "
                   "H, T, R, B lists single results, not pairs. HT is not possible: there is only one coin."))
    assert len(outcomes("HT", "RB")) == 4
    its.append(mcq("You toss two coins. Which list shows the whole sample space?", "HH, HT, TH, TT",
                   ["HH, HT, TT", "HH, TT", "H, T"],
                   "The first coin can be H or T, and so can the second: 2 × 2 = 4 outcomes, <b>HH, HT, TH, TT</b>. "
                   "HT and TH are different: heads on the first coin is not the same as heads on the second."))
    assert len(O4) == 4
    its.append(mcq(TREE3() + "How many outcomes does the tree diagram show?", "6", ["5", "3", "2"],
                   "Each of the 2 coin branches splits into 3 colours: 2 × 3 = <b>6</b> outcomes. "
                   "5 comes from adding 2 + 3.", ans=len(O6)))
    its.append(mcq(TREE3() + "Which outcome is NOT in the sample space?", "H, green",
                   ["H, red", "T, blue", "T, yellow"],
                   "The spinner only has red, blue and yellow, so <b>H, green</b> can’t happen. "
                   "The other three are all at the end of a branch."))
    assert ("H", "green") not in O6
    its.append(mcq(TREE4() + "How many branches come out of H?", "4", ["2", "8", "1"],
                   "After heads, the spinner can land on 1, 2, 3 or 4, so <b>4</b> branches come out of H. "
                   "8 is the number of outcomes in the whole tree.", ans=4))
    its.append(mcq(TABLE12() + "How many outcomes in the table show tails?", "6", ["12", "1", "3"],
                   "The tails row has T1, T2, T3, T4, T5 and T6: <b>6</b> outcomes. 12 is the whole table.",
                   ans=cnt(O12, lambda c, k: c == "T")))
    n = cnt(O12, lambda c, k: c == "H" and k % 2 == 1)
    assert n == 3
    its.append(mcq(TABLE12() + "How many outcomes show heads and an odd number?", "3", ["6", "1", "12"],
                   "Heads and odd: H1, H3 and H5, so <b>3</b> outcomes. 6 counts the odd numbers with tails too.", ans=n))
    n = cnt(O12, lambda c, k: k == 6)
    assert n == 2
    its.append(mcq(TABLE12() + "How many outcomes show a 6?", "2", ["1", "6", "12"],
                   "A 6 can come with heads or with tails: H6 and T6, so <b>2</b> outcomes. "
                   "1 forgets that the coin can land either way.", ans=n))
    its.append(mcq("You toss a coin and roll a number cube with the numbers 1 to 6. How many outcomes are there?",
                   "12", ["8", "6", "2"],
                   "Each coin face goes with each of the 6 numbers: 2 × 6 = <b>12</b>. 8 comes from adding 2 + 6.",
                   ans=len(O12)))
    its.append(mcq(TWO() + "You spin spinner A and spinner B. How many outcomes are there?", "8", ["6", "4", "16"],
                   "Each colour goes with each of the 4 numbers: 2 × 4 = <b>8</b>. 6 comes from adding 2 + 4.",
                   ans=len(O8)))
    its.append(mcq(TWO() + "Which list shows every outcome with blue? (R = red, B = blue)", "B1, B2, B3, B4",
                   ["B1, B2", "B4", "R1, B1"],
                   "Blue on spinner A can go with any of the 4 numbers on spinner B: <b>B1, B2, B3, B4</b>."))
    its.append(mcq("You toss a coin and spin a spinner with 5 equal sections numbered 1 to 5. "
                   "How many outcomes are there?", "10", ["7", "5", "25"],
                   "2 coin faces × 5 numbers = <b>10</b> outcomes. 7 comes from 2 + 5. 25 is 5 × 5, "
                   "as if there were two spinners.", ans=2 * 5))
    its.append(mcq("You spin a spinner with 3 equal sections (red, blue and yellow) two times. "
                   "How many outcomes are there?", "9", ["6", "3", "8"],
                   "Each of the 3 colours on the first spin goes with each of the 3 colours on the second: "
                   "3 × 3 = <b>9</b>. 6 comes from adding 3 + 3.", ans=len(O9)))
    its.append(mcq("A Burnaby school lunch program has 3 kinds of wraps and 4 kinds of drinks. "
                   "How many different wrap-and-drink lunches are possible?", "12", ["7", "4", "3"],
                   "Each wrap goes with each of the 4 drinks: 3 × 4 = <b>12</b>. 7 comes from adding 3 + 4.",
                   ans=3 * 4))
    its.append(mcq("You roll two number cubes, each with the numbers 1 to 6. How many outcomes are there?", "36",
                   ["12", "11", "6"],
                   "Each of the 6 numbers on the first cube goes with each of the 6 on the second: 6 × 6 = <b>36</b>. "
                   "12 comes from adding 6 + 6. 11 is the number of different sums (2 to 12), not outcomes.",
                   ans=len(O36)))
    n = cnt(O36, lambda a, b: a + b == 7)
    assert n == 6
    its.append(mcq(SUMS() + "The table shows the sum for every outcome of rolling two number cubes. "
                   "How many outcomes give a sum of 7?", "6", ["1", "3", "7"],
                   "The 7s run along a diagonal: 1 + 6, 2 + 5, 3 + 4, 4 + 3, 5 + 2, 6 + 1. That is <b>6</b> outcomes. "
                   "3 forgets that 1 + 6 and 6 + 1 are different outcomes.", ans=n))
    n = cnt(O36, lambda a, b: a + b == 10)
    assert n == 3
    its.append(mcq(SUMS() + "How many outcomes give a sum of 10?", "3", ["2", "1", "10"],
                   "4 + 6, 5 + 5 and 6 + 4: <b>3</b> outcomes. 2 forgets that 4 + 6 and 6 + 4 are different.", ans=n))
    sums = {t: cnt(O36, lambda a, b, t=t: a + b == t) for t in range(2, 13)}
    assert max(sums, key=sums.get) == 7 and list(sums.values()).count(6) == 1
    its.append(mcq(SUMS() + "Which sum comes up most often in the table?", "7", ["12", "6", "2"],
                   "The sum 7 is in 6 cells, more than any other sum, so <b>7</b> is the most likely sum. "
                   "12 is the largest sum, but it is in only one cell.", ans=7))
    its.append(mcq("You toss a nickel and a dime. Are “nickel heads, dime tails” and “nickel tails, dime heads” "
                   "the same outcome?", "No: they are 2 different outcomes",
                   ["Yes: both are one head and one tail", "Yes: the order of the coins does not matter",
                    "No: only one of them can ever happen"],
                   "The coins are different, so HT and TH are <b>2 different outcomes</b>. That is why two coins "
                   "have 4 outcomes (HH, HT, TH, TT), not 3."))
    its.append(mcq("Ava says, “A coin has 2 outcomes and a number cube has 6, so together there are 2 + 6 = 8 "
                   "outcomes.” What is wrong?", "Each coin face pairs with all 6 numbers: 2 × 6 = 12",
                   ["Nothing, 2 + 6 = 8 is right", "There are only 6 outcomes; the coin does not count",
                    "There are 2 × 6 × 2 = 24 outcomes"],
                   "Heads can go with 1, 2, 3, 4, 5 or 6, and so can tails. That makes 6 + 6 = 2 × 6 = <b>12</b> "
                   "outcomes. Multiply, don’t add."))
    assert len(its) == 20
    return {"title": "Sample spaces: tables and tree diagrams", "items": its}


# ============================================================ set 2: theoretical probability
def set_theory():
    its = []
    p = P(O12, lambda c, k: c == "H" and k == 6)
    assert p == F(1, 12) and F(1, 2) + F(1, 6) == F(4, 6)
    its.append(mcq(TABLE12() + "What is the probability of heads and a 6?", fr(1, 12), [fr(1, 8), fr(4, 6), fr(1, 6)],
                   "H6 is 1 of the 12 equally likely outcomes: <b>" + fr(1, 12) + "</b>. " + fr(4, 6) + " comes from adding "
                   + fr(1, 2) + " + " + fr(1, 6) + ". " + fr(1, 8) + " adds 2 + 6 outcomes.", ans=p))
    p = P(O12, lambda c, k: c == "T" and k % 2 == 0)
    its.append(mcq(TABLE12() + "What is the probability of tails and an even number?", fr(3, 12),
                   [fr(3, 8), fr(3, 6), fr(1, 12)],
                   "Tails and even: T2, T4 and T6, so 3 of 12 outcomes: <b>" + fr(3, 12) + "</b> (= " + fr(1, 4) + "). "
                   + fr(3, 6) + " only looks at the number cube.", ans=p))
    p = P(O4, lambda a, b: a == b == "H")
    its.append(mcq("You toss two coins. What is the probability of two heads?", fr(1, 4), [fr(1, 3), fr(1, 2), "1"],
                   "HH is 1 of the 4 outcomes (HH, HT, TH, TT): <b>" + fr(1, 4) + "</b>. Adding " + fr(1, 2) + " + "
                   + fr(1, 2) + " gives 1, which would mean two heads is certain. " + fr(1, 3) +
                   " forgets that HT and TH are different.", ans=p))
    p = P(O4, lambda a, b: a != b)
    its.append(mcq("You toss two coins. What is the probability of one head and one tail?", fr(2, 4),
                   [fr(1, 3), fr(1, 4), fr(3, 4)],
                   "HT and TH: 2 of the 4 outcomes, so <b>" + fr(2, 4) + "</b> (= " + fr(1, 2) + "). " + fr(1, 3) +
                   " treats HT and TH as one outcome. " + fr(3, 4) + " also counts HH.", ans=p))
    p = P(O8, lambda c, k: c == "blue" and k == 4)
    its.append(mcq(TWO() + "You spin both spinners. What is the probability of blue and 4?", fr(1, 8),
                   [fr(3, 4), fr(1, 6), fr(1, 4)],
                   "Blue and 4 is 1 of the 2 × 4 = 8 outcomes: <b>" + fr(1, 8) + "</b>. " + fr(3, 4) + " adds "
                   + fr(1, 2) + " + " + fr(1, 4) + ". " + fr(1, 6) + " adds 2 + 4 outcomes.", ans=p))
    p = P(O8, lambda c, k: c == "red" and k % 2 == 0)
    its.append(mcq(TWO() + "What is the probability of red and an even number?", fr(2, 8),
                   [fr(2, 6), fr(2, 4), "1"],
                   "Red and even: R2 and R4, so 2 of 8 outcomes: <b>" + fr(2, 8) + "</b> (= " + fr(1, 4) + "). "
                   + fr(2, 4) + " only looks at spinner B. Adding " + fr(1, 2) + " + " + fr(2, 4) + " gives 1, which would "
                   "mean certain.", ans=p))
    p = F(1, 2) * F(2, 6)
    assert p == P(O12, lambda c, k: c == "H" and k >= 5) == F(2, 12) and F(1, 2) + F(2, 6) == F(5, 6)
    its.append(mcq("For a coin and a number cube, P(heads) = " + fr(1, 2) + " and P(5 or 6) = " + fr(2, 6) +
                   ". What is P(heads and a 5 or 6)?", fr(2, 12), [fr(5, 6), fr(2, 8), fr(1, 12)],
                   "For independent events, multiply: " + fr(1, 2) + " × " + fr(2, 6) + " = <b>" + fr(2, 12) + "</b>. "
                   "Check with a table: H5 and H6 are 2 of 12 outcomes. " + fr(5, 6) + " comes from adding the probabilities.",
                   ans=p))
    p = P(O4, lambda a, b: a == b == "T")
    its.append(mcq("You toss two coins. What is the probability of two tails, as a decimal?", "0.25",
                   ["0.5", "0.4", "0.75"],
                   "TT is 1 of 4 outcomes: " + fr(1, 4) + " = <b>0.25</b>. " + fr(1, 4) + " is not 0.4. "
                   "0.5 is the chance of tails on one coin only.", ans=p))
    p = P(outcomes("HT", range(1, 6)), lambda c, k: c == "H" and k == 3)
    assert p == F(1, 10)
    its.append(mcq("You toss a coin and spin a spinner with 5 equal sections numbered 1 to 5. "
                   "What is the probability of heads and 3, as a percent?", "10%", ["70%", "20%", "50%"],
                   "There are 2 × 5 = 10 outcomes and H3 is one of them: " + fr(1, 10) + " = <b>10%</b>. "
                   "70% adds 50% + 20%. 20% is the chance of 3 on its own, and 50% is heads on its own.", ans=p))
    p = P(O36, lambda a, b: a == b == 6)
    its.append(mcq("You roll two number cubes. What is the probability of a 6 on both?", fr(1, 36),
                   [fr(1, 12), fr(2, 6), fr(1, 6)],
                   "6 and 6 is 1 of the 6 × 6 = 36 outcomes: <b>" + fr(1, 36) + "</b>. " + fr(2, 6) + " adds "
                   + fr(1, 6) + " + " + fr(1, 6) + ". " + fr(1, 12) + " adds 6 + 6 outcomes.", ans=p))
    p = P(O36, lambda a, b: a + b == 7)
    its.append(mcq(SUMS() + "What is the probability that the sum is 7?", fr(6, 36), [fr(1, 36), fr(7, 36), fr(1, 11)],
                   "6 of the 36 cells show 7: <b>" + fr(6, 36) + "</b> (= " + fr(1, 6) + "). " + fr(1, 11) +
                   " treats the 11 sums (2 to 12) as equally likely, but they are not.", ans=p))
    p = P(O36, lambda a, b: a + b == 10)
    its.append(mcq(SUMS() + "What is the probability that the sum is 10?", fr(3, 36), [fr(2, 36), fr(1, 11), fr(3, 12)],
                   "4 + 6, 5 + 5 and 6 + 4: 3 of 36 outcomes, so <b>" + fr(3, 36) + "</b> (= " + fr(1, 12) + "). "
                   + fr(2, 36) + " forgets that 4 + 6 and 6 + 4 are different.", ans=p))
    p = P(O36, lambda a, b: a % 2 == 0 and b % 2 == 0)
    assert p == F(9, 36) and cnt(O36, lambda a, b: a == b and a % 2 == 0) == 3
    its.append(mcq("You roll two number cubes. What is the probability that both numbers are even?", fr(9, 36),
                   ["1", fr(3, 36), fr(3, 6)],
                   "Each cube has 3 even numbers, so there are 3 × 3 = 9 even-even outcomes out of 36: <b>" + fr(9, 36) +
                   "</b> (= " + fr(1, 4) + "). " + fr(3, 36) + " counts only 2-2, 4-4 and 6-6. Adding "
                   + fr(1, 2) + " + " + fr(1, 2) + " = 1 would mean certain.", ans=p))
    p = P(O9, lambda a, b: a == b == "red")
    its.append(mcq("A spinner has 3 equal sections: red, blue and yellow. You spin it twice. "
                   "What is the probability of red both times?", fr(1, 9), [fr(2, 3), fr(1, 6), fr(1, 3)],
                   "Red, red is 1 of the 3 × 3 = 9 outcomes: <b>" + fr(1, 9) + "</b>. " + fr(2, 3) + " adds "
                   + fr(1, 3) + " + " + fr(1, 3) + ". " + fr(1, 6) + " adds 3 + 3 outcomes.", ans=p))
    p = P(O9, lambda a, b: a == b)
    its.append(mcq("You spin the same red, blue and yellow spinner twice. What is the probability that both spins "
                   "land on the same colour?", fr(3, 9), [fr(1, 9), fr(3, 6), fr(6, 9)],
                   "Red-red, blue-blue and yellow-yellow: 3 of 9 outcomes, so <b>" + fr(3, 9) + "</b> (= " + fr(1, 3) + "). "
                   + fr(1, 9) + " counts only one colour. " + fr(6, 9) + " is the chance of different colours.", ans=p))
    p = 1 - P(O12, lambda c, k: c == "H" and k == 6)
    its.append(mcq("You toss a coin and roll a number cube. What is the probability of NOT getting heads and a 6?",
                   fr(11, 12), [fr(1, 12), fr(1, 2), fr(5, 6)],
                   "Heads and 6 is 1 of 12 outcomes, so the other <b>" + fr(11, 12) + "</b> are not. "
                   + fr(5, 6) + " is the chance of not rolling a 6 on its own.", ans=p))
    p = P(O4, lambda a, b: "H" in (a, b))
    its.append(mcq("You toss two coins. What is the probability of at least one head, as a percent?", "75%",
                   ["25%", "50%", "about 67%"],
                   "HH, HT and TH have at least one head: 3 of 4 outcomes, " + fr(3, 4) + " = <b>75%</b>. "
                   "About 67% (" + fr(2, 3) + ") uses only 3 outcomes, joining HT and TH together.", ans=p))
    p = P(outcomes("HT", ["red", "blue", "yellow", "green"]), lambda c, s: c == "T" and s == "blue")
    assert p == F(1, 8)
    its.append(mcq("You toss a coin and spin a spinner with 4 equal sections: red, blue, yellow and green. "
                   "What is the probability of tails and blue, as a decimal?", "0.125", ["0.75", "0.25", "0.18"],
                   "There are 2 × 4 = 8 outcomes, so the probability is " + fr(1, 8) + " = 1 ÷ 8 = <b>0.125</b>. "
                   "0.75 adds 0.5 + 0.25. 0.18 just writes the digits 1 and 8.", ans=p))
    assert P(O4, lambda a, b: a == b == "H") > P(O12, lambda c, k: c == "H" and k == 1)
    its.append(mcq("Which is more likely: two heads when you toss two coins, or heads and a 1 when you toss a coin "
                   "and roll a number cube?", "Two heads with two coins",
                   ["Heads and a 1", "They are equally likely", "You can’t tell"],
                   "Two heads: 1 of 4 outcomes, " + fr(1, 4) + ". Heads and a 1: 1 of 12 outcomes, " + fr(1, 12) + ". "
                   + fr(1, 4) + " &gt; " + fr(1, 12) + ", so <b>two heads with two coins</b> is more likely."))
    p = F(1, 2) * part(RED34, "red")
    sp4 = outcomes("HT", ["red", "red", "red", "blue"])
    assert p == F(3, 8) == P(sp4, lambda c, s: c == "H" and s == "red")
    its.append(mcq(fig(spinner_svg(RED34, R=56, label="spinner three quarters red one quarter blue")) +
                   "You toss a coin and spin this spinner. What is the probability of heads and red?", fr(3, 8),
                   [fr(1, 4), fr(5, 4), fr(3, 6)],
                   "Split the spinner into 4 equal parts: 3 are red. That gives 2 × 4 = 8 equally likely outcomes, "
                   "and heads with red is 3 of them: <b>" + fr(3, 8) + "</b>. Or multiply: " + fr(1, 2) + " × " + fr(3, 4) +
                   " = " + fr(3, 8) + ". " + fr(1, 4) + " treats red and blue as equally likely. "
                   + fr(5, 4) + " adds and is more than 1.", ans=p))
    assert len(its) == 20
    return {"title": "Theoretical probability of two events", "items": its}


# ============================================================ set 3: experimental probability
T50V = [12, 13, 14, 11]
T40C = ["red, 1", "red, 2", "blue, 1", "blue, 2"]
T40V = [11, 9, 6, 14]
T60C = ["H, red", "H, blue", "H, yellow", "T, red", "T, blue", "T, yellow"]
T60V = [11, 9, 12, 8, 10, 10]


def T50():
    return fig(freq_svg("Two coins tossed 50 times", "Outcome", ["HH", "HT", "TH", "TT"], T50V, tally=False,
                        label="frequency table two coins 50 tosses"))


def T40():
    return fig(freq_svg("Spinners A and B, 40 spins", "Outcome", T40C, T40V, tally=False,
                        label="frequency table two spinners 40 spins"))


def T60():
    return fig(freq_svg("Coin and spinner, 60 trials", "Outcome", T60C, T60V, tally=False,
                        label="frequency table coin and spinner 60 trials"))


def set_experimental():
    assert sum(T50V) == 50 and sum(T40V) == 40 and sum(T60V) == 60
    its = []
    its.append(mcq(T50() + "What is the experimental probability of HH, as a decimal?", "0.24",
                   ["0.12", "0.25", "0.76"],
                   "HH came up 12 times in 50 tosses: " + fr(12, 50) + " = " + fr(24, 100) + " = <b>0.24</b>. "
                   "0.25 is the theoretical probability. 0.12 uses the count as the decimal.", ans=F(12, 50)))
    its.append(mcq(T50() + "What is the experimental probability of one head and one tail, as a decimal?", "0.54",
                   ["0.14", "0.27", "0.5"],
                   "One head and one tail is HT or TH: 13 + 14 = 27 times. " + fr(27, 50) + " = " + fr(54, 100) +
                   " = <b>0.54</b>. 0.5 is the theoretical probability.", ans=F(27, 50)))
    its.append(mcq(T50() + "What is the experimental probability of TT, as a percent?", "22%", ["11%", "25%", "78%"],
                   "TT came up 11 times in 50: " + fr(11, 50) + " = " + fr(22, 100) + " = <b>22%</b>. "
                   "11% uses the count as the percent. 78% is NOT TT.", ans=F(11, 50)))
    assert F(T50V[2], 50) == F(28, 100)
    its.append(mcq(T50() + "Which outcome has an experimental probability of 0.28?", "TH", ["HH", "HT", "TT"],
                   "0.28 = " + fr(28, 100) + " = " + fr(14, 50) + ". TH came up 14 times, so the answer is <b>TH</b>."))
    its.append(mcq("Noah tosses a coin and rolls a number cube 60 times. He gets heads and a 6 four times. "
                   "What is the experimental probability of heads and a 6?", fr(4, 60), [fr(4, 56), fr(1, 12), fr(4, 6)],
                   "Experimental probability = times it happened ÷ number of trials = <b>" + fr(4, 60) + "</b>. "
                   + fr(1, 12) + " is the theoretical probability. " + fr(4, 56) + " compares with the other trials, "
                   "not with all 60.", ans=F(4, 60)))
    its.append(mcq("Chloe rolls two number cubes 90 times. The sum is 7 on 18 rolls. What is the experimental "
                   "probability of a sum of 7?", fr(1, 5), [fr(18, 72), fr(1, 18), fr(1, 6)],
                   fr(18, 90) + " = <b>" + fr(1, 5) + "</b>. " + fr(1, 6) + " is the theoretical probability, not what "
                   "happened. " + fr(18, 72) + " divides by the rolls that were not 7.", ans=F(18, 90)))
    its.append(mcq(T40() + "What is the experimental probability of blue, 2 as a percent?", "35%",
                   ["14%", "25%", "65%"],
                   "Blue, 2 came up 14 times in 40 spins: " + fr(14, 40) + " = " + fr(35, 100) + " = <b>35%</b>. "
                   "14% uses the count as the percent. 25% is the theory.", ans=F(14, 40)))
    p = F(T40V[2] + T40V[3], 40)
    its.append(mcq(T40() + "What is the experimental probability of blue with either number, as a decimal?", "0.5",
                   ["0.2", "0.35", "0.15"],
                   "Blue, 1 and blue, 2: 6 + 14 = 20 times. " + fr(20, 40) + " = <b>0.5</b>. "
                   "0.35 uses only blue, 2, and 0.15 only blue, 1.", ans=p))
    p = F(T40V[0] + T40V[2], 40)
    assert p == F("0.425")
    its.append(mcq(T40() + "What is the experimental probability of a 1 with either colour, as a decimal?", "0.425",
                   ["0.17", "0.275", "0.5"],
                   "Red, 1 and blue, 1: 11 + 6 = 17 times. " + fr(17, 40) + " = 17 ÷ 40 = <b>0.425</b>. "
                   "0.275 uses only red, 1. 0.5 is the theory.", ans=p))
    its.append(mcq(T60() + "What is the experimental probability of H, yellow as a percent?", "20%",
                   ["12%", "80%", "about 17%"],
                   "H, yellow came up 12 times in 60: " + fr(12, 60) + " = " + fr(1, 5) + " = <b>20%</b>. "
                   "About 17% is the theory (" + fr(1, 6) + "). 12% uses the count as the percent.", ans=F(12, 60)))
    p = F(T60V[0] + T60V[3], 60)
    its.append(mcq(T60() + "What is the experimental probability of red, with either heads or tails?", fr(19, 60),
                   [fr(11, 60), fr(8, 60), fr(19, 41)],
                   "H, red and T, red: 11 + 8 = 19 times in 60 trials: <b>" + fr(19, 60) + "</b>. "
                   + fr(19, 41) + " compares red with the other results, not with all 60.", ans=p))
    assert [c for c, v in zip(T60C, T60V) if F(v, 60) == F(15, 100)] == ["H, blue"]
    its.append(mcq(T60() + "Which outcome has an experimental probability of 0.15?", "H, blue",
                   ["H, red", "T, red", "H, yellow"],
                   "0.15 × 60 = 9. <b>H, blue</b> came up 9 times: " + fr(9, 60) + " = 0.15."))
    assert F("0.3") * 50 == 15
    its.append(mcq("After 50 trials, the experimental probability of heads and an even number is 0.3. "
                   "How many times did heads and an even number happen?", "15", ["30", "3", "35"],
                   "0.3 × 50 = <b>15</b>. Check: " + fr(15, 50) + " = " + fr(3, 10) + " = 0.3. 35 is the number of "
                   "trials when it did NOT happen.", ans=15))
    its.append(mcq("Simran tosses a coin and rolls a number cube 60 times. She gets heads and an even number 18 times. "
                   "What is the experimental probability, as a percent?", "30%", ["18%", "42%", "25%"],
                   fr(18, 60) + " = " + fr(3, 10) + " = <b>30%</b>. 25% is the theory. 18% uses the count as the percent.",
                   ans=F(18, 60)))
    p = F(4 + 6 + 5, 60)
    its.append(mcq("Three groups each toss two coins 20 times. They get HH 4, 6 and 5 times. "
                   "Use all the results to find the experimental probability of HH.", fr(15, 60),
                   [fr(15, 20), fr(4, 20), fr(6, 20)],
                   "Add the results: 4 + 6 + 5 = 15 in 3 × 20 = 60 trials: <b>" + fr(15, 60) + "</b> (= " + fr(1, 4) + "). "
                   + fr(15, 20) + " forgets that there were 60 trials in all.", ans=p))
    its.append(mcq("Ji-woo rolls two number cubes 50 times and gets doubles 9 times. What is the experimental "
                   "probability of NOT getting doubles?", fr(41, 50), [fr(9, 50), fr(9, 41), fr(5, 6)],
                   "50 − 9 = 41 rolls were not doubles: <b>" + fr(41, 50) + "</b>. " + fr(5, 6) +
                   " is the theoretical probability. " + fr(9, 50) + " is doubles.", ans=F(41, 50)))
    its.append(mcq("A computer simulates tossing a coin and rolling a number cube 1000 times. Heads and 6 comes up 86 "
                   "times. What is the experimental probability, as a decimal?", "0.086", ["0.86", "0.0086", "0.083"],
                   "86 ÷ 1000 = <b>0.086</b>. Dividing by 1000 moves the decimal point 3 places to the left. "
                   "0.083 is about the theoretical probability, " + fr(1, 12) + ".", ans=F(86, 1000)))
    its.append(mcq("Mateo plays a game: he wins on heads and red, using a coin and a spinner with 4 equal colours. "
                   "He wins 9 of 40 games. What is his experimental probability of winning, as a percent?", "22.5%",
                   ["9%", "31%", "12.5%"],
                   fr(9, 40) + " = 9 ÷ 40 = 0.225 = <b>22.5%</b>. 12.5% (" + fr(1, 8) + ") is the theory. "
                   "31% comes from 40 − 9.", ans=F(9, 40)))
    assert F("0.25") * 80 == 20
    its.append(mcq("After 80 trials, the experimental probability of two tails is 0.25. How many times did two tails "
                   "come up?", "20", ["25", "60", "320"],
                   "0.25 × 80 = <b>20</b>. 320 comes from dividing 80 by 0.25 instead of multiplying. 60 is NOT two tails.",
                   ans=20))
    its.append(mcq("Hana tosses two coins 20 times and gets HH 7 times. She says the experimental probability of HH is "
                   + fr(7, 13) + ". What is wrong?", "She should divide by all 20 trials: " + fr(7, 20),
                   ["Nothing, " + fr(7, 13) + " is right", "She should use the theory: " + fr(1, 4),
                    "She should divide by the 4 outcomes: " + fr(7, 4)],
                   "7 HH out of 20 trials is <b>" + fr(7, 20) + "</b>. " + fr(7, 13) + " compares HH with the other "
                   "13 trials, not with all 20."))
    assert len(its) == 20
    return {"title": "Experimental probability from results", "items": its}


# ============================================================ set 4: experimental vs theoretical
def set_compare():
    its = []
    assert F(1, 12) * 120 == 10 and F(120, 8) == 15
    its.append(mcq("You toss a coin and roll a number cube 120 times. About how many times would you expect heads "
                   "and a 6?", "about 10", ["about 15", "about 20", "about 60"],
                   "Heads and 6 is " + fr(1, 12) + ". " + fr(1, 12) + " of 120 = 120 ÷ 12 = <b>about 10</b>. "
                   "About 15 comes from 120 ÷ 8 (adding 2 + 6 outcomes). About 20 uses " + fr(1, 6) + " only."))
    assert F(1, 4) * 200 == 50
    its.append(mcq("You toss two coins 200 times. About how many times would you expect two heads?", "about 50",
                   ["about 100", "about 67", "about 150"],
                   "P(HH) = " + fr(1, 4) + ". " + fr(1, 4) + " of 200 = <b>about 50</b>. About 67 uses " + fr(1, 3) +
                   ", which forgets that HT and TH are different."))
    assert F(6, 36) * 360 == 60
    its.append(mcq("You roll two number cubes 360 times. About how many times would you expect a sum of 7?",
                   "about 60", ["about 33", "about 10", "about 70"],
                   "P(sum of 7) = " + fr(6, 36) + " = " + fr(1, 6) + ". 360 ÷ 6 = <b>about 60</b>. About 33 treats the 11 sums "
                   "as equally likely. About 10 uses only one of the 6 ways to make 7."))
    its.append(mcq(TWO() + "You spin both spinners 80 times. About how many times would you expect each outcome?",
                   "about 10", ["about 20", "about 13", "about 40"],
                   "There are 8 equally likely outcomes, so each has probability " + fr(1, 8) + ". 80 ÷ 8 = <b>about 10</b>. "
                   "About 13 comes from 80 ÷ 6 (adding 2 + 4 outcomes)."))
    assert F(8, 20) == F(4, 10) and F(96, 400) == F(24, 100)
    its.append(mcq("The theoretical probability of two heads is 0.25. Group A tosses two coins 20 times and gets HH 8 "
                   "times. Group B tosses them 400 times and gets HH 96 times. Whose experimental probability is "
                   "closer to 0.25?", "Group B’s", ["Group A’s", "They are equally close", "Neither is close"],
                   "Group A: " + fr(8, 20) + " = 0.4. Group B: " + fr(96, 400) + " = 0.24. 0.24 is much closer to 0.25, "
                   "so <b>Group B’s</b> is closer."))
    its.append(mcq("Why are the results of 400 trials usually closer to the theory than the results of 20 trials?",
                   "More trials usually get closer to the theory",
                   ["Big groups toss more carefully", "The coins wear out after 20 tosses",
                    "Big experiments always match the theory exactly"],
                   "With only a few trials, luck changes the results a lot. <b>More trials usually get closer</b> "
                   "to the theoretical probability, but not exactly."))
    its.append(mcq("Ryan tosses two coins 10 times and gets HH 4 times. He says the coins must be unfair because 0.4 "
                   "is not 0.25. Is he right?", "No, 10 trials are too few to tell",
                   ["Yes, 0.4 is far from 0.25", "Yes, HH should come up exactly 2.5 times",
                    "No, HH can never come up 4 times"],
                   "With only 10 trials, results can be far from the theory just by chance. "
                   "<b>10 trials are too few to tell</b>. He should do many more trials."))
    assert F(1, 4) * 1000 == 250
    its.append(mcq("Two coins are tossed 1000 times and HH comes up 381 times. What do the results suggest?",
                   "The coins are probably not fair",
                   ["The coins are fair", "1000 trials are too few to tell", "HH will now come up less often"],
                   "Theory: " + fr(1, 4) + " of 1000 = 250. 381 is far from 250 after a lot of trials, so "
                   "<b>the coins are probably not fair</b>."))
    assert F("0.3") - F("0.25") == F("0.05")
    its.append(mcq("The experimental probability of an outcome is 0.3 and the theoretical probability is 0.25. "
                   "What is the difference?", "0.05", ["0.55", "0.5", "0.25"],
                   "0.30 − 0.25 = <b>0.05</b>. 0.55 adds them instead of subtracting.", ans=F("0.05")))
    res = {"26 out of 100": F(26, 100), "4 out of 10": F(4, 10), "7 out of 20": F(7, 20), "1 out of 2": F(1, 2)}
    assert min(res, key=lambda k: abs(res[k] - F(1, 4))) == "26 out of 100"
    its.append(mcq("The theoretical probability of heads and an even number is " + fr(1, 4) + ". Which experimental "
                   "result is closest to the theory?", "26 out of 100", ["4 out of 10", "7 out of 20", "1 out of 2"],
                   "As decimals: 0.26, 0.4, 0.35 and 0.5. " + fr(1, 4) + " = 0.25, so <b>26 out of 100</b> is closest."))
    run = [["20", "0.35"], ["100", "0.29"], ["500", "0.26"], ["2000", "0.252"]]
    its.append(mcq(fig(table_svg("Two coins: experimental P(HH)", ["Trials", "P(HH)"], run,
                                 label="results table trials and experimental probability")) +
                   "As the number of trials grows, which number is the experimental probability getting close to?",
                   "0.25", ["0.35", "0.5", "0"],
                   "0.35, 0.29, 0.26, 0.252 … the results get closer and closer to <b>0.25</b>, the theoretical "
                   "probability " + fr(1, 4) + ".", ans=F(1, 4)))
    its.append(mcq("Two fair coins have landed TT four times in a row. What is the probability of HH on the next toss?",
                   fr(1, 4), ["1", fr(1, 2), fr(4, 5)],
                   "Coins have no memory. Every toss is a new trial, so HH is still <b>" + fr(1, 4) + "</b>. "
                   "Thinking HH is “due” is called the gambler’s fallacy.", ans=F(1, 4)))
    its.append(mcq("Mei tosses a coin and gets heads. Then she rolls a number cube. What is the probability that the "
                   "number cube shows a 6?", fr(1, 6), [fr(1, 12), fr(4, 6), fr(1, 2)],
                   "The coin does not change the number cube: the events are independent. A 6 is still <b>" + fr(1, 6) +
                   "</b>. " + fr(1, 12) + " is the chance of heads AND 6 before anything is tossed.", ans=F(1, 6)))
    assert F(9, 50) * 200 == 36
    its.append(mcq("In 50 trials with a coin and a spinner, Liam gets heads and red 9 times. Use his results to predict "
                   "how many times he will get heads and red in 200 trials.", "about 36", ["about 9", "about 159",
                                                                                        "about 18"],
                   "200 trials is 4 times as many as 50, so expect about 4 × 9 = <b>36</b>. About 159 adds 150 instead "
                   "of multiplying. About 18 only doubles."))
    assert F(3, 9) * 90 == 30
    its.append(mcq("You spin a red, blue and yellow spinner (3 equal sections) twice, and do this 90 times. About how "
                   "many times would you expect both spins to be the same colour?", "about 30",
                   ["about 10", "about 45", "about 60"],
                   "P(same colour) = " + fr(3, 9) + " = " + fr(1, 3) + ". " + fr(1, 3) + " of 90 = <b>about 30</b>. "
                   "About 10 counts only one colour. About 45 uses " + fr(3, 6) + "."))
    its.append(mcq("Which is the best way to make an experimental probability closer to the theoretical probability?",
                   "Do many more trials", ["Do the trials faster", "Stop when the results look right",
                                           "Use a new coin for each toss"],
                   "Results from a few trials vary a lot. <b>Doing many more trials</b> usually brings the experimental "
                   "probability closer to the theory."))
    its.append(mcq("Why might a class use a computer simulation instead of tossing real coins?",
                   "It can run thousands of trials quickly",
                   ["It always matches the theory exactly", "It makes the coins fair", "It needs fewer trials"],
                   "A simulation <b>can run thousands of trials quickly</b>. With so many trials, the experimental "
                   "probability usually gets close to the theory, but it is still not exact."))
    assert F(1, 4) * 120 == 30
    its.append(mcq("Owen tosses a coin and rolls a number cube 120 times. He gets heads and an odd number 33 times. "
                   "How does this compare with the theory?", "Close: theory says about 30",
                   ["Far off: theory says about 60", "Far off: theory says about 20", "Exactly right: theory says 33"],
                   "Heads and odd: H1, H3, H5, so " + fr(3, 12) + " = " + fr(1, 4) + ". " + fr(1, 4) + " of 120 = 30. "
                   "33 is <b>close to 30</b>. About 60 uses heads only."))
    assert F(3, 8) * 80 == 30
    its.append(mcq(fig(spinner_svg(RED34, R=56, label="spinner three quarters red one quarter blue")) +
                   "You toss a coin and spin this spinner 80 times. About how many times would you expect heads and red?",
                   "about 30", ["about 20", "about 40", "about 100"],
                   "P(heads and red) = " + fr(1, 2) + " × " + fr(3, 4) + " = " + fr(3, 8) + ". 80 ÷ 8 × 3 = <b>about 30</b>. "
                   "About 20 treats red and blue as equally likely. About 100 adds the probabilities (" + fr(5, 4) + ")."))
    assert P(O4, lambda a, b: a == b) == F(1, 2)
    its.append(mcq("In a game, you win if two coins match (HH or TT). Nadia plays 100 times and wins 47 times. "
                   "Do her results fit the theory?", "Yes, 47 is close to the 50 the theory predicts",
                   ["No, she should win exactly 50 times", "No, 47 means the game is unfair",
                    "Yes, because 47 is close to 100"],
                   "P(match) = " + fr(2, 4) + " = " + fr(1, 2) + ", so theory predicts about 50 wins. "
                   "<b>47 is close to 50</b>; small differences are normal."))
    assert len(its) == 20
    return {"title": "Comparing experimental and theoretical probability", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []
    LUNCH = outcomes(["turkey", "veggie"], ["apple", "banana", "orange"])
    p = P(LUNCH, lambda a, b: a == "veggie" and b == "apple")
    its.append(mcq("At a Surrey school, a hot lunch comes with a random sandwich (turkey or veggie) and a random fruit "
                   "(apple, banana or orange). What is the probability of a veggie sandwich and an apple?", fr(1, 6),
                   [fr(1, 5), fr(5, 6), fr(1, 3)],
                   "There are 2 × 3 = 6 outcomes and veggie-apple is one of them: <b>" + fr(1, 6) + "</b>. "
                   + fr(1, 5) + " adds 2 + 3 outcomes. " + fr(5, 6) + " adds " + fr(1, 2) + " + " + fr(1, 3) + ".", ans=p))
    p = P(LUNCH, lambda a, b: a == "turkey" and b != "banana")
    its.append(mcq("With the same lunch choices, what is the probability of a turkey sandwich and NOT a banana?",
                   fr(2, 6), [fr(4, 6), fr(2, 5), fr(1, 6)],
                   "Turkey-apple and turkey-orange: 2 of 6 outcomes, so <b>" + fr(2, 6) + "</b> (= " + fr(1, 3) + "). "
                   + fr(4, 6) + " counts every lunch without a banana, veggie too.", ans=p))
    TRIP = outcomes(["Grouse Mountain", "Stanley Park", "Science World", "the Vancouver Aquarium"], ["Monday", "Friday"])
    p = P(TRIP, lambda a, b: a == "Grouse Mountain" and b == "Friday")
    its.append(mcq("A Grade 7 class draws a field trip at random from 4 places (Grouse Mountain, Stanley Park, "
                   "Science World, the Vancouver Aquarium) and tosses a coin to pick Monday or Friday. "
                   "What is the probability of Grouse Mountain on a Friday?", fr(1, 8), [fr(1, 6), fr(3, 4), fr(1, 4)],
                   "4 places × 2 days = 8 outcomes, so <b>" + fr(1, 8) + "</b>. " + fr(3, 4) + " adds "
                   + fr(1, 4) + " + " + fr(1, 2) + ". " + fr(1, 4) + " forgets the day.", ans=p))
    p = P(O4, lambda a, b: a == b == "H")
    its.append(mcq("Kai guesses the answers to two true-or-false questions. What is the probability that he gets "
                   "both right?", fr(1, 4), [fr(1, 2), "1", fr(1, 3)],
                   "Right-right, right-wrong, wrong-right, wrong-wrong: 4 outcomes, so <b>" + fr(1, 4) + "</b>. "
                   "Adding " + fr(1, 2) + " + " + fr(1, 2) + " = 1 would mean he is sure to get both right.", ans=p))
    p = F(1, 4) * F(1, 2)
    assert p == F(125, 1000)
    its.append(mcq("Olivia guesses a multiple-choice question with 4 choices (A, B, C, D) and a true-or-false question. "
                   "What is the probability that she gets both right, as a percent?", "12.5%", ["75%", "25%", "50%"],
                   "4 × 2 = 8 outcomes, and only one has both right: " + fr(1, 8) + " = <b>12.5%</b>. "
                   "75% adds 25% + 50%. 25% and 50% look at one question only.", ans=p))
    p = P(O36, lambda a, b: a == b)
    its.append(mcq("In a board game, Lucas needs doubles on two number cubes to get out of jail. "
                   "What is the probability that he rolls doubles?", fr(6, 36), [fr(1, 36), fr(2, 6), fr(6, 12)],
                   "1-1, 2-2, 3-3, 4-4, 5-5, 6-6: 6 of the 36 outcomes, so <b>" + fr(6, 36) + "</b> (= " + fr(1, 6) + "). "
                   + fr(1, 36) + " counts only one double. " + fr(6, 12) + " adds 6 + 6 outcomes.", ans=p))
    p = P(O36, lambda a, b: a + b == 12)
    its.append(mcq("In the same game, Lucas needs a sum of 12 to win. What is the probability?", fr(1, 36),
                   [fr(1, 11), fr(12, 36), fr(2, 36)],
                   "Only 6 + 6 makes 12: <b>" + fr(1, 36) + "</b>. " + fr(1, 11) + " treats the 11 sums as equally likely. "
                   + fr(12, 36) + " uses the sum as the number of outcomes.", ans=p))
    DRILL = outcomes(["passing", "shooting", "cradling"], ["north", "south"])
    p = P(DRILL, lambda a, b: a == "passing" and b == "north")
    its.append(mcq("At lacrosse practice in Coquitlam, the coach spins a spinner with 3 equal sections to pick a drill "
                   "(passing, shooting or cradling) and tosses a coin to pick the north or south end. "
                   "What is the probability of a passing drill at the north end?", fr(1, 6),
                   [fr(1, 5), fr(5, 6), fr(1, 3)],
                   "3 drills × 2 ends = 6 outcomes, so <b>" + fr(1, 6) + "</b>. " + fr(5, 6) + " adds " + fr(1, 3) +
                   " + " + fr(1, 2) + ". " + fr(1, 3) + " forgets the end of the field.", ans=p))
    p = F(1, 2) * F(1, 4)
    its.append(mcq("Sofia makes a game for the school fun fair. A player tosses a coin and spins a spinner with 4 equal "
                   "colours, and wins on heads and red. What is the probability of winning, as a decimal?", "0.125",
                   ["0.75", "0.18", "0.25"],
                   "2 × 4 = 8 outcomes and one wins: " + fr(1, 8) + " = <b>0.125</b>. 0.75 adds 0.5 + 0.25. "
                   "0.18 just writes the digits 1 and 8.", ans=p))
    assert F(1, 8) * 160 == 20
    its.append(mcq("Sofia expects 160 players at the fun fair. Her game has a " + fr(1, 8) + " chance of winning. "
                   "About how many prizes should she bring?", "about 20", ["about 40", "about 80", "about 27"],
                   fr(1, 8) + " of 160 = 160 ÷ 8 = <b>about 20</b>. About 27 comes from 160 ÷ 6 (adding 2 + 4 outcomes). "
                   "About 80 uses " + fr(1, 2) + " for heads only."))
    its.append(mcq("At the fun fair, 24 of the 160 players won Sofia’s game. What is the experimental probability "
                   "of winning, as a percent?", "15%", ["24%", "12.5%", "85%"],
                   fr(24, 160) + " = " + fr(15, 100) + " = <b>15%</b>. 12.5% is the theoretical probability. 85% is "
                   "the players who did not win.", ans=F(24, 160)))
    its.append(mcq("Theory said about 20 of the 160 players would win, but 24 won. Does this mean Sofia’s game is "
                   "broken?", "No, results usually differ a little from the theory",
                   ["Yes, exactly 20 should have won", "Yes, the coin must be unfair", "No, 24 is exactly what the theory predicts"],
                   "Experimental results are rarely exactly the same as the theory. 24 is fairly close to 20, so "
                   "<b>the game is probably fine</b>."))
    its.append(mcq("Arjun and Hana each toss a coin. Arjun wins if the coins match; Hana wins if they don’t. "
                   "Is the game fair?", "Yes, each has a probability of " + fr(2, 4),
                   ["No, Arjun wins more often", "No, Hana wins more often", "Yes, because there are 2 players"],
                   "Match: HH, TT. Different: HT, TH. Each player has 2 of 4 outcomes, so <b>the game is fair</b>."))
    assert P(O36, lambda a, b: a + b == 7) > P(O36, lambda a, b: a + b in (2, 12))
    its.append(mcq("Ethan and Leah roll two number cubes. Ethan wins on a sum of 7. Leah wins on a sum of 2 or 12. "
                   "Who is more likely to win a roll?", "Ethan", ["Leah", "They are equally likely", "You can’t tell"],
                   "Sum of 7: 6 of 36 outcomes. Sum of 2 or 12: only 1-1 and 6-6, 2 of 36. "
                   + fr(6, 36) + " &gt; " + fr(2, 36) + ", so <b>Ethan</b> is more likely to win."))
    p = P(O36, lambda a, b: a % 2 == 1 and b % 2 == 1)
    assert p == F(9, 36)
    its.append(mcq("Emma wins a game if both number cubes show an odd number. What is the probability that she wins?",
                   fr(9, 36), ["1", fr(3, 36), fr(18, 36)],
                   "3 odd numbers × 3 odd numbers = 9 outcomes out of 36: <b>" + fr(9, 36) + "</b> (= " + fr(1, 4) + "). "
                   + fr(3, 36) + " counts only 1-1, 3-3 and 5-5. Adding " + fr(1, 2) + " + " + fr(1, 2) +
                   " = 1 would mean she always wins.", ans=p))
    p = F(1, 5) * F(1, 2)
    its.append(mcq("For a hike in the Okanagan, Zara picks a snack at random from 5 kinds (one is her favourite) and a "
                   "drink at random (milk or water). What is the probability of her favourite snack and water, as a decimal?", "0.1",
                   ["0.7", "0.2", "0.5"],
                   "5 × 2 = 10 outcomes, and one is right: " + fr(1, 10) + " = <b>0.1</b>. 0.7 adds 0.2 + 0.5. "
                   "0.2 is the snack on its own.", ans=p))
    assert F(2, 12) * 60 == 10 and F(2, 8) * 60 == 15
    its.append(mcq("Harjot tosses a coin and rolls a number cube. He scores a point on heads and a number greater than 4. "
                   "About how many points would he expect in 60 turns?", "about 10", ["about 15", "about 20", "about 30"],
                   "Heads and 5 or 6: H5, H6, so " + fr(2, 12) + " = " + fr(1, 6) + ". 60 ÷ 6 = <b>about 10</b>. "
                   "About 15 uses " + fr(2, 8) + " (adding 2 + 6 outcomes). About 30 uses heads only."))
    p = F(1, 4) * F(1, 5)
    assert p == F(5, 100)
    its.append(mcq("At the Terry Fox Run, each runner gets a random wristband (4 colours, equally likely) and a random "
                   "sticker (5 kinds, one is an orca). What is the probability that Nadia gets a green wristband and the "
                   "orca sticker, as a percent?", "5%", ["45%", "20%", "about 11%"],
                   "4 × 5 = 20 outcomes, so " + fr(1, 20) + " = <b>5%</b>. 45% adds 25% + 20%. About 11% is " + fr(1, 9) +
                   ", which adds 4 + 5 outcomes.", ans=p))
    its.append(mcq("Before the fun fair, Owen tests a two-coin game 80 times and gets HH 22 times. What is the "
                   "experimental probability of HH, as a decimal?", "0.275", ["0.22", "0.25", "0.725"],
                   fr(22, 80) + " = 22 ÷ 80 = <b>0.275</b>. 0.25 is the theory. 0.725 is NOT HH.", ans=F(22, 80)))
    n = 5
    assert F(1, 2) * F(1, n) == F(1, 10)
    its.append(mcq("A game uses a coin and a spinner with equal sections, one of them red. The probability of heads and "
                   "red is " + fr(1, 10) + ". How many sections does the spinner have?", "5", ["10", "8", "20"],
                   fr(1, 2) + " × " + fr(1, 5) + " = " + fr(1, 10) + ", so the spinner has <b>5</b> sections "
                   "(2 × 5 = 10 outcomes). 10 forgets the coin. 8 comes from adding outcomes: 2 + 8 = 10.", ans=n))
    assert len(its) == 20
    return {"title": "Word problems: games, lunches and field trips", "items": its}


# ============================================================ lesson
def body_html():
    tree = tree_svg(["H", "T"], ["red", "blue", "yellow"], label="tree diagram coin then spinner red blue yellow")
    tab = outcome_table_svg(["heads", "tails"], CUBE, "Number cube", label="outcome table coin and number cube")
    return (
        "<h2>Two independent events</h2>"
        "<p>Two events are <b>independent</b> when one does not change the chance of the other. "
        "Tossing a coin does not change how a number cube lands.</p>"
        "<p>The list of all possible outcomes is the <b>sample space</b>. Show it with a tree diagram or a table. "
        "Count the outcomes by <b>multiplying</b>: a coin (2) and a spinner with 3 equal sections give 2 × 3 = 6 outcomes.</p>"
        "<figure class='sn-fig'>" + tree +
        "<figcaption>Each coin branch splits into 3 colours: 6 outcomes.</figcaption></figure>"
        "<h2>Theoretical probability</h2>"
        "<p>When the outcomes are equally likely:</p>"
        "<p><b>probability = outcomes you want ÷ all the outcomes</b></p>"
        "<figure class='sn-fig'>" + tab +
        "<figcaption>A coin and a number cube: 2 × 6 = 12 outcomes.</figcaption></figure>"
        + ex("Example 1", "You toss a coin and roll a number cube. What is P(heads and 6)?",
             "H6 is 1 of the 12 outcomes in the table. You can also multiply: " + fr(1, 2) + " × " + fr(1, 6) + " = "
             + fr(1, 12) + ".", fr(1, 12) + " ≈ 0.083 ≈ 8.3%")
        + ex("Example 2", "You toss a coin and roll a number cube. What is P(tails and an even number)?",
             "T2, T4 and T6 are 3 of 12 outcomes.", fr(3, 12) + " = " + fr(1, 4) + " = 0.25 = 25%")
        + "<h2>Experimental probability</h2>"
        "<p>Experimental probability = times it happened ÷ number of trials. It is usually close to the theory, "
        "but rarely exactly the same. <b>More trials usually get closer.</b></p>"
        + table(["Tosses of two coins", "Two heads", "Experimental P(HH)"], [
            ["20", "8", fr(8, 20) + " = 0.4"],
            ["100", "29", fr(29, 100) + " = 0.29"],
            ["1000", "252", fr(252, 1000) + " = 0.252"],
        ])
        + ex("Example 3", "You toss two coins 200 times. About how many times would you expect two heads?",
             "P(HH) = " + fr(1, 4) + ". " + fr(1, 4) + " of 200 = 200 ÷ 4 = 50.", "about 50")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["P(heads and 6) = " + fr(1, 2) + " + " + fr(1, 6) + " = " + fr(4, 6),
             "Don’t add the probabilities. Count in the table, or multiply: " + fr(1, 12) + "."],
            ["A coin and a number cube give 2 + 6 = 8 outcomes.", "Multiply: 2 × 6 = 12 outcomes."],
            ["Two coins: HH, HT, TT (3 outcomes).", "HT and TH are different: 4 outcomes."],
            ["Two number cubes: P(sum of 7) = " + fr(1, 11) + ".", "The sums are not equally likely: " + fr(6, 36) + "."],
            ["“The experiment must match the theory exactly.”", "Results vary. More trials get closer."],
        ])
    )


FAQ = [
    {"q": "What are independent events in Grade 7 math?",
     "a": "Two events are independent when the result of one does not change the chance of the other, like tossing a coin and rolling a number cube. Taking two marbles from a bag without putting the first one back is not independent."},
    {"q": "How do you find the probability of two independent events?",
     "a": "List the sample space in a table or tree diagram, then divide the outcomes you want by all the outcomes. For a coin and a number cube, P(heads and 6) = 1/12, which is also 1/2 × 1/6."},
    {"q": "What is the difference between experimental and theoretical probability?",
     "a": "Theoretical probability is what should happen (1/4 for two heads). Experimental probability is what did happen in trials (for example 12 of 50 tosses = 0.24), and it usually gets closer to the theory with more trials."},
    {"q": "Is probability on the Grade 7 FSA?",
     "a": "The Grade 7 FSA numeracy section draws on the BC math curriculum, which includes probability. Practising tables, tree diagrams and fractions, decimals and percents like these helps students get ready."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (tables, tree diagrams, two spinners)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(37815)
    sets = [set_sample_spaces(), set_theory(), set_experimental(), set_compare(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "probability-of-two-independent-events",
        "sort": 15, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Probability of Two Independent Events",
        "seo_title": "Grade 7 Probability of Two Independent Events Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Probability of two independent events",
        "domain": "Data and probability",
        "standard_code": "Grade 7: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Experimental probability with two independent events",
        "meta_desc": "Free Grade 7 math worksheets on the probability of two independent events for the BC curriculum: sample spaces with tables and tree diagrams, theoretical probability as fractions, decimals and percents, experimental probability from results, and comparing the two. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "For two independent events, list every outcome in a table or tree diagram, then divide: outcomes you want ÷ all outcomes.",
        "key_sub": "A coin and a number cube give 2 × 6 = 12 outcomes, so P(heads and 6) = 1/12, not 1/2 + 1/6. Experimental results get closer to the theory with more trials.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(frequency table|tree diagram|outcome table|two spinners|sum table|results table)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
