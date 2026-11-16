# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Subtraction Within 10 (K.OA.A.1, K.OA.A.2)
  python3 tools/gen_us_math_gk_subtraction_within_10.py
Take away (cross out), subtract with ten-frames, hop back on a number line,
match a picture with its number sentence, and solve short take-away stories.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import name, crossed_row_svg, tenframe_mix_svg, hop_line_svg, KINDS
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"


def wrongs(a, b):
    d = a - b
    return [d + 1, d - 1, a + b, b if b != d else None, a, d + 2]


def back(a, b):
    return ", ".join(str(a - k) for k in range(1, b + 1))


PLAN1 = [(3, 1), (4, 1), (3, 2), (4, 3), (4, 2), (5, 2), (5, 1), (5, 3), (6, 2), (6, 4),
         (7, 1), (7, 3), (6, 3), (8, 2), (7, 5), (8, 3), (9, 4), (8, 6), (9, 2), (10, 3)]


# ============================================================ set 1: take away
def set_cross(rnd, K):
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = []
    for i, (a, b) in enumerate(PLAN1):
        kind = kinds[i % len(kinds)]
        svg = crossed_row_svg(a, kind, b)
        q = "There are %d %s. %d %s crossed out. How many are left?" % (
            a, name(kind), b, "is" if b == 1 else "are")
        d = a - b
        e = ("Count the ones that are not crossed out: %s. %d take away %d is %d. There %s <b>%d</b> left."
             % (", ".join(str(k) for k in range(1, d + 1)), a, b, d, "is" if d == 1 else "are", d))
        its.append(mcq(fig(svg) + q, d, wrongs(a, b), e))
    return {"title": "Take away", "items": its}


# ============================================================ set 2: ten-frames
def set_frames(rnd, K):
    plan = [(3, 1), (4, 2), (5, 1), (5, 4), (6, 1), (6, 5), (7, 2), (7, 4), (8, 1), (8, 4),
            (8, 5), (9, 3), (9, 1), (9, 5), (10, 1), (10, 4), (10, 2), (9, 7), (10, 6), (10, 8)]
    its = []
    for i, (a, b) in enumerate(plan):
        svg = tenframe_mix_svg(["r"] * (a - b) + ["x"] * b)
        d = a - b
        q = ("%d dots. %d %s crossed out. How many dots are left?" % (a, b, "is" if b == 1 else "are")) if i % 2 == 0 \
            else "Look at the ten-frame. %d − %d = ?" % (a, b)
        e = "There are %d dots. Take away the %d crossed out. %d are left. %d − %d = <b>%d</b>." % (a, b, d, a, b, d)
        if d == 1:
            e = "There are %d dots. Take away the %d crossed out. 1 is left. %d − %d = <b>1</b>." % (a, b, a, b)
        its.append(mcq(fig(svg) + q, d, wrongs(a, b), e))
    return {"title": "Subtract with ten-frames", "items": its}


# ============================================================ set 3: number line
def set_line(rnd, K):
    plan = [(3, 1), (4, 2), (5, 1), (5, 2), (6, 3), (7, 1), (6, 2), (8, 2), (7, 3), (9, 1),
            (8, 3), (9, 2), (10, 2), (7, 4), (9, 3), (10, 3), (8, 4), (10, 4), (9, 5), (10, 5)]
    its = []
    for i, (a, b) in enumerate(plan):
        svg = hop_line_svg(a, -b)
        d = a - b
        q = ("Start at %d. Make %d %s back. Where do you land?" % (a, b, "hop" if b == 1 else "hops")) if i % 2 == 0 \
            else "Use the number line. %d − %d = ?" % (a, b)
        e = ("Start at %d (the red dot). Hop back %d: %s. You land on <b>%d</b>. Do not count the start."
             % (a, b, back(a, b), d))
        its.append(mcq(fig(svg) + q, d, [d + 1, d - 1, a + b, b if b != d else None, d + 2], e))
    return {"title": "Hop back on a number line", "items": its}


