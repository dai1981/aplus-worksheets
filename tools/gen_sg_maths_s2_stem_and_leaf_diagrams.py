# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Stem-and-leaf diagrams (MOE syllabus S1 Data handling and analysis)
  python3 gen_sg_maths_s2_stem_and_leaf_diagrams.py
Reading stem-and-leaf diagrams, finding the median, mode, range and mean from a diagram, building a diagram from data,
describing shape, centre, spread and outliers, and comparing two data sets with back-to-back diagrams.
Wrong answers come from real mistakes: reading a leaf on its own (4 instead of 24), counting stems instead of
leaves, finding the median before checking the leaves are in order, and forgetting the key.
"""
import random
from fractions import Fraction as F
from sg_sec import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, INK, RED, BLUE

R = random.Random(821600)
CTX = [("The ages of people in a dance class", "years"), ("The number of goals scored by netball players in a season", "goals"),
       ("The heights of tomato plants, in cm", "cm"), ("The scores in a maths quiz out of 60", "marks"),
       ("The number of minutes students spent on homework", "minutes"), ("Daily maximum temperatures in Singapore, in °C", "°C"),
       ("The masses of puppies at a vet, in kg", "kg"), ("The number of runs scored by a cricket team", "runs")]


def plot_svg(data, key_stem=None, label="stem-and-leaf diagram", back=None):
    """data: sorted list of 2-digit numbers. back: optional second data set shown on the left (back-to-back)."""
    stems = sorted(set(v // 10 for v in data + (back or [])))
    stems = list(range(stems[0], stems[-1] + 1))
    rows = len(stems)
    lh = 26
    cx = 170 if back else 60
    W = 340 if back else 300
    s = [text(cx, 22, "Stem", 13), line(cx + 22, 8, cx + 22, 34 + rows * lh, INK, 2)]
    s.append(text(cx + 30, 22, "Class A" if back else "Leaf", 13, anchor="start"))
    if back:
        s.append(text(cx - 30, 22, "Class B", 13, anchor="end"))
        s.append(line(cx - 22, 8, cx - 22, 34 + rows * lh, INK, 2))
    s.append(line(10, 30, W - 10, 30, INK, 1))
    for i, st in enumerate(stems):
        y = 30 + (i + 1) * lh - 7
        s.append(text(cx, y, str(st), 16))
        leaves = [v % 10 for v in data if v // 10 == st]
        s.append(text(cx + 30, y, "  ".join(str(l) for l in leaves), 16, anchor="start", weight=400))
        if back:
            bl = sorted([v % 10 for v in back if v // 10 == st], reverse=True)
            s.append(text(cx - 30, y, "  ".join(str(l) for l in bl), 16, anchor="end", weight=400))
    ks = key_stem if key_stem is not None else stems[0]
    kv = ks * 10 + 4
    s.append(text(W / 2 if not back else W / 2, 30 + rows * lh + 26, "Key: %d | 4 = %d" % (ks, kv), 13, col=BLUE))
    return svg_wrap(W, 30 + rows * lh + 38, "".join(s), label)


def make_data(r, n=None, lo=1, hi=6):
    n = n or r.randint(11, 17)
    st = r.randint(lo, hi - 2)
    span = r.randint(3, 4)
    vals = sorted(r.randint(st * 10, (st + span) * 10 - 1) for _ in range(n))
    return vals


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def mode(xs):
    c = {}
    for x in xs:
        c[x] = c.get(x, 0) + 1
    m = max(c.values())
    ms = [k for k, v in c.items() if v == m]
    return ms[0] if len(ms) == 1 and m > 1 else None


# ------------------------------------------------------------ set 1: reading a diagram
def one_read(r):
    d = make_data(r)
    ctx, u = r.choice(CTX)
    g = fig(plot_svg(d))
    kind = r.choice(["count", "max", "min", "over"])
    stems = sorted(set(v // 10 for v in d))
    if kind == "count":
        q = g + "%s are shown. How many values are in the diagram?" % ctx
        return QN(q, len(d), [len(stems), len(d) - 1, len(d) + len(stems)], "Count the leaves, not the stems: there are <b>%d</b> values." % len(d))
    if kind == "max":
        q = g + "%s are shown. What is the largest value?" % ctx
        return QN(q, d[-1], [d[-1] % 10, d[-1] // 10, d[-1] + 10], "The last leaf in the last row: <b>%d</b>. Use the key to join the stem and the leaf." % d[-1])
    if kind == "min":
        q = g + "%s are shown. What is the smallest value?" % ctx
        return QN(q, d[0], [d[0] % 10, d[0] // 10 * 10, d[0] + 10], "The first leaf in the first row: <b>%d</b>." % d[0])
    t = r.choice(d[2:-2]) // 10 * 10 + r.choice([0, 5])
    c = sum(1 for v in d if v > t)
    if c in (0, len(d)):
        return None
    q = g + "%s are shown. How many values are greater than %d?" % (ctx, t)
    return QN(q, c, [sum(1 for v in d if v >= t) if sum(1 for v in d if v >= t) != c else c + 1, len(d) - c, c - 1 if c > 1 else c + 2],
              "Count the values above %d: <b>%d</b>." % (t, c))


# ------------------------------------------------------------ set 2: median and mode
def one_medmode(r):
    d = make_data(r)
    g = fig(plot_svg(d))
    if r.random() < 0.6:
        md = median(d)
        n = len(d)
        q = g + "Find the median of the data."
        pos = "the %s value" % ("%dth" % ((n + 1) // 2) if (n + 1) // 2 not in (1, 2, 3) else {1: "1st", 2: "2nd", 3: "3rd"}[(n + 1) // 2]) if n % 2 else "halfway between the %dth and %dth values" % (n // 2, n // 2 + 1)
        e = "There are %d values, so the median is %s: <b>%s</b>." % (n, pos, num(md))
        return QN(q, md, [F(n + 1, 2), F(d[n // 2]) if F(d[n // 2]) != md else md + 1, median([v % 10 for v in d])], e)
    m = mode(d)
    if m is None:
        return None
    q = g + "What is the mode of the data?"
    cnt = d.count(m)
    return QN(q, m, [m % 10, cnt, max(set(v // 10 for v in d), key=lambda st: sum(1 for v in d if v // 10 == st)) * 10],
              "The value that appears most often is <b>%d</b> (%d times). Look for repeated leaves on the same stem." % (m, cnt))


# ------------------------------------------------------------ set 3: range and mean
def one_rangemean(r):
    if r.random() < 0.55:
        d = make_data(r)
        rg = d[-1] - d[0]
        q = fig(plot_svg(d)) + "Find the range of the data."
        return QN(q, rg, [d[-1], d[-1] % 10 - d[0] % 10 if d[-1] % 10 != d[0] % 10 else rg + 10, d[-1] // 10 - d[0] // 10], "Range = largest − smallest = %d − %d = <b>%d</b>." % (d[-1], d[0], rg))
    for _ in range(50):
        d = make_data(r, n=r.choice([5, 6, 8]))
        m = F(sum(d), len(d))
        if m.denominator in (1, 2, 4, 5):
            break
    else:
        return None
    q = fig(plot_svg(d)) + "Find the mean of the data."
    return QN(q, m, [median(d), F(sum(d), len(d) - 1), F(sum(v % 10 for v in d), len(d))], "Total = %s. %s ÷ %d = <b>%s</b>." % (num(sum(d)), num(sum(d)), len(d), num(m)))


# ------------------------------------------------------------ set 4: building a diagram
def row_text(data, st):
    return "%d | %s" % (st, " ".join(str(v % 10) for v in sorted(data) if v // 10 == st))


def one_build(r):
    d = make_data(r, n=r.randint(9, 13))
    shown = d[:]
    r.shuffle(shown)
    st = r.choice(sorted(set(v // 10 for v in d)))
    right = row_text(d, st)
    leaves = [v % 10 for v in sorted(d) if v // 10 == st]
    if len(leaves) < 2:
        return None
    unsorted = "%d | %s" % (st, " ".join(str(v % 10) for v in shown if v // 10 == st))
    wr = [unsorted if unsorted != right else "%d | %s" % (st, " ".join(str(x) for x in reversed(leaves))),
          "%d | %s" % (st, " ".join(str(v) for v in sorted(d) if v // 10 == st)),
          "%d | %s" % (st, " ".join(str(x) for x in sorted(set(leaves)))) if len(set(leaves)) < len(leaves) else "%d | %s" % (st, " ".join(str(x) for x in leaves[:-1]))]
    q = "These values are put in an ordered stem-and-leaf diagram: %s. Which is the row for stem %d?" % (B(", ".join(str(v) for v in shown)), st)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, "Each value %d0–%d9 goes on stem %d, with its ones digit as a leaf, in order. Repeated values keep every leaf: <b>%s</b>." % (st, st, st, right))


# ------------------------------------------------------------ set 5: interpreting and comparing
def problems():
    its = []
    a = [22, 25, 28, 31, 33, 34, 36, 38, 41, 44, 47]
    b = [15, 19, 21, 24, 26, 27, 29, 30, 32, 35, 51]
    g = fig(plot_svg(a, back=b, label="back-to-back stem-and-leaf diagram"))
    head = g + "The back-to-back diagram shows quiz scores for Class A (right) and Class B (left). "
    its += [
        T(head + "What is the median score for Class A?", "34", ["30", "33", "36"], "Class A has 11 scores; the 6th is <b>34</b>."),
        T(head + "What is the median score for Class B?", "27", ["26", "29", "24"], "Class B has 11 scores; the 6th in order is <b>27</b>."),
        T(head + "Which class had the higher median?", "Class A", ["Class B", "They are the same", "You cannot tell"], "34 is higher than 27, so <b>Class A</b>."),
        T(head + "What is the range for Class B?", "36", ["21", "51", "15"], "51 − 15 = <b>36</b>."),
        T(head + "Which score looks like an outlier?", "51 in Class B", ["22 in Class A", "15 in Class B", "47 in Class A"], "51 is far above the other Class B scores: <b>51 in Class B</b>."),
    ]
    sym = [31, 33, 35, 41, 42, 44, 45, 46, 47, 48, 52, 53, 55, 58, 61, 64]
    gsym = fig(plot_svg(sym))
    its.append(T(gsym + "How would you describe the shape of this distribution?", "Roughly symmetrical, with most values in the middle",
                 ["Positively skewed, with a long tail of high values", "Negatively skewed, with a long tail of low values", "Every value appears once with no pattern"],
                 "The rows are short, long, short, so it is <b>roughly symmetrical</b>."))
    sk = [12, 13, 13, 14, 15, 16, 16, 17, 18, 21, 22, 24, 27, 33, 45]
    gsk = fig(plot_svg(sk))
    its.append(T(gsk + "How would you describe the shape of this distribution?", "Positively skewed, with a tail of high values",
                 ["Roughly symmetrical", "Negatively skewed, with a tail of low values", "It has two peaks"],
                 "Most values are low, with a few much higher: <b>positively skewed</b>."))
    its.append(T(gsk + "Which measure of centre best describes a typical value here?", "The median, because the high values pull the mean up",
                 ["The mean, because it uses every value", "The range", "The largest value"], "The tail of high values (and 45) pulls the mean up, so <b>the median</b> is more typical."))
    data = [
        ("In the key 3 | 6 = 36, what does the 3 represent?", "The tens digit (the stem)", ["The ones digit (the leaf)", "The number of values", "The median"], "The stem is <b>the tens digit</b> and the leaf is the ones digit."),
        ("Why should the leaves in each row be written in order?", "So you can read the median and other values easily", ["Because the key says so", "So the diagram looks wider", "It does not matter at all"],
         "An <b>ordered</b> plot lets you count to the middle and read the smallest and largest values."),
        ("A stem-and-leaf diagram has stems 1 to 5 and 18 leaves altogether. How many values does it show?", "18", ["5", "23", "13"], "Every leaf is one value: <b>18</b>."),
        ("What is one advantage of a stem-and-leaf diagram over a bar graph?", "You can still see every actual data value", ["It always uses less space", "It shows percentages", "It can show categories like colours"],
         "A stem-and-leaf diagram keeps the original numbers, so <b>you can still see every value</b>."),
        ("In a diagram with key 2 | 3 = 2.3, what value does 4 | 7 show?", "4.7", ["47", "0.47", "470"], "With this key the stem is the ones digit and the leaf is tenths: <b>4.7</b>."),
        ("A row reads 6 | 0 0 4 9. Which values are in this row?", "60, 60, 64 and 69", ["60, 4 and 9", "6, 0, 4 and 9", "600, 649"], "Each leaf joins the stem: <b>60, 60, 64 and 69</b>."),
        ("Which data set is best shown in a stem-and-leaf diagram?", "The ages of 25 people at a party", ["Favourite colours of 25 people", "The type of pet each student owns", "The country each tourist came from"],
         "Stem-and-leaf diagrams are for <b>numerical</b> data such as ages."),
        ("A diagram has rows 1 | 5 8, 2 | 0 3 3 7, 3 | 1 4. What is the mode?", "23", ["3", "2", "20"], "The value 23 appears twice: <b>23</b>."),
        ("A diagram has rows 1 | 5 8, 2 | 0 3 3 7, 3 | 1 4. What is the median?", "23", ["20", "25", "27"], "8 values: halfway between the 4th (23) and 5th (23) is <b>23</b>."),
        ("A diagram has rows 1 | 5 8, 2 | 0 3 3 7, 3 | 1 4. What is the range?", "19", ["4", "34", "16"], "34 − 15 = <b>19</b>."),
        ("Removing a very high outlier from a data set would…", "lower the mean", ["raise the mean", "not change the mean", "change the mode"], "A high outlier pulls the mean up, so removing it <b>lowers the mean</b>."),
        ("Two back-to-back diagrams have the same median, but one has a much larger range. What does this tell you?", "Its data is more spread out", ["Its data is higher", "Its data is lower", "It has more values"],
         "A larger range means <b>the data is more spread out</b>."),
    ]
    its += [T(q, a_[0].upper() + a_[1:], [w[0].upper() + w[1:] for w in ws], e) for q, a_, ws, e in data]
    return its


def body():
    return lesson(
        "<p>A <b>stem-and-leaf diagram</b> shows every value of numerical data. The <b>stem</b> is usually the tens digit and the "
        "<b>leaf</b> is the ones digit, so 3 | 6 means 36. Always include a <b>key</b>, and write the leaves in order.</p>"
        "<p>From an ordered diagram you can read the smallest and largest values, count to the median, spot the mode and outliers, "
        "and see the <b>shape</b>: symmetrical, or skewed with a long tail.</p>"
        + fig(plot_svg([12, 15, 18, 21, 23, 23, 27, 30, 34], label="example stem-and-leaf diagram")),
        [("How many values are in the diagram above?", ["Count the leaves."], "9"),
         ("What is the median?", ["9 values: the 5th value."], "23"),
         ("What is the range?", ["34 − 12."], "22")],
        ["Reading a leaf on its own: in 2 | 4 the value is 24, not 4.",
         "Counting the stems instead of the leaves.",
         "Finding the median without the leaves in order.",
         "Leaving out repeated values: 23 and 23 need two leaves."])


def main():
    sets = [S("Reading a stem-and-leaf diagram", collect(one_read, 20, R)),
            S("Median and mode from a diagram", collect(one_medmode, 20, R)),
            S("Range and mean from a diagram", collect(one_rangemean, 20, R)),
            S("Building a stem-and-leaf diagram", collect(one_build, 20, R)),
            S("Shape, outliers and comparing", problems())]
    make(2, "stem-and-leaf-diagrams", 15, "S1",
         "Stem-and-Leaf Diagrams: Reading, Median, Range and Shape",
         "Secondary 2 Stem-and-Leaf Diagram Worksheets: Reading Diagrams, Median, Mode, Range and Back-to-Back Diagrams (Free, Answer Key)",
         "Stem-and-leaf diagrams",
         "analysis and interpretation of dot diagrams, histograms and stem-and-leaf diagrams; mean, mode and median as measures of central tendency for a set of data",
         "Free Secondary 2 maths worksheets on stem-and-leaf diagrams: reading diagrams, median, "
         "mode, range and mean, building diagrams, shape, outliers and back-to-back diagrams. 100 questions with an answer key.",
         "Stem = tens digit, leaf = ones digit: 3 | 6 means 36.",
         "Count the leaves to find how many values there are, then count to the middle for the median.",
         body(),
         [("How do you read a stem-and-leaf diagram?", "Join each leaf to its stem using the key. If the key says 3 | 6 = 36, then a leaf of 2 on stem 4 means 42."),
          ("How do you find the median from a stem-and-leaf diagram?", "Count the leaves to find how many values there are, then count from the start to the middle value."),
          ("What is a back-to-back stem-and-leaf diagram?", "Two data sets share the same stems: one set's leaves go to the right and the other's to the left, so they are easy to compare."),
          ("What does skewed mean?", "Most values are bunched at one end with a long tail at the other. A tail of high values is positively skewed.")],
         sets, R)


if __name__ == "__main__":
    main()
