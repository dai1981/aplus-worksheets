# -*- coding: utf-8 -*-
"""
AU Year 5 Maths: 12- and 24-Hour Time (Australian Curriculum v9.0, AC9M5M03)
  python3 tools/gen_au_maths_y5_time.py
Every analog clock is drawn from the time itself (the hour hand moves between the numbers).
Every answer is worked out in code from minutes since midnight. Wrong answers come from real student
mistakes: 3:45 pm written as 13:45 (a 1 put in front), 15:45 read as 5:45 pm (the 1 dropped),
12 am and 12 pm mixed up, am and pm swapped, an hour counted as 100 minutes, the hour hand read as the next hour.
HTML attributes use single quotes (no backslashes in the JSON). Australian English ("analog", "program").
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Charlotte", "she"), ("Oliver", "he"), ("Isla", "she"), ("Jack", "he"), ("Mia", "she"), ("Noah", "he"),
          ("Amelia", "she"), ("William", "he"), ("Ava", "she"), ("Leo", "he"), ("Harper", "she"), ("Lachlan", "he"),
          ("Chloe", "she"), ("Liam", "he"), ("Ruby", "she"), ("Aarav", "he"), ("Mei", "she"), ("Kai", "he"),
          ("Zara", "she"), ("Cooper", "he"), ("Matilda", "she"), ("Ethan", "he"), ("Sienna", "she"), ("Grace", "she")]
USED = set()   # (hour, minute) already asked in sets 1 to 3
# times written into fixed questions, kept out of the random picks
RESERVED = {(15, 43), (8, 38), (19, 12), (11, 52), (19, 45), (16, 25), (17, 52), (14, 15)}


# ------------------------------------------------------------ time formats
def h12(h24):
    return (h24 - 1) % 12 + 1


def tm12(h24, m):
    """12-hour digital: 3:45 pm"""
    h24 %= 24
    return "%d:%02d %s" % (h12(h24), m, "am" if h24 < 12 else "pm")


def t24(h24, m):
    """24-hour digital: 15:45"""
    return "%02d:%02d" % (h24 % 24, m)


def f24(t):
    return t24((t // 60) % 24, t % 60)


def f12(t):
    return tm12((t // 60) % 24, t % 60)


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


def raw_dur(hh, mm):
    """a duration as a student might write it, e.g. 1 hour 75 minutes (minutes may be 60 or more)"""
    if hh <= 0:
        return mins(mm) if mm > 0 else None
    return "%d hour%s" % (hh, "" if hh == 1 else "s") + (" %s" % mins(mm) if mm else "")


def dur_value(s):
    v = 0
    for n, unit in re.findall(r"(\d+) (hour|minute)", s):
        v += int(n) * (60 if unit == "hour" else 1)
    return v


def naive100(t1, t2):
    """the 100-minutes-in-an-hour mistake: 16:10 - 14:35 done as 1610 - 1435 = 175 -> 1 hour 75 minutes"""
    a = (t1 // 60) * 100 + t1 % 60
    b = (t2 // 60) * 100 + t2 % 60
    n = b - a
    if n <= 0:
        return None
    return raw_dur(n // 100, n % 100)


def hour_minute_diff(t1, t2):
    """hours subtracted, minutes subtracted the wrong way round: 14:35 to 16:10 -> 2 hours 25 minutes"""
    hh = t2 // 60 - t1 // 60
    mm = abs(t2 % 60 - t1 % 60)
    return raw_dur(hh, mm) if hh > 0 or mm > 0 else None


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


def clock_svg(h, m, size=200, inner24=False):
    """Analog clock face. The hour hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) >= 12, (h, m)
    R = size / 2.0 - 6
    cx = cy = size / 2.0
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
    hl = 0.4 if inner24 else 0.48
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * hl * math.cos(ah), cy + R * hl * math.sin(ah), LINE, 8 * k))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.82 * math.cos(am), cy + R * 0.82 * math.sin(am), RED, 4.5 * k))
    fs = max(19 * k, 15)
    rn = R - 29 * k
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, LINE, 3.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    if inner24:   # the afternoon hours in green, with a white edge so they stay readable over the hands
        fs2 = max(14 * k, 14)
        rn2 = R - 54 * k
        s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='3' "
                 "paint-order='stroke'>" % (fs2, GREEN))
        for n in range(1, 13):
            a = math.radians(n * 30 - 90)
            lab = "00" if n == 12 else str(n + 12)
            s.append("<text x='%.1f' y='%.1f'>%s</text>" % (cx + rn2 * math.cos(a), cy + rn2 * math.sin(a) + fs2 * 0.36, lab))
        s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return svg_wrap(size, size, "".join(s), "analog clock")


def jump_label(n):
    hh, mm = divmod(n, 60)
    if not hh:
        return "+%d min" % mm
    if not mm:
        return "+%d h" % hh
    return "+%d h %d min" % (hh, mm)


def jumps(t1, t2):
    """start -> next o'clock -> last o'clock -> end (absolute minutes, t2 may be the next day)"""
    pts = [t1]
    a = -(-t1 // 60) * 60
    if t1 < a <= t2:
        pts.append(a)
    b = (t2 // 60) * 60
    if b > pts[-1]:
        pts.append(b)
    if t2 > pts[-1]:
        pts.append(t2)
    return pts


def timeline_svg(t1, t2, fmt, W=460):
    """An open number line (not to scale): equal spaces, each jump labelled."""
    pts = jumps(t1, t2)
    L, R, Y = 52, W - 52, 72
    n = len(pts) - 1

    def X(i):
        return L + (R - L) * i / float(n)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i, t in enumerate(pts):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X(i), Y - 10, X(i), Y + 10, LINE))
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X(i), Y + 32, LINE, fmt(t)))
    for i in range(n):
        x1, x2 = X(i), X(i + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1 + 4, Y - 12, (x1 + x2) / 2, Y - 54, x2 - 4, Y - 12, RED))
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % ((x1 + x2) / 2, Y - 40, RED, jump_label(pts[i + 1] - pts[i])))
    return svg_wrap(W, 114, "".join(s), "time line from %s to %s" % (fmt(t1), fmt(t2)))


