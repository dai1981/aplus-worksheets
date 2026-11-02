# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Probability (Ontario Mathematics Curriculum 2020, Grade 6: Data, D2)
  python3 tools/gen_ca_math_g6_probability.py
The probability line from 0 to 1 (chance words to numbers, estimating), probability as a fraction, decimal and
percent (1/4 = 0.25 = 25%), probability from spinners, number cubes and bags, two independent events (coin and
spinner, coin and number cube, two spinners) with outcome tables and tree diagrams, and theoretical vs experimental
probability with predictions and decisions in Canadian contexts.
Wrong answers come from real student mistakes: probabilities greater than 1, part-to-part instead of part-to-whole
(3 red, 5 blue gives 3/5), counting colours or sections instead of section sizes, reading 1/4 as 0.4, adding the
outcomes of two events instead of multiplying (2 + 6 = 8), adding the probabilities of two events, treating HT and
TH as one outcome, and the gambler's fallacy (after 5 tails, heads is "due").
Every spinner is drawn to its exact fractions; every answer is checked in code with fractions.Fraction.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
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


def tree_svg(first, second, label="tree diagram"):
    """Tree diagram: first event (e.g. coin: H, T), then every outcome of the second event on each branch."""
    k = len(second)
    gap = 24
    top = 34
    rows = len(first) * k
    H = top + rows * gap + 4
    xr, xa, xb, xo = 14, 112, 214, 300
    s = [text(xa, 18, "Coin", 15), text(xb + 26, 18, "Spinner", 15), text(xo + 34, 18, "Outcome", 15)]
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
    W = int(xo + max(tw(a + ", " + b, 15, False) for a in first for b in second) + 10)
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


EQ3 = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 3), "yellow")]
TREE3 = lambda: tree_svg(["H", "T"], ["red", "blue", "yellow"],
                         label="tree diagram coin then spinner red blue yellow")
CUBE = [str(k) for k in range(1, 7)]
TABLE12 = lambda: outcome_table_svg(["heads", "tails"], CUBE, "Number cube",
                                    label="outcome table coin and number cube")


def outcomes(a, b):
    return [(x, y) for x in a for y in b]


# ============================================================ set 1: the probability line
def set_line():
    its = []
    its.append(mcq("What is the probability of an event that is impossible?", "0", ["1", fr(1, 2), "0.1"],
                   "An impossible event can never happen, so its probability is <b>0</b>. 0.1 is very unlikely, "
                   "but it can still happen.", ans=0))
    its.append(mcq("What is the probability of an event that is certain?", "1", ["0", "100", fr(1, 2)],
                   "A certain event will happen, so its probability is <b>1</b> (or 100%). The number 100 on its own "
                   "is far bigger than 1, so it can’t be a probability.", ans=1))
    its.append(mcq("An event is equally likely to happen or not happen. What is its probability?", fr(1, 2),
                   ["2", "1", "0"],
                   "Equally likely is halfway between 0 and 1: <b>" + fr(1, 2) + "</b> (0.5 or 50%). "
                   "2 is the number of outcomes, not the probability.", ans=F(1, 2)))
    its.append(mcq("Which number can NOT be a probability?", "1.5", ["0.5", "0", "1"],
                   "Probabilities go from 0 to 1. <b>1.5</b> is bigger than 1, so it can’t be a probability. "
                   "0 and 1 are allowed: they mean impossible and certain."))
    its.append(mcq("Which percent can NOT be a probability?", "120%", ["12%", "0%", "100%"],
                   "As a percent, probabilities go from 0% to 100%. <b>120%</b> is more than 100%, so it is not possible."))
    its.append(mcq(fig(scale_svg(10, [(F(8, 10), "")], TENTHS, label="probability line arrow at 0.8")) +
                   "Which word best describes the chance shown by the arrow?", "likely",
                   ["unlikely", "certain", "equally likely"],
                   "The arrow is at 0.8. That is between 0.5 and 1, close to 1: <b>likely</b>. "
                   "It is not certain, because it is not at 1."))
    its.append(mcq(fig(scale_svg(10, [(F(1, 10), "")], TENTHS, label="probability line arrow at 0.1")) +
                   "Which word best describes the chance shown by the arrow?", "unlikely",
                   ["impossible", "likely", "equally likely"],
                   "The arrow is at 0.1, close to 0 but not at 0: <b>unlikely</b>. Impossible would be exactly 0."))
    its.append(mcq("Which probability means an event is very likely?", "0.95", ["0.05", "0.5", "9.5"],
                   "<b>0.95</b> is very close to 1, so the event is very likely. 0.05 is very close to 0 (very unlikely). "
                   "9.5 is bigger than 1, so it is not a probability."))
    its.append(mcq("Which probability shows the most likely event?", "0.8", ["0.08", "0.35", "0.5"],
                   "Compare the tenths: 0.8 = 0.80 is the greatest. 0.35 has more digits, but 0.35 &lt; 0.80. "
                   "So <b>0.8</b> is most likely.", ans=F(8, 10)))
    assert max(F("0.8"), F("0.08"), F("0.35"), F("0.5")) == F("0.8")
    its.append(mcq("Which probability shows the least likely event?", "0.05", ["0.5", "0.15", "0.3"],
                   "Write them with two decimal places: 0.05, 0.50, 0.15, 0.30. The least is <b>0.05</b>, "
                   "so that event is least likely.", ans=F(5, 100)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a 7?", "0",
                   ["1", fr(1, 7), fr(1, 6)],
                   "The cube only has 1 to 6, so a 7 is impossible. Its probability is <b>0</b>.", ans=0))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a number "
                   "from 1 to 6?", "1", [fr(1, 6), fr(1, 2), "6"],
                   "Every roll gives a number from 1 to 6, so it is certain: <b>1</b>. "
                   "6 is the number of outcomes, and probabilities are never more than 1.", ans=1))
    its.append(mcq(fig(scale_svg(4, [(F(1, 4), "")], ENDS, label="probability line in quarters arrow at one quarter")) +
                   "The probability line is split into quarters. What probability does the arrow show?", fr(1, 4),
                   [fr(3, 4), fr(1, 3), "0.4"],
                   "There are 4 equal parts from 0 to 1, and the arrow is 1 part from 0: <b>" + fr(1, 4) + "</b> (0.25). "
                   + fr(3, 4) + " counts from the 1 end. " + fr(1, 4) + " is 0.25, not 0.4.", ans=F(1, 4)))
    its.append(mcq(fig(scale_svg(10, [(F(7, 10), "")], TENTHS, label="probability line arrow at 0.7")) +
                   "The probability line is split into tenths. What probability does the arrow show?", "0.7",
                   ["0.07", "0.3", "7"],
                   "Each small step is 0.1. The arrow is 7 steps from 0, so it shows <b>0.7</b>. "
                   "0.3 counts back from 1. 7 is too big to be a probability.", ans=F(7, 10)))
    its.append(mcq(fig(scale_svg(10, [(F(3, 10), "")], TENTHS, label="probability line arrow at 0.3")) +
                   "What probability does the arrow show, as a percent?", "30%",
                   ["3%", "70%", "0.3%"],
                   "The arrow is at 0.3. 0.3 = 30 hundredths = <b>30%</b>. 3% would be 0.03.", ans=F(3, 10)))
    its.append(mcq("Owen says the probability that his hockey team wins on Saturday is 1.2, because they are very good. "
                   "What is wrong?", "A probability can’t be more than 1",
                   ["Nothing, strong teams can go above 1", "It should be written as 120%", "It should be 12"],
                   "Even a certain event has probability 1 (100%). <b>A probability can’t be more than 1</b>. "
                   "A very good team might be 0.8 or 0.9: likely, not certain."))
    its.append(mcq("Which list orders these probabilities from least likely to most likely?<br>0.6, 0.25, 0.9, 0.06",
                   "0.06, 0.25, 0.6, 0.9",
                   ["0.9, 0.6, 0.25, 0.06", "0.06, 0.6, 0.25, 0.9", "0.6, 0.06, 0.9, 0.25"],
                   "Write them as hundredths: 0.60, 0.25, 0.90, 0.06. Least to greatest: <b>0.06, 0.25, 0.6, 0.9</b>. "
                   "0.25 is less than 0.6, even though 25 is more than 6."))
    assert sorted([F("0.6"), F("0.25"), F("0.9"), F("0.06")]) == [F("0.06"), F("0.25"), F("0.6"), F("0.9")]
    marks = [(F(0), "A"), (F(3, 10), "B"), (F(7, 10), "C"), (F(1), "D")]
    its.append(mcq_fixed(fig(scale_svg(10, marks, TENTHS, label="probability line with points A B C D")) +
                         "A bag has 3 red and 7 blue marbles. You take one without looking. "
                         "Which letter shows the probability of taking a red marble?", ["A", "B", "C", "D"], 1,
                         "3 of the 10 marbles are red: " + fr(3, 10) + " = 0.3. That is point <b>B</b>. "
                         "C (0.7) is the probability of blue."))
    assert F(3, 10) == marks[1][0]
    its.append(mcq_fixed(fig(scale_svg(10, marks, TENTHS, label="probability line with points A B C D")) +
                         "A spinner has 10 equal sections: 7 green and 3 yellow. "
                         "Which letter shows the probability of landing on green?", ["A", "B", "C", "D"], 2,
                         "7 of the 10 equal sections are green: " + fr(7, 10) + " = 0.7. That is point <b>C</b>."))
    assert F(7, 10) == marks[2][0]
    its.append(mcq("Arjun estimates the probability of four events. Which estimate makes the most sense?",
                   "snow on the ground in Winnipeg on January 15: 0.9",
                   ["a coin landing on heads: 0.9", "rolling a 6 on a number cube: 0.6",
                    "snow in Toronto on July 15: 0.5"],
                   "Winnipeg almost always has snow on the ground in January, so 0.9 (very likely) makes sense. "
                   "A coin is about 0.5 for heads, a 6 is only " + fr(1, 6) + " (about 0.17), and snow in Toronto in "
                   "July is close to 0. So the answer is <b>snow in Winnipeg in January</b>."))
    return {"title": "The probability line from 0 to 1", "items": its}


