# -*- coding: utf-8 -*-
"""
British Columbia Grade 4 Math: 12- and 24-hour time (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g4_time.py
Every analog clock is drawn from the time itself (the hour hand moves between the numbers).
Every answer is worked out in code from (hour, minute) values. Wrong answers come from real student mistakes:
hands swapped, an hour hand just before a number read as that number, the number the minute hand points to read
as minutes, a.m. and p.m. swapped, 15:00 read as 5 p.m. (dropping the 1), 12:30 a.m. written as 12:30,
an hour counted as 100 minutes (subtracting times like whole numbers).
Canadian English; 12-hour times written 3:45 p.m., 24-hour times 15:45. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Liam", "he"), ("Olivia", "she"), ("Ethan", "he"), ("Ava", "she"), ("Noah", "he"), ("Chloe", "she"),
          ("Arjun", "he"), ("Simran", "she"), ("Harjot", "he"), ("Jasleen", "she"), ("Wei", "he"), ("Mei", "she"),
          ("Ji-woo", "she"), ("Mateo", "he"), ("Hana", "she"), ("Lucas", "he"), ("Sofia", "she"), ("Kai", "he"),
          ("Emma", "she"), ("Owen", "he"), ("Leah", "she"), ("Ryan", "he"), ("Zara", "she"), ("Nadia", "she")]


# ------------------------------------------------------------ time formats
def h12(h24):
    return (h24 - 1) % 12 + 1


def tm12(h24, m):
    """12-hour digital: 3:45 p.m."""
    h24 %= 24
    assert not (h24 in (0, 12) and m == 0)
    return "%d:%02d %s" % (h12(h24), m, "a.m." if h24 < 12 else "p.m.")


def t24(h24, m):
    """24-hour digital: 15:45, 07:30, 00:30"""
    return "%02d:%02d" % (h24 % 24, m)


def dig(h, m):
    """digital without a.m./p.m.: 3:45"""
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


def time_value(s):
    """minutes after midnight for '3:45 p.m.' or '15:45' (so no two choices name the same moment)"""
    m = re.match(r"^(\d{1,2}):(\d\d)( a\.m\.| p\.m\.)?$", s)
    if not m:
        return s
    h, mm, ap = int(m.group(1)), int(m.group(2)), m.group(3)
    if ap:
        h = h % 12 + (12 if ap == " p.m." else 0)
    return h * 60 + mm


def add(h, m, d):
    t = (h * 60 + m + d) % (24 * 60)
    return t // 60, t % 60


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def tidy(t):
    """never a second period after a.m. / p.m."""
    return t.replace("m.</b>.", "m.</b>").replace("a.m..", "a.m.").replace("p.m..", "p.m.")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, key=None):
    """correct first + the first 3 different wrong answers (in order of how common the mistake is)."""
    key = key or (lambda x: x)
    seen = {key(correct)}
    seen_txt = {correct}
    pick = []
    for c in cands:
        if not c or key(c) in seen or c in seen_txt:
            continue
        seen.add(key(c))
        seen_txt.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": tidy(q), "c": [correct] + pick, "a": 0, "e": tidy(e)}


def tmcq(q, correct, cands, e):
    return mcq(q, correct, cands, e, key=time_value)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def face(cx, cy, R, k):
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
    return s


def clock_body(h, m, size, ox=0.0, oy=0.0):
    """Analog clock face. The hour hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) >= 12, (h, m)
    R = size / 2.0 - 6
    cx, cy = ox + size / 2.0, oy + size / 2.0
    k = R / 94.0
    s = face(cx, cy, R, k)
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.48 * math.cos(ah), cy + R * 0.48 * math.sin(ah), LINE, 8 * k))
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
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200, ring24=False):
    if not ring24:
        return svg_wrap(size, size, clock_body(h, m, size), "analog clock")
    # 24-hour clock: the afternoon hours (13 to 23, and 00) in green, in a ring outside the dial
    pad = 30
    W = size + 2 * pad
    c = W / 2.0
    R = size / 2.0 - 6
    s = [clock_body(h, m, size, pad, pad),
         "<g font-size='17' font-weight='700' fill='%s' text-anchor='middle'>" % GREEN]
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        r2 = R + 19
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (c + r2 * math.cos(a), c + r2 * math.sin(a) + 6,
                                                       "00" if n == 12 else str(n + 12)))
    s.append("</g>")
    return svg_wrap(W, W, "".join(s), "analog clock with 24-hour numbers")


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


def digital_svg(txt):
    W, H = 200 if len(txt) <= 5 else 290, 84
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='#fff' stroke='%s' stroke-width='4'/>" % (W - 6, H - 6, GREEN),
         "<rect x='16' y='14' width='%d' height='%d' rx='6' fill='#eef5f0'/>" % (W - 32, H - 28),
         "<text x='%d' y='%d' font-size='40' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Consolas, Menlo, monospace'>%s</text>" % (W / 2, H / 2 + 14, LINE, txt)]
    return svg_wrap(W, H, "".join(s), "digital clock")


def timeline_svg(h1, m1, h2, m2, fmt, W=420):
    """Start -> next o'clock -> end, the jumps labelled."""
    t1, t2 = h1 * 60 + m1, h2 * 60 + m2
    mid = (h1 + 1) * 60 if m1 else None
    L, R, Y = 56, W - 56, 70

    def X(t):
        return L + (R - L) * (t - t1) / float(t2 - t1)
    pts = [t1] + ([mid] if mid and t1 < mid < t2 else []) + [t2]
    xs = [X(t) for t in pts]
    assert all(b - a >= 90 for a, b in zip(xs, xs[1:])), (h1, m1, h2, m2)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for t in pts:
        lab = fmt(t // 60, t % 60) if t % (12 * 60) or t % 60 else ("12:00 noon" if t == 720 else fmt(t // 60, 0))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X(t), Y - 10, X(t), Y + 10, LINE))
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X(t), Y + 32, LINE, lab))
    for a, b in zip(pts, pts[1:]):
        x1, x2 = X(a), X(b)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, Y - 12, (x1 + x2) / 2, Y - 52, x2, Y - 12, RED))
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>+%d min</text>"
                 % ((x1 + x2) / 2, Y - 40, RED, b - a))
    return svg_wrap(W, 112, "".join(s), "time line")