def count_on(t1, t2, fmt):
    """Explanation: count on in jumps."""
    pts = jumps(t1, t2)
    parts = ["%s to %s is %s" % (fmt(a), fmt(b), dur(b - a)) for a, b in zip(pts, pts[1:])]
    d = t2 - t1
    if len(parts) == 1:
        return "Count on: %s. So it is <b>%s</b>." % (parts[0], dur(d))
    terms = [dur(b - a) for a, b in zip(pts, pts[1:])]
    hrs = [x for x in terms if "minute" not in x]
    mns = [x for x in terms if "minute" in x]
    return "Count on: %s. %s = <b>%s</b>." % (", ".join(parts), " + ".join(hrs + mns), dur(d))


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
    if extra == 0:
        mm = "The minute hand points to <b>%d</b>: %d × 5 = <b>%d minutes</b> past." % (n, n, m)
    elif n == 0:
        mm = "The minute hand is <b>%d small mark%s</b> past the 12: <b>%s</b> past." % (extra, "" if extra == 1 else "s", mins(m))
    else:
        mm = ("The minute hand is %d small mark%s past the %d. Count in 5s to %d, then on in 1s: <b>%d minutes</b> past."
              % (extra, "" if extra == 1 else "s", n, n * 5, m))
    hh = "The hour hand is between <b>%d</b> and <b>%d</b>, so the hour is still <b>%d</b>." % (h, h % 12 + 1, h)
    return hh + " " + mm


def free(h, m):
    if (h, m) in USED:
        return False
    USED.add((h, m))
    return True


# ============================================================ set 1: analog clocks to 12-hour digital time
CONTEXTS = [  # sentence, possible hours (24-hour), minutes from, minutes to
    ("{n} goes for an early morning run.", [5, 6], 5, 55),
    ("{n} eats breakfast before school.", [7], 10, 50),
    ("The school bell rings in the morning.", [8], 40, 55),
    ("{n} eats recess with friends.", [10], 30, 55),
    ("{n} eats lunch at school.", [12], 5, 50),
    ("{n} has sport in the afternoon.", [13, 14], 5, 55),
    ("School finishes in the afternoon.", [15], 5, 25),
    ("{n} goes to footy training after school.", [16], 5, 55),
    ("{n} feeds the dog in the evening.", [17], 5, 55),
    ("{n} has dinner with the family.", [18], 5, 55),
    ("{n} goes to bed at night.", [20], 5, 45),
    ("{n} goes to the beach on Saturday morning.", [9], 5, 55),
    ("{n} watches the cricket on Sunday afternoon.", [14, 15], 5, 55),
    ("{n} wakes up to a storm in the middle of the night.", [2, 3], 5, 55),
    ("{n} hears the neighbours’ party just after midnight.", [0], 10, 50),
    ("{n} plays netball on Saturday morning.", [11], 5, 50),
]


def set_clocks(rnd, people):
    its = []
    ctx = CONTEXTS[:]
    rnd.shuffle(ctx)
    # o'clock-ish times first: the ones in 5s, then to the minute
    for i, (sent, hrs, lo, hi) in enumerate(ctx):
        while True:
            H = rnd.choice(hrs)
            if i < 5:
                m = rnd.choice([x for x in range(lo, hi + 1) if x % 5 == 0])
            else:
                m = rnd.choice([x for x in range(lo, hi + 1) if x % 5 and x not in (1, 59)])
            if hands_gap(H, m) >= 14 and free(H, m):
                break
        n = m // 5
        nm = next(people)[0]
        right = tm12(H, m)
        c = [tm12(H + 12, m)]                            # am and pm mixed up (12 pm and 12 am too)
        if m >= 35:
            c.append(tm12(H + 1, 60 - m))                # "13 minutes to 4" written as 4:13
        if n and n != m:
            c.append(tm12(H, n))                         # number the minute hand is near read as minutes
        c += [tm12(H + 1, m), tm12(H + 13, m), tm12(H, (m + 5) % 60)]
        if H == 0:
            why = "Just after midnight is the start of the morning, so it is <b>am</b>: 12 am, not 12 pm."
        elif H == 12:
            why = "Just after midday is the afternoon, so it is <b>pm</b>: 12 pm, not 12 am."
        elif H < 12:
            why = "Times from midnight to midday are <b>am</b>."
        else:
            why = "Times from midday to midnight are <b>pm</b>."
        e = "%s %s So it is <b>%s</b>." % (hand_text(H, m), why, right)
        q = fig(clock_svg(H, m)) + sent.format(n=nm) + " What is the time in 12-hour digital time?"
        its.append(mcq(q, right, c, e))
    # words to 12-hour digital
    word_qs = [(15, 43, "in the afternoon"), (8, 38, "in the morning"), (19, 12, "in the evening"), (11, 52, "in the morning")]
    for H, m, part in word_qs:
        w = words(H, m)
        right = tm12(H, m)
        ap = "am" if H < 12 else "pm"
        if m > 30:
            c = [tm12(H + 1, 60 - m), tm12(H + 1, m), tm12(H, 60 - m), tm12(H + 12, m)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d:%02d. "
                 "%s is %s, so it is <b>%s</b>." % (w, 60 - m, h12(H + 1), 60 - m, m, h12(H), m, part[0].upper() + part[1:], ap, right))
        else:
            c = [tm12(H - 1, 60 - m), tm12(H + 12, m), tm12(H, 60 - m), tm12(H + 1, m)]
            e = ("“%s” means %d minutes <b>after</b> %d o’clock: %d:%02d. %s is %s, so it is <b>%s</b>."
                 % (w, m, h12(H), h12(H), m, part[0].upper() + part[1:], ap, right))
        its.append(mcq("Write <b>%s %s</b> as a 12-hour digital time." % (w, part), right, c, e))
    return {"title": "Read analog clocks: 12-hour time with am and pm", "items": its}


# ============================================================ set 2: 12-hour to 24-hour time
SET_HOURS = []   # hours already used in the current set (so the set does not keep asking about 2 pm)


def pick(rnd, hrs, five=True, clock=False):
    tries = 0
    while True:
        tries += 1
        h = rnd.choice(hrs)
        m = rnd.choice(range(5, 56, 5)) if five else rnd.choice([x for x in range(2, 59) if x % 5])
        if clock and hands_gap(h, m) < 14:
            continue
        if h in SET_HOURS and tries < 300:
            continue
        if free(h, m):
            SET_HOURS.append(h)
            return h, m


def q_pm_to24(H, m):
    h = H - 12
    right = t24(H, m)
    c = [t24(10 + h, m) if h < 10 else None,        # a 1 put in front: 3:45 pm -> 13:45
         "%02d:%02d" % (h, m), t24(H - 1, m), t24(H + 1, m), t24(H - 2, m)]
    note = " (Do not just put a 1 in front: 1%d:%02d is %s.)" % (h, m, tm12(10 + h, m)) if h < 10 else ""
    e = ("pm times are after midday. Add 12 to the hour: %d + 12 = %d. So %s is <b>%s</b>.%s"
         % (h, H, tm12(H, m), right, note))
    return mcq("Write <b>%s</b> in 24-hour time." % tm12(H, m), right, c, e)


