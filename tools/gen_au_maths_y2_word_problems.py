# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Word problems and number sentences (Australian Curriculum v9.0, AC9M2N06)
  python3 tools/gen_au_maths_y2_word_problems.py
Choose the number sentence, join and take-away stories, compare (how many more), missing parts,
equal groups and two-step stories. Pictures: objects, bar models, equal groups and step diagrams.
Every answer and every wrong answer is checked in code. HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
PINK = "#f6d5d1"
INK = "#2b2b2b"
RED = "#c0392b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
Q = "<b>?</b>"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.lstrip("$").split(" ")[0].rstrip("c")
        if c in seen or not c:
            continue
        if lead.replace(".", "").isdigit() and (float(lead) < 1 or float(lead) > 999):
            continue
        if c.startswith("-") or c.startswith("0"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
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


def solve(sent):
    """Value of ? that makes the number sentence true (None if none)."""
    s = sent.replace("−", "-").replace(Q, "?")
    l, r = s.split(" = ")
    for v in range(-1000, 2001):
        if eval(l.replace("?", "(%d)" % v)) == eval(r.replace("?", "(%d)" % v)):
            return v
    return None


def check_sentences(right, wrong, ans):
    assert solve(right) == ans, (right, ans)
    for w in wrong:
        assert solve(w) != ans, (w, ans)


def carry(a, b):
    return a % 10 + b % 10 >= 10


def borrow(a, b):
    return a % 10 < b % 10


def sfl(a, b):
    """Smaller digit from bigger digit in each column: 52 − 27 → 35 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def add_wrong(a, b):
    s = a + b
    w = []
    if carry(a, b):
        w.append(s - 10)                    # forgot to regroup the ten
    w.append(abs(a - b))                    # subtracted instead
    w += [s + 10, s - 1, s + 1, s - 10]
    return w


def sub_wrong(a, b):
    d = a - b
    w = []
    if borrow(a, b):
        w.append(sfl(a, b))                 # smaller digit from bigger digit
        w.append(d + 10)                    # regrouped but did not take 1 from the tens
    w.append(a + b)                         # added instead
    w += [d - 10, d + 1, d - 1]
    return w


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def one(self):
        n, he, his = self.next()
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his))

    def two(self):
        a = self.next()
        b = self.next()
        return dict(A=a[0], B=b[0], HeA=cap(a[1]))


def cap(s):
    return s[0].upper() + s[1:]


def say(t, p, **k):
    d = dict(p)
    d.update(k)
    return t.format(**d)


def unit(n, u):
    """u is 'c' (cents) or (one, many)."""
    if u == "c":
        return "%dc" % n if n < 100 else "$%d.%02d" % divmod(n, 100)
    return "%d %s" % (n, u[0] if n == 1 else u[1])


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text."""
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


# ------------------------------------------------------------ pictures
def icon(kind, cx, cy, s, fill, stroke):
    """One small picture centred at (cx, cy); s is about the width."""
    h = s / 2.0
    sw = 1.8
    if kind == "apple":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                % (cx, cy + 1, h - 1, fill, stroke, sw, cx, cy - h + 2, cx + 2, cy - h - 3, INK))
    if kind == "ball":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.5'/>"
                % (cx, cy, h - 1, fill, stroke, sw, cx - h + 2, cy - 3, cx, cy + 4, cx + h - 2, cy - 3, stroke))
    if kind == "book":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
                % (cx - h + 3, cy - h, s - 6, s, fill, stroke, sw, cx - h + 7, cy - h, cx - h + 7, cy + h, stroke))
    if kind == "star":
        import math
        pts = []
        for k in range(10):
            r = (h - 0.5) if k % 2 == 0 else (h - 0.5) * 0.45
            a = math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + 1.5 - r * math.sin(a)))
        return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='%.1f' stroke-linejoin='round'/>" % (
            " ".join(pts), fill, stroke, sw)
    if kind == "kid":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                % (cx, cy - h + s * 0.22, s * 0.2, fill, stroke, sw,
                   cx - h + 2, cy + h, cx, cy - s * 0.15, cx + h - 2, cy + h, fill, stroke, sw))
    # counter
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, h - 1, fill, stroke, sw)


STYLE = {"a": (FILL, GREEN), "b": (PINK, RED), "w": ("#ffffff", GREY), "x": (FILL, GREEN)}


def objs_svg(kind, groups, label):
    """Rows of up to 10 pictures (a gap after 5). groups: list of (count, style); each group starts a new row.
    Style 'x' pictures are crossed out (taken away); they are the LAST pictures of the group before."""
    S, cell, gap, pad = 22, 26, 8, 6
    rows = []
    for n, st in groups:
        if st == "x":                         # cross out the last n pictures already drawn
            k = n
            for row in reversed(rows):
                for j in range(len(row) - 1, -1, -1):
                    if k and row[j] != "x":
                        row[j] = "x"
                        k -= 1
            assert k == 0
            continue
        left = n
        while left:
            m = min(10, left)
            rows.append([st] * m)
            left -= m
    W = pad * 2 + 10 * cell + gap
    H = pad * 2 + len(rows) * cell
    s = []
    for r, row in enumerate(rows):
        for j, st in enumerate(row):
            cx = pad + j * cell + cell / 2 + (gap if j >= 5 else 0)
            cy = pad + r * cell + cell / 2
            f, k = STYLE[st]
            s.append(icon(kind, cx, cy, S, f, k))
            if st == "x":
                d = S / 2 - 1
                s.append("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='2.5'/>"
                         % (cx - d, cy - d, cx + d, cy + d, cx - d, cy + d, cx + d, cy - d, RED))
    used = max(len(r) for r in rows)
    W = pad * 2 + used * cell + (gap if used > 5 else 0)
    return svg_wrap(W, H, "".join(s), "picture of objects: " + label)


