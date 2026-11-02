# -*- coding: utf-8 -*-
"""
CA Grade 3 Math: Telling Time (Ontario Mathematics Curriculum 2020, Grade 3: E2.6)
  python3 tools/gen_ca_math_g3_time.py
Every analog clock and stopwatch is drawn from the time itself (the hour hand moves between the numbers).
Every answer is worked out in code. Wrong answers come from real student mistakes:
hands swapped, hour hand just before a number read as that number, the number the minute hand points to read
as minutes, a.m. and p.m. swapped, an hour (or a minute) counted as 100, counting the numbers instead of the jumps.
Canadian English; times written 3:45 p.m. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Liam", "he"), ("Olivia", "she"), ("Noah", "he"), ("Emma", "she"), ("Aiden", "he"), ("Maya", "she"),
          ("Lucas", "he"), ("Zoe", "she"), ("Owen", "he"), ("Amira", "she"), ("Arjun", "he"), ("Mei", "she"),
          ("Ethan", "he"), ("Chloe", "she"), ("Jayden", "he"), ("Priya", "she"), ("Benjamin", "he"), ("Leah", "she"),
          ("Mateo", "he"), ("Hana", "she"), ("Nathan", "he"), ("Ava", "she"), ("Kai", "he"), ("Sofia", "she")]


# ------------------------------------------------------------ time formats
def h12(h24):
    return (h24 - 1) % 12 + 1


def tm12(h24, m):
    """12-hour digital: 3:45 p.m."""
    h24 %= 24
    if h24 == 12 and m == 0:
        return "12:00 noon"
    return "%d:%02d %s" % (h12(h24), m, "a.m." if h24 < 12 else "p.m.")


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


def secs(n):
    assert n > 0
    return "%d second%s" % (n, "" if n == 1 else "s")


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
    for n, unit in re.findall(r"(\d+) (hour|minute|second)", s):
        v += int(n) * {"hour": 3600, "minute": 60, "second": 1}[unit]
    return v


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
    return {"q": tidy(q), "c": [correct] + pick, "a": 0, "e": tidy(e)}


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


def dial_numbers(cx, cy, R, k, labels):
    fs = max(19 * k, 15)
    rn = R - 29 * k
    s = ["<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
         "paint-order='stroke'>" % (fs, LINE, 3.5 * k)]
    for i, lab in enumerate(labels):
        a = math.radians((i + 1) * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, lab))
    s.append("</g>")
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
    s += dial_numbers(cx, cy, R, k, [str(n) for n in range(1, 13)])
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200):
    return svg_wrap(size, size, clock_body(h, m, size), "analog clock")


def labelled_clocks_svg(times, labels, size=170, label="analog clocks"):
    """Clocks in one row with a label above each (one SVG per question)."""
    gap, top = 14, 30
    n = len(times)
    W = n * size + (n - 1) * gap
    s = []
    for i, (h, m) in enumerate(times):
        x = i * (size + gap)
        s.append("<text x='%.1f' y='22' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + size / 2.0, GREEN, labels[i]))
        s.append(clock_body(h, m, size, x, top))
    return svg_wrap(W, size + top, "".join(s), label)


def four_clocks_svg(times):
    return labelled_clocks_svg(times, "ABCD", label="four analog clocks")


def start_end_svg(h1, m1, h2, m2):
    return labelled_clocks_svg([(h1, m1), (h2, m2)], ["Start", "End"], size=180, label="start and end clocks")


def digital_svg(text):
    W, H = 200, 84
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='#fff' stroke='%s' stroke-width='4'/>" % (W - 6, H - 6, GREEN),
         "<rect x='16' y='14' width='%d' height='%d' rx='6' fill='#eef5f0'/>" % (W - 32, H - 28),
         "<text x='%d' y='%d' font-size='40' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Consolas, Menlo, monospace'>%s</text>" % (W / 2, H / 2 + 14, LINE, text)]
    return svg_wrap(W, H, "".join(s), "digital clock")


def timer_svg(mm, ss):
    """Digital timer: minutes : seconds, labelled underneath."""
    W, H = 200, 108
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='#fff' stroke='%s' stroke-width='4'/>" % (W - 6, H - 6, GREEN),
         "<rect x='16' y='12' width='%d' height='58' rx='6' fill='#eef5f0'/>" % (W - 32),
         "<text x='%d' y='56' font-size='40' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Consolas, Menlo, monospace'>%d:%02d</text>" % (W / 2, LINE, mm, ss),
         "<text x='68' y='92' font-size='15' fill='%s' text-anchor='middle'>min</text>" % LINE,
         "<text x='134' y='92' font-size='15' fill='%s' text-anchor='middle'>sec</text>" % LINE]
    return svg_wrap(W, H, "".join(s), "timer")


def stopwatch_svg(sec, size=200):
    """Stopwatch dial: 60 seconds once around, numbers 5 to 60, one red hand."""
    assert 0 < sec < 60
    top = 22
    R = size / 2.0 - 6
    cx, cy = size / 2.0, top + size / 2.0
    k = R / 94.0
    s = ["<rect x='%.1f' y='2' width='24' height='%d' rx='4' fill='%s'/>" % (cx - 12, top + 4, GREEN)]
    s += face(cx, cy, R, k)
    a = math.radians(sec * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.84 * math.cos(a), cy + R * 0.84 * math.sin(a), RED, 4.5 * k))
    s += dial_numbers(cx, cy, R, k, [str(5 * n) for n in range(1, 13)])
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return svg_wrap(size, size + top, "".join(s), "stopwatch")


def timeline_svg(h1, m1, h2, m2, W=420):
    """Start -> next o'clock -> end, the jumps labelled."""
    t1, t2 = h1 * 60 + m1, h2 * 60 + m2
    mid = (h1 + 1) * 60 if m1 else None
    L, R, Y = 50, W - 50, 70

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
    """hands swapped: short hand read as the minutes, long hand read as the hour (only for m in 5s)"""
    hh = m // 5 or 12
    return dig(hh, (h % 12) * 5)


