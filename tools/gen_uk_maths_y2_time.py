# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Telling the Time to 5 Minutes (National Curriculum in England, Measurement)
  python3 tools/gen_uk_maths_y2_time.py
Every clock picture is drawn from the time itself (the short hand moves between the numbers).
Every answer is worked out in code. Wrong answers come from real pupil mistakes:
the short hand read as the next number ("25 to 9" read as 9:35), the number the long hand points to
read as minutes (pointing at 4 = 4 minutes), past and to mixed up, quarter to read as 45 past the next hour.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
GRAY = "#9aa3a0"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Oliver", "he"), ("Amelia", "she"), ("Harry", "he"), ("Isla", "she"), ("Mohammed", "he"), ("Freya", "she"),
          ("Jack", "he"), ("Poppy", "she"), ("Arjun", "he"), ("Ava", "she"), ("Noah", "he"), ("Aisha", "she"),
          ("George", "he"), ("Lily", "she"), ("Leo", "he"), ("Zara", "she"), ("Alfie", "he"), ("Grace", "she"),
          ("Kai", "he"), ("Ruby", "she"), ("Ethan", "he"), ("Maya", "she"), ("Charlie", "he"), ("Evie", "she")]


# ------------------------------------------------------------ time words
def h12(h):
    return (h - 1) % 12 + 1


def nxt(h):
    return h12(h + 1)


def prv(h):
    return h12(h - 1)


def words(h, m):
    """UK clock words: 20 past 7, 25 to 4, quarter to 9, half past 6, 3 o’clock"""
    h = h12(h)
    assert m % 5 == 0 and 0 <= m < 60
    if m == 0:
        return "%d o’clock" % h
    if m == 15:
        return "quarter past %d" % h
    if m == 30:
        return "half past %d" % h
    if m == 45:
        return "quarter to %d" % nxt(h)
    if m < 30:
        return "%d past %d" % (m, h)
    return "%d to %d" % (60 - m, nxt(h))


def dig(h, m):
    return "%d:%02d" % (h12(h), m)


def mins(n):
    return "%d minute%s" % (n, "" if n == 1 else "s")


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def to_min(h, m):
    return (h % 12) * 60 + m


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    seen = {correct}
    pick = []
    for c in cands:
        if not c or c in seen:
            continue
        seen.add(c)
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
        s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle'>" % (15 * k, RED))
        for n in range(1, 13):
            a = math.radians(n * 30 - 90)
            rn = R + 17 * k
            s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + 5 * k, (n * 5) % 60))
        s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200, ring=False):
    assert hands_gap(h, m) >= 12, (h, m)
    pad = 26 if ring else 0
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6 - pad, ring), "clock showing %s" % words(h, m))


def clocks4_svg(times):
    """2 x 2 grid of clocks labelled A to D (a square picture)."""
    CELL = 124
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY)]
    for k, (h, m) in enumerate(times):
        assert hands_gap(h, m) >= 12, (h, m)
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        el.append(clock_body(h, m, x0 + 65, y0 + 63, 56))
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 20, LINE, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), "four clocks labelled A to D")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def count5(n):
    return ", ".join(str(5 * i) for i in range(1, n + 1))


def count5_back(n):
    return ", ".join(str(5 * i) for i in range(1, n + 1))


def hand_text(h, m):
    """How to read the two hands (for explanations)."""
    h = h12(h)
    n = m // 5
    if m == 0:
        return "The long hand points to the <b>12</b>. The short hand points to the <b>%d</b>." % h
    if m == 30:
        mm = "The long hand points to the <b>6</b>: half way round, so it is <b>half past</b>."
    elif m == 15:
        mm = "The long hand points to the <b>3</b>: a quarter of the way round, so it is <b>quarter past</b>."
    elif m == 45:
        mm = "The long hand points to the <b>9</b>: a quarter of an hour before the 12, so it is <b>quarter to</b>."
    elif m < 30:
        mm = ("The long hand points to the <b>%d</b>. Count in 5s from the 12: %s. That is <b>%d minutes past</b>."
              % (n, count5(n), m))
    else:
        mm = ("The long hand points to the <b>%d</b>. Count in 5s back to the 12: %s. That is <b>%d minutes to</b>."
              % (n, count5_back(12 - n), 60 - m))
    hh = "The short hand is between <b>%d</b> and <b>%d</b>." % (h, nxt(h))
    return mm + " " + hh


