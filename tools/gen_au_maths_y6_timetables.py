# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Timetables and Itineraries (Australian Curriculum v9.0, AC9M6M03)
  python3 tools/gen_au_maths_y6_timetables.py
Every timetable is built from a list of departure times and the minutes between stops, and every answer is
worked out in code from minutes since midnight. Wrong answers come from real student mistakes: reading the
wrong row (the next stop) or the wrong column (the next service), an hour counted as 100 minutes, am and pm
mixed up (3:45 pm read as 13:45 or 15:45 read as 5:45 pm), adding instead of counting back when planning,
catching a service that arrives just too late, and forgetting the part of a journey after midnight.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
HL = "#fff1b8"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Charlotte", "she"), ("Oliver", "he"), ("Isla", "she"), ("Jack", "he"), ("Mia", "she"), ("Noah", "he"),
          ("Amelia", "she"), ("William", "he"), ("Ava", "she"), ("Leo", "he"), ("Harper", "she"), ("Lachlan", "he"),
          ("Chloe", "she"), ("Liam", "he"), ("Ruby", "she"), ("Aarav", "he"), ("Mei", "she"), ("Kai", "he"),
          ("Zara", "she"), ("Cooper", "he"), ("Matilda", "she"), ("Ethan", "he"), ("Sienna", "she"), ("Grace", "she")]
HIS = {"she": "her", "he": "his"}
DAY = 24 * 60


def T(h, m):
    return h * 60 + m


# ------------------------------------------------------------ time formats
def h12(h24):
    return (h24 - 1) % 12 + 1


def f24(t):
    if t is None:
        return None
    t %= DAY
    return "%02d:%02d" % (t // 60, t % 60)


def f12(t):
    if t is None:
        return None
    t %= DAY
    h = t // 60
    return "%d:%02d %s" % (h12(h), t % 60, "am" if h < 12 else "pm")


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


def sdur(n):
    return dur(n) if n and n > 0 else None


def raw_dur(hh, mm):
    if hh <= 0:
        return mins(mm) if mm > 0 else None
    return "%d hour%s" % (hh, "" if hh == 1 else "s") + (" %s" % mins(mm) if mm else "")


def dur_value(s):
    v = 0
    for n, unit in re.findall(r"(\d+) (hour|minute)", s):
        v += int(n) * (60 if unit == "hour" else 1)
    return v


def naive100(t1, t2):
    """the 100-minutes-in-an-hour mistake: 16:10 - 14:35 done as 1610 - 1435 = 175 -> 1 hour 75 minutes"""
    a = (t1 // 60) * 100 + t1 % 60
    b = (t2 // 60) * 100 + t2 % 60
    n = b - a
    if n <= 0:
        return None
    return raw_dur(n // 100, n % 100)


def hour_minute_diff(t1, t2):
    """hours subtracted, minutes subtracted the wrong way round: 14:35 to 16:10 -> 2 hours 25 minutes"""
    hh = t2 // 60 - t1 // 60
    mm = abs(t2 % 60 - t1 % 60)
    return raw_dur(hh, mm) if hh > 0 or mm > 0 else None


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


def text_w(s, size=16):
    """rough width of Arial text"""
    return len(s) * size * 0.55


def jump_label(n):
    hh, mm = divmod(n, 60)
    if not hh:
        return "+%d min" % mm
    if not mm:
        return "+%d h" % hh
    return "+%d h %d min" % (hh, mm)


def jumps(t1, t2):
    """start -> next o'clock -> last o'clock -> end (absolute minutes, t2 may be the next day)"""
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


def timeline_svg(t1, t2, fmt=f24, W=460):
    """An open number line (not to scale): equal spaces, each jump labelled."""
    pts = jumps(t1, t2)
    L, R, Y = 52, W - 52, 72
    n = len(pts) - 1

    def X(i):
        return L + (R - L) * i / float(n)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i, t in enumerate(pts):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X(i), Y - 10, X(i), Y + 10, LINE))
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X(i), Y + 32, LINE, fmt(t)))
    for i in range(n):
        x1, x2 = X(i), X(i + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1 + 4, Y - 12, (x1 + x2) / 2, Y - 54, x2 - 4, Y - 12, RED))
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % ((x1 + x2) / 2, Y - 40, RED, jump_label(pts[i + 1] - pts[i])))
    return svg_wrap(W, 114, "".join(s), "time line from %s to %s" % (fmt(t1), fmt(t2)))


def count_on(t1, t2, fmt=f24):
    """Explanation: count on in jumps."""
    pts = jumps(t1, t2)
    parts = ["%s to %s is %s" % (fmt(a), fmt(b), dur(b - a)) for a, b in zip(pts, pts[1:])]
    d = t2 - t1
    if len(parts) == 1:
        return "Count on: %s. So it is <b>%s</b>." % (parts[0], dur(d))
    terms = [dur(b - a) for a, b in zip(pts, pts[1:])]
    hrs = [x for x in terms if "minute" not in x]
    mns = [x for x in terms if "minute" in x]
    return "Count on: %s. %s = <b>%s</b>." % (", ".join(parts), " + ".join(hrs + mns), dur(d))


def dur_q(q, t1, t2, extra=(), fmt=f24, note=""):
    """How long from t1 to t2 (t2 may be the next day)."""
    d = t2 - t1
    assert d > 0
    c = list(extra)
    if t2 < DAY:
        c += [naive100(t1, t2), hour_minute_diff(t1, t2)]
    c += [sdur(d + 10), sdur(d - 10), sdur(d + 60), sdur(d - 60), sdur(d + 5), sdur(d - 5)]
    e = note + count_on(t1, t2, fmt)
    if t2 < DAY and naive100(t1, t2) and dur_value(naive100(t1, t2)) != d:
        e += " (An hour has 60 minutes, not 100, so do not just subtract the numbers.)"
    return mcq(q, dur(d), c, e, key=dur_value)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ timetables
class TT(object):
    """A timetable: stops down the side, one column per service (None = does not stop)."""

    def __init__(self, title, vehicle, stops, offsets, deps, skip=None):
        self.title, self.vehicle, self.stops = title, vehicle, stops
        self.cols = []
        for j, d in enumerate(deps):
            off = offsets if not skip or j not in skip else skip[j]
            self.cols.append([None if o is None else d + o for o in off])

    def t(self, j, i):
        if 0 <= j < len(self.cols) and 0 <= i < len(self.stops):
            return self.cols[j][i]
        return None

    def ft(self, j, i):
        return f24(self.t(j, i))

    def svg(self, hl=None):
        n = len(self.cols)
        LW = int(max(text_w(s) for s in self.stops + [self.title[:0]]) + 22)
        CW, RH = 70, 30
        W = LW + CW * n + 4
        H = RH * (len(self.stops) + 1) + 4
        s = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (W - 4, RH, GREEN)]
        s.append("<text x='10' y='23' font-size='15' font-weight='700' fill='#fff'>%s</text>" % self.title)
        for i, st in enumerate(self.stops):
            y = 2 + RH * (i + 1)
            if i % 2:
                s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
        if hl is not None:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (2 + LW + CW * hl, 2 + RH, CW, RH * len(self.stops), HL))
        for i, st in enumerate(self.stops):
            y = 2 + RH * (i + 1)
            s.append("<text x='10' y='%d' font-size='16' fill='%s'>%s</text>" % (y + 21, LINE, st))
            for j, col in enumerate(self.cols):
                s.append("<text x='%.0f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (2 + LW + CW * j + CW / 2.0, y + 21, LINE, f24(col[i]) if col[i] is not None else "—"))
        s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, LINE))
        for j in range(n):
            x = 2 + LW + CW * j
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, 2 + RH, x, H - 2, LINE))
        return svg_wrap(W, H, "".join(s), "timetable: %s" % self.title)