# ============================================================ set 2: fractions, decimals and percents
def set_fdp():
    its = []
    its.append(mcq("The probability of heads is " + fr(1, 2) + ". What is this as a decimal?", "0.5",
                   ["0.2", "1.2", "0.12"],
                   fr(1, 2) + " = 1 ÷ 2 = <b>0.5</b>. Writing the digits 1 and 2 as 0.12 or 1.2 is a common mistake.",
                   ans=F(1, 2)))
    its.append(mcq("The probability of landing on blue is " + fr(1, 4) + ". What is this as a percent?", "25%",
                   ["14%", "4%", "40%"],
                   fr(1, 4) + " = " + fr(25, 100) + " = <b>25%</b>. 14% just writes the digits 1 and 4.", ans=F(1, 4)))
    its.append(mcq("Write the probability " + fr(3, 10) + " as a decimal.", "0.3", ["0.03", "3.1", "0.13"],
                   fr(3, 10) + " is 3 tenths = <b>0.3</b>. 0.03 is 3 hundredths.", ans=F(3, 10)))
    its.append(mcq("Write the probability 0.75 as a percent.", "75%", ["7.5%", "0.75%", "25%"],
                   "To change a decimal to a percent, multiply by 100: 0.75 × 100 = <b>75%</b>.", ans=F(3, 4)))
    its.append(mcq("Which fraction is equal to the probability 0.2?", fr(1, 5), [fr(1, 2), fr(2, 100), fr(1, 20)],
                   "0.2 = " + fr(2, 10) + " = <b>" + fr(1, 5) + "</b>. " + fr(1, 2) + " is 0.5, and "
                   + fr(2, 100) + " is 0.02.", ans=F(1, 5)))
    its.append(mcq("Write the probability " + fr(1, 5) + " as a percent.", "20%", ["15%", "5%", "50%"],
                   fr(1, 5) + " = " + fr(20, 100) + " = <b>20%</b>. Multiply the numerator and denominator by 20.",
                   ans=F(1, 5)))
    its.append(mcq("Write the probability " + fr(9, 10) + " as a decimal.", "0.9", ["0.09", "9.1", "0.1"],
                   fr(9, 10) + " is 9 tenths = <b>0.9</b>. 0.1 is the probability that the event does NOT happen.",
                   ans=F(9, 10)))
    its.append(mcq("Write the probability " + fr(3, 5) + " as a percent.", "60%", ["35%", "30%", "53%"],
                   fr(3, 5) + " = " + fr(60, 100) + " = <b>60%</b>. Multiply the numerator and denominator by 20.",
                   ans=F(3, 5)))
    its.append(mcq("Write the probability 40% as a fraction in lowest terms.", fr(2, 5), [fr(1, 4), fr(4, 100), fr(1, 40)],
                   "40% = " + fr(40, 100) + ". Divide the numerator and denominator by 20: <b>" + fr(2, 5) + "</b>. "
                   + fr(4, 100) + " would be 4%.", ans=F(2, 5)))
    its.append(mcq("Write the probability 0.05 as a percent.", "5%", ["50%", "0.05%", "0.5%"],
                   "0.05 × 100 = <b>5%</b>. 50% would be 0.5.", ans=F(5, 100)))
    its.append(mcq("Write the probability " + fr(1, 8) + " as a decimal.", "0.125", ["0.8", "0.18", "1.8"],
                   "1 ÷ 8 = <b>0.125</b>. A quick check: " + fr(1, 4) + " = 0.25, and " + fr(1, 8) + " is half of that.",
                   ans=F(1, 8)))
    its.append(mcq("Write the probability " + fr(7, 20) + " as a percent.", "35%", ["7%", "27%", "72%"],
                   "Multiply the numerator and denominator by 5: " + fr(7, 20) + " = " + fr(35, 100) + " = <b>35%</b>. "
                   "27% comes from adding 7 + 20.", ans=F(7, 20)))
    its.append(mcq("Write the probability " + fr(12, 25) + " as a decimal.", "0.48", ["0.12", "0.37", "0.24"],
                   "Multiply the numerator and denominator by 4: " + fr(12, 25) + " = " + fr(48, 100) + " = <b>0.48</b>. "
                   "0.37 comes from adding 12 + 25.", ans=F(12, 25)))
    its.append(mcq("Write the probability " + fr(6, 8) + " as a percent.", "75%", ["68%", "6.8%", "60%"],
                   fr(6, 8) + " = " + fr(3, 4) + " = <b>75%</b>. 68% just writes the digits 6 and 8.", ans=F(6, 8)))
    its.append(mcq("The weather forecast says there is a 30% chance of snow. What is this as a decimal?", "0.3",
                   ["0.03", "3.0", "30"],
                   "30% = " + fr(30, 100) + " = <b>0.3</b>. Divide by 100 to change a percent to a decimal.",
                   ans=F(3, 10)))
    its.append(mcq("Which of these is NOT equal to a probability of " + fr(1, 2) + "?", "0.2",
                   ["0.5", "50%", fr(2, 4)],
                   fr(1, 2) + " = 0.5 = 50% = " + fr(2, 4) + ". <b>0.2</b> is " + fr(1, 5) + ", not a half.",
                   same_ok=True))
    its.append(mcq("Which of these is NOT equal to a probability of " + fr(3, 4) + "?", "0.34",
                   ["0.75", "75%", fr(6, 8)],
                   fr(3, 4) + " = 0.75 = 75% = " + fr(6, 8) + ". <b>0.34</b> just writes the digits 3 and 4; it is not "
                   + fr(3, 4) + ".", same_ok=True))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    assert part(sp, "blue") == F(1, 4) == F("0.25")
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow")) +
                   "Which shows the probability of landing on blue as a fraction, a decimal and a percent?",
                   fr(1, 4) + ", 0.25, 25%",
                   [fr(1, 4) + ", 0.4, 40%", fr(1, 4) + ", 0.14, 14%", fr(1, 2) + ", 0.5, 50%"],
                   "Blue covers one quarter of the spinner: <b>" + fr(1, 4) + " = 0.25 = 25%</b>. "
                   + fr(1, 2) + " is the probability of red. " + fr(1, 4) + " is 0.25, not 0.4 or 0.14."))
    its.append(mcq("Which probability is the greatest?", fr(3, 4), ["0.7", "72%", "0.69"],
                   "Change them all to decimals: " + fr(3, 4) + " = 0.75, 0.7 = 0.70, 72% = 0.72, 0.69. "
                   "The greatest is <b>" + fr(3, 4) + "</b>.", ans=F(3, 4)))
    assert F(3, 4) > max(F("0.7"), F("0.72"), F("0.69"))
    its.append(mcq("Which list orders these probabilities from least to greatest?",
                   fr(1, 4) + ", 0.3, 35%",
                   ["35%, 0.3, " + fr(1, 4), "0.3, " + fr(1, 4) + ", 35%", fr(1, 4) + ", 35%, 0.3"],
                   "Change them to decimals: " + fr(1, 4) + " = 0.25, 0.3 = 0.30, 35% = 0.35. "
                   "So the order is <b>" + fr(1, 4) + ", 0.3, 35%</b>. " + fr(1, 4) + " is 0.25, not 0.4."))
    assert F(1, 4) < F("0.3") < F("0.35")
    return {"title": "Probability as a fraction, decimal and percent", "items": its}