# ============================================================ set 4: number sentences
def set_sentences(rnd, K):
    plan = [(3, 1), (4, 1), (4, 3), (5, 2), (5, 4), (6, 1), (6, 3), (7, 2), (7, 5), (8, 1),
            (8, 3), (8, 7), (9, 2), (9, 4), (9, 6), (10, 1), (10, 3), (10, 5), (10, 7), (6, 4)]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = []
    for i, (a, b) in enumerate(plan):
        kind = kinds[i % len(kinds)]
        d = a - b
        svg = crossed_row_svg(a, kind, b)
        right = "%d − %d = %d" % (a, b, d)
        wr = ["%d + %d = %d" % (a, b, a + b) if a + b <= 10 else "%d − %d = %d" % (a, b, d + 1),
              "%d − %d = %d" % (a, b, d + 1),
              "%d − %d = %d" % (a, d, b) if d != b else "%d − %d = %d" % (a, b, d - 1),
              "%d − %d = %d" % (a, b, d - 1),
              "%d − %d = %d" % (a - 1, b, d)]
        q = "Which number sentence matches the picture?"
        e = ("There %s %d %s. %d %s crossed out. %d %s left. The sentence is <b>%s</b>."
             % ("is" if a == 1 else "are", a, name(kind, a), b, "is" if b == 1 else "are", d,
                "is" if d == 1 else "are", right))
        its.append(mcq(fig(svg) + q, right, wr, e, allow_zero=True))
    return {"title": "Number sentences", "items": its}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []

    def story(a, b, kind, text, unit=None):
        p = K.next()
        t = text.format(a=a, b=b, **p)
        d = a - b
        svg = crossed_row_svg(a, kind, b)
        u1, u = unit or (name(kind, 1), name(kind))
        e = "%d take away %d is %d. %d − %d = %d. The answer is <b>%d %s</b>." % (a, b, d, a, b, d, d, u1 if d == 1 else u)
        unit = lambda v: "%d %s" % (v, u1 if v == 1 else u)
        its.append(mcq(fig(svg) + t, unit(d), [unit(w) for w in wrongs(a, b) if w and w > 0], e))

    story(3, 1, "apple", "{n} has {a} apples. {He} eats {b}. How many apples are left?")
    story(4, 2, "duck", "{a} ducks are in a pond. {b} swim away. How many ducks are still in the pond?")
    story(5, 1, "ball", "{n} has {a} balls. {He} gives {b} to a friend. How many balls does {he} have now?")
    story(5, 3, "bug", "{a} ladybugs sit on a leaf. {b} fly away. How many ladybugs are left?")
    story(6, 2, "cup", "There are {a} cups. {n} breaks {b}. How many cups are not broken?")
    story(6, 4, "star", "{n} has {a} star stickers. {He} uses {b}. How many stickers are left?",
          unit=("sticker", "stickers"))
    story(7, 3, "fish", "{a} fish are in a tank. {n} moves {b} to a new tank. How many fish are in the first tank now?")
    story(7, 1, "flower", "{n} picks {a} flowers. {He} gives {b} to {his} mom. How many flowers does {he} have now?")
    story(8, 2, "heart", "{n} draws {a} hearts. {He} erases {b}. How many hearts are left?")
    story(8, 5, "button", "{n} has {a} buttons. {He} loses {b}. How many buttons does {he} have now?")
    story(9, 3, "apple", "There are {a} apples on a tree. {b} fall down. How many apples are still on the tree?")
    story(6, 5, "duck", "{a} ducks are on the grass. {b} go into the water. How many ducks are still on the grass?")
    story(9, 6, "ball", "{n} has {a} balls. {b} roll away. How many balls are left?")
    story(10, 2, "bug", "{a} ladybugs are on a rock. {b} fly away. How many are still on the rock?")
    story(10, 4, "cup", "{n} sets out {a} cups. {b} kids take a cup. How many cups are left?")
    story(8, 4, "star", "There are {a} stars on a chart. {n} takes off {b}. How many stars are still on the chart?")
    story(10, 7, "fish", "{n} catches {a} fish. {He} lets {b} go. How many fish does {he} keep?")
    story(9, 8, "flower", "{a} flowers are in a vase. {b} are taken out. How many flowers are left in the vase?")
    story(7, 4, "heart", "{n} has {a} heart stickers. {He} gives away {b}. How many does {he} have left?",
          unit=("sticker", "stickers"))
    story(10, 5, "button", "A shirt has {a} buttons. {b} come off. How many buttons are still on the shirt?")
    return {"title": "Take-away stories", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Subtracting means taking away</h2>"
        "<p>Start with a group. Take some away. Count what is <b>left</b>.</p>"
        "<figure class='sn-fig'>" + crossed_row_svg(5, "apple", 2)
        + "<figcaption>5 apples. 2 are eaten. 3 are left: 5 − 2 = 3.</figcaption></figure>"
        "<h2>Use a ten-frame</h2>"
        "<figure class='sn-fig'>" + tenframe_mix_svg(["r"] * 5 + ["x"] * 3)
        + "<figcaption>8 dots. Cross out 3. 5 are left: 8 − 3 = 5.</figcaption></figure>"
        "<h2>Hop back on a number line</h2>"
        "<figure class='sn-fig'>" + hop_line_svg(7, -2)
        + "<figcaption>Start at 7. Hop back 2: 6, 5. So 7 − 2 = 5.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Adding instead of taking away", "“Left”, “away” and “eats” mean take away"],
            ["Counting the crossed-out ones", "Count only the ones that are left"],
            ["Counting the start on a number line", "Count the hops back, not the start"],
        ])
    )


FAQ = [
    {"q": "How do kindergartners learn to subtract?",
     "a": "They start with a group of objects, take some away and count what is left. Acting out stories with toys and crossing out pictures both help."},
    {"q": "Is the minus sign used in kindergarten?",
     "a": "Yes. Children read and write simple sentences like 5 − 2 = 3. They should also say it in words: 5 take away 2 is 3."},
    {"q": "Why does my child add when the story says take away?",
     "a": "Many children see two numbers and add them. Ask them to act out the story first: Do we have more now or less? Then choose add or take away."},
    {"q": "How far should kindergartners subtract?",
     "a": "Within 10, using objects, fingers or drawings. Quick recall is only expected within 5. Subtracting within 20 comes in Grade 1."},
]


def gen():
    rnd = random.Random(2006)
    K = Kids(rnd)
    sets = [set_cross(rnd, K), set_frames(rnd, K), set_line(rnd, K), set_sentences(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=20)
    return {
        "slug": "subtraction-within-10", "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Subtraction Within 10: Take Away and Count What Is Left",
        "seo_title": "Kindergarten Subtraction Worksheets Within 10: Take Away, Ten-Frames, Number Lines",
        "short_title": "Subtraction Within 10",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "K.OA.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/OA/A/1/",
        "standard_text": "Represent addition and subtraction with objects, fingers, mental images, drawings, sounds "
                         "(e.g., claps), acting out situations, verbal explanations, expressions, or equations.",
        "meta_desc": "Free kindergarten subtraction worksheets within 10: take away and cross out, subtract with "
                     "ten-frames, hop back on a number line, match pictures with number sentences, and solve "
                     "take-away stories. 100 picture questions with an answer key.",
        "key_big": "Subtracting is taking away. Count what is left.",
        "key_sub": "5 take away 2 is 3: 5 − 2 = 3. Words like left, away and eats often mean take away.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