def grid_svg(label, title, rows, widths=(70, 196)):
    """Itinerary picture: a title bar, then time | activity pairs in two halves side by side."""
    RH = 30
    half = (len(rows) + 1) // 2
    pair = sum(widths)
    W = pair * 2 + 4
    H = RH * (half + 1) + 4
    s = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (W - 4, RH, GREEN),
         "<text x='10' y='23' font-size='15' font-weight='700' fill='#fff'>%s</text>" % title]
    for r in range(half):
        y = 2 + RH * (r + 1)
        if r % 2:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
    for k, (t, act) in enumerate(rows):
        r, side = k % half, k // half
        y = 2 + RH * (r + 1)
        x0 = 2 + pair * side
        assert text_w(act) < widths[1] - 12, act
        s.append("<text x='%.0f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x0 + widths[0] / 2.0, y + 21, LINE, f24(t)))
        s.append("<text x='%d' y='%d' font-size='16' fill='%s'>%s</text>" % (x0 + widths[0] + 8, y + 21, LINE, act))
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, LINE))
    for x in (2 + widths[0], 2 + pair, 2 + pair + widths[0]):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, 2 + RH, x, H - 2, LINE, "1.5" if x == 2 + pair else "1"))
    return svg_wrap(W, H, "".join(s), label)


PLURAL = {"bus": "buses", "train": "trains", "ferry": "ferries"}
ORD = ["first", "second", "third", "fourth", "fifth"]

# Set 1 timetables (real Australian routes; times are typical, not an official timetable)
MEL = TT("Frankston line: Monday morning", "train",
         ["Flinders Street", "Richmond", "Caulfield", "Cheltenham", "Frankston"], [0, 4, 15, 30, 59],
         [T(7, 12), T(7, 24), T(7, 39), T(7, 51)], skip={2: [0, 4, 15, None, 52]})
BNE = TT("Bus: City to Carindale", "bus",
         ["City (Queen Street)", "South Bank", "Woolloongabba", "Coorparoo", "Carindale"], [0, 6, 11, 19, 33],
         [T(15, 5), T(15, 35), T(15, 58), T(16, 25)])
SYD = TT("Parramatta River ferry", "ferry",
         ["Circular Quay", "Balmain", "Cockatoo Island", "Sydney Olympic Park", "Parramatta"], [0, 12, 21, 53, 79],
         [T(10, 20), T(11, 5), T(11, 50), T(12, 35)])
PER = TT("Perth to Fremantle: Saturday night", "train",
         ["Perth", "Subiaco", "Claremont", "Cottesloe", "Fremantle"], [0, 6, 14, 19, 28],
         [T(22, 15), T(22, 45), T(23, 15), T(23, 45)])


# ============================================================ set 1: read timetables
def k_arrive(tt, j, a, b, people):
    nm, pr = next(people)
    right = tt.ft(j, b)
    c = [tt.ft(j, b - 1), tt.ft(j, b + 1), tt.ft(j + 1, b), tt.ft(j - 1, b), tt.ft(j + 2, b)]
    e = ("Find %s in the %s row. Go down <b>that column</b> to the %s row: <b>%s</b>. "
         "(Stay in the same column: the times next to it belong to other %s.)"
         % (tt.ft(j, a), tt.stops[a], tt.stops[b], right, PLURAL[tt.vehicle]))
    q = fig(tt.svg()) + "%s catches the %s that leaves <b>%s</b> at %s. What time does %s get to <b>%s</b>?" % (
        nm, tt.vehicle, tt.stops[a], tt.ft(j, a), pr, tt.stops[b])
    return mcq(q, right, c, e)


def k_left(tt, j, a, b):
    right = tt.ft(j, a)
    c = [tt.ft(j, a + 1), tt.ft(j - 1, a), tt.ft(j + 1, a), tt.ft(j, b), tt.ft(j - 2, a)]
    e = ("Find %s in the %s row. Go <b>up</b> that column to the %s row: <b>%s</b>."
         % (tt.ft(j, b), tt.stops[b], tt.stops[a], right))
    q = fig(tt.svg()) + "A %s gets to <b>%s</b> at %s. What time did it leave <b>%s</b>?" % (
        tt.vehicle, tt.stops[b], tt.ft(j, b), tt.stops[a])
    return mcq(q, right, c, e)


def k_nth(tt, j, s):
    right = tt.ft(j, s)
    c = [tt.ft(j + 1, s), tt.ft(j - 1, s), tt.ft(j, s + 1), tt.ft(j, s - 1), tt.ft(j, 0)]
    e = ("Each column is one %s, in time order from left to right. Count %d column%s from the left, "
         "then go down to the %s row: <b>%s</b>." % (tt.vehicle, j + 1, "" if j == 0 else "s", tt.stops[s], right))
    q = fig(tt.svg()) + "What time does the <b>%s</b> %s on the timetable leave <b>%s</b>?" % (ORD[j], tt.vehicle, tt.stops[s])
    return mcq(q, right, c, e)


def k_where(tt, j, i):
    right = tt.stops[i]
    near = sorted([k for k in range(len(tt.stops)) if k != i], key=lambda k: abs(k - i))
    c = [tt.stops[k] for k in near]
    e = ("Find the %s that leaves %s at %s. Go down that column until you reach %s. It is in the <b>%s</b> row."
         % (tt.vehicle, tt.stops[0], tt.ft(j, 0), tt.ft(j, i), right))
    q = fig(tt.svg()) + "The %s that leaves %s at %s stops somewhere at <b>%s</b>. Where is it?" % (
        tt.vehicle, tt.stops[0], tt.ft(j, 0), tt.ft(j, i))
    return mcq(q, right, c, e)


def k_12(tt, j, a, b, people):
    nm, pr = next(people)
    t = tt.t(j, b)
    right = f12(t)
    H, m = (t % DAY) // 60, t % 60
    c = []
    if 13 <= H <= 19:
        c.append("%d:%02d pm" % (H - 10, m))         # the 1 dropped: 13:09 -> 3:09 pm
    if H == 0:
        c += ["12:%02d pm" % m, "0:%02d am" % m]       # 00:04 is 12:04 am
    c += [f12(t + 12 * 60), f12(tt.t(j + 1, b)), f12(tt.t(j, b - 1)), f12(tt.t(j - 1, b))]
    if H == 0:
        why = "The hour 00 is just after <b>midnight</b>. In 12-hour time it is 12 am, so it is <b>%s</b>." % right
    elif H >= 13:
        why = "%d is more than 12, so it is pm. %d − 12 = %d, so it is <b>%s</b>." % (H, H, H - 12, right)
    elif H == 12:
        why = "12 is the hour just after midday, so it is pm: <b>%s</b>." % right
    else:
        why = "%02d is before midday, so it is am: <b>%s</b>." % (H, right)
    q = fig(tt.svg()) + "%s catches the %s that leaves <b>%s</b> at %s. What time does %s get to <b>%s</b>, in 12-hour time?" % (
        nm, tt.vehicle, tt.stops[a], f12(tt.t(j, a)), pr, tt.stops[b])
    e = "%s is %s in 24-hour time. Go down that column to %s: %s. %s" % (
        f12(tt.t(j, a)), tt.ft(j, a), tt.stops[b], tt.ft(j, b), why)
    return mcq(q, right, c, e)


