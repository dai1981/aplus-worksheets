# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Addition Within 10 (K.OA.A.1, K.OA.A.2)
  python3 tools/gen_us_math_gk_addition_within_10.py
Put two groups together, add with two-colour ten-frames, hop on a number line,
match a picture with its number sentence, and solve short addition stories.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import name, two_groups_svg, tenframe_mix_svg, hop_line_svg, KINDS
from k_common import Kids, mcq, lst, finish

UPDATED = "2026-11-16"


def wrongs(a, b):
    s = a + b
    return [s - 1, s + 1, max(a, b), abs(a - b) or None, s + 2]


def count_on_e(a, b, what=""):
    s = a + b
    return "Start at %d and count on %d: %s. %d + %d = <b>%d</b>%s." % (
        a, b, lst(a + 1, s), a, b, s, (" " + what) if what else "")


# ============================================================ set 1: put together
def set_groups(rnd, K):
    plan = [(1, 1), (2, 1), (1, 3), (2, 2), (3, 1), (2, 3), (4, 1), (3, 3), (1, 5), (4, 2),
            (5, 2), (3, 4), (2, 6), (5, 3), (4, 4), (6, 3), (7, 2), (5, 5), (3, 6), (4, 6)]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = []
    for i, (a, b) in enumerate(plan):
        kind = kinds[i % len(kinds)]
        svg = two_groups_svg(a, kind, b, word="and")
        q = "%d %s and %d %s. How many %s in all?" % (a, name(kind, a), b, name(kind, b), name(kind))
        e = "Put them together and count all: %s. There are <b>%d</b> %s in all." % (lst(1, a + b), a + b, name(kind))
        its.append(mcq(fig(svg) + q, a + b, wrongs(a, b), e))
    return {"title": "Put together", "items": its}


# ============================================================ set 2: ten-frames
def set_frames(rnd, K):
    plan = [(2, 1), (3, 2), (1, 4), (4, 3), (5, 1), (2, 5), (6, 2), (3, 5), (5, 4), (4, 4),
            (7, 1), (6, 3), (2, 7), (5, 5), (8, 2), (3, 7), (6, 4), (1, 8), (4, 5), (7, 3)]
    its = []
    for i, (a, b) in enumerate(plan):
        svg = tenframe_mix_svg(["r"] * a + ["b"] * b)
        if i % 2 == 0:
            q = "%d red dots and %d blue dots. How many dots in all?" % (a, b)
        else:
            q = "Look at the ten-frame. %d + %d = ?" % (a, b)
        s = a + b
        if s == 10:
            e = "%d red and %d blue fill the ten-frame. A full ten-frame is 10. %d + %d = <b>10</b>." % (a, b, a, b)
        else:
            e = count_on_e(a, b)
        its.append(mcq(fig(svg) + q, s, wrongs(a, b), e))
    return {"title": "Add with ten-frames", "items": its}


# ============================================================ set 3: number line
def set_line(rnd, K):
    plan = [(1, 2), (3, 1), (2, 2), (4, 1), (2, 3), (5, 2), (3, 3), (6, 1), (4, 3), (1, 5),
            (6, 2), (5, 3), (2, 6), (7, 2), (4, 4), (3, 5), (6, 3), (8, 2), (5, 4), (2, 8)]
    its = []
    for i, (a, b) in enumerate(plan):
        svg = hop_line_svg(a, b)
        s = a + b
        q = ("Start at %d. Make %d %s of 1. Where do you land?" % (a, b, "jump" if b == 1 else "jumps")) if i % 2 == 0 else \
            ("Use the number line. %d + %d = ?" % (a, b))
        e = ("Start at %d (the red dot). Make %d %s: %s. You land on <b>%d</b>. "
             "Do not count the start." % (a, b, "jump" if b == 1 else "jumps", lst(a + 1, s), s))
        its.append(mcq(fig(svg) + q, s, [s - 1, s + 1, b, a + b + 2], e))
    return {"title": "Add on a number line", "items": its}


