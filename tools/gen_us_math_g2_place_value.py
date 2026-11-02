# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Place Value to 1000 (2.NBT.A.1, 2.NBT.A.3)
  python tools/gen_us_math_g2_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 2: numbers up to 1000, no commas. Short sentences for 7-8 year olds.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for x in cands:
        if x is None:
            continue
        x = str(x)
        if x in seen or not x or x.startswith("-") or x == "0":
            continue
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_n(q, correct, cands, e, rnd):
    """Number choices. Wrong numbers that are 0 or less are dropped."""
    return mcq(q, correct, [v for v in cands if v is not None and v > 0 and v != correct], e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


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


def hto(n):
    return n // 100, n // 10 % 10, n % 10


def unit(k, one, many):
    return "%d %s" % (k, one if k == 1 else many)


def H(k):
    return unit(k, "hundred", "hundreds")


def T(k):
    return unit(k, "ten", "tens")


def O(k):
    return unit(k, "one", "ones")


def hto_text(h, t, o):
    return "%s, %s, %s" % (H(h), T(t), O(o))


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


# ------------------------------------------------------------ number names (no "and", hyphens for 21-99)
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    if n == 1000:
        return "one thousand"
    out = []
    if n >= 100:
        out.append(ONES[n // 100] + " hundred")
        n %= 100
    if n >= 20:
        out.append(TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else ""))
    elif n > 0:
        out.append(ONES[n])
    return " ".join(out)


def expanded(n):
    h, t, o = hto(n)
    return " + ".join(str(v) for v in (h * 100, t * 10, o) if v)


# ------------------------------------------------------------ figures
U = 8                      # one small cube = U x U, a rod = U x 10U, a flat = 10U x 10U
FG, RG, CG, GG, M = 8, 6, 4, 20, 6   # gaps: flats, rods, cubes, between groups; margin


def blocks_svg(h, t, o, labels=False):
    """Base-ten blocks: h hundred flats, t ten rods, o ones cubes. Sizes are exact (1 : 10 : 100)."""
    F = 10 * U
    fcols = h if h <= 2 else (h + 1) // 2                # 3 or more flats: two rows, so the picture prints larger
    frows = 1 if h <= 2 else 2
    groups = []                                            # (width, height, draw(x, y) -> list)

    def flats(x, y):
        s = []
        for k in range(h):
            fx = x + (k % fcols) * (F + FG)
            fy = y + (k // fcols) * (F + FG)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (fx, fy, F, F, FILL, GREEN))
            for i in range(1, 10):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                         % (fx + i * U, fy, fx + i * U, fy + F, GREEN))
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                         % (fx, fy + i * U, fx + F, fy + i * U, GREEN))
        return s

    def rods(x, y):
        s = []
        for k in range(t):
            rx = x + k * (U + RG)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (rx, y, U, F, FILL, GREEN))
            for i in range(1, 10):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                         % (rx, y + i * U, rx + U, y + i * U, GREEN))
        return s

    ccols = (o + 4) // 5

    def cubes(x, y):
        s = []
        for k in range(o):
            cx = x + (k // 5) * (U + CG + 2)
            cy = y + (k % 5) * (U + CG + 4)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, cy, U, U, CUBE, GREEN))
        return s

    if h:
        groups.append((fcols * F + (fcols - 1) * FG, frows * F + (frows - 1) * FG, flats, H(h)))
    if t:
        groups.append((t * U + (t - 1) * RG, F, rods, T(t)))
    if o:
        groups.append((ccols * U + (ccols - 1) * (CG + 2), 5 * U + 4 * (CG + 4), cubes, O(o)))
    LBL = 15
    lab_w = lambda s: int(len(s) * 8.6) + 4
    widths = [max(g[0], lab_w(g[3])) if labels else g[0] for g in groups]
    body_h = max(g[1] for g in groups)
    W = 2 * M + sum(widths) + GG * (len(groups) - 1)
    Hh = 2 * M + body_h + (26 if labels else 0)
    s = []
    x = M
    for (gw, gh, draw, lab), w in zip(groups, widths):
        s += draw(x + (w - gw) // 2, M)
        if labels:
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x + w / 2, M + body_h + 20, LBL, INK, lab))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "base-ten blocks")


CW, HEAD, ROW = 92, 34, 50


