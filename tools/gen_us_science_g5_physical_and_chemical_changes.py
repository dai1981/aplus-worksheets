# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Physical and Chemical Changes (5-PS1-4)
  python tools/gen_us_science_g5_physical_and_chemical_changes.py
When two substances are mixed, do they make a new substance? Physical changes (shape, size, state,
dissolving) keep the same substances. Chemical changes make new substances, with evidence such as
gas bubbles, a new color, a temperature change, light, a new solid or a new smell.
Wrong answers come from real mistakes: "melting makes a new substance", "any color change is
chemical (mixing paints)", "dissolving destroys the sugar", "boiling bubbles are a new gas".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(50103)
R = U.R
P = People(R)

CHEM = ["an iron bike chain rusting", "wood burning in a campfire", "baking a cake", "frying an egg", "milk going sour",
        "baking soda fizzing in vinegar", "a silver spoon tarnishing", "a sliced apple turning brown", "a glow stick lighting up",
        "fireworks exploding", "toast browning in a toaster", "food being digested in your stomach", "a candle wick burning",
        "a copper roof turning green", "bread dough rising with yeast", "a fizzing antacid tablet in water", "leaves rotting in a compost pile"]
PHYS = ["ice melting in a cup", "cutting paper into strips", "crushing an aluminum can", "dissolving sugar in tea", "water boiling in a pot",
        "freezing juice into pops", "breaking a glass", "mixing sand and pebbles", "bending a paper clip", "stretching a rubber band",
        "chopping wood for a fire", "melting butter in a pan", "tearing a sheet of foil", "water vapor condensing on a mirror",
        "grinding pepper", "mixing salt into water", "shaping clay into a pot", "a puddle evaporating"]


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ set 1
def g_which_chem():
    a = R.choice(CHEM)
    w = R.sample(PHYS, 3)
    return item("Which is a <b>chemical</b> change?", a, w, cap(a) + " makes a new substance. The others only change shape, size or state, or mix things.")


def g_which_phys():
    a = R.choice(PHYS)
    w = R.sample(CHEM, 3)
    return item("Which is a <b>physical</b> change?", a, w, cap(a) + " does not make a new substance. The others all make new substances.")


def g_classify():
    if R.random() < 0.5:
        x = R.choice(CHEM)
        return item("What kind of change is " + x + "?", "a chemical change, because a new substance forms",
                    ["a physical change, because only the shape changes", "a physical change, because only the state changes", "no change at all"],
                    cap(x) + " makes a new substance with new properties, so it is a chemical change.")
    x = R.choice(PHYS)
    return item("What kind of change is " + x + "?", "a physical change, because no new substance forms",
                ["a chemical change, because a new substance forms", "a chemical change, because it gives off light", "no change at all"],
                cap(x) + " changes the shape, size, state or mixture, but the substances stay the same.")


B1 = bank([
    ("What is a chemical change?", "a change that makes one or more new substances", ["a change in shape only", "a change from solid to liquid", "any change you can see"],
     "In a chemical change, the particles join in new ways to make new substances with new properties."),
    ("What is a physical change?", "a change in shape, size or state where no new substance forms", ["a change that always gives off light", "a change that makes a new substance", "a change that can never be undone"],
     "Cutting, melting, freezing and dissolving are physical changes. The substance is still the same."),
    ("Ice melts into water. Is water a new substance?", "No. Ice and water are the same substance in different states.", ["Yes, because it is a liquid now.", "Yes, because it changed shape.", "Yes, because it got warmer."],
     "Changing state is a physical change. Water can freeze back into the same ice."),
    ("Which change can usually be undone easily?", "freezing water into ice", ["burning a log", "baking a cake", "rusting a nail"],
     "Many physical changes can be reversed: ice can melt again. Most chemical changes cannot be undone easily."),
    ("A new substance has", "different properties from the substances that formed it", ["exactly the same properties as before", "no properties", "the same color always"],
     "Rust is red-brown and crumbly, very different from shiny, strong iron. Different properties tell you it is a new substance."),
    ("Which word best describes what happens to particles in a chemical change?", "They rearrange to form new substances.", ["They disappear.", "They only move farther apart.", "They stop moving."],
     "No particles disappear. They join together in new ways, which makes new substances."),
])


