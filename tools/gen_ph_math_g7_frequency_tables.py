# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Organizing Data in a Frequency Distribution Table (Grade 7: Data and Probability)
  python3 tools/gen_ph_math_g7_frequency_tables.py
Counting frequencies from raw data, class width, class marks and classes, reading a grouped frequency table (own
makers), and grouped data (Singapore Secondary 2 maker).
Wrong answers come from real mistakes: counting a value twice, taking the class width as upper minus lower limit,
and putting a boundary value in the wrong class.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_sg_maths_s2_frequency_tables_and_grouped_data as sgf
adopt(sgf)
if hasattr(sgf, 'R'): sgf.R = random.Random(707190)
ph_common.GRADE = "grade-7"

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


def one_tally(r):
    vals = [r.choice([1, 2, 2, 3, 3, 3, 4, 4, 5]) for _ in range(r.choice([15, 18, 20, 24]))]
    k = r.randint(1, 5)
    what = r.choice(["the number of siblings of %d learners" % len(vals), "the number of books read by %d learners last month" % len(vals),
                     "the number of pets of %d families" % len(vals), "the number of jeepney rides of %d learners in a day" % len(vals)])
    c = vals.count(k)
    if c == 0:
        raise AssertionError
    q = "The data show %s:<br><b>%s</b><br>In a frequency table, what is the frequency of %d?" % (what, ", ".join(map(str, vals)), k)
    return mcq(q, c, [c + 1, c - 1, len(vals) - c, k], "Count every %d in the list: there are <b>%d</b>. The frequencies of all the values add up to %d." % (k, c, len(vals)), allow_zero=True)


def one_class(r):
    lo = r.choice([10, 20, 30, 40, 50, 60])
    w = r.choice([5, 10])
    k = r.randint(0, 4)
    a = lo + k * w
    b = a + w - 1
    kind = r.choice(["width", "mark", "which"])
    if kind == "width":
        q = "A frequency table has the classes %d–%d, %d–%d, %d–%d. What is the class width (class size)?" % (lo, lo + w - 1, lo + w, lo + 2 * w - 1, lo + 2 * w, lo + 3 * w - 1)
        return mcq(q, w, [w - 1, w + 1, 3 * w], "From one lower limit to the next: %d − %d = <b>%d</b>." % (lo + w, lo, w))
    if kind == "mark":
        m = (a + b) / 2
        ms = ("%g" % m)
        q = "What is the class mark (midpoint) of the class %d–%d?" % (a, b)
        return mcq(q, ms, ["%g" % x for x in (b - a, a + w / 2, (a + b + 1) / 2 + 1)] + [str(a)], "Class mark = (lower limit + upper limit) ÷ 2 = (%d + %d) ÷ 2 = <b>%s</b>." % (a, b, ms))
    v = r.randint(a, b)
    q = "Scores are grouped in classes %d–%d, %d–%d, %d–%d, … In which class is a score of %d?" % (lo, lo + w - 1, lo + w, lo + 2 * w - 1, lo + 2 * w, lo + 3 * w - 1, v)
    right = "%d–%d" % (a, b)
    wr = ["%d–%d" % (a + w, b + w), "%d–%d" % (a - w, b - w) if a - w >= lo else "%d–%d" % (a + 2 * w, b + 2 * w), "%d–%d" % (v, v + w - 1) if v != a else "%d–%d" % (a + 1, b + 1)]
    return mcq(q, right, wr, "%d is from %d to %d, so it is in the class <b>%s</b>." % (v, a, b, right))


def one_freq(r):
    lo, w = r.choice([(31, 5), (41, 5), (50, 10), (60, 10), (1, 5)])
    fs = [r.randint(1, 12) for _ in range(5)]
    cls = ["%d–%d" % (lo + i * w, lo + (i + 1) * w - 1) for i in range(5)]
    import gen_uk_maths_y4_statistics as st4
    tbl = fig(st4.table_svg("Frequency distribution table", ["Class", "Frequency"], [[c, str(f)] for c, f in zip(cls, fs)], label="frequency distribution table"))
    kind = r.choice(["total", "most", "atleast"])
    if kind == "total":
        return mcq(tbl + "How many data values are in the table?", sum(fs), [sum(fs) - fs[0], len(fs), max(fs) * 5], "Add the frequencies: %s = <b>%d</b>." % (" + ".join(map(str, fs)), sum(fs)))
    if kind == "most":
        if fs.count(max(fs)) > 1:
            raise AssertionError
        i = fs.index(max(fs))
        return mcq(tbl + "Which class has the most data values?", cls[i], [c for j, c in enumerate(cls) if j != i][:3], "The greatest frequency is %d, in the class <b>%s</b>." % (max(fs), cls[i]))
    k = r.randint(2, 4)
    s = sum(fs[k:])
    return mcq(tbl + "How many values are %d or more?" % (lo + k * w), s, [sum(fs[:k]), s + fs[k - 1], fs[k]], "Add the classes from %s up: %s = <b>%d</b>." % (cls[k], " + ".join(map(str, fs[k:])), s), allow_zero=True)


def build():
    sets, R = build_sets([
        ("Count the frequency", [("collect", uniq(one_tally), 20)]),
        ("Classes, class width and class marks", [("collect", uniq(one_class), 20)]),
        ("Read a frequency distribution table", [("collect", uniq(one_freq), 20)]),
        ("Grouped data", [("collect", sgf.one_grouped, 20)]),
        ("Frequency tables mixed", [("collect", uniq(one_freq), 7), ("collect", uniq(one_class), 7), ("collect", uniq(one_tally), 6)]),
    ], 70719)
    finish(sets, R)
    body = lesson('<ul><li>A <b>frequency distribution table</b> shows each value or class and how many times it occurs (its frequency).</li><li>Use tally marks to count, then write the frequency. The frequencies add up to the number of data values.</li><li>For many different values, group them into <b>classes</b> of equal width, like 50–59, 60–69. The <b>class width</b> is the difference between the lower limits: 60 − 50 = 10.</li><li>The <b>class mark</b> is the midpoint of a class: (50 + 59) ÷ 2 = 54.5.</li></ul>',
        [example("Classes 41–45, 46–50, 51–55", ["46 − 41 = 5", "(41 + 45) ÷ 2 = 43"], "width 5, first class mark 43")],
        [['Counting twice', 'Cross out each value as you tally it.'], ['Width = upper − lower', '45 − 41 = 4, but the width is 5.'], ['Boundary values', '50 belongs to 46–50, not 51–55.']])
    faq = [('What does MATATAG Math 7 ask about frequency tables?', 'Organize statistical data in a frequency distribution table.'), ('How many classes should I use?', 'Usually 5 to 10 classes of equal width.'), ('What is a class mark used for?', 'It stands for all the values in the class, for example to estimate the mean.'), ('What is relative frequency?', 'The frequency divided by the total.')]
    make('frequency-distribution-tables', 19, 'Data and Probability', 'Grade 7: Data and Probability',
         'Organize statistical data in a frequency distribution table.',
         'Organizing Data in a Frequency Distribution Table', 'Frequency Distribution Tables',
         'Free Grade 7 frequency distribution table worksheets for the DepEd MATATAG curriculum: tallies, frequencies, classes, class width, class marks and grouped data. 100 questions with answers.',
         'The frequencies add up to the number of data values.', 'Class mark = (lower limit + upper limit) ÷ 2.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
