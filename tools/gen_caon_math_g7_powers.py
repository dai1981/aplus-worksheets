# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 7 Math: Powers and Large Numbers
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 - Grade 7, Number, B2.7 and B1.1)
  python3 tools/gen_caon_math_g7_powers.py
Whole numbers to one billion, place value and powers of ten, exponential notation, evaluating powers,
expanded form with powers of ten, and word problems in real Canadian contexts.
Numbers: 4-digit numbers have no separator; 5 or more digits use a no-break space (45 300 000). Never commas.
Exponents are written with <sup> in HTML fields; plain-text fields (title, key, FAQ, set titles) use
Unicode superscripts (2⁵).
Every answer is checked in code (exact integers). Every choice that is a number or an expression is
evaluated, so no two choices are ever equal in value.
Wrong answers come from real mistakes: base × exponent (2⁵ = 10), swapping base and exponent (5² for 2⁵),
counting the × signs instead of the factors, one zero too many or too few (10⁶ with 7 zeros), giving the
digit instead of its value, missing zero placeholders, comparing first digits only, adding instead of
multiplying, and multiplying 10 × 10⁴ into 100⁴.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
DZX, DZY = 0.55, 0.40

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands",
      "millions", "ten millions", "hundred millions", "billions"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand",
       "million", "ten million", "hundred million", "billion"]
SUPS = dict(zip("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))


# ------------------------------------------------------------ helpers
def n(x):
    """Ontario/SI style: 4536, 10 000, 45 300 000 (no-break spaces, never commas)."""
    s = str(x)
    if len(s) <= 4:
        return s
    g = []
    while s:
        g.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(g)


def pw(b, e):
    """Power in HTML: 2<sup>5</sup>."""
    return "%s<sup>%d</sup>" % (b, e)


def ups(b, e):
    """Power in plain text: 2⁵."""
    return "%s%s" % (b, "".join(SUPS[c] for c in str(e)))


def tms(d, e):
    """d × 10^e in HTML."""
    return "%d × %s" % (d, pw(10, e))


def expanded(x):
    """Expanded form with powers of ten (10 for the tens, no 10⁰ term), largest place first."""
    parts = []
    s = str(x)
    for j, ch in enumerate(s):
        k = len(s) - 1 - j
        d = int(ch)
        if not d:
            continue
        parts.append(str(d) if k == 0 else ("%d × 10" % d if k == 1 else tms(d, k)))
    return " + ".join(parts)


def value(c):
    """Exact value of a choice that is a number or an expression; None otherwise (words, lists, comparisons)."""
    t = c.replace(NB, "")
    t = re.sub(r"<sup>(\d+)</sup>", r"**\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r" (km|m|cm|cells|layers|parents|people|bills|zeros|places)(²|³)?$", "", t)
    t = t.replace("$", "")
    if not re.fullmatch(r"[\d ×+−*()]+", t):
        return None
    t = t.replace("×", "*").replace("−", "-")
    return eval(t)


def mcq(q, correct, wrong, e):
    """4 choices: correct first + 3 wrong. No two choices may be equal in value."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    vs = [value(x) for x in ch]
    known = [v for v in vs if v is not None]
    assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def pick3(correct, cands):
    out = []
    for v in cands:
        if v is None or v <= 0 or v == correct or v in out:
            continue
        out.append(v)
        if len(out) == 3:
            break
    assert len(out) == 3, (correct, cands)
    return out


def mcq_n(q, correct, cands, e, unit=""):
    return mcq(q, n(correct) + unit, [n(v) + unit for v in pick3(correct, cands)], e)


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
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def B(s):
    return "<b>%s</b>" % s


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def digit(x, i):
    return (x // 10 ** i) % 10


def ndig(x):
    return len(str(x))


def cap(s):
    return s[0].upper() + s[1:]


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


# ------------------------------------------------------------ numbers in words (no "and")
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def w100(x):
    if x < 20:
        return ONES[x]
    return TENS[x // 10] + ("-" + ONES[x % 10] if x % 10 else "")


def w1000(x):
    h, r = divmod(x, 100)
    out = []
    if h:
        out.append(ONES[h] + " hundred")
    if r:
        out.append(w100(r))
    return " ".join(out)


def words(x):
    assert 0 < x <= 10 ** 9
    if x == 10 ** 9:
        return "one billion"
    m, r = divmod(x, 10 ** 6)
    t, o = divmod(r, 1000)
    parts = []
    if m:
        parts.append(w1000(m) + " million")
    if t:
        parts.append(w1000(t) + " thousand")
    if o:
        parts.append(w1000(o))
    return " ".join(parts)


assert words(608040500) == "six hundred eight million forty thousand five hundred"
assert words(2070009) == "two million seventy thousand nine"
assert words(1017449) == "one million seventeen thousand four hundred forty-nine"


def zero_mistakes(x):
    """Numbers a student writes when a zero goes missing, moves, or is added."""
    s = str(x)
    out = []
    for i, ch in enumerate(s):
        if ch == "0":
            for j in (i - 1, i + 1):
                if 0 < j < len(s) and s[j] != "0":
                    l = list(s)
                    l[i], l[j] = l[j], l[i]
                    out.append(int("".join(l)))
            out.append(int(s[:i] + s[i + 1:]))
    for i in range(1, len(s)):
        if s[i] == "0":
            out.append(int(s[:i] + "0" + s[i:]))
    return [v for v in out if v != x and 1000 <= v < 10 ** 10]


def joined_digits(x):
    return int("".join(ch for ch in str(x) if ch != "0"))


# ------------------------------------------------------------ figures
CW, H1, H2, ROW = 50, 28, 30, 48
SUB = ["H", "T", "O"] * 3


def chart_svg(x, hi=None, powers=False):
    """Millions | Thousands | Ones chart (9 places). Second header row: H T O, or the powers of ten 10⁸ ... 10¹ and 1."""
    x0 = y0 = 6
    W, H = 2 * x0 + 9 * CW, 2 * y0 + H1 + H2 + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (x0, y0, 9 * CW, H1 + H2 + ROW),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 9 * CW, H1 + H2, FILL)]
    for k, name in [(0, "Millions"), (3, "Thousands"), (6, "Ones")]:
        s.append(text(x0 + k * CW + 1.5 * CW, y0 + 19, name, 14, bold=True))
    for k in (3, 6):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + k * CW, y0, x0 + k * CW, y0 + H1 + H2 + ROW, GREEN))
    nd = ndig(x)
    for k in range(9):
        i = 8 - k
        xx = x0 + k * CW
        if k not in (0, 3, 6):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (xx, y0 + H1, xx, y0 + H1 + H2 + ROW, GREEN))
        if powers and i == 0:
            s.append(text(xx + CW / 2, y0 + H1 + 21, "1", 16, bold=True))
        elif powers:
            s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>"
                     "10<tspan dy='-7' font-size='14'>%d</tspan></text>" % (xx + CW / 2.0, y0 + H1 + 22, INK, i))
        else:
            s.append(text(xx + CW / 2, y0 + H1 + 20, SUB[k], 14, bold=True))
        if i < nd:
            s.append(text(xx + CW / 2, y0 + H1 + H2 + 34, str(digit(x, i)), 28, bold=True,
                          col=RED if hi == i else INK))
    for y in (y0 + H1, y0 + H1 + H2):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0, y, x0 + 9 * CW, y, GREEN, "1.2" if y == y0 + H1 else "2"))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, 9 * CW, H1 + H2 + ROW, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % n(x))


def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(" ") * 0.3) * fs * 0.6


class Canvas:
    """Collects shapes and text, tracks the bounding box, then writes a tight SVG."""
    def __init__(self):
        self.el, self.boxes = [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=1.6, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def circle(self, x, y, r, fill, col=GREEN):
        self.el.append(("c", x, y, r, fill, col))
        self.grow(x - r - 1, y - r - 1, x + r + 1, y + r + 1)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK):
        """(x, y) is the middle of the text."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def svg(self, label, pad=5, square_ok=False):
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H_ = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H_ and not square_ok:
            W += 1
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "c":
                _, x, y, r, f, col = e
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s' stroke='%s' stroke-width='1.6'/>"
                         % (x - ox, y - oy, r, f, col))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H_, "".join(s), label)


def proj(X, Y, Z, k):
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


def draw_cube(cv, m, k, dx=0.0):
    """m × m × m unit cubes, back to front; faces hidden by a neighbour are left out."""
    keys = {(x, y, z) for x in range(m) for y in range(m) for z in range(m)}
    drawn = 0
    for x, y, z in sorted(keys, key=lambda c: (-c[2], c[1], c[0])):
        p = lambda a, b, c: (proj(x + a, y + b, z + c, k)[0] + dx, proj(x + a, y + b, z + c, k)[1])
        if (x, y, z - 1) not in keys:
            cv.poly([p(0, 0, 0), p(1, 0, 0), p(1, 1, 0), p(0, 1, 0)], FILL)
        if (x, y + 1, z) not in keys:
            cv.poly([p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1)], TOP)
        if (x + 1, y, z) not in keys:
            cv.poly([p(1, 0, 0), p(1, 0, 1), p(1, 1, 1), p(1, 1, 0)], SIDE)
        drawn += 1
    assert drawn == m ** 3


