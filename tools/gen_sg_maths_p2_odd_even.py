# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Odd and Even Numbers
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 2: Whole Numbers — odd and even numbers)
  python3 tools/gen_sg_maths_p2_odd_even.py
Pair up objects and look for one left over, use the ones digit for numbers up to 1000, find odd and even
numbers in number patterns, add odd and even numbers, and solve word problems in Singapore settings
with bar models.
Wrong answers come from real mistakes: looking at the tens (or hundreds) digit instead of the ones digit,
thinking 0 is not even, forgetting the one left over, thinking odd + odd is odd, and counting the pairs
instead of the objects.
Every count, sum and odd/even label is checked in code. HTML attributes use single quotes.
Primary 2: short sentences for 7-8-year-olds.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
GOLD = "#e3a81b"
INK = "#2b2b2b"
GREY = "#9a948c"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set.
    Items marked 'fixed' (A-D pictures) already have their position; the rest fill the gaps."""
    for s in sets:
        left = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                left[it["a"]] -= 1
        assert min(left.values()) >= 0
        targets = [p for p in range(4) for _ in range(left[p])]
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fixed")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


def cap(s):
    return s[0].upper() + s[1:]


def par(n):
    return "even" if n % 2 == 0 else "odd"


def Par(n):
    return cap(par(n))


def other(p):
    return {"even": "odd", "odd": "even", "Even": "Odd", "Odd": "Even"}[p]


def and_list(xs):
    xs = [str(x) for x in xs]
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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


# ------------------------------------------------------------ figures
PITCH = 28          # one object per 28 x 28 cell; objects are at most 22 wide, so they never touch
KINDS = {"counters": ("counter", "counters", RED),
         "stars": ("star", "stars", GOLD),
         "blocks": ("block", "blocks", GREEN)}


def obj(kind, cx, cy, col=None):
    col = col or KINDS[kind][2]
    if kind == "counters":
        return "<circle cx='%.1f' cy='%.1f' r='10' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, col, INK)
    if kind == "blocks":
        return ("<rect x='%.1f' y='%.1f' width='19' height='19' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (cx - 9.5, cy - 9.5, col, INK))
    pts = []
    for k in range(10):
        r = 11 if k % 2 == 0 else 4.6
        a = math.pi / 2 + k * math.pi / 5
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a) + 1))
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(pts), col, INK)


def pairs_body(x0, y0, n, kind, col=None, outline=False, gx=0):
    """n objects in columns of 2 (pairs). Object i goes to column i // 2, row i % 2,
    so a left-over object sits alone in the top row of the last column."""
    s = []
    cols = (n + 1) // 2
    CP = PITCH + gx
    if outline:
        for c in range(n // 2):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='1.5' "
                     "stroke-dasharray='4 3'/>" % (x0 + c * CP + gx / 2 - 1, y0 - 2, PITCH + 2, 2 * PITCH + 4, GREEN))
        if n % 2:
            s.append("<circle cx='%d' cy='%d' r='13' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x0 + (cols - 1) * CP + gx / 2 + PITCH // 2, y0 + PITCH // 2, RED))
    for i in range(n):
        c, r = divmod(i, 2)
        s.append(obj(kind, x0 + c * CP + gx / 2 + PITCH / 2, y0 + r * PITCH + PITCH / 2, col))
    return "".join(s), cols * CP, 2 * PITCH


def pairs_svg(n, kind):
    o = 6
    body, w, h = pairs_body(o, o, n, kind)
    return svg_wrap(w + 2 * o, h + 2 * o, body, "%d %s in pairs" % (n, KINDS[kind][1]))


def scattered_svg(n, kind, rnd):
    """n objects placed at random cells of a 6 x 3 grid (34 px cells) with a small jitter. No overlap."""
    C, cols, rows, o = 34, 6, 3, 4
    assert n <= cols * rows
    cells = rnd.sample(range(cols * rows), n)
    s = []
    for k in sorted(cells):
        r, c = divmod(k, cols)
        jx, jy = rnd.randint(-5, 5), rnd.randint(-5, 5)
        s.append(obj(kind, o + c * C + C / 2 + jx, o + r * C + C / 2 + jy))
    return svg_wrap(cols * C + 2 * o, rows * C + 2 * o, "".join(s), "%d %s mixed up" % (n, KINDS[kind][1]))


def abcd_svg(counts, kind):
    """2 x 2 grid of groups labelled A to D. Each group is drawn in pairs."""
    assert len(counts) == 4 and max(counts) <= 12
    LW, CW, CH = 26, 26 + 6 * PITCH + 8, 2 * PITCH + 16
    W, H = 2 * CW, 2 * CH
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CW, CW, H - 4, GREY),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CH, W - 4, CH, GREY)]
    for k, n in enumerate(counts):
        x0, y0 = (k % 2) * CW, (k // 2) * CH
        s.append(text(x0 + 6, y0 + CH / 2 + 6, "ABCD"[k], 18, anchor="start"))
        body, _, _ = pairs_body(x0 + LW, y0 + 8, n, kind)
        s.append(body)
    return svg_wrap(W, H, "".join(s), "four groups labelled A to D")


def sum_svg(a, b, kind):
    """Two groups drawn in pairs with a plus sign between them."""
    o, gap = 6, 34
    ba, wa, h = pairs_body(o, o, a, kind)
    bb, wb, _ = pairs_body(o + wa + gap, o, b, kind)
    plus = text(o + wa + gap / 2, o + h / 2 + 8, "+", 24)
    return svg_wrap(o + wa + gap + wb + o, h + 2 * o, ba + plus + bb,
                    "%d %s plus %d %s" % (a, KINDS[kind][1], b, KINDS[kind][1]))


def numline_svg(seq, k):
    """Number line counting by 2s: one tick per number in seq, the k-th label is a box with ?."""
    P, o, y = 62, 30, 58
    step = seq[1] - seq[0]
    W = o * 2 + P * (len(seq) - 1)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (o - 18, y, W - o + 18, y, INK)]
    for i, v in enumerate(seq):
        x = o + i * P
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 7, x, y + 7, INK))
        if i == k:
            s.append("<rect x='%d' y='%d' width='40' height='24' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x - 20, y + 11, FILL, GREEN))
            s.append(text(x, y + 29, "?", 17, col=GREEN))
        else:
            s.append(text(x, y + 29, str(v), 16))
        if i:
            x0 = o + (i - 1) * P
            s.append("<path d='M%d %d Q%d %d %d %d' fill='none' stroke='%s' stroke-width='1.8'/>"
                     % (x0 + 3, y - 9, (x0 + x) / 2, y - 44, x - 3, y - 9, GREEN))
            s.append(text((x0 + x) / 2, y - 30, ("+%d" % step) if step > 0 else ("−%d" % -step), 14, col=GREEN))
    return svg_wrap(W, y + 42, "".join(s), "number line counting by 2s")


def bar_svg(rows, total=None, label="bar model"):
    """Singapore bar model, drawn to scale.
    rows = [(name, [(value, dashed)], [(first seg, last seg, text)], right text (optional))];
    total = text for a brace on the right spanning all the rows."""
    LW, BW, BH = 84, 280, 30
    big = max(sum(v for v, _ in r[1]) for r in rows)
    sc = BW / float(big)
    W = LW + BW + (78 if total else 14) + (30 if any(len(r) > 3 for r in rows) else 0)
    y = 6
    s = []
    tops = []
    for row in rows:
        name, segs, over = row[:3]
        y += 24
        tops.append(y)
        s.append(text(LW - 10, y + BH / 2.0 + 5, name, 14, anchor="end"))
        xs = [LW]
        for v, dashed in segs:
            xs.append(xs[-1] + v * sc)
        for k, (v, dashed) in enumerate(segs):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.6'%s/>"
                     % (xs[k], y, xs[k + 1] - xs[k], BH, "#fff" if dashed else FILL, INK if not dashed else RED,
                        " stroke-dasharray='5 4'" if dashed else ""))
        for a, b, t in over:
            x1, x2 = xs[a] + 1, xs[b + 1] - 1
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='1.4'/>"
                     % (x1, y - 2, x1, y - 7, x2, y - 7, x2, y - 2, INK))
            s.append(text((x1 + x2) / 2.0, y - 11, t, 14, col=RED if "?" in t else INK))
        if len(row) > 3:
            s.append(text(xs[-1] + 10, y + BH / 2.0 + 6, row[3], 16, anchor="start", col=RED))
        y += BH + 12
    H = y
    if total:
        xb = LW + BW + 10
        y1, y2 = tops[0], tops[-1] + BH
        ym = (y1 + y2) / 2.0
        s.append("<path d='M%d %d q6 0 6 6 L%d %.1f q0 3 4 3 q-4 0 -4 3 L%d %d q0 6 -6 6' fill='none' "
                 "stroke='%s' stroke-width='1.6'/>" % (xb, y1, xb + 6, ym - 3, xb + 6, y2 - 6, INK))
        s.append(text(xb + 16, ym + 5, total, 14, anchor="start", col=RED if total == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


def lesson_odd_even_svg(a, b, kind="counters"):
    """Two groups with pair outlines and labels under them (lesson only)."""
    o, gap, lab = 10, 60, 26
    ba, wa, h = pairs_body(o, o, a, kind, outline=True, gx=10)
    bb, wb, _ = pairs_body(o + wa + gap, o, b, kind, outline=True, gx=10)
    W = wa + wb + gap + 2 * o
    t1 = text(o + wa / 2, o + h + 20, "%d: %s" % (a, par(a)), 16, col=GREEN if a % 2 == 0 else RED)
    t2 = text(o + wa + gap + wb / 2, o + h + 20, "%d: %s" % (b, par(b)), 16, col=GREEN if b % 2 == 0 else RED)
    return svg_wrap(W, h + 2 * o + lab - 6, ba + bb + t1 + t2,
                    "%d counters in pairs, none left over, and %d counters in pairs with 1 left over" % (a, b))


def lesson_sum_svg(a, b, kind="counters"):
    """a + b with the two left-over objects circled together (lesson only)."""
    assert a % 2 and b % 2
    o, gap = 10, 40
    ba, wa, h = pairs_body(o, o, a, kind, outline=True, gx=10)
    bb, wb, _ = pairs_body(o + wa + gap, o, b, kind, outline=True, gx=10)
    plus = text(o + wa + gap / 2, o + h / 2 + 8, "+", 24)
    # the two left-over objects sit in the top row of the last column of each group
    x1 = o + wa - (PITCH + 10) / 2.0
    x2 = o + wa + gap + wb - (PITCH + 10) / 2.0
    yl = o + PITCH / 2.0
    link = ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='2' "
            "stroke-dasharray='5 4'/>" % (x1, yl - 14, (x1 + x2) / 2, yl - 34 + 6, x2, yl - 14, RED))
    cap_t = text((o + wa + gap + wb + o) / 2.0, o + h + 22, "%d + %d = %d: even" % (a, b, a + b), 16, col=GREEN)
    top = 22
    body = "<g transform='translate(0 %d)'>%s</g>" % (top, ba + bb + plus + link + cap_t)
    return svg_wrap(o + wa + gap + wb + o, h + 2 * o + 28 + top, body,
                    "%d counters plus %d counters: the two left-over counters make a new pair" % (a, b))


def lesson_digits_svg(n):
    """A 3-digit number with the ones digit circled (lesson only)."""
    d = str(n)
    C, o = 78, 6
    s = []
    names = ["hundreds", "tens", "ones"][-len(d):]
    for i, ch in enumerate(d):
        x = o + i * C + C / 2
        last = i == len(d) - 1
        s.append(text(x, o + 36, ch, 34, col=GREEN if last else GREY))
        s.append(text(x, o + 66, names[i], 14, col=GREEN if last else GREY))
    xl = o + (len(d) - 1) * C + C / 2
    s.append("<circle cx='%.1f' cy='%d' r='22' fill='none' stroke='%s' stroke-width='2.5'/>" % (xl, o + 24, GREEN))
    W = o * 2 + C * len(d)
    return svg_wrap(W, o + 76, "".join(s), "the number %d with the ones digit circled" % n)


# ============================================================ set 1: pair up objects
def set_pairs(rnd):
    its = []
    for n, kind in [(7, "counters"), (10, "stars"), (13, "blocks"), (6, "counters"),
                    (15, "stars"), (12, "blocks"), (9, "counters"), (16, "stars")]:
        one, many, _ = KINDS[kind]
        h = n // 2
        q = fig(pairs_svg(n, kind)) + "How many %s are there? Is the number odd or even?" % many
        if n % 2:
            e = ("There are %d pairs and 1 %s left over. 1 left over means odd. "
                 "So %d is <b>odd</b>." % (h, one, n))
        else:
            e = ("There are %d pairs and none left over. Every %s has a partner, "
                 "so %d is <b>even</b>." % (h, one, n))
        alt = other(par(n))
        its.append(mcq(q, "%d: %s" % (n, par(n)),
                       ["%d: %s" % (n, alt), "%d: %s" % (n + 1, par(n + 1)), "%d: %s" % (n - 1, par(n - 1))], e))

    for n, kind in [(14, "counters"), (18, "blocks"), (11, "stars"), (20, "counters")]:
        one, many, _ = KINDS[kind]
        cols = (n + 1) // 2
        q = fig(pairs_svg(n, kind)) + "Count in twos. How many %s are there?" % many
        say = ", ".join(str(2 * k) for k in range(1, n // 2 + 1))
        if n % 2:
            e = "Count the pairs in twos: %s. Then add the 1 left over: %d + 1 = <b>%d</b>." % (say, n - 1, n)
        else:
            e = ("Count the pairs in twos: %s. There are <b>%d</b> %s. "
                 "Do not count the pairs only: %d pairs is %d %s." % (say, n, many, n // 2, n, many))
        its.append(mcq(q, n, [cols, n + 1, n - 1, n + 2], e))

    for n, kind in [(11, "stars"), (12, "counters"), (9, "blocks"), (14, "stars")]:
        one, many, _ = KINDS[kind]
        h = n // 2
        q = (fig(scattered_svg(n, kind, rnd))
             + "Pair up the %s. How many pairs? How many are left over?" % many)
        if n % 2:
            right = "%d pairs, 1 left" % h
            wrong = ["%d pairs, 0 left" % (h + 1), "%d pairs, 0 left" % h, "%d pairs, 3 left" % (h - 1)]
            e = ("There are %d %s. Put them 2 at a time. You get %d pairs, and 1 %s has no partner. "
                 "%d + %d + 1 = %d, so %d is odd." % (n, many, h, one, h, h, n, n))
        else:
            right = "%d pairs, 0 left" % h
            wrong = ["%d pairs, 1 left" % h, "%d pairs, 2 left" % (h - 1), "%d pairs, 0 left" % n]
            e = ("There are %d %s. Put them 2 at a time. You get %d pairs, and none is left over. "
                 "If 2 are left, they make 1 more pair. %d is even." % (n, many, h, n))
        its.append(mcq(q, right, wrong, e))

    abcd = [("even", [8, 7, 9, 5], "stars"), ("odd", [6, 9, 10, 4], "counters"),
            ("even", [11, 7, 12, 9], "blocks"), ("odd", [10, 8, 4, 11], "stars")]
    for pos, (want, counts, kind) in enumerate(abcd):
        one, many, _ = KINDS[kind]
        hits = [k for k, n in enumerate(counts) if par(n) == want]
        assert hits == [pos], (want, counts)
        q = fig(abcd_svg(counts, kind)) + "Which group has an <b>%s</b> number of %s?" % (want, many)
        n = counts[pos]
        ot = ["ABCD"[k] for k in range(4) if k != pos]
        others = "%s, %s and %s" % tuple(ot)
        if want == "even":
            e = ("Group <b>%s</b> has %d %s: %d pairs and none left over, so it is even. "
                 "In groups %s, 1 %s is left over." % ("ABCD"[pos], n, many, n // 2, others, one))
        else:
            e = ("Group <b>%s</b> has %d %s: %d pairs and 1 left over, so it is odd. "
                 "In groups %s, every %s has a partner." % ("ABCD"[pos], n, many, n // 2, others, one))
        its.append({"q": q, "c": ["A", "B", "C", "D"], "a": pos, "e": e, "fixed": True})
    assert len(its) == 20, len(its)
    return {"title": "Pair up objects: is one left over?", "items": its}


# ============================================================ set 2: the ones digit
def set_ones_digit():
    its = []
    labels = [(14, "Even: ends in 4", ["Odd: ends in 4", "Odd: 1 ten", "Odd: 7 pairs"]),
              (47, "Odd: ends in 7", ["Even: ends in 7", "Even: 4 tens", "Even: 23 pairs"]),
              (352, "Even: ends in 2", ["Odd: ends in 2", "Odd: 5 tens", "Odd: 3 hundreds"]),
              (530, "Even: ends in 0", ["Odd: ends in 0", "Odd: 3 tens", "Not odd or even"]),
              (861, "Odd: ends in 1", ["Even: ends in 1", "Even: 6 tens", "Even: 8 hundreds"]),
              (909, "Odd: ends in 9", ["Even: ends in 9", "Even: 0 tens", "Even: 454 pairs"]),
              (1000, "Even: ends in 0", ["Odd: ends in 0", "Odd: 1 thousand", "Not odd or even"]),
              (0, "Even", ["Odd", "Not odd or even", "Both odd and even"])]
    for n, r, w in labels:
        assert r.lower().startswith(par(n))
        assert all(not x.lower().startswith(par(n)) for x in w)
        for x in w:
            m = re.match(r"(\w+): (\d+) pairs", x)
            if m and n % 2:
                assert 2 * int(m.group(2)) + 1 == n          # forgot the 1 left over
            if m and n % 2 == 0:
                assert 2 * int(m.group(2)) == n              # thinks an odd number of pairs is odd
        if n == 0:
            e = ("0 is <b>even</b>. Count in twos from 0: 0, 2, 4, 6, 8. "
                 "That is why 10, 20 and 500 are even too.")
        else:
            e = "Look only at the ones digit. %d ends in %d, and %d is %s. So %d is <b>%s</b>." % (
                n, n % 10, n % 10, par(n % 10), n, par(n))
            if n % 10 == 0:
                e += " 0 is even."
            if n == 14:
                e += " 14 is 7 pairs with none left over. It does not matter that 7 is odd."
            elif n % 2:
                e += " %d is %d pairs and 1 left over. Do not forget the 1." % (n, n // 2)
            else:
                e += " The other digits do not matter."
        its.append(mcq("Is %d odd or even?" % n, r, w, e))

    pick = [("even", 254, [345, 167, 523]), ("odd", 381, [418, 836, 214]),
            ("even", 590, [905, 509, 595]), ("odd", 763, [376, 736, 670])]
    for i, (want, r, w) in enumerate(pick):
        assert par(r) == want and all(par(x) != want for x in w)
        stem = ["Which number is <b>%s</b>?", "Which number is <b>%s</b>?",
                "Look at the ones digit. Which number is <b>%s</b>?",
                "Look at the ones digit. Which number is <b>%s</b>?"][i]
        e = ("%d ends in %d, so it is <b>%s</b>. %s end in %s, so they are %s. "
             "The tens digit does not matter." % (r, r % 10, want, and_list(w), and_list([x % 10 for x in w]),
                                                   other(want)))
        its.append(mcq(stem % want, r, w, e))

    for shown, want, r, w in [("73", "even", 0, [3, 5, 7]), ("18", "odd", 5, [0, 4, 8])]:
        assert par(int(shown + str(r))) == want and all(par(int(shown + str(x))) != want for x in w)
        q = "%s□ is an <b>%s</b> number. Which digit can go in the box?" % (shown, want)
        e = ("Only the ones digit tells odd or even. %s%d ends in %d, so it is %s. "
             "%s would make %s numbers." % (shown, r, r, want, and_list(w), other(want)))
        if r == 0:
            e += " 0 is even, so 730 is even."
        its.append(mcq(q, r, w, e))

    lists = [("even", "412, 414, 416, 418", ["412, 414, 417, 418", "411, 413, 415, 417", "412, 415, 416, 418"],
              "412, 414, 416 and 418 end in 2, 4, 6 and 8. They are all <b>even</b>. "
              "Each other list has at least one odd number, like 417 or 415."),
             ("odd", "675, 677, 679, 681", ["675, 677, 678, 681", "674, 676, 678, 680", "675, 678, 679, 681"],
              "675, 677, 679 and 681 end in 5, 7, 9 and 1. They are all <b>odd</b>. "
              "Each other list has at least one even number, like 678.")]
    for want, r, w, e in lists:
        assert all(par(int(x)) == want for x in r.split(", "))
        assert all(any(par(int(x)) != want for x in l.split(", ")) for l in w)
        its.append(mcq("Which list has only <b>%s</b> numbers?" % want, r, w, e))

    its.append(mcq("What is the next <b>even</b> number after 157?", 158, [159, 156, 160],
                   "The number after 157 is 158. 158 ends in 8, so it is even. The answer is <b>158</b>. "
                   "159 is the next odd number."))
    its.append(mcq("What is the next <b>odd</b> number after 390?", 391, [392, 389, 393],
                   "The number after 390 is 391. 391 ends in 1, so it is odd. The answer is <b>391</b>. "
                   "392 is the next even number."))
    its.append(mcq("Mei Ling says 54 is odd because 5 is odd. Is she right?", "No, 54 is even",
                   ["Yes, 54 is odd", "Yes, 5 tens is odd", "No, 54 is neither"],
                   "Mei Ling looked at the tens digit. Look at the ones digit: 54 ends in 4, and 4 is even. "
                   "So <b>no</b>, 54 is even. It is 27 pairs with none left over."))
    its.append(mcq("Hafiz says every number that ends in 0 is even. Is he right?", "Yes, 0 is even",
                   ["No, 0 is not even", "No, only 10 is even", "No, they are odd"],
                   "<b>Yes</b>. 0 is even, so 10, 40, 200 and 1000 are all even. "
                   "Count in twos from 0: 0, 2, 4, 6, 8, 10."))
    assert len(its) == 20, len(its)
    return {"title": "Odd or even? Look at the ones digit", "items": its}


# ============================================================ set 3: number patterns
def set_patterns():
    its = []
    for seq, k in [([36, 38, 40, 42, 44], 2), ([127, 129, 131, 133, 135], 3), ([396, 398, 400, 402], 2),
                   ([705, 703, 701, 699], 2), ([998, 996, 994, 992], 1), ([489, 491, 493, 495], 3)]:
        d = seq[1] - seq[0]
        assert abs(d) == 2 and all(b - a == d for a, b in zip(seq, seq[1:])) and max(seq) <= 1000
        ans = seq[k]
        shown = ", ".join("<b>?</b>" if i == k else str(v) for i, v in enumerate(seq))
        if d > 0:
            q = "Count on in twos. What number is missing?<br>%s" % shown
            e = "Counting on in twos means adding 2 each time. %d + 2 = <b>%d</b>." % (seq[k - 1], ans)
            wrong = [ans - 1, ans + 1, ans + 10]
        else:
            q = "Count back in twos. What number is missing?<br>%s" % shown
            e = "Counting back in twos means taking away 2 each time. %d − 2 = <b>%d</b>." % (seq[k - 1], ans)
            wrong = [ans + 1, ans - 1, ans - 10]
        if ans == 400:
            wrong = [399, 401, 300, 410]
            e += " 398 + 2 crosses the hundred: 398, 399, 400."
        e += " All the numbers are %s." % par(ans)
        its.append(mcq(q, ans, wrong, e))

    for seq, k in [([214, 216, 218, 220, 222], 3), ([565, 567, 569, 571, 573], 2),
                   ([796, 798, 800, 802], 2), ([893, 895, 897, 899], 3)]:
        assert all(b - a == 2 for a, b in zip(seq, seq[1:])) and max(seq) <= 1000
        ans = seq[k]
        q = fig(numline_svg(seq, k)) + "What number goes in the box?"
        e = "Each jump adds 2. %d + 2 = <b>%d</b>. It ends in %d, so it is %s like the others." % (
            seq[k - 1], ans, ans % 10, par(ans))
        wrong = [ans - 1, ans + 1, ans + 10] if ans != 800 else [799, 801, 700]
        its.append(mcq(q, ans, wrong, e))

    its.append(mcq("What is the next <b>even</b> number after 499?", 500, [501, 498, 502],
                   "The number after 499 is 500. 500 ends in 0, and 0 is even. The answer is <b>500</b>. "
                   "501 is the next odd number."))
    its.append(mcq("What is the next <b>odd</b> number after 699?", 701, [700, 697, 703],
                   "The next number is 700, but it ends in 0, so it is even. The number after 700 is 701. "
                   "701 ends in 1, so it is odd. The answer is <b>701</b>."))

    for seq, r, w, e in [
        ([35, 45, 55, 65], "All odd", ["All even", "Odd, even, odd, even", "Even, odd, even, odd"],
         "Counting on in tens does not change the ones digit. Every number ends in 5, so they are "
         "<b>all odd</b>. The tens digits 3, 4, 5, 6 do not matter."),
        ([248, 348, 448, 548], "All even", ["All odd", "Even, odd, even, odd", "Odd, even, odd, even"],
         "Counting on in hundreds does not change the ones digit. Every number ends in 8, so they are "
         "<b>all even</b>. The hundreds digits 2, 3, 4, 5 do not matter.")]:
        d = seq[1] - seq[0]
        assert all(b - a == d for a, b in zip(seq, seq[1:]))
        assert r == "All " + par(seq[0]) and len(set(par(x) for x in seq)) == 1
        word = "tens" if d == 10 else "hundreds"
        q = "Count on in %s: %s. Are these numbers odd or even?" % (word, ", ".join(map(str, seq)))
        its.append(mcq(q, r, w, e))

    ev = [x for x in range(342, 351) if x % 2 == 0]
    od = [x for x in range(606, 615) if x % 2]
    its.append(mcq("How many <b>even</b> numbers are there between 341 and 351?", len(ev), [4, 6, 10],
                   "Count in twos: %s. That is <b>%d</b> even numbers. 341 and 351 are odd, "
                   "and “between” does not count them." % (and_list(ev), len(ev))))
    its.append(mcq("How many <b>odd</b> numbers are there between 605 and 615?", len(od), [5, 6, 10],
                   "Count in twos: %s. That is <b>%d</b> odd numbers. Do not count 605 and 615: "
                   "they are not between." % (and_list(od), len(od))))

    lists = [("Count on in twos. Which list has only <b>odd</b> numbers?", "451, 453, 455, 457",
              ["451, 453, 456, 457", "450, 452, 454, 456", "451, 454, 455, 457"],
              "451, 453, 455 and 457 end in 1, 3, 5 and 7. They are all <b>odd</b>. "
              "Each other list has an even number, like 456 or 454.", "odd", True),
             ("These patterns should count on in twos with even numbers. Which pattern has a mistake?",
              "610, 612, 615, 616", ["720, 722, 724, 726", "538, 540, 542, 544", "994, 996, 998, 1000"],
              "In <b>610, 612, 615, 616</b>, 615 ends in 5, so it is odd. It should be 614. "
              "The other patterns are all correct.", "even", False)]
    for q, r, w, e, want, good in lists:
        rn = [int(x) for x in r.split(", ")]
        assert all(par(x) == want for x in rn) == good
        for l in w:
            ln = [int(x) for x in l.split(", ")]
            assert all(par(x) == want for x in ln) != good
        its.append(mcq(q, r, w, e))

    its.append(mcq("A pattern counts on in twos: 81, 83, 85, 87, … Will 100 be in the pattern?",
                   "No: 100 is even", ["Yes: keep counting", "Yes: 100 is odd", "No: 100 is too big"],
                   "81, 83, 85 and 87 are odd. Adding 2 to an odd number gives the next odd number. "
                   "100 ends in 0, so it is even. <b>No</b>, it will be skipped: 97, 99, 101."))
    its.append(mcq("A pattern counts on in twos from 0: 0, 2, 4, 6, … Will 250 be in the pattern?",
                   "Yes: 250 is even", ["No: 250 is odd", "No: 5 tens is odd", "No: 0 is not even"],
                   "Counting in twos from 0 gives all the even numbers. 250 ends in 0, and 0 is even. "
                   "So <b>yes</b>. The 5 tens does not matter."))
    assert len(its) == 20, len(its)
    return {"title": "Odd and even numbers in patterns", "items": its}


# ============================================================ set 4: adding odd and even numbers
def set_sums():
    its = []
    for a, b, kind in [(5, 7, "counters"), (4, 3, "stars"), (6, 8, "blocks"), (9, 4, "counters")]:
        s = a + b
        q = fig(sum_svg(a, b, kind)) + "What is %d + %d? Is the answer odd or even?" % (a, b)
        if a % 2 and b % 2:
            e = ("%d is %d pairs and 1 left over. %d is %d pairs and 1 left over. The 2 left-over %s make "
                 "a new pair. %d + %d = %d, which is <b>even</b>." % (a, a // 2, b, b // 2, KINDS[kind][1], a, b, s))
        elif s % 2:
            o_ = a if a % 2 else b
            e = ("Only %d has 1 left over. Nothing can pair with it. %d + %d = %d, which is <b>odd</b>."
                 % (o_, a, b, s))
        else:
            e = "Both groups are pairs with none left over. %d + %d = %d, which is <b>even</b>." % (a, b, s)
        its.append(mcq(q, "%d: %s" % (s, par(s)),
                       ["%d: %s" % (s, other(par(s))), "%d: %s" % (s + 1, par(s + 1)),
                        "%d: %s" % (s - 1, par(s - 1))], e))

    CH = ["Always even", "Always odd", "Sometimes even", "Cannot tell"]
    for q, r, e in [("Odd + odd. Is the answer odd or even?", "Always even",
                     "The 2 left-over ones make a new pair, so odd + odd is <b>always even</b>. Example: 3 + 5 = 8."),
                    ("Even + even. Is the answer odd or even?", "Always even",
                     "Pairs + pairs are still pairs, so even + even is <b>always even</b>. Example: 4 + 6 = 10."),
                    ("Odd + even. Is the answer odd or even?", "Always odd",
                     "The 1 left over from the odd number has no partner, so odd + even is <b>always odd</b>. "
                     "Example: 7 + 2 = 9."),
                    ("Odd + odd + odd. Is the answer odd or even?", "Always odd",
                     "Odd + odd is even. Then even + odd is odd. So odd + odd + odd is <b>always odd</b>. "
                     "Example: 1 + 3 + 5 = 9.")]:
        its.append(mcq(q, r, [c for c in CH if c != r], e))
    # check the rules with numbers
    for x in range(1, 20):
        for y in range(1, 20):
            assert par(x + y) == ("even" if par(x) == par(y) else "odd")

    for a, b in [(23, 41), (135, 250), (346, 428), (417, 259), (508, 163), (642, 175)]:
        s = a + b
        assert s <= 1000
        ta, tb = (a // 10) % 10, (b // 10) % 10
        right = "%s: %s + %s" % (Par(s), par(a), par(b))
        cands = ["%s: %s + %s" % (other(Par(s)), par(a), par(b)),
                 "%s: %s + %s" % (Par(ta + tb), par(ta), par(tb))]
        for P_ in ("Even", "Odd"):
            for pa in ("odd", "even"):
                for pb in ("odd", "even"):
                    cands.append("%s: %s + %s" % (P_, pa, pb))
        q = "Without adding, is %d + %d odd or even?" % (a, b)
        e = ("Look at the ones digits: %d is %s and %d is %s. %s + %s = %s. So %d + %d is <b>%s</b>. "
             "Check: %d + %d = %d." % (a % 10, par(a), b % 10, par(b), cap(par(a)), par(b), par(s),
                                       a, b, par(s), a, b, s))
        it = mcq(q, right, cands, e)
        assert sum(1 for c in it["c"] if c.split(":")[0] == Par(s) and c.split(": ")[1] == "%s + %s" % (par(a), par(b))) == 1
        its.append(it)

    for want, r, w in [("odd", "16 + 23", ["15 + 27", "24 + 38", "31 + 19"]),
                       ("even", "45 + 37", ["45 + 36", "52 + 17", "60 + 29"]),
                       ("odd", "120 + 305", ["125 + 305", "240 + 316", "133 + 451"])]:
        val = lambda t: sum(int(x) for x in t.split(" + "))
        assert par(val(r)) == want and all(par(val(x)) != want for x in w)
        ra, rb = [int(x) for x in r.split(" + ")]
        e = ("%d is %s and %d is %s, so %s is <b>%s</b>: %s = %d. "
             "In the other sums both numbers are %s or both are %s, so the answers are %s."
             % (ra, par(ra), rb, par(rb), r, want, r, val(r), "odd", "even", "even")) if want == "odd" else (
            "%d and %d are both odd, so %s is <b>even</b>: %s = %d. "
            "Each other sum has one odd and one even number, so the answers are odd." % (ra, rb, r, r, val(r)))
        if want == "odd":
            for x in w:
                xa, xb = [int(t) for t in x.split(" + ")]
                assert par(xa) == par(xb)
        else:
            for x in w:
                xa, xb = [int(t) for t in x.split(" + ")]
                assert par(xa) != par(xb)
        stem = "Which sum is <b>%s</b>?" % want if r != "120 + 305" else "Look at the ones digits. Which sum is <b>odd</b>?"
        its.append(mcq(stem, r, w, e))

    for q, r, w, e, ok in [
        ("7 + □ is an even number. Which number can go in the box?", 5, [4, 6, 8],
         "7 is odd. Odd + odd = even, so the box needs an odd number. 7 + 5 = 12, which is even. "
         "4, 6 and 8 are even and give odd answers.", lambda x: (7 + x) % 2 == 0),
        ("12 + □ is an odd number. Which number can go in the box?", 9, [0, 2, 4],
         "12 is even. Even + odd = odd, so the box needs an odd number. 12 + 9 = 21, which is odd. "
         "0 is even too: 12 + 0 = 12 is even.", lambda x: (12 + x) % 2 == 1),
        ("□ + 35 is an even number. Which number can go in the box?", 15, [10, 20, 24],
         "35 is odd. Odd + odd = even, so the box needs an odd number. 15 + 35 = 50, which is even. "
         "10, 20 and 24 are even.", lambda x: (x + 35) % 2 == 0)]:
        assert ok(r) and not any(ok(x) for x in w)
        its.append(mcq(q, r, w, e))
    assert len(its) == 20, len(its)
    return {"title": "Adding odd and even numbers", "items": its}


# ============================================================ set 5: word problems
def set_stories():
    its = []

    def add(q, r, w, e, model=None):
        if model:
            q = fig(model) + q
        its.append(mcq(q, r, w, e))

    add("There are 13 pupils in a PE lesson. They make pairs. Can every pupil have a partner?",
        "No, 1 is left out", ["Yes, 6 pairs", "Yes, 7 pairs", "No, 2 are left out"],
        "6 pairs make 12 pupils. 1 pupil has no partner. 13 is <b>odd</b>.")
    add("A hawker stall puts 9 pairs of chopsticks on a tray. How many chopsticks are there?",
        "18 chopsticks", ["9 chopsticks", "11 chopsticks", "16 chopsticks"],
        "Each pair has 2 chopsticks. Count in twos: 2, 4, 6, 8, 10, 12, 14, 16, 18. 9 + 9 = <b>18</b>.")
    add("22 pupils go to the Singapore Zoo. Each pupil needs a buddy. Can every pupil have a buddy?",
        "Yes, 11 pairs", ["No, 11 is odd", "No, 1 is left out", "Yes, 12 pairs"],
        "11 + 11 = 22. That is 11 pairs, and nobody is left out. 22 is <b>even</b>. "
        "It does not matter that 11 is odd.")
    assert 18 + 18 == 36
    add("Wei Ming and Jun Jie share 36 stickers equally. How many stickers does each boy get?",
        "18 stickers", ["17 stickers", "36 stickers", "72 stickers"],
        "The model has 2 equal units. 2 units = 36. 18 + 18 = 36, so 1 unit = 18. "
        "Each boy gets <b>18 stickers</b>. 36 is even, so it can be shared equally between 2.",
        bar_svg([("Wei Ming", [(18, False)], [(0, 0, "?")]), ("Jun Jie", [(18, False)], [])], "36",
                "bar model: 2 equal units make 36"))
    add("Mrs Lim has 30 mandarin oranges for Chinese New Year. She gives them away in pairs. "
        "How many pairs can she give?", "15 pairs", ["14 pairs", "30 pairs", "60 pairs"],
        "15 + 15 = 30, so 30 oranges make <b>15 pairs</b>. None is left over, so 30 is even.")
    assert 15 + 8 == 23
    add("Ali has 15 marbles. Priya has 8 more marbles than Ali. How many marbles does Priya have? "
        "Is it odd or even?", "23: odd", ["23: even", "7: odd", "22: even"],
        "Priya has 8 more, so add: 15 + 8 = 23. 23 ends in 3, so it is <b>odd</b>. "
        "Odd + even = odd. Do not subtract: 15 − 8 = 7 is wrong.",
        bar_svg([("Ali", [(15, False)], [(0, 0, "15")]),
                 ("Priya", [(15, False), (8, False)], [(1, 1, "8")], "?")], None,
                "bar model: Priya has 8 more than Ali"))
    add("27 pupils get on a school bus. They sit 2 in a row. How many rows have 2 pupils?",
        "13 rows", ["14 rows", "12 rows", "27 rows"],
        "13 + 13 = 26, so 26 pupils fill <b>13 rows</b>. 1 pupil sits alone, so 27 is odd.")
    assert 26 - 14 == 12
    add("There are 26 pupils in Class 2A. 14 of them are girls. How many boys are there? Is it odd or even?",
        "12: even", ["12: odd", "40: even", "13: odd"],
        "Take away the girls: 26 − 14 = 12 boys. 12 ends in 2, so it is <b>even</b>. "
        "Do not add: 26 + 14 = 40 is wrong.",
        bar_svg([("Class 2A", [(14, False), (12, True)], [(0, 0, "14 girls"), (1, 1, "? boys")])], "26",
                "bar model: 26 pupils, 14 girls and some boys"))
    add("Hui Min has an even number of red packets. It is more than 40 and less than 44. "
        "How many red packets does she have?", "42", ["41", "43", "40"],
        "The numbers more than 40 and less than 44 are 41, 42 and 43. Only <b>42</b> is even. "
        "40 is even, but it is not more than 40.")
    add("A box has an odd number of rambutans. It is more than 65 and less than 68. "
        "How many rambutans are in the box?", "67", ["66", "65", "68"],
        "The numbers more than 65 and less than 68 are 66 and 67. Only <b>67</b> is odd. "
        "65 is odd, but it is not more than 65.")
    add("Kumar has 9 beads. He wants to put all of them in pairs, with none left over. "
        "What is the smallest number of beads he must add?", "1 bead", ["2 beads", "0 beads", "9 beads"],
        "9 is 4 pairs and 1 left over. Add <b>1 bead</b> to give it a partner. 9 + 1 = 10, and 10 is even.")
    add("Farah makes 15 red paper flowers and 15 yellow paper flowers for Teachers’ Day. "
        "Is the number of flowers odd or even?", "Even: 30", ["Odd: 30", "Odd: 15", "Odd: 31"],
        "The model shows 15 + 15 = 30. Odd + odd = even, so the answer is <b>even</b>. "
        "30 ends in 0, and 0 is even.",
        bar_svg([("Red", [(15, False)], [(0, 0, "15")]), ("Yellow", [(15, False)], [(0, 0, "15")])], "?",
                "bar model: 15 red and 15 yellow flowers"))
    add("8 girls and 5 boys go to the badminton CCA. They play in pairs. Will everyone have a partner?",
        "No, 1 is left out", ["Yes, 8 is even", "Yes, 7 pairs", "Yes, 6 pairs"],
        "8 + 5 = 13. Even + odd = odd. 6 pairs make 12, so 1 child is left out. 13 is <b>odd</b>.")
    assert 20 + 20 == 40
    add("Mr Tan puts 40 chairs in 2 equal rows at the void deck for a party. How many chairs are in each row?",
        "20 chairs", ["40 chairs", "10 chairs", "80 chairs"],
        "2 equal rows means 2 equal units. 2 units = 40. 20 + 20 = 40, so 1 unit = 20. "
        "Each row has <b>20 chairs</b>.",
        bar_svg([("Row 1", [(20, False)], [(0, 0, "?")]), ("Row 2", [(20, False)], [])], "40",
                "bar model: 2 equal rows make 40"))
    add("There are 21 pigeons at the void deck. Then 1 more pigeon lands. Is the number of pigeons odd or even now?",
        "Even: 22 pigeons", ["Odd: 22 pigeons", "Odd: 21 pigeons", "Even: 23 pigeons"],
        "21 is 10 pairs and 1 left over. The new pigeon is a partner for it. 21 + 1 = 22, and 22 is <b>even</b>.")
    assert 347 + 215 == 562
    add("A library has 347 storybooks and 215 comics. Is the total number of books odd or even?",
        "Even: 562", ["Odd: 562", "Odd: 563", "Even: 132"],
        "347 is odd and 215 is odd. Odd + odd = even. Check: 347 + 215 = 562, which ends in 2. "
        "The answer is <b>even</b>.",
        bar_svg([("Books", [(347, False), (215, False)], [(0, 0, "347"), (1, 1, "215")])], "?",
                "bar model: 347 storybooks and 215 comics"))
    for x in [245, 427, 163]:
        assert x % 2 and ((x // 10) % 10) % 2 == 0
    add("The lockers in a school are numbered. The lockers with even numbers are on the left. "
        "Which locker is on the left?", "254", ["245", "427", "163"],
        "254 ends in 4, so it is <b>even</b>. 245, 427 and 163 end in 5, 7 and 3, so they are odd. "
        "Do not look at the tens digit.")
    add("Arjun counts the shoes outside his flat in twos: 2, 4, 6, 8, 10, 12, 14, 16. "
        "How many shoes are there? Is it odd or even?",
        "16: even", ["8: even", "16: odd", "17: odd"],
        "The last number Arjun says is 16, so there are 16 shoes. He said 8 numbers, but each one counts 2 shoes. "
        "16 ends in 6, so it is <b>even</b>.")
    add("Xin Yi has 15 stickers. She wants to share them equally with her sister. "
        "Can they each get the same number?", "No, 1 is left over", ["Yes, 7 each", "Yes, 8 each", "Yes, 7 and 8"],
        "7 + 7 = 14 and 8 + 8 = 16. No 2 equal numbers make 15, so 1 sticker is left over. "
        "15 is <b>odd</b>. 7 and 8 are not the same number.")
    assert 120 - 35 == 85
    add("Chloe has 120 beads. Sarah has 35 fewer beads than Chloe. How many beads does Sarah have? "
        "Is it odd or even?", "85: odd", ["85: even", "155: odd", "95: odd"],
        "Sarah has fewer, so subtract: 120 − 35 = 85. 85 ends in 5, so it is <b>odd</b>. "
        "Do not add: 120 + 35 = 155 is wrong.",
        bar_svg([("Chloe", [(120, False)], [(0, 0, "120")]),
                 ("Sarah", [(85, False), (35, True)], [(0, 0, "?"), (1, 1, "35")])], None,
                "bar model: Sarah has 35 fewer than Chloe"))
    assert len(its) == 20, len(its)
    return {"title": "Odd and even word problems", "items": its}


# ============================================================ lesson
def body_html():
    model = bar_svg([("Siti", [(12, False)], [(0, 0, "?")]), ("Ahmad", [(12, False)], [])], "24",
                    "bar model: 2 equal units make 24")
    return (
        "<h2>Odd or even? Pair them up</h2>"
        "<p>Put the things in pairs (groups of 2). If every one has a partner, the number is <b>even</b>. "
        "If 1 is left over, the number is <b>odd</b>.</p>"
        "<figure class='sn-fig'>" + lesson_odd_even_svg(8, 7) +
        "<figcaption>8 counters make 4 pairs with none left over, so 8 is even. "
        "7 counters make 3 pairs and 1 left over, so 7 is odd.</figcaption></figure>"
        "<h2>Look at the ones digit</h2>"
        "<p>Count in twos from 0: 0, 2, 4, 6, 8, 10, 12. These are the even numbers. "
        "Count in twos from 1: 1, 3, 5, 7, 9, 11. These are the odd numbers. "
        "For any number up to 1000, look only at the <b>ones digit</b> (the last digit).</p>"
        + table(["Ones digit", "The number is", "Examples"], [
            ["0, 2, 4, 6, 8", "even", "10, 36, 254, 1000"],
            ["1, 3, 5, 7, 9", "odd", "7, 23, 381, 909"],
        ])
        + "<figure class='sn-fig'>" + lesson_digits_svg(352) +
        "<figcaption>352 ends in 2, so 352 is even. The 3 hundreds and the 5 tens do not matter.</figcaption></figure>"
        + ex("Odd or even?", "Is 761 odd or even?",
             "Look only at the ones digit. 761 ends in 1, and 1 is odd. The 6 tens does not matter.", "odd")
        + "<h2>Adding odd and even numbers</h2>"
        "<p>When you add two odd numbers, the two left-over ones make a new pair.</p>"
        "<figure class='sn-fig'>" + lesson_sum_svg(5, 3) +
        "<figcaption>5 + 3: each group has 1 left over. Together they make a pair, so 8 is even.</figcaption></figure>"
        + table(["Add", "Answer", "Example"], [
            ["even + even", "even", "4 + 6 = 10"],
            ["odd + odd", "even", "5 + 3 = 8"],
            ["odd + even", "odd", "7 + 2 = 9"],
        ])
        + ex("Without adding", "Is 135 + 250 odd or even?",
             "Look at the ones digits: 5 is odd and 0 is even. Odd + even = odd. Check: 135 + 250 = 385.", "odd")
        + "<h2>Sharing equally between 2</h2>"
        "<p>An even number can be shared equally between 2 people. An odd number always has 1 left over.</p>"
        "<figure class='sn-fig'>" + model +
        "<figcaption>Siti and Ahmad share 24 sweets equally. 2 units = 24. 12 + 12 = 24, "
        "so 1 unit = 12.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Looking at the tens digit: 352 has 5 tens, so it is odd",
             "Look at the ones digit: 2 is even, so 352 is even"],
            ["Thinking 0 is not odd or even", "0 is even, so 10, 200 and 1000 are even too"],
            ["Forgetting the one left over: 47 is 23 pairs, so it is even", "23 pairs and 1 left over: 47 is odd"],
            ["Thinking odd + odd is odd: 5 + 3 is odd", "The 2 left-over ones make a pair: 5 + 3 = 8 is even"],
            ["Counting the pairs, not the things: 7 pairs of shoes is 7 shoes", "Count in twos: 7 pairs is 14 shoes"],
        ])
    )


FAQ = [
    {"q": "What is taught in P2 odd and even numbers?",
     "a": "Primary 2 students tell whether a number up to 1000 is odd or even. They pair up objects, "
          "count in twos, look at the ones digit and spot odd and even numbers in number patterns."},
    {"q": "How do I explain odd and even numbers to my child?",
     "a": "Pair up socks, shoes or sweets: if every one has a partner the number is even, and if 1 is left over "
          "it is odd. Then show that only the ones digit matters, so 352 is even because it ends in 2."},
    {"q": "Is 0 an even number?",
     "a": "Yes, 0 is even. Counting in twos starts at 0, and numbers that end in 0, like 10, 200 and 1000, "
          "are even too."},
    {"q": "Is odd and even numbers in the MOE syllabus?",
     "a": "Yes. Odd and even numbers are part of Whole Numbers in the MOE 2021 Primary 2 Mathematics syllabus, "
          "together with numbers up to 1000."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and the objects stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_figures(sets):
    """Objects drawn must match the numbers in the aria-label."""
    for s in sets:
        for it in s["items"]:
            svgs = re.findall(r"<svg.*?</svg>", it["q"])
            assert len(svgs) <= 1
            for svg in svgs:
                n_obj = len(re.findall(r"<(circle|rect x='[\d.]+' y='[\d.]+' width='19'|polygon)", svg))
                m = re.search(r"aria-label='(\d+) \w+ (in pairs|mixed up)'", svg)
                if m:
                    assert n_obj == int(m.group(1)), (m.group(0), n_obj)
                m = re.search(r"aria-label='(\d+) \w+ plus (\d+) \w+'", svg)
                if m:
                    assert n_obj == int(m.group(1)) + int(m.group(2)), (m.group(0), n_obj)


def gen():
    rnd = random.Random(62802)
    sets = [set_pairs(rnd), set_ones_digit(), set_patterns(), set_sums(), set_stories()]
    check_figures(sets)
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert "\\" not in it["q"] + it["e"] + "".join(it["c"])
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "odd-and-even-numbers", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Odd and Even Numbers",
        "seo_title": "P2 Odd and Even Numbers Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Odd and even numbers",
        "domain": "Number and Algebra",
        "standard_code": "Primary 2: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Odd and even numbers",
        "meta_desc": "Free P2 maths practice on odd and even numbers to 1000: pairing objects, the ones digit, "
                     "number patterns and adding. 100 questions with answers.",
        "key_big": "Look only at the ones digit: 0, 2, 4, 6 and 8 mean the number is even.",
        "key_sub": "352 is even because it ends in 2, not odd because of the 5 tens.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(four groups labelled A to D|number line counting by 2s|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
