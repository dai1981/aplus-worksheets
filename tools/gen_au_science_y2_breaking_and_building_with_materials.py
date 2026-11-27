# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 2, AC9S2U03: breaking materials into smaller pieces and building with them - cutting,
tearing, crushing and snapping, building and rebuilding with blocks, and choosing materials for a job.
  python tools/gen_au_science_y2_breaking_and_building_with_materials.py
Reuses the US Grade 2 building with small pieces and choosing materials makers and the UK Year 2 uses of everyday materials makers
with Australian names, plus own questions. Short sentences.
Wrong answers come from real mistakes: thinking small pieces are a different material, and choosing a material for its colour
instead of its properties.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once
import sci_kids as K

YEAR, SORT = 2, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

BS = "gen_us_science_g2_building_with_small_pieces"
CM = "gen_us_science_g2_choosing_materials"
UM = "gen_uk_science_y2_uses_of_everyday_materials"
b_count = limit(src(BS, "g_count"), 6)
b_rebuild = limit(src(BS, "g_rebuild"), 10)
b_same = limit(src(BS, "g_same"), 10)
b_pieces = src(BS, "g_pieces")
b_b1 = src.B(BS, "B1")
b_b5 = src.B(BS, "B5")
c_job = limit(src(CM, "g_job"), 10)
c_test = limit(src(CM, "g_test", rep=[(r"Which material the ", "Which material is the ")]), 9)
c_b5 = src.B(CM, "B5")
u_why = limit(src(UM, "g_why"), 6)
u_bad = src(UM, "g_bad")
u_mat = src(UM, "g_mat")

BRK = [("cut paper with scissors", "cutting"), ("tear a leaf into bits", "tearing"), ("crush a biscuit", "crushing"),
       ("snap a stick in half", "snapping"), ("grate cheese", "grating"), ("chop a carrot", "chopping"), ("smash ice for a drink", "crushing"),
       ("break a chocolate bar into squares", "snapping")]


def g_brk():
    a, w = R.choice(BRK)
    k = R.choice(["word", "same"])
    if not once(("bk", a, k)):
        return None
    if k == "word":
        return tq("You %s. What is this action called?" % a, w, [x for x in ["cutting", "tearing", "crushing", "snapping", "grating", "stretching"] if x != w][:3],
                  "These actions break materials into smaller pieces.")
    return tq("You %s. Are the small pieces still the same material?" % a, "yes", ["no, they are a new material", "no, they turn into water", "no, they disappear"],
              "Smaller pieces are still the same material.")