def draw_square(cv, m, c, x0=0.0, y0=0.0):
    for i in range(m):
        for j in range(m):
            x, y = x0 + i * c, y0 - (j + 1) * c
            cv.poly([(x, y), (x + c, y), (x + c, y + c), (x, y + c)], FILL)


def cube_svg(m):
    cv = Canvas()
    draw_cube(cv, m, k=min(24, 130 / m))
    return cv.svg("cube made of unit cubes, %d on each edge" % m)


def square_svg(m):
    cv = Canvas()
    draw_square(cv, m, c=min(20, 120 / m))
    return cv.svg("square grid of unit squares, %d on each side" % m, square_ok=True)


def square_and_cube_svg():
    """Lesson: 3 × 3 square (3² = 9) next to a 3 × 3 × 3 cube (3³ = 27)."""
    cv = Canvas()
    c = 24
    draw_square(cv, 3, c)
    cv.text(1.5 * c, 18, "3² = 9", 18)
    x0 = 3 * c + 60
    draw_cube(cv, 3, c, dx=x0)
    cv.text(x0 + 1.5 * c, 18, "3³ = 27", 18)
    return cv.svg("a 3 by 3 square of 9 unit squares and a 3 by 3 by 3 cube of 27 unit cubes")


def doubling_svg(rows=4):
    """Cells that split in two every hour: Start 1, 1 h 2, 2 h 4, 3 h 8."""
    cv = Canvas()
    r, gap, rowh = 8, 22, 26
    for k in range(rows):
        y = k * rowh
        cv.text(0, y, "Start" if k == 0 else "%d h" % k, 14, anchor="end")
        for j in range(2 ** k):
            cv.circle(18 + r + j * gap, y, r, FILL)
        cv.text(18 + 2 * r + (2 ** (rows - 1) - 1) * gap + 14, y, str(2 ** k), 14, anchor="start", col=GREEN)
    return cv.svg("cells that double every hour: 1, 2, 4, 8")


# ============================================================ set 1: numbers to one billion
def value_cands(d, i):
    return [d * 10 ** (i + 1) if i + 1 <= 8 else None, d * 10 ** (i - 1) if i >= 1 else None, d,
            d * 10 ** (i - 2) if i >= 2 else None, d * 10 ** (i + 2) if i + 2 <= 8 else None]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), n(v), d, n(v)))


def distinct9(rnd, used, need_place=None):
    while True:
        ds = rnd.sample(range(10), 9)
        if ds[0] == 0:
            continue
        x = int("".join(map(str, ds)))
        if x in used or (need_place is not None and digit(x, need_place) == 0):
            continue
        used.add(x)
        return x


