# -*- coding: utf-8 -*-
"""
UK Year 5 Maths (National Curriculum in England): Rounding numbers up to 1,000,000
to the nearest 10, 100, 1,000, 10,000 and 100,000
  python3 tools/gen_uk_maths_y5_rounding.py
HTML attributes use single quotes (no backslashes in the JSON).
Numbers of 1,000 or more are always written with commas.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

PLACE = {10: "10", 100: "100", 1000: "1,000", 10000: "10,000", 100000: "100,000"}
LOOK = {10: "ones", 100: "tens", 1000: "hundreds", 10000: "thousands", 100000: "ten thousands"}       # digit to look at
OWN = {10: "tens", 100: "hundreds", 1000: "thousands", 10000: "ten thousands", 100000: "hundred thousands"}
NEXT1 = {10: "hundred", 100: "thousand", 1000: "ten thousand", 10000: "hundred thousand", 100000: "million"}


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
    """Short explanation of rounding n to the nearest p."""
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
    """When a 9 rounds up: writing “10” in one place (695,000 -> 6,100,000) or forgetting to exchange (-> 600,000)."""
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
    other = lo + p if r == lo else lo                         # rounded the wrong way
    out = [other] + nine_mistakes(n, p)
    if r > lo:
        out.append(r + n % p)                                 # kept the digits after the place
    if p >= 100:
        out.append(round_to(n, p // 10))                      # rounded to the place on the right
        out.append(n // (p // 10) * (p // 10))                # cut off at the wrong place
    out.append(n // (p * 10) * (p * 10))                      # changed the wrong digit
    if p >= 10000:
        out.append(round_to(n, p // 100))                     # rounded to a place two to the right
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
        """A number in [lo, hi] that is not a multiple of 10, not halfway, has no 9 in the rounding place, not used."""
        while True:
            n = self.rnd.randint(lo, hi)
            if (n % 10 and n % p != p // 2 and digit(n, lg(p)) != 9 and n not in self.used and ok(n)
                    and round_to(n, p) > 0):
                self.used.add(n)
                return n


def q_round(n, p, rnd, line=False):
    q = "Round %s to the nearest %s." % (c(n), PLACE[p])
    if line:
        q = line_for(n, p) + q
    return mcq_n(q, round_to(n, p), round_cands(n, p), round_expl(n, p), rnd)


FIVE = (10001, 98999)
SIX = (100001, 989999)


# ============================================================ set 1: nearest 10, 100 and 1,000
def set_small(rnd, pk):
    its = []
    for p, sizes in [(10, [FIVE, FIVE, FIVE, SIX]), (100, [FIVE, FIVE, SIX, SIX]), (1000, [FIVE, FIVE, SIX, SIX])]:
        for lo, hi in sizes:                                   # number line
            its.append(q_round(pk.pick(lo, hi, p), p, rnd, True))
    for n, p in [(None, 10), (45996, 10), (None, 100), (None, 100), (72961, 100),
                 (None, 1000), (None, 1000), (58712, 1000)]:   # no picture
        if n is None:
            n = pk.pick(*(SIX if len(its) % 2 else FIVE), p)
        else:
            n = pk.take(n)
        its.append(q_round(n, p, rnd))
    return {"title": "Round to the nearest 10, 100 and 1,000", "items": its}


# ============================================================ set 2: nearest 10,000
def set_tenk(rnd, pk):
    its = []
    for j in range(8):                                         # number line
        its.append(q_round(pk.pick(*(FIVE if j < 4 else SIX), 10000), 10000, rnd, True))
    fixed = {2: 49600, 5: 296400, 8: 803700, 10: 14999}
    for j in range(12):                                        # no picture
        n = pk.take(fixed[j]) if j in fixed else pk.pick(*(SIX if j % 2 else FIVE), 10000)
        its.append(q_round(n, 10000, rnd))
    return {"title": "Round to the nearest 10,000", "items": its}


# ============================================================ set 3: nearest 100,000
def set_hundredk(rnd, pk):
    its = []
    for j in range(8):                                         # number line
        its.append(q_round(pk.pick(100001, 889999, 100000), 100000, rnd, True))
    fixed = {1: 965300, 4: 349999, 7: 52800, 10: 921000}
    for j in range(12):                                        # no picture
        n = pk.take(fixed[j]) if j in fixed else pk.pick(100001, 889999, 100000)
        its.append(q_round(n, 100000, rnd))
    return {"title": "Round to the nearest 100,000", "items": its}


# ============================================================ set 4: halfway, 9s, which numbers round, estimating
def which_rounds(target, p, right, wrong, rnd):
    assert round_to(right, p) == target
    for w in wrong:
        assert round_to(w, p) != target, (target, w)
    lo, hi = target - p // 2, target + p // 2 - 1
    e = ("Numbers from %s to %s round to %s. %s is in that range. %s rounds to %s."
         % (c(lo), c(hi), c(target), c(right), c(wrong[0]), c(round_to(wrong[0], p))))
    return mcq("Which number rounds to %s when you round to the nearest %s?" % (c(target), PLACE[p]),
               c(right), [c(w) for w in wrong], e, rnd)


def estimate(a, b, op, p, rnd, story=None, unit=c, extra=""):
    ra, rb = round_to(a, p), round_to(b, p)
    exact = a + b if op == "+" else a - b
    est = ra + rb if op == "+" else ra - rb
    ta, tb = a // p * p, b // p * p                            # always rounded down
    trunc = ta + tb if op == "+" else ta - tb
    other = round_to(a, p // 10) + round_to(b, p // 10) if op == "+" else round_to(a, p // 10) - round_to(b, p // 10)
    assert est != exact and est > 0
    sym = "+" if op == "+" else "−"
    e = ("%s rounds to %s and %s rounds to %s. %s %s %s = %s. (The exact answer is %s%s.)%s"
         % (c(a), c(ra), c(b), c(rb), c(ra), sym, c(rb), c(est), c(exact),
            ", so the estimate is close" if abs(est - exact) <= p // 2 else "", extra))
    q = story or ("Estimate %s %s %s by rounding each number to the nearest %s." % (c(a), sym, c(b), PLACE[p]))
    return mcq_n(q, est, [exact, trunc, other, est + p, est - p], e, rnd, fmt=unit)


def set_mixed(rnd, pk):
    its = []
    # halfway numbers (4)
    for n, p in [(45500, 1000), (235000, 10000), (650000, 100000), (72850, 100)]:
        its.append(q_round(pk.take(n), p, rnd))
    # 9s that roll over (4)
    for n, p in [(695000, 10000), (384995, 10), (39960, 100), (499600, 1000)]:
        its.append(q_round(pk.take(n), p, rnd))
    # which numbers round to a value (4)
    its.append(which_rounds(250000, 10000, 246300, [255000, 244900, 262000], rnd))
    its.append(which_rounds(700000, 100000, 658000, [750000, 649999, 612000], rnd))
    its.append(which_rounds(40000, 1000, 39620, [40500, 38950, 41200], rnd))
    its.append(which_rounds(100000, 10000, 96500, [105000, 94800, 110200], rnd))
    # smallest and greatest (3)
    its.append(mcq("What is the smallest whole number that rounds to 300,000 when you round to the nearest 100,000?",
                   "250,000", ["249,999", "200,000", "350,000"],
                   "Numbers from 250,000 to 349,999 round to 300,000. 249,999 has 4 ten thousands, so it rounds down "
                   "to 200,000. The smallest is 250,000.", rnd))
    its.append(mcq("What is the greatest whole number that rounds to 80,000 when you round to the nearest 10,000?",
                   "84,999", ["85,000", "89,999", "84,000"],
                   "Numbers from 75,000 to 84,999 round to 80,000. 85,000 is exactly halfway, so it rounds up to "
                   "90,000. The greatest is 84,999.", rnd))
    its.append(mcq("What is the smallest whole number that rounds to 63,700 when you round to the nearest 100?",
                   "63,650", ["63,649", "63,600", "63,750"],
                   "Numbers from 63,650 to 63,749 round to 63,700. 63,649 has 4 tens, so it rounds down to 63,600. "
                   "The smallest is 63,650.", rnd))
    # two places (2)
    its.append(mcq("Round 645,380 to the nearest 10,000 and to the nearest 100,000. Which pair is correct?",
                   "650,000; 600,000", ["650,000; 700,000", "640,000; 600,000", "645,000; 600,000"],
                   "Always round the number you started with, 645,380. Nearest 10,000: the thousands digit is 5, "
                   "so 650,000. Nearest 100,000: the ten thousands digit is 4, so 600,000. "
                   "Do not round 650,000 again to get 700,000.", rnd))
    for w in [386600, 384900, 385400]:
        assert round_to(w, 1000) != 386000
    assert round_to(385740, 1000) == 386000 and round_to(385740, 10000) == 390000
    its.append(mcq("Which number rounds to 386,000 to the nearest 1,000 and to 390,000 to the nearest 10,000?",
                   "385,740", ["386,600", "384,900", "385,400"],
                   "Numbers from 385,500 to 386,499 round to 386,000. Only 385,740 is in that range, and it rounds "
                   "to 390,000 because its thousands digit is 5. 386,600 rounds to 387,000.", rnd))
    # estimating (3)
    for a, b, op, p in [(48750, 31260, "+", 1000), (386400, 142900, "−", 10000), (61840, 27390, "+", 10000)]:
        its.append(estimate(a, b, op, p, rnd))
    return {"title": "Halfway numbers, 9s and estimating", "items": its}


# ============================================================ set 5: word problems
def unit_fmt(pre="", post=""):
    return lambda v: pre + c(v) + post


def story(t, n, p, rnd, pre="", post=""):
    f = unit_fmt(pre, post)
    r = round_to(n, p)
    return mcq_n(t, r, round_cands(n, p), round_expl(n, p).replace("Answer: %s." % c(r), "Answer: %s." % f(r)),
                 rnd, fmt=f)


def set_words(rnd, P):
    its = []
    its.append(story("A crowd of 87,469 watched a cup final at Wembley. What is the crowd to the nearest 1,000?",
                     87469, 1000, rnd, post=" fans"))
    its.append(story("A crowd of 52,316 watched a rugby match. What is the crowd to the nearest 10,000?",
                     52316, 10000, rnd, post=" fans"))
    its.append(story("The Moon is about 384,400 km from the Earth. What is this distance to the nearest 10,000 km?",
                     384400, 10000, rnd, post=" km"))
    its.append(story("A house is for sale for £284,950. What is the price to the nearest £10,000?",
                     284950, 10000, rnd, pre="£"))
    its.append(story("A flat sold for £347,500. What is the price to the nearest £1,000?", 347500, 1000, rnd, pre="£"))
    its.append(story("A town has 136,742 people. How many is that to the nearest 100,000?", 136742, 100000, rnd,
                     post=" people"))
    its.append(story("A smaller town has 68,519 people. How many is that to the nearest 10,000?", 68519, 10000, rnd,
                     post=" people"))
    its.append(story("In a London marathon, 53,682 runners finished. How many is that to the nearest 1,000?",
                     53682, 1000, rnd, post=" runners"))
    its.append(story("A plane flies 16,993 km from London to Sydney. How far is that to the nearest 1,000 km?",
                     16993, 1000, rnd, post=" km"))
    its.append(story("A charity raised £695,280. How much is that to the nearest £10,000?", 695280, 10000, rnd, pre="£"))
    its.append(story("Mount Everest is 8,849 m high. What is its height to the nearest 100 m?", 8849, 100, rnd,
                     post=" m"))
    its.append(story("A football stadium has 74,310 seats. How many is that to the nearest 1,000?", 74310, 1000, rnd,
                     post=" seats"))
    name, she, her = P.next()
    its.append(story("%s’s family car has travelled 99,640 km. How far is that to the nearest 1,000 km?" % name,
                     99640, 1000, rnd, post=" km"))
    its.append(story("A children’s book sold 405,862 copies. How many is that to the nearest 100,000?",
                     405862, 100000, rnd, post=" copies"))
    its.append(story("A seaside pier had 652,380 visitors last year. How many is that to the nearest 100,000?",
                     652380, 100000, rnd, post=" visitors"))
    # estimating to check (2)
    name, she, her = P.next()
    its.append(estimate(38460, 24915, "+", 1000, rnd,
                        story="%s works out 38,460 + 24,915 and gets 53,375. Round each number to the nearest 1,000 "
                              "to estimate the answer. What is the estimate?" % name,
                        extra=" %s’s answer is too far from 63,000, so it must be wrong." % name))
    its.append(estimate(243800, 318500, "+", 10000, rnd, unit=unit_fmt(pre="£"),
                        story="Two houses cost £243,800 and £318,500. Round each price to the nearest £10,000 "
                              "to estimate the total cost."))
    # reasoning (3)
    for w in [54800, 65000, 66300]:
        assert round_to(w, 10000) != 60000
    assert round_to(56200, 10000) == 60000
    its.append(mcq("A newspaper says “about 60,000 fans” were at a concert. The number was rounded to the nearest "
                   "10,000. Which could be the real number?", "56,200", ["54,800", "65,000", "66,300"],
                   "Numbers from 55,000 to 64,999 round to 60,000. 56,200 is in that range. 54,800 rounds down to "
                   "50,000, and 65,000 and 66,300 round up to 70,000.", rnd))
    its.append(mcq("About 400,000 people live in a city, rounded to the nearest 100,000. "
                   "What is the greatest number of people who could live there?", "449,999",
                   ["450,000", "499,999", "399,999"],
                   "Numbers from 350,000 to 449,999 round to 400,000. 450,000 rounds up to 500,000, so the greatest "
                   "is 449,999.", rnd))
    its.append(mcq("A poster says the Moon is about 400,000 km away. The real distance is 384,400 km. "
                   "What was it rounded to?", "the nearest 100,000",
                   ["the nearest 10,000", "the nearest 1,000", "the nearest 100"],
                   "To the nearest 100,000, 384,400 rounds up to 400,000. To the nearest 10,000 it is 380,000, "
                   "and to the nearest 1,000 it is 384,000.", rnd))
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
        "<p>Rounding finds the <b>closest</b> 10, 100, 1,000, 10,000 or 100,000. Rounded numbers are easier to "
        "work with, and they help you check whether an answer makes sense.</p>"
        "<figure class='sn-fig'>" + number_line_svg(200000, 300000, 245180, 10000) +
        "<figcaption>245,180 is closer to 200,000 than to 300,000. It has not reached the halfway point, 250,000, "
        "so to the nearest 100,000 it rounds down to 200,000.</figcaption></figure>"
        "<h2>The rounding rule</h2>"
        "<ol class='rk-step'><li>Find the digit in the place you are rounding to.</li>"
        "<li>Look at the digit <b>one place to its right</b>.</li>"
        "<li><b>5 or more</b>: round up (add 1 to the rounding digit). <b>4 or less</b>: round down (keep it).</li>"
        "<li>Change every digit to the right of the rounding place to 0.</li></ol>"
        "<figure class='sn-fig'>" + number_line_svg(34000, 35000, 34628, 100) +
        "<figcaption>34,628 is past the halfway point, 34,500, so to the nearest 1,000 it rounds up to 35,000.</figcaption></figure>" +
        table(["Round 548,362 to the nearest", "Look at", "Answer"], [
            ["10", "the ones digit: 2", "548,360"],
            ["100", "the tens digit: 6", "548,400"],
            ["1,000", "the hundreds digit: 3", "548,000"],
            ["10,000", "the thousands digit: 8", "550,000"],
            ["100,000", "the ten thousands digit: 4", "500,000"],
        ]) +
        ex("Exactly halfway", "Round 465,000 to the nearest 10,000.",
           "465,000 is exactly halfway between 460,000 and 470,000. A number that is exactly halfway rounds up.",
           "470,000") +
        ex("Watch the 9s", "Round 396,500 to the nearest 10,000.",
           "The ten thousands digit is 9 and the thousands digit is 6, so round up. 9 ten thousands + 1 ten thousand "
           "= 10 ten thousands. Exchange them for 1 hundred thousand: 390,000 + 10,000 = 400,000.", "400,000") +
        "<h2>Estimating with rounding</h2>"
        "<p>Round each number first, then add or subtract the rounded numbers. If your exact answer is far from "
        "the estimate, check your working.</p>" +
        ex("Estimate", "Estimate 59,820 + 21,350 by rounding to the nearest 1,000.",
           "59,820 rounds to 60,000 and 21,350 rounds to 21,000. 60,000 + 21,000 = 81,000. "
           "The exact answer, 81,170, is close.", "about 81,000") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Rounding 465,000 down to 460,000", "Exactly halfway rounds up: 470,000"],
            ["Rounding the wrong place (548,362 to the nearest 10,000 = 548,000)", "Find the ten thousands digit first: 550,000"],
            ["Keeping the digits after the place (34,628 → 35,628)", "Change every digit after the place to 0: 35,000"],
            ["Writing 10 in one place (695,000 → 6,100,000) or losing it (695,000 → 600,000)",
             "Exchange 10 ten thousands for 1 hundred thousand: 700,000"],
            ["Rounding twice (645,380 → 650,000 → 700,000)", "Always round the original number: 600,000"],
        ])
    )


FAQ = [
    {"q": "What rounding do Year 5 children learn?",
     "a": "The National Curriculum says Year 5 pupils should round any number up to 1,000,000 to the nearest 10, 100, "
          "1,000, 10,000 and 100,000. They also round decimals to the nearest whole number and to one decimal place."},
    {"q": "How do you round to the nearest 10,000?",
     "a": "Look at the thousands digit. If it is 5 or more, round up; if it is 4 or less, round down. "
          "So 46,800 rounds to 50,000 and 43,900 rounds to 40,000."},
    {"q": "How do you round to the nearest 100,000?",
     "a": "Look at the ten thousands digit. 5 or more rounds up and 4 or less rounds down, so 258,000 rounds to "
          "300,000 and 349,999 rounds to 300,000."},
    {"q": "How do you teach rounding in Year 5?",
     "a": "Start with a number line to show which multiple is closer, then teach the rule: look one place to the right. "
          "Practise halfway numbers and 9s that round up, such as 695,000 to 700,000, and use rounding to estimate."},
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
    rnd = random.Random(5502)
    P = People(rnd)
    pk = Picker(rnd)
    sets = [set_small(rnd, pk), set_tenk(rnd, pk), set_hundredk(rnd, pk), set_mixed(rnd, pk), set_words(rnd, P)]
    balance(sets, rnd)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
            assert len(set(it["c"])) == 4, it
            vals = [x.replace(",", "") for x in it["c"]]
            assert len(set(vals)) == 4, it
    u = {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "rounding", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Rounding Numbers up to 1,000,000",
        "seo_title": "Year 5 Rounding Worksheets: Nearest 10 to 100,000 (Free, with Answer Key)",
        "short_title": "Rounding to 1,000,000",
        "domain": "Number and place value",
        "standard_code": "Year 5: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Round any number up to 1,000,000 to the nearest 10, 100, 1,000, 10,000 and 100,000; solve number problems and practical problems that involve all of the above.",
        "meta_desc": "Free Year 5 maths rounding worksheets for the National Curriculum: round numbers up to 1,000,000 to the nearest 10, 100, 1,000, 10,000 and 100,000, with number lines, halfway numbers, 9s, estimating and word problems. 100 questions with answer key.",
        "key_big": "Look one place to the right. 5 or more: round up. 4 or less: round down.",
        "key_sub": "Then change every digit after the rounding place to 0. A number exactly halfway, such as 465,000, rounds up. A 9 that rounds up is exchanged: 695,000 to the nearest 10,000 is 700,000.",
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
