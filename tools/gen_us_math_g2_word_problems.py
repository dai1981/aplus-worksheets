# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Word Problems within 100 (2.OA.A.1)
  python tools/gen_us_math_g2_word_problems.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
PINK = "#f6d5d1"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
BOX = "☐"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero, negative or over-100 numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].rstrip("¢")
        if c in seen or not c:
            continue
        if lead.lstrip("-").isdigit() and (int(lead) < 2 or int(lead) > 100):
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

    def one(self):
        n, he, his = self.next()
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his), him="her" if he == "she" else "him")

    def two(self):
        a = self.next()
        b = self.next()
        while b[0] == a[0]:
            b = self.next()
        return dict(A=a[0], B=b[0], HeA=cap(a[1]))


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width in px of bold Arial text."""
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def fmt(n, u):
    """u is '¢' or (one, many)."""
    if u == "¢":
        return "%d¢" % n
    return "%d %s" % (n, u[0] if n == 1 else u[1])


def carry(a, b):
    return a % 10 + b % 10 >= 10


def borrow(a, b):
    return a % 10 < b % 10


def add_wrong(a, b):
    """Typical mistakes for a + b."""
    s = a + b
    w = []
    if carry(a, b):
        w.append(s - 10)                    # forgot to regroup the ten
    w.append(abs(a - b))                    # subtracted instead
    w += [s + 10, s - 1, s + 1, s - 10, s + 2]   # off by ten / counting slip
    return w


def sub_err(a, b):
    """Subtracted the smaller ones digit from the bigger one (52 − 27 -> 35)."""
    return (a // 10 - b // 10) * 10 + abs(a % 10 - b % 10)


def sub_wrong(a, b):
    """Typical mistakes for a − b."""
    d = a - b
    w = []
    if borrow(a, b):
        w.append(sub_err(a, b))             # smaller digit from bigger digit
        w.append(d + 10)                    # regrouped but did not take 1 from the tens
    w.append(a + b)                         # added instead
    w += [d - 10, d + 1, d - 1, d + 2]
    return w


def pick_add(r, lo, hi, maxsum, regroup, used):
    while True:
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        if a + b <= maxsum and carry(a, b) == regroup and a % 10 and b % 10 and a != b and (a, b) not in used:
            used.add((a, b))
            return a, b


def pick_sub(r, alo, ahi, blo, bhi, regroup, used):
    while True:
        a, b = r.randint(alo, ahi), r.randint(blo, bhi)
        if a - b >= 6 and (a - b) % 10 and borrow(a, b) == regroup and b % 10 and a != 2 * b and (a, b) not in used:
            used.add((a, b))
            return a, b


# ------------------------------------------------------------ bar models
def tape_svg(whole, parts, vals, subs, wlab, label):
    """Part-whole bar: bracket on top with the whole, one bar split into two parts, short words under the parts."""
    fs, sfs = 16, 14
    x0 = 10
    total = float(sum(vals))
    ws = []
    for t, v, sname in zip(parts, vals, subs):
        mn = max(tw(t, fs), tw(sname, sfs)) + 14
        ws.append(max(mn, 240 * v / total))
    bw = sum(ws)
    top = "%s %s" % (whole, wlab) if wlab else whole
    W = max(x0 * 2 + bw, tw(top, fs) + 20)
    x0 = (W - bw) / 2
    s = []
    s.append(text(x0 + bw / 2, 18, top, col=RED if whole == "?" else INK))
    s.append("<path d='M%.1f 34 v-8 H%.1f v8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, x0 + bw, INK))
    x = x0
    for t, w, sname in zip(parts, ws, subs):
        unknown = t == "?"
        s.append("<rect x='%.1f' y='40' width='%.1f' height='34' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
                 % (x, w, PINK if unknown else FILL, RED if unknown else GREEN, " stroke-dasharray='5 3'" if unknown else ""))
        s.append(text(x + w / 2, 63, t, col=RED if unknown else INK))
        s.append(text(x + w / 2, 94, sname, fs=sfs, col=INK))
        x += w
    return svg_wrap(int(W + 0.99), 102, "".join(s), label)


def cmp_svg(nb, ns, vb, vs, tb, ts, td, label):
    """Comparison bars: the bigger amount on top; the smaller bar plus a dashed part (the difference) underneath."""
    fs = 16
    lw = max(tw(nb, fs), tw(ns, fs))
    x0 = 10 + lw + 8
    L = 220.0
    dmin = max(44, tw(td, fs) + 16)
    ls = max(tw(ts, fs) + 16, 44, L * vs / vb)
    ls = min(ls, L - dmin)
    s = []
    s.append(text(x0 - 8, 27, nb, anchor="end"))
    s.append(text(x0 - 8, 69, ns, anchor="end"))
    s.append("<rect x='%.1f' y='6' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, L, FILL, GREEN))
    s.append(text(x0 + L / 2, 28, tb, col=RED if tb == "?" else INK))
    s.append("<rect x='%.1f' y='48' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, ls, FILL, GREEN))
    s.append(text(x0 + ls / 2, 70, ts, col=RED if ts == "?" else INK))
    s.append("<rect x='%.1f' y='48' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5' stroke-dasharray='5 3'/>"
             % (x0 + ls, L - ls, PINK, RED))
    s.append(text(x0 + ls + (L - ls) / 2, 70, td, col=RED))
    return svg_wrap(int(x0 + L + 10.99), 86, "".join(s), label)


# ------------------------------------------------------------ contexts: add to / take from
# Keys: s (start), ss (some at start), ad (add), ads (add some), tk (take), tks (take some), now, qn (now?), qs (start?),
#       qa (how many added?), qt (how many taken?), u (unit), mx (largest sensible number)
JOIN = [
    dict(s="{N} had {a} stickers.", ss="{N} had some stickers.",
         ad="{He} got {b} more stickers from a friend.", ads="{He} got some more stickers from a friend.",
         tk="{He} gave {b} stickers to a friend.", tks="{He} gave some stickers to a friend.",
         now="Now {he} has {c} stickers.", qn="How many stickers does {N} have now?", qs="How many stickers did {N} have at first?",
         qa="How many stickers did {N} get?", qt="How many stickers did {N} give away?", u=("sticker", "stickers"), mx=99),
    dict(s="There were {a} birds in a tree.", ss="Some birds were in a tree.",
         ad="{b} more birds flew to the tree.", ads="Some more birds flew to the tree.",
         tk="{b} birds flew away.", tks="Some birds flew away.",
         now="Now there are {c} birds in the tree.", qn="How many birds are in the tree now?", qs="How many birds were in the tree at first?",
         qa="How many birds flew to the tree?", qt="How many birds flew away?", u=("bird", "birds"), mx=50),
    dict(s="There were {a} children on a bus.", ss="Some children were on a bus.",
         ad="At the next stop, {b} more children got on.", ads="At the next stop, some more children got on.",
         tk="At the next stop, {b} children got off.", tks="At the next stop, some children got off.",
         now="Now there are {c} children on the bus.", qn="How many children are on the bus now?", qs="How many children were on the bus at first?",
         qa="How many children got on?", qt="How many children got off?", u=("child", "children"), mx=55),
    dict(s="{N} had {a} apples in a basket.", ss="{N} had some apples in a basket.",
         ad="{He} picked {b} more apples.", ads="{He} picked some more apples.",
         tk="{He} used {b} apples to make pies.", tks="{He} used some apples to make pies.",
         now="Now {he} has {c} apples.", qn="How many apples does {N} have now?", qs="How many apples did {N} have at first?",
         qa="How many apples did {N} pick?", qt="How many apples did {N} use?", u=("apple", "apples"), mx=80),
    dict(s="{N} had {a} marbles.", ss="{N} had some marbles.",
         ad="{He} won {b} more marbles in a game.", ads="{He} won some more marbles in a game.",
         tk="{He} lost {b} marbles in a game.", tks="{He} lost some marbles in a game.",
         now="Now {he} has {c} marbles.", qn="How many marbles does {N} have now?", qs="How many marbles did {N} have at first?",
         qa="How many marbles did {N} win?", qt="How many marbles did {N} lose?", u=("marble", "marbles"), mx=99),
    dict(s="A library cart had {a} books.", ss="A library cart had some books.",
         ad="{N} put {b} more books on the cart.", ads="{N} put some more books on the cart.",
         tk="{N} took {b} books off the cart.", tks="{N} took some books off the cart.",
         now="Now the cart has {c} books.", qn="How many books are on the cart now?", qs="How many books were on the cart at first?",
         qa="How many books did {N} put on the cart?", qt="How many books did {N} take off the cart?", u=("book", "books"), mx=90),
    dict(s="{N} had {a} shells.", ss="{N} had some shells.",
         ad="At the beach, {he} found {b} more shells.", ads="At the beach, {he} found some more shells.",
         tk="{He} gave {b} shells to {his} brother.", tks="{He} gave some shells to {his} brother.",
         now="Now {he} has {c} shells.", qn="How many shells does {N} have now?", qs="How many shells did {N} have at first?",
         qa="How many shells did {N} find?", qt="How many shells did {N} give to {his} brother?", u=("shell", "shells"), mx=90),
    dict(s="There were {a} cars in a parking lot.", ss="There were some cars in a parking lot.",
         ad="Then {b} more cars came in.", ads="Then some more cars came in.",
         tk="Then {b} cars drove away.", tks="Then some cars drove away.",
         now="Now there are {c} cars in the lot.", qn="How many cars are in the lot now?", qs="How many cars were in the lot at first?",
         qa="How many cars came in?", qt="How many cars drove away?", u=("car", "cars"), mx=99),
    dict(s="{N} baked {a} cookies.", ss="{N} baked some cookies.",
         ad="Then {he} baked {b} more cookies.", ads="Then {he} baked some more cookies.",
         tk="{His} family ate {b} of the cookies.", tks="{His} family ate some of the cookies.",
         now="Now there are {c} cookies.", qn="How many cookies are there now?", qs="How many cookies did {N} bake at first?",
         qa="How many more cookies did {N} bake?", qt="How many cookies did the family eat?", u=("cookie", "cookies"), mx=60),
    dict(s="There were {a} balloons at a party.", ss="There were some balloons at a party.",
         ad="{N} blew up {b} more balloons.", ads="{N} blew up some more balloons.",
         tk="Then {b} balloons popped.", tks="Then some balloons popped.",
         now="Now there are {c} balloons.", qn="How many balloons are there now?", qs="How many balloons were there at first?",
         qa="How many balloons did {N} blow up?", qt="How many balloons popped?", u=("balloon", "balloons"), mx=60),
    dict(s="There were {a} ducks in a pond.", ss="There were some ducks in a pond.",
         ad="Then {b} more ducks swam over.", ads="Then some more ducks swam over.",
         tk="Then {b} ducks swam away.", tks="Then some ducks swam away.",
         now="Now there are {c} ducks in the pond.", qn="How many ducks are in the pond now?", qs="How many ducks were in the pond at first?",
         qa="How many ducks swam over?", qt="How many ducks swam away?", u=("duck", "ducks"), mx=50),
    dict(s="{N} had {a} pennies in a jar.", ss="{N} had some pennies in a jar.",
         ad="{He} put {b} more pennies in the jar.", ads="{He} put some more pennies in the jar.",
         tk="{He} took {b} pennies out to buy a pencil.", tks="{He} took some pennies out to buy a pencil.",
         now="Now there are {c} pennies in the jar.", qn="How many pennies are in the jar now?", qs="How many pennies were in the jar at first?",
         qa="How many pennies did {N} put in?", qt="How many pennies did {N} take out?", u=("penny", "pennies"), mx=99),
    dict(s="{N} had {a} toy cars.", ss="{N} had some toy cars.",
         ad="For {his} birthday, {he} got {b} more toy cars.", ads="For {his} birthday, {he} got some more toy cars.",
         tk="{He} gave {b} toy cars to {his} cousin.", tks="{He} gave some toy cars to {his} cousin.",
         now="Now {he} has {c} toy cars.", qn="How many toy cars does {N} have now?", qs="How many toy cars did {N} have at first?",
         qa="How many toy cars did {N} get for {his} birthday?", qt="How many toy cars did {N} give away?", u=("toy car", "toy cars"), mx=70),
    dict(s="A pet store had {a} fish in a tank.", ss="A pet store had some fish in a tank.",
         ad="The owner put in {b} more fish.", ads="The owner put in some more fish.",
         tk="The store sold {b} fish.", tks="The store sold some fish.",
         now="Now there are {c} fish in the tank.", qn="How many fish are in the tank now?", qs="How many fish were in the tank at first?",
         qa="How many fish did the owner put in?", qt="How many fish did the store sell?", u=("fish", "fish"), mx=80),
    dict(s="{N} put {a} beads on a string.", ss="{N} put some beads on a string.",
         ad="Then {he} added {b} more beads.", ads="Then {he} added some more beads.",
         tk="Then {he} took off {b} beads.", tks="Then {he} took off some beads.",
         now="Now there are {c} beads on the string.", qn="How many beads are on the string now?", qs="How many beads were on the string at first?",
         qa="How many beads did {N} add?", qt="How many beads did {N} take off?", u=("bead", "beads"), mx=99),
    dict(s="Ms. Lee had {a} pencils.", ss="Ms. Lee had some pencils.",
         ad="She bought {b} more pencils.", ads="She bought some more pencils.",
         tk="She gave {b} pencils to her students.", tks="She gave some pencils to her students.",
         now="Now she has {c} pencils.", qn="How many pencils does Ms. Lee have now?", qs="How many pencils did Ms. Lee have at first?",
         qa="How many pencils did Ms. Lee buy?", qt="How many pencils did Ms. Lee give away?", u=("pencil", "pencils"), mx=99),
    dict(s="There were {a} people at the pool.", ss="There were some people at the pool.",
         ad="Then {b} more people came.", ads="Then some more people came.",
         tk="Then {b} people went home.", tks="Then some people went home.",
         now="Now there are {c} people at the pool.", qn="How many people are at the pool now?", qs="How many people were at the pool at first?",
         qa="How many people came?", qt="How many people went home?", u=("person", "people"), mx=90),
    dict(s="A farm had {a} chickens.", ss="A farm had some chickens.",
         ad="The farmer bought {b} more chickens.", ads="The farmer bought some more chickens.",
         tk="The farmer sold {b} chickens.", tks="The farmer sold some chickens.",
         now="Now the farm has {c} chickens.", qn="How many chickens does the farm have now?", qs="How many chickens did the farm have at first?",
         qa="How many chickens did the farmer buy?", qt="How many chickens did the farmer sell?", u=("chicken", "chickens"), mx=90),
]


def say(t, p, **k):
    d = dict(p)
    d.update(k)
    return t.format(**d)


# ------------------------------------------------------------ set 1: add to / take from (result unknown)
def set_result(rnd, P):
    ctx = rnd.sample(JOIN, 18) + rnd.sample(JOIN, 2)
    ops = ["add", "take"] * 10
    rnd.shuffle(ops)
    for i in range(18, 20):                                   # a repeated context uses the other operation
        j = [k for k in range(18) if ctx[k] is ctx[i]][0]
        ops[i] = "take" if ops[j] == "add" else "add"
    used = set()
    its = []
    for i, (c, op) in enumerate(zip(ctx, ops)):
        p = P.one()
        regroup = i % 4 != 0
        mx = c["mx"]
        if op == "add":
            a, b = pick_add(rnd, 11, mx - 11, mx, regroup, used)
            ans = a + b
            q = say(c["s"] + " " + c["ad"] + " " + c["qn"], p, a=a, b=b)
            e = "%d more were added, so add: %d + %d = %s. %d + %d = %d." % (b, a, b, BOX, a, b, ans)
            if carry(a, b):
                e += " Regroup: %d + %d = %d ones. Trade 10 ones for 1 ten." % (a % 10, b % 10, a % 10 + b % 10)
            w = add_wrong(a, b)
        else:
            a, b = pick_sub(rnd, 30, mx, 8, mx - 15, regroup, used)
            ans = a - b
            q = say(c["s"] + " " + c["tk"] + " " + c["qn"], p, a=a, b=b)
            e = "%d were taken away, so subtract: %d − %d = %s. %d − %d = %d." % (b, a, b, BOX, a, b, ans)
            if borrow(a, b):
                e += " You cannot take %d from %d in the ones place, so trade 1 ten for 10 ones first." % (b % 10, a % 10)
            w = sub_wrong(a, b)
        e = say(e, p)
        its.append(mcq(q, fmt(ans, c["u"]), [fmt(v, c["u"]) for v in w], e + " Answer: %s." % fmt(ans, c["u"]), rnd))
    return {"title": "Add to and take from", "items": its}


# ------------------------------------------------------------ set 2: put together / take apart
# tot: total unknown, part: one part unknown; lab: short words for the bar model
PARTS = [
    dict(tot="{N} has {a} red marbles and {b} blue marbles. How many marbles does {he} have in all?",
         part="{N} has {c} marbles. {a} are red, and the rest are blue. How many blue marbles does {he} have?",
         u=("marble", "marbles"), lab=("red", "blue"), mx=99),
    dict(tot="There are {a} girls and {b} boys at a school picnic. How many children are at the picnic?",
         part="There are {c} children at a school picnic. {a} of them are girls. How many boys are at the picnic?",
         u=("child", "children"), pu=("boy", "boys"), lab=("girls", "boys"), mx=99),
    dict(tot="An animal shelter has {a} cats and {b} dogs. How many animals are at the shelter?",
         part="An animal shelter has {c} cats and dogs. {a} of them are cats. How many dogs are at the shelter?",
         u=("animal", "animals"), pu=("dog", "dogs"), lab=("cats", "dogs"), mx=80),
    dict(tot="A garden has {a} red tulips and {b} yellow tulips. How many tulips are in the garden?",
         part="A garden has {c} tulips. {a} are red, and the rest are yellow. How many yellow tulips are there?",
         u=("tulip", "tulips"), lab=("red", "yellow"), mx=99),
    dict(tot="A bakery made {a} chocolate cupcakes and {b} vanilla cupcakes. How many cupcakes did it make?",
         part="A bakery made {c} cupcakes. {a} were chocolate, and the rest were vanilla. How many vanilla cupcakes did it make?",
         u=("cupcake", "cupcakes"), lab=("chocolate", "vanilla"), mx=99),
    dict(tot="{N} has {a} storybooks and {b} comic books. How many books does {he} have in all?",
         part="{N} has {c} books. {a} are storybooks, and the rest are comic books. How many comic books does {he} have?",
         u=("book", "books"), pu=("comic book", "comic books"), lab=("story", "comic"), mx=90),
    dict(tot="A pond has {a} ducks and {b} geese. How many birds are on the pond?",
         part="A pond has {c} ducks and geese. {a} of them are ducks. How many geese are on the pond?",
         u=("bird", "birds"), pu=("goose", "geese"), lab=("ducks", "geese"), mx=70),
    dict(tot="A sticker sheet has {a} gold stars and {b} silver stars. How many stars are on the sheet?",
         part="A sticker sheet has {c} stars. {a} are gold, and the rest are silver. How many silver stars are there?",
         u=("star", "stars"), lab=("gold", "silver"), mx=99),
    dict(tot="{N} bought {a} green apples and {b} red apples. How many apples did {he} buy?",
         part="{N} bought {c} apples. {a} were green, and the rest were red. How many red apples did {he} buy?",
         u=("apple", "apples"), lab=("green", "red"), mx=60),
    dict(tot="A toy box has {a} toy cars and {b} toy trucks. How many toys are in the box?",
         part="A toy box has {c} toy cars and toy trucks. {a} are cars. How many trucks are in the box?",
         u=("toy", "toys"), pu=("truck", "trucks"), lab=("cars", "trucks"), mx=80),
    dict(tot="{N} scored {a} points in the first game and {b} points in the second game. How many points did {he} score in all?",
         part="{N} scored {c} points in two games. {He} scored {a} points in the first game. How many points did {he} score in the second game?",
         u=("point", "points"), lab=("game 1", "game 2"), mx=99),
    dict(tot="{N} read {a} pages on Monday and {b} pages on Tuesday. How many pages did {he} read in all?",
         part="{N} read {c} pages on Monday and Tuesday. {He} read {a} pages on Monday. How many pages did {he} read on Tuesday?",
         u=("page", "pages"), lab=("Mon.", "Tue."), mx=99),
    dict(tot="A farmer has {a} brown eggs and {b} white eggs. How many eggs does the farmer have?",
         part="A farmer has {c} eggs. {a} are brown, and the rest are white. How many white eggs are there?",
         u=("egg", "eggs"), lab=("brown", "white"), mx=99),
    dict(tot="A tree has {a} green leaves and {b} yellow leaves. How many leaves are on the tree?",
         part="A small tree has {c} leaves. {a} are green, and the rest are yellow. How many yellow leaves are there?",
         u=("leaf", "leaves"), lab=("green", "yellow"), mx=99),
    dict(tot="A class planted {a} bean seeds and {b} corn seeds. How many seeds did the class plant?",
         part="A class planted {c} seeds. {a} were bean seeds, and the rest were corn seeds. How many corn seeds did the class plant?",
         u=("seed", "seeds"), lab=("bean", "corn"), mx=99),
    dict(tot="{N} has {a} baseball cards and {b} football cards. How many cards does {he} have?",
         part="{N} has {c} cards. {a} are baseball cards, and the rest are football cards. How many football cards does {he} have?",
         u=("card", "cards"), pu=("football card", "football cards"), lab=("baseball", "football"), mx=99),
]


def set_parts(rnd, P):
    order = rnd.sample(PARTS, 16) + rnd.sample(PARTS, 4)
    kinds = ["tot"] * 10 + ["part"] * 10
    rnd.shuffle(kinds)
    for i in range(16, 20):                                   # a repeated context gets the other kind
        j = [k for k in range(16) if order[k] is order[i]][0]
        kinds[i] = "part" if kinds[j] == "tot" else "tot"
    used = set()
    its = []
    nfig = 0
    for i, (c, kind) in enumerate(zip(order, kinds)):
        p = P.one()
        regroup = i % 5 != 0
        if kind == "tot":
            a, b = pick_add(rnd, 12, c["mx"] - 12, c["mx"], regroup, used)
            ans = a + b
            q = say(c["tot"], p, a=a, b=b)
            e = "You know both parts. Put them together: %d + %d = %s. %d + %d = %d. Answer: %s." % (a, b, BOX, a, b, ans, fmt(ans, c["u"]))
            w = add_wrong(a, b)
        else:
            tot, a = pick_sub(rnd, 35, c["mx"], 12, c["mx"] - 12, regroup, used)
            ans = tot - a
            q = say(c["part"], p, c=tot, a=a)
            pu = c.get("pu", c["u"])
            e = ("You know the whole (%d) and one part (%d). Find the other part: %d + %s = %d, or %d − %d = %s. "
                 "%d − %d = %d. Answer: %s." % (tot, a, a, BOX, tot, tot, a, BOX, tot, a, ans, fmt(ans, pu)))
            w = [tot + a] + sub_wrong(tot, a)                  # adding both numbers is the big trap here
            if nfig < 4 and i >= 6:
                nfig += 1
                q = fig(tape_svg(str(tot), [str(a), "?"], [a, ans], list(c["lab"]), "in all",
                                 "part-whole bar model: %d in all, %d %s" % (tot, a, c["lab"][0]))) + q
        uu = c["u"] if kind == "tot" else c.get("pu", c["u"])
        its.append(mcq(q, fmt(ans, uu), [fmt(v, uu) for v in w], e, rnd))
    assert nfig == 4, nfig
    return {"title": "Put together and take apart", "items": its}


# ------------------------------------------------------------ set 3: compare
# has: X has n; more: X has d more than Y; fewer: X has d fewer than Y; qm/qf: how many more/fewer; qh: how many does X have
def has_ctx(T):
    return dict(has="{X} has {n} %s." % T, more="{X} has {d} more %s than {Y}." % T, fewer="{X} has {d} fewer %s than {Y}." % T,
                qm="How many more %s does {X} have than {Y}?" % T, qf="How many fewer %s does {X} have than {Y}?" % T,
                qh="How many %s does {X} have?" % T, u=(T[:-1], T), v="has")


CMP = [has_ctx(T) for T in ["shells", "stickers", "marbles", "baseball cards", "beads", "toy cars", "crayons", "stamps", "rocks", "books"]] + [
    dict(has="{X} read {n} pages.", more="{X} read {d} more pages than {Y}.", fewer="{X} read {d} fewer pages than {Y}.",
         qm="How many more pages did {X} read than {Y}?", qf="How many fewer pages did {X} read than {Y}?",
         qh="How many pages did {X} read?", u=("page", "pages"), v="read"),
    dict(has="{X} scored {n} points.", more="{X} scored {d} more points than {Y}.", fewer="{X} scored {d} fewer points than {Y}.",
         qm="How many more points did {X} score than {Y}?", qf="How many fewer points did {X} score than {Y}?",
         qh="How many points did {X} score?", u=("point", "points"), v="scored"),
    dict(has="{X} picked {n} strawberries.", more="{X} picked {d} more strawberries than {Y}.", fewer="{X} picked {d} fewer strawberries than {Y}.",
         qm="How many more strawberries did {X} pick than {Y}?", qf="How many fewer strawberries did {X} pick than {Y}?",
         qh="How many strawberries did {X} pick?", u=("strawberry", "strawberries"), v="picked"),
    dict(has="{X} jumped rope {n} times.", more="{X} jumped rope {d} more times than {Y}.", fewer="{X} jumped rope {d} fewer times than {Y}.",
         qm="How many more times did {X} jump than {Y}?", qf="How many fewer times did {X} jump than {Y}?",
         qh="How many times did {X} jump rope?", u=("time", "times"), v="jumped"),
]


def cmp_items(rnd, P):
    # kind, count: D = how many more, F = how many fewer, B = bigger unknown (more), S = smaller unknown (more),
    #              BF = bigger unknown (fewer), SF = smaller unknown (fewer)
    kinds = ["D"] * 3 + ["F"] * 3 + ["B"] * 3 + ["S"] * 4 + ["BF"] * 4 + ["SF"] * 3
    ctx = rnd.sample(CMP, 14) + rnd.sample(CMP, 6)
    rnd.shuffle(kinds)
    used = set()
    its = []
    figs = {"S": 0, "BF": 0}
    for i, (kind, c) in enumerate(zip(kinds, ctx)):
        p = P.two()
        A, B, HeA, v = p["A"], p["B"], p["HeA"], c["v"]
        U = lambda v: fmt(v, c["u"])
        regroup = i % 4 != 0
        big, d = pick_sub(rnd, 30, 95, 6, 40, regroup, used)
        small = big - d
        if kind in ("D", "F"):
            # big - small = d ; numbers in the story are big and small
            if kind == "D":
                q = say(c["has"], {}, X=A, n=big) + " " + say(c["has"], {}, X=B, n=small) + " " + say(c["qm"], {}, X=A, Y=B)
            else:
                q = say(c["has"], {}, X=A, n=big) + " " + say(c["has"], {}, X=B, n=small) + " " + say(c["qf"], {}, X=B, Y=A)
            e = ("To compare, find the difference. Subtract the smaller number from the bigger one: %d − %d = %s. "
                 "%d − %d = %d. Check: %d + %d = %d. Answer: %s."
                 % (big, small, BOX, big, small, d, small, d, big, U(d)))
            w = [big + small] + sub_wrong(big, small)[:-3] + [d + 10, big, d - 1, d + 1]
            if kind == "D":
                e += " The word “more” does not mean add here."
            ans = d
        elif kind == "B":         # A has n; B has d more than A -> B = n + d
            n = small
            q = say(c["has"], {}, X=A, n=n) + " " + say(c["more"], {}, X=B, d=d, Y=A) + " " + say(c["qh"], {}, X=B)
            ans = n + d
            e = "%s %s %d more than %s, so add: %d + %d = %d. Answer: %s." % (B, v, d, A, n, d, ans, U(ans))
            w = [abs(n - d)] + add_wrong(n, d)[:-3] + [d, ans + 10, ans - 1]
        elif kind == "S":         # A has big; A has d more than B -> B = big - d
            q = say(c["has"], {}, X=A, n=big) + " " + say(c["more"], {}, X=HeA, d=d, Y=B) + " " + say(c["qh"], {}, X=B)
            ans = small
            e = ("%s %s %d more than %s, so %s %s %d fewer. Subtract: %d − %d = %d. "
                 "The word “more” is in the story, but you subtract. Answer: %s." % (A, v, d, B, B, v, d, big, d, small, U(ans)))
            w = [big + d] + sub_wrong(big, d)[:-3] + [ans + 10, ans - 1, ans + 1]
            if figs["S"] < 2:
                figs["S"] += 1
                q = fig(cmp_svg(A, B, big, small, str(big), "?", str(d), "comparison bar model: %s has %d more than %s" % (A, d, B))) + q
        elif kind == "BF":        # A has small; A has d fewer than B -> B = small + d
            q = say(c["has"], {}, X=A, n=small) + " " + say(c["fewer"], {}, X=HeA, d=d, Y=B) + " " + say(c["qh"], {}, X=B)
            ans = big
            e = ("%s %s %d fewer than %s, so %s %s %d more. Add: %d + %d = %d. "
                 "The word “fewer” is in the story, but you add. Answer: %s." % (A, v, d, B, B, v, d, small, d, big, U(ans)))
            w = [abs(small - d)] + add_wrong(small, d)[:-3] + [ans + 10, ans - 1, ans + 1]
            if figs["BF"] < 3:
                figs["BF"] += 1
                q = fig(cmp_svg(B, A, big, small, "?", str(small), str(d), "comparison bar model: %s has %d fewer than %s" % (A, d, B))) + q
        else:                     # SF: A has big; B has d fewer than A -> B = big - d
            q = say(c["has"], {}, X=A, n=big) + " " + say(c["fewer"], {}, X=B, d=d, Y=A) + " " + say(c["qh"], {}, X=B)
            ans = small
            e = "%s %s %d fewer than %s, so subtract: %d − %d = %d. Answer: %s." % (B, v, d, A, big, d, small, U(ans))
            w = [big + d] + sub_wrong(big, d)[:-3] + [ans + 10, ans - 1, ans + 1]
        its.append(mcq(q, U(ans), [U(v) for v in w], e, rnd))
    assert figs == {"S": 2, "BF": 3}, figs
    return {"title": "Compare: how many more or fewer?", "items": its}


# ------------------------------------------------------------ set 4: unknown start or change
def solve_box(eq, v):
    """Check an equation with a box: return True if v makes it true."""
    l, r = eq.replace("−", "-").replace(BOX, str(v)).split(" = ")
    return eval(l) == eval(r)


def unk_items(rnd, P):
    # SA: start unknown, add to; ST: start unknown, take from; CA: change unknown, add to; CT: change unknown, take from
    kinds = ["SA", "ST", "CA", "CT"] * 5
    rnd.shuffle(kinds)
    # 3 solve + 2 equation of each kind
    per = {k: ["solve"] * 3 + ["eq"] * 2 for k in ("SA", "ST", "CA", "CT")}
    for k in per:
        rnd.shuffle(per[k])
    ctx = rnd.sample(JOIN, 18) + rnd.sample(JOIN, 2)
    used = set()
    its = []
    nfig = 0
    for i, (kind, c) in enumerate(zip(kinds, ctx)):
        mode = per[kind].pop()
        p = P.one()
        U = lambda v: fmt(v, c["u"])
        mx = c["mx"]
        regroup = i % 3 != 0
        if kind in ("SA", "CA"):
            a, b = pick_add(rnd, 11, mx - 11, mx, regroup, used)       # a = start, b = change, t = a + b
            t = a + b
        else:
            a, b = pick_sub(rnd, 30, mx, 8, mx - 15, regroup, used)    # a = start, b = change, t = a - b
            t = a - b
        if kind == "SA":
            story = say(c["ss"] + " " + c["ad"] + " " + c["now"], p, b=b, c=t)
            qq = say(c["qs"], p)
            eq, ans = "%s + %d = %d" % (BOX, b, t), a
            bad = ["%d + %d = %s" % (b, t, BOX), "%s − %d = %d" % (BOX, b, t), "%s − %d = %d" % (BOX, t, b)]
            why = ("The start is unknown, so it is the %s. %d more were added, so %s. To solve it, take the %d away: "
                   "%d − %d = %d." % (BOX, b, eq, b, t, b, a))
            wrong = [t + b] + sub_wrong(t, b)[:3] + [a + 10, a - 1]
            tape = (str(t), [("?", a), (str(b), b)], ("at first", "more"), "now")
        elif kind == "ST":
            story = say(c["ss"] + " " + c["tk"] + " " + c["now"], p, b=b, c=t)
            qq = say(c["qs"], p)
            eq, ans = "%s − %d = %d" % (BOX, b, t), a
            bad = ["%d − %d = %s" % (t, b, BOX), "%s + %d = %d" % (BOX, b, t), "%d − %s = %d" % (t, BOX, b)]
            why = ("The start is unknown, so it is the %s. %d were taken away, so %s. To solve it, put the %d back: "
                   "%d + %d = %d." % (BOX, b, eq, b, t, b, a))
            wrong = [abs(t - b)] + add_wrong(t, b)[:-3] + [a + 10, a - 1, a + 1]
            tape = ("?", [(str(t), t), (str(b), b)], ("left", "gone"), "at first")
        elif kind == "CA":
            story = say(c["s"] + " " + c["ads"] + " " + c["now"], p, a=a, c=t)
            qq = say(c["qa"], p)
            eq, ans = "%d + %s = %d" % (a, BOX, t), b
            bad = ["%d + %d = %s" % (a, t, BOX), "%d − %s = %d" % (a, BOX, t), "%s − %d = %d" % (BOX, a, t)]
            why = ("The change is unknown, so it is the %s: %s. Count up from %d to %d, or subtract: "
                   "%d − %d = %d." % (BOX, eq, a, t, t, a, b))
            wrong = [t + a] + sub_wrong(t, a)[:3] + [b + 10, b - 1]
            tape = (str(t), [(str(a), a), ("?", b)], ("at first", "more"), "now")
        else:
            story = say(c["s"] + " " + c["tks"] + " " + c["now"], p, a=a, c=t)
            qq = say(c["qt"], p)
            eq, ans = "%d − %s = %d" % (a, BOX, t), b
            bad = ["%d + %d = %s" % (a, t, BOX), "%d + %s = %d" % (a, BOX, t), "%s − %d = %d" % (BOX, a, t)]
            why = ("The change is unknown, so it is the %s: %s. Think: what number takes %d down to %d? "
                   "%d − %d = %d." % (BOX, eq, a, t, a, t, b))
            wrong = [a + t] + sub_wrong(a, t)[:3] + [b + 10, b - 1]
            tape = (str(a), [(str(t), t), ("?", b)], ("left", "gone"), "at first")
        assert solve_box(eq, ans), (eq, ans)
        for x in bad:                                          # no wrong equation may have the same answer
            if x.endswith(BOX):
                assert eval(x.split(" = ")[0].replace("−", "-")) != ans, x
            else:
                assert not solve_box(x, ans), (x, ans)
        if mode == "eq":
            q = story + " Which equation matches the story?"
            e = why + " Answer: %s." % U(ans)
            its.append(mcq(q, eq, bad, e, rnd))
        else:
            q = story + " " + qq
            e = why + " Answer: %s." % U(ans)
            if nfig < 8:
                nfig += 1
                top, parts, subs, wl = tape
                q = fig(tape_svg(top, [x[0] for x in parts], [x[1] for x in parts], list(subs), wl,
                                 "part-whole bar model for a story with an unknown")) + q
            its.append(mcq(q, U(ans), [U(v) for v in wrong], e, rnd))
    assert nfig == 8, nfig
    return {"title": "Find the missing start or change", "items": its}


# ------------------------------------------------------------ set 5: two-step problems
def two_step(rnd, P):
    T = []

    def add(f):
        T.append(f)
        return f

    @add
    def t1(r, p):
        while True:
            a, b, c = r.randint(25, 55), r.randint(12, 30), r.randint(9, 35)
            if a + b <= 99 and a + b - c >= 5 and carry(a, b):
                break
        return dict(q=say("{N} had {a} stickers. {He} got {b} more. Then {he} gave {c} stickers to {his} sister. How many stickers does {N} have now?", p, a=a, b=b, c=c),
                    s1="Got more: %d + %d = %d." % (a, b, a + b), s2="Gave away: %d − %d = %d." % (a + b, c, a + b - c),
                    eq="%d + %d − %d = %s" % (a, b, c, BOX), ans=a + b - c, u=("sticker", "stickers"), wrong=[a + b, a + b + c, a - b + c, a + b - c + 10])

    @add
    def t2(r, p):
        while True:
            a, b, c = r.randint(30, 50), r.randint(8, 19), r.randint(6, 18)
            if a - b + c <= 60 and borrow(a, b) and c != b:
                break
        return dict(q="A bus had %d people on it. At the first stop, %d people got off and %d people got on. How many people are on the bus now?" % (a, b, c),
                    s1="Got off: %d − %d = %d." % (a, b, a - b), s2="Got on: %d + %d = %d." % (a - b, c, a - b + c),
                    eq="%d − %d + %d = %s" % (a, b, c, BOX), ans=a - b + c, u=("person", "people"), wrong=[a - b, a - b - c, a + b + c, a - b + c + 10])

    @add
    def t3(r, p):
        while True:
            a, b, c = r.randint(30, 48), r.randint(6, 15), r.randint(5, 14)
            if a - b - c >= 6 and b != c:
                break
        return dict(q="There were %d birds in a tree. %d birds flew away. Then %d more birds flew away. How many birds are in the tree now?" % (a, b, c),
                    s1="First group: %d − %d = %d." % (a, b, a - b), s2="Second group: %d − %d = %d." % (a - b, c, a - b - c),
                    eq="%d − %d − %d = %s" % (a, b, c, BOX), ans=a - b - c, u=("bird", "birds"), wrong=[a - b, a - b + c, b + c, a - b - c + 10])

    @add
    def t4(r, p):
        q = P.two()
        while True:
            a, d = r.randint(18, 40), r.randint(5, 15)
            if 2 * a + d <= 99:
                break
        return dict(q="%s has %d shells. %s has %d more shells than %s. How many shells do they have in all?" % (q["A"], a, q["B"], d, q["A"]),
                    s1="%s's shells: %d + %d = %d." % (q["B"], a, d, a + d), s2="In all: %d + %d = %d." % (a, a + d, 2 * a + d),
                    eq="%d + %d + %d = %s" % (a, a, d, BOX), ans=2 * a + d, u=("shell", "shells"), wrong=[a + d, 2 * a - d, 2 * a, 2 * a + d + 10])

    @add
    def t5(r, p):
        while True:
            a, d = r.randint(28, 48), r.randint(7, 16)
            if 2 * a - d <= 99 and borrow(a, d):
                break
        return dict(q="A red box has %d beads. A blue box has %d fewer beads than the red box. How many beads are in both boxes?" % (a, d),
                    s1="Blue box: %d − %d = %d." % (a, d, a - d), s2="Both boxes: %d + %d = %d." % (a, a - d, 2 * a - d),
                    eq="%d + %d − %d = %s" % (a, a, d, BOX), ans=2 * a - d, u=("bead", "beads"), wrong=[a - d, a + d, 2 * a + d, 2 * a - d - 10])

    @add
    def t6(r, p):
        while True:
            g = r.choice([80, 90, 100])
            a, b = r.randint(21, 38), r.randint(15, 33)
            if g - a - b >= 8 and carry(a, b):
                break
        return dict(q="A class wants to read %d books. The children read %d books in May and %d books in June. How many more books do they need to read?" % (g, a, b),
                    s1="Books read: %d + %d = %d." % (a, b, a + b), s2="Still to read: %d − %d = %d." % (g, a + b, g - a - b),
                    eq="%d − %d − %d = %s" % (g, a, b, BOX), ans=g - a - b, u=("book", "books"), wrong=[a + b, g - a, g - a + b, g - a - b + 10])

    @add
    def t7(r, p):
        while True:
            a, b, c = r.randint(18, 40), r.randint(15, 40), r.randint(12, 30)
            if a + b <= 80 and a + b - c >= 10 and a != b:
                break
        return dict(q="Ms. Diaz has %d red pencils and %d blue pencils. She gives %d pencils to her students. How many pencils does she have left?" % (a, b, c),
                    s1="Pencils in all: %d + %d = %d." % (a, b, a + b), s2="Left: %d − %d = %d." % (a + b, c, a + b - c),
                    eq="%d + %d − %d = %s" % (a, b, c, BOX), ans=a + b - c, u=("pencil", "pencils"), wrong=[a + b, a + b + c, a + c - b if a + c > b else a + b - c - 10, a + b - c + 10])

    @add
    def t8(r, p):
        while True:
            a, b, c = r.randint(18, 30), r.randint(18, 30), r.randint(11, 25)
            if a != b and a + b - c >= 10:
                break
        return dict(q="Grandma baked %d cookies on Saturday and %d cookies on Sunday. The family ate %d cookies. How many cookies are left?" % (a, b, c),
                    s1="Cookies baked: %d + %d = %d." % (a, b, a + b), s2="Left: %d − %d = %d." % (a + b, c, a + b - c),
                    eq="%d + %d − %d = %s" % (a, b, c, BOX), ans=a + b - c, u=("cookie", "cookies"), wrong=[a + b, a + b + c, b - c + a + 10, a - c if a > c + 1 else a + b - c - 10])

    @add
    def t9(r, p):
        q = P.two()
        while True:
            a, d, e = r.randint(15, 35), r.randint(6, 15), r.randint(3, 9)
            if d != e:
                break
        n = P.next()
        return dict(q="%s read %d pages. %s read %d more pages than %s. %s read %d fewer pages than %s. How many pages did %s read?"
                      % (q["A"], a, q["B"], d, q["A"], n[0], e, q["B"], n[0]),
                    s1="%s: %d + %d = %d pages." % (q["B"], a, d, a + d), s2="%s: %d − %d = %d pages." % (n[0], a + d, e, a + d - e),
                    eq="%d + %d − %d = %s" % (a, d, e, BOX), ans=a + d - e, u=("page", "pages"), wrong=[a + d, a + d + e, a - d + e, a - e])

    @add
    def t10(r, p):
        while True:
            a, b, c = r.randint(40, 70), r.randint(9, 25), r.randint(12, 30)
            if a + b <= 95 and a + b - c >= 10 and b != c:
                break
        return dict(q="There were %d cars in a parking lot. %d more cars came in. Then %d cars drove away. How many cars are in the lot now?" % (a, b, c),
                    s1="Came in: %d + %d = %d." % (a, b, a + b), s2="Drove away: %d − %d = %d." % (a + b, c, a + b - c),
                    eq="%d + %d − %d = %s" % (a, b, c, BOX), ans=a + b - c, u=("car", "cars"), wrong=[a + b, a + b + c, a - b + c, a + b - c - 10])

    @add
    def t11(r, p):
        while True:
            a = r.choice([50, 60, 75, 80, 90])
            b, c = r.randint(12, 35), r.randint(10, 30)
            if a - b - c >= 5 and b != c and abs(a - b - c - (b + c)) > 2 and a - b != b + c:
                break
        return dict(q=say("{N} has {a}¢. {He} buys a pencil for {b}¢ and an eraser for {c}¢. How much money does {he} have left?", p, a=a, b=b, c=c),
                    s1="Spent: %d¢ + %d¢ = %d¢." % (b, c, b + c), s2="Left: %d¢ − %d¢ = %d¢." % (a, b + c, a - b - c),
                    eq="%d − %d − %d = %s" % (a, b, c, BOX), ans=a - b - c, u="¢", wrong=[a - b, b + c, a - b + c, a - c])

    @add
    def t12(r, p):
        while True:
            a = r.choice([70, 80, 90, 100])
            b, c = r.randint(15, 30), r.randint(12, 28)
            if a - b - c >= 10 and b != c:
                break
        return dict(q=say("A ribbon is {a} cm long. {N} cuts off {b} cm. Then {he} cuts off {c} cm more. How long is the ribbon now?", p, a=a, b=b, c=c),
                    s1="First cut: %d − %d = %d cm." % (a, b, a - b), s2="Second cut: %d − %d = %d cm." % (a - b, c, a - b - c),
                    eq="%d − %d − %d = %s" % (a, b, c, BOX), ans=a - b - c, u=("cm", "cm"), wrong=[a - b, b + c, a - b + c, a - b - c + 10])

    @add
    def t13(r, p):
        while True:
            a, b, c = r.randint(20, 35), r.randint(18, 34), r.randint(30, 50)
            if a + b - c >= 6 and a + b <= 70 and c > a and c > b and a != b:
                break
        return dict(q="The Tigers scored %d points in the first half and %d points in the second half. The Bears scored %d points in all. How many more points did the Tigers score than the Bears?" % (a, b, c),
                    s1="Tigers in all: %d + %d = %d." % (a, b, a + b), s2="How many more: %d − %d = %d." % (a + b, c, a + b - c),
                    eq="%d + %d − %d = %s" % (a, b, c, BOX), ans=a + b - c, u=("point", "points"), wrong=[a + b, a + b + c, c - a, c - b])

    @add
    def t14(r, p):
        while True:
            a, b, c = r.randint(24, 40), r.randint(9, 18), r.randint(10, 25)
            if a - b + c <= 60 and borrow(a, b) and b != c:
                break
        return dict(q="%d children were playing outside. %d children went inside. Then %d more children came out to play. How many children are outside now?" % (a, b, c),
                    s1="Went inside: %d − %d = %d." % (a, b, a - b), s2="Came out: %d + %d = %d." % (a - b, c, a - b + c),
                    eq="%d − %d + %d = %s" % (a, b, c, BOX), ans=a - b + c, u=("child", "children"), wrong=[a - b, a - b - c, a + b + c, a - b + c - 10])

    @add
    def t15(r, p):
        q = P.two()
        while True:
            a, b, c = r.randint(25, 40), r.randint(50, 70), r.randint(5, 12)
            if b - a - c >= 3 and b - a != c:
                break
        return dict(q="%s has %d stamps. %s has %d stamps. Then %s gets %d more stamps. How many more stamps does %s have than %s now?"
                      % (q["A"], a, q["B"], b, q["A"], c, q["B"], q["A"]),
                    s1="%s now: %d + %d = %d." % (q["A"], a, c, a + c), s2="How many more: %d − %d = %d." % (b, a + c, b - a - c),
                    eq="%d − %d − %d = %s" % (b, a, c, BOX), ans=b - a - c, u=("stamp", "stamps"), wrong=[b - a, a + c, b - a + c, b - a - c + 10])

    @add
    def t16(r, p):
        while True:
            a, b, c = r.randint(20, 35), r.randint(15, 30), r.randint(10, 25)
            if a + b <= 70 and a + b - c >= 8 and a != b:
                break
        return dict(q="A pet store had %d fish. The owner put in %d more fish. Then the store sold %d fish. How many fish are in the store now?" % (a, b, c),
                    s1="Put in: %d + %d = %d." % (a, b, a + b), s2="Sold: %d − %d = %d." % (a + b, c, a + b - c),
                    eq="%d + %d − %d = %s" % (a, b, c, BOX), ans=a + b - c, u=("fish", "fish"), wrong=[a + b, a + b + c, a - b + c if a + c > b else a + b - c + 10, a + b - c - 10])

    @add
    def t17(r, p):
        while True:
            a, b, c = r.randint(45, 70), r.randint(12, 22), r.randint(7, 15)
            if a - b - c >= 10 and b != c and borrow(a, b):
                break
        return dict(q=say("{N} had {a} toy cars. {He} gave {b} to {his} cousin and {c} to a friend. How many toy cars does {N} have left?", p, a=a, b=b, c=c),
                    s1="Gave to the cousin: %d − %d = %d." % (a, b, a - b), s2="Gave to a friend: %d − %d = %d." % (a - b, c, a - b - c),
                    eq="%d − %d − %d = %s" % (a, b, c, BOX), ans=a - b - c, u=("toy car", "toy cars"), wrong=[a - b, b + c, a - b + c, a - b - c + 10])

    @add
    def t18(r, p):
        while True:
            s, a, b = r.choice([40, 45, 50]), r.randint(15, 25), r.randint(6, 12)
            if s - a - b >= 4:
                break
        return dict(q="A school bus has %d seats. %d children sit down. Then %d more children get on and sit down. How many seats are empty now?" % (s, a, b),
                    s1="Children on the bus: %d + %d = %d." % (a, b, a + b), s2="Empty seats: %d − %d = %d." % (s, a + b, s - a - b),
                    eq="%d − %d − %d = %s" % (s, a, b, BOX), ans=s - a - b, u=("seat", "seats"), wrong=[s - a, a + b, s - a + b, s - b])

    @add
    def t19(r, p):
        while True:
            a, b, c = r.randint(21, 38), r.randint(25, 42), r.randint(30, 50)
            if a + b <= 80 and a + b - c >= 8 and carry(a, b) and a != b:
                break
        return dict(q=say("{N} has {a} red beads and {b} blue beads. {He} uses {c} beads to make a necklace. How many beads are left?", p, a=a, b=b, c=c),
                    s1="Beads in all: %d + %d = %d." % (a, b, a + b), s2="Left: %d − %d = %d." % (a + b, c, a + b - c),
                    eq="%d + %d − %d = %s" % (a, b, c, BOX), ans=a + b - c, u=("bead", "beads"), wrong=[a + b, a + b + c, a + b - c - 10, a + b - c + 10])

    @add
    def t20(r, p):
        while True:
            a, b, c = r.randint(25, 40), r.randint(6, 12), r.randint(10, 20)
            if a - b + c <= 60 and borrow(a, b) and b != c:
                break
        return dict(q=say("There were {a} balloons at a party. {b} balloons popped. Then {N} blew up {c} more. How many balloons are there now?", p, a=a, b=b, c=c),
                    s1="Popped: %d − %d = %d." % (a, b, a - b), s2="Blew up more: %d + %d = %d." % (a - b, c, a - b + c),
                    eq="%d − %d + %d = %s" % (a, b, c, BOX), ans=a - b + c, u=("balloon", "balloons"), wrong=[a - b, a - b - c, a + b + c, a - b + c + 10])

    its = []
    order = list(T)
    rnd.shuffle(order)
    for t in order:
        while True:                                          # the answer must not be a number from the story
            d = t(rnd, P.one())
            nums = [int(x) for x in re.findall(r"\d+", d["eq"])]
            if d["ans"] not in nums:
                break
        assert all(1 <= v <= 100 for v in nums + [d["ans"]]), d
        U = lambda v: fmt(v, d["u"])
        e = "Step 1: %s Step 2: %s Equation: %s. Answer: %s." % (d["s1"], d["s2"], d["eq"], U(d["ans"]))
        its.append(mcq(d["q"], U(d["ans"]), [U(v) for v in d["wrong"] + [d["ans"] + 10, d["ans"] - 1, d["ans"] + 1]], e, rnd))
    return {"title": "Two-step word problems", "items": its}


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
        "<h2>Picture the story first</h2>"
        "<p>Do not hunt for key words. Ask: <b>what is happening?</b> Is something added, taken away, put together or compared? "
        "Then find what you do not know. It can be the start, the change or the end.</p>"
        "<h2>Five kinds of stories</h2>" +
        table(["Kind", "Story", "Equation"], [
            ["Add to", "Mia had 24 stickers. She got 17 more. How many now?", "24 + 17 = ☐"],
            ["Take from", "32 birds were in a tree. 15 flew away. How many are left?", "32 − 15 = ☐"],
            ["Put together", "Leo has 26 red and 18 blue marbles. How many in all?", "26 + 18 = ☐"],
            ["Take apart", "52 marbles. 27 are red. The rest are blue. How many are blue?", "27 + ☐ = 52"],
            ["Compare", "Sam has 40 cards. Ava has 28. How many more does Sam have?", "28 + ☐ = 40"],
        ]) +
        "<h2>Draw a bar model</h2>"
        "<p>A bar model shows the <b>parts</b> and the <b>whole</b>. If you know the whole, subtract to find a part. "
        "If you know both parts, add.</p>"
        "<figure class='sn-fig'>" +
        tape_svg("?", ["15", "8"], [15, 8], ["left", "gone"], "at first", "part-whole bar model: 15 left and 8 gone") +
        "<figcaption>Some birds were in a tree. 8 flew away. 15 are left. The two parts make the whole: 15 + 8 = 23 birds at first.</figcaption></figure>"
        "<p>For a compare story, draw two bars. The extra part is the difference.</p>"
        "<figure class='sn-fig'>" +
        cmp_svg("Sam", "Ava", 40, 28, "40", "28", "?", "comparison bar model: Sam 40, Ava 28") +
        "<figcaption>Sam has 40 cards and Ava has 28. The dashed part shows how many more Sam has: 40 − 28 = 12.</figcaption></figure>"
        "<h2>Use a box for the unknown</h2>"
        "<p>Write an equation and put a <b>☐</b> where the unknown number goes. The box can be anywhere.</p>" +
        ex("Example", "Some birds were in a tree. 8 flew away. Now 15 are left. How many birds were there at first?",
           "We do not know the start: ☐ − 8 = 15. Put the 8 back: 15 + 8 = 23.", "23 birds") +
        ex("Example", "Sam has 12 more cards than Ava. Sam has 40 cards. How many cards does Ava have?",
           "Sam has more, so Ava has fewer: 40 − 12 = 28. The word “more” does not always mean add.", "28 cards") +
        "<h2>Two-step problems</h2>"
        "<p>Some stories need two steps. Find the first answer, then use it.</p>" +
        ex("Example", "Ava has 25 shells. Leo has 8 more shells than Ava. How many shells do they have in all?",
           "Step 1: Leo has 25 + 8 = 33 shells. Step 2: in all, 25 + 33 = 58. Equation: 25 + 25 + 8 = ☐.", "58 shells") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding because the story says “more”", "Ask who has more. If you know the bigger number, subtract."],
            ["Adding both numbers when the whole is given", "If you know the whole, subtract to find the part"],
            ["Forgetting to regroup (37 + 25 = 52)", "7 + 5 = 12 ones. That is 1 ten and 2 ones: 62"],
            ["Taking the small digit from the big one (52 − 27 = 35)", "Trade 1 ten for 10 ones: 12 − 7 = 5, 4 − 2 = 2. So 25."],
            ["Stopping after step 1", "Read the question again. What does it ask?"],
        ])
    )


FAQ = [
    {"q": "What kinds of word problems do 2nd graders solve?",
     "a": "They solve adding to, taking from, putting together, taking apart and compare problems with numbers up to 100. The unknown can be the start, the change or the result, and some problems take two steps."},
    {"q": "What is a bar model (tape diagram) in 2nd grade math?",
     "a": "It is a long box split into parts. It shows the parts and the whole, so children can see if they need to add or subtract."},
    {"q": "Why is “Sam has 12 more than Ava” so hard?",
     "a": "Children see “more” and add. But if the story gives Sam's number, Ava has 12 fewer, so you subtract. Drawing two bars helps."},
    {"q": "What does the box mean in an equation like ☐ − 8 = 15?",
     "a": "The box stands for the unknown number. Here it is the start, so the answer is 15 + 8 = 23."},
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


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='[^']*" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_word_problems():
    rnd = random.Random(203)
    P = People(rnd)
    sets = [set_result(rnd, P), set_parts(rnd, P), cmp_items(rnd, P), unk_items(rnd, P), two_step(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "word-problems-within-100", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction Word Problems within 100",
        "seo_title": "Grade 2 Word Problems within 100 Worksheets: Add To, Take From, Compare, Bar Models and Two-Step Problems",
        "short_title": "Word problems within 100",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "2.OA.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/OA/A/1/",
        "standard_text": "Use addition and subtraction within 100 to solve one- and two-step word problems involving situations of adding to, taking from, putting together, taking apart, and comparing, with unknowns in all positions, e.g., by using drawings and equations with a symbol for the unknown number to represent the problem.",
        "meta_desc": "Free Grade 2 word problem worksheets within 100: add to, take from, put together, take apart and compare stories, missing start or change with bar models and ☐ equations, and two-step problems. 100 practice questions with simple answers.",
        "key_big": "Picture the story. Then decide: add or subtract?",
        "key_sub": "Find what you do not know: the start, the change or the end. Draw a bar model and write an equation with a ☐. The word “more” does not always mean add.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "bar model")


if __name__ == "__main__":
    u = gen_word_problems()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
