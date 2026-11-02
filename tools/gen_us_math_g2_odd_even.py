# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Odd and Even Numbers (2.OA.C.3)
  python tools/gen_us_math_g2_odd_even.py
Every count, sum and odd/even label is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 2: short sentences for 7-8 year olds.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
GOLD = "#e3a81b"
INK = "#2b2b2b"
GRAY = "#9a948c"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


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


def unit(k, one, many):
    return "%d %s" % (k, one if k == 1 else many)


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
    import math
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
    CP = PITCH + gx                 # column pitch (wider in the lesson so the pair outlines do not touch)
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


def pairs_svg(n, kind, outline=False):
    o = 6
    body, w, h = pairs_body(o, o, n, kind, outline=outline)
    return svg_wrap(w + 2 * o, h + 2 * o, body, "%d %s in pairs" % (n, KINDS[kind][1] if n != 1 else KINDS[kind][0]))


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
    """2 x 2 grid of groups labeled A to D. Each group is drawn in pairs."""
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
    return svg_wrap(W, H, "".join(s), "four groups labeled A to D")


def two_groups_svg(a, b, kind="counters"):
    """Group a (red) + group b (green), each in pairs."""
    o, gap = 6, 40
    ba, wa, h = pairs_body(o, o, a, kind, RED)
    bb, wb, _ = pairs_body(o + wa + gap, o, b, kind, GREEN)
    plus = text(o + wa + gap / 2, o + h / 2 + 9, "+", 26)
    return svg_wrap(wa + wb + gap + 2 * o, h + 2 * o, ba + plus + bb, "%d counters and %d counters" % (a, b))


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


