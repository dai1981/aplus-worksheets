# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Place Value, Comparing and Rounding Multi-Digit Numbers (4.NBT.A.1-3)
  python tools/gen_us_math_g4_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Numbers of 1,000 or more are always written with commas.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million"]


# ------------------------------------------------------------ helpers
def c(n):
    """Number with commas: 4536 -> 4,536."""
    return "{:,}".format(n)


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
    """Number choices written with commas. Wrong numbers that are 0 or less are dropped."""
    return mcq(q, c(correct), [c(v) for v in cands if v is not None and v > 0 and v != correct], e, rnd)


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


def digit(n, i):
    return (n // 10 ** i) % 10


def ndig(n):
    return len(str(n))


# ------------------------------------------------------------ number names
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words_999(n):
    out = []
    if n >= 100:
        out.append(ONES[n // 100] + " hundred")
        n %= 100
    if n >= 20:
        out.append(TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else ""))
    elif n > 0:
        out.append(ONES[n])
    return " ".join(out)


def words(n):
    """Number name without 'and'. A comma follows 'thousand' when more words come after it."""
    if n == 1000000:
        return "one million"
    th, rest = divmod(n, 1000)
    if th and rest:
        return words_999(th) + " thousand, " + words_999(rest)
    if th:
        return words_999(th) + " thousand"
    return words_999(rest)


def expanded(n):
    return " + ".join(c(digit(n, i) * 10 ** i) for i in range(ndig(n) - 1, -1, -1) if digit(n, i))


# ------------------------------------------------------------ typical mistakes with zeros
def zero_mistakes(n):
    """Numbers a student writes when a zero goes missing, moves, or is added."""
    s = str(n)
    out = []
    for i, ch in enumerate(s):
        if ch == "0":
            t = s[:i] + s[i + 1:]                         # left out a zero
            out.append(int(t))
            for j in (i - 1, i + 1):                      # zero swapped with a neighbor
                if 0 < j < len(s) and s[j] != "0":
                    l = list(s)
                    l[i], l[j] = l[j], l[i]
                    out.append(int("".join(l)))
    for i in range(1, len(s)):                            # an extra zero
        if s[i] == "0":
            out.append(int(s[:i] + "0" + s[i:]))
    return [v for v in out if v != n and 10 <= v < 1000000]


def joined_digits(n):
    """Writing only the non-zero digits side by side (300,000 + 4,000 + 60 + 2 -> 3,462)."""
    return int("".join(ch for ch in str(n) if ch != "0"))


# ------------------------------------------------------------ figures
CW, HEAD, ROW = 74, 44, 50       # chart: column width, header height, digit row height


def chart_svg(n, cols=6, hi=None, big=False):
    """Place-value chart with n written in it. hi = place index to color red."""
    labels = [("Ones",), ("Tens",), ("Hundreds",), ("Thousands",), ("Ten", "thousands"),
              ("Hundred", "thousands"), ("Millions",)]
    x0, y0 = 6, 6
    W = x0 * 2 + CW * cols
    H = y0 * 2 + HEAD + ROW
    s = []
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
             % (x0, y0, CW * cols, HEAD + ROW, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, CW * cols, HEAD, FILL))
    for k in range(cols):
        i = cols - 1 - k                                   # place index of this column
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%d'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN, 3 if i % 3 == 2 else 1))
        lab = labels[i]
        cx = x + CW / 2
        if len(lab) == 1:
            s.append("<text x='%.1f' y='%d' font-size='14' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (cx, y0 + 27, INK, lab[0]))
        else:
            s.append("<text x='%.1f' y='%d' font-size='14' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (cx, y0 + 19, INK, lab[0]))
            s.append("<text x='%.1f' y='%d' font-size='14' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (cx, y0 + 36, INK, lab[1]))
        if i < ndig(n):
            col = RED if hi == i else INK
            s.append("<text x='%.1f' y='%d' font-size='30' font-weight='800' fill='%s' text-anchor='middle'>%d</text>"
                     % (cx, y0 + HEAD + 36, col, digit(n, i)))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + CW * cols, y0 + HEAD, GREEN))
    return svg_wrap(W, H, "".join(s), "place-value chart showing %s" % c(n))


def number_line_svg(lo, hi, n, step):
    """Number line from lo to hi, ticks every step, labels at both ends and the halfway point, red dot on n."""
    L, R, Y = 44, 376, 52
    W, H = 420, 96
    span = hi - lo
    mid = lo + span // 2

    def X(v):
        return L + (v - lo) * (R - L) / span

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, R + 10, Y, INK)]
    v = lo
    while v <= hi:
        big = v in (lo, mid, hi)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (X(v), Y - (11 if big else 6), X(v), Y + (11 if big else 6), INK, 2 if big else 1))
        if big:
            s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (X(v), Y + 32, GREEN if v != mid else "#6b6259", c(v)))
        v += step
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(n), Y, RED))
    tx = min(max(X(n), 40), W - 40)
    s.append("<text x='%.1f' y='%d' font-size='16' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (tx, Y - 18, RED, c(n)))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (c(lo), c(hi)))


# ------------------------------------------------------------ rounding
def round_to(n, p):
    return ((n + p // 2) // p) * p


def round_expl(n, p):
    """Short explanation of rounding n to place p (p = 10, 100, ...)."""
    i = len(str(p)) - 1
    r = round_to(n, p)
    lo = n // p * p
    nxt = digit(n, i - 1)
    s = ("Round to the nearest %s: %s is between %s and %s. The digit to the right of the %s place is %d, so round %s."
         % (PL1[i], c(n), c(lo), c(lo + p), PL[i], nxt, "up" if r > lo else "down"))
    if nxt == 5 and n % (p // 10) == 0:
        s = ("Round to the nearest %s: %s is exactly halfway between %s and %s. The digit to the right of the %s place is 5, "
             "and 5 rounds up." % (PL1[i], c(n), c(lo), c(lo + p), PL[i]))
    if r > lo and digit(n, i) == 9:
        s += " The %s digit is 9, so adding 1 %s regroups: %s + %s = %s." % (PL[i], PL1[i], c(lo), c(p), c(r))
    return s + " Answer: %s." % c(r)


def round_cands(n, p):
    """Wrong answers from real mistakes."""
    r = round_to(n, p)
    lo = n // p * p
    other = lo + p if r == lo else lo                     # rounded the wrong way
    keep = r + n % (p // 10) if p >= 1000 else None         # changed only two digits and kept the rest
    big = round_to(n, p * 10)                              # rounded to the place on the left
    small = round_to(n, p // 10) if p >= 100 else n        # rounded to the place on the right
    return [other, keep, small, big, r + p, r - p]


def place_name(p):
    return PL1[len(str(p)) - 1]


# ============================================================ set 1: value and place names
def set_value(rnd, used):
    its = []

    def distinct_number(k):
        while True:
            d = rnd.sample(range(10), k)
            if d[0] == 0:
                continue
            n = int("".join(map(str, d)))
            if n not in used:
                used.add(n)
                return n

    # value of a digit, with a chart (6) and without (5)
    for j in range(11):
        k = 5 if j % 3 == 0 else 6
        n = distinct_number(k)
        i = rnd.choice([x for x in range(1, k) if digit(n, x) != 0])
        d = digit(n, i)
        v = d * 10 ** i
        q = "What is the value of the digit %d in %s?" % (d, c(n))
        if j < 6:
            q = fig(chart_svg(n)) + "What is the value of the digit %d in this number?" % d
        cands = [d, d * 10 ** (i - 1), d * 10 ** (i + 1), d * 10 ** (i - 2) if i >= 2 else d * 10 ** (i + 2)]
        e = ("The %d is in the %s place, so its value is %d × %s = %s. The digit is %d, but its value is %s."
             % (d, PL[i], d, c(10 ** i), c(v), d, c(v)))
        its.append(mcq_n(q, v, cands, e, rnd))

    # which digit is in a place (4)
    for _ in range(4):
        n = distinct_number(rnd.choice([5, 6]))
        i = rnd.choice(range(2, ndig(n)))
        d = digit(n, i)
        e = ("Name the places from the right: %s. The %s digit is %d."
             % (", ".join("%s %d" % (PL[x], digit(n, x)) for x in range(i + 1)), PL[i], d))
        # the digits in the neighboring places (counted one place off), nearest first
        cands = [digit(n, x) for x in sorted(range(ndig(n)), key=lambda x: (abs(x - i), x)) if x != i]
        its.append(mcq("In %s, which digit is in the %s place?" % (c(n), PL[i]), d, cands, e, rnd))

    # name the place of a digit (3)
    for _ in range(3):
        n = distinct_number(6)
        i = rnd.choice([2, 3, 4])
        d = digit(n, i)
        if d == 0:
            i += 1
            d = digit(n, i)
        cands = [PL[i - 1], PL[i + 1], PL[i - 2], PL[i + 2] if i + 2 < 6 else PL[0]]
        its.append(mcq("In %s, what is the place of the digit %d?" % (c(n), d), PL[i], cands,
                       "Count places from the right: ones, tens, hundreds, thousands, ten thousands, hundred thousands. "
                       "The %d is in the %s place, so it is worth %s." % (d, PL[i], c(d * 10 ** i)), rnd))

    # which number has the digit in a place (2)
    for d, i in [(6, 5), (3, 4)]:
        others = [x for x in range(10) if x != d]
        rnd.shuffle(others)
        base = others[:5]                                   # five other digits, used in every choice
        if base[0] == 0:
            base[0], base[1] = base[1], base[0]
        nums = {}
        for pos in [5, 4, 3, 2]:
            ds = base[:]
            ds.insert(5 - pos, d)                           # put d at place index pos
            if ds[0] == 0:
                ds[0], ds[1] = ds[1], ds[0]
            nums[pos] = int("".join(map(str, ds)))
        assert digit(nums[i], i) == d
        wrong = [c(nums[x]) for x in nums if x != i]
        its.append(mcq("Which number has a %d in the %s place?" % (d, PL[i]), c(nums[i]), wrong,
                       "The %s place is the %s digit from the right. In %s the %d is there, so it is worth %s."
                       % (PL[i], ["1st", "2nd", "3rd", "4th", "5th", "6th"][i], c(nums[i]), d, c(d * 10 ** i)), rnd))
    return {"title": "Value of a digit and place names", "items": its}


# ============================================================ set 2: ten times the place to the right
TIMES = ["10 times", "100 times", "1,000 times", "the same"]


def set_ten_times(rnd, used):
    its = []
    # 10 × a number (4)
    for d, i in [(6, 3), (4, 2), (9, 4), (1, 5)]:
        a = d * 10 ** i
        e = ("Multiplying by 10 moves each digit one place to the left: %d %s %s %d %s. %s × 10 = %s."
             % (d, PL[i] if d > 1 else PL1[i], "become" if d > 1 else "becomes", d, PL[i + 1] if d > 1 else PL1[i + 1], c(a), c(a * 10)))
        its.append(mcq_n("What is 10 × %s?" % c(a), a * 10, [v for v in [a * 100, a, a // 10, a // 100, a * 1000] if v <= 1000000], e, rnd))
    # ÷ 10 (3)
    for d, i in [(7, 4), (5, 3), (2, 5)]:
        a = d * 10 ** i
        e = ("Dividing by 10 moves each digit one place to the right: %d %s become %d %s. %s ÷ 10 = %s."
             % (d, PL[i], d, PL[i - 1], c(a), c(a // 10)))
        its.append(mcq_n("What is %s ÷ 10?" % c(a), a // 10, [v for v in [a // 100, a * 10, a, a // 1000] if v <= 1000000], e, rnd))
    # ___ is 10 times as much as what? (4)
    for d, i in [(8, 2), (3, 4), (5, 5), (7, 3)]:
        a = d * 10 ** i
        e = ("Ask: 10 times what number is %s? One place to the right of the %s place is the %s place, so the answer is %s. Check: 10 × %s = %s."
             % (c(a), PL[i], PL[i - 1], c(a // 10), c(a // 10), c(a)))
        its.append(mcq_n("%s is 10 times as much as what number?" % c(a), a // 10, [v for v in [a // 100, a * 10, a, d] if v <= 1000000], e, rnd))
    # how many of a smaller unit (4)
    for n, j in [(900, 1), (50000, 3), (7000, 2), (200000, 4)]:
        ans = n // 10 ** j
        e = ("Each place is 10 times the place to its right. %s = %s %s, because %s × %s = %s."
             % (c(n), c(ans), PL[j], c(ans), c(10 ** j), c(n)))
        cands = [int(str(n)[0]), ans // 10, ans * 10, n, n * 10]
        its.append(mcq_n("How many %s are in %s?" % (PL[j], c(n)), ans, cands, e, rnd))
    # two equal digits (5)
    specs = [(3, 4, 1), (5, 2, 1), (7, 3, 1), (4, 5, 1), (8, 3, 2)]
    for d, i, gap in specs:
        while True:
            k = rnd.choice([5, 6]) if i < 5 else 6
            if i + 1 > k:
                continue
            ds = [rnd.choice([x for x in range(10) if x != d]) for _ in range(k)]
            ds = ds[::-1]                                  # ds[x] = digit at place x (ones first)
            ds[i], ds[i - gap] = d, d
            if ds[k - 1] == 0:
                continue
            n = sum(ds[x] * 10 ** x for x in range(k))
            if n not in used:
                used.add(n)
                break
        a, b = d * 10 ** i, d * 10 ** (i - gap)
        ans = TIMES[gap - 1]
        e = ("The %d on the left is in the %s place: %s. The %d on the right is in the %s place: %s. %s = %d × %s, so it is worth %s as much."
             % (d, PL[i], c(a), d, PL[i - gap], c(b), c(a), 10 ** gap, c(b), ans))
        its.append(mcq("Look at the two %ds in %s. The %d on the left is worth how many times as much as the %d on the right?"
                       % (d, c(n), d, d), ans, [t for t in TIMES if t != ans], e, rnd))
    return {"title": "Each place is 10 times the place to its right", "items": its}


# ============================================================ set 3: standard, word and expanded form
def with_zero(rnd, used, k):
    """A k-digit number with one or two zeros inside (the tricky ones)."""
    while True:
        ds = [rnd.randint(1, 9)] + [rnd.randint(0, 9) for _ in range(k - 1)]
        z = sum(1 for x in ds[1:] if x == 0)
        n = int("".join(map(str, ds)))
        if 1 <= z <= 3 and n not in used and len(zero_mistakes(n)) >= 3:
            used.add(n)
            return n


def set_forms(rnd, used):
    its = []
    # word form -> standard form (6)
    fixed = [40006, 305040]
    for j in range(6):
        n = fixed[j] if j < 2 else with_zero(rnd, used, [5, 6, 6, 5][j - 2])
        used.add(n)
        cands = zero_mistakes(n)
        rnd.shuffle(cands)
        th, rest = divmod(n, 1000)
        e = ("Before the comma, write the thousands: “%s thousand” → %s. After the comma, always write 3 digits: “%s” → %s. "
             "So the number is %s." % (words_999(th), c(th), words_999(rest), "%03d" % rest, c(n)))
        its.append(mcq_n("Write this number in standard form: <b>%s</b>" % words(n), n, cands, e, rnd))
    # standard form -> word form (5)
    for j in range(5):
        n = with_zero(rnd, used, 6 if j % 2 == 0 else 5)
        cands = [words(v) for v in zero_mistakes(n) if v >= 1000]
        rnd.shuffle(cands)
        th, rest = divmod(n, 1000)
        e = ("Read the number before the comma, then say “thousand”, then read the last 3 digits: %s thousand, %s. "
             "Do not say “and” in a whole number." % (words_999(th), words_999(rest)))
        if not rest:
            e = "Read the number before the comma, then say “thousand”: %s thousand." % words_999(th)
        its.append(mcq("Which is %s in word form?" % c(n), words(n), cands, e, rnd))
    # standard form -> expanded form (5)
    for j in range(5):
        n = with_zero(rnd, used, 5 if j < 3 else 6)
        cands = [expanded(v) for v in zero_mistakes(n)]
        rnd.shuffle(cands)
        e = ("Write the value of each non-zero digit and add: %s. A zero adds nothing, so it does not get its own part."
             % expanded(n))
        its.append(mcq("Which shows %s in expanded form?" % c(n), expanded(n), cands, e, rnd))
    # expanded form -> standard form (4)
    for j in range(4):
        n = with_zero(rnd, used, 6 if j % 2 == 0 else 5)
        cands = [joined_digits(n)] + zero_mistakes(n)
        e = ("Put each digit in its place and write 0 in any place that is missing: %s = %s."
             % (expanded(n), c(n)))
        its.append(mcq_n("What number is <b>%s</b>?" % expanded(n), n, cands, e, rnd))
    return {"title": "Standard form, word form and expanded form", "items": its}


# ============================================================ set 4: compare and order
def first_diff(a, b):
    """Place index where a and b first differ, reading from the left (same number of digits)."""
    for i in range(ndig(a) - 1, -1, -1):
        if digit(a, i) != digit(b, i):
            return i
    return None


def compare_expl(big, small):
    if ndig(big) != ndig(small):
        return "%s has %d digits and %s has only %d, so %s is greater." % (c(big), ndig(big), c(small), ndig(small), c(big))
    i = first_diff(big, small)
    same = "Both have the same digits until the %s place" % PL[i] if i < ndig(big) - 1 else "Start at the %s place" % PL[i]
    return ("Line up the places and compare from the left. %s: %d %s is more than %d %s. So %s &gt; %s."
            % (same, digit(big, i), PL[i] if digit(big, i) != 1 else PL1[i],
               digit(small, i), PL[i] if digit(small, i) != 1 else PL1[i], c(big), c(small)))


def lt_step(small, big):
    i = first_diff(big, small)
    return "%s &lt; %s, because in the %s place %d &lt; %d." % (c(small), c(big), PL[i], digit(small, i), digit(big, i))


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


def lookalikes(rnd, k):
    """4 different k-digit numbers that use the same digits (easy to mix up)."""
    while True:
        ds = rnd.sample(range(1, 10), k)
        base = int("".join(map(str, ds)))
        out = {base}
        tries = 0
        while len(out) < 4 and tries < 50:
            tries += 1
            l = ds[:]
            a, b = rnd.sample(range(k), 2)
            if min(a, b) < k - 4:                          # keep most of the left digits the same
                continue
            l[a], l[b] = l[b], l[a]
            out.add(int("".join(map(str, l))))
        if len(out) == 4:
            return sorted(out)


def set_compare(rnd, used, P):
    its = []
    # greatest (5) and least (4)
    for j in range(9):
        k = [5, 5, 6, 6, 6, 5, 6, 5, 6][j]
        nums = lookalikes(rnd, k)
        want_max = j < 5
        ans = nums[-1] if want_max else nums[0]
        nxt = nums[-2] if want_max else nums[1]
        e = compare_expl(ans, nxt) if want_max else compare_expl(nxt, ans).replace(
            "So %s &gt; %s." % (c(nxt), c(ans)), "So %s &lt; %s, and %s is the least." % (c(ans), c(nxt), c(ans)))
        if want_max:
            e += " %s is the greatest." % c(ans)
        its.append(mcq("Which number is the %s?" % ("greatest" if want_max else "least"), c(ans),
                       [c(v) for v in nums if v != ans], e, rnd))
    # more digits beats a bigger first digit (2)
    for big, smalls in [(102345, [98765, 99870, 97531]), (100204, [99999, 91004, 89990])]:
        e = ("%s has 6 digits. The other numbers have only 5 digits, so they are less than 100,000. "
             "A bigger first digit does not matter when there are fewer digits. %s is the greatest." % (c(big), c(big)))
        its.append(mcq("Which number is the greatest?", c(big), [c(v) for v in smalls], e, rnd))
    # which comparison is true (5)
    for j in range(5):
        while True:
            k = rnd.choice([5, 6])
            a = rnd.randint(10 ** (k - 1), 10 ** k - 1)
            i = rnd.randint(1, k - 2)                      # b differs from a first at place i
            hi_part = a // 10 ** (i + 1)
            da = digit(a, i)
            db = rnd.choice([x for x in range(10) if x != da])
            b = hi_part * 10 ** (i + 1) + db * 10 ** i + rnd.randint(0, 10 ** i - 1)
            if ndig(b) == k and a not in used and b not in used and a != b:
                used.update([a, b])
                break
        big, small = max(a, b), min(a, b)
        x, y = (a, b) if j % 2 == 0 else (b, a)
        right = "%s %s %s" % (c(x), "&lt;" if x < y else "&gt;", c(y))
        wrong = ["%s %s %s" % (c(x), "&gt;" if x < y else "&lt;", c(y)), "%s = %s" % (c(x), c(y)),
                 "%s %s %s" % (c(y), "&lt;" if x < y else "&gt;", c(x))]
        its.append(mcq("Which comparison is true?", right, wrong, compare_expl(big, small), rnd))
    # order from least to greatest, with a story (4)
    stories = [
        ("Three baseball games had these crowds: %s fans, %s fans and %s fans.", 5),
        ("Three towns have these populations: %s people, %s people and %s people.", 5),
        ("Three trucks have driven %s miles, %s miles and %s miles.", 6),
        ("Last month, three websites had %s visits, %s visits and %s visits.", 6),
    ]
    for t, k in stories:
        while True:
            nums = lookalikes(rnd, k)
            three = rnd.sample(nums, 3)
            if three != sorted(three):
                break
        order = sorted(three)
        perms = [[order[0], order[2], order[1]], [order[1], order[0], order[2]], three[::-1] if three[::-1] != order else order[::-1],
                 order[::-1], [order[2], order[0], order[1]]]
        fmt = lambda l: "; ".join(c(v) for v in l)
        e = "Compare from the left. %s %s So the order is %s." % (lt_step(order[0], order[1]), lt_step(order[1], order[2]), fmt(order))
        its.append(mcq((t % tuple(c(v) for v in three)) + " Which list shows the numbers from least to greatest?",
                       fmt(order), [fmt(p) for p in perms], e, rnd))
    return {"title": "Compare and order multi-digit numbers", "items": its}


# ============================================================ set 5: round to any place
def set_round(rnd, used, P):
    its = []
    # with a number line (6)
    for n, p in [(3482, 100), (96500, 1000), (64350, 10000), (28716, 1000), (372904, 100000), (845230, 10000)]:
        lo = n // p * p
        q = fig(number_line_svg(lo, lo + p, n, p // 10)) + "Round %s to the nearest %s." % (c(n), place_name(p))
        its.append(mcq_n(q, round_to(n, p), round_cands(n, p), round_expl(n, p), rnd))
    # without a picture, every place, tricky ones included (6)
    for n, p in [(38465, 10), (499999, 1000), (79581, 100), (209617, 10000), (649999, 100000), (51962, 1000)]:
        cands = round_cands(n, p)
        if n == 499999:
            cands = [499000, 400000, 499900, 510000]
        its.append(mcq_n("Round %s to the nearest %s." % (c(n), place_name(p)), round_to(n, p), cands,
                         round_expl(n, p), rnd))
    # word problems (8)
    name, she, her = P.next()
    stories = [
        ("A city has %s people. What is its population rounded to the nearest ten thousand?", 284516, 10000, " people"),
        ("At a baseball game, %s fans were in the stadium. A news report rounds this to the nearest thousand. "
         "What number does the report give?", 41736, 1000, " fans"),
        ("%s's family drove %%s miles on a road trip. What is that distance rounded to the nearest hundred?" % name,
         1486, 100, " miles"),
        ("A video has %s views. Rounded to the nearest hundred thousand, about how many views is that?",
         349612, 100000, " views"),
        ("A school district has %s students. What is that number rounded to the nearest hundred?", 24951, 100, " students"),
    ]
    for t, n, p, u in stories:
        r = round_to(n, p)
        its.append(mcq(t % c(n), c(r) + u, [c(v) + u for v in round_cands(n, p) if v and v > 0 and v != r],
                       round_expl(n, p), rnd))
    its.append(mcq("A park had 72,480 visitors this year. A sign says “about 72,000 visitors.” "
                   "To which place was the number rounded?", "nearest thousand",
                   ["nearest hundred", "nearest ten thousand", "nearest ten"],
                   "72,480 to the nearest thousand: the hundreds digit is 4, so round down to 72,000. "
                   "To the nearest hundred it would be 72,500, and to the nearest ten thousand it would be 70,000.", rnd))
    its.append(mcq("What is the greatest whole number that rounds to 50,000 when you round to the nearest thousand?",
                   "50,499", ["50,500", "50,999", "49,500"],
                   "Numbers from 49,500 to 50,499 round to 50,000. 50,500 has a 5 in the hundreds place, so it rounds up to 51,000.",
                   rnd))
    its.append(mcq("A concert sold about 30,000 tickets, rounded to the nearest ten thousand. "
                   "Which could be the exact number of tickets sold?", "25,104",
                   ["35,200", "24,870", "38,000"],
                   "Numbers from 25,000 to 34,999 round to 30,000. 25,104 is in that range. 35,200 and 38,000 round up to 40,000, "
                   "and 24,870 rounds down to 20,000.", rnd))
    tail = its[12:]
    rnd.shuffle(tail)
    return {"title": "Round to any place and word problems", "items": its[:12] + tail}


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
        "<h2>Each place is 10 times the place to its right</h2>"
        "<p>A digit's <b>value</b> depends on its <b>place</b>. Move one place to the left, and the value becomes "
        "<b>10 times as much</b>. 10 ones make 1 ten, 10 tens make 1 hundred, 10 hundreds make 1 thousand, and so on.</p>"
        "<figure class='sn-fig'>" + chart_svg(472615, hi=4) +
        "<figcaption>In 472,615 the 7 is in the ten thousands place, so its value is 70,000. "
        "The comma separates the thousands from the hundreds, tens and ones.</figcaption></figure>" +
        ex("Ten times", "In 44,000, how does the first 4 compare to the second 4?",
           "The first 4 is in the ten thousands place: 40,000. The second 4 is in the thousands place: 4,000. "
           "40,000 = 10 × 4,000.", "The first 4 is worth 10 times as much") +
        "<h2>Three ways to write a number</h2>" +
        table(["Form", "305,040"], [
            ["Standard form", "305,040"],
            ["Word form", "three hundred five thousand, forty"],
            ["Expanded form", "300,000 + 5,000 + 40"],
        ]) +
        "<p>In word form, read the part before the comma, say “thousand”, then read the last 3 digits. "
        "Never say “and” in a whole number. In standard form, write a <b>0</b> in every empty place.</p>"
        "<h2>Compare from the left</h2>"
        "<p>First count the digits: more digits means a greater number. If they have the same number of digits, "
        "compare place by place from the left until two digits are different.</p>" +
        ex("Compare", "45,309 ☐ 45,390",
           "Ten thousands: 4 = 4. Thousands: 5 = 5. Hundreds: 3 = 3. Tens: 0 &lt; 9.", "45,309 &lt; 45,390") +
        "<h2>Round to any place</h2>"
        "<ol class='rk-step'><li>Find the digit in the place you are rounding to.</li>"
        "<li>Look at the digit <b>one place to its right</b>.</li>"
        "<li><b>5 or more</b>: add 1 to the rounding digit. <b>4 or less</b>: keep it.</li>"
        "<li>Change every digit to the right of the rounding place to 0. Digits on the left stay the same, unless a 9 regroups.</li></ol>"
        "<figure class='sn-fig'>" + number_line_svg(96000, 97000, 96500, 100) +
        "<figcaption>96,500 is exactly halfway between 96,000 and 97,000. A 5 rounds up, so 96,500 rounds to 97,000.</figcaption></figure>" +
        table(["Round 284,516 to the nearest", "Look at", "Answer"], [
            ["ten", "6 ones", "284,520"],
            ["hundred", "1 ten", "284,500"],
            ["thousand", "5 hundreds", "285,000"],
            ["ten thousand", "4 thousands", "280,000"],
            ["hundred thousand", "8 ten thousands", "300,000"],
        ]) +
        ex("Watch the 9s", "Round 499,999 to the nearest thousand.",
           "The thousands digit is 9. The digit to its right is 9, so round up. 499,000 + 1,000 = 500,000.", "500,000") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Giving the digit, not its value (the 7 in 472,615 is 7)", "Multiply by the place: 7 × 10,000 = 70,000"],
            ["Leaving out zeros (forty thousand six = 4,006)", "Write 3 digits after the comma: 40,006"],
            ["Comparing the first digits only (98,765 &gt; 102,345)", "Count the digits first: 6 digits beat 5 digits"],
            ["Rounding 96,500 down to 96,000", "A 5 rounds up: 97,000"],
            ["Rounding to the wrong place (64,350 to the nearest ten thousand = 64,000)", "Find the ten thousands digit first: 60,000"],
        ])
    )


FAQ = [
    {"q": "What place value should a 4th grader know?",
     "a": "Grade 4 students work with whole numbers up to 1,000,000. They read and write them in standard, word and expanded form, and know that each place is worth 10 times the place to its right."},
    {"q": "What is expanded form in 4th grade math?",
     "a": "Expanded form writes a number as the sum of the values of its digits. For example, 52,078 = 50,000 + 2,000 + 70 + 8."},
    {"q": "How do you round to the nearest ten thousand?",
     "a": "Find the ten thousands digit, then look at the thousands digit to its right. If it is 5 or more, round up; if it is 4 or less, round down. 64,350 rounds to 60,000."},
    {"q": "How do you compare two large numbers?",
     "a": "Count the digits first; the number with more digits is greater. If they have the same number of digits, compare from the left until two digits are different."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (wide charts and number lines) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_place_value():
    rnd = random.Random(108)
    P = People(rnd)
    used = set()
    sets = [set_value(rnd, used), set_ten_times(rnd, used), set_forms(rnd, used),
            set_compare(rnd, used, P), set_round(rnd, used, P)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    u = {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "place-value-rounding", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value, Comparing and Rounding Multi-Digit Numbers",
        "seo_title": "Grade 4 Place Value and Rounding Worksheets: Expanded Form, Comparing and Rounding to Any Place",
        "short_title": "Place value and rounding",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "4.NBT.A.1–3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NBT/A/",
        "standard_text": "Recognize that in a multi-digit whole number, a digit in one place represents ten times what it represents in the place to its right. Read and write multi-digit whole numbers using base-ten numerals, number names, and expanded form. Compare two multi-digit numbers based on meanings of the digits in each place, using >, =, and < symbols. Use place value understanding to round multi-digit whole numbers to any place.",
        "meta_desc": "Free Grade 4 place value worksheets: value of a digit up to 1,000,000, ten times the place to the right, standard, word and expanded form, comparing with >, = and <, and rounding to any place with number lines. 100 practice questions with answers.",
        "key_big": "Each place is worth 10 times the place to its right. Compare from the left; round by looking one place to the right.",
        "key_sub": "The 7 in 70,000 is worth 10 times the 7 in 7,000. Write a 0 in every empty place, count digits before comparing, and remember that a 5 rounds up.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(place-value chart|number line)")


if __name__ == "__main__":
    u = gen_place_value()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
