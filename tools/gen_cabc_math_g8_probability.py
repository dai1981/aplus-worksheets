# -*- coding: utf-8 -*-
"""
BC Grade 8 Math: Probability of Two Independent Events
(BC Mathematics Curriculum, Grade 8: Data and probability, theoretical probability with two independent events)
  python3 tools/gen_cabc_math_g8_probability.py
Sample spaces with outcome tables, product and sum tables and tree diagrams, independent and dependent events,
theoretical probability of two independent events by counting, the multiplication rule P(A and B) = P(A) × P(B)
with fractions, decimals and percents (unequal spinners, marbles put back, probability trees), comparing
predictions with results (expected counts, more trials, fair games) and word problems in BC contexts
(BC Ferries, Whistler, Grouse Mountain field trip, lacrosse, orca tours, school fun fair).
Wrong answers come from real student mistakes: adding the probabilities instead of multiplying (1/2 + 1/6),
adding the outcomes (4 + 3 = 7), adding the tops and the bottoms (1/2 and 1/5 -> 2/7), counting only one order
(2 × 2 but not the reverse), treating the different sums or products as equally likely, decimal place errors
(0.3 × 0.3 = 0.9), using one path of a probability tree only, not putting the marble back, using an experimental
result as the prediction and the gambler's fallacy.
Helpers (spinners, marble jar, outcome tables, tree diagrams, probability trees) are adapted from
gen_cabc_math_g7_probability.py and gen_caon_math_g8_probability.py.
Every answer is checked in code with fractions.Fraction. Canadian English. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
GREEN = "#006633"
HEAD = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
COL = {"red": "#f08a80", "blue": "#8db4ee", "yellow": "#f7dc6f", "green": "#8fd19e",
       "purple": "#c9aef0", "white": "#ffffff", "grey": "#e4e4e4"}
INIT = {"red": "R", "blue": "B", "yellow": "Y", "green": "G", "purple": "P", "white": "W"}
NB = " "
M = "−"


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


def mcq(q, correct, wrong, e, ans=None):
    """4 choices: correct first + 3 wrong; positions are set later by balance().
    Numeric choices must all have different values; ans checks the value of the correct choice."""
    ch = [str(correct)] + [str(x) for x in wrong]
    assert len(ch) == 4, (q, ch)
    plain = [re.sub(r"<[^>]+>", " ", x).strip() for x in ch]
    assert len(set(plain)) == 4, (q, ch)
    vals = [val(x) for x in ch]
    nums = [v for v in vals if v is not None]
    assert len(set(nums)) == len(nums), ("two equal values", q, ch)
    if ans is not None:
        assert vals[0] == F(ans), (q, vals[0], ans)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    assert "'" not in label
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
    r = R * 0.64
    ang = 2 * math.pi * float(f)
    chord = 2 * r * math.sin(min(ang, math.pi) / 2) if ang < 2 * math.pi else 2 * R
    return tw(t, fs) + 6 <= chord and r + fs / 2 + 2 <= R


def spinner_body(cx, cy, R, spec, fs=15):
    """Spinner drawn to its exact fractions, starting at 12 o'clock and going clockwise."""
    s = []
    a0 = F(0)
    labels = []
    for lab, f, c in spec:
        fill = COL.get(c, c)
        a1 = a0 + f
        t0 = 2 * math.pi * float(a0) - math.pi / 2
        t1 = 2 * math.pi * float(a1) - math.pi / 2
        x0, y0 = cx + R * math.cos(t0), cy + R * math.sin(t0)
        x1, y1 = cx + R * math.cos(t1), cy + R * math.sin(t1)
        big = 1 if f > F(1, 2) else 0
        s.append("<path d='M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2' "
                 "stroke-linejoin='round'/>" % (cx, cy, x0, y0, R, R, big, x1, y1, fill, LINE))
        if lab:
            tm = (t0 + t1) / 2
            rr = R * 0.64
            assert label_fits(R, f, lab, fs), (lab, f, R)
            labels.append(text(cx + rr * math.cos(tm), cy + rr * math.sin(tm) + fs * 0.35, lab, fs))
        a0 = a1
    s += labels
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


def spinner_svg(spec, R=60, label="spinner"):
    W = 2 * R + 12
    H = 2 * R + 12
    return svg_wrap(W, H, spinner_body(W / 2, H / 2, R, secs_of(spec), fs=14), label)


def key_line(names):
    return ",  ".join("%s = %s" % (INIT[n], n) for n in names)


def bag_svg(counts, label="bag of marbles"):
    """A jar of marbles; each marble is coloured and carries its initial. counts: list of (colour, n)."""
    marbles = [c for c, n in counts for _ in range(n)]
    n = len(marbles)
    per = min(6, n)
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
    if W > jw + 20:
        s = ["<g transform='translate(%.1f 0)'>" % ((W - jw - 20) / 2)] + s + ["</g>"]
    s.append(text(W / 2, H - 6, k, 14, weight=400))
    return svg_wrap(W, int(H), "".join(s), label)


def grid_svg(corner, rows, cols, cell, top_title, label, cw_min=34):
    """Outcome table: header row = second event, first column = first event, cell(r, c) = the outcome text."""
    fs, rh = 15, 28
    c1 = int(max(max(tw(r, fs) for r in rows), tw(corner, fs)) + 18)
    cw = int(max(max(tw(cell(r, c), fs, False) for r in rows for c in cols) + 14,
                 max(tw(c, fs) for c in cols) + 12, cw_min))
    W = int(max(c1 + cw * len(cols) + 8, tw(top_title, 15) + 12))
    x0 = (W - c1 - cw * len(cols)) / 2
    s = [text(x0 + c1 + cw * len(cols) / 2, 17, top_title, 15)]
    assert x0 + c1 + cw * len(cols) / 2 + tw(top_title, 15) / 2 <= W
    y0 = 24
    for r in range(len(rows) + 1):
        for k in range(len(cols) + 1):
            x = x0 + (0 if k == 0 else c1 + (k - 1) * cw)
            w = c1 if k == 0 else cw
            y = y0 + r * rh
            hd = r == 0 or k == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, w, rh, HEAD if hd else "#ffffff", GREEN))
            if r == 0 and k == 0:
                s.append(text(x + w / 2, y + 19, corner, fs))
            elif r == 0:
                s.append(text(x + w / 2, y + 19, cols[k - 1], fs))
            elif k == 0:
                s.append(text(x + w / 2, y + 19, rows[r - 1], fs))
            else:
                s.append(text(x + w / 2, y + 19, cell(rows[r - 1], cols[k - 1]), fs, weight=400))
    H = y0 + (len(rows) + 1) * rh + 4
    return svg_wrap(int(W), int(H), "".join(s), label)


def tree_svg(levels, heads, label="tree diagram"):
    """Tree diagram for 2 events, each level a list of short labels; outcomes listed on the right."""
    gap, top = 22, 34
    nleaf = 1
    for lv in levels:
        nleaf *= len(lv)
    H = top + nleaf * gap + 4
    xr = 12
    colw = [max(tw(t, 16) for t in lv) for lv in levels]
    xs = []
    x = xr + 52
    for k, w in enumerate(colw):
        xs.append(x + w / 2)
        x += w + 52
    xo = max(x - 52 + 22, xs[-1] + tw(heads[-1], 14) / 2 + 14)
    joint = ", " if any(len(t) > 1 for lv in levels for t in lv) else ""
    s = [text(xs[k], 18, heads[k], 14) for k in range(len(levels))]
    s.append(text(xo, 18, "Outcome", 14, anchor="start"))
    for k in range(len(levels) - 1):
        assert xs[k] + tw(heads[k], 14) / 2 + 6 < xs[k + 1] - tw(heads[k + 1], 14) / 2, heads
    assert xs[0] - tw(heads[0], 14) / 2 >= 2, heads
    s.append("<circle cx='%d' cy='%.1f' r='4' fill='%s'/>" % (xr, top + nleaf * gap / 2, LINE))
    outs = []

    def node(level, prefix, i0, px, py):
        under = 1
        for lv in levels[level + 1:]:
            under *= len(lv)
        for j, t in enumerate(levels[level]):
            a = i0 + j * under
            y = top + (a + under / 2) * gap
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (px, py, xs[level] - tw(t, 16) / 2 - 5, y, THIN))
            s.append(text(xs[level], y + 6, t, 16, col=GREEN if level == 0 else LINE))
            if level + 1 < len(levels):
                node(level + 1, prefix + [t], a, xs[level] + tw(t, 16) / 2 + 5, y)
            else:
                o = joint.join(prefix + [t])
                outs.append(o)
                s.append(text(xo, y + 5, o, 15, anchor="start", weight=400))

    node(0, [], 0, xr, top + nleaf * gap / 2)
    W = int(max(xo + max(tw(o, 15, False) for o in outs) + 8, xo + tw("Outcome", 14) + 8))
    return svg_wrap(W, int(H), "".join(s), label)


