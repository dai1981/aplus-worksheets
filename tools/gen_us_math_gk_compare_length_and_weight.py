# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Compare Length, Height and Weight (K.MD.A.1, K.MD.A.2)
  python3 tools/gen_us_math_gk_compare_length_and_weight.py
Compare two pencils (longer, shorter, same), find the longest and shortest, compare cube towers
(taller, shorter, how many more cubes), read a pan balance (heavier, lighter), and name what we measure.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import name, pencils_svg, towers_svg, balance_svg
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"
SAME = "They are the same length"
CANT = "We cannot tell"


# ============================================================ set 1: longer or shorter
def set_two(rnd, K):
    its = []
    plan = [(4, 7, "longer"), (6, 3, "longer"), (5, 8, "shorter"), (7, 4, "shorter"), (5, 5, "longer"),
            (3, 6, "longer"), (8, 5, "shorter"), (6, 7, "longer"), (4, 4, "shorter"), (7, 6, "shorter"),
            (6, 8, "longer"), (5, 3, "shorter"), (8, 7, "longer"), (3, 4, "shorter"), (7, 7, "longer"),
            (4, 6, "shorter"), (6, 5, "longer"), (5, 6, "shorter"), (8, 4, "longer"), (6, 6, "shorter")]
    for a, b, word in plan:
        q = fig(pencils_svg([a, b])) + "Which pencil is <b>%s</b>?" % word
        if a == b:
            ans = SAME
            e = "The pencils start at the same place and end at the same place. <b>They are the same length</b>."
        else:
            big = "Pencil A" if a > b else "Pencil B"
            small = "Pencil B" if a > b else "Pencil A"
            ans = big if word == "longer" else small
            e = ("Both pencils start at the same place. Look at where they end. %s goes further, so it is longer. "
                 "The answer is <b>%s</b>." % (big, ans))
        ch = ["Pencil A", "Pencil B", SAME, CANT]
        its.append(mcq(q, ans, [c for c in ch if c != ans], e))
    return {"title": "Longer or shorter", "items": its}


# ============================================================ set 2: longest and shortest
def set_four(rnd, K):
    its = []
    plans = [([5, 7, 4, 6], "longest"), ([6, 3, 7, 5], "shortest"), ([4, 6, 8, 5], "longest"),
             ([7, 5, 6, 3], "shortest"), ([8, 6, 5, 7], "longest"), ([5, 4, 7, 6], "shortest"),
             ([3, 5, 4, 6], "longest"), ([7, 8, 4, 6], "shortest"), ([6, 4, 5, 8], "longest"),
             ([4, 7, 6, 5], "shortest"), ([5, 8, 6, 7], "longest"), ([8, 5, 3, 6], "shortest"),
             ([6, 5, 7, 4], "longest"), ([5, 6, 8, 2], "shortest"), ([7, 4, 3, 5], "longest"),
             ([3, 6, 7, 5], "shortest"), ([4, 5, 3, 7], "longest"), ([6, 7, 5, 8], "shortest"),
             ([2, 4, 6, 3], "longest"), ([7, 3, 5, 4], "shortest")]
    for lens, word in plans:
        assert len(set(lens)) == 4
        v = max(lens) if word == "longest" else min(lens)
        ans = "Pencil " + "ABCD"[lens.index(v)]
        q = fig(pencils_svg(lens)) + "Which pencil is the <b>%s</b>?" % word
        e = ("All the pencils start at the same place. %s ends %s than all the others, so it is the %s. "
             "The answer is <b>%s</b>." % (ans, "further" if word == "longest" else "sooner", word, ans))
        its.append(mcq(q, ans, ["Pencil " + "ABCD"[j] for j in range(4) if lens[j] != v], e))
    return {"title": "Longest and shortest", "items": its}


