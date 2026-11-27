# -*- coding: utf-8 -*-
"""
Singapore Primary 4 science: Matter (Cycles)
  python tools/gen_sg_science_p4_matter.py
Matter is anything that has mass and occupies space. Light, heat, sound and shadows are not matter.
Solids have a definite shape and a definite volume; liquids have a definite volume but take the shape of their container;
gases have no definite shape or volume, fill their container and can be compressed.
PSLE-style experiments: syringes with air and water, measuring the volume of a stone with a measuring cylinder,
showing that air has mass and occupies space. UK Year 4 states of matter questions are reused (no particle model here).
Wrong answers come from real mistakes: "air has no mass", "a liquid has a definite shape", "light is matter",
"a gas has a definite volume", "sand is a liquid because it pours".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63403)
R = U.R
P = People(R)
SL = use(U, "gen_uk_science_y4_solids_liquids_and_gases", drop=["particle", "fizzy", "helium", "winter", "snow"])

MATTER = ["air", "water", "a stone", "steam", "cooking oil", "a wooden block", "sand", "oxygen", "milk", "an ice cube", "a coin", "the gas in a balloon"]
NOT_MATTER = ["light", "heat", "sound", "a shadow", "a rainbow's colours", "electricity", "a thought", "a reflection in a mirror"]


def g_matter():
    k = R.choice(["is", "isnot"])
    if k == "is":
        a = R.choice(MATTER)
        w = R.sample(NOT_MATTER, 3)
        q = "Which of these is matter?"
        e = "%s has mass and occupies space." % (a[0].upper() + a[1:])
    else:
        a = R.choice(NOT_MATTER)
        w = R.sample(MATTER, 3)
        q = "Which of these is NOT matter?"
        e = "%s has no mass and does not occupy space." % (a[0].upper() + a[1:])
    if not once(("mt", a)):
        return None
    return item(q, a, w, e)


STATES = {"solid": ("has a definite shape and a definite volume", ["a coin", "an eraser", "a pencil", "an ice cube", "a block of wood", "a glass marble", "a grain of rice"]),
          "liquid": ("has a definite volume but no definite shape", ["water", "cooking oil", "milk", "soya sauce", "orange juice", "honey", "liquid soap"]),
          "gas": ("has no definite shape and no definite volume", ["air", "steam", "oxygen", "carbon dioxide", "water vapour", "the gas in a balloon"])}


def g_state():
    s = R.choice(list(STATES))
    a = R.choice(STATES[s][1])
    k = R.choice(["what", "which"])
    if not once(("st", k, a)):
        return None
    if k == "what":
        return item("Is %s a solid, a liquid or a gas?" % a, "a " + s, ["a " + x for x in STATES if x != s] + ["not matter"], "It %s." % STATES[s][0])
    others = [R.choice(STATES[x][1]) for x in STATES if x != s] + [R.choice(NOT_MATTER)]
    return item("Which of these is a %s?" % s, a, others, "A %s %s." % (s, STATES[s][0]))


PROPS = [("has a definite shape", "solids"), ("takes the shape of its container", "liquids and gases"), ("has a definite volume", "solids and liquids"),
         ("can be compressed (squashed into a smaller space) easily", "gases"), ("fills up the whole of any container it is in", "gases"),
         ("keeps its shape when moved from a bowl to a plate", "solids"), ("can be poured but cannot be compressed easily", "liquids")]


def g_prop():
    p, a = R.choice(PROPS)
    if not once(("pp", p)):
        return None
    w = [x for x in ["solids", "liquids", "gases", "solids and liquids", "liquids and gases", "solids and gases"] if x != a]
    return item("Which state of matter %s?" % p, a, R.sample(w, 3),
                "Solids: definite shape and volume. Liquids: definite volume, no definite shape. Gases: no definite shape or volume.")


def g_cyl():
    v0 = R.choice([40, 50, 60, 70])
    obj = R.choice(["stone", "metal key", "glass marble", "toy car", "lump of plasticine"])
    dv = R.choice([5, 8, 10, 12, 15, 20])
    k = R.choice(["vol", "why", "new", "float"])
    if k in ("vol", "new"):
        if not once(("cy", k, obj, dv)) or not once(("cyn", k), 6 if k == "vol" else 3):
            return None
    elif not once(("cy", k)):
        return None
    q0 = "A measuring cylinder had %d ml of water. When a %s was put in, the water rose to %d ml." % (v0, obj, v0 + dv)
    if k == "vol":
        return item(q0 + " What is the volume of the %s?" % obj, "%d cm³" % dv, ["%d cm³" % (v0 + dv), "%d cm³" % v0, "%d cm³" % (2 * dv)],
                    "%d − %d = %d ml, and 1 ml = 1 cm³." % (v0 + dv, v0, dv))
    if k == "why":
        return item(q0 + " Why did the water level rise?", "The %s takes up space and pushes the water up." % obj, ["The %s absorbs water." % obj, "The water became warmer.", "The %s melted." % obj],
                    "Matter occupies space, so two things cannot be in the same place.")
    if k == "new":
        return item(q0 + " A second, identical %s was added. What would the reading be?" % obj, "%d ml" % (v0 + 2 * dv), ["%d ml" % (v0 + dv), "%d ml" % (v0 + dv + 1), "%d ml" % (2 * (v0 + dv))],
                    "Each one takes up %d cm³." % dv)
    return item(q0 + " Why can this method not be used for a cork?", "A cork floats, so it does not go fully under the water.", ["A cork has no volume.", "A cork is a liquid.", "A cork has no mass."],
                "The object must be fully under the water.")


def g_syr():
    k = R.choice(["air", "water", "why", "comp", "mass"])
    if not once(("sy", k)):
        return None
    nm = P.next()[0]
    if k == "air":
        return item("%s sealed the tip of a syringe filled with air and pushed the plunger. What happened?" % nm, "The plunger moved in a little, because air can be compressed.",
                    ["The plunger could not move at all.", "The air escaped through the plastic.", "The air turned into water."], "Gases can be compressed.")
    if k == "water":
        return item("%s sealed the tip of a syringe filled with water and pushed the plunger. What happened?" % nm, "The plunger hardly moved, because water cannot be compressed easily.",
                    ["The plunger moved in a lot.", "The water turned into air.", "The syringe became lighter."], "Liquids have a definite volume.")
    if k == "why":
        return item("Why can a syringe of air be pushed in further than a syringe of water?", "Air can be compressed; water cannot be compressed easily.",
                    ["Air is heavier than water.", "Water has no volume.", "Air has a definite volume."], "Gases have no definite volume.")
    if k == "comp":
        return item("Which of these is NOT a use of the fact that gases can be compressed?", "drinking water from a bottle", ["pumping air into a bicycle tyre", "filling a scuba diving tank", "storing cooking gas in a cylinder"],
                    "Compressed air or gas is stored in tyres and tanks.")
    return item("%s weighed a flat football, then pumped air into it and weighed it again. What did %s find?" % (nm, nm), "The pumped-up ball was heavier.",
                ["The pumped-up ball was lighter.", "Both had the same mass.", "The ball had no mass."], "Air has mass.")


def g_bal():
    cup = R.choice([20, 25, 30, 40])
    liq = R.choice([50, 60, 75, 80, 100, 120])
    what = R.choice(["water", "cooking oil", "sand", "rice grains"])
    k = R.choice(["liq", "total", "air"])
    if not once(("bl", k, what if k != "air" else "")) or not once(("bln", k), 4):
        return None
    if k == "liq":
        return item("An empty cup has a mass of %d g. When it is filled with %s, the mass is %d g. What is the mass of the %s?" % (cup, what, cup + liq, what),
                    "%d g" % liq, ["%d g" % (cup + liq), "%d g" % cup, "%d g" % (liq + 2 * cup)], "%d − %d = %d g." % (cup + liq, cup, liq))
    if k == "total":
        return item("An empty cup has a mass of %d g. %d g of %s is put into it. What will the balance show?" % (cup, liq, what),
                    "%d g" % (cup + liq), ["%d g" % liq, "%d g" % cup, "%d g" % (liq - cup)], "%d + %d = %d g." % (cup, liq, cup + liq))
    return item("A deflated ball has a mass of %d g. After it is pumped with air, its mass is %d g. What does this show?" % (cup * 10, cup * 10 + R.randint(2, 6)),
                "Air has mass.", ["Air has no mass.", "The ball became a liquid.", "Air has a definite shape."], "The extra mass is the mass of the air pumped in.")


B1 = bank([
    ("What is matter?", "anything that has mass and occupies space", ["anything that we can see", "anything that is hard", "anything that is alive"], "Air is matter even though we cannot see it."),
    ("What are the three states of matter?", "solid, liquid and gas", ["hot, warm and cold", "hard, soft and runny", "metal, wood and plastic"], "Matter can exist in these three states."),
    ("What does 'occupies space' mean?", "takes up room", ["is heavy", "can move", "is cold"], "Two objects cannot be in the same place at the same time."),
    ("Which instrument is used to measure mass?", "an electronic balance", ["a measuring cylinder", "a ruler", "a thermometer"], "Mass is measured in grams (g) or kilograms (kg)."),
    ("Which instrument is used to measure the volume of a liquid?", "a measuring cylinder", ["a balance", "a thermometer", "a stopwatch"], "Volume is measured in ml or cm³."),
    ("Does air have mass?", "Yes. A ball pumped with air is heavier than a flat ball.", ["No, air weighs nothing.", "Only cold air has mass.", "Only when it is windy."], "Air is matter."),
    ("Why is sand called a solid even though it can be poured?", "Each grain has a definite shape and volume.", ["It is really a liquid.", "It is a gas.", "Sand is not matter."], "Many tiny solids together can be poured."),
    ("Why is light not matter?", "It has no mass and does not occupy space.", ["It is too bright.", "It moves too fast to be weighed.", "It is a liquid."], "Light is a form of energy."),
])
B2 = bank([
    ("Water is poured from a tall glass into a flat dish. What happens to its volume?", "It stays the same.", ["It increases.", "It decreases.", "It becomes zero."], "A liquid has a definite volume."),
    ("Water is poured from a tall glass into a flat dish. What happens to its shape?", "It changes to the shape of the dish.", ["It stays the shape of the glass.", "It has no shape at all.", "It becomes a solid shape."], "Liquids have no definite shape."),
    ("Air from a small balloon is let into a big empty box. What happens to the air?", "It spreads out to fill the whole box.", ["It stays in one corner.", "It turns into a liquid.", "It disappears."], "Gases fill their container."),
    ("A stone is moved from a cup to a tray. What happens to its shape and volume?", "Both stay the same.", ["Its shape changes.", "Its volume changes.", "Both change."], "Solids have a definite shape and volume."),
    ("Why does a bicycle tyre feel hard after it is pumped?", "More air has been compressed into it.", ["The rubber has become harder.", "Air has no mass.", "The tyre is full of water."], "Gases can be compressed."),
    ("Which statement about gases is correct?", "They have no definite shape and no definite volume.", ["They have a definite shape.", "They have a definite volume.", "They cannot be compressed."], "A gas fills any container it is in."),
    ("Why does an 'empty' bottle pushed upside down into water not fill up with water?", "It is full of air, which occupies space.", ["Water cannot enter plastic.", "The bottle is too small.", "Water is lighter than air."], "Air takes up space."),
    ("Which has a definite volume but no definite shape?", "cooking oil", ["a wooden ruler", "steam", "oxygen"], "Oil is a liquid."),
])
B3 = bank([
    ("A balloon is blown up. What fills it?", "air, which occupies space", ["nothing", "water", "light"], "The balloon gets bigger because air takes up space."),
    ("1 litre of water is poured into a 2-litre bottle. What is the volume of the water now?", "1 litre", ["2 litres", "half a litre", "3 litres"], "The volume of a liquid does not change with the container."),
    ("Why do you need to make a second hole in a can of milk to pour it out smoothly?", "Air needs to get in to take the place of the milk.", ["The milk needs light.", "The can is too heavy.", "Milk has no volume."], "Air and milk cannot occupy the same space."),
    ("A sealed syringe contains 30 cm³ of air. The plunger is pushed in. What happens to the volume of air?", "It becomes smaller.", ["It becomes larger.", "It stays at 30 cm³.", "It becomes zero at once."], "Gases can be compressed."),
    ("Which of these can be compressed the most?", "air", ["water", "a stone", "cooking oil"], "Gases can be compressed; solids and liquids hardly can."),
    ("Why is steam a gas?", "It has no definite shape or volume and spreads out.", ["It is hot.", "It is white.", "It is wet."], "Steam is water in its gas state."),
])
B5 = bank([
    ("Siti pushed an upside-down cup into a tank of water. A tissue stuck inside the cup stayed dry. Why?", "Air in the cup occupied the space and kept the water out.", ["Water cannot touch tissue.", "The cup was waterproof only.", "The tissue was magnetic."], "Air is matter: it occupies space."),
    ("Ravi weighed a balloon before and after blowing it up. What was he trying to find out?", "whether air has mass", ["whether air is a liquid", "whether balloons float", "whether balloons are magnetic"], "The mass increased a little, so air has mass."),
    ("A pupil poured 100 ml of water into four different-shaped containers and measured the volume each time. What did she find?", "The volume was 100 ml each time.", ["The volume changed with the container.", "The tallest container had the most water.", "The widest container had the least water."], "Liquids have a definite volume."),
    ("Why should the measuring cylinder be read at eye level?", "to get an accurate reading", ["to make the water rise", "to keep the water warm", "to make the reading bigger"], "Looking from above or below gives a wrong reading."),
    ("A stone made the water in a measuring cylinder rise from 50 ml to 65 ml. A second stone made it rise from 50 ml to 58 ml. Which stone has the bigger volume?", "the first stone (15 cm³)", ["the second stone (8 cm³)", "both the same", "cannot be found"], "The bigger rise means the bigger volume."),
    ("Mei Ling filled a syringe with sand and sealed the tip. She could push the plunger in a little. Why?", "There is air between the grains of sand.", ["Sand is a gas.", "Sand is a liquid.", "Sand has no volume."], "The air between the grains can be compressed."),
])


def body():
    think = ("<p><b>Matter is anything that has mass and occupies space.</b> Air, water and stones are matter. Light, heat, sound and shadows are not.</p>"
             "<ul><li><b>Solid</b>: definite shape and definite volume.</li>"
             "<li><b>Liquid</b>: definite volume, but takes the shape of its container.</li>"
             "<li><b>Gas</b>: no definite shape or volume; fills its container and can be compressed.</li></ul>"
             "<p>Measure mass with a balance. Measure the volume of a liquid with a measuring cylinder (1 ml = 1 cm³).</p>")
    ex = [("Water rises from 40 ml to 52 ml when a stone is added. Find the volume of the stone.", ["52 − 40 = 12 ml", "1 ml = 1 cm³"], "12 cm³."),
          ("A syringe of air is sealed and pushed. Why does the plunger move in?", ["Air is a gas", "Gases can be compressed"], "The air is compressed.")]
    mist = ["Thinking air has no mass. A pumped-up ball is heavier than a flat one.",
            "Thinking liquids have a definite shape. They take the shape of their container.",
            "Thinking light, heat or a shadow is matter. They have no mass.",
            "Thinking a gas has a definite volume. It spreads out to fill its container."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is matter?", B1 + [(g_matter, 6), (g_state, 4), (SL.g_state, 2)]),
        ("Solids, liquids and gases", B2 + [(g_state, 5), (g_prop, 4), (SL.g_pick, 3)]),
        ("Shape, volume and compression", B3 + [(g_prop, 3), (g_syr, 4), (g_cyl, 3), (SL.g_prop, 2), (g_matter, 2)]),
        ("Measuring mass and volume", SL.B1 + [(g_cyl, 4), (g_bal, 4), (g_state, 3), (g_matter, 3), (SL.g_pick, 4), (g_syr, 2)]),
        ("PSLE-style experiments", B5 + SL.B5 + [(g_cyl, 4), (g_syr, 3), (g_bal, 4), (g_prop, 2)]),
    ])
    make_sg(4, "matter", 3, "Cycles", "Cycles in matter and water (Matter)",
            "Recognise that matter is anything that has mass and occupies space, and that it exists in three states: solid, liquid and gas. "
            "Compare the states in terms of shape and volume, and show that gases can be compressed. Measure mass and volume "
            "(summary of the MOE Primary Science Syllabus).",
            "Matter: Solids, Liquids and Gases",
            "Primary 4 Science: Matter Worksheets – Solids, Liquids and Gases (with Answers)",
            "Matter",
            "Free Primary 4 science worksheets for Singapore pupils on matter: mass and volume, solids, liquids and gases, compressing air, and measuring with a measuring cylinder. 100 questions with answers.",
            "Matter has mass and occupies space.",
            "Solids, liquids and gases differ in shape and volume.",
            body(),
            [("Is air matter?", "Yes. Air has mass (a pumped-up ball is heavier than a flat one) and it occupies space (it stops water filling an upside-down cup)."),
             ("What is the difference between a liquid and a gas?", "A liquid has a definite volume but takes the shape of its container. A gas has no definite shape or volume, fills its container and can be compressed."),
             ("How do I find the volume of a stone?", "Put it in a measuring cylinder of water. The rise in the water level is the volume of the stone (1 ml = 1 cm³).")],
            sets)


if __name__ == "__main__":
    main()