def k_skip():
    tt = MEL
    right = "Cheltenham"
    c = ["Caulfield", "Richmond", "Frankston"]
    e = ("A dash (—) means the train does not stop there. In the 07:39 column the dash is in the "
         "<b>Cheltenham</b> row. This train is an express, so it gets to Frankston sooner (08:31).")
    return mcq(fig(tt.svg()) + "The train that leaves Flinders Street at 07:39 is an express. Which station does it <b>not</b> stop at?",
               right, c, e)


def k_express():
    tt = MEL
    a, b = tt.t(1, 0), tt.t(2, 4)
    right = "07:39"
    c = ["07:24", "07:51", "08:31"]
    e = ("Look along the Frankston row: 08:11, 08:23, 08:31, 08:50. The train leaving at 07:39 arrives at 08:31, "
         "before the 07:51 train (08:50). If you are at Flinders Street at 07:30, the 07:24 has gone, so catch the "
         "<b>07:39</b>: it gets there at 08:31.")
    return mcq(fig(tt.svg()) + "Isla gets to Flinders Street at 07:30. Which train should she catch to get to <b>Frankston</b> as early as possible?",
               right, c, e)


def set_read(rnd, people):
    its = []
    its.append(k_arrive(MEL, 1, 0, 3, people))
    its.append(k_nth(MEL, 0, 2))
    its.append(k_left(MEL, 3, 0, 2))
    its.append(k_skip())
    its.append(k_where(MEL, 0, 3))
    its.append(k_arrive(BNE, 2, 0, 4, people))
    its.append(k_nth(BNE, 3, 1))
    its.append(k_left(BNE, 1, 1, 3))
    its.append(k_where(BNE, 2, 2))
    its.append(k_12(BNE, 0, 0, 3, people))
    its.append(k_arrive(SYD, 1, 0, 3, people))
    its.append(k_nth(SYD, 2, 2))
    its.append(k_12(SYD, 1, 0, 4, people))
    its.append(k_left(SYD, 3, 1, 4))
    its.append(k_where(SYD, 3, 1))
    its.append(k_arrive(PER, 2, 1, 4, people))
    its.append(k_nth(PER, 1, 3))
    its.append(k_12(PER, 3, 0, 3, people))
    its.append(k_left(PER, 0, 0, 4))
    its.append(k_express())
    assert len(its) == 20
    return {"title": "Read bus, train and ferry timetables", "items": its}


# ============================================================ set 2: how long is the journey?
BLUE = TT("Blue Mountains line: Saturday", "train",
          ["Central", "Strathfield", "Penrith", "Katoomba", "Mount Victoria"], [0, 14, 53, 121, 143],
          [T(8, 18), T(9, 18), T(10, 18), T(11, 18)])

SHORT = [  # sentence, minutes, possible start hours
    ("A tram leaves Glenelg at <b>%s</b> and gets to the Adelaide city centre at <b>%s</b>.", 33, [8, 9, 13, 16]),
    ("The Manly ferry leaves Circular Quay at <b>%s</b> and gets to Manly at <b>%s</b>.", 30, [10, 11, 14]),
    ("A Canberra light rail tram leaves Gungahlin at <b>%s</b> and gets to the city at <b>%s</b>.", 24, [7, 8, 17]),
    ("A train leaves Perth at <b>%s</b> and gets to Mandurah at <b>%s</b>.", 51, [6, 15, 18]),
]
LONG = [
    ("A train leaves Central at <b>%s</b> and gets to Wollongong at <b>%s</b>.", 87, [9, 10, 13]),
    ("A coach leaves Sydney at <b>%s</b> and gets to Canberra at <b>%s</b>.", 205, [7, 8, 11]),
    ("A train leaves Brisbane at <b>%s</b> and gets to Varsity Lakes on the Gold Coast at <b>%s</b>.", 78, [9, 12, 16]),
    ("A train leaves Southern Cross station in Melbourne at <b>%s</b> and gets to Ballarat at <b>%s</b>.", 84, [10, 14, 17]),
]


def set_durations(rnd, people):
    its = []
    for sent, d, hrs in SHORT:
        while True:
            t1 = T(rnd.choice(hrs), rnd.choice([x for x in range(31, 59) if x % 5]))
            if (t1 + d) // 60 != t1 // 60 and (t1 + d) % 60 > 0:
                break
        its.append(dur_q(sent % (f24(t1), f24(t1 + d)) + " How long is the trip?", t1, t1 + d))
    for sent, d, hrs in LONG:
        while True:
            t1 = T(rnd.choice(hrs), rnd.choice([x for x in range(21, 58) if x % 5]))
            if (t1 + d) % 60 < t1 % 60 and (t1 + d) % 60 > 0:
                break
        its.append(dur_q(sent % (f24(t1), f24(t1 + d)) + " How long is the trip?", t1, t1 + d))
    # from a timetable
    for j, a, b in [(1, 0, 2), (2, 1, 3), (0, 0, 4), (3, 2, 4)]:
        t1, t2 = BLUE.t(j, a), BLUE.t(j, b)
        extra = [sdur(BLUE.t(j, b - 1) - t1) if b - 1 > a else None, sdur(BLUE.t(j, b + 1) - t1) if BLUE.t(j, b + 1) else None]
        q = fig(BLUE.svg()) + "How long does the %s train take from <b>%s</b> to <b>%s</b>?" % (
            BLUE.ft(j, 0), BLUE.stops[a], BLUE.stops[b])
        its.append(dur_q(q, t1, t2, extra=extra,
                         note="In the %s column, it leaves %s at %s and gets to %s at %s. " % (
                             BLUE.ft(j, 0), BLUE.stops[a], f24(t1), BLUE.stops[b], f24(t2))))
    # 12-hour and 24-hour mixed, and a trip with a change
    t1, t2 = T(9, 45), T(13, 20)
    its.append(dur_q("A Year 6 excursion bus leaves school at <b>9:45 am</b> and gets back at <b>13:20</b>. How long is the excursion?",
                     t1, t2, extra=[dur(T(9, 45) - T(3, 20))],
                     note="Change 9:45 am to 09:45. "))
    t1, t2 = T(11, 40), T(14, 5)
    its.append(dur_q("A koala-spotting walk starts at <b>11:40 am</b> and ends at <b>2:05 pm</b>. How long is the walk?",
                     t1, t2, extra=[dur(T(11, 40) - T(2, 5))], fmt=f12,
                     note="It goes past midday, so count on from 11:40 am. "))
    t1, t2 = T(18, 50), T(21, 15)
    its.append(dur_q("Cooper’s family boards a dinner cruise at <b>18:50</b> and gets off at <b>9:15 pm</b>. How long is the cruise?",
                     t1, t2, extra=[dur(T(18, 50) - T(9, 15))], note="9:15 pm is 21:15. "))
    a1, a2, b1, b2 = T(8, 12), T(8, 47), T(9, 5), T(9, 38)
    its.append(mcq("Ruby catches a train at <b>08:12</b> that arrives at <b>08:47</b>. She then catches a bus at <b>09:05</b> "
                   "that arrives at <b>09:38</b>. How long is her whole journey, from the start of the train to the end of the bus?",
                   dur(b2 - a1), [dur((a2 - a1) + (b2 - b1)), dur(b1 - a1), dur(b2 - a2), dur(b2 - a1 + 10)],
                   "The whole journey is from 08:12 to 09:38, and that includes the wait between the train and the bus. "
                   + count_on(a1, b2) + " (Adding only the two rides, 35 + 33 = 68 minutes, leaves out the wait.)",
                   key=dur_value))
    # across midnight
    mid = [
        ("The last train leaves Flinders Street at <b>23:52</b> and gets to Frankston at <b>00:51</b>. How long is the trip?",
         T(23, 52), DAY + T(0, 51)),
        ("The last train of the night leaves Perth at <b>23:45</b> and gets to Fremantle at <b>00:13</b>. How long is the trip?",
         T(23, 45), DAY + T(0, 13)),
        ("On New Year’s Eve, Charlotte’s family leaves home at <b>22:35</b> to watch the midnight fireworks. "
         "They get home at <b>01:10</b>. How long were they out?", T(22, 35), DAY + T(1, 10)),
        ("An overnight coach leaves Sydney at <b>19:15</b> and gets to Byron Bay at <b>08:35</b> the next morning. "
         "How long is the trip?", T(19, 15), DAY + T(8, 35)),
    ]
    for q, t1, t2 in mid:
        to_mid = DAY - t1
        back = t1 - (t2 - DAY)
        extra = [sdur(back), sdur(to_mid), sdur(t2 - t1 + 60)]
        it = dur_q(q, t1, t2, extra=extra)
        it["e"] += " (Count on through midnight. Taking the smaller time from the bigger one gives the wrong answer.)"
        its.append(it)
    assert len(its) == 20
    return {"title": "How long is the journey? Across hours and midnight", "items": its}


