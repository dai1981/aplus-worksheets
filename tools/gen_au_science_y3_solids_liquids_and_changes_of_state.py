# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 3, AC9S3U04: solids and liquids, and how adding or removing heat makes a solid melt
or a liquid freeze (melting points; reversible changes).
  python tools/gen_au_science_y3_solids_liquids_and_changes_of_state.py
Reuses the UK Year 4 solids-liquids and changes-of-state makers and the SG Primary 5 heat makers with Australian names; gases
are left to Year 5. Own questions on melting and freezing in Australian contexts (chocolate in a hot car, icy poles, butter).
Wrong answers come from real mistakes: thinking sand is a liquid because it pours, thinking ice "disappears" when it melts,
and thinking freezing needs a freezer (water freezes at 0 °C anywhere).
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 3, 5
U, R, P, src = AU(seed_of(YEAR, SORT))

SL = "gen_uk_science_y4_solids_liquids_and_gases"
CS = "gen_uk_science_y4_changes_of_state"
SG = "gen_sg_science_p5_water_and_changes_of_state"
import re
NOGAS = []
_GAS = re.compile(r"\b(gas|gases|vapour|steam|evaporat\w*|condens\w*|boil\w*|carbon dioxide|oxygen|helium|bubbles|air)\b", re.I)


def ng(f):
    """keep items whose question and answer do not need gases (Year 3 is solids and liquids); a gas option becomes another wrong answer"""
    def g():
        it = f()
        if not it:
            return None
        a = it["c"][it["a"]]
        if _GAS.search(re.sub(r"<[^>]+>", " ", it["q"]) + " " + a):
            return None
        fill = [x for x in ["none of these", "both of these", "it depends on its colour", "neither of these"] if x not in it["c"]]
        it["c"] = [fill.pop(0) if _GAS.search(c) and c != a else c for c in it["c"]]
        if len({c.lower() for c in it["c"]}) < 4:
            return None
        return it
    return g
sl_state = limit(ng(src(SL, "g_state", rep=[(r"a solid, a liquid or a gas", "a solid or a liquid")])), 6)
sl_pick = limit(ng(src(SL, "g_pick", drop=NOGAS)), 5)
sl_prop = ng(src(SL, "g_prop", drop=NOGAS))
sl_b5 = ng(src.B(SL, "B5", drop=NOGAS))
cs_ex = ng(src(CS, "g_ex", drop=NOGAS))
cs_mp = limit(src(CS, "g_mp"), 6)
cs_heat = limit(ng(src(CS, "g_heat", drop=NOGAS)), 3)
cs_word = ng(src(CS, "g_word", drop=NOGAS))
cs_b5 = ng(src.B(CS, "B5", drop=NOGAS))
sg_heat = ng(src(SG, "g_heat", drop=NOGAS))
sg_b5 = ng(src.B(SG, "B5", drop=NOGAS))

SOL = [("an ice cube", "solid"), ("a wooden block", "solid"), ("a rock", "solid"), ("sand", "solid"), ("sugar", "solid"), ("a coin", "solid"),
       ("butter from the fridge", "solid"), ("a crayon", "solid"), ("milk", "liquid"), ("honey", "liquid"), ("orange juice", "liquid"),
       ("cooking oil", "liquid"), ("sea water", "liquid"), ("melted chocolate", "liquid"), ("shampoo", "liquid"), ("tomato sauce", "liquid")]


def g_sol():
    o, k = R.choice(SOL)
    return tq("Is %s a solid or a liquid?" % o, "a " + k, ["a liquid" if k == "solid" else "a solid", "neither: it is a mixture of light", "it changes every second"],
              {"solid": "Solids keep their own shape.", "liquid": "Liquids flow and take the shape of their container."}[k] +
              (" Each grain of sand or sugar is a solid, even though the grains can be poured." if o in ("sand", "sugar") else ""))


CH = [("Chocolate left in a hot car goes soft and runny.", "melting"), ("Water in an ice-cube tray turns hard in the freezer.", "freezing (solidifying)"),
      ("An icy pole drips on a hot day.", "melting"), ("Candle wax drips down and hardens on the table.", "freezing (solidifying)"),
      ("Butter in a frying pan turns into a liquid.", "melting"), ("Melted chocolate sets hard on a cake in the fridge.", "freezing (solidifying)"),
      ("Snow on Mount Kosciuszko turns to water in spring.", "melting"), ("Hot jelly sets in the fridge.", "freezing (solidifying)"),
      ("An ice block in an esky becomes water.", "melting"), ("Hot wax from a crayon sets in a mould.", "freezing (solidifying)")]