def q_am_to24(H, m):
    right = t24(H, m)
    c = [t24(H + 12, m), t24(H + 10, m), t24(H + 1, m), t24(H - 1, m)]
    if H < 10:
        e = ("am times are before midday, so the hour stays the same. A 24-hour time always has 4 digits, "
             "so put a 0 in front of a 1-digit hour: %s is <b>%s</b>." % (tm12(H, m), right))
    else:
        e = "am times are before midday, so the hour stays the same. Do not add 12. %s is <b>%s</b>." % (tm12(H, m), right)
    return mcq("Write <b>%s</b> in 24-hour time." % tm12(H, m), right, c, e)


def set_to24(rnd):
    its = []
    SET_HOURS[:] = [19, 16]
    for k in range(2):
        its.append(q_pm_to24(*pick(rnd, [13, 14, 15, 16, 17, 18, 19])))
    for k in range(2):
        its.append(q_am_to24(*pick(rnd, [6, 7, 8, 9])))
    for k in range(2):
        its.append(q_pm_to24(*pick(rnd, [20, 21, 22, 23])))
    its.append(q_am_to24(*pick(rnd, [10, 11])))
    # noon and midnight
    H, m = pick(rnd, [12])
    its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(12, m), t24(12, m),
                   ["24:%02d" % m, "00:%02d" % m, "13:%02d" % m],
                   "12 pm is the hour just after <b>midday</b>. Midday is 12:00 in 24-hour time, so do not add 12. "
                   "%s is <b>%s</b>." % (tm12(12, m), t24(12, m))))
    H, m = pick(rnd, [0])
    its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(0, m), t24(0, m),
                   ["12:%02d" % m, "24:%02d" % m, "01:%02d" % m],
                   "12 am is the hour just after <b>midnight</b>. In 24-hour time a new day starts at 00:00, "
                   "so %s is <b>%s</b>." % (tm12(0, m), t24(0, m))))
    # to the minute
    for k in range(3):
        its.append(q_pm_to24(*pick(rnd, [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], five=False)))
    its.append(q_am_to24(*pick(rnd, [5, 6, 7, 8, 9], five=False)))
    its.append(q_am_to24(*pick(rnd, [10, 11], five=False)))
    H, m = pick(rnd, [12], five=False)
    its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(12, m), t24(12, m),
                   ["00:%02d" % m, "24:%02d" % m, "13:%02d" % m],
                   "12 pm is just after midday, and midday is 12:00. Keep the 12: <b>%s</b>." % t24(12, m)))
    H, m = pick(rnd, [0], five=False)
    its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(0, m), t24(0, m),
                   ["12:%02d" % m, "24:%02d" % m, "11:%02d" % m],
                   "12 am is just after midnight. The 24-hour clock starts the day at 00, so %s is <b>%s</b>."
                   % (tm12(0, m), t24(0, m))))
    # words to 24-hour
    for H, m, part in [(19, 45, "in the evening"), (16, 25, "in the afternoon")]:
        w = words(H, m)
        right = t24(H, m)
        if m > 30:
            c = [t24(H + 1, m), t24(H + 1, 60 - m), "%02d:%02d" % (H - 12, m), t24(H - 2, m)]
            e = ("“%s” is %d minutes before %d o’clock: %d:%02d pm. Add 12 to the hour: %d + 12 = %d. So it is <b>%s</b>."
                 % (w, 60 - m, h12(H + 1), h12(H), m, h12(H), H, right))
        else:
            c = ["%02d:%02d" % (H - 12, m), t24(H - 2, m), t24(H - 1, 60 - m), t24(H + 1, m)]
            e = ("“%s” is %d:%02d pm. Add 12 to the hour: %d + 12 = %d. So it is <b>%s</b>."
                 % (w, h12(H), m, h12(H), H, right))
        its.append(mcq("Which 24-hour time is <b>%s %s</b>?" % (w, part), right, c, e))
    # clocks to 24-hour
    for sent, hrs in [("The clock shows a time in the evening.", [18, 19, 20, 21]),
                      ("The clock shows a time in the afternoon.", [13, 14, 15, 16])]:
        H, m = pick(rnd, hrs, five=False, clock=True)
        n = m // 5
        right = t24(H, m)
        c = ["%02d:%02d" % (H - 12, m), t24(H - 2, m)]
        if n and n != m:
            c.append(t24(H, n))
        c += [t24(H + 1, m), t24(H, (m + 5) % 60)]
        e = ("%s It is %d:%02d pm. Add 12 to the hour: %d + 12 = %d. So it is <b>%s</b>."
             % (hand_text(H, m), h12(H), m, h12(H), H, right))
        its.append(mcq(fig(clock_svg(H, m)) + sent + " Write it in 24-hour time.", right, c, e))
    assert len(its) == 20, len(its)
    return {"title": "Change 12-hour time to 24-hour time", "items": its}


# ============================================================ set 3: 24-hour to 12-hour time
def q_24pm(H, m):
    right = tm12(H, m)
    c = []
    if H <= 22:
        c.append("%d:%02d pm" % (H - 10, m))             # 15:45 -> 5:45 pm (the 1 dropped); 21:30 -> 11:30 pm (10 taken away)
    c += [tm12(H - 12, m), tm12(H - 1, m), tm12(H + 1, m)]
    if H <= 19:
        note = " (Do not just drop the 1: %d:%02d pm is %s.)" % (H - 10, m, t24(H + 2, m))
    elif H <= 22:
        note = " (Take away 12, not 10: %d:%02d pm is %s.)" % (H - 10, m, t24(H + 2, m) if H < 22 else t24(12, m))
    else:
        note = ""
    e = ("Hours 13 to 23 are pm. Take away 12: %d − 12 = %d. So %s is <b>%s</b>.%s" % (H, H - 12, t24(H, m), right, note))
    return mcq("Write <b>%s</b> as a 12-hour time." % t24(H, m), right, c, e)


def q_24am(H, m):
    right = tm12(H, m)
    c = [tm12(H + 12, m), tm12(H + 1, m), tm12(H - 1, m), tm12(H + 13, m)]
    if H < 10:
        e = ("The hour %02d is less than 12, so it is a morning time: <b>am</b>. Drop the 0 at the front: <b>%s</b>."
             % (H, right))
    else:
        e = "The hour %d is less than 12, so it is a morning time. Keep the hour and write am: <b>%s</b>." % (H, right)
    return mcq("Write <b>%s</b> as a 12-hour time." % t24(H, m), right, c, e)


