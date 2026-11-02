# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Telling the Time to the Quarter Hour (Australian Curriculum v9.0, AC9M2M04)
  python3 tools/gen_au_maths_y2_time.py
Every analog clock is drawn from the time itself (the short hand moves between the numbers).
Every answer is worked out in code. Wrong answers come from real student mistakes:
the two hands swapped, the short hand read as the next number (half past 3 read as half past 4),
quarter to 4 read as 4:15 or written as 4:45, past and to mixed up, the number 3 read as 3 minutes (3:03).
HTML attributes use single quotes (no backslashes in the JSON). Australian English ("analog", "mum").
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
GRAY = "#9aa3a0"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Charlotte", "she"), ("Oliver", "he"), ("Isla", "she"), ("Jack", "he"), ("Mia", "she"), ("Noah", "he"),
          ("Amelia", "she"), ("William", "he"), ("Ava", "she"), ("Leo", "he"), ("Harper", "she"), ("Lachlan", "he"),
          ("Chloe", "she"), ("Liam", "he"), ("Ruby", "she"), ("Aarav", "he"), ("Mei", "she"), ("Kai", "he"),
          ("Zara", "she"), ("Cooper", "he"), ("Matilda", "she"), ("Ethan", "he"), ("Sienna", "she"), ("Grace", "she")]


# ------------------------------------------------------------ time words
def h12(h):
    return (h - 1) % 12 + 1


def nxt(h):
    return h12(h + 1)


def prv(h):
    return h12(h - 1)


def words(h, m):
    """o’clock, quarter past, half past, quarter to"""
    h = h12(h)
    assert m in (0, 15, 30, 45)
    return {0: "%d o’clock" % h, 15: "quarter past %d" % h, 30: "half past %d" % h,
            45: "quarter to %d" % nxt(h)}[m]


def dig(h, m):
    return "%d:%02d" % (h12(h), m)


def tmin(h, m):
    return (h % 12) * 60 + m


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def cap(s):
    return s[0].upper() + s[1:]


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


