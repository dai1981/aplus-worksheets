# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Roman Numerals to 100 (National Curriculum in England, Number and place value)
  python tools/gen_uk_maths_y4_roman_numerals.py
Numbers 1 to 100 only (I, V, X, L, C). Every value is checked in code.
Wrong answers come from real pupil mistakes: IIII for 4, XXXX for 40, IL for 49, VX for 5, LC for 50,
reading IX as 11 (adding every symbol), swapping IV and VI, writing 47 as IV VII.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
LINE = "#2b2b2b"
RED = "#d6453b"
GRAY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
MINUS = "−"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
PAIRS = [(100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


# ------------------------------------------------------------ Roman numerals
def roman(n):
    assert 1 <= n <= 399, n
    out = []
    for v, s in PAIRS:
        while n >= v:
            out.append(s)
            n -= v
    return "".join(out)


def value(s):
    """Standard reading: a smaller symbol before a bigger one is subtracted."""
    t = 0
    for i, ch in enumerate(s):
        v = VAL[ch]
        if i + 1 < len(s) and VAL[s[i + 1]] > v:
            t -= v
        else:
            t += v
    return t


def naive(s):
    """The mistake of adding every symbol (IX read as 11)."""
    return sum(VAL[ch] for ch in s)


def additive(n):
    """Writing without the subtraction rule: 4 = IIII, 40 = XXXX, 49 = XXXXVIIII."""
    out = []
    for v, s in [(100, "C"), (50, "L"), (10, "X"), (5, "V"), (1, "I")]:
        while n >= v:
            out.append(s)
            n -= v
    return "".join(out)


def swapped(n):
    """Putting the small symbol on the wrong side: IV -> VI, IX -> XI, XL -> LX, XC -> CX."""
    r = roman(n)
    for a, b in [("XC", "CX"), ("XL", "LX"), ("IX", "XI"), ("IV", "VI")]:
        r = r.replace(a, b)
    return r


def shortcut(n):
    """Subtracting from the next round number in one go: 49 = IL, 99 = IC, 45 = VL, 18 = XIIX."""
    for s, sym in [(1, "I"), (2, "II"), (5, "V")]:
        m = n + s
        if m % 10 == 0 and m <= 100 or m == 5:
            rm = roman(m)
            w = rm[:-1] + sym + rm[-1]
            if w != roman(n):
                return w
    return None


def digitwise(n):
    """Writing each digit with ones symbols: 47 -> IV VII = IVVII."""
    if n < 20 or n % 10 == 0 or n == 100:
        return None
    return roman(n // 10) + roman(n % 10)


def write_cands(n, extra=()):
    c = list(extra) + [shortcut(n), additive(n), swapped(n)]
    for d in (1, -1, 10, -10):
        if 1 <= n + d <= 100:
            c.append(roman(n + d))
    return c + [digitwise(n)]


def read_cands(r):
    """Numbers pupils give when they misread the numeral r."""
    n = value(r)
    c = [naive(r)]
    no_prefix = re.sub(r"I(?=[VX])|X(?=[LC])", "", r)        # ignoring the small symbol in IV, IX, XL, XC
    if no_prefix != r:
        c.append(value(no_prefix))
    if "II" in r or "IV" in r or "IX" in r:
        c += [n + 1, n - 1]
    if "XX" in r:
        c += [n + 10, n - 10]
    if "V" in r:
        c.append(n + 5)                                     # V mixed up with X
    if "L" in r:
        c.append(n + 50)                                    # L mixed up with C
    c += [n + 1, n - 1, n + 10, n - 10]
    return [v for v in c if v > 0 and v != n]


def chunk(v):
    """'XL = 50 − 10 = 40' or 'LXX = 50 + 10 + 10 = 70'."""
    r = roman(v)
    if r in ("IV", "IX", "XL", "XC"):
        return "%s = %d %s %d = %d" % (r, VAL[r[1]], MINUS, VAL[r[0]], v)
    if len(r) == 1:
        return "%s = %d" % (r, v)
    return "%s = %s = %d" % (r, " + ".join(str(VAL[ch]) for ch in r), v)


def parts(n):
    if n == 100:
        return [100]
    return [p for p in (n // 10 * 10, n % 10) if p]


def read_e(r):
    n = value(r)
    ps = parts(n)
    if len(ps) == 1:
        return "%s." % chunk(n)
    return "Split it into tens and ones: %s and %s. So %s = %d + %d = %d." % (chunk(ps[0]), chunk(ps[1]), r, ps[0], ps[1], n)


def write_e(n):
    ps = parts(n)
    if len(ps) == 1:
        return "%s, so %d = %s." % (chunk(n), n, roman(n))
    return "Partition %d into %d + %d. %d is %s and %d is %s. So %d = %s." % (
        n, ps[0], ps[1], ps[0], roman(ps[0]), ps[1], roman(ps[1]), n, roman(n))


NOTE = {
    4: " IIII is wrong: never write 4 of the same symbol in a row.",
    9: " VIIII is wrong: never write 4 of the same symbol in a row.",
    40: " XXXX is wrong: never write 4 Xs in a row.",
    90: " LXXXX is wrong: never write 4 Xs in a row.",
    45: " VL is not allowed: only I, X (and C) go before a bigger symbol, and only I before V or X.",
    49: " IL is not allowed: I can only go before V or X.",
    95: " VC is not allowed: V is never put before a bigger symbol.",
    99: " IC is not allowed: I can only go before V or X.",
}


def note(n):
    return NOTE.get(n, "")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
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
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [p for p in range(4) for _ in range(5)]
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def b(r):
    return "<b>%s</b>" % r


def ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "the %d%s" % (n, suf)


# ------------------------------------------------------------ pictures
HOURS = ["twelve", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven"]


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def say_time(h, m):
    nx = HOURS[(h + 1) % 12]
    hr = HOURS[h % 12]
    return {0: "%s o’clock" % hr, 15: "quarter past %s" % hr, 30: "half past %s" % hr,
            45: "quarter to %s" % nx}[m]


def clock_body(h, m, cx, cy, R):
    """Clock face with Roman numerals I to XII. The hour hand is placed by the exact time: (h + m/60) x 30 degrees."""
    k = R / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, R, GREEN, 5 * k)]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (10 if i % 5 == 0 else 6) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (R - 3 * k) * math.cos(a), cy + (R - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), LINE, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), LINE, 2.6 * k))
    if h is not None:
        ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
        am = math.radians(m * 6 - 90)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
                 % (cx, cy, cx + R * 0.48 * math.cos(ah), cy + R * 0.48 * math.sin(ah), LINE, 8 * k))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
                 % (cx, cy, cx + R * 0.84 * math.cos(am), cy + R * 0.84 * math.sin(am), RED, 4.5 * k))
    fs = 16 * k
    s.append("<g font-family='Georgia, serif' font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' "
             "stroke='#fff' stroke-width='%.1f' paint-order='stroke'>" % (fs, LINE, 3 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        rn = R - 30 * k
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, roman(n)))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200):
    assert h is None or hands_gap(h, m) >= 12, (h, m)
    c = size / 2.0
    label = "clock with Roman numerals" + (" showing %s" % say_time(h, m) if h is not None else "")
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6), label)


