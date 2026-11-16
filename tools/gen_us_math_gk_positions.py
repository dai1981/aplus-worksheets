# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Positions - Above, Below, Next To, In Front Of, Behind (K.G.A.1)
  python3 tools/gen_us_math_gk_positions.py
Describe where things are: above and below (table, shelves), next to and between (a row),
in front of and behind (a box), turn the sentence around, and name shapes by where they are.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import (name, table_scene_svg, box_scene_svg, shelf_svg, kinds_row_svg, shapes_scene_svg, KINDS)
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"
T_REL = {"above": "above the table", "below": "below the table", "beside": "next to the table"}
B_REL = {"front": "in front of the box", "behind": "behind the box", "beside": "next to the box", "above": "above the box"}
T_WHY = {"above": "The %s is higher than the table and not touching it. It is <b>above the table</b>.",
         "below": "The %s is under the table top. It is <b>below the table</b>.",
         "beside": "The %s is at the side of the table. It is <b>next to the table</b>."}
B_WHY = {"front": "The %s covers part of the box, so it is closer to you. It is <b>in front of the box</b>.",
         "behind": "The box covers part of the %s, so it is farther away. It is <b>behind the box</b>.",
         "beside": "The %s is at the side of the box. It is <b>next to the box</b>.",
         "above": "The %s is higher than the box. It is <b>above the box</b>."}


def the(k):
    return "the " + name(k, 1)


