# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Telling the Time (Australian Curriculum v9.0, AC9M3M04 and AC9M3M03)
  python3 tools/gen_au_maths_y3_time.py
Every analog clock is drawn from the time itself (the hour hand moves between the numbers).
Every answer is worked out in code. Wrong answers come from real student mistakes:
hour hand read as the next hour ("25 to 9" -> 9:35), the number the minute hand points to read as
minutes, past and to mixed up, am and pm swapped, an hour counted as 100 minutes, small marks miscounted.
HTML attributes use single quotes (no backslashes in the JSON). Australian English ("analog", "program").
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Charlotte", "she"), ("Oliver", "he"), ("Isla", "she"), ("Jack", "he"), ("Mia", "she"), ("Noah", "he"),
          ("Amelia", "she"), ("William", "he"), ("Ava", "she"), ("Leo", "he"), ("Harper", "she"), ("Lachlan", "he"),
          ("Chloe", "she"), ("Liam", "he"), ("Ruby", "she"), ("Aarav", "he"), ("Mei", "she"), ("Kai", "he"),
          ("Zara", "she"), ("Cooper", "he"), ("Matilda", "she"), ("Ethan", "he"), ("Sienna", "she"), ("Grace", "she")]


# ------------------------------------------------------------ time formats
def h12(h24):
    return (h24 - 1) % 12 + 1


def tm12(h24, m):
    """12-hour digital: 3:45 pm"""
    h24 %= 24
    return "%d:%02d %s" % (h12(h24), m, "am" if h24 < 12 else "pm")


def dig(h, m):
    """digital without am/pm: 3:45"""
    return "%d:%02d" % (h12(h), m)


def words(h, m):
    """clock words: 20 past 7, 25 to 4, quarter to 9, 13 minutes past 6"""
    h = h12(h)
    nx = h % 12 + 1
    if m == 0:
        return "%d o’clock" % h
    if m == 15:
        return "quarter past %d" % h
    if m == 30:
        return "half past %d" % h
    if m == 45:
        return "quarter to %d" % nx
    if m < 30:
        n, word, hr = m, "past", h
    else:
        n, word, hr = 60 - m, "to", nx
    if n % 5 == 0:
        return "%d %s %d" % (n, word, hr)
    return "%d minute%s %s %d" % (n, "" if n == 1 else "s", word, hr)


def mins(n):
    assert n > 0
    return "%d minute%s" % (n, "" if n == 1 else "s")


def dur(n):
    assert n > 0
    hh, mm = divmod(n, 60)
    parts = []
    if hh:
        parts.append("%d hour%s" % (hh, "" if hh == 1 else "s"))
    if mm:
        parts.append(mins(mm))
    return " ".join(parts)


def dur_value(s):
    v = 0
    for n, unit in re.findall(r"(\d+) (hour|minute)", s):
        v += int(n) * (60 if unit == "hour" else 1)
    return v


def add(h, m, d):
    t = (h * 60 + m + d) % (24 * 60)
    return t // 60, t % 60


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, key=None):
    key = key or (lambda x: x)
    seen = {key(correct)}
    pick = []
    for c in cands:
        if not c or key(c) in seen:
            continue
        seen.add(key(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def clock_body(h, m, size, ox=0.0, oy=0.0):
    """Analog clock face. The hour hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) >= 12, (h, m)
    R = size / 2.0 - 6
    cx, cy = ox + size / 2.0, oy + size / 2.0
    k = R / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, R, GREEN, 5 * k)]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (12 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (R - 3 * k) * math.cos(a), cy + (R - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), LINE, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), LINE, 2.6 * k))
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.48 * math.cos(ah), cy + R * 0.48 * math.sin(ah), LINE, 8 * k))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.82 * math.cos(am), cy + R * 0.82 * math.sin(am), RED, 4.5 * k))
    fs = max(19 * k, 15)
    rn = R - 29 * k
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' paint-order='stroke'>" % (fs, LINE, 3.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200):
    return svg_wrap(size, size, clock_body(h, m, size), "analog clock")


def four_clocks_svg(times, size=170):
    """Clocks A, B, C, D in one row (one SVG per question)."""
    gap, top = 14, 30
    W = 4 * size + 3 * gap
    s = []
    for i, (h, m) in enumerate(times):
        x = i * (size + gap)
        s.append("<text x='%.1f' y='22' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + size / 2.0, GREEN, "ABCD"[i]))
        s.append(clock_body(h, m, size, x, top))
    return svg_wrap(W, size + top, "".join(s), "four analog clocks")


def digital_svg(text):
    W, H = 200, 84
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='#fff' stroke='%s' stroke-width='4'/>" % (W - 6, H - 6, GREEN),
         "<rect x='16' y='14' width='%d' height='%d' rx='6' fill='#eef5f0'/>" % (W - 32, H - 28),
         "<text x='%d' y='%d' font-size='40' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Consolas, Menlo, monospace'>%s</text>" % (W / 2, H / 2 + 14, LINE, text)]
    return svg_wrap(W, H, "".join(s), "digital clock")


def timeline_svg(h1, m1, h2, m2, W=420):
    """Start -> next o'clock -> end, the jumps labelled."""
    t1, t2 = h1 * 60 + m1, h2 * 60 + m2
    mid = (h1 + 1) * 60 if m1 else None
    L, R, Y = 40, W - 40, 70

    def X(t):
        return L + (R - L) * (t - t1) / float(t2 - t1)
    pts = [t1] + ([mid] if mid and t1 < mid < t2 else []) + [t2]
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for t in pts:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X(t), Y - 10, X(t), Y + 10, LINE))
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X(t), Y + 32, LINE, tm12(t // 60, t % 60)))
    for a, b in zip(pts, pts[1:]):
        x1, x2 = X(a), X(b)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, Y - 12, (x1 + x2) / 2, Y - 52, x2, Y - 12, RED))
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>+%d min</text>"
                 % ((x1 + x2) / 2, Y - 40, RED, b - a))
    return svg_wrap(W, 112, "".join(s), "time line")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def hand_text(h, m):
    """How to read the two hands (for explanations)."""
    h = h12(h)
    n, extra = divmod(m, 5)
    if m == 0:
        mm = "The long minute hand points to <b>12</b>, so it is exactly on the hour."
    elif extra == 0:
        mm = "The long minute hand points to <b>%d</b>. Count in 5s: %d × 5 = <b>%d minutes</b> past." % (n, n, m)
    elif n == 0:
        mm = "The long minute hand is <b>%d small mark%s</b> past the 12: <b>%s</b> past." % (extra, "" if extra == 1 else "s", mins(m))
    else:
        mm = ("The long minute hand is %d small mark%s past the %d. Count in 5s to %d, then on in 1s: <b>%d minutes</b> past."
              % (extra, "" if extra == 1 else "s", n, n * 5, m))
    if m == 0:
        hh = "The short hour hand points to <b>%d</b>." % h
    else:
        hh = ("The short hour hand is between <b>%d</b> and <b>%d</b>, so the hour is still <b>%d</b>."
              % (h, h % 12 + 1, h))
    return hh + " " + mm


