# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Positive and Negative Numbers (6.NS.C.5, 6.NS.C.6a, 6.NS.C.6c)
  python tools/gen_us_math_g6_negative_numbers.py
HTML attributes use single quotes (no backslashes in the JSON).

Every number is a Fraction. Negative numbers use the real minus sign − (U+2212).
No integer arithmetic (that is Grade 7). Absolute value and ordering are a later unit, so
comparison only appears as “colder / farther below / farther left” in the word problems.
Number lines are drawn exactly: tick i sits at lo + i * step, labels only on the label marks.
Wrong answers come from real mistakes: the sign flipped, reading the tick on the wrong side of a
label, counting every tick as 1 when the scale counts by 2 or 5 (or by 0.25 as 0.1), confusing
“opposite” with “reciprocal”, −(−5) = −5, and counting tick marks instead of spaces.
"""
import json, os, random, re
from decimal import Decimal
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ numbers
def frh(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def dec(v):
    """Fraction -> '−2.5' (terminating decimals only)."""
    v = F(v)
    s = M if v < 0 else ""
    a = abs(v)
    if a.denominator == 1:
        return s + str(a.numerator)
    d = (Decimal(a.numerator) / Decimal(a.denominator))
    t = format(d.normalize(), "f")
    assert F(t) == a, (v, t)
    return s + t


def frc(v):
    """Fraction -> mixed number HTML: '−2 1/2' with a stacked fraction."""
    v = F(v)
    s = M if v < 0 else ""
    a = abs(v)
    w, r = divmod(a.numerator, a.denominator)
    if r == 0:
        return s + str(w)
    if w == 0:
        return s + frh(r, a.denominator)
    return "%s%d %s" % (s, w, frh(r, a.denominator))


def frp(v):
    """Plain text mixed number for aria labels: '−2 1/2'."""
    v = F(v)
    s = M if v < 0 else ""
    a = abs(v)
    w, r = divmod(a.numerator, a.denominator)
    if r == 0:
        return s + str(w)
    if w == 0:
        return "%s%d/%d" % (s, r, a.denominator)
    return "%s%d %d/%d" % (s, w, r, a.denominator)


def fimp(v):
    """Fraction -> improper fraction HTML: '−4/3'."""
    v = F(v)
    if v.denominator == 1:
        return dec(v)
    return (M if v < 0 else "") + frh(abs(v.numerator), v.denominator)


def auto(v):
    """Decimal when it ends quickly, otherwise a fraction."""
    v = F(v)
    return dec(v) if v.denominator in (1, 2, 4, 5, 10) else fimp(v)


def money(v):
    v = F(v)
    return (M if v < 0 else "") + "$" + dec(abs(v))


def cnum(n):
    """Commas for numbers of 1,000 or more."""
    return "{:,}".format(n)


def times(n):
    return {1: "once", 2: "twice"}.get(n, "%d times" % n)


def spaces(n):
    return "1 space" if n == 1 else "%d spaces" % n


def ticks(n):
    return "1 tick mark" if n == 1 else "%d tick marks" % n


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e, rnd):
    """correct and cands: strings, or (string, value) pairs. A candidate equal in value to the
    correct answer or to an earlier candidate is skipped."""
    cs, cv = correct if isinstance(correct, tuple) else (correct, None)
    seen, vals, pick = {cs}, {cv} if cv is not None else set(), []
    for c in cands:
        if c is None:
            continue
        s, v = c if isinstance(c, tuple) else (c, None)
        if s in seen or not s:
            continue
        if v is not None:
            if v in vals:
                continue
            vals.add(v)
        seen.add(s)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq_v(q, v, cands, e, rnd, fmt=dec):
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
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
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


def cap(s):
    return s[0].upper() + s[1:]


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


# ------------------------------------------------------------ number line pictures
class NL:
    """Horizontal number line from lo to hi with a tick every `step` and a number under every
    multiple of `lab`. `mid`: optional medium ticks (for example every 0.5 on a tenths line)."""

    def __init__(self, lo, hi, step, lab, gap=None, mid=None):
        lo, hi, step, lab = F(lo), F(hi), F(step), F(lab)
        n = (hi - lo) / step
        assert n.denominator == 1 and (lab / step).denominator == 1
        self.lo, self.hi, self.step, self.lab, self.mid = lo, hi, step, lab, (F(mid) if mid else None)
        self.n = int(n)
        self.labels = [lo + i * step for i in range(self.n + 1) if ((lo + i * step) / lab).denominator == 1]
        lw = max(tw(dec(v), 14) for v in self.labels)
        self.g = gap or max(12, min(30, int(360 / self.n)))
        assert (lab / step) * self.g >= lw + 6, ("labels overlap", lo, hi, step, lab, self.g)
        self.pad = int(max(26, lw / 2 + 8))
        self.W = int(2 * self.pad + self.n * self.g)
        self.Y = 40
        self.H = 72
        self.pts, self.extra, self.top = [], [], 0

    def X(self, v):
        k = (F(v) - self.lo) / self.step
        return self.pad + float(k) * self.g

    def point(self, v, name=None, col=GREEN):
        assert self.lo <= F(v) <= self.hi and ((F(v) - self.lo) / self.step).denominator == 1, v
        self.pts.append((F(v), name, col))
        return self

    def brace(self, a, b, label):
        """Bracket above the line from a to b with a label (lesson pictures)."""
        x1, x2 = self.X(a), self.X(b)
        y = 22
        self.extra.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='1.5'/>"
                          % (x1, y + 6, y, x2, y + 6, GRAY))
        self.extra.append(text((x1 + x2) / 2, y - 4, label, 14, col=GRAY))
        self.top = 12
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
            md = self.mid is not None and (v / self.mid).denominator == 1
            h = 9 if big else (7 if md else 5)
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                     % (x, Y - h, x, Y + h, INK, "1.8" if big else "1.2"))
            if big:
                s.append(text(x, Y + 26, dec(v), 14, bold=(v == 0)))
        xs = sorted(self.X(v) for v, nm, c in self.pts if nm)
        assert all(b - a >= 16 for a, b in zip(xs, xs[1:])), ("letters overlap", label)
        for v, nm, col in self.pts:
            x = self.X(v)
            s.append("<circle cx='%.1f' cy='%d' r='5.5' fill='%s'/>" % (x, Y, col))
            if nm:
                s.append(text(x, Y - 13, nm, 16, bold=True, col=col))
        s += self.extra
        return svg_wrap(self.W, H, "".join(s), label)


def nl_label(nl, what):
    return "number line from %s to %s %s" % (dec(nl.lo), dec(nl.hi), what)


def thermo_svg(lo, hi, step, lab, val, unit="°F"):
    """Thermometer with a scale on the left; the red column ends at val."""
    lo, hi, step, lab, val = F(lo), F(hi), F(step), F(lab), F(val)
    n = int((hi - lo) / step)
    g = 16
    top = 16
    x = 74
    Yv = lambda v: top + float((hi - v) / step) * g
    bot = Yv(lo)
    s = ["<rect x='%d' y='%d' width='14' height='%.1f' rx='7' fill='#ffffff' stroke='%s' stroke-width='1.6'/>"
         % (x - 7, top - 8, bot - top + 16, INK)]
    s.append("<circle cx='%d' cy='%.1f' r='12' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, bot + 18, RED, INK))
    s.append("<rect x='%d' y='%.1f' width='6' height='%.1f' fill='%s'/>" % (x - 3, Yv(val), bot + 14 - Yv(val), RED))
    for i in range(n + 1):
        v = lo + i * step
        y = Yv(v)
        big = (v / lab).denominator == 1
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x - 9 - (8 if big else 4), y, x - 9, y, INK, "1.6" if big else "1.1"))
        if big:
            s.append(text(x - 22, y + 5, dec(v), 14, anchor="end", bold=(v == 0)))
    s.append(text(x + 14, top + 4, unit, 14, anchor="start"))
    H = int(bot + 34)
    return svg_wrap(110, H, "".join(s), "thermometer from %s to %s %s counting by %s" % (dec(lo), dec(hi), unit, dec(step)))


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
        s.append(text(x - 14, y + 5, dec(v), 14, anchor="end", bold=(v == 0)))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#e7efe9'/>" % (x + 14, Yv(0) - 1, 120, 2))
    s.append(text(x + 16, Yv(0) - 6, "ground floor", 14, anchor="start", col=GRAY))
    s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (x, Yv(val), GREEN))
    s.append(text(x + 16, Yv(val) + 5, mark, 15, anchor="start", bold=True, col=GREEN))
    return svg_wrap(190, int(Yv(lo) + 16), "".join(s),
                    "vertical number line of building levels from %d to %d" % (lo, hi))


# ============================================================ set 1: real-world situations
# (positive phrase, negative phrase, what 0 means) - {n} is the size
SIT = {
    "temp": ("{n} degrees above zero", "{n} degrees below zero"),
    "sea": ("{n} feet above sea level", "{n} feet below sea level"),
    "bank": ("a deposit of ${n}", "a withdrawal of ${n}"),
    "yards": ("a gain of {n} yards", "a loss of {n} yards"),
    "floors": ("{n} floors above ground level", "{n} floors below ground level"),
    "points": ("earning {n} points", "losing {n} points"),
    "golf": ("{n} strokes over par", "{n} strokes under par"),
    "money": ("earning ${n}", "spending ${n}"),
}


def sit(kind, v):
    p, n = SIT[kind]
    return (p if v > 0 else n).format(n=abs(v))


def two_story(kind, a, b, P):
    """A story with two signed quantities a (first) and b (second). Returns (text, names of a, b)."""
    nm, he, his = P.next()
    if kind == "temp":
        return ("At 6 a.m. in Duluth, the temperature was %s. By 3 p.m., it was %s." % (sit("temp", a), sit("temp", b)),
                "the temperature at 6 a.m.", "the temperature at 3 p.m.")
    if kind == "sea":
        return ("A submarine is %s. A helicopter flies %s." % (sit("sea", a), sit("sea", b)),
                "the submarine’s position", "the helicopter’s position")
    if kind == "bank":
        return ("%s’s bank account changed twice. On Monday, %s made %s. On Friday, %s made %s."
                % (nm, he, sit("bank", a), he, sit("bank", b)),
                "the Monday change to the account", "the Friday change to the account")
    if kind == "yards":
        team = "Hawks" if abs(a) > abs(b) else "Bears"
        return ("On the first play, the %s had %s. On the next play, they had %s." % (team, sit("yards", a), sit("yards", b)),
                "the first play", "the second play")
    if kind == "floors":
        return ("In a hotel, the pool is %s. The gym is %s." % (sit("floors", a), sit("floors", b)),
                "the floor of the pool", "the floor of the gym")
    if kind == "golf":
        nm2 = P.next()[0]
        return ("In a golf game, %s finished %s and %s finished %s." % (nm, sit("golf", a), nm2, sit("golf", b)),
                "%s’s score compared with par" % nm, "%s’s score compared with par" % nm2)
    raise ValueError(kind)


NEGWORD = {"temp": "below zero", "sea": "below sea level", "bank": "a withdrawal", "yards": "a loss",
           "floors": "below ground level", "points": "points taken away", "golf": "under par", "money": "spending"}
POSWORD = {"temp": "above zero", "sea": "above sea level", "bank": "a deposit", "yards": "a gain",
           "floors": "above ground level", "points": "points added", "golf": "over par", "money": "earning"}
ZERO = {"temp": "0 degrees", "sea": "sea level", "bank": "no change to the account", "yards": "no gain and no loss",
        "floors": "ground level", "points": "no change to the score", "golf": "par", "money": "no change"}


def set_situations(rnd, P):
    its = []
    # A: a story with two quantities; write one of them as a signed number (8)
    plan = [("temp", -9, 14, 0), ("sea", -240, 600, 0), ("bank", 35, -20, 1), ("yards", 12, -7, 1),
            ("floors", -2, 5, 0), ("golf", 3, -2, 1), ("bank", -60, 45, 0), ("yards", 6, -15, 0)]
    for kind, a, b, ask in plan:
        story, na, nb = two_story(kind, a, b, P)
        v, w, nv = (a, b, na) if ask == 0 else (b, a, nb)
        q = story + " Which number represents %s?" % nv
        word = NEGWORD[kind] if v < 0 else POSWORD[kind]
        e = ("“%s” is the %s direction, so the number is <b>%s</b>. Here, 0 would mean %s."
             % (cap(word), "negative" if v < 0 else "positive", dec(v), ZERO[kind]))
        its.append(mcq_v(q, v, [-v, w, -w], e, rnd))
    # B: what 0 means (5)
    zero = [
        ("Elevation is measured in feet above or below sea level. What does an elevation of 0 feet mean?",
         "exactly at sea level", ["at the bottom of the ocean", "at the top of a mountain", "there is no elevation"],
         "Above sea level is positive and below sea level is negative. 0 is the starting point between them: <b>exactly at sea level</b>."),
        ("A thermometer shows degrees Celsius (°C). What does 0°C mean?",
         "the temperature at which water freezes", ["no temperature at all", "the coldest temperature possible",
                                                    "the temperature at which water boils"],
         "On the Celsius scale, water freezes at 0°C. Temperatures colder than that are negative, so 0°C is not the coldest possible: <b>water freezes at 0°C</b>."),
        ("In football, a gain of yards is positive and a loss of yards is negative. What does a change of 0 yards mean?",
         "no gain and no loss", ["a loss of 10 yards", "the team scored", "the ball went to the other team"],
         "0 is between gaining and losing. A change of 0 yards means the ball ended where the play started: <b>no gain and no loss</b>."),
        ("In an elevator, floors below the ground floor are negative. What does floor 0 mean?",
         "the ground floor", ["the top floor", "the lowest parking level", "a floor that does not exist"],
         "Floors above ground are positive and floors below are negative. 0 is the level between them: <b>the ground floor</b>."),
        ("An object can have a positive or a negative electric charge. What does a charge of 0 mean?",
         "it is neutral (no overall charge)", ["it has a very large charge", "it has a negative charge",
                                               "it has a positive charge"],
         "Positive and negative charges balance out at 0. An object with a charge of 0 is <b>neutral</b>."),
    ]
    for q, c, w, e in zero:
        its.append(mcq(q, c, w, e, rnd))
    # C: which situation could a negative number represent (4)
    for kind, n, others in [("bank", 18, ["sea", "yards"]), ("yards", 9, ["bank", "temp"]),
                            ("sea", 40, ["temp", "floors"]), ("temp", 5, ["golf", "bank"])]:
        q = "Which situation could the number %s represent?" % dec(-n)
        e = ("A negative number shows the direction that is %s. %s matches %s. The other choices are positive."
             % ("below or less than 0", cap(sit(kind, -n)), dec(-n)))
        its.append(mcq(q, sit(kind, -n), [sit(kind, n), sit(others[0], n), sit(others[1], n)], e, rnd))
    # D: which would be written as a negative number (3)
    for neg, poss in [(("money", 12), [("bank", 12), ("temp", 12), ("points", 12)]),
                      (("golf", 4), [("floors", 4), ("yards", 4), ("sea", 4)]),
                      (("floors", 3), [("golf", 3), ("money", 3), ("temp", 3)])]:
        k, n = neg
        q = "Which of these would be written as a negative number?"
        e = "%s is the opposite of %s, so it is written as %s. The other three are positive." % (
            cap(sit(k, -n)), sit(k, n), dec(-n))
        its.append(mcq(q, sit(k, -n), [sit(kk, nn) for kk, nn in poss], e, rnd))
    return {"title": "Positive and negative numbers in real life", "items": its}


# ============================================================ set 2: integers on a number line
def e_read(nl, v, near, name="A"):
    """Explain reading point A at v from the nearest label `near`."""
    k = int(abs(v - near) / nl.step)
    side = "left" if v < near else "right"
    per = nl.lab / nl.step
    t = "The labels count by %s, and there are %s between labels, so each tick mark is %s. " % (
        dec(nl.lab), spaces(int(per)), dec(nl.step))
    return t + "Point %s is %s to the %s of %s, so %s = <b>%s</b>." % (name, ticks(k), side, dec(near), name, dec(v))


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
    # A: labels on every other tick (6)
    for v, R in [(-3, 6), (-5, 8), (-7, 8), (-1, 6), (5, 6), (-9, 10)]:
        nl = NL(-R, R, 1, 2).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What number is at point A?"
        near = v + 1
        e = e_read(nl, v, near)
        if v < 0:
            e += " Do not drop the minus sign: A is to the left of 0."
        its.append(mcq_v(q, v, [-v, v + 1, v - 1, -(v + 1)], e, rnd))
    # B: labels every 5 (6)
    for v in [-7, -3, -8, -6, 4, -9]:
        nl = NL(-10, 10, 1, 5).point(v, "A")
        near = 5 * round(v / 5)
        if near == 0 and v < 0:
            near = 0
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What number is at point A?"
        e = e_read(nl, v, near)
        near0 = 5 * int(v / 5)                           # the label between A and 0
        mirror = 2 * near0 - v                           # counted the ticks the wrong way from that label
        its.append(mcq_v(q, v, [mirror, -v, v + 1, v - 1], e, rnd))
    # C: scale counts by 2 or 5 (4)
    for lo, hi, st, lab, v in [(-10, 10, 2, 10, -6), (-25, 25, 5, 25, -15), (-10, 10, 2, 10, -4), (-25, 25, 5, 25, -20)]:
        nl = NL(lo, hi, st, lab).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What number is at point A?"
        k = abs(v) // st
        e = ("There are %s between 0 and %s, so each tick mark is %s ÷ %d = %d. "
             "Point A is %s to the left of 0: %s. A = <b>%s</b>."
             % (spaces(int(lab / st)), dec(lab), dec(lab), int(lab / st), st, ticks(k),
                ", ".join(dec(-st * i) for i in range(1, k + 1)), dec(v)))
        its.append(mcq_v(q, v, [-k, -v, v + st, v - st], e, rnd))
    # D: which point is at ... (4)
    for v, R in [(-5, 6), (-3, 6), (-7, 8), (-1, 6)]:
        nl = NL(-R, R, 1, 2)
        vals = [v, -v, v + 1, v - 1]
        lp = pos.next()
        letters_q(nl, vals, 0, lp)
        q = fig(nl.svg(nl_label(nl, "with points A, B, C and D"))) + "Which point is at %s?" % dec(v)
        e = ("%s is %d unit%s to the left of 0. Point %s is there. The point at %s is to the right of 0."
             % (dec(v), abs(v), "" if abs(v) == 1 else "s", "ABCD"[lp], dec(-v)))
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], "ABCD"[lp], e))
    return {"title": "Read integers on a number line", "items": its}


# ============================================================ set 3: opposites
def set_opposites(rnd, P):
    its = []
    pos = Pos(rnd)
    # A: the opposite of a number (5)
    for v, fmt in [(F(9), None), (F(-14), None), (F(3, 4), fimp), (F(-5, 2), dec), (F(0), None)]:
        if v == 0:
            q = "What is the opposite of 0?"
            e = "The opposite of a number is the same distance from 0 on the other side. 0 is 0 units from itself, so the opposite of 0 is <b>0</b>."
            its.append(mcq(q, "0", ["1", M + "1", "0 has no opposite"], e, rnd))
            continue
        fmt = fmt or auto
        q = "What is the opposite of %s?" % fmt(v)
        e = ("The opposite is the same distance from 0, on the other side of 0. Change the sign: the opposite of %s is <b>%s</b>. "
             "(Flipping the number to %s gives the reciprocal, not the opposite.)" % (fmt(v), fmt(-v), fmt(1 / v)))
        its.append(mcq_v(q, -v, [v, 1 / v, -1 / v], e, rnd, fmt))
    # B: the opposite of the opposite (5)
    for expr, v, inner in [(M + "(" + M + "7)", 7, -7), ("the opposite of the opposite of 11", 11, 11),
                           (M + "(" + M + "2.5)", F(5, 2), F(-5, 2)), ("the opposite of the opposite of " + M + "6", -6, -6),
                           (M + "(" + M + "(" + M + "4))", -4, None)]:
        v = F(v)
        q = "What is %s?" % expr
        if inner is None:
            e = ("Work from the inside: %s(%s4) = 4, and the opposite of 4 is %s4. Three minus signs: <b>%s4</b>."
                 % (M, M, M, M))
            cands = [4, 0, -8]
        elif expr.startswith("the"):
            e = ("The opposite of %s is %s. The opposite of that is %s again. Taking the opposite twice brings you back: <b>%s</b>."
                 % (dec(inner), dec(-inner), dec(inner), dec(v)))
            cands = [-v, 0, 2 * v]
        else:
            e = ("%s means “the opposite of %s.” %s is %s units to the left of 0, so its opposite is %s units to the right: <b>%s</b>."
                 % (expr, dec(inner), dec(inner), dec(-inner), dec(-inner), dec(v)))
            cands = [-v, 0, 2 * inner]
        its.append(mcq_v(q, v, cands, e, rnd))
    # C: the opposite of a point on a number line (4)
    for v, R, lab in [(-6, 8, 2), (4, 8, 2), (-7, 10, 5), (-3, 6, 2)]:
        nl = NL(-R, R, 1, lab).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What is the opposite of the number at point A?"
        e = ("Point A is at %s, %d units from 0. The opposite is %d units from 0 on the other side: <b>%s</b>."
             % (dec(v), abs(v), abs(v), dec(-v)))
        sgn = 1 if v < 0 else -1
        its.append(mcq_v(q, -v, [v, -v - sgn, -v + sgn], e, rnd))
    # D: which point is the opposite (3)
    for target, shown, R in [(4, "the opposite of " + M + "4", 6), (-5, "the opposite of 5", 8), (3, M + "(" + M + "3)", 6)]:
        nl = NL(-R, R, 1, 2)
        vals = [target, -target, target - 1, target + 1]
        lp = pos.next()
        letters_q(nl, vals, 0, lp)
        q = fig(nl.svg(nl_label(nl, "with points A, B, C and D"))) + "Which point is at %s?" % shown
        e = ("%s is %s, %d units %s of 0. Point %s is there. The point at %s is the number you started from, not its opposite."
             % (cap(shown), dec(target), abs(target), "to the right" if target > 0 else "to the left", "ABCD"[lp],
                dec(-target)))
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], "ABCD"[lp], e))
    # E: opposites in words (3)
    its.append(mcq("Two numbers are opposites. On a number line, each one is 6 units from 0. What are the two numbers?",
                   "6 and " + M + "6", ["3 and " + M + "3", "0 and 6", M + "6 and " + M + "12"],
                   "Opposites are the same distance from 0 on different sides. 6 units right of 0 is 6, and 6 units left is "
                   + M + "6: <b>6 and " + M + "6</b>. (3 and " + M + "3 are 6 units apart, but each is only 3 units from 0.)", rnd))
    its.append(mcq("Point A is 9 units to the left of 0. Point B is at the opposite of point A. Where is point B?",
                   "9 units to the right of 0", ["9 units to the left of 0", "at 0", "18 units to the right of 0"],
                   "A is at " + M + "9. Its opposite is 9, the same distance from 0 on the other side: <b>9 units to the right of 0</b>. "
                   "(18 units is the distance from A to B, not from 0 to B.)", rnd))
    its.append(mcq("Which statement is true?", M + "(" + M + "8) = 8",
                   [M + "(" + M + "8) = " + M + "8", "The opposite of " + M + "8 is " + M + "8",
                    M + "8 and 8 are on the same side of 0"],
                   M + "(" + M + "8) means the opposite of " + M + "8, which is 8. " + M + "8 and 8 are on different sides of 0, "
                   "each 8 units away. True: <b>" + M + "(" + M + "8) = 8</b>.", rnd))
    return {"title": "Opposites and the opposite of the opposite", "items": its}


# ============================================================ set 4: fractions and decimals on a number line
def set_fractions(rnd, P):
    its = []
    pos = Pos(rnd)
    # A: halves, read as a decimal (4)
    for v, lo, hi in [(F(-5, 2), -4, 2), (F(-1, 2), -3, 3), (F(-7, 2), -5, 1), (F(3, 2), -3, 3)]:
        nl = NL(lo, hi, F(1, 2), 1).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "marked in halves with point A"))) + "What number is at point A? Write it as a decimal."
        a, b = v - F(1, 2), v + F(1, 2)
        e = ("There are 2 spaces between whole numbers, so each tick mark is 0.5. "
             "Point A is halfway between %s and %s: <b>%s</b>." % (dec(a), dec(b), dec(v)))
        if v < 0:
            e += " It is to the left of 0, so it is negative."
        point2 = (1 if v > 0 else -1) * (int(abs(v)) + F(2, 10))     # wrote 1/2 as 0.2
        its.append(mcq_v(q, v, [-v, v + 1, v - 1, point2], e, rnd))
    # B: fourths and tenths, read as a decimal (4)
    for v, lo, hi, st in [(F(-7, 4), -3, 1, F(1, 4)), (F(-5, 4), -2, 2, F(1, 4)), (F(-7, 10), -2, 1, F(1, 10)),
                          (F(-13, 10), -2, 1, F(1, 10))]:
        mid = F(1, 2) if st == F(1, 10) else None
        nl = NL(lo, hi, st, 1, mid=mid).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "marked in %s with point A" % ("fourths" if st == F(1, 4) else "tenths")))) + \
            "What number is at point A? Write it as a decimal."
        right = -((-v).numerator // (-v).denominator)          # the whole number just right of A (toward 0)
        right = F(right)
        k = int((right - v) / st)
        per = int(1 / st)
        e = ("There are %d spaces between whole numbers, so each tick mark is %s. "
             "Point A is %s to the left of %s: <b>%s</b>." % (per, dec(st), ticks(k), dec(right), dec(v)))
        other = right - 1 + k * st                               # counted from the whole number on the other side
        if st == F(1, 4):
            tenth = right - F(k, 10)                             # read each fourth as a tenth
            its.append(mcq_v(q, v, [-v, other, tenth, v - st], e + " Each tick is 0.25, not 0.1.", rnd))
        else:
            its.append(mcq_v(q, v, [-v, other, v + st, v - st], e, rnd))
    # C: read as a fraction (5)
    for v, lo, hi, st in [(F(-3, 4), -2, 1, F(1, 4)), (F(-3, 2), -3, 1, F(1, 2)), (F(-9, 4), -3, 1, F(1, 4)),
                          (F(-1, 3), -2, 1, F(1, 3)), (F(-5, 3), -2, 1, F(1, 3))]:
        nl = NL(lo, hi, st, 1).point(v, "A")
        d = st.denominator
        wname = {2: "halves", 3: "thirds", 4: "fourths"}[d]
        q = fig(nl.svg(nl_label(nl, "marked in %s with point A" % wname))) + "What number is at point A? Write it as a fraction or mixed number."
        right = F(-((-v).numerator // (-v).denominator))
        k = int((right - v) / st)
        e = ("Count the spaces, not the tick marks: each whole is cut into %d equal spaces, so each tick mark is %s. "
             "Point A is %s to the left of %s: <b>%s</b>." % (d, frc(st), ticks(k), dec(right), frc(v)))
        other = right - 1 + k * st
        wrong_d = right - F(k, d + 1)                           # counted the tick marks and saw d+1 parts
        its.append(mcq_v(q, v, [-v, other, wrong_d, v - 1], e, rnd, frc))
    # D: which point is at ... (4)
    for vals, lo, hi, st, fmt in [([F(-3, 2), F(3, 2), F(-1, 2), F(-5, 2)], -3, 3, F(1, 2), dec),
                                  ([F(-1, 2), F(1, 2), F(-3, 2), F(3, 2)], -2, 2, F(1, 2), frc),
                                  ([F(-9, 4), F(-7, 4), F(-11, 4), F(-5, 4)], -3, 1, F(1, 4), dec),
                                  ([F(-3, 4), F(3, 4), F(-1, 4), F(-7, 4)], -2, 2, F(1, 4), frc)]:
        v = vals[0]
        nl = NL(lo, hi, st, 1)
        right = F(-((-v).numerator // (-v).denominator))
        k = int((right - v) / st)
        assert len(set(vals)) == 4, vals
        lp = pos.next()
        letters_q(nl, vals, 0, lp)
        q = fig(nl.svg(nl_label(nl, "with points A, B, C and D"))) + "Which point is at %s?" % fmt(v)
        e = ("Each tick mark is %s. %s is %s to the left of %s. Point %s is there."
             % (fmt(st), fmt(v), ticks(k), dec(right), "ABCD"[lp]))
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], "ABCD"[lp], e))
    # E: no picture (3)
    its.append(mcq("Between which two integers is " + M + "3.4 on a number line?", M + "4 and " + M + "3",
                   ["3 and 4", M + "3 and " + M + "2", M + "5 and " + M + "4"],
                   M + "3.4 is a little more than 3 units to the left of 0. It is past " + M + "3 but not as far as " + M +
                   "4: <b>between " + M + "4 and " + M + "3</b>.", rnd))
    its.append(mcq_v("What number is halfway between " + M + "5 and " + M + "4?", F(-9, 2), [F(9, 2), F(-7, 2), F(-11, 2)],
                     "Halfway between two whole numbers is the half: between " + M + "5 and " + M + "4 is <b>" + M + "4.5</b>. "
                     "It is negative because both numbers are to the left of 0.", rnd))
    its.append(mcq("Where is " + M + "2" + " " + frh(1, 4) + " on a number line?",
                   "between " + M + "3 and " + M + "2, closer to " + M + "2",
                   ["between " + M + "3 and " + M + "2, closer to " + M + "3", "between 2 and 3, closer to 2",
                    "between " + M + "2 and " + M + "1, closer to " + M + "2"],
                   M + "2 " + frh(1, 4) + " is " + frh(1, 4) + " past " + M + "2, going left. So it is <b>between " + M +
                   "3 and " + M + "2, closer to " + M + "2</b>.", rnd))
    return {"title": "Fractions and decimals on the number line", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    # 1-2: temperature stories
    for city, t1, t2 in [("Fargo", -12, 5), ("Anchorage", -4, 9)]:
        nm, he, his = P.next()
        q = ("On a winter morning in %s, %s read the thermometer: %d degrees below zero (°F). "
             "In the afternoon, it was %d degrees above zero. Which number shows the morning temperature?"
             % (city, nm, -t1, t2))
        e = "Below zero is negative. The morning temperature is <b>%s°F</b>. The afternoon temperature is %s°F." % (dec(t1), dec(t2))
        its.append(mcq(q, (dec(t1) + "°F", t1), [(dec(-t1) + "°F", -t1), (dec(t2) + "°F", t2), (dec(-t2) + "°F", -t2)], e, rnd))
    # 3: real elevations
    q = ("Mount Whitney in California is 14,505 feet above sea level. Not far away, Badwater Basin in Death Valley is "
         "282 feet below sea level. Which number represents the elevation of Badwater Basin?")
    e = "Below sea level is negative, and sea level is 0. Badwater Basin is at <b>" + M + "282 feet</b>."
    its.append(mcq(q, M + "282 feet", ["282 feet", "14,505 feet", M + "14,505 feet"], e, rnd))
    # 4: thermometer picture
    q = fig(thermo_svg(-10, 10, 2, 10, -6)) + "What temperature does the thermometer show?"
    e = ("There are 5 spaces between 0 and 10, so each tick mark is 10 ÷ 5 = 2 degrees. "
         "The red column ends 3 tick marks below 0: " + M + "2, " + M + "4, " + M + "6. The temperature is <b>" + M + "6°F</b>.")
    its.append(mcq(q, M + "6°F", ["6°F", M + "3°F", M + "4°F"], e, rnd))
    # 5: diver
    q = "A diver’s depth gauge reads " + M + "35 feet. Sea level is 0. What does " + M + "35 mean?"
    e = "Negative numbers are below sea level. " + M + "35 feet means <b>35 feet below sea level</b>."
    its.append(mcq(q, "35 feet below sea level", ["35 feet above sea level", "35 feet above the ocean floor", "35 feet from the boat"], e, rnd))
    # 6: building levels picture
    nm, he, his = P.next()
    q = fig(floors_svg(-3, 4, -2, "car")) + ("In a hotel, the ground floor is 0. %s parks on the level marked “car.” "
                                             "Which number is that level?" % nm)
    e = ("The ground floor is 0. Levels below it are negative. The car is 2 levels below 0, at " + M + "1, then " + M +
         "2. The level is <b>" + M + "2</b>.")
    its.append(mcq_v(q, -2, [2, -3, -1], e, rnd))
    # 7: bank balance
    nm, he, his = P.next()
    q = "%s’s bank account balance is %s. What does this mean?" % (nm, money(-15))
    e = ("A balance of $0 means no money and no debt. A negative balance means money is owed: "
         "<b>%s owes the bank $15</b>." % nm)
    its.append(mcq(q, "%s owes the bank $15." % nm, ["%s has $15 in the account." % nm, "%s has $0 in the account." % nm,
                                                     "%s deposited $15." % nm], e, rnd))
    # 8: deposit and withdrawal
    nm, he, his = P.next()
    q = ("%s deposits $40 into %s account. Later %s withdraws $25. Which pair of numbers shows the two changes, in order?"
         % (nm, his, he))
    e = "A deposit adds money, so it is positive: 40. A withdrawal takes money out, so it is negative: " + M + "25. <b>40 and " + M + "25</b>."
    its.append(mcq(q, "40 and " + M + "25", [M + "40 and 25", "40 and 25", M + "40 and " + M + "25"], e, rnd))
    # 9: football
    q = ("On the first play, the Tigers lost 8 yards. On the second play, they gained 5 yards. "
         "Which pair of numbers shows the two plays, in order?")
    e = "A loss is negative and a gain is positive: " + M + "8 for the first play and 5 for the second. <b>" + M + "8 and 5</b>."
    its.append(mcq(q, M + "8 and 5", ["8 and " + M + "5", "8 and 5", M + "8 and " + M + "5"], e, rnd))
    # 10-11: coldest / farthest left
    cities = [("Fairbanks", -18), ("Bismarck", -7), ("Chicago", 3), ("Boston", 0)]
    q = ("One January morning, the temperatures were: " + ", ".join("%s %s°F" % (c, dec(t)) for c, t in cities) +
         ". Which city was the coldest?")
    e = ("The coldest temperature is the one farthest below 0. 18 degrees below zero is colder than 7 degrees below zero, "
         "so <b>Fairbanks</b> (" + M + "18°F) was the coldest.")
    its.append(mcq(q, "Fairbanks", ["Bismarck", "Boston", "Chicago"], e, rnd))
    cities = [("Duluth", -2), ("Minneapolis", -9), ("Detroit", 4), ("Omaha", -5)]
    q = ("A class plotted these temperatures on a number line: " + ", ".join("%s %s°F" % (c, dec(t)) for c, t in cities) +
         ". Which city’s point is farthest to the left?")
    e = ("Numbers to the left of 0 are negative, and the farther below 0, the farther left. " + M + "9 is 9 units left of 0, "
         "more than " + M + "5 or " + M + "2. <b>Minneapolis</b> is farthest left.")
    its.append(mcq(q, "Minneapolis", ["Duluth", "Omaha", "Detroit"], e, rnd))
    # 12: farther below sea level
    q = "A shark swims at " + M + "40 feet. A sea turtle swims at " + M + "25 feet. Which animal is farther below sea level?"
    e = M + "40 feet means 40 feet below sea level, and " + M + "25 feet means 25 feet below. 40 feet is deeper, so <b>the shark</b> is farther below."
    its.append(mcq(q, "the shark", ["the sea turtle", "They are at the same depth.", "Neither: both are above sea level."], e, rnd))
    # 13: golf
    a, b = P.next(), P.next()
    q = "In golf, par is 0. %s finished 3 strokes under par. %s finished 2 strokes over par. Which number shows %s’s score?" % (
        a[0], b[0], b[0])
    e = "Over par is positive and under par is negative. %s is 2 over par: <b>2</b>. (%s’s score is %s3.)" % (b[0], a[0], M)
    its.append(mcq_v(q, 2, [-2, -3, 3], e, rnd))
    # 14: rocket countdown
    q = ("A rocket launch happens at time 0. The engines start 10 seconds before launch. "
         "30 seconds after launch, the rocket passes the clouds. Which number shows when the engines start?")
    e = "Before 0 is negative and after 0 is positive. 10 seconds before launch is <b>" + M + "10 seconds</b>."
    its.append(mcq(q, M + "10 seconds", ["10 seconds", "30 seconds", M + "30 seconds"], e, rnd))
    # 15: opposite elevation
    q = ("A submarine is at " + M + "120 feet. A seagull flies at the opposite elevation. Where is the seagull?")
    e = "The opposite of " + M + "120 is 120. 120 feet is positive, so it is <b>120 feet above sea level</b>."
    its.append(mcq(q, "120 feet above sea level", ["120 feet below sea level", "at sea level", "240 feet above sea level"], e, rnd))
    # 16: opposite temperature
    q = ("At noon, the temperature was 5°F. At midnight, it was the opposite of the noon temperature. "
         "What was the temperature at midnight?")
    e = "The opposite of 5 is " + M + "5, the same distance from 0 on the other side. Midnight: <b>" + M + "5°F</b>."
    its.append(mcq(q, M + "5°F", ["5°F", "0°F", M + "10°F"], e, rnd))
    # 17: depth gauge reads 0
    q = "A diver’s depth gauge reads 0 feet. Where is the diver?"
    e = "0 feet on a depth gauge is sea level, the line between above and below. The diver is <b>at the surface of the water</b>."
    its.append(mcq(q, "at the surface of the water", ["at the bottom of the sea", "100 feet below the surface",
                                                       "flying above the water"], e, rnd))
    # 18: change of 0
    q = "The price of a stock changed by $0 today. What does this mean?"
    e = "A positive change means the price went up and a negative change means it went down. A change of 0 means <b>the price did not go up or down</b>."
    its.append(mcq(q, "The price did not go up or down.", ["The price went down to $0.", "The stock is worth nothing.",
                                                          "The price went up."], e, rnd))
    # 19: dolphin and pelican
    q = "A dolphin swims 20 feet below sea level. A pelican flies 15 feet above sea level. Which pair of numbers shows the dolphin, then the pelican?"
    e = "Below sea level is negative and above is positive: dolphin " + M + "20, pelican 15. <b>" + M + "20 and 15</b>."
    its.append(mcq(q, M + "20 and 15", ["20 and " + M + "15", "20 and 15", M + "20 and " + M + "15"], e, rnd))
    # 20: charge
    q = ("A balloon rubbed on hair picks up extra negative charge. Its charge is " + M + "5 units. "
         "The hair is left with the opposite charge. What is the charge of the hair?")
    e = "The opposite of " + M + "5 is 5. The hair has a positive charge of <b>5 units</b>."
    its.append(mcq(q, "5 units", [M + "5 units", "0 units", M + "10 units"], e, rnd))
    return {"title": "Negative numbers word problems", "items": its}


# ============================================================ lesson
def body_html():
    nl1 = NL(-5, 5, 1, 1, gap=30).point(-3, None, GREEN).point(3, None, GREEN).brace(-3, 0, "3 units").brace(0, 3, "3 units")
    opp = nl1.svg("number line from " + M + "5 to 5 showing that " + M + "3 and 3 are both 3 units from 0")
    nl2 = NL(-3, 1, F(1, 2), 1, gap=36).point(F(-5, 2), "A").point(F(-1, 2), "B")
    half = nl2.svg("number line from " + M + "3 to 1 marked in halves with A at " + M + "2.5 and B at " + M + "1/2")
    nl3 = NL(-10, 10, 2, 10).point(-6, "C")
    by2 = nl3.svg("number line from " + M + "10 to 10 counting by 2 with C at " + M + "6")
    return (
        "<h2>Two directions from 0</h2>"
        "<p>Many quantities go in two opposite directions: above and below, up and down, in and out. "
        "We use <b>positive numbers</b> for one direction and <b>negative numbers</b> for the other. "
        "A negative number has a minus sign: " + M + "8 is read “negative 8.”</p>"
        "<p><b>0</b> is the starting point between the two directions. It is neither positive nor negative.</p>" +
        table(["Situation", "Positive", "Zero means", "Negative"], [
            ["Temperature", "above zero: 12°F", "0 degrees", "below zero: " + M + "8°F"],
            ["Elevation", "above sea level: 300 ft", "sea level", "below sea level: " + M + "40 ft"],
            ["Bank account", "deposit: $25", "no change", "withdrawal: " + M + "$25"],
            ["Football", "gain: 6 yards", "no gain or loss", "loss: " + M + "6 yards"],
            ["Building", "floor 3", "ground floor", "2 floors below: " + M + "2"],
            ["Electric charge", "positive: 4", "neutral", "negative: " + M + "4"],
        ]) +
        ex("Example", "A diver is 15 feet below sea level. Which number represents the diver’s position?",
           "Sea level is 0. “Below” is the negative direction.", M + "15 feet") +
        "<h2>Negative numbers on a number line</h2>"
        "<p>Positive numbers are to the <b>right</b> of 0. Negative numbers are to the <b>left</b>. "
        "To read a point, check what each tick mark counts by first.</p>"
        "<figure class='sn-fig'>" + by2 +
        "<figcaption>There are 5 spaces from 0 to 10, so each tick mark is 2. C is 3 tick marks left of 0: " + M + "2, " +
        M + "4, " + M + "6. So C = " + M + "6, not " + M + "3.</figcaption></figure>"
        "<h2>Opposites</h2>"
        "<p>Two numbers are <b>opposites</b> when they are the same distance from 0 on different sides. "
        "3 and " + M + "3 are opposites. The opposite of 0 is 0.</p>"
        "<figure class='sn-fig'>" + opp +
        "<figcaption>" + M + "3 and 3 are both 3 units from 0, on opposite sides.</figcaption></figure>"
        "<p>The minus sign can mean “the opposite of.” So " + M + "(" + M + "5) means the opposite of " + M +
        "5, which is 5. Taking the opposite twice brings you back to the number you started with.</p>" +
        ex("Example", "What is " + M + "(" + M + "9)?", M + "9 is 9 units left of 0. Its opposite is 9 units right of 0.", "9") +
        "<h2>Fractions and decimals below 0</h2>"
        "<p>Negative fractions and decimals sit between the negative integers. " + M + "2.5 is halfway between " + M +
        "3 and " + M + "2. " + M + frh(1, 2) + " is halfway between " + M + "1 and 0.</p>"
        "<figure class='sn-fig'>" + half +
        "<figcaption>Each tick mark is " + frh(1, 2) + ". A is 1 tick mark left of " + M + "2, so A = " + M + "2.5 = " + M +
        "2 " + frh(1, 2) + ". B is 1 tick mark left of 0, so B = " + M + frh(1, 2) + ".</figcaption></figure>" +
        ex("Example", "Between which two integers is " + M + "4.3?",
           "It is a little more than 4 units left of 0, so it is past " + M + "4 but not as far as " + M + "5.",
           "between " + M + "5 and " + M + "4") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing 20 for “20 feet below sea level”", "Below, loss, withdrawal and under par are negative: " + M + "20"],
            ["Reading " + M + "2.5 as " + M + "1.5", "Count left from " + M + "2: " + M + "2.5 is farther from 0 than " + M + "2"],
            ["Counting each tick as 1 when the scale counts by 2 or 0.5", "Find the tick value first: label difference ÷ spaces"],
            ["Thinking " + M + "(" + M + "5) = " + M + "5", "The opposite of " + M + "5 is 5"],
            ["Thinking the opposite of 4 is " + frh(1, 4), frh(1, 4) + " is the reciprocal. The opposite of 4 is " + M + "4"],
            ["Counting tick marks instead of spaces for fractions", "Thirds have 3 spaces between whole numbers, not 3 tick marks"],
        ])
    )


FAQ = [
    {"q": "How do you explain negative numbers to a 6th grader?",
     "a": "Negative numbers describe the opposite direction from 0, like below zero on a thermometer, below sea level or money taken out of an account. On a number line they are to the left of 0."},
    {"q": "What does 0 mean with positive and negative numbers?",
     "a": "0 is the starting point between the two directions, and it depends on the situation: sea level for elevation, the ground floor in a building, no gain or loss in football, or a neutral electric charge."},
    {"q": "What is the opposite of a negative number?",
     "a": "It is the positive number the same distance from 0. The opposite of −7 is 7, so −(−7) = 7."},
    {"q": "How do you find −2.5 on a number line?",
     "a": "Go to −2, then move half a unit farther left. −2.5 is halfway between −3 and −2."},
]


def gen_unit():
    rnd = random.Random(607)
    P = People(rnd)
    sets = [set_situations(rnd, P), set_read(rnd, P), set_opposites(rnd, P), set_fractions(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "negative-numbers", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Positive and Negative Numbers: Real-World Meaning, Opposites and the Number Line",
        "seo_title": "Grade 6 Negative Numbers Worksheets: Integers in Real Life, Opposites and Number Lines (6.NS.C.5)",
        "short_title": "Negative numbers",
        "domain": "The Number System",
        "standard_code": "6.NS.C.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/NS/C/5/",
        "standard_text": "Understand that positive and negative numbers are used together to describe quantities having opposite directions or values (e.g., temperature above/below zero, elevation above/below sea level, credits/debits, positive/negative electric charge); use positive and negative numbers to represent quantities in real-world contexts, explaining the meaning of 0 in each situation.",
        "meta_desc": "Free Grade 6 negative numbers worksheets: write positive and negative numbers for real-world situations, explain what 0 means, read integers, fractions and decimals on a number line, and find opposites like −(−5). 100 practice questions with answers.",
        "key_big": "Positive and negative numbers point in opposite directions from 0.",
        "key_sub": "Below zero, below sea level, a loss or a withdrawal is negative. Negative numbers are to the left of 0 on a number line, and opposites like 3 and −3 are the same distance from 0, so −(−3) = 3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(number line|vertical|thermometer)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