def ptree_svg(first, second, label="probability tree", h1="First spin", h2="Second spin"):
    """Probability tree for two independent events. first, second: [(name, 'p')]."""
    fs = 15
    gap, top = 34, 40
    rows = len(first) * len(second)
    H = top + rows * gap + 2
    xr = 10
    x1a, x1b = 54, 112
    xa = 118
    w1 = max(tw(a, 16) for a, _ in first)
    x2s = xa + w1 + 6
    x2a, x2b = x2s + 40, x2s + 98
    xb = x2b + 6
    w2 = max(tw(b, fs) for b, _ in second)
    xo = max(xb + w2 + 22, xb + w2 / 2 + tw(h2, fs) / 2 + 16)
    assert xa + w1 / 2 + tw(h1, fs) / 2 + 10 < xb + w2 / 2 - tw(h2, fs) / 2, (h1, h2)
    assert xa + w1 / 2 - tw(h1, fs) / 2 >= 2, h1
    for _, p in first + second:
        assert tw(p, fs) <= 56, p
    s = [text(xa + w1 / 2, 18, h1, fs), text(xb + w2 / 2, 18, h2, fs), text(xo, 18, "Outcome", fs, anchor="start")]
    ry = top + rows * gap / 2
    s.append("<circle cx='%d' cy='%.1f' r='4' fill='%s'/>" % (xr, ry, LINE))
    k = len(second)
    for i, (a, pa) in enumerate(first):
        ay = top + (i * k + k / 2) * gap
        s.append("<polyline points='%d,%.1f %d,%.1f %d,%.1f' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xr, ry, x1a, ay, x1b, ay, THIN))
        s.append(text((x1a + x1b) / 2, ay - 6, pa, fs, col=GREEN))
        s.append(text(xa, ay + 6, a, 16, anchor="start"))
        for j, (b, pb) in enumerate(second):
            by = top + (i * k + j + 0.5) * gap
            s.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x2s, ay, x2a, by, x2b, by, THIN))
            s.append(text((x2a + x2b) / 2, by - 6, pb, fs, col=GREEN))
            s.append(text(xb, by + 5, b, fs, anchor="start"))
            s.append(text(xo, by + 5, a + ", " + b, fs, anchor="start", weight=400))
    W = int(max(xo + max(tw(a + ", " + b, fs, False) for a, _ in first for b, _ in second) + 8,
                xo + tw("Outcome", fs) + 8))
    return svg_wrap(W, int(H), "".join(s), label)


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


# ------------------------------------------------------------ sample spaces and figures
def outcomes(a, b):
    return [(x, y) for x in a for y in b]


def P(space, cond):
    return F(sum(1 for o in space if cond(*o)), len(space))


def cnt(space, cond):
    return sum(1 for o in space if cond(*o))


NUM4 = [1, 2, 3, 4]
CLR3 = ["red", "blue", "green"]
O_NC = outcomes(NUM4, CLR3)                 # number spinner 1-4 and colour spinner
O_P = outcomes(NUM4, NUM4)                  # two spinners 1-4 (products)
O36 = outcomes(range(1, 7), range(1, 7))    # two number cubes
O_SC = outcomes("ABC", "HT")                # spinner A, B, C then coin
O12 = outcomes("HT", range(1, 7))           # coin and number cube


def TAB_NC():
    return fig(grid_svg("", ["1", "2", "3", "4"], ["red", "blue", "green"],
                        lambda r, c: r + INIT[c], "Colour spinner",
                        label="outcome table number spinner 1 to 4 and colour spinner"))


def TAB_P():
    return fig(grid_svg("×", ["1", "2", "3", "4"], ["1", "2", "3", "4"],
                        lambda r, c: str(int(r) * int(c)), "Second spinner",
                        label="outcome table products of two spinners 1 to 4"))


def TAB_S():
    return fig(grid_svg("+", [str(k) for k in range(1, 7)], [str(k) for k in range(1, 7)],
                        lambda r, c: str(int(r) + int(c)), "Second number cube",
                        label="outcome table sums of two number cubes"))


def TREE_SC():
    return fig(tree_svg([["A", "B", "C"], ["H", "T"]], ["Spinner", "Coin"],
                        label="tree diagram spinner A B C then coin"))


YG = [("yellow", F(1, 3), "yellow"), ("yellow", F(1, 3), "yellow"), ("green", F(1, 3), "green")]


def SPIN_YG():
    return fig(spinner_svg(YG, R=72, label="spinner two yellow sections one green section"))


FT = [("make", "0.6"), ("miss", "0.4")]
GW = [("green", "1/4"), ("white", "3/4")]


def PT_FT():
    return fig(ptree_svg(FT, FT, label="probability tree two free throws", h1="First shot", h2="Second shot"))


def PT_GW():
    return fig(ptree_svg(GW, GW, label="probability tree spinner green and white spun twice"))


BAG = [("red", 3), ("blue", 2)]


def BAGF():
    return fig(bag_svg(BAG, label="jar with 3 red and 2 blue marbles"))


COINS60 = [("HH", 18), ("HT or TH", 27), ("TT", 15)]


def T60():
    return fig(table_svg("Two coins tossed 60 times", ["Outcome"] + [c for c, _ in COINS60],
                         [["Frequency"] + [str(v) for _, v in COINS60]], label="results table two coins 60 tosses"))


# ============================================================ set 1: sample spaces
def set_sample_spaces():
    its = []
    its.append(mcq(TREE_SC() + "A spinner has 3 equal sections, A, B and C. You spin it and toss a coin. "
                   "How many outcomes does the tree diagram show?", "6", ["5", "3", "8"],
                   "Each of the 3 spinner branches splits into 2 coin branches: 3 × 2 = <b>6</b> outcomes. "
                   "5 comes from adding 3 + 2.", ans=len(O_SC)))
    its.append(mcq(TREE_SC() + "Which outcome is NOT in the sample space?", "DH", ["AH", "BT", "CT"],
                   "The spinner only has A, B and C, so <b>DH</b> can’t happen. The other three are at the end of a branch."))
    its.append(mcq(TREE_SC() + "How many outcomes show tails?", "3", ["1", "6", "2"],
                   "AT, BT and CT: <b>3</b> outcomes. Every spinner branch has one tails branch.",
                   ans=cnt(O_SC, lambda a, b: b == "T")))
    its.append(mcq(TAB_NC() + "You spin a number spinner (1 to 4) and a colour spinner (red, blue, green). "
                   "How many outcomes are in the table?", "12", ["7", "4", "16"],
                   "4 rows × 3 columns = <b>12</b> outcomes. 7 comes from adding 4 + 3.", ans=len(O_NC)))
    n = cnt(O_NC, lambda k, c: k % 2 == 0 and c == "green")
    its.append(mcq(TAB_NC() + "How many outcomes show an even number and green?", "2", ["4", "1", "3"],
                   "Even numbers are 2 and 4, so 2G and 4G: <b>2</b> outcomes. 4 counts every green outcome.", ans=n))
    n = cnt(O_NC, lambda k, c: c == "red")
    its.append(mcq(TAB_NC() + "How many outcomes show red?", "4", ["1", "3", "12"],
                   "The red column has 1R, 2R, 3R and 4R: <b>4</b> outcomes. 12 is the whole table.", ans=n))
    n = cnt(O_NC, lambda k, c: k > 2 and c != "blue")
    assert cnt(O_NC, lambda k, c: k > 2) == 6 and cnt(O_NC, lambda k, c: c != "blue") == 8
    its.append(mcq(TAB_NC() + "How many outcomes show a number greater than 2 and NOT blue?", "4", ["2", "6", "8"],
                   "Numbers 3 and 4 with red or green: 3R, 3G, 4R, 4G, so <b>4</b> outcomes. "
                   "6 counts every outcome with 3 or 4. 8 counts every outcome that is not blue.", ans=n))
    its.append(mcq("You roll a number cube and spin a spinner with 4 equal sections. How many outcomes are there?",
                   "24", ["10", "6", "4"],
                   "Each of the 6 numbers goes with each of the 4 sections: 6 × 4 = <b>24</b>. 10 comes from adding 6 + 4.",
                   ans=6 * 4))
    its.append(mcq("A spinner has 5 equal sections. You spin it twice. How many outcomes are there?", "25",
                   ["10", "5", "20"],
                   "Each of the 5 results on the first spin goes with each of the 5 on the second: 5 × 5 = <b>25</b>. "
                   "10 comes from adding 5 + 5.", ans=25))
    n = cnt(O_P, lambda a, b: a * b == 4)
    assert n == 3
    its.append(mcq(TAB_P() + "You spin two spinners, each with 4 equal sections numbered 1 to 4, and multiply the "
                   "numbers. How many outcomes give a product of 4?", "3", ["2", "1", "4"],
                   "1 × 4, 2 × 2 and 4 × 1: <b>3</b> outcomes. 2 forgets that 1 × 4 and 4 × 1 are different outcomes.",
                   ans=n))
    n = cnt(O_P, lambda a, b: a * b % 2 == 1)
    assert n == 4
    its.append(mcq(TAB_P() + "How many outcomes give an odd product?", "4", ["8", "2", "12"],
                   "The product is odd only when both numbers are odd: 2 × 2 = <b>4</b> outcomes (1, 3, 3, 9). "
                   "12 is the number of even products.", ans=n))
    prods = {}
    for a, b in O_P:
        prods[a * b] = prods.get(a * b, 0) + 1
    assert max(prods, key=prods.get) == 4 and list(prods.values()).count(3) == 1
    its.append(mcq(TAB_P() + "Which product appears in the most cells?", "4", ["16", "12", "1"],
                   "4 is in 3 cells (1 × 4, 2 × 2, 4 × 1). Every other product is in 1 or 2 cells, so <b>4</b> is the "
                   "most likely product. 16 is the largest product, but it is in only one cell.", ans=4))
    its.append(mcq("Kai picks a hoodie (grey or navy) and a cap (black, white or red). In a tree diagram, how many "
                   "branches end on the right side?", "6", ["5", "2", "3"],
                   "Each of the 2 hoodies splits into 3 caps: 2 × 3 = <b>6</b> end branches, one for each outfit. "
                   "5 adds 2 + 3.", ans=6))
    its.append(mcq("You toss a nickel and a dime. Which list shows the sample space?", "HH, HT, TH, TT",
                   ["HH, HT, TT", "H, T", "HT, TH"],
                   "Each coin can land H or T: 2 × 2 = 4 outcomes, <b>HH, HT, TH, TT</b>. "
                   "HT (nickel heads) and TH (dime heads) are different outcomes."))
    its.append(mcq("Which pair of events is independent?", "Rolling a number cube and tossing a coin",
                   ["Drawing two cards from a deck without putting the first back",
                    "Picking a team captain, then a co-captain from the other players",
                    "Taking two granola bars from a box without putting the first back"],
                   "A coin cannot change how a number cube lands, so <b>a number cube and a coin</b> are independent. "
                   "In the other pairs, the first pick changes what is left for the second."))
    its.append(mcq("Which pair of events is NOT independent?", "Picking two names from a hat without putting the first back",
                   ["Spinning the same spinner twice", "Rolling two number cubes", "Tossing a coin and spinning a spinner"],
                   "When the first name stays out, there are fewer names left, so the chance for the second pick "
                   "changes. Those events are <b>not independent</b>. Coins, cubes and spinners have no memory."))
    its.append(mcq("Ava says, “A spinner with 4 sections and a spinner with 3 sections give 4 + 3 = 7 outcomes.” "
                   "What is wrong?", "Each of the 4 results pairs with all 3: 4 × 3 = 12",
                   ["Nothing, 4 + 3 = 7 is right", "There are only 4 outcomes, from the bigger spinner",
                    "There are 4 × 3 × 2 = 24 outcomes"],
                   "Result 1 can go with each of the 3 sections, and so can 2, 3 and 4. That is 3 + 3 + 3 + 3 = "
                   "4 × 3 = <b>12</b> outcomes. Multiply, don’t add."))
    its.append(mcq(fig(bag_svg([("red", 1), ("blue", 1), ("green", 1), ("yellow", 1)],
                               label="jar with one red one blue one green and one yellow marble")) +
                   "You take a marble, put it back, and take a marble again. How many outcomes are there?", "16",
                   ["8", "12", "4"],
                   "The marble goes back, so the second pick also has 4 colours: 4 × 4 = <b>16</b>. 8 adds 4 + 4. "
                   "12 = 4 × 3 would be right only if the first marble stayed out.", ans=16))
    its.append(mcq("You make an outcome table for a coin and a spinner with 8 equal sections. How many cells with "
                   "outcomes does it have?", "16", ["10", "8", "64"],
                   "2 rows × 8 columns = <b>16</b> cells. 10 adds 2 + 8. 64 is 8 × 8, as if there were two spinners.",
                   ans=2 * 8))
    its.append(mcq("Two independent events have 18 outcomes in all. The first event is a coin toss. How many "
                   "outcomes does the second event have?", "9", ["16", "36", "20"],
                   "2 × ? = 18, so the second event has 18 ÷ 2 = <b>9</b> outcomes. 16 subtracts 18 − 2.".replace("−", M),
                   ans=9))
    assert len(its) == 20
    return {"title": "Sample spaces: tables and tree diagrams", "items": its}


