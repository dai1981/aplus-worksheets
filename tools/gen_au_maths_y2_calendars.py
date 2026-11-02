# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Calendars and Dates (Australian Curriculum v9.0, AC9M2M03)
  python3 tools/gen_au_maths_y2_calendars.py
Every calendar is drawn from the real month (weeks start on Monday, as on most Australian calendars).
Every date and day is worked out in code with the calendar module.
Wrong answers come from real student mistakes: counting the start day when finding the days between two
dates, months or days out of order, the date in the row above or below read instead, a new month started in
the Monday column, last week’s day given for “next”, and seasons taken from the Northern Hemisphere
(Christmas in winter, July in summer).
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import calendar, json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
SHORT = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
SEASONS = [("Summer", [12, 1, 2], "#f6c26b"), ("Autumn", [3, 4, 5], "#e9a27a"),
           ("Winter", [6, 7, 8], "#9cc3e6"), ("Spring", [9, 10, 11], "#a8d08d")]
Y = 2027


def wd(m, d, y=Y):
    return WEEKDAYS[calendar.weekday(y, m, d)]


def dt(m, d):
    return "%d %s" % (d, MONTHS[m])


def season_of(m):
    return next(n for n, ms, c in SEASONS if m in ms)


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


def strip_svg(labels, label):
    """A row of boxes (days or months). None is drawn as a red ?."""
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
            s.append("<text x='%.1f' y='33' font-size='24' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                     % (x + bw / 2.0, RED))
        else:
            s.append("<rect x='%d' y='2' width='%d' height='%d' rx='8' fill='#eef5f0' stroke='%s' stroke-width='2'/>"
                     % (x, bw, H - 4, GREEN))
            s.append("<text x='%.1f' y='31' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x + bw / 2.0, LINE, t))
    return svg_wrap(W, H, "".join(s), label)


def months_svg(missing):
    """All 12 months in two rows of 6; the missing one is a red ?."""
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
            s.append("<text x='%.1f' y='%d' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                     % (x + bw / 2.0, y + 28, RED))
        else:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='7' fill='#eef5f0' stroke='%s' stroke-width='2'/>"
                     % (x, y, bw, bh, GREEN))
            s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x + bw / 2.0, y + 26, LINE, SHORT[m]))
    return svg_wrap(W, H, "".join(s), "months of the year in order")


