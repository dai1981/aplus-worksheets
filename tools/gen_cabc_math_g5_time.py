# -*- coding: utf-8 -*-
"""
British Columbia Grade 5 Math: Duration of time (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g5_time.py
Units of time and conversions (seconds to years); elapsed time within and across hours, across noon and midnight
(open time line, count on in jumps); start and end times; 24-hour times; schedules and word problems
(BC Ferries timetable, SkyTrain Expo Line timetable).
Every time is worked out in minutes since midnight and every duration is checked in code.
Wrong answers come from real mistakes: an hour counted as 100 minutes (subtracting the clock numbers),
a.m. and p.m. not switched at noon or midnight, forgetting to carry the extra hour, adding instead of counting back,
15:00 read as 5 p.m., subtracting backwards across midnight, using 12 hours in a day or 5 days in a week.
Canadian English; 12-hour times written 3:45 p.m., 24-hour times 15:45. HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
SOFT = "#eef5f0"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
DAY = 24 * 60
PEOPLE = [("Liam", "he"), ("Olivia", "she"), ("Ethan", "he"), ("Ava", "she"), ("Noah", "he"), ("Chloe", "she"),
          ("Arjun", "he"), ("Simran", "she"), ("Harjot", "he"), ("Jasleen", "she"), ("Wei", "he"), ("Mei", "she"),
          ("Ji-woo", "she"), ("Mateo", "he"), ("Hana", "she"), ("Lucas", "he"), ("Sofia", "she"), ("Kai", "he"),
          ("Emma", "she"), ("Owen", "he"), ("Leah", "she"), ("Ryan", "he"), ("Zara", "she"), ("Nadia", "she")]


# ------------------------------------------------------------ times and durations
def T(h, mi, half):
    """T(7, 25, 'pm') -> minutes since midnight."""
    assert 1 <= h <= 12 and 0 <= mi < 60
    return (h % 12) * 60 + mi + (720 if half == "pm" else 0)


def H(h, mi):
    """24-hour: H(15, 45) -> minutes since midnight."""
    assert 0 <= h < 24 and 0 <= mi < 60
    return h * 60 + mi


def h12(h24):
    return (h24 - 1) % 12 + 1


def f12(t):
    """12-hour time: 3:45 p.m.; 12:00 noon; 12:00 midnight."""
    t %= DAY
    if t == 720:
        return "12:00 noon"
    if t == 0:
        return "12:00 midnight"
    h = t // 60
    return "%d:%02d %s" % (h12(h), t % 60, "a.m." if h < 12 else "p.m.")


def f24(t):
    t %= DAY
    return "%02d:%02d" % (t // 60, t % 60)


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


UNIT_S = {"year": 31536000, "week": 604800, "day": 86400, "hour": 3600, "minute": 60, "second": 1}


def dur_value(s):
    """Any duration text -> seconds (keeps every choice a different amount of time)."""
    v = 0
    for n_, unit in re.findall(r"(\d+) (year|week|day|hour|minute|second)", s):
        v += int(n_) * UNIT_S[unit]
    return v if v else s


def time_value(s):
    m = re.match(r"^(\d{1,2}):(\d\d)( a\.m\.| p\.m\.)?$", s)
    if not m:
        return s
    h, mm, ap = int(m.group(1)), int(m.group(2)), m.group(3)
    if ap:
        h = h % 12 + (12 if ap == " p.m." else 0)
    return h * 60 + mm


def clock_num(t, fmt):
    """The clock reading as a number: 2:05 p.m. -> 205, 14:05 -> 1405."""
    t %= DAY
    if fmt is f24:
        return (t // 60) * 100 + t % 60
    return h12(t // 60) * 100 + t % 60


def naive100(t1, t2, fmt):
    """Subtracting the clock numbers as if an hour had 100 minutes: 9:40 to 11:15 -> 1115 - 940 = 175."""
    k = clock_num(t2, fmt) - clock_num(t1, fmt)
    if k <= 0:
        return None
    return raw_dur(k // 100, k % 100)


def mm_wrong_way(t1, t2):
    """Hours subtracted, then the smaller minutes taken from the bigger: 2:50 to 4:05 -> 2 hours 45 minutes."""
    hh = t2 // 60 - t1 // 60
    mm = abs(t2 % 60 - t1 % 60)
    return raw_dur(hh, mm)


def backwards(t1, t2, fmt):
    """Across noon or midnight, the smaller clock time taken from the bigger one: 9:20 to 2:05 -> 7 hours 15 minutes."""
    a = (h12(t1 // 60 % 24) if fmt is f12 else t1 // 60 % 24) * 60 + t1 % 60
    b = (h12(t2 // 60 % 24) if fmt is f12 else t2 // 60 % 24) * 60 + t2 % 60
    return dur(a - b) if a > b else None


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


def count_on(t1, t2, fmt=f12):
    pts = jumps(t1, t2)
    parts = ["%s to %s is %s" % (fmt(a), fmt(b), dur(b - a)) for a, b in zip(pts, pts[1:])]
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


def add_e(t, d, fmt=f12):
    """Explanation for t + d: add the hours, then count on the minutes through the next o'clock."""
    hh, mm = divmod(d, 60)
    s, cur = [], t
    if hh:
        s.append("Add %s: %s → %s." % (hrs(hh), fmt(cur), fmt(cur + hh * 60)))
        cur += hh * 60
    if mm:
        to_next = 60 - cur % 60
        if mm > to_next:
            s.append(("Then add" if s else "Add") + " %s: %s takes you to %s, and %s more is %s." % (
                mins(mm), mins(to_next), fmt(cur + to_next), mins(mm - to_next), fmt(cur + mm)))
        else:
            s.append(("Then add" if s else "Add") + " %s: %s." % (mins(mm), fmt(cur + mm)))
    return " ".join(s)


def back_e(t, d, fmt=f12):
    """Explanation for t - d: count back the hours, then the minutes through the o'clock."""
    hh, mm = divmod(d, 60)
    s, cur = [], t
    if hh:
        s.append("Count back %s: %s → %s." % (hrs(hh), fmt(cur), fmt(cur - hh * 60)))
        cur -= hh * 60
    if mm:
        back = cur % 60
        if back and mm > back:
            s.append(("Then count back" if s else "Count back") + " %s: %s takes you to %s, and %s more is %s." % (
                mins(mm), mins(back), fmt(cur - back), mins(mm - back), fmt(cur - mm)))
        else:
            s.append(("Then count back" if s else "Count back") + " %s: %s." % (mins(mm), fmt(cur - mm)))
    return " ".join(s)


def tidy(t):
    """never a second period after a.m. / p.m."""
    return t.replace("m.</b>.", "m.</b>").replace("a.m..", "a.m.").replace("p.m..", "p.m.")


# ------------------------------------------------------------ question helpers
def auto_key(x):
    if re.search(r"\d+ (year|week|day|hour|minute|second)", x):
        return dur_value(x)
    return time_value(x)


def mcq(q, correct, cands, e, key=None):
    """correct first + the first 3 different wrong answers (in order of how common the mistake is)."""
    key = key or auto_key
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", bold=True, col=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


