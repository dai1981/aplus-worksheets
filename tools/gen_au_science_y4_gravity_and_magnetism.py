# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 4, AC9S4U03: non-contact forces - gravity, magnetism and static electricity act from
a distance.
  python tools/gen_au_science_y4_gravity_and_magnetism.py
Reuses the UK Year 3 magnet makers, the US Grade 3 magnet and static makers and the UK Year 5 gravity makers (mass, not weight in
newtons) with Australian names. Wrong answers come from real mistakes: thinking all metals are magnetic, thinking heavier
objects always fall faster, and thinking gravity only works on Earth.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 4, 5
U, R, P, src = AU(seed_of(YEAR, SORT))

MA = "gen_uk_science_y3_magnets_attract_and_repel"
MM = "gen_uk_science_y3_magnetic_materials"
US = "gen_us_science_g3_magnets_and_static_electricity"
GR = "gen_uk_science_y5_gravity"
ma_pic = src(MA, "g_pic")
ma_txt = src(MA, "g_txt")
ma_train = limit(src(MA, "g_train"), 4)
ma_use = src(MA, "g_use")
ma_str = limit(src(MA, "g_strength"), 3)
ma_b1 = src.B(MA, "B1")
ma_b5 = src.B(MA, "B5")
mm_is = limit(src(MM, "g_is"), 8)
mm_pick = limit(src(MM, "g_pick"), 5)
mm_sort = src(MM, "g_sort")
mm_b1 = src.B(MM, "B1")
us_metal = src(US, "g_metal")
us_dist = limit(src(US, "g_dist"), 3)
us_static = src(US, "g_static")
us_attract = limit(src(US, "g_attract"), 5)
us_poles = src(US, "g_poles")
ma_three = src(MA, "g_three")
us_b1 = src.B(US, "B1")
us_b5 = src.B(US, "B5")
gr_moon = limit(src(GR, "g_moon", drop=[" N", "newton", "weigh"]), 3)
gr_b5 = src.B(GR, "B5", drop=[" N", "newton"])

POOL1 = pool(R, [
    ("What is gravity?", "a force that pulls objects towards the centre of Earth", ["a force that pushes things up", "a kind of friction", "air pushing down"], "Gravity acts without touching."),
    ("Why does a ball you throw up come back down?", "Gravity pulls it back towards Earth.", ["Air pushes it up.", "The ball gets tired.", "Magnetism pulls it."], "Gravity acts on everything with mass."),
    ("Is gravity a contact or a non-contact force?", "a non-contact force", ["a contact force", "not a force", "a kind of friction"], "Gravity acts at a distance."),
    ("Which way does gravity pull people in Australia?", "down, towards the centre of Earth", ["up into the sky", "north", "sideways"], "Down means towards Earth's centre, wherever you are."),
    ("Why does the Moon orbit Earth?", "Earth's gravity pulls on it.", ["Wind pushes it.", "It is magnetic.", "It is tied by a rope."], "Gravity keeps the Moon in orbit."),
    ("Why do astronauts on the Moon bounce when they walk?", "The Moon's gravity is weaker than Earth's.", ["The Moon has more air.", "The Moon is magnetic.", "Their boots have springs."], "The Moon's pull is about one-sixth of Earth's."),
    ("A feather and a hammer are dropped on the Moon, where there is no air. What happens?", "They land at the same time.", ["The hammer lands first.", "The feather lands first.", "They float away."], "Without air resistance, all objects fall together."),
    ("Which force makes a balloon rubbed on your hair stick to a wall?", "static electricity", ["gravity", "friction only", "magnetism"], "Static electricity is a non-contact force."),
    ("Which of these is a magnetic material?", "iron", ["aluminium", "copper", "gold"], "Iron, steel, nickel and cobalt are magnetic."),
    ("Why does a compass needle point north?", "It is a small magnet that lines up with Earth's magnetic field.", ["Wind blows it north.", "Gravity pulls it north.", "It is heavier at one end."], "Earth acts like a giant magnet."),
])
POOL5 = pool(R, [
    ("Mia tests how many paperclips a magnet can hold through 1, 2 and 3 sheets of card. She gets 8, 5 and 2. What pattern does she find?", "More card means fewer paperclips are held.", ["More card means more paperclips are held.", "Card makes no difference.", "Magnets do not work through card."], "Magnetism gets weaker with distance."),
    ("Jack drops a tennis ball and a cricket ball from the same height at the same time. What will he see?", "They land at almost the same time.", ["The cricket ball lands much earlier.", "The tennis ball floats.", "The tennis ball lands much earlier."], "Gravity makes them fall together; air resistance is small for both."),
    ("Ruby says, 'All metals stick to magnets.' How could she test this?", "Hold a magnet near objects made of different metals, such as foil, copper and steel.", ["Test only steel objects.", "Use a magnet on wood.", "Ask a friend."], "Aluminium and copper are not attracted."),
    ("Kai rubs a balloon on his jumper and holds it over small pieces of paper. What happens?", "The paper jumps up to the balloon.", ["Nothing happens.", "The paper is pushed away to the floor.", "The balloon pops."], "Static electricity attracts light objects."),
    ("Why do recycling plants use a large magnet?", "to separate steel cans from aluminium cans", ["to crush glass", "to clean plastic", "to dry paper"], "Only the steel cans are attracted."),
    ("Ella measures the distance at which a magnet first pulls a paperclip. What should she keep the same?", "the magnet and the paperclip", ["the distance", "nothing", "the result"], "Only the thing being tested should change."),
])


