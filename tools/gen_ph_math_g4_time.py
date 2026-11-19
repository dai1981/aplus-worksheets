# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Converting Units of Time and Elapsed Time (Grade 4: Measurement and Geometry)
  python3 tools/gen_ph_math_g4_time.py
Converting seconds, minutes, hours, days, weeks, months and years (own maker and UK Year 4 maker), elapsed time on a
clock (US Grade 3 maker), and elapsed time in hours and minutes with a.m. and p.m. (own makers).
Wrong answers come from real mistakes: using 100 minutes in an hour, counting from the wrong time, and forgetting to
regroup 60 minutes.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y4_converting_units as ukc
adopt(ukc)
if hasattr(ukc, 'R'): ukc.R = random.Random(704140)
import gen_us_math_g3_time as ust
adopt(ust)
if hasattr(ust, 'R'): ust.R = random.Random(704141)
ph_common.GRADE = "grade-4"

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


TU = [("minutes", "seconds", 60), ("hours", "minutes", 60), ("days", "hours", 24), ("weeks", "days", 7), ("years", "months", 12)]


def one_tconv(r):
    big, small, f = r.choice(TU + [("months", "weeks", 4)])
    n = r.randint(2, 12 if f > 12 else 20)
    note = " (Use 1 month = 4 weeks.)" if big == "months" else ""
    if r.random() < 0.5:
        right, q, w = n * f, "%d %s = ☐ %s%s" % (n, big, small, note), [n * 100, n + f, n * f // 2 if n * f % 2 == 0 else n * f + f]
        e = "1 %s = %d %s, so %d × %d = <b>%s %s</b>." % (big[:-1], f, small, n, f, comma(n * f), small)
        u = small
    else:
        right, q, w = n, "%s %s = ☐ %s%s" % (comma(n * f), small, big, note), [n * f // 10 if n * f >= 10 else n + 2, n * 10, n + 1]
        e = "%d %s = 1 %s, so %s ÷ %d = <b>%d %s</b>." % (f, small, big[:-1], comma(n * f), f, n, big)
        u = big
    return mcq("Convert. " + q, "%s %s" % (comma(right), u), ["%s %s" % (comma(x), u) for x in w if x != right], e)


def tstr(m):
    h, mi = divmod(m % (24 * 60), 60)
    ap = "a.m." if h < 12 else "p.m."
    h12 = h % 12 or 12
    return "%d:%02d %s" % (h12, mi, ap)


def dur(m):
    h, mi = divmod(m, 60)
    parts = []
    if h:
        parts.append("%d hour%s" % (h, "" if h == 1 else "s"))
    if mi:
        parts.append("%d minute%s" % (mi, "" if mi == 1 else "s"))
    return " ".join(parts)


TRIPS = [("A bus leaves Manila for Baguio at %s. The trip takes %s.", "What time does the bus arrive?", 5, 9, "end"),
         ("A ferry leaves Batangas port at %s and arrives in Calapan at %s.", "How long is the trip?", 1, 3, "dur"),
         ("%(n)s starts studying at %s and studies for %s.", "What time does %(he)s finish?", 1, 3, "end"),
         ("A basketball game starts at %s and ends at %s.", "How long does the game last?", 1, 3, "dur"),
         ("A movie starts at %s. It is %s long.", "What time does it end?", 1, 3, "end"),
         ("%(n)s's family leaves Cebu City at %s and reaches the beach at %s.", "How long is the drive?", 1, 4, "dur"),
         ("A cake goes in the oven at %s and bakes for %s.", "What time is it done?", 0, 1, "end"),
         ("School starts at %s and the last class ends at %s.", "How long is the school day?", 6, 9, "dur")]


def one_elapsed(r):
    k = Kid(r).next()
    t, ask, h1, h2, kind = r.choice(TRIPS)
    start_h = {"A bus": r.choice([5, 6, 7, 21, 22]), "A ferry": r.choice([6, 8, 10, 13]), "School": 7, "A movie": r.choice([13, 15, 18, 19]), "A cake": r.choice([9, 10, 14, 15])}
    s0 = [v for kk, v in start_h.items() if t.startswith(kk) or t.startswith("%(n)s") and False]
    sh = s0[0] if s0 else r.choice([8, 9, 13, 14, 16])
    start = sh * 60 + r.choice(range(0, 60, 5))
    length = r.randint(h1, h2) * 60 + r.choice(range(5, 60, 5))
    if length < 20:
        raise AssertionError
    end = start + length
    t = t.replace("%(n)s", k["n"])
    ask = ask.replace("%(he)s", k["he"])
    if kind == "end":
        q = (t % (tstr(start), dur(length))) + " " + ask
        right = tstr(end)
        w = [tstr(end + 60), tstr(end - 60), tstr(start + (length // 60) * 100 // 60 + length % 60 + 40) if tstr(start + (length // 60) * 100 // 60 + length % 60 + 40) != right else tstr(end + 10)]
        e = "From %s, count on %s: <b>%s</b>" % (tstr(start), dur(length), right)
    else:
        q = (t % (tstr(start), tstr(end))) + " " + ask
        right = dur(length)
        w = [dur(length + 60), dur(abs(length - 40)) if length > 45 else dur(length + 30), dur(length - 60) if length > 60 else dur(length + 120)]
        e = "From %s to %s is <b>%s</b>." % (tstr(start), tstr(end), right)
    if end >= 24 * 60:
        raise AssertionError
    return mcq(q.replace("m..", "m."), right, w, e)


def build():
    sets, R = build_sets([
        ("Convert units of time", [("collect", uniq(one_tconv), 20)]),
        ("Hours, minutes and seconds", [("run", ukc.set_time, ("rnd",), 20)]),
        ("Elapsed time on the clock", [("run", ust.set_elapsed, ("rnd",), 20)]),
        ("Elapsed time with a.m. and p.m.", [("collect", uniq(one_elapsed), 20)]),
        ("Time word problems", [("run", ust.set_story, ("rnd",), 20)]),
    ], 70414)
    finish(sets, R)
    body = lesson('<ul><li>1 minute = 60 seconds, 1 hour = 60 minutes, 1 day = 24 hours, 1 week = 7 days, 1 year = 12 months.</li><li>From a bigger unit to a smaller one, multiply; from a smaller unit to a bigger one, divide.</li><li><b>Elapsed time</b> is how much time passes. Count on in hours, then in minutes.</li><li>Use a.m. for times from midnight to noon and p.m. for times from noon to midnight.</li></ul>',
        [example("Start 9:40 a.m., 2 hours 35 minutes", ["9:40 + 2 hours = 11:40", "11:40 + 35 minutes = 12:15"], "12:15 p.m.")],
        [['100 minutes in an hour', 'An hour has 60 minutes.'], ['Counting from the wrong time', 'Start at the start time.'], ['Not regrouping 60 minutes', '75 minutes is 1 hour 15 minutes.']])
    faq = [('What does MATATAG Math 4 ask about time?', 'Convert time measures from smaller to larger units and vice versa (seconds, minutes, hours, days, weeks, months, years), and solve problems involving conversion of units, including elapsed time in hours and minutes.'), ('How many weeks are in a month?', 'About 4 weeks; most months have a few days more.'), ('Is 12:00 noon a.m. or p.m.?', '12:00 noon is 12:00 p.m.'), ('How do I find elapsed time across noon?', 'Count to 12:00 first, then count on.')]
    make('converting-time-and-elapsed-time', 14, 'Measurement and Geometry', 'Grade 4: Measurement and Geometry',
         'Convert time measures from smaller to larger units, and vice versa: seconds to minutes, minutes to hours, hours to days, days to weeks, weeks to months, and months to years; solve problems involving conversion of units of length, mass, capacity, and time, including problems involving elapsed time in hours and minutes.',
         'Converting Units of Time and Elapsed Time', 'Time and Elapsed Time',
         'Free Grade 4 time worksheets for the DepEd MATATAG curriculum: convert seconds, minutes, hours, days, weeks, months and years, and elapsed time with a.m. and p.m. 100 questions with answers.',
         '1 hour = 60 minutes; count on hours, then minutes.', 'Bigger to smaller unit: multiply.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