def tape_svg(whole, parts, vals, subs, wlab, label):
    """Part-whole bar: the whole on top, one bar split into two parts, short words under the parts."""
    fs, sfs = 16, 14
    total = float(sum(vals))
    ws = []
    for t, v, sname in zip(parts, vals, subs):
        mn = max(tw(t, fs), tw(sname, sfs)) + 14
        ws.append(max(mn, 220 * v / total))
    bw = sum(ws)
    top = "%s %s" % (whole, wlab) if wlab else whole
    W = max(20 + bw, tw(top, fs) + 20)
    x0 = (W - bw) / 2
    s = [text(x0 + bw / 2, 18, top, col=RED if whole == "?" else INK),
         "<path d='M%.1f 34 v-8 H%.1f v8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, x0 + bw, INK)]
    x = x0
    for t, w, sname in zip(parts, ws, subs):
        unk = t == "?"
        s.append("<rect x='%.1f' y='40' width='%.1f' height='34' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
                 % (x, w, PINK if unk else FILL, RED if unk else GREEN, " stroke-dasharray='5 3'" if unk else ""))
        s.append(text(x + w / 2, 63, t, col=RED if unk else INK))
        s.append(text(x + w / 2, 94, sname, fs=sfs))
        x += w
    return svg_wrap(int(W + 0.99), 102, "".join(s), "bar model: " + label)


def cmp_svg(nb, ns, vb, vs, tb, ts, td, label):
    """Two bars: the bigger amount on top; the smaller bar plus a dashed part (the difference) underneath."""
    fs = 16
    lw = max(tw(nb, fs), tw(ns, fs))
    x0 = 10 + lw + 8
    L = 220.0
    dmin = max(44, tw(td, fs) + 16)
    ls = max(tw(ts, fs) + 16, 44, L * vs / vb)
    ls = min(ls, L - dmin)
    s = [text(x0 - 8, 27, nb, anchor="end"), text(x0 - 8, 69, ns, anchor="end"),
         "<rect x='%.1f' y='6' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, L, FILL, GREEN),
         text(x0 + L / 2, 28, tb, col=RED if tb == "?" else INK),
         "<rect x='%.1f' y='48' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, ls, FILL, GREEN),
         text(x0 + ls / 2, 70, ts, col=RED if ts == "?" else INK),
         "<rect x='%.1f' y='48' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5' stroke-dasharray='5 3'/>"
         % (x0 + ls, L - ls, PINK, RED),
         text(x0 + ls + (L - ls) / 2, 70, td, col=RED if td == "?" else INK)]
    return svg_wrap(int(x0 + L + 10.99), 86, "".join(s), "comparison bars: " + label)


def groups_svg(ng, per, kind, label, share_total=None):
    """ng bags in a row, each with `per` pictures (5 to a row). With share_total: a row of the things
    to share on top and empty bags with ? underneath."""
    S, cell = 18, 22
    cols = min(per, 5) if share_total is None else 2
    rows = (per + 4) // 5 if share_total is None else 1
    bw = max(cols * cell + 14, 56)
    bh = max(rows * cell + 14, 40)
    gap = 12
    top = 0
    s = []
    if share_total is not None:
        n = share_total
        rws = (n + 9) // 10
        for k in range(n):
            r, j = divmod(k, 10)
            s.append(icon(kind, 10 + j * 24 + 12 + (6 if j >= 5 else 0), 6 + r * 24 + 12, 20, FILL, GREEN))
        top = 12 + rws * 24
    W = max(ng * bw + (ng - 1) * gap + 12, 290 if share_total is not None else 0)
    x0 = (W - (ng * bw + (ng - 1) * gap)) / 2
    for g in range(ng):
        x = x0 + g * (bw + gap)
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='10' fill='#ffffff' stroke='%s' stroke-width='2.5'/>"
                 % (x, top + 4, bw, bh, INK))
        if share_total is None:
            gw = cols * cell
            for k in range(per):
                r, j = divmod(k, 5)
                s.append(icon(kind, x + (bw - gw) / 2 + j * cell + cell / 2, top + 4 + 7 + r * cell + cell / 2, S, FILL, GREEN))
        else:
            s.append(text(x + bw / 2, top + 4 + bh / 2 + 7, "?", 20, col=RED))
    H = top + 4 + bh + 6
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), "equal groups: " + label)


def steps_svg(start, j1, j2, label):
    """Two-step diagram: [start] —j1→ [ ] —j2→ [?]."""
    fs = 16
    bw = max(tw(start, fs) + 20, 56)
    aw = max(tw(j1, 15), tw(j2, 15)) + 30
    aw = max(aw, 70)
    y, bh = 30, 36
    W = 10 + 3 * bw + 2 * aw + 10
    s = []
    xs = [10, 10 + bw + aw, 10 + 2 * (bw + aw)]
    labels = [start, "", "?"]
    for x, t in zip(xs, labels):
        unk = t != start
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
                 % (x, y, bw, bh, PINK if t == "?" else (FILL if not unk else "#ffffff"),
                    RED if t == "?" else (GREEN if not unk else INK), " stroke-dasharray='5 3'" if unk else ""))
        if t:
            s.append(text(x + bw / 2, y + 24, t, fs, col=RED if t == "?" else INK))
    for k, j in enumerate([j1, j2]):
        x1 = xs[k] + bw + 6
        x2 = xs[k + 1] - 6
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x1, y + bh / 2, x2 - 2, y + bh / 2, GREEN))
        s.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                 % (x2 - 9, y + bh / 2 - 6, x2, y + bh / 2, x2 - 9, y + bh / 2 + 6, GREEN))
        s.append(text((x1 + x2) / 2, y - 8, j, 15, col=GREEN))
    return svg_wrap(int(W + 0.99), y + bh + 6, "".join(s), "two-step diagram: " + label)


# ============================================================ set 1: choose the number sentence
S1 = {
    "join": [
        ("apple", "There are {a} apples in a bowl. Mum puts in {b} more. How many apples are in the bowl now?"),
        ("ball", "There are {a} balls in the sports shed. The teacher brings {b} more. How many balls are there now?"),
        ("star", "{N} has {a} star stickers. {He} gets {b} more. How many stickers does {he} have now?"),
        ("kid", "{a} students are in the library. {b} more students come in. How many students are in the library now?"),
        ("book", "{N} has {a} books on a shelf. {He} puts {b} more on the shelf. How many books are on the shelf now?"),
        ("apple", "The canteen has {a} apples. The cook brings {b} more apples. How many apples are there now?"),
    ],
    "take": [
        ("apple", "There are {a} apples in a bowl. The class eats {b} at recess. How many apples are left?"),
        ("ball", "There are {a} balls in the sports shed. Students take {b} out to play. How many balls are left in the shed?"),
        ("star", "{N} has {a} star stickers. {He} gives {b} to a friend. How many stickers does {he} have left?"),
        ("kid", "{a} students are on the bus. {b} students get off. How many students are still on the bus?"),
        ("book", "There are {a} books on the library shelf. Students borrow {b} books. How many books are left on the shelf?"),
        ("kid", "{a} children are in the pool. {b} children get out. How many children are still in the pool?"),
    ],
    "together": [
        ("apple", "There are {a} apples in a bowl and {b} apples in a bag. How many apples are there in all?"),
        ("ball", "There are {a} footballs and {b} netballs in the shed. How many balls are there altogether?"),
        ("kid", "{a} girls and {b} boys are at the library. How many children are there altogether?"),
        ("star", "{N} got {a} stars on Monday and {b} stars on Tuesday. How many stars did {he} get in all?"),
    ],
    "apart": [
        ("apple", "There are {c} apples. {a} are in a bowl. The rest are in a bag. How many apples are in the bag?"),
        ("ball", "There are {c} balls in the shed. {a} are footballs. The rest are netballs. How many netballs are there?"),
        ("kid", "There are {c} students in the class. {a} are boys. The rest are girls. How many girls are there?"),
        ("book", "{N} has {c} books. {a} are about animals. The rest are about space. How many are about space?"),
    ],
}