# ------------------------------------------------------------ figures
def timeline_svg(t1, t2, fmt=f12, W=520):
    """Open time line (not to scale): equal spaces, each jump labelled."""
    pts = jumps(t1, t2)
    n_ = len(pts) - 1
    labels = [fmt(t) for t in pts]
    longest = max(len(x) for x in labels)
    # room for the end labels (about 8.3 px per character at 15px bold)
    half = longest * 4.3 + 4
    L, R, Y = max(50, half), W - max(50, half), 72
    gap = (R - L) / float(n_)
    assert gap >= longest * 8.6 + 8, (labels, gap)

    def X(i):
        return L + gap * i
    s = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i, t in enumerate(pts):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>"
                 % (X(i), Y - 10, X(i), Y + 10, LINE))
        s.append(text(X(i), Y + 32, labels[i], 15))
    for i in range(n_):
        x1, x2 = X(i), X(i + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1 + 4, Y - 12, (x1 + x2) / 2, Y - 54, x2 - 4, Y - 12, RED))
        s.append(text((x1 + x2) / 2, Y - 40, jump_label(pts[i + 1] - pts[i]), 15, col=RED))
    return svg_wrap(W, 114, "".join(s), "time line")


def schedule_svg(title, head, rows, widths, label="schedule", left_first=False):
    """A timetable drawn as a small table (one SVG)."""
    rh, th = 30, 34
    W = sum(widths) + 4
    Hh = th + rh * (len(rows) + 1) + 4
    s = ["<rect x='2' y='2' width='%d' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (W - 4, Hh - 4, GREEN),
         "<rect x='2' y='2' width='%d' height='%d' rx='8' fill='%s'/>" % (W - 4, th, GREEN),
         text(W / 2.0, 25, title, 17, col="#fff")]
    y = th + 2
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, SOFT))
    for r_i, row in enumerate([head] + rows):
        x = 2
        for c_i, cell in enumerate(row):
            if c_i == 0 and left_first:
                s.append(text(x + 12, y + 21, cell, 16, anchor="start", bold=(r_i == 0)))
            else:
                s.append(text(x + widths[c_i] / 2.0, y + 21, cell, 16, bold=True))
            x += widths[c_i]
        y += rh
        if r_i < len(rows):
            s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='#b9cfc0' stroke-width='1.5'/>" % (y, W - 2, y))
    x = 2
    for w in widths[:-1]:
        x += w
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#b9cfc0' stroke-width='1.5'/>" % (x, th + 2, x, Hh - 2))
    return svg_wrap(W, Hh, "".join(s), label)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ============================================================ set 1: units of time and conversions
def set_units(rnd, people):
    q = {}
    q["s_min"] = mcq("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "24"],
                     "There are <b>60 seconds</b> in 1 minute. (Not 100: time does not count in hundreds.)", key=str)
    q["h_day"] = mcq("How many <b>hours</b> are in 1 day?", "24", ["12", "60", "100"],
                     "A day is 24 hours: 12 a.m. hours and 12 p.m. hours. 12 + 12 = <b>24</b>. "
                     "(Not 12: the hour hand goes around the clock twice in one day.)", key=str)
    q["d_yr"] = mcq("How many <b>days</b> are in a year that is not a leap year?", "365", ["366", "360", "52"],
                    "A year has <b>365 days</b>. A leap year has one extra day, February 29, so it has 366. "
                    "(52 is the number of weeks in a year. 360 uses 30 days in every month, but some months have 31.)", key=str)
    q["ferry"] = mcq("About how long does a BC Ferries trip from Tsawwassen to Swartz Bay take?",
                     "about 1 hour 35 minutes",
                     ["about 1 minute 35 seconds", "about 1 day 3 hours", "about 1 week 3 days"],
                     "The ferry crosses the Strait of Georgia in a bit more than an hour and a half: "
                     "<b>about 1 hour 35 minutes</b>. 1 minute 35 seconds is far too short, and days or weeks are far too long.")
    assert 4 * 60 == 240
    q["4h"] = mcq("<b>4 hours</b> = ? minutes", "240", ["400", "64", "96"],
                  "1 hour = 60 minutes. 4 × 60 = <b>240 minutes</b>. (400 counts an hour as 100 minutes. "
                  "96 uses 24, but 24 is the hours in a day.)", key=str)
    assert 5 * 60 == 300
    q["5min"] = mcq("<b>5 minutes</b> = ? seconds", "300", ["500", "65", "120"],
                    "1 minute = 60 seconds. 5 × 60 = <b>300 seconds</b>. (500 counts a minute as 100 seconds. "
                    "65 adds 60 + 5 instead of multiplying.)", key=str)
    assert 3 * 24 == 72
    q["3d"] = mcq("<b>3 days</b> = ? hours", "72", ["36", "180", "27"],
                  "1 day = 24 hours. 3 × 24 = <b>72 hours</b>. (36 uses 12 hours in a day. 180 uses 60.)", key=str)
    assert 6 * 7 == 42
    q["6wk"] = mcq("<b>6 weeks</b> = ? days", "42", ["30", "13", "60"],
                   "1 week = 7 days. 6 × 7 = <b>42 days</b>. (30 counts only the 5 school days in each week. "
                   "13 adds 6 + 7.)", key=str)
    assert 60 * 60 == 3600
    q["1h_s"] = mcq("<b>1 hour</b> = ? seconds", "3600", ["6000", "360", "120"],
                    "1 hour = 60 minutes and each minute = 60 seconds. 60 × 60 = <b>3600 seconds</b>. "
                    "(6000 uses 100 minutes in an hour. 120 adds 60 + 60.)", key=str)
    q["210"] = mcq("<b>210 minutes</b> = ?", "3 hours 30 minutes",
                   ["2 hours 10 minutes", "21 hours", "3 hours 10 minutes"],
                   "60 + 60 + 60 = 180 minutes make 3 hours. 210 − 180 = 30 minutes left. "
                   "So 210 minutes = <b>3 hours 30 minutes</b>. (2 hours 10 minutes counts an hour as 100 minutes.)")
    assert 6 * 60 + 40 == 400
    q["400s"] = mcq("<b>400 seconds</b> = ?", "6 minutes 40 seconds",
                    ["4 minutes", "40 minutes", "7 minutes 40 seconds"],
                    "6 × 60 = 360 seconds make 6 minutes. 400 − 360 = 40 seconds left. "
                    "So 400 seconds = <b>6 minutes 40 seconds</b>. (4 minutes counts a minute as 100 seconds.)")
    assert 3 * 60 + 25 == 205
    q["3h25"] = mcq("<b>3 hours 25 minutes</b> = ? minutes", "205", ["325", "28", "145"],
                    "3 hours = 3 × 60 = 180 minutes. 180 + 25 = <b>205 minutes</b>. (325 counts an hour as 100 minutes. "
                    "145 counts only 2 hours.)", key=str)
    assert 4 * 24 + 4 == 100
    q["100h"] = mcq("<b>100 hours</b> = ?", "4 days 4 hours", ["1 day", "8 days 4 hours", "4 days"],
                    "1 day = 24 hours. 4 × 24 = 96 hours make 4 days. 100 − 96 = 4 hours left. "
                    "So 100 hours = <b>4 days 4 hours</b>. (1 day thinks a day has 100 hours. "
                    "8 days 4 hours uses 12 hours in a day.)")
    q["2yr"] = mcq("<b>2 years</b> = ? months", "24", ["104", "730", "12"],
                   "1 year = 12 months. 2 × 12 = <b>24 months</b>. (104 is the weeks in 2 years, and 730 is the days.)",
                   key=str)
    q["3q"] = mcq("How many minutes are in <b>three quarters of an hour</b>?", "45", ["75", "30", "34"],
                  "A quarter of an hour is 60 ÷ 4 = 15 minutes. 3 × 15 = <b>45 minutes</b>. "
                  "(75 is three quarters of 100, but an hour is 60 minutes.)", key=str)
    assert 7 * 24 == 168
    q["wk_h"] = mcq("How many <b>hours</b> are in 1 week?", "168", ["84", "700", "31"],
                    "1 week = 7 days and each day = 24 hours. 7 × 24 = <b>168 hours</b>. "
                    "(84 uses 12 hours in a day. 31 adds 7 + 24.)", key=str)
    assert 24 * 60 * 60 == 86400
    q["day_s"] = mcq("How many <b>seconds</b> are in 1 day?", "86" + NB + "400",
                     ["1440", "144" + NB + "000", "8640"],
                     "1 day = 24 hours = 24 × 60 = 1440 minutes. Each minute is 60 seconds: 1440 × 60 = "
                     "<b>86" + NB + "400 seconds</b>. (1440 is the minutes in a day, not the seconds. "
                     "144" + NB + "000 uses 100 minutes in an hour.)", key=str)
    assert 3 * 7 + 4 == 25
    nm = next(people)[0]
    q["camp"] = mcq("%s’s family camps on Vancouver Island for <b>3 weeks 4 days</b>. How many days is that?" % nm,
                    "25 days", ["19 days", "34 days", "7 days"],
                    "3 weeks = 3 × 7 = 21 days. 21 + 4 = <b>25 days</b>. (19 uses 5 days in a week. "
                    "34 uses 10 days in a week.)")
    assert 2 * 60 + 10 == 130 > 125
    q["cmp"] = mcq("Which is <b>longer</b>: 2 hours 10 minutes or 125 minutes?", "2 hours 10 minutes",
                   ["125 minutes", "They are the same.", "You cannot tell."],
                   "2 hours 10 minutes = 60 + 60 + 10 = 130 minutes. 130 is more than 125, so "
                   "<b>2 hours 10 minutes</b> is longer, by 5 minutes. (2 hours 10 minutes is not 210 minutes.)",
                   key=str)
    assert 90 < 100 < 105
    q["order"] = mcq("Put these in order from <b>shortest</b> to <b>longest</b>: 1 hour 45 minutes, 100 minutes, "
                     "1 hour 30 minutes.", "1 hour 30 minutes, 100 minutes, 1 hour 45 minutes",
                     ["100 minutes, 1 hour 30 minutes, 1 hour 45 minutes",
                      "1 hour 30 minutes, 1 hour 45 minutes, 100 minutes",
                      "1 hour 45 minutes, 100 minutes, 1 hour 30 minutes"],
                     "Change everything to minutes. 1 hour 30 minutes = 90, 100 minutes = 100, 1 hour 45 minutes = 105. "
                     "So the order is <b>1 hour 30 minutes, 100 minutes, 1 hour 45 minutes</b>. "
                     "(100 minutes is not 1 hour: it is 1 hour 40 minutes.)", key=str)
    order = ["s_min", "h_day", "d_yr", "ferry", "4h", "5min", "3d", "6wk", "3q", "2yr", "3h25", "210", "1h_s",
             "400s", "wk_h", "camp", "cmp", "order", "100h", "day_s"]
    assert sorted(order) == sorted(q)
    return {"title": "Units of time and conversions", "items": [q[k] for k in order]}


