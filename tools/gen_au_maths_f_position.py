# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Position and Location (Australian Curriculum v9.0, AC9MFSP02)
  python3 tools/gen_au_maths_f_position.py
Above, under and next to a table; in front of, behind, next to and on top of a box; top, middle and bottom
shelves; first, last, next to and between in a line; and position words in everyday places.
Wrong answers come from real mistakes: mixing up in front of and behind, above and under, first and last,
and choosing a thing next to the right one instead of between.
"""
import random
from k_pics import name, table_scene_svg, box_scene_svg, shelf_svg, kinds_row_svg, KINDS
from f_common import Kids, mcq, finish, make, fig, figure, mistakes

R = random.Random(100101)
T_REL = {"above": "Above the table", "below": "Under the table", "beside": "Next to the table"}
B_REL = {"front": "In front of the box", "behind": "Behind the box", "beside": "Next to the box", "above": "On top of the box"}


# ------------------------------------------------------------ set 1: table
def set_table(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        k = KINDS[len(its) % len(KINDS)]
        rel = ["above", "below", "beside"][len(its) % 3]
        form = (len(its) // 3) % 2
        if (k, rel, form) in seen:
            k = rnd.choice(KINDS)
            if (k, rel, form) in seen:
                continue
        seen.add((k, rel, form))
        svg = table_scene_svg(k, rel)
        ans = T_REL[rel]
        if form == 0:
            q = fig(svg) + "Where is the %s?" % name(k, 1)
            wr = [v for r, v in T_REL.items() if r != rel] + ["On the floor far away"]
        else:
            q = fig(svg) + "Is the %s above the table, under the table or next to the table?" % name(k, 1)
            wr = [v for r, v in T_REL.items() if r != rel] + ["Inside the table"]
        e = {"above": "The %s is higher than the table top. It is <b>above the table</b>.",
             "below": "The %s is lower than the table top, between the legs. It is <b>under the table</b>.",
             "beside": "The %s is at the side of the table. It is <b>next to the table</b>."}[rel] % name(k, 1)
        its.append(mcq(q, ans, wr, e))
    return {"title": "Above, under and next to", "items": its}


# ------------------------------------------------------------ set 2: box
def set_box(rnd):
    its = []
    seen = set()
    rels = ["front", "behind", "beside", "above"]
    while len(its) < 20:
        k = rnd.choice(KINDS)
        rel = rels[len(its) % 4]
        if (k, rel) in seen:
            continue
        seen.add((k, rel))
        ans = B_REL[rel]
        q = fig(box_scene_svg(k, rel)) + "Where is the %s?" % name(k, 1)
        e = {"front": "The %s covers part of the box, so it is closer to us: <b>in front of the box</b>.",
             "behind": "The box hides part of the %s, so it is further away: <b>behind the box</b>.",
             "beside": "The %s is at the side of the box: <b>next to the box</b>.",
             "above": "The %s is higher than the box: <b>on top of the box</b>."}[rel] % name(k, 1)
        its.append(mcq(q, ans, [v for r, v in B_REL.items() if r != rel], e))
    return {"title": "In front of and behind", "items": its}


# ------------------------------------------------------------ set 3: shelves
def set_shelf(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        ks = rnd.sample(KINDS, 3)
        kind = len(its) % 4
        key = (tuple(ks), kind)
        if key in seen:
            continue
        seen.add(key)
        svg = shelf_svg(ks)
        names = [name(k, 1) for k in ks]
        if kind == 0:
            pos = rnd.randrange(3)
            where = ["top", "middle", "bottom"][pos]
            q = fig(svg) + "What is on the <b>%s</b> shelf?" % where
            ans = "The " + names[pos]
            e = "Look at the %s shelf: <b>the %s</b>." % (where, names[pos])
            wr = ["The " + n for n in names if n != names[pos]] + ["Nothing"]
        elif kind == 1:
            pos = rnd.randrange(3)
            q = fig(svg) + "Which shelf is the %s on?" % names[pos]
            ans = ["The top shelf", "The middle shelf", "The bottom shelf"][pos]
            wr = [x for x in ["The top shelf", "The middle shelf", "The bottom shelf"] if x != ans] + ["On the floor"]
            e = "The %s is on <b>%s</b>." % (names[pos], ans.lower())
        elif kind == 2:
            q = fig(svg) + "What is just <b>above</b> the %s?" % names[1]
            ans = "The " + names[0]
            wr = ["The " + names[2], "The " + names[1], "Nothing"]
            e = "Above means higher up. Just above the %s is <b>the %s</b>." % (names[1], names[0])
        else:
            q = fig(svg) + "What is just <b>below</b> the %s?" % names[1]
            ans = "The " + names[2]
            wr = ["The " + names[0], "The " + names[1], "Nothing"]
            e = "Below means lower down. Just below the %s is <b>the %s</b>." % (names[1], names[2])
        its.append(mcq(q, ans, wr, e))
    return {"title": "Top, middle and bottom", "items": its}


# ------------------------------------------------------------ set 4: in a line
def set_line(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        ks = rnd.sample(KINDS, 5)
        kind = len(its) % 4
        key = (tuple(ks), kind)
        if key in seen:
            continue
        seen.add(key)
        svg = kinds_row_svg(ks)
        names = [name(k, 1) for k in ks]
        pre = fig(svg) + "The line starts on the left. "
        if kind == 0:
            q = pre + "What is <b>first</b> in the line?"
            ans, wr = names[0], [names[4], names[1], names[2]]
            e = "The line starts on the left, so the first one is <b>the %s</b>." % names[0]
        elif kind == 1:
            q = pre + "What is <b>last</b> in the line?"
            ans, wr = names[4], [names[0], names[3], names[2]]
            e = "The last one is at the end on the right: <b>the %s</b>." % names[4]
        elif kind == 2:
            j = rnd.randrange(1, 4)
            q = pre + "What is <b>between</b> the %s and the %s?" % (names[j - 1], names[j + 1])
            ans, wr = names[j], [names[j - 1], names[j + 1], names[(j + 2) % 5]]
            e = "Between means in the middle of the two. <b>The %s</b> is between them." % names[j]
        else:
            j = rnd.choice([0, 4])
            q = pre + "What is <b>next to</b> the %s?" % names[j]
            nb = names[1] if j == 0 else names[3]
            ans, wr = nb, [names[2], names[4 - j], names[j]]
            e = "Next to means right beside it. Next to the %s is <b>the %s</b>." % (names[j], nb)
        its.append(mcq(q, "The " + ans, ["The " + w for w in wr], e))
    return {"title": "First, last, next to and between", "items": its}


# ------------------------------------------------------------ set 5: everyday places
def set_words(rnd):
    K = Kids(rnd)
    its = []
    plan = [("{n}'s hat is on {his} head. Where is the hat?", "On top of {his} head", ["Under {his} feet", "Behind the door", "Inside {his} bag"]),
            ("The cat is hiding and we can only see its tail sticking out from the bed. Where is the cat?", "Under the bed", ["On top of the bed", "Next to the window", "Above the bed"]),
            ("{n} stands at the front of the line, so nobody is ahead of {him}. Where is {n} in the line?", "First", ["Last", "In the middle", "Behind everyone"]),
            ("{n} puts {his} lunch box in {his} school bag and zips it up. Where is the lunch box?", "Inside the bag", ["On top of the bag", "Next to the bag", "Under the bag"]),
            ("The kookaburra sits on a branch high up in the tree. Is it above or below the ground?", "Above the ground", ["Below the ground", "Inside the ground", "Next to the ground"]),
            ("{n} sits between two friends on the mat. How many friends are next to {him}?", "2", ["1", "3", "0"]),
            ("The teacher is in front of the class. Where are the children?", "Behind the teacher", ["In front of the teacher", "On top of the teacher", "Under the teacher"]),
            ("The sun is high in the sky. The grass is on the ground. Which is above the other?", "The sun is above the grass", ["The grass is above the sun", "They are next to each other", "The sun is under the grass"]),
            ("{n} is the last child on the bus line. Who is behind {him}?", "Nobody", ["Everyone", "The first child", "The teacher at the front"]),
            ("A wombat goes down into its burrow. Is it now above or below the ground?", "Below the ground", ["Above the ground", "On top of the ground", "Next to the ground"]),
            ("{n}'s shoes are on {his} feet. {His} socks are inside {his} shoes. Where are the socks?", "Inside the shoes", ["On top of the shoes", "Next to the shoes", "Above {his} head"]),
            ("In the photo, {n} is closer to the camera than the tree. Where is {n}?", "In front of the tree", ["Behind the tree", "On top of the tree", "Under the tree"]),
            ("The light hangs from the ceiling over the table. Where is the light?", "Above the table", ["Under the table", "Next to the table", "Inside the table"]),
            ("{n} hides so that the big rock is between {him} and {his} friend. Where is {n}, as {his} friend sees it?", "Behind the rock", ["On top of the rock", "In front of the rock", "Under the rock"]),
            ("A koala hugs the trunk, halfway up the tree. What is above the koala?", "The top of the tree", ["The roots", "The ground", "Nothing"]),
            ("The dog sleeps on the mat by the door. Where is the mat?", "Under the dog", ["On top of the dog", "Above the dog", "Inside the dog"]),
            ("There are 3 children in a line: Ava, then {n}, then Sam. Who is in the middle?", "{n}", ["Ava", "Sam", "Nobody"]),
            ("{n} puts the book back on the shelf, between the red book and the blue book. What is next to {his} book?", "The red book and the blue book", ["Only the red book", "Only the blue book", "No books"]),
            ("The boat floats on the water. The fish swims under the boat. Where is the boat?", "Above the fish", ["Under the fish", "Inside the fish", "Behind the fish"]),
            ("{n} looks into a mirror and waves. The mirror is on the wall in front of {him}. Where is the wall?", "In front of {n}", ["Behind {n}", "Under {n}", "On top of {n}"])]
    for t, ans, wr in plan:
        kid = K.next()
        f = dict(n=kid["n"], his=kid["his"], His=kid["His"], him="her" if kid["he"] == "she" else "him")
        q = t.format(**f)
        a = ans.format(**f)
        w = [x.format(**f) for x in wr]
        its.append(mcq(q, a, w, "Picture it in your head: <b>%s</b>." % a, allow_zero=True))
    return {"title": "Where is it? Everyday places", "items": its}


def body():
    return (
        "<h2>Position words</h2>"
        "<p>Position words tell <b>where</b> something is: above, under, next to, in front of, behind, on top of, inside, between, first and last.</p>"
        + figure(table_scene_svg("ball", "above"), "The ball is above the table.")
        + figure(box_scene_svg("duck", "behind"), "The duck is behind the box. The box hides part of it.")
        + "<h2>In a line</h2><p>The first one is at the start and the last one is at the end. Between means in the middle of two things.</p>"
        + figure(kinds_row_svg(["apple", "star", "duck", "ball"]), "The star is between the apple and the duck.")
        + mistakes([["Mixing up in front of and behind", "In front is closer to you; behind is hidden or further away"],
                    ["Mixing up above and under", "Above is higher up; under is lower down"],
                    ["Mixing up first and last", "First is at the start of the line"]]))


FAQ = [("What position words do Foundation students learn?",
        "Words like above, under, next to, in front of, behind, on top of, inside, between, first and last, to describe where they and objects are (AC9MFSP02)."),
       ("Do Foundation students learn left and right?",
        "Left and right are introduced gently but are not the focus. Words like next to, between, in front of and behind come first."),
       ("Why are position words part of maths?",
        "They are the start of geometry and maps. Later children use them to give directions, read grids and describe shapes."),
       ("How can I practise at home?",
        "Play hide and seek with a toy and describe where it is, or give instructions: Put the cup next to the plate. Stand behind the chair.")]


def build():
    sets = [set_table(R), set_box(R), set_shelf(R), set_line(R), set_words(R)]
    finish(sets, R, max_num=10)
    make("position-and-location", 11, "AC9MFSP02", "Space",
         "Position and Location: Where Is It?",
         "Foundation Position Words Worksheets: Above, Under, Behind, Between (Free, with Answers)",
         "Position and location",
         "Describe the position and location of themselves and objects in relation to other people and objects within a familiar space.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on position and location, matched to the Australian Curriculum (AC9MFSP02): above, under, next to, in front of, behind, on top of, between, first and last. 100 picture questions with answers.",
         "Position words tell where something is.",
         "In front of is closer, behind is further away. Between is in the middle of two things.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
