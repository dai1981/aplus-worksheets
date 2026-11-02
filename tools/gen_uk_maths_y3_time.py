# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Telling the Time (National Curriculum in England, Measurement)
  python3 tools/gen_uk_maths_y3_time.py
Every clock picture is drawn from the time itself (the hour hand moves between the numbers),
with Arabic numerals or Roman numerals I to XII. Every answer is worked out in code.
Wrong answers come from real pupil mistakes: hour hand read as the next hour ("25 to 9" -> 9:35),
the number the minute hand points to read as minutes, past and to mixed up, am and pm swapped,
February given 30 days, an hour counted as 100 minutes.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Oliver", "he"), ("Amelia", "she"), ("Harry", "he"), ("Isla", "she"), ("Mohammed", "he"), ("Freya", "she"),
          ("Jack", "he"), ("Poppy", "she"), ("Arjun", "he"), ("Ava", "she"), ("Noah", "he"), ("Aisha", "she"),
          ("George", "he"), ("Lily", "she"), ("Leo", "he"), ("Zara", "she"), ("Alfie", "he"), ("Grace", "she"),
          ("Kai", "he"), ("Ruby", "she"), ("Ethan", "he"), ("Maya", "she"), ("Charlie", "he"), ("Evie", "she")]
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


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


def t24(h24, m):
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
    for num, unit in re.findall(r"(\d+) (hour|minute)", s):
        v += int(num) * (60 if unit == "hour" else 1)
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