# ============================================================ set 3: which service? plan to arrive on time
HOB = TT("Bus: Kingston to Hobart", "bus",
         ["Kingston", "Taroona", "Sandy Bay", "Hobart city"], [0, 9, 17, 26],
         [T(7, 5), T(7, 25), T(7, 40), T(8, 0), T(8, 20)])


def latest(tt, frm, to, by):
    js = [j for j in range(len(tt.cols)) if tt.t(j, to) <= by]
    return max(js)


def set_plan(rnd, people):
    its = []
    tt = HOB
    S = fig(tt.svg())
    # 1 latest bus to be in Hobart city by 08:15
    j = latest(tt, 0, 3, T(8, 15))
    its.append(mcq(S + "Oliver must be in <b>Hobart city</b> by 08:15. What is the latest bus he can catch from <b>Kingston</b>?",
                   tt.ft(j, 0), [tt.ft(j + 1, 0), tt.ft(j, 3), tt.ft(j - 1, 0)],
                   "Look along the Hobart city row for the last time that is not after 08:15: %s. Go up that column to Kingston: "
                   "<b>%s</b>. The next bus gets to Hobart city at %s, which is too late." % (tt.ft(j, 3), tt.ft(j, 0), tt.ft(j + 1, 3))))
    # 2 latest from Taroona to be at Sandy Bay by 07:50
    j = latest(tt, 1, 2, T(7, 50))
    its.append(mcq(S + "Mei must be at <b>Sandy Bay</b> by 07:50. What is the latest bus she can catch from <b>Taroona</b>?",
                   tt.ft(j, 1), [tt.ft(j + 1, 1), tt.ft(j, 2), tt.ft(j - 1, 1)],
                   "In the Sandy Bay row, the last time not after 07:50 is %s. Go up that column to the Taroona row: <b>%s</b>. "
                   "The %s bus from Taroona reaches Sandy Bay at %s, which is too late." % (
                       tt.ft(j, 2), tt.ft(j, 1), tt.ft(j + 1, 1), tt.ft(j + 1, 2))))
    # 3 next bus
    its.append(mcq(S + "Jack gets to the <b>Kingston</b> stop at 07:31. What time is the next bus?",
                   "07:40", ["07:25", "07:34", "08:00"],
                   "The 07:25 bus has already gone. The next time in the Kingston row is <b>07:40</b>. "
                   "(07:34 is in the Taroona row.)"))
    # 4 wait at Taroona
    its.append(mcq(S + "Amelia gets to the <b>Taroona</b> stop at 07:38. How long must she wait for the next bus?",
                   "11 minutes", ["4 minutes", "2 minutes", "31 minutes"],
                   "The 07:34 bus has gone. The next bus from Taroona is at 07:49. 07:38 to 07:49 is <b>11 minutes</b>. "
                   "(07:40 is in the Kingston row, not the Taroona row.)", key=dur_value))
    # 5 walk to the stop
    nm, pr = next(people)
    its.append(mcq(S + "It takes %s 15 minutes to walk to the <b>Kingston</b> stop. %s wants to catch the 07:40 bus. "
                   "What is the latest time %s can leave home?" % (nm, pr.capitalize(), pr),
                   "07:25", ["07:55", "07:10", "07:15"],
                   "Work backwards: count back 15 minutes from 07:40. 07:40 − 15 minutes = <b>07:25</b>. "
                   "(Adding 15 minutes gives 07:55, after the bus has left.)"))
    # 6 school with a walk
    j = latest(tt, 0, 2, T(8, 34))
    its.append(mcq(S + "School in Sandy Bay starts at 08:40. It is a 6-minute walk from the Sandy Bay stop to school. "
                   "What is the latest bus Lachlan can catch from <b>Kingston</b>?",
                   tt.ft(j, 0), [tt.ft(j + 1, 0), tt.ft(j, 2), tt.ft(j - 1, 0)],
                   "He must be at the Sandy Bay stop by 08:40 − 6 minutes = 08:34. In the Sandy Bay row, the last time not after "
                   "08:34 is %s. Go up to Kingston: <b>%s</b>. (The %s bus gets to Sandy Bay at %s, so he would be late after the walk.)"
                   % (tt.ft(j, 2), tt.ft(j, 0), tt.ft(j + 1, 0), tt.ft(j + 1, 2))))
    # 7 12-hour
    j = latest(tt, 2, 3, T(7, 55))
    its.append(mcq(S + "Sienna must be in <b>Hobart city</b> by <b>7:55 am</b>. What is the latest bus she can catch from <b>Sandy Bay</b>?",
                   tt.ft(j, 2), [tt.ft(j + 1, 2), tt.ft(j, 3), tt.ft(j - 1, 2)],
                   "7:55 am is 07:55. In the Hobart city row, the last time not after 07:55 is %s. Go up to Sandy Bay: <b>%s</b>."
                   % (tt.ft(j, 3), tt.ft(j, 2))))
    # 8 earliest arrival
    its.append(mcq(S + "Ethan is at the <b>Taroona</b> stop at 07:52. What is the earliest time he can get to <b>Hobart city</b>?",
                   "08:26", ["08:06", "08:09", "08:46"],
                   "The 07:49 bus from Taroona has gone. The next one is at 08:09. Go down that column to Hobart city: <b>08:26</b>. "
                   "(08:06 belongs to the bus that has already left.)"))
    # 9 wait after arriving
    its.append(mcq(S + "Leo catches the 07:40 bus from Kingston to Hobart city. His swimming lesson starts at 08:30. "
                   "How long does he have between getting off the bus and the start of his lesson?",
                   "24 minutes", ["50 minutes", "33 minutes", "39 minutes"],
                   "Go down the 07:40 column to Hobart city: 08:06. 08:06 to 08:30 is <b>24 minutes</b>. "
                   "(Starting from 07:40 gives 50 minutes, but that includes the bus ride.)", key=dur_value))
    # 10 how many before 8 am
    its.append(mcq(S + "How many buses leave <b>Kingston</b> before 8 am?", "3", ["4", "5", "2"],
                   "8 am is 08:00. In the Kingston row, 07:05, 07:25 and 07:40 are before 08:00, so <b>3</b> buses. "
                   "The 08:00 bus leaves at 8 am, not before it."))
    # text plans
    its.append(mcq("A movie starts at <b>19:10</b>. Kai wants to be there 10 minutes early. The bus trip takes 35 minutes. "
                   "Buses leave at 18:05, 18:25 and 18:45. Which is the latest bus he can catch?",
                   "18:25", ["18:45", "18:35", "18:05"],
                   "Work backwards: he must arrive by 19:10 − 10 minutes = 19:00. Then 19:00 − 35 minutes = 18:25. "
                   "The latest bus at or before 18:25 is <b>18:25</b>. (18:35 is not a bus time.)"))
    its.append(mcq("Chloe’s family wants to watch the footy at the MCG, which starts at <b>19:40</b>. The train takes 25 minutes, "
                   "then they walk for 10 minutes. Trains leave at 18:52, 19:07 and 19:22. Which is the latest train that gets them there in time?",
                   "18:52", ["19:07", "19:22", "18:37"],
                   "Work backwards: 19:40 − 10 minutes = 19:30, then 19:30 − 25 minutes = 19:05. "
                   "The latest train not after 19:05 is <b>18:52</b>. (The 19:07 train only works if you forget the walk.)"))
    its.append(mcq("A netball game starts at <b>9:15 am</b>. Players must arrive 20 minutes early. The drive takes 25 minutes. "
                   "What is the latest time Matilda can leave home, in 24-hour time?",
                   "08:30", ["08:50", "08:55", "20:30"],
                   "Count back 20 minutes from 09:15: 08:55. Then count back 25 minutes: <b>08:30</b>. "
                   "It is in the morning, so it is 08:30, not 20:30."))
    its.append(mcq("Aarav’s train gets to the interchange at <b>08:47</b>. It takes him 5 minutes to walk to the bus stop. "
                   "Buses leave at 08:40, 08:55 and 09:10. Which bus can he catch?",
                   "08:55", ["08:40", "09:10", "08:52"],
                   "He can be at the bus stop at 08:47 + 5 minutes = 08:52. The 08:40 bus has gone, so the first bus he can catch "
                   "is <b>08:55</b>. (08:52 is not a bus time.)"))
    its.append(mcq("Ferries from Circular Quay to Manly leave on the hour and at half past. The trip takes 30 minutes. "
                   "Harper’s family gets to Circular Quay at <b>10:40</b>. What time do they get to Manly?",
                   "11:30", ["11:10", "11:00", "12:00"],
                   "The 10:30 ferry has gone. The next one leaves at 11:00. 11:00 + 30 minutes = <b>11:30</b>. "
                   "(11:10 forgets the wait for the ferry.)"))
    its.append(mcq("Trains leave a station every 12 minutes, starting at <b>06:10</b>. William gets to the station at 07:00. "
                   "What time is the next train?",
                   "07:10", ["07:00", "06:58", "07:12"],
                   "Count on in 12s: 06:10, 06:22, 06:34, 06:46, 06:58, 07:10. The 06:58 train has gone, so the next is "
                   "<b>07:10</b>. (Trains do not have to leave on the hour.)"))
    its.append(mcq("Coaches from Adelaide to Victor Harbor leave at 08:30, 11:30 and 16:00. The trip takes 1 hour 35 minutes. "
                   "Isla wants to be in Victor Harbor by <b>1:30 pm</b>. Which is the latest coach she can catch?",
                   "11:30", ["16:00", "08:30", "13:05"],
                   "1:30 pm is 13:30. 13:30 − 1 hour 35 minutes = 11:55. The latest coach not after 11:55 is <b>11:30</b>; "
                   "it arrives at 13:05. (13:05 is the arrival time, not a coach time.)"))
    its.append(mcq("Buses to the beach leave every 15 minutes from 08:50. The trip takes 48 minutes. Jack wants to be at the "
                   "beach by <b>10:30 am</b>. Which is the latest bus he can catch?",
                   "09:35", ["09:50", "09:42", "09:20"],
                   "Work backwards: 10:30 − 48 minutes = 09:42. The buses are 08:50, 09:05, 09:20, 09:35, 09:50. "
                   "The latest one not after 09:42 is <b>09:35</b> (it arrives at 10:23). The 09:50 bus arrives at 10:38, too late."))
    its.append(mcq("Grace can go to the zoo two ways. <b>Train:</b> leaves 08:05, arrives 08:52, then a 6-minute walk. "
                   "<b>Bus:</b> leaves 08:12, arrives 09:04, then a 2-minute walk. Which way gets her to the zoo first, and by how much?",
                   "Train, 8 minutes earlier", ["Train, 12 minutes earlier", "Train, 7 minutes earlier", "Train, 1 minute earlier"],
                   "Find the time she reaches the zoo each way. Train: 08:52 + 6 minutes = 08:58. Bus: 09:04 + 2 minutes = 09:06. "
                   "08:58 to 09:06 is 8 minutes, so the <b>train</b> is <b>8 minutes earlier</b>. "
                   "(Comparing only the arrival times forgets the walks.)"))
    its.append(mcq("Mia’s flight leaves at <b>14:20</b>. She must be at the airport 1 hour before. The drive to the airport "
                   "takes 50 minutes. What is the latest time she can leave home?",
                   "12:30", ["13:30", "13:20", "16:10"],
                   "Work backwards: 14:20 − 1 hour = 13:20 (at the airport). Then 13:20 − 50 minutes = <b>12:30</b>. "
                   "(13:30 forgets the hour at the airport; 16:10 adds instead of counting back.)"))
    assert len(its) == 20
    return {"title": "Which service? Plan to arrive on time", "items": its}


