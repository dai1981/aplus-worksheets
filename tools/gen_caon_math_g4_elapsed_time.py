# -*- coding: utf-8 -*-
"""
CA Grade 4 Math: Elapsed Time (Ontario Mathematics Curriculum 2020, Grade 4: E2.3)
  python3 tools/gen_caon_math_g4_elapsed_time.py
Units of time (60 s = 1 min, 60 min = 1 h, 24 h = 1 day, 7 days = 1 week); reading clocks to the minute with
a.m. and p.m.; elapsed time within the hour and across hours (open time line, count on in jumps); finding the
start or end time; schedules and word problems (hockey practice, a road trip from Toronto to Ottawa).
Every time is worked out in minutes since midnight and every duration is checked in code.
Wrong answers come from real mistakes: an hour counted as 100 minutes (subtracting the clock numbers),
a.m. and p.m. mixed up, forgetting to carry the extra hour, adding instead of counting back, using the wrong
unit relationship (12 hours in a day, 5 days in a week), and reading the clock hands the wrong way.
Canadian English; times written 3:45 p.m. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
SOFT = "#eef5f0"
FONT = "Arial, Helvetica, sans-serif"
DAY = 24 * 60
PEOPLE = [("Liam", "he"), ("Olivia", "she"), ("Noah", "he"), ("Emma", "she"), ("Aiden", "he"), ("Maya", "she"),
          ("Lucas", "he"), ("Zoe", "she"), ("Owen", "he"), ("Amira", "she"), ("Arjun", "he"), ("Mei", "she"),
          ("Ethan", "he"), ("Chloe", "she"), ("Jayden", "he"), ("Priya", "she"), ("Benjamin", "he"), ("Leah", "she"),
          ("Mateo", "he"), ("Hana", "she"), ("Nathan", "he"), ("Ava", "she"), ("Kai", "he"), ("Sofia", "she")]


# ------------------------------------------------------------ times and durations
def T(h, mi, half):
    """T(7, 25, 'pm') -> minutes since midnight."""
    assert 1 <= h <= 12 and 0 <= mi < 60
    return (h % 12) * 60 + mi + (720 if half == "pm" else 0)


def h12(h24):
    return (h24 - 1) % 12 + 1


def f12(t):
    """12-hour digital time: 3:45 p.m. (None for midnight, which is never used)."""
    t %= DAY
    if t == 720:
        return "12:00 noon"
    if t == 0:
        return None
    h = t // 60
    return "%d:%02d %s" % (h12(h), t % 60, "a.m." if h < 12 else "p.m.")


def dig(h, m):
    return "%d:%02d" % (h12(h), m)


def tm12(h, m):
    return f12(h * 60 + m)


def flip(t):
    return (t + 720) % DAY


def mins(n):
    assert n > 0
    return "%d minute%s" % (n, "" if n == 1 else "s")


def secs(n):
    assert n > 0
    return "%d second%s" % (n, "" if n == 1 else "s")


def hrs(n):
    return "%d hour%s" % (n, "" if n == 1 else "s")


def dur(n):
    assert n > 0
    hh, mm = divmod(n, 60)
    parts = []
    if hh:
        parts.append(hrs(hh))
    if mm:
        parts.append(mins(mm))
    return " ".join(parts)


def raw_dur(hh, mm):
    """'2 hours 70 minutes' style (for the 100-minutes-in-an-hour mistake)."""
    if hh <= 0 and mm <= 0:
        return None
    if hh <= 0:
        return mins(mm)
    return hrs(hh) + (" " + mins(mm) if mm else "")


UNIT_S = {"week": 604800, "day": 86400, "hour": 3600, "minute": 60, "second": 1}


def dur_value(s):
    """Any duration text -> seconds (used to keep every choice a different amount of time)."""
    v = 0
    for n_, unit in re.findall(r"(\d+) (week|day|hour|minute|second)", s):
        v += int(n_) * UNIT_S[unit]
    return v if v else s


def clock_num(t):
    """12-hour clock reading as a number: 2:05 p.m. -> 205."""
    t %= DAY
    return h12(t // 60) * 100 + t % 60


def naive100(t1, t2):
    """Subtracting the clock numbers as if an hour had 100 minutes: 9:40 to 11:15 -> 1115 - 940 = 175."""
    k = clock_num(t2) - clock_num(t1)
    if k <= 0:
        return None
    return raw_dur(k // 100, k % 100)


def mm_wrong_way(t1, t2):
    """Hours subtracted, then the smaller minutes taken from the bigger: 2:50 to 4:05 -> 2 hours 45 minutes."""
    hh = t2 // 60 - t1 // 60
    mm = abs(t2 % 60 - t1 % 60)
    return raw_dur(hh, mm)


def jumps(t1, t2):
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


def jump_label(n_):
    hh, mm = divmod(n_, 60)
    if not hh:
        return "+%d min" % mm
    if not mm:
        return "+%d h" % hh
    return "+%d h %d min" % (hh, mm)


def count_on(t1, t2):
    pts = jumps(t1, t2)
    parts = ["%s to %s is %s" % (f12(a), f12(b), dur(b - a)) for a, b in zip(pts, pts[1:])]
    d = t2 - t1
    if len(parts) == 1 and t1 // 60 == t2 // 60:
        return "Both times are in the same hour: %d − %d = <b>%s</b>." % (t2 % 60, t1 % 60, dur(d))
    if len(parts) == 1:
        return "Count on: %s. So it is <b>%s</b>." % (parts[0], dur(d))
    terms = [dur(b - a) for a, b in zip(pts, pts[1:])]
    hs = [x for x in terms if "minute" not in x]
    ms = [x for x in terms if "minute" in x]
    tail = ""
    mtot = sum(dur_value(x) for x in ms) // 60
    if len(ms) == 2 and mtot >= 60:
        tail = " (%s + %s = %d minutes = %s.)" % (ms[0], ms[1], mtot, dur(mtot))
    return "Count on in jumps: %s. %s = <b>%s</b>.%s" % ("; ".join(parts), " + ".join(hs + ms), dur(d), tail)


def add_e(t, d):
    """Explanation for t + d: add the hours, then count on the minutes through the next o'clock."""
    hh, mm = divmod(d, 60)
    s, cur = [], t
    if hh:
        s.append("Add %s: %s → %s." % (hrs(hh), f12(cur), f12(cur + hh * 60)))
        cur += hh * 60
    if mm:
        to_next = 60 - cur % 60
        if mm > to_next:
            s.append(("Then add" if s else "Add") + " %s: %s takes you to %s, and %s more is %s." % (
                mins(mm), mins(to_next), f12(cur + to_next), mins(mm - to_next), f12(cur + mm)))
        else:
            s.append(("Then add" if s else "Add") + " %s: %s." % (mins(mm), f12(cur + mm)))
    return " ".join(s)