# ============================================================ set 1: pair up objects
def set_pairs(P, rnd):
    its = []
    for n, kind in [(7, "counters"), (10, "stars"), (13, "blocks"), (6, "counters"),
                    (15, "stars"), (12, "blocks"), (9, "counters"), (16, "stars")]:
        one, many, _ = KINDS[kind]
        h = n // 2
        q = fig(pairs_svg(n, kind)) + "How many %s are there? Is the number odd or even?" % many
        if n % 2:
            e = ("Make pairs: %d pairs and 1 %s left over. One left over means odd. "
                 "So %d is <b>odd</b>." % (h, one, n))
        else:
            e = ("Make pairs: %d pairs and none left over. Every %s has a partner, "
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
            e = "Count each pair by 2s: %s. Then add the 1 left over: %d + 1 = <b>%d</b>." % (say, n - 1, n)
        else:
            e = "Count each pair by 2s: %s. There are <b>%d</b> %s." % (say, n, many)
        its.append(mcq(q, n, [cols, n + 1, n - 1, n + 2], e))

    for n, kind in [(11, "stars"), (12, "counters"), (9, "blocks"), (14, "stars")]:
        one, many, _ = KINDS[kind]
        h = n // 2
        q = (fig(scattered_svg(n, kind, rnd))
             + "Make pairs. How many pairs can you make? How many %s are left over?" % many)
        if n % 2:
            right = "%d pairs, 1 left" % h
            wrong = ["%d pairs, 0 left" % (h + 1), "%d pairs, 0 left" % h, "%d pairs, 3 left" % (h - 1)]
            e = ("There are %d %s. Join them 2 at a time. You get %d pairs, and 1 %s has no partner. "
                 "%d + %d + 1 = %d, so %d is odd." % (n, many, h, one, h, h, n, n))
        else:
            right = "%d pairs, 0 left" % h
            wrong = ["%d pairs, 1 left" % h, "%d pairs, 2 left" % (h - 1), "%d pairs, 0 left" % n]
            e = ("There are %d %s. Join them 2 at a time. You get %d pairs, and none is left over. "
                 "2 left over can still make 1 more pair. %d is even." % (n, many, h, n))
        its.append(mcq(q, right, wrong, e))

    # A-D pictures: answer position fixed (A, B, C, D once each)
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
    return {"title": "Pair up objects: odd or even?", "items": its}


# ============================================================ set 2: count by 2s, ones digit
def set_ones_digit(P):
    its = []
    for seq, k in [([4, 6, 8, 10, 12], 3), ([12, 14, 16, 18], 2), ([3, 5, 7, 9], 3), ([11, 13, 15, 17, 19], 3)]:
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
         "0 is <b>even</b>. When you count by 2s, you start at 0: 0, 2, 4, 6. That is why 10 and 20 are even too."),
    ]
    for q, r, w, e in one_digit:
        n = int(re.search(r"\d+", q).group())
        assert r.lower().startswith(par(n)), q
        its.append(mcq(q, r, w, e))

    # which number is even / odd: wrong choices trap a child who looks at the wrong digit
    pick = [("even", 20, [21, 23, 25], "20 ends in 0, and 0 is even. 21, 23 and 25 end in 1, 3 and 5, so they are odd."),
            ("odd", 41, [14, 40, 22], "41 ends in 1, so it is odd. 14, 40 and 22 end in 4, 0 and 2, so they are even."),
            ("even", 36, [41, 63, 25], "Look at the ones digit only. 36 ends in 6, so it is even. "
                                        "41, 63 and 25 end in 1, 3 and 5. Their tens digits do not matter."),
            ("odd", 57, [52, 74, 38], "57 ends in 7, so it is odd. 52, 74 and 38 end in 2, 4 and 8, so they are even."),
            ("even", 128, [281, 463, 605], "For big numbers, still look at the ones digit. 128 ends in 8, so it is even. "
                                            "281, 463 and 605 end in 1, 3 and 5, so they are odd."),
            ("odd", 357, [574, 932, 716], "357 ends in 7, so it is odd. 574, 932 and 716 end in 4, 2 and 6, so they are even. "
                                           "The first digit does not matter.")]
    stems = ["Which number is <b>%s</b>?", "Which number is <b>%s</b>?", "Which of these numbers is <b>%s</b>?",
             "Which of these numbers is <b>%s</b>?", "Which big number is <b>%s</b>?", "Which big number is <b>%s</b>?"]
    for stem, (want, r, w, e) in zip(stems, pick):
        assert par(r) == want and all(par(x) != want for x in w)
        its.append(mcq(stem % want, r, w, e))

    lists = [("even", "10, 12, 14, 16", ["10, 12, 15, 16", "11, 13, 15, 17", "12, 14, 17, 18"],
              "10, 12, 14 and 16 end in 0, 2, 4 and 6. They are all even. The other lists have 15, 17 or odd numbers."),
             ("odd", "13, 15, 17, 19", ["13, 15, 18, 19", "12, 14, 16, 18", "11, 14, 17, 19"],
              "13, 15, 17 and 19 end in 3, 5, 7 and 9. They are all odd. The other lists have 18, 14 or even numbers.")]
    for want, r, w, e in lists:
        assert all(par(int(x)) == want for x in r.split(", "))
        assert all(any(par(int(x)) != want for x in l.split(", ")) for l in w)
        its.append(mcq("Which list has only <b>%s</b> numbers?" % want, r, w, e))
    its[-2]["e"] = ("10, 12, 14 and 16 end in 0, 2, 4 and 6. They are all even. "
                    "Each other list has at least one odd number, like 15 or 17.")
    its[-1]["e"] = ("13, 15, 17 and 19 end in 3, 5, 7 and 9. They are all odd. "
                    "Each other list has at least one even number, like 18 or 14.")

    its.append(mcq("What is the next <b>even</b> number after 17?", 18, [19, 16, 20],
                   "The number after 17 is 18. 18 ends in 8, so it is even. The answer is <b>18</b>. 19 is the next odd number."))
    its.append(mcq("What is the next <b>odd</b> number after 24?", 25, [26, 23, 27],
                   "The number after 24 is 25. 25 ends in 5, so it is odd. The answer is <b>25</b>. 26 is the next even number."))

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
    return {"title": "Count by 2s and look at the ones digit", "items": its}


