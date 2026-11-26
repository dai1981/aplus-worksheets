# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Properties and Chemical Reactions (MS-PS1-2)
  python tools/gen_us_science_g7_properties_and_chemical_reactions.py
Analyze and interpret data on the properties of substances before and after they interact to determine if a
chemical reaction has occurred. Characteristic properties: density, melting point, boiling point, solubility,
flammability, odor. A new substance has different characteristic properties. Signs: gas, color change,
precipitate, temperature change, new smell. Physical changes keep the same substance.
Wrong answers come from real mistakes: "melting is a chemical reaction", "a change in shape makes a new
substance", "dissolving sugar makes a new substance", "any bubbles mean a chemical reaction" (boiling).
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(70102)
R = U.R
P = People(R)

CHEM = ["baking soda and vinegar fizz and make a gas", "an iron nail rusts in damp air", "wood burns to ash and smoke", "a cake batter bakes into a cake",
        "milk turns sour and smells bad", "a copper statue turns green over many years", "two clear liquids mix and form a solid yellow powder", "a glow stick is bent and starts to glow",
        "a match lights", "an apple slice turns brown in the air", "fireworks explode with colors", "food is digested in the stomach"]
PHYS = ["an ice cube melts", "water boils and turns to steam", "sugar dissolves in tea", "a piece of paper is cut into strips", "a glass bottle breaks",
        "butter softens in a warm room", "salt is mixed with sand", "a rubber band is stretched", "water freezes into ice", "chocolate is melted and poured into a mold",
        "clay is shaped into a bowl", "wax is melted"]


def g_kind():
    who = P.next()[0]
    if R.random() < 0.5:
        x = R.choice(CHEM)
        return item("%s observes that %s. Is this a chemical change or a physical change?" % (who, x), "a chemical change, because a new substance forms",
                    ["a physical change, because only the shape or state changes", "neither", "a physical change, because it is a mixture"],
                    "Gas, color change, new smell, light, heat or a new solid are signs of a new substance.")
    x = R.choice(PHYS)
    return item("%s observes that %s. Is this a chemical change or a physical change?" % (who, x), "a physical change, because no new substance forms",
                ["a chemical change, because a new substance forms", "neither", "a chemical change, because it looks different"],
                "The substance is still the same; only its shape, size or state changed.")


def g_which():
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s lists changes in the kitchen. Which is a chemical change?" % who, R.choice(CHEM), R.sample(PHYS, 3), "A new substance with new properties forms.")
    return item("%s lists changes around the house. Which is a physical change?" % who, R.choice(PHYS), R.sample(CHEM, 3), "The substance stays the same.")


SUBST = [("water", "1.00 g/cm³", "0 °C", "100 °C", "dissolves in water", "does not burn"),
         ("table salt", "2.16 g/cm³", "801 °C", "1,413 °C", "dissolves in water", "does not burn"),
         ("sugar", "1.59 g/cm³", "186 °C", "decomposes", "dissolves in water", "burns"),
         ("baking soda", "2.20 g/cm³", "decomposes at 50 °C", "—", "dissolves in water", "does not burn"),
         ("vegetable oil", "0.92 g/cm³", "−17 °C", "about 300 °C", "does not dissolve in water", "burns"),
         ("iron", "7.87 g/cm³", "1,538 °C", "2,862 °C", "does not dissolve in water", "does not burn as a block"),
         ("rust (iron oxide)", "5.24 g/cm³", "1,565 °C", "—", "does not dissolve in water", "does not burn"),
         ("carbon dioxide", "0.0018 g/cm³", "—", "—", "dissolves a little in water", "does not burn")]