def seasons_svg(miss_season=None, miss_month=None):
    """The Australian year from December: summer, autumn, winter, spring. Each season has 3 months."""
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
                s.append("<text x='%.1f' y='28' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                         % (x + bw / 2.0, RED))
            else:
                s.append("<rect x='%d' y='2' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x, bw, bh, col, LINE))
                s.append("<text x='%.1f' y='26' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x + bw / 2.0, LINE, SHORT[m]))
        if name == miss_season:
            s.append("<text x='%.1f' y='%d' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                     % (gx + gw / 2.0, bh + 30, RED))
        else:
            s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (gx + gw / 2.0, bh + 29, LINE, name))
    return svg_wrap(W, H, "".join(s), "seasons in Australia")


def calendar_svg(month, box=None, circle=None, legend=(), year=Y):
    """Month calendar, weeks start on Monday. box = today (green square), circle = an event (red ring)."""
    CW, RH, top = 46, 30, 62
    weeks = calendar.Calendar(0).monthdayscalendar(year, month)
    W = 7 * CW + 4
    gh = top + RH * len(weeks)
    H = gh + 4 + (34 if legend else 0)
    s = ["<rect x='2' y='2' width='%d' height='32' fill='%s'/>" % (W - 4, GREEN),
         "<text x='%.0f' y='25' font-size='18' font-weight='700' fill='#fff' text-anchor='middle'>%s %d</text>"
         % (W / 2.0, MONTHS[month], year)]
    for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        s.append("<text x='%.0f' y='54' font-size='14' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (2 + CW * i + CW / 2.0, GREEN if i < 5 else RED, d))
    for r, wk in enumerate(weeks):
        y = top + RH * r
        if r % 2 == 0:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
        for i, d in enumerate(wk):
            if not d:
                continue
            cx = 2 + CW * i + CW / 2.0
            if d == box:
                s.append("<rect x='%.1f' y='%d' width='34' height='26' rx='4' fill='none' stroke='%s' stroke-width='3'/>"
                         % (cx - 17, y + 2, GREEN))
            if d == circle:
                s.append("<circle cx='%.1f' cy='%d' r='14' fill='none' stroke='%s' stroke-width='3'/>" % (cx, y + 15, RED))
            s.append("<text x='%.0f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (cx, y + 21, LINE, d))
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, gh - 2, LINE))
    if legend:
        y = gh + 22
        x = 8
        for kind, text in legend:
            if kind == "box":
                s.append("<rect x='%d' y='%d' width='22' height='18' rx='3' fill='none' stroke='%s' stroke-width='3'/>"
                         % (x, y - 14, GREEN))
            else:
                s.append("<circle cx='%d' cy='%d' r='10' fill='none' stroke='%s' stroke-width='3'/>" % (x + 11, y - 5, RED))
            s.append("<text x='%d' y='%d' font-size='15' fill='%s'>%s</text>" % (x + 30, y, LINE, text))
            x += 30 + int(len(text) * 8) + 18
        assert x - 18 <= W, legend
    return svg_wrap(W, H, "".join(s), "calendar for %s %d" % (MONTHS[month].lower(), year))


def cal(month, box=None, circle=None, event=None, today=True):
    legend = []
    if box:
        legend.append(("box", "today" if today else "start"))
    if circle:
        legend.append(("circle", event))
    return fig(calendar_svg(month, box, circle, legend))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def nxt(day, n):
    return WEEKDAYS[(WEEKDAYS.index(day) + n) % 7]


def nxm(m, n):
    return MONTHS[(m - 1 + n) % 12 + 1]


# ============================================================ set 1: days and months in order
def set_order():
    its = []
    assert nxt("Monday", 1) == "Tuesday"
    its.append(mcq(fig(strip_svg(["Monday", None], "days in a row")) + "Which day comes <b>after</b> Monday?", "Tuesday",
                   ["Sunday", "Wednesday", "Thursday"],
                   "Say the days in order: Monday, <b>Tuesday</b>, Wednesday … So Tuesday comes after Monday. "
                   "(Sunday comes before Monday.)"))
    assert nxt("Friday", -1) == "Thursday"
    its.append(mcq(fig(strip_svg([None, "Friday"], "days in a row")) + "Which day comes <b>before</b> Friday?", "Thursday",
                   ["Saturday", "Wednesday", "Monday"],
                   "Monday, Tuesday, Wednesday, <b>Thursday</b>, Friday. Thursday is just before Friday. "
                   "(Saturday comes after Friday.)"))
    its.append(mcq("How many days are in <b>1 week</b>?", "7", ["5", "12", "30"],
                   "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. That is <b>7 days</b>. "
                   "(5 is only the school days. 12 is the number of months.)"))
    its.append(mcq(fig(strip_svg(["Tuesday", None, "Thursday"], "days in a row")) + "Which day is missing?", "Wednesday",
                   ["Monday", "Friday", "Saturday"],
                   "Tuesday, <b>Wednesday</b>, Thursday. Wednesday is the day between Tuesday and Thursday."))
    assert nxt("Sunday", 1) == "Monday"
    its.append(mcq(fig(strip_svg(["Sunday", None], "days in a row")) + "Which day comes <b>after</b> Sunday?", "Monday",
                   ["Saturday", "Tuesday", "Friday"],
                   "Sunday is the last day on the calendar. Then a new week starts with <b>Monday</b>."))
    its.append(mcq("Which two days are the <b>weekend</b>?", "Saturday and Sunday",
                   ["Friday and Saturday", "Sunday and Monday", "Monday and Tuesday"],
                   "There is no school on the weekend: <b>Saturday and Sunday</b>. School is Monday to Friday."))
    assert nxt("Thursday", -1) == "Wednesday"
    its.append(mcq("Today is <b>Thursday</b>. What day was it <b>yesterday</b>?", "Wednesday",
                   ["Friday", "Tuesday", "Saturday"],
                   "Yesterday is the day before. The day before Thursday is <b>Wednesday</b>. "
                   "(Friday is tomorrow.)"))
    its.append(mcq("How many months are in <b>1 year</b>?", "12", ["7", "52", "4"],
                   "January to December: <b>12 months</b>. (7 is the days in a week, 52 is the weeks in a year "
                   "and 4 is the seasons.)"))
    its.append(mcq("What is the <b>first</b> month of the year?", "January", ["December", "February", "March"],
                   "The year starts on 1 January. <b>January</b> is first. December is the last month."))
    assert nxm(3, 1) == "April"
    its.append(mcq(fig(strip_svg(["March", None], "months in a row")) + "Which month comes <b>after</b> March?", "April",
                   ["May", "February", "June"],
                   "January, February, March, <b>April</b>, May … April comes after March. (February comes before it.)"))
    assert nxm(10, -1) == "September"
    its.append(mcq(fig(strip_svg([None, "October"], "months in a row")) + "Which month comes <b>before</b> October?",
                   "September", ["November", "August", "December"],
                   "… August, <b>September</b>, October, November … September is just before October."))
    assert nxm(12, 1) == "January"
    its.append(mcq(fig(strip_svg(["December", None], "months in a row")) + "Which month comes <b>after</b> December?",
                   "January", ["November", "February", "June"],
                   "December is the last month. Then a new year starts with <b>January</b>."))
    its.append(mcq(fig(months_svg(7)) + "Which month is missing?", "July", ["June", "August", "January"],
                   "Jan, Feb, Mar, Apr, May, Jun, <b>Jul</b>, Aug … The missing month is <b>July</b>. "
                   "(June and August are next to it.)"))
    its.append(mcq(fig(months_svg(11)) + "Which month is missing?", "November", ["October", "December", "September"],
                   "Sep, Oct, <b>Nov</b>, Dec. The missing month is <b>November</b>. It is the 11th month."))
    assert nxt("Friday", 2) == "Sunday"
    its.append(mcq("Today is <b>Friday</b>. What day will it be in <b>2 days</b>?", "Sunday",
                   ["Saturday", "Monday", "Wednesday"],
                   "Count on 2 days from Friday: Saturday (1), Sunday (2). It will be <b>Sunday</b>. "
                   "(Saturday is only 1 day. Do not count Friday.)"))
    assert MONTHS[5] == "May"
    its.append(mcq("What is the <b>5th</b> month of the year?", "May", ["June", "April", "March"],
                   "January (1st), February (2nd), March (3rd), April (4th), <b>May</b> (5th)."))
    its.append(mcq("Which list of days is <b>in order</b>?", "Tuesday, Wednesday, Thursday",
                   ["Tuesday, Thursday, Wednesday", "Thursday, Wednesday, Tuesday", "Wednesday, Tuesday, Thursday"],
                   "The days go Monday, <b>Tuesday, Wednesday, Thursday</b>, Friday … The other lists mix them up."))
    its.append(mcq("Which list of months is <b>in order</b>?", "May, June, July",
                   ["June, May, July", "July, June, May", "May, July, June"],
                   "The months go April, <b>May, June, July</b>, August … The other lists mix them up."))
    assert nxt("Tuesday", -3) == "Saturday"
    its.append(mcq("Today is <b>Tuesday</b>. What day was it <b>3 days ago</b>?", "Saturday",
                   ["Sunday", "Friday", "Monday"],
                   "Count back 3 days from Tuesday: Monday (1), Sunday (2), Saturday (3). It was <b>Saturday</b>. "
                   "(Sunday counts Tuesday as one of the days. Friday counts on, not back.)"))
    assert nxm(11, 2) == "January"
    its.append(mcq("Which month is <b>2 months after</b> November?", "January", ["December", "February", "September"],
                   "Count on from November: December (1), January (2). After December the year starts again, so it is "
                   "<b>January</b>. (September is 2 months before.)"))
    assert len(its) == 20
    return {"title": "Days of the week and months of the year in order", "items": its}


# ============================================================ set 2: read a month calendar
def set_read():
    its = []
    M = 5
    c = cal(M)
    weeks = calendar.Calendar(0).monthdayscalendar(Y, M)
    days = calendar.monthrange(Y, M)[1]
    its.append(mcq(c + "Which month does this calendar show?", "May", ["Monday", "April", "June"],
                   "The month is at the top of the calendar: <b>May</b> 2027. (Monday is a day, not a month.)"))
    assert days == 31 and len(weeks) == 6
    its.append(mcq(c + "How many days are in May?", "31", ["30", "7", "6"],
                   "The last date is 31, so May has <b>31 days</b>. (7 is the days in one row. 6 is the number of rows.)"))
    assert wd(M, 1) == "Saturday"
    its.append(mcq(c + "What day of the week is <b>1 May</b>?", "Saturday", ["Monday", "Sunday", "Friday"],
                   "Find 1 and go up its column to the top: Sat. 1 May is a <b>Saturday</b>. "
                   "(A month does not always start on Monday.)"))
    for d, w in [(12, "Wednesday"), (20, "Thursday")]:
        assert wd(M, d) == w
        its.append(mcq(c + "What day of the week is <b>%d May</b>?" % d, w, [nxt(w, -1), nxt(w, 1), "Monday"],
                       "Find %d and go up its column to the top: <b>%s</b>." % (d, w)))
    first_mon = [d for d in range(1, days + 1) if wd(M, d) == "Monday"]
    assert first_mon[0] == 3
    its.append(mcq(c + "What is the date of the <b>first Monday</b> in May?", "3 May", ["1 May", "10 May", "2 May"],
                   "Go down the Mon column. The first number is 3. So it is <b>3 May</b>. "
                   "(1 May is the first date, but it is a Saturday.)"))
    after = 19 + 1
    its.append(mcq(c + "What date comes just <b>after</b> 19 May?", dt(M, after), [dt(M, 18), dt(M, 26), dt(M, 21)],
                   "The next date is one more: 19 + 1 = <b>20 May</b>. (26 May is the date under it, one week later.)"))
    its.append(mcq(c + "What date comes just <b>before</b> 10 May?", dt(M, 9), [dt(M, 11), dt(M, 3), dt(M, 8)],
                   "The date before is one less: 10 − 1 = <b>9 May</b>. On the calendar, 9 is at the end of the row "
                   "above. (3 May is the date above 10, one week earlier.)"))
    suns = [d for d in range(1, days + 1) if wd(M, d) == "Sunday"]
    assert len(suns) == 5
    its.append(mcq(c + "How many <b>Sundays</b> are in May 2027?", "5", ["4", "7", "30"],
                   "The Sundays are %s. That is <b>5 Sundays</b>. (30 is the last Sunday’s date.)"
                   % ", ".join(map(str, suns))))
    fris = [d for d in range(1, days + 1) if wd(M, d) == "Friday"]
    assert fris[:3] == [7, 14, 21]
    its.append(mcq(c + "What is the date of the <b>second Friday</b> in May?", "14 May", ["7 May", "21 May", "13 May"],
                   "The Fridays are %s. The second one is <b>14 May</b>. (7 May is the first Friday.)"
                   % ", ".join(map(str, fris))))
    weds = [d for d in range(1, days + 1) if wd(M, d) == "Wednesday"]
    assert weds[-1] == 26
    its.append(mcq(c + "What is the date of the <b>last Wednesday</b> in May?", "26 May", ["5 May", "31 May", "27 May"],
                   "Go down the Wed column to the bottom: 5, 12, 19, 26. The last one is <b>26 May</b>. "
                   "(31 May is the last date, but it is a Monday.)"))
    assert wd(M, 15) == "Saturday" and all(wd(M, d) != "Saturday" for d in (14, 16, 17))
    its.append(mcq(c + "Which date is a <b>Saturday</b>?", "15 May", ["14 May", "16 May", "17 May"],
                   "Look in the Sat column: 1, 8, <b>15</b>, 22, 29. So 15 May is a Saturday. "
                   "(14 May is a Friday and 16 May is a Sunday.)"))
    assert wd(M, 31) == "Monday"
    its.append(mcq(c + "What day of the week is <b>31 May</b>?", "Monday", ["Sunday", "Saturday", "Friday"],
                   "31 is on its own row, in the Mon column. 31 May is a <b>Monday</b>."))
    # August 2027 with two events
    M = 8
    bday, sport = 18, 6
    c2 = fig(calendar_svg(M, box=sport, circle=bday, legend=[("box", "sports day"), ("circle", "Isla’s birthday")]))
    its.append(mcq(c2 + "Isla’s birthday is circled. What is the date?", dt(M, bday), [dt(M, 17), dt(M, 19), dt(M, 11)],
                   "The circle is around 18. Isla’s birthday is <b>18 August</b>."))
    assert wd(M, bday) == "Wednesday"
    its.append(mcq(c2 + "What day of the week is Isla’s birthday?", "Wednesday", ["Tuesday", "Thursday", "Monday"],
                   "Go up from the circled 18 to the top of its column: <b>Wednesday</b>."))
    assert wd(M, sport) == "Friday"
    its.append(mcq(c2 + "Sports day is in the green box. What day of the week is it?", "Friday",
                   ["Thursday", "Saturday", "Monday"],
                   "Go up from 6 to the top of its column: <b>Friday</b>. So sports day is Friday 6 August."))
    mons = [d for d in range(1, 32) if wd(M, d) == "Monday"]
    assert len(mons) == 5 and mons[-1] == 30
    its.append(mcq(c2 + "How many <b>Mondays</b> are in August 2027?", "5", ["4", "6", "30"],
                   "The Mondays are %s. That is <b>5 Mondays</b>. (30 is the date of the last one.)"
                   % ", ".join(map(str, mons))))
    assert calendar.monthrange(Y, 8)[1] == 31
    its.append(mcq(c2 + "What is the date of the <b>last day</b> of August?", "31 August",
                   ["30 August", "1 August", "31 July"],
                   "The last number on the calendar is 31. So the last day is <b>31 August</b>. "
                   "(August has 31 days, not 30.)"))
    assert wd(8, 31) == "Tuesday" and wd(9, 1) == "Wednesday"
    its.append(mcq(c2 + "What day of the week will <b>1 September</b> be?", "Wednesday",
                   ["Monday", "Tuesday", "Thursday"],
                   "31 August is a Tuesday. 1 September is the next day, so it is a <b>Wednesday</b>. "
                   "(A new month does not always start on Monday.)"))
    assert wd(8, 1) == "Sunday" and wd(7, 31) == "Saturday"
    its.append(mcq(c2 + "What day of the week was <b>31 July</b>?", "Saturday", ["Sunday", "Monday", "Friday"],
                   "1 August is a Sunday. 31 July is the day before, so it was a <b>Saturday</b>."))
    assert len(its) == 20
    order = [0, 1, 2, 3, 6, 7, 12, 13, 4, 14, 5, 15, 10, 8, 9, 11, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Read a month calendar", "items": [its[i] for i in order]}


# ============================================================ set 3: next Tuesday, tomorrow, 1 week later
def set_next():
    its = []
    M, T = 6, 9
    assert wd(M, T) == "Wednesday"
    c = cal(M, box=T)
    pre = c + "Today is <b>Wednesday 9 June</b>. "
    its.append(mcq(pre + "What is the date <b>tomorrow</b>?", dt(M, 10), [dt(M, 8), dt(M, 16), dt(M, 11)],
                   "Tomorrow is the next day: 9 + 1 = <b>10 June</b>. (8 June was yesterday.)"))
    its.append(mcq(pre + "What was the date <b>yesterday</b>?", dt(M, 8), [dt(M, 10), dt(M, 2), dt(M, 7)],
                   "Yesterday is the day before: 9 − 1 = <b>8 June</b>. (10 June is tomorrow.)"))
    assert wd(M, 12) == "Saturday"
    its.append(mcq(pre + "What day of the week will it be in <b>3 days</b>?", "Saturday",
                   ["Friday", "Sunday", "Thursday"],
                   "Count on from Wednesday: Thursday (1), Friday (2), Saturday (3). It will be <b>Saturday</b>. "
                   "(Friday counts Wednesday as day 1.)"))
    assert wd(M, 14) == "Monday" and wd(M, 7) == "Monday"
    its.append(mcq(pre + "What is the date of the <b>next Monday</b>?", dt(M, 14), [dt(M, 7), dt(M, 21), dt(M, 13)],
                   "Go forward from the box to the next date in the Mon column: <b>14 June</b>. "
                   "(7 June was the Monday that has gone. 13 June is a Sunday.)"))
    assert wd(M, 15) == "Tuesday"
    its.append(mcq(pre + "What is the date of the <b>next Tuesday</b>?", dt(M, 15), [dt(M, 8), dt(M, 22), dt(M, 16)],
                   "Go forward from the box to the next date in the Tue column: <b>15 June</b>. "
                   "(8 June was last Tuesday. 22 June is the Tuesday after that.)"))
    its.append(mcq(pre + "What is the date <b>1 week</b> from today?", dt(M, 16), [dt(M, 15), dt(M, 10), dt(M, 23)],
                   "1 week = 7 days. 9 + 7 = 16. Go straight down one row: <b>16 June</b>. "
                   "(15 June counts today as one of the 7 days.)"))
    its.append(mcq(pre + "What is the date <b>2 weeks</b> from today?", dt(M, 23), [dt(M, 22), dt(M, 16), dt(M, 11)],
                   "2 weeks = 14 days. 9 + 14 = 23. Go straight down two rows: <b>23 June</b>. "
                   "(16 June is only 1 week. 11 June is 2 days, not 2 weeks.)"))
    its.append(mcq(pre + "What was the date <b>1 week ago</b>?", dt(M, 2), [dt(M, 16), dt(M, 3), dt(M, 8)],
                   "1 week ago is 7 days back: 9 − 7 = 2. Go straight up one row: <b>2 June</b>. "
                   "(16 June is 1 week from now, not 1 week ago.)"))
    its.append(mcq(pre + "What is the date <b>5 days</b> after today?", dt(M, 14), [dt(M, 13), dt(M, 4), dt(M, 15)],
                   "9 + 5 = <b>14 June</b>. Count the jumps: 10, 11, 12, 13, 14. (13 June counts today as day 1.)"))
    its.append(mcq(pre + "What was the date <b>4 days</b> before today?", dt(M, 5), [dt(M, 6), dt(M, 13), dt(M, 4)],
                   "9 − 4 = <b>5 June</b>. Count back: 8, 7, 6, 5. (6 June counts today as one of the days. "
                   "13 June is 4 days after.)"))
    M, T = 10, 15
    assert wd(M, T) == "Friday"
    c = cal(M, box=T)
    pre = c + "Today is <b>Friday 15 October</b>. "
    its.append(mcq(pre + "What day of the week will it be <b>tomorrow</b>?", "Saturday",
                   ["Thursday", "Sunday", "Monday"],
                   "The day after Friday is <b>Saturday</b>. (Thursday was yesterday.)"))
    assert wd(M, 18) == "Monday"
    its.append(mcq(pre + "What is the date of the <b>next Monday</b>?", dt(M, 18), [dt(M, 11), dt(M, 25), dt(M, 17)],
                   "Go forward to the next date in the Mon column: <b>18 October</b>. (11 October was last Monday.)"))
    assert wd(M, 19) == "Tuesday"
    its.append(mcq(pre + "What is the date of the <b>next Tuesday</b>?", dt(M, 19), [dt(M, 12), dt(M, 26), dt(M, 20)],
                   "Go forward to the next date in the Tue column: <b>19 October</b>. (12 October was last Tuesday.)"))
    assert wd(M, 21) == "Thursday"
    its.append(mcq(pre + "The class goes to the library every <b>Thursday</b>. What is the date of the next library day?",
                   dt(M, 21), [dt(M, 14), dt(M, 28), dt(M, 22)],
                   "Go forward to the next date in the Thu column: <b>21 October</b>. "
                   "(14 October was yesterday, so that library day has gone.)"))
    its.append(mcq(pre + "What day of the week will it be <b>1 week</b> from today?", "Friday",
                   ["Thursday", "Saturday", "Monday"],
                   "1 week later is 7 days later. It is always the <b>same day</b> of the week: <b>Friday</b> 22 October."))
    assert wd(M, 13) == "Wednesday"
    its.append(mcq(pre + "What was the date <b>last Wednesday</b>?", dt(M, 13), [dt(M, 20), dt(M, 6), dt(M, 14)],
                   "Go back to the Wed column in this row: <b>13 October</b>. (20 October is next Wednesday.)"))
    its.append(mcq(pre + "What is the date <b>10 days</b> from today?", dt(M, 25), [dt(M, 24), dt(M, 5), dt(M, 26)],
                   "15 + 10 = <b>25 October</b>. (24 October counts today as one of the 10 days. 5 October counts back.)"))
    its.append(mcq(pre + "What is the date <b>2 weeks</b> from today?", dt(M, 29), [dt(M, 28), dt(M, 22), dt(M, 17)],
                   "2 weeks = 14 days. 15 + 14 = 29. Go down two rows: <b>29 October</b>. (22 October is only 1 week.)"))
    assert nxt("Tuesday", 7) == "Tuesday"
    its.append(mcq("Today is <b>Tuesday</b>. What day will it be in <b>7 days</b>?", "Tuesday",
                   ["Monday", "Wednesday", "Sunday"],
                   "7 days is 1 week. After 1 week it is the same day again: <b>Tuesday</b>. "
                   "(Monday counts today as one of the 7 days.)"))
    assert wd(10, 28) == "Thursday" and calendar.monthrange(Y, 10)[1] == 31 and wd(11, 1) == "Monday"
    its.append(mcq("Today is <b>Thursday 28 October</b>. October has 31 days. What is the date of the <b>next Monday</b>?",
                   "1 November", ["32 October", "31 October", "25 October"],
                   "Count on: Friday 29, Saturday 30, Sunday 31 October. October ends on the 31st, so Monday is "
                   "<b>1 November</b>. (There is no 32 October. 25 October was last Monday.)"))
    assert len(its) == 20
    order = [0, 1, 10, 2, 5, 14, 3, 4, 11, 12, 13, 7, 15, 8, 9, 6, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Tomorrow, next Tuesday and 1 week later", "items": [its[i] for i in order]}


# ============================================================ set 4: days between events
def between(q, a, b, extra_wrong, e_extra=""):
    n = b - a
    assert n > 0
    e = ("Count the jumps from %d to %d. Do not count the start day. %d − %d = <b>%d</b>.%s "
         "(%d counts the start day as well.%s)"
         % (a, b, b, a, n, e_extra, n + 1, " %d adds the dates." % extra_wrong if extra_wrong == a + b else ""))
    return mcq(q, str(n), [str(n + 1), str(n - 1), str(extra_wrong)], e)


def set_between():
    its = []
    M = 9
    its.append(between(cal(M, 3, 10, "sports day") + "Today is 3 September. How many days until sports day?",
                       3, 10, 13, ""))
    its.append(between(cal(M, 6, 15, "Ava’s birthday") + "Today is 6 September. How many days until Ava’s birthday?",
                       6, 15, 21, ""))
    its.append(between(cal(M, 14, 18, "Kai’s party") + "Today is 14 September. How many <b>sleeps</b> until Kai’s party?",
                       14, 18, 32, " Each sleep is one night: 14, 15, 16, 17."))
    its.append(between(cal(M, 1, 24, "last day of term") + "Today is 1 September. How many days until the last day of term?",
                       1, 24, 25, ""))
    M = 11
    assert 16 - 2 == 14
    its.append(mcq(cal(M, 2, 16, "swimming carnival") + "Today is 2 November. How many <b>weeks</b> until the swimming carnival?",
                   "2 weeks", ["3 weeks", "14 weeks", "1 week"],
                   "16 is 2 rows straight below 2. Each row down is 1 week. 16 − 2 = 14 days = <b>2 weeks</b>. "
                   "(3 weeks counts the rows instead of the jumps. 14 is days, not weeks.)"))
    its.append(between(cal(M, 8, 26, "school concert") + "Today is 8 November. How many days until the school concert?",
                       8, 26, 34, ""))
    its.append(between(fig(calendar_svg(M, box=5, circle=19, legend=[("box", "Mia’s birthday"), ("circle", "Jack’s birthday")]))
                       + "How many days is it from Mia’s birthday to Jack’s birthday?", 5, 19, 24,
                       " That is 2 weeks: 19 is 2 rows below 5."))
    its.append(between(fig(calendar_svg(M, box=12, circle=15, legend=[("box", "book due"), ("circle", "book returned")]))
                       + "A library book is due on 12 November. Noah returns it on 15 November. How many days late is it?",
                       12, 15, 27, " The book was not late on the due day."))
    its.append(between(cal(M, 22, 30, "end of November") + "Today is 22 November. How many days until 30 November?",
                       22, 30, 52, ""))
    M = 2
    assert calendar.monthrange(Y, 2)[1] == 28
    its.append(between(cal(M, 1, 9, "school photos") + "Today is 1 February. How many days until school photos?",
                       1, 9, 10, ""))
    its.append(between(cal(M, 10, 25, "athletics carnival") + "Today is 10 February. How many days until the athletics carnival?",
                       10, 25, 35, ""))
    its.append(mcq(cal(M, 3) + "Today is 3 February. The school fete is in <b>2 weeks</b>. What is the date of the fete?",
                   dt(M, 17), [dt(M, 16), dt(M, 10), dt(M, 5)],
                   "2 weeks = 14 days. 3 + 14 = 17. Go straight down two rows: <b>17 February</b>. "
                   "(16 February counts today as day 1. 10 February is only 1 week. 5 February is 2 days.)"))
    its.append(between(cal(M, 15, 28, "last day of February") + "Today is 15 February. How many days until the last day of February?",
                       15, 28, 43, " February 2027 has 28 days."))
    # text only
    its.append(between("Grace’s birthday is on <b>27 May</b>. Today is <b>19 May</b>. How many days until her birthday?",
                       19, 27, 46, ""))
    its.append(between("The class plants seeds on <b>3 March</b>. The first flower opens on <b>17 March</b>. "
                       "How many days does it take?", 3, 17, 20, " That is 2 weeks."))
    assert 30 - 29 + 3 == 4
    its.append(mcq("Today is <b>29 June</b>. June has 30 days. The school holidays start on <b>3 July</b>. "
                   "How many days until the holidays?", "4", ["5", "26", "3"],
                   "Count the jumps: 29 June to 30 June is 1. 30 June to 3 July is 3 more (1, 2, 3 July). "
                   "1 + 3 = <b>4 days</b>. (5 counts today as well. 26 is 29 − 3.)"))
    assert 15 + 3 == 18
    its.append(mcq("Isla’s family goes camping on <b>15 March</b>. They stay <b>3 nights</b>. "
                   "What date do they come home?", dt(3, 18), [dt(3, 17), dt(3, 19), dt(3, 12)],
                   "One night for each jump: 15 to 16, 16 to 17, 17 to 18. 15 + 3 = <b>18 March</b>. "
                   "(17 March counts the first day as one of the nights. 12 March counts back.)"))
    its.append(mcq("Liam plants a bean seed on <b>7 June</b>. It sprouts <b>10 days later</b>. On what date does it sprout?",
                   dt(6, 17), [dt(6, 16), dt(6, 18), dt(6, 10)],
                   "7 + 10 = <b>17 June</b>. (16 June counts 7 June as one of the 10 days. 10 June uses the 10 as a date.)"))
    its.append(mcq("Today is <b>12 August</b>. Book Week is in <b>2 weeks</b>. What date is that?",
                   dt(8, 26), [dt(8, 25), dt(8, 19), dt(8, 14)],
                   "2 weeks = 14 days. 12 + 14 = <b>26 August</b>. (19 August is only 1 week. 14 August is 2 days.)"))
    assert 27 - 20 == 7
    its.append(between("Kai’s cousin comes to stay on <b>20 April</b> and goes home on <b>27 April</b>. "
                       "How many nights does she stay?", 20, 27, 47, " One night for each jump. That is 1 week."))
    assert len(its) == 20
    for it in its:
        assert len(set(it["c"])) == 4
    order = [0, 1, 2, 9, 3, 5, 10, 8, 4, 6, 7, 12, 11, 13, 14, 19, 15, 16, 17, 18]
    assert sorted(order) == list(range(20))
    return {"title": "Count the days between events", "items": [its[i] for i in order]}


# ============================================================ set 5: seasons and school holidays
def set_seasons(people):
    its = []
    assert season_of(1) == "Summer" and season_of(7) == "Winter" and season_of(10) == "Spring" and season_of(4) == "Autumn"
    its.append(mcq("In Australia, which season is <b>January</b>?", "Summer", ["Winter", "Autumn", "Spring"],
                   "In Australia, summer is December, January and February. January is <b>summer</b>. "
                   "(It is winter in January in countries like England and the USA, not in Australia.)"))
    its.append(mcq("In Australia, which season is <b>July</b>?", "Winter", ["Summer", "Autumn", "Spring"],
                   "In Australia, winter is June, July and August. July is <b>winter</b>. "
                   "(Countries in the north of the world have summer in July.)"))
    its.append(mcq("How many <b>seasons</b> are in a year?", "4", ["12", "3", "2"],
                   "Summer, autumn, winter and spring: <b>4 seasons</b>. (12 is the number of months.)"))
    its.append(mcq("How many <b>months</b> are in each season?", "3", ["4", "12", "2"],
                   "12 months shared into 4 seasons is 3 each. Each season has <b>3 months</b>."))
    its.append(mcq(fig(seasons_svg(miss_season="Spring")) + "Which season is missing?", "Spring",
                   ["Autumn", "Summer", "Winter"],
                   "The seasons go summer, autumn, winter, <b>spring</b>. September, October and November are spring."))
    its.append(mcq(fig(seasons_svg(miss_month=7)) + "Which month is missing?", "July", ["January", "June", "September"],
                   "Winter is Jun, <b>Jul</b>, Aug. The missing month is <b>July</b>. (January is in summer.)"))
    its.append(mcq("Which season comes <b>after</b> summer?", "Autumn", ["Spring", "Winter", "Summer"],
                   "The seasons go summer, <b>autumn</b>, winter, spring, and then summer again. "
                   "(Spring comes <b>before</b> summer.)"))
    its.append(mcq("Which months are <b>summer</b> in Australia?", "December, January and February",
                   ["June, July and August", "March, April and May", "September, October and November"],
                   "In Australia it is hot in <b>December, January and February</b>. That is summer. "
                   "(June, July and August is summer in the north of the world, but winter here.)"))
    its.append(mcq("Which months are <b>winter</b> in Australia?", "June, July and August",
                   ["December, January and February", "March, April and May", "September, October and November"],
                   "In Australia it is cold in <b>June, July and August</b>. That is winter."))
    assert season_of(12) == "Summer"
    its.append(mcq("Christmas Day is on <b>25 December</b>. Which season is that in Australia?", "Summer",
                   ["Winter", "Spring", "Autumn"],
                   "December is in summer in Australia, so Christmas is in <b>summer</b>. Many families go to the beach. "
                   "(Christmas is in winter in England, not here.)"))
    assert season_of(4) == "Autumn"
    its.append(mcq("Anzac Day is on <b>25 April</b>. Which season is that in Australia?", "Autumn",
                   ["Spring", "Winter", "Summer"],
                   "Autumn is March, April and May. So 25 April is in <b>autumn</b>. "
                   "(Spring is in the north of the world in April, not in Australia.)"))
    nm, pr = next(people)
    its.append(mcq("%s’s birthday is in <b>October</b>. Which season is that in Australia?" % nm, "Spring",
                   ["Autumn", "Summer", "Winter"],
                   "Spring is September, October and November. So October is in <b>spring</b>. "
                   "(October is autumn in England and the USA.)"))
    its.append(mcq("It is <b>winter</b> in Australia. Which month could it be?", "August",
                   ["February", "December", "May"],
                   "Winter is June, July and <b>August</b>. (February and December are summer. May is autumn.)"))
    nm, pr = next(people)
    its.append(mcq("%s’s birthday is in <b>summer</b>. Which month could it be?" % nm, "February",
                   ["July", "May", "October"],
                   "Summer in Australia is December, January and <b>February</b>. (July is winter here.)"))
    its.append(mcq("Matilda visits Hobart in <b>July</b>. What will the weather be like?", "Cold: it is winter",
                   ["Hot: it is summer", "Warm: it is spring", "Cool: it is autumn"],
                   "July is winter in Australia, so Hobart will be <b>cold</b>. Pack a warm jacket!"))
    its.append(mcq("In Australia, the long <b>summer holidays</b> are in which months?", "December and January",
                   ["June and July", "April and May", "September and October"],
                   "The long holidays are in summer, at the end of one school year and the start of the next: "
                   "<b>December and January</b>. (June and July is the long summer break in the north of the world.)"))
    its.append(mcq("How many school <b>terms</b> are in a year in Australian schools?", "4", ["2", "3", "12"],
                   "Australian schools have <b>4 terms</b> a year, with holidays between them."))
    its.append(mcq("The winter holidays are <b>2 weeks</b> long. How many days is that?", "14", ["10", "7", "2"],
                   "1 week = 7 days. 7 + 7 = <b>14 days</b>. (10 is the school days in 2 weeks, but holidays count every day.)"))
    assert wd(7, 3) == "Saturday" and wd(7, 19) == "Monday"
    its.append(mcq(fig(calendar_svg(7, box=3, circle=19, legend=[("box", "holidays start"), ("circle", "back to school")]))
                   + "The winter holidays start on Saturday 3 July. School goes back on Monday 19 July. "
                   "How many days is that?", "16", ["17", "15", "22"],
                   "Count the jumps from 3 to 19. 19 − 3 = <b>16 days</b>. (17 counts the start day as well. 22 adds the dates.)"))
    assert 25 - 18 == 7
    its.append(mcq(cal(12, 18, 25, "Christmas Day") + "Today is 18 December. How many <b>sleeps</b> until Christmas Day?",
                   "7", ["8", "6", "43"],
                   "25 is straight below 18, so it is 1 week. 25 − 18 = <b>7 sleeps</b>. "
                   "(8 counts today as well. 43 adds the dates.)"))
    assert len(its) == 20
    order = [2, 3, 0, 1, 6, 4, 5, 9, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Seasons in Australia and school holidays", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Days and months in order</h2>"
        "<p>A week has <b>7 days</b>. A year has <b>12 months</b>. Say them in order every day.</p>"
        + table(["", "In order"], [
            ["Days (7)", "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"],
            ["Months (12)", "January, February, March, April, May, June, July, August, September, October, November, December"]]) +
        "<p>After Sunday a new week starts. After December a new year starts.</p>"
        "<h2>Reading a calendar</h2>"
        "<p>Each row is <b>1 week</b>. Each column is one day of the week. Find the date, then go up to the top "
        "to see the day.</p>"
        "<figure class='sn-fig'>" + calendar_svg(9, box=3, circle=10, legend=[("box", "today"), ("circle", "sports day")]) +
        "<figcaption>Today is Friday 3 September. Sports day is Friday 10 September. 10 is straight below 3, so it is "
        "<b>1 week</b> later.</figcaption></figure>"
        + ex("Next Tuesday", "Today is Wednesday 9 June. What is the date of the next Tuesday?",
             "Go forward from 9 to the next date in the Tue column.", "15 June") +
        "<h2>How many days between?</h2>"
        "<p>Count the <b>jumps</b>, not the boxes. Do not count today: no time has passed yet. "
        "You can also take away: later date − earlier date.</p>"
        + ex("Sports day", "Today is 3 September. Sports day is 10 September. How many days until sports day?",
             "Jumps: 4, 5, 6, 7, 8, 9, 10. That is 7 jumps. Or 10 − 3 = 7.", "7 days") +
        ex("A birthday", "Today is 14 September. Kai’s party is on 18 September. How many sleeps?",
           "18 − 14 = 4. The sleeps are the nights of 14, 15, 16 and 17 September.", "4 sleeps") +
        "<h2>Seasons in Australia</h2>"
        "<p>Australia is in the south of the world. Our seasons are the <b>opposite</b> of England and the USA. "
        "Christmas is in summer here.</p>"
        "<figure class='sn-fig'>" + seasons_svg() +
        "<figcaption>Summer: December, January, February. Autumn: March, April, May. "
        "Winter: June, July, August. Spring: September, October, November.</figcaption></figure>"
        "<p>Australian schools have <b>4 terms</b>. The long summer holidays are in December and January.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting today: 3 to 10 September is 8 days", "Count the jumps: 10 − 3 = 7 days"],
            ["Months out of order: May, July, June", "Say them in order: May, June, July"],
            ["After December comes “13th month”", "After December a new year starts: January"],
            ["July is summer", "In Australia July is winter. Summer is December to February"],
            ["Every month starts on Monday", "Look at the calendar: 1 May 2027 is a Saturday"],
        ])
    )


FAQ = [
    {"q": "What do Year 2 students learn about calendars in Australia?",
     "a": "In the Australian Curriculum v9.0 (AC9M2M03), Year 2 students find the date on a calendar and work out the number of days between events, such as from today to a birthday or sports day."},
    {"q": "How do you count the days between two dates?",
     "a": "Count the jumps from one date to the next, not the boxes, and do not count the start day. From 3 September to 10 September is 10 − 3 = 7 days."},
    {"q": "What are the seasons in Australia?",
     "a": "Summer is December, January and February; autumn is March to May; winter is June to August; spring is September to November. They are the opposite of the seasons in Europe and North America."},
    {"q": "How can I help my child learn the days and months?",
     "a": "Keep a calendar on the fridge, cross off each day and count the sleeps to birthdays and holidays together. Say the days and months in order, and talk about which season each month is in."},
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


PEOPLE = [("Mia", "she"), ("Noah", "he"), ("Zara", "she"), ("Cooper", "he"), ("Ruby", "she"), ("Ethan", "he")]


def gen():
    rnd = random.Random(2811)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people)
    sets = [set_order(), set_read(), set_next(), set_between(), set_seasons(people)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    u = {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "calendars-and-dates", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 2 Calendars and Dates",
        "seo_title": "Year 2 Calendar Worksheets: Days, Months, Dates and Seasons (Free, with Answer Key)",
        "short_title": "Calendars and dates",
        "domain": "Measurement",
        "standard_code": "AC9M2M03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Identify the date and determine the number of days between events using calendars",
        "meta_desc": "Free Year 2 maths worksheets on calendars for the Australian Curriculum (AC9M2M03): days of the week and months in order, reading a month calendar, finding next Tuesday, counting the days between events and Australian seasons and school holidays. 100 questions with an answer key.",
        "key_big": "Count the jumps, not the boxes: do not count today.",
        "key_sub": "Each row of a calendar is 1 week. From 3 September to 10 September is 10 − 3 = 7 days. In Australia summer is December to February and winter is June to August.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    for p in ("calendar", "days in a row", "months in a row", "months of the year", "seasons"):
        mark_large(u, p)
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