# ------------------------------------------------------------ set 2: physical changes
B2 = bank([
    ("Sugar dissolves in water. Why is this a physical change?", "The sugar is still sugar; the water can evaporate to get it back.", ["The sugar is destroyed.", "A new gas forms.", "The water turns into sugar."],
     "Dissolving makes a mixture. Evaporate the water and the sugar crystals are left behind."),
    ("Which is <b>not</b> a sign of a physical change?", "a gas forming when two liquids mix", ["a change in shape", "a change in size", "a change from liquid to gas when heated"],
     "A new gas from mixing can mean a new substance. Changing shape, size or state are physical changes."),
    ("Water boils and bubbles form. Is this evidence of a new substance?", "No. The bubbles are water vapor, the same substance as a gas.", ["Yes, the bubbles are a new gas.", "Yes, because it is hot.", "Yes, because the water disappears."],
     "Boiling is a change of state. The bubbles are water in its gas form."),
    ("Mixing blue paint and yellow paint makes green paint. What kind of change is this?", "a physical change: the two paints are mixed", ["a chemical change, because the color changed", "a chemical change, because it gives off heat", "not a change at all"],
     "The colors only blend. Not every color change means a new substance."),
    ("Sand and iron filings are mixed. Which shows the mixing was a physical change?", "A magnet can pull the iron filings back out.", ["The mixture is gray.", "The mixture is heavier.", "The mixture is dry."],
     "If you can separate the parts and they are unchanged, no new substance formed."),
    ("Which is a physical change to a piece of paper?", "folding it into an airplane", ["burning it", "letting it rot in soil", "letting it turn yellow in the sun for years"],
     "Folding changes the shape only. It is still paper."),
    ("A chocolate bar melts in a hot car and then hardens again in the fridge. What kind of changes are these?", "both physical changes", ["both chemical changes", "melting is chemical, hardening is physical", "melting is physical, hardening is chemical"],
     "Melting and freezing are changes of state. The chocolate is still chocolate."),
    ("Salt water is heated until the water is gone and salt is left. What does this show about dissolving salt?", "It was a physical change: the salt was still there.", ["It was a chemical change.", "The salt was destroyed.", "The water turned into salt."],
     "The same salt comes back, so no new substance had formed."),
    ("Which change makes a mixture, not a new substance?", "stirring raisins into cereal", ["burning a match", "cooking an egg", "rusting a steel can"],
     "Raisins and cereal can be picked apart. Each keeps its own properties."),
    ("Lemonade powder is stirred into water and the water turns yellow. Is a new substance formed?", "No. The powder dissolves and colors the water, making a mixture.", ["Yes, because the color changed.", "Yes, because bubbles must form.", "Yes, because the powder disappears."],
     "The powder only dissolves. The color comes from the powder spreading through the water."),
])


# ------------------------------------------------------------ set 3: signs of chemical change
SIGNS = [("Bubbles of gas form when two substances are mixed.", "a new gas"), ("The mixture changes to a color that neither substance had.", "a new color"),
         ("The mixture gets much warmer or colder by itself.", "a temperature change"), ("The mixture gives off light.", "light"),
         ("A solid forms when two clear liquids are mixed.", "a new solid"), ("A new smell is produced.", "a new smell")]
NOT_SIGNS = ["The substance changes shape.", "The substance melts.", "The substance breaks into smaller pieces.", "The substance dissolves in water.",
             "The water boils and bubbles.", "The substance freezes."]


def g_sign():
    a, _ = R.choice(SIGNS)
    w = R.sample(NOT_SIGNS, 3)
    return item("Which observation is evidence that a <b>new substance</b> may have formed?", a, w,
                "Gas from mixing, a new color, a temperature change, light, a new solid or a new smell are signs of a chemical change. Shape and state changes are physical.")


def g_sign_example():
    ex = [("Baking soda is added to vinegar and it fizzes.", "gas bubbles", "g"), ("A match is struck and it flames.", "light and heat", "lt"),
          ("A nail left outside turns red-brown and flaky.", "a new color and a new solid", "cs"), ("Two clear liquids are mixed and a cloudy white solid appears.", "a new solid", "s"),
          ("A cake batter rises and turns brown in the oven.", "gas and a new color", "gc"), ("Milk left out for days smells sour.", "a new smell", "m"),
          ("A hand warmer pack is opened and gets hot.", "a temperature change", "t"), ("A glow stick is bent and starts to glow.", "light", "l"),
          ("An antacid tablet is dropped in water and fizzes.", "gas bubbles", "g"), ("A banana peel turns black.", "a new color", "c")]
    one = {"g": "gas bubbles", "l": "light", "c": "a new color", "s": "a new solid", "m": "a new smell", "t": "a temperature change"}
    s_, sign, tags = R.choice(ex)
    others = [v for k, v in sorted(one.items()) if k not in tags and not (k == "t" and "h" in sign)]
    w = R.sample(others, 2) + ["a change of shape only"]
    return item(s_ + " What evidence of a chemical change is there?", sign, w, "The observation shows " + sign + ", which is evidence that a new substance formed.")