# ============================================================ set 3: spinners, number cubes and bags
def set_find():
    its = []
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a 4?", fr(1, 6),
                   [fr(1, 4), fr(4, 6), fr(1, 5)],
                   "There are 6 equally likely outcomes and only one of them is 4: <b>" + fr(1, 6) + "</b>. "
                   + fr(4, 6) + " would be the chance of 1, 2, 3 or 4.", ans=F(1, 6)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling an even number?",
                   fr(3, 6), [fr(1, 6), fr(2, 6), fr(6, 3)],
                   "The even numbers are 2, 4 and 6: 3 of the 6 outcomes, so <b>" + fr(3, 6) + "</b> (= " + fr(1, 2) + "). "
                   + fr(6, 3) + " is upside down: it is greater than 1.", ans=F(1, 2)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a number "
                   "greater than 4?", fr(2, 6), [fr(3, 6), fr(4, 6), fr(1, 6)],
                   "Greater than 4 means 5 or 6: 2 of the 6 outcomes, so <b>" + fr(2, 6) + "</b>. "
                   + fr(3, 6) + " wrongly includes the 4. " + fr(1, 6) + " forgets the 5.", ans=F(1, 3)))
    its.append(mcq(fig(bag_svg([("red", 3), ("blue", 5)])) +
                   "A bag has 3 red and 5 blue marbles. You take one without looking. What is the probability of red?",
                   fr(3, 8), [fr(3, 5), fr(5, 8), fr(1, 2)],
                   "There are 3 + 5 = 8 marbles and 3 are red: <b>" + fr(3, 8) + "</b>. " + fr(3, 5) +
                   " compares red with blue, not with all the marbles. Two colours does not mean " + fr(1, 2) + ".",
                   ans=F(3, 8)))
    its.append(mcq(fig(bag_svg([("red", 4), ("blue", 2), ("yellow", 2)])) +
                   "You take one marble without looking. What is the probability of blue?",
                   fr(2, 8), [fr(2, 6), fr(4, 8), fr(6, 8)],
                   "There are 4 + 2 + 2 = 8 marbles and 2 are blue: <b>" + fr(2, 8) + "</b> (= " + fr(1, 4) + "). "
                   + fr(2, 6) + " compares blue with the other 6 marbles, not with all 8. " + fr(4, 8) + " is red.",
                   ans=F(1, 4)))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner red half")) + "What is the probability of landing on red?",
                   fr(1, 2), [fr(1, 3), fr(1, 4), fr(2, 3)],
                   "Red covers half of the spinner: <b>" + fr(1, 2) + "</b>. " + fr(1, 3) +
                   " counts the colours, but the sections are not equal.", ans=part(sp, "red")))
    sp = [("G", F(1, 8), "green"), ("Y", F(1, 8), "yellow"), ("Y", F(1, 8), "yellow"), ("G", F(1, 8), "green"),
          ("Y", F(1, 8), "yellow"), ("Y", F(1, 8), "yellow"), ("G", F(1, 8), "green"), ("Y", F(1, 8), "yellow")]
    assert part(sp, "G") == F(3, 8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner eight sections three green")) +
                   "The spinner has 8 equal sections: G is green and Y is yellow. What is the probability of green?",
                   fr(3, 8), [fr(3, 5), fr(5, 8), fr(1, 8)],
                   "3 of the 8 equal sections are green: <b>" + fr(3, 8) + "</b>. " + fr(3, 5) +
                   " compares green with yellow. " + fr(5, 8) + " is yellow.", ans=F(3, 8)))
    its.append(mcq("A spinner has 10 equal sections: 3 blue and 7 red. What is the probability of blue as a decimal?",
                   "0.3", ["0.03", "0.7", "0.37"],
                   "3 of the 10 sections are blue: " + fr(3, 10) + " = <b>0.3</b>. 0.7 is the probability of red.",
                   ans=F(3, 10)))
    its.append(mcq("A bag has 20 marbles and 5 of them are green. What is the probability of green as a percent?",
                   "25%", ["5%", "20%", "75%"],
                   fr(5, 20) + " = " + fr(25, 100) + " = <b>25%</b>. 5% uses the number of green marbles as the "
                   "percent. 75% is NOT green.", ans=F(5, 20)))
    its.append(mcq("A bag has 3 red and 7 yellow marbles. What is the probability of NOT getting red?",
                   fr(7, 10), [fr(3, 10), fr(7, 3), fr(1, 10)],
                   "Not red means yellow: 7 of the 10 marbles, so <b>" + fr(7, 10) + "</b>. Check: "
                   + fr(3, 10) + " + " + fr(7, 10) + " = 1.", ans=F(7, 10)))
    its.append(mcq("Cards numbered 1 to 10 are shuffled. You pick one. What is the probability of a multiple of 3?",
                   fr(3, 10), [fr(1, 3), fr(3, 7), fr(10, 3)],
                   "The multiples of 3 are 3, 6 and 9: 3 of the 10 cards, so <b>" + fr(3, 10) + "</b>. "
                   + fr(1, 3) + " comes from the word “3”, not from counting cards.", ans=F(3, 10)))
    assert [k for k in range(1, 11) if k % 3 == 0] == [3, 6, 9]
    sp = [(str(k), F(1, 8), NUMFILL[k - 1]) for k in range(1, 9)]
    primes = [k for k in range(1, 9) if k > 1 and all(k % d for d in range(2, k))]
    assert primes == [2, 3, 5, 7]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 1 to 8")) + "What is the probability of landing on a prime number?",
                   fr(4, 8), [fr(3, 8), fr(5, 8), fr(1, 8)],
                   "The prime numbers are 2, 3, 5 and 7: 4 of the 8 sections, so <b>" + fr(4, 8) + "</b> (= " + fr(1, 2) + "). "
                   + fr(5, 8) + " wrongly counts 1, which is not prime. " + fr(3, 8) + " forgets 2.", ans=F(1, 2)))
    its.append(mcq("A bag has 2 red, 3 blue and 5 green marbles. What is the probability of red or blue?",
                   fr(5, 10), [fr(2, 10), fr(3, 10), fr(5, 5)],
                   "Red or blue: 2 + 3 = 5 of the 10 marbles, so <b>" + fr(5, 10) + "</b>. " + fr(5, 5) +
                   " compares red and blue with green; it would mean certain.", ans=F(1, 2)))
    sp = [("red", F(1, 8), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"), ("red", F(1, 8), "red"),
          ("blue", F(1, 4), "blue")]
    assert part(sp, "red") == F(1, 4) and len(sp) == 5
    its.append(mcq(fig(spinner_svg(sp, label="spinner red in two small parts")) +
                   "Red is in two small parts, each one eighth of the spinner. What is the probability of red?",
                   fr(1, 4), [fr(1, 8), fr(1, 3), fr(2, 5)],
                   fr(1, 8) + " + " + fr(1, 8) + " = " + fr(2, 8) + " = <b>" + fr(1, 4) + "</b>. "
                   + fr(2, 5) + " counts 2 of the 5 sections, but the sections are not the same size.", ans=F(1, 4)))
    word = "TORONTO"
    assert word.count("O") == 3 and len(word) == 7 and len(set(word)) == 4
    its.append(mcq("The letters of TORONTO are written on 7 cards. You pick one card without looking. "
                   "What is the probability of O?",
                   fr(3, 7), [fr(1, 7), fr(1, 4), fr(3, 4)],
                   "TORONTO has 7 letters and 3 of them are O: <b>" + fr(3, 7) + "</b>. "
                   + fr(1, 4) + " counts the 4 different letters, but O is on 3 cards. "
                   + fr(3, 4) + " compares the 3 O cards with the other 4 cards.", ans=F(3, 7)))
    its.append(mcq("A 12-sided die has the numbers 1 to 12. What is the probability of rolling a number greater than 9, "
                   "as a percent?", "25%", ["75%", "3%", "33%"],
                   "Greater than 9 means 10, 11 or 12: " + fr(3, 12) + " = " + fr(1, 4) + " = <b>25%</b>. "
                   "3% uses the count as the percent.", ans=F(3, 12)))
    A = [("red", F(1, 4), "red"), ("blue", F(1, 2), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green")]
    B = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 3), "yellow")]
    C = [("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green"),
         ("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green")]
    D = [("blue", F(1, 4), "blue"), ("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("blue", F(1, 4), "blue")]
    blues = [part(x, "blue") for x in (A, B, C, D)]
    assert blues == [F(1, 2), F(1, 3), F(1, 4), F(3, 4)]
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D])) + "On which spinner is the probability of blue " + fr(1, 4) + "?",
                         ["A", "B", "C", "D"], 2,
                         "On spinner <b>C</b> blue has 2 of the 8 equal sections: " + fr(2, 8) + " = " + fr(1, 4) + ". "
                         "A has 4 sections, but blue is half of it."))
    bags = {"4 red, 4 blue": (4, 4), "5 red, 10 blue": (5, 10), "2 red, 4 blue": (2, 4), "3 red, 5 blue": (3, 5)}
    assert [k for k, (r, b) in bags.items() if F(r, r + b) == F(1, 2)] == ["4 red, 4 blue"]
    its.append(mcq("Which bag gives a probability of 0.5 for taking a red marble?", "4 red, 4 blue",
                   ["5 red, 10 blue", "2 red, 4 blue", "3 red, 5 blue"],
                   "0.5 means half of the marbles are red. With <b>4 red and 4 blue</b>, 4 of 8 are red. "
                   "5 red, 10 blue gives " + fr(5, 15) + ", not " + fr(5, 10) + "."))
    its.append(mcq("A bag has 10 marbles. The probability of red is " + fr(2, 5) + ". How many red marbles are there?",
                   "4", ["2", "5", "6"],
                   fr(2, 5) + " = " + fr(4, 10) + ", so <b>4</b> of the 10 marbles are red. "
                   "2 uses the numerator without changing to tenths. 6 is the number that are not red.", ans=4))
    assert F(2, 5) * 10 == 4
    its.append(mcq("A bag has 3 green marbles and some blue marbles. The probability of green is " + fr(1, 4) +
                   ". How many blue marbles are there?", "9", ["12", "4", "1"],
                   fr(1, 4) + " = " + fr(3, 12) + ", so there are 12 marbles in total. 12 − 3 = <b>9</b> blue. "
                   "12 is the total, not the number of blue marbles.", ans=9))
    assert F(3, 3 + 9) == F(1, 4)
    return {"title": "Spinners, number cubes and bags", "items": its}