# ============================================================ set 1: above and below
def set_above(rnd, K):
    its = []
    for kind, rel in [("ball", "above"), ("duck", "below"), ("star", "above"), ("cup", "below"), ("bug", "below"),
                      ("heart", "above"), ("fish", "below"), ("flower", "above")]:
        ch = ["Above the table", "Below the table", "Next to the table", "In front of the table"]
        ans = T_REL[rel][0].upper() + T_REL[rel][1:]
        its.append(mcq(fig(table_scene_svg(kind, rel)) + "Where is the %s?" % name(kind, 1), ans,
                       [c for c in ch if c != ans], T_WHY[rel] % name(kind, 1)))
    for kinds, ask, ref in [(["apple", "cup", "duck"], "above", "cup"), (["star", "ball", "fish"], "below", "ball"),
                            (["heart", "bug", "flower"], "above", "flower"), (["cup", "apple", "star"], "below", "cup"),
                            (["duck", "fish", "button"], "above", "fish"), (["ball", "heart", "bug"], "below", "heart"),
                            (["flower", "star", "cup"], "above", "cup"), (["fish", "duck", "apple"], "below", "fish")]:
        i = kinds.index(ref)
        tgt = kinds[i - 1] if ask == "above" else kinds[i + 1]
        others = [k for k in kinds if k != tgt]
        ans = the(tgt).capitalize()
        ch = [the(k).capitalize() for k in others] + ["The " + name([k for k in KINDS if k not in kinds][0], 1)]
        e = "Look at the %s. The shelf just %s it has <b>%s</b>." % (name(ref, 1), ask, the(tgt))
        its.append(mcq(fig(shelf_svg(kinds)) + "What is just <b>%s</b> the %s?" % (ask, name(ref, 1)), ans, ch, e))
    for kinds, where in [(["apple", "duck", "cup"], "top"), (["ball", "star", "fish"], "bottom"),
                         (["bug", "heart", "flower"], "middle"), (["cup", "button", "apple"], "bottom")]:
        tgt = {"top": kinds[0], "middle": kinds[1], "bottom": kinds[2]}[where]
        ans = the(tgt).capitalize()
        ch = [the(k).capitalize() for k in kinds if k != tgt] + ["The " + name([k for k in KINDS if k not in kinds][1], 1)]
        e = "The %s shelf has <b>%s</b>." % (where, the(tgt))
        its.append(mcq(fig(shelf_svg(kinds)) + "What is on the <b>%s</b> shelf?" % where, ans, ch, e))
    o = its
    order = [o[0], o[1], o[16], o[2], o[3], o[8], o[17], o[4], o[9], o[10],
             o[5], o[18], o[11], o[12], o[6], o[19], o[13], o[7], o[14], o[15]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Above and below", "items": order}


# ============================================================ set 2: next to and between
def set_next(rnd, K):
    its = []
    rows = [["apple", "duck", "star", "cup"], ["ball", "fish", "heart", "bug"], ["flower", "cup", "apple", "star"],
            ["duck", "button", "ball", "heart"], ["bug", "star", "fish", "apple"], ["cup", "heart", "duck", "flower"],
            ["star", "apple", "bug", "ball"], ["fish", "flower", "button", "duck"]]
    for i, kinds in enumerate(rows):
        end = kinds[0] if i % 2 == 0 else kinds[-1]
        nb = kinds[1] if i % 2 == 0 else kinds[-2]
        ans = the(nb).capitalize()
        ch = [the(k).capitalize() for k in kinds if k not in (nb,)]
        e = "The %s is at the end of the row. Only one thing is beside it: <b>%s</b>." % (name(end, 1), the(nb))
        its.append(mcq(fig(kinds_row_svg(kinds)) + "What is <b>next to</b> the %s?" % name(end, 1), ans, ch, e))
    for i, kinds in enumerate(rows):
        a, b = (kinds[0], kinds[2]) if i % 2 == 0 else (kinds[1], kinds[3])
        mid = kinds[1] if i % 2 == 0 else kinds[2]
        ans = the(mid).capitalize()
        ch = [the(k).capitalize() for k in kinds if k != mid]
        e = "Find the %s and the %s. The one in the middle is <b>%s</b>." % (name(a, 1), name(b, 1), the(mid))
        its.append(mcq(fig(kinds_row_svg(kinds)) + "What is <b>between</b> the %s and the %s?" % (name(a, 1), name(b, 1)),
                       ans, ch, e))
    for kind, rel in [("cup", "beside"), ("ball", "beside"), ("bug", "beside"), ("apple", "beside")]:
        ch = ["Next to the table", "Above the table", "Below the table", "Behind the table"]
        its.append(mcq(fig(table_scene_svg(kind, rel)) + "Where is the %s?" % name(kind, 1), "Next to the table",
                       [c for c in ch if c != "Next to the table"], T_WHY[rel] % name(kind, 1)))
    o = its
    order = [o[0], o[16], o[1], o[8], o[2], o[17], o[9], o[3], o[10], o[18],
             o[4], o[11], o[5], o[12], o[19], o[6], o[13], o[7], o[14], o[15]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Next to and between", "items": order}


# ============================================================ set 3: in front of and behind
def set_front(rnd, K):
    its = []
    plan = [("ball", "front"), ("duck", "behind"), ("star", "front"), ("cup", "behind"), ("apple", "beside"),
            ("bug", "behind"), ("heart", "front"), ("fish", "behind"), ("flower", "front"), ("ball", "above"),
            ("button", "behind"), ("duck", "front"), ("star", "behind"), ("cup", "front"), ("apple", "behind"),
            ("bug", "front"), ("heart", "above"), ("fish", "front"), ("flower", "behind"), ("button", "beside")]
    for kind, rel in plan:
        ch = ["In front of the box", "Behind the box", "Next to the box", "Above the box"]
        ans = B_REL[rel][0].upper() + B_REL[rel][1:]
        its.append(mcq(fig(box_scene_svg(kind, rel)) + "Where is the %s?" % name(kind, 1), ans,
                       [c for c in ch if c != ans], B_WHY[rel] % name(kind, 1)))
    return {"title": "In front of and behind", "items": its}


# ============================================================ set 4: turn it around
def set_turn(rnd, K):
    its = []
    for kind, rel, q, ans, wr, e in [
        ("ball", "above", "The ball is above the table. Where is the table?", "Below the ball",
         ["Above the ball", "Next to the ball", "Behind the ball"], "If the ball is above the table, the table is <b>below the ball</b>."),
        ("duck", "below", "The duck is below the table. Where is the table?", "Above the duck",
         ["Below the duck", "Next to the duck", "In front of the duck"], "If the duck is below the table, the table is <b>above the duck</b>."),
        ("star", "above", "The star is above the table. What is below the star?", "The table",
         ["The floor only", "Nothing", "The sky"], "The star is above the table, so <b>the table</b> is below the star."),
        ("cup", "below", "Is the cup above or below the table?", "Below",
         ["Above", "Next to", "Behind"], "The cup is under the table top. It is <b>below</b>."),
        ("heart", "above", "Is the heart above or below the table?", "Above",
         ["Below", "Next to", "Behind"], "The heart is higher than the table. It is <b>above</b>."),
    ]:
        its.append(mcq(fig(table_scene_svg(kind, rel)) + q, ans, wr, e))
    for kind, rel, q, ans, wr, e in [
        ("ball", "front", "The ball is in front of the box. Where is the box?", "Behind the ball",
         ["In front of the ball", "Above the ball", "Below the ball"], "If the ball is in front of the box, the box is <b>behind the ball</b>."),
        ("duck", "behind", "The duck is behind the box. Where is the box?", "In front of the duck",
         ["Behind the duck", "Above the duck", "Below the duck"], "If the duck is behind the box, the box is <b>in front of the duck</b>."),
        ("bug", "behind", "Can you see all of the ladybug?", "No, the box hides part of it",
         ["Yes, all of it", "No, it is in the box", "Yes, it is above the box"],
         "The ladybug is behind the box. <b>No, the box hides part of it</b>."),
        ("star", "above", "Is the star above or in front of the box?", "Above",
         ["In front of", "Behind", "Below"], "The star is higher than the box. It is <b>above</b> the box."),
        ("apple", "front", "Is the apple in front of or behind the box?", "In front of",
         ["Behind", "Above", "Below"], "The apple covers part of the box. It is <b>in front of</b> the box."),
    ]:
        its.append(mcq(fig(box_scene_svg(kind, rel)) + q, ans, wr, e))
    for kinds, q, ans, wr, e in [
        (["apple", "cup", "duck"], "The cup is between two things. What is above it?", "The apple",
         ["The duck", "The cup", "The star"], "The apple is on the shelf just above the cup. The answer is <b>the apple</b>."),
        (["star", "ball", "fish"], "Which thing has nothing above it?", "The star",
         ["The ball", "The fish", "The duck"], "The star is on the top shelf. <b>The star</b> has nothing above it."),
        (["heart", "bug", "flower"], "Which thing has nothing below it?", "The flower",
         ["The heart", "The ladybug", "The cup"], "The flower is on the bottom shelf. <b>The flower</b> has nothing below it."),
        (["cup", "button", "duck"], "The button is ___ the cup.", "below",
         ["above", "behind", "in front of"], "The cup is on the top shelf. The button is lower. It is <b>below</b> the cup."),
        (["fish", "apple", "star"], "The fish is ___ the star.", "above",
         ["below", "next to", "behind"], "The fish is on the top shelf. The star is at the bottom. The fish is <b>above</b> the star."),
    ]:
        its.append(mcq(fig(shelf_svg(kinds)) + q, ans, wr, e))
    for kinds, q, ans, wr, e in [
        (["duck", "apple", "cup", "star"], "The apple is next to the duck and the ___.", "cup",
         ["star", "duck", "ball"], "The apple is between the duck and the cup. It is next to both. The answer is <b>cup</b>."),
        (["ball", "heart", "fish", "bug"], "How many things are next to the heart?", "2",
         ["1", "3", "4"], "The ball is on one side and the fish is on the other. That is <b>2</b>."),
        (["star", "flower", "button", "cup"], "How many things are next to the star?", "1",
         ["2", "3", "4"], "The star is at the end. Only the flower is next to it. That is <b>1</b>."),
        (["bug", "duck", "apple", "ball"], "What is between the duck and the ball?", "The apple",
         ["The ladybug", "The duck", "The ball"], "<b>The apple</b> is in the middle of the duck and the ball."),
        (["fish", "cup", "heart", "flower"], "The heart is between the cup and the ___.", "flower",
         ["fish", "cup", "star"], "The heart is in the middle of the cup and the <b>flower</b>."),
    ]:
        its.append(mcq(fig(kinds_row_svg(kinds)) + q, ans, wr, e))
    o = its
    order = [o[3], o[4], o[8], o[9], o[13], o[16], o[17], o[0], o[5], o[10],
             o[18], o[14], o[1], o[6], o[11], o[15], o[19], o[2], o[7], o[12]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Turn it around", "items": order}


# ============================================================ set 5: shapes and where they are
def set_shapes(rnd, K):
    its = []
    scenes = [
        [("circle", "red", 1, 0), ("square", "blue", 1, 1), ("triangle", "yellow", 1, 2)],
        [("triangle", "green", 0, 1), ("circle", "blue", 1, 1), ("square", "red", 2, 1)],
        [("square", "yellow", 1, 0), ("rectangle", "green", 1, 1), ("hexagon", "red", 1, 2)],
        [("hexagon", "blue", 0, 1), ("triangle", "red", 1, 1), ("circle", "yellow", 2, 1)],
        [("rectangle", "red", 1, 0), ("circle", "green", 1, 1), ("square", "blue", 1, 2)],
    ]
    names = ["circle", "square", "triangle", "rectangle", "hexagon"]
    for sc in scenes:
        svg = shapes_scene_svg(sc)
        vertical = sc[0][2] == sc[1][2]
        a, b, c = [x[0] for x in sc]
        if vertical:
            qs = [("What shape is <b>above</b> the %s?" % b, a, "The %s is just above the %s." % (a, b)),
                  ("What shape is <b>below</b> the %s?" % b, c, "The %s is just below the %s." % (c, b)),
                  ("What shape is at the <b>top</b>?", a, "The shape at the top is the %s." % a),
                  ("What shape is <b>between</b> the %s and the %s?" % (a, c), b, "The %s is in the middle." % b)]
        else:
            qs = [("What shape is <b>between</b> the %s and the %s?" % (a, c), b, "The %s is in the middle." % b),
                  ("What shape is <b>next to</b> the %s at the end?" % a, b, "Only the %s is beside the %s." % (b, a)),
                  ("Which shape is <b>next to</b> both other shapes?", b, "The %s is in the middle, so it is next to both." % b),
                  ("What shape is at the other end from the %s?" % c, a, "The %s is at the other end." % a)]
        for q, ans, e in qs:
            wr = [x for x in [a, b, c] if x != ans] + [x for x in names if x not in (a, b, c)]
            its.append(mcq(fig(svg) + q, ans.capitalize(), [w.capitalize() for w in wr],
                           e + " The answer is <b>%s</b>." % ans))
    return {"title": "Shapes and where they are", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Position words tell where things are</h2>"
        + table(["Word", "Meaning"], [
            ["above", "higher than"], ["below", "lower than, under"], ["next to / beside", "at the side of"],
            ["between", "in the middle of two things"], ["in front of", "closer to you"], ["behind", "farther away, partly hidden"],
        ]) +
        "<h2>Above and below</h2>"
        "<figure class='sn-fig'>" + table_scene_svg("ball", "above") + "<figcaption>The ball is above the table.</figcaption></figure>"
        "<h2>In front of and behind</h2>"
        "<p>If something covers part of the box, it is <b>in front of</b> the box. "
        "If the box covers part of it, it is <b>behind</b> the box.</p>"
        "<figure class='sn-fig'>" + box_scene_svg("duck", "behind") + "<figcaption>The duck is behind the box.</figcaption></figure>"
        "<h2>Turn it around</h2>"
        "<p>If the ball is above the table, then the table is below the ball.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Mixing up above and below", "Above is up high. Below is down low"],
            ["Mixing up in front of and behind", "Ask: what is hiding part of what?"],
            ["Saying next to for the middle thing", "Use between when it has a thing on each side"],
        ])
    )