def back_e(t, d):
    """Explanation for t - d: count back the hours, then the minutes through the o'clock."""
    hh, mm = divmod(d, 60)
    s, cur = [], t
    if hh:
        s.append("Count back %s: %s → %s." % (hrs(hh), f12(cur), f12(cur - hh * 60)))
        cur -= hh * 60
    if mm:
        back = cur % 60
        if back and mm > back:
            s.append(("Then count back" if s else "Count back") + " %s: %s takes you to %s, and %s more is %s." % (
                mins(mm), mins(back), f12(cur - back), mins(mm - back), f12(cur - mm)))
        else:
            s.append(("Then count back" if s else "Count back") + " %s: %s." % (mins(mm), f12(cur - mm)))
    return " ".join(s)


def tidy(t):
    """never a second period after a.m. / p.m."""
    return (t.replace("m.</b>.", "m.</b>").replace("a.m..", "a.m.").replace("p.m..", "p.m.")
            .replace("noon</b>.", "noon</b>."))


# ------------------------------------------------------------ question helpers
def auto_key(x):
    return dur_value(x) if re.search(r"\d+ (week|day|hour|minute|second)", x) else x


def mcq(q, correct, cands, e, key=None):
    key = key or auto_key
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


def text(x, y, t, fs=16, anchor="middle", bold=True, col=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


# ------------------------------------------------------------ figures
def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


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


def dial_numbers(cx, cy, R, k):
    fs = max(19 * k, 15)
    rn = R - 29 * k
    s = ["<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
         "paint-order='stroke'>" % (fs, LINE, 3.5 * k)]
    for i in range(12):
        a = math.radians((i + 1) * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, i + 1))
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
    s += dial_numbers(cx, cy, R, k)
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


def start_end_svg(t1, t2):
    return labelled_clocks_svg([(t1 // 60, t1 % 60), (t2 // 60, t2 % 60)], ["Start", "End"], size=180,
                               label="start and end clocks")


def timeline_svg(t1, t2, W=470):
    """Open time line (not to scale): equal spaces, each jump labelled."""
    pts = jumps(t1, t2)
    L, R, Y = 50, W - 50, 72
    n_ = len(pts) - 1

    def X(i):
        return L + (R - L) * i / float(n_)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i, t in enumerate(pts):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>"
                 % (X(i), Y - 10, X(i), Y + 10, LINE))
        s.append(text(X(i), Y + 32, f12(t), 15))
    for i in range(n_):
        x1, x2 = X(i), X(i + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1 + 4, Y - 12, (x1 + x2) / 2, Y - 54, x2 - 4, Y - 12, RED))
        s.append(text((x1 + x2) / 2, Y - 40, jump_label(pts[i + 1] - pts[i]), 15, col=RED))
    return svg_wrap(W, 114, "".join(s), "time line")


def schedule_svg(title, head, rows, widths):
    """A schedule drawn as a small table (one SVG)."""
    rh, th = 30, 34
    W = sum(widths) + 4
    H = th + rh * (len(rows) + 1) + 4
    s = ["<rect x='2' y='2' width='%d' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (W - 4, H - 4, GREEN),
         "<rect x='2' y='2' width='%d' height='%d' rx='8' fill='%s'/>" % (W - 4, th, GREEN),
         text(W / 2.0, 25, title, 17, col="#fff")]
    y = th + 2
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, SOFT))
    for r_i, row in enumerate([head] + rows):
        x = 2
        for c_i, cell in enumerate(row):
            if c_i == 0:
                s.append(text(x + 12, y + 21, cell, 16, anchor="start", bold=(r_i == 0)))
            else:
                s.append(text(x + widths[c_i] / 2.0, y + 21, cell, 16, bold=(r_i == 0)))
            x += widths[c_i]
        y += rh
        if r_i < len(rows):
            s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='#b9cfc0' stroke-width='1.5'/>" % (y, W - 2, y))
    x = 2
    for w in widths[:-1]:
        x += w
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#b9cfc0' stroke-width='1.5'/>" % (x, th + 2, x, H - 2))
    return svg_wrap(W, H, "".join(s), "schedule")


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


def words(h, m):
    h = h12(h)
    nx = h % 12 + 1
    if m < 30:
        return "%s past %d" % (mins(m), h)
    return "%s to %d" % (mins(60 - m), nx)