B3 = bank([
    ("A sparkler is lit and gives off bright light and sparks. What kind of change is this?", "a chemical change", ["a physical change", "a change of state only", "no change"],
     "The metal powder in a sparkler burns and makes new substances, giving off light and heat."),
    ("Which kitchen change makes a new substance?", "toasting bread until it turns brown", ["slicing bread", "freezing bread", "squashing bread flat"],
     "Toasting changes the bread into new brown substances with a new smell and taste."),

    ("When baking soda and vinegar are mixed, bubbles form. What are the bubbles?", "a new gas (carbon dioxide)", ["air that was already in the cup", "water vapor from boiling", "tiny pieces of baking soda"],
     "The fizzing is a new gas, carbon dioxide, made by the chemical change."),
    ("Iron rusts in wet air. Which property shows rust is a new substance?", "Rust is red-brown and crumbles instead of being shiny and strong.", ["Rust is heavier.", "Rust is a solid, like iron.", "Rust is the same color as iron."],
     "Rust has different properties from iron, so it is a new substance."),
    ("A bubbling mixture is not always a chemical change. Which example only has a physical change?", "boiling water", ["vinegar on baking soda", "yeast in bread dough", "an antacid tablet in water"],
     "Boiling water makes bubbles of water vapor. No new substance forms."),
    ("Which change gives off both light and heat as a new substance forms?", "a candle burning", ["a light bulb glowing", "ice melting", "a flashlight shining"],
     "Burning wax makes new substances (gases and soot) and gives off light and heat. A light bulb changes no substance."),
    ("Why is cooking an egg a chemical change?", "The runny egg turns into a solid with new properties that cannot change back.", ["The egg gets hot.", "The egg shell breaks.", "The egg is in a pan."],
     "Cooking changes the egg into new substances. You cannot uncook an egg."),
    ("A student mixes two clear liquids, and a yellow solid appears. What is the solid?", "a new substance made by the mixing", ["dust from the air", "frozen water", "the liquids changing shape"],
     "A new solid that forms when two liquids mix is evidence of a chemical change."),
])


# ------------------------------------------------------------ set 4: data
LIQ = ["Liquid A", "Liquid B", "Liquid C", "Liquid D"]


def g_temp():
    t0 = R.randint(18, 24)
    sub, sign = R.choice([(("vinegar", "baking soda"), -1), (("salt water", "iron powder from a hand warmer"), 1),
                          (("hydrogen peroxide", "yeast"), 1), (("vinegar", "steel wool"), 1)])
    d = sign * R.choice([3, 4, 5, 6, 7, 8, 9, 11])
    p = P.next()
    q = ("%s mixes %s and %s. The thermometer reads %d °C before mixing and %d °C one minute later. What does this temperature change suggest?"
         % (p[0], sub[0], sub[1], t0, t0 + d))
    return item(q, "A new substance may have formed.", ["Nothing changed.", "The thermometer is broken.", "The mixture changed shape only."],
                "The temperature changed by %d degrees on its own. A temperature change when substances mix is evidence of a chemical change." % abs(d))


def g_table():
    rows = []
    obs = [("bubbles, temperature went up", 1), ("turned purple, a solid formed", 1), ("no change", 0), ("color mixed to light green", 0),
           ("fizzed, smelled sharp", 1), ("powder dissolved, no other change", 0), ("glowed, got warm", 1), ("liquid got cloudy and a solid settled", 1)]
    pick = R.sample(obs, 4)
    if not any(x[1] for x in pick) or all(x[1] for x in pick):
        return None
    for i, (o, _) in enumerate(pick):
        rows.append(["Test %d" % (i + 1), o])
    ask = R.choice([1, 0])
    good = [i for i, (_, c) in enumerate(pick) if c == ask]
    if len(good) != 1:
        return None
    k = good[0]
    w = ["Test %d" % (i + 1) for i in range(4) if i != k]
    word = "most likely made a new substance" if ask else "most likely did <b>not</b> make a new substance"
    return item(table(["Mixture", "What was observed"], rows) + "Which test %s?" % word, "Test %d" % (k + 1), w,
                ("Test %d shows %s: evidence of a new substance." if ask else "Test %d shows %s: no sign of a new substance.") % (k + 1, pick[k][0]))


