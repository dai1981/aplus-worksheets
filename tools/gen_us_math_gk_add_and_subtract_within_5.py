# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Add and Subtract Within 5 (K.OA.A.5)
  python3 tools/gen_us_math_gk_add_and_subtract_within_5.py
Fluency with the facts within 5: add with dot cubes and pictures, take away, mixed facts,
missing numbers and short stories. No answer is 0.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import name, dice_svg, two_groups_svg, crossed_row_svg, tenframe_mix_svg, cards_svg, KINDS
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"
ADD = [(1, 1), (2, 1), (1, 2), (3, 1), (2, 2), (1, 3), (4, 1), (3, 2), (2, 3), (1, 4)]
SUB = [(2, 1), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (5, 4)]


def add_w(a, b):
    s = a + b
    return [s - 1, s + 1, abs(a - b) or None, max(a, b), s + 2]


def sub_w(a, b):
    d = a - b
    return [d + 1, d - 1, a + b, b if b != d else None, a, d + 2, d + 3]


# ============================================================ set 1: add
def set_add(rnd, K):
    its = []
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    for a, b in ADD:
        s = a + b
        q = fig(dice_svg([a, b])) + "Add the dots. %d + %d = ?" % (a, b)
        e = "%d dots and %d more: count on %s. %d + %d = <b>%d</b>." % (
            a, b, ", ".join(str(k) for k in range(a + 1, s + 1)), a, b, s)
        its.append(mcq(q, s, add_w(a, b), e))
    for i, (a, b) in enumerate(ADD):
        kind = kinds[i]
        s = a + b
        q = fig(two_groups_svg(a, kind, b, word="+")) + "How many %s in all?" % name(kind)
        e = "%d and %d make %d. %d + %d = <b>%d</b>." % (a, b, s, a, b, s)
        its.append(mcq(q, s, add_w(a, b), e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14],
             o[5], o[15], o[6], o[16], o[7], o[17], o[8], o[18], o[9], o[19]]
    return {"title": "Add within 5", "items": order}


# ============================================================ set 2: subtract
def set_sub(rnd, K):
    its = []
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    for i, (a, b) in enumerate(SUB):
        kind = kinds[i]
        d = a - b
        q = fig(crossed_row_svg(a, kind, b)) + "%d %s. Take away %d. How many are left?" % (a, name(kind), b)
        e = "%d take away %d leaves %d. %d − %d = <b>%d</b>." % (a, b, d, a, b, d)
        its.append(mcq(q, d, sub_w(a, b), e))
    for a, b in SUB:
        d = a - b
        q = fig(tenframe_mix_svg(["r"] * d + ["x"] * b)) + "%d − %d = ?" % (a, b)
        e = "%d dots. %d are crossed out. %d %s left. %d − %d = <b>%d</b>." % (a, b, d, "is" if d == 1 else "are", a, b, d)
        its.append(mcq(q, d, sub_w(a, b), e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14],
             o[5], o[15], o[6], o[16], o[7], o[17], o[8], o[18], o[9], o[19]]
    return {"title": "Subtract within 5", "items": order}


# ============================================================ set 3: mixed facts
def set_mixed(rnd, K):
    facts = [("+", 2, 2), ("−", 4, 1), ("+", 3, 1), ("−", 5, 2), ("+", 1, 4), ("−", 3, 2), ("+", 2, 3),
             ("−", 5, 4), ("+", 4, 0), ("−", 4, 2), ("+", 3, 2), ("−", 5, 3), ("+", 1, 3), ("−", 2, 1),
             ("+", 4, 1), ("−", 5, 0), ("+", 0, 3), ("−", 4, 3), ("+", 2, 1), ("−", 5, 1)]
    its = []
    for op, a, b in facts:
        r = a + b if op == "+" else a - b
        q = fig(cards_svg([str(a), op, str(b), "=", "?"], w=46)) + "What is %d %s %d?" % (a, op, b)
        if op == "+":
            if b == 0 or a == 0:
                e = "Adding 0 does not change a number. %d + %d = <b>%d</b>." % (a, b, r)
                w = [r + 1, r - 1, 0, r + 2]
            else:
                e = "Start at %d and count on %d. %d + %d = <b>%d</b>." % (a, b, a, b, r)
                w = add_w(a, b)
        else:
            if b == 0:
                e = "Taking away 0 takes nothing away. %d − 0 = <b>%d</b>." % (a, r)
                w = [r - 1, r + 1, 0, r - 2]
            else:
                e = "Start at %d and count back %d. %d − %d = <b>%d</b>." % (a, b, a, b, r)
                w = sub_w(a, b)
        its.append(mcq(q, r, w, e, allow_zero=True))
    return {"title": "Mixed facts", "items": its}


