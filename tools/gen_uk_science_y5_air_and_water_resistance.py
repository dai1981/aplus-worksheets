# -*- coding: utf-8 -*-
"""
UK Year 5 science: Air and Water Resistance (Forces)
  python tools/gen_uk_science_y5_air_and_water_resistance.py
Air resistance and water resistance slow moving objects; parachute investigations; falling shapes in water;
streamlined shapes in nature and design; forces on a falling parachute.
Wrong answers come from real mistakes: "air resistance pushes in the direction of movement", "a bigger parachute
falls faster", "air resistance only matters for things in water", "streamlined means heavier".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq, num

U = Unit(61512)
R = U.R
P = People(R)


def g_chute():
    who = P.next()[0]
    sizes = [10, 20, 30, 40]
    base = R.choice([1.2, 1.4, 1.6])
    t = [round(base + 0.6 * i + R.choice([-0.1, 0, 0.1]), 1) for i in range(4)]
    k = R.choice(["read", "read", "slow", "pattern", "var", "same", "diff"])
    ri = R.randrange(4)
    if not once(("ch", tuple(t), k, ri if k == "read" else 0)) or (k in ("pattern", "var", "same") and not once(("ck", k), 2)):
        return None
    tab = table(["Parachute width (cm)", "Time to fall 2 m (s)"], [[str(a), num(b, 2)] for a, b in zip(sizes, t)])
    intro = tab + "%s dropped parachutes of different sizes with the same load. " % who
    if k == "read":
        g = "%s s" % num(t[ri], 2)
        return item(intro + "How long did the %d cm parachute take to fall?" % sizes[ri], g, uniq(g, ["%s s" % num(x, 2) for x in t] + ["%s s" % num(t[ri] + 0.5, 2)]), "Read the row.")
    if k == "slow":
        return item(intro + "Which parachute fell most slowly?", "the 40 cm parachute", ["the 10 cm parachute", "the 20 cm parachute", "the 30 cm parachute"], "The longest time means the slowest fall.")
    if k == "pattern":
        return item(intro + "What pattern do the results show?", "The bigger the parachute, the longer it takes to fall.", ["The bigger the parachute, the faster it falls.", "Size makes no difference.", "Only the smallest parachute works."],
                    "A bigger canopy has more air resistance.")
    if k == "var":
        return item(intro + "Which variable did %s change?" % who, "the width of the parachute", ["the time to fall", "the load", "the drop height"], "One variable is changed on purpose.")
    if k == "same":
        return item(intro + "What should be kept the same?", "the load, the drop height and the material", ["the width of the parachute", "the time to fall", "nothing"], "Control variables.")
    d = round(t[3] - t[0], 1)
    g = "%s s" % num(d, 2)
    return item(intro + "How much longer did the 40 cm parachute take than the 10 cm one?", g, uniq(g, ["%s s" % num(t[3], 2), "%s s" % num(t[0], 2), "%s s" % num(d + 0.5, 2), "%s s" % num(t[3] + t[0], 2)]),
                "%s − %s = %s s." % (num(t[3], 2), num(t[0], 2), num(d, 2)))


SHAPES = {"torpedo shape": 2, "ball": 3, "cube": 4, "cone (point down)": 3, "flat pancake": 8, "boat shape": 5}


def g_shape():
    who = P.next()[0]
    s = R.sample(sorted(SHAPES), 4)
    v = [SHAPES[x] + R.choice([0, 0.5]) for x in s]
    if len(set(v)) < 4:
        return None
    k = R.choice(["fast", "slow", "read", "why"])
    ri = R.randrange(4)
    if not once(("sh", tuple(s), tuple(v), k, ri if k == "read" else 0)) or (k == "why" and not once(("sw",), 3)):
        return None
    tab = table(["Shape of plasticine (same mass)", "Time to sink to the bottom (s)"], [[a, num(b, 2)] for a, b in zip(s, v)])
    intro = tab + "%s dropped plasticine shapes into a tall tube of water. " % who
    if k == "fast":
        a = s[v.index(min(v))]
        return item(intro + "Which shape had the least water resistance?", a, [x for x in s if x != a], "The fastest shape is the most streamlined.")
    if k == "slow":
        a = s[v.index(max(v))]
        return item(intro + "Which shape had the most water resistance?", a, [x for x in s if x != a], "The slowest shape pushed against the most water.")
    if k == "read":
        g = "%s s" % num(v[ri], 2)
        return item(intro + "How long did the %s take to sink?" % s[ri], g, uniq(g, ["%s s" % num(x, 2) for x in v] + ["%s s" % num(v[ri] + 1, 2)]), "Read the row.")
    return item(intro + "Why must each shape have the same mass?", "so only the shape affects how fast it sinks", ["so it sinks faster", "to make it float", "it does not matter"], "Fair test.")


STREAM = [("a dolphin", "a smooth, streamlined body to move through water easily"), ("a racing car", "a low, smooth body to cut through the air"),
          ("a cyclist in a race", "crouching low with a pointed helmet to reduce air resistance"), ("a falcon diving", "folding its wings to be streamlined"),
          ("a swimmer", "a tight swimming cap and smooth costume to reduce water resistance"), ("a fish", "a pointed head and smooth scales"),
          ("a high-speed train", "a long, pointed nose"), ("a penguin swimming", "a torpedo-shaped body")]
SLOW = [("a skydiver opening a parachute", "to increase air resistance and slow down"), ("a dragster using a drag chute", "to increase air resistance and stop quickly"),
        ("a sycamore seed spinning", "to increase air resistance and fall slowly"), ("a duck's webbed feet", "to push against more water when paddling"),
        ("a skydiver spreading arms and legs", "to increase air resistance"), ("a boat's wide oars", "to push against more water")]


def g_stream():
    k = R.random() < 0.55
    if k:
        w, f = R.choice(STREAM)
        if not once(("st", w)):
            return None
        bad = ["a wide, flat front that pushes lots of air or water", "a rough surface covered in bumps", "big flat sheets sticking out to catch the air",
               "spreading out as wide as possible", "a square, boxy shape"]
        return item("How is %s designed or adapted to go fast?" % w, f, R.sample(bad, 3), "Streamlined shapes reduce air and water resistance.")
    w, f = R.choice(SLOW)
    if not once(("sl", w)):
        return None
    return item("Why does this happen: %s?" % w, f, ["to reduce air resistance and go faster", "to make gravity stronger", "to reduce friction with the ground"], "Sometimes we want more resistance.")


DIR = [("A ball falls downwards.", "upwards"), ("A cyclist rides forwards.", "backwards"), ("A swimmer swims to the left.", "to the right"), ("A rocket flies upwards.", "downwards"),
       ("A boat moves to the right.", "to the left"), ("A leaf falls downwards.", "upwards")]


def g_dir():
    s, a = R.choice(DIR)
    if not once(("di", s)):
        return None
    m = {"upwards": "downwards", "downwards": "upwards", "backwards": "forwards", "to the right": "to the left", "to the left": "to the right"}[a]
    return item("%s Which way does air or water resistance act on it?" % s, a, [m, "sideways", "it does not act at all"], "Resistance always acts against the movement.")


B1 = bank([
    ("What is air resistance?", "a force from the air that pushes against moving objects", ["a force that pulls things down", "the weight of air", "a kind of wind"], "It slows things down."),
    ("What is water resistance?", "a force from water that pushes against objects moving through it", ["the weight of water", "a type of current", "a force that makes things float"], "Like air resistance, in water."),
    ("What does streamlined mean?", "shaped so that air or water flows past easily", ["heavier at the front", "covered in fur", "very big and flat"], "Pointed and smooth."),
    ("Why does a parachute slow a skydiver down?", "Its large area causes lots of air resistance.", ["It makes gravity weaker.", "It is very heavy.", "It pushes the ground away."], "More area, more resistance."),
    ("Which forces act on a falling parachute?", "gravity pulling down and air resistance pushing up", ["only gravity", "only air resistance", "friction from the ground"], "Two forces."),
    ("Why is it harder to run through water than through air?", "Water resistance is much bigger than air resistance.", ["Water has no resistance.", "Gravity is stronger in water.", "Air is heavier than water."], "Water is denser."),
    ("Why does a sheet of paper fall more slowly than the same paper screwed into a ball?", "The flat sheet has more air resistance.", ["The flat sheet is lighter.", "Gravity does not pull flat paper.", "The ball has more air resistance."], "Same mass, different shape."),
    ("When a parachute falls at a steady speed, what is true about the forces?", "Air resistance balances the pull of gravity.", ["There is no gravity.", "Air resistance is zero.", "Gravity has doubled."], "Balanced forces."),
])
B5 = bank([
    ("How could you test which shape of boat has the least water resistance?", "Pull boats of the same mass along a water tank with the same force and time them.", ["Use boats of different masses.", "Pull them with different forces.", "Paint them different colours."], "Fair test."),
    ("Why do lorries have curved panels on top of their cabs?", "to make them more streamlined and use less fuel", ["to keep the rain off", "to make them heavier", "to increase air resistance"], "Less resistance saves fuel."),
    ("Why do skydivers' speeds stop increasing after a while?", "Air resistance grows until it balances gravity.", ["Gravity switches off.", "They run out of energy.", "Air resistance disappears."], "Terminal speed."),
    ("Why might a parachute investigation give different times for the same parachute?", "Small changes in how it is dropped or timed; so repeat and take a mean.", ["Gravity changes each time.", "The parachute grows.", "Timers are always perfect."], "Repeat readings."),
    ("Why do many sea animals have similar streamlined shapes?", "Moving easily through water helps them catch food and escape predators.", ["They are all related to sharks.", "Water makes everything the same shape.", "It makes them heavier."], "Adaptation."),
])


def body():
    think = ("<p><b>Air and water push against moving objects and slow them down.</b></p>"
             "<ul><li>Air resistance and water resistance act against the direction of movement.</li>"
             "<li>A bigger area means more resistance: a bigger parachute falls more slowly.</li>"
             "<li>Streamlined shapes (dolphins, racing cars, fish) reduce resistance so they move faster.</li></ul>")
    ex = [("A ball falls. Air resistance acts?", ["Against the movement"], "upwards"),
          ("10 cm or 40 cm parachute: slower?", ["More area, more air resistance"], "40 cm")]
    mist = ["Thinking resistance pushes in the direction of movement.", "Thinking a bigger parachute falls faster.", "Thinking streamlined means heavier."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Air and water resistance", B1 + [(g_dir, 6), (g_stream, 6)]),
        ("Streamlined shapes", [(g_stream, 8), (g_shape, 12)]),
        ("Parachutes", [(g_chute, 20)]),
        ("Shapes in water", [(g_shape, 12), (g_chute, 8)]),
        ("Investigating resistance", B5 + [(g_chute, 8), (g_shape, 7)]),
    ])
    make_uk(5, "air-and-water-resistance", 11, "Forces",
            "Identify the effects of air resistance, water resistance and friction, that act between moving surfaces.",
            "Air and Water Resistance",
            "Year 5 Science: Air and Water Resistance Worksheets (Parachutes and Streamlining)",
            "Air and Water Resistance",
            "Free Year 5 science worksheets on air and water resistance: parachute investigations, falling shapes in water, streamlined animals and vehicles, and forces on falling objects. 100 questions with answers.",
            "Air and water push back.",
            "Big surfaces feel more resistance; streamlined shapes slip through.",
            body(),
            [("What is air resistance?", "A force from the air that acts against objects moving through it. It slows falling objects and moving vehicles."),
             ("Why does a bigger parachute fall more slowly?", "It has a bigger area, so more air pushes against it and there is more air resistance."),
             ("What does streamlined mean?", "Having a smooth, pointed shape that lets air or water flow past easily, so there is less resistance.")],
            sets)


if __name__ == "__main__":
    main()
