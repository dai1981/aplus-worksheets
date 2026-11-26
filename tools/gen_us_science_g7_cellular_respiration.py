# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Cellular Respiration (MS-LS1-7)
  python tools/gen_us_science_g7_cellular_respiration.py
Develop a model to describe how food is rearranged through chemical reactions forming new molecules that
support growth and/or release energy as matter moves through an organism. Digestion breaks food into small
molecules; cells use glucose + oxygen -> carbon dioxide + water + energy (in mitochondria); some molecules
build new tissue. Evidence: yeast and sugar balloons, bromothymol blue turning yellow with exhaled CO2,
breathing faster during exercise. Plants respire too.
Wrong answers come from real mistakes: "only animals do respiration", "respiration is just breathing",
"energy is created from nothing", "food turns directly into energy without making new molecules".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(70107)
R = U.R
P = People(R)

IO = {"glucose (sugar)": "an input", "oxygen": "an input", "carbon dioxide": "an output", "water": "an output", "usable energy for the cell": "an output"}


def g_io():
    x = R.choice(sorted(IO))
    who = P.next()[0]
    return item("%s is modeling cellular respiration. Is %s an input or an output?" % (who, x), IO[x], ["an output" if IO[x] == "an input" else "an input", "neither", "both"],
                "Glucose + oxygen → carbon dioxide + water + energy.")


def g_compare():
    rows = [("happens in chloroplasts", "photosynthesis"), ("happens in mitochondria", "cellular respiration"), ("uses carbon dioxide and water", "photosynthesis"),
            ("uses glucose and oxygen", "cellular respiration"), ("stores light energy in sugar", "photosynthesis"), ("releases energy from sugar", "cellular respiration"),
            ("releases oxygen", "photosynthesis"), ("releases carbon dioxide", "cellular respiration"), ("happens in both plant and animal cells", "cellular respiration"),
            ("happens only in plants, algae and some bacteria", "photosynthesis")]
    a, b = R.choice(rows)
    who = P.next()[0]
    return item("%s's chart has a row that says it “%s.” Which process is it?" % (who, a), b,
                ["photosynthesis" if b == "cellular respiration" else "cellular respiration", "digestion only", "neither"],
                "Photosynthesis stores energy in sugar; respiration releases it.")


def g_yeast():
    sug = [0, 5, 10, 15]
    sizes = [R.randint(0, 2)] + sorted(R.sample(range(5, 30), 3))
    rows = [["%d g" % s, "%d cm" % c] for s, c in zip(sug, sizes)]
    who = P.next()[0]
    tab = table(["Sugar added to yeast and warm water", "Balloon width after 30 min"], rows)
    k = R.choice(["gas", "pattern", "zero"])
    if k == "gas":
        return item(tab + "In %s's experiment, which gas filled the balloons?" % who, "carbon dioxide", ["oxygen", "nitrogen", "hydrogen"],
                    "Yeast cells break down sugar and release carbon dioxide.")
    if k == "pattern":
        return item(tab + "What pattern does %s's data show?" % who, "More sugar gave the yeast more food, so more carbon dioxide was released.",
                    ["Sugar slowed the yeast down.", "The balloons filled with air from outside.", "Sugar did not matter."], "The balloon width grew with more sugar.")
    return item(tab + "Why did the balloon with 0 g of sugar barely inflate in %s's test?" % who, "The yeast had no food to break down.",
                ["The yeast was too warm.", "The balloon was broken.", "Yeast does not need food."], "No sugar, very little respiration.")


def g_body():
    who = P.next()[0]
    k = R.choice(["breath", "btb", "path", "build"])
    if k == "breath":
        r1, r2 = R.randint(12, 16), R.randint(28, 40)
        return item("%s breathes %d times a minute at rest and %d times a minute after running. Why?" % (who, r1, r2),
                    "Muscle cells need more oxygen for respiration to release more energy.", ["Running makes the lungs smaller.", "The body needs less oxygen when running.", "Breathing has nothing to do with energy."],
                    "More activity, more respiration, more oxygen needed.")
    if k == "btb":
        return item("%s blows through a straw into blue bromothymol blue solution. It turns yellow. What does this show?" % who, "Exhaled breath contains carbon dioxide from cellular respiration.",
                    ["Breath contains extra oxygen.", "The straw is yellow.", "Breath has no gases."], "Bromothymol blue turns yellow when CO₂ is added.")
    if k == "path":
        return item("%s eats a sandwich. Which describes the path of the sugar in the bread?" % who, "digested into glucose → absorbed into blood → carried to cells → used in mitochondria",
                    ["stays in the stomach forever", "goes straight to the lungs", "turns directly into muscle without any reactions"], "Food molecules are broken down and rearranged.")
    return item("%s's body uses food in two main ways. Which pair is correct?" % who, "to release energy and to build new molecules for growth and repair",
                ["only to make heat", "only to make carbon dioxide", "to make new atoms"], "Food atoms are rearranged into new molecules or broken down to release energy.")


