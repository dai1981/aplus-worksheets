# -*- coding: utf-8 -*-
"""
UK Year 4 Maths (National Curriculum in England): Rounding to the nearest 10, 100 and 1,000
  python3 tools/gen_uk_maths_y4_rounding.py
HTML attributes use single quotes (no backslashes in the JSON).
Numbers of 1,000 or more are always written with commas.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

PLACE = {10: "10", 100: "100", 1000: "1,000"}
LOOK = {10: "ones", 100: "tens", 1000: "hundreds"}          # digit to look at
OWN = {10: "tens", 100: "hundreds", 1000: "thousands"}      # digit that is rounded
NEXT1 = {10: "hundred", 100: "thousand", 1000: "ten thousand"}


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


def mcq_n(q, correct, cands, e, rnd, fmt=c):
    """Number choices. Wrong numbers that are 0 or less, or equal to the answer, are dropped."""
    return mcq(q, fmt(correct), [fmt(v) for v in cands if v is not None and v > 0 and v != correct], e, rnd)


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


def digit(n, i):
    return (n // 10 ** i) % 10


def lg(p):
    return len(str(p)) - 1


# ------------------------------------------------------------ figure
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


def line_for(n, p):
    lo = n // p * p
    return fig(number_line_svg(lo, lo + p, n, p // 10))


# ------------------------------------------------------------ rounding
def round_to(n, p):
    return ((n + p // 2) // p) * p


def round_expl(n, p):
    """Short explanation of rounding n to the nearest p (10, 100 or 1,000)."""
    lo = n // p * p
    r = round_to(n, p)
    d = digit(n, lg(p) - 1)
    if n - lo == p // 2:
        s = ("%s is exactly halfway between %s and %s. A number that is exactly halfway rounds up."
             % (c(n), c(lo), c(lo + p)))
    else:
        s = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s."
             % (c(n), c(lo), c(lo + p), LOOK[p], d,
                "5 or more" if d >= 5 else "4 or less", "up" if r > lo else "down"))
    if r > lo and digit(n, lg(p)) == 9:
        s += (" The %s digit is 9, so rounding up makes 10 %s. Exchange them for 1 %s: %s + %s = %s."
              % (OWN[p], OWN[p], NEXT1[p], c(lo), c(p), c(r)))
    return s + " Answer: %s." % c(r)


def nine_mistakes(n, p):
    """When a 9 rounds up: writing “10” in one place (2,965 -> 21,000) or forgetting to exchange (2,965 -> 2,000)."""
    r = round_to(n, p)
    lo = n // p * p
    if r == lo or digit(n, lg(p)) != 9:
        return []
    pre = n // (p * 10)
    out = [pre * p * 10]                                      # 9 became 0, nothing carried
    if pre:
        out.insert(0, int(str(pre) + "10" + "0" * lg(p)))     # “10” written in the 9's place
    return out


def round_cands(n, p):
    """Wrong answers from real mistakes, most likely first."""
    r = round_to(n, p)
    lo = n // p * p
    other = lo + p if r == lo else lo                         # rounded the wrong way (450 -> 400)
    out = [other] + nine_mistakes(n, p)
    if r > lo:
        out.append(r + n % p)                                 # kept the digits after the place (3,462 -> 3,562)
    if p >= 100:
        out.append(round_to(n, p // 10))                      # rounded to the place on the right (3,460)
        out.append(n // (p // 10) * (p // 10))                # cut off at the wrong place (3,400)
    out.append(n // (p * 10) * (p * 10))                      # changed the wrong digit (3,000)
    out.append(round_to(n, p * 10))
    out += [r + p, r - p, n]
    return out


# ============================================================ number pickers
class Picker:
    def __init__(self, rnd):
        self.rnd = rnd
        self.used = set()

    def take(self, n):
        assert n not in self.used, n
        self.used.add(n)
        return n

    def pick(self, lo, hi, p, ok=lambda n: True):
        """A number in [lo, hi] that is not a multiple of p and not used before."""
        while True:
            n = self.rnd.randint(lo, hi)
            if n % p and n % 10 and n not in self.used and ok(n) and round_to(n, p) > 0:
                self.used.add(n)
                return n


def q_round(n, p, rnd, line=False):
    q = "Round %s to the nearest %s." % (c(n), PLACE[p])
    if line:
        q = line_for(n, p) + q
    return mcq_n(q, round_to(n, p), round_cands(n, p), round_expl(n, p), rnd)


# ============================================================ set 1: nearest 10
def set_ten(rnd, pk):
    its = []
    no9 = lambda n: digit(n, 1) != 9
    for _ in range(4):                                         # 2-digit, number line
        its.append(q_round(pk.pick(11, 89, 10, no9), 10, rnd, True))
    for _ in range(5):                                         # 3-digit, number line
        its.append(q_round(pk.pick(101, 989, 10, no9), 10, rnd, True))
    for j in range(5):                                         # 4-digit, number line
        n = pk.take(3496) if j == 2 else pk.pick(1001, 9889, 10, no9)
        its.append(q_round(n, 10, rnd, True))
    for j in range(6):                                         # no picture
        if j == 4:
            n = pk.take(2996)
        elif j == 5:
            n = pk.take(5705)
        elif j < 2:
            n = pk.pick(101, 989, 10, no9)
        else:
            n = pk.pick(1001, 9889, 10, no9)
        its.append(q_round(n, 10, rnd))
    return {"title": "Round to the nearest 10", "items": its}


# ============================================================ set 2: nearest 100
def set_hundred(rnd, pk):
    its = []
    no9 = lambda n: digit(n, 2) != 9 and n % 100 != 50
    for _ in range(4):                                         # 3-digit, number line
        its.append(q_round(pk.pick(110, 890, 100, no9), 100, rnd, True))
    for j in range(6):                                         # 4-digit, number line
        n = pk.take(3462) if j == 1 else pk.take(4962) if j == 4 else pk.pick(1010, 8890, 100, no9)
        its.append(q_round(n, 100, rnd, True))
    fixed = {3: 6038, 6: 1049, 8: 2965, 9: 7981}
    for j in range(10):                                        # no picture
        n = pk.take(fixed[j]) if j in fixed else pk.pick(1010, 8890, 100, no9)
        its.append(q_round(n, 100, rnd))
    return {"title": "Round to the nearest 100", "items": its}


# ============================================================ set 3: nearest 1,000
def set_thousand(rnd, pk):
    its = []
    no9 = lambda n: digit(n, 3) != 9 and n % 1000 != 500
    for j in range(6):                                         # 4-digit, number line
        n = pk.take(9615) if j == 5 else pk.pick(1010, 8990, 1000, no9)
        its.append(q_round(n, 1000, rnd, True))
    fixed = {2: 4062, 5: 6950, 7: 8499}
    for j in range(10):                                        # 4-digit, no picture
        n = pk.take(fixed[j]) if j in fixed else pk.pick(1010, 8990, 1000, no9)
        its.append(q_round(n, 1000, rnd))
    for n in [12640, 19615, 45381, 30742]:                     # 5-digit
        its.append(q_round(pk.take(n), 1000, rnd))
    return {"title": "Round to the nearest 1,000", "items": its}


# ============================================================ set 4: the 5 rule, 9s, which numbers round, estimating
def which_rounds(target, p, right, wrong, rnd):
    assert round_to(right, p) == target
    for w in wrong:
        assert round_to(w, p) != target, (target, w)
    lo, hi = target - p // 2, target + p // 2 - 1
    e = ("Numbers from %s to %s round to %s. %s is in that range. %s rounds to %s."
         % (c(lo), c(hi), c(target), c(right), c(wrong[0]), c(round_to(wrong[0], p))))
    return mcq("Which number rounds to %s when you round to the nearest %s?" % (c(target), PLACE[p]),
               c(right), [c(w) for w in wrong], e, rnd)


def estimate(a, b, op, p, rnd, story=None, unit=c):
    ra, rb = round_to(a, p), round_to(b, p)
    exact = a + b if op == "+" else a - b
    est = ra + rb if op == "+" else ra - rb
    ta, tb = a // p * p, b // p * p                            # always rounded down
    trunc = ta + tb if op == "+" else ta - tb
    other = round_to(a, p // 10) + round_to(b, p // 10) if op == "+" else round_to(a, p // 10) - round_to(b, p // 10)
    assert est != exact and est > 0
    sym = "+" if op == "+" else "−"
    e = ("%s rounds to %s and %s rounds to %s. %s %s %s = %s. (The exact answer is %s%s.)"
         % (c(a), c(ra), c(b), c(rb), c(ra), sym, c(rb), c(est), c(exact),
            ", so the estimate is close" if abs(est - exact) <= p // 2 else ""))
    q = story or ("Estimate %s %s %s by rounding each number to the nearest %s." % (c(a), sym, c(b), PLACE[p]))
    return mcq_n(q, est, [exact, trunc, other, est + p, est - p], e, rnd, fmt=unit)


def set_mixed(rnd, pk):
    its = []
    # the 5 rule (5)
    for n, p in [(450, 100), (65, 10), (3500, 1000), (2850, 100), (7495, 10)]:
        its.append(q_round(pk.take(n), p, rnd))
    # 9s (2)
    for n, p in [(6997, 10), (3950, 100)]:
        its.append(q_round(pk.take(n), p, rnd))
    # which numbers round to a value (4)
    its.append(which_rounds(450, 10, 447, [455, 441, 458], rnd))
    its.append(which_rounds(800, 100, 763, [850, 742, 871], rnd))
    its.append(which_rounds(1000, 100, 972, [1050, 940, 1130], rnd))
    its.append(which_rounds(3000, 1000, 2684, [3500, 2450, 3812], rnd))
    # smallest and greatest (2)
    its.append(mcq("What is the smallest whole number that rounds to 600 when you round to the nearest 100?", "550",
                   ["500", "549", "600"],
                   "Numbers from 550 to 649 round to 600. 549 has 4 tens, so it rounds down to 500. The smallest is 550.",
                   rnd))
    its.append(mcq("What is the greatest whole number that rounds to 4,000 when you round to the nearest 1,000?", "4,499",
                   ["4,500", "4,999", "4,449"],
                   "Numbers from 3,500 to 4,499 round to 4,000. 4,500 has 5 hundreds, so it rounds up to 5,000. "
                   "The greatest is 4,499.", rnd))
    # one number, three places (1)
    its.append(mcq("Round 6,348 to the nearest 10, the nearest 100 and the nearest 1,000. Which list is correct?",
                   "6,350; 6,300; 6,000", ["6,350; 6,400; 6,000", "6,340; 6,300; 6,000", "6,350; 6,300; 7,000"],
                   "Always round the number you started with, 6,348. Nearest 10: the ones digit is 8, so 6,350. "
                   "Nearest 100: the tens digit is 4, so 6,300. Nearest 1,000: the hundreds digit is 3, so 6,000. "
                   "Do not round 6,350 again to get 6,400.", rnd))
    # estimating (6)
    its.append(estimate(2987, 1045, "+", 1000, rnd))
    for a, b, op, p in [(4812, 3275, "+", 1000), (378, 452, "+", 100), (2648, 1173, "+", 100),
                        (6812, 2395, "−", 100), (8730, 3214, "−", 1000)]:
        its.append(estimate(a, b, op, p, rnd))
    return {"title": "Halfway numbers, 9s and estimating", "items": its}


# ============================================================ set 5: word problems
def unit_fmt(pre="", post=""):
    return lambda v: pre + c(v) + post


def story(t, n, p, rnd, pre="", post="", extra=""):
    f = unit_fmt(pre, post)
    r = round_to(n, p)
    return mcq_n(t, r, round_cands(n, p), round_expl(n, p).replace("Answer: %s." % c(r), "Answer: %s." % f(r)) + extra,
                 rnd, fmt=f)


def set_words(rnd, P):
    its = []
    its.append(story("A crowd of 34,628 fans watched a football match. What is the crowd rounded to the nearest 1,000?",
                     34628, 1000, rnd, post=" fans"))
    its.append(story("At another match, 41,375 fans were in the stadium. Round this to the nearest 100.",
                     41375, 100, rnd, post=" fans"))
    its.append(story("The River Thames is 346 km long. How long is it to the nearest 10 km?", 346, 10, rnd, post=" km"))
    its.append(story("Ben Nevis is 1,345 m high. What is its height to the nearest 100 m?", 1345, 100, rnd, post=" m"))
    its.append(story("Snowdon is 1,085 m high. What is its height to the nearest 100 m?", 1085, 100, rnd, post=" m"))
    its.append(story("The school fair raised £1,346. How much is that to the nearest £10?", 1346, 10, rnd, pre="£"))
    its.append(story("The summer fair raised £2,483. How much is that to the nearest £100?", 2483, 100, rnd, pre="£"))
    its.append(story("The town library has 6,752 books. How many is that to the nearest 1,000?", 6752, 1000, rnd,
                     post=" books"))
    its.append(story("The school library has 4,815 books. How many is that to the nearest 100?", 4815, 100, rnd,
                     post=" books"))
    its.append(story("A primary school has 465 pupils. How many is that to the nearest 100?", 465, 100, rnd,
                     post=" pupils"))
    name, she, her = P.next()
    its.append(story("%s walked 8,964 steps on Saturday. How many steps is that to the nearest 100?" % name,
                     8964, 100, rnd, post=" steps"))
    its.append(story("The car park at a shopping centre has 1,250 spaces. How many is that to the nearest 100?",
                     1250, 100, rnd, post=" spaces"))
    name, she, her = P.next()
    its.append(story("%s’s family car has travelled 25,961 km. How far is that to the nearest 100 km?" % name,
                     25961, 100, rnd, post=" km"))
    its.append(story("A marathon is 42,195 m long. How long is it to the nearest 1,000 m?", 42195, 1000, rnd, post=" m"))
    # estimating in context (3)
    name, she, her = P.next()
    its.append(estimate(386, 247, "+", 100, rnd, unit=unit_fmt(post=" km"),
                        story="%s’s family drove 386 km to Cornwall on Saturday and 247 km around Cornwall during the week. "
                              "Round each distance to the nearest 100 km to estimate the total." % name))
    its.append(estimate(1947, 2186, "+", 1000, rnd, unit=unit_fmt(pre="£"),
                        story="A school raised £1,947 at its winter fair and £2,186 at its summer fair. "
                              "Round each amount to the nearest £1,000 to estimate the total."))
    its.append(estimate(9875, 6912, "−", 1000, rnd, unit=unit_fmt(post=" seats"),
                        story="A stadium has 9,875 seats. 6,912 tickets were sold. Round each number to the nearest 1,000 "
                              "to estimate how many seats were empty."))
    # reasoning (3)
    for w in [26450, 27500, 27900]:
        assert round_to(w, 1000) != 27000
    assert round_to(26580, 1000) == 27000
    its.append(mcq("A newspaper says “about 27,000 fans” watched a match. The number was rounded to the nearest 1,000. "
                   "Which could be the real crowd?", "26,580", ["26,450", "27,500", "27,900"],
                   "Numbers from 26,500 to 27,499 round to 27,000. 26,580 is in that range. 26,450 rounds down to 26,000, "
                   "and 27,500 and 27,900 round up to 28,000.", rnd))
    its.append(mcq("A library says it has about 3,000 books, rounded to the nearest 1,000. "
                   "What is the greatest number of books it could have?", "3,499", ["3,500", "3,999", "2,999"],
                   "Numbers from 2,500 to 3,499 round to 3,000. 3,500 rounds up to 4,000, so the greatest is 3,499.", rnd))
    its.append(mcq("A museum had 18,463 visitors in March. Which poster shows this number rounded to the nearest 100?",
                   "about 18,500", ["about 18,460", "about 18,000", "about 18,400"],
                   "To the nearest 100, look at the tens digit: 6. 5 or more, so round up to 18,500. "
                   "18,460 is to the nearest 10 and 18,000 is to the nearest 1,000.", rnd))
    return {"title": "Rounding word problems", "items": its}


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
        "<h2>What rounding means</h2>"
        "<p>Rounding finds the <b>closest</b> 10, 100 or 1,000. Rounded numbers are easier to add and subtract "
        "in your head, and they help you check whether an answer makes sense.</p>"
        "<figure class='sn-fig'>" + number_line_svg(40, 50, 47, 1) +
        "<figcaption>47 is closer to 50 than to 40, so 47 rounded to the nearest 10 is 50.</figcaption></figure>"
        "<h2>The rounding rule</h2>"
        "<ol class='rk-step'><li>Find the digit in the place you are rounding to.</li>"
        "<li>Look at the digit <b>one place to its right</b>.</li>"
        "<li><b>5 or more</b>: round up (add 1 to the rounding digit). <b>4 or less</b>: round down (keep it).</li>"
        "<li>Change every digit to the right of the rounding place to 0.</li></ol>"
        "<figure class='sn-fig'>" + number_line_svg(3400, 3500, 3462, 10) +
        "<figcaption>3,462 is between 3,400 and 3,500. It is past the halfway point, 3,450, so it rounds to 3,500.</figcaption></figure>" +
        table(["Round 3,462 to the nearest", "Look at", "Answer"], [
            ["10", "the ones digit: 2", "3,460"],
            ["100", "the tens digit: 6", "3,500"],
            ["1,000", "the hundreds digit: 4", "3,000"],
        ]) +
        ex("Exactly halfway", "Round 450 to the nearest 100.",
           "450 is exactly halfway between 400 and 500. A number that is exactly halfway rounds up.", "500") +
        ex("Watch the 9s", "Round 2,965 to the nearest 100.",
           "The hundreds digit is 9 and the tens digit is 6, so round up. 9 hundreds + 1 hundred = 10 hundreds. "
           "Exchange 10 hundreds for 1 thousand: 2,900 + 100 = 3,000.", "3,000") +
        "<h2>Estimating with rounding</h2>"
        "<p>Round each number first, then add or subtract the rounded numbers. Compare the estimate with your "
        "exact answer to spot a mistake.</p>" +
        ex("Estimate", "Estimate 2,987 + 1,045 by rounding to the nearest 1,000.",
           "2,987 rounds to 3,000 and 1,045 rounds to 1,000. 3,000 + 1,000 = 4,000. The exact answer, 4,032, is close.",
           "about 4,000") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Rounding 450 down to 400", "Exactly halfway rounds up: 500"],
            ["Changing the wrong digit (3,462 to the nearest 100 = 3,460 or 3,000)", "Find the hundreds digit first: 3,500"],
            ["Keeping the digits after the place (3,462 → 3,562)", "Change every digit after the place to 0: 3,500"],
            ["Writing 10 in one place (2,965 → 21,000) or losing it (2,965 → 2,000)", "Exchange 10 hundreds for 1 thousand: 3,000"],
            ["Rounding twice (6,348 → 6,350 → 6,400)", "Always round the original number: 6,300"],
        ])
    )


FAQ = [
    {"q": "What rounding does a Year 4 child need to know?",
     "a": "The National Curriculum says Year 4 pupils should round any number to the nearest 10, 100 or 1,000. "
          "They also round decimals with one decimal place to the nearest whole number."},
    {"q": "How do you round to the nearest 1,000?",
     "a": "Look at the hundreds digit. If it is 5 or more, round up; if it is 4 or less, round down. "
          "So 4,612 rounds to 5,000 and 4,388 rounds to 4,000."},
    {"q": "Does 5 round up or down?",
     "a": "5 rounds up. A number that is exactly halfway, such as 35 or 450, always rounds up, so 35 becomes 40 and 450 becomes 500."},
    {"q": "Why do children learn to round numbers?",
     "a": "Rounding is used to estimate. Estimating before a column addition or subtraction is a quick way to check "
          "whether the exact answer is sensible."},
]


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


def mark_large(u, pattern):
    """Tag pictures that must print larger (number lines) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4403)
    P = People(rnd)
    pk = Picker(rnd)
    sets = [set_ten(rnd, pk), set_hundred(rnd, pk), set_thousand(rnd, pk), set_mixed(rnd, pk), set_words(rnd, P)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [x.replace(",", "") for x in it["c"]]
            assert len(set(vals)) == 4, it
    u = {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "rounding", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Rounding to the Nearest 10, 100 and 1,000",
        "seo_title": "Year 4 Rounding Worksheets: Nearest 10, 100 and 1,000 (Free, with Answer Key)",
        "short_title": "Rounding to 10, 100 and 1,000",
        "domain": "Number and place value",
        "standard_code": "Year 4: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Round any number to the nearest 10, 100 or 1,000; solve number and practical problems that involve all of the above and with increasingly large positive numbers.",
        "meta_desc": "Free Year 4 maths rounding worksheets for the National Curriculum: round to the nearest 10, 100 and 1,000 with number lines, halfway numbers, rounding 9s, estimating and word problems. 100 questions with answer key.",
        "key_big": "Look one place to the right. 5 or more: round up. 4 or less: round down.",
        "key_sub": "Then change every digit after the rounding place to 0. A number exactly halfway, such as 450, rounds up. A 9 that rounds up is exchanged: 2,965 to the nearest 100 is 3,000.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