# ============================================================ set 2: probability of two events
def set_two_events():
    its = []
    p = P(O_NC, lambda k, c: k == 3 and c == "red")
    assert F(1, 4) + F(1, 3) == F(7, 12)
    its.append(mcq(TAB_NC() + "What is the probability of 3 and red?", fr(1, 12), [fr(1, 7), fr(7, 12), fr(1, 4)],
                   "3R is 1 of the 12 equally likely outcomes: <b>" + fr(1, 12) + "</b>. " + fr(7, 12) + " adds "
                   + fr(1, 4) + " + " + fr(1, 3) + ". " + fr(1, 7) + " adds 4 + 3 outcomes.", ans=p))
    p = P(O_NC, lambda k, c: k % 2 == 0 and c == "blue")
    its.append(mcq(TAB_NC() + "What is the probability of an even number and blue?", fr(2, 12),
                   [fr(2, 7), fr(2, 4), fr(1, 12)],
                   "2B and 4B: 2 of 12 outcomes, so <b>" + fr(2, 12) + "</b> (= " + fr(1, 6) + "). "
                   + fr(2, 4) + " only looks at the number spinner.", ans=p))
    p = P(O_NC, lambda k, c: k < 4 and c != "green")
    its.append(mcq(TAB_NC() + "What is the probability of a number less than 4 and NOT green?", fr(6, 12),
                   [fr(3, 12), fr(6, 7), fr(8, 12)],
                   "1, 2 or 3 with red or blue: 3 × 2 = 6 of 12 outcomes, so <b>" + fr(6, 12) + "</b> (= " + fr(1, 2) + "). "
                   + fr(8, 12) + " counts every outcome that is not green, even with a 4.", ans=p))
    p = P(O_P, lambda a, b: a * b == 6)
    its.append(mcq(TAB_P() + "What is the probability that the product is 6?", fr(2, 16), [fr(1, 16), fr(2, 9), fr(6, 16)],
                   "2 × 3 and 3 × 2: 2 of 16 cells, so <b>" + fr(2, 16) + "</b> (= " + fr(1, 8) + "). " + fr(2, 9) +
                   " treats the 9 different products as equally likely. " + fr(6, 16) + " uses the product as the count.",
                   ans=p))
    p = P(O_P, lambda a, b: a * b % 2 == 0)
    assert len(set(a * b for a, b in O_P)) == 9 and len(set(a * b for a, b in O_P if a * b % 2 == 0)) == 6
    its.append(mcq(TAB_P() + "What is the probability that the product is even?", fr(12, 16),
                   [fr(4, 16), fr(8, 16), fr(6, 9)],
                   "Only odd × odd is odd (4 cells), so 16 − 4 = 12 cells are even: <b>".replace("−", M) + fr(12, 16) +
                   "</b> (= " + fr(3, 4) + "). " + fr(8, 16) + " guesses that half are even. " + fr(6, 9) +
                   " counts the different products, not the cells.", ans=p))
    p = P(O_P, lambda a, b: a * b > 8)
    its.append(mcq(TAB_P() + "What is the probability that the product is greater than 8?", fr(4, 16),
                   [fr(3, 16), fr(3, 9), fr(8, 16)],
                   "9, 12, 12 and 16: 4 of 16 cells, so <b>" + fr(4, 16) + "</b> (= " + fr(1, 4) + "). " + fr(3, 16) +
                   " counts 12 only once, but 3 × 4 and 4 × 3 are different outcomes.", ans=p))
    p = P(O36, lambda a, b: a + b == 8)
    its.append(mcq(TAB_S() + "You roll two number cubes. What is the probability that the sum is 8?", fr(5, 36),
                   [fr(1, 11), fr(3, 36), fr(8, 36)],
                   "2 + 6, 3 + 5, 4 + 4, 5 + 3, 6 + 2: 5 of 36 cells, so <b>" + fr(5, 36) + "</b>. " + fr(3, 36) +
                   " counts each pair in one order only. " + fr(1, 11) + " treats the 11 sums as equally likely.", ans=p))
    p = P(O36, lambda a, b: a + b < 5)
    its.append(mcq(TAB_S() + "What is the probability that the sum is less than 5?", fr(6, 36),
                   [fr(3, 11), fr(3, 36), fr(10, 36)],
                   "Sum 2: 1 cell, sum 3: 2 cells, sum 4: 3 cells. 1 + 2 + 3 = 6, so <b>" + fr(6, 36) + "</b> (= "
                   + fr(1, 6) + "). " + fr(10, 36) + " also counts the sum of 5, which is not less than 5.", ans=p))
    p = P(O36, lambda a, b: a > 4 and b > 4)
    its.append(mcq("You roll two number cubes. What is the probability that both numbers are greater than 4?",
                   fr(4, 36), [fr(2, 36), fr(4, 12), fr(2, 3)],
                   "Each cube has 2 numbers greater than 4 (5 and 6): 2 × 2 = 4 outcomes (5-5, 5-6, 6-5, 6-6), so <b>"
                   + fr(4, 36) + "</b> (= " + fr(1, 9) + "). " + fr(2, 36) + " counts only 5-5 and 6-6. " + fr(2, 3) +
                   " adds " + fr(1, 3) + " + " + fr(1, 3) + ".", ans=p))
    p = P(O_SC, lambda a, b: a == "A" and b == "H")
    its.append(mcq(TREE_SC() + "What is the probability of A and heads?", fr(1, 6), [fr(1, 5), fr(5, 6), fr(1, 3)],
                   "AH is 1 of the 6 outcomes: <b>" + fr(1, 6) + "</b>. " + fr(5, 6) + " adds " + fr(1, 3) + " + "
                   + fr(1, 2) + ". " + fr(1, 3) + " forgets the coin.", ans=p))
    p = P(O_SC, lambda a, b: a != "A" and b == "T")
    its.append(mcq(TREE_SC() + "What is the probability of NOT A and tails?", fr(2, 6), [fr(2, 5), fr(1, 6), fr(4, 6)],
                   "BT and CT: 2 of 6 outcomes, so <b>" + fr(2, 6) + "</b> (= " + fr(1, 3) + "). " + fr(4, 6) +
                   " counts every outcome that is not A, with heads too.", ans=p))
    O44 = outcomes(range(4), range(4))
    p = P(O44, lambda a, b: a != b)
    its.append(mcq("A spinner has 4 equal sections: red, blue, yellow and green. You spin it twice. "
                   "What is the probability of two different colours?", fr(12, 16),
                   [fr(4, 16), fr(1, 2), fr(6, 16)],
                   "Same colour happens in 4 of the 4 × 4 = 16 outcomes, so different colours happen in 12: <b>"
                   + fr(12, 16) + "</b> (= " + fr(3, 4) + "). " + fr(6, 16) + " counts red-blue but not blue-red.", ans=p))
    p = P(O12, lambda c, k: c == "H" or k == 6)
    its.append(mcq("You toss a coin and roll a number cube. What is the probability of heads OR a 6 (or both)?",
                   fr(7, 12), [fr(8, 12), fr(1, 12), fr(6, 12)],
                   "H1 to H6 is 6 outcomes, plus T6: 7 of 12, so <b>" + fr(7, 12) + "</b>. " + fr(8, 12) +
                   " counts H6 twice. " + fr(1, 12) + " is heads AND 6.", ans=p))
    its.append(mcq(TAB_NC() + "What is the probability of 4 and green, as a percent?", "about 8%",
                   ["about 58%", "12%", "25%"],
                   "4G is 1 of 12 outcomes: " + fr(1, 12) + " = 1 ÷ 12 ≈ 0.083, so <b>about 8%</b>. About 58% is "
                   + fr(7, 12) + ", from adding " + fr(1, 4) + " + " + fr(1, 3) + ". 12% just writes the 12 as a percent."))
    p = P(O36, lambda a, b: a + b in (7, 11))
    its.append(mcq(TAB_S() + "What is the probability that the sum is 7 or 11?", fr(8, 36),
                   [fr(2, 11), fr(6, 36), fr(4, 36)],
                   "Sum 7 is in 6 cells and sum 11 is in 2 cells (5 + 6, 6 + 5): 6 + 2 = 8, so <b>" + fr(8, 36) + "</b> (= "
                   + fr(2, 9) + "). " + fr(4, 36) + " counts each pair in one order only.", ans=p))
    p = P(O36, lambda a, b: a > b)
    its.append(mcq("You roll a red number cube and a blue number cube. What is the probability that the red number "
                   "is greater than the blue number?", fr(15, 36), [fr(18, 36), fr(21, 36), fr(6, 36)],
                   "36 outcomes, 6 of them are doubles. The other 30 split evenly: red greater in 15, blue greater in 15. "
                   "So <b>" + fr(15, 36) + "</b>. " + fr(18, 36) + " forgets the doubles. " + fr(21, 36) +
                   " includes the doubles. " + fr(6, 36) + " is the chance of doubles.", ans=p))
    O_RB = outcomes(range(4), range(4))
    p = P(O_RB, lambda a, b: a == b == 0)
    its.append(mcq("A jar has 4 marbles: red, blue, green and yellow. You take one, put it back and take another. "
                   "What is the probability of red both times?", fr(1, 16), [fr(2, 4), fr(1, 8), fr(1, 12)],
                   "Red, red is 1 of the 4 × 4 = 16 outcomes: <b>" + fr(1, 16) + "</b>. " + fr(2, 4) + " adds "
                   + fr(1, 4) + " + " + fr(1, 4) + ". " + fr(1, 12) + " forgets that the marble goes back.", ans=p))
    p = P(O_RB, lambda a, b: a == b)
    its.append(mcq("With the same jar (one marble of each colour, put back each time), what is the probability of the "
                   "same colour both times?", fr(4, 16), [fr(1, 16), fr(4, 8), fr(12, 16)],
                   "Red-red, blue-blue, green-green, yellow-yellow: 4 of 16, so <b>" + fr(4, 16) + "</b> (= " + fr(1, 4) +
                   "). " + fr(1, 16) + " counts only one colour. " + fr(12, 16) + " is the chance of different colours.",
                   ans=p))
    p = 1 - P(O_NC, lambda k, c: k == 1 and c == "red")
    its.append(mcq(TAB_NC() + "What is the probability of NOT getting 1 and red?", fr(11, 12),
                   [fr(1, 12), fr(3, 4), fr(2, 3)],
                   "1R is 1 of the 12 outcomes, so the other <b>" + fr(11, 12) + "</b> are not. " + fr(3, 4) +
                   " is the chance of not spinning 1. " + fr(2, 3) + " is the chance of not red.", ans=p))
    ps, pp = P(O36, lambda a, b: a + b == 6), P(O_P, lambda a, b: a * b == 4)
    assert ps == F(5, 36) and pp == F(3, 16) and pp > ps
    its.append(mcq("Which is more likely: a sum of 6 with two number cubes, or a product of 4 with two spinners "
                   "numbered 1 to 4?", "A product of 4 with the spinners",
                   ["A sum of 6 with the number cubes", "They are equally likely", "You can’t tell"],
                   "Sum of 6: 5 of 36 ≈ 0.14. Product of 4: 3 of 16 ≈ 0.19. 0.19 &gt; 0.14, so <b>a product of 4 with "
                   "the spinners</b> is more likely."))
    assert len(its) == 20
    return {"title": "Probability of two events", "items": its}