# ============================================================ set 1: o'clock, half past, quarter past / to
def set_quarters(rnd):
    its = []
    used = set()

    def pick(m):
        hs = [x for x in range(1, 13) if (x, m) not in used and hands_gap(x, m) >= 20]
        h = rnd.choice(hs)
        used.add((h, m))
        return h

    for m in [0, 0, 0, 30, 30, 30, 15, 15, 15, 45, 45, 45]:
        h = pick(m)
        right = words(h, m)
        if m == 0:
            c = ["12 o’clock" if h != 12 else "6 o’clock", words(h, 30), words(nxt(h), 0), words(prv(h), 0)]
            e = ("%s So it is <b>%s</b>. (The long hand on the 12 does not mean 12 o’clock. The short hand tells the hour.)"
                 % (hand_text(h, m), right))
        elif m == 30:
            c = [words(nxt(h), 30), "6 o’clock" if h != 6 else "12 o’clock", words(h, 15), words(prv(h), 30)]
            e = ("%s The short hand has not reached the %d yet, so the hour is still %d. It is <b>%s</b>."
                 % (hand_text(h, m), nxt(h), h, right))
        elif m == 15:
            c = ["quarter to %d" % h, "3 past %d" % h, words(nxt(h), 15), words(h, 30)]
            e = "%s The short hand has just passed the %d. It is <b>%s</b>." % (hand_text(h, m), h, right)
        else:
            c = ["quarter to %d" % h, "quarter past %d" % nxt(h), "quarter past %d" % h, "45 past %d" % nxt(h)]
            e = ("%s The short hand is nearly at the %d, but not there yet. In 15 more minutes it will be %d o’clock. "
                 "So it is <b>%s</b>." % (hand_text(h, m), nxt(h), nxt(h), right))
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show?", right, c, e))

    its.append(mcq("At <b>half past</b>, where does the long hand point?", "the 6", ["the 3", "the 12", "the 9"],
                   "Half past means the long hand has gone <b>half way</b> round the clock, from the 12 to the <b>6</b>."))
    its.append(mcq("At <b>quarter past</b>, where does the long hand point?", "the 3", ["the 9", "the 6", "the 4"],
                   "Quarter past means the long hand has gone a quarter of the way round, from the 12 to the <b>3</b>. "
                   "(The 9 is for quarter to.)"))
    its.append(mcq("At <b>quarter to</b>, where does the long hand point?", "the 9", ["the 3", "the 6", "the 4"],
                   "Quarter to means a quarter of an hour <b>before</b> the 12. The long hand points to the <b>9</b>. "
                   "(The 3 is for quarter past.)"))
    h = pick(30)
    its.append(mcq("At <b>half past %d</b>, where is the short hand?" % h, "between %d and %d" % (h, nxt(h)),
                   ["on the %d" % h, "on the %d" % nxt(h), "between %d and %d" % (prv(h), h)],
                   "In half an hour the short hand moves half way to the next number. At half past %d it is "
                   "<b>between %d and %d</b>." % (h, h, nxt(h))))
    its.append(mcq("Quarter past 6 is how many minutes after 6 o’clock?", "15", ["45", "30", "3"],
                   "A quarter of an hour is <b>15 minutes</b>. Count in 5s from the 12 to the 3: 5, 10, 15. "
                   "(3 is the number, not the minutes.)"))
    its.append(mcq("Quarter to 6 is how many minutes before 6 o’clock?", "15", ["45", "9", "30"],
                   "Quarter to 6 is a quarter of an hour before 6 o’clock. That is <b>15 minutes</b>. "
                   "Count in 5s back from the 12 to the 9: 5, 10, 15."))
    its.append(mcq("Which digital time is the same as <b>half past 3</b>?", "3:30", ["4:30", "3:03", "3:06"],
                   "Half past 3 is 30 minutes after 3 o’clock. On a digital clock it is <b>3:30</b>. "
                   "(Not 4:30: the hour is still 3.)"))
    its.append(mcq("Which digital time is the same as <b>quarter to 6</b>?", "5:45", ["6:45", "6:15", "5:15"],
                   "Quarter to 6 is 15 minutes <b>before</b> 6 o’clock, so it is still in the 5 o’clock hour: 45 minutes past 5. "
                   "That is <b>5:45</b>. (6:45 is quarter to 7.)"))
    assert len(its) == 20
    return {"title": "O’clock, half past, quarter past and quarter to", "items": its}


