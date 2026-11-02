# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Probability with Venn and Tree Diagrams
(Ontario Curriculum 2020, Grade 8: D2.1 Venn and tree diagrams, D2.2 multiple independent events,
theoretical and experimental probability)
  python3 tools/gen_caon_math_g8_probability.py
Venn diagrams with counts (and, or, neither, only one), tree diagrams for two and three events, probability
trees with branch probabilities, the multiplication rule for independent events (fractions, decimals, percents),
experimental vs theoretical probability (three coins, pooled class results, predictions) and word problems in
Ontario contexts (Terry Fox Run, canoe trip in Algonquin, ringette, bike locks, school raffles, fall fair).
Wrong answers come from real student mistakes: adding instead of multiplying (1/2 + 1/6), adding the outcomes
(2 + 6 = 8), double counting the overlap of a Venn diagram (13 + 15 = 28), forgetting the "neither" region,
dividing by the wrong total, counting only one order (green-white but not white-green), decimal place errors
(0.3 × 0.3 = 0.9), treating 0, 1, 2, 3 heads as equally likely and the gambler's fallacy.
Helpers (probability tree, tables) are adapted from gen_cabc_math_g7_probability.py and
gen_caon_math_g7_probability.py. Every answer is checked in code with fractions.Fraction.
Canadian English. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
GREEN = "#006633"
BLUE = "#2f5f9e"
HEAD = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
M = "−"


# ------------------------------------------------------------ helpers
def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


def frf(x):
    x = F(x)
    return fr(x.numerator, x.denominator)


FRX = re.compile(r"<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>")


def val(s):
    """Numeric value of a choice (fraction, decimal, percentage or whole number), or None for words."""
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
def venn_svg(title, la, lb, a, ab, b, n, label):
    """Venn diagram with counts: a = A only, ab = both, b = B only, n = neither (in the corner of the box)."""
    W, r, d = 320, 58, 72
    cx1, cx2 = W / 2 - d / 2, W / 2 + d / 2
    cy = 64 + r
    H = cy + r + 26
    assert tw(title, 15) <= W - 8, title
    xla, xlb = cx1 - 34, cx2 + 34
    assert xla - tw(la, 15) / 2 >= 12 and xlb + tw(lb, 15) / 2 <= W - 12, (la, lb)
    assert xla + tw(la, 15) / 2 + 8 <= xlb - tw(lb, 15) / 2, (la, lb)
    s = [text(W / 2, 18, title, 15),
         "<rect x='4' y='28' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (W - 8, H - 32, LINE),
         "<circle cx='%.1f' cy='%d' r='%d' fill='#cfe8d8' fill-opacity='0.6' stroke='%s' stroke-width='2'/>" % (cx1, cy, r, GREEN),
         "<circle cx='%.1f' cy='%d' r='%d' fill='#d6e2f0' fill-opacity='0.6' stroke='%s' stroke-width='2'/>" % (cx2, cy, r, BLUE),
         text(xla, 54, la, 15, col=GREEN), text(xlb, 54, lb, 15, col=BLUE),
         text(cx1 - 28, cy + 6, str(a), 18), text(W / 2, cy + 6, str(ab), 18), text(cx2 + 28, cy + 6, str(b), 18),
         text(W - 26, H - 14, str(n), 18)]
    for v in (a, ab, b, n):
        assert tw(str(v), 18) <= 26, v
    return svg_wrap(W, int(H), "".join(s), label)


def tree_svg(levels, heads, label="tree diagram"):
    """Tree diagram for 2 or 3 events, each level a list of short labels; outcomes listed on the right."""
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
    s.append("<circle cx='%d' cy='%.1f' r='4' fill='%s'/>" % (xr, top + nleaf * gap / 2, LINE))
    outs = []

    def node(level, prefix, i0, px, py):
        under = 1
        for lv in levels[level + 1:]:
            under *= len(lv)
        for j, t in enumerate(levels[level]):
            a = i0 + j * under
            y = top + (a + under / 2) * gap
            w = colw[level]
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (px, py, xs[level] - tw(t, 16) / 2 - 5, y, THIN))
            s.append(text(xs[level], y + 6, t, 16, col=GREEN if level == 0 else LINE))
            if level + 1 < len(levels):
                node(level + 1, prefix + [t], a, xs[level] + tw(t, 16) / 2 + 5, y)
            else:
                o = joint.join(prefix + [t])
                outs.append(o)
                s.append(text(xo, y + 5, o, 15, anchor="start", weight=400))
            del w

    node(0, [], 0, xr, top + nleaf * gap / 2)
    W = int(max(xo + max(tw(o, 15, False) for o in outs) + 8, xo + tw("Outcome", 14) + 8))
    return svg_wrap(W, int(H), "".join(s), label)


def ptree_svg(first, second, label="probability tree", h1="First spin", h2="Second spin"):
    """Probability tree for two independent events. first, second: [(name, 'p')]. The same second branches
    come out of every first branch. Each branch is a slant then a short flat part; p sits above the flat part."""
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


def P(space, cond):
    return F(sum(1 for o in space if cond(o)), len(space))


# ------------------------------------------------------------ data
# Venn diagrams: (A only, both, B only, neither)
V1 = (8, 5, 10, 7)        # hockey / soccer, 30 students
V2 = (14, 6, 9, 11)       # dog / cat, 40 students
V4 = (18, 12, 9, 11)      # skating / skiing, 50 students
NUMS = range(1, 21)
assert sum(V1) == 30 and sum(V2) == 40 and sum(V4) == 50


def VEN1():
    return fig(venn_svg("A Grade 8 class: 30 students", "Hockey", "Soccer", *V1,
                        label="Venn diagram hockey and soccer 30 students"))


def VEN2():
    return fig(venn_svg("Pets survey: 40 students", "Has a dog", "Has a cat", *V2,
                        label="Venn diagram dog and cat 40 students"))


def VEN3():
    a = sum(1 for k in NUMS if k % 2 == 0 and k % 3)
    ab = sum(1 for k in NUMS if k % 6 == 0)
    b = sum(1 for k in NUMS if k % 3 == 0 and k % 2)
    n = 20 - a - ab - b
    return fig(venn_svg("The whole numbers 1 to 20", "Multiple of 2", "Multiple of 3", a, ab, b, n,
                        label="Venn diagram multiples of 2 and 3 from 1 to 20"))


def VEN4():
    return fig(venn_svg("Winter sports: 50 students", "Skating", "Skiing", *V4,
                        label="Venn diagram skating and skiing 50 students"))


C3 = list(product("HT", repeat=3))


def TREE3():
    return fig(tree_svg([["H", "T"]] * 3, ["Coin 1", "Coin 2", "Coin 3"], label="tree diagram three coins"))


def TREE_CS():
    return fig(tree_svg([["H", "T"], ["red", "blue", "yellow", "green"]], ["Coin", "Spinner"],
                        label="tree diagram coin then spinner with 4 colours"))


GW = [("green", "1/3"), ("white", "2/3")]
FT = [("make", "0.7"), ("miss", "0.3")]


def PT_GW():
    return fig(ptree_svg(GW, GW, label="probability tree spinner green and white spun twice"))


def PT_FT():
    return fig(ptree_svg(FT, FT, label="probability tree two free throws", h1="First shot", h2="Second shot"))


