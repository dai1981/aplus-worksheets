# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Counting to 20 (K.CC.B.4, K.CC.B.5)
  python3 tools/gen_us_math_gk_counting_to_20.py
Count objects in a line, an array, a circle (to 20) and scattered (to 10); the last number tells
how many; 1 more is the next number; moving things does not change how many; count out a number.
Every answer and every picture is computed in code.
"""
import random, re
from ws_common import balance, People, table, write_unit, fig
from k_pics import (name, row_svg, array_svg, circle_svg, scatter_svg, tenframe_svg,
                    lettered_groups_svg, KINDS)

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


def lst(a, b):
    return ", ".join(str(i) for i in range(a, b + 1))


def rev(n):
    s = str(n)
    return int(s[::-1]) if len(s) == 2 and s[1] != "0" and s[0] != s[1] else None


# ------------------------------------------------------------ one picture + its explanation
def picture(n, kind, how, rnd):
    """Return (svg, explanation). how: row, scatter, circle, tenframe, rows10, array:RxC."""
    k = name(kind, n)
    if how == "row":
        assert n <= 12
        svg = row_svg(n, kind, per_row=max(n, 1), gap5=False)
        e = "Touch each one and count: %s. The last number you say tells how many. There %s <b>%d</b> %s." % (
            lst(1, n), "is" if n == 1 else "are", n, k)
    elif how == "row5":
        assert 6 <= n <= 10
        svg = row_svg(n, kind)
        e = ("There are 5 in the first group. Count on: %s. There are <b>%d</b> %s."
             % (lst(6, n), n, k))
    elif how == "scatter":
        assert n <= 10
        svg = scatter_svg(n, kind, seed=rnd.randint(1, 10 ** 6))
        e = ("Touch each one and count: %s. Mark each one as you count it, so you do not count it twice. "
             "There are <b>%d</b> %s." % (lst(1, n), n, k))
    elif how == "circle":
        svg = circle_svg(n, kind)
        e = ("Start at one %s and go around: %s. Stop when you get back to the start. "
             "Do not count the first one again. There are <b>%d</b> %s." % (name(kind, 1), lst(1, n), n, k))
    elif how == "tenframe":
        svg = tenframe_svg(n)
        if n <= 5:
            e = "Count the dots: %s. There are <b>%d</b> dots." % (lst(1, n), n)
        elif n < 10:
            e = "The top row is full. That is 5. Count on: %s. There are <b>%d</b> dots." % (lst(6, n), n)
        elif n == 10:
            e = "The ten-frame is full. A full ten-frame has <b>10</b> dots."
        elif n < 20:
            e = "The first ten-frame is full. That is 10. Count on: %s. There are <b>%d</b> dots." % (lst(11, n), n)
        else:
            e = "Both ten-frames are full. 10 and 10 more: count on 11, 12 … 20. There are <b>20</b> dots."
    elif how == "rows10":
        assert 11 <= n <= 20
        svg = row_svg(n, kind)
        if n < 20:
            e = "The top row has 10. Count on: %s. There are <b>%d</b> %s." % (lst(11, n), n, k)
        else:
            e = "Each row has 10. Count the top row to 10, then count on: %s. There are <b>20</b> %s." % (lst(11, 20), k)
    elif how.startswith("array:"):
        r, c = map(int, how[6:].split("x"))
        assert r * c == n
        svg = array_svg(r, c, kind)
        parts = ["%s" % lst(i * c + 1, i * c + c) for i in range(r)]
        e = "Count one row at a time: %s. There are <b>%d</b> %s." % (", then ".join(parts), n, k)
    else:
        raise ValueError(how)
    return svg, e


def wrongs(n, how):
    """Common counting mistakes: one more (counted one twice), one less (skipped one), and others."""
    w = [n + 1, n - 1]
    if how == "circle":
        w = [n + 1, n - 1, n + 2]          # counted the first one again
    if n > 10 and how in ("rows10", "tenframe"):
        w += [n - 10]                     # counted only the ones after the full ten
    if n > 10:
        w += [rev(n)]                     # wrote the digits the wrong way (31 for 13)
    w += [n + 2, n - 2, n + 3]
    return w


def count_q(n, kind, how, rnd, q=None):
    svg, e = picture(n, kind, how, rnd)
    k = name(kind)
    if how == "tenframe":
        k = "dots"
    q = q or "How many %s are there?" % k
    return mcq(fig(svg) + q, n, wrongs(n, how), e)


# ============================================================ set 1: count 1 to 5
def set_1_to_5(rnd, P):
    plan = [(1, "row"), (2, "row"), (2, "scatter"), (3, "row"), (3, "tenframe"), (3, "scatter"),
            (4, "row"), (4, "array:2x2"), (4, "tenframe"), (4, "scatter"), (5, "row"), (5, "tenframe"),
            (3, "circle"), (5, "scatter"), (4, "circle"), (5, "circle"), (2, "tenframe"), (5, "row"),
            (4, "scatter"), (5, "scatter")]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = [count_q(n, kinds[i % len(kinds)], how, rnd) for i, (n, how) in enumerate(plan)]
    return {"title": "Count 1 to 5", "items": its}


# ============================================================ set 2: count 6 to 10
def set_6_to_10(rnd, P):
    plan = [(6, "row"), (6, "tenframe"), (7, "row"), (6, "array:2x3"), (7, "tenframe"), (6, "scatter"),
            (8, "row5"), (8, "array:2x4"), (7, "scatter"), (8, "tenframe"), (9, "row5"), (9, "array:3x3"),
            (8, "circle"), (9, "tenframe"), (10, "row5"), (10, "array:2x5"), (8, "scatter"), (9, "circle"),
            (10, "circle"), (10, "scatter")]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = [count_q(n, kinds[i % len(kinds)], how, rnd) for i, (n, how) in enumerate(plan)]
    return {"title": "Count 6 to 10", "items": its}


# ============================================================ set 3: count 11 to 20
def set_11_to_20(rnd, P):
    plan = [(11, "rows10"), (12, "tenframe"), (12, "rows10"), (13, "tenframe"), (12, "array:3x4"),
            (14, "rows10"), (15, "tenframe"), (15, "array:3x5"), (11, "circle"), (16, "rows10"),
            (16, "array:4x4"), (17, "tenframe"), (12, "circle"), (18, "rows10"), (18, "array:3x6"),
            (19, "tenframe"), (14, "circle"), (20, "rows10"), (20, "array:4x5"), (15, "circle")]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = [count_q(n, kinds[i % len(kinds)], how, rnd) for i, (n, how) in enumerate(plan)]
    return {"title": "Count 11 to 20", "items": its}


# ============================================================ set 4: how counting works
def set_ideas(rnd, P):
    its = []
    # the last number tells how many
    for n, kind in [(4, "duck"), (6, "cup"), (8, "star"), (7, "flower"), (13, "ball")]:
        nm, he, his = P.next()
        how = "row" if n <= 10 else "rows10"
        svg, _ = picture(n, kind, how, rnd)
        q = fig(svg) + "%s counts the %s: %s. How many %s are there?" % (nm, name(kind), lst(1, n), name(kind))
        e = ("The last number %s says is %d. The last number tells how many. So there are <b>%d</b> %s. "
             "It is not 1. 1 is only the first one." % (nm, n, n, name(kind)))
        its.append(mcq(q, n, [1, n + 1, n - 1], e))
    # 1 more is the next number
    for n, kind in [(3, "apple"), (5, "fish"), (7, "bug"), (9, "heart"), (4, "button"), (14, "duck")]:
        how = "row" if n <= 5 else ("row5" if n <= 10 else "rows10")
        svg, _ = picture(n, kind, how, rnd)
        one = name(kind, 1)
        q = fig(svg) + "Count the %s. Then 1 more %s comes. How many %s are there now?" % (name(kind), one, name(kind))
        e = ("There are %d %s. 1 more is the next number when you count: %d, <b>%d</b>. "
             "Now there are <b>%d</b> %s." % (n, name(kind), n, n + 1, n + 1, name(kind)))
        its.append(mcq(q, n + 1, [n, n + 2, n - 1], e))
    # moving things does not change how many
    for n, kind, how, where in [(6, "ball", "circle", "into a circle"), (8, "star", "scatter", "all over the table"),
                                (8, "cup", "array:2x4", "into 2 rows"), (12, "flower", "circle", "into a circle"),
                                (9, "button", "scatter", "all over the table")]:
        nm, he, his = P.next()
        svg, _ = picture(n, kind, how, rnd)
        q = (fig(svg) + "%s had %d %s in a line. %s moved them %s. How many %s are there now?"
             % (nm, n, name(kind), he.capitalize(), where, name(kind)))
        e = ("Moving them does not change how many. Count them again: %s. There are still <b>%d</b> %s."
             % (lst(1, n), n, name(kind)))
        its.append(mcq(q, n, [n + 1, n - 1, n + 2], e))
    # count out a number: which box has n?
    for target, counts, kind in [(4, [3, 5, 4, 6], "apple"), (6, [6, 7, 5, 8], "duck"),
                                 (8, [9, 7, 10, 8], "star"), (9, [8, 10, 9, 7], "heart")]:
        assert sorted(counts) == sorted(set(counts)) and target in counts
        svg = lettered_groups_svg([(c, kind) for c in counts])
        ans = "Box " + "ABCD"[counts.index(target)]
        q = fig(svg) + "Which box has %d %s?" % (target, name(kind))
        e = "Count each box. %s. So the answer is <b>%s</b>." % (
            ". ".join("Box %s has %d" % ("ABCD"[i], c) for i, c in enumerate(counts)), ans)
        its.append(mcq(q, ans, ["Box " + "ABCD"[i] for i in range(4) if counts[i] != target], e))
    o = its
    # easy to hard
    order = [o[0], o[5], o[1], o[16], o[6], o[11], o[2], o[7], o[12], o[17],
             o[3], o[8], o[13], o[18], o[9], o[14], o[19], o[4], o[10], o[15]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "How counting works", "items": order}


# ============================================================ set 5: counting stories
def set_stories(rnd, P):
    its = []

    def add(n, kind, how, text, extra_wrong=(), each=None):
        nm, he, his = P.next()
        svg, e = picture(n, kind, how, rnd)
        if each:
            e = e.replace("<b>%d</b> dots." % n, "%d dots." % n) + " Each dot is 1 %s, so there are <b>%d</b> %s." % (each[0], n, each[1])
        t = text.format(n=nm, he=he, He=he.capitalize(), his=his, k=name(kind), one=name(kind, 1))
        it = mcq(fig(svg) + t, n, list(extra_wrong) + wrongs(n, how), e)
        its.append(it)

    add(7, "fish", "scatter", "Fish swim in the tank. How many fish are in the tank?")
    add(6, "duck", "row", "Ducks walk in a line to the pond. How many ducks are there?")
    add(8, "cup", "row5", "{n} puts 1 cup out for each friend. How many cups are there?")
    add(9, "bug", "scatter", "{n} sees ladybugs on a leaf. How many ladybugs are there?")
    add(10, "apple", "array:2x5", "Apples are in a box. How many apples are in the box?")
    add(10, "flower", "circle", "{n} plants flowers in a circle. How many flowers are there?")
    add(11, "duck", "row", "{n} lines up toy ducks. How many toy ducks are there?")
    add(12, "cup", "array:2x6", "Cups are on a shelf in 2 rows. How many cups are there?")
    add(13, "star", "rows10", "{n} gets a star for each book {he} reads. How many stars does {he} have?")
    add(12, "ball", "array:3x4", "Balls are in a big box. How many balls are there?")
    add(14, "heart", "tenframe", "{n} puts a dot in the ten-frames for each day of school. How many days is that?", each=("day", "days"))
    add(15, "button", "array:3x5", "{n} sorts buttons into rows. How many buttons are there?")
    add(13, "bug", "circle", "Kids sit in a circle. Each kid has 1 ladybug sticker. How many stickers are there?")
    add(16, "fish", "rows10", "{n} counts the fish in the pet shop. How many fish are there?")
    add(17, "apple", "rows10", "{n} picks apples. How many apples does {he} have?")
    add(18, "flower", "tenframe", "Each dot is 1 flower in the garden. How many flowers are there?", each=("flower", "flowers"))
    add(19, "duck", "rows10", "Ducks swim in rows. How many ducks are there?")
    add(16, "star", "circle", "{n} puts star stickers around a plate. How many stars are there?")
    add(20, "cup", "array:4x5", "{n} stacks cups in rows for a party. How many cups are there?")
    add(20, "heart", "tenframe", "Each dot is 1 heart on the card. How many hearts are there?", each=("heart", "hearts"))
    # questions whose picture is a ten-frame ask about dots
    for it in its:
        assert it["q"].count("<svg") == 1
    return {"title": "Counting stories", "items": its}


# ============================================================ lesson
def body_html(rnd):
    s1, _ = picture(5, "apple", "row", rnd)
    s2, _ = picture(8, "star", "circle", rnd)
    s3 = tenframe_svg(14)
    s4 = scatter_svg(6, "bug", seed=7)
    return (
        "<h2>Count each thing one time</h2>"
        "<p>Touch each thing. Say one number for each one. "
        "The <b>last number</b> you say tells <b>how many</b>.</p>"
        "<figure class='sn-fig'>" + s1 + "<figcaption>1, 2, 3, 4, 5. There are 5 apples.</figcaption></figure>"
        "<h2>Things in a circle or all over</h2>"
        "<p>In a circle, start at one thing. Stop when you get back to it. "
        "When things are all over, mark each one as you count it.</p>"
        "<figure class='sn-fig'>" + s2 + "<figcaption>Start at the top and go around: there are 8 stars.</figcaption></figure>"
        "<figure class='sn-fig'>" + s4 + "<figcaption>Mark each one: there are 6 ladybugs.</figcaption></figure>"
        "<h2>Count 11 to 20</h2>"
        "<p>Fill a ten-frame first. That is 10. Then count on.</p>"
        "<figure class='sn-fig'>" + s3 + "<figcaption>10, then 11, 12, 13, 14. There are 14 dots.</figcaption></figure>"
        "<h2>Big ideas</h2>"
        + table(["Idea", "Example"], [
            ["The last number tells how many", "1, 2, 3, 4, 5, 6: there are 6"],
            ["1 more is the next number", "5 ducks and 1 more: 6 ducks"],
            ["Moving things does not change how many", "6 balls in a line or in a circle: still 6"],
        ]) +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Counting one thing two times", "Touch each thing only once"],
            ["Skipping a thing", "Mark or move each thing as you count"],
            ["Counting the first one in a circle again", "Stop when you get back to the start"],
            ["Counting again to say how many", "Say the last number: that is how many"],
        ])
    )


FAQ = [
    {"q": "How high should a kindergartner count objects?",
     "a": "By the end of kindergarten, children count up to 20 things in a line, in rows or in a circle, and up to 10 things that are spread out. They also count out a number, like 'give me 7 blocks'."},
    {"q": "My child can say the numbers but miscounts. Why?",
     "a": "Saying 1 to 20 is not the same as counting things. Ask your child to touch or move each thing as they say one number. This 'one number for one thing' rule is the key skill."},
    {"q": "What does 'the last number tells how many' mean?",
     "a": "When you count 1, 2, 3, 4, 5, the answer to 'how many?' is 5. Some children count again or say all the numbers. Ask 'So how many are there?' after they count."},
    {"q": "How do ten-frames help with counting to 20?",
     "a": "A full ten-frame is always 10, so children do not have to count it again. They say 10 and count on: 11, 12, 13. This also gets them ready for teen numbers."},
]


def gen():
    rnd = random.Random(2001)
    P = People(rnd)
    sets = [set_1_to_5(rnd, P), set_6_to_10(rnd, P), set_11_to_20(rnd, P), set_ideas(rnd, P), set_stories(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        for it in s["items"]:
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    v = int(tok)
                    assert 1 <= v <= 23 or v in (31, 41, 51, 61, 71, 81, 91), c
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"][-80:]
            seen.add(key)
            it["q"] = it["q"].replace("<svg ", "<svg data-pf='lg' ")
    return {
        "slug": "counting-to-20", "sort": 1, "updated": UPDATED, "pdf_url": "",
        "title": "Counting to 20: How Many Are There?",
        "seo_title": "Kindergarten Counting Worksheets: Count Objects to 20 (How Many?)",
        "short_title": "Counting to 20",
        "domain": "Counting and Cardinality",
        "standard_code": "K.CC.B.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/CC/B/5/",
        "standard_text": "Count to answer “how many?” questions about as many as 20 things arranged in a line, a rectangular "
                         "array, or a circle, or as many as 10 things in a scattered configuration; given a number from "
                         "1–20, count out that many objects.",
        "meta_desc": "Free kindergarten counting worksheets: count objects to 20 in a line, in rows, in a circle and "
                     "spread out, use ten-frames, learn that the last number tells how many, and count out a number. "
                     "100 picture questions with an answer key.",
        "key_big": "Touch each thing once and count. The last number you say tells how many.",
        "key_sub": "1 more is the next number. Moving things does not change how many.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