def chart_svg(n, hi=None):
    """Hundreds / tens / ones chart with n in it. hi = place (2, 1, 0) to color red."""
    x0 = y0 = 6
    W, Hh = 2 * x0 + 3 * CW, 2 * y0 + HEAD + ROW
    h, t, o = hto(n)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 3 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 3 * CW, HEAD, FILL)]
    for k, (lab, d, place) in enumerate([("Hundreds", h, 2), ("Tens", t, 1), ("Ones", o, 0)]):
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        cx = x + CW / 2
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (cx, y0 + 23, INK, lab))
        s.append("<text x='%.1f' y='%d' font-size='30' font-weight='800' fill='%s' text-anchor='middle'>%d</text>"
                 % (cx, y0 + HEAD + 36, RED if hi == place else INK, d))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 3 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, Hh, "".join(s), "place value chart")


# ------------------------------------------------------------ typical mistakes
def swap_to(n):
    h, t, o = hto(n)
    return h * 100 + o * 10 + t


def drop_zero(n):
    """406 -> 46, 450 -> 45 (a zero place left out)."""
    s = str(n)
    return int(s[0] + s[1:].replace("0", "")) if "0" in s[1:] else None


def as_heard(n):
    """Writing each spoken part: three hundred six -> 3006, four hundred twenty-seven -> 40027."""
    h, r = divmod(n, 100)
    return int(str(h * 100) + str(r)) if r else None


def block_cands(h, t, o):
    n = 100 * h + 10 * t + o
    c = [swap_to(n), drop_zero(n), h + t + o, n + 10 if t < 9 else n - 10]
    if o:
        c.append(o * 100 + t * 10 + h)
    c += [n - 10 if t else n + 1, n + 100]
    return c


def count_e(h, t, o):
    n = 100 * h + 10 * t + o
    s = "Count each kind. %s = %d. %s = %d. %s = %d. " % (cap(H(h)), h * 100, cap(T(t)), t * 10, cap(O(o)), o)
    s += "%s = %d." % (" + ".join(str(v) for v in (h * 100, t * 10, o) if v), n)
    if t == 0:
        s += " There are no tens, so write 0 in the tens place."
    elif o == 0:
        s += " There are no ones, so write 0 in the ones place."
    return s


# ============================================================ set 1: base-ten blocks
def set_blocks(rnd, used):
    its = []
    specs = []
    # (h, t, o): 2 with no tens, 2 with no ones, the rest mixed
    zt = [(rnd.randint(1, 5), 0, rnd.randint(1, 9)) for _ in range(2)]
    zo = [(rnd.randint(1, 5), rnd.randint(2, 7), 0) for _ in range(2)]
    while len(specs) < 10:
        h, t, o = rnd.randint(1, 6), rnd.randint(1, 7), rnd.randint(1, 9)
        if t == o or (h, t, o) in specs:
            continue
        specs.append((h, t, o))
    specs = specs[:3] + zt[:1] + specs[3:6] + zo[:1] + specs[6:8] + zt[1:] + specs[8:] + zo[1:]
    for h, t, o in specs[:14]:
        n = 100 * h + 10 * t + o
        used.add(n)
        its.append(mcq_n(fig(blocks_svg(h, t, o)) + "What number do the blocks show?", n,
                         block_cands(h, t, o), count_e(h, t, o), rnd))
    # how many hundreds, tens and ones (3)
    for _ in range(3):
        while True:
            h, t, o = rnd.randint(1, 4), rnd.randint(1, 7), rnd.randint(1, 9)
            n = 100 * h + 10 * t + o
            if t != o and h != t and n not in used:
                used.add(n)
                break
        wrong = [hto_text(h, o, t), hto_text(t, h, o), hto_text(h, t + 1, o)]
        its.append(mcq(fig(blocks_svg(h, t, o)) + "Which matches the blocks?", hto_text(h, t, o), wrong,
                       "A big square is 1 hundred. A long rod is 1 ten. A small cube is 1 one. "
                       "Count each kind: %s." % hto_text(h, t, o), rnd))
    # value of the rods (3)
    for t in rnd.sample(range(2, 9), 3):
        while True:
            h, o = rnd.randint(1, 4), rnd.randint(1, 9)
            n = 100 * h + 10 * t + o
            if t != o and n not in used:
                used.add(n)
                break
        its.append(mcq_n(fig(blocks_svg(h, t, o)) + "What are the ten rods worth in all?", t * 10,
                         [t, t * 100, n, t * 10 + o],
                         "Each rod is 10. There are %d rods. %s = %d." % (t, cap(T(t)), t * 10), rnd))
    order = its[:3] + its[14:16] + its[3:8] + its[17:19] + its[8:12] + its[16:17] + its[19:] + its[12:14]
    assert len(order) == 20
    return {"title": "Count base-ten blocks", "items": order}