# ============================================================ set 4: two independent events
def set_two_events():
    its = []
    o6 = outcomes("HT", ["red", "blue", "yellow"])
    assert len(o6) == 6
    its.append(mcq("You toss a coin and spin a spinner with 3 equal sections: red, blue and yellow. "
                   "How many different outcomes are there?", "6", ["5", "3", "9"],
                   "Each coin face goes with each of the 3 colours: 2 × 3 = <b>6</b> outcomes. "
                   "5 comes from adding 2 + 3, which is a common mistake.", ans=6))
    tree = lambda: fig(TREE3())
    its.append(mcq(tree() + "The tree diagram shows tossing a coin, then spinning a spinner with 3 equal sections. "
                   "What is the probability of heads and red?", fr(1, 6), [fr(1, 5), fr(1, 3), fr(5, 6)],
                   "Heads and red is 1 of the 6 equally likely outcomes: <b>" + fr(1, 6) + "</b>. "
                   + fr(1, 5) + " adds the outcomes (2 + 3) instead of multiplying. " + fr(5, 6) + " adds "
                   + fr(1, 2) + " + " + fr(1, 3) + ".", ans=F(sum(1 for o in o6 if o == ("H", "red")), 6)))
    n = sum(1 for c, s in o6 if c == "T" and s != "red")
    assert n == 2
    its.append(mcq(tree() + "Use the tree diagram. What is the probability of tails and NOT red?", fr(2, 6),
                   [fr(1, 6), fr(4, 6), fr(2, 5)],
                   "Tails and not red: T, blue and T, yellow. That is 2 of 6 outcomes: <b>" + fr(2, 6) + "</b>. "
                   + fr(4, 6) + " counts every outcome that is not red, with heads too. " + fr(2, 5) +
                   " adds 2 + 3 outcomes instead of multiplying.", ans=F(n, 6)))
    n = sum(1 for c, s in o6 if s == "red")
    assert n == 2
    its.append(mcq(tree() + "Use the tree diagram. What is the probability of red, with either heads or tails?",
                   fr(2, 6), [fr(1, 6), fr(3, 6), fr(2, 5)],
                   "Red shows up in 2 outcomes: H, red and T, red. So the probability is <b>" + fr(2, 6) + "</b> (= "
                   + fr(1, 3) + "), the same as spinning red on its own. " + fr(1, 6) + " forgets T, red. "
                   + fr(2, 5) + " adds 2 + 3 outcomes instead of multiplying.", ans=F(n, 6)))
    o12 = outcomes("HT", range(1, 7))
    assert len(o12) == 12
    its.append(mcq("You toss a coin and roll a number cube with the numbers 1 to 6. How many different outcomes are there?",
                   "12", ["8", "6", "2"],
                   "Each coin face goes with each of the 6 numbers: 2 × 6 = <b>12</b>. "
                   "8 comes from adding 2 + 6.", ans=12))
    tab = lambda: fig(TABLE12())
    its.append(mcq(tab() + "The table shows every outcome of tossing a coin and rolling a number cube. "
                   "What is the probability of heads and a 6?", fr(1, 12), [fr(1, 8), fr(1, 6), fr(4, 6)],
                   "H6 is 1 of the 12 outcomes in the table: <b>" + fr(1, 12) + "</b>. " + fr(1, 8) +
                   " adds 2 + 6 outcomes. " + fr(4, 6) + " adds " + fr(1, 2) + " + " + fr(1, 6) + ".",
                   ans=F(sum(1 for o in o12 if o == ("H", 6)), 12)))
    n = sum(1 for c, k in o12 if c == "T" and k % 2 == 0)
    assert n == 3
    its.append(mcq(tab() + "Use the table. What is the probability of tails and an even number?", fr(3, 12),
                   [fr(3, 8), fr(3, 6), fr(1, 12)],
                   "Tails and even: T2, T4 and T6. That is 3 of 12 outcomes: <b>" + fr(3, 12) + "</b> (= " + fr(1, 4) + "). "
                   + fr(3, 6) + " only looks at the number cube.", ans=F(n, 12)))
    n = sum(1 for c, k in o12 if c == "H" and k > 4)
    assert n == 2
    its.append(mcq(tab() + "Use the table. What is the probability of heads and a number greater than 4?", fr(2, 12),
                   [fr(2, 8), fr(4, 12), fr(1, 12)],
                   "Heads and greater than 4: H5 and H6. That is 2 of 12 outcomes: <b>" + fr(2, 12) + "</b>. "
                   + fr(4, 12) + " also counts T5 and T6.", ans=F(n, 12)))
    its.append(mcq("A coin is tossed and a spinner with 2 equal sections (red and blue) is spun. "
                   "Which list shows all the outcomes? (H = heads, T = tails, R = red, B = blue)",
                   "HR, HB, TR, TB", ["H, T, R, B", "HR, TB", "HR, HB, TR, TB, HT"],
                   "Pair each coin face with each colour: 2 × 2 = 4 outcomes, <b>HR, HB, TR, TB</b>. "
                   "H, T, R, B lists single results, not pairs. HT is not possible: there is only one coin."))
    A2 = [("red", F(1, 2), "red"), ("blue", F(1, 2), "blue")]
    B4 = [(str(k), F(1, 4), NUMFILL[k - 1]) for k in range(1, 5)]
    two = lambda: fig(spinners_row_svg([A2, B4], ["Spinner A", "Spinner B"], label="two spinners A and B"))
    o8 = outcomes(["red", "blue"], range(1, 5))
    assert len(o8) == 8
    its.append(mcq(two() + "You spin spinner A and spinner B. How many different outcomes are there?", "8",
                   ["6", "4", "16"],
                   "Each colour goes with each of the 4 numbers: 2 × 4 = <b>8</b>. 6 comes from adding 2 + 4.", ans=8))
    its.append(mcq(two() + "You spin both spinners. What is the probability of blue and 4?", fr(1, 8),
                   [fr(1, 6), fr(3, 4), fr(1, 4)],
                   "Blue and 4 is 1 of the 8 outcomes (red 1 … blue 4): <b>" + fr(1, 8) + "</b>. " + fr(1, 6) +
                   " adds the outcomes (2 + 4). " + fr(3, 4) + " adds " + fr(1, 2) + " + " + fr(1, 4) + ".",
                   ans=F(sum(1 for o in o8 if o == ("blue", 4)), 8)))
    its.append(mcq("Nathan says, “A coin has 2 outcomes and a number cube has 6, so together there are 2 + 6 = 8 outcomes.” "
                   "What is wrong?", "Each coin face pairs with all 6 numbers: 2 × 6 = 12",
                   ["Nothing, 2 + 6 = 8 is right", "There are only 6 outcomes; the coin does not count",
                    "There are 2 × 6 × 2 = 24 outcomes"],
                   "Heads can go with 1, 2, 3, 4, 5 or 6, and so can tails. That makes 6 + 6 = 2 × 6 = <b>12</b> "
                   "outcomes. Multiply, don’t add."))
    o4 = outcomes("HT", "HT")
    n = sum(1 for a, b in o4 if a != b)
    assert n == 2 and len(o4) == 4
    its.append(mcq("You toss two coins. What is the probability of getting one head and one tail?", fr(2, 4),
                   [fr(1, 3), fr(1, 4), fr(2, 3)],
                   "The outcomes are HH, HT, TH and TT. One head and one tail is HT or TH: <b>" + fr(2, 4) + "</b> (= "
                   + fr(1, 2) + "). " + fr(1, 3) + " forgets that HT and TH are different outcomes.", ans=F(n, 4)))
    its.append(mcq("You toss two coins. What is the probability of getting two heads?", fr(1, 4),
                   [fr(1, 3), fr(1, 2), fr(3, 4)],
                   "HH is 1 of the 4 outcomes (HH, HT, TH, TT): <b>" + fr(1, 4) + "</b>. " + fr(1, 3) +
                   " uses only 3 outcomes (two heads, one of each, two tails), but they are not equally likely. "
                   + fr(3, 4) + " is NOT two heads.", ans=F(1, 4)))
    its.append(mcq("Mei tosses a coin and gets heads. Then she rolls a number cube. What is the probability that "
                   "the number cube shows a 6?", fr(1, 6), [fr(1, 12), fr(1, 2), fr(4, 6)],
                   "The coin does not change the number cube: the events are independent. A 6 is still <b>" + fr(1, 6) +
                   "</b>. " + fr(1, 12) + " is the chance of heads AND 6 before anything is tossed.", ans=F(1, 6)))
    its.append(mcq("Which two events are independent?", "Tossing a coin and spinning a spinner",
                   ["Taking two marbles from a bag without putting the first one back",
                    "Rain this morning and a wet schoolyard at recess",
                    "Practising free throws and making more baskets"],
                   "Two events are independent when one does not change the chance of the other. A coin can’t change "
                   "a spinner, so <b>tossing a coin and spinning a spinner</b> are independent. Taking a marble out "
                   "changes what is left in the bag."))
    o8b = outcomes("HT", range(1, 5))
    n = sum(1 for c, k in o8b if c == "T" and k % 2 == 1)
    assert n == 2
    its.append(mcq("You toss a coin and spin a spinner with 4 equal sections: 1, 2, 3 and 4. "
                   "What is the probability of tails and an odd number?", fr(2, 8), [fr(2, 6), fr(2, 4), fr(1, 8)],
                   "There are 2 × 4 = 8 outcomes. Tails and odd: T1 and T3. So the probability is <b>" + fr(2, 8) +
                   "</b> (= " + fr(1, 4) + "). " + fr(2, 6) + " adds 2 + 4 outcomes. " + fr(2, 4) +
                   " only looks at the spinner.", ans=F(n, 8)))
    its.append(mcq(tab() + "Use the table. What is the probability of heads and any number from 1 to 6?", fr(6, 12),
                   [fr(1, 12), "1", fr(6, 8)],
                   "H1, H2, H3, H4, H5 and H6: 6 of the 12 outcomes, so <b>" + fr(6, 12) + "</b> (= " + fr(1, 2) + "). "
                   "It is the same as the chance of heads, because every number is allowed.",
                   ans=F(sum(1 for c, k in o12 if c == "H"), 12)))
    its.append(mcq("You toss a coin and roll a number cube 120 times. About how many times would you expect "
                   "heads and a 6?", "about 10", ["about 20", "about 60", "about 15"],
                   "Heads and 6 is 1 of 12 outcomes. " + fr(1, 12) + " of 120 is 120 ÷ 12 = 10, so <b>about 10</b>. "
                   "About 15 comes from 120 ÷ 8 (adding 2 + 6 outcomes)."))
    assert F(1, 12) * 120 == 10 and F(120, 8) == 15
    pa = F(1, 2) * F(1, 4)
    pb = F(2, 6)
    assert pa == F(1, 8) and pb > pa
    its.append(mcq("Game A: you win if a coin shows heads AND a spinner with 4 equal colours lands on red. "
                   "Game B: you win if a number cube shows 1 or 2. Which game gives a better chance of winning?",
                   "Game B", ["Game A", "They are the same", "You can’t tell"],
                   "Game A: heads and red is 1 of 2 × 4 = 8 outcomes, so " + fr(1, 8) + ". "
                   "Game B: 2 of 6 outcomes, so " + fr(2, 6) + " = " + fr(1, 3) + ". " + fr(1, 3) + " &gt; " + fr(1, 8) +
                   ", so <b>Game B</b> is better."))
    return {"title": "Two independent events: tables and tree diagrams", "items": its}