# ============================================================ set 1: units of time
def set_units(rnd, people):
    q = {}
    q["min_h"] = mcq("How many <b>minutes</b> are in 1 hour?", "60", ["100", "24", "30"],
                     "There are <b>60 minutes</b> in 1 hour. (Not 100: time does not count in hundreds.)")
    q["s_min"] = mcq("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "30"],
                     "There are <b>60 seconds</b> in 1 minute, just like 60 minutes in 1 hour.")
    q["h_day"] = mcq("How many <b>hours</b> are in 1 day?", "24", ["12", "60", "100"],
                     "A day is 24 hours: 12 hours of a.m. and 12 hours of p.m. 12 + 12 = <b>24</b>. "
                     "(Not 12: the clock goes around twice in one day.)")
    q["d_wk"] = mcq("How many <b>days</b> are in 1 week?", "7", ["5", "10", "30"],
                    "A week has <b>7 days</b>: Monday to Sunday. (5 is only the school days.)")
    q["unit"] = mcq("Which unit would you use to tell how long <b>March Break</b> lasts?", "days",
                    ["minutes", "seconds", "hours"],
                    "March Break is more than a week long. We count it in <b>days</b> (9 days with the weekends).")
    q["trip"] = mcq("About how long does a car trip from <b>Toronto</b> to <b>Ottawa</b> take?", "5 hours",
                    ["5 minutes", "5 days", "5 weeks"],
                    "Toronto and Ottawa are about 450 km apart. Driving on the highway takes about <b>5 hours</b>. "
                    "5 minutes is far too short, and 5 days is far too long.")
    assert 3 * 60 == 180
    q["3min"] = mcq("<b>3 minutes</b> = ? seconds", "180", ["300", "63", "120"],
                    "1 minute = 60 seconds. 3 × 60 = <b>180 seconds</b>. (300 counts a minute as 100 seconds. "
                    "63 adds 60 + 3 instead of multiplying.)")
    q["2h"] = mcq("<b>2 hours</b> = ? minutes", "120", ["200", "62", "48"],
                  "1 hour = 60 minutes. 2 × 60 = <b>120 minutes</b>. (200 counts an hour as 100 minutes. "
                  "48 uses 24, but 24 is the hours in a day.)")
    q["5wk"] = mcq("<b>5 weeks</b> = ? days", "35", ["25", "50", "12"],
                   "1 week = 7 days. 5 × 7 = <b>35 days</b>. (25 counts only the 5 school days in each week.)")
    q["3d"] = mcq("<b>3 days</b> = ? hours", "72", ["36", "180", "27"],
                  "1 day = 24 hours. 3 × 24 = <b>72 hours</b>. (36 uses 12 hours in a day. 180 uses 60.)")
    q["180s"] = mcq("<b>180 seconds</b> = ?", "3 minutes", ["18 minutes", "1 minute 80 seconds", "30 minutes"],
                    "60 seconds = 1 minute. 60 + 60 + 60 = 180, so 180 seconds = <b>3 minutes</b>. "
                    "(1 minute 80 seconds counts a minute as 100 seconds.)")
    assert 60 + 15 == 75
    q["75"] = mcq("<b>1 hour 15 minutes</b> = ? minutes", "75", ["115", "16", "45"],
                  "1 hour = 60 minutes. 60 + 15 = <b>75 minutes</b>. (115 counts an hour as 100 minutes.)")
    nm, pr = next(people)
    q["hockey"] = mcq("%s’s hockey practice lasts <b>1 hour 30 minutes</b>. How many minutes is that?" % nm,
                      "90 minutes", ["130 minutes", "31 minutes", "60 minutes"],
                      "1 hour = 60 minutes. 60 + 30 = <b>90 minutes</b>. (130 counts an hour as 100 minutes.)")
    q["150s"] = mcq("<b>2 minutes 30 seconds</b> = ? seconds", "150", ["230", "32", "90"],
                    "2 minutes = 2 × 60 = 120 seconds. 120 + 30 = <b>150 seconds</b>. (230 counts a minute as 100 seconds.)")
    nm, pr = next(people)
    q["camp"] = mcq("%s goes to summer camp for <b>2 weeks</b>. How many days is that?" % nm, "14 days",
                    ["10 days", "9 days", "20 days"],
                    "1 week = 7 days. 2 × 7 = <b>14 days</b>. (10 days counts only school days. 9 adds 2 + 7.)")
    q["21d"] = mcq("<b>21 days</b> = ?", "3 weeks", ["4 weeks 1 day", "14 weeks", "2 weeks"],
                   "7 days make 1 week. 7 + 7 + 7 = 21, so 21 days = <b>3 weeks</b>. "
                   "(4 weeks 1 day uses 5 days in a week.)")
    q["10d"] = mcq("<b>10 days</b> = ?", "1 week 3 days", ["1 week 5 days", "2 weeks", "1 week"],
                   "1 week = 7 days. 10 − 7 = 3 days left. So 10 days = <b>1 week 3 days</b>. "
                   "(1 week 5 days is 12 days.)")
    q["150m"] = mcq("<b>150 minutes</b> = ?", "2 hours 30 minutes", ["1 hour 50 minutes", "15 hours", "2 hours 5 minutes"],
                    "60 + 60 = 120 minutes make 2 hours. 150 − 120 = 30 minutes left. So 150 minutes = "
                    "<b>2 hours 30 minutes</b>. (1 hour 50 minutes counts an hour as 100 minutes.)")
    assert 60 + 20 == 80 < 90
    q["cmp1"] = mcq("Which is <b>longer</b>: 90 minutes or 1 hour 20 minutes?", "90 minutes",
                    ["1 hour 20 minutes", "They are the same.", "You cannot tell."],
                    "1 hour 20 minutes = 60 + 20 = 80 minutes. 90 is more than 80, so <b>90 minutes</b> is longer. "
                    "(1 hour 20 minutes is not 120 minutes.)", key=lambda x: x)
    assert 3 * 24 == 72 > 70
    q["cmp2"] = mcq("Which is <b>longer</b>: 3 days or 70 hours?", "3 days",
                    ["70 hours", "They are the same.", "You cannot tell."],
                    "3 days = 3 × 24 = 72 hours. 72 is more than 70, so <b>3 days</b> is longer, by 2 hours.",
                    key=lambda x: x)
    order = ["min_h", "s_min", "h_day", "d_wk", "unit", "trip", "3min", "2h", "5wk", "3d", "180s", "75", "hockey",
             "150s", "camp", "21d", "10d", "150m", "cmp1", "cmp2"]
    assert sorted(order) == sorted(q)
    return {"title": "Units of time: seconds, minutes, hours, days and weeks", "items": [q[k] for k in order]}


# ============================================================ set 2: clocks to the minute, a.m. and p.m.
CONTEXTS = [
    ("{n} wakes up on a school day.", 7, 2, 28),
    ("{n} gets on the school bus.", 8, 2, 26),
    ("Morning recess starts.", 10, 6, 28),
    ("{n}’s class goes to lunch.", 11, 32, 54),
    ("{n} gets home from school.", 15, 32, 56),
    ("{n} leaves for hockey practice.", 17, 4, 26),
    ("{n}’s family eats dinner.", 18, 32, 54),
    ("{n} starts reading before bed.", 20, 4, 28),
]


def part_of_day(h24):
    if h24 < 6:
        return "in the middle of the night"
    if h24 < 12:
        return "in the morning"
    if h24 < 17:
        return "in the afternoon"
    if h24 < 21:
        return "in the evening"
    return "at night"