def g_mass_hint():
    a = R.choice([50, 80, 100, 120, 150])
    b = R.choice([10, 15, 20, 25])
    return item("A sealed bag holds %d g of vinegar and a small cup with %d g of baking soda. The bag is tipped so they mix and the bag puffs up. What is the total mass now?" % (a, b),
                "%d g" % (a + b), ["%d g" % a, "%d g" % (a + b + 5), "%d g" % (a - b)],
                "A new gas forms, but the bag is sealed, so nothing gets out: %d + %d = %d g. The particles are rearranged, not destroyed." % (a, b, a + b))


B4 = bank([
    ("A student mixes a white powder into water. The water gets cloudy, but after stirring it is clear. There are no bubbles and no temperature change. What is the best conclusion?", "The powder dissolved; no new substance is evident.", ["A new substance formed.", "The powder was destroyed.", "The water became a gas."],
     "Dissolving alone is a physical change. There was no evidence of a new substance."),
    ("A class mixes milk with vinegar. White lumps form and float in a clear liquid. What is the evidence of a new substance?", "A new solid (the lumps) formed.", ["The milk was cold.", "The vinegar is a liquid.", "The cup got wet."],
     "Solid curds forming from two liquids is evidence of a chemical change."),
    ("Which result would show that mixing two substances did <b>not</b> make a new substance?", "The mixture can be separated into the same two substances.", ["Bubbles keep forming.", "The mixture glows.", "A new smell appears."],
     "If you can get back the same substances, the change was physical."),
])


# ------------------------------------------------------------ set 5: investigations
B5 = bank([
    ("Two cups of milk are left out, one in a warm room and one in the fridge. Which will most likely smell sour first?", "the milk in the warm room", ["the milk in the fridge", "both at the same time", "neither, milk never changes"],
     "Souring is a chemical change made by tiny living things. It happens faster when it is warm."),
    ("Luis wants to know if salt makes ice melt faster. Which is the best plan?", "Put the same size ice cubes on two plates, add salt to one, and time both.", ["Use a big cube with salt and a small cube without.", "Put salt on both cubes.", "Time only the salted cube."],
     "Change only one thing (the salt) and compare with a cube that has no salt."),
    ("A student says that burning paper is a physical change because the ashes are still paper. Which evidence shows the student is wrong?", "Ash, smoke and gases have different properties from paper, and they cannot turn back into paper.", ["The paper got smaller.", "The paper was flat.", "The paper was white."],
     "Burning makes new substances. Ash cannot be made back into a sheet of paper."),
    ("Which observation would show that rusting is faster in salt water than in fresh water?", "Nails in salt water get more rust in the same number of days.", ["Nails in fresh water stay longer.", "Salt water is clear.", "Both nails are the same size."],
     "Compare the amount of rust after the same time. More rust means a faster chemical change."),
    ("Zoe mixes 3 spoonfuls of baking soda with vinegar and gets a lot of bubbles. With 1 spoonful she gets fewer bubbles. What did she change?", "the amount of baking soda", ["the kind of vinegar", "the temperature", "the shape of the cup"],
     "Only the amount of baking soda changed, so that is the variable she tested."),
    ("Why do scientists repeat an investigation several times?", "to check that the results are reliable", ["to make the results different", "to use up materials", "to change the question"],
     "If the same results happen again and again, you can trust them more."),

    ("Kai wants to test whether yeast makes a gas when mixed with sugar water. What should he use as a control?", "the same sugar water with no yeast", ["yeast with no water", "a cup with more yeast", "a different kind of cup"],
     "The control is identical except for the yeast, so any difference is caused by the yeast."),
    ("Mia drops the same size antacid tablet into cold water and hot water. Which variable is she testing?", "the temperature of the water", ["the size of the tablet", "the kind of tablet", "the kind of cup"],
     "Only the water temperature is different, so that is the variable she is testing."),
    ("In Mia's test, the tablet fizzes faster in hot water. What is the best conclusion?", "The chemical change happens faster at a higher temperature.", ["Hot water makes a physical change.", "The tablet is bigger in hot water.", "Cold water has no particles."],
     "Warmer particles move faster and react more quickly."),
    ("Ben puts a steel wool pad in a jar with a little water and seals it. After a week it is orange. Why does he also keep a dry steel wool pad in a sealed jar?", "to see if water is needed for rusting", ["to make the test faster", "to weigh the water", "to make more rust"],
     "Comparing wet and dry steel wool shows whether water affects rusting."),
    ("Which safety rule is most important when testing mixtures in class?", "Wear safety goggles and never taste the mixtures.", ["Mix as many things as possible.", "Smell each mixture closely.", "Work without an adult."],
     "Unknown mixtures can be harmful. Goggles protect your eyes, and you should never taste them."),
    ("Ava mixes two liquids and sees no bubbles, no color change and no temperature change. Can she be sure no new substance formed?", "Not completely; she can test more properties of the mixture.", ["Yes, she is completely sure.", "No, a new substance always forms.", "Yes, because liquids never react."],
     "Not every chemical change is easy to see. More tests (like testing with a magnet or heating) can give more evidence."),
    ("A team bakes two cakes: one with baking powder and one without. Only one rises. What does the baking powder do?", "It reacts to make gas bubbles that make the cake rise.", ["It makes the cake heavier.", "It cools the batter.", "It melts in the oven."],
     "Baking powder makes carbon dioxide gas when wet and heated. The bubbles puff up the cake."),
    ("Which question can be answered by mixing two substances and observing?", "Does mixing vinegar and baking soda make a new substance?", ["Why is the sky blue?", "How many planets are there?", "How tall is the school?"],
     "You can test it in class: mix them, observe the bubbles and compare properties."),
])


