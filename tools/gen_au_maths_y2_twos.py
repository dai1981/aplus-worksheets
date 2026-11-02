# -*- coding: utf-8 -*-
"""
AU Year 2 Maths (Australian Curriculum v9.0, AC9M2A03): twos, doubling and halving.
  python3 tools/gen_au_maths_y2_twos.py
Every count, product, double, half and quotient is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Year 2: very short sentences for 7-8 year olds, numbers to 1000, a picture in most questions.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
RED = "#c0392b"
BLUE = "#2f6db5"
GOLD = "#e3a81b"
INK = "#2b2b2b"
GREY = "#9a948c"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
X = "×"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set.
    Picture-label questions (A, B, C, D) keep that order: the picture is drawn with the answer at the target."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for i, (it, t) in enumerate(zip(s["items"], targets)):
            if "_abcd" in it:
                s["items"][i] = it["_abcd"](t)
                continue
            c = it["c"]
            wrong = [x for k, x in enumerate(c) if k != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, large=None):
    if large is None:
        large = w > 2.2 * h
    return ("<svg %sxmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>"
            % ("data-pf='lg' " if large else "", w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def calc(expr):
    assert re.fullmatch(r"[0-9 +×÷−]+", expr), expr
    return eval(expr.replace(X, "*").replace("÷", "/").replace("−", "-"))


def twos(k, start=2):
    return ", ".join(str(start + 2 * i) for i in range(k))


# ------------------------------------------------------------ figures
def sock(x, y, col):
    """sock 22 wide, 36 tall; top-left at x, y. Toe points left."""
    return ("<path d='M%d %d h12 v24 q0 10 -10 10 h-8 q-4 0 -4 -5 q0 -5 5 -6 h5 v-23 z' fill='%s' stroke='%s' "
            "stroke-width='1.5' stroke-linejoin='round'/>" % (x + 8, y, col, INK)
            + "<rect x='%d' y='%d' width='12' height='5' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x + 8, y, INK))


def shoe(x, y, col):
    """runner 26 wide, 18 tall; top-left at x, y. Toe points right."""
    return ("<path d='M%d %d v-12 q0 -4 4 -4 h5 q2 6 8 6 q6 1 9 7 v5 z' fill='%s' stroke='%s' stroke-width='1.5' "
            "stroke-linejoin='round'/>" % (x, y + 16, col, INK)
            + "<rect x='%d' y='%d' width='26' height='3' rx='1.5' fill='#fff' stroke='%s' stroke-width='1.2'/>"
            % (x, y + 15, INK))


def mitten(x, y, col, flip=False):
    """mitten 20 wide, 30 tall."""
    if flip:
        d = "M%d %d v-16 q0 -8 7 -8 q7 0 7 8 v4 l3 -3 q3 -2 4 1 l-4 9 v5 z" % (x + 3, y + 30)
    else:
        d = "M%d %d v-16 q0 -8 -7 -8 q-7 0 -7 8 v4 l-3 -3 q-3 -2 -4 1 l4 9 v5 z" % (x + 17, y + 30)
    return ("<path d='%s' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>" % (d, col, INK)
            + "<rect x='%d' y='%d' width='14' height='4' fill='#fff' stroke='%s' stroke-width='1.2'/>"
            % (x + 3, y + 27, INK))


ITEM = {  # kind: (draw, width of one item, height, colours)
    "socks": (sock, 22, 36, [BLUE, RED, GREEN, GOLD, "#8e44ad", "#16a085", "#d35400", "#7f8c8d"]),
    "shoes": (shoe, 26, 20, [RED, BLUE, GREEN, GOLD, "#8e44ad", "#16a085", "#d35400", "#7f8c8d"]),
    "gloves": (None, 20, 30, [RED, BLUE, GREEN, GOLD, "#8e44ad", "#16a085", "#d35400", "#7f8c8d"]),
}


def pairs_svg(n, kind, boxed=True, per_row=4):
    """n pairs of socks / shoes / gloves; each pair in a dashed box."""
    draw, w, h, cols = ITEM[kind]
    gap_in, pad, gap = 4, 5, 8
    bw, bh = 2 * w + gap_in + 2 * pad, h + 2 * pad
    per_row = min(per_row, n)
    nrows = (n + per_row - 1) // per_row
    W = per_row * bw + (per_row - 1) * gap + 4
    H = nrows * bh + (nrows - 1) * gap + 4
    s = []
    for i in range(n):
        r, c = divmod(i, per_row)
        x, y = 2 + c * (bw + gap), 2 + r * (bh + gap)
        if boxed:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='1.5' "
                     "stroke-dasharray='4 3'/>" % (x, y, bw, bh, GREY))
        col = cols[i % len(cols)]
        if kind == "gloves":
            s.append(mitten(x + pad, y + pad, col) + mitten(x + pad + w + gap_in, y + pad, col, flip=True))
        else:
            s.append(draw(x + pad, y + pad, col) + draw(x + pad + w + gap_in, y + pad, col))
    return svg_wrap(W, H, "".join(s), "%d pairs of %s" % (n, kind))


def number_line_svg(top, jumps, start=0):
    """number line 0..top, labels every 2, with jumps of 2 from start."""
    u, o, base = 22, 14, 64
    W = top * u + 2 * o
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (o - 6, base, o + top * u + 6, base, INK)]
    for k in range(top + 1):
        x = o + k * u
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, base - (7 if k % 2 == 0 else 4), x, base + (7 if k % 2 == 0 else 4), INK, 2 if k % 2 == 0 else 1))
        if k % 2 == 0:
            s.append(text(x, base + 24, str(k), 14))
    for j in range(jumps):
        x1, x2 = o + (start + 2 * j) * u, o + (start + 2 * j + 2) * u
        s.append("<path d='M%d %d Q%d %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, base - 4, (x1 + x2) / 2, base - 40, x2, base - 4, RED))
        s.append("<path d='M%d %d l-7 -3 l3 6 z' fill='%s'/>" % (x2, base - 4, RED))
    return svg_wrap(W, base + 32, "".join(s), "number line from 0 to %d with %d jumps of 2" % (top, jumps), large=True)


def dots(x0, y0, rows, cols, cell, col=GREEN):
    return "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                   % (x0 + c * cell + cell // 2, y0 + r * cell + cell // 2, cell // 3, col)
                   for r in range(rows) for c in range(cols))


def array_svg(rows, cols, cell=24):
    o = 6
    W, H = cols * cell + 2 * o, rows * cell + 2 * o
    return svg_wrap(W, H, dots(o, o, rows, cols, cell),
                    "array of %d rows with %d dots in each row" % (rows, cols), large=cols >= 7)


def arrays_abcd_svg(shapes):
    """four small arrays labelled A to D in one picture."""
    cell, o, gap, lab = 16, 4, 18, 22
    widths = [c * cell for r, c in shapes]
    H = max(r * cell for r, c in shapes) + lab + 2 * o
    W = sum(widths) + gap * 3 + 2 * o
    s, x = [], o
    for (r, c), w, L in zip(shapes, widths, "ABCD"):
        s.append(text(x + w / 2, o + 16, L, 16))
        s.append(dots(x, o + lab, r, c, cell))
        x += w + gap
    return svg_wrap(W, H, "".join(s), "four arrays labelled A, B, C and D", large=True)


PIPS = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (0, 2), (2, 0), (2, 2)],
        5: [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)], 6: [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]}


def domino_svg(n):
    """a double domino: n pips on each half."""
    S, o = 54, 4
    s = ["<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='2.5'/>"
         % (o, o, 2 * S, S, INK),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (o + S, o + 6, o + S, o + S - 6, INK)]
    for half in (0, 1):
        for r, c in PIPS[n]:
            s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (o + half * S + 12 + c * 15, o + 12 + r * 15, INK))
    return svg_wrap(2 * S + 2 * o, S + 2 * o, "".join(s), "double domino with %d dots on each side" % n)


def frame_dots(x0, y0, n, cell, col):
    """n counters in rows of 5"""
    return "".join("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
                   % (x0 + (i % 5) * cell + cell // 2, y0 + (i // 5) * cell + cell // 2, cell // 2 - 3, col, INK)
                   for i in range(n))


def mirror_svg(n):
    """n counters, a dashed mirror line, then the same n counters again."""
    cell, o, gap = 20, 6, 24
    cols = min(n, 5)
    rows = (n + 4) // 5
    w = cols * cell
    W, H = 2 * w + gap + 2 * o, rows * cell + 2 * o
    s = [frame_dots(o, o, n, cell, RED), frame_dots(o + w + gap, o, n, cell, BLUE),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
         % (o + w + gap // 2, 2, o + w + gap // 2, H - 2, GREY)]
    return svg_wrap(W, H, "".join(s), "%d red counters and %d blue counters" % (n, n), large=False)


def rods_svg(tens, ones):
    """base-ten blocks: tens rods and ones cubes"""
    C, rw, gap, o = 11, 13, 7, 4
    s = []
    for i in range(tens):
        x = o + i * (rw + gap)
        for k in range(10):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                     % (x, o + k * C, rw, C, FILL, GREEN))
    x0 = o + tens * (rw + gap) + (6 if tens else 0)
    for j in range(ones):
        r, c = divmod(j, 2)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (x0 + c * (C + 3), o + 10 * C - (r + 1) * (C + 3) + 3, C, C, GOLD, INK))
    W = x0 + (min(ones, 2) * (C + 3) if ones else -gap) + o
    return svg_wrap(W, 10 * C + 2 * o, "".join(s), "%d %s and %d %s" % (tens, "ten" if tens == 1 else "tens", ones, "one" if ones == 1 else "ones"), large=False)


def share_svg(n, col=RED, noun="counters"):
    """n counters shared equally onto 2 plates."""
    h = n // 2
    cell, o, gap = 20, 6, 20
    cols = min(h, 4)
    rows = (h + cols - 1) // cols
    pw, ph = cols * cell + 16, rows * cell + 16
    W, H = 2 * pw + gap + 2 * o, ph + 2 * o
    s = []
    for p in (0, 1):
        x = o + p * (pw + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
                 % (x, o, pw, ph, min(pw, ph) // 2, GREY))
        s.append("".join("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='1.2'/>"
                         % (x + 8 + (i % cols) * cell + cell // 2, o + 8 + (i // cols) * cell + cell // 2, col, INK)
                         for i in range(h)))
    return svg_wrap(W, H, "".join(s), "%d %s shared onto 2 plates" % (n, noun), large=False)


def bike(x, y):
    """bike 56 wide, 34 tall"""
    return ("<circle cx='%d' cy='%d' r='11' fill='none' stroke='%s' stroke-width='3'/>" % (x + 12, y + 22, INK)
            + "<circle cx='%d' cy='%d' r='11' fill='none' stroke='%s' stroke-width='3'/>" % (x + 44, y + 22, INK)
            + "<path d='M%d %d L%d %d L%d %d L%d %d Z M%d %d L%d %d M%d %d L%d %d' fill='none' stroke='%s' "
              "stroke-width='2.5' stroke-linejoin='round'/>"
            % (x + 12, y + 22, x + 22, y + 8, x + 40, y + 8, x + 28, y + 22, x + 40, y + 8, x + 44, y + 22,
               x + 22, y + 8, x + 20, y + 3, RED)
            + "<path d='M%d %d h8 M%d %d l2 -6 h5' fill='none' stroke='%s' stroke-width='2.5' stroke-linecap='round'/>"
            % (x + 16, y + 3, x + 40, y + 8, INK))


def bikes_svg(k):
    o, w, gap = 4, 56, 8
    per_row = min(k, 3)
    nrows = (k + per_row - 1) // per_row
    W = per_row * w + (per_row - 1) * gap + 2 * o
    H = nrows * 36 + (nrows - 1) * gap + 2 * o
    body = "".join(bike(o + (i % per_row) * (w + gap), o + (i // per_row) * (36 + gap)) for i in range(k))
    return svg_wrap(W, H, body, "%d bikes" % k)


# ------------------------------------------------------------ mistakes
def fact_cands(a, rnd):
    """a × 2. Real mistakes: one group too many or too few, adding 2, using the 3s."""
    p = 2 * a
    pool = [(a + 1) * 2, (a - 1) * 2, a + 2, 3 * a]
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [p + 1, p - 1]


def fact_q(a, rnd):
    x, y = (a, 2) if rnd.random() < 0.5 else (2, a)
    return mcq("%d %s %d = ?" % (x, X, y), 2 * a, fact_cands(a, rnd),
               "%s 2 means double. Double %d: %d + %d = <b>%d</b>." % (X, a, a, a, 2 * a))


def seq_q(seq, wrong, back=False):
    step = -2 if back else 2
    nxt = seq[-1] + step
    assert all(seq[i + 1] - seq[i] == step for i in range(len(seq) - 1)) and nxt not in wrong
    word = "back" if back else "on"
    e = "Each number is 2 %s than the one before: %d %s 2 = <b>%d</b>." % (
        "less" if back else "more", seq[-1], "−" if back else "+", nxt)
    return mcq("Count %s in twos. What comes next?<br>%s, ?" % (word, ", ".join(map(str, seq))), nxt, wrong, e)


# ============================================================ set 1: counting in twos
def set_count(rnd):
    its = []
    for n, kind in [(3, "socks"), (4, "shoes"), (6, "socks"), (5, "shoes"), (7, "socks"), (8, "shoes")]:
        p = 2 * n
        e = ("Each pair has 2 %s. Count in twos: %s. So there are <b>%d %s</b>. %d counts the pairs, not the %s."
             % (kind, twos(n), p, kind, n, kind))
        its.append(mcq(fig(pairs_svg(n, kind)) + "How many %s are there?" % kind, p,
                       [n, p + 2, p - 2, n + 2], e))
    its.append(mcq(fig(pairs_svg(5, "socks", boxed=False, per_row=5)) + "How many <b>pairs</b> of socks are there?",
                   5, [10, 4, 6], "There are 10 socks. A pair is 2 socks. Count in twos: 2, 4, 6, 8, 10. "
                                  "That is 5 twos, so there are <b>5 pairs</b>. 10 counts the socks, not the pairs."))
    its.append(mcq("How many socks are in 10 pairs?", 20, [10, 12, 22],
                   "Count in twos 10 times: %s. So there are <b>20 socks</b>. 12 is 10 + 2. That adds 2, but each pair has 2." % twos(10)))
    its.append(seq_q([2, 4, 6, 8], [9, 12, 6]))
    its.append(seq_q([12, 14, 16], [17, 20, 14]))
    its.append(seq_q([34, 36, 38], [39, 42, 36]))
    its.append(seq_q([20, 18, 16], [15, 12, 18], back=True))
    its.append(mcq("Count in twos. What is the missing number?<br>8, 10, ?, 14", 12, [11, 13, 16],
                   "The numbers go up by 2. 10 + 2 = <b>12</b>. Check: 12 + 2 = 14."))
    its.append(seq_q([94, 96, 98], [99, 102, 108]))
    its.append(seq_q([104, 106, 108], [109, 112, 118]))
    its.append(mcq("Count on in twos from 1. What comes next?<br>1, 3, 5, 7, ?", 9, [8, 10, 11],
                   "Each number is 2 more: 7 + 2 = <b>9</b>. Counting in twos from 1 gives the odd numbers."))
    right, wrong = "6, 8, 10, 12", ["6, 7, 8, 9", "6, 9, 12, 15", "6, 10, 14, 18"]
    for l in [right] + wrong:
        v = [int(t) for t in l.split(", ")]
        assert all(v[i + 1] - v[i] == 2 for i in range(3)) == (l == right)
    its.append(mcq("Which list counts in twos?", right, wrong,
                   "In <b>6, 8, 10, 12</b> each number is 2 more than the one before. "
                   "The other lists go up by 1, 3 or 4."))
    its.append(mcq("Which number do you say when you count in twos from 0?", 14, [13, 15, 21],
                   "Counting in twos from 0: 2, 4, 6, 8, 10, 12, <b>14</b>. These numbers are even. 13, 15 and 21 are odd."))
    for k in (5, 7):
        nm = ["Ava", "Lachlan"][k == 7]
        e = "Each jump is 2. Count in twos %d times: %s. %s lands on <b>%d</b>." % (k, twos(k), nm, 2 * k)
        its.append(mcq(fig(number_line_svg(20, k)) + "%s makes %d jumps of 2 from 0. Where does %s land?"
                       % (nm, k, "she" if nm == "Ava" else "he"), 2 * k, [k, 2 * k + 2, 2 * k - 2, k + 2], e))
    assert len(its) == 20, len(its)
    return {"title": "Counting in twos", "items": its}


# ============================================================ set 2: 2 × facts and arrays
def set_facts(rnd):
    its = []
    for n in (3, 5, 9):
        p = 2 * n
        e = "There are 2 rows of %d. Double %d: %d + %d = %d. So 2 %s %d = <b>%d</b>." % (n, n, n, n, p, X, n, p)
        its.append(mcq(fig(array_svg(2, n)) + "How many dots are there?", p, [n + 2, p + 2, p - 2, n], e))
    for n in (6, 8):
        p = 2 * n
        right = "2 %s %d" % (X, n)
        wrong = ["2 + %d" % n, "2 %s %d" % (X, n + 1), "2 %s %d" % (X, n - 1)]
        assert calc(right) == p and all(calc(w) != p for w in wrong)
        e = ("There are 2 rows with %d dots in each row. That is 2 %s %d = %d. "
             "2 + %d adds the numbers. It does not match the rows." % (n, X, n, p, n))
        its.append(mcq(fig(array_svg(2, n)) + "Which matches the array?", right, wrong, e))

    def abcd(t):
        wrong = [(2, 5), (1, 6), (4, 4)]
        shapes = wrong[:t] + [(2, 4)] + wrong[t:]
        assert sum(1 for r, c in shapes if r * c == 8) == 1
        L = "ABCD"[t]
        e = ("2 %s 4 means 2 rows of 4. Picture <b>%s</b> has 2 rows with 4 dots in each row: 4 + 4 = 8."
             % (X, L))
        return {"q": fig(arrays_abcd_svg(shapes)) + "Which array shows 2 %s 4?" % X, "c": ["A", "B", "C", "D"],
                "a": t, "e": e}
    its.append({"_abcd": abcd})

    its += [fact_q(a, rnd) for a in rnd.sample([4, 7, 10, 6, 8, 3, 9, 5], 8)]

    for (expr, ans, wrong) in [("2 %s ? = 12" % X, 6, [10, 24, 5]),
                               ("? %s 2 = 14" % X, 7, [12, 28, 8]),
                               ("2 %s ? = 18" % X, 9, [16, 36, 8])]:
        total = int(expr.split("= ")[1])
        assert 2 * ans == total
        its.append(mcq(expr, ans, wrong,
                       "Ask: double what makes %d? %d + %d = %d, so ? = <b>%d</b>." % (total, ans, ans, total, ans)))
    its.append(mcq("2 %s 8 = 8 %s ?" % (X, X), 2, [8, 16, 10],
                   "You can turn a multiplication around. 2 %s 8 = 16 and 8 %s 2 = 16. So ? = <b>2</b>." % (X, X)))
    assert 2 * 8 == 8 * 2
    right, wrong = "6 + 6", ["2 + 6", "6 + 6 + 6", "2 + 2 + 2"]
    assert calc(right) == 12 and all(calc(w) != 12 for w in wrong) and len({calc(w) for w in wrong}) == 3
    its.append(mcq("Which is the same as 2 %s 6?" % X, right, wrong,
                   "2 %s 6 is two sixes: <b>6 + 6</b> = 12. 2 + 6 = 8, so it is not the same." % X))
    right, wrong = 13, [12, 16, 18]
    assert right % 2 == 1 and all(v % 2 == 0 and v // 2 <= 10 for v in wrong)
    its.append(mcq("Which number is <b>not</b> an answer to a twos fact?", right, wrong,
                   "Twos answers are always even: 2 %s 6 = 12, 2 %s 8 = 16, 2 %s 9 = 18. "
                   "<b>13</b> is odd, so it is not a twos answer." % (X, X, X)))
    assert len(its) == 20, len(its)
    return {"title": "2 × facts and arrays", "items": its}


# ============================================================ set 3: doubles and doubling
def dbl_e(n):
    return "Double %d means %d + %d. %d + %d = <b>%d</b>." % (n, n, n, n, n, 2 * n)


def set_double(rnd):
    its = []
    for n, wrong in [(3, [5, 3, 7]), (4, [6, 4, 2]), (6, [8, 6, 11])]:
        its.append(mcq(fig(domino_svg(n)) + "This domino shows double %d. How many dots in all?" % n, 2 * n, wrong,
                       "Each side has %d dots. %s Count both sides, not just one." % (n, dbl_e(n))))
    for n, wrong in [(5, [7, 5, 11]), (7, [9, 7, 13]), (9, [11, 9, 17])]:
        its.append(mcq(fig(mirror_svg(n)) + "There are %d red and %d blue counters. What is double %d?" % (n, n, n),
                       2 * n, wrong, dbl_e(n) + " %d counts only one colour." % n))
    its.append(mcq("Double 8 = ?", 16, [10, 4, 18],
                   "%s 10 is 8 + 2. That adds 2. Double means add the same number again." % dbl_e(8)))
    right, wrong = "6 + 6", ["6 + 2", "6 + 1", "3 + 3"]
    assert calc(right) == 12 and all(calc(w) != 12 for w in wrong)
    its.append(mcq("Which is the same as double 6?", right, wrong,
                   "Double 6 means 6 and 6 more: <b>6 + 6</b> = 12. 6 + 2 = 8 only adds 2."))
    its.append(mcq("Jack says double 6 is 8. What did he do?", "He added 2",
                   ["He halved 6", "He took away 2", "Nothing, he is right"],
                   "6 + 2 = 8, so <b>he added 2</b>. Double 6 is 6 + 6 = 12."))
    for t, wrong in [(20, [22, 10, 30]), (30, [32, 15, 50]), (50, [52, 25, 90])]:
        its.append(mcq(fig(rods_svg(t // 10, 0)) + "This shows %d. What is double %d?" % (t, t), 2 * t, wrong,
                       "%d tens doubled is %d tens. %d + %d = <b>%d</b>." % (t // 10, t // 5, t, t, 2 * t)))
    for n, wrong in [(13, [15, 23, 16]), (24, [26, 44, 12]), (35, [37, 65, 60])]:
        tn, on = n - n % 10, n % 10
        its.append(mcq(fig(rods_svg(tn // 10, on)) + "This shows %d. What is double %d?" % (n, n), 2 * n, wrong,
                       "Double the tens: double %d = %d. Double the ones: double %d = %d. %d + %d = <b>%d</b>."
                       % (tn, 2 * tn, on, 2 * on, 2 * tn, 2 * on, 2 * n)))
    its.append(mcq("Double 45 = ?", 90, [47, 85, 80],
                   "Double 40 = 80. Double 5 = 10. 80 + 10 = <b>90</b>. 85 forgets to double the 5."))
    assert 2 * 45 == 90
    its.append(mcq("Double 100 = ?", 200, [102, 50, 110],
                   "100 + 100 = <b>200</b>. 50 is half of 100, not double."))
    its.append(mcq("Double 200 = ?", 400, [202, 100, 220],
                   "2 hundreds doubled is 4 hundreds. 200 + 200 = <b>400</b>."))
    its.append(mcq("Double ? = 14", 7, [28, 12, 16],
                   "Ask: what number added to itself makes 14? 7 + 7 = 14, so ? = <b>7</b>."))
    assert 7 + 7 == 14
    its.append(mcq("Which is the same as 2 %s 9?" % X, "double 9", ["9 + 2", "half of 18", "double 2"],
                   "2 %s 9 is two nines: 9 + 9 = 18. That is <b>double 9</b>. 9 + 2 = 11 and half of 18 = 9." % X))
    assert 2 * 9 == 18 and 9 + 2 != 18 and 18 // 2 != 18 and 2 * 2 != 18
    assert len(its) == 20, len(its)
    return {"title": "Doubles and doubling", "items": its}


# ============================================================ set 4: halving and ÷ 2
def set_half(rnd):
    its = []
    for n in (8, 10, 12, 16):
        h = n // 2
        its.append(mcq(fig(share_svg(n)) + "%d counters are shared equally onto 2 plates. How many on each plate?" % n,
                       h, [n, n - 2, h + 1, 2 * n],
                       "%d %s 2 = %d. Half of %d is %d. Each plate has <b>%d</b>. Check: double %d is %d."
                       % (n, "÷", h, n, h, h, h, n)))
    its.append(mcq("Half of 14 = ?", 7, [6, 12, 28],
                   "Double 7 is 14, so half of 14 is <b>7</b>. 6 is a counting slip: 6 + 6 = 12, not 14."))
    for n, wrong in [(18, [16, 8, 36]), (6, [4, 12, 2]), (20, [18, 40, 5])]:
        h = n // 2
        its.append(mcq("%d ÷ 2 = ?" % n, h, wrong,
                       "÷ 2 means halve. Think: double what makes %d? %d + %d = %d, so %d ÷ 2 = <b>%d</b>."
                       % (n, h, h, n, n, h)))
    its.append(mcq("Double 11 is 22. So half of 22 is ?", 11, [44, 20, 12],
                   "Halving undoes doubling. Double 11 = 22, so half of 22 = <b>11</b>."))
    for n, wrong in [(40, [80, 38, 10]), (60, [120, 58, 20]), (80, [160, 78, 20])]:
        h = n // 2
        its.append(mcq(fig(rods_svg(n // 10, 0)) + "This shows %d. What is half of %d?" % (n, n), h, wrong,
                       "Share the %d tens into 2 equal groups: %d tens each. Half of %d is <b>%d</b>."
                       % (n // 10, n // 20, n, h)))
    its.append(mcq("Half of 30 = ?", 15, [60, 28, 13],
                   "30 is 3 tens. Half of 20 is 10. Half of the last 10 is 5. 10 + 5 = <b>15</b>. Check: 15 + 15 = 30."))
    assert 15 * 2 == 30
    for n, wrong in [(48, [28, 46, 96]), (26, [16, 24, 52])]:
        tn, on = n - n % 10, n % 10
        its.append(mcq(fig(rods_svg(tn // 10, on)) + "This shows %d. What is half of %d?" % (n, n), n // 2, wrong,
                       "Halve the tens: half of %d = %d. Halve the ones: half of %d = %d. %d + %d = <b>%d</b>."
                       % (tn, tn // 2, on, on // 2, tn // 2, on // 2, n // 2)))
        assert tn % 20 == 0 and on % 2 == 0
    its.append(mcq("Half of 100 = ?", 50, [200, 98, 25],
                   "50 + 50 = 100, so half of 100 is <b>50</b>. 200 is double 100, not half."))
    its.append(mcq("Half of 200 = ?", 100, [400, 198, 50],
                   "100 + 100 = 200, so half of 200 is <b>100</b>."))
    its.append(mcq("? ÷ 2 = 7", 14, [9, 5, 12],
                   "Halving undoes doubling. Double 7 is 14, so ? = <b>14</b>. Check: 14 ÷ 2 = 7."))
    right, wrong = 15, [14, 16, 20]
    assert right % 2 == 1 and all(w % 2 == 0 for w in wrong)
    its.append(mcq("Which number <b>cannot</b> be shared equally between 2?", right, wrong,
                   "<b>15</b> is odd. 7 + 7 = 14, so 1 is left over. Even numbers like 14, 16 and 20 share equally."))
    its.append(mcq("Mia says half of 12 is 24. What did she do?", "She doubled 12",
                   ["She added 2", "She took away 2", "Nothing, she is right"],
                   "12 + 12 = 24, so <b>she doubled 12</b>. Half of 12 is 6, because 6 + 6 = 12."))
    assert len(its) == 20, len(its)
    return {"title": "Halving and ÷ 2 facts", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        u = (lambda v: "$%d" % v) if unit == "$" else (lambda v: "%d %s" % (v, unit))
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    w(fig(bikes_svg(4)) + "A bike has 2 wheels. How many wheels do these bikes have?", 8, "wheels", [6, 4, 10],
      "4 bikes with 2 wheels each: 2, 4, 6, 8. 4 %s 2 = <b>8</b>. 6 is 4 + 2, which adds 2." % X, 4 * 2)
    w("There are 7 bikes in the school bike rack. How many wheels is that?", 14, "wheels", [9, 12, 16],
      "7 %s 2 is double 7: 7 + 7 = <b>14</b>. 9 is 7 + 2, which adds 2." % X, 7 * 2)
    nm, he, his = P.next()
    w(fig(pairs_svg(6, "gloves", per_row=3)) + "%s has 6 pairs of gloves for winter. How many gloves is that?" % nm,
      12, "gloves", [8, 6, 14], "A pair is 2. 6 pairs is double 6: 6 + 6 = <b>12</b>. 6 counts the pairs.", 6 * 2)
    nm, he, his = P.next()
    w("%s takes 3 pairs of thongs to the beach. How many thongs is that?" % nm, 6, "thongs", [5, 3, 8],
      "A pair is 2. Count in twos: 2, 4, 6. 3 %s 2 = <b>6</b>." % X, 3 * 2)
    nm, he, his = P.next()
    w(fig(share_svg(16, noun="strawberries")) + "%s shares 16 strawberries equally with a friend. How many does each child get?" % nm,
      8, "strawberries", [16, 14, 32], "Sharing between 2 means halve. 16 ÷ 2 = 8. Check: 8 + 8 = 16. "
      "Each child gets <b>8 strawberries</b>.", 16 // 2)
    nm, he, his = P.next()
    w("%s and %s brother share 20 stickers equally. How many stickers does each child get?" % (nm, his), 10,
      "stickers", [20, 18, 40], "20 ÷ 2 = 10. Check: 10 + 10 = 20. Each child gets <b>10 stickers</b>.", 20 // 2)
    w("A kookaburra has 2 wings. How many wings do 5 kookaburras have?", 10, "wings", [7, 8, 12],
      "Count in twos: 2, 4, 6, 8, 10. 5 %s 2 = <b>10</b>. 7 is 5 + 2, which adds 2." % X, 5 * 2)
    w("A kangaroo hops on its 2 back legs. How many back legs do 9 kangaroos have?", 18, "legs", [11, 16, 20],
      "9 %s 2 is double 9: 9 + 9 = <b>18</b>." % X, 9 * 2)
    w("At the swimming carnival, 12 students swim in pairs. How many pairs are there?", 6, "pairs", [12, 10, 24],
      "12 ÷ 2 = 6. Count in twos: 2, 4, 6, 8, 10, 12. That is 6 twos, so <b>6 pairs</b>.", 12 // 2)
    w("At the sausage sizzle, 8 bread rolls are cut in half. How many halves are there?", 16, "halves",
      [4, 10, 8], "Each roll makes 2 halves. 8 %s 2 is double 8: 8 + 8 = <b>16</b>. 4 is half of 8, not double." % X,
      8 * 2)
    nm, he, his = P.next()
    w("A fruit cup costs $2 at the school canteen. %s buys 5 fruit cups. How much does %s spend?" % (nm, he), 10, "$",
      [7, 12, 8], "5 %s $2: count in twos 2, 4, 6, 8, 10. %s spends <b>$10</b>. $7 is 5 + 2." % (X, he.capitalize()), 5 * 2)
    a, he1, _ = P.next()
    b, he2, _ = P.next()
    w("%s has 9 marbles. %s has double that. How many marbles does %s have?" % (a, b, b), 18, "marbles", [11, 16, 20],
      "Double 9 is 9 + 9 = <b>18</b>. 11 is 9 + 2. That adds 2 instead of doubling.", 2 * 9)
    nm, he, his = P.next()
    w("%s has 30 footy cards. %s gives half to %s sister. How many cards does %s give away?" % (nm, he.capitalize(), his, he),
      15, "cards", [60, 28, 13], "Half of 30: 15 + 15 = 30. So %s gives away <b>15 cards</b>." % he, 30 // 2)
    nm, he, his = P.next()
    w("%s reads 12 pages on Monday. On Tuesday %s reads half as many. How many pages on Tuesday?" % (nm, he), 6,
      "pages", [24, 10, 14], "Half as many means halve. Half of 12 is <b>6</b>, because 6 + 6 = 12. "
      "24 is double 12, not half.", 12 // 2)
    a, _, _ = P.next()
    b, he2, _ = P.next()
    w("%s has 25 shells from the beach. %s has double that. How many shells does %s have?" % (a, b, b), 50, "shells",
      [27, 45, 52], "Double 20 = 40. Double 5 = 10. 40 + 10 = <b>50</b>. 45 forgets to double the 5.", 2 * 25)
    nm, he, his = P.next()
    w("Mum hangs 11 pairs of socks on the clothesline. How many socks is that?", 22, "socks", [13, 11, 20],
      "Double 11: 11 + 11 = <b>22</b>. 13 is 11 + 2, which adds 2.", 11 * 2)
    w("18 children make 2 equal teams for cricket. How many children are in each team?", 9, "children",
      [18, 16, 36], "18 ÷ 2 = 9. Check: 9 + 9 = 18. There are <b>9 children</b> in each team.", 18 // 2)
    w("There are 4 sets of twins in Year 2. How many children is that?", 8, "children", [4, 6, 10],
      "Twins come in twos. Count in twos: 2, 4, 6, 8. 4 %s 2 = <b>8</b>." % X, 4 * 2)
    nm, he, his = P.next()
    w("%s has 4 pairs of shoes. %s gives 1 pair away. How many shoes are left?" % (nm, he.capitalize()), 6, "shoes",
      [7, 3, 8], "4 pairs − 1 pair = 3 pairs. 3 %s 2 = <b>6 shoes</b>. 7 takes away 1 shoe, but a pair is 2 shoes." % X,
      (4 - 1) * 2)
    nm, he, his = P.next()
    w("%s has 10 cherries. %s eats 2, then shares the rest equally with a friend. How many does each child get?"
      % (nm, he.capitalize()), 4, "cherries", [5, 8, 3],
      "10 − 2 = 8 left. Half of 8 is 4. Each child gets <b>4 cherries</b>. 5 is half of 10, but 2 were eaten first.",
      (10 - 2) // 2)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: twos, doubles and halves", "items": its}


# ============================================================ lesson
def body_html():
    rows = [["2 %s %d = %d" % (X, k, 2 * k), "double %d = %d" % (k, 2 * k), "%d ÷ 2 = %d" % (2 * k, k)]
            for k in range(1, 11)]
    return (
        "<h2>Count in twos</h2>"
        "<p>Socks, shoes and gloves come in <b>pairs</b>. A pair is 2. "
        "To count them fast, count in twos: 2, 4, 6, 8, 10.</p>"
        + "<figure class='sn-fig'>" + pairs_svg(4, "socks")
        + "<figcaption>4 pairs of socks: 2, 4, 6, 8. That is 8 socks.</figcaption></figure>"
        + "<h2>Times 2 means double</h2>"
        "<p>2 %s 6 means 2 rows of 6, or two sixes. That is the same as <b>double 6</b>: "
        "6 + 6 = 12. You can turn it around: 6 %s 2 = 12 too.</p>" % (X, X)
        + "<figure class='sn-fig'>" + array_svg(2, 6)
        + "<figcaption>2 rows of 6 dots: 6 + 6 = 12. So 2 %s 6 = 12.</figcaption></figure>" % X
        + ex("Example", "Double 8 = ?", "Add 8 and 8 more: 8 + 8 = 16.", "16")
        + "<p>For a bigger number, double the tens, then double the ones, then add.</p>"
        + "<figure class='sn-fig'>" + rods_svg(2, 4)
        + "<figcaption>24 is 2 tens and 4 ones.</figcaption></figure>"
        + ex("Example", "Double 24 = ?", "Double 20 = 40. Double 4 = 8. 40 + 8 = 48.", "48")
        + "<h2>Halving and ÷ 2</h2>"
        "<p>To <b>halve</b>, share into 2 equal groups. ÷ 2 means halve. "
        "Halving undoes doubling: double 7 is 14, so half of 14 is 7.</p>"
        + "<figure class='sn-fig'>" + share_svg(14)
        + "<figcaption>14 shared onto 2 plates: 7 on each plate. 14 ÷ 2 = 7.</figcaption></figure>"
        + ex("Example", "Half of 48 = ?", "Half of 40 = 20. Half of 8 = 4. 20 + 4 = 24.", "24")
        + table(["Twos fact", "Double", "Halve (÷ 2)"], rows)
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding 2: double 8 = 10", "Double means add the same number: 8 + 8 = 16"],
            ["Half of 14 = 6", "Check by doubling: 6 + 6 = 12, not 14. 7 + 7 = 14, so half is 7"],
            ["Mixing up double and half: half of 12 = 24", "Half makes it smaller: half of 12 = 6"],
            ["Counting pairs, not things: 5 pairs of socks = 5 socks", "Each pair is 2: 2, 4, 6, 8, 10 socks"],
        ])
    )


FAQ = [
    {"q": "What multiplication facts do Year 2 students learn in Australia?",
     "a": "The Australian Curriculum (v9.0) asks Year 2 students to recall the multiplication facts for twos and use doubling and halving to find the matching division facts, like 14 ÷ 2 = 7. The 3s, 4s, 5s and 10s come in Year 3."},
    {"q": "Is doubling the same as multiplying by 2?",
     "a": "Yes. Double 8 is 8 + 8 = 16, and 2 × 8 = 16. A common mistake is adding 2 instead, which gives 10."},
    {"q": "How do you halve a 2-digit number?",
     "a": "Halve the tens, halve the ones, then add. Half of 48 is half of 40 (20) plus half of 8 (4), which is 24. Check by doubling: 24 + 24 = 48."},
    {"q": "How can I help my child practise twos, doubling and halving at home?",
     "a": "Count pairs of socks, shoes and thongs in twos, play with double dominoes, and share snacks equally between two people. Ask “What is double 7?” and then “So what is half of 14?”."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            if "data-pf=" not in it["q"]:
                it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(2805)
    P = People(rnd)
    sets = [set_count(rnd), set_facts(rnd), set_double(rnd), set_half(rnd), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            for c in it["c"]:
                for v in re.findall(r"\d+", c):
                    assert int(v) < 1000, it
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "twos-doubling-and-halving", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Twos, Doubling and Halving",
        "seo_title": "Year 2 Twos, Doubling and Halving Worksheets: 2 × Facts and ÷ 2 with Answers",
        "short_title": "Twos, doubling and halving",
        "domain": "Algebra",
        "standard_code": "AC9M2A03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recall and demonstrate proficiency with multiplication facts for twos; extend and apply facts to develop the related division facts using doubling and halving",
        "meta_desc": "Free Year 2 maths worksheets on twos, doubling and halving: counting in twos with pairs, 2 × facts with arrays, doubles, halves, ÷ 2 facts and word problems. 100 questions with an answer key, following the Australian Curriculum.",
        "key_big": "Times 2 means double. Divide by 2 means halve.",
        "key_sub": "Double 8 is 8 + 8 = 16, so 2 × 8 = 16 and 16 ÷ 2 = 8. Doubling is not adding 2, and halving undoes doubling.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "([6-9]|1[0-9]) pairs")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