# ============================================================ set 4: missing numbers
def set_missing(rnd, K):
    its = []
    for a, s in [(1, 3), (2, 4), (3, 5), (1, 5), (4, 5), (2, 3), (3, 4), (2, 5), (1, 4), (1, 2)]:
        b = s - a
        q = fig(tenframe_mix_svg(["r"] * a + [""] * (5 - a))) + "%d + ? = %d" % (a, s)
        e = "Start at %d and count on to %d: %s. That is %d more. %d + %d = %d, so the missing number is <b>%d</b>." % (
            a, s, ", ".join(str(k) for k in range(a + 1, s + 1)), b, a, b, s, b)
        its.append(mcq(q, b, [b + 1, b - 1, s, a, s + a, b + 2, b + 3], e))
    for a, d in [(3, 1), (4, 2), (5, 3), (5, 1), (4, 1), (5, 2), (3, 2), (4, 3), (5, 4), (2, 1)]:
        b = a - d
        q = fig(dice_svg([a])) + "%d − ? = %d" % (a, d)
        e = "Take away from %d until %d %s left. You take away %d. %d − %d = %d, so the missing number is <b>%d</b>." % (
            a, d, "is" if d == 1 else "are", b, a, b, d, b)
        its.append(mcq(q, b, [b + 1, b - 1, a + d, d if d != b else None, a, b + 2, b + 3], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[5], o[16], o[2], o[12], o[6], o[17],
             o[3], o[13], o[7], o[18], o[4], o[14], o[8], o[19], o[9], o[15]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Missing numbers", "items": order}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []

    def add(a, b, kind, text):
        p = K.next()
        s = a + b
        u = lambda v: "%d %s" % (v, name(kind, v))
        t = text.format(a=a, b=b, **p)
        e = "%d and %d more make %d. %d + %d = %d. The answer is <b>%s</b>." % (a, b, s, a, b, s, u(s))
        its.append(mcq(fig(two_groups_svg(a, kind, b, word="and")) + t, u(s), [u(w) for w in add_w(a, b) if w], e))

    def sub(a, b, kind, text):
        p = K.next()
        d = a - b
        u = lambda v: "%d %s" % (v, name(kind, v))
        t = text.format(a=a, b=b, **p)
        e = "%d take away %d leaves %d. %d − %d = %d. The answer is <b>%s</b>." % (a, b, d, a, b, d, u(d))
        its.append(mcq(fig(crossed_row_svg(a, kind, b)) + t, u(d), [u(w) for w in sub_w(a, b) if w and w > 0], e))

    add(2, 1, "apple", "{n} has {a} apples. {He} gets {b} more. How many apples now?")
    sub(3, 1, "ball", "{n} has {a} balls. {He} gives away {b}. How many balls are left?")
    add(1, 1, "duck", "{a} duck swims. {b} more duck comes. How many ducks now?")
    sub(4, 2, "cup", "There are {a} cups. {b} break. How many cups are left?")
    add(3, 1, "fish", "{n} sees {a} fish. Then {he} sees {b} more. How many fish in all?")
    sub(5, 1, "bug", "{a} ladybugs are on a leaf. {b} flies away. How many are left?")
    add(2, 2, "star", "{n} gets {a} stars today and {b} stars tomorrow. How many stars in all?")
    sub(4, 1, "flower", "{n} picks {a} flowers. {He} gives {b} to a friend. How many are left?")
    add(1, 3, "heart", "{n} draws {a} heart. Then {he} draws {b} more. How many hearts now?")
    sub(5, 3, "apple", "There are {a} apples. {n} eats {b}. How many apples are left?")
    add(4, 1, "button", "A coat has {a} buttons. {n} sews on {b} more. How many buttons now?")
    sub(3, 2, "duck", "{a} ducks are in a pond. {b} walk away. How many are still in the pond?")
    add(3, 2, "ball", "{n} has {a} balls. {He} gets {b} more. How many balls now?")
    sub(5, 2, "fish", "{a} fish are in a bowl. {n} moves {b}. How many are still in the bowl?")
    add(2, 3, "cup", "{a} cups are on the table. {n} puts out {b} more. How many cups now?")
    sub(4, 3, "star", "{n} has {a} stars. {He} uses {b}. How many stars are left?")
    add(1, 4, "flower", "{n} has {a} flower. {He} picks {b} more. How many flowers now?")
    sub(5, 4, "heart", "{n} has {a} hearts. {He} gives {b} away. How many are left?")
    add(1, 2, "bug", "{a} ladybug is on a rock. {b} more come. How many ladybugs now?")
    sub(2, 1, "button", "{n} has {a} buttons. {He} loses {b}. How many are left?")
    return {"title": "Quick stories", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Know the facts within 5</h2>"
        "<p>These facts are small. With practice, you can say them fast, without counting.</p>"
        + table(["Add", "Take away"], [
            ["1 + 1 = 2", "2 − 1 = 1"], ["2 + 1 = 3", "3 − 1 = 2"], ["2 + 2 = 4", "4 − 2 = 2"],
            ["3 + 1 = 4", "4 − 1 = 3"], ["3 + 2 = 5", "5 − 2 = 3"], ["4 + 1 = 5", "5 − 1 = 4"],
        ]) +
        "<h2>Use your fingers or dots</h2>"
        "<figure class='sn-fig'>" + dice_svg([3, 2]) + "<figcaption>3 and 2 make 5: 3 + 2 = 5.</figcaption></figure>"
        "<h2>Add 0, take away 0</h2>"
        "<p>Adding 0 or taking away 0 does not change the number: 4 + 0 = 4, 5 − 0 = 5.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Mixing up + and −", "+ means more. − means take away"],
            ["Off by one", "Count on or count back from the first number"],
            ["Thinking 4 + 0 = 0", "Adding nothing keeps the number the same"],
        ])
    )