def set_billion(rnd, used):
    A, Bv, C = [], [], []
    for i in [6, 7, 8, 5]:                                      # chart, red digit (4)
        x = distinct9(rnd, used, i)
        d = digit(x, i)
        A.append(mcq_n(fig(chart_svg(x, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True)))
    for i in [7, 6, 4]:                                         # value, no chart (3)
        x = distinct9(rnd, used, i)
        d = digit(x, i)
        Bv.append(mcq_n("What is the value of the digit %d in %s?" % (d, n(x)), d * 10 ** i,
                        value_cands(d, i), value_e(d, i)))
    for i in [6, 8]:                                            # which digit is in a place (2)
        x = distinct9(rnd, used, i)
        d = digit(x, i)
        cands = [str(digit(x, k)) for k in sorted(range(9), key=lambda k: (abs(k - i), k)) if k != i][:3]
        e = ("Read the groups from the right: ones, thousands, millions. In the millions group the places are "
             "millions, ten millions and hundred millions. In %s the %s digit is %d, worth %s."
             % (n(x), PL[i], d, n(d * 10 ** i)))
        C.append(mcq("In %s, which digit is in the %s place?" % (n(x), PL[i]), str(d), cands, e))
    Dw = []
    for x in [45300000, 608040500, 2070009]:                   # words -> numeral (3)
        used.add(x)
        m, r = divmod(x, 10 ** 6)
        t, o = divmod(r, 1000)
        grp = "%s million → %d. %s thousand → %03d. %s → %03d." % (
            cap(w1000(m)), m, cap(w1000(t)) if t else "No", t, cap(w1000(o)) if o else "Nothing more", o)
        e = "Write each group after the millions as three digits. %s Fill every empty place with 0: %s." % (grp, n(x))
        Dw.append(mcq_n("Which number is <b>%s</b>?" % words(x), x, zero_mistakes(x) + [joined_digits(x)], e))
    Ew = []
    for x in [30500200, 704006000]:                            # numeral -> words (2)
        used.add(x)
        wr = [words(v) for v in zero_mistakes(x) if ndig(v) == ndig(x)][:3]
        m, r = divmod(x, 10 ** 6)
        t, o = divmod(r, 1000)
        e = ("Split %s into groups of three: %d million, %d thousand and %d. Say each group, then its name: %s."
             % (n(x), m, t, o, words(x)))
        Ew.append(mcq("How do you write %s in words?" % n(x), words(x), wr, e))
    G = []
    a, b = 99870000, 102300000
    G.append(mcq("Which is true?", "%s &lt; %s" % (n(a), n(b)),
                 ["%s &gt; %s" % (n(a), n(b)), "%s = %s" % (n(a), n(b)), "%s &lt; %s" % (n(b), n(a))],
                 "%s has 8 digits and %s has 9 digits, so %s is greater. A big first digit does not matter "
                 "when a number has fewer digits." % (n(a), n(b), n(b))))
    nums = [508090000, 580009000, 508900000, 99800000]
    assert max(nums) == 580009000
    G.append(mcq("Which number is the greatest?", n(580009000), [n(v) for v in nums if v != 580009000],
                 "99 800 000 has only 8 digits, so it is the least. The others start with 5 hundred millions. "
                 "Compare the ten millions: 8 &gt; 0. So 580 009 000 is the greatest."))
    assert 49600000 + 10 ** 6 == 50600000
    G.append(mcq_n("What is 1 000 000 more than 49 600 000?", 50600000, [49700000, 59600000, 49601000],
                   "Add 1 to the millions digit: 9 millions + 1 = 10 millions. Regroup them as 1 ten million: "
                   "4 + 1 = 5 ten millions. 49 600 000 + 1 000 000 = 50 600 000."))
    assert 302450000 - 10 ** 7 == 292450000
    G.append(mcq_n("What is 10 000 000 less than 302 450 000?", 292450000, [301450000, 202450000, 312450000],
                   "There are 0 ten millions, so regroup 1 hundred million as 10 ten millions. 10 − 1 = 9 ten "
                   "millions and 2 hundred millions are left. 302 450 000 − 10 000 000 = 292 450 000."))
    G.append(mcq_n("How many millions are there in one billion?", 1000, [100, 10000, 1000000],
                   "1 000 000 000 ÷ 1 000 000 = 1000. One thousand millions make one billion."))
    assert 7 * 10 ** 8 // (7 * 10 ** 5) == 1000
    G.append(mcq_n("In 777 777 777, the 7 in the hundred millions place is worth how many times the 7 in the "
                   "hundred thousands place?", 1000, [3, 100, 10000],
                   "700 000 000 ÷ 700 000 = 1000. The places are 3 places apart, and each place is worth 10 times "
                   "the place to its right: 10 × 10 × 10 = 1000, not 3."))
    its = A[:3] + Bv[:2] + C + Dw[:2] + [G[0]] + A[3:] + Bv[2:] + [Dw[2]] + Ew + [G[1], G[2], G[3], G[4], G[5]]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Read and write numbers to one billion", "items": its}


# ============================================================ set 2: place value and powers of ten
def set_tens(rnd, used):
    its = []
    its.append(mcq_n("%s = ?" % B(pw(10, 3)), 1000, [30, 100, 10000],
                     "%s = 10 × 10 × 10 = 1000. The exponent 3 gives 3 zeros. It is not 10 × 3 = 30." % pw(10, 3)))
    its.append(mcq_n("%s = ?" % B(pw(10, 5)), 100000, [50, 10000, 1000000],
                     "%s = 10 × 10 × 10 × 10 × 10 = 100 000: a 1 followed by 5 zeros." % pw(10, 5)))
    its.append(mcq_n("%s = ?" % B(pw(10, 6)), 1000000, [10000000, 100000, 60],
                     "%s is a 1 followed by 6 zeros: 1 000 000, one million. 10 000 000 has 7 zeros, so it is %s."
                     % (pw(10, 6), pw(10, 7))))
    its.append(mcq("How many zeros does %s have when you write it as a number?" % B(pw(10, 7)), "7", ["8", "6", "70"],
                   "The exponent tells how many 10s are multiplied, and each 10 adds one zero: %s = 10 000 000 "
                   "has 7 zeros. Do not count the 1 as a zero." % pw(10, 7)))
    its.append(mcq("Which power of ten is equal to 10 000?", pw(10, 4), [pw(10, 5), pw(10, 3), pw(4, 10)],
                   "10 000 = 10 × 10 × 10 × 10 = %s. Count the zeros (4), not all the digits (5)." % pw(10, 4)))
    its.append(mcq("Which power of ten is equal to one million?", pw(10, 6), [pw(10, 7), pw(10, 5), pw(10, 9)],
                   "One million = 1 000 000 has 6 zeros, so it is %s. %s is one billion." % (pw(10, 6), pw(10, 9))))
    its.append(mcq_n("%s = ?" % B(pw(10, 9)), 10 ** 9, [10 ** 8, 10 ** 10, 90],
                     "%s is a 1 followed by 9 zeros: 1 000 000 000, one billion. It is not 10 × 9 = 90." % pw(10, 9)))
    its.append(mcq("How many zeros are there in one billion written as a number?", "9", ["10", "8", "6"],
                   "One billion = 1 000 000 000 = %s. There are three groups of 000 after the 1: 9 zeros. "
                   "One million has 6 zeros." % pw(10, 9)))
    for i, k in [(5, 0), (7, 1)]:                               # HTO chart: which power
        x = distinct9(rnd, used, i)
        its.append(mcq(fig(chart_svg(x, hi=i)) + "Which power of ten is the place value of the red digit?",
                       pw(10, i), [pw(10, i + 1), pw(10, i - 1), pw(i, 10)],
                       "The red digit is in the %s place. One %s = %s = %s. There are %d places to its right, "
                       "so the exponent is %d. Do not count the digit itself."
                       % (PL[i], PL1[i], n(10 ** i), pw(10, i), i, i)))
    for i in [5, 8]:                                            # powers chart: value
        x = distinct9(rnd, used, i)
        d = digit(x, i)
        its.append(mcq_n(fig(chart_svg(x, hi=i, powers=True)) + "What is the value of the red digit?", d * 10 ** i,
                         [d * 10 ** (i - 1), d * 10 ** (i + 1), d * i, d * 10 ** (i - 2)],
                         "The red %d is under %s, so its value is %s = %d × %s = %s. It is not %d × %d = %d." %
                         (d, pw(10, i), tms(d, i), d, n(10 ** i), n(d * 10 ** i), d, i, d * i)))
    x = 527160384
    assert digit(x, 7) == 2 and str(x).index("7") == 2
    its.append(mcq("In 527 160 384, which power of ten is the place value of the digit 7?", pw(10, 6),
                   [pw(10, 7), pw(10, 5), pw(7, 10)],
                   "5 2 <b>7</b> | 1 6 0 | 3 8 4: the 7 is in the millions place, and one million = %s. "
                   "%s would be the ten millions place." % (pw(10, 6), pw(10, 7))))
    its.append(mcq_n("%s is how many times as much as %s?" % (B(pw(10, 6)), B(pw(10, 3))), 1000, [2, 3, 100],
                     "1 000 000 ÷ 1000 = 1000 = %s. Do not divide the exponents (6 ÷ 3 = 2)." % pw(10, 3)))
    its.append(mcq_n("How many hundreds are there in one million?", 10000, [1000, 100000, 100],
                     "1 000 000 ÷ 100 = 10 000. Taking away 2 zeros from 6 zeros leaves 4 zeros: %s." % pw(10, 4)))
    assert 10 * 10 ** 4 == 10 ** 5
    its.append(mcq("Which power is equal to 10 × %s?" % pw(10, 4), pw(10, 5), [pw(100, 4), pw(20, 4), pw(10, 4)],
                   "%s = 10 × 10 × 10 × 10. One more 10 makes five 10s: 10 × %s = %s = 100 000. "
                   "%s is far too big: it multiplies 100 by itself 4 times." % (pw(10, 4), pw(10, 4), pw(10, 5), pw(100, 4))))
    assert 6 * 10 ** 4 == 60000
    its.append(mcq_n("%s = ?" % B(tms(6, 4)), 60000, [6000, 600000, 24],
                     "%s = 10 000, so 6 × 10 000 = 60 000. Multiplying by %s puts 4 zeros after the 6. "
                     "It is not 6 × 4." % (pw(10, 4), pw(10, 4))))
    assert 45 * 10 ** 3 == 45000
    its.append(mcq_n("%s = ?" % B(tms(45, 3)), 45000, [4500, 450000, 135],
                     "%s = 1000, so 45 × 1000 = 45 000. Each digit moves 3 places to the left." % pw(10, 3)))
    its.append(mcq("Which is equal to 2 000 000?", tms(2, 6), [tms(2, 7), tms(2, 5), pw(2, 6)],
                   "2 000 000 = 2 × 1 000 000, and 1 000 000 = %s. So 2 000 000 = %s. %s = 64." %
                   (pw(10, 6), tms(2, 6), pw(2, 6))))
    assert 307 * 10 ** 4 == 3070000
    its.append(mcq_n("%s = ?" % B(tms(307, 4)), 3070000, [307000, 30700000, 1228],
                     "Multiplying by %s = 10 000 puts 4 zeros after 307: 3 070 000. "
                     "Keep the 0 inside 307. It is not 307 × 4 = 1228." % pw(10, 4)))
    order = [0, 1, 4, 3, 2, 5, 6, 7, 8, 10, 9, 11, 16, 15, 12, 13, 14, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20
    return {"title": "Place value and powers of ten", "items": its}


# ============================================================ set 3: exponential notation
def set_notation():
    its = []
    for b, e in [(4, 3), (6, 5), (7, 4), (3, 6), (10, 6)]:
        prod = " × ".join([str(b)] * e)
        good = pw(b, e)
        assert len({b ** e, e ** b, b ** (e - 1), b * e}) == 4
        its.append(mcq("Which power means %s?" % B(prod), good, [pw(e, b), pw(b, e - 1), "%d × %d" % (b, e)],
                       "%d is used as a factor %d times, so the base is %d and the exponent is %d: %s. "
                       "Count the factors, not the × signs (there %s only %d × sign%s)."
                       % (b, e, b, e, good, "is" if e == 2 else "are", e - 1, "" if e == 2 else "s")))
    for b, e in [(2, 5), (5, 4), (9, 3)]:
        good = " × ".join([str(b)] * e)
        swap = " × ".join([str(e)] * b)
        short = " × ".join([str(b)] * (e - 1))
        times = "%d × %d" % (b, e)
        its.append(mcq("Which means the same as %s?" % B(pw(b, e)), good, [times, swap, short],
                       "The exponent %d says to use the base %d as a factor %d times: %s = %s. It does not mean "
                       "%s = %d." % (e, b, e, pw(b, e), good, times, b * e)))
    its.append(mcq("In %s, which number is the base?" % B(pw(6, 4)), "6", ["4", "24", n(1296)],
                   "The base is the number that is multiplied: 6. The small raised 4 is the exponent. "
                   "%s = 6 × 6 × 6 × 6 = 1296 is the value." % pw(6, 4)))
    its.append(mcq("In %s, which number is the exponent?" % B(pw(3, 7)), "7", ["3", "21", n(2187)],
                   "The exponent is the small raised number: 7. It tells you to use the base 3 as a factor 7 times."))
    its.append(mcq("In %s, what does the exponent 8 tell you?" % B(pw(5, 8)), "Use 5 as a factor 8 times",
                   ["Multiply 5 by 8", "Use 8 as a factor 5 times", "Add 5 eight times"],
                   "The exponent tells how many times the base is used as a factor: %s = 5 × 5 × 5 × 5 × 5 × 5 × 5 × 5. "
                   "It is not 5 × 8." % pw(5, 8)))
    its.append(mcq("How do you read %s?" % B(pw(9, 2)), "9 squared", ["9 cubed", "9 times 2", "2 to the 9th power"],
                   "An exponent of 2 is read “squared”, because %s is the area of a square with sides of 9. "
                   "“Cubed” is for an exponent of 3." % pw(9, 2)))
    its.append(mcq("Which power is “8 cubed”?", pw(8, 3), [pw(3, 8), "8 × 3", pw(8, 2)],
                   "“Cubed” means an exponent of 3: %s = 8 × 8 × 8 = 512. It is not 8 × 3 = 24." % pw(8, 3)))
    its.append(mcq("How do you read %s?" % B(pw(2, 6)), "2 to the 6th power",
                   ["6 to the 2nd power", "2 times 6", "2 cubed"],
                   "Read the base first, then the exponent: %s is “2 to the 6th power”. "
                   "It means 2 × 2 × 2 × 2 × 2 × 2 = 64." % pw(2, 6)))
    its.append(mcq("Which power shows “7 used as a factor 5 times”?", pw(7, 5), [pw(5, 7), "7 × 5", pw(7, 4)],
                   "The base is the factor, 7. The exponent is how many times it is used, 5: %s." % pw(7, 5)))
    its.append(mcq(fig(square_svg(7)) + "The square is 7 units long on each side. Which power shows how many unit "
                   "squares cover it?", pw(7, 2), [pw(2, 7), "7 × 2", pw(7, 3)],
                   "7 rows of 7 squares: 7 × 7 = %s = 49 unit squares. That is why an exponent of 2 is called "
                   "“squared”." % pw(7, 2)))
    its.append(mcq(fig(cube_svg(4)) + "The cube is made of unit cubes, 4 on each edge. Which power shows how many "
                   "unit cubes make it?", pw(4, 3), [pw(4, 2), pw(3, 4), "4 × 3"],
                   "Each layer has 4 × 4 cubes and there are 4 layers: 4 × 4 × 4 = %s = 64. That is why an exponent "
                   "of 3 is called “cubed”. %s = 16 counts only one face." % (pw(4, 3), pw(4, 2))))
    for (a, m), (b, k) in [((2, 3), (5, 2)), ((3, 4), (7, 2))]:
        prod = " × ".join([str(a)] * m + [str(b)] * k)
        good = "%s × %s" % (pw(a, m), pw(b, k))
        bad = ["%s + %s" % (pw(a, m), pw(b, k)), "%s × %s" % (pw(a, k), pw(b, m)), pw(a * b, m + k)]
        its.append(mcq("Which shows %s using exponents?" % B(prod), good, bad,
                       "There are %d factors of %d and %d factors of %d, so the expression is %s. "
                       "The factors are multiplied, so use ×, not +." % (m, a, k, b, good)))
    prod = "2 × 2 × 3 × 2 × 3 × 3 × 2 × 2"
    assert prod.count("2") == 5 and prod.count("3") == 3
    its.append(mcq("Which shows %s using exponents?" % B(prod), "%s × %s" % (pw(2, 5), pw(3, 3)),
                   ["%s × %s" % (pw(2, 4), pw(3, 3)), "%s + %s" % (pw(2, 5), pw(3, 3)), pw(6, 8)],
                   "The order of factors does not matter when you multiply. Count each one: five 2s and three 3s. "
                   "So the product is %s × %s." % (pw(2, 5), pw(3, 3))))
    order = [5, 0, 1, 8, 9, 10, 11, 12, 13, 14, 2, 6, 15, 3, 7, 16, 4, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Exponential notation", "items": its}


# ============================================================ set 4: evaluate powers
def chain(b, e):
    return " × ".join([str(b)] * e)


def set_evaluate():
    its = []
    for b, e, wrong, why in [
        (2, 5, [10, 25, 16], "Not 10: that is 2 × 5. Not 25: that is %s." % pw(5, 2)),
        (3, 4, [12, 64, 27], "Not 12: that is 3 × 4. Not 27: that uses only three 3s."),
        (4, 3, [12, 81, 16], "Not 12: that is 4 × 3. Not 81: that is %s." % pw(3, 4)),
        (6, 2, [12, 64, 216], "Not 12: that is 6 × 2 or 6 + 6."),
        (5, 3, [15, 243, 25], "Not 15: that is 5 × 3. Not 25: that uses only two 5s."),
        (7, 2, [14, 128, 343], "Not 14: that is 7 × 2. Not 343: that is %s." % pw(7, 3)),
        (2, 7, [14, 49, 64], "Not 14: that is 2 × 7. Not 49: that is %s." % pw(7, 2)),
        (1, 9, [9, 10, 0], "1 times 1 is always 1, so every power of 1 is 1. Not 9: that is 1 × 9."),
        (9, 3, [27, 81, 6561], "Not 27: that is 9 × 3. Not 81: that uses only two 9s."),
        (3, 5, [15, 125, 81], "Not 15: that is 3 × 5. Not 125: that is %s." % pw(5, 3)),
        (2, 10, [20, 100, 512], "Not 20: that is 2 × 10. Not 100: that is %s." % pw(10, 2)),
        (12, 2, [24, 14, 1728], "Not 24: that is 12 × 2. Not 1728: that is %s." % pw(12, 3)),
    ]:
        v = b ** e
        assert v not in wrong
        steps = chain(b, e)
        if e > 3 and b > 1:
            run, parts = b, [str(b)]
            for _ in range(e - 1):
                run *= b
                parts.append(n(run))
            steps += " (" + " → ".join(parts) + ")"
        its.append(mcq("Evaluate %s." % B(pw(b, e)), n(v), [n(w) for w in wrong],
                       "%s = %s = %s. %s" % (pw(b, e), steps, n(v), why)))
    its.append(mcq_n(fig(cube_svg(5)) + "The cube is made of unit cubes, 5 on each edge. How many unit cubes make "
                     "the cube?", 125, [25, 15, 61],
                     "%s = 5 × 5 × 5 = 125. Not 25: that is only one face. Not 61: that counts only the cubes you "
                     "can see." % pw(5, 3)))
    assert 5 ** 3 - 4 ** 3 == 61
    assert 2 ** 5 > 5 ** 2
    its.append(mcq("Compare %s and %s." % (B(pw(2, 5)), B(pw(5, 2))), "%s &gt; %s" % (pw(2, 5), pw(5, 2)),
                   ["%s &lt; %s" % (pw(2, 5), pw(5, 2)), "%s = %s" % (pw(2, 5), pw(5, 2)), "You can’t tell"],
                   "%s = 32 and %s = 25. So %s &gt; %s. Swapping the base and the exponent changes the value."
                   % (pw(2, 5), pw(5, 2), pw(2, 5), pw(5, 2))))
    vals = {(2, 7): 128, (5, 3): 125, (3, 4): 81, (4, 3): 64}
    for (b, e), v in vals.items():
        assert b ** e == v
    its.append(mcq("Which power has the greatest value?", pw(2, 7), [pw(5, 3), pw(3, 4), pw(4, 3)],
                   "%s = 128, %s = 125, %s = 81, %s = 64. The greatest is %s, even though its base is the smallest."
                   % (pw(2, 7), pw(5, 3), pw(3, 4), pw(4, 3), pw(2, 7))))
    assert 2 ** 6 == 64
    its.append(mcq("2<sup>☐</sup> = 64. Which exponent goes in the box?", "6", ["32", "8", "5"],
                   "Keep multiplying by 2 and count the 2s: 2, 4, 8, 16, 32, 64. That is six 2s, so %s = 64. "
                   "Not 32: 2 × 32 = 64 is not a power. Not 8: 8 × 8 = 64 is %s." % (pw(2, 6), pw(8, 2))))
    assert 4 ** 3 == 64 and 8 ** 2 == 64
    its.append(mcq("☐<sup>3</sup> = 64. Which number goes in the box?", "4", ["8", "2", "16"],
                   "Try cubes: %s = 8, %s = 27, %s = 4 × 4 × 4 = 64. Not 8: %s = 64, but %s = 512. "
                   "Not 2: %s = 64." % (pw(2, 3), pw(3, 3), pw(4, 3), pw(8, 2), pw(8, 3), pw(2, 6))))
    assert 2 ** 3 * 5 == 40
    its.append(mcq_n("Evaluate %s." % B("%s × 5" % pw(2, 3)), 40, [1000, 30, 13],
                     "Evaluate the power first: %s = 8. Then 8 × 5 = 40. Not 1000: that is (2 × 5)<sup>3</sup>. "
                     "Not 30: that is 2 × 3 × 5." % pw(2, 3)))
    assert 2 ** 4 + 3 ** 2 == 25
    its.append(mcq_n("Evaluate %s." % B("%s + %s" % (pw(2, 4), pw(3, 2))), 25, [14, 17, 22],
                     "%s = 16 and %s = 9, so 16 + 9 = 25. Not 14: that is 2 × 4 + 3 × 2. "
                     "Not 17: that uses 2 × 4 = 8 for %s." % (pw(2, 4), pw(3, 2), pw(2, 4))))
    assert 5 ** 2 - 2 ** 3 == 17
    its.append(mcq_n("Evaluate %s." % B("%s − %s" % (pw(5, 2), pw(2, 3))), 17, [4, 33, 19],
                     "%s = 25 and %s = 8, so 25 − 8 = 17. Not 4: that is 5 × 2 − 2 × 3. "
                     "Not 19: that uses 2 × 3 = 6 for %s." % (pw(5, 2), pw(2, 3), pw(2, 3))))
    order = [0, 3, 1, 2, 5, 4, 7, 6, 12, 13, 8, 9, 14, 10, 11, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Evaluate powers", "items": its}


# ============================================================ set 5: expanded form and word problems
def ev(expr):
    return value(expr)


def set_words():
    its = []
    # 1 expanded -> number
    x = 7040500
    assert ev(expanded(x)) == x
    its.append(mcq_n("What number is %s?" % B(expanded(x)), x, [70405000, 7405000, 704050],
                     "%s = 7 000 000, %s = 40 000 and %s = 500. Add them and keep 0s in the empty places: "
                     "7 040 500." % (tms(7, 6), tms(4, 4), tms(5, 2))))
    # 2 expanded -> number
    x = 45300000
    assert ev(expanded(x)) == x
    its.append(mcq_n("What number is %s?" % B(expanded(x)), x, [4530000, 453000000, 453],
                     "%s = 40 000 000, %s = 5 000 000 and %s = 300 000. Together: 45 300 000."
                     % (tms(4, 7), tms(5, 6), tms(3, 5))))
    # 3 number -> expanded
    x = 3080600
    good = expanded(x)
    bad = [tms(3, 7) + " + " + tms(8, 5) + " + " + tms(6, 3), tms(3, 6) + " + " + tms(8, 5) + " + " + tms(6, 4),
           tms(3, 6) + " + " + tms(8, 3) + " + " + tms(6, 2)]
    assert ev(good) == x
    its.append(mcq("Which is 3 080 600 in expanded form with powers of ten?", good, bad,
                   "3 is in the millions place (%s), 8 is in the ten thousands place (%s) and 6 is in the hundreds "
                   "place (%s). The exponent is the number of places after the digit, not the number of digits."
                   % (pw(10, 6), pw(10, 4), pw(10, 2))))
    # 4 number -> expanded
    x = 900006000
    good = expanded(x)
    bad = [tms(9, 9) + " + " + tms(6, 4), tms(9, 8) + " + " + tms(6, 4), tms(9, 7) + " + " + tms(6, 3)]
    assert ev(good) == x and good == tms(9, 8) + " + " + tms(6, 3)
    its.append(mcq("Which is 900 006 000 in expanded form with powers of ten?", good, bad,
                   "900 006 000 = 900 000 000 + 6000. 900 000 000 has 8 places after the 9, so it is %s. "
                   "6000 has 3 places after the 6, so it is %s." % (tms(9, 8), tms(6, 3))))
    # 5 missing part
    x = 62015000
    assert ev(expanded(x)) == x and expanded(x) == " + ".join([tms(6, 7), tms(2, 6), tms(1, 4), tms(5, 3)])
    its.append(mcq("62 015 000 = %s + %s + ☐ + %s. What goes in the box?" % (tms(6, 7), tms(2, 6), tms(5, 3)),
                   tms(1, 4), [tms(1, 5), tms(1, 3), tms(1, 6)],
                   "62 015 000: the 1 is in the ten thousands place, worth 10 000 = %s. So the missing part is %s."
                   % (pw(10, 4), tms(1, 4))))
    # 6 Ottawa words
    x = 1017449
    wr = [words(v) for v in [1170449, 1007449, 117449]]
    its.append(mcq("At the 2021 census, Ottawa had a population of 1 017 449. How do you say this number in words?",
                   words(x), wr,
                   "Split it into groups: 1 | 017 | 449. One million, seventeen thousand, four hundred forty-nine. "
                   "The 0 means there are no hundred thousands."))
    # 7 Canada value of the 6
    x = 36991981
    assert digit(x, 6) == 6
    its.append(mcq_n("At the 2021 census, Canada had 36 991 981 people. What is the value of the 6?", 6000000,
                     [600000, 60000000, 6],
                     "36 991 981: the 6 is in the millions place, so it is worth 6 millions = 6 000 000 = %s." % tms(6, 6)))
    # 8 Toronto
    x = 2794356
    assert digit(x, 5) == 7
    its.append(mcq("At the 2021 census, the city of Toronto had 2 794 356 people. Which shows the value of the 7?",
                   tms(7, 5), [tms(7, 6), tms(7, 4), pw(7, 5)],
                   "2 794 356: the 7 is in the hundred thousands place, worth 700 000 = 7 × 100 000 = %s." % tms(7, 5)))
    # 9 Moon
    x = 384400
    wr = [words(v) for v in [384040, 38440, 3844000]]
    its.append(mcq("The average distance from Earth to the Moon is 384 400 km. How do you say this number in words?",
                   words(x) + " kilometres", [w + " kilometres" for w in wr],
                   "Split it into groups: 384 | 400. Three hundred eighty-four thousand, four hundred."))
    # 10 provinces order
    pops = [("Ontario", 14223942), ("Quebec", 8501833), ("British Columbia", 5000879), ("Alberta", 4262635)]
    right = ", ".join(p for p, _ in sorted(pops, key=lambda t: -t[1]))
    wrongs = ["Quebec, British Columbia, Alberta, Ontario", "Quebec, Ontario, British Columbia, Alberta",
              "Ontario, Quebec, Alberta, British Columbia"]
    assert right == "Ontario, Quebec, British Columbia, Alberta" and right not in wrongs
    its.append(mcq("At the 2021 census, the populations were: Alberta 4 262 635, British Columbia 5 000 879, "
                   "Ontario 14 223 942, Quebec 8 501 833. Which list goes from greatest to least?", right, wrongs,
                   "Ontario has 8 digits, so it is the greatest, even though it starts with 1. The others have 7 digits: "
                   "8 millions &gt; 5 millions &gt; 4 millions."))
    # 11 difference
    a, b = 14223942, 8501833
    assert a - b == 5722109
    its.append(mcq_n("At the 2021 census, Ontario had 14 223 942 people and Quebec had 8 501 833. How many more "
                     "people lived in Ontario?", 5722109, [6722109, 22725775, 14322111],
                     "14 223 942 − 8 501 833 = 5 722 109. Regroup carefully: 14 millions − 8 millions − 1 (borrowed) "
                     "= 5 millions. Not 14 322 111: that takes the smaller digit from the larger one in each column. "
                     "Not 22 725 775: that adds the numbers.", " people"))
    # 12 Canada area rounding
    x = 9984670
    assert (x + 500000) // 10 ** 6 * 10 ** 6 == 10 ** 7
    its.append(mcq("Canada’s area is 9 984 670 km². What is this rounded to the nearest million square kilometres?",
                   n(10 ** 7) + " km²", [n(9000000) + " km²", n(9980000) + " km²", n(9900000) + " km²"],
                   "9 984 670 is between 9 000 000 and 10 000 000. The hundred thousands digit is 9, so round up. "
                   "9 millions + 1 = 10 millions: 10 000 000 = %s. 9 000 000 just cuts off the digits." % pw(10, 7)))
    # 13 Sun
    assert 15 * 10 ** 7 == 150000000
    its.append(mcq("The Sun is about 150 000 000 km from Earth. Which shows this distance?",
                   tms(15, 7) + " km", [tms(15, 8) + " km", tms(15, 6) + " km", tms(15, 9) + " km"],
                   "150 000 000 = 15 × 10 000 000. 10 000 000 has 7 zeros, so it is %s. Count only the zeros after 15."
                   % pw(10, 7)))
    # 14 $100 bills
    assert 10 ** 6 // 100 == 10 ** 4
    its.append(mcq_n("How many $100 bills make one million dollars?", 10000, [1000, 100000, 100],
                     "$1 000 000 ÷ $100 = 10 000. One million has 6 zeros and 100 has 2, so the answer has 4 zeros: "
                     "%s bills." % pw(10, 4), " bills"))
    # 15 paper folding
    assert 2 ** 5 == 32
    its.append(mcq_n("Arjun folds a sheet of paper in half, then in half again, 5 times in all. Each fold doubles the "
                     "number of layers. How many layers are there now?", 32, [10, 25, 16],
                     "Each fold multiplies the layers by 2: 2 × 2 × 2 × 2 × 2 = %s = 32. "
                     "Not 10: that is 2 × 5. Not 16: that is only 4 folds." % pw(2, 5), " layers"))
    # 16 cells
    assert 2 ** 6 == 64
    its.append(mcq_n(fig(doubling_svg()) + "In a science video, a cell splits into 2 cells every hour, as shown. "
                     "Starting with 1 cell, how many cells are there after 6 hours?", 64, [12, 32, 36],
                     "The number doubles 6 times: %s = 2 × 2 × 2 × 2 × 2 × 2 = 64. Not 12: that is 2 × 6. "
                     "Not 32: that is 5 hours. Not 36: that is %s." % (pw(2, 6), pw(6, 2)), " cells"))
    # 17 phone tree
    assert 3 ** 4 == 81
    its.append(mcq_n("On a snow day, the principal calls 3 parents. Each of them calls 3 more parents, and so on. "
                     "How many parents get a call in the 4th round of calls?", 81, [12, 27, 64],
                     "Round 1: 3. Round 2: 3 × 3 = 9. Round 3: 27. Round 4: 81. That is %s = 81. "
                     "Not 12: that is 3 × 4. Not 64: that is %s." % (pw(3, 4), pw(4, 3)), " parents"))
    # 18 rink
    assert 30 ** 2 == 900
    its.append(mcq_n("An outdoor skating rink is a square, 30 m on each side. Its area is %s m². What is its area?"
                     % pw(30, 2), 900, [60, 120, 90],
                     "%s = 30 × 30 = 900 m². Not 60: that is 30 × 2. Not 120: that is the perimeter. "
                     "Not 90: 3 × 3 = 9, and 30 × 30 needs two zeros." % pw(30, 2), " m²"))
    # 19 cube box
    assert 10 ** 3 == 1000
    its.append(mcq_n("A box is a cube with edges of 10 cm. Its volume is %s cm³. What is its volume?" % pw(10, 3),
                     1000, [30, 100, 10000],
                     "%s = 10 × 10 × 10 = 1000 cm³. Not 30: that is 10 × 3. Not 100: that is only one layer, %s."
                     % (pw(10, 3), pw(10, 2)), " cm³"))
    # 20 light
    assert 300000 * 1000 == 3 * 10 ** 8
    its.append(mcq_n("Light travels about 300 000 km in one second. About how far does it travel in 1000 seconds?",
                     300000000, [30000000, 3000000000, 301000],
                     "300 000 = %s and 1000 = %s. 300 000 × 1000 adds 3 more zeros: 300 000 000 km = %s. "
                     "Not 301 000: that adds instead of multiplying." % (tms(3, 5), pw(10, 3), tms(3, 8)), " km"))
    order = [0, 1, 2, 4, 3, 6, 7, 5, 8, 18, 14, 13, 17, 16, 15, 12, 9, 10, 11, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Expanded form and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>Numbers to one billion</h2>"
        "<p>Big numbers are split into groups of three digits: <b>millions</b>, <b>thousands</b> and <b>ones</b>. "
        "In Canada we leave a small space between the groups (45 300 000), not a comma. "
        "Each place is worth <b>10 times</b> the place to its right.</p>"
        "<figure class='sn-fig'>" + chart_svg(608040500, hi=8) +
        "<figcaption>608 040 500: the 6 is in the hundred millions place, so it is worth 600 000 000. "
        "The zeros hold the empty places.</figcaption></figure>"
        + ex("Words to digits", "Write six hundred eight million forty thousand five hundred in digits.",
             "Six hundred eight million → 608. Forty thousand → 040. Five hundred → 500.", "608 040 500")
        + "<p>One thousand millions make <b>one billion</b>: 1 000 000 000.</p>"
        "<h2>Exponents</h2>"
        "<p>An <b>exponent</b> is a short way to write repeated multiplication. The <b>base</b> is the factor. "
        "The exponent tells how many times the base is used as a factor.</p>"
        + ex("Read and evaluate", "What does 2<sup>5</sup> mean?",
             "2<sup>5</sup> = 2 × 2 × 2 × 2 × 2. Multiply step by step: 2, 4, 8, 16, 32.",
             "2<sup>5</sup> = 32 (not 2 × 5 = 10)")
        + "<p>An exponent of 2 is read “squared” and an exponent of 3 is read “cubed”.</p>"
        "<figure class='sn-fig'>" + square_and_cube_svg() +
        "<figcaption>3 squared is a 3 by 3 square: 9 unit squares. 3 cubed is a 3 by 3 by 3 cube: 27 unit cubes."
        "</figcaption></figure>"
        "<h2>Powers of ten</h2>"
        "<p>Every place value is a power of ten. The exponent tells how many zeros come after the 1.</p>"
        + table(["Power", "Number", "Name"], [
            [pw(10, 1), "10", "ten"],
            [pw(10, 2), "100", "hundred"],
            [pw(10, 3), "1000", "thousand"],
            [pw(10, 4), n(10 ** 4), "ten thousand"],
            [pw(10, 5), n(10 ** 5), "hundred thousand"],
            [pw(10, 6), n(10 ** 6), "million"],
            [pw(10, 7), n(10 ** 7), "ten million"],
            [pw(10, 8), n(10 ** 8), "hundred million"],
            [pw(10, 9), n(10 ** 9), "billion"],
        ])
        + "<h2>Expanded form with powers of ten</h2>"
        "<p>Write each non-zero digit times the power of ten for its place.</p>"
        "<figure class='sn-fig'>" + chart_svg(45300000, powers=True) +
        "<figcaption>The 4 is under 10<sup>7</sup>, the 5 under 10<sup>6</sup> and the 3 under 10<sup>5</sup>."
        "</figcaption></figure>"
        + ex("Expanded form", "Write 45 300 000 in expanded form with powers of ten.",
             "4 ten millions, 5 millions and 3 hundred thousands.", expanded(45300000))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["2<sup>5</sup> = 10 (base × exponent)", "Use 2 as a factor 5 times: 2<sup>5</sup> = 32"],
            ["2<sup>5</sup> = 5<sup>2</sup> (swapping)", "2<sup>5</sup> = 32 but 5<sup>2</sup> = 25"],
            ["10<sup>6</sup> has 7 zeros", "The exponent is the number of zeros: 1 000 000 has 6"],
            ["Missing a zero (two million seventy thousand nine → 270 009)", "Write each group as three digits: 2 | 070 | 009"],
            ["Giving the digit, not its value (the 6 in 608 040 500 is 6)", "It is in the hundred millions place: 600 000 000"],
            ["Comparing first digits only (99 870 000 &gt; 102 300 000)", "Count the digits first: 9 digits beat 8"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about exponents in the Ontario math curriculum?",
     "a": "In Grade 7 (Number, B2.7) students use exponents to write and evaluate repeated multiplication of whole "
          "numbers, such as 2⁵ = 2 × 2 × 2 × 2 × 2 = 32. They also work with whole numbers up to one billion and "
          "write them in expanded form with powers of ten (B1.1)."},
    {"q": "Is 2⁵ the same as 2 × 5?",
     "a": "No. 2⁵ means 2 is used as a factor 5 times: 2 × 2 × 2 × 2 × 2 = 32. 2 × 5 is only 10."},
    {"q": "How many zeros are in one million and one billion?",
     "a": "One million is 10⁶ = 1 000 000, with 6 zeros. One billion is 10⁹ = 1 000 000 000, with 9 zeros, "
          "and it is one thousand millions."},
    {"q": "How do you write a number in expanded form using powers of ten?",
     "a": "Multiply each non-zero digit by the power of ten for its place and add the parts. "
          "For example, 3 080 600 = 3 × 10⁶ + 8 × 10⁴ + 6 × 10²."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (45 300 000) everywhere outside SVG markup."""
    return "".join(p if p.startswith("<svg") else GAP.sub(NB, p) for p in SVG.split(s))


def fix_spaces(u):
    for k in ("title", "seo_title", "short_title", "meta_desc", "key_big", "key_sub", "body_html"):
        u[k] = nbsp(u[k])
    for f in u["faq"]:
        f["q"], f["a"] = nbsp(f["q"]), nbsp(f["a"])
    for s in u["sets"]:
        s["title"] = nbsp(s["title"])
        for it in s["items"]:
            it["q"], it["e"] = nbsp(it["q"]), nbsp(it["e"])
            it["c"] = [nbsp(c) for c in it["c"]]
    return u


def mark_large(u, pattern):
    """Tag wide pictures (place value charts) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(47801)
    used = set()
    sets = [set_billion(rnd, used), set_tens(rnd, used), set_notation(), set_evaluate(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "powers-and-large-numbers", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Powers and Large Numbers: Exponents, Powers of Ten and Numbers to One Billion",
        "seo_title": "Grade 7 Exponents and Large Numbers Worksheets: Powers of Ten to One Billion (Free, Answer Key)",
        "short_title": "Powers and large numbers",
        "domain": "Number",
        "standard_code": "Grade 7: B2.7",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Evaluate and express repeated multiplication of whole numbers using exponential notation, in various contexts",
        "meta_desc": "Free Grade 7 math worksheets for the Ontario curriculum: read and write numbers to one billion, "
                     "powers of ten, exponential notation, evaluating powers, and expanded form with powers of ten. "
                     "100 questions with an answer key.",
        "key_big": "An exponent tells how many times the base is used as a factor: 2⁵ = 2 × 2 × 2 × 2 × 2 = 32, not 2 × 5.",
        "key_sub": "Powers of ten build place value: 10³ = 1000, 10⁶ = one million (6 zeros), 10⁹ = one billion. "
                   "So 45 300 000 = 4 × 10⁷ + 5 × 10⁶ + 3 × 10⁵.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(fix_spaces(u), "place value chart")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
