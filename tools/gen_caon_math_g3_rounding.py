# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 3 Math: Rounding and Estimating
(Ontario Mathematics Curriculum 2020, Grade 3: B1.3, with B2.3 mental math and estimation)
  python3 tools/gen_ca_math_g3_rounding.py
Whole numbers to 1000. Round half up (450 -> 500). Every answer is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#6b6259"
CARD = "#eef5f0"
CARDEDGE = "#7aa58a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
MINUS = "−"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ numbers
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


def dol(n):
    return "$" + nf(n)


def km(n):
    return nf(n) + " km"


def metres(n):
    return nf(n) + " m"


def val(s):
    """Value of a number text, or None for words."""
    s = re.sub(r"<[^>]+>", "", s).replace(NB, "")
    m = re.match(r"^\$(\d+)$", s)
    if m:
        return ("$", int(m.group(1)))
    m = re.match(r"^(\d+)( km| m)?$", s)
    if m:
        return ("n" + (m.group(2) or ""), int(m.group(1)))
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
def number_line_svg(lo, hi, n, step):
    """Number line from lo to hi, ticks every step, labels at both ends and halfway, red dot on n."""
    L, R, Y = 40, 400, 52
    W, H = 440, 92
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
            s.append(text(X(v), Y + 32, nf(v), 15, col=GREEN if v != mid else GREY))
        v += step
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(n), Y, RED))
    s.append(text(X(n), Y - 18, nf(n), 16, col=RED, wt=800))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (nf(lo), nf(hi)))


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


# ============================================================ set 1: round to the nearest 10 and 100
WORD = {10: "ten", 100: "hundred"}
LOOK = {10: "ones", 100: "tens"}


