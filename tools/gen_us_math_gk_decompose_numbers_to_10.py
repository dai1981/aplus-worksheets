# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Decompose Numbers to 10 (K.OA.A.3)
  python3 tools/gen_us_math_gk_decompose_numbers_to_10.py
Break a number up to 10 into two parts in more than one way: two-colour ten-frames, number bonds,
hidden parts in a box, equations like 7 = 4 + 3, and short stories.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import name, tenframe_mix_svg, bond_svg, box_svg, two_groups_svg, KINDS
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"


def part_wrongs(n, a):
    b = n - a
    return [b + 1, b - 1, a if a != b else None, n, n + a, b + 2]


# ============================================================ set 1: two colours
def set_colours(rnd, K):
    plan = [(3, 2), (4, 1), (4, 3), (5, 2), (5, 4), (6, 1), (6, 4), (7, 2), (7, 5), (8, 3),
            (8, 6), (9, 4), (9, 7), (10, 3), (10, 6), (6, 3), (7, 4), (8, 5), (9, 1), (10, 8)]
    its = []
    for i, (n, a) in enumerate(plan):
        b = n - a
        svg = tenframe_mix_svg(["r"] * a + ["b"] * b)
        q = "There are %d dots. %d are red. How many are blue?" % (n, a)
        e = "%d is %d and %d. %d = %d + %d. So <b>%d</b> are blue." % (n, a, b, n, a, b, b)
        if b == 1:
            e = "%d is %d and 1. %d = %d + 1. So <b>1</b> is blue." % (n, a, n, a)
        its.append(mcq(fig(svg) + q, b, part_wrongs(n, a), e))
    return {"title": "Two colours, one number", "items": its}


# ============================================================ set 2: number bonds
def set_bonds(rnd, K):
    plan = [(4, 2), (5, 1), (5, 3), (6, 2), (6, 5), (7, 3), (7, 6), (8, 2), (8, 4), (9, 3),
            (9, 6), (10, 4), (10, 7), (3, 1), (8, 7), (9, 5), (10, 2), (7, 1), (6, 3), (10, 5)]
    its = []
    for i, (n, a) in enumerate(plan):
        b = n - a
        if i % 2 == 0:
            svg = bond_svg(n, a, "?")
        else:
            svg = bond_svg(n, "?", a)
        q = "%d is made of two parts. One part is %d. What is the other part?" % (n, a)
        e = "%d and %d make %d. The missing part is <b>%d</b>." % (a, b, n, b)
        its.append(mcq(fig(svg) + q, b, part_wrongs(n, a), e))
    return {"title": "Number bonds", "items": its}


# ============================================================ set 3: hidden in the box
def set_box(rnd, K):
    plan = [(4, 3), (5, 2), (5, 4), (6, 3), (6, 1), (7, 4), (7, 2), (8, 5), (8, 3), (9, 6),
            (9, 2), (10, 7), (6, 4), (7, 5), (8, 6), (9, 4), (10, 4), (8, 1), (9, 8), (10, 2)]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = []
    for i, (n, a) in enumerate(plan):
        kind = kinds[i % len(kinds)]
        b = n - a
        svg = box_svg(a, kind)
        q = "There are %d %s in all. Some are in the box. How many are in the box?" % (n, name(kind))
        e = ("You see %d. Count on to %d: %s. So <b>%d</b> %s in the box."
             % (a, n, ", ".join(str(k) for k in range(a + 1, n + 1)), b, "is" if b == 1 else "are"))
        its.append(mcq(fig(svg) + q, b, part_wrongs(n, a), e))
    return {"title": "How many are hidden?", "items": its}


