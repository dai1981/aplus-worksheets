# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Telling Time and Elapsed Time (3.MD.A.1)
  python tools/gen_us_math_g3_time.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
LINE = "#2b2b2b"
NAMES = ["Maya", "Leo", "Ava", "Noah", "Mia", "Eli", "Zoe", "Sam", "Lily", "Ben", "Emma", "Omar", "Kai", "Nora", "Jack", "Ruby"]


# ------------------------------------------------------------ helpers
def tm(h, m, ap=""):
    h = (h - 1) % 12 + 1
    return "%d:%02d%s" % (h, m, (" " + ap) if ap else "")


def add(h, m, mins):
    t = (h * 60 + m + mins) % (24 * 60)
    return t // 60, t % 60


def mins_text(n):
    if n < 60:
        return "%d minute%s" % (n, "" if n == 1 else "s")
    hh, mm = divmod(n, 60)
    s = "%d hour%s" % (hh, "" if hh == 1 else "s")
    return s + (" %d minute%s" % (mm, "" if mm == 1 else "s") if mm else "")


def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    def tidy(t):
        return t.replace("a.m..", "a.m.").replace("p.m..", "p.m.").replace("m.</b>.", "m.</b>")
    return {"q": tidy(q), "c": ch, "a": ch.index(correct), "e": tidy(e)}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def clock_svg(h, m, size=200, numbers=True):
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
    if numbers:
        s.append("<g font-size='19' font-weight='700' fill='%s' text-anchor='middle'>" % LINE)
        for n in range(1, 13):
            a = math.radians(n * 30 - 90)
            rn = R - 29
            s.append("<text x='%.0f' y='%.0f'>%d</text>" % (c + rn * math.cos(a), c + rn * math.sin(a) + 7, n))
    if numbers:
        s.append("</g>")
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='8' stroke-linecap='round'/>"
             % (c, c, c + R * 0.5 * math.cos(ah), c + R * 0.5 * math.sin(ah), LINE))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#d6453b' stroke-width='4.5' stroke-linecap='round'/>"
             % (c, c, c + R * 0.8 * math.cos(am), c + R * 0.8 * math.sin(am)))
    s.append("<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (c, c, LINE))
    return svg_wrap(size, size, "".join(s), "clock showing %s" % tm(h, m))


def timeline_svg(h1, m1, h2, m2, W=420):
    """Start -> next hour -> end, with the two jumps labeled."""
    t1, t2 = h1 * 60 + m1, h2 * 60 + m2
    mid = (h1 + 1) * 60 if m1 else None
    L, R, Y = 30, W - 30, 70
    def X(t):
        return L + (R - L) * (t - t1) / float(t2 - t1)
    pts = [t1] + ([mid] if mid and t1 < mid < t2 else []) + [t2]
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for t in pts:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X(t), Y - 10, X(t), Y + 10, LINE))
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X(t), Y + 32, LINE, tm(t // 60, t % 60)))
    for a, b in zip(pts, pts[1:]):
        x1, x2 = X(a), X(b)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='#d6453b' stroke-width='2.5'/>"
                 % (x1, Y - 12, (x1 + x2) / 2, Y - 52, x2, Y - 12))
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='800' fill='#d6453b' text-anchor='middle'>+%d min</text>"
                 % ((x1 + x2) / 2, Y - 40, b - a))
    return svg_wrap(W, 112, "".join(s), "time line from %s to %s" % (tm(h1, m1), tm(h2, m2)))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def read_cands(h, m):
    """Typical wrong readings of a clock showing h:m."""
    c = []
    n = m // 5
    if 1 <= n <= 12 and h * 5 < 60:
        c.append(tm(n, h * 5))                       # hands mixed up
    c.append(tm(h + 1, m))                           # hour hand read as the next number
    if m >= 10 and n >= 1:
        c.append(tm(h, n))                           # minute number read as minutes (3:05 for 3:25)
    c.append(tm(h - 1, m))
    c.append(tm(h, (m + 5) % 60))
    c.append(tm(h, (m - 5) % 60))
    c.append(tm(h, (m + 10) % 60))
    return c


