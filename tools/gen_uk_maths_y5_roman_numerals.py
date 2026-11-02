# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Roman Numerals to 1,000 and Years (National Curriculum in England, Number and place value)
  python tools/gen_uk_maths_y5_roman_numerals.py
Numbers to 1,000 with D and M, and years such as MCMXCIX. Every value is checked in code.
Wrong answers come from real pupil mistakes: DM for 500, CCCC for 400, IM for 999, XD for 490,
reading every symbol as an add (CM = 1,100, MCM = 2,100), MIM for 1999, swapping CD and DC,
mixing up D with L or M, writing a subtraction as a numeral (CCD for 300).
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
LINE = "#2b2b2b"
RED = "#d6453b"
GRAY = "#6b6259"
STONE = "#e4ded3"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
PAIRS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
         (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
SUB = {"IV", "IX", "XL", "XC", "CD", "CM"}


# ------------------------------------------------------------ Roman numerals
def roman(n):
    assert 1 <= n <= 3999, n
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
    """The mistake of adding every symbol (CM read as 1,100)."""
    return sum(VAL[ch] for ch in s)


def fmt(n):
    return "{:,}".format(n)


def chunk(v):
    """'CM = 1,000 − 100 = 900' or 'DCC = 500 + 100 + 100 = 700'."""
    r = roman(v)
    if r in SUB:
        return "%s = %s %s %s = %s" % (r, fmt(VAL[r[1]]), MINUS, fmt(VAL[r[0]]), fmt(v))
    if len(r) == 1:
        return "%s = %s" % (r, fmt(v))
    return "%s = %s = %s" % (r, " + ".join(fmt(VAL[ch]) for ch in r), fmt(v))


def parts(n):
    """Thousands, hundreds, tens, ones (zeros left out)."""
    return [p for p in (n // 1000 * 1000, n % 1000 // 100 * 100, n % 100 // 10 * 10, n % 10) if p]


def read_e(r, year=False):
    n = value(r)
    assert roman(n) == r, r
    ps = parts(n)
    if len(ps) == 1:
        e = "%s." % chunk(n)
    else:
        e = "Split it: %s. So %s = %s." % ("; ".join(chunk(p) for p in ps), r, " + ".join(fmt(p) for p in ps))
    if year:
        e += " The year is %d." % n
    elif len(ps) > 1:
        e = e[:-1] + " = %s." % fmt(n)
    return e


def write_e(n, year=False):
    ps = parts(n)
    num = str(n) if year else fmt(n)
    if len(ps) == 1:
        return "%s, so %s = %s." % (chunk(n), num, roman(n))
    names = ["%s = %s" % (fmt(p), roman(p)) for p in ps]
    return "Partition %s into %s. %s and %s. So %s = %s." % (
        num, " + ".join(fmt(p) for p in ps), ", ".join(names[:-1]), names[-1], num, roman(n))


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e):
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    return {"q": q, "c": [correct] + wrong, "a": 0, "e": e}


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


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and every symbol can be read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


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
    """Clock face with Roman numerals I to XII. The hour hand is placed by the exact time."""
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
    assert hands_gap(h, m) >= 12, (h, m)
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6), "clock with Roman numerals showing %s" % say_time(h, m))