# ============================================================ set 2: elapsed time (12-hour)
def dur_q(q, t1, t2, fmt=f12, extra=(), note=""):
    d = t2 - t1
    assert d > 0
    cands = list(extra)
    nv = naive100(t1, t2, fmt)
    if nv:
        cands.append(nv)
    if t1 // 720 != t2 // 720 or (fmt is f24 and t2 >= DAY):
        bw = backwards(t1, t2, fmt)
        if bw:
            cands.append(bw)
    else:
        bw = None
    cands.append(mm_wrong_way(t1, t2))
    for k in (60, -60, 10, -10, 20, -20, 5):
        if d + k > 0:
            cands.append(dur(d + k))
    e = note + count_on(t1, t2, fmt)
    it = mcq(q, dur(d), cands, e)
    if nv and dur_value(nv) != d * 60 and nv in it["c"]:
        it["e"] += " (Not %s: an hour has 60 minutes, not 100, so do not just subtract the clock numbers.)" % nv
    if bw and bw in it["c"]:
        def bare(t):
            return fmt(t).replace(" a.m.", "").replace(" p.m.", "")
        it["e"] += (" (Not %s: that takes the smaller clock time from the bigger one, %s − %s. Count on past %s "
                    "instead.)" % (bw, bare(t1), bare(t2),
                                   ("midnight" if fmt is f12 else "midnight (00:00)") if t2 >= DAY else "12 noon"))
    return it


def set_elapsed(rnd, people):
    its = []

    def how(text_, a, b, line=False, **kw):
        f = fig(timeline_svg(a, b)) if line else ""
        its.append(dur_q(f + text_ % {"a": "<b>%s</b>" % f12(a), "b": "<b>%s</b>" % f12(b)}, a, b, **kw))

    nm = [next(people) for _ in range(8)]
    NOON = "The time goes past 12 noon, from a.m. to p.m. "
    MID = "The time goes past 12 midnight, from p.m. to a.m. "
    # 0-4 within the hour or across one o'clock
    how("Recess starts at %(a)s and ends at %(b)s. How long is recess?", T(10, 15, "am"), T(10, 32, "am"))
    how("Library time is from %(a)s to %(b)s. How long is library time?", T(1, 5, "pm"), T(1, 48, "pm"))
    how("Music class is from %(a)s to %(b)s. How long is music class?", T(9, 35, "am"), T(10, 20, "am"), line=True)
    how(nm[0][0] + "’s swimming lesson is from %(a)s to %(b)s. How long is the lesson?", T(4, 50, "pm"), T(5, 35, "pm"))
    how("Salmon cooks on the barbecue from %(a)s to %(b)s. How long does it cook?", T(5, 38, "pm"), T(6, 21, "pm"))
    # 5-6 across noon, less than an hour
    how("Lunch is from %(a)s to %(b)s. How long is lunch?", T(11, 48, "am"), T(12, 25, "pm"), line=True, note=NOON)
    how("The Terry Fox Run at school starts at %(a)s. " + nm[1][0] + " finishes at %(b)s. How long does "
        + nm[1][1] + " take?", T(10, 35, "am"), T(11, 22, "am"))
    # 7-12 more than an hour
    how(nm[2][0] + " hikes the Grouse Grind from %(a)s to %(b)s. How long is the hike?", T(8, 47, "am"), T(10, 22, "am"),
        line=True)
    how(nm[3][0] + "’s soccer practice is from %(a)s to %(b)s. How long is practice?", T(5, 45, "pm"), T(7, 10, "pm"))
    how("A movie starts at %(a)s and ends at %(b)s. How long is the movie?", T(6, 55, "pm"), T(9, 10, "pm"), line=True)
    how("A lacrosse game is from %(a)s to %(b)s. How long is the game?", T(6, 40, "pm"), T(8, 55, "pm"))
    how(nm[4][0] + "’s snowboard lesson at Whistler is from %(a)s to %(b)s. How long is the lesson?",
        T(10, 45, "am"), T(1, 15, "pm"), note=NOON)
    how("A kayak tour on the Fraser River is from %(a)s to %(b)s. How long is the tour?", T(9, 50, "am"),
        T(12, 35, "pm"), line=True, note=NOON)
    # 13-17 long, across noon
    how("A class field trip to Science World is from %(a)s to %(b)s. How long is the trip?",
        T(9, 20, "am"), T(2, 5, "pm"), line=True, note=NOON)
    how(nm[5][0] + "’s family drives from Vancouver to Kelowna. They leave at %(a)s and arrive at %(b)s. "
        "How long is the drive?", T(7, 25, "am"), T(12, 10, "pm"), note=NOON)
    how("The school day is from %(a)s to %(b)s. How long is the school day?", T(8, 40, "am"), T(2, 58, "pm"), note=NOON)
    how("A charity skate-a-thon runs from %(a)s to %(b)s. How long does it run?", T(3, 35, "pm"), T(9, 10, "pm"))
    how("A hockey tournament runs from %(a)s to %(b)s. How long does it run?", T(7, 40, "am"), T(3, 25, "pm"), note=NOON)
    # 18-19 across midnight
    how("The power goes out at %(a)s. It comes back on at %(b)s the next morning. How long is the power out?",
        T(11, 40, "pm"), T(2, 15, "am") + DAY, line=True, note=MID)
    how("On a camping trip, " + nm[6][0] + " falls asleep at %(a)s and wakes up at %(b)s the next morning. "
        "How long does " + nm[6][1] + " sleep?", T(9, 50, "pm"), T(6, 35, "am") + DAY, line=True, note=MID)
    assert len(its) == 20
    return {"title": "Elapsed time within and across hours", "items": its}