# ============================================================ set 3: towers
def set_towers(rnd, K):
    its = []
    for a, b, word in [(5, 3, "taller"), (4, 7, "taller"), (6, 2, "shorter"), (3, 5, "shorter"), (6, 6, "taller")]:
        q = fig(towers_svg([a, b])) + "Which tower is <b>%s</b>?" % word
        if a == b:
            ans, e = "They are the same height", "Both towers have %d cubes. <b>They are the same height</b>." % a
        else:
            tall, short = ("Tower A", "Tower B") if a > b else ("Tower B", "Tower A")
            ans = tall if word == "taller" else short
            e = "Tower A has %d cubes. Tower B has %d cubes. %s is taller. The answer is <b>%s</b>." % (a, b, tall, ans)
        ch = ["Tower A", "Tower B", "They are the same height", CANT]
        its.append(mcq(q, ans, [c for c in ch if c != ans], e))
    for hs, word in [([4, 6, 3], "tallest"), ([5, 2, 4], "shortest"), ([3, 7, 5, 6], "tallest"),
                     ([6, 4, 7, 5], "shortest"), ([2, 5, 3, 4], "tallest"), ([7, 6, 4, 8], "shortest"),
                     ([5, 8, 6, 7], "tallest")]:
        v = max(hs) if word == "tallest" else min(hs)
        ans = "Tower " + "ABCD"[hs.index(v)]
        q = fig(towers_svg(hs)) + "Which tower is the <b>%s</b>?" % word
        e = "Count the cubes: %s. %s has %d, so it is the %s. The answer is <b>%s</b>." % (
            ", ".join("%s has %d" % ("ABCD"[j], h) for j, h in enumerate(hs)), ans, v, word, ans)
        wr = ["Tower " + "ABCD"[j] for j in range(len(hs)) if hs[j] != v]
        if len(wr) < 3:
            wr.append("They are the same height")
        its.append(mcq(q, ans, wr, e))
    for a, b in [(5, 3), (4, 7), (8, 6), (3, 6), (7, 3), (2, 5), (6, 5), (4, 8)]:
        tall, short = ("A", "B") if a > b else ("B", "A")
        d = abs(a - b)
        q = fig(towers_svg([a, b])) + "How many more cubes does Tower %s have than Tower %s?" % (tall, short)
        e = ("Tower A has %d cubes. Tower B has %d cubes. Match the cubes from the bottom. "
             "Tower %s has <b>%d</b> more." % (a, b, tall, d))
        its.append(mcq(q, d, [d + 1, d - 1, max(a, b), min(a, b), d + 2], e))
    o = its
    order = [o[0], o[1], o[2], o[12], o[3], o[5], o[13], o[4], o[6], o[14],
             o[7], o[15], o[8], o[16], o[9], o[17], o[10], o[18], o[11], o[19]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Taller and shorter", "items": order}


# ============================================================ set 4: heavier or lighter
def set_balance(rnd, K):
    its = []
    plan = [("apple", "ball", "left", "heavier"), ("cup", "duck", "right", "heavier"),
            ("star", "fish", "left", "lighter"), ("button", "apple", "right", "lighter"),
            ("ball", "cup", "equal", "heavier"), ("duck", "heart", "left", "heavier"),
            ("flower", "bug", "right", "heavier"), ("fish", "star", "right", "lighter"),
            ("heart", "button", "left", "lighter"), ("bug", "flower", "equal", "lighter"),
            ("apple", "duck", "right", "heavier"), ("cup", "ball", "left", "lighter"),
            ("star", "apple", "right", "heavier"), ("fish", "button", "left", "heavier"),
            ("duck", "cup", "right", "lighter"), ("ball", "heart", "equal", "heavier"),
            ("flower", "fish", "left", "lighter"), ("bug", "apple", "left", "heavier"),
            ("button", "star", "right", "lighter"), ("heart", "duck", "right", "heavier")]
    for l, r, tilt, word in plan:
        L, R = "the " + name(l, 1), "the " + name(r, 1)
        q = fig(balance_svg((l, 1), (r, 1), tilt)) + "Which is <b>%s</b>?" % word
        sameans = "They weigh the same"
        if tilt == "equal":
            ans = sameans
            e = "The balance is level. Both sides are the same. <b>They weigh the same</b>."
        else:
            heavy, light = (L, R) if tilt == "left" else (R, L)
            ans = heavy if word == "heavier" else light
            e = ("The heavier side goes down. %s is on the low side, so it is heavier. The answer is <b>%s</b>."
                 % (heavy[0].upper() + heavy[1:], ans))
        ans = ans[0].upper() + ans[1:]
        ch = [L[0].upper() + L[1:], R[0].upper() + R[1:], sameans, CANT]
        its.append(mcq(q, ans, [c for c in ch if c != ans], e.replace("<b>the", "<b>The")))
    return {"title": "Heavier or lighter", "items": its}


# ============================================================ set 5: what we measure
def set_words(rnd, K):
    its = []
    T = [
        ("Which word tells how long something is?", "length", ["weight", "color", "shape"],
         "<b>Length</b> tells how long something is."),
        ("Which word tells how heavy something is?", "weight", ["length", "height", "color"],
         "<b>Weight</b> tells how heavy something is."),
        ("Which word tells how tall something is?", "height", ["weight", "shape", "color"],
         "<b>Height</b> tells how tall something is."),
        ("You want to know if a box is heavy. What do you look at?", "its weight", ["its color", "its shape", "its length"],
         "Heavy or light is about <b>its weight</b>."),
        ("You want to know if a rope is long. What do you look at?", "its length", ["its weight", "its color", "its shape"],
         "Long or short is about <b>its length</b>."),
        ("Which is heavier?", "A car", ["A cup", "A pencil", "A leaf"],
         "A car is very heavy. <b>A car</b> is the heaviest one here."),
        ("Which is lighter?", "A feather", ["A brick", "A dog", "A chair"],
         "A feather is very light. <b>A feather</b> is the lightest one here."),
        ("Which is taller?", "A tree", ["A cat", "A shoe", "A book"],
         "<b>A tree</b> is the tallest one here."),
        ("Which is longer?", "A bus", ["A crayon", "A spoon", "A sock"],
         "<b>A bus</b> is the longest one here."),
        ("Which is heavier?", "A watermelon", ["A grape", "A crayon", "A sticker"],
         "A watermelon is big and full of water. <b>A watermelon</b> is the heaviest one here."),
        ("How do you check which of two pencils is longer?", "Line them up at one end", ["Look at their colors",
         "Put one on top of the other at any place", "Weigh them"],
         "<b>Line them up at one end</b>. Then see which one goes further."),
    ]
    for q, a, w, e in T:
        its.append(mcq(q, a, w, e))
    p = K.next()
    its.append(mcq(fig(pencils_svg([6, 4], labels=["A", "B"], offsets=[0, 3])) +
                   "%s says Pencil B is longer because it ends further right. Is %s right?" % (p["n"], p["he"]),
                   "No, the pencils do not start at the same place",
                   ["Yes, Pencil B is longer", "Yes, they are the same", CANT],
                   "Pencil B starts later. Pencil A has 6 units and Pencil B has 4. "
                   "<b>No, the pencils do not start at the same place</b>, so we must line them up."))
    for l, r, tilt, ask in [("apple", "button", "left", "Which is heavier?"),
                            ("cup", "duck", "equal", "Which is heavier?")]:
        p = K.next()
        q = fig(balance_svg((l, 1), (r, 2), tilt)) + "%s puts 1 %s and 2 %s on a balance. %s" % (
            p["n"], name(l, 1), name(r), ask)
        if tilt == "equal":
            ans, e = "They weigh the same", "The balance is level. 1 %s weighs the same as 2 %s. <b>They weigh the same</b>." % (name(l, 1), name(r))
        else:
            ans, e = "The " + name(l, 1), "The side with the %s goes down. <b>The %s</b> is heavier." % (name(l, 1), name(l, 1))
        ch = ["The " + name(l, 1), "The 2 " + name(r), "They weigh the same", CANT]
        its.append(mcq(q, ans, [c for c in ch if c != ans], e))
    for a, b, word in [(5, 8, "longer"), (7, 4, "shorter")]:
        p, r = K.two()
        q = fig(pencils_svg([a, b], labels=[p["n"], r["n"]])) + \
            "These are the pencils of %s and %s. Whose pencil is %s?" % (p["n"], r["n"], word)
        long_ = p["n"] if a > b else r["n"]
        short = r["n"] if a > b else p["n"]
        ans = long_ if word == "longer" else short
        e = "Both start at the same place. %s’s goes further, so it is longer. The answer is <b>%s</b>." % (long_, ans)
        its.append(mcq(q, ans, [x for x in [p["n"], r["n"], "They are the same length", CANT] if x != ans], e))
    for a, b in [(6, 4), (3, 7), (5, 5)]:
        p, r = K.two()
        q = fig(towers_svg([a, b], labels=[p["n"], r["n"]])) + \
            "%s built the left tower. %s built the right tower. Whose tower is taller?" % (p["n"], r["n"])
        if a == b:
            ans, e = "They are the same height", "Both towers have %d cubes. <b>They are the same height</b>." % a
        else:
            ans = p["n"] if a > b else r["n"]
            e = "%s’s tower has %d cubes. %s’s has %d. <b>%s</b>’s tower is taller." % (p["n"], a, r["n"], b, ans)
        its.append(mcq(q, ans, [x for x in [p["n"], r["n"], "They are the same height", CANT] if x != ans], e))
    p = K.next()
    its.append(mcq(fig(balance_svg(("ball", 1), ("apple", 1), "right")) +
                   "%s says the ball is heavier because it is up high. Is %s right?" % (p["n"], p["he"]),
                   "No, the apple is heavier", ["Yes, the ball is heavier", "They weigh the same", CANT],
                   "The heavier side goes <b>down</b>. The apple is down. <b>No, the apple is heavier</b>."))
    o = its
    order = [o[0], o[1], o[2], o[5], o[6], o[7], o[8], o[10], o[3], o[4],
             o[14], o[12], o[16], o[9], o[15], o[17], o[11], o[13], o[18], o[19]]
    assert len(o) == 20 and len({id(x) for x in order}) == 20
    return {"title": "What we measure", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Things we can measure</h2>"
        + table(["Word", "It tells", "Compare with"], [
            ["Length", "how long", "longer, shorter"],
            ["Height", "how tall", "taller, shorter"],
            ["Weight", "how heavy", "heavier, lighter"],
        ]) +
        "<h2>Compare length: line them up</h2>"
        "<p>Put both things at the <b>same starting line</b>. The one that goes further is longer.</p>"
        "<figure class='sn-fig'>" + pencils_svg([5, 7]) + "<figcaption>Pencil B is longer. Pencil A is shorter.</figcaption></figure>"
        "<h2>Compare height</h2>"
        "<figure class='sn-fig'>" + towers_svg([5, 3]) + "<figcaption>Tower A is taller. It has 2 more cubes.</figcaption></figure>"
        "<h2>Compare weight with a balance</h2>"
        "<p>The <b>heavier</b> side goes <b>down</b>. If the balance is level, they weigh the same.</p>"
        "<figure class='sn-fig'>" + balance_svg(("apple", 1), ("ball", 1), "left") + "<figcaption>The apple is heavier. The ball is lighter.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Not lining up the ends", "Start both at the same line"],
            ["Thinking the high side is heavier", "The heavier side goes down"],
            ["Thinking bigger is always heavier", "Use a balance to check"],
        ])
    )