def body():
    think = ("<p>When substances change, ask: <b>is there a new substance?</b></p>"
             "<p>In a <b>physical change</b> the substance stays the same. Its shape, size or state changes, or it mixes or dissolves. "
             "Melting ice, cutting paper and dissolving sugar are physical changes.</p>"
             "<p>In a <b>chemical change</b> the particles rearrange to make <b>new substances</b> with new properties. "
             "Rusting, burning, cooking an egg and mixing baking soda with vinegar are chemical changes.</p>"
             + table(["Evidence of a new substance", "Example"], [["gas bubbles from mixing", "baking soda + vinegar"], ["a new color", "a nail rusting"],
                                                                 ["a temperature change", "a hand warmer heating up"], ["light", "a glow stick"],
                                                                 ["a new solid from two liquids", "milk + vinegar making curds"], ["a new smell", "milk going sour"]]))
    ex = [("Is boiling water a chemical change? It makes bubbles.", ["The bubbles are water vapor.", "Water vapor is still water, only as a gas."], "No. It is a physical change (change of state)."),
          ("Vinegar is poured on baking soda. It fizzes and the cup feels cooler. What kind of change is it?", ["Fizzing from mixing: a new gas.", "The temperature changed on its own."], "A chemical change.")]
    mist = ["Calling melting, freezing or boiling a chemical change. A change of state is physical.",
            "Thinking every color change means a new substance. Mixing paints only blends colors.",
            "Thinking dissolving destroys a substance. The salt or sugar can be recovered.",
            "Thinking boiling bubbles are a new gas. They are water vapor."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("New substance or not?", [g_which_chem, g_which_phys, g_classify] + B1),
        ("Physical changes", [g_which_phys, g_classify] + B2),
        ("Signs of a chemical change", [g_sign, g_sign_example] + B3),
        ("Reading investigation data", [g_temp, g_table, g_mass_hint] + B4),
        ("Investigations", [g_table, g_temp] + B5),
    ])
    make("grade-5", "physical-and-chemical-changes", 4, "5-PS1-4",
         "Conduct an investigation to determine whether the mixing of two or more substances results in new substances.",
         "Physical and Chemical Changes",
         "Grade 5 Physical and Chemical Changes Worksheets: New Substances, Evidence and Tests",
         "Physical and Chemical Changes",
         "Free Grade 5 science worksheets on physical and chemical changes (NGSS 5-PS1-4): new substances, signs like gas bubbles, color and temperature changes, and fair tests of mixing substances. 100 practice questions with answers.",
         "A chemical change makes a new substance; a physical change does not.",
         "Gas from mixing, a new color, a temperature change, light, a new solid or a new smell are evidence of a new substance.",
         body(),
         [("What is the difference between a physical and a chemical change?", "A physical change changes shape, size or state, or mixes substances, but no new substance forms. A chemical change makes new substances with new properties, such as rust from iron."),
          ("What are signs of a chemical change?", "Gas bubbles when substances mix, a new color, a temperature change, light, a new solid forming from two liquids, or a new smell."),
          ("Is dissolving sugar a chemical change?", "No. It is a physical change. The sugar is still there and can be recovered by evaporating the water."),
          ("Is boiling water a chemical change?", "No. The bubbles are water vapor, which is still water. Boiling is a change of state.")],
         sets)


if __name__ == "__main__":
    main()
