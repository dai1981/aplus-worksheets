# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Integers (Ontario Mathematics Curriculum 2020, Grade 6: Number, B1)
  python3 tools/gen_ca_math_g6_integers.py
Integers in context (winter temperatures in Winnipeg, below sea level, bank balances, golf scores, parking
levels), reading integers on horizontal and vertical number lines and thermometers, comparing and ordering
integers, opposite integers, and word problems with simple changes on a number line (temperature changes).
Wrong answers come from real student mistakes: dropping the minus sign, −7 > −2 because 7 > 2, ordering by
the digits and ignoring the sign, counting every tick as 1 when the scale counts by 2 or 5, counting the wrong
way from a label, skipping 0 when counting across zero, thinking the opposite of a number is 0 or one step
away, counting only to 0 instead of across it, and moving the wrong way.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ numbers
def n(v):
    """Integer with the real minus sign. Ontario style: 4 digits with no separator, 5+ with a space."""
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
    return n(v) + NBSP + "m"


def spaces(k):
    return "1 space" if k == 1 else "%d spaces" % k


def ticks(k):
    return "1 tick mark" if k == 1 else "%d tick marks" % k


def steps(k):
    return "1 step" if k == 1 else "%d steps" % k


def units(k):
    return "1 unit" if k == 1 else "%d units" % k


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


def vline_svg(lo, hi, step, lab, pts, label, zero_note=None):
    """Vertical number line; pts = [(value, name)] drawn as dots with the name to the right."""
    lo, hi, step, lab = F(lo), F(hi), F(step), F(lab)
    k = int((hi - lo) / step)
    g = 20
    top = 18
    x = 58
    Yv = lambda v: top + float((hi - F(v)) / step) * g
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x, top - 12, x, Yv(lo) + 12, INK)]
    s.append("<path d='M%d %d l-5 9 h10 z M%d %.1f l-5 -9 h10 z' fill='%s'/>" % (x, top - 14, x, Yv(lo) + 14, INK))
    for i in range(k + 1):
        v = lo + i * step
        y = Yv(v)
        big = (v / lab).denominator == 1
        h = 9 if big else 5
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x - h, y, x + h, y, INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(x - 15, y + 5, n(v), 14, anchor="end", bold=(v == 0)))
    W = 120
    if zero_note:
        assert all(F(v) != 0 for v, nm in pts)
        s.append(text(x + 16, Yv(0) + 5, zero_note, 14, anchor="start", col=GRAY))
        W = int(x + 16 + tw(zero_note, 14) + 8)
    ys = sorted(Yv(v) for v, nm in pts)
    assert all(b - a >= 18 for a, b in zip(ys, ys[1:])), ("letters overlap", label)
    for v, nm in pts:
        assert lo <= F(v) <= hi and ((F(v) - lo) / step).denominator == 1
        s.append("<circle cx='%d' cy='%.1f' r='5.5' fill='%s'/>" % (x, Yv(v), GREEN))
        s.append(text(x + 16, Yv(v) + 6, nm, 16, anchor="start", bold=True, col=GREEN))
    return svg_wrap(W, int(Yv(lo) + 22), "".join(s), label)


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
ZERO = {"temp": "0" + NBSP + "°C", "sea": "sea level", "bank": "no change to the account", "floors": "the ground floor",
        "points": "no change to the score", "golf": "par", "money": "no change", "owe": "no money and no debt"}


def sit(kind, v):
    p, q = SIT[kind]
    return (p if v > 0 else q).format(n=abs(v))


def two_story(kind, a, b, P):
    """A story with two signed quantities a (first) and b (second). Returns (text, name of a, name of b)."""
    nm, he, his = P.next()
    if kind == "temp_winnipeg":
        return ("On a January morning in Winnipeg, the temperature at 7 a.m. was %s. By 3 p.m., it was %s."
                % (sit("temp", a), sit("temp", b)), "the temperature at 7 a.m.", "the temperature at 3 p.m.")
    if kind == "temp_ottawa":
        return ("On a March day in Ottawa, the temperature at 6 a.m. was %s. At 2 p.m., it was %s."
                % (sit("temp", a), sit("temp", b)), "the temperature at 6 a.m.", "the temperature at 2 p.m.")
    if kind == "sea":
        return ("Off the coast of Nova Scotia, a scuba diver is %s. A seagull flies %s." % (sit("sea", a), sit("sea", b)),
                "the diver’s position", "the seagull’s position")
    if kind == "bank":
        return ("%s’s bank account changed twice. On Monday, %s made %s. On Friday, %s made %s."
                % (nm, he, sit("bank", a), he, sit("bank", b)),
                "the Monday change to the account", "the Friday change to the account")
    if kind == "floors":
        return ("In a Toronto shopping mall, the parking garage is %s. The food court is %s."
                % (sit("floors", a), sit("floors", b)),
                "the level of the parking garage", "the level of the food court")
    if kind == "golf":
        nm2 = P.next()[0]
        return ("In a round of golf, %s finished %s and %s finished %s." % (nm, sit("golf", a), nm2, sit("golf", b)),
                "%s’s score compared with par" % nm, "%s’s score compared with par" % nm2)
    if kind == "money":
        return ("On Saturday, %s earned $%d shovelling snow. On Sunday, %s spent $%d at the hockey arena snack bar."
                % (nm, a, he, -b), "the money earned on Saturday", "the money spent on Sunday")
    if kind == "points":
        return ("In a class trivia game, a team wins %d points for a right answer and loses %d points for a wrong answer."
                % (a, -b), "a right answer", "a wrong answer")
    raise ValueError(kind)


