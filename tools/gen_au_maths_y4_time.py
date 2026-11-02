# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Time, am and pm, and Duration (Australian Curriculum v9.0, AC9M4M03)
  python3 tools/gen_au_maths_y4_time.py
Every analog clock and calendar is drawn from the data. Every answer is worked out in code.
Wrong answers come from real student mistakes: an hour counted as 100 minutes, am and pm swapped at midday,
the start day counted when finding the days between two dates, the hour hand read as the next hour,
hours and minutes subtracted separately, 2 1/2 hours read as 2 hours 50 minutes, forgetting to carry into the next hour.
HTML attributes use single quotes (no backslashes in the JSON). Australian English ("analog", "program").
"""
import calendar, json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Charlotte", "she"), ("Oliver", "he"), ("Isla", "she"), ("Jack", "he"), ("Mia", "she"), ("Noah", "he"),
          ("Amelia", "she"), ("William", "he"), ("Ava", "she"), ("Leo", "he"), ("Harper", "she"), ("Lachlan", "he"),
          ("Chloe", "she"), ("Liam", "he"), ("Ruby", "she"), ("Aarav", "he"), ("Mei", "she"), ("Kai", "he"),
          ("Zara", "she"), ("Cooper", "he"), ("Matilda", "she"), ("Ethan", "he"), ("Sienna", "she"), ("Grace", "she")]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


# ------------------------------------------------------------ time formats
def h12(h24):
    return (h24 - 1) % 12 + 1


def tm12(h24, m):
    """12-hour digital: 3:45 pm"""
    h24 %= 24
    return "%d:%02d %s" % (h12(h24), m, "am" if h24 < 12 else "pm")


def f12(t):
    """absolute minutes -> 12-hour time"""
    t %= 24 * 60
    return tm12(t // 60, t % 60)


def T(h, m):
    return h * 60 + m


def dig(h, m):
    return "%d:%02d" % (h12(h), m)


def words(h, m):
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
    """a duration as a student might write it (minutes may be 60 or more)"""
    if hh <= 0:
        return mins(mm) if mm > 0 else None
    return "%d hour%s" % (hh, "" if hh == 1 else "s") + (" %s" % mins(mm) if mm else "")


def dur_value(s):
    v = 0
    for n, unit in re.findall(r"(\d+) (hour|minute)", s):
        v += int(n) * (60 if unit == "hour" else 1)
    return v


def naive100(t1, t2):
    """the 100-minutes-in-an-hour mistake: 9:40 to 11:15 done as 1115 − 940 = 175 -> 1 hour 75 minutes"""
    a = (t1 // 60) * 100 + t1 % 60
    b = (t2 // 60) * 100 + t2 % 60
    n = b - a
    if n <= 0 or n % 100 < 60:
        return None
    return raw_dur(n // 100, n % 100)


def hour_minute_diff(t1, t2):
    """hours subtracted, minutes subtracted the wrong way round: 9:40 to 1:15 pm -> 4 hours 25 minutes"""
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
    gap, top = 14, 30
    W = 4 * size + 3 * gap
    s = []
    for i, (h, m) in enumerate(times):
        x = i * (size + gap)
        s.append("<text x='%.1f' y='22' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + size / 2.0, GREEN, "ABCD"[i]))
        s.append(clock_body(h, m, size, x, top))
    return svg_wrap(W, size + top, "".join(s), "four analog clocks")


def jump_label(n):
    hh, mm = divmod(n, 60)
    if not hh:
        return "+%d min" % mm
    if not mm:
        return "+%d h" % hh
    return "+%d h %d min" % (hh, mm)


def jumps(t1, t2):
    """start -> next o'clock -> midday (if passed) -> last o'clock -> end"""
    pts = [t1]
    a = -(-t1 // 60) * 60
    if t1 < a <= t2:
        pts.append(a)
    for noon in (12 * 60, 24 * 60):
        if pts[-1] < noon < t2 and noon not in pts:
            pts.append(noon)
    b = (t2 // 60) * 60
    if b > pts[-1]:
        pts.append(b)
    if t2 > pts[-1]:
        pts.append(t2)
    return pts


def timeline_svg(t1, t2, W=470):
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
                 % (X(i), Y + 32, LINE, f12(t)))
    for i in range(n):
        x1, x2 = X(i), X(i + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1 + 4, Y - 12, (x1 + x2) / 2, Y - 54, x2 - 4, Y - 12, RED))
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % ((x1 + x2) / 2, Y - 40, RED, jump_label(pts[i + 1] - pts[i])))
    return svg_wrap(W, 114, "".join(s), "time line from %s to %s" % (f12(t1), f12(t2)))


def count_on(t1, t2):
    pts = jumps(t1, t2)
    parts = ["%s to %s is %s" % (f12(a), f12(b), dur(b - a)) for a, b in zip(pts, pts[1:])]
    d = t2 - t1
    if len(parts) == 1:
        return "Count on: %s. So it is <b>%s</b>." % (parts[0], dur(d))
    terms = [dur(b - a) for a, b in zip(pts, pts[1:])]
    hrs = [x for x in terms if "minute" not in x]
    mns = [x for x in terms if "minute" in x]
    return "Count on: %s. %s = <b>%s</b>." % (", ".join(parts), " + ".join(hrs + mns), dur(d))


def calendar_svg(year, month):
    """Month calendar, weeks start on Monday (as on most Australian calendars)."""
    CW, RH, top = 46, 32, 70
    weeks = calendar.Calendar(0).monthdayscalendar(year, month)
    W = 7 * CW + 4
    H = top + RH * len(weeks) + 4
    s = ["<rect x='2' y='2' width='%d' height='36' fill='%s'/>" % (W - 4, GREEN),
         "<text x='%.0f' y='27' font-size='18' font-weight='700' fill='#fff' text-anchor='middle'>%s %d</text>"
         % (W / 2.0, MONTHS[month], year)]
    for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        s.append("<text x='%.0f' y='60' font-size='14' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (2 + CW * i + CW / 2.0, GREEN if i < 5 else RED, d))
    for r, wk in enumerate(weeks):
        y = top + RH * r
        if r % 2 == 0:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
        for i, d in enumerate(wk):
            if d:
                s.append("<text x='%.0f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                         % (2 + CW * i + CW / 2.0, y + 22, LINE, d))
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, LINE))
    return svg_wrap(W, H, "".join(s), "calendar for %s %d" % (MONTHS[month].lower(), year))


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
        s.append(put(i, 21, hd, "#fff", True))
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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def hand_text(h, m):
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
        hh = "The short hour hand is between <b>%d</b> and <b>%d</b>, so the hour is still <b>%d</b>." % (h, h % 12 + 1, h)
    return hh + " " + mm


# ============================================================ set 1: analog clocks to the minute, am and pm
CONTEXTS = [  # sentence, 24-hour hour, minute range, 5-minute times only?
    ("{n}’s alarm goes off in the morning.", 6, 31, 54, True),
    ("{n} catches the bus to school in the morning.", 8, 6, 24, True),
    ("Recess finishes in the morning.", 11, 6, 24, True),
    ("{n} eats lunch just after midday.", 12, 33, 56, False),
    ("Sport starts in the afternoon.", 14, 6, 27, False),
    ("{n} gets home from school in the afternoon.", 15, 36, 57, False),
    ("Footy training starts in the late afternoon.", 17, 6, 27, False),
    ("{n} eats dinner in the evening.", 18, 36, 57, False),
    ("{n} has breakfast in the morning.", 7, 33, 56, False),
    ("{n} goes to bed at night.", 20, 6, 27, False),
]


def set_clocks(rnd, people):
    its = []
    # midday and midnight
    its.append(mcq("What is <b>midday</b> (noon) in 12-hour time?", "12:00 pm", ["12:00 am", "11:00 am", "1:00 pm"],
                   "Midday is 12 o’clock in the middle of the day. Times from midday to midnight are pm, so midday is "
                   "<b>12:00 pm</b>. 12:00 am is midnight."))
    its.append(mcq("It is <b>5 minutes after midnight</b>. What time is it?", "12:05 am", ["12:05 pm", "11:55 pm", "11:05 pm"],
                   "A new day starts at midnight, and times from midnight to midday are am. So 5 minutes after midnight is "
                   "<b>12:05 am</b>. (11:55 pm is 5 minutes <b>before</b> midnight.)"))
    assert T(11, 50) + 20 == T(12, 10)
    its.append(mcq("It is <b>11:50 am</b>. What time will it be in <b>20 minutes</b>?", "12:10 pm",
                   ["12:10 am", "1:10 pm", "11:10 am"],
                   "11:50 am + 10 minutes = 12:00 pm (midday). 10 more minutes makes 12:10. It is now after midday, "
                   "so the time changes from am to <b>pm</b>: <b>12:10 pm</b>."))
    assert T(12, 10) - 15 == T(11, 55)
    its.append(mcq("It is <b>12:10 pm</b>. What time was it <b>15 minutes ago</b>?", "11:55 am",
                   ["11:55 pm", "12:25 pm", "11:45 am"],
                   "Count back 10 minutes to 12:00 pm (midday), then 5 more minutes to 11:55. That is before midday, "
                   "so it is <b>11:55 am</b>. (12:25 pm is 15 minutes later, not earlier.)"))
    # analog clocks with a time of day
    ctx = CONTEXTS[:]
    used = set()
    clock_items = []
    for sent, H, lo, hi, five in ctx:
        ms = [x for x in range(lo, hi + 1) if (x % 5 == 0) == five and hands_gap(H, x) >= 15 and x not in used]
        m = rnd.choice(ms)
        used.add(m)
        n = m // 5
        nm, pr = next(people)
        right = tm12(H, m)
        c = [tm12(H + 12, m)]                             # am and pm swapped
        if m > 30:
            c.append(tm12(H + 1, m))                      # hour hand read as the next hour
        if m % 5 and n:
            c.append(tm12(H, n))                          # number the minute hand passed read as minutes
        if m % 5 == 0:
            c.append(tm12(H, n))
        c += [tm12(H, 60 - m), tm12(H + 1, m), tm12(H - 1, m)]
        if H < 12:
            why = "It is the morning, before midday, so it is <b>am</b>."
        elif H == 12:
            why = "The hour is 12 and it is just after midday, so it is <b>pm</b> (not am)."
        else:
            why = "It is after midday, so it is <b>pm</b>."
        e = "%s %s So it is <b>%s</b>." % (hand_text(H, m), why, right)
        q = fig(clock_svg(H, m)) + sent.format(n=nm) + " What is the time?"
        clock_items.append(mcq(q, right, c, e))
    # which analog clock (pictures A to D)
    L = "ABCD"
    pos = [2, 1]
    pic = []
    for (h, m), p in zip([(7, 48), (4, 13)], pos):
        others = [(h + 1, m), (h, 60 - m), (h, m // 5)]
        times = list(others)
        times.insert(p, (h, m))
        assert len(set(times)) == 4
        wrong = "; ".join("clock %s shows %s" % (L[times.index(t)], dig(*t)) for t in others)
        e = ("At %s the long hand is %d small mark%s past the %d (count in 5s to %d, then on in 1s to %d), and the short hand "
             "is between %d and %d. That is clock <b>%s</b>. (%s.)"
             % (dig(h, m), m % 5, "" if m % 5 == 1 else "s", m // 5, m // 5 * 5, m, h, h % 12 + 1, L[p],
                wrong[0].upper() + wrong[1:]))
        pic.append({"q": fig(four_clocks_svg(times)) + "Which analog clock shows <b>%s</b>?" % dig(h, m),
                    "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True})
    # words -> 12-hour digital
    wd = []
    for H, m, part in [(18, 47, "in the evening"), (12, 45, "in the afternoon"), (23, 22, "at night"),
                       (11, 52, "just before midday")]:
        w = words(H, m)
        right = tm12(H, m)
        ap = "am" if H < 12 else "pm"
        if m > 30:
            c = [tm12(H + 1, m), tm12(H + 12, m), tm12(H, 60 - m), tm12(H + 1, 60 - m)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d minutes past %d. "
                 "It is %s, so it is %s: <b>%s</b>." % (w, 60 - m, h12(H + 1), 60 - m, m, m, h12(H), part, ap, right))
            if H == 11:
                e += " (Not 12:52 pm: the time is before 12 o’clock, and before midday is am.)"
            if H == 12:
                e += " (Quarter to 1 is still in the 12 o’clock hour, and after midday is pm.)"
        else:
            c = [tm12(H + 12, m), tm12(H - 1, 60 - m), tm12(H + 1, m), tm12(H, m // 5)]
            e = "“%s” means %d minutes <b>after</b> %d o’clock. It is %s, so it is %s: <b>%s</b>." % (w, m, h12(H), part, ap, right)
        wd.append(mcq("Write <b>%s %s</b> as a digital time with am or pm." % (w, part), right, c, e))
    its = ([its[0], clock_items[0], clock_items[1], clock_items[2], its[1], clock_items[8], pic[0], clock_items[3],
            its[2], clock_items[4], clock_items[5], wd[0], clock_items[6], pic[1], its[3], clock_items[7], wd[1],
            clock_items[9], wd[2], wd[3]])
    assert len(its) == 20
    return {"title": "Read analog clocks to the minute and write am or pm", "items": its}


# ============================================================ set 2: units of time and conversions
def set_units():
    half, quarter, three_q = fr(1, 2), fr(1, 4), fr(3, 4)
    assert 2 * 60 + 30 == 150 and 3 * 60 == 180 and 4 * 60 == 240 and 60 + 30 == 90 and 3 * 24 == 72
    assert 96 // 24 == 4 and 200 == 3 * 60 + 20 and 150 == 2 * 60 + 30 and 24 // 4 == 6
    F = [
        ("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "24"],
         "There are <b>60 seconds</b> in 1 minute. Time does not count in hundreds."),
        ("How many <b>minutes</b> are in 1 hour?", "60", ["100", "24", "12"],
         "There are <b>60 minutes</b> in 1 hour. (Not 100: an hour is not like a dollar with 100 cents.)"),
        ("How many <b>hours</b> are in 1 day?", "24", ["12", "60", "100"],
         "There are <b>24 hours</b> in 1 day: 12 am hours (midnight to midday) and 12 pm hours (midday to midnight)."),
        ("How many <b>months</b> are in 1 year?", "12", ["52", "10", "365"],
         "January to December: <b>12 months</b>. (52 is about the number of weeks, and 365 is the number of days.)"),
        ("How many <b>days</b> are in a year that is <b>not</b> a leap year?", "365", ["366", "360", "52"],
         "A normal year has <b>365 days</b>. A leap year has one extra day (29 February), so it has 366 days."),
        ("How many days are in a <b>leap year</b>?", "366", ["365", "364", "400"],
         "A leap year has an extra day, 29 February. 365 + 1 = <b>366 days</b>. Leap years come every 4 years."),
        ("<b>3 weeks</b> = ? days", "21", ["15", "30", "10"],
         "1 week = 7 days. 3 × 7 = <b>21 days</b>. (15 is only the school days in 3 weeks.)"),
        ("<b>3 minutes</b> = ? seconds", "180", ["300", "63", "120"],
         "1 minute = 60 seconds. 3 × 60 = <b>180 seconds</b>. (Not 300: a minute is 60 seconds, not 100.)"),
        ("<b>4 hours</b> = ? minutes", "240", ["400", "64", "24"],
         "1 hour = 60 minutes. 4 × 60 = <b>240 minutes</b>. (Not 400: an hour is 60 minutes, not 100.)"),
        ("<b>2 years</b> = ? months", "24", ["104", "20", "14"],
         "1 year = 12 months. 2 × 12 = <b>24 months</b>. (104 is the number of weeks in 2 years.)"),
        ("<b>" + three_q + " of an hour</b> = ? minutes", "45", ["75", "15", "34"],
         "A quarter of an hour is 60 ÷ 4 = 15 minutes. Three quarters is 3 × 15 = <b>45 minutes</b>. "
         "(75 would be three quarters of 100.)"),
        ("<b>1" + half + " minutes</b> = ? seconds", "90", ["150", "110", "60"],
         "1 minute = 60 seconds and half a minute = 30 seconds. 60 + 30 = <b>90 seconds</b>. "
         "(110 comes from reading 1" + half + " as 1 minute 50 seconds.)"),
        ("<b>2" + half + " hours</b> = ? minutes", "150", ["250", "170", "120"],
         "2 hours = 2 × 60 = 120 minutes. Half an hour = 30 minutes. 120 + 30 = <b>150 minutes</b>. "
         "(170 comes from reading 2" + half + " hours as 2 hours 50 minutes.)"),
        ("<b>3 days</b> = ? hours", "72", ["36", "48", "30"],
         "1 day = 24 hours. 3 × 24 = <b>72 hours</b>. (36 uses 12 hours for a day, but a day is 24 hours.)"),
        ("<b>" + quarter + " of a day</b> = ? hours", "6", ["15", "4", "12"],
         "1 day = 24 hours. A quarter is 24 ÷ 4 = <b>6 hours</b>. (15 is a quarter of an hour in minutes, and 12 hours is half a day.)"),
        ("<b>150 minutes</b> = ?", "2 hours 30 minutes", ["1 hour 50 minutes", "2 hours 50 minutes", "3 hours"],
         "60 minutes make 1 hour. 150 = 60 + 60 + 30, so it is <b>2 hours 30 minutes</b>. "
         "(1 hour 50 minutes uses 100 minutes in an hour.)"),
        ("<b>200 seconds</b> = ?", "3 minutes 20 seconds", ["2 minutes", "3 minutes 33 seconds", "2 minutes 20 seconds"],
         "60 seconds make 1 minute. 3 × 60 = 180, and 200 − 180 = 20. So it is <b>3 minutes 20 seconds</b>. "
         "(2 minutes uses 100 seconds in a minute.)"),
        ("<b>96 hours</b> = ? days", "4", ["8", "9", "3"],
         "1 day = 24 hours. 24 × 4 = 96, so 96 hours = <b>4 days</b>. (8 days would use 12 hours for a day.)"),
        ("Which time is the <b>longest</b>?", "100 minutes", ["1" + half + " hours", "1 hour 35 minutes", "1 hour 20 minutes"],
         "Change them all to minutes: 1" + half + " hours = 90 minutes, 1 hour 35 minutes = 95 minutes, "
         "1 hour 20 minutes = 80 minutes. <b>100 minutes</b> is the longest (it is 1 hour 40 minutes)."),
        ("Which of these is <b>true</b>?", "100 minutes = 1 hour 40 minutes",
         ["1 hour = 100 minutes", "100 minutes = 1 hour", "1 hour 40 minutes = 140 minutes"],
         "1 hour = 60 minutes. 100 − 60 = 40, so <b>100 minutes = 1 hour 40 minutes</b>. "
         "1 hour 40 minutes = 60 + 40 = 100 minutes, not 140."),
    ]
    its = [mcq(q, a, c, e) for q, a, c, e in F]
    return {"title": "Units of time and converting between them", "items": its}


# ============================================================ set 3: how long? within and across am and pm
def dur_q(q, t1, t2, line=False, extra=()):
    d = t2 - t1
    assert d > 0
    c = list(extra) + [naive100(t1, t2), hour_minute_diff(t1, t2)]
    if (t1 < 12 * 60 < t2 or t1 < 24 * 60 < t2) and h12(t2 // 60) < h12(t1 // 60) and h12(t2 // 60) != 12:
        c.append(dur(12 * 60 - d))                        # am/pm ignored: 9:40 − 1:15 = 8 hours 25 minutes
    c += [dur(d + 60) if d < 60 else dur(d - 60), dur(d + 60), dur(d + 10), dur(d - 5)]
    e = count_on(t1, t2)
    if t1 < 12 * 60 < t2:
        e += " (The time goes past midday, so am changes to pm. Count on through 12:00 pm.)"
    if naive100(t1, t2):
        e += " (Not %s: an hour has 60 minutes, not 100.)" % naive100(t1, t2)
    return mcq((fig(timeline_svg(t1, t2)) if line else "") + q, dur(d), c, e, key=dur_value)


def end_q(q, start, d, right_t, wrong_ts, e):
    assert start + d == right_t
    return mcq(q, f12(right_t), [f12(x) for x in wrong_ts], e)


def back_q(q, end, d, right_t, wrong_ts, e):
    assert end - d == right_t
    return mcq(q, f12(right_t), [f12(x) for x in wrong_ts], e)


def set_durations(people):
    its = []
    nm, pr = next(people)
    its.append(dur_q("%s starts a maths test at <b>9:15 am</b> and finishes at <b>9:52 am</b>. How long does %s take?"
                     % (nm, pr), T(9, 15), T(9, 52)))
    its.append(dur_q("A TV program starts at <b>2:35 pm</b> and ends at <b>3:10 pm</b>. How long is it?",
                     T(14, 35), T(15, 10), line=True))
    nm, pr = next(people)
    its.append(dur_q("%s leaves home at <b>7:40 am</b> and gets to school at <b>8:25 am</b>. How long is the trip?" % nm,
                     T(7, 40), T(8, 25)))
    its.append(dur_q("A school concert goes from <b>10:20 am</b> to <b>11:45 am</b>. How long is the concert?",
                     T(10, 20), T(11, 45)))
    its.append(dur_q("Cricket practice goes from <b>3:45 pm</b> to <b>5:20 pm</b>. How long is practice?",
                     T(15, 45), T(17, 20), line=True))
    its.append(dur_q("The sausage sizzle cooks from <b>11:48 am</b> to <b>12:17 pm</b>. How long is that?",
                     T(11, 48), T(12, 17)))
    nm, pr = next(people)
    its.append(dur_q("%s’s family has dinner at a restaurant from <b>6:50 pm</b> to <b>8:05 pm</b>. How long are they there?" % nm,
                     T(18, 50), T(20, 5)))
    its.append(dur_q("A cake goes in the oven at <b>11:30 am</b> and comes out at <b>12:15 pm</b>. How long does it bake?",
                     T(11, 30), T(12, 15), line=True))
    its.append(dur_q("A school excursion leaves at <b>10:45 am</b> and gets back at <b>1:10 pm</b>. How long is it?",
                     T(10, 45), T(13, 10), line=True))
    its.append(dur_q("The swimming carnival starts at <b>9:40 am</b> and ends at <b>1:15 pm</b>. How long does it go for?",
                     T(9, 40), T(13, 15), line=True))
    nm, pr = next(people)
    its.append(dur_q("%s’s birthday party goes from <b>11:20 am</b> to <b>2:05 pm</b>. How long is the party?" % nm,
                     T(11, 20), T(14, 5)))
    its.append(dur_q("The school fete opens at <b>8:25 am</b> and closes at <b>12:40 pm</b>. How long is it open?",
                     T(8, 25), T(12, 40)))
    its.append(dur_q("A family drives from Brisbane to the beach. They leave at <b>10:55 am</b> and arrive at <b>4:30 pm</b>, "
                     "after stopping for lunch. How long does the trip take?", T(10, 55), T(16, 30)))
    # end times and start times (am to pm)
    its.append(end_q("A movie starts at <b>10:40 am</b>. It lasts <b>1 hour 35 minutes</b>. What time does it end?",
                     T(10, 40), 95, T(12, 15), [T(0, 15), T(11, 15), T(13, 15)],
                     "10:40 am + 1 hour = 11:40 am. Then 20 minutes takes it to 12:00 pm (midday), and 15 more minutes makes "
                     "<b>12:15 pm</b>. It is after midday, so it is pm. (11:15 am forgets to carry the 60 minutes into the next hour.)"))
    nm, pr = next(people)
    its.append(end_q("%s starts a jigsaw puzzle at <b>11:25 am</b> and works on it for <b>50 minutes</b>. What time does %s stop?"
                     % (nm, pr), T(11, 25), 50, T(12, 15), [T(0, 15), T(11, 15), T(13, 15)],
                     "11:25 am + 35 minutes = 12:00 pm (midday). 50 − 35 = 15 more minutes: <b>12:15 pm</b>. "
                     "After midday it is pm, not am."))
    its.append(end_q("A bushwalk starts at <b>9:50 am</b> and takes <b>2 hours 45 minutes</b>. What time does it finish?",
                     T(9, 50), 165, T(12, 35), [T(0, 35), T(11, 35), T(13, 35)],
                     "9:50 am + 2 hours = 11:50 am. 10 more minutes is 12:00 pm, then 35 more minutes: <b>12:35 pm</b>. "
                     "(45 − 10 = 35.)"))
    its.append(back_q("A netball carnival ends at <b>1:20 pm</b>. It lasted <b>1 hour 45 minutes</b>. What time did it start?",
                      T(13, 20), 105, T(11, 35), [T(23, 35), T(12, 35), T(15, 5)],
                      "Count back 1 hour: 1:20 pm → 12:20 pm. Then back 20 minutes to 12:00 pm and 25 more to 11:35. "
                      "That is before midday, so it started at <b>11:35 am</b>. (3:05 pm counts on instead of back.)"))
    nm, pr = next(people)
    its.append(back_q("%s must be at the station at <b>12:10 pm</b>. The walk takes <b>25 minutes</b>. What is the latest time "
                      "%s can leave home?" % (nm, pr), T(12, 10), 25, T(11, 45), [T(23, 45), T(12, 35), T(11, 35)],
                      "Count back 10 minutes to 12:00 pm (midday), then 15 more: 11:45. It is before midday, so <b>11:45 am</b>. "
                      "(12:35 pm counts on instead of back, and 11:35 am forgets the 10 minutes after midday.)"))
    its.append(back_q("A footy match finishes at <b>4:05 pm</b>. It lasted <b>2 hours 30 minutes</b>. What time did it start?",
                      T(16, 5), 150, T(13, 35), [T(1, 35), T(18, 35), T(14, 5)],
                      "Count back 2 hours: 4:05 pm → 2:05 pm. Then back 30 minutes: 5 minutes to 2:00 pm and 25 more to "
                      "<b>1:35 pm</b>. (2:05 pm only takes away the 2 hours.)"))
    its.append(dur_q("A plane leaves Perth at <b>10:30 pm</b> and lands in Adelaide at <b>1:15 am</b> the next morning, "
                     "Perth time. How long is the flight?", T(22, 30), T(25, 15), line=True))
    assert len(its) == 20
    order = [0, 1, 2, 3, 5, 4, 6, 7, 13, 14, 8, 9, 10, 17, 15, 11, 16, 12, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "How long? Durations across am and pm", "items": [its[i] for i in order]}


# ============================================================ set 4: calendars
def set_calendar():
    Y, M = 2027, 3
    cal = fig(calendar_svg(Y, M))

    def wd(d, month=M, year=Y):
        return WEEKDAYS[calendar.weekday(year, month, d)]
    its = []
    # text-only facts
    assert calendar.monthrange(2027, 4)[1] == 30
    its.append(mcq("How many days are in <b>April</b>?", "30", ["31", "28", "12"],
                   "“30 days has September, April, June and November.” So April has <b>30 days</b>."))
    assert [calendar.monthrange(2027, m)[1] for m in (7, 6, 9, 11)] == [31, 30, 30, 30]
    its.append(mcq("Which month has <b>31 days</b>?", "July", ["June", "September", "November"],
                   "September, April, June and November have 30 days. February has 28 (29 in a leap year). "
                   "All the others, including <b>July</b>, have 31."))
    assert calendar.isleap(2028) and not any(calendar.isleap(y) for y in (2026, 2027, 2030))
    its.append(mcq("Which year is a <b>leap year</b>?", "2028", ["2026", "2027", "2030"],
                   "Leap years come every 4 years. 2024 was a leap year, so the next one is 2024 + 4 = <b>2028</b>. "
                   "(2028 ÷ 4 = 507 with no remainder.)"))
    assert calendar.monthrange(2028, 2)[1] == 29
    its.append(mcq("2028 is a leap year. How many days are in <b>February 2028</b>?", "29", ["28", "30", "31"],
                   "February has 28 days, but in a leap year it gets one extra day: <b>29 days</b>."))
    # calendar picture: March 2027
    assert wd(18) == "Thursday"
    its.append(mcq(cal + "Look at the calendar. What day of the week is <b>18 March</b>?", "Thursday",
                   ["Wednesday", "Friday", "Sunday"],
                   "Find 18 in the calendar and go up its column to the top: <b>Thursday</b>."))
    sats = [d for d in range(1, 32) if wd(d) == "Saturday"]
    assert sats[1] == 13
    its.append(mcq(cal + "What is the date of the <b>second Saturday</b> in March 2027?", "13 March",
                   ["6 March", "20 March", "14 March"],
                   "The Saturdays are %s. The second one is <b>13 March</b>. (6 March is the first Saturday and 14 March is a Sunday.)"
                   % ", ".join(str(x) for x in sats)))
    fris = [d for d in range(1, 32) if wd(d) == "Friday"]
    assert len(fris) == 4
    its.append(mcq(cal + "%s has a swimming lesson every <b>Friday</b> in March. How many lessons is that?" % "Ava", "4",
                   ["5", "3", "31"],
                   "The Fridays are %s. That is <b>4</b> lessons. (Not every month has 5 of each day.)"
                   % ", ".join(str(x) for x in fris)))
    assert 19 - 4 == 15
    its.append(mcq(cal + "How many days is it from <b>4 March</b> to <b>19 March</b>?", "15", ["16", "14", "23"],
                   "19 − 4 = <b>15 days</b>. Count the jumps from one day to the next: 5, 6, 7 … 19 is 15 jumps. "
                   "(16 counts 4 March as well, but no time has passed on the start day.)"))
    assert 11 + 7 == 18 and wd(11) == "Thursday"
    its.append(mcq(cal + "What is the date <b>1 week after</b> Thursday 11 March?", "Thursday 18 March",
                   ["Wednesday 17 March", "Friday 19 March", "Thursday 25 March"],
                   "1 week = 7 days. 11 + 7 = 18. Go straight down one row on the calendar: <b>Thursday 18 March</b>. "
                   "(17 March counts 11 March as the first day.)"))
    assert 12 + 10 == 22 and wd(22) == "Monday"
    its.append(mcq(cal + "What is the date <b>10 days after</b> 12 March?", "22 March", ["21 March", "23 March", "2 March"],
                   "12 + 10 = <b>22 March</b>. (21 March counts 12 March as one of the 10 days.)"))
    assert 26 - 9 == 17
    its.append(mcq(cal + "Today is <b>9 March</b>. The school excursion is on <b>26 March</b>. How many days until the excursion?",
                   "17", ["18", "16", "35"],
                   "26 − 9 = <b>17 days</b>. (18 counts today as well.)"))
    assert 3 + 14 == 17
    its.append(mcq(cal + "Liam borrows a library book on <b>3 March</b>. It is due back <b>2 weeks</b> later. What is the due date?",
                   "17 March", ["16 March", "10 March", "5 March"],
                   "2 weeks = 14 days. 3 + 14 = <b>17 March</b>. On the calendar, go down 2 rows from 3. "
                   "(10 March is only 1 week later, and 5 March adds 2 days, not 2 weeks.)"))
    assert 30 - 21 == 9
    its.append(mcq(cal + "Today is <b>21 March</b>. Zara’s birthday is on <b>30 March</b>. How many days until her birthday?",
                   "9", ["10", "8", "51"],
                   "30 − 21 = <b>9 days</b>. (10 counts today as one of the days.)"))
    assert 5 + 21 == 26
    its.append(mcq(cal + "What is the date <b>3 weeks after</b> 5 March?", "26 March", ["25 March", "8 March", "19 March"],
                   "3 weeks = 3 × 7 = 21 days. 5 + 21 = <b>26 March</b>. On the calendar, go down 3 rows from 5. "
                   "(19 March is only 2 weeks later.)"))
    assert 27 - 6 == 21
    its.append(mcq(cal + "Lachlan stays with his grandparents from Saturday <b>6 March</b> to Saturday <b>27 March</b>. How many weeks is that?",
                   "3 weeks", ["4 weeks", "21 weeks", "2 weeks"],
                   "27 − 6 = 21 days. 21 ÷ 7 = <b>3 weeks</b>. On the calendar, 27 is 3 rows below 6. "
                   "(4 weeks counts the rows from 6 to 27 instead of the jumps.)"))
    assert wd(15) == "Monday" and wd(19) == "Friday"
    its.append(mcq(cal + "School camp starts on Monday <b>15 March</b> and ends on Friday <b>19 March</b>. On how many "
                   "days is the camp, counting both Monday and Friday?", "5", ["4", "34", "7"],
                   "The camp is on Monday, Tuesday, Wednesday, Thursday and Friday: <b>5 days</b>. Here we count the days "
                   "the camp is on, so both the first and last day count. (19 − 15 = 4 is the number of nights.)"))
    assert calendar.weekday(2027, 4, 1) == 3 and wd(31) == "Wednesday"
    its.append(mcq(cal + "What day of the week will <b>1 April 2027</b> be?", "Thursday", ["Wednesday", "Monday", "Friday"],
                   "31 March is a Wednesday, and 1 April is the next day, so it is a <b>Thursday</b>. "
                   "(A new month does not start on a new row: it carries on from the last day of March.)"))
    # text-only harder problems
    assert 23 == 14 + 9
    its.append(mcq("Today is <b>14 June</b>. What will the date be in <b>9 days</b>?", "23 June", ["22 June", "24 June", "5 June"],
                   "14 + 9 = <b>23 June</b>. (22 June counts today as one of the 9 days, and 5 June counts back.)"))
    assert 31 - 1 == 30
    its.append(mcq("How many days is it from <b>1 May</b> to <b>31 May</b>?", "30", ["31", "29", "32"],
                   "31 − 1 = <b>30 days</b>. May has 31 dates, but from the 1st to the 31st there are 30 jumps. "
                   "(31 counts 1 May as well.)"))
    assert 12 - 8 == 4
    its.append(mcq("Year 4 camp leaves on <b>8 August</b> and comes home on <b>12 August</b>. How many <b>nights</b> are "
                   "the students away?", "4", ["5", "20", "3"],
                   "Nights away: 8th, 9th, 10th and 11th. 12 − 8 = <b>4 nights</b>. (5 counts the days the camp is on, "
                   "not the nights.)"))
    assert len(its) == 20
    order = [0, 1, 4, 2, 3, 5, 6, 8, 9, 7, 16, 12, 10, 11, 13, 17, 14, 15, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Calendars: days, weeks and dates", "items": [its[i] for i in order]}


# ============================================================ set 5: timetables and everyday problems
SCHOOL = [("Session 1", T(8, 50), T(10, 50)), ("Recess", T(10, 50), T(11, 20)), ("Session 2", T(11, 20), T(13, 10)),
          ("Lunch", T(13, 10), T(14, 0)), ("Session 3", T(14, 0), T(15, 10))]
SWIM = [("Starfish", T(15, 45), 30), ("Dolphins", T(16, 20), 45), ("Sharks", T(17, 15), 50)]
MOVIES = [("Koala Rescue", T(10, 15), 95), ("Space Kids", T(11, 50), 110), ("Ocean Quest", T(16, 40), 125)]


def len_text(n):
    hh, mm = divmod(n, 60)
    return ("%d h %d min" % (hh, mm)) if hh and mm else ("%d h" % hh if hh else "%d min" % mm)


def set_problems(people):
    its = []
    sch = fig(grid_svg("school day timetable", ["Session", "Starts", "Ends"], [130, 110, 110],
                       [[a, f12(b), f12(c)] for a, b, c in SCHOOL], "lmm"))
    swim = fig(grid_svg("swimming lesson timetable", ["Class", "Starts", "Lasts"], [130, 110, 110],
                        [[a, f12(b), len_text(c)] for a, b, c in SWIM], "lmm"))
    mov = fig(grid_svg("movie session times", ["Movie", "Starts", "Length"], [150, 110, 110],
                       [[a, f12(b), len_text(c)] for a, b, c in MOVIES], "lmm"))
    # school day
    a, b, c = SCHOOL[1]
    its.append(dur_q(sch + "Look at the timetable. How long is <b>recess</b>?", b, c))
    a, b, c = SCHOOL[3]
    its.append(dur_q(sch + "How long is <b>lunch</b>?", b, c))
    a, b, c = SCHOOL[2]
    its.append(dur_q(sch + "How long is <b>Session 2</b>?", b, c))
    its.append(dur_q(sch + "How long is the whole school day, from the start of Session 1 to the end of Session 3?",
                     SCHOOL[0][1], SCHOOL[4][2]))
    cls = sum(c - b for a, b, c in SCHOOL if a.startswith("Session"))
    assert cls == 300
    its.append(mcq(sch + "How much time is spent in the three <b>sessions</b> altogether?", dur(cls),
                   ["6 hours 20 minutes", "4 hours", "5 hours 20 minutes"],
                   "Session 1: 2 hours. Session 2: 1 hour 50 minutes. Session 3: 1 hour 10 minutes. "
                   "2 hours + 1 hour 50 minutes + 1 hour 10 minutes = 4 hours 60 minutes = <b>5 hours</b>. "
                   "(6 hours 20 minutes is the whole day, with recess and lunch.)", key=dur_value))
    # swimming
    a, b, c = SWIM[1]
    assert b + c == T(17, 5)
    its.append(mcq(swim + "What time does the <b>Dolphins</b> class finish?", f12(b + c),
                   [f12(T(16, 5)), f12(T(5, 5)), f12(T(17, 15))],
                   "4:20 pm + 40 minutes = 5:00 pm. 45 − 40 = 5 more minutes: <b>5:05 pm</b>. "
                   "(4:05 pm forgets to carry into the next hour: 20 + 45 = 65 minutes = 1 hour 5 minutes.)"))
    nm, pr = next(people)
    its.append(dur_q(swim + "%s gets to the pool at <b>4:40 pm</b> and waits for the <b>Sharks</b> class to start. "
                     "How long does %s wait?" % (nm, pr), T(16, 40), SWIM[2][1]))
    nm, pr = next(people)
    assert 4 * 50 == 200
    its.append(mcq(swim + "%s goes to the <b>Sharks</b> class once a week for <b>4 weeks</b>. How much time is that in the pool?"
                   % nm, "3 hours 20 minutes", ["2 hours", "3 hours 33 minutes", "4 hours"],
                   "4 × 50 = 200 minutes. 200 = 60 + 60 + 60 + 20, so it is <b>3 hours 20 minutes</b>. "
                   "(2 hours uses 100 minutes in an hour.)", key=dur_value))
    assert 9 * 30 == 270
    its.append(mcq(swim + "A term of <b>Starfish</b> lessons has <b>9</b> classes. How long is that altogether?",
                   "4 hours 30 minutes", ["2 hours 70 minutes", "3 hours", "27 hours"],
                   "9 × 30 = 270 minutes. 270 = 4 × 60 + 30, so it is <b>4 hours 30 minutes</b>. "
                   "(2 hours 70 minutes uses 100 minutes in an hour, and 27 hours mixes up minutes and hours.)",
                   key=dur_value))
    # movies
    a, b, c = MOVIES[0]
    assert b + c == T(11, 50)
    its.append(mcq(mov + "What time does <b>Koala Rescue</b> end?", f12(b + c), [f12(T(23, 50)), f12(T(12, 50)), f12(T(11, 35))],
                   "10:15 am + 1 hour = 11:15 am. 11:15 am + 35 minutes = <b>11:50 am</b>. It is still before midday, so it is am."))
    a, b, c = MOVIES[1]
    assert b + c == T(13, 40)
    its.append(mcq(mov + "What time does <b>Space Kids</b> end?", f12(b + c), [f12(T(1, 40)), f12(T(12, 40)), f12(T(14, 40))],
                   "11:50 am + 1 hour = 12:50 pm. 12:50 pm + 10 minutes = 1:00 pm, then 40 more minutes: <b>1:40 pm</b>. "
                   "(12:40 pm forgets to carry: 50 + 50 = 100 minutes = 1 hour 40 minutes.)"))
    assert MOVIES[2][2] == 125
    its.append(mcq(mov + "How many <b>minutes</b> long is <b>Ocean Quest</b>?", "125 minutes",
                   ["205 minutes", "120 minutes", "65 minutes"],
                   "2 hours = 2 × 60 = 120 minutes. 120 + 5 = <b>125 minutes</b>. (205 uses 100 minutes in an hour.)",
                   key=dur_value))
    its.append(mcq(mov + "Which movie is the <b>longest</b>?", "Ocean Quest",
                   ["Space Kids", "Koala Rescue", "They are all the same length."],
                   "Koala Rescue is 95 minutes, Space Kids is 110 minutes and Ocean Quest is 2 × 60 + 5 = 125 minutes. "
                   "<b>Ocean Quest</b> is the longest."))
    a, b, c = MOVIES[2]
    assert b + 15 + c == T(19, 0)
    its.append(mcq(mov + "Before <b>Ocean Quest</b> there are <b>15 minutes</b> of ads. The movie starts after the ads. "
                   "What time does the movie end?", f12(T(19, 0)), [f12(T(18, 45)), f12(T(7, 0)), f12(T(18, 0))],
                   "The movie starts at 4:40 pm + 15 minutes = 4:55 pm. 4:55 pm + 2 hours = 6:55 pm. "
                   "6:55 pm + 5 minutes = <b>7:00 pm</b>. (6:45 pm forgets the ads.)"))
    # everyday problems
    assert 4 * 10 + 3 * 3 == 49
    its.append(mcq("A junior netball game has <b>4 quarters of 10 minutes</b> with a <b>3-minute break</b> between quarters. "
                   "How long is the whole game?", "49 minutes", ["52 minutes", "40 minutes", "43 minutes"],
                   "Playing time: 4 × 10 = 40 minutes. There are 3 breaks between 4 quarters: 3 × 3 = 9 minutes. "
                   "40 + 9 = <b>49 minutes</b>. (52 counts 4 breaks.)", key=dur_value))
    nm, pr = next(people)
    assert T(17, 35) + 75 == T(18, 50)
    its.append(mcq("%s puts a lasagne in the oven at <b>5:35 pm</b>. It cooks for <b>1" % nm + fr(1, 4) + " hours</b>. "
                   "What time will it be ready?", f12(T(18, 50)), [f12(T(18, 0)), f12(T(19, 0)), f12(T(6, 50))],
                   "1" + fr(1, 4) + " hours = 1 hour 15 minutes. 5:35 pm + 1 hour = 6:35 pm. 6:35 pm + 15 minutes = "
                   "<b>6:50 pm</b>. (7:00 pm reads 1" + fr(1, 4) + " hours as 1 hour 25 minutes, and 6:00 pm adds only 25 minutes.)"))
    assert T(10, 30) + 180 + 25 == T(13, 55)
    its.append(mcq("A family leaves Sydney at <b>10:30 am</b> and drives to Canberra. They drive for <b>3 hours</b> and stop "
                   "for lunch for <b>25 minutes</b>. What time do they arrive?", f12(T(13, 55)),
                   [f12(T(1, 55)), f12(T(13, 30)), f12(T(11, 55))],
                   "10:30 am + 3 hours = 1:30 pm (11:30, 12:30, 1:30). Add the 25-minute stop: <b>1:55 pm</b>. "
                   "After midday it is pm. (1:30 pm forgets the lunch stop.)"))
    nm, pr = next(people)
    assert 14 * 25 == 350 and 350 == 5 * 60 + 50
    its.append(mcq("%s reads for <b>25 minutes</b> every day for a <b>fortnight</b>. How long does %s read altogether?" % (nm, pr),
                   "5 hours 50 minutes", ["3 hours 50 minutes", "2 hours 55 minutes", "6 hours 10 minutes"],
                   "A fortnight is 14 days. 14 × 25 = 350 minutes. 350 = 5 × 60 + 50, so it is <b>5 hours 50 minutes</b>. "
                   "(3 hours 50 minutes uses 100 minutes in an hour, and 2 hours 55 minutes uses only 7 days.)", key=dur_value))
    its.append(dur_q("A Year 4 excursion bus leaves school at <b>9:15 am</b> and gets back at <b>3:45 pm</b>. "
                     "How long are the students away from school?", T(9, 15), T(15, 45)))
    nm, pr = next(people)
    assert T(24 + 6, 45) - 630 == T(20, 15)
    its.append(mcq("%s’s alarm goes off at <b>6:45 am</b>. %s slept for <b>10" % (nm, pr.capitalize()) + fr(1, 2) +
                   " hours</b>. What time did %s go to sleep the night before?" % pr, f12(T(20, 15)),
                   [f12(T(8, 15)), f12(T(17, 15)), f12(T(19, 55))],
                   "10" + fr(1, 2) + " hours = 10 hours 30 minutes. Count back 10 hours from 6:45 am: 8:45 pm the night before. "
                   "Then back 30 minutes: <b>8:15 pm</b>. It was in the evening, so it is pm, not am. "
                   "(5:15 pm counts on instead of back, and 7:55 pm reads 10" + fr(1, 2) + " hours as 10 hours 50 minutes.)"))
    assert len(its) == 20
    order = [0, 1, 5, 9, 2, 12, 6, 3, 10, 14, 11, 7, 15, 4, 8, 13, 16, 18, 17, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Timetables and everyday problems: school, swimming and movies", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>am and pm</h2>"
        "<p>A day has <b>24 hours</b>. An analog clock goes around twice. <b>am</b> times go from midnight to midday "
        "(night and morning). <b>pm</b> times go from midday to midnight (afternoon and evening).</p>"
        "<p>Midday is <b>12:00 pm</b> and midnight is <b>12:00 am</b>. One minute after 11:59 am, the time becomes 12:00 pm.</p>"
        "<figure class='sn-fig'>" + clock_svg(15, 37, size=230) +
        "<figcaption>The long hand is 2 small marks past the 7: 35, 36, 37. The short hand is between 3 and 4. "
        "In the afternoon this is <b>3:37 pm</b>.</figcaption></figure>"
        "<h2>Units of time</h2>"
        + table(["Unit", "Equals"], [["1 minute", "60 seconds"], ["1 hour", "60 minutes"], ["1 day", "24 hours"],
                               ["1 week", "7 days"], ["1 fortnight", "14 days"], ["1 year", "12 months"],
                               ["1 year", "365 days (366 in a leap year)"]]) +
        ex("Hours to minutes", "2" + fr(1, 2) + " hours = ? minutes",
           "2 hours = 2 × 60 = 120 minutes. Half an hour = 30 minutes. 120 + 30 = 150.", "150 minutes") +
        ex("Minutes to hours", "200 minutes = ? hours and minutes",
           "3 × 60 = 180, and 200 − 180 = 20.", "3 hours 20 minutes") +
        "<h2>How long? Count on in jumps</h2>"
        "<p>An hour has 60 minutes, not 100, so do not just subtract the numbers. "
        "Jump to the next o’clock, then on in whole hours (through midday), then to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(T(9, 40), T(13, 15)) +
        "<figcaption>9:40 am to 10:00 am is 20 minutes, 10:00 am to 12:00 pm is 2 hours, 12:00 pm to 1:00 pm is 1 hour "
        "and 1:00 pm to 1:15 pm is 15 minutes. Altogether <b>3 hours 35 minutes</b>.</figcaption></figure>"
        + ex("Finding the end time", "A movie starts at 11:50 am and lasts 1 hour 50 minutes. When does it end?",
             "11:50 am + 1 hour = 12:50 pm. + 10 minutes = 1:00 pm. + 40 minutes = 1:40 pm.", "1:40 pm") +
        "<h2>Days between dates</h2>"
        "<p>To find how many days from one date to another in the same month, subtract the dates. "
        "Do not count the start day: no time has passed yet on that day.</p>"
        + ex("On a calendar", "How many days is it from 4 March to 19 March?", "19 − 4 = 15. Count the jumps: 5, 6 … 19.", "15 days") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["9:40 am to 11:15 am worked out as 1115 − 940 = 1 hour 75 minutes", "Count on: 20 minutes + 1 hour + 15 minutes = 1 hour 35 minutes"],
            ["2" + fr(1, 2) + " hours written as 250 minutes or 2 hours 50 minutes", "Half an hour is 30 minutes: 120 + 30 = 150 minutes"],
            ["20 minutes after 11:50 am written as 12:10 am", "After midday the time is pm: 12:10 pm"],
            ["Midday written as 12:00 am", "Midday is 12:00 pm. Midnight is 12:00 am"],
            ["4 March to 19 March counted as 16 days", "Do not count the start day: 19 − 4 = 15 days"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about time in Australia?",
     "a": "In the Australian Curriculum v9.0 (AC9M4M03), Year 4 students solve problems about how long things last, including times that go from am to pm, and convert between units of time such as hours, minutes and seconds."},
    {"q": "Is 12:00 pm midday or midnight?",
     "a": "12:00 pm is midday (noon) and 12:00 am is midnight. One minute after 11:59 am is 12:00 pm, so lunch at 12:30 is 12:30 pm."},
    {"q": "How do you work out how long something lasts across midday?",
     "a": "Count on in jumps: to the next o’clock, then whole hours through 12:00 pm, then the extra minutes. For 9:40 am to 1:15 pm that is 20 minutes + 3 hours + 15 minutes = 3 hours 35 minutes."},
    {"q": "Do you count the first day when working out days between dates?",
     "a": "No. From 4 March to 19 March is 19 − 4 = 15 days. Only count both days when you want the number of days an event is on, such as a camp from Monday to Friday (5 days)."},
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
    u["body_html"] = u["body_html"]
    return u


def gen():
    rnd = random.Random(4814)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_clocks(rnd, people), set_units(), set_durations(people), set_calendar(), set_problems(people)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    u = {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "time-am-pm-and-duration", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 4 Time: am, pm and How Long",
        "seo_title": "Year 4 Time Worksheets: am and pm, Units of Time, Duration and Calendars (Free, with Answer Key)",
        "short_title": "Time: am, pm and duration",
        "domain": "Measurement",
        "standard_code": "AC9M4M03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Solve problems involving the duration of time including situations involving “am” and “pm” and conversions between units of time",
        "meta_desc": "Free Year 4 maths worksheets on time for the Australian Curriculum (AC9M4M03): read analog clocks to the minute with am and pm, convert hours, minutes and seconds, work out how long events last across midday, count days on a calendar and solve timetable problems. 100 questions with an answer key.",
        "key_big": "An hour has 60 minutes, not 100. Count on in jumps through midday.",
        "key_sub": "am is midnight to midday, pm is midday to midnight, and midday is 12:00 pm. 2½ hours = 150 minutes. From 4 March to 19 March is 19 − 4 = 15 days: do not count the start day.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "time line")
    mark_large(u, "four analog clocks")
    mark_large(u, "calendar")
    mark_large(u, "school day timetable")
    mark_large(u, "swimming lesson timetable")
    mark_large(u, "movie session times")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