# ============================================================ set 1: Venn diagrams
def set_venn():
    its = []
    a, ab, b, n = V1
    t = sum(V1)
    its.append(mcq(VEN1() + "How many students play hockey?", str(a + ab), [str(a), str(a + b), str(ab)],
                   "Count the whole hockey circle: the 8 who play only hockey plus the 5 in the overlap: 8 + 5 = <b>13</b>. "
                   "8 is only the part of the circle outside the overlap.", ans=a + ab))
    its.append(mcq(VEN1() + "A student is chosen at random. What is the probability that the student plays both sports?",
                   fr(ab, t), [fr(ab, t - n), fr(a + ab, t), fr(ab, a + ab)],
                   "5 students are in the overlap, out of all 30: <b>" + fr(5, 30) + "</b> (= " + fr(1, 6) + "). "
                   + fr(5, 23) + " leaves out the 7 students outside the circles, but they are part of the class too.",
                   ans=F(ab, t)))
    its.append(mcq(VEN1() + "What is the probability that the student plays hockey or soccer (or both)?",
                   fr(a + ab + b, t), [fr(2 * ab + a + b, t), fr(a + b, t), fr(n, t)],
                   "Add the three regions inside the circles: 8 + 5 + 10 = 23, so <b>" + fr(23, 30) + "</b>. "
                   "Adding the circle totals, 13 + 15 = 28, counts the 5 students in the overlap twice.",
                   ans=F(a + ab + b, t)))
    its.append(mcq(VEN1() + "What is the probability that the student plays neither sport?", fr(n, t),
                   [fr(n, t - n), fr(a + ab + b, t), fr(a + b, t)],
                   "7 students are outside both circles: <b>" + fr(7, 30) + "</b>. " + fr(7, 23) +
                   " divides by the wrong total. " + fr(23, 30) + " is the chance of at least one sport.", ans=F(n, t)))
    its.append(mcq(VEN1() + "What is the probability that the student plays exactly one of the two sports?",
                   fr(a + b, t), [fr(a + ab + b, t), fr(a + ab, t), fr(b, t)],
                   "Exactly one means hockey only or soccer only: 8 + 10 = 18, so <b>" + fr(18, 30) + "</b> (= " + fr(3, 5) +
                   "). " + fr(23, 30) + " also counts the 5 who play both.", ans=F(a + b, t)))
    its.append(mcq(VEN1() + "What is the probability that the student plays soccer but not hockey?", fr(b, t),
                   [fr(b + ab, t), fr(ab, t), fr(b, t - n)],
                   "Soccer but not hockey is the soccer circle outside the overlap: 10 students, so <b>" + fr(10, 30) +
                   "</b> (= " + fr(1, 3) + "). " + fr(15, 30) + " includes the 5 who also play hockey.", ans=F(b, t)))
    a, ab, b, n = V2
    t = sum(V2)
    its.append(mcq(VEN2() + "A student from the survey is chosen at random. What is the probability that the student "
                   "has a dog?", fr(a + ab, t), [fr(a, t), fr(a + ab + b, t), fr(a + ab, a + ab + b)],
                   "The dog circle holds 14 + 6 = 20 students: " + fr(20, 40) + " = <b>" + fr(1, 2) + "</b>. "
                   + fr(14, 40) + " forgets the 6 who have a dog and a cat.", ans=F(a + ab, t)))
    its.append(mcq(VEN2() + "What is the probability that the student has a dog and a cat?", fr(ab, t),
                   [fr(ab, a + ab + b), fr(a + 2 * ab + b, t), fr(a + ab + b, t)],
                   "“And” means the overlap: 6 of 40 students, so <b>" + fr(6, 40) + "</b> (= " + fr(3, 20) + "). "
                   + fr(29, 40) + " is “dog or cat”.", ans=F(ab, t)))
    its.append(mcq(VEN2() + "What is the probability that the student has a dog or a cat (or both)?", fr(a + ab + b, t),
                   [fr(a + 2 * ab + b, t), fr(a + b, t), fr(n, t)],
                   "14 + 6 + 9 = 29 students are inside the circles: <b>" + fr(29, 40) + "</b>. "
                   "20 dog owners + 15 cat owners = 35 counts the 6 in the overlap twice.", ans=F(a + ab + b, t)))
    its.append(mcq(VEN2() + "What is the probability that the student has neither a dog nor a cat, as a percent?",
                   "27.5%", ["11%", "72.5%", "37.9%"],
                   "11 of 40 students are outside both circles: 11 ÷ 40 = 0.275 = <b>27.5%</b>. "
                   "11% uses the count as the percent. 37.9% divides by 29 instead of 40.", ans=F(n, t)))
    its.append(mcq(VEN3() + "Where does the number 12 belong in this Venn diagram?", "In the overlap",
                   ["In “Multiple of 2” only", "In “Multiple of 3” only", "Outside both circles"],
                   "12 = 2 × 6 and 12 = 3 × 4, so 12 is a multiple of 2 and of 3. It goes <b>in the overlap</b>."))
    u = P(list(NUMS), lambda k: k % 2 == 0 or k % 3 == 0)
    assert u == F(13, 20)
    its.append(mcq(VEN3() + "A number from 1 to 20 is chosen at random. What is the probability that it is a multiple "
                   "of 2 or a multiple of 3?", fr(13, 20), [fr(16, 20), fr(10, 20), fr(7, 20)],
                   "Inside the circles: 7 + 3 + 3 = 13 numbers, so <b>" + fr(13, 20) + "</b>. " + fr(16, 20) +
                   " adds the 10 multiples of 2 and the 6 multiples of 3, so 6, 12 and 18 are counted twice.", ans=u))
    p = P(list(NUMS), lambda k: k % 6 == 0)
    assert p == F(3, 20) and F(1, 2) * F(1, 3) == F(1, 6)
    its.append(mcq(VEN3() + "What is the probability that the number is a multiple of 2 and a multiple of 3?",
                   fr(3, 20), [fr(1, 6), fr(3, 13), fr(16, 20)],
                   "The overlap holds 6, 12 and 18: <b>" + fr(3, 20) + "</b>. " + fr(1, 6) + " uses " + fr(1, 2) + " × "
                   + fr(1, 3) + ", but only 6 of these 20 numbers are multiples of 3, not one third of them. "
                   "Counting the overlap is safest.",
                   ans=p))
    t, A, B, ab = 28, 15, 10, 4
    n = t - (A + B - ab)
    assert n == 7
    its.append(mcq("In a class of 28 students, 15 take French club, 10 play in the band and 4 do both. "
                   "How many students do neither?", str(n), [str(t - A - B), str(A + B - ab), str(ab)],
                   "French or band: 15 + 10 − 4 = 21 students (subtract the 4 so they are counted once). "
                   "28 − 21 = <b>7</b>. 28 − 15 − 10 = 3 counts the 4 students who do both twice.".replace("−", M),
                   ans=n))
    its.append(mcq("In the same class of 28, a student is chosen at random. What is the probability that the student "
                   "does neither French club nor band?", fr(n, t), [fr(3, t), fr(21, t), fr(n, 21)],
                   "7 of the 28 students do neither: <b>" + fr(7, 28) + "</b> (= " + fr(1, 4) + "). " + fr(3, 28) +
                   " comes from forgetting to subtract the overlap.", ans=F(n, t)))
    its.append(mcq("Of 32 students, 18 have visited Toronto, 12 have visited Ottawa and 6 have visited both. "
                   "What is the probability that a random student has visited at least one of the two cities?",
                   fr(24, 32), [fr(30, 32), fr(18, 32), fr(8, 32)],
                   "18 + 12 − 6 = 24 students, so <b>".replace("−", M) + fr(24, 32) + "</b> (= " + fr(3, 4) + "). "
                   + fr(30, 32) + " counts the 6 who visited both cities twice. " + fr(8, 32) + " is the chance of neither.",
                   ans=F(24, 32)))
    a, ab, b, n = V4
    t = sum(V4)
    its.append(mcq(VEN4() + "A student is chosen at random. What is the probability that the student skates, "
                   "as a decimal?", "0.6", ["0.36", "0.78", "0.3"],
                   "The skating circle holds 18 + 12 = 30 students: 30 ÷ 50 = <b>0.6</b>. 0.36 uses only the 18 "
                   "outside the overlap. 0.78 is skating or skiing.", ans=F(a + ab, t)))
    its.append(mcq(VEN4() + "What is the probability that the student skis but does not skate, as a percent?", "18%",
                   ["9%", "42%", "22%"],
                   "Skiing only: 9 students out of 50 = 9 ÷ 50 = <b>18%</b>. 9% uses the count as the percent. "
                   "42% is everyone who skis (21). 22% is neither.", ans=F(b, t)))
    its.append(mcq(VEN4() + "What is the probability that the student does both, as a decimal?", "0.24",
                   ["0.12", "0.48", "0.3"],
                   "12 students are in the overlap: 12 ÷ 50 = <b>0.24</b>. 0.12 uses the count as the decimal. "
                   "0.48 counts the overlap twice (24).", ans=F(ab, t)))
    t, a, b, n = 30, 9, 8, 6
    ab = t - a - b - n
    assert ab == 7
    its.append(mcq("A Venn diagram shows 30 students. 9 are in circle A only, 8 are in circle B only and 6 are "
                   "outside both circles. How many students are in the overlap?", str(ab),
                   [str(t - a - b), str(t - a - n), str(a + b)],
                   "All four regions add to 30: 30 − 9 − 8 − 6 = <b>7</b>. 13 forgets the 6 students outside the "
                   "circles. 17 just adds 9 + 8.".replace("−", M), ans=ab))
    assert len(its) == 20
    return {"title": "Venn diagrams and probability", "items": its}


