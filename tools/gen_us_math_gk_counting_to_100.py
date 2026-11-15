# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Counting to 100 (K.CC.A.1, K.CC.A.2)
  python3 tools/gen_us_math_gk_counting_to_100.py
Count on by 1s to 20, then to 100 from any number (also across a new ten); count by 10s with
cards, ten rods and the hundred chart; find missing numbers on the hundred chart; short stories.
"""
import random, re
from ws_common import balance, People, table, write_unit, fig
from k_pics import cards_svg, number_line_svg, chart_svg, rods_svg, tenframe_svg

UPDATED = "2026-11-16"


def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c in ("0", "") or c.startswith("-"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def lst(xs):
    return ", ".join(str(x) for x in xs)


def rev(n):
    s = str(n)
    return int(s[::-1]) if len(s) == 2 and s[1] != "0" and s[0] != s[1] else None


def next_wrong(last):
    """Wrong answers for 'what comes next after last' (counting by 1s)."""
    a = last + 1
    w = []
    if a % 10 == 0 and a > 10:
        w += [a - 10, a + 1]               # went back to the start of the ten (29, 20) / skipped
    w += [a + 1, last, last - 1, rev(a), a + 10]
    return w


def next_e(last):
    a = last + 1
    if a == 100:
        return "After 99 comes <b>100</b>. 9 tens and 1 more ten make one hundred."
    if a % 10 == 0 and a > 10:
        return ("After %d comes <b>%d</b>. After 9 in the ones place, start a new ten: %d, %d."
                % (last, a, last, a))
    if a == 10:
        return "After 9 comes <b>10</b>."
    return "Count on by 1s. After %d comes <b>%d</b>." % (last, a)


# ============================================================ set 1: count on to 20
def set_to_20(rnd, P):
    its = []
    for start in [1, 3, 5, 2, 6, 7, 8, 11, 13, 16, 17]:
        xs = [start, start + 1, start + 2]
        q = fig(cards_svg([str(x) for x in xs] + ["?"])) + "Count on. What number comes next?"
        its.append(mcq(q, xs[-1] + 1, next_wrong(xs[-1]), next_e(xs[-1])))
    for a, b in [(4, 6), (9, 11), (12, 14), (15, 17), (18, 20)]:
        q = fig(cards_svg([str(a), "?", str(b)])) + "What number is missing?"
        m = a + 1
        e = "The missing number comes after %d and before %d. After %d comes <b>%d</b>." % (a, b, a, m)
        its.append(mcq(q, m, [m + 1, m - 1 if m - 1 != a else a - 1, rev(m), b + 1], e))
    for lo, hi, at in [(0, 10, 7), (10, 20, 13), (10, 20, 19), (5, 15, 11)]:
        marks = {lo: str(lo), hi: str(hi), at: "?"}
        q = fig(number_line_svg(lo, hi, marks, sp=34)) + "What number goes at the ?"
        e = "Count on from %d: %s. The ? is <b>%d</b>." % (lo, lst(range(lo + 1, at + 1)), at)
        its.append(mcq(q, at, [at + 1, at - 1, rev(at), at + 2], e))
    o = its
    order = [o[0], o[1], o[2], o[11], o[3], o[16], o[4], o[5], o[12], o[6],
             o[17], o[7], o[13], o[8], o[18], o[9], o[14], o[10], o[19], o[15]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Count on to 20", "items": order}


# ============================================================ set 2: count by 10s
def set_tens(rnd, P):
    its = []
    for xs in [[10, 20, 30], [20, 30, 40], [40, 50, 60], [60, 70, 80], [70, 80, 90]]:
        a = xs[-1] + 10
        q = fig(cards_svg([str(x) for x in xs] + ["?"], w=56)) + "Count by 10s. What number comes next?"
        e = "Count by 10s: %s, <b>%d</b>. Only the tens digit goes up by 1." % (lst(xs), a)
        if a == 100:
            e = "Count by 10s: %s, <b>100</b>. 10 tens make one hundred." % lst(xs)
        its.append(mcq(q, a, [xs[-1] + 1, a + 10, a // 10, xs[-1]], e))
    for xs, mi in [([10, 20, 30, 40], 2), ([30, 40, 50, 60], 1), ([50, 60, 70, 80], 2), ([70, 80, 90, 100], 2)]:
        ans = xs[mi]
        shown = [str(x) if i != mi else "?" for i, x in enumerate(xs)]
        q = fig(cards_svg(shown, w=56)) + "Count by 10s. What number is missing?"
        e = "Count by 10s: %s. The missing number is <b>%d</b>." % (lst(xs), ans)
        its.append(mcq(q, ans, [xs[mi - 1] + 1, ans + 10 if ans + 10 not in xs else ans + 20, ans // 10, ans + 5], e))
    for t in [2, 3, 4, 5, 6, 7, 8, 10]:
        q = fig(rods_svg(t)) + "Each rod has 10 cubes. Count by 10s. How many cubes are there?"
        e = "Count the rods by 10s: %s. There are <b>%d</b> cubes." % (lst(range(10, 10 * t + 1, 10)), 10 * t)
        its.append(mcq(q, 10 * t, [t, 10 * t + 10, 10 * t - 10, t + 10], e))
    for tl, rows, tr in [(10, 4, 3), (40, 5, 3)]:
        q = fig(chart_svg(tl, rows, 1, target=(tr, 0))) + "This is the 10s column of a hundred chart. What number goes at the ?"
        ans = tl + 10 * tr
        e = "Count down the column by 10s: %s. The ? is <b>%d</b>." % (lst(range(tl, ans + 1, 10)), ans)
        its.append(mcq(q, ans, [ans - 10 + 1, ans + 10, ans // 10, ans - 10], e))
    its.append(mcq("Count by 10s: 70, 80, 90. What comes after 90?", 100, [91, 1000, 110],
                   "Count by 10s: 70, 80, 90, <b>100</b>. 10 tens make one hundred."))
    o = its
    order = [o[0], o[9], o[10], o[1], o[5], o[11], o[2], o[17], o[12], o[6],
             o[13], o[3], o[7], o[14], o[18], o[4], o[15], o[8], o[16], o[19]]
    assert len(o) == 20 and len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Count by 10s", "items": order}


# ============================================================ set 3: count on from any number
def set_any(rnd, P):
    its = []
    for start in [24, 33, 45, 51, 62, 76, 84, 27, 37, 56, 67, 87, 97]:
        xs = [start, start + 1, start + 2]
        q = fig(cards_svg([str(x) for x in xs] + ["?"])) + "Count on. What number comes next?"
        its.append(mcq(q, xs[-1] + 1, next_wrong(xs[-1]), next_e(xs[-1])))
    for a in [41, 58, 72, 89]:
        q = fig(cards_svg([str(a), "?", str(a + 2)])) + "What number is missing?"
        m = a + 1
        if m % 10 == 0:
            e = "After %d comes <b>%d</b>. After 9 in the ones place, start a new ten." % (a, m)
            w = [m - 10, m + 1, a - 1, m + 10]
        else:
            e = "The missing number comes after %d and before %d. After %d comes <b>%d</b>." % (a, a + 2, a, m)
            w = [a + 3, a - 1, rev(m), m + 10]
        its.append(mcq(q, m, w, e))
    for lo, at in [(35, 39), (66, 71), (94, 100)]:
        marks = {lo: str(lo), at: "?"}
        q = fig(number_line_svg(lo, lo + 6, marks, sp=40)) + "Count on by 1s. What number goes at the ?"
        e = "Count on from %d: %s. The ? is <b>%d</b>." % (lo, lst(range(lo + 1, at + 1)), at)
        w = [at + 1, at - 1, (at - 10) if at % 10 == 0 else rev(at), at + 10]
        its.append(mcq(q, at, w, e))
    o = its
    order = [o[0], o[1], o[13], o[2], o[17], o[3], o[14], o[4], o[5], o[18],
             o[6], o[7], o[15], o[8], o[9], o[16], o[10], o[11], o[19], o[12]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Count on from any number", "items": order}


# ============================================================ set 4: hundred chart
def set_chart(rnd, P):
    Q = "This is part of a hundred chart. What number goes in the box with the ?"
    pieces = [
        # tl, rows, cols, target (r, c), hide, wrong
        (1, 1, 6, (0, 3), set(), [5, 3, 40]),
        (11, 1, 6, (0, 4), set(), [16, 14, 51]),
        (21, 2, 5, (0, 2), set(), [24, 22, 32]),
        (14, 2, 5, (1, 3), set(), [28, 26, 72]),
        (32, 2, 5, (1, 1), set(), [44, 42, 34]),
        (5, 2, 6, (0, 5), set(), [11, 1, 9]),
        (45, 2, 5, (1, 4), set(), [50, 61, 59]),
        (51, 2, 5, (0, 4), {(0, 3)}, [54, 56, 65]),
        (63, 2, 5, (1, 2), set(), [76, 74, 57]),
        (17, 2, 4, (0, 3), set(), [10, 21, 210]),
        (36, 2, 4, (1, 3), set(), [50, 94, 59]),
        (72, 2, 5, (1, 4), {(1, 3)}, [85, 87, 68]),
        (85, 2, 5, (0, 3), set(), [89, 87, 98]),
        (66, 2, 5, (0, 4), set(), [60, 71, 610]),
        (91, 1, 6, (0, 4), set(), [96, 94, 59]),
        (46, 2, 5, (1, 2), {(1, 1), (1, 3)}, [57, 59, 85]),
        (77, 2, 4, (1, 3), set(), [80, 91, 810]),
        (95, 1, 6, (0, 5), set(), [10, 91, 1000]),
    ]
    its = []
    for tl, rows, cols, tgt, hide, wrong in pieces:
        ans = tl + 10 * tgt[0] + tgt[1]
        r, c = tgt
        if c > 0 and (r, c - 1) not in hide:
            left = ans - 1
            if ans % 10 == 0:
                e = "The number just before the ? is %d. After %d comes <b>%d</b>. A row of the chart ends with a ten." % (left, left, ans)
            elif ans == 100:
                e = "After 99 comes <b>100</b>."
            else:
                e = "The number just before the ? is %d. Count on 1. The ? is <b>%d</b>." % (left, ans)
        else:
            e = "Count along the row: %s, <b>%d</b>." % (lst(range(tl + 10 * r, ans)), ans)
        if ans == 100:
            e = "The row goes 95, 96, 97, 98, 99. After 99 comes <b>100</b>."
        shown = {tl + 10 * rr + cc for rr in range(rows) for cc in range(cols) if (rr, cc) not in hide and (rr, cc) != tgt}
        wrong = [w for w in wrong if w not in shown]
        wrong += [ans + 1, ans - 1, ans + 2, ans + 10, rev(ans), ans - 10, ans + 3, ans + 4, ans + 20, ans + 11]
        wrong = [w for w in wrong if w is not None]
        wrong = [w for w in wrong if w not in shown]
        its.append(mcq(fig(chart_svg(tl, rows, cols, tgt, hide)) + Q, ans, wrong, e))
    its.append(mcq("On a hundred chart, which number comes just after 49?", 50, [40, 410, 59],
                   "After 49 comes <b>50</b>. After 9 in the ones place, start a new ten."))
    its.append(mcq("On a hundred chart, which number is the very last one?", 100, [99, 10, 1000],
                   "A hundred chart goes from 1 to <b>100</b>. 100 is the last number."))
    o = its
    order = [o[0], o[1], o[2], o[3], o[4], o[5], o[18], o[6], o[7], o[8],
             o[9], o[10], o[11], o[12], o[13], o[14], o[15], o[16], o[19], o[17]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Hundred chart", "items": order}


# ============================================================ set 5: stories
def set_stories(rnd, P):
    its = []

    def story(text, ans, wrong, e, pic=None):
        nm, he, his = P.next()
        d = dict(n=nm, he=he, He=he.capitalize(), his=his)
        if pic is None:
            m = re.search(r"\d+(?:, \d+)+", text)
            if m:
                pic = cards_svg(m.group(0).split(", ") + ["?"], w=56)
        its.append(mcq((fig(pic) if pic else "") + text.format(**d), ans, wrong, e.format(**d)))

    story("{n} counts the steps: 8, 9, 10. What step comes next?", 11, [12, 10, 9], "After 10 comes <b>11</b>.")
    story("{n} hops and counts: 15, 16, 17. What number does {he} say next?", 18, [19, 81, 16], "After 17 comes <b>18</b>.")
    story("Today is day 19 of school. What day of school is tomorrow?", 20,
          [21, 10, 18], "After 19 comes <b>20</b>. Tomorrow is day 20.")
    story("Each kid has 10 fingers. Count the fingers by 10s. How many fingers do 3 kids have?", 30, [3, 13, 40],
          "Count by 10s, 1 ten for each kid: 10, 20, <b>30</b>.")
    story("{n} counts the books on a shelf: 31, 32, 33. What comes next?", 34, [35, 43, 33],
          "After 33 comes <b>34</b>.")
    story("{n} is on page 39 of {his} book. {He} turns the page. What page comes next?", 40, [30, 41, 310],
          "After 39 comes <b>40</b>. After 9 in the ones place, start a new ten.")
    story("Each box has 10 crayons. {n} counts 4 boxes by 10s. How many crayons are there?", 40, [4, 14, 50],
          "Count by 10s: 10, 20, 30, <b>40</b>.")
    story("{n} counts cars: 46, 47, 48. What number comes next?", 49, [50, 94, 48], "After 48 comes <b>49</b>.")
    story("{n} counts by 10s to 50: 10, 20, 30, 40. What does {he} say last?", 50, [41, 60, 5],
          "Count by 10s: 10, 20, 30, 40, <b>50</b>.")
    story("{n} counts from 55 to 60: 55, 56, 57, 58, 59 … What comes next?", 60, [50, 61, 510],
          "After 59 comes <b>60</b>. After 9 in the ones place, start a new ten.")
    story("Each ten-frame is full. Count by 10s. How many dots are there?", 20, [2, 11, 30],
          "A full ten-frame has 10. Count by 10s: 10, <b>20</b>.", pic=tenframe_svg(20))
    story("{n} counts jumps with a rope: 63, 64, 65. What comes next?", 66, [67, 56, 65], "After 65 comes <b>66</b>.")
    story("Each stack has 10 blocks. How many blocks are in 6 stacks?", 60, [6, 16, 70],
          "Count by 10s: 10, 20, 30, 40, 50, <b>60</b>.", pic=rods_svg(6))
    story("{n} counts on from 70: 70, 71, 72. What comes next?", 73, [74, 37, 80], "After 72 comes <b>73</b>.")
    story("{n} counts beads: 78, 79. What comes next?", 80, [70, 81, 710],
          "After 79 comes <b>80</b>. After 9 in the ones place, start a new ten.")
    story("{n} counts by 10s: 50, 60, 70, 80. What comes next?", 90, [81, 100, 9],
          "Count by 10s: 50, 60, 70, 80, <b>90</b>.")
    story("{n} counts the stars on a chart: 85, 86, 87. What comes next?", 88, [89, 78, 98], "After 87 comes <b>88</b>.")
    story("Today is day 99 of school. Tomorrow is day … ?", 100, [90, 1000, 101],
          "After 99 comes <b>100</b>. Tomorrow is the 100th day of school.")
    story("{n} has 9 rods. Each rod has 10 cubes. How many cubes does {he} have?", 90, [9, 100, 80],
          "Count by 10s: 10, 20, 30, 40, 50, 60, 70, 80, <b>90</b>.", pic=rods_svg(9))
    story("{n} counts the cars in a long line: 91, 92, 93. What comes next?", 94, [95, 49, 93], "After 93 comes <b>94</b>.")
    return {"title": "Counting stories", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Count on by 1s</h2>"
        "<p>Each number is 1 more. You can start at any number and count on.</p>"
        "<figure class='sn-fig'>" + cards_svg(["5", "6", "7", "8"]) + "<figcaption>5, 6, 7, 8 …</figcaption></figure>"
        "<h2>A new ten</h2>"
        "<p>After 9 in the ones place, start a <b>new ten</b>.</p>"
        + table(["Count on", "Next"], [["27, 28, 29", "<b>30</b>"], ["57, 58, 59", "<b>60</b>"], ["97, 98, 99", "<b>100</b>"]]) +
        "<h2>Count by 10s</h2>"
        "<p>A rod has 10 cubes. Count the rods by 10s.</p>"
        "<figure class='sn-fig'>" + rods_svg(5) + "<figcaption>10, 20, 30, 40, 50. There are 50 cubes.</figcaption></figure>"
        "<h2>The hundred chart</h2>"
        "<p>Each row has 10 numbers. A row ends with a ten.</p>"
        "<figure class='sn-fig'>" + chart_svg(41, 2, 10) + "<figcaption>41 to 50, then 51 to 60.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Going back after 29: 29, 20", "Start a new ten: 29, 30"],
            ["Writing 210 after 29", "29, 30 (3 tens)"],
            ["Counting rods by 1s: 1, 2, 3", "Count rods by 10s: 10, 20, 30"],
            ["Skipping a number", "Say each number: 46, 47, 48"],
        ])
    )


FAQ = [
    {"q": "How high should a kindergartner count?",
     "a": "By the end of kindergarten, children count to 100 by ones and by tens. They also start at any number, like 47, and count on: 48, 49, 50."},
    {"q": "Why does my child say 29, 20 or 29, 210?",
     "a": "They know the pattern 1 to 9 but not what comes after 9. Show 29 on a hundred chart and point to the next row: after 9 ones comes a new ten, 30."},
    {"q": "How do I teach counting by 10s?",
     "a": "Use bundles of 10 straws, ten rods or fingers (10 for each person). Count the bundles: 10, 20, 30. Then look at the last column of a hundred chart."},
    {"q": "Does my child need to read and write numbers to 100?",
     "a": "Not yet. In kindergarten, children say the numbers to 100 and write numbers 0 to 20. Reading and writing larger numbers comes in Grade 1."},
]


def gen():
    rnd = random.Random(2002)
    P = People(rnd)
    sets = [set_to_20(rnd, P), set_tens(rnd, P), set_any(rnd, P), set_chart(rnd, P), set_stories(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        for it in s["items"]:
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    v = int(tok)
                    assert 1 <= v <= 110 or v in (210, 310, 410, 510, 610, 710, 810, 1000), c
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"][-80:]
            seen.add(key)
            it["q"] = it["q"].replace("<svg ", "<svg data-pf='lg' ")
    return {
        "slug": "counting-to-100", "sort": 2, "updated": UPDATED, "pdf_url": "",
        "title": "Counting to 100: Count by Ones and by Tens",
        "seo_title": "Kindergarten Counting to 100 Worksheets: Count by 1s and 10s, Hundred Chart",
        "short_title": "Counting to 100",
        "domain": "Counting and Cardinality",
        "standard_code": "K.CC.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/CC/A/1/",
        "standard_text": "Count to 100 by ones and by tens.",
        "meta_desc": "Free kindergarten counting to 100 worksheets: count on by 1s from any number, cross a new ten "
                     "(29, 30), count by 10s with ten rods, and find missing numbers on a hundred chart. "
                     "100 picture questions with an answer key.",
        "key_big": "Count on by 1s from any number. After 9 in the ones place, start a new ten: 29, 30.",
        "key_sub": "Count by 10s: 10, 20, 30 … 100. 10 tens make one hundred.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
