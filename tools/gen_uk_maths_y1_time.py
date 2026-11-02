# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: Time (National Curriculum in England, Year 1: Measurement)
  python tools/gen_uk_maths_y1_time.py
O’clock and half past on clocks with hands (every clock is drawn from the time itself: the short hand
moves between the numbers as the minutes go by), time words and the order of events,
days of the week and months of the year, and simple time questions from everyday life.
British English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
GREY = "#b9b2a6"
PALE = "#eef5f0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


# ------------------------------------------------------------ time words
def nxt(h):
    return h % 12 + 1


def prv(h):
    return (h - 2) % 12 + 1


def oc(h):
    return "%d o’clock" % ((h - 1) % 12 + 1)


def hp(h):
    return "half past %d" % ((h - 1) % 12 + 1)


def say(h, m):
    return oc(h) if m == 0 else hp(h)


def hands_gap(h, m):
    """Angle in degrees between the short hand and the long hand."""
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def day_after(d, k=1):
    return DAYS[(DAYS.index(d) + k) % 7]


def month_after(mo, k=1):
    return MONTHS[(MONTHS.index(mo) + k) % 12]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set.
    Items marked 'fixed' (A-D clock pictures) already have their position; the rest fill the gaps."""
    for s in sets:
        left = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                left[it["a"]] -= 1
        assert min(left.values()) >= 0
        targets = [p for p in range(4) for _ in range(left[p])]
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fixed")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ pictures
def clock_body(h, m, cx, cy, R):
    """Clock face with numbers. The short hand is placed by the exact time: (h + m/60) x 30 degrees."""
    k = R / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, R, GREEN, 5 * k)]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (13 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (R - 3 * k) * math.cos(a), cy + (R - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), LINE, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), LINE, 2.6 * k))
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.5 * math.cos(ah), cy + R * 0.5 * math.sin(ah), LINE, 8 * k))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.86 * math.cos(am), cy + R * 0.86 * math.sin(am), RED, 4.5 * k))
    fs = 19 * k
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, LINE, 3.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        rn = R - 29 * k
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200):
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6), "clock showing %s" % say(h, m))


def clocks4_svg(times):
    """2 x 2 grid of clocks labelled A-D (square picture, printed large)."""
    CELL = 124
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GREY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GREY)]
    for k, (h, m) in enumerate(times):
        assert hands_gap(h, m) >= 12, (h, m)
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        el.append(clock_body(h, m, x0 + 65, y0 + 63, 56))
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 20, LINE, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), "four clocks labelled A to D")


def wrap2(t, n=11):
    """Split a label into at most 2 lines."""
    if len(t) <= n:
        return [t]
    words = t.split(" ")
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        w = max(len(a), len(b))
        if best is None or w < best[0]:
            best = (w, a, b)
    assert best and best[0] <= 12, t
    return [best[1], best[2]]


def strip_svg(labels, bw=112, gap=24):
    """Boxes in a row joined by arrows (the order of events). '?' is a missing box."""
    BH, FS = 62, 15
    W = len(labels) * bw + (len(labels) - 1) * gap + 8
    H = BH + 8
    el = []
    for i, t in enumerate(labels):
        x = 4 + i * (bw + gap)
        miss = t == "?"
        el.append("<rect x='%d' y='4' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
                  % (x, bw, BH, "#fff" if miss else PALE, RED if miss else GREEN,
                     " stroke-dasharray='7 5'" if miss else ""))
        if miss:
            el.append("<text x='%d' y='%d' font-size='30' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                      % (x + bw // 2, 4 + BH // 2 + 11, RED))
        else:
            ls = wrap2(t)
            assert max(len(s) for s in ls) * FS * 0.58 <= bw - 8, t
            y0 = 4 + BH / 2.0 - (len(ls) - 1) * 9 + 5
            for j, s in enumerate(ls):
                el.append("<text x='%d' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                          % (x + bw // 2, y0 + j * 18, FS, LINE, s))
        if i < len(labels) - 1:
            ax = x + bw + 3
            ay = 4 + BH // 2
            el.append("<path d='M%d %dH%dM%d %dL%d %dL%d %d' stroke='%s' stroke-width='2.5' fill='none' "
                      "stroke-linecap='round' stroke-linejoin='round'/>"
                      % (ax, ay, ax + gap - 6, ax + gap - 11, ay - 6, ax + gap - 6, ay, ax + gap - 11, ay + 6, LINE))
    return svg_wrap(W, H, "".join(el), "boxes in order: " + ", then ".join(labels))


# ------------------------------------------------------------ clock questions
def hour_e(h):
    return ("The long hand is on the <b>12</b>, so it is an o’clock time. "
            "The short hand points to the <b>%d</b>. It is <b>%s</b>." % (h, oc(h)))


def half_e(h):
    return ("The long hand is on the <b>6</b>, so it is half past. "
            "The short hand is halfway <b>between %d and %d</b>. It has gone past the %d but not reached the %d. "
            "It is <b>%s</b>, not %s." % (h, nxt(h), h, nxt(h), hp(h), hp(nxt(h))))


def read_hour(h, rnd, text="What time is it?"):
    rest = [hp(h), oc(nxt(h)), oc(prv(h))]
    rnd.shuffle(rest)
    e = hour_e(h) + " (12 o’clock would mean the short hand is on the 12.)" if h != 12 else hour_e(h)
    return mcq(fig(clock_svg(h, 0)) + text, oc(h), ["12 o’clock"] + rest, e)


def read_half(h, rnd, text="What time is it?"):
    rest = ["6 o’clock" if h != 6 else hp(prv(h)), oc(h), oc(nxt(h))]
    rnd.shuffle(rest)
    return mcq(fig(clock_svg(h, 30)) + text, hp(h), [hp(nxt(h))] + rest, half_e(h))


def four_clocks(h, m, p, rnd):
    """Clock times for A-D: the right one at position p and 3 real mistakes."""
    if m == 0:
        swap = (12, 5 * h)                       # long hand on the hour number, short hand near the 12
        wrong = [swap, (nxt(h), 0), (h, 30)]
    else:
        swap = (6, 5 * h) if h != 6 else None    # short hand near the 6, long hand on the hour number
        wrong = [(nxt(h), 30), (h, 0), swap if swap else (prv(h), 30)]
    rnd.shuffle(wrong)
    times = wrong[:p] + [(h, m)] + wrong[p:]
    assert len(set(times)) == 4
    L = "ABCD"[p]
    if m == 0:
        e = "Clock %s has the long hand on the 12 and the short hand on the %d. It shows <b>%s</b>." % (L, h, oc(h))
    else:
        e = ("Clock %s has the long hand on the 6 and the short hand halfway between %d and %d. It shows <b>%s</b>."
             % (L, h, nxt(h), hp(h)))
    if swap in times:
        e += " Clock %s has the hands swapped: the long hand is on the %d." % ("ABCD"[times.index(swap)], h)
    if (nxt(h), 30) in times:
        e += " Clock %s shows %s." % ("ABCD"[times.index((nxt(h), 30))], hp(nxt(h)))
    return times, e


def clocks_item(top, h, m, p, rnd):
    times, e = four_clocks(h, m, p, rnd)
    return {"q": top + fig(clocks4_svg(times)), "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True}


# ============================================================ set 1: o’clock
def set_oclock(rnd):
    its = []
    hrs = [h for h in range(1, 12) if h != 7]
    rnd.shuffle(hrs)
    for h in hrs:                                # no 12 o’clock picture: both hands on the 12 look like one hand
        its.append(read_hour(h, rnd))
    its.append(mcq("Which hand tells you the <b>hour</b>?", "the short hand",
                   ["the long hand", "both hands", "the number 12"],
                   "The <b>short hand</b> is the hour hand. The long hand shows the minutes."))
    its.append(mcq("At every o’clock time, where does the long hand point?", "to the 12",
                   ["to the 6", "to the 1", "to the 3"],
                   "At 1 o’clock, 2 o’clock and every o’clock time, the long hand points straight up to the <b>12</b>."))
    its.append(mcq("At <b>8 o’clock</b>, where does the short hand point?", "to the 8",
                   ["to the 12", "to the 9", "between 8 and 9"],
                   "At 8 o’clock the short hand points right <b>to the 8</b>. The long hand points to the 12."))
    its.append(mcq("At <b>12 o’clock</b>, where are the two hands?", "both on the 12",
                   ["both on the 6", "on the 12 and the 6", "on the 1 and the 12"],
                   "The short hand is on the 12 for the hour. The long hand is on the 12 for o’clock. "
                   "So <b>both hands are on the 12</b>, one on top of the other."))
    its.append(mcq("The long hand is on the 12. The short hand is on the 5. What time is it?", "5 o’clock",
                   ["12 o’clock", "half past 5", "6 o’clock"],
                   "The short hand tells the hour: <b>5</b>. The long hand on the 12 means o’clock. It is <b>5 o’clock</b>."))
    its.append(mcq("The long hand is on the 12. The short hand is on the 2. What time is it?", "2 o’clock",
                   ["12 o’clock", "half past 2", "3 o’clock"],
                   "The short hand tells the hour: <b>2</b>. The long hand on the 12 means o’clock. It is <b>2 o’clock</b>. "
                   "(12 o’clock mixes up the hands.)"))
    its.append(mcq("At <b>6 o’clock</b>, where does the long hand point?", "to the 12",
                   ["to the 6", "to the 1", "between 6 and 7"],
                   "At 6 o’clock the long hand points <b>to the 12</b>. It is the short hand that points to the 6."))
    for (h, p) in [(7, 2), (4, 0), (10, 3)]:
        its.append(clocks_item("Which clock shows <b>%s</b>?" % oc(h), h, 0, p, rnd))
    assert len(its) == 20, len(its)
    return {"title": "O’clock times", "items": its}


# ============================================================ set 2: half past
def set_half(rnd):
    its = []
    hrs = [h for h in range(1, 13) if h not in (5,)]
    rnd.shuffle(hrs)
    hrs = hrs[:10]
    for h in hrs:
        its.append(read_half(h, rnd))
    its.append(mcq("At every half past time, where does the long hand point?", "to the 6",
                   ["to the 12", "to the 3", "to the 30"],
                   "Half past means the long hand has gone <b>half of the way round</b>. It points straight down to the <b>6</b>."))
    its.append(mcq("At <b>half past 9</b>, where does the long hand point?", "to the 6",
                   ["to the 9", "to the 12", "to the 3"],
                   "At half past, the long hand always points <b>to the 6</b>. The short hand is between 9 and 10."))
    its.append(mcq("Half past is how long after the o’clock time?", "half an hour",
                   ["1 hour", "6 minutes", "a day"],
                   "Half past 1 is <b>half an hour</b> after 1 o’clock. The long hand goes half of the way round."))
    its.append(mcq("At <b>half past 2</b>, where is the short hand?", "between 2 and 3",
                   ["on the 2", "on the 3", "between 1 and 2"],
                   "The short hand moves slowly. In half an hour it goes halfway to the next number. "
                   "At half past 2 it is halfway <b>between 2 and 3</b>."))
    its.append(mcq("At <b>half past 10</b>, where is the short hand?", "between 10 and 11",
                   ["on the 10", "on the 11", "between 9 and 10"],
                   "At half past 10 the short hand has gone past the 10. It is halfway <b>between 10 and 11</b>."))
    its.append(mcq("<b>Half past 4</b> is half an hour after …", "4 o’clock",
                   ["5 o’clock", "half past 3", "6 o’clock"],
                   "Half past 4 comes <b>half an hour after 4 o’clock</b>. Then 5 o’clock comes next."))
    its.append(mcq("The long hand is on the 6. The short hand is between 7 and 8. What time is it?", "half past 7",
                   ["half past 8", "7 o’clock", "6 o’clock"],
                   "The long hand on the 6 means half past. Use the number the short hand has <b>gone past</b>: 7. "
                   "It is <b>half past 7</b>."))
    for (h, p) in [(5, 1), (8, 3), (11, 0)]:
        its.append(clocks_item("Which clock shows <b>%s</b>?" % hp(h), h, 30, p, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Half past times", "items": its}


# ============================================================ set 3: time words and order of events
def set_order(rnd, P):
    its = []
    n, he, his = P.next()
    its.append(mcq("%s eats breakfast. When is that?" % n, "in the morning",
                   ["in the evening", "in the afternoon", "at night"],
                   "Breakfast is the first meal of the day. We eat it <b>in the morning</b>."))
    its.append(mcq("The sun comes up. What part of the day is it?", "the morning",
                   ["the evening", "the afternoon", "lunchtime"],
                   "The sun comes up at the start of the day. That is <b>the morning</b>."))
    its.append(mcq("Which happens in the morning?", "getting up",
                   ["going to bed", "having tea", "home time"],
                   "We <b>get up</b> in the morning. Tea and bedtime are in the evening. Home time is in the afternoon."))
    its.append(mcq("School finishes for the day. What part of the day is it?", "the afternoon",
                   ["the morning", "the evening", "night"],
                   "School finishes after lunch, before tea. That is <b>the afternoon</b>."))
    n, he, his = P.next()
    its.append(mcq("%s goes to bed. When is that?" % n, "in the evening",
                   ["in the morning", "in the afternoon", "at lunchtime"],
                   "Children go to bed at the end of the day, <b>in the evening</b>."))
    its.append(mcq("Which happens in the evening?", "having tea",
                   ["eating breakfast", "getting up", "morning register"],
                   "Tea is the meal at the end of the day. We have it <b>in the evening</b>."))
    its.append(mcq("Which part of the school day comes <b>first</b>?", "the morning",
                   ["lunchtime", "the afternoon", "the evening"],
                   "The day goes in this order: <b>morning</b>, lunchtime, afternoon, evening."))
    its.append(mcq("Which part of the day comes <b>straight after</b> the afternoon?", "the evening",
                   ["the morning", "lunchtime", "breakfast time"],
                   "Morning, afternoon, then <b>evening</b>. The evening comes straight after the afternoon."))
    its.append(mcq("Put these in order: evening, morning, afternoon. Which is in the <b>middle</b>?", "the afternoon",
                   ["the morning", "the evening", "lunchtime"],
                   "The order is morning, <b>afternoon</b>, evening. The afternoon is in the middle."))
    # boxes in order
    s1 = ["wake up", "get dressed", "eat breakfast", "go to school"]
    its.append(mcq(fig(strip_svg(s1)) + "What happens <b>first</b>?", "wake up",
                   ["go to school", "eat breakfast", "get dressed"],
                   "Follow the arrows from the left. The first box is <b>wake up</b>."))
    s2 = ["mix it", "bake it", "let it cool", "eat it"]
    its.append(mcq(fig(strip_svg(s2)) + "We make a cake. What happens <b>last</b>?", "eat it",
                   ["mix it", "let it cool", "bake it"],
                   "Follow the arrows to the end. The last box is <b>eat it</b>. (Mix it is first, not last.)"))
    s3 = ["plant a seed", "water it", "it grows", "a flower opens"]
    its.append(mcq(fig(strip_svg(s3)) + "What happens <b>next</b>, after “water it”?", "it grows",
                   ["plant a seed", "a flower opens", "water it"],
                   "Find “water it”. Follow the arrow to the next box: <b>it grows</b>. "
                   "(Plant a seed comes before, not after.)"))
    s4 = ["it snows", "make a snowman", "the sun comes out", "the snowman melts"]
    its.append(mcq(fig(strip_svg(s4)) + "What happens <b>just before</b> “the snowman melts”?", "the sun comes out",
                   ["it snows", "make a snowman", "the snowman melts"],
                   "Find “the snowman melts”. Look at the box just before it: <b>the sun comes out</b>."))
    s5 = ["have tea", "have a bath", "?", "go to sleep"]
    its.append(mcq(fig(strip_svg(s5)) + "What goes in the box with the <b>?</b>", "read a story",
                   ["wake up", "eat breakfast", "go to school"],
                   "It comes after a bath and before sleep, so it is in the evening: <b>read a story</b>. "
                   "Waking up, breakfast and school are in the morning."))
    s6 = ["morning lessons", "?", "afternoon lessons", "home time"]
    its.append(mcq(fig(strip_svg(s6)) + "What goes in the box with the <b>?</b>", "lunchtime",
                   ["breakfast", "bedtime", "wake up"],
                   "It comes after the morning and before the afternoon. That is <b>lunchtime</b>."))
    n, he, his = P.next()
    its.append(mcq("%s gets up. Next %s has breakfast. Then %s goes to school. What does %s do <b>last</b>?"
                   % (n, he, he, he), "goes to school",
                   ["gets up", "has breakfast", "has tea"],
                   "First %s gets up. Next %s has breakfast. Last, %s <b>goes to school</b>." % (he, he, he)))
    n, he, his = P.next()
    its.append(mcq("%s eats lunch. After lunch, %s plays outside. What does %s do <b>first</b>?" % (n, he, he),
                   "eats lunch", ["plays outside", "goes to bed", "has a bath"],
                   "“After lunch, %s plays” means lunch comes first. So %s <b>eats lunch</b> first." % (he, he)))
    its.append(mcq("You put on your socks ____ your shoes.", "before",
                   ["after", "at the same time as", "instead of"],
                   "Socks go on your feet first. Then shoes go on top. So socks go on <b>before</b> your shoes."))
    its.append(mcq("You dry your hands ____ you wash them.", "after",
                   ["before", "at the same time as", "instead of"],
                   "First you wash your hands. Then you dry them. So you dry them <b>after</b> you wash them."))
    its.append(mcq("Tea is in the evening. Breakfast is in the morning. Which do you have <b>first</b> in the day?",
                   "breakfast", ["tea", "they are at the same time", "you can’t tell"],
                   "The morning comes before the evening. So <b>breakfast</b> comes first."))
    assert len(its) == 20, len(its)
    return {"title": "Morning, afternoon, evening and the order of events", "items": its}


# ============================================================ set 4: days and months
def set_calendar(rnd):
    its = []
    its.append(mcq("How many days are there in a <b>week</b>?", "7", ["5", "12", "10"],
                   "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. That is <b>7 days</b>. "
                   "(5 is only the school days.)"))
    for d, w in [("Tuesday", ["Monday", "Thursday", "Saturday"]),
                 ("Monday", ["Sunday", "Wednesday", "Saturday"]),
                 ("Sunday", ["Saturday", "Tuesday", "Friday"])]:
        a = day_after(d)
        its.append(mcq("Which day comes <b>just after %s</b>?" % d, a, w,
                       ("Sunday is the last day of the week. Then a new week starts with <b>Monday</b>."
                        if d == "Sunday" else
                        "Say the days in order: … %s, <b>%s</b> … So %s comes just after %s." % (d, a, a, d))))
    its.append(mcq("Which day comes <b>just before Friday</b>?", "Thursday", ["Saturday", "Wednesday", "Sunday"],
                   "Say the days in order: Wednesday, <b>Thursday</b>, Friday. Thursday comes just before Friday. "
                   "(Saturday comes after Friday.)"))
    days5 = ["Monday", "Tuesday", "?", "Thursday", "Friday"]
    its.append(mcq(fig(strip_svg(days5, bw=96, gap=20)) + "Which day is missing?", "Wednesday",
                   ["Saturday", "Sunday", "Thursday"],
                   "Tuesday comes before the gap and Thursday comes after it. The missing day is <b>Wednesday</b>."))
    its.append(mcq("Which two days are the <b>weekend</b>?", "Saturday and Sunday",
                   ["Friday and Saturday", "Sunday and Monday", "Monday and Friday"],
                   "Most children go to school from Monday to Friday. <b>Saturday and Sunday</b> are the weekend."))
    its.append(mcq("Which day comes just before the weekend?", "Friday", ["Saturday", "Monday", "Thursday"],
                   "The weekend starts on Saturday. The day just before Saturday is <b>Friday</b>."))
    its.append(mcq("The day <b>after today</b> is called …", "tomorrow", ["yesterday", "today", "last week"],
                   "Yesterday was the day before today. <b>Tomorrow</b> is the day after today."))
    its.append(mcq("The day <b>before today</b> is called …", "yesterday", ["tomorrow", "today", "next week"],
                   "<b>Yesterday</b> is the day before today. Tomorrow is the day after today."))
    its.append(mcq("Today is <b>Monday</b>. What day was <b>yesterday</b>?", "Sunday",
                   ["Tuesday", "Saturday", "Wednesday"],
                   "Yesterday is the day <b>before</b> today. The day before Monday is <b>Sunday</b>. "
                   "(Tuesday is tomorrow.)"))
    its.append(mcq("Today is <b>Thursday</b>. What day will it be <b>tomorrow</b>?", "Friday",
                   ["Wednesday", "Saturday", "Tuesday"],
                   "Tomorrow is the day <b>after</b> today. The day after Thursday is <b>Friday</b>. "
                   "(Wednesday was yesterday.)"))
    its.append(mcq("<b>Yesterday</b> was Friday. What day is it today?", "Saturday",
                   ["Thursday", "Sunday", "Friday"],
                   "Today is the day after yesterday. The day after Friday is <b>Saturday</b>."))
    its.append(mcq("<b>Tomorrow</b> will be Wednesday. What day is it today?", "Tuesday",
                   ["Thursday", "Wednesday", "Monday"],
                   "Today is the day before tomorrow. The day before Wednesday is <b>Tuesday</b>."))
    its.append(mcq("How many months are there in a <b>year</b>?", "12", ["7", "10", "24"],
                   "January to December. Count them: there are <b>12 months</b> in a year. (7 is the days in a week.)"))
    its.append(mcq("Which is the <b>first</b> month of the year?", "January", ["December", "March", "June"],
                   "The year starts with <b>January</b>. December is the last month."))
    its.append(mcq("Which month comes <b>just after March</b>?", "April", ["February", "May", "June"],
                   "Say the months in order: February, March, <b>April</b>, May. April comes just after March."))
    its.append(mcq("Which month comes <b>just before June</b>?", "May", ["July", "April", "March"],
                   "Say the months in order: April, <b>May</b>, June, July. May comes just before June."))
    its.append(mcq("Which month comes <b>just after December</b>?", "January", ["November", "February", "October"],
                   "December is the last month. Then a new year starts with <b>January</b>."))
    mons = ["August", "September", "?", "November"]
    its.append(mcq(fig(strip_svg(mons)) + "Which month is missing?", "October",
                   ["December", "July", "January"],
                   "September comes before the gap and November comes after it. The missing month is <b>October</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Days of the week and months of the year", "items": its}


# ============================================================ set 5: time in everyday life
def set_life(rnd, P):
    its = []
    acts = [("School starts in the morning. What time is it?", 9, 0),
            ("It is playtime. What time is it?", 10, 30),
            ("It is lunchtime at school. What time is it?", 12, 30),
            ("It is home time. What time is it?", 3, 30),
            ("{n} has tea. What time is it?", 5, 0),
            ("{n} goes to bed in the evening. What time is it?", 7, 0)]
    for q, h, m in acts:
        n, he, his = P.next()
        t = q.format(n=n)
        its.append(read_hour(h, rnd, t) if m == 0 else read_half(h, rnd, t))
    its.append(mcq("It is <b>3 o’clock</b>. What time will it be in <b>1 hour</b>?", "4 o’clock",
                   ["2 o’clock", "half past 3", "5 o’clock"],
                   "In 1 hour the short hand moves on to the next number. 3 o’clock → <b>4 o’clock</b>. "
                   "(2 o’clock was 1 hour ago.)"))
    its.append(mcq("It is <b>9 o’clock</b>. What time will it be in <b>half an hour</b>?", "half past 9",
                   ["half past 10", "10 o’clock", "half past 8"],
                   "In half an hour the long hand goes from the 12 down to the 6. 9 o’clock → <b>half past 9</b>. "
                   "(10 o’clock is 1 hour later.)"))
    its.append(mcq("It is <b>half past 4</b>. What time will it be in <b>half an hour</b>?", "5 o’clock",
                   ["half past 5", "4 o’clock", "6 o’clock"],
                   "In half an hour the long hand goes from the 6 back up to the 12. A new hour starts: <b>5 o’clock</b>. "
                   "(Half past 5 is 1 hour later.)"))
    its.append(mcq("It is <b>half past 2</b>. What time will it be in <b>1 hour</b>?", "half past 3",
                   ["3 o’clock", "half past 1", "4 o’clock"],
                   "In 1 hour the hour goes up by 1 and it is still half past. Half past 2 → <b>half past 3</b>."))
    its.append(mcq("Which time is the <b>earliest</b> in the morning?", "7 o’clock",
                   ["half past 7", "8 o’clock", "half past 8"],
                   "The order is 7 o’clock, half past 7, 8 o’clock, half past 8. The earliest is <b>7 o’clock</b>."))
    its.append(mcq("Which time is the <b>latest</b> in the afternoon?", "4 o’clock",
                   ["half past 3", "3 o’clock", "half past 2"],
                   "The order is half past 2, 3 o’clock, half past 3, 4 o’clock. The latest is <b>4 o’clock</b>. "
                   "(Half past 3 comes before 4 o’clock.)"))
    n, he, his = P.next()
    its.append(mcq("Swimming starts at 10 o’clock. %s gets there at half past 9. Is %s early or late?" % (n, he),
                   "early", ["late", "on time", "a day late"],
                   "Half past 9 comes <b>before</b> 10 o’clock. So %s is <b>early</b>." % n))
    n, he, his = P.next()
    its.append(mcq("The bus comes at half past 8. %s gets to the bus stop at 9 o’clock. Is %s early or late?" % (n, he),
                   "late", ["early", "on time", "a day early"],
                   "9 o’clock comes <b>after</b> half past 8. So %s is <b>late</b>." % n))
    n, he, his = P.next()
    its.append(mcq("A film starts at 4 o’clock. It ends at 5 o’clock. How long is the film?", "1 hour",
                   ["half an hour", "5 hours", "9 hours"],
                   "From 4 o’clock to 5 o’clock the short hand moves on 1 number. That is <b>1 hour</b>. "
                   "(5 is the end time, not how long.)"))
    n, he, his = P.next()
    its.append(mcq("%s reads from 6 o’clock to half past 6. How long does %s read?" % (n, he), "half an hour",
                   ["1 hour", "6 minutes", "6 hours"],
                   "From 6 o’clock to half past 6 the long hand goes from the 12 to the 6. That is <b>half an hour</b>."))
    n, he, his = P.next()
    its.append(mcq("Today is Friday. %s’s party is <b>tomorrow</b>. What day is the party?" % n, "Saturday",
                   ["Thursday", "Friday", "Sunday"],
                   "Tomorrow is the day after today. The day after Friday is <b>Saturday</b>. (Thursday was yesterday.)"))
    n, he, his = P.next()
    its.append(mcq("Today is Tuesday. %s went to the park <b>yesterday</b>. What day was that?" % n, "Monday",
                   ["Wednesday", "Tuesday", "Sunday"],
                   "Yesterday is the day before today. The day before Tuesday is <b>Monday</b>. (Wednesday is tomorrow.)"))
    n, he, his = P.next()
    its.append(mcq("%s’s birthday is in the month just after May. Which month is it?" % n, "June",
                   ["April", "July", "March"],
                   "Say the months in order: April, May, <b>June</b>. June comes just after May."))
    its.append(mcq("Christmas Day is in December. Which month comes just <b>before</b> December?", "November",
                   ["January", "October", "September"],
                   "Say the months in order: October, <b>November</b>, December. November comes just before December."))
    assert len(its) == 20, len(its)
    return {"title": "Time in everyday life", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The two hands</h2>"
        "<p>A clock has two hands. The <b>short hand</b> is the hour hand. The <b>long hand</b> is the minute hand. "
        "Look at the long hand first. Then look at the short hand.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 0, size=220) +
        "<figcaption>The long hand (red) is on the 12. The short hand (black) is on the 3. It is 3 o’clock.</figcaption></figure>"
        "<ol class='rk-step'>"
        "<li><b>Long hand on the 12:</b> it is an o’clock time.</li>"
        "<li><b>Long hand on the 6:</b> it is half past.</li>"
        "<li><b>Short hand:</b> it tells the hour. If it is between two numbers, use the number it has <b>gone past</b>.</li></ol>"
        "<h2>Half past</h2>"
        "<p>Half past means half an hour after the o’clock time. The long hand has gone half of the way round. "
        "The short hand has moved halfway to the next number.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 30, size=220) +
        "<figcaption>The long hand is on the 6. The short hand is halfway between 3 and 4. It is half past 3.</figcaption></figure>"
        + table(["Time", "Long hand", "Short hand"], [
            ["3 o’clock", "on the 12", "on the 3"],
            ["half past 3", "on the 6", "between 3 and 4"],
            ["4 o’clock", "on the 12", "on the 4"],
        ])
        + ex("Example 1", "The long hand is on the 12. The short hand is on the 9. What time is it?",
             "The long hand on the 12 means o’clock. The short hand tells the hour: 9.", "9 o’clock")
        + ex("Example 2", "The long hand is on the 6. The short hand is between 6 and 7. What time is it?",
             "The long hand on the 6 means half past. The short hand has gone past the 6, so the hour is 6.", "half past 6")
        + "<h2>Time words and the order of events</h2>"
        "<p>The day goes in order: <b>morning</b>, <b>afternoon</b>, <b>evening</b>. "
        "Use <b>first</b>, <b>next</b>, <b>then</b> and <b>last</b> to tell things in order. "
        "<b>Before</b> means earlier. <b>After</b> means later.</p>"
        "<figure class='sn-fig'>" + strip_svg(["wake up", "eat breakfast", "go to school", "go to bed"]) +
        "<figcaption>Follow the arrows. First wake up, next eat breakfast, then go to school. Last of all, go to bed.</figcaption></figure>"
        + table(["Word", "Means"], [
            ["yesterday", "the day before today"],
            ["today", "this day"],
            ["tomorrow", "the day after today"],
        ])
        + "<h2>Days and months</h2>"
        "<p>There are <b>7 days</b> in a week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. "
        "Saturday and Sunday are the weekend.</p>"
        "<p>There are <b>12 months</b> in a year: January, February, March, April, May, June, July, August, "
        "September, October, November, December.</p>"
        + ex("Example 3", "Today is Wednesday. What day will it be tomorrow?",
             "Tomorrow is the day after today. Say the days: Wednesday, Thursday.", "Thursday")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Reading half past 3 as half past 4 because the short hand is near the 4",
             "Use the number the short hand has gone past: half past 3"],
            ["Mixing up the hands (reading half past 3 as 6 o’clock)", "Short hand = hour. Long hand on the 6 = half past"],
            ["Mixing up yesterday and tomorrow", "Yesterday is before today. Tomorrow is after today"],
            ["Saying the days out of order", "Say them in order every day: Monday, Tuesday, Wednesday …"],
        ])
    )


FAQ = [
    {"q": "What time should a Year 1 child be able to tell?",
     "a": "In Year 1, children tell the time to the hour and half past the hour, like 3 o’clock and half past 3, "
          "and draw the hands on a clock. Quarter past, quarter to and 5-minute times come in Year 2."},
    {"q": "What does half past mean on a clock?",
     "a": "Half past means half an hour after the o’clock time. At half past 3 the long hand points to the 6 "
          "and the short hand is halfway between the 3 and the 4."},
    {"q": "Why is the hour hand between two numbers at half past?",
     "a": "The hour hand moves slowly all through the hour. At half past 3 it has gone halfway from the 3 to the 4, "
          "so the hour is still 3."},
    {"q": "How can I help my child learn the days of the week and months of the year?",
     "a": "Say them in order every day and talk about yesterday, today and tomorrow, for example "
          "“Today is Monday, so tomorrow is Tuesday.” Point out the month on a calendar and link it to birthdays and holidays."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D clocks, boxes in a row) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(1108)
    P = People(rnd)
    sets = [set_oclock(rnd), set_half(rnd), set_order(rnd, P), set_calendar(rnd), set_life(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + it["q"][-300:] + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            # every single clock picture shows an o’clock or half past time, never 12 o’clock
            assert "aria-label='clock showing 12 o’clock'" not in it["q"]
            # the right answer, if it is a clock time, is o’clock or half past
            r = it["c"][it["a"]]
            if "o’clock" in r or "half past" in r:
                assert re.fullmatch(r"(\d{1,2} o’clock|half past \d{1,2})", r), r
            for x in it["c"]:
                assert "'" not in x and "\\" not in x
    u = {
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "time", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Time: O’clock, Half Past, Days and Months",
        "seo_title": "Year 1 Time Worksheets: O’clock, Half Past, Days of the Week and Months (Free, with Answers)",
        "short_title": "Time",
        "domain": "Measurement",
        "standard_code": "Year 1: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Sequence events in chronological order using language [for example, before and after, next, first, "
                         "today, yesterday, tomorrow, morning, afternoon and evening]; recognise and use language relating "
                         "to dates, including days of the week, weeks, months and years; tell the time to the hour and half "
                         "past the hour and draw the hands on a clock face to show these times.",
        "meta_desc": "Free Year 1 maths worksheets on time: o’clock and half past on clocks, morning, afternoon and evening, "
                     "putting events in order, yesterday and tomorrow, days of the week and months of the year. "
                     "100 picture questions with an answer key, following the National Curriculum.",
        "key_big": "Long hand on the 12: o’clock. Long hand on the 6: half past.",
        "key_sub": "The short hand tells the hour. At half past it is between two numbers: use the number it has gone past, "
                   "so half past 3, not half past 4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "four clocks labelled A to D|boxes in order")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