def g_ch():
    st, k = R.choice(CH)
    return tq("%s Which change is this?" % st, k, [x for x in ["melting", "freezing (solidifying)", "dissolving", "burning"] if x != k],
              "Melting: solid to liquid when heat is added. Freezing: liquid to solid when heat is removed.")


MP = [("ice", 0), ("butter", 32), ("chocolate", 34), ("candle wax", 60), ("crayon wax", 65), ("sugar", 186), ("salt", 801), ("iron", 1538)]


def g_mp():
    from au_sci import once
    if R.random() < 0.6:
        (a, x), (b, y) = R.sample(MP, 2)
        k = R.choice(["lower", "higher"])
        ans = a if (x < y) == (k == "lower") else b
        if not once(("mp", tuple(sorted((a, b))), k)):
            return None
        return tq("Which melts at a %s temperature: %s or %s?" % (k, a, b), ans, [b if ans == a else a, "They melt at the same temperature.", "Neither can ever melt."],
                  "Melting points: %s about %d °C, %s about %d °C." % (a, x, b, y))
    m, t = R.choice(MP)
    if not once(("car", m)):
        return None
    yes = t < 60
    return tq("On a summer day, the inside of a parked car reaches about 60 °C. Will %s left in the car melt?" % m,
              "Yes, because it melts below 60 °C." if yes else "No, because it melts above 60 °C.",
              ["No, because it melts above 60 °C." if yes else "Yes, because it melts below 60 °C.", "Only if it is wet.", "Only at night."],
              "%s melts at about %d °C." % (m[0].upper() + m[1:], t))


POOL1 = pool(R, [
    ("Why do icy poles melt faster in Darwin than in Hobart in winter?", "Darwin is much warmer, so more heat is added.", ["Hobart is closer to the Sun.", "Icy poles are different there.", "Darwin has no air."], "Warmer surroundings give more heat."),
    ("What is the solid form of water called?", "ice", ["steam", "rain", "salt"], "Water is solid below 0 °C."),
    ("Which of these is a liquid at room temperature?", "cooking oil", ["butter from the fridge", "a candle", "sugar"], "Oil flows and takes the shape of its container."),
    ("Lava cools and becomes rock. Which change is this?", "freezing (solidifying)", ["melting", "dissolving", "burning"], "Liquid rock becomes solid rock as it loses heat."),
    ("Why is metal melted to make cans and car parts?", "As a liquid it can be poured into moulds, then cooled into a solid shape.", ["Melted metal is lighter.", "Melting makes new metal.", "Solid metal cannot be cooled."], "Melting and freezing are reversible."),
    ("What happens when a solid is heated enough?", "It melts and becomes a liquid.", ["It becomes harder.", "It disappears.", "It becomes heavier."], "Adding heat causes melting."),
    ("What must happen for a liquid to freeze?", "Heat must be taken away so it cools.", ["Heat must be added.", "It must be stirred.", "It must be poured."], "Removing heat causes freezing."),
    ("At what temperature does pure water freeze?", "0 °C", ["100 °C", "10 °C", "37 °C"], "Ice melts at the same temperature."),
    ("Is melting a reversible change?", "Yes. The liquid can be frozen again.", ["No, it can never be undone.", "Only for chocolate.", "Only in winter."], "No new material is made."),
    ("An ice cube melts in a glass. Has the water disappeared?", "No. The same water is now a liquid.", ["Yes, it has gone.", "It has turned into glass.", "It has turned into air."], "The amount of water stays the same."),
    ("Why does chocolate melt in your hand but not in the fridge?", "Your hand is warmer than chocolate's melting point; the fridge is colder.", ["Hands are wet.", "The fridge is dark.", "Chocolate is a liquid."], "Each solid melts at its own temperature."),
    ("Which melts fastest on a hot sunny day?", "an icy pole", ["a rock", "a metal spoon", "a wooden block"], "Ice has a very low melting point."),
    ("Why is sand called a solid even though you can pour it?", "Each grain keeps its own shape.", ["It is a liquid.", "It flows like water.", "It has no shape."], "Pouring tiny solids is not the same as flowing like a liquid."),
    ("Which describes a liquid?", "It flows and takes the shape of its container.", ["It keeps its own shape.", "It cannot be poured.", "It is always hot."], "Liquids keep the same amount but change shape."),
    ("What tool measures the temperature at which something melts?", "a thermometer", ["a ruler", "scales", "a magnet"], "Melting points are measured in °C."),
])
POOL5 = pool(R, [
    ("Mia puts the same-sized pieces of butter, chocolate and cheese in the sun. Butter melts first, then chocolate, then cheese. What does this show?", "Different solids melt at different temperatures.", ["All solids melt at the same time.", "Cheese is a liquid.", "The Sun only melts butter."], "Each solid has its own melting point."),
    ("In Mia's test, what should she keep the same?", "the size of each piece and where she puts them", ["the type of food", "nothing", "the result"], "Change only the material."),
    ("Jack times how long ice cubes take to melt: in the sun 8 minutes, in the shade 20 minutes, in the fridge 3 hours. What pattern does he find?", "The warmer the place, the faster the ice melts.", ["The colder the place, the faster it melts.", "Place makes no difference.", "Ice melts fastest in the fridge."], "More heat makes melting faster."),
    ("Kai puts a chocolate button on a plate in the sun and one in the shade. Which melts first?", "the one in the sun", ["the one in the shade", "both at the same time", "neither will melt"], "More heat is added in the sun."),
    ("Ella melts some chocolate, pours it into a mould and puts it in the fridge. What will happen?", "It becomes solid again in the shape of the mould.", ["It stays a liquid forever.", "It turns into a gas.", "It disappears."], "Melting can be reversed by cooling."),
    ("Noah wants to test which ice cube melts fastest: one in water, one in air, one in salt. What must be the same for each?", "the size of the ice cubes and the starting temperature", ["the place each one is put", "nothing", "the time each melts"], "Change only one thing."),
    ("Ruby fills a cup with water, marks the level and freezes it. What does she notice?", "The ice takes up a little more space than the water did.", ["The ice takes up much less space.", "The water disappears.", "The cup gets bigger by itself."], "Water expands when it freezes."),
])