# ============================================================ set 3: start and end times (12-hour)
def safe(t, fmt=f12):
    return fmt(t) if t % 720 else None


def end_q(q, t, d, fmt=f12, extra=()):
    r = t + d
    cands = list(extra)
    if t % 60 + d % 60 >= 60:
        cands.append(safe(r - 60, fmt))                  # forgot to carry the extra hour
    if fmt is f12:
        cands.append(safe(flip(r)))                       # a.m. / p.m. not switched (or switched wrongly)
    cands += [safe(t - d, fmt), safe(r + 60, fmt), safe(r - 60, fmt), safe(r + 10, fmt), safe(r - 10, fmt)]
    e = add_e(t, d, fmt)
    if fmt is f12 and (t % DAY < 720) != (r % DAY < 720):
        e += " The time goes past 12 %s, so it changes from %s." % (
            "noon" if r % DAY >= 720 else "midnight", "a.m. to p.m." if r % DAY >= 720 else "p.m. to a.m.")
    return mcq(q, fmt(r), cands, e)


def start_q(q, t, d, fmt=f12, extra=()):
    r = t - d
    cands = list(extra)
    if t % 60 < d % 60:
        cands.append(safe(r + 60, fmt))                  # borrowed the minutes but did not take away the hour
    cands.append(safe(t + d, fmt))                        # added instead of counting back
    if fmt is f12:
        cands.append(safe(flip(r)))
    cands += [safe(r - 60, fmt), safe(r + 60, fmt), safe(r + 10, fmt), safe(r - 10, fmt)]
    e = back_e(t, d, fmt)
    if fmt is f12 and (t % DAY < 720) != (r % DAY < 720):
        e += " Counting back past 12 %s changes %s." % (
            "noon" if t % DAY >= 720 else "midnight", "p.m. to a.m." if t % DAY >= 720 else "a.m. to p.m.")
    e += " (Count <b>back</b> to find a start time. Adding gives a time after %s.)" % fmt(t)
    return mcq(q, fmt(r), cands, e)


def set_start_end(rnd, people):
    q = {}
    nm = [next(people) for _ in range(8)]
    q["e1"] = end_q("Recess starts at <b>10:20 a.m.</b> It lasts <b>25 minutes</b>. What time does recess end?",
                    T(10, 20, "am"), 25)
    q["e2"] = end_q("The school bus leaves at <b>8:35 a.m.</b> The ride takes <b>40 minutes</b>. "
                    "What time does it get to school?", T(8, 35, "am"), 40)
    q["s1"] = start_q("Art class ends at <b>3:10 p.m.</b> It lasted <b>35 minutes</b>. What time did it start?",
                      T(3, 10, "pm"), 35)
    q["e3"] = end_q("%s starts a science project at <b>1:45 p.m.</b> and works for <b>50 minutes</b>. "
                    "What time does %s stop?" % (nm[0][0], nm[0][1]), T(1, 45, "pm"), 50)
    q["s2"] = start_q("School starts at <b>8:45 a.m.</b> %s’s bus ride takes <b>50 minutes</b>. "
                      "What time must %s get on the bus?" % (nm[1][0], nm[1][1]), T(8, 45, "am"), 50)
    q["e4"] = end_q("Gym class starts at <b>11:25 a.m.</b> It lasts <b>55 minutes</b>. What time does it end?",
                    T(11, 25, "am"), 55)
    q["s3"] = start_q("Lunch is ready at <b>12:15 p.m.</b> The soup cooked for <b>40 minutes</b>. "
                      "What time did it start cooking?", T(12, 15, "pm"), 40)
    q["e5"] = end_q("A movie starts at <b>6:50 p.m.</b> It lasts <b>1 hour 35 minutes</b>. What time does it end?",
                    T(6, 50, "pm"), 95)
    q["s4"] = start_q("Early hockey practice ends at <b>7:30 a.m.</b> It lasted <b>1 hour 15 minutes</b>. "
                      "What time did it start?", T(7, 30, "am"), 75)
    q["e6"] = end_q("A field trip to Stanley Park starts at <b>9:40 a.m.</b> It lasts <b>2 hours 45 minutes</b>. "
                    "What time does it end?", T(9, 40, "am"), 165)
    q["s5"] = start_q("A concert ends at <b>9:05 p.m.</b> It lasted <b>1 hour 50 minutes</b>. What time did it start?",
                      T(9, 5, "pm"), 110)
    q["e7"] = end_q("Bread rises from <b>2:20 p.m.</b> for <b>100 minutes</b>. What time is it ready?",
                    T(2, 20, "pm"), 100, extra=[f12(T(3, 20, "pm"))])
    q["e7"]["e"] = tidy("100 minutes is not 1 hour: 100 = 60 + 40, so it is 1 hour 40 minutes. " + q["e7"]["e"] +
                        " (3:20 p.m. counts 100 minutes as 1 hour.)")
    q["e8"] = end_q("%s’s family leaves for Whistler at <b>7:55 a.m.</b> The trip takes <b>3 hours 25 minutes</b> with "
                    "stops. What time do they arrive?" % nm[2][0], T(7, 55, "am"), 205)
    q["s6"] = start_q("A whale-watching tour gets back to Victoria at <b>1:20 p.m.</b> It lasted "
                      "<b>2 hours 35 minutes</b>. What time did it start?", T(1, 20, "pm"), 155)
    assert T(4, 0, "pm") - 135 == T(1, 45, "pm")
    q["s7"] = start_q("A ringette tournament ends at <b>4:00 p.m.</b> The last game lasted <b>135 minutes</b>. "
                      "What time did the last game start?", T(4, 0, "pm"), 135, extra=[f12(T(2, 25, "pm"))])
    q["s7"]["e"] = tidy("135 minutes = 60 + 60 + 15 = 2 hours 15 minutes. " + q["s7"]["e"] +
                        " (2:25 p.m. reads 135 minutes as 1 hour 35 minutes.)")
    q["e9"] = end_q("The New Year’s Eve fireworks show in Vancouver starts at <b>11:35 p.m.</b> %s watches for "
                    "<b>40 minutes</b>. What time does %s stop watching?" % (nm[3][0], nm[3][1]), T(11, 35, "pm"), 40)
    q["e10"] = end_q("%s’s family starts driving to Prince George at <b>9:30 p.m.</b> The drive takes "
                     "<b>3 hours 50 minutes</b> before they stop to rest. What time do they stop?" % nm[4][0],
                     T(9, 30, "pm"), 230)
    q["s8"] = start_q("A bus arrives in Vancouver at <b>6:10 a.m.</b> after an overnight trip of <b>7 hours 25 minutes</b>. "
                      "What time did it leave?", T(6, 10, "am") + DAY, 445)
    # minutes until midnight
    q["mid"] = dur_q("It is <b>10:38 p.m.</b> How long is it until <b>12:00 midnight</b>?", T(10, 38, "pm"), DAY)
    # latest start time, two steps
    r = T(6, 30, "pm") - 70 - 25
    assert f12(r) == "4:55 p.m."
    q["pie"] = mcq("A salmon pie bakes for <b>1 hour 10 minutes</b> and then cools for <b>25 minutes</b>. "
                   "Dinner is at <b>6:30 p.m.</b> What is the latest time the pie can go in the oven?", f12(r),
                   ["5:20 p.m.", "5:05 p.m.", "8:05 p.m."],
                   "Add the times first: 1 hour 10 minutes + 25 minutes = 1 hour 35 minutes. Count back from 6:30 p.m.: "
                   "1 hour → 5:30 p.m. 30 minutes → 5:00 p.m. 5 more minutes → <b>4:55 p.m.</b> "
                   "(5:20 p.m. forgets the cooling time. 8:05 p.m. adds instead of counting back.)")
    order = ["e1", "e2", "s1", "e3", "s2", "e4", "s3", "e5", "s4", "mid", "e6", "s5", "e7", "e8", "s6", "s7",
             "e9", "e10", "s8", "pie"]
    assert sorted(order) == sorted(q)
    return {"title": "Finding the start time or the end time", "items": [q[k] for k in order]}


