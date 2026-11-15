# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Writing Numbers 0 to 20 (K.CC.A.3)
  python3 tools/gen_us_math_gk_writing_numbers_0_to_20.py
Match a group of objects with its written number (0 means none), read the number names
zero to twenty, and write teen numbers the right way round (14, not 41).
"""
import random, re
from ws_common import balance, People, table, write_unit, fig
from k_pics import (name, row_svg, scatter_svg, tenframe_svg, plate_svg, dice_svg, rods_svg, array_svg,
                    cards_svg, KINDS)

UPDATED = "2026-11-16"
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or c.startswith("-"):
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


def wrong_for(n):
    if n == 0:
        return [1, 10, 2]
    if n == 10:
        return [1, 0, 11, 9]
    if 11 <= n <= 19:
        return [rev(n), int("10%d" % (n - 10)), n - 10, n + 1, n - 1]
    if n == 20:
        return [2, 12, 200, 19]
    return [n + 1, n - 1, n + 2, n - 2]


def why(n):
    """How to write n (the second half of an explanation)."""
    if n == 0:
        return "Zero means none. We write it <b>0</b>."
    if 11 <= n <= 19:
        return ("%s is 10 and %d more. Write the 1 for the ten first, then the %d: <b>%d</b>."
                % (WORDS[n].capitalize(), n - 10, n - 10, n))
    if n == 20:
        return "Twenty is 2 tens. Write a 2 and a 0: <b>20</b>."
    if n == 10:
        return "Ten is written with a 1 and a 0: <b>10</b>."
    return "The number %s is written <b>%d</b>." % (WORDS[n], n)


# ------------------------------------------------------------ pictures with a count explanation
def pic(n, kind, how, rnd):
    k = name(kind, n)
    if how == "plate":
        svg = plate_svg(n, kind)
        e = ("Count the %s on the plate: %s. " % (k, lst(1, n))) if n else "The plate is empty. "
    elif how == "tenframe":
        svg = tenframe_svg(n, frames=1 if n <= 10 else 2)
        k = "dots"
        if n == 0:
            e = "The ten-frame is empty. "
        elif n <= 5:
            e = "Count the dots: %s. " % lst(1, n)
        elif n < 10:
            e = "The top row is 5. Count on: %s. " % lst(6, n)
        elif n == 10:
            e = "The ten-frame is full. That is 10. "
        elif n < 20:
            e = "The first ten-frame is full. That is 10. Count on: %s. " % lst(11, n)
        else:
            e = "Both ten-frames are full: 10 and 10 more. "
    elif how == "dice":
        svg = dice_svg([n])
        k = "dots"
        e = "Count the dots: %s. " % lst(1, n)
    elif how == "row":
        svg = row_svg(n, kind, per_row=10)
        e = ("Count: %s. " % lst(1, n)) if n <= 10 else "The top row has 10. Count on: %s. " % lst(11, n)
    elif how == "scatter":
        svg = scatter_svg(n, kind, seed=rnd.randint(1, 10 ** 6))
        e = "Count each one: %s. " % lst(1, n)
    elif how == "rods":
        svg = rods_svg(n // 10, n % 10)
        k = "cubes"
        e = ("The rod has 10 cubes. Count on: %s. " % lst(11, n)) if n % 10 else "Each rod has 10 cubes: 10, 20. "
    elif how.startswith("array:"):
        r, c = map(int, how[6:].split("x"))
        svg = array_svg(r, c, kind)
        e = "Count row by row: %s. " % ", then ".join(lst(i * c + 1, i * c + c) for i in range(r))
    else:
        raise ValueError(how)
    return svg, k, e


def match_q(n, kind, how, rnd, q=None):
    svg, k, e = pic(n, kind, how, rnd)
    if q is None:
        q = "How many %s? Pick the number." % k if how not in ("plate",) else "How many %s are on the plate? Pick the number." % name(kind)
    if n == 0:
        e = e + why(0)
    else:
        e = e + ("There is 1. " if n == 1 else "There are %d. " % n) + why(n)
    return mcq(fig(svg) + q, n, wrong_for(n), e)


# ============================================================ set 1: 0 to 5
def set_0_to_5(rnd, P):
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    plan = [(1, "plate"), (2, "dice"), (3, "row"), (0, "plate"), (4, "dice"), (2, "plate"), (5, "dice"),
            (3, "tenframe"), (0, "tenframe"), (4, "row"), (1, "dice"), (5, "row"), (3, "scatter"),
            (4, "plate"), (2, "tenframe"), (5, "plate"), (4, "scatter"), (5, "tenframe"), (3, "dice")]
    its = [match_q(n, kinds[i % len(kinds)], how, rnd) for i, (n, how) in enumerate(plan)]
    its.insert(9, mcq(fig(plate_svg(0, "cup")) + "Which number means <b>none</b>?", 0, [1, 10, 9],
                      "When there is nothing, the number is <b>0</b> (zero)."))
    return {"title": "Numbers 0 to 5", "items": its}


# ============================================================ set 2: 6 to 10
def set_6_to_10(rnd, P):
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    plan = [(6, "dice"), (6, "tenframe"), (7, "row"), (6, "plate"), (7, "tenframe"), (8, "row"),
            (8, "plate"), (8, "tenframe"), (9, "row"), (6, "scatter"), (9, "tenframe"), (7, "plate"),
            (10, "tenframe"), (10, "row"), (9, "plate"), (8, "array:2x4"), (7, "scatter"), (9, "array:3x3"),
            (10, "plate"), (10, "array:2x5")]
    its = [match_q(n, kinds[i % len(kinds)], how, rnd) for i, (n, how) in enumerate(plan)]
    return {"title": "Numbers 6 to 10", "items": its}


# ============================================================ set 3: 11 to 20
def set_11_to_20(rnd, P):
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    plan = [(11, "tenframe"), (12, "rods"), (13, "row"), (12, "tenframe"), (14, "rods"), (13, "tenframe"),
            (15, "row"), (14, "tenframe"), (16, "rods"), (15, "tenframe"), (17, "row"), (16, "tenframe"),
            (18, "rods"), (17, "tenframe"), (19, "row"), (18, "tenframe"), (19, "rods"), (20, "tenframe"),
            (20, "row"), (11, "rods")]
    its = [match_q(n, kinds[i % len(kinds)], how, rnd) for i, (n, how) in enumerate(plan)]
    return {"title": "Numbers 11 to 20", "items": its}


# ============================================================ set 4: number names
def set_names(rnd, P):
    its = []
    for n in [3, 8, 0, 5, 10, 12, 13, 15, 14, 17, 19, 11, 16, 18, 20]:
        w = WORDS[n]
        q = "Which number is <b>%s</b>?" % w
        e = why(n)
        if 11 <= n <= 19 and rev(n):
            e += " Do not write %d. That is a different number." % rev(n)
        wr = {3: [8, 2, 4], 8: [3, 6, 9], 0: [10, 1, 6], 5: [2, 4, 6], 10: [1, 0, 100]}.get(n) or wrong_for(n)
        if n == 12:
            wr = [21, 2, 20, 102]
        if n == 20:
            wr = [2, 12, 200]
        its.append(mcq(q, n, wr, e))
    for n in [6, 9, 14, 17, 20]:
        q = fig(cards_svg([str(n)], w=64, h=64)) + "How do you say this number?"
        w = WORDS[n]
        wr = {6: ["nine", "sixteen", "seven"], 9: ["six", "nineteen", "ninety"],
              14: ["forty", "four", "forty-one"], 17: ["seventy", "seventy-one", "seven"],
              20: ["two", "twelve", "two hundred"]}[n]
        e = "This number is said <b>%s</b>." % w
        if n in (14, 17):
            e += " The 1 means one ten, so it is a teen number."
        its.append(mcq(q, w, wr, e))
    o = its
    order = [o[0], o[1], o[15], o[2], o[3], o[16], o[4], o[5], o[6], o[17],
             o[7], o[8], o[9], o[18], o[10], o[11], o[12], o[13], o[19], o[14]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Number names", "items": order}


# ============================================================ set 5: stories
def set_stories(rnd, P):
    its = []

    def add(n, kind, how, text):
        nm, he, his = P.next()
        svg, k, e = pic(n, kind, how, rnd)
        t = text.format(n=nm, he=he, He=he.capitalize(), his=his)
        e = e + (("There is 1. " if n == 1 else "There are %d. " % n) if n else "") + why(n)
        its.append(mcq(fig(svg) + t, n, wrong_for(n), e))

    add(4, "apple", "plate", "{n} puts apples on a plate. Which number tells how many apples?")
    add(0, "cup", "plate", "{n} ate all the cookies. The plate is empty. How many cookies are left?")
    add(6, "duck", "row", "Ducks swim in a line. Which number tells how many ducks?")
    add(5, "fish", "scatter", "Fish swim in a pond. Which number tells how many fish?")
    add(7, "flower", "plate", "{n} puts flowers on a plate. Which number tells how many flowers?")
    add(3, "star", "dice", "{n} rolls a dot cube. Which number tells how many dots?")
    add(8, "bug", "scatter", "Ladybugs sit on a leaf. Which number tells how many ladybugs?")
    add(9, "heart", "tenframe", "{n} puts a dot in the ten-frame for each heart {he} drew. How many hearts did {he} draw?")
    add(10, "ball", "row", "{n} lines up balls. Which number tells how many balls?")
    add(0, "dot", "tenframe", "Nobody has put a dot in the ten-frame yet. How many dots are there?")
    add(11, "cube", "rods", "{n} has a rod of 10 cubes and some more cubes. How many cubes in all?")
    add(12, "apple", "row", "{n} picks apples. Which number tells how many apples?")
    add(13, "dot", "tenframe", "Each dot is 1 day of school. How many days is that?")
    add(14, "star", "row", "{n} gets stars on {his} chart. Which number tells how many stars?")
    add(15, "cube", "rods", "{n} builds with cubes. How many cubes are there?")
    add(16, "dot", "tenframe", "Each dot is 1 kid on the bus. How many kids are on the bus?")
    add(17, "cup", "row", "Cups are ready for a party. Which number tells how many cups?")
    add(18, "fish", "row", "{n} counts the fish in a tank. Which number tells how many fish?")
    add(19, "cube", "rods", "{n} makes a tower. How many cubes are there?")
    add(20, "dot", "tenframe", "Each dot is 1 crayon. How many crayons are there?")
    for it in its:
        it["e"] = it["e"].replace("There are 13. ", "That is 13 days. ").replace("There are 16. ", "That is 16 kids. ")\
            .replace("There are 20. ", "That is 20 crayons. ").replace("There are 9. ", "That is 9 hearts. ")
    return {"title": "Count and write the number", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>A number tells how many</h2>"
        "<p>Count the things. Then write the number.</p>"
        "<figure class='sn-fig'>" + plate_svg(3, "apple") + "<figcaption>1, 2, 3. We write <b>3</b>.</figcaption></figure>"
        "<h2>Zero means none</h2>"
        "<p>When there is nothing, the number is <b>0</b>.</p>"
        "<figure class='sn-fig'>" + plate_svg(0, "apple") + "<figcaption>The plate is empty: 0 apples.</figcaption></figure>"
        "<h2>Numbers 0 to 20</h2>"
        + table(["Number", "Name", "Number", "Name"], [
            ["0", "zero", "11", "eleven"], ["1", "one", "12", "twelve"], ["2", "two", "13", "thirteen"],
            ["3", "three", "14", "fourteen"], ["4", "four", "15", "fifteen"], ["5", "five", "16", "sixteen"],
            ["6", "six", "17", "seventeen"], ["7", "seven", "18", "eighteen"], ["8", "eight", "19", "nineteen"],
            ["9", "nine", "20", "twenty"], ["10", "ten", "", ""],
        ]) +
        "<h2>Teen numbers: the 1 comes first</h2>"
        "<p>Fourteen is 10 and 4. We say the 4 first, but we <b>write the 1 first</b>: 14.</p>"
        "<figure class='sn-fig'>" + tenframe_svg(14) + "<figcaption>10 and 4 more: 14.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Writing 41 for fourteen", "Write the 1 first: 14"],
            ["Writing 104 for fourteen (10 and 4)", "Teen numbers have only 2 digits: 14"],
            ["Writing 1 for none", "None is 0"],
            ["Writing 2 for twenty", "Twenty is 2 tens: 20"],
        ])
    )


FAQ = [
    {"q": "Which numbers should a kindergartner write?",
     "a": "By the end of kindergarten, children write the numbers 0 to 20. They also write a number to show how many things are in a group, and use 0 when there are none."},
    {"q": "Why does my child write 41 instead of 14?",
     "a": "We say 'four-teen', so the 4 comes first in speech. Show 14 as a full ten-frame and 4 more: the 1 stands for the ten, so it comes first."},
    {"q": "My child writes some numbers backward, like a backward 3. Is that a problem?",
     "a": "It is very common at age 5 and 6. Give a model to copy, trace numbers in sand or with a finger, and say how the stroke goes. Most children stop by age 7."},
    {"q": "Why is zero hard for young children?",
     "a": "Zero is the number for nothing, so there is nothing to count. Use an empty plate or an empty ten-frame and ask 'How many?' to show that the answer is 0."},
]


def gen():
    rnd = random.Random(2003)
    P = People(rnd)
    sets = [set_0_to_5(rnd, P), set_6_to_10(rnd, P), set_11_to_20(rnd, P), set_names(rnd, P), set_stories(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        for it in s["items"]:
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"][-80:]
            seen.add(key)
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert int(tok) <= 21 or int(tok) in (31, 41, 51, 61, 71, 81, 91, 100, 101, 102, 103, 104, 105, 106,
                                                          107, 108, 109, 200), c
            it["q"] = it["q"].replace("<svg ", "<svg data-pf='lg' ")
    return {
        "slug": "writing-numbers-0-to-20", "sort": 3, "updated": UPDATED, "pdf_url": "",
        "title": "Writing Numbers 0 to 20: Match Numbers to Groups",
        "seo_title": "Kindergarten Writing Numbers 0-20 Worksheets: Number Names and Zero",
        "short_title": "Writing Numbers 0 to 20",
        "domain": "Counting and Cardinality",
        "standard_code": "K.CC.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/CC/A/3/",
        "standard_text": "Write numbers from 0 to 20. Represent a number of objects with a written numeral 0–20 "
                         "(with 0 representing a count of no objects).",
        "meta_desc": "Free kindergarten number writing worksheets: match groups of objects to the numbers 0 to 20, "
                     "learn that 0 means none, read the number names zero to twenty, and write teen numbers the "
                     "right way (14, not 41). 100 picture questions with an answer key.",
        "key_big": "Count the group, then write the number. Zero (0) means none.",
        "key_sub": "In teen numbers the 1 comes first: fourteen is 10 and 4, written 14.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
