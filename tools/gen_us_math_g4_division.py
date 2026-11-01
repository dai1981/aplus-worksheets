# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Long Division (4.NBT.B.6)
  python tools/gen_us_math_g4_division.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
PLACE = ["ones", "tens", "hundreds", "thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 4 style: commas in numbers of 1,000 and more."""
    return "{:,}".format(n)


def qr(q, r):
    return "%s R %d" % (f(q), r) if r else f(q)


def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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


def units(k, one, many):
    return "%s %s" % (f(k), one if k == 1 else many)


# ------------------------------------------------------------ long division, step by step
def ld_rows(n, d):
    """The steps of long division: list of (index of digit, partial dividend, quotient digit)."""
    ds = [int(c) for c in str(n)]
    cur, steps, started = 0, [], False
    for i, x in enumerate(ds):
        cur = cur * 10 + x
        if not started and cur < d and i < len(ds) - 1:
            continue
        started = True
        q = cur // d
        steps.append((i, cur, q))
        cur -= q * d
    return steps, cur


def ld_steps(n, d, end=True):
    """Divide, multiply, subtract, bring down — in words. Ends with the answer and a check."""
    ds = str(n)
    steps, r = ld_rows(n, d)
    q = n // d
    parts = []
    for k, (i, cur, qd) in enumerate(steps):
        if k == 0:
            head = ("%s is less than %d, so start with %d. " % (ds[0], d, cur)) if i > 0 else ""
            parts.append(head + "%d ÷ %d = %d, %d × %d = %d, %d − %d = %d."
                         % (cur, d, qd, qd, d, qd * d, cur, qd * d, cur - qd * d))
        elif qd == 0:
            parts.append("Bring down %s: %d ÷ %d = 0, so write 0 in the quotient." % (ds[i], cur, d))
        else:
            parts.append("Bring down %s: %d ÷ %d = %d, %d × %d = %d, %d − %d = %d."
                         % (ds[i], cur, d, qd, qd, d, qd * d, cur, qd * d, cur - qd * d))
    if r:
        parts.append("Nothing is left to bring down, so the remainder is %d." % r)
    chk = ("Check: %s × %d + %d = %s." % (f(q), d, r, f(n))) if r else ("Check: %s × %d = %s." % (f(q), d, f(n)))
    if end:
        parts.append("Answer: %s. %s" % (qr(q, r), chk))
    else:
        parts.append("So %s ÷ %d = %s. %s" % (f(n), d, qr(q, r), chk))
    return " ".join(parts)


# ------------------------------------------------------------ typical mistakes
def digitwise(n, d):
    """Dividing each digit on its own and throwing the remainders away (456 ÷ 3 → 112)."""
    return int("".join(str(int(c) // d) for c in str(n)))


def drop_zero(q):
    """Skipping the 0 in the quotient (703 → 73)."""
    s = str(q).replace("0", "")
    return int(s) if s else 0


def no_rem_cands(n, d):
    q = n // d
    c = []
    if "0" in str(q):
        c.append(drop_zero(q))
    if int(str(n)[0]) >= d:
        c.append(digitwise(n, d))
    if q >= 100:
        c.append(q // 10)                                    # stopped before the last bring down
    c.append(q * 10)                                         # started one place too far left
    return [f(x) for x in c + [q + 10, q - 10, q + 1, q - 1, q + 100]]


def rem_cands(n, d):
    q, r = n // d, n % d
    c = []
    if "0" in str(q):
        c.append(qr(drop_zero(q), r))
    c += [qr(q - 1, r + d),                                  # remainder bigger than the divisor
          f(q),                                              # left the remainder out
          qr(q, d - r),                                      # wrote how many more are needed
          qr(q + 1, r), qr(q - 1, r)]
    return c


# ------------------------------------------------------------ figures
FS = 24                       # digit size in question figures


def bracket_svg(n, d, fs=FS, work=False):
    """Long division layout: divisor, bracket and dividend. With work=True, the full worked
    example (quotient, products, differences, brought-down digits) is drawn."""
    cw = fs * 0.85                                           # column width (room for the comma)
    ds = str(n)
    L = len(ds)
    dw = len(str(d)) * fs * 0.62
    x0 = 10 + dw + 18                                        # left edge of the dividend columns
    steps, r = ld_rows(n, d)
    q = n // d
    rh = fs * 1.25
    top = (rh + 6) if work else 10                          # bar height
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    def digits_at(txt, last, y, colr=INK):
        for k, ch in enumerate(reversed(txt)):
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (col(last - k), y, fs, colr, ch))

    by = top + rh - fs * 0.18                                # dividend baseline
    digits_at(ds, L - 1, by)
    if L >= 4:                                               # comma between thousands and hundreds
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                 "font-family='monospace'>,</text>" % (x0 + cw * (L - 3), by + fs * 0.08, int(fs * 0.8), INK))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end' "
             "font-family='monospace'>%d</text>" % (x0 - 14, by, fs, GREEN, d))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * L + 8
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0 - 6, top, W - 4, top, INK))
    H = top + bh + 8
    if work:
        digits_at(str(q), L - 1, top - 8, GREEN)
        if r:
            rt = "R %d" % r
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' font-family='monospace'>%s</text>"
                     % (x0 + cw * L + 12, top - 8, fs, GREEN, rt))
            W = max(W, x0 + cw * L + 12 + len(rt) * fs * 0.62 + 8)
        y = by
        for k, (i, cur, qd) in enumerate(steps):
            p = qd * d
            y += rh
            digits_at(str(p), i, y)
            left = i - len(str(max(p, cur))) + 1
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>−</text>"
                     % (col(left) - cw * 0.85, y, fs, RED))
            ly = y + fs * 0.3
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (col(left) - cw * 1.2, ly, col(i) + cw * 0.5, ly, INK))
            y += rh
            diff = cur - p
            if k + 1 < len(steps):
                nxt = steps[k + 1][1]                       # difference with the next digit brought down
                digits_at(str(nxt), i + 1, y)
                s.append("<path d='M%.1f %.1f V%.1f' stroke='%s' stroke-width='1.5' stroke-dasharray='3 3' "
                         "marker-end='url(#ah)'/>" % (col(i + 1), by + fs * 0.3, y - fs * 0.95, GREEN))
            else:
                digits_at(str(diff), i, y, GREEN if diff else INK)
        H = y + 12
        s.insert(0, "<defs><marker id='ah' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='6' markerHeight='6' "
                    "orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % GREEN)
    label = ("%s divided by %d worked out with long division" if work else "%s divided by %d written as long division") % (f(n), d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label)


def tw(t, fs):
    return len(str(t)) * fs * 0.6


def area_svg(d, parts, tops):
    """Area model: a rectangle with the divisor on the side, split into parts (area written inside).
    tops: label above each part (partial quotient, or '?')."""
    fs = 18
    xs = 40
    ws = [max(70, tw(f(p), fs) + 24) for p in parts]
    y0, h = 34, 58
    s = []
    x = xs
    for p, t, w in zip(parts, tops, ws):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x, y0, w, h, FILL, GREEN))
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + w / 2, y0 + h / 2 + 6, fs, INK, f(p)))
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + w / 2, y0 - 10, fs, RED if t == "?" else GREEN, t))
        x += w
    s.append("<text x='%d' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
             % (xs - 16, y0 + h / 2 + 6, fs, GREEN, d))
    W, H = int(x + 8), y0 + h + 8
    return svg_wrap(W, H, "".join(s), "area model for %s divided by %d" % (f(sum(parts)), d))


