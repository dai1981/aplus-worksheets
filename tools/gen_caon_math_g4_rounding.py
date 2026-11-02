# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 4 Math: Rounding and Estimating
(Ontario Mathematics Curriculum 2020, Grade 4: B1.3 round whole numbers to the nearest ten, hundred or thousand;
 B1.8 round decimal tenths to the nearest whole number)
  python3 tools/gen_caon_math_g4_rounding.py
Whole numbers to 10 000 and decimal tenths. Round half up (4500 -> 5000, 3.5 -> 4). Every answer is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#6b6259"
CARD = "#eef5f0"
CARDEDGE = "#7aa58a"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
MINUS = "−"


# ------------------------------------------------------------ numbers
def nf(n):
    """4536 -> '4536', 10000 -> '10 000' (no-break space from 5 digits)."""
    assert n >= 0 and n == int(n), n
    s = str(int(n))
    if len(s) < 5:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(out)


def dec(t):
    """tenths -> text: 35 -> '3.5', 40 -> '4'"""
    assert t >= 0
    return nf(t // 10) if t % 10 == 0 else "%s.%d" % (nf(t // 10), t % 10)


def dol(n):
    return "$" + nf(n)


def unit(u):
    return lambda n: nf(n) + " " + u


def unit_t(u):
    return lambda t: dec(t) + " " + u


def val(s):
    """Value of a number text, or None for words."""
    s = re.sub(r"<[^>]+>", "", s).replace(NB, "")
    m = re.match(r"^(\$)?(\d+(?:\.\d)?)( [a-zA-Z]+)?$", s)
    if m:
        return ((m.group(1) or "") + (m.group(3) or ""), Fraction(m.group(2)))
    return None


def rnd_to(n, p):
    """round half up to the nearest p"""
    return (n + p // 2) // p * p


def cap(s):
    return s[0].upper() + s[1:]


def opf(op):
    return " + " if op > 0 else " " + MINUS + " "


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


def mq_n(q, correct, cands, e, fmt=nf):
    return mcq(q, fmt(correct), [fmt(x) for x in cands if x is not None and 0 < x <= 10000], e)


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


def cards_svg(items):
    """Cards in one row: items = [(label, value text), ...]"""
    tw, th, gap, pad = 124, 66, 10, 4
    W = pad * 2 + len(items) * tw + (len(items) - 1) * gap
    H = th + pad * 2
    s = []
    for i, (name, v) in enumerate(items):
        assert len(name) <= 14, name
        x = pad + i * (tw + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, pad, tw, th, CARD, CARDEDGE))
        s.append(text(x + tw / 2, pad + 25, name, 14, col=GREY))
        s.append(text(x + tw / 2, pad + 53, v, 20))
    return svg_wrap(W, H, "".join(s), "cards: " + ", ".join("%s %s" % (n, v) for n, v in items))


# ============================================================ rounding whole numbers
WORD = {10: "ten", 100: "hundred", 1000: "thousand"}
LOOK = {10: "ones", 100: "tens", 1000: "hundreds"}          # digit to look at
OWN = {10: "tens", 100: "hundreds", 1000: "thousands"}      # place being rounded


def digit(n, i):
    return (n // 10 ** i) % 10


def lg(p):
    return len(str(p)) - 1


def round_expl(n, p, fmt=nf):
    lo = n // p * p
    r = rnd_to(n, p)
    d = digit(n, lg(p) - 1)
    if n - lo == p // 2:
        s = ("%s is exactly halfway between %s and %s. The %s digit is 5, and 5 rounds up."
             % (nf(n), nf(lo), nf(lo + p), LOOK[p]))
    else:
        s = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s."
             % (nf(n), nf(lo), nf(lo + p), LOOK[p], d,
                "%d is 5 or more" % d if d >= 5 else "%d is 4 or less" % d, "up" if r > lo else "down"))
    if r > lo and digit(n, lg(p)) == 9:
        s += " %d %s and 1 more %s make %d %s, which is %s." % (
            n // p, OWN[p], WORD[p], r // p, OWN[p], nf(r))
    chain, q = [n], 10
    while q <= p:
        chain.append(rnd_to(chain[-1], q))
        q *= 10
    chain = [x for i, x in enumerate(chain) if i == 0 or x != chain[i - 1]]
    if p >= 100 and chain[-1] != r:
        s += " Do not round in steps (%s). Look only at the %s digit." % (" → ".join(nf(x) for x in chain), LOOK[p])
    return s + " Answer: <b>%s</b>." % fmt(r)


def round_cands(n, p):
    """Wrong answers from real mistakes, most likely first."""
    r = rnd_to(n, p)
    lo = n // p * p
    out = []
    if p == 1000:
        out.append(rnd_to(rnd_to(rnd_to(n, 10), 100), 1000))  # rounded in steps (1449 -> 1450 -> 1500 -> 2000)
    if p >= 100:
        out.append(rnd_to(rnd_to(n, p // 10), p))           # rounded in steps (3462 -> 3500 -> 4000)
    out.append(lo + p if r == lo else lo)                    # wrong way / always rounding down (4500 -> 4000)
    if p >= 100:
        out.append(rnd_to(n, p // 10))                       # rounded the wrong place (6382 -> 6400)
    if r > lo and digit(n, lg(p)) == 9:
        out.append(n // (p * 10) * (p * 10))                 # 9 became 0, nothing regrouped
    if r > lo:
        out.append(r + n % p)                                # kept the digits after the place
    if p == 10:
        out.append(n)                                        # did not round
        out.append(rnd_to(n, 100))                           # rounded the wrong digit
    else:
        out.append(n // (p // 10) * (p // 10))               # cut off at the wrong place
    out += [r + p, r - p, n]
    return [x for x in out if x != r]


def q_round(n, p, line=True, q=None, fmt=nf):
    lo = n // p * p
    q = q or "Round %s to the nearest %s." % (nf(n), WORD[p])
    if line:
        q = fig(number_line_svg(lo, lo + p, n, p // 10)) + q
    return mq_n(q, rnd_to(n, p), round_cands(n, p), round_expl(n, p, fmt), fmt)


def q_which_rounds(target, p, right, wrongs):
    assert rnd_to(right, p) == target
    for w in wrongs:
        assert rnd_to(w, p) != target
    lst = "; ".join("%s → %s" % (nf(x), nf(rnd_to(x, p))) for x in [right] + wrongs)
    e = "Round each number to the nearest %s: %s. Only <b>%s</b> rounds to %s." % (WORD[p], lst, nf(right), nf(target))
    return mq_n("Which number rounds to %s when you round to the nearest %s?" % (nf(target), WORD[p]),
                right, wrongs, e)


# ============================================================ set 1: nearest ten and hundred
def set_round_10_100():
    its = []
    for n, line in [(368, True), (1243, True), (2875, True), (3352, False), (4605, True), (5098, True),
                    (7996, True), (6431, False)]:
        its.append(q_round(n, 10, line))
    its.append(q_which_rounds(2470, 10, 2466, [2475, 2464, 2476]))
    for n, line in [(642, True), (2308, True), (4519, True), (1850, True), (8072, True), (7450, False),
                    (3749, False), (5961, True), (6984, False), (9035, True)]:
        its.append(q_round(n, 100, line))
    its.append(q_which_rounds(3500, 100, 3462, [3438, 3551, 3550]))
    return {"title": "Round to the nearest ten and hundred", "items": its}


# ============================================================ set 2: nearest thousand
def set_round_1000():
    its = []
    for n, line in [(4682, True), (7391, True), (5208, True), (3087, False), (650, True), (2500, True),
                    (4500, True), (8549, False), (5555, False), (6499, False), (1449, True), (9615, True)]:
        its.append(q_round(n, 1000, line))
    its.append(q_which_rounds(3000, 1000, 2614, [2499, 3500, 3714]))
    its.append(q_which_rounds(7000, 1000, 7381, [6499, 7500, 7612]))
    for x in range(5500, 6500):
        assert rnd_to(x, 1000) == 6000
    assert rnd_to(5499, 1000) == 5000 and rnd_to(4499, 1000) == 4000 and rnd_to(4500, 1000) == 5000
    its.append(mq_n("What is the smallest whole number that rounds to 6000 when you round to the nearest thousand?",
                    5500, [5499, 5000, 5501],
                    "The numbers from 5500 to 6499 round to 6000. 5499 has a 4 in the hundreds place, so it "
                    "rounds down to 5000. The smallest is <b>5500</b>, because 5 in the hundreds place rounds up."))
    its.append(mq_n("What is the largest whole number that rounds to 4000 when you round to the nearest thousand?",
                    4499, [4500, 4999, 4490],
                    "The numbers from 3500 to 4499 round to 4000. 4500 is exactly halfway, so it rounds up to 5000. "
                    "4490 rounds to 4000 too, but 4499 is larger. The largest is <b>4499</b>."))
    its.append(mcq("Which digit do you look at to round 5273 to the nearest thousand?",
                   "the hundreds digit, 2",
                   ["the thousands digit, 5", "the tens digit, 7", "the ones digit, 3"],
                   "To round to the nearest thousand, look one place to the right of the thousands: the "
                   "<b>hundreds digit, 2</b>. 2 is 4 or less, so 5273 rounds down to 5000."))
    its.append(mcq("Liam says 4500 rounds to 4000 when you round to the nearest thousand. Is he right?",
                   "No, it rounds to 5000",
                   ["Yes, because 4 is less than 5", "Yes, because it rounds down", "No, it rounds to 4600"],
                   "4500 is exactly halfway between 4000 and 5000. The hundreds digit is 5, and 5 rounds up. "
                   "Liam is not right: 4500 rounds to <b>5000</b>."))
    assert rnd_to(6382, 1000) == 6000 and rnd_to(6382, 100) == 6400
    its.append(mq_n("Owen rounds 6382 to the nearest thousand and gets 6400. What should he get?",
                    6000, [6400, 6380, 7000],
                    "Owen rounded to the nearest hundred. For the nearest thousand, look at the hundreds digit: 3. "
                    "3 is 4 or less, so round down. 6382 rounds to <b>6000</b>."))
    assert rnd_to(3462, 1000) == 3000 and rnd_to(rnd_to(rnd_to(3462, 10), 100), 1000) == 4000
    its.append(mq_n("Maya rounds 3462 to the nearest thousand. She says “3462 → 3460 → 3500 → 4000.” "
                    "What is the right answer?",
                    3000, [4000, 3500, 3460],
                    "Do not round in steps. To round to the nearest thousand, look only at the hundreds digit: 4. "
                    "4 is 4 or less, so round down. 3462 rounds to <b>3000</b>."))
    return {"title": "Round to the nearest thousand", "items": its}


# ============================================================ set 3: round tenths to the nearest whole number
def round_dec_expl(t, fmt):
    lo = t // 10
    r = rnd_to(t, 10) // 10
    d = t % 10
    if d == 5:
        s = "%s is exactly halfway between %s and %s. The tenths digit is 5, and 5 rounds up." % (
            dec(t), nf(lo), nf(lo + 1))
    else:
        s = "%s is between %s and %s. Look at the tenths digit: %d. %s, so round %s." % (
            dec(t), nf(lo), nf(lo + 1), d, "%d is 5 or more" % d if d >= 5 else "%d is 4 or less" % d,
            "up" if r > lo else "down")
    if r > lo and lo % 10 == 9:
        s += " %d + 1 = %s." % (lo, nf(r))
    return s + " Answer: <b>%s</b>." % fmt(r * 10)


def round_dec_cands(t):
    """in tenths; real mistakes first"""
    r = rnd_to(t, 10)
    lo = t // 10 * 10
    out = [lo + 10 if r == lo else lo,      # wrong way / just drops the decimal part
           t]                               # did not round
    if t >= 100:
        out.append(rnd_to(t, 100))         # rounded to the nearest ten
    out += [r + 10, r - 10, t + 10 - t % 10 + 10]
    return [x for x in out if x != r]


def q_round_dec(t, line=True, q=None, fmt=dec):
    assert t % 10 != 0 and rnd_to(t, 10) > 0
    q = q or "Round %s to the nearest whole number." % dec(t)
    if line:
        lo = t // 10 * 10
        q = fig(number_line_svg(lo, lo + 10, t, 1, dec)) + q
    return mcq(q, fmt(rnd_to(t, 10)), [fmt(x) for x in round_dec_cands(t) if x >= 0], round_dec_expl(t, fmt))


def set_round_tenths():
    its = []
    for t, line in [(23, True), (68, True), (35, True), (74, True), (16, True), (45, False), (92, True),
                    (85, True), (6, True), (124, False), (97, True)]:
        its.append(q_round_dec(t, line))
    kg, kmf, L, m, cm = unit_t("kg"), unit_t("km"), unit_t("L"), unit_t("m"), unit_t("cm")
    its.append(q_round_dec(46, True, "A pumpkin from the farm has a mass of 4.6 kg. "
                           "What is its mass to the nearest kilogram?", kg))
    its.append(q_round_dec(34, False, "Kai skis a trail that is 3.4 km long. "
                           "How long is the trail to the nearest kilometre?", kmf))
    its.append(q_round_dec(15, True, "Ethan’s water jug holds 1.5 L. "
                           "How much does it hold to the nearest litre?", L))
    its.append(q_round_dec(65, False, "Sofia cuts a piece of ribbon 6.5 m long for a craft. "
                           "How long is it to the nearest metre?", m))
    its.append(q_round_dec(143, True, "On a snow day, 14.3 cm of snow falls in Ottawa. "
                           "How much snow is that to the nearest centimetre?", cm))
    its.append(q_round_dec(198, False, "Hana’s family drives 19.8 km to the skating rink. "
                           "How far is that to the nearest kilometre?", kmf))
    assert rnd_to(46, 10) == 50 and all(rnd_to(x, 10) != 50 for x in (44, 55, 56))
    its.append(mcq("Which decimal rounds to 5 when you round to the nearest whole number?", "4.6",
                   ["4.4", "5.5", "5.6"],
                   "Round each one: 4.6 → 5; 4.4 → 4; 5.5 → 6; 5.6 → 6. Only <b>4.6</b> rounds to 5."))
    assert rnd_to(65, 10) == 70
    its.append(mcq("Zoe says 6.5 rounds to 6 when you round to the nearest whole number. Is she right?",
                   "No, it rounds to 7",
                   ["Yes, because 6 is less than 7", "Yes, because it rounds down", "No, it rounds to 6.6"],
                   "6.5 is exactly halfway between 6 and 7. The tenths digit is 5, and 5 rounds up. "
                   "Zoe is not right: 6.5 rounds to <b>7</b>."))
    assert rnd_to(38, 10) == 40
    its.append(mq_n("Nathan rounds 3.8 to the nearest whole number. He drops the .8 and gets 3. What should he get?",
                    40, [30, 38, 50], "Look at the tenths digit: 8. 8 is 5 or more, so round up. "
                    "3.8 is closer to 4 than to 3. Answer: <b>4</b>.", dec))
    return {"title": "Round tenths to the nearest whole number", "items": its}


# ============================================================ set 4: estimate sums and differences
def expr(xs, fmt=nf):
    out = fmt(xs[0][0])
    for v, sg in xs[1:]:
        out += opf(sg) + fmt(v)
    return out


def est_core(terms, p):
    rs = [(rnd_to(n, p), sg) for n, sg in terms]
    exact = sum(n * sg for n, sg in terms)
    est = sum(r * sg for r, sg in rs)
    down = sum(n // p * p * sg for n, sg in terms)
    assert est != exact and est > 0 and exact > 0 and exact <= 10000
    return rs, exact, est, down


def est_cands(terms, p, rs, exact, est, down):
    out = [down]
    if p >= 100:
        out.append(sum(rnd_to(n, p // 10) * sg for n, sg in terms))   # rounded to the wrong place
    out.append(exact)
    if any(sg < 0 for _, sg in terms):
        out.append(sum(r for r, _ in rs))                              # added instead of subtracting
    out += [est + p, est - p]
    return out


def est_terms(terms, p):
    rs, exact, est, down = est_core(terms, p)
    e = ("Round each number to the nearest %s: %s = <b>%s</b>. (The exact answer is %s.)"
         % (WORD[p], expr(rs), nf(est), nf(exact)))
    q = "Estimate %s by rounding each number to the nearest %s." % (expr(terms), WORD[p])
    return mq_n(q, est, est_cands(terms, p, rs, exact, est, down), e)


def set_sums():
    A, S = 1, -1
    its = []
    for terms, p in [
        ([(67, A), (28, A)], 10), ([(243, A), (168, A)], 10), ([(526, A), (283, S)], 10),
        ([(718, A), (156, A)], 10), ([(1265, A), (342, A)], 10),
        ([(347, A), (486, A)], 100), ([(812, A), (385, S)], 100), ([(1246, A), (372, A)], 100),
        ([(2718, A), (1450, S)], 100), ([(3529, A), (1284, A)], 100), ([(4062, A), (1875, S)], 100),
        ([(298, A), (405, A), (187, A)], 100),
        ([(4682, A), (2371, A)], 1000), ([(8350, A), (2716, S)], 1000), ([(3529, A), (4475, A)], 1000),
        ([(9208, A), (4861, S)], 1000), ([(6815, A), (2742, A)], 1000), ([(7604, A), (3518, S)], 1000),
        ([(5390, A), (2580, A)], 1000), ([(2150, A), (3870, A), (1460, A)], 1000),
    ]:
        its.append(est_terms(terms, p))
    return {"title": "Estimate sums and differences", "items": its}


# ============================================================ set 5: reasonable answers and word problems
def far(x, est):
    return abs(x - est) / est


def colsub(a, b):
    """smaller digit from the bigger digit in every column (a real mistake)"""
    sa, sb = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(sa, sb)))


def nocarry(a, b):
    """add each column and drop the carry"""
    sa, sb = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str((int(x) + int(y)) % 10) for x, y in zip(sa, sb)))


def word_est(q, terms, p, fmt=nf, pic=None):
    rs, exact, est, down = est_core(terms, p)
    e = ("Round to the nearest %s: %s = <b>%s</b>. (The exact answer is %s.)"
         % (WORD[p], expr(rs, fmt), fmt(est), fmt(exact)))
    if pic:
        q = fig(cards_svg(pic)) + q
    return mq_n(q, est, est_cands(terms, p, rs, exact, est, down), e, fmt)


def word_est_dec(q, terms, fmt):
    """terms in tenths; round each to the nearest whole number"""
    rs = [(rnd_to(t, 10), sg) for t, sg in terms]
    exact = sum(t * sg for t, sg in terms)
    est = sum(r * sg for r, sg in rs)
    down = sum(t // 10 * 10 * sg for t, sg in terms)
    assert est != exact and est > 0 and exact > 0
    cands = [down, exact]
    if any(sg < 0 for _, sg in terms):
        cands.append(sum(r for r, _ in rs))
    cands += [est + 10, est - 10]
    e = ("Round each number to the nearest whole number: %s = <b>%s</b>. (The exact answer is %s.)"
         % (expr(rs, fmt), fmt(est), fmt(exact)))
    return mq_n(q, est, cands, e, fmt)


def yes_no(name, a, b, op, said, p, slip=""):
    exact = a + op * b
    est = rnd_to(a, p) + op * rnd_to(b, p)
    down = a // p * p + op * (b // p * p)
    ok = said == exact
    if ok:
        assert far(said, est) < 0.2
    else:
        assert far(said, est) > 0.35, (a, b, said, est)
    trap = down if down != est else est + p
    right = ("Yes, it is close to %s" if ok else "No, it should be about %s") % nf(est)
    other = ("No, it should be about %s" if ok else "Yes, it is close to %s") % nf(est)
    traps = ["Yes, it is close to %s" % nf(trap), "No, it should be about %s" % nf(trap)]
    why = "%s%s%s = %s" % (nf(rnd_to(a, p)), opf(op), nf(rnd_to(b, p)), nf(est))
    e = "Estimate: %s. %s is %s %s, so it is %s.%s" % (
        why, nf(said), "close to" if ok else "far from", nf(est),
        "<b>reasonable</b>" if ok else "<b>not reasonable</b>",
        "" if ok else " The exact answer is %s.%s" % (nf(exact), slip))
    q = "%s works out %s%s%s and gets %s. Is the answer reasonable? Round to the nearest %s to check." % (
        name, nf(a), opf(op), nf(b), nf(said), WORD[p])
    return mcq(q, right, [other] + traps, e)


def reasonable_pick(a, b, op, p, wrongs, notes):
    exact = a + op * b
    est = rnd_to(a, p) + op * rnd_to(b, p)
    assert far(exact, est) < 0.2
    for w in wrongs:
        assert far(w, est) > 0.35, (a, b, w, est)
    why = "%s%s%s = %s" % (nf(rnd_to(a, p)), opf(op), nf(rnd_to(b, p)), nf(est))
    e = "Estimate: %s. Only <b>%s</b> is close to %s. %s" % (why, nf(exact), nf(est), notes)
    return mq_n("Use an estimate to choose the reasonable answer.<br>%s%s%s = ?" % (nf(a), opf(op), nf(b)),
                exact, wrongs, e)


def more_less(q, a, b, p, noun):
    ra, rb = rnd_to(a, p), rnd_to(b, p)
    up = ra > a and rb > b
    assert up or (ra < a and rb < b)
    est, exact = ra + rb, a + b
    wd = "up" if up else "down"
    other = "down" if up else "up"
    right = "%s, both numbers were rounded %s" % ("Less" if up else "More", wd)
    cands = ["%s, both numbers were rounded %s" % ("More" if up else "Less", wd),
             "%s, both numbers were rounded %s" % ("Less" if up else "More", other),
             "%s, both numbers were rounded %s" % ("More" if up else "Less", other)]
    e = ("%s → %s and %s → %s. Both numbers were rounded %s, so %s is too %s. "
         "The exact total is %s %s, which is <b>%s</b> than %s."
         % (nf(a), nf(ra), nf(b), nf(rb), wd, nf(est), "big" if up else "small", nf(exact), noun,
            "less" if up else "more", nf(est)))
    return mcq(q, right, cands, e)


def enough(q, terms, p, limit, fmt, pic=None):
    rs, exact, est, down = est_core(terms, p)
    ok = est <= limit
    assert ok == (exact <= limit) and est != limit and down != est
    yes, no = "Yes, about %s", "No, about %s"
    right = (yes if ok else no) % fmt(est)
    cands = [(no if ok else yes) % fmt(est), (yes if down <= limit else no) % fmt(down),
             (no if down <= limit else yes) % fmt(down)]
    g = dol if fmt is dol else nf
    e = "Round to the nearest %s: %s = %s. %s is %s %s, so <b>%s</b>. (The exact answer is %s.)" % (
        WORD[p], expr(rs, g), g(est), g(est), "less than" if ok else "more than", g(limit),
        "yes" if ok else "no", g(exact))
    if pic:
        q = fig(cards_svg(pic)) + q
    return mcq(q, right, cands, e)


def set_words():
    A, S = 1, -1
    km, L = unit("km"), unit("L")
    its = []
    its.append(word_est("Mateo’s family drives 448 km from Toronto to Ottawa, then 198 km from Ottawa to Montréal. "
                        "About how far do they drive? Round to the nearest ten.",
                        [(448, A), (198, A)], 10, km))
    its.append(word_est("A maple syrup farm makes 1265 L of syrup in March and 842 L in April. "
                        "About how much syrup is that? Round to the nearest hundred.",
                        [(1265, A), (842, A)], 100, L, pic=[("March", "1265 L"), ("April", "842 L")]))
    its.append(word_est("The school raises $2385 at the Terry Fox Run this year and $2940 last year. "
                        "About how much is that in all? Round to the nearest hundred.",
                        [(2385, A), (2940, A)], 100, dol, pic=[("this year", "$2385"), ("last year", "$2940")]))
    its.append(word_est("3478 fans watch a hockey game on Friday and 2856 fans watch on Saturday. "
                        "About how many more fans come on Friday? Round to the nearest hundred.",
                        [(3478, A), (2856, S)], 100, pic=[("Friday", "3478"), ("Saturday", "2856")]))
    its.append(word_est("Bird watchers count 2650 Canada geese on Monday and 3180 on Tuesday. "
                        "About how many geese is that? Round to the nearest thousand.",
                        [(2650, A), (3180, A)], 1000))
    kgt, kmt, mt = unit_t("kg"), unit_t("km"), unit_t("m")
    its.append(word_est_dec("Owen’s backpack has a mass of 3.6 kg. His lunch bag has a mass of 1.3 kg. "
                            "About what is the total mass? Round each to the nearest whole number.",
                            [(36, A), (13, A)], kgt))
    its.append(word_est_dec("On a canoe trip, Priya’s group paddles 6.4 km before lunch and 4.5 km after lunch. "
                            "About how far do they paddle? Round each to the nearest whole number.",
                            [(64, A), (45, A)], kmt))
    its.append(word_est_dec("Chloe has 8.7 m of ribbon. She uses 2.4 m for a gift. "
                            "About how much ribbon is left? Round each to the nearest whole number.",
                            [(87, A), (24, S)], mt))
    assert 2385 + 1476 == 3861
    its.append(yes_no("Ava", 2385, 1476, A, 3861, 100))
    assert colsub(5203, 1867) == 4664
    its.append(yes_no("Arjun", 5203, 1867, S, 4664, 100,
                      " (The smaller digit was taken from the bigger digit in each column. "
                      "Regroup instead: you cannot take 7 from 3.)"))
    assert 3467 + 2580 == 6047
    its.append(yes_no("Leah", 3467, 258, A, 6047, 100,
                      " (258 was lined up under the wrong places, as if it were 2580. Line up ones with ones.)"))
    its.append(yes_no("Benjamin", 7020, 3984, S, 3036, 1000))
    assert colsub(6215, 2870) == 4665 and 6215 + 2870 == 9085
    its.append(reasonable_pick(6215, 2870, S, 1000, [9085, 4665, 345],
                               "9085 adds instead of subtracting, 4665 takes the smaller digit from the bigger one "
                               "in each column, and 345 forgets the thousands."))
    assert nocarry(1857, 468) == 1215 and 1857 + 4680 == 6537 and 1857 + 468 == 2325
    its.append(reasonable_pick(1857, 468, A, 100, [6537, 1215, 325],
                               "6537 lines up 468 as 4680, 1215 forgets to regroup, "
                               "and 325 forgets the thousands."))
    its.append(more_less("A sugar bush sells 1680 bottles of syrup in spring and 2790 bottles in fall. "
                         "Mei estimates 2000 + 3000 = 5000 bottles. Did it sell more or less than 5000 bottles?",
                         1680, 2790, 1000, "bottles"))
    its.append(more_less("Jayden’s school wants to read 6000 pages in October. Grade 4 reads 4180 pages and "
                         "Grade 5 reads 2345 pages. Jayden estimates 4000 + 2000 = 6000. "
                         "Did they read more or less than 6000 pages?", 4180, 2345, 1000, "pages"))
    its.append(enough("The arena has 6000 seats. 3420 adults and 2190 children have tickets for a hockey game. "
                      "Are there enough seats? Round to the nearest hundred to decide.",
                      [(3420, A), (2190, A)], 100, 6000, unit("people")))
    its.append(enough("Hana’s family has $1500 for a trip to Halifax. The hotel costs $865 and gas and food "
                      "cost $712. Is $1500 enough? Round to the nearest hundred to decide.",
                      [(865, A), (712, A)], 100, 1500, dol, pic=[("hotel", "$865"), ("gas and food", "$712")]))
    its.append(word_est("A fall fair sells 2465 tickets on Saturday, 1830 on Sunday and 1275 on Monday. "
                        "About how many tickets is that? Round to the nearest hundred.",
                        [(2465, A), (1830, A), (1275, A)], 100,
                        pic=[("Saturday", "2465"), ("Sunday", "1830"), ("Monday", "1275")]))
    its.append(word_est("The goal for the food drive is 5000 cans. The students have 3260 cans. "
                        "About how many more cans do they need? Round to the nearest hundred.",
                        [(5000, A), (3260, S)], 100))
    return {"title": "Reasonable answers and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Rounding: find the closer ten, hundred or thousand</h2>"
        "<p>Rounding finds the <b>closest</b> ten, hundred or thousand. Rounded numbers are easy to add and "
        "subtract in your head.</p>"
        "<figure class='sn-fig'>" + number_line_svg(4000, 5000, 4682, 100) +
        "<figcaption>4682 is past the halfway point, 4500, so to the nearest thousand it rounds up to 5000."
        "</figcaption></figure>"
        "<h2>The 5 rule</h2>"
        "<p>Look at the digit <b>one place to the right</b> of the place you are rounding to. "
        "<b>5 or more</b>: round up. <b>4 or less</b>: round down. Exactly halfway rounds up.</p>"
        + table(["Round to the nearest", "Look at the", "Example"], [
            ["ten", "ones digit", "2875 → 2880"],
            ["hundred", "tens digit", "4519 → 4500"],
            ["thousand", "hundreds digit", "7391 → 7000"],
            ["whole number", "tenths digit", "6.8 → 7"],
        ]) +
        ex("Exactly halfway", "Round 4500 to the nearest thousand.",
           "4500 is exactly halfway between 4000 and 5000. The hundreds digit is 5, and 5 rounds up.", "5000")
        + ex("A 9 that rounds up", "Round 9615 to the nearest thousand.",
             "The hundreds digit is 6, so round up. 9 thousands and 1 more thousand make 10 thousands.",
             nf(10000))
        + "<h2>Round tenths to the nearest whole number</h2>"
        "<p>A decimal like 3.5 is between two whole numbers, 3 and 4. Look at the <b>tenths digit</b>.</p>"
        "<figure class='sn-fig'>" + number_line_svg(30, 40, 35, 1, dec) +
        "<figcaption>3.5 is exactly halfway between 3 and 4. The tenths digit is 5, so 3.5 rounds up to 4."
        "</figcaption></figure>"
        + ex("Round a decimal", "A pumpkin has a mass of 4.6 kg. What is its mass to the nearest kilogram?",
             "The tenths digit is 6. 6 is 5 or more, so round up.", "5 kg")
        + "<h2>Estimate, then check</h2>"
        "<p>An estimate is a quick answer that is close to the exact answer. Round the numbers, "
        "then add or subtract in your head. If your exact answer is far from the estimate, check your work.</p>"
        + ex("Estimate a sum", "Estimate 4682 + 2371 to the nearest thousand.",
             "5000 + 2000 = 7000. The exact answer is 7053, which is close.", "about 7000")
        + ex("Is the answer reasonable?", "Arjun says 5203 " + MINUS + " 1867 = 4664.",
             "Estimate: 5200 " + MINUS + " 1900 = 3300. 4664 is far from 3300, so it is not reasonable. "
             "The exact answer is 3336.", "not reasonable")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Rounding 4500 down to 4000", "Exactly halfway rounds up: 5000"],
            ["Rounding the wrong place: 6382 to the nearest thousand → 6400",
             "For the nearest thousand, look at the hundreds digit: 3, so 6000"],
            ["Rounding in steps: 3462 → 3500 → 4000", "Look only at the hundreds digit: 4, so 3000"],
            ["Dropping the decimal: 3.8 → 3", "The tenths digit is 8 (5 or more), so 3.8 rounds to 4"],
            ["Not checking: 3467 + 258 = 6047", "Estimate 3500 + 300 = 3800; 6047 is far too big. The answer is 3725"],
        ])
    )


FAQ = [
    {"q": "What does Grade 4 learn about rounding in the Ontario math curriculum?",
     "a": "Grade 4 students round whole numbers to the nearest ten, hundred or thousand in real situations (B1.3). "
          "They also round decimal tenths to the nearest whole number, such as 3.5 to 4 (B1.8)."},
    {"q": "Does 4500 round to 4000 or 5000?",
     "a": "To the nearest thousand, 4500 rounds to 5000. A number exactly halfway between two thousands is rounded up."},
    {"q": "How do you round a decimal to the nearest whole number?",
     "a": "Look at the tenths digit. If it is 5 or more, round up; if it is 4 or less, keep the whole number. "
          "So 6.8 rounds to 7 and 7.4 rounds to 7."},
    {"q": "How can my child check if an answer is reasonable?",
     "a": "Estimate first by rounding, then compare. If 3467 + 258 gives 6047 but 3500 + 300 = 3800, the answer is "
          "far too big and should be checked."},
]


def gen():
    rnd = random.Random(44803)
    sets = [set_round_10_100(), set_round_1000(), set_round_tenths(), set_sums(), set_words()]
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
            assert it["q"].count("<svg") <= 1
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "rounding-and-estimating", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Rounding and Estimating",
        "seo_title": "Grade 4 Rounding and Estimating Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Rounding and Estimating",
        "domain": "Number",
        "standard_code": "Grade 4: B1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Round whole numbers to the nearest ten, hundred, or thousand, in various contexts",
        "meta_desc": "Free Grade 4 math worksheets on rounding and estimating, aligned to the Ontario curriculum "
                     "(B1.3, B1.8): round to the nearest ten, hundred and thousand, round tenths to the nearest "
                     "whole number, estimate sums and differences, check if answers are reasonable and solve word "
                     "problems. 100 questions with an answer key.",
        "key_big": "Look one place to the right: 5 or more rounds up, 4 or less rounds down. "
                   "4500 rounds to 5000 and 3.5 rounds to 4.",
        "key_sub": "Estimate before you calculate: 4682 + 2371 is about 5000 + 2000 = 7000. If your answer is far "
                   "from the estimate, check your work.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|cards: [^,']*,)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