# ============================================================ set 4: ways to make a number
def set_ways(rnd, K):
    its = []
    for n, a in [(4, 1), (5, 2), (6, 4), (7, 3), (8, 5), (9, 2), (10, 6), (6, 1), (8, 2), (10, 3)]:
        b = n - a
        kind = KINDS[(n + a) % len(KINDS)]
        svg = two_groups_svg(a, kind, b, word="and")
        right = "%d = %d + %d" % (n, a, b)
        wr = ["%d = %d + %d" % (n, a, b + 1), "%d = %d + %d" % (n, a + 1, b + 1), "%d = %d + %d" % (n, a, b - 1) if b > 1 else "%d = %d + %d" % (n, a - 1 if a > 1 else a + 2, b)]
        e = "%d %s and %d %s make %d. So <b>%s</b>." % (a, name(kind, a), b, name(kind, b), n, right)
        its.append(mcq(fig(svg) + "Which matches the picture?", right, wr, e))
    for n, right, wr in [
        (5, "5 = 4 + 1", ["5 = 4 + 2", "5 = 3 + 3", "5 = 1 + 3"]),
        (6, "6 = 3 + 3", ["6 = 3 + 4", "6 = 2 + 3", "6 = 5 + 2"]),
        (7, "7 = 2 + 5", ["7 = 2 + 4", "7 = 3 + 5", "7 = 6 + 2"]),
        (8, "8 = 6 + 2", ["8 = 6 + 3", "8 = 4 + 3", "8 = 7 + 2"]),
        (9, "9 = 5 + 4", ["9 = 5 + 5", "9 = 4 + 4", "9 = 6 + 4"]),
        (10, "10 = 7 + 3", ["10 = 7 + 2", "10 = 6 + 3", "10 = 8 + 3"]),
        (7, "7 = 1 + 6", ["7 = 1 + 5", "7 = 2 + 6", "7 = 1 + 7"]),
        (9, "9 = 8 + 1", ["9 = 8 + 2", "9 = 7 + 1", "9 = 9 + 1"]),
        (8, "8 = 4 + 4", ["8 = 4 + 3", "8 = 5 + 4", "8 = 3 + 3"]),
        (10, "10 = 1 + 9", ["10 = 1 + 8", "10 = 2 + 9", "10 = 0 + 9"]),
    ]:
        a, b = [int(x) for x in right.split("=")[1].split("+")]
        assert a + b == n
        for w in wr:
            x, y = [int(t) for t in w.split("=")[1].split("+")]
            assert x + y != n, w
        q = fig(tenframe_mix_svg(["r"] * n)) + "Which is a way to make %d?" % n
        e = "%d and %d make %d. So <b>%s</b> is right. Check each one by adding the parts." % (a, b, n, right)
        its.append(mcq(q, right, wr, e, allow_zero=True))
    o = its
    order = [o[0], o[10], o[1], o[11], o[7], o[2], o[12], o[3], o[16], o[13],
             o[8], o[4], o[18], o[14], o[5], o[15], o[9], o[17], o[6], o[19]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Ways to make a number", "items": order}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []

    def story(n, a, kind, text, unit=None):
        p = K.next()
        b = n - a
        t = text.format(n_=n, a=a, **p)
        one, many = unit or (name(kind, 1), name(kind))
        u = lambda v: "%d %s" % (v, one if v == 1 else many)
        svg = box_svg(a, kind)
        e = "%d and %d make %d. %d = %d + %d. The answer is <b>%s</b>." % (a, b, n, n, a, b, u(b))
        its.append(mcq(fig(svg) + t, u(b), [u(w) for w in part_wrongs(n, a) if w and w > 0], e))

    story(4, 3, "apple", "{n} has {n_} apples. {a} are on the table. The rest are in a box. How many are in the box?")
    story(5, 2, "ball", "{n} has {n_} balls. {a} are out. The rest are in the toy box. How many are in the toy box?")
    story(6, 4, "duck", "There are {n_} toy ducks. {a} are out of the box. How many are still in the box?")
    story(5, 4, "cup", "{n} needs {n_} cups. {He} sees {a}. The rest are in a box. How many are in the box?")
    story(6, 2, "star", "{n} has {n_} star stickers. {He} sees {a}. The rest are in a box. How many are in the box?",
          unit=("sticker", "stickers"))
    story(7, 5, "fish", "There are {n_} toy fish. {a} are out. How many are still in the box?")
    story(7, 3, "flower", "{n} picks {n_} flowers. {He} puts {a} on the table and the rest in a box. How many are in the box?")
    story(8, 6, "button", "A box had {n_} buttons. {n} took out {a}. How many are still in the box?")
    story(8, 4, "heart", "{n} cuts out {n_} hearts. {a} are on the table. The rest are in a box. How many are in the box?")
    story(9, 5, "bug", "There are {n_} toy ladybugs. {a} are out. How many are still in the box?")
    story(9, 7, "apple", "{n} has {n_} apples. {He} puts {a} in a bowl. The rest go in a box. How many go in the box?")
    story(10, 6, "ball", "There are {n_} balls in all. {a} are on the floor. How many are in the box?")
    story(10, 2, "duck", "{n} has {n_} toy ducks. {a} are out. How many are in the box?")
    story(6, 5, "cup", "{n_} cups are for a party. {a} are on the table. How many are still in the box?")
    story(7, 6, "star", "{n} has {n_} stars. {a} are on {his} chart. The rest are in a box. How many are in the box?")
    story(8, 3, "fish", "There are {n_} toy fish in all. {a} are out. How many are in the box?")
    story(9, 3, "flower", "{n} has {n_} paper flowers. {a} are on the wall. The rest are in a box. How many are in the box?")
    story(10, 5, "button", "{n} has {n_} buttons. {a} are on a coat. The rest are in a box. How many are in the box?")
    story(10, 9, "heart", "{n} made {n_} hearts. {a} are on the table. How many are in the box?")
    story(9, 1, "bug", "There are {n_} toy ladybugs. Only {a} is out. How many are in the box?")
    return {"title": "Part and whole stories", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>A number has parts</h2>"
        "<p>You can break a number into two parts. Together, the parts make the number.</p>"
        "<figure class='sn-fig'>" + tenframe_mix_svg(["r"] * 4 + ["b"] * 3)
        + "<figcaption>7 is 4 and 3. We write 7 = 4 + 3.</figcaption></figure>"
        "<h2>More than one way</h2>"
        + table(["Number", "Ways to make it"], [
            ["5", "5 = 1 + 4, 5 = 2 + 3"],
            ["7", "7 = 1 + 6, 7 = 2 + 5, 7 = 3 + 4"],
            ["10", "10 = 1 + 9, 10 = 2 + 8, 10 = 3 + 7, 10 = 4 + 6, 10 = 5 + 5"],
        ]) +
        "<h2>Number bonds</h2>"
        "<figure class='sn-fig'>" + bond_svg(8, 5, "?")
        + "<figcaption>8 is 5 and 3. The missing part is 3.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Giving the whole, not the part", "Ask: what goes with this part?"],
            ["Off by one", "Count on from the part you know"],
            ["Thinking there is only one way", "Try 1 + ?, 2 + ?, 3 + ?"],
        ])
    )


