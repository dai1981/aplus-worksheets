# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 4: Data Handling and Presentation
  python3 tools/gen_in_maths_c6_data_handling_and_presentation.py
Collecting and organising data with tally marks, reading pictographs (one symbol stands for several items, half
symbols), and reading and comparing bar graphs (the bar graphs reuse the Class 9 maker).
Wrong answers come from real mistakes: counting symbols instead of multiplying by the key, ignoring a half symbol,
and reading the next grid line on a bar graph.
"""
import random
from in_common import num, unit, T, QN, table
import gen_in_maths_c9_statistics as st

R = random.Random(906004)


def c6(fn):
    def f(r):
        it = fn(r)
        if it:
            it["q"] = it["q"].replace("Class 9", "Class 6").replace("class 9", "class 6")
        return it
    f.__name__ = fn.__name__
    return f


def tally(n):
    return " ".join(["<s>||||</s>"] * (n // 5) + (["|" * (n % 5)] if n % 5 else []))


def one_tally(r):
    kind = r.choice(["read", "read", "count", "most"])
    if kind == "read":
        n = r.randint(6, 29)
        return QN("Tally marks are grouped in fives (<s>||||</s> = 5). What number is shown by %s?" % tally(n), n, [n // 5 + n % 5, n + 5, n - n % 5 + (n % 5) * 5 if n % 5 else n + 1],
                  "%d groups of 5 and %d more: <b>%d</b>." % (n // 5, n % 5, n))
    fruits = r.sample(["Mango", "Banana", "Apple", "Guava", "Orange", "Grapes", "Papaya"], 4)
    data = r.sample(range(3, 19), 4)
    tb = table(["Fruit", "Tally"], [[f, tally(d)] for f, d in zip(fruits, data)])
    if kind == "count":
        return QN(tb + "<p>Students chose their favourite fruit. How many students were asked in all?</p>", sum(data), [sum(data) - data[0], max(data) * 4, sum(data) + 5],
                  "%s = <b>%d</b>." % (" + ".join(map(str, data)), sum(data)))
    i = data.index(max(data))
    return T(tb + "<p>Which fruit was chosen by the most students?</p>", fruits[i], [f for f in fruits if f != fruits[i]], "<b>%s</b> has the most tally marks (%d)." % (fruits[i], data[i]))


def one_picto(r):
    k = r.choice([2, 4, 5, 10, 10, 20, 50, 100])
    days = r.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], 4)
    sym = [r.randint(1, 8) + (0.5 if r.random() < 0.3 and k % 2 == 0 else 0) for _ in days]
    item = r.choice(["books borrowed from the library", "cycles sold in a shop", "visitors to a museum", "trees planted"])
    rows = [[d, "● " * int(s) + ("◐" if s % 1 else "")] for d, s in zip(days, sym)]
    tb = table(["Day", ("Number (● = %d, ◐ = %d)" % (k, k // 2)) if k % 2 == 0 else "Number (● = %d)" % k], rows)
    kind = r.choice(["read", "read", "diff", "total"])
    vals = [int(s * k) for s in sym]
    i, j = r.sample(range(4), 2)
    if kind == "read":
        return QN(tb + "<p>The pictograph shows %s. How many on %s?</p>" % (item, days[i]), vals[i], [sym[i] if sym[i] % 1 == 0 else int(sym[i]) + 1, int(sym[i]) * k, vals[i] + k],
                  "%s symbols × %d = <b>%s</b>." % (num(sym[i]) if sym[i] % 1 == 0 else "%d½" % int(sym[i]), k, num(vals[i])))
    if kind == "diff":
        if vals[i] == vals[j]:
            return None
        if vals[i] < vals[j]:
            i, j = j, i
        return QN(tb + "<p>How many more on %s than on %s?</p>" % (days[i], days[j]), vals[i] - vals[j], [vals[i] + vals[j], int(sym[i] - sym[j] + 0.5), vals[i] - vals[j] + k],
                  "%s − %s = <b>%s</b>." % (num(vals[i]), num(vals[j]), num(vals[i] - vals[j])))
    return QN(tb + "<p>What is the total for the four days?</p>", sum(vals), [int(sum(sym)), sum(vals) - vals[0], sum(vals) + k],
              "%s = <b>%s</b>." % (" + ".join(num(v) for v in vals), num(sum(vals))))


def main():
    unit(6, 0, 4, "data-handling-and-presentation", 4, "D", "Data Handling and Presentation: Tally Marks, Pictographs and Bar Graphs", "data handling and presentation",
         "Collecting and organising data, tally marks, pictographs with a scale, and drawing and interpreting bar graphs (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Data Handling and Presentation worksheet (Ganita Prakash Chapter 4): tally marks, pictographs and bar graphs. 100 questions with answers.",
         "Read the key: one symbol may stand for many", "In a bar graph, read the top of each bar against the scale.",
         "<p><b>Tally marks</b> are grouped in fives so they are easy to count: <s>||||</s> ||| = 8.</p>"
         "<p>In a <b>pictograph</b>, each picture stands for a number given in the key. If ● = 10, then ●●●◐ = 35.</p>"
         "<p>A <b>bar graph</b> uses bars of equal width; the height of each bar shows the value on the scale.</p>",
         [("If ● = 20, what does ●●●● show?", ["4 × 20"], "80"),
          ("What number is <s>||||</s> <s>||||</s> ||?", ["5 + 5 + 2"], "12")],
         ["Counting the symbols in a pictograph without using the key.", "Ignoring a half symbol.", "Reading the next grid line instead of the top of the bar."],
         [("What are tally marks?", "Marks used to count, grouped in fives (four strokes with a fifth across) so the total is quick to read."),
          ("What is a pictograph?", "A chart that uses pictures; the key tells how many items each picture stands for."),
          ("What is a bar graph?", "A graph of bars of equal width whose heights show the values against a scale.")],
         [("Tally marks", [(one_tally, 20)]),
          ("Reading pictographs", [(one_picto, 20)]),
          ("Reading bar graphs", [(c6(st.K(st.one_bar, "read")), 12), (c6(st.K(st.one_bar, "max")), 4), (c6(st.K(st.one_bar, "min")), 4)]),
          ("Comparing with bar graphs", [(c6(st.K(st.one_bar, "diff")), 10), (c6(st.K(st.one_bar, "total")), 6), (c6(st.K(st.one_bar, "times")), 4)]),
          ("Data problems", [(one_picto, 10), (one_tally, 5), (c6(st.one_bar), 5)])], R)


if __name__ == "__main__":
    main()