# ============================================================ set 3: multiply probabilities
def set_multiply():
    its = []
    its.append(mcq("A and B are independent. P(A) = " + fr(1, 2) + " and P(B) = " + fr(1, 5) + ". What is P(A and B)?",
                   fr(1, 10), [fr(7, 10), fr(1, 7), fr(2, 7)],
                   "Multiply: " + fr(1, 2) + " × " + fr(1, 5) + " = <b>" + fr(1, 10) + "</b>. " + fr(7, 10) + " adds. "
                   + fr(2, 7) + " adds the tops and the bottoms. " + fr(1, 7) + " adds the bottoms.",
                   ans=F(1, 2) * F(1, 5)))
    its.append(mcq("A and B are independent. P(A) = " + fr(2, 3) + " and P(B) = " + fr(3, 4) + ". What is P(A and B)?",
                   fr(1, 2), [fr(17, 12), fr(5, 7), fr(8, 9)],
                   fr(2, 3) + " × " + fr(3, 4) + " = " + fr(6, 12) + " = <b>" + fr(1, 2) + "</b>. " + fr(17, 12) +
                   " adds and is more than 1. " + fr(8, 9) + " cross-multiplies as if dividing.", ans=F(2, 3) * F(3, 4)))
    p = F(2, 3) * F(1, 2)
    its.append(mcq(SPIN_YG() + "You spin this spinner and toss a coin. What is P(yellow and tails)?", fr(2, 6),
                   [fr(7, 6), fr(1, 4), fr(3, 5)],
                   "P(yellow) = " + fr(2, 3) + " (2 of 3 equal sections). " + fr(2, 3) + " × " + fr(1, 2) + " = <b>"
                   + fr(2, 6) + "</b> (= " + fr(1, 3) + "). " + fr(1, 4) + " treats yellow and green as equally likely. "
                   + fr(7, 6) + " adds.", ans=p))
    its.append(mcq("A and B are independent. P(A) = 0.5 and P(B) = 0.7. What is P(A and B)?", "0.35",
                   ["1.2", "0.035", "3.5"],
                   "5 × 7 = 35, with two decimal places: 0.5 × 0.7 = <b>0.35</b>. 1.2 adds and is more than 1. "
                   "0.035 and 3.5 put the decimal point in the wrong place.", ans=F("0.5") * F("0.7")))
    its.append(mcq("A and B are independent. P(A) = 0.3 and P(B) = 0.3. What is P(A and B)?", "0.09",
                   ["0.9", "0.6", "0.03"],
                   "3 × 3 = 9, with two decimal places: 0.3 × 0.3 = <b>0.09</b>. 0.9 has only one decimal place. "
                   "0.6 adds.", ans=F("0.3") ** 2))
    its.append(mcq("A and B are independent. P(A) = 40% and P(B) = 25%. What is P(A and B)?", "10%",
                   ["65%", "1000%", "1%"],
                   "Change to decimals: 0.4 × 0.25 = 0.1 = <b>10%</b>. 65% adds. 1000% multiplies 40 × 25 without "
                   "changing to decimals.", ans=F("0.4") * F("0.25")))
    its.append(mcq(PT_FT() + "Ryan makes a free throw with probability 0.6. His shots are independent. "
                   "What is P(make, make)?", "0.36", ["1.2", "3.6", "0.6"],
                   "Multiply along the path: 0.6 × 0.6 = <b>0.36</b>. 1.2 adds. 0.6 is one shot only.",
                   ans=F("0.6") ** 2))
    its.append(mcq(PT_FT() + "What is P(miss, miss)?", "0.16", ["0.8", "0.08", "1.6"],
                   "0.4 × 0.4 = <b>0.16</b>. 0.8 adds. 0.08 forgets that 4 × 4 = 16.", ans=F("0.4") ** 2))
    p = F("0.6") * F("0.4") * 2
    its.append(mcq(PT_FT() + "What is the probability that Ryan makes exactly one of the two shots?", "0.48",
                   ["0.24", "1", "0.36"],
                   "Two paths work. Make, miss: 0.6 × 0.4 = 0.24. Miss, make: 0.4 × 0.6 = 0.24. Add the paths: "
                   "<b>0.48</b>. 0.24 uses only one path. 1 adds 0.6 + 0.4.", ans=p))
    its.append(mcq(PT_GW() + "A spinner lands on green with probability " + fr(1, 4) + " and on white with probability " + fr(3, 4) + ". You spin it twice. What is P(white, white)?", fr(9, 16),
                   [fr(6, 4), fr(6, 8), fr(1, 16)],
                   fr(3, 4) + " × " + fr(3, 4) + " = <b>" + fr(9, 16) + "</b>. " + fr(6, 4) + " adds and is more than 1. "
                   + fr(6, 8) + " adds the tops and the bottoms. " + fr(1, 16) + " is green, green.", ans=F(3, 4) ** 2))
    p = 1 - F(3, 4) ** 2
    assert p == F(7, 16) == F(1, 16) + 2 * F(3, 16)
    its.append(mcq(PT_GW() + "What is the probability of at least one green?", fr(7, 16),
                   [fr(2, 4), fr(1, 16), fr(6, 16)],
                   "Every outcome except white, white has a green: 1 − ".replace("−", M) + fr(9, 16) + " = <b>" + fr(7, 16) +
                   "</b>. " + fr(2, 4) + " adds " + fr(1, 4) + " + " + fr(1, 4) + ". " + fr(6, 16) +
                   " is exactly one green and forgets green, green.", ans=p))
    p = F(2, 5) * F(2, 5)
    its.append(mcq(BAGF() + "You take a marble, put it back, and take another. What is P(blue, blue)?", fr(4, 25),
                   [fr(4, 10), fr(2, 20), fr(4, 5)],
                   "The marble goes back, so P(blue) = " + fr(2, 5) + " both times. " + fr(2, 5) + " × " + fr(2, 5) +
                   " = <b>" + fr(4, 25) + "</b>. " + fr(2, 20) + " forgets to put the marble back (" + fr(2, 5) + " × "
                   + fr(1, 4) + "). " + fr(4, 5) + " adds.", ans=p))
    p = F(3, 5) * F(2, 5)
    its.append(mcq(BAGF() + "Same jar, the marble is put back. What is P(red, then blue)?", fr(6, 25),
                   [fr(5, 10), "1", fr(6, 20)],
                   fr(3, 5) + " × " + fr(2, 5) + " = <b>" + fr(6, 25) + "</b>. Adding " + fr(3, 5) + " + " + fr(2, 5) +
                   " = 1 would mean it is certain. " + fr(6, 20) + " forgets to put the marble back.", ans=p))
    p = F(3, 6) * F(1, 4)
    its.append(mcq("You roll a number cube and spin a spinner with 4 equal sections, one of them blue. "
                   "What is P(even number and blue)?", fr(1, 8), [fr(3, 4), fr(2, 6), fr(1, 2)],
                   "P(even) = " + fr(3, 6) + " = " + fr(1, 2) + " and P(blue) = " + fr(1, 4) + ". " + fr(1, 2) + " × "
                   + fr(1, 4) + " = <b>" + fr(1, 8) + "</b>. " + fr(3, 4) + " adds. " + fr(2, 6) +
                   " adds the tops and the bottoms.", ans=p))
    its.append(mcq("A and B are independent. P(A) = " + fr(1, 2) + " and P(A and B) = " + fr(1, 10) + ". What is P(B)?",
                   fr(1, 5), [fr(1, 20), fr(2, 5), fr(1, 8)],
                   "P(A) × P(B) = P(A and B), so P(B) = " + fr(1, 10) + " ÷ " + fr(1, 2) + " = <b>" + fr(1, 5) + "</b>. "
                   "Check: " + fr(1, 2) + " × " + fr(1, 5) + " = " + fr(1, 10) + ". " + fr(1, 20) +
                   " multiplies instead of dividing. " + fr(2, 5) + " subtracts.", ans=F(1, 10) / F(1, 2)))
    its.append(mcq("Two independent events each have a probability between 0 and 1. What is true about "
                   "P(A and B)?", "It is less than both P(A) and P(B)",
                   ["It is greater than both P(A) and P(B)", "It is always " + fr(1, 2), "It equals P(A) + P(B)"],
                   "Multiplying by a number less than 1 makes a number smaller. Both events happening is <b>less likely "
                   "than either one alone</b>. If your answer is bigger, you probably added."))
    p = F(3, 5) * F(1, 2)
    its.append(mcq("A spinner has 5 equal sections numbered 1 to 5. You spin it and toss a coin. "
                   "What is P(prime number and heads), as a decimal?", "0.3", ["1.1", "0.6", "0.03"],
                   "2, 3 and 5 are prime, so P(prime) = " + fr(3, 5) + " = 0.6. 0.6 × 0.5 = <b>0.3</b>. "
                   "1.1 adds. 0.6 forgets the coin.", ans=p))
    its.append(mcq("You roll two number cubes. What is P(6 on the first cube and an odd number on the second)?",
                   fr(1, 12), [fr(4, 6), fr(2, 8), fr(1, 6)],
                   fr(1, 6) + " × " + fr(3, 6) + " = " + fr(3, 36) + " = <b>" + fr(1, 12) + "</b>. " + fr(4, 6) +
                   " adds. " + fr(1, 6) + " forgets the second cube.", ans=F(1, 6) * F(1, 2)))
    its.append(mcq("A spinner has 10 equal sections numbered 1 to 10. You spin it twice. "
                   "What is the probability of 10 both times, as a percent?", "1%", ["20%", "10%", "0.1%"],
                   fr(1, 10) + " × " + fr(1, 10) + " = " + fr(1, 100) + " = <b>1%</b>. 20% adds 10% + 10%. "
                   "10% is one spin only.", ans=F(1, 100)))
    its.append(mcq("Zara says, “P(heads and 5) is " + fr(1, 2) + " + " + fr(1, 6) + " = " + fr(4, 6) + ".” "
                   "What is wrong?", "She should multiply: " + fr(1, 2) + " × " + fr(1, 6) + " = " + fr(1, 12),
                   ["Nothing, " + fr(4, 6) + " is right", "She should add the bottoms: " + fr(1, 8),
                    "She should subtract: " + fr(1, 2) + " " + M + " " + fr(1, 6) + " = " + fr(2, 6)],
                   "Both events must happen, so multiply: <b>" + fr(1, 12) + "</b>. H5 is 1 of the 2 × 6 = 12 outcomes. "
                   "Adding gives a bigger chance, but “both” should be less likely than one alone."))
    assert len(its) == 20
    return {"title": "Multiplying probabilities", "items": its}


