# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Repeating Patterns (BC Mathematics Curriculum, Kindergarten Content: Repeating patterns with
two or three elements; sorting and classifying using a single attribute)
  python3 tools/gen_cabc_math_k_repeating_patterns.py
What comes next in AB patterns and in AAB, ABB and ABC patterns, the core (the part that repeats), the missing
piece, and patterns in sounds and actions with sorting by one attribute. Sets 1 to 4 and half of set 5 reuse the
AU Foundation pattern makers with Canadian names and spelling.
Wrong answers come from real mistakes: repeating the last item, choosing the item after the next one, taking
only one item as the core, and sorting by two rules at once.
"""
import random
from k_pics import shapes_mix_svg, lettered_shapes_svg
import bck_common
from bck_common import Kids, Cycle, mcq, letters, finish, make, fig, figure, lesson, collect, S
import gen_au_maths_f_repeating_patterns as au
from f_common import pattern_svg

R = random.Random(52601)
au.Kids = Kids
SHAPES = ["circle", "square", "triangle", "rectangle"]
COLS = ["red", "blue", "yellow", "green"]
POS = Cycle()


def take(set_fn, n, r):
    its = set_fn(r)["items"]
    return its[:n]


# ------------------------------------------------------------ sorting by one attribute
def one_sort(r):
    kind = r.choice(["odd_col", "odd_shape", "count_col", "count_shape"])
    if kind in ("odd_col", "odd_shape"):
        if kind == "odd_col":
            col, other = r.sample(COLS, 2)
            ks = r.sample(SHAPES, 4)
            items = [(k, col) for k in ks]
            j = POS.next()
            items[j] = (items[j][0], other)
            rule = "colour"
            e = "Three are %s. Shape <b>%s</b> is %s, so it does not belong when we sort by colour." % (col, "ABCD"[j], other)
        else:
            k, other = r.sample(SHAPES, 2)
            cs = r.sample(COLS, 4)
            items = [(k, c) for c in cs]
            j = POS.next()
            items[j] = (other, items[j][1])
            rule = "shape"
            e = "Three are %ss. Shape <b>%s</b> is a %s, so it does not belong when we sort by shape." % (k, "ABCD"[j], other)
        it = mcq(fig(lettered_shapes_svg(items)) + "We sort by <b>%s</b>. Which one does not belong?" % rule, "ABCD"[j], [l for l in "ABCD" if l != "ABCD"[j]], e)
        return letters(it, "ABCD"[j])
    n = r.randint(2, 6)
    m = r.randint(2, 6)
    if n + m > 10:
        return None
    if kind == "count_col":
        c1, c2 = r.sample(COLS, 2)
        items = [(r.choice(SHAPES), c1) for _ in range(n)] + [(r.choice(SHAPES), c2) for _ in range(m)]
        return mcq(fig(shapes_mix_svg(items, r.randint(1, 9999))) + "Sort the shapes by colour. How many are <b>%s</b>?" % c1, n, [m, n + m, n + 1, n - 1],
                   "Look only at the colour. There are <b>%d</b> %s shapes." % (n, c1))
    s1, s2 = r.sample(SHAPES, 2)
    items = [(s1, r.choice(COLS)) for _ in range(n)] + [(s2, r.choice(COLS)) for _ in range(m)]
    return mcq(fig(shapes_mix_svg(items, r.randint(1, 9999))) + "Sort the shapes by shape. How many are <b>%ss</b>?" % s1, n, [m, n + m, n + 1, n - 1],
               "Look only at the shape, not the colour. There are <b>%d</b> %ss." % (n, s1))


def build():
    sets = [S("What comes next? (AB)", take(au.set_ab, 20, R)),
            S("What comes next? (AAB, ABB, ABC)", take(au.set_harder, 20, R)),
            S("The part that repeats", take(au.set_unit, 20, R)),
            S("Find the missing piece", take(au.set_missing, 20, R)),
            S("Sounds, actions and sorting", take(au.set_ways, 10, R) + collect(one_sort, 10, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li>A <b>repeating pattern</b> has a part that repeats again and again. This part is called the <b>core</b>.</li>"
        "<li>Say the pattern out loud: red, blue, red, blue … Then say what comes next.</li>"
        "<li>Patterns can have 2 or 3 things in the core: AB, AAB, ABB or ABC.</li>"
        "<li>To <b>sort</b>, choose one rule, like colour or shape, and put things that match together.</li></ul>",
        [figure(pattern_svg([("shape", "circle", "red"), ("shape", "square", "blue")] * 3), "The core is red circle, blue square. It repeats."),
         figure(pattern_svg([("obj", "apple"), ("obj", "apple"), ("obj", "star")] * 2), "The core is apple, apple, star (AAB).")],
        [["Repeating the last thing", "Say the whole pattern out loud from the start."],
         ["Taking only one thing as the core", "Find where the pattern starts again."],
         ["Sorting by colour and shape at once", "Choose one rule at a time."]])
    faq = [("What is a repeating pattern?", "A pattern where the same group of things, the core, repeats again and again, such as red, blue, red, blue."),
           ("What is the core of a pattern?", "The shortest part that repeats. In clap, clap, stamp, clap, clap, stamp, the core is clap, clap, stamp."),
           ("What patterns do Kindergarten children learn?", "Repeating patterns with two or three elements, such as AB, AAB, ABB and ABC, shown with objects, colours, sounds and actions."),
           ("How does sorting help with patterns?", "Sorting by one attribute, like colour or shape, helps children notice what is the same and what changes in a pattern.")]
    make("repeating-patterns", 6, "Patterning", "Repeating Patterns: What Comes Next and the Core", "Repeating patterns",
         "Repeating patterns with two or three elements: sorting and classifying using a single attribute, identifying patterns in the world, repeating patterns with 2-3 elements, identifying the core",
         "Free Kindergarten math worksheets on repeating patterns for the BC curriculum: AB, AAB, ABB and ABC patterns, the core, missing pieces, sound and action patterns, and sorting by one attribute. 100 picture questions with answers.",
         "The core is the part of a pattern that repeats.", "Say the pattern out loud. Find where it starts again to see the core.",
         body, faq, sets)


if __name__ == "__main__":
    build()
