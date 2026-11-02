# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Time - 12- and 24-hour clock (National Curriculum in England, Measurement)
  python3 tools/gen_uk_maths_y4_time.py
Every clock picture is drawn from the time itself (the hour hand moves between the numbers).
Every answer is worked out in code from (hour, minute) values.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Oliver", "he"), ("Amelia", "she"), ("Harry", "he"), ("Isla", "she"), ("Mohammed", "he"), ("Freya", "she"),
          ("Jack", "he"), ("Poppy", "she"), ("Arjun", "he"), ("Ava", "she"), ("Noah", "he"), ("Aisha", "she"),
          ("George", "he"), ("Lily", "she"), ("Leo", "he"), ("Zara", "she"), ("Alfie", "he"), ("Grace", "she"),
          ("Kai", "he"), ("Ruby", "she"), ("Ethan", "he"), ("Maya", "she"), ("Charlie", "he"), ("Evie", "she")]


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


def words(h, m):
    """UK clock words: 20 past 7, 25 to 4, quarter to 9, 13 minutes past 6"""
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


def dur(n):
    """duration in hours and minutes: 1 hour 25 minutes"""
    assert n > 0
    hh, mm = divmod(n, 60)
    parts = []
    if hh:
        parts.append("%d hour%s" % (hh, "" if hh == 1 else "s"))
    if mm:
        parts.append("%d minute%s" % (mm, "" if mm == 1 else "s"))
    return " ".join(parts)


def mins(n):
    return "%d minute%s" % (n, "" if n == 1 else "s")


def dur_value(s):
    """minutes in a duration string (to make sure no two choices are equal)"""
    v = 0
    for num, unit in re.findall(r"(\d+) (hour|minute)", s):
        v += int(num) * (60 if unit == "hour" else 1)
    return v


def add(h, m, d):
    t = (h * 60 + m + d) % (24 * 60)
    return t // 60, t % 60


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, key=None):
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
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def clock_svg(h, m, size=200, inner24=False):
    c = size / 2.0
    R = c - 6
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='5'/>" % (c, c, R, GREEN)]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (13 if i % 5 == 0 else 7)
        seg = "M%.0f %.0fL%.0f %.0f" % (c + r1 * math.cos(a), c + r1 * math.sin(a), c + (R - 3) * math.cos(a), c + (R - 3) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='1.2'/>" % ("".join(small), LINE))
    s.append("<path d='%s' stroke='%s' stroke-width='2.6'/>" % ("".join(big), LINE))
    s.append("<g font-size='19' font-weight='700' fill='%s' text-anchor='middle'>" % LINE)
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        rn = R - 29
        s.append("<text x='%.0f' y='%.0f'>%d</text>" % (c + rn * math.cos(a), c + rn * math.sin(a) + 7, n))
    s.append("</g>")
    hl = 0.36 if inner24 else 0.5
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='8' stroke-linecap='round'/>"
             % (c, c, c + R * hl * math.cos(ah), c + R * hl * math.sin(ah), LINE))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4.5' stroke-linecap='round'/>"
             % (c, c, c + R * 0.8 * math.cos(am), c + R * 0.8 * math.sin(am), RED))
    s.append("<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (c, c, LINE))
    if inner24:   # 24-hour numbers on top of the hands, with a white edge so they stay readable
        s.append("<g font-size='14' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='3' "
                 "paint-order='stroke'>" % GREEN)
        for n in range(1, 13):
            a = math.radians(n * 30 - 90)
            rn = R - 54
            lab = "00" if n == 12 else str(n + 12)
            s.append("<text x='%.0f' y='%.0f'>%s</text>" % (c + rn * math.cos(a), c + rn * math.sin(a) + 5, lab))
        s.append("</g>")
    return svg_wrap(size, size, "".join(s), "clock showing %d:%02d" % (h12(h), m))


def timeline_svg(h1, m1, h2, m2, W=420):
    """Start -> next hour -> end, 24-hour labels, the jumps labelled."""
    t1, t2 = h1 * 60 + m1, h2 * 60 + m2
    mid = (h1 + 1) * 60 if m1 else None
    L, R, Y = 34, W - 34, 70
    def X(t):
        return L + (R - L) * (t - t1) / float(t2 - t1)
    pts = [t1] + ([mid] if mid and t1 < mid < t2 else []) + [t2]
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for t in pts:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X(t), Y - 10, X(t), Y + 10, LINE))
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X(t), Y + 32, LINE, t24(t // 60, t % 60)))
    for a, b in zip(pts, pts[1:]):
        x1, x2 = X(a), X(b)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, Y - 12, (x1 + x2) / 2, Y - 52, x2, Y - 12, RED))
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>+%d min</text>"
                 % ((x1 + x2) / 2, Y - 40, RED, b - a))
    return svg_wrap(W, 112, "".join(s), "time line from %s to %s" % (t24(h1, m1), t24(h2, m2)))


