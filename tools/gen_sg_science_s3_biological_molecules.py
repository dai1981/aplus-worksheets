# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Biology (6093), Topic 3: Biological Molecules
  python tools/gen_sg_science_s3_biological_molecules.py
Water as a solvent; carbohydrates (monosaccharides, disaccharides, polysaccharides: starch, glycogen, cellulose), fats (glycerol
and fatty acids) and proteins (amino acids joined by peptide bonds), condensation and hydrolysis; food tests (Benedict's, iodine,
biuret, ethanol emulsion); enzymes as biological catalysts: lock-and-key specificity and the effects of temperature and pH.
US macromolecule makers and UK enzyme and food-test makers are reused (Singapore names); the rest is written here.
Wrong answers come from real mistakes: "sucrose is a reducing sugar", "Benedict's turns blue when positive", "enzymes are killed
by heat", "glycogen is stored in plants", "each amino acid is joined by a glycosidic bond".
"""
from sg_ol import OL, seed_of, make_ol, tq, rows, pool

LV, SUBJ, SORT = 3, "Biology", 21
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

us_dehyd = src("gen_us_science_bio_carbon_and_macromolecules", "g_dehyd", drop=["nucleotide", "DNA"], rep=[("dehydration synthesis", "condensation"), ("starch chain", "polysaccharide chain")])
uk_test = src("gen_uk_science_y10_organisation_and_enzymes", "g_test")
uk_rate = src("gen_uk_science_y10_organisation_and_enzymes", "g_rate")
uk_enz = src("gen_uk_science_y8_food_and_digestion", "g_enz")

SUG = [("glucose", "monosaccharide"), ("fructose", "monosaccharide"), ("galactose", "monosaccharide"), ("maltose", "disaccharide"), ("sucrose", "disaccharide"),
       ("lactose", "disaccharide"), ("starch", "polysaccharide"), ("glycogen", "polysaccharide"), ("cellulose", "polysaccharide")]


def g_sug():
    s, t = R.choice(SUG)
    return tq("What type of carbohydrate is %s?" % s, "a " + t, ["a " + x for x in ("monosaccharide", "disaccharide", "polysaccharide", "lipid") if x != t], "Mono = one sugar unit, di = two, poly = many.")


MADE = [("maltose", "two glucose molecules"), ("sucrose", "glucose and fructose"), ("lactose", "glucose and galactose"), ("starch", "many glucose molecules (stored in plants)"),
        ("glycogen", "many glucose molecules (stored in animals)"), ("a fat (triglyceride)", "glycerol and three fatty acids"), ("a protein", "amino acids joined by peptide bonds")]
g_made = rows(R, MADE, "What is %s made from?", "Which molecule is made from %s?")

BEN = [("blue (no change)", "no reducing sugar"), ("green", "a trace of reducing sugar"), ("yellow", "a small amount of reducing sugar"),
       ("orange", "a moderate amount of reducing sugar"), ("brick-red", "a large amount of reducing sugar")]


def g_ben():
    c, m = R.choice(BEN)
    food = R.choice(["a sucrose solution", "egg white", "a starch suspension", "cooking oil"] if m.startswith("no ") else
                    ["grape juice", "a solution of crushed banana", "milk", "a honey solution", "apple juice", "a pear extract", "a diluted glucose drink"])
    if R.random() < 0.5:
        return tq("%s is heated with Benedict's solution and turns %s. What does this show?" % (food[0].upper() + food[1:], c.split(" (")[0]), m,
                  [x for _, x in BEN if x != m][:3], "Benedict's solution changes from blue through green, yellow and orange to brick-red as the amount of reducing sugar increases.")
    return tq("%s contains %s. What colour is seen after heating with Benedict's solution?" % (food[0].upper() + food[1:], m.replace("no reducing", "no reducing")), c,
              R.sample([x for x, _ in BEN if x != c], 3), "Blue → green → yellow → orange → brick-red as reducing sugar increases.")


FT = [("starch", "iodine solution", "orange-brown to blue-black"), ("reducing sugar", "Benedict's solution, heated in a water bath", "blue to brick-red precipitate"),
      ("protein", "biuret solution", "blue to violet (purple)"), ("fat", "ethanol, then water (emulsion test)", "a cloudy white emulsion")]


def g_ft():
    f, r_, c = R.choice(FT)
    k = R.choice(["reag", "col", "which"])
    o = [x for x in FT if x[0] != f]
    if k == "reag":
        return tq("Which test is used for %s?" % f, r_, [x[1] for x in o], "Learn the reagent and the positive result for each food test.")
    if k == "col":
        return tq("What is a positive result in the test for %s?" % f, c, [x[2] for x in o], "Learn the reagent and the positive result for each food test.")
    return tq("A food sample gives %s. Which substance is present?" % c, f, [x[0] for x in o], "Learn the reagent and the positive result for each food test.")


ENZ = [("an enzyme", "a protein that acts as a biological catalyst"), ("the active site", "the part of an enzyme where the substrate binds"),
       ("the substrate", "the molecule an enzyme acts on"), ("denaturation", "a permanent change in the shape of the active site caused by high temperature or extreme pH"),
       ("the optimum temperature", "the temperature at which an enzyme works fastest"), ("specificity", "an enzyme acts only on one substrate because their shapes are complementary")]
g_enzd = rows(R, ENZ, "What is meant by %s?", "Which term means %s?")

COND = [("salivary amylase at 37 °C, pH 7", "starch is digested quickly"), ("salivary amylase boiled and cooled, then added to starch", "starch is not digested"),
        ("pepsin at pH 2", "protein is digested quickly"), ("pepsin at pH 8", "protein is digested very slowly or not at all"),
        ("salivary amylase at 5 °C", "starch is digested very slowly"), ("amylase added to a protein (egg white)", "the protein is not digested")]
g_cond = rows(R, COND, "What happens with %s?", "Which experiment gives this result: %s?")

POOL1 = pool(R, [
    ("Why is water important in living organisms?", "It is a solvent in which reactions take place and substances are transported.", ["It is a source of energy.", "It forms cell walls.", "It is an enzyme."], "Blood plasma and cytoplasm are mostly water."),
    ("Which chemical elements are found in all carbohydrates?", "carbon, hydrogen and oxygen", ["carbon, hydrogen and nitrogen", "carbon and nitrogen only", "carbon, hydrogen, oxygen and sulfur"], "Proteins also contain nitrogen."),
    ("Which element is found in proteins but not in carbohydrates or fats?", "nitrogen", ["carbon", "hydrogen", "oxygen"], "Amino acids have an amine group."),
    ("What is hydrolysis?", "breaking a large molecule into smaller ones by adding water", ["joining small molecules and removing water", "burning a molecule in oxygen", "changing the shape of an enzyme"], "Digestion uses hydrolysis."),
    ("What is a condensation reaction?", "joining small molecules into a larger one with the removal of water", ["breaking molecules by adding water", "a reaction that needs light", "dissolving in water"], "Making starch from glucose."),
    ("Why is starch a good storage molecule?", "It is insoluble, so it does not affect water potential, and it is compact.", ["It is soluble and sweet.", "It contains nitrogen.", "It is easily denatured."], "Animals store glycogen instead."),
    ("Why is fat a good energy store?", "It releases about twice as much energy per gram as carbohydrate.", ["It dissolves in water.", "It is a catalyst.", "It contains nitrogen."], "Fat also insulates the body."),
    ("Which sugar is non-reducing?", "sucrose", ["glucose", "maltose", "fructose"], "Sucrose gives no change with Benedict's unless first hydrolysed."),
    ("Why do enzymes work slowly at low temperatures?", "The molecules have less kinetic energy, so there are fewer collisions between enzyme and substrate.", ["The enzyme is denatured.", "The active site is destroyed.", "There is no substrate."], "The enzyme works again when warmed."),
    ("What is the lock-and-key hypothesis?", "The substrate fits into the active site like a key into a lock.", ["Enzymes lock substrates away.", "Every enzyme fits every substrate.", "The enzyme is used up in the reaction."], "This explains why enzymes are specific."),
])
POOL5 = pool(R, [
    ("An enzyme's activity falls sharply above 45 °C and does not recover when cooled. Why?", "The enzyme is denatured: the shape of its active site has changed permanently.", ["The enzyme has been killed.", "The enzyme has melted.", "The substrate has run out."], "Enzymes are proteins, not living things."),
    ("Why does pepsin work in the stomach but not in the small intestine?", "Its optimum pH is about 2; the small intestine is alkaline.", ["The small intestine is too cold.", "There is no protein in the small intestine.", "Pepsin is used up in the stomach."], "Each enzyme has an optimum pH."),
    ("Why are biological washing powders less effective in very hot water?", "The enzymes in them are denatured.", ["The enzymes are dissolved.", "Hot water removes all stains anyway.", "The enzymes work faster than the water."], "They work best at about 40 °C."),
    ("A sample gives a blue-black colour with iodine and a violet colour with biuret. What does it contain?", "starch and protein", ["sugar and fat", "starch only", "protein and sugar"], "Iodine: starch. Biuret: protein."),
    ("Why is the Benedict's test heated in a water bath rather than over a flame?", "to heat it evenly and safely to about 80 °C", ["to cool it", "to make it turn blue", "to stop the reaction"], "A boiling water bath is used."),
    ("A sucrose solution gives a brick-red precipitate with Benedict's only after boiling with dilute acid. Why?", "The acid hydrolyses sucrose into glucose and fructose, which are reducing sugars.", ["The acid is a reducing sugar.", "Sucrose is a reducing sugar.", "Benedict's reacts with acid."], "The acid is neutralised before the test."),
    ("Why can amylase digest starch but not protein?", "The shape of its active site is complementary only to starch.", ["Protein is too small.", "Amylase is a carbohydrate.", "Protein has no bonds."], "Enzymes are specific."),
    ("Cellulose and starch are both made of glucose. Why can humans not digest cellulose?", "Humans do not make an enzyme that breaks the bonds in cellulose.", ["Cellulose is not made of glucose.", "Cellulose is a protein.", "Cellulose dissolves in water."], "Cellulose is dietary fibre."),
])


def main():
    sets = U.sets([
        ("Carbohydrates, fats and proteins", [(g_sug, 7), (g_made, 7), (POOL1, 4), (g_ft, 2)]),
        ("Building and breaking molecules", [(us_dehyd, 11), (POOL1, 4), (g_made, 4), (g_sug, 1)]),
        ("Food tests", [(g_ft, 8), (g_ben, 8), (uk_test, 4)]),
        ("Enzymes", [(g_enzd, 7), (g_cond, 6), (uk_enz, 4), (uk_rate, 3)]),
        ("Exam-style questions", [(POOL5, 8), (uk_rate, 3), (g_ben, 4), (g_cond, 3), (g_enzd, 2)]),
    ])
    make_ol(LV, SUBJ, "biological-molecules", SORT, "Biological Molecules",
            "State the roles of water in living organisms; describe the structure of carbohydrates, fats and proteins in terms of their smaller basic units, and "
            "condensation and hydrolysis; describe and carry out tests for starch, reducing sugars, protein and fats; explain enzyme action using the lock-and-key "
            "hypothesis, and investigate and explain the effects of temperature and pH on enzyme activity (summary of the Singapore-Cambridge O-Level Biology 6093 "
            "syllabus).",
            "Biological Molecules", "Biological molecules",
            "Free Secondary 3 O-Level Biology worksheets on biological molecules: carbohydrates, fats, proteins, food tests, Benedict's test, enzymes, temperature and "
            "pH. 100 questions with answers.",
            "Big molecules are chains of small units.", "Enzymes are proteins: specific, and denatured by heat or extreme pH.",
            "<p><b>Know the units and the tests.</b></p><ul>"
            "<li>Starch, glycogen and cellulose: many glucose. Fats: glycerol + 3 fatty acids. Proteins: amino acids joined by peptide bonds.</li>"
            "<li>Condensation joins units (water removed); hydrolysis breaks them (water added).</li>"
            "<li>Iodine: blue-black (starch). Benedict's, heated: blue → brick-red (reducing sugar). Biuret: violet (protein). Ethanol: cloudy emulsion (fat).</li>"
            "<li>Enzymes have an active site that fits one substrate. Activity rises to an optimum temperature, then falls as the enzyme is denatured.</li></ul>",
            [("6 glucose join to make a chain. Water molecules?", ["5 bonds form", "one water per bond"], "5"),
             ("Biuret turns violet. Present?", ["biuret tests protein"], "protein")],
            ["Saying enzymes are “killed” by heat.", "Saying sucrose is a reducing sugar.", "Mixing up glycogen (animals) and starch (plants).",
             "Saying a positive Benedict's test stays blue."],
            [("What is the difference between starch, glycogen and cellulose?", "All are polysaccharides of glucose. Starch is the storage carbohydrate in plants, glycogen in animals, and cellulose forms plant cell walls."),
             ("Why do enzymes stop working at high temperatures?", "Above the optimum temperature the enzyme is denatured: the shape of the active site changes, so the substrate no longer fits."),
             ("How do you test for a reducing sugar?", "Add Benedict's solution and heat in a boiling water bath. A green, yellow, orange or brick-red precipitate shows a reducing sugar.")],
            sets)


if __name__ == "__main__":
    main()