def ferry_svg(rows):
    """Ferry timetable in 24-hour time: leaves Tsawwassen / arrives Swartz Bay."""
    CW, RH, TOP = 170, 30, 34
    W = 2 * CW + 4
    H = TOP + RH * (len(rows) + 1) + 4
    s = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (W - 4, TOP, GREEN),
         "<text x='%d' y='25' font-size='17' font-weight='700' fill='#fff' text-anchor='middle'>Ferry timetable (24-hour time)</text>" % (W / 2),
         "<rect x='2' y='%d' width='%d' height='%d' fill='#cfe6d6'/>" % (2 + TOP, W - 4, RH)]
    for j, head in enumerate(["Leaves Tsawwassen", "Arrives Swartz Bay"]):
        s.append("<text x='%.0f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (2 + CW * j + CW / 2.0, 2 + TOP + 21, LINE, head))
    for i, (a, b) in enumerate(rows):
        y = 2 + TOP + RH * (i + 1)
        if i % 2:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
        for j, t in enumerate([a, b]):
            s.append("<text x='%.0f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (2 + CW * j + CW / 2.0, y + 21, LINE, t24(*t)))
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, LINE))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (2 + CW, 2 + TOP, 2 + CW, H - 2, LINE))
    return svg_wrap(W, H, "".join(s), "ferry timetable")


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
        mm = "The long minute hand points to <b>%d</b>. Count by 5s: %d × 5 = <b>%d minutes</b>." % (n, n, m)
    elif n == 0:
        mm = "The long minute hand is <b>%d small mark%s</b> past the 12: <b>%s</b>." % (extra, "" if extra == 1 else "s", mins(m))
    else:
        mm = ("The long minute hand is %d small mark%s past the %d. Count by 5s to %d, then by 1s: <b>%d minutes</b>."
              % (extra, "" if extra == 1 else "s", n, n * 5, m))
    if m == 0:
        hh = "The short hour hand points to <b>%d</b>." % h
    else:
        hh = ("The short hour hand is between <b>%d</b> and <b>%d</b>. It has not reached %d yet, so the hour is <b>%d</b>."
              % (h, h % 12 + 1, h % 12 + 1, h))
    return hh + " " + mm


