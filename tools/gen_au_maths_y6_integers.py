# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Integers and negative numbers (Australian Curriculum v9.0: AC9M6N01)
  python3 tools/gen_au_maths_y6_integers.py
Integers in context (winter temperatures in Thredbo and Canberra, car park levels below the ground floor,
bank balances and money owed, metres above and below sea level), reading integers on number lines and
thermometers, comparing and ordering integers, counting on and back across zero, and word problems.
Wrong answers come from real student mistakes: dropping the minus sign, −7 > −2 because 7 > 2, ordering by
the digits and ignoring the sign, counting every tick as 1 when the scale counts by 2 or 5, counting from the
wrong label, skipping 0 when counting across zero, counting the starting number as a step, counting the
numbers instead of the spaces, and moving the wrong way.
HTML attributes use single quotes (no backslashes in the JSON). Australian English. Real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NBSP = " "
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ numbers
def n(v):
    """Integer with the real minus sign. Australian style: 4 digits with no separator."""
    v = F(v)
    assert v.denominator == 1, v
    a = abs(v.numerator)
    s = str(a) if a < 10000 else "{:,}".format(a).replace(",", NBSP)
    return (M if v < 0 else "") + s


def deg(v):
    return n(v) + NBSP + "°C"


def money(v):
    v = F(v)
    return (M if v < 0 else "") + "$" + n(abs(v))


def metres(v):
    return n(v) + " m"


def spaces(k):
    return "1 space" if k == 1 else "%d spaces" % k


def ticks(k):
    return "1 tick mark" if k == 1 else "%d tick marks" % k


def steps(k):
    return "1 step" if k == 1 else "%d steps" % k


def lst(vals):
    return ", ".join(n(v) for v in vals)


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ question helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e, rnd):
    """correct and cands: strings, or (string, value) pairs. A candidate equal in value (or text) to the
    correct answer or to an earlier candidate is skipped."""
    cs, cv = correct if isinstance(correct, tuple) else (correct, None)
    seen, vals, pick = {plain(cs)}, ({cv} if cv is not None else set()), []
    for c in cands:
        if c is None:
            continue
        s, v = c if isinstance(c, tuple) else (c, None)
        if not s or plain(s) in seen:
            continue
        if v is not None:
            if v in vals:
                continue
            vals.add(v)
        seen.add(plain(s))
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq_v(q, v, cands, e, rnd, fmt=n):
    return mcq(q, (fmt(v), F(v)), [(fmt(c), F(c)) for c in cands if c is not None], e, rnd)


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


