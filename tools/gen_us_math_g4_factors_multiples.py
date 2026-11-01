# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Factors, Multiples, Prime and Composite (4.OA.B.4)
  python tools/gen_us_math_g4_factors_multiples.py
All numbers are 1-100. Every factor, multiple and prime fact is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ math
def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def pairs(n):
    return [(d, n // d) for d in factors(n) if d * d <= n]


def is_prime(n):
    return len(factors(n)) == 2


def lst(xs):
    return ", ".join(str(x) for x in xs)


def rem(n, d):
    q, r = divmod(n, d)
    assert r, (n, d)
    return "%d ÷ %d = %d R %d" % (n, d, q, r)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
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
    ch = [correct] + pick
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def tiles(x0, y0, rows, cols, cell):
    return "".join("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                   % (x0 + c * cell, y0 + r * cell, cell, cell, FILL, GREEN) for r in range(rows) for c in range(cols))


def array_svg(rows, cols, cell=22):
    o = 6
    return svg_wrap(cols * cell + 2 * o, rows * cell + 2 * o, tiles(o, o, rows, cols, cell),
                    "array of square tiles in %d rows and %d columns" % (rows, cols))


def dots_svg(rows, cols, size=30):
    o = 6
    s = ["<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='2.5'/>"
         % (o, o, cols * size + 8, rows * size + 8, INK)]
    for r in range(rows):
        for c in range(cols):
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (o + 4 + c * size + size // 2, o + 4 + r * size + size // 2, size // 2 - 3, "#f3ead2", INK))
    return svg_wrap(cols * size + 8 + 2 * o, rows * size + 8 + 2 * o, "".join(s),
                    "egg carton with %d rows of %d eggs" % (rows, cols))


def rects_svg(n, cell=14):
    """Every rectangle that can be made with n tiles, side by side, labeled underneath."""
    ps = [(a, b) for a, b in pairs(n)]
    gap, o = 26, 8
    widths = [max(b * cell, 50) for a, b in ps]
    hmax = max(a for a, b in ps) * cell
    W = sum(widths) + gap * (len(ps) - 1) + 2 * o
    H = o + hmax + 28
    s, x = [], o
    for (a, b), w in zip(ps, widths):
        tx = x + (w - b * cell) / 2
        s.append(tiles(int(tx), o + hmax - a * cell, a, b, cell))
        s.append(text(x + w / 2, o + hmax + 22, "%d × %d" % (a, b)))
        x += w + gap
    return svg_wrap(W, H, "".join(s), "every rectangle made with %d tiles" % n)


def rainbow_svg(n, step=40):
    """Factor rainbow: the factors of n in a row, each factor pair joined by an arc."""
    fs = factors(n)
    o, top = 20, 76
    W = (len(fs) - 1) * step + 2 * o
    xs = {f: o + i * step for i, f in enumerate(fs)}
    s = []
    for k, (a, b) in enumerate(pairs(n)):
        if a == b:
            continue
        ry = 16 + 14 * (len(pairs(n)) - 1 - k)
        s.append("<path d='M %d %d A %d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xs[a], top, (xs[b] - xs[a]) // 2, ry, xs[b], top, GREEN))
    for f in fs:
        s.append(text(xs[f], top + 22, str(f), 18))
    return svg_wrap(W, top + 30, "".join(s), "factor rainbow for %d" % n)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def pairs_txt(n):
    return ", ".join("%d × %d" % p for p in pairs(n))


def rect_word(k):
    return "1 rectangle" if k == 1 else "%d rectangles" % k


# ============================================================ set 1: factor pairs and arrays
def set_pairs(P):
    its = []
    for r, c in [(3, 4), (2, 8), (4, 5), (3, 6), (4, 6), (5, 6)]:
        n = r * c
        q = (fig(array_svg(r, c)) + "%d square tiles are in %d equal rows. Find the missing factor: %d × <b>?</b> = %d"
             % (n, r, r, n))
        e = ("Count the tiles in one row: <b>%d</b>. %d rows of %d make %d, so %d and %d are a factor pair of %d."
             % (c, r, c, n, r, c, n))
        its.append(mcq(q, c, [n - r, c + 1, c - 1, n + r], e))

    for n in [12, 18, 13, 16, 24, 36]:
        ps = pairs(n)
        k = len(ps)
        nf = len(factors(n))
        a, b = ps[1] if k > 1 else ps[0]
        q = ("You have %d square tiles. How many different rectangles can you make with all %d tiles? "
             "(Turning a rectangle, like %d × %d to %d × %d, does not make a new one.)" % (n, n, a, b, b, a))
        if n == 13:
            e = ("13 is a prime number. The only factor pair is 1 × 13, so you can make <b>1 rectangle</b>: "
                 "one long row. A single row still counts as a rectangle.")
        else:
            e = ("Each rectangle is a factor pair: %s. That is <b>%s</b>. Don’t forget the long 1 × %d row%s."
                 % (pairs_txt(n), rect_word(k), n,
                    ", and count %d × %d only once" % (ps[-1]) if ps[-1][0] == ps[-1][1] else ""))
        its.append(mcq(q, rect_word(k), [rect_word(x) for x in (k - 1, nf, k + 1, k + 2)], e))

    for n, (a, b), wrong in [(28, (4, 7), [(8, 20), (3, 9), (5, 6)]), (42, (6, 7), [(20, 22), (6, 8), (5, 8)]),
                             (32, (4, 8), [(16, 16), (4, 9), (3, 11)]), (45, (5, 9), [(20, 25), (6, 8), (4, 11)])]:
        assert a * b == n and all(x * y != n for x, y in wrong) and wrong[0][0] + wrong[0][1] == n
        e = ("%d × %d = <b>%d</b>. %d + %d is also %d, but a factor pair must <b>multiply</b> to %d, not add to it."
             % (a, b, n, wrong[0][0], wrong[0][1], n, n))
        its.append(mcq("Which is a factor pair of %d?" % n, "%d and %d" % (a, b),
                       ["%d and %d" % w for w in wrong], e))

    for n, shown, miss, near in [(24, [(1, 24), (2, 12), (4, 6)], (3, 8), (3, 7)),
                                 (36, [(1, 36), (2, 18), (3, 12), (6, 6)], (4, 9), (4, 8)),
                                 (30, [(1, 30), (2, 15), (5, 6)], (3, 10), (3, 9)),
                                 (48, [(1, 48), (2, 24), (3, 16), (6, 8)], (4, 12), (4, 11))]:
        assert sorted(shown + [miss]) == pairs(n) and near[0] * near[1] != n
        nm, he, his = P.next()
        rev = [(b, a) for a, b in shown if a != b]
        e = ("Test each number in order: 1, 2, 3, 4 … %d × %d = %d is missing. Turning a pair around (like %d × %d) "
             "is not a new pair." % (miss[0], miss[1], n, rev[-1][0], rev[-1][1]))
        q = ("%s lists the factor pairs of %d: %s. Which pair did %s miss?"
             % (nm, n, ", ".join("%d × %d" % p for p in shown), he))
        its.append(mcq(q, "%d × %d" % miss, ["%d × %d" % rev[-1], "%d × %d" % near, "%d × %d" % rev[-2]], e))
    assert len(its) == 20, len(its)
    return {"title": "Factor pairs and arrays", "items": its}


# ============================================================ set 2: all the factors
def set_factors(P):
    its = []
    for n in [16, 20, 28, 30, 32, 45]:
        fs = factors(n)
        a, b = pairs(n)[-1]
        stop = [x for x in fs if x not in (a, b)]
        mid = [x for x in fs if x not in (1, n)]
        mult = [n * k for k in range(1, 5)]
        q = "Which list shows <b>all</b> the factors of %d?" % n
        e = ("Factor pairs: %s. So the factors are <b>%s</b>. Remember 1 and %d, and keep testing until the pairs meet."
             % (pairs_txt(n), lst(fs), n))
        its.append(mcq(q, lst(fs), [lst(stop), lst(mid), lst(mult)], e))

    for n, bad, good in [(36, 8, [4, 9, 12]), (30, 4, [3, 5, 6]), (48, 9, [6, 8, 12]),
                         (45, 6, [3, 5, 9]), (60, 8, [4, 6, 12])]:
        assert all(n % g == 0 for g in good) and n % bad
        e = ("%s, so <b>%d</b> is not a factor of %d. The others divide evenly: %s."
             % (rem(n, bad), bad, n, ", ".join("%d × %d = %d" % (g, n // g, n) for g in good)))
        its.append(mcq("Which number is <b>not</b> a factor of %d?" % n, bad, good, e))

    for n in [24, 36, 18, 49, 50]:
        fs = factors(n)
        k = len(pairs(n))
        sq = pairs(n)[-1][0] == pairs(n)[-1][1]
        q = "How many factors does %d have?" % n
        e = ("The factors are %s. That is <b>%d</b> factors. Each pair gives 2 factors%s."
             % (lst(fs), len(fs), ", but %d × %d gives only one: %d" % (pairs(n)[-1] + (pairs(n)[-1][0],)) if sq else ""))
        its.append(mcq(q, len(fs), [k, len(fs) - 2, len(fs) + 1 if sq else len(fs) - 1], e))

    for a, b, kind in [(6, 7, "factor"), (8, 9, "multiple"), (5, 9, "multiple"), (4, 8, "factor")]:
        n = a * b
        if kind == "factor":
            right = "%d is a factor of %d" % (a, n)
            wrong = ["%d is a factor of %d" % (n, a), "%d is a multiple of %d" % (a, n), "%d is a multiple of %d" % (b, n)]
        else:
            right = "%d is a multiple of %d" % (n, b)
            wrong = ["%d is a multiple of %d" % (b, n), "%d is a factor of %d" % (n, b), "%d is a factor of %d" % (n, a)]
        e = ("%d and %d are factors of %d. %d is a multiple of %d and of %d. The bigger number, %d, is the multiple."
             % (a, b, n, n, a, b, n))
        its.append(mcq("%d × %d = %d. Which sentence is true?" % (a, b, n), right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Find all the factors", "items": its}


# ============================================================ set 3: multiples and divisibility
CLUE = {3: "Clue for 3: the digits add up to a multiple of 3.",
        4: "Clue for 4: the number is even, and half of it is still even.",
        6: "Clue for 6: the number is even <b>and</b> its digits add up to a multiple of 3.",
        7: "There is no quick clue for 7, so divide.",
        8: "Clue for 8: halve it three times. If you never get a remainder, it is a multiple of 8.",
        9: "Clue for 9: the digits add up to 9 or 18."}


def set_multiples(P):
    its = []
    for d in [6, 7, 8, 9]:
        m = [d * k for k in range(1, 6)]
        skip = [d * k for k in (1, 2, 3, 4, 6)]
        e = ("Multiples of %d are %d × 1, %d × 2, %d × 3 … Count by %ds: <b>%s</b>. "
             "%s is the list of factors of %d, not multiples." % (d, d, d, d, d, lst(m), lst(factors(d)), d))
        its.append(mcq("Which list shows the first 5 multiples of %d?" % d, lst(m),
                       [lst(factors(d)), lst([1] + m[:4]), lst(skip)], e))

    for d, right, wrong in [(3, 57, [43, 73, 52]), (4, 76, [54, 34, 42]), (6, 84, [64, 46, 63]),
                            (9, 72, [39, 29, 98]), (7, 91, [27, 57, 74]), (8, 96, [68, 84, 28])]:
        assert right % d == 0 and all(w % d for w in wrong)
        e = ("%d × %d = <b>%d</b>. The others leave a remainder: %s. %s"
             % (d, right // d, right, ", ".join(rem(w, d) for w in wrong), CLUE[d]))
        its.append(mcq("Which number is a multiple of %d?" % d, right, wrong, e))

    yn = [
        ("Is 87 a multiple of 3?", "Yes. 3 × 29 = 87", ["No. 87 is odd", "No. It does not end in 3", "No. 3 × 10 is only 30"],
         "8 + 7 = 15, and 15 is a multiple of 3, so 87 is too: 3 × 29 = 87. Odd numbers can be multiples of 3."),
        ("Is 75 a multiple of 5?", "Yes. 5 × 15 = 75", ["No. 75 is odd", "No. 7 + 5 = 12", "No. 5 × 10 is only 50"],
         "Numbers that end in 0 or 5 are multiples of 5. 5 × 15 = 75. Don’t stop at 5 × 10."),
        ("Is 92 a multiple of 6?", "No. 92 ÷ 6 = 15 R 2", ["Yes. 92 is even", "Yes. It ends in 2, like 12", "Yes. 6 × 16 = 92"],
         "A multiple of 6 is even <b>and</b> its digits add up to a multiple of 3. 9 + 2 = 11, so 92 is not. 6 × 15 = 90 and 6 × 16 = 96."),
        ("Is 81 a multiple of 9?", "Yes. 9 × 9 = 81", ["No. It does not end in 9", "No. 81 ÷ 9 has a remainder", "No. 81 is odd"],
         "8 + 1 = 9, so 81 is a multiple of 9: 9 × 9 = 81. Odd numbers can be multiples of 9."),
        ("Is 70 a multiple of 4?", "No. 70 ÷ 4 = 17 R 2", ["Yes. 70 is even", "Yes. It ends in 0, like 40", "Yes. 4 × 17 = 70"],
         "Half of 70 is 35, which is odd, so 70 is not a multiple of 4. 4 × 17 = 68 and 4 × 18 = 72."),
        ("Is 96 a multiple of 8?", "Yes. 8 × 12 = 96", ["No. It does not end in 8", "No. 8 × 10 is only 80", "No. 9 + 6 = 15"],
         "8 × 10 = 80 and 8 × 2 = 16. 80 + 16 = 96, so 8 × 12 = 96."),
    ]
    for q, right, wrong, e in yn:
        n, d = map(int, re.findall(r"\d+", q))
        assert (n % d == 0) == right.startswith("Yes")
        its.append(mcq(q, right, wrong, e))

    for d in [9, 7, 8, 6]:
        k = 100 // d
        e = ("%s, so %d × %d = <b>%d</b> is the biggest multiple of %d up to 100. There are <b>%d</b> multiples. "
             "Don’t stop at %d × 10 = %d." % (rem(100, d), d, k, d * k, d, k, d, d * 10))
        its.append(mcq("How many multiples of %d are there from 1 to 100?" % d, k, [10, k + 1, k - 1, k + 2], e))
    assert len(its) == 20, len(its)
    return {"title": "Multiples and divisibility clues", "items": its}


# ============================================================ set 4: prime or composite
def set_prime(P):
    its = []
    cls = [
        (1, "Neither: it has 1 factor", ["Prime: 1 × 1 = 1", "Prime: 1 is odd", "Composite: 1 × 1 = 1"],
         "A prime number has exactly 2 factors. 1 has only one factor (1), so it is <b>neither</b> prime nor composite."),
        (2, "Prime: only 1 and 2", ["Composite: it is even", "Neither: it is too small", "Composite: 1 × 2 = 2"],
         "2 has exactly 2 factors, 1 and 2, so it is <b>prime</b>. It is the only even prime number."),
        (9, "Composite: 3 × 3 = 9", ["Prime: it is odd", "Prime: only 1 × 9", "Neither: it is odd"],
         "9 has 3 factors: 1, 3 and 9. More than 2 factors means <b>composite</b>. Odd does not mean prime."),
        (31, "Prime: only 1 and 31", ["Composite: it is odd", "Composite: 3 × 11 = 31", "Neither: it ends in 1"],
         "31 is not a multiple of 2, 3, 5 or 7, so its only factors are 1 and 31. It is <b>prime</b>. (3 × 11 = 33.)"),
        (57, "Composite: 3 × 19 = 57", ["Prime: it is odd", "Prime: only 1 × 57", "Neither: it is odd"],
         "5 + 7 = 12, a multiple of 3, so 3 is a factor: 3 × 19 = 57. 57 is <b>composite</b>."),
    ]
    for n, right, wrong, e in cls:
        assert right.startswith("Prime") == is_prime(n) and right.startswith("Neither") == (n == 1)
        its.append(mcq("Is %d prime, composite or neither?" % n, right, wrong, e))

    def why(w):
        if w == 1:
            return "1 is neither prime nor composite"
        r = int(w ** 0.5)
        if r * r == w:
            return "%d = %d × %d" % (w, r, r)
        return "%d = %d × %d" % (w, factors(w)[1], w // factors(w)[1])

    for right, wrong in [(29, [27, 39, 1]), (2, [1, 9, 21]), (53, [51, 57, 91]), (89, [87, 81, 69])]:
        assert is_prime(right) and not any(is_prime(w) for w in wrong)
        e = ("<b>%d</b> has only 2 factors: 1 and %d. The others: %s.%s"
             % (right, right, "; ".join(why(w) for w in wrong),
                " 2 is the only even prime." if right == 2 else " Odd does not always mean prime."))
        its.append(mcq("Which number is prime?", right, wrong, e))

    for right, wrong in [(49, [47, 2, 1]), (87, [83, 89, 97]), (39, [37, 31, 2]), (93, [97, 1, 23])]:
        assert not is_prime(right) and right > 1 and not any(len(factors(w)) > 2 for w in wrong)
        e = ("%s, so <b>%d</b> has more than 2 factors: it is composite. %s"
             % (why(right), right, "The others are prime" + (", except 1, which is neither." if 1 in wrong else ".")))
        its.append(mcq("Which number is composite?", right, wrong, e))

    for lo, hi, wrong, word in [(1, 10, [5, 3, 6], "from 1 to 10"), (10, 20, [5, 3, 2], "between 10 and 20"),
                                (20, 30, [5, 3, 4], "between 20 and 30")]:
        ps = [x for x in range(lo, hi + 1) if is_prime(x) and (lo == 1 or lo < x < hi)]
        note = {1: "1 is not prime, and 2 is.", 10: "15 = 3 × 5 is not prime.",
                20: "21 = 3 × 7, 25 = 5 × 5 and 27 = 3 × 9 are odd but not prime."}[lo]
        e = "The primes are %s. That is <b>%d</b>. %s" % (lst(ps), len(ps), note)
        its.append(mcq("How many prime numbers are there %s?" % word, len(ps), wrong, e))

    claims = [
        ("says 51 is prime because it is odd", "No. 51 = 3 × 17", ["Yes. 51 is odd", "Yes. Only 1 × 51 = 51", "Yes. 51 ÷ 2 has a remainder"],
         "5 + 1 = 6, so 3 is a factor: 51 = 3 × 17. 51 is composite. Many odd numbers are composite."),
        ("says 91 is prime because 2, 3 and 5 are not factors", "No. 91 = 7 × 13",
         ["Yes. 91 is odd", "Yes. Only 1 × 91 = 91", "No. 91 = 9 × 11"],
         "Also try 7: 91 ÷ 7 = 13. So 91 = 7 × 13 is composite. (9 × 11 = 99.)"),
        ("says 1 is a prime number", "No. 1 has only 1 factor", ["Yes. Its only factor is 1", "Yes. 1 is odd", "No. 1 is composite"],
         "A prime number has exactly 2 factors. 1 has only one, so 1 is neither prime nor composite."),
        ("says 2 is composite because it is even", "No. 2 is prime", ["Yes. Even numbers are composite", "Yes. 2 is a factor of 2", "No. 2 is neither"],
         "2 has exactly 2 factors, 1 and 2, so it is prime. Every other even number has 2 as a factor, so 2 is the only even prime."),
    ]
    for c, right, wrong, e in claims:
        nm, he, his = P.next()
        its.append(mcq("%s %s. Is %s right?" % (nm, c, he), right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Prime or composite?", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    for n, thing, place, unit, good, bad in [
            (36, "chairs", "in rows. Each row gets", "rows", [4, 6, 9], 8),
            (48, "cupcakes", "on trays. Each tray gets", "trays", [6, 8, 12], 9),
            (40, "stickers", "in rows. Each row gets", "rows", [4, 5, 8], 6),
            (60, "photos", "in an album. Each page gets", "pages", [5, 12, 15], 8)]:
        assert all(n % g == 0 for g in good) and n % bad
        nm, he, his = P.next()
        q = ("%s puts %d %s %s the same number, with none left over. Which number of %s will <b>not</b> work?"
             % (nm, n, thing, place, unit))
        e = ("%s, so %d %s leave some %s left over. The others are factors of %d: %s."
             % (rem(n, bad), bad, unit, thing, n, ", ".join("%d × %d = %d" % (g, n // g, n) for g in good)))
        its.append(mcq(q, "%d %s" % (bad, unit), ["%d %s" % (g, unit) for g in good], e))

    for n, thing in [(24, "desks"), (18, "chairs"), (20, "plants")]:
        nm, he, his = P.next()
        fs = factors(n)
        k = len(pairs(n))
        q = ("%s sets out %d %s in rows. Each row has the same number of %s, and one long row is allowed. "
             "How many different numbers of rows can %s use?" % (nm, n, thing, thing, he))
        e = ("The number of rows must be a factor of %d: %s. That is <b>%d</b> choices. Count both numbers in each pair: "
             "2 rows of %d is different from %d rows of 2." % (n, lst(fs), len(fs), n // 2, n // 2))
        its.append(mcq(q, len(fs), [k, len(fs) - 2, len(fs) - 1], e))

    nm, he, his = P.next()
    its.append(mcq("Pencils come in packs of 8. %s buys some packs. Which number of pencils could %s have?" % (nm, he),
                   "56 pencils", ["58 pencils", "52 pencils", "60 pencils"],
                   "%s can only have a multiple of 8: 8 × 7 = <b>56</b>. 58 ends in 8, but 8 × 7 = 56 and 8 × 8 = 64." % cap(he)))
    nm, he, his = P.next()
    its.append(mcq("Juice boxes come in packs of 6. Can %s buy exactly 40 juice boxes?" % nm,
                   "No. 40 is not a multiple of 6", ["Yes. 40 is even", "Yes. 40 ends in 0", "Yes. 6 × 7 = 40"],
                   "6 × 6 = 36 and 6 × 7 = 42. 40 is between them, so it is <b>not</b> a multiple of 6. Being even is not enough."))
    nm, he, his = P.next()
    its.append(mcq("Tennis balls come in cans of 3. %s needs exactly 51 balls. Can %s buy exactly 51?" % (nm, he),
                   "Yes. 3 × 17 = 51", ["No. 51 is odd", "No. 51 doesn’t end in 3", "No. 3 × 10 is only 30"],
                   "5 + 1 = 6, a multiple of 3, so 51 is a multiple of 3. 3 × 17 = 51, so %s buys <b>17 cans</b>." % he))
    nm, he, his = P.next()
    its.append(mcq("Stickers come in sheets of 9. %s buys some sheets. How many stickers could %s have?" % (nm, he),
                   "63 stickers", ["69 stickers", "49 stickers", "96 stickers"],
                   "9 × 7 = <b>63</b>, and 6 + 3 = 9. The digits of 69, 49 and 96 add up to 15, 13 and 15, so they are not multiples of 9. Ending in 9 is not the clue."))
    nm, he, his = P.next()
    its.append(mcq("Cups come in packs of 6 and plates in packs of 8. %s wants the same number of cups and plates. "
                   "What is the smallest number of each %s can buy?" % (nm, he),
                   "24 of each", ["48 of each", "14 of each", "12 of each"],
                   "Multiples of 6: 6, 12, 18, <b>24</b>. Multiples of 8: 8, 16, <b>24</b>. 24 is the first number in both lists. "
                   "6 × 8 = 48 works too, but it is not the smallest."))
    nm, he, his = P.next()
    its.append(mcq("Hot dogs come in packs of 10 and buns in packs of 8. %s wants the same number of hot dogs and buns. "
                   "What is the smallest number of each %s can buy?" % (nm, he),
                   "40 of each", ["80 of each", "18 of each", "20 of each"],
                   "Multiples of 10: 10, 20, 30, <b>40</b>. Multiples of 8: 8, 16, 24, 32, <b>40</b>. 40 is the first number in both lists. "
                   "20 is a multiple of 10 but not of 8."))

    puzzles = [
        ("I am between 20 and 30. I am a multiple of 4 and a multiple of 6. What number am I?", 24, [28, 30, 26],
         "Multiples of 4 between 20 and 30: 24, 28. Multiples of 6 between 20 and 30: 24. Only <b>24</b> is both. 30 is a multiple of 6, but not of 4.",
         lambda x: 20 < x < 30 and x % 4 == 0 and x % 6 == 0),
        ("I am a prime number between 30 and 40. My digits add up to 10. What number am I?", 37, [31, 19, 28],
         "The primes between 30 and 40 are 31 and 37. 3 + 7 = 10, so the number is <b>37</b>. 31 has digits that add up to 4.",
         lambda x: 30 < x < 40 and is_prime(x) and sum(map(int, str(x))) == 10),
        ("I am an odd two-digit number less than 40. 9 is a factor of me. What number am I?", 27, [18, 36, 39],
         "Two-digit multiples of 9 less than 40: 18, 27, 36. Only <b>27</b> is odd. 39 ends in 9, but 39 ÷ 9 = 4 R 3.",
         lambda x: 9 < x < 40 and x % 2 and x % 9 == 0),
        ("I am less than 40. 2, 3 and 5 are all factors of me. What number am I?", 30, [15, 10, 6],
         "2 × 3 × 5 = <b>30</b>. 15 is odd, so 2 is not a factor. 10 does not have 3 as a factor, and 6 does not have 5.",
         lambda x: x < 40 and x % 30 == 0),
        ("I am an odd composite number between 50 and 60. 3 is not one of my factors. What number am I?", 55, [51, 57, 53],
         "The odd numbers between 50 and 60 are 51, 53, 55, 57, 59. 51 = 3 × 17 and 57 = 3 × 19 have 3 as a factor. "
         "53 and 59 are prime. <b>55</b> = 5 × 11.",
         lambda x: 50 < x < 60 and x % 2 and not is_prime(x) and x % 3),
    ]
    for q, right, wrong, e, ok in puzzles:
        assert [x for x in range(1, 101) if ok(x)] == [right] and not any(ok(w) for w in wrong), q
        its.append(mcq(q, right, wrong, e))

    nm, he, his = P.next()
    its.append(mcq("%s has 17 square tiles. Can %s make a rectangle with all 17 tiles and more than one row?" % (nm, he),
                   "No. 17 is prime", ["Yes. 3 rows of 6", "Yes. 2 rows of 9", "Yes. 17 is odd"],
                   "17 has only 2 factors, 1 and 17, so the only rectangle is 1 row of 17. 3 × 6 = 18 and 2 × 9 = 18, not 17."))
    its.append(mcq(fig(dots_svg(2, 6)) + "This egg carton holds 12 eggs in 2 rows of 6. Which other carton could hold exactly 12 eggs "
                   "in equal rows?", "3 rows of 4", ["3 rows of 5", "4 rows of 4", "5 rows of 2"],
                   "3 × 4 = 12, so 3 rows of 4 hold exactly 12 eggs. 3 × 5 = 15, 4 × 4 = 16 and 5 × 2 = 10."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with factors and multiples", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Factors are the numbers you multiply</h2>"
        "<p>In 3 × 4 = 12, 3 and 4 are <b>factors</b> of 12. They are a <b>factor pair</b>. "
        "Every factor pair makes a rectangle of tiles. 12 tiles make 3 different rectangles, so 12 has 3 factor pairs.</p>"
        "<figure class='sn-fig'>" + rects_svg(12) +
        "<figcaption>All the rectangles for 12: 1 × 12, 2 × 6 and 3 × 4. The factors of 12 are 1, 2, 3, 4, 6 and 12.</figcaption></figure>"
        "<h2>Find every factor pair</h2>"
        "<p>Test 1, 2, 3, 4 … in order. Stop when the pairs meet or turn around.</p>"
        "<figure class='sn-fig'>" + rainbow_svg(24) +
        "<figcaption>Factors of 24: 1 × 24, 2 × 12, 3 × 8, 4 × 6. Next would be 6 × 4, a pair you already have, so stop.</figcaption></figure>"
        + ex("Example", "Find all the factors of 36.",
             "1 × 36, 2 × 18, 3 × 12, 4 × 9, 6 × 6. 5 is not a factor (36 ÷ 5 = 7 R 1). 6 × 6 is the middle, so stop and write 6 once.",
             "1, 2, 3, 4, 6, 9, 12, 18, 36")
        + "<h2>Multiples: count by the number</h2>"
        "<p>The <b>multiples</b> of 6 are 6, 12, 18, 24, 30 … A number is a multiple of each of its factors: "
        "6 × 7 = 42, so 42 is a multiple of 6 and of 7. These clues tell you fast:</p>"
        + table(["Multiple of", "Clue", "Example"], [
            ["2", "Ends in 0, 2, 4, 6 or 8", "58"],
            ["3", "Digits add up to a multiple of 3", "87: 8 + 7 = 15"],
            ["5", "Ends in 0 or 5", "75"],
            ["6", "Even <b>and</b> digits add up to a multiple of 3", "72: 7 + 2 = 9"],
            ["9", "Digits add up to 9 or 18", "81: 8 + 1 = 9"],
            ["10", "Ends in 0", "90"],
        ]) +
        "<h2>Prime or composite</h2>"
        "<p>A <b>prime</b> number has exactly 2 factors: 1 and itself. A <b>composite</b> number has more than 2. "
        "1 is <b>neither</b>. To test a number up to 100, try 2, 3, 5 and 7.</p>"
        "<figure class='sn-fig'>" + rects_svg(7) +
        "<figcaption>7 tiles make only one rectangle, 1 × 7. 7 is prime.</figcaption></figure>"
        + ex("Example", "Is 91 prime or composite?", "91 is odd, and 2, 3 and 5 are not factors. Try 7: 91 ÷ 7 = 13.",
             "Composite, because 91 = 7 × 13")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Missing a pair: factors of 24 are 1, 2, 12, 24", "Test every number in order until the pairs meet: 3 × 8, 4 × 6"],
            ["Mixing up factor and multiple: “42 is a factor of 6”", "The factor is the smaller number. 6 is a factor of 42; 42 is a multiple of 6"],
            ["Calling 1 prime", "1 has only one factor, so it is neither prime nor composite"],
            ["Thinking every odd number is prime (9, 51, 91)", "Check 3 and 7: 9 = 3 × 3, 51 = 3 × 17, 91 = 7 × 13"],
            ["Thinking 2 is composite because it is even", "2 has only 1 and 2 as factors. It is the only even prime"],
            ["Stopping at × 10: “84 is not a multiple of 6”", "Keep going past 10: 6 × 14 = 84"],
        ])
    )


FAQ = [
    {"q": "How do you find all the factor pairs of a number?",
     "a": "Test 1, 2, 3, 4 … in order and write each pair, like 1 × 24, 2 × 12, 3 × 8, 4 × 6. Stop when the next pair would repeat one you have (6 × 4), so you know you found them all."},
    {"q": "What is the difference between a factor and a multiple?",
     "a": "Factors are the numbers you multiply; the multiple is the answer. In 6 × 7 = 42, 6 and 7 are factors of 42, and 42 is a multiple of 6 and of 7."},
    {"q": "Is 1 a prime number?",
     "a": "No. A prime number has exactly two factors, 1 and itself. 1 has only one factor, so it is neither prime nor composite. 2 is the smallest prime and the only even one."},
    {"q": "How can a 4th grader tell if a number is prime?",
     "a": "For a number up to 100, try dividing by 2, 3, 5 and 7. If none of them divides evenly, the number is prime. 91 looks prime, but 91 = 7 × 13, so it is composite."},
]


def gen():
    rnd = random.Random(110)
    P = People(rnd)
    sets = [set_pairs(P), set_factors(P), set_multiples(P), set_prime(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "factors-multiples-prime", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Factors, Multiples, Prime and Composite Numbers",
        "seo_title": "Grade 4 Factors and Multiples Worksheets: Factor Pairs, Divisibility Rules, Prime and Composite Numbers",
        "short_title": "Factors, multiples and primes",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "4.OA.B.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/OA/B/4/",
        "standard_text": "Find all factor pairs for a whole number in the range 1–100. Recognize that a whole number is a multiple of each of its factors. Determine whether a given whole number in the range 1–100 is a multiple of a given one-digit number. Determine whether a given whole number in the range 1–100 is prime or composite.",
        "meta_desc": "Free Grade 4 factors and multiples worksheets: find factor pairs with arrays, list all factors, use divisibility clues for 2, 3, 5, 6 and 9, tell prime from composite numbers, and solve word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Factors multiply to make a number. Multiples are what you get when you count by it.",
        "key_sub": "3 × 8 = 24: 3 and 8 are factors of 24, and 24 is a multiple of 3 and 8. A prime number has exactly 2 factors. 1 is neither prime nor composite, and 2 is the only even prime.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
