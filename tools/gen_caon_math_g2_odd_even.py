# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 2 Math: Odd and Even Numbers (Ontario Mathematics Curriculum 2020, B1.5)
  python3 tools/gen_caon_math_g2_odd_even.py
Make pairs and look for one left over, even numbers end in 0, 2, 4, 6 or 8, odd or even for
numbers to 200, doubles are always even, and word problems in Canadian settings.
Wrong answers come from real mistakes: looking at the first digit (or the tens digit) instead of
the ones digit, thinking 0 is not even, forgetting the one left over, thinking 18 is odd because
9 + 9 uses an odd number, and using two different addends instead of a double.
Every count, sum and odd/even label is checked in code. HTML attributes use single quotes.
Grade 2: short sentences for 7-8 year olds.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
GOLD = "#e3a81b"
INK = "#2b2b2b"
GRAY = "#9a948c"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


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


def par(n):
    return "even" if n % 2 == 0 else "odd"


def Par(n):
    return cap(par(n))


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
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CW, CW, H - 4, GRAY),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CH, W - 4, CH, GRAY)]
    for k, n in enumerate(counts):
        x0, y0 = (k % 2) * CW, (k // 2) * CH
        s.append(text(x0 + 6, y0 + CH / 2 + 6, "ABCD"[k], 18, anchor="start"))
        body, _, _ = pairs_body(x0 + LW, y0 + 8, n, kind)
        s.append(body)
    return svg_wrap(W, H, "".join(s), "four groups labelled A to D")


def numline_svg(seq, k):
    """Number line counting by 2s: one tick per number in seq, the k-th label is a box with ?.
    Jump arcs of +2 between the ticks."""
    P, o, y = 62, 30, 58
    W = o * 2 + P * (len(seq) - 1)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (o - 18, y, W - o + 18, y, INK)]
    for i, v in enumerate(seq):
        x = o + i * P
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 7, x, y + 7, INK))
        if i == k:
            s.append("<rect x='%d' y='%d' width='34' height='24' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x - 17, y + 11, FILL, GREEN))
            s.append(text(x, y + 29, "?", 17, col=GREEN))
        else:
            s.append(text(x, y + 29, str(v), 16))
        if i:
            x0 = o + (i - 1) * P
            s.append("<path d='M%d %d Q%d %d %d %d' fill='none' stroke='%s' stroke-width='1.8'/>"
                     % (x0 + 3, y - 9, (x0 + x) / 2, y - 44, x - 3, y - 9, GREEN))
            s.append(text((x0 + x) / 2, y - 30, "+2", 14, col=GREEN))
    return svg_wrap(W, y + 42, "".join(s), "number line counting by 2s")


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


def lesson_double_svg(h, kind="stars"):
    """Two equal rows of h with the row totals written at the right."""
    o = 8
    body, w, ht = pairs_body(o, o, 2 * h, kind)
    tx = o + w + 14
    t = (text(tx, o + PITCH / 2 + 6, str(h), 18, anchor="start", col=GREEN)
         + text(tx, o + PITCH * 1.5 + 6, "+ " + str(h), 18, anchor="start", col=GREEN))
    return svg_wrap(tx + 40, ht + 2 * o, body + t, "two equal rows of %d stars" % h)


def lesson_digits_svg(n):
    """A 3-digit number with the ones digit circled (lesson only)."""
    d = str(n)
    C, o = 78, 6
    s = []
    names = ["hundreds", "tens", "ones"][-len(d):]
    for i, ch in enumerate(d):
        x = o + i * C + C / 2
        last = i == len(d) - 1
        s.append(text(x, o + 36, ch, 34, col=GREEN if last else GRAY))
        s.append(text(x, o + 66, names[i], 14, col=GREEN if last else GRAY))
    xl = o + (len(d) - 1) * C + C / 2
    s.append("<circle cx='%.1f' cy='%d' r='22' fill='none' stroke='%s' stroke-width='2.5'/>" % (xl, o + 24, GREEN))
    W = o * 2 + C * len(d)
    return svg_wrap(W, o + 76, "".join(s), "the number %d with the ones digit circled" % n)


# ============================================================ set 1: make pairs
def set_pairs(P, rnd):
    its = []
    for n, kind in [(7, "counters"), (10, "stars"), (13, "blocks"), (6, "counters"),
                    (15, "stars"), (12, "blocks"), (9, "counters"), (16, "stars")]:
        one, many, _ = KINDS[kind]
        h = n // 2
        q = fig(pairs_svg(n, kind)) + "How many %s? Is the number odd or even?" % many
        if n % 2:
            e = ("There are %d pairs and 1 %s left over. One left over means odd. "
                 "So %d is <b>odd</b>." % (h, one, n))
        else:
            e = ("There are %d pairs and none left over. Every %s has a partner, "
                 "so %d is <b>even</b>." % (h, one, n))
        alt = "even" if n % 2 else "odd"
        its.append(mcq(q, "%d: %s" % (n, par(n)),
                       ["%d: %s" % (n, alt), "%d: %s" % (n + 1, par(n + 1)), "%d: %s" % (n - 1, par(n - 1))], e))

    for n, kind in [(14, "counters"), (18, "blocks"), (11, "stars"), (20, "counters")]:
        one, many, _ = KINDS[kind]
        cols = (n + 1) // 2
        q = fig(pairs_svg(n, kind)) + "Count by 2s. How many %s are there?" % many
        say = ", ".join(str(2 * k) for k in range(1, n // 2 + 1))
        if n % 2:
            e = "Count the pairs by 2s: %s. Then add the 1 left over: %d + 1 = <b>%d</b>." % (say, n - 1, n)
        else:
            e = "Count the pairs by 2s: %s. There are <b>%d</b> %s." % (say, n, many)
        its.append(mcq(q, n, [cols, n + 1, n - 1, n + 2], e))

    for n, kind in [(11, "stars"), (12, "counters"), (9, "blocks"), (14, "stars")]:
        one, many, _ = KINDS[kind]
        h = n // 2
        q = (fig(scattered_svg(n, kind, rnd))
             + "Make pairs. How many pairs? How many %s are left over?" % many)
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
    return {"title": "Make pairs: is one left over?", "items": its}


# ============================================================ set 2: ones digit 0, 2, 4, 6, 8
def which_e(want, r, w):
    return ("Look at the ones digit. %d ends in %d, so it is <b>%s</b>. %s end in %s, so they are %s. "
            "The tens digit does not matter." % (r, r % 10, want, and_list(w), and_list([x % 10 for x in w]),
                                                  "odd" if want == "even" else "even"))


def set_ones_digit(P):
    its = []
    for seq, k in [([4, 6, 8, 10, 12], 3), ([12, 14, 16, 18], 2), ([3, 5, 7, 9], 3), ([21, 23, 25, 27, 29], 2)]:
        assert all(b - a == 2 for a, b in zip(seq, seq[1:]))
        ans = seq[k]
        shown = ", ".join("<b>?</b>" if i == k else str(v) for i, v in enumerate(seq))
        q = "Count by 2s. What number is missing?<br>%s" % shown
        e = "Counting by 2s means adding 2 each time. %d + 2 = <b>%d</b>." % (seq[k - 1], ans)
        if k + 1 < len(seq):
            e += " Then %d + 2 = %d." % (ans, seq[k + 1])
        its.append(mcq(q, ans, [ans - 1, ans + 1, ans + 4], e))

    one_digit = [
        ("Is 14 odd or even?", "Even: ends in 4", ["Odd: ends in 4", "Odd: 1 ten", "Odd: 7 pairs"],
         "Look at the ones digit. 14 ends in 4, and 4 is even. So 14 is <b>even</b>. "
         "The 1 ten does not matter. 14 is 7 pairs with none left over."),
        ("Is 30 odd or even?", "Even: ends in 0", ["Odd: ends in 0", "Odd: 3 tens", "Not odd or even"],
         "30 ends in 0, and 0 is even. So 30 is <b>even</b>. It makes 15 pairs with none left over."),
        ("Is 23 odd or even?", "Odd: ends in 3", ["Even: ends in 3", "Even: 2 tens", "Even: 11 pairs"],
         "Look at the ones digit. 23 ends in 3, and 3 is odd. So 23 is <b>odd</b>. "
         "23 is 11 pairs and 1 left over. Do not forget the 1."),
        ("Is 0 odd or even?", "Even", ["Odd", "Not odd or even", "Both odd and even"],
         "0 is <b>even</b>. Counting by 2s starts at 0: 0, 2, 4, 6. That is why 10, 20 and 30 are even too."),
    ]
    for q, r, w, e in one_digit:
        n = int(re.search(r"\d+", q).group())
        assert r.lower().startswith(par(n)), q
        its.append(mcq(q, r, w, e))

    pick = [("even", 20, [21, 23, 25]), ("odd", 41, [14, 40, 22]),
            ("even", 36, [63, 45, 87]), ("odd", 57, [52, 74, 38])]
    stems = ["Which number is <b>%s</b>?", "Which number is <b>%s</b>?",
             "Which of these numbers is <b>%s</b>?", "Which of these numbers is <b>%s</b>?"]
    for stem, (want, r, w) in zip(stems, pick):
        assert par(r) == want and all(par(x) != want for x in w)
        e = which_e(want, r, w)
        if r == 20:
            e = "20 ends in 0, and 0 is even. So 20 is <b>even</b>. 21, 23 and 25 end in 1, 3 and 5, so they are odd."
        its.append(mcq(stem % want, r, w, e))

    for n_shown, want, r, w in [("4", "even", 6, [3, 5, 7]), ("7", "odd", 1, [0, 4, 8])]:
        assert par(int(n_shown + str(r))) == want and all(par(int(n_shown + str(x))) != want for x in w)
        q = "%s□ is an <b>%s</b> number. Which digit can go in the box?" % (n_shown, want)
        e = ("Only the ones digit tells odd or even. %s%d ends in %d, so it is %s. "
             "%s would make %s numbers." % (n_shown, r, r, want, and_list(w), "odd" if want == "even" else "even"))
        if r == 1:
            e += " 0 is even, so 70 is even."
        its.append(mcq(q, r, w, e))

    lists = [("even", "10, 12, 14, 16", ["10, 12, 15, 16", "11, 13, 15, 17", "12, 14, 17, 18"],
              "10, 12, 14 and 16 end in 0, 2, 4 and 6. They are all <b>even</b>. "
              "Each other list has at least one odd number, like 15 or 17."),
             ("odd", "13, 15, 17, 19", ["13, 15, 18, 19", "12, 14, 16, 18", "11, 14, 17, 19"],
              "13, 15, 17 and 19 end in 3, 5, 7 and 9. They are all <b>odd</b>. "
              "Each other list has at least one even number, like 18 or 14.")]
    for want, r, w, e in lists:
        assert all(par(int(x)) == want for x in r.split(", "))
        assert all(any(par(int(x)) != want for x in l.split(", ")) for l in w)
        its.append(mcq("Which list has only <b>%s</b> numbers?" % want, r, w, e))

    its.append(mcq("What is the next <b>even</b> number after 17?", 18, [19, 16, 20],
                   "The number after 17 is 18. 18 ends in 8, so it is even. The answer is <b>18</b>. "
                   "19 is the next odd number."))
    its.append(mcq("What is the next <b>odd</b> number after 24?", 25, [26, 23, 27],
                   "The number after 24 is 25. 25 ends in 5, so it is odd. The answer is <b>25</b>. "
                   "26 is the next even number."))

    nm, he, his = P.next()
    its.append(mcq("%s counts by 2s. %s starts at 0. Which number will %s <b>not</b> say?" % (nm, cap(he), he),
                   15, [12, 16, 20],
                   "0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20. Counting by 2s from 0 gives the even numbers. "
                   "15 is odd, so %s skips it. The answer is <b>15</b>." % nm))
    nm, he, his = P.next()
    its.append(mcq("%s counts by 2s. %s starts at 1. Which number will %s <b>not</b> say?" % (nm, cap(he), he),
                   14, [13, 17, 19],
                   "1, 3, 5, 7, 9, 11, 13, 15, 17, 19. Counting by 2s from 1 gives the odd numbers. "
                   "14 is even, so %s skips it. The answer is <b>14</b>." % nm))
    assert len(its) == 20, len(its)
    return {"title": "Even numbers end in 0, 2, 4, 6 or 8", "items": its}


# ============================================================ set 3: numbers to 200
def set_to_200(P):
    its = []
    labels = [(136, "Even: ends in 6", ["Odd: ends in 6", "Odd: starts with 1", "Odd: 3 tens"]),
              (147, "Odd: ends in 7", ["Even: ends in 7", "Even: 4 tens", "Even: 73 pairs"]),
              (120, "Even: ends in 0", ["Odd: ends in 0", "Odd: starts with 1", "Not odd or even"]),
              (165, "Odd: ends in 5", ["Even: ends in 5", "Even: 6 tens", "Even: 82 pairs"]),
              (172, "Even: ends in 2", ["Odd: ends in 2", "Odd: 7 tens", "Odd: starts with 1"]),
              (189, "Odd: ends in 9", ["Even: ends in 9", "Even: 8 tens", "Even: 94 pairs"])]
    for n, r, w in labels:
        assert r.lower().startswith(par(n)) and r.endswith(str(n % 10))
        assert all(not x.lower().startswith(par(n)) for x in w)
        for x in w:
            m = re.match(r"(\w+): (\d+) pairs", x)
            if m:
                assert 2 * int(m.group(2)) + 1 == n          # forgot the 1 left over
        e = "Look only at the ones digit. %d ends in %d, and %d is %s. So %d is <b>%s</b>." % (
            n, n % 10, n % 10, par(n % 10), n, par(n))
        if "starts with 1" in "".join(w):
            e += " The 1 at the start does not matter."
        elif n % 2:
            e += " %d is %d pairs and 1 left over. Do not forget the 1." % (n, n // 2)
        else:
            e += " The tens digit does not matter."
        if n % 10 == 0:
            e += " 0 is even."
        its.append(mcq("Is %d odd or even?" % n, r, w, e))

    pick = [("even", 114, [141, 123, 165]), ("odd", 183, [138, 146, 160]),
            ("even", 150, [105, 151, 115]), ("odd", 127, [172, 154, 190]),
            ("even", 196, [169, 175, 163]), ("odd", 101, [110, 152, 174])]
    for i, (want, r, w) in enumerate(pick):
        assert par(r) == want and all(par(x) != want for x in w) and max([r] + w) <= 200
        stem = ["Which big number is <b>%s</b>?", "Which big number is <b>%s</b>?",
                "Look at the ones digit. Which number is <b>%s</b>?", "Look at the ones digit. Which number is <b>%s</b>?",
                "Which of these 3-digit numbers is <b>%s</b>?", "Which of these 3-digit numbers is <b>%s</b>?"][i]
        e = ("Look at the ones digit. %d ends in %d, so it is <b>%s</b>. %s end in %s, so they are %s. "
             "The first digit does not matter." % (r, r % 10, want, and_list(w), and_list([x % 10 for x in w]),
                                                    "odd" if want == "even" else "even"))
        its.append(mcq(stem % want, r, w, e))

    for seq, k in [([94, 96, 98, 100, 102], 3), ([145, 147, 149, 151, 153], 3),
                   ([186, 188, 190, 192], 2), ([171, 173, 175, 177], 3)]:
        assert all(b - a == 2 for a, b in zip(seq, seq[1:])) and max(seq) <= 200
        ans = seq[k]
        q = fig(numline_svg(seq, k)) + "Count by 2s. What number goes in the box?"
        e = "Each jump adds 2. %d + 2 = <b>%d</b>. %s" % (
            seq[k - 1], ans, "It ends in %d, so it is %s like the others." % (ans % 10, par(ans)))
        its.append(mcq(q, ans, [ans - 1, ans + 1, ans + 10], e))

    its.append(mcq("What is the next <b>even</b> number after 149?", 150, [151, 148, 152],
                   "The number after 149 is 150. 150 ends in 0, and 0 is even. The answer is <b>150</b>. "
                   "151 is the next odd number."))
    its.append(mcq("What is the next <b>odd</b> number after 178?", 179, [180, 177, 181],
                   "The number after 178 is 179. 179 ends in 9, so it is odd. The answer is <b>179</b>. "
                   "180 is the next even number."))
    lists = [("even", "130, 132, 134, 136", ["130, 132, 135, 136", "131, 133, 135, 137", "132, 134, 137, 138"],
              "130, 132, 134 and 136 end in 0, 2, 4 and 6. They are all <b>even</b>. "
              "Each other list has at least one odd number, like 135 or 137."),
             ("odd", "181, 183, 185, 187", ["181, 183, 186, 187", "180, 182, 184, 186", "181, 184, 185, 187"],
              "181, 183, 185 and 187 end in 1, 3, 5 and 7. They are all <b>odd</b>. "
              "Each other list has at least one even number, like 186 or 184.")]
    for want, r, w, e in lists:
        assert all(par(int(x)) == want for x in r.split(", "))
        assert all(any(par(int(x)) != want for x in l.split(", ")) for l in w)
        its.append(mcq("Count on by 2s. Which list has only <b>%s</b> numbers?" % want, r, w, e))
    assert len(its) == 20, len(its)
    return {"title": "Odd or even? Numbers to 200", "items": its}


# ============================================================ set 4: doubles are even
def set_doubles(P):
    its = []
    for h, kind in [(4, "counters"), (7, "stars"), (5, "blocks"), (9, "counters"), (6, "stars"), (8, "blocks")]:
        one, many, _ = KINDS[kind]
        n = 2 * h
        q = fig(pairs_svg(n, kind)) + "The %s are in 2 equal rows. Which equation matches?" % many
        e = ("Each row has %d %s. Two equal rows make a double: %d + %d = <b>%d</b>. "
             "%d is even." % (h, many, h, h, n, n))
        its.append(mcq(q, "%d + %d = %d" % (h, h, n),
                       ["%d + %d = %d" % (h - 1, h + 1, n), "%d + 2 = %d" % (h, h + 2), "%d + %d = %d" % (h, h, n - 2)], e))

    for n in [12, 18, 30, 40]:
        h = n // 2
        q = "Which shows %d as a double (two equal addends)?" % n
        w = ["%d + %d" % (h - 1, h + 1), "%d + %d" % (n, n)]
        w.append("%d + %d" % (n // 10, n % 10) if n % 10 else "10 + %d" % (n - 10))
        e = ("Equal addends are the same number. %d + %d = %d, so %d = <b>%d + %d</b>. "
             "%d + %d also makes %d, but %d and %d are not equal." % (h, h, n, n, h, h, h - 1, h + 1, n, h - 1, h + 1))
        its.append(mcq(q, "%d + %d" % (h, h), w, e))

    for n, q in [(16, "Which equation is a true double?"),
                 (24, "Which equation is true <b>and</b> has two equal addends?"),
                 (20, "Which one shows an even number as a double?"),
                 (50, "Which double is correct?")]:
        h = n // 2
        right = "%d = %d + %d" % (n, h, h)
        w = ["%d = %d + %d" % (n + 1, h, h), "%d = %d + %d" % (n, h - 1, h + 1), "%d = %d + %d" % (n + 1, h, h + 1)]
        e = ("%d + %d = %d, so <b>%s</b> is true and the addends are equal. %s is not true. "
             "%s is true, but %d and %d are not equal." % (h, h, n, right, w[0], w[1], h - 1, h + 1))
        its.append(mcq(q, right, w, e))

    can = [(15, "No: 15 is odd", ["Yes: 7 + 7", "Yes: 7 + 8", "Yes: 5 + 5 + 5"],
            "7 + 7 = 14 and 8 + 8 = 16. No double makes 15. 15 is odd, so it <b>cannot</b> be a double."),
           (18, "Yes: 9 + 9", ["No: 9 is odd", "Yes: 8 + 10", "No: 1 is odd"],
            "9 + 9 = 18, so <b>yes</b>. It does not matter that 9 is odd. 18 ends in 8, so it is even."),
           (21, "No: 21 is odd", ["Yes: 10 + 11", "Yes: 10 + 10", "Yes: 11 + 11"],
            "10 + 10 = 20 and 11 + 11 = 22. No double makes 21. 21 is odd, so it <b>cannot</b> be a double."),
           (30, "Yes: 15 + 15", ["No: 15 is odd", "Yes: 10 + 20", "No: 3 is odd"],
            "15 + 15 = 30, so <b>yes</b>. 15 is odd, but 30 ends in 0, so it is even. "
            "Do not look at the first digit, 3.")]
    for n, r, w, e in can:
        assert r.startswith("Yes") == (n % 2 == 0)
        its.append(mcq("Can %d be written as a double (two equal addends)?" % n, r, w, e))

    for h, r, w, e in [(25, "50: even", ["50: odd", "55: odd", "40: even"],
                        "25 + 25: add the tens, 20 + 20 = 40. Add the ones, 5 + 5 = 10. 40 + 10 = <b>50</b>. "
                        "A double is always even. 50 ends in 0."),
                       (35, "70: even", ["70: odd", "65: odd", "60: even"],
                        "35 + 35: add the tens, 30 + 30 = 60. Add the ones, 5 + 5 = 10. 60 + 10 = <b>70</b>. "
                        "A double is always even. 70 ends in 0.")]:
        assert int(r.split(":")[0]) == 2 * h
        its.append(mcq("What is %d + %d? Is the answer odd or even?" % (h, h), r, w, e))
    assert len(its) == 20, len(its)
    return {"title": "Doubles are always even", "items": its}


# ============================================================ set 5: word problems
def set_stories(P):
    its = []

    def add(q, r, w, e):
        its.append(mcq(q, r, w, e))

    add("There are 13 students in gym class. They make partners. Can every student have a partner?",
        "No, 1 is left out", ["Yes, 6 pairs", "Yes, 7 pairs", "No, 2 are left out"],
        "6 pairs make 12 students. 1 student has no partner. 13 is <b>odd</b>.")
    nm, he, his = P.next()
    add("%s has 18 mitts. %s puts them in pairs. How many pairs does %s make?" % (nm, cap(he), he),
        "9 pairs", ["8 pairs", "10 pairs", "36 pairs"],
        "9 + 9 = 18, so 18 mitts make <b>9 pairs</b>. None is left over, so 18 is even.")
    add("There are 7 pairs of winter boots by the classroom door. How many boots are there?",
        "14 boots", ["7 boots", "9 boots", "12 boots"],
        "Each pair has 2 boots. Count by 2s: 2, 4, 6, 8, 10, 12, 14. 7 + 7 = <b>14</b>.")
    add("22 students go on a field trip. Each student needs a buddy. Can every student have a buddy?",
        "Yes, 11 pairs", ["No, 11 is odd", "No, 1 is left out", "Yes, 12 pairs"],
        "11 + 11 = 22. That is 11 pairs, and nobody is left out. 22 is <b>even</b>. "
        "It does not matter that 11 is odd.")
    add("Two hockey teams have the same number of players. There are 24 players in all. Which equation shows this?",
        "12 + 12 = 24", ["11 + 13 = 24", "24 + 24 = 48", "12 + 13 = 25"],
        "The same number on each team means equal addends. <b>12 + 12 = 24</b>. "
        "11 + 13 is 24, but the teams would not be the same.")
    add("A bin at the skating rink has 5 pairs of skates and 1 more skate. How many skates? Odd or even?",
        "11: odd", ["11: even", "10: even", "6: even"],
        "5 pairs is 10 skates. 10 + 1 = 11. The extra skate has no partner, so 11 is <b>odd</b>.")
    nm, he, his = P.next()
    add("%s counts loons on the lake by 2s: 2, 4, 6, 8, 10, 12, 14, 16. How many loons? Odd or even?" % nm,
        "16: even", ["8: even", "16: odd", "17: odd"],
        "The last number %s says is 16, so there are 16 loons. %s said 8 numbers, but each one counts 2 loons. "
        "16 ends in 6, so it is <b>even</b>." % (nm, cap(he)))
    nm, he, his = P.next()
    add("%s has 15 maple candies. %s wants to share them equally with a friend. Can they each get the same number?"
        % (nm, cap(he)), "No, 1 is left over", ["Yes, 7 each", "Yes, 8 each", "Yes, 7 and 8"],
        "7 + 7 = 14 and 8 + 8 = 16. No double makes 15, so 1 candy is left over. 15 is <b>odd</b>. "
        "7 and 8 are not the same number.")
    nm, he, his = P.next()
    m = P.next()[0]
    add("%s and %s each have 8 hockey cards. Which equation shows how many cards they have in all?" % (nm, m),
        "8 + 8 = 16", ["8 + 2 = 10", "8 + 8 = 17", "7 + 9 = 16"],
        "Each child has 8, so add 8 two times: <b>8 + 8 = 16</b>. 16 is even.")
    add("The houses on one side of a street in Ottawa have even numbers. Which house could be on that side?",
        "134", ["143", "127", "161"],
        "134 ends in 4, so it is <b>even</b>. 143, 127 and 161 end in 3, 7 and 1, so they are odd. "
        "Do not look at the first digit.")
    nm, he, his = P.next()
    add("%s has an even number of stickers. It is more than 30 and less than 34. How many stickers does %s have?"
        % (nm, he), "32 stickers", ["31 stickers", "33 stickers", "30 stickers"],
        "The numbers more than 30 and less than 34 are 31, 32 and 33. Only <b>32</b> is even. "
        "30 is even, but it is not more than 30.")
    add("A box has an odd number of pencils. It is more than 45 and less than 48. How many pencils are in the box?",
        "47 pencils", ["46 pencils", "45 pencils", "48 pencils"],
        "The numbers more than 45 and less than 48 are 46 and 47. Only <b>47</b> is odd. "
        "45 is odd, but it is not more than 45.")
    add("17 campers go out in canoes. Each canoe holds 2 campers. How many canoes have 2 campers in them?",
        "8 canoes", ["9 canoes", "7 canoes", "17 canoes"],
        "8 + 8 = 16, so 16 campers fill <b>8 canoes</b>. 1 camper is left over, so 17 is odd.")
    nm, he, his = P.next()
    add("%s has 9 beads. %s wants to put all of them in pairs, with none left over. What is the fewest beads %s must add?"
        % (nm, cap(he), he), "1 bead", ["2 beads", "0 beads", "9 beads"],
        "9 is 4 pairs and 1 left over. Add <b>1 bead</b> to give it a partner. 9 + 1 = 10, and 10 is even.")
    nm, he, his = P.next()
    add("%s picks 15 red apples and 15 green apples at the orchard. Is the number of apples odd or even?" % nm,
        "Even: 15 + 15 = 30", ["Odd: 15 is odd", "Odd: 15 + 15 = 31", "Odd: ends in 5"],
        "15 + 15 = 30 is a double, and doubles are always even. 30 ends in 0. The answer is <b>even</b>.")
    add("There are 8 girls and 5 boys at skating lessons. They skate in pairs. Will everyone have a partner?",
        "No, 1 is left out", ["Yes, 8 is even", "Yes, 7 pairs", "Yes, 6 pairs"],
        "8 + 5 = 13. 6 pairs make 12, so 1 child is left out. 13 is <b>odd</b>.")
    nm, he, his = P.next()
    add("%s puts 30 chairs in 2 equal rows for the school concert. How many chairs are in each row?" % nm,
        "15 chairs", ["30 chairs", "16 chairs", "60 chairs"],
        "2 equal rows means a double. 15 + 15 = 30, so each row has <b>15 chairs</b>.")
    nm, he, his = P.next()
    m = P.next()[0]
    add("%s and %s share 26 stickers equally. How many stickers does each child get?" % (nm, m),
        "13 stickers", ["12 stickers", "14 stickers", "52 stickers"],
        "Find the double that makes 26. 13 + 13 = 26, so each child gets <b>13 stickers</b>.")
    add("There are 21 Canada geese in a field. Then 1 more goose lands. Is the number of geese odd or even now?",
        "Even: 22 geese", ["Odd: 22 geese", "Odd: 21 geese", "Even: 23 geese"],
        "21 is 10 pairs and 1 left over. The new goose is a partner for it. 21 + 1 = 22, and 22 is <b>even</b>.")
    add("27 students walk in pairs in the Terry Fox Run. How many pairs? How many students are left over?",
        "13 pairs, 1 left", ["14 pairs, 0 left", "13 pairs, 0 left", "12 pairs, 3 left"],
        "13 + 13 = 26, so 26 students make <b>13 pairs</b>. 1 student is left over. 27 is odd.")
    assert len(its) == 20, len(its)
    return {"title": "Odd and even word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Odd or even? Make pairs</h2>"
        "<p>Put the things in pairs (groups of 2). If every one has a partner, the number is <b>even</b>. "
        "If 1 is left over, the number is <b>odd</b>.</p>"
        "<figure class='sn-fig'>" + lesson_odd_even_svg(8, 7) +
        "<figcaption>8 counters make 4 pairs with none left over, so 8 is even. "
        "7 counters make 3 pairs and 1 left over, so 7 is odd.</figcaption></figure>"
        "<h2>Look at the ones digit</h2>"
        "<p>Count by 2s from 0: 0, 2, 4, 6, 8, 10, 12, 14. These are the even numbers. "
        "Count by 2s from 1: 1, 3, 5, 7, 9, 11, 13. These are the odd numbers. "
        "For any number, look only at the <b>ones digit</b> (the last digit).</p>"
        + table(["Ones digit", "The number is", "Examples"], [
            ["0, 2, 4, 6, 8", "even", "10, 36, 120, 158"],
            ["1, 3, 5, 7, 9", "odd", "7, 23, 101, 189"],
        ])
        + "<figure class='sn-fig'>" + lesson_digits_svg(147) +
        "<figcaption>147 ends in 7, so 147 is odd. The 1 and the 4 do not matter.</figcaption></figure>"
        + ex("Odd or even?", "Is 136 odd or even?",
             "Look only at the ones digit. 136 ends in 6, and 6 is even. The 1 at the start does not matter.", "even")
        + "<h2>A double is always even</h2>"
        "<p>An even number can be split into 2 equal groups. So it is a double, "
        "like 14 = 7 + 7. An odd number is never a double.</p>"
        "<figure class='sn-fig'>" + lesson_double_svg(7) +
        "<figcaption>14 stars in 2 equal rows. Each row has 7, so 14 = 7 + 7.</figcaption></figure>"
        + table(["Even number", "Double"], [
            ["10", "5 + 5"], ["14", "7 + 7"], ["18", "9 + 9"], ["30", "15 + 15"], ["50", "25 + 25"],
        ])
        + ex("No double", "Can 15 be written as a double?",
             "7 + 7 = 14 and 8 + 8 = 16. No double makes 15, because 15 is odd.", "No")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Looking at the first digit: 136 starts with 1, so it is odd",
             "Look at the ones digit: 6 is even, so 136 is even"],
            ["Thinking 0 is not odd or even", "0 is even, so 10, 20 and 120 are even too"],
            ["Forgetting the one left over: 147 is 73 pairs, so it is even", "73 pairs and 1 left over: 147 is odd"],
            ["Thinking 18 is odd because 9 is odd (18 = 9 + 9)", "18 is 9 pairs with none left over, so 18 is even"],
            ["Using different addends: 14 = 6 + 8", "A double uses the same number: 14 = 7 + 7"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about odd and even numbers in Ontario?",
     "a": "In the Ontario math curriculum (B1.5), Grade 2 students describe what makes a number even or odd. "
          "They make pairs, count by 2s and look at the ones digit for numbers up to 200."},
    {"q": "How do you know if a number is odd or even?",
     "a": "Look at the ones digit (the last digit). If it is 0, 2, 4, 6 or 8, the number is even; "
          "if it is 1, 3, 5, 7 or 9, the number is odd."},
    {"q": "Is 0 an even number?",
     "a": "Yes, 0 is even. Counting by 2s starts at 0, and numbers that end in 0, like 10, 50 and 120, are even too."},
    {"q": "How can I help my child practise odd and even numbers at home?",
     "a": "Pair up mitts, socks or toy cars and check if one is left over. Then count by 2s together and "
          "look at house numbers on your street: one side is usually even and the other side odd."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so the objects stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_figures(sets):
    """Objects drawn must match the number in the aria-label."""
    for s in sets:
        for it in s["items"]:
            svgs = re.findall(r"<svg.*?</svg>", it["q"])
            assert len(svgs) <= 1
            for svg in svgs:
                n_obj = len(re.findall(r"<(circle|rect x='[\d.]+' y='[\d.]+' width='19'|polygon)", svg))
                m = re.search(r"aria-label='(\d+) \w+ (in pairs|mixed up)'", svg)
                if m:
                    assert n_obj == int(m.group(1)), (m.group(0), n_obj)


def gen():
    rnd = random.Random(42803)
    P = People(rnd)
    sets = [set_pairs(P, rnd), set_ones_digit(P), set_to_200(P), set_doubles(P), set_stories(P)]
    check_figures(sets)
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert "\\" not in it["q"] + it["e"] + "".join(it["c"])
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "odd-and-even-numbers", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Odd and Even Numbers to 200",
        "seo_title": "Grade 2 Odd and Even Numbers Worksheets: Pairs, Ones Digit and Doubles (Free, Answer Key, Ontario)",
        "short_title": "Odd and even numbers",
        "domain": "Number",
        "standard_code": "Grade 2: B1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Describe what makes a number even or odd",
        "meta_desc": "Free Grade 2 math worksheets on odd and even numbers for the Ontario curriculum: make pairs "
                     "and look for one left over, count by 2s, use the ones digit for numbers to 200, and see why "
                     "doubles like 7 + 7 are always even. 100 questions with an answer key.",
        "key_big": "Even numbers make pairs with none left over. Odd numbers have 1 left over.",
        "key_sub": "Look only at the ones digit: 0, 2, 4, 6 and 8 mean even. 136 is even because it ends in 6, "
                   "not because of the 1. 0 is even. Every double is even: 14 = 7 + 7.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    u = mark_large(u, "four groups labelled A to D")
    return mark_large(u, "number line counting by 2s")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