FAQ = [
    {"q": "Which position words do kindergartners learn?",
     "a": "Above, below, beside, next to, in front of and behind. Many classes also use between, top, middle and bottom."},
    {"q": "Why are position words part of math?",
     "a": "They help children describe shapes and space. Later they use the same ideas for maps, graphs and geometry."},
    {"q": "How can I practice position words at home?",
     "a": "Play hide and seek with a toy and ask: Is it under the table? Behind the chair? Give directions like 'Put the cup next to the plate'."},
    {"q": "My child mixes up in front of and behind. What helps?",
     "a": "Stand a toy and a box on a table. Move the toy and ask which one hides part of the other. The one that is hidden is behind."},
]


def gen():
    rnd = random.Random(2014)
    K = Kids(rnd)
    sets = [set_above(rnd, K), set_next(rnd, K), set_front(rnd, K), set_turn(rnd, K), set_shapes(rnd, K)]
    finish(sets, rnd, max_num=10)
    return {
        "slug": "positions", "sort": 14, "updated": UPDATED, "pdf_url": "",
        "title": "Positions: Above, Below, Next To, In Front Of, Behind",
        "seo_title": "Kindergarten Position Words Worksheets: Above, Below, Beside, In Front Of, Behind",
        "short_title": "Position Words",
        "domain": "Geometry",
        "standard_code": "K.G.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/G/A/1/",
        "standard_text": "Describe objects in the environment using names of shapes, and describe the relative positions "
                         "of these objects using terms such as above, below, beside, in front of, behind, and next to.",
        "meta_desc": "Free kindergarten position words worksheets: above, below, next to, between, in front of and "
                     "behind with tables, shelves, boxes and shapes. 100 picture questions with an answer key.",
        "key_big": "Position words tell where things are: above, below, next to, in front of, behind.",
        "key_sub": "If the ball is above the table, the table is below the ball.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
