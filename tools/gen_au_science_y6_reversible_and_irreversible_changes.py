# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 6, AC9S6U04: reversible and irreversible changes to materials (melting, freezing,
dissolving, evaporating; burning, cooking, rusting, rotting) and the signs that a new substance has formed.
  python tools/gen_au_science_y6_reversible_and_irreversible_changes.py
Reuses the UK Year 5 reversible-change makers and the US Grade 5 physical and chemical change makers with Australian names,
plus own questions on Australian contexts (bushfires, Anzac biscuits, a damper on a campfire, rusty farm sheds).
Wrong answers come from real mistakes: thinking dissolving makes a substance disappear, calling melting irreversible
because it is hard to undo, and thinking every colour change means a new substance.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 6, 6
U, R, P, src = AU(seed_of(YEAR, SORT))

UK = "gen_uk_science_y5_reversible_and_irreversible_changes"
US = "gen_us_science_g5_physical_and_chemical_changes"
uk_pick = limit(src(UK, "g_pick"), 6)
uk_rev = limit(src(UK, "g_rev"), 10)
uk_sign = limit(src(UK, "g_sign"), 3)
uk_fizz = limit(src(UK, "g_fizz"), 4)
uk_rust = limit(src(UK, "g_rust"), 3)
uk_b1 = src.B(UK, "B1")
uk_b5 = src.B(UK, "B5")
us_se = src(US, "g_sign_example")
us_chem = src(US, "g_which_chem")
us_phys = src(US, "g_which_phys")
us_table = limit(src(US, "g_table"), 3)
us_temp = limit(src(US, "g_temp"), 2)
us_b1 = src.B(US, "B1")
us_b2 = src.B(US, "B2")
us_b3 = src.B(US, "B3")
us_b5 = src.B(US, "B5", drop=["repeat an investigation"])

AUC = [("Wattle seeds are roasted on a campfire and turn dark brown.", "irreversible"), ("Damper dough is cooked in hot coals.", "irreversible"),
       ("A bushfire burns grass to ash and smoke.", "irreversible"), ("Butter melts on hot toast.", "reversible"),
       ("The roof of an old farm shed goes rusty.", "irreversible"), ("Ice in an esky melts into water.", "reversible"),
       ("Salt is left behind when sea water evaporates in salt ponds.", "reversible"),
       ("Chocolate on an Anzac biscuit melts in the sun and sets again in the fridge.", "reversible"), ("Fruit peel rots in a compost bin.", "irreversible"),
       ("Wax drips from a candle and hardens.", "reversible"), ("Anzac biscuit mixture is baked in the oven.", "irreversible")]


def g_auc():
    st, k = R.choice(AUC)
    w = ["reversible" if k == "irreversible" else "irreversible", "not a change at all", "a change that only happens in a laboratory"]
    e = ("It can be undone, so no new material is made." if k == "reversible" else "It cannot be undone, and new materials are made.")
    return tq("%s Is this a reversible or an irreversible change?" % st, k, w, e)