# ============================================================ set 4: 24-hour times
def set_24(rnd, people):
    q = {}
    q["c1"] = mcq("Write <b>16:35</b> as a 12-hour time.", "4:35 p.m.", ["6:35 p.m.", "4:35 a.m.", "3:35 p.m."],
                  "Hours from 13 to 23 are p.m. times. Take away 12: 16 − 12 = 4. So 16:35 is <b>4:35 p.m.</b> "
                  "(Not 6:35 p.m.: do not just drop the 1. 16 − 12 = 4, not 6.)")
    q["c2"] = mcq("Write <b>9:20 p.m.</b> in 24-hour time.", "21:20", ["09:20", "19:20", "22:20"],
                  "p.m. times are after noon. Add 12 to the hour: 9 + 12 = 21. So 9:20 p.m. is <b>21:20</b>. "
                  "(09:20 is in the morning.)")
    q["c3"] = mcq("Write <b>00:45</b> as a 12-hour time.", "12:45 a.m.", ["12:45 p.m.", "1:45 a.m.", "10:45 p.m."],
                  "00 is the hour just after <b>midnight</b>. In 12-hour time that hour is 12 a.m. So 00:45 is "
                  "<b>12:45 a.m.</b>, 45 minutes after midnight. (12:45 p.m. is 45 minutes after noon.)")
    q["c4"] = mcq("Write <b>12:10 p.m.</b> in 24-hour time.", "12:10", ["00:10", "24:10", "13:10"],
                  "12:10 p.m. is 10 minutes after <b>noon</b>. Noon is 12:00 in 24-hour time, so do not add 12. "
                  "It is <b>12:10</b>. (00:10 is 10 minutes after midnight.)")
    pp = [next(people) for _ in range(6)]
    q["d1"] = dur_q("A ferry sails from <b>09:40</b> to <b>11:15</b>. How long is the trip?", H(9, 40), H(11, 15), fmt=f24)
    q["d2"] = dur_q(fig(timeline_svg(H(13, 25), H(16, 10), f24)) + "A soccer tournament runs from <b>13:25</b> to "
                    "<b>16:10</b>. How long does it run?", H(13, 25), H(16, 10), fmt=f24)
    q["d3"] = dur_q("%s’s family visits the Vancouver Aquarium from <b>14:50</b> to <b>18:05</b>. How long is the visit?"
                    % pp[0][0], H(14, 50), H(18, 5), fmt=f24)
    q["d4"] = dur_q("A train leaves at <b>08:35</b> and arrives at <b>15:20</b>. How long is the trip?",
                    H(8, 35), H(15, 20), fmt=f24)
    q["d5"] = dur_q("A hockey game on TV is on from <b>17:48</b> to <b>20:30</b>. How long is it on?",
                    H(17, 48), H(20, 30), fmt=f24)
    q["d6"] = dur_q(fig(timeline_svg(H(22, 40), H(1, 15) + DAY, f24)) + "A plane leaves Vancouver at <b>22:40</b> and "
                    "lands at <b>01:15</b> the next morning (Vancouver time). How long is the flight?",
                    H(22, 40), H(1, 15) + DAY, fmt=f24, note="The time goes past midnight (00:00). ")
    q["d7"] = dur_q("A night shift at the hospital is from <b>23:20</b> to <b>06:45</b> the next morning. "
                    "How long is the shift?", H(23, 20), H(6, 45) + DAY, fmt=f24,
                    note="The time goes past midnight (00:00). ")
    q["d8"] = dur_q("%s is at a ski camp on Grouse Mountain from <b>06:55</b> to <b>19:10</b>. How long is that?"
                    % pp[1][0], H(6, 55), H(19, 10), fmt=f24)
    q["n1"] = end_q("A ferry leaves at <b>14:35</b>. The trip takes <b>2 hours 50 minutes</b>. What time does it arrive?",
                    H(14, 35), 170, fmt=f24)
    q["n2"] = end_q("A concert starts at <b>19:40</b> and lasts <b>3 hours 35 minutes</b>. What time does it end?",
                    H(19, 40), 215, fmt=f24)
    assert f24(H(22, 30) + 255) == "02:45"
    q["n3"] = end_q("A bus leaves Kamloops at <b>22:30</b>. The trip takes <b>4 hours 15 minutes</b>. "
                    "What time does it arrive?", H(22, 30), 255, fmt=f24, extra=["26:45"])
    q["n3"]["e"] += " After 23:59 the clock starts again at 00:00, so there is no 26:45."
    q["n4"] = end_q("A SkyTrain trip starts at <b>11:50</b>. %s rides and walks for <b>95 minutes</b> in all. "
                    "What time does %s get there?" % (pp[2][0], pp[2][1]), H(11, 50), 95, fmt=f24,
                    extra=["12:45"])
    q["n4"]["e"] = "95 minutes = 60 + 35 = 1 hour 35 minutes. " + q["n4"]["e"] + " (12:45 reads 95 minutes as 55 minutes.)"
    q["b1"] = start_q("A ferry arrives at <b>13:10</b> after a trip of <b>2 hours 25 minutes</b>. "
                      "What time did it leave?", H(13, 10), 145, fmt=f24)
    q["b2"] = start_q("%s’s bus arrives in Prince George at <b>07:20</b> after a trip of <b>9 hours 40 minutes</b>. "
                      "What time did it leave the evening before?" % pp[3][0], H(7, 20) + DAY, 580, fmt=f24)
    assert H(12, 30) - H(10, 45) == 105 and H(17, 30) - H(15, 50) == 100
    q["cmp"] = mcq("Which lasts <b>longer</b>: a game from <b>10:45</b> to <b>12:30</b>, or a game from <b>15:50</b> "
                   "to <b>17:30</b>?", "10:45 to 12:30, by 5 minutes",
                   ["15:50 to 17:30, by 5 minutes", "15:50 to 17:30, by 35 minutes", "They are the same."],
                   "10:45 to 12:30: 15 minutes + 1 hour + 30 minutes = 1 hour 45 minutes. "
                   "15:50 to 17:30: 10 minutes + 1 hour + 30 minutes = 1 hour 40 minutes. "
                   "So <b>10:45 to 12:30</b> is longer, <b>by 5 minutes</b>. (“15:50 to 17:30, by 35 minutes” counts it as "
                   "2 hours 20 minutes: 17 − 15 = 2 and 50 − 30 = 20. But 17:30 is not 2 full hours after 15:50.)", key=str)
    assert H(21, 5) - H(18, 40) == 145
    q["min"] = mcq("An electric bike charges from <b>18:40</b> to <b>21:05</b>. How many <b>minutes</b> is that?",
                   "145 minutes", ["265 minutes", "125 minutes", "205 minutes"],
                   "18:40 to 19:00 is 20 minutes. 19:00 to 21:00 is 2 hours = 120 minutes. 21:00 to 21:05 is 5 minutes. "
                   "20 + 120 + 5 = <b>145 minutes</b>. (265 subtracts the clock numbers: 2105 − 1840 = 265, as if an "
                   "hour had 100 minutes.)")
    order = ["c1", "c2", "c3", "c4", "d1", "d2", "d3", "n1", "b1", "d4", "d5", "n2", "min", "n4", "cmp", "d8",
             "d6", "n3", "d7", "b2"]
    assert sorted(order) == sorted(q)
    return {"title": "24-hour times: converting and elapsed time", "items": [q[k] for k in order]}


