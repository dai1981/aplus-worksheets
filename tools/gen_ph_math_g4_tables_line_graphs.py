# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Data in Tables and Single Line Graphs (Grade 4: Data and Probability)
  python3 tools/gen_ph_math_g4_tables_line_graphs.py
Data with a time element in tables and single line graphs: presenting data (axes, scale, filling in a table from a
graph), reading values, the highest and lowest points, changes between two times, and problems with two variables in
a table (own makers on the UK Year 4 graph and table drawings).
Wrong answers come from real mistakes: reading the wrong grid line, adding when the question asks for a difference,
and reading the graph for the wrong time.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)

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


import gen_uk_maths_y4_statistics as st4


def hr(h):
    return "%d %s" % (h % 12 or 12, "a.m." if h < 12 else "p.m.")


CTXS = {
    "temp": dict(title="Temperature in the schoolyard", xt="Time", yt="Temperature (°C)", u="°C", what="the temperature", scale=2,
                 noun="temperature", up="warmer", down="cooler"),
    "plant": dict(title="Height of a mongo plant", xt="Day", yt="Height (cm)", u="cm", what="the height of the plant", scale=2,
                  noun="height", up="taller", down="shorter"),
    "lib": dict(title="Learners in the library", xt="Time", yt="Number of learners", u="learners", what="the number of learners", scale=5,
                noun="number of learners", up="more", down="fewer"),
    "tank": dict(title="Water in a tank", xt="Time", yt="Water (L)", u="L", what="the amount of water", scale=20,
                 noun="amount of water", up="more", down="less"),
    "sales": dict(title="Pandesal sold at a bakery", xt="Day", yt="Pieces sold", u="pieces", what="the number of pieces sold", scale=50,
                  noun="number of pieces sold", up="more", down="fewer"),
}
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
DAYN = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}