# ============================================================ set 2: tree diagrams
def set_trees():
    its = []
    its.append(mcq(TREE3() + "You toss three coins. How many outcomes does the tree diagram show?", "8",
                   ["6", "4", "9"],
                   "Each branch splits in 2 at every coin: 2 × 2 × 2 = <b>8</b>. 6 comes from adding 2 + 2 + 2. "
                   "4 stops after two coins.", ans=len(C3)))
    p = P(C3, lambda o: o == ("H", "H", "H"))
    its.append(mcq(TREE3() + "What is the probability of three heads?", fr(1, 8), [fr(1, 6), fr(3, 2), fr(3, 8)],
                   "HHH is 1 of the 8 equally likely outcomes: <b>" + fr(1, 8) + "</b>. " + fr(3, 2) + " adds "
                   + fr(1, 2) + " + " + fr(1, 2) + " + " + fr(1, 2) + ", which is more than 1. " + fr(1, 6) +
                   " adds 2 + 2 + 2 outcomes.", ans=p))
    p = P(C3, lambda o: o.count("H") == 2)
    its.append(mcq(TREE3() + "What is the probability of exactly two heads?", fr(3, 8), [fr(1, 8), fr(2, 8), fr(3, 6)],
                   "HHT, HTH and THH: 3 of 8 outcomes, so <b>" + fr(3, 8) + "</b>. " + fr(1, 8) +
                   " counts only HHT; the tail can be on any of the three coins.", ans=p))
    p = P(C3, lambda o: "H" in o)
    its.append(mcq(TREE3() + "What is the probability of at least one head?", fr(7, 8), [fr(1, 8), fr(4, 8), fr(3, 4)],
                   "Only TTT has no heads, so 8 − 1 = 7 outcomes have at least one: <b>".replace("−", M) + fr(7, 8) +
                   "</b>. " + fr(4, 8) + " counts only the outcomes that start with H. " + fr(3, 4) +
                   " is the answer for two coins.", ans=p))
    n = sum(1 for o in C3 if o.count("T") == 1)
    its.append(mcq(TREE3() + "How many outcomes have exactly one tail?", str(n), ["1", "2", "4"],
                   "HHT, HTH and THH: <b>3</b> outcomes. The tail can be on coin 1, coin 2 or coin 3.", ans=n))
    p = P(C3, lambda o: len(set(o)) == 1)
    its.append(mcq(TREE3() + "What is the probability that all three coins show the same face?", fr(2, 8),
                   [fr(1, 8), fr(2, 6), fr(3, 8)],
                   "HHH and TTT: 2 of 8 outcomes, so <b>" + fr(2, 8) + "</b> (= " + fr(1, 4) + "). "
                   + fr(1, 8) + " counts only HHH.", ans=p))
    CS = list(product("HT", ["red", "blue", "yellow", "green"]))
    n = sum(1 for c, _ in CS if c == "T")
    its.append(mcq(TREE_CS() + "How many outcomes in this tree diagram start with T?", str(n), ["8", "2", "1"],
                   "Four branches come out of T, one for each colour: <b>4</b> outcomes. 8 is the whole tree.", ans=n))
    p = P(CS, lambda o: o == ("H", "green"))
    its.append(mcq(TREE_CS() + "What is the probability of heads and green?", fr(1, 8),
                   [fr(1, 6), fr(3, 4), fr(1, 4)],
                   "H, green is 1 of the 2 × 4 = 8 outcomes: <b>" + fr(1, 8) + "</b>. " + fr(3, 4) + " adds "
                   + fr(1, 2) + " + " + fr(1, 4) + ". " + fr(1, 6) + " adds 2 + 4 outcomes.", ans=p))
    g, w = F(1, 3), F(2, 3)
    its.append(mcq(PT_GW() + "A spinner is green with probability " + fr(1, 3) + " and white with probability "
                   + fr(2, 3) + ". You spin it twice. What is P(green, green)?", fr(1, 9),
                   [fr(2, 3), fr(1, 3), fr(2, 9)],
                   "Multiply along the branches: " + fr(1, 3) + " × " + fr(1, 3) + " = <b>" + fr(1, 9) + "</b>. "
                   + fr(2, 3) + " adds the branches. " + fr(2, 9) + " is P(green, white).", ans=g * g))
    its.append(mcq(PT_GW() + "What is P(white, white)?", fr(4, 9), [fr(4, 3), fr(2, 3), fr(2, 9)],
                   fr(2, 3) + " × " + fr(2, 3) + " = <b>" + fr(4, 9) + "</b>. " + fr(4, 3) + " adds " + fr(2, 3) + " + "
                   + fr(2, 3) + ", which is more than 1. " + fr(2, 3) + " looks at one spin only.", ans=w * w))
    its.append(mcq(PT_GW() + "What is the probability of one green and one white, in either order?", fr(4, 9),
                   [fr(2, 9), "1", fr(5, 9)],
                   "Green, white: " + fr(1, 3) + " × " + fr(2, 3) + " = " + fr(2, 9) + ". White, green: " + fr(2, 3) + " × "
                   + fr(1, 3) + " = " + fr(2, 9) + ". Add the two paths: <b>" + fr(4, 9) + "</b>. " + fr(2, 9) +
                   " counts only one order. " + fr(5, 9) + " is the chance of at least one green.", ans=2 * g * w))
    assert g * g + g * w + w * g + w * w == 1
    its.append(mcq(PT_GW() + "What do the probabilities of all four outcomes add up to?", "1",
                   ["4", fr(4, 9), "2"],
                   fr(1, 9) + " + " + fr(2, 9) + " + " + fr(2, 9) + " + " + fr(4, 9) + " = " + fr(9, 9) + " = <b>1</b>. "
                   "One of the four outcomes is certain to happen.", ans=1))
    mk = F(7, 10)
    its.append(mcq(PT_FT() + "Kai makes a free throw with probability 0.7, and each shot is independent. "
                   "What is the probability that he makes both shots?", "0.49", ["1.4", "0.7", "0.21"],
                   "Multiply along the make, make path: 0.7 × 0.7 = <b>0.49</b>. 1.4 adds the branches. "
                   "0.21 is P(make, miss).", ans=mk * mk))
    its.append(mcq(PT_FT() + "What is the probability that Kai misses both shots?", "0.09", ["0.6", "0.9", "0.3"],
                   "0.3 × 0.3 = <b>0.09</b>. 0.9 is a decimal place mistake: 3 × 3 = 9, and there are two decimal "
                   "places in all. 0.6 adds 0.3 + 0.3.", ans=(1 - mk) ** 2))
    its.append(mcq(PT_FT() + "What is the probability that Kai makes exactly one of the two shots?", "0.42",
                   ["0.21", "1", "0.51"],
                   "Make, miss: 0.7 × 0.3 = 0.21. Miss, make: 0.3 × 0.7 = 0.21. Together: <b>0.42</b>. "
                   "0.21 counts only one order. 0.51 = 1 − 0.49 is “not both”, which also includes missing both.".replace("−", M),
                   ans=2 * mk * (1 - mk)))
    its.append(mcq("You toss a coin, roll a number cube and toss another coin. How many outcomes are there?", "24",
                   ["10", "12", "14"],
                   "Multiply the choices at each step: 2 × 6 × 2 = <b>24</b>. 10 adds 2 + 6 + 2. 12 forgets the second "
                   "coin.", ans=len(list(product("HT", range(1, 7), "HT")))))
    sp = list(product("HT", "HT", range(1, 7)))
    p = P(sp, lambda o: o == ("H", "H", 6))
    its.append(mcq("You toss two coins and roll a number cube. What is the probability of heads, heads and a 6?",
                   fr(1, 24), [fr(1, 10), fr(7, 6), fr(1, 12)],
                   fr(1, 2) + " × " + fr(1, 2) + " × " + fr(1, 6) + " = <b>" + fr(1, 24) + "</b> (2 × 2 × 6 = 24 outcomes). "
                   + fr(7, 6) + " adds the probabilities. " + fr(1, 12) + " forgets one coin.", ans=p))
    sp = list(product(range(1, 5), repeat=3))
    p = P(sp, lambda o: o == (1, 1, 1))
    its.append(mcq("A spinner has 4 equal sections numbered 1 to 4. You spin it three times. What is the probability "
                   "of getting 1 all three times?", fr(1, 64), [fr(1, 12), fr(3, 4), fr(1, 16)],
                   "4 × 4 × 4 = 64 outcomes and only 1, 1, 1 works: <b>" + fr(1, 64) + "</b>. " + fr(1, 12) +
                   " adds 4 + 4 + 4. " + fr(3, 4) + " adds " + fr(1, 4) + " three times. " + fr(1, 16) + " stops after two spins.",
                   ans=p))
    its.append(mcq("Leah draws a tree diagram for tossing two coins and then spinning a spinner with 3 colours. "
                   "How many branches end on the right of her tree?", "12", ["7", "6", "8"],
                   "Every final branch is one outcome: 2 × 2 × 3 = <b>12</b>. 7 adds 2 + 2 + 3. 6 forgets one coin.",
                   ans=12))
    its.append(mcq("Ethan says, “The probability of three heads is " + fr(1, 2) + " + " + fr(1, 2) + " + " + fr(1, 2) +
                   " = " + fr(3, 2) + ".” What is wrong?",
                   "He should multiply: " + fr(1, 2) + " × " + fr(1, 2) + " × " + fr(1, 2) + " = " + fr(1, 8),
                   ["Nothing, " + fr(3, 2) + " is right", "He should use " + fr(1, 3) + " for each coin",
                    "He should add the denominators: " + fr(1, 6)],
                   "A probability can never be more than 1. For independent events, multiply: <b>" + fr(1, 8) +
                   "</b>, which matches 1 path out of the 8 in a tree diagram."))
    assert len(its) == 20
    return {"title": "Tree diagrams for two and three events", "items": its}


