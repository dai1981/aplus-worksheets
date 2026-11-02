# -*- coding: utf-8 -*-
"""
Australia Year 5 Maths: Estimation and Money Problems
(Australian Curriculum v9.0, AC9M5N08, with AC9M5N09)
  python3 tools/gen_au_maths_y5_estimation_money.py
All money is held as whole cents (int), so every total, change and mistake is exact.
Writing money: under $1 as 75c, from $1 as $3.45; rounded estimates as whole dollars ($14).
Cash totals are rounded to the nearest 5c (1, 2 down to 0; 3, 4 up to 5; 6, 7 down to 5; 8, 9 up to 10).
Numbers of 5 or more digits use a no-break space between groups of three (37 080); 4-digit numbers have none.
Every answer is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#6b6259"
TAG = "#fff4d6"
TAGEDGE = "#b8860b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
MINUS = "−"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ numbers and money
def nf(n):
    """4536 -> '4536', 37080 -> '37 080' (no-break space from 5 digits)."""
    assert n >= 0, n
    s = str(n)
    if len(s) < 5:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(out)


def aud(c):
    """cents -> '75c' or '$3.45'"""
    assert c > 0, c
    return "%dc" % c if c < 100 else "$%s.%02d" % (nf(c // 100), c % 100)


def dol(c):
    """whole dollars: 1400 -> '$14'"""
    assert c % 100 == 0 and c > 0, c
    return "$" + nf(c // 100)


def val(s):
    """Value of a number or money text (in cents for money), or None for words."""
    s = re.sub(r"<[^>]+>", "", s).replace(NB, "")
    m = re.match(r"^\$(\d+)(?:\.(\d\d))?$", s)
    if m:
        return ("$", int(m.group(1)) * 100 + int(m.group(2) or 0))
    m = re.match(r"^(\d+)c$", s)
    if m:
        return ("$", int(m.group(1)))
    m = re.match(r"^(\d+)$", s)
    if m:
        return ("n", int(m.group(1)))
    m = re.match(r"^(\d+) weeks?$", s)
    if m:
        return ("w", int(m.group(1)))
    return None


def rnd_to(n, p):
    """round half up to the nearest p"""
    return (n + p // 2) // p * p


def r5(c):
    """cash rounding to the nearest 5c"""
    return (c + 2) // 5 * 5


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """correct is a string; cands are strings (None skipped). Wrong choices equal in value to the answer
    or to another choice are dropped. The first 3 left are used."""
    seen_t, seen_v = {correct}, {val(correct)} - {None}
    pick = []
    for x in cands:
        if x is None:
            continue
        v = val(x)
        if x in seen_t or (v is not None and v in seen_v):
            continue
        seen_t.add(x)
        if v is not None:
            seen_v.add(v)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mq_n(q, correct, cands, e):
    return mcq(q, nf(correct), [nf(x) for x in cands if x is not None and x > 0], e)


def mq_c(q, correct, cands, e, fmt=aud):
    return mcq(q, fmt(correct), [fmt(x) for x in cands if x is not None and x > 0], e)


def balance(sets, rnd):
    """Each position (A to D) is the right answer 5 times in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
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


def text(x, y, t, fs=16, anchor="middle", col=INK, wt=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, wt, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def number_line_svg(lo, hi, n, step, fmt=nf):
    """Number line from lo to hi, ticks every step, labels at both ends and halfway, red dot on n."""
    L, R, Y = 52, 388, 52
    W, H = 440, 96
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
            s.append(text(X(v), Y + 32, fmt(v), 15, col=GREEN if v != mid else GREY))
        v += step
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(n), Y, RED))
    tx = min(max(X(n), 40), W - 40)
    s.append(text(tx, Y - 18, fmt(n), 16, col=RED, wt=800))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (fmt(lo), fmt(hi)))