class Pos:
    """Correct letters (A-D) for picture questions, spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Choices with a fixed order
    (A-D points) stay as they are; the other questions fill the gaps."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [max(0, 5 - c) for c in cnt]
        while sum(need) > len(free):
            need[need.index(max(need))] -= 1
        while sum(need) < len(free):
            i = min(range(4), key=lambda j: cnt[j] + need[j])
            need[i] += 1
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


# ------------------------------------------------------------ pictures
class NL:
    """Horizontal number line from lo to hi with a tick every `step` and a number under every
    multiple of `lab`. Optional hops (arcs of one step each) above the line for the lesson."""

    def __init__(self, lo, hi, step, lab, gap=None):
        lo, hi, step, lab = F(lo), F(hi), F(step), F(lab)
        k = (hi - lo) / step
        assert k.denominator == 1 and (lab / step).denominator == 1
        self.lo, self.hi, self.step, self.lab = lo, hi, step, lab
        self.n = int(k)
        self.labels = [lo + i * step for i in range(self.n + 1) if ((lo + i * step) / lab).denominator == 1]
        lw = max(tw(n(v), 14) for v in self.labels)
        self.g = gap or max(12, min(30, int(360 / self.n)))
        assert (lab / step) * self.g >= lw + 6, ("labels overlap", lo, hi, step, lab, self.g)
        self.pad = int(max(26, lw / 2 + 8))
        self.W = int(2 * self.pad + self.n * self.g)
        self.Y = 40
        self.H = 72
        self.pts, self.hops, self.top = [], [], 0
        self.hop_label = None

    def X(self, v):
        return self.pad + float((F(v) - self.lo) / self.step) * self.g

    def point(self, v, name=None, col=GREEN):
        assert self.lo <= F(v) <= self.hi and ((F(v) - self.lo) / self.step).denominator == 1, v
        self.pts.append((F(v), name, col))
        return self

    def hop(self, a, b, label):
        """One arc per step from a to b (a < b or a > b), with a label above."""
        d = 1 if b > a else -1
        v = a
        while v != b:
            self.hops.append((v, v + d * self.step))
            v += d * self.step
        self.hop_label = label
        self.top = 30
        return self

    def svg(self, label):
        Y = self.Y + self.top
        H = self.H + self.top
        s = []
        x0, x1 = self.pad - 18, self.W - self.pad + 18
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, Y, x1, Y, INK))
        s.append("<path d='M%d %d l9 -5 v10 z M%d %d l-9 -5 v10 z' fill='%s'/>" % (x0 - 2, Y, x1 + 2, Y, INK))
        for i in range(self.n + 1):
            v = self.lo + i * self.step
            x = self.X(v)
            big = v in self.labels
            h = 9 if big else 5
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                     % (x, Y - h, x, Y + h, INK, "1.8" if big else "1.2"))
            if big:
                s.append(text(x, Y + 26, n(v), 14, bold=(v == 0)))
        for a, b in self.hops:
            xa, xb = self.X(a), self.X(b)
            s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='1.8'/>"
                     % (xa, Y - 7, (xa + xb) / 2, Y - 30, xb, Y - 7, RED))
            dx = 1 if xb > xa else -1
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d z' fill='%s'/>"
                     % (xb, Y - 7, xb - dx * 8, Y - 11, xb - dx * 3, Y - 15, RED))
        if self.hops:
            xs = [self.X(a) for a, b in self.hops] + [self.X(b) for a, b in self.hops]
            s.append(text((min(xs) + max(xs)) / 2, Y - 34, self.hop_label, 14, bold=True, col=RED))
        xs = sorted(self.X(v) for v, nm, c in self.pts if nm)
        assert all(b - a >= 16 for a, b in zip(xs, xs[1:])), ("letters overlap", label)
        for v, nm, col in self.pts:
            x = self.X(v)
            s.append("<circle cx='%.1f' cy='%d' r='5.5' fill='%s'/>" % (x, Y, col))
            if nm:
                s.append(text(x, Y - 13, nm, 16, bold=True, col=col))
        return svg_wrap(self.W, H, "".join(s), label)


def nl_label(nl, what):
    return "number line from %s to %s %s" % (n(nl.lo), n(nl.hi), what)


def thermo_svg(lo, hi, step, lab, val):
    """Thermometer (°C) with a scale on the left; the red column ends at val."""
    lo, hi, step, lab, val = F(lo), F(hi), F(step), F(lab), F(val)
    k = int((hi - lo) / step)
    g = 16
    top = 16
    x = 74
    Yv = lambda v: top + float((hi - v) / step) * g
    bot = Yv(lo)
    s = ["<rect x='%d' y='%d' width='14' height='%.1f' rx='7' fill='#ffffff' stroke='%s' stroke-width='1.6'/>"
         % (x - 7, top - 8, bot - top + 16, INK)]
    s.append("<circle cx='%d' cy='%.1f' r='12' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, bot + 18, RED, INK))
    s.append("<rect x='%d' y='%.1f' width='6' height='%.1f' fill='%s'/>" % (x - 3, Yv(val), bot + 14 - Yv(val), RED))
    for i in range(k + 1):
        v = lo + i * step
        y = Yv(v)
        big = (v / lab).denominator == 1
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x - 9 - (8 if big else 4), y, x - 9, y, INK, "1.6" if big else "1.1"))
        if big:
            s.append(text(x - 22, y + 5, n(v), 14, anchor="end", bold=(v == 0)))
    s.append(text(x + 14, top + 4, "°C", 14, anchor="start"))
    H = int(bot + 34)
    return svg_wrap(110, H, "".join(s), "thermometer from %s to %s °C counting by %s" % (n(lo), n(hi), n(step)))


def floors_svg(lo, hi, val, mark):
    """Vertical number line of building levels; 0 is the ground floor; a dot at val."""
    g = 24
    top = 14
    x = 60
    Yv = lambda v: top + (hi - v) * g
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, top - 6, x, Yv(lo) + 6, INK)]
    for v in range(lo, hi + 1):
        y = Yv(v)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x - 7, y, x + 7, y, INK))
        s.append(text(x - 14, y + 5, n(v), 14, anchor="end", bold=(v == 0)))
    s.append(text(x + 16, Yv(0) + 5, "ground floor", 14, anchor="start", col=GRAY))
    assert val != 0
    s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (x, Yv(val), GREEN))
    s.append(text(x + 16, Yv(val) + 5, mark, 15, anchor="start", bold=True, col=GREEN))
    return svg_wrap(170, int(Yv(lo) + 16), "".join(s),
                    "vertical number line of building levels from %d to %d" % (lo, hi))


# ============================================================ set 1: integers in everyday life
SIT = {
    "temp": ("{n} degrees above zero", "{n} degrees below zero"),
    "sea": ("{n} metres above sea level", "{n} metres below sea level"),
    "bank": ("a deposit of ${n}", "a withdrawal of ${n}"),
    "floors": ("{n} levels above the ground floor", "{n} levels below the ground floor"),
    "points": ("winning {n} points", "losing {n} points"),
    "golf": ("{n} strokes over par", "{n} strokes under par"),
    "money": ("earning ${n}", "spending ${n}"),
    "owe": ("having ${n} saved", "owing ${n}"),
}
NEGWORD = {"temp": "below zero", "sea": "below sea level", "bank": "a withdrawal", "floors": "below the ground floor",
           "points": "losing points", "golf": "under par", "money": "spending", "owe": "owing"}
POSWORD = {"temp": "above zero", "sea": "above sea level", "bank": "a deposit", "floors": "above the ground floor",
           "points": "winning points", "golf": "over par", "money": "earning", "owe": "saving"}
ZERO = {"temp": "0 °C", "sea": "sea level", "bank": "no change to the account", "floors": "the ground floor",
        "points": "no change to the score", "golf": "par", "money": "no change", "owe": "no money and no debt"}


def sit(kind, v):
    p, q = SIT[kind]
    return (p if v > 0 else q).format(n=abs(v))


def two_story(kind, a, b, P):
    """A story with two signed quantities a (first) and b (second). Returns (text, name of a, name of b)."""
    nm, he, his = P.next()
    if kind == "temp_thredbo":
        return ("On a July morning in Thredbo, the temperature at 6 am was %s. By 2 pm, it was %s."
                % (sit("temp", a), sit("temp", b)), "the temperature at 6 am", "the temperature at 2 pm")
    if kind == "temp_canberra":
        return ("On a winter day in Canberra, the temperature at 7 am was %s. At 3 pm, it was %s."
                % (sit("temp", a), sit("temp", b)), "the temperature at 7 am", "the temperature at 3 pm")
    if kind == "sea":
        return ("On the Great Barrier Reef, a diver is %s. A seagull flies %s." % (sit("sea", a), sit("sea", b)),
                "the diver’s position", "the seagull’s position")
    if kind == "bank":
        return ("%s’s bank account changed twice. On Monday, %s made %s. On Friday, %s made %s."
                % (nm, he, sit("bank", a), he, sit("bank", b)),
                "the Monday change to the account", "the Friday change to the account")
    if kind == "floors":
        return ("In a Brisbane shopping centre, the car park is %s. The cinema is %s." % (sit("floors", a), sit("floors", b)),
                "the level of the car park", "the level of the cinema")
    if kind == "golf":
        nm2 = P.next()[0]
        return ("In a round of golf, %s finished %s and %s finished %s." % (nm, sit("golf", a), nm2, sit("golf", b)),
                "%s’s score compared with par" % nm, "%s’s score compared with par" % nm2)
    if kind == "money":
        return ("On Saturday, %s earned $%d for washing the car. On Sunday, %s spent $%d at the school fete."
                % (nm, a, he, -b), "the money earned on Saturday", "the money spent on Sunday")
    if kind == "points":
        return ("In a class quiz, a team wins %d points for a right answer and loses %d points for a wrong answer."
                % (a, -b), "a right answer", "a wrong answer")
    raise ValueError(kind)


def set_situations(rnd, P):
    its = []
    # A: a story with two quantities; write one of them as an integer (8)
    plan = [("temp_thredbo", -6, 3, 0, "temp"), ("sea", -9, 14, 0, "sea"), ("bank", 35, -20, 1, "bank"),
            ("floors", -2, 4, 0, "floors"), ("golf", 3, -2, 1, "golf"), ("temp_canberra", -4, 12, 1, "temp"),
            ("money", 18, -11, 1, "money"), ("points", 10, -5, 0, "points")]
    for kind, a, b, ask, base in plan:
        story, na, nb = two_story(kind, a, b, P)
        v, w, nv = (a, b, na) if ask == 0 else (b, a, nb)
        q = story + " Which integer represents %s?" % nv
        word = NEGWORD[base] if v < 0 else POSWORD[base]
        e = ("%s is the %s direction, so the integer is <b>%s</b>. Here, 0 would mean %s."
             % (cap(word), "negative" if v < 0 else "positive", n(v), ZERO[base]))
        if v < 0:
            e += " Do not drop the minus sign."
        its.append(mcq_v(q, v, [-v, w, -w], e, rnd))
    # B: what 0 means (4)
    zero = [
        ("Heights are measured in metres above or below sea level. What does a height of 0 m mean?",
         "exactly at sea level", ["at the bottom of the ocean", "at the top of a mountain", "there is no height to measure"],
         "Above sea level is positive and below sea level is negative. 0 m is the starting point between them: <b>exactly at sea level</b>."),
        ("A thermometer shows degrees Celsius (°C). What does 0" + NBSP + "°C mean?",
         "the temperature at which water freezes", ["no temperature at all", "the coldest temperature possible",
                                                    "the temperature at which water boils"],
         "Water freezes at 0" + NBSP + "°C. Colder temperatures are negative, so 0" + NBSP + "°C is not the coldest possible: "
         "<b>water freezes at 0" + NBSP + "°C</b>."),
        ("In a lift, the levels below the ground floor are negative. What does level 0 mean?",
         "the ground floor", ["the top floor", "the lowest car park level", "a level that does not exist"],
         "Levels above the ground floor are positive and levels below it are negative. 0 is the level between them: <b>the ground floor</b>."),
        ("A bank account balance can be positive or negative. What does a balance of $0 mean?",
         "no money in the account and nothing owed", ["the account owes you money", "you owe the bank money",
                                                      "the account has been closed"],
         "A positive balance is money you have. A negative balance is money you owe. $0 is between them: "
         "<b>no money in the account and nothing owed</b>."),
    ]
    for q, c, w, e in zero:
        its.append(mcq(q, c, w, e, rnd))
    # C: which situation could a negative integer represent (4)
    for kind, k, others in [("bank", 18, ["sea", "points"]), ("owe", 25, ["bank", "temp"]),
                            ("sea", 40, ["temp", "floors"]), ("temp", 5, ["golf", "money"])]:
        q = "Which situation could the integer %s represent?" % n(-k)
        e = ("A negative integer shows the direction below or less than 0. %s matches %s. The other choices are positive."
             % (cap(sit(kind, -k)), n(-k)))
        its.append(mcq(q, sit(kind, -k), [sit(kind, k), sit(others[0], k), sit(others[1], k)], e, rnd))
    # D: which would be written as a negative integer (4)
    for neg, poss in [(("money", 12), [("bank", 12), ("temp", 12), ("points", 12)]),
                      (("golf", 4), [("floors", 4), ("owe", 4), ("sea", 4)]),
                      (("floors", 3), [("golf", 3), ("money", 3), ("temp", 3)]),
                      (("points", 6), [("sea", 6), ("golf", 6), ("bank", 6)])]:
        k, m = neg
        q = "Which of these would be written as a negative integer?"
        e = "%s is the opposite of %s, so it is written as %s. The other three are positive." % (
            cap(sit(k, -m)), sit(k, m), n(-m))
        its.append(mcq(q, sit(k, -m), [sit(kk, mm) for kk, mm in poss], e, rnd))
    assert len(its) == 20
    return {"title": "Integers in everyday life", "items": its}


# ============================================================ set 2: integers on a number line
def e_read(nl, v, near, name="A"):
    """Explain reading point A at v from the nearest label `near`."""
    k = int(abs(v - near) / nl.step)
    per = int(nl.lab / nl.step)
    t = "The labels count by %s, and there are %s between labels, so each tick mark is %s. " % (
        n(nl.lab), spaces(per), n(nl.step))
    if k == 0:
        return t + "Point %s is on the label: %s = <b>%s</b>." % (name, name, n(v))
    side = "left" if v < near else "right"
    return t + "Point %s is %s to the %s of %s, so %s = <b>%s</b>." % (name, ticks(k), side, n(near), name, n(v))


def letters_q(nl, values, correct_idx, letter_pos):
    """Put the 4 values on the line with letters A-D so that values[correct_idx] gets letter_pos."""
    order = [i for i in range(4) if i != correct_idx]
    lets = {}
    others = [l for l in range(4) if l != letter_pos]
    for i, l in zip(order, others):
        lets[i] = l
    lets[correct_idx] = letter_pos
    for i, v in enumerate(values):
        nl.point(v, "ABCD"[lets[i]])
    return lets


def set_read(rnd, P):
    its = []
    pos = Pos(rnd)
    # A: labels on every other tick (5)
    for v, R in [(-3, 6), (-5, 8), (-7, 8), (-1, 6), (-9, 10)]:
        nl = NL(-R, R, 1, 2).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What integer is at point A?"
        e = e_read(nl, v, v + 1) + " A is to the left of 0, so it is negative."
        its.append(mcq_v(q, v, [-v, v + 1, v - 1, -(v + 1)], e, rnd))
    # B: labels every 5 (5)
    for v in [-7, -3, -8, -6, -4]:
        nl = NL(-10, 10, 1, 5).point(v, "A")
        near = 5 * round(v / 5.0)
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What integer is at point A?"
        e = e_read(nl, v, near)
        near0 = 5 * int(v / 5.0)                         # the label between A and 0
        mirror = 2 * near0 - v                           # counted the ticks the wrong way from that label
        if near0 == 0:
            e += " Count left from 0, not right."
        else:
            e += " Count left from %s: the numbers get smaller as you go left." % n(near0)
        its.append(mcq_v(q, v, [mirror, -v, v + 1, v - 1], e, rnd))
    # C: scale counts by 2, 5 or 10 (4)
    for lo, hi, st, lab, v in [(-10, 10, 2, 10, -6), (-25, 25, 5, 25, -15), (-50, 50, 10, 50, -30), (-25, 25, 5, 25, -20)]:
        nl = NL(lo, hi, st, lab).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What integer is at point A?"
        k = abs(v) // st
        e = ("There are %s between 0 and %s, so each tick mark is %s ÷ %d = %d. "
             "Point A is %s to the left of 0: %s. A = <b>%s</b>. (Counting each tick as 1 gives %s.)"
             % (spaces(lab // st), n(lab), n(lab), lab // st, st, ticks(k),
                ", ".join(n(-st * i) for i in range(1, k + 1)), n(v), n(-k)))
        its.append(mcq_v(q, v, [-k, -v, v + st, v - st], e, rnd))
    # D: which point is at ... (4)
    for v, R in [(-5, 6), (-3, 6), (-7, 8), (-2, 6)]:
        nl = NL(-R, R, 1, 2)
        vals = [v, -v, v + 1, v - 1]
        lp = pos.next()
        letters_q(nl, vals, 0, lp)
        q = fig(nl.svg(nl_label(nl, "with points A, B, C and D"))) + "Which point is at %s?" % n(v)
        e = ("%s is %d units to the left of 0. Point %s is there. The point at %s is to the right of 0."
             % (n(v), abs(v), "ABCD"[lp], n(-v)))
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], "ABCD"[lp], e))
    # E: thermometers (2)
    for lo, hi, st, lab, v, place in [(-10, 10, 2, 10, -4, "Perisher"), (-15, 15, 5, 15, -10, "Thredbo")]:
        q = fig(thermo_svg(lo, hi, st, lab, v)) + "A thermometer at %s shows this temperature. What is it?" % place
        k = abs(v) // st
        e = ("There are %s between 0 and %s, so each tick mark is %d degrees. The red column ends %s below 0: %s. "
             "The temperature is <b>%s</b>." % (spaces(lab // st), n(lab), st, ticks(k),
                                                  ", ".join(n(-st * i) for i in range(1, k + 1)), deg(v)))
        its.append(mcq(q, (deg(v), v), [(deg(-v), -v), (deg(-k), -k), (deg(v + st), v + st), (deg(v - st), v - st)], e, rnd))
    assert len(its) == 20
    return {"title": "Integers on a number line", "items": its}


# ============================================================ set 3: compare and order
def set_compare(rnd, P):
    its = []
    # A: the greatest (5)
    for vals in [[-6, 2, -9, -1], [-3, -8, -1, -6], [-12, -5, -9, -2], [-4, 0, -7, -10], [-15, -11, -20, -13]]:
        big = max(vals)
        q = "Which integer is the greatest? " + lst(vals)
        e = ("The greatest number is the one farthest to the right on a number line. ")
        negs = [v for v in vals if v < 0]
        if big < 0:
            e += ("All four are negative, so the one closest to 0 is the greatest: <b>%s</b>. "
                  "%s is the smallest even though %d is the biggest digit." % (n(big), n(min(vals)), -min(vals)))
        else:
            e += "%s is the farthest right, so it is the greatest: <b>%s</b>." % (n(big), n(big))
            if big == 0:
                e += " 0 is greater than every negative number."
        its.append(mcq_v(q, big, [v for v in sorted(vals, key=lambda x: -abs(x)) if v != big], e, rnd))
    # B: the smallest (5)
    for vals in [[-2, 1, -9, -5], [-3, -1, 0, 2], [-14, -8, -17, -11], [4, -4, -6, 6], [-7, -2, -10, -5]]:
        sm = min(vals)
        q = "Which integer is the smallest? " + lst(vals)
        e = ("The smallest number is the one farthest to the left on a number line. %s is the farthest left: <b>%s</b>."
             % (n(sm), n(sm)))
        others = sorted([v for v in vals if v < 0 and v != sm], key=lambda x: -x)
        if others:
            e += " %s is greater than %s because it is closer to 0." % (n(others[0]), n(sm))
        its.append(mcq_v(q, sm, [v for v in sorted(vals, key=lambda x: abs(x)) if v != sm], e, rnd))
    # C: which statement is true (4)
    def lt(a, b):
        return "%s &lt; %s" % (n(a), n(b))

    def gt(a, b):
        return "%s &gt; %s" % (n(a), n(b))
    stmts = [
        (lt(-7, -2), [gt(-7, -2), lt(-2, -7), gt(-5, 0)], -7, -2),
        (gt(-3, -10), [lt(-3, -10), gt(-10, -3), gt(-1, 1)], -10, -3),
        (gt(0, -6), [lt(0, -6), gt(-6, 0), gt(-6, -4)], -6, 0),
        (lt(-12, -11), [gt(-12, -11), lt(-11, -12), gt(-20, -2)], -12, -11),
    ]
    for right, wrongs, a, b in stmts:
        assert a < b
        q = "Which statement is true?"
        e = ("%s is to the left of %s on a number line, so %s is smaller: <b>%s</b>. "
             "Do not compare the digits only: %d &gt; %d, but %s &lt; %s."
             % (n(a), n(b), n(a), right, abs(a), abs(b), n(a), n(b))) if (a < 0 and b < 0) else \
            ("%s is to the left of %s on a number line, so %s is smaller: <b>%s</b>. Every negative number is less than 0."
             % (n(a), n(b), n(a), right))
        its.append(mcq(q, right, wrongs, e, rnd))
    # D: order from smallest to largest (4)
    for vals in [[-2, 3, -8, -5], [-1, -6, 4, 0], [5, -9, -3, 1], [-4, 7, -10, -7]]:
        asc = sorted(vals)
        right = lst(asc)
        by_abs = lst(sorted(vals, key=abs))                    # ignored the signs
        desc = lst(sorted(vals, reverse=True))                 # largest first
        neg_wrong = lst(sorted([v for v in vals if v < 0], reverse=True) + sorted(v for v in vals if v >= 0))
        q = "Which list is in order from smallest to largest? " + lst(vals)
        e = ("Start with the number farthest left on a number line. The negative number with the biggest digits is the smallest: "
             "<b>%s</b>." % right)
        its.append(mcq(q, right, [neg_wrong, by_abs, desc], e, rnd))
    # E: between (2)
    its.append(mcq_v("How many integers are between " + M + "3 and 2? (Do not count " + M + "3 or 2.)", 4, [3, 5, 6],
                     "List them: " + M + "2, " + M + "1, 0, 1. That is <b>4</b> integers. Do not forget 0: it is an integer too.",
                     rnd))
    its.append(mcq_v("Which integer is between " + M + "6 and " + M + "2 on a number line?", -4, [4, -7, -1],
                     M + "6 and " + M + "2 are both to the left of 0. The integers between them are " + M + "5, " + M + "4 and "
                     + M + "3, so the answer is <b>" + M + "4</b>. 4 is to the right of 0, so it is not between them.", rnd))
    assert len(its) == 20
    return {"title": "Compare and order integers", "items": its}


# ============================================================ set 4: count on and back across zero
def path(a, b):
    d = 1 if b > a else -1
    return ", ".join(n(v) for v in range(a + d, b + d, d))


def count_cands(s, d, up):
    """Wrong answers for counting d steps from s (up = to the right)."""
    r = s + d if up else s - d
    cross = (s < 0 < r) or (r < 0 < s)
    skip = (r + 1 if up else r - 1) if cross else None   # skipped 0
    start = r - 1 if up else r + 1                     # counted the start as a step
    wrongway = s - d if up else s + d
    return r, [skip, wrongway, -r, start]


def set_count(rnd, P):
    its = []
    # A: count on (5)
    for s, d in [(-4, 7), (-6, 8), (-2, 7), (-9, 13), (-3, 4)]:
        r, c = count_cands(s, d, True)
        q = "Start at %s on a number line. Count on %d. Where do you land?" % (n(s), d)
        e = ("Counting on moves to the right. From %s to 0 is %s, then %s more: %s. You land on <b>%s</b>. "
             "Count 0 as a step." % (n(s), steps(-s), steps(d + s), path(s, r), n(r)))
        its.append(mcq_v(q, r, c, e, rnd))
    # B: count back (5)
    for s, d in [(3, 7), (5, 8), (2, 6), (1, 9), (4, 11)]:
        r, c = count_cands(s, d, False)
        q = "Start at %s on a number line. Count back %d. Where do you land?" % (n(s), d)
        e = ("Counting back moves to the left. From %s to 0 is %s, then %s more: %s. You land on <b>%s</b>. "
             "Count 0 as a step." % (n(s), steps(s), steps(d - s), path(s, r), n(r)))
        its.append(mcq_v(q, r, c, e, rnd))
    # C: temperatures rise and fall (5)
    temps = [("At 5 am in Thredbo, the temperature was %s. By 11 am, it had risen %d degrees.", -5, 8, True),
             ("In Canberra, the temperature was %s at 9 pm. Overnight, it fell %d degrees.", 4, 7, False),
             ("At Perisher, the temperature was %s at dawn. By lunchtime, it had risen %d degrees.", -7, 4, True),
             ("At Falls Creek, the temperature was %s at 4 pm. By midnight, it had fallen %d degrees.", 2, 6, False),
             ("On Mount Hotham, the temperature was %s at 6 am. By 1 pm, it had risen %d degrees.", -8, 10, True)]
    for txt, s, d, up in temps:
        r, c = count_cands(s, d, up)
        q = (txt % (deg(s), d)) + " What was the new temperature?"
        way = "Rising means counting up" if up else "Falling means counting down"
        e = "%s %d degrees from %s: %s. The new temperature is <b>%s</b>." % (way, d, deg(s), path(s, r), deg(r))
        if (s < 0 < r) or (r < 0 < s):
            e += " Do not skip 0" + NBSP + "°C."
        its.append(mcq(q, (deg(r), r), [(deg(x), x) for x in c if x is not None], e, rnd))
    # D: how many steps between (5)
    gaps = [("How many steps is it from %s to %s on a number line?", -5, 3, None),
            ("How many degrees warmer is %s than %s?", 4, -3, "deg"),
            ("How many steps is it from %s to %s on a number line?", -2, 7, None),
            ("How many degrees warmer is %s than %s?", 4, -9, "deg"),
            ("The temperature fell from %s to %s. How many degrees did it fall?", 6, -5, "deg")]
    for txt, a, b, u in gaps:
        lo, hi = min(a, b), max(a, b)
        d = hi - lo
        shown = (deg(a), deg(b)) if u else (n(a), n(b))
        q = txt % shown
        e = ("From %s up to 0 is %d. From 0 to %s is %d. %d + %d = <b>%d</b>. "
             "(Taking away the digits, %d %s %d, ignores the signs.)"
             % (n(lo), -lo, n(hi), hi, -lo, hi, d, max(hi, -lo), M, min(hi, -lo)))
        its.append(mcq_v(q, d, [abs(hi + lo), d - 1, d + 1], e, rnd))
    assert len(its) == 20
    return {"title": "Count on and back across zero", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    # 1: two money situations
    a, b = P.next(), P.next()
    q = ("%s has $20 saved. %s owes %s mum $15. Which pair of integers shows %s’s and %s’s money, in order?"
         % (a[0], b[0], b[2], a[0], b[0]))
    e = "Money saved is positive and money owed is negative: %s 20, %s %s15. <b>20 and %s15</b>." % (a[0], b[0], M, M)
    its.append(mcq(q, "20 and " + M + "15", [M + "20 and 15", "20 and 15", M + "20 and " + M + "15"], e, rnd))
    # 2: negative balance
    nm, he, his = P.next()
    q = "%s’s bank account balance is %s. What does this mean?" % (nm, money(-40))
    e = "A balance of $0 means no money and nothing owed. A negative balance means money is owed: <b>%s owes the bank $40</b>." % nm
    its.append(mcq(q, "%s owes the bank $40." % nm, ["%s has $40 in the account." % nm, "%s has $0 in the account." % nm,
                                                     "%s put $40 into the account." % nm], e, rnd))
    # 3: balance goes below zero
    nm, he, his = P.next()
    q = ("%s has $25 in %s bank account. %s pays a $40 bill, and the bank lets the balance go below zero. "
         "What is the balance now?" % (nm, his, he.capitalize()))
    e = "Count back 40 from 25: 25 takes you to $0, then 15 more takes you to " + M + "$15. The balance is <b>" + M + "$15</b> (owing $15)."
    its.append(mcq(q, (money(-15), -15), [(money(15), 15), (money(-65), -65), (money(65), 65)], e, rnd))
    # 4: deposit brings it back above zero
    nm, he, his = P.next()
    q = "%s’s bank balance is %s. %s puts in $50 from %s birthday money. What is the balance now?" % (
        nm, money(-30), he.capitalize(), his)
    e = "Count on 50 from " + M + "30: 30 takes you to $0, then 20 more. The balance is <b>$20</b>."
    its.append(mcq(q, (money(20), 20), [(money(-20), -20), (money(80), 80), (money(-80), -80)], e, rnd))
    # 5: who owes the most
    people = [P.next()[0] for _ in range(4)]
    bal = [-12, -45, 8, -30]
    q = ("Four students wrote their bank balances: " + ", ".join("%s %s" % (p, money(v)) for p, v in zip(people, bal)) +
         ". Who owes the most money?")
    e = ("The balance farthest below $0 shows the most money owed. " + money(-45) + " is less than " + money(-30) +
         " and " + money(-12) + ", so <b>%s</b> owes the most." % people[1])
    its.append(mcq(q, people[1], [people[0], people[2], people[3]], e, rnd))
    # 6: paying back part of a debt
    nm, he, his = P.next()
    q = "%s owes a friend $12. %s pays back $8. Which integer shows %s money situation now, in dollars?" % (
        nm, he.capitalize(), his)
    e = "Owing $12 is " + M + "12. Paying back $8 moves 8 towards 0: " + M + "12 to " + M + "4. %s still owes $4: <b>%s4</b>." % (
        he.capitalize(), M)
    its.append(mcq_v(q, -4, [4, -20, 20], e, rnd))
    # 7: sea level facts
    q = ("Mount Kosciuszko is 2228 m above sea level. Kati Thanda–Lake Eyre is about 15 m below sea level. "
         "Which pair of integers shows their heights, in order?")
    e = "Above sea level is positive and below sea level is negative: <b>2228 and " + M + "15</b>."
    its.append(mcq(q, "2228 and " + M + "15", [M + "2228 and 15", "2228 and 15", M + "2228 and " + M + "15"], e, rnd))
    # 8: diver swims up
    nm, he, his = P.next()
    q = "%s is snorkelling at %s. %s swims up 5 m. What integer shows %s new position?" % (nm, metres(-12), he.capitalize(), his)
    e = "Up means counting towards 0: " + path(-12, -7) + ". %s is now at <b>%s</b>, still below sea level." % (nm, metres(-7))
    its.append(mcq(q, (metres(-7), -7), [(metres(-17), -17), (metres(7), 7), (metres(-6), -6)], e, rnd))
    # 9: coldest morning
    days = [("Monday", -6), ("Tuesday", -2), ("Wednesday", 0), ("Thursday", -9)]
    q = ("These were the 6 am temperatures in Thredbo one week in July: " +
         ", ".join("%s %s" % (d, deg(t)) for d, t in days) + ". Which morning was the coldest?")
    e = "The coldest temperature is the one farthest below 0. " + deg(-9) + " is colder than " + deg(-6) + ", so <b>Thursday</b> was the coldest."
    its.append(mcq(q, "Thursday", ["Monday", "Tuesday", "Wednesday"], e, rnd))
    # 10: order cities
    cities = [("Canberra", -4), ("Thredbo", -9), ("Hobart", 2), ("Sydney", 8)]
    q = ("At 6 am one July morning: " + ", ".join("%s %s" % (c, deg(t)) for c, t in cities) +
         ". Which list goes from coldest to warmest?")
    e = ("Coldest means farthest left on a number line: " + deg(-9) + ", " + deg(-4) + ", " + deg(2) + ", " + deg(8) +
         ". <b>Thredbo, Canberra, Hobart, Sydney</b>. " + deg(-9) + " is colder than " + deg(-4) + ".")
    its.append(mcq(q, "Thredbo, Canberra, Hobart, Sydney",
                   ["Canberra, Thredbo, Hobart, Sydney", "Sydney, Hobart, Canberra, Thredbo", "Hobart, Canberra, Sydney, Thredbo"],
                   e, rnd))
    # 11: car park lift (picture)
    nm, he, his = P.next()
    q = fig(floors_svg(-3, 4, -2, "car")) + ("%s parks on the level marked “car”. %s takes the lift up 5 levels to the cinema. "
                                             "Which level is the cinema on?" % (nm, he.capitalize()))
    e = ("The car is on level " + M + "2. Count up 5 levels: " + path(-2, 3) + ". The cinema is on level <b>3</b>. "
         "Level 0 (the ground floor) counts as a level.")
    its.append(mcq_v(q, 3, [4, -7, -3], e, rnd))
    # 12: lift down
    nm, he, his = P.next()
    q = "%s is on level 3 of a hospital. %s takes the lift down 5 levels to the car park. Which level is the car park?" % (
        nm, he.capitalize())
    e = "Count down 5 levels from 3: " + path(3, -2) + ". The car park is on level <b>" + M + "2</b>. Do not skip level 0."
    its.append(mcq_v(q, -2, [-3, 8, 2], e, rnd))
    # 13: temperature fall
    q = "In Canberra, the temperature was " + deg(2) + " at 6 pm and " + deg(-5) + " at 3 am. How many degrees did it fall?"
    e = "From 2 down to 0 is 2 degrees. From 0 down to " + M + "5 is 5 degrees. 2 + 5 = <b>7 degrees</b>."
    its.append(mcq(q, "7 degrees", ["3 degrees", "6 degrees", "8 degrees"], e, rnd))
    # 14: record low
    q = ("The lowest temperature ever recorded in Australia is " + deg(-23) + ", at Charlotte Pass in New South Wales. "
         "One winter morning in Canberra was " + deg(-5) + ". How many degrees colder is the record?")
    e = ("Both are below 0. From " + M + "5 down to " + M + "23 is 23 " + M + " 5 = <b>18 degrees</b>. "
         "Do not add 23 and 5: both temperatures are on the same side of 0.")
    its.append(mcq(q, "18 degrees", ["28 degrees", "19 degrees", "23 degrees"], e, rnd))
    # 15: golf
    a, b = P.next(), P.next()
    q = "In golf, par is 0. %s finished 4 strokes under par. %s finished 1 stroke over par. Which integer shows %s’s score?" % (
        a[0], b[0], a[0])
    e = "Under par is negative and over par is positive. %s is 4 under par: <b>%s4</b>. (%s’s score is 1.)" % (a[0], M, b[0])
    its.append(mcq_v(q, -4, [4, 1, -1], e, rnd))
    # 16: freezer and fridge
    q = "A freezer is set to " + deg(-18) + ". The fridge is " + deg(4) + ". How many degrees colder is the freezer than the fridge?"
    e = "From 4 down to 0 is 4 degrees. From 0 down to " + M + "18 is 18 degrees. 4 + 18 = <b>22 degrees</b>."
    its.append(mcq(q, "22 degrees", ["14 degrees", "21 degrees", "23 degrees"], e, rnd))
    # 17: chores pay back a debt
    nm, he, his = P.next()
    q = ("%s owes %s dad $8. %s earns $5 doing chores and gives it all to %s dad. Which integer shows %s money situation now, in dollars?"
         % (nm, his, he.capitalize(), his, his))
    e = "Owing $8 is " + M + "8. Paying back $5 moves 5 towards 0: " + path(-8, -3) + ". %s still owes $3: <b>%s3</b>." % (
        he.capitalize(), M)
    its.append(mcq_v(q, -3, [3, -13, 13], e, rnd))
    # 18: compare two negative balances
    a, b = P.next(), P.next()
    q = "%s’s bank balance is %s. %s’s balance is %s. Which statement is true?" % (a[0], money(-20), b[0], money(-35))
    e = (M + "20 is closer to 0 than " + M + "35, so " + M + "20 &gt; " + M + "35. <b>%s has more money</b>: %s owes less." % (a[0], a[1]))
    its.append(mcq(q, "%s has more money: %s20 &gt; %s35." % (a[0], M, M),
                   ["%s has more money: %s35 &gt; %s20." % (b[0], M, M), "They have the same amount of money.",
                    "Neither of them owes any money."], e, rnd))
    # 19: gannet dives
    q = ("An Australasian gannet is flying 6 m above the sea. It dives down 9 m to catch a fish. "
         "What integer shows its position now, in metres compared with sea level?")
    e = "Count down 9 from 6: " + path(6, -3) + ". The gannet is at <b>" + M + "3 m</b>, 3 m below sea level."
    its.append(mcq(q, (metres(-3), -3), [(metres(-4), -4), (metres(15), 15), (metres(3), 3)], e, rnd))
    # 20: quiz score
    q = ("In a class quiz, a team starts on 0 points. They lose 3 points, win 5 points, then lose 4 points. "
         "What is their score now?")
    e = "0 back 3 is " + M + "3. On 5 is 2. Back 4 is " + M + "2. The score is <b>" + M + "2</b>."
    its.append(mcq_v(q, -2, [2, -12, 12], e, rnd))
    assert len(its) == 20
    return {"title": "Integers word problems", "items": its}


# ============================================================ lesson
def body_html():
    nl1 = NL(-10, 10, 2, 10).point(-6, "C")
    by2 = nl1.svg("number line from " + M + "10 to 10 counting by 2 with C at " + M + "6")
    nl2 = NL(-8, 2, 1, 1, gap=30).point(-7, "P").point(-2, "Q")
    cmp_ = nl2.svg("number line from " + M + "8 to 2 with P at " + M + "7 and Q at " + M + "2")
    nl3 = NL(-4, 3, 1, 1, gap=36).point(-3).point(2).hop(-3, 2, "5 steps")
    hop = nl3.svg("number line from " + M + "4 to 3 with 5 hops from " + M + "3 to 2")
    return (
        "<h2>What are integers?</h2>"
        "<p><b>Integers</b> are the whole numbers, their negatives and 0: … " + M + "3, " + M + "2, " + M + "1, 0, 1, 2, 3 … "
        "A negative number has a minus sign. " + M + "8 is read “negative 8”.</p>"
        "<p>Integers describe two opposite directions. <b>0</b> is the starting point between them. It is neither positive nor negative.</p>" +
        table(["Situation", "Positive", "0 means", "Negative"], [
            ["Temperature", "above zero: 12" + NBSP + "°C", "water freezes", "below zero: " + deg(-5)],
            ["Height", "above sea level: 2228 m", "sea level", "below sea level: " + M + "15 m"],
            ["Money", "saved: $20", "nothing saved or owed", "owing: " + money(-15)],
            ["Lift", "level 3", "ground floor", "car park: level " + M + "2"],
        ]) +
        ex("Example 1", "At 6 am in Thredbo, it is 4 degrees below zero. Which integer shows the temperature?",
           "“Below zero” is the negative direction.", deg(-4)) +
        "<h2>Integers on a number line</h2>"
        "<p>Positive integers are to the <b>right</b> of 0. Negative integers are to the <b>left</b>. "
        "Before you read a point, work out what each tick mark is worth.</p>"
        "<figure class='sn-fig'>" + by2 +
        "<figcaption>There are 5 spaces from 0 to 10, so each tick mark is 2. C is 3 tick marks left of 0: " + M + "2, " +
        M + "4, " + M + "6. So C = " + M + "6, not " + M + "3.</figcaption></figure>"
        "<h2>Compare and order integers</h2>"
        "<p>The farther <b>left</b> a number is, the <b>smaller</b> it is. So every negative number is less than 0, "
        "and " + M + "7 is less than " + M + "2.</p>"
        "<figure class='sn-fig'>" + cmp_ +
        "<figcaption>P (" + M + "7) is to the left of Q (" + M + "2), so " + M + "7 &lt; " + M + "2. "
        "7 is bigger than 2, but " + M + "7 is smaller than " + M + "2.</figcaption></figure>" +
        ex("Example 2", "Order from smallest to largest: 3, " + M + "5, 0, " + M + "8",
           "Start with the number farthest left. " + M + "8 is farther left than " + M + "5.",
           M + "8, " + M + "5, 0, 3") +
        "<h2>Count on and back across zero</h2>"
        "<p>Counting on (a rise, a deposit, going up) moves right. Counting back (a fall, spending, going down) moves left. "
        "When you pass 0, <b>0 counts as a step</b>.</p>"
        "<figure class='sn-fig'>" + hop +
        "<figcaption>The temperature is " + deg(-3) + " and rises 5 degrees: " + M + "2, " + M + "1, 0, 1, 2. "
        "The new temperature is " + deg(2) + ".</figcaption></figure>" +
        ex("Example 3", "Zara has $10 in her account. She pays a $25 bill, and the balance goes below zero. What is her balance?",
           "Count back 25 from 10: 10 takes you to $0, then 15 more.", money(-15) + " (she owes $15)") +
        "<p>Integers are also used as coordinates on the Cartesian plane, such as (" + M + "3, 2), where " + M +
        "3 means 3 units left of the origin.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing 15 for “owing $15”", "Owing, below zero, below sea level and spending are negative: " + M + "15"],
            [M + "7 &gt; " + M + "2 because 7 &gt; 2", "Farther left is smaller: " + M + "7 &lt; " + M + "2"],
            ["Counting each tick as 1 when the scale counts by 2 or 5", "Find the tick value first: label difference ÷ spaces"],
            ["Skipping 0: " + M + "3 up 5 is 3", "Count 0 as a step: " + M + "2, " + M + "1, 0, 1, 2"],
            ["From " + M + "3 to 4 is 1 step", "Go through 0: 3 steps to 0, then 4 more, so 7 steps"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about integers in the Australian Curriculum?",
     "a": "In Year 6 (AC9M6N01) students recognise situations that use integers, including money, and locate and represent integers on a number line and as coordinates on the Cartesian plane. Adding and subtracting integers comes in Year 7."},
    {"q": "How do you explain negative numbers to a Year 6 child?",
     "a": "Negative numbers show the opposite direction from 0, like below zero on a thermometer, below sea level or money you owe. On a number line they are to the left of 0."},
    {"q": "Is −7 bigger or smaller than −2?",
     "a": "−7 is smaller. It is farther left on the number line, just as −7 °C is colder than −2 °C, so −7 < −2."},
    {"q": "How do you count across zero on a number line?",
     "a": "Count one step at a time and include 0. From −3, counting on 5 goes −2, −1, 0, 1, 2, so you land on 2."},
]


def gen_unit():
    rnd = random.Random(6801)
    P = People(rnd)
    sets = [set_situations(rnd, P), set_read(rnd, P), set_compare(rnd, P), set_count(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "integers-and-negative-numbers", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Integers and Negative Numbers: Number Lines, Ordering and Counting across Zero",
        "seo_title": "Year 6 Integers Worksheets: Negative Numbers, Number Lines and Ordering (Free, Answer Key)",
        "short_title": "Integers",
        "domain": "Number",
        "standard_code": "AC9M6N01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise situations, including financial contexts, that use integers; locate and represent integers on a number line and as coordinates on the Cartesian plane",
        "meta_desc": "Free Year 6 maths worksheets on integers for the Australian Curriculum (AC9M6N01): negative numbers in temperatures, sea level and bank balances, reading number lines, comparing and ordering integers, and counting across zero. 100 questions with an answer key.",
        "key_big": "Negative numbers are to the left of 0, so −7 < −2.",
        "key_sub": "Below zero, below sea level and money owed are negative. The farther left on the number line, the smaller the number. When you count across zero, 0 counts as a step.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(number line|vertical|thermometer)")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