def clock_svg(h, m, size=200, roman=False):
    """Analogue clock. The hour hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) >= 12, (h, m)
    c = size / 2.0
    R = c - 6
    k = R / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (c, c, R, GREEN, 5 * k)]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (12 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (c + r1 * math.cos(a), c + r1 * math.sin(a),
                                        c + (R - 3 * k) * math.cos(a), c + (R - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), LINE, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), LINE, 2.6 * k))
    # hands first, numbers on top (white edge) so a hand never hides a number
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (c, c, c + R * 0.48 * math.cos(ah), c + R * 0.48 * math.sin(ah), LINE, 8 * k))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (c, c, c + R * 0.82 * math.cos(am), c + R * 0.82 * math.sin(am), RED, 4.5 * k))
    if roman:
        fs = 16 * k
        s.append("<g font-family='Georgia, serif' font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' paint-order='stroke'>" % (fs, LINE, 3.5 * k))
        rn = R - 30 * k
    else:
        fs = 19 * k
        s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' paint-order='stroke'>" % (fs, LINE, 3.5 * k))
        rn = R - 29 * k
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        lab = ROMAN[n] if roman else str(n)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (c + rn * math.cos(a), c + rn * math.sin(a) + fs * 0.36, lab))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (c, c, 6 * k, LINE))
    return svg_wrap(size, size, "".join(s), "clock with Roman numerals" if roman else "analogue clock")


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


def num(n, roman):
    return "%s (%d)" % (ROMAN[n], n) if roman else str(n)


def hand_text(h, m, roman=False):
    """How to read the two hands (for explanations)."""
    h = h12(h)
    n, extra = divmod(m, 5)
    if m == 0:
        mm = "The long minute hand points to <b>%s</b>, so it is exactly on the hour." % num(12, roman)
    elif extra == 0:
        mm = "The long minute hand points to <b>%s</b>. Count in 5s: %d × 5 = <b>%d minutes</b> past." % (num(n, roman), n, m)
    elif n == 0:
        mm = "The long minute hand is <b>%d small mark%s</b> past the 12: <b>%s</b> past." % (extra, "" if extra == 1 else "s", mins(m))
    else:
        mm = ("The long minute hand is %d small mark%s past the %s. Count in 5s to %d, then on in 1s: <b>%d minutes</b> past."
              % (extra, "" if extra == 1 else "s", num(n, roman), n * 5, m))
    if m == 0:
        hh = "The short hour hand points to <b>%s</b>." % num(h, roman)
    else:
        hh = ("The short hour hand is between <b>%s</b> and <b>%s</b>, so the hour is still <b>%d</b>."
              % (num(h, roman), num(h % 12 + 1, roman), h))
    return hh + " " + mm


def pick_hour(rnd, m, used, exclude=()):
    hrs = list(range(1, 13))
    rnd.shuffle(hrs)
    for h in hrs:
        if (h, m) in used or h in exclude or hands_gap(h, m) < 15:
            continue
        used.add((h, m))
        return h
    raise AssertionError(m)


# ============================================================ set 1: o'clock, half past, quarter past / to
def set_quarters(rnd):
    its = []
    used = set()
    plan = [0, 0, 30, 30, 0, 30, 15, 15, 30, 0, 15, 45, 45, 15, 45, 30, 45, 15, 45, 45]
    for i, m in enumerate(plan):
        rom = i % 3 == 1
        h = pick_hour(rnd, m, used)
        right = words(h, m)
        if m == 0:
            c = [words(12, 5 * h) if h != 12 else None, words(h, 30), words(h + 1, 0), words(h - 1, 0)]
            e = ("%s It is <b>%s</b>. (Do not read the short hand as minutes: the long hand tells the minutes.)"
                 % (hand_text(h, m, rom), right))
        elif m == 30:
            c = [words(h + 1, 30), "6 o’clock" if h != 6 else "12 o’clock", words(h, 15), words(h - 1, 30)]
            e = ("%s Half past means 30 minutes past. The hour hand has not reached %d yet, so it is <b>%s</b>, not half past %d."
                 % (hand_text(h, m, rom), h12(h + 1), right, h12(h + 1)))
        elif m == 15:
            c = [words(h, 45), words(h, 3), words(h + 1, 45), words(h - 1, 15)]
            e = ("%s 15 minutes is a quarter of an hour, and the minute hand is on the right-hand side, so we say <b>past</b>. "
                 "It is <b>%s</b>." % (hand_text(h, m, rom), right))
        else:
            c = [words(h - 1, 45), words(h + 1, 15), words(h, 9), words(h, 15)]
            e = ("%s 45 minutes past %d is 15 minutes before %d o’clock. The minute hand is on the left-hand side, so we say "
                 "<b>to</b> the next hour: <b>%s</b>." % (hand_text(h, m, rom), h12(h), h12(h + 1), right))
        q = fig(clock_svg(h, m, roman=rom)) + ("This clock has Roman numerals. " if rom else "") + "What time does the clock show?"
        its.append(mcq(q, right, c, e))
    return {"title": "O’clock, half past, quarter past and quarter to", "items": its}


# ============================================================ set 2: times to 5 minutes
def set_fives(rnd):
    its = []
    used = set()
    plan = [10, 20, 5, 25, 50, 40, 55, 35, 20, 10, 40, 25, 50, 5, 35, 55]
    for i, m in enumerate(plan):
        rom = i % 3 == 2
        h = pick_hour(rnd, m, used)
        right = words(h, m)
        n = m // 5
        if m < 30:
            c = [words(h + 1, m), words(h, n), words(h - 1, 60 - m), words(h, 60 - m), words(h, m + 5)]
            e = ("%s The minute hand is on the right-hand side, so we say <b>past %d</b>. It is <b>%s</b>."
                 % (hand_text(h, m, rom), h12(h), right))
        else:
            c = [words(h - 1, m), words(h, n), words(h + 1, 60 - m), words(h, 60 - m), words(h, m - 5)]
            e = ("%s That is %d minutes before %d o’clock (60 − %d = %d). The minute hand is on the left-hand side, so we say "
                 "<b>to %d</b>. It is <b>%s</b>." % (hand_text(h, m, rom), 60 - m, h12(h + 1), m, 60 - m, h12(h + 1), right))
        q = fig(clock_svg(h, m, roman=rom)) + ("This clock has Roman numerals. " if rom else "") + "What time does the clock show?"
        its.append(mcq(q, right, c, e))
    # digital clock to words
    for h, m in [(8, 35), (4, 20), (2, 50), (11, 40)]:
        right = words(h, m)
        if m > 30:
            c = [words(h - 1, m),                              # "25 to 8" for 8:35 (wrong hour)
                 "%d to %d" % (m, h12(h + 1)),                 # did not take away from 60
                 words(h, 60 - m),                            # "25 past 8"
                 "%d past %d" % (m, h)]
            e = ("%s is %d minutes past %d. That is more than half past, so say <b>to</b> the next hour. "
                 "60 − %d = %d minutes to %d: <b>%s</b>." % (dig(h, m), m, h, m, 60 - m, h12(h + 1), right))
        else:
            c = [words(h, 60 - m), words(h + 1, m), words(h + 1, 60 - m)]
            e = "%s is %d minutes after %d o’clock. It is less than half past, so say <b>past</b>: <b>%s</b>." % (dig(h, m), m, h, right)
        its.append(mcq(fig(digital_svg(dig(h, m))) + "The digital clock shows a time. How do we say it?", right, c, e))
    order = list(range(20))
    # 5-minute clocks first, then digital ones mixed into the second half
    order = order[:12] + [16, 12, 13, 17, 14, 18, 15, 19]
    its = [its[i] for i in order]
    return {"title": "Times to 5 minutes: past and to", "items": its}


# ============================================================ set 3: to the minute, am and pm
CONTEXTS = [
    ("{n} wakes up in the morning.", 7, 2, 28),
    ("{n} walks to school in the morning.", 8, 31, 54),
    ("{n} has lunch at school.", 12, 11, 48),
    ("School finishes in the afternoon.", 15, 16, 28),
    ("{n} has tea in the evening.", 17, 32, 56),
    ("{n} goes to bed in the evening.", 19, 6, 27),
]


def set_minute(rnd, people):
    its = []
    # vocabulary
    its.append(mcq("What does <b>noon</b> mean?", "12 o’clock in the middle of the day",
                   ["12 o’clock at night", "6 o’clock in the evening", "the start of the morning"],
                   "<b>Noon</b> is 12 o’clock in the middle of the day. <b>Midnight</b> is 12 o’clock at night."))
    its.append(mcq("What does <b>midnight</b> mean?", "12 o’clock at night",
                   ["12 o’clock in the middle of the day", "9 o’clock at night", "the end of the afternoon"],
                   "<b>Midnight</b> is 12 o’clock at night, when one day ends and the next day starts."))
    its.append(mcq("Which times are <b>am</b>?", "from midnight to noon",
                   ["from noon to midnight", "only times at night", "only times after school"],
                   "<b>am</b> times go from midnight to noon (night and morning). <b>pm</b> times go from noon to midnight "
                   "(afternoon and evening)."))
    nm, pr = next(people)
    its.append(mcq("Which time is in the <b>afternoon</b>?", "2:30 pm", ["2:30 am", "11:30 am", "9:15 am"],
                   "The afternoon is after noon, so it is a <b>pm</b> time. 2:30 am is in the middle of the night. "
                   "So the answer is <b>2:30 pm</b>."))
    its.append(mcq("Which is a sensible time for school to start?", "8:50 am", ["8:50 pm", "3:50 am", "11:50 pm"],
                   "School starts in the morning, so it is an <b>am</b> time. 3:50 am is the middle of the night. "
                   "So the answer is <b>8:50 am</b>."))
    its.append(mcq("Which time is closest to <b>midnight</b>?", "11:50 pm", ["11:50 am", "6:00 pm", "12:30 pm"],
                   "Midnight is 12 o’clock at night. 11:50 pm is 10 minutes before midnight. 11:50 am is 10 minutes "
                   "before <b>noon</b>. So the answer is <b>11:50 pm</b>."))
    assert add(11, 30, 60) == (12, 30)
    its.append(mcq("It is <b>11:30 am</b>. What time will it be <b>1 hour</b> later?", "12:30 pm",
                   ["12:30 am", "11:30 pm", "1:30 pm"],
                   "1 hour after 11:30 is 12:30. It is now after noon, so it changes to <b>pm</b>: <b>12:30 pm</b>. "
                   "(12:30 am is just after midnight.)"))
    # clocks to the minute -> 12-hour digital with am / pm
    ctx = CONTEXTS[:]
    rnd.shuffle(ctx)
    for sent, H, lo, hi in ctx:
        ms = [x for x in range(lo, hi + 1) if x % 5 and hands_gap(H, x) >= 15]
        m = rnd.choice(ms)
        n = m // 5
        nm, pr = next(people)
        right = tm12(H, m)
        c = [tm12(H + 12, m)]                             # am and pm mixed up
        if m >= 35:
            c.append(tm12(H + 1, m))                      # hour hand read as the next hour
        if n and n != m:
            c.append(tm12(H, n))                          # minute number read as minutes
        c += [tm12(H + 1, m), tm12(H, m + 5 if m < 55 else m - 5)]
        ap = "am" if H < 12 else "pm"
        why = ("It is the morning, so it is <b>am</b>." if ap == "am" else
               "It is after noon, so it is <b>pm</b>.")
        e = "%s %s So it is <b>%s</b>." % (hand_text(H, m), why, right)
        q = fig(clock_svg(H, m)) + sent.format(n=nm) + " What is the time?"
        its.append(mcq(q, right, c, e))
    # words -> digital
    for H, m, part in [(10, 20, "in the morning"), (8, 35, "in the morning"), (16, 40, "in the afternoon"), (19, 55, "in the evening")]:
        w = words(H, m)
        right = tm12(H, m)
        if m > 30:
            c = [tm12(H + 1, m), tm12(H + 1, 60 - m), tm12(H, 60 - m), tm12(H + 12, m)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d minutes past %d: %s. "
                 "It is %s, so it is %s: <b>%s</b>. (Not %s: that is after %d o’clock.)"
                 % (w, 60 - m, h12(H + 1), 60 - m, m, m, h12(H), dig(H, m), part, "am" if H < 12 else "pm", right,
                    tm12(H + 1, m), h12(H + 1)))
        else:
            c = [tm12(H - 1, 60 - m), tm12(H + 12, m), tm12(H, m // 5), tm12(H + 1, m)]
            e = ("“%s” means %d minutes <b>after</b> %d o’clock: %s. It is %s, so it is %s: <b>%s</b>."
                 % (w, m, h12(H), dig(H, m), part, "am" if H < 12 else "pm", right))
        its.append(mcq("Write <b>%s %s</b> as a digital time." % (w, part), right, c, e))
    # light 24-hour
    its.append(mcq("On a 24-hour clock, what is <b>3 pm</b>?", "15:00", ["03:00", "13:00", "16:00"],
                   "pm times are after noon. Add 12 to the hour: 3 + 12 = 15. So 3 pm is <b>15:00</b>."))
    its.append(mcq("A 24-hour clock shows <b>18:30</b>. What is this in 12-hour time?", "6:30 pm",
                   ["8:30 pm", "6:30 am", "8:30 am"],
                   "Take away 12 from the hour: 18 − 12 = 6. It is in the evening, so it is <b>6:30 pm</b>. "
                   "(Do not just drop the 1: 18:30 is not 8:30.)"))
    its.append(mcq("How is <b>midnight</b> shown on a 24-hour clock?", "00:00", ["24:00", "12:00", "00:12"],
                   "On a 24-hour clock a new day starts at midnight, so midnight is <b>00:00</b>. 12:00 is noon."))
    assert len(its) == 20, len(its)
    return {"title": "To the minute: am, pm, noon and midnight", "items": its}


# ============================================================ set 4: time facts
def set_facts(rnd):
    its = []
    F = [("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "30"], "There are <b>60 seconds</b> in 1 minute."),
         ("How many <b>minutes</b> are in 1 hour?", "60", ["100", "24", "30"],
          "There are <b>60 minutes</b> in 1 hour. (Not 100: time does not count in hundreds.)"),
         ("How many <b>hours</b> are in 1 day?", "24", ["12", "60", "7"],
          "There are <b>24 hours</b> in 1 day: 12 am hours and 12 pm hours. 12 + 12 = 24."),
         ("How many <b>days</b> are in 1 week?", "7", ["5", "12", "10"],
          "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: <b>7 days</b>. (5 is just the school days.)"),
         ("How many <b>months</b> are in 1 year?", "12", ["10", "52", "7"],
          "January to December: <b>12 months</b>. (52 is the number of weeks.)"),
         ("How many days are in a year that is <b>not</b> a leap year?", "365", ["366", "360", "52"],
          "A normal year has <b>365 days</b>. A leap year has 1 more: 366."),
         ("How many days are in a <b>leap year</b>?", "366", ["365", "364", "360"],
          "A leap year has 1 extra day, 29 February. 365 + 1 = <b>366 days</b>."),
         ("How many days does <b>February</b> have in a normal year?", "28", ["30", "29", "31"],
          "February is the shortest month. It has <b>28 days</b>, and 29 days in a leap year. It never has 30."),
         ("In a <b>leap year</b>, how many days does February have?", "29", ["28", "30", "31"],
          "In a leap year February gets 1 extra day: 28 + 1 = <b>29 days</b>."),
         ]
    for q, a, c, e in F:
        its.append(mcq(q, a, c, e))
    rhyme = "Remember: “30 days has September, April, June and November. All the rest have 31, except February.”"
    for mo, d in [("September", 30), ("July", 31), ("April", 30)]:
        its.append(mcq("How many days are in <b>%s</b>?" % mo, str(d), [str(61 - d), "28", "29"],
                       "%s So %s has <b>%d days</b>." % (rhyme, mo, d)))
    its.append(mcq("Which month has <b>31 days</b>?", "August", ["June", "September", "November"],
                   "%s June, September and November have 30 days. <b>August</b> has 31." % rhyme))
    its.append(mcq("How many minutes are in <b>half an hour</b>?", "30", ["50", "15", "20"],
                   "1 hour = 60 minutes. Half of 60 is <b>30 minutes</b>. (Not 50: an hour is not 100 minutes.)"))
    its.append(mcq("How many minutes are in <b>a quarter of an hour</b>?", "15", ["25", "30", "4"],
                   "1 hour = 60 minutes. A quarter of 60 is 60 ÷ 4 = <b>15 minutes</b>. (25 would be a quarter of 100.)"))
    its.append(mcq("<b>1 minute 30 seconds</b> = ? seconds", "90", ["130", "31", "60"],
                   "1 minute = 60 seconds. 60 + 30 = <b>90 seconds</b>. (Not 130: a minute is 60 seconds, not 100.)"))
    its.append(mcq("Which is the <b>longest</b> time?", "2 minutes", ["100 seconds", "90 seconds", "1 minute"],
                   "Change them all to seconds. 2 minutes = 60 + 60 = 120 seconds. 120 is more than 100 and 90. "
                   "So <b>2 minutes</b> is the longest."))
    its.append(mcq("Which is the <b>shortest</b> time?", "50 seconds", ["1 minute", "70 seconds", "1 hour"],
                   "1 minute = 60 seconds. 50 seconds is less than 60 seconds, 70 seconds and 1 hour. "
                   "So <b>50 seconds</b> is the shortest."))
    its.append(mcq("About how long does it take to brush your teeth?", "2 minutes", ["2 seconds", "2 hours", "2 days"],
                   "2 seconds is far too quick, and 2 hours is far too long. Brushing your teeth takes about <b>2 minutes</b>."))
    its.append(mcq("About how long does a Year 3 child sleep at night?", "10 hours", ["10 minutes", "10 seconds", "10 days"],
                   "Children sleep from the evening until the morning. That is about <b>10 hours</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Time facts: seconds, minutes, days and months", "items": its}


# ============================================================ set 5: how long? time problems
def set_problems(rnd, people):
    its = []

    def how_long(text, h1, m1, h2, m2, line=False):
        d = (h2 * 60 + m2) - (h1 * 60 + m1)
        assert 0 < d < 60 or (h2 != h1)
        q = (fig(timeline_svg(h1, m1, h2, m2)) if line else "") + text
        if h1 == h2:
            c = [mins(m2), mins(d + 10), mins(d - 5) if d > 5 else None, mins(d + 5), mins(m1 + m2) if m1 + m2 != d else None]
            e = "Both times are in the same hour. %d − %d = <b>%s</b>." % (m2, m1, mins(d))
        else:
            naive = (h12(h2) * 100 + m2) - (h12(h1) * 100 + m1)
            c = ["%d minutes" % naive if 0 < naive < 100 and naive != d else None, mins(abs(m2 - m1)) if m2 != m1 else None,
                 dur(d + 60) if d < 60 else dur(d - 60), dur(d + 10), dur(d - 5)]
            e = ("Count on to the next o’clock first: %s to %s is %s. Then %s to %s is %s. %d + %d = <b>%s</b>. "
                 "(An hour has 60 minutes, not 100, so do not just take away the numbers.)"
                 % (tm12(h1, m1), tm12(h1 + 1, 0), mins(60 - m1), tm12(h1 + 1, 0), tm12(h2, m2),
                    dur(d - (60 - m1)), 60 - m1, d - (60 - m1),
                    mins(d) if d < 60 else "%d minutes = %s" % (d, dur(d))))
        return mcq(q, dur(d), c, e, key=dur_value)

    its.append(how_long("A TV programme starts at <b>4:10 pm</b> and ends at <b>4:35 pm</b>. How long is it?", 16, 10, 16, 35))
    nm, pr = next(people)
    its.append(how_long("%s starts reading at <b>7:05 pm</b> and stops at <b>7:45 pm</b>. How long does %s read for?"
                        % (nm, pr), 19, 5, 19, 45))
    its.append(how_long("Morning break starts at <b>10:30 am</b> and ends at <b>10:45 am</b>. How long is break?", 10, 30, 10, 45))
    nm, pr = next(people)
    its.append(how_long("%s’s piano lesson is from <b>5:20 pm</b> to <b>5:50 pm</b>. How long is the lesson?" % nm, 17, 20, 17, 50))
    its.append(how_long("Assembly starts at <b>9:05 am</b> and ends at <b>9:27 am</b>. How long is assembly?", 9, 5, 9, 27))
    its.append(how_long("A football match starts at <b>2:45 pm</b> and ends at <b>3:30 pm</b>. How long is the match?",
                        14, 45, 15, 30, line=True))
    nm, pr = next(people)
    its.append(how_long("%s gets on the school bus at <b>8:40 am</b>. %s gets to school at <b>9:05 am</b>. How long is the bus ride?"
                        % (nm, pr.capitalize()), 8, 40, 9, 5))
    nm, pr = next(people)
    its.append(how_long("%s’s swimming lesson is from <b>3:50 pm</b> to <b>4:35 pm</b>. How long is it?" % nm,
                        15, 50, 16, 35, line=True))
    its.append(how_long("A cake goes in the oven at <b>11:48 am</b>. It comes out at <b>12:13 pm</b>. How long does it bake?",
                        11, 48, 12, 13))
    its.append(how_long("A film starts at <b>5:50 pm</b> and ends at <b>7:20 pm</b>. How long is the film?", 17, 50, 19, 20))
    # end times
    its.append(mcq("A TV programme starts at <b>6:15 pm</b>. It lasts <b>25 minutes</b>. What time does it end?", "6:40 pm",
                   ["6:40 am", "7:40 pm", "6:45 pm"],
                   "Count on 25 minutes from 6:15: 15 + 25 = 40. It is still the evening, so it ends at <b>6:40 pm</b>."))
    its.append(mcq("Lunchtime starts at <b>12:10 pm</b>. It lasts <b>50 minutes</b>. What time does it end?", "1:00 pm",
                   ["12:00 pm", "1:00 am", "1:10 pm"],
                   "12:10 + 50 minutes: 10 + 50 = 60 minutes, which is a new hour. So it ends at <b>1:00 pm</b>."))
    assert add(12, 10, 50) == (13, 0) and add(18, 15, 25) == (18, 40)
    nm, pr = next(people)
    assert add(19, 30, -20) == (19, 10)
    its.append(mcq("%s goes to bed at <b>7:30 pm</b>. %s has a bath <b>20 minutes</b> before bed. What time does the bath start?"
                   % (nm, pr.capitalize()), "7:10 pm", ["7:50 pm", "7:10 am", "7:20 pm"],
                   "Count <b>back</b> 20 minutes from 7:30: 30 − 20 = 10. The bath starts at <b>7:10 pm</b>. "
                   "(7:50 pm is 20 minutes <b>after</b> bedtime.)"))
    assert add(17, 40, 95) == (19, 15)
    its.append(mcq("A film starts at <b>5:40 pm</b>. It lasts <b>1 hour 35 minutes</b>. What time does it end?", "7:15 pm",
                   ["6:15 pm", "7:15 am", "7:05 pm"],
                   "Add 1 hour: 5:40 pm → 6:40 pm. Then add 35 minutes: 20 minutes takes you to 7:00 pm, and 15 more makes "
                   "<b>7:15 pm</b>."))
    # school day
    assert (15 * 60 + 20) - (8 * 60 + 50) == 390
    its.append(mcq("School starts at <b>8:50 am</b> and ends at <b>3:20 pm</b>. How long is the school day?", "6 hours 30 minutes",
                   ["5 hours 30 minutes", "7 hours 30 minutes", "6 hours"],
                   "8:50 am to 2:50 pm is 6 hours. 2:50 pm to 3:20 pm is 30 minutes. So the school day is <b>6 hours 30 minutes</b>.",
                   key=dur_value))
    # compare durations
    a, b = next(people), next(people)
    its.append(mcq("%s’s film lasts <b>1 hour 30 minutes</b>. %s’s film lasts <b>95 minutes</b>. Whose film is longer, and by how much?"
                   % (a[0], b[0]), "%s’s, by 5 minutes" % b[0],
                   ["%s’s, by 5 minutes" % a[0], "%s’s, by 35 minutes" % a[0], "%s’s, by 65 minutes" % b[0]],
                   "1 hour 30 minutes = 60 + 30 = 90 minutes. 95 − 90 = 5. So <b>%s’s</b> film is longer, by <b>5 minutes</b>." % b[0]))
    a, b = next(people), next(people)
    assert 65 - 58 == 7
    its.append(mcq("%s runs a race in <b>58 seconds</b>. %s takes <b>1 minute 5 seconds</b>. How much faster is %s?"
                   % (a[0], b[0], a[0]), "7 seconds", ["47 seconds", "53 seconds", "1 minute 7 seconds"],
                   "1 minute 5 seconds = 60 + 5 = 65 seconds. 65 − 58 = <b>7 seconds</b>. "
                   "(Not 47: a minute is 60 seconds, not 100.)"))
    nm, pr = next(people)
    its.append(mcq("%s practises the recorder for <b>15 minutes</b> a day for <b>4 days</b>. How long is that in total?" % nm,
                   "1 hour", ["19 minutes", "45 minutes", "1 hour 15 minutes"],
                   "4 × 15 = 60 minutes. 60 minutes = <b>1 hour</b>.", key=dur_value))
    its.append(mcq("Today is <b>27 April</b>. The school trip is in <b>5 days</b>. What is the date of the trip?", "2 May",
                   ["32 April", "1 May", "3 May"],
                   "April has 30 days. Count on: 28, 29, 30 April, then 1 May, 2 May. The trip is on <b>2 May</b>."))
    its.append(mcq("How many days are there in <b>June and July</b> together?", "61", ["62", "60", "59"],
                   "June has 30 days and July has 31 days. 30 + 31 = <b>61 days</b>."))
    assert len(its) == 20, len(its)
    return {"title": "How long? Time problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The two hands</h2>"
        "<p>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "Each number on the clock is <b>5 minutes</b> for the long hand, so count in 5s.</p>"
        "<figure class='sn-fig'>" + clock_svg(8, 35, size=230) +
        "<figcaption>The long hand points to 7: 7 × 5 = 35 minutes past 8. The short hand is between 8 and 9, "
        "so the hour is still 8. It is <b>25 to 9</b> (8:35).</figcaption></figure>"
        "<h2>Past and to</h2>"
        "<p>When the long hand is on the right-hand side, say minutes <b>past</b> the hour. "
        "When it is on the left-hand side, say minutes <b>to</b> the next hour.</p>"
        + table(["Digital", "We say"], [["4:00", "4 o’clock"], ["4:15", "quarter past 4"], ["4:20", "20 past 4"],
                                        ["4:30", "half past 4"], ["4:35", "25 to 5"], ["4:45", "quarter to 5"],
                                        ["4:50", "10 to 5"]]) +
        "<h2>To the nearest minute</h2>"
        "<p>Between two numbers there are 5 small marks, one for each minute. Count in 5s to the last number, then on in 1s.</p>"
        + ex("Read to the minute", "The long hand is 3 small marks past the 4. The short hand is between 6 and 7.",
             "Count in 5s to the 4: 5, 10, 15, 20. Then 21, 22, 23.", "23 minutes past 6 (6:23)") +
        "<h2>Roman numeral clocks</h2>"
        "<p>Some clocks use Roman numerals. Read them in the same way.</p>"
        "<figure class='sn-fig'>" + clock_svg(10, 10, size=230, roman=True) +
        "<figcaption>The long hand points to II (2): 2 × 5 = 10 minutes past. The short hand is just past X (10). "
        "It is <b>10 past 10</b> (10:10).</figcaption></figure>"
        + table(["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"],
                [[str(n) for n in range(1, 13)]]) +
        "<h2>am, pm, noon and midnight</h2>"
        "<p><b>am</b> is from midnight to noon (night and morning). <b>pm</b> is from noon to midnight (afternoon and evening). "
        "<b>Noon</b> is 12 o’clock in the day. <b>Midnight</b> is 12 o’clock at night.</p>"
        + ex("am or pm?", "Isla eats breakfast at 25 to 8. Write the time.",
             "25 to 8 is 35 minutes past 7. Breakfast is in the morning, so it is am.", "7:35 am") +
        "<h2>Time facts</h2>"
        + table(["Unit", "Equals"], [["1 minute", "60 seconds"], ["1 hour", "60 minutes"], ["1 day", "24 hours"],
                               ["1 week", "7 days"], ["1 year", "12 months, 365 days"], ["1 leap year", "366 days (29 February)"]]) +
        "<p>“30 days has September, April, June and November. All the rest have 31, except February.” "
        "February has 28 days, or 29 in a leap year.</p>"
        "<h2>How long? Count on</h2>"
        "<p>An hour has 60 minutes, not 100. Jump to the next o’clock first, then on to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(15, 45, 16, 20) +
        "<figcaption>3:45 pm to 4:00 pm is 15 minutes. 4:00 pm to 4:20 pm is 20 minutes. 15 + 20 = 35 minutes.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“25 to 9” written as 9:35", "25 to 9 is before 9 o’clock: 60 − 25 = 35, so 8:35"],
            ["Long hand on 4 read as 4 minutes", "Each number is 5 minutes: 4 × 5 = 20 minutes"],
            ["Half past 3 read as half past 4", "The short hand has not reached 4 yet, so the hour is still 3"],
            ["Breakfast at 7:30 pm", "Morning times are am: 7:30 am"],
            ["February has 30 days", "February has 28 days, or 29 in a leap year"],
            ["3:45 to 4:20 worked out as 420 − 345 = 75 minutes", "Count on: 15 + 20 = 35 minutes"],
        ])
    )


FAQ = [
    {"q": "What time should a Year 3 child be able to tell?",
     "a": "By the end of Year 3, children should tell the time to the nearest minute on an analogue clock, including clocks with Roman numerals, and write it as a 12-hour time with am or pm."},
    {"q": "What is the difference between am and pm?",
     "a": "am times are from midnight to noon (night and morning). pm times are from noon to midnight (afternoon and evening). So breakfast is usually am and tea is pm."},
    {"q": "How many days are in each month?",
     "a": "April, June, September and November have 30 days. February has 28 days, or 29 in a leap year. All the other months have 31 days."},
    {"q": "How can I help my child learn to tell the time?",
     "a": "Use a real analogue clock at home and ask the time at everyday moments, such as breakfast or bedtime. Start with o’clock and half past, then quarter past and quarter to, then count in 5s for the other times."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
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
    rnd = random.Random(3311)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_quarters(rnd), set_fives(rnd), set_minute(rnd, people), set_facts(rnd), set_problems(rnd, people)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    u = {
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "telling-the-time", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Telling the Time",
        "seo_title": "Year 3 Telling the Time Worksheets: Clocks to the Minute, am and pm (Free, with Answers)",
        "short_title": "Telling the time",
        "domain": "Measurement",
        "standard_code": "Year 3: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Tell and write the time from an analogue clock, including using Roman numerals from I to XII, and 12-hour and 24-hour clocks; estimate and read time with increasing accuracy to the nearest minute; record and compare time in terms of seconds, minutes and hours; use vocabulary such as o’clock, a.m./p.m., morning, afternoon, noon and midnight; know the number of seconds in a minute and the number of days in each month, year and leap year; compare durations of events.",
        "meta_desc": "Free Year 3 maths worksheets on telling the time: o’clock, half past, quarter past and quarter to, times to 5 minutes and to the minute, Roman numeral clocks, am and pm, days in each month, leap years and how long events last. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Short hand: the hour. Long hand: count in 5s for the minutes.",
        "key_sub": "Right-hand side: minutes past. Left-hand side: minutes to the next hour, so 25 to 9 is 8:35. am is before noon, pm is after noon.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "time line")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