# ============================================================ set 4: compare predictions
def set_predict():
    its = []
    assert F(1, 4) * 80 == 20
    its.append(mcq("You toss two coins 80 times. About how many times would you expect two heads?", "about 20",
                   ["about 40", "about 27", "about 60"],
                   "P(HH) = " + fr(1, 4) + ". " + fr(1, 4) + " of 80 = 80 ÷ 4 = <b>about 20</b>. About 27 uses "
                   + fr(1, 3) + ", as if HT and TH were one outcome. About 60 is NOT two heads."))
    assert F(1, 12) * 120 == 10
    its.append(mcq("You toss a coin and roll a number cube 120 times. About how many times would you expect "
                   "heads and a 6?", "about 10", ["about 80", "about 15", "about 20"],
                   "P(heads and 6) = " + fr(1, 12) + ". 120 ÷ 12 = <b>about 10</b>. About 80 uses " + fr(4, 6) +
                   " (adding). About 15 uses " + fr(1, 8) + " (adding 2 + 6 outcomes). About 20 forgets the coin."))
    assert F(3, 16) * 160 == 30
    its.append(mcq(TAB_P() + "You spin both spinners 160 times. About how many times would you expect a product of 4?",
                   "about 30", ["about 10", "about 18", "about 40"],
                   "P(product 4) = " + fr(3, 16) + ". 160 ÷ 16 = 10, and 10 × 3 = <b>about 30</b>. About 10 counts "
                   "only one cell. About 18 uses " + fr(1, 9) + ", treating the 9 products as equally likely."))
    its.append(mcq(T60() + "Ji-woo tossed two coins 60 times. What is the experimental probability of HH?", "0.3",
                   ["0.25", "0.18", "0.7"],
                   "HH came up 18 times in 60: " + fr(18, 60) + " = <b>0.3</b>. 0.25 is the theoretical probability. "
                   "0.18 uses the count as the decimal. 0.7 is NOT HH.", ans=F(18, 60)))
    assert F(1, 4) * 60 == 15
    its.append(mcq(T60() + "How many times does the theory predict HH in 60 tosses?", "15", ["18", "20", "30"],
                   fr(1, 4) + " of 60 = <b>15</b>. 18 is what actually happened. 20 uses " + fr(1, 3) +
                   ", as if there were only 3 outcomes.", ans=15))
    its.append(mcq(T60() + "Which statement about Ji-woo’s results is true?",
                   "They are close to the theory, as expected",
                   ["The coins must be unfair", "HH should have come up exactly 15 times",
                    "TT is now due to come up more often"],
                   "Results almost never match the theory exactly. 18 HH and 15 TT are close to the 15 predicted, so "
                   "<b>the results are close to the theory</b>. Coins have no memory, so nothing is “due”."))
    its.append(mcq("Four students toss two coins. Whose experimental probability of HH is most likely to be closest "
                   "to " + fr(1, 4) + "?", "Leah’s, with 1000 tosses",
                   ["Owen’s, with 40 tosses", "Mei’s, with 10 tosses", "Lucas’s, with 4 tosses"],
                   "More trials usually give an experimental probability closer to the theory, so <b>1000 tosses</b>."))
    its.append(mcq("Mei rolls two number cubes and gets doubles 3 times in a row. What is the probability of doubles "
                   "on her next roll?", fr(1, 6), [fr(1, 216), "0", fr(1, 2)],
                   "The cubes have no memory. Doubles is 6 of 36 outcomes on every roll: <b>" + fr(1, 6) + "</b>. "
                   + fr(1, 216) + " is the chance of 3 doubles in a row, worked out before any rolls.", ans=F(1, 6)))
    assert F(1, 12) > F(1, 16)
    its.append(mcq("Game A: you win on heads and a 6 (coin and number cube). Game B: you win if two spinners "
                   "numbered 1 to 4 both land on 4. Which game gives a better chance to win?", "Game A",
                   ["Game B", "They are the same", "You can’t tell"],
                   "Game A: " + fr(1, 2) + " × " + fr(1, 6) + " = " + fr(1, 12) + ". Game B: " + fr(1, 4) + " × " + fr(1, 4) +
                   " = " + fr(1, 16) + ". " + fr(1, 12) + " &gt; " + fr(1, 16) + ", so <b>Game A</b>."))
    pe = P(O_P, lambda a, b: a * b % 2 == 0)
    assert pe == F(3, 4)
    its.append(mcq(TAB_P() + "Hana wins if the product is even. Kai wins if it is odd. Is the game fair?",
                   "No, Hana wins " + fr(12, 16) + " of the time",
                   ["Yes, even and odd are equally likely", "No, Kai wins " + fr(12, 16) + " of the time",
                    "Yes, each player has 8 cells"],
                   "12 of the 16 cells are even and only 4 are odd. <b>Hana</b> is 3 times as likely to win, "
                   "so the game is not fair."))
    assert P(O36, lambda a, b: (a + b) % 2 == 0) == F(1, 2)
    its.append(mcq(TAB_S() + "Arjun wins if the sum of two number cubes is even. Nadia wins if it is odd. "
                   "Is the game fair?", "Yes, each has 18 of the 36 outcomes",
                   ["No, Arjun wins more: 6 of the 11 sums are even", "No, Nadia wins more: odd sums include 7",
                    "No, Arjun wins more: doubles are always even"],
                   "Count cells, not sums. 18 cells are even and 18 are odd, so <b>the game is fair</b>. The 11 sums "
                   "are not equally likely."))
    p = F(3, 4) * F(1, 2)
    assert p * 200 == 75
    its.append(mcq(fig(spinner_svg([("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")], R=56,
                                   label="spinner three quarters red one quarter blue")) +
                   "You spin this spinner and toss a coin 200 times. About how many times would you expect red and "
                   "heads?", "about 75", ["about 50", "about 100", "about 150"],
                   "P(red and heads) = " + fr(3, 4) + " × " + fr(1, 2) + " = " + fr(3, 8) + ". " + fr(3, 8) +
                   " of 200 = <b>about 75</b>. About 50 treats red and blue as equally likely. About 100 forgets the "
                   "spinner, and about 150 forgets the coin."))
    its.append(mcq("Two groups toss two coins. Group 1: 8 HH in 20 tosses (0.4). Group 2: 52 HH in 200 tosses (0.26). "
                   "Which result is the better estimate of P(HH)?", "Group 2, because it has more trials",
                   ["Group 1, because 0.4 is bigger", "Group 1, because it used fewer tosses",
                    "They are equally good estimates"],
                   "More trials give a more reliable estimate. 0.26 is also close to the theory, " + fr(1, 4) +
                   " = 0.25. So <b>Group 2</b>."))
    assert F(1, 12) * 600 == 50 and F(6, 50) * 600 == 72
    its.append(mcq("Simran spins two spinners 50 times. The outcome 3 and red came up 6 times. The theoretical "
                   "probability is " + fr(1, 12) + ". Using the theory, about how many times would you predict 3 and red "
                   "in 600 spins?", "about 50", ["about 72", "about 100", "about 12"],
                   fr(1, 12) + " of 600 = 600 ÷ 12 = <b>about 50</b>. About 72 uses her experimental result "
                   + fr(6, 50) + ", which is based on only 50 spins. About 100 uses " + fr(1, 6) + "."))
    assert F(1, 12) * 60 == 5
    its.append(mcq("You want to expect about 5 results of heads and a 6 (coin and number cube). About how many "
                   "turns do you need?", "about 60", ["about 30", "about 40", "about 10"],
                   "Heads and 6 happens " + fr(1, 12) + " of the time. 5 × 12 = <b>about 60</b> turns. About 40 uses "
                   + fr(1, 8) + " (adding 2 + 6 outcomes). About 30 forgets the coin."))
    assert round(F(1, 11) * 360) == 33 and F(6, 36) * 360 == 60
    its.append(mcq("Owen predicts a sum of 7 about 33 times in 360 rolls of two number cubes, because there are 11 sums. "
                   "Leah predicts about 60 times. Who is right?",
                   "Leah: " + fr(6, 36) + " of 360 = 60",
                   ["Owen: each sum is " + fr(1, 11), "Both, the numbers are close enough",
                    "Neither: it should be about 36"],
                   "The 11 sums are not equally likely. A sum of 7 is in 6 of the 36 cells, so " + fr(6, 36) +
                   " × 360 = 60. <b>Leah</b> is right."))
    p = P(O36, lambda a, b: a % 2 == 0 and b % 2 == 0)
    assert p == F(1, 4)
    its.append(mcq("In 100 rolls of two number cubes, both numbers were even 31 times. What is the theoretical "
                   "probability that both are even, as a percent?", "25%", ["31%", "50%", "9%"],
                   fr(1, 2) + " × " + fr(1, 2) + " = " + fr(1, 4) + " = <b>25%</b>. 31% is the experimental result. "
                   "50% is one cube only. 9% comes from the 9 even-even cells, but there are 36 cells, not 100.",
                   ans=p))
    its.append(mcq("Sofia tosses two coins. P(HH) was 0.27 after 100 tosses and 0.252 after 1000 tosses. What do you "
                   "expect after 10" + NB + "000 tosses?", "Close to 0.25",
                   ["Exactly 0.25", "About 0.234, because it keeps going down", "Close to 0.5"],
                   "With more trials the experimental probability gets <b>close to 0.25</b>, the theoretical value. "
                   "It is rarely exactly 0.25, and it does not keep moving in one direction."))
    assert F("0.36") * 50 == 18
    its.append(mcq("Ryan makes a free throw with probability 0.6, and his shots are independent. He goes to the line "
                   "for 2 shots 50 times. About how many times would you expect him to make both shots?",
                   "about 18", ["about 30", "about 60", "about 25"],
                   "P(make, make) = 0.6 × 0.6 = 0.36. 0.36 × 50 = <b>about 18</b>. About 30 uses 0.6 for one shot. "
                   "About 60 adds 0.6 + 0.6 = 1.2, which is more than every trip."))
    assert F(1, 4) * 100 == 25 and F(1, 6) * 120 == 20
    its.append(mcq("Which prediction is greater: two heads in 100 tosses of two coins, or doubles in 120 rolls of two "
                   "number cubes?", "Two heads: about 25",
                   ["Doubles: about 20", "They are equal", "Doubles: about 60"],
                   "Two heads: " + fr(1, 4) + " × 100 = 25. Doubles: " + fr(6, 36) + " × 120 = 20. "
                   "25 &gt; 20, so <b>two heads, about 25</b>."))
    assert len(its) == 20
    return {"title": "Comparing predictions and results", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []
    p = F(1, 4) * F(1, 3)
    its.append(mcq("On a BC Ferries sailing from Tsawwassen to Swartz Bay, Liam picks a meal at random from 4 meals "
                   "(one is fish and chips) and a drink at random from 3 (one is apple juice). What is the probability "
                   "of fish and chips with apple juice?", fr(1, 12), [fr(7, 12), fr(1, 7), fr(1, 4)],
                   "4 × 3 = 12 meal-and-drink outcomes, so <b>" + fr(1, 12) + "</b>. " + fr(7, 12) + " adds "
                   + fr(1, 4) + " + " + fr(1, 3) + ". " + fr(1, 4) + " forgets the drink.", ans=p))
    p = F(1, 3) * F(1, 5)
    its.append(mcq("A Grade 8 class in Vancouver draws its field trip at random: Stanley Park, Grouse Mountain or "
                   "Science World, on one of the 5 school days. What is the probability of Grouse Mountain on a Friday?",
                   fr(1, 15), [fr(8, 15), fr(1, 8), fr(1, 5)],
                   "3 places × 5 days = 15 outcomes: <b>" + fr(1, 15) + "</b>. " + fr(8, 15) + " adds " + fr(1, 3) +
                   " + " + fr(1, 5) + ". " + fr(1, 8) + " adds 3 + 5 outcomes.", ans=p))
    p = F("0.9") * F("0.8")
    its.append(mcq("Nadia takes a bus and then the SkyTrain to school. The bus is on time with probability 0.9 and the "
                   "SkyTrain with probability 0.8. Assume the two are independent. What is the probability that both "
                   "are on time?", "0.72", ["1.7", "0.072", "0.98"],
                   "0.9 × 0.8 = <b>0.72</b>. 1.7 adds and is more than 1. 0.072 has one decimal place too many. "
                   "0.98 is the chance that at least one is on time.", ans=p))
    p = F("0.7") ** 2
    its.append(mcq("In hockey, Noah scores on a shootout attempt with probability 0.3. His attempts are independent. "
                   "What is the probability that he misses two attempts in a row?", "0.49", ["1.4", "0.21", "0.09"],
                   "P(miss) = 1 − 0.3 = 0.7. 0.7 × 0.7 = <b>0.49</b>. 1.4 adds. 0.21 is score, then miss. "
                   "0.09 is scoring both.".replace("−", M), ans=p))
    p = F(1, 4) * F(1, 6)
    its.append(mcq("At Whistler, Ji-woo picks one of 4 chairlifts at random, then one of 6 runs from the top at random. "
                   "What is the probability that she picks one certain chairlift and one certain run?", fr(1, 24),
                   [fr(1, 10), fr(10, 24), fr(1, 6)],
                   "4 × 6 = 24 outcomes: <b>" + fr(1, 24) + "</b>. " + fr(1, 10) + " adds 4 + 6 outcomes. "
                   + fr(10, 24) + " adds " + fr(1, 4) + " + " + fr(1, 6) + ".", ans=p))
    p = P(O36, lambda a, b: a + b >= 9)
    assert p == F(10, 36) and cnt(O36, lambda a, b: a + b >= 9 and a <= b) == 6
    its.append(mcq("In a board game, Chloe needs a sum of 9 or more on two number cubes. What is the probability?",
                   fr(10, 36), [fr(4, 11), fr(6, 36), fr(4, 36)],
                   "Sum 9: 4 ways, 10: 3, 11: 2, 12: 1. 4 + 3 + 2 + 1 = 10 of 36, so <b>" + fr(10, 36) + "</b> (= "
                   + fr(5, 18) + "). " + fr(4, 11) + " treats the sums as equally likely. " + fr(6, 36) +
                   " counts each pair in one order only. " + fr(4, 36) + " is a sum of 9 only.", ans=p))
    p = F(1, 10) * F(1, 10)
    its.append(mcq("Mateo’s bike lock has 2 dials, each with the digits 0 to 9. He forgot the code and tries one "
                   "combination at random. What is the probability that it opens, as a percent?", "1%",
                   ["5%", "10%", "20%"],
                   "10 × 10 = 100 combinations, so " + fr(1, 100) + " = <b>1%</b>. 5% uses 10 + 10 = 20 outcomes. "
                   "20% adds 10% + 10%.", ans=p))
    p = F(1, 2) * F(2, 6)
    assert p * 180 == 30 and (F(1, 2) + F(1, 3)) * 180 == 150
    its.append(mcq("Sofia’s fun fair game: a player wins on heads and a number greater than 4 on a number cube. "
                   "She expects 180 players. About how many prizes should she bring?", "about 30",
                   ["about 90", "about 60", "about 150"],
                   "P(win) = " + fr(1, 2) + " × " + fr(2, 6) + " = " + fr(1, 6) + ". 180 ÷ 6 = <b>about 30</b>. "
                   "About 150 adds " + fr(1, 2) + " + " + fr(1, 3) + ". About 90 forgets the cube, and about 60 forgets the coin."))
    p = F(1, 25) ** 2
    its.append(mcq("A Burnaby class of 25 draws one name each day for 2 days to pick the class helper. The name goes "
                   "back in after each draw. What is the probability that Zara is picked both days?", fr(1, 625),
                   [fr(2, 25), fr(1, 50), fr(1, 600)],
                   fr(1, 25) + " × " + fr(1, 25) + " = <b>" + fr(1, 625) + "</b>. " + fr(2, 25) + " adds. "
                   + fr(1, 50) + " uses 25 + 25 outcomes. " + fr(1, 600) + " forgets that the name goes back in.", ans=p))
    p = 1 - F(24, 25) ** 2
    assert p == F(49, 625) and 2 * F(1, 25) * F(24, 25) == F(48, 625)
    its.append(mcq("Same draw: what is the probability that Zara is picked on at least one of the 2 days?", fr(49, 625),
                   [fr(2, 25), fr(1, 625), fr(48, 625)],
                   "Not picked both days: " + fr(24, 25) + " × " + fr(24, 25) + " = " + fr(576, 625) + ". At least once: "
                   "1 − ".replace("−", M) + fr(576, 625) + " = <b>" + fr(49, 625) + "</b>. " + fr(2, 25) + " (= " + fr(50, 625) +
                   ") counts picked-both-days twice. " + fr(48, 625) + " is exactly one day.", ans=p))
    p = F(1, 4) ** 2
    its.append(mcq("Owen guesses two multiple-choice questions, each with 4 choices. What is the probability that he "
                   "gets both right, as a percent?", "6.25%", ["50%", "12.5%", "25%"],
                   fr(1, 4) + " × " + fr(1, 4) + " = " + fr(1, 16) + " = 0.0625 = <b>6.25%</b>. 50% adds 25% + 25%. "
                   "12.5% uses 4 + 4 = 8 outcomes. 25% is one question.", ans=p))
    p = F(3, 4) ** 2
    its.append(mcq("Same two guesses: what is the probability that Owen gets both wrong?", fr(9, 16),
                   [fr(6, 4), fr(3, 16), fr(6, 8)],
                   "P(wrong) = " + fr(3, 4) + " for each. " + fr(3, 4) + " × " + fr(3, 4) + " = <b>" + fr(9, 16) + "</b>. "
                   + fr(6, 4) + " adds. " + fr(3, 16) + " is right, then wrong.", ans=p))
    p = F("0.8") ** 2
    its.append(mcq("A whale-watching tour from Victoria sees orcas on a trip with probability 0.8. Assume trips are "
                   "independent. Leah goes on 2 trips. What is the probability she sees orcas on both?", "0.64",
                   ["1.6", "0.16", "6.4"],
                   "0.8 × 0.8 = <b>0.64</b>. 1.6 adds. 0.16 is orcas on the first trip but not the second.", ans=p))
    p = F(2, 3) * F(1, 4)
    its.append(mcq("On a hike in the Okanagan, Zara picks one of 3 trails at random and one of 4 snacks at random. "
                   "What is the probability that she does NOT pick the lake trail but does pick granola?", fr(2, 12),
                   [fr(1, 12), fr(11, 12), fr(3, 7)],
                   "P(not lake trail) = " + fr(2, 3) + " and P(granola) = " + fr(1, 4) + ". " + fr(2, 3) + " × " + fr(1, 4) +
                   " = <b>" + fr(2, 12) + "</b> (= " + fr(1, 6) + "). " + fr(1, 12) + " is the lake trail with granola.",
                   ans=p))
    assert F(1, 2) * F(1, 5) == F(1, 10) and F(1, 2) * F(1, 6) == F(1, 12)
    its.append(mcq("Kai wants a fun fair game with a " + fr(1, 10) + " chance of winning. Which game works?",
                   "Heads on a coin and 5 on a spinner numbered 1 to 5",
                   ["Heads on a coin and 6 on a number cube", "Heads on two coins", "1 or 2 on a number cube"],
                   fr(1, 2) + " × " + fr(1, 5) + " = <b>" + fr(1, 10) + "</b>. The others are " + fr(1, 12) + ", "
                   + fr(1, 4) + " and " + fr(1, 3) + "."))
    assert F(1, 10) * 250 == 25 and (F(1, 2) + F(1, 5)) * 250 == 175
    its.append(mcq("Kai expects 250 players at his game with a " + fr(1, 10) + " chance of winning. About how many "
                   "prizes should he bring?", "about 25", ["about 125", "about 175", "about 50"],
                   fr(1, 10) + " of 250 = <b>about 25</b>. About 175 adds " + fr(1, 2) + " + " + fr(1, 5) + ". "
                   "About 125 uses the coin only, and about 50 uses the spinner only."))
    p = F(3, 9)
    its.append(mcq("Nadia’s soccer team picks a jersey colour at random (red, white or blue) and a sock colour at "
                   "random (red, white or blue). What is the probability that the jersey and socks match?", fr(3, 9),
                   [fr(1, 9), fr(6, 9), fr(3, 6)],
                   "3 × 3 = 9 outcomes, and 3 of them match: <b>" + fr(3, 9) + "</b> (= " + fr(1, 3) + "). "
                   + fr(1, 9) + " counts one colour only. " + fr(3, 6) + " adds 3 + 3 outcomes.",
                   ans=P(outcomes("RWB", "RWB"), lambda a, b: a == b)))
    p = F(1, 15) * F(1, 12)
    assert F(1, 15) + F(1, 12) == F(3, 20)
    its.append(mcq("Two lacrosse teams in Coquitlam each pick a captain at random. Team A has 15 players (Lucas is one). "
                   "Team B has 12 players (Emma is one). What is the probability that Lucas and Emma are both picked?",
                   fr(1, 180), [fr(3, 20), fr(1, 27), fr(2, 27)],
                   fr(1, 15) + " × " + fr(1, 12) + " = <b>" + fr(1, 180) + "</b>. " + fr(3, 20) + " adds. " + fr(1, 27) +
                   " adds 15 + 12 players. " + fr(2, 27) + " adds the tops and the bottoms.", ans=p))
    its.append(mcq("A game uses a coin and a spinner with equal sections, one of them green. P(heads and green) = "
                   + fr(1, 12) + ". How many sections does the spinner have?", "6", ["12", "10", "24"],
                   fr(1, 2) + " × " + fr(1, 6) + " = " + fr(1, 12) + ", so <b>6</b> sections (2 × 6 = 12 outcomes). "
                   "12 forgets the coin. 10 subtracts 12 − 2.".replace("−", M), ans=6))
    assert F(1, 4) * 60 == 15 and F(1, 6) * 60 == 10
    its.append(mcq("Ryan can play Game A (win on two heads with two coins) or Game B (win on tails and a 5 or 6 on a "
                   "number cube). Which game should give more wins in 60 turns, and about how many?",
                   "Game A: about 15", ["Game B: about 10", "Game B: about 20", "Game A: about 30"],
                   "Game A: " + fr(1, 4) + " × 60 = 15. Game B: " + fr(1, 2) + " × " + fr(2, 6) + " = " + fr(1, 6) +
                   ", and " + fr(1, 6) + " × 60 = 10. So <b>Game A, about 15</b>. About 20 forgets the coin in Game B."))
    assert len(its) == 20
    return {"title": "Word problems: games, sports and trips", "items": its}


# ============================================================ lesson
def body_html():
    tree = tree_svg([["A", "B", "C"], ["H", "T"]], ["Spinner", "Coin"], label="tree diagram spinner A B C then coin")
    tab = grid_svg("", ["1", "2", "3", "4"], ["red", "blue", "green"], lambda r, c: r + INIT[c], "Colour spinner",
                   label="outcome table number spinner 1 to 4 and colour spinner")
    pt = ptree_svg(FT, FT, label="probability tree two free throws", h1="First shot", h2="Second shot")
    return (
        "<h2>Independent events and sample spaces</h2>"
        "<p>Two events are <b>independent</b> when one does not change the chance of the other. A coin cannot change "
        "how a spinner lands. Taking a marble and NOT putting it back changes the jar, so those picks are not "
        "independent.</p>"
        "<p>The <b>sample space</b> is the list of all outcomes. Show it with a tree diagram or a table. "
        "Count the outcomes by <b>multiplying</b>: a 3-section spinner and a coin give 3 × 2 = 6 outcomes.</p>"
        "<figure class='sn-fig'>" + tree +
        "<figcaption>Each spinner branch splits into heads and tails: 6 outcomes.</figcaption></figure>"
        "<figure class='sn-fig'>" + tab +
        "<figcaption>A number spinner and a colour spinner: 4 × 3 = 12 outcomes.</figcaption></figure>"
        + ex("Example 1", "You spin both spinners in the table. What is P(even number and blue)?",
             "2B and 4B are 2 of the 12 equally likely outcomes.", fr(2, 12) + " = " + fr(1, 6))
        + "<h2>Multiply the probabilities</h2>"
        "<p>For independent events, <b>P(A and B) = P(A) × P(B)</b>. This works even when the outcomes are not equally "
        "likely. On a probability tree, multiply along each path. If more than one path works, add those paths.</p>"
        + ex("Example 2", "You roll a number cube and toss a coin. What is P(5 or 6, and heads)?",
             "P(5 or 6) = " + fr(2, 6) + " and P(heads) = " + fr(1, 2) + ". " + fr(2, 6) + " × " + fr(1, 2) + " = "
             + fr(2, 12) + ".", fr(2, 12) + " = " + fr(1, 6))
        + "<figure class='sn-fig'>" + pt +
        "<figcaption>Ryan makes a free throw with probability 0.6.</figcaption></figure>"
        + ex("Example 3", "What is the probability that Ryan makes exactly one of two free throws?",
             "Make, miss: 0.6 × 0.4 = 0.24. Miss, make: 0.4 × 0.6 = 0.24. Add the two paths.", "0.48")
        + "<h2>Making predictions</h2>"
        "<p>Expected number = probability × number of trials. Real results are usually close to the prediction, "
        "but rarely exactly the same. <b>More trials usually get closer.</b></p>"
        + ex("Example 4", "You toss a coin and roll a number cube 120 times. About how many times would you expect "
             "heads and a 6?", "P(heads and 6) = " + fr(1, 12) + ". " + fr(1, 12) + " of 120 = 120 ÷ 12 = 10.",
             "about 10")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["P(heads and 6) = " + fr(1, 2) + " + " + fr(1, 6) + " = " + fr(4, 6),
             "“And” for independent events: multiply. " + fr(1, 2) + " × " + fr(1, 6) + " = " + fr(1, 12) + "."],
            ["A 4-section and a 3-section spinner give 4 + 3 = 7 outcomes.", "Multiply: 4 × 3 = 12 outcomes."],
            [fr(1, 2) + " and " + fr(1, 5) + " give " + fr(2, 7) + ".", "Multiply the tops and the bottoms: "
             + fr(1, 10) + "."],
            ["0.3 × 0.3 = 0.9", "Count the decimal places: 0.3 × 0.3 = 0.09."],
            ["Product of 4 on two 1–4 spinners: only 1 × 4 and 2 × 2.", "4 × 1 is a different outcome: 3 cells."],
            ["“Doubles came up 3 times, so they are less likely now.”", "Cubes have no memory. It is still "
             + fr(1, 6) + "."],
        ])
    )