def set_choose(rnd, P):
    its = []
    used = set()
    plan = []
    for kind in ("join", "take", "together", "apart"):
        for k, ctx in enumerate(S1[kind]):
            plan.append((kind, ctx))
    order = [plan[i] for i in [0, 6, 1, 7, 12, 2, 8, 13, 3, 9, 16, 4, 10, 14, 17, 5, 11, 15, 18, 19]]
    assert sorted(id(x) for x in order) == sorted(id(x) for x in plan)
    for i, (kind, (ic, t)) in enumerate(order):
        p = P.one()
        hard = i >= 10
        while True:
            if kind in ("join", "together"):
                a, b = rnd.randint(4, 12), rnd.randint(3, 9)
                ok = a != b and (11 <= a + b <= 20 if hard else a + b <= 10)
            elif kind == "take":
                a, b = rnd.randint(9, 20 if hard else 14), rnd.randint(3, 9)
                ok = a - b >= 3 and a != 2 * b
            else:
                a, b = rnd.randint(11, 20), rnd.randint(4, 12)       # a = whole, b = part
                ok = a - b >= 3 and a != 2 * b
            if ok and (kind, a, b) not in used and (a, b) not in {(x, y) for _, x, y in used}:
                used.add((kind, a, b))
                break
        if kind in ("join", "together"):
            q = say(t, p, a=a, b=b)
            ans = a + b
            right = "%d + %d = ?" % (a, b)
            big, sm = max(a, b), min(a, b)
            wrong = ["%d − %d = ?" % (big, sm), "%d − %d = ?" % (sm, big), "%d − ? = %d" % (big, sm)]
            pic = objs_svg(ic, [(a, "a"), (b, "b")], "%d and %d" % (a, b))
            e = ("%s, so add: <b>%d + %d = ?</b>. %d + %d = %d. "
                 % ("More are added" if kind == "join" else "Two groups are put together", a, b, a, b, ans))
            e += "Subtracting would make the number smaller, but there are more now." if kind == "join" else "“In all” and “altogether” mean add."
        elif kind == "take":
            q = say(t, p, a=a, b=b)
            ans = a - b
            right = "%d − %d = ?" % (a, b)
            wrong = ["%d + %d = ?" % (a, b), "%d − %d = ?" % (b, a), "? − %d = %d" % (b, a)]
            pic = objs_svg(ic, [(a, "a"), (b, "x")], "%d with %d crossed out" % (a, b))
            e = ("Some are taken away, so subtract. Start with the bigger number: <b>%d − %d = ?</b>. %d − %d = %d. "
                 "Adding would give more, but some have gone." % (a, b, a, b, ans))
        else:
            c, a2 = a, b
            q = say(t, p, a=a2, c=c)
            ans = c - a2
            right = "%d − %d = ?" % (c, a2)
            wrong = ["%d + %d = ?" % (c, a2), "%d − %d = ?" % (a2, c), "? − %d = %d" % (a2, c)]
            pic = objs_svg(ic, [(a2, "a"), (ans, "w")], "%d in all, %d coloured" % (c, a2))
            e = ("You know the whole (%d) and one part (%d). Take the part away: <b>%d − %d = ?</b>. %d − %d = %d. "
                 "Do not add the two numbers: %d is already the total." % (c, a2, c, a2, c, a2, ans, c))
        check_sentences(right, wrong, ans)
        its.append(mcq(fig(pic) + q + " Which number sentence matches?", right, wrong, e))
    return {"title": "Choose the number sentence", "items": its}


# ============================================================ stories for sets 2 and 4
# s: start, ss: some at start, ad/ads: add (some), tk/tks: take (some), now, qn: now?, qs: start?, qa: how many added?,
# qt: how many taken?, u: units, mx: largest sensible number, lab: words under the bar parts (added, taken)
JOIN = [
    dict(s="{N} had {a} stickers.", ss="{N} had some stickers.",
         ad="{He} got {b} more stickers.", ads="{He} got some more stickers.",
         tk="{He} gave {b} stickers to a friend.", tks="{He} gave some stickers to a friend.",
         now="Now {he} has {c} stickers.", qn="How many stickers does {N} have now?", qs="How many stickers did {N} have at first?",
         qa="How many stickers did {N} get?", qt="How many stickers did {N} give away?", u=("sticker", "stickers"), mx=99),
    dict(s="There were {a} students on the bus.", ss="Some students were on the bus.",
         ad="At the next stop, {b} more students got on.", ads="At the next stop, some more students got on.",
         tk="At the next stop, {b} students got off.", tks="At the next stop, some students got off.",
         now="Now there are {c} students on the bus.", qn="How many students are on the bus now?", qs="How many students were on the bus at first?",
         qa="How many students got on?", qt="How many students got off?", u=("student", "students"), mx=60),
    dict(s="There were {a} birds in a gum tree.", ss="Some birds were in a gum tree.",
         ad="{b} more birds flew in.", ads="Some more birds flew in.",
         tk="{b} birds flew away.", tks="Some birds flew away.",
         now="Now there are {c} birds in the tree.", qn="How many birds are in the tree now?", qs="How many birds were in the tree at first?",
         qa="How many birds flew in?", qt="How many birds flew away?", u=("bird", "birds"), mx=50),
    dict(s="The library trolley had {a} books.", ss="The library trolley had some books.",
         ad="{N} put {b} more books on it.", ads="{N} put some more books on it.",
         tk="{N} took {b} books off it.", tks="{N} took some books off it.",
         now="Now the trolley has {c} books.", qn="How many books are on the trolley now?", qs="How many books were on the trolley at first?",
         qa="How many books did {N} put on?", qt="How many books did {N} take off?", u=("book", "books"), mx=90),
    dict(s="{N} had {a} shells.", ss="{N} had some shells.",
         ad="At the beach, {he} found {b} more shells.", ads="At the beach, {he} found some more shells.",
         tk="{He} gave {b} shells to {his} brother.", tks="{He} gave some shells to {his} brother.",
         now="Now {he} has {c} shells.", qn="How many shells does {N} have now?", qs="How many shells did {N} have at first?",
         qa="How many shells did {N} find?", qt="How many shells did {N} give away?", u=("shell", "shells"), mx=90),
    dict(s="{N} had {a} footy cards.", ss="{N} had some footy cards.",
         ad="{He} got {b} more footy cards.", ads="{He} got some more footy cards.",
         tk="{He} gave {b} footy cards to {his} cousin.", tks="{He} gave some footy cards to {his} cousin.",
         now="Now {he} has {c} footy cards.", qn="How many footy cards does {N} have now?", qs="How many footy cards did {N} have at first?",
         qa="How many footy cards did {N} get?", qt="How many footy cards did {N} give away?", u=("footy card", "footy cards"), mx=99),
    dict(s="The canteen had {a} sausage rolls.", ss="The canteen had some sausage rolls.",
         ad="The cook made {b} more.", ads="The cook made some more.",
         tk="At recess, students bought {b} sausage rolls.", tks="At recess, students bought some sausage rolls.",
         now="Now there are {c} sausage rolls.", qn="How many sausage rolls are there now?", qs="How many sausage rolls were there at first?",
         qa="How many sausage rolls did the cook make?", qt="How many sausage rolls did students buy?", u=("sausage roll", "sausage rolls"), mx=90),
    dict(s="There were {a} children in the pool.", ss="Some children were in the pool.",
         ad="{b} more children jumped in.", ads="Some more children jumped in.",
         tk="{b} children got out.", tks="Some children got out.",
         now="Now there are {c} children in the pool.", qn="How many children are in the pool now?", qs="How many children were in the pool at first?",
         qa="How many children jumped in?", qt="How many children got out?", u=("child", "children"), mx=60),
    dict(s="A tub had {a} pencils.", ss="A tub had some pencils.",
         ad="The teacher put in {b} more pencils.", ads="The teacher put in some more pencils.",
         tk="Students took {b} pencils out.", tks="Students took some pencils out.",
         now="Now there are {c} pencils in the tub.", qn="How many pencils are in the tub now?", qs="How many pencils were in the tub at first?",
         qa="How many pencils did the teacher put in?", qt="How many pencils did students take out?", u=("pencil", "pencils"), mx=90),
    dict(s="{N} had {a} marbles.", ss="{N} had some marbles.",
         ad="{He} won {b} more marbles.", ads="{He} won some more marbles.",
         tk="{He} lost {b} marbles.", tks="{He} lost some marbles.",
         now="Now {he} has {c} marbles.", qn="How many marbles does {N} have now?", qs="How many marbles did {N} have at first?",
         qa="How many marbles did {N} win?", qt="How many marbles did {N} lose?", u=("marble", "marbles"), mx=99),
    dict(s="There were {a} ducks on the pond.", ss="Some ducks were on the pond.",
         ad="{b} more ducks swam over.", ads="Some more ducks swam over.",
         tk="{b} ducks swam away.", tks="Some ducks swam away.",
         now="Now there are {c} ducks on the pond.", qn="How many ducks are on the pond now?", qs="How many ducks were on the pond at first?",
         qa="How many ducks swam over?", qt="How many ducks swam away?", u=("duck", "ducks"), mx=50),
    dict(s="There were {a} chairs in the hall.", ss="There were some chairs in the hall.",
         ad="{N} carried in {b} more chairs.", ads="{N} carried in some more chairs.",
         tk="{N} took {b} chairs out.", tks="{N} took some chairs out.",
         now="Now there are {c} chairs in the hall.", qn="How many chairs are in the hall now?", qs="How many chairs were in the hall at first?",
         qa="How many chairs did {N} carry in?", qt="How many chairs did {N} take out?", u=("chair", "chairs"), mx=99),
    dict(s="{N} put {a} beads on a string.", ss="{N} put some beads on a string.",
         ad="Then {he} added {b} more beads.", ads="Then {he} added some more beads.",
         tk="Then {he} took off {b} beads.", tks="Then {he} took off some beads.",
         now="Now there are {c} beads on the string.", qn="How many beads are on the string now?", qs="How many beads were on the string at first?",
         qa="How many beads did {N} add?", qt="How many beads did {N} take off?", u=("bead", "beads"), mx=99),
    dict(s="The cake stall had {a} cupcakes.", ss="The cake stall had some cupcakes.",
         ad="{N}'s dad brought {b} more cupcakes.", ads="{N}'s dad brought some more cupcakes.",
         tk="People bought {b} cupcakes.", tks="People bought some cupcakes.",
         now="Now there are {c} cupcakes.", qn="How many cupcakes are there now?", qs="How many cupcakes were there at first?",
         qa="How many cupcakes did {N}'s dad bring?", qt="How many cupcakes did people buy?", u=("cupcake", "cupcakes"), mx=80),
    dict(s="There were {a} kangaroos in a paddock.", ss="Some kangaroos were in a paddock.",
         ad="{b} more kangaroos hopped in.", ads="Some more kangaroos hopped in.",
         tk="{b} kangaroos hopped away.", tks="Some kangaroos hopped away.",
         now="Now there are {c} kangaroos in the paddock.", qn="How many kangaroos are in the paddock now?", qs="How many kangaroos were in the paddock at first?",
         qa="How many kangaroos hopped in?", qt="How many kangaroos hopped away?", u=("kangaroo", "kangaroos"), mx=60),
    dict(s="There were {a} cars in the school car park.", ss="Some cars were in the school car park.",
         ad="Then {b} more cars came in.", ads="Then some more cars came in.",
         tk="Then {b} cars drove away.", tks="Then some cars drove away.",
         now="Now there are {c} cars in the car park.", qn="How many cars are in the car park now?", qs="How many cars were in the car park at first?",
         qa="How many cars came in?", qt="How many cars drove away?", u=("car", "cars"), mx=80),
]


