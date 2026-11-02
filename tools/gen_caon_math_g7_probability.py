# -*- coding: utf-8 -*-
"""
Ontario Grade 7 Math: Probability of Independent and Dependent Events
(Ontario Curriculum 2020, Grade 7: Data, D2.1 and D2.2)
  python3 tools/gen_caon_math_g7_probability.py
Telling independent and dependent events apart (with and without replacement), sample spaces with tables and tree
diagrams (including draws without replacement), the probability of two independent events, the probability of two
dependent events (multiply along the branches of a probability tree), and comparing theoretical and experimental
probability, with word problems in Ontario contexts (fun fair, field trips in Toronto, hockey, Terry Fox Run).
Wrong answers come from real student mistakes: adding the probabilities, adding the outcomes instead of multiplying,
forgetting that the first item was not put back (3/5 x 3/5 instead of 3/5 x 2/4), lowering the number of the colour
but not the total (2/5 instead of 2/4), adding tops and bottoms, ignoring order, using the theory as the result,
and the gambler's fallacy.
Helpers are adapted from gen_cabc_math_g7_probability.py. Every answer is checked in code with fractions.Fraction.
Canadian English. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
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




def tree_svg(first, second, label="tree diagram", h1="Coin", h2="Spinner"):
    """Tree diagram. second is a list (same for every first outcome) or a dict first -> list (dependent events)."""
    sec = second if isinstance(second, dict) else {a: second for a in first}
    gap = 24
    top = 34
    rows = sum(len(sec[a]) for a in first)
    H = top + rows * gap + 4
    w1 = max(tw(a, 17) for a in first)
    xr, xa = 14, 100
    xb = int(xa + w1 / 2 + 70)
    w2 = max(tw(b, 15) for a in first for b in sec[a])
    xo = int(max(xb + 4 + w2 + 26, xb + 4 + tw(h2, 15) + 16))
    s = [text(xa, 18, h1, 15), text(xb + 4, 18, h2, 15, anchor="start"), text(xo, 18, "Outcome", 15, anchor="start")]
    ry = top + rows * gap / 2
    s.append("<circle cx='%d' cy='%.1f' r='4' fill='%s'/>" % (xr, ry, LINE))
    r0 = 0
    for a in first:
        k = len(sec[a])
        ay = top + (r0 + k / 2) * gap
        s.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xr, ry, xa - w1 / 2 - 6, ay, THIN))
        s.append(text(xa, ay + 6, a, 17, col=GREEN))
        for j, b in enumerate(sec[a]):
            by = top + (r0 + j + 0.5) * gap
            s.append("<line x1='%.1f' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (xa + w1 / 2 + 6, ay, xb - 2, by, THIN))
            s.append(text(xb + 4, by + 5, b, 15, anchor="start"))
            s.append(text(xo, by + 5, a + ", " + b, 15, anchor="start", weight=400))
        r0 += k
    W = int(max(xo + max(tw(a + ", " + b, 15, False) for a in first for b in sec[a]) + 10,
                xo + tw("Outcome", 15) + 8))
    return svg_wrap(W, int(H), "".join(s), label)


def ptree_svg(first, second, label="probability tree", h1="First draw", h2="Second draw"):
    """Probability tree for two draws. first: [(name, 'p')]; second: {name: [(name2, 'p')]}.
    Each branch is a slant then a short flat part; the probability sits above the flat part."""
    fs = 15
    gap = 34
    top = 40
    rows = sum(len(second[a]) for a, _ in first)
    H = top + rows * gap + 2
    xr = 10
    x1a, x1b = 54, 112          # first branch: slant to x1a, flat to x1b
    xa = 118                    # first label (start)
    w1 = max(tw(a, 16) for a, _ in first)
    x2s = xa + w1 + 6           # second branch starts
    x2a, x2b = x2s + 40, x2s + 98
    xb = x2b + 6
    w2 = max(tw(b, fs) for a, _ in first for b, _ in second[a])
    xo = max(xb + w2 + 22, xb + w2 / 2 + tw(h2, fs) / 2 + 16)
    assert (xa + w1 / 2) + tw(h1, fs) / 2 + 12 < xb + w2 / 2 - tw(h2, fs) / 2, (h1, h2)
    s = [text((xa + w1 / 2), 18, h1, fs), text(xb + w2 / 2, 18, h2, fs), text(xo, 18, "Outcome", fs, anchor="start")]
    ry = top + rows * gap / 2
    s.append("<circle cx='%d' cy='%.1f' r='4' fill='%s'/>" % (xr, ry, LINE))
    r0 = 0
    for a, pa in first:
        k = len(second[a])
        ay = top + (r0 + k / 2) * gap
        s.append("<polyline points='%d,%.1f %d,%.1f %d,%.1f' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xr, ry, x1a, ay, x1b, ay, THIN))
        s.append(text((x1a + x1b) / 2, ay - 6, pa, fs, col=GREEN))
        s.append(text(xa, ay + 6, a, 16, anchor="start"))
        for j, (b, pb) in enumerate(second[a]):
            by = top + (r0 + j + 0.5) * gap
            s.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x2s, ay, x2a, by, x2b, by, THIN))
            s.append(text((x2a + x2b) / 2, by - 6, pb, fs, col=GREEN))
            s.append(text(xb, by + 5, b, fs, anchor="start"))
            s.append(text(xo, by + 5, a + ", " + b, fs, anchor="start", weight=400))
        r0 += k
    W = int(max(xo + max(tw(a + ", " + b, fs, False) for a, _ in first for b, _ in second[a]) + 8,
                xo + tw("Outcome", fs) + 8))
    return svg_wrap(W, int(H), "".join(s), label)


def cards_table_svg(n, replace=False, label="outcome table for two cards"):
    """Two cards drawn from cards 1..n. Without replacement the same-card cells are grey with a dash."""
    c, fs = 46, 15
    x0, y0 = 30, 26
    W = x0 + (n + 1) * c + 6
    s = [text(x0 + c + n * c / 2, 17, "Second card", fs)]
    mid = y0 + c + n * c / 2
    s.append("<text x='16' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle' "
             "transform='rotate(-90 16 %.1f)'>First card</text>" % (mid, LINE, mid))
    for r in range(n + 1):
        for k in range(n + 1):
            x, y = x0 + k * c, y0 + r * c
            hd = r == 0 or k == 0
            same = r == k and r > 0 and not replace
            fill = HEAD if hd else ("#d4d4d4" if same else "#ffffff")
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, c, c, fill, GREEN))
            if r == 0 and k == 0:
                continue
            if r == 0:
                t = str(k)
            elif k == 0:
                t = str(r)
            elif same:
                t = "—"
            else:
                t = "%d, %d" % (r, k)
            s.append(text(x + c / 2, y + c / 2 + 5, t, fs, weight=700 if hd else 400))
    H = y0 + (n + 1) * c + 4
    return svg_wrap(int(W), int(H), "".join(s), label)


def cards_svg(labels, label="cards"):
    """A row of face-up cards."""
    cw, ch, gap = 40, 54, 10
    W = len(labels) * (cw + gap) + gap
    s = []
    for i, t in enumerate(labels):
        x = gap + i * (cw + gap)
        s.append("<rect x='%d' y='4' width='%d' height='%d' rx='5' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x, cw, ch, LINE))
        s.append(text(x + cw / 2, 4 + ch / 2 + 8, t, 22))
    return svg_wrap(int(W), ch + 8, "".join(s), label)


CUBE = [str(k) for k in range(1, 7)]
A2 = [("red", F(1, 2), "red"), ("blue", F(1, 2), "blue")]
B4 = [(str(k), F(1, 4), NUMFILL[k - 1]) for k in range(1, 5)]
RED34 = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]


def TABLE12():
    return fig(outcome_table_svg(["heads", "tails"], CUBE, "Number cube", label="outcome table coin and number cube"))


def TREE3():
    return fig(tree_svg(["H", "T"], ["red", "blue", "yellow"], label="tree diagram coin then spinner red blue yellow"))


def TWO():
    return fig(spinners_row_svg([A2, B4], ["Spinner A", "Spinner B"], label="two spinners A and B"))


def SUMS():
    return fig(sums_svg())


def BAG():
    return fig(bag_svg([("red", 3), ("blue", 2)], label="bag of 3 red and 2 blue marbles"))


def CARDS4():
    return fig(cards_table_svg(4, label="outcome table two cards 1 to 4 without replacement"))


def ABC_DEP():
    return fig(tree_svg(["A", "B", "C"], {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]},
                        label="tree diagram two cards A B C without replacement", h1="First card", h2="Second card"))


def ABC_IND():
    return fig(tree_svg(["A", "B", "C"], ["A", "B", "C"],
                        label="tree diagram two cards A B C with replacement", h1="First card", h2="Second card"))


GY = [("green", "4/6"), ("yellow", "2/6")]
GY2 = {"green": [("green", "3/5"), ("yellow", "2/5")], "yellow": [("green", "4/5"), ("yellow", "1/5")]}


def PTREE(hide=None):
    sec = {a: [(b, "?" if (a, b) == hide else p) for b, p in GY2[a]] for a in GY2}
    return fig(ptree_svg(GY, sec, label="probability tree two marbles without replacement"))


def outcomes(a, b):
    return [(x, y) for x in a for y in b]


def dep(items):
    """Ordered pairs of two different items (drawn without replacement). items may repeat colours: use indexes."""
    return [(items[i], items[j]) for i in range(len(items)) for j in range(len(items)) if i != j]


O12 = outcomes("HT", range(1, 7))
O6 = outcomes("HT", ["red", "blue", "yellow"])
O8 = outcomes(["red", "blue"], range(1, 5))
O4 = outcomes("HT", "HT")
O36 = outcomes(range(1, 7), range(1, 7))
O9 = outcomes(["red", "blue", "yellow"], ["red", "blue", "yellow"])
M32 = ["red"] * 3 + ["blue"] * 2
D32 = dep(M32)                                  # 20 equally likely ordered draws
R32 = outcomes(M32, M32)                        # 25 with replacement
C4 = dep([1, 2, 3, 4])                          # 12
M42 = ["green"] * 4 + ["yellow"] * 2
D42 = dep(M42)                                  # 30


def P(space, cond):
    return F(sum(1 for o in space if cond(*o)), len(space))


def cnt(space, cond):
    return sum(1 for o in space if cond(*o))


# ============================================================ set 1: independent or dependent?
IND = "Independent: the first result does not change the chances for the second"
DEP = "Dependent: the first result changes the chances for the second"
W_WANT = "Dependent: you want both events to happen"
W_RAND = "Independent: each result is random"
W_TIME = "Independent: the two events happen one after the other"


def W_SAME(x):
    return "Dependent: the same %s is used both times" % x


def set_kind():
    its = []
    its.append(mcq("You roll a number cube, then roll the same number cube again. Are the two rolls independent or "
                   "dependent?", IND, [DEP, W_SAME("number cube"), W_TIME],
                   "The cube does not remember the first roll. Every number is still " + fr(1, 6) + " on the second roll, "
                   "so the rolls are <b>independent</b>. Using the same cube does not make them dependent, and "
                   "“one after the other” is not the reason."))
    its.append(mcq("You toss a coin and spin a spinner. Are the two events independent or dependent?", IND,
                   [DEP, W_RAND, "Dependent: the coin and the spinner are used together"],
                   "The coin cannot change where the spinner stops, so the events are <b>independent</b>. "
                   "Being random is not the reason: random draws can still be dependent."))
    its.append(mcq("You take a marble from a bag and keep it. Then you take a second marble from the same bag. "
                   "Are the two draws independent or dependent?", DEP, [IND, W_RAND, W_WANT],
                   "The first marble is not put back, so the bag has one less marble and one less of that colour. "
                   "The chances for the second draw change: the draws are <b>dependent</b>. Wanting both events "
                   "does not decide it."))
    its.append(mcq("You pick a card from 10 cards, put it back, shuffle, and pick again. Are the two picks independent "
                   "or dependent?", IND, [DEP, W_SAME("set of cards"), W_TIME],
                   "The card goes back, so the second pick has the same 10 cards as the first. "
                   "The picks are <b>independent</b> because nothing is taken away, not because they happen one after "
                   "the other."))
    its.append(mcq("A teacher draws a name from a hat for line leader. The name is not put back. Then she draws a name "
                   "for door holder. Are the two draws independent or dependent?", DEP, [IND, W_TIME, W_WANT],
                   "The first student is out of the hat, so every other student now has a better chance on the "
                   "second draw. The draws are <b>dependent</b> because the name is kept out."))
    its.append(mcq("Two raffle tickets are drawn at the school fun fair, one for first prize and one for second prize. "
                   "The first ticket is not put back. Are the two draws independent or dependent?", DEP,
                   [IND, "Independent: there are many tickets", W_WANT],
                   "The winning ticket is not put back, so there is one less ticket for the second draw. "
                   "The draws are <b>dependent</b>. Even with many tickets, the chances change a little."))
    its.append(mcq("Olivia guesses the answer to a true-or-false question. Then she guesses the answer to a different "
                   "true-or-false question. Are the two guesses independent or dependent?", IND,
                   [DEP, W_RAND, "Dependent: both questions are on the same test"],
                   "Each guess has a " + fr(1, 2) + " chance of being right, whatever happened on the first one. "
                   "The guesses are <b>independent</b> because the first guess does not change the second."))
    its.append(mcq("A box has 8 granola bars of 2 kinds. Emma takes one and eats it. Then Liam takes one from the same box. "
                   "Are the two picks independent or dependent?", DEP, [IND, W_RAND, W_WANT],
                   "Emma’s bar is gone, so Liam picks from 7 bars, and one kind has one less bar. "
                   "The picks are <b>dependent</b>, even though each pick is random."))
    its.append(mcq("You spin a spinner, then spin the same spinner again. Are the two spins independent or dependent?",
                   IND, [DEP, W_SAME("spinner"), W_RAND],
                   "The spinner looks the same before every spin, so the first spin does not change the second. "
                   "The spins are <b>independent</b>. Random results can still be dependent, so that is not the reason."))
    its.append(mcq("Which pair of events is dependent?", "Picking two different students for two jobs",
                   ["Tossing a coin twice", "Rolling two number cubes", "Spinning a spinner and tossing a coin"],
                   "Once a student has the first job, that student can’t be picked again, so the chances change. "
                   "<b>Picking two different students for two jobs</b> is dependent. The others are independent."))
    its.append(mcq("Which pair of events is independent?", "Drawing a card, putting it back, then drawing again",
                   ["Drawing two cards without putting the first back", "Picking a class president, then a vice-president",
                    "Eating a cookie from a jar, then taking another"],
                   "When the card goes back, the second draw is the same as the first. "
                   "<b>Drawing with replacement</b> gives independent events."))
    its.append(mcq("Which phrase means the first item is put back before the next draw?", "with replacement",
                   ["without replacement", "dependent", "sample space"],
                   "<b>With replacement</b> means the item goes back, so the draws are independent. "
                   "Without replacement means it stays out, so the draws are dependent."))
    its.append(mcq(BAG() + "This bag has 3 red and 2 blue marbles. You take out a red marble and keep it. "
                   "How many marbles are in the bag now?", "4", ["5", "3", "2"],
                   "5 − 1 = <b>4</b> marbles are left. 5 forgets that the red marble was not put back.", ans=4))
    its.append(mcq(BAG() + "You take out a red marble and keep it. How many red marbles are left in the bag?", "2",
                   ["3", "4", "1"],
                   "3 − 1 = <b>2</b> red marbles are left (with 2 blue). 4 is all the marbles left.", ans=2))
    its.append(mcq(BAG() + "You take out a red marble and put it back. What is the probability that the next marble "
                   "is red?", fr(3, 5), [fr(2, 4), fr(2, 5), fr(3, 4)],
                   "The marble went back, so the bag still has 3 red out of 5: <b>" + fr(3, 5) + "</b>. "
                   + fr(2, 4) + " would be right only if the red marble were kept.", ans=F(3, 5)))
    its.append(mcq(BAG() + "You take out a red marble and keep it. What happens to the chance of red on the next draw?",
                   "It goes down, from " + fr(3, 5) + " to " + fr(2, 4),
                   ["It stays the same, " + fr(3, 5), "It goes up, from " + fr(3, 5) + " to " + fr(3, 4),
                    "It goes down, from " + fr(3, 5) + " to " + fr(2, 5)],
                   "Now there are 2 red out of 4 marbles. " + fr(3, 5) + " = 0.6 and " + fr(2, 4) + " = 0.5, so the chance "
                   "<b>goes down</b>. " + fr(2, 5) + " takes a red away but forgets that the total went down too."))
    assert F(3, 5) > F(2, 4)
    its.append(mcq("A bag has 4 green and 2 yellow marbles. You draw one marble, keep it, and draw another. "
                   "How can you change the experiment so the two draws are independent?",
                   "Put the first marble back before the second draw",
                   ["Draw the two marbles faster", "Take both marbles out at the same time",
                    "Use your other hand for the second draw"],
                   "<b>Putting the first marble back</b> makes the bag the same for both draws. Taking both at the "
                   "same time is the same as drawing without replacement: still dependent."))
    its.append(mcq("Zoe has 6 cards numbered 1 to 6. She draws the 6 and does not put it back. What is the probability "
                   "that her next card is the 6?", "0", [fr(1, 6), fr(1, 5), fr(1, 36)],
                   "The 6 is no longer in the pile, so drawing it again is impossible: <b>0</b>. "
                   + fr(1, 6) + " would be right if the card were put back.", ans=0))
    its.append(mcq("Maya tosses a coin 4 times and gets heads every time. What is the probability of heads on the next "
                   "toss?", fr(1, 2), [fr(1, 32), fr(1, 5), fr(1, 4)],
                   "Coin tosses are independent: the coin has no memory. Heads is still <b>" + fr(1, 2) + "</b>. "
                   + fr(1, 32) + " is the chance of 5 heads in a row before you start, not the chance of the next toss.",
                   ans=F(1, 2)))
    its.append(mcq("Liam says, “Rolling a number cube twice is dependent because I use the same cube.” Is he right?",
                   "No: the cube is the same before each roll, so the rolls are independent",
                   ["Yes: the same cube makes the rolls dependent", "Yes: the second roll depends on the first",
                    "No: the rolls are dependent only if the numbers match"],
                   "Dependent means the first result <b>changes the chances</b> of the second. Nothing is taken away "
                   "from a number cube, so every number is still " + fr(1, 6) + "."))
    order = [0, 1, 2, 3, 8, 6, 4, 7, 5, 11, 9, 10, 12, 13, 14, 15, 17, 18, 16, 19]
    its = [its[i] for i in order]
    assert len(its) == 20
    return {"title": "Independent or dependent events?", "items": its}


# ============================================================ set 2: sample spaces
def set_sample_spaces():
    its = []
    its.append(mcq("You toss a coin and spin a spinner with 2 equal sections, red and blue. Which list shows all the "
                   "outcomes? (H = heads, T = tails, R = red, B = blue)", "HR, HB, TR, TB",
                   ["H, T, R, B", "HR, TB", "HR, HB, TR, TB, HT"],
                   "Pair each side of the coin with each colour: 2 × 2 = 4 outcomes, <b>HR, HB, TR, TB</b>. "
                   "H, T, R, B lists single results, not pairs."))
    its.append(mcq(TREE3() + "How many outcomes does the tree diagram show?", "6", ["5", "3", "2"],
                   "Each of the 2 coin branches splits into 3 colours: 2 × 3 = <b>6</b>. 5 comes from adding 2 + 3.",
                   ans=len(O6)))
    its.append(mcq(TREE3() + "Which outcome is NOT in the sample space?", "T, green", ["H, red", "T, blue", "H, yellow"],
                   "The spinner has only red, blue and yellow, so <b>T, green</b> can’t happen."))
    assert ("T", "green") not in O6
    its.append(mcq("You toss a coin and roll a number cube with the numbers 1 to 6. How many outcomes are there?", "12",
                   ["8", "6", "36"],
                   "Each side of the coin goes with each of the 6 numbers: 2 × 6 = <b>12</b>. 8 comes from adding 2 + 6.",
                   ans=len(O12)))
    n = cnt(O12, lambda c, k: c == "T" and k > 4)
    its.append(mcq(TABLE12() + "How many outcomes show tails and a number greater than 4?", "2", ["6", "1", "3"],
                   "Tails with 5 or 6: T5 and T6, so <b>2</b> outcomes. 3 counts the 4 as well, but 4 is not greater "
                   "than 4.", ans=n))
    its.append(mcq("You roll two number cubes, each numbered 1 to 6. How many outcomes are there?", "36",
                   ["12", "11", "30"],
                   "6 × 6 = <b>36</b>. 12 comes from adding 6 + 6. 11 is the number of different sums (2 to 12). "
                   "30 = 6 × 5 would be right only if the second cube could not repeat the first number.", ans=len(O36)))
    n = cnt(O36, lambda a, b: a + b == 8)
    assert n == 5
    its.append(mcq(SUMS() + "The table shows the sum for every outcome of rolling two number cubes. How many outcomes "
                   "give a sum of 8?", "5", ["3", "6", "8"],
                   "2 + 6, 3 + 5, 4 + 4, 5 + 3 and 6 + 2: <b>5</b> outcomes. 3 forgets that 2 + 6 and 6 + 2 are "
                   "different outcomes.", ans=n))
    its.append(mcq(ABC_IND() + "Three cards say A, B and C. You draw a card, put it back, and draw again. "
                   "How many outcomes are there?", "9", ["6", "3", "27"],
                   "The card goes back, so each of the 3 first cards goes with all 3 second cards: 3 × 3 = <b>9</b>. "
                   "6 would be right without replacement.", ans=9))
    its.append(mcq(ABC_DEP() + "This time you draw a card and keep it, then draw a second card. "
                   "How many outcomes are there?", "6", ["9", "3", "5"],
                   "The first card is not put back, so only 2 cards are left for the second draw: 3 × 2 = <b>6</b>. "
                   "9 forgets that the first card is gone. 3 forgets that AB and BA are different orders.",
                   ans=len(dep("ABC"))))
    its.append(mcq("You draw two cards from A, B and C without replacement. Which list shows the whole sample space?",
                   "AB, AC, BA, BC, CA, CB", ["AA, AB, AC, BA, BB, BC, CA, CB, CC", "AB, AC, BC", "AB, BC, CA"],
                   "The first card is kept, so AA, BB and CC are impossible. Order matters: AB (A first) is not BA. "
                   "That gives <b>AB, AC, BA, BC, CA, CB</b>."))
    assert len(dep("ABC")) == 6
    its.append(mcq(CARDS4() + "Four cards are numbered 1 to 4. You draw two cards without replacement. "
                   "How many outcomes are there?", "12", ["16", "8", "6"],
                   "4 first cards × 3 cards left = <b>12</b>. The 4 grey cells can’t happen. "
                   "16 counts them. 6 forgets that order matters.", ans=len(C4)))
    its.append(mcq(CARDS4() + "Why are 4 cells in the table grey?", "The same card can’t be drawn twice",
                   ["Those outcomes are less likely", "Those cards are put back", "Those sums are too big"],
                   "The first card is kept, so “1, 1”, “2, 2”, “3, 3” and “4, 4” are impossible: "
                   "<b>the same card can’t be drawn twice</b>."))
    n = cnt(C4, lambda a, b: a + b == 6)
    assert n == 2
    its.append(mcq(CARDS4() + "How many outcomes have a sum of 6?", "2", ["3", "1", "6"],
                   "2, 4 and 4, 2: <b>2</b> outcomes. 3 also counts 3, 3, which is a grey cell: there is only one 3 card.",
                   ans=n))
    n = cnt(C4, lambda a, b: a > b)
    assert n == 6 and cnt(outcomes(range(1, 5), range(1, 5)), lambda a, b: a >= b) == 10
    its.append(mcq(CARDS4() + "How many outcomes have a first card greater than the second card?", "6", ["12", "3", "10"],
                   "2, 1; 3, 1; 3, 2; 4, 1; 4, 2; 4, 3: <b>6</b> outcomes, the cells below the grey ones. "
                   "10 also counts the grey cells.", ans=n))
    its.append(mcq("At a Mississauga school’s pizza lunch, each student gets 1 of 3 kinds of pizza and 1 of 4 drinks. "
                   "How many different pizza-and-drink lunches are possible?", "12", ["7", "4", "3"],
                   "Each pizza goes with each of the 4 drinks: 3 × 4 = <b>12</b>. 7 comes from adding 3 + 4.", ans=12))
    its.append(mcq("You toss a coin 3 times. How many outcomes are there?", "8", ["6", "3", "9"],
                   "2 × 2 × 2 = <b>8</b> (HHH, HHT, HTH, HTT, THH, THT, TTH, TTT). 6 comes from 2 × 3.",
                   ans=len(outcomes(O4, "HT"))))
    its.append(mcq("A Grade 7 class picks a president and then a vice-president from 5 students who are running. "
                   "One student can’t have both jobs. How many outcomes are there?", "20", ["25", "10", "9"],
                   "5 choices for president, then 4 students left for vice-president: 5 × 4 = <b>20</b>. "
                   "25 lets one student have both jobs. 10 forgets that the order (who gets which job) matters.",
                   ans=len(dep(range(5)))))
    its.append(mcq("A bag has 4 marbles: red, blue, yellow and green. You draw 2 marbles without replacement. "
                   "How many outcomes are there?", "12", ["16", "8", "6"],
                   "4 first marbles × 3 marbles left = <b>12</b>. 16 puts the first marble back. "
                   "6 forgets that red then blue is not the same as blue then red.", ans=len(dep(range(4)))))
    its.append(mcq("At the fun fair, 8 raffle tickets are left in a box. One ticket is drawn for first prize and is not "
                   "put back. Then one is drawn for second prize. How many outcomes are there?", "56",
                   ["64", "16", "15"],
                   "8 tickets for first prize, then 7 left: 8 × 7 = <b>56</b>. 64 = 8 × 8 puts the first ticket back. "
                   "15 comes from adding 8 + 7.", ans=len(dep(range(8)))))
    its.append(mcq("Ava says, “Drawing two cards from cards 1 to 4 without replacement gives 4 × 4 = 16 outcomes.” "
                   "What is wrong?", "The first card is kept, so there are 4 × 3 = 12",
                   ["Nothing, 4 × 4 = 16 is right", "There are 4 + 4 = 8 outcomes", "There are 4 + 3 = 7 outcomes"],
                   "Only 3 cards are left for the second draw: <b>4 × 3 = 12</b> outcomes. "
                   "Multiply, and use the number of items that are really left."))
    order = [0, 3, 1, 2, 4, 5, 6, 14, 15, 7, 8, 9, 10, 11, 12, 13, 17, 16, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20
    return {"title": "Sample spaces: tables and tree diagrams", "items": its}


# ============================================================ set 3: two independent events
def set_independent():
    its = []
    p = P(O12, lambda c, k: c == "H" and k == 6)
    assert p == F(1, 12)
    its.append(mcq(TABLE12() + "What is the probability of heads and a 6?", fr(1, 12), [fr(1, 8), fr(4, 6), fr(1, 6)],
                   "H6 is 1 of the 12 equally likely outcomes: <b>" + fr(1, 12) + "</b>. " + fr(4, 6) + " comes from "
                   "adding " + fr(1, 2) + " + " + fr(1, 6) + ". " + fr(1, 8) + " adds 2 + 6 outcomes.", ans=p))
    p = P(O12, lambda c, k: c == "T" and k % 2 == 0)
    its.append(mcq(TABLE12() + "What is the probability of tails and an even number?", fr(3, 12),
                   [fr(3, 8), fr(3, 6), fr(1, 12)],
                   "T2, T4 and T6: 3 of 12 outcomes, so <b>" + fr(3, 12) + "</b> (= " + fr(1, 4) + "). "
                   + fr(3, 6) + " looks only at the number cube.", ans=p))
    p = P(O4, lambda a, b: a == b == "H")
    its.append(mcq("You toss two coins. What is the probability of two heads?", fr(1, 4), [fr(1, 3), fr(1, 2), "1"],
                   "HH is 1 of the 4 outcomes (HH, HT, TH, TT): <b>" + fr(1, 4) + "</b>. Adding " + fr(1, 2) + " + "
                   + fr(1, 2) + " gives 1, which would mean certain. " + fr(1, 3) + " forgets that HT and TH are different.",
                   ans=p))
    p = P(O8, lambda c, k: c == "blue" and k == 4)
    its.append(mcq(TWO() + "You spin both spinners. What is the probability of blue and 4?", fr(1, 8),
                   [fr(3, 4), fr(1, 6), fr(1, 4)],
                   "Blue and 4 is 1 of the 2 × 4 = 8 outcomes: <b>" + fr(1, 8) + "</b>. " + fr(3, 4) + " adds "
                   + fr(1, 2) + " + " + fr(1, 4) + ". " + fr(1, 6) + " adds 2 + 4 outcomes.", ans=p))
    p = F(1, 2) * F(2, 6)
    assert p == P(O12, lambda c, k: c == "H" and k >= 5) == F(2, 12)
    its.append(mcq("For a coin and a number cube, P(heads) = " + fr(1, 2) + " and P(5 or 6) = " + fr(2, 6) +
                   ". What is P(heads and a 5 or 6)?", fr(2, 12), [fr(5, 6), fr(2, 8), fr(1, 12)],
                   "For independent events, multiply: " + fr(1, 2) + " × " + fr(2, 6) + " = <b>" + fr(2, 12) + "</b>. "
                   "Check: H5 and H6 are 2 of 12 outcomes. " + fr(5, 6) + " comes from adding.", ans=p))
    p = P(O36, lambda a, b: a == b == 6)
    its.append(mcq("You roll two number cubes. What is the probability of a 6 on both?", fr(1, 36),
                   [fr(1, 12), fr(2, 6), fr(1, 6)],
                   fr(1, 6) + " × " + fr(1, 6) + " = <b>" + fr(1, 36) + "</b>. " + fr(2, 6) + " adds " + fr(1, 6) +
                   " + " + fr(1, 6) + ". " + fr(1, 12) + " adds 6 + 6 outcomes.", ans=p))
    p = P(O36, lambda a, b: a + b == 7)
    its.append(mcq(SUMS() + "What is the probability that the sum is 7?", fr(6, 36), [fr(1, 36), fr(7, 36), fr(1, 11)],
                   "6 of the 36 cells show 7: <b>" + fr(6, 36) + "</b> (= " + fr(1, 6) + "). " + fr(1, 11) +
                   " treats the 11 sums as equally likely, but they are not.", ans=p))
    p = P(R32, lambda a, b: a == b == "red")
    assert p == F(9, 25)
    its.append(mcq(BAG() + "You draw a marble, put it back, and draw again. What is the probability of red both times?",
                   fr(9, 25), [fr(6, 20), fr(6, 10), fr(3, 25)],
                   "The marble goes back, so red is " + fr(3, 5) + " both times: " + fr(3, 5) + " × " + fr(3, 5) +
                   " = <b>" + fr(9, 25) + "</b>. " + fr(6, 20) + " would be right without replacement. " + fr(6, 10) +
                   " adds the tops and the bottoms. " + fr(3, 25) + " multiplies only the bottoms.", ans=p))
    p = P(R32, lambda a, b: a == b == "blue")
    its.append(mcq(BAG() + "You draw a marble, put it back, and draw again. What is the probability of blue both times?",
                   fr(4, 25), [fr(2, 20), fr(4, 10), fr(2, 25)],
                   fr(2, 5) + " × " + fr(2, 5) + " = <b>" + fr(4, 25) + "</b>. " + fr(2, 20) + " forgets that the marble "
                   "was put back. " + fr(4, 10) + " adds the tops and the bottoms. " + fr(2, 25) + " does not multiply the tops.", ans=p))
    p = P(R32, lambda a, b: a == "red" and b == "blue")
    its.append(mcq(BAG() + "You draw a marble, put it back, and draw again. What is the probability of red first, then "
                   "blue?", fr(6, 25), [fr(6, 20), fr(5, 10), fr(2, 5)],
                   fr(3, 5) + " × " + fr(2, 5) + " = <b>" + fr(6, 25) + "</b>. " + fr(6, 20) + " would be right without "
                   "replacement. " + fr(5, 10) + " adds the tops and the bottoms. " + fr(2, 5) + " is blue on its own.", ans=p))
    p = P(O9, lambda a, b: a == b == "red")
    its.append(mcq("A spinner has 3 equal sections: red, blue and yellow. You spin it twice. What is the probability of "
                   "red both times?", fr(1, 9), [fr(2, 3), fr(1, 6), fr(1, 3)],
                   fr(1, 3) + " × " + fr(1, 3) + " = <b>" + fr(1, 9) + "</b>. " + fr(2, 3) + " adds the probabilities. "
                   + fr(1, 6) + " adds 3 + 3 outcomes.", ans=p))
    p = P(O9, lambda a, b: a == b)
    its.append(mcq("You spin the same red, blue and yellow spinner twice. What is the probability that both spins land on "
                   "the same colour?", fr(3, 9), [fr(1, 9), fr(3, 6), fr(6, 9)],
                   "Red-red, blue-blue and yellow-yellow: 3 of 9 outcomes, <b>" + fr(3, 9) + "</b> (= " + fr(1, 3) + "). "
                   + fr(1, 9) + " counts only one colour. " + fr(6, 9) + " is the chance of different colours.", ans=p))
    p = 1 - P(O12, lambda c, k: c == "H" and k == 6)
    its.append(mcq("You toss a coin and roll a number cube. What is the probability of NOT getting heads and a 6?",
                   fr(11, 12), [fr(1, 12), fr(1, 2), fr(5, 6)],
                   "Heads and 6 is 1 of 12 outcomes, so the other <b>" + fr(11, 12) + "</b> are not. "
                   + fr(5, 6) + " is the chance of not rolling a 6 on its own.", ans=p))
    p = P(O4, lambda a, b: "H" in (a, b))
    its.append(mcq("You toss two coins. What is the probability of at least one head, as a percent?", "75%",
                   ["25%", "50%", "about 67%"],
                   "HH, HT and TH: 3 of 4 outcomes, " + fr(3, 4) + " = <b>75%</b>. About 67% (" + fr(2, 3) +
                   ") joins HT and TH into one outcome.", ans=p))
    p = P(outcomes("HT", ["red", "blue", "yellow", "green"]), lambda c, s: c == "T" and s == "blue")
    assert p == F(1, 8)
    its.append(mcq("You toss a coin and spin a spinner with 4 equal sections: red, blue, yellow and green. What is the "
                   "probability of tails and blue, as a decimal?", "0.125", ["0.75", "0.25", "0.18"],
                   "2 × 4 = 8 outcomes, so " + fr(1, 8) + " = 1 ÷ 8 = <b>0.125</b>. 0.75 adds 0.5 + 0.25. "
                   "0.18 just writes the digits 1 and 8.", ans=p))
    p = F(1, 2) * part(RED34, "red")
    assert p == F(3, 8) == P(outcomes("HT", ["red", "red", "red", "blue"]), lambda c, s: c == "H" and s == "red")
    its.append(mcq(fig(spinner_svg(RED34, R=56, label="spinner three quarters red one quarter blue")) +
                   "You toss a coin and spin this spinner. What is the probability of heads and red?", fr(3, 8),
                   [fr(1, 4), fr(5, 4), fr(3, 6)],
                   fr(1, 2) + " × " + fr(3, 4) + " = <b>" + fr(3, 8) + "</b>. " + fr(1, 4) + " treats red and blue as "
                   "equally likely. " + fr(5, 4) + " adds, and a probability can’t be more than 1.", ans=p))
    p = P(outcomes("HT", range(1, 6)), lambda c, k: c == "H" and k == 3)
    assert p == F(1, 10)
    its.append(mcq("You toss a coin and spin a spinner with 5 equal sections numbered 1 to 5. What is the probability of "
                   "heads and 3, as a percent?", "10%", ["70%", "20%", "50%"],
                   "2 × 5 = 10 outcomes, and H3 is one of them: " + fr(1, 10) + " = <b>10%</b>. 70% adds 50% + 20%. "
                   "20% is a 3 on its own.", ans=p))
    p = P(O36, lambda a, b: a % 2 == 0 and b % 2 == 0)
    assert p == F(9, 36)
    its.append(mcq("You roll two number cubes. What is the probability that both numbers are even?", fr(9, 36),
                   ["1", fr(3, 36), fr(3, 6)],
                   "3 even numbers × 3 even numbers = 9 outcomes out of 36: <b>" + fr(9, 36) + "</b> (= " + fr(1, 4) +
                   "). " + fr(3, 36) + " counts only 2-2, 4-4 and 6-6. Adding " + fr(1, 2) + " + " + fr(1, 2) +
                   " = 1 would mean certain.", ans=p))
    assert P(O4, lambda a, b: a == b == "H") > P(O12, lambda c, k: c == "H" and k == 1)
    its.append(mcq("Which is more likely: two heads when you toss two coins, or heads and a 1 when you toss a coin and "
                   "roll a number cube?", "Two heads with two coins", ["Heads and a 1", "They are equally likely",
                                                                      "You can’t tell"],
                   "Two heads: " + fr(1, 4) + ". Heads and a 1: " + fr(1, 12) + ". " + fr(1, 4) + " &gt; " + fr(1, 12) +
                   ", so <b>two heads</b> is more likely."))
    assert F(1, 2) * F(1, 5) == F(1, 10)
    its.append(mcq("A game uses a coin and a spinner with equal sections, one of them red. The probability of heads and "
                   "red is " + fr(1, 10) + ". How many sections does the spinner have?", "5", ["10", "8", "20"],
                   fr(1, 2) + " × " + fr(1, 5) + " = " + fr(1, 10) + ", so the spinner has <b>5</b> sections. "
                   "10 forgets the coin. 20 multiplies by 2 instead of dividing. 8 adds outcomes: 2 + 8 = 10.", ans=5))
    order = [0, 1, 2, 3, 4, 5, 6, 10, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20
    return {"title": "Probability of two independent events", "items": its}


# ============================================================ set 4: dependent events
def set_dependent():
    its = []
    p = P(D32, lambda a, b: b == "red" and a == "red") / P(D32, lambda a, b: a == "red")
    assert p == F(2, 4)
    its.append(mcq(BAG() + "You take out a red marble and keep it. What is the probability that the next marble is red?",
                   fr(2, 4), [fr(3, 5), fr(2, 5), fr(3, 4)],
                   "2 red are left out of 4 marbles: <b>" + fr(2, 4) + "</b>. " + fr(3, 5) + " forgets that the first "
                   "marble was not put back. " + fr(2, 5) + " takes away a red but keeps 5 marbles.", ans=p))
    p = P(D32, lambda a, b: a == b == "blue") / P(D32, lambda a, b: a == "blue")
    assert p == F(1, 4)
    its.append(mcq(BAG() + "You take out a blue marble and keep it. What is the probability that the next marble is blue?",
                   fr(1, 4), [fr(2, 5), fr(2, 4), fr(1, 5)],
                   "1 blue is left out of 4 marbles: <b>" + fr(1, 4) + "</b>. " + fr(2, 5) + " forgets that the blue "
                   "marble was kept. " + fr(1, 5) + " keeps 5 marbles in the bag.", ans=p))
    assert F(3, 7) < F(4, 7)
    its.append(mcq("A bag has 4 green and 4 yellow marbles. You take out a green marble and keep it. Which colour is now "
                   "more likely on the next draw?", "Yellow: " + fr(4, 7) + " beats " + fr(3, 7),
                   ["Green: " + fr(4, 7) + " beats " + fr(3, 7), "They are still equally likely: " + fr(4, 8),
                    "Green, because it just came out"],
                   "3 green and 4 yellow are left, out of 7. <b>Yellow</b> is now more likely, " + fr(4, 7) + " to "
                   + fr(3, 7) + ". Before the draw they were equally likely; keeping the marble changed that."))
    its.append(mcq(CARDS4() + "You draw the 4 and keep it. What is the probability that the second card is also the 4?",
                   "0", [fr(1, 4), fr(1, 3), fr(1, 16)],
                   "There is only one 4 card, and it is already out, so the probability is <b>0</b> (impossible). "
                   + fr(1, 4) + " would be right with replacement.", ans=0))
    its.append(mcq(PTREE() + "A bag has 4 green and 2 yellow marbles. You draw two marbles without replacement. "
                   "Why is the probability on the branch green → green " + fr(3, 5) + "?",
                   "After one green is taken, 3 green are left out of 5",
                   ["There are 3 green and 5 yellow marbles", "It is " + fr(4, 6) + " made simpler",
                    "It is " + fr(4, 6) + " − " + fr(1, 6)],
                   "The first green marble is kept, so the bag now has 3 green and 2 yellow: <b>3 green out of 5</b>. "
                   + fr(4, 6) + " = " + fr(2, 3) + ", not " + fr(3, 5) + "."))
    p = P(D42, lambda a, b: a == b == "yellow") / P(D42, lambda a, b: a == "yellow")
    assert p == F(1, 5)
    its.append(mcq(PTREE(("yellow", "yellow")) + "What probability belongs on the branch marked “?” (yellow, then "
                   "yellow)?", fr(1, 5), [fr(2, 6), fr(2, 5), fr(1, 6)],
                   "After a yellow is taken, the bag has 4 green and 1 yellow: <b>" + fr(1, 5) + "</b>. " + fr(2, 6) +
                   " forgets that the first marble was kept. " + fr(2, 5) + " lowers the total but forgets to take away the yellow.", ans=p))
    p = P(D42, lambda a, b: a == b == "green")
    assert p == F(4, 6) * F(3, 5) == F(12, 30)
    its.append(mcq(PTREE() + "What is the probability of green, then green?", fr(12, 30),
                   [fr(16, 36), fr(7, 11), fr(12, 36)],
                   "Multiply along the branches: " + fr(4, 6) + " × " + fr(3, 5) + " = <b>" + fr(12, 30) + "</b> (= "
                   + fr(2, 5) + "). " + fr(16, 36) + " uses " + fr(4, 6) + " twice, as if the marble went back. "
                   + fr(12, 36) + " lowers the top but not the bottom. " + fr(7, 11) + " adds the tops and the bottoms.", ans=p))
    p = P(D42, lambda a, b: a == b == "yellow")
    assert p == F(2, 6) * F(1, 5) == F(2, 30)
    its.append(mcq(PTREE() + "What is the probability of yellow, then yellow?", fr(2, 30),
                   [fr(4, 36), fr(3, 11), fr(1, 5)],
                   fr(2, 6) + " × " + fr(1, 5) + " = <b>" + fr(2, 30) + "</b> (= " + fr(1, 15) + "). " + fr(4, 36) +
                   " uses " + fr(2, 6) + " twice. " + fr(3, 11) + " adds the tops and the bottoms. " + fr(1, 5) + " is only the second branch.", ans=p))
    p = P(D32, lambda a, b: a == b == "red")
    assert p == F(6, 20)
    its.append(mcq(BAG() + "You draw two marbles without replacement. What is the probability of red, then red?",
                   fr(6, 20), [fr(9, 25), fr(2, 4), fr(6, 25)],
                   fr(3, 5) + " × " + fr(2, 4) + " = <b>" + fr(6, 20) + "</b> (= " + fr(3, 10) + "). " + fr(9, 25) +
                   " puts the marble back. " + fr(6, 25) + " takes one from the red but forgets that the bag also has "
                   "one less marble.", ans=p))
    p = P(D32, lambda a, b: a == b == "blue")
    assert p == F(2, 20)
    its.append(mcq(BAG() + "You draw two marbles without replacement. What is the probability of blue, then blue?",
                   fr(2, 20), [fr(4, 25), fr(1, 4), fr(2, 25)],
                   fr(2, 5) + " × " + fr(1, 4) + " = <b>" + fr(2, 20) + "</b> (= " + fr(1, 10) + "). " + fr(4, 25) +
                   " puts the marble back. " + fr(1, 4) + " is only the second draw.", ans=p))
    p = P(D32, lambda a, b: a == "red" and b == "blue")
    assert p == F(6, 20)
    its.append(mcq(BAG() + "You draw two marbles without replacement. What is the probability of red first, then blue?",
                   fr(6, 20), [fr(6, 25), fr(5, 20), fr(2, 4)],
                   fr(3, 5) + " × " + fr(2, 4) + " = <b>" + fr(6, 20) + "</b>. After a red, there are still 2 blue but "
                   "only 4 marbles. " + fr(6, 25) + " puts the marble back. " + fr(5, 20) + " adds 3 + 2 on top.", ans=p))
    p = P(C4, lambda a, b: a + b == 5)
    assert p == F(4, 12)
    its.append(mcq(CARDS4() + "You draw two cards without replacement. What is the probability that the sum is 5?",
                   fr(4, 12), [fr(4, 16), fr(2, 12), fr(1, 12)],
                   "1, 4; 2, 3; 3, 2; 4, 1: 4 of the 12 white cells, <b>" + fr(4, 12) + "</b> (= " + fr(1, 3) + "). "
                   + fr(4, 16) + " also counts the grey cells. " + fr(2, 12) + " forgets that order matters.", ans=p))
    p = P(C4, lambda a, b: a % 2 == 0 and b % 2 == 0)
    assert p == F(2, 12)
    its.append(mcq(CARDS4() + "What is the probability that both cards are even?", fr(2, 12),
                   [fr(4, 16), fr(1, 12), fr(4, 12)],
                   "2, 4 and 4, 2: <b>" + fr(2, 12) + "</b> (= " + fr(1, 6) + "). Or " + fr(2, 4) + " × " + fr(1, 3) +
                   " = " + fr(2, 12) + ". " + fr(4, 16) + " uses " + fr(2, 4) + " twice, as if the card went back.", ans=p))
    p = F(1, 5) * F(1, 4)
    assert p == P(dep(range(5)), lambda a, b: a == 0 and b == 1)
    its.append(mcq("A teacher puts 5 names in a hat: Liam, Olivia, Noah, Emma and Maya. She draws one name for line "
                   "leader and keeps it out, then draws one for door holder. What is the probability that Liam is line "
                   "leader and Olivia is door holder?", fr(1, 20), [fr(1, 25), fr(2, 20), fr(2, 5)],
                   fr(1, 5) + " × " + fr(1, 4) + " = <b>" + fr(1, 20) + "</b>. " + fr(1, 25) + " puts Liam’s name back. "
                   + fr(2, 20) + " counts Olivia first and Liam second too, but the jobs are different. " + fr(2, 5) + " adds " + fr(1, 5) + " + " + fr(1, 5) + ".", ans=p))
    M41 = ["red"] * 4 + ["blue"]
    p = P(dep(M41), lambda a, b: a == b == "red")
    assert p == F(12, 20) == F(60, 100)
    its.append(mcq("A bag has 4 red marbles and 1 blue marble. You draw two marbles without replacement. What is the "
                   "probability of red both times, as a percent?", "60%", ["64%", "80%", "75%"],
                   fr(4, 5) + " × " + fr(3, 4) + " = " + fr(12, 20) + " = <b>60%</b>. 64% (" + fr(16, 25) + ") puts the "
                   "marble back. 80% is only the first draw, and 75% is only the second.", ans=p))
    assert P(R32, lambda a, b: a == b == "red") > P(D32, lambda a, b: a == b == "red")
    its.append(mcq(BAG() + "Is red, then red more likely with replacement or without replacement?",
                   "With replacement: " + fr(9, 25) + " is more than " + fr(6, 20),
                   ["Without replacement: " + fr(6, 20) + " is more than " + fr(9, 25), "They are equally likely",
                    "Without replacement, because there are fewer marbles"],
                   "With replacement: " + fr(3, 5) + " × " + fr(3, 5) + " = " + fr(9, 25) + " = 0.36. Without: " + fr(3, 5) +
                   " × " + fr(2, 4) + " = " + fr(6, 20) + " = 0.3. <b>With replacement</b> is more likely, because a red "
                   "marble is not used up."))
    its.append(mcq(BAG() + "Mei finds P(red, then red) without replacement as " + fr(3, 5) + " × " + fr(3, 5) +
                   ". What is wrong?", "After one red is kept, the second draw is " + fr(2, 4),
                   ["Nothing, " + fr(3, 5) + " × " + fr(3, 5) + " is right", "She should add: " + fr(3, 5) + " + " + fr(3, 5),
                    "The second draw should be " + fr(3, 4)],
                   "Without replacement, the bag has one less red and one less marble: <b>" + fr(2, 4) + "</b>. "
                   + fr(3, 5) + " × " + fr(2, 4) + " = " + fr(6, 20) + "."))
    p = P(dep(range(1, 11)), lambda a, b: a % 2 == 1 and b % 2 == 1)
    assert p == F(5, 10) * F(4, 9) == F(20, 90)
    its.append(mcq("Ten cards are numbered 1 to 10. You draw two cards without replacement. What is the probability that "
                   "both cards are odd?", fr(20, 90), [fr(25, 100), fr(4, 9), fr(9, 19)],
                   fr(5, 10) + " × " + fr(4, 9) + " = <b>" + fr(20, 90) + "</b> (= " + fr(2, 9) + "). " + fr(25, 100) +
                   " puts the card back. " + fr(4, 9) + " is only the second draw. " + fr(9, 19) + " adds the tops and the bottoms.", ans=p))
    BARS = ["choc"] * 4 + ["oat"] * 6
    p = P(dep(BARS), lambda a, b: a == b == "choc")
    assert p == F(12, 90)
    its.append(mcq("A box has 4 chocolate chip and 6 oatmeal granola bars. Noah takes one without looking and eats it. "
                   "Then Hana takes one without looking. What is the probability that both get chocolate chip?",
                   fr(12, 90), [fr(16, 100), fr(7, 19), fr(12, 100)],
                   fr(4, 10) + " × " + fr(3, 9) + " = <b>" + fr(12, 90) + "</b> (= " + fr(2, 15) + "). " + fr(16, 100) +
                   " forgets that Noah’s bar is gone. " + fr(12, 100) + " lowers the top but not the bottom. " + fr(7, 19) + " adds the tops and the bottoms.", ans=p))
    SOCKS = ["black", "black", "white", "white"]
    p = P(dep(SOCKS), lambda a, b: a == b)
    assert p == F(4, 12)
    its.append(mcq("Ethan’s drawer has 2 black socks and 2 white socks. In the dark, he takes out two socks. What is the "
                   "probability that they match?", fr(4, 12), [fr(1, 2), fr(2, 12), fr(2, 3)],
                   "Black-black: " + fr(2, 4) + " × " + fr(1, 3) + " = " + fr(2, 12) + ". White-white is also "
                   + fr(2, 12) + ". Together: <b>" + fr(4, 12) + "</b> (= " + fr(1, 3) + "). " + fr(1, 2) + " forgets "
                   "that after one black sock, only 1 of the 3 socks left is black. " + fr(2, 12) + " counts one colour only.",
                   ans=p))
    order = [0, 1, 2, 3, 4, 5, 8, 9, 10, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20
    return {"title": "Dependent events: drawing without replacement", "items": its}


# ============================================================ set 5: theoretical vs experimental, word problems
T50V = [12, 13, 14, 11]
DRAWC = ["red, red", "red, blue", "blue, red", "blue, blue"]
DRAWV = [27, 33, 31, 9]


def T50():
    return fig(freq_svg("Two coins tossed 50 times", "Outcome", ["HH", "HT", "TH", "TT"], T50V, tally=False,
                        label="frequency table two coins 50 tosses"))


def T100():
    return fig(freq_svg("Two marbles, no replacement, 100 trials", "Outcome", DRAWC, DRAWV, tally=False,
                        label="frequency table two marbles 100 trials"))


def set_words():
    assert sum(T50V) == 50 and sum(DRAWV) == 100
    its = []
    its.append(mcq(T50() + "What is the experimental probability of HH, as a decimal?", "0.24", ["0.12", "0.25", "0.76"],
                   "HH came up 12 times in 50 tosses: " + fr(12, 50) + " = " + fr(24, 100) + " = <b>0.24</b>. 0.25 is the "
                   "theoretical probability. 0.12 uses the count as the decimal.", ans=F(12, 50)))
    its.append(mcq(T50() + "How does the experimental probability of HH compare with the theoretical probability, "
                   + fr(1, 4) + "?", "It is a little less: 0.24 is less than 0.25",
                   ["It is a little more: 0.24 is more than 0.25", "It is exactly the same",
                    "It is much less: 0.12 is less than 0.25"],
                   fr(12, 50) + " = 0.24 and " + fr(1, 4) + " = 0.25. The experiment is <b>a little less</b> than the "
                   "theory, which is normal."))
    its.append(mcq(T100() + "A class draws two marbles without replacement from a bag of 3 red and 2 blue, 100 times. "
                   "What is the experimental probability of red, red, as a percent?", "27%",
                   ["30%", "36%", "73%"],
                   "Red, red happened 27 times in 100 trials: <b>27%</b>. 30% is the theory (" + fr(6, 20) + "). "
                   "36% is the theory with replacement. 73% is NOT red, red.", ans=F(27, 100)))
    p = P(D32, lambda a, b: a == b == "blue")
    assert p == F(10, 100)
    its.append(mcq(T100() + "What is the theoretical probability of blue, blue, as a percent?", "10%",
                   ["16%", "9%", "40%"],
                   fr(2, 5) + " × " + fr(1, 4) + " = " + fr(2, 20) + " = <b>10%</b>. 9% is what happened in the "
                   "experiment. 16% (" + fr(4, 25) + ") puts the marble back. 40% is " + fr(2, 5) + ", the first draw only.", ans=p))
    p = F(DRAWV[1] + DRAWV[2], 100)
    assert P(D32, lambda a, b: a != b) == F(12, 20)
    its.append(mcq(T100() + "What is the experimental probability of one red and one blue (in either order), as a "
                   "decimal?", "0.64", ["0.33", "0.6", "0.31"],
                   "Red, blue and blue, red: 33 + 31 = 64 times. " + fr(64, 100) + " = <b>0.64</b>. 0.6 is the theory: "
                   + fr(12, 20) + ". 0.33 counts only red, blue.", ans=p))
    assert P(D32, lambda a, b: a == b == "red") * 200 == 60 and P(R32, lambda a, b: a == b == "red") * 200 == 72
    its.append(mcq(BAG() + "You draw two marbles without replacement, and do this 200 times. About how many times would "
                   "you expect red, red?", "about 60", ["about 72", "about 120", "about 54"],
                   "P(red, red) = " + fr(3, 5) + " × " + fr(2, 4) + " = " + fr(3, 10) + ". " + fr(3, 10) +
                   " of 200 = <b>60</b>. About 72 uses " + fr(9, 25) + " (with replacement). About 120 uses " + fr(3, 5) +
                   ", the first draw only."))
    assert F(1, 12) * 120 == 10
    its.append(mcq("You toss a coin and roll a number cube 120 times. About how many times would you expect heads and "
                   "a 6?", "about 10", ["about 15", "about 20", "about 60"],
                   "P(heads and 6) = " + fr(1, 12) + ". 120 ÷ 12 = <b>about 10</b>. About 15 uses " + fr(1, 8) +
                   " (adding 2 + 6 outcomes). About 20 uses " + fr(1, 6) + " only."))
    its.append(mcq("The theoretical probability of HH is 0.25. Group A tosses two coins 20 times and gets HH 8 times. "
                   "Group B tosses them 400 times and gets HH 96 times. Whose result is closer to 0.25?", "Group B’s",
                   ["Group A’s", "They are equally close", "Neither, both are far off"],
                   "Group A: " + fr(8, 20) + " = 0.4. Group B: " + fr(96, 400) + " = 0.24. <b>Group B’s</b> is closer. "
                   "More trials usually get closer to the theory."))
    assert F(8, 20) == F(4, 10) and F(96, 400) == F(24, 100)
    its.append(mcq("Two fair coins have landed TT four times in a row. What is the probability of HH on the next toss?",
                   fr(1, 4), ["1", fr(1, 2), fr(4, 5)],
                   "Coin tosses are independent. HH is still <b>" + fr(1, 4) + "</b>. Thinking HH is “due” is called "
                   "the gambler’s fallacy.", ans=F(1, 4)))
    its.append(mcq("Ryan draws two marbles without replacement from the bag of 3 red and 2 blue, 10 times. He gets "
                   "blue, blue 3 times. He says the bag must be wrong because the theory is 10%. Is he right?",
                   "No, 10 trials are too few to tell",
                   ["Yes, 30% is far from 10%", "Yes, blue, blue should happen exactly once", "No, blue, blue is impossible"],
                   "With only 10 trials, results can be far from the theory just by chance. <b>10 trials are too few "
                   "to tell</b>. He should do many more trials."))
    BAG22 = ["red", "red", "blue", "blue"]
    same = P(dep(BAG22), lambda a, b: a == b)
    assert same == F(4, 12) and 1 - same == F(8, 12)
    its.append(mcq("Arjun and Hana use a bag of 2 red and 2 blue marbles. They draw two marbles without replacement. "
                   "Arjun wins if the colours match. Hana wins if they are different. Who is more likely to win?",
                   "Hana: " + fr(8, 12) + " to " + fr(4, 12),
                   ["It is fair: each has " + fr(1, 2), "Arjun: " + fr(8, 12) + " to " + fr(4, 12), "You can’t tell"],
                   "Match: " + fr(2, 4) + " × " + fr(1, 3) + " for red-red plus the same for blue-blue = " + fr(4, 12) +
                   ". Different: " + fr(8, 12) + ". <b>Hana</b> is more likely to win. Many people guess " + fr(1, 2) +
                   " because they forget that the first marble is kept."))
    TRIPS = ["CN Tower", "ROM", "AGO", "Casa Loma"]
    p = P(dep(TRIPS), lambda a, b: a == "CN Tower" and b == "Casa Loma")
    assert p == F(1, 12)
    its.append(mcq("A Grade 7 class in Toronto draws a fall field trip at random from 4 places: the CN Tower, the Royal "
                   "Ontario Museum, the Art Gallery of Ontario and Casa Loma. The spring trip is drawn from the 3 places "
                   "left. What is the probability of the CN Tower in the fall and Casa Loma in the spring?", fr(1, 12),
                   [fr(1, 16), fr(1, 7), fr(2, 12)],
                   fr(1, 4) + " × " + fr(1, 3) + " = <b>" + fr(1, 12) + "</b>. " + fr(1, 16) + " forgets that the fall "
                   "place is not drawn again. " + fr(1, 7) + " adds 4 + 3. " + fr(2, 12) + " counts the other order too.",
                   ans=p))
    p = F(1, 15) * F(1, 14)
    assert p == F(1, 210)
    its.append(mcq("A hockey coach draws a captain at random from 15 players, then an assistant captain from the other "
                   "14. What is the probability that Owen is captain and Kai is assistant captain?", fr(1, 210),
                   [fr(1, 225), fr(2, 29), fr(1, 29)],
                   fr(1, 15) + " × " + fr(1, 14) + " = <b>" + fr(1, 210) + "</b>. " + fr(1, 225) + " lets Owen be drawn "
                   "twice. " + fr(1, 29) + " adds 15 + 14.", ans=p))
    p = F(1, 4) * F(1, 5)
    its.append(mcq("At the Terry Fox Run, each runner gets a random wristband (4 colours, equally likely) and a random "
                   "sticker (5 kinds, one is a loon). What is the probability that Priya gets a green wristband and the "
                   "loon sticker, as a percent?", "5%", ["45%", "20%", "about 11%"],
                   "The wristband and sticker are independent: " + fr(1, 4) + " × " + fr(1, 5) + " = " + fr(1, 20) +
                   " = <b>5%</b>. 45% adds 25% + 20%. About 11% is " + fr(1, 9) + ", from adding 4 + 5 outcomes.",
                   ans=p))
    assert F(1, 8) * 160 == 20
    its.append(mcq("Sofia’s fun fair game has a " + fr(1, 8) + " chance of winning. She expects 160 players. About how "
                   "many prizes should she bring?", "about 20", ["about 40", "about 80", "about 140"],
                   fr(1, 8) + " of 160 = 160 ÷ 8 = <b>about 20</b>. About 140 is the players who should NOT win. "
                   "About 80 is half the players."))
    its.append(mcq("At the fun fair, 24 of the 160 players won Sofia’s game. What is the experimental probability of "
                   "winning, as a percent?", "15%", ["24%", "12.5%", "85%"],
                   fr(24, 160) + " = " + fr(15, 100) + " = <b>15%</b>. 12.5% is the theoretical probability, " + fr(1, 8) +
                   ". 85% is the players who did not win.", ans=F(24, 160)))
    MUF = ["b"] * 5 + ["n"] * 7
    p = P(dep(MUF), lambda a, b: a == b == "b")
    assert p == F(20, 132)
    its.append(mcq("A box has 12 muffins: 5 blueberry and 7 banana. Mateo takes one without looking, then Chloe takes "
                   "one. What is the probability that both get blueberry?", fr(20, 132),
                   [fr(25, 144), fr(9, 23), fr(20, 144)],
                   fr(5, 12) + " × " + fr(4, 11) + " = <b>" + fr(20, 132) + "</b> (= " + fr(5, 33) + "). " + fr(25, 144) +
                   " forgets that Mateo’s muffin is gone. " + fr(20, 144) + " lowers the top but not the bottom. " + fr(9, 23) + " adds the tops and the bottoms.", ans=p))
    assert p * 264 == 40 and F(25, 144) * 264 > 45 and F(5, 12) * 264 == 110
    its.append(mcq("Leah simulates the muffin draw 264 times on a computer. About how many times does the theory predict "
                   "two blueberry muffins?", "about 40", ["about 46", "about 110", "about 20"],
                   fr(20, 132) + " × 264 = 20 × 2 = <b>40</b>. About 46 uses " + fr(25, 144) + " (with replacement). "
                   "About 110 uses " + fr(5, 12) + ", Mateo’s pick only. About 20 is just the top of the fraction."))
    p = P(dep(range(1, 6)), lambda a, b: a + b == 9)
    assert p == F(2, 20)
    its.append(mcq("Jayden draws two cards from cards 1 to 5 without replacement. He does this 60 times and gets a sum "
                   "of 9 eight times. What is the theoretical probability of a sum of 9?", fr(2, 20),
                   [fr(8, 60), fr(1, 20), fr(2, 25)],
                   "4, 5 and 5, 4 are 2 of the 5 × 4 = 20 outcomes: <b>" + fr(2, 20) + "</b> (= " + fr(1, 10) + "). "
                   + fr(8, 60) + " is the experimental probability. " + fr(2, 25) + " uses 5 × 5 outcomes, as if the card "
                   "went back.", ans=p))
    its.append(mcq("Kai tosses two coins 20 times and gets HH 7 times. He says the experimental probability of HH is "
                   + fr(7, 13) + ". What is wrong?", "He should divide by all 20 trials: " + fr(7, 20),
                   ["Nothing, " + fr(7, 13) + " is right", "He should use the theory: " + fr(1, 4),
                    "He should divide by the 4 outcomes: " + fr(7, 4)],
                   "7 HH out of 20 trials is <b>" + fr(7, 20) + "</b>. " + fr(7, 13) + " compares HH with the other 13 "
                   "trials, not with all 20."))
    assert len(its) == 20
    return {"title": "Theoretical vs experimental probability and word problems", "items": its}


# ============================================================ lesson
def body_html():
    bag = bag_svg([("red", 3), ("blue", 2)], label="bag of 3 red and 2 blue marbles")
    tree = ptree_svg([("red", "3/5"), ("blue", "2/5")],
                     {"red": [("red", "2/4"), ("blue", "2/4")], "blue": [("red", "3/4"), ("blue", "1/4")]},
                     label="probability tree red and blue marbles without replacement")
    return (
        "<h2>Independent or dependent?</h2>"
        "<p>Two events are <b>independent</b> when the first result does not change the chances for the second. "
        "Tossing a coin and rolling a number cube are independent. So is drawing a card, <b>putting it back</b>, "
        "and drawing again.</p>"
        "<p>Two events are <b>dependent</b> when the first result changes the chances for the second. "
        "Drawing a marble and <b>keeping it</b> before the next draw makes the draws dependent.</p>"
        "<h2>Sample spaces</h2>"
        "<p>List every outcome in a table or a tree diagram. Count by <b>multiplying</b>. "
        "A coin and a number cube give 2 × 6 = 12 outcomes. Two cards from cards 1 to 4 without replacement give "
        "4 × 3 = 12 outcomes, because only 3 cards are left for the second draw.</p>"
        "<figure class='sn-fig'>" + cards_table_svg(4, label="outcome table two cards 1 to 4 without replacement") +
        "<figcaption>The grey cells can’t happen: the same card can’t be drawn twice.</figcaption></figure>"
        "<h2>Two independent events</h2>"
        "<p>Multiply the two probabilities, or count in the table.</p>"
        + ex("Example 1", "You toss a coin and roll a number cube. What is P(heads and 6)?",
             fr(1, 2) + " × " + fr(1, 6) + " = " + fr(1, 12) + ". In the table, H6 is 1 of 12 outcomes.",
             fr(1, 12))
        + "<h2>Two dependent events</h2>"
        "<p>For the second draw, use what is <b>left</b> in the bag: one less item, and one less of the colour you drew.</p>"
        "<figure class='sn-fig'>" + bag + "<figcaption>3 red and 2 blue marbles.</figcaption></figure>"
        "<figure class='sn-fig'>" + tree +
        "<figcaption>Two draws without replacement. The second-draw probabilities depend on the first draw.</figcaption></figure>"
        + ex("Example 2", "You draw two marbles from this bag without replacement. What is P(red, then red)?",
             "First red: " + fr(3, 5) + ". Then 2 red are left out of 4: " + fr(2, 4) + ". Multiply along the branches: "
             + fr(3, 5) + " × " + fr(2, 4) + " = " + fr(6, 20) + ".",
             fr(6, 20) + " = " + fr(3, 10) + " = 0.3 = 30%")
        + ex("Example 3", "Same bag, but the first marble is put back. What is P(red, then red)?",
             "The bag is the same for both draws: " + fr(3, 5) + " × " + fr(3, 5) + " = " + fr(9, 25) + ".",
             fr(9, 25) + " = 0.36 = 36%")
        + "<h2>Theoretical and experimental probability</h2>"
        "<p>Theoretical probability is what should happen. Experimental probability is what did happen: "
        "times it happened ÷ number of trials. They are usually close, but rarely the same. "
        "<b>More trials usually get closer.</b></p>"
        + table(["Draws of two marbles (no replacement)", "Red, red", "Experimental P(red, red)"], [
            ["20", "8", fr(8, 20) + " = 0.4"],
            ["100", "27", fr(27, 100) + " = 0.27"],
            ["1000", "304", fr(304, 1000) + " = 0.304"],
        ])
        + ex("Example 4", "About how many times would you expect red, red in 200 draws of two marbles without replacement?",
             "P(red, red) = " + fr(3, 10) + ". " + fr(3, 10) + " of 200 = 60.", "about 60")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["P(heads and 6) = " + fr(1, 2) + " + " + fr(1, 6) + " = " + fr(4, 6),
             "Don’t add. Multiply: " + fr(1, 2) + " × " + fr(1, 6) + " = " + fr(1, 12) + "."],
            ["Without replacement: P(red, red) = " + fr(3, 5) + " × " + fr(3, 5) + ".",
             "The first marble was kept: " + fr(3, 5) + " × " + fr(2, 4) + "."],
            ["Second draw: " + fr(2, 5) + " (one less red, same total).", "The total goes down too: " + fr(2, 4) + "."],
            ["Two cards from 1 to 4 without replacement: 4 × 4 = 16 outcomes.", "4 × 3 = 12 outcomes."],
            ["“The experiment must match the theory exactly.”", "Results vary. More trials get closer."],
        ])
    )


FAQ = [
    {"q": "What is the difference between independent and dependent events in Grade 7 math?",
     "a": "Independent events do not change each other’s chances, like tossing a coin and rolling a number cube. Dependent events do: if you draw a marble and keep it, the next draw has one less marble, so the chances change."},
    {"q": "How do you find the probability of two dependent events?",
     "a": "Multiply the probability of the first event by the probability of the second event after the first has happened. For 3 red and 2 blue marbles drawn without replacement, P(red, then red) = 3/5 × 2/4 = 6/20 = 3/10."},
    {"q": "What does the Ontario Grade 7 math curriculum expect for probability?",
     "a": "In the Data strand (D2.1 and D2.2), Grade 7 students describe independent and dependent events, and determine and compare the theoretical and experimental probabilities of two independent events and of two dependent events happening."},
    {"q": "What is the difference between theoretical and experimental probability?",
     "a": "Theoretical probability is what should happen, found by counting outcomes or multiplying probabilities. Experimental probability is what actually happened in trials, such as 27 red, red results in 100 trials (27%). With more trials, the two usually get closer."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (tables, tree diagrams, two spinners)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(47816)
    sets = [set_kind(), set_sample_spaces(), set_independent(), set_dependent(), set_words()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-7",
        "slug": "probability-of-independent-and-dependent-events", "sort": 16, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Probability of Independent and Dependent Events",
        "seo_title": "Grade 7 Independent and Dependent Events Worksheets: Free Probability Math with Answer Key (Ontario Curriculum)",
        "short_title": "Independent and dependent events",
        "domain": "Data",
        "standard_code": "Grade 7: D2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine and compare the theoretical and experimental probabilities of two independent events happening and of two dependent events happening",
        "meta_desc": "Free Grade 7 math worksheets on independent and dependent events for the Ontario curriculum: telling the two apart, sample spaces with tables and tree diagrams, probability with and without replacement, and comparing theoretical and experimental probability. 100 questions with an answer key.",
        "key_big": "Independent: multiply the two probabilities. Dependent: for the second event, use what is left after the first.",
        "key_sub": "3 red and 2 blue marbles: with replacement, P(red, red) = 3/5 × 3/5 = 9/25. Without replacement, 3/5 × 2/4 = 6/20. Never add the probabilities.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(frequency table|tree diagram|outcome table|two spinners|sum table|probability tree)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