FAQ = [
    {"q": "What do kindergartners learn about measurement?",
     "a": "They learn that things have length, height and weight. They compare two things directly and use words like longer, shorter, taller, heavier and lighter."},
    {"q": "Do kindergartners use rulers?",
     "a": "Not yet. In kindergarten they compare by lining things up side by side. Measuring with units like cubes or inches starts in Grade 1."},
    {"q": "How does a pan balance show which is heavier?",
     "a": "The heavier side goes down and the lighter side goes up. When the two sides are level, the things weigh the same."},
    {"q": "How can I practice at home?",
     "a": "Compare spoons, shoes or toys. Ask: Which is longer? How do you know? Hold two things, one in each hand, and guess which is heavier."},
]


def gen():
    rnd = random.Random(2011)
    K = Kids(rnd)
    sets = [set_two(rnd, K), set_four(rnd, K), set_towers(rnd, K), set_balance(rnd, K), set_words(rnd, K)]
    finish(sets, rnd, max_num=10)
    return {
        "slug": "compare-length-and-weight", "sort": 11, "updated": UPDATED, "pdf_url": "",
        "title": "Compare Length, Height and Weight",
        "seo_title": "Kindergarten Measurement Worksheets: Longer, Shorter, Taller, Heavier, Lighter",
        "short_title": "Length and Weight",
        "domain": "Measurement and Data",
        "standard_code": "K.MD.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/MD/A/2/",
        "standard_text": "Directly compare two objects with a measurable attribute in common, to see which object has "
                         "“more of”/“less of” the attribute, and describe the difference. For example, directly compare "
                         "the heights of two children and describe one child as taller/shorter.",
        "meta_desc": "Free kindergarten measurement worksheets: compare length (longer, shorter), height (taller), and "
                     "weight on a pan balance (heavier, lighter), find the longest and shortest, and learn the words. "
                     "100 picture questions with an answer key.",
        "key_big": "Line things up at one end to compare length. The heavier side of a balance goes down.",
        "key_sub": "Length tells how long, height how tall, and weight how heavy.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