def pick_add(r, lo, hi, mx, regroup, used):
    while True:
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        if a + b <= mx and carry(a, b) == regroup and a % 10 and b % 10 and a != b and (a, b) not in used:
            used.add((a, b))
            return a, b


def pick_sub(r, alo, ahi, blo, bhi, regroup, used):
    while True:
        a, b = r.randint(alo, ahi), r.randint(blo, bhi)
        if a - b >= 6 and (a - b) % 10 and borrow(a, b) == regroup and b % 10 and a != 2 * b and (a, b) not in used:
            used.add((a, b))
            return a, b


# ============================================================ set 2: join and take away
def set_join(rnd, P):
    ctx = rnd.sample(JOIN, 16) + rnd.sample(JOIN, 2)
    ops = ["add", "take"] * 9
    rnd.shuffle(ops)
    for i in range(16, 18):
        j = [k for k in range(16) if ctx[k] is ctx[i]][0]
        ops[i] = "take" if ops[j] == "add" else "add"
    regs = [False] * 6 + [True] * 12
    used = set()
    rows = []
    for c, op, rg in zip(ctx, ops, regs):
        p = P.one()
        mx = c["mx"]
        if op == "add":
            a, b = pick_add(rnd, 11, mx - 11, mx, rg, used)
            ans = a + b
            q = say(c["s"] + " " + c["ad"] + " " + c["qn"], p, a=a, b=b)
            e = "More came, so add: %d + %d = <b>%d</b>." % (a, b, ans)
            if carry(a, b):
                e += " %d + %d = %d ones. Trade 10 ones for 1 ten." % (a % 10, b % 10, a % 10 + b % 10)
            w = add_wrong(a, b)
            pic = tape_svg("?", [str(a), str(b)], [a, b], ["at first", "more"], "now", "%d and %d more" % (a, b))
        else:
            a, b = pick_sub(rnd, 30, mx, 8, mx - 15, rg, used)
            ans = a - b
            q = say(c["s"] + " " + c["tk"] + " " + c["qn"], p, a=a, b=b)
            e = "Some went away, so subtract: %d − %d = <b>%d</b>." % (a, b, ans)
            if borrow(a, b):
                e += " You cannot take %d from %d %s, so trade 1 ten for 10 ones first." % (b % 10, a % 10, "one" if a % 10 == 1 else "ones")
            w = sub_wrong(a, b)
            pic = tape_svg(str(a), ["?", str(b)], [ans, b], ["left", "gone"], "at first", "%d at first, %d gone" % (a, b))
        e = say(e, p) + " Answer: %s." % unit(ans, c["u"])
        rows.append((q, unit(ans, c["u"]), [unit(v, c["u"]) for v in w if v > 0], e, pic))
    # money (cents, multiples of 5)
    p = P.one()
    a, b = 45, 30
    rows.insert(4, (say("{N} has 45c. {He} finds 30c more. How much money does {he} have now?", p),
                    unit(a + b, "c"), [unit(15, "c"), unit(85, "c"), unit(70, "c")],
                    "{N} gets more money, so add: 45c + 30c = <b>75c</b>. 4 tens + 3 tens = 7 tens, and 5 more.".format(**p),
                    tape_svg("?", ["45c", "30c"], [45, 30], ["had", "found"], "now", "45c and 30c more")))
    assert a + b == 75 and a - b == 15
    p = P.one()
    a, b = 90, 35
    rows.insert(12, (say("{N} has 90c. {He} buys a pencil for 35c. How much money does {he} have left?", p),
                     unit(a - b, "c"), [unit(sfl(a, b), "c"), unit(a + b, "c"), unit(60, "c")],
                     "Spending money takes it away, so subtract: 90c − 35c. 90 − 30 = 60, then 60 − 5 = <b>55c</b>.",
                     tape_svg("90c", ["?", "35c"], [55, 35], ["left", "spent"], "at first", "90c at first, 35c spent")))
    assert a - b == 55 and sfl(a, b) == 65
    its = []
    for k, (q, right, wrong, e, pic) in enumerate(rows):
        if k % 4 != 3:                       # most questions have a bar model
            q = fig(pic) + q
        its.append(mcq(q, right, wrong, e))
    return {"title": "Join and take-away problems", "items": its}