# ============================================================ set 3: multiplying probabilities
def set_multiply():
    its = []
    its.append(mcq("A and B are independent. P(A) = " + fr(1, 2) + " and P(B) = " + fr(1, 3) + ". What is P(A and B)?",
                   fr(1, 6), [fr(5, 6), fr(2, 5), fr(1, 5)],
                   "Multiply: " + fr(1, 2) + " × " + fr(1, 3) + " = <b>" + fr(1, 6) + "</b>. " + fr(5, 6) + " adds the "
                   "probabilities. " + fr(2, 5) + " adds the tops and the bottoms.", ans=F(1, 2) * F(1, 3)))
    its.append(mcq("A and B are independent. P(A) = " + fr(2, 5) + " and P(B) = " + fr(3, 4) + ". What is P(A and B)?",
                   fr(6, 20), [fr(23, 20), fr(5, 9), fr(6, 9)],
                   fr(2, 5) + " × " + fr(3, 4) + " = <b>" + fr(6, 20) + "</b> (= " + fr(3, 10) + "). " + fr(23, 20) +
                   " adds and is more than 1. " + fr(6, 9) + " multiplies the tops but adds the bottoms.",
                   ans=F(2, 5) * F(3, 4)))
    its.append(mcq("A and B are independent. P(A) = " + fr(3, 8) + " and P(B) = " + fr(2, 3) + ". What is P(A and B)?",
                   fr(1, 4), [fr(25, 24), fr(5, 11), fr(6, 11)],
                   fr(3, 8) + " × " + fr(2, 3) + " = " + fr(6, 24) + " = <b>" + fr(1, 4) + "</b>. " + fr(25, 24) +
                   " adds the probabilities. " + fr(5, 11) + " adds the tops and the bottoms.", ans=F(3, 8) * F(2, 3)))
    its.append(mcq("A and B are independent. P(A) = 0.4 and P(B) = 0.5. What is P(A and B)?", "0.2",
                   ["0.9", "0.02", "0.1"],
                   "0.4 × 0.5 = <b>0.2</b>. 0.9 adds. 0.02 puts the decimal point in the wrong place.",
                   ans=F("0.4") * F("0.5")))
    its.append(mcq("A and B are independent. P(A) = 0.3 and P(B) = 0.6. What is P(A and B)?", "0.18",
                   ["0.9", "1.8", "0.018"],
                   "3 × 6 = 18, and there are two decimal places in all: 0.3 × 0.6 = <b>0.18</b>. 0.9 adds.",
                   ans=F("0.3") * F("0.6")))
    its.append(mcq("A and B are independent. P(A) = 50% and P(B) = 20%. What is P(A and B)?", "10%",
                   ["70%", "30%", "1%"],
                   "Change to decimals: 0.5 × 0.2 = 0.1 = <b>10%</b>. 70% adds. 1% multiplies 50 × 20 = 1000 and then "
                   "misplaces the decimal point.", ans=F(1, 10)))
    its.append(mcq("A and B are independent. P(A) = 60% and P(B) = 50%. What is P(A and B)?", "30%",
                   ["110%", "55%", "3%"],
                   "0.6 × 0.5 = 0.3 = <b>30%</b>. 110% adds, and no probability is more than 100%. "
                   "55% is the average, not the product.", ans=F(3, 10)))
    p = F(1, 2) * F(2, 6)
    its.append(mcq("You toss a coin and roll a number cube. What is the probability of tails and a number greater "
                   "than 4?", fr(2, 12), [fr(5, 6), fr(2, 8), fr(1, 12)],
                   "P(tails) = " + fr(1, 2) + " and P(5 or 6) = " + fr(2, 6) + ". " + fr(1, 2) + " × " + fr(2, 6) + " = <b>"
                   + fr(2, 12) + "</b> (= " + fr(1, 6) + "). " + fr(1, 12) + " counts only the 5 or only the 6.", ans=p))
    p = F(3, 5) * F(1, 6)
    its.append(mcq("A spinner has 5 equal sections: 2 blue and 3 yellow. You spin it and roll a number cube. "
                   "What is P(yellow and 1)?", fr(3, 30), [fr(23, 30), fr(1, 30), fr(3, 11)],
                   "P(yellow) = " + fr(3, 5) + " and P(1) = " + fr(1, 6) + ". " + fr(3, 5) + " × " + fr(1, 6) + " = <b>"
                   + fr(3, 30) + "</b> (= " + fr(1, 10) + "). " + fr(1, 30) + " uses only one yellow section. "
                   + fr(23, 30) + " adds.", ans=p))
    p = F(1, 2) * F(1, 2) * F(1, 4)
    its.append(mcq("You toss two coins and spin a spinner with 4 equal sections. What is P(heads, heads, red), "
                   "if one section is red?", fr(1, 16), [fr(5, 4), fr(1, 8), fr(1, 4)],
                   fr(1, 2) + " × " + fr(1, 2) + " × " + fr(1, 4) + " = <b>" + fr(1, 16) + "</b>. " + fr(1, 8) +
                   " forgets one coin. " + fr(5, 4) + " adds.", ans=p))
    its.append(mcq("You toss a coin 4 times. What is the probability of 4 heads?", fr(1, 16),
                   [fr(1, 8), fr(1, 4), fr(1, 2)],
                   fr(1, 2) + " × " + fr(1, 2) + " × " + fr(1, 2) + " × " + fr(1, 2) + " = <b>" + fr(1, 16) + "</b>, "
                   "since 2<sup>4</sup> = 16. " + fr(1, 8) + " uses 2 × 4 instead of 2<sup>4</sup>.",
                   ans=F(1, 2) ** 4))
    its.append(mcq("Three traffic lights work on their own timers. Each is green with probability 0.5 when you get "
                   "there. What is the probability that all three are green?", "0.125", ["1.5", "0.25", "0.5"],
                   "0.5 × 0.5 × 0.5 = <b>0.125</b>. 1.5 adds. 0.25 stops after two lights. 0.5 is one light.",
                   ans=F(1, 2) ** 3))
    pr, ps = F("0.2"), F("0.3")
    its.append(mcq("The chance of rain is 0.2 on Saturday and 0.3 on Sunday. The days are independent. "
                   "What is the probability of rain on both days?", "0.06", ["0.5", "0.6", "0.1"],
                   "0.2 × 0.3 = <b>0.06</b>. 0.5 adds. 0.6 puts the decimal point in the wrong place: 2 × 3 = 6, "
                   "with two decimal places.", ans=pr * ps))
    its.append(mcq("With the same forecast (0.2 on Saturday, 0.3 on Sunday), what is the probability of no rain on "
                   "either day?", "0.56", ["0.5", "0.06", "1.5"],
                   "No rain: 1 − 0.2 = 0.8 and 1 − 0.3 = 0.7. Multiply: 0.8 × 0.7 = <b>0.56</b>. "
                   "0.5 is 1 − 0.2 − 0.3, which does not handle the two days correctly.".replace("−", M),
                   ans=(1 - pr) * (1 - ps)))
    p = F(3, 4) * F(1, 2)
    its.append(mcq("A spinner is red with probability " + fr(1, 4) + ". You spin it and toss a coin. "
                   "What is P(not red and heads)?", fr(3, 8), [fr(1, 8), fr(5, 4), fr(3, 4)],
                   "P(not red) = 1 − ".replace("−", M) + fr(1, 4) + " = " + fr(3, 4) + ". " + fr(3, 4) + " × " + fr(1, 2) +
                   " = <b>" + fr(3, 8) + "</b>. " + fr(1, 8) + " is P(red and heads). " + fr(5, 4) + " adds.", ans=p))
    its.append(mcq("A and B are independent. P(A) = " + fr(1, 3) + " and P(A and B) = " + fr(1, 12) + ". What is P(B)?",
                   fr(1, 4), [fr(1, 36), fr(5, 12), fr(2, 3)],
                   "P(A) × P(B) = P(A and B), so " + fr(1, 3) + " × P(B) = " + fr(1, 12) + ". P(B) = " + fr(1, 12) + " ÷ "
                   + fr(1, 3) + " = <b>" + fr(1, 4) + "</b>. Check: " + fr(1, 3) + " × " + fr(1, 4) + " = " + fr(1, 12) + ". "
                   + fr(1, 36) + " multiplies instead of dividing.", ans=F(1, 12) / F(1, 3)))
    its.append(mcq("A and B are independent. P(A) = 0.6 and P(A and B) = 0.24. What is P(B)?", "0.4",
                   ["0.144", "0.36", "0.84"],
                   "0.6 × P(B) = 0.24, so P(B) = 0.24 ÷ 0.6 = <b>0.4</b>. 0.144 multiplies 0.6 × 0.24. "
                   "0.36 subtracts.", ans=F("0.24") / F("0.6")))
    its.append(mcq("Which pair of events is independent?", "Tossing a coin and rolling a number cube",
                   ["Drawing two names from a hat without putting the first back",
                    "Choosing a class president, then a vice-president from the others",
                    "A big snowstorm tonight and school buses cancelled tomorrow"],
                   "The coin cannot change how the number cube lands, so <b>a coin and a number cube</b> are independent. "
                   "In the other pairs, the first event changes the chance of the second."))
    its.append(mcq("Which pair of events is NOT independent?",
                   "Taking two marbles from a bag without putting the first back",
                   ["Spinning the same spinner twice", "Rolling two number cubes", "Tossing a coin and spinning a spinner"],
                   "If the first marble is not put back, the bag has changed, so the chance for the second marble changes. "
                   "Those events are <b>not independent</b>. Spinners, coins and number cubes have no memory."))
    its.append(mcq("Zoe says, “P(6 and 6) with two number cubes is " + fr(1, 6) + " + " + fr(1, 6) + " = " + fr(2, 6) +
                   ".” What is wrong?",
                   "She should multiply: " + fr(1, 6) + " × " + fr(1, 6) + " = " + fr(1, 36),
                   ["Nothing, " + fr(2, 6) + " is right", "She should add the denominators: " + fr(1, 12),
                    "She should subtract: " + fr(1, 6) + " − ".replace("−", M) + fr(1, 6) + " = 0"],
                   "Both events must happen, so multiply: <b>" + fr(1, 36) + "</b>. 6 and 6 is 1 of the 6 × 6 = 36 "
                   "outcomes. Adding makes the chance bigger, but “both” should be less likely than one alone."))
    assert len(its) == 20
    return {"title": "Multiplying probabilities of independent events", "items": its}