B1 = bank([
    ("What is cellular respiration?", "a chemical process in cells that breaks down glucose with oxygen to release energy", ["breathing in and out", "making sugar from sunlight", "digesting food in the stomach"],
     "Breathing supplies the oxygen; respiration happens inside cells."),
    ("Where in the cell does cellular respiration mainly happen?", "in the mitochondria", ["in the nucleus", "in the chloroplasts", "in the cell wall"], "Mitochondria are the cell's power plants."),
    ("Do plants do cellular respiration?", "Yes. Plant cells also break down sugar to get energy.", ["No, only animals do.", "Only at night.", "Only in flowers."], "Plants make sugar and also use it."),
    ("Which equation shows cellular respiration?", "glucose + oxygen → carbon dioxide + water + energy", ["carbon dioxide + water + light → glucose + oxygen", "oxygen → glucose", "water → energy"],
     "It is like photosynthesis in reverse."),
    ("What happens to food in the digestive system before cells can use it?", "It is broken down into small molecules like glucose.", ["It stays whole.", "It becomes oxygen.", "It turns into cells right away."],
     "Small molecules can enter the blood."),
    ("Why do you exhale more carbon dioxide during exercise?", "Your cells are doing more respiration to release more energy.", ["You are making less energy.", "Your lungs make carbon dioxide from nothing.", "Exercise stops respiration."],
     "CO₂ is a product of respiration."),
    ("How do photosynthesis and respiration work together?", "The products of one are the inputs of the other.", ["They have nothing in common.", "They both make oxygen.", "They both use light."],
     "This cycles carbon and oxygen through ecosystems."),
    ("Is energy created during cellular respiration?", "No. Energy stored in sugar is released and changed into usable forms.", ["Yes, from nothing.", "Yes, from oxygen.", "Energy is destroyed."],
     "Energy is transformed, not created."),
])
B5 = bank([
    ("Ava puts yeast and sugar in warm water in one bottle and in cold water in another. The warm bottle's balloon inflates more. What does this suggest?", "Respiration in yeast is faster in warm temperatures.", ["Cold speeds up respiration.", "Temperature does not matter.", "Yeast cannot respire."],
     "Temperature affects the rate."),
    ("Leo seals a plant in a jar in the dark. The CO₂ level rises. Why?", "The plant is doing respiration but not photosynthesis in the dark.", ["The plant is doing photosynthesis.", "The jar makes CO₂.", "Light makes CO₂."],
     "Plants respire all the time."),
    ("Mia measures her pulse before and after 2 minutes of jumping. It rises. How is this connected to cellular respiration?", "The heart pumps faster to bring more oxygen and glucose to working cells.", ["The heart slows down.", "Muscles stop using oxygen.", "It is not connected."],
     "Body systems support respiration."),
    ("A student says food turns straight into energy. How would you improve this model?", "Food molecules are broken down and rearranged in chemical reactions that release energy and build new molecules.", ["Food disappears.", "Food becomes new atoms.", "The model is correct."],
     "Atoms are rearranged."),
    ("Why does bread dough rise when yeast is added?", "Yeast releases carbon dioxide gas as it breaks down sugar.", ["Yeast releases oxygen.", "Flour expands in water.", "Heat makes air."], "CO₂ bubbles make the dough rise."),
])


def body():
    think = ("<p>Living things get energy from food through <b>cellular respiration</b>, which happens in the <b>mitochondria</b> of plant and animal cells:</p>"
             "<p style='text-align:center'><b>glucose + oxygen → carbon dioxide + water + energy</b></p>"
             "<p>First, digestion breaks food into small molecules such as glucose. Blood carries glucose and oxygen to cells. In cells, chemical reactions <b>rearrange</b> the atoms: some molecules are broken down to <b>release energy</b>, and some are rebuilt into new molecules for <b>growth and repair</b>.</p>"
             "<p>Respiration is the reverse of photosynthesis, so the two processes cycle carbon and oxygen.</p>")
    ex = [("What gas fills a balloon on a bottle of yeast and sugar?", ["Yeast does respiration.", "CO₂ is a product."], "carbon dioxide"),
          ("Do plant cells do respiration?", ["All living cells need energy."], "Yes.")]
    mist = ["Thinking respiration just means breathing.",
            "Thinking only animals do respiration.",
            "Thinking food turns directly into energy without chemical reactions."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Inputs and outputs", B1 + [(g_io, 6), (g_compare, 6)]),
        ("Photosynthesis and respiration", [(g_compare, 14), (g_io, 6)]),
        ("Yeast experiments", [(g_yeast, 14), (g_body, 6)]),
        ("Food in the body", [(g_body, 12), (g_compare, 4), (g_yeast, 4)]),
        ("Modeling matter and energy", B5 + [g_body, g_yeast, g_compare, g_io]),
    ])
    make("grade-7", "cellular-respiration", 7, "MS-LS1-7",
         "Develop a model to describe how food is rearranged through chemical reactions forming new molecules that support growth and/or release energy as this matter moves through an organism.",
         "Cellular Respiration",
         "Grade 7 Cellular Respiration Worksheets: Glucose, Oxygen, Mitochondria and Energy",
         "Cellular Respiration",
         "Free middle school science worksheets on cellular respiration (NGSS MS-LS1-7): glucose and oxygen to carbon dioxide, water and energy, mitochondria, comparing photosynthesis, and yeast experiments. 100 practice questions with answers.",
         "Cells release energy from food.",
         "In mitochondria, glucose and oxygen react to form carbon dioxide and water, releasing energy for life.",
         body(),
         [("What is cellular respiration?", "A chemical process in cells that uses glucose and oxygen to release energy, producing carbon dioxide and water."),
          ("How is cellular respiration related to photosynthesis?", "They are opposite processes. Photosynthesis makes glucose and oxygen; respiration uses them and releases carbon dioxide and water."),
          ("Do plants do cellular respiration?", "Yes. Plant cells break down the sugar they make to get energy, just like animal cells.")],
         sets)


if __name__ == "__main__":
    main()