# ============================================================ set 2: hundreds, tens and ones
def three_digit(rnd, used, distinct=True, zero=None):
    while True:
        h, t, o = rnd.randint(1, 9), rnd.randint(1, 9), rnd.randint(1, 9)
        if zero == "t":
            t = 0
        if zero == "o":
            o = 0
        n = 100 * h + 10 * t + o
        if distinct and len({h, t, o}) < 3:
            continue
        if n not in used:
            used.add(n)
            return n


PNAME = {2: "hundreds", 1: "tens", 0: "ones"}


def set_hto(rnd, used):
    its = []
    # value of the red digit with a chart (6)
    for j in range(6):
        n = three_digit(rnd, used)
        p = 2 if j % 2 == 0 else 1
        d = hto(n)[2 - p]
        v = d * 10 ** p
        cands = [d, d * 10, d * 100, n]
        e = ("The red %d is in the %s place. %d %s = %d. The digit is %d, but its value is %d."
             % (d, PNAME[p], d, PNAME[p] if d > 1 else PNAME[p][:-1], v, d, v))
        its.append(mcq_n(fig(chart_svg(n, hi=p)) + "What is the value of the red digit?", v, cands, e, rnd))
    # which digit is in a place (4)
    for p in [1, 2, 1, 2]:
        n = three_digit(rnd, used)
        d = hto(n)[2 - p]
        others = [x for x in hto(n) if x != d]
        e = "%d has %s, %s and %s. The %s digit is %d." % (n, H(hto(n)[0]), T(hto(n)[1]), O(hto(n)[2]), PNAME[p], d)
        its.append(mcq_n("Which digit is in the %s place in %d?" % (PNAME[p], n), d,
                         others + [d * 10 ** p], e, rnd))
    # value of a digit, no chart (3)
    for p in [1, 2, 1]:
        n = three_digit(rnd, used)
        d = hto(n)[2 - p]
        v = d * 10 ** p
        its.append(mcq_n("What is the value of the %d in %d?" % (d, n), v, [d, d * 10, d * 100, n],
                         "The %d is in the %s place. Its value is %d." % (d, PNAME[p], v), rnd))
    # which number has ... with a zero (3)
    for j, z in enumerate(["t", "t", "o"]):
        n = 706 if j == 0 else three_digit(rnd, used, zero=z)
        used.add(n)
        h, t, o = hto(n)
        e = "Write %d hundreds, %d tens, %d ones in order: %d, %d, %d. That is %d." % (h, t, o, h, t, o, n)
        e += " The 0 holds the %s place." % ("tens" if t == 0 else "ones")
        wrong = [swap_to(n), drop_zero(n), as_heard(n) if t == 0 else n * 10]
        its.append(mcq_n("Which number has %s?" % hto_text(h, t, o), n, wrong, e, rnd))
    # a hundred is ten tens (2)
    its.append(mcq("Which is the same as 1 hundred?", "10 tens", ["10 ones", "1 ten", "100 tens"],
                   "A hundred is a bundle of 10 tens. 10 tens = 100.", rnd))
    its.append(mcq("Which is the same as 600?", "6 hundreds", ["6 tens", "60 hundreds", "6 ones"],
                   "600 has a 6 in the hundreds place and 0 tens and 0 ones. 600 = 6 hundreds.", rnd))
    # tens to a number (2)
    its.append(mcq_n("30 tens = ☐", 300, [30, 3000, 3],
                     "10 tens make 1 hundred. So 30 tens make 3 hundreds. 30 tens = 300.", rnd))
    its.append(mcq_n("How many tens are in 400?", 40, [4, 400, 10],
                     "1 hundred is 10 tens. 4 hundreds are 4 groups of 10 tens. That is 40 tens.", rnd))
    order = its[0:2] + its[6:8] + its[2:4] + its[10:12] + its[13:15] + its[4:6] + its[8:10] + its[12:13] + its[15:]
    assert len(order) == 20, len(order)
    return {"title": "Hundreds, tens and ones", "items": order}


