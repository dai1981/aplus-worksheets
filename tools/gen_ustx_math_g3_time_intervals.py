# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Time Intervals in Minutes (TEKS 3.7C)
  python3 tools/gen_ustx_math_g3_time_intervals.py
Reading a clock to the minute and finding how much time passes (the US Grade 3 time makers with Texas names),
adding time intervals in minutes on a number line, subtracting time intervals, and word problems.
Wrong answers come from real mistakes: treating an hour as 100 minutes, counting the tick marks instead of the
jumps, adding when time is used up, and mixing up a.m. and p.m.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, run_many, adopt, svg_wrap, text, line,
                       GREEN, INK, BLUE, example)
import gen_us_math_g3_time as ust

adopt(ust)
R = random.Random(61701)
EVENTS = ["warm up", "read", "practice piano", "eat lunch", "play outside", "do homework", "clean up", "watch a show",
          "ride bikes", "walk the dog", "bake cookies", "swim"]


def jumps_line(parts):
    """Number line in minutes from 0 with one jump per part."""
    tot = sum(parts)
    end = ((tot + 9) // 10) * 10 + 10
    W, x0, x1, y = 460, 24, 436, 70
    X = lambda v: x0 + (x1 - x0) * v / float(end)
    s = [line(x0 - 6, y, x1 + 6, y, INK, 2)]
    for v in range(0, end + 1, 5):
        big = v % 10 == 0
        s.append(line(X(v), y - (8 if big else 5), X(v), y + (8 if big else 5), INK, 2 if big else 1.2))
        if big:
            s.append(text(X(v), y + 26, str(v), 12, weight=400))
    at = 0
    for p in parts:
        xa, xb = X(at), X(at + p)
        mid = (xa + xb) / 2
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (xa, y - 4, mid, y - 44, xb, y - 4, BLUE))
        s.append(text(mid, y - 30, "+%d" % p, 13, col=BLUE))
        at += p
    return svg_wrap(W, y + 36, "".join(s), "number line in minutes with jumps of %s" % ", ".join(map(str, parts)))


# ------------------------------------------------------------ set 3: add time intervals
def one_add(r):
    n = r.choice([2, 2, 3])
    parts = [r.choice([5, 10, 15, 20, 25, 30, 35, 40, 45]) for _ in range(n)]
    tot = sum(parts)
    if tot > 90:
        return None
    k = Kid(r).next()
    evs = r.sample(EVENTS, n)
    desc = ", then ".join("%s for %d minutes" % (e, p) for e, p in zip(evs, parts))
    pic = fig(jumps_line(parts)) if r.random() < 0.6 else ""
    wrong = [tot + 10, tot - 5, tot + 5 if tot % 10 else tot - 10, max(parts) * n if max(parts) * n != tot else tot + 15]
    right = "%d minutes" % tot
    if tot >= 60:
        e = "%s = <b>%d minutes</b>, which is 1 hour%s." % (" + ".join(map(str, parts)), tot, " %d minutes" % (tot - 60) if tot > 60 else "")
    else:
        e = "%s = <b>%d minutes</b>." % (" + ".join(map(str, parts)), tot)
    return mcq(pic + "%s will %s. How many minutes is that in all?" % (k["n"], desc), right, ["%d minutes" % w for w in wrong], e)