# ============================================================ set 3: compare
def has_ctx(T, one):
    return dict(has="{X} has {n} %s." % T, more="{X} has {d} more %s than {Y}." % T, fewer="{X} has {d} fewer %s than {Y}." % T,
                qm="How many more %s does {X} have than {Y}?" % T, qf="How many fewer %s does {X} have than {Y}?" % T,
                qh="How many %s does {X} have?" % T, u=(one, T), v="has")


CMP = [has_ctx(T, o) for T, o in [("shells", "shell"), ("stickers", "sticker"), ("marbles", "marble"), ("footy cards", "footy card"),
                                  ("beads", "bead"), ("stamps", "stamp"), ("bottle tops", "bottle top")]] + [
    dict(has="{X} read {n} pages.", more="{X} read {d} more pages than {Y}.", fewer="{X} read {d} fewer pages than {Y}.",
         qm="How many more pages did {X} read than {Y}?", qf="How many fewer pages did {X} read than {Y}?",
         qh="How many pages did {X} read?", u=("page", "pages"), v="read"),
    dict(has="{X} scored {n} points.", more="{X} scored {d} more points than {Y}.", fewer="{X} scored {d} fewer points than {Y}.",
         qm="How many more points did {X} score than {Y}?", qf="How many fewer points did {X} score than {Y}?",
         qh="How many points did {X} score?", u=("point", "points"), v="scored"),
    dict(has="{X} skipped {n} times.", more="{X} skipped {d} more times than {Y}.", fewer="{X} skipped {d} fewer times than {Y}.",
         qm="How many more times did {X} skip than {Y}?", qf="How many fewer times did {X} skip than {Y}?",
         qh="How many times did {X} skip?", u=("time", "times"), v="skipped"),
    dict(has="{X} picked up {n} pieces of rubbish.", more="{X} picked up {d} more pieces of rubbish than {Y}.",
         fewer="{X} picked up {d} fewer pieces of rubbish than {Y}.",
         qm="How many more pieces did {X} pick up than {Y}?", qf="How many fewer pieces did {X} pick up than {Y}?",
         qh="How many pieces did {X} pick up?", u=("piece", "pieces"), v="picked up"),
]


def set_compare(rnd, P):
    kinds = ["D"] * 4 + ["F"] * 3 + ["B"] * 3 + ["SF"] * 3 + ["S"] * 4 + ["BF"] * 3
    ctx = rnd.sample(CMP, 11) + rnd.sample(CMP, 9)
    rnd.shuffle(ctx)
    used = set()
    its = []
    for i, (kind, c) in enumerate(zip(kinds, ctx)):
        p = P.two()
        A, B, HeA, v = p["A"], p["B"], p["HeA"], c["v"]
        U = lambda x: unit(x, c["u"])
        rg = i % 3 != 0
        big, d = pick_sub(rnd, 30, 95, 6, 40, rg, used)
        small = big - d
        if kind in ("D", "F"):
            if kind == "D":
                q = say(c["has"], {}, X=A, n=big) + " " + say(c["has"], {}, X=B, n=small) + " " + say(c["qm"], {}, X=A, Y=B)
            else:
                q = say(c["has"], {}, X=A, n=big) + " " + say(c["has"], {}, X=B, n=small) + " " + say(c["qf"], {}, X=B, Y=A)
            ans = d
            e = ("Find the difference. Subtract the smaller number from the bigger one: %d − %d = <b>%d</b>. "
                 "Check: %d + %d = %d." % (big, small, d, small, d, big))
            if kind == "D":
                e += " The word “more” does not mean add here."
            w = [big + small] + sub_wrong(big, small)[:-3] + [big, d + 10, d - 1, d + 1]
            pic = cmp_svg(A, B, big, small, str(big), str(small), "?", "%s %d, %s %d" % (A, big, B, small))
        elif kind == "B":           # A has small; B has d more than A
            q = say(c["has"], {}, X=A, n=small) + " " + say(c["more"], {}, X=B, d=d, Y=A) + " " + say(c["qh"], {}, X=B)
            ans = big
            e = "%s %s %d more than %s, so add: %d + %d = <b>%d</b>." % (B, v, d, A, small, d, big)
            w = [abs(small - d)] + add_wrong(small, d)[:-3] + [d, big + 10, big - 1]
            pic = cmp_svg(B, A, big, small, "?", str(small), str(d), "%s has %d more than %s" % (B, d, A))
        elif kind == "SF":          # A has big; B has d fewer than A
            q = say(c["has"], {}, X=A, n=big) + " " + say(c["fewer"], {}, X=B, d=d, Y=A) + " " + say(c["qh"], {}, X=B)
            ans = small
            e = "%s %s %d fewer than %s, so subtract: %d − %d = <b>%d</b>." % (B, v, d, A, big, d, small)
            w = [big + d] + sub_wrong(big, d)[:-3] + [small + 10, small - 1, small + 1]
            pic = cmp_svg(A, B, big, small, str(big), "?", str(d), "%s has %d fewer than %s" % (B, d, A))
        elif kind == "S":           # A has big; A has d more than B
            q = say(c["has"], {}, X=A, n=big) + " " + say(c["more"], {}, X=HeA, d=d, Y=B) + " " + say(c["qh"], {}, X=B)
            ans = small
            e = ("%s %s %d more than %s, so %s %s %d fewer. Subtract: %d − %d = <b>%d</b>. "
                 "The word “more” is in the story, but you subtract." % (A, v, d, B, B, v, d, big, d, small))
            w = [big + d] + sub_wrong(big, d)[:-3] + [small + 10, small - 1, small + 1]
            pic = cmp_svg(A, B, big, small, str(big), "?", str(d), "%s has %d more than %s" % (A, d, B))
        else:                       # BF: A has small; A has d fewer than B
            q = say(c["has"], {}, X=A, n=small) + " " + say(c["fewer"], {}, X=HeA, d=d, Y=B) + " " + say(c["qh"], {}, X=B)
            ans = big
            e = ("%s %s %d fewer than %s, so %s %s %d more. Add: %d + %d = <b>%d</b>. "
                 "The word “fewer” is in the story, but you add." % (A, v, d, B, B, v, d, small, d, big))
            w = [abs(small - d)] + add_wrong(small, d)[:-3] + [big + 10, big - 1, big + 1]
            pic = cmp_svg(B, A, big, small, "?", str(small), str(d), "%s has %d fewer than %s" % (A, d, B))
        if i % 5 != 4:
            q = fig(pic) + q
        its.append(mcq(q, U(ans), [U(x) for x in w if x > 0], e + " Answer: %s." % U(ans)))
    return {"title": "Compare: how many more?", "items": its}