# ============================================================ set 5: experiments, predictions and decisions
def set_experiments():
    its = []
    its.append(mcq("Liam rolls a number cube 60 times. About how many times would he expect to roll a 6?", "about 10",
                   ["about 6", "about 1", "about 30"],
                   "A 6 has a theoretical probability of " + fr(1, 6) + ". " + fr(1, 6) + " of 60 is 60 ÷ 6 = 10, "
                   "so <b>about 10</b>."))
    assert F(1, 6) * 60 == 10
    its.append(mcq("Zoe tosses a coin 100 times. How many heads should she expect?", "about 50",
                   ["exactly 50", "about 100", "about 2"],
                   "Half of 100 is 50. Results change from one experiment to the next, so expect <b>about 50</b>, "
                   "not exactly 50."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red")) +
                   "Aiden spins this spinner 40 times. About how many times should he expect red?", "about 30",
                   ["about 10", "about 3", "about 40"],
                   "Red is " + fr(3, 4) + " of the spinner. 40 ÷ 4 = 10, and 3 × 10 = 30, so <b>about 30</b>. "
                   "About 10 is for blue."))
    assert part(sp, "red") * 40 == 30
    its.append(mcq("Benjamin tosses a coin 50 times and gets 23 heads. What is the experimental probability of heads?",
                   fr(23, 50), [fr(23, 27), fr(1, 2), fr(27, 50)],
                   "Experimental probability = number of times it happened ÷ number of trials = <b>" + fr(23, 50) +
                   "</b>. " + fr(1, 2) + " is the theoretical probability. " + fr(23, 27) + " compares heads with tails.",
                   ans=F(23, 50)))
    its.append(mcq(fig(freq_svg("20 spins", "Colour", ["red", "blue"], [12, 8], tally=False,
                                label="frequency table 20 spins")) +
                   "Priya’s class recorded 20 spins. What is the experimental probability of red, as a decimal?", "0.6",
                   ["0.12", "1.5", "0.4"],
                   "Red came up 12 times in 20 spins: " + fr(12, 20) + " = " + fr(6, 10) + " = <b>0.6</b>. "
                   "1.5 comes from 12 ÷ 8 (red ÷ blue), and it is greater than 1.", ans=F(12, 20)))
    vals = [18, 12, 10]
    assert sum(vals) == 40
    its.append(mcq(fig(freq_svg("40 spins", "Colour", ["red", "blue", "yellow"], vals, tally=False,
                                label="frequency table 40 spins")) +
                   "What is the experimental probability of yellow, as a percent?", "25%", ["10%", "40%", "30%"],
                   "Yellow came up 10 times in 40 spins: " + fr(10, 40) + " = " + fr(1, 4) + " = <b>25%</b>. "
                   "10% uses the count as the percent.", ans=F(10, 40)))
    its.append(mcq("Before each ringette game, a coin is tossed to decide which team starts. Tails has come up "
                   "5 games in a row. What is the probability of heads at the next game?",
                   fr(1, 2), [fr(5, 6), fr(1, 6), "1"],
                   "The coin has no memory. Every toss is a new trial, so heads is still <b>" + fr(1, 2) + "</b>. "
                   "Thinking heads is “due” is called the gambler’s fallacy.", ans=F(1, 2)))
    its.append(mcq("Kai has rolled a number cube 12 times without getting a 6. What is the probability of a 6 "
                   "on the next roll?", fr(1, 6), ["1", fr(2, 6), fr(1, 12)],
                   "The number cube does not remember earlier rolls. A 6 is still <b>" + fr(1, 6) + "</b>. "
                   "It is not certain (1), even after a long wait.", ans=F(1, 6)))
    its.append(mcq("Ava tosses a coin 10 times and gets 7 heads. Noah tosses a coin 1000 times and gets 508 heads. "
                   "Whose experimental probability of heads is closer to " + fr(1, 2) + "?",
                   "Noah’s", ["Ava’s", "They are equally close", "Neither is close"],
                   "Ava: " + fr(7, 10) + " = 0.7. Noah: " + fr(508, 1000) + " = 0.508. 0.508 is much closer to 0.5, "
                   "so <b>Noah’s</b> is closer."))
    assert abs(F(508, 1000) - F(1, 2)) < abs(F(7, 10) - F(1, 2))
    its.append(mcq("Why are Noah’s results (1000 tosses) closer to " + fr(1, 2) + " than Ava’s (10 tosses)?",
                   "More trials usually get closer to the theory",
                   ["Noah tossed the coin more carefully", "Ava’s coin must be unfair",
                    "Big experiments are always exactly right"],
                   "With only a few trials, luck changes the results a lot. <b>More trials usually get closer</b> "
                   "to the theoretical probability, but not exactly."))
    vals = [9, 11, 10, 8, 12, 10]
    assert sum(vals) == 60
    its.append(mcq(fig(freq_svg("A number cube rolled 60 times", "Number", ["1", "2", "3", "4", "5", "6"], vals,
                                tally=False, label="frequency table number cube")) +
                   "How do these results compare with the theory?",
                   "Close: each number should come up about 10 times",
                   ["The number cube must be unfair", "5 is the most likely number", "4 will come up more next time"],
                   "Theory: " + fr(1, 6) + " of 60 = 10 for each number. The results are all between 8 and 12, which is "
                   "<b>close to the theory</b>. Small differences are normal."))
    its.append(mcq("Leah rolls a number cube 600 times and gets a 6 on 104 rolls. How does this compare with the theory?",
                   "Close: theory says about 100", ["Far off: theory says about 6", "Far off: theory says about 300",
                                                    "Exactly right: theory says 104"],
                   fr(1, 6) + " of 600 = 600 ÷ 6 = 100. 104 is <b>close to 100</b>. Experiments are rarely exactly "
                   "the same as the theory."))
    assert F(600, 6) == 100
    its.append(mcq("A computer simulates tossing a coin 10" + NB + "000 times. About how many heads would you expect?",
                   "about 5000", ["exactly 5000", "about 1000", "about 50"],
                   "Half of 10" + NB + "000 is 5000. A simulation with many trials gets close to the theory, so expect "
                   "<b>about 5000</b>, not exactly 5000."))
    its.append(mcq("Zoe and Mateo toss a coin and spin a spinner with 3 equal sections (red, blue, yellow) 60 times. "
                   "They get heads and red 13 times. How does this compare with the theory?",
                   "Close: theory says about 10",
                   ["Far off: theory says about 30", "Far off: theory says about 12", "Exactly right: theory says 13"],
                   "Heads and red is 1 of 2 × 3 = 6 outcomes. " + fr(1, 6) + " of 60 = 10, and 13 is <b>close to 10</b>. "
                   "About 12 comes from 60 ÷ 5 (adding 2 + 3 outcomes)."))
    assert F(60, 6) == 10 and F(60, 5) == 12
    its.append(mcq("At hockey practice, Maya’s experimental probability of scoring is 0.32 after 25 shots. "
                   "How many goals did she score?", "8", ["32", "17", "3"],
                   "0.32 × 25 = <b>8</b>. Check: " + fr(8, 25) + " = " + fr(32, 100) + " = 0.32. "
                   "32 would need 100 shots.", ans=8))
    assert F("0.32") * 25 == 8
    its.append(mcq("Ethan counts 40 cars passing the school. 14 of them are white. Estimate the probability that "
                   "the next car is white.", "0.35", ["0.14", "0.65", "0.4"],
                   "14 ÷ 40 = " + fr(35, 100) + " = <b>0.35</b>. 0.65 is the estimate for a car that is NOT white.",
                   ans=F(14, 40)))
    its.append(mcq("A bag has 20 marbles. Sofia takes one, records its colour and puts it back. She does this 100 times "
                   "and gets red 26 times. About how many red marbles are in the bag?", "about 5",
                   ["about 26", "about 10", "about 15"],
                   "Red came up " + fr(26, 100) + " = 0.26 of the time, about a quarter. " + fr(1, 4) +
                   " of 20 is 5, so there are <b>about 5</b> red marbles. 26 is more than the whole bag."))
    assert round(F(26, 100) * 20) == 5
    its.append(mcq("Three groups spin the same spinner 20 times each. Red comes up 9, 13 and 8 times. "
                   "Use all the results to estimate the probability of red.", fr(30, 60),
                   [fr(9, 20), fr(13, 20), fr(30, 20)],
                   "Add the results: 9 + 13 + 8 = 30 reds in 3 × 20 = 60 spins. <b>" + fr(30, 60) + "</b> (= " + fr(1, 2) +
                   "). Using all 60 spins gives a better estimate than one group. " + fr(30, 20) + " is greater than 1.",
                   ans=F(1, 2)))
    assert 9 + 13 + 8 == 30
    its.append(mcq("A spinner has 4 equal sections: red, blue, yellow and green. At the fall fair, red comes up 98 times "
                   "in 200 spins. What do the results suggest?", "The spinner is probably not fair",
                   ["The spinner is fair", "Red will stop coming up soon", "200 spins are too few to tell"],
                   "Theory: " + fr(1, 4) + " of 200 = 50 reds. 98 is almost double that, after many spins, so "
                   "<b>the spinner is probably not fair</b>."))
    assert F(1, 4) * 200 == 50
    assert F(3, 10) > F(7, 25)
    its.append(mcq("At the school fun fair, Box A has 10 tickets and 3 of them win. Box B has 25 tickets and 7 of them win. "
                   "Which box gives a better chance of winning?", "Box A",
                   ["Box B, it has more winning tickets", "They are the same", "You can’t tell"],
                   "Box A: " + fr(3, 10) + " = 30%. Box B: " + fr(7, 25) + " = " + fr(28, 100) + " = 28%. "
                   "<b>Box A</b> is better, even though Box B has more winning tickets."))
    return {"title": "Experimental and theoretical probability: predictions and decisions", "items": its}