def symbols_svg():
    """The five symbols with their values."""
    W, H = 5 * 72 + 12, 104
    s = []
    for i, ch in enumerate("IVXLC"):
        x = 6 + i * 72
        s.append("<rect x='%d' y='6' width='64' height='54' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, FILL, GREEN))
        s.append("<text x='%d' y='45' font-family='Georgia, serif' font-size='30' font-weight='700' fill='%s' "
                 "text-anchor='middle'>%s</text>" % (x + 32, LINE, ch))
        s.append("<text x='%d' y='90' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                 % (x + 32, RED, VAL[ch]))
    return svg_wrap(W, H, "".join(s), "the symbols I, V, X, L and C with their values 1, 5, 10, 50 and 100")


def split_svg(n):
    """Numeral split into its tens part and ones part, with the value under each part."""
    ps = parts(n)
    boxes = [(roman(p), str(p)) for p in ps]
    widths = [max(64, 26 * len(r) + 24) for r, _ in boxes]
    gap = 40
    W = sum(widths) + gap * (len(boxes) - 1) + 12 + 90
    H = 112
    s = []
    x = 6
    for i, ((r, v), w) in enumerate(zip(boxes, widths)):
        s.append("<rect x='%d' y='6' width='%d' height='54' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, w, FILL, GREEN))
        s.append("<text x='%.1f' y='45' font-family='Georgia, serif' font-size='30' font-weight='700' fill='%s' "
                 "text-anchor='middle'>%s</text>" % (x + w / 2.0, LINE, r))
        s.append("<text x='%.1f' y='94' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + w / 2.0, RED, v))
        x += w
        if i < len(boxes) - 1:
            s.append("<text x='%.1f' y='94' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>+</text>"
                     % (x + gap / 2.0, LINE))
            x += gap
    s.append("<text x='%d' y='94' font-size='22' font-weight='700' fill='%s'>= %d</text>" % (x + 12, RED, n))
    return svg_wrap(W, H, "".join(s), "%s split into %s" % (roman(n), " and ".join(r for r, _ in boxes)))


# ============================================================ set 1: symbols and numbers to 20
def set_symbols():
    its = []
    for ch, wr in [("I", [10, 5, 50]), ("V", [10, 50, 1]), ("X", [5, 100, 1]), ("L", [100, 5, 500]), ("C", [50, "1,000", 10])]:
        e = "%s means %d." % (ch, VAL[ch])
        if ch == "L":
            e += " Do not mix it up with C, which means 100."
        if ch == "C":
            e += " C is the first letter of the Latin word centum, which means a hundred (think of a century)."
        if ch == "V":
            e += " Do not mix it up with X, which means 10."
        its.append(mcq("What number does %s stand for?" % b(ch), VAL[ch], wr, e))
    its.append(mcq("Which Roman numeral stands for 50?", "L", ["C", "V", "X"],
                   "L = 50. C = 100, X = 10 and V = 5."))
    its.append(mcq("Which Roman numeral means 5?", "V", ["VX", "IIIII", "X"],
                   "5 has its own symbol: V. VX is not a Roman numeral: V is never put before a bigger symbol. "
                   "IIIII uses 5 Is, but you never write more than 3 of the same symbol in a row."))
    # read numbers to 20 without subtraction (7)
    for n in [3, 7, 12, 15, 11, 18, 17]:
        r = roman(n)
        its.append(mcq("What number is %s?" % b(r), n, (["111"] if r == "III" else []) + read_cands(r), read_e(r) if n > 10 else
                       "%s = %s = %d." % (r, " + ".join(str(VAL[ch]) for ch in r), n)
                       + (" It is not 111: each I means 1, wherever it is." if r == "III" else "")))
    # write numbers to 20 without subtraction (6)
    for n in [6, 8, 12, 13, 16, 20]:
        ex_ = []
        if n == 8:
            ex_ = ["IIX", "VII", "VIIII"]
        if n == 20:
            ex_ = ["XXX", "XIX", "XXI"]
        if n == 12:
            ex_ = ["III", "XIII", "XI"]
        if n == 6:
            ex_ = ["IV", "VII", "IIIIII"]
        e = write_e(n) if n > 10 else "%d = %s, so %d = %s." % (n, " + ".join(str(VAL[ch]) for ch in roman(n)), n, roman(n))
        if n == 8:
            e += " IIX is wrong: you can only put one I before a bigger symbol."
        if n == 6:
            e += " IV is 4, because the I comes before the V."
        if n == 12:
            e += " III is only 3: the 1 ten must be written X."
        if n == 20:
            e = "20 = 10 + 10, so 20 = XX."
        its.append(mcq("Which Roman numeral is %d?" % n, roman(n), ex_ + write_cands(n), e))
    return {"title": "The symbols I, V, X, L, C and numbers to 20", "items": its}


# ============================================================ set 2: subtraction rule and reading to 100
def set_read():
    its = []
    for r in ["IV", "IX", "XIV", "XIX", "XL", "XC"]:
        n = value(r)
        e = read_e(r)
        if r in ("IV", "IX", "XL", "XC"):
            e += " A smaller symbol before a bigger one is taken away, so %s is not %d." % (r, naive(r))
        else:
            e += " The I comes before the bigger symbol, so take it away. %s is not %d." % (r, naive(r))
        its.append(mcq("What number is %s?" % b(r), n, read_cands(r), e))
    its.append(mcq("Which Roman numeral means 50?", "L", ["LC", "XXXXX", "C"],
                   "50 has its own symbol: L. LC is not allowed: L is never put before a bigger symbol. "
                   "C is 100, and XXXXX uses too many Xs."))
    for r in ["XXIV", "XXXVII", "XXXIX", "XLVI", "LIV", "LXIX", "LXXVIII", "LXXX", "LXXXIV", "XCII", "XLIX",
              "XCV", "XCIX"]:
        assert roman(value(r)) == r
        its.append(mcq("What number is %s?" % b(r), value(r), read_cands(r), read_e(r)))
    return {"title": "The subtraction rule: IV, IX, XL and XC", "items": its}


# ============================================================ set 3: writing numbers
def set_write():
    its = []

    def w(n, extra=()):
        its.append(mcq("Write %d in Roman numerals." % n, roman(n), write_cands(n, extra), write_e(n) + note(n)))

    def notright(ok, bad, why):
        for r in ok:
            assert roman(value(r)) == r
        its.append(mcq("Which Roman numeral is <b>not</b> written correctly?", bad, ok, why))

    def missing(n, start, extra):
        rest = roman(n)[len(start):]
        assert roman(n).startswith(start)
        its.append(mcq("Which symbols are missing? %d = %s ?" % (n, start), rest, extra,
                       "%d = %d + %d. %s = %d, so the missing part is %d = %s." % (
                           n, value(start), n - value(start), start, value(start), n - value(start), rest)))

    w(14, ["XVI"])
    w(19, ["XVIIII", "XXI"])
    w(27)
    w(40, ["XXXX", "LX"])
    missing(76, "LXX", ["IV", "VII", "IIIIII"])
    w(44, ["XXXXIIII", "XLVI"])
    w(47, ["XXXXVII", "IVVII", "LXVII"])
    notright(["XIV", "XL", "LX"], "IIII", "IIII is not correct: 4 is written IV. The others are correct: XIV = 14, XL = 40, LX = 60.")
    w(49, ["IL", "XXXXIX", "XLVIIII"])
    w(58)
    missing(38, "XXX", ["IIX", "VII", "VIIII"])
    w(66, ["LXIV"])
    notright(["XXX", "XLV", "XC"], "XXXX", "XXXX is not correct: 40 is written XL. The others are correct: XXX = 30, XLV = 45, XC = 90.")
    w(73)
    w(89, ["LXXXVIIII", "XIC"])
    w(90, ["LXXXX", "CX"])
    missing(94, "XC", ["IIII", "VI", "IX"])
    w(95, ["VC", "LXXXXV", "XCIV"])
    notright(["XLIX", "LI", "XIX"], "IL", "IL is not correct: I can only go before V or X. 49 is written XLIX. "
             "The others are correct: XLIX = 49, LI = 51, XIX = 19.")
    w(99, ["IC", "LXXXXVIIII", "XCVIIII"])
    return {"title": "Write numbers to 100 in Roman numerals", "items": its}


# ============================================================ set 4: compare, order and calculate
def set_calc():
    its = []
    for x, y in [("XL", "LX"), ("IX", "XI")]:
        vx, vy = value(x), value(y)
        right = "%s %s %s" % (x, "&lt;" if vx < vy else "&gt;", y)
        wrong = ["%s %s %s" % (x, "&gt;" if vx < vy else "&lt;", y), "%s = %s" % (x, y),
                 "%s %s %s" % (y, "&lt;" if vx < vy else "&gt;", x)]
        its.append(mcq("Which is true?", right, wrong,
                       "%s = %d and %s = %d. %d &lt; %d, so %s." % (x, vx, y, vy, min(vx, vy), max(vx, vy), right)))
    for lst, want in [(["XL", "XXXVIII", "XXXV", "XXIX"], max), (["LX", "XL", "LIV", "XLVIII"], max),
                      (["XC", "LXXXVIII", "LXXIX", "LXXXV"], max), (["VIII", "IX", "XI", "XII"], min)]:
        vals = [value(r) for r in lst]
        ans = lst[vals.index(want(vals))]
        word = "greatest" if want is max else "smallest"
        e = ", ".join("%s = %d" % (r, value(r)) for r in sorted(lst, key=value)) + ". %s is the %s." % (ans, word)
        if want is max and len(ans) < max(len(r) for r in lst):
            e += " A longer numeral is not always bigger."
        its.append(mcq("Which Roman numeral is the %s?" % word, ans, [r for r in lst if r != ans], e))
    for seq, nxt, wr in [(["XXXVI", "XXXVII", "XXXVIII"], "XXXIX", ["XXXVIIII", "XL", "XXXX"]),
                         (["XL", "L", "LX"], "LXX", ["LXL", "XC", "LXXX"])]:
        vs = [value(r) for r in seq]
        step = vs[1] - vs[0]
        assert vs[2] - vs[1] == step and value(nxt) == vs[2] + step
        its.append(mcq("What comes next? %s, ?" % ", ".join(seq), nxt, wr,
                       "%s. The numbers go up in %ss. %d + %d = %d = %s." % (
                           ", ".join("%s = %d" % (r, v) for r, v in zip(seq, vs)), step, vs[2], step, vs[2] + step, nxt)))
    for three, wrongs in [(["XIX", "XXI", "XVI"], [["XIX", "XVI", "XXI"], ["XVI", "XXI", "XIX"]]),
                          (["XL", "XXXV", "L"], [["XL", "XXXV", "L"], ["XL", "L", "XXXV"]])]:
        order = sorted(three, key=value)
        fmt = lambda l: ", ".join(l)
        perms = wrongs + [order[::-1]]
        e = ", ".join("%s = %d" % (r, value(r)) for r in order) + ". From smallest to largest: %s." % fmt(order)
        its.append(mcq("Which list is in order from smallest to largest?", fmt(order), [fmt(p) for p in perms], e))
    calcs = [("XXIV", "+", "VI"), ("XV", "+", "IX"), ("XL", "+", "X"), ("XXXV", "+", "XV"), ("L", MINUS, "I"),
             ("XC", MINUS, "X"), ("XIX", "+", "XXI"), ("LX", MINUS, "XV"), ("XLV", "+", "XLV"), ("C", MINUS, "I")]
    for x, op, y in calcs:
        f = (lambda a, c: a + c) if op == "+" else (lambda a, c: a - c)
        v = f(value(x), value(y))
        assert 1 <= v <= 100
        nv = f(naive(x), naive(y))
        cands = []
        if nv != v and 1 <= nv <= 300:
            cands.append(roman(nv))
        if op == "+":
            cands.append(x + y)                            # writing the two numerals side by side
        cands += write_cands(v)
        e = "%s = %d and %s = %d. %d %s %d = %d, and %d = %s." % (x, value(x), y, value(y), value(x), op, value(y), v, v, roman(v))
        e += note(v)
        its.append(mcq("Work out %s %s %s. Give the answer in Roman numerals." % (b(x), op, b(y)), roman(v), cands, e))
    return {"title": "Compare, order and calculate with Roman numerals", "items": its}


# ============================================================ set 5: real life
def set_life(P):
    its = []
    for h, m, wr in [(9, 0, ["eleven o’clock", "quarter to one", "twelve o’clock"]),
                     (4, 30, ["half past six", "half past five", "twenty past six"]),
                     (11, 15, ["quarter past nine", "quarter past twelve", "quarter to eleven"]),
                     (7, 45, ["quarter to nine", "quarter past eight", "quarter to seven"])]:
        hour_sym = roman(h if m < 45 else h % 12 + 1)
        if m == 0:
            e = "The minute hand (red) points to XII, so it is o’clock. The hour hand points to %s = %d. It is %s." % (
                roman(h), h, say_time(h, m))
        elif m == 30:
            e = ("The minute hand points to VI, which is half past. The hour hand is between %s (%d) and %s (%d), "
                 "so it is %s." % (roman(h), h, roman(h + 1), h + 1, say_time(h, m)))
        elif m == 15:
            e = ("The minute hand points to III, which is quarter past. The hour hand has just passed %s (%d), "
                 "so it is %s." % (roman(h), h, say_time(h, m)))
        else:
            e = ("The minute hand points to IX, which is quarter to. The hour hand is nearly at %s (%d), "
                 "so it is %s." % (hour_sym, h + 1, say_time(h, m)))
        e += {9: " Be careful: IX is 9, not 11.", 11: " Be careful: XI is 11, not 9.", 4: " Be careful: IV is 4, not 6."}.get(h, "")
        its.append(mcq(fig(clock_svg(h, m)) + "What time does this clock show?", say_time(h, m), wr, e))
    its.append(mcq("On a clock with Roman numerals, the minute hand points to VI. How many minutes past the hour is it?",
                   "30 minutes", ["6 minutes", "4 minutes", "20 minutes"],
                   "VI = 6. Each number on the clock is 5 minutes for the minute hand: 6 × 5 = 30 minutes. That is half past."))
    # monarchs
    its.append(mcq("King Henry VIII had six wives. Which King Henry was he?", ordinal(8),
                   [ordinal(7), ordinal(3), ordinal(13)],
                   "VIII = 5 + 1 + 1 + 1 = 8, so he was the 8th King Henry. We say “Henry the Eighth”."))
    its.append(mcq("Queen Elizabeth II’s father was King George VI. Which King George was he?", ordinal(6),
                   [ordinal(4), ordinal(11), ordinal(7)],
                   "VI = 5 + 1 = 6. The I comes after the V, so add it. IV would be 4."))
    its.append(mcq("King Louis XIV of France was king for 72 years. Which King Louis was he?", ordinal(14),
                   [ordinal(16), ordinal(4), ordinal(15)],
                   "XIV = X + IV = 10 + 4 = 14. The I is before the V, so it is taken away: XIV is not 16."))
    its.append(mcq("Charles III became king in 2022. If there is a king called Charles after him, how will his number be written?",
                   "IV", ["IIII", "VI", "IIV"],
                   "The next Charles will be the 4th. 4 = 5 − 1 = IV. IIII is wrong, and VI is 6."))
    # books and films
    name, she, her = P.next()
    its.append(mcq("%s’s book has chapters numbered from I to XXIV. How many chapters are there?" % name, "24",
                   ["26", "22", "25"],
                   "XXIV = XX + IV = 20 + 4 = 24. The I before the V is taken away, so it is not 26."))
    name, she, her = P.next()
    its.append(mcq("%s has just finished Chapter XIX. What is the number of the next chapter?" % name, "XX",
                   ["XXI", "XIXI", "XVIII"],
                   "XIX = 10 + 9 = 19. The next chapter is 20 = XX. XIXI is not a Roman numeral."))
    name, she, her = P.next()
    its.append(mcq("%s reads chapters XII to XV of a book. How many chapters does %s read?" % (name, she), "4",
                   ["3", "5", "27"],
                   "XII = 12 and XV = 15. The chapters are 12, 13, 14 and 15: that is 4 chapters. "
                   "15 − 12 = 3 forgets to count chapter 12."))
    its.append(mcq("The newest film in a series is film XIV. What will the next film be?", "XV",
                   ["XIVI", "XVI", "XIIII"],
                   "XIV = 14, so the next film is 15. 15 = 10 + 5 = XV. You cannot just add an I to the end of XIV."))
    # Romans in Britain
    its.append(mcq("Roman soldiers of the Ninth Legion built a fortress at York. How did the Romans write nine?", "IX",
                   ["VIIII", "XI", "IIX"],
                   "9 = 10 − 1, so put I before X: IX. XI is 11, and IIX is not allowed."))
    its.append(mcq("The Romans invaded Britain in the year AD 43. How do you write 43 in Roman numerals?", "XLIII",
                   ["XXXXIII", "IVIII", "LXIII"],
                   "43 = 40 + 3. 40 = XL (50 − 10) and 3 = III. So 43 = XLIII. LXIII would be 63."))
    its.append(mcq("A museum label says a Roman coin is from the year AD LXXIX, the year a volcano buried the town of Pompeii. "
                   "What year is that?", "AD 79", ["AD 81", "AD 69", "AD 71"],
                   read_e("LXXIX") + " The I before the X is taken away, so it is not 81."))
    # no zero, no place value
    its.append(mcq("Which Roman numeral stands for zero?", "There isn’t one", ["O", "I", "X"],
                   "The Romans had no symbol for zero. Our zero came later, from India, through Arabic mathematicians."))
    its.append(mcq("In the number 77, the two 7s have different values. In the Roman numeral XX, what is each X worth?",
                   "10 each", ["10 and 1", "20 and 10", "1 and 10"],
                   "Roman numerals do not use place value. X always means 10, wherever it is. XX = 10 + 10 = 20. "
                   "In 77 the first 7 is worth 70 because of its place."))
    its.append(mcq("We need a 0 to write 50. Why do Roman numerals never need a zero?",
                   "Each symbol has a fixed value", ["Romans only counted to 10", "Zero was written as O",
                                                     "Each symbol depends on its place"],
                   "In 50 the 0 holds the ones place, so the 5 stays in the tens. Roman numerals have no places: "
                   "L always means 50 and C always means 100, so 50 is just L, with no gap to fill."))
    its.append(mcq("Which number is much quicker to write with our digits than with Roman numerals?", "88",
                   ["10", "50", "100"],
                   "88 = LXXXVIII: 8 symbols. With digits it is just 2. 10 = X, 50 = L and 100 = C each need only 1 symbol."))
    return {"title": "Real life: clocks, kings and queens, books and Roman history", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    return (
        "<h2>Five symbols</h2>"
        "<p>Roman numerals use letters for numbers. To 100 you need only five of them.</p>"
        "<figure class='sn-fig'>" + symbols_svg() +
        "<figcaption>I = 1, V = 5, X = 10, L = 50, C = 100. C is for centum, the Latin word for a hundred.</figcaption></figure>"
        "<h2>Add or take away?</h2>"
        "<ol class='rk-step'>"
        "<li><b>Same or smaller symbol after:</b> add. VI = 5 + 1 = 6. LX = 50 + 10 = 60.</li>"
        "<li><b>Smaller symbol before a bigger one:</b> take it away. IV = 5 − 1 = 4. XL = 50 − 10 = 40.</li>"
        "<li><b>Never more than 3 of the same symbol in a row.</b> 4 is IV, not IIII. 40 is XL, not XXXX.</li></ol>"
        + table(["Take away", "Means", "Value"], [
            ["IV", "5 − 1", "4"], ["IX", "10 − 1", "9"], ["XL", "50 − 10", "40"], ["XC", "100 − 10", "90"],
        ]) +
        "<p>These four pairs are the only ones you need to 100. I goes only before V or X, and X goes only before L or C.</p>"
        "<h2>Read a Roman numeral</h2>"
        "<p>Split it into tens and ones, then add.</p>"
        "<figure class='sn-fig'>" + split_svg(47) +
        "<figcaption>XLVII = XL + VII = 40 + 7 = 47.</figcaption></figure>"
        + ex("Read", "What number is LXXXIX?",
             "Tens: LXXX = 50 + 10 + 10 + 10 = 80. Ones: IX = 10 − 1 = 9. 80 + 9 = 89.", "89") +
        "<h2>Write a number as a Roman numeral</h2>"
        "<p>Partition the number into tens and ones. Write the tens, then the ones.</p>"
        + table(["Tens", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"],
                [["Roman", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC", "C"]]) +
        table(["Ones", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
              [["Roman", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]]) +
        ex("Write", "Write 49 in Roman numerals.",
           "49 = 40 + 9. 40 = XL and 9 = IX. Put them together.", "XLIX (not IL)") +
        "<h2>Roman numerals in real life</h2>"
        "<p>You see them on clock faces, after the names of kings and queens (Henry VIII, Elizabeth II), "
        "on chapters of books and in the titles of films.</p>"
        "<figure class='sn-fig'>" + clock_svg(4, 30, size=230) +
        "<figcaption>The minute hand (red) points to VI and the hour hand is between IV and V. It is half past four.</figcaption></figure>"
        "<h2>No zero and no place value</h2>"
        "<p>In our number 77, the first 7 is worth 70 and the second 7 is worth 7: the <b>place</b> changes the value. "
        "In Roman numerals, X always means 10, wherever it is. That is why the Romans did not need a zero. "
        "Our digits 0 to 9, with zero and place value, came later from India through Arabic mathematicians. "
        "They make big numbers and written calculations much easier.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["IIII for 4, XXXX for 40", "Never 4 of the same symbol in a row: IV, XL"],
            ["Adding every symbol (IX = 11, XL = 60)", "Smaller before bigger means take away: IX = 9, XL = 40"],
            ["IL for 49, IC for 99", "Partition first: 49 = XL + IX = XLIX, 99 = XC + IX = XCIX"],
            ["VX for 5, LC for 50", "V and L are never put before a bigger symbol: 5 = V, 50 = L"],
            ["Writing 47 as IVVII (4 then 7)", "40 is XL, not IV: 47 = XLVII"],
        ])
    )


FAQ = [
    {"q": "Do Year 4 children need to learn Roman numerals?",
     "a": "Yes. The National Curriculum in England says Year 4 pupils should read Roman numerals to 100 (I to C) and know that the number system changed over time to include zero and place value."},
    {"q": "How do you write 4 and 9 in Roman numerals?",
     "a": "4 is IV (5 − 1) and 9 is IX (10 − 1). A smaller symbol before a bigger one is taken away, so you never write IIII or VIIII."},
    {"q": "Why do some clocks show IIII instead of IV?",
     "a": "Many clockmakers use IIII as a tradition, partly so the face looks balanced opposite VIII. In maths, the correct way to write 4 is IV."},
    {"q": "Why did the Romans not have a zero?",
     "a": "Each Roman symbol always has the same value, so there are no empty places to fill. Zero is only needed with place value, which came to Europe later from India through Arabic mathematicians."},
]


def gen():
    rnd = random.Random(4404)
    P = People(rnd)
    sets = [set_symbols(), set_read(), set_write(), set_calc(), set_life(P)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(p) == 5 for p in range(4))
    return {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "roman-numerals", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Roman Numerals to 100",
        "seo_title": "Year 4 Roman Numerals Worksheets (I to C): Free Maths Practice with Answer Key",
        "short_title": "Roman numerals",
        "domain": "Number and place value",
        "standard_code": "Year 4: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Read Roman numerals to 100 (I to C) and know that over time, the numeral system changed to include the concept of zero and place value.",
        "meta_desc": "Free Year 4 Roman numerals worksheets for the National Curriculum: I, V, X, L and C, the subtraction rule (IV, IX, XL, XC), reading and writing numbers to 100, clocks, kings and queens, and why the Romans had no zero. 100 questions with answer key.",
        "key_big": "Add when the same or a smaller symbol comes after. Take away when a smaller symbol comes before: IV = 4, IX = 9, XL = 40, XC = 90.",
        "key_sub": "I = 1, V = 5, X = 10, L = 50, C = 100. Partition into tens and ones: 47 = XL + VII = XLVII. Never write 4 of the same symbol in a row.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