def g_table():
    who = P.next()[0]
    case = R.choice(["rust", "mix", "dissolve", "melt"])
    if case == "rust":
        before = [["iron nail", "gray, shiny", "7.87 g/cm³", "attracted to a magnet"]]
        after = [["orange-brown flakes", "orange-brown, dull", "5.24 g/cm³", "not attracted to a magnet"]]
        q = "%s left an iron nail in salt water for a week. The table shows properties before and after. Did a chemical reaction happen?" % who
        a, w = "Yes. The flakes have different properties, so a new substance formed.", ["No. Only the shape changed.", "No. The density stayed the same.", "No. Iron cannot change."]
        e = "The color, density and magnetism all changed, so the orange-brown flakes are a new substance (rust)."
    elif case == "mix":
        before = [["clear liquid A", "colorless", "1.05 g/cm³", "no smell"], ["clear liquid B", "colorless", "1.10 g/cm³", "no smell"]]
        after = [["mixture", "yellow solid forms", "—", "no smell"]]
        q = "%s mixed two clear liquids. The table shows what happened. What is the best conclusion?" % who
        a, w = "A chemical reaction happened, because a new solid formed.", ["A physical change happened, because both were liquids.", "Nothing happened.", "Liquid A melted."]
        e = "A solid that forms from two liquids (a precipitate) is evidence of a new substance."
    elif case == "dissolve":
        before = [["sugar", "white crystals", "1.59 g/cm³", "sweet"], ["water", "clear", "1.00 g/cm³", "no taste"]]
        after = [["sugar water", "clear", "1.10 g/cm³", "sweet; sugar returns when the water evaporates"]]
        q = "%s dissolved sugar in water. The table shows properties before and after. Did a chemical reaction happen?" % who
        a, w = "No. The sugar is still there and can be recovered, so no new substance formed.", ["Yes. The sugar disappeared.", "Yes. The density changed.", "Yes. Water turned into sugar."]
        e = "Dissolving is a physical change; the sugar's properties come back when the water evaporates."
    else:
        before = [["solid wax", "white, solid", "0.90 g/cm³", "melts at 60 °C"]]
        after = [["liquid wax", "clear, liquid", "0.80 g/cm³", "hardens again at 60 °C"]]
        q = "%s heated candle wax until it melted. Did a chemical reaction happen?" % who
        a, w = "No. It is still wax with the same melting point.", ["Yes. It turned into a liquid.", "Yes. The density changed a little, so it is new.", "Yes. Heat always makes new substances."]
        e = "Melting changes the state, not the substance. Its characteristic melting point stays the same."
    tab = table(["Substance", "Appearance", "Density", "Other"], before + [["→ after", "", "", ""]] + after)
    return item(tab + q, a, w, e)


def g_prop():
    s = R.choice(SUBST)
    who = P.next()[0]
    k = R.choice(["dens", "sol"])
    if k == "dens":
        others = [x for x in SUBST if x[0] != s[0]]
        return item("%s measures an unknown substance. Its density is %s. Using a reference table, which substance could it be?" % (who, s[1]), s[0],
                    [x[0] for x in R.sample(others, 3)], "Density is a characteristic property: %s has a density of %s." % (s[0], s[1]))
    return item("Which is a characteristic property that can help identify %s?" % s[0], "its density, %s" % s[1],
                ["its shape", "its mass", "its volume"], "Density, melting point and boiling point do not depend on the amount, so they help identify a substance.")