def pick_hour(rnd, m, used):
    hrs = list(range(1, 13))
    rnd.shuffle(hrs)
    for h in hrs:
        if (h, m) in used or hands_gap(h, m) < 15:
            continue
        used.add((h, m))
        return h
    raise AssertionError(m)


# ============================================================ set 1: to the 5 minutes
def set_five(rnd):
    its = []
    used = set()
    plan = [(0, "d"), (0, "d"), (30, "d"), (30, "w"), (15, "d"), (15, "w"), (45, "d"), (45, "w"), (5, "d"), (10, "d"),
            (20, "d"), (25, "d"), (35, "d"), (40, "d"), (50, "d"), (55, "d"), (20, "w"), (40, "w"), (35, "d"), (50, "w")]
    for m, mode in plan:
        h = pick_hour(rnd, m, used)
        n = m // 5
        if mode == "d":
            right = dig(h, m)
            sw = swapped(h, m)
            if m == 0:
                c = [sw, "%d:12" % h12(h), dig(h + 1, 0), dig(h - 1, 0)]
                note = "(Not %s: that swaps the hands. Not %d:12: when the long hand points to 12, it is 0 minutes.)" % (sw, h12(h))
            elif m >= 30:
                c = [dig(h + 1, m), sw, dig(h, n), dig(h, 60 - m)]
                note = ("(Not %s: the hour hand is <b>before</b> %d, so it is not %d o’clock yet. Not %s: that swaps the hands.)"
                        % (dig(h + 1, m), h12(h + 1), h12(h + 1), sw))
            else:
                c = [dig(h, n), sw, dig(h + 1, m), dig(h, 60 - m)]
                note = "(Not %s: each number is 5 minutes, so %d means %d × 5 = %d. Not %s: that swaps the hands.)" % (
                    dig(h, n), n, n, m, sw)
            e = "%s So the time is <b>%s</b>. %s" % (hand_text(h, m), right, note)
            q = fig(clock_svg(h, m)) + "What time does the clock show?"
        else:
            right = words(h, m)
            if m == 30:
                c = [words(h + 1, 30), words(h, 15), words(h - 1, 30), "6 o’clock" if h != 6 else "12 o’clock"]
                e = ("%s Half past means 30 minutes past. The hour hand has not reached %d yet, so it is <b>%s</b>, not half past %d."
                     % (hand_text(h, m), h12(h + 1), right, h12(h + 1)))
            elif m == 15:
                c = [words(h, 45), words(h, 3), words(h - 1, 15), words(h + 1, 45)]
                e = ("%s 15 minutes is a quarter of an hour. The long hand is on the right side, so we say <b>past</b>. "
                     "It is <b>%s</b>." % (hand_text(h, m), right))
            elif m == 45:
                c = [words(h, 15), words(h + 1, 15), words(h - 1, 45), words(h, 9)]
                e = ("%s 45 minutes past %d is 15 minutes before %d o’clock. The long hand is on the left side, so we say "
                     "<b>to</b> the next hour: <b>%s</b>." % (hand_text(h, m), h12(h), h12(h + 1), right))
            elif m < 30:
                c = [words(h + 1, m), words(h, 60 - m), words(h, n), words(h - 1, 60 - m)]
                e = ("%s The long hand is on the right side, so we say <b>past %d</b>. It is <b>%s</b>."
                     % (hand_text(h, m), h12(h), right))
            else:
                c = [words(h - 1, m), "%d past %d" % (60 - m, h12(h)), words(h, n), words(h + 1, 60 - m)]
                e = ("%s That is %d minutes before %d o’clock (60 − %d = %d). The long hand is on the left side, so we say "
                     "<b>to %d</b>. It is <b>%s</b>." % (hand_text(h, m), 60 - m, h12(h + 1), m, 60 - m, h12(h + 1), right))
            q = fig(clock_svg(h, m)) + "What time does the clock show? Choose the words."
        its.append(mcq(q, right, c, e))
    return {"title": "Reading analog clocks to the 5 minutes", "items": its}