def symbols_svg():
    """The seven symbols with their values."""
    W, H = 7 * 72 + 12, 104
    s = []
    for i, ch in enumerate("IVXLCDM"):
        x = 6 + i * 72
        s.append("<rect x='%d' y='6' width='64' height='54' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, FILL, GREEN))
        s.append("<text x='%d' y='45' font-family='Georgia, serif' font-size='30' font-weight='700' fill='%s' "
                 "text-anchor='middle'>%s</text>" % (x + 32, LINE, ch))
        s.append("<text x='%d' y='90' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + 32, RED, fmt(VAL[ch])))
    return svg_wrap(W, H, "".join(s), "the symbols I, V, X, L, C, D and M with their values 1, 5, 10, 50, 100, 500 and 1,000")


def split_svg(n, year=False):
    """Numeral split into its parts, with the value under each part."""
    ps = parts(n)
    boxes = [(roman(p), fmt(p)) for p in ps]
    widths = [max(64, 24 * len(r) + 24) for r, _ in boxes]
    gap = 36
    total = str(n) if year else fmt(n)
    W = sum(widths) + gap * (len(boxes) - 1) + 6 + 10 + 12 * (len(total) + 2) + 6
    H = 112
    s = []
    x = 6
    for i, ((r, v), w) in enumerate(zip(boxes, widths)):
        s.append("<rect x='%d' y='6' width='%d' height='54' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, w, FILL, GREEN))
        s.append("<text x='%.1f' y='45' font-family='Georgia, serif' font-size='28' font-weight='700' fill='%s' "
                 "text-anchor='middle'>%s</text>" % (x + w / 2.0, LINE, r))
        s.append("<text x='%.1f' y='94' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + w / 2.0, RED, v))
        x += w
        if i < len(boxes) - 1:
            s.append("<text x='%.1f' y='94' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>+</text>"
                     % (x + gap / 2.0, LINE))
            x += gap
    s.append("<text x='%d' y='94' font-size='20' font-weight='700' fill='%s'>= %s</text>" % (x + 10, RED, total))
    return svg_wrap(W, H, "".join(s), "%s split into %s" % (roman(n), ", ".join(r for r, _ in boxes)))


def stone_svg(r, line1, line2):
    """A foundation stone with a year carved in Roman numerals."""
    W, H = 300, 140
    s = ["<rect x='4' y='4' width='292' height='132' rx='3' fill='%s' stroke='%s' stroke-width='3'/>" % (STONE, GRAY),
         "<rect x='14' y='14' width='272' height='112' fill='none' stroke='%s' stroke-width='1.5'/>" % GRAY,
         "<g font-family='Georgia, serif' fill='%s' text-anchor='middle'>" % LINE,
         "<text x='150' y='44' font-size='16' letter-spacing='2'>%s</text>" % line1,
         "<text x='150' y='68' font-size='16' letter-spacing='2'>%s</text>" % line2,
         "<text x='150' y='108' font-size='30' font-weight='700' letter-spacing='3'>%s</text>" % r,
         "</g>"]
    return svg_wrap(W, H, "".join(s), "foundation stone carved with %s" % r)


# ============================================================ set 1: the seven symbols and numbers to 100
def set_symbols():
    its = []
    its.append(mcq("What number does %s stand for?" % b("C"), "100", ["50", "500", "1,000"],
                   "C = 100. C is the first letter of centum, the Latin word for a hundred (think of a century). L is 50 and D is 500."))
    its.append(mcq("What number does %s stand for?" % b("D"), "500", ["50", "1,000", "5,000"],
                   "D = 500. Do not mix it up with L (50) or M (1,000)."))
    its.append(mcq("What number does %s stand for?" % b("M"), "1,000", ["500", "100", "1,000,000"],
                   "M = 1,000. It comes from mille, the Latin word for a thousand. M does not stand for a million."))
    its.append(mcq("What number does %s stand for?" % b("L"), "50", ["500", "100", "5"],
                   "L = 50. D is 500, C is 100 and V is 5."))
    its.append(mcq("Which Roman numeral means 500?", "D", ["DM", "CCCCC", "M"],
                   "500 has its own symbol: D. DM is not allowed: D is never put before a bigger symbol. "
                   "CCCCC uses 5 Cs, but you never write more than 3 of the same symbol in a row. M is 1,000."))
    its.append(mcq("Which Roman numeral means 1,000?", "M", ["DD", "D", "CM"],
                   "1,000 has its own symbol: M. DD is not allowed: D is never repeated. D is 500 and CM is 900."))
    its.append(mcq("Which Roman numeral means 100?", "C", ["L", "D", "XC"],
                   "C = 100. L is 50, D is 500 and XC is 90."))
    its.append(mcq("Which three symbols are <b>never</b> repeated, like VV or DD?", "V, L and D",
                   ["I, X and C", "C, D and M", "I, V and X"],
                   "V, L and D are never repeated, because two of them make another symbol: VV = X, LL = C and DD = M."))
    its.append(mcq("Which symbols can go in front of a bigger symbol to be taken away?", "I, X and C",
                   ["V, L and D", "I, V and X", "C, D and M"],
                   "Only I, X and C are taken away: IV, IX, XL, XC, CD and CM. V, L and D are never put before a bigger symbol."))
    its.append(mcq("What is the most times you can write the same symbol in a row?", "3", ["4", "2", "5"],
                   "Never more than 3 in a row: III = 3, XXX = 30, CCC = 300. 4 is IV, 40 is XL and 400 is CD."))
    reads = [("XIV", ["16", "6", "15"], " The I is before the V, so take it away: XIV is not 16."),
             ("XXXIX", ["41", "29", "49"], " IX is 9, not 11, so XXXIX is not 41."),
             ("XLIX", ["71", "69", "51"], " Adding every symbol gives 71, which is wrong."),
             ("LXXXVIII", ["83", "78", "98"], " Count carefully: L and three Xs make 80, then VIII is 8."),
             ("XCIV", ["116", "114", "96"], " XC is 90, not 110, and IV is 4, not 6.")]
    for r, wr, note in reads:
        its.append(mcq("What number is %s?" % b(r), value(r), wr, read_e(r) + note))
    writes = [(40, ["XXXX", "LX", "XC"], " XXXX is wrong: never 4 Xs in a row. LX is 60."),
              (64, ["LXVI", "LXIIII", "XLIV"], " IV is 4, so LXVI (66) is wrong, and IIII is never used."),
              (90, ["LXXXX", "CX", "XL"], " CX is 110: the smaller symbol must come before the bigger one to take away."),
              (49, ["IL", "XXXXIX", "XLVIIII"], " IL is not allowed: I can only go before V or X."),
              (99, ["IC", "LXXXXVIIII", "XCVIIII"], " IC is not allowed: I can only go before V or X.")]
    for n, wr, note in writes:
        its.append(mcq("Write %d in Roman numerals." % n, roman(n), wr, write_e(n) + note))
    return {"title": "The seven symbols I, V, X, L, C, D, M and numbers to 100", "items": its}


# ============================================================ set 2: read numbers to 1,000
def set_read():
    its = []
    data = [
        ("CCC", ["30", "200", "400"], " Each C is 100. Do not mix C up with X (10)."),
        ("DC", ["400", "1,100", "150"], " The smaller C comes after the D, so add it. D is 500, not 1,000 (M) or 50 (L)."),
        ("CD", ["600", "900", "40"], " The smaller C comes before the D, so take it away: CD is not 600."),
        ("CM", ["1,100", "400", "90"], " The C comes before the M, so take it away: CM is not 1,100."),
        ("DCCC", ["700", "900", "1,300"], " Count the Cs: there are three. D is 500, not 1,000."),
        ("CXX", ["80", "220", "102"], " The Xs come after the C, so add them. Roman numerals have no place value, so it is not 102."),
        ("CCLX", ["240", "360", "160"], " LX is 60. XL would be 40."),
        ("CDL", ["650", "550", "400"], " CD is 400, not 600, so CDL is not 650."),
        ("DXL", ["560", "550", "1,040"], " XL is 40, not 60."),
        ("CCXLV", ["265", "255", "345"], " XL is 40, not 60."),
        ("CDIX", ["611", "411", "609"], " CD is 400 and IX is 9: take away both times."),
        ("CMIV", ["1,106", "906", "1,104"], " CM is 900 and IV is 4: take away both times."),
        ("CXLIX", ["171", "169", "151"], " XL is 40, not 60, and IX is 9, not 11."),
        ("DCLXVI", ["646", "664", "466"], " Every symbol here is followed by a smaller one, so add them all. DCLXVI uses D, C, L, X, V and I once each."),
        ("DCCLXXVII", ["757", "677", "787"], " Count carefully: DCC = 700, LXX = 70, VII = 7."),
        ("CCCXCIX", ["421", "419", "401"], " XC is 90, not 110, and IX is 9, not 11."),
        ("CDXCIV", ["694", "514", "496"], " CD is 400 (not 600), XC is 90 (not 110) and IV is 4 (not 6)."),
        ("DCCCLXXXVIII", ["788", "878", "887"], " Count carefully: three Cs, three Xs and three Is."),
        ("CMXC", ["1,210", "1,190", "1,010"], " CM is 900 (not 1,100) and XC is 90 (not 110)."),
        ("CMXCIX", ["1,221", "1,199", "1,001"], " It is the biggest number below 1,000. It is not IM."),
    ]
    for r, wr, note in data:
        n = value(r)
        assert roman(n) == r and n <= 1000
        if r == "CMXCIX":
            note = " 999 is the biggest number below 1,000. It is never written IM."
        its.append(mcq("What number is %s?" % b(r), fmt(n), wr, read_e(r) + note))
    return {"title": "Read Roman numerals to 1,000: CD, D, DC, CM and M", "items": its}


# ============================================================ set 3: write numbers to 1,000
def set_write():
    its = []

    def w(n, wr, note=""):
        its.append(mcq("Write %d in Roman numerals." % n, roman(n), wr, write_e(n) + note))

    def notright(ok, bad, why):
        for r in ok:
            assert roman(value(r)) == r
        its.append(mcq("Which Roman numeral is <b>not</b> written correctly?", bad, ok, why))

    def missing(n, start, wr):
        rest = roman(n)[len(start):]
        assert roman(n).startswith(start)
        its.append(mcq("Which symbols are missing? %d = %s ?" % (n, start), rest, wr,
                       "%d = %d + %d. %s = %d, so the missing part is %d = %s." % (
                           n, value(start), n - value(start), start, value(start), n - value(start), rest)))

    w(140, ["CXXXX", "CLX", "XLC"], " Write the hundreds first, then the tens: C then XL.")
    w(400, ["CCCC", "DC", "CCD"], " CCCC is wrong (never 4 Cs in a row) and DC is 600. Only one C can go before D.")
    w(600, ["CD", "CCCCCC", "DCC"], " The C comes after the D because we add it. CD would be 400.")
    w(250, ["LCC", "CLL", "CCXL"], " Write the bigger values first. L is never repeated, so CLL is wrong.")
    missing(760, "DCC", ["XL", "VI", "LXX"])
    w(900, ["DCCCC", "MC", "CCM"], " DCCCC has 4 Cs in a row, and MC is 1,100.")
    w(444, ["CCCCXXXXIIII", "DCLXVI", "CDXLVI"], " Take away in every part: CD, XL, IV. Swapping them all gives DCLXVI, which is 666.")
    notright(["CD", "DC", "CM"], "CCCC", "CCCC is not correct: 400 is written CD. The others are correct: CD = 400, DC = 600, CM = 900.")
    w(490, ["XD", "CCCCLXXXX", "DCCX"], " XD is not allowed: X can only go before L or C.")
    w(495, ["VD", "XDV", "CDXCIV"], " VD is not allowed: V is never put before a bigger symbol. CDXCIV is 494.")
    w(499, ["ID", "CDIC", "CCCCLXXXXVIIII"], " ID and IC are not allowed: I can only go before V or X.")
    w(550, ["LD", "DXL", "CCCCCL"], " LD is not allowed: L is never put before a bigger symbol. DXL is 540.")
    notright(["CDXC", "CMXL", "DXC"], "XD", "XD is not correct: X can only go before L or C, so 490 = CD + XC = CDXC. "
             "The others are correct: CDXC = 490, CMXL = 940, DXC = 590.")
    w(707, ["DCCLXX", "DCCCVII", "DCVII"], " There are no tens, so write nothing for them. DCCLXX is 770.")
    missing(940, "CM", ["LX", "XXXX", "IV"])
    w(840, ["DCCCLX", "DCCCXXXX", "CCMXL"], " 800 is DCCC: only one C can go before M, so CCM is wrong.")
    w(385, ["CCCXXCV", "CCCXXXV", "CDLXXXV"], " 80 = LXXX. Only one X can go before C, so XXC is wrong.")
    notright(["M", "CC", "CCC"], "DD", "DD is not correct: D is never repeated, so 1,000 is written M. The others are correct: M = 1,000, CC = 200, CCC = 300.")
    w(990, ["XM", "DCCCCLXXXX", "MCCX"], " XM is not allowed: X can only go before L or C.")
    w(999, ["IM", "DCCCCLXXXXVIIII", "CMXCVIIII"], " IM is not allowed: I can only go before V or X.")
    return {"title": "Write numbers to 1,000 in Roman numerals", "items": its}


# ============================================================ set 4: years
def set_years():
    its = []
    reads = [
        ("MMV", ["1005", "2050", "2010"], " Count both Ms. V is 5: do not mix it up with L (50) or X (10)."),
        ("MMX", ["1010", "2100", "2020"], " Count both Ms. X is 10, not 100."),
        ("MDCCC", ["1700", "1900", "1350"], " Count the Cs: three. D is 500, not 50."),
        ("MCM", ["2100", "2000", "1100"], " The C is before the second M, so take it away: CM = 900. MCM is not 2100."),
        ("MDCCCL", ["1800", "1950", "1650"], " Do not forget the L at the end."),
        ("MLXVI", ["1064", "1046", "1116"], " LX is 60 and VI is 6. This is the year of the Battle of Hastings."),
        ("MCMXLV", ["2165", "1965", "2145"], " CM is 900 (not 1,100) and XL is 40 (not 60)."),
        ("MCMLXX", ["2170", "1960", "1980"], " CM is 900, not 1,100."),
        ("MCMXC", ["2210", "2190", "2010"], " CM is 900 (not 1,100) and XC is 90 (not 110)."),
        ("MMXII", ["1012", "2002", "2021"], " Count both Ms, then read XII = 12."),
        ("MDCLXVI", ["1646", "1664", "1466"], " This is the year of the Great Fire of London."),
        ("MCDLXXXV", ["1685", "1585", "1475"], " CD is 400, not 600."),
    ]
    for r, wr, note in reads:
        n = value(r)
        assert roman(n) == r
        its.append(mcq("What year is %s?" % b(r), n, wr, read_e(r, year=True) + note))
    writes = [
        (1500, ["DM", "MCCCCC", "MDC"], " Write the thousands first: M, then D. DM is not allowed: D is never put before a bigger symbol."),
        (1950, ["MDCCCCL", "MLM", "MCMXL"], " MLM is not allowed: L is never put before a bigger symbol."),
        (1984, ["MCMLXXXVI", "MCMLXXXIIII", "MCMXXXIV"], " IV is 4. VI would be 6."),
        (1999, ["MIM", "MCMXCVIIII", "MDCCCCLXXXXIX"], " MIM is a common mistake: I can only go before V or X, so 999 must be CMXCIX."),
        (2020, ["MXX", "MMCC", "MMXXX"], " 2,000 needs two Ms: MXX is 1020."),
        (2026, ["MMXXIV", "MMXVVI", "MMXXXVI"], " VI is 6 (V then I). IV would be 4, and V is never repeated."),
    ]
    for n, wr, note in writes:
        its.append(mcq("Write the year %d in Roman numerals." % n, roman(n), wr, write_e(n, year=True) + note))
    first = ["MCMLXVI", "MCMXL", "MCMLXXX", "MCMXCIX"]
    vals = [value(r) for r in first]
    ans = first[vals.index(min(vals))]
    its.append(mcq("Which year came first?", ans, [r for r in first if r != ans],
                   ", ".join("%s = %d" % (r, value(r)) for r in sorted(first, key=value)) + ". %s is the earliest year." % ans))
    last = ["MCMXCIX", "MMI", "MCMLXXXVIII", "MMX"]
    vals = [value(r) for r in last]
    ans = last[vals.index(max(vals))]
    its.append(mcq("Which year is the latest?", ans, [r for r in last if r != ans],
                   ", ".join("%s = %d" % (r, value(r)) for r in sorted(last, key=value))
                   + ". %s is the latest. A longer numeral is not always a bigger number." % ans))
    return {"title": "Years in Roman numerals: MCM, MCMXCIX and MMXXVI", "items": its}


# ============================================================ set 5: real life, compare and calculate
def set_life(P):
    its = []
    for h, m, wr in [(10, 15, ["quarter past eleven", "quarter past nine", "quarter to ten"]),
                     (3, 45, ["quarter to six", "quarter past four", "quarter to three"])]:
        if m == 15:
            e = ("The minute hand (red) points to III, which is quarter past. The hour hand has just passed X (10), "
                 "so it is quarter past ten. Be careful: X is 10 and XI is 11.")
        else:
            e = ("The minute hand (red) points to IX, which is quarter to. The hour hand is nearly at IV (4), "
                 "so it is quarter to four. Be careful: IV is 4, not 6.")
        assert say_time(h, m) not in wr
        its.append(mcq(fig(clock_svg(h, m)) + "What time does this clock show?", say_time(h, m), wr, e))
    name, she, her = P.next()
    its.append(mcq("At the end of a film, %s sees “© MCMXCVII”. In what year was the film made?" % name, "1997",
                   ["2197", "1999", "1995"],
                   read_e("MCMXCVII", year=True) + " CM is 900, not 1,100, and VII is 7."))
    its.append(mcq(fig(stone_svg("MDCCCXCII", "THIS STONE", "WAS LAID IN")) + "In what year was this stone laid?",
                   "1892", ["2092", "1912", "1872"],
                   read_e("MDCCCXCII", year=True) + " XC is 90, not 110."))
    its.append(mcq("Queen Victoria became queen in MDCCCXXXVII. What year was that?", "1837",
                   ["1835", "1873", "1637"], read_e("MDCCCXXXVII", year=True)
                   + " Count the Cs (three) and the Xs (three). VII is 7."))
    its.append(mcq("Queen Elizabeth II was crowned in MCMLIII. What year was that?", "1953",
                   ["2153", "1903", "1958"], read_e("MCMLIII", year=True) + " L is 50 and III is 3."))
    its.append(mcq("A monument says MDCCCXV, the year of the Battle of Waterloo. What year is that?", "1815",
                   ["1825", "1615", "1817"], read_e("MDCCCXV", year=True) + " XV is 15, not 17."))
    its.append(mcq("The London 2012 Olympic Games were called “the Games of the XXX Olympiad”. Which Olympiad was that?",
                   "the 30th", ["the 3rd", "the 300th", "the 33rd"],
                   "XXX = 10 + 10 + 10 = 30, so London 2012 was the 30th Olympiad. X is 10, not 1 or 100."))
    name, she, her = P.next()
    its.append(mcq("%s’s favourite film came out in MCMXCIX and its sequel in MMIX. How many years apart are they?" % name,
                   "10", ["12", "8", "1,010"],
                   "MCMXCIX = 1999 and MMIX = 2009. 2009 " + MINUS + " 1999 = 10 years. "
                   "Reading IX as 11 gives 12 or 8, and forgetting the first M of MCMXCIX gives 1,010."))
    its.append(mcq("M comes from mille, the Latin word for a thousand. Which English word also comes from mille?",
                   "millennium", ["metre", "minute", "medium"],
                   "A millennium is 1,000 years. Metre, minute and medium come from other Latin and Greek words."))
    vx, vy = value("CD"), value("DC")
    its.append(mcq("Which is true?", "CD &lt; DC", ["CD &gt; DC", "CD = DC", "DC &lt; CD"],
                   "CD = 500 %s 100 = %d and DC = 500 + 100 = %d. %d &lt; %d, so CD &lt; DC." % (MINUS, vx, vy, vx, vy)))
    lst = ["CMX", "DCCCLXXX", "DCCCXC", "CM"]
    vals = [value(r) for r in lst]
    assert max(vals) == value("CMX")
    its.append(mcq("Which Roman numeral is the greatest?", "CMX", [r for r in lst if r != "CMX"],
                   ", ".join("%s = %d" % (r, value(r)) for r in sorted(lst, key=value))
                   + ". CMX is the greatest. A longer numeral is not always bigger."))
    order = ["MCMLX", "MCMLXX", "MCMXC"]
    assert [value(r) for r in order] == sorted(value(r) for r in order)
    fmtl = lambda l: ", ".join(l)
    its.append(mcq("Which list of years goes from earliest to latest?", fmtl(order),
                   [fmtl(["MCMXC", "MCMLXX", "MCMLX"]), fmtl(["MCMLXX", "MCMLX", "MCMXC"]), fmtl(["MCMLX", "MCMXC", "MCMLXX"])],
                   ", ".join("%s = %d" % (r, value(r)) for r in order) + ". From earliest to latest: %s." % fmtl(order)))
    calcs = [
        ("CM", "+", "C", ["MCC", "CMC", "DD"], " CMC just puts the numerals side by side. DD is not allowed: D is never repeated."),
        ("M", MINUS, "I", ["IM", "CMIC", "MI"], " IM is not allowed: I can only go before V or X. MI is 1,001."),
        ("D", MINUS, "CC", ["DCC", "CD", "CCD"], " CCD is not a Roman numeral: only one C can go before D. DCC is 500 + 200."),
        ("CDL", "+", "L", ["DCC", "CDLL", "CDC"], " CD is 400, not 600, so the answer is not DCC (700)."),
        ("C", "×", "V", ["CV", "M", "CCCCC"], " CV is 105, not 100 × 5. M is 100 × 10. CCCCC has too many Cs."),
    ]
    for x, op, y, wr, note in calcs:
        vxx, vyy = value(x), value(y)
        v = {"+": vxx + vyy, MINUS: vxx - vyy, "×": vxx * vyy}[op]
        assert 1 <= v <= 1000
        e = "%s = %s and %s = %s. %s %s %s = %s, and %s = %s." % (x, fmt(vxx), y, fmt(vyy), fmt(vxx), op, fmt(vyy), fmt(v), fmt(v), roman(v))
        its.append(mcq("Work out %s %s %s. Give the answer in Roman numerals." % (b(x), op, b(y)), roman(v), wr, e + note))
    name, she, her = P.next()
    assert naive("MCMXXXVI") == 2136 and value("MCMXXXVI") == 1936
    its.append(mcq("A foundation stone says MCMXXXVI. %s reads it as 2136. What mistake did %s make?" % (name, she),
                   "Added the C instead of taking it away",
                   ["Read each X as 100", "Read VI as 4", "Read the first M as 2,000"],
                   "MCMXXXVI = M + CM + XXX + VI = 1,000 + 900 + 30 + 6, so the year is 1936. "
                   "Adding the C gives 1,000 + 100 + 1,000 + 30 + 6 = 2136. The C comes before the M, so it must be taken away."))
    its.append(mcq("Which year is <b>not</b> written correctly?", "MIM", ["MCMXCIX", "MCMLXXX", "MMXX"],
                   "MIM is not correct: I can only go before V or X. 1999 is written MCMXCIX. "
                   "The others are correct: MCMXCIX = 1999, MCMLXXX = 1980, MMXX = 2020."))
    return {"title": "Real life: films, foundation stones, kings and queens, and calculations", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    return (
        "<h2>Seven symbols</h2>"
        "<p>In Year 4 you used I, V, X, L and C. Now add two more: D for 500 and M for 1,000.</p>"
        "<figure class='sn-fig'>" + symbols_svg() +
        "<figcaption>I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1,000. M is for mille, the Latin word for a thousand.</figcaption></figure>"
        "<h2>Add or take away?</h2>"
        "<ol class='rk-step'>"
        "<li><b>Same or smaller symbol after:</b> add. DC = 500 + 100 = 600. MD = 1,000 + 500 = 1,500.</li>"
        "<li><b>Smaller symbol before a bigger one:</b> take it away. CD = 500 − 100 = 400. CM = 1,000 − 100 = 900.</li>"
        "<li><b>Never more than 3 of the same symbol in a row.</b> 400 is CD, not CCCC. V, L and D are never repeated.</li></ol>"
        + table(["Take away", "Means", "Value"], [
            ["IV", "5 − 1", "4"], ["IX", "10 − 1", "9"], ["XL", "50 − 10", "40"], ["XC", "100 − 10", "90"],
            ["CD", "500 − 100", "400"], ["CM", "1,000 − 100", "900"],
        ]) +
        "<p>These six pairs are the only ones. I goes only before V or X, X only before L or C, and C only before D or M.</p>"
        "<h2>Read a Roman numeral</h2>"
        "<p>Split it into hundreds, tens and ones, then add the parts.</p>"
        "<figure class='sn-fig'>" + split_svg(494) +
        "<figcaption>CDXCIV = CD + XC + IV = 400 + 90 + 4 = 494.</figcaption></figure>"
        + ex("Read", "What number is DCCXLVIII?",
             "Hundreds: DCC = 500 + 100 + 100 = 700. Tens: XL = 50 − 10 = 40. Ones: VIII = 8. 700 + 40 + 8 = 748.", "748") +
        "<h2>Write a number as a Roman numeral</h2>"
        "<p>Partition the number into hundreds, tens and ones. Write each part, biggest first.</p>"
        + table(["Hundreds", "100", "200", "300", "400", "500", "600", "700", "800", "900", "1,000"],
                [["Roman", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM", "M"]]) +
        ex("Write", "Write 999 in Roman numerals.",
           "999 = 900 + 90 + 9. 900 = CM, 90 = XC and 9 = IX. Put them together.", "CMXCIX (not IM)") +
        "<h2>Years in Roman numerals</h2>"
        "<p>Years are bigger than 1,000, but they are easy: write M for each thousand, then the rest is a number to 1,000 that you already know.</p>"
        "<figure class='sn-fig'>" + split_svg(1999, year=True) +
        "<figcaption>MCMXCIX = M + CM + XC + IX = 1,000 + 900 + 90 + 9. The year is 1999.</figcaption></figure>"
        + ex("Year", "Write the year 2026 in Roman numerals.",
             "2026 = 2,000 + 20 + 6. 2,000 = MM, 20 = XX and 6 = VI.", "MMXXVI") +
        "<p>You see years like this at the end of films and TV programmes, on foundation stones of old buildings, "
        "and on monuments. Kings and queens (Henry VIII, Charles III) and clock faces use smaller Roman numerals.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["CCCC for 400, DCCCC for 900", "Never 4 of the same symbol in a row: CD, CM"],
            ["Adding every symbol (CM = 1,100, MCM = 2,100)", "Smaller before bigger means take away: CM = 900, MCM = 1900"],
            ["IM for 999, XD for 490, MIM for 1999", "Partition first: 999 = CM + XC + IX = CMXCIX"],
            ["DM for 500, DD for 1,000", "D is never put before a bigger symbol or repeated: 500 = D, 1,000 = M"],
            ["Mixing up D with L or M", "L = 50, D = 500, M = 1,000"],
        ])
    )


FAQ = [
    {"q": "What Roman numerals do Year 5 children need to know?",
     "a": "The National Curriculum in England says Year 5 pupils should read Roman numerals to 1,000 (M) and recognise years written in Roman numerals. That adds D (500) and M (1,000) to the I, V, X, L and C learned in Year 4."},
    {"q": "How do you write 400, 900 and 999 in Roman numerals?",
     "a": "400 is CD (500 − 100) and 900 is CM (1,000 − 100). 999 is CMXCIX (900 + 90 + 9), not IM, because I can only go before V or X."},
    {"q": "How do you read a year in Roman numerals, like MCMXCIX?",
     "a": "Split it into parts: M = 1,000, CM = 900, XC = 90 and IX = 9. Add the parts to get 1999."},
    {"q": "Why are years at the end of films written in Roman numerals?",
     "a": "It is a long tradition that makes the date look formal, a bit like a carved stone. You also see Roman numeral years on foundation stones, monuments and clock faces."},
]


def gen():
    rnd = random.Random(5503)
    P = People(rnd)
    sets = [set_symbols(), set_read(), set_write(), set_years(), set_life(P)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(p) == 5 for p in range(4))
    u = {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "roman-numerals-to-1000", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Roman Numerals to 1,000 and Years",
        "seo_title": "Year 5 Roman Numerals Worksheets (to 1,000 with D and M, and Years): Free Maths Practice with Answer Key",
        "short_title": "Roman numerals to 1,000",
        "domain": "Number and place value",
        "standard_code": "Year 5: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Read Roman numerals to 1,000 (M) and recognise years written in Roman numerals.",
        "meta_desc": "Free Year 5 Roman numerals worksheets for the National Curriculum: D and M, CD and CM, reading and writing numbers to 1,000, years like MCMXCIX and MMXXVI, film dates, foundation stones and clocks. 100 questions with answer key.",
        "key_big": "D = 500 and M = 1,000. A smaller symbol before a bigger one is taken away: CD = 400, CM = 900.",
        "key_sub": "Partition into hundreds, tens and ones: 494 = CD + XC + IV = CDXCIV. For a year, write M for each thousand first: 1999 = M + CM + XC + IX = MCMXCIX.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "foundation stone")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