POOL = pool(R, [
    ("What is a reversible change?", "a change that can be undone, such as melting or freezing", ["a change that makes a new material", "a change that cannot be undone", "a change only to the colour"], "No new material is made."),
    ("What is an irreversible change?", "a change that cannot be undone and usually makes new materials", ["a change that can easily be undone", "a change in shape only", "a change in temperature only"], "Burning, cooking and rusting are irreversible."),
    ("Salt dissolves in water. Has the salt disappeared?", "No. It is spread through the water and can be got back by evaporation.", ["Yes, it is gone forever.", "Yes, it turns into water.", "It turns into a gas."], "Dissolving is reversible."),
    ("Which change is reversible?", "water evaporating from a puddle", ["a match burning", "bread toasting", "a nail rusting"], "The water vapour can condense back into water."),
    ("Which change is irreversible?", "cooking a pancake", ["melting chocolate", "freezing juice", "dissolving sugar"], "Cooking makes new substances."),
    ("Which is a sign that a new material may have been made?", "bubbles of gas, a new smell or heat given off", ["a change of shape", "being cut into pieces", "being folded"], "These are signs of a chemical change."),
    ("How could you get sugar back from sugar water?", "Let the water evaporate.", ["Filter it through paper.", "Freeze it.", "Stir it faster."], "The sugar is left behind."),
    ("Which needs oxygen from the air?", "burning and rusting", ["melting and freezing", "dissolving and filtering", "bending and folding"], "Both react with oxygen."),
    ("Why does a rusty bike chain not turn back into shiny steel?", "Rust is a new material made from iron, water and oxygen.", ["Rust is just dirt.", "Rust melts when it is cold.", "It can be scrubbed back into iron easily."], "Rusting is irreversible."),
    ("When a candle burns, which part of the change is reversible?", "the wax melting", ["the wick burning", "the smoke forming", "the flame giving off light"], "Melted wax can set again; burning makes new gases."),
])
POOL5 = pool(R, [
    ("Mia heats 20 g of chocolate until it melts, then cools it. It weighs 20 g again. What does this show?", "Melting is reversible and no material is lost.", ["Melting makes new materials.", "Chocolate gains mass when it melts.", "The change is irreversible."], "The same material changed state."),
    ("Jack wants to find out which liquid makes iron nails rust fastest. What should he keep the same?", "the kind of nail, the amount of liquid and the time", ["the liquid used", "nothing", "only the colour of the tubes"], "Only the liquid should change."),
    ("Ruby mixes bicarbonate of soda and vinegar. It fizzes and the bottle gets cold. Which conclusion is best?", "A new substance (a gas) was made.", ["Nothing new was made.", "The vinegar evaporated.", "The bottle melted."], "Bubbling is a sign of a new substance."),
    ("Kai dissolves sugar in warm and cold water. Which is a fair way to compare them?", "use the same amount of sugar, water and stirring", ["use more sugar in the cold water", "stir only the warm water", "use different cups of different sizes"], "Change only the temperature."),
    ("Why should an adult light a candle or heat food in a class investigation?", "to keep everyone safe from burns and fire", ["to make the change reversible", "to make the results bigger", "because children cannot see flames"], "Safety comes first."),
    ("Ella says, 'Cooking an egg is reversible because the egg is still there.' Why is she wrong?", "The egg's materials have changed and cannot go back to raw egg.", ["Eggs cannot be cooked.", "Cooking is always reversible.", "The egg disappears when cooked."], "New materials form when the egg cooks."),
])


def main():
    sets = U.sets([
        ("Reversible or irreversible?", [(POOL, 5), (uk_rev, 7), (g_auc, 6), (uk_b1, 2)]),
        ("Everyday changes", [(g_auc, 6), (uk_pick, 6), (us_phys, 4), (us_chem, 4)]),
        ("Signs of a new material", [(uk_sign, 3), (us_se, 7), (us_b3, 5), (POOL, 3), (us_temp, 2)]),
        ("Dissolving, melting and burning", [(POOL, 2), (us_b1, 4), (us_b2, 6), (us_chem, 4), (us_phys, 4)]),
        ("Investigations", [(POOL5, 6), (uk_fizz, 4), (uk_rust, 3), (uk_b5, 3), (us_table, 2), (us_b5, 2)]),
    ])
    make_au(YEAR, "reversible-and-irreversible-changes", SORT, "AC9S6U04", "Chemical sciences",
            "Compare reversible changes, including dissolving and changes of state, and irreversible changes, including cooking, "
            "burning and rusting, that produce new substances (summary of the Australian Curriculum v9.0 Science content description).",
            "Reversible and Irreversible Changes", "Reversible and irreversible changes",
            "Free Year 6 science worksheets on reversible and irreversible changes: melting, dissolving and evaporating, burning, cooking "
            "and rusting, and the signs of a new substance. 100 questions with answers.",
            "Can the change be undone?", "Reversible changes can be undone; irreversible changes make new materials.",
            "<p><b>Ask: can the change be undone, and is a new material made?</b></p><ul>"
            "<li>Reversible: melting, freezing, evaporating, condensing and dissolving. The material can be got back.</li>"
            "<li>Irreversible: burning, cooking, rusting and rotting. New materials are made and the change cannot be undone.</li>"
            "<li>Signs of a new material: gas bubbles, a new smell, light, heat given off or taken in, or a lasting colour change.</li></ul>",
            [("Salt dissolves in water. Reversible?", ["evaporate the water", "the salt is left"], "yes"),
             ("Damper bakes in hot coals. Reversible?", ["the dough turns into new materials"], "no")],
            ["Thinking dissolved salt or sugar has disappeared.", "Calling melting irreversible because it takes time to undo.",
             "Thinking every colour change makes a new material (mixing paints does not)."],
            [("Is dissolving reversible?", "Yes. When sugar or salt dissolves, it spreads through the water. If the water evaporates, the sugar or salt is left behind."),
             ("Why is burning irreversible?", "Burning makes new materials such as ash, smoke, carbon dioxide and water vapour. These cannot be turned back into the wood or paper."),
             ("What are signs of a chemical (irreversible) change?", "Look for gas bubbles, a new smell, light, heat being given off or taken in, or a colour change that does not go back.")],
            sets)


if __name__ == "__main__":
    main()
