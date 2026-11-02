# -*- coding: utf-8 -*-
"""
British Columbia Grade 3 Math: Time (BC Mathematics Curriculum, Geometry and measurement: time concepts)
  python3 tools/gen_cabc_math_g3_time.py
Units of time from seconds to years, analog clocks to the 5 minutes and to the minute, a.m. and p.m.,
calendars (drawn from the real months of 2027 with the calendar module), and elapsed time word problems.
Every analog clock is drawn from the time itself (the hour hand moves between the numbers).
Every answer is worked out in code. Wrong answers come from real student mistakes:
hands swapped, an hour hand just before a number read as that number, the number the minute hand points to read
as minutes, a.m. and p.m. swapped, an hour counted as 100 minutes, a week counted as 10 days,
counting both the first and the last day, counting the numbers instead of the jumps.
Canadian English; times written 3:45 p.m. HTML attributes use single quotes (no backslashes in the JSON).
"""
import calendar, json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
SOFT = "#eef5f0"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Liam", "he"), ("Olivia", "she"), ("Ethan", "he"), ("Ava", "she"), ("Noah", "he"), ("Chloe", "she"),
          ("Arjun", "he"), ("Simran", "she"), ("Harjot", "he"), ("Jasleen", "she"), ("Wei", "he"), ("Mei", "she"),
          ("Ji-woo", "she"), ("Mateo", "he"), ("Hana", "she"), ("Lucas", "he"), ("Sofia", "she"), ("Kai", "he"),
          ("Emma", "she"), ("Owen", "he"), ("Leah", "she"), ("Ryan", "he"), ("Zara", "she"), ("Nadia", "she")]
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
SHORTD = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
Y = 2027


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
    assert all(X(b) - X(a) >= 90 for a, b in zip(pts, pts[1:])), (h1, m1, h2, m2)
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
        if (h, m) in used or hands_gap(h, m) < 15 or swapped(h, m) == dig(h, m):
            continue
        used.add((h, m))
        return h
    raise AssertionError(m)



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



# ------------------------------------------------------------ calendar helpers
def wd(m, d, y=Y):
    """Day name of a date (calendar.weekday: Monday = 0)."""
    return DAYS[(calendar.weekday(y, m, d) + 1) % 7]


def ndays(m, y=Y):
    return calendar.monthrange(y, m)[1]


def dt(m, d):
    return "%s %d" % (MONTHS[m], d)


def txt(x, y, t, fs=16, col=LINE, anchor="middle", bold=True):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def calendar_svg(month, box=None, circle=None, legend=(), year=Y):
    """Month calendar, weeks start on Sunday. box = green square, circle = red ring."""
    CW, RH, top = 46, 30, 62
    weeks = calendar.Calendar(6).monthdayscalendar(year, month)
    W = 7 * CW + 4
    gh = top + RH * len(weeks)
    widths = [30 + int(len(t) * 8) for k, t in legend]
    one_row = sum(widths) + 18 * (len(widths) - 1) + 8 <= W - 4
    H = gh + 4 + ((34 if one_row else 30 * len(legend) + 4) if legend else 0)
    s = ["<rect x='2' y='2' width='%d' height='32' fill='%s'/>" % (W - 4, GREEN),
         txt(W / 2.0, 25, "%s %d" % (MONTHS[month], year), 18, "#fff")]
    for i, d in enumerate(SHORTD):
        s.append(txt(2 + CW * i + CW / 2.0, 54, d, 14, RED if i in (0, 6) else GREEN))
    for r, wk in enumerate(weeks):
        y = top + RH * r
        if r % 2 == 0:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, RH, SOFT))
        for i, d in enumerate(wk):
            if not d:
                continue
            cx = 2 + CW * i + CW / 2.0
            assert wd(month, d, year) == DAYS[i]
            if d == box:
                s.append("<rect x='%.1f' y='%d' width='34' height='26' rx='4' fill='none' stroke='%s' stroke-width='3'/>"
                         % (cx - 17, y + 2, GREEN))
            if d == circle:
                s.append("<circle cx='%.1f' cy='%d' r='14' fill='none' stroke='%s' stroke-width='3'/>" % (cx, y + 15, RED))
            s.append(txt(cx, y + 21, str(d), 16))
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, gh - 2, LINE))
    if legend:
        y = gh + 22
        x = 8
        for kind, t in legend:
            if kind == "box":
                s.append("<rect x='%d' y='%d' width='22' height='18' rx='3' fill='none' stroke='%s' stroke-width='3'/>"
                         % (x, y - 14, GREEN))
            else:
                s.append("<circle cx='%d' cy='%d' r='10' fill='none' stroke='%s' stroke-width='3'/>" % (x + 11, y - 5, RED))
            s.append(txt(x + 30, y, t, 15, anchor="start", bold=False))
            assert x + 30 + len(t) * 8 <= W, legend
            if one_row:
                x += 30 + int(len(t) * 8) + 18
            else:
                y += 30
    return svg_wrap(W, H, "".join(s), "calendar for %s %d" % (MONTHS[month], year))