def pick_hour(rnd, m, used):
    hrs = list(range(1, 13))
    rnd.shuffle(hrs)
    for h in hrs:
        if (h, m) in used or hands_gap(h, m) < 15:
            continue
        used.add((h, m))
        return h
    raise AssertionError(m)


# ============================================================ set 1: o'clock, half, quarter, then 5 minutes
def set_quarters(rnd):
    its = []
    used = set()
    plan = [0, 0, 30, 30, 0, 30, 15, 15, 30, 15, 45, 45, 10, 20, 40, 55, 25, 50, 35, 5]
    for m in plan:
        h = pick_hour(rnd, m, used)
        right = words(h, m)
        n = m // 5
        if m == 0:
            c = [words(12, 5 * h) if h != 12 else None, words(h, 30), words(h + 1, 0), words(h - 1, 0)]
            e = ("%s It is <b>%s</b>. (The long hand tells the minutes, so do not read the short hand as minutes.)"
                 % (hand_text(h, m), right))
        elif m == 30:
            c = [words(h + 1, 30), "6 o’clock" if h != 6 else "12 o’clock", words(h, 15), words(h - 1, 30)]
            e = ("%s Half past means 30 minutes past. The hour hand has not reached %d yet, so it is <b>%s</b>, not half past %d."
                 % (hand_text(h, m), h12(h + 1), right, h12(h + 1)))
        elif m == 15:
            c = [words(h, 45), words(h, 3), words(h + 1, 45), words(h - 1, 15)]
            e = ("%s 15 minutes is a quarter of an hour, and the minute hand is on the right-hand side, so we say <b>past</b>. "
                 "It is <b>%s</b>." % (hand_text(h, m), right))
        elif m == 45:
            c = [words(h - 1, 45), words(h + 1, 15), words(h, 9), words(h, 15)]
            e = ("%s 45 minutes past %d is 15 minutes before %d o’clock. The minute hand is on the left-hand side, so we say "
                 "<b>to</b> the next hour: <b>%s</b>." % (hand_text(h, m), h12(h), h12(h + 1), right))
        elif m < 30:
            c = [words(h + 1, m), words(h, n), words(h - 1, 60 - m), words(h, 60 - m), words(h, m + 5)]
            e = ("%s The minute hand is on the right-hand side, so we say <b>past %d</b>. It is <b>%s</b>."
                 % (hand_text(h, m), h12(h), right))
        else:
            c = [words(h - 1, m), words(h, n), words(h + 1, 60 - m), words(h, 60 - m), words(h, m - 5)]
            e = ("%s That is %d minutes before %d o’clock (60 − %d = %d). The minute hand is on the left-hand side, so we say "
                 "<b>to %d</b>. It is <b>%s</b>." % (hand_text(h, m), 60 - m, h12(h + 1), m, 60 - m, h12(h + 1), right))
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the analog clock show?", right, c, e))
    return {"title": "O’clock, half past, quarter past, quarter to and 5 minutes", "items": its}


