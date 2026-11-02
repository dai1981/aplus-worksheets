# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Long Division with Two-Digit Divisors (5.NBT.B.6)
  python3 tools/gen_us_math_g5_division.py
Every quotient and remainder comes from divmod, and every figure is drawn from the numbers in the question.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
PLACE = ["ones", "tens", "hundreds", "thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """Commas in numbers of 1,000 and more."""
    return "{:,}".format(n)


def qr(q, r):
    return "%s R %d" % (f(q), r) if r else f(q)


def r10(x):
    """Round to the nearest ten (5 rounds up)."""
    return (x + 5) // 10 * 10


def r100(x):
    return (x + 50) // 100 * 100


VAL = re.compile(r"^(?:about )?\$?([\d,]+)(.*)$")


def val(c):
    m = VAL.match(c)
    return (int(m.group(1).replace(",", "")), m.group(2)) if m else None


def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 distractors with a different value. Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    vals = [val(correct)]
    pick = []
    for c in cands:
        c = str(c)
        v = val(c)
        if c in seen or not c or "-" in c.split(" ")[0] or (v and v in vals) or (v and v[0] <= 0):
            continue
        seen.add(c)
        vals.append(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, font=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, font, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ long division, step by step
def ld_rows(n, d):
    """The steps of long division: list of (index of digit, partial dividend, quotient digit), remainder."""
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


def check_txt(n, d):
    q, r = divmod(n, d)
    if r:
        return "Check: %s × %d + %d = %s." % (f(q), d, r, f(n))
    return "Check: %s × %d = %s." % (f(q), d, f(n))


def ld_steps(n, d, end=True):
    """Divide, multiply, subtract, bring down — in words. Ends with the answer and a check."""
    ds = str(n)
    steps, r = ld_rows(n, d)
    q = n // d
    parts = []
    for k, (i, cur, qd) in enumerate(steps):
        if k == 0:
            head = ("%d is less than %d, so start with %s. " % (int(ds[:i]), d, f(cur))) if i > 0 else ""
            parts.append(head + "%s ÷ %d = %d: %d × %d = %s, %s − %s = %d."
                         % (f(cur), d, qd, qd, d, f(qd * d), f(cur), f(qd * d), cur - qd * d))
        elif qd == 0:
            parts.append("Bring down %s: %d does not fit into %d, so write 0 in the quotient." % (ds[i], d, cur))
        else:
            parts.append("Bring down %s: %d ÷ %d = %d: %d × %d = %d, %d − %d = %d."
                         % (ds[i], cur, d, qd, qd, d, qd * d, cur, qd * d, cur - qd * d))
    if r:
        parts.append("Nothing is left to bring down, so the remainder is %d." % r)
    if end:
        parts.append("Answer: %s. %s" % (qr(q, r), check_txt(n, d)))
    else:
        parts.append("So %s ÷ %d = %s. %s" % (f(n), d, qr(q, r), check_txt(n, d)))
    return " ".join(parts)


def first_est(n, d):
    """Rounded divisor and the first try for a one-digit quotient (182 ÷ 26: 26 → 30, 182 ÷ 30 → 6)."""
    D = r10(d)
    return D, max(1, min(9, n // D))


def est_steps(n, d):
    """One-digit quotient: estimate with the rounded divisor, then adjust the try up or down."""
    q, r = divmod(n, d)
    D, e = first_est(n, d)
    parts = []
    if n // D > 9:
        parts.append("Round %d to %d. %d ÷ %d is about %d, but the quotient has only one digit, so try 9." % (d, D, n, D, n // D))
    elif D != d:
        parts.append("Round %d to %d. %d ÷ %d is about %d, so try %d." % (d, D, n, D, e, e))
    else:
        parts.append("%d ÷ %d is about %d, so try %d." % (n, d, e, e))
    while e * d > n:
        parts.append("%d × %d = %d, which is more than %d, so %d is too big." % (e, d, e * d, n, e))
        e -= 1
        parts.append("Try %d." % e)
    while n - e * d >= d:
        parts.append("%d × %d = %d and %d − %d = %d, which is not less than %d, so %d is too small."
                     % (e, d, e * d, n, e * d, n - e * d, d, e))
        e += 1
        parts.append("Try %d." % e)
    assert e == q
    parts.append("%d × %d = %d and %d − %d = %d." % (q, d, q * d, n, q * d, r))
    parts.append("Answer: %s. %s" % (qr(q, r), check_txt(n, d)))
    return " ".join(parts)


# ------------------------------------------------------------ typical mistakes
def drop_zero(q):
    """Skipping the 0 in the quotient (200 → 2, 105 → 15)."""
    s = str(q).replace("0", "")
    return int(s) if s else 0


def no_rem_cands(n, d):
    q = n // d
    c = []
    if "0" in str(q):
        c.append(f(drop_zero(q)))
    c += [f(q * 10),                                         # first digit written above the wrong place
          qr(q - 1, d),                                      # estimate not adjusted: "remainder" equals the divisor
          f(q + 1), f(q - 10), f(q + 10), f(q - 1)]
    return c


def rem_cands(n, d):
    q, r = n // d, n % d
    c = []
    if "0" in str(q):
        c.append(qr(drop_zero(q), r))
    c += [qr(q - 1, r + d),                                  # remainder bigger than the divisor
          f(q),                                              # left the remainder out
          qr(q, d - r),                                      # wrote how many more are needed
          qr(q * 10, r), qr(q + 1, r), qr(q - 1, r)]
    return c


# ------------------------------------------------------------ figures
def bracket_svg(n, d, fs=24, work=False):
    """Long division layout: divisor, bracket and dividend. With work=True, the full worked
    example (quotient, products, differences, brought-down digits) is drawn."""
    cw = fs * 0.85
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
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (col(last - k), y, fs, colr, ch))

    by = top + rh - fs * 0.18                                # dividend baseline
    digits_at(ds, L - 1, by)
    if L >= 4:                                               # comma between thousands and hundreds
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>,</text>"
                 % (x0 + cw * (L - 3), by + fs * 0.08, int(fs * 0.8), INK))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
             % (x0 - 14, by, fs, GREEN, d))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * L + 8
    H = top + bh + 8
    if work:
        digits_at(str(q), L - 1, top - 8, GREEN)
        if r:
            rt = "R %d" % r
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s'>%s</text>"
                     % (x0 + cw * L + 10, top - 8, fs, GREEN, rt))
            W = max(W, x0 + cw * L + 10 + len(rt) * fs * 0.62 + 8)
        y = by
        for k, (i, cur, qd) in enumerate(steps):
            p = qd * d
            y += rh
            digits_at(str(p), i, y)
            left = i - len(str(max(p, cur))) + 1
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>−</text>"
                     % (col(i - len(str(p)) + 1) - cw * 0.85, y, fs, RED))
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
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + cw * L + 4, top, INK))
    label = ("%s divided by %d worked out with long division" if work else "%s divided by %d written as long division") % (f(n), d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label, "monospace")


def area_svg(d, parts, tops):
    """Area model: a rectangle with the divisor on the side, split into parts (area written inside).
    tops: label above each part (partial quotient, or '?')."""
    fs = 18
    xs = 40
    ws = [max(76, len(f(p)) * fs * 0.6 + 26) for p in parts]
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
             % (xs - 18, y0 + h / 2 + 6, fs, GREEN, d))
    W, H = int(x + 8), y0 + h + 8
    return svg_wrap(W, H, "".join(s), "area model for %s divided by %d" % (f(sum(parts)), d))


def area_parts(q, d, split_tens=False):
    """Partial quotients from the digits of q: 63 → 60, 3 (or 50, 10, 3 when split_tens)."""
    t, o = q // 10 * 10, q % 10
    pq = [t] if not split_tens or t < 20 else [t - 10, 10]
    if o:
        pq.append(o)
    return pq


# ============================================================ set 1: multiples of 10 and estimating
def set_tens(rnd, used):
    its = []
    pairs = [(dd, qq) for dd in range(2, 10) for qq in range(2, 10)]
    rnd.shuffle(pairs)

    def take(n_scale, zero_fact):
        while True:
            dd, qq = pairs.pop(0)
            fact = dd * qq
            n = fact * n_scale
            if (fact % 10 == 0) != zero_fact or n in used or n > 9999 or n < 100:
                pairs.append((dd, qq))
                continue
            used.add(n)
            return n, dd, qq, fact

    # 1) 4 with n in tens (480 ÷ 60), 3 with n in hundreds (3,600 ÷ 40), 1 where the fact ends in 0 (3,000 ÷ 60)
    for n_scale, zf in [(10, False)] * 4 + [(100, False)] * 2 + [(100, True)]:
        n, dd, qq, fact = take(n_scale, zf)
        d = dd * 10
        q = n // d
        e = "Cross out one zero in each number: %s ÷ %d = %s ÷ %d. " % (f(n), d, f(n // 10), dd)
        if n_scale == 10:
            e += "%d ÷ %d = %d." % (fact, dd, qq)
        else:
            e += "%d ÷ %d = %d, so %s ÷ %d = %s." % (fact, dd, qq, f(n // 10), dd, f(q))
            e += " Be careful: cross out the same number of zeros in both numbers." if not zf else (
                " Be careful: %s has %d zeros, but one of them belongs to the fact %d ÷ %d." % (f(n), str(n).count("0"), fact, dd))
        e += " Check: %s × %d = %s." % (f(q), d, f(n))
        cands = [f(q * 10), f(q // 10) if q % 10 == 0 else f(q * 100), f(q + (10 if q >= 10 else 1)),
                 f(q - (10 if q >= 10 else 1))]
        its.append(mcq("What is %s ÷ %d?" % (f(n), d), f(q), cands, e))
    # 2) missing factor
    for n_scale in (100, 10, 100):
        n, dd, qq, fact = take(n_scale, False)
        d = dd * 10
        q = n // d
        e = ("Think: what number times %d is %s? That is %s ÷ %d = %s ÷ %d = %s. Check: %s × %d = %s."
             % (d, f(n), f(n), d, f(n // 10), dd, f(q), f(q), d, f(n)))
        cands = [f(q * 10), f(q // 10) if q % 10 == 0 else f(q * 100), f(q + (10 if q >= 10 else 1))]
        its.append(mcq("What number goes in the box?  <b>☐ × %d = %s</b>" % (d, f(n)), f(q), cands, e))

    # 3) estimate with compatible numbers
    def est_pick(four):
        while True:
            D = rnd.choice([20, 30, 40, 50, 60, 70, 80, 90])
            d = D + rnd.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            if four:
                e = rnd.randint(2, 9) * 10
                m = e * D
                n = m + rnd.choice([-1, 1]) * rnd.randint(12, 45)
                if not (1000 <= n <= 9999):
                    continue
            else:
                e = rnd.randint(3, 9)
                m = e * D
                n = m + rnd.choice([-1, 1]) * rnd.randint(2, 9)
                if not (100 <= n <= 999):
                    continue
            if n in used or n % 10 == 0 or r10(n) == m or (not four and r100(n) % D == 0):
                continue
            q = n // d
            if abs(q - e) > (6 if four else 1):
                continue
            used.add(n)
            return n, d, D, e, m

    for four in [False, False, False, True, True, True]:
        n, d, D, e, m = est_pick(four)
        q, r = divmod(n, d)
        if four:
            fact = "%d ÷ %d = %d" % (m // 100, D // 10, e // 10)
            cands = ["about %d" % (e // 10), "about %s" % f(e * 10), "about %d" % (e + 10), "about %d" % (e - 10)]
        else:
            fact = "%d ÷ %d = %d" % (m // 10, D // 10, e)
            cands = ["about %d" % (e * 10), "about %d" % (e + 1), "about %d" % (e - 1), "about %d" % (e + 2)]
        expl = ("Round %d to %d. A number close to %s that %d divides easily is %s, because %s. "
                "%s ÷ %d = %s, so %s ÷ %d is about %s. (The exact answer is %s, which is close.)"
                % (d, D, f(n), D, f(m), fact, f(m), D, f(e), f(n), d, f(e), qr(q, r)))
        its.append(mcq("Use compatible numbers to estimate %s ÷ %d." % (f(n), d), "about %s" % f(e), cands, expl))
    # 4) choose the compatible numbers
    for _ in range(4):
        n, d, D, e, m = est_pick(False)
        good = "%d ÷ %d" % (m, D)
        nb = sorted({"%d ÷ %d" % (r100(n), D), "%d ÷ %d" % (r10(n), D)})
        bad = " and ".join(nb) + (" do not come out evenly" if len(nb) > 1 else " does not come out evenly")
        expl = ("Round %d to %d. Then find a number near %d that %d divides easily: %d ÷ %d = %d, so use <b>%s</b> = %d. "
                "%s." % (d, D, n, D, m // 10, D // 10, e, good, e, bad))
        its.append(mcq("Which numbers are best for estimating %d ÷ %d?" % (n, d), good,
                       ["%d ÷ %d" % (r100(n), D), "%d ÷ %d" % (r10(n), D), "%d ÷ %d" % (m, d), "%d ÷ %d" % (n, D)], expl))
    assert len(its) == 20, len(its)
    return {"title": "Divide with multiples of 10 and estimate", "items": its}


# ============================================================ set 2: one-digit quotients, adjust the estimate
def pick3(rnd, used, rem, kind):
    """3-digit ÷ 2-digit with a one-digit quotient. kind: 'up' (first try too small),
    'down' (first try too big) or 'ok' (first try right)."""
    while True:
        d = rnd.randint(12, 98)
        if d % 10 == 0:
            continue
        q = rnd.randint(3, 9)
        r = rnd.randint(1, d - 1) if rem else 0
        n = q * d + r
        if n < 100 or n > 999 or n in used:
            continue
        D, e = first_est(n, d)
        k = "ok" if e == q else "up" if e == q - 1 else "down" if e == q + 1 else None
        if k != kind:
            continue
        used.add(n)
        return n, d


def set_one_digit(rnd, used, P):
    its = []
    # plain division, half as long division figures
    for i, (rem, kind) in enumerate([(False, "up"), (False, "down"), (False, "ok"), (False, "up"),
                                     (True, "down"), (True, "up"), (True, "ok"), (True, "down")]):
        n, d = pick3(rnd, used, rem, kind)
        q, r = divmod(n, d)
        D, e = first_est(n, d)
        cands = []
        if e < q:
            cands.append(qr(e, n - e * d))                   # stopped at the first try: remainder too big
        elif e > q:
            cands.append(f(e))                               # kept a try that is too big
        cands += (rem_cands(n, d) if r else no_rem_cands(n, d))
        qtxt = (fig(bracket_svg(n, d)) + "Divide.") if i % 2 == 0 else "What is %d ÷ %d?" % (n, d)
        its.append(mcq(qtxt, qr(q, r), cands, est_steps(n, d)))
    # what to do next after a first try
    for kind in ["up", "down", "up", "down", "up", "down"]:
        name, he, his = P.next()
        n, d = pick3(rnd, used, rnd.random() < 0.5, kind)
        q, r = divmod(n, d)
        D, e = first_est(n, d)
        lead = "%s divides %d ÷ %d. %s rounds %d to %d and tries %d. " % (name, n, d, cap(he), d, D, e)
        if kind == "up":
            lead += "%d × %d = %d and %d − %d = %d." % (e, d, e * d, n, e * d, n - e * d)
            cands = ["Try %d instead" % (e - 1), "Write %d R %d" % (e, n - e * d),
                     "Try %d instead" % (q + 1) if q < 9 else "Try %d instead" % (e - 2)]
            expl = ("The difference %d is not less than the divisor %d, so %d fits one more time. "
                    "Try %d: %d × %d = %d and %d − %d = %d. So %d ÷ %d = %s. %s"
                    % (n - e * d, d, d, q, q, d, q * d, n, q * d, r, n, d, qr(q, r), check_txt(n, d)))
        else:
            lead += "%d × %d = %d, which is more than %d." % (e, d, e * d, n)
            cands = ["Keep %d" % e, "Write %d R %d" % (e, e * d - n), "Try %d instead" % (q - 1)]
            expl = ("%d is more than %d, so %d is too big. Try %d: %d × %d = %d and %d − %d = %d, "
                    "which is less than %d. So %d ÷ %d = %s. %s"
                    % (e * d, n, e, q, q, d, q * d, n, q * d, r, d, n, d, qr(q, r), check_txt(n, d)))
        its.append(mcq(lead + " What should %s do next?" % he, "Try %d instead" % q, cands, expl))
    # the greatest product that fits
    for _ in range(3):
        n, d = pick3(rnd, used, True, rnd.choice(["up", "down", "ok"]))
        q, r = divmod(n, d)
        good = "%d × %d = %d" % (q, d, q * d)
        expl = ("You need the greatest product that is not more than %d. %d × %d = %d is too big, and %d × %d = %d "
                "leaves %d, which is less than %d. So %d ÷ %d = %s."
                % (n, q + 1, d, (q + 1) * d, q, d, q * d, r, d, n, d, qr(q, r)))
        its.append(mcq("To divide %d ÷ %d, which product should you use?" % (n, d), good,
                       ["%d × %d = %d" % (q + 1, d, (q + 1) * d), "%d × %d = %d" % (q - 1, d, (q - 1) * d),
                        "%d × %d = %d" % (q - 2, d, (q - 2) * d)], expl))
    # the remainder is asked for
    for _ in range(3):
        n, d = pick3(rnd, used, True, rnd.choice(["up", "down", "ok"]))
        q, r = divmod(n, d)
        its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), str(r),
                       [str(q), str(d - r), str(r + d), str(d)],
                       "The question asks for the remainder, not the quotient. " + est_steps(n, d)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "One-digit quotients: adjust the estimate", "items": its}


# ============================================================ set 3: two-digit quotients
def pick(rnd, used, lo, hi, rem=False, qlo=11, qhi=99, zero_q=False):
    while True:
        d = rnd.randint(12, 98)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if (r != 0) != rem or n in used or not (qlo <= q <= qhi) or d % 10 == 0:
            continue
        if ("0" in str(q)) != zero_q:
            continue
        used.add(n)
        return n, d


def exact(rnd, used, lo, hi, qlo, qhi, zero_q=False):
    """Exact division: pick the quotient and the divisor, then multiply."""
    while True:
        d = rnd.randint(12, 98)
        q = rnd.randint(qlo, qhi)
        n = q * d
        if n < lo or n > hi or n in used or d % 10 == 0 or ("0" in str(q)) != zero_q:
            continue
        used.add(n)
        return n, d


def item_div(n, d, figure):
    q, r = divmod(n, d)
    qtxt = (fig(bracket_svg(n, d)) + "Divide.") if figure else "What is %s ÷ %d?" % (f(n), d)
    cands = rem_cands(n, d) if r else no_rem_cands(n, d)
    return mcq(qtxt, qr(q, r), cands, ld_steps(n, d))


def set_two_digit(rnd, used):
    its = []
    for i in range(3):                                      # 3-digit dividends
        n, d = exact(rnd, used, 300, 999, 12, 49)
        its.append(item_div(n, d, i == 1))
    for i in range(5):                                      # 4-digit, no remainder
        n, d = exact(rnd, used, 1000, 9999, 21, 99)
        its.append(item_div(n, d, i % 2 == 0))
    for i in range(4):                                      # 4-digit, remainder
        n, d = pick(rnd, used, 1000, 9999, rem=True, qlo=21)
        its.append(item_div(n, d, i % 2 == 1))
    # area model
    k = 0
    while k < 3:
        d = rnd.randint(12, 48)
        q = rnd.randint(21, 89)
        n = q * d
        if n in used or n < 1000 or d % 10 == 0 or "0" in str(q):
            continue
        used.add(n)
        pq = area_parts(q, d, split_tens=(k == 2))
        parts = [p * d for p in pq]
        e = ("The model splits %s into %s. Divide each part by %d: %s. Add the partial quotients: %s = %s. %s"
             % (f(n), " + ".join(f(p) for p in parts), d,
                ", ".join("%s ÷ %d = %d" % (f(p), d, x) for p, x in zip(parts, pq)),
                " + ".join(str(x) for x in pq), f(q), check_txt(n, d)))
        cands = [f(sum(x // 10 if x % 10 == 0 else x for x in pq)),     # wrote 60 as 6
                 f(q - pq[-1]),                                          # forgot the last part
                 f(q * 10), f(q + 10)]
        its.append(mcq(fig(area_svg(d, parts, ["?"] * len(parts))) + "Use the area model to find %s ÷ %d." % (f(n), d),
                       f(q), cands, e))
        k += 1
    # partial quotients written out
    k = 0
    while k < 2:
        d = rnd.randint(13, 39)
        q = rnd.randint(41, 89)
        n = q * d
        if n in used or n < 1000 or d % 10 == 0 or "0" in str(q):
            continue
        used.add(n)
        t, o = q // 10 * 10, q % 10
        a = t - 10
        rest1 = n - a * d
        rest2 = rest1 - 10 * d
        lines = ("%d × %d = %s, and %s − %s = %d. %d × 10 = %d, and %d − %d = %d. %d × %d = %d, and %d − %d = 0."
                 % (d, a, f(a * d), f(n), f(a * d), rest1, d, 10 * d, rest1, 10 * d, rest2, d, o, o * d, rest2, o * d))
        e = ("Add the partial quotients: %d + 10 + %d = %d. %s" % (a, o, q, check_txt(n, d)))
        its.append(mcq("%s uses partial quotients to find %s ÷ %d: %s What is the quotient?"
                       % ("Ms. Rivera" if k == 0 else "Mr. Chen", f(n), d, lines),
                       str(q), [str(a // 10 + 1 + o), str(a + o), str(a + 10), str(q + 10)], e))
        k += 1
    # where does the first digit go / how many digits
    for kind in ("hundreds", "tens"):
        while True:
            d = rnd.randint(12, 98)
            n = rnd.randint(1000, 9999)
            first = int(str(n)[:2])
            if d % 10 == 0 or n in used or n % d == 0:
                continue
            if (first >= d) == (kind == "hundreds"):
                break
        used.add(n)
        steps, _ = ld_rows(n, d)
        i = steps[0][0]
        place = PLACE[len(str(n)) - 1 - i]
        why = ("%d is at least %d, so start with %d hundreds: %d ÷ %d = %d." % (first, d, first, first, d, first // d)) if i == 1 else (
            "%d is less than %d, so there are no hundreds in the quotient. Start with %d tens: %d ÷ %d = %d."
            % (first, d, steps[0][1], steps[0][1], d, steps[0][2]))
        its.append(mcq("You divide %s ÷ %d with long division. Above which place do you write the first digit of the quotient?" % (f(n), d),
                       "the %s place" % place, ["the %s place" % p for p in ["thousands", "hundreds", "tens", "ones"] if p != place],
                       why + " The quotient is %s." % qr(n // d, n % d)))
    assert len(its) == 19, len(its)
    while True:
        d = rnd.randint(12, 98)
        n = rnd.randint(1000, 9999)
        if d % 10 == 0 or n in used or n % d == 0 or int(str(n)[:2]) >= d:
            continue
        break
    used.add(n)
    q = n // d
    its.append(mcq("How many digits does the quotient of %s ÷ %d have?" % (f(n), d), "%d digits" % len(str(q)),
                   ["%d digits" % x for x in [4, 3] if x != len(str(q))] + ["1 digit"],
                   "%d is less than %d, so the quotient has no hundreds. Start with %d tens. "
                   "%s ÷ %d = %s, which has %d digits." % (int(str(n)[:2]), d, int(str(n)[:3]), f(n), d, qr(q, n % d), len(str(q)))))
    rnd.shuffle(its)
    return {"title": "Two-digit quotients: long division and area models", "items": its}


# ============================================================ set 4: zeros, remainders and checking
def set_zeros(rnd, used, P):
    its = []
    # zeros in the quotient
    for i, shape in enumerate(["x00", "x0y", "x0y", "xy0", "x0", "x0y"]):
        while True:
            d = rnd.randint(12, 49)
            q = int(shape.replace("x", str(rnd.randint(1, 9)), 1).replace("y", str(rnd.randint(1, 9))))
            r = rnd.randint(2, d - 1) if i % 2 == 0 else 0
            n = q * d + r
            if 1000 <= n <= 9999 and n not in used and d % 10:
                break
        used.add(n)
        its.append(item_div(n, d, i % 2 == 1))
    # remainders, two-digit quotients
    for i in range(6):
        n, d = pick(rnd, used, 1000, 9999, rem=True, qlo=21)
        its.append(item_div(n, d, i % 2 == 0))
    # remainder bigger than the divisor
    for _ in range(2):
        name, he, his = P.next()
        n, d = pick(rnd, used, 1000, 9999, rem=True, qlo=21)
        q, r = divmod(n, d)
        r_show = r + d
        its.append(mcq("%s says %s ÷ %d = %s. What mistake did %s make?" % (name, f(n), d, qr(q - 1, r_show), he),
                       "The remainder is too big",
                       ["%s forgot to bring down" % cap(he), "%s skipped a 0" % cap(he), "There is no mistake"],
                       "The remainder must be less than the divisor. %d is more than %d, so %d fits one more time: %d − %d = %d. "
                       "The answer is %s. %s" % (r_show, d, d, r_show, d, r, qr(q, r), check_txt(n, d))))
    # skipped zero
    for shape in ["x0y", "x00"]:
        name, he, his = P.next()
        while True:
            d = rnd.randint(12, 49)
            q = int(shape.replace("x", str(rnd.randint(1, 9)), 1).replace("y", str(rnd.randint(1, 9))))
            r = rnd.randint(2, d - 1)
            n = q * d + r
            if 1000 <= n <= 9999 and n not in used and d % 10:
                break
        used.add(n)
        wq = drop_zero(q)
        its.append(mcq("%s says %s ÷ %d = %s. What mistake did %s make?" % (name, f(n), d, qr(wq, r), he),
                       "%s skipped a 0" % cap(he),
                       ["The remainder is too big", "%s forgot the remainder" % cap(he), "There is no mistake"],
                       "Check %s answer: %d × %d + %d = %s, not %s. When %d does not fit, write 0 in the quotient. "
                       % (his, wq, d, r, f(wq * d + r), f(n), d) + ld_steps(n, d)))
    # check by multiplying
    for _ in range(3):
        n, d = pick(rnd, used, 1000, 9999, rem=True, qlo=21)
        q, r = divmod(n, d)
        good = "%d × %d + %d" % (d, q, r)
        its.append(mcq("%s ÷ %d = %s. Which expression checks this answer? It should equal %s." % (f(n), d, qr(q, r), f(n)), good,
                       ["%d × %d − %d" % (d, q, r), "%d × %d + %d" % (q, r, d), "%d + %d + %d" % (d, q, r)],
                       "Multiply the quotient by the divisor, then add the remainder: %d × %d = %s, %s + %d = %s. "
                       "It matches the dividend, so the answer is right." % (d, q, f(d * q), f(d * q), r, f(n))))
    # find the dividend
    d, q, r = 34, 56, 12
    n = d * q + r
    its.append(mcq("In a division problem, the divisor is %d, the quotient is %d and the remainder is %d. What is the dividend?" % (d, q, r),
                   f(n), [f(d * q), f(d * q - r), f(d * (q + r))],
                   "Dividend = quotient × divisor + remainder: %d × %d = %s, %s + %d = %s. Check: %s ÷ %d = %s."
                   % (q, d, f(q * d), f(q * d), r, f(n), f(n), d, qr(q, r))))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Zeros in the quotient, remainders and checking", "items": its}


# ============================================================ set 5: word problems
def find(rnd, lo, hi, ds, kind, used):
    """n, d with a remainder (or without one when kind == 'exact')."""
    while True:
        d = rnd.choice(ds)
        if kind == "exact":
            q = rnd.randint(-(-lo // d), hi // d)
            n = q * d
            if n % 10 == 0 or n in used or "0" in str(q):
                continue
            used.add(n)
            return n, d
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if r > 1 and r not in (q, q + 1, q - 1) and n not in used and n % 10:
            used.add(n)
            return n, d


def story(kind, text, lo, hi, ds, one, many, rnd, P, used, why=None):
    name, he, his = P.next()
    n, d = find(rnd, lo, hi, ds, kind, used)
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
        cands = [U(int(x.split(" ")[0].replace(",", ""))) for x in no_rem_cands(n, d) if " R " not in x]
    return mcq(q_txt, ans, cands, e)


def set_story(rnd, P, used):
    its = []
    S = [
        ("up", "A school is taking {n} students on a field trip. Each bus holds {d} students. How many buses are needed to take everyone?",
         310, 690, [44, 48, 52], "bus", "buses", ("student", "students", "still need a bus")),
        ("up", "A concert hall needs seats for {n} people. Each row has {d} seats. How many rows are needed so everyone has a seat?",
         410, 890, [24, 28, 32], "row", "rows", ("person", "people", "still need a seat")),
        ("up", "A school library is moving {n} books. Each box holds {d} books. How many boxes are needed to pack all the books?",
         1050, 1990, [36, 45], "box", "boxes", ("book", "books", "still need a box")),
        ("up", "A bakery is delivering {n} muffins. Each tray holds {d} muffins. How many trays are needed for all the muffins?",
         410, 790, [24, 18], "tray", "trays", ("muffin", "muffins", "still need a tray")),
        ("up", "There are {n} cars waiting for a ferry. The ferry carries {d} cars on each trip. How many trips does the ferry need to make?",
         150, 330, [18, 22], "trip", "trips", ("car", "cars", "still need a trip")),
        ("up", "There are {n} guests at a banquet. Each table seats {d} guests. How many tables are needed so every guest has a seat?",
         210, 390, [12, 14], "table", "tables", ("guest", "guests", "still need a seat")),
        ("down", "A factory has {n} crayons. It puts {d} crayons in each box. How many boxes can it fill completely?",
         2010, 3990, [24, 64], "box", "boxes", ("crayon", "crayons", "to fill another box")),
        ("down", "A summer camp has {n} campers. Each cabin group needs exactly {d} campers. How many full groups can be made?",
         150, 290, [12, 14], "group", "groups", ("camper", "campers", "to make another group")),
        ("down", "{name} has ${n} saved. Concert tickets cost ${d} each. How many tickets can {he} buy?",
         150, 390, [35, 45, 28], "ticket", "tickets", ("dollar", "dollars", "to buy another ticket")),
        ("down", "{name} has a roll of ribbon that is {n} inches long. {He} cuts it into pieces that are each {d} inches long. How many pieces can {he} cut?",
         310, 790, [15, 18], "piece", "pieces", ("inch", "inches", "to cut another piece")),
        ("down", "A farm collected {n} eggs. It packs them in cartons of {d}. How many cartons can it fill completely?",
         1010, 2490, [12, 18], "carton", "cartons", ("egg", "eggs", "to fill another carton")),
        ("down", "A school has ${n} to spend on calculators. Each calculator costs ${d}. How many calculators can the school buy?",
         510, 990, [14, 16], "calculator", "calculators", ("dollar", "dollars", "to buy another calculator")),
        ("rem", "{name} shares {n} stickers equally among {d} classmates. Each classmate gets as many as possible. How many stickers are left over?",
         210, 490, [24, 26, 28], "sticker", "stickers", None),
        ("rem", "A bakery made {n} cookies. It packs them in boxes of {d} and fills as many boxes as it can. How many cookies are not in a box?",
         1010, 1990, [36, 48], "cookie", "cookies", None),
        ("rem", "Ms. Rivera has {n} sheets of paper. She gives the same number of sheets to each of her {d} students, as many as she can. How many sheets are left over?",
         310, 690, [27, 29], "sheet", "sheets", None),
        ("rem", "An orchard picked {n} apples. The apples are packed in crates of {d}, and every crate is filled. How many apples are left over?",
         2010, 4990, [72, 88], "apple", "apples", None),
        ("exact", "A school raised ${n} at a fun fair. It shares the money equally among {d} classes. How much money does each class get?",
         1010, 3990, [12, 15, 24], "$", "$", None),
        ("exact", "A train travels {n} miles in {d} hours. It goes the same distance every hour. How many miles does it travel each hour?",
         710, 1490, [12, 14, 16], "mile", "miles", None),
        ("exact", "A theater sold tickets for ${n} in all. Each ticket cost ${d}. How many tickets did the theater sell?",
         2010, 5990, [25, 35], "ticket", "tickets", None),
    ]
    for kind, text, lo, hi, ds, one, many, why in S:
        its.append(story(kind, text, lo, hi, ds, one, many, rnd, P, used, why))
    # check a story answer by multiplying
    name, he, his = P.next()
    n, d = find(rnd, 300, 600, [24], "up", used)
    q, r = divmod(n, d)
    good = "%d × %d + %d" % (d, q, r)
    its.append(mcq("%s has %d beads. %s makes necklaces with %d beads each and says %s can make %d necklaces with %d beads left over. "
                   "Which expression checks %s answer? It should equal %d." % (name, n, cap(he), d, he, q, r, his, n), good,
                   ["%d × %d − %d" % (d, q, r), "%d × %d + %d" % (q, r, d), "%d + %d + %d" % (d, q, r)],
                   "Multiply the number of necklaces by the beads on each one, then add the beads left over: %d × %d = %d, %d + %d = %d. "
                   "That is all %d beads, so %s answer is right." % (q, d, d * q, d * q, r, n, n, his)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: what to do with the remainder", "items": its}


# ============================================================ lesson
def body_html():
    f_ld = bracket_svg(2385, 48, fs=26, work=True)
    f_zero = bracket_svg(5412, 27, fs=26, work=True)
    f_area = area_svg(24, [1200, 240, 72], ["50", "10", "3"])
    return (
        "<h2>The big idea</h2>"
        "<p>Dividing by a two-digit number uses the same four steps as before: <b>divide, multiply, subtract, bring down</b>. "
        "The new part is the <b>divide</b> step. You cannot just know 238 ÷ 48 as a fact, so you <b>estimate</b>, "
        "try a digit and fix it if needed.</p>"
        "<h2>Estimate with compatible numbers</h2>"
        "<p>Round the divisor to the nearest ten. Then change the dividend to a nearby number that divides easily.</p>"
        + ex("Example", "Estimate 312 ÷ 41.",
             "41 is close to 40. 320 is close to 312, and 32 ÷ 4 = 8, so 320 ÷ 40 = 8.", "about 8 (exactly 7 R 25)")
        + "<p>Multiples of 10 work like basic facts: cross out the same number of zeros in both numbers. "
        "3,600 ÷ 40 = 360 ÷ 4 = 90.</p>"
        "<h2>Long division with a two-digit divisor</h2>"
        "<figure class='sn-fig'>" + f_ld +
        "<figcaption>2,385 ÷ 48: 23 is less than 48, so start with 238. 238 ÷ 48 is about 240 ÷ 50 = 4. "
        "4 × 48 = 192, 238 − 192 = 46. Bring down 5: 465 ÷ 48 is about 450 ÷ 50 = 9. 9 × 48 = 432, 465 − 432 = 33. "
        "Answer: 49 R 33.</figcaption></figure>"
        "<h2>Adjust the estimate</h2>"
        "<p>Rounding the divisor can make a try one too big or one too small. Look at what you get:</p>"
        + table(["What you see", "What it means", "Fix"], [
            ["The product is more than the number", "The digit is too big", "Try one less"],
            ["The difference is the divisor or more", "The digit is too small", "Try one more"],
        ])
        + ex("Example", "182 ÷ 26",
             "Round 26 to 30: 182 ÷ 30 is about 6. 6 × 26 = 156 and 182 − 156 = 26. 26 is not less than 26, "
             "so 6 is too small. Try 7: 7 × 26 = 182.", "7")
        + "<h2>Another way: area model and partial quotients</h2>"
        "<p>Take away easy chunks of the divisor (× 10, × 50, …) until nothing is left. Then add the chunks.</p>"
        "<figure class='sn-fig'>" + f_area +
        "<figcaption>1,512 ÷ 24: 24 × 50 = 1,200, 24 × 10 = 240, 24 × 3 = 72. Add: 50 + 10 + 3 = 63.</figcaption></figure>"
        "<h2>Remainders and checking</h2>"
        "<p>The <b>remainder</b> is always <b>less than the divisor</b>. If the divisor does not fit after you bring down, "
        "write <b>0</b> in the quotient.</p>"
        "<figure class='sn-fig'>" + f_zero +
        "<figcaption>5,412 ÷ 27: 54 ÷ 27 = 2. Bring down 1: 27 does not fit, write 0. Bring down 2: 27 does not fit into 12, "
        "write 0. Answer: 200 R 12, not 20 R 12.</figcaption></figure>"
        "<p>Check every answer: <b>quotient × divisor + remainder = dividend</b>. 200 × 27 + 12 = 5,412.</p>"
        "<h2>Word problems: what does the remainder mean?</h2>"
        + table(["The question asks", "Use the remainder like this", "500 students, 48 on each bus: 500 ÷ 48 = 10 R 20"], [
            ["How many are needed for everyone?", "Add 1 to the quotient", "11 buses"],
            ["How many full groups?", "Leave the remainder out", "10 full buses"],
            ["How many are left over?", "The remainder is the answer", "20 students"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Keeping a try that is too small (182 ÷ 26 = 6 R 26)", "If the difference is the divisor or more, add 1 to the digit"],
            ["Skipping a zero (5,412 ÷ 27 = 20 R 12)", "Every digit you bring down needs a digit in the quotient"],
            ["Crossing out different numbers of zeros (3,600 ÷ 40 = 9)", "Cross out the same number of zeros: 360 ÷ 4 = 90"],
            ["Ignoring the remainder in a word problem", "Ask: do the leftovers need one more bus, box or row?"],
        ])
    )


FAQ = [
    {"q": "How do you divide by a two-digit number?",
     "a": "Use long division: estimate how many times the divisor fits by rounding it to the nearest ten, multiply, subtract and bring down the next digit. Repeat until every digit is used."},
    {"q": "What do you do when your estimate in long division is wrong?",
     "a": "If the product is bigger than the number you are dividing, try one less. If the difference is equal to or more than the divisor, try one more."},
    {"q": "How do you check a long division answer with a remainder?",
     "a": "Multiply the quotient by the divisor and add the remainder. For 2,385 ÷ 48 = 49 R 33: 49 × 48 + 33 = 2,385."},
    {"q": "What does 5.NBT.B.6 mean?",
     "a": "It is the Common Core Grade 5 standard for dividing whole numbers with up to four-digit dividends by two-digit divisors, and explaining the work with equations, arrays or area models."},
]


def gen():
    rnd = random.Random(510)
    P = People(rnd)
    used = set()
    sets = [set_tens(rnd, used), set_one_digit(rnd, used, P), set_two_digit(rnd, used),
            set_zeros(rnd, used, P), set_story(rnd, P, used)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "long-division-two-digit-divisors", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Long Division with Two-Digit Divisors",
        "seo_title": "Grade 5 Long Division with 2-Digit Divisors Worksheets: Estimating, Adjusting the Quotient, Remainders and Word Problems",
        "short_title": "Divide by 2-digit numbers",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "5.NBT.B.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NBT/B/6/",
        "standard_text": "Find whole-number quotients of whole numbers with up to four-digit dividends and two-digit divisors, using strategies based on place value, the properties of operations, and/or the relationship between multiplication and division. Illustrate and explain the calculation by using equations, rectangular arrays, and/or area models.",
        "meta_desc": "Free Grade 5 worksheets on dividing by 2-digit numbers: divide with multiples of 10, estimate with compatible numbers, adjust the quotient digit, long division and area models with 4-digit dividends, zeros in the quotient, remainders and word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Round the divisor to estimate each digit. Then check: too big, try one less; remainder too big, try one more.",
        "key_sub": "Use compatible numbers (312 ÷ 41 is about 320 ÷ 40 = 8). The remainder must be less than the divisor, and every digit you bring down needs a digit in the quotient, even 0. Check: quotient × divisor + remainder = dividend.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (area models) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "area model")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