# ============================================================ set 5: schedules and word problems
FERRY = [(H(h, 0), H(h, 0) + 95) for h in (9, 11, 13, 15, 17, 19)]
SKY = [("Waterfront", H(8, 47)), ("Commercial–Broadway", H(8, 56)), ("Metrotown", H(9, 4)),
       ("New Westminster", H(9, 11)), ("King George", H(9, 26))]


def ferry_svg():
    return schedule_svg("BC Ferries: Swartz Bay to Tsawwassen", ["Leaves Swartz Bay", "Arrives Tsawwassen"],
                        [[f24(a), f24(b)] for a, b in FERRY], [190, 190], label="ferry timetable")


def sky_svg():
    return schedule_svg("SkyTrain Expo Line (one train)", ["Station", "Time"],
                        [[a, f24(b)] for a, b in SKY], [240, 110], label="SkyTrain timetable",
                        left_first=True)


def set_story(rnd, people):
    q = {}
    FT, ST = fig(ferry_svg()), fig(sky_svg())
    assert FERRY[2] == (H(13, 0), H(14, 35))
    q["f1"] = mcq(FT + "The ferry leaves Swartz Bay at <b>13:00</b>. What time does it arrive in Tsawwassen?", "14:35",
                  ["12:35", "16:35", "13:35"],
                  "Find 13:00 in the “Leaves Swartz Bay” column. Look across that row: it arrives at <b>14:35</b>. "
                  "(12:35 and 16:35 are on other rows.)")
    q["f2"] = dur_q(FT + "How long does the ferry take to go from Swartz Bay to Tsawwassen?", H(13, 0), H(14, 35), fmt=f24,
                    extra=["2 hours 35 minutes"])
    q["f2"]["e"] = "Take any row, such as 13:00 to 14:35. " + q["f2"]["e"]
    nm = next(people)
    assert FERRY[4] == (H(17, 0), H(18, 35))
    q["f3"] = mcq(FT + "%s arrives in Tsawwassen at <b>6:35 p.m.</b> Which sailing did %s take from Swartz Bay?"
                  % (nm[0], nm[1]), "17:00", ["15:00", "19:00", "18:00"],
                  "6:35 p.m. in 24-hour time is 6 + 12 = 18, so 18:35. Find 18:35 in the “Arrives” column. That ferry "
                  "leaves Swartz Bay at <b>17:00</b>. (Not 15:00: that ferry arrives at 16:35, which is 4:35 p.m.)")
    nm = next(people)
    assert FERRY[2][1] < H(16, 0) < FERRY[3][1]
    q["f4"] = mcq(FT + "%s’s family must be in Tsawwassen by <b>4:00 p.m.</b> What is the latest ferry they can take "
                  "from Swartz Bay?" % nm[0], "13:00", ["15:00", "14:35", "11:00"],
                  "4:00 p.m. is 16:00. Look down the “Arrives” column for the last time before 16:00: 14:35. "
                  "That ferry leaves at <b>13:00</b>. (The 15:00 ferry arrives at 16:35, too late. "
                  "14:35 is an arrival time, not a sailing.)", key=str)
    nm = next(people)
    q["f5"] = dur_q(FT + "%s gets to the Swartz Bay terminal at <b>10:05</b>, just after the 09:00 ferry has left. "
                    "How long must %s wait for the next ferry?" % (nm[0], nm[1]), H(10, 5), H(11, 0), fmt=f24)
    nm = next(people)
    r = FERRY[3][1] + 50
    assert f12(r) == "5:25 p.m."
    q["f6"] = mcq(FT + "%s’s family takes the <b>15:00</b> ferry from Swartz Bay. When they get off in Tsawwassen, "
                  "they drive <b>50 minutes</b> home to Surrey. What time do they get home, in 12-hour time?" % nm[0],
                  f12(r), ["7:25 p.m.", "4:25 p.m.", "5:25 a.m."],
                  "The 15:00 ferry arrives at 16:35. 16:35 + 50 minutes: 25 minutes takes you to 17:00, and 25 more is "
                  "17:25. 17 − 12 = 5, so it is <b>5:25 p.m.</b> (Not 7:25 p.m.: 17:25 is 5:25 p.m., not 7:25 p.m. "
                  "4:25 p.m. forgets to carry the new hour.)")
    nm = next(people)
    r = H(11, 0) - 45 - 35
    assert f24(r) == "09:40"
    q["f7"] = mcq(FT + "%s’s family wants to be at Swartz Bay <b>45 minutes</b> before the <b>11:00</b> ferry. "
                  "The drive from Victoria takes <b>35 minutes</b>. What is the latest time they can leave home?" % nm[0],
                  f24(r), ["10:15", "10:25", "12:20"],
                  "They must be at the terminal by 11:00 − 45 minutes = 10:15. Count back the drive: 10:15 − 15 minutes "
                  "= 10:00, and 20 more minutes back is <b>09:40</b>. (10:15 forgets the drive. 10:25 forgets the "
                  "45 minutes at the terminal. 12:20 adds instead of counting back.)")
    # SkyTrain
    q["s1"] = dur_q(ST + "How long does the train take from <b>Waterfront</b> to <b>Metrotown</b>?",
                    SKY[0][1], SKY[2][1], fmt=f24)
    q["s2"] = dur_q(ST + "How long is the whole ride, from <b>Waterfront</b> to <b>King George</b>?",
                    SKY[0][1], SKY[4][1], fmt=f24)
    q["s3"] = dur_q(ST + "How long does the train take from <b>Commercial–Broadway</b> to <b>New Westminster</b>?",
                    SKY[1][1], SKY[3][1], fmt=f24)
    nm = next(people)
    assert H(9, 45) - (SKY[4][1] + 12) == 7
    q["s4"] = mcq(ST + "%s gets off at <b>King George</b> and walks <b>12 minutes</b> to a swim meet that starts at "
                  "<b>09:45</b>. How many minutes early is %s?" % (nm[0], nm[1]), "7 minutes",
                  ["19 minutes", "31 minutes", "17 minutes"],
                  "The train gets to King George at 09:26. 09:26 + 12 minutes = 09:38. 09:38 to 09:45 is "
                  "<b>7 minutes</b>. (19 minutes forgets the walk. 31 minutes adds the walk instead of taking it away.)")
    nm = next(people)
    r = SKY[2][1] + 150 + (SKY[2][1] - SKY[0][1])
    assert f24(r) == "11:51"
    q["s5"] = mcq(ST + "%s takes this train from Waterfront to Metrotown. %s shops for <b>2 hours 30 minutes</b>, then "
                  "rides back to Waterfront. The ride back takes the same time. What time does %s get back?"
                  % (nm[0], nm[1].capitalize(), nm[1]), f24(r), ["11:34", "11:17", "12:08"],
                  "%s arrives at Metrotown at 09:04. Add 2 hours 30 minutes: 11:34. The ride takes 17 minutes "
                  "(08:47 to 09:04). 11:34 + 17 minutes = <b>11:51</b>, because 34 + 17 = 51. "
                  "(11:34 forgets the ride back. 11:17 starts the shopping at 08:47, before the train ride.)" % nm[0])
    # word problems
    q["w1"] = dur_q("One summer, a ferry on the Inside Passage leaves Port Hardy at <b>07:30</b> and arrives in "
                    "Prince Rupert at <b>23:30</b> the same day. How long is the trip?", H(7, 30), H(23, 30), fmt=f24,
                    extra=["4 hours"])
    q["w1"]["e"] += " (Not 4 hours: 23:30 is 11:30 p.m., not 11:30 a.m.)"
    assert 3 * 75 == 225
    q["w2"] = mcq("%s has hockey practice <b>3 times</b> a week. Each practice is <b>1 hour 15 minutes</b>. "
                  "How much practice is that in one week?" % next(people)[0], "3 hours 45 minutes",
                  ["3 hours 15 minutes", "1 hour 45 minutes", "4 hours 15 minutes"],
                  "3 × 1 hour = 3 hours. 3 × 15 minutes = 45 minutes. Together: <b>3 hours 45 minutes</b>. "
                  "(3 hours 15 minutes forgets to multiply the minutes by 3.)")
    assert 14 * 25 == 350 == 5 * 60 + 50
    q["w3"] = mcq("%s practises piano for <b>25 minutes</b> every day for <b>2 weeks</b>. How long is that in all?"
                  % next(people)[0], "5 hours 50 minutes",
                  ["3 hours 50 minutes", "2 hours 55 minutes", "50 minutes"],
                  "2 weeks = 14 days. 14 × 25 = 350 minutes. 5 × 60 = 300, and 350 − 300 = 50. So 350 minutes = "
                  "<b>5 hours 50 minutes</b>. (3 hours 50 minutes counts an hour as 100 minutes. "
                  "2 hours 55 minutes is only 1 week.)")
    assert 5 * (T(3, 0, "pm") - T(8, 45, "am")) == 31 * 60 + 15
    q["w4"] = mcq("School runs from <b>8:45 a.m.</b> to <b>3:00 p.m.</b>, 5 days a week. How long is %s at school "
                  "in one week?" % next(people)[0], "31 hours 15 minutes",
                  ["6 hours 15 minutes", "30 hours 15 minutes", "37 hours 30 minutes"],
                  "One day: 8:45 a.m. to 9:00 a.m. is 15 minutes, and 9:00 a.m. to 3:00 p.m. is 6 hours, so 6 hours "
                  "15 minutes. 5 days: 5 × 6 hours = 30 hours and 5 × 15 minutes = 75 minutes = 1 hour 15 minutes. "
                  "30 hours + 1 hour 15 minutes = <b>31 hours 15 minutes</b>. (6 hours 15 minutes is only one day. "
                  "30 hours 15 minutes forgets to multiply the minutes by 5.)")
    r = T(8, 45, "am") + 3 * 50 + 2 * 15
    assert f12(r) == "11:45 a.m."
    q["w5"] = mcq("At a soccer tournament, a team plays <b>3 games</b>. Each game lasts <b>50 minutes</b>, and there is "
                  "a <b>15-minute</b> break between games. The first game starts at <b>8:45 a.m.</b> "
                  "What time does the last game end?", f12(r), ["11:15 a.m.", "12:00 noon", "11:45 p.m."],
                  "Game 1: 8:45 to 9:35. Break: to 9:50. Game 2: to 10:40. Break: to 10:55. Game 3: to "
                  "<b>11:45 a.m.</b> There are only 2 breaks, because the breaks are between games. "
                  "(11:15 a.m. forgets the breaks. 12:00 noon adds 3 breaks.)", key=str)
    nm = next(people)
    q["w6"] = mcq("%s’s family camps at a provincial park from <b>Friday at 4:00 p.m.</b> to <b>Sunday at 11:00 a.m.</b> "
                  "How long is the camping trip?" % nm[0], "43 hours",
                  ["55 hours", "48 hours", "31 hours"],
                  "Friday 4:00 p.m. to Saturday 4:00 p.m. is 1 day = 24 hours. Saturday 4:00 p.m. to Sunday 4:00 a.m. is "
                  "12 hours, and on to 11:00 a.m. is 7 more. 24 + 12 + 7 = <b>43 hours</b>. "
                  "(55 hours reads 4:00 p.m. as 4:00 a.m. 31 hours uses 12 hours in a day.)")
    a, b = next(people), next(people)
    assert 95 - 85 == 10
    q["w7"] = mcq("%s’s swim practice is <b>1 hour 25 minutes</b>. %s’s swim practice is <b>95 minutes</b>. "
                  "Whose practice is longer, and by how much?" % (a[0], b[0]), "%s’s, by 10 minutes" % b[0],
                  ["%s’s, by 30 minutes" % a[0], "%s’s, by 10 minutes" % a[0], "%s’s, by 30 minutes" % b[0]],
                  "1 hour 25 minutes = 60 + 25 = 85 minutes. 95 − 85 = 10. So <b>%s’s</b> practice is longer, by "
                  "<b>10 minutes</b>. (%s’s by 30 minutes counts an hour as 100 minutes: 125 − 95 = 30.)" % (b[0], a[0]),
                  key=str)
    nm = next(people)
    q["w8"] = dur_q("%s’s family drives overnight from Prince George to Vancouver. They leave at <b>9:25 p.m.</b> and "
                    "arrive at <b>5:40 a.m.</b> How long is the drive?" % nm[0], T(9, 25, "pm"), T(5, 40, "am") + DAY,
                    note="The drive goes past 12 midnight. ")
    order = ["f1", "f2", "s1", "f3", "s2", "f4", "w2", "s3", "f5", "w1", "w7", "s4", "f6", "w3", "w8", "f7", "s5",
             "w5", "w4", "w6"]
    assert sorted(order) == sorted(q)
    return {"title": "Schedules and word problems: BC Ferries and SkyTrain", "items": [q[k] for k in order]}