# ============================================================ set 4: missing parts
PW = [
    dict(t="There are {c} students in the class. {a} are at the library. The rest are in the classroom. How many are in the classroom?",
         u=("student", "students"), lab=("library", "class"), mx=30),
    dict(t="The canteen made {c} pies and sausage rolls. {a} are pies. How many are sausage rolls?",
         u=("sausage roll", "sausage rolls"), lab=("pies", "rolls"), mx=90),
    dict(t="{N} has {c} footy cards. {a} are AFL cards. The rest are rugby league cards. How many are rugby league cards?",
         u=("card", "cards"), lab=("AFL", "league"), mx=99),
    dict(t="A box has {c} pencils. {a} are red. The rest are blue. How many pencils are blue?",
         u=("pencil", "pencils"), lab=("red", "blue"), mx=99),
]


def set_missing(rnd, P):
    its = []
    used = set()
    # 4 kinds × 4 = 16 story problems, plus 4 part-whole; 4 of the stories ask for the number sentence
    kinds = ["CT", "CA", "CT", "PW", "CA", "ST", "CT", "SA", "PW", "CA", "ST", "SA", "CT", "PW", "ST", "CA", "SA", "PW", "ST", "SA"]
    eqs = {2, 7, 11, 16}
    ctx = rnd.sample(JOIN, 16)
    pw = list(PW)
    rnd.shuffle(pw)
    ci = 0
    for i, kind in enumerate(kinds):
        p = P.one()
        rg = i % 4 != 0
        if kind == "PW":
            c = pw.pop()
            tot, a = pick_sub(rnd, 20 if c["mx"] < 40 else 35, c["mx"], 6, c["mx"] - 12, rg if c["mx"] >= 40 else False, used)
            ans = tot - a
            q = say(c["t"], p, c=tot, a=a)
            e = ("You know the whole (%d) and one part (%d). Take the part away: %d − %d = <b>%d</b>. "
                 "Check: %d + %d = %d." % (tot, a, tot, a, ans, a, ans, tot))
            w = [tot + a] + sub_wrong(tot, a)
            pic = tape_svg(str(tot), [str(a), "?"], [a, ans], list(c["lab"]), "in all", "%d in all, %d %s" % (tot, a, c["lab"][0]))
            its.append(mcq(fig(pic) + q, unit(ans, c["u"]), [unit(v, c["u"]) for v in w if v > 0], e + " Answer: %s." % unit(ans, c["u"])))
            continue
        c = ctx[ci]
        ci += 1
        mx = c["mx"]
        U = lambda v: unit(v, c["u"])
        if kind in ("SA", "CA"):
            a, b = pick_add(rnd, 11, mx - 11, mx, rg, used)
            t = a + b
        else:
            a, b = pick_sub(rnd, 30, mx, 8, mx - 15, rg, used)
            t = a - b
        if kind == "CT":
            story = say(c["s"] + " " + c["tks"] + " " + c["now"], p, a=a, c=t)
            qq, ans = say(c["qt"], p), b
            right = "%d − ? = %d" % (a, t)
            bad = ["%d + %d = ?" % (a, t), "? − %d = %d" % (a, t), "%d + ? = %d" % (a, t)]
            why = ("Some went away. %s. Count back from %d to %d, or subtract: %d − %d = <b>%d</b>. Check: %d − %d = %d."
                   % (right.replace("?", Q), a, t, a, t, b, a, b, t))
            wrong = [a + t] + sub_wrong(a, t)[:3] + [b + 10, b - 1]
            pic = tape_svg(str(a), [str(t), "?"], [t, b], ["left", "gone"], "at first", "%d at first, %d left" % (a, t))
        elif kind == "CA":
            story = say(c["s"] + " " + c["ads"] + " " + c["now"], p, a=a, c=t)
            qq, ans = say(c["qa"], p), b
            right = "%d + ? = %d" % (a, t)
            bad = ["%d + %d = ?" % (a, t), "%d − ? = %d" % (a, t), "? − %d = %d" % (a, t)]
            why = ("Some more came. %s. Count on from %d to %d, or subtract: %d − %d = <b>%d</b>. Check: %d + %d = %d."
                   % (right.replace("?", Q), a, t, t, a, b, a, b, t))
            wrong = [t + a] + sub_wrong(t, a)[:3] + [b + 10, b - 1]
            pic = tape_svg(str(t), [str(a), "?"], [a, b], ["at first", "more"], "now", "%d at first, %d now" % (a, t))
        elif kind == "ST":
            story = say(c["ss"] + " " + c["tk"] + " " + c["now"], p, b=b, c=t)
            qq, ans = say(c["qs"], p), a
            right = "? − %d = %d" % (b, t)
            bad = ["%d − %d = ?" % (t, b), "? + %d = %d" % (b, t), "%d − ? = %d" % (b, t)]
            why = ("The start is missing. %s. Put back the ones that went: %d + %d = <b>%d</b>. Check: %d − %d = %d."
                   % (right.replace("?", Q), t, b, a, a, b, t))
            wrong = [abs(t - b)] + add_wrong(t, b)[:-3] + [a + 10, a - 1, a + 1]
            pic = tape_svg("?", [str(t), str(b)], [t, b], ["left", "gone"], "at first", "%d left, %d gone" % (t, b))
        else:   # SA
            story = say(c["ss"] + " " + c["ad"] + " " + c["now"], p, b=b, c=t)
            qq, ans = say(c["qs"], p), a
            right = "? + %d = %d" % (b, t)
            bad = ["%d + %d = ?" % (t, b), "? − %d = %d" % (b, t), "%d − ? = %d" % (b, t)]
            why = ("The start is missing. %s. Take away the ones that came: %d − %d = <b>%d</b>. Check: %d + %d = %d."
                   % (right.replace("?", Q), t, b, a, a, b, t))
            wrong = [t + b] + sub_wrong(t, b)[:3] + [a + 10, a - 1]
            pic = tape_svg(str(t), ["?", str(b)], [a, b], ["at first", "more"], "now", "%d now, %d more" % (t, b))
        check_sentences(right, bad, ans)
        if i in eqs:
            its.append(mcq(story + " Which number sentence matches the story?", right, bad,
                           why + " Answer: %s." % right))
        else:
            its.append(mcq(fig(pic) + story + " " + qq, U(ans), [U(v) for v in wrong if v > 0], why + " Answer: %s." % U(ans)))
    assert ci == 16
    return {"title": "Missing parts: some got off the bus", "items": its}


