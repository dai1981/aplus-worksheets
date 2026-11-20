# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Time: Time Intervals, Timetables and Units from Seconds to Centuries (Grade 6: 4.4 Time)
  python3 tools/gen_za_maths_g6_time.py
Units of time from seconds to centuries (maker from the Grade 5 generator and UK Year 6 maker), time intervals in
24-hour time, and Gautrain, MyCiTi, Metrorail and bus timetables (own makers).
Wrong answers come from real mistakes: using 100 minutes in an hour, reading the wrong row or column of a timetable,
and counting the hours wrongly across the hour.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_converting_units as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(806290)
import gen_za_maths_g5_time as zt5
adopt(zt5)
if isinstance(getattr(zt5, 'R', None), random.Random): zt5.R = random.Random(806291)
za_common.GRADE = "grade-6"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)


LINES = [("Gautrain", ["Park", "Rosebank", "Sandton", "Marlboro", "Midrand", "Centurion", "Pretoria", "Hatfield"]),
         ("MyCiTi bus", ["Civic Centre", "Thibault Square", "Woodbridge Island", "Table View", "Sunset Beach", "Big Bay", "Melkbosstrand"]),
         ("Metrorail train", ["Cape Town", "Salt River", "Observatory", "Rondebosch", "Claremont", "Wynberg", "Muizenberg", "Fish Hoek", "Simon's Town"]),
         ("Durban bus", ["Durban Station", "Berea", "Umgeni Road", "Durban North", "Umhlanga", "La Lucia", "Ballito"])]