def set_clocks(rnd, people):
    its = []
    used = []

    def pick(lo, hi):
        while True:
            h = rnd.randint(1, 12)
            m = rnd.randint(lo, hi)
            if m % 5 and (h, m) not in used and hands_gap(h, m) >= 18 and h not in [x[0] for x in used][-2:]:
                used.append((h, m))
                return h, m

    # clock -> digital, to the minute
    for lo, hi in [(6, 24), (31, 44), (46, 59), (16, 29), (36, 54), (1, 14)]:
        h, m = pick(lo, hi)
        n = m // 5
        right = dig(h, m)
        c = []
        if m >= 30:
            c.append(dig(h + 1, m))
        if n:
            c.append(dig(h, n * 5))
            c.append(dig(h, n))
        c += [dig(h, 60 - m), dig(h + 1, m), dig(h - 1, m), dig(h, m + 1 if m % 5 != 4 else m - 1)]
        e = "%s So the time is <b>%s</b>." % (hand_text(h, m), right)
        if m >= 30:
            e += " (Not %s: the hour hand has not reached %d yet.)" % (dig(h + 1, m), h12(h + 1))
        elif n:
            e += " (Not %s: count the small marks after the %d too.)" % (dig(h, n * 5), n)
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show?", right, c, e))
    # which clock (A to D)
    pos = [0, 1, 2, 3]
    rnd.shuffle(pos)
    for p in pos[:2]:
        while True:
            h, m = rnd.randint(1, 12), rnd.choice([x for x in range(32, 59) if x % 5])
            others = [(h + 1, m), (h, 60 - m), (h, m // 5)]
            times = list(others)
            times.insert(p, (h, m))
            if (h, m) not in used and len({(a % 12, b) for a, b in times}) == 4 and all(hands_gap(*t) >= 15 for t in times):
                used.append((h, m))
                break
        L = "ABCD"
        wrong = "; ".join("clock %s shows %s" % (L[times.index(t)], dig(*t)) for t in others)
        e = ("At %s the long hand is %d small mark%s past the %d, and the short hand is between %d and %d, close to %d. "
             "That is clock <b>%s</b>. (%s.)"
             % (dig(h, m), m % 5, "" if m % 5 == 1 else "s", m // 5, h12(h), h12(h + 1), h12(h + 1), L[p],
                wrong[0].upper() + wrong[1:]))
        its.append({"q": fig(four_clocks_svg(times)) + "Which clock shows <b>%s</b>?" % dig(h, m),
                    "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True})
    # words -> digital
    for H, mm_, part in [(9, 17, "in the morning"), (15, 42, "in the afternoon")]:
        w = words(H, mm_)
        right = tm12(H, mm_)
        if mm_ > 30:
            c = [tm12(H + 1, mm_), tm12(H + 1, 60 - mm_), tm12(H, 60 - mm_), tm12(H + 12, mm_)]
            e = ("“%s” means %d minutes <b>before</b> %d o’clock. 60 − %d = %d, so it is %d minutes past %d. "
                 "It is %s, so the time is <b>%s</b>" % (w, 60 - mm_, h12(H + 1), 60 - mm_, mm_, mm_, h12(H), part, right))
        else:
            c = [tm12(H + 12, mm_), tm12(H, 60 - mm_), tm12(H - 1, 60 - mm_), tm12(H + 1, mm_)]
            e = "“%s” means %d minutes <b>after</b> %d o’clock. It is %s, so the time is <b>%s</b>" % (
                w, mm_, h12(H), part, right)
        its.append(mcq("Write <b>%s %s</b> as a digital time." % (w, part), right, c, e))
    # contexts: clock + a.m. / p.m.
    for sent, H, lo, hi in CONTEXTS:
        ms = [x for x in range(lo, hi + 1) if x % 5 and hands_gap(H, x) >= 15]
        m = rnd.choice(ms)
        n = m // 5
        nm, pr = next(people)
        right = tm12(H, m)
        c = [tm12(H + 12, m)]
        if m >= 30:
            c.append(tm12(H + 1, m))
        if n:
            c.append(tm12(H, n))
        c += [tm12(H, 60 - m), tm12(H + 1, m), tm12(H - 1, m)]
        why = "It is before noon, so it is <b>a.m.</b>" if H < 12 else "It is after noon, so it is <b>p.m.</b>"
        e = "%s %s The time is <b>%s</b>" % (hand_text(H, m), why, right)
        e += " (Not %s: that is %s.)" % (c[0], part_of_day((H + 12) % 24))
        its.append(mcq(fig(clock_svg(H, m)) + sent.format(n=nm) + " What time is it?", right, c, e))
    assert len(its) == 18
    # morning vs evening: which is later; minutes to the next hour
    its.append(mcq("Which time is <b>later</b> in the same day: <b>10:50 a.m.</b> or <b>2:05 p.m.</b>?", "2:05 p.m.",
                   ["10:50 a.m.", "They are the same time.", "You cannot tell."],
                   "a.m. times come before noon and p.m. times come after noon. So <b>2:05 p.m.</b> is later, "
                   "even though 10 is bigger than 2.", key=lambda x: x))
    its.append(mcq("A digital clock shows <b>6:38 p.m.</b> How many minutes is it until 7:00 p.m.?", "22 minutes",
                   ["62 minutes", "38 minutes", "32 minutes"],
                   "An hour has 60 minutes. 60 − 38 = <b>22 minutes</b>. (Not 62: that is 100 − 38, but an hour is "
                   "60 minutes, not 100.)"))
    order = [0, 1, 2, 10, 11, 3, 4, 6, 12, 13, 18, 14, 15, 5, 16, 7, 17, 8, 9, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Clocks to the minute, a.m. and p.m.", "items": [its[i] for i in order]}


# ============================================================ set 3: elapsed time
def dur_q(q, t1, t2, extra=(), note=""):
    d = t2 - t1
    assert d > 0
    cands = list(extra)
    nv = naive100(t1, t2)
    if nv:
        cands.append(nv)
    cands.append(mm_wrong_way(t1, t2))
    for k in (60, -60, 10, -10, 20, -20, 5):
        if d + k > 0:
            cands.append(dur(d + k))
    e = note + count_on(t1, t2)
    if nv and dur_value(nv) != d * 60:
        e += " (Not %s: an hour has 60 minutes, not 100, so do not just subtract the clock numbers.)" % nv
    return mcq(q, dur(d), cands, e)


def set_elapsed(rnd, people):
    its = []

    def how(text_, a, b, figure=None, **kw):
        f = {"line": lambda: fig(timeline_svg(a, b)), "clocks": lambda: fig(start_end_svg(a, b)),
             None: lambda: ""}[figure]()
        its.append(dur_q(f + text_ % {"a": "<b>%s</b>" % f12(a), "b": "<b>%s</b>" % f12(b)}, a, b, **kw))

    nm = [next(people) for _ in range(8)]
    # within the hour
    how("Recess starts at %(a)s and ends at %(b)s. How long is recess?", T(10, 20, "am"), T(10, 35, "am"), "clocks")
    how("Library time is from %(a)s to %(b)s. How long is library time?", T(1, 5, "pm"), T(1, 48, "pm"))
    how(nm[0][0] + "’s piano lesson is from %(a)s to %(b)s. How long is the lesson?", T(4, 12, "pm"), T(4, 50, "pm"), "clocks")
    how(nm[1][0] + " gets on the bus at %(a)s and gets to school at %(b)s. How long is the bus ride?",
        T(8, 7, "am"), T(8, 34, "am"))
    how(nm[2][0] + " reads from %(a)s to %(b)s. How long does " + nm[2][1] + " read?", T(7, 25, "pm"), T(7, 52, "pm"), "clocks")
    # across one o'clock, less than an hour
    how("Lunch is from %(a)s to %(b)s. How long is lunch?", T(11, 45, "am"), T(12, 25, "pm"), "line")
    how(nm[3][0] + " skates at the rink from %(a)s to %(b)s. How long does " + nm[3][1] + " skate?",
        T(3, 50, "pm"), T(4, 20, "pm"), "line")
    how("Gym class is from %(a)s to %(b)s. How long is gym class?", T(9, 35, "am"), T(10, 10, "am"), "line")
    how(nm[4][0] + "’s swimming lesson is from %(a)s to %(b)s. How long is it?", T(5, 40, "pm"), T(6, 15, "pm"))
    how("Banana bread bakes in the oven from %(a)s to %(b)s. How long does it bake?", T(2, 48, "pm"), T(3, 41, "pm"))
    # more than an hour
    how("A movie starts at %(a)s and ends at %(b)s. How long is the movie?", T(6, 45, "pm"), T(8, 30, "pm"), "line")
    how("The field trip bus leaves at %(a)s and gets to the museum at %(b)s. How long is the ride?",
        T(9, 20, "am"), T(11, 5, "am"), "line")
    how("A birthday party is from %(a)s to %(b)s. How long is the party?", T(2, 0, "pm"), T(4, 45, "pm"), "clocks")
    how("The Terry Fox Run at school goes from %(a)s to %(b)s. How long is it?", T(10, 50, "am"), T(12, 35, "pm"), "line")
    how(nm[5][0] + "’s family drives to the cottage from %(a)s to %(b)s. How long is the drive?",
        T(1, 35, "pm"), T(4, 10, "pm"))
    how("A soccer tournament runs from %(a)s to %(b)s. How long is the tournament?", T(10, 30, "am"), T(2, 15, "pm"), "line",
        note="The time goes past 12 noon, from a.m. to p.m. ")
    how("The maple syrup festival is open from %(a)s to %(b)s. How long is it open?", T(9, 40, "am"), T(1, 10, "pm"),
        note="The time goes past 12 noon, from a.m. to p.m. ")
    how("A class visits the science centre from %(a)s to %(b)s. How long is the visit?", T(9, 55, "am"), T(2, 30, "pm"),
        note="The time goes past 12 noon, from a.m. to p.m. ")
    how("School starts at %(a)s and ends at %(b)s. How long is the school day?", T(8, 45, "am"), T(3, 20, "pm"),
        note="The time goes past 12 noon. ")
    how(nm[6][0] + " and " + nm[7][0] + " go on a canoe trip from %(a)s to %(b)s. How long is the trip?",
        T(8, 15, "am"), T(12, 0, "pm"), "line")
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 10, 11, 19, 13, 14, 16, 15, 17, 18]
    assert sorted(order) == list(range(20)) and len(its) == 20
    return {"title": "Elapsed time within the hour and across hours", "items": [its[i] for i in order]}


# ============================================================ set 4: start time or end time
def safe(t):
    return f12(t) if t % DAY else None


def end_q(q, t, d, extra=()):
    r = t + d
    cands = list(extra)
    if t % 60 + d % 60 >= 60:
        cands.append(safe(r - 60))                  # forgot to carry the extra hour
    cands += [safe(flip(r)), safe(t - d), safe(r + 60), safe(r - 60), safe(r + 10), safe(r - 10)]
    e = add_e(t, d)
    if (t < 720) != (r < 720):
        e += " The time goes past 12 noon, so it changes from a.m. to p.m."
    return mcq(q, f12(r), cands, e)


def start_q(q, t, d, extra=()):
    r = t - d
    cands = list(extra)
    if t % 60 < d % 60:
        cands.append(safe(r + 60))                  # borrowed minutes but forgot to take away the hour
    cands += [safe(t + d), safe(flip(r)), safe(r - 60), safe(r + 60), safe(r + 10), safe(r - 10)]
    e = back_e(t, d)
    if (t < 720) != (r < 720):
        e += " Counting back past 12 noon changes p.m. to a.m."
    e += " (Count <b>back</b> to find a start time. Adding gives a time after %s.)" % f12(t)
    return mcq(q, f12(r), cands, e)


def set_start_end(rnd, people):
    its = []
    nm = [next(people) for _ in range(8)]
    its.append(end_q("Recess starts at <b>10:20 a.m.</b> It lasts <b>15 minutes</b>. What time does recess end?",
                     T(10, 20, "am"), 15))
    its.append(end_q("The school bus leaves at <b>8:25 a.m.</b> The ride takes <b>30 minutes</b>. What time does it get to school?",
                     T(8, 25, "am"), 30))
    its.append(start_q("%s goes to bed at <b>8:30 p.m.</b> %s reads for <b>20 minutes</b> before bed. "
                       "What time does %s start reading?" % (nm[0][0], nm[0][1].capitalize(), nm[0][1]),
                       T(8, 30, "pm"), 20))
    its.append(end_q("Art class starts at <b>1:35 p.m.</b> It lasts <b>40 minutes</b>. What time does it end?",
                     T(1, 35, "pm"), 40))
    its.append(end_q("%s starts reading at <b>7:45 p.m.</b> and reads for <b>25 minutes</b>. What time does %s stop?"
                     % (nm[1][0], nm[1][1]), T(7, 45, "pm"), 25))
    its.append(start_q("%s’s soccer game starts at <b>6:10 p.m.</b> %s leaves home <b>25 minutes</b> before the game. "
                       "What time does %s leave?" % (nm[2][0], nm[2][1].capitalize(), nm[2][1]), T(6, 10, "pm"), 25))
    its.append(end_q("%s’s swimming lesson starts at <b>4:40 p.m.</b> It lasts <b>55 minutes</b>. What time does it end?"
                     % nm[3][0], T(4, 40, "pm"), 55))
    its.append(start_q("School starts at <b>8:45 a.m.</b> %s’s walk to school takes <b>18 minutes</b>. "
                       "What time must %s leave home?" % (nm[4][0], nm[4][1]), T(8, 45, "am"), 18))
    its.append(end_q("Lunch starts at <b>11:50 a.m.</b> It lasts <b>40 minutes</b>. What time does lunch end?",
                     T(11, 50, "am"), 40))
    its.append(start_q("The pizza is ready at <b>12:20 p.m.</b> It baked for <b>35 minutes</b>. What time did it go in the oven?",
                       T(12, 20, "pm"), 35))
    its.append(end_q("A movie starts at <b>6:50 p.m.</b> It lasts <b>1 hour 45 minutes</b>. What time does it end?",
                     T(6, 50, "pm"), 105))
    its.append(end_q("The field trip bus leaves at <b>9:15 a.m.</b> The ride takes <b>1 hour 50 minutes</b>. "
                     "What time does the bus arrive?", T(9, 15, "am"), 110))
    its.append(start_q("A concert ends at <b>3:05 p.m.</b> It lasted <b>50 minutes</b>. What time did it start?",
                       T(3, 5, "pm"), 50))
    its.append(start_q("A movie ends at <b>9:05 p.m.</b> It lasted <b>1 hour 40 minutes</b>. What time did it start?",
                       T(9, 5, "pm"), 100))
    its.append(start_q("Early hockey practice ends at <b>7:30 a.m.</b> It lasted <b>1 hour 15 minutes</b>. "
                       "What time did it start?", T(7, 30, "am"), 75))
    its.append(end_q("Bread rises from <b>2:20 p.m.</b> for <b>100 minutes</b>. What time is it ready?",
                     T(2, 20, "pm"), 100, extra=[f12(T(3, 20, "pm"))]))
    its[-1]["e"] = tidy("100 minutes is not 1 hour: 100 = 60 + 40, so it is 1 hour 40 minutes. " + its[-1]["e"] +
                        " (3:20 p.m. counts 100 minutes as 1 hour.)")
    its.append(end_q("On Thanksgiving, the turkey goes in the oven at <b>11:30 a.m.</b> It cooks for "
                     "<b>3 hours 15 minutes</b>. What time is it ready?", T(11, 30, "am"), 195))
    its.append(end_q("A soccer tournament starts at <b>10:45 a.m.</b> It lasts <b>2 hours 30 minutes</b>. "
                     "What time does it end?", T(10, 45, "am"), 150))
    its.append(start_q("%s’s family gets to the cottage at <b>1:10 p.m.</b> The drive took <b>2 hours 25 minutes</b>. "
                       "What time did they leave home?" % nm[5][0], T(1, 10, "pm"), 145))
    its.append(end_q("A canoe trip starts at <b>8:40 a.m.</b> It lasts <b>3 hours 35 minutes</b>. What time does it end?",
                     T(8, 40, "am"), 215))
    assert len(its) == 20
    return {"title": "Finding the start time or the end time", "items": its}


# ============================================================ set 5: schedules and word problems
HOCKEY = [("Warm-up", T(9, 0, "am"), T(9, 15, "am")), ("Skating drills", T(9, 15, "am"), T(9, 50, "am")),
          ("Passing drills", T(9, 50, "am"), T(10, 20, "am")), ("Scrimmage", T(10, 20, "am"), T(10, 45, "am"))]
TRIP = [("Leave Toronto", T(8, 35, "am")), ("Arrive in Kingston", T(11, 5, "am")),
        ("Leave Kingston", T(11, 50, "am")), ("Arrive in Ottawa", T(1, 55, "pm"))]


def hockey_svg():
    return schedule_svg("Saturday hockey practice", ["Part", "Start", "End"],
                        [[a, f12(b), f12(c)] for a, b, c in HOCKEY], [170, 115, 115])


def trip_svg():
    return schedule_svg("Road trip: Toronto to Ottawa", ["Stop", "Time"],
                        [[a, f12(b)] for a, b in TRIP], [230, 140])


def set_story(rnd, people):
    q = {}
    H = HOCKEY
    q["h1"] = dur_q(fig(hockey_svg()) + "How long are the <b>skating drills</b>?", H[1][1], H[1][2])
    q["h2"] = dur_q(fig(hockey_svg()) + "How long is the <b>whole practice</b>, from the start of the warm-up to the "
                    "end of the scrimmage?", H[0][1], H[3][2])
    lens = {a: c - b for a, b, c in H}
    assert max(lens, key=lens.get) == "Skating drills" and lens["Skating drills"] == 35
    assert naive100(H[2][1], H[2][2]) == "70 minutes"
    q["h3"] = mcq(fig(hockey_svg()) + "Which part of the practice is the <b>longest</b>?", "Skating drills",
                  ["Passing drills", "Scrimmage", "Warm-up"],
                  "Warm-up: 15 minutes. Skating drills: 9:15 to 9:50 is 35 minutes. Passing drills: 10 minutes to 10:00, "
                  "then 20 more: 30 minutes. Scrimmage: 25 minutes. The longest is <b>skating drills</b>. "
                  "(Passing drills are not 70 minutes: 1020 − 950 counts an hour as 100 minutes.)", key=lambda x: x)
    nk = next(people)
    q["h4"] = start_q(fig(hockey_svg()) + "%s gets to the rink <b>20 minutes</b> before the warm-up starts. "
                      "What time does %s get there?" % (nk[0], nk[1]), H[0][1], 20)
    P = [t for _, t in TRIP]
    q["t1"] = dur_q(fig(trip_svg()) + "How long is the drive from <b>Toronto</b> to <b>Kingston</b>?", P[0], P[1])
    q["t2"] = dur_q(fig(trip_svg()) + "How long does the family stop in <b>Kingston</b>?", P[1], P[2])
    q["t3"] = dur_q(fig(trip_svg()) + "How long is the drive from <b>Kingston</b> to <b>Ottawa</b>?", P[2], P[3],
                    extra=["9 hours 55 minutes"],
                    note="The drive goes past 12 noon, so jump to noon on the way. ")
    q["t3"]["e"] += " (Not 9 hours 55 minutes: 1:55 p.m. is after 11:50 a.m., not before it.)"
    assert 11 * 60 + 50 - (1 * 60 + 55) == 9 * 60 + 55
    q["t4"] = dur_q(fig(trip_svg()) + "How long is the <b>whole trip</b>, from leaving Toronto to arriving in Ottawa?",
                    P[0], P[3], extra=["4 hours 35 minutes"],
                    note="The trip goes past 12 noon. ")
    q["t4"]["e"] += " (4 hours 35 minutes is only the driving time. The whole trip also has the stop.)"
    drive = (P[1] - P[0]) + (P[3] - P[2])
    assert drive == 275
    q["t5"] = mcq(fig(trip_svg()) + "How much of the trip is spent <b>driving</b>?", dur(drive),
                  [dur(P[3] - P[0]), dur(P[3] - P[0] + (P[2] - P[1])), "4 hours 25 minutes"],
                  "Toronto to Kingston: 2 hours 30 minutes. Kingston to Ottawa: 2 hours 5 minutes. "
                  "2 hours + 2 hours = 4 hours, and 30 + 5 = 35 minutes. The driving time is <b>4 hours 35 minutes</b>. "
                  "(5 hours 20 minutes is the whole trip with the 45-minute stop.)")
    assert 3 * 75 == 225
    q["w_hockey"] = mcq("%s has hockey practice <b>3 times</b> a week. Each practice is <b>1 hour 15 minutes</b>. "
                        "How much practice is that in one week?" % next(people)[0], "3 hours 45 minutes",
                        ["3 hours 15 minutes", "1 hour 45 minutes", "4 hours 15 minutes"],
                        "3 × 1 hour = 3 hours. 3 × 15 minutes = 45 minutes. Together: <b>3 hours 45 minutes</b>. "
                        "(3 hours 15 minutes forgets to multiply the minutes by 3.)")
    assert 2 * 7 + 3 == 17
    q["w_cottage"] = mcq("%s’s family stays at the cottage for <b>2 weeks 3 days</b>. How many days is that?" % next(people)[0],
                         "17 days", ["13 days", "23 days", "5 days"],
                         "2 weeks = 2 × 7 = 14 days. 14 + 3 = <b>17 days</b>. (13 uses 5 days in a week. "
                         "23 uses 10 days in a week.)")
    q["w_camp"] = mcq("%s’s family goes camping for <b>72 hours</b>. How many days is that?" % next(people)[0],
                      "3 days", ["6 days", "7 days", "2 days"],
                      "1 day = 24 hours. 24 + 24 + 24 = 72, so 72 hours = <b>3 days</b>. (6 days uses 12 hours in a day.)")
    np_ = next(people)
    q["w_fox"] = end_q("The Terry Fox Run starts at <b>10:40 a.m.</b> %s finishes <b>48 minutes</b> later. "
                       "What time does %s finish?" % (np_[0], np_[1]), T(10, 40, "am"), 48)
    nd = next(people)
    q["w_drive"] = end_q("%s’s family leaves for the cottage at <b>7:50 a.m.</b> The drive takes <b>4 hours 25 minutes</b>. "
                         "What time do they arrive?" % nd[0], T(7, 50, "am"), 265)
    assert 7 * 25 == 175 == 2 * 60 + 55
    q["w_piano"] = mcq("%s practises piano for <b>25 minutes</b> every day for <b>1 week</b>. How long is that in all?"
                       % next(people)[0], "2 hours 55 minutes",
                       ["1 hour 75 minutes", "2 hours 5 minutes", "1 hour 55 minutes"],
                       "1 week = 7 days. 7 × 25 = 175 minutes. 175 − 60 − 60 = 55, so 175 minutes = "
                       "<b>2 hours 55 minutes</b>. (1 hour 75 minutes counts an hour as 100 minutes. "
                       "2 hours 5 minutes uses only 5 days.)")
    a, b = next(people), next(people)
    assert 95 - 80 == 15
    q["w_cmp"] = mcq("%s’s ringette practice is <b>1 hour 20 minutes</b>. %s’s swim practice is <b>95 minutes</b>. "
                     "Whose practice is longer, and by how much?" % (a[0], b[0]), "%s’s, by 15 minutes" % b[0],
                     ["%s’s, by 25 minutes" % a[0], "%s’s, by 15 minutes" % a[0], "%s’s, by 25 minutes" % b[0]],
                     "1 hour 20 minutes = 60 + 20 = 80 minutes. 95 − 80 = 15. So <b>%s’s</b> practice is longer, by "
                     "<b>15 minutes</b>. (%s’s by 25 minutes counts an hour as 100 minutes: 120 − 95 = 25.)" % (b[0], a[0]),
                     key=lambda x: x)
    nz = next(people)
    r = T(6, 50, "pm") + 75 + 20
    assert f12(r) == "8:25 p.m."
    q["w_ring"] = mcq("A ringette game starts at <b>6:50 p.m.</b> and lasts <b>1 hour 15 minutes</b>. Then %s’s family "
                      "drives <b>20 minutes</b> home. What time do they get home?" % nz[0], f12(r),
                      ["8:05 p.m.", "8:25 a.m.", "7:25 p.m."],
                      "Game: 6:50 p.m. + 1 hour = 7:50 p.m., + 15 minutes = 8:05 p.m. Drive: 8:05 p.m. + 20 minutes = "
                      "<b>8:25 p.m.</b> (8:05 p.m. is when the game ends, before the drive.)")
    r = T(12, 10, "pm") + 40 + 85
    assert f12(r) == "2:15 p.m."
    q["w_canoe"] = mcq("On a canoe trip, a class paddles until <b>12:10 p.m.</b> They stop for lunch for <b>40 minutes</b>. "
                       "Then they paddle for <b>1 hour 25 minutes</b> more. What time do they finish?", f12(r),
                       ["1:35 p.m.", "2:15 a.m.", "3:15 p.m."],
                       "Lunch: 12:10 p.m. + 40 minutes = 12:50 p.m. Paddling: 12:50 p.m. + 1 hour = 1:50 p.m., "
                       "+ 10 minutes = 2:00 p.m., + 15 minutes = <b>2:15 p.m.</b> (1:35 p.m. forgets the lunch stop.)")
    r = T(9, 0, "am") + 3 * 60 + 2 * 45
    assert f12(r) == "1:30 p.m."
    q["w_tourn"] = mcq("At a hockey tournament, a team plays <b>3 games</b>. Each game lasts <b>1 hour</b>, and there is "
                       "a <b>45-minute</b> break between games. The first game starts at <b>9:00 a.m.</b> "
                       "What time does the last game end?", f12(r), ["12:00 noon", "2:15 p.m.", "1:30 a.m."],
                       "Game 1: 9:00 to 10:00. Break: to 10:45. Game 2: to 11:45. Break: to 12:30 p.m. Game 3: to "
                       "<b>1:30 p.m.</b> There are only 2 breaks, because the breaks are between games. "
                       "(12:00 noon forgets the breaks. 2:15 p.m. adds 3 breaks.)", key=lambda x: x)
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    assert days[(10 - 1) % 7] == "Monday"
    q["w_day"] = mcq("%s’s family goes on a <b>10-day</b> road trip. Day 1 is a <b>Saturday</b>. "
                     "On what day of the week is day 10?" % next(people)[0], "Monday",
                     ["Tuesday", "Sunday", "Wednesday"],
                     "A week is 7 days, so day 8 is a Saturday again. Day 9 is Sunday and day 10 is <b>Monday</b>. "
                     "(Tuesday is 10 days <b>after</b> day 1, which would be day 11.)", key=lambda x: x)
    order = ["h1", "h2", "h4", "h3", "w_cottage", "w_camp", "w_fox", "t1", "t2", "t3", "t4", "t5", "w_hockey",
             "w_cmp", "w_piano", "w_drive", "w_ring", "w_canoe", "w_tourn", "w_day"]
    assert sorted(order) == sorted(q)
    return {"title": "Schedules and word problems: hockey practice and a road trip", "items": [q[k] for k in order]}


# ============================================================ lesson
def body_html():
    a, b = T(10, 45, "am"), T(1, 20, "pm")
    return tidy(
        "<h2>Units of time</h2>"
        "<p>Time does not count in tens and hundreds. Learn these facts:</p>"
        + table(["Bigger unit", "Is the same as"], [
            ["1 minute", "60 seconds"], ["1 hour", "60 minutes"], ["1 day", "24 hours"], ["1 week", "7 days"]]) +
        "<p>To change a bigger unit into a smaller one, multiply: 3 hours = 3 × 60 = 180 minutes. "
        "To change minutes into hours, take away 60 for each hour: 150 minutes = 60 + 60 + 30 = 2 hours 30 minutes.</p>"
        "<h2>Clocks to the minute, a.m. and p.m.</h2>"
        "<p>The short hand shows the hour. The long hand shows the minutes: count by 5s to the last number, then by 1s. "
        "<b>a.m.</b> times are from midnight to noon. <b>p.m.</b> times are from noon to midnight.</p>"
        "<figure class='sn-fig'>" + clock_svg(4, 37, size=220) +
        "<figcaption>The long hand is 2 marks past the 7: 35, 36, 37. The short hand has not reached 5 yet. "
        "After school, this is <b>4:37 p.m.</b></figcaption></figure>"
        "<h2>Elapsed time: count on in jumps</h2>"
        "<p>Elapsed time is how much time passes from a start time to an end time. Draw a time line. "
        "Jump to the next o’clock, then jump whole hours, then jump the minutes that are left. Add the jumps.</p>"
        "<figure class='sn-fig'>" + timeline_svg(a, b) +
        "<figcaption>From 10:45 a.m. to 1:20 p.m.: 15 minutes + 2 hours + 20 minutes = 2 hours 35 minutes."
        "</figcaption></figure>"
        + ex("Example 1: within the hour", "Recess is from 10:20 a.m. to 10:35 a.m. How long is it?",
             "Both times are in the same hour: 35 − 20 = 15.", "15 minutes") +
        ex("Example 2: across an hour", "Skating is from 3:50 p.m. to 4:20 p.m. How long is it?",
           "3:50 to 4:00 is 10 minutes. 4:00 to 4:20 is 20 minutes. 10 + 20 = 30.", "30 minutes (not 70 minutes)") +
        "<h2>Finding the end time or the start time</h2>"
        "<p>To find an <b>end</b> time, add: first the hours, then the minutes. "
        "To find a <b>start</b> time, count <b>back</b>. Watch for 12 noon: times after noon are p.m.</p>"
        + ex("Example 3: end time", "A movie starts at 6:50 p.m. and lasts 1 hour 45 minutes. When does it end?",
             add_e(T(6, 50, "pm"), 105), "8:35 p.m.") +
        ex("Example 4: start time", "Lunch is ready at 12:20 p.m. It cooked for 35 minutes. When did it start?",
           back_e(T(12, 20, "pm"), 35) + " Going back past noon changes p.m. to a.m.", "11:45 a.m.") +
        "<h2>Reading a schedule</h2>"
        "<p>A schedule lists start and end times. Find the two times you need, then count on.</p>"
        "<figure class='sn-fig'>" + hockey_svg() +
        "<figcaption>Skating drills: 9:15 a.m. to 9:50 a.m. is 35 minutes. "
        "The whole practice, 9:00 a.m. to 10:45 a.m., is 1 hour 45 minutes.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3:50 to 4:20 worked out as 420 − 350 = 70 minutes", "An hour has 60 minutes, not 100. Count on: 10 + 20 = 30 minutes"],
            ["1 hour 15 minutes = 115 minutes", "1 hour = 60 minutes: 60 + 15 = 75 minutes"],
            ["11:50 a.m. + 40 minutes = 12:30 a.m.", "After 12 noon the time is p.m.: 12:30 p.m."],
            ["9:45 + 30 minutes = 9:15 (forgot the new hour)", "45 + 30 = 75 minutes = 1 hour 15 minutes, so it is 10:15"],
            ["3 days = 36 hours", "1 day = 24 hours, not 12: 3 × 24 = 72 hours"],
            ["Adding to find a start time", "Count back from the end time"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about elapsed time in Ontario?",
     "a": "In the Ontario math curriculum (expectation E2.3), Grade 4 students solve problems about elapsed time using "
          "the relationships between seconds, minutes, hours, days and weeks."},
    {"q": "What is the easiest way to teach elapsed time?",
     "a": "Use an open time line and count on in jumps: to the next o’clock, then whole hours, then the minutes left. "
          "Adding the jumps is easier and safer than subtracting the times."},
    {"q": "Why can’t you subtract times like ordinary numbers?",
     "a": "An hour has 60 minutes, not 100. So 4:20 − 3:50 is not 70 minutes; counting on gives 10 + 20 = 30 minutes."},
    {"q": "What time facts should a Grade 4 student know?",
     "a": "60 seconds = 1 minute, 60 minutes = 1 hour, 24 hours = 1 day and 7 days = 1 week. "
          "They should also know that a.m. is from midnight to noon and p.m. is from noon to midnight."},
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
    rnd = random.Random(44816)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_units(rnd, people), set_clocks(rnd, people), set_elapsed(rnd, people), set_start_end(rnd, people),
            set_story(rnd, people)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["e"]
            for f in [it["q"], it["e"]] + it["c"]:
                assert "m.." not in re.sub("<[^>]+>", "", f), f
            k = re.sub("<svg.*?</svg>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "elapsed-time", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Elapsed Time: Units of Time, Start and End Times, and Schedules",
        "seo_title": "Grade 4 Elapsed Time Worksheets: Hours and Minutes, a.m. and p.m., Schedules (Free Math, Answer Key)",
        "short_title": "Elapsed time",
        "domain": "Spatial Sense",
        "standard_code": "Grade 4: E2.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve problems involving elapsed time by applying the relationships between different units of time",
        "meta_desc": "Free Grade 4 math worksheets on elapsed time for the Ontario curriculum: seconds, minutes, hours, "
                     "days and weeks, clocks to the minute with a.m. and p.m., elapsed time across hours, start and end "
                     "times, and schedules for hockey practice and a road trip. 100 questions with an answer key.",
        "key_big": "Count on in jumps: to the next o’clock, then whole hours, then the minutes left.",
        "key_sub": "1 hour = 60 minutes, not 100, so do not subtract clock times like ordinary numbers. "
                   "1 minute = 60 seconds, 1 day = 24 hours and 1 week = 7 days. After 12 noon, times are p.m.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "time line")
    mark_large(u, "four analog clocks")
    mark_large(u, "start and end clocks")
    mark_large(u, "schedule")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