# ============================================================ set 4: itineraries
CAMP = [(T(8, 15), "Bus leaves school"), (T(11, 40), "Arrive at camp"), (T(12, 15), "Lunch"), (T(13, 0), "Canoeing"),
        (T(14, 45), "Afternoon tea"), (T(15, 10), "Bushwalk"), (T(17, 35), "Free time"), (T(18, 0), "Dinner"),
        (T(19, 15), "Night walk"), (T(20, 45), "Lights out")]
PHIL = [(T(9, 30), "Leave Melbourne"), (T(11, 35), "Koala reserve"), (T(13, 0), "Lunch in Cowes"),
        (T(14, 10), "Beach walk"), (T(16, 15), "Nobbies boardwalk"), (T(17, 30), "Penguin Parade"),
        (T(19, 0), "Drive home"), (T(21, 10), "Arrive home")]


def what_on(rows, t):
    for k in range(len(rows) - 1, -1, -1):
        if rows[k][0] <= t:
            return k


def set_itin(rnd, people):
    its = []
    C = fig(grid_svg("itinerary: Year 6 camp, day 1", "Year 6 camp: Day 1 (each activity ends when the next starts)", CAMP))
    ct = dict((a, t) for t, a in CAMP)
    its.append(dur_q(C + "How long is the bus trip from school to camp?", ct["Bus leaves school"], ct["Arrive at camp"]))
    its.append(dur_q(C + "How long is canoeing?", ct["Canoeing"], ct["Afternoon tea"],
                     extra=[dur(ct["Bushwalk"] - ct["Canoeing"])]))
    its.append(dur_q(C + "How long is free time?", ct["Free time"], ct["Dinner"], extra=["35 minutes", "65 minutes"]))
    k = what_on(CAMP, T(16, 20))
    its.append(mcq(C + "What are the students doing at <b>4:20 pm</b>?", CAMP[k][1],
                   [CAMP[what_on(CAMP, T(14, 20))][1], CAMP[k + 1][1], CAMP[k - 1][1]],
                   "4:20 pm is 16:20 (4 + 12 = 16). The bushwalk starts at 15:10 and free time starts at 17:35, so at 16:20 they are on "
                   "the <b>%s</b>. (Reading 4:20 pm as 14:20 gives canoeing.)" % CAMP[k][1].lower()))
    k = what_on(CAMP, T(19, 50))
    its.append(mcq(C + "What are the students doing at <b>7:50 pm</b>?", CAMP[k][1],
                   [CAMP[what_on(CAMP, T(17, 50))][1], CAMP[k - 1][1], CAMP[k + 1][1]],
                   "7:50 pm is 19:50 (7 + 12 = 19). The night walk starts at 19:15 and lights out is at 20:45, so it is the "
                   "<b>night walk</b>. (Reading 7:50 pm as 17:50 gives free time.)"))
    its.append(mcq(C + "How long is it from arriving at camp to the start of canoeing?", "1 hour 20 minutes",
                   ["1 hour 60 minutes", "35 minutes", "2 hours 20 minutes"],
                   count_on(ct["Arrive at camp"], ct["Canoeing"]) + " (Doing 1300 − 1140 = 160 and calling it 1 hour 60 minutes "
                   "uses 100 minutes in an hour.)", key=dur_value))
    its.append(dur_q(C + "How long is it from the start of dinner to lights out?", ct["Dinner"], ct["Lights out"],
                     extra=[dur(ct["Night walk"] - ct["Dinner"])]))
    its.append(dur_q(C + "How long is the bushwalk?", ct["Bushwalk"], ct["Free time"],
                     extra=[dur(ct["Bushwalk"] - ct["Afternoon tea"])]))
    wake = DAY + T(6, 45)
    its.append(mcq(C + "On day 2 the students wake up at <b>06:45</b>. How long is it from lights out to waking up?",
                   dur(wake - ct["Lights out"]), [dur(ct["Lights out"] - T(6, 45)), dur(DAY - ct["Lights out"]), dur(wake - ct["Lights out"] + 60)],
                   count_on(ct["Lights out"], wake) + " (20:45 − 06:45 = 14 hours is the wrong way round, and stopping at "
                   "midnight gives only 3 hours 15 minutes.)", key=dur_value))
    late = ct["Afternoon tea"] + 20 + 25
    its.append(mcq(C + "Canoeing runs <b>20 minutes</b> late, so afternoon tea starts 20 minutes late. Afternoon tea still lasts "
                   "25 minutes. What time does the bushwalk start now?", f24(late),
                   [f24(ct["Bushwalk"]), f24(ct["Afternoon tea"] + 20), f24(late + 20)],
                   "Afternoon tea starts at 14:45 + 20 minutes = 15:05. It lasts 25 minutes (14:45 to 15:10), "
                   "so 15:05 + 25 minutes = <b>%s</b>." % f24(late)))
    # Phillip Island day trip
    P = fig(grid_svg("itinerary: Phillip Island day trip", "Phillip Island day trip (July)", PHIL))
    pt = dict((a, t) for t, a in PHIL)
    its.append(dur_q(P + "How long is the drive from Melbourne to the koala reserve?", pt["Leave Melbourne"], pt["Koala reserve"]))
    its.append(dur_q(P + "How long does the family spend at the koala reserve?", pt["Koala reserve"], pt["Lunch in Cowes"]))
    its.append(dur_q(P + "How long is the family away from home, from leaving Melbourne to arriving home?",
                     pt["Leave Melbourne"], pt["Arrive home"]))
    its.append(dur_q(P + "How long is the drive home?", pt["Drive home"], pt["Arrive home"],
                     extra=[dur(pt["Arrive home"] - pt["Penguin Parade"])]))
    k = what_on(PHIL, T(15, 0))
    its.append(mcq(P + "What is the family doing at <b>3 pm</b>?", PHIL[k][1],
                   [PHIL[what_on(PHIL, T(13, 0))][1], PHIL[k + 1][1], PHIL[k - 2][1]],
                   "3 pm is 15:00. The beach walk starts at 14:10 and the Nobbies boardwalk starts at 16:15, so they are on the "
                   "<b>beach walk</b>. (Reading 3 pm as 13:00 gives lunch.)"))
    its.append(mcq(P + "What time does the Penguin Parade start, in 12-hour time?", "5:30 pm",
                   ["7:30 pm", "5:30 am", "3:30 pm"],
                   "17 is more than 12, so it is pm. 17 − 12 = 5, so 17:30 is <b>5:30 pm</b>. (Dropping the 1 gives 7:30 pm.)"))
    late = pt["Arrive home"] + 25
    its.append(mcq(P + "The family leaves Melbourne <b>25 minutes</b> late, and every part of the day moves 25 minutes later. "
                   "What time do they get home?", f24(late), [f24(pt["Arrive home"] - 25), f24(pt["Arrive home"]), f24(late + 60)],
                   "Add 25 minutes to 21:10: 21:10 + 25 minutes = <b>%s</b>." % f24(late)))
    # time zones (July: no daylight saving in New South Wales or Western Australia)
    its.append(mcq("In July, Perth time is <b>2 hours behind</b> Sydney time. Grandma calls from Perth at <b>18:30</b> Perth time. "
                   "What time is it in Sydney?", "20:30", ["16:30", "18:30", "19:30"],
                   "Sydney is 2 hours <b>ahead</b> of Perth, so add 2 hours: 18:30 + 2 hours = <b>20:30</b>. "
                   "(Taking away 2 hours gives the wrong direction.)"))
    its.append(mcq("In July, Perth is 2 hours behind Sydney. A flight leaves Sydney at <b>08:00</b> Sydney time and takes "
                   "<b>5 hours 20 minutes</b>. What time does it land, in Perth time?", "11:20", ["13:20", "15:20", "10:20"],
                   "08:00 + 5 hours 20 minutes = 13:20 Sydney time. Perth is 2 hours behind, so 13:20 − 2 hours = <b>11:20</b> Perth time. "
                   "(13:20 forgets the time difference.)"))
    its.append(mcq("In July, Sydney is 2 hours ahead of Perth. A flight leaves Perth at <b>13:35</b> Perth time and takes "
                   "<b>4 hours 15 minutes</b>. What time does it land, in Sydney time?", "19:50", ["17:50", "15:50", "18:50"],
                   "13:35 + 4 hours 15 minutes = 17:50 Perth time. Sydney is 2 hours ahead, so 17:50 + 2 hours = <b>19:50</b> Sydney time. "
                   "(17:50 forgets the time difference.)"))
    assert len(its) == 20, len(its)
    return {"title": "Itineraries: a school camp and a day trip", "items": its}