def set_situations(rnd, P):
    its = []
    # A: a story with two quantities; write one of them as an integer (8)
    plan = [("temp_winnipeg", -24, -15, 0, "temp"), ("sea", -9, 14, 0, "sea"), ("bank", 35, -20, 1, "bank"),
            ("floors", -2, 4, 0, "floors"), ("golf", 3, -2, 1, "golf"), ("temp_ottawa", -4, 6, 1, "temp"),
            ("money", 18, -11, 1, "money"), ("points", 10, -5, 1, "points")]
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
        ("Heights are measured in metres above or below sea level. What does a height of 0" + NBSP + "m mean?",
         "exactly at sea level", ["at the bottom of the ocean", "at the top of a mountain", "there is no height to measure"],
         "Above sea level is positive and below sea level is negative. 0" + NBSP + "m is the starting point between them: "
         "<b>exactly at sea level</b>."),
        ("A thermometer shows degrees Celsius (°C). What does 0" + NBSP + "°C mean?",
         "the temperature at which water freezes", ["no temperature at all", "the coldest temperature possible",
                                                    "the temperature at which water boils"],
         "Water freezes at 0" + NBSP + "°C. A Winnipeg winter is often much colder, with negative temperatures, so "
         "0" + NBSP + "°C is not the coldest possible: <b>water freezes at 0" + NBSP + "°C</b>."),
        ("In an elevator, the levels below the ground floor are negative. What does level 0 mean?",
         "the ground floor", ["the top floor", "the lowest parking level", "a level that does not exist"],
         "Levels above the ground floor are positive and levels below it are negative. 0 is the level between them: "
         "<b>the ground floor</b>."),
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
                            ("sea", 40, ["temp", "floors"]), ("temp", 30, ["sea", "money"])]:
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


