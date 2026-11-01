# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Multiplicative Comparison and Multistep Word Problems (4.OA.A.1–3)
  python tools/gen_us_math_g4_comparison_problems.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 4 style: 4536 -> 4,536."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def two(self):
        a = self.next()
        b = self.next()
        return dict(A=a[0], heA=a[1], HeA=cap(a[1]), hisA=a[2], B=b[0], heB=b[1], HeB=cap(b[1]), hisB=b[2])


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=True):
    """Approximate text width in px (Arial). Commas are narrow."""
    t = str(t)
    return (len(t) - t.count(",") * 0.6) * fs * (0.6 if bold else 0.56)


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def unit(u, n):
    """u is '$' or (one, many)."""
    if u == "$":
        return "$" + f(n)
    return "%s %s" % (f(n), u[0] if n == 1 else u[1])


def nocarry(a, k):
    """Forgot to regroup: write only the ones digit of each product (1,875 × 4 -> 4,280)."""
    ds = [int(c) for c in reversed(str(a))]
    out = 0
    for i, d in enumerate(ds):
        p = d * k
        out += (p if i == len(ds) - 1 else p % 10) * 10 ** i
    return out


# ------------------------------------------------------------ comparison bar model
def bar_svg(la, lb, k, top, cell, total, label=None):
    """Two bars: la has one part (top), lb has k equal parts (cell in each), bracket under lb with total."""
    fs = 16
    lw = max(tw(la, fs), tw(lb, fs)) + 14
    x0 = 14 + lw
    cw = max(34, tw(top, fs) + 14, tw(cell, fs) + 14)
    bh, y1 = 32, 6
    y2 = y1 + bh + 12
    s = []
    s.append(text(x0 - 8, y1 + bh / 2 + 6, la, anchor="end"))
    s.append(text(x0 - 8, y2 + bh / 2 + 6, lb, anchor="end"))
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, y1, cw, bh, FILL, GREEN))
    s.append(text(x0 + cw / 2, y1 + bh / 2 + 6, top, col=RED if top == "?" else INK))
    for i in range(k):
        x = x0 + i * cw
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x, y2, cw, bh, FILL, GREEN))
        if cell:
            s.append(text(x + cw / 2, y2 + bh / 2 + 6, cell, col=RED if cell == "?" else INK))
    xe = x0 + k * cw
    yb = y2 + bh + 6
    s.append("<path d='M%.1f %d v8 H%.1f v-8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, yb, xe, INK))
    cx = (x0 + xe) / 2
    s.append(text(cx, yb + 28, total, col=RED if total == "?" else INK))
    W = max(xe, cx + tw(total, fs) / 2) + 8
    H = yb + 36
    return svg_wrap(int(W + 0.99), H, "".join(s), label or "comparison bar model: %s and %s" % (la, lb))


# ------------------------------------------------------------ set 1: comparison statements and equations
def set_statements(rnd, P):
    its = []
    pairs = [(k, s) for k in range(3, 10) for s in range(3, 10) if k != s]
    rnd.shuffle(pairs)
    used = set()

    def take():
        while True:
            k, s = pairs.pop(0)
            if k * s in used:
                continue
            used.add(k * s)
            return k, s, k * s

    def eq_choices(b, k, s):
        return "%d = %d × %d" % (b, k, s), ["%d = %d × %d" % (s, k, b), "%d = %d + %d" % (b, k, s), "%d = %d × %d" % (k, b, s)]

    # a) statement -> equation (4 plain, 2 in a story)
    for _ in range(4):
        k, s, b = take()
        good, bad = eq_choices(b, k, s)
        its.append(mcq("Which equation shows “%d is %d times as many as %d”?" % (b, k, s), good, bad,
                       "“%d times as many as %d” means %d groups of %d, so multiply: %d × %d = %d. The equation is %d = %d × %d."
                       % (k, s, k, s, k, s, b, b, k, s), rnd))
    n, he, his = P.next()
    k, s = rnd.choice([(4, 9), (5, 8), (4, 8), (5, 7)])
    b = k * s
    good, bad = eq_choices(b, k, s)
    its.append(mcq("%s is %d years old. %s aunt is %d times as old as %s. %s aunt is %d. Which equation compares their ages?"
                   % (n, s, cap(his), k, n, cap(his), b), good, bad,
                   "The aunt's age is %d times %s's age: %d × %d = %d. So %d = %d × %d." % (k, n, k, s, b, b, k, s), rnd))
    k, s = 7, 9
    b = k * s
    good, bad = eq_choices(b, k, s)
    its.append(mcq("A cat weighs %d pounds. A dog weighs %d times as much as the cat. The dog weighs %d pounds. "
                   "Which equation compares their weights?" % (s, k, b), good, bad,
                   "The dog weighs %d times as much as the cat: %d × %d = %d. So %d = %d × %d." % (k, k, s, b, b, k, s), rnd))
    # b) equation -> statement, both ways of reading it
    for i in range(4):
        k, s, b = take()
        if i < 2:
            good = "%d is %d times as many as %d" % (b, k, s)
            bad = ["%d is %d more than %d" % (b, k, s), "%d is %d times as many as %d" % (s, k, b), "%d is %d times as many as %d" % (k, s, b)]
            q = "Which sentence matches the equation <b>%d = %d × %d</b>?" % (b, k, s)
        else:
            good = "%d is %d times as many as %d" % (b, s, k)
            bad = ["%d is %d more than %d" % (b, s, k), "%d is %d times as many as %d" % (k, s, b), "%d is %d times as many as %d" % (s, k, b)]
            q = ("<b>%d = %d × %d</b> means %d is %d times as many as %d. What else does it mean?" % (b, k, s, b, k, s))
        its.append(mcq(q, good, bad,
                       "%d = %d × %d can be read two ways: %d is %d times as many as %d, and %d is %d times as many as %d. "
                       "“More than” would mean adding, not multiplying." % (b, k, s, b, k, s, b, s, k), rnd))
    # c) fill in the comparison
    for i in range(4):
        k, s, b = take()
        if i < 2:
            its.append(mcq("What number makes the sentence true?  <b>☐ is %d times as many as %d.</b>" % (k, s), str(b),
                           [str(s + k), str((k + 1) * s), str((k - 1) * s), str(b + 10)],
                           "%d times as many as %d is %d × %d = %d. Adding (%d + %d = %d) would give “%d more than %d”."
                           % (k, s, k, s, b, s, k, s + k, k, s), rnd))
        else:
            its.append(mcq("What number makes the sentence true?  <b>%d is ☐ times as many as %d.</b>" % (b, s), str(k),
                           [str(b - s), str(b + s), str(k + 1), str(k - 1)],
                           "Think: ☐ × %d = %d. %d × %d = %d, so %d is %d times as many as %d. "
                           "%d − %d = %d tells how many more, not how many times." % (s, b, k, s, b, b, k, s, b, s, b - s), rnd))
    # d) read a bar model
    for i in range(6):
        k, s, b = take()
        while k > 8:
            k, s, b = take()
        p = P.two()
        F = fig(bar_svg(p["A"], p["B"], k, str(s), str(s), str(b)))
        why = ("%s's bar is %d equal parts, and each part is the same as %s's bar (%d). "
               "So %s has %d times as many: %d × %d = %d." % (p["B"], k, p["A"], s, p["B"], k, k, s, b))
        if i % 2 == 0:
            good, bad = eq_choices(b, k, s)
            its.append(mcq(F + "Which equation matches the bar model?", good, bad, why + " The equation is %d = %d × %d." % (b, k, s), rnd))
        else:
            good = "%s has %d times as many as %s" % (p["B"], k, p["A"])
            bad = ["%s has %d times as many as %s" % (p["A"], k, p["B"]), "%s has %d more than %s" % (p["B"], k, p["A"]),
                   "%s has %d times as many as %s" % (p["B"], b, p["A"])]
            its.append(mcq(F + "What does the bar model show?", good, bad, why, rnd))
    rnd.shuffle(its)
    return {"title": "Times as many: statements and equations", "items": its}


# ------------------------------------------------------------ contexts for sets 2 and 3
# la/lb: short bar labels.  s: range of the smaller amount.  k: range of the factor.
# u: '$' or (one, many).  big: find the bigger amount.  small: find the smaller.  times: find how many times.
CTX = [
    dict(la="{A}", lb="{B}", s=(12, 95), k=(3, 9), u=("sticker", "stickers"),
         big="{A} has {s} stickers. {B} has {k} times as many stickers as {A}. How many stickers does {B} have?",
         small="{B} has {b} stickers. That is {k} times as many stickers as {A} has. How many stickers does {A} have?",
         times="{B} has {b} stickers. {A} has {s} stickers. How many times as many stickers as {A} does {B} have?"),
    dict(la="puppy", lb="mother", s=(5, 12), k=(3, 6), u=("pound", "pounds"),
         big="A puppy weighs {s} pounds. Its mother weighs {k} times as much as the puppy. How much does the mother weigh?",
         small="A mother dog weighs {b} pounds. That is {k} times as much as her puppy weighs. How much does the puppy weigh?",
         times="A mother dog weighs {b} pounds, and her puppy weighs {s} pounds. How many times as much as the puppy does the mother weigh?"),
    dict(la="bush", lb="tree", s=(3, 7), k=(4, 9), u=("foot", "feet"),
         big="A rose bush is {s} feet tall. An oak tree is {k} times as tall as the rose bush. How tall is the oak tree?",
         small="An oak tree is {b} feet tall. It is {k} times as tall as a rose bush. How tall is the rose bush?",
         times="An oak tree is {b} feet tall. A rose bush is {s} feet tall. How many times as tall as the bush is the tree?"),
    dict(la="game", lb="bike", s=(15, 60), k=(3, 8), u="$",
         big="A board game costs ${s}. A bike costs {k} times as much as the board game. How much does the bike cost?",
         small="A bike costs ${b}. That is {k} times as much as a board game costs. How much does the board game cost?",
         times="A bike costs ${b}. A board game costs ${s}. How many times as much as the game does the bike cost?"),
    dict(la="{A}", lb="{B}", s=(24, 95), k=(3, 9), u=("page", "pages"),
         big="{A} read {s} pages this week. {B} read {k} times as many pages as {A}. How many pages did {B} read?",
         small="{B} read {b} pages this week. That is {k} times as many pages as {A} read. How many pages did {A} read?",
         times="{B} read {b} pages this week, and {A} read {s} pages. How many times as many pages as {A} did {B} read?"),
    dict(la="{A}", lb="{B}", s=(6, 24), k=(3, 6), u=("mile", "miles"),
         big="{A} rode {hisA} bike {s} miles this month. {B} rode {k} times as far as {A}. How many miles did {B} ride?",
         small="{B} rode {hisB} bike {b} miles this month. That is {k} times as far as {A} rode. How many miles did {A} ride?",
         times="{B} rode {hisB} bike {b} miles this month, and {A} rode {s} miles. How many times as far as {A} did {B} ride?"),
    dict(la="cows", lb="chickens", s=(12, 48), k=(4, 9), u=("chicken", "chickens"), u_small=("cow", "cows"),
         big="A farm has {s} cows. It has {k} times as many chickens as cows. How many chickens does the farm have?",
         small="A farm has {b} chickens. That is {k} times as many chickens as cows. How many cows does the farm have?",
         times="A farm has {b} chickens and {s} cows. How many times as many chickens as cows does the farm have?"),
    dict(la="town", lb="city", s=(1050, 2400), k=(3, 4), u=("person", "people"),
         big="A town has {s} people. A nearby city has {k} times as many people as the town. How many people live in the city?",
         small="A city has {b} people. That is {k} times as many people as a nearby town has. How many people live in the town?",
         times="A city has {b} people, and a nearby town has {s} people. How many times as many people as the town does the city have?"),
    dict(la="{A}", lb="{B}", s=(115, 480), k=(2, 5), u=("point", "points"),
         big="{A} scored {s} points in a video game. {B} scored {k} times as many points as {A}. How many points did {B} score?",
         small="{B} scored {b} points in a video game. That is {k} times as many points as {A} scored. How many points did {A} score?",
         times="{B} scored {b} points in a video game, and {A} scored {s} points. How many times as many points as {A} did {B} score?"),
    dict(la="red", lb="blue", s=(8, 25), k=(3, 7), u=("inch", "inches"),
         big="A red ribbon is {s} inches long. A blue ribbon is {k} times as long as the red ribbon. How long is the blue ribbon?",
         small="A blue ribbon is {b} inches long. It is {k} times as long as a red ribbon. How long is the red ribbon?",
         times="A blue ribbon is {b} inches long, and a red ribbon is {s} inches long. How many times as long as the red ribbon is the blue ribbon?"),
    dict(la="bucket", lb="bathtub", s=(4, 6), k=(7, 9), u=("gallon", "gallons"),
         big="A bucket holds {s} gallons of water. A bathtub holds {k} times as much water as the bucket. How many gallons does the bathtub hold?",
         small="A bathtub holds {b} gallons of water. That is {k} times as much as a bucket holds. How many gallons does the bucket hold?",
         times="A bathtub holds {b} gallons of water, and a bucket holds {s} gallons. How many times as much water as the bucket does the bathtub hold?"),
    dict(la="muffins", lb="cookies", s=(36, 140), k=(3, 8), u=("cookie", "cookies"), u_small=("muffin", "muffins"),
         big="A bakery sold {s} muffins on Saturday. It sold {k} times as many cookies as muffins. How many cookies did it sell?",
         small="A bakery sold {b} cookies on Saturday. That is {k} times as many cookies as muffins. How many muffins did it sell?",
         times="A bakery sold {b} cookies and {s} muffins on Saturday. How many times as many cookies as muffins did it sell?"),
    dict(la="small", lb="big", s=(8, 24), k=(3, 7), u=("fish", "fish"),
         big="The small tank at a pet store has {s} fish. The big tank has {k} times as many fish as the small tank. How many fish are in the big tank?",
         small="The big tank at a pet store has {b} fish. That is {k} times as many fish as the small tank has. How many fish are in the small tank?",
         times="The big tank at a pet store has {b} fish, and the small tank has {s} fish. How many times as many fish as the small tank does the big tank have?"),
    dict(la="house", lb="office", s=(24, 36), k=(5, 9), u=("foot", "feet"),
         big="A house is {s} feet tall. An office building is {k} times as tall as the house. How tall is the office building?",
         small="An office building is {b} feet tall. It is {k} times as tall as a house. How tall is the house?",
         times="An office building is {b} feet tall, and a house is {s} feet tall. How many times as tall as the house is the office building?"),
    dict(la="Monday", lb="Saturday", s=(15, 30), k=(2, 4), u=("minute", "minutes"),
         big="{A} practiced piano for {s} minutes on Monday. On Saturday, {heA} practiced {k} times as long. How many minutes did {heA} practice on Saturday?",
         small="{A} practiced piano for {b} minutes on Saturday. That is {k} times as long as {heA} practiced on Monday. How many minutes did {heA} practice on Monday?",
         times="{A} practiced piano for {b} minutes on Saturday and {s} minutes on Monday. How many times as long did {heA} practice on Saturday?"),
    dict(la="DVDs", lb="books", s=(350, 980), k=(6, 9), u=("book", "books"), u_small=("DVD", "DVDs"),
         big="A library has {s} DVDs. It has {k} times as many books as DVDs. How many books does the library have?",
         small="A library has {b} books. That is {k} times as many books as DVDs. How many DVDs does the library have?",
         times="A library has {b} books and {s} DVDs. How many times as many books as DVDs does the library have?"),
    dict(la="theater", lb="hall", s=(120, 350), k=(3, 6), u=("seat", "seats"),
         big="A small theater has {s} seats. A concert hall has {k} times as many seats as the theater. How many seats does the concert hall have?",
         small="A concert hall has {b} seats. That is {k} times as many seats as a small theater has. How many seats does the small theater have?",
         times="A concert hall has {b} seats, and a small theater has {s} seats. How many times as many seats as the theater does the hall have?"),
    dict(la="pear", lb="apple", s=(16, 85), k=(3, 8), u=("apple tree", "apple trees"), u_small=("pear tree", "pear trees"),
         big="An orchard has {s} pear trees. It has {k} times as many apple trees as pear trees. How many apple trees does it have?",
         small="An orchard has {b} apple trees. That is {k} times as many apple trees as pear trees. How many pear trees does it have?",
         times="An orchard has {b} apple trees and {s} pear trees. How many times as many apple trees as pear trees does it have?"),
    dict(la="{A}", lb="{B}", s=(14, 85), k=(3, 9), u="$",
         big="{A} saved ${s}. {B} saved {k} times as much money as {A}. How much money did {B} save?",
         small="{B} saved ${b}. That is {k} times as much money as {A} saved. How much money did {A} save?",
         times="{B} saved ${b}, and {A} saved ${s}. How many times as much money as {A} did {B} save?"),
    dict(la="tablet", lb="laptop", s=(110, 260), k=(3, 5), u="$",
         big="A tablet costs ${s}. A laptop costs {k} times as much as the tablet. How much does the laptop cost?",
         small="A laptop costs ${b}. That is {k} times as much as a tablet costs. How much does the tablet cost?",
         times="A laptop costs ${b}, and a tablet costs ${s}. How many times as much as the tablet does the laptop cost?"),
    dict(la="dolphin", lb="whale", s=(10, 12), k=(8, 9), u=("foot", "feet"),
         big="A dolphin is {s} feet long. A blue whale is {k} times as long as the dolphin. How long is the blue whale?",
         small="A blue whale is {b} feet long. It is {k} times as long as a dolphin. How long is the dolphin?",
         times="A blue whale is {b} feet long, and a dolphin is {s} feet long. How many times as long as the dolphin is the whale?"),
    dict(la="Monday", lb="Saturday", s=(215, 890), k=(3, 9), u=("visitor", "visitors"),
         big="A museum had {s} visitors on Monday. On Saturday, it had {k} times as many visitors. How many visitors came on Saturday?",
         small="A museum had {b} visitors on Saturday. That is {k} times as many visitors as on Monday. How many visitors came on Monday?",
         times="A museum had {b} visitors on Saturday and {s} visitors on Monday. How many times as many visitors came on Saturday?"),
    dict(la="pickup", lb="dump", s=(1500, 2400), k=(4, 6), u=("pound", "pounds"),
         big="A pickup truck can carry {s} pounds. A dump truck can carry {k} times as much as the pickup. How many pounds can the dump truck carry?",
         small="A dump truck can carry {b} pounds. That is {k} times as much as a pickup truck can carry. How many pounds can the pickup carry?",
         times="A dump truck can carry {b} pounds, and a pickup truck can carry {s} pounds. How many times as much as the pickup can the dump truck carry?"),
]


def fill(t, c, p, s, k, b):
    d = dict(p)
    d.update(s=f(s), k=k, b=f(b))
    return t.format(**d)


def labels(c, p):
    return c["la"].format(**p), c["lb"].format(**p)


def item_big(c, rnd, P, used, figure):
    while True:
        s, k = rnd.randint(*c["s"]), rnd.randint(*c["k"])
        if figure and (s > 99 or k > 8):
            continue
        if (s, k) not in used and s % 10:
            break
    used.add((s, k))
    b = k * s
    p = P.two()
    U = lambda v: unit(c["u"], v)
    q = fill(c["big"], c, p, s, k, b)
    if figure:
        la, lb = labels(c, p)
        q = fig(bar_svg(la, lb, k, f(s), f(s), "?")) + q
    ph = re.search(r"%d times as \w+" % k, q).group(0)
    V = lambda v: "$" + f(v) if c["u"] == "$" else f(v)
    e = ("“%s” means %d equal parts, each the size of %s. Multiply: %d × %s = %s. "
         "Adding %s + %d would answer “%d more”, which is a different question. Answer: %s."
         % (ph, k, V(s), k, V(s), V(b), V(s), k, k, U(b)))
    cands = [U(s + k), U(b + s), U(b - s), U(nocarry(s, k)) if nocarry(s, k) != b else U(b + 10), U(b + 10)]
    return mcq(q, U(b), cands, e, rnd)


def item_small(c, rnd, P, used, figure):
    while True:
        s, k = rnd.randint(*c["s"]), rnd.randint(*c["k"])
        if figure and (s > 99 or k > 8):
            continue
        if (s, k) not in used and s % 10 and k * s - k > 1:
            break
    used.add((s, k))
    b = k * s
    p = P.two()
    us = c.get("u_small", c["u"])
    U = lambda v: unit(us, v)
    q = fill(c["small"], c, p, s, k, b)
    if figure:
        la, lb = labels(c, p)
        q = fig(bar_svg(la, lb, k, "?", "", f(b))) + q
    V = lambda v: "$" + f(v) if c["u"] == "$" else f(v)
    e = ("The bigger amount, %s, is %d equal parts. Each part is the smaller amount, so divide: %s ÷ %d = %s. "
         "Check: %d × %s = %s. Answer: %s." % (V(b), k, V(b), k, V(s), k, V(s), V(b), U(s)))
    cands = [U(b - k), U(b * k), U(b + k), U(s + 1), U(s - 1)]
    return mcq(q, U(s), cands, e, rnd)


def item_times(c, rnd, P, used):
    lo, hi = c["s"]
    while True:
        if hi <= 15:
            s = rnd.randint(lo, hi)
        elif hi < 100:
            s = rnd.choice([v for v in range(lo, hi + 1) if v % 5 == 0])
        else:
            s = rnd.choice([v for v in range(lo, hi + 1) if v % 100 == 0] or [v for v in range(lo, hi + 1) if v % 10 == 0])
        k = rnd.randint(*c["k"])
        if (s, k) not in used:
            break
    used.add((s, k))
    b = k * s
    p = P.two()
    q = fill(c["times"], c, p, s, k, b)
    e = ("To find “how many times”, divide the bigger amount by the smaller one. Think: ☐ × %s = %s. "
         "%d × %s = %s, so the answer is %d. %s − %s = %s tells how many more, not how many times."
         % (f(s), f(b), k, f(s), f(b), k, f(b), f(s), f(b - s)))
    cands = [f(b - s), f(b + s), str(k + 1), str(k - 1) if k > 2 else str(k + 2)]
    return mcq(q, str(k), cands, e, rnd)


def set_bigger(rnd, P):
    ctx = rnd.sample(CTX, 20)
    used = set()
    figs = [i for i, c in enumerate(ctx) if c["s"][0] <= 60 and c["k"][0] <= 8][:5]
    its = [item_big(c, rnd, P, used, i in figs) for i, c in enumerate(ctx)]
    rnd.shuffle(its)
    return {"title": "Find the bigger amount: multiply", "items": its}


def set_smaller(rnd, P):
    ctx = rnd.sample(CTX, 20)
    used = set()
    its = []
    nfig = 0
    for i, c in enumerate(ctx):
        if i % 2 == 0:
            figure = nfig < 4 and c["s"][0] <= 60 and c["k"][0] <= 8
            nfig += figure
            its.append(item_small(c, rnd, P, used, figure))
        else:
            its.append(item_times(c, rnd, P, used))
    rnd.shuffle(its)
    return {"title": "Find the smaller amount or how many times: divide", "items": its}


# ------------------------------------------------------------ set 4: times as many or how many more?
# (more wording, times wording, question, how-many-more question, unit)
HAS = [("shells", "shell"), ("marbles", "marble"), ("rocks", "rock"), ("stamps", "stamp"), ("baseball cards", "baseball card"),
       ("beads", "bead"), ("toy cars", "toy car"), ("comic books", "comic book"), ("seashells", "seashell"), ("crayons", "crayon")]
MEAS = [
    ("{A} made a paper chain {s} inches long. {B} made a chain {d} inches longer than {A}'s chain.",
     "{A} made a paper chain {s} inches long. {B} made a chain {d} times as long as {A}'s chain.",
     "How long is {B}'s chain?", "How much longer is {B}'s chain than {A}'s chain?", ("inch", "inches")),
    ("{A} biked {s} miles this month. {B} biked {d} miles farther than {A}.",
     "{A} biked {s} miles this month. {B} biked {d} times as far as {A}.",
     "How far did {B} bike?", "How much farther did {B} bike than {A}?", ("mile", "miles")),
    ("A book costs ${s}. A video game costs ${d} more than the book.",
     "A book costs ${s}. A video game costs {d} times as much as the book.",
     "How much does the video game cost?", "How much more does the video game cost than the book?", "$"),
    ("A small fish tank holds {s} gallons. A big tank holds {d} more gallons than the small tank.",
     "A small fish tank holds {s} gallons. A big tank holds {d} times as much water as the small tank.",
     "How many gallons does the big tank hold?", "How many more gallons does the big tank hold than the small tank?", ("gallon", "gallons")),
]


def has_ctx(T, one):
    return ("{A} has {s} %s. {B} has {d} more %s than {A}." % (T, T),
            "{A} has {s} %s. {B} has {d} times as many %s as {A}." % (T, T),
            "How many %s does {B} have?" % T, "How many more %s does {B} have than {A}?" % T, (one, T))


def set_more_or_times(rnd, P):
    ctx = [has_ctx(T, one) for T, one in HAS] + MEAS
    rnd.shuffle(ctx)
    its = []
    used = set()

    def nums(lo=6, hi=30):
        while True:
            s, d = rnd.randint(lo, hi), rnd.randint(3, 9)
            if (s, d) not in used and s != d and s % 10:
                used.add((s, d))
                return s, d

    plan = ["more"] * 6 + ["times"] * 6 + ["diff"] * 4
    for i, kind in enumerate(plan):
        more_t, times_t, q_t, diff_t, u = ctx[i % len(ctx)]
        p = P.two()
        s, d = nums()
        U = lambda v: unit(u, v)
        fm = lambda t: t.format(s=s, d=d, **p)
        if kind == "more":
            ans = s + d
            q = fm(more_t) + " " + fm(q_t)
            ph = re.search(r"(?<![0-9,$])\$?%d [^.]*?(more|farther|longer)" % d, q).group(0)
            e = ("“%s” means add %d: %d + %d = %d. Multiplying (%d × %d = %d) would answer a “%d times as …” question. Answer: %s."
                 % (ph, d, s, d, ans, d, s, d * s, d, U(ans)))
            cands = [U(d * s), U(s - d) if s - d > 1 else U(ans + 10), U(d), U(ans + 10)]
        elif kind == "times":
            ans = d * s
            q = fm(times_t) + " " + fm(q_t)
            e = ("“%d times as many” means %d groups of %d: %d × %d = %d. Adding (%d + %d = %d) would answer “%d more”. Answer: %s."
                 % (d, d, s, d, s, ans, s, d, s + d, d, U(ans)))
            ph = re.search(r"%d times as \w+" % d, q).group(0)
            e = e.replace("“%d times as many” means" % d, "“%s” means" % ph, 1)
            cands = [U(s + d), U(ans + s), U(ans - s), U(ans + 10)]
        else:
            b = d * s
            ans = b - s
            q = fm(times_t) + " " + fm(diff_t)
            e = ("Step 1: find the bigger amount: %d × %d = %d. Step 2: “how many more” means subtract: %d − %d = %d. "
                 "%d is the bigger amount, not the difference. Answer: %s." % (d, s, b, b, s, ans, b, U(ans)))
            cands = [U(b), U(b + s), U(d * s - d), U(ans + 10)]
        its.append(mcq(q, U(ans), cands, e, rnd))
    # which equation fits? one "more", one "times"
    n1 = P.two()
    s, d = nums(8, 15)
    its.append(mcq("%s has %d stickers. %s has %d more stickers than %s. Which equation finds <b>a</b>, the number of stickers %s has?"
                   % (n1["A"], s, n1["B"], d, n1["A"], n1["B"]), "a = %d + %d" % (s, d),
                   ["a = %d × %d" % (d, s), "a = %d − %d" % (s, d), "%d = a + %d" % (s, d)],
                   "“%d more than %d” means add: a = %d + %d = %d. “%d times as many” would be a = %d × %d." % (d, s, s, d, s + d, d, d, s), rnd))
    n1 = P.two()
    s, d = nums(8, 15)
    its.append(mcq("%s picked %d strawberries. %s picked %d times as many strawberries as %s. Which equation finds <b>p</b>, the number %s picked?"
                   % (n1["A"], s, n1["B"], d, n1["A"], n1["B"]), "p = %d × %d" % (d, s),
                   ["p = %d + %d" % (s, d), "%d = %d × p" % (s, d), "p = %d − %d" % (s, d)],
                   "“%d times as many as %d” means multiply: p = %d × %d = %d. “%d more” would be p = %d + %d." % (d, s, d, s, d * s, d, s, d), rnd))
    # which sentence is true?
    k, s = 5, 8
    b = k * s
    its.append(mcq("A school bus is %d feet long. A car is %d feet long. Which sentence is true?" % (b, s),
                   "The bus is %d times as long as the car" % k,
                   ["The bus is %d feet longer than the car" % k, "The car is %d times as long as the bus" % k,
                    "The bus is %d times as long as the car" % (b - s)],
                   "%d × %d = %d, so the bus is %d times as long as the car. It is %d − %d = %d feet longer, not %d feet longer."
                   % (k, s, b, k, b, s, b - s, k), rnd))
    p = P.two()
    k, s = 7, 6
    b = k * s
    its.append(mcq("%s picked %d apples. %s picked %d apples. Which sentence is true?" % (p["A"], b, p["B"], s),
                   "%s picked %d more apples than %s" % (p["A"], b - s, p["B"]),
                   ["%s picked %d more apples than %s" % (p["A"], k, p["B"]), "%s picked %d times as many apples as %s" % (p["A"], b - s, p["B"]),
                    "%s picked %d more apples than %s" % (p["B"], b - s, p["A"])],
                   "%d − %d = %d, so %s picked %d more. %s also picked %d times as many (%d × %d = %d), but not %d more."
                   % (b, s, b - s, p["A"], b - s, p["A"], k, k, s, b, k), rnd))
    rnd.shuffle(its)
    return {"title": "Times as many or how many more?", "items": its}


# ------------------------------------------------------------ set 5: multistep problems
def steps_text(steps, ans):
    return " ".join("Step %d: %s" % (i + 1, t) for i, t in enumerate(steps)) + " So the answer is %s." % ans


def m_both(r, P, v):
    k = r.randint(3, 6)
    s = r.randint(45, 95) if v == 0 else r.randint(14, 38)
    ks = k * s
    if v == 0:
        q = ("The third grade read %d books this month. The fourth grade read %d times as many books as the third grade. "
             "How many books did the two grades read in all?" % (s, k))
        u, L, who = ("book", "books"), "b", "Fourth grade"
    else:
        q = "A pond has %d frogs. It has %d times as many tadpoles as frogs. How many frogs and tadpoles are in the pond in all?" % (s, k)
        u, L, who = ("animal", "animals"), "p", "Tadpoles"
    t = s + ks
    return dict(q=q, ans=t, u=u, steps=["%s: %d × %d = %d." % (who, k, s, ks), "In all: %d + %d = %d." % (s, ks, t)],
                wrong=[ks, 2 * s + k, ks - s, t + 10], L=L,
                eq="%d + %d × %d = %s" % (s, k, s, L),
                eq_wrong=["%d + %d + %d = %s" % (s, k, s, L), "%d × %d = %s" % (k, s, L), "%d × %d − %d = %s" % (k, s, s, L)])


def m_give(r, P, v):
    p = P.two()
    k = r.randint(3, 6)
    s = r.randint(14, 45)
    ks = k * s
    g = r.randint(10, ks - 12)
    if v == 0:
        q = ("%s has %d trading cards. %s has %d times as many cards as %s. Then %s gives %d cards to %s cousin. "
             "How many cards does %s have now?" % (p["A"], s, p["B"], k, p["A"], p["B"], g, p["hisB"], p["B"]))
        u, L, st = ("card", "cards"), "c", ["%s's cards: %d × %d = %d." % (p["B"], k, s, ks), "After giving: %d − %d = %d." % (ks, g, ks - g)]
    else:
        q = ("A school garden grew %d carrots. It grew %d times as many radishes as carrots. The students picked %d radishes. "
             "How many radishes are still in the garden?" % (s, k, g))
        u, L, st = ("radish", "radishes"), "r", ["Radishes: %d × %d = %d." % (k, s, ks), "Still in the garden: %d − %d = %d." % (ks, g, ks - g)]
    return dict(q=q, ans=ks - g, u=u, steps=st,
                wrong=[ks, ks + g, s + k - g if s + k - g > 1 else ks - s, ks - g + 10], L=L,
                eq="%d × %d − %d = %s" % (k, s, g, L),
                eq_wrong=["%d + %d − %d = %s" % (k, s, g, L), "%d × %d + %d = %s" % (k, s, g, L), "%d × %d = %s" % (k, s, L)])


def m_change(r, P, v):
    n, he, his = P.next()
    while True:
        s, k = r.randint(8, 16), r.randint(3, 6)
        if 40 <= k * s <= 92:
            break
    ks = k * s
    if v == 0:
        q = ("A T-shirt costs $%d. A jacket costs %d times as much as the T-shirt. %s pays for the jacket with a $100 bill. "
             "How much change does %s get?" % (s, k, n, he))
        st = ["The jacket: %d × $%d = $%d." % (k, s, ks), "Change: $100 − $%d = $%d." % (ks, 100 - ks)]
    else:
        q = ("A sandwich costs $%d. A party platter costs %d times as much as the sandwich. %s pays for the platter with a $100 bill. "
             "How much change does %s get?" % (s, k, n, he))
        st = ["The platter: %d × $%d = $%d." % (k, s, ks), "Change: $100 − $%d = $%d." % (ks, 100 - ks)]
    return dict(q=q, ans=100 - ks, u="$", steps=st, wrong=[ks, 100 - s - k, 100 - s, 100 - ks + 10], L="c",
                eq="100 − %d × %d = c" % (k, s),
                eq_wrong=["100 − %d − %d = c" % (k, s), "%d × %d = c" % (k, s), "100 + %d × %d = c" % (k, s)])


def m_coops(r, P, v):
    while True:
        s, k, n = r.randint(12, 30), r.randint(3, 6), r.randint(3, 8)
        if (k * s) % n == 0 and n != k and k * s // n > 2 and s % n:
            break
    ks = k * s
    if v == 0:
        q = ("A farm has %d ducks. It has %d times as many chickens as ducks. The chickens live in %d coops, with the same number "
             "in each coop. How many chickens live in each coop?" % (s, k, n))
        u, L, who, each = ("chicken", "chickens"), "c", "Chickens", "Each coop"
    else:
        q = ("One class made %d paper cranes. Another class made %d times as many. The second class hangs its cranes equally on "
             "%d strings. How many cranes are on each string?" % (s, k, n))
        u, L, who, each = ("crane", "cranes"), "c", "The second class", "Each string"
    return dict(q=q, ans=ks // n, u=u, steps=["%s: %d × %d = %d." % (who, k, s, ks), "%s: %d ÷ %d = %d." % (each, ks, n, ks // n)],
                wrong=[ks, ks - n, ks // n + k, ks * n], L=L,
                eq="%d × %d ÷ %d = %s" % (k, s, n, L),
                eq_wrong=["%d × %d − %d = %s" % (k, s, n, L), "%d + %d ÷ %d = %s" % (k, s, n, L), "%d × %d × %d = %s" % (k, s, n, L)])


def m_chain(r, P, v):
    s, k, m = r.randint(4, 7), r.randint(2, 4), r.randint(3, 5)
    t = s * k * m
    q = ("A small fish tank has %d fish. A medium tank has %d times as many fish as the small tank. A big tank has %d times as many "
         "fish as the medium tank. How many fish are in the big tank?" % (s, k, m))
    return dict(q=q, ans=t, u=("fish", "fish"), steps=["Medium tank: %d × %d = %d." % (k, s, k * s), "Big tank: %d × %d = %d." % (m, k * s, t)],
                wrong=[k * s, (k + m) * s, k * s + m, t + 10], L="f",
                eq="%d × (%d × %d) = f" % (m, k, s),
                eq_wrong=["%d + %d × %d = f" % (m, k, s), "%d × %d = f" % (k, s), "(%d + %d) × %d = f" % (m, k, s)])


def m_together(r, P, v):
    s, k = r.randint(6, 12), r.randint(3, 7)
    b = k * s
    if v == 0:
        q = ("A mother dog weighs %d pounds. That is %d times as much as her puppy weighs. How much do the mother and the puppy "
             "weigh together?" % (b, k))
        return dict(q=q, ans=b + s, u=("pound", "pounds"),
                    steps=["The puppy: %d ÷ %d = %d pounds." % (b, k, s), "Together: %d + %d = %d." % (b, s, b + s)],
                    wrong=[s, b + k * b, b - s, b + k], L="w",
                    eq="%d + %d ÷ %d = w" % (b, b, k),
                    eq_wrong=["%d + %d × %d = w" % (b, k, b), "%d ÷ %d = w" % (b, k), "%d − %d ÷ %d = w" % (b, b, k)])
    s = r.randint(22, 35)
    b = k * s
    q = "An office building is %d feet tall. That is %d times as tall as a house. How much taller is the office building than the house?" % (b, k)
    return dict(q=q, ans=b - s, u=("foot", "feet"),
                steps=["The house: %d ÷ %d = %d feet." % (b, k, s), "How much taller: %d − %d = %d." % (b, s, b - s)],
                wrong=[s, b - k, b + s, b - s + 10], L="t",
                eq="%d − %d ÷ %d = t" % (b, b, k),
                eq_wrong=["%d − %d = t" % (b, k), "%d ÷ %d = t" % (b, k), "%d + %d ÷ %d = t" % (b, b, k)])


def m_gift(r, P, v):
    p = P.two()
    while True:
        s, k = r.randint(8, 20), r.randint(2, 4)
        t = s + k * s
        g = r.randint(t // 2, t - 6)
        if g > k * s + 2:
            break
    q = ("%s saved $%d. %s saved %d times as much money as %s. Together they buy a gift that costs $%d. "
         "How much money do they have left?" % (p["A"], s, p["B"], k, p["A"], g))
    return dict(q=q, ans=t - g, u="$",
                steps=["%s saved %d × $%d = $%d." % (p["B"], k, s, k * s), "Together: $%d + $%d = $%d." % (s, k * s, t),
                       "Left: $%d − $%d = $%d." % (t, g, t - g)],
                wrong=[t, 2 * s + k - g if 2 * s + k - g > 1 else t + g, t + g, t - g + 10], L="m",
                eq="%d + %d × %d − %d = m" % (s, k, s, g),
                eq_wrong=["%d × %d − %d = m" % (k, s, g), "%d + %d + %d − %d = m" % (s, k, s, g), "%d + %d × %d + %d = m" % (s, k, s, g)])


def fmt(v, u):
    return unit(u, v)


def rem_items(rnd, P):
    its = []
    # 1) all the cans need a box: round up
    while True:
        s, k, d = rnd.randint(35, 68), rnd.randint(3, 5), rnd.choice([8, 9])
        ks = k * s
        q, r = divmod(ks, d)
        if r >= 2:
            break
    its.append(mcq("The third grade collected %d cans of food. The fourth grade collected %d times as many cans. The fourth grade "
                   "packs its cans in boxes of %d. How many boxes does it need for all its cans?" % (s, k, d),
                   unit(("box", "boxes"), q + 1),
                   [unit(("box", "boxes"), q), "%d R %d" % (q, r), unit(("box", "boxes"), ks), unit(("box", "boxes"), q + 2)],
                   steps_text(["Fourth grade cans: %d × %d = %d." % (k, s, ks), "%d ÷ %d = %d R %d." % (ks, d, q, r),
                               "%d boxes hold %d cans. The other %d cans still need a box, so add 1." % (q, q * d, r)],
                              unit(("box", "boxes"), q + 1)), rnd))
    # 2) full boxes only: leave the remainder out
    while True:
        s, k = rnd.randint(24, 45), rnd.randint(3, 4)
        ks = k * s
        q, r = divmod(ks, 6)
        if r >= 2:
            break
    its.append(mcq("A bakery made %d muffins in the morning. In the afternoon, it made %d times as many. It packs the afternoon "
                   "muffins in boxes of 6. How many boxes can it fill completely?" % (s, k),
                   unit(("box", "boxes"), q),
                   [unit(("box", "boxes"), q + 1), "%d R %d" % (q, r), unit(("box", "boxes"), ks), unit(("box", "boxes"), (s + ks) // 6)],
                   steps_text(["Afternoon muffins: %d × %d = %d." % (k, s, ks), "%d ÷ 6 = %d R %d." % (ks, q, r),
                               "The %d muffins left over are not enough to fill another box, so leave them out." % r],
                              unit(("box", "boxes"), q)), rnd))
    # 3) how many are left over: the remainder
    p = P.two()
    while True:
        s, k, d = rnd.randint(13, 25), rnd.randint(3, 5), rnd.choice([6, 7, 8])
        ks = k * s
        q, r = divmod(ks, d)
        if r >= 2 and r not in (q, d - r):
            break
    its.append(mcq("%s has %d marbles. %s has %d times as many marbles as %s. %s shares all of %s marbles equally among %d friends, "
                   "giving each friend as many as possible. How many marbles are left over?"
                   % (p["A"], s, p["B"], k, p["A"], p["B"], p["hisB"], d),
                   unit(("marble", "marbles"), r),
                   [unit(("marble", "marbles"), q), unit(("marble", "marbles"), d - r), "%d R %d" % (q, r), unit(("marble", "marbles"), ks)],
                   steps_text(["%s's marbles: %d × %d = %d." % (p["B"], k, s, ks), "%d ÷ %d = %d R %d. Each friend gets %d." % (ks, d, q, r, q),
                               "The question asks how many are left over. That is the remainder."], unit(("marble", "marbles"), r)), rnd))
    # 4) three steps: students and adults, then vans
    while True:
        s, k, d = rnd.randint(6, 9), rnd.randint(5, 7), rnd.choice([8, 9])
        t = s + k * s
        q, r = divmod(t, d)
        if r >= 2 and -(-k * s // d) != q + 1:
            break
    its.append(mcq("A school trip has %d adults. There are %d times as many students as adults. Each van holds %d people. "
                   "How many vans are needed for all the students and adults?" % (s, k, d),
                   unit(("van", "vans"), q + 1),
                   [unit(("van", "vans"), q), unit(("van", "vans"), -(-k * s // d)), "%d R %d" % (q, r), unit(("van", "vans"), q + 2)],
                   steps_text(["Students: %d × %d = %d." % (k, s, k * s), "Everyone: %d + %d = %d people." % (s, k * s, t),
                               "%d ÷ %d = %d R %d. The other %d people still need a van, so add 1." % (t, d, q, r, r)],
                              unit(("van", "vans"), q + 1)), rnd))
    return its


def r100(v):
    return int((v + 50) // 100 * 100)


def est_items(rnd, P):
    its = []
    S = [("A school library has %d picture books. The town library has %d times as many picture books. "
          "About how many picture books does the town library have? Round to the nearest hundred first.", "picture books"),
         ("A farm stand sold %d pounds of apples in September. In October, it sold %d times as many pounds. "
          "About how many pounds did it sell in October? Round to the nearest hundred first.", "pounds"),
         ("A small concert hall has %d seats. A stadium has %d times as many seats. "
          "About how many seats does the stadium have? Round to the nearest hundred first.", "seats")]
    done = set()
    for t, _ in S:
        while True:
            a, k = rnd.randint(250, 480), rnd.randint(4, 8)
            if a % 100 >= 55 and a % 10 and (r100(a), k) not in done:
                done.add((r100(a), k))
                break
        ra = r100(a)
        est = ra * k
        its.append(mcq(t % (a, k), "about %s" % f(est),
                       ["about %s" % f(v) for v in [ra, (ra - 100) * k, est * 10]],
                       "%d rounds to %d. %d × %d = %s. The exact answer, %d × %d = %s, is close to %s."
                       % (a, ra, k, ra, f(est), a, k, f(a * k), f(est)), rnd))
    checks = [("A pickup truck can carry %s pounds. A dump truck can carry %d times as much. %s says the dump truck can carry %s pounds. ",
               (1610, 2390), (4, 5), False),
              ("A school has %s students. The whole town has %d times as many children. %s says the town has %s children. ",
               (1120, 1480), (6, 7), True)]
    for t, ar, kr, ok in checks:
        n, he, his = P.next()
        while True:
            a, k = rnd.randint(*ar), rnd.randint(*kr)
            ra = int(round(a, -3))
            est = ra * k
            exact = a * k
            wrong = nocarry(a, k)
            if abs(a - ra) <= 400 and abs(exact - est) < est * 0.15 and (ok or abs(wrong - est) > est * 0.3):
                break
        claim = exact if ok else wrong
        good = ("Yes, it is close to %s" if ok else "No, it should be close to %s") % f(est)
        cands = [("No, it should be close to %s" if ok else "Yes, it is close to %s") % f(est),
                 "No, it should be close to %s" % f(ra), "Yes, it is close to %s" % f(r100(claim) // 1000 * 1000 if not ok else est * 10),
                 "No, it should be close to %s" % f(est * 10)]
        tail = ("%s answer, %s, is close to %s, so it is reasonable." % (cap(his), f(claim), f(est)) if ok else
                "%s answer, %s, is far from %s, so it is not reasonable. %s forgot to regroup. The exact answer is %s × %d = %s."
                % (cap(his), f(claim), f(est), n, f(a), k, f(exact)))
        its.append(mcq((t % (f(a), k, n, f(claim))) + "Use rounding to check. Is %s answer reasonable?" % his, good, cands,
                       "%s rounds to %s. Estimate: %d × %s = %s. %s" % (f(a), f(ra), k, f(ra), f(est), tail), rnd))
    return its


def set_multistep(rnd, P):
    its = []
    for fn in [m_both, m_give, m_change, m_chain, m_together, m_gift]:
        d = fn(rnd, P, 0)
        cands = [fmt(v, d["u"]) for v in d["wrong"] if v > 1]
        its.append(mcq(d["q"], fmt(d["ans"], d["u"]), cands, steps_text(d["steps"], fmt(d["ans"], d["u"])), rnd))
    for fn in [m_both, m_give, m_change, m_coops, m_together]:
        d = fn(rnd, P, 1)
        L = d["L"]
        stem = d["q"] + " Which equation can you use to find <b>%s</b>?" % L
        e = (" ".join("Step %d: %s" % (i + 1, t) for i, t in enumerate(d["steps"])) +
             " Put the steps together: %s, so %s = %s." % (d["eq"], L, fmt(d["ans"], d["u"])))
        its.append(mcq(stem, d["eq"], d["eq_wrong"], e, rnd))
    its += rem_items(rnd, P)
    its += est_items(rnd, P)
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Multistep problems: equations, remainders and estimates", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>What does “times as many” mean?</h2>"
        "<p>A multiplication equation can <b>compare</b> two amounts. 35 = 5 × 7 means "
        "<b>35 is 5 times as many as 7</b>. It also means 35 is 7 times as many as 5.</p>" +
        ex("Example", "Ava has 7 shells. Leo has 5 times as many shells as Ava. How many shells does Leo have?",
           "Leo has 5 groups the size of Ava's 7 shells: 5 × 7 = 35.", "35 shells") +
        "<figure class='sn-fig'>" + bar_svg("Ava", "Leo", 5, "7", "7", "35", "comparison bar model: Leo has 5 times as many as Ava") +
        "<figcaption>A comparison bar model: Leo's bar is 5 parts, and each part is the same size as Ava's bar. 5 × 7 = 35.</figcaption></figure>"
        "<h2>Times as many or more than?</h2>"
        "<p>Read the words carefully. “Times as many” compares by multiplying. “More than” compares by adding.</p>" +
        table(["The story says", "Do this", "With 18 and 6"], [
            ["Leo has 3 times as many as Ava (6)", "multiply", "3 × 6 = 18"],
            ["Leo has 3 more than Ava (6)", "add", "6 + 3 = 9"],
            ["How many times as many? (18 and 6)", "divide", "18 ÷ 6 = 3"],
            ["How many more? (18 and 6)", "subtract", "18 − 6 = 12"],
        ]) +
        "<h2>Find the smaller amount</h2>"
        "<p>If you know the bigger amount, <b>divide</b> to find the smaller one.</p>" +
        "<figure class='sn-fig'>" + bar_svg("puppy", "mother", 6, "?", "", "48", "comparison bar model: 48 is 6 times as much as the puppy") +
        "<figcaption>A mother dog weighs 48 pounds, 6 times as much as her puppy. 48 ÷ 6 = 8, so the puppy weighs 8 pounds.</figcaption></figure>"
        "<h2>Multistep problems: use a letter</h2>"
        "<p>Write one equation with a <b>letter</b> for the unknown. Then solve it one step at a time.</p>" +
        ex("Example", "Ben has 24 cards. Ava has 3 times as many cards. She gives away 15. How many cards does Ava have now?",
           "Equation: 3 × 24 − 15 = c. Step 1: 3 × 24 = 72. Step 2: 72 − 15 = 57. "
           "Check: 3 × 20 = 60, and 60 − 15 = 45. 57 is a little more, which makes sense because 24 is more than 20.", "57 cards") +
        "<p>If the last step is a division with a remainder, ask what the remainder means: "
        "<b>add 1</b> if everything needs a place (vans, boxes), <b>leave it out</b> for full groups, "
        "or <b>give the remainder</b> if the question asks how many are left over.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding for “times as many” (6 and 3 → 9)", "Times as many means multiply: 3 × 6 = 18"],
            ["Answering “how many more” with the bigger amount", "Find the bigger amount, then subtract the smaller one"],
            ["Multiplying when the bigger amount is given", "If you know the bigger amount, divide to find the smaller one"],
            ["Stopping after step 1", "Read the question again: what does it ask for?"],
            ["Ignoring the remainder", "Decide: add 1, leave it out, or give the remainder"],
        ])
    )


FAQ = [
    {"q": "What is multiplicative comparison in 4th grade math?",
     "a": "It means comparing two amounts by multiplying, such as “35 is 5 times as many as 7.” Students learn to write it as an equation, 35 = 5 × 7, and to solve word problems with it."},
    {"q": "What is the difference between “times as many” and “more than”?",
     "a": "“Times as many” means multiply: 3 times as many as 6 is 18. “More than” means add: 3 more than 6 is 9."},
    {"q": "How do you know whether to multiply or divide in a comparison problem?",
     "a": "Multiply when you know the smaller amount and want the bigger one. Divide when you know the bigger amount and want the smaller one, or when you want to know how many times as many."},
    {"q": "How do you draw a bar model for “times as many”?",
     "a": "Draw one bar for the smaller amount. Under it, draw a bar made of that many equal copies, such as 4 copies for “4 times as many.” Put a bracket under the long bar for the total."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen_comparison():
    rnd = random.Random(111)
    P = People(rnd)
    sets = [set_statements(rnd, P), set_bigger(rnd, P), set_smaller(rnd, P), set_more_or_times(rnd, P), set_multistep(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "multiplicative-comparison-word-problems", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplicative Comparison and Multistep Word Problems",
        "seo_title": "Grade 4 Multiplicative Comparison Word Problems Worksheets: Times as Many, Bar Models and Multistep Problems",
        "short_title": "Comparison word problems",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "4.OA.A.1–3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/OA/A/",
        "standard_text": "Interpret a multiplication equation as a comparison, e.g., interpret 35 = 5 × 7 as a statement that 35 is 5 times as many as 7 and 7 times as many as 5. Multiply or divide to solve word problems involving multiplicative comparison, distinguishing multiplicative comparison from additive comparison. Solve multistep word problems posed with whole numbers and having whole-number answers using the four operations, including problems in which remainders must be interpreted. Represent these problems using equations with a letter standing for the unknown quantity. Assess the reasonableness of answers using mental computation and estimation strategies including rounding.",
        "meta_desc": "Free Grade 4 multiplicative comparison worksheets: “times as many” equations and bar models, multiply or divide to compare, times as many vs. how many more, and multistep word problems with a letter, remainders and estimates. 100 practice questions with step-by-step answers.",
        "key_big": "“Times as many” means multiply. “More than” means add.",
        "key_sub": "18 is 3 times as many as 6 (3 × 6 = 18), but it is 12 more than 6 (6 + 12 = 18). To find the smaller amount or how many times as many, divide.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_comparison()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "comparison bar model")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