FAQ = [
    {"q": "What does fluently add and subtract within 5 mean?",
     "a": "It means a child can say facts like 3 + 2 = 5 and 4 − 1 = 3 quickly and correctly. This is the one fluency goal of kindergarten math."},
    {"q": "Which facts are within 5?",
     "a": "All sums up to 5, like 1 + 1, 2 + 3 and 4 + 1, and all differences from numbers up to 5, like 5 − 2 and 3 − 1."},
    {"q": "How can my child learn these facts fast?",
     "a": "Play short games every day: show fingers, roll a dot cube, or use 5 small toys and hide some. A few minutes a day works better than one long session."},
    {"q": "Should my child still use fingers?",
     "a": "Yes, at first. Fingers show the facts. Over time, children remember the answer and do not need to count."},
]


def gen():
    rnd = random.Random(2009)
    K = Kids(rnd)
    sets = [set_add(rnd, K), set_sub(rnd, K), set_mixed(rnd, K), set_missing(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=10)
    return {
        "slug": "add-and-subtract-within-5", "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Add and Subtract Within 5: Fast Facts",
        "seo_title": "Kindergarten Add and Subtract Within 5 Worksheets: Math Fact Fluency",
        "short_title": "Facts Within 5",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "K.OA.A.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/OA/A/5/",
        "standard_text": "Fluently add and subtract within 5.",
        "meta_desc": "Free kindergarten worksheets to add and subtract within 5: dot cubes, take-away pictures, mixed "
                     "facts, missing numbers and quick stories. Build math fact fluency with 100 questions and an answer key.",
        "key_big": "Learn the small facts until you can say them fast: 3 + 2 = 5, 5 − 2 = 3.",
        "key_sub": "Adding 0 or taking away 0 does not change the number.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