# ============================================================ set 2: number lines and thermometers
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
    # A: labels on every other tick (4)
    for v, R in [(-3, 6), (-5, 8), (-7, 8), (-9, 10)]:
        nl = NL(-R, R, 1, 2).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What integer is at point A?"
        e = e_read(nl, v, v + 1) + " A is to the left of 0, so it is negative."
        its.append(mcq_v(q, v, [-v, v + 1, v - 1, -(v + 1)], e, rnd))
    # B: labels every 5 (4)
    for v in [-7, -3, -8, -4]:
        nl = NL(-10, 10, 1, 5).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What integer is at point A?"
        near0 = 5 * int(v / 5.0)                         # the label between A and 0
        mirror = 2 * near0 - v                           # counted the ticks the wrong way from that label
        e = e_read(nl, v, near0)
        e += " The numbers get smaller as you go left, so do not count right from %s." % n(near0)
        its.append(mcq_v(q, v, [mirror, -v, v + 1, v - 1], e, rnd))
    # C: scale counts by 2, 5 or 10 (3)
    for lo, hi, st, lab, v in [(-10, 10, 2, 10, -6), (-25, 25, 5, 25, -15), (-50, 50, 10, 50, -30)]:
        nl = NL(lo, hi, st, lab).point(v, "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What integer is at point A?"
        k = abs(v) // st
        e = ("There are %s between 0 and %s, so each tick mark is %s ÷ %d = %d. "
             "Point A is %s to the left of 0: %s. A = <b>%s</b>. (Counting each tick as 1 gives %s.)"
             % (spaces(lab // st), n(lab), n(lab), lab // st, st, ticks(k),
                ", ".join(n(-st * i) for i in range(1, k + 1)), n(v), n(-k)))
        its.append(mcq_v(q, v, [-k, -v, v + st, v - st], e, rnd))
    # D: which point is at ... (3)
    for v, R in [(-5, 6), (-3, 6), (-7, 8)]:
        nl = NL(-R, R, 1, 2)
        vals = [v, -v, v + 1, v - 1]
        lp = pos.next()
        letters_q(nl, vals, 0, lp)
        q = fig(nl.svg(nl_label(nl, "with points A, B, C and D"))) + "Which point is at %s?" % n(v)
        e = ("%s is %s to the left of 0. Point %s is there. The point at %s is to the right of 0."
             % (n(v), units(abs(v)), "ABCD"[lp], n(-v)))
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], "ABCD"[lp], e))
    # E: thermometers (vertical number lines) (4)
    for lo, hi, st, lab, v, place, when in [(-10, 10, 2, 10, -6, "Ottawa", "on a December morning"),
                                            (-30, 10, 5, 10, -25, "Winnipeg", "on a January morning"),
                                            (-20, 20, 5, 10, -15, "Montréal", "on a February night"),
                                            (-40, 0, 5, 10, -35, "Yellowknife", "on a January night")]:
        q = fig(thermo_svg(lo, hi, st, lab, v)) + "A thermometer in %s %s shows this temperature. What is it?" % (place, when)
        L = int(math.ceil(F(v) / lab)) * lab              # the label just above the top of the column
        m = (L - v) // st
        e = ("The labels count by %d, and there are %s between labels, so each tick mark is %d degrees. "
             "The top of the red column is %s below %s. Count down by %d: %s. The temperature is <b>%s</b>."
             % (lab, spaces(lab // st), st, ticks(m), n(L), st,
                ", ".join(n(L - st * i) for i in range(1, m + 1)), deg(v)))
        e += " Below 0, the numbers get smaller as you go down."
        wrong = [L - m, L + m * st, -v, v - st]           # each tick as 1, counted up, no minus sign, one tick off
        its.append(mcq(q, (deg(v), v), [(deg(x), x) for x in wrong], e, rnd))
    # F: vertical number lines (2)
    q = (fig(vline_svg(-20, 20, 5, 10, [(-15, "A")], "vertical number line from " + M + "20 to 20 counting by 5 with point A",
                       "sea level")) +
         "This vertical number line shows heights in metres. 0 is sea level. What integer is at point A?")
    e = ("The labels count by 10, and there are 2 spaces between labels, so each tick mark is 5. "
         "Point A is 1 tick mark below " + M + "10, so A = <b>" + M + "15</b>. That is 15" + NBSP + "m below sea level.")
    its.append(mcq_v(q, -15, [-11, -5, 15, -3], e, rnd))
    q = (fig(vline_svg(-6, 4, 1, 2, [(-5, "A")], "vertical number line from " + M + "6 to 4 with point A",
                       "ground floor")) +
         "This vertical number line shows the levels of a Calgary office tower. What level is point A?")
    e = ("The labels count by 2, so each tick mark is 1. Point A is 1 tick mark above " + M + "6, so A = <b>" + M + "5</b>. "
         "Going up, " + M + "6 becomes " + M + "5, not " + M + "7.")
    its.append(mcq_v(q, -5, [-7, 5, -4, -3], e, rnd))
    assert len(its) == 20
    return {"title": "Number lines and thermometers", "items": its}


# ============================================================ set 3: compare and order
def set_compare(rnd, P):
    its = []
    # A: the greatest (4)
    for vals in [[-6, 2, -9, -1], [-3, -8, -1, -6], [-12, -5, -9, -2], [-15, -11, -20, -13]]:
        big = max(vals)
        q = "Which integer is the greatest? " + lst(vals)
        e = "The greatest number is the one farthest to the right on a number line. "
        if big < 0:
            e += ("All four are negative, so the one closest to 0 is the greatest: <b>%s</b>. "
                  "%s is the least even though %d has the biggest digits." % (n(big), n(min(vals)), -min(vals)))
        else:
            e += "%s is the farthest right, so it is the greatest: <b>%s</b>." % (n(big), n(big))
        its.append(mcq_v(q, big, [v for v in sorted(vals, key=lambda x: -abs(x)) if v != big], e, rnd))
    # B: the least (4)
    for vals in [[-2, 1, -9, -5], [-3, -1, 0, 2], [-14, -8, -17, -11], [4, -4, -6, 6]]:
        sm = min(vals)
        q = "Which integer is the least? " + lst(vals)
        e = ("The least number is the one farthest to the left on a number line. %s is the farthest left: <b>%s</b>."
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
        if a < 0 and b < 0:
            e = ("%s is to the left of %s on a number line, so %s is less: <b>%s</b>. "
                 "Do not compare the digits only: %d &gt; %d, but %s &lt; %s."
                 % (n(a), n(b), n(a), right, abs(a), abs(b), n(a), n(b)))
        else:
            e = ("%s is to the left of %s on a number line, so %s is less: <b>%s</b>. Every negative number is less than 0."
                 % (n(a), n(b), n(a), right))
        its.append(mcq(q, right, wrongs, e, rnd))
    # D: order from least to greatest (3)
    for vals in [[-2, 3, -8, -5], [-1, -6, 4, 0], [-4, 7, -10, -7]]:
        asc = sorted(vals)
        right = lst(asc)
        by_abs = lst(sorted(vals, key=abs))                    # ignored the signs
        desc = lst(sorted(vals, reverse=True))                 # greatest first
        neg_wrong = lst(sorted([v for v in vals if v < 0], reverse=True) + sorted(v for v in vals if v >= 0))
        q = "Which list is in order from least to greatest? " + lst(vals)
        e = ("Start with the number farthest left on a number line. The negative number with the biggest digits is the least: "
             "<b>%s</b>." % right)
        its.append(mcq(q, right, [neg_wrong, by_abs, desc], e, rnd))
    # E: order from greatest to least (2)
    for vals in [[-3, 5, -9, 0], [-16, -4, 7, -11]]:
        desc = sorted(vals, reverse=True)
        right = lst(desc)
        by_abs = lst(sorted(vals, key=abs, reverse=True))      # biggest digits first
        asc = lst(sorted(vals))                                # least first
        neg_wrong = lst(sorted([v for v in vals if v >= 0], reverse=True) + sorted(v for v in vals if v < 0))
        q = "Which list is in order from greatest to least? " + lst(vals)
        e = ("Start with the number farthest right on a number line and move left. Among the negative numbers, "
             "the one closest to 0 comes first: <b>%s</b>." % right)
        its.append(mcq(q, right, [neg_wrong, by_abs, asc], e, rnd))
    # F: between (3)
    its.append(mcq_v("How many integers are between " + M + "3 and 2? (Do not count " + M + "3 or 2.)", 4, [3, 5, 6],
                     "List them: " + M + "2, " + M + "1, 0, 1. That is <b>4</b> integers. Do not forget 0: it is an integer too.",
                     rnd))
    its.append(mcq_v("Which integer is between " + M + "6 and " + M + "2 on a number line?", -4, [4, -7, -1],
                     M + "6 and " + M + "2 are both to the left of 0. The integers between them are " + M + "5, " + M + "4 and "
                     + M + "3, so the answer is <b>" + M + "4</b>. 4 is to the right of 0, so it is not between them.", rnd))
    its.append(mcq("Which temperature is colder than " + deg(-8) + "?", (deg(-11), -11),
                   [(deg(-5), -5), (deg(8), 8), (deg(0), 0)],
                   "Colder means farther down the thermometer, so the number is less. " + M + "11 is to the left of " + M +
                   "8, so <b>" + deg(-11) + "</b> is colder. " + deg(-5) + " is warmer: it is closer to 0.", rnd))
    assert len(its) == 20
    return {"title": "Compare and order integers", "items": its}


# ============================================================ set 4: opposite integers
def set_opposites(rnd, P):
    its = []
    pos = Pos(rnd)
    # A: the opposite of a number (5)
    for v in [-8, 13, -21, 6, -150]:
        o = -v
        step = o + (1 if o > 0 else -1)                       # one step too far
        q = "What is the opposite of %s?" % n(v)
        e = ("Opposites are the same distance from 0 on opposite sides of 0. %s is %s %s of 0, so its opposite is "
             "%s %s of 0: <b>%s</b>." % (n(v), units(abs(v)), "left" if v < 0 else "right", units(abs(v)),
                                         "right" if v < 0 else "left", n(o)))
        e += " The opposite of a number is not 0."
        its.append(mcq_v(q, o, [v, 0, step], e, rnd))
    # B: number line, which point is the opposite of P (4)
    for v, R in [(-4, 6), (3, 6), (-6, 8), (5, 8)]:
        nl = NL(-R, R, 1, 2).point(v, "P", RED)
        o = -v
        vals = [o, o + 1, o - 1, 0] if abs(v) > 1 else None
        lp = pos.next()
        letters_q(nl, vals, 0, lp)
        q = (fig(nl.svg(nl_label(nl, "with point P and points A, B, C and D"))) +
             "Which point shows the opposite of the integer at point P?")
        e = ("P is at %s, which is %s %s of 0. The opposite is %s %s of 0: %s. That is point <b>%s</b>."
             % (n(v), units(abs(v)), "left" if v < 0 else "right", units(abs(v)), "right" if v < 0 else "left",
                n(o), "ABCD"[lp]))
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], "ABCD"[lp], e))
    # C: the opposite of a situation (3)
    sits = [
        ("What is the opposite of 5 degrees below zero?", "5 degrees above zero",
         ["10 degrees above zero", "0 degrees", "5 degrees colder"],
         "5 degrees below zero is " + deg(-5) + ". Its opposite is the same distance from 0 on the other side: "
         "<b>5 degrees above zero</b> (" + deg(5) + ")."),
        ("What is the opposite of 30 metres below sea level?", "30 metres above sea level",
         ["60 metres above sea level", "at sea level", "30 metres deeper"],
         "30 metres below sea level is " + metres(-30) + ". Its opposite is <b>30 metres above sea level</b> (" + metres(30) +
         "). The distance from 0 stays the same; only the direction changes."),
        ("What is the opposite of 4 strokes under par in golf?", "4 strokes over par",
         ["8 strokes over par", "a score of par", "4 more strokes under par"],
         "4 under par is " + M + "4. Its opposite is <b>4 strokes over par</b> (4). The opposite keeps the same number "
         "and changes the direction."),
    ]
    for q, c, w, e in sits:
        its.append(mcq(q, c, w, e, rnd))
    # D: two integers at a distance from 0 (2)
    for d in [7, 12]:
        h = F(d, 2)
        hs = str(h) if h.denominator == 1 else "%.1f" % float(h)
        q = "Which two integers are each %s from 0 on a number line?" % units(d)
        e = ("Count %d units right of 0 to get %d and %d units left of 0 to get %s. "
             "The two integers are <b>%s and %d</b>. They are opposites." % (d, d, d, n(-d), n(-d), d))
        its.append(mcq(q, "%s and %d" % (n(-d), d),
                       ["0 and %d" % d, "%s and %d" % (n(-d), 2 * d), "%s%s and %s" % (M, hs, hs)], e, rnd))
    # E: how many integers between a number and its opposite (2)
    for k in [4, 6]:
        cnt = 2 * k - 1
        q = "How many integers are between %s and its opposite? (Do not count %s or its opposite.)" % (n(-k), n(-k))
        e = ("The opposite of %s is %d. The integers between them are %s. There are %d negative ones, 0 and %d positive ones: "
             "%d + 1 + %d = <b>%d</b>. Do not forget 0."
             % (n(-k), k, lst(range(-k + 1, k)), k - 1, k - 1, k - 1, k - 1, cnt))
        its.append(mcq_v(q, cnt, [cnt - 1, cnt + 1, cnt + 2], e, rnd))
    # F: distance between a number and its opposite (2)
    for v in [-6, -15]:
        d = 2 * abs(v)
        q = "Point A is at %s. Point B is at the opposite of A. How many units apart are A and B?" % n(v)
        e = ("B is at %d. From %s to 0 is %s, and from 0 to %d is %s more. %d + %d = <b>%d</b>."
             % (-v, n(v), units(-v), -v, units(-v), -v, -v, d))
        its.append(mcq_v(q, d, [abs(v), 0, d + 1], e, rnd))
    # G: halfway between opposites; which pair are opposites (2)
    its.append(mcq_v("Which integer is exactly halfway between " + M + "8 and 8?", 0, [4, -4, 8],
                     M + "8 and 8 are opposites. They are each 8 units from 0, so the point halfway between them is "
                     "<b>0</b>. (4 is halfway between 0 and 8.)", rnd))
    its.append(mcq("Which pair of integers are opposites?", M + "11 and 11",
                   [M + "11 and 0", M + "11 and " + M + "1", "11 and 1"],
                   "Opposites are the same distance from 0 on opposite sides. " + M + "11 and 11 are both 11 units from 0: "
                   "<b>" + M + "11 and 11</b>.", rnd))
    assert len(its) == 20
    return {"title": "Opposite integers", "items": its}