# ============================================================ set 4: experimental vs theoretical
HEADS3 = [17, 64, 58, 21]
GROUPS = [["A", "40", "9"], ["B", "40", "13"], ["C", "40", "10"], ["D", "40", "8"]]


def T160():
    return fig(table_svg("Three coins tossed 160 times", ["Number of heads", "0", "1", "2", "3"],
                         [["Frequency"] + [str(v) for v in HEADS3]], label="frequency table three coins 160 tosses"))


def TGROUP():
    return fig(table_svg("Three coins: all the same face", ["Group", "Trials", "All the same"], GROUPS,
                         label="results table four groups"))


def set_exp():
    assert sum(HEADS3) == 160 and sum(int(g[2]) for g in GROUPS) == 40
    theo = [P(C3, lambda o, k=k: o.count("H") == k) for k in range(4)]
    assert theo == [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
    its = []
    its.append(mcq("Mei tosses three coins 80 times and gets three heads 12 times. What is the experimental probability "
                   "of three heads, as a decimal?", "0.15", ["0.125", "0.12", "0.85"],
                   "12 ÷ 80 = <b>0.15</b>. 0.125 is the theoretical probability, " + fr(1, 8) + ". "
                   "0.12 uses the count as the decimal. 0.85 is NOT three heads.", ans=F(12, 80)))
    its.append(mcq("Mei tosses three coins 80 times. How many times does theory predict three heads?", "10",
                   ["12", "20", "40"],
                   "P(HHH) = " + fr(1, 8) + ", and " + fr(1, 8) + " of 80 = <b>10</b>. 12 is what Mei actually got. "
                   "20 uses " + fr(1, 4) + ", as if 0, 1, 2 and 3 heads were equally likely. 40 uses " + fr(1, 2) + ".", ans=F(1, 8) * 80))
    its.append(mcq(T160() + "What is the experimental probability of exactly 2 heads?", fr(58, 160),
                   [fr(3, 8), fr(58, 102), fr(1, 4)],
                   "2 heads happened 58 times in 160 trials: <b>" + fr(58, 160) + "</b>. " + fr(3, 8) +
                   " is the theory. " + fr(1, 4) + " treats 0, 1, 2 and 3 heads as equally likely.", ans=F(58, 160)))
    its.append(mcq(T160() + "What is the theoretical probability of exactly 1 head?", fr(3, 8),
                   [fr(1, 4), fr(64, 160), fr(1, 8)],
                   "HTT, THT and TTH are 3 of the 8 outcomes: <b>" + fr(3, 8) + "</b>. " + fr(1, 4) + " treats the four "
                   "results 0, 1, 2, 3 as equally likely, but they are not. " + fr(64, 160) + " is the experimental "
                   "probability.", ans=theo[1]))
    its.append(mcq(T160() + "How many times does theory predict 3 heads in 160 tosses?", "20", ["40", "21", "53"],
                   fr(1, 8) + " of 160 = 160 ÷ 8 = <b>20</b>. 40 uses " + fr(1, 4) + " (four equally likely results). "
                   "21 is what happened.", ans=theo[3] * 160))
    exp = [theo[k] * 160 for k in range(4)]
    diff = [abs(HEADS3[k] - exp[k]) for k in range(4)]
    assert exp == [20, 60, 60, 20] and diff == [3, 4, 2, 1] and diff.index(max(diff)) == 1
    its.append(mcq(T160() + "Theory predicts 20, 60, 60 and 20. Which result is furthest from the theory?",
                   "1 head", ["0 heads", "2 heads", "3 heads"],
                   "Differences: 0 heads: 20 − 17 = 3; 1 head: 64 − 60 = 4; 2 heads: 60 − 58 = 2; 3 heads: 21 − 20 = 1. "
                   "The biggest difference is for <b>1 head</b>.".replace("−", M)))
    its.append(mcq(TGROUP() + "Four groups each tossed three coins 40 times. Use all the results together. "
                   "What is the experimental probability that all three coins show the same face?", fr(40, 160),
                   [fr(9, 40), fr(40, 40), fr(10, 160)],
                   "Add: 9 + 13 + 10 + 8 = 40 in 4 × 40 = 160 trials: <b>" + fr(40, 160) + "</b> (= " + fr(1, 4) + "). "
                   + fr(9, 40) + " uses group A only.", ans=F(40, 160)))
    th = F(2, 8)
    gp = {g[0]: F(int(g[2]), 40) for g in GROUPS}
    far = max(gp, key=lambda k: abs(gp[k] - th))
    assert far == "B" and [k for k in gp if gp[k] == th] == ["C"]
    its.append(mcq(TGROUP() + "The theoretical probability is " + fr(2, 8) + " = 0.25. Which group’s result is "
                   "furthest from the theory?", "Group B", ["Group A", "Group C", "Group D"],
                   "A: 9 ÷ 40 = 0.225, B: 13 ÷ 40 = 0.325, C: 10 ÷ 40 = 0.25, D: 8 ÷ 40 = 0.2. "
                   "<b>Group B</b> is 0.075 away, the most."))
    its.append(mcq(TGROUP() + "Why is the class result (all 160 trials) a better estimate than one group’s result?",
                   "More trials usually give a result closer to the theory",
                   ["Group results are always wrong", "160 trials always match the theory exactly",
                    "The groups used different coins"],
                   "With only 40 trials, chance moves the result a lot (from 0.2 to 0.325 here). "
                   "<b>More trials usually give a result closer to the theory</b>, but not exactly."))
    its.append(mcq("Three fair coins landed TTT the last 3 times. What is the probability of TTT on the next toss?",
                   fr(1, 8), [fr(1, 2), "0", fr(1, 16)],
                   "Coins have no memory. Each toss of three coins is a new trial, so P(TTT) is still <b>" + fr(1, 8) +
                   "</b>. Thinking it is now less likely is the gambler’s fallacy.", ans=F(1, 8)))
    its.append(mcq("A spinner has 4 equal sections, one red. It lands on red 410 times in 1000 spins. What do the "
                   "results suggest?", "The spinner is probably not fair",
                   ["The spinner is fair", "1000 spins are too few to tell", "Red will now come up less often"],
                   "Theory: " + fr(1, 4) + " of 1000 = 250. 410 is far from 250 after many spins, so <b>the spinner is "
                   "probably not fair</b>."))
    its.append(mcq("Amira tosses two coins 4 times and never gets HH. Does this prove the coins are unfair?",
                   "No, 4 trials are too few to tell",
                   ["Yes, HH should come up once in 4 tosses", "Yes, the probability of HH is 0",
                    "No, HH is impossible with two coins"],
                   "P(no HH in one toss) = " + fr(3, 4) + ", so getting no HH in 4 tosses happens fairly often. "
                   "<b>4 trials are too few to tell.</b>"))
    its.append(mcq("Which of these is a theoretical probability?", "P(two heads) = " + fr(1, 4) +
                   " because HH is 1 of 4 outcomes",
                   ["Liam got HH 11 times in 40 tosses", "Our class got HH 26% of the time",
                    "A computer simulation gave 0.249"],
                   "A theoretical probability comes from counting equally likely outcomes, not from trials. "
                   "The other three come from experiments."))
    its.append(mcq("Why do you need an experiment to find the probability that a thumbtack lands point up?",
                   "Its two ways of landing are not equally likely",
                   ["A thumbtack has only one way to land", "The probability must be " + fr(1, 2),
                    "Thumbtacks can’t be tossed more than once"],
                   "You can only count outcomes when they are equally likely. Point up and point down are "
                   "<b>not equally likely</b>, so you toss it many times and use the results."))
    pf = F(42, 60)
    assert pf == F("0.7")
    its.append(mcq("Nathan makes 42 of 60 free throws. Use his experimental probability to estimate the probability "
                   "that he makes his next two free throws.", "0.49", ["1.4", "0.7", "0.21"],
                   "42 ÷ 60 = 0.7. If the shots are independent: 0.7 × 0.7 = <b>0.49</b>. 1.4 adds. "
                   "0.7 is one shot only.", ans=pf * pf))
    its.append(mcq("You roll two number cubes 72 times. How many doubles does theory predict?", "12",
                   ["6", "2", "36"],
                   "P(doubles) = " + fr(6, 36) + " = " + fr(1, 6) + ". " + fr(1, 6) + " of 72 = <b>12</b>. "
                   "6 uses " + fr(1, 12) + " (adding 6 + 6 outcomes). 2 counts only one double, 6 and 6.",
                   ans=F(6, 36) * 72))
    its.append(mcq("After 200 spins, the experimental probability of red is 0.32. How many times did the spinner land "
                   "on red?", "64", ["32", "136", "625"],
                   "0.32 × 200 = <b>64</b>. 136 is the spins that were NOT red. 625 divides 200 by 0.32.",
                   ans=F("0.32") * 200))
    late = F(6, 40)
    assert late * 20 == 3
    its.append(mcq("Ava’s school bus was late on 6 of the last 40 school days. Use this to predict how many of the next "
                   "20 school days it will be late.", "3", ["6", "14", "12"],
                   "Experimental probability: " + fr(6, 40) + " = 0.15. 0.15 × 20 = <b>3</b>. "
                   "20 days is half of 40, so expect about half of 6. 12 doubles instead of halving.",
                   ans=late * 20))
    its.append(mcq("A computer simulates rolling two number cubes 10" + NB + "000 times. The sum is 7 in 1671 rolls. "
                   "How does this compare with the theory?", "Very close: theory predicts about 1667",
                   ["Far off: theory predicts about 909", "Far off: theory predicts about 833",
                    "Exactly right: theory predicts 1671"],
                   "P(sum of 7) = " + fr(6, 36) + " = " + fr(1, 6) + ". 10" + NB + "000 ÷ 6 ≈ 1667, so 1671 is "
                   "<b>very close</b>. About 909 treats the 11 sums as equally likely. About 833 uses " + fr(1, 12) + " (adding 6 + 6 outcomes)."))
    its.append(mcq("A game is fair in theory, with a " + fr(1, 2) + " chance to win. Jayden plays 100 times and wins 46. "
                   "What is the best conclusion?", "46 is close to 50, so the results fit the theory",
                   ["He should have won exactly 50 times", "The game is unfair", "He will win the next 4 games"],
                   "Theory predicts about 50 wins. Results vary a little from the theory by chance, and "
                   "<b>46 is close to 50</b>."))
    assert len(its) == 20
    return {"title": "Experimental vs theoretical probability", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []
    t, run, skate, both = 120, 64, 38, 22
    u = run + skate - both
    assert u == 80 and (run - both) + (skate - both) == 58
    its.append(mcq("Of 120 Grade 8 students at a Mississauga school, 64 did the Terry Fox Run, 38 went on the "
                   "skating trip and 22 did both. What is the probability that a random student did at least one?",
                   fr(u, t), [fr(run + skate, t), fr(58, t), fr(t - u, t)],
                   "64 + 38 − 22 = 80 students, so <b>".replace("−", M) + fr(80, 120) + "</b> (= " + fr(2, 3) + "). "
                   + fr(102, 120) + " counts the 22 students who did both twice. " + fr(58, 120) + " is exactly one.",
                   ans=F(u, t)))
    its.append(mcq("Of the same 120 students (64 Terry Fox Run, 38 skating trip, 22 both), what is the probability "
                   "that a random student went on the skating trip but did not do the run?", fr(skate - both, t),
                   [fr(skate, t), fr(both, t), fr(skate - both, skate)],
                   "Skating only: 38 − 22 = 16 students, so <b>".replace("−", M) + fr(16, 120) + "</b> (= " + fr(2, 15) + "). "
                   + fr(38, 120) + " includes the 22 who also did the run.", ans=F(skate - both, t)))
    c, f, n, t = 35, 28, 10, 60
    b = c + f - (t - n)
    assert b == 13
    its.append(mcq("At a cottage weekend, 60 people were asked about canoeing and fishing. 35 like canoeing, 28 like "
                   "fishing and 10 like neither. How many like both?", str(b), ["3", "50", "63"],
                   "60 − 10 = 50 like at least one. 35 + 28 = 63, which is 13 more than 50, so <b>13</b> people were "
                   "counted twice: they like both. 3 forgets the 10 who like neither.".replace("−", M), ans=b))
    its.append(mcq("Same cottage weekend (60 people, 13 like both, 35 like canoeing): what is the probability that a "
                   "random person likes canoeing but not fishing?", fr(c - b, t), [fr(c, t), fr(b, t), fr(c - b, t - n)],
                   "Canoeing only: 35 − 13 = 22, so <b>".replace("−", M) + fr(22, 60) + "</b> (= " + fr(11, 30) + "). "
                   + fr(35, 60) + " includes the 13 who like both.", ans=F(c - b, t)))
    its.append(mcq("In a survey of Grade 8 students in Hamilton, 45% have a library card, 30% play an instrument and "
                   "12% do both. What percent do neither?", "37%", ["25%", "63%", "12%"],
                   "At least one: 45% + 30% − 12% = 63%. Neither: 100% − 63% = <b>37%</b>. 25% comes from "
                   "100 − 45 − 30, which counts the 12% twice.".replace("−", M), ans=F(37, 100)))
    pr = F("0.2")
    its.append(mcq("On a two-day canoe trip in Algonquin Park, the chance of rain is 0.2 each day, and the days are "
                   "independent. What is the probability of no rain on either day?", "0.64",
                   ["0.6", "0.04", "1.6"],
                   "No rain: 1 − 0.2 = 0.8 each day. 0.8 × 0.8 = <b>0.64</b>. 0.04 is rain on both days. "
                   "1.6 adds.".replace("−", M), ans=(1 - pr) ** 2))
    its.append(mcq("Winnipeg has a 40% chance of snow on Saturday and a 40% chance on Sunday (independent). "
                   "What is the probability of snow on both days?", "16%", ["80%", "40%", "1.6%"],
                   "0.4 × 0.4 = 0.16 = <b>16%</b>. 80% adds. 1.6% puts the decimal point in the wrong place.",
                   ans=F(4, 10) ** 2))
    g = F(3, 4)
    its.append(mcq("A hockey goalie stops 3 of every 4 shots in a shootout, and each shot is independent. "
                   "What is the probability that she stops the next two shots?", fr(9, 16),
                   [fr(3, 2), fr(3, 4), fr(6, 16)],
                   fr(3, 4) + " × " + fr(3, 4) + " = <b>" + fr(9, 16) + "</b>. " + fr(3, 2) + " adds and is more than 1. "
                   + fr(6, 16) + " adds the tops but multiplies the bottoms.", ans=g * g))
    w = F(18, 30)
    assert w == F("0.6")
    its.append(mcq("Hana’s ringette team won 18 of its last 30 games. Use this to estimate the probability that the "
                   "team wins its next two games.", "0.36", ["1.2", "0.6", "3.6"],
                   "18 ÷ 30 = 0.6. Two wins in a row: 0.6 × 0.6 = <b>0.36</b>. 1.2 adds. 3.6 puts the decimal point "
                   "in the wrong place.", ans=w * w))
    its.append(mcq("A bike lock has 3 dials, each with the digits 0 to 9. Owen forgot the code and guesses once. "
                   "What is the probability that his guess is right?", fr(1, 1000), [fr(1, 30), fr(1, 10), fr(3, 10)],
                   "10 × 10 × 10 = 1000 possible codes, and one is right: <b>" + fr(1, 1000) + "</b>. "
                   + fr(1, 30) + " adds 10 + 10 + 10.", ans=F(1, 10) ** 3))
    its.append(mcq("Priya guesses all 4 questions on a quiz. Each question has 4 choices. What is the probability "
                   "that she gets all 4 right?", fr(1, 256), [fr(1, 16), fr(1, 4), "1"],
                   fr(1, 4) + " × " + fr(1, 4) + " × " + fr(1, 4) + " × " + fr(1, 4) + " = <b>" + fr(1, 256) + "</b> "
                   "(4<sup>4</sup> = 256). " + fr(1, 16) + " uses 4 × 4. Adding " + fr(1, 4) + " four times gives 1, "
                   "which would mean certain.", ans=F(1, 4) ** 4))
    its.append(mcq("Maya buys 1 of 30 tickets in a school raffle and 1 of 20 tickets in a library raffle. "
                   "What is the probability that she wins both?", fr(1, 600), [fr(1, 50), fr(5, 60), fr(1, 20)],
                   fr(1, 30) + " × " + fr(1, 20) + " = <b>" + fr(1, 600) + "</b>. " + fr(1, 50) + " adds 30 + 20. "
                   + fr(5, 60) + " adds the probabilities.", ans=F(1, 30) * F(1, 20)))
    its.append(mcq("The school cafeteria gives a random lunch: 3 kinds of wraps, 2 kinds of soup and 2 kinds of fruit, "
                   "all equally likely. What is the probability that Lucas gets a chicken wrap, tomato soup and an apple "
                   "(one of each kind)?", fr(1, 12), [fr(1, 7), fr(1, 6), fr(7, 6)],
                   "3 × 2 × 2 = 12 lunches, so <b>" + fr(1, 12) + "</b>. " + fr(1, 7) + " adds 3 + 2 + 2. "
                   + fr(1, 6) + " forgets the fruit.", ans=F(1, 3) * F(1, 2) * F(1, 2)))
    its.append(mcq("A Grade 8 class tosses a coin to choose the CN Tower or the Ontario Science Centre, then spins a "
                   "spinner with 3 equal sections to choose Tuesday, Wednesday or Thursday. What is the probability of "
                   "the CN Tower on a Thursday?", fr(1, 6), [fr(1, 5), fr(5, 6), fr(1, 3)],
                   "2 × 3 = 6 outcomes, so <b>" + fr(1, 6) + "</b>. " + fr(1, 5) + " adds 2 + 3 outcomes. "
                   + fr(1, 3) + " forgets the coin.", ans=F(1, 2) * F(1, 3)))
    p = F(1, 4) * F(1, 6)
    its.append(mcq("At a fall fair game, a player wins by spinning red on a spinner with 4 equal colours and rolling a 6. "
                   "About how many winners should there be in 240 plays?", "10", ["100", "24", "40"],
                   fr(1, 4) + " × " + fr(1, 6) + " = " + fr(1, 24) + ", and " + fr(1, 24) + " of 240 = <b>10</b>. "
                   "100 uses " + fr(1, 4) + " + " + fr(1, 6) + " = " + fr(5, 12) + ". 24 uses " + fr(1, 10) +
                   " (adding 4 + 6 outcomes). 40 uses the number cube only.", ans=p * 240))
    its.append(mcq("In a board game, Benjamin rolls three number cubes. What is the probability of three 6s?",
                   fr(1, 216), [fr(1, 18), fr(1, 2), fr(1, 36)],
                   "6 × 6 × 6 = 216 outcomes, so <b>" + fr(1, 216) + "</b>. " + fr(1, 18) + " adds 6 + 6 + 6. "
                   + fr(1, 2) + " adds " + fr(1, 6) + " three times. " + fr(1, 36) + " uses two cubes.", ans=F(1, 6) ** 3))
    pb = F(1, 10)
    its.append(mcq("Owen’s bus is late on 1 day in 10, and each day is independent. What is the probability that it is "
                   "late on Monday, Tuesday and Wednesday?", "0.001", ["0.3", "0.1", "0.01"],
                   "0.1 × 0.1 × 0.1 = <b>0.001</b>. 0.3 adds. 0.01 stops after two days.", ans=pb ** 3))
    its.append(mcq("Sofia tosses three coins 400 times and gets all three the same 97 times. "
                   "Do her results fit the theory?", "Yes, theory predicts about 100",
                   ["No, theory predicts about 200", "No, theory predicts about 50", "Yes, theory predicts exactly 97"],
                   "All the same: HHH or TTT, 2 of 8 outcomes = " + fr(1, 4) + ". " + fr(1, 4) + " of 400 = 100, and 97 "
                   "is <b>close to 100</b>. About 50 counts only HHH.", ans=None))
    its.append(mcq("Arjun and Chloe each roll a number cube. Arjun wins if both numbers are even. Chloe wins if both are "
                   "odd. Otherwise no one wins. Is the game fair?", "Yes, each has a " + fr(1, 4) + " chance",
                   ["No, Arjun has a better chance", "No, Chloe has a better chance",
                    "Yes, each has a " + fr(1, 2) + " chance"],
                   "Both even: " + fr(1, 2) + " × " + fr(1, 2) + " = " + fr(1, 4) + ". Both odd: " + fr(1, 2) + " × " + fr(1, 2) +
                   " = " + fr(1, 4) + ". The chances are equal, so <b>the game is fair</b>."))
    n = 6
    assert F(1, n) ** 2 == F(1, 36)
    its.append(mcq("A game uses two identical spinners, each with equal sections and one gold section. "
                   "P(gold on both) = " + fr(1, 36) + ". How many sections does each spinner have?", str(n),
                   ["18", "36", "72"],
                   fr(1, 6) + " × " + fr(1, 6) + " = " + fr(1, 36) + ", so each spinner has <b>6</b> sections. "
                   "18 comes from 18 + 18 = 36, adding instead of multiplying. 36 forgets there are two spinners.",
                   ans=n))
    assert len(its) == 20
    return {"title": "Word problems: Venn diagrams, trees and independent events", "items": its}


# ============================================================ lesson
def body_html():
    ven = venn_svg("A Grade 8 class: 30 students", "Hockey", "Soccer", *V1, label="Venn diagram hockey and soccer 30 students")
    tree = tree_svg([["H", "T"]] * 3, ["Coin 1", "Coin 2", "Coin 3"], label="tree diagram three coins")
    pt = ptree_svg(FT, FT, label="probability tree two free throws", h1="First shot", h2="Second shot")
    return (
        "<h2>Venn diagrams</h2>"
        "<p>A Venn diagram sorts a group into regions. The <b>overlap</b> is “A and B”. Everything inside the circles "
        "is “A or B”. The number outside the circles is “neither”. All the regions add up to the whole group.</p>"
        "<figure class='sn-fig'>" + ven +
        "<figcaption>8 play only hockey, 5 play both, 10 play only soccer and 7 (bottom right) play neither.</figcaption>"
        "</figure>"
        + ex("Example 1", "A student from this class is chosen at random. What is P(hockey or soccer)?",
             "Add the regions inside the circles once each: 8 + 5 + 10 = 23. Do not add 13 + 15 = 28: that counts the "
             "5 in the overlap twice.", fr(23, 30))
        + "<h2>Tree diagrams</h2>"
        "<p>A tree diagram shows every outcome of two or more events. Each path from left to right is one outcome. "
        "Count the outcomes by <b>multiplying</b>: three coins give 2 × 2 × 2 = 8 outcomes.</p>"
        "<figure class='sn-fig'>" + tree +
        "<figcaption>Three coins: 8 equally likely outcomes.</figcaption></figure>"
        + ex("Example 2", "You toss three coins. What is P(exactly two heads)?",
             "HHT, HTH and THH are 3 of the 8 paths.", fr(3, 8))
        + "<h2>Independent events: multiply</h2>"
        "<p>Events are <b>independent</b> when one does not change the chance of the other. Then "
        "<b>P(A and B) = P(A) × P(B)</b>. On a probability tree, multiply along the path; "
        "if two paths both work, add their results.</p>"
        "<figure class='sn-fig'>" + pt +
        "<figcaption>Kai makes a free throw with probability 0.7.</figcaption></figure>"
        + ex("Example 3", "What is the probability that Kai makes exactly one of two free throws?",
             "Make, miss: 0.7 × 0.3 = 0.21. Miss, make: 0.3 × 0.7 = 0.21. Add the two paths: 0.21 + 0.21.", "0.42")
        + "<h2>Experimental and theoretical probability</h2>"
        "<p>Theoretical probability comes from counting equally likely outcomes. Experimental probability = times it "
        "happened ÷ number of trials. The two are usually close but rarely equal. <b>More trials usually get closer.</b></p>"
        + ex("Example 4", "Three coins are tossed 160 times. About how many times should you expect three heads?",
             "P(HHH) = " + fr(1, 8) + ". " + fr(1, 8) + " of 160 = 160 ÷ 8 = 20.", "about 20")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["P(heads and 6) = " + fr(1, 2) + " + " + fr(1, 6) + " = " + fr(4, 6),
             "“And” for independent events: multiply. " + fr(1, 2) + " × " + fr(1, 6) + " = " + fr(1, 12) + "."],
            ["Hockey or soccer = 13 + 15 = 28", "The overlap is counted twice. 13 + 15 − 5 = 23.".replace("−", M)],
            ["Forgetting the number outside the circles", "The whole group includes “neither”. Divide by the total."],
            ["Exactly one make = 0.7 × 0.3 = 0.21", "Two paths work (make, miss and miss, make): 0.42."],
            ["0.3 × 0.3 = 0.9", "Count the decimal places: 0.3 × 0.3 = 0.09."],
            ["“TTT came up, so TTT is less likely next time.”", "Coins have no memory. It is still " + fr(1, 8) + "."],
        ])
    )