class Data:
    def __init__(self, r):
        self.kind = r.choice(list(CTXS))
        self.c = CTXS[self.kind]
        sc = self.c["scale"]
        for _ in range(500):
            if self.kind == "temp":
                h0 = r.choice([6, 7, 8])
                self.xl = [hr(h) for h in range(h0, h0 + 7)]
                v = [r.randint(22, 25)]
                for d in (2, 2, 2, 1, 0, -2):
                    v.append(v[-1] + d + r.choice([-1, 0, 1]))
            elif self.kind == "plant":
                self.xl = [str(d) for d in range(1, 8)]
                v = [r.randint(1, 3)]
                for _k in range(6):
                    v.append(v[-1] + r.randint(1, 4))
            elif self.kind == "lib":
                h0 = r.choice([7, 8])
                self.xl = [hr(h) for h in range(h0, h0 + 7)]
                v = [r.randint(0, 3) * 5 + r.choice([0, 0, 5]) + 5 for _k in range(7)]
                v = [x if x > 0 else 5 for x in v]
            elif self.kind == "tank":
                h0 = r.choice([6, 7])
                self.xl = [hr(h) for h in range(h0, h0 + 6)]
                v = [r.choice([180, 200])]
                for _k in range(5):
                    v.append(v[-1] - r.choice([0, 10, 20, 30, 40]))
            else:
                d0 = 0
                self.xl = DAYS[:]
                v = [r.randint(4, 10) * 50 + r.choice([0, 25]) for _k in range(6)]
            n = len(v)
            top = -(-max(v) // sc) * sc
            if not (3 <= top // sc <= 10) or min(v) < 0:
                continue
            ch = [v[i + 1] - v[i] for i in range(n - 1)]
            if v.count(max(v)) == 1 and v.count(min(v)) == 1 and ch.count(max(ch)) == 1 and ch.count(min(ch)) == 1:
                break
        else:
            raise AssertionError
        self.v = v

    def at(self, i):
        x = self.xl[i]
        if self.kind == "plant":
            return "day %s" % x
        if self.kind == "sales":
            return DAYN[x]
        return x

    def at2(self, i):
        return ("on " if self.kind in ("plant", "sales") else "at ") + self.at(i)

    def val(self, x):
        u = self.c["u"]
        return "%s %s" % (comma(x), u) if u not in ("°C",) else "%d°C" % x

    def graph(self):
        return fig(st4.time_svg(self.c["title"], self.xl, self.c["xt"], self.c["yt"], self.v, self.c["scale"], label="line graph: " + self.c["title"].lower()))

    def table(self, hide=None):
        rows = [[self.xl[i] if self.kind != "sales" else self.xl[i], "?" if i == hide else comma(self.v[i])] for i in range(len(self.v))]
        head = [self.c["xt"], self.c["yt"]]
        return fig(st4.table_svg(self.c["title"], head, rows, label="table: " + self.c["title"].lower()))


def one_read(r):
    D = Data(r)
    n, v, sc = len(D.v), D.v, D.c["scale"]
    kind = r.choice(["read", "read", "max", "min", "when"])
    if kind == "read":
        i = r.randrange(n)
        q = D.graph() + "What was %s %s?" % (D.c["what"], D.at2(i))
        wr = [v[i] + sc, v[i] - sc, v[i - 1] if i else v[i + 1], v[(i + 1) % n]]
        return mcq(q, D.val(v[i]), [D.val(x) for x in wr if x >= 0], "Go up from %s to the point, then across to the scale: <b>%s</b>." % (D.at(i), D.val(v[i])))
    if kind in ("max", "min"):
        i = v.index(max(v) if kind == "max" else min(v))
        word = {"temp": ("warmest", "coolest"), "plant": None, "lib": ("the most learners", "the fewest learners"), "tank": ("the most water", "the least water"),
                "sales": ("the most pieces sold", "the fewest pieces sold")}[D.kind]
        if word is None:
            raise AssertionError
        w = word[0] if kind == "max" else word[1]
        ask = "When was it %s?" % w if D.kind == "temp" else "When were there %s?" % w if D.kind == "lib" else "When was there %s?" % w if D.kind == "tank" else "On which day were %s?" % w.replace("the most pieces sold", "the most pieces sold").replace("the fewest", "the fewest")
        if D.kind == "sales":
            ask = "On which day did the bakery sell %s pandesal?" % ("the most" if kind == "max" else "the fewest")
        j = v.index(min(v) if kind == "max" else max(v))
        wr = [D.at(j), D.at(i - 1) if i else D.at(i + 1), D.at((i + 1) % n), D.at((i + 2) % n)]
        return mcq(D.graph() + ask, D.at(i), wr, "Find the %s point on the line: it is at %s (%s). <b>%s</b>." % ("highest" if kind == "max" else "lowest", D.at(i), D.val(v[i]), D.at(i)))
    i = r.randrange(n)
    if v.count(v[i]) > 1:
        raise AssertionError
    ask = {"temp": "At what time was the temperature %s?", "plant": "On which day was the plant %s tall?", "lib": "At what time were there %s in the library?",
           "tank": "At what time was there %s of water in the tank?", "sales": "On which day were %s sold?"}[D.kind]
    q = D.graph() + ask % D.val(v[i])
    wr = [D.at(k) for k in range(n) if k != i]
    r.shuffle(wr)
    return mcq(q, D.at(i), wr, "Find %s on the scale and go across to the point, then down: <b>%s</b>." % (D.val(v[i]), D.at(i)))


def one_change(r):
    D = Data(r)
    n, v = len(D.v), D.v
    kind = r.choice(["diff", "diff", "most", "trend"])
    if kind == "diff":
        i, j = sorted(r.sample(range(n), 2))
        if v[i] == v[j]:
            raise AssertionError
        d = abs(v[j] - v[i])
        word = D.c["up"] if v[j] > v[i] else D.c["down"]
        if D.kind == "plant":
            q = "How much did the plant grow from day %s to day %s?" % (D.xl[i], D.xl[j])
        elif D.kind == "sales":
            q = "How many more pieces were sold on %s than on %s?" % ((D.at(j), D.at(i)) if v[j] > v[i] else (D.at(i), D.at(j)))
        else:
            q = "How much %s was %s %s than %s?" % (word, D.c["what"], D.at2(j), D.at2(i)) if D.kind != "lib" else "How many %s learners were there %s than %s?" % (word, D.at2(j), D.at2(i))
        wr = [v[i] + v[j], max(v[i], v[j]), d + D.c["scale"], abs(d - D.c["scale"])]
        return mcq(D.graph() + q, D.val(d), [D.val(x) for x in wr if x > 0 and x != d], "Read both points: %s %s and %s %s. %s − %s = <b>%s</b>." % (D.val(v[i]), D.at2(i), D.val(v[j]), D.at2(j), comma(max(v[i], v[j])), comma(min(v[i], v[j])), D.val(d)))
    ch = [v[k + 1] - v[k] for k in range(n - 1)]
    if kind == "most":
        up = r.random() < 0.6 and max(ch) > 0
        k = ch.index(max(ch) if up else min(ch))
        if not up and ch[k] >= 0:
            raise AssertionError
        lab = lambda a: ("%s to %s" % (D.at(a), D.at(a + 1)))[0].upper() + ("%s to %s" % (D.at(a), D.at(a + 1)))[1:]
        q = "Between which two %s did %s go %s the most?" % ("days" if D.kind in ("plant", "sales") else "times", D.c["what"], "up" if up else "down")
        wr = [lab(a) for a in range(n - 1) if a != k]
        r.shuffle(wr)
        return mcq(D.graph() + q, lab(k), wr, "Look for the steepest part of the line going %s: from %s, a change of %s. <b>%s</b>." % ("up" if up else "down", lab(k).lower() if D.kind == "plant" else lab(k), D.val(abs(ch[k])), lab(k)))
    k = r.randrange(n - 1)
    s = "went up" if ch[k] > 0 else "went down" if ch[k] < 0 else "stayed the same"
    opts = ["went up", "went down", "stayed the same", "went up, then down"]
    q = D.graph() + "What happened to %s from %s to %s?" % (D.c["what"], D.at(k), D.at(k + 1))
    return mcq(q, s, [o for o in opts if o != s], "%s %s, %s %s, so it <b>%s</b>. A line going up shows an increase; a flat line shows no change." % (D.val(v[k]), D.at2(k), D.val(v[k + 1]), D.at2(k + 1), s))


def one_present(r):
    kind = r.choice(["missing", "missing", "missing", "time", "axis"])
    if kind == "missing":
        D = Data(r)
        i = r.randrange(len(D.v))
        q = D.graph() + D.table(hide=i) + "The table shows the same data as the line graph. What number goes in place of the ?"
        v = D.v[i]
        wr = [v + D.c["scale"], v - D.c["scale"], D.v[i - 1] if i else D.v[i + 1], v + 1]
        return mcq(q, comma(v), [comma(x) for x in wr if x > 0 and x != v], "Find %s on the graph and read across: <b>%s</b>." % (D.at(i), comma(v)))
    if kind == "time":
        good = ["the temperature in the classroom every hour", "the height of a plant every day", "the number of jeepneys passing every 10 minutes",
                "the rainfall in Davao each month", "the weight of a puppy every week", "the amount of rice sold each day"]
        bad = ["the favorite fruits of the class", "the colors of cars in a parking lot", "the number of learners in each section", "the favorite sports of Grade 4",
               "the kinds of trees in the park", "the number of pets each learner has"]
        if r.random() < 0.5:
            g = r.choice(good)
            return mcq("Which data has a <b>time element</b> and can be shown in a line graph?", g, r.sample(bad, 3),
                       "Data with a time element is collected again and again over time, so it shows a change. <b>%s</b>." % g)
        b = r.choice(bad)
        return mcq("Which data does <b>not</b> have a time element?", b, r.sample(good, 3), "The others are measured again and again over time. <b>%s</b> is collected only once.%s" % (b[0].upper() + b[1:], ""))
    D = Data(r)
    k = r.choice(["x", "y", "title"])
    if k == "x":
        right = D.c["xt"]
        wr = [D.c["yt"], D.c["title"], "Number of points"]
        return mcq(D.table() + "You make a line graph of this table. What do you write along the <b>horizontal</b> axis?", right, wr, "Time (hours or days) goes along the horizontal axis. <b>%s</b>." % right)
    if k == "y":
        right = D.c["yt"]
        wr = [D.c["xt"], D.c["title"], "Number of days"]
        return mcq(D.table() + "You make a line graph of this table. What do you write along the <b>vertical</b> axis?", right, wr, "The values that change go on the vertical axis. <b>%s</b>." % right)
    hi = max(D.v)
    sc = D.c["scale"]
    right = "0 to %s, by %ss" % (comma(-(-hi // sc) * sc), comma(sc))
    wr = ["0 to %s, by 1s" % comma(hi), "0 to %s, by %ss" % (comma(-(-hi // sc) * sc // 2), comma(sc)), "%s to %s, by %ss" % (comma(min(D.v)), comma(hi), comma(sc * 10))]
    return mcq(D.table() + "You make a line graph of this table. Which scale fits best on the vertical axis?", right, wr,
               "The scale must start at 0 and go past the greatest value, %s, with equal steps. <b>%s</b>." % (comma(hi), right))


T2 = [("Rice sold at a store (kg)", "Day", "Rice", "Corn", "kg", "rice", "corn"),
      ("Learners who walked or rode to school", "Day", "Walked", "Rode", "learners", "walked", "rode"),
      ("Mangoes picked on a farm", "Day", "Carabao", "Indian", "mangoes", "Carabao mangoes", "Indian mangoes")]


def one_two(r):
    title, xt, A, B, u, an, bn = r.choice(T2)
    days = DAYS[:5]
    if "kg" in title:
        va = [r.randint(20, 90) for _ in days]
        vb = [r.randint(10, 60) for _ in days]
    elif "Learners" in title:
        va = [r.randint(80, 150) for _ in days]
        vb = [r.randint(40, 120) for _ in days]
    else:
        va = [r.randint(100, 400) for _ in days]
        vb = [r.randint(50, 300) for _ in days]
    if len(set(va)) < 5 or len(set(vb)) < 5 or any(a == b for a, b in zip(va, vb)):
        raise AssertionError
    rows = [[d, comma(a), comma(b)] for d, a, b in zip(days, va, vb)]
    T = fig(st4.table_svg(title, [xt, A, B], rows, label="table: " + title.lower()))
    kind = r.choice(["diff", "total", "both", "most_diff", "more"])
    i = r.randrange(5)
    uu = (lambda x: "%s %s" % (comma(x), u))
    if kind == "diff":
        d = abs(va[i] - vb[i])
        q = "On %s, how many more %s than %s were there?" % (DAYN[days[i]], *((an, bn) if va[i] > vb[i] else (bn, an))) if u != "kg" else "On %s, how much more %s than %s was sold?" % (DAYN[days[i]], *((an, bn) if va[i] > vb[i] else (bn, an)))
        return mcq(T + q, uu(d), [uu(x) for x in (va[i] + vb[i], d + 10, abs(va[(i + 1) % 5] - vb[(i + 1) % 5]))], "%s − %s = <b>%s</b>." % (comma(max(va[i], vb[i])), comma(min(va[i], vb[i])), uu(d)))
    if kind == "total":
        col, nm = r.choice([(va, an), (vb, bn)])
        t = sum(col)
        q = "What is the total for %s from Monday to Friday?" % nm
        return mcq(T + q, uu(t), [uu(x) for x in (t - col[-1], t + 10, sum(va) + sum(vb) - t if sum(va) + sum(vb) - t != t else t + 20)], "%s = <b>%s</b>." % (" + ".join(comma(x) for x in col), uu(t)))
    if kind == "both":
        t = va[i] + vb[i]
        q = "How many %s were there in all on %s?" % (u, DAYN[days[i]]) if u != "kg" else "How many kilograms of rice and corn were sold in all on %s?" % DAYN[days[i]]
        return mcq(T + q, uu(t), [uu(x) for x in (abs(va[i] - vb[i]), t + 10, va[(i + 1) % 5] + vb[(i + 1) % 5])], "%s + %s = <b>%s</b>." % (comma(va[i]), comma(vb[i]), uu(t)))
    if kind == "most_diff":
        ds = [abs(a - b) for a, b in zip(va, vb)]
        if ds.count(max(ds)) > 1:
            raise AssertionError
        k = ds.index(max(ds))
        q = "On which day was the difference between %s and %s the greatest?" % (an, bn)
        return mcq(T + q, DAYN[days[k]], [DAYN[days[j]] for j in sorted(range(5), key=lambda j: -ds[j]) if j != k][:3],
                   "Differences: %s. The greatest is on <b>%s</b>." % (", ".join("%s %s" % (days[j], comma(ds[j])) for j in range(5)), DAYN[days[k]]))
    cnt = sum(1 for a, b in zip(va, vb) if a > b)
    q = "On how many days were there more %s than %s?" % (an, bn) if u != "kg" else "On how many days was more rice than corn sold?"
    return mcq(T + q, cnt, [x for x in range(6) if x != cnt][:3] if cnt > 2 else [cnt + 1, cnt + 2, 5 - cnt if 5 - cnt != cnt else cnt + 3],
               "Compare the two numbers for each day. %s on <b>%d</b> day%s." % ("More " + an + " than " + bn, cnt, "" if cnt == 1 else "s"), allow_zero=True)


def build():
    sets, R = build_sets([
        ("Present data in tables and line graphs", [("collect", uniq(one_present), 20)]),
        ("Read a line graph", [("collect", uniq(one_read), 20)]),
        ("Changes over time", [("collect", uniq(one_change), 20)]),
        ("Two variables in a table", [("collect", uniq(one_two), 20)]),
        ("Line graph problems", [("collect", uniq(one_change), 10), ("collect", uniq(one_read), 10)]),
    ], 70425)
    finish(sets, R)
    body = lesson('<ul><li>Data with a <b>time element</b> is collected again and again over time: every hour, every day, every month.</li><li>A <b>single line graph</b> shows how one quantity changes over time. Time goes on the horizontal axis; the values go on the vertical axis.</li><li>To read a point, go up from the time to the point, then across to the scale. Check what each grid line stands for.</li><li>A line going up shows an increase, a line going down shows a decrease, and a flat line shows no change. The steepest part shows the biggest change.</li></ul>',
        [example("Temperature: 24°C at 8 a.m., 30°C at 12 p.m.", ["30 − 24"], "6°C warmer")],
        [['Reading the wrong grid line', 'Check the scale first: each line may be 2, 5 or 10.'], ['Adding instead of subtracting', '“How much more” asks for a difference.'], ['Using the wrong time', 'Go straight up from the time you need.']])
    faq = [('What does MATATAG Math 4 ask about data?', 'Collect data with a time element, present data in a tabular form or in a single line graph, interpret it, and solve problems using data for at most two variables in a tabular form or in a single line graph.'), ('When should I use a line graph?', 'When data changes over time, like temperature every hour.'), ('Must the scale start at 0?', 'In Grade 4, yes: start at 0 and use equal steps.'), ('What is a variable?', 'A quantity that changes, like the amount of rice sold.')]
    make('tables-and-line-graphs', 25, 'Data and Probability', 'Grade 4: Data and Probability',
         'Collect data with time element using appropriate sources; present data in a tabular form, or in a single line graph; interpret data presented in a tabular form, or in a single line graph; solve problems using data for at most two variables in a tabular form, or in a single line graph.',
         'Data in Tables and Single Line Graphs', 'Tables and Line Graphs',
         'Free Grade 4 tables and line graphs worksheets for the DepEd MATATAG curriculum: data with a time element, reading line graphs, changes over time and two-variable tables. 100 questions with answers.',
         'Time goes across; the values go up.', 'Check the scale before you read a point.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
