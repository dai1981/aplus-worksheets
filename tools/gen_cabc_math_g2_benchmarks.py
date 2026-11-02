# -*- coding: utf-8 -*-
"""
British Columbia Grade 2 Math: Benchmarks of 25, 50 and 100
(BC Mathematics Curriculum, Grade 2: Number - "Benchmarks of 25, 50, and 100 and personal referents")
  python3 tools/gen_cabc_math_g2_benchmarks.py
Numbers to 100. Short sentences for 7-8 year olds, a picture in many questions
(number lines, jars of marbles, trays of beans, a 100 chart, a metre stick, coins, a ferry deck).
Wrong answers come from real mistakes: looking only at the tens digit (48 is closer to 25),
picking the next benchmark the wrong way, reading 10 as close to 100, reversing digits (53 and 35),
counting by 5s after 75 (75, 80), adding the number of handfuls (2 handfuls of 25 = 27),
mixing up quarters and nickels (2 quarters = 10¢), counting coins instead of cents (3 quarters = 3¢),
halving only the gap (halfway between 50 and 100 is 25) and taking the smaller digit from the bigger one.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
LIGHT = "#e8f3ec"
RED = "#c0392b"
BLUE = "#2e6da4"
BEAN = "#8b4a2b"
GREY = "#9a9a9a"
DGREY = "#6b6259"
INK = "#2b2b2b"
WOOD = "#f3dd9b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
BENCH = [0, 25, 50, 100]


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e):
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    return {"q": q, "c": [correct] + wrong, "a": 0, "e": e}


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            wrong = [x for i, x in enumerate(ch) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [ch[it["a"]]] + wrong[t:]
            it["a"] = t
        assert [sum(1 for it in st["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, large=False):
    assert "'" not in label
    return ("<svg %sxmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>"
            % ("data-pf='lg' " if large else "", w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, wt=700):
    assert fs >= 14
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, wt, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def closest(n, cands=BENCH):
    """The one closest benchmark (asserts there is no tie)."""
    d = sorted((abs(n - b), b) for b in cands)
    assert d[0][0] < d[1][0], (n, cands)
    return d[0][1]


def bench_near(n):
    """closest of 0, 25, 50, 100, and the number must not be nearer to 75 (75 is not a choice here)."""
    b = closest(n)
    assert abs(n - b) < abs(n - 75), n
    return b


def ce(n):
    return "%d¢" % n


# ------------------------------------------------------------ pictures
def nl_svg(lo, hi, minor, labels, dot=None, q_at=None, hl=None, aria=None):
    """Number line lo..hi. labels: values that get a number under them (big ticks).
    dot: red dot with its number above. q_at: red ? under that tick. hl: a value whose label is red."""
    L, R = 26, 414
    Y = 40 if dot is not None else 16
    W, H = 440, Y + 38
    span = float(hi - lo)

    def X(v):
        return L + (v - lo) * (R - L) / span

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 8, Y, R + 8, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels or v == q_at
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (X(v), Y - (10 if big else 5), X(v), Y + (10 if big else 5), RED if v == q_at else INK,
                    2 if big else 1))
        if v in labels:
            s.append(text(X(v), Y + 30, str(v), 15, col=RED if v == hl else GREEN))
        if v == q_at:
            s.append(text(X(v), Y + 31, "?", 18, col=RED))
        v += minor
    if dot is not None:
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(dot), Y, RED))
        s.append(text(X(dot), Y - 16, str(dot), 16, col=RED, wt=800))
    return svg_wrap(W, H, "".join(s), aria or "number line from %d to %d" % (lo, hi), large=True)


JC, JR, JCELL = 10, 10, 14


def jar(x, y, n, lab):
    """A jar that holds 100 marbles (10 rows of 10), filled from the bottom with n marbles."""
    jw_, jh = JC * JCELL + 10, JR * JCELL + 10
    s = ["<rect x='%d' y='%d' width='%d' height='10' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
         % (x + 22, y - 10, jw_ - 44, GREY, INK),
         "<rect x='%d' y='%d' width='%d' height='%d' rx='14' fill='#ffffff' stroke='%s' stroke-width='2.5'/>"
         % (x, y, jw_, jh, INK)]
    for c in range(n):
        r, cc = divmod(c, JC)
        cx = x + 5 + cc * JCELL + JCELL / 2.0
        cy = y + jh - 5 - r * JCELL - JCELL / 2.0
        s.append("<circle cx='%.1f' cy='%.1f' r='5.6' fill='%s'/>" % (cx, cy, BLUE))
    if lab is not None:
        s.append(text(x + jw_ / 2.0, y + jh + 22, lab, 18, col=RED if lab == "?" else INK))
    return "".join(s), jw_, jh


def jar_svg(n):
    body, jw_, jh = jar(4, 14, n, None)
    return svg_wrap(jw_ + 8, jh + 20, body, "a jar that holds 100 marbles with %d marbles in it" % n)


def two_jars_svg(ref, n):
    a, jw_, jh = jar(4, 14, ref, str(ref))
    b, _, _ = jar(4 + jw_ + 40, 14, n, "?")
    return svg_wrap(8 + 2 * jw_ + 40, 14 + jh + 30, a + b,
                    "a jar with %d marbles and a jar with %d marbles" % (ref, n), large=True)


def tray_svg(n, rnd, kind):
    """n beans or marbles spread over a tray of 14 x 8 cells (one per cell, small wobble), so none overlap."""
    cols, rows, cell = 14, 8, 22
    assert n <= cols * rows
    W, H = 12 + cols * cell, 12 + rows * cell
    s = ["<rect x='2' y='2' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='1.5'/>"
         % (W - 4, H - 4, LIGHT, GREEN)]
    for k in sorted(rnd.sample(range(cols * rows), n)):
        r, c = divmod(k, cols)
        cx = 6 + c * cell + cell / 2.0 + rnd.uniform(-3, 3)
        cy = 6 + r * cell + cell / 2.0 + rnd.uniform(-3, 3)
        if kind == "beans":
            s.append("<ellipse cx='%.1f' cy='%.1f' rx='8' ry='5' fill='%s' transform='rotate(%d %.1f %.1f)'/>"
                     % (cx, cy, BEAN, rnd.choice([-40, -20, 0, 20, 40, 70]), cx, cy))
        else:
            s.append("<circle cx='%.1f' cy='%.1f' r='7.5' fill='%s'/>" % (cx, cy, BLUE))
    return svg_wrap(W, H, "".join(s), "%d %s spread out on a tray" % (n, kind), large=True)


def chart100_svg(shaded):
    """A 100 chart (10 x 10 squares) with the first `shaded` squares coloured, row by row."""
    c, m = 15, 3
    s = []
    for k in range(100):
        r, cc = divmod(k, 10)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (m + cc * c, m + r * c, c, c, "#f2b27a" if k < shaded else "#ffffff", GREEN))
    return svg_wrap(2 * m + 10 * c, 2 * m + 10 * c, "".join(s), "a 100 chart with %d squares coloured" % shaded)


def metre_svg():
    """A metre stick from 0 to 100 cm, with a red arrow at the halfway mark."""
    L, R, Y = 20, 420, 20
    s = ["<rect x='%d' y='%d' width='%d' height='34' fill='%s' stroke='%s' stroke-width='2'/>" % (L, Y, R - L, WOOD, INK)]
    for cm in range(0, 101, 5):
        x = L + cm * (R - L) / 100.0
        h = 14 if cm % 10 == 0 else 8
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>" % (x, Y, x, Y + h, INK))
    s.append(text(L + 4, Y + 30, "0", 14, anchor="start"))
    s.append(text(R - 4, Y + 30, "100 cm", 14, anchor="end"))
    xm = L + 50 * (R - L) / 100.0
    s.append("<path d='M %.1f %d L %.1f %d L %.1f %d Z' fill='%s'/>" % (xm, Y + 38, xm - 8, Y + 54, xm + 8, Y + 54, RED))
    s.append(text(xm, Y + 74, "?", 18, col=RED))
    return svg_wrap(440, Y + 82, "".join(s), "a metre stick from 0 to 100 cm with an arrow halfway", large=True)


def coin(cx, cy, kind):
    if kind == "quarter":
        return ("<circle cx='%.1f' cy='%.1f' r='25' fill='#dfe3e7' stroke='#7a828a' stroke-width='2'/>"
                "<circle cx='%.1f' cy='%.1f' r='21' fill='none' stroke='#9aa2aa' stroke-width='1'/>"
                % (cx, cy, cx, cy) + text(cx, cy + 6, "25¢", 16))
    if kind == "loonie":
        import math
        pts = " ".join("%.1f,%.1f" % (cx + 25 * math.sin(2 * math.pi * k / 11), cy - 25 * math.cos(2 * math.pi * k / 11))
                       for k in range(11))
        return ("<polygon points='%s' fill='#e3bd52' stroke='#8a6d1c' stroke-width='2'/>" % pts
                + text(cx, cy + 6, "$1", 16))
    raise ValueError(kind)


def coins_svg(kinds):
    s = [coin(30 + i * 60, 30, k) for i, k in enumerate(kinds)]
    W = 60 * len(kinds)
    return svg_wrap(W, 60, "".join(s), "coins: " + ", ".join(kinds))


def track_svg(cells):
    w, h, m = 56, 42, 3
    s = []
    for i, v in enumerate(cells):
        q = v == "?"
        x = m + i * w
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, m, w, h, FILL if q else "#ffffff", GREEN))
        s.append(text(x + w / 2.0, m + 28, str(v), 20, col=RED if q else INK))
    return svg_wrap(2 * m + len(cells) * w, 2 * m + h, "".join(s), "number track")


def deck_svg(n):
    """A ferry car deck with 100 spaces (5 lanes of 20). n cars are parked from the front."""
    cw, ch, gx, gy, m = 16, 11, 2, 5, 8
    W = 2 * m + 20 * cw + 19 * gx
    H = 2 * m + 5 * ch + 4 * gy
    s = ["<rect x='2' y='2' width='%d' height='%d' rx='8' fill='#f4f4f4' stroke='%s' stroke-width='2'/>"
         % (W - 4, H - 4, INK)]
    for k in range(100):
        lane, c = divmod(k, 20)
        x, y = m + c * (cw + gx), m + lane * (ch + gy)
        if k < n:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='3' fill='%s'/>" % (x, y, cw, ch, BLUE))
        else:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='3' fill='none' stroke='%s' stroke-width='1' "
                     "stroke-dasharray='2 2'/>" % (x, y, cw, ch, GREY))
    return svg_wrap(W, H, "".join(s), "a ferry deck with 100 spaces and %d cars" % n, large=True)


# ============================================================ set 1: closest benchmark on a number line
def bench_expl(n):
    b = bench_near(n)
    lo = max(x for x in BENCH if x <= n)
    hi = min(x for x in BENCH if x >= n)
    if lo == hi:
        return "%d is a benchmark itself. Answer: <b>%d</b>." % (n, n)
    return ("%d is between %d and %d. It is %d away from %d and %d away from %d. "
            "%d is closer, so %d is closest to <b>%d</b>."
            % (n, lo, hi, n - lo, lo, hi - n, hi, b, n, b))


def q_bench(n, pic=True, prompt=None, extra=""):
    b = bench_near(n)
    q = prompt or "Is %d closest to 0, 25, 50 or 100?" % n
    if pic:
        q = fig(nl_svg(0, 100, 5, BENCH, dot=n)) + q
    return mcq(q, b, [x for x in BENCH if x != b], bench_expl(n) + extra)


def q_nearest_to(target, right, wrongs, why):
    ds = {x: abs(x - target) for x in [right] + wrongs}
    assert all(ds[right] < ds[w] for w in wrongs)
    lst = ", ".join("%d is %d away" % (x, ds[x]) for x in sorted([right] + wrongs, key=lambda v: ds[v]))
    q = fig(nl_svg(0, 100, 5, BENCH, hl=target)) + "Which number is closest to %d?" % target
    return mcq(q, right, wrongs, "Count how far each number is from %d: %s. The closest is <b>%d</b>.%s"
               % (target, lst, right, why))


def set_closest():
    its = []
    for n in [4, 96, 52, 23, 47, 9, 29, 54, 91, 18, 33, 44, 58, 89]:
        its.append(q_bench(n))
    its.append(q_bench(48, extra=" Do not look only at the tens digit: 4 tens is close to 5 tens."))
    its.append(q_nearest_to(50, 53, [35, 60, 5], " 35 has the same digits as 53, but it is much farther away."))
    its.append(q_nearest_to(100, 94, [10, 80, 50], " 10 looks like 100, but it is 90 away."))
    its.append(q_nearest_to(25, 27, [52, 15, 40], " 52 has the same digits as 25, but it is far away."))
    its.append(q_nearest_to(0, 3, [30, 13, 20], " 30 has a 3 in it, but it is 30 away from 0."))
    its.append(q_nearest_to(50, 46, [60, 64, 30], ""))
    return {"title": "Closest to 0, 25, 50 or 100?", "items": its}


# ============================================================ set 2: estimate collections
ABOUT = [10, 25, 50, 100]


def about(n):
    return "about %d" % n


def est_q(q, n, how):
    b = closest(n, ABOUT)
    return mcq(q, about(b), [about(x) for x in ABOUT if x != b],
               "%s There are %d, so <b>about %d</b> is the best estimate." % (how, n, b))


def set_estimate(rnd):
    its = []
    for n in [48, 26, 97, 11, 52, 23]:
        b = closest(n, ABOUT)
        how = {10: "The jar has only about 1 row of 10, so it is nearly empty.",
               25: "A full jar is 100. This jar is about a quarter full.",
               50: "A full jar is 100. This jar is about half full.",
               100: "The jar is almost full, and a full jar is 100."}[b]
        its.append(est_q(fig(jar_svg(n)) + "A full jar holds 100 marbles. About how many marbles are in this jar?",
                         n, how))
    for n in [51, 98, 27, 47, 94, 22]:
        b = closest(n, ABOUT)
        how = {25: "The second jar looks about the same as the first jar.",
               50: "The second jar looks like 2 jars of 25: 25, 50.",
               100: "The second jar looks like 4 jars of 25: 25, 50, 75, 100."}[b]
        its.append(est_q(fig(two_jars_svg(25, n)) + "The first jar has 25 marbles. "
                         "About how many marbles are in the second jar?", n, how))
    for n, kind in [(26, "beans"), (49, "marbles"), (96, "beans"), (12, "marbles"),
                    (53, "beans"), (24, "marbles"), (99, "marbles"), (47, "beans")]:
        b = closest(n, ABOUT)
        how = {10: "Only a few are on the tray.",
               25: "About a quarter of the tray is used.",
               50: "About half of the tray is used.",
               100: "The tray is almost full."}[b]
        its.append(est_q(fig(tray_svg(n, rnd, kind)) + "Do not count. About how many %s are on the tray?" % kind,
                         n, how))
    # order easy -> harder: jars first, then compare, then trays (already in that order)
    return {"title": "Estimate: about 25, 50 or 100?", "items": its}


# ============================================================ set 3: halfway to 100 is 50
HALF = ["more than halfway", "less than halfway", "exactly halfway", "all the way to 100"]


def half_dot(n):
    right = "exactly halfway" if n == 50 else "more than halfway" if n > 50 else "less than halfway"
    e = ("Halfway from 0 to 100 is 50. " +
         ("The dot is on 50, so it is <b>exactly halfway</b>." if n == 50 else
          "%d is %s than 50, so the dot is <b>%s</b>." % (n, "more" if n > 50 else "less", right)))
    return mcq(fig(nl_svg(0, 100, 10, [0, 50, 100], dot=n)) + "Is the dot more or less than halfway to 100?",
               right, [x for x in HALF if x != right], e)


def set_halfway():
    its = []
    its.append(mcq(fig(nl_svg(0, 100, 10, [0, 100], q_at=50)) + "What number is halfway between 0 and 100?",
                   50, [10, 25, 75],
                   "There are 10 jumps of 10 from 0 to 100. Halfway is 5 jumps: 10, 20, 30, 40, 50. "
                   "Answer: <b>50</b>."))
    its.append(mcq(fig(chart100_svg(50)) + "How many squares are coloured?", 50, [5, 25, 10],
                   "5 rows of 10 are coloured: 10, 20, 30, 40, 50. That is <b>50</b>, half of the 100 chart."))
    its.append(mcq("What is half of 100?", 50, [25, 10, 200],
                   "50 + 50 = 100, so half of 100 is <b>50</b>. 25 is a quarter of 100."))
    its.append(mcq("How many 50s make 100?", 2, [50, 5, 10],
                   "50 + 50 = 100. That is <b>2</b> fifties."))
    assert 50 + 50 == 100
    for n in [62, 38, 50, 90]:
        its.append(half_dot(n))
    its.append(mcq(fig(nl_svg(0, 50, 5, [0, 50], q_at=25)) + "What number is halfway between 0 and 50?",
                   25, [20, 30, 10],
                   "From 0 to 50 there are 10 jumps of 5. Halfway is 5 jumps: 5, 10, 15, 20, 25. Answer: <b>25</b>."))
    its.append(mcq(fig(metre_svg()) + "A metre stick is 100 cm long. The arrow is halfway. What number is there?",
                   "50 cm", ["5 cm", "25 cm", "10 cm"],
                   "Half of 100 cm is <b>50 cm</b>. 50 cm + 50 cm = 100 cm."))
    its.append(mcq("How far is it from 50 to 100?", 50, [150, 25, 100],
                   "Count on by 10s from 50: 60, 70, 80, 90, 100. That is 5 tens, or <b>50</b>. "
                   "150 adds 50 and 100."))
    its.append(mcq("Which number is more than halfway to 100?", 58, [45, 39, 50],
                   "Halfway is 50. Only <b>58</b> is more than 50. 50 is exactly halfway, not more."))
    its.append(mcq("Which number is less than halfway to 100?", 47, [52, 61, 74],
                   "Halfway is 50. Only <b>47</b> is less than 50. Look at the tens first: 4 tens is less than 5 tens."))
    its.append(mcq("A loonie is worth 100¢. How much is half of a loonie?", "50¢", ["25¢", "10¢", "200¢"],
                   "Half of 100¢ is <b>50¢</b>. 50¢ + 50¢ = 100¢. 25¢ is only a quarter of a loonie."))
    its.append(mcq(fig(nl_svg(50, 100, 5, [50, 100], q_at=75)) + "What number is halfway between 50 and 100?",
                   75, [25, 70, 80],
                   "From 50 to 100 is 50. Half of 50 is 25. Start at 50 and add 25: 50 + 25 = <b>75</b>. "
                   "25 is only the jump, not the number."))
    its.append(mcq("What number is halfway between 40 and 60?", 50, [20, 100, 45],
                   "40 is 10 less than 50, and 60 is 10 more than 50. So <b>50</b> is halfway."))
    its.append(mcq("What number is halfway between 25 and 75?", 50, [25, 100, 60],
                   "25 is 25 less than 50, and 75 is 25 more than 50. So <b>50</b> is halfway. "
                   "25 is only half of the gap."))
    its.append(mcq("50 is halfway between 0 and what number?", 100, [25, 75, 60],
                   "From 0 to 50 is 50. Go 50 more: 50 + 50 = <b>100</b>."))
    its.append(mcq("Ethan says halfway between 0 and 100 is 10. Is he right?",
                   "No, it is 50", ["Yes, it is 10", "No, it is 25", "No, it is 100"],
                   "10 is only 1 jump of 10. Halfway is 5 jumps of 10, which is <b>50</b>. 50 + 50 = 100."))
    its.append(mcq("The path to the playground is 100 m long. Sofia stops halfway to tie her shoe. "
                   "How far has she walked?", "50 m", ["10 m", "25 m", "100 m"],
                   "Halfway along 100 m is <b>50 m</b>, because 50 + 50 = 100."))
    return {"title": "Halfway to 100 is 50", "items": its}


# ============================================================ set 4: count by 25s and quarters
def set_quarters():
    its = []
    its.append(mcq(fig(track_svg([25, 50, 75, "?"])) + "Count by 25s. What number comes next?", 100, [80, 76, 125],
                   "Count by 25s: 25, 50, 75, <b>100</b>. 80 switches to counting by 5s."))
    its.append(mcq(fig(track_svg([25, "?", 75, 100])) + "Count by 25s. What is the missing number?", 50, [30, 26, 60],
                   "25 + 25 = <b>50</b>. Then 50 + 25 = 75. 30 adds only 5."))
    its.append(mcq(fig(track_svg([100, 75, 50, "?"])) + "Count back by 25s. What number comes next?", 25, [45, 0, 49],
                   "Count back by 25s: 100, 75, 50, <b>25</b>. 45 counts back by 5s."))
    its.append(mcq(fig(nl_svg(0, 100, 5, [0, 50, 100], q_at=25)) + "What number is at the ? mark?", 25, [20, 10, 30],
                   "Halfway from 0 to 50 is <b>25</b>. Each small jump is 5: 5, 10, 15, 20, 25."))
    its.append(mcq(fig(nl_svg(0, 100, 5, [0, 50, 100], q_at=75)) + "What number is at the ? mark?", 75, [70, 60, 25],
                   "Halfway from 50 to 100 is <b>75</b>. From 50, count 5 small jumps of 5: 55, 60, 65, 70, 75."))
    its.append(mcq("Which shows counting by 25s?", "25, 50, 75, 100",
                   ["25, 30, 35, 40", "25, 50, 70, 100", "20, 25, 30, 35"],
                   "Add 25 each time: 25, 50, 75, 100. Answer: <b>25, 50, 75, 100</b>. "
                   "25, 50, 70, 100 does not add the same number each time."))
    its.append(mcq("How many 25s make 100?", 4, [10, 5, 3],
                   "Count by 25s: 25, 50, 75, 100. That is <b>4</b> twenty-fives."))
    its.append(mcq("How many 25s make 50?", 2, [5, 25, 4],
                   "25 + 25 = 50. That is <b>2</b> twenty-fives."))
    its.append(mcq("25 + 25 = ?", 50, [40, 410, 30],
                   "5 + 5 = 10 ones, which is 1 ten. 2 tens + 2 tens + 1 ten = 5 tens. Answer: <b>50</b>. "
                   "40 forgets the new ten."))
    assert 25 + 25 == 50 and 50 + 25 == 75 and 100 - 25 == 75
    its.append(mcq("50 + 25 = ?", 75, [70, 525, 85],
                   "50 + 20 = 70, then 70 + 5 = <b>75</b>. 70 forgets the 5 ones."))
    its.append(mcq(fig(chart100_svg(25)) + "How many squares are coloured?", 25, [4, 20, 50],
                   "2 full rows of 10 and 5 more: 10, 20, 21, 22, 23, 24, 25. That is <b>25</b>, a quarter of the chart."))
    its.append(mcq(fig(chart100_svg(75)) + "How many squares are coloured?", 75, [70, 25, 7],
                   "7 full rows of 10 and 5 more: 70 + 5 = <b>75</b>. 25 squares are white, and 75 + 25 = 100."))
    its.append(mcq("Which number is one quarter of the way from 0 to 100?", 25, [4, 50, 75],
                   "Cut 0 to 100 into 4 equal jumps: 25, 50, 75, 100. One quarter of the way is <b>25</b>."))
    its.append(mcq(fig(coins_svg(["quarter", "quarter"])) + "How much money is this?", "50¢", ["2¢", "25¢", "10¢"],
                   "A quarter is 25¢. Count by 25s: 25¢, <b>50¢</b>. 10¢ counts them as nickels."))
    its.append(mcq(fig(coins_svg(["quarter", "quarter", "quarter"])) + "How much money is this?", "75¢",
                   ["3¢", "15¢", "50¢"],
                   "Count by 25s: 25¢, 50¢, <b>75¢</b>. 3¢ counts the coins, not the cents."))
    its.append(mcq(fig(coins_svg(["quarter"] * 4)) + "How much money is this?", "100¢", ["4¢", "20¢", "75¢"],
                   "Count by 25s: 25¢, 50¢, 75¢, <b>100¢</b>. That is the same as $1."))
    its.append(mcq(fig(coins_svg(["quarter"] * 4)) + "4 quarters have the same value as which coin?",
                   "a loonie", ["a toonie", "a dime", "a nickel"],
                   "4 quarters are 100¢, and a loonie is $1 = 100¢. Answer: <b>a loonie</b>. A toonie is $2."))
    its.append(mcq("100 " + MINUS + " 25 = ?", 75, [125, 80, 25],
                   "Count back by 25 from 100: <b>75</b>. 75 + 25 = 100. "
                   "125 takes the smaller digit from the bigger one in each place."))
    its.append(mcq("Nadia has 75¢ in quarters. How many quarters does she have?", 3, [75, 7, 4],
                   "Count by 25s: 25¢, 50¢, 75¢. That is <b>3</b> quarters."))
    its.append(mcq("Wei has 3 quarters. How many more quarters does he need to make 100¢?", 1, [25, 4, 2],
                   "3 quarters are 75¢. 75¢ + 25¢ = 100¢. He needs <b>1</b> more quarter."))
    return {"title": "Count by 25s and quarters", "items": its}


# ============================================================ set 5: personal referents and word problems
FULL = ["about a quarter full", "about half full", "almost full", "almost empty"]


def deck_q(n):
    right = {25: FULL[0], 50: FULL[1], 100: FULL[2]}[closest(n, [25, 50, 100])]
    return mcq(fig(deck_svg(n)) + "A BC Ferries car deck has 100 spaces. %d cars are on it. "
               "How full is the deck?" % n, right, [x for x in FULL if x != right],
               "%d is close to %d, and the deck holds 100. So it is <b>%s</b>."
               % (n, closest(n, [25, 50, 100]), right))


def set_words():
    its = []
    its.append(mcq("A handful of beans is about 25 beans. Mei takes 2 handfuls. About how many beans does she have?",
                   "about 50", ["about 27", "about 25", "about 100"],
                   "Count by 25s for each handful: 25, 50. So <b>about 50</b>. 27 adds 2 instead of 2 handfuls."))
    its.append(mcq("A handful of beans is about 25 beans. Owen takes 4 handfuls. About how many beans does he have?",
                   "about 100", ["about 29", "about 50", "about 75"],
                   "Count by 25s: 25, 50, 75, 100. So <b>about 100</b>."))
    its.append(q_bench(24, False, "Ms. Lee’s Grade 2 class has 24 students. Is 24 closest to 0, 25, 50 or 100?"))
    its.append(q_bench(46, False, "At the Terry Fox Run, Lucas’s class runs 46 laps of the field in all. "
                       "Is 46 closest to 0, 25, 50 or 100?"))
    its.append(q_bench(93, False, "On a field trip to a creek, Kai’s class counts 93 salmon. "
                       "Is 93 closest to 0, 25, 50 or 100?"))
    its.append(q_bench(27, False, "Zara sees 27 bald eagles in the trees by the river. "
                       "Is 27 closest to 0, 25, 50 or 100?"))
    for n in [49, 26, 97]:
        its.append(deck_q(n))
    its.append(mcq("Liam has 100 stickers. He gives half of them to his sister. How many does he keep?",
                   50, [25, 98, 10],
                   "Half of 100 is <b>50</b>, because 50 + 50 = 100. 25 is a quarter, not a half."))
    its.append(mcq("A ribbon is 100 cm long. Ava cuts it in half. How long is each piece?",
                   "50 cm", ["25 cm", "10 cm", "200 cm"],
                   "Half of 100 cm is <b>50 cm</b>. 50 cm + 50 cm = 100 cm."))
    its.append(mcq(fig(coins_svg(["quarter", "quarter"])) + "Nadia has 2 quarters. A loonie is 100¢. "
                   "How much more does she need to make a loonie?", "50¢", ["98¢", "75¢", "25¢"],
                   "2 quarters are 50¢. 50¢ + 50¢ = 100¢. She needs <b>50¢</b> more. 98¢ takes away 2 coins, not 50¢."))
    its.append(mcq("Ryan has 75¢. How much more does he need to make 100¢?", "25¢", ["35¢", "175¢", "15¢"],
                   "Count on from 75: 75 + 25 = 100. He needs <b>25¢</b>. 175¢ adds instead."))
    its.append(mcq("A Grade 2 class has about 25 students. About 100 students come to an assembly. "
                   "About how many classes is that?", 4, [25, 2, 10],
                   "Count by 25s: 25, 50, 75, 100. That is <b>4</b> classes."))
    its.append(mcq("Which is about 100?", "the students in 4 classes",
                   ["the students in 1 class", "the fingers on 2 hands", "the wheels on a bike"],
                   "One class is about 25 students. 4 classes: 25, 50, 75, 100. So <b>the students in 4 classes</b> "
                   "is about 100. 2 hands have only 10 fingers."))
    its.append(mcq("Which is about 25?", "the students in 1 class",
                   ["the students in 4 classes", "the fingers on 1 hand", "the days in a week"],
                   "A Grade 2 class has about 25 students, so <b>the students in 1 class</b> is about 25. "
                   "1 hand has 5 fingers and a week has 7 days."))
    its.append(mcq("Jasleen says 48 is closer to 25, because 4 is less than 5. Is she right?",
                   "No, 48 is closer to 50", ["Yes, 48 is closer to 25", "No, 48 is closer to 100",
                                              "Yes, 48 is closer to 0"],
                   "48 is 2 away from 50 and 23 away from 25. So <b>48 is closer to 50</b>. "
                   "Look at how far away it is, not only at the tens digit."))
    assert abs(48 - 50) == 2 and abs(48 - 25) == 23 and abs(52 - 50) == 2 and abs(100 - 52) == 48
    its.append(mcq("Arjun estimates there are 100 marbles in a jar. He counts 52. Was his estimate close?",
                   "No, 52 is closer to 50", ["Yes, 52 is closer to 100", "Yes, it was exactly right",
                                              "No, 52 is closer to 25"],
                   "52 is 2 away from 50 and 48 away from 100. So <b>52 is closer to 50</b>, and 100 was not close."))
    its.append(mcq("A Grade 2 class plants 50 cedar seedlings. A Grade 3 class plants 50 more. "
                   "How many seedlings do they plant in all?", 100, [10, 1000, 60],
                   "50 + 50 = <b>100</b>. 5 tens and 5 tens make 10 tens, which is 100."))
    its.append(mcq("Emma’s class wants to read 100 books in March. They have read 52 books. How far along are they?",
                   "about halfway", ["almost done", "just started", "all done"],
                   "52 is close to 50, and 50 is halfway to 100. So they are <b>about halfway</b>."))
    return {"title": "Personal referents and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is a benchmark?</h2>"
        "<p>A benchmark is a friendly number you know well. In Grade 2, the benchmarks are <b>25</b>, <b>50</b> "
        "and <b>100</b> (and 0). We use them to think about other numbers. Is a number close to 25, 50 or 100?</p>"
        "<figure class='sn-fig'>" + nl_svg(0, 100, 5, BENCH, dot=48) +
        "<figcaption>48 is 2 away from 50 and 23 away from 25. 48 is closest to 50.</figcaption></figure>"
        + ex("Closest benchmark", "Is 29 closest to 0, 25, 50 or 100?",
             "29 is between 25 and 50. It is 4 away from 25 and 21 away from 50.", "25")
        + "<h2>Halfway and quarters</h2>"
        "<p>Halfway from 0 to 100 is <b>50</b>, because 50 + 50 = 100. Count by 25s to cut 100 into "
        "4 equal parts: 25, 50, 75, 100. A quarter coin is 25¢, and 4 quarters make 100¢, or $1.</p>"
        + table(["Count by 25s", "Quarters", "Part of 100"], [
            ["25", "1 quarter = 25¢", "a quarter"],
            ["50", "2 quarters = 50¢", "half"],
            ["75", "3 quarters = 75¢", "three quarters"],
            ["100", "4 quarters = 100¢ = $1", "all of it"],
        ]) +
        "<figure class='sn-fig'>" + chart100_svg(50) +
        "<figcaption>Half of the 100 chart is coloured: 5 rows of 10 = 50.</figcaption></figure>"
        "<h2>Estimate with a personal referent</h2>"
        "<p>A personal referent is something you know that is about 25, 50 or 100. A handful of beans is about 25. "
        "A Grade 2 class is about 25 students. Use it to estimate without counting.</p>"
        "<figure class='sn-fig'>" + two_jars_svg(25, 51) +
        "<figcaption>The first jar has 25. The second looks like 2 jars of 25, so it has about 50.</figcaption></figure>"
        + ex("Handfuls", "A handful of beans is about 25. About how many beans are in 4 handfuls?",
             "Count by 25s: 25, 50, 75, 100.", "about 100")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["48 is closer to 25, because 4 is less than 5", "48 is 2 away from 50 and 23 away from 25: it is closer to 50"],
            ["10 is close to 100, because it looks the same", "10 is 90 away from 100. Look at the value"],
            ["Counting 25, 50, 75, 80", "Keep adding 25: 25, 50, 75, 100"],
            ["Halfway between 50 and 100 is 25", "Start at 50 and add half of the gap: 50 + 25 = 75"],
            ["2 handfuls of 25 are about 27", "Count by 25s: 25, 50. About 50"],
        ])
    )


FAQ = [
    {"q": "What are benchmarks of 25, 50 and 100 in Grade 2 math in BC?",
     "a": "In the Number area of the BC Grade 2 math curriculum, students use 25, 50 and 100 as friendly numbers. "
          "They decide which benchmark a number is closest to and use benchmarks to estimate how many things are in a group."},
    {"q": "What is a personal referent in math?",
     "a": "A personal referent is something familiar that shows about how many or how much, such as a handful of beans "
          "being about 25 or a class being about 25 students. Children use it to make good estimates without counting."},
    {"q": "Is 48 closer to 25 or 50?",
     "a": "48 is closer to 50. It is only 2 away from 50 but 23 away from 25. Many children say 25 because they look "
          "only at the 4 in the tens place."},
    {"q": "How can I practise benchmarks of 25, 50 and 100 at home?",
     "a": "Grab a handful of beans or pasta and count it, then ask: about how many are in 2 or 4 handfuls? "
          "Count by 25s with quarters, and ask whether numbers like 47 or 92 are closer to 25, 50 or 100."},
]


def gen_unit():
    rnd = random.Random(52802)
    sets = [set_closest(), set_estimate(rnd), set_halfway(), set_quarters(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            key = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
            m = re.search(r"aria-label='(\d+) (beans|marbles) spread out", it["q"])
            if m:
                tag = "<ellipse" if m.group(2) == "beans" else "r='7.5'"
                assert it["q"].count(tag) == int(m.group(1))
            m = re.search(r"with (\d+) marbles in it", it["q"])
            if m:
                assert it["q"].count("r='5.6'") == int(m.group(1))
            m = re.search(r"aria-label='a jar with (\d+) marbles and a jar with (\d+) marbles", it["q"])
            if m:
                assert it["q"].count("r='5.6'") == int(m.group(1)) + int(m.group(2))
            m = re.search(r"100 spaces and (\d+) cars", it["q"])
            if m:
                assert it["q"].count("rx='3' fill='%s'" % BLUE) == int(m.group(1))
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "benchmarks-25-50-and-100", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 2 Benchmarks of 25, 50 and 100: Closest Number, Halfway and Estimating",
        "seo_title": "Grade 2 Benchmarks of 25, 50 and 100 Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Benchmarks of 25, 50 and 100",
        "domain": "Number",
        "standard_code": "Grade 2: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Benchmarks of 25, 50, and 100 and personal referents",
        "meta_desc": "Free Grade 2 math worksheets on benchmarks of 25, 50 and 100 for the BC curriculum: find the closest "
                     "benchmark on a number line, estimate jars and trays of beans, learn that halfway to 100 is 50, "
                     "count by 25s with quarters and use personal referents in word problems. 100 questions with an answer key.",
        "key_big": "25, 50 and 100 are friendly numbers. Find the one that is closest: 48 is closest to 50.",
        "key_sub": "Halfway to 100 is 50. Count by 25s: 25, 50, 75, 100. A handful of beans is about 25, "
                   "so 4 handfuls are about 100.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