def main():
    sets = U.sets([
        ("Solid or liquid?", [(g_sol, 8), (sl_state, 6), (POOL1, 6)]),
        ("Properties of solids and liquids", [(sl_prop, 6), (POOL1, 5), (g_sol, 5), (sl_b5, 1), (cs_word, 3)]),
        ("Melting and freezing", [(g_ch, 10), (cs_ex, 4), (sg_heat, 4), (POOL1, 2)]),
        ("Melting points", [(cs_mp, 6), (g_mp, 12), (cs_heat, 2)]),
        ("Investigations", [(POOL5, 7), (cs_b5, 3), (sg_b5, 2), (g_mp, 3), (g_sol, 3), (cs_ex, 2)]),
    ])
    make_au(YEAR, "solids-liquids-and-changes-of-state", SORT, "AC9S3U04", "Chemical sciences",
            "Compare the properties of solids and liquids and describe how adding or removing heat causes a change of state between solid "
            "and liquid (summary of the Australian Curriculum v9.0 Science content description).",
            "Solids, Liquids and Changes of State", "Solids and liquids",
            "Free Year 3 science worksheets on solids and liquids, melting and freezing, and melting points, with examples such as icy poles, "
            "chocolate and candle wax. 100 questions with answers.",
            "Heat melts; cooling freezes.", "Solids keep their shape, liquids flow; adding or removing heat changes one into the other.",
            "<p><b>Solids keep their own shape. Liquids flow and take the shape of their container.</b></p><ul>"
            "<li>Adding heat can melt a solid into a liquid (ice, chocolate, butter, wax).</li>"
            "<li>Removing heat can freeze a liquid into a solid. Water freezes and ice melts at 0 °C.</li>"
            "<li>Melting and freezing are reversible: the material stays the same, only its state changes.</li></ul>",
            [("An icy pole drips in the sun. Which change?", ["heat is added", "solid to liquid"], "melting"),
             ("Is sand a solid?", ["each grain keeps its shape"], "yes")],
            ["Thinking sand or sugar is a liquid because it can be poured.", "Thinking ice disappears when it melts.",
             "Thinking freezing needs a freezer (water freezes at 0 °C wherever it is that cold)."],
            [("What is the difference between a solid and a liquid?", "A solid keeps its own shape. A liquid flows and takes the shape of its container, but the amount stays the same."),
             ("What is a melting point?", "It is the temperature at which a solid melts. Ice melts at 0 °C; chocolate melts at about 30–35 °C."),
             ("Is melting reversible?", "Yes. When a melted solid cools, it can become solid again, like melted chocolate setting on a cake.")],
            sets)


if __name__ == "__main__":
    main()