def tags_svg(items):
    """Price tags in one row: items = [(name, cents), ...]"""
    tw, th, gap, pad = 112, 66, 10, 4
    W = pad * 2 + len(items) * tw + (len(items) - 1) * gap
    H = th + pad * 2
    s = []
    for i, (name, p) in enumerate(items):
        x = pad + i * (tw + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, pad, tw, th, TAG, TAGEDGE))
        s.append("<circle cx='%d' cy='%d' r='4' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x + 12, pad + 12, TAGEDGE))
        s.append(text(x + tw / 2, pad + 26, name, 14, col=GREY))
        s.append(text(x + tw / 2, pad + 54, aud(p), 20))
    return svg_wrap(W, H, "".join(s), "price tags: " + ", ".join("%s %s" % (n, aud(p)) for n, p in items))


def cash_table_svg():
    """last digit of the cents -> what it rounds to (for the lesson)"""
    rows = [("1, 2", "down to 0", "$4.32 → $4.30"), ("3, 4", "up to 5", "$4.34 → $4.35"),
            ("6, 7", "down to 5", "$4.37 → $4.35"), ("8, 9", "up to 10", "$4.38 → $4.40")]
    W, rh = 420, 34
    s = [text(70, 22, "last digit", 14, col=GREY), text(200, 22, "rounds", 14, col=GREY),
         text(340, 22, "example", 14, col=GREY)]
    for i, (a, b, c) in enumerate(rows):
        y = 32 + i * rh
        s.append("<rect x='4' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='#d8cfc3'/>"
                 % (y, W - 8, rh - 4, "#f6f1ea" if i % 2 == 0 else "#ffffff"))
        s.append(text(70, y + 21, a, 16))
        s.append(text(200, y + 21, b, 16, col=GREEN))
        s.append(text(340, y + 21, c, 16))
    return svg_wrap(W, 32 + 4 * rh + 4, "".join(s), "rounding cash to the nearest 5c")


# ============================================================ set 1: round to estimate
def round_cands(n, p):
    r = rnd_to(n, p)
    lo = n // p * p
    out = [lo + p if r == lo else lo]                          # rounded the wrong way
    if r > lo:
        out.append(r + n % p)                                  # kept the digits after the place
    if p >= 100:
        out.append(rnd_to(n, p // 10))                         # rounded to the place on the right
    out.append(n // (p * 10) * (p * 10))
    out += [rnd_to(n, p * 10), r + p, r - p]
    return [x for x in out if x != r]


LOOK = {10: "ones", 100: "tens", 1000: "hundreds"}


def q_round(n, p):
    lo = n // p * p
    r = rnd_to(n, p)
    d = (n // (p // 10)) % 10
    e = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s to <b>%s</b>."
         % (nf(n), nf(lo), nf(lo + p), LOOK[p], d, "5 or more" if d >= 5 else "4 or less",
            "up" if r > lo else "down", nf(r)))
    q = fig(number_line_svg(lo, lo + p, n, p // 10)) + "Round %s to the nearest %d." % (nf(n), p)
    return mq_n(q, r, round_cands(n, p), e)


def est2(a, b, op, p):
    """estimate a op b by rounding both to the nearest p"""
    ra, rb = rnd_to(a, p), rnd_to(b, p)
    exact = a + b if op == "+" else a - b
    est = ra + rb if op == "+" else ra - rb
    trunc = a // p * p + (b // p * p if op == "+" else -(b // p * p))     # rounded both down
    finer = rnd_to(a, p // 10) + (rnd_to(b, p // 10) if op == "+" else -rnd_to(b, p // 10)) if p > 10 else None
    sym = "+" if op == "+" else MINUS
    assert est != exact and est > 0
    e = ("%s rounds to %s and %s rounds to %s. %s %s %s = <b>%s</b>. (The exact answer is %s.)"
         % (nf(a), nf(ra), nf(b), nf(rb), nf(ra), sym, nf(rb), nf(est), nf(exact)))
    q = "Estimate %s %s %s by rounding each number to the nearest %d." % (nf(a), sym, nf(b), p)
    return mq_n(q, est, [trunc, exact, finer, est + p, est - p], e)


def est_mul(a, k, p):
    """estimate a × k (k a single digit) by rounding a to the nearest p"""
    ra = rnd_to(a, p)
    est = ra * k
    exact = a * k
    down = a // p * p * k if a // p * p != ra else (ra + p) * k
    e = ("%s rounds to %s. %d × %s = <b>%s</b>. (The exact answer is %s.)"
         % (nf(a), nf(ra), k, nf(ra), nf(est), nf(exact)))
    q = "Estimate %d × %s by rounding %s to the nearest %d." % (k, nf(a), nf(a), p)
    return mq_n(q, est, [down, exact, est * 10, ra + k], e)


def front(a):
    k = 10 ** (len(str(a)) - 1)
    return a // k * k


def est_front(a, b, op):
    fa, fb = front(a), front(b)
    if op == "×":
        est, exact = a * fb, a * b                          # a is the single digit
        p = 10 ** (len(str(b)) - 1)
        rnd_est = a * rnd_to(b, p)
        small = a * (fb // 10)
        sym = "×"
        e = ("Keep the first digit of %s and make the other digits 0: %s. %d × %s = <b>%s</b>. "
             "(The exact answer is %s. A front-end estimate is always lower than the exact answer.)"
             % (nf(b), nf(fb), a, nf(fb), nf(est), nf(exact)))
        q = "Use front-end estimation to estimate %d × %s." % (a, nf(b))
        return mq_n(q, est, [rnd_est, exact, small], e)
    est = fa + fb if op == "+" else fa - fb
    exact = a + b if op == "+" else a - b
    p = 10 ** (len(str(a)) - 1)
    rnd_est = rnd_to(a, p) + rnd_to(b, p) if op == "+" else rnd_to(a, p) - rnd_to(b, p)
    small = est // 10                                         # wrong place value: 6 + 2 = 8 -> 800
    sym = "+" if op == "+" else MINUS
    assert rnd_est != est
    e = ("Keep the first digit of each number and make the other digits 0: %s %s %s = <b>%s</b>. "
         "(The exact answer is %s.)" % (nf(fa), sym, nf(fb), nf(est), nf(exact)))
    q = "Use front-end estimation to estimate %s %s %s." % (nf(a), sym, nf(b))
    return mq_n(q, est, [rnd_est, exact, small], e)


def set_round():
    its = [q_round(368, 10), q_round(7451, 100), q_round(4682, 1000), q_round(2507, 1000)]
    for a, b, op, p in [(63, 28, "+", 10), (94, 47, "-", 10),
                        (347, 486, "+", 100), (812, 385, "-", 100), (629, 254, "+", 100), (935, 468, "-", 100),
                        (4682, 2371, "+", 1000), (8350, 2716, "-", 1000), (3529, 4475, "+", 1000),
                        (9208, 4861, "-", 1000)]:
        its.append(est2(a, b, op, p))
    its.append(est_mul(38, 6, 10))
    its.append(est_mul(293, 7, 100))
    its.append(est_front(6815, 2742, "+"))
    its.append(est_front(538, 376, "+"))
    its.append(est_front(7384, 2915, "-"))
    its.append(est_front(4, 1873, "×"))
    return {"title": "Round to estimate", "items": its}


# ============================================================ set 2: is the answer reasonable?
def reasonable_pick(expr, exact, est, wrong, why):
    """Which answer is reasonable? exact is the true answer; wrong are real mistakes, all far from est."""
    assert abs(exact - est) / est < 0.25, (expr, exact, est)
    for w in wrong:
        assert abs(w - est) / est > 0.4, (expr, w, est)
    e = "Estimate: %s. Only <b>%s</b> is close to that. %s" % (why, nf(exact), "")
    return mq_n("Use an estimate to choose the reasonable answer.<br>%s = ?" % expr, exact, wrong, e.strip())


def yes_no(person, expr, said, exact, est_txt, est, why):
    """Is the answer reasonable? Exactly one of the four statements is true."""
    name = person[0]
    ok = abs(said - est) / est < 0.25
    assert ok == (said == exact), (expr, said, exact, est)
    if not ok:
        assert abs(said - est) / est > 0.4
    right = ("Yes, it is close to %s" if ok else "No, it should be about %s") % nf(est)
    other = ("No, it should be about %s" if ok else "Yes, it is close to %s") % nf(est)
    big = est * 10 if said > est else est // 10            # the estimate with the wrong place value
    traps = ["Yes, it is close to %s" % nf(big), "No, it should be about %s" % nf(big)]
    e = "Estimate: %s. %s is %s, so it is %s. %s" % (
        why, nf(said), "close to %s" % nf(est) if ok else "not close to %s" % nf(est),
        "reasonable" if ok else "not reasonable",
        "" if ok else "The exact answer is %s." % nf(exact))
    q = "%s works out %s and gets %s. Estimate to check. Is the answer reasonable?" % (name, expr, nf(said))
    return mcq(q, right, [other] + traps, e.strip())


def best_est(expr, exact, cands, why):
    best = min(cands, key=lambda x: abs(x - exact))
    for x in cands:
        if x != best:
            assert abs(x - exact) > abs(best - exact)
    e = "%s = <b>%s</b>. (The exact answer is %s, so this estimate is the closest.)" % (why, nf(best), nf(exact))
    return mq_n("Which estimate is closest to the exact answer of %s?" % expr, best,
                [x for x in cands if x != best], e)


def set_reasonable(P):
    its = []
    for expr, exact, est, wrong, why in [
        ("412 × 9", 412 * 9, 3600, [37080, 421, 403], "400 × 9 = 3600"),
        ("3046 + 528", 3046 + 528, 3500, [3046 + 5280, 35740, 346 + 528], "3000 + 500 = 3500"),
        ("6 × 715", 6 * 715, 4200, [42900, 721, 709], "6 × 700 = 4200"),
        ("1872 ÷ 8", 1872 // 8, 250, [2340, 23, 1864], "2000 ÷ 8 = 250"),
        ("5283 − 1947", 5283 - 1947, 3000, [4744, 7230, 5283 - 194], "5000 − 2000 = 3000"),
        ("48 × 23", 48 * 23, 1000, [240, 11040, 71], "50 × 20 = 1000"),
        ("3 × 2985", 3 * 2985, 9000, [89550, 2988, 2982], "3 × 3000 = 9000"),
        ("9156 ÷ 4", 9156 // 4, 2300, [22890, 9152, 36624], "9200 ÷ 4 = 2300"),
    ]:
        assert exact * 1 == eval(expr.replace("×", "*").replace("÷", "//").replace("−", "-"))
        its.append(reasonable_pick(expr, exact, est, wrong, why))
    for expr, said, exact, est, why in [
        ("308 × 6", 18480, 1848, 1800, "300 × 6 = 1800"),
        ("7 × 589", 4123, 4123, 4200, "7 × 600 = 4200"),
        ("4875 + 3290", 8165, 8165, 8000, "5000 + 3000 = 8000"),
        ("6034 − 2879", 4255, 3155, 3000, "6000 − 3000 = 3000"),
        ("2736 ÷ 9", 34, 304, 300, "2700 ÷ 9 = 300"),
        ("63 × 18", 1134, 1134, 1200, "60 × 20 = 1200"),
        ("395 + 278 + 412", 1085, 1085, 1100, "400 + 300 + 400 = 1100"),
        ("25 × 41", 125, 1025, 1000, "25 × 40 = 1000"),
    ]:
        assert exact == eval(expr.replace("×", "*").replace("÷", "//").replace("−", "-"))
        its.append(yes_no(P.next(), expr, said, exact, why, est, why))
    its.append(best_est("498 × 6", 498 * 6, [3000, 2400, 300, 30000], "500 × 6"))
    its.append(best_est("3125 ÷ 5", 3125 // 5, [600, 800, 60, 6000], "3000 ÷ 5"))
    its.append(best_est("6890 + 2155", 6890 + 2155, [9000, 8000, 900, 10000], "7000 + 2000"))
    its.append(best_est("8 × 3976", 8 * 3976, [32000, 24000, 3200, 320000], "8 × 4000"))
    return {"title": "Is the answer reasonable?", "items": its}


# ============================================================ set 3: estimating with money
def near_dollar(p, item, cands):
    r = rnd_to(p, 100)
    lo = p // 100 * 100
    c = p % 100
    if c == 50:
        why = "%s is exactly halfway between %s and %s. Halfway rounds up, so <b>%s</b>." % (
            aud(p), dol(lo), dol(lo + 100), dol(r))
    else:
        why = "%s is between %s and %s. Look at the cents: %dc is %s 50c, so round %s to <b>%s</b>." % (
            aud(p), dol(lo) if lo else "0c", dol(lo + 100), c, "more than" if c > 50 else "less than",
            "up" if r > lo else "down", dol(r))
    q = "A %s costs %s. What is the price to the nearest dollar?" % (item, aud(p))
    fm = lambda x: dol(x) if x % 100 == 0 else aud(x)
    return mcq(q, dol(r), [fm(x) for x in cands], why)


def sum_est(items, ask):
    prices = [p for _, p in items]
    rs = [rnd_to(p, 100) for p in prices]
    est = sum(rs)
    exact = sum(prices)
    down = sum(p // 100 * 100 for p in prices)
    up = sum(p // 100 * 100 + 100 for p in prices)
    assert est != exact
    e = "Round each price to the nearest dollar: %s = <b>%s</b>. (The exact total is %s.)" % (
        " + ".join(dol(r) for r in rs), dol(est), aud(exact))
    q = fig(tags_svg(items)) + ask
    fm = lambda x: dol(x) if x % 100 == 0 else aud(x)
    return mcq(q, dol(est), [fm(down), fm(up), fm(exact), fm(est + 100), fm(est - 100)], e)


def enough(person, items, budget, place):
    name, she, her = person
    prices = [p for _, p in items]
    rs = [rnd_to(p, 100) for p in prices]
    est, exact = sum(rs), sum(prices)
    down = sum(p // 100 * 100 for p in prices)
    ok = est <= budget
    assert ok == (exact <= budget) and abs(est - budget) >= 200 and down != est
    yes, no = "Yes, about %s", "No, about %s"
    right = (yes if ok else no) % dol(est)
    cands = [(no if ok else yes) % dol(est), (yes if down <= budget else no) % dol(down),
             (no if down <= budget else yes) % dol(down)]
    e = "Round to the nearest dollar: %s = %s. %s is %s %s, so %s. (The exact total is %s.)" % (
        " + ".join(dol(r) for r in rs), dol(est), dol(est), "less than" if ok else "more than", dol(budget),
        "<b>yes</b>, it is enough" if ok else "<b>no</b>, it is not enough", aud(exact))
    lst = ", ".join("%s for %s" % (n, aud(p)) for n, p in items[:-1]) + " and %s for %s" % (items[-1][0], aud(items[-1][1]))
    q = "%s has %s at %s. %s wants to buy %s. Is %s enough? Estimate to decide." % (
        name, dol(budget), place, cap(she), lst, dol(budget))
    return mcq(q, right, cands, e)


def set_money_est(P):
    its = []
    for p, item, wr in [(345, "glue stick", [400, 350, 345]), (750, "pair of thongs", [700, 1000, 750]),
                        (1295, "beach towel", [1200, 1000, 1400]), (408, "notebook", [500, 410, 800]),
                        (85, "pencil", [90, 85, 8500]), (1962, "cricket ball", [1900, 1960, 1000])]:
        its.append(near_dollar(p, item, wr))
    for items in [[("pencils", 295), ("ruler", 420), ("eraser", 165)],
                  [("milk", 335), ("bread", 480), ("apples", 610)],
                  [("sunscreen", 1295), ("hat", 1850), ("water", 245)],
                  [("footy", 2490), ("socks", 875), ("cap", 1520)],
                  [("book", 1695), ("puzzle", 1240), ("cards", 560), ("pens", 435)]]:
        its.append(sum_est(items, "Round each price to the nearest dollar. Estimate the total cost."))
    its.append(enough(P.next(), [("a lunch box", 1295), ("a drink bottle", 1840), ("a pencil case", 960)], 5000,
                      "the shops"))
    its.append(enough(P.next(), [("a novel", 1499), ("a colouring book", 825)], 2000, "the book fair"))
    its.append(enough(P.next(), [("a kite", 2350), ("a frisbee", 1180), ("a ball", 975)], 5000, "the toy shop"))
    its.append(enough(P.next(), [("a hot dog", 650), ("a juice", 380), ("an ice block", 290)], 1000,
                      "the athletics carnival"))
    its.append(enough(P.next(), [("a T-shirt", 1990), ("shorts", 2245), ("goggles", 1460)], 5000, "the surf shop"))
    # multiply and change
    n, she, her = P.next()
    p, k = 295, 4
    its.append(mcq("%s buys %d packets of stickers at %s each. Round the price to the nearest dollar. "
                   "About how much does %s spend?" % (n, k, aud(p), she), dol(rnd_to(p, 100) * k),
                   [dol(p // 100 * 100 * k), aud(p * k), dol((rnd_to(p, 100) // 100 + k) * 100)],
                   "%s rounds to %s. %d × %s = <b>%s</b>. (The exact cost is %s.)" % (
                       aud(p), dol(rnd_to(p, 100)), k, dol(rnd_to(p, 100)), dol(rnd_to(p, 100) * k), aud(p * k))))
    p, k = 620, 3
    assert rnd_to(p, 100) == 600
    its.append(mcq("Movie tickets cost %s each. About how much do %d tickets cost?" % (aud(p), k),
                   dol(600 * k), [dol(700 * k), aud(p * k), dol(6000 * k)],
                   "%s rounds to $6. %d × $6 = <b>%s</b>. (The exact cost is %s.)" % (aud(p), k, dol(600 * k), aud(p * k))))
    a, b = 680, 815
    est = rnd_to(a, 100) + rnd_to(b, 100)
    assert est == 1500
    its.append(mcq(fig(tags_svg([("sandwich", a), ("salad", b)])) +
                   "Mum pays for these with a $20 note. About how much change does she get?",
                   dol(2000 - est), [dol(est), dol(2000 - (a // 100 + b // 100) * 100), dol(2000 - 1600)],
                   "Round: $7 + $8 = $15. $20 " + MINUS + " $15 = <b>$5</b>. (The exact change is %s.)" % aud(2000 - a - b)))
    a, b, c = 1960, 2310, 840
    est = rnd_to(a, 100) + rnd_to(b, 100) + rnd_to(c, 100)
    assert est == 5100
    its.append(mcq("Dad buys a cricket ball for %s, batting gloves for %s and a cap for %s. "
                   "He pays with a $100 note. About how much change does he get?" % (aud(a), aud(b), aud(c)),
                   dol(10000 - est), [dol(est), dol(10000 - 5000), dol(10000 - 5300)],
                   "Round: $20 + $23 + $8 = $51. $100 " + MINUS + " $51 = <b>$49</b>. (The exact change is %s.)"
                   % aud(10000 - a - b - c)))
    return {"title": "Estimating with money", "items": its}


# ============================================================ set 4: dollars and cents
def set_cents(P):
    its = []
    its.append(mcq("Write 407c in dollars.", "$4.07", ["$4.70", "$40.70", "$47"],
                   "100c = $1. 407c = 400c + 7c = $4 and 7c = <b>$4.07</b>. The cents always take two digits."))
    its.append(mcq("Write $2.60 in cents.", "260c", ["26c", "206c", "2600c"],
                   "$1 = 100c, so $2 = 200c. 200c + 60c = <b>260c</b>."))
    for a, b, wr, e in [
        (465, 280, [645, 785, 7450], "Cents: 65c + 80c = 145c = $1.45. Dollars: $4 + $2 = $6. $6 + $1.45 = <b>$7.45</b>."),
        (1395, 850, [2145, 2345, 1445], "Cents: 95c + 50c = 145c = $1.45. Dollars: $13 + $8 = $21. $21 + $1.45 = <b>$22.45</b>."),
        (378, 245, [523, 613, 633], "Cents: 78c + 45c = 123c = $1.23. Dollars: $3 + $2 = $5. $5 + $1.23 = <b>$6.23</b>."),
    ]:
        its.append(mq_c("Add %s + %s." % (aud(a), aud(b)), a + b, wr, e))
    for paid, price, wr in [(1000, 635, [465, 375, 435]), (2000, 1285, [825, 815, 725]), (5000, 3740, [1360, 1340, 2260])]:
        ch = paid - price
        e = ("Count on from %s: to the next dollar, then to %s. %s = <b>%s</b>." % (
            aud(price), dol(paid),
            "%s + %s" % (aud(100 - price % 100), dol(paid - (price // 100 + 1) * 100)), aud(ch)))
        its.append(mq_c("What is %s " % dol(paid) + MINUS + " %s?" % aud(price), ch, wr, e))
    its.append(mq_c("What is 3 × $2.45?", 735, [635, 725, 7350],
                    "3 × $2 = $6 and 3 × 45c = 135c = $1.35. $6 + $1.35 = <b>$7.35</b>."))
    its.append(mq_c("What is 4 × $3.80?", 1520, [1220, 1280, 15200],
                    "4 × $3 = $12 and 4 × 80c = 320c = $3.20. $12 + $3.20 = <b>$15.20</b>."))
    its.append(mq_c("Share $7.50 equally between 3 people. How much does each person get?", 250, [205, 2500, 450],
                    "$7.50 = 750c. 750c ÷ 3 = 250c = <b>$2.50</b>."))
    its.append(mq_c("Share $9.60 equally between 4 people. How much does each person get?", 240, [215, 2400, 560],
                    "$9.60 = 960c. 960c ÷ 4 = 240c = <b>$2.40</b>."))
    # rounding to 5c
    for p in [437, 691, 348, 1293]:
        r = r5(p)
        d = p % 10
        rule = {1: "1 rounds down to 0", 2: "2 rounds down to 0", 3: "3 rounds up to 5", 4: "4 rounds up to 5",
                6: "6 rounds down to 5", 7: "7 rounds down to 5", 8: "8 rounds up to 10", 9: "9 rounds up to 10"}[d]
        lo5 = p // 5 * 5
        other = lo5 + 5 if r == lo5 else lo5
        e = ("Look at the last digit of the cents: %s. %s is closer to %s than to %s, so the cash total is <b>%s</b>."
             % (rule, aud(p), aud(r), aud(other), aud(r)))
        its.append(mq_c("A shop rounds cash totals to the nearest 5c. What does a %s bill cost in cash?" % aud(p),
                        r, [other, p // 10 * 10, rnd_to(p, 10), p, rnd_to(p, 100)], e))
    # cash change with rounding
    for price, paid in [(642, 1000), (1347, 2000), (2768, 5000), (419, 500)]:
        r = r5(price)
        ch = paid - r
        lo5 = price // 5 * 5
        wrong_way = lo5 + 5 if r == lo5 else lo5
        e = ("First round the total to the nearest 5c: %s → %s. Then %s " + MINUS + " %s = <b>%s</b>.") % (
            aud(price), aud(r), dol(paid), aud(r), aud(ch))
        its.append(mq_c("The bill is %s. You pay cash with a %s note, and the total is rounded to the nearest 5c. "
                        "How much change do you get?" % (aud(price), dol(paid)),
                        ch, [paid - price, paid - wrong_way, ch + 100], e))
    return {"title": "Dollars and cents", "items": its}


# ============================================================ set 5: practical money problems
def set_words(P):
    its = []

    def add(q, right, cands, e, fmt=aud):
        its.append(mcq(q, fmt(right) if isinstance(right, int) else right,
                       [fmt(x) if isinstance(x, int) else x for x in cands], e))

    add("A class of 28 students goes on a school excursion to the zoo. Entry is $12 for each student. "
        "What is the total entry cost?", 28 * 1200, [336000, 4000, 29600],
        "28 × $12 = 28 × $10 + 28 × $2 = $280 + $56 = <b>$336</b>. Check: 30 × $10 = $300, so $336 is reasonable.",
        fmt=dol)
    add("The bus for a school excursion costs $450. The cost is shared equally by 25 students. "
        "How much does each student pay?", 1800, [18000, 180, 42500],
        "$450 ÷ 25 = <b>$18</b>, because 25 × $18 = $450. Check: $450 ÷ 25 is a bit less than $500 ÷ 25 = $20.",
        fmt=lambda x: dol(x) if x % 100 == 0 else aud(x))
    add("A group of 31 students goes to the aquarium. Each ticket costs $19. Round both numbers to estimate the total cost.",
        60000, [600000, 30000, 5000],
        "31 rounds to 30 and $19 rounds to $20. 30 × $20 = <b>$600</b>. (The exact cost is $589.)", fmt=dol)
    name, she, her = P.next()
    t, k = 350, 4
    add("At the sausage sizzle, a sausage in bread costs $3.50. %s buys %d for %s family. "
        "How much does %s pay?" % (name, k, her, she), t * k, [1200, 14000, 750],
        "4 × $3 = $12 and 4 × 50c = $2. $12 + $2 = <b>$14</b>.", fmt=lambda x: dol(x) if x % 100 == 0 else aud(x))
    name, she, her = P.next()
    weeks = -(-7500 // 600)
    assert weeks == 13
    add("%s saves $6 of %s pocket money every week. %s wants a skateboard that costs $75. "
        "How many weeks does %s need to save?" % (name, her, cap(she), she), "13 weeks",
        ["12 weeks", "69 weeks", "15 weeks"],
        "$75 ÷ $6 = 12 remainder $3. After 12 weeks %s has $72, which is not enough, so %s needs "
        "<b>13 weeks</b>." % (she, she))
    name, she, her = P.next()
    add("%s gets $8 pocket money each week and saves half of it. How much does %s save in 6 weeks?" % (name, she),
        2400, [4800, 1400, 1200],
        "Half of $8 is $4. 6 × $4 = <b>$24</b>.", fmt=dol)
    assert 3 * 180 - 500 == 40
    add("Muesli bars cost $1.80 each, or 3 for $5. How much do you save if you buy the 3 for $5 deal?",
        40, [320, 4, 400],
        "3 × $1.80 = $5.40. $5.40 " + MINUS + " $5.00 = <b>40c</b>.")
    assert 320 // 2 == 160 < 175
    add("A 2 L bottle of milk costs $3.20. A 1 L bottle costs $1.75. Which is the better buy?",
        "the 2 L bottle: $1.60 per litre",
        ["the 1 L bottle: it costs less", "the 1 L bottle: $1.75 per litre", "the 2 L bottle: $3.20 per litre"],
        "Compare the price of 1 litre. $3.20 ÷ 2 = $1.60 per litre, which is less than $1.75, so "
        "<b>the 2 L bottle</b> is the better buy.")
    name, she, her = P.next()
    add("At the school canteen %s buys a sushi roll for $4.20 and a juice for $2.50. %s pays with a $10 note. "
        "How much change does %s get?" % (name, cap(she), she), 330, [430, 670, 380],
        "$4.20 + $2.50 = $6.70. $10 " + MINUS + " $6.70 = <b>$3.30</b>. (The total ends in 0, so no rounding is needed.)")
    tot = 2347
    assert r5(tot) == 2345
    add("The shopping costs $23.47. Mum pays cash with a $50 note, so the total is rounded to the nearest 5c. "
        "How much change does she get?", 5000 - 2345, [5000 - 2347, 5000 - 2350, 5000 - 2245],
        "$23.47 rounds to $23.45 (7 rounds down to 5). $50 " + MINUS + " $23.45 = <b>$26.55</b>.")
    name, she, her = P.next()
    assert r5(998) == 1000
    add("%s’s bill is $9.98. %s pays in cash, so the total is rounded to the nearest 5c. "
        "How much does %s pay?" % (name, cap(she), she), 1000, [995, 998, 990],
        "The last digit is 8, and 8 rounds up to 10. $9.98 → <b>$10.00</b>.")
    add("Year 5 sells 46 cupcakes at $2.50 each for a fundraiser. How much money do they raise?",
        11500, [9200, 1150, 4850],
        "46 × $2 = $92 and 46 × 50c = $23. $92 + $23 = <b>$115</b>. Check: 50 × $2.50 = $125, so $115 is reasonable.",
        fmt=lambda x: dol(x) if x % 100 == 0 else aud(x))
    name, she, her = P.next()
    assert 6 * 495 == 2970
    add("%s buys 6 packs of footy cards at $4.95 each. The screen shows $297.00. "
        "Is this reasonable?" % name, "No, it should be about $30",
        ["Yes, it is close to $300", "No, it should be about $3", "Yes, it is close to $30"],
        "$4.95 rounds to $5. 6 × $5 = $30, so $297.00 is <b>not reasonable</b>. The exact total is $29.70; "
        "the point was put in the wrong place.")
    tot = 35000 + 62 * 800
    assert tot == 84600
    add("Year 5 has $900 for an excursion. The bus costs $350, and entry is $8 for each of the 62 students. "
        "How much money is left?", 90000 - tot, [14600, 55000, 40400],
        "Entry: 62 × $8 = $496. Total: $350 + $496 = $846. $900 " + MINUS + " $846 = <b>$54</b>.", fmt=dol)
    name, she, her = P.next()
    add("%s saves $4.85 every week for 10 weeks. Round to the nearest dollar. About how much does %s save?"
        % (name, she), 5000, [4000, 50000, 1500],
        "$4.85 rounds to $5. 10 × $5 = <b>$50</b>. (The exact amount is $48.50.)", fmt=dol)
    assert 2 * 490 + 3 * 350 == 2030
    add("Apples cost $4.90 per kilogram and bananas cost $3.50 per kilogram. Dad buys 2 kg of apples and "
        "3 kg of bananas. How much does he pay?", 2030, [840, 1930, 1330],
        "Apples: 2 × $4.90 = $9.80. Bananas: 3 × $3.50 = $10.50. $9.80 + $10.50 = <b>$20.30</b>.")
    assert 10 * 120 - 950 == 250
    add("Pens cost $1.20 each, or $9.50 for a pack of 10. How much do you save if you buy the pack?",
        250, [830, 350, 1070],
        "10 × $1.20 = $12.00. $12.00 " + MINUS + " $9.50 = <b>$2.50</b>.")
    assert 3480 // 4 == 870
    add("After the swimming carnival, 4 friends share a $34.80 pizza bill equally. How much does each pay?",
        870, [820, 3080, 807],
        "$34 ÷ 4 = $8 remainder $2. $2.80 = 280c, and 280c ÷ 4 = 70c. Each pays <b>$8.70</b>.")
    name, she, her = P.next()
    assert rnd_to(1495, 100) + rnd_to(550, 100) == 2100 and 1495 + 550 > 2000
    add("%s has $20. %s wants a footy for $14.95 and socks for $5.50. Estimate. Does %s have enough?"
        % (name, cap(she), she), "No, about $21",
        ["Yes, about $21", "Yes, about $19", "No, about $19"],
        "Round: $15 + $6 = $21. $21 is more than $20, so <b>no</b>. (The exact total is $20.45.)")
    name, she, her = P.next()
    assert 3 * 450 == 1350 and 2 * 650 == 1300
    add("Pool entry costs $4.50 for one visit, or $13 for a 3-visit pass. %s goes 3 times. "
        "Which is cheaper, and by how much?" % name,
        "the pass, by 50c", ["single visits, by 50c", "the pass, by $5", "the pass, by $8.50"],
        "3 × $4.50 = $13.50. $13.50 " + MINUS + " $13.00 = 50c, so <b>the pass is cheaper by 50c</b>.")
    return {"title": "Practical money problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Estimate first, then check</h2>"
        "<p>An estimate is a quick answer that is close to the exact answer. Round the numbers to friendly numbers, "
        "then work out the estimate in your head. If your exact answer is far from the estimate, check your working.</p>"
        "<figure class='sn-fig'>" + number_line_svg(4000, 5000, 4682, 100) +
        "<figcaption>4682 is past the halfway point, 4500, so to the nearest 1000 it rounds up to 5000.</figcaption></figure>"
        + table(["Way to estimate", "4682 + 2371", "Estimate"], [
            ["Round to the nearest 1000", "5000 + 2000", "7000"],
            ["Round to the nearest 100", "4700 + 2400", "7100"],
            ["Front-end: keep the first digit", "4000 + 2000", "6000"],
        ]) +
        "<p>The exact answer is 7053. Rounding to the nearest 100 gives the closest estimate. "
        "Front-end estimation is the quickest, but its answer is always lower than the exact answer.</p>"
        + ex("Is the answer reasonable?", "Noah says 412 × 9 = 37" + NB + "080.",
             "Estimate: 400 × 9 = 3600. 37" + NB + "080 is about 10 times too big, so it is not reasonable. "
             "The exact answer is 3708.", "not reasonable")
        + "<h2>Estimating with money</h2>"
        "<p>Round each price to the nearest dollar. 50c or more rounds up; less than 50c rounds down.</p>"
        "<figure class='sn-fig'>" + tags_svg([("crayons", 385), ("glue", 240), ("scissors", 670)]) +
        "<figcaption>$3.85 → $4, $2.40 → $2, $6.70 → $7. Estimate: $4 + $2 + $7 = $13. "
        "The exact total is $12.95.</figcaption></figure>"
        + ex("Will $50 be enough?", "A school bag costs $29.95, a hat $12.40 and a ruler $2.60.",
             "Round: $30 + $12 + $3 = $45. $45 is less than $50, so $50 is enough.", "yes")
        + "<h2>Paying cash: round to the nearest 5c</h2>"
        "<p>Australia has no 1c or 2c coins. When you pay with cash, the total is rounded to the nearest 5c. "
        "If you pay by card, you pay the exact amount.</p>"
        "<figure class='sn-fig'>" + cash_table_svg() +
        "<figcaption>Look only at the last digit of the cents. A total that ends in 0 or 5 stays the same.</figcaption></figure>"
        + ex("Cash change", "The bill is $8.62. You pay cash with a $10 note.",
             "Round the total first: $8.62 → $8.60. Then $10 " + MINUS + " $8.60 = $1.40.", "$1.40")
        + ex("Compare deals", "Juice boxes cost $1.40 each, or 4 for $5.",
             "4 × $1.40 = $5.60. $5.60 " + MINUS + " $5.00 = 60c, so the 4 for $5 deal saves 60c.", "4 for $5")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Rounding $3.65 down to $3", "65c is more than 50c, so round up: $4"],
            ["Estimating 400 × 9 as 36" + NB + "000", "Count the zeros: 4 hundreds × 9 = 36 hundreds = 3600"],
            ["Writing 407c as $4.70 or $40.70", "100c = $1, so 407c = $4.07"],
            ["Forgetting to round a cash total: $10 " + MINUS + " $8.62 = $1.38", "Round first: $8.60, so the change is $1.40"],
            ["Choosing the deal with the smaller price tag", "Compare the same amount: the price for 1 litre, or for 3 items"],
        ])
    )


FAQ = [
    {"q": "What does Year 5 learn about estimation in the Australian Curriculum?",
     "a": "Year 5 students check and explain whether answers are reasonable by estimating, including in money problems "
          "(AC9M5N08). They round numbers, use front-end estimation and compare the estimate with the exact answer."},
    {"q": "What is front-end estimation?",
     "a": "Keep the first digit of each number and make the other digits 0, then calculate. "
          "For 6815 + 2742 the estimate is 6000 + 2000 = 8000; it is quick but always lower than the exact answer (here 9557)."},
    {"q": "How does rounding to the nearest 5 cents work in Australia?",
     "a": "Cash totals are rounded because there are no 1c or 2c coins. Totals ending in 1 or 2 round down to 0, "
          "3 or 4 round up to 5, 6 or 7 round down to 5, and 8 or 9 round up to 10. Card payments are not rounded."},
    {"q": "How can my child check if an answer is reasonable?",
     "a": "Round the numbers, work out an estimate in your head and compare. If 412 × 9 gives 37 080 but 400 × 9 = 3600, "
          "the answer is too big and should be checked."},
]


def gen():
    rnd = random.Random(5808)
    P = People(rnd)
    sets = [set_round(), set_reasonable(P), set_money_est(P), set_cents(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vv = [val(c) for c in it["c"] if val(c) is not None]
            assert len(set(vv)) == len(vv), it["c"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "estimation-and-money-problems", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Estimation and Money Problems",
        "seo_title": "Year 5 Estimation and Money Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Estimation and Money Problems",
        "domain": "Number",
        "standard_code": "AC9M5N08",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Check and explain the reasonableness of solutions to problems including financial contexts using estimation strategies appropriate to the context",
        "meta_desc": "Free Year 5 maths worksheets on estimation and money, aligned to the Australian Curriculum (AC9M5N08, AC9M5N09): round to estimate, front-end estimation, check if answers are reasonable, round prices to the nearest dollar, round cash to the nearest 5c, and solve budget and best-buy problems. 100 questions with an answer key, great for NAPLAN practice.",
        "key_big": "Estimate first, then check: if 412 × 9 gives 37 080 but 400 × 9 = 3600, the answer is not reasonable.",
        "key_sub": "Round prices to the nearest dollar to estimate a total. When you pay cash, round the total to the nearest 5c first: $8.62 becomes $8.60, so the change from $10 is $1.40.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|price tags)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