FAQ = [
    {"q": "What are independent events in Grade 8 math?",
     "a": "Two events are independent when the result of one does not change the chance of the other, like tossing a coin and rolling a number cube. Taking two marbles from a bag without putting the first one back is not independent."},
    {"q": "How do you find the probability of two independent events?",
     "a": "Multiply the two probabilities: P(A and B) = P(A) × P(B). For heads and a 6, 1/2 × 1/6 = 1/12. You can check by counting the outcomes in a table or tree diagram."},
    {"q": "Why do you multiply probabilities instead of adding them?",
     "a": "Both events must happen, so the chance is smaller than either one alone. Adding gives a bigger number, like 1/2 + 1/6 = 4/6, and can even go over 1."},
    {"q": "How do you use probability to make a prediction?",
     "a": "Multiply the probability by the number of trials. With a 1/12 chance and 120 turns, expect about 10 results; real results are usually close but rarely exact."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (tables, tree diagrams, probability trees)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(58813)
    sets = [set_sample_spaces(), set_two_events(), set_multiply(), set_predict(), set_words()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "probability-of-two-independent-events",
        "sort": 13, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Probability of Two Independent Events",
        "seo_title": "Grade 8 Probability of Two Independent Events Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Probability of two independent events",
        "domain": "Data and probability",
        "standard_code": "Grade 8: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Theoretical probability with two independent events",
        "meta_desc": "Free Grade 8 math worksheets on the probability of two independent events for the BC curriculum: sample spaces with tables and tree diagrams, multiplying probabilities as fractions, decimals and percents, probability trees, and predictions compared with results. 100 questions with an answer key.",
        "key_big": "For two independent events, multiply: P(A and B) = P(A) × P(B).",
        "key_sub": "A coin and a number cube give 2 × 6 = 12 outcomes, so P(heads and 6) = 1/2 × 1/6 = 1/12, not 1/2 + 1/6. Expected count = probability × number of trials.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(tree diagram|outcome table|probability tree|results table)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