def swapped(h, m):
    """hands swapped: short hand read as the minutes, long hand read as the hour"""
    return dig(m // 5 or 12, (h % 12) * 5)


# ============================================================ set 1: analog clocks to the minute
def set_read(rnd):
    its = []
    used = []

    def pick(ms):
        while True:
            h = rnd.randint(1, 12)
            m = rnd.choice(ms)
            if (h, m) in used or hands_gap(h, m) < 18 or h in [x[0] for x in used][-3:]:
                continue
            used.append((h, m))
            return h, m

    # to the 5 minutes (warm-up), then to the minute
    plan = [[10], [25], [40], [55]] + [list(range(lo, hi + 1)) for lo, hi in
                                      [(1, 4), (11, 14), (16, 19), (21, 24), (31, 34), (36, 39), (41, 44), (46, 49),
                                       (51, 54), (56, 59)]]
    for ms in plan:
        if len(ms) > 1:
            ms = [x for x in ms if x % 5]
        h, m = pick(ms)
        n = m // 5
        right = dig(h, m)
        c = []
        if m >= 30:
            c.append(dig(h + 1, m))                       # hour hand just before the next number read as that number
        c.append(swapped(h, m))                           # hands swapped
        if m % 5 and n:
            c.append(dig(h, n * 5))                       # small marks not counted
        if n:
            c.append(dig(h, n))                           # the number the minute hand is near read as minutes
        c += [dig(h, 60 - m), dig(h + 1, m), dig(h - 1, m)]
        e = "%s So the time is <b>%s</b>." % (hand_text(h, m), right)
        if m >= 30:
            e += " (Not %s: the hour hand has not reached %d yet.)" % (dig(h + 1, m), h12(h + 1))
        elif m % 5 and n:
            e += " (Not %s: count the small marks after the %d too.)" % (dig(h, n * 5), n)
        else:
            e += " (Not %s: that swaps the hands. The short hand is the hour.)" % swapped(h, m)
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show?", right, c, e))
    # clock -> words
    for ms in [[x for x in range(16, 29) if x % 5], [x for x in range(37, 44) if x % 5], [x for x in range(47, 54) if x % 5]]:
        h, m = pick(ms)
        right = words(h, m)
        if m < 30:
            c = ["%s to %d" % (mins(m), h12(h)), "%s past %d" % (mins(m), h12(h + 1)),
                 "%s to %d" % (mins(60 - m), h12(h)), "%s past %d" % (mins(m + 1), h12(h))]
            e = ("%s The long hand is on the right side of the clock, so we say <b>past %d</b>: <b>%s</b>."
                 % (hand_text(h, m), h12(h), right))
        else:
            c = ["%s to %d" % (mins(60 - m), h12(h)), "%s past %d" % (mins(60 - m), h12(h)),
                 "%s to %d" % (mins(m), h12(h + 1)), "%s to %d" % (mins(60 - m + 1), h12(h + 1))]
            e = ("%s That is after half past, so count the minutes <b>to</b> the next hour: 60 − %d = %d. "
                 "It is <b>%s</b>. (Not “to %d”: %d o’clock has already passed.)"
                 % (hand_text(h, m), m, 60 - m, right, h12(h), h12(h)))
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show? Choose the words.", right, c, e))
    # minutes until the next o'clock
    for ms in [[x for x in range(33, 39) if x % 5], [x for x in range(42, 49) if x % 5], [x for x in range(51, 58) if x % 5]]:
        h, m = pick(ms)
        right = mins(60 - m)
        c = [mins(100 - m), mins(60 - m // 5 * 5), mins(m), mins(60 - m + 10)]
        e = ("%s It is %s. An hour has <b>60 minutes</b>, so there are 60 − %d = <b>%s</b> until %d o’clock. "
             "(Not %d: an hour is 60 minutes, not 100.)" % (hand_text(h, m), dig(h, m), m, right, h12(h + 1), 100 - m))
        its.append(mcq(fig(clock_svg(h, m)) + "How many minutes is it until <b>%d o’clock</b>?" % h12(h + 1), right, c, e,
                       key=dur_value))
    assert len(its) == 20
    return {"title": "Reading analog clocks to the minute", "items": its}


# ============================================================ set 2: analog and digital
def set_match(rnd):
    its = []
    # A to D: which analog clock shows the digital time
    pos = [0, 1, 2, 3]
    rnd.shuffle(pos)
    abcd = []
    for (h, m), p in zip([(3, 47), (9, 17), (6, 53), (11, 8)], pos):
        others = [(h - 1, m), (h, 60 - m), (m // 5, (h % 12) * 5)]
        times = list(others)
        times.insert(p, (h, m))
        assert len(set((a % 12, b) for a, b in times)) == 4
        L = "ABCD"
        why = []
        for t in others:
            if t == (h - 1, m):
                why.append("clock %s shows %s (its hour hand is between %d and %d)" % (L[times.index(t)], dig(*t), h12(h - 1), h12(h)))
            elif t == (h, 60 - m):
                why.append("clock %s shows %s" % (L[times.index(t)], dig(*t)))
            else:
                why.append("clock %s has the hands swapped (%s)" % (L[times.index(t)], dig(*t)))
        e = ("At %s the long hand is %d small mark%s past the %d (%d minutes), and the short hand is between %d and %d. "
             "That is clock <b>%s</b>. Not the others: %s."
             % (dig(h, m), m % 5, "" if m % 5 == 1 else "s", m // 5, m, h12(h), h12(h + 1), L[p], "; ".join(why)))
        abcd.append({"q": fig(four_clocks_svg(times)) + "Which analog clock shows <b>%s</b>?" % dig(h, m),
                     "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True})
    # digital -> words
    dw = []
    for h, m in [(4, 20), (8, 45), (2, 51), (7, 36)]:
        right = words(h, m)
        if m == 45:
            c = ["quarter to 8", "quarter past 8", "45 to 9", "15 past 9"]
            e = "8:45 is 45 minutes past 8. 60 − 45 = 15, and 15 minutes is a quarter of an hour. So it is <b>quarter to 9</b>."
        elif m < 30:
            c = ["20 to 4", "20 past 5", "20 to 5", "40 to 4"]
            e = "4:20 is 20 minutes after 4 o’clock. It is before half past, so say <b>past</b>: <b>20 past 4</b>."
        else:
            c = ["%s to %d" % (mins(60 - m), h12(h)), "%s past %d" % (mins(60 - m), h12(h + 1)),
                 "%s to %d" % (mins(m), h12(h + 1)), "%s to %d" % (mins(60 - m + 10), h12(h + 1))]
            e = ("%s is %d minutes past %d. That is after half past, so say <b>to</b> the next hour. "
                 "60 − %d = %d, so it is <b>%s</b>. (Not “to %d”: %d o’clock has already passed.)"
                 % (dig(h, m), m, h12(h), m, 60 - m, right, h12(h), h12(h)))
        dw.append(mcq(fig(digital_svg(dig(h, m))) + "How do we say this digital time in words?", right, c, e))
    # words -> digital
    wd = []
    for h, m in [(10, 15), (5, 40), (1, 33), (11, 52)]:
        w = words(h, m)
        right = dig(h, m)
        if m > 30:
            c = [dig(h + 1, 60 - m), dig(h + 1, m), dig(h, 60 - m), dig(h, 100 - (60 - m)) if 100 - (60 - m) < 60 else None,
                 dig(h - 1, m)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d minutes past %d: <b>%s</b>. "
                 "(Not %s: that is %d minutes <b>after</b> %d o’clock.)"
                 % (w, 60 - m, h12(h + 1), 60 - m, m, m, h12(h), right, dig(h + 1, 60 - m), 60 - m, h12(h + 1)))
        else:
            c = [dig(h, 45), dig(h + 1, 15), dig(h - 1, 45), dig(h, 25)]
            e = "Quarter past means 15 minutes <b>after</b> the hour. So quarter past 10 is <b>10:15</b>."
        wd.append(mcq("Write <b>%s</b> as a digital time." % w, right, c, e))
    # where is the hour hand?
    hh = []
    for h, m in [(2, 14), (10, 30), (7, 48), (4, 53)]:
        a, b, c3 = h12(h), h12(h + 1), h12(h + 2)
        if m == 30:
            right = "halfway between %d and %d" % (a, b)
            c = ["exactly on %d" % a, "halfway between %d and %d" % (h12(h - 1), a), "exactly on %d" % b]
            e = "At %s it is half past %d. The hour hand has gone half of the way from %d to %d: <b>%s</b>." % (dig(h, m), a, a, b, right)
        elif m < 30:
            right = "just past %d" % a
            c = ["just before %d" % a, "just past %d" % b, "exactly on %d" % a]
            e = ("At %s only %d minutes have passed since %d o’clock. The hour hand has moved only a little past %d: <b>%s</b>. "
                 "It points exactly on %d only at %d:00." % (dig(h, m), m, a, a, right, a, a))
        else:
            right = "just before %d" % b
            c = ["just past %d" % b, "just past %d" % a, "exactly on %d" % a]
            e = ("At %s it is %d minutes to %d. The hour hand is almost at %d, but it has not reached it: <b>%s</b>. "
                 "(It is still %d o’clock and something, so the digital time starts with %d.)"
                 % (dig(h, m), 60 - m, b, b, right, a, a))
        hh.append(mcq(fig(digital_svg(dig(h, m))) + "The digital clock shows this time. Where is the <b>short hour hand</b> "
                      "on an analog clock?", right, c, e))
    # where is the minute hand?
    mh = []
    for m in [23, 16, 48, 37]:
        n, k = divmod(m, 5)
        mk = lambda kk, word, nn: "%d small mark%s %s the %d" % (kk, "" if kk == 1 else "s", word, nn)
        right = mk(k, "past", n)
        tens, ones = divmod(m, 10)
        c = [mk(ones, "past", tens), mk(k, "before", n), mk(k, "past", n + 1)]
        e = ("Count by 5s to the %d: %d × 5 = %d. Then count on by 1s: %d more makes %d. So the long hand is <b>%s</b>. "
             "(Not %s: the numbers on a clock count by 5s, so you cannot read the digits %d and %d separately.)"
             % (n, n, n * 5, k, m, right, mk(ones, "past", tens), tens, ones))
        mh.append(mcq(fig(digital_svg(dig(rnd.choice([3, 5, 8, 9]), m))) + "Where does the <b>long minute hand</b> point "
                      "on an analog clock?", right, c, e))
    its = [wd[0], dw[0], dw[1], abcd[0], hh[0], mh[0], wd[1], hh[1], abcd[1], mh[1], dw[2], wd[2], abcd[2], hh[2],
           mh[2], dw[3], wd[3], abcd[3], hh[3], mh[3]]
    assert len(its) == 20
    return {"title": "Matching analog and digital clocks", "items": its}


# ============================================================ set 3: a.m. and p.m.
CONTEXTS = [
    ("{n} wakes up for an early hockey practice.", 5, 31, 52),
    ("{n} waits for the school bus in the morning.", 8, 6, 24),
    ("{n} hikes in Stanley Park on Saturday morning.", 10, 36, 54),
    ("{n} eats lunch at school.", 12, 6, 24),
    ("{n} watches for orcas from the ferry in the afternoon.", 14, 36, 54),
    ("{n} goes to soccer practice after school.", 16, 6, 28),
    ("{n}’s family eats dinner in the evening.", 18, 31, 52),
    ("{n} goes to bed in the evening.", 20, 6, 28),
]


def set_ampm(rnd, people):
    its = []
    its.append(mcq("Which times are <b>a.m.</b> times?", "from midnight to noon",
                   ["from noon to midnight", "only times at night", "only times after school"],
                   "<b>a.m.</b> times go from midnight to noon (night and morning). <b>p.m.</b> times go from noon to "
                   "midnight (afternoon and evening)."))
    its.append(mcq("What is <b>midnight</b>?", "12 o’clock at night",
                   ["12 o’clock in the middle of the day", "9 o’clock at night", "the time the sun goes down"],
                   "<b>Midnight</b> is 12 o’clock at night, when one day ends and the next day starts. "
                   "12 o’clock in the middle of the day is <b>noon</b>."))
    its.append(mcq("Which time is in the <b>afternoon</b>?", "3:20 p.m.", ["3:20 a.m.", "11:20 a.m.", "8:20 a.m."],
                   "The afternoon is after noon, so it is a <b>p.m.</b> time. 3:20 a.m. is in the middle of the night. "
                   "So the answer is <b>3:20 p.m.</b>"))
    nm, pr = next(people)
    its.append(mcq("%s eats breakfast at 7:25 in the morning. Is that a.m. or p.m.?" % nm,
                   "a.m., because it is before noon",
                   ["p.m., because it is before noon", "p.m., because it is after noon", "a.m., because it is after noon"],
                   "Morning times are before noon. Times before noon are <b>a.m.</b> times. So breakfast is at 7:25 a.m."))
    # sensible times
    for q, right, c, e in [
        ("Which is a sensible time for school to start?", "8:40 a.m.", ["8:40 p.m.", "3:40 a.m.", "11:40 p.m."],
         "School starts in the morning, so it is an <b>a.m.</b> time. 3:40 a.m. is the middle of the night. So it is <b>8:40 a.m.</b>"),
        ("Which is a sensible time for the summer fireworks at English Bay in Vancouver?", "10:00 p.m.",
         ["10:00 a.m.", "6:00 a.m.", "1:00 p.m."],
         "Fireworks need a dark sky, so they are late in the evening: a <b>p.m.</b> time. 10:00 a.m. is in the morning. "
         "So it is <b>10:00 p.m.</b>"),
        ("Which is a sensible time for a Saturday morning ski lesson on Grouse Mountain?", "9:30 a.m.",
         ["9:30 p.m.", "2:30 a.m.", "12:30 a.m."],
         "A morning lesson is before noon, so it is an <b>a.m.</b> time. 2:30 a.m. and 12:30 a.m. are in the middle of the "
         "night. So it is <b>9:30 a.m.</b>"),
        ("Which is a sensible time for school to end?", "2:55 p.m.", ["2:55 a.m.", "8:55 p.m.", "10:55 a.m."],
         "School ends in the afternoon, after noon, so it is a <b>p.m.</b> time. 2:55 a.m. is in the middle of the night. "
         "So it is <b>2:55 p.m.</b>"),
    ]:
        its.append(tmcq(q, right, c, e))
    # clocks with a time of day -> 12-hour digital with a.m. / p.m.
    ctx = CONTEXTS[:]
    rnd.shuffle(ctx)
    for sent, H, lo, hi in ctx:
        ms = [x for x in range(lo, hi + 1) if x % 5 and hands_gap(H, x) >= 18]
        m = rnd.choice(ms)
        n = m // 5
        nm, pr = next(people)
        right = tm12(H, m)
        c = [tm12(H + 12, m)]                             # a.m. and p.m. swapped
        if m >= 30:
            c.append(tm12(H + 1, m))                      # hour hand just before the next number
        if n:
            c.append(tm12(H, n))
        c += [tm12(H, 60 - m), tm12(H + 1, m), tm12(H - 1, m)]
        why = "It is in the morning, so it is <b>a.m.</b>" if H < 12 else "It is after noon, so it is <b>p.m.</b>"
        e = "%s %s So the time is <b>%s</b>" % (hand_text(H, m), why, right)
        swap = (H + 12) % 24
        e += " (Not %s: that is %s.)" % (c[0], "in the middle of the night" if swap < 5 else "late at night" if swap >= 22 else
                                         ("in the morning" if swap < 12 else "in the afternoon or evening"))
        q = fig(clock_svg(H, m)) + sent.format(n=nm) + " What is the time?"
        its.append(tmcq(q, right, c, e))
    # order, across noon
    its.append(tmcq("Which time is <b>earliest</b> in the day?", "11:45 a.m.", ["1:15 p.m.", "2:30 p.m.", "12:10 p.m."],
                    "a.m. times come before noon and p.m. times come after noon. So <b>11:45 a.m.</b> is the earliest, "
                    "even though 11 is a bigger number than 1 or 2."))
    its.append(mcq("Put these times in order from <b>earliest</b> to <b>latest</b> in one day: "
                   "4:00 p.m., 6:30 a.m., 9:15 p.m., 10:00 a.m.",
                   "6:30 a.m., 10:00 a.m., 4:00 p.m., 9:15 p.m.",
                   ["4:00 p.m., 6:30 a.m., 9:15 p.m., 10:00 a.m.", "10:00 a.m., 9:15 p.m., 6:30 a.m., 4:00 p.m.",
                    "6:30 a.m., 4:00 p.m., 9:15 p.m., 10:00 a.m."],
                   "All a.m. times come first, then the p.m. times. a.m.: 6:30, then 10:00. p.m.: 4:00, then 9:15. "
                   "So the order is <b>6:30 a.m., 10:00 a.m., 4:00 p.m., 9:15 p.m.</b>"))
    its.append(mcq("How many hours is it from <b>10:00 a.m.</b> to <b>3:00 p.m.</b>?", "5 hours",
                   ["7 hours", "6 hours", "13 hours"],
                   "10:00 a.m. → 12:00 noon is 2 hours. 12:00 noon → 3:00 p.m. is 3 hours. 2 + 3 = <b>5 hours</b>. "
                   "(Not 7: 10 − 3 = 7 does not work across noon. Not 6: count the jumps, not the numbers.)",
                   key=dur_value))
    its.append(mcq("How many hours is it from <b>8:00 p.m.</b> to <b>6:00 a.m.</b> the next morning?", "10 hours",
                   ["2 hours", "14 hours", "11 hours"],
                   "8:00 p.m. → 12:00 midnight is 4 hours. Midnight → 6:00 a.m. is 6 hours. 4 + 6 = <b>10 hours</b>. "
                   "(Not 2: 8 − 6 = 2 does not work across midnight.)", key=dur_value))
    assert len(its) == 20
    order = [0, 2, 3, 1, 4, 5, 8, 9, 6, 10, 11, 7, 12, 16, 13, 14, 17, 15, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "a.m. and p.m.", "items": [its[i] for i in order]}


# ============================================================ set 4: 12-hour and 24-hour time
def set_convert(rnd):
    its = []
    # p.m. -> 24-hour
    for H, m in [(15, 45), (13, 20), (18, 5), (21, 38)]:
        right = t24(H, m)
        c = ["%02d:%02d" % (H - 12, m), t24(H - 2, m), t24(H + 1, m), t24(H - 1, m)]
        e = ("p.m. times are after noon. Add 12 to the hour: %d + 12 = %d. So %s is <b>%s</b>. "
             "(Not %s: that would be a morning time.)" % (H - 12, H, tm12(H, m), right, "%02d:%02d" % (H - 12, m)))
        its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(H, m), right, c, e))
    # a.m. -> 24-hour
    for H, m in [(7, 30), (9, 52)]:
        right = t24(H, m)
        c = [t24(H + 12, m), t24(H + 10, m), t24(H + 1, m)]
        e = ("a.m. times are before noon, so the hour stays the same. A 24-hour time has 4 digits, so put a 0 in front: "
             "%s is <b>%s</b>. (Not %s: that is in the evening.)" % (tm12(H, m), right, t24(H + 12, m)))
        its.append(mcq("Write <b>%s</b> in 24-hour time." % tm12(H, m), right, c, e))
    # 24-hour -> p.m. (mistake: drop the 1, so 15:00 = 5 p.m.)
    for H, m in [(15, 0), (17, 25), (14, 10), (19, 47)]:
        right = tm12(H, m)
        c = []
        if H - 10 <= 12:
            c.append("%d:%02d p.m." % (H - 10, m))       # 15:00 -> 5:00 p.m.
        c += [tm12(H - 12, m), tm12(H - 1, m), tm12(H + 1, m)]
        e = ("Hours from 13 to 23 are p.m. times. Take away 12: %d − 12 = %d. So %s is <b>%s</b>."
             % (H, H - 12, t24(H, m), right))
        if H - 10 <= 12:
            e += " (Not %d:%02d p.m.: do not just drop the 1. %d − 12 = %d, not %d.)" % (H - 10, m, H, H - 12, H - 10)
        its.append(tmcq("Write <b>%s</b> as a 12-hour time." % t24(H, m), right, c, e))
    # 24-hour -> a.m.
    its.append(tmcq("Write <b>08:15</b> as a 12-hour time.", "8:15 a.m.", ["8:15 p.m.", "10:15 p.m.", "6:15 p.m."],
                    "The hour 08 is less than 12, so it is a morning time: <b>a.m.</b> Drop the 0 at the front: <b>8:15 a.m.</b> "
                    "(Not 8:15 p.m.: only hours from 12 to 23 are p.m.)"))
    # midnight and noon
    its.append(mcq("Write <b>00:30</b> as a 12-hour time.", "12:30 a.m.", ["12:30 p.m.", "0:30 p.m.", "1:30 a.m."],
                    "00 is the hour just after <b>midnight</b>. In 12-hour time we call it 12 a.m. So 00:30 is "
                    "<b>12:30 a.m.</b>, 30 minutes after midnight. (12:30 p.m. is 30 minutes after noon.)"))
    its.append(mcq("Write <b>12:20 a.m.</b> in 24-hour time.", "00:20", ["12:20", "24:20", "01:20"],
                   "12:20 a.m. is 20 minutes after <b>midnight</b>. In 24-hour time, the hour after midnight is 00. "
                   "So it is <b>00:20</b>. (12:20 is 20 minutes after noon.)"))
    its.append(mcq("Write <b>12:45 p.m.</b> in 24-hour time.", "12:45", ["24:45", "00:45", "13:45"],
                   "12:45 p.m. is 45 minutes after <b>noon</b>. Noon is 12:00 in 24-hour time, so do not add 12. "
                   "It is <b>12:45</b>."))
    # time of day
    its.append(mcq("Which 24-hour time is in the <b>evening</b>?", "19:30", ["07:30", "09:30", "11:30"],
                   "Hours from 13 to 23 are p.m. times. 19 − 12 = 7, so 19:30 is 7:30 p.m., in the evening. "
                   "07:30, 09:30 and 11:30 are all a.m. times. The answer is <b>19:30</b>."))
    # analog clock with a time of day -> 24-hour
    for H, m, part in [(20, 25, "in the evening"), (13, 52, "in the afternoon"), (22, 11, "at night")]:
        right = t24(H, m)
        n = m // 5
        c = ["%02d:%02d" % (H - 12, m), t24(H - 2, m)]
        if m >= 30:
            c.append(t24(H + 1, m))
        if n and m % 5:
            c.append(t24(H, n))
        c += [t24(H, 60 - m), t24(H + 1, m)]
        e = ("%s It is %s %s, so it is %s. Add 12 to the hour: %d + 12 = %d. So it is <b>%s</b>."
             % (hand_text(H, m), dig(H, m), part, tm12(H, m), h12(H), H, right))
        its.append(mcq(fig(clock_svg(H, m)) + "The clock shows a time %s. Write it in 24-hour time." % part, right, c, e))
    # 24-hour clock face
    H, m = 17, 40
    its.append(mcq(fig(clock_svg(H, m, ring24=True)) + "The green numbers around the clock show the hours after noon. "
                   "This clock shows a time in the afternoon. What is the 24-hour time?", "17:40",
                   ["05:40", "18:40", "15:40"],
                   "The short hand is between 5 and 6, so it is 5:40 p.m. In the afternoon, read the green number "
                   "next to the 5: 17. So it is <b>17:40</b>. (Not 18:40: the hour hand has not reached 6, or 18, yet.)"))
    # words -> 24-hour
    its.append(mcq("Which 24-hour time is <b>quarter to 4 in the afternoon</b>?", "15:45",
                   ["16:45", "16:15", "03:45"],
                   "Quarter to 4 is 15 minutes before 4:00, so it is 3:45 p.m. Add 12 to the hour: 3 + 12 = 15. "
                   "It is <b>15:45</b>. (Not 16:45: quarter to 4 is before 4 o’clock.)"))
    assert len(its) == 20
    order = [0, 4, 1, 6, 2, 5, 10, 7, 8, 3, 9, 14, 11, 12, 13, 15, 16, 18, 17, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Converting 12-hour and 24-hour time", "items": [its[i] for i in order]}


# ============================================================ set 5: elapsed time and schedules
FERRY = [((h, 0), add(h, 0, 95)) for h in (9, 11, 13, 15, 17, 19)]


def how_long(q, h1, m1, h2, m2, wrong, e):
    d = (h2 * 60 + m2) - (h1 * 60 + m1)
    assert d > 0
    return mcq(q, dur(d), wrong, e, key=dur_value)


def set_elapsed(rnd, people):
    its = {}
    FT = fig(ferry_svg(FERRY))
    assert FERRY[1] == ((11, 0), (12, 35))
    # 1 same hour
    its[1] = how_long("Recess starts at <b>10:10 a.m.</b> and ends at <b>10:25 a.m.</b> How long is recess?",
                      10, 10, 10, 25, ["25 minutes", "10 minutes", "35 minutes"],
                      "Both times are in the same hour. 25 − 10 = <b>15 minutes</b>.")
    # 2 hockey practice early morning (100-minute mistake)
    nm, pr = next(people)
    assert (7 * 60 + 30) - (6 * 60 + 15) == 75
    its[2] = how_long("%s’s hockey practice is from <b>6:15 a.m.</b> to <b>7:30 a.m.</b> How long is practice?" % nm,
                      6, 15, 7, 30, ["115 minutes", "1 hour 45 minutes", "45 minutes"],
                      "6:15 to 7:15 is 1 hour. 7:15 to 7:30 is 15 minutes. So practice is <b>1 hour 15 minutes</b>. "
                      "(Not 115 minutes: 730 − 615 = 115 treats an hour as 100 minutes.)")
    # 3 lunch across noon
    its[3] = how_long(fig(timeline_svg(11, 40, 12, 20, tm12)) + "Lunch starts at <b>11:40 a.m.</b> and ends at "
                      "<b>12:20 p.m.</b> How long is lunch?", 11, 40, 12, 20,
                      ["80 minutes", "20 minutes", "1 hour 40 minutes"],
                      "Count on to 12:00 noon first: 11:40 a.m. to 12:00 is 20 minutes. Then 12:00 to 12:20 p.m. is 20 minutes. "
                      "20 + 20 = <b>40 minutes</b>. (Not 80: 1220 − 1140 = 80 treats an hour as 100 minutes.)")
    # 4 SkyTrain
    nm, pr = next(people)
    its[4] = how_long(fig(timeline_svg(15, 52, 16, 9, t24)) + "%s gets on the SkyTrain at Waterfront Station at <b>15:52</b>. "
                      "%s gets off at Metrotown at <b>16:09</b>. How long is the ride?" % (nm, pr.capitalize()),
                      15, 52, 16, 9, ["57 minutes", "43 minutes", "27 minutes"],
                      "Count on to the next hour first: 15:52 to 16:00 is 8 minutes. Then 16:00 to 16:09 is 9 minutes. "
                      "8 + 9 = <b>17 minutes</b>. (Not 57: 1609 − 1552 = 57 treats an hour as 100 minutes.)")
    # 5 ferry: arrival
    its[5] = tmcq(FT + "The ferry leaves Tsawwassen at <b>11:00</b>. What time does it arrive at Swartz Bay?",
                  "12:35", ["14:35", "10:35", "13:35"],
                  "Find 11:00 in the “Leaves Tsawwassen” column. Look across that row: it arrives at <b>12:35</b>. "
                  "(10:35 and 14:35 are on other rows.)")
    # 6 ferry: crossing time
    its[6] = how_long(FT + "How long does the ferry take to go from Tsawwassen to Swartz Bay?", 11, 0, 12, 35,
                      ["135 minutes", "2 hours 35 minutes", "35 minutes"],
                      "Take any row, such as 11:00 to 12:35. 11:00 to 12:00 is 1 hour. 12:00 to 12:35 is 35 minutes. "
                      "So the crossing takes <b>1 hour 35 minutes</b>. (Not 135 minutes: 1235 − 1100 = 135 treats an hour "
                      "as 100 minutes. 1 hour 35 minutes is 95 minutes.)")
    # 7 minutes -> hours and minutes
    its[7] = mcq("A lacrosse practice lasts <b>90 minutes</b>. How long is that in hours and minutes?",
                 "1 hour 30 minutes", ["1 hour 10 minutes", "9 hours", "2 hours 30 minutes"],
                 "60 minutes make 1 hour. 90 − 60 = 30 minutes left over. So 90 minutes = <b>1 hour 30 minutes</b>. "
                 "(1 hour 10 minutes would be 70 minutes.)", key=dur_value)
    # 8 hockey practice end time in 24-hour time
    assert add(17, 45, 80) == (19, 5)
    its[8] = tmcq("A hockey practice starts at <b>17:45</b>. It lasts <b>1 hour 20 minutes</b>. What time does it end?",
                  "19:05", ["19:25", "18:05", "20:05"],
                  "Add 1 hour: 17:45 → 18:45. Then add 20 minutes: 15 minutes takes you to 19:00, and 5 more makes "
                  "<b>19:05</b>. (Not 19:25: that adds 1 hour 40 minutes.)")
    # 9 count back
    nm, pr = next(people)
    assert add(6, 15, -35) == (5, 40)
    its[9] = tmcq("%s’s hockey practice starts at <b>6:15 a.m.</b> %s leaves home <b>35 minutes</b> before. "
                  "What time does %s leave home?" % (nm, pr.capitalize(), pr), "5:40 a.m.",
                  ["6:50 a.m.", "5:40 p.m.", "5:20 a.m."],
                  "Count back 15 minutes to 6:00 a.m. 35 − 15 = 20, so count back 20 more minutes: <b>5:40 a.m.</b> "
                  "(6:50 a.m. is 35 minutes <b>after</b> 6:15.)")
    # 10 ferry: which sailing, from a 12-hour arrival time
    nm, pr = next(people)
    assert FERRY[3] == ((15, 0), (16, 35))
    its[10] = tmcq(FT + "%s arrives at Swartz Bay at <b>4:35 p.m.</b> Which sailing did %s take from Tsawwassen?" % (nm, pr),
                   "15:00", ["13:00", "17:00", "16:00"],
                   "4:35 p.m. in 24-hour time is 4 + 12 = 16, so 16:35. Find 16:35 in the “Arrives” column. "
                   "That ferry leaves Tsawwassen at <b>15:00</b>. (Not 13:00: that ferry arrives at 14:35, which is 2:35 p.m.)")
    # 11 hockey game on TV
    its[11] = how_long("A hockey game on TV starts at <b>19:00</b> and ends at <b>21:40</b>. How long is it?",
                       19, 0, 21, 40, ["3 hours 40 minutes", "240 minutes", "1 hour 40 minutes"],
                       "19:00 to 21:00 is 2 hours. 21:00 to 21:40 is 40 minutes. So the game is <b>2 hours 40 minutes</b>. "
                       "(Count the jumps 19 → 20 → 21: that is 2 hours, not 3. Not 240 minutes: 2140 − 1900 = 240 treats an hour as 100 minutes.)")
    # 12 SkyTrain Expo Line
    assert add(8, 47, 39) == (9, 26)
    its[12] = tmcq("A SkyTrain leaves Waterfront at <b>08:47</b>. The ride to King George Station takes <b>39 minutes</b>. "
                   "What time does it get there?", "09:26", ["08:26", "10:26", "09:36"],
                   "From 08:47, 13 minutes takes you to 09:00. 39 − 13 = 26 more minutes makes <b>09:26</b>. "
                   "(Not 08:26: going past 60 minutes means the hour goes up by 1.)")
    # 13 ferry: latest sailing
    nm, pr = next(people)
    assert FERRY[4] == ((17, 0), (18, 35))
    its[13] = tmcq(FT + "%s’s family must be at Swartz Bay by <b>7:00 p.m.</b> What is the latest ferry they can take "
                   "from Tsawwassen?" % nm, "17:00", ["19:00", "15:00", "18:35"],
                   "7:00 p.m. is 19:00. Look down the “Arrives” column for the last time before 19:00: 18:35. "
                   "That ferry leaves at <b>17:00</b>. (The 19:00 ferry leaves at 7:00 p.m., so it arrives too late. "
                   "18:35 is an arrival time, not a sailing.)")
    # 14 field trip
    assert (14 * 60 + 40) - (9 * 60 + 15) == 325
    its[14] = how_long("The class field trip bus leaves for Stanley Park at <b>09:15</b>. It gets back to school at "
                       "<b>14:40</b>. How long is the trip?", 9, 15, 14, 40,
                       ["5 hours 55 minutes", "4 hours 25 minutes", "5 hours 40 minutes"],
                       "09:15 to 14:15 is 5 hours (10, 11, 12, 13, 14). 14:15 to 14:40 is 25 minutes. "
                       "So the trip is <b>5 hours 25 minutes</b>.")
    # 15 ferry: waiting time
    nm, pr = next(people)
    its[15] = how_long(FT + "%s gets to the Tsawwassen terminal at <b>13:20</b>, just after the 13:00 ferry has left. "
                       "How long must %s wait for the next ferry?" % (nm, pr), 13, 20, 15, 0,
                       ["1 hour 80 minutes", "2 hours", "1 hour 20 minutes"],
                       "The next ferry is at 15:00. 13:20 to 14:00 is 40 minutes. 14:00 to 15:00 is 1 hour. "
                       "So the wait is <b>1 hour 40 minutes</b>. (Not 1 hour 80 minutes: 1500 − 1320 = 180 treats an hour as 100 minutes.)")
    # 16 Horseshoe Bay - Departure Bay
    assert add(10, 40, 100) == (12, 20)
    its[16] = tmcq("The ferry from Horseshoe Bay to Nanaimo leaves at <b>10:40</b>. The crossing takes <b>1 hour 40 minutes</b>. "
                   "What time does it arrive?", "12:20", ["11:20", "12:40", "12:10"],
                   "Add 1 hour: 10:40 → 11:40. Then add 40 minutes: 20 minutes takes you to 12:00, and 20 more makes "
                   "<b>12:20</b>. (Not 12:40: that adds 2 hours.)")
    # 17 Sea-to-Sky drive
    nm, pr = next(people)
    assert (9 * 60 + 35) - (7 * 60 + 50) == 105
    its[17] = how_long("%s’s family drives up the Sea-to-Sky Highway to Whistler. They leave at <b>7:50 a.m.</b> and arrive at "
                       "<b>9:35 a.m.</b> How long is the drive?" % nm, 7, 50, 9, 35,
                       ["185 minutes", "2 hours 45 minutes", "1 hour 15 minutes"],
                       "7:50 to 8:00 is 10 minutes. 8:00 to 9:00 is 1 hour. 9:00 to 9:35 is 35 minutes. "
                       "10 + 35 = 45, so the drive is <b>1 hour 45 minutes</b>. (Not 185 minutes: 935 − 750 = 185 treats "
                       "an hour as 100 minutes.)")
    # 18 compare durations
    a, b = next(people), next(people)
    its[18] = mcq("%s’s swimming lesson lasts <b>1 hour 15 minutes</b>. %s’s lesson lasts <b>80 minutes</b>. "
                  "Whose lesson is longer, and by how much?" % (a[0], b[0]), "%s’s, by 5 minutes" % b[0],
                  ["%s’s, by 35 minutes" % a[0], "%s’s, by 5 minutes" % a[0], "%s’s, by 65 minutes" % b[0]],
                  "1 hour 15 minutes = 60 + 15 = 75 minutes. 80 − 75 = 5. So <b>%s’s</b> lesson is longer, by "
                  "<b>5 minutes</b>. (Not %s’s by 35: that counts an hour as 100 minutes.)" % (b[0], a[0]))
    # 19 Terry Fox Run
    nm, pr = next(people)
    assert (11 * 60 + 12) - (10 * 60 + 30) == 42
    its[19] = how_long("The school Terry Fox Run starts at <b>10:30 a.m.</b> %s finishes at <b>11:12 a.m.</b> "
                       "How long does %s take?" % (nm, pr), 10, 30, 11, 12,
                       ["82 minutes", "18 minutes", "1 hour 42 minutes"],
                       "10:30 to 11:00 is 30 minutes. 11:00 to 11:12 is 12 minutes. 30 + 12 = <b>42 minutes</b>. "
                       "(Not 82: 1112 − 1030 = 82 treats an hour as 100 minutes.)")
    # 20 multi-step, answer in 12-hour time
    assert add(*add(13, 0, 95), 30) == (15, 5)
    nm, pr = next(people)
    its[20] = tmcq("%s’s family takes the <b>13:00</b> ferry from Tsawwassen. The crossing takes <b>1 hour 35 minutes</b>. "
                   "Then they drive <b>30 minutes</b> to Victoria. What time do they get to Victoria in 12-hour time?" % nm,
                   "3:05 p.m.", ["5:05 p.m.", "2:35 p.m.", "3:05 a.m."],
                   "13:00 + 1 hour 35 minutes = 14:35. 14:35 + 30 minutes = 15:05. 15 − 12 = 3, so it is <b>3:05 p.m.</b> "
                   "(Not 5:05 p.m.: 15:00 is 3 p.m., not 5 p.m.)")
    out = [its[i] for i in range(1, 21)]
    return {"title": "Elapsed time and schedules", "items": out}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Reading an analog clock to the minute</h2>"
        "<p>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "Each number is <b>5 minutes</b> for the long hand, and each small mark is 1 minute. "
        "Count by 5s to the last number, then count on by 1s.</p>"
        "<figure class='sn-fig'>" + clock_svg(4, 38, size=230) +
        "<figcaption>The long hand is 3 small marks past the 7: 35, 36, 37, 38 minutes. The short hand is between 4 and 5. "
        "It has not reached 5 yet, so the hour is 4. It is <b>4:38</b>, or 22 minutes to 5.</figcaption></figure>"
        "<h2>a.m. and p.m.</h2>"
        "<p>A day has 24 hours, but a clock face shows only 12. In 12-hour time we write <b>a.m.</b> for times from midnight "
        "to noon (night and morning) and <b>p.m.</b> for times from noon to midnight (afternoon and evening).</p>"
        + ex("a.m. or p.m.?", "Simran eats dinner at 22 minutes to 6 in the evening. Write the time.",
             "22 minutes to 6 is 38 minutes past 5. It is the evening, so it is p.m.", "5:38 p.m.") +
        "<h2>24-hour time</h2>"
        "<p>The 24-hour clock counts the hours from 00 to 23, so it needs no a.m. or p.m. It always has <b>4 digits</b>: "
        "07:30, 15:45. Ferry and transit schedules often use it.</p>"
        "<figure class='sn-fig'>" + clock_svg(15, 45, size=230, ring24=True) +
        "<figcaption>The green numbers around the clock show the hours after noon. The short hand is between 3 and 4 (15 and 16), "
        "so in the afternoon this clock shows <b>15:45</b>, which is 3:45 p.m.</figcaption></figure>"
        + table(["12-hour", "24-hour", "Rule"], [
            ["7:30 a.m.", "07:30", "a.m.: keep the hour, write 4 digits"],
            ["12:15 p.m.", "12:15", "just after noon: keep 12"],
            ["3:45 p.m.", "15:45", "p.m.: add 12 (3 + 12 = 15)"],
            ["9:10 p.m.", "21:10", "p.m.: add 12 (9 + 12 = 21)"],
            ["12:30 a.m.", "00:30", "just after midnight: 00"],
        ]) +
        "<p>To go back to 12-hour time, take away 12 from the hours 13 to 23: 18:05 is 18 − 12 = 6, so 6:05 p.m.</p>"
        + ex("24-hour to 12-hour", "Write 15:00 as a 12-hour time.", "15 − 12 = 3. The hour is after 12, so it is p.m.",
             "3:00 p.m.") +
        "<h2>Elapsed time: how long?</h2>"
        "<p>An hour has <b>60 minutes</b>, not 100, so do not subtract times like ordinary numbers. "
        "Jump to the next o’clock first, then on to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(15, 52, 16, 9, t24) +
        "<figcaption>A SkyTrain ride from 15:52 to 16:09: 8 minutes to 16:00, then 9 more minutes. "
        "8 + 9 = 17 minutes.</figcaption></figure>"
        + ex("Read a ferry schedule", "A ferry leaves Tsawwassen at 13:00 and arrives at Swartz Bay at 14:35. How long is the crossing?",
             "13:00 to 14:00 is 1 hour. 14:00 to 14:35 is 35 minutes.", "1 hour 35 minutes")
        + ex("Find the end time", "Hockey practice starts at 17:45 and lasts 1 hour 20 minutes. When does it end?",
             "17:45 + 1 hour = 18:45. 18:45 + 15 minutes = 19:00, then 5 more minutes.", "19:05") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["15:00 read as 5:00 p.m.", "Take away 12, do not just drop the 1. 15 − 12 = 3, so 3:00 p.m."],
            ["3:45 p.m. written as 13:45 or 03:45", "p.m.: add 12 to the hour. 3 + 12 = 15, so 15:45"],
            ["12:30 a.m. written as 12:30", "Just after midnight is 00 in 24-hour time: 00:30"],
            ["Swapping the hands: reading 4:38 as 7:20", "The short hand is the hour. The long hand is the minutes"],
            ["Short hand just before 5 read as 5:38", "The short hand has not reached 5 yet, so the hour is still 4: 4:38"],
            ["15:52 to 16:09 worked out as 1609 − 1552 = 57 minutes", "An hour has 60 minutes, not 100. Count on: 8 + 9 = 17 minutes"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about time in BC?",
     "a": "In the BC Grade 4 math curriculum, students learn how to tell time with analog and digital clocks, using both 12-hour and 24-hour clocks. Using a.m. and p.m. and working out how long events last are a natural part of this."},
    {"q": "How do you change 24-hour time to 12-hour time?",
     "a": "For hours from 13 to 23, take away 12 and write p.m. (15:45 is 3:45 p.m.). For hours from 01 to 11, keep the hour and write a.m. (08:15 is 8:15 a.m.). 12:00 is noon and 00:00 is midnight."},
    {"q": "Is 00:30 in the morning or at night?",
     "a": "00:30 is 12:30 a.m., which is 30 minutes after midnight, in the middle of the night. 12:30 in the afternoon is written 12:30 in 24-hour time."},
    {"q": "Is telling time on the Grade 4 FSA?",
     "a": "The Foundation Skills Assessment (FSA) that BC students write in Grade 4 checks numeracy skills from the BC curriculum, and it does not list every topic in advance. Reading clocks, 24-hour time and schedules is good all-round numeracy practice."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5). Picture items (A to D) keep their order and position."""
    for s in sets:
        targets = [p for p in range(4) for _ in range(5)]
        for it in s["items"]:
            if it.get("fixed"):
                targets.remove(it["a"])
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
    rnd = random.Random(34810)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_read(rnd), set_match(rnd), set_ampm(rnd, people), set_convert(rnd), set_elapsed(rnd, people)]
    balance(sets, rnd)
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = (it["q"], tuple(sorted(it["c"])))
            assert k not in allq, it["q"]
            allq.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "12-and-24-hour-time", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "12- and 24-Hour Time: Analog Clocks, a.m. and p.m., and Schedules",
        "seo_title": "Grade 4 Math: 12- and 24-Hour Time Worksheets (Free, BC Curriculum, Answer Key)",
        "short_title": "12- and 24-hour time",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 4: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "How to tell time with analog and digital clocks, using 12- and 24-hour clocks",
        "meta_desc": "Free Grade 4 math worksheets on telling time for the BC curriculum: read analog clocks to the minute, match analog and digital clocks, use a.m. and p.m., convert between 12-hour and 24-hour time, and work out elapsed time with ferry and SkyTrain schedules. 100 questions with an answer key, good numeracy practice for the FSA.",
        "key_big": "p.m.: add 12 to the hour. 3:45 p.m. = 15:45.",
        "key_sub": "To go back, take away 12: 15:00 is 3:00 p.m., not 5:00 p.m. Just after midnight is 00 (12:30 a.m. = 00:30). An hour has 60 minutes, not 100, so count on to the next o’clock when you work out how long.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "time line")
    mark_large(u, "four analog clocks")
    mark_large(u, "ferry timetable")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