# ------------------------------------------------------------ set 4: subtract time intervals
def one_sub(r):
    k = Kid(r).next()
    total = r.choice([30, 40, 45, 50, 60, 75, 90])
    used = r.choice([x for x in range(5, total, 5)])
    kind = r.choice(["left", "left", "longer"])
    if kind == "left":
        what = r.choice(["recess", "free time", "reading time", "screen time", "art time"])
        q = "%s has %d minutes of %s. %s has used %d minutes. How many minutes are left?" % (k["n"], total, what, k["He"], used)
        return mcq(q, "%d minutes" % (total - used), ["%d minutes" % (total + used), "%d minutes" % (100 - used if total == 60 else total - used + 10), "%d minutes" % (total - used - 5) if total - used > 5 else "%d minutes" % (total - used + 5)],
                   "%d − %d = <b>%d minutes</b>." % (total, used, total - used))
    a, b = r.sample(EVENTS, 2)
    ta, tb = r.choice(range(15, 75, 5)), r.choice(range(10, 60, 5))
    if ta <= tb:
        return None
    q = "%s takes %d minutes to %s and %d minutes to %s. How many more minutes does it take to %s?" % (k["n"], ta, a, tb, b, a)
    return mcq(q, "%d minutes" % (ta - tb), ["%d minutes" % (ta + tb), "%d minutes" % (ta - tb + 10), "%d minutes" % (ta - tb - 5) if ta - tb > 5 else "%d minutes" % (ta - tb + 5)],
               "Compare by subtracting: %d − %d = <b>%d minutes</b>." % (ta, tb, ta - tb))


def build():
    sets = []
    for title, fn in [("Read the clock to the minute", ust.set_one), ("How much time passes?", ust.set_elapsed)]:
        sets.append(S(title, run_many(fn, "rnd", seed=181 + len(sets), avoid=sets)))
    sets.append(S("Add time intervals", collect(one_add, 20, R)))
    sets.append(S("Subtract time intervals", collect(one_sub, 20, R)))
    sets.append(S("Time word problems", run_many(ust.set_story, "rnd", seed=185, avoid=sets)))
    finish(sets, R)
    body = lesson(
        "<ul><li>A <b>time interval</b> is how long something takes: 15 minutes, 40 minutes.</li>"
        "<li>To add intervals, add the minutes: a 15-minute event plus a 30-minute event is 45 minutes. A number line with jumps helps.</li>"
        "<li>1 hour = 60 minutes, not 100. 75 minutes is 1 hour 15 minutes.</li>"
        "<li>To find how much time is left or how much longer, subtract.</li></ul>",
        [figure(jumps_line([15, 30]), "15 minutes + 30 minutes = 45 minutes."),
         example("Practice starts at 4:15 p.m. and lasts 35 minutes. When does it end?", ["4:15 + 15 minutes = 4:30", "4:30 + 20 minutes = 4:50"], "4:50 p.m.")],
        [["Thinking an hour is 100 minutes", "1 hour = 60 minutes. Count on to the next hour first."],
         ["Counting tick marks instead of jumps", "Count the minutes each jump covers."],
         ["Adding when the problem asks how much is left", "Time used up means subtract."]])
    faq = [("What does TEKS 3.7C ask?", "Solve problems involving addition and subtraction of time intervals in minutes using pictorial models or tools, such as a 15-minute event plus a 30-minute event equals 45 minutes."),
           ("How do you add time intervals?", "Add the minutes. If the total is 60 or more, you can also say it in hours and minutes: 70 minutes is 1 hour 10 minutes."),
           ("What tools help with elapsed time?", "A number line marked in minutes, or a clock you can move. Jump to the next 5 or 10 minutes, then to the hour."),
           ("How is time tested on the STAAR?", "Word problems ask how long an activity lasts, when it ends, or how much longer one activity is than another.")]
    make("time-intervals", 17, "Geometry and Measurement", "3.7C",
         "3.7C determine the solutions to problems involving addition and subtraction of time intervals in minutes using pictorial models or tools such as a 15-minute event plus a 30-minute event equals 45 minutes",
         "Time Intervals: Adding and Subtracting Minutes", "Time Intervals",
         "Free Grade 3 time worksheets for Texas TEKS 3.7C: read a clock to the minute, how much time passes, add and subtract time intervals in minutes on a number line and word problems. 100 questions with answers.",
         "Add the minutes to put time intervals together.", "1 hour = 60 minutes. A 15-minute event plus a 30-minute event is 45 minutes.",
         body, faq, sets, seo_title="Grade 3 Time Intervals Worksheets: Adding and Subtracting Minutes (TEKS 3.7C)")


if __name__ == "__main__":
    build()