POOL1 = pool(R, [
    ("A big tower of blocks is pulled apart and built into a bridge. What is the same?", "the blocks", ["the shape", "the name of the object", "nothing"], "The same pieces can make new objects."),
    ("Why are bricks good for building a house?", "they are strong and hard", ["they are soft", "they are see-through", "they melt in the sun"], "Materials are chosen for their properties."),
    ("Why are windows made of glass?", "you can see through glass", ["glass is soft", "glass is bendy", "glass soaks up water"], "Choose a material for the job."),
    ("Which material would make the best tent?", "waterproof fabric", ["paper", "glass", "metal sheet"], "A tent must keep you dry and fold up."),
    ("Sand is made of tiny pieces of rock. What are they still?", "rock", ["water", "plastic", "wood"], "Wind and water break rocks into sand."),
    ("Why is a slide at the park made of smooth plastic or metal?", "so you slide down easily", ["so it is soft", "so it soaks up water", "so it breaks"], "Smooth surfaces are slippery."),
    ("What happens to a jigsaw puzzle when you take it apart?", "it is in pieces, but they can go back together", ["the pieces become a new material", "it disappears", "it melts"], "The pieces fit back together."),
    ("Which material would make a good bag for groceries?", "strong fabric", ["tissue paper", "glass", "ice"], "Bags must hold weight without tearing."),
    ("Why do people recycle old paper into new paper?", "the paper fibres can be broken up and made into new sheets", ["paper becomes metal", "it makes paper disappear", "it is not possible"], "Recycling saves trees."),
    ("Which is the best material for a spoon used in hot soup?", "metal", ["chocolate", "paper", "ice"], "It must not melt or bend in hot food."),
])
POOL5 = pool(R, [
    ("Mia builds a car with 20 blocks. She takes it apart and builds a house. How many blocks are in the house?", "20", ["10", "40", "0"], "The same pieces were used again."),
    ("Jack tests which paper towel soaks up the most water. What should he keep the same?", "the amount of water and the size of each towel", ["the type of towel", "nothing", "the colour"], "Only change the towel."),
    ("Ruby crushes a cracker into crumbs. She weighs the cracker before and the crumbs after. What will she find?", "about the same weight", ["the crumbs weigh nothing", "the crumbs weigh double", "the cracker disappears"], "No material was added or taken away."),
    ("Kai wants to make a boat that floats. Which material should he test first?", "a plastic tray", ["a rock", "a metal key", "a lump of clay"], "Plastic trays float."),
    ("Ella cuts a sheet of paper into 8 pieces. Can the pieces make the same sheet again?", "yes, if they are put back together like a puzzle", ["no, they are a new material", "yes, they melt together", "no, they vanished"], "The material has not changed."),
    ("Noah builds a bridge from paper and tests it with coins. How can he make it stronger?", "fold the paper into a zigzag", ["wet the paper", "use thinner paper", "paint it"], "Folding changes the shape and makes it stronger."),
])


def main():
    sets = U.sets([
        ("Breaking into smaller pieces", [(g_brk, 10), (POOL1, 4), (b_pieces, 4), (b_b1, 2)]),
        ("Building and rebuilding", [(b_rebuild, 6), (b_same, 6), (b_count, 5), (POOL1, 3)]),
        ("Choosing materials", [(c_job, 6), (u_why, 6), (u_mat, 4), (POOL1, 2), (u_bad, 2)]),
        ("Is it the right material?", [(u_bad, 5), (c_test, 5), (POOL1, 1), (POOL5, 3), (g_brk, 3), (b_count, 1), (u_mat, 2)]),
        ("Let's test it", [(POOL5, 3), (b_b5, 4), (c_b5, 4), (c_test, 1), (b_same, 2), (b_rebuild, 2), (c_job, 2), (g_brk, 2)]),
    ])
    pic = K.row(["block", "paper", "house", "rock"], words=["blocks", "cut paper", "build", "sand"], size=80, label="blocks, cut paper, a house and a rock")
    make_au(YEAR, "breaking-and-building-with-materials", SORT, "AC9S2U03", "Chemical sciences",
            "Recognise that materials can be changed physically without changing their material composition and explore the effect of "
            "different actions on materials including bending, twisting, stretching and breaking into smaller pieces "
            "(summary of the Australian Curriculum v9.0 Science content description).",
            "Breaking and Building with Materials", "Breaking and building",
            "Free Year 2 science worksheets on breaking and building with materials: cutting, tearing and crushing, building and "
            "rebuilding with pieces, and choosing materials for a job. 100 questions with answers.",
            "Small pieces, same material.", "Cutting makes smaller pieces of the same material. Pieces can build new things.",
            ("We can break materials into pieces.", ["Cut, tear, crush or snap.", "The pieces are still the same material.",
                                                    "Pieces can build something new."]),
            [("Crushed biscuit: still biscuit?", ["only the size changed"], "yes")],
            ["Thinking small pieces are a different material.", "Choosing a material for its colour instead of what it can do."],
            [("Is cutting a physical change?", "Yes. Cutting makes smaller pieces, but they are still the same material."),
             ("How do we choose a material for a job?", "Think about what it must do: be strong, waterproof, see-through, bendy or soft, then pick a material with that property."),
             ("How can children explore this?", "Build with blocks and rebuild into new shapes, cut paper into puzzles, and test which materials are best for a boat or a bag.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