# ============================================================ set 2: to the nearest minute
def set_minute(rnd):
    its = []
    used = set()

    def pick(lo, hi):
        while True:
            h = rnd.randint(1, 12)
            m = rnd.randint(lo, hi)
            if m % 5 and (h, m) not in used and hands_gap(h, m) >= 18 and h not in [x[0] for x in used][-2:]:
                used.add((h, m))
                return h, m

    # clock -> digital (no am/pm)
    for lo, hi in [(1, 14), (16, 29), (31, 44), (46, 59), (16, 29), (31, 44), (1, 14), (46, 59), (31, 44), (46, 59)]:
        h, m = pick(lo, hi)
        n = m // 5
        right = dig(h, m)
        c = []
        if m >= 30:
            c.append(dig(h + 1, m))                       # hour hand read as the next hour
        if n:
            c.append(dig(h, n))                           # number the minute hand points to read as minutes
        c += [dig(h, 60 - m), dig(h, m + 1 if m % 5 != 4 else m - 1), dig(h - 1, m), dig(h + 1, m)]
        e = "%s So the digital time is <b>%s</b>." % (hand_text(h, m), right)
        if m >= 30:
            e += " (Not %s: the hour hand has not reached %d yet.)" % (dig(h + 1, m), h12(h + 1))
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show? Choose the digital time.", right, c, e))
    # clock -> words to the minute
    for lo, hi in [(6, 24), (36, 54), (36, 54), (6, 24), (36, 54), (6, 24)]:
        h, m = pick(lo, hi)
        right = words(h, m)
        if m < 30:
            c = [words(h + 1, m), "%s to %d" % (mins(m), h12(h + 1)), "%s past %d" % (mins(60 - m), h12(h)),
                 words(h, m + 1 if m % 5 != 4 else m - 1)]
            e = ("%s The minute hand is on the right-hand side, so say <b>past</b>: <b>%s</b>." % (hand_text(h, m), right))
        else:
            c = [words(h - 1, m), "%s to %d" % (mins(60 - m), h12(h)), "%s past %d" % (mins(60 - m), h12(h)),
                 "%s to %d" % (mins(m), h12(h + 1))]
            e = ("%s That is %d minutes past %d. It is after half past, so count the minutes <b>to</b> %d: "
                 "60 − %d = %d. It is <b>%s</b>." % (hand_text(h, m), m, h12(h), h12(h + 1), m, 60 - m, right))
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show? Choose the time in words.", right, c, e))
    # digital -> words
    for h, m in [(7, 48), (2, 13), (10, 51), (5, 37)]:
        right = words(h, m)
        if m > 30:
            c = [words(h - 1, m), "%s to %d" % (mins(m), h12(h + 1)), "%s past %d" % (mins(60 - m), h12(h)),
                 "%s to %d" % (mins(60 - m), h12(h))]
            e = ("%s is %d minutes past %d. That is after half past, so say <b>to</b> the next hour. "
                 "60 − %d = %d minutes to %d: <b>%s</b>." % (dig(h, m), m, h12(h), m, 60 - m, h12(h + 1), right))
        else:
            c = [words(h + 1, m), "%s to %d" % (mins(m), h12(h + 1)), "%s to %d" % (mins(m), h12(h)),
                 words(h, m + 1)]
            e = "%s is %d minutes after %d o’clock. It is before half past, so say <b>past</b>: <b>%s</b>." % (dig(h, m), m, h12(h), right)
        its.append(mcq(fig(digital_svg(dig(h, m))) + "How do we say this digital time in words?", right, c, e))
    order = [0, 1, 2, 3, 10, 4, 5, 11, 16, 6, 12, 7, 17, 8, 13, 18, 9, 14, 19, 15]
    assert sorted(order) == list(range(20))
    return {"title": "Reading the time to the nearest minute", "items": [its[i] for i in order]}


# ============================================================ set 3: analog and digital, am and pm
CONTEXTS = [
    ("{n} wakes up in the morning.", 7, 2, 28),
    ("{n} walks to school in the morning.", 8, 31, 44),
    ("{n} eats lunch at school.", 13, 2, 24),
    ("{n} walks home from school in the afternoon.", 15, 16, 28),
    ("{n} has dinner in the evening.", 18, 6, 26),
    ("{n} goes to bed in the evening.", 19, 36, 54),
]


def which_clock(h, m, others, pos):
    """A, B, C, D clocks; the right one at position pos. The others are real mistakes."""
    times = list(others)
    times.insert(pos, (h, m))
    return times