# ============================================================ lesson
def body_html():
    a, b = T(10, 45, "am"), T(1, 20, "pm")
    c, d = H(22, 40), H(1, 15) + DAY
    return tidy(
        "<h2>Units of time</h2>"
        "<p>Time does not count in tens and hundreds. Learn these facts:</p>"
        + table(["Unit", "Is the same as"], [
            ["1 minute", "60 seconds"], ["1 hour", "60 minutes = 3600 seconds"], ["1 day", "24 hours = 1440 minutes"],
            ["1 week", "7 days = 168 hours"], ["1 year", "12 months = 52 weeks and 1 day = 365 days (366 in a leap year)"]]) +
        "<p>To change a bigger unit into a smaller one, <b>multiply</b>: 3 hours = 3 × 60 = 180 minutes. "
        "To change a smaller unit into a bigger one, take away groups: 210 minutes = 60 + 60 + 60 + 30 = "
        "3 hours 30 minutes.</p>"
        + ex("Example 1: conversion", "How many hours are in 3 days?", "1 day = 24 hours. 3 × 24 = 72.",
             "72 hours (not 36: a day is 24 hours, not 12)") +
        "<h2>Elapsed time: count on in jumps</h2>"
        "<p>Elapsed time is how much time passes from a start time to an end time. Draw an open time line. "
        "Jump to the next o’clock, then jump whole hours, then jump the minutes that are left. Add the jumps.</p>"
        "<figure class='sn-fig'>" + timeline_svg(a, b) +
        "<figcaption>From 10:45 a.m. to 1:20 p.m.: 15 minutes + 2 hours + 20 minutes = 2 hours 35 minutes. "
        "The time line goes past 12 noon, so a.m. changes to p.m.</figcaption></figure>"
        + ex("Example 2: across an hour", "Swimming is from 4:50 p.m. to 5:35 p.m. How long is it?",
             "4:50 to 5:00 is 10 minutes. 5:00 to 5:35 is 35 minutes. 10 + 35 = 45.",
             "45 minutes (not 85 minutes: 535 − 450 = 85 counts an hour as 100 minutes)") +
        "<h2>Finding the end time or the start time</h2>"
        "<p>To find an <b>end</b> time, add: first the hours, then the minutes. "
        "To find a <b>start</b> time, count <b>back</b>. At 12 noon, a.m. changes to p.m. At 12 midnight, p.m. "
        "changes to a.m. and a new day starts.</p>"
        + ex("Example 3: end time", "A movie starts at 6:50 p.m. and lasts 1 hour 35 minutes. When does it end?",
             add_e(T(6, 50, "pm"), 95), "8:25 p.m.") +
        ex("Example 4: start time", "A concert ends at 9:05 p.m. It lasted 1 hour 50 minutes. When did it start?",
           back_e(T(9, 5, "pm"), 110), "7:15 p.m.") +
        "<h2>24-hour time</h2>"
        "<p>Ferry and SkyTrain timetables often use 24-hour time. The hours go from 00 to 23, so there is no a.m. or p.m. "
        "For p.m. times, add 12 to the hour: 4:35 p.m. = 16:35. Count on in jumps the same way. "
        "After 23:59 the clock goes back to 00:00.</p>"
        "<figure class='sn-fig'>" + timeline_svg(c, d, f24) +
        "<figcaption>A flight from 22:40 to 01:15: 20 minutes + 2 hours + 15 minutes = 2 hours 35 minutes."
        "</figcaption></figure>"
        "<h2>Reading a timetable</h2>"
        "<p>Find the row for your trip, then read across. To find how long a trip takes, count on from the leaving time "
        "to the arriving time.</p>"
        "<figure class='sn-fig'>" + sky_svg() +
        "<figcaption>Waterfront 08:47 to Metrotown 09:04: 13 minutes to 09:00, then 4 more. "
        "The ride takes 17 minutes.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["08:47 to 09:04 worked out as 904 − 847 = 57 minutes", "An hour has 60 minutes, not 100. Count on: 13 + 4 = 17 minutes"],
            ["1 hour 15 minutes = 115 minutes", "1 hour = 60 minutes: 60 + 15 = 75 minutes"],
            ["11:25 a.m. + 55 minutes = 12:20 a.m.", "After 12 noon the time is p.m.: 12:20 p.m."],
            ["9:45 + 30 minutes = 9:15 (forgot the new hour)", "45 + 30 = 75 minutes = 1 hour 15 minutes, so it is 10:15"],
            ["16:35 read as 6:35 p.m.", "Take away 12: 16 − 12 = 4, so 4:35 p.m."],
            ["22:40 to 01:15 worked out as 22:40 − 01:15", "Count on past midnight: 20 minutes + 2 hours + 15 minutes"],
            ["3 days = 36 hours", "1 day = 24 hours, not 12: 3 × 24 = 72 hours"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about time in BC?",
     "a": "The BC Grade 5 math curriculum includes duration, using measurement of time. Students convert between "
          "units such as seconds, minutes, hours, days and weeks, and work out how long events last, including with "
          "12-hour and 24-hour times and real schedules."},
    {"q": "What is the easiest way to work out elapsed time?",
     "a": "Use an open time line and count on in jumps: to the next o’clock, then whole hours, then the minutes left. "
          "Adding the jumps is safer than subtracting the clock times."},
    {"q": "Why can’t you subtract times like ordinary numbers?",
     "a": "An hour has 60 minutes, not 100. So 09:04 − 08:47 is not 57 minutes; counting on gives 13 + 4 = 17 minutes."},
    {"q": "How do you find elapsed time across midnight?",
     "a": "Count on to midnight first, then from midnight to the end time, and add the two parts. "
          "From 10:40 p.m. to 1:15 a.m. is 1 hour 20 minutes + 1 hour 15 minutes = 2 hours 35 minutes."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5)."""
    for s in sets:
        targets = [p for p in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        targets = iter(targets)
        for it in s["items"]:
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
    rnd = random.Random(55812)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_units(rnd, people), set_elapsed(rnd, people), set_start_end(rnd, people), set_24(rnd, people),
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
                assert "\\" not in f
            k = re.sub("<svg.*?</svg>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "duration-of-time", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Duration of Time: Converting Units, Elapsed Time, 24-Hour Time and Schedules",
        "seo_title": "Grade 5 Math: Elapsed Time Worksheets (Free, BC Curriculum, Answer Key)",
        "short_title": "Duration of time",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 5: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Duration, using measurement of time",
        "meta_desc": "Free Grade 5 math worksheets on duration of time for the BC curriculum: convert seconds, minutes, "
                     "hours, days and weeks, find elapsed time across noon and midnight, work out start and end times, "
                     "use 24-hour time, and read BC Ferries and SkyTrain timetables. 100 questions with an answer key.",
        "key_big": "Count on in jumps: to the next o’clock, then whole hours, then the minutes left.",
        "key_sub": "1 hour = 60 minutes, not 100, so do not subtract clock times like ordinary numbers. "
                   "1 day = 24 hours and 1 week = 7 days. At noon a.m. changes to p.m.; at midnight a new day starts.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "time line")
    mark_large(u, "ferry timetable")
    mark_large(u, "SkyTrain timetable")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