FAQ = [
    {"q": "How do you find probability with a Venn diagram in Grade 8?",
     "a": "Add the regions that match the event and divide by the whole group, including the number outside the circles. For “A or B”, count the overlap only once; for “A and B”, use only the overlap."},
    {"q": "When do you multiply probabilities?",
     "a": "Multiply when you want two or more independent events to all happen, such as heads and a 6 (1/2 × 1/6 = 1/12). Adding the probabilities is a common mistake and can give an answer greater than 1."},
    {"q": "How do you use a tree diagram for three events?",
     "a": "Draw a branch for each outcome of the first event, then split every branch for the second and third events. Each path is one outcome, so three coins give 2 × 2 × 2 = 8 outcomes."},
    {"q": "What is the difference between experimental and theoretical probability?",
     "a": "Theoretical probability comes from counting equally likely outcomes, like 1/8 for three heads. Experimental probability comes from trials, like 12 three-heads results in 80 tosses (0.15), and it usually gets closer to the theory with more trials."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (tree diagrams, probability trees, tables)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(48813)
    sets = [set_venn(), set_trees(), set_multiply(), set_exp(), set_words()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "probability-venn-and-tree-diagrams",
        "sort": 13, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Probability: Venn Diagrams, Tree Diagrams and Independent Events",
        "seo_title": "Grade 8 Probability Worksheets: Venn and Tree Diagrams (Free, Answer Key, Ontario Curriculum)",
        "short_title": "Probability: Venn and tree diagrams",
        "domain": "Data",
        "standard_code": "Grade 8: D2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve various problems that involve probability, using appropriate tools and strategies, including Venn and tree diagrams",
        "meta_desc": "Free Grade 8 math worksheets on probability for the Ontario curriculum: Venn diagrams (and, or, neither), tree diagrams for two and three events, multiplying probabilities of independent events, and experimental vs theoretical probability. 100 questions with an answer key.",
        "key_big": "For independent events, P(A and B) = P(A) × P(B). In a Venn diagram, count the overlap only once.",
        "key_sub": "Three coins give 2 × 2 × 2 = 8 outcomes, so P(HHH) = 1/8, not 1/2 + 1/2 + 1/2. Divide by the whole group, including the people outside the circles. More trials bring experimental results closer to the theory.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(tree diagram|probability tree|frequency table|results table)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