# ============================================================ set 1: read the clock (5 minutes)
def set_five(rnd):
    its = []
    times = [(h, m) for h in range(1, 13) for m in range(0, 60, 5)]
    rnd.shuffle(times)
    seen_m = set()
    pick = []
    for h, m in times:                   # spread the minutes out
        if m in seen_m and len(seen_m) < 12:
            continue
        seen_m.add(m)
        pick.append((h, m))
        if len(pick) == 20:
            break
    for h, m in pick:
        n = m // 5
        hour_tip = ("The short hand is <b>between %d and %d</b>, so the hour is still <b>%d</b>." % (h, h % 12 + 1, h)
                    if m else "The short hand points to <b>%d</b>." % h)
        min_tip = ("The long hand points to <b>%d</b>. Count by 5s: %d × 5 = <b>%d minutes</b>." % (n, n, m)
                   if m else "The long hand points to <b>12</b>: <b>0 minutes</b>, so write :00.")
        its.append(mcq(fig(clock_svg(h, m)) + "What time is it?", tm(h, m), read_cands(h, m),
                       hour_tip + " " + min_tip + " It is %s." % tm(h, m), rnd))
    return {"title": "Read the clock (5 minutes)", "items": its}


# ============================================================ set 2: read the clock (1 minute)
def set_one(rnd):
    its = []
    for _ in range(20):
        h = rnd.randint(1, 12)
        m = rnd.choice([x for x in range(1, 60) if x % 5])
        base = m // 5 * 5
        extra = m - base
        cands = [tm(h, x) for x in (m + 1, m - 1, base, base + 5, m + 10, m - 10) if 0 <= x < 60] + [tm(h + 1, m)]
        e = ("The long hand is <b>%d small mark%s</b> past the %d. Count by 5s to the %d (%d minutes), then count on by 1s: "
             "%d + %d = <b>%d</b>. The short hand is past the %d, so it is %s."
             % (extra, "" if extra == 1 else "s", base // 5 if base else 12, base // 5 if base else 12, base, base, extra, m, h, tm(h, m)))
        rnd.shuffle(cands)
        its.append(mcq(fig(clock_svg(h, m)) + "What time is it?", tm(h, m), cands, e, rnd))
    return {"title": "Read the clock (1 minute)", "items": its}


# ============================================================ set 3: time words and a.m./p.m.
def set_words(rnd):
    its = []
    words = []
    for h in rnd.sample(range(1, 13), 9):
        words.append(h)
    # quarter past / half past / quarter to
    for i, h in enumerate(words[:9]):
        kind = ["quarter past", "half past", "quarter to"][i % 3]
        if kind == "quarter past":
            right = tm(h, 15)
            e = "<b>Quarter past %d</b> means 15 minutes after %d:00. That is %s." % (h, h, right)
            cands = [tm(h, 45), tm(h - 1, 45), tm(h, 25), tm(h, 30)]
        elif kind == "half past":
            right = tm(h, 30)
            e = "<b>Half past %d</b> means 30 minutes after %d:00 (half of an hour). That is %s." % (h, h, right)
            cands = [tm(h - 1, 30), tm(h, 50), tm(h, 15), tm(h + 1, 30)]
        else:
            right = tm(h - 1, 45)
            e = ("<b>Quarter to %d</b> means 15 minutes <b>before</b> %d:00. One hour before is %s, plus 45 minutes: %s."
                 % (h, h, tm(h - 1, 0), right))
            cands = [tm(h, 45), tm(h, 15), tm(h - 1, 15), tm(h, 40)]
        its.append(mcq("What time is <b>%s %d</b>?" % (kind, h), right, cands, e, rnd))

    facts = [
        ("How many minutes are in 1 hour?", "60", ["100", "30", "12", "24"], "The long hand goes all the way around the clock once in one hour: <b>60 minutes</b>."),
        ("How many minutes are in half an hour?", "30", ["50", "15", "60", "20"], "Half of 60 minutes is <b>30 minutes</b>."),
        ("How many minutes are in a quarter hour?", "15", ["25", "4", "30", "45"], "A quarter is one of 4 equal parts. 60 ÷ 4 = <b>15 minutes</b>."),
    ]
    for q, a, w, e in facts:
        its.append(mcq(q, a, w, e, rnd))

    ampm = [
        ("School starts in the morning. Which time could it be?", "8:00 a.m.", ["8:00 p.m.", "2:00 a.m.", "11:30 p.m."]),
        ("Which time is in the <b>afternoon</b>?", "3:15 p.m.", ["3:15 a.m.", "9:00 a.m.", "11:45 a.m."]),
        ("You eat dinner in the evening. Which time could it be?", "6:30 p.m.", ["6:30 a.m.", "12:30 a.m.", "10:00 a.m."]),
        ("Which time is <b>after midnight and before noon</b>?", "7:20 a.m.", ["7:20 p.m.", "12:40 p.m.", "4:00 p.m."]),
        ("You go to bed at night. Which time could it be?", "9:00 p.m.", ["9:00 a.m.", "1:00 p.m.", "11:00 a.m."]),
    ]
    for q, a, w in ampm:
        e = ("<b>a.m.</b> is from midnight to noon (night and morning). <b>p.m.</b> is from noon to midnight "
             "(afternoon and evening). The answer is %s." % a)
        its.append(mcq(q, a, w, e, rnd))

    h = rnd.randint(2, 11)
    its.append(mcq("How do you say %s?" % tm(h, 45), "quarter to %d" % (h + 1),
                   ["quarter past %d" % h, "quarter to %d" % h, "half past %d" % h],
                   "%s is 15 minutes before %d:00, so it is <b>quarter to %d</b>." % (tm(h, 45), h + 1, h + 1), rnd))
    h = rnd.randint(1, 11)
    its.append(mcq("How do you say %s?" % tm(h, 30), "half past %d" % h,
                   ["half past %d" % (h + 1), "quarter past %d" % h, "quarter to %d" % h],
                   "%s is 30 minutes after %d:00, so it is <b>half past %d</b>." % (tm(h, 30), h, h), rnd))
    h = rnd.randint(1, 11)
    its.append(mcq("How do you say %s?" % tm(h, 15), "quarter past %d" % h,
                   ["quarter to %d" % h, "quarter past %d" % (h + 1), "half past %d" % h],
                   "%s is 15 minutes after %d:00, so it is <b>quarter past %d</b>." % (tm(h, 15), h, h), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Time words, a.m. and p.m.", "items": its}


# ============================================================ set 4: elapsed time
def elapsed_e(h1, m1, h2, m2):
    d = (h2 * 60 + m2) - (h1 * 60 + m1)
    if m2 == 0 and h2 == h1 + 1:
        return "From %s to the next hour, %s, is 60 − %d = <b>%d minutes</b>." % (tm(h1, m1), tm(h2, 0), m1, d)
    if h1 == h2 or m1 == 0:
        return ("Count on from %s to %s: %d − %d = <b>%d minutes</b>." % (tm(h1, m1), tm(h2, m2), m2 + 60 * (h2 - h1), m1, d)
                if h1 == h2 else "From %s to %s is <b>%s</b>." % (tm(h1, m1), tm(h2, m2), mins_text(d)))
    to_hour = 60 - m1
    return ("Jump to the next hour first: %s to %s is %d minutes. Then %s to %s is %d minutes. "
            "%d + %d = <b>%s</b>." % (tm(h1, m1), tm(h1 + 1, 0), to_hour, tm(h1 + 1, 0), tm(h2, m2), d - to_hour,
                                      to_hour, d - to_hour, mins_text(d)))


def set_elapsed(rnd):
    its = []
    seen = set()
    i = 0
    while len(its) < 20:
        i = len(its)
        h1 = rnd.randint(1, 10)
        if i < 6:                                # inside one hour
            m1 = rnd.choice(range(0, 40, 5))
            d = rnd.choice(range(10, 60 - m1 + 1, 5))
        elif i < 16:                             # crosses the hour
            m1 = rnd.choice(range(25, 56, 5)) if i % 2 else rnd.choice([x for x in range(21, 59) if x % 5])
            d = rnd.randint(70 - m1 if 70 - m1 > 10 else 12, 59)
            if (m1 + d) // 60 != 1:
                d = 60 - m1 + rnd.randint(5, 30)
        else:                                    # more than an hour
            m1 = rnd.choice(range(0, 56, 5))
            d = rnd.choice([65, 70, 75, 80, 90, 95, 100, 105, 110])
        h2, m2 = add(h1, m1, d)
        h2 = h1 + (m1 + d) // 60
        if (h1, m1, d) in seen:
            continue
        seen.add((h1, m1, d))
        q = "How much time passes from <b>%s</b> to <b>%s</b>?" % (tm(h1, m1), tm(h2, m2))
        if i in (6, 7, 8):
            q = fig(timeline_svg(h1, m1, h2, m2)) + q
        naive = abs(m2 - m1)
        cands = [mins_text(naive) if naive else None, mins_text(d + 5), mins_text(d - 5),
                 mins_text(d + 60) if d < 60 else mins_text(d - 60), mins_text(d + 10), mins_text(d - 10)]
        its.append(mcq(q, mins_text(d), [c for c in cands if c and not c.startswith("-")], elapsed_e(h1, m1, h2, m2), rnd))
    return {"title": "How much time passes?", "items": its}


# ============================================================ set 5: word problems
def set_story(rnd):
    its = []
    names = NAMES[:]
    rnd.shuffle(names)
    nm = iter(names * 3)
    acts = [  # what, how, finish, earliest hour, latest hour, a.m./p.m.
        ("starts reading", "reads", "finish reading", 7, 8, "p.m."),
        ("starts soccer practice", "practices", "finish practice", 3, 5, "p.m."),
        ("puts a cake in the oven", "bakes it", "take the cake out", 2, 4, "p.m."),
        ("starts a movie", "watches it", "finish the movie", 6, 7, "p.m."),
        ("starts homework", "works", "finish homework", 3, 5, "p.m."),
        ("gets on the school bus", "rides", "get to school", 7, 7, "a.m."),
        ("starts piano practice", "plays", "stop playing", 4, 5, "p.m."),
        ("starts cleaning the room", "cleans", "finish cleaning", 9, 10, "a.m."),
        ("starts a bike ride", "rides", "finish the ride", 10, 11, "a.m."),
        ("starts painting a picture", "paints", "finish painting", 1, 3, "p.m."),
    ]
    for i in range(10):                         # find the end time
        a = acts[i]
        p = next(nm)
        h = rnd.randint(a[3], a[4])
        ap = a[5]
        m = rnd.choice(range(0, 60, 5)) if i % 3 else rnd.choice([x for x in range(1, 59) if x % 5])
        d = rnd.choice([25, 30, 35, 40, 45, 50, 55, 65, 75, 90] if i % 2 else [10, 15, 20, 25, 35, 40, 45])
        if a[5] == "a.m." and a[2] == "get to school":
            d = rnd.choice([15, 20, 25, 30, 35])
        h2, m2 = add(h, m, d)
        if ap == "a.m." and h2 >= 12:
            ap2 = "p.m."
        else:
            ap2 = ap
        end = tm(h2, m2, ap2)
        q = "%s %s at %s and %s for %s. What time does %s %s?" % (p, a[0], tm(h, m, ap), a[1], mins_text(d), p, a[2])
        to_hour = 60 - m
        if m and d > to_hour:
            e = ("Add in two jumps. %s + %s = %s. Then add the other %s: <b>%s</b>"
                 % (tm(h, m, ap), mins_text(to_hour), tm(h + 1, 0, ap2), mins_text(d - to_hour), end))
        else:
            e = "%s + %s = <b>%s</b>" % (tm(h, m, ap), mins_text(d), end)
        cands = [tm(h2, x, ap2) for x in (m2 + 10, m2 - 10, m2 + 5) if 0 <= x < 60] + [tm(h2 + 1, m2, ap2), tm(h2 - 1, m2, ap2)]
        if m + d >= 60 and (m + d) % 60 != m2:
            pass
        if m + d >= 60:
            cands.insert(0, tm(h, (m + d) % 60, ap))   # forgot to change the hour
        its.append(mcq(q, end, cands, e, rnd))

    for i in range(6):                          # find the start time
        p = next(nm)
        h2 = rnd.randint(2, 7)
        m2 = rnd.choice(range(0, 60, 5))
        d = rnd.choice([20, 25, 30, 40, 45, 50, 55, 70])
        t = h2 * 60 + m2 - d
        h1, m1 = t // 60, t % 60
        ev = ["a swim lesson", "a math test", "a game", "a walk", "a show", "a class trip"][i]
        q = "%s finished %s at %s. It took %s. What time did it <b>start</b>?" % (p, ev, tm(h2, m2, "p.m."), mins_text(d))
        if m2 and d > m2:
            e = ("Count <b>back</b> in two jumps: %s − %s = %s. Then go back the other %s: <b>%s</b>"
                 % (tm(h2, m2, "p.m."), mins_text(m2), tm(h2, 0, "p.m."), mins_text(d - m2), tm(h1, m1, "p.m.")))
        else:
            e = "Count <b>back</b> %s from %s: <b>%s</b>" % (mins_text(d), tm(h2, m2, "p.m."), tm(h1, m1, "p.m."))
        cands = [tm(*add(h2, m2, d), ap="p.m.") if False else None]
        hh, mm = add(h2, m2, d)
        cands = [tm(hh, mm, "p.m."), tm(h1 + 1, m1, "p.m."), tm(h1, (m1 + 10) % 60, "p.m."), tm(h1 - 1, m1, "p.m."), tm(h1, (m1 - 5) % 60, "p.m.")]
        its.append(mcq(q, tm(h1, m1, "p.m."), cands, e, rnd))

    for i in range(4):                          # how long
        p = next(nm)
        h1 = rnd.randint(1, 9)
        m1 = rnd.choice(range(10, 56, 5))
        d = rnd.choice([25, 35, 40, 45, 50, 55])
        h2, m2 = add(h1, m1, d)
        h2 = h1 + (m1 + d) // 60
        ev = ["at the park", "at the library", "at the museum", "at swim practice"][i]
        q = "%s got to %s at %s and left at %s. How long was %s there?" % (p, ev.replace("at the ", "the ").replace("at swim", "swim"),
                                                                            tm(h1, m1, "p.m."), tm(h2, m2, "p.m."), p)
        naive = abs(m2 - m1)
        cands = [mins_text(naive) if naive else None, mins_text(d + 5), mins_text(d - 5), mins_text(d + 60), mins_text(d + 10)]
        its.append(mcq(q, mins_text(d), [c for c in cands if c], elapsed_e(h1, m1, h2, m2), rnd))
    assert len(its) == 20
    return {"title": "Time word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The two hands</h2>"
        "<figure class='sn-fig'>" + clock_svg(3, 25, size=230) +
        "<figcaption>The <b>short hand</b> (black) shows the hour. The <b>long hand</b> (red) shows the minutes. This clock shows 3:25.</figcaption></figure>"
        "<ol class='rk-step'>"
        "<li><b>Hour:</b> look at the short hand. If it is between two numbers, use the <b>smaller</b> one (between 3 and 4 means 3).</li>"
        "<li><b>Minutes:</b> look at the long hand. Count by 5s for each number: 1 is 5, 2 is 10, 3 is 15 … 12 is 0.</li>"
        "<li><b>Write it:</b> hour, colon, two-digit minutes: 3:25, 7:05, 10:00.</li></ol>"
        + table(["Long hand on", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                [["Minutes", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "0"]]) +
        "<h2>To the nearest minute</h2>"
        "<p>Between two numbers there are <b>5 small marks</b>, one for each minute. Count by 5s to the last number the long hand passed, "
        "then count on by 1s.</p>"
        "<figure class='sn-fig'>" + clock_svg(8, 37, size=230) +
        "<figcaption>The long hand is 2 marks past the 7. Count 5, 10 … 35, then 36, 37. The time is 8:37.</figcaption></figure>"
        "<h2>Time words, a.m. and p.m.</h2>"
        + table(["Words", "Time", "Means"], [
            ["o'clock", "4:00", "exactly on the hour"],
            ["quarter past 4", "4:15", "15 minutes after 4"],
            ["half past 4", "4:30", "30 minutes after 4"],
            ["quarter to 5", "4:45", "15 minutes before 5"],
        ]) +
        "<p><b>a.m.</b> is from midnight to noon: night and morning. <b>p.m.</b> is from noon to midnight: afternoon and evening. "
        "1 hour = 60 minutes, half an hour = 30 minutes, a quarter hour = 15 minutes.</p>"
        "<h2>How much time passes (elapsed time)</h2>"
        "<p>Do not just subtract the minutes. Use a <b>time line</b>: jump to the next hour first, then jump to the end time, and add the jumps.</p>"
        "<figure class='sn-fig'>" + timeline_svg(3, 40, 4, 15) +
        "<figcaption>3:40 to 4:00 is 20 minutes. 4:00 to 4:15 is 15 minutes. 20 + 15 = 35 minutes.</figcaption></figure>"
        + ex("Find the end time", "Ana starts reading at 4:35 p.m. and reads for 40 minutes. When does she finish?",
             "4:35 + 25 minutes = 5:00. 40 − 25 = 15 more minutes: 5:15.", "5:15 p.m.")
        + ex("Find the start time", "A show ended at 7:10 p.m. It lasted 30 minutes. When did it start?",
             "Count back 10 minutes to 7:00, then 20 more minutes to 6:40.", "6:40 p.m.")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Mixing up the hands (reading 3:25 as 5:15)", "Short hand = hour, long hand = minutes"],
            ["Reading 3:50 as 4:50 because the short hand is near the 4", "If the short hand has not reached the number, use the number before it"],
            ["Reading the long hand on 5 as 5 minutes", "Each number on the clock is worth 5 minutes: 5 × 5 = 25"],
            ["3:40 to 4:15 = 25 minutes (15 − 40)", "Jump to 4:00 first: 20 + 15 = 35 minutes"],
        ])
    )


FAQ = [
    {"q": "When do kids learn to tell time to the nearest minute?",
     "a": "In the Common Core, students tell time to the nearest hour and half hour in Grade 1, to the nearest five minutes in Grade 2, and to the nearest minute in Grade 3, along with elapsed time."},
    {"q": "How do you teach a child to read an analog clock?",
     "a": "Read the short hand first for the hour, then count the long hand by 5s for the minutes. When the long hand is between numbers, count on by 1s from the last number it passed."},
    {"q": "What is elapsed time?",
     "a": "Elapsed time is how much time passes from a start time to an end time, such as from 3:40 to 4:15 (35 minutes)."},
    {"q": "What is the easiest way to find elapsed time?",
     "a": "Use a time line. Jump from the start time to the next hour, then from that hour to the end time, and add the jumps together."},
    {"q": "What do a.m. and p.m. mean?",
     "a": "a.m. is used for times from midnight to noon, and p.m. is used for times from noon to midnight."},
]


def gen_time():
    rnd = random.Random(36)
    sets = [set_five(rnd), set_one(rnd), set_words(rnd), set_elapsed(rnd), set_story(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert all("-" not in c.split(":")[0] for c in it["c"]), it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "telling-time", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Telling Time and Elapsed Time",
        "seo_title": "Grade 3 Telling Time Worksheets: Nearest Minute and Elapsed Time (with Clocks)",
        "short_title": "Telling time",
        "domain": "Measurement and Data",
        "standard_code": "3.MD.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/MD/A/1/",
        "standard_text": "Tell and write time to the nearest minute, measure time intervals in minutes, and solve word problems about elapsed time.",
        "meta_desc": "Free Grade 3 telling time worksheets with clock pictures: read the clock to the nearest 5 minutes and the nearest minute, quarter past and quarter to, a.m. and p.m., and elapsed time word problems. 100 practice questions with answers.",
        "key_big": "Short hand = hour. Long hand = minutes: count by 5s, then by 1s.",
        "key_sub": "If the short hand is between two numbers, use the smaller one. To find how much time passes, jump to the next hour first, then add the jumps.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_time()
    path = os.path.join(OUT, "telling-time.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