def cal(month, box=None, circle=None, legend=()):
    return fig(calendar_svg(month, box, circle, legend))


# ============================================================ set 1: units of time
def set_units(rnd, people):
    its = []
    its.append(mcq("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "30"],
                   "There are <b>60 seconds</b> in 1 minute. (Not 100: time does not count in hundreds.)"))
    its.append(mcq("How many <b>minutes</b> are in 1 hour?", "60", ["100", "24", "12"],
                   "There are <b>60 minutes</b> in 1 hour. The long hand goes once around the clock. "
                   "(Not 100: an hour is not like a hundred.)"))
    its.append(mcq("How many <b>hours</b> are in 1 day?", "24", ["12", "60", "7"],
                   "The short hand goes around the clock 2 times in a day: 12 + 12 = <b>24 hours</b>. "
                   "(12 is only half a day.)"))
    its.append(mcq("How many <b>days</b> are in 1 week?", "7", ["10", "5", "12"],
                   "Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday: <b>7 days</b>. "
                   "(5 is only the school days.)"))
    its.append(mcq("How many <b>months</b> are in 1 year?", "12", ["10", "52", "7"],
                   "January to December is <b>12 months</b>. (52 is the number of weeks in a year.)"))
    its.append(mcq("About how many <b>weeks</b> are in 1 year?", "52", ["12", "365", "100"],
                   "A year has 365 days. 52 weeks × 7 days = 364 days, so a year is about <b>52 weeks</b>. "
                   "(12 is the months and 365 is the days.)"))
    its.append(mcq("Put these in order from <b>shortest</b> to <b>longest</b>: hour, second, day, minute",
                   "second, minute, hour, day",
                   ["minute, second, hour, day", "day, hour, minute, second", "second, hour, minute, day"],
                   "A second is very short. 60 seconds make a minute, 60 minutes make an hour, and 24 hours make a day. "
                   "So the order is <b>second, minute, hour, day</b>."))
    its.append(mcq("Put these in order from <b>shortest</b> to <b>longest</b>: year, day, month, week",
                   "day, week, month, year",
                   ["week, day, month, year", "day, month, week, year", "year, month, week, day"],
                   "7 days make a week. About 4 weeks make a month. 12 months make a year. "
                   "So the order is <b>day, week, month, year</b>."))
    # best unit
    for thing, right, wrong, why in [
            ("a sneeze takes", "seconds", ["hours", "days", "months"], "A sneeze is over very fast"),
            ("it takes to brush your teeth", "minutes", ["hours", "days", "years"], "Brushing your teeth takes a few minutes"),
            ("a school day is", "hours", ["seconds", "weeks", "years"], "A school day is from the morning to the afternoon"),
            ("summer holidays in BC (July and August) are", "months", ["seconds", "minutes", "hours"],
             "July and August are 2 whole months")]:
        its.append(mcq("Which unit is best to measure how long %s?" % thing, right, wrong,
                       "%s, so we use <b>%s</b>." % (why, right)))
    # conversions
    its.append(mcq("<b>2 hours</b> = ? minutes", "120", ["200", "62", "24"],
                   "1 hour = 60 minutes. 2 hours = 60 + 60 = <b>120 minutes</b>. (Not 200: an hour is 60 minutes, not 100.)"))
    its.append(mcq("<b>3 weeks</b> = ? days", "21", ["30", "10", "37"],
                   "1 week = 7 days. 3 weeks = 7 + 7 + 7 = <b>21 days</b>. (30 counts a week as 10 days.)"))
    its.append(mcq("<b>2 days</b> = ? hours", "48", ["24", "26", "120"],
                   "1 day = 24 hours. 2 days = 24 + 24 = <b>48 hours</b>. (24 counts a day as 12 hours. 120 uses 60, but that is the minutes in an hour.)"))
    its.append(mcq("<b>1 hour 15 minutes</b> = ? minutes", "75", ["115", "65", "16"],
                   "1 hour = 60 minutes. 60 + 15 = <b>75 minutes</b>. (115 counts an hour as 100 minutes.)"))
    its.append(mcq("Which is the same as <b>90 minutes</b>?", "1 hour 30 minutes",
                   ["9 hours", "1 hour 10 minutes", "1 hour 90 minutes"],
                   "60 minutes make 1 hour. 90 − 60 = 30 minutes left. So 90 minutes = <b>1 hour 30 minutes</b>. "
                   "(1 hour 10 minutes would be 70 minutes.)"))
    its.append(mcq("Which is <b>longer</b>: 100 minutes or 2 hours?", "2 hours",
                   ["100 minutes", "They are the same.", "You cannot tell."],
                   "2 hours = 60 + 60 = 120 minutes. 120 minutes is more than 100 minutes, so <b>2 hours</b> is longer. "
                   "(An hour is 60 minutes, not 100.)"))
    nm, pr = next(people)
    its.append(mcq("%s’s Spring Break is <b>2 weeks</b> long. How many days is that?" % nm, "14 days",
                   ["20 days", "12 days", "9 days"],
                   "1 week = 7 days. 2 weeks = 7 + 7 = <b>14 days</b>. (20 counts a week as 10 days.)"))
    nm, pr = next(people)
    its.append(mcq("%s’s baby cousin is <b>18 months</b> old. How old is that in years and months?" % nm,
                   "1 year 6 months", ["1 year 8 months", "18 years", "2 years 6 months"],
                   "12 months make 1 year. 18 − 12 = 6 months left. So 18 months = <b>1 year 6 months</b>. "
                   "(1 year 8 months counts a year as 10 months.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 8, 9, 10, 11, 6, 7, 5, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Units of time: seconds to years", "items": [its[i] for i in order]}


# ============================================================ set 2: analog clocks to 5 minutes and to the minute
def set_clocks(rnd):
    its = []
    used = set()
    plan = [(0, "d"), (30, "d"), (15, "w"), (45, "w"), (5, "d"), (20, "d"), (40, "d"), (25, "d"), (35, "d"), (50, "d")]
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
            if m == 15:
                c = [words(h, 45), words(h, 3), words(h - 1, 15), words(h + 1, 45)]
                e = ("%s 15 minutes is a quarter of an hour. The long hand is on the right side, so we say <b>past</b>. "
                     "It is <b>%s</b>." % (hand_text(h, m), right))
            else:
                c = [words(h, 15), words(h + 1, 15), words(h - 1, 45), words(h, 9)]
                e = ("%s 45 minutes past %d is 15 minutes before %d o’clock. The long hand is on the left side, so we say "
                     "<b>to</b> the next hour: <b>%s</b>." % (hand_text(h, m), h12(h), h12(h + 1), right))
            q = fig(clock_svg(h, m)) + "What time does the clock show? Choose the words."
        its.append(mcq(q, right, c, e))
    # to the minute
    usedm = []

    def pick(lo, hi):
        while True:
            h = rnd.randint(1, 12)
            m = rnd.randint(lo, hi)
            if (m % 5 and (h, m) not in usedm and hands_gap(h, m) >= 18 and h not in [x[0] for x in usedm][-2:]
                    and (h, m // 5 * 5) not in used):
                usedm.append((h, m))
                return h, m

    for lo, hi in [(1, 14), (16, 29), (31, 44), (46, 59), (6, 24), (31, 44), (46, 59), (36, 54)]:
        h, m = pick(lo, hi)
        n = m // 5
        right = dig(h, m)
        c = []
        if m >= 30:
            c.append(dig(h + 1, m))
        if n:
            c.append(dig(h, n * 5))
            c.append(dig(h, n))
        c += [dig(h, 60 - m), dig(h, m + 1 if m % 5 != 4 else m - 1), dig(h + 1, m), dig(h - 1, m)]
        e = "%s So the time is <b>%s</b>." % (hand_text(h, m), right)
        if m >= 30:
            e += " (Not %s: the hour hand has not reached %d yet.)" % (dig(h + 1, m), h12(h + 1))
        elif n:
            e += " (Not %s: count the small marks after the %d too.)" % (dig(h, n * 5), n)
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show? Read it to the minute.", right, c, e))
    # which clock (A to D)
    pos = [0, 1, 2, 3]
    rnd.shuffle(pos)
    for (h, m), p in zip([(5, 38), (8, 13)], pos):
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
    assert len(its) == 20
    order = [0, 1, 4, 2, 5, 6, 3, 7, 8, 9, 10, 11, 12, 13, 18, 14, 15, 16, 19, 17]
    assert sorted(order) == list(range(20))
    return {"title": "Analog clocks to the 5 minutes and to the minute", "items": [its[i] for i in order]}


# ============================================================ set 3: a.m. and p.m.
CONTEXTS = [
    ("{n} wakes up in the morning.", 7, 2, 28),
    ("{n} rides the bus to school in the morning.", 8, 6, 24),
    ("{n} eats lunch at school.", 12, 6, 24),
    ("{n} goes to soccer practice after school.", 16, 6, 28),
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
    its.append(mcq("Which is a sensible time for school to start?", "8:40 a.m.", ["8:40 p.m.", "3:40 a.m.", "11:40 p.m."],
                   "School starts in the morning, so it is an <b>a.m.</b> time. 3:40 a.m. is the middle of the night. "
                   "So the answer is <b>8:40 a.m.</b>"))
    nm, pr = next(people)
    its.append(mcq("%s eats breakfast at 7:15 in the morning. Is that a.m. or p.m.?" % nm,
                   "a.m., because it is before noon",
                   ["p.m., because it is before noon", "p.m., because it is after noon", "a.m., because it is after noon"],
                   "Morning times are before noon. Times before noon are <b>a.m.</b> times. So breakfast is at 7:15 a.m."))
    its.append(mcq("Which is earlier in the same day: <b>11:50 a.m.</b> or <b>1:10 p.m.</b>?", "11:50 a.m.",
                   ["1:10 p.m.", "They are the same time.", "You cannot tell."],
                   "a.m. times come before noon and p.m. times come after noon. So <b>11:50 a.m.</b> is earlier, "
                   "even though 11 is bigger than 1."))
    ctx = CONTEXTS[:]
    rnd.shuffle(ctx)
    for sent, H, lo, hi in ctx:
        ms = [x for x in range(lo, hi + 1) if x % 5 and hands_gap(H, x) >= 15]
        m = rnd.choice(ms)
        n = m // 5
        nm, pr = next(people)
        right = tm12(H, m)
        c = [tm12(H + 12, m)]
        if n:
            c.append(tm12(H, n))
        c += [tm12(H + 1, m), tm12(H, 60 - m), tm12(H - 1, m)]
        why = "It is in the morning, so it is <b>a.m.</b>" if H < 12 else "It is after noon, so it is <b>p.m.</b>"
        e = "%s %s So the time is <b>%s</b>" % (hand_text(H, m), why, right)
        hh = (H + 12) % 24
        e += " (Not %s: that is %s.)" % (c[0], "in the middle of the night" if hh < 6 else
                                          ("in the afternoon or evening" if hh >= 12 else "in the morning"))
        q = fig(clock_svg(H, m)) + sent.format(n=nm) + " What is the time?"
        its.append(mcq(q, right, c, e))
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
    its.append(mcq("How many hours is it from <b>9:00 a.m.</b> to <b>noon</b>?", "3 hours",
                   ["4 hours", "2 hours", "9 hours"],
                   "Count the jumps, not the numbers: 9:00 → 10:00 → 11:00 → 12:00 noon. That is <b>3 hours</b>. "
                   "(4 counts the numbers 9, 10, 11 and 12.)"))
    its.append(mcq("How many hours is it from <b>11:00 a.m.</b> to <b>2:00 p.m.</b>?", "3 hours",
                   ["9 hours", "2 hours", "13 hours"],
                   "11:00 a.m. → 12:00 noon is 1 hour. 12:00 noon → 2:00 p.m. is 2 hours. 1 + 2 = <b>3 hours</b>. "
                   "(Not 9 hours: 11 − 2 = 9 does not work across noon.)"))
    its.append(mcq("Put these times in order from <b>earliest</b> to <b>latest</b> in one day: "
                   "3:00 p.m., 7:00 a.m., 9:30 p.m., 11:00 a.m.",
                   "7:00 a.m., 11:00 a.m., 3:00 p.m., 9:30 p.m.",
                   ["3:00 p.m., 7:00 a.m., 9:30 p.m., 11:00 a.m.", "11:00 a.m., 9:30 p.m., 7:00 a.m., 3:00 p.m.",
                    "7:00 a.m., 3:00 p.m., 9:30 p.m., 11:00 a.m."],
                   "All a.m. times come first, then the p.m. times. a.m.: 7:00, then 11:00. p.m.: 3:00, then 9:30. "
                   "So the order is <b>7:00 a.m., 11:00 a.m., 3:00 p.m., 9:30 p.m.</b>"))
    its.append(mcq("A digital clock shows <b>4:37 p.m.</b> How many minutes is it until 5:00 p.m.?", "23 minutes",
                   ["63 minutes", "37 minutes", "13 minutes"],
                   "An hour has 60 minutes. It is 37 minutes past 4. 60 − 37 = <b>23 minutes</b> until 5:00 p.m. "
                   "(Not 63: that uses 100 − 37, but an hour is 60 minutes, not 100.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 12, 7, 13, 8, 14, 9, 15, 10, 11, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "a.m. and p.m.", "items": [its[i] for i in order]}


# ============================================================ set 4: calendars
def nth(n):
    return {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth"}[n]


def set_calendar(rnd, people):
    its = []
    # September 2027
    S = 9
    first = 7
    tf = 23
    assert wd(S, 1) == "Wednesday" and wd(S, first) == "Tuesday" and wd(S, tf) == "Thursday"
    its.append(mcq(cal(S) + "What day of the week is <b>September 1, 2027</b>?", wd(S, 1),
                   ["Sunday", "Tuesday", "Thursday"],
                   "Find the 1 on the calendar. Look up its column to the day name: <b>%s</b>. "
                   "(Not Sunday: the month does not always start in the first column.)" % wd(S, 1)))
    nm, pr = next(people)
    its.append(mcq(cal(S, box=first, legend=[("box", "first day of school")]) +
                   "The green box is %s’s first day of school. What day of the week is it?" % nm, wd(S, first),
                   ["Monday", "Wednesday", "Sunday"],
                   "The box is around the 7. Look up the column: it is a <b>%s</b>. So the first day of school is "
                   "Tuesday, September 7." % wd(S, first)))
    nm, pr = next(people)
    its.append(mcq(cal(S, circle=tf, legend=[("circle", "Terry Fox Run")]) +
                   "%s’s school has its Terry Fox Run on the circled day. What is the date?" % nm,
                   "Thursday, September 23", ["Wednesday, September 23", "Thursday, September 22", "Friday, September 24"],
                   "The red circle is around the 23. Look up the column: it is a Thursday. So the date is "
                   "<b>Thursday, September 23</b>."))
    weds = [d for d in range(1, ndays(S) + 1) if wd(S, d) == "Wednesday"]
    assert len(weds) == 5
    its.append(mcq(cal(S) + "How many <b>Wednesdays</b> are in September 2027?", "5", ["4", "7", "6"],
                   "Look down the Wed column: %s. That is <b>5 Wednesdays</b>. (Many months have 4, but count to be sure.)"
                   % ", ".join(str(d) for d in weds)))
    d = tf - first
    assert d == 16
    its.append(mcq(cal(S, box=first, circle=tf, legend=[("box", "first day"), ("circle", "Terry Fox Run")]) +
                   "How many days is it from the first day of school to the Terry Fox Run?", "16 days",
                   ["17 days", "23 days", "14 days"],
                   "Count the jumps from 7 to 23: 23 − 7 = <b>16 days</b>. That is 2 weeks (to the 21st) and 2 more days. "
                   "(17 counts the first day too. 23 is just the date.)"))
    # no picture
    assert wd(10, 4) == "Monday" and wd(10, 11) == "Monday"
    its.append(mcq("Today is <b>Monday, October 4</b>. What is the date <b>1 week</b> from today?", "October 11",
                   ["October 14", "October 10", "October 5"],
                   "1 week is 7 days. 4 + 7 = 11, so it is <b>Monday, October 11</b>. (October 14 counts a week as 10 days.)"))
    its.append(mcq("Today is <b>Wednesday</b>. What day will it be in <b>3 days</b>?", "Saturday",
                   ["Friday", "Sunday", "Tuesday"],
                   "Count 3 jumps: Wednesday → Thursday → Friday → <b>Saturday</b>. (Friday counts today as one of the days.)"))
    thirty = [m for m in range(1, 13) if ndays(m) == 30]
    assert 4 in thirty and all(ndays(m) == 31 for m in (3, 7, 8))
    its.append(mcq("Which month has <b>30 days</b>?", "April", ["March", "July", "August"],
                   "April, June, September and November have 30 days. March, July and August have 31 days. "
                   "So the answer is <b>April</b>."))
    assert ndays(2) == 28
    its.append(mcq("How many days are in <b>February 2027</b>?", "28", ["30", "31", "29"],
                   "February is the shortest month. In 2027 it has <b>28 days</b>. (It has 29 days only in a leap year, "
                   "such as 2028.)"))
    assert calendar.isleap(2028) and not calendar.isleap(2027)
    nm, pr = next(people)
    its.append(mcq("%s’s birthday is on the <b>last day of June</b>. What is the date?" % nm, "June 30",
                   ["June 31", "July 1", "June 29"],
                   "June has 30 days, so the last day of June is <b>June 30</b>. (There is no June 31. July 1 is Canada Day, "
                   "the next day.)"))
    assert ndays(6) == 30
    its.append(mcq("Which month comes <b>3 months after November</b>?", "February", ["January", "March", "August"],
                   "Count 3 jumps: November → December → January → <b>February</b>. (January counts November as one "
                   "of the months.)"))
    assert wd(7, 1) == "Thursday"
    its.append(mcq(cal(7, circle=1, legend=[("circle", "Canada Day")]) +
                   "Canada Day is July 1. What day of the week is Canada Day in 2027?", "Thursday",
                   ["Sunday", "Wednesday", "Friday"],
                   "Find the 1 and look up its column: <b>Thursday</b>. (Not Sunday: the first column is not always the 1st.)"))
    mons = [d for d in range(1, 32) if wd(8, d) == "Monday"]
    assert mons[0] == 2
    its.append(mcq(cal(8) + "<b>BC Day</b> is a holiday on the first Monday in August. What is the date of BC Day in 2027?",
                   "August 2", ["August 1", "August 9", "August 30"],
                   "Look down the Mon column. The first Monday is the 2nd. So BC Day is <b>Monday, August 2</b>. "
                   "(August 1 is a Sunday. August 9 is the second Monday.)"))
    assert wd(3, 15) == "Monday" and wd(3, 29) == "Monday"
    nm, pr = next(people)
    its.append(mcq(cal(3, box=15, legend=[("box", "Spring Break starts")]) +
                   "%s’s Spring Break starts on Monday, March 15. It is <b>2 weeks</b> long. "
                   "On what date does %s go back to school?" % (nm, pr),
                   "Monday, March 29", ["Monday, March 22", "Tuesday, March 30", "Thursday, March 25"],
                   "Each row of the calendar is 1 week. Go down 2 rows from the 15: 15 + 7 + 7 = 29. School starts again on "
                   "<b>Monday, March 29</b>. (March 22 is only 1 week later. March 25 counts a week as 5 days.)"))
    mons10 = [d for d in range(1, 32) if wd(10, d) == "Monday"]
    tg = mons10[1]
    assert tg == 11
    its.append(mcq(cal(10, circle=tg, box=31, legend=[("circle", "Thanksgiving"), ("box", "Halloween")]) +
                   "Thanksgiving is Monday, October 11. Halloween is October 31. How many days is it from Thanksgiving "
                   "to Halloween?", "20 days", ["21 days", "31 days", "19 days"],
                   "Count the jumps from 11 to 31: 31 − 11 = <b>20 days</b>. (21 counts Thanksgiving too.)"))
    nm, pr = next(people)
    assert wd(5, 1) == "Saturday" and wd(5, 15) == "Saturday"
    its.append(mcq(cal(5, circle=1, legend=[("circle", "first game")]) +
                   "%s has a soccer game every Saturday. The first game is May 1. What is the date of the "
                   "<b>third</b> game?" % nm, "May 15", ["May 22", "May 8", "May 3"],
                   "The games are 1 week apart. First game: May 1. Second: May 8. Third: <b>May 15</b>. "
                   "(May 22 adds 3 weeks to the first game, but that is the fourth game.)"))
    assert wd(10, 6) == "Wednesday" and wd(10, 27) == "Wednesday"
    nm, pr = next(people)
    its.append(mcq("%s borrows a library book on <b>Wednesday, October 6</b>. It is due in <b>3 weeks</b>. "
                   "What is the due date?" % nm, "Wednesday, October 27",
                   ["Saturday, October 9", "Tuesday, October 26", "Wednesday, October 20"],
                   "3 weeks = 7 + 7 + 7 = 21 days. 6 + 21 = 27. The book is due on <b>Wednesday, October 27</b>. "
                   "(October 9 adds 3 days, not 3 weeks. October 20 is only 2 weeks.)"))
    its.append(mcq("June has 30 days. How many <b>weeks and days</b> is that?", "4 weeks 2 days",
                   ["3 weeks", "4 weeks", "5 weeks"],
                   "4 weeks = 4 × 7 = 28 days. 30 − 28 = 2 days left. So 30 days = <b>4 weeks 2 days</b>. "
                   "(3 weeks counts a week as 10 days.)"))
    nm, pr = next(people)
    assert wd(7, 9) == "Friday" and wd(7, 12) == "Monday"
    its.append(mcq("%s’s family goes camping in the Okanagan. They arrive on <b>Friday, July 9</b> and go home on "
                   "<b>Monday, July 12</b>. How many nights do they sleep in the tent?" % nm, "3 nights",
                   ["4 nights", "2 nights", "12 nights"],
                   "Count the jumps: Friday night, Saturday night and Sunday night. 12 − 9 = <b>3 nights</b>. "
                   "(4 counts the days Friday, Saturday, Sunday and Monday.)"))
    its.append(mcq("Which is the <b>longest</b> time?", "1 year", ["11 months", "50 weeks", "300 days"],
                   "1 year = 12 months = about 52 weeks = 365 days. 11 months, 50 weeks and 300 days are all a bit less. "
                   "So the longest is <b>1 year</b>."))
    assert len(its) == 20
    order = [0, 5, 6, 1, 7, 2, 8, 3, 9, 11, 10, 12, 4, 13, 17, 14, 15, 16, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Calendars: days, weeks and months", "items": [its[i] for i in order]}


# ============================================================ set 5: elapsed time word problems
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
            if 0 < naive < 100 and naive != d:
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
    its.append(how_long("%s starts the Terry Fox Run at <b>1:15 p.m.</b> %s finishes at <b>1:52 p.m.</b> "
                        "How long does %s take?" % (nm, pr.capitalize(), pr), 13, 15, 13, 52))
    its.append(how_long("Math class is from <b>9:00 a.m.</b> to <b>10:00 a.m.</b> How long is math class?", 9, 0, 10, 0, "clocks"))
    nm, pr = next(people)
    its.append(how_long("%s’s family hikes in Stanley Park from <b>1:00 p.m.</b> to <b>3:00 p.m.</b> How long is the hike?"
                        % nm, 13, 0, 15, 0))
    its.append(how_long("The bus for the field trip to Science World leaves at <b>9:35 a.m.</b> It gets there at "
                        "<b>10:20 a.m.</b> How long is the bus ride?", 9, 35, 10, 20, "line"))
    nm, pr = next(people)
    its.append(how_long("%s rides the SkyTrain from <b>3:45 p.m.</b> to <b>4:10 p.m.</b> How long is the ride?" % nm,
                        15, 45, 16, 10, "line"))
    nm, pr = next(people)
    its.append(how_long("%s’s swimming lesson is from <b>4:45 p.m.</b> to <b>5:20 p.m.</b> How long is it?" % nm,
                        16, 45, 17, 20))
    its.append(how_long("A hockey game starts at <b>6:30 p.m.</b> and ends at <b>8:00 p.m.</b> How long is the game?",
                        18, 30, 20, 0, "line"))
    its.append(how_long("A BC Ferries boat leaves Tsawwassen at <b>11:00 a.m.</b> It gets to Swartz Bay on Vancouver Island "
                        "at <b>12:35 p.m.</b> How long is the trip?", 11, 0, 12, 35))
    nm, pr = next(people)
    its.append(how_long("%s’s lacrosse practice is from <b>5:30 p.m.</b> to <b>6:50 p.m.</b> How long is practice?" % nm,
                        17, 30, 18, 50, "line"))
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
                   "(6:35 p.m. is 25 minutes <b>after</b> 6:10. 5:35 p.m. is 35 minutes before.)"))
    assert add(9, 20, 95) == (10, 55)
    its.append(mcq("A BC Ferries boat leaves at <b>9:20 a.m.</b> The trip takes <b>1 hour 35 minutes</b>. "
                   "What time does the boat arrive?", "10:55 a.m.", ["10:55 p.m.", "9:55 a.m.", "11:15 a.m."],
                   "Add 1 hour: 9:20 a.m. → 10:20 a.m. Then add 35 minutes: 20 + 35 = 55. The boat arrives at "
                   "<b>10:55 a.m.</b> (9:55 a.m. forgets the 1 hour.)"))
    assert (15 * 60) - (8 * 60 + 45) == 375
    its.append(mcq("School starts at <b>8:45 a.m.</b> and ends at <b>3:00 p.m.</b> How long is the school day?",
                   "6 hours 15 minutes", ["5 hours 15 minutes", "7 hours 15 minutes", "6 hours 45 minutes"],
                   "8:45 a.m. to 2:45 p.m. is 6 hours. 2:45 p.m. to 3:00 p.m. is 15 more minutes. So the school day is "
                   "<b>6 hours 15 minutes</b>. (Not 7 hours 15 minutes: 8:45 a.m. to 3:45 p.m. would be 7 hours, and school ends before 3:45.)",
                   key=dur_value))
    assert add(17, 50, 25) == (18, 15)
    nm, pr = next(people)
    its.append(mcq("%s’s dad puts salmon in the oven at <b>5:50 p.m.</b> It bakes for <b>25 minutes</b>. "
                   "What time is it ready?" % nm, "6:15 p.m.", ["6:25 p.m.", "6:15 a.m.", "6:05 p.m."],
                   "From 5:50 p.m., 10 minutes takes you to 6:00 p.m. 25 − 10 = 15 more minutes makes <b>6:15 p.m.</b> "
                   "(6:25 p.m. adds 25 minutes to 6:00 instead of to 5:50.)"))
    a, b = next(people), next(people)
    its.append(mcq("%s’s movie is <b>1 hour 30 minutes</b> long. %s’s movie is <b>95 minutes</b> long. "
                   "Whose movie is longer, and by how much?" % (a[0], b[0]), "%s’s, by 5 minutes" % b[0],
                   ["%s’s, by 5 minutes" % a[0], "%s’s, by 35 minutes" % a[0], "%s’s, by 65 minutes" % b[0]],
                   "1 hour 30 minutes = 60 + 30 = 90 minutes. 95 − 90 = 5. So <b>%s’s</b> movie is longer, by <b>5 minutes</b>. "
                   "(Not %s’s by 35: that counts an hour as 100 minutes.)" % (b[0], a[0])))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 12, 6, 7, 8, 14, 13, 9, 10, 11, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Elapsed time word problems", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Units of time</h2>"
        "<p>We measure time with seconds, minutes, hours, days, weeks, months and years. "
        "Time does <b>not</b> count in tens or hundreds. Learn these facts:</p>"
        + table(["Unit", "Is the same as"], [["1 minute", "60 seconds"], ["1 hour", "60 minutes"], ["1 day", "24 hours"],
                                           ["1 week", "7 days"], ["1 year", "12 months, about 52 weeks, 365 days"]]) +
        "<p>Short things, like a sneeze, take seconds. A school day takes hours. Summer holidays take months.</p>"
        "<h2>Read an analog clock</h2>"
        "<p>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "Each number is <b>5 minutes</b> for the long hand, so count by 5s. "
        "Between two numbers there are 5 small marks, one for each minute.</p>"
        "<figure class='sn-fig'>" + clock_svg(8, 37, size=230) +
        "<figcaption>The long hand is 2 marks past the 7: count 5, 10, … 35, then 36, 37. The short hand is between 8 and 9. "
        "It has not reached 9 yet, so the hour is 8. It is <b>8:37</b>.</figcaption></figure>"
        + table(["Digital", "We say"], [["4:15", "quarter past 4"], ["4:30", "half past 4"], ["4:45", "quarter to 5"],
                                        ["4:50", "10 to 5"]]) +
        "<h2>a.m. and p.m.</h2>"
        "<p><b>a.m.</b> is from midnight to noon (night and morning). <b>p.m.</b> is from noon to midnight "
        "(afternoon and evening).</p>"
        + ex("a.m. or p.m.?", "Ava eats breakfast at 25 to 8. Write the time.",
             "25 to 8 is 35 minutes past 7. Breakfast is in the morning, so it is a.m.", "7:35 a.m.") +
        "<h2>Read a calendar</h2>"
        "<p>Each row of a calendar is <b>1 week</b>. Look up a column to find the day of the week. "
        "To count days, count the jumps. Do not count the first day.</p>"
        "<figure class='sn-fig'>" + calendar_svg(9, box=7, circle=23,
                                                  legend=[("box", "first day"), ("circle", "Terry Fox Run")]) +
        "<figcaption>From Tuesday, September 7 to Thursday, September 23 is 23 − 7 = <b>16 days</b>. "
        "One row down is 7 days later.</figcaption></figure>"
        + ex("Days in a month", "How many days are in November?",
             "April, June, September and November have 30 days. February has 28 (29 in a leap year). The rest have 31.",
             "30 days") +
        "<h2>Elapsed time: how long?</h2>"
        "<p>An hour has 60 minutes, not 100. Jump to the next o’clock first, then on to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(11, 45, 12, 20) +
        "<figcaption>Lunch from 11:45 a.m. to 12:20 p.m.: 15 minutes to 12:00 noon, then 20 more minutes. "
        "15 + 20 = 35 minutes.</figcaption></figure>"
        + ex("Find the end time", "A ferry leaves at 9:20 a.m. The trip takes 1 hour 35 minutes. When does it arrive?",
             "Add 1 hour: 10:20 a.m. Add 35 minutes: 20 + 35 = 55.", "10:55 a.m.") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Swapping the hands: reading 8:35 as 7:40", "The short hand is the hour. The long hand is the minutes"],
            ["Short hand just before 9 read as 9:35", "The short hand has not reached 9 yet, so the hour is still 8: 8:35"],
            ["Long hand on 4 read as 4 minutes", "Each number is 5 minutes: 4 × 5 = 20 minutes"],
            ["10:50 to 11:20 worked out as 1120 − 1050 = 70 minutes", "An hour has 60 minutes, not 100. Count on: 10 + 20 = 30 minutes"],
            ["Counting the first day: May 4 to May 6 is 3 days", "Count the jumps: 6 − 4 = 2 days"],
            ["Breakfast at 7:30 p.m.", "Morning times are a.m.: 7:30 a.m."],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about time in BC?",
     "a": "The BC Grade 3 math curriculum lists time concepts under Geometry and measurement. Students learn units of time from seconds to years, read clocks, use a.m. and p.m., read calendars and work out how long events last."},
    {"q": "How many days are in each month?",
     "a": "April, June, September and November have 30 days. February has 28 days, or 29 in a leap year. All the other months have 31 days."},
    {"q": "What is the difference between a.m. and p.m.?",
     "a": "a.m. times are from midnight to noon (night and morning). p.m. times are from noon to midnight (afternoon and evening), so school starts at an a.m. time and dinner is at a p.m. time."},
    {"q": "How can I help my child learn to tell time?",
     "a": "Keep an analog clock and a wall calendar at home. Ask the time at everyday moments like breakfast and bedtime, count the days to a birthday together, and practise counting by 5s around the clock."},
]


def gen():
    rnd = random.Random(53808)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_units(rnd, people), set_clocks(rnd), set_ampm(rnd, people), set_calendar(rnd, people),
            set_elapsed(rnd, people)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    qs = [it["q"] for s in sets for it in s["items"]]
    dup = [q for q in qs if qs.count(q) > 1]
    assert not dup, [re.sub("<svg.*?</svg>", "[svg]", q) for q in dup]
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "time", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Time: Units of Time, Clocks, a.m. and p.m., Calendars and Elapsed Time",
        "seo_title": "Grade 3 Time Worksheets: Clocks, Calendars and Elapsed Time (Free, BC Curriculum)",
        "short_title": "Time",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 3: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Time concepts",
        "meta_desc": "Free Grade 3 math worksheets on time for the BC curriculum: units of time from seconds to years, reading analog clocks to the 5 minutes and to the minute, a.m. and p.m., calendars, and elapsed time word problems. 100 questions with an answer key.",
        "key_big": "1 hour = 60 minutes, not 100. Short hand: the hour. Long hand: count by 5s, then by 1s.",
        "key_sub": "1 minute = 60 seconds, 1 day = 24 hours, 1 week = 7 days, 1 year = 12 months. If the short hand has not reached a number yet, it is still the hour before. On a calendar, count the jumps, not the first day.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    for p in ("time line", "four analog clocks", "start and end clocks", "calendar for"):
        mark_large(u, p)
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
