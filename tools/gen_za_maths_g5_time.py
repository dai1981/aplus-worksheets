# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Time: Seconds to Centuries, 24-Hour Time and Time Intervals (Grade 5: 4.4 Time)
  python3 tools/gen_za_maths_g5_time.py
Units of time from seconds to centuries (own maker and BC Grade 5 maker), 12-hour and 24-hour time, elapsed time,
start and end times and problems (BC Grade 5 and Australia Year 5 makers with South African names).
Wrong answers come from real mistakes: using 100 seconds in a minute, adding 10 instead of 12 for p.m. times, and
counting the hours wrongly across noon.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g5_time as cbt
adopt(cbt)
if isinstance(getattr(cbt, 'R', None), random.Random): cbt.R = random.Random(805250)
import gen_au_maths_y5_time as aut
adopt(aut)
if isinstance(getattr(aut, 'R', None), random.Random): aut.R = random.Random(805251)
za_common.GRADE = "grade-5"

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


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)


LONG = [("decade", 10), ("century", 100), ("millennium", 1000)]
PL = {"decade": "decades", "century": "centuries", "millennium": "millennia", "year": "years"}


def one_long(r):
    k = r.choice(["to_years", "from_years", "between", "sec"])
    if k == "to_years":
        u, v = r.choice(LONG[:2])
        n = r.randint(2, 9)
        return mcq("How many years are in <b>%d %s</b>?" % (n, PL[u]), "%s years" % comma(n * v), ["%s years" % comma(x) for x in (n * v * 10, n * v // 10 if v > 10 else n + 10, n * 12)],
                   "1 %s = %d years, so %d %s = <b>%s years</b>." % (u, v, n, PL[u], comma(n * v)))
    if k == "from_years":
        u, v = r.choice(LONG)
        n = r.randint(2, 9) if v < 1000 else r.randint(2, 5)
        y = n * v
        return mcq("<b>%s years</b> is how many %s?" % (comma(y), PL[u]), "%d %s" % (n, PL[u]), ["%s %s" % (comma(x), PL[u]) for x in (n * 10, y // 2, n + 1)],
                   "1 %s = %s years. %s ÷ %s = <b>%d %s</b>." % (u, comma(v), comma(y), comma(v), n, PL[u]))
    if k == "between":
        c, dd, y = r.randint(1, 4), r.randint(1, 9), r.randint(1, 9)
        what = r.choice(["An old church is", "A baobab tree is", "A stone bridge is", "A farmhouse is"])
        t = c * 100 + dd * 10 + y
        return mcq("%s %d %s, %d %s and %d %s old. How many years old is it?" % (what, c, "century" if c == 1 else "centuries", dd, "decade" if dd == 1 else "decades", y, "year" if y == 1 else "years"),
                   "%d years" % t, ["%d years" % x for x in (c + dd + y, c * 100 + dd + y, c * 10 + dd * 10 + y if c * 10 + dd * 10 + y != t else t + 10)],
                   "%d × 100 + %d × 10 + %d = %d + %d + %d = <b>%d years</b>." % (c, dd, y, c * 100, dd * 10, y, t))
    m = r.randint(2, 9)
    s = r.choice([0, 10, 15, 20, 30, 45])
    t = m * 60 + s
    if r.random() < 0.5:
        return mcq("How many seconds are in <b>%d minutes%s</b>?" % (m, (" %d seconds" % s) if s else ""), "%s seconds" % comma(t), ["%s seconds" % comma(x) for x in (m * 100 + s, m + s if m + s != t else t + 1, t + 60)],
                   "%d × 60 = %s seconds%s = <b>%s seconds</b>." % (m, comma(m * 60), (" and %s + %d" % (comma(m * 60), s)) if s else "", comma(t)))
    return mcq("<b>%s seconds</b> = ☐ minutes ☐ seconds" % comma(t), "%d minutes %d seconds" % (m, s) if s else "%d minutes" % m,
               ["%d minutes %d seconds" % (t // 100, t % 100), "%d minutes %d seconds" % (m + 1, s), "%d minutes %d seconds" % (m, s + 10)],
               "%d × 60 = %s, with %d seconds left: <b>%d minutes%s</b>." % (m, comma(m * 60), s, m, (" %d seconds" % s) if s else ""))


def build():
    sets, R = build_sets([
        ("Units of time", [("collect", uniq(one_long), 12), ("run", cbt.set_units, ("rnd", lambda r: __import__("itertools").cycle(cbt.PEOPLE) if hasattr(cbt, "PEOPLE") else cbt.People(r)), 8, nodec)]),
        ("12-hour and 24-hour time", [("run", aut.set_to24, ("rnd",), 10, nodec), ("run", cbt.set_24, ("rnd", lambda r: __import__("itertools").cycle(cbt.PEOPLE) if hasattr(cbt, "PEOPLE") else cbt.People(r)), 10, nodec)]),
        ("Elapsed time", [("run", cbt.set_elapsed, ("rnd", lambda r: __import__("itertools").cycle(cbt.PEOPLE) if hasattr(cbt, "PEOPLE") else cbt.People(r)), 10, nodec), ("run", aut.set_durations, ("rnd",), 10, nodec)]),
        ("Start and end times", [("run", cbt.set_start_end, ("rnd", lambda r: __import__("itertools").cycle(cbt.PEOPLE) if hasattr(cbt, "PEOPLE") else cbt.People(r)), 14, nodec), ("run", aut.set_clocks, ("rnd", lambda r: __import__("itertools").cycle(aut.PEOPLE) if hasattr(aut, "PEOPLE") else aut.People(r)), 6, nodec)]),
        ("Time problems", [("run", cbt.set_story, ("rnd", lambda r: __import__("itertools").cycle(cbt.PEOPLE) if hasattr(cbt, "PEOPLE") else cbt.People(r)), 10, nodec), ("run", aut.set_problems, ("rnd", lambda r: __import__("itertools").cycle(aut.PEOPLE) if hasattr(aut, "PEOPLE") else aut.People(r)), 6, nodec), ("run", cbt.set_elapsed, ("rnd", lambda r: __import__("itertools").cycle(cbt.PEOPLE) if hasattr(cbt, "PEOPLE") else cbt.People(r)), 4, nodec)]),
    ], 80525)
    finish(sets, R)
    body = lesson('<ul><li>60 seconds = 1 minute, 60 minutes = 1 hour, 24 hours = 1 day.</li><li>10 years = 1 decade, 100 years = 1 century, 1 000 years = 1 millennium.</li><li>24-hour time: for p.m. times, add 12 to the hour: 4:25 p.m. = 16:25.</li><li>To find a time interval, count on to the next hour, then the whole hours, then the minutes.</li></ul>',
        [example("From 09:45 to 13:20", ["09:45 → 10:00 is 15 min", "10:00 → 13:00 is 3 h", "13:00 → 13:20 is 20 min"], "3 hours 35 minutes")],
        [['100 seconds', '1 minute = 60 seconds.'], ['Adding 10 for p.m.', 'Add 12: 7 p.m. = 19:00.'], ['Across noon', 'Count on through 12:00.']])
    faq = [('What does CAPS Grade 5 say about time?', 'Read, tell and write time in 12-hour and 24-hour formats, use clocks, calendars and stopwatches, calculate time intervals, and convert between seconds, minutes, hours, days, weeks, months, years, decades and centuries.'), ('How many years is a century?', '100.'), ('What is 21:40 in 12-hour time?', '9:40 p.m.'), ('How do I count an interval?', 'Count on to the next hour first.')]
    make('time', 25, 'Measurement', 'Grade 5: 4.4 Time',
         'Read, tell and write time in 12-hour and 24-hour formats on both analogue and digital instruments in hours, minutes and seconds; use clocks, calendars and stopwatches; calculate time intervals; convert between seconds, minutes, hours, days, weeks, months, years, decades and centuries.',
         'Time: Seconds to Centuries, 24-Hour Time and Time Intervals', 'Time',
         'Free CAPS Grade 5 time worksheets: seconds to centuries, 12-hour and 24-hour time, elapsed time and time problems. 100 questions with memos.',
         '60 s = 1 min, 60 min = 1 h, 100 years = 1 century.', 'p.m. to 24-hour time: add 12.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