# ============================================================ set 2: minutes past the hour
def set_past(rnd):
    its = []
    for n in [2, 4, 1, 5]:
        m = 5 * n
        c = [mins(n), mins(m + 5), mins(m - 5) if m > 5 else mins(15), mins(60 - m)]
        its.append(mcq("The long hand points to the <b>%d</b>. How many minutes past the hour is it?" % n, mins(m), c,
                       "Each number on the clock is <b>5 minutes</b>. Count in 5s from the 12 to the %d: %s. "
                       "It is <b>%s</b> past. (Not %s: the number is not the minutes.)" % (n, count5(n), mins(m), mins(n))))
    used = set()
    plan = [10, 5, 20, 25, 10, 5, 20, 25, 20, 10, 25, 5]
    for m in plan:
        n = m // 5
        hs = [x for x in range(1, 13) if (x, m) not in used and hands_gap(x, m) >= 20 and x != n]
        h = rnd.choice(hs)
        used.add((h, m))
        right = words(h, m)
        c = ["%d to %d" % (m, h),                       # past and to mixed up
             "%d minutes past %d" % (n, h) if n > 1 else "1 minute past %d" % h,   # number read as minutes
             "%d past %d" % (m, nxt(h)),               # short hand read as the next number
             "%d past %d" % (m + 5, h)]
        e = ("%s So it is <b>%s</b>. The long hand is on the right-hand side, so we say <b>past</b>."
             % (hand_text(h, m), right))
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show?", right, c, e))
    for h, m in [(3, 25), (7, 10), (11, 20), (4, 5)]:
        n = m // 5
        c = ["the %d" % (12 - n), "the %d" % h, "the %d" % (n + 1), "the %d" % m if m <= 12 else None, "the %d" % (n - 1) if n > 1 else None]
        its.append(mcq("At <b>%s</b>, where does the long hand point?" % words(h, m), "the %d" % n, c,
                       "Count in 5s from the 12 until you say %d: %s. That is %d number%s, so the long hand points to the <b>%d</b>. "
                       "(The %d on the other side is for %d to.)" % (m, count5(n), n, "" if n == 1 else "s", n, 12 - n, m)))
    # order: text warm-ups, easy clocks, harder clocks, then "where does the hand point"
    assert len(its) == 20
    return {"title": "Times to 5 minutes: past the hour", "items": its}