# ============================================================ set 5: equal groups and two steps
def set_two(rnd, P):
    its = []

    def groups(t, ng, per, kind, u, p):
        ans = ng * per
        q = fig(groups_svg(ng, per, kind, "%d groups of %d" % (ng, per))) + say(t, p, g=ng, n=per)
        add = " + ".join([str(per)] * ng)
        e = ("There are %d equal groups of %d. Add %d again and again: %s = <b>%d</b>. "
             "Do not add %d + %d: that counts the groups, not the things." % (ng, per, per, add, ans, ng, per))
        w = [ng + per, (ng - 1) * per, (ng + 1) * per, per, ans + 1]
        its.append(mcq(q, unit(ans, u), [unit(v, u) for v in w if v > 0 and v != ans], e + " Answer: %s." % unit(ans, u)))

    def share(t, tot, ng, kind, u, p):
        ans = tot // ng
        assert ans * ng == tot
        q = fig(groups_svg(ng, ans, kind, "%d shared into %d groups" % (tot, ng), share_total=tot)) + say(t, p, tot=tot, g=ng)
        e = ("Share them out one at a time into %d groups. Each group gets %d, because %s = %d. Answer: %s."
             % (ng, ans, " + ".join([str(ans)] * ng), tot, unit(ans, u)))
        w = [tot - ng, tot + ng, ng, ans + 1, ans - 1]
        its.append(mcq(q, unit(ans, u), [unit(v, u) for v in w if v > 0 and v != ans], e))

    def step(q, start, j1, j2, ans, s1, s2, u, wrong, slabel=None, pic=None):
        pic = pic or steps_svg(slabel or str(start), j1, j2, "%s, then %s, then %s" % (start, j1.replace("−", "minus "), j2.replace("−", "minus ")))
        e = "Step 1: %s Step 2: %s Answer: %s." % (s1, s2, unit(ans, u))
        its.append(mcq(fig(pic) + q, unit(ans, u), [unit(v, u) for v in wrong if v > 0 and v != ans], e))

    p = P.one()
    groups("There are {g} bags. Each bag has {n} apples. How many apples are there?", 3, 5, "apple", ("apple", "apples"), p)
    groups("{N} has {g} packets of stickers. Each packet has {n} stickers. How many stickers does {N} have?", 4, 2, "star", ("sticker", "stickers"), P.one())
    groups("There are {g} tables in the classroom. {n} students sit at each table. How many students are there?", 5, 4, "kid", ("student", "students"), P.one())
    groups("The coach has {g} bags of balls. Each bag has {n} balls. How many balls are there?", 2, 10, "ball", ("ball", "balls"), P.one())
    groups("There are {g} shelves. Each shelf has {n} books. How many books are there?", 4, 3, "book", ("book", "books"), P.one())
    share("{tot} apples are shared equally into {g} bags. How many apples go in each bag?", 12, 3, "apple", ("apple", "apples"), P.one())
    share("The teacher shares {tot} balls equally between {g} teams. How many balls does each team get?", 10, 2, "ball", ("ball", "balls"), P.one())
    groups("{N} buys {g} packs of juice boxes. Each pack has {n} juice boxes. How many juice boxes does {he} buy?", 3, 4, "counter",
           ("juice box", "juice boxes"), P.one())

    # two-step stories (numbers chosen so that every step stays positive and the answer is not in the story)
    p = P.one()
    a, b, c = 26, 17, 9
    step(say("{N} had {a} stickers. {He} got {b} more. Then {he} gave {c} to {his} sister. How many stickers does {N} have now?", p, a=a, b=b, c=c),
         a, "+%d" % b, "−%d" % c, a + b - c, "%d + %d = %d." % (a, b, a + b), "%d − %d = %d." % (a + b, c, a + b - c),
         ("sticker", "stickers"), [a + b, a + b + c, a - b + c, a + b - c + 10])
    a, b, c = 34, 8, 12
    step("There were %d students on the bus. At the first stop, %d got off and %d got on. How many students are on the bus now?" % (a, b, c),
         a, "−%d" % b, "+%d" % c, a - b + c, "%d − %d = %d." % (a, b, a - b), "%d + %d = %d." % (a - b, c, a - b + c),
         ("student", "students"), [a - b, a - b - c, a + b + c, a - b + c + 10])
    a, b, c = 45, 30, 28
    step("The canteen made %d sausage rolls. Then it made %d more. Students bought %d at recess. How many sausage rolls are left?" % (a, b, c),
         a, "+%d" % b, "−%d" % c, a + b - c, "%d + %d = %d." % (a, b, a + b), "%d − %d = %d." % (a + b, c, a + b - c),
         ("sausage roll", "sausage rolls"), [a + b, a + b + c, sfl(a + b, c), a + b - c + 10])
    a, b, c = 40, 12, 15
    step("There were %d birds in a gum tree. %d birds flew away. Then %d more flew away. How many birds are in the tree now?" % (a, b, c),
         a, "−%d" % b, "−%d" % c, a - b - c, "%d − %d = %d." % (a, b, a - b), "%d − %d = %d." % (a - b, c, a - b - c),
         ("bird", "birds"), [a - b, a - b + c, b + c, a - b - c + 10])
    p = P.one()
    a, b, c = 52, 25, 16
    step(say("The library had {a} books on a shelf. Students borrowed {b}. Then they brought back {c}. How many books are on the shelf now?", p, a=a, b=b, c=c),
         a, "−%d" % b, "+%d" % c, a - b + c, "%d − %d = %d." % (a, b, a - b), "%d + %d = %d." % (a - b, c, a - b + c),
         ("book", "books"), [a - b, a - b - c, a + b + c, sfl(a, b) + c])
    p = P.two()
    a, d = 23, 9
    step("%s has %d shells. %s has %d more shells than %s. How many shells do they have altogether?" % (p["A"], a, p["B"], d, p["A"]),
         a, "+%d" % d, "+%d" % a, 2 * a + d, "%s has %d + %d = %d." % (p["B"], a, d, a + d), "Altogether: %d + %d = %d." % (a, a + d, 2 * a + d),
         ("shell", "shells"), [a + d, 2 * a, 2 * a - d, 2 * a + d + 10])
    p = P.one()
    step(say("{N} has 3 packets of pencils. Each packet has 5 pencils. Then {he} buys 4 more pencils. How many pencils does {he} have?", p),
         15, "+5", "+4", 19, "3 groups of 5: 5 + 5 + 5 = 15.", "15 + 4 = 19.",
         ("pencil", "pencils"), [12, 15, 14], pic=groups_svg(3, 5, "counter", "3 groups of 5 pencils"))
    a, b, c = 60, 24, 17
    step("There are %d chairs in the hall. %d are for parents and %d are for students. The rest are empty. How many chairs are empty?" % (a, b, c),
         a, "−%d" % b, "−%d" % c, a - b - c, "%d − %d = %d." % (a, b, a - b), "%d − %d = %d." % (a - b, c, a - b - c),
         ("chair", "chairs"), [a - b, b + c, a - b + c, a - c])
    a, b, c = 28, 15, 21
    step("There were %d children in the pool. %d more jumped in. Then %d got out. How many children are in the pool now?" % (a, b, c),
         a, "+%d" % b, "−%d" % c, a + b - c, "%d + %d = %d." % (a, b, a + b), "%d − %d = %d." % (a + b, c, a + b - c),
         ("child", "children"), [a + b, a + b + c, a - b + c, a + b - c + 10])
    p = P.one()
    a, b, c = 36, 19, 24
    step(say("The cake stall had {a} cupcakes. People bought {b}. Then {N}'s dad brought {c} more. How many cupcakes are there now?", p, a=a, b=b, c=c),
         a, "−%d" % b, "+%d" % c, a - b + c, "%d − %d = %d." % (a, b, a - b), "%d + %d = %d." % (a - b, c, a - b + c),
         ("cupcake", "cupcakes"), [a - b, a + b + c, sfl(a, b) + c, a - b + c + 10])
    p = P.one()
    step(say("{N} has 90c. {He} buys an apple for 30c and a juice for 45c. How much money does {he} have left?", p),
         90, "−30c", "−45c", 15, "90c − 30c = 60c.", "60c − 45c = 15c.",
         "c", [60, 75, 45, 165], slabel="90c")
    p = P.one()
    step(say("{N} has a 50c coin and two 20c coins. {He} buys a pencil for 35c. How much money is left?", p),
         90, "+40c", "−35c", 55, "50c + 20c + 20c = 90c.", "90c − 35c = 55c.",
         "c", [65, 90, 15, 125], slabel="50c")
    assert 50 + 40 - 35 == 55 and 90 - 30 - 45 == 15 and 3 * 5 + 4 == 19
    # easy → hard: groups and sharing first, then two-step
    order = [0, 1, 4, 3, 2, 7, 5, 6, 8, 11, 9, 16, 10, 12, 17, 15, 14, 13, 18, 19]
    assert sorted(order) == list(range(20))
    its[:] = [its[i] for i in order]
    return {"title": "Equal groups and two-step problems", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>Picture the story first</h2>"
        "<p>Read the story. Ask: <b>what is happening?</b> Do things join, go away, or do we compare two amounts? "
        "Then write a <b>number sentence</b>. Use a <b>?</b> for the number you do not know.</p>"
        + table(["What happens", "Story", "Number sentence"], [
            ["Join (more come)", "26 students are on the bus. 17 more get on.", "26 + 17 = ?"],
            ["Take away (some go)", "45 birds are in a tree. 18 fly away.", "45 − 18 = ?"],
            ["Compare", "Mia has 52 shells. Leo has 37. How many more does Mia have?", "52 − 37 = ?"],
            ["Missing part", "40 students were on the bus. Some got off. 25 are left.", "40 − ? = 25"],
            ["Equal groups", "3 bags with 5 apples in each bag", "5 + 5 + 5 = ?"],
        ]) +
        "<h2>Draw a bar model</h2>"
        "<p>A bar model shows the <b>parts</b> and the <b>whole</b>. If you know both parts, add. "
        "If you know the whole and one part, subtract.</p>"
        "<figure class='sn-fig'>" +
        tape_svg("40", ["25", "?"], [25, 15], ["left", "got off"], "at first", "40 at first, 25 left") +
        "<figcaption>40 students were on the bus. Some got off. 25 are left. 40 − 25 = 15, so 15 got off.</figcaption></figure>"
        + ex("Example", "There were 40 students on the bus. Some got off. Now there are 25. How many got off?",
             "The whole is 40 and one part is 25. Subtract: 40 − 25 = 15. Check: 40 − 15 = 25.", "15 students") +
        "<h2>Compare: how many more?</h2>"
        "<p>To compare, draw two bars. The extra part is the <b>difference</b>. Find it by subtracting.</p>"
        "<figure class='sn-fig'>" +
        cmp_svg("Mia", "Leo", 52, 37, "52", "37", "?", "Mia 52, Leo 37") +
        "<figcaption>Mia has 52 shells and Leo has 37. The dashed part shows how many more Mia has: 52 − 37 = 15.</figcaption></figure>"
        + ex("Example", "Mia has 52 shells. Leo has 37 shells. How many more shells does Mia have?",
             "“How many more” asks for the difference, so subtract: 52 − 37 = 15. Check: 37 + 15 = 52.", "15 shells") +
        "<h2>Equal groups and two steps</h2>"
        "<p>When every group has the same number, add that number again and again.</p>"
        "<figure class='sn-fig'>" + groups_svg(3, 5, "apple", "3 groups of 5") +
        "<figcaption>3 bags of 5 apples: 5 + 5 + 5 = 15 apples.</figcaption></figure>"
        "<p>Some stories have two steps. Work out the first step, then use that answer.</p>"
        "<figure class='sn-fig'>" + steps_svg("26", "+17", "−9", "26, then +17, then minus 9") +
        "<figcaption>26 stickers, get 17 more, give 9 away: 26 + 17 = 43, then 43 − 9 = 34.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding when the question asks “how many more”", "“How many more” is a difference. Subtract: 52 − 37 = 15"],
            ["Using the wrong operation because of one word", "Picture the story. Did things join, go away, or are you comparing?"],
            ["Adding the whole and a part (40 + 25)", "If you know the whole, subtract to find the other part"],
            ["Adding the number of groups and the number in each group (3 + 5)", "3 bags of 5 is 5 + 5 + 5 = 15"],
            ["Stopping after step 1", "Read the question again. What does it ask?"],
        ])
    )


