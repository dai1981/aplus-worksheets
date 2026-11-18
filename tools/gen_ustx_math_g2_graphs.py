# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Pictographs and Bar Graphs (TEKS 2.10A, 2.10B, 2.10C, 2.10D)
  python3 tools/gen_ustx_math_g2_graphs.py
Reading picture graphs and tally charts, reading bar graphs, in all, how many more and how many fewer, and making
graphs (the US Grade 2 makers with Texas names), plus drawing conclusions (own maker).
Wrong answers come from real mistakes: counting the grid lines instead of reading the bar, misreading the key, and
adding when the question asks how many more.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_graphs as gr
adopt(gr)
import random
gr.P = gr.People(random.Random(69219))
tx_common.GRADE = "grade-2"

INK = "#1f2937"


def no_plot(it):
    return "line plot" not in it["q"]


CATS = [("Favorite fruit", ["Apples", "Bananas", "Grapes", "Peaches"]), ("Favorite pet", ["Dogs", "Cats", "Fish", "Birds"]), ("Favorite recess game", ["Tag", "Swings", "Slide", "Ball"]),
        ("Favorite season", ["Spring", "Summer", "Fall", "Winter"])]


def bars(title, cats, vals):
    top = max(vals) + 2
    W, H, x0, y0 = 320, 170, 40, 14
    ph = H - 40
    s = ["<svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='bar graph: %s'>" % (W, H + 20, W, title)]
    for t in range(0, top + 1):
        y = y0 + ph - ph * t / float(top)
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s'/>" % (x0, y, W - 10, y, "#9ca3af" if t % 2 == 0 else "#e5e7eb"))
        if t % 2 == 0:
            s.append("<text x='%d' y='%.1f' font-size='12' text-anchor='end' fill='%s'>%d</text>" % (x0 - 5, y + 4, INK, t))
    bw = (W - 10 - x0) / 4.0
    for i, (c, v) in enumerate(zip(cats, vals)):
        h = ph * v / float(top)
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#60a5fa' stroke='%s'/>" % (x0 + i * bw + bw * 0.2, y0 + ph - h, bw * 0.6, h, INK))
        s.append("<text x='%.1f' y='%d' font-size='12' text-anchor='middle' fill='%s'>%s</text>" % (x0 + i * bw + bw / 2, y0 + ph + 16, INK, c))
    s.append("<text x='%d' y='%d' font-size='13' text-anchor='middle' fill='%s'>%s</text></svg>" % (W // 2 + 15, H + 14, INK, title))
    return fig("".join(s))


def one_conclude(r):
    title, cats = r.choice(CATS)
    vals = r.sample(range(2, 15), 4)
    pic = bars(title, cats, vals)
    hi = max(range(4), key=lambda i: vals[i])
    lo = min(range(4), key=lambda i: vals[i])
    kind = r.choice(["most", "least", "true", "predict"])
    if kind == "most":
        return mcq(pic + "Which choice is the most popular?", cats[hi], [c for i, c in enumerate(cats) if i != hi], "The tallest bar is <b>%s</b> (%d)." % (cats[hi], vals[hi]))
    if kind == "least":
        return mcq(pic + "Which choice is the least popular?", cats[lo], [c for i, c in enumerate(cats) if i != lo], "The shortest bar is <b>%s</b> (%d)." % (cats[lo], vals[lo]))
    if kind == "true":
        a, b = r.sample(range(4), 2)
        big, small = (a, b) if vals[a] > vals[b] else (b, a)
        st = "%s got %d more votes than %s."
        right = st % (cats[big], vals[big] - vals[small], cats[small])
        return mcq(pic + "Which statement is true?", right, [st % (cats[small], vals[big] - vals[small], cats[big]), st % (cats[big], vals[big] + vals[small], cats[small]), "All the bars are the same."],
                   "%d − %d = %d, so <b>%s</b>" % (vals[big], vals[small], vals[big] - vals[small], right))
    return mcq(pic + "The class asks the same question to a new group of children. Which choice will most likely be the most popular again?", cats[hi], [c for i, c in enumerate(cats) if i != hi],
               "%s was the most popular here, so it is a good prediction: <b>%s</b>." % (cats[hi], cats[hi]))


def build():
    sets, R = build_sets([
        ("Read picture graphs and tally charts", [("run", gr.set_picture, ("rnd", gr.Picker), 20)]),
        ("Read bar graphs", [("run", gr.set_bar, ("rnd", gr.Picker), 20)]),
        ("In all, how many more, how many fewer", [("run", gr.set_compare, ("rnd", gr.Picker), 20)]),
        ("Make a graph", [("run", gr.set_make, ("rnd", gr.Picker, gr.LPicker, gr.People), 15, no_plot), ("collect", one_conclude, 5)]),
        ("Draw conclusions and predict", [("collect", one_conclude, 20)]),
    ], 69219)
    finish(sets, R)
    body = lesson('<ul><li>In a <b>pictograph</b>, count the pictures. Check the key if one picture stands for more than 1.</li><li>In a <b>bar graph</b>, read the number at the top of each bar.</li><li>How many more or fewer: subtract. In all: add.</li><li>Use the graph to draw conclusions, like which choice is the most popular.</li></ul>',
        [example("Bar graph: Dogs 9, Cats 5", ["9 − 5"], "4 more dogs")],
        [['Counting grid lines instead of reading the bar', 'Read the number where the bar ends.'], ['Misreading the key', 'If each picture is 2, multiply.'], ['Adding when asked how many more', 'How many more means subtract.']])
    faq = [('What does TEKS 2.10A ask?', 'Explain that the length of a bar in a bar graph or the number of pictures in a pictograph represents the number of data points for a given category.'), ('What does TEKS 2.10B ask?', 'Organize a collection of data with up to four categories using pictographs and bar graphs with intervals of one or more.'), ('What does TEKS 2.10C ask?', 'Write and solve one-step word problems involving addition or subtraction using data represented within pictographs and bar graphs with intervals of one.'), ('What does TEKS 2.10D ask?', 'Draw conclusions and make predictions from information in a graph.')]
    make('pictographs-and-bar-graphs', 19, 'Data Analysis', '2.10A, 2.10B, 2.10C, 2.10D',
         '2.10A explain that the length of a bar in a bar graph or the number of pictures in a pictograph represents the number of data points for a given category; 2.10B organize a collection of data with up to four categories using pictographs and bar graphs with intervals of one or more; 2.10C write and solve one-step word problems involving addition or subtraction using data represented within pictographs and bar graphs with intervals of one; 2.10D draw conclusions and make predictions from information in a graph',
         'Pictographs and Bar Graphs', 'Pictographs and Bar Graphs',
         'Free Grade 2 graph worksheets for Texas TEKS 2.10: read pictographs, tally charts and bar graphs, compare data, make graphs and draw conclusions. 100 questions with answers.',
         'Read the bar or count the pictures; check the key.', 'Dogs 9, Cats 5: 4 more dogs.',
         body, faq, sets, seo_title='Grade 2 Pictographs and Bar Graphs Worksheets (TEKS 2.10)')


if __name__ == "__main__":
    build()