# ============================================================ set 3: minutes to the hour
def set_to(rnd):
    its = []
    for n in [11, 8, 10, 7]:
        k = 12 - n
        c = [mins(5 * n), mins(n), mins(5 * k + 5), mins(5 * k - 5)]
        its.append(mcq("The long hand points to the <b>%d</b>. How many minutes is it <b>to</b> the next hour?" % n,
                       mins(5 * k), c,
                       "Count in 5s <b>back</b> from the %d to the 12: %s. It is <b>%s</b> to the hour. "
                       "(%s is how many minutes <b>past</b>.)" % (n, count5(k), mins(5 * k), mins(5 * n))))
    used = set()
    plan = [50, 40, 55, 35, 50, 40, 55, 35, 40, 35, 50, 55]
    for m in plan:
        n = m // 5
        hs = [x for x in range(1, 13) if (x, m) not in used and hands_gap(x, m) >= 20 and x != n and nxt(x) != n]
        h = rnd.choice(hs)
        used.add((h, m))
        right = words(h, m)
        k = 60 - m
        c = ["%d to %d" % (k, h),                        # short hand: used the number it has passed
             "%d past %d" % (k, nxt(h)),                 # past and to mixed up
             "%d to %d" % (m, nxt(h)),                   # counted from the 12 the wrong way
             "%d past %d" % (k, h)]
        e = ("%s The short hand is between %d and %d, nearly at the %d. So it is <b>%s</b>. "
             "(It is not %d to %d: the next hour is %d.)"
             % (hand_text(h, m).split(" The short hand")[0], h, nxt(h), nxt(h), right, k, h, nxt(h)))
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show?", right, c, e))
    for h, m in [(8, 35), (2, 50)]:
        w = words(h, m)
        k = 60 - m
        c = [dig(nxt(h), m), dig(nxt(h), k), dig(h, k)]
        its.append(mcq("Which digital time is the same as <b>%s</b>?" % w, dig(h, m), c,
                       "%s is %d minutes <b>before</b> %d o’clock, so it is still in the %d o’clock hour. "
                       "60 − %d = %d minutes past %d: <b>%s</b>. (%s is %d minutes after %d o’clock.)"
                       % (w[0].upper() + w[1:], k, nxt(h), h, k, m, h, dig(h, m), dig(nxt(h), m), m, nxt(h))))
    for h, m in [(3, 50), (6, 40)]:
        n = m // 5
        k = 60 - m
        c = ["the %d" % (k // 5), "the %d" % nxt(h), "the %d" % (n + 1), "the %d" % (n - 1)]
        its.append(mcq("At <b>%s</b>, where does the long hand point?" % words(h, m), "the %d" % n, c,
                       "%d to means %d minutes before the 12. Count back in 5s from the 12: %s. The long hand points to the <b>%d</b>. "
                       "(The %d is for %d past.)" % (k, k, count5(k // 5), n, k // 5, k)))
    assert len(its) == 20
    return {"title": "Times to 5 minutes: to the hour", "items": its}


# ============================================================ set 4: which clock? and time facts
def set_match(rnd):
    its = []
    picks = [(1, 15), (10, 20), (6, 45), (8, 35), (2, 50), (5, 5), (11, 30), (12, 40), (9, 25), (7, 55)]
    pos = [0, 1, 2, 3, 1, 2, 3, 0, 2, 1]
    for (h, m), p in zip(picks, pos):
        n = m // 5
        k = 60 - m
        cand = []
        if m > 30:
            cand.append((nxt(h), m))                # "25 to 9" drawn as 9:35
            cand.append((nxt(h), k))                # past and to mixed up: 25 past 9
        else:
            cand.append((h, k if k != m else 0))    # past and to mixed up: 20 to 11 side
            cand.append((prv(h), m))
        if 5 * h < 60 and n != h % 12:
            cand.append((n if n else 12, 5 * (h % 12)))   # hands swapped
        cand += [(h, (m + 5) % 60), (h, (m - 5) % 60), (nxt(h), 0)]
        wrong = []
        for t in cand:
            t = (h12(t[0]), t[1])
            if t != (h, m) and t not in wrong and hands_gap(*t) >= 15:
                wrong.append(t)
        wrong = wrong[:3]
        assert len(wrong) == 3
        rnd.shuffle(wrong)
        times = wrong[:p] + [(h, m)] + wrong[p:]
        L = "ABCD"[p]
        how = hand_text(h, m)
        e = "%s Clock <b>%s</b> shows %s." % (how, L, words(h, m))
        if m > 30:
            bad = (nxt(h), m)
            if bad in times:
                e += " (Clock %s shows %s, not %s: its short hand is past the %d.)" % ("ABCD"[times.index(bad)], words(*bad), words(h, m), nxt(h))
        its.append({"q": fig(clocks4_svg(times)) + "Which clock shows <b>%s</b>?" % words(h, m),
                    "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True})

    F = [("How many <b>minutes</b> are in 1 hour?", "60", ["100", "12", "24"],
          "There are <b>60 minutes</b> in 1 hour. The long hand goes all the way round: 12 numbers × 5 = 60. (Not 100.)"),
         ("How many <b>hours</b> are in 1 day?", "24", ["12", "60", "7"],
          "There are <b>24 hours</b> in 1 day. The short hand goes round the clock twice: 12 + 12 = 24."),
         ("How many minutes are in <b>half an hour</b>?", "30", ["50", "15", "6"],
          "1 hour is 60 minutes. Half of 60 is <b>30</b>. (Not 50: an hour is not 100 minutes.)"),
         ("How many minutes are in <b>a quarter of an hour</b>?", "15", ["25", "4", "30"],
          "1 hour is 60 minutes. A quarter of 60 is <b>15</b>. The long hand goes from the 12 to the 3: 5, 10, 15."),
         ("The long hand goes all the way round once. How long is that?", "1 hour", ["1 minute", "12 minutes", "1 day"],
          "Each number is 5 minutes, and there are 12 numbers: 60 minutes. 60 minutes is <b>1 hour</b>."),
         ("Which is the same as <b>1 day</b>?", "24 hours", ["12 hours", "60 hours", "7 hours"],
          "1 day is <b>24 hours</b>. (12 hours is only half a day.)"),
         ("The long hand moves from the <b>12</b> to the <b>6</b>. How many minutes go by?", "30", ["6", "60", "15"],
          "Count in 5s for each number: 5, 10, 15, 20, 25, 30. <b>30 minutes</b> go by. That is half an hour."),
         ("The long hand moves from the <b>3</b> to the <b>6</b>. How many minutes go by?", "15", ["3", "30", "9"],
          "From the 3 to the 6 is 3 numbers. Count in 5s: 5, 10, 15. <b>15 minutes</b> go by."),
         ("How many hours are in <b>half a day</b>?", "12", ["24", "30", "6"],
          "1 day is 24 hours. Half of 24 is <b>12 hours</b>. (30 is half an hour in minutes.)"),
         ("How many <b>days</b> are in 1 week?", "7", ["5", "24", "12"],
          "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: <b>7 days</b>. (5 is just the school days.)"),
         ]
    for q, a, c, e in F:
        its.append(mcq(q, a, c, e))
    # interleave: clocks and facts
    order = []
    for i in range(10):
        order += [i, 10 + i]
    its = [its[i] for i in order]
    assert len(its) == 20
    return {"title": "Which clock? Minutes, hours and days", "items": its}


# ============================================================ set 5: compare and order times
def set_problems(rnd, people):
    its = []

    def person():
        return next(people)

    def lat(h, m, d):
        t = (h * 60 + m + d) % 720
        return h12(t // 60) if t // 60 else 12, t % 60

    its.append(mcq("Which takes the <b>longest</b>?", "a night’s sleep",
                   ["brushing your teeth", "eating an apple", "putting on your shoes"],
                   "Brushing teeth, eating an apple and putting on shoes take a few minutes. "
                   "A night’s sleep takes many <b>hours</b>. So <b>a night’s sleep</b> takes the longest."))
    its.append(mcq("About how long does a film at the cinema last?", "2 hours", ["2 minutes", "2 days", "20 hours"],
                   "2 minutes is far too short, and 2 days or 20 hours is far too long. A film lasts about <b>2 hours</b>."))
    its.append(mcq("Which is <b>longer</b>: 1 hour or 45 minutes?", "1 hour", ["45 minutes", "They are the same", "You cannot tell"],
                   "1 hour is 60 minutes. 60 is more than 45. So <b>1 hour</b> is longer."))
    its.append(mcq("Which is the <b>shortest</b> time?", "quarter of an hour", ["half an hour", "1 hour", "40 minutes"],
                   "Quarter of an hour = 15 minutes. Half an hour = 30 minutes. 1 hour = 60 minutes. "
                   "15 is the smallest, so <b>quarter of an hour</b> is the shortest."))
    its.append(mcq("Which time is the <b>earliest</b>?", "quarter to 8", ["8 o’clock", "10 past 8", "half past 8"],
                   "Quarter to 8 is 15 minutes <b>before</b> 8 o’clock. The others are 8 o’clock or later. "
                   "So <b>quarter to 8</b> is the earliest."))
    its.append(mcq("Which time is the <b>latest</b>?", "25 to 5", ["4 o’clock", "quarter past 4", "20 past 4"],
                   "25 to 5 is 4:35. 20 past 4 is 4:20 and quarter past 4 is 4:15. 4:35 is the latest, so the answer is <b>25 to 5</b>."))
    its.append(mcq("What comes next? 3 o’clock, quarter past 3, half past 3, …", "quarter to 4",
                   ["quarter to 3", "4 o’clock", "half past 4"],
                   "Each time is 15 minutes later. 15 minutes after half past 3 is <b>quarter to 4</b>."))
    its.append(mcq("What comes next? 5 past 2, 10 past 2, quarter past 2, …", "20 past 2",
                   ["25 past 2", "20 to 2", "half past 2"],
                   "Each time is 5 minutes later. 5 minutes after quarter past 2 (15 past) is <b>20 past 2</b>."))
    its.append(mcq("It is <b>4 o’clock</b>. What time will it be <b>1 hour</b> later?", "5 o’clock",
                   ["half past 4", "3 o’clock", "4 o’clock"],
                   "1 hour later, the short hand moves on one number, from 4 to 5. It will be <b>5 o’clock</b>."))
    its.append(mcq("It is <b>half past 6</b>. What time will it be <b>1 hour</b> later?", "half past 7",
                   ["7 o’clock", "half past 8", "quarter to 7"],
                   "1 hour later, the hour goes up by 1 and the minutes stay the same. Half past 6 → <b>half past 7</b>."))
    nm, pr = person()
    its.append(mcq("%s has tea at <b>5 o’clock</b>. It is <b>4 o’clock</b> now. How long until tea?" % nm, "1 hour",
                   ["5 hours", "4 hours", "30 minutes"],
                   "From 4 o’clock to 5 o’clock the short hand moves on one number. That is <b>1 hour</b>."))
    its.append(mcq("Lunchtime starts at <b>12 o’clock</b> and ends at <b>half past 12</b>. How long is lunchtime?", "30 minutes",
                   ["12 minutes", "1 hour", "15 minutes"],
                   "The long hand moves from the 12 to the 6. Count in 5s: 5, 10, 15, 20, 25, 30. Lunchtime is <b>30 minutes</b>."))
    its.append(mcq("A TV programme starts at <b>4 o’clock</b> and ends at <b>quarter past 4</b>. How long is it?", "15 minutes",
                   ["3 minutes", "45 minutes", "1 hour"],
                   "The long hand moves from the 12 to the 3. Count in 5s: 5, 10, 15. It is <b>15 minutes</b> long. "
                   "(3 is the number, not the minutes.)"))
    assert lat(5, 0, 120) == (7, 0)
    its.append(mcq("A film starts at <b>5 o’clock</b>. It lasts <b>2 hours</b>. When does it end?", "7 o’clock",
                   ["6 o’clock", "3 o’clock", "half past 5"],
                   "Count on 2 hours: 5 o’clock → 6 o’clock → <b>7 o’clock</b>. (3 o’clock is 2 hours before.)"))
    nm, pr = person()
    assert lat(4, 15, 30) == (4, 45)
    its.append(mcq("%s’s swimming lesson starts at <b>quarter past 4</b>. It lasts <b>half an hour</b>. When does it end?" % nm,
                   "quarter to 5", ["quarter past 5", "half past 4", "quarter to 4"],
                   "Half an hour is 30 minutes. Quarter past 4 is 4:15. 4:15 + 30 minutes = 4:45. That is <b>quarter to 5</b>. "
                   "(Quarter to 4 is before the lesson starts.)"))
    nm, pr = person()
    assert lat(2, 0, 20) == (2, 20)
    its.append(mcq("%s puts a cake in the oven at <b>2 o’clock</b>. It is ready <b>20 minutes</b> later. When is it ready?" % nm,
                   "20 past 2", ["20 to 2", "20 to 3", "4 minutes past 2"],
                   "Count on 20 minutes from 2 o’clock: the long hand moves from the 12 to the 4 (5, 10, 15, 20). "
                   "It is ready at <b>20 past 2</b>. (20 to 2 is before 2 o’clock.)"))
    nm, pr = person()
    assert to_min(8, 50) - to_min(8, 40) == 10
    its.append(mcq("%s gets to the bus stop at <b>20 to 9</b>. The bus comes at <b>10 to 9</b>. How long does %s wait?" % (nm, pr),
                   "10 minutes", ["20 minutes", "30 minutes", "9 minutes"],
                   "20 to 9 is 8:40. 10 to 9 is 8:50. From 8:40 to 8:50 is <b>10 minutes</b>. (Do not add 20 and 10.)"))
    a, b = person(), person()
    its.append(mcq("%s reads for <b>20 minutes</b>. %s reads for <b>half an hour</b>. Who reads for longer, and by how much?"
                   % (a[0], b[0]), "%s, by 10 minutes" % b[0],
                   ["%s, by 10 minutes" % a[0], "%s, by 20 minutes" % b[0], "They read for the same time"],
                   "Half an hour is 30 minutes. 30 is more than 20, and 30 − 20 = 10. So <b>%s</b> reads for longer, "
                   "by <b>10 minutes</b>." % b[0]))
    its.append(mcq("Put these times in order, earliest first.", "quarter past 3, half past 3, quarter to 4",
                   ["quarter to 4, quarter past 3, half past 3", "half past 3, quarter past 3, quarter to 4",
                    "quarter past 3, quarter to 4, half past 3"],
                   "Quarter past 3 is 3:15. Half past 3 is 3:30. Quarter to 4 is 3:45. So the order is "
                   "<b>quarter past 3, half past 3, quarter to 4</b>. (Quarter to 4 comes last: it is nearly 4 o’clock.)"))
    nm, pr = person()
    assert lat(4, 10, 20) == (4, 30)
    its.append(mcq(fig(clock_svg(4, 10)) + "The clock shows when %s starts %s homework. %s works for <b>20 minutes</b>. "
                   "When does %s finish?" % (nm, "his" if pr == "he" else "her", pr.capitalize(), pr),
                   "half past 4", ["20 past 4", "half past 5", "quarter to 5"],
                   "The clock shows 10 past 4. Count on 20 minutes: 10 past, 15 past, 20 past, 25 past, half past. "
                   "%s finishes at <b>half past 4</b>." % pr.capitalize()))
    assert len(its) == 20
    return {"title": "Compare and order times", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The two hands</h2>"
        "<p>A clock has two hands. The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "Each number is <b>5 minutes</b> for the long hand, so count in 5s.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 20, size=240, ring=True) +
        "<figcaption>The red numbers show the minutes. The long hand points to the 4: 5, 10, 15, 20. "
        "The short hand is just past the 3. It is <b>20 past 3</b>.</figcaption></figure>"
        "<h2>O’clock, half past, quarter past and quarter to</h2>"
        + table(["Long hand on", "We say", "Digital"],
                [["12", "7 o’clock", "7:00"], ["3", "quarter past 7", "7:15"], ["6", "half past 7", "7:30"],
                 ["9", "quarter to 8", "7:45"]]) +
        "<h2>Past and to</h2>"
        "<p>Long hand on the <b>right-hand side</b>: say minutes <b>past</b> the hour. "
        "Long hand on the <b>left-hand side</b>: say minutes <b>to</b> the next hour. Count in 5s back to the 12.</p>"
        "<figure class='sn-fig'>" + clock_svg(8, 35, size=200) +
        "<figcaption>The long hand points to the 7. Count back to the 12: 5, 10, 15, 20, 25. "
        "The short hand is between 8 and 9, nearly at the 9. It is <b>25 to 9</b> (8:35).</figcaption></figure>"
        + ex("Read the clock", "The long hand points to the 10. The short hand is between 4 and 5.",
             "The 10 is on the left-hand side, so say “to”. Count back to the 12: 5, 10. The next hour is 5.",
             "10 to 5") +
        ex("Draw the hands", "Show 25 past 6 on a clock.",
           "Long hand: count in 5s to 25. That is the 5. Short hand: just under half way from the 6 to the 7.",
           "Long hand on the 5, short hand between 6 and 7") +
        "<h2>Time facts</h2>"
        + table(["Time", "Equals"], [["1 hour", "60 minutes"], ["half an hour", "30 minutes"],
                                    ["a quarter of an hour", "15 minutes"], ["1 day", "24 hours"]]) +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“25 to 9” read as 9:35", "25 to 9 is before 9 o’clock. The short hand has not reached 9, so it is 8:35."],
            ["Long hand on the 4 read as 4 minutes", "Each number is 5 minutes: 5, 10, 15, 20. It is 20 past."],
            ["Past and to mixed up", "Right-hand side: past. Left-hand side: to."],
            ["Quarter to 6 written as 6:45", "Quarter to 6 is 15 minutes before 6 o’clock: 5:45."],
        ])
    )


FAQ = [
    {"q": "What time should a Year 2 child be able to tell?",
     "a": "By the end of Year 2, children should tell and write the time to 5 minutes, including quarter past and quarter to, and draw the hands on a clock to show these times."},
    {"q": "How many minutes are in an hour and hours in a day?",
     "a": "There are 60 minutes in 1 hour and 24 hours in 1 day. Year 2 children are expected to know both facts."},
    {"q": "Why do children say “25 to 9” for 8:35?",
     "a": "When the long hand is on the left-hand side of the clock, we count the minutes back to the next hour. 8:35 is 25 minutes before 9 o’clock, so it is 25 to 9."},
    {"q": "How can I help my child learn to tell the time?",
     "a": "Use an analogue clock at home and ask the time at everyday moments, such as breakfast or bedtime. Practise counting in 5s round the clock, then move from o’clock and half past to quarter past, quarter to and 5-minute times."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5). Items marked 'fixed' (A-D clock pictures) keep their position."""
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
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


def gen():
    rnd = random.Random(2209)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_quarters(rnd), set_past(rnd), set_to(rnd), set_match(rnd), set_problems(rnd, people)]
    balance(sets, rnd)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
    u = {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "telling-the-time-to-5-minutes", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Telling the Time to 5 Minutes",
        "seo_title": "Year 2 Telling the Time Worksheets: O’clock, Quarter Past and 5 Minutes (Free, with Answers)",
        "short_title": "Telling the time",
        "domain": "Measurement",
        "standard_code": "Year 2: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Compare and sequence intervals of time; tell and write the time to five minutes, including quarter past/to the hour and draw the hands on a clock face to show these times; know the number of minutes in an hour and the number of hours in a day.",
        "meta_desc": "Free Year 2 maths worksheets on telling the time: o’clock, half past, quarter past and quarter to, then 5-minute times past and to the hour, minutes in an hour, hours in a day, and comparing and ordering times. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Short hand: the hour. Long hand: count in 5s for the minutes.",
        "key_sub": "Long hand on the right-hand side: minutes past. On the left-hand side: minutes to the next hour, so 25 to 9 is 8:35.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