def set_to12(rnd, people):
    its = []
    SET_HOURS[:] = [17, 14]
    for k in range(2):
        its.append(q_24pm(*pick(rnd, [13, 14, 15, 16, 17])))
    for k in range(2):
        its.append(q_24am(*pick(rnd, [6, 7, 8, 9])))
    for k in range(2):
        its.append(q_24pm(*pick(rnd, [18, 19, 20, 21, 22])))
    its.append(q_24am(*pick(rnd, [10, 11])))
    H, m = pick(rnd, [12])
    its.append(mcq("Write <b>%s</b> as a 12-hour time." % t24(12, m), tm12(12, m),
                   ["12:%02d am" % m, "0:%02d pm" % m, "11:%02d am" % m],
                   "12 is the hour just after <b>midday</b>, so it is pm. Do not take away 12. %s is <b>%s</b>."
                   % (t24(12, m), tm12(12, m))))
    H, m = pick(rnd, [0])
    its.append(mcq("Write <b>%s</b> as a 12-hour time." % t24(0, m), tm12(0, m),
                   ["12:%02d pm" % m, "0:%02d am" % m, "11:%02d pm" % m],
                   "00 is the hour just after <b>midnight</b>. In 12-hour time we call it 12 am. %s is <b>%s</b>."
                   % (t24(0, m), tm12(0, m))))
    for k in range(3):
        its.append(q_24pm(*pick(rnd, [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], five=False)))
    its.append(q_24am(*pick(rnd, [4, 5, 6, 7, 8, 9], five=False)))
    its.append(q_24am(*pick(rnd, [10, 11], five=False)))
    H, m = pick(rnd, [12], five=False)
    its.append(mcq("Write <b>%s</b> as a 12-hour time." % t24(12, m), tm12(12, m),
                   ["12:%02d am" % m, "0:%02d pm" % m, "1:%02d pm" % m],
                   "12 is just after midday, so it is pm. Keep the 12: <b>%s</b>." % tm12(12, m)))
    H, m = pick(rnd, [0], five=False)
    its.append(mcq("Write <b>%s</b> as a 12-hour time." % t24(0, m), tm12(0, m),
                   ["12:%02d pm" % m, "0:%02d am" % m, "10:%02d am" % m],
                   "00 is the first hour of the day, just after midnight. In 12-hour time it is 12 am: <b>%s</b>." % tm12(0, m)))
    # in context
    nm, pr = next(people)
    its.append(mcq("%s’s train leaves at <b>17:52</b>. What is this in 12-hour time?" % nm, "5:52 pm",
                   ["7:52 pm", "5:52 am", "6:52 pm"],
                   "17 is more than 12, so it is pm. 17 − 12 = 5. 17:52 is <b>5:52 pm</b>. "
                   "(Dropping the 1 gives 7:52 pm, which is 19:52.)"))
    its.append(mcq("The koala talk at the wildlife park starts at <b>14:15</b>. What is this in 12-hour time?", "2:15 pm",
                   ["4:15 pm", "2:15 am", "12:15 pm"],
                   "14 − 12 = 2, and it is after midday, so it is pm. 14:15 is <b>2:15 pm</b>."))
    # compare the two systems
    t = ["9:15 pm", "20:50", "11:05 am", "18:30"]
    its.append(mcq("Which of these times is the <b>latest</b> in the day?", t[0], t[1:],
                   "Change them all to 24-hour time: 9:15 pm = 21:15, 11:05 am = 11:05. "
                   "11:05, 18:30, 20:50, 21:15. The latest is <b>9:15 pm</b>."))
    t = ["12:40 am", "1:15 am", "06:30", "12:10 pm"]
    its.append(mcq("Which of these times is the <b>earliest</b> in the day?", t[0], t[1:],
                   "Change them all to 24-hour time: 12:40 am = 00:40, 1:15 am = 01:15, 12:10 pm = 12:10. "
                   "The day starts at 00:00, so the earliest is <b>12:40 am</b>."))
    assert len(its) == 20, len(its)
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 9, 10, 11, 12, 13, 14, 15, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Change 24-hour time to 12-hour time", "items": [its[i] for i in order]}


# ============================================================ set 4: how long? durations across times
def dur_q(q, t1, t2, fmt, extra=(), line=False):
    d = t2 - t1
    c = list(extra) + [naive100(t1, t2), hour_minute_diff(t1, t2), dur(d + 10), dur(d - 5) if d > 5 else None,
                       dur(d + 60), dur(d - 60) if d > 60 else None, dur(d + 5)]
    e = count_on(t1, t2, fmt)
    if naive100(t1, t2) and dur_value(naive100(t1, t2)) != d:
        e += " (An hour has 60 minutes, not 100, so do not just subtract the numbers.)"
    if line:
        q = fig(timeline_svg(t1, t2, fmt)) + q
    return mcq(q, dur(d), c, e, key=dur_value)