def hm(m):
    return "%02d:%02d" % (m // 60 % 24, m % 60)


def dur(m):
    h, mm = divmod(m, 60)
    if h and mm:
        return "%d %s %d %s" % (h, "hour" if h == 1 else "hours", mm, "minute" if mm == 1 else "minutes")
    if h:
        return "%d %s" % (h, "hour" if h == 1 else "hours")
    return "%d %s" % (mm, "minute" if mm == 1 else "minutes")


def make_tt(r):
    name, stops = r.choice(LINES)
    k = r.randint(4, 5)
    i0 = r.randint(0, len(stops) - k)
    st = stops[i0:i0 + k]
    gaps = [r.choice([4, 6, 7, 8, 9, 11, 12, 13, 15]) for _ in range(k - 1)]
    first = r.randint(5 * 60 + 30, 16 * 60)
    first -= first % 5
    every = r.choice([20, 25, 30, 35, 40, 45])
    trips = [first + j * every for j in range(3)]
    rows = []
    for si, s0 in enumerate(st):
        rows.append([s0] + [hm(t + sum(gaps[:si])) for t in trips])
    html = "<table class='sn-table'><tr><th>%s</th><th>Trip 1</th><th>Trip 2</th><th>Trip 3</th></tr>" % name
    for row in rows:
        html += "<tr><td>%s</td>%s</tr>" % (row[0], "".join("<td>%s</td>" % x for x in row[1:]))
    html += "</table>"
    return name, st, gaps, trips, html


def one_tt(r):
    name, st, gaps, trips, html = make_tt(r)
    k = r.choice(["arrive", "long", "catch", "wait"])
    j = r.randrange(3)
    a, b = sorted(r.sample(range(len(st)), 2))
    ta = trips[j] + sum(gaps[:a])
    tb = trips[j] + sum(gaps[:b])
    if k == "arrive":
        q = "Trip %d leaves %s at %s. When does it reach %s?" % (j + 1, st[a], hm(ta), st[b])
        return mcq(html + q, hm(tb), [hm(tb + 5), hm(ta + sum(gaps[a:b]) - gaps[a]) if b - a > 1 else hm(tb - 2), hm(trips[(j + 1) % 3] + sum(gaps[:b]))], "Read the %s row in the Trip %d column: <b>%s</b>." % (st[b], j + 1, hm(tb)))
    if k == "long":
        d = tb - ta
        return mcq(html + "How long does the trip from %s to %s take?" % (st[a], st[b]), dur(d), [dur(d + 10), dur(d - gaps[a]) if d - gaps[a] > 0 else dur(d + 5), dur(tb % 60 + 60 - ta % 60) if tb % 60 + 60 - ta % 60 != d else dur(d + 20)],
                   "%s to %s is %s. <b>%s</b>." % (hm(ta), hm(tb), dur(d), dur(d)))
    if k == "catch":
        need = trips[j] + sum(gaps[:b]) + r.randint(1, 4)
        if j == 2:
            raise AssertionError
        good = [jj for jj in range(3) if trips[jj] + sum(gaps[:b]) <= need]
        best = max(good)
        return mcq(html + "%s must be at %s by %s. Which is the latest trip %s can catch from %s?" % ("Zanele", st[b], hm(need), "she", st[0]),
                   "Trip %d" % (best + 1), ["Trip %d" % x for x in range(1, 4) if x != best + 1] + ["none of them"],
                   "Trip %d reaches %s at %s, before %s. <b>Trip %d</b>." % (best + 1, st[b], hm(trips[best] + sum(gaps[:b])), hm(need), best + 1))
    arr = trips[j] + sum(gaps[:a]) + r.randint(2, 15)
    if j == 2:
        raise AssertionError
    nxt = trips[j + 1] + sum(gaps[:a])
    w = nxt - arr
    return mcq(html + "Thabo gets to %s at %s, just after Trip %d has left. How long must he wait for the next trip?" % (st[a], hm(arr), j + 1), dur(w), [dur(w + 10), dur(nxt % 60) if nxt % 60 and nxt % 60 != w else dur(w + 5), dur(arr - trips[j] - sum(gaps[:a]))],
               "The next trip leaves %s at %s. %s to %s is <b>%s</b>." % (st[a], hm(nxt), hm(arr), hm(nxt), dur(w)))


DAY = [("Netball practice", 15 * 60, 16 * 60 + 30), ("The school concert", 18 * 60, 21 * 60), ("A soccer match", 14 * 60, 16 * 60), ("A bus trip from Johannesburg to Durban", 7 * 60, 15 * 60),
       ("A drive from Cape Town to Hermanus", 8 * 60, 11 * 60), ("Choir practice", 13 * 60, 15 * 60), ("A movie", 19 * 60, 22 * 60), ("A cricket match", 10 * 60, 17 * 60)]


def one_dur6(r):
    what, lo, hi = r.choice(DAY)
    s0 = r.randint(lo, lo + 50)
    s0 -= s0 % 5
    d = r.randint(35, hi - lo)
    d -= d % 5
    e0 = s0 + d
    if r.random() < 0.5:
        return mcq("%s starts at %s and ends at %s. How long is it?" % (what, hm(s0), hm(e0)), dur(d), [dur(d + 40) if (e0 % 60) < (s0 % 60) else dur(d + 60), dur(d - 5), dur(abs(e0 % 60 - s0 % 60) + 60 * (e0 // 60 - s0 // 60))] if (e0 % 60) < (s0 % 60) else [dur(d + 60), dur(d + 5), dur(d + 100) if d + 100 < 1000 else dur(d + 15)],
                   "Count on from %s to %s: <b>%s</b>." % (hm(s0), hm(e0), dur(d)))
    return mcq("%s starts at %s and lasts %s. When does it end?" % (what, hm(s0), dur(d)), hm(e0), [hm(e0 + 60), hm(e0 - 10), hm(s0 + d // 60 * 100 + d % 60) if hm(s0 + d // 60 * 100 + d % 60) != hm(e0) else hm(e0 + 5)],
               "%s + %s = <b>%s</b>." % (hm(s0), dur(d), hm(e0)))


def build():
    sets, R = build_sets([
        ("Units of time", [("collect", zt5.uniq(zt5.one_long), 10), ("run", ukc.set_time, ("rnd",), 10, dec3)]),
        ("Time intervals", [("collect", uniq(one_dur6), 20)]),
        ("Read the timetable", [("collect", uniq(one_tt), 20)]),
        ("Plan a trip", [("collect", uniq(one_tt), 20)]),
        ("Time problems", [("collect", uniq(one_dur6), 10), ("collect", uniq(one_tt), 10)]),
    ], 80629)
    finish(sets, R)
    body = lesson('<ul><li>60 seconds = 1 minute, 60 minutes = 1 hour, 24 hours = 1 day; 10 years = 1 decade, 100 years = 1 century.</li><li>24-hour time: 3:45 p.m. = 15:45.</li><li>To find a time interval, count on to the next hour, then the whole hours, then the minutes.</li><li>In a timetable, find the row for the place and the column for the trip.</li></ul>',
        [example("Bus leaves 08:35, arrives 11:10", ["08:35 → 09:00 is 25 min", "09:00 → 11:00 is 2 h", "+ 10 min"], "2 hours 35 minutes")],
        [['100 minutes', '1 hour = 60 minutes.'], ['The wrong row', 'Use a ruler to follow the row.'], ['Across noon', 'Count on through 12:00.']])
    faq = [('What does CAPS Grade 6 say about time?', 'Read, tell and write time in 12-hour and 24-hour formats, use calendars and timetables, calculate time intervals, and convert between units of time from seconds to centuries.'), ('What is 19:20 in 12-hour time?', '7:20 p.m.'), ('How many minutes are in 2,5 hours?', '150 minutes.'), ('What is an itinerary?', 'A plan of a trip with times and places.')]
    make('time', 29, 'Measurement', 'Grade 6: 4.4 Time',
         'Read, tell and write time in 12-hour and 24-hour formats on both analogue and digital instruments in hours, minutes and seconds; use clocks, calendars, stopwatches and timetables; calculate and solve problems involving time intervals; convert between seconds, minutes, hours, days, weeks, months, years, decades and centuries.',
         'Time: Time Intervals, Timetables and Units from Seconds to Centuries', 'Time',
         'Free CAPS Grade 6 time worksheets: units of time, time intervals, timetables, itineraries and time problems. 100 questions with memos.',
         'Count on to the next hour first.', '1 hour = 60 minutes, not 100.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
