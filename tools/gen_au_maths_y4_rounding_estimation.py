# -*- coding: utf-8 -*-
"""
Australia Year 4 Maths: Rounding and Estimation
(Australian Curriculum v9.0, AC9M4N07)
  python3 tools/gen_au_maths_y4_rounding_estimation.py
All money is held as whole cents (int), so every total, change and mistake is exact.
Writing money: under $1 as 75c, from $1 as $3.45; rounded estimates as whole dollars ($14).
Cash totals are rounded to the nearest 5c (1, 2 down to 0; 3, 4 up to 5; 6, 7 down to 5; 8, 9 up to 10).
Numbers of 5 or more digits use a no-break space between groups of three (37 080); 4-digit numbers have none.
Every answer is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
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


# ============================================================ set 1: round to the nearest 10, 100, 1000
LOOK = {10: "ones", 100: "tens", 1000: "hundreds"}            # digit to look at
OWN = {10: "tens", 100: "hundreds", 1000: "thousands"}       # digit that is rounded
NEXT1 = {10: "hundred", 100: "thousand", 1000: "ten thousand"}


def digit(n, i):
    return (n // 10 ** i) % 10


def lg(p):
    return len(str(p)) - 1


def round_expl(n, p):
    lo = n // p * p
    r = rnd_to(n, p)
    d = digit(n, lg(p) - 1)
    if n - lo == p // 2:
        s = ("%s is exactly halfway between %s and %s. A number exactly halfway rounds up."
             % (nf(n), nf(lo), nf(lo + p)))
    else:
        s = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s."
             % (nf(n), nf(lo), nf(lo + p), LOOK[p], d,
                "5 or more" if d >= 5 else "4 or less", "up" if r > lo else "down"))
    if r > lo and digit(n, lg(p)) == 9:
        s += (" The %s digit is 9, so rounding up makes 10 %s. Regroup them as 1 %s."
              % (OWN[p], OWN[p], NEXT1[p]))
    if p >= 100 and rnd_to(rnd_to(n, p // 10), p) != r:
        s += " Do not round in steps (%s → %s → %s); look only at the %s digit." % (
            nf(n), nf(rnd_to(n, p // 10)), nf(rnd_to(rnd_to(n, p // 10), p)), LOOK[p])
    return s + " Answer: <b>%s</b>." % nf(r)


def round_cands(n, p):
    """Wrong answers from real mistakes, most likely first."""
    r = rnd_to(n, p)
    lo = n // p * p
    out = []
    if p >= 100:
        out.append(rnd_to(rnd_to(n, p // 10), p))           # rounded in steps (6499 -> 6500 -> 7000)
    out.append(lo + p if r == lo else lo)                    # wrong way / always rounding down (450 -> 400)
    if r > lo and digit(n, lg(p)) == 9:
        out.append(n // (p * 10) * (p * 10))                 # 9 became 0, nothing regrouped
    if r > lo:
        out.append(r + n % p)                                # kept the digits after the place
    if p >= 100:
        out.append(rnd_to(n, p // 10))                       # rounded to the wrong place
        out.append(n // (p // 10) * (p // 10))               # cut off at the wrong place
    out.append(rnd_to(n, p * 10))                            # rounded the wrong digit
    out.append(n // (p * 10) * (p * 10))
    out += [r + p, r - p]
    return [x for x in out if x != r]


def q_round(n, p, line=True):
    lo = n // p * p
    q = "Round %s to the nearest %s." % (nf(n), nf(p))
    if line:
        q = fig(number_line_svg(lo, lo + p, n, p // 10)) + q
    return mq_n(q, rnd_to(n, p), round_cands(n, p), round_expl(n, p))


def q_which_rounds(target, p, right, wrongs):
    assert rnd_to(right, p) == target
    for w in wrongs:
        assert rnd_to(w, p) != target
    lst = "; ".join("%s → %s" % (nf(x), nf(rnd_to(x, p))) for x in [right] + wrongs)
    e = "Round each number to the nearest %s: %s. Only <b>%s</b> rounds to %s." % (nf(p), lst, nf(right), nf(target))
    return mq_n("Which number rounds to %s when you round to the nearest %s?" % (nf(target), nf(p)),
                right, wrongs, e)


def set_round():
    its = []
    for n, p, line in [(47, 10, True), (83, 10, True), (365, 10, True), (726, 10, False), (1238, 10, False),
                       (2995, 10, True),
                       (340, 100, True), (450, 100, True), (682, 100, False), (1749, 100, True), (3962, 100, True),
                       (5050, 100, False),
                       (4682, 1000, True), (2500, 1000, True), (7391, 1000, False), (6499, 1000, True),
                       (9615, 1000, True), (3087, 1000, False)]:
        its.append(q_round(n, p, line))
    its.insert(12, q_which_rounds(500, 100, 462, [438, 551, 550]))
    its.append(q_which_rounds(3000, 1000, 2614, [2499, 3500, 3714]))
    return {"title": "Round to the nearest 10, 100 and 1000", "items": its}


# ============================================================ set 2: estimate sums and differences
def est_terms(terms, p):
    """terms = [(n, +1/-1), ...]; estimate by rounding each number to the nearest p"""
    rs = [(rnd_to(n, p), sg) for n, sg in terms]
    exact = sum(n * sg for n, sg in terms)
    est = sum(r * sg for r, sg in rs)
    down = sum(n // p * p * sg for n, sg in terms)                       # rounded every number down
    finer = sum(rnd_to(n, p // 10) * sg for n, sg in terms) if p > 10 else None   # rounded the wrong digit
    assert est != exact and est > 0

    def expr(xs):
        out = nf(xs[0][0])
        for v, sg in xs[1:]:
            out += (" + " if sg > 0 else " " + MINUS + " ") + nf(v)
        return out
    e = ("Round each number to the nearest %s: %s = <b>%s</b>. (The exact answer is %s.)"
         % (nf(p), expr(rs), nf(est), nf(exact)))
    q = "Estimate %s by rounding each number to the nearest %s." % (expr(terms), nf(p))
    return mq_n(q, est, [down, finer, exact, est + p, est - p, est * 10], e)


def set_sums():
    A, S = 1, -1
    its = []
    for terms, p in [
        ([(38, A), (47, A)], 10), ([(72, A), (29, S)], 10), ([(64, A), (23, A)], 10), ([(91, A), (46, S)], 10),
        ([(28, A), (43, A), (17, A)], 10),
        ([(347, A), (486, A)], 100), ([(812, A), (385, S)], 100), ([(629, A), (254, A)], 100),
        ([(935, A), (468, S)], 100), ([(1246, A), (372, A)], 100), ([(2718, A), (1450, S)], 100),
        ([(298, A), (405, A), (187, A)], 100),
        ([(4682, A), (2371, A)], 1000), ([(8350, A), (2716, S)], 1000), ([(3529, A), (4475, A)], 1000),
        ([(9208, A), (4861, S)], 1000), ([(6815, A), (2742, A)], 1000),
        ([(2150, A), (3870, A), (1460, A)], 1000),
        ([(12480, A), (6390, A)], 1000), ([(25360, A), (9840, S)], 1000),
    ]:
        its.append(est_terms(terms, p))
    return {"title": "Estimate sums and differences", "items": its}


# ============================================================ set 3: estimate products
def est_mul(a, k, p):
    """estimate k × a (k a single digit) by rounding a to the nearest p"""
    ra = rnd_to(a, p)
    other = a // p * p if a // p * p != ra else ra + p
    est, exact = ra * k, a * k
    assert est != exact
    e = ("%s rounds to %s. %d × %s = <b>%s</b>. (The exact answer is %s.)"
         % (nf(a), nf(ra), k, nf(ra), nf(est), nf(exact)))
    q = "Estimate %s × %d by rounding %s to the nearest %s." % (nf(a), k, nf(a), nf(p))
    return mq_n(q, est, [other * k, exact, est * 10, est // 10 if est % 10 == 0 else None, ra + k], e)


def best_sentence(a, k, p, wrongs):
    """Which number sentence gives the best estimate? wrongs = [(x, y), ...] meaning x × y"""
    exact = a * k
    best = (rnd_to(a, p), k)
    allc = [best] + wrongs
    for x, y in wrongs:
        assert abs(x * y - exact) > abs(best[0] * best[1] - exact), (x, y)
    fm = lambda t: "%s × %s" % (nf(t[0]), nf(t[1]))
    e = ("Round %s to the nearest %s: %s. Keep %d as it is. %s = %s, which is close to the exact answer %s."
         % (nf(a), nf(p), nf(best[0]), k, fm(best), nf(best[0] * k), nf(exact)))
    e = e.replace(" = %s, which" % nf(best[0] * k), " = <b>%s</b>, which" % nf(best[0] * k))
    return mcq("Which is the best way to estimate %s × %d?" % (nf(a), k), fm(best), [fm(w) for w in wrongs], e)


def more_less(person, a, k):
    name, she, her = person
    ra = rnd_to(a, 10)
    est, exact = ra * k, a * k
    up = ra > a
    right = "%s, because %d was rounded %s" % ("Less" if up else "More", a, "up" if up else "down")
    cands = ["%s, because %d was rounded %s" % ("More" if up else "Less", a, "up" if up else "down"),
             "%s, because %d was rounded %s" % ("Less" if up else "More", a, "down" if up else "up"),
             "%s, because %d was rounded %s" % ("More" if up else "Less", a, "down" if up else "up")]
    e = ("%d was rounded %s to %d, so the estimate %s is %s than the exact answer. "
         "The exact answer is %d × %d = %s, which is <b>%s</b> than %s."
         % (a, "up" if up else "down", ra, nf(est), "more" if up else "less", a, k, nf(exact),
            "less" if up else "more", nf(est)))
    q = ("%s estimates %d × %d as %d × %d = %s. Is the exact answer more or less than %s?"
         % (name, a, k, ra, k, nf(est), nf(est)))
    return mcq(q, right, cands, e)


def set_products(P):
    its = []
    for a, k in [(38, 4), (52, 3), (67, 5), (29, 6), (84, 7), (43, 8), (76, 9), (95, 4)]:
        its.append(est_mul(a, k, 10))
    its.append(best_sentence(47, 6, 10, [(40, 6), (47, 10), (50, 10)]))
    its.append(more_less(P.next(), 38, 4))
    for a, k in [(312, 3), (487, 2), (598, 4), (721, 6), (845, 5), (263, 7)]:
        its.append(est_mul(a, k, 100))
    its.append(best_sentence(289, 3, 100, [(200, 3), (289, 10), (30, 3)]))
    its.append(more_less(P.next(), 62, 5))
    for a, k in [(2085, 3), (1920, 4)]:
        its.append(est_mul(a, k, 1000))
    return {"title": "Estimate products", "items": its}


# ============================================================ set 4: is the answer reasonable?
def calc(expr):
    return eval(expr.replace("×", "*").replace("÷", "//").replace(MINUS, "-"))


def reasonable_pick(expr, est, wrong, why):
    exact = calc(expr)
    assert abs(exact - est) / est < 0.25, (expr, exact, est)
    for w in wrong:
        assert abs(w - est) / est > 0.4, (expr, w, est)
    e = "Estimate: %s. Only <b>%s</b> is close to %s." % (why, nf(exact), nf(est))
    return mq_n("Use an estimate to choose the reasonable answer.<br>%s = ?" % expr.replace("-", MINUS),
                exact, wrong, e)


def yes_no(person, expr, said, est, why, slip=""):
    name = person[0]
    exact = calc(expr)
    ok = abs(said - est) / est < 0.25
    assert ok == (said == exact), (expr, said, exact, est)
    if not ok:
        assert abs(said - est) / est > 0.4
    right = ("Yes, it is close to %s" if ok else "No, it should be about %s") % nf(est)
    other = ("No, it should be about %s" if ok else "Yes, it is close to %s") % nf(est)
    big = est * 10 if said > est else est // 10
    traps = ["Yes, it is close to %s" % nf(big), "No, it should be about %s" % nf(big)]
    e = "Estimate: %s. %s is %s %s, so it is %s.%s" % (
        why, nf(said), "close to" if ok else "far from", nf(est),
        "<b>reasonable</b>" if ok else "<b>not reasonable</b>",
        "" if ok else " The exact answer is %s.%s" % (nf(exact), slip))
    q = "%s works out %s and gets %s. Is the answer reasonable?" % (name, expr.replace("-", MINUS), nf(said))
    return mcq(q, right, [other] + traps, e)


def best_est(expr, cands, why):
    exact = calc(expr)
    best = min(cands, key=lambda x: abs(x - exact))
    for x in cands:
        if x != best:
            assert abs(x - exact) > abs(best - exact)
    e = "%s = <b>%s</b>. (The exact answer is %s, so this estimate is the closest.)" % (why, nf(best), nf(exact))
    return mq_n("Which estimate is closest to the exact answer of %s?" % expr.replace("-", MINUS), best,
                [x for x in cands if x != best], e)


def set_reasonable(P):
    its = []
    for expr, est, wrong, why in [
        ("386 + 247", 600, [6330, 2856, 139], "400 + 200 = 600"),
        ("923 - 458", 400, [1381, 4650, 47], "900 " + MINUS + " 500 = 400"),
        ("4 × 68", 280, [2720, 72, 27], "4 × 70 = 280"),
        ("9 × 41", 360, [3690, 50, 36], "9 × 40 = 360"),
        ("6 × 512", 3000, [30720, 518, 307], "6 × 500 = 3000"),
        ("2389 + 3546", 6000, [59350, 1157, 593], "2000 + 4000 = 6000"),
        ("7015 - 2988", 4000, [10003, 40270, 403], "7000 " + MINUS + " 3000 = 4000"),
        ("8 × 395", 3200, [31600, 403, 316], "8 × 400 = 3200"),
    ]:
        its.append(reasonable_pick(expr, est, wrong, why))
    for expr, said, est, why, slip in [
        ("9 × 48", 432, 450, "9 × 50 = 450", ""),
        ("293 + 418", 711, 700, "300 + 400 = 700", ""),
        ("4 × 76", 2824, 320, "4 × 80 = 320",
         " (4 × 7 = 28 and 4 × 6 = 24 were written side by side, but 4 × 7 tens = 28 tens = 280.)"),
        ("6 × 307", 1842, 1800, "6 × 300 = 1800", ""),
        ("3 × 214", 6312, 600, "3 × 200 = 600",
         " (Each part was written side by side; 3 × 214 = 600 + 30 + 12.)"),
        ("5216 - 2980", 2236, 2000, "5000 " + MINUS + " 3000 = 2000", ""),
        ("7 × 29", 1463, 210, "7 × 30 = 210",
         " (7 × 2 tens = 14 tens = 140, not 1400.)"),
        ("1875 + 2460", 4335, 4000, "2000 + 2000 = 4000", ""),
    ]:
        its.append(yes_no(P.next(), expr, said, est, why, slip))
    its.append(best_est("52 × 7", [350, 300, 3500, 35], "50 × 7"))
    its.append(best_est("689 + 214", [900, 800, 9000, 90], "700 + 200"))
    its.append(best_est("3 × 1985", [6000, 3000, 600, 60000], "3 × 2000"))
    its.append(best_est("8120 - 2965", [5000, 6000, 500, 50000], "8000 " + MINUS + " 3000"))
    return {"title": "Is the answer reasonable?", "items": its}


# ============================================================ set 5: money word problems
def near_dollar(p, item, cands):
    r = rnd_to(p, 100)
    lo = p // 100 * 100
    c = p % 100
    if c == 50:
        why = "%s is exactly halfway between %s and %s. Halfway rounds up, so <b>%s</b>." % (
            aud(p), dol(lo), dol(lo + 100), dol(r))
    else:
        why = "%s is between %s and %s. Look at the cents: %dc is %s 50c, so round %s to <b>%s</b>." % (
            aud(p), dol(lo), dol(lo + 100), c, "more than" if c > 50 else "less than",
            "up" if r > lo else "down", dol(r))
    q = "A %s costs %s. What is the price to the nearest dollar?" % (item, aud(p))
    fm = lambda x: dol(x) if x % 100 == 0 else aud(x)
    return mcq(q, dol(r), [fm(x) for x in cands], why)


def sum_est(items, ask):
    prices = [p for _, p in items]
    rs = [rnd_to(p, 100) for p in prices]
    est, exact = sum(rs), sum(prices)
    down = sum(p // 100 * 100 for p in prices)
    up = sum(p // 100 * 100 + 100 for p in prices)
    assert est != exact
    e = "Round each price to the nearest dollar: %s = <b>%s</b>. (The exact total is %s.)" % (
        " + ".join(dol(r) for r in rs), dol(est), aud(exact))
    fm = lambda x: dol(x) if x % 100 == 0 else aud(x)
    return mcq(fig(tags_svg(items)) + ask, dol(est), [fm(down), fm(up), fm(exact), fm(est + 100), fm(est - 100)], e)


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


RULE5 = {1: "1 rounds down to 0", 2: "2 rounds down to 0", 3: "3 rounds up to 5", 4: "4 rounds up to 5",
         6: "6 rounds down to 5", 7: "7 rounds down to 5", 8: "8 rounds up to 10", 9: "9 rounds up to 10"}


def cash_change(price, paid, who, she):
    r = r5(price)
    ch = paid - r
    lo5 = price // 5 * 5
    wrong_way = lo5 + 5 if r == lo5 else lo5
    e = ("First round the total to the nearest 5c: %s → %s. Then %s " + MINUS + " %s = <b>%s</b>.") % (
        aud(price), aud(r), dol(paid), aud(r), aud(ch))
    q = ("%s’s shopping comes to %s. %s pays cash with a %s note, so the total is rounded to the nearest 5c. "
         "How much change does %s get?" % (who, aud(price), cap(she), dol(paid), she))
    return mq_c(q, ch, [paid - price, paid - wrong_way, ch + 100, ch - 100], e)


def set_money(P):
    its = []
    for p, item, wr in [(345, "pack of stickers", [400, 350, 345]), (750, "pair of thongs", [700, 750, 7500]),
                        (1295, "beach towel", [1200, 1000, 1295]), (608, "notebook", [700, 610, 608]),
                        (1950, "cricket ball", [1900, 1950, 1000])]:
        its.append(near_dollar(p, item, wr))
    for items in [[("pencils", 295), ("ruler", 420), ("eraser", 165)],
                  [("milk", 335), ("bread", 480), ("apples", 610)],
                  [("sunscreen", 1295), ("hat", 1850), ("water", 245)],
                  [("footy", 2490), ("socks", 875), ("cap", 1520)]]:
        its.append(sum_est(items, "Round each price to the nearest dollar. Estimate the total cost."))
    its.append(enough(P.next(), [("a lunch box", 1295), ("a drink bottle", 1840), ("a pencil case", 960)], 5000,
                      "the shops"))
    its.append(enough(P.next(), [("a hot dog", 650), ("a juice", 380), ("an ice block", 290)], 1000,
                      "the athletics carnival"))
    its.append(enough(P.next(), [("a book", 1499), ("a colouring book", 825)], 2000, "the book fair"))
    # cash rounding to the nearest 5c
    for p, ctx in [(437, "At the school canteen a sandwich and a juice cost %s."),
                   (691, "At the sausage sizzle a family buys lunch for %s."),
                   (348, "At the newsagent a pen and a card cost %s."),
                   (1293, "At the supermarket the shopping costs %s.")]:
        name, she, her = P.next()
        q = ctx % aud(p) + " %s pays cash, so the total is rounded to the nearest 5c. How much does %s pay?" % (name, she)
        r = r5(p)
        lo5 = p // 5 * 5
        other = lo5 + 5 if r == lo5 else lo5
        e = ("Look at the last digit of the cents: %s. %s is closer to %s than to %s, so %s pays <b>%s</b>."
             % (RULE5[p % 10], aud(p), aud(r), aud(other), she, aud(r)))
        its.append(mq_c(q, r, [other, p // 10 * 10, rnd_to(p, 10), p, rnd_to(p, 100)], e))
    for price, paid in [(642, 1000), (1347, 2000)]:
        name, she, her = P.next()
        its.append(cash_change(price, paid, name, she))
    # is the money answer reasonable?
    name, she, her = P.next()
    assert 4 * 295 == 1180
    its.append(mcq("%s buys 4 packs of footy cards at $2.95 each. The calculator shows $118.00. "
                   "Is this reasonable?" % name, "No, it should be about $12",
                   ["Yes, it is close to $120", "No, it should be about $1", "Yes, it is close to $12"],
                   "$2.95 rounds to $3. 4 × $3 = $12, so $118.00 is <b>not reasonable</b>. The exact total is $11.80; "
                   "the decimal point was put in the wrong place."))
    assert 495 + 720 + 285 == 1500
    its.append(mcq("Dad buys bread for $4.95, cheese for $7.20 and grapes for $2.85. The receipt says $15.00. "
                   "Is this reasonable?", "Yes, it is close to $15",
                   ["No, it should be about $13", "No, it should be about $150", "Yes, it is close to $150"],
                   "Round: $5 + $7 + $3 = $15. $15.00 is close to $15, so it is <b>reasonable</b>. "
                   "(Rounding every price down gives $4 + $7 + $2 = $13, which is too low.)"))
    return {"title": "Money: round, estimate and pay cash", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Rounding: find the closer friendly number</h2>"
        "<p>To round, find the two friendly numbers on each side. Then look at the digit to the right of the place "
        "you are rounding to. 5 or more rounds up. 4 or less rounds down.</p>"
        + table(["Round to the nearest", "Look at the", "Example"], [
            ["10", "ones digit", "365 → 370"],
            ["100", "tens digit", "1749 → 1700"],
            ["1000", "hundreds digit", "4682 → 5000"],
        ]) +
        "<figure class='sn-fig'>" + number_line_svg(4000, 5000, 4682, 100) +
        "<figcaption>4682 is past the halfway point, 4500, so to the nearest 1000 it rounds up to 5000.</figcaption></figure>"
        + ex("Exactly halfway", "Round 450 to the nearest 100.",
             "450 is exactly halfway between 400 and 500. A number exactly halfway rounds up.", "500")
        + ex("A 9 that rounds up", "Round 3962 to the nearest 100.",
             "Look at the tens digit: 6, so round up. 9 hundreds + 1 hundred = 10 hundreds = 1 thousand.", "4000")
        + "<h2>Estimate, then check</h2>"
        "<p>An estimate is a quick answer that is close to the exact answer. Round the numbers, "
        "then work it out in your head. If your exact answer is far from the estimate, check your working.</p>"
        + ex("Estimate a sum", "Estimate 347 + 486.", "Round to the nearest 100: 300 + 500 = 800. "
             "The exact answer is 833, which is close.", "about 800")
        + ex("Estimate a product", "Estimate 38 × 4.", "38 rounds to 40. 40 × 4 = 160. "
             "The exact answer is 152. 38 was rounded up, so the estimate is a bit too big.", "about 160")
        + ex("Is the answer reasonable?", "Jack says 4 × 76 = 2824.",
             "Estimate: 4 × 80 = 320. 2824 is far too big, so it is not reasonable. The exact answer is 304.",
             "not reasonable")
        + "<h2>Estimating with money</h2>"
        "<p>Round each price to the nearest dollar. 50c or more rounds up; less than 50c rounds down.</p>"
        "<figure class='sn-fig'>" + tags_svg([("crayons", 385), ("glue", 240), ("scissors", 670)]) +
        "<figcaption>$3.85 → $4, $2.40 → $2, $6.70 → $7. Estimate: $4 + $2 + $7 = $13. "
        "The exact total is $12.95.</figcaption></figure>"
        "<h2>Paying cash: round to the nearest 5c</h2>"
        "<p>Australia has no 1c or 2c coins. When you pay with cash, the total is rounded to the nearest 5c. "
        "If you pay by card, you pay the exact amount.</p>"
        "<figure class='sn-fig'>" + cash_table_svg() +
        "<figcaption>Look only at the last digit of the cents. A total that ends in 0 or 5 stays the same.</figcaption></figure>"
        + ex("Cash change", "The bill is $8.62. You pay cash with a $10 note.",
             "Round the total first: $8.62 → $8.60. Then $10 " + MINUS + " $8.60 = $1.40.", "$1.40")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Looking at the wrong digit: 1749 to the nearest 100 → 1750",
             "For the nearest 100, look at the tens digit: 4, so 1700"],
            ["Rounding 450 down to 400", "Exactly halfway rounds up: 500"],
            ["Always rounding down: 682 → 600", "The tens digit is 8 (5 or more), so round up: 700"],
            ["Rounding in steps: 6499 → 6500 → 7000", "Look only at the hundreds digit: 4, so 6000"],
            ["Not checking: 3 × 214 = 6312", "Estimate 3 × 200 = 600; 6312 is far too big. The answer is 642"],
        ])
    )


FAQ = [
    {"q": "What does Year 4 learn about rounding and estimation in the Australian Curriculum?",
     "a": "Year 4 students choose and use estimation and rounding to check whether answers are reasonable, including "
          "money amounts (AC9M4N07). They round to the nearest 10, 100 or 1000 and estimate sums, differences and products."},
    {"q": "Does 450 round to 400 or 500?",
     "a": "To the nearest 100, 450 rounds to 500. A number exactly halfway between two hundreds is rounded up."},
    {"q": "How does rounding to the nearest 5 cents work in Australia?",
     "a": "Cash totals are rounded because there are no 1c or 2c coins. Totals ending in 1 or 2 round down to 0, "
          "3 or 4 round up to 5, 6 or 7 round down to 5, and 8 or 9 round up to 10. Card payments are not rounded."},
    {"q": "How can my child check if an answer is reasonable?",
     "a": "Round the numbers and work out an estimate in your head first. If 4 × 76 gives 2824 but 4 × 80 = 320, "
          "the answer is far too big and should be checked."},
]


def gen():
    rnd = random.Random(4808)
    P = People(rnd)
    sets = [set_round(), set_sums(), set_products(P), set_reasonable(P), set_money(P)]
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
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "rounding-and-estimation", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 4 Rounding and Estimation",
        "seo_title": "Year 4 Rounding and Estimation Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Rounding and Estimation",
        "domain": "Number",
        "standard_code": "AC9M4N07",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Choose and use estimation and rounding to check and explain the reasonableness of calculations including the results of financial transactions",
        "meta_desc": "Free Year 4 maths worksheets on rounding and estimation, aligned to the Australian Curriculum (AC9M4N07): round to the nearest 10, 100 and 1000 on number lines, estimate sums, differences and products, check if answers are reasonable, round prices to the nearest dollar and round cash to the nearest 5c. 100 questions with an answer key.",
        "key_big": "To round, look at the digit to the right: 5 or more rounds up, 4 or less rounds down. 450 rounds to 500.",
        "key_sub": "Estimate before you calculate: 38 × 4 is about 40 × 4 = 160. If your answer is far from the estimate, check it. When you pay cash, round the total to the nearest 5c.",
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