# ============================================================ set 3: expanded form
def exp_cands(n):
    h, t, o = hto(n)
    c = []
    if t and o:
        c += ["%d + %d + %d" % (h, t, o), "%d + %d + %d" % (h * 100, t, o)]
        if t != o:
            c.append("%d + %d + %d" % (h * 100, o * 10, t))
        c.append("%d + %d + %d" % (h * 10, t * 10, o))
    elif t == 0:
        c += ["%d + %d" % (h * 100, o * 10), "%d + %d" % (h * 10, o), "%d + %d" % (h, o)]
    else:
        c += ["%d + %d" % (h * 100, t), "%d + %d" % (h * 10, t), "%d + %d" % (h, t)]
    return c


def set_expanded(rnd, used):
    its = []
    # number -> expanded form (7)
    for z in [None, None, "t", None, "o", None, "t"]:
        n = three_digit(rnd, used, zero=z)
        e = "Write the value of each digit and add them: %s." % expanded(n)
        if z:
            e += " The 0 is worth nothing, so it gets no part."
        its.append(mcq("Which shows %d in expanded form?" % n, expanded(n), exp_cands(n), e, rnd))
    # expanded form -> number (7), some out of order
    for j, z in enumerate([None, "t", None, "o", None, "t", None]):
        n = three_digit(rnd, used, zero=z)
        h, t, o = hto(n)
        parts = [str(v) for v in (h * 100, t * 10, o) if v]
        shown = parts if j < 4 else parts[::-1]
        e = "%s = %d. Put each part in its place: %s." % (" + ".join(shown), n, hto_text(h, t, o))
        cands = [drop_zero(n), as_heard(n) if t == 0 else n * 10, swap_to(n)] if z else [
            swap_to(n), int("".join(parts)), h + t + o]
        if j >= 4:
            cands = [int("".join(p[0] for p in shown))] + cands
            e += " Start with the hundreds, even if they come last."
        its.append(mcq_n("What number is %s?" % " + ".join(shown), n, cands, e, rnd))
    # fill in the missing part (6)
    for p in [1, 1, 0, 2, 1, 0]:
        n = three_digit(rnd, used)
        h, t, o = hto(n)
        vals = [h * 100, t * 10, o]
        ans = vals[2 - p]
        d = hto(n)[2 - p]
        show = ["☐" if i == 2 - p else str(v) for i, v in enumerate(vals)]
        q = "%s = %d. What number goes in the box?" % (" + ".join(show), n)
        cands = [d, d * 10, d * 100, int(str(n)[2 - p:]), int(str(n)[1:])]
        e = "The %s digit of %d is %d. Its value is %d. Check: %s = %d." % (PNAME[p], n, d, ans, expanded(n), n)
        its.append(mcq_n(q, ans, cands, e, rnd))
    order = its[0:3] + its[7:10] + its[3:5] + its[14:17] + its[10:12] + its[5:7] + its[17:] + its[12:14]
    assert len(order) == 20
    return {"title": "Expanded form", "items": order}