def set_durations(rnd):
    its = []
    seen = set()

    hours = {}

    def new(t1, t2):
        """no repeated question, and a different start hour within each kind of question"""
        tier = len(its) // 3 if len(its) < 6 else 2 if len(its) < 10 else 3
        if (t1, t2) in seen or t1 // 60 in hours.setdefault(tier, set()):
            return False
        seen.add((t1, t2))
        hours[tier].add(t1 // 60)
        return True
    # crosses one o'clock, less than an hour, minutes in 5s
    k = 0
    while k < 3:
        h1 = rnd.randint(7, 20)
        m1 = rnd.choice([35, 40, 45, 50, 55])
        d = 60 - m1 + rnd.choice(range(5, 31, 5))
        t1 = h1 * 60 + m1
        if d >= 60 or not new(t1, t1 + d):
            continue
        its.append(dur_q("How long is it from <b>%s</b> to <b>%s</b>?" % (f24(t1), f24(t1 + d)), t1, t1 + d, f24, line=k == 0))
        k += 1
    # crosses one o'clock, to the minute
    k = 0
    while k < 3:
        h1 = rnd.randint(7, 20)
        m1 = rnd.choice([x for x in range(33, 58) if x % 5])
        d = 60 - m1 + rnd.choice([x for x in range(3, 30) if x % 5])
        t1 = h1 * 60 + m1
        if d >= 60 or not new(t1, t1 + d):
            continue
        its.append(dur_q("How long is it from <b>%s</b> to <b>%s</b>?" % (f24(t1), f24(t1 + d)), t1, t1 + d, f24))
        k += 1
    # more than an hour, 24-hour times (the end minutes are smaller than the start minutes)
    k = 0
    while k < 4:
        h1 = rnd.randint(8, 18)
        m1 = rnd.choice(range(20, 56, 5)) if k < 2 else rnd.choice([x for x in range(21, 58) if x % 5])
        d = rnd.choice([x for x in range(65, 230, 5 if k < 2 else 1) if x % 60])
        t1 = h1 * 60 + m1
        t2 = t1 + d
        if t2 % 60 >= m1 or t2 % 60 == 0 or t2 // 60 > 22 or not new(t1, t2):
            continue
        its.append(dur_q("How long is it from <b>%s</b> to <b>%s</b>?" % (f24(t1), f24(t2)), t1, t2, f24, line=k == 0))
        k += 1
    # across midday in 12-hour time
    k = 0
    while k < 3:
        h1 = rnd.choice([9, 10, 11])
        m1 = rnd.choice(range(25, 56, 5))
        h2 = rnd.choice([12, 13, 14, 15])
        m2 = rnd.choice([x for x in range(5, m1, 5)])
        t1, t2 = h1 * 60 + m1, h2 * 60 + m2
        if not new(t1, t2):
            continue
        back = (h1 * 60 + m1) - (h12(h2) * 60 + m2)       # took the smaller time from the bigger one
        extra = [dur(back) if h2 > 12 and back > 0 else None]
        its.append(dur_q("How long is it from <b>%s</b> to <b>%s</b>?" % (f12(t1), f12(t2)), t1, t2, f12, extra=extra,
                         line=k == 0))
        k += 1
    # mixed formats
    for (a, b) in [((8, 50, "12"), (13, 25, "24")), ((11, 40, "24"), (4, 15, "12pm"))]:
        t1 = a[0] * 60 + a[1]
        t2 = (b[0] + (12 if b[2] == "12pm" else 0)) * 60 + b[1]
        s1 = f12(t1) if a[2] == "12" else f24(t1)
        s2 = f12(t2) if b[2].startswith("12") else f24(t2)
        d = t2 - t1
        if b[2] == "24":
            extra = [dur(t2 + 120 - t1)]                    # 13:25 read as 3:25 pm (the 1 dropped)
        else:
            extra = [dur(t1 - (b[0] * 60 + b[1]))]          # took 4:15 from 11:40
        e_pre = "Change both times to 24-hour time first: %s and %s. " % (f24(t1), f24(t2))
        it = dur_q("How long is it from <b>%s</b> to <b>%s</b>?" % (s1, s2), t1, t2, f24, extra=extra)
        it["e"] = e_pre + it["e"]
        its.append(it)
    # finishing times
    for t1, d, txt in [(14 * 60 + 35, 110, "A junior cricket match starts at <b>%s</b> and lasts <b>%s</b>."),
                       (9 * 60 + 48, 135, "The Year 5 excursion bus leaves school at <b>%s</b>. The trip to the zoo takes <b>%s</b>."),
                       (19 * 60 + 50, 75, "The school concert starts at <b>%s</b> and lasts <b>%s</b>.")]:
        t2 = t1 + d
        right = f24(t2)
        c = [f24(t2 - 60),                               # minutes went over 60 but the extra hour was not added
             "%02d:%02d" % (h12(t2 // 60), t2 % 60) if t2 // 60 > 12 else None,
             f24(t2 + 60), f24(t2 + 10), f24(t2 - 10)]
        e = ("Add the hours first: %s + %s = %s. Then add %s: %s. So it is <b>%s</b>."
             % (f24(t1), dur(d - d % 60), f24(t1 + d - d % 60), mins(d % 60),
                count_on(t1 + d - d % 60, t2, f24).replace("Count on: ", "").split(". ")[0], right))
        ask = " What time does it get there?" if "bus" in txt else " What time does it finish?"
        its.append(mcq(txt % (f24(t1), dur(d)) + ask, right, c, e))
    # starting times
    for t2, d in [(16 * 60 + 20, 105), (12 * 60 + 10, 95)]:
        t1 = t2 - d
        right = f24(t1)
        c = [f24(t1 + 60), f24(t2 + d), f24(t1 + 10), f24(t1 - 10)]
        e = ("Count back the hours first: %s − %s = %s. Then count back %s: <b>%s</b>."
             % (f24(t2), dur(d - d % 60), f24(t2 - (d - d % 60)), mins(d % 60), right))
        txt = ("A movie finishes at <b>%s</b>. It is <b>%s</b> long. What time did it start?" % (f24(t2), dur(d))
               if t2 // 60 == 16 else
               "The athletics carnival breaks for lunch at <b>%s</b>. The morning events took <b>%s</b>. "
               "What time did they start?" % (f24(t2), dur(d)))
        its.append(mcq(txt, right, c, e))
    assert len(its) == 20, len(its)
    return {"title": "How long? Durations across 12- and 24-hour times", "items": its}


# ============================================================ set 5: timetables and practical problems
def timetable_svg(title, head, stops, cols):
    """cols: list of columns, each a list of absolute minutes for every stop."""
    LW, CW, RH = 140, 74, 30
    W = LW + CW * len(cols) + 4
    H = RH * (len(stops) + 1) + 4
    s = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (W - 4, RH, GREEN)]
    s.append("<text x='10' y='23' font-size='15' font-weight='700' fill='#fff'>%s</text>" % title)
    for j in range(len(cols)):
        s.append("<text x='%.0f' y='23' font-size='15' font-weight='700' fill='#fff' text-anchor='middle'>%s %d</text>"
                 % (2 + LW + CW * j + CW / 2.0, head, j + 1))
    for i, st in enumerate(stops):
        y = 2 + RH * (i + 1)
        if i % 2:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
        s.append("<text x='10' y='%d' font-size='16' fill='%s'>%s</text>" % (y + 21, LINE, st))
        for j, col in enumerate(cols):
            s.append("<text x='%.0f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (2 + LW + CW * j + CW / 2.0, y + 21, LINE, f24(col[i])))
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, LINE))
    for j in range(len(cols)):
        x = 2 + LW + CW * j
        s.append("<line x1='%d' y1='2' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, x, H - 2, LINE))
    return svg_wrap(W, H, "".join(s), "timetable: %s" % title.lower())


def grid_svg(label, head, widths, rows, aligns):
    """A simple table picture: header row in green, rows of text."""
    RH = 30
    W = sum(widths) + 4
    H = RH * (len(rows) + 1) + 4
    s = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (W - 4, RH, GREEN)]
    xs = [2]
    for w in widths:
        xs.append(xs[-1] + w)

    def put(i, y, txt, color, bold):
        if aligns[i] == "m":
            x, anc = (xs[i] + xs[i + 1]) / 2.0, "middle"
        else:
            x, anc = xs[i] + 8, "start"
        return ("<text x='%.0f' y='%d' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
                % (x, y, 15 if color == "#fff" else 16, "700" if bold else "400", color, anc, txt))
    for i, hd in enumerate(head):
        s.append(put(i, 23, hd, "#fff", True))
    for r, row in enumerate(rows):
        y = 2 + RH * (r + 1)
        if r % 2:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
        for i, cell in enumerate(row):
            s.append(put(i, y + 21, cell, LINE, aligns[i] == "m"))
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, LINE))
    for x in xs[1:-1]:
        s.append("<line x1='%d' y1='2' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, x, H - 2, LINE))
    return svg_wrap(W, H, "".join(s), label)


def train_qs(rnd, people):
    legs = [0, 3, 0, 0]
    legs[2] = legs[1] + rnd.choice([10, 11, 12])
    legs[3] = legs[2] + rnd.choice([13, 14, 15])
    first = 16 * 60 + rnd.choice([38, 41, 44])
    cols = [[first + 15 * j + l for l in legs] for j in range(4)]
    S = ["Central", "Redfern", "Strathfield", "Parramatta"]
    svg = fig(timetable_svg("Sydney trains", "Train", S, cols))
    its = []
    # 1 arrival
    j = rnd.choice([1, 2])
    right = f24(cols[j][3])
    c = [f24(cols[j][2]), f24(cols[j + 1][3]), f24(cols[j - 1][3]), f24(cols[j][1])]
    its.append(mcq(svg + "A train leaves <b>Central</b> at %s. What time does it get to <b>Parramatta</b>?" % f24(cols[j][0]),
                   right, c, "Find %s in the Central row. Go down that column to the Parramatta row: <b>%s</b>." % (f24(cols[j][0]), right)))
    # 2 which one leaves
    j2 = 3 if j != 3 else 0
    right = f24(cols[j2][0])
    c = [f24(cols[j2][1]), f24(cols[j2 - 1][0]), f24(cols[(j2 + 1) % 4][0]), f24(cols[j2][2])]
    its.append(mcq(svg + "A train gets to <b>Strathfield</b> at %s. What time did it leave <b>Central</b>?" % f24(cols[j2][2]),
                   right, c, "Find %s in the Strathfield row. Go up that column to the Central row: <b>%s</b>." % (f24(cols[j2][2]), right)))
    # 3 journey time (crosses the hour)
    jj = [x for x in range(4) if cols[x][0] // 60 != cols[x][3] // 60]
    a, b = cols[rnd.choice(jj)][0], None
    b = a + legs[3]
    its.append(dur_q(svg + "How long does the train that leaves <b>Central</b> at %s take to get to <b>Parramatta</b>?" % f24(a),
                     a, b, f24, extra=[mins(legs[2])]))
    # 4 latest train to be on time
    nm, pr = next(people)
    j4 = rnd.choice([1, 2])
    lim = cols[j4][3] + rnd.choice([3, 5, 7])
    while lim % 5:
        lim += 1
    assert cols[j4][3] <= lim < cols[j4 + 1][3]
    right = f24(cols[j4][1])
    c = [f24(cols[j4 + 1][1]), f24(cols[j4 - 1][1]), f24(cols[j4][0]), f24(cols[j4][3])]
    e = ("Look along the Parramatta row for the last time that is not after %s: %s. Go up that column to Redfern: <b>%s</b>. "
         "The next train gets to Parramatta at %s, which is too late." % (f24(lim), f24(cols[j4][3]), right, f24(cols[j4 + 1][3])))
    its.append(mcq(svg + "%s must be at <b>Parramatta</b> by %s. What is the latest train %s can catch from <b>Redfern</b>?"
                   % (nm, f24(lim), pr), right, c, e))
    # 5 waiting time
    nm, pr = next(people)
    j5 = rnd.choice([0, 1, 2])
    arr = cols[j5][1] + rnd.choice([4, 6, 8, 9])
    wait = cols[j5 + 1][1] - arr
    c = [mins(15), naive100(arr, cols[j5 + 1][1]), mins(wait + 5), mins(wait - 2), mins(wait + 10)]
    e = ("The %s train has gone. The next train from Redfern is at %s. %s"
         % (f24(cols[j5][1]), f24(cols[j5 + 1][1]), count_on(arr, cols[j5 + 1][1], f24)))
    its.append(mcq(svg + "%s gets to <b>Redfern</b> at %s, just after a train has left. How long must %s wait for the next one?"
                   % (nm, f24(arr), pr), mins(wait), c, e, key=dur_value))
    # 6 12-hour time on the timetable
    nm, pr = next(people)
    t = cols[rnd.choice(range(4))][2]
    right = f24(t)
    H, m = t // 60, t % 60
    c = ["%02d:%02d" % (H - 12, m), t24(H - 2, m), f24(t - legs[2] + legs[1]), t24(H + 1, m)]
    e = "%s is after midday, so add 12 to the hour: %d + 12 = %d. Look for <b>%s</b> in the Strathfield row." % (
        f12(t), H - 12, H, right)
    its.append(mcq(svg + "%s’s train gets to <b>Strathfield</b> at %s. Which time on the timetable is this?" % (nm, f12(t)),
                   right, c, e))
    return its


FLIGHTS = [("Sydney", "Melbourne", 7 * 60 + 10, 8 * 60 + 40), ("Melbourne", "Hobart", 9 * 60 + 55, 11 * 60 + 10),
           ("Sydney", "Canberra", 13 * 60 + 25, 14 * 60 + 20), ("Melbourne", "Sydney", 17 * 60 + 45, 19 * 60 + 10)]


def flight_qs(people):
    rows = [[a, b, f24(d), f24(r)] for a, b, d, r in FLIGHTS]
    svg = fig(grid_svg("flight timetable", ["From", "To", "Departs", "Arrives"], [116, 116, 90, 90], rows, "llmm"))
    its = []
    a, b, d, r = FLIGHTS[1]
    its.append(dur_q(svg + "How long is the flight from <b>Melbourne to Hobart</b>?", d, r, f24))
    names = ["%s to %s" % (x[0], x[1]) for x in FLIGHTS]
    lens = [x[3] - x[2] for x in FLIGHTS]
    best = lens.index(min(lens))
    e = ("Work out each flight: " + ", ".join("%s %s" % (n, dur(l)) for n, l in zip(names, lens)) +
         ". The shortest is <b>%s</b>." % names[best])
    its.append(mcq(svg + "Which flight takes the <b>shortest</b> time?", names[best], [n for i, n in enumerate(names) if i != best], e))
    nm, pr = next(people)
    a, b, d, r = FLIGHTS[3]
    its.append(mcq(svg + "%s flies from <b>Melbourne to Sydney</b>. What time does %s land, in 12-hour time?" % (nm, pr),
                   f12(r), ["9:10 pm", f12(r - 720), f12(d)],
                   "The flight arrives at %s. 19 − 12 = 7, and it is the evening, so it is <b>%s</b>." % (f24(r), f12(r))))
    a, b, d, r = FLIGHTS[2]
    nr = r + 45
    its.append(mcq(svg + "The flight from <b>Sydney to Canberra</b> is <b>45 minutes</b> late. What time does it land now?",
                   f24(nr), [f24(nr - 60), f24(r + 60), f24(d + 45)],
                   "It was going to land at %s. %s + 45 minutes: 40 minutes takes it to 15:00, then 5 more minutes: <b>%s</b>."
                   % (f24(r), f24(r), f24(nr))))
    return its


TV = [(17 * 60, "Cricket highlights"), (18 * 60, "News"), (19 * 60, "Quiz show"), (19 * 60 + 30, "Wildlife documentary"),
      (20 * 60 + 45, "Movie"), (23 * 60 + 10, "Late news")]


def tv_qs(people):
    rows = [[f24(TV[i][0]), TV[i][1], f24(TV[i + 3][0]), TV[i + 3][1]] for i in range(3)]
    svg = fig(grid_svg("TV guide", ["Time", "Saturday", "Time", "Saturday"], [70, 196, 70, 196], rows, "mlml"))
    its = []
    progs = [p for _, p in TV]
    its.append(mcq(svg + "Which program is on at <b>8:15 pm</b>?", "Wildlife documentary", ["News", "Movie", "Quiz show"],
                   "8:15 pm is 20:15 in 24-hour time (8 + 12 = 20). The documentary starts at 19:30 and the movie starts at 20:45, "
                   "so the <b>Wildlife documentary</b> is on. (8:15 pm is not 18:15.)"))
    t1, t2 = TV[4][0], TV[5][0]
    its.append(dur_q(svg + "The movie runs until the late news starts. How long is the movie?", t1, t2, f24))
    nm, pr = next(people)
    bed = 21 * 60 + 30
    its.append(mcq(svg + "%s’s bedtime is <b>9:30 pm</b>. How much of the movie can %s watch before bed?" % (nm, pr),
                   mins(bed - t1), ["85 minutes", "1 hour 15 minutes", "15 minutes"],
                   "9:30 pm is 21:30. %s" % count_on(t1, bed, f24), key=dur_value))
    its.append(mcq(svg + "What time does the <b>Late news</b> start, in 12-hour time?", f12(TV[5][0]),
                   ["3:10 pm", "11:10 am", "10:10 pm"],
                   "The late news starts at 23:10. 23 − 12 = 11, and it is night, so it is <b>11:10 pm</b>. "
                   "(Dropping the 2 gives 3:10 pm, which is 15:10.)"))
    return its


def daily(people):
    out = []
    nm, pr = next(people)
    out.append(mcq("A Friday night footy match starts at <b>19:25</b>. With the breaks it lasts <b>2 hours 40 minutes</b>. "
                   "What time does it finish, in 12-hour time?", "10:05 pm", ["9:05 pm", "10:05 am", "11:05 pm"],
                   "19:25 + 2 hours = 21:25. Then add 40 minutes: 35 minutes takes it to 22:00, then 5 more: 22:05. "
                   "22 − 12 = 10, so it finishes at <b>10:05 pm</b>."))
    t1, t2 = 9 * 60 + 35, 14 * 60 + 20
    out.append(mcq("The swimming carnival starts at <b>9:35 am</b> and finishes at <b>14:20</b>. How long does it last?",
                   dur(t2 - t1), [dur(t2 + 120 - t1), naive100(t1, t2), hour_minute_diff(t1, t2)],
                   "Change 9:35 am to 09:35. %s (14:20 is 2:20 pm, not 4:20 pm.)" % count_on(t1, t2, f24), key=dur_value))
    nm, pr = next(people)
    out.append(mcq("%s gets to the pool at <b>5:10 pm</b>. The sign says the pool closes at <b>17:45</b>. "
                   "How long can %s swim?" % (nm, pr), "35 minutes",
                   ["2 hours 35 minutes", "12 hours 35 minutes", "1 hour 35 minutes"],
                   "17:45 is 5:45 pm (17 − 12 = 5), not 7:45 pm. 5:10 pm to 5:45 pm is 45 − 10 = <b>35 minutes</b>.",
                   key=dur_value))
    out.append(mcq("Dinner is at <b>18:30</b>. A roast takes <b>1 hour 45 minutes</b> to cook. What time must it go in the oven?",
                   "16:45", ["20:15", "17:45", "17:15"],
                   "Count back 1 hour: 18:30 − 1 hour = 17:30. Then count back 45 minutes: 30 minutes to 17:00, "
                   "then 15 more: <b>16:45</b>."))
    out.append(mcq("An overnight train leaves Sydney at <b>20:40</b> and gets to Melbourne at <b>07:35</b> the next morning. "
                   "How long is the trip?", dur(11 * 60 - 5), ["13 hours 5 minutes", "11 hours 55 minutes", "9 hours 55 minutes"],
                   count_on(20 * 60 + 40, 24 * 60 + 7 * 60 + 35, f24) +
                   " (Taking 07:35 from 20:40 gives 13 hours 5 minutes, but the train travels through midnight.)",
                   key=dur_value))
    nm, pr = next(people)
    out.append(mcq("%s’s mum parks at <b>11:55 am</b> and pays for <b>2 hours 30 minutes</b>. "
                   "By what time must she leave, in 24-hour time?" % nm, "14:25", ["02:25", "13:55", "13:25"],
                   "11:55 + 2 hours = 13:55. Then add 30 minutes: 5 minutes takes it to 14:00, then 25 more: <b>14:25</b>. "
                   "It is after midday, so the hour is 14, not 02."))
    return out


def set_problems(rnd, people):
    d = daily(people)
    its = train_qs(rnd, people) + d[0:2] + flight_qs(people) + d[2:4] + tv_qs(people) + d[4:6]
    assert len(its) == 20, len(its)
    return {"title": "Timetables and time problems: trains, flights and TV", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Two ways to write the time</h2>"
        "<p>A day has 24 hours. An analog clock only shows 12, so <b>12-hour time</b> adds <b>am</b> (midnight to midday) "
        "or <b>pm</b> (midday to midnight). <b>24-hour time</b> counts the hours from 00 to 23, so it needs no am or pm. "
        "It always has <b>4 digits</b>: 07:30, 15:45. Train timetables, flights and TV guides often use it.</p>"
        "<figure class='sn-fig'>" + clock_svg(15, 45, size=260, inner24=True) +
        "<figcaption>The green numbers are the afternoon and evening hours. The hour after 12 is 13, so in the afternoon "
        "this clock shows <b>15:45</b>, which is 3:45 pm.</figcaption></figure>"
        "<h2>12-hour to 24-hour</h2>"
        + table(["12-hour", "24-hour", "Rule"], [
            ["12:20 am", "00:20", "just after midnight: the hour is 00"],
            ["7:05 am", "07:05", "am: keep the hour, write 4 digits"],
            ["12:20 pm", "12:20", "just after midday: keep 12"],
            ["3:45 pm", "15:45", "pm: add 12 (3 + 12 = 15)"],
            ["9:10 pm", "21:10", "pm: add 12 (9 + 12 = 21)"],
        ]) +
        ex("Analog to 24-hour", "The clock shows 20 to 7 in the evening. Write it in 24-hour time.",
           "20 to 7 is 40 minutes past 6: 6:40 pm. Add 12 to the hour: 6 + 12 = 18.", "18:40") +
        "<h2>24-hour to 12-hour</h2>"
        "<p>Hours 13 to 23: take away 12 and write pm. Hours 01 to 11: keep the hour and write am. "
        "12 is pm and 00 is 12 am.</p>"
        + ex("Read a timetable time", "A train arrives at 17:08. Write it in 12-hour time.",
             "17 − 12 = 5, and it is after midday.", "5:08 pm") +
        "<h2>How long? Count on in jumps</h2>"
        "<p>An hour has 60 minutes, not 100, so do not just subtract the numbers. "
        "Jump to the next o’clock, then on in whole hours, then to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(14 * 60 + 35, 16 * 60 + 10, f24) +
        "<figcaption>14:35 to 15:00 is 25 minutes, 15:00 to 16:00 is 1 hour, 16:00 to 16:10 is 10 minutes. "
        "Altogether <b>1 hour 35 minutes</b>.</figcaption></figure>"
        + ex("Mixed times", "A school excursion leaves at 9:40 am and gets back at 14:15. How long is it?",
             "Change 9:40 am to 09:40. 09:40 to 10:00 is 20 minutes, 10:00 to 14:00 is 4 hours, 14:00 to 14:15 is 15 minutes.",
             "4 hours 35 minutes") +
        ex("Through midnight", "A New Year’s Eve harbour cruise leaves at 23:20 and lasts 1 hour 50 minutes. What time does it finish?",
           "23:20 + 40 minutes = 00:00 (midnight). 1 hour 50 minutes − 40 minutes = 1 hour 10 minutes. 00:00 + 1 hour 10 minutes = 01:10.",
           "01:10, which is 1:10 am") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3:45 pm written as 13:45", "Add 12, do not put a 1 in front: 3 + 12 = 15, so 15:45"],
            ["15:45 read as 5:45 pm", "Take away 12, do not drop the 1: 15 − 12 = 3, so 3:45 pm"],
            ["12:20 am written as 12:20", "Just after midnight is 00 in 24-hour time: 00:20"],
            ["12:20 pm written as 00:20 or 24:20", "Just after midday stays 12: 12:20"],
            ["7:05 am written as 7:05 in 24-hour time", "24-hour time has 4 digits: 07:05"],
            ["14:35 to 16:10 worked out as 1610 − 1435 = 1 hour 75 minutes", "Count on: 25 minutes + 1 hour + 10 minutes = 1 hour 35 minutes"],
        ])
    )