# ============================================================ set 5: problems
def set_problems(rnd, people):
    its = []

    def tq(q, right_t, wrong_ts, e):
        return mcq(q, f24(right_t), [f24(x) for x in wrong_ts], e)

    nm, pr = next(people)
    t = T(16, 42) + 28 + 7
    its.append(tq("%s catches the <b>16:42</b> tram home. The tram ride takes 28 minutes, then %s walks for 7 minutes. "
                  "What time does %s get home?" % (nm, pr, pr), t, [t - 7, t + 60, t - 10],
                  "16:42 + 28 minutes = 17:10 (18 minutes to 17:00, then 10 more). Then 17:10 + 7 minutes = <b>17:17</b>."))
    t = T(9, 5) + 50 + 135 + 30 + 50
    its.append(tq("A Year 6 excursion bus leaves school at <b>09:05</b>. The trip to the museum takes 50 minutes. The class spends "
                  "2 hours 15 minutes in the museum and 30 minutes having lunch, then takes the 50-minute trip back. "
                  "What time do they get back to school?", t, [t - 50, t - 30, t + 60],
                  "09:05 + 50 minutes = 09:55. 09:55 + 2 hours 15 minutes = 12:10. 12:10 + 30 minutes = 12:40. "
                  "12:40 + 50 minutes = <b>13:30</b>. Remember the trip back."))
    t = T(9, 30) + 14 * 6
    its.append(tq("At the swimming carnival, 14 races are swum one after another, starting at <b>09:30</b>. Each race takes "
                  "6 minutes. What time do the races finish?", t, [T(10, 14), t - 6, t + 60],
                  "14 × 6 = 84 minutes = 1 hour 24 minutes. 09:30 + 1 hour 24 minutes = <b>10:54</b>. "
                  "(84 minutes is not 0 hours 84 minutes, so 10:14 is wrong.)"))
    t = T(8, 40) + 40 + 11
    its.append(tq("A netball game has 4 quarters of 10 minutes. There are breaks of 3 minutes, 5 minutes and 3 minutes between "
                  "the quarters. The game starts at <b>08:40</b>. What time does it finish?", t, [T(9, 20), t - 3, t + 3],
                  "Playing time: 4 × 10 = 40 minutes. Breaks: 3 + 5 + 3 = 11 minutes. 40 + 11 = 51 minutes. "
                  "08:40 + 51 minutes = <b>09:31</b>. (There are only 3 breaks between 4 quarters.)"))
    its.append(mcq("A day of cricket runs from <b>10:00</b> to <b>17:00</b>, with a 40-minute lunch break and a 20-minute tea break. "
                   "How much time is spent playing?", "6 hours", ["7 hours", "6 hours 40 minutes", "6 hours 20 minutes"],
                   "10:00 to 17:00 is 7 hours. The breaks are 40 + 20 = 60 minutes = 1 hour. 7 hours − 1 hour = <b>6 hours</b>.",
                   key=dur_value))
    its.append(mcq("It is <b>21:40</b> on 31 December. How long is it until the midnight fireworks?", "2 hours 20 minutes",
                   ["2 hours 60 minutes", "3 hours 20 minutes", "2 hours 40 minutes"],
                   count_on(T(21, 40), DAY) + " (Midnight is 24:00 at the end of the day. Doing 2400 − 2140 = 260 uses 100 "
                   "minutes in an hour.)", key=dur_value))
    its.append(mcq("A nurse starts a night shift at <b>21:30</b> and works for <b>10 hours</b>. What time does the shift end?",
                   "07:30", ["31:30", "19:30", "08:30"],
                   "21:30 + 2 hours 30 minutes = 24:00, which is midnight (00:00). 10 hours − 2 hours 30 minutes = 7 hours 30 minutes. "
                   "00:00 + 7 hours 30 minutes = <b>07:30</b> the next morning. (A 24-hour time never goes past 23:59.)"))
    t = T(9, 48) + 75 + 20
    its.append(tq("Cooper’s family catches a <b>09:48</b> train from Brisbane to the Gold Coast. The train takes 1 hour 15 minutes, "
                  "then a bus to the theme park takes 20 minutes. What time do they get to the theme park?",
                  t, [t - 20, t - 60, t + 60],
                  "09:48 + 1 hour = 10:48. 10:48 + 15 minutes = 11:03. 11:03 + 20 minutes = <b>11:23</b>."))
    its.append(mcq("A movie starts at <b>7:15 pm</b>. Ruby’s family wants 1 hour for dinner before it, and it takes 25 minutes to "
                   "drive to the restaurant. What is the latest time they can leave home, in 24-hour time?",
                   "17:50", ["05:50", "18:50", "18:15"],
                   "7:15 pm is 19:15. Count back 1 hour: 18:15. Count back 25 minutes: 15 minutes to 18:00, then 10 more: <b>17:50</b>. "
                   "It is the evening, so it is 17:50, not 05:50."))
    its.append(mcq("Zara’s family gets to a wildlife park at <b>13:55</b>. The platypus tour starts at <b>14:20</b>. "
                   "How long do they wait?", "25 minutes", ["65 minutes", "35 minutes", "1 hour 25 minutes"],
                   count_on(T(13, 55), T(14, 20)) + " (1420 − 1355 = 65 uses 100 minutes in an hour.)", key=dur_value))
    its.append(dur_q("A school fun run starts at <b>7:45 am</b>. Noah finishes at <b>9:12 am</b>. How long does he take?",
                     T(7, 45), T(9, 12), fmt=f12))
    t = T(7, 52) + 8 + 6 + 22
    its.append(tq("Liam leaves home at <b>07:52</b>. He walks to the bus stop in 8 minutes, waits 6 minutes, then rides the bus "
                  "for 22 minutes. What time does he get to school?", t, [t - 6, t - 8, t + 10],
                  "8 + 6 + 22 = 36 minutes. 07:52 + 36 minutes: 8 minutes to 08:00, then 28 more = <b>08:28</b>. "
                  "(Remember the waiting time.)"))
    its.append(mcq("An overnight ferry across Bass Strait leaves at <b>19:30</b> and arrives at <b>06:30</b> the next morning. "
                   "How long is the trip?", "11 hours", ["13 hours", "4 hours 30 minutes", "12 hours"],
                   count_on(T(19, 30), DAY + T(6, 30)) + " (19:30 − 06:30 = 13 hours is the wrong way round.)", key=dur_value))
    t = T(9, 20) + 75 + 30 + 45
    its.append(tq("A Year 6 class plans a city day. They start at <b>09:20</b>, spend 1 hour 15 minutes at the museum, walk for "
                  "30 minutes to the art gallery, then spend 45 minutes there. What time do they finish at the gallery?",
                  t, [t - 30, t + 60, t - 20],
                  "1 hour 15 minutes + 30 minutes + 45 minutes = 2 hours 30 minutes. 09:20 + 2 hours 30 minutes = <b>11:50</b>."))
    its.append(mcq("Trains leave a station at 10, 30 and 50 minutes past every hour. Charlotte gets to the station at <b>08:07</b>. "
                   "How long must she wait?", "3 minutes", ["13 minutes", "7 minutes", "23 minutes"],
                   "The trains around then leave at 07:50, 08:10 and 08:30. At 08:07 the next train is at 08:10, so she waits "
                   "<b>3 minutes</b>.", key=dur_value))
    its.append(mcq("A movie starts at <b>19:35</b> and is 1 hour 50 minutes long. Isla’s bedtime is <b>9:15 pm</b>. When does "
                   "the movie end?", "10 minutes after her bedtime",
                   ["10 minutes before her bedtime", "1 hour 10 minutes after her bedtime", "At her bedtime"],
                   "19:35 + 1 hour 50 minutes = 21:25. 9:15 pm is 21:15. 21:15 to 21:25 is 10 minutes, so it ends "
                   "<b>10 minutes after her bedtime</b>."))
    t = T(8, 50) + 195 + 25
    its.append(tq("A family drives from Sydney to Canberra. The driving takes 3 hours 15 minutes and they stop for 25 minutes "
                  "on the way. They leave at <b>08:50</b>. What time do they get to Canberra?", t, [t - 25, t - 60, t + 60],
                  "3 hours 15 minutes + 25 minutes = 3 hours 40 minutes. 08:50 + 3 hours = 11:50. 11:50 + 40 minutes = <b>12:30</b>."))
    its.append(mcq("Sienna has swimming training from <b>06:15</b> to <b>07:30</b> on 4 mornings a week. How much training time "
                   "is that each week?", "5 hours", ["4 hours 15 minutes", "5 hours 15 minutes", "4 hours"],
                   "06:15 to 07:30 is 1 hour 15 minutes. 4 × 1 hour = 4 hours and 4 × 15 minutes = 60 minutes = 1 hour. "
                   "4 hours + 1 hour = <b>5 hours</b>.", key=dur_value))
    arr = T(7, 45) + 230 + 20
    its.append(mcq("The camp bus leaves at <b>07:45</b>. The driving takes 3 hours 50 minutes, plus a 20-minute stop. "
                   "Lunch at camp is at <b>12:30</b>. How long is it from arriving at camp to lunch?",
                   dur(T(12, 30) - arr), [dur(T(12, 30) - arr + 20), dur(T(12, 30) - arr - 20), dur(T(12, 30) - arr + 60)],
                   "3 hours 50 minutes + 20 minutes = 4 hours 10 minutes. 07:45 + 4 hours 10 minutes = 11:55. "
                   + count_on(arr, T(12, 30)), key=dur_value))
    its.append(mcq("In July, Perth is 2 hours behind Sydney. A flight leaves Sydney at <b>17:30</b> Sydney time and lands in Perth "
                   "at <b>20:50</b> Perth time. How long is the flight?", "5 hours 20 minutes",
                   ["3 hours 20 minutes", "1 hour 20 minutes", "4 hours 20 minutes"],
                   "Change the landing time to Sydney time: 20:50 + 2 hours = 22:50. "
                   + count_on(T(17, 30), T(22, 50)) + " (3 hours 20 minutes forgets the time difference.)", key=dur_value))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: plan the day", "items": its}