# ============================================================ set 4: number names
def set_names(rnd, used):
    its = []
    # words -> number (8)
    kinds = ["t", None, "t", "o", "teen", "t", "o", None]
    for z in kinds:
        if z == "teen":
            while True:
                n = rnd.randint(1, 9) * 100 + rnd.randint(13, 19)
                if n not in used and n % 10 != 1:
                    used.add(n)
                    break
            h, r = divmod(n, 100)
            cands = [h * 100 + (r % 10) * 10 + 1, as_heard(n), h * 100 + (r % 10) * 10]
            e = ("The name “%s” means %s and %s. %s is 1 ten and %s. So the number is %d."
                 % (words(n), H(h), words(r), cap(words(r)), O(r % 10), n))
        else:
            n = three_digit(rnd, used, distinct=not z, zero=z)
            h, t, o = hto(n)
            if z == "t":
                cands = [as_heard(n), swap_to(n), drop_zero(n)]
            elif z == "o":
                cands = [as_heard(n), swap_to(n), drop_zero(n)]
            else:
                cands = [as_heard(n), swap_to(n), h * 1000 + n % 100]
            e = "The name “%s” means %s. Write %d, %d, %d. The number is %d." % (words(n), hto_text(h, t, o), h, t, o, n)
            if z:
                e += " Do not write %d: a 3-digit number has only 3 digits." % as_heard(n)
        its.append(mcq_n("Which number is <b>%s</b>?" % words(n), n, cands, e, rnd))
    # number -> words (8)
    for z in ["t", None, "o", "t", None, "t", "o", None]:
        while True:
            n = three_digit(rnd, used, distinct=not z, zero=z)
            h, t, o = hto(n)
            if z != "o" or t >= 3:
                break
        if z == "t":
            alt = [swap_to(n), drop_zero(n), o * 100 + h]          # 306: 360, 36, read from the right 603
        elif z == "o":
            alt = [swap_to(n), drop_zero(n), h * 100 + 10 + t]     # 450: 405, 45, fifty heard as fifteen 415
        else:
            alt = [swap_to(n), o * 100 + t * 10 + h, t * 100 + h * 10 + o]
        cands = [words(v) for v in alt if v and v != n]
        e = "%d is %s. Say “%s hundred”, then read the tens and ones: %s." % (
            n, hto_text(h, t, o), ONES[h], words(n % 100))
        e += " Use a hyphen in numbers like forty-two." if t >= 2 and o else ""
        its.append(mcq("Which is %d in words?" % n, words(n), cands, e, rnd))
    # fix a mistake (4)
    for n, cands in [(512, [5012, 521, 5120]), (308, [380, 38, 3080]), (670, [607, 67, 6070]), (915, [951, 9015, 950])]:
        name, she, her = P.next()
        bad = as_heard(n)
        used.add(n)
        h, t, o = hto(n)
        q = "%s writes “%s” as %d. What should %s write?" % (name, words(n), bad, she)
        e = "%s is %s. A 3-digit number has only 3 digits. Write %d." % (cap(words(n)), hto_text(h, t, o), n)
        its.append(mcq_n(q, n, cands, e, rnd))
    order = its[0:2] + its[8:10] + its[2:4] + its[10:12] + its[4:6] + its[16:18] + its[12:14] + its[6:8] + its[14:16] + its[18:]
    assert len(order) == 20
    return {"title": "Number names and numerals", "items": order}


