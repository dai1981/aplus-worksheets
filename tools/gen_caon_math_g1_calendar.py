# -*- coding: utf-8 -*-
"""
CA-ON Grade 1 Math: The calendar: days, weeks and months (Ontario Curriculum 2020, E2.3)
  python3 tools/gen_caon_math_g1_calendar.py
Days of the week in order (yesterday, today, tomorrow), months and the seasons in Canada, reading a calendar
page, counting days on a calendar, and Canadian holidays (Canada Day, Thanksgiving, Family Day).
Every calendar is drawn from the real month in 2027 (weeks start on Sunday, as on most Canadian calendars).
Every date, day and count is worked out in code with the calendar module.
Wrong answers come from real mistakes: Monday after Saturday (a new week does not start with Monday),
counting today as one of the days, yesterday and tomorrow mixed up, the date in the row above or below,
every month starting on the first column, US Thanksgiving in November, and summer in January.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import calendar, json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
SOFT = "#eef5f0"
FONT = "Arial, Helvetica, sans-serif"
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
SHORTD = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
SHORT = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
SEASONS = [("Winter", [12, 1, 2], "#9cc3e6"), ("Spring", [3, 4, 5], "#a8d08d"),
           ("Summer", [6, 7, 8], "#f6c26b"), ("Fall", [9, 10, 11], "#e9a27a")]
Y = 2027


def wd(m, d, y=Y):
    """Day name of a date (calendar.weekday: Monday = 0)."""
    return DAYS[(calendar.weekday(y, m, d) + 1) % 7]


def dt(m, d):
    return "%s %d" % (MONTHS[m], d)


def season_of(m):
    return next(n for n, ms, c in SEASONS if m in ms)


def nxt(day, n):
    return DAYS[(DAYS.index(day) + n) % 7]


def nxm(m, n):
    return MONTHS[(m - 1 + n) % 12 + 1]


def ndays(m, y=Y):
    return calendar.monthrange(y, m)[1]


def dates_on(m, day):
    return [d for d in range(1, ndays(m) + 1) if wd(m, d) == day]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
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


def txt(x, y, t, fs=16, col=LINE, anchor="middle", bold=True):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ pictures
def strip_svg(labels, label):
    """A row of boxes (days, months or dates). None is drawn as a red ?."""
    longest = max(len(x) for x in labels if x)
    bw = max(64, 11 * longest + 22)
    gap, H = 10, 50
    W = len(labels) * bw + (len(labels) - 1) * gap + 4
    s = []
    for i, t in enumerate(labels):
        x = 2 + i * (bw + gap)
        if t is None:
            s.append("<rect x='%d' y='2' width='%d' height='%d' rx='8' fill='#fde8e6' stroke='%s' stroke-width='2'/>"
                     % (x, bw, H - 4, RED))
            s.append(txt(x + bw / 2.0, 33, "?", 24, RED))
        else:
            s.append("<rect x='%d' y='2' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, bw, H - 4, SOFT, GREEN))
            s.append(txt(x + bw / 2.0, 31, t, 17))
    return svg_wrap(W, H, "".join(s), label)


def week_svg(missing=None, marks=None, shade=()):
    """The 7 days Sun..Sat in one row. missing: index drawn as ?. marks: {index: word under the box}.
    shade: indexes filled green."""
    marks = marks or {}
    bw, gap, bh = 54, 6, 44
    W = 7 * bw + 6 * gap + 4
    H = bh + 4 + (28 if marks else 0)
    s = []
    for i in range(7):
        x = 2 + i * (bw + gap)
        cx = x + bw / 2.0
        if i == missing:
            s.append("<rect x='%d' y='2' width='%d' height='%d' rx='7' fill='#fde8e6' stroke='%s' stroke-width='2'/>"
                     % (x, bw, bh, RED))
            s.append(txt(cx, 32, "?", 22, RED))
            continue
        fill = "#bfe0c9" if i in shade else SOFT
        s.append("<rect x='%d' y='2' width='%d' height='%d' rx='7' fill='%s' stroke='%s' stroke-width='%s'/>"
                 % (x, bw, bh, fill, GREEN, "3.5" if i in marks else "2"))
        s.append(txt(cx, 30, SHORTD[i], 16, RED if i in (0, 6) else LINE))
    for i, word in marks.items():
        cx = 2 + i * (bw + gap) + bw / 2.0
        half = len(word) * 4.4
        cx = min(max(cx, half + 2), W - half - 2)
        s.append(txt(cx, bh + 26, word, 15, GREEN))
    lab = "the 7 days of the week from Sunday to Saturday"
    if missing is not None:
        lab += ", one day is missing"
    for i, word in sorted(marks.items()):
        lab += ", %s is %s" % (DAYS[i], word)
    return svg_wrap(W, H, "".join(s), lab)


def grid_svg(n, rows):
    """Week rows (Sun..Sat). The first n boxes are filled. Used to count days in weeks."""
    cw, rh, top = 46, 34, 26
    W = 7 * cw + 4
    H = top + rows * rh + 4
    s = []
    for i in range(7):
        s.append(txt(2 + i * cw + cw / 2.0, 19, SHORTD[i], 14, RED if i in (0, 6) else GREEN))
    k = 0
    for r in range(rows):
        for i in range(7):
            x, y = 2 + i * cw, top + r * rh
            on = k < n
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, "#bfe0c9" if on else "#fff", LINE))
            if on:
                s.append("<circle data-d='1' cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (x + cw / 2.0, y + rh / 2.0, GREEN))
            k += 1
    svg = svg_wrap(W, H, "".join(s), "calendar weeks with %d days coloured" % n)
    assert svg.count("data-d='1'") == n
    return svg


def months_svg(missing=None, mark=None):
    """All 12 months in two rows of 6; the missing one is a red ?, the marked one has a thick border."""
    bw, bh, gap = 62, 40, 8
    W = 6 * bw + 5 * gap + 4
    H = 2 * bh + gap + 4
    s = []
    for m in range(1, 13):
        r, c = divmod(m - 1, 6)
        x, y = 2 + c * (bw + gap), 2 + r * (bh + gap)
        if m == missing:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='7' fill='#fde8e6' stroke='%s' stroke-width='2'/>"
                     % (x, y, bw, bh, RED))
            s.append(txt(x + bw / 2.0, y + 28, "?", 22, RED))
        else:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='7' fill='%s' stroke='%s' stroke-width='%s'/>"
                     % (x, y, bw, bh, "#bfe0c9" if m == mark else SOFT, GREEN, "3.5" if m == mark else "2"))
            s.append(txt(x + bw / 2.0, y + 26, SHORT[m], 17))
    return svg_wrap(W, H, "".join(s), "the 12 months of the year in order")


def seasons_svg(miss_season=None, miss_month=None):
    """The year in Canada from December: winter, spring, summer, fall. Each season has 3 months."""
    bw, bh, gap, ggap = 46, 36, 4, 14
    gw = 3 * bw + 2 * gap
    W = 4 * gw + 3 * ggap + 4
    H = bh + 40
    s = []
    for g, (name, ms, col) in enumerate(SEASONS):
        gx = 2 + g * (gw + ggap)
        for i, m in enumerate(ms):
            x = gx + i * (bw + gap)
            if m == miss_month:
                s.append("<rect x='%d' y='2' width='%d' height='%d' rx='6' fill='#fff' stroke='%s' stroke-width='2'/>"
                         % (x, bw, bh, RED))
                s.append(txt(x + bw / 2.0, 28, "?", 22, RED))
            else:
                s.append("<rect x='%d' y='2' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x, bw, bh, col, LINE))
                s.append(txt(x + bw / 2.0, 26, SHORT[m], 16))
        if name == miss_season:
            s.append(txt(gx + gw / 2.0, bh + 30, "?", 20, RED))
        else:
            s.append(txt(gx + gw / 2.0, bh + 29, name, 17))
    return svg_wrap(W, H, "".join(s), "the four seasons in Canada")


def month_card_svg(m):
    """A calendar page with the month name on top and a small grid below."""
    W, H = 150, 112
    s = ["<rect x='3' y='10' width='%d' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (W - 6, H - 13, LINE),
         "<path d='M3 18 a8 8 0 0 1 8 -8 h%d a8 8 0 0 1 8 8 v24 h-%d z' fill='%s'/>" % (W - 22, W - 6, GREEN)]
    for x in (38, W - 38):
        s.append("<rect x='%d' y='3' width='8' height='16' rx='3' fill='%s'/>" % (x - 4, LINE))
    s.append(txt(W / 2.0, 36, MONTHS[m], 18, "#fff"))
    for r in range(3):
        for c in range(6):
            s.append("<rect x='%d' y='%d' width='18' height='12' rx='2' fill='%s'/>"
                     % (17 + c * 20, 52 + r * 17, SOFT if (r + c) % 2 else "#dbe9df"))
    return svg_wrap(W, H, "".join(s), "calendar page for %s" % MONTHS[m])


def icon_svg(kind):
    """A big simple season picture: snow, sun, leaf, flower."""
    W = H = 100
    cx, cy = 50, 50
    s = []
    if kind == "snow":
        for k in range(6):
            a = k * math.pi / 3
            x2, y2 = cx + 38 * math.cos(a), cy + 38 * math.sin(a)
            s.append("<line x1='%d' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>"
                     % (cx, cy, x2, y2, "#3b7dd8"))
            for sgn in (-1, 1):
                b = a + sgn * 0.6
                mx, my = cx + 24 * math.cos(a), cy + 24 * math.sin(a)
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
                         % (mx, my, mx + 12 * math.cos(b), my + 12 * math.sin(b), "#3b7dd8"))
        lab = "a snowflake"
    elif kind == "sun":
        for k in range(12):
            a = k * math.pi / 6
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>"
                     % (cx + 30 * math.cos(a), cy + 30 * math.sin(a), cx + 44 * math.cos(a), cy + 44 * math.sin(a), "#f08a24"))
        s.append("<circle cx='%d' cy='%d' r='24' fill='#f2c230' stroke='%s' stroke-width='2.5'/>" % (cx, cy, "#f08a24"))
        lab = "a hot sun"
    elif kind == "leaf":
        s.append("<path d='M50 8 C82 22 88 60 50 84 C12 60 18 22 50 8 Z' fill='#e0702a' stroke='%s' stroke-width='2.5'/>" % LINE)
        s.append("<line x1='50' y1='16' x2='50' y2='96' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % LINE)
        for y in (32, 48, 64):
            s.append("<path d='M50 %d l-16 -10 M50 %d l16 -10' stroke='%s' stroke-width='2' fill='none'/>" % (y, y, LINE))
        lab = "an orange fall leaf"
    elif kind == "flower":
        s.append("<line x1='50' y1='56' x2='50' y2='96' stroke='#3fa34d' stroke-width='5'/>")
        s.append("<ellipse cx='64' cy='80' rx='12' ry='6' fill='#3fa34d' transform='rotate(-30 64 80)'/>")
        for k in range(6):
            a = k * math.pi / 3
            s.append("<circle cx='%.1f' cy='%.1f' r='13' fill='#e86aa6' stroke='%s' stroke-width='1.5'/>"
                     % (50 + 17 * math.cos(a), 38 + 17 * math.sin(a), LINE))
        s.append("<circle cx='50' cy='38' r='10' fill='#f2c230' stroke='%s' stroke-width='1.5'/>" % LINE)
        lab = "a spring flower"
    else:
        raise ValueError(kind)
    return svg_wrap(W, H, "".join(s), "picture: " + lab)


def calendar_svg(month, box=None, circle=None, legend=(), crossed=(), year=Y):
    """Month calendar, weeks start on Sunday. box = today (green square), circle = an event (red ring),
    crossed = dates with an X."""
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
            if d in crossed:
                s.append("<g data-x='1' opacity='0.6'><line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>"
                         "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/></g>"
                         % (cx - 17, y + 3, cx + 17, y + 27, RED, cx - 17, y + 27, cx + 17, y + 3, RED))
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
    svg = svg_wrap(W, H, "".join(s), "calendar for %s %d" % (MONTHS[month], year))
    assert svg.count("data-x='1'") == len(crossed)
    return svg


def cal(month, box=None, circle=None, event=None, start="today", crossed=()):
    legend = []
    if box:
        legend.append(("box", start))
    if circle:
        legend.append(("circle", event))
    return fig(calendar_svg(month, box, circle, legend, crossed))


# ============================================================ set 1: days of the week
def set_days():
    its = []

    def add(q, right, wrong, e, pic):
        its.append(mcq(fig(pic) + q, right, wrong, e))

    assert nxt("Monday", 1) == "Tuesday"
    add("Which day comes <b>after</b> Monday?", "Tuesday", ["Sunday", "Wednesday", "Friday"],
        "Say the days: Monday, <b>Tuesday</b>, Wednesday. Tuesday comes after Monday. (Sunday comes before.)",
        strip_svg(["Monday", None], "two days in a row, the second day is missing"))
    assert nxt("Friday", -1) == "Thursday"
    add("Which day comes <b>before</b> Friday?", "Thursday", ["Saturday", "Wednesday", "Monday"],
        "Wednesday, <b>Thursday</b>, Friday. Thursday is just before Friday. (Saturday comes after.)",
        strip_svg([None, "Friday"], "two days in a row, the first day is missing"))
    add("Which day is missing?", "Wednesday", ["Monday", "Friday", "Sunday"],
        "Tuesday, <b>Wednesday</b>, Thursday. Wednesday is between them.",
        strip_svg(["Tuesday", None, "Thursday"], "three days in a row, the middle day is missing"))
    add("Which day is missing?", "Saturday", ["Sunday", "Thursday", "Monday"],
        "Friday, <b>Saturday</b>, Sunday. Saturday is between them.",
        strip_svg(["Friday", None, "Sunday"], "three days in a row, the middle day is missing"))
    assert nxt("Saturday", 1) == "Sunday"
    add("Which day comes <b>after</b> Saturday?", "Sunday", ["Monday", "Friday", "Thursday"],
        "After Saturday comes <b>Sunday</b>. Then a new week goes on: Monday, Tuesday … (Monday comes after Sunday.)",
        strip_svg(["Saturday", None], "two days in a row, the second day is missing"))
    assert nxt("Sunday", -1) == "Saturday"
    add("Which day comes <b>before</b> Sunday?", "Saturday", ["Monday", "Friday", "Tuesday"],
        "Friday, <b>Saturday</b>, Sunday. Saturday is just before Sunday. (Monday comes after.)",
        strip_svg([None, "Sunday"], "two days in a row, the first day is missing"))
    add("Which day is missing?", "Wednesday", ["Tuesday", "Thursday", "Saturday"],
        "Sun, Mon, Tue, <b>Wed</b>, Thu, Fri, Sat. <b>Wednesday</b> is missing.", week_svg(missing=3))
    add("Which day is missing?", "Friday", ["Saturday", "Thursday", "Monday"],
        "Sun, Mon, Tue, Wed, Thu, <b>Fri</b>, Sat. <b>Friday</b> is missing.", week_svg(missing=5))
    add("Which two days are the <b>weekend</b>?", "Saturday and Sunday",
        ["Friday and Saturday", "Sunday and Monday", "Monday and Friday"],
        "The weekend is <b>Saturday and Sunday</b>. They are red on the calendar. There is no school.",
        week_svg())
    assert nxt("Thursday", 1) == "Friday"
    add("Today is <b>Thursday</b>. What day is <b>tomorrow</b>?", "Friday", ["Wednesday", "Thursday", "Saturday"],
        "Tomorrow is the next day. The day after Thursday is <b>Friday</b>. (Wednesday was yesterday.)",
        week_svg(marks={4: "today"}))
    assert nxt("Tuesday", -1) == "Monday"
    add("Today is <b>Tuesday</b>. What day was <b>yesterday</b>?", "Monday", ["Wednesday", "Tuesday", "Sunday"],
        "Yesterday is the day before. The day before Tuesday is <b>Monday</b>. (Wednesday is tomorrow.)",
        week_svg(marks={2: "today"}))
    add("Today is <b>Saturday</b>. What day is <b>tomorrow</b>?", "Sunday", ["Monday", "Friday", "Saturday"],
        "The day after Saturday is <b>Sunday</b>. (A new week does not start with Monday on this calendar.)",
        week_svg(marks={6: "today"}))
    assert nxt("Monday", -1) == "Sunday"
    add("Today is <b>Monday</b>. What day was <b>yesterday</b>?", "Sunday", ["Tuesday", "Saturday", "Friday"],
        "The day before Monday is <b>Sunday</b>. (Tuesday is tomorrow.)", week_svg(marks={1: "today"}))
    add("Today is <b>Wednesday</b>. What day was <b>yesterday</b>?", "Tuesday", ["Thursday", "Monday", "Wednesday"],
        "The day before Wednesday is <b>Tuesday</b>. (Thursday is tomorrow.)", week_svg(marks={3: "today"}))
    assert nxt("Friday", -1) == "Thursday"
    add("<b>Tomorrow</b> is Friday. What day is <b>today</b>?", "Thursday", ["Saturday", "Friday", "Wednesday"],
        "Today is the day before tomorrow. The day before Friday is <b>Thursday</b>.",
        week_svg(marks={5: "tomorrow"}))
    assert nxt("Sunday", 1) == "Monday"
    add("<b>Yesterday</b> was Sunday. What day is <b>today</b>?", "Monday", ["Saturday", "Sunday", "Tuesday"],
        "Today is the day after yesterday. The day after Sunday is <b>Monday</b>.",
        week_svg(marks={0: "yesterday"}))
    add("Which list of days is <b>in order</b>?", "Mon, Tue, Wed",
        ["Mon, Wed, Tue", "Wed, Tue, Mon", "Tue, Mon, Wed"],
        "The days go Sunday, <b>Monday, Tuesday, Wednesday</b>, Thursday … The other lists mix them up.", week_svg())
    assert nxt("Wednesday", 2) == "Friday"
    add("Today is <b>Wednesday</b>. What day is the day <b>after tomorrow</b>?", "Friday",
        ["Thursday", "Saturday", "Monday"],
        "Tomorrow is Thursday. The day after that is <b>Friday</b>. (Thursday is only tomorrow.)",
        week_svg(marks={3: "today"}))
    assert nxt("Friday", -2) == "Wednesday"
    add("Today is <b>Friday</b>. What day was it <b>2 days ago</b>?", "Wednesday",
        ["Thursday", "Sunday", "Tuesday"],
        "Count back 2 days. Do not count today. Thursday (1), Wednesday (2). It was <b>Wednesday</b>. "
        "(Thursday counts today as day 1. Sunday counts on, not back.)", week_svg(marks={5: "today"}))
    assert nxt("Saturday", 2) == "Monday"
    add("Today is <b>Saturday</b>. What day will it be in <b>2 days</b>?", "Monday",
        ["Sunday", "Tuesday", "Thursday"],
        "Count on 2 days. Do not count today. Sunday (1), Monday (2). It will be <b>Monday</b>. "
        "(Sunday counts today as day 1.)", week_svg(marks={6: "today"}))
    assert len(its) == 20
    return {"title": "Days of the week: yesterday, today and tomorrow", "items": its}


# ============================================================ set 2: months and seasons in Canada
def set_months():
    its = []

    def add(q, right, wrong, e, pic):
        its.append(mcq(fig(pic) + q, right, wrong, e))

    add("How many months are in a year?", "12", ["7", "4", "11"],
        "Count the boxes: January to December. There are <b>12 months</b>. (7 is the days in a week. 4 is the seasons.)",
        months_svg())
    add("Which month is <b>first</b> in the year?", "January", ["December", "February", "March"],
        "The year starts with <b>January</b>. December is the last month.", months_svg(missing=1))
    assert nxm(3, 1) == "April"
    add("Which month comes <b>after</b> March?", "April", ["February", "May", "June"],
        "January, February, March, <b>April</b>. April comes after March. (February comes before it.)",
        strip_svg(["March", None], "two months in a row, the second month is missing"))
    assert nxm(10, -1) == "September"
    add("Which month comes <b>before</b> October?", "September", ["November", "August", "December"],
        "August, <b>September</b>, October. September is just before October.",
        strip_svg([None, "October"], "two months in a row, the first month is missing"))
    assert nxm(12, 1) == "January"
    add("Which month comes <b>after</b> December?", "January", ["November", "February", "June"],
        "December is the last month. Then a new year starts with <b>January</b>.",
        strip_svg(["December", None], "two months in a row, the second month is missing"))
    add("Which month is missing?", "July", ["June", "August", "January"],
        "Jun, <b>Jul</b>, Aug. The missing month is <b>July</b>.", months_svg(missing=7))
    add("Which month is missing?", "November", ["October", "December", "September"],
        "Oct, <b>Nov</b>, Dec. The missing month is <b>November</b>.", months_svg(missing=11))
    add("How many <b>seasons</b> are in a year?", "4", ["12", "3", "2"],
        "Winter, spring, summer and fall: <b>4 seasons</b>. (12 is the number of months.)", seasons_svg())
    add("Which season is missing?", "Fall", ["Spring", "Summer", "Winter"],
        "The seasons go winter, spring, summer, <b>fall</b>. September, October and November are fall.",
        seasons_svg(miss_season="Fall"))
    add("Which month is missing?", "January", ["July", "June", "March"],
        "Winter is Dec, <b>Jan</b>, Feb. The missing month is <b>January</b>. (July is in summer.)",
        seasons_svg(miss_month=1))
    for m, right, wrong, why in [
            (1, "Winter", ["Summer", "Fall", "Spring"], "December, January and February are winter. It is cold and snowy."),
            (7, "Summer", ["Winter", "Spring", "Fall"], "June, July and August are summer. It is hot. There is no school."),
            (10, "Fall", ["Spring", "Winter", "Summer"], "September, October and November are fall. The leaves change colour."),
            (4, "Spring", ["Fall", "Summer", "Winter"], "March, April and May are spring. The snow melts.")]:
        assert season_of(m) == right
        add("In Canada, which season is <b>%s</b>?" % MONTHS[m], right, wrong,
            "%s So %s is in <b>%s</b>." % (why, MONTHS[m], right.lower()), month_card_svg(m))
    add("Which months are <b>winter</b> in Canada?", "December, January and February",
        ["June, July and August", "March, April and May", "September, October and November"],
        "It is cold and snowy in <b>December, January and February</b>. That is winter.", icon_svg("snow"))
    add("Which months are <b>summer</b> in Canada?", "June, July and August",
        ["December, January and February", "March, April and May", "September, October and November"],
        "It is hot in <b>June, July and August</b>. That is summer.", icon_svg("sun"))
    add("Which season comes <b>after</b> winter?", "Spring", ["Fall", "Summer", "Winter"],
        "The seasons go winter, <b>spring</b>, summer, fall. Then winter again. (Fall comes before winter.)",
        strip_svg(["Winter", None], "two seasons in a row, the second season is missing"))
    assert season_of(8) == "Summer"
    add("Hana’s birthday is in <b>August</b>. Which season is that?", "Summer", ["Winter", "Fall", "Spring"],
        "June, July and August are summer. So her birthday is in <b>summer</b>.", month_card_svg(8))
    assert season_of(2) == "Winter"
    add("It is <b>winter</b>. Which month could it be?", "February", ["July", "May", "September"],
        "Winter is December, January and <b>February</b>. (July is summer. May is spring. September is fall.)",
        icon_svg("snow"))
    assert season_of(11) == "Fall"
    add("The leaves fall off the trees. Which month could it be?", "November", ["March", "July", "January"],
        "Leaves fall in <b>fall</b>: September, October and <b>November</b>.", icon_svg("leaf"))
    assert len(its) == 20
    return {"title": "Months of the year and seasons in Canada", "items": its}


# ============================================================ set 3: read a calendar page
def set_read():
    its = []
    M = 6
    c = cal(M)
    assert ndays(M) == 30 and wd(M, 1) == "Tuesday"
    its.append(mcq(c + "Which month does this calendar show?", "June", ["Sunday", "May", "July"],
                   "The month is at the top: <b>June</b> 2027. (Sunday is a day, not a month.)"))
    its.append(mcq(c + "What day is <b>June 1</b>?", "Tuesday", ["Sunday", "Monday", "Wednesday"],
                   "Find 1. Go up to the top of its column: Tue. June 1 is a <b>Tuesday</b>. "
                   "(A month does not always start on Sunday.)"))
    for d in (10, 19, 27):
        w = wd(M, d)
        its.append(mcq(c + "What day is <b>June %d</b>?" % d, w, [nxt(w, -1), nxt(w, 1), nxt(w, 3)],
                       "Find %d. Go up to the top of its column: <b>%s</b>." % (d, w)))
    fris = dates_on(M, "Friday")
    assert fris[0] == 4 and wd(M, 5) == "Saturday"
    its.append(mcq(c + "What is the date of the <b>first Friday</b> in June?", "June 4",
                   ["June 1", "June 11", "June 5"],
                   "Go down the Fri column. The first number is 4. It is <b>June 4</b>. "
                   "(June 1 is the first date, but it is a Tuesday.)"))
    assert wd(M, 14) == "Monday" and all(wd(M, d) != "Monday" for d in (13, 15, 16))
    its.append(mcq(c + "Which date is a <b>Monday</b>?", "June 14", ["June 13", "June 15", "June 16"],
                   "Look in the Mon column: 7, <b>14</b>, 21, 28. So June 14 is a Monday. "
                   "(June 13 is a Sunday.)"))
    suns = dates_on(M, "Sunday")
    assert len(suns) == 4
    its.append(mcq(c + "How many <b>Sundays</b> are in June?", "4", ["5", "7", "27"],
                   "The Sundays are %s. That is <b>4 Sundays</b>. (27 is the date of the last one.)"
                   % ", ".join(map(str, suns))))
    its.append(mcq(c + "What date comes just <b>after</b> June 15?", "June 16", ["June 14", "June 22", "June 17"],
                   "The next date is one more: 15 + 1 = <b>16</b>. (June 22 is the date under it, one week later.)"))
    its.append(mcq(c + "What date comes just <b>before</b> June 13?", "June 12", ["June 14", "June 6", "June 11"],
                   "The date before is one less: 13 − 1 = <b>12</b>. It is at the end of the row above. "
                   "(June 6 is the date above 13, one week before.)"))
    its.append(mcq(c + "What is the <b>last day</b> of June?", "June 30", ["June 31", "June 1", "July 1"],
                   "The last number on the calendar is 30. So it is <b>June 30</b>. (June has 30 days. There is no June 31.)"))
    assert wd(M, 30) == "Wednesday"
    its.append(mcq(c + "What day is the <b>last day</b> of June?", "Wednesday", ["Thursday", "Saturday", "Sunday"],
                   "The last date is 30. Go up its column: <b>Wednesday</b>. (Saturday is the end of the row, not the "
                   "last day.)"))
    # September 2027: school and the Terry Fox Run
    M = 9
    school, terry = 7, 24
    assert wd(M, 6) == "Monday" and wd(M, school) == "Tuesday" and wd(M, terry) == "Friday"
    c2 = fig(calendar_svg(M, box=school, circle=terry, legend=[("box", "first day of school"), ("circle", "Terry Fox Run")]))
    its.append(mcq(c2 + "The <b>Terry Fox Run</b> is circled. What is the date?", "September 24",
                   ["September 23", "September 25", "September 17"],
                   "The red circle is around 24. The run is on <b>September 24</b>."))
    its.append(mcq(c2 + "What day is the <b>Terry Fox Run</b>?", "Friday", ["Thursday", "Saturday", "Wednesday"],
                   "Go up from the circled 24 to the top: <b>Friday</b>."))
    its.append(mcq(c2 + "The <b>first day of school</b> is in the green box. What is the date?", "September 7",
                   ["September 6", "September 8", "September 14"],
                   "The green box is around 7. School starts on <b>September 7</b>."))
    its.append(mcq(c2 + "What day is the <b>first day of school</b>?", "Tuesday", ["Monday", "Wednesday", "Sunday"],
                   "Go up from 7 to the top: <b>Tuesday</b>. (Monday, September 6 is Labour Day.)"))
    assert wd(M, 15) == "Wednesday"
    its.append(mcq(c2 + "Mei’s birthday is <b>September 15</b>. What day is that?", "Wednesday",
                   ["Tuesday", "Thursday", "Friday"],
                   "Find 15. Go up to the top of its column: <b>Wednesday</b>."))
    sat = dates_on(M, "Saturday")
    assert 18 in sat and not set(sat) & {17, 19, 12}
    its.append(mcq(c2 + "Which date is a <b>Saturday</b>?", "September 18",
                   ["September 17", "September 19", "September 12"],
                   "Look in the Sat column: 4, 11, <b>18</b>, 25. So September 18 is a Saturday. "
                   "(September 19 is a Sunday.)"))
    assert len(dates_on(M, "Friday")) == 4
    its.append(mcq(c2 + "How many <b>Fridays</b> are in September?", "4", ["5", "3", "24"],
                   "The Fridays are %s. That is <b>4 Fridays</b>." % ", ".join(map(str, dates_on(M, "Friday")))))
    assert ndays(9) == 30 and wd(9, 30) == "Thursday" and wd(10, 1) == "Friday"
    its.append(mcq(c2 + "September 30 is the last day. What day will <b>October 1</b> be?", "Friday",
                   ["Thursday", "Sunday", "Wednesday"],
                   "September 30 is a Thursday. October 1 is the next day: <b>Friday</b>. "
                   "(A new month does not always start on Sunday.)"))
    assert len(its) == 20
    return {"title": "Read the date on a calendar", "items": its}


# ============================================================ set 4: count days and weeks
def between(c, q, a, b, extra, e_extra="", first="today"):
    """Days from date a to date b (same month): count the jumps; today is not counted."""
    n = b - a
    assert 0 < n and n + 1 <= 50 and extra <= 50
    e = ("Count the jumps from %d to %d: %s. That is <b>%d</b>. Do not count %s.%s (%d counts %s too.)"
         % (a, b, ", ".join(str(a + i) for i in range(1, n + 1)) if n <= 8 else "%d − %d = %d" % (b, a, n),
            n, first, e_extra, n + 1, first))
    return mcq(c + q, str(n), [str(n + 1), str(n - 1), str(extra)], e)


def set_count():
    its = []
    its.append(mcq(fig(week_svg()) + "How many days are in <b>1 week</b>?", "7", ["5", "6", "12"],
                   "Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday. That is <b>7 days</b>. "
                   "(5 is only the school days.)"))
    its.append(mcq(fig(week_svg(shade=(1, 2, 3, 4, 5))) + "How many <b>school days</b> are in 1 week?", "5",
                   ["7", "2", "6"],
                   "Monday to Friday are school days. That is <b>5 days</b>. (7 counts the weekend too.)"))
    its.append(mcq(fig(week_svg(shade=(0, 6))) + "How many days are in the <b>weekend</b>?", "2", ["7", "5", "1"],
                   "Saturday and Sunday. That is <b>2 days</b>."))
    its.append(mcq(fig(grid_svg(14, 2)) + "How many days are in <b>2 weeks</b>?", "14", ["7", "9", "2"],
                   "1 week is 7 days. 7 + 7 = <b>14 days</b>. (7 is only 1 week.)"))
    assert 7 + 2 == 9
    its.append(mcq(fig(grid_svg(9, 2)) + "Noah’s cousin stays for <b>1 week and 2 days</b>. How many days is that?",
                   "9", ["8", "3", "10"],
                   "1 week is 7 days. 7 + 2 = <b>9 days</b>. (3 adds 1 + 2. It forgets that a week is 7 days.)"))
    M = 6
    its.append(between(cal(M, 9, 12, "Ava’s party"), "Today is June 9. How many days until Ava’s party?", 9, 12, 21))
    its.append(between(cal(M, 14, 18, "field trip"), "Today is June 14. How many days until the field trip?",
                       14, 18, 32))
    its.append(between(cal(M, 2, 9, "class picnic"), "Today is June 2. How many days until the class picnic?",
                       2, 9, 11, " 9 is right under 2. That is 1 week."))
    its.append(between(cal(M, 21, 26, "soccer game"), "Today is June 21. How many days until the soccer game?",
                       21, 26, 47))
    its.append(mcq(cal(M, 15) + "Today is June 15. What is the date <b>1 week</b> from today?", "June 22",
                   ["June 21", "June 16", "June 8"],
                   "1 week is 7 days. 15 + 7 = 22. Go straight down one row: <b>June 22</b>. "
                   "(June 21 counts today as day 1. June 8 is 1 week ago.)"))
    its.append(mcq(cal(M, 8) + "Today is June 8. What is the date <b>3 days</b> from today?", "June 11",
                   ["June 10", "June 5", "June 12"],
                   "Count on 3: 9, 10, 11. It is <b>June 11</b>. (June 10 counts today as day 1. June 5 counts back.)"))
    assert dates_on(6, "Monday") == [7, 14, 21, 28]
    its.append(mcq(cal(M, 7, 21, "swimming test", start="first swim class")
                   + "How many <b>weeks</b> from the first swim class to the swimming test?", "2 weeks",
                   ["3 weeks", "14 weeks", "1 week"],
                   "21 is 2 rows straight under 7. Each row down is 1 week. That is <b>2 weeks</b>. "
                   "(3 weeks counts the rows, not the jumps.)"))
    its.append(mcq(cal(M) + "How many days are in <b>June</b>?", "30", ["31", "7", "5"],
                   "The last date is 30. June has <b>30 days</b>. (7 is the days in one row. 5 is the rows.)"))
    M = 11
    crossed = tuple(range(1, 10))
    its.append(mcq(fig(calendar_svg(M, box=10, crossed=crossed, legend=[("box", "today")]))
                   + "Arjun crosses off each day that is done. Today is November 10. How many days are crossed off?",
                   "9", ["10", "8", "2"],
                   "The Xs are on 1 to 9. That is <b>9 days</b>. (10 counts today too, but today is not done yet.)"))
    assert len(dates_on(M, "Monday")) == 5
    its.append(mcq(cal(M) + "How many <b>Mondays</b> are in November?", "5", ["4", "29", "7"],
                   "The Mondays are %s. That is <b>5 Mondays</b>. (29 is the date of the last one.)"
                   % ", ".join(map(str, dates_on(M, "Monday")))))
    its.append(between(cal(M, 4, 11, "Remembrance Day"), "Today is November 4. How many days until Remembrance Day?",
                       4, 11, 15, " 11 is right under 4. That is 1 week."))
    its.append(mcq(fig(week_svg(marks={2: "swim"})) + "Liam swims every <b>Tuesday</b>. How many times does he swim in "
                   "<b>2 weeks</b>?", "2", ["14", "1", "7"],
                   "There is 1 Tuesday in each week. 1 + 1 = <b>2 times</b>. (14 is the days in 2 weeks.)"))
    assert (DAYS.index("Monday") - DAYS.index("Friday")) % 7 == 3
    its.append(mcq(fig(week_svg(marks={5: "today"})) + "Today is <b>Friday</b>. The field trip is on <b>Monday</b>. "
                   "How many days until the field trip?", "3", ["4", "2", "5"],
                   "Count on from Friday: Saturday (1), Sunday (2), Monday (3). That is <b>3 days</b>. "
                   "(4 counts today too.)"))
    assert (DAYS.index("Saturday") - DAYS.index("Sunday")) % 7 == 6
    its.append(mcq(fig(week_svg(marks={0: "today", 6: "hockey"})) + "Today is <b>Sunday</b>. Ethan has hockey on "
                   "<b>Saturday</b>. How many days until hockey?", "6", ["7", "5", "1"],
                   "Count on: Mon, Tue, Wed, Thu, Fri, Sat. That is <b>6 days</b>. (7 counts today too.)"))
    its.append(between(cal(9, 7, 14, "today", start="first day of school"),
                       "School started on September 7. Today is September 14. How many days ago did school start?",
                       7, 14, 21, " 14 is right under 7. That is 1 week."))
    assert len(its) == 20
    return {"title": "Count the days: weeks and days on a calendar", "items": its}


# ============================================================ set 5: holidays
def set_holidays():
    its = []
    M = 7
    assert wd(7, 1) == "Thursday"
    c = cal(M, circle=1, event="Canada Day")
    its.append(mcq(c + "<b>Canada Day</b> is circled. What is the date?", "July 1", ["June 1", "July 7", "July 31"],
                   "The red circle is around 1 in July. Canada Day is <b>July 1</b>. It is Canada’s birthday."))
    its.append(mcq(c + "What day is <b>Canada Day</b> in 2027?", "Thursday", ["Wednesday", "Friday", "Sunday"],
                   "Go up from the circled 1 to the top: <b>Thursday</b>. (July does not start on Sunday.)"))
    assert season_of(7) == "Summer"
    its.append(mcq(fig(month_card_svg(7)) + "Canada Day is in July. Which <b>season</b> is that?", "Summer",
                   ["Spring", "Fall", "Winter"],
                   "June, July and August are summer. Canada Day is in <b>summer</b>. There is no school."))
    assert ndays(6) == 30
    its.append(mcq(fig(strip_svg(["June 28", "June 29", "June 30", "July 1"], "dates June 28 to July 1"))
                   + "Today is <b>June 28</b>. How many sleeps until Canada Day?", "3", ["4", "2", "29"],
                   "Count the jumps: June 29 (1), June 30 (2), July 1 (3). That is <b>3 sleeps</b>. "
                   "(4 counts today too.)"))
    M = 10
    mons = dates_on(M, "Monday")
    assert mons[1] == 11
    c = cal(M, circle=11, event="Thanksgiving")
    its.append(mcq(c + "<b>Thanksgiving</b> is circled. What is the date?", "October 11",
                   ["October 10", "October 12", "October 4"],
                   "The red circle is around 11. Thanksgiving is on <b>October 11</b> in 2027."))
    its.append(mcq(c + "What day is <b>Thanksgiving</b>?", "Monday", ["Sunday", "Tuesday", "Friday"],
                   "Go up from 11 to the top: <b>Monday</b>. In Canada, Thanksgiving is always on a Monday in October."))
    its.append(mcq(fig(icon_svg("leaf")) + "In Canada, which <b>month</b> is Thanksgiving in?", "October",
                   ["November", "September", "December"],
                   "Canada has Thanksgiving in <b>October</b>. (The USA has it in November.)"))
    assert season_of(10) == "Fall"
    its.append(mcq(fig(month_card_svg(10)) + "Thanksgiving is in October. Which <b>season</b> is that?", "Fall",
                   ["Winter", "Summer", "Spring"],
                   "September, October and November are fall. Thanksgiving is in <b>fall</b>."))
    its.append(between(cal(M, 4, 11, "Thanksgiving"), "Today is October 4. How many days until Thanksgiving?",
                       4, 11, 15, " 11 is right under 4. That is 1 week."))
    assert wd(10, 31) == "Sunday"
    its.append(mcq(cal(M, circle=31, event="Halloween") + "Halloween is <b>October 31</b>. What day is it in 2027?",
                   "Sunday", ["Saturday", "Monday", "Friday"],
                   "31 is in the first column: <b>Sunday</b>. (Saturday is the last column.)"))
    M = 2
    mons = dates_on(M, "Monday")
    assert mons[2] == 15 and ndays(M) == 28
    c = cal(M, circle=15, event="Family Day")
    its.append(mcq(c + "<b>Family Day</b> is circled. What is the date?", "February 15",
                   ["February 14", "February 16", "February 8"],
                   "The red circle is around 15. Family Day is on <b>February 15</b> in 2027. "
                   "(February 14 is Valentine’s Day.)"))
    its.append(mcq(c + "What day is <b>Family Day</b>?", "Monday", ["Sunday", "Tuesday", "Saturday"],
                   "Go up from 15 to the top: <b>Monday</b>. Family Day is always on a Monday in February."))
    assert season_of(2) == "Winter"
    its.append(mcq(fig(month_card_svg(2)) + "Family Day is in February. Which <b>season</b> is that?", "Winter",
                   ["Spring", "Fall", "Summer"],
                   "December, January and February are winter. Family Day is in <b>winter</b>. Many families go skating."))
    its.append(between(cal(M, 10, 15, "Family Day"), "Today is February 10. How many days until Family Day?",
                       10, 15, 25))
    its.append(mcq(fig(week_svg(marks={1: "Family Day"}, shade=(2, 3, 4, 5)))
                   + "There is no school on Family Day. How many <b>school days</b> are in that week?", "4",
                   ["5", "3", "6"],
                   "School days are Monday to Friday, but Monday is a holiday. Tuesday to Friday is <b>4 days</b>. "
                   "(5 forgets the holiday.)"))
    assert wd(12, 25) == "Saturday"
    its.append(between(cal(12, 20, 25, "Christmas Day"), "Today is December 20. How many sleeps until Christmas Day?",
                       20, 25, 45))
    its.append(mcq(fig(icon_svg("sun")) + "Which holiday is in <b>summer</b>?", "Canada Day",
                   ["Thanksgiving", "Family Day", "Christmas Day"],
                   "<b>Canada Day</b> is July 1. July is summer. (Thanksgiving is in fall. Family Day and Christmas "
                   "are in winter.)"))
    its.append(mcq(fig(month_card_svg(1)) + "<b>New Year’s Day</b> is the first day of the year. What is the date?",
                   "January 1", ["December 31", "January 31", "December 1"],
                   "The year starts with January. The first day is <b>January 1</b>. (December 31 is the last day.)"))
    assert 4 + 7 == 11
    its.append(mcq(cal(11, 4) + "Maya’s class makes poppies on <b>November 4</b>. Remembrance Day is <b>1 week</b> "
                   "later. What is the date?", "November 11", ["November 10", "November 5", "November 18"],
                   "1 week is 7 days. 4 + 7 = 11. Go straight down one row: <b>November 11</b>. "
                   "(November 10 counts November 4 as day 1.)"))
    its.append(between(cal(7, 1, 9, "Leah’s birthday", start="Canada Day"),
                       "Canada Day is July 1. Leah’s birthday is July 9. How many days after Canada Day is it?",
                       1, 9, 10, first="July 1"))
    assert len(its) == 20
    return {"title": "Holidays on the calendar: Canada Day, Thanksgiving, Family Day", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Days of the week</h2>"
        "<p>A week has <b>7 days</b>. Say them in order every day.</p>"
        "<figure class='sn-fig'>" + week_svg(marks={3: "today"}) +
        "<figcaption>Today is Wednesday. Yesterday was Tuesday. Tomorrow is Thursday.</figcaption></figure>"
        "<p>After Saturday comes Sunday. Then the days go round again.</p>"
        + ex("Tomorrow", "Today is Saturday. What day is tomorrow?", "The day after Saturday is Sunday.", "Sunday") +
        "<h2>Months and seasons</h2>"
        "<p>A year has <b>12 months</b>. It starts with January and ends with December.</p>"
        "<figure class='sn-fig'>" + seasons_svg() +
        "<figcaption>In Canada: winter is December to February. Spring is March to May. Summer is June to August. "
        "Fall is September to November.</figcaption></figure>"
        "<h2>Read a calendar</h2>"
        "<p>Each row is <b>1 week</b>. Find the date. Then go up to the top to see the day.</p>"
        "<figure class='sn-fig'>" + calendar_svg(7, box=1, circle=9, legend=[("box", "Canada Day"), ("circle", "Leah’s birthday")]) +
        "<figcaption>Canada Day is Thursday, July 1. Leah’s birthday is Friday, July 9.</figcaption></figure>"
        + ex("Count the days", "How many days from July 1 to July 9?",
             "Count the jumps: 2, 3, 4, 5, 6, 7, 8, 9. That is 8 jumps. Do not count July 1.", "8 days") +
        "<h2>Holidays in Ontario</h2>"
        + table(["Holiday", "When", "Season"], [
            ["New Year’s Day", "January 1", "winter"],
            ["Family Day", "a Monday in February", "winter"],
            ["Canada Day", "July 1", "summer"],
            ["Thanksgiving", "a Monday in October", "fall"],
            ["Christmas Day", "December 25", "winter"]]) +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["After Saturday comes Monday", "After Saturday comes Sunday"],
            ["Counting today: June 9 to June 12 is 4 days", "Count the jumps: 10, 11, 12. That is 3 days"],
            ["Mixing up yesterday and tomorrow", "Yesterday is the day before. Tomorrow is the day after"],
            ["Every month starts on Sunday", "Look at the calendar: June 1, 2027 is a Tuesday"],
            ["January is summer", "In Canada, January is winter"],
        ])
    )


FAQ = [
    {"q": "What do Grade 1 students learn about the calendar in Ontario?",
     "a": "In the Ontario Mathematics Curriculum (2020), Grade 1 students read the date on a calendar and use it to find days, weeks, months, holidays and seasons."},
    {"q": "What are the seasons in Canada by month?",
     "a": "Winter is December, January and February; spring is March, April and May; summer is June, July and August; fall is September, October and November."},
    {"q": "When are Canada Day, Thanksgiving and Family Day?",
     "a": "Canada Day is always July 1. Thanksgiving is the second Monday in October, and Family Day in Ontario is the third Monday in February."},
    {"q": "How can I help my child learn the days and months at home?",
     "a": "Hang a calendar at your child’s height. Each morning, say the date together, cross off yesterday and count the sleeps to the next birthday or holiday."},
]


def balance(sets, rnd):
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


def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert "<svg" in it["q"], it["q"]
            key = re.sub(r"<[^>]+>", " ", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
            for t in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in t and '"' not in t and ".." not in t, t
            if all(re.fullmatch(r"\d+", c) for c in it["c"]):
                assert all(0 < int(c) <= 50 for c in it["c"]), it["c"]
            # every month-date shown in a question or choice is a real 2027 date
            for m, d in re.findall(r"\b(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2})\b",
                                   re.sub(r"<[^>]+>", " ", it["q"])):
                assert int(d) <= ndays(MONTHS.index(m)), (m, d)
            right = it["c"][it["a"]]
            mm = re.fullmatch(r"(\w+) (\d+)", right)
            if mm and mm.group(1) in MONTHS:
                assert int(mm.group(2)) <= ndays(MONTHS.index(mm.group(1))), right


def gen():
    rnd = random.Random(41814)
    sets = [set_days(), set_months(), set_read(), set_count(), set_holidays()]
    balance(sets, rnd)
    check(sets)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "calendar-days-weeks-and-months",
        "sort": 14, "updated": UPDATED, "pdf_url": "",
        "title": "The Calendar: Days of the Week, Months, Seasons and Holidays",
        "seo_title": "Grade 1 Calendar Math Worksheets: Days, Weeks, Months and Seasons, Free with Answer Key (Ontario)",
        "short_title": "Calendar: days, weeks and months",
        "domain": "Spatial Sense",
        "standard_code": "Grade 1: E2.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read the date on a calendar, and use a calendar to identify days, weeks, months, holidays, and seasons",
        "meta_desc": "Free Grade 1 math worksheets on the calendar for the Ontario curriculum: days of the week, yesterday "
                     "and tomorrow, months and seasons in Canada, reading the date on a calendar, counting days and "
                     "weeks, and Canada Day, Thanksgiving and Family Day. 100 picture questions with an answer key.",
        "key_big": "A week has 7 days. A year has 12 months. Each row of a calendar is 1 week.",
        "key_sub": "After Saturday comes Sunday. To count days, count the jumps and do not count today. "
                   "In Canada, winter is December to February.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    for p in ("calendar for", "two days", "three days", "two months", "three months", "two seasons", "the 7 days",
              "the 12 months", "the four seasons", "dates June", "calendar weeks"):
        mark_large(u, p)
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