def main():
    sets = U.sets([
        ("Gravity and static", [(POOL1, 7), (gr_moon, 3), (gr_b5, 3), (us_static, 3), (us_b1, 2), (us_poles, 2)]),
        ("Magnets attract and repel", [(ma_pic, 6), (ma_txt, 4), (ma_b1, 4), (ma_train, 3), (ma_three, 3)]),
        ("Magnetic materials", [(mm_is, 6), (mm_pick, 4), (us_metal, 3), (mm_b1, 4), (us_attract, 3)]),
        ("Uses of magnets and static", [(ma_use, 6), (mm_sort, 4), (us_static, 4), (us_b5, 3), (POOL1, 3)]),
        ("Investigations", [(POOL5, 6), (ma_b5, 4), (ma_str, 3), (us_dist, 3), (us_attract, 2), (us_static, 2)]),
    ])
    make_au(YEAR, "gravity-and-magnetism", SORT, "AC9S4U03", "Physical sciences",
            "Identify that forces can be exerted by one object on another by direct contact or from a distance, such as gravity, "
            "magnetism and static electricity (summary of the Australian Curriculum v9.0 Science content description).",
            "Gravity and Magnetism", "Gravity and magnetism",
            "Free Year 4 science worksheets on non-contact forces: gravity, magnets that attract and repel, magnetic materials and static "
            "electricity. 100 questions with answers.",
            "Some forces act without touching.", "Gravity, magnetism and static electricity are non-contact forces.",
            "<p><b>Non-contact forces act from a distance, without touching.</b></p><ul>"
            "<li>Gravity pulls objects towards the centre of Earth. It keeps the Moon in orbit.</li>"
            "<li>Magnets attract iron, steel, nickel and cobalt. Like poles repel; unlike poles attract.</li>"
            "<li>Static electricity, such as a rubbed balloon, can attract light objects like paper and hair.</li></ul>",
            [("North pole facing north pole. What happens?", ["like poles"], "they repel"),
             ("Will a magnet pick up an aluminium can?", ["aluminium is not a magnetic metal"], "no")],
            ["Thinking all metals are magnetic (aluminium, copper and gold are not).", "Thinking heavier objects always fall much faster.",
             "Thinking gravity only works on Earth."],
            [("Which materials do magnets attract?", "Magnets attract iron, steel, nickel and cobalt. They do not attract aluminium, copper, gold, plastic, wood or glass."),
             ("Why is gravity called a non-contact force?", "Gravity pulls objects towards Earth without touching them. It even pulls on the Moon from far away."),
             ("What is static electricity?", "It is an electric charge that builds up when some materials are rubbed together. It can make hair stand up and balloons stick to walls.")],
            sets)


if __name__ == "__main__":
    main()
