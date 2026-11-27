# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Foundation, AC9SFU03: objects are made of materials (wood, metal, plastic, glass, fabric,
paper, rubber) and materials have properties we can observe (hard or soft, rough or smooth, bendy or stiff, see-through,
waterproof).
  python tools/gen_au_science_f_materials_and_their_properties.py
Reuses the UK Year 1 objects and materials and properties of materials makers and the US Grade 2 properties of materials makers
with Australian names, plus own questions. Very short sentences.
Wrong answers come from real mistakes: confusing an object with its material, and thinking all shiny things are metal.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit
import sci_kids as K

YEAR, SORT = 0, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

OM = "gen_uk_science_y1_objects_and_materials"
PM = "gen_uk_science_y1_properties_of_materials"
U2 = "gen_us_science_g2_properties_of_materials"
o_om = limit(src(OM, "g_om"), 6)
o_pick = limit(src(OM, "g_pick"), 6)
o_which = limit(src(OM, "g_which"), 6)
o_multi = src(OM, "g_multi")
o_b1 = src.B(OM, "B1")
o_b5 = src.B(OM, "B5")
m_group = limit(src(PM, "g_group"), 6)
m_opp = src(PM, "g_opp")
m_prop = limit(src(PM, "g_prop"), 6)
m_soak = src(PM, "g_soak")
m_b1 = src.B(PM, "B1")
m_b5 = src.B(PM, "B5")
u_which = limit(src(U2, "g_which"), 5)
u_true = limit(src(U2, "g_true"), 4)

POOL1 = pool(R, [
    ("What is a spoon often made of?", "metal", ["paper", "wool", "glass"], "Metal is hard and strong."),
    ("What is a window made of?", "glass", ["wood", "paper", "fabric"], "Glass is see-through."),
    ("What is a T-shirt made of?", "fabric", ["metal", "glass", "rock"], "Fabric is soft and bendy."),
    ("Which material is see-through?", "glass", ["wood", "metal", "brick"], "We can see through glass."),
    ("Which material is soft?", "wool", ["metal", "stone", "glass"], "Wool feels soft."),
    ("Which material bends and stretches?", "rubber", ["glass", "stone", "wood"], "A rubber band stretches."),
    ("What is a raincoat made of so it keeps you dry?", "a waterproof material such as plastic", ["paper", "cotton wool", "tissue"], "Waterproof materials do not let water through."),
    ("What is a cricket bat made of?", "wood", ["glass", "wool", "paper"], "Wood is hard and strong."),
    ("Which one is shiny?", "a metal spoon", ["a wooden block", "a wool sock", "a paper bag"], "Many metals are shiny."),
    ("Which one feels rough?", "sandpaper", ["glass", "a plastic cup", "silk"], "Rough means bumpy to touch."),
    ("Which one floats in water?", "a cork", ["a rock", "a metal key", "a coin"], "Some materials float."),
    ("What is a hat made of to keep the sun off in summer?", "fabric", ["glass", "metal", "stone"], "Slip, slop, slap: wear a hat in the sun."),
])
POOL5 = pool(R, [
    ("Mia drops water on paper, plastic and foil. Which one soaks it up?", "the paper", ["the plastic", "the foil", "none"], "Paper is absorbent."),
    ("Jack tests which material is best for an umbrella. Which should he pick?", "plastic", ["paper", "tissue", "cotton wool"], "An umbrella must be waterproof."),
    ("Ruby puts a torch behind wood, glass and cardboard. Which lets light through?", "glass", ["wood", "cardboard", "none"], "Glass is transparent."),
    ("Kai sorts objects into 'hard' and 'soft'. Where does a pillow go?", "soft", ["hard", "both", "neither"], "Press it gently to test."),
    ("Ella tests which objects a magnet picks up. Which one does it pick up?", "a steel paper clip", ["a plastic spoon", "a wooden block", "a rubber band"], "Magnets pick up some metals."),
    ("Noah wants a material for a sandpit spade that will not bend. Which is best?", "hard plastic", ["paper", "fabric", "jelly"], "It must be stiff and strong."),
])


def main():
    sets = U.sets([
        ("What is it made of?", [(o_om, 6), (o_which, 6), (POOL1, 5), (o_b1, 3)]),
        ("Kinds of materials", [(o_pick, 6), (o_multi, 4), (POOL1, 4), (m_group, 4), (u_which, 2)]),
        ("Hard, soft, rough and smooth", [(m_prop, 6), (m_opp, 6), (POOL1, 3), (m_b1, 3), (m_group, 2)]),
        ("See-through, bendy and waterproof", [(m_soak, 5), (u_which, 3), (u_true, 4), (POOL1, 3), (m_prop, 2), (o_b1, 3)]),
        ("Let's test it", [(POOL5, 6), (o_b5, 4), (m_b5, 4), (m_soak, 2), (o_multi, 2), (u_true, 2)]),
    ])
    pic = K.row(["spoon", "glass", "sock", "block"], words=["metal", "glass", "fabric", "wood"], size=80, label="a metal spoon, a glass, a fabric sock and a wooden block")
    make_au(YEAR, "materials-and-their-properties", SORT, "AC9SFU03", "Chemical sciences",
            "Recognise that objects can be composed of different materials and describe the observable properties of those materials "
            "(Australian Curriculum v9.0 Science content description).",
            "Materials and Their Properties", "Materials",
            "Free Foundation science worksheets on materials: wood, metal, plastic, glass, fabric and paper, and properties such as "
            "hard, soft, rough, smooth, see-through and waterproof. 100 questions with answers.",
            "Everything is made of materials.", "Wood, metal, plastic, glass and fabric each feel and act differently.",
            ("Objects are made of materials.", ["A spoon can be metal or plastic.", "Glass is see-through.", "Rubber is bendy; wool is soft."]),
            [("What is a window made of?", ["you can see through it"], "glass")],
            ["Mixing up the object (a cup) with its material (plastic).", "Thinking all shiny things are metal."],
            [("What is a material?", "A material is what an object is made of, such as wood, metal, plastic, glass, paper or fabric."),
             ("What are properties?", "Properties describe a material: hard or soft, rough or smooth, bendy or stiff, see-through or not."),
             ("How can children test materials?", "Drip water on them, shine a torch through them, bend them gently and feel them.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