# ============================================================ lesson
def body_html():
    tt = MEL
    return (
        "<h2>Reading a timetable</h2>"
        "<p>A timetable lists the stops down the side. Each <b>column</b> is one bus, train or ferry. "
        "To read it, find the <b>row</b> for the stop and the <b>column</b> for the service. The time is where they meet. "
        "A dash (—) means the service does not stop there. Most timetables use <b>24-hour time</b>.</p>"
        "<figure class='sn-fig'>" + tt.svg(hl=1) +
        "<figcaption>The highlighted column is one train. It leaves Flinders Street at 07:24 and gets to Frankston at 08:23.</figcaption></figure>"
        + ex("Read across and down", "A train leaves Richmond at 07:55. What time does it get to Cheltenham?",
             "Find 07:55 in the Richmond row. Go down that column (not across) to the Cheltenham row.", "08:21") +
        "<h2>How long is the journey? Count on in jumps</h2>"
        "<p>An hour has 60 minutes, not 100, so do not just subtract the numbers. "
        "Jump to the next o’clock, then on in whole hours, then to the end time. If the journey goes past midnight, "
        "count on through 00:00.</p>"
        "<figure class='sn-fig'>" + timeline_svg(T(22, 35), DAY + T(1, 10)) +
        "<figcaption>22:35 to 23:00 is 25 minutes, 23:00 to 01:00 is 2 hours, 01:00 to 01:10 is 10 minutes. "
        "Altogether <b>2 hours 35 minutes</b>.</figcaption></figure>"
        + ex("Journey time", "A train leaves Central at 09:18 and gets to Penrith at 10:11. How long is the trip?",
             "09:18 to 10:00 is 42 minutes. 10:00 to 10:11 is 11 minutes. 42 + 11 = 53.", "53 minutes") +
        "<h2>Plan to arrive on time: work backwards</h2>"
        "<p>Start from the time you must be there. Count back any walking or waiting, then choose the <b>latest</b> service "
        "that arrives at or before that time.</p>"
        + ex("Which train?", "The footy starts at 19:40. The train takes 25 minutes and the walk takes 10 minutes. "
             "Trains leave at 18:52, 19:07 and 19:22. Which is the latest train?",
             "19:40 − 10 minutes = 19:30. 19:30 − 25 minutes = 19:05. The latest train not after 19:05 is 18:52.", "18:52") +
        "<h2>Itineraries</h2>"
        "<p>An itinerary is a plan for a day or a trip. Each activity usually ends when the next one starts, so subtract "
        "start times to find how long each part lasts. When a trip crosses time zones, use the local time. In winter, "
        "Perth is 2 hours behind Sydney.</p>"
        + ex("Camp itinerary", "Canoeing starts at 13:00 and afternoon tea starts at 14:45. How long is canoeing?",
             "13:00 to 14:00 is 1 hour. 14:00 to 14:45 is 45 minutes.", "1 hour 45 minutes") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Reading the time next to the right one (the wrong row or the wrong column)", "Put a finger on the row and another on the column, and read where they meet"],
            ["09:18 to 10:11 worked out as 1011 − 918 = 93 minutes", "An hour has 60 minutes. Count on: 42 + 11 = 53 minutes"],
            ["4:20 pm read as 14:20", "Add 12 to a pm hour: 4 + 12 = 16, so 16:20"],
            ["Catching the train that arrives just after the start time", "Choose the latest service that arrives <b>at or before</b> the time you need"],
            ["Adding the walking time when you should count back", "Work backwards from the time you must be there"],
            ["22:35 to 01:10 worked out as 22:35 − 01:10", "Count on through midnight: 25 minutes + 2 hours + 10 minutes"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about timetables and itineraries?",
     "a": "In the Australian Curriculum v9.0 (AC9M6M03), Year 6 students Interpret and use timetables and itineraries to plan activities and work out how long events and journeys take, using 24-hour time."},
    {"q": "How do you read a bus or train timetable?",
     "a": "Find the row for your stop and the column for your service; the time is where they meet. To plan a trip, look along the row where you want to arrive and choose the latest service that gets there in time."},
    {"q": "How do you work out how long a journey takes when it goes past midnight?",
     "a": "Count on in jumps: from the start time to midnight (00:00), then on to the end time. For example, 22:35 to 01:10 is 25 minutes + 2 hours + 10 minutes = 2 hours 35 minutes."},
    {"q": "How many hours is Perth behind Sydney?",
     "a": "Perth is 2 hours behind Sydney from April to early October. When New South Wales uses daylight saving (early October to early April) the difference is 3 hours, because Western Australia does not use daylight saving."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5)."""
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
    rnd = random.Random(6814)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_read(rnd, people), set_durations(rnd, people), set_plan(rnd, people), set_itin(rnd, people),
            set_problems(rnd, people)]
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
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "timetables-and-itineraries", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Timetables and Itineraries",
        "seo_title": "Year 6 Timetables and Itineraries Worksheets: Reading Timetables, Journey Times and Planning (Free, with Answer Key)",
        "short_title": "Timetables and itineraries",
        "domain": "Measurement",
        "standard_code": "AC9M6M03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Interpret and use timetables and itineraries to plan activities and determine the duration of events and journeys",
        "meta_desc": "Free Year 6 maths worksheets on timetables and itineraries for the Australian Curriculum (AC9M6M03): read bus, train and ferry timetables in 24-hour time, work out journey times across hours and midnight, choose the right service to arrive on time and plan a school camp or day trip. 100 questions with an answer key.",
        "key_big": "Find the row for the stop and the column for the service. The time is where they meet.",
        "key_sub": "To find how long a journey takes, count on to the next o’clock in jumps: an hour has 60 minutes, not 100. To arrive on time, work backwards from the time you must be there and pick the latest service that gets you there.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "(timetable|time line|itinerary)")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