def area_parts(n, d):
    """Split n into place-value parts that d divides evenly (852, 4 → 800, 40, 12)."""
    parts, rest = [], n
    for scale in (1000, 100, 10):
        k = (rest // scale) // d * d * scale
        if k:
            parts.append(k)
            rest -= k
    if rest:
        parts.append(rest)
    return parts


# ------------------------------------------------------------ set 1: basic facts with tens and hundreds
def set_facts(rnd, used):
    its = []
    pairs = [(dd, qq) for dd in range(3, 10) for qq in range(2, 10) if dd * qq >= 12]
    rnd.shuffle(pairs)

    def take(scale, zero_fact=None):
        while True:
            dd, qq = pairs.pop(0)
            fact = dd * qq
            if zero_fact is not None and (fact % 10 == 0) != zero_fact:
                pairs.append((dd, qq))
                continue
            n = fact * scale
            if n in used or n > 9999:
                pairs.append((dd, qq))
                continue
            used.add(n)
            return n, dd, qq, fact

    # 1) 6 with tens, 6 with hundreds, 2 where the basic fact itself ends in 0 (4,000 ÷ 5)
    plan = [(10, False)] * 6 + [(100, False)] * 6 + [(100, True), (10, True)]
    for scale, zf in plan:
        n, dd, qq, fact = take(scale, zf)
        q = n // dd
        name = "tens" if scale == 10 else "hundreds"
        e = "%s is %d %s. %d ÷ %d = %d, so %d %s ÷ %d = %d %s = %s." % (f(n), fact, name, fact, dd, qq, fact, name, dd, qq, name, f(q))
        if zf:
            e += " Be careful: %s has %d zeros, but one of them belongs to the fact %d ÷ %d." % (f(n), str(n).count("0"), fact, dd)
        e += " Check: %s × %d = %s." % (f(q), dd, f(n))
        cands = [f(q // 10), f(q * 10), f((qq + 1) * scale), f((qq - 1) * scale)]
        if zf:
            cands = [f(q * 10), f(q // 10)] + cands
        its.append(mcq("What is %s ÷ %d?" % (f(n), dd), f(q), cands, e, rnd))
    # 2) think in place-value units: 28 hundreds ÷ 7 = 4 hundreds
    for scale in (100, 10, 100):
        n, dd, qq, fact = take(scale, False)
        name = "tens" if scale == 10 else "hundreds"
        other = "ones" if scale == 10 else "tens"
        e = ("%s is %d %s. Share %d %s into %d equal groups: %d ÷ %d = %d, so each group gets %d %s. "
             "%d %s = %s. Check: %s × %d = %s."
             % (f(n), fact, name, fact, name, dd, fact, dd, qq, qq, name, qq, name, f(n // dd), f(n // dd), dd, f(n)))
        its.append(mcq("%s is %d %s. What is %d %s ÷ %d?" % (f(n), fact, name, fact, name, dd),
                       "%d %s" % (qq, name), ["%d %s" % (qq, other), "%d %s" % (qq * 10, name), "%d ones" % qq, "%d %s" % (qq + 1, name)],
                       e, rnd))
    # 3) missing factor: division is the opposite of multiplication
    for scale in (100, 10, 100):
        n, dd, qq, fact = take(scale, False)
        q = n // dd
        e = "Think: %d times what number is %s? That is %s ÷ %d. %d ÷ %d = %d, so the answer is %s. Check: %s × %d = %s." % (
            dd, f(n), f(n), dd, fact, dd, qq, f(q), f(q), dd, f(n))
        its.append(mcq("What number goes in the box?  <b>☐ × %d = %s</b>" % (dd, f(n)), f(q),
                       [f(q // 10), f(q * 10), f((qq + 1) * scale), f((qq - 1) * scale)], e, rnd))
    rnd.shuffle(its)
    return {"title": "Divide tens and hundreds using basic facts", "items": its}


# ------------------------------------------------------------ set 2: no remainder
def pick(rnd, used, lo, hi, d_lo=2, rem=False, zero_q=None, first_small=None, regroup=False):
    while True:
        d = rnd.randint(d_lo, 9)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if (r != 0) != rem or n in used or q < 10:
            continue
        if zero_q is not None and ("0" in str(q)) != zero_q:
            continue
        if first_small is not None and (int(str(n)[0]) < d) != first_small:
            continue
        if regroup and int(str(n)[0]) % d == 0:                  # first step leaves nothing to regroup
            continue
        used.add(n)
        return n, d


def item_div(n, d, rnd, figure):
    q, r = divmod(n, d)
    if figure:
        qtxt = fig(bracket_svg(n, d)) + "Divide."
    else:
        qtxt = "What is %s ÷ %d?" % (f(n), d)
    cands = rem_cands(n, d) if r else no_rem_cands(n, d)
    return mcq(qtxt, qr(q, r), cands, ld_steps(n, d), rnd)


def item_area(n, d, rnd):
    parts = area_parts(n, d)
    tops = [f(p // d) for p in parts]
    q = n // d
    fig_ = fig(area_svg(d, parts, ["?"] * len(parts)))
    e = ("The model splits %s into %s. Divide each part by %d: %s. Add the parts of the quotient: %s = %s. Check: %s × %d = %s."
         % (f(n), " + ".join(f(p) for p in parts), d,
            ", ".join("%s ÷ %d = %s" % (f(p), d, t) for p, t in zip(parts, tops)),
            " + ".join(tops), f(q), f(q), d, f(n)))
    pq = [p // d for p in parts]
    cands = [f(q - pq[-1]), f(q - pq[1]) if len(pq) > 2 else f(q * 10)]
    if len(pq) > 1 and pq[1] >= 10:                                  # 40 ÷ 4 written as 1
        cands.append(f(q - pq[1] + pq[1] // 10))
    cands += [f(q + 10), f(q * 10)]
    return mcq(fig_ + "Use the area model to find %s ÷ %d." % (f(n), d), f(q), cands, e, rnd)


def set_no_rem(rnd, used):
    its = []
    for i in range(6):
        n, d = pick(rnd, used, 36, 98, d_lo=3, zero_q=False, regroup=True)
        its.append(item_div(n, d, rnd, False))
    for i in range(10):
        n, d = pick(rnd, used, 112, 990, d_lo=3, zero_q=False, first_small=(i % 3 == 0))
        its.append(item_div(n, d, rnd, i % 2 == 0))
    area = 0
    while area < 4:
        d = rnd.randint(3, 8)
        q = rnd.randint(112, 199) if d <= 4 else rnd.randint(41, 99)
        n = q * d
        parts = area_parts(n, d)
        if n in used or n > 999 or len(parts) < 3 or "0" in str(q):
            continue
        used.add(n)
        its.append(item_area(n, d, rnd))
        area += 1
    rnd.shuffle(its)
    return {"title": "Divide 2- and 3-digit numbers", "items": its}


# ------------------------------------------------------------ set 3: remainders
def set_rem(rnd, used, P):
    its = []
    for i in range(6):
        n, d = pick(rnd, used, 37, 99, d_lo=3, rem=True)
        its.append(item_div(n, d, rnd, False))
    for i in range(8):
        n, d = pick(rnd, used, 113, 989, d_lo=3, rem=True, zero_q=False, first_small=(i % 2 == 0))
        its.append(item_div(n, d, rnd, i % 2 == 1))
    # the remainder is asked for
    for _ in range(2):
        n, d = pick(rnd, used, 120, 980, d_lo=4, rem=True, zero_q=False)
        q, r = divmod(n, d)
        its.append(mcq("What is the remainder when %s is divided by %d?" % (f(n), d), str(r),
                       [f(q), str(d - r), str(r + d), str(d)], "The question asks for the remainder, not the quotient. " + ld_steps(n, d), rnd))
    # check by multiplying
    for _ in range(2):
        n, d = pick(rnd, used, 120, 980, d_lo=3, rem=True, zero_q=False)
        q, r = divmod(n, d)
        good = "%d × %d + %d" % (d, q, r)
        its.append(mcq("%s ÷ %d = %s. Which expression checks this answer? It should equal %s." % (f(n), d, qr(q, r), f(n)), good,
                       ["%d × %d − %d" % (d, q, r), "%d × %d + %d" % (q, r, d), "%d + %d + %d" % (d, q, r)],
                       "Multiply the quotient by the divisor, then add the remainder: %d × %d = %s, %s + %d = %s. "
                       "It matches the dividend, so the answer is right." % (d, q, f(d * q), f(d * q), r, f(n)), rnd))
    # remainder bigger than the divisor
    for _ in range(2):
        name, he, his = P.next()
        n, d = pick(rnd, used, 50, 99, d_lo=4, rem=True)
        q, r = divmod(n, d)
        good = "The remainder is too big"
        its.append(mcq("%s says %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q - 1, r + d), he), good,
                       ["%s forgot to bring down" % cap(he), "%s should not have a remainder" % cap(he), "There is no mistake"],
                       "The remainder must be less than the divisor. %d is more than %d, so %d more fits: %d − %d = %d. "
                       "The answer is %s. Check: %d × %d + %d = %d." % (r + d, d, d, r + d, d, r, qr(q, r), q, d, r, n), rnd))
    rnd.shuffle(its)
    return {"title": "Divide with remainders", "items": its}


# ------------------------------------------------------------ set 4: four-digit dividends and zeros
def set_four(rnd, used):
    its = []
    # zeros in the quotient, no remainder
    k = 0
    while k < 8:
        d = rnd.randint(3, 9)
        qs = rnd.choice(["x0y", "x0y", "xy0", "1x0y"]) if k < 7 else "x0y"
        q = int(qs.replace("x", str(rnd.randint(1, 9))).replace("y", str(rnd.randint(1, 9))))
        n = q * d
        if n in used or n < 1000 or n > 9999:
            continue
        used.add(n)
        its.append(item_div(n, d, rnd, k % 2 == 0))
        k += 1
    # four digits, no zero in the quotient
    for i in range(4):
        n, d = pick(rnd, used, 1100, 9800, d_lo=3, zero_q=False, first_small=(i % 2 == 0))
        its.append(item_div(n, d, rnd, i % 2 == 1))
    # zeros and a remainder
    k = 0
    while k < 4:
        d = rnd.randint(4, 9)
        q = rnd.randint(1, 9) * 100 + rnd.randint(1, 9)
        r = rnd.randint(1, d - 1)
        n = q * d + r
        if n in used or n < 1000:
            continue
        used.add(n)
        its.append(item_div(n, d, rnd, k % 2 == 1))
        k += 1
    # where does the first digit go / how many digits
    for n, d in [(2156, 7), (4635, 3)]:
        steps, _ = ld_rows(n, d)
        i = steps[0][0]
        place = PLACE[len(str(n)) - 1 - i]
        first = str(n)[0]
        why = ("%s is less than %d, so there are no thousands in the quotient. Start with %d hundreds: %d ÷ %d = %d."
               % (first, d, steps[0][1], steps[0][1], d, steps[0][2])) if i else (
            "%s is at least %d, so you can divide the thousands: %s ÷ %d = %d." % (first, d, first, d, steps[0][2]))
        its.append(mcq("You divide %s ÷ %d with long division. Above which place do you write the first digit of the quotient?" % (f(n), d),
                       "the %s place" % place, ["the %s place" % p for p in ["thousands", "hundreds", "tens", "ones"] if p != place],
                       why + " The quotient is %s." % qr(n // d, n % d), rnd))
    for n, d in [(3248, 8), (7236, 6)]:
        q = n // d
        nd = len(str(q))
        first = int(str(n)[0])
        why = ("%d is less than %d, so the quotient has no thousands digit. " % (first, d)) if first < d else (
            "%d is at least %d, so the quotient starts in the thousands. " % (first, d))
        its.append(mcq("How many digits does the quotient of %s ÷ %d have?" % (f(n), d), "%d digits" % nd,
                       ["%d digits" % x for x in [4, 3, 2, 5] if x != nd],
                       why + "%s ÷ %d = %s, which has %d digits." % (f(n), d, f(q), nd), rnd))
    rnd.shuffle(its)
    return {"title": "Four-digit dividends and zeros in the quotient", "items": its}


# ------------------------------------------------------------ set 5: word problems
def find(rnd, lo, hi, ds, kind):
    """n, d with a remainder (or without one when kind == 'exact')."""
    while True:
        d = rnd.choice(ds)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if kind == "exact" and r == 0 and n % 10:
            return n, d
        if kind != "exact" and r and r not in (q, q + 1, q - 1) and r != 1:
            return n, d


def story(kind, text, lo, hi, ds, one, many, rnd, P, why=None, fixed=None):
    name, he, his = P.next()
    n, d = fixed or find(rnd, lo, hi, ds, kind)
    q, r = divmod(n, d)
    money = one == "$"
    U = (lambda k: "$" + f(k)) if money else (lambda k: units(k, one, many))
    q_txt = text.format(n=f(n), d=d, name=name, he=he, He=cap(he), his=his)
    base = "Divide: " + ld_steps(n, d, end=False) + " "
    if kind == "up":
        ans = U(q + 1)
        e = base + "%s %s are not enough: %s %s. Add 1 more, so the answer is %s." % (
            f(q), many, units(r, why[0], why[1]), why[2], ans)
        cands = [U(q), qr(q, r), U(r), U(q + 2)]
    elif kind == "down":
        ans = U(q)
        e = base + "The %s left over %s not enough %s, so leave the remainder out. The answer is %s." % (
            units(r, why[0], why[1]), "is" if r == 1 else "are", why[2], ans)
        cands = [U(q + 1), qr(q, r), U(r), U(q - 1)]
    elif kind == "rem":
        ans = U(r)
        e = base + "The question asks how many are left over. That is the remainder: %s." % ans
        cands = [U(q), U(d - r), qr(q, r), U(r + d)]
    else:
        ans = U(q)
        e = base + "There is no remainder, so the answer is %s." % ans
        cands = [U(int(x.replace(",", ""))) for x in no_rem_cands(n, d)]
    return mcq(q_txt, ans, cands, e, rnd)


def set_story(rnd, P):
    its = []
    S = [
        ("up", "A school is taking {n} students and adults on a field trip. Each van holds {d} people. How many vans are needed to take everyone?",
         100, 199, [7, 8], "van", "vans", ("person", "people", "still need a van")),
        ("up", "{name} is putting {n} photos into an album. Each page holds {d} photos. How many pages does {he} need for all the photos?",
         110, 290, [4, 6], "page", "pages", ("photo", "photos", "still need a page")),
        ("up", "A school library is moving {n} books. Each box holds {d} books. How many boxes are needed to pack all the books?",
         1050, 1990, [9], "box", "boxes", ("book", "books", "still need a box")),
        ("up", "There are {n} campers going on an overnight trip. Each tent sleeps {d} campers. How many tents are needed?",
         53, 99, [4, 6], "tent", "tents", ("camper", "campers", "still need a tent")),
        ("up", "A farm collected {n} eggs. Each carton holds {d} eggs. How many cartons are needed to hold all the eggs?",
         1010, 1490, [6], "carton", "cartons", ("egg", "eggs", "still need a carton")),
        ("up", "There are {n} people waiting for a boat ride across a lake. The boat carries {d} people on each trip. How many trips does the boat need to make?",
         100, 199, [8, 9], "trip", "trips", ("person", "people", "still need a ride")),
        ("up", "There are {n} guests at a wedding. Each table seats {d} guests. How many tables are needed so every guest has a seat?",
         120, 250, [8], "table", "tables", ("guest", "guests", "still need a seat")),
        ("down", "A factory has {n} crayons. It puts {d} crayons in each box. How many boxes can it fill completely?",
         2010, 3990, [8], "box", "boxes", ("crayon", "crayons", "to fill another box")),
        ("down", "A total of {n} students sign up for a soccer tournament. Each team needs {d} players. How many full teams can be made?",
         100, 160, [7], "team", "teams", ("student", "students", "to make another team")),
        ("down", "{name} has ${n}. Movie tickets cost ${d} each. How many tickets can {he} buy?",
         45, 99, [7, 8, 9], "ticket", "tickets", ("dollars", "dollars", "to buy another ticket")),
        ("down", "{name} has a ribbon that is {n} inches long. {He} cuts it into pieces that are each {d} inches long. How many pieces can {he} cut?",
         100, 199, [6, 8], "piece", "pieces", ("inch", "inches", "to cut another piece")),
        ("down", "There are 365 days in a year. How many full weeks are in a year?",
         0, 0, [7], "week", "weeks", ("day", "days", "to make another week")),
        ("down", "An orchard picked {n} apples. The apples are packed in bags of {d}. How many full bags can be packed?",
         1010, 2490, [6, 8], "bag", "bags", ("apple", "apples", "to fill another bag")),
        ("rem", "{name} shares {n} stickers equally among {d} friends. Each friend gets as many as possible. How many stickers are left over?",
         50, 99, [3, 4, 6, 7], "sticker", "stickers", None),
        ("rem", "Ms. Lee has {n} pencils. She puts the same number of pencils in each of {d} cups, as many as she can. How many pencils are left over?",
         100, 199, [6, 7, 8], "pencil", "pencils", None),
        ("rem", "A bakery made {n} cookies. It packs them in boxes of {d} and fills as many boxes as it can. How many cookies are not in a box?",
         1010, 1990, [6, 8], "cookie", "cookies", None),
        ("rem", "A deck has 52 cards. {name} deals as many cards as {he} can so that each of {d} players gets the same number. How many cards are left over?",
         0, 0, [5], "card", "cards", None),
        ("exact", "A school raised ${n} at a book fair. It shares the money equally among {d} classes. How much money does each class get?",
         1200, 3990, [4, 5, 6], "$", "$", None),
        ("exact", "A bike club rode {n} miles in {d} days. They rode the same distance each day. How many miles did they ride each day?",
         120, 490, [3, 4], "mile", "miles", None),
    ]
    for kind, text, lo, hi, ds, one, many, why in S:
        fixed = (365, 7) if "365" in text else (52, 5) if "52 cards" in text else None
        its.append(story(kind, text, lo, hi, ds, one, many, rnd, P, why, fixed))
    # check a story answer by multiplying
    name, he, his = P.next()
    n, d = find(rnd, 100, 199, [6], "up")
    q, r = divmod(n, d)
    good = "%d × %d + %d" % (d, q, r)
    its.append(mcq("%s has %d beads. %s makes bracelets with %d beads each and says %s can make %d bracelets with %d beads left over. "
                   "Which expression checks %s answer? It should equal %d." % (name, n, cap(he), d, he, q, r, his, n), good,
                   ["%d × %d − %d" % (d, q, r), "%d × %d + %d" % (q, r, d), "%d + %d + %d" % (d, q, r)],
                   "Multiply the number of bracelets by the beads on each one, then add the beads left over: %d × %d = %d, %d + %d = %d. "
                   "That is all %d beads, so %s answer is right." % (d, q, d * q, d * q, r, n, n, his), rnd))
    rnd.shuffle(its)
    return {"title": "Word problems: what to do with the remainder", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Divide one place at a time</h2>"
        "<p>To divide a big number, split it into <b>hundreds, tens and ones</b> and divide each part. "
        "Then add the answers. An <b>area model</b> shows this: the divisor is the side, the dividend is the area.</p>"
        "<figure class='sn-fig'>" + area_svg(4, [800, 40, 12], ["200", "10", "3"]) +
        "<figcaption>852 ÷ 4: 800 ÷ 4 = 200, 40 ÷ 4 = 10, 12 ÷ 4 = 3. Add: 200 + 10 + 3 = 213.</figcaption></figure>"
        "<h2>Long division: 4 steps</h2>"
        "<p>Long division does the same thing in a short layout. Start with the biggest place and repeat four steps.</p>" +
        table(["Step", "What you do"], [
            ["1. Divide", "How many times does the divisor fit?"],
            ["2. Multiply", "Quotient digit × divisor"],
            ["3. Subtract", "The difference must be less than the divisor"],
            ["4. Bring down", "Write the next digit next to the difference, then divide again"],
        ]) +
        "<figure class='sn-fig'>" + bracket_svg(857, 6, fs=26, work=True) +
        "<figcaption>857 ÷ 6: 8 ÷ 6 = 1, subtract 6, 2 left. Bring down 5: 25 ÷ 6 = 4, subtract 24, 1 left. "
        "Bring down 7: 17 ÷ 6 = 2, subtract 12, 5 left. Answer: 142 R 5.</figcaption></figure>"
        "<h2>Remainders</h2>"
        "<p>The <b>remainder</b> is what is left when nothing more can be shared. It is always <b>less than the divisor</b>. "
        "Write it with R: 857 ÷ 6 = 142 R 5. Check: <b>quotient × divisor + remainder = dividend</b>. "
        "142 × 6 + 5 = 857.</p>"
        "<h2>Zeros in the quotient</h2>"
        "<p>If the divisor does not fit, write <b>0</b> in the quotient and bring down the next digit. Never skip a place.</p>"
        "<figure class='sn-fig'>" + bracket_svg(4218, 6, fs=26, work=True) +
        "<figcaption>4,218 ÷ 6: 4 is less than 6, so start with 42. 42 ÷ 6 = 7. Bring down 1: 1 ÷ 6 = 0, so write 0. "
        "Bring down 8: 18 ÷ 6 = 3. Answer: 703, not 73.</figcaption></figure>"
        "<h2>Word problems: what does the remainder mean?</h2>" +
        table(["The question asks", "Use the remainder like this", "125 people, 8 in each van: 125 ÷ 8 = 15 R 5"], [
            ["How many are needed for everyone?", "Add 1 to the quotient", "16 vans"],
            ["How many full groups?", "Leave the remainder out", "15 full vans"],
            ["How many are left over?", "The remainder is the answer", "5 people"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Skipping a zero (4,218 ÷ 6 = 73)", "When the divisor does not fit, write 0 in the quotient"],
            ["A remainder bigger than the divisor (85 ÷ 6 = 13 R 7)", "If the difference is the divisor or more, the divisor fits one more time"],
            ["Forgetting to bring down a digit", "Every digit of the dividend needs a digit above it in the quotient"],
            ["Ignoring the remainder in a word problem", "Ask: do the leftovers need one more van, box or table?"],
        ])
    )


FAQ = [
    {"q": "How do you teach long division to a 4th grader?",
     "a": "Teach four repeating steps: divide, multiply, subtract, bring down. Start with an area model or place-value sharing so the steps make sense, then move to the long division layout."},
    {"q": "Why is there a 0 in the quotient of 4,218 ÷ 6?",
     "a": "After dividing 42 hundreds, you bring down the 1 ten. 6 does not fit into 1, so the quotient has 0 tens. Without the 0, the answer would be 73 instead of 703."},
    {"q": "How do you check a division answer with a remainder?",
     "a": "Multiply the quotient by the divisor and add the remainder. You should get the dividend: for 857 ÷ 6 = 142 R 5, 142 × 6 + 5 = 857."},
    {"q": "What does 4.NBT.B.6 mean?",
     "a": "It is the Common Core standard for Grade 4: divide numbers up to four digits by one-digit numbers, find quotients and remainders, and explain the work with equations, arrays or area models."},
]


def gen_division():
    rnd = random.Random(102)
    P = People(rnd)
    used = set()
    sets = [set_facts(rnd, set()), set_no_rem(rnd, used), set_rem(rnd, used, P), set_four(rnd, used), set_story(rnd, P)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "long-division", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Long Division",
        "seo_title": "Grade 4 Long Division Worksheets: Remainders, Zeros in the Quotient and Word Problems",
        "short_title": "Long division",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "4.NBT.B.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NBT/B/6/",
        "standard_text": "Find whole-number quotients and remainders with up to four-digit dividends and one-digit divisors, using strategies based on place value, the properties of operations, and/or the relationship between multiplication and division. Illustrate and explain the calculation by using equations, rectangular arrays, and/or area models.",
        "meta_desc": "Free Grade 4 long division worksheets: divide up to 4-digit numbers by 1-digit numbers, remainders, zeros in the quotient, area models and word problems that use the remainder. 100 practice questions with step-by-step answers.",
        "key_big": "Divide, multiply, subtract, bring down. Repeat until every digit is used.",
        "key_sub": "Start with the biggest place. If the divisor does not fit, write 0. The remainder is always less than the divisor. Check: quotient × divisor + remainder = dividend.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, rulers, A-D choices) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_division()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "area model")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