# ============================================================ set 5: regroup and solve
def set_regroup(rnd, used):
    its = []
    # more than 9 tens or ones (5)
    for h, t, o in [(5, 13, 2), (2, 11, 6), (6, 14, 3), (3, 4, 15), (4, 7, 12)]:
        n = 100 * h + 10 * t + o
        used.add(n)
        cands = [int("%d%d%d" % (h, t, o)), (h * 100 + (t % 10) * 10 + o) if t > 9 else (h * 100 + t * 10 + o % 10),
                 (h * 100 + t + o) if t > 9 else ((h + 1) * 100 + t * 10 + o % 10)]
        if t > 9:
            e = ("%s is 1 hundred and %s. So %s, %s, %s is %s, %s, %s = %d."
                 % (cap(T(t)), T(t - 10), H(h), T(t), O(o), H(h + 1), T(t - 10), O(o), n))
        else:
            e = ("%s is 1 ten and %s. So %s, %s, %s is %s, %s, %s = %d."
                 % (cap(O(o)), O(o - 10), H(h), T(t), O(o), H(h), T(t + 1), O(o - 10), n))
        its.append(mcq_n("What number is %s?" % hto_text(h, t, o), n, cands, e, rnd))
    # blocks with more than 9 rods (3)
    for h, t, o in [(2, 12, 4), (1, 15, 3), (3, 10, 7)]:
        n = 100 * h + 10 * t + o
        used.add(n)
        cands = [int("%d%d%d" % (h, t, o)), h * 100 + (t % 10) * 10 + o, h * 100 + t + o]
        e = ("Count the rods: %d tens. 10 tens make 1 hundred, so %d tens = %d. Then %d + %d + %d = %d."
             % (t, t, t * 10, h * 100, t * 10, o, n))
        its.append(mcq_n(fig(blocks_svg(h, t, o)) + "What number do the blocks show?", n, cands, e, rnd))
    # another way to show (2)
    for n in [452, 638]:
        h, t, o = hto(n)
        right = hto_text(h - 1, t + 10, o)
        wrong = [hto_text(h, t + 10, o), hto_text(h - 1, t, o), hto_text(h - 1, t + 9, o)]
        e = ("Break 1 hundred into 10 tens. %s, %s, %s becomes %s, %s, %s. It is still %d."
             % (H(h), T(t), O(o), H(h - 1), T(t + 10), O(o), n))
        its.append(mcq("Which is another way to show %d?" % n, right, wrong, e, rnd))
    # how many tens in all (2)
    for n in [340, 580]:
        h, t, o = hto(n)
        its.append(mcq_n("How many tens are in %d in all?" % n, n // 10, [t, h, t * 10],
                         "%s is %d tens. Add %s: %d + %d = %d tens in all." % (cap(H(h)), h * 10, T(t), h * 10, t, n // 10), rnd))
    # puzzles and stories (8)
    g = []
    g.append(mcq_n("I have 4 hundreds, 0 tens and 9 ones. What number am I?", 409, [490, 49, 4009],
                   "Write the digits in order: 4 hundreds, 0 tens, 9 ones. That is 409. The 0 holds the tens place.", rnd))
    g.append(mcq_n("I am a 3-digit number. My hundreds digit is 5. My tens digit is 0. "
                   "My ones digit is 3 more than my hundreds digit. What number am I?", 508, [580, 58, 503],
                   "Hundreds: 5. Tens: 0. Ones: 5 + 3 = 8. The number is 508.", rnd))
    g.append(mcq_n("I am a 3-digit number. My hundreds digit is 4. My tens digit is 2 more than that. "
                   "My ones digit is 0. What number am I?", 460, [406, 46, 420],
                   "Hundreds: 4. Tens: 4 + 2 = 6. Ones: 0. The number is 460.", rnd))
    name, she, her = P.next()
    g.append(mcq_n("Pencils come in boxes of 100 and packs of 10. %s buys 3 boxes, 4 packs and 7 single pencils. "
                   "How many pencils does %s have?" % (name, she), 347, [14, 374, 437],
                   "3 boxes = 300. 4 packs = 40. 7 single pencils = 7. 300 + 40 + 7 = 347.", rnd))
    name, she, her = P.next()
    g.append(mcq_n("%s has 2 books of 100 stickers. %s also has 15 sheets of 10 stickers. "
                   "How many stickers does %s have?" % (name, cap(she), she), 350, [215, 2150, 250],
                   "2 books = 200. 15 sheets of 10 = 15 tens = 150. 200 + 150 = 350.", rnd))
    g.append(mcq_n("A baker has 600 cookies. She puts 10 cookies in each bag. How many bags does she fill?",
                   60, [6, 600, 10],
                   "600 is 6 hundreds. Each hundred is 10 tens, so 600 = 60 tens. She fills 60 bags.", rnd))
    name, she, her = P.next()
    g.append(mcq_n("%s makes 836 with base-ten blocks. How many ten rods does %s use?" % (name, she), 3,
                   [8, 6, 30],
                   "836 = 8 hundreds, 3 tens, 6 ones. The tens show how many rods: 3 rods.", rnd))
    g.append(mcq_n("In which number is the 4 worth 40?", 142, [421, 214, 412],
                   "The 4 must be in the tens place. In 142 the 4 is in the tens place, so it is worth 40. "
                   "In 421 and 412 it is worth 400. In 214 it is worth 4.", rnd))
    g = [g[0], g[6], g[7], g[1], g[2], g[3], g[5], g[4]]
    its = its[:2] + its[5:6] + its[3:4] + its[8:9] + its[2:3] + its[6:7] + its[4:5] + its[10:11] + its[7:8] \
        + its[9:10] + its[11:12] + g
    assert len(its) == 20, len(its)
    return {"title": "Regroup and solve puzzles", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Each digit has a place</h2>"
        "<p>A 3-digit number has a <b>hundreds</b> digit, a <b>tens</b> digit and a <b>ones</b> digit. "
        "The place tells you what the digit is worth. 10 ones make 1 ten. <b>10 tens make 1 hundred.</b></p>"
        "<figure class='sn-fig'>" + blocks_svg(2, 4, 3, labels=True) +
        "<figcaption>A big square is 1 hundred. A rod is 1 ten. A small cube is 1 one. "
        "2 hundreds, 4 tens and 3 ones make 243.</figcaption></figure>"
        "<h2>The place value chart</h2>"
        "<figure class='sn-fig'>" + chart_svg(243, hi=1) +
        "<figcaption>In 243 the 4 is in the tens place. Its value is 4 tens, or 40.</figcaption></figure>" +
        ex("Value of a digit", "What is the value of the 6 in 635?",
           "The 6 is in the hundreds place. 6 hundreds = 600.", "600") +
        "<h2>Three ways to write a number</h2>" +
        table(["Way", "243", "706"], [
            ["Base-ten numeral", "243", "706"],
            ["Number name", "two hundred forty-three", "seven hundred six"],
            ["Expanded form", "200 + 40 + 3", "700 + 6"],
            ["Hundreds, tens, ones", "2 hundreds, 4 tens, 3 ones", "7 hundreds, 0 tens, 6 ones"],
        ]) +
        "<p>Use a hyphen for numbers like forty-three. Do not say “and” in a whole number.</p>"
        "<h2>Zero holds a place</h2>"
        "<p>706 has <b>0 tens</b>. The 0 keeps the 7 in the hundreds place. Without it, 706 would turn into 76.</p>"
        "<figure class='sn-fig'>" + chart_svg(706, hi=1) +
        "<figcaption>706 = 7 hundreds, 0 tens, 6 ones. The red 0 shows there are no tens.</figcaption></figure>" +
        ex("Write the number", "Write “three hundred six” as a number.",
           "3 hundreds, 0 tens, 6 ones. Write 3, 0, 6.", "306") +
        ex("More than 9 tens", "5 hundreds, 13 tens, 2 ones = ?",
           "13 tens = 1 hundred and 3 tens. So it is 6 hundreds, 3 tens, 2 ones.", "632") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing “three hundred six” as 3006", "Use only 3 digits: 306"],
            ["Writing 306 as 36 or 360", "Put the 0 in the tens place: 306"],
            ["Giving the digit, not its value (the 4 in 243 is 4)", "The 4 is in the tens place: 40"],
            ["Mixing up tens and ones (4 tens, 3 ones = 34)", "Tens come first: 43"],
            ["Writing 13 tens as 13 in the tens place (5132)", "13 tens = 130: 500 + 130 + 2 = 632"],
        ])
    )


FAQ = [
    {"q": "What place value should a 2nd grader know?",
     "a": "Grade 2 students learn that a 3-digit number is made of hundreds, tens and ones, and that 10 tens make 1 hundred. They read and write numbers up to 1000 as numerals, number names and expanded form."},
    {"q": "What is expanded form in 2nd grade math?",
     "a": "Expanded form shows the value of each digit as a sum. For example, 432 = 400 + 30 + 2, and 706 = 700 + 6."},
    {"q": "How do you teach place value with base-ten blocks?",
     "a": "Let the child build a number with flats (hundreds), rods (tens) and cubes (ones), then count each kind and write the digits in order. Trading 10 rods for 1 flat shows that 10 tens make 1 hundred."},
    {"q": "Why does my child write 3006 for three hundred six?",
     "a": "They write each part they hear: 300 and then 6. Show that “three hundred six” is 3 hundreds, 0 tens and 6 ones, so it has only 3 digits: 306."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (base-ten blocks) so the small cubes stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


P = None


def gen_place_value():
    global P
    rnd = random.Random(204)
    P = People(rnd)
    used = set()
    sets = [set_blocks(rnd, used), set_hto(rnd, used), set_expanded(rnd, used),
            set_names(rnd, used), set_regroup(rnd, used)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "place-value", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value to 1000: Hundreds, Tens and Ones",
        "seo_title": "Grade 2 Place Value Worksheets: Hundreds, Tens and Ones, Expanded Form and Base-Ten Blocks",
        "short_title": "Place value to 1000",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "2.NBT.A.1, 2.NBT.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/NBT/A/",
        "standard_text": "Understand that the three digits of a three-digit number represent amounts of hundreds, tens, and ones; e.g., 706 equals 7 hundreds, 0 tens, and 6 ones. Understand that 100 can be thought of as a bundle of ten tens — called a hundred. Read and write numbers to 1000 using base-ten numerals, number names, and expanded form.",
        "meta_desc": "Free Grade 2 place value worksheets: count base-ten blocks, hundreds, tens and ones, value of a digit, expanded form, number names to 1000 and regrouping like 13 tens. 100 practice questions with answers.",
        "key_big": "A 3-digit number is hundreds, tens and ones. 10 tens make 1 hundred.",
        "key_sub": "706 = 7 hundreds, 0 tens, 6 ones = 700 + 6. The 0 holds the tens place, so “seven hundred six” is 706, not 7006 or 76.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "base-ten blocks")


if __name__ == "__main__":
    u = gen_place_value()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