FAQ = [
    {"q": "What word problems do Year 2 students solve in maths?",
     "a": "In the Australian Curriculum, Year 2 students solve join, take-away, compare and missing-part problems, simple money problems and equal-group stories, and they write a number sentence to show what is happening."},
    {"q": "What is a number sentence in Year 2 maths?",
     "a": "A number sentence uses numbers and symbols to show a story, such as 26 + 17 = ? or 40 − ? = 25. The ? stands for the number you need to find."},
    {"q": "How can I help my child decide whether to add or subtract?",
     "a": "Ask them to picture or act out the story first. If things join, add; if some go away or you compare two amounts, subtract. Drawing a bar model helps."},
    {"q": "Why do children add when the question says “how many more”?",
     "a": "They see the word “more” and add. “How many more” asks for the difference between two amounts, so they need to subtract the smaller number from the bigger one."},
]


def mark_large(u):
    """All pictures in this unit are wide, so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:picture of objects|bar model|comparison bars|equal groups|two-step diagram))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(2804)
    P = People(rnd)
    sets = [set_choose(rnd, P), set_join(rnd, P), set_compare(rnd, P), set_missing(rnd, P), set_two(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            for n in re.findall(r"\d+", re.sub(r"<[^>]+>", " ", it["q"]) + " " + " ".join(it["c"])):
                assert int(n) < 1000, it["q"]
    u = {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "word-problems-and-number-sentences",
        "sort": 4, "updated": UPDATED, "pdf_url": "",
        "title": "Word Problems and Number Sentences",
        "seo_title": "Year 2 Word Problems and Number Sentences Worksheets (Australian Curriculum)",
        "short_title": "Word problems and number sentences",
        "domain": "Number",
        "standard_code": "AC9M2N06",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Use mathematical modelling to solve practical additive and multiplicative problems, including money transactions, representing the situation and choosing calculation strategies; interpret and communicate solutions in terms of the situation",
        "meta_desc": "Free Year 2 maths worksheets on word problems and number sentences: choose the number sentence, join and take-away stories, compare problems, missing parts, equal groups, money and two-step problems. 100 questions with pictures and an answer key, matched to the Australian Curriculum.",
        "key_big": "Picture the story. Then choose: add or subtract?",
        "key_sub": "Things join: add. Some go away, or you compare: subtract. Equal groups: add the same number again. Write a number sentence with a ? for the number you need to find.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u)


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