def clock_body(h, m, cx, cy, R):
    """Analog clock face. The short hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) > 16, (h, m)
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
    rn = R - 13 * k - fs * 0.75
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, LINE, max(3.5 * k, 2.5)))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200):
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6), "analog clock")


def clocks4_svg(times):
    """2 x 2 grid of clocks labelled A to D (a square picture)."""
    CELL = 150
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY)]
    for i, (h, m) in enumerate(times):
        x0, y0 = (i % 2) * CELL, (i // 2) * CELL
        el.append(clock_body(h, m, x0 + 80, y0 + 77, 66))
        el.append("<text x='%d' y='%d' font-size='20' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, y0 + 22, GREEN, "ABCD"[i]))
    return svg_wrap(W, H, "".join(el), "four analog clocks")


def digital_svg(text):
    W, H = 200, 84
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='#fff' stroke='%s' stroke-width='4'/>" % (W - 6, H - 6, GREEN),
         "<rect x='16' y='14' width='%d' height='%d' rx='6' fill='#eef5f0'/>" % (W - 32, H - 28),
         "<text x='%d' y='%d' font-size='40' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Consolas, Menlo, monospace'>%s</text>" % (W / 2, H / 2 + 14, LINE, text)]
    return svg_wrap(W, H, "".join(s), "digital clock")


def quarters_svg(h):
    """Lesson: four clocks in a row, h o’clock to quarter to h+1, with words underneath."""
    S, gap = 140, 14
    W = 4 * S + 3 * gap
    el = []
    for i, m in enumerate([0, 15, 30, 45]):
        x = i * (S + gap)
        el.append(clock_body(h, m, x + S / 2.0, S / 2.0, S / 2.0 - 6))
        el.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (x + S / 2.0, S + 22, LINE, words(h, m)))
        el.append("<text x='%.1f' y='%d' font-size='16' fill='%s' text-anchor='middle'>%s</text>"
                  % (x + S / 2.0, S + 44, RED, dig(h, m)))
    return svg_wrap(W, S + 52, "".join(el), "four clocks in a row")


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
    if m == 0:
        return "The long hand points to the <b>12</b>. The short hand points to the <b>%d</b>." % h
    if m == 30:
        return ("The long hand points to the <b>6</b>: half way round. The short hand is half way between "
                "%d and %d, so the hour is still <b>%d</b>." % (h, nxt(h), h))
    if m == 15:
        return ("The long hand points to the <b>3</b>: a quarter of the way round. "
                "The short hand is just past the <b>%d</b>." % h)
    return ("The long hand points to the <b>9</b>: a quarter of an hour before the 12. "
            "The short hand is nearly at the <b>%d</b>, but not there yet." % nxt(h))


def which_clock(h, m, others, pos, note, digital=False):
    times = list(others)
    times.insert(pos, (h, m))
    L = "ABCD"[pos]
    shown = "%s, which is %s" % (words(h, m), dig(h, m)) if digital else words(h, m)
    e = "%s So clock <b>%s</b> shows %s. %s" % (hand_text(h, m), L, shown, note(times))
    return {"q": fig(clocks4_svg(times)) + "Which clock shows <b>%s</b>?" % (dig(h, m) if digital else words(h, m)),
            "c": ["A", "B", "C", "D"], "a": pos, "e": e.strip(), "fixed": True}


def letter(times, t):
    return "ABCD"[times.index(t)]


def interleave(a, b):
    """Spread the b items through a, keeping both orders."""
    out = []
    step = len(a) / float(len(b) + 1)
    j = 0
    for i, x in enumerate(a):
        out.append(x)
        while j < len(b) and i + 1 >= step * (j + 1):
            out.append(b[j])
            j += 1
    out += b[j:]
    return out


# ============================================================ set 1: o'clock
def set_oclock(rnd):
    reads = []
    hrs = list(range(1, 12))
    rnd.shuffle(hrs)
    for h in hrs:
        right = words(h, 0)
        c = ["12 o’clock", words(nxt(h), 0), words(prv(h), 0), words(h, 30)]
        e = ("%s It is <b>%s</b>. (Not 12 o’clock: the long hand on the 12 only tells us it is o’clock. "
             "The short hand tells the hour.)" % (hand_text(h, 0), right))
        reads.append(mcq(fig(clock_svg(h, 0)) + "What time does the clock show?", right, c, e))
    other = [
        which_clock(7, 0, [(12, 35), (8, 0), (7, 30)], 2,
                    lambda t: "(Clock %s has the hands swapped: its short hand is near the 12 and its long hand is on the 7.)"
                    % letter(t, (12, 35))),
        mcq("At <b>4 o’clock</b>, where does the long hand point?", "the 12", ["the 4", "the 6", "the 3"],
            "At every o’clock time the long hand points straight up to the <b>12</b>. The short hand points to the 4."),
        which_clock(2, 0, [(12, 10), (3, 0), (2, 30)], 0,
                    lambda t: "(Clock %s has the hands swapped: its long hand is on the 2.)" % letter(t, (12, 10))),
        mcq("At <b>9 o’clock</b>, where does the short hand point?", "the 9", ["the 12", "the 3", "between 9 and 10"],
            "The short hand shows the hour. At 9 o’clock it points right at the <b>9</b>. The long hand points to the 12."),
        mcq(fig(digital_svg("5:00")) + "What time is this?", "5 o’clock", ["half past 5", "6 o’clock", "4 o’clock"],
            "On a digital clock the number before the colon is the hour: 5. The <b>00</b> means 0 minutes past. "
            "It is <b>5 o’clock</b>."),
        mcq("Which digital time is <b>8 o’clock</b>?", "8:00", ["8:12", "12:08", "8:30"],
            "8 o’clock is 8 hours and 0 minutes. On a digital clock it is <b>8:00</b>. "
            "(Not 8:12: the long hand on the 12 means 0 minutes, not 12 minutes.)"),
        mcq("The short hand points to the <b>6</b>. The long hand points to the <b>12</b>. What time is it?", "6 o’clock",
            ["12 o’clock", "half past 6", "7 o’clock"],
            "The short hand tells the hour: 6. The long hand on the 12 means o’clock. It is <b>6 o’clock</b>. "
            "(12 o’clock mixes up the hands.)"),
        which_clock(10, 0, [(11, 0), (12, 50), (10, 30)], 3,
                    lambda t: "(Clock %s has the hands swapped: its long hand is on the 10.)" % letter(t, (12, 50))),
        mcq("The long hand goes all the way round once. How long is that?", "1 hour",
            ["1 minute", "12 minutes", "1 day"],
            "When the long hand goes all the way round, the short hand moves from one number to the next. "
            "From 3 o’clock to 4 o’clock is <b>1 hour</b>."),
    ]
    its = reads[:4] + interleave(reads[4:], other)
    assert len(its) == 20
    return {"title": "O’clock", "items": its}


# ============================================================ set 2: half past
def set_half(rnd):
    reads = []
    hrs = [x for x in range(1, 13) if hands_gap(x, 30) > 16]
    assert len(hrs) == 10
    rnd.shuffle(hrs)
    for h in hrs:
        right = words(h, 30)
        c = [words(nxt(h), 30), "6 o’clock", words(h, 0), words(prv(h), 30)]
        e = ("%s It is <b>%s</b>. (Not %s: the short hand has not reached the %d yet.)"
             % (hand_text(h, 30), right, words(nxt(h), 30), nxt(h)))
        reads.append(mcq(fig(clock_svg(h, 30)) + "What time does the clock show?", right, c, e))
    other = [
        mcq("At <b>half past 4</b>, where does the long hand point?", "the 6", ["the 4", "the 12", "the 3"],
            "Half past means the long hand has gone <b>half way</b> round, from the 12 to the <b>6</b>."),
        mcq("At <b>half past 8</b>, where is the short hand?", "between 8 and 9",
            ["on the 8", "on the 9", "between 7 and 8"],
            "In half an hour the short hand moves half way to the next number. At half past 8 it is "
            "<b>between 8 and 9</b>."),
        which_clock(2, 30, [(3, 30), (6, 10), (2, 0)], 1,
                    lambda t: "(Clock %s shows half past 3: its short hand is past the 3. Clock %s has the hands swapped.)"
                    % (letter(t, (3, 30)), letter(t, (6, 10)))),
        mcq(fig(digital_svg("3:30")) + "What time is this?", "half past 3", ["half past 4", "half past 2", "3 o’clock"],
            "The hour is 3 and the minutes are 30. 30 minutes is half an hour. It is <b>half past 3</b>. "
            "(Not half past 4: it is not 4 o’clock yet.)"),
        mcq("Which digital time is <b>half past 10</b>?", "10:30", ["11:30", "10:06", "10:00"],
            "Half past 10 is 30 minutes after 10 o’clock. On a digital clock it is <b>10:30</b>. "
            "(Not 10:06: the long hand on the 6 means 30 minutes.)"),
        mcq("How many minutes are in <b>half an hour</b>?", "30", ["50", "60", "6"],
            "1 hour is 60 minutes. Half of 60 is <b>30</b>."),
        mcq("The long hand moves from the 12 to the 6. How long is that?", "half an hour",
            ["6 minutes", "1 hour", "a quarter of an hour"],
            "The long hand goes half way round the clock. That is <b>half an hour</b> (30 minutes)."),
        which_clock(9, 30, [(10, 30), (9, 0), (6, 45)], 3,
                    lambda t: "(Clock %s shows half past 10. Clock %s has the hands swapped.)"
                    % (letter(t, (10, 30)), letter(t, (6, 45)))),
        mcq("Half past 11 is half an hour after which time?", "11 o’clock", ["12 o’clock", "6 o’clock", "10 o’clock"],
            "Half past 11 is 30 minutes <b>after 11 o’clock</b>. It comes before 12 o’clock."),
        mcq("Half past 7 is how many minutes after 7 o’clock?", "30 minutes", ["6 minutes", "60 minutes", "15 minutes"],
            "Half an hour is <b>30 minutes</b>. (6 is the number the long hand points to, not the minutes.)"),
    ]
    its = reads[:4] + interleave(reads[4:], other)
    assert len(its) == 20
    return {"title": "Half past", "items": its}


# ============================================================ set 3: quarter past and quarter to
def set_quarter(rnd):
    qp = [x for x in range(1, 13) if hands_gap(x, 15) > 16]
    qt = [x for x in range(1, 13) if hands_gap(x, 45) > 16]
    rnd.shuffle(qp)
    rnd.shuffle(qt)
    reads = []
    for i in range(6):
        h = qp[i]
        right = words(h, 15)
        c = ["quarter to %d" % h, words(nxt(h), 15), words(h, 30), words(h, 0)]
        e = ("%s It is <b>%s</b>. (Quarter to is when the long hand is on the 9.)" % (hand_text(h, 15), right))
        reads.append(mcq(fig(clock_svg(h, 15)) + "What time does the clock show?", right, c, e))
        h = qt[i]
        right = words(h, 45)
        c = ["quarter past %d" % nxt(h), "quarter to %d" % h, "quarter past %d" % h, words(h, 30)]
        e = ("%s It is <b>%s</b>. (Not quarter to %d: the short hand has passed the %d, so the next hour is %d.)"
             % (hand_text(h, 45), right, h, h, nxt(h)))
        reads.append(mcq(fig(clock_svg(h, 45)) + "What time does the clock show?", right, c, e))
    other = [
        mcq("At <b>quarter past</b>, where does the long hand point?", "the 3", ["the 9", "the 6", "the 12"],
            "Quarter past means the long hand has gone a quarter of the way round, from the 12 to the <b>3</b>. "
            "(The 9 is for quarter to.)"),
        mcq("At <b>quarter to</b>, where does the long hand point?", "the 9", ["the 3", "the 6", "the 4"],
            "Quarter to means a quarter of an hour <b>before</b> the 12. The long hand points to the <b>9</b>. "
            "(The 3 is for quarter past.)"),
        mcq("Quarter past 5 is how many minutes after 5 o’clock?", "15", ["3", "45", "30"],
            "A quarter of an hour is <b>15 minutes</b>. Count in 5s from the 12 to the 3: 5, 10, 15. "
            "(3 is the number, not the minutes.)"),
        which_clock(3, 45, [(4, 15), (4, 45), (9, 20)], 1,
                    lambda t: "(Clock %s shows quarter past 4, not quarter to 4. Clock %s has the hands swapped.)"
                    % (letter(t, (4, 15)), letter(t, (9, 20)))),
        mcq("Quarter to 6 is how many minutes before 6 o’clock?", "15", ["45", "9", "30"],
            "Quarter to 6 is a quarter of an hour before 6 o’clock. That is <b>15 minutes</b>. "
            "Count in 5s back from the 12 to the 9: 5, 10, 15."),
        mcq("At <b>quarter to 4</b>, where is the short hand?", "between 3 and 4",
            ["between 4 and 5", "on the 4", "on the 9"],
            "Quarter to 4 is before 4 o’clock. The short hand is nearly at the 4, but not there yet. "
            "It is <b>between 3 and 4</b>."),
        which_clock(7, 15, [(7, 45), (8, 15), (3, 35)], 2,
                    lambda t: "(Clock %s shows quarter to 8. Clock %s has the hands swapped.)"
                    % (letter(t, (7, 45)), letter(t, (3, 35)))),
        mcq("How many minutes are in <b>a quarter of an hour</b>?", "15", ["25", "4", "30"],
            "1 hour is 60 minutes. A quarter of 60 is <b>15</b>. The long hand goes from the 12 to the 3: 5, 10, 15."),
    ]
    its = reads[:4] + interleave(reads[4:], other)
    assert len(its) == 20
    return {"title": "Quarter past and quarter to", "items": its}


# ============================================================ set 4: analog and digital
def set_match(rnd):
    an = []
    for h, m in [(5, 0), (10, 30), (7, 15), (1, 45), (2, 30), (11, 15), (9, 45), (11, 45)]:
        right = dig(h, m)
        if m == 0:
            c = ["%d:12" % h, "12:%02d" % (5 * h), dig(nxt(h), 0)]
            why = "(Not %d:12: the long hand on the 12 means 0 minutes.)" % h
        elif m == 30:
            c = [dig(nxt(h), 30), "%d:06" % h, "6:%02d" % (5 * h)]
            why = "(Not %d:06: the long hand on the 6 means 30 minutes.)" % h
        elif m == 15:
            c = ["%d:03" % h, dig(h, 45), dig(nxt(h), 15)]
            why = "(Not %d:03: the long hand on the 3 means 15 minutes.)" % h
        else:
            c = [dig(nxt(h), 45), dig(nxt(h), 15), "%d:09" % h]
            why = ("(Not %s: quarter to %d is still in the %d o’clock hour.)" % (dig(nxt(h), 45), nxt(h), h))
        e = "%s It is %s. On a digital clock that is <b>%s</b>. %s" % (hand_text(h, m), words(h, m), right, why)
        an.append(mcq(fig(clock_svg(h, m)) + "Which digital time does the clock show?", right, c, e))

    dw = [
        mcq(fig(digital_svg("2:15")) + "What time is this?", "quarter past 2", ["quarter to 2", "quarter past 3", "half past 2"],
            "The hour is 2. 15 minutes is a quarter of an hour, so it is <b>quarter past 2</b>."),
        mcq(fig(digital_svg("6:30")) + "What time is this?", "half past 6", ["half past 7", "half past 5", "6 o’clock"],
            "The hour is 6. 30 minutes is half an hour, so it is <b>half past 6</b>."),
        mcq(fig(digital_svg("5:45")) + "What time is this?", "quarter to 6", ["quarter to 5", "quarter past 6", "quarter past 5"],
            "5:45 is 45 minutes past 5. 15 more minutes makes 6 o’clock. So it is <b>quarter to 6</b>. "
            "(Not quarter to 5: that is 4:45.)"),
        mcq(fig(digital_svg("12:15")) + "What time is this?", "quarter past 12", ["quarter to 12", "quarter past 1", "quarter to 1"],
            "The hour is 12. 15 minutes past is <b>quarter past 12</b>."),
    ]
    wd = [
        mcq("Which digital time is <b>quarter past 3</b>?", "3:15", ["3:03", "3:45", "4:15"],
            "Quarter past 3 is 15 minutes after 3 o’clock: <b>3:15</b>. (Not 3:03: the long hand on the 3 means 15 minutes.)"),
        mcq("Which digital time is <b>quarter to 4</b>?", "3:45", ["4:45", "4:15", "3:15"],
            "Quarter to 4 is 15 minutes <b>before</b> 4 o’clock. It is still the 3 o’clock hour: 45 minutes past 3. "
            "That is <b>3:45</b>. (4:45 is quarter to 5, and 4:15 is quarter past 4.)"),
        mcq("Which digital time is <b>half past 9</b>?", "9:30", ["10:30", "9:06", "9:00"],
            "Half past 9 is 30 minutes after 9 o’clock: <b>9:30</b>. (10:30 is half past 10.)"),
        mcq("Which digital time is <b>11 o’clock</b>?", "11:00", ["11:12", "12:00", "10:00"],
            "11 o’clock is 11 hours and 0 minutes: <b>11:00</b>."),
    ]
    pics = [
        which_clock(4, 45, [(4, 15), (5, 45), (9, 20)], 0,
                    lambda t: "(Clock %s shows 4:15. Clock %s shows 5:45.)"
                    % (letter(t, (4, 15)), letter(t, (5, 45))), True),
        which_clock(1, 30, [(2, 30), (1, 0), (6, 5)], 2,
                    lambda t: "(Clock %s shows 2:30: its short hand is past the 2.)" % letter(t, (2, 30)), True),
        which_clock(10, 15, [(10, 45), (11, 15), (3, 50)], 1,
                    lambda t: "(Clock %s shows 10:45, which is quarter to 11. Clock %s has the hands swapped.)"
                    % (letter(t, (10, 45)), letter(t, (3, 50))), True),
        which_clock(7, 45, [(7, 15), (6, 45), (9, 35)], 3,
                    lambda t: "(Clock %s shows 6:45, which is quarter to 7.)" % letter(t, (6, 45)), True),
    ]
    its = []
    for i in range(4):
        its += [an[i], wd[i]]
    for i in range(4):
        its += [an[4 + i], dw[i], pics[i]]
    assert len(its) == 20
    return {"title": "Match analog and digital times", "items": its}


# ============================================================ set 5: daily routines
def set_routines(rnd, people):
    its = []
    P = lambda: next(people)

    def his(pr):
        return "his" if pr == "he" else "her"

    its.append(mcq(fig(clock_svg(9, 0)) + "School starts at this time. What time is it?", "9 o’clock",
                   ["12 o’clock", "half past 9", "10 o’clock"],
                   "%s School starts at <b>9 o’clock</b>." % hand_text(9, 0)))
    nm, pr = P()
    its.append(mcq(fig(clock_svg(7, 30)) + "%s eats breakfast at this time. What time is it?" % nm, "half past 7",
                   ["half past 8", "7 o’clock", "6 o’clock"],
                   "%s %s eats breakfast at <b>half past 7</b>." % (hand_text(7, 30), cap(pr))))
    its.append(mcq(fig(clock_svg(10, 45)) + "The bell rings for recess. What time is it?", "quarter to 11",
                   ["quarter to 10", "quarter past 11", "quarter past 10"],
                   "%s So recess is at <b>quarter to 11</b> (10:45)." % hand_text(10, 45)))
    its.append(mcq(fig(clock_svg(3, 0)) + "School finishes at this time. What time is it?", "3 o’clock",
                   ["12 o’clock", "half past 3", "4 o’clock"],
                   "%s School finishes at <b>3 o’clock</b>." % hand_text(3, 0)))
    its.append(mcq("Lunch is at <b>half past 12</b>. Which digital time is that?", "12:30",
                   ["1:30", "12:06", "6:12"],
                   "Half past 12 is 30 minutes after 12 o’clock: <b>12:30</b>. (1:30 is half past 1.)"))
    nm, pr = P()
    its.append(mcq(fig(clock_svg(6, 45)) + "%s has dinner at this time. What time is it?" % nm, "quarter to 7",
                   ["quarter to 6", "quarter past 7", "quarter past 6"],
                   "%s %s has dinner at <b>quarter to 7</b> (6:45)." % (hand_text(6, 45), cap(pr))))
    nm, pr = P()
    its.append(mcq("%s goes to bed at <b>quarter past 8</b>. Where does the long hand point?" % nm, "the 3",
                   ["the 8", "the 9", "the 12"],
                   "At quarter past, the long hand points to the <b>3</b>. The short hand is just past the 8."))
    its.append(mcq("The school bus comes at <b>quarter past 8</b>. Which digital time is that?", "8:15",
                   ["8:03", "8:45", "9:15"],
                   "Quarter past 8 is 15 minutes after 8 o’clock: <b>8:15</b>. (8:45 is quarter to 9.)"))
    nm, pr = P()
    its.append(mcq("%s’s footy game starts at <b>quarter to 4</b>. Which digital time is that?" % nm, "3:45",
                   ["4:45", "4:15", "3:15"],
                   "Quarter to 4 is 15 minutes before 4 o’clock. It is still the 3 o’clock hour: <b>3:45</b>. "
                   "(4:45 is quarter to 5.)"))
    assert tmin(3, 0) - tmin(2, 0) == 60
    its.append(mcq(fig(clock_svg(2, 0)) + "Sport starts at this time. It lasts <b>1 hour</b>. When does it end?",
                   "3 o’clock", ["1 o’clock", "half past 2", "4 o’clock"],
                   "The clock shows 2 o’clock. 1 hour later the short hand moves on to the next number. "
                   "Sport ends at <b>3 o’clock</b>. (1 o’clock is 1 hour before.)"))
    nm, pr = P()
    assert tmin(7, 30) - tmin(7, 0) == 30
    its.append(mcq(fig(clock_svg(7, 0)) + "%s wakes up at this time. Breakfast is <b>half an hour</b> later. "
                   "When is breakfast?" % nm, "half past 7", ["half past 8", "8 o’clock", "half past 6"],
                   "The clock shows 7 o’clock. Half an hour later the long hand is on the 6. "
                   "Breakfast is at <b>half past 7</b>."))
    assert tmin(1, 0) - tmin(12, 30) == 30
    its.append(mcq(fig(clock_svg(12, 30)) + "Lunch starts at this time. It lasts <b>half an hour</b>. When does it end?",
                   "1 o’clock", ["half past 1", "12 o’clock", "quarter to 1"],
                   "The clock shows half past 12. Half an hour more takes the long hand from the 6 back to the 12. "
                   "Lunch ends at <b>1 o’clock</b>. (Half past 1 is 1 hour later, not half an hour.)"))
    nm, pr = P()
    assert tmin(4, 15) - tmin(4, 0) == 15
    its.append(mcq(fig(clock_svg(4, 0)) + "%s’s swimming lesson starts at this time. It lasts <b>a quarter of an hour</b>. "
                   "When does it end?" % nm, "quarter past 4", ["quarter to 4", "quarter past 5", "half past 4"],
                   "The clock shows 4 o’clock. A quarter of an hour later the long hand is on the 3. "
                   "The lesson ends at <b>quarter past 4</b>. (Quarter to 4 is before it starts.)"))
    nm, pr = P()
    assert tmin(9, 0) - tmin(8, 45) == 15
    its.append(mcq("School starts at <b>9 o’clock</b>. %s gets to school at <b>quarter to 9</b>. Is %s early or late?"
                   % (nm, pr), "early, by 15 minutes",
                   ["late, by 15 minutes", "early, by 45 minutes", "right on time"],
                   "Quarter to 9 is 15 minutes <b>before</b> 9 o’clock (8:45). So %s is <b>early, by 15 minutes</b>." % nm))
    assert tmin(6, 30) - tmin(6, 0) == 30
    its.append(mcq(fig(clock_svg(6, 0)) + "Mum says dinner is at <b>half past 6</b>. The clock shows the time now. "
                   "How long until dinner?", "half an hour", ["1 hour", "a quarter of an hour", "6 minutes"],
                   "The clock shows 6 o’clock. From 6 o’clock to half past 6 the long hand goes from the 12 to the 6. "
                   "That is <b>half an hour</b>."))
    assert tmin(9, 45) - tmin(9, 15) == 30
    its.append(mcq("Assembly starts at <b>quarter past 9</b>. It ends at <b>quarter to 10</b>. How long is it?",
                   "half an hour", ["1 hour", "a quarter of an hour", "45 minutes"],
                   "Quarter past 9 is 9:15. Quarter to 10 is 9:45. The long hand goes from the 3 to the 9: half way round. "
                   "Assembly is <b>half an hour</b>."))
    its.append(mcq("Which time is the <b>latest</b>?", "quarter to 5",
                   ["quarter past 4", "half past 4", "4 o’clock"],
                   "4 o’clock is 4:00, quarter past 4 is 4:15, half past 4 is 4:30, and quarter to 5 is 4:45. "
                   "The latest is <b>quarter to 5</b>."))
    its.append(mcq("Put these times in order, earliest first.", "quarter past 3, half past 3, quarter to 4",
                   ["quarter to 4, quarter past 3, half past 3", "half past 3, quarter past 3, quarter to 4",
                    "quarter past 3, quarter to 4, half past 3"],
                   "Quarter past 3 is 3:15. Half past 3 is 3:30. Quarter to 4 is 3:45. So the order is "
                   "<b>quarter past 3, half past 3, quarter to 4</b>."))
    a, b = P(), P()
    its.append(mcq("%s reads for <b>a quarter of an hour</b>. %s reads for <b>half an hour</b>. Who reads for longer?"
                   % (a[0], b[0]), b[0], [a[0], "They read for the same time", "You cannot tell"],
                   "A quarter of an hour is 15 minutes. Half an hour is 30 minutes. 30 is more than 15, "
                   "so <b>%s</b> reads for longer." % b[0]))
    nm, pr = P()
    assert tmin(4, 45) - tmin(4, 15) == 30
    its.append(mcq(fig(clock_svg(4, 15)) + "%s starts %s homework at this time. %s works for <b>half an hour</b>. "
                   "When does %s finish?" % (nm, his(pr), cap(pr), pr),
                   "quarter to 5", ["quarter past 5", "half past 4", "quarter to 4"],
                   "The clock shows quarter past 4 (4:15). Half an hour later the long hand moves from the 3 to the 9. "
                   "That is 4:45, or <b>quarter to 5</b>. (Quarter past 5 is 1 hour later.)"))
    assert len(its) == 20
    return {"title": "Daily routines", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The two hands</h2>"
        "<p>An analog clock has two hands. The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "When the long hand goes all the way round, <b>1 hour</b> has passed.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 0, size=220) +
        "<figcaption>The long hand points to the 12. The short hand points to the 3. It is <b>3 o’clock</b> (3:00).</figcaption></figure>"
        "<h2>O’clock, quarter past, half past and quarter to</h2>"
        "<p>Look at the long hand first. Then look at the short hand for the hour.</p>"
        "<figure class='sn-fig'>" + quarters_svg(7) +
        "<figcaption>The long hand on the 12, the 3, the 6 and the 9. The short hand moves slowly from the 7 towards the 8.</figcaption></figure>"
        + table(["Long hand on", "We say", "Digital"],
                [["12", "7 o’clock", "7:00"], ["3", "quarter past 7", "7:15"], ["6", "half past 7", "7:30"],
                 ["9", "quarter to 8", "7:45"]]) +
        ex("Half past", "The long hand points to the 6. The short hand is between 3 and 4.",
           "The long hand on the 6 means half past. The short hand has not reached the 4, so the hour is 3.",
           "half past 3 (3:30)") +
        "<h2>Quarter to</h2>"
        "<p>Quarter to means 15 minutes <b>before</b> the next o’clock. The short hand is nearly at the next number.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 45, size=220) +
        "<figcaption>The long hand points to the 9. The short hand is nearly at the 4. It is <b>quarter to 4</b>. "
        "On a digital clock it is 3:45.</figcaption></figure>"
        + ex("Analog to digital", "Write quarter past 3 as a digital time.",
             "Quarter past 3 is 15 minutes after 3 o’clock.", "3:15") +
        "<h2>Time facts</h2>"
        + table(["Time", "Equals"], [["1 hour", "60 minutes"], ["half an hour", "30 minutes"],
                                    ["a quarter of an hour", "15 minutes"]]) +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Hands swapped: 3 o’clock read as 12 o’clock", "The short hand tells the hour. The long hand tells the minutes."],
            ["Half past 3 read as half past 4", "The short hand has not reached the 4 yet, so the hour is still 3."],
            ["Quarter to 4 read as 4:15", "Quarter to 4 is before 4 o’clock. It is 3:45."],
            ["Quarter to 4 written as 4:45", "4:45 is quarter to 5. Quarter to 4 is 3:45."],
            ["Quarter past 3 written as 3:03", "The long hand on the 3 means 15 minutes: 3:15."],
        ])
    )


FAQ = [
    {"q": "What time should a Year 2 student be able to tell in Australia?",
     "a": "In the Australian Curriculum (AC9M2M04), Year 2 students read the time on an analog clock to the hour, half-hour and quarter-hour: o’clock, half past, quarter past and quarter to."},
    {"q": "What does quarter to mean on a clock?",
     "a": "Quarter to means 15 minutes before the next hour. The long hand points to the 9, so quarter to 4 is 3:45."},
    {"q": "Do Year 2 students sit NAPLAN?",
     "a": "No. NAPLAN is for Years 3, 5, 7 and 9. In Year 3, students build on these clock skills and read the time to the nearest minute."},
    {"q": "How can I help my child learn to tell the time?",
     "a": "Use a real analog clock at home and ask the time at everyday moments, such as breakfast, school pick-up and bedtime. Start with o’clock and half past, then quarter past and quarter to."},
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


def gen():
    rnd = random.Random(2810)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_oclock(rnd), set_half(rnd), set_quarter(rnd), set_match(rnd), set_routines(rnd, people)]
    balance(sets, rnd)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
    u = {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "telling-the-time-to-the-quarter-hour", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Telling the Time to the Quarter Hour",
        "seo_title": "Year 2 Telling the Time Worksheets: O’clock, Half Past, Quarter Past and Quarter To (Free, with Answers)",
        "short_title": "Telling the time",
        "domain": "Measurement",
        "standard_code": "AC9M2M04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise and read the time represented on an analog clock to the hour, half-hour and quarter-hour",
        "meta_desc": "Free Year 2 maths worksheets on telling the time on an analog clock: o’clock, half past, quarter past and quarter to, matching analog and digital times, and daily routines. 100 questions with an answer key, following the Australian Curriculum.",
        "key_big": "Short hand: the hour. Long hand: o’clock, quarter past, half past or quarter to.",
        "key_sub": "Long hand on 12: o’clock. On 3: quarter past. On 6: half past. On 9: quarter to the next hour, so quarter to 4 is 3:45.",
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