# ============================================================ set 3: doubles (equal addends)
def set_doubles(P):
    its = []
    for h, kind in [(4, "counters"), (7, "stars"), (5, "blocks"), (9, "counters"), (6, "stars"), (8, "blocks")]:
        one, many, _ = KINDS[kind]
        n = 2 * h
        q = fig(pairs_svg(n, kind)) + "The %s are in 2 equal rows. Which equation matches the picture?" % many
        e = ("Each row has %d %s. Two equal rows make a double: %d + %d = <b>%d</b>. "
             "%d is even." % (h, many, h, h, n, n))
        its.append(mcq(q, "%d + %d = %d" % (h, h, n),
                       ["%d + %d = %d" % (h - 1, h + 1, n), "%d + 2 = %d" % (h, h + 2), "%d + %d = %d" % (h, h, n - 2)], e))

    for n in [12, 18, 14, 20, 16, 10]:
        h = n // 2
        q = "Which shows %d as a sum of two equal addends?" % n
        w = ["%d + %d" % (h - 1, h + 1), "%d + %d" % (n, n)]
        w.append("%d + %d" % (n // 10, n % 10) if n % 10 else "%d + %d" % (h - 1, h - 1))
        e = ("Equal addends are the same number. %d + %d = %d, so %d = <b>%d + %d</b>. "
             "%d + %d also makes %d, but %d and %d are not equal." % (h, h, n, n, h, h, h - 1, h + 1, n, h - 1, h + 1))
        its.append(mcq(q, "%d + %d" % (h, h), w, e))

    for n, q in [(14, "Which equation shows an even number as a sum of two equal addends?"),
                 (18, "Which equation is true <b>and</b> has two equal addends?"),
                 (12, "Which equation shows a double that is correct?"),
                 (16, "Which one writes an even number as two equal addends?")]:
        h = n // 2
        right = "%d = %d + %d" % (n, h, h)
        w = ["%d = %d + %d" % (n + 1, h, h), "%d = %d + %d" % (n, h - 1, h + 1), "%d = %d + %d" % (n + 1, h, h + 1)]
        e = ("%d + %d = %d, so <b>%s</b> is true and the addends are equal. %s is not true. "
             "%s is true, but %d and %d are not equal." % (h, h, n, right, w[0], w[1], h - 1, h + 1))
        its.append(mcq(q, right, w, e))

    can = [(15, "No: 15 is odd", ["Yes: 7 + 7", "Yes: 7 + 8", "Yes: 5 + 5 + 5"],
            "7 + 7 = 14 and 8 + 8 = 16. No double makes 15. 15 is odd, so it <b>cannot</b> be two equal addends."),
           (18, "Yes: 9 + 9", ["No: 9 is odd", "Yes: 8 + 10", "No: 1 is odd"],
            "9 + 9 = 18, so <b>yes</b>. It does not matter that 9 is odd. 18 ends in 8, so it is even."),
           (13, "No: 13 is odd", ["Yes: 6 + 7", "Yes: 6 + 6", "Yes: 7 + 7"],
            "6 + 6 = 12 and 7 + 7 = 14. No double makes 13. 13 is odd, so it <b>cannot</b> be two equal addends."),
           (10, "Yes: 5 + 5", ["No: 5 is odd", "Yes: 4 + 6", "Yes: 10 + 10"],
            "5 + 5 = 10, so <b>yes</b>. 5 is odd, but 10 is even. 4 + 6 also makes 10, but 4 and 6 are not equal.")]
    for n, r, w, e in can:
        assert (r.startswith("Yes")) == (n % 2 == 0)
        its.append(mcq("Can %d be written as a sum of two equal addends?" % n, r, w, e))
    assert len(its) == 20, len(its)
    return {"title": "Even numbers as doubles", "items": its}


# ============================================================ set 4: odd and even sums
def sum_e(a, b):
    s = a + b
    if a % 2 and b % 2:
        return "%d and %d are both odd. Each has 1 left over, and the two left-overs make a pair. Odd + odd is even." % (a, b)
    if a % 2 == 0 and b % 2 == 0:
        return "%d and %d are both even. Every one already has a partner. Even + even is even." % (a, b)
    o = a if a % 2 else b
    return "Only %d has 1 left over. Nothing pairs with it. Even + odd is odd." % o


def set_sums(P):
    its = []
    for a, b in [(3, 5), (4, 6), (5, 4), (2, 7), (7, 5), (6, 8)]:
        s = a + b
        q = fig(two_groups_svg(a, b)) + "How many counters are there in all? Is the number odd or even?"
        e = sum_e(a, b) + " %d + %d = %d, which is <b>%s</b>." % (a, b, s, par(s))
        alt = "odd" if s % 2 == 0 else "even"
        its.append(mcq(q, "%d: %s" % (s, par(s)),
                       ["%d: %s" % (s, alt), "%d: %s" % (s - 1, par(s - 1)), "%d: %s" % (s + 1, par(s + 1))], e))

    def rule_ok(r):
        x, _, y, _, z = r.split()
        return ("even" if (x == "odd") == (y == "odd") else "odd") == z

    rules = [("Which sentence is true?", "odd + odd = even",
              ["odd + odd = odd", "even + odd = even", "even + even = odd"],
              "Two odd numbers each have 1 left over. Those two make a pair. So <b>odd + odd = even</b>, like 3 + 5 = 8."),
             ("Which one is always true?", "even + even = even",
              ["even + even = odd", "odd + odd = odd", "odd + even = even"],
              "In two even numbers, everything is in pairs. Nothing is left over. So <b>even + even = even</b>, like 4 + 6 = 10."),
             ("Which rule is correct?", "even + odd = odd",
              ["even + odd = even", "odd + odd = odd", "even + even = odd"],
              "The odd number has 1 left over, and nothing pairs with it. So <b>even + odd = odd</b>, like 4 + 5 = 9.")]
    for q, r, w, e in rules:
        assert rule_ok(r) and not any(rule_ok(x) for x in w)
        its.append(mcq(q, r, w, e))
    its.append(mcq("Which example shows odd + odd = even?", "3 + 5 = 8", ["3 + 4 = 7", "2 + 6 = 8", "3 + 5 = 9"],
                   "3 and 5 are both odd, and 3 + 5 = <b>8</b> is even. 3 + 4 uses an even number, 4. "
                   "2 + 6 uses two even numbers. And 3 + 5 is 8, not 9."))

    for a, b in [(7, 9), (6, 8), (5, 8), (12, 7), (13, 15), (14, 6)]:
        s = a + b
        pa, pb = par(a), par(b)
        right = "%s: %s + %s" % (Par(s), pa, pb)
        alt = "Odd" if s % 2 == 0 else "Even"
        w = ["%s: %s + %s" % (alt, pa, pb)]
        if par(b) != par(s):
            w.append("%s: ends in %d" % (Par(b), b % 10))          # looked only at the last number
        else:
            w.append("%s: %d + %d = %d" % (Par(s - 1), a, b, s - 1))   # added wrong
        w.append("%s: %d + %d = %d" % (Par(s + 1), a, b, s + 1))       # added wrong
        q = "Do not add. Is %d + %d odd or even?" % (a, b)
        e = "%d is %s and %d is %s. %s + %s is always %s, so %d + %d is <b>%s</b>. Check: %d + %d = %d." % (
            a, pa, b, pb, cap(pa), pb, par(s), a, b, par(s), a, b, s)
        its.append(mcq(q, right, w, e))

    for stem, want, r, w in [("Which sum is <b>%s</b>?", "even", "3 + 5", ["4 + 3", "6 + 7", "9 + 2"]),
                             ("Which sum is <b>%s</b>?", "odd", "6 + 7", ["5 + 7", "4 + 8", "9 + 9"]),
                             ("Do not add. Which sum is <b>%s</b>?", "even", "9 + 7", ["8 + 5", "2 + 9", "6 + 3"]),
                             ("Do not add. Which sum is <b>%s</b>?", "odd", "4 + 9", ["3 + 7", "6 + 6", "5 + 11"])]:
        val = lambda t: sum(int(x) for x in t.split(" + "))
        assert par(val(r)) == want and all(par(val(x)) != want for x in w)
        kind = lambda t: " + ".join(par(int(x)) for x in t.split(" + "))
        e = "%s is %s, so it is <b>%s</b>: %s = %d. The others are %s, so they are %s: %s." % (
            r, kind(r), want, r, val(r), " or ".join(sorted({kind(x) for x in w})), par(val(w[0])),
            ", ".join("%s = %d" % (x, val(x)) for x in w))
        its.append(mcq(stem % want, r, w, e))
    assert len(its) == 20, len(its)
    return {"title": "Odd and even sums", "items": its}


# ============================================================ set 5: word problems
def set_stories(P):
    its = []

    def add(q, r, w, e):
        its.append(mcq(q, r, w, e))

    add("There are 15 children in a class. They make partners. Can every child have a partner?",
        "No, 1 is left out", ["Yes, 7 pairs", "Yes, 8 pairs", "No, 2 are left out"],
        "7 pairs make 14 children. 1 child has no partner. 15 is <b>odd</b>.")
    nm, he, his = P.next()
    add("%s has 18 socks. %s puts them in pairs. How many pairs does %s make?" % (nm, cap(he), he),
        "9 pairs", ["8 pairs", "10 pairs", "36 pairs"],
        "9 + 9 = 18, so 18 socks make <b>9 pairs</b>. None is left over, so 18 is even.")
    add("There are 7 pairs of shoes by the door. How many shoes are there?",
        "14 shoes", ["7 shoes", "9 shoes", "12 shoes"],
        "Each pair has 2 shoes. Count by 2s: 2, 4, 6, 8, 10, 12, 14. 7 + 7 = <b>14</b>.")
    add("18 children go on a trip. Each child needs a buddy. Can every child have a buddy?",
        "Yes, 9 pairs", ["No, 9 is odd", "No, 1 is left out", "Yes, 8 pairs"],
        "9 + 9 = 18. That is 9 pairs, and nobody is left out. 18 is <b>even</b>. It does not matter that 9 is odd.")
    add("Two teams have the same number of players. There are 16 players in all. Which equation shows this?",
        "8 + 8 = 16", ["7 + 9 = 16", "16 + 16 = 32", "8 + 9 = 17"],
        "The same number on each team means equal addends. <b>8 + 8 = 16</b>. 7 + 9 is 16, but the teams would not be the same.")
    nm, he, his = P.next()
    add("There are 5 pairs of mittens and 1 more mitten in a box. How many mittens are there? Is the number odd or even?",
        "11: odd", ["11: even", "10: even", "6: even"],
        "5 pairs is 10 mittens. 10 + 1 = 11. The extra mitten has no partner, so 11 is <b>odd</b>.")
    add("%s counts %s toy cars by 2s: 2, 4, 6, 8, 10, 12. How many toy cars are there? Is the number odd or even?"
        % (nm, his), "12: even", ["6: even", "12: odd", "13: odd"],
        "The last number %s says is 12, so there are 12 cars. %s said 6 numbers, but each one counts 2 cars. "
        "12 ends in 2, so it is <b>even</b>." % (he, cap(he)))
    nm, he, his = P.next()
    add("%s has 13 crayons. %s wants to share them equally with a friend. Can they each get the same number?"
        % (nm, cap(he)), "No, 1 is left over", ["Yes, 6 each", "Yes, 7 each", "Yes, 6 and 7"],
        "6 + 6 = 12 and 7 + 7 = 14. No double makes 13, so 1 crayon is left over. 13 is <b>odd</b>. "
        "6 and 7 are not the same number.")
    nm, he, his = P.next()
    m = P.next()[0]
    add("%s and %s each have 6 shells. Which equation shows how many shells they have in all?" % (nm, m),
        "6 + 6 = 12", ["6 + 2 = 8", "6 + 6 = 13", "5 + 7 = 12"],
        "Each child has 6, so add 6 two times: <b>6 + 6 = 12</b>. 12 is even.")
    add("Houses on one side of a street have even numbers. Which house could be on that side?",
        "34", ["43", "27", "61"],
        "34 ends in 4, so it is even. 43, 27 and 61 end in 3, 7 and 1, so they are odd. Do not look at the tens digit.")
    nm, he, his = P.next()
    add("%s has an even number of marbles. It is more than 10 and less than 14. How many marbles does %s have?"
        % (nm, he), "12 marbles", ["11 marbles", "13 marbles", "10 marbles"],
        "The numbers more than 10 and less than 14 are 11, 12 and 13. Only <b>12</b> is even. 10 is not more than 10.")
    add("A box has an odd number of pencils. It is more than 15 and less than 18. How many pencils are in the box?",
        "17 pencils", ["16 pencils", "15 pencils", "18 pencils"],
        "The numbers more than 15 and less than 18 are 16 and 17. Only <b>17</b> is odd. 15 is not more than 15.")
    add("17 children ride a bus. Each seat holds 2 children. How many seats have 2 children in them?",
        "8 seats", ["9 seats", "7 seats", "17 seats"],
        "8 + 8 = 16, so 16 children fill <b>8 seats</b>. The last child sits alone. 17 is odd.")
    nm, he, his = P.next()
    add("%s has 9 beads. %s wants to put all of them in pairs, with none left over. What is the fewest beads %s must add?"
        % (nm, cap(he), he), "1 bead", ["2 beads", "0 beads", "9 beads"],
        "9 is 4 pairs and 1 left over. Add <b>1 bead</b> to give it a partner. 9 + 1 = 10, and 10 is even.")
    nm, he, his = P.next()
    add("%s has 7 red apples and 7 green apples. Is the number of apples odd or even?" % nm,
        "Even: 7 + 7 = 14", ["Odd: 7 is odd", "Odd: 7 + 7 = 15", "Odd: odd + odd"],
        "7 + 7 = 14 is a double, and doubles are always even. Odd + odd is even, too. The answer is <b>even</b>.")
    add("There are 8 girls and 5 boys in a dance class. They dance in pairs. Will everyone have a partner?",
        "No, 1 is left out", ["Yes, 8 is even", "Yes, 7 pairs", "Yes, 6 pairs"],
        "8 + 5 = 13. 6 pairs make 12, so 1 child is left out. Even + odd is <b>odd</b>.")
    nm, he, his = P.next()
    add("%s has 5 red blocks and 7 blue blocks. Can %s put all the blocks in pairs?" % (nm, he),
        "Yes, 6 pairs", ["No, 1 is left over", "No, both are odd", "Yes, 7 pairs"],
        "5 + 7 = 12. 12 is 6 pairs with none left over, so <b>yes</b>. Odd + odd is even.")
    nm, he, his = P.next()
    add("%s puts 20 chairs in 2 equal rows. How many chairs are in each row?" % nm,
        "10 chairs", ["20 chairs", "11 chairs", "40 chairs"],
        "2 equal rows means a double. 10 + 10 = 20, so each row has <b>10 chairs</b>.")
    nm, he, his = P.next()
    m = P.next()[0]
    add("%s and %s share 14 stickers equally. How many stickers does each child get?" % (nm, m),
        "7 stickers", ["6 stickers", "8 stickers", "28 stickers"],
        "Find the double that makes 14. 7 + 7 = 14, so each child gets <b>7 stickers</b>.")
    nm, he, his = P.next()
    add("%s puts 19 cups in pairs. Then a friend brings 1 more cup. Is the number of cups odd or even now?" % nm,
        "Even: 20 cups", ["Odd: 20 cups", "Odd: 19 cups", "Even: 21 cups"],
        "19 is 9 pairs and 1 left over. The new cup is a partner for it. 19 + 1 = 20, and 20 is <b>even</b>.")
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
        "For any number, look only at the <b>ones digit</b>.</p>"
        + table(["Ones digit", "The number is", "Examples"], [
            ["0, 2, 4, 6, 8", "even", "10, 14, 36, 128"],
            ["1, 3, 5, 7, 9", "odd", "7, 15, 23, 57"],
        ])
        + ex("Odd or even?", "Is 57 odd or even?",
             "Look only at the ones digit. 57 ends in 7, and 7 is odd. The 5 tens do not matter.", "odd")
        + "<h2>An even number is a double</h2>"
        "<p>An even number can be split into 2 equal groups. So you can write it as a sum of "
        "<b>two equal addends</b>: 14 = 7 + 7.</p>"
        "<figure class='sn-fig'>" + lesson_double_svg(7) +
        "<figcaption>14 stars in 2 equal rows. Each row has 7, so 14 = 7 + 7.</figcaption></figure>"
        + table(["Even number", "Two equal addends"], [
            ["10", "5 + 5"], ["12", "6 + 6"], ["14", "7 + 7"], ["16", "8 + 8"], ["18", "9 + 9"], ["20", "10 + 10"],
        ])
        + ex("No double", "Can 15 be written as two equal addends?",
             "7 + 7 = 14 and 8 + 8 = 16. No double makes 15, because 15 is odd.", "No")
        + "<h2>Adding odd and even numbers</h2>"
        + table(["Add", "The sum is", "Example"], [
            ["even + even", "even", "4 + 6 = 10"],
            ["odd + odd", "even", "3 + 5 = 8"],
            ["even + odd", "odd", "4 + 5 = 9"],
        ])
        + "<p>Odd + odd is even: each odd number has 1 left over, and the two left-overs make a pair.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Looking at the tens digit: 23 has 2 tens, so it is even", "Look at the ones digit: 3 is odd, so 23 is odd"],
            ["Thinking 0 is not odd or even", "0 is even, so 10, 20 and 30 are even too"],
            ["Thinking odd + odd is odd", "The two left-overs make a pair: 3 + 5 = 8, even"],
            ["Writing 15 = 7 + 7", "7 + 7 = 14. 15 is odd, so it has no double"],
            ["Using different addends: 14 = 6 + 8", "Equal addends are the same: 14 = 7 + 7"],
            ["Thinking 18 is odd because 9 is odd (18 = 9 + 9)", "18 is 9 pairs with none left over, so 18 is even"],
        ])
    )