FAQ = [
    {"q": "What does decompose a number mean?",
     "a": "It means breaking a number into two parts. For example, 6 can be 1 and 5, 2 and 4, or 3 and 3. The parts always add up to the number."},
    {"q": "What is a number bond?",
     "a": "It is a small drawing with the whole number on top and its two parts below. It shows how the parts and the whole fit together."},
    {"q": "How does this help with adding and subtracting?",
     "a": "If you know 8 is 5 and 3, you also know 5 + 3 = 8, 8 − 3 = 5 and 8 − 5 = 3. Parts and wholes make facts easy to learn."},
    {"q": "How can I practice at home?",
     "a": "Hide some of 7 small toys under a cup and show the rest. Ask how many are hidden. Then try again with a different number hidden."},
]


def gen():
    rnd = random.Random(2008)
    K = Kids(rnd)
    sets = [set_colours(rnd, K), set_bonds(rnd, K), set_box(rnd, K), set_ways(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=20)
    return {
        "slug": "decompose-numbers-to-10", "sort": 8, "updated": UPDATED, "pdf_url": "",
        "title": "Decompose Numbers to 10: Parts and Wholes",
        "seo_title": "Kindergarten Decomposing Numbers Worksheets: Number Bonds and Parts to 10",
        "short_title": "Parts of Numbers to 10",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "K.OA.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/OA/A/3/",
        "standard_text": "Decompose numbers less than or equal to 10 into pairs in more than one way, e.g., by using "
                         "objects or drawings, and record each decomposition by a drawing or equation "
                         "(e.g., 5 = 2 + 3 and 5 = 4 + 1).",
        "meta_desc": "Free kindergarten worksheets on decomposing numbers to 10: two-colour ten-frames, number bonds, "
                     "hidden parts, and number sentences like 7 = 4 + 3. 100 picture questions with an answer key.",
        "key_big": "A number can be broken into two parts. The parts make the whole.",
        "key_sub": "7 is 4 and 3, or 5 and 2, or 6 and 1. We write 7 = 4 + 3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