FAQ = [
    {"q": "When do students learn 24-hour time in Australia?",
     "a": "In the Australian Curriculum v9.0, Year 5 students compare the 12- and 24-hour time systems and convert between them to solve practical problems (AC9M5M03). They read analog clocks to the nearest minute from Year 3."},
    {"q": "How do you change 12-hour time into 24-hour time?",
     "a": "For am times keep the hour and write 4 digits, so 7:05 am is 07:05. For pm times add 12 to the hour, so 3:45 pm is 15:45. 12:20 pm stays 12:20 and 12:20 am becomes 00:20."},
    {"q": "Is midnight 00:00 or 24:00?",
     "a": "Midnight at the start of a day is written 00:00, so 12:20 am is 00:20. Some timetables write 24:00 for the very end of a day, but 00:00 is the usual way."},
    {"q": "Where is 24-hour time used in Australia?",
     "a": "You see 24-hour time on train and bus timetables, airline tickets and flight boards, TV guides, phones and in hospitals. Practising with real timetables helps students with NAPLAN-style time problems."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5)."""
    for s in sets:
        targets = [p for p in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
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
    USED.clear()
    USED.update(RESERVED)
    rnd = random.Random(5812)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_clocks(rnd, people), set_to24(rnd), set_to12(rnd, people), set_durations(rnd), set_problems(rnd, people)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    u = {
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "12-and-24-hour-time", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 12- and 24-Hour Time",
        "seo_title": "Year 5 12- and 24-Hour Time Worksheets: Converting Time, Durations and Timetables (Free, with Answer Key)",
        "short_title": "12- and 24-hour time",
        "domain": "Measurement",
        "standard_code": "AC9M5M03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Compare 12- and 24-hour time systems and solve practical problems involving the conversion between them",
        "meta_desc": "Free Year 5 maths worksheets on 12- and 24-hour time for the Australian Curriculum (AC9M5M03): read analog clocks to the minute, convert between am/pm and 24-hour time, work out how long events last and solve problems with Sydney train timetables, flights and TV guides. 100 questions with an answer key, great for NAPLAN practice.",
        "key_big": "pm: add 12 to the hour. 3:45 pm = 15:45.",
        "key_sub": "am times keep the hour with 4 digits (7:05 am = 07:05). 12:20 pm = 12:20, but 12:20 am = 00:20. An hour has 60 minutes, so count on to the next o’clock to work out how long.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "(timetable|time line|flight|TV guide)")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