# ============================================================ set 5: word problems
def path(a, b):
    d = 1 if b > a else -1
    return ", ".join(n(v) for v in range(a + d, b + d, d))


def set_words(rnd, P):
    its = []
    # 1: two money situations
    a, b = P.next(), P.next()
    q = ("%s has $20 saved. %s owes %s mom $15. Which pair of integers shows %s’s and %s’s money, in order?"
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
    q = "%s’s bank balance is %s. %s puts in $50 of %s birthday money. What is the balance now?" % (
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
    # 6: paying back a debt with chores
    nm, he, his = P.next()
    q = ("%s owes %s dad $8. %s earns $5 shovelling a neighbour’s driveway and gives it all to %s dad. "
         "Which integer shows %s money situation now, in dollars?" % (nm, his, he.capitalize(), his, his))
    e = "Owing $8 is " + M + "8. Paying back $5 moves 5 toward 0: " + path(-8, -3) + ". %s still owes $3: <b>%s3</b>." % (
        he.capitalize(), M)
    its.append(mcq_v(q, -3, [3, -13, 13], e, rnd))
    # 7: compare two negative balances
    a, b = P.next(), P.next()
    q = "%s’s bank balance is %s. %s’s balance is %s. Which statement is true?" % (a[0], money(-20), b[0], money(-35))
    e = (M + "20 is closer to 0 than " + M + "35, so " + M + "20 &gt; " + M + "35. <b>%s has more money</b>: %s owes less."
         % (a[0], a[1]))
    its.append(mcq(q, "%s has more money: %s20 &gt; %s35." % (a[0], M, M),
                   ["%s has more money: %s35 &gt; %s20." % (b[0], M, M), "They have the same amount of money.",
                    "Neither of them owes any money."], e, rnd))
    # 8: Mount Logan and a diver
    q = ("Mount Logan in Yukon is 5959" + NBSP + "m above sea level. A scuba diver off Vancouver Island is 18" + NBSP +
         "m below sea level. Which pair of integers shows their heights, in order?")
    e = "Above sea level is positive and below sea level is negative: <b>5959 and " + M + "18</b>."
    its.append(mcq(q, "5959 and " + M + "18", [M + "5959 and 18", "5959 and 18", M + "5959 and " + M + "18"], e, rnd))
    # 9: diver swims up
    nm, he, his = P.next()
    q = "%s is scuba diving at %s. %s swims up 5" % (nm, metres(-12), he.capitalize()) + NBSP + \
        "m. Which integer shows %s new position?" % his
    e = "Up means counting toward 0: " + path(-12, -7) + ". %s is now at <b>%s</b>, still below sea level." % (nm, metres(-7))
    its.append(mcq(q, (metres(-7), -7), [(metres(-17), -17), (metres(7), 7), (metres(-6), -6)], e, rnd))
    # 10: coldest morning in Winnipeg
    days = [("Monday", -24), ("Tuesday", -19), ("Wednesday", -31), ("Thursday", -28)]
    q = ("These were the 7 a.m. temperatures in Winnipeg one week in January: " +
         ", ".join("%s %s" % (d, deg(t)) for d, t in days) + ". Which morning was the coldest?")
    e = ("The coldest temperature is the one farthest below 0. " + deg(-31) + " is colder than " + deg(-28) +
         ", so <b>Wednesday</b> was the coldest.")
    its.append(mcq(q, "Wednesday", ["Monday", "Tuesday", "Thursday"], e, rnd))
    # 11: order cities
    cities = [("Ottawa", -12), ("Winnipeg", -26), ("Vancouver", 4), ("Toronto", -5)]
    q = ("At 7 a.m. one January morning: " + ", ".join("%s %s" % (c, deg(t)) for c, t in cities) +
         ". Which list goes from coldest to warmest?")
    e = ("Coldest means farthest down the thermometer: " + deg(-26) + ", " + deg(-12) + ", " + deg(-5) + ", " + deg(4) +
         ". <b>Winnipeg, Ottawa, Toronto, Vancouver</b>. " + deg(-26) + " is colder than " + deg(-12) + ".")
    its.append(mcq(q, "Winnipeg, Ottawa, Toronto, Vancouver",
                   ["Toronto, Ottawa, Winnipeg, Vancouver", "Vancouver, Toronto, Ottawa, Winnipeg",
                    "Ottawa, Toronto, Winnipeg, Vancouver"], e, rnd))
    # 12: elevator up (picture)
    nm, he, his = P.next()
    q = fig(vline_svg(-3, 4, 1, 1, [(-2, "car")], "vertical number line of building levels from " + M + "3 to 4",
                      "ground floor")) + \
        ("%s’s family parks on the level marked “car”. They take the elevator up 5 levels to the movie theatre. "
         "Which level is the movie theatre on?" % nm)
    e = ("The car is on level " + M + "2. Count up 5 levels: " + path(-2, 3) + ". The movie theatre is on level <b>3</b>. "
         "Level 0 (the ground floor) counts as a level.")
    its.append(mcq_v(q, 3, [4, -7, -3], e, rnd))
    # 13: elevator down
    nm, he, his = P.next()
    q = ("%s is on level 3 of a hospital. %s takes the elevator down 5 levels to the parking garage. "
         "Which level is the parking garage on?" % (nm, he.capitalize()))
    e = "Count down 5 levels from 3: " + path(3, -2) + ". The parking garage is on level <b>" + M + "2</b>. Do not skip level 0."
    its.append(mcq_v(q, -2, [-3, 8, 2], e, rnd))
    # 14: snow day temperature rise
    q = "On a snow day in Sudbury, the temperature was " + deg(-8) + " at 6 a.m. By noon, it had risen 11 degrees. What was the temperature at noon?"
    e = ("Rising means counting up 11 from " + M + "8: " + path(-8, 3) + ". The temperature at noon was <b>" + deg(3) + "</b>. "
         "Do not skip 0" + NBSP + "°C.")
    its.append(mcq(q, (deg(3), 3), [(deg(4), 4), (deg(-19), -19), (deg(-3), -3)], e, rnd))
    # 15: temperature drop
    q = "In Halifax, the temperature was " + deg(4) + " at 5 p.m. Overnight, it fell 9 degrees. What was the new temperature?"
    e = ("Falling means counting down 9 from 4: " + path(4, -5) + ". The new temperature was <b>" + deg(-5) + "</b>. "
         "Do not skip 0" + NBSP + "°C.")
    its.append(mcq(q, (deg(-5), -5), [(deg(-6), -6), (deg(13), 13), (deg(5), 5)], e, rnd))
    # 16: temperature fall, how many degrees
    q = "In Ottawa, the temperature was " + deg(3) + " at 6 p.m. and " + deg(-6) + " at 3 a.m. How many degrees did it fall?"
    e = "From 3 down to 0 is 3 degrees. From 0 down to " + M + "6 is 6 degrees. 3 + 6 = <b>9 degrees</b>."
    its.append(mcq(q, "9 degrees", ["3 degrees", "6 degrees", "10 degrees"], e, rnd))
    # 17: freezer and fridge
    q = "A freezer is set to " + deg(-18) + ". The fridge is " + deg(4) + ". How many degrees colder is the freezer than the fridge?"
    e = "From 4 down to 0 is 4 degrees. From 0 down to " + M + "18 is 18 degrees. 4 + 18 = <b>22 degrees</b>."
    its.append(mcq(q, "22 degrees", ["14 degrees", "18 degrees", "23 degrees"], e, rnd))
    # 18: record low
    q = ("The lowest temperature ever recorded in Canada is " + deg(-63) + ", at Snag, Yukon, in 1947. "
         "One January morning in Winnipeg was " + deg(-28) + ". How many degrees colder is the record?")
    e = ("Both are below 0. From " + M + "28 down to " + M + "63 is 63 " + M + " 28 = <b>35 degrees</b>. "
         "Do not add 63 and 28: both temperatures are on the same side of 0.")
    its.append(mcq(q, "35 degrees", ["91 degrees", "36 degrees", "63 degrees"], e, rnd))
    # 19: golf
    a, b = P.next(), P.next()
    q = ("In golf, par is 0. %s finished 4 strokes under par. %s finished 1 stroke over par. "
         "Which integer shows %s’s score?" % (a[0], b[0], a[0]))
    e = "Under par is negative and over par is positive. %s is 4 under par: <b>%s4</b>. (%s’s score is 1.)" % (a[0], M, b[0])
    its.append(mcq_v(q, -4, [4, 1, -1], e, rnd))
    # 20: trivia score
    q = ("In a class trivia game, a team starts with 0 points. They lose 3 points, win 5 points, then lose 4 points. "
         "What is their score now?")
    e = "Start at 0. Back 3 is " + M + "3. On 5 is 2. Back 4 is " + M + "2. The score is <b>" + M + "2</b>."
    its.append(mcq_v(q, -2, [2, -12, 12], e, rnd))
    assert len(its) == 20
    return {"title": "Integer word problems", "items": its}


# ============================================================ lesson
def body_html():
    nl1 = NL(-10, 10, 2, 10).point(-6, "C")
    by2 = nl1.svg("number line from " + M + "10 to 10 counting by 2 with C at " + M + "6")
    th = thermo_svg(-30, 10, 5, 10, -15)
    nl2 = NL(-8, 2, 1, 1, gap=30).point(-7, "P").point(-2, "Q")
    cmp_ = nl2.svg("number line from " + M + "8 to 2 with P at " + M + "7 and Q at " + M + "2")
    nl4 = NL(-6, 6, 1, 1, gap=26).point(-4, "A").point(4, "B")
    opp = nl4.svg("number line from " + M + "6 to 6 with A at " + M + "4 and B at 4")
    nl3 = NL(-4, 3, 1, 1, gap=36).point(-3).point(2).hop(-3, 2, "5 steps")
    hop = nl3.svg("number line from " + M + "4 to 3 with 5 hops from " + M + "3 to 2")
    return (
        "<h2>What are integers?</h2>"
        "<p><b>Integers</b> are the whole numbers, their opposites and 0: … " + M + "3, " + M + "2, " + M + "1, 0, 1, 2, 3 … "
        "A negative number has a minus sign. " + M + "8 is read “negative 8”.</p>"
        "<p>Integers describe two opposite directions. <b>0</b> is the starting point between them. It is neither positive nor negative.</p>" +
        table(["Situation", "Positive", "0 means", "Negative"], [
            ["Temperature", "above zero: " + deg(12), "water freezes", "below zero: " + deg(-25)],
            ["Height", "above sea level: 5959" + NBSP + "m", "sea level", "below sea level: " + metres(-18)],
            ["Money", "saved: $20", "nothing saved or owed", "owing: " + money(-15)],
            ["Golf", "3 over par: 3", "par", "2 under par: " + M + "2"],
        ]) +
        ex("Example 1", "At 7 a.m. in Winnipeg, it is 24 degrees below zero. Which integer shows the temperature?",
           "“Below zero” is the negative direction.", deg(-24)) +
        "<h2>Horizontal and vertical number lines</h2>"
        "<p>On a horizontal number line, positive integers are to the <b>right</b> of 0 and negative integers are to the "
        "<b>left</b>. On a vertical number line, like a thermometer, positive integers are <b>above</b> 0 and negative "
        "integers are <b>below</b>. Before you read a point, work out what each tick mark is worth.</p>"
        "<figure class='sn-fig'>" + by2 +
        "<figcaption>There are 5 spaces from 0 to 10, so each tick mark is 2. C is 3 tick marks left of 0: " + M + "2, " +
        M + "4, " + M + "6. So C = " + M + "6, not " + M + "3.</figcaption></figure>"
        "<figure class='sn-fig'>" + th +
        "<figcaption>The labels count by 10 and each tick mark is 5 degrees. The red column ends 1 tick mark below " + M +
        "10, so the temperature is " + deg(-15) + ".</figcaption></figure>"
        "<h2>Compare and order integers</h2>"
        "<p>The farther <b>left</b> (or the farther <b>down</b>) a number is, the <b>less</b> it is. So every negative number "
        "is less than 0, and " + M + "7 is less than " + M + "2.</p>"
        "<figure class='sn-fig'>" + cmp_ +
        "<figcaption>P (" + M + "7) is to the left of Q (" + M + "2), so " + M + "7 &lt; " + M + "2. "
        "7 is bigger than 2, but " + M + "7 is less than " + M + "2.</figcaption></figure>" +
        ex("Example 2", "Order from least to greatest: 3, " + M + "5, 0, " + M + "8",
           "Start with the number farthest left. " + M + "8 is farther left than " + M + "5.",
           M + "8, " + M + "5, 0, 3") +
        "<h2>Opposite integers</h2>"
        "<p><b>Opposites</b> are the same distance from 0, on opposite sides. The opposite of 4 is " + M + "4, and the "
        "opposite of " + M + "4 is 4. The opposite of 0 is 0.</p>"
        "<figure class='sn-fig'>" + opp +
        "<figcaption>A (" + M + "4) and B (4) are both 4 units from 0, so they are opposites. They are 8 units apart.</figcaption></figure>"
        "<h2>Changes on a number line</h2>"
        "<p>A rise, a deposit or going up moves right (or up). A fall, spending or going down moves left (or down). "
        "When you pass 0, <b>0 counts as a step</b>.</p>"
        "<figure class='sn-fig'>" + hop +
        "<figcaption>The temperature is " + deg(-3) + " and rises 5 degrees: " + M + "2, " + M + "1, 0, 1, 2. "
        "The new temperature is " + deg(2) + ".</figcaption></figure>" +
        ex("Example 3", "Maya has $10 in her account. She pays a $25 bill, and the balance goes below zero. What is her balance?",
           "Count back 25 from 10: 10 takes you to $0, then 15 more.", money(-15) + " (she owes $15)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing 15 for “owing $15”", "Owing, below zero, below sea level and spending are negative: " + M + "15"],
            [M + "7 &gt; " + M + "2 because 7 &gt; 2", "Farther left is less: " + M + "7 &lt; " + M + "2"],
            ["Counting each tick as 1 when the scale counts by 2 or 5", "Find the tick value first: label difference ÷ spaces"],
            ["Thinking the opposite of " + M + "6 is 0", "Go the same distance to the other side of 0: 6"],
            ["Skipping 0: " + M + "3 up 5 is 3", "Count 0 as a step: " + M + "2, " + M + "1, 0, 1, 2"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about integers in the Ontario math curriculum?",
     "a": "In Grade 6, students read and represent integers on horizontal and vertical number lines, and compare and order them, using contexts like temperature, sea level and money. Adding and subtracting integers comes in Grade 7."},
    {"q": "How do you explain negative numbers to a Grade 6 child?",
     "a": "Negative numbers show the opposite direction from 0, like below zero on a thermometer, below sea level or money you owe. On a number line they are to the left of 0, or below 0 on a vertical line."},
    {"q": "Is −7 bigger or smaller than −2?",
     "a": "−7 is smaller. It is farther left on the number line, just as −7 °C is colder than −2 °C, so −7 < −2."},
    {"q": "What is the opposite of an integer?",
     "a": "The opposite is the integer the same distance from 0 on the other side. The opposite of −9 is 9, the opposite of 9 is −9, and the opposite of 0 is 0."},
]


def gen_unit():
    rnd = random.Random(36802)
    P = People(rnd)
    sets = [set_situations(rnd, P), set_read(rnd, P), set_compare(rnd, P), set_opposites(rnd, P), set_words(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "integers", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Integers: Number Lines, Thermometers, Comparing, Ordering and Opposites",
        "seo_title": "Grade 6 Integers Worksheets: Number Lines, Comparing and Ordering (Free, Answer Key)",
        "short_title": "Integers",
        "domain": "Number",
        "standard_code": "Grade 6: Number, B1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read and represent integers, using a variety of tools and strategies, including horizontal and vertical number lines, and compare and order integers",
        "meta_desc": "Free Grade 6 math worksheets on integers for the Ontario curriculum: negative numbers in winter temperatures, sea level and bank balances, horizontal and vertical number lines, comparing and ordering, and opposites. 100 questions with an answer key, good EQAO practice.",
        "key_big": "Negative numbers are to the left of 0 (or below it), so −7 < −2.",
        "key_sub": "Below zero, below sea level and money owed are negative. The farther left on the number line, the less the number. Opposites like −4 and 4 are the same distance from 0.",
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
