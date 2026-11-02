# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Factors, primes and divisibility (Ontario Mathematics Curriculum 2020, Grade 6: Number, B2)
  python3 tools/gen_ca_math_g6_factors.py
Divisibility rules for 2, 3, 4, 5, 6, 8, 9 and 10, factors and multiples, prime and composite numbers
(1 is neither), prime factorization with factor trees, and word problems (arranging chairs, packaging).
Every rule, factor, prime and product is checked in code.
Wrong answers come from real student mistakes: 1 is prime (or composite), 9 / 51 / 57 / 91 are prime,
2 is not prime, the digit-sum rule used for 4, “ends in 9” for 9, “ends in 3” for 3, the last two digits
used for 8, only checking “even” for 6, confusing factors and multiples, stopping a factor tree at a
composite number, writing 1 in a prime factorization, and adding the prime factors instead of multiplying.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, os, random, re
from math import prod

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ math
def n(x):
    """Ontario style: 4 digits with no separator, 5 or more digits grouped with a no-break space."""
    x = int(x)
    return str(x) if abs(x) < 10000 else "{:,}".format(x).replace(",", NBSP)


def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def pairs(x):
    return [(d, x // d) for d in factors(x) if d * d <= x]


def is_prime(x):
    return len(factors(x)) == 2


def primes_of(x):
    out, d = [], 2
    while x > 1:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    return out


def lst(xs):
    return ", ".join(n(x) for x in xs)


def times(xs):
    return " × ".join(str(x) for x in xs)


def dsum(x):
    return sum(int(c) for c in str(x))


def dsum_s(x):
    return "%s = %d" % (" + ".join(str(x)), dsum(x))


def why_not_prime(x):
    if x == 1:
        return "1 has only one factor, so it is not prime"
    s = pairs(x)[1]
    return "%d = %d × %d, so %d is not prime" % (x, s[0], s[1], x)


def rule(x, d):
    """Short reason, using the divisibility rule, why x is or is not divisible by d. Checked in code."""
    ok = x % d == 0
    s = n(x)
    yes = "is" if ok else "is not"
    if d == 2:
        r = "%s ends in %d, %s digit, so it %s divisible by 2" % (s, x % 10, "an even" if x % 2 == 0 else "an odd", yes)
    elif d == 5:
        r = "%s ends in %d, so it %s divisible by 5" % (s, x % 10, yes)
    elif d == 10:
        r = "%s ends in %d, so it %s divisible by 10" % (s, x % 10, yes)
    elif d in (3, 9):
        r = "%s: %s, and %d %s divisible by %d, so it %s divisible by %d" % (
            s, dsum_s(x), dsum(x), "is" if dsum(x) % d == 0 else "is not", d, yes, d)
        assert (dsum(x) % d == 0) == ok
    elif d == 4:
        t = x % 100
        assert t >= 10
        r = "%s: the last two digits make %d, and %d ÷ 4 %s, so it %s divisible by 4" % (
            s, t, t, "= %d" % (t // 4) if t % 4 == 0 else "has a remainder", yes)
        assert (t % 4 == 0) == ok
    elif d == 8:
        t = x % 1000
        assert t >= 100
        r = "%s: the last three digits make %d, and %d ÷ 8 %s, so it %s divisible by 8" % (
            s, t, t, "= %d" % (t // 8) if t % 8 == 0 else "has a remainder", yes)
        assert (t % 8 == 0) == ok
    elif d == 6:
        e2, e3 = x % 2 == 0, dsum(x) % 3 == 0
        r = "%s is %s and its digits add to %d (%s by 3), so it %s divisible by 6" % (
            s, "even" if e2 else "odd", dsum(x), "divisible" if e3 else "not divisible", yes)
        assert (e2 and e3) == ok
    else:
        raise ValueError(d)
    return r


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


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
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
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


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so every number stays readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def T(v, a=None, b=None):
    """Tree node: v splits into a and b (themselves nodes or ints)."""
    if a is None:
        return (v, None)
    a = a if isinstance(a, tuple) else (a, None)
    b = b if isinstance(b, tuple) else (b, None)
    assert a[0] * b[0] == v, (v, a[0], b[0])
    return (v, [a, b])


def split(x):
    """Most balanced factor pair of x (both > 1), or None if x is prime."""
    best = None
    for a in range(2, int(x ** 0.5) + 1):
        if x % a == 0:
            best = (a, x // a)
    return best


def auto_tree(x):
    s = split(x)
    return T(x) if s is None else T(x, auto_tree(s[0]), auto_tree(s[1]))


def leaves(t):
    return [t[0]] if t[1] is None else leaves(t[1][0]) + leaves(t[1][1])


def depth(t):
    return 1 if t[1] is None else 1 + max(depth(c) for c in t[1])


def tree_svg(t, hide=None, step=46, dy=50):
    """Factor tree: each number splits into a factor pair; the primes at the ends are circled.
    'hide' is a value shown as ? in a red box (the first node with that value)."""
    assert prod(leaves(t)) == t[0]
    assert all(is_prime(v) for v in leaves(t))
    o = 22
    W = (len(leaves(t)) - 1) * step + 2 * o
    H = (depth(t) - 1) * dy + 2 * o
    pos = {}
    s = []
    cnt = [0]

    def place(node, lvl):
        if node[1] is None:
            px = o + cnt[0] * step
            cnt[0] += 1
        else:
            xs = [place(c, lvl + 1) for c in node[1]]
            px = sum(xs) / 2
        pos[id(node)] = (px, o + lvl * dy)
        return px

    place(t, 0)
    hidden = [0]

    def draw(node):
        px, py = pos[id(node)]
        if node[1] is not None:
            for c in node[1]:
                cx, cy = pos[id(c)]
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                         % (px, py + 9, cx, cy - 15, GREY))
                draw(c)
        if node[0] == hide and not hidden[0]:
            hidden[0] = 1
            s.append("<rect x='%.1f' y='%.1f' width='30' height='28' rx='4' fill='#fff' stroke='%s' stroke-width='2'/>"
                     % (px - 15, py - 14, RED))
            s.append(text(px, py + 6, "?", 18, col=RED))
            return
        if node[1] is None:
            s.append("<circle cx='%.1f' cy='%.1f' r='15' fill='%s' stroke='%s' stroke-width='2'/>" % (px, py, FILL, GREEN))
        s.append(text(px, py + 6, str(node[0]), 17))

    draw(t)
    if hide is not None:
        assert hidden[0]
    lab = "factor tree for %s" % ("a number" if hide == t[0] else t[0]) + (" with one number missing" if hide else "")
    return svg_wrap(W, H, "".join(s), lab)


def rainbow_svg(x, step=40):
    """Lesson: the factors of x in a row, each factor pair joined by an arc."""
    fs = factors(x)
    o, top = 20, 76
    W = (len(fs) - 1) * step + 2 * o
    xs = {f: o + i * step for i, f in enumerate(fs)}
    s = []
    ps = pairs(x)
    for k, (a, b) in enumerate(ps):
        if a == b:
            continue
        ry = 16 + 14 * (len(ps) - 1 - k)
        s.append("<path d='M %d %d A %d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xs[a], top, (xs[b] - xs[a]) // 2, ry, xs[b], top, GREEN))
    for f in fs:
        s.append(text(xs[f], top + 22, str(f), 18))
    return svg_wrap(W, top + 30, "".join(s), "factor rainbow for %d" % x)


def chairs_svg(rows, cols, cell=18):
    """Chairs (small squares) set out in equal rows, with the size written underneath."""
    o = 6
    W = max(cols * cell + 2 * o, 80)
    H = rows * cell + 2 * o + 24
    x0 = (W - cols * cell) / 2
    s = ["<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
         % (x0 + j * cell + 3, o + i * cell + 3, cell - 6, cell - 6, FILL, GREEN)
         for i in range(rows) for j in range(cols)]
    s.append(text(W / 2, H - 6, "%d rows of %d" % (rows, cols), 15))
    return s, W, H


def chairs_row_svg(sizes, gap=28):
    """Lesson: 24 chairs in different equal-row arrangements, side by side."""
    parts, x, H = [], 0, 0
    built = [chairs_svg(r, c) for r, c in sizes]
    H = max(h for _, _, h in built)
    for p, w, h in built:
        parts.append("<g transform='translate(%d %d)'>%s</g>" % (x, H - h, "".join(p)))
        x += w + gap
    W = x - gap
    return svg_wrap(W, H, "".join(parts), "24 chairs as %s" % ", ".join("%d rows of %d" % rc for rc in sizes))


# ============================================================ set 1: divisibility rules
def which_div(d, right, wrong, extra="", q=None):
    assert right % d == 0 and all(w % d for w in wrong), (d, right, wrong)
    e = cap(rule(right, d)) + ". " + " ".join(cap(rule(w, d)) + "." for w in wrong)
    e = e.replace("so it is divisible", "so it <b>is</b> divisible", 1)
    return mcq(q or "Which number is divisible by %d?" % d, n(right), [n(w) for w in wrong], e + extra)


def set_divisibility(P):
    its = []
    its.append(which_div(2, 3458, [2483, 4865, 6047],
                         " Only the ones digit matters, not the other digits."))
    its.append(which_div(5, 7465, [5472, 3051, 4558],
                         " A 5 at the start or in the middle does not count."))
    its.append(which_div(10, 6390, [6305, 1009, 4501]))
    its.append(which_div(3, 4521, [413, 2723, 5833],
                         " Ending in 3 does not make a number divisible by 3. Add the digits."))
    its.append(which_div(9, 7254, [3719, 4596, 9142],
                         " 4596 is divisible by 3 (24), but not by 9. Ending in 9 or starting with 9 does not matter."))
    its.append(which_div(4, 5316, [1030, 2618, 3422],
                         " Do not add the digits for 4: 1 + 0 + 3 + 0 = 4, but 1030 is not divisible by 4. "
                         "Being even is not enough either."))
    its.append(which_div(6, 4362, [4365, 2654, 1636],
                         " A number divisible by 6 must pass <b>both</b> tests: even, and digits adding to a multiple of 3."))
    its.append(which_div(8, 7128, [3148, 5612, 6324],
                         " For 8, use the last <b>three</b> digits. 48 is divisible by 8, but 148 is not."))

    for d, right, wrong in [(3, 2581, [1752, 3201, 4419]), (4, 7354, [3128, 6540, 2916])]:
        assert right % d and all(w % d == 0 for w in wrong)
        e = cap(rule(right, d)) + ". " + " ".join(cap(rule(w, d)) + "." for w in wrong)
        its.append(mcq("Which number is <b>not</b> divisible by %d?" % d, n(right), [n(w) for w in wrong], e))

    assert 5832 % 9 == 0
    its.append(mcq("Is 5832 divisible by 9?", "Yes. The digits add to 18",
                   ["No. It does not end in 9", "No. 5832 is even", "No. The digits add to 17"],
                   "5 + 8 + 3 + 2 = 18, and 18 is divisible by 9, so <b>yes</b>: 5832 ÷ 9 = 648. "
                   "The last digit does not matter for 9, and even numbers can be divisible by 9."))

    nm, he, his = P.next()
    assert 1210 % 4 and dsum(1210) == 4
    its.append(mcq("%s says 1210 is divisible by 4 because 1 + 2 + 1 + 0 = 4. Is %s right?" % (nm, he),
                   "No. Check the last two digits", ["Yes. The digits add to 4", "Yes. 1210 is even",
                                                     "No. It must end in 4"],
                   "Adding the digits works for 3 and 9, <b>not</b> for 4. The last two digits make 10, and "
                   "10 ÷ 4 has a remainder, so 1210 is not divisible by 4. But 1216 is divisible by 4, because 16 ÷ 4 = 4."))
    assert 1216 % 4 == 0

    ok = [d for d in range(10) if (520 + d) % 9 == 0]
    assert ok == [2] and (525) % 3 == 0 and 525 % 9
    its.append(mcq("Which digit can go in the blank to make 52_ divisible by 9?", 2, [9, 5, 0],
                   "5 + 2 = 7. The digit sum must be 9, so the missing digit is <b>2</b>: 522 ÷ 9 = 58. "
                   "529 ends in 9 but 5 + 2 + 9 = 16. 525 adds to 12, which works for 3 but not 9."))

    good, bad = 8730, [8735, 8752, 5728]
    assert good % 10 == 0 and all(b % 2 or b % 5 for b in bad)
    its.append(mcq("Which number is divisible by both 2 and 5?", n(good), [n(b) for b in bad],
                   "A number divisible by 2 and 5 is divisible by 10, so it ends in 0: <b>8730</b>. "
                   "8735 is odd, and 8752 and 5728 do not end in 0 or 5."))

    good, bad = 2412, [1240, 3615, 2654]
    assert good % 6 == 0 and good % 4 == 0 and all(b % 6 for b in bad) and good % 5
    good, bad = 4320, [1240, 3615, 2412]
    assert good % 30 == 0 and all(b % 30 for b in bad)
    its.append(mcq("Which number is divisible by 2, by 3 and by 5?", n(good), [n(b) for b in bad],
                   "4320 ends in 0 (so it is divisible by 2 and 5), and 4 + 3 + 2 + 0 = 9 (divisible by 3). "
                   "So the answer is <b>4320</b>. 1240 adds to 7, 3615 is odd, and 2412 does not end in 0 or 5."))

    x = 1236
    divs = {d: x % d == 0 for d in (4, 9, 5, 8)}
    assert divs == {4: True, 9: False, 5: False, 8: False}
    its.append(mcq("1236 is divisible by which of these numbers?", 4, [9, 5, 8],
                   cap(rule(x, 4)) + ". " + cap(rule(x, 9)).replace("1236: ", "") + ". It ends in 6, so not 5. "
                   + cap(rule(x, 8).replace("1236: ", "")) + "."))

    its.append(mcq("A number is divisible by 6 when it is…", "divisible by 2 and by 3",
                   ["even", "a number ending in 6", "divisible by 2 or by 3"],
                   "6 = 2 × 3, so the number must pass <b>both</b> tests. 16 is even and ends in 6, "
                   "but 16 is not divisible by 6. 9 is divisible by 3, but not by 6."))

    nm, he, his = P.next()
    assert 29 % 9 and all(v % 9 == 0 for v in (99, 189, 909))
    its.append(mcq("%s says every number ending in 9 is divisible by 9. Which number shows %s is wrong?" % (nm, he),
                   29, [99, 189, 909],
                   "2 + 9 = 11, and 11 is not divisible by 9, so <b>29</b> is not divisible by 9. "
                   "99 (18), 189 (18) and 909 (18) are all divisible by 9. Use the digit sum, not the last digit."))

    x = 4536
    assert x % 9 == 0 and x % 5 and x % 10 and x % 3 == 0
    its.append(mcq("Which statement about 4536 is true?", "It is divisible by 9",
                   ["It is divisible by 5", "It is divisible by 10", "It is not divisible by 3"],
                   "4 + 5 + 3 + 6 = 18, so 4536 is divisible by 9 (and by 3). It ends in 6, not 0 or 5, "
                   "so it is not divisible by 5 or 10."))

    its.append(which_div(8, 15216, [15124, 16132, 18418],
                         " For 15" + NBSP + "124, 24 is divisible by 8, but you must test the last three digits, 124.",
                         q="Which 5-digit number is divisible by 8?"))
    assert len(its) == 20, len(its)
    return {"title": "Divisibility rules", "items": its}


# ============================================================ set 2: factors and multiples
def set_factors(P):
    its = []
    for x, drop in [(18, (3, 6)), (28, (4, 7)), (36, (4, 9)), (40, (5, 8))]:
        fs = factors(x)
        right = lst(fs)
        missing = lst([d for d in fs if d not in drop])
        multi = lst([x * k for k in range(1, 5)])
        no_ends = lst(fs[1:-1])
        e = ("Find the factor pairs: %s. So the factors are <b>%s</b>. Do not forget 1 and %d, and do not miss %d × %d. "
             "%s are multiples of %d, not factors."
             % (", ".join("%d × %d" % p for p in pairs(x)), right, x, drop[0], drop[1], multi, x))
        its.append(mcq("Which list shows <b>all</b> the factors of %d?" % x, right, [missing, no_ends, multi], e))

    for x, bad, good in [(48, 18, [12, 16, 6]), (60, 8, [12, 15, 20]), (72, 16, [8, 12, 24]), (90, 20, [15, 18, 30])]:
        assert x % bad and all(x % g == 0 for g in good)
        e = ("%d ÷ %d = %d with a remainder of %d, so <b>%d</b> is not a factor of %d. %s"
             % (x, bad, x // bad, x % bad, bad, x,
                " ".join("%d × %d = %d." % (g, x // g, x) for g in good)))
        its.append(mcq("Which number is <b>not</b> a factor of %d?" % x, bad, good, e))

    for x, good, bad in [(84, 14, [16, 168, 24]), (96, 32, [36, 192, 28])]:
        assert x % good == 0 and all(x % b for b in bad) and bad[1] == 2 * x
        e = ("%d × %d = %d, so <b>%d</b> is a factor of %d. %d is a multiple of %d, not a factor, and %d and %d "
             "leave a remainder." % (good, x // good, x, good, x, bad[1], x, bad[0], bad[2]))
        its.append(mcq("Which number is a factor of %d?" % x, good, bad, e))

    assert len(pairs(36)) == 5 and len(factors(36)) == 9
    its.append(mcq("How many factor pairs does 36 have?", 5, [4, 9, 6],
                   "1 × 36, 2 × 18, 3 × 12, 4 × 9 and 6 × 6. That is <b>5</b> factor pairs. 6 × 6 counts as a pair, "
                   "and 9 is the number of factors, not pairs."))

    nm, he, his = P.next()
    shown = [(1, 72), (2, 36), (3, 24), (6, 12), (8, 9)]
    assert sorted(shown + [(4, 18)]) == pairs(72)
    its.append(mcq("%s lists the factor pairs of 72: %s. Which pair did %s miss?"
                   % (nm, ", ".join("%d × %d" % p for p in shown), he), "4 × 18", ["9 × 8", "7 × 10", "5 × 14"],
                   "Test 1, 2, 3, 4 … in order. 72 ÷ 4 = 18, so <b>4 × 18</b> is missing. 9 × 8 is the same pair as 8 × 9, "
                   "and 7 × 10 and 5 × 14 both make 70, not 72."))

    for v, right, wrong in [(7, 63, [27, 17, 57]), (8, 96, [58, 18, 84]), (9, 108, [109, 98, 119])]:
        assert right % v == 0 and all(w % v for w in wrong)
        e = "%d × %d = %d, so <b>%d</b> is a multiple of %d. %s" % (
            v, right // v, right, right, v,
            " ".join("%d ÷ %d = %d R%d." % (w, v, w // v, w % v) for w in wrong))
        if v == 7:
            e += " Having a 7 as a digit does not make a number a multiple of 7."
        if v == 8:
            e += " 84 is a multiple of 4 and of 12, but not of 8."
        its.append(mcq("Which number is a multiple of %d?" % v, right, wrong, e))

    assert 63 % 6 and all(x % 6 == 0 for x in (42, 54, 72))
    its.append(mcq("Which number is <b>not</b> a multiple of 6?", 63, [42, 54, 72],
                   "Multiples of 6 are even. 63 is odd, so <b>63</b> is not a multiple of 6 (it is a multiple of 3, 7 and 9). "
                   "6 × 7 = 42, 6 × 9 = 54 and 6 × 12 = 72."))

    assert 7 * 12 == 84
    its.append(mcq("What is the 12th multiple of 7?", 84, [77, 91, 19],
                   "The 12th multiple of 7 is 7 × 12 = <b>84</b>. 77 is the 11th multiple, 91 is the 13th, and 19 is 7 + 12."))

    its.append(mcq("Which list shows the first five multiples of 6?", "6, 12, 18, 24, 30",
                   ["1, 2, 3, 6", "12, 18, 24, 30, 36", "6, 16, 26, 36, 46"],
                   "The multiples of 6 are 6 × 1, 6 × 2, 6 × 3 …: <b>6, 12, 18, 24, 30</b>. The first multiple is 6 itself. "
                   "1, 2, 3, 6 are the factors of 6."))

    nm, he, his = P.next()
    its.append(mcq("%s says 4 is a multiple of 12. Is %s right?" % (nm, he), "No. 4 is a factor of 12",
                   ["Yes. 4 × 3 = 12", "Yes. 12 ÷ 4 = 3", "No. 4 is a prime number"],
                   "4 × 3 = 12, so 4 is a <b>factor</b> of 12 and 12 is a multiple of 4. A factor divides the number; "
                   "a multiple is the number times 1, 2, 3 … 4 is not prime: 4 = 2 × 2."))

    assert 36 % 8
    its.append(mcq("Which statement is true?", "36 is a multiple of 9",
                   ["9 is a multiple of 36", "36 is a factor of 9", "8 is a factor of 36"],
                   "9 × 4 = 36, so <b>36 is a multiple of 9</b> (and 9 is a factor of 36). 36 ÷ 8 = 4 R4, "
                   "so 8 is not a factor of 36."))
    assert len(its) == 20, len(its)
    return {"title": "Factors and multiples", "items": its}


# ============================================================ set 3: prime and composite numbers
def set_primes(P):
    its = []
    for right, wrong in [(23, [21, 27, 1]), (37, [39, 57, 33]), (53, [51, 49, 9]), (41, [91, 87, 81])]:
        assert is_prime(right) and not any(is_prime(w) for w in wrong)
        e = ("%d has exactly two factors, 1 and %d, so <b>%d</b> is prime. " % (right, right, right)
             + ". ".join(cap(why_not_prime(w)) for w in wrong) + ".")
        its.append(mcq("Which of these is a prime number?", right, wrong, e))

    for right, wrong in [(1, [2, 3, 5]), (51, [2, 53, 47]), (91, [89, 97, 31])]:
        assert not is_prime(right) and all(is_prime(w) for w in wrong)
        e = cap(why_not_prime(right)).replace(str(right) + " is not", "<b>%d</b> is not" % right, 1) + ". "
        e += "%s and %d are prime: each has exactly two factors." % (", ".join(str(w) for w in wrong[:-1]), wrong[-1])
        if 2 in wrong:
            e += " 2 is prime, even though it is even."
        its.append(mcq("Which number is <b>not</b> a prime number?", right, wrong, e))

    comp = lambda v: len(factors(v)) > 2
    for right, wrong in [(9, [1, 2, 7]), (51, [1, 53, 47]), (87, [89, 1, 83])]:
        assert comp(right) and not any(comp(w) for w in wrong)
        s = pairs(right)[1]
        e = ("%d = %d × %d, so %d has more than two factors: <b>%d</b> is composite. " % (right, s[0], s[1], right, right)
             + "1 is not composite (it has only one factor). "
             + " and ".join(str(w) for w in wrong if w != 1) + " are prime.")
        its.append(mcq("Which of these is a composite number?", right, wrong, e))

    its.append(mcq("Which statement about the number 1 is true?", "It is neither prime nor composite",
                   ["It is a prime number", "It is a composite number", "It is both prime and composite"],
                   "A prime has exactly two factors and a composite number has more than two. 1 has only <b>one</b> "
                   "factor, so it is <b>neither</b>."))

    nm, he, his = P.next()
    its.append(mcq("%s says 2 is not a prime number because it is even. Is %s right?" % (nm, he),
                   "No. 2 has exactly two factors",
                   ["Yes. All primes are odd", "Yes. 2 has only one factor", "No. 2 is composite"],
                   "The factors of 2 are 1 and 2, so <b>2 is prime</b>. It is the only even prime: every other even "
                   "number can be divided by 2, so it is composite."))

    nm, he, his = P.next()
    its.append(mcq("%s says 9 is a prime number because it is odd. Is %s right?" % (nm, he),
                   "No. 9 = 3 × 3",
                   ["Yes. Odd numbers are prime", "Yes. 9 is not even", "No. 9 has only one factor"],
                   "The factors of 9 are 1, 3 and 9. That is three factors, so 9 is <b>composite</b>. "
                   "Many odd numbers are composite: 9, 15, 21, 25, 27 …"))

    ps = [p for p in range(10, 21) if is_prime(p)]
    assert ps == [11, 13, 17, 19]
    its.append(mcq("How many prime numbers are there between 10 and 20?", 4, [5, 3, 6],
                   "The primes are 11, 13, 17 and 19: <b>4</b> primes. 15 is odd but not prime (15 = 3 × 5)."))
    ps = [p for p in range(30, 41) if is_prime(p)]
    assert ps == [31, 37]
    its.append(mcq("How many prime numbers are there between 30 and 40?", 2, [5, 3, 4],
                   "Test the odd numbers: 31 is prime, 33 = 3 × 11, 35 = 5 × 7, 37 is prime and 39 = 3 × 13. "
                   "So there are <b>2</b> primes, 31 and 37. 5 counts every odd number."))

    its.append(mcq("How many factors does every prime number have?", "Exactly 2", ["Exactly 1", "Exactly 3", "More than 2"],
                   "A prime number has <b>exactly two</b> factors: 1 and itself. More than two factors means composite."))

    assert 57 == 3 * 19
    its.append(mcq("Is 57 prime or composite?", "Composite. 57 = 3 × 19",
                   ["Prime. It is odd", "Prime. It is not in a times table", "Composite. 57 = 7 × 8"],
                   "5 + 7 = 12, so 57 is divisible by 3: 57 = 3 × 19. It is <b>composite</b>. "
                   "7 × 8 = 56, not 57."))

    lists = {"2, 13, 29, 31": True, "1, 13, 29, 31": False, "3, 13, 27, 31": False, "2, 13, 29, 33": False}
    assert all(all(is_prime(int(v)) for v in k.split(", ")) == ok for k, ok in lists.items())
    its.append(mcq("Which list has <b>only</b> prime numbers?", "2, 13, 29, 31",
                   ["1, 13, 29, 31", "3, 13, 27, 31", "2, 13, 29, 33"],
                   "2, 13, 29 and 31 each have exactly two factors, so <b>2, 13, 29, 31</b> are all prime. "
                   "1 is not prime, 27 = 3 × 9 and 33 = 3 × 11."))

    ps = [p for p in range(1, 20) if is_prime(p)]
    assert ps == [2, 3, 5, 7, 11, 13, 17, 19]
    its.append(mcq("Which list shows all the prime numbers less than 20?", "2, 3, 5, 7, 11, 13, 17, 19",
                   ["1, 3, 5, 7, 11, 13, 17, 19", "3, 5, 7, 9, 11, 13, 15, 17, 19", "2, 3, 5, 7, 11, 13, 17"],
                   "The primes less than 20 are <b>2, 3, 5, 7, 11, 13, 17, 19</b>. 1 is not prime, 2 is prime, "
                   "9 and 15 are composite, and 19 must not be left out."))

    assert not is_prime(21) and is_prime(23)
    its.append(mcq("Which number is odd <b>and</b> composite?", 21, [23, 1, 4],
                   "21 = 3 × 7, so <b>21</b> is composite, and it is odd. 23 is prime, 1 is neither prime nor composite, "
                   "and 4 is composite but even."))
    assert len(its) == 20, len(its)
    return {"title": "Prime and composite numbers", "items": its}


# ============================================================ set 4: prime factorization and factor trees
def set_trees(P):
    its = []
    for x in [24, 60, 45, 36, 72, 90]:
        t = auto_tree(x)
        ps = sorted(leaves(t))
        assert all(is_prime(p) for p in ps) and prod(ps) == x
        first = split(x)
        once = sorted(set(ps))
        if prod(once) == x:
            once = None
        with1 = [1] + ps
        cands = [times(first), times(with1)] + ([times(once)] if once else []) + [" + ".join(map(str, ps))]
        comp = sorted(set(v for v in first if not is_prime(v)))
        e = ("Keep splitting until every branch ends in a prime: %d = <b>%s</b>. %s is not finished, because %s "
             "not prime. 1 is not prime, so it is not written."
             % (x, times(ps), times(first), " and ".join(map(str, comp)) + (" are" if len(comp) > 1 else " is")))
        if once:
            e += " Write a repeated prime every time it appears."
        its.append(mcq(fig(tree_svg(t)) + "What is the prime factorization of %d?" % x, times(ps), cands, e))

    # missing number in a tree
    t = T(84, T(4, 2, 2), T(21, 3, 7))
    its.append(mcq(fig(tree_svg(t, hide=21)) + "What number is missing from the factor tree?", 21, [88, 80, 42],
                   "The branches of 84 must multiply to 84: 4 × ? = 84, so ? = 84 ÷ 4 = <b>21</b>. "
                   "Check: 21 = 3 × 7. 80 comes from subtracting 4, 88 from adding 4, and 42 is 84 ÷ 2."))
    t = T(150, T(10, 2, 5), T(15, 3, 5))
    its.append(mcq(fig(tree_svg(t, hide=150)) + "What number is at the top of the factor tree?", 150, [17, 30, 75],
                   "Multiply the primes at the ends: 2 × 5 × 3 × 5 = <b>150</b>. Or 10 × 15 = 150. "
                   "17 comes from adding 2 + 5 + 3 + 5, 30 uses each prime only once, and 75 leaves out the 2."))
    t = T(98, 2, T(49, 7, 7))
    its.append(mcq(fig(tree_svg(t, hide=49)) + "What number is missing from the factor tree?", 49, [14, 96, 196],
                   "2 × ? = 98, so ? = 98 ÷ 2 = <b>49</b>, and 49 = 7 × 7. "
                   "14 is 7 + 7, 96 comes from subtracting 2, and 196 comes from multiplying 98 × 2."))

    for x in [18, 40, 56, 100, 126]:
        ps = primes_of(x)
        first = split(x)
        cands = [times(first)]
        once = sorted(set(ps))
        if prod(once) != x:
            cands.append(times(once))
        cands += [times([1] + ps), times(ps[1:])]
        e = ("Split %d into a factor pair and keep going until every factor is prime: %d = %s = <b>%s</b>. "
             "%s is not finished, because %s is not prime. Write every prime, even when it repeats, and do not write 1."
             % (x, x, times(first), times(ps), times(first),
                " and ".join(str(v) for v in sorted(set(first)) if not is_prime(v))))
        comp = sorted(set(v for v in first if not is_prime(v)))
        if len(comp) > 1:
            e = e.replace("is not prime.", "are not prime.")
        its.append(mcq("What is the prime factorization of %d?" % x, times(ps), cands, e))

    for ps, wrong_extra in [([2, 2, 3, 5], 120), ([2, 3, 3, 7], 252)]:
        x = prod(ps)
        s = sum(ps)
        once = prod(sorted(set(ps)))
        assert wrong_extra == 2 * x
        its.append(mcq("Which number has the prime factorization %s?" % times(ps), x, [s, once, wrong_extra],
                       "Multiply the primes: %s = <b>%d</b>. %d comes from adding them, %d uses each prime only once, "
                       "and %d has an extra 2." % (times(ps), x, s, once, wrong_extra)))

    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    its.append(mcq("%s starts a factor tree for 36 with 4 × 9. %s starts with 6 × 6. What will they find?" % (nm, nm2),
                   "Both get 2 × 2 × 3 × 3",
                   ["Only %s is right" % nm, "Only %s is right" % nm2, "They get different primes"],
                   "4 × 9 = 2 × 2 × 3 × 3 and 6 × 6 = 2 × 3 × 2 × 3. The order is different, but the primes are the same. "
                   "Every composite number has only <b>one</b> prime factorization."))
    assert sorted(primes_of(36)) == [2, 2, 3, 3]

    nm, he, his = P.next()
    its.append(mcq("%s’s factor tree for 40 ends with 2, 4 and 5. What should %s do next?" % (nm, he),
                   "Split 4 into 2 × 2", ["Nothing. It is finished", "Split 5 into 1 × 5", "Add 2 + 4 + 5"],
                   "4 is not prime, so the branch is not finished. 4 = 2 × 2, so 40 = <b>2 × 2 × 2 × 5</b>. "
                   "5 is already prime, and we never split off 1."))
    assert primes_of(40) == [2, 2, 2, 5]

    assert primes_of(48) == [2, 2, 2, 2, 3] and 2 * 2 * 2 * 3 == 24
    its.append(mcq("Which prime factorization is correct?", "48 = 2 × 2 × 2 × 2 × 3",
                   ["48 = 2 × 2 × 2 × 6", "48 = 2 × 3 × 8", "48 = 2 × 2 × 2 × 3"],
                   "2 × 2 × 2 × 2 × 3 = 16 × 3 = 48, and every factor is prime, so <b>48 = 2 × 2 × 2 × 2 × 3</b> is correct. "
                   "6 and 8 are not prime, and 2 × 2 × 2 × 3 = 24, not 48."))

    assert 42 % 7 == 0 and is_prime(7) and not any(is_prime(v) for v in (6, 21, 14))
    its.append(mcq("Which number is a <b>prime</b> factor of 42?", 7, [6, 21, 14],
                   "42 = 2 × 3 × 7, so the prime factors are 2, 3 and 7. <b>7</b> is the answer. "
                   "6, 21 and 14 are factors of 42, but they are composite."))
    assert len(its) == 20, len(its)
    return {"title": "Prime factorization with factor trees", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    # arranging chairs
    nm, he, his = P.next()
    good, bad = (4, 9), [(5, 7), (6, 7), (8, 4)]
    assert prod(good) == 36 and all(prod(b) != 36 for b in bad)
    its.append(mcq("%s sets up 36 chairs for the school assembly in equal rows. Which arrangement uses all 36 chairs?" % nm,
                   "4 rows of 9", ["%d rows of %d" % b for b in bad],
                   "4 × 9 = 36, so <b>4 rows of 9</b> works. 5 × 7 = 35, 6 × 7 = 42 and 8 × 4 = 32."))

    ways = [d for d in factors(28) if 2 <= d <= 14]
    assert ways == [2, 4, 7, 14]
    its.append(mcq("A teacher puts 28 chairs in equal rows, with at least 2 rows and at least 2 chairs in each row. "
                   "4 rows of 7 and 7 rows of 4 count as different. How many arrangements are possible?",
                   4, [6, 2, 3],
                   "The number of rows must be a factor of 28 between 2 and 14: 2, 4, 7 and 14. That gives <b>4</b> "
                   "arrangements: 2 × 14, 4 × 7, 7 × 4 and 14 × 2. 6 would include 1 row of 28 and 28 rows of 1."))

    its.append(mcq("Ms. Chen has 23 chairs. She cannot set them in equal rows, unless she uses 1 row. Why?",
                   "23 is a prime number", ["23 is an odd number", "23 ends in 3", "23 is a composite number"],
                   "The only factors of 23 are 1 and 23, so <b>23 is prime</b>: the only rows are 1 row of 23 or 23 rows "
                   "of 1. Being odd is not the reason: 21 chairs can make 3 rows of 7."))

    assert all(120 % r for r in (14, 16, 18)) and 120 % 12 == 0
    its.append(mcq("The gym has 120 chairs for the Grade 6 graduation. They go in equal rows, with between 10 and 20 rows. "
                   "Which number of rows works?", "12 rows", ["14 rows", "16 rows", "18 rows"],
                   "120 ÷ 12 = 10, so <b>12 rows</b> of 10 chairs works. 120 ÷ 14, 120 ÷ 16 and 120 ÷ 18 all leave a "
                   "remainder. Being even is not enough."))

    good, bad = 36, [30, 42, 26]
    assert all(good % d == 0 for d in (3, 4, 6)) and all(any(b % d for d in (3, 4, 6)) for b in bad)
    its.append(mcq("Which number of chairs can be set out in rows of 3, in rows of 4 <b>or</b> in rows of 6, "
                   "with no chairs left over?", 36, bad,
                   "36 ÷ 3 = 12, 36 ÷ 4 = 9 and 36 ÷ 6 = 6, so <b>36</b> works. 30 and 42 are not divisible by 4 "
                   "(30 ÷ 4 = 7 R2, 42 ÷ 4 = 10 R2), and 2 + 6 = 8, so 26 is not divisible by 3."))

    # packaging
    assert 132 % 6 == 0
    its.append(mcq("A bakery packs 132 butter tarts in boxes of 6. Will any tarts be left over?",
                   "No. 132 is divisible by 6", ["Yes. 132 does not end in 6", "Yes. 132 is not divisible by 3",
                                                "No. All even numbers divide by 6"],
                   "132 is even, and 1 + 3 + 2 = 6 is divisible by 3. So 132 is divisible by 6: 132 ÷ 6 = 22 boxes, "
                   "with <b>none left over</b>. Not every even number works: 140 ÷ 6 has a remainder."))
    assert 140 % 6

    assert 1318 % 4 == 2
    its.append(mcq("A farm packs 1318 eggs in trays of 4. How many eggs are left over?", 2, [0, 3, 1],
                   "The last two digits make 18. 18 ÷ 4 = 4 R2, so 1318 ÷ 4 = 329 R2: <b>2 eggs</b> are left over. "
                   "1318 is even, but that does not make it divisible by 4."))

    assert 1458 % 9 == 0 and 1458 // 9 == 162
    its.append(mcq("A sugar shack has 1458 maple candies. Can they all go into bags of 9 with none left over?",
                   "Yes. The digits add to 18", ["No. 1458 does not end in 9", "No. 1458 is even",
                                                "No. The digits add to 17"],
                   "1 + 4 + 5 + 8 = 18, and 18 is divisible by 9. So <b>yes</b>: 1458 ÷ 9 = 162 bags."))

    good, bad = 2136, [2124, 2140, 2116]
    assert good % 8 == 0 and all(b % 8 for b in bad) and all(b % 4 == 0 for b in bad)
    its.append(mcq("Juice boxes come in packs of 8. Which order of juice boxes can be packed with none left over?",
                   n(good), [n(b) for b in bad],
                   cap(rule(good, 8)) + ". 2124, 2140 and 2116 are divisible by 4, but their last three digits (124, 140, "
                   "116) are not divisible by 8. 24 is divisible by 8, but 124 is not."))

    nm, he, his = P.next()
    assert 1350 % 9 == 0 and 1350 // 9 == 150
    its.append(mcq("%s has 1350 hockey cards to share equally among 9 friends. How many cards does each friend get?" % nm,
                   150, [15, 105, 160],
                   "1 + 3 + 5 + 0 = 9, so 1350 is divisible by 9. 1350 ÷ 9 = <b>150</b>, with none left over. "
                   "Check: 150 × 9 = 1350. 15 forgets the 0, 105 × 9 = 945, and 160 × 9 = 1440."))

    nm, he, his = P.next()
    assert 72 % 5 and all(72 % v == 0 for v in (8, 9, 6))
    its.append(mcq("%s packs 72 granola bars into equal bags for a field trip. Which number of bags does <b>not</b> work?" % nm,
                   "5 bags", ["8 bags", "9 bags", "6 bags"],
                   "72 ends in 2, so it is not divisible by 5: <b>5 bags</b> do not work. 72 ÷ 8 = 9, 72 ÷ 9 = 8 and "
                   "72 ÷ 6 = 12."))

    assert 30 % 4 and all(30 % r == 0 for r in (5, 3, 2))
    its.append(mcq("A box holds 30 chocolates in equal rows. Which number of rows is <b>not</b> possible?",
                   "4 rows", ["5 rows", "3 rows", "2 rows"],
                   "30 ÷ 4 = 7 R2, so <b>4 rows</b> is not possible. 5 rows of 6, 3 rows of 10 and 2 rows of 15 all "
                   "make 30. 4 is even like 30, but it is not a factor of 30."))

    # teams
    assert 48 % 7 and all(48 % v == 0 for v in (6, 8, 4))
    its.append(mcq("There are 48 students in a gym class. Which team size leaves some students out?",
                   "7 players", ["6 players", "8 players", "4 players"],
                   "48 ÷ 7 = 6 R6, so teams of <b>7</b> leave 6 students out. 48 ÷ 6 = 8, 48 ÷ 8 = 6 and 48 ÷ 4 = 12."))

    nm, he, his = P.next()
    assert 51 == 3 * 17
    its.append(mcq("%s says 51 campers cannot be split into equal canoe groups, because 51 is prime. Is %s right?"
                   % (nm, he), "No. 3 groups of 17 work",
                   ["Yes. 51 is prime", "Yes. 51 is odd", "No. 5 groups of 10 work"],
                   "5 + 1 = 6, so 51 is divisible by 3: 51 = 3 × 17. 51 is <b>composite</b>, so 3 groups of 17 "
                   "(or 17 groups of 3) work. 5 groups of 10 is only 50."))

    # riddles
    ans = [v for v in range(41, 50) if is_prime(v) and dsum(v) == 7]
    assert ans == [43] and is_prime(41) and is_prime(47) and not is_prime(49)
    its.append(mcq("I am a prime number between 40 and 50. My digits add up to 7. What number am I?",
                   43, [41, 47, 49],
                   "The primes between 40 and 50 are 41, 43 and 47. 4 + 3 = 7, so the number is <b>43</b>. "
                   "49 is not prime: 49 = 7 × 7."))

    ans = [v for v in range(20, 41) if v % 4 == 0 and v % 9 == 0]
    assert ans == [36]
    its.append(mcq("I am a number between 20 and 40. I am divisible by 4 and by 9. What number am I?",
                   36, [13, 24, 27],
                   "36 ÷ 4 = 9 and 36 ÷ 9 = 4, so the number is <b>36</b>. 13 is 4 + 9, 24 is divisible by 4 only, "
                   "and 27 is divisible by 9 only."))

    good, bad = (11, 13), [(9, 15), (1, 23), (2, 22)]
    assert sum(good) == 24 and all(map(is_prime, good))
    assert all(sum(p) == 24 and not all(map(is_prime, p)) for p in bad)
    its.append(mcq("Which pair of prime numbers adds up to 24?", "11 and 13", ["%d and %d" % p for p in bad],
                   "11 and 13 are both prime, and 11 + 13 = <b>24</b>. 9 and 15 are composite, 1 is not prime, "
                   "and 22 = 2 × 11 is not prime."))

    # prime factorization in context
    nm, he, his = P.next()
    assert prod([2, 3, 5]) == 30
    its.append(mcq("%s multiplies three <b>different</b> prime numbers and gets 30. What are the three primes?" % nm,
                   "2, 3 and 5", ["1, 2 and 15", "1, 5 and 6", "2, 3 and 6"],
                   "30 = 2 × 3 × 5, and 2, 3 and 5 are all prime. So the answer is <b>2, 3 and 5</b>. "
                   "1 is not prime, 15 and 6 are composite, and 2 × 3 × 6 = 36."))

    nm, he, his = P.next()
    assert prod([2, 3, 7]) == 42
    its.append(mcq("The code for %s’s locker is a 2-digit number. Its prime factorization is 2 × 3 × 7. "
                   "What is the code?" % nm, 42, [12, 21, 84],
                   "2 × 3 × 7 = 6 × 7 = <b>42</b>. 12 comes from adding 2 + 3 + 7, 21 forgets the 2, "
                   "and 84 has an extra 2."))

    assert primes_of(64) == [2] * 6 and 64 // 2 == 32
    its.append(mcq("A class collects 64 cans for the food bank and packs them in boxes. Each box holds a prime number "
                   "of cans and every box is full. How many cans are in each box?", "2 cans",
                   ["4 cans", "8 cans", "3 cans"],
                   "64 = 2 × 2 × 2 × 2 × 2 × 2, so 2 is its <b>only</b> prime factor. Each box holds <b>2 cans</b> "
                   "(32 boxes). 4 and 8 are factors of 64, but they are not prime, and 64 ÷ 3 has a remainder."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: chairs, packages and teams", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Divisibility rules</h2>"
        "<p>A number is <b>divisible</b> by another when it divides with no remainder. "
        "These rules let you check quickly, without dividing.</p>"
        + table(["Divisible by", "Rule", "Example"], [
            ["2", "The last digit is even (0, 2, 4, 6, 8)", "3458"],
            ["3", "The digits add to a multiple of 3", "4521: 4 + 5 + 2 + 1 = 12"],
            ["4", "The last two digits make a number divisible by 4", "5316: 16 ÷ 4 = 4"],
            ["5", "The last digit is 0 or 5", "7465"],
            ["6", "Divisible by 2 <b>and</b> by 3", "4362: even, digits add to 15"],
            ["8", "The last three digits make a number divisible by 8", "7128: 128 ÷ 8 = 16"],
            ["9", "The digits add to a multiple of 9", "7254: 7 + 2 + 5 + 4 = 18"],
            ["10", "The last digit is 0", "6390"],
        ])
        + ex("Example", "Is 2748 divisible by 3, 4, 6 and 9?",
             "Digits: 2 + 7 + 4 + 8 = 21. 21 is divisible by 3, but not by 9. Last two digits: 48 ÷ 4 = 12. "
             "2748 is even and divisible by 3, so it is divisible by 6.",
             "by 3, 4 and 6, but not by 9")
        + "<h2>Factors and multiples</h2>"
        "<p>A <b>factor</b> divides a number exactly. A <b>multiple</b> is the number times 1, 2, 3 and so on. "
        "3 × 8 = 24, so 3 and 8 are factors of 24, and 24 is a multiple of 3 and of 8.</p>"
        "<p>To find all the factors, find the <b>factor pairs</b>. Test 1, 2, 3, 4 … in order and stop when the pairs meet.</p>"
        "<figure class='sn-fig'>" + rainbow_svg(36) +
        "<figcaption>The factor pairs of 36: 1 × 36, 2 × 18, 3 × 12, 4 × 9 and 6 × 6. 36 has 9 factors.</figcaption></figure>"
        + "<h2>Prime and composite numbers</h2>"
        "<p>A <b>prime number</b> has exactly two factors: 1 and itself. A <b>composite number</b> has more than two. "
        "<b>1 is neither</b>, because it has only one factor. 2 is the only even prime.</p>"
        + table(["Prime numbers to 50"], [["2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47"]])
        + "<p>Some odd numbers look prime but are not: 9 = 3 × 3, 51 = 3 × 17, 57 = 3 × 19 and 91 = 7 × 13. "
        "Use the divisibility rules to test them.</p>"
        "<h2>Prime factorization</h2>"
        "<p>Every composite number can be written as a product of primes. A <b>factor tree</b> splits the number "
        "into a factor pair, then splits again, until every branch ends in a prime.</p>"
        "<figure class='sn-fig'>" + tree_svg(auto_tree(60)) +
        "<figcaption>60 = 6 × 10 = 2 × 3 × 2 × 5. In order: 60 = 2 × 2 × 3 × 5.</figcaption></figure>"
        + ex("Example", "Write 72 as a product of prime factors.",
             "72 = 8 × 9. 8 = 2 × 2 × 2 and 9 = 3 × 3. Check: 8 × 9 = 72.", "72 = 2 × 2 × 2 × 3 × 3")
        + "<p>You can start the tree with any factor pair (72 = 6 × 12 works too). You always end with the same primes.</p>"
        "<h2>Using factors in problems</h2>"
        "<p>Setting out chairs in equal rows or packing things into equal boxes is a factor problem. "
        "The number of rows must be a factor of the number of chairs.</p>"
        "<figure class='sn-fig'>" + chairs_row_svg([(2, 12), (3, 8), (4, 6)]) +
        "<figcaption>24 chairs can go in 2 rows of 12, 3 rows of 8 or 4 rows of 6. 23 chairs could only make 1 row, "
        "because 23 is prime.</figcaption></figure>"
        + ex("Example", "Can 1458 maple candies go into bags of 9 with none left over?",
             "1 + 4 + 5 + 8 = 18, and 18 is divisible by 9.", "yes, 162 bags")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Saying 1 is prime (or composite)", "1 has only one factor. It is neither"],
            ["Saying 9 is prime because it is odd", "9 = 3 × 3. Test odd numbers with the rules"],
            ["Adding the digits to test for 4", "The digit sum works for 3 and 9 only. For 4, use the last two digits"],
            ["Using the last two digits for 8", "For 8, use the last three digits"],
            ["Checking only “even” for 6", "Test for 2 and for 3"],
            ["Thinking a number ending in 9 is divisible by 9", "Add the digits: 29 → 11, not divisible"],
            ["Stopping a factor tree at 4 or 9", "Keep going until every branch is prime"],
            ["Writing 1 in a prime factorization", "1 is not prime, so leave it out"],
        ])
    )


FAQ = [
    {"q": "What divisibility rules do Grade 6 students learn in Ontario?",
     "a": "The Ontario Grade 6 math curriculum uses the rules for 2, 3, 4, 5, 6, 8, 9 and 10. For example, a number is divisible by 3 when its digits add to a multiple of 3, and by 4 when its last two digits make a multiple of 4."},
    {"q": "Is 1 a prime number or a composite number?",
     "a": "Neither. A prime has exactly two factors and a composite number has more than two, but 1 has only one factor. The smallest prime is 2."},
    {"q": "How do you find the prime factorization of a number?",
     "a": "Make a factor tree: split the number into any factor pair and keep splitting until every branch ends in a prime. For example, 60 = 2 × 2 × 3 × 5."},
    {"q": "Are factors, primes and divisibility on the Grade 6 EQAO math test?",
     "a": "EQAO’s Grade 6 math assessment is based on the Ontario curriculum, which includes divisibility rules, factors and prime numbers, so questions on them can appear. They also help with simplifying fractions."},
]


def gen():
    rnd = random.Random(36808)
    P = People(rnd)
    sets = [set_divisibility(P), set_factors(P), set_primes(P), set_trees(P), set_words(P)]
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
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "factors-primes-and-divisibility", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Factors, Prime Numbers and Divisibility Rules",
        "seo_title": "Grade 6 Divisibility Rules, Factors and Prime Numbers Worksheets (Free, Answer Key)",
        "short_title": "Factors, primes and divisibility",
        "domain": "Number",
        "standard_code": "Grade 6: Number, B2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use the divisibility rules for 2, 3, 4, 5, 6, 8, 9, and 10 to determine whether numbers are divisible by these numbers, and use prime factors to express composite numbers",
        "meta_desc": "Free Grade 6 math worksheets for the Ontario curriculum: divisibility rules for 2, 3, 4, 5, 6, 8, 9 and 10, factors and multiples, prime and composite numbers, prime factorization with factor trees, and word problems. 100 questions with an answer key, good EQAO practice.",
        "key_big": "A prime number has exactly two factors. Every composite number is a product of primes.",
        "key_sub": "1 is neither prime nor composite. Add the digits to test for 3 and 9; use the last two digits for 4 and the last three for 8. For 6, test 2 and 3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "factor tree")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