B1 = bank([
    ("What is a chemical reaction?", "a process in which atoms rearrange to form new substances with new properties", ["a change in shape only", "a change of state like melting", "mixing sand and salt"],
     "New substances have different properties."),
    ("Which is a characteristic property of a substance?", "its boiling point", ["its mass", "its volume", "its shape"], "Characteristic properties do not depend on the amount."),
    ("Which observation is evidence of a chemical reaction?", "a gas forms when two substances mix", ["ice melts", "a stick breaks", "sugar dissolves"], "A new gas is a new substance."),
    ("Water boils and makes bubbles. Is this evidence of a chemical reaction?", "No. The bubbles are water vapor, the same substance.", ["Yes, all bubbles mean a reaction.", "Yes, because it gets hot.", "Yes, because steam is new."],
     "Boiling is a change of state."),
    ("How can density help identify a substance?", "Each pure substance has its own density.", ["Density depends on the shape.", "All substances have the same density.", "Density changes with size."],
     "Density = mass ÷ volume."),
    ("Burning a log produces ash, smoke and gases. What does this show?", "New substances formed, so it is a chemical reaction.", ["It is a physical change.", "The log only changed shape.", "No change happened."],
     "The ash has different properties from wood."),
    ("Why is cutting paper a physical change?", "It is still paper with the same properties.", ["Paper turns into a new substance.", "It releases a gas.", "It changes color."], "Only the size and shape changed."),
    ("A substance has a melting point of 0 °C and a boiling point of 100 °C. What is it most likely?", "water", ["salt", "iron", "oil"], "Those are water's characteristic properties."),
])
B5 = bank([
    ("Ava mixes vinegar and baking soda in a bag. The bag puffs up and feels cold. Name two pieces of evidence of a chemical reaction.", "gas formed and the temperature changed", ["the bag got bigger only because of air from outside", "nothing changed", "the vinegar melted"],
     "A new gas and a temperature change are signs of a reaction."),
    ("Leo measures the melting point of a white powder before and after heating it strongly. Before: 186 °C. After: a black solid that does not melt at 186 °C. What happened?", "a chemical reaction formed a new substance", ["the powder only melted", "nothing changed", "the thermometer broke"],
     "A different melting point means a different substance."),
    ("Mia wants to test if a change is chemical. What should she compare?", "the characteristic properties before and after", ["only the size before and after", "only the color of the container", "the time of day"],
     "New properties mean a new substance."),
    ("Why should students wear goggles when testing reactions?", "Some reactions can splash or release substances that hurt the eyes.", ["Goggles make reactions faster.", "Goggles show the properties.", "They are only for decoration."],
     "Safety first."),
    ("Two samples have the same color, but different densities and boiling points. What can you conclude?", "They are different substances.", ["They are the same substance.", "Color is enough to identify them.", "They are both water."],
     "Color alone is not a characteristic property you can rely on."),
])


def body():
    think = ("<p>Every pure substance has <b>characteristic properties</b> that do not depend on how much you have: density, melting point, boiling point, solubility, flammability and odor.</p>"
             "<p>In a <b>chemical reaction</b>, atoms rearrange to form <b>new substances</b>, so the characteristic properties change. "
             "Evidence: a gas forms, a solid forms from liquids, the color changes, the temperature changes, light is given off, or there is a new smell.</p>"
             "<p>In a <b>physical change</b> (melting, boiling, dissolving, cutting, bending), the substance stays the same. Compare properties <b>before and after</b> to decide.</p>")
    ex = [("An iron nail becomes orange-brown and is no longer magnetic. Chemical or physical?", ["Its properties changed.", "A new substance (rust) formed."], "chemical"),
          ("Ice melts into water. Chemical or physical?", ["It is still water."], "physical")]
    mist = ["Thinking melting or boiling is a chemical reaction.",
            "Thinking dissolving makes a new substance.",
            "Using mass or volume to identify a substance. Use characteristic properties."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Chemical and physical changes", B1 + [(g_kind, 6), (g_which, 6)]),
        ("Is it a reaction?", [(g_kind, 12), (g_which, 8)]),
        ("Characteristic properties", [(g_prop, 14), (g_which, 6)]),
        ("Before-and-after data", [(g_table, 8), (g_prop, 6), (g_kind, 6)]),
        ("Investigating reactions", B5 + [g_table, g_kind, g_prop, g_which]),
    ])
    make("grade-7", "properties-and-chemical-reactions", 2, "MS-PS1-2",
         "Analyze and interpret data on the properties of substances before and after the substances interact to determine if a chemical reaction has occurred.",
         "Properties and Chemical Reactions",
         "Grade 7 Chemical Reactions Worksheets: Characteristic Properties and Evidence of a Reaction",
         "Chemical Reactions",
         "Free middle school science worksheets on properties and chemical reactions (NGSS MS-PS1-2): characteristic properties like density and melting point, chemical vs. physical changes, and before-and-after data. 100 practice questions with answers.",
         "New properties mean a new substance.",
         "Compare density, melting point and other characteristic properties before and after. If they change, a chemical reaction happened.",
         body(),
         [("How can you tell if a chemical reaction happened?", "Compare characteristic properties before and after. Signs include a new gas, a new solid, a color or temperature change, light or a new smell."),
          ("What are characteristic properties?", "Properties that do not depend on the amount, such as density, melting point, boiling point, solubility and flammability."),
          ("Is dissolving sugar in water a chemical reaction?", "No. The sugar is still there and comes back when the water evaporates, so it is a physical change.")],
         sets)


if __name__ == "__main__":
    main()
