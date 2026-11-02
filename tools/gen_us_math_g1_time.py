# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Telling Time to the Hour and Half Hour (1.MD.B.3)
  python tools/gen_us_math_g1_time.py
Every time is on the hour (:00) or the half hour (:30). Every clock picture is drawn from the time itself
(the short hand moves between the numbers as the minutes go by).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
GRAY = "#b9b2a6"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ time
def tm(h, m, ap=""):
    assert 0 <= m < 60, m
    h = (h - 1) % 12 + 1
    return "%d:%02d%s" % (h, m, (" " + ap) if ap else "")


def hands_gap(h, m):
    """Angle in degrees between the short hand and the long hand."""
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def nxt(h):
    return h % 12 + 1


def prv(h):
    return (h - 2) % 12 + 1


def mins(n):
    return "%d minute%s" % (n, "" if n == 1 else "s")


# ------------------------------------------------------------ helpers
def tidy(t):
    return t.replace("a.m..", "a.m.").replace("p.m..", "p.m.").replace("m.</b>.", "m.</b>")


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
    return {"q": tidy(q), "c": [correct] + pick, "a": 0, "e": tidy(e)}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set.
    Items marked 'fixed' (A-D clock pictures) already have their position; the rest fill the gaps."""
    for s in sets:
        left = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                left[it["a"]] -= 1
        targets = [p for p in range(4) for _ in range(left[p])]
        assert min(left.values()) >= 0
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


def cap(s):
    return s[0].upper() + s[1:]


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
def clock_body(h, m, cx, cy, R, ring=False):
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
    # hands first; the numbers are drawn on top with a white edge so they stay easy to read
    if h is not None:
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
    if ring:      # minutes written outside the face
        s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle'>" % (14 * k, RED))
        for n in range(1, 13):
            a = math.radians(n * 30 - 90)
            rn = R + 17 * k
            s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + 5 * k, (n * 5) % 60))
        s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200, ring=False):
    pad = 26 if ring else 0
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6 - pad, ring), "clock showing %s" % tm(h, m))


def clocks4_svg(times):
    """2 x 2 grid of clocks labeled A-D (square picture, printed large)."""
    CELL = 124
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY)]
    for k, (h, m) in enumerate(times):
        assert hands_gap(h, m) >= 12, (h, m)
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        el.append(clock_body(h, m, x0 + 65, y0 + 63, 56))
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 20, LINE, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), "four clocks labeled A to D")


def digital_svg(t):
    W, H = 190, 84
    s = ["<rect x='4' y='4' width='%d' height='%d' rx='14' fill='#fff' stroke='%s' stroke-width='5'/>" % (W - 8, H - 8, GREEN),
         "<rect x='18' y='16' width='%d' height='%d' rx='6' fill='#eef5f0' stroke='%s' stroke-width='1.5'/>" % (W - 36, H - 32, GRAY),
         "<text x='%d' y='%d' font-size='42' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (W // 2, H // 2 + 15, LINE, t)]
    return svg_wrap(W, H, "".join(s), "digital clock showing %s" % t)



# ------------------------------------------------------------ Grade 1 wrong answers (real mistakes)
def hour_cands(h):
    """Wrong readings of a clock at h:00."""
    return ["12:%02d" % h if h < 12 else None,   # hands switched: long hand read as the hour, short hand as minutes
            "%d:12" % h,                          # the 12 read as 12 minutes
            tm(nxt(h), 0), tm(prv(h), 0), tm(h, 30)]


def half_cands(h):
    """Wrong readings of a clock at h:30."""
    return [tm(nxt(h), 30),                       # short hand is past the middle, read as the next number
            "%d:06" % h,                          # the 6 read as 6 minutes
            tm(h, 0), tm(prv(h), 30)]


def hour_e(h):
    return ("The short hand points to the <b>%d</b>. The long hand points to the <b>12</b>. "
            "It is %d o'clock: <b>%s</b>." % (h, h, tm(h, 0)))


def half_e(h):
    return ("The long hand points to the <b>6</b>. That is half of the way around, 30 minutes. "
            "The short hand is halfway <b>between %d and %d</b>. It has not reached the %d yet, so the hour is %d. "
            "It is <b>%s</b>, half past %d." % (h, nxt(h), nxt(h), h, tm(h, 30), h))


def read_q(h, m, text="What time is it?"):
    return mcq(fig(clock_svg(h, m)) + text, tm(h, m), hour_cands(h) if m == 0 else half_cands(h),
               hour_e(h) if m == 0 else half_e(h))


# ============================================================ set 1: time to the hour
def set_hour(rnd):
    its = []
    hrs = list(range(1, 12))
    rnd.shuffle(hrs)
    for h in hrs:                               # no 12:00 picture: both hands on the 12 look like one hand
        its.append(read_q(h, 0))
    its.append(mcq("It is <b>12 o'clock</b>. Where are the two hands?", "both on the 12",
                   ["both on the 6", "on the 12 and the 6", "on the 1 and the 12"],
                   "The short hand is on the 12 for the hour. The long hand is on the 12 for 0 minutes. "
                   "So <b>both hands are on the 12</b>, one on top of the other."))
    for h in rnd.sample([2, 5, 9, 11], 2):
        its.append(mcq("How do you say <b>%s</b>?" % tm(h, 0), "%d o'clock" % h,
                       ["half past %d" % h, "12 o'clock", "%d o'clock" % nxt(h), "%d o'clock" % prv(h)],
                       "The minutes are :00. It is right on the hour, so you say <b>%d o'clock</b>." % h))
    for h in [4, 10]:
        its.append(mcq("How do you write <b>%d o'clock</b>?" % h, tm(h, 0),
                       ["%d:0" % h, "12:%02d" % h, "%d:30" % h],
                       "%d o'clock means the hour is %d and there are 0 minutes. Write <b>%s</b>." % (h, h, tm(h, 0))))
    for h in [3, 8]:
        its.append(mcq(fig(clock_svg(h, 0)) + "Which words tell the time?", "%d o'clock" % h,
                       ["12 o'clock", "%d o'clock" % nxt(h), "half past %d" % h],
                       "The long hand is on the 12 and the short hand is on the %d. That is <b>%d o'clock</b>. "
                       "(12 is where the long hand points, not the hour.)" % (h, h)))
    its.append(mcq("At every o'clock time, where does the long hand point?", "on the 12",
                   ["on the 6", "on the 1", "on the 3"],
                   "At 1:00, 2:00, 3:00 and every o'clock time, the long hand points straight up to the <b>12</b>."))
    its.append(mcq("How many minutes are in <b>1 hour</b>?", mins(60), [mins(12), mins(30), mins(100)],
                   "In 1 hour the long hand goes all the way around the clock. That is <b>60 minutes</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Time to the hour", "items": its}


# ============================================================ set 2: time to the half hour
def set_half(rnd):
    its = []
    hrs = list(range(1, 13))
    rnd.shuffle(hrs)
    for h in hrs:
        its.append(read_q(h, 30))
    for h in [2, 7]:
        its.append(mcq("What time is <b>half past %d</b>?" % h, tm(h, 30),
                       [tm(nxt(h), 30), "%d:03" % h, tm(h, 0)],
                       "<b>Half past %d</b> means half an hour (30 minutes) after %d o'clock. Write <b>%s</b>." % (h, h, tm(h, 30))))
    for h in [5, 11]:
        its.append(mcq("How do you say <b>%s</b>?" % tm(h, 30), "half past %d" % h,
                       ["half past %d" % nxt(h), "%d o'clock" % h, "%d o'clock" % nxt(h)],
                       "%s is 30 minutes after %d o'clock. You say <b>half past %d</b>." % (tm(h, 30), h, h)))
    for h in [9, 4]:
        its.append(mcq(fig(clock_svg(h, 30)) + "Which words tell the time?", "half past %d" % h,
                       ["half past %d" % nxt(h), "%d o'clock" % h, "6 o'clock" if h != 6 else "half past 6"],
                       "The long hand is on the 6, so it is half past. The short hand is between %d and %d. "
                       "It has passed the %d, so it is <b>half past %d</b>." % (h, nxt(h), h, h)))
    its.append(mcq("At every half past time, where does the long hand point?", "on the 6",
                   ["on the 12", "on the 3", "on the 30"],
                   "Half past means half of the way around the clock. The long hand points straight down to the <b>6</b>."))
    its.append(mcq("How many minutes are in <b>half an hour</b>?", mins(30), [mins(60), mins(50), mins(6)],
                   "1 hour is 60 minutes. Half of 60 is <b>30 minutes</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Time to the half hour", "items": its}


# ============================================================ A-D clock pictures
def four_clocks(h, m, p, rnd):
    """Clock times for A-D: the right one at position p and 3 real mistakes."""
    if m == 0:
        wrong = [(12, 5 * h), (nxt(h), 0), (h, 30)]               # hands switched / next hour / half past
        swap = (12, 5 * h)
    else:
        wrong = [(nxt(h), 30), (h, 0)]
        swap = (6, 5 * h) if h != 6 else None
        wrong.append(swap if swap else (prv(h), 30))
    rnd.shuffle(wrong)
    times = wrong[:p] + [(h, m)] + wrong[p:]
    assert len(set(times)) == 4
    L = "ABCD"[p]
    if m == 0:
        e = "Clock %s has the short hand on the %d and the long hand on the 12. It shows %s." % (L, h, tm(h, 0))
    else:
        e = ("Clock %s has the long hand on the 6 and the short hand halfway between %d and %d. It shows %s."
             % (L, h, nxt(h), tm(h, 30)))
    if swap in times:
        e += " Clock %s has the hands switched: the long hand is on the %d." % ("ABCD"[times.index(swap)], h)
    if (nxt(h), 30) in times:
        e += " Clock %s shows %s." % ("ABCD"[times.index((nxt(h), 30))], tm(nxt(h), 30))
    return times, e


def clocks_item(top, h, m, p, rnd):
    times, e = four_clocks(h, m, p, rnd)
    return {"q": top + fig(clocks4_svg(times)), "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True}


# ============================================================ set 3: match analog and digital
def set_match(rnd):
    its = []
    picks = [(3, 0), (7, 30), (10, 0), (1, 30), (6, 0), (4, 30), (9, 0), (11, 30), (2, 0), (8, 30)]
    pos = [0, 1, 2, 3, 2, 0, 3, 1, 1, 2]
    for (h, m), p in zip(picks, pos):
        top = "A digital clock shows <b>%s</b>. Which clock shows the same time?" % tm(h, m)
        its.append(clocks_item(top, h, m, p, rnd))
    for h, m in [(5, 30), (1, 0), (6, 30), (8, 0), (10, 30)]:
        right = tm(h, m)
        if m == 30:
            c = ["%d:03" % h, "30:%d" % h, tm(nxt(h), 30)]
            e = ("The clock shows half past %d. A digital clock shows the hour, then a colon, then the minutes. "
                 "Half past is 30 minutes, so write <b>%s</b>. (Not %d:03 and not 30:%d.)" % (h, right, h, h))
        else:
            c = ["%d:12" % h, "%d:0" % h, tm(nxt(h), 0)]
            e = ("The clock shows %d o'clock. The minutes are 0, and a digital clock writes them with two digits: "
                 "<b>%s</b>." % (h, right))
        its.append(mcq(fig(clock_svg(h, m)) + "What does a digital clock show at this time?", right, c, e))
    for h, m in [(3, 30), (7, 0), (12, 30), (5, 0), (9, 30)]:
        t = tm(h, m)
        if m == 30:
            right = "half past %d" % h
            c = ["half past %d" % nxt(h), "%d o'clock" % h, "%d o'clock" % nxt(h)]
            e = "The minutes are :30. 30 minutes after %d o'clock is <b>half past %d</b>." % (h, h)
        else:
            right = "%d o'clock" % h
            c = ["half past %d" % h, "%d o'clock" % nxt(h), "%d o'clock" % prv(h)]
            e = "The minutes are :00, so it is right on the hour: <b>%d o'clock</b>." % h
        its.append(mcq(fig(digital_svg(t)) + "Which words tell this time?", right, c, e))
    assert len(its) == 20, len(its)
    return {"title": "Match clocks with hands and digital clocks", "items": its}


# ============================================================ set 4: the hands
def set_hands(rnd):
    its = []
    for h in [4, 10, 1]:
        its.append(mcq("At <b>%s</b>, where does the long hand point?" % tm(h, 30), "on the 6",
                       ["on the 3", "on the 12", "on the %d" % h],
                       "At half past, the long hand is half of the way around the clock. It points to the <b>6</b>."))
    for h in [5, 9, 2]:
        its.append(mcq("At <b>%s</b>, where does the long hand point?" % tm(h, 0), "on the 12",
                       ["on the %d" % h, "on the 6", "on the 1"],
                       "At %d o'clock the long hand points to the <b>12</b>. The short hand points to the %d." % (h, h)))
    for h in [3, 8, 11]:
        its.append(mcq("At <b>%s</b>, where is the short hand?" % tm(h, 30), "between %d and %d" % (h, nxt(h)),
                       ["on the %d" % h, "on the %d" % nxt(h), "between %d and %d" % (prv(h), h)],
                       "The short hand moves slowly. In half an hour it goes halfway to the next number. "
                       "At %s it is halfway <b>between %d and %d</b>." % (tm(h, 30), h, nxt(h))))
    for h in [6, 12, 7]:
        its.append(mcq("At <b>%s</b>, where is the short hand?" % tm(h, 0), "on the %d" % h,
                       ["between %d and %d" % (h, nxt(h)), "on the %d" % nxt(h), "on the 12" if h != 12 else "on the 6"],
                       "At %d o'clock the short hand points right <b>on the %d</b>." % (h, h)))
    its.append(mcq("The short hand is on the 6. The long hand is on the 12. What time is it?", "6:00",
                   ["12:30", "12:06", "6:12"],
                   "The short hand tells the hour: <b>6</b>. The long hand on the 12 means 0 minutes. It is <b>6:00</b>. "
                   "(12:30 has the hands switched.)"))
    its.append(mcq("The short hand is between 12 and 1. The long hand is on the 6. What time is it?", "12:30",
                   ["6:00", "1:30", "12:06"],
                   "The long hand on the 6 means half past. The short hand has passed the 12 but not the 1, so the hour is 12. "
                   "It is <b>12:30</b>. (6:00 has the hands switched.)"))
    its.append(mcq("The short hand is between 9 and 10. The long hand is on the 6. What time is it?", "9:30",
                   ["10:30", "9:06", "6:09"],
                   "Use the number the short hand has <b>passed</b>: 9. The long hand on the 6 means 30 minutes. It is <b>9:30</b>."))
    its.append(mcq("The short hand is on the 2. The long hand is on the 12. What time is it?", "2:00",
                   ["12:02", "2:12", "12:10"],
                   "The short hand tells the hour: <b>2</b>. The long hand on the 12 means 0 minutes. It is <b>2:00</b>."))
    # A-D pictures from words (hardest)
    for (h, m), p in zip([(7, 30), (5, 0), (2, 30), (4, 0)], [3, 0, 2, 1]):
        w = "half past %d" % h if m else "%d o'clock" % h
        its.append(clocks_item("Which clock shows <b>%s</b>?" % w, h, m, p, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Where do the hands point?", "items": its}


# ============================================================ set 5: daily life
def set_life(rnd, P):
    its = []
    acts = [("{n} wakes up in the morning. What time is it?", 7, 0),
            ("{n} gets on the school bus. What time is it?", 7, 30),
            ("School starts. What time is it?", 8, 0),
            ("{n} eats lunch at school. What time is it?", 11, 30),
            ("{n} gets home from school. What time is it?", 3, 30),
            ("{n} goes to bed at night. What time is it?", 8, 30)]
    for q, h, m in acts:
        n, he, his = P.next()
        its.append(read_q(h, m, q.format(n=n)))
    when = [("{n} eats breakfast. When could it be?", "7:00 in the morning",
             ["7:00 at night", "11:00 at night", "3:00 in the afternoon"],
             "We eat breakfast in the <b>morning</b>, before school: 7:00 in the morning."),
            ("School starts. When could it be?", "8:30 in the morning",
             ["8:30 at night", "10:30 at night", "5:30 in the afternoon"],
             "School starts in the <b>morning</b>: 8:30 in the morning. At night we are asleep."),
            ("{n} eats dinner with {his} family. When could it be?", "6:00 in the evening",
             ["6:00 in the morning", "9:00 in the morning", "11:00 in the morning"],
             "Dinner is in the <b>evening</b>: 6:00 in the evening. 6:00 in the morning is time for breakfast."),
            ("{n} goes to bed. When could it be?", "8:00 at night",
             ["8:00 in the morning", "10:00 in the morning", "1:00 in the afternoon"],
             "We go to bed at <b>night</b>: 8:00 at night. 8:00 in the morning is time for school.")]
    for q, a, w, e in when:
        n, he, his = P.next()
        its.append(mcq(q.format(n=n, his=his), a, w, e))
    its.append(mcq("It is <b>3:00</b>. What time will it be in <b>1 hour</b>?", "4:00", ["3:01", "2:00", "3:30"],
                   "In 1 hour the short hand moves to the next number. 3:00 → <b>4:00</b>. (3:01 is only 1 minute later.)"))
    its.append(mcq("It is <b>9:00</b>. What time will it be in <b>half an hour</b>?", "9:30", ["10:00", "10:30", "8:30"],
                   "Half an hour is 30 minutes. The long hand moves from the 12 to the 6. 9:00 → <b>9:30</b>. "
                   "(10:00 is 1 hour later.)"))
    its.append(mcq("It is <b>2:30</b>. What time will it be in <b>1 hour</b>?", "3:30", ["2:31", "3:00", "1:30"],
                   "In 1 hour the hour goes up by 1. The minutes stay the same. 2:30 → <b>3:30</b>."))
    its.append(mcq(fig(clock_svg(10, 0)) + "What time will it be in <b>1 hour</b>?", "11:00", ["10:30", "9:00", "10:01"],
                   "The clock shows 10:00. In 1 hour the short hand moves to the 11. It will be <b>11:00</b>."))
    its.append(mcq(fig(clock_svg(5, 30)) + "What time will it be in <b>half an hour</b>?", "6:00", ["6:30", "5:00", "4:30"],
                   "The clock shows 5:30. In half an hour the long hand goes from the 6 up to the 12, "
                   "and a new hour starts. It will be <b>6:00</b>. (6:30 is 1 hour later.)"))
    its.append(mcq(fig(clock_svg(1, 30)) + "What time will it be in <b>half an hour</b>?", "2:00", ["2:30", "1:00", "12:30"],
                   "The clock shows 1:30. 30 more minutes takes the long hand back up to the 12. It will be <b>2:00</b>."))
    n, he, his = P.next()
    its.append(mcq("%s's soccer game starts at 4:00. It lasts 1 hour. When does it end?" % n, "5:00", ["4:01", "3:00", "4:30"],
                   "1 hour after 4:00 is <b>5:00</b>."))
    n, he, his = P.next()
    its.append(mcq("%s reads a book from 7:00 to 7:30. How long does %s read?" % (n, he), "half an hour",
                   ["1 hour", "7 minutes", "30 hours"],
                   "From 7:00 to 7:30 the long hand goes from the 12 to the 6. That is 30 minutes, <b>half an hour</b>."))
    n, he, his = P.next()
    its.append(mcq("%s watches a movie. It starts at 6:30. It is 1 hour long. When does it end?" % n, "7:30",
                   ["6:31", "7:00", "5:30"],
                   "1 hour after 6:30 is <b>7:30</b>. The minutes stay the same. (7:00 is only half an hour later.)"))
    n, he, his = P.next()
    its.append(mcq("%s's bedtime is 8:30. It is 8:00 now. How long until bedtime?" % n, "half an hour",
                   ["1 hour", "8 minutes", "2 hours"],
                   "From 8:00 to 8:30 is 30 minutes. That is <b>half an hour</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Time in daily life", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The big idea</h2>"
        "<p>A clock has two hands. The <b>short hand</b> is the hour hand. The <b>long hand</b> is the minute hand. "
        "Look at the short hand first. Then look at the long hand.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 0, size=220) +
        "<figcaption>The short hand (black) is on the 3. The long hand (red) is on the 12. It is 3 o'clock: 3:00.</figcaption></figure>"
        "<ol class='rk-step'>"
        "<li><b>Long hand on the 12:</b> it is an o'clock time. Write :00.</li>"
        "<li><b>Long hand on the 6:</b> it is half past. Write :30.</li>"
        "<li><b>Short hand:</b> it tells the hour. If it is between two numbers, use the number it has <b>passed</b>.</li></ol>"
        "<h2>Half past</h2>"
        "<p>Half past means 30 minutes after the hour. The long hand has gone half of the way around. "
        "The short hand has moved halfway to the next number.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 30, size=220) +
        "<figcaption>The long hand is on the 6. The short hand is halfway between 3 and 4. It is half past 3: 3:30.</figcaption></figure>"
        "<figure class='sn-fig'>" + digital_svg("3:30") +
        "<figcaption>A digital clock shows the same time with numbers: 3:30.</figcaption></figure>"
        + table(["Words", "Digital", "Long hand", "Short hand"], [
            ["3 o'clock", "3:00", "on the 12", "on the 3"],
            ["half past 3", "3:30", "on the 6", "between 3 and 4"],
            ["4 o'clock", "4:00", "on the 12", "on the 4"],
        ])
        + ex("Example 1", "The short hand is on the 9. The long hand is on the 12. What time is it?",
             "The long hand on the 12 means o'clock. The short hand tells the hour: 9.", "9:00, 9 o'clock")
        + ex("Example 2", "The short hand is between 6 and 7. The long hand is on the 6. What time is it?",
             "The long hand on the 6 means half past. The short hand has passed the 6, so the hour is 6.", "6:30, half past 6")
        + ex("Example 3", "It is 4:30. What time will it be in half an hour?",
             "The long hand moves from the 6 up to the 12. A new hour starts.", "5:00")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Reading half past 3 as 4:30 because the short hand is near the 4", "Use the number the short hand has passed: 3:30"],
            ["Switching the hands (reading 6:00 as 12:30)", "Short hand = hour. Long hand = minutes"],
            ["Writing half past 3 as 3:03 or 30:3", "Hour first, then a colon, then 30: 3:30"],
            ["Reading the long hand on the 6 as 6 minutes", "Long hand on the 6 means 30 minutes"],
        ])
    )


FAQ = [
    {"q": "What time should a 1st grader be able to tell?",
     "a": "In Grade 1, children tell and write time to the hour and half hour on clocks with hands and on digital clocks, like 7:00 and 7:30. "
          "Telling time to 5 minutes comes in Grade 2."},
    {"q": "What does half past mean?",
     "a": "Half past means 30 minutes after the hour. Half past 3 is 3:30, and the long hand points to the 6."},
    {"q": "Why is the hour hand between two numbers at half past?",
     "a": "The hour hand moves slowly all hour. At 3:30 it is halfway from the 3 to the 4, so the hour is still 3."},
    {"q": "How do I teach my child to tell time to the hour?",
     "a": "Start with the long hand on the 12 and say o'clock times out loud during the day, like 7 o'clock for breakfast. "
          "Then show that the short hand points to the hour."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D clock choices) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(110)
    P = People(rnd)
    sets = [set_hour(rnd), set_half(rnd), set_match(rnd), set_hands(rnd), set_life(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            # every clock picture in a question (outside A-D grids) is on :00 or :30
            for hh, mm in re.findall(r"aria-label='(?:digital )?clock showing (\d+):(\d+)'", it["q"]):
                assert mm in ("00", "30"), it["q"][-80:]
            assert "aria-label='clock showing 12:00'" not in it["q"]
            # the right answer, if it is a time, is :00 or :30
            for hh, mm in re.findall(r"\b(\d{1,2}):(\d\d)\b", it["c"][it["a"]]):
                assert mm in ("00", "30") and 1 <= int(hh) <= 12
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "telling-time-hour-half-hour", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Telling Time to the Hour and Half Hour",
        "seo_title": "Grade 1 Telling Time Worksheets: Hour and Half Hour (O'Clock and Half Past)",
        "short_title": "Telling time (hour, half hour)",
        "domain": "Measurement and Data",
        "standard_code": "1.MD.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/MD/B/3/",
        "standard_text": "Tell and write time in hours and half-hours using analog and digital clocks.",
        "meta_desc": "Free Grade 1 telling time worksheets with clock pictures: o'clock and half past, matching clocks with hands "
                     "to digital clocks, where the hands point, and times in daily life. 100 practice questions with an answer key for 1st grade.",
        "key_big": "Long hand on the 12 = o'clock (:00). Long hand on the 6 = half past (:30).",
        "key_sub": "The short hand tells the hour. At half past it is halfway between two numbers: use the number it has passed, "
                   "so half past 3 is 3:30, not 4:30.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "four clocks labeled A to D")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