def set_ampm(rnd, people):
    its = []
    its.append(mcq("Which times are <b>am</b> times?", "from midnight to midday",
                   ["from midday to midnight", "only times at night", "only times after school"],
                   "<b>am</b> times go from midnight to midday (night and morning). <b>pm</b> times go from midday to "
                   "midnight (afternoon and evening)."))
    its.append(mcq("What does <b>midnight</b> mean?", "12 o’clock at night",
                   ["12 o’clock in the middle of the day", "9 o’clock at night", "the end of the afternoon"],
                   "<b>Midnight</b> is 12 o’clock at night, when one day ends and the next day starts. "
                   "12 o’clock in the middle of the day is <b>midday</b> (also called noon)."))
    its.append(mcq("Which time is in the <b>afternoon</b>?", "2:30 pm", ["2:30 am", "11:30 am", "9:15 am"],
                   "The afternoon is after midday, so it is a <b>pm</b> time. 2:30 am is in the middle of the night. "
                   "So the answer is <b>2:30 pm</b>."))
    its.append(mcq("Which is a sensible time for school to start?", "8:50 am", ["8:50 pm", "3:50 am", "11:50 pm"],
                   "School starts in the morning, so it is an <b>am</b> time. 3:50 am is the middle of the night. "
                   "So the answer is <b>8:50 am</b>."))
    # how the hands are related
    its.append(mcq("The long minute hand goes <b>all the way around</b> the clock once. How much time has passed?", "1 hour",
                   ["1 minute", "12 hours", "5 minutes"],
                   "The minute hand passes all 60 small marks, one for each minute. 60 minutes = <b>1 hour</b>. "
                   "In that time the short hour hand moves from one number to the next."))
    assert 60 - 37 == 23
    its.append(mcq("A digital clock shows <b>4:37</b>. How many minutes is it until 5 o’clock?", "23 minutes",
                   ["37 minutes", "63 minutes", "13 minutes"],
                   "An hour has 60 minutes. It is 37 minutes past 4. 60 − 37 = <b>23 minutes</b> to 5 o’clock. "
                   "(Not 63: an hour is 60 minutes, not 100.)"))
    # clocks to the minute with a time of day -> 12-hour digital with am / pm
    ctx = CONTEXTS[:]
    rnd.shuffle(ctx)
    for sent, H, lo, hi in ctx:
        ms = [x for x in range(lo, hi + 1) if x % 5 and hands_gap(H, x) >= 15]
        m = rnd.choice(ms)
        n = m // 5
        nm, pr = next(people)
        right = tm12(H, m)
        c = [tm12(H + 12, m)]                             # am and pm swapped
        if m >= 35:
            c.append(tm12(H + 1, m))                      # hour hand read as the next hour
        if n:
            c.append(tm12(H, n))                          # minute number read as minutes
        c += [tm12(H + 1, m), tm12(H, 60 - m), tm12(H, m + 5 if m < 55 else m - 5)]
        why = "It is the morning, so it is <b>am</b>." if H < 12 else "It is after midday, so it is <b>pm</b>."
        e = "%s %s So it is <b>%s</b>." % (hand_text(H, m), why, right)
        q = fig(clock_svg(H, m)) + sent.format(n=nm) + " What is the time?"
        its.append(mcq(q, right, c, e))
    # which analog clock matches the digital time (pictures A to D, answer position fixed here)
    pos = [0, 1, 2, 3]
    rnd.shuffle(pos)
    for (h, m), p in zip([(3, 37), (10, 12), (6, 52), (7, 26)], pos):
        others = [(h + 1, m), (h, 60 - m), (h, m // 5)]
        times = which_clock(h, m, others, p)
        assert len(set(times)) == 4
        L = "ABCD"
        wrong = "; ".join("clock %s shows %s" % (L[times.index(t)], dig(*t)) for t in others)
        e = ("At %s the long hand is %d small mark%s past the %d (count in 5s to %d, then on in 1s to %d), and the short hand "
             "is between %d and %d. That is clock <b>%s</b>. (%s.)"
             % (dig(h, m), m % 5, "" if m % 5 == 1 else "s", m // 5, m // 5 * 5, m, h, h % 12 + 1, L[p], wrong[0].upper() + wrong[1:]))
        it = {"q": fig(four_clocks_svg(times)) + "Which analog clock shows <b>%s</b>?" % dig(h, m),
              "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True}
        its.append(it)
    # words -> digital with am / pm
    for H, m, part in [(8, 45, "in the morning"), (15, 35, "in the afternoon"), (19, 20, "in the evening"), (7, 50, "in the morning")]:
        w = words(H, m)
        right = tm12(H, m)
        ap = "am" if H < 12 else "pm"
        if m > 30:
            c = [tm12(H + 1, m), tm12(H + 1, 60 - m), tm12(H, 60 - m), tm12(H + 12, m)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d minutes past %d: %s. "
                 "It is %s, so it is %s: <b>%s</b>. (Not %s: that is after %d o’clock.)"
                 % (w, 60 - m, h12(H + 1), 60 - m, m, m, h12(H), dig(H, m), part, ap, right, tm12(H + 1, m), h12(H + 1)))
        else:
            c = [tm12(H - 1, 60 - m), tm12(H + 12, m), tm12(H, m // 5), tm12(H + 1, m)]
            e = ("“%s” means %d minutes <b>after</b> %d o’clock: %s. It is %s, so it is %s: <b>%s</b>."
                 % (w, m, h12(H), dig(H, m), part, ap, right))
        its.append(mcq("Write <b>%s %s</b> as a digital time." % (w, part), right, c, e))
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 4, 6, 7, 16, 12, 8, 17, 13, 9, 5, 18, 14, 10, 19, 15, 11]
    assert sorted(order) == list(range(20))
    return {"title": "Analog and digital clocks with am and pm", "items": [its[i] for i in order]}


# ============================================================ set 4: units of time
def set_units(rnd):
    its = []
    F = [("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "30"], "There are <b>60 seconds</b> in 1 minute."),
         ("How many <b>minutes</b> are in 1 hour?", "60", ["100", "24", "30"],
          "There are <b>60 minutes</b> in 1 hour. (Not 100: time does not count in hundreds.)"),
         ("How many <b>hours</b> are in 1 day?", "24", ["12", "60", "7"],
          "There are <b>24 hours</b> in 1 day: 12 am hours and 12 pm hours. 12 + 12 = 24."),
         ("How many <b>days</b> are in 1 week?", "7", ["5", "12", "10"],
          "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: <b>7 days</b>. (5 is just the school days.)"),
         ("A <b>fortnight</b> is 2 weeks. How many days is that?", "14", ["10", "2", "7"],
          "1 week = 7 days. 2 weeks = 7 + 7 = <b>14 days</b>. (10 is only the school days in 2 weeks.)"),
         ("How many <b>months</b> are in 1 year?", "12", ["10", "52", "7"],
          "January to December: <b>12 months</b>. (52 is the number of weeks.)"),
         ("How many minutes are in <b>half an hour</b>?", "30", ["50", "15", "20"],
          "1 hour = 60 minutes. Half of 60 is <b>30 minutes</b>. (Not 50: an hour is not 100 minutes.)"),
         ("How many minutes are in <b>a quarter of an hour</b>?", "15", ["25", "30", "4"],
          "1 hour = 60 minutes. A quarter of 60 is 60 ÷ 4 = <b>15 minutes</b>. (25 would be a quarter of 100.)"),
         ("<b>2 hours</b> = ? minutes", "120", ["200", "60", "24"],
          "1 hour = 60 minutes. 2 hours = 60 + 60 = <b>120 minutes</b>. (Not 200: an hour is 60 minutes, not 100.)"),
         ("<b>2 minutes</b> = ? seconds", "120", ["200", "60", "20"],
          "1 minute = 60 seconds. 2 minutes = 60 + 60 = <b>120 seconds</b>."),
         ("<b>1 minute 30 seconds</b> = ? seconds", "90", ["130", "31", "60"],
          "1 minute = 60 seconds. 60 + 30 = <b>90 seconds</b>. (Not 130: a minute is 60 seconds, not 100.)"),
         ("<b>2 days</b> = ? hours", "48", ["24", "14", "120"],
          "1 day = 24 hours. 2 days = 24 + 24 = <b>48 hours</b>."),
         ("Which is longer: <b>100 seconds</b> or <b>2 minutes</b>?", "2 minutes",
          ["100 seconds", "They are the same.", "You cannot tell."],
          "2 minutes = 60 + 60 = 120 seconds. 120 seconds is more than 100 seconds, so <b>2 minutes</b> is longer. "
          "(100 seconds is 1 minute 40 seconds.)"),
         ("Which is the <b>shortest</b> time?", "50 seconds", ["1 minute", "70 seconds", "1 hour"],
          "1 minute = 60 seconds. 50 seconds is less than 60 seconds, 70 seconds and 1 hour. So <b>50 seconds</b> is the shortest."),
         ("Which is longer: <b>1 hour</b> or <b>70 minutes</b>?", "70 minutes",
          ["1 hour", "They are the same.", "You cannot tell."],
          "1 hour = 60 minutes. 70 minutes is 10 minutes more than 60 minutes, so <b>70 minutes</b> is longer."),
         ("Put these in order from <b>shortest</b> to <b>longest</b>: 1 hour, 1 second, 1 day, 1 minute.",
          "1 second, 1 minute, 1 hour, 1 day",
          ["1 day, 1 hour, 1 minute, 1 second", "1 minute, 1 second, 1 hour, 1 day", "1 second, 1 hour, 1 minute, 1 day"],
          "1 minute = 60 seconds, 1 hour = 60 minutes and 1 day = 24 hours. So the order is "
          "<b>1 second, 1 minute, 1 hour, 1 day</b>."),
         ("Which unit would you use to time a <b>50 m race</b> at the athletics carnival?", "seconds",
          ["hours", "days", "weeks"],
          "A 50 m race is over very quickly, in less than a minute. We time it in <b>seconds</b>."),
         ("About how long does it take to brush your teeth?", "2 minutes", ["2 seconds", "2 hours", "2 days"],
          "2 seconds is far too quick, and 2 hours is far too long. Brushing your teeth takes about <b>2 minutes</b>."),
         ("About how long does a Year 3 student sleep at night?", "10 hours", ["10 minutes", "10 seconds", "10 days"],
          "Children sleep from the evening until the morning. That is about <b>10 hours</b>."),
         ("About how long is a school day?", "6 hours", ["6 minutes", "60 hours", "6 days"],
          "School starts in the morning and finishes in the afternoon. That is about <b>6 hours</b>."),
         ]
    assert 120 > 100 and 70 > 60 and 2 * 24 == 48 and 60 + 30 == 90
    for q, a, c, e in F:
        its.append(mcq(q, a, c, e))
    order = [0, 1, 2, 3, 6, 7, 4, 5, 9, 8, 10, 11, 17, 18, 16, 19, 13, 12, 14, 15]
    assert sorted(order) == list(range(20))
    return {"title": "Units of time: seconds, minutes, hours and days", "items": [its[i] for i in order]}


# ============================================================ set 5: how long? time in daily life
def set_problems(rnd, people):
    its = []

    def how_long(text, h1, m1, h2, m2, line=False):
        d = (h2 * 60 + m2) - (h1 * 60 + m1)
        assert d > 0
        q = (fig(timeline_svg(h1, m1, h2, m2)) if line else "") + text
        if h1 == h2:
            c = [mins(m2), mins(d + 10), mins(d - 5) if d > 5 else None, mins(d + 5), mins(m1 + m2) if m1 + m2 != d else None]
            e = "Both times are in the same hour. %d − %d = <b>%s</b>." % (m2, m1, mins(d))
        else:
            naive = (h12(h2) * 100 + m2) - (h12(h1) * 100 + m1)
            c = ["%d minutes" % naive if 0 < naive < 100 and naive != d else None, mins(abs(m2 - m1)) if m2 != m1 else None,
                 dur(d + 60) if d < 60 else dur(d - 60), dur(d + 10), dur(d - 5)]
            rest = d - (60 - m1)
            e = ("Count on to the next o’clock first: %s to %s is %s. Then %s to %s is %s. %d + %d = <b>%s</b>. "
                 "(An hour has 60 minutes, not 100, so do not just take away the numbers.)"
                 % (tm12(h1, m1), tm12(h1 + 1, 0), mins(60 - m1), tm12(h1 + 1, 0), tm12(h2, m2),
                    dur(rest), 60 - m1, rest, mins(d) if d < 60 else "%d minutes = %s" % (d, dur(d))))
        return mcq(q, dur(d), c, e, key=dur_value)

    its.append(how_long("A TV program starts at <b>4:10 pm</b> and ends at <b>4:35 pm</b>. How long is it?", 16, 10, 16, 35))
    nm, pr = next(people)
    its.append(how_long("%s starts reading at <b>7:05 pm</b> and stops at <b>7:45 pm</b>. How long does %s read for?"
                        % (nm, pr), 19, 5, 19, 45))
    its.append(how_long("Assembly starts at <b>9:05 am</b> and ends at <b>9:27 am</b>. How long is assembly?", 9, 5, 9, 27))
    nm, pr = next(people)
    its.append(how_long("%s’s netball game starts at <b>9:15 am</b> and ends at <b>9:50 am</b>. How long is the game?" % nm,
                        9, 15, 9, 50))
    its.append(how_long("Recess starts at <b>10:50 am</b> and ends at <b>11:20 am</b>. How long is recess?",
                        10, 50, 11, 20, line=True))
    its.append(how_long("Lunch starts at <b>12:50 pm</b> and ends at <b>1:30 pm</b>. How long is lunch?", 12, 50, 13, 30))
    nm, pr = next(people)
    its.append(how_long("%s gets on the school bus at <b>8:20 am</b>. %s gets to school at <b>8:43 am</b>. How long is the bus ride?"
                        % (nm, pr.capitalize()), 8, 20, 8, 43))
    nm, pr = next(people)
    its.append(how_long("%s’s swimming lesson is from <b>3:50 pm</b> to <b>4:35 pm</b>. How long is it?" % nm,
                        15, 50, 16, 35, line=True))
    its.append(how_long("At the school sausage sizzle, the sausages go on the barbecue at <b>11:48 am</b>. They come off at "
                        "<b>12:03 pm</b>. How long do they cook?", 11, 48, 12, 3))
    its.append(how_long("School starts at <b>8:50 am</b>. Recess starts at <b>10:50 am</b>. How long is it from the start of "
                        "school to recess?", 8, 50, 10, 50))
    its.append(how_long("A footy match starts at <b>1:45 pm</b> and ends at <b>3:50 pm</b>. How long is the match?", 13, 45, 15, 50))
    # end and start times
    assert add(18, 15, 25) == (18, 40)
    its.append(mcq("A TV program starts at <b>6:15 pm</b>. It lasts <b>25 minutes</b>. What time does it end?", "6:40 pm",
                   ["6:40 am", "7:40 pm", "6:45 pm"],
                   "Count on 25 minutes from 6:15: 15 + 25 = 40. It is still the evening, so it ends at <b>6:40 pm</b>."))
    assert add(13, 40, 50) == (14, 30)
    its.append(mcq("Sport starts at <b>1:40 pm</b>. It lasts <b>50 minutes</b>. What time does it finish?", "2:30 pm",
                   ["2:40 pm", "2:30 am", "2:10 pm"],
                   "From 1:40 pm, 20 minutes takes you to 2:00 pm. 50 − 20 = 30 more minutes makes <b>2:30 pm</b>. "
                   "(2:40 pm would be 1 hour later, not 50 minutes.)"))
    nm, pr = next(people)
    assert add(19, 30, -20) == (19, 10)
    its.append(mcq("%s goes to bed at <b>7:30 pm</b>. %s has a shower <b>20 minutes</b> before bed. What time does the shower start?"
                   % (nm, pr.capitalize()), "7:10 pm", ["7:50 pm", "7:10 am", "7:20 pm"],
                   "Count <b>back</b> 20 minutes from 7:30: 30 − 20 = 10. The shower starts at <b>7:10 pm</b>. "
                   "(7:50 pm is 20 minutes <b>after</b> bedtime.)"))
    assert add(9, 20, 85) == (10, 45)
    its.append(mcq("The bus for the school excursion leaves at <b>9:20 am</b>. The trip takes <b>1 hour 25 minutes</b>. "
                   "What time does the bus arrive?", "10:45 am", ["10:45 pm", "9:45 am", "11:05 am"],
                   "Add 1 hour: 9:20 am → 10:20 am. Then add 25 minutes: 20 + 25 = 45. The bus arrives at <b>10:45 am</b>."))
    assert (15 * 60 + 10) - (8 * 60 + 50) == 380
    its.append(mcq("School starts at <b>8:50 am</b> and finishes at <b>3:10 pm</b>. How long is the school day?",
                   "6 hours 20 minutes", ["5 hours 20 minutes", "7 hours 20 minutes", "6 hours 40 minutes"],
                   "8:50 am to 2:50 pm is 6 hours. 2:50 pm to 3:10 pm is 20 minutes. So the school day is "
                   "<b>6 hours 20 minutes</b>.", key=dur_value))
    # compare durations
    a, b = next(people), next(people)
    its.append(mcq("%s’s movie lasts <b>1 hour 30 minutes</b>. %s’s movie lasts <b>95 minutes</b>. Whose movie is longer, and by how much?"
                   % (a[0], b[0]), "%s’s, by 5 minutes" % b[0],
                   ["%s’s, by 5 minutes" % a[0], "%s’s, by 35 minutes" % a[0], "%s’s, by 65 minutes" % b[0]],
                   "1 hour 30 minutes = 60 + 30 = 90 minutes. 95 − 90 = 5. So <b>%s’s</b> movie is longer, by <b>5 minutes</b>." % b[0]))
    a, b = next(people), next(people)
    assert 65 - 58 == 7
    its.append(mcq("At the athletics carnival, %s runs a race in <b>58 seconds</b>. %s takes <b>1 minute 5 seconds</b>. "
                   "How much faster is %s?" % (a[0], b[0], a[0]), "7 seconds", ["47 seconds", "53 seconds", "1 minute 7 seconds"],
                   "1 minute 5 seconds = 60 + 5 = 65 seconds. 65 − 58 = <b>7 seconds</b>. "
                   "(Not 47: a minute is 60 seconds, not 100.)"))
    nm, pr = next(people)
    its.append(mcq("%s practises reading for <b>15 minutes</b> a day for <b>4 days</b>. How long is that in total?" % nm,
                   "1 hour", ["19 minutes", "45 minutes", "1 hour 15 minutes"],
                   "4 × 15 = 60 minutes. 60 minutes = <b>1 hour</b>.", key=dur_value))
    assert 2 * 7 + 3 == 17
    its.append(mcq("The school holidays last <b>2 weeks and 3 days</b>. How many days is that?", "17 days",
                   ["23 days", "10 days", "5 days"],
                   "1 week = 7 days, so 2 weeks = 14 days. 14 + 3 = <b>17 days</b>. (23 days would mean a week of 10 days.)"))
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 6, 4, 5, 11, 8, 7, 12, 13, 9, 14, 10, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "How long? Time in daily life", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Hours and minutes on an analog clock</h2>"
        "<p>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "When the long hand goes all the way around once, 60 minutes pass. "
        "In that time the short hand moves from one number to the next: <b>60 minutes = 1 hour</b>.</p>"
        "<p>Each number on the clock is <b>5 minutes</b> for the long hand, so count in 5s.</p>"
        "<figure class='sn-fig'>" + clock_svg(8, 35, size=230) +
        "<figcaption>The long hand points to 7: 7 × 5 = 35 minutes past 8. The short hand is between 8 and 9, "
        "so the hour is still 8. It is <b>25 to 9</b>, or 8:35 on a digital clock.</figcaption></figure>"
        "<h2>Past and to</h2>"
        "<p>When the long hand is on the right-hand side, say minutes <b>past</b> the hour. "
        "When it is on the left-hand side, say minutes <b>to</b> the next hour.</p>"
        + table(["Digital", "We say"], [["4:00", "4 o’clock"], ["4:15", "quarter past 4"], ["4:20", "20 past 4"],
                                        ["4:30", "half past 4"], ["4:35", "25 to 5"], ["4:45", "quarter to 5"],
                                        ["4:50", "10 to 5"]]) +
        "<h2>To the nearest minute</h2>"
        "<p>Between two numbers there are 5 small marks, one for each minute. Count in 5s to the last number, then on in 1s.</p>"
        + ex("Read to the minute", "The long hand is 3 small marks past the 4. The short hand is between 6 and 7.",
             "Count in 5s to the 4: 5, 10, 15, 20. Then 21, 22, 23.", "23 minutes past 6, or 6:23") +
        "<figure class='sn-fig'>" + clock_svg(4, 37, size=230) +
        "<figcaption>The long hand is 2 small marks past the 7: 35, 36, 37. The short hand is between 4 and 5. "
        "The digital time is <b>4:37</b>. It is 23 minutes to 5, because 60 − 37 = 23.</figcaption></figure>"
        "<h2>Digital clocks, am and pm</h2>"
        "<p>A digital clock shows the hour, then a colon, then the minutes: 4:37 means 37 minutes past 4. "
        "<b>am</b> is from midnight to midday (night and morning). <b>pm</b> is from midday to midnight (afternoon and evening).</p>"
        + ex("am or pm?", "Isla eats breakfast at 25 to 8. Write the time.",
             "25 to 8 is 35 minutes past 7. Breakfast is in the morning, so it is am.", "7:35 am") +
        "<h2>Units of time</h2>"
        + table(["Unit", "Equals"], [["1 minute", "60 seconds"], ["1 hour", "60 minutes"], ["1 day", "24 hours"],
                               ["1 week", "7 days"], ["1 fortnight", "14 days"], ["1 year", "12 months"]]) +
        "<p>To compare times, change them to the same unit. 2 minutes = 120 seconds, so 2 minutes is longer than 100 seconds.</p>"
        "<h2>How long? Count on</h2>"
        "<p>An hour has 60 minutes, not 100. Jump to the next o’clock first, then on to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(10, 50, 11, 20) +
        "<figcaption>Recess from 10:50 am to 11:20 am: 10 minutes to 11:00 am, then 20 more minutes. "
        "10 + 20 = 30 minutes.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“25 to 9” written as 9:35", "25 to 9 is before 9 o’clock: 60 − 25 = 35, so 8:35"],
            ["Long hand on 4 read as 4 minutes", "Each number is 5 minutes: 4 × 5 = 20 minutes"],
            ["Half past 3 read as half past 4", "The short hand has not reached 4 yet, so the hour is still 3"],
            ["8:40 said as “20 past 8”", "The long hand is on the left-hand side, so it is 20 <b>to</b> 9"],
            ["Breakfast at 7:30 pm", "Morning times are am: 7:30 am"],
            ["10:50 to 11:20 worked out as 1120 − 1050 = 70 minutes", "Count on: 10 + 20 = 30 minutes"],
        ])
    )


FAQ = [
    {"q": "What time should a Year 3 student be able to tell in Australia?",
     "a": "In the Australian Curriculum (AC9M3M04), Year 3 students read the time to the nearest minute on analog and digital clocks and describe how the hours and minutes are related."},
    {"q": "What is the difference between am and pm?",
     "a": "am times are from midnight to midday (night and morning). pm times are from midday to midnight (afternoon and evening), so school starts at an am time and dinner is at a pm time."},
    {"q": "Is telling the time tested in NAPLAN?",
     "a": "Measurement, including time, is part of the Year 3 NAPLAN numeracy test. Reading clocks and working out how long events last are useful skills to practise."},
    {"q": "How can I help my child learn to tell the time?",
     "a": "Use a real analog clock at home and ask the time at everyday moments, such as breakfast or bedtime. Start with o’clock and half past, then quarter past and quarter to, then count in 5s and on in 1s."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5). Picture items (A to D) keep their order and position."""
    for s in sets:
        fixed = [it["a"] for it in s["items"] if it.get("fixed")]
        targets = [p for p in range(4) for _ in range(5)]
        for p in fixed:
            targets.remove(p)
        rnd.shuffle(targets)
        targets = iter(targets)
        for it in s["items"]:
            if it.pop("fixed", False):
                continue
            t = next(targets)
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(3809)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_quarters(rnd), set_minute(rnd), set_ampm(rnd, people), set_units(rnd), set_problems(rnd, people)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    u = {
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "telling-the-time", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Telling the Time",
        "seo_title": "Year 3 Telling the Time Worksheets: Analog and Digital Clocks to the Minute (Free, with Answers)",
        "short_title": "Telling the time",
        "domain": "Measurement",
        "standard_code": "AC9M3M04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Describe the relationship between the hours and minutes on analog and digital clocks, and read the time to the nearest minute",
        "meta_desc": "Free Year 3 maths worksheets on telling the time: o’clock, half past, quarter past and quarter to, 5 minutes and the nearest minute on analog and digital clocks, am and pm, units of time and how long events last. 100 questions with an answer key, following the Australian Curriculum and useful for NAPLAN.",
        "key_big": "Short hand: the hour. Long hand: count in 5s, then on in 1s.",
        "key_sub": "60 minutes = 1 hour. Right-hand side: minutes past. Left-hand side: minutes to the next hour, so 25 to 9 is 8:35. am is before midday, pm is after midday.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "time line")
    mark_large(u, "four analog clocks")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