def timetable_svg(title, head, stops, cols):
    """cols: list of columns, each a list of (h, m) for every stop."""
    LW, CW, RH = 150, 72, 30
    W = LW + CW * len(cols) + 4
    H = RH * (len(stops) + 1) + 4
    s = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (W - 4, RH, GREEN)]
    s.append("<text x='10' y='%d' font-size='15' font-weight='700' fill='#fff'>%s</text>" % (2 + 21, title))
    for j in range(len(cols)):
        s.append("<text x='%.0f' y='%d' font-size='15' font-weight='700' fill='#fff' text-anchor='middle'>%s %d</text>"
                 % (2 + LW + CW * j + CW / 2.0, 2 + 21, head, j + 1))
    for i, st in enumerate(stops):
        y = 2 + RH * (i + 1)
        if i % 2:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
        s.append("<text x='10' y='%d' font-size='16' fill='%s'>%s</text>" % (y + 21, LINE, st.replace("the ", "")))
        for j, col in enumerate(cols):
            s.append("<text x='%.0f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (2 + LW + CW * j + CW / 2.0, y + 21, LINE, t24(*col[i])))
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, LINE))
    for j in range(len(cols)):
        x = 2 + LW + CW * j
        s.append("<line x1='%d' y1='2' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, x, H - 2, LINE))
    return svg_wrap(W, H, "".join(s), "timetable: %s" % title.lower())


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
        mm = "The minute hand points to <b>12</b>, so it is exactly on the hour."
    elif extra == 0:
        mm = "The minute hand points to <b>%d</b>: %d × 5 = <b>%d minutes</b> past." % (n, n, m)
    elif n == 0:
        mm = "The minute hand is <b>%d small mark%s</b> past the 12: <b>%d minute%s</b> past." % (extra, "" if extra == 1 else "s", m, "" if m == 1 else "s")
    else:
        mm = ("The minute hand is %d small mark%s past the %d. Count in 5s to the %d (%d), then on in 1s: <b>%d minutes</b> past."
              % (extra, "" if extra == 1 else "s", n, n, n * 5, m))
    if m == 0:
        hh = "The hour hand points to <b>%d</b>." % h
    else:
        hh = "The hour hand is between <b>%d</b> and <b>%d</b>, so the hour is still <b>%d</b>." % (h, h % 12 + 1, h)
    return hh + " " + mm


# ============================================================ set 1: clocks in words
def set_words(rnd):
    its = []
    times = []
    fives = [15, 30, 45, 20, 50, 10, 35, 25, 40, 5, 55]
    rnd.shuffle(fives)
    hours = list(range(1, 13))
    rnd.shuffle(hours)
    for i, m in enumerate([15, 30, 45] + [x for x in fives if x not in (15, 30, 45)][:5]):
        times.append((hours[i], m))
    odd = [x for x in range(2, 59) if x % 5 and x not in (29, 31)]
    rnd.shuffle(odd)
    lows = [x for x in odd if x < 30][:6]
    highs = [x for x in odd if x > 30][:6]
    hrs2 = list(range(1, 13))
    rnd.shuffle(hrs2)
    for i, m in enumerate([v for pair in zip(lows, highs) for v in pair]):
        times.append((hrs2[i], m))
    for h, m in times:
        right = words(h, m)
        n = m // 5
        c = []
        if m < 30:
            c.append(words(h + 1, m))                    # hour hand read as the next number
            c.append(words(h - 1, 60 - m))               # "past" and "to" mixed up: 20 to 7
            if n:
                c.append(words(h, n))                    # minute number read as minutes: 4 minutes past 7
            c.append(words(h, 60 - m))                   # "to" with the wrong hour
            c.append(words(h, m + 5))
        else:
            c.append(words(h - 1, m))                    # "to" the hour just gone: 10 to 2 for 2:50
            c.append(words(h + 1, 60 - m))               # "past" and "to" mixed up: 10 past 3
            c.append(words(h, 60 - m))                   # 10 past 2
            if n and n != 60 - m:
                c.append(words(h, n))                    # minute number read as minutes
            c.append(words(h, m - 5))
        if m == 30:
            c = [words(h + 1, 30), words(h, 6), words(h - 1, 30), words(h, 45)]
        if m == 15:
            c = [words(h - 1, 45), words(h, 3), words(h + 1, 15), words(h, 45)]
        if m == 45:
            c = [words(h - 1, 45), words(h, 9), words(h, 15), words(h + 1, 15)]
        hh = h12(h)
        if m <= 30:
            e = ("%s The minute hand is on the right-hand side, so we say <b>past %d</b>. It is <b>%s</b>."
                 % (hand_text(h, m), hh, right))
        else:
            e = ("%s That is %d minutes before %d o’clock (60 − %d = %d). The minute hand is on the left-hand side, so we say "
                 "<b>to %d</b>. It is <b>%s</b>." % (hand_text(h, m), 60 - m, hh % 12 + 1, m, 60 - m, hh % 12 + 1, right))
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show?", right, c, e, rnd))
    return {"title": "Read the clock in words", "items": its}


# ============================================================ set 2: analogue to 12-hour digital (am / pm)
CONTEXTS = [  # sentence, possible hours (24-hour), minutes from, minutes to
    ("{n} wakes up in the morning.", [6, 7], 0, 59),
    ("{n} eats breakfast before school.", [7], 10, 50),
    ("School starts in the morning.", [8], 40, 55),
    ("{n} has morning break.", [10], 15, 40),
    ("{n} has lunch at school.", [12], 5, 50),
    ("{n} has PE in the afternoon.", [13, 14], 0, 59),
    ("School finishes in the afternoon.", [15], 10, 25),
    ("{n} goes to football practice after school.", [16], 5, 55),
    ("{n} has tea in the evening.", [17], 10, 50),
    ("{n} has a bath in the evening.", [18], 5, 55),
    ("{n} goes to bed in the evening.", [19, 20], 0, 45),
    ("{n} goes swimming on Saturday morning.", [9, 10], 0, 59),
    ("{n}’s baby brother wakes up in the night.", [2, 3], 0, 59),
    ("{n} watches a film on Sunday afternoon.", [14], 0, 59),
]


def set_digital(rnd, people):
    its = []
    ctx = CONTEXTS[:]
    rnd.shuffle(ctx)
    for i, (sent, hrs, lo, hi) in enumerate(ctx):
        H = rnd.choice(hrs)
        if i < 5:
            m = rnd.choice([x for x in range(lo, hi + 1) if x % 5 == 0])
        else:
            m = rnd.choice([x for x in range(lo, hi + 1) if x % 5 and x not in (1, 59)])
        n = m // 5
        nm = next(people)[0]
        right = tm12(H, m)
        c = [tm12(H + 12, m)]                            # am and pm mixed up
        if m >= 35:
            c.append(tm12(H + 1, 60 - m))                # "13 to 4" written as 4:13
        if n and n != m:
            c.append(tm12(H, n))                         # minute number read as minutes
        c += [tm12(H + 1, m), tm12(H + 13, m), tm12(H, (m + 5) % 60)]
        ap = "am" if H < 12 else "pm"
        why = ("Times from midnight to noon are <b>am</b>." if ap == "am" else "Times from noon to midnight are <b>pm</b>.")
        e = "%s %s So it is <b>%s</b>." % (hand_text(H, m), why, right)
        q = fig(clock_svg(H, m)) + sent.format(n=nm) + " What is the time in 12-hour digital time?"
        its.append(mcq(q, right, c, e, rnd))
    # words to 12-hour digital
    word_qs = [(15, 35, "in the afternoon"), (8, 45, "in the morning"), (19, 20, "in the evening"),
               (11, 50, "in the morning"), (16, 55, "in the afternoon"), (21, 10, "at night")]
    rnd.shuffle(word_qs)
    for H, m, part in word_qs:
        w = words(H, m)
        right = tm12(H, m)
        if m > 30:
            c = [tm12(H + 1, 60 - m), tm12(H + 1, m), tm12(H, 60 - m), tm12(H + 12, m)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d:%02d. "
                 "%s means %s, so it is <b>%s</b>." % (w, 60 - m, h12(H + 1), 60 - m, m, h12(H), m, part[0].upper() + part[1:], "am" if H < 12 else "pm", right))
        else:
            c = [tm12(H - 1, 60 - m), tm12(H + 12, m), tm12(H, m + 5), tm12(H + 1, m)]
            e = ("“%s” means %d minutes <b>after</b> %d o’clock: %d:%02d. %s means %s, so it is <b>%s</b>."
                 % (w, m, h12(H), h12(H), m, part[0].upper() + part[1:], "am" if H < 12 else "pm", right))
        its.append(mcq("Write <b>%s %s</b> as a 12-hour digital time." % (w, part), right, c, e, rnd))
    return {"title": "Analogue clocks to digital time (am and pm)", "items": its}


# ============================================================ set 3: 12-hour and 24-hour clock
def set_convert(rnd):
    its = []
    seen = set()

    def free(hrs, h):
        if (tuple(hrs), h) in seen:
            return False
        seen.add((tuple(hrs), h))
        return True

    def pick(hrs, five=True):
        while True:
            h = rnd.choice(hrs)
            m = rnd.choice(range(5, 56, 5)) if five else rnd.choice([x for x in range(1, 59) if x % 5])
            if free(hrs, h):
                return h, m

    # A: pm -> 24-hour
    for k in range(4):
        H, m = pick([13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], five=k < 2)
        right = t24(H, m)
        c = [t24(H - 2, m), "%02d:%02d" % (H - 12, m), t24(H - 1, m), t24(H + 1, m)]
        e = ("pm times are after noon. Add 12 to the hour: %d + 12 = %d. So %s is <b>%s</b>."
             % (H - 12, H, tm12(H, m), right))
        its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(H, m), right, c, e, rnd))
    # B: am -> 24-hour
    for k in range(2):
        H, m = pick([6, 7, 8, 9, 10, 11] if k else [6, 7, 8, 9], five=k == 0)
        right = t24(H, m)
        c = [t24(H + 12, m), t24(H + 10, m), t24(H + 1, m)]
        e = ("am times are before noon, so the hour stays the same. A 24-hour time always has 4 digits, so put a 0 in front "
             "of a 1-digit hour. %s is <b>%s</b>." % (tm12(H, m), right) if H < 10 else
             "am times are before noon, so the hour stays the same. %s is <b>%s</b>." % (tm12(H, m), right))
        its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(H, m), right, c, e, rnd))
    # C: 24-hour -> pm
    for k in range(4):
        H, m = pick([13, 14, 15, 16, 17, 18, 19, 20, 21, 22], five=k < 2)
        right = tm12(H, m)
        c = []
        if H - 10 <= 12:
            c.append("%d:%02d pm" % (H - 10, m))         # 15:45 -> 5:45 pm (just drop the 1)
        c += [tm12(H - 12, m), tm12(H + 1, m), tm12(H - 1, m)]
        e = ("Hours from 13 to 23 are pm. Take away 12: %d − 12 = %d. So %s is <b>%s</b>."
             % (H, H - 12, t24(H, m), right))
        its.append(mcq("Write <b>%s</b> as a 12-hour time." % t24(H, m), right, c, e, rnd))
    # midnight and noon
    m = rnd.choice([10, 20, 25, 35, 40])
    its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(0, m), t24(0, m),
                   ["12:%02d" % m, "24:%02d" % m, "01:%02d" % m],
                   "12 am is the hour just after <b>midnight</b>. In 24-hour time midnight is 00:00, so %s is <b>%s</b>."
                   % (tm12(0, m), t24(0, m)), rnd))
    m2 = rnd.choice([x for x in [5, 15, 30, 45, 50] if x != m])
    its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(12, m2), t24(12, m2),
                   ["24:%02d" % m2, "00:%02d" % m2, "13:%02d" % m2],
                   "12 pm is the hour just after <b>noon</b>. Noon is 12:00 in 24-hour time, so do not add 12. "
                   "%s is <b>%s</b>." % (tm12(12, m2), t24(12, m2)), rnd))
    m3 = rnd.choice([x for x in [5, 15, 20, 30, 45] if x not in (m, m2)])
    its.append(mcq("Write <b>%s</b> as a 12-hour time." % t24(0, m3), tm12(0, m3),
                   [tm12(12, m3), "0:%02d am" % m3, tm12(23, m3)],
                   "00 is the hour just after <b>midnight</b>. In 12-hour time we call it 12 am. %s is <b>%s</b>."
                   % (t24(0, m3), tm12(0, m3)), rnd))
    H, m = pick([6, 7, 8, 9])
    its.append(mcq("Write <b>%s</b> as a 12-hour time." % t24(H, m), tm12(H, m),
                   [tm12(H + 12, m), "%d:%02d pm" % (H + 2, m), tm12(H + 10, m)],
                   "The hour %02d is less than 12, so it is a morning time: <b>am</b>. Drop the 0 at the front: <b>%s</b>."
                   % (H, tm12(H, m)), rnd))
    # E: words -> 24-hour
    for H, m, part in [(15, 45, "in the afternoon"), (15, 35, "in the afternoon"), (21, 20, "in the evening")]:
        w = words(H, m)
        right = t24(H, m)
        if m > 30:
            c = [t24(H + 1, m), t24(H + 1, 60 - m), "%02d:%02d" % (H - 12, m), t24(H, 60 - m)]
            e = ("“%s” is %d minutes before %d o’clock: %d:%02d %s. Add 12 to the hour: <b>%s</b>."
                 % (w, 60 - m, h12(H + 1), h12(H), m, "pm", right))
        else:
            c = ["%02d:%02d" % (H - 12, m), t24(H - 2, m), t24(H - 1, 60 - m), t24(H, m + 10)]
            e = ("“%s” is %d:%02d pm. Add 12 to the hour: %d + 12 = %d. So it is <b>%s</b>."
                 % (w, h12(H), m, h12(H), H, right))
        its.append(mcq("Which 24-hour time is <b>%s %s</b>?" % (w, part), right, c, e, rnd))
    # clock -> 24-hour
    for k, (sent, hrs) in enumerate([("The clock shows a time in the evening.", [18, 19, 20]),
                                     ("The clock shows a time in the afternoon.", [13, 14, 15, 16]),
                                     ("The clock shows a time in the evening.", [21, 22])]):
        H, m = pick(hrs, five=k == 0)
        n = m // 5
        right = t24(H, m)
        c = ["%02d:%02d" % (H - 12, m), t24(H - 2, m)]
        if n and n != m:
            c.append(t24(H, n))
        c += [t24(H + 1, m), t24(H, (m + 5) % 60)]
        e = ("%s It is %d:%02d pm. Add 12 to the hour: %d + 12 = %d. So it is <b>%s</b>."
             % (hand_text(H, m), h12(H), m, h12(H), H, right))
        its.append(mcq(fig(clock_svg(H, m)) + sent + " Write it in 24-hour time.", right, c, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "12-hour and 24-hour clock", "items": its}


# ============================================================ set 4: durations and converting units
def set_durations(rnd):
    its = []
    # simple conversions
    h = rnd.randint(2, 5)
    its.append(mcq("How many minutes are in <b>%d hours</b>?" % h, str(60 * h), [str(100 * h), str(10 * h), str(60 + h)],
                   "1 hour = 60 minutes. %d × 60 = <b>%d minutes</b>." % (h, 60 * h), rnd))
    n = rnd.choice([x for x in range(2, 7) if x != h])
    its.append(mcq("How many seconds are in <b>%d minutes</b>?" % n, str(60 * n), [str(100 * n), str(10 * n), str(60 + n)],
                   "1 minute = 60 seconds. %d × 60 = <b>%d seconds</b>." % (n, 60 * n), rnd))
    y = rnd.randint(2, 6)
    its.append(mcq("How many months are in <b>%d years</b>?" % y, str(12 * y), [str(10 * y), str(12 + y), str(52 * y)],
                   "1 year = 12 months. %d × 12 = <b>%d months</b>." % (y, 12 * y), rnd))
    w = rnd.choice([x for x in range(3, 10) if x != y])
    its.append(mcq("How many days are in <b>%d weeks</b>?" % w, str(7 * w), [str(5 * w), str(7 + w), str(10 * w)],
                   "1 week = 7 days. %d × 7 = <b>%d days</b>." % (w, 7 * w), rnd))
    # mixed units to the smaller unit
    h, m = rnd.randint(1, 3), rnd.choice([10, 15, 20, 25, 40, 45])
    its.append(mcq("<b>%s %d minutes</b> = ? minutes" % ("%d hour%s" % (h, "" if h == 1 else "s"), m), str(60 * h + m),
                   ["%d%02d" % (h, m), str(60 * h), str(60 * (h + 1) + m), str(60 + m)],
                   "%d × 60 = %d minutes. Then add the %d minutes: %d + %d = <b>%d minutes</b>."
                   % (h, 60 * h, m, 60 * h, m, 60 * h + m), rnd))
    n, s = rnd.randint(2, 4), rnd.choice([10, 15, 30, 35, 50])
    its.append(mcq("<b>%d minutes %d seconds</b> = ? seconds" % (n, s), str(60 * n + s),
                   ["%d%02d" % (n, s), str(60 * n), str(60 * (n + 1) + s), str(60 + s)],
                   "%d × 60 = %d seconds. Then add the %d seconds: %d + %d = <b>%d seconds</b>."
                   % (n, 60 * n, s, 60 * n, s, 60 * n + s), rnd))
    # to the bigger unit with a remainder
    tot = rnd.choice([75, 90, 110, 130, 150, 170])
    a, b = divmod(tot, 60)
    c = ["%s" % dur(60 * (tot // 100) + tot % 100) if tot % 100 < 60 and tot >= 100 else None,
         dur(60 * a + b + 60), dur(60 * a + (b + 10) % 60) if b + 10 < 60 else None, dur(tot - 60) if tot > 60 else None,
         dur(tot + 10)]
    its.append(mcq("<b>%d minutes</b> = ?" % tot, dur(tot), c,
                   "60 minutes make 1 hour. %d = %s, so %d minutes = <b>%s</b>."
                   % (tot, " + ".join(["60"] * a + ([str(b)] if b else [])), tot, dur(tot)), rnd, key=dur_value))
    secs = rnd.choice([130, 150, 200, 210, 250])
    a, b = divmod(secs, 60)

    def mmss(v):
        p, q = divmod(v, 60)
        return "%d minute%s %d seconds" % (p, "" if p == 1 else "s", q) if q else "%d minutes" % p
    wrong100 = 60 * (secs // 100) + secs % 100 if secs % 100 < 60 else None
    its.append(mcq("<b>%d seconds</b> = ?" % secs, mmss(secs),
                   [mmss(wrong100) if wrong100 else None, mmss(secs + 60), mmss(secs - 60), mmss(secs + 10)],
                   "60 seconds make 1 minute. %d × 60 = %d, and %d − %d = %d. So %d seconds = <b>%s</b>."
                   % (a, 60 * a, secs, 60 * a, b, secs, mmss(secs)), rnd))
    mo = rnd.choice([30, 42, 51])
    a, b = divmod(mo, 12)

    def ym(v):
        p, q = divmod(v, 12)
        return "%d year%s %d month%s" % (p, "" if p == 1 else "s", q, "" if q == 1 else "s") if q else "%d years" % p
    its.append(mcq("<b>%d months</b> = ?" % mo, ym(mo), [ym(12 * (mo // 10) + mo % 10), ym(mo + 12), ym(mo - 12), ym(mo + 2)],
                   "12 months make 1 year. %d × 12 = %d, and %d − %d = %d. So %d months = <b>%s</b>. "
                   "(Do not split by 10: a year has 12 months.)" % (a, 12 * a, mo, 12 * a, b, mo, ym(mo)), rnd))
    dd = rnd.choice([17, 23, 26, 31])
    a, b = divmod(dd, 7)

    def wd(v):
        p, q = divmod(v, 7)
        return "%d week%s %d day%s" % (p, "" if p == 1 else "s", q, "" if q == 1 else "s") if q else "%d weeks" % p
    its.append(mcq("<b>%d days</b> = ?" % dd, wd(dd), [wd(7 * (dd // 10) + dd % 10), wd(dd + 7), wd(dd - 7), wd(dd + 1)],
                   "7 days make 1 week. %d × 7 = %d, and %d − %d = %d. So %d days = <b>%s</b>."
                   % (a, 7 * a, dd, 7 * a, b, dd, wd(dd)), rnd))

    # durations between 24-hour times
    seen = set()
    k = 0
    while k < 10:
        if k < 3:                                        # inside one hour
            h1 = rnd.randint(8, 19)
            m1 = rnd.choice(range(5, 31, 5))
            d = rnd.choice(range(15, 60 - m1, 5))
        elif k < 7:                                      # crosses the hour
            h1 = rnd.randint(8, 19)
            m1 = rnd.choice([35, 40, 45, 50, 55]) if k < 5 else rnd.choice([x for x in range(32, 58) if x % 5])
            d = 60 - m1 + rnd.choice(range(5, 31, 5) if k < 5 else range(3, 30))
        else:                                            # more than an hour
            h1 = rnd.randint(8, 17)
            m1 = rnd.choice(range(10, 56, 5))
            d = rnd.choice([65, 75, 80, 85, 95, 100, 110])
        tier = 0 if k < 3 else 1 if k < 7 else 2
        if (tier, h1) in seen:
            continue
        seen.add((tier, h1))
        h2, m2 = add(h1, m1, d)
        q = "How long is it from <b>%s</b> to <b>%s</b>?" % (t24(h1, m1), t24(h2, m2))
        if k in (3, 7):
            jumps = [60 - m1, d - (60 - m1)]
            if min(jumps) * 352.0 / d < 56:              # keep the time line labels apart
                seen.discard((tier, h1))
                continue
            q = fig(timeline_svg(h1, m1, h2, m2)) + q
        naive100 = (h2 * 100 + m2) - (h1 * 100 + m1)
        c = []
        if h2 != h1 and naive100 < 100:
            c.append("%d minutes" % naive100)            # counted 100 minutes in an hour
        if d >= 60:
            c.append(dur(60 * (h2 - h1) + abs(m2 - m1)) if m2 != m1 else None)
        c.append(mins(abs(m2 - m1)) if m2 != m1 else None)
        c += [dur(d + 10), dur(d - 5), dur(d + 5), dur(d + 60) if d < 60 else dur(d - 60)]
        to_hour = 60 - m1
        if h2 == h1:
            e = "Both times are in the same hour. %d − %d = <b>%s</b>." % (m2, m1, mins(d))
        else:
            e = ("Count on to the next hour first: %s to %s is %d minutes. Then %s to %s is %d minutes. "
                 "%d + %d = <b>%s</b>. (An hour has 60 minutes, not 100, so do not just subtract the numbers.)"
                 % (t24(h1, m1), t24(h1 + 1, 0), to_hour, t24(h1 + 1, 0), t24(h2, m2), d - to_hour, to_hour, d - to_hour,
                    mins(d) if d < 60 else "%d minutes = %s" % (d, dur(d))))
        its.append(mcq(q, dur(d), c, e, rnd, key=dur_value))
        k += 1
    return {"title": "Durations and time conversions", "items": its}


# ============================================================ set 5: timetables and time problems
def make_table(rnd, first_h, first_m, gap, legs):
    cols = []
    for j in range(4):
        h0, m0 = add(first_h, first_m, gap * j)
        cols.append([add(h0, m0, l) for l in legs])
    return cols


def tmin(t):
    return t[0] * 60 + t[1]


def timetable_qs(rnd, people, title, head, word, stops, cols, legs):
    its = []
    svg = fig(timetable_svg(title, head, stops, cols))
    S = stops
    Sr = [x.replace("the ", "") for x in stops]
    # 1 arrival
    j = rnd.choice([1, 2])
    right = t24(*cols[j][3])
    c = [t24(*cols[j][2]), t24(*cols[j + 1][3]), t24(*cols[j - 1][3]), t24(*cols[j][1])]
    its.append(mcq(svg + "The %s leaves <b>%s</b> at %s. What time does it get to <b>%s</b>?" % (word, S[0], t24(*cols[j][0]), S[3]),
                   right, c, "Find %s in the %s row. Go down that column to the %s row: <b>%s</b>." % (t24(*cols[j][0]), Sr[0], Sr[3], right), rnd))
    # 2 which one leaves
    j2 = 3 if j != 3 else 0
    right = t24(*cols[j2][0])
    c = [t24(*cols[j2][1]), t24(*cols[j2 - 1][0]), t24(*cols[(j2 + 1) % 4][0]), t24(*cols[j2][2])]
    its.append(mcq(svg + "A %s gets to <b>%s</b> at %s. What time did it leave <b>%s</b>?" % (word, S[2], t24(*cols[j2][2]), S[0]),
                   right, c, "Find %s in the %s row. Go up that column to the %s row: <b>%s</b>." % (t24(*cols[j2][2]), Sr[2], Sr[0], right), rnd))
    # 3 journey time (crosses the hour)
    jj = [x for x in range(4) if cols[x][0][0] != cols[x][3][0]]
    j3 = rnd.choice(jj)
    a, b = cols[j3][0], cols[j3][3]
    d = tmin(b) - tmin(a)
    naive = (b[0] * 100 + b[1]) - (a[0] * 100 + a[1])
    c = ["%d minutes" % naive if naive < 100 else None, mins(legs[2]), dur(d + 10), mins(abs(b[1] - a[1])) if b[1] != a[1] else None, dur(d - 5)]
    e = ("%s to %s is %d minutes. %s to %s is %d minutes. %d + %d = <b>%s</b>."
         % (t24(*a), t24(a[0] + 1, 0), 60 - a[1], t24(a[0] + 1, 0), t24(*b), b[1], 60 - a[1], b[1], dur(d)))
    its.append(mcq(svg + "How long does the %s that leaves <b>%s</b> at %s take to get to <b>%s</b>?" % (word, S[0], t24(*a), S[3]),
                   dur(d), c, e, rnd, key=dur_value))
    # 4 latest one to be on time
    nm, pr = next(people)
    j4 = rnd.choice([1, 2])
    lim = add(cols[j4][3][0], cols[j4][3][1], rnd.choice([3, 5, 7]))
    while tmin(lim) % 5:
        lim = add(lim[0], lim[1], 1)
    assert tmin(cols[j4][3]) <= tmin(lim) < tmin(cols[j4 + 1][3])
    right = t24(*cols[j4][1])
    c = [t24(*cols[j4 + 1][1]), t24(*cols[j4 - 1][1]), t24(*cols[j4][0]), t24(*cols[j4][3])]
    e = ("Look along the %s row for the last time that is not after %s: %s. Go up that column to %s: <b>%s</b>. "
         "The next %s gets to %s at %s, which is too late."
         % (Sr[3], t24(*lim), t24(*cols[j4][3]), S[1], right, word, S[3], t24(*cols[j4 + 1][3])))
    its.append(mcq(svg + "%s must be at <b>%s</b> by %s. What is the latest %s %s can catch from <b>%s</b>?"
                   % (nm, S[3], t24(*lim), word, pr, S[1]), right, c, e, rnd))
    # 5 waiting time
    nm, pr = next(people)
    j5 = rnd.choice([0, 1, 2])
    arr = add(cols[j5][1][0], cols[j5][1][1], rnd.choice([4, 6, 8, 9]))
    wait = tmin(cols[j5 + 1][1]) - tmin(arr)
    gap = tmin(cols[1][0]) - tmin(cols[0][0])
    naive = (cols[j5 + 1][1][0] * 100 + cols[j5 + 1][1][1]) - (arr[0] * 100 + arr[1])
    c = [mins(gap), "%d minutes" % naive if naive != wait and naive < 100 else None, mins(wait + 5), mins(wait - 4), mins(wait + 10)]
    e = ("The %s at %s has gone. The next %s from %s is at %s. From %s to %s is <b>%s</b>."
         % (word, t24(*cols[j5][1]), word, S[1], t24(*cols[j5 + 1][1]), t24(*arr), t24(*cols[j5 + 1][1]), mins(wait)))
    its.append(mcq(svg + "%s gets to <b>%s</b> at %s, just after a %s has left. How long must %s wait for the next one?"
                   % (nm, S[1], t24(*arr), word, pr), mins(wait), c, e, rnd, key=dur_value))
    # 6 12-hour time on the timetable
    nm, pr = next(people)
    j6 = rnd.choice([x for x in range(4) if cols[x][2][0] > 12 or cols[x][2][0] < 12])
    t = cols[j6][2]
    right = t24(*t)
    if t[0] >= 13:
        c = ["%02d:%02d" % (t[0] - 12, t[1]), t24(t[0] - 2, t[1]), t24(*cols[j6][1]), t24(t[0] + 1, t[1])]
        e = "%s is in the afternoon or evening, so add 12 to the hour: %d + 12 = %d. Look for <b>%s</b> in the %s row." % (
            tm12(*t), t[0] - 12, t[0], right, Sr[2])
    else:
        c = [t24(t[0] + 12, t[1]), t24(t[0] + 10, t[1]), t24(*cols[j6][1]), t24(t[0] + 1, t[1])]
        e = "%s is in the morning, so the hour stays the same. Write it with 4 digits: <b>%s</b>." % (tm12(*t), right)
    its.append(mcq(svg + "%s’s %s gets to <b>%s</b> at %s. Which time on the timetable is this?" % (nm, word, S[2], tm12(*t)),
                   right, c, e, rnd))
    return its


def daily_problems(rnd, people):
    out = []
    nm, pr = next(people)
    out.append(mcq("Tea is at <b>17:30</b>. A pie takes <b>45 minutes</b> to cook. What time must it go in the oven?", "16:45",
                   ["18:15", "17:15", "16:35", "17:45"],
                   "Count back 30 minutes to 17:00. Then count back 15 more minutes: <b>16:45</b>.", rnd))
    nm, pr = next(people)
    out.append(mcq("A film starts at <b>18:50</b> and lasts <b>1 hour 35 minutes</b>. What time does it finish?", "20:25",
                   ["19:25", "20:35", "21:25", "20:15"],
                   "18:50 + 1 hour = 19:50. Then add 35 minutes: 10 minutes to 20:00, then 25 more minutes: <b>20:25</b>.", rnd))
    out.append(mcq("%s’s holiday lasts <b>3 weeks 4 days</b>. How many days is that?" % nm, "25",
                   ["34", "7", "28", "21"],
                   "3 weeks = 3 × 7 = 21 days. 21 + 4 = <b>25 days</b>.", rnd))
    nm, pr = next(people)
    out.append(mcq("%s is <b>8 years 7 months</b> old. How old is %s in months?" % (nm, pr), "103",
                   ["87", "96", "15", "91"],
                   "8 years = 8 × 12 = 96 months. 96 + 7 = <b>103 months</b>.", rnd))
    nm, pr = next(people)
    out.append(mcq("%s goes to bed at <b>19:30</b>. %s reads for <b>25 minutes</b> before bed. What time does %s start reading?"
                   % (nm, pr.capitalize(), pr), "19:05", ["19:55", "18:05", "19:15", "18:55"],
                   "Count back 25 minutes from 19:30: 19:30 − 25 minutes = <b>19:05</b>.", rnd))
    nm, pr = next(people)
    out.append(mcq("A song lasts <b>3 minutes 40 seconds</b>. How many seconds is that?", "220",
                   ["340", "180", "120", "43"],
                   "3 minutes = 3 × 60 = 180 seconds. 180 + 40 = <b>220 seconds</b>.", rnd))
    nm, pr = next(people)
    out.append(mcq("School starts at <b>8:45 am</b> and finishes at <b>3:15 pm</b>. How long is the school day?",
                   "6 hours 30 minutes", ["5 hours 30 minutes", "7 hours 30 minutes", "6 hours", "5 hours"],
                   "8:45 am to 2:45 pm is 6 hours. 2:45 pm to 3:15 pm is 30 minutes. 6 hours + 30 minutes = <b>6 hours 30 minutes</b>.",
                   rnd, key=dur_value))
    nm, pr = next(people)
    out.append(mcq("%s has a <b>45-minute</b> swimming lesson every week. How long does %s swim in <b>4 weeks</b>?" % (nm, pr),
                   "3 hours", ["1 hour 80 minutes", "2 hours 45 minutes", "4 hours 45 minutes", "1 hour 30 minutes"],
                   "4 × 45 = 180 minutes. 60 minutes make 1 hour, so 180 minutes = 3 × 60 = <b>3 hours</b>.", rnd, key=dur_value))
    return out


def set_timetables(rnd, people):
    bus_legs = [0, rnd.choice([10, 12, 13]), 0, 0]
    bus_legs[2] = bus_legs[1] + rnd.choice([11, 13, 14])
    bus_legs[3] = bus_legs[2] + rnd.choice([12, 15, 16])
    bh, bm = 15, rnd.choice([25, 30, 35, 40])
    bus = make_table(rnd, bh, bm, 30, bus_legs)
    train_legs = [0, rnd.choice([8, 9, 11]), 0, 0]
    train_legs[2] = train_legs[1] + rnd.choice([12, 14, 17])
    train_legs[3] = train_legs[2] + rnd.choice([16, 18, 21])
    tm_ = rnd.choice([20, 25, 35])
    train = make_table(rnd, 7, tm_, 20, train_legs)
    its = timetable_qs(rnd, people, "Bus stop", "Bus", "bus", ["the Bus Station", "Market Square", "the Library", "Park Road"], bus, bus_legs)
    daily = daily_problems(rnd, people)
    its += daily[:4]
    its += timetable_qs(rnd, people, "Station", "Train", "train", ["Oakfield", "Bridgeton", "Hillside", "City Centre"], train, train_legs)
    its += daily[4:]
    assert len(its) == 20
    return {"title": "Timetables and time problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Analogue clocks: past and to</h2>"
        "<p>The <b>hour hand</b> is short. The <b>minute hand</b> is long. When the minute hand is on the right-hand side, "
        "say minutes <b>past</b> the hour. When it is on the left-hand side, say minutes <b>to</b> the next hour.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 40, size=230) +
        "<figcaption>The minute hand shows 40 minutes. 60 − 40 = 20, so this is <b>20 to 4</b> (3:40).</figcaption></figure>"
        + table(["Time", "We say"], [["7:15", "quarter past 7"], ["7:20", "20 past 7"], ["7:30", "half past 7"],
                                     ["7:35", "25 to 8"], ["7:45", "quarter to 8"], ["7:52", "8 minutes to 8"]]) +
        "<h2>12-hour time: am and pm</h2>"
        "<p>A day has 24 hours, but a clock face only shows 12. So we write <b>am</b> for times from midnight to noon "
        "(night and morning) and <b>pm</b> for times from noon to midnight (afternoon and evening).</p>"
        + ex("Analogue to digital", "The clock shows 20 to 4 in the afternoon. Write it as a 12-hour time.",
             "20 to 4 is 40 minutes past 3. It is the afternoon, so it is pm.", "3:40 pm") +
        "<h2>24-hour time</h2>"
        "<p>The 24-hour clock counts the hours from 00 to 23, so you do not need am or pm. It always has <b>4 digits</b>: "
        "07:30, 15:45. Bus and train timetables use it.</p>"
        "<figure class='sn-fig'>" + clock_svg(15, 45, size=230, inner24=True) +
        "<figcaption>The green numbers show the afternoon hours. The hour after 12 is 13, so this clock shows 15:45 (3:45 pm).</figcaption></figure>"
        + table(["12-hour", "24-hour", "Rule"], [
            ["7:30 am", "07:30", "am: keep the hour, write 4 digits"],
            ["12:00 noon", "12:00", "12 pm: keep 12"],
            ["3:45 pm", "15:45", "pm: add 12 (3 + 12 = 15)"],
            ["9:10 pm", "21:10", "pm: add 12 (9 + 12 = 21)"],
            ["12:20 am", "00:20", "just after midnight: 00"],
        ]) +
        "<p>To go back from 24-hour to 12-hour time, take away 12 from hours 13 to 23: 18:05 is 6:05 pm.</p>"
        "<h2>How long? Count on in jumps</h2>"
        "<p>An hour has 60 minutes, not 100, so do not just subtract the numbers. Jump to the next o’clock first, then to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(14, 35, 15, 10) +
        "<figcaption>14:35 to 15:00 is 25 minutes. 15:00 to 15:10 is 10 minutes. 25 + 10 = 35 minutes.</figcaption></figure>"
        + ex("Read a timetable", "A bus leaves the Bus Station at 15:40 and gets to Park Road at 16:18. How long is the journey?",
             "15:40 to 16:00 is 20 minutes. 16:00 to 16:18 is 18 minutes. 20 + 18 = 38.", "38 minutes") +
        "<h2>Converting units of time</h2>"
        + table(["Bigger unit", "Smaller unit"], [["1 minute", "60 seconds"], ["1 hour", "60 minutes"], ["1 day", "24 hours"],
                                                  ["1 week", "7 days"], ["1 year", "12 months"]]) +
        "<p>Bigger unit to smaller unit: <b>multiply</b>. For mixed units, add the extra part.</p>"
        + ex("Hours to minutes", "2 hours 15 minutes = ? minutes", "2 × 60 = 120. 120 + 15 = 135.", "135 minutes")
        + ex("Days to weeks", "23 days = ? weeks and days", "3 × 7 = 21. 23 − 21 = 2.", "3 weeks 2 days")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3:45 pm written as 13:45 or 03:45", "pm: add 12 to the hour. 3 + 12 = 15, so 15:45"],
            ["15:45 read as 5:45 pm", "Take away 12, do not just drop the 1. 15 − 12 = 3, so 3:45 pm"],
            ["12:20 am written as 12:20", "Just after midnight is 00 in 24-hour time: 00:20"],
            ["Minute hand on 4 read as 4 minutes", "Each number is 5 minutes: 4 × 5 = 20 minutes"],
            ["Quarter to 4 written as 4:45", "Quarter to 4 is 15 minutes before 4:00, so 3:45"],
            ["14:35 to 15:10 worked out as 1510 − 1435 = 75 minutes", "An hour is 60 minutes. Count on: 25 + 10 = 35 minutes"],
        ])
    )


FAQ = [
    {"q": "When do children learn the 24-hour clock?",
     "a": "In the National Curriculum in England, children learn to read, write and convert between analogue and digital 12- and 24-hour clocks in Year 4. In Year 3 they tell the time to the nearest minute and use am and pm."},
    {"q": "How do you change 12-hour time into 24-hour time?",
     "a": "For am times keep the hour and write 4 digits (7:30 am is 07:30). For pm times add 12 to the hour (3:45 pm is 15:45). 12 noon stays 12:00 and 12 midnight is 00:00."},
    {"q": "Is midnight 00:00 or 24:00?",
     "a": "In 24-hour time midnight is written 00:00, the start of a new day. So 12:20 am is 00:20 and noon is 12:00."},
    {"q": "What time conversions should a Year 4 child know?",
     "a": "Year 4 children should convert hours to minutes, minutes to seconds, years to months and weeks to days, using 1 hour = 60 minutes, 1 minute = 60 seconds, 1 year = 12 months and 1 week = 7 days."},
]


def spread(sets, rnd):
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
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4413)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_words(rnd), set_digital(rnd, people), set_convert(rnd), set_durations(rnd), set_timetables(rnd, people)]
    spread(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    u = {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "time-12-and-24-hour-clock", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Time: the 12-Hour and 24-Hour Clock",
        "seo_title": "Year 4 12- and 24-Hour Clock Worksheets: Analogue, Digital and Converting Time (Free, with Answers)",
        "short_title": "12- and 24-hour clock",
        "domain": "Measurement",
        "standard_code": "Year 4: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Read, write and convert time between analogue and digital 12- and 24-hour clocks; solve problems involving converting from hours to minutes; minutes to seconds; years to months; weeks to days.",
        "meta_desc": "Free Year 4 maths worksheets on time: read analogue clocks to the minute, write am and pm times, convert between the 12-hour and 24-hour clock, work out durations, read bus and train timetables and convert hours, minutes, seconds, weeks and years. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "pm: add 12 to the hour. 3:45 pm = 15:45.",
        "key_sub": "am times keep the hour with 4 digits (7:30 am = 07:30). Midnight is 00:00. An hour has 60 minutes, so count on to the next o’clock when you work out how long.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "timetable")
    mark_large(u, "time line")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