def digit(n, i):
    return (n // 10 ** i) % 10


def round_expl(n, p, unit=""):
    lo = n // p * p
    r = rnd_to(n, p)
    d = digit(n, 0 if p == 10 else 1)
    if n % p == p // 2:
        s = ("%s is exactly halfway between %s and %s. The %s digit is 5, and 5 rounds up."
             % (nf(n), nf(lo), nf(lo + p), LOOK[p]))
    else:
        s = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s."
             % (nf(n), nf(lo), nf(lo + p), LOOK[p], d,
                "%d is 5 or more" % d if d >= 5 else "%d is 4 or less" % d, "up" if r > lo else "down"))
    if r == 1000 and p == 100:
        s += " 9 hundreds and 1 more hundred make 10 hundreds, which is 1000."
    elif p == 10 and r > lo and digit(n, 1) == 9:  # 397 -> 400, 996 -> 1000
        s += " %d tens and 1 more ten make %d tens, which is %s." % (n // 10, r // 10, nf(r))
    if p == 100 and rnd_to(rnd_to(n, 10), 100) != r:
        s += " Do not round in two steps (%s → %s → %s). Look only at the tens digit." % (
            nf(n), nf(rnd_to(n, 10)), nf(rnd_to(rnd_to(n, 10), 100)))
    return s + " Answer: <b>%s%s</b>." % (nf(r), unit)


def round_cands(n, p):
    """Wrong answers from real mistakes, most likely first."""
    r = rnd_to(n, p)
    lo = n // p * p
    out = []
    if p == 100:
        out.append(rnd_to(rnd_to(n, 10), 100))   # rounded in two steps (449 -> 450 -> 500)
    out.append(lo + p if r == lo else lo)        # rounded the wrong way / always rounding down (450 -> 400)
    if p == 10:
        out.append(n)                            # did not round at all
        out.append(rnd_to(n, 100))               # rounded to the hundred (wrong digit)
    else:
        out.append(rnd_to(n, 10))                # rounded to the nearest ten (looked at the ones digit)
        out.append(n // 10 * 10)                 # cut off the ones only
    out += [r + p, r - p]
    return [x for x in out if x != r]


def q_round(n, p, line=True, q=None, fmt=nf, unit=""):
    lo = n // p * p
    q = q or "Round %s to the nearest %s." % (nf(n), WORD[p])
    if line:
        q = fig(number_line_svg(lo, lo + p, n, p // 10)) + q
    return mq_n(q, rnd_to(n, p), round_cands(n, p), round_expl(n, p, unit), fmt)


def q_which_rounds(target, p, right, wrongs):
    assert rnd_to(right, p) == target
    for w in wrongs:
        assert rnd_to(w, p) != target
    lst = "; ".join("%s → %s" % (nf(x), nf(rnd_to(x, p))) for x in [right] + wrongs)
    e = "Round each number to the nearest %s: %s. Only <b>%s</b> rounds to %s." % (WORD[p], lst, nf(right), nf(target))
    return mq_n("Which number rounds to %s when you round to the nearest %s?" % (nf(target), WORD[p]),
                right, wrongs, e)


def set_round():
    its = []
    for n, line in [(47, True), (83, True), (62, True), (25, True), (38, False)]:
        its.append(q_round(n, 10, line))
    its.append(q_which_rounds(80, 10, 77, [72, 85, 69]))
    for n, line in [(365, True), (728, False), (594, True), (805, True), (397, True)]:
        its.append(q_round(n, 10, line))
    for n, line in [(340, True), (682, True), (450, True), (251, True), (719, False), (849, True), (150, False),
                    (960, True)]:
        its.append(q_round(n, 100, line))
    its.append(q_which_rounds(500, 100, 462, [438, 551, 550]))
    return {"title": "Round to the nearest ten and hundred", "items": its}


# ============================================================ set 2: round in real life
def q_could_be(ask, target, p, right, wrongs, why):
    assert rnd_to(right, p) == target
    for w in wrongs:
        assert rnd_to(w, p) != target, w
    lst = "; ".join("%s → %s" % (nf(x), nf(rnd_to(x, p))) for x in [right] + wrongs)
    e = "Round each number to the nearest %s: %s. Only <b>%s</b> rounds to %s.%s" % (
        WORD[p], lst, nf(right), nf(target), why)
    return mq_n(ask, right, wrongs, e)


def set_context():
    its = []
    its.append(q_round(47, 10, False, fig(cards_svg([("books read", "47")])) +
                       "Grade 3 students read 47 books in March. To the nearest ten, about how many books is that?"))
    its.append(q_round(92, 10, True, "A farmer counts 92 Canada geese on a pond. "
                       "About how many geese is that, to the nearest ten?"))
    its.append(q_round(75, 10, True, "There are 75 maple candies in a jar. "
                       "To the nearest ten, about how many candies are there?"))
    its.append(q_round(165, 10, True, "The skating rink has 165 pairs of skates to rent. "
                       "To the nearest ten, about how many pairs is that?"))
    its.append(q_round(238, 10, True, "Hana’s family drives 238 km to the cottage. "
                       "How far is that to the nearest ten kilometres?", km, " km"))
    its.append(q_round(386, 100, True, "386 people come to the school winter concert. "
                       "To the nearest hundred, about how many people is that?"))
    its.append(q_round(918, 100, False, fig(cards_svg([("library books", "918")])) +
                       "The school library has 918 books. To the nearest hundred, about how many books is that?"))
    its.append(q_round(735, 100, False, fig(cards_svg([("money raised", "$735")])) +
                       "The class raised $735 at the Terry Fox Run. To the nearest hundred dollars, "
                       "about how much is that?", dol, ""))
    its[-1]["e"] = its[-1]["e"].replace("735 is between 700 and 800", "$735 is between $700 and $800").replace("<b>700</b>", "<b>$700</b>")
    its.append(q_round(553, 100, True, "The CN Tower in Toronto is 553 m tall. "
                       "How tall is it to the nearest hundred metres?", metres, " m"))
    its.append(q_round(850, 100, True, "The hockey arena has 850 seats. "
                       "To the nearest hundred, about how many seats is that?"))
    its.append(q_round(455, 100, True, "A farm sells 455 pumpkins before Thanksgiving. "
                       "To the nearest hundred, about how many pumpkins is that?"))
    its.append(q_round(604, 10, False, fig(cards_svg([("bags sold", "604")])) +
                       "A popcorn stand sells 604 bags at the fall fair. To the nearest ten, about how many bags is that?"))
    its.append(q_round(996, 10, False, fig(cards_svg([("cans", "996")])) +
                       "The school collects 996 cans for the food drive. Round 996 to the nearest ten."))
    its.append(q_could_be("About 70 students go on the field trip. The number was rounded to the nearest ten. "
                          "Which could be the real number of students?", 70, 10, 74, [75, 64, 79],
                          " 75 is exactly halfway, so it rounds up to 80."))
    its.append(q_could_be("About 300 people came to the Canada Day picnic. The number was rounded to the nearest "
                          "hundred. Which could be the real number?", 300, 100, 284, [350, 249, 391],
                          " 350 is exactly halfway, so it rounds up to 400."))
    its.append(mq_n("What is the smallest whole number that rounds to 60 when you round to the nearest ten?",
                    55, [54, 50, 56],
                    "The numbers that round to 60 are 55, 56, 57, 58, 59, 60, 61, 62, 63 and 64. "
                    "54 rounds down to 50. The smallest is <b>55</b>, because a 5 in the ones place rounds up."))
    its.append(mq_n("What is the largest whole number that rounds to 400 when you round to the nearest hundred?",
                    449, [450, 499, 440],
                    "Numbers from 350 to 449 round to 400. 450 is exactly halfway, so it rounds up to 500. "
                    "440 rounds to 400, but 449 is larger. The largest is <b>449</b>."))
    for x in range(350, 450):
        assert rnd_to(x, 100) == 400
    assert rnd_to(450, 100) == 500 and rnd_to(349, 100) == 300 and rnd_to(55, 10) == 60 and rnd_to(54, 10) == 50
    name, she, her = ("Mei", "she", "her")
    its.append(mcq("Mei says 450 rounds to 400 when you round to the nearest hundred. Is she right?",
                   "No, it rounds to 500",
                   ["Yes, because 4 is less than 5", "Yes, because it rounds down", "No, it rounds to 450"],
                   "450 is exactly halfway between 400 and 500. The tens digit is 5, and 5 rounds up. "
                   "Mei is not right: 450 rounds to <b>500</b>."))
    assert rnd_to(682, 100) == 700
    its.append(mq_n("Owen rounds 682 to the nearest hundred and gets 600. What should he get?",
                    700, [600, 680, 690],
                    "Owen always rounded down. Look at the tens digit: 8. 8 is 5 or more, so round up. "
                    "682 rounds to <b>700</b>."))
    assert rnd_to(349, 100) == 300 and rnd_to(rnd_to(349, 10), 100) == 400
    its.append(mq_n("Zoe rounds 349 to the nearest hundred. She says “349 → 350 → 400.” What is the right answer?",
                    300, [400, 350, 500],
                    "Do not round in two steps. To round to the nearest hundred, look only at the tens digit: 4. "
                    "4 is 4 or less, so round down. 349 rounds to <b>300</b>."))
    return {"title": "Round in real life: about how many?", "items": its}


# ============================================================ set 3: estimate sums and differences
def expr(xs):
    out = nf(xs[0][0])
    for v, sg in xs[1:]:
        out += opf(sg) + nf(v)
    return out


def est_core(terms, p):
    rs = [(rnd_to(n, p), sg) for n, sg in terms]
    exact = sum(n * sg for n, sg in terms)
    est = sum(r * sg for r, sg in rs)
    down = sum(n // p * p * sg for n, sg in terms)
    assert est != exact and est > 0 and exact > 0
    return rs, exact, est, down


def est_cands(terms, p, rs, exact, est, down):
    out = [down, exact]
    if any(sg < 0 for _, sg in terms):
        out.append(sum(r for r, _ in rs))                       # added instead of subtracting
    if p == 100:
        out.append(sum(rnd_to(n, 10) * sg for n, sg in terms))   # rounded to the nearest ten instead
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
        ([(38, A), (47, A)], 10), ([(64, A), (23, A)], 10), ([(72, A), (29, S)], 10), ([(91, A), (46, S)], 10),
        ([(56, A), (35, A)], 10), ([(83, A), (38, S)], 10), ([(28, A), (43, A), (17, A)], 10),
        ([(274, A), (138, A)], 10), ([(352, A), (126, S)], 10),
        ([(347, A), (486, A)], 100), ([(629, A), (254, A)], 100), ([(812, A), (385, S)], 100),
        ([(563, A), (178, A)], 100), ([(935, A), (468, S)], 100), ([(298, A), (405, A)], 100),
        ([(718, A), (450, S)], 100), ([(904, A), (296, S)], 100), ([(641, A), (239, S)], 100),
        ([(156, A), (249, A), (372, A)], 100), ([(487, A), (163, A), (215, A)], 100),
    ]:
        its.append(est_terms(terms, p))
    return {"title": "Estimate sums and differences", "items": its}


# ============================================================ set 4: is the answer reasonable?
def far(x, est):
    return abs(x - est) / est


def best_sentence(a, b, op, wrongs):
    best = "%s%s%s" % (nf(rnd_to(a, 100)), opf(op), nf(rnd_to(b, 100)))
    e = ("Round each number to the nearest hundred: %s → %s and %s → %s. The best estimate is <b>%s</b>."
         % (nf(a), nf(rnd_to(a, 100)), nf(b), nf(rnd_to(b, 100)), best))
    return mcq("Which is the best way to estimate %s%s%s by rounding to the nearest hundred?" % (nf(a), opf(op), nf(b)),
               best, wrongs, e)


def best_est(a, b, op, cands):
    exact = a + op * b
    best = min(cands, key=lambda x: abs(x - exact))
    for x in cands:
        if x != best:
            assert abs(x - exact) > abs(best - exact)
    assert best == rnd_to(a, 100) + op * rnd_to(b, 100)
    e = ("Round to the nearest hundred: %s%s%s = <b>%s</b>. The exact answer is %s, so %s is the closest."
         % (nf(rnd_to(a, 100)), opf(op), nf(rnd_to(b, 100)), nf(best), nf(exact), nf(best)))
    return mq_n("Which is the best estimate for %s%s%s?" % (nf(a), opf(op), nf(b)), best,
                [x for x in cands if x != best], e)


def more_less(person, a, b):
    name = person[0]
    ra, rb = rnd_to(a, 10), rnd_to(b, 10)
    up = ra > a and rb > b
    assert up or (ra < a and rb < b)
    est, exact = ra + rb, a + b
    wd = "up" if up else "down"
    other = "down" if up else "up"
    right = "%s, both numbers were rounded %s" % ("Less" if up else "More", wd)
    cands = ["%s, both numbers were rounded %s" % ("More" if up else "Less", wd),
             "%s, both numbers were rounded %s" % ("Less" if up else "More", other),
             "%s, both numbers were rounded %s" % ("More" if up else "Less", other)]
    e = ("%d → %d and %d → %d. Both numbers were rounded %s, so the estimate %d is too %s. "
         "The exact sum is %d, which is <b>%s</b> than %d."
         % (a, ra, b, rb, wd, est, "big" if up else "small", exact, "less" if up else "more", est))
    q = "%s estimates %d + %d as %d + %d = %d. Is the exact sum more or less than %d?" % (
        name, a, b, ra, rb, est, est)
    return mcq(q, right, cands, e)


def yes_no(person, a, b, op, said, p, slip=""):
    name = person[0]
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


def set_reasonable(P):
    A, S = 1, -1
    its = []
    its.append(best_sentence(497, 312, A, ["400 + 300", "500 + 400", "490 + 310"]))
    its.append(best_sentence(782, 359, S, ["700 " + MINUS + " 300", "800 " + MINUS + " 300", "780 " + MINUS + " 360"]))
    its.append(best_est(386, 247, A, [600, 500, 700, 800]))
    its.append(best_est(689, 214, A, [900, 800, 1000, 700]))
    its.append(best_est(823, 291, S, [500, 600, 400, 700]))
    its.append(best_est(574, 318, S, [300, 200, 400, 100]))
    its.append(more_less(P.next(), 38, 47))
    its.append(more_less(P.next(), 62, 21))
    its.append(more_less(P.next(), 127, 346))
    its.append(more_less(P.next(), 243, 512))
    its.append(yes_no(P.next(), 298, 415, A, 713, 100))
    its.append(yes_no(P.next(), 91, 46, S, 45, 10))
    its.append(yes_no(P.next(), 59, 87, A, 1316, 10,
                      " (9 + 7 = 16 and 5 + 8 = 13 were written side by side. Regroup 16 as 1 ten and 6 ones.)"))
    its.append(yes_no(P.next(), 467, 28, A, 747, 10,
                      " (28 was lined up under the wrong places, as if it were 280. Line up ones with ones.)"))
    its.append(yes_no(P.next(), 723, 196, S, 527, 100))
    its.append(yes_no(P.next(), 604, 278, S, 474, 100,
                      " (The smaller digit was taken away from the bigger digit in each column. "
                      "Regroup instead: you cannot take 8 from 4.)"))
    its.append(reasonable_pick(356, 27, A, 10, [626, 3713, 83],
                               "626 lines up 27 as 270, 3713 writes 6 + 7 = 13 without regrouping, "
                               "and 83 forgets the hundreds."))
    its.append(reasonable_pick(728, 46, A, 10, [1188, 7614, 74],
                               "1188 lines up 46 as 460, 7614 writes 8 + 6 = 14 without regrouping, "
                               "and 74 forgets the hundreds."))
    its.append(reasonable_pick(812, 385, S, 100, [1197, 573, 27],
                               "1197 adds instead of subtracting, 573 takes the smaller digit from the bigger one "
                               "in each column, and 27 forgets the hundreds."))
    its.append(reasonable_pick(930, 487, S, 100, [1417, 557, 43],
                               "1417 adds instead of subtracting, 557 takes the smaller digit from the bigger one "
                               "in each column, and 43 forgets the hundreds."))
    assert 356 + 270 == 626 and 728 + 460 == 1188 and 812 + 385 == 1197 and 930 + 487 == 1417
    return {"title": "Is the answer reasonable?", "items": its}


# ============================================================ set 5: word problems
def word_est(q, terms, p, fmt=nf, pic=None, unit=""):
    rs, exact, est, down = est_core(terms, p)
    e = ("Round to the nearest %s: %s = <b>%s</b>. (The exact answer is %s.)"
         % (WORD[p], "".join((fmt(r) if i == 0 else opf(sg) + fmt(r)) for i, (r, sg) in enumerate(rs)),
            fmt(est), fmt(exact)))
    if pic:
        q = fig(cards_svg(pic)) + q
    return mq_n(q, est, est_cands(terms, p, rs, exact, est, down), e, fmt)


def enough(q, terms, p, limit, noun, pic=None, fmt=None):
    g = dol if fmt is dol else nf
    fmt = fmt or (lambda x: nf(x) + " " + noun)
    rs, exact, est, down = est_core(terms, p)
    ok = est <= limit
    assert ok == (exact <= limit) and est != limit and down != est
    yes, no = "Yes, about %s", "No, about %s"
    right = (yes if ok else no) % fmt(est)
    cands = [(no if ok else yes) % fmt(est), (yes if down <= limit else no) % fmt(down),
             (no if down <= limit else yes) % fmt(down)]
    e = "Round to the nearest %s: %s = %s. %s is %s %s, so <b>%s</b>. (The exact answer is %s.)" % (
        WORD[p], "".join((g(r) if i == 0 else opf(sg) + g(r)) for i, (r, sg) in enumerate(rs)), g(est), g(est),
        "less than" if ok else "more than", g(limit), "yes" if ok else "no", g(exact))
    if pic:
        q = fig(cards_svg(pic)) + q
    return mcq(q, right, cands, e)


def set_words(P):
    A, S = 1, -1
    its = []
    its.append(word_est("Mateo’s family canoes 38 km on Saturday and 27 km on Sunday. "
                        "About how far do they canoe in all? Round to the nearest ten.",
                        [(38, A), (27, A)], 10, km))
    its.append(word_est("A sugar shack sells 178 bottles of maple syrup on Saturday and 226 bottles on Sunday. "
                        "About how many bottles does it sell? Round to the nearest ten.",
                        [(178, A), (226, A)], 10, pic=[("Saturday", "178"), ("Sunday", "226")]))
    n1 = P.next()
    its.append(word_est("%s’s book has 312 pages. %s has read 146 pages. About how many pages are left? "
                        "Round to the nearest ten." % (n1[0], cap(n1[1])), [(312, A), (146, S)], 10))
    its.append(word_est("At the hockey game there are 386 adults and 247 children. "
                        "About how many people are there? Round to the nearest hundred.",
                        [(386, A), (247, A)], 100, pic=[("adults", "386"), ("children", "247")]))
    its.append(word_est("The school has 612 students. On a snow day, 187 students stay home. "
                        "About how many students come to school? Round to the nearest hundred.",
                        [(612, A), (187, S)], 100))
    its.append(word_est("At the Terry Fox Run, Grade 3 raises $468 and Grade 4 raises $325. "
                        "About how much do they raise in all? Round to the nearest hundred.",
                        [(468, A), (325, A)], 100, dol, pic=[("Grade 3", "$468"), ("Grade 4", "$325")]))
    its.append(word_est("The CN Tower is 553 m tall. An office tower in Toronto is 287 m tall. "
                        "About how much taller is the CN Tower? Round to the nearest hundred.",
                        [(553, A), (287, S)], 100, metres))
    its.append(word_est("A bike costs $289 and a helmet costs $48. About how much do they cost in all? "
                        "Round to the nearest ten.", [(289, A), (48, A)], 10, dol,
                        pic=[("bike", "$289"), ("helmet", "$48")]))
    its.append(word_est("The arena sells 735 tickets on Friday and 468 tickets on Saturday. "
                        "About how many more tickets are sold on Friday? Round to the nearest ten.",
                        [(735, A), (468, S)], 10, pic=[("Friday", "735"), ("Saturday", "468")]))
    its.append(word_est("A class collects 124 cans in week 1, 98 cans in week 2 and 153 cans in week 3. "
                        "About how many cans is that? Round to the nearest ten.",
                        [(124, A), (98, A), (153, A)], 10,
                        pic=[("week 1", "124"), ("week 2", "98"), ("week 3", "153")]))
    its.append(enough("The gym has 500 chairs. 238 parents and 196 students come to the spring concert. "
                      "Are there enough chairs? Round to the nearest hundred to decide.",
                      [(238, A), (196, A)], 100, 500, "people"))
    its.append(enough("A ferry can carry 400 people. 268 adults and 179 children want to get on. "
                      "Can they all get on? Round to the nearest hundred to decide.",
                      [(268, A), (179, A)], 100, 400, "people"))
    n2 = P.next()
    its.append(enough("%s has $500. %s wants a tablet for $279 and a case for $135. Is $500 enough? "
                      "Round to the nearest hundred to decide." % (n2[0], cap(n2[1])),
                      [(279, A), (135, A)], 100, 500, "", pic=[("tablet", "$279"), ("case", "$135")], fmt=dol))
    its.append(enough("A school bus can drive 900 km before it needs fuel. The trip is 365 km there and "
                      "365 km back. Can the bus do the trip without more fuel? Round to the nearest hundred to decide.",
                      [(365, A), (365, A)], 100, 900, "km"))
    n3 = P.next()
    assert 702 - 389 == 313
    its.append(mcq("%s works out how many more pumpkins the farm sold: 702 %s 389. %s gets 487. "
                   "Is this reasonable?" % (n3[0], MINUS, cap(n3[1])),
                   "No, it should be about 300",
                   ["Yes, it is close to 500", "No, it should be about 1100", "Yes, it is close to 400"],
                   "Round to the nearest hundred: 700 " + MINUS + " 400 = 300. 487 is far from 300, so it is "
                   "<b>not reasonable</b>. The exact answer is 313. (The smaller digit was taken away from the "
                   "bigger digit in each column.)"))
    n4 = P.next()
    assert 345 + 278 == 623
    its.append(mcq("%s adds the cans two classes collected: 345 + 278. %s gets 623. "
                   "Is this reasonable?" % (n4[0], cap(n4[1])),
                   "Yes, it is close to 600",
                   ["No, it should be about 500", "Yes, it is close to 500", "No, it should be about 700"],
                   "Round to the nearest hundred: 300 + 300 = 600. 623 is close to 600, so it is <b>reasonable</b>. "
                   "(Rounding 278 down to 200 gives 500, which is too low. Rounding 345 up to 400 gives 700, which is too high.)"))
    # estimate is more or less than exact, in context
    assert 289 + 196 == 485 and rnd_to(289, 100) + rnd_to(196, 100) == 500
    its.append(mcq("Ava needs 289 beads for a necklace and 196 beads for a bracelet. She estimates "
                   "300 + 200 = 500 beads. Will she need more or less than 500 beads?",
                   "Less, both numbers were rounded up",
                   ["More, both numbers were rounded up", "Less, both numbers were rounded down",
                    "More, both numbers were rounded down"],
                   "289 → 300 and 196 → 200. Both numbers were rounded up, so 500 is too big. "
                   "She needs 485 beads, which is <b>less</b> than 500."))
    assert 412 + 331 == 743 and rnd_to(412, 100) + rnd_to(331, 100) == 700
    its.append(mcq("Leah’s class wants to read 700 pages in October. Leah reads 412 pages and her friends read "
                   "331 pages. Leah estimates 400 + 300 = 700. Did they read more or less than 700 pages?",
                   "More, both numbers were rounded down",
                   ["Less, both numbers were rounded down", "More, both numbers were rounded up",
                    "Less, both numbers were rounded up"],
                   "412 → 400 and 331 → 300. Both numbers were rounded down, so 700 is too small. "
                   "They read 743 pages, which is <b>more</b> than 700."))
    # about how many, then compare
    its.append(word_est("The Terry Fox Run goal is 900 laps. Students run 386 laps in the morning. "
                        "About how many more laps do they need? Round to the nearest hundred.",
                        [(900, A), (386, S)], 100))
    its.append(word_est("A canoe trip is 96 km long. Kai’s group paddles 28 km on day 1 and 34 km on day 2. "
                        "About how many kilometres are left? Round to the nearest ten.",
                        [(96, A), (28, S), (34, S)], 10, km))
    return {"title": "Word problems: estimate and check", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Rounding: find the closer ten or hundred</h2>"
        "<p>Rounding finds the <b>closest</b> ten or hundred. Rounded numbers are easy to add and subtract "
        "in your head.</p>"
        "<figure class='sn-fig'>" + number_line_svg(40, 50, 47, 1) +
        "<figcaption>47 is closer to 50 than to 40, so 47 rounds to 50.</figcaption></figure>"
        "<h2>The 5 rule</h2>"
        "<p>Look at the digit <b>one place to the right</b> of the place you are rounding to. "
        "<b>5 or more</b>: round up. <b>4 or less</b>: round down.</p>"
        + table(["Round to the nearest", "Look at the", "Example"], [
            ["ten", "ones digit", "365 → 370"],
            ["hundred", "tens digit", "682 → 700"],
        ]) +
        "<figure class='sn-fig'>" + number_line_svg(300, 400, 386, 10) +
        "<figcaption>386 is past the halfway point, 350, so to the nearest hundred it rounds up to 400.</figcaption></figure>"
        + ex("Exactly halfway", "Round 450 to the nearest hundred.",
             "450 is exactly halfway between 400 and 500. The tens digit is 5, and 5 rounds up.", "500")
        + ex("A 9 that rounds up", "Round 960 to the nearest hundred.",
             "The tens digit is 6, so round up. 9 hundreds and 1 more hundred make 10 hundreds.", "1000")
        + "<h2>Estimate, then check</h2>"
        "<p>An estimate is a quick answer that is close to the exact answer. Round the numbers, "
        "then add or subtract in your head. If your exact answer is far from the estimate, check your work.</p>"
        + ex("Estimate a sum", "About how many people? 386 adults and 247 children.",
             "Round to the nearest hundred: 400 + 200 = 600. The exact answer is 633, which is close.", "about 600")
        + ex("Estimate a difference", "Estimate 812 " + MINUS + " 385.",
             "Round to the nearest hundred: 800 " + MINUS + " 400 = 400. The exact answer is 427.", "about 400")
        + ex("Is the answer reasonable?", "Arjun says 604 " + MINUS + " 278 = 474.",
             "Estimate: 600 " + MINUS + " 300 = 300. 474 is far from 300, so it is not reasonable. "
             "The exact answer is 326.", "not reasonable")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Rounding 450 down to 400", "Exactly halfway rounds up: 500"],
            ["Looking at the wrong digit: 349 to the nearest hundred → 350",
             "For the nearest hundred, look at the tens digit: 4, so 300"],
            ["Always rounding down: 682 → 600", "The tens digit is 8 (5 or more), so round up: 700"],
            ["Rounding in two steps: 349 → 350 → 400", "Look only at the tens digit: 4, so 300"],
            ["Not checking: 59 + 87 = 1316", "Estimate 60 + 90 = 150; 1316 is far too big. The answer is 146"],
        ])
    )


FAQ = [
    {"q": "What does Grade 3 learn about rounding in the Ontario math curriculum?",
     "a": "Grade 3 students round whole numbers to the nearest ten or hundred in real situations (B1.3). "
          "They also use mental math and estimation to add and subtract numbers up to 1000 (B2.3)."},
    {"q": "Does 450 round to 400 or 500?",
     "a": "To the nearest hundred, 450 rounds to 500. A number exactly halfway between two hundreds is rounded up."},
    {"q": "What is the difference between rounding and estimating?",
     "a": "Rounding changes one number to the closest ten or hundred. Estimating uses rounded numbers to get a quick "
          "answer, such as 386 + 247 is about 400 + 200 = 600."},
    {"q": "How can my child check if an answer is reasonable?",
     "a": "Estimate first by rounding, then compare. If 59 + 87 gives 1316 but 60 + 90 = 150, the answer is far too "
          "big and should be checked. This habit helps on the Grade 3 EQAO math assessment too."},
]


def gen():
    rnd = random.Random(33806)
    P = People(rnd)
    sets = [set_round(), set_context(), set_sums(), set_reasonable(P), set_words(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "rounding-and-estimating", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 3 Rounding and Estimating",
        "seo_title": "Grade 3 Rounding and Estimating Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Rounding and Estimating",
        "domain": "Number",
        "standard_code": "Grade 3: B1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Round whole numbers to the nearest ten or hundred, in various contexts",
        "meta_desc": "Free Grade 3 math worksheets on rounding and estimating, aligned to the Ontario curriculum (B1.3, B2.3): "
                     "round to the nearest ten and hundred on number lines, use the 5 rule, estimate sums and "
                     "differences, check if answers are reasonable and solve word problems. 100 questions with an "
                     "answer key. Great EQAO practice.",
        "key_big": "Look one place to the right: 5 or more rounds up, 4 or less rounds down. 450 rounds to 500.",
        "key_sub": "Estimate before you calculate: 386 + 247 is about 400 + 200 = 600. If your answer is far from "
                    "the estimate, check your work.",
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