# ============================================================ set 4: number sentences
def set_sentences(rnd, K):
    plan = [(2, 1), (1, 3), (3, 2), (2, 4), (4, 1), (3, 3), (5, 2), (1, 6), (4, 3), (6, 2),
            (2, 5), (5, 4), (3, 6), (7, 3), (4, 4), (2, 7), (6, 4), (5, 3), (8, 1), (3, 7)]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = []
    for i, (a, b) in enumerate(plan):
        kind = kinds[i % len(kinds)]
        s = a + b
        svg = two_groups_svg(a, kind, b, word="+")
        right = "%d + %d = %d" % (a, b, s)
        wr = ["%d + %d = %d" % (a, b + 1, s + 1) if s < 10 else "%d + %d = %d" % (a, b - 1, s - 1),
              "%d − %d = %d" % (max(a, b), min(a, b), max(a, b) - min(a, b)) if a != b else "%d + %d = %d" % (a, a, s + 1),
              "%d + %d = %d" % (a, b, s - 1)]
        if a + 1 + b <= 10:
            wr.append("%d + %d = %d" % (a + 1, b, s + 1))
        q = "Which number sentence matches the picture?"
        e = ("There %s %d %s and %d more. %d and %d make %d. The sentence is <b>%s</b>."
             % ("is" if a == 1 else "are", a, name(kind, a), b, a, b, s, right))
        its.append(mcq(fig(svg) + q, right, wr, e, allow_zero=True))
    return {"title": "Number sentences", "items": its}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []

    def story(a, b, kind, text, unit=None):
        p = K.next()
        t = text.format(a=a, b=b, **p)
        s = a + b
        svg = two_groups_svg(a, kind, b, word="and")
        u = unit or name(kind)
        e = "%d and %d more make %d. %d + %d = %d. The answer is <b>%d %s</b>." % (a, b, s, a, b, s, s, u if s != 1 else name(kind, 1))
        its.append(mcq(fig(svg) + t, "%d %s" % (s, u), ["%d %s" % (w, u) for w in wrongs(a, b) if w], e))

    story(2, 1, "duck", "{a} ducks are in a pond. {b} more duck comes. How many ducks are there now?")
    story(3, 2, "apple", "{n} has {a} apples. {He} picks {b} more. How many apples does {he} have now?")
    story(1, 4, "ball", "{n} has {a} ball. A friend gives {n} {b} more balls. How many balls does {n} have now?")
    story(4, 2, "bug", "{a} ladybugs sit on a leaf. {b} more land on it. How many ladybugs are on the leaf?")
    story(3, 3, "fish", "{n} sees {a} fish. Then {he} sees {b} more fish. How many fish does {he} see in all?")
    story(5, 1, "star", "{n} gets {a} stars on Monday and {b} star on Tuesday. How many stars does {he} get in all?")
    story(2, 5, "flower", "{n} picks {a} flowers. Then {he} picks {b} more. How many flowers does {he} pick in all?")
    story(4, 3, "cup", "There are {a} cups on the table. {n} puts out {b} more. How many cups are there now?")
    story(6, 2, "heart", "{n} draws {a} hearts. Then {he} draws {b} more. How many hearts does {he} draw in all?")
    story(5, 3, "button", "A coat has {a} buttons. A shirt has {b} buttons. How many buttons is that in all?")
    story(3, 5, "duck", "{a} ducks swim. {b} ducks walk. How many ducks are there in all?")
    story(7, 2, "apple", "{a} apples are in a bowl. {n} puts in {b} more. How many apples are in the bowl now?")
    story(4, 4, "ball", "{n} has {a} balls. {He} gets {b} more. How many balls does {he} have now?")
    story(6, 3, "fish", "{a} fish are in one tank. {b} fish are in another. How many fish are there in all?")
    story(2, 7, "star", "{n} has {a} stars. {He} gets {b} more. How many stars does {he} have now?")
    story(5, 5, "cup", "{n} stacks {a} cups. Then {he} stacks {b} more. How many cups are in the stack?")
    story(8, 1, "bug", "{a} ladybugs are on a rock. {b} more ladybug comes. How many ladybugs are there now?")
    story(3, 6, "flower", "{n} plants {a} flowers. {His} dad plants {b} more. How many flowers are there now?")
    story(7, 3, "heart", "{n} has {a} heart stickers. {He} gets {b} more. How many heart stickers does {he} have?",
          unit="stickers")
    story(6, 4, "button", "{n} finds {a} buttons. Then {he} finds {b} more. How many buttons does {he} find in all?")
    return {"title": "Addition stories", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Adding means putting together</h2>"
        "<p>Put two groups together. Count them all. That is the <b>sum</b>.</p>"
        "<figure class='sn-fig'>" + two_groups_svg(3, "apple", 2, word="+")
        + "<figcaption>3 apples and 2 apples: 3 + 2 = 5.</figcaption></figure>"
        "<h2>Count on</h2>"
        "<p>Start with the first number. Count on the second number.</p>"
        "<figure class='sn-fig'>" + tenframe_mix_svg(["r"] * 4 + ["b"] * 3)
        + "<figcaption>4 red. Count on 3 blue: 5, 6, 7. So 4 + 3 = 7.</figcaption></figure>"
        "<h2>Hop on a number line</h2>"
        "<figure class='sn-fig'>" + hop_line_svg(5, 2)
        + "<figcaption>Start at 5. Hop 2: 6, 7. So 5 + 2 = 7.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Counting the start on a number line", "Count the hops, not the start"],
            ["Saying only the bigger number", "Count both groups"],
            ["Taking away instead of adding", "“More” and “in all” mean add"],
        ])
    )


FAQ = [
    {"q": "How do kindergartners learn to add?",
     "a": "They put two groups of objects together and count them all. Then they learn to count on from the first number. Fingers, blocks and ten-frames all help."},
    {"q": "What is a ten-frame?",
     "a": "It is a box with 2 rows of 5. Children put counters in it to see numbers. Two colours show the two parts of an addition, like 4 red and 3 blue make 7."},
    {"q": "Should my child know addition facts by heart?",
     "a": "In kindergarten, children add within 10 with objects or drawings. Only facts within 5 should be quick. Fast recall of facts to 20 comes in Grade 1 and 2."},
    {"q": "Which words mean add in a story?",
     "a": "Words like more, in all, and, together and now (after more come) often mean add. But read the whole story and act it out, because key words can trick you."},
]


def gen():
    rnd = random.Random(2005)
    K = Kids(rnd)
    sets = [set_groups(rnd, K), set_frames(rnd, K), set_line(rnd, K), set_sentences(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=12)
    return {
        "slug": "addition-within-10", "sort": 5, "updated": UPDATED, "pdf_url": "",
        "title": "Addition Within 10: Put Together and Count On",
        "seo_title": "Kindergarten Addition Worksheets Within 10: Pictures, Ten-Frames, Number Lines",
        "short_title": "Addition Within 10",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "K.OA.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/OA/A/2/",
        "standard_text": "Solve addition and subtraction word problems, and add and subtract within 10, e.g., by using "
                         "objects or drawings to represent the problem.",
        "meta_desc": "Free kindergarten addition worksheets within 10: put two groups together, add with two-colour "
                     "ten-frames, hop on a number line, match pictures with number sentences, and solve addition "
                     "stories. 100 picture questions with an answer key.",
        "key_big": "Adding is putting together. Start with one number and count on.",
        "key_sub": "3 and 2 more make 5: 3 + 2 = 5. Words like more and in all often mean add.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