# ============================================================ lesson
def body_html():
    line = scale_svg(4, [], [(F(0), "0"), (F(1, 4), "0.25"), (F(1, 2), "0.5"), (F(3, 4), "0.75"), (F(1), "1")],
                     words=True, label="probability line from impossible to certain")
    bag = bag_svg([("red", 3), ("blue", 5)], label="bag of 3 red and 5 blue marbles")
    return (
        "<h2>The probability line</h2>"
        "<p>A probability is a number from <b>0</b> to <b>1</b>. 0 means impossible. 1 means certain. "
        "Halfway, " + fr(1, 2) + " or 0.5, means equally likely to happen or not. A probability is never more than 1.</p>"
        "<figure class='sn-fig'>" + line +
        "<figcaption>Every probability has a place on this line.</figcaption></figure>"
        "<p>The same probability can be written as a fraction, a decimal or a percent. "
        "As a percent, the line goes from 0% to 100%.</p>"
        + table(["Fraction", "Decimal", "Percent", "Chance"], [
            ["0", "0", "0%", "impossible"],
            [fr(1, 4), "0.25", "25%", "unlikely"],
            [fr(1, 2), "0.5", "50%", "equally likely"],
            [fr(3, 4), "0.75", "75%", "likely"],
            ["1", "1", "100%", "certain"],
        ])
        + "<h2>Working out a probability</h2>"
        "<p>When the outcomes are equally likely:</p>"
        "<p><b>probability = number of outcomes you want ÷ total number of outcomes</b></p>"
        "<figure class='sn-fig'>" + bag +
        "<figcaption>3 red and 5 blue marbles: 8 marbles in total.</figcaption></figure>"
        + ex("Example 1", "What is the probability of taking a red marble from this bag?",
             "There are 3 red marbles and 8 marbles altogether. Compare with all 8, not with the 5 blue.",
             fr(3, 8) + " = 0.375 = 37.5%")
        + "<h2>Two independent events</h2>"
        "<p>Two events are <b>independent</b> when one does not change the chance of the other, like tossing a coin "
        "and spinning a spinner. List every outcome in a tree diagram or a table. "
        "The number of outcomes is found by <b>multiplying</b>: 2 coin faces × 3 colours = 6 outcomes.</p>"
        "<figure class='sn-fig'>" + TREE3() +
        "<figcaption>Each coin face goes with each of the 3 colours: 6 equally likely outcomes.</figcaption></figure>"
        + ex("Example 2", "You toss a coin and spin the spinner (red, blue, yellow, all equal). "
             "What is the probability of tails and blue?",
             "The tree has 6 outcomes. Only one of them is T, blue.", fr(1, 6))
        + "<figure class='sn-fig'>" + TABLE12() +
        "<figcaption>A coin and a number cube: 2 × 6 = 12 outcomes.</figcaption></figure>"
        + ex("Example 3", "What is the probability of heads and an even number?",
             "Find H2, H4 and H6 in the table: 3 of the 12 outcomes.", fr(3, 12) + " = " + fr(1, 4) + " = 25%")
        + "<h2>Theoretical and experimental probability</h2>"
        "<p>The <b>theoretical</b> probability is what should happen, found by counting outcomes. "
        "The <b>experimental</b> probability is what did happen: number of times it happened ÷ number of trials. "
        "They are usually close, but rarely exactly the same. <b>More trials usually get closer.</b></p>"
        + table(["Coin tosses", "Heads", "Experimental probability"], [
            ["10", "7", fr(7, 10) + " = 0.7"],
            ["100", "46", fr(46, 100) + " = 0.46"],
            ["1000", "508", fr(508, 1000) + " = 0.508"],
        ])
        + ex("Example 4", "You roll a number cube 60 times. About how many 6s would you expect?",
             "A 6 has probability " + fr(1, 6) + ". " + fr(1, 6) + " of 60 is 60 ÷ 6 = 10.", "about 10")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“The probability is 1.2.”", "Probabilities are never more than 1 (100%)."],
            ["3 red, 5 blue, so P(red) = " + fr(3, 5) + ".", "Divide by ALL the outcomes: " + fr(3, 8) + "."],
            ["A coin and a number cube give 2 + 6 = 8 outcomes.", "Multiply: 2 × 6 = 12 outcomes."],
            ["“5 tails in a row, so heads is due.”", "A coin has no memory. Heads is still " + fr(1, 2) + "."],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about probability in the Ontario math curriculum?",
     "a": "In Grade 6 (Data, D2), students write probabilities as fractions, decimals and percents, place them on a probability line from 0 to 1, and use them to make predictions and decisions. They also find and compare the theoretical and experimental probabilities of two independent events, such as tossing a coin and spinning a spinner."},
    {"q": "What are independent events?",
     "a": "Two events are independent when one does not change the chance of the other. Tossing a coin and rolling a number cube are independent: getting heads does not make a 6 more or less likely."},
    {"q": "How do you find the probability of two independent events in Grade 6?",
     "a": "List every outcome in a tree diagram or a table, then count. A coin and a number cube give 2 × 6 = 12 equally likely outcomes, so heads and a 6 has a probability of 1/12."},
    {"q": "What is the difference between theoretical and experimental probability?",
     "a": "Theoretical probability is what should happen, found by counting outcomes. Experimental probability is what actually happened in trials, such as 23 heads in 50 tosses (23/50). With more trials, the two usually get closer."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (probability lines, rows of spinners, tables, tree diagrams)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(36818)
    sets = [set_line(), set_fdp(), set_find(), set_two_events(), set_experiments()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "probability", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Probability: Probability Lines, Fractions, Decimals, Percents and Two Independent Events",
        "seo_title": "Grade 6 Probability Worksheets: Probability Line, Tree Diagrams and Experiments (Free, Answer Key)",
        "short_title": "Probability",
        "domain": "Data",
        "standard_code": "Grade 6: Data, D2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use fractions, decimals, and percents to express the probability of events happening, represent this probability on a probability line, and use it to make predictions and informed decisions; determine and compare the theoretical and experimental probabilities of two independent events happening",
        "meta_desc": "Free Grade 6 math worksheets on probability for the Ontario curriculum: the probability line from 0 to 1, probability as a fraction, decimal and percent, spinners, number cubes and bags, two independent events with tables and tree diagrams, and theoretical vs experimental probability. 100 questions with an answer key, good EQAO practice.",
        "key_big": "A probability is a number from 0 (impossible) to 1 (certain): the outcomes you want ÷ all the outcomes.",
        "key_sub": "1/4 = 0.25 = 25%. A coin and a number cube give 2 × 6 = 12 outcomes, not 2 + 6. More trials get closer to the theory, and a coin has no memory: after 5 tails, heads is still 1/2.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(probability line|four spinners|frequency table|tree diagram|outcome table|two spinners)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