# ============================================================ set 2: to the minute; analog and digital
def set_minute(rnd):
    its = []
    used = []

    def pick(lo, hi):
        while True:
            h = rnd.randint(1, 12)
            m = rnd.randint(lo, hi)
            if m % 5 and (h, m) not in used and hands_gap(h, m) >= 18 and h not in [x[0] for x in used][-2:]:
                used.append((h, m))
                return h, m

    # clock -> digital
    for lo, hi in [(1, 14), (16, 29), (31, 44), (46, 59), (16, 29), (31, 44), (1, 14), (46, 59), (31, 44), (46, 59),
                   (6, 24), (36, 54)]:
        h, m = pick(lo, hi)
        n = m // 5
        right = dig(h, m)
        c = []
        if m >= 30:
            c.append(dig(h + 1, m))                       # hour hand before the number read as that number
        if n:
            c.append(dig(h, n * 5))                       # stopped at the last number, small marks not counted
            c.append(dig(h, n))                           # number the minute hand points near read as minutes
        c += [dig(h, 60 - m), dig(h, m + 1 if m % 5 != 4 else m - 1), dig(h + 1, m), dig(h - 1, m)]
        e = "%s So the digital time is <b>%s</b>." % (hand_text(h, m), right)
        if m >= 30:
            e += " (Not %s: the hour hand has not reached %d yet.)" % (dig(h + 1, m), h12(h + 1))
        elif n:
            e += " (Not %s: count the small marks after the %d too.)" % (dig(h, n * 5), n)
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show? Choose the digital time.", right, c, e))
    # which analog clock matches the digital time (A to D)
    pos = [0, 1, 2, 3]
    rnd.shuffle(pos)
    for (h, m), p in zip([(5, 38), (8, 13), (6, 52), (11, 27)], pos):
        others = [(h + 1, m), (h, 60 - m), (h, m // 5)]
        times = list(others)
        times.insert(p, (h, m))
        assert len(set(times)) == 4
        L = "ABCD"
        wrong = "; ".join("clock %s shows %s" % (L[times.index(t)], dig(*t)) for t in others)
        e = ("At %s the long hand is %d small mark%s past the %d (count by 5s to %d, then by 1s to %d), and the short hand "
             "is between %d and %d. That is clock <b>%s</b>. (%s.)"
             % (dig(h, m), m % 5, "" if m % 5 == 1 else "s", m // 5, m // 5 * 5, m, h12(h), h12(h + 1), L[p],
                wrong[0].upper() + wrong[1:]))
        its.append({"q": fig(four_clocks_svg(times)) + "Which analog clock shows <b>%s</b>?" % dig(h, m),
                    "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True})
    # digital -> words, words -> digital
    for h, m in [(7, 48), (2, 14)]:
        right = words(h, m)
        if m > 30:
            c = [words(h - 1, m), "%s to %d" % (mins(m), h12(h + 1)), "%s past %d" % (mins(60 - m), h12(h)),
                 "%s to %d" % (mins(60 - m), h12(h))]
            e = ("%s is %d minutes past %d. That is after half past, so say <b>to</b> the next hour. "
                 "60 − %d = %d minutes to %d: <b>%s</b>." % (dig(h, m), m, h12(h), m, 60 - m, h12(h + 1), right))
        else:
            c = [words(h + 1, m), "%s to %d" % (mins(m), h12(h + 1)), "%s to %d" % (mins(m), h12(h)), words(h, m + 1)]
            e = "%s is %d minutes after %d o’clock. It is before half past, so say <b>past</b>: <b>%s</b>." % (dig(h, m), m, h12(h), right)
        its.append(mcq(fig(digital_svg(dig(h, m))) + "How do we say this digital time in words?", right, c, e))
    for h, m in [(5, 37), (10, 6)]:
        w = words(h, m)
        right = dig(h, m)
        if m > 30:
            c = [dig(h + 1, 60 - m), dig(h + 1, m), dig(h, 60 - m), dig(h - 1, m)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d minutes past %d: <b>%s</b>. "
                 "(Not %s: that would be after %d o’clock.)" % (w, 60 - m, h12(h + 1), 60 - m, m, m, h12(h), right,
                                                                 dig(h + 1, m), h12(h + 1)))
        else:
            c = [dig(h, 60 - m), dig(h - 1, 60 - m), dig(h + 1, m), dig(h, m + 10)]
            e = "“%s” means %d minutes <b>after</b> %d o’clock: <b>%s</b>." % (w, m, h12(h), right)
        its.append(mcq("Write <b>%s</b> as a digital time." % w, right, c, e))
    assert len(its) == 20
    order = [0, 1, 6, 12, 2, 3, 16, 13, 4, 5, 18, 7, 14, 8, 17, 9, 15, 10, 19, 11]
    assert sorted(order) == list(range(20))
    return {"title": "To the minute: matching analog and digital clocks", "items": [its[i] for i in order]}


# ============================================================ set 3: a.m. and p.m.
CONTEXTS = [
    ("{n} wakes up in the morning.", 7, 2, 28),
    ("{n} walks to school in the morning.", 8, 6, 24),
    ("{n} eats lunch at school.", 12, 6, 24),
    ("{n} goes to skating practice after school.", 16, 6, 28),
    ("{n} eats dinner in the evening.", 18, 2, 26),
    ("{n} goes to bed in the evening.", 20, 6, 28),
]


def set_ampm(rnd, people):
    its = []
    its.append(mcq("Which times are <b>a.m.</b> times?", "from midnight to noon",
                   ["from noon to midnight", "only times at night", "only times after school"],
                   "<b>a.m.</b> times go from midnight to noon (night and morning). <b>p.m.</b> times go from noon to "
                   "midnight (afternoon and evening)."))
    its.append(mcq("What does <b>noon</b> mean?", "12 o’clock in the middle of the day",
                   ["12 o’clock at night", "1 o’clock in the afternoon", "the end of the school day"],
                   "<b>Noon</b> is 12 o’clock in the middle of the day, when the morning ends. "
                   "12 o’clock at night is <b>midnight</b>."))
    its.append(mcq("Which time is in the <b>afternoon</b>?", "2:30 p.m.", ["2:30 a.m.", "11:30 a.m.", "9:15 a.m."],
                   "The afternoon is after noon, so it is a <b>p.m.</b> time. 2:30 a.m. is in the middle of the night. "
                   "So the answer is <b>2:30 p.m.</b>"))
    its.append(mcq("Which is a sensible time for school to start?", "8:45 a.m.", ["8:45 p.m.", "3:45 a.m.", "11:45 p.m."],
                   "School starts in the morning, so it is an <b>a.m.</b> time. 3:45 a.m. is the middle of the night. "
                   "So the answer is <b>8:45 a.m.</b>"))
    nm, pr = next(people)
    its.append(mcq("%s eats breakfast at 7:15 in the morning. Is that a.m. or p.m.?" % nm,
                   "a.m., because it is before noon",
                   ["p.m., because it is before noon", "p.m., because it is after noon", "a.m., because it is after noon"],
                   "Morning times are before noon. Times before noon are <b>a.m.</b> times. So breakfast is at 7:15 a.m."))
    its.append(mcq("Which is earlier in the same day: <b>11:50 a.m.</b> or <b>1:10 p.m.</b>?", "11:50 a.m.",
                   ["1:10 p.m.", "They are the same time.", "You cannot tell."],
                   "a.m. times come before noon and p.m. times come after noon. So <b>11:50 a.m.</b> is earlier, "
                   "even though 11 is bigger than 1."))
    # clocks with a time of day -> 12-hour digital with a.m. / p.m.
    ctx = CONTEXTS[:]
    rnd.shuffle(ctx)
    for sent, H, lo, hi in ctx:
        ms = [x for x in range(lo, hi + 1) if x % 5 and hands_gap(H, x) >= 15]
        m = rnd.choice(ms)
        n = m // 5
        nm, pr = next(people)
        right = tm12(H, m)
        c = [tm12(H + 12, m)]                             # a.m. and p.m. swapped
        if n:
            c.append(tm12(H, n))                          # number near the minute hand read as minutes
        c += [tm12(H + 1, m), tm12(H, 60 - m), tm12(H - 1, m)]
        why = "It is in the morning, so it is <b>a.m.</b>" if H < 12 else "It is after noon, so it is <b>p.m.</b>"
        e = "%s %s So the time is <b>%s</b>" % (hand_text(H, m), why, right)
        if c[0] != right:
            e += " (Not %s: that is %s.)" % (c[0], "in the middle of the night" if (H + 12) % 24 < 6 or (H + 12) % 24 == 0
                                              else ("in the afternoon or evening" if (H + 12) % 24 >= 12 else "in the morning"))
        q = fig(clock_svg(H, m)) + sent.format(n=nm) + " What is the time?"
        its.append(mcq(q, right, c, e))
    # words -> digital with a.m. / p.m.
    for H, m, part in [(7, 45, "in the morning"), (15, 35, "in the afternoon"), (19, 20, "in the evening"),
                       (10, 50, "in the morning")]:
        w = words(H, m)
        right = tm12(H, m)
        ap = "a.m." if H < 12 else "p.m."
        if m > 30:
            c = [tm12(H + 1, m), tm12(H + 1, 60 - m), tm12(H, 60 - m), tm12(H + 12, m)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d minutes past %d: %s. "
                 "It is %s, so it is %s: <b>%s</b>"
                 % (w, 60 - m, h12(H + 1), 60 - m, m, m, h12(H), dig(H, m), part, ap, right))
        else:
            c = [tm12(H + 12, m), tm12(H - 1, 60 - m), tm12(H, m // 5), tm12(H + 1, m)]
            e = ("“%s” means %d minutes <b>after</b> %d o’clock: %s. It is %s, so it is %s: <b>%s</b>"
                 % (w, m, h12(H), dig(H, m), part, ap, right))
        its.append(mcq("Write <b>%s %s</b> as a digital time." % (w, part), right, c, e))
    # hours across noon
    its.append(mcq("How many hours is it from <b>9:00 a.m.</b> to <b>noon</b>?", "3 hours",
                   ["4 hours", "2 hours", "9 hours"],
                   "Count the jumps, not the numbers: 9:00 → 10:00 → 11:00 → 12:00 noon. That is <b>3 hours</b>. "
                   "(4 counts the numbers 9, 10, 11 and 12.)"))
    its.append(mcq("How many hours is it from <b>11:00 a.m.</b> to <b>2:00 p.m.</b>?", "3 hours",
                   ["9 hours", "2 hours", "13 hours"],
                   "11:00 a.m. → 12:00 noon is 1 hour. 12:00 noon → 2:00 p.m. is 2 hours. 1 + 2 = <b>3 hours</b>. "
                   "(Not 9 hours: 11 − 2 = 9 does not work across noon.)"))
    assert len(its) == 18
    its.append(mcq("Put these times in order from <b>earliest</b> to <b>latest</b> in one day: "
                   "3:00 p.m., 7:00 a.m., 9:30 p.m., 11:00 a.m.",
                   "7:00 a.m., 11:00 a.m., 3:00 p.m., 9:30 p.m.",
                   ["3:00 p.m., 7:00 a.m., 9:30 p.m., 11:00 a.m.", "11:00 a.m., 9:30 p.m., 7:00 a.m., 3:00 p.m.",
                    "7:00 a.m., 3:00 p.m., 9:30 p.m., 11:00 a.m."],
                   "All a.m. times come first, then the p.m. times. a.m.: 7:00, then 11:00. p.m.: 3:00, then 9:30. "
                   "So the order is <b>7:00 a.m., 11:00 a.m., 3:00 p.m., 9:30 p.m.</b>"))
    its.append(mcq("A digital clock shows <b>4:37 p.m.</b> How many minutes is it until 5:00 p.m.?", "23 minutes",
                   ["37 minutes", "63 minutes", "13 minutes"],
                   "An hour has 60 minutes. It is 37 minutes past 4. 60 − 37 = <b>23 minutes</b> until 5:00 p.m. "
                   "(Not 63: an hour is 60 minutes, not 100.)"))
    order = [0, 1, 2, 3, 4, 5, 6, 12, 7, 13, 8, 14, 9, 15, 10, 11, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "a.m. and p.m.", "items": [its[i] for i in order]}


# ============================================================ set 4: elapsed time
def how_long(text, h1, m1, h2, m2, figure=None):
    d = (h2 * 60 + m2) - (h1 * 60 + m1)
    assert d > 0
    q = {"line": lambda: fig(timeline_svg(h1, m1, h2, m2)), "clocks": lambda: fig(start_end_svg(h1, m1, h2, m2)),
         None: lambda: ""}[figure]() + text
    if h1 == h2:
        c = [mins(m2), mins(d + 10), mins(d - 5) if d > 5 else None, mins(d + 5), mins(m1 + m2)]
        e = "Both times are in the same hour. %d − %d = <b>%s</b>." % (m2, m1, mins(d))
    elif m1 == m2:
        hrs = d // 60
        steps = " → ".join(tm12(h1 + i, m1) for i in range(hrs + 1))
        c = [dur(d + 60), "%d minutes" % (hrs * 100), dur(d - 60) if d > 60 else "%d minutes" % 10,
             "%d hours" % abs(h12(h2) - h12(h1)) if abs(h12(h2) - h12(h1)) not in (0, 1, hrs) else None, dur(d + 120)]
        e = ("The minutes are the same, so count the hours. Count the jumps, not the numbers: %s. That is <b>%s</b>. "
             "(1 hour is 60 minutes, not 100.)" % (steps, dur(d)))
    else:
        naive = (h12(h2) * 100 + m2) - (h12(h1) * 100 + m1)
        c = ["%d minutes" % naive if 0 < naive < 100 and naive != d else None, mins(abs(m2 - m1)) if m2 != m1 else None,
             dur((h2 - h1) * 60) if m1 and m2 == 0 else None,
             dur(d + 60) if d < 60 else dur(d - 60), dur(d + 10), dur(d - 5)]
        if m1 == 0:
            e = ("From %s to %s is %s. Then %s to %s is %s. So it is <b>%s</b>."
                 % (tm12(h1, 0), tm12(h2, 0), dur((h2 - h1) * 60), tm12(h2, 0), tm12(h2, m2), mins(m2), dur(d)))
        else:
            rest = d - (60 - m1)
            e = ("Count on to the next o’clock first: %s to %s is %s. Then %s to %s is %s. %d + %d = %s"
                 % (tm12(h1, m1), tm12(h1 + 1, 0), mins(60 - m1), tm12(h1 + 1, 0), tm12(h2, m2),
                    dur(rest), 60 - m1, rest, "<b>%s</b>." % mins(d) if d < 60 else "%d minutes = <b>%s</b>." % (d, dur(d))))
            if naive > 0 and naive < 100 and naive != d:
                e += " (Not %d minutes: an hour has 60 minutes, not 100, so do not just subtract the numbers.)" % naive
    return mcq(q, dur(d), c, e, key=dur_value)


def set_elapsed(rnd, people):
    its = []
    its.append(how_long("Recess starts at <b>10:15 a.m.</b> and ends at <b>10:30 a.m.</b> How long is recess?",
                        10, 15, 10, 30, "clocks"))
    its.append(how_long("Gym class starts at <b>1:05 p.m.</b> and ends at <b>1:45 p.m.</b> How long is gym class?", 13, 5, 13, 45))
    nm, pr = next(people)
    its.append(how_long("%s starts reading at <b>7:10 p.m.</b> and stops at <b>7:35 p.m.</b> How long does %s read?"
                        % (nm, pr), 19, 10, 19, 35, "clocks"))
    nm, pr = next(people)
    its.append(how_long("%s gets on the school bus at <b>8:12 a.m.</b> %s gets to school at <b>8:31 a.m.</b> "
                        "How long is the bus ride?" % (nm, pr.capitalize()), 8, 12, 8, 31))
    its.append(how_long("Math class is from <b>9:00 a.m.</b> to <b>10:00 a.m.</b> How long is math class?", 9, 0, 10, 0, "clocks"))
    its.append(how_long("The bus for the field trip leaves at <b>9:00 a.m.</b> It gets to the museum at <b>11:00 a.m.</b> "
                        "How long is the bus ride?", 9, 0, 11, 0))
    its.append(how_long("Lunch starts at <b>11:40 a.m.</b> and ends at <b>12:20 p.m.</b> How long is lunch?",
                        11, 40, 12, 20, "line"))
    nm, pr = next(people)
    its.append(how_long("%s skates at the rink from <b>3:50 p.m.</b> to <b>4:15 p.m.</b> How long does %s skate?"
                        % (nm, pr), 15, 50, 16, 15, "line"))
    nm, pr = next(people)
    its.append(how_long("%s’s swimming lesson is from <b>4:45 p.m.</b> to <b>5:20 p.m.</b> How long is it?" % nm,
                        16, 45, 17, 20))
    its.append(how_long("A hockey game starts at <b>6:30 p.m.</b> and ends at <b>8:00 p.m.</b> How long is the game?",
                        18, 30, 20, 0, "line"))
    its.append(how_long("A movie starts at <b>7:00 p.m.</b> and ends at <b>8:45 p.m.</b> How long is the movie?", 19, 0, 20, 45))
    its.append(how_long("The maple syrup festival is open from <b>10:30 a.m.</b> to <b>1:30 p.m.</b> How long is it open?",
                        10, 30, 13, 30))
    # end and start times
    assert add(10, 15, 15) == (10, 30)
    its.append(mcq("Recess starts at <b>10:15 a.m.</b> It lasts <b>15 minutes</b>. What time does it end?", "10:30 a.m.",
                   ["10:30 p.m.", "11:15 a.m.", "10:25 a.m."],
                   "Count on 15 minutes from 10:15: 15 + 15 = 30. It is still the morning, so recess ends at <b>10:30 a.m.</b> "
                   "(11:15 a.m. would be 1 hour later.)"))
    assert add(13, 40, 50) == (14, 30)
    its.append(mcq("Art starts at <b>1:40 p.m.</b> It lasts <b>50 minutes</b>. What time does it end?", "2:30 p.m.",
                   ["2:40 p.m.", "2:30 a.m.", "2:10 p.m."],
                   "From 1:40 p.m., 20 minutes takes you to 2:00 p.m. 50 − 20 = 30 more minutes makes <b>2:30 p.m.</b> "
                   "(2:40 p.m. would be 1 hour later, not 50 minutes.)"))
    nm, pr = next(people)
    assert add(20, 30, -20) == (20, 10)
    its.append(mcq("%s goes to bed at <b>8:30 p.m.</b> %s reads for <b>20 minutes</b> before bed. What time does %s start reading?"
                   % (nm, pr.capitalize(), pr), "8:10 p.m.", ["8:50 p.m.", "8:10 a.m.", "8:20 p.m."],
                   "Count <b>back</b> 20 minutes from 8:30: 30 − 20 = 10. Reading starts at <b>8:10 p.m.</b> "
                   "(8:50 p.m. is 20 minutes <b>after</b> bedtime.)"))
    nm, pr = next(people)
    assert add(18, 10, -25) == (17, 45)
    its.append(mcq("%s’s soccer game starts at <b>6:10 p.m.</b> %s leaves home <b>25 minutes</b> before the game. "
                   "What time does %s leave home?" % (nm, pr.capitalize(), pr), "5:45 p.m.",
                   ["6:35 p.m.", "5:35 p.m.", "5:45 a.m."],
                   "Count back 10 minutes to 6:00 p.m. 25 − 10 = 15, so count back 15 more minutes: <b>5:45 p.m.</b> "
                   "(6:35 p.m. is 25 minutes <b>after</b> 6:10.)"))
    assert add(9, 20, 85) == (10, 45)
    its.append(mcq("The bus for the field trip leaves at <b>9:20 a.m.</b> The ride takes <b>1 hour 25 minutes</b>. "
                   "What time does the bus arrive?", "10:45 a.m.", ["10:45 p.m.", "9:45 a.m.", "11:05 a.m."],
                   "Add 1 hour: 9:20 a.m. → 10:20 a.m. Then add 25 minutes: 20 + 25 = 45. The bus arrives at <b>10:45 a.m.</b>"))
    assert (15 * 60 + 15) - (8 * 60 + 45) == 390
    its.append(mcq("School starts at <b>8:45 a.m.</b> and ends at <b>3:15 p.m.</b> How long is the school day?",
                   "6 hours 30 minutes", ["5 hours 30 minutes", "7 hours 30 minutes", "7 hours"],
                   "8:45 a.m. to 2:45 p.m. is 6 hours. 2:45 p.m. to 3:15 p.m. is 30 minutes. So the school day is "
                   "<b>6 hours 30 minutes</b>. (Not 7 hours: 8:45 to 3:45 would be 7 hours, but school ends 30 minutes before 3:45.)", key=dur_value))
    a, b = next(people), next(people)
    its.append(mcq("%s’s movie is <b>1 hour 30 minutes</b> long. %s’s movie is <b>95 minutes</b> long. "
                   "Whose movie is longer, and by how much?" % (a[0], b[0]), "%s’s, by 5 minutes" % b[0],
                   ["%s’s, by 5 minutes" % a[0], "%s’s, by 35 minutes" % a[0], "%s’s, by 65 minutes" % b[0]],
                   "1 hour 30 minutes = 60 + 30 = 90 minutes. 95 − 90 = 5. So <b>%s’s</b> movie is longer, by <b>5 minutes</b>. "
                   "(Not %s’s by 35: that counts an hour as 100 minutes.)" % (b[0], a[0])))
    assert add(11, 30, 195) == (14, 45)
    its.append(mcq("On Thanksgiving, the turkey goes in the oven at <b>11:30 a.m.</b> It cooks for <b>3 hours 15 minutes</b>. "
                   "What time is it ready?", "2:45 p.m.", ["2:45 a.m.", "3:45 p.m.", "2:15 p.m."],
                   "Add 3 hours: 11:30 a.m. → 12:30 p.m. → 1:30 p.m. → 2:30 p.m. Then add 15 minutes: <b>2:45 p.m.</b> "
                   "It is after noon, so it is p.m."))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 12, 6, 7, 8, 14, 13, 9, 10, 11, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Elapsed time in minutes and hours", "items": [its[i] for i in order]}


# ============================================================ set 5: timers and seconds
def set_timers(rnd, people):
    its = []
    its.append(mcq("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "30"],
                   "There are <b>60 seconds</b> in 1 minute. (Not 100: time does not count in hundreds.)"))
    its.append(mcq(fig(stopwatch_svg(35)) + "The stopwatch hand goes once around in 60 seconds. How much time does it show?",
                   "35 seconds", ["7 seconds", "35 minutes", "40 seconds"],
                   "The numbers on a stopwatch count by 5s. The hand points to <b>35</b>, so it shows <b>35 seconds</b>. "
                   "(Not 7: 35 is the 7th number, but each number is 5 seconds.)"))
    its.append(mcq(fig(stopwatch_svg(47)) + "How much time does the stopwatch show?",
                   "47 seconds", ["45 seconds", "52 seconds", "47 minutes"],
                   "The hand is 2 small marks past the 45. Count by 5s to 45, then by 1s: 46, 47. It shows <b>47 seconds</b>. "
                   "(A stopwatch hand that goes once around in 60 seconds shows seconds, not minutes.)"))
    nm, pr = next(people)
    its.append(mcq("The class does a <b>60-second challenge</b>. %s does jumping jacks until the timer beeps. "
                   "How long is that?" % nm, "1 minute", ["6 minutes", "10 minutes", "1 hour"],
                   "60 seconds = <b>1 minute</b>. (60 minutes would be 1 hour.)", key=dur_value))
    its.append(mcq(fig(timer_svg(1, 20)) + "The timer shows minutes and seconds. How many seconds is that?",
                   "80 seconds", ["120 seconds", "20 seconds", "21 seconds"],
                   "1:20 means 1 minute 20 seconds. 1 minute = 60 seconds. 60 + 20 = <b>80 seconds</b>. "
                   "(Not 120: a minute is 60 seconds, not 100.)", key=dur_value))
    its.append(mcq("<b>2 minutes</b> = ? seconds", "120", ["200", "60", "20"],
                   "1 minute = 60 seconds. 2 minutes = 60 + 60 = <b>120 seconds</b>. (Not 200: a minute is not 100 seconds.)"))
    its.append(mcq("Which is the same as <b>90 seconds</b>?", "1 minute 30 seconds",
                   ["9 minutes", "90 minutes", "1 minute 10 seconds"],
                   "60 seconds make 1 minute. 90 − 60 = 30 seconds left. So 90 seconds = <b>1 minute 30 seconds</b>. "
                   "(1 minute 10 seconds would be 70 seconds.)", key=dur_value))
    its.append(mcq("Which unit would you use to time a <b>50 m race</b> in gym class?", "seconds",
                   ["hours", "days", "weeks"],
                   "A 50 m race is over very fast, in less than a minute. We time it in <b>seconds</b>."))
    its.append(mcq("About how long does it take to tie your shoes?", "30 seconds",
                   ["30 minutes", "30 hours", "3 days"],
                   "Tying shoes is quick. 30 minutes is much too long. It takes about <b>30 seconds</b>.", key=dur_value))
    its.append(mcq("Which is <b>longer</b>: 100 seconds or 2 minutes?", "2 minutes",
                   ["100 seconds", "They are the same.", "You cannot tell."],
                   "2 minutes = 60 + 60 = 120 seconds. 120 seconds is more than 100 seconds, so <b>2 minutes</b> is longer."))
    # word problems
    nm, pr = next(people)
    its.append(mcq("In the 60-second challenge, %s has used <b>45 seconds</b>. How many seconds are left?" % nm,
                   "15 seconds", ["55 seconds", "105 seconds", "45 seconds"],
                   "60 − 45 = <b>15 seconds</b>. (55 would be 100 − 45, but a minute has 60 seconds.)", key=dur_value))
    its.append(mcq(fig(timer_svg(1, 0)) + "A timer starts at 1:00 and counts down. What does it show after "
                   "<b>25 seconds</b>?", "0:35", ["0:75", "0:25", "1:25"],
                   "1:00 is 1 minute = 60 seconds. 60 − 25 = 35 seconds left, so it shows <b>0:35</b>. "
                   "(0:75 comes from 100 − 25, but there are only 60 seconds in a minute.)"))
    its.append(mcq("Popcorn cooks in the microwave for <b>2 minutes 30 seconds</b>. How many seconds is that?",
                   "150 seconds", ["230 seconds", "130 seconds", "250 seconds"],
                   "2 minutes = 120 seconds. 120 + 30 = <b>150 seconds</b>. (230 counts a minute as 100 seconds.)",
                   key=dur_value))
    nm, pr = next(people)
    its.append(mcq("%s skates 1 lap of the rink in <b>40 seconds</b>. How long do <b>3 laps</b> take?" % nm,
                   "2 minutes", ["1 minute 20 seconds", "43 seconds", "1 minute 40 seconds"],
                   "40 + 40 + 40 = 120 seconds. 120 seconds = 60 + 60 = <b>2 minutes</b>. "
                   "(1 minute 20 seconds counts a minute as 100 seconds.)", key=dur_value))
    a, b = next(people), next(people)
    assert 65 - 58 == 7
    its.append(mcq("At the Terry Fox Run, %s runs the first part in <b>58 seconds</b>. %s takes <b>1 minute 5 seconds</b>. "
                   "How much faster is %s?" % (a[0], b[0], a[0]), "7 seconds",
                   ["47 seconds", "53 seconds", "1 minute 7 seconds"],
                   "1 minute 5 seconds = 60 + 5 = 65 seconds. 65 − 58 = <b>7 seconds</b>. "
                   "(Not 47: a minute is 60 seconds, not 100.)", key=dur_value))
    a, b = next(people), next(people)
    its.append(mcq("%s holds a plank for <b>1 minute 20 seconds</b>. %s holds it for <b>55 seconds</b>. "
                   "How much longer is %s’s plank?" % (a[0], b[0], a[0]), "25 seconds",
                   ["65 seconds", "35 seconds", "1 minute 25 seconds"],
                   "1 minute 20 seconds = 60 + 20 = 80 seconds. 80 − 55 = <b>25 seconds</b>. "
                   "(65 comes from 120 − 55, which counts a minute as 100 seconds.)", key=dur_value))
    a, b = next(people), next(people)
    its.append(mcq("%s’s time in a ringette drill is <b>1 minute 15 seconds</b>. %s’s time is <b>70 seconds</b>. "
                   "Who is faster?" % (a[0], b[0]), "%s, by 5 seconds" % b[0],
                   ["%s, by 5 seconds" % a[0], "%s, by 45 seconds" % b[0], "%s, by 55 seconds" % a[0]],
                   "1 minute 15 seconds = 60 + 15 = 75 seconds. 70 is less than 75, so <b>%s</b> is faster, by "
                   "75 − 70 = <b>5 seconds</b>. (A faster time is a smaller number.)" % b[0]))
    its.append(mcq("On a snow day, hot chocolate heats in the microwave for <b>1 minute 30 seconds</b>. "
                   "<b>50 seconds</b> have passed. How much time is left?", "40 seconds",
                   ["80 seconds", "2 minutes 20 seconds", "30 seconds"],
                   "1 minute 30 seconds = 60 + 30 = 90 seconds. 90 − 50 = <b>40 seconds</b>. "
                   "(80 comes from 130 − 50, which counts a minute as 100 seconds.)", key=dur_value))
    its.append(mcq(fig(timer_svg(2, 45)) + "The oven timer shows how long until the cookies are done. "
                   "How many seconds is that?", "165 seconds", ["245 seconds", "105 seconds", "47 seconds"],
                   "2:45 means 2 minutes 45 seconds. 2 minutes = 120 seconds. 120 + 45 = <b>165 seconds</b>. "
                   "(245 counts a minute as 100 seconds.)", key=dur_value))
    assert add(14, 40, 12) == (14, 52)
    its.append(mcq("Mom sets a timer for <b>12 minutes</b> at <b>2:40 p.m.</b> to bake maple cookies. "
                   "When does the timer beep?", "2:52 p.m.", ["2:52 a.m.", "3:52 p.m.", "2:28 p.m."],
                   "Count on 12 minutes from 2:40: 40 + 12 = 52. It is the afternoon, so the timer beeps at <b>2:52 p.m.</b>"))
    assert len(its) == 20
    order = [0, 1, 3, 5, 2, 4, 7, 6, 8, 9, 10, 11, 12, 13, 19, 14, 15, 16, 17, 18]
    assert sorted(order) == list(range(20))
    return {"title": "Timers, seconds and the 60-second challenge", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Hours and minutes on an analog clock</h2>"
        "<p>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "When the long hand goes all the way around once, 60 minutes pass. "
        "In that time the short hand moves from one number to the next: <b>60 minutes = 1 hour</b>.</p>"
        "<p>Each number on the clock is <b>5 minutes</b> for the long hand, so count by 5s.</p>"
        "<figure class='sn-fig'>" + clock_svg(8, 35, size=230) +
        "<figcaption>The long hand points to 7: 7 × 5 = 35 minutes. The short hand is between 8 and 9. "
        "It has not reached 9 yet, so the hour is 8. It is <b>8:35</b>, or 25 to 9.</figcaption></figure>"
        "<h2>Past and to</h2>"
        "<p>When the long hand is on the right side, say minutes <b>past</b> the hour. "
        "When it is on the left side, say minutes <b>to</b> the next hour.</p>"
        + table(["Digital", "We say"], [["4:00", "4 o’clock"], ["4:15", "quarter past 4"], ["4:20", "20 past 4"],
                                        ["4:30", "half past 4"], ["4:35", "25 to 5"], ["4:45", "quarter to 5"],
                                        ["4:50", "10 to 5"]]) +
        "<h2>To the nearest minute</h2>"
        "<p>Between two numbers there are 5 small marks, one for each minute. Count by 5s to the last number, then by 1s.</p>"
        + ex("Read to the minute", "The long hand is 2 small marks past the 7. The short hand is between 4 and 5.",
             "Count by 5s to the 7: 5, 10, 15, 20, 25, 30, 35. Then 36, 37. The hour is still 4.", "4:37") +
        "<figure class='sn-fig'>" + clock_svg(4, 37, size=230) +
        "<figcaption>The digital time is <b>4:37</b>. It is 23 minutes to 5, because 60 − 37 = 23.</figcaption></figure>"
        "<h2>a.m. and p.m.</h2>"
        "<p>A digital clock shows the hour, then a colon, then the minutes. "
        "<b>a.m.</b> is from midnight to noon (night and morning). <b>p.m.</b> is from noon to midnight (afternoon and evening).</p>"
        + ex("a.m. or p.m.?", "Maya eats breakfast at 25 to 8. Write the time.",
             "25 to 8 is 35 minutes past 7. Breakfast is in the morning, so it is a.m.", "7:35 a.m.") +
        "<h2>Elapsed time: how long?</h2>"
        "<p>An hour has 60 minutes, not 100. Jump to the next o’clock first, then on to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(11, 45, 12, 20) +
        "<figcaption>Lunch from 11:45 a.m. to 12:20 p.m.: 15 minutes to 12:00 noon, then 20 more minutes. "
        "15 + 20 = 35 minutes.</figcaption></figure>"
        + ex("Same hour", "Recess is from 10:15 a.m. to 10:30 a.m. How long is it?", "30 − 15 = 15", "15 minutes") +
        "<h2>Timers and seconds</h2>"
        "<p><b>1 minute = 60 seconds</b>. A stopwatch hand goes once around in 60 seconds, and its numbers count by 5s. "
        "A digital timer shows minutes, a colon, then seconds: 1:30 is 1 minute 30 seconds = 90 seconds.</p>"
        "<figure class='sn-fig'>" + stopwatch_svg(40) +
        "<figcaption>The hand points to 40, so the stopwatch shows <b>40 seconds</b>. "
        "In a 60-second challenge, there are 60 − 40 = 20 seconds left.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Swapping the hands: reading 8:35 as 7:40", "The short hand is the hour. The long hand is the minutes"],
            ["Short hand just before 9 read as 9:35", "The short hand has not reached 9 yet, so the hour is still 8: 8:35"],
            ["Long hand on 4 read as 4 minutes", "Each number is 5 minutes: 4 × 5 = 20 minutes"],
            ["Breakfast at 7:30 p.m.", "Morning times are a.m.: 7:30 a.m."],
            ["10:50 to 11:20 worked out as 1120 − 1050 = 70 minutes", "An hour has 60 minutes, not 100. Count on: 10 + 20 = 30 minutes"],
            ["1 minute 20 seconds = 120 seconds", "A minute has 60 seconds: 60 + 20 = 80 seconds"],
        ])
    )


FAQ = [
    {"q": "What should a Grade 3 student know about time in Ontario?",
     "a": "In the Ontario math curriculum (expectation E2.6), Grade 3 students use analog and digital clocks and timers to tell time in hours, minutes and seconds."},
    {"q": "What is the difference between a.m. and p.m.?",
     "a": "a.m. times are from midnight to noon (night and morning). p.m. times are from noon to midnight (afternoon and evening), so school starts at an a.m. time and dinner is at a p.m. time."},
    {"q": "Is telling time on the Grade 3 EQAO math assessment?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum expectations, and using clocks and timers is one of them. Practising clocks, a.m. and p.m., and elapsed time is good preparation."},
    {"q": "How can I help my child learn to tell time?",
     "a": "Keep an analog clock at home and ask the time at everyday moments, such as breakfast or bedtime. Start with o’clock and half past, then count by 5s, then by 1s, and use a kitchen timer to feel how long 60 seconds is."},
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
    rnd = random.Random(33810)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_five(rnd), set_minute(rnd), set_ampm(rnd, people), set_elapsed(rnd, people), set_timers(rnd, people)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "telling-time", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Telling Time: Clocks, a.m. and p.m., Elapsed Time and Timers",
        "seo_title": "Grade 3 Telling Time Worksheets: Analog and Digital Clocks, Elapsed Time and Timers (Free, Ontario)",
        "short_title": "Telling time",
        "domain": "Spatial Sense",
        "standard_code": "Grade 3: E2.6",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use analog and digital clocks and timers to tell time in hours, minutes, and seconds",
        "meta_desc": "Free Grade 3 math worksheets on telling time for the Ontario curriculum: read analog clocks to the 5 minutes and to the minute, match analog and digital clocks, a.m. and p.m., elapsed time, and timers in seconds. 100 questions with an answer key, good practice for EQAO.",
        "key_big": "Short hand: the hour. Long hand: count by 5s, then by 1s.",
        "key_sub": "1 hour = 60 minutes and 1 minute = 60 seconds, not 100. If the short hand has not reached a number yet, it is still the hour before. a.m. is midnight to noon; p.m. is noon to midnight.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "time line")
    mark_large(u, "four analog clocks")
    mark_large(u, "start and end clocks")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