FAQ = [
    {"q": "How do you know if a number is odd or even?",
     "a": "Look at the ones digit. If it is 0, 2, 4, 6 or 8, the number is even; if it is 1, 3, 5, 7 or 9, the number is odd."},
    {"q": "Is 0 an even number?",
     "a": "Yes, 0 is even. Counting by 2s starts at 0, and numbers that end in 0, like 10 and 20, are even too."},
    {"q": "What does a sum of two equal addends mean in 2nd grade?",
     "a": "It means writing a number as a double, like 14 = 7 + 7. Only even numbers can be written this way (Common Core 2.OA.C.3)."},
    {"q": "How can I teach odd and even numbers to my child?",
     "a": "Start with real things: pair up socks or blocks and see if one is left over. Then count by 2s together and notice that even numbers end in 0, 2, 4, 6 or 8."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D groups) so the objects stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_figures(sets):
    """Objects drawn must match the number in the aria-label."""
    for s in sets:
        for it in s["items"]:
            for svg in re.findall(r"<svg.*?</svg>", it["q"]):
                n_obj = len(re.findall(r"<(circle|rect x='[\d.]+' y='[\d.]+' width='19'|polygon)", svg))
                m = re.search(r"aria-label='(\d+) \w+ (in pairs|mixed up)'", svg)
                if m:
                    assert n_obj == int(m.group(1)), (m.group(0), n_obj)
                m = re.search(r"aria-label='(\d+) counters and (\d+) counters'", svg)
                if m:
                    assert n_obj == int(m.group(1)) + int(m.group(2))


def gen():
    rnd = random.Random(210)
    P = People(rnd)
    sets = [set_pairs(P, rnd), set_ones_digit(P), set_doubles(P), set_sums(P), set_stories(P)]
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
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "odd-and-even", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Odd and Even Numbers",
        "seo_title": "Grade 2 Odd and Even Numbers Worksheets: Pairs, Counting by 2s and Doubles",
        "short_title": "Odd and even numbers",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "2.OA.C.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/OA/C/3/",
        "standard_text": "Determine whether a group of objects (up to 20) has an odd or even number of members, e.g., by pairing objects or counting them by 2s; write an equation to express an even number as a sum of two equal addends.",
        "meta_desc": "Free Grade 2 odd and even worksheets: pair up objects, count by 2s, use the ones digit, write even numbers as doubles like 14 = 7 + 7, and add odd and even numbers. 100 practice questions with answers.",
        "key_big": "Even numbers make pairs with none left over. Odd numbers have 1 left over.",
        "key_sub": "Look at the ones digit: 0, 2, 4, 6 and 8 mean even. 57 is odd because it ends in 7. Every even number is a double: 14 = 7 + 7.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "four groups labeled A to D")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
