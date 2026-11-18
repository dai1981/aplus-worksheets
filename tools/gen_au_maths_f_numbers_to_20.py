# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Numbers to 20 (Australian Curriculum v9.0, AC9MFN01)
  python3 tools/gen_au_maths_f_numbers_to_20.py
Count and name numbers 0 to 10 (zero is an empty plate), numbers 11 to 20 on two ten-frames, the number
before, after and between, ordering numbers, and counting in everyday stories.
Wrong answers come from real mistakes: counting one thing twice or missing one, reading 12 as 21, mixing up
before and after, and thinking zero is not a number.
"""
import random
from k_pics import row_svg, tenframe_svg, plate_svg, cards_svg, number_line_svg, scatter_svg, name, KINDS
from f_common import Kids, mcq, finish, make, fig, figure, mistakes

R = random.Random(99101)


# ------------------------------------------------------------ set 1: how many? (0 to 10)
def set_count(rnd):
    its = []
    plan = [(3, "apple", "row"), (5, "star", "row"), (0, "apple", "plate"), (4, "duck", "scatter"), (7, "ball", "row"),
            (2, "fish", "plate"), (6, "flower", "scatter"), (8, "heart", "row"), (1, "cup", "plate"), (9, "button", "row"),
            (10, "bug", "row"), (5, "duck", "scatter"), (0, "fish", "plate"), (7, "star", "scatter"), (6, "cup", "row"),
            (3, "bug", "plate"), (8, "apple", "scatter"), (4, "heart", "plate"), (9, "flower", "scatter"), (10, "ball", "row")]
    for i, (n, k, how) in enumerate(plan):
        svg = row_svg(n, k) if how == "row" else plate_svg(n, k) if how == "plate" else scatter_svg(n, k, 500 + i)
        q = fig(svg) + ("How many %s are on the plate?" % name(k) if how == "plate" else "How many %s?" % name(k))
        if n == 0:
            e = "The plate is empty. There are no %s. We write <b>0</b> (zero)." % name(k)
            its.append(mcq(q, 0, [1, 10, "We cannot count them"], e, allow_zero=True))
            continue
        e = "Touch and count each one once: %s. The last number you say is how many: <b>%d</b>." % (", ".join(str(j) for j in range(1, n + 1)), n)
        its.append(mcq(q, n, [n + 1, n - 1, n + 2, n - 2, n + 3], e))
    return {"title": "How many? Numbers 0 to 10", "items": its}


# ------------------------------------------------------------ set 2: numbers 11 to 20 on ten-frames
def set_teens(rnd):
    its = []
    for i, n in enumerate([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 12, 15, 17, 13, 19, 16, 14, 18, 11, 20]):
        if i < 10:
            q = fig(tenframe_svg(n)) + "How many dots are there?"
            rev = int(str(n)[::-1]) if n % 10 else None
            e = "The first ten-frame is full: that is 10. The second has %d more. 10 and %d make <b>%d</b>." % (n - 10, n - 10, n)
            its.append(mcq(q, n, [rev if rev and rev <= 21 else n + 2, n - 10, n + 1, n - 1], e))
        else:
            words = {11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen",
                     18: "eighteen", 19: "nineteen", 20: "twenty"}
            if i % 2:
                q = "Which number is <b>%s</b>?" % words[n]
                e = "%s is 10 and %d more: <b>%d</b>." % (words[n].capitalize(), n - 10, n)
                rev = int(str(n)[::-1]) if n % 10 else 0
                wrong = [rev if 0 < rev <= 21 else n + 2, n + 1, n - 1, n - 10]
                its.append(mcq(q, n, wrong, e, allow_zero=False))
            else:
                q = fig(tenframe_svg(n)) + "Which word tells how many dots?"
                e = "10 and %d make %d. We say <b>%s</b>." % (n - 10, n, words[n])
                its.append(mcq(q, words[n], [words.get(n + 1, "nineteen"), words.get(n - 1, "ten"), words.get(n - 10 + 10 + 2, "seventeen")], e))
    return {"title": "Numbers 11 to 20", "items": its}


# ------------------------------------------------------------ set 3: before, after and between
def set_order(rnd):
    its = []
    plan = [("after", 4), ("after", 9), ("before", 6), ("before", 11), ("between", 7), ("after", 13), ("before", 15),
            ("between", 12), ("after", 17), ("before", 20), ("between", 16), ("after", 0), ("before", 1), ("between", 18),
            ("after", 19), ("before", 10), ("between", 3), ("after", 11), ("before", 14), ("between", 9)]
    for kind, n in plan:
        if kind == "after":
            q = fig(cards_svg([str(n), "?"])) + "Which number comes just <b>after</b> %d?" % n
            ans = n + 1
            e = "Count on one: %d, <b>%d</b>." % (n, ans)
            its.append(mcq(q, ans, [n - 1, n + 2, n, n + 3], e, allow_zero=True))
        elif kind == "before":
            q = fig(cards_svg(["?", str(n)])) + "Which number comes just <b>before</b> %d?" % n
            ans = n - 1
            e = "Count back one: %d, <b>%d</b>." % (n, ans)
            its.append(mcq(q, ans, [n + 1, n - 2, n, n + 2], e, allow_zero=True))
        else:
            q = fig(cards_svg([str(n - 1), "?", str(n + 1)])) + "Which number goes in the middle?"
            e = "Count: %d, <b>%d</b>, %d." % (n - 1, n, n + 1)
            its.append(mcq(q, n, [n + 2, n - 2, n + 1], e, allow_zero=True))
    return {"title": "Before, after and between", "items": its}


# ------------------------------------------------------------ set 4: ordering numbers
def set_compare(rnd):
    its = []
    pairs = [(3, 5), (8, 6), (12, 9), (15, 18), (20, 17), (11, 14), (0, 2), (19, 16), (7, 13), (10, 4)]
    for i, (a, b) in enumerate(pairs):
        if i % 2 == 0:
            q = fig(cards_svg([str(a), str(b)])) + "Which number is <b>bigger</b>?"
            ans, oth = max(a, b), min(a, b)
            e = "When we count, %d comes after %d. <b>%d</b> is bigger." % (ans, oth, ans)
        else:
            q = fig(cards_svg([str(a), str(b)])) + "Which number is <b>smaller</b>?"
            ans, oth = min(a, b), max(a, b)
            e = "When we count, %d comes before %d. <b>%d</b> is smaller." % (ans, oth, ans)
        its.append(mcq(q, ans, [oth, "They are the same", ans + 10 if ans + 10 <= 20 and ans + 10 != oth else (ans + 1 if ans + 1 != oth else ans + 2)], e, allow_zero=True))
    sets3 = [(4, 9, 2), (11, 7, 15), (18, 13, 20), (6, 16, 10), (3, 0, 8), (14, 12, 19), (5, 17, 1), (9, 20, 11), (2, 10, 7), (13, 6, 18)]
    for i, t in enumerate(sets3):
        srt = sorted(t)
        if i % 2 == 0:
            q = fig(cards_svg([str(x) for x in t])) + "Put the numbers in order, <b>smallest first</b>."
            ans = ", ".join(str(x) for x in srt)
            wr = [", ".join(str(x) for x in srt[::-1]), ", ".join(str(x) for x in t), ", ".join(str(x) for x in [srt[1], srt[0], srt[2]]), ", ".join(str(x) for x in [srt[0], srt[2], srt[1]])]
            e = "Start with the smallest number: <b>%s</b>." % ans
        else:
            q = fig(cards_svg([str(x) for x in t])) + "Put the numbers in order, <b>biggest first</b>."
            ans = ", ".join(str(x) for x in srt[::-1])
            wr = [", ".join(str(x) for x in srt), ", ".join(str(x) for x in t), ", ".join(str(x) for x in [srt[1], srt[2], srt[0]]), ", ".join(str(x) for x in [srt[2], srt[0], srt[1]])]
            e = "Start with the biggest number: <b>%s</b>." % ans
        its.append(mcq(q, ans, wr, e, allow_zero=True))
    o = its
    order = [o[0], o[1], o[10], o[2], o[11], o[3], o[12], o[4], o[13], o[5], o[14], o[6], o[15], o[7], o[16], o[8], o[17], o[9], o[18], o[19]]
    return {"title": "Bigger, smaller and in order", "items": order}


# ------------------------------------------------------------ set 5: numbers in stories
def set_story(rnd):
    K = Kids(rnd)
    its = []
    for i in range(20):
        k = K.next()
        kind = i % 5
        if kind == 0:
            n = [6, 9, 12, 15][i // 5]
            q = "%s counts %d steps up the slide. Then %s climbs one more step. How many steps is that?" % (k["n"], n, k["he"])
            its.append(mcq(q, n + 1, [n, n + 2, n - 1], "One more than %d is <b>%d</b>." % (n, n + 1)))
        elif kind == 1:
            seq = [[3, 4, 5], [10, 11, 12], [15, 16, 17], [7, 8, 9]][i // 5]
            q = fig(number_line_svg(seq[0] - 1, seq[-1] + 2, {v: str(v) for v in seq} | {seq[-1] + 1: "?"})) + "%s counts: %s. What does %s say next?" % (k["n"], ", ".join(map(str, seq)), k["he"])
            ans = seq[-1] + 1
            its.append(mcq(q, ans, [seq[-1], ans + 1, seq[0]], "Counting goes up by one each time: %s, <b>%d</b>." % (", ".join(map(str, seq)), ans)))
        elif kind == 2:
            n = [14, 12, 17, 20][i // 5]
            q = "There are %d children in %s's class. Which card shows %d?" % (n, k["n"], n)
            rev = int(str(n)[::-1]) if n % 10 else 2
            rev = rev if rev <= 21 else n + 2
            its.append(mcq(q, "%d" % n, ["%d" % rev if rev != n else "12", "%d" % (n - 10), "%d" % (n + 1)], "%d is 1 ten and %d more. It is written <b>%d</b>, with the 1 first." % (n, n - 10, n) if n < 20 else "Twenty is 2 tens. It is written <b>20</b>."))
        elif kind == 3:
            n = [5, 8, 3, 10][i // 5]
            kk = ["apple", "ball", "duck", "star"][i // 5]
            q = fig(row_svg(n, kk)) + "%s puts the %s in a line. How many %s are there?" % (k["n"], name(kk), name(kk))
            its.append(mcq(q, n, [n + 1, n - 1, n + 2], "Count each one once. The last number you say is <b>%d</b>." % n))
        else:
            n = [0, 0, 0, 0][i // 5]
            what = [("biscuits", "the jar is empty"), ("birds", "all the birds fly away"), ("cars", "the car park is empty"), ("balls", "the box is empty")][i // 5]
            q = "%s looks for %s, but %s. How many %s are there?" % (k["n"], what[0], what[1], what[0])
            its.append(mcq(q, 0, [1, 10, "No number"], "There are none. <b>0</b> (zero) is the number for none.", allow_zero=True))
    return {"title": "Numbers in stories", "items": its}


def body():
    return (
        "<h2>Count each thing once</h2>"
        "<p>Touch each thing and say one number. The <b>last number</b> you say tells <b>how many</b>.</p>"
        + figure(row_svg(6, "apple"), "1, 2, 3, 4, 5, 6. There are 6 apples.")
        + "<h2>Zero means none</h2><p>An empty plate has <b>0</b> things on it. Zero is a number too.</p>"
        "<h2>Numbers 11 to 20</h2><p>A full ten-frame is 10. Teen numbers are 10 and some more.</p>"
        + figure(tenframe_svg(14), "10 and 4 make 14.")
        + "<h2>Before and after</h2><p>Count on one to find the number <b>after</b>. Count back one to find the number <b>before</b>. Numbers that come later when we count are <b>bigger</b>.</p>"
        + figure(number_line_svg(0, 10, sp=34), "8 comes after 7. 8 is bigger than 7.")
        + mistakes([["Counting a thing twice or missing one", "Touch or move each thing as you count"],
                    ["Writing 21 for twelve", "Teen numbers start with the 1: 12 is 10 and 2"],
                    ["Thinking zero is not a number", "0 is the number for none"],
                    ["Mixing up before and after", "Before: count back. After: count on"]]))


FAQ = [("What numbers do Foundation students learn in maths?",
        "In the Australian Curriculum (AC9MFN01), Foundation students name, represent and order numbers from 0 to at least 20. They count things, read and write numerals and say which number comes before or after."),
       ("Is Foundation the same as Prep or Kindergarten?",
        "Yes. Foundation is the first year of school. It is called Kindergarten in NSW and the ACT, Prep in Queensland, Victoria and Tasmania, Pre-primary in WA, Reception in SA and Transition in the NT."),
       ("Why does my child write 21 for twelve?",
        "We say the teen numbers backwards (four-teen sounds like 4 then 10). Show 12 on two ten-frames: one full ten and 2 more, so the 1 is written first."),
       ("How can I practise counting at home?",
        "Count steps, pegs, grapes or toy cars, touching each one. Ask: How many? What number comes next? What comes before?")]


def build():
    sets = [set_count(R), set_teens(R), set_order(R), set_compare(R), set_story(R)]
    finish(sets, R, max_num=21, extra_ok=(22,))
    make("numbers-to-20", 1, "AC9MFN01", "Number",
         "Numbers to 20: Count, Name and Order",
         "Foundation Numbers to 20 Worksheets: Counting, Ten-Frames and Ordering (Free, with Answers)",
         "Numbers to 20",
         "Name, represent and order numbers including zero to at least 20, using physical and virtual materials and numerals.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on numbers to 20, matched to the Australian Curriculum (AC9MFN01): count things, zero, teen numbers on ten-frames, before and after, and ordering. 100 picture questions with answers.",
         "Count each thing once. The last number you say is how many.",
         "Zero means none. A full ten-frame is 10, so 14 is 10 and 4 more.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
