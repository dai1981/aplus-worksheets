# -*- coding: utf-8 -*-
"""
UK A level Biology question makers (Year 12 = AS content, Year 13 = the rest). Units are listed in UNITS(year).
Numbers follow the usual A level methods: magnification = image ÷ actual size, mitotic index, cardiac output = stroke volume × heart rate,
Simpson's index D = 1 − Σn(n − 1)/N(N − 1), Hardy–Weinberg p² + 2pq + q² = 1, χ² = Σ(O − E)²/E, Lincoln index N = n₁n₂/m.
Wrong answers come from real mistakes: forgetting to change mm into µm, dividing the wrong way, using n instead of n − 1,
using q² for q, forgetting to square, confusing the template and coding strands.
"""
import math
import random
from fractions import Fraction as F
from uk_alsci import nf, nq, tq, once_maker, U

R = random.Random(0)


def ch(xs):
    return R.choice(xs)


def K(f, *kinds):
    g = lambda: f(R.choice(kinds))
    g.__name__ = f.__name__ + "_" + "_".join(kinds)
    return g


def fr(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (x.numerator, x.denominator)


COMP = {"A": "T", "T": "A", "G": "C", "C": "G"}
RNA = {"A": "U", "T": "A", "G": "C", "C": "G"}


def seq(n):
    return "".join(R.choice("ATGC") for _ in range(n))


# =================================================================== Year 12: biological molecules
def m_cond(k=None):
    k = k or ch(["water", "pep", "mass", "dip", "tri"])
    n = ch([3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 50, 100, 150, 200, 300])
    if k == "water":
        return nq("How many water molecules are released when %d glucose molecules join to form a polysaccharide chain?" % n, n - 1, [n, n + 1, 2 * n], "",
                  "Each glycosidic bond releases one water molecule, and %d monomers make %d bonds: <b>%d</b>." % (n, n - 1, n - 1))
    if k == "pep":
        return nq("How many peptide bonds are in a single polypeptide chain of %d amino acids?" % n, n - 1, [n, n + 1, n // 2], "", "A chain of n amino acids has n − 1 peptide bonds: <b>%d</b>." % (n - 1))
    if k == "mass":
        if n > 50:
            return None
        return nq("Glucose has M<sub>r</sub> 180 and water 18. Calculate the M<sub>r</sub> of a straight chain of %d glucose units joined by condensation." % n, 180 * n - 18 * (n - 1),
                  [180 * n, 180 * n - 18 * n, 180 * n + 18 * (n - 1)], "", "%d × 180 − %d × 18 = <b>%d</b>." % (n, n - 1, 180 * n - 18 * (n - 1)))
    if k == "tri":
        fa = ch([256, 280, 282, 284, 278])
        return nq("Glycerol has M<sub>r</sub> 92 and a fatty acid has M<sub>r</sub> %d. Calculate the M<sub>r</sub> of the triglyceride made from glycerol and three of these fatty acids (water M<sub>r</sub> 18)." % fa,
                  92 + 3 * fa - 54, [92 + 3 * fa, 92 + 3 * fa - 18, 92 + fa - 18], "", "Three ester bonds form, releasing 3 water molecules: 92 + 3 × %d − 3 × 18 = <b>%d</b>." % (fa, 92 + 3 * fa - 54))
    a, b = ch([("glycine", 75), ("alanine", 89), ("serine", 105), ("valine", 117), ("leucine", 131), ("lysine", 146)]), ch([("glycine", 75), ("alanine", 89), ("cysteine", 121), ("tyrosine", 181), ("glutamine", 146)])
    return nq("%s (M<sub>r</sub> %d) and %s (M<sub>r</sub> %d) join to make a dipeptide. Calculate the M<sub>r</sub> of the dipeptide." % (a[0].capitalize(), a[1], b[0], b[1]), a[1] + b[1] - 18,
              [a[1] + b[1], a[1] + b[1] + 18, a[1] + b[1] - 36], "", "Condensation releases one water molecule: %d + %d − 18 = <b>%d</b>." % (a[1], b[1], a[1] + b[1] - 18))


def m_chargaff(k=None):
    a = ch(list(range(12, 39)))
    g = (100 - 2 * a) / 2
    k = k or ch(["G", "T", "C", "AT"])
    sp = ch(["a bacterium", "a plant", "a mammal", "a fungus", "an insect", "a fish"])
    if k == "T":
        return nq("In the DNA of %s, %d%% of the bases are adenine. What percentage are thymine?" % (sp, a), a, [100 - a, g, 50 - a], "%", "A pairs with T, so %%T = %%A = <b>%d%%</b>." % a)
    if k == "AT":
        return nq("In the DNA of %s, %d%% of the bases are adenine. What percentage are adenine and thymine together?" % (sp, a), 2 * a, [a, 100 - 2 * a, 100 - a], "%", "%%A + %%T = 2 × %d = <b>%d%%</b>." % (a, 2 * a))
    nm = "guanine" if k == "G" else "cytosine"
    return nq("In the DNA of %s, %d%% of the bases are adenine. What percentage are %s?" % (sp, a, nm), g, [100 - a, 100 - 2 * a, 50 - a / 2], "%",
              "A + T = %d%%, so G + C = %d%%, and %s = half of that: <b>%s%%</b>." % (2 * a, 100 - 2 * a, nm, nf(g)))


def m_dna(k=None):
    s = seq(ch([8, 9, 10, 12]))
    k = k or ch(["comp", "count"])
    if k == "count":
        bp = ch([100, 150, 200, 240, 300, 500, 600, 1000])
        return nq("A section of double-stranded DNA is %d base pairs long. How many nucleotides does it contain?" % bp, 2 * bp, [bp, bp // 2, 3 * bp], "",
                  "Each base pair is two nucleotides: <b>%d</b>." % (2 * bp))
    c = "".join(COMP[x] for x in s)
    wr = ["".join(RNA[x] for x in s), s, c[::-1] if c[::-1] != c else s[::-1], "".join({"A": "G", "G": "A", "T": "C", "C": "T"}[x] for x in s)]
    return tq("One DNA strand has the base sequence %s. What is the sequence of the complementary strand?" % s, c, wr, "A pairs with T and G pairs with C.")


MOL = [("Which bond joins two α-glucose molecules in maltose?", "an α-1,4 glycosidic bond", ["a peptide bond", "an ester bond", "a phosphodiester bond"], "Formed by a condensation reaction."),
       ("Which disaccharide is made from glucose and fructose?", "sucrose", ["lactose", "maltose", "cellulose"], "Lactose is glucose + galactose; maltose is glucose + glucose."),
       ("Which disaccharide is made from glucose and galactose?", "lactose", ["sucrose", "maltose", "glycogen"], "Found in milk."),
       ("Why is starch good for storing energy in plants?", "it is insoluble and compact, so it does not affect water potential", ["it is a protein", "it forms strong fibres", "it is soluble and moves easily"], "Amylose coils into a helix."),
       ("Why is glycogen well suited to energy storage in animals?", "it is highly branched, so glucose is released quickly", ["it is made of β-glucose", "it is soluble in water", "it contains peptide bonds"], "Enzymes act on the many branch ends."),
       ("What makes cellulose strong?", "β-glucose chains held together by many hydrogen bonds into microfibrils", ["α-glucose helices", "disulfide bridges", "ester bonds between chains"], "Alternate β-glucose molecules are inverted."),
       ("What type of reaction breaks a glycosidic bond?", "hydrolysis", ["condensation", "oxidation", "polymerisation"], "Water is used to split the bond."),
       ("What is a triglyceride made from?", "one glycerol and three fatty acids", ["three glycerols and one fatty acid", "amino acids", "glucose and phosphate"], "Joined by ester bonds."),
       ("Why do phospholipids form a bilayer in water?", "the phosphate heads are hydrophilic and the fatty acid tails are hydrophobic", ["they are proteins", "they are fully soluble", "they carry a positive charge"], "Tails point inwards, away from water."),
       ("What is an unsaturated fatty acid?", "one with at least one C=C double bond in its chain", ["one with no double bonds", "one with a phosphate group", "one that contains nitrogen"], "Double bonds put kinks in the chain."),
       ("Which bond holds the primary structure of a protein together?", "peptide bonds", ["hydrogen bonds only", "ionic bonds", "glycosidic bonds"], "The sequence of amino acids."),
       ("What is the secondary structure of a protein?", "an α-helix or β-pleated sheet held by hydrogen bonds", ["the sequence of amino acids", "the overall 3D folding", "two or more polypeptides together"], "Hydrogen bonds between –NH and –C=O groups."),
       ("Which bonds help hold the tertiary structure of a protein?", "hydrogen, ionic and disulfide bonds", ["glycosidic bonds only", "phosphodiester bonds", "ester bonds"], "Disulfide bridges form between cysteines."),
       ("What does quaternary structure describe?", "more than one polypeptide chain joined together", ["the order of amino acids", "an α-helix", "a single folded chain"], "Haemoglobin has four chains."),
       ("Which group is on every amino acid?", "an amine group and a carboxyl group", ["a phosphate group", "a glycerol group", "a nitrogenous base"], "The R group is different for each."),
       ("What is the sugar in a DNA nucleotide?", "deoxyribose", ["ribose", "glucose", "fructose"], "RNA contains ribose."),
       ("Which base is found in RNA but not DNA?", "uracil", ["thymine", "adenine", "guanine"], "Uracil replaces thymine."),
       ("What bond joins nucleotides in a polynucleotide?", "a phosphodiester bond", ["a peptide bond", "a glycosidic bond only", "a hydrogen bond"], "Between the phosphate of one and the sugar of the next."),
       ("Why is DNA replication described as semi-conservative?", "each new DNA molecule has one original strand and one new strand", ["both strands are new", "only half the DNA is copied", "the original molecule is kept whole"], "Shown by Meselson and Stahl."),
       ("What does DNA helicase do?", "breaks the hydrogen bonds between the two strands", ["joins nucleotides together", "adds RNA primers", "joins Okazaki fragments only"], "The strands separate to act as templates."),
       ("What does DNA polymerase do?", "joins new nucleotides to form phosphodiester bonds", ["breaks hydrogen bonds", "unwinds the helix only", "pairs bases"], "It works in the 5′ to 3′ direction."),
       ("What is ATP made of?", "adenine, ribose and three phosphate groups", ["adenine, deoxyribose and two phosphates", "glucose and phosphate", "thymine, ribose and three phosphates"], "ATP is a nucleotide derivative."),
       ("Why is ATP a good immediate energy source?", "hydrolysis releases a small, manageable amount of energy in one step", ["it stores a large amount of energy", "it is insoluble", "it cannot be resynthesised"], "ATP → ADP + Pᵢ."),
       ("Why is water a good solvent?", "it is polar, so ions and polar molecules dissolve in it", ["it is non-polar", "it has a low specific heat capacity", "it is ionic"], "Many reactions happen in solution."),
       ("Why does water have a high specific heat capacity?", "lots of energy is needed to break the hydrogen bonds", ["it is non-polar", "its molecules are large", "it has covalent bonds between molecules"], "It buffers temperature changes."),
       ("Why does sweating cool the body?", "water has a high latent heat of vaporisation", ["water is a good solvent", "water is dense", "water is transparent"], "Evaporation takes heat from the skin."),
       ("What is the role of phosphate ions in cells?", "they are part of DNA, RNA and ATP", ["they carry oxygen", "they form the cell wall", "they control water potential only"], "Phosphate links nucleotides."),
       ("What do hydrogen ions affect in the body?", "pH", ["temperature", "blood clotting only", "the speed of nerve impulses only"], "Enzymes work best at their optimum pH.")]
TESTS = [("Which test shows a reducing sugar?", "heat with Benedict's reagent: blue to brick-red precipitate", ["add iodine: orange to blue-black", "add biuret: blue to purple", "shake with ethanol: milky emulsion"], "All monosaccharides are reducing sugars."),
         ("Which test shows starch?", "add iodine solution: orange-brown to blue-black", ["Benedict's test: brick-red", "biuret test: purple", "emulsion test: milky white"], "Iodine fits inside the amylose helix."),
         ("Which test shows protein?", "add biuret reagent: blue to purple", ["add iodine: blue-black", "heat with Benedict's: brick-red", "add ethanol then water: milky"], "Biuret reacts with peptide bonds."),
         ("Which test shows lipids?", "shake with ethanol then add water: a milky white emulsion", ["add biuret: purple", "add iodine: blue-black", "Benedict's: green"], "Lipids form tiny droplets in water."),
         ("How do you test for a non-reducing sugar such as sucrose?", "boil with dilute HCl, neutralise, then do the Benedict's test", ["add iodine directly", "add biuret reagent", "heat with Benedict's only"], "The acid hydrolyses sucrose into reducing sugars."),
         ("A Benedict's test turns green. What does this show?", "a small amount of reducing sugar", ["no reducing sugar", "a lot of protein", "starch is present"], "More sugar gives yellow, orange then brick-red."),
         ("Why is a colorimeter useful in the Benedict's test?", "it measures the amount of sugar more objectively than by eye", ["it speeds up the reaction", "it changes the colour", "it removes the precipitate"], "Absorbance or transmission of the filtrate is measured."),
         ("Which result means no reducing sugar is present?", "the Benedict's reagent stays blue", ["the solution turns purple", "a brick-red precipitate forms", "the solution turns blue-black"], "Copper(II) ions are not reduced."),
         ("What colour shows a negative biuret test?", "blue", ["purple", "brick-red", "blue-black"], "Purple would mean protein is present."),
         ("What is chromatography used for in biology?", "separating molecules such as amino acids or pigments", ["measuring the pH", "testing for starch", "killing bacteria"], "Different molecules move different distances."),
         ("Why must the Benedict's test be heated?", "the reaction needs heat to reduce the copper(II) ions", ["to dissolve the starch", "to kill bacteria", "to change the pH"], "Use a water bath at about 80 °C or above."),
         ("Which food is likely to give a positive emulsion test?", "olive oil", ["table sugar", "egg white", "potato starch"], "Oil is a lipid."),
         ("Which food is likely to give a positive biuret test?", "egg white", ["olive oil", "table sugar", "cellulose"], "Egg white is mostly protein."),
         ("Which food is likely to give a positive iodine test?", "potato", ["olive oil", "glucose tablets", "egg white"], "Potatoes store starch."),
         ("Which sugar is NOT a reducing sugar?", "sucrose", ["glucose", "fructose", "maltose"], "Sucrose has no free reducing group.")]
ENZ = [("How do enzymes speed up reactions?", "they lower the activation energy", ["they raise the temperature", "they give molecules more energy", "they change the products"], "They provide an alternative route."),
       ("What is the induced-fit model?", "the active site changes shape slightly as the substrate binds", ["the active site is rigid", "the enzyme changes the product", "the substrate changes into the enzyme"], "This puts strain on the substrate's bonds."),
       ("Why does a high temperature stop an enzyme working?", "hydrogen and ionic bonds break and the active site changes shape (denatures)", ["the enzyme melts", "the substrate becomes too small", "the peptide bonds break"], "The substrate no longer fits."),
       ("Why does the rate of an enzyme reaction level off at high substrate concentration?", "all the active sites are occupied", ["the enzyme is denatured", "the substrate is used up", "the temperature falls"], "Enzyme concentration is now the limiting factor."),
       ("How does a competitive inhibitor work?", "it binds to the active site, so substrate cannot bind", ["it binds elsewhere and changes the active site shape", "it destroys the enzyme", "it changes the pH"], "Adding more substrate reduces its effect."),
       ("How does a non-competitive inhibitor work?", "it binds away from the active site and changes its shape", ["it binds to the active site", "it is a substrate", "it raises the activation energy only"], "More substrate does not reduce its effect."),
       ("Why does a change in pH affect enzyme activity?", "it changes the charges on R groups, breaking ionic and hydrogen bonds", ["it breaks peptide bonds", "it adds water to the enzyme", "it gives molecules more kinetic energy"], "The active site shape changes."),
       ("Why does increasing temperature (below the optimum) speed up an enzyme reaction?", "molecules have more kinetic energy, so there are more successful collisions", ["the active site gets larger", "the enzyme denatures", "the activation energy rises"], "More enzyme–substrate complexes form."),
       ("Which is an example of a competitive inhibitor in medicine?", "a drug with a similar shape to the substrate", ["a heavy metal ion", "a high temperature", "a strong acid"], "It competes for the active site."),
       ("What is the substrate of amylase?", "starch", ["protein", "lipid", "DNA"], "Amylase gives maltose."),
       ("Where is lipase produced?", "the pancreas", ["the salivary glands", "the stomach only", "the liver"], "It breaks lipids into fatty acids and monoglycerides."),
       ("Which enzyme breaks a dipeptide into amino acids?", "dipeptidase", ["maltase", "lipase", "amylase"], "A membrane-bound enzyme in the ileum."),
       ("What is an enzyme–substrate complex?", "the substrate bound to the enzyme's active site", ["two substrates joined together", "an enzyme bound to an inhibitor", "the product of the reaction"], "Products are released after the reaction."),
       ("What is the effect of a cofactor such as chloride ions on amylase?", "it helps the enzyme work or bind its substrate", ["it denatures amylase", "it inhibits amylase", "it is the substrate"], "Many enzymes need cofactors."),
       ("Why are enzymes specific?", "only one substrate has a complementary shape to the active site", ["they work at every pH", "they are made of lipid", "they can bind any molecule"], "The tertiary structure decides the shape."),
       ("How can you measure the rate of catalase activity?", "measure the volume of oxygen released per minute", ["measure the starch remaining", "count the bacteria", "measure the mass of glucose"], "Catalase breaks down hydrogen peroxide.")]


def m_rate(k=None):
    k = k or ch(["vol", "inv", "half"])
    if k == "inv":
        t = ch([20, 25, 32, 40, 50, 64, 80, 125, 160, 200, 250])
        return nq("A starch solution takes %d s to be broken down by amylase. Calculate the rate as 1/time." % t, 1 / t, [t / 1000, 1 / t * 60, t / 60], " s⁻¹", "Rate = 1/t = 1/%d = <b>%s s⁻¹</b>." % (t, nf(1 / t)))
    if k == "half":
        a, b = ch([(30, 42), (25, 50), (36, 48), (20, 35), (40, 64), (18, 45)])
        return nq("At 25 °C the initial rate of an enzyme reaction is %d units and at 35 °C it is %d units. Calculate the percentage increase in rate." % (a, b), (b - a) / a * 100, [(b - a) / b * 100, b / a * 100, b - a], "%",
                  "(%d − %d) ÷ %d × 100 = <b>%s%%</b>." % (b, a, a, nf((b - a) / a * 100)))
    v, t = ch([4.0, 6.0, 7.5, 9.0, 12.0, 15.0, 18.0, 24.0, 30.0]), ch([30, 45, 60, 90, 120, 150, 180])
    return nq("Catalase releases %s cm³ of oxygen in the first %d s. Calculate the mean rate in cm³ per minute." % (nf(v, 2), t), v / t * 60, [v / t, t / v, v * t / 60], " cm³ min⁻¹",
              "%s ÷ %d × 60 = <b>%s cm³ min⁻¹</b>." % (nf(v, 2), t, nf(v / t * 60)))


# =================================================================== Year 12: cells
def m_mag(k=None):
    k = k or ch(["A", "M", "I", "bar"])
    M = ch([40, 100, 200, 400, 500, 1000, 1500, 2000, 4000, 5000, 10000, 20000])
    obj, sizes = ch([("a cheek cell", [40.0, 50.0, 60.0, 80.0]), ("a nucleus", [5.0, 6.0, 8.0, 10.0]), ("a chloroplast", [4.0, 5.0, 6.0, 8.0]), ("a mitochondrion", [1.5, 2.0, 2.5, 4.0]),
                     ("a red blood cell", [7.5, 8.0]), ("a pollen grain", [25.0, 30.0, 40.0, 50.0, 80.0]), ("a bacterium", [1.5, 2.0, 2.5, 4.0, 5.0]), ("a guard cell", [20.0, 25.0, 30.0, 40.0]),
                     ("a palisade cell", [50.0, 60.0, 80.0, 100.0]), ("a yeast cell", [4.0, 5.0, 8.0, 10.0])])
    act = ch(sizes)
    img = act * M / 1000
    if img < 5 or img > 300:
        return None
    if k == "A":
        return nq("In a photograph %s is %s mm long. The magnification is ×%s. Calculate its actual length in µm." % (obj, nf(img), "{:,}".format(M)), act, [act / 1000, img * M, act * 1000], " µm",
                  "Actual size = image ÷ magnification = %s mm ÷ %s = %s mm = <b>%s µm</b>." % (nf(img), "{:,}".format(M), nf(act / 1000), nf(act)))
    if k == "M":
        return nq("%s is %s µm long. Its image is %s mm long. Calculate the magnification." % (obj.capitalize(), nf(act), nf(img)), M, [M // 1000 or M / 1000, M * 1000, round(act / img, 4)], "",
                  "Change mm to µm: %s µm. Magnification = image ÷ actual = <b>×%s</b>." % (nf(img * 1000), "{:,}".format(M)))
    if k == "I":
        return nq("%s is %s µm long. How long will its image be, in mm, at a magnification of ×%s?" % (obj.capitalize(), nf(act), "{:,}".format(M)), img, [img * 1000, act / M, img / 10], " mm",
                  "Image = actual × magnification = %s µm = <b>%s mm</b>." % (nf(act * M), nf(img)))
    bar, lab = ch([(20, 50), (25, 10), (30, 5), (40, 100), (10, 2), (15, 20), (50, 10), (24, 1)])
    return nq("A scale bar %d mm long represents %d µm. Calculate the magnification of the drawing." % (bar, lab), bar * 1000 / lab, [lab / bar, bar / lab, bar * lab], "",
              "%d mm = %s µm; magnification = %s ÷ %d = <b>×%s</b>." % (bar, "{:,}".format(bar * 1000), "{:,}".format(bar * 1000), lab, nf(bar * 1000 / lab)))


def m_mitotic(k=None):
    k = k or ch(["mi", "time"])
    tot = ch([120, 150, 200, 240, 250, 300, 400, 500])
    mit = ch([12, 15, 18, 20, 24, 30, 36, 40, 45, 50, 60])
    if mit > tot / 5:
        return None
    if k == "mi":
        return nq("In a root tip squash, %d of %d cells are in mitosis. Calculate the mitotic index as a percentage." % (mit, tot), mit / tot * 100, [mit / (tot - mit) * 100, (tot - mit) / tot * 100, tot / mit], "%",
                  "Mitotic index = cells in mitosis ÷ total cells × 100 = <b>%s%%</b>." % nf(mit / tot * 100))
    cyc = ch([12, 16, 18, 20, 24]) * 60
    return nq("A cell cycle lasts %d hours. In a sample, %d of %d cells are in mitosis. Estimate how long mitosis lasts, in minutes." % (cyc // 60, mit, tot), mit / tot * cyc, [mit / tot * cyc / 60, tot / mit * cyc, (tot - mit) / tot * cyc], " min",
              "Fraction in mitosis × cycle time = %d/%d × %d min = <b>%s min</b>." % (mit, tot, cyc, nf(mit / tot * cyc)))


def m_wp(k=None):
    a, b = R.sample([-100, -150, -200, -250, -300, -350, -400, -500, -600, -700, -800, -1000, -1200], 2)
    t1, t2 = ch([("cell X", "cell Y"), ("a root hair cell", "the soil water"), ("a potato cell", "the sucrose solution"), ("an onion cell", "the salt solution"), ("cell A", "cell B")])
    k = k or ch(["dir", "high"])
    v = lambda x: "−%d kPa" % -x
    if k == "high":
        hi = t1 if a > b else t2
        return tq("%s has a water potential of %s and %s has %s. Which has the higher water potential?" % (t1[0].upper() + t1[1:], v(a), t2, v(b)), hi,
                  [t2 if hi == t1 else t1, "they are the same", "it depends on the temperature"], "The value closer to zero (%s) is higher." % v(max(a, b)))
    if a > b:
        ans = "from %s to %s" % (t1, t2)
        other = "from %s to %s" % (t2, t1)
    else:
        ans = "from %s to %s" % (t2, t1)
        other = "from %s to %s" % (t1, t2)
    return tq("%s has a water potential of %s and %s has %s. In which direction does water move by osmosis?" % (t1[0].upper() + t1[1:], v(a), t2, v(b)), ans,
              [other, "no net movement", "it moves both ways equally"], "Water moves from a higher (less negative) water potential to a lower (more negative) water potential.")


CELLS = [("Which organelle is the site of aerobic respiration?", "mitochondrion", ["ribosome", "Golgi apparatus", "lysosome"], "Mitochondria make most of the cell's ATP."),
         ("Which organelle makes proteins?", "ribosome", ["lysosome", "nucleolus", "vacuole"], "Ribosomes are on the rough ER and free in the cytoplasm."),
         ("What is the function of the Golgi apparatus?", "modifying and packaging proteins and lipids into vesicles", ["making ATP", "photosynthesis", "storing DNA"], "It also makes lysosomes."),
         ("What is the function of the smooth endoplasmic reticulum?", "making and processing lipids", ["making proteins", "respiration", "digesting old organelles"], "It has no ribosomes."),
         ("What do lysosomes contain?", "hydrolytic enzymes (lysozymes)", ["chlorophyll", "DNA", "starch grains"], "They digest worn-out organelles and pathogens."),
         ("Which structure is found in prokaryotic cells but not eukaryotic cells?", "plasmids", ["mitochondria", "a nucleus", "Golgi apparatus"], "Prokaryotes also have 70S ribosomes."),
         ("What are the ribosomes of prokaryotes?", "70S, smaller than eukaryotic 80S ribosomes", ["80S", "bound to the nuclear envelope", "absent"], "Mitochondria and chloroplasts also have 70S ribosomes."),
         ("What is the cell wall of a bacterium made of?", "murein (peptidoglycan)", ["cellulose", "chitin", "phospholipid"], "Plant cell walls are made of cellulose."),
         ("Why is a virus not considered a living cell?", "it has no cytoplasm or ribosomes and can only replicate inside a host cell", ["it is too large", "it has DNA", "it has a cell wall"], "Viruses are acellular."),
         ("Which microscope has the highest resolution?", "the transmission electron microscope", ["the light microscope", "the scanning electron microscope", "a hand lens"], "Electrons have a much shorter wavelength than light."),
         ("What does a scanning electron microscope produce?", "a 3D image of the surface", ["a colour image of living cells", "a 2D image of thin sections", "an image of DNA sequences"], "Its resolution is lower than a TEM."),
         ("What is resolution?", "the ability to distinguish two points that are close together", ["how much bigger the image is", "the brightness of the image", "the depth of focus"], "Magnification without resolution gives a blurred image."),
         ("Why is cell fractionation done in an ice-cold, isotonic, buffered solution?", "to stop enzymes working, stop osmosis damaging organelles and keep pH constant", ["to speed up enzyme action", "to kill bacteria", "to dissolve the membranes"], "Then the homogenate is filtered and centrifuged."),
         ("In ultracentrifugation, which organelle forms the first pellet?", "nuclei", ["ribosomes", "mitochondria", "lysosomes"], "The heaviest organelles settle at the lowest speed."),
         ("What happens in interphase?", "DNA replicates and the cell grows", ["chromosomes line up at the equator", "the cytoplasm divides", "chromatids separate"], "Organelles are also copied."),
         ("What happens in metaphase of mitosis?", "chromosomes line up at the equator, attached to spindle fibres", ["chromatids move to the poles", "the nuclear envelope reforms", "DNA replicates"], "Spindle fibres attach to centromeres."),
         ("What happens in anaphase of mitosis?", "sister chromatids are pulled to opposite poles", ["chromosomes condense", "the cell membrane pinches in", "the nucleus reforms"], "The centromeres divide."),
         ("How do prokaryotic cells divide?", "binary fission", ["mitosis", "meiosis", "budding of the nucleus"], "The circular DNA and plasmids are copied first."),
         ("Why is cancer linked to uncontrolled mitosis?", "mutations in genes that control the cell cycle", ["cells stop replicating DNA", "cells lose their membranes", "meiosis happens too fast"], "Tumours form from rapidly dividing cells."),
         ("What is facilitated diffusion?", "passive movement of molecules through channel or carrier proteins", ["movement using ATP", "movement against a gradient", "engulfing large particles"], "Down a concentration gradient."),
         ("What is active transport?", "movement against a concentration gradient using ATP and carrier proteins", ["passive movement through channels", "osmosis", "diffusion through the bilayer"], "Carrier proteins change shape."),
         ("Why can oxygen diffuse straight through the phospholipid bilayer?", "it is small and non-polar", ["it is charged", "it is large", "it binds to carrier proteins"], "Ions need channel proteins."),
         ("How does sodium–glucose co-transport absorb glucose in the ileum?", "Na⁺ diffuses into the cell down its gradient, carrying glucose with it", ["glucose moves by osmosis", "glucose is pumped out by ATP", "glucose diffuses through the bilayer"], "The gradient is set up by the Na⁺/K⁺ pump."),
         ("What does cholesterol do in a cell membrane?", "it reduces fluidity and makes the membrane more stable", ["it carries glucose", "it makes ATP", "it acts as a receptor"], "It sits between the phospholipids."),
         ("What are glycoproteins in membranes used for?", "cell recognition and as receptors", ["making ATP", "storing glucose", "transporting oxygen"], "They have carbohydrate chains outside the cell."),
         ("What happens to a red blood cell in pure water?", "water enters by osmosis and it bursts", ["it shrinks", "nothing", "it becomes plasmolysed"], "Animal cells have no cell wall.")]
IMM = [("What is an antigen?", "a molecule that triggers an immune response", ["a protein made by B cells", "a type of white blood cell", "a drug that kills bacteria"], "Usually a protein on the surface of a cell or virus."),
       ("What is an antibody?", "a protein that binds to a specific antigen", ["a pathogen", "a phagocyte", "a type of vaccine only"], "Made by plasma cells."),
       ("Which cells make antibodies?", "plasma cells", ["T helper cells", "phagocytes", "red blood cells"], "Plasma cells are made from B cells."),
       ("What do cytotoxic T cells do?", "kill infected body cells by making holes in them (perforin)", ["make antibodies", "engulf bacteria", "present antigens only"], "Part of the cellular response."),
       ("What do T helper cells do?", "release cytokines that stimulate B cells and phagocytes", ["make antibodies", "carry oxygen", "kill bacteria directly"], "HIV infects T helper cells."),
       ("What is phagocytosis?", "a phagocyte engulfs a pathogen and digests it with lysosome enzymes", ["B cells make antibodies", "a virus enters a cell", "T cells divide"], "The phagocyte then presents antigens."),
       ("Why is the secondary immune response faster than the primary response?", "memory cells are already present", ["antibodies never leave the blood", "the pathogen is weaker", "phagocytes become larger"], "More antibodies are made more quickly."),
       ("What does an antibody's variable region do?", "binds to a specific antigen", ["binds to phagocytes only", "forms disulfide bridges", "carries oxygen"], "Its shape is complementary to the antigen."),
       ("What is agglutination?", "antibodies clump pathogens together", ["pathogens dividing", "antibodies breaking down", "cells bursting"], "Each antibody has two binding sites."),
       ("What is active immunity?", "your own immune system makes antibodies after exposure to an antigen", ["receiving antibodies from another source", "having no antigens", "taking antibiotics"], "It gives long-lasting memory."),
       ("What is passive immunity?", "antibodies are given rather than made, so there are no memory cells", ["making your own antibodies", "a vaccine with dead pathogens", "being immune for life"], "For example antibodies across the placenta."),
       ("How does a vaccine give protection?", "it contains antigens that cause memory cells to be made", ["it contains antibiotics", "it kills all bacteria", "it contains antibodies only"], "A later infection gives a fast secondary response."),
       ("What is herd immunity?", "when enough people are vaccinated that a disease cannot spread easily", ["immunity in cattle only", "immunity from antibiotics", "a single person's immunity"], "It protects unvaccinated people too."),
       ("What is antigenic variability?", "a pathogen's antigens change, so memory cells do not recognise them", ["antibodies change shape", "B cells become T cells", "vaccines become stronger"], "This is why flu vaccines change each year."),
       ("How does HIV cause AIDS?", "it destroys T helper cells, weakening the immune system", ["it destroys red blood cells", "it makes antibodies", "it attacks the lungs directly"], "Opportunistic infections follow."),
       ("Why do antibiotics not work against HIV?", "viruses have no cell wall or ribosomes for antibiotics to target", ["HIV is too large", "HIV is a bacterium", "antibiotics only work on fungi"], "Antiretroviral drugs are used instead."),
       ("What is a monoclonal antibody?", "an antibody made from a single clone of B cells", ["a mixture of antibodies", "an antigen", "a type of vaccine"], "Used in pregnancy tests and targeted drugs."),
       ("How does the ELISA test detect an antigen?", "an enzyme-linked antibody gives a colour change", ["it counts bacteria", "it uses PCR", "it measures pH"], "Washing removes unbound antibodies."),
       ("Why might a transplanted organ be rejected?", "the body recognises its antigens as foreign", ["the organ has no blood supply", "antibiotics damage it", "the organ is too small"], "Immunosuppressant drugs reduce the risk."),
       ("Which white blood cells mature in the thymus?", "T lymphocytes", ["B lymphocytes", "phagocytes", "plasma cells"], "B cells mature in the bone marrow."),
       ("What is clonal selection?", "the B or T cell with the matching receptor is selected and divides", ["all lymphocytes divide equally", "antibodies select antigens", "phagocytes clone themselves"], "Then clonal expansion happens."),
       ("What is an ethical issue with vaccines?", "testing may involve animals or there may be side effects", ["vaccines contain antibiotics", "vaccines give passive immunity", "vaccines change your DNA"], "There are also questions about compulsory vaccination."),
       ("What is the role of antigen-presenting cells?", "they display a pathogen's antigens so T helper cells can bind to them", ["they make antibodies", "they carry oxygen", "they destroy memory cells"], "Phagocytes act as antigen-presenting cells."),
       ("What is the humoral response?", "the response involving B cells and antibodies", ["the response of T cells only", "phagocytosis only", "the inflammatory response"], "Antibodies are in body fluids."),
       ("What is the cellular response?", "the response involving T cells", ["antibodies in the plasma", "red blood cells", "the response of skin"], "T cells respond to antigens on cells."),
       ("How does an antibody's structure suit its job?", "it has two variable regions that bind specific antigens and a constant region", ["it has one binding site", "it is made of lipid", "it has no quaternary structure"], "Four polypeptide chains joined by disulfide bridges.")]


# =================================================================== Year 12: exchange and transport
def m_sav(k=None):
    s = ch([1, 2, 3, 4, 5, 6, 8, 10])
    k = k or ch(["cube", "cuboid"])
    if k == "cube":
        sa, v = 6 * s * s, s ** 3
        return nq("Calculate the surface area to volume ratio of a cube with sides of %d cm, as x : 1." % s, sa / v, [v / sa, sa, 4 * s * s / v], " : 1", "SA = 6 × %d² = %d cm², V = %d cm³, ratio = %d ÷ %d = <b>%s : 1</b>." % (s, sa, v, sa, v, nf(sa / v)))
    a, b, c = ch([1, 2, 3]), ch([2, 3, 4]), ch([5, 6, 8, 10])
    sa, v = 2 * (a * b + b * c + a * c), a * b * c
    return nq("A block of agar is %d cm × %d cm × %d cm. Calculate its surface area to volume ratio, as x : 1." % (a, b, c), sa / v, [v / sa, (a * b + b * c + a * c) / v, 6 * c * c / c ** 3], " : 1",
              "SA = 2(%d + %d + %d) = %d cm², V = %d cm³, ratio = <b>%s : 1</b>." % (a * b, b * c, a * c, sa, v, nf(sa / v)))


def m_cardiac(k=None):
    k = k or ch(["CO", "SV", "HR", "cycle", "vent", "tv"])
    sv, hr = ch([60, 65, 70, 75, 80, 90, 100, 110, 120]), ch([60, 64, 70, 72, 75, 80, 90, 100, 120, 150, 180])
    co = sv * hr
    if k == "CO":
        return nq("Stroke volume is %d cm³ and heart rate is %d beats per minute. Calculate cardiac output in dm³ min⁻¹." % (sv, hr), co / 1000, [co, sv / hr, (sv + hr) / 1000], " dm³ min⁻¹",
                  "Cardiac output = stroke volume × heart rate = %s cm³ min⁻¹ = <b>%s dm³ min⁻¹</b>." % ("{:,}".format(co), nf(co / 1000)))
    if k == "SV":
        return nq("Cardiac output is %s dm³ min⁻¹ and heart rate is %d beats per minute. Calculate the stroke volume in cm³." % (nf(co / 1000), hr), sv, [co / 1000 / hr, co * hr / 1000, hr / co * 1000], " cm³",
                  "SV = CO ÷ HR = %s cm³ ÷ %d = <b>%d cm³</b>." % ("{:,}".format(co), hr, sv))
    if k == "HR":
        return nq("Cardiac output is %s dm³ min⁻¹ and stroke volume is %d cm³. Calculate the heart rate." % (nf(co / 1000), sv), hr, [co / 1000 / sv, sv * co / 1000, co / sv / 60], " beats min⁻¹",
                  "HR = CO ÷ SV = %s ÷ %d = <b>%d beats min⁻¹</b>." % ("{:,}".format(co), sv, hr))
    if k == "cycle":
        t = ch([0.40, 0.50, 0.60, 0.75, 0.80, 1.0, 1.2])
        return nq("One cardiac cycle on an ECG lasts %s s. Calculate the heart rate in beats per minute." % nf(t, 2), 60 / t, [t * 60, 1 / t, 60 * t / 2], " beats min⁻¹", "Heart rate = 60 ÷ %s = <b>%s beats min⁻¹</b>." % (nf(t, 2), nf(60 / t)))
    tv, br = ch([0.40, 0.45, 0.50, 0.55, 0.60, 0.75, 1.0, 1.5, 2.0]), ch([10, 12, 14, 15, 16, 18, 20, 24, 30])
    if k == "vent":
        return nq("A person has a tidal volume of %s dm³ and breathes %d times per minute. Calculate the pulmonary ventilation rate." % (nf(tv, 2), br), tv * br, [tv / br, br / tv, tv * br * 60], " dm³ min⁻¹",
                  "Pulmonary ventilation = tidal volume × breathing rate = <b>%s dm³ min⁻¹</b>." % nf(tv * br))
    return nq("Pulmonary ventilation is %s dm³ min⁻¹ at %d breaths per minute. Calculate the tidal volume." % (nf(tv * br), br), tv, [tv * br * br, br / (tv * br), tv * 1000], " dm³",
              "Tidal volume = ventilation ÷ breathing rate = <b>%s dm³</b>." % nf(tv))


def m_potometer(k=None):
    d, r, t = ch([12, 15, 18, 20, 24, 25, 30, 36, 40, 45, 50]), ch([0.25, 0.4, 0.5, 0.6, 0.75, 1.0]), ch([2, 4, 5, 6, 10])
    k = k or ch(["transp", "resp"])
    vol = math.pi * r * r * d
    what = "an air bubble in a potometer moves %d mm" % d if k == "transp" else "the liquid in a respirometer moves %d mm" % d
    stem = "Calculate the rate of water uptake" if k == "transp" else "Calculate the rate of oxygen uptake"
    return nq("In %d minutes %s along a capillary tube of radius %s mm. %s in mm³ min⁻¹." % (t, what, nf(r, 2), stem), vol / t, [d / t, math.pi * (2 * r) ** 2 * d / t, vol], " mm³ min⁻¹",
              "Volume = πr²d = π × %s² × %d = %s mm³; ÷ %d min = <b>%s mm³ min⁻¹</b>." % (nf(r, 2), d, nf(vol), t, nf(vol / t)))


GAS = [("Why do single-celled organisms not need a gas exchange system?", "they have a large surface area to volume ratio, so diffusion is fast enough", ["they do not respire", "they live in water", "they have no cell membrane"], "Larger organisms need specialised surfaces."),
       ("How is air carried to the cells of an insect?", "through spiracles, tracheae and tracheoles", ["through gills", "through alveoli", "in the blood with haemoglobin"], "Gas exchange happens at the tracheole ends."),
       ("What is the counter-current system in fish gills?", "water and blood flow in opposite directions, keeping a diffusion gradient along the whole lamella", ["water and blood flow the same way", "blood flows back into the mouth", "water only flows during exhalation"], "More oxygen is absorbed than with parallel flow."),
       ("How are leaves adapted for gas exchange?", "stomata and air spaces in the spongy mesophyll", ["a thick waxy cuticle with no openings", "xylem vessels in every cell", "red pigments"], "Guard cells open and close the stomata."),
       ("How do xerophytes reduce water loss?", "sunken stomata, rolled leaves and hairs that trap moist air", ["more stomata on the upper surface", "a thin cuticle", "large flat leaves"], "These reduce the water potential gradient."),
       ("Why are alveoli efficient gas exchange surfaces?", "a large surface area, thin walls and a good blood supply", ["thick walls", "few capillaries", "a small surface area"], "Ventilation keeps a steep gradient."),
       ("What happens during inspiration?", "the external intercostal muscles and diaphragm contract, so the volume of the thorax increases", ["the diaphragm relaxes and rises", "pressure in the lungs increases", "the internal intercostals contract"], "Air pressure in the lungs falls below atmospheric pressure."),
       ("What happens during normal expiration?", "the diaphragm and external intercostal muscles relax", ["the diaphragm contracts", "the thorax volume increases", "the ribs move up and out"], "Expiration is mostly passive."),
       ("What does the trachea contain to keep it open?", "rings of cartilage", ["muscle only", "alveoli", "valves"], "The cartilage is C-shaped."),
       ("What is the effect of emphysema on gas exchange?", "the alveoli walls break down, reducing the surface area", ["the alveoli get thinner", "more capillaries form", "the airways widen"], "Elastin is damaged, so exhaling is harder."),
       ("What is the effect of fibrosis?", "scar tissue makes the alveoli walls thicker, so diffusion is slower", ["the surface area increases", "the lungs become more elastic", "more oxygen enters the blood"], "Tidal volume also falls."),
       ("How does asthma reduce the rate of gas exchange?", "the airways narrow, so less air reaches the alveoli", ["the alveoli burst", "the blood carries less haemoglobin", "the diaphragm stops working"], "Inflamed bronchioles produce mucus."),
       ("What is tidal volume?", "the volume of air breathed in or out in one normal breath", ["the maximum volume of the lungs", "the volume left after breathing out", "air breathed per minute"], "About 0.5 dm³ at rest."),
       ("Why are gill filaments covered in lamellae?", "to increase the surface area for gas exchange", ["to pump water", "to store oxygen", "to filter food only"], "Each lamella has many capillaries."),
       ("What do bile salts do in digestion?", "emulsify lipids into small droplets", ["break peptide bonds", "digest starch", "absorb water"], "This gives lipase a larger surface area."),
       ("How are monoglycerides and fatty acids absorbed into ileum cells?", "micelles carry them to the cell, then they diffuse through the membrane", ["by active transport with glucose", "through the capillaries directly", "by osmosis"], "In the cell they reform triglycerides and form chylomicrons."),
       ("Why does the ileum have villi and microvilli?", "to give a large surface area for absorption", ["to make enzymes", "to churn food", "to store bile"], "Villi also have a good blood supply."),
       ("Which enzyme digests starch to maltose?", "amylase", ["maltase", "lipase", "pepsin"], "Made in the salivary glands and pancreas."),
       ("What do exopeptidases do?", "remove amino acids from the ends of polypeptides", ["hydrolyse peptide bonds in the middle of chains", "digest lipids", "break glycosidic bonds"], "Endopeptidases act within the chain."),
       ("Where does maltase act?", "on the membrane of epithelial cells in the ileum", ["in the stomach", "in the mouth", "in the liver"], "It gives glucose."),
       ("Why can insects not grow very large?", "gases move along the tracheae mainly by diffusion, which is slow over long distances", ["they have no lungs", "they have no blood", "their spiracles are always open"], "Muscle movement can help ventilate the tracheae."),
       ("How do insects reduce water loss through gas exchange?", "they close their spiracles", ["they open more spiracles", "they sweat", "they have gills"], "A waxy cuticle also helps."),
       ("What is the role of the epithelium in the alveoli?", "it is one cell thick, giving a short diffusion pathway", ["it makes mucus", "it pumps oxygen", "it is many cells thick"], "Capillary walls are also very thin."),
       ("Which enzyme digests proteins in the stomach?", "pepsin (an endopeptidase)", ["amylase", "lipase", "maltase"], "It works best in acid conditions.")]
CIRC = [("Why does haemoglobin have a high affinity for oxygen in the lungs?", "the partial pressure of oxygen is high there", ["the partial pressure of carbon dioxide is high", "the pH is low", "the temperature is high"], "Haemoglobin loads oxygen."),
        ("What is the Bohr effect?", "a higher partial pressure of CO₂ lowers haemoglobin's affinity for oxygen", ["oxygen raises the pH", "CO₂ increases oxygen loading", "haemoglobin binds CO₂ more strongly than O₂"], "The dissociation curve moves to the right."),
        ("Why is the oxygen dissociation curve S-shaped?", "binding the first oxygen changes the shape and makes it easier for more to bind (cooperative binding)", ["haemoglobin has one binding site", "oxygen is not soluble", "red cells have no nucleus"], "The curve is steepest in the middle."),
        ("Why is the curve of an organism living at high altitude shifted to the left?", "its haemoglobin has a higher affinity for oxygen, so it loads at lower partial pressures", ["it has less haemoglobin", "it needs less oxygen", "its blood is more acidic"], "Llamas and fetal haemoglobin show this."),
        ("Which blood vessel carries blood from the heart to the lungs?", "the pulmonary artery", ["the pulmonary vein", "the aorta", "the vena cava"], "It carries deoxygenated blood."),
        ("Which blood vessel brings oxygenated blood from the lungs to the heart?", "the pulmonary vein", ["the pulmonary artery", "the aorta", "the vena cava"], "It enters the left atrium."),
        ("Why does the left ventricle have a thicker wall than the right?", "it pumps blood all round the body at higher pressure", ["it holds more blood", "it pumps blood to the lungs", "it receives blood from the vena cava"], "The right ventricle only pumps to the lungs."),
        ("When do the atrioventricular valves close?", "when ventricular pressure becomes higher than atrial pressure", ["when the atria contract", "when the aorta pressure falls", "at the end of diastole"], "This stops backflow into the atria."),
        ("When do the semilunar valves open?", "when ventricular pressure becomes higher than the pressure in the arteries", ["when the atria contract", "when the ventricles relax", "when blood enters the atria"], "Blood leaves the ventricles."),
        ("Why do arteries have thick muscular and elastic walls?", "to withstand and smooth out high pressure", ["to allow diffusion", "to stop backflow with valves", "to store blood"], "Elastic recoil keeps blood flowing."),
        ("Why do capillaries have walls one cell thick?", "to give a short diffusion distance", ["to resist high pressure", "to stop backflow", "to make blood flow faster"], "Exchange with tissue fluid happens here."),
        ("Why do veins have valves?", "to stop blood flowing backwards at low pressure", ["to raise blood pressure", "to allow diffusion", "to pump blood"], "Skeletal muscles squeeze veins."),
        ("How is tissue fluid formed?", "hydrostatic pressure at the arteriole end forces fluid out of the capillaries", ["osmosis at the arteriole end", "active transport from the cells", "diffusion of plasma proteins"], "Plasma proteins stay in the blood."),
        ("Why does fluid return to the capillaries at the venule end?", "the water potential of the blood is lower because of the plasma proteins", ["the hydrostatic pressure is higher", "the capillary walls are thicker", "the heart pulls it back"], "Excess fluid drains into the lymph."),
        ("What is an atheroma?", "a fatty deposit in an artery wall", ["a blood clot in a vein", "a burst capillary", "a heart valve"], "It can lead to thrombosis and heart attacks."),
        ("Which risk factor increases the risk of cardiovascular disease?", "high blood pressure", ["a low-salt diet", "regular exercise", "low blood cholesterol"], "Smoking and a high-saturated-fat diet are others."),
        ("What is the role of the coronary arteries?", "to supply the heart muscle with oxygenated blood", ["to carry blood to the lungs", "to drain blood from the brain", "to carry blood to the kidneys"], "Blockage causes a myocardial infarction.")]
PLANT = [("What is transpiration?", "the loss of water vapour from the leaves through the stomata", ["water uptake by root hairs", "movement of sugars in phloem", "photosynthesis"], "It pulls water up the xylem."),
         ("What is the cohesion–tension theory?", "water evaporating from leaves pulls a continuous column of water up the xylem", ["root pressure pushes all water up", "phloem pumps water", "water moves by active transport"], "Hydrogen bonds hold the water molecules together."),
         ("Which factor increases the rate of transpiration?", "higher temperature", ["higher humidity", "less light", "no wind"], "Molecules evaporate faster."),
         ("Why does high humidity reduce transpiration?", "the water potential gradient between the leaf and the air is smaller", ["the stomata close", "the xylem gets blocked", "photosynthesis stops"], "Less water vapour diffuses out."),
         ("Why is lignin present in xylem walls?", "it strengthens the vessels so they do not collapse", ["it makes them waterproof only", "it transports sucrose", "it carries out photosynthesis"], "Xylem vessels are dead with no end walls."),
         ("What does phloem transport?", "organic substances such as sucrose", ["water and minerals only", "oxygen", "red blood cells"], "This is translocation."),
         ("What is the mass flow hypothesis?", "sucrose loaded at the source lowers water potential, water enters and pressure pushes the sap to the sink", ["sucrose diffuses all the way", "xylem pumps sucrose", "sucrose moves by osmosis only"], "Sinks include roots and growing tips."),
         ("What is a source in translocation?", "where sugars are made or released, such as a leaf", ["where sugars are used or stored", "the root hair", "the xylem"], "A sink uses or stores sugars."),
         ("What does a ringing experiment show?", "removing the phloem makes sugars build up above the ring", ["xylem carries sugars", "water moves down the stem", "roots make sugars"], "Evidence that phloem carries organic substances."),
         ("Why must a potometer be set up under water?", "to stop air entering the xylem and the apparatus", ["to keep the plant cool", "to increase transpiration", "to measure photosynthesis"], "An airlock would stop the water column."),
         ("What does a potometer actually measure?", "water uptake, which is close to the rate of transpiration", ["sugar movement", "oxygen release", "the rate of respiration"], "Some water is used in photosynthesis."),
         ("What are companion cells for?", "providing ATP for active loading of sucrose into sieve tubes", ["carrying water", "photosynthesis", "strengthening the stem"], "They have many mitochondria."),
         ("Why do stomata close at night in most plants?", "there is no light for photosynthesis, so closing reduces water loss", ["to take in more CO₂", "to increase transpiration", "because roots stop working"], "Guard cells lose turgor."),
         ("How do radioactive tracers show translocation?", "¹⁴CO₂ is supplied to a leaf and labelled sugars are found in the phloem", ["dye shows water in the xylem", "oxygen is measured in roots", "glucose stains blue"], "Autoradiography shows the path."),
       ("What forms the xylem?", "dead cells with no end walls, forming continuous tubes", ["living cells with sieve plates", "companion cells", "guard cells"], "The tubes are strengthened by lignin."),
       ("What is root pressure?", "active loading of ions into the xylem in roots lowers water potential so water enters", ["water evaporating from leaves", "phloem pushing water", "air pressure"], "It only pushes water a short distance.")]


# =================================================================== Year 12: genetic information, variation and relationships
CODONS = {"AUG": "Met", "UUU": "Phe", "UUC": "Phe", "GGU": "Gly", "GGC": "Gly", "GCU": "Ala", "GCA": "Ala", "UCU": "Ser", "AGC": "Ser", "CCU": "Pro", "ACU": "Thr",
          "UAU": "Tyr", "CAU": "His", "CAA": "Gln", "AAU": "Asn", "AAA": "Lys", "GAU": "Asp", "GAA": "Glu", "UGU": "Cys", "UGG": "Trp", "CGU": "Arg", "GUU": "Val", "AUU": "Ile", "CUU": "Leu"}


def m_mrna(k=None):
    k = k or ch(["mrna", "anti", "aa", "trip"])
    if k == "mrna":
        t = seq(ch([9, 12]))
        m = "".join(RNA[x] for x in t)
        return tq("A DNA template strand has the sequence %s. What is the sequence of the mRNA made from it?" % t, m,
                  ["".join(COMP[x] for x in t), t.replace("T", "U"), m[::-1] if m[::-1] != m else "".join(COMP[x] for x in t)[::-1]], "mRNA is complementary to the template, with U instead of T.")
    if k == "anti":
        c = ch(sorted(CODONS))
        a = "".join({"A": "U", "U": "A", "G": "C", "C": "G"}[x] for x in c)
        return tq("Which tRNA anticodon pairs with the mRNA codon %s?" % c, a, [c, a.replace("U", "T"), a[::-1] if a[::-1] != a else c[::-1]], "The anticodon is complementary to the codon: A–U and G–C.")
    if k == "aa":
        n = ch([150, 300, 450, 600, 900, 1200, 1500, 1800, 2400, 3000])
        intr = ch([0, 0, 90, 150, 300, 600])
        if intr >= n:
            return None
        ex = n - intr
        q = "A gene is %s bases long%s. How many amino acids does it code for? (Ignore start and stop codons.)" % ("{:,}".format(n), "" if not intr else ", of which %s bases are in introns" % "{:,}".format(intr))
        return nq(q, ex // 3, [n // 3, ex, ex // 3 * 2 if intr else n * 3, n // 3 - intr // 3 + 1 if intr else n // 2], "", "Only exons are translated: %s bases ÷ 3 = <b>%s</b>." % ("{:,}".format(ex), "{:,}".format(ex // 3)))
    cs = [ch(sorted(CODONS)) for _ in range(3)]
    if cs[0] == cs[1] == cs[2]:
        return None
    m = "".join(cs)
    tab = ", ".join("%s = %s" % (c, CODONS[c]) for c in sorted(set(cs)) + [x for x in R.sample(sorted(CODONS), 2) if x not in cs])
    ans = "–".join(CODONS[c] for c in cs)
    wr = ["–".join(CODONS[c] for c in cs[::-1]), "–".join(CODONS[c] for c in [cs[1], cs[0], cs[2]]), "–".join(CODONS.get("".join(COMP.get(x, "A") for x in c).replace("T", "U"), "Gly") for c in cs),
          "–".join(CODONS[c] for c in [cs[0], cs[2], cs[1]])]
    return tq("mRNA: %s. Codons: %s. What is the amino acid sequence?" % (m, tab), ans, wr, "Read the mRNA in triplets from the start: %s." % " ".join(cs))


def m_meiosis(k=None):
    n = ch([2, 3, 4, 5, 6, 7, 8, 10, 12, 23])
    k = k or ch(["comb", "fert", "hap", "dip"])
    org = ch(["a plant", "an animal", "a species of fruit fly", "a fish", "a fungus"])
    if k == "comb":
        return nq("A diploid cell of %s has %d chromosomes. How many different combinations of chromosomes can its gametes have by independent segregation?" % (org, 2 * n), 2 ** n, [2 ** (2 * n), 2 * n, n ** 2], "",
                  "With n = %d pairs, combinations = 2<sup>n</sup> = <b>%s</b>." % (n, "{:,}".format(2 ** n)))
    if k == "fert":
        if n > 8:
            return None
        return nq("A species has %d pairs of chromosomes. How many different chromosome combinations can occur in zygotes from random fertilisation (ignoring crossing over)?" % n, (2 ** n) ** 2, [2 ** n, 2 * 2 ** n, (2 * n) ** 2], "",
                  "(2<sup>n</sup>)² = (2<sup>%d</sup>)² = <b>%s</b>." % (n, "{:,}".format((2 ** n) ** 2)))
    if k == "hap":
        return nq("A diploid body cell of %s has %d chromosomes. How many chromosomes are in one of its gametes?" % (org, 2 * n), n, [2 * n, 4 * n, n // 2 or 1], "", "Meiosis halves the number: <b>%d</b>." % n)
    return nq("A gamete of %s has %d chromosomes. How many chromosomes are in a cell after mitosis in this organism?" % (org, n), 2 * n, [n, 4 * n, n + 1], "", "Body cells are diploid (2n): <b>%d</b>." % (2 * n))


def m_simpson(k=None):
    ns = [ch([2, 3, 4, 5, 6, 8, 10, 12, 15, 20]) for _ in range(ch([3, 4, 5]))]
    N = sum(ns)
    D = 1 - sum(x * (x - 1) for x in ns) / (N * (N - 1))
    tab = ", ".join("%s %d" % (s, x) for s, x in zip(["species A", "species B", "species C", "species D", "species E"], ns))
    return nq("A quadrat survey found: %s. Calculate Simpson's index of diversity, D = 1 − Σn(n − 1)/N(N − 1)." % tab, D,
              [sum(x * (x - 1) for x in ns) / (N * (N - 1)), 1 - sum(x * x for x in ns) / (N * N), 1 - sum(x * (x - 1) for x in ns) / (N * N)], "",
              "N = %d; Σn(n − 1) = %d; D = 1 − %d/%d = <b>%s</b>." % (N, sum(x * (x - 1) for x in ns), sum(x * (x - 1) for x in ns), N * (N - 1), nf(D)))


TAXA = ["domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"]


def m_taxa(k=None):
    i = R.randrange(1, 7)
    k = k or ch(["after", "before"])
    if k == "after":
        return tq("In the hierarchy of classification, which taxon comes directly below %s?" % TAXA[i], TAXA[i + 1], [TAXA[j] for j in (i - 1, (i + 2) % 8, (i + 3) % 8) if j != i + 1], "Domain, kingdom, phylum, class, order, family, genus, species.")
    return tq("In the hierarchy of classification, which taxon comes directly above %s?" % TAXA[i], TAXA[i - 1], [TAXA[j] for j in (i + 1, (i + 2) % 8, (i - 2) % 8) if j != i - 1], "Domain, kingdom, phylum, class, order, family, genus, species.")


GENE = [("What is a gene?", "a sequence of DNA bases that codes for a polypeptide or functional RNA", ["a whole chromosome", "a type of protein", "a single nucleotide"], "Each gene has a fixed locus."),
        ("What is an allele?", "a different form of the same gene", ["a section of a chromosome without genes", "a type of cell", "a protein"], "Alleles have different base sequences."),
        ("Why is the genetic code described as degenerate?", "most amino acids are coded for by more than one triplet", ["each triplet codes for several amino acids", "the code overlaps", "it differs between species"], "There are 64 triplets and 20 amino acids."),
        ("Why is the genetic code described as non-overlapping?", "each base is read in only one triplet", ["bases are shared between triplets", "triplets are read backwards", "only half the bases are read"], "Triplets are read one after another."),
        ("Why is the genetic code described as universal?", "the same triplets code for the same amino acids in almost all organisms", ["all organisms have the same genes", "the code changes between cells", "all genes are expressed"], "This is evidence of a common origin."),
        ("What are introns?", "non-coding sequences in genes that are removed from pre-mRNA", ["coding sequences", "proteins in the nucleus", "start codons"], "Exons are joined by splicing."),
        ("How is DNA stored in eukaryotic cells?", "as long linear molecules wound around histone proteins", ["as short circular molecules without proteins", "only in plasmids", "in ribosomes"], "Prokaryotes have circular DNA not linked to histones."),
        ("Where else is DNA found in eukaryotic cells?", "mitochondria and chloroplasts", ["ribosomes", "lysosomes", "the Golgi apparatus"], "This DNA is short and circular, like prokaryote DNA."),
        ("Where does transcription take place in eukaryotes?", "the nucleus", ["the ribosome", "the cytoplasm only", "the Golgi apparatus"], "RNA polymerase makes pre-mRNA."),
        ("What does RNA polymerase do?", "joins RNA nucleotides complementary to the template strand", ["splices out introns", "carries amino acids", "joins amino acids"], "It moves along the gene."),
        ("What is the job of tRNA?", "carrying a specific amino acid to the ribosome", ["copying DNA", "removing introns", "forming peptide bonds alone"], "Its anticodon pairs with an mRNA codon."),
        ("What happens during translation?", "tRNA anticodons pair with mRNA codons and amino acids are joined by peptide bonds", ["DNA is copied", "introns are removed", "mRNA is made"], "ATP is used to attach amino acids to tRNA."),
        ("What is the genome?", "the complete set of genes in a cell", ["all the proteins in a cell", "one chromosome", "a single gene"], "The proteome is the full range of proteins."),
        ("What is the proteome?", "the full range of proteins a cell can produce", ["the complete set of genes", "the set of chromosomes", "the ribosomes"], "Alternative splicing makes it larger than the gene count."),
        ("What is a homologous pair of chromosomes?", "two chromosomes with the same genes at the same loci", ["two identical sister chromatids", "a pair of sex chromosomes only", "two chromosomes from one parent"], "One comes from each parent."),
        ("Which mutation is most likely to change many amino acids?", "a deletion of one base (frameshift)", ["a substitution of one base", "a deletion of three bases", "a silent mutation"], "Every codon after it is changed."),
        ("Why might a base substitution have no effect on the protein?", "the new triplet may code for the same amino acid", ["substitutions never happen in genes", "the protein is not made", "the code overlaps"], "Because the code is degenerate.")]
VAR = [("How does crossing over create genetic variation?", "homologous chromosomes swap sections of chromatids", ["sister chromatids join", "chromosomes are lost", "DNA replicates twice"], "It happens in prophase I."),
       ("What is independent segregation?", "homologous pairs line up and separate randomly in meiosis I", ["chromatids separate in mitosis", "genes swap places", "gametes fuse at random"], "Each gamete gets a random mix of maternal and paternal chromosomes."),
       ("What is non-disjunction?", "chromosomes fail to separate properly in meiosis", ["crossing over between chromatids", "a base substitution", "random fertilisation"], "Down's syndrome is caused by an extra chromosome 21."),
       ("How many cells are made from one cell in meiosis?", "four genetically different haploid cells", ["two identical diploid cells", "four identical diploid cells", "two haploid cells"], "Meiosis has two divisions."),
       ("What is a mutagenic agent?", "something that increases the rate of mutation", ["an enzyme that repairs DNA", "a type of chromosome", "a hormone"], "For example UV light or tobacco smoke."),
       ("What is genetic diversity?", "the number of different alleles in a population", ["the number of species", "the number of chromosomes", "the size of a population"], "More diversity helps a population adapt."),
       ("What is a genetic bottleneck?", "a big drop in population size that reduces genetic diversity", ["a new mutation", "migration into a population", "a large increase in alleles"], "Survivors carry only some of the alleles."),
       ("What is the founder effect?", "a small group starts a new population, so it has little genetic diversity", ["natural selection in a large population", "crossing over", "a population with many alleles"], "Some alleles may become common by chance."),
       ("What is directional selection?", "individuals with an extreme phenotype are favoured", ["the middle phenotype is favoured", "both extremes are favoured", "no phenotype is favoured"], "For example antibiotic resistance."),
       ("What is stabilising selection?", "individuals with the average phenotype are favoured", ["one extreme is favoured", "variation increases", "mutation rate rises"], "For example human birth mass."),
       ("What is a species?", "a group of organisms that can interbreed to give fertile offspring", ["organisms that look the same", "organisms in one habitat", "a group of populations that cannot breed"], "Mules are infertile, so horses and donkeys are different species."),
       ("What does the binomial name Homo sapiens tell you?", "the genus is Homo and the species is sapiens", ["the family is Homo", "the kingdom is sapiens", "the order is Homo"], "The genus has a capital letter."),
       ("What is a phylogenetic classification based on?", "evolutionary relationships", ["habitat", "size", "colour"], "Shown in phylogenetic trees."),
       ("How can DNA sequences show how closely related two species are?", "more similar base sequences mean a more recent common ancestor", ["longer DNA means more related", "the number of chromosomes", "more introns mean less related"], "Amino acid sequences and immunology are also used."),
       ("What is courtship behaviour used for?", "recognising members of the same species and a mate ready to breed", ["finding food", "avoiding predators", "marking territory only"], "It helps prevent breeding between species."),
       ("Why is random sampling used to measure biodiversity?", "to avoid bias", ["to find every organism", "to make the sample smaller", "to choose the most interesting sites"], "Use random coordinates for quadrats."),
       ("How does farming tend to affect biodiversity?", "removing hedgerows and growing monocultures reduce it", ["it always increases it", "pesticides increase species", "it has no effect"], "Conservation schemes try to balance this."),
       ("What is a base substitution?", "one base in DNA is replaced by a different base", ["a base is removed", "a base is added", "a section is reversed"], "It changes at most one amino acid."),
       ("What does meiosis I separate?", "homologous chromosomes", ["sister chromatids", "the nucleus only", "the cytoplasm"], "Meiosis II separates the chromatids.")]


# =================================================================== Year 13: energy transfers
def m_energy(k=None):
    k = k or ch(["npp", "eff", "gpp", "rf", "rq"])
    if k == "rf":
        d, s = ch([1.5, 2.0, 2.4, 3.0, 3.6, 4.2, 5.4, 6.0]), ch([8.0, 9.0, 10.0, 12.0])
        pig = "a pigment spot"
        return nq("In a chromatogram of leaf pigments, %s moves %s cm and the solvent moves %s cm. Calculate its R<sub>f</sub> value." % (pig, nf(d, 2), nf(s, 2)), d / s, [s / d, s - d, d * s / 100], "",
                  "R<sub>f</sub> = %s ÷ %s = <b>%s</b>." % (nf(d, 2), nf(s, 2), nf(d / s)))
    if k == "rq":
        o = ch([20, 24, 25, 30, 36, 40, 45, 50, 60, 80])
        c = round(o * ch([1.0, 0.7, 0.72, 0.8, 0.9]))
        if c == o and o not in (20, 30, 40, 50):
            return None
        return nq("An organism takes in %d cm³ of oxygen and gives out %d cm³ of carbon dioxide. Calculate the respiratory quotient." % (o, c), c / o, [o / c, c / (o + c), (o - c) / o if c != o else 0.7], "",
                  "RQ = CO₂ given out ÷ O₂ taken in = <b>%s</b> (1.0 for carbohydrate, about 0.7 for lipid, about 0.9 for protein)." % nf(c / o))
    gpp = ch([12000, 15000, 18000, 20000, 25000, 30000, 36000, 40000])
    rr = gpp * ch([0.4, 0.45, 0.5, 0.55, 0.6, 0.65])
    npp = gpp - rr
    if k == "npp":
        return nq("A crop has a gross primary production of %s kJ m⁻² year⁻¹ and loses %s kJ m⁻² year⁻¹ in respiration. Calculate its net primary production." % ("{:,}".format(gpp), "{:,}".format(int(rr))), npp,
                  [gpp + rr, rr - npp if rr != npp else gpp, npp / gpp * 100], " kJ m⁻² year⁻¹", "NPP = GPP − R = <b>%s kJ m⁻² year⁻¹</b>." % "{:,}".format(int(npp)))
    if k == "gpp":
        return nq("A woodland has a net primary production of %s kJ m⁻² year⁻¹ and respiratory losses of %s kJ m⁻² year⁻¹. Calculate the gross primary production." % ("{:,}".format(int(npp)), "{:,}".format(int(rr))), gpp,
                  [npp - rr if npp > rr else rr - npp, npp, rr], " kJ m⁻² year⁻¹", "GPP = NPP + R = <b>%s kJ m⁻² year⁻¹</b>." % "{:,}".format(gpp))
    a = ch([8000, 10000, 12000, 15000, 20000, 24000])
    b = a * ch([0.05, 0.08, 0.1, 0.12, 0.15, 0.2])
    lv = ch([("producers", "primary consumers"), ("primary consumers", "secondary consumers"), ("secondary consumers", "tertiary consumers")])
    return nq("The %s contain %s kJ m⁻² year⁻¹ and the %s contain %s kJ m⁻² year⁻¹. Calculate the efficiency of energy transfer." % (lv[0], "{:,}".format(a), lv[1], "{:,}".format(int(b))), b / a * 100,
              [a / b, (a - b) / a * 100, b / a], "%", "Efficiency = energy at next level ÷ energy at previous level × 100 = <b>%s%%</b>." % nf(b / a * 100))


PHOTO = [("Where do the light-dependent reactions take place?", "the thylakoid membranes", ["the stroma", "the matrix", "the cytoplasm"], "Chlorophyll is in photosystems in the thylakoids."),
         ("Where does the Calvin cycle (light-independent reaction) take place?", "the stroma", ["the thylakoid membranes", "the cristae", "the cytoplasm"], "It uses ATP and reduced NADP."),
         ("What is photolysis?", "light splitting water into protons, electrons and oxygen", ["fixing carbon dioxide", "making glucose", "breaking down ATP"], "2H₂O → 4H⁺ + 4e⁻ + O₂."),
         ("What are the products of the light-dependent reaction used in the Calvin cycle?", "ATP and reduced NADP", ["oxygen and water", "glucose and CO₂", "pyruvate and NAD"], "Oxygen is a by-product."),
         ("Which enzyme fixes carbon dioxide in the Calvin cycle?", "rubisco", ["ATP synthase", "DNA polymerase", "amylase"], "CO₂ + RuBP → 2 GP."),
         ("What happens to glycerate 3-phosphate (GP) in the Calvin cycle?", "it is reduced to triose phosphate using ATP and reduced NADP", ["it is oxidised to CO₂", "it is split by light", "it becomes chlorophyll"], "Some triose phosphate makes glucose; most regenerates RuBP."),
         ("How is ATP made in the light-dependent reaction?", "protons flow through ATP synthase down a gradient (chemiosmosis)", ["by substrate-level phosphorylation only", "by glycolysis", "by rubisco"], "This is photophosphorylation."),
         ("What is a limiting factor in photosynthesis?", "the factor in shortest supply that limits the rate", ["the factor in greatest supply", "a factor that has no effect", "the end product"], "Light intensity, CO₂ concentration and temperature."),
         ("Why do growers burn paraffin in greenhouses?", "it raises CO₂ concentration and temperature", ["it adds oxygen", "it kills pests only", "it lowers humidity"], "Both can limit photosynthesis."),
         ("What happens to the amount of GP if light intensity falls?", "it rises, because less ATP and reduced NADP are available to reduce it", ["it falls", "it stays the same", "it turns into RuBP"], "RuBP falls because it is not regenerated."),
         ("What does a dehydrogenase activity experiment with DCPIP show?", "the light-dependent reaction is happening, because DCPIP is reduced from blue to colourless", ["glucose is being made", "CO₂ is fixed", "starch is present"], "DCPIP accepts electrons instead of NADP."),
         ("What does chlorophyll absorb mainly?", "red and blue light", ["green light", "infrared only", "ultraviolet only"], "Green light is reflected."),
       ("What is the role of NADP in photosynthesis?", "it accepts electrons and protons, becoming reduced NADP", ["it splits water", "it absorbs light", "it fixes CO₂"], "Reduced NADP is used to reduce GP."),
       ("What is RuBP?", "a 5-carbon compound that combines with CO₂ in the Calvin cycle", ["a 3-carbon sugar", "a pigment", "an enzyme"], "Ribulose bisphosphate is regenerated using ATP."),
       ("What happens to RuBP if the CO₂ concentration falls?", "it builds up, because less is being used", ["it falls", "it turns into glucose", "it is split by light"], "GP falls at the same time."),
       ("Which molecule is released as a waste product of photosynthesis?", "oxygen", ["carbon dioxide", "ATP", "NADP"], "It comes from photolysis of water."),
       ("Why does the rate of photosynthesis fall at very high temperatures?", "enzymes such as rubisco are denatured", ["light is absorbed too fast", "CO₂ becomes too concentrated", "chlorophyll turns green"], "Stomata may also close.")]
RESP = [("Where does glycolysis take place?", "the cytoplasm", ["the mitochondrial matrix", "the cristae", "the stroma"], "Glucose is split into two pyruvate."),
        ("What is the net ATP gain from glycolysis per glucose?", "2 ATP", ["4 ATP", "36 ATP", "0 ATP"], "4 are made and 2 are used."),
        ("Where does the Krebs cycle take place?", "the mitochondrial matrix", ["the cytoplasm", "the inner membrane", "the outer membrane"], "Acetyl CoA joins oxaloacetate."),
        ("Where is the electron transfer chain?", "the inner mitochondrial membrane (cristae)", ["the matrix", "the cytoplasm", "the outer membrane"], "Folding into cristae gives a large surface area."),
        ("What is the final electron acceptor in aerobic respiration?", "oxygen", ["NAD", "pyruvate", "carbon dioxide"], "Oxygen combines with electrons and protons to form water."),
        ("What happens in the link reaction?", "pyruvate is oxidised to acetyl CoA, releasing CO₂ and reducing NAD", ["glucose is split", "oxygen is used", "ATP is made by chemiosmosis"], "It takes place in the matrix."),
        ("What is produced in anaerobic respiration in mammals?", "lactate", ["ethanol and CO₂", "oxygen", "acetyl CoA"], "Pyruvate is reduced, regenerating NAD."),
        ("What is produced in anaerobic respiration in yeast?", "ethanol and carbon dioxide", ["lactate", "oxygen", "water"], "This is alcoholic fermentation."),
        ("Why does anaerobic respiration make much less ATP?", "only glycolysis produces ATP; the Krebs cycle and electron transfer chain stop", ["it uses more glucose", "it makes no NAD", "it happens in mitochondria"], "Only 2 ATP per glucose."),
        ("Which molecule can be respired if glucose runs out?", "lipids or proteins", ["DNA", "cellulose", "chlorophyll"], "Fatty acids enter as acetyl CoA."),
        ("What is oxidative phosphorylation?", "ATP made using energy from electrons in the electron transfer chain", ["ATP made in glycolysis", "ATP made in photosynthesis", "ATP broken down"], "Protons flow through ATP synthase."),
        ("Why is a respirometer kept at constant temperature?", "temperature changes gas volume and enzyme activity", ["to stop photosynthesis", "to kill bacteria", "to supply oxygen"], "Use a water bath and a control tube."),
        ("Why is potassium hydroxide used in a respirometer?", "it absorbs the carbon dioxide produced", ["it releases oxygen", "it provides food", "it measures pH"], "So the change in volume is oxygen taken in."),
       ("How many ATP molecules are made directly in one turn of the Krebs cycle?", "one", ["four", "none", "thirty-two"], "Two turns per glucose give two ATP."),
       ("What are cristae?", "folds of the inner mitochondrial membrane", ["folds of the outer membrane", "granules in the matrix", "parts of the chloroplast"], "They give a large surface area for the electron transfer chain."),
       ("What is the role of NAD in respiration?", "it carries hydrogen (protons and electrons) to the electron transfer chain", ["it breaks down glucose", "it releases oxygen", "it forms lactate only"], "It is reduced in glycolysis, the link reaction and the Krebs cycle."),
       ("What does ATP synthase do?", "uses the flow of protons to make ATP from ADP and Pᵢ", ["pumps protons out", "splits water", "carries electrons"], "Found in the inner mitochondrial membrane.")]
CYCLE = [("What do saprobionts do in the nitrogen cycle?", "decompose dead organisms, releasing ammonium ions (ammonification)", ["fix nitrogen gas", "turn nitrates into nitrogen gas", "absorb nitrates"], "They secrete enzymes and absorb the products."),
         ("What is nitrification?", "bacteria oxidise ammonium to nitrites and then nitrates", ["nitrogen gas is converted to ammonia", "nitrates are converted to nitrogen gas", "proteins are made"], "Needs oxygen, so it happens in aerated soils."),
         ("What is nitrogen fixation?", "bacteria such as Rhizobium convert nitrogen gas into ammonia", ["nitrates become nitrogen gas", "ammonium becomes nitrate", "plants release nitrogen"], "Rhizobium lives in root nodules of legumes."),
         ("What is denitrification?", "bacteria convert nitrates into nitrogen gas in waterlogged soil", ["bacteria fix nitrogen", "plants absorb nitrates", "ammonium becomes nitrite"], "It happens in anaerobic conditions."),
         ("What are mycorrhizae?", "fungi associated with plant roots that increase the surface area for absorbing water and minerals", ["bacteria in root nodules", "a type of algae", "a plant hormone"], "The plant gives the fungus sugars."),
         ("What is eutrophication?", "excess nutrients cause algal growth, leading to low oxygen levels in water", ["a fall in nutrients", "an increase in fish", "the formation of nitrogen gas"], "Bacteria decomposing dead algae use up oxygen."),
         ("Why is phosphate needed by plants?", "to make ATP, DNA and phospholipids", ["to make cellulose", "to make chlorophyll only", "to make starch"], "Phosphate comes from rocks, not the air."),
         ("What is the main reason energy is lost between trophic levels?", "respiration releases heat, and some parts are not eaten or digested", ["photosynthesis stops", "energy is recycled", "predators eat too much"], "Typically only about 10% is passed on."),
       ("Why do farmers add fertilisers?", "to replace minerals such as nitrates and phosphates removed when crops are harvested", ["to kill pests", "to add carbon dioxide", "to lower the pH"], "Natural fertilisers include manure."),
       ("What is net production in a consumer?", "chemical energy in food minus energy lost in faeces, urine and respiration", ["all the energy eaten", "energy lost as heat", "energy in the producer"], "N = I − (F + R)."),
       ("Why do intensive farming methods keep animals warm and still?", "less energy is lost in respiration, so more goes into growth", ["it increases disease", "animals eat more", "to increase heat loss"], "This improves efficiency of energy transfer."),
       ("What is leaching?", "nitrates are washed out of soil into rivers and lakes", ["nitrogen fixation by bacteria", "plants absorbing nitrates", "nitrates turning to gas"], "It can cause eutrophication.")]


# =================================================================== Year 13: response and homeostasis
def m_nerve(k=None):
    k = k or ch(["speed", "freq", "kid", "gluc"])
    if k == "speed":
        d, t = ch([10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 100, 120]), ch([0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 4.0, 5.0])
        return nq("An impulse travels %d mm along an axon in %s ms. Calculate its speed in m s⁻¹." % (d, nf(t, 2)), d / t, [d / t / 1000, d * t, t / d], " m s⁻¹",
                  "%d mm ÷ %s ms = %s m ÷ %s s = <b>%s m s⁻¹</b>." % (d, nf(t, 2), nf(d / 1000), nf(t / 1000), nf(d / t)))
    if k == "freq":
        rp = ch([0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 8.0, 10.0])
        return nq("The refractory period of a neurone is %s ms. Calculate the maximum frequency of impulses, in impulses per second." % nf(rp, 2), 1000 / rp, [1 / rp, rp * 1000, 100 / rp], " Hz",
                  "Maximum frequency = 1 ÷ %s s = <b>%s Hz</b>." % (nf(rp / 1000), nf(1000 / rp)))
    if k == "kid":
        f, u = ch([110, 115, 120, 125, 130]), ch([0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0])
        return nq("The kidneys filter %d cm³ of blood plasma per minute and produce %s cm³ of urine per minute. What percentage of the filtrate is reabsorbed?" % (f, nf(u, 2)), (f - u) / f * 100,
                  [u / f * 100, (f - u) / u, f / u], "%", "(%d − %s) ÷ %d × 100 = <b>%s%%</b>." % (f, nf(u, 2), f, nf((f - u) / f * 100)))
    a, b, t = ch([(5.0, 8.5), (4.5, 9.0), (5.5, 7.7), (4.8, 10.2), (5.2, 6.8)]) + (ch([30, 45, 60, 90]),)
    return nq("After a meal, blood glucose rises from %s to %s mmol dm⁻³ in %d minutes. Calculate the mean rate of increase." % (nf(a, 2), nf(b, 2), t), (b - a) / t, [b / t, (b - a) * t, (b - a) / t * 60 / 10], " mmol dm⁻³ min⁻¹",
              "(%s − %s) ÷ %d = <b>%s mmol dm⁻³ min⁻¹</b>." % (nf(b, 2), nf(a, 2), t, nf((b - a) / t)))


NERVE = [("What is the resting potential of a typical neurone?", "about −70 mV", ["about +40 mV", "0 mV", "about −10 mV"], "The inside is negative compared with the outside."),
         ("How is the resting potential kept?", "the Na⁺/K⁺ pump moves 3 Na⁺ out for every 2 K⁺ in, and K⁺ diffuses out", ["Na⁺ diffuses in freely", "Cl⁻ is pumped in", "the membrane is fully permeable"], "The pump uses ATP."),
         ("What causes depolarisation in an action potential?", "voltage-gated Na⁺ channels open and Na⁺ ions diffuse in", ["K⁺ channels open and K⁺ leaves", "the Na⁺/K⁺ pump stops", "Cl⁻ ions enter"], "The inside becomes positive."),
         ("What causes repolarisation?", "Na⁺ channels close and voltage-gated K⁺ channels open, so K⁺ diffuses out", ["more Na⁺ enters", "Ca²⁺ enters", "the pump stops"], "The potential falls back towards rest."),
         ("What is the all-or-nothing principle?", "a stimulus above the threshold always gives a full-size action potential", ["bigger stimuli give bigger action potentials", "every stimulus gives an action potential", "action potentials fade along the axon"], "Stronger stimuli give more frequent impulses."),
         ("Why do myelinated neurones conduct impulses faster?", "the impulse jumps between nodes of Ranvier (saltatory conduction)", ["the axon is thinner", "myelin carries the current", "there are more synapses"], "Depolarisation happens only at the nodes."),
         ("What is the role of the refractory period?", "it makes impulses travel in one direction and limits their frequency", ["it speeds impulses up", "it opens Na⁺ channels", "it releases neurotransmitter"], "Na⁺ channels cannot reopen straight away."),
         ("What triggers the release of neurotransmitter at a synapse?", "Ca²⁺ ions entering the presynaptic knob", ["Na⁺ ions leaving", "K⁺ ions entering", "ATP binding to receptors"], "Vesicles fuse with the membrane."),
         ("Why are synapses unidirectional?", "neurotransmitter is released only from the presynaptic side and receptors are only on the postsynaptic side", ["the axon only conducts one way", "the synaptic cleft is too wide", "enzymes block the other side"], "So impulses travel one way."),
         ("What does acetylcholinesterase do?", "breaks down acetylcholine in the synaptic cleft", ["makes acetylcholine", "opens Na⁺ channels", "pumps Ca²⁺"], "This stops continuous stimulation."),
         ("What is summation at a synapse?", "several small stimuli add together to reach the threshold", ["one impulse splits in two", "the synapse is blocked", "neurotransmitter is recycled"], "Spatial or temporal summation."),
         ("Which part of the sarcomere gets shorter during muscle contraction?", "the I-band and the H-zone", ["the A-band", "the actin filaments", "the myosin filaments"], "Filaments slide; they do not shorten."),
         ("What do Ca²⁺ ions do in muscle contraction?", "move tropomyosin away from the binding sites on actin", ["break down ATP directly", "bind to myosin heads only", "make the sarcomere longer"], "Released from the sarcoplasmic reticulum."),
         ("What is ATP used for in muscle contraction?", "detaching the myosin head from actin and re-cocking it", ["releasing calcium", "making actin", "opening Na⁺ channels"], "ATP hydrolysis gives the energy for the power stroke cycle."),
         ("Which type of muscle fibre is adapted for endurance?", "slow-twitch fibres with many mitochondria and myoglobin", ["fast-twitch fibres", "fibres with no blood supply", "fibres with little myoglobin"], "They respire aerobically."),
         ("What is a Pacinian corpuscle?", "a pressure receptor in the skin", ["a light receptor", "a type of synapse", "a muscle fibre"], "Pressure deforms stretch-mediated Na⁺ channels."),
         ("Why do rod cells give higher sensitivity in dim light?", "several rods connect to one bipolar neurone (summation)", ["they contain three pigments", "each rod has its own neurone", "they detect colour"], "Cones give higher visual acuity."),
         ("Which node starts each heartbeat?", "the sinoatrial node (SAN)", ["the atrioventricular node", "the bundle of His", "the Purkyne tissue"], "It is the pacemaker."),
       ("What is a generator potential?", "a depolarisation of a receptor membrane caused by a stimulus", ["the resting potential", "a hormone", "a muscle contraction"], "If it reaches threshold, an action potential follows."),
       ("Where is the cardiovascular control centre?", "the medulla oblongata", ["the cerebellum", "the heart", "the spinal cord"], "It changes heart rate through the SAN."),
       ("How does a rise in blood CO₂ change the heart rate?", "chemoreceptors send more impulses to the medulla, which increases heart rate through sympathetic nerves", ["it decreases heart rate", "it has no effect", "it stops the SAN"], "Faster blood flow removes CO₂."),
       ("What is a reflex arc?", "a pathway from receptor to sensory, relay and motor neurone to an effector", ["a voluntary movement", "a hormone pathway", "a synapse in the brain only"], "Reflexes are rapid and protective.")]
HOME = [("What is homeostasis?", "keeping the internal environment within restricted limits", ["changing body temperature with the weather", "growing new cells", "digesting food"], "For example core temperature, blood glucose and water potential."),
        ("What is negative feedback?", "a change triggers a response that brings the level back towards normal", ["a change triggers a larger change", "no response to change", "a response that has no effect"], "Most homeostasis uses negative feedback."),
        ("Which hormone lowers blood glucose?", "insulin", ["glucagon", "adrenaline", "ADH"], "It is made by β cells in the islets of Langerhans."),
        ("Which hormone raises blood glucose?", "glucagon", ["insulin", "ADH", "oestrogen"], "It is made by α cells."),
        ("What is glycogenolysis?", "breaking glycogen down into glucose", ["making glycogen from glucose", "making glucose from amino acids", "breaking down fats"], "Stimulated by glucagon and adrenaline."),
        ("What is gluconeogenesis?", "making glucose from non-carbohydrate sources such as glycerol and amino acids", ["breaking glycogen", "storing glucose", "absorbing glucose"], "It happens in the liver."),
        ("What is the main cause of type 1 diabetes?", "the β cells cannot make insulin", ["cells stop responding to insulin", "too much glucagon", "eating too much sugar"], "It is treated with insulin injections."),
        ("What is the main cause of type 2 diabetes?", "body cells no longer respond properly to insulin", ["the pancreas makes no insulin at all", "too little glucose in the diet", "the kidneys fail"], "Linked to obesity; controlled by diet and exercise."),
        ("What is the second messenger in the action of adrenaline and glucagon?", "cyclic AMP", ["ATP", "insulin", "calcium carbonate"], "It activates protein kinase."),
        ("Where does ultrafiltration happen in the kidney?", "the glomerulus into Bowman's capsule", ["the loop of Henle", "the collecting duct", "the ureter"], "High blood pressure forces small molecules out."),
        ("Where is most glucose reabsorbed in the kidney?", "the proximal convoluted tubule", ["the loop of Henle", "the collecting duct", "the bladder"], "By co-transport with Na⁺."),
        ("What does the loop of Henle do?", "creates a low water potential in the medulla so water can be reabsorbed", ["filters the blood", "secretes glucose", "stores urine"], "Na⁺ and Cl⁻ are pumped out of the ascending limb."),
        ("What does ADH do?", "makes the collecting duct more permeable to water", ["makes the kidneys filter more blood", "raises blood glucose", "causes more urine to be made"], "It acts through aquaporins."),
        ("When is more ADH released?", "when the water potential of the blood is too low", ["when blood water potential is high", "after drinking a lot", "when blood glucose is high"], "Osmoreceptors in the hypothalamus detect it."),
        ("What are auxins?", "plant growth factors that cause cell elongation", ["animal hormones", "enzymes that digest starch", "pigments"], "IAA is an auxin."),
        ("How does IAA cause positive phototropism in shoots?", "it moves to the shaded side, which grows faster", ["it is destroyed on the shaded side", "it stops growth on the shaded side", "it moves to the lit side, which grows faster"], "The shoot bends towards light."),
        ("Why do roots bend downwards (positive gravitropism)?", "IAA builds up on the lower side, which inhibits growth there", ["IAA speeds up growth on the lower side", "roots have no IAA", "gravity pulls the root"], "In roots, high IAA inhibits elongation."),
        ("What is a taxis?", "a directional movement of a whole organism towards or away from a stimulus", ["a change in the rate of movement only", "a plant growth response", "a reflex"], "Kinesis is a non-directional change in speed or turning."),
       ("What is the role of the liver in controlling blood glucose?", "it converts glucose to glycogen and back again", ["it makes insulin", "it filters glucose out of urine", "it stores glucose as starch"], "Liver cells have insulin and glucagon receptors."),
       ("How does insulin lower blood glucose?", "it increases glucose uptake by cells and activates glycogenesis", ["it breaks down glycogen", "it is broken down into glucose", "it makes the kidneys excrete glucose"], "More glucose channel proteins appear in membranes."),
       ("What is glycogenesis?", "making glycogen from glucose", ["breaking down glycogen", "making glucose from fat", "breaking down glucose in respiration"], "Stimulated by insulin."),
       ("Why does glucose appear in the urine of someone with untreated diabetes?", "the carrier proteins in the proximal tubule cannot reabsorb all of it", ["the glomerulus stops filtering", "insulin is excreted", "the bladder makes glucose"], "Blood glucose is too high."),
       ("Which part of the kidney is affected by ADH?", "the collecting duct (and distal tubule)", ["the glomerulus", "Bowman's capsule", "the ureter"], "Aquaporins are inserted into the membranes."),
       ("What is a kinesis?", "a change in the speed of movement or rate of turning in response to a stimulus", ["a directional movement", "a plant growth response", "a hormone"], "Woodlice move faster in dry conditions.")]


# =================================================================== Year 13: genetics, populations, evolution and ecosystems
def m_hw(k=None):
    k = k or ch(["het", "q", "p", "dom"])
    q2 = ch([0.01, 0.04, 0.09, 0.16, 0.25, 0.36, 0.0025, 0.0004, 0.0016, 0.0064, 0.0049, 0.0081])
    q = math.sqrt(q2)
    p = 1 - q
    trait = ch(["cystic fibrosis", "albinism", "a recessive coat colour", "a recessive flower colour", "red-green colour vision (in a model population)", "a recessive leaf shape"])
    if "colour vision" in trait:
        trait = "a recessive eye colour"
    pct = "%s%%" % nf(q2 * 100, 2)
    if k == "q":
        return nq("In a population, %s of individuals show %s (homozygous recessive). Calculate the frequency of the recessive allele." % (pct, trait), q, [q2, 1 - q2, q2 * 2], "", "q² = %s, so q = √%s = <b>%s</b>." % (nf(q2), nf(q2), nf(q)))
    if k == "p":
        return nq("In a population, %s of individuals show %s (homozygous recessive). Calculate the frequency of the dominant allele." % (pct, trait), p, [1 - q2, q, 1 - 2 * q2], "", "q = %s, p = 1 − q = <b>%s</b>." % (nf(q), nf(p)))
    if k == "dom":
        return nq("In a population, %s of individuals show %s (homozygous recessive). What percentage are homozygous dominant?" % (pct, trait), p * p * 100, [(1 - q2) * 100, 2 * p * q * 100, p * 100], "%",
                  "p = %s; p² = <b>%s%%</b>." % (nf(p), nf(p * p * 100)))
    return nq("In a population, %s of individuals show %s (homozygous recessive). What percentage are heterozygous carriers?" % (pct, trait), 2 * p * q * 100, [p * q * 100, (1 - q2) * 100, 2 * q2 * 100], "%",
              "q = %s, p = %s; 2pq = <b>%s%%</b>." % (nf(q), nf(p), nf(2 * p * q * 100)))


CROSS = [("Aa × Aa", "show the recessive phenotype", F(1, 4)), ("Aa × Aa", "show the dominant phenotype", F(3, 4)), ("Aa × Aa", "are heterozygous", F(1, 2)),
         ("Aa × aa", "show the recessive phenotype", F(1, 2)), ("AA × aa", "show the recessive phenotype", F(0)), ("AaBb × AaBb", "show both recessive phenotypes (aabb)", F(1, 16)),
         ("AaBb × AaBb", "show both dominant phenotypes", F(9, 16)), ("AaBb × AaBb", "are dominant for A and recessive for b", F(3, 16)), ("AaBb × aabb", "are aabb", F(1, 4)),
         ("AaBb × aabb", "show both dominant phenotypes", F(1, 4)), ("Aabb × aaBb", "are aabb", F(1, 4)), ("AaBB × Aabb", "are aaBb", F(1, 4)),
         ("Cᴿ Cᵂ × Cᴿ Cᵂ (codominant red and white flowers)", "are pink (Cᴿ Cᵂ)", F(1, 2)), ("Cᴿ Cᵂ × Cᴿ Cᴿ (codominant)", "are red (Cᴿ Cᴿ)", F(1, 2)),
         ("XᴴXʰ × XᴴY (haemophilia carrier mother)", "are sons with haemophilia, out of all children", F(1, 4)), ("XᴴXʰ × XᴴY (haemophilia carrier mother)", "of the sons have haemophilia", F(1, 2)),
         ("XᴴXʰ × XʰY", "of the daughters have haemophilia", F(1, 2)), ("Iᴬ Iᴼ × Iᴮ Iᴼ (blood groups)", "have blood group AB", F(1, 4)), ("Iᴬ Iᴼ × Iᴮ Iᴼ (blood groups)", "have blood group O", F(1, 4)),
         ("Iᴬ Iᴬ × Iᴮ Iᴼ (blood groups)", "have blood group A", F(1, 2))]


def m_cross(k=None):
    c, ph, p = ch(CROSS)
    org = ch(["pea plants", "fruit flies", "mice", "humans", "snapdragons", "rabbits", "tomato plants"])
    if ("X" in c or "I" in c) and org != "humans":
        org = "humans"
    if "codominant" in c:
        org = "snapdragons"
    alls = [F(0), F(1, 16), F(3, 16), F(1, 8), F(1, 4), F(3, 8), F(1, 2), F(9, 16), F(3, 4), F(1)]
    wr = [fr(x) for x in alls if x != p]
    R.shuffle(wr)
    near = [fr(x) for x in alls if x != p and abs(x - p) <= F(1, 4)]
    return tq("In %s, the cross %s is made. What proportion of the offspring %s?" % (org, c, ph), fr(p), near[:2] + wr, "Draw a Punnett square for %s and count the matching boxes: <b>%s</b>." % (c, fr(p)))


def m_chi(k=None):
    k = k or ch(["calc", "df", "sig"])
    if k == "df":
        n = ch([2, 3, 4, 5, 6])
        what = {2: "a 3 : 1 ratio", 3: "a 1 : 2 : 1 ratio", 4: "a 9 : 3 : 3 : 1 ratio", 5: "five phenotype classes", 6: "six phenotype classes"}[n]
        return nq("A chi-squared test is used on a cross expected to give %s (%d categories). How many degrees of freedom are there?" % (what, n), n - 1, [n, n + 1, n - 2 if n > 2 else 3], "", "Degrees of freedom = number of categories − 1 = <b>%d</b>." % (n - 1))
    ratio = ch([(3, 1), (1, 1), (9, 3, 3, 1), (1, 2, 1)])
    tot = sum(ratio) * ch([10, 12, 15, 20, 25, 30, 40])
    E = [tot * r / sum(ratio) for r in ratio]
    O = [max(1, int(e + R.randint(-max(2, int(e * 0.2)), max(2, int(e * 0.2))))) for e in E]
    O[-1] += tot - sum(O)
    if O[-1] < 1:
        return None
    chi = sum((o - e) ** 2 / e for o, e in zip(O, E))
    crit = {1: 3.84, 2: 5.99, 3: 7.82}[len(ratio) - 1]
    rs = " : ".join(str(r) for r in ratio)
    data = ", ".join(str(o) for o in O)
    if k == "sig":
        sig = chi > crit
        return tq("A cross expected to give %s produced %s (total %d). χ² = %s. The critical value at p = 0.05 is %s. What should you conclude?" % (rs, data, tot, nf(chi), nf(crit)),
                  "the difference is significant, so the results do not fit the expected ratio" if sig else "the difference is not significant; it is due to chance",
                  ["the difference is significant, so the results do not fit the expected ratio", "the difference is not significant; it is due to chance", "the expected ratio is proved true", "the test cannot be used"],
                  "χ² = %s is %s than the critical value %s." % (nf(chi), "greater" if sig else "less", nf(crit)))
    return nq("A cross expected to give a %s ratio produced %s offspring (total %d). Calculate χ² = Σ(O − E)²/E." % (rs, data, tot), chi,
              [sum((o - e) ** 2 / o for o, e in zip(O, E)), sum((o - e) ** 2 for o, e in zip(O, E)), sum(abs(o - e) / e for o, e in zip(O, E))], "",
              "Expected: %s. χ² = <b>%s</b>." % (", ".join(nf(e) for e in E), nf(chi)))


def m_pop(k=None):
    k = k or ch(["lincoln", "quad", "pct"])
    if k == "lincoln":
        n1, n2 = ch([20, 30, 40, 45, 50, 60, 80, 100]), ch([25, 30, 40, 50, 60, 75])
        m = ch([2, 3, 4, 5, 6, 8, 10, 12, 15])
        if m >= min(n1, n2):
            return None
        an = ch(["woodlice", "snails", "beetles", "voles", "grasshoppers", "fish"])
        return nq("%d %s are caught, marked and released. Later %d are caught and %d of these are marked. Estimate the population size." % (n1, an, n2, m), n1 * n2 / m, [n1 * m / n2, n1 + n2 - m, n2 * m / n1], "",
                  "N = n₁ × n₂ ÷ m = %d × %d ÷ %d = <b>%s</b>." % (n1, n2, m, nf(n1 * n2 / m)))
    if k == "quad":
        mean, qa = ch([2.5, 3.2, 4.0, 4.5, 6.0, 7.5, 8.4, 12.0]), ch([0.25, 0.5, 1.0])
        area = ch([100, 200, 250, 400, 500, 1000, 1500])
        pl = ch(["daisies", "dandelions", "buttercups", "limpets", "plantains"])
        return nq("Quadrats of %s m² are placed at random in a %s m² field. The mean is %s %s per quadrat. Estimate the total number of %s." % (nf(qa, 2), "{:,}".format(area), nf(mean, 2), pl, pl), mean / qa * area,
                  [mean * area, mean * qa * area, mean / qa], "", "Density = %s ÷ %s = %s per m²; × %s = <b>%s</b>." % (nf(mean, 2), nf(qa, 2), nf(mean / qa), "{:,}".format(area), nf(mean / qa * area)))
    sq, hit = ch([25, 50, 100]), ch([5, 8, 10, 12, 15, 18, 20])
    if hit >= sq:
        return None
    return nq("A quadrat divided into %d squares has a species in %d of them. Calculate the percentage cover (frequency)." % (sq, hit), hit / sq * 100, [hit, sq / hit, (sq - hit) / sq * 100], "%",
              "%d ÷ %d × 100 = <b>%s%%</b>." % (hit, sq, nf(hit / sq * 100)))


EVO = [("What is a gene pool?", "all the alleles of all the genes in a population", ["all the organisms in a habitat", "one gene in one organism", "the genome of a species"], "Allele frequencies describe the gene pool."),
       ("Which condition is needed for the Hardy–Weinberg principle?", "no mutation, selection or migration, random mating and a large population", ["a small population", "strong natural selection", "lots of immigration"], "Real populations rarely meet all of these."),
       ("What is genetic drift?", "random changes in allele frequency, important in small populations", ["changes caused by natural selection", "mutation in large populations", "migration between populations"], "Chance has a bigger effect when the population is small."),
       ("What is allopatric speciation?", "populations separated by a geographical barrier evolve into different species", ["speciation in the same area", "hybridisation", "artificial selection"], "Mutation, selection and drift act separately."),
       ("What is sympatric speciation?", "new species form in the same area, for example through reproductive isolation", ["a mountain range separates populations", "two species merge", "a species becomes extinct"], "It can be caused by polyploidy or behaviour changes."),
       ("What is reproductive isolation?", "changes that stop two populations interbreeding to give fertile offspring", ["two populations in one place", "a large population size", "random mating"], "It can be seasonal, mechanical or behavioural."),
       ("What is disruptive selection?", "both extreme phenotypes are favoured over the middle", ["the middle phenotype is favoured", "one extreme is favoured", "selection stops"], "It can lead to speciation."),
       ("What is epistasis?", "one gene affects or masks the expression of another gene", ["two alleles are both expressed", "a gene on the X chromosome", "a mutation in a gamete"], "It changes the expected 9 : 3 : 3 : 1 ratio."),
       ("What does autosomal linkage do to dihybrid cross ratios?", "parental combinations appear more often than expected", ["it gives exactly 9 : 3 : 3 : 1", "it removes all variation", "it makes recombinants more common"], "Linked genes are inherited together unless crossing over separates them."),
       ("Why are sex-linked recessive conditions more common in males?", "males have only one X chromosome, so one recessive allele is expressed", ["males have two X chromosomes", "the Y chromosome carries the allele", "females cannot inherit them"], "Females need two recessive alleles."),
       ("What does codominance mean?", "both alleles are expressed in the heterozygote", ["one allele masks the other", "neither allele is expressed", "the alleles are on different chromosomes"], "For example the AB blood group."),
       ("What is a niche?", "the role of a species in its habitat", ["the place where an organism lives", "all the species in an area", "the population size"], "Two species cannot share exactly the same niche."),
       ("What is carrying capacity?", "the maximum population size an environment can support", ["the number of species", "the rate of birth", "the biomass of producers"], "Limited by abiotic and biotic factors."),
       ("What is succession?", "a gradual change in the species in an area over time", ["a sudden extinction", "one species replacing itself", "seasonal migration"], "Pioneer species change the conditions for others."),
       ("What is a climax community?", "the final, stable community of succession", ["the first species to colonise", "a community after a fire", "a community with only producers"], "In the UK it is often oak woodland."),
       ("Why does biodiversity often increase during succession?", "conditions become less hostile and more niches form", ["pioneer species take over", "the soil disappears", "predators leave"], "Biomass also increases."),
       ("What is an abiotic factor?", "a non-living factor such as light or temperature", ["predation", "competition", "disease"], "Biotic factors are living."),
       ("Why might conservation use managed grazing?", "to stop succession reaching woodland so a valued habitat is kept", ["to speed up succession", "to remove all plants", "to increase pollution"], "This is called deflected succession."),
       ("What is natural selection?", "individuals with advantageous alleles survive and reproduce more, passing on the alleles", ["organisms change to suit their environment", "random mating", "a new mutation in every organism"], "Allele frequencies change over generations."),
       ("What is interspecific competition?", "competition between different species", ["competition within one species", "predation", "symbiosis"], "It can reduce the population of one species."),
       ("Why do predator and prey populations rise and fall in cycles?", "more prey supports more predators, which then reduce the prey", ["both are limited only by temperature", "predators reproduce faster", "prey have no other limits"], "Predator peaks lag behind prey peaks.")]


# =================================================================== Year 13: control of gene expression and biotechnology
def m_biotech(k=None):
    k = k or ch(["pcr", "gel", "probe", "pcrn"])
    if k == "pcr":
        m, n = ch([1, 2, 3, 5, 10, 20, 50, 100]), ch([3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30])
        return nq("PCR starts with %d DNA molecule%s. How many molecules are there after %d cycles?" % (m, "" if m == 1 else "s", n), m * 2 ** n, [m * 2 * n, 2 ** n, m * n ** 2], "",
                  "The DNA doubles each cycle: %d × 2<sup>%d</sup> = <b>%s</b>." % (m, n, nf(m * 2 ** n) if m * 2 ** n >= 1e7 else "{:,}".format(m * 2 ** n)))
    if k == "pcrn":
        t = ch([2, 3, 4, 5])
        n = ch([10, 15, 20, 25, 30])
        return nq("Each PCR cycle takes %d minutes. How many cycles can be completed in %d minutes, and so how many times larger is the DNA amount?" % (t, t * n), 2 ** n, [n, 2 * n, n ** 2], "×",
                  "%d cycles; amount × 2<sup>%d</sup> = <b>%s</b>." % (n, n, "{:,}".format(2 ** n)))
    if k == "gel":
        L = ch([1000, 1200, 1500, 2000, 2400, 3000, 4000])
        cuts = sorted(R.sample(range(100, L - 100, 50), ch([1, 2, 3])))
        pts = [0] + cuts + [L]
        fr_ = sorted([pts[i + 1] - pts[i] for i in range(len(pts) - 1)], reverse=True)
        if len(set(fr_)) < len(fr_):
            return None
        ans = ", ".join("{:,}".format(x) for x in fr_)
        wr = [", ".join("{:,}".format(x) for x in sorted(cuts + [L], reverse=True)), ", ".join("{:,}".format(x) for x in sorted([L - c for c in cuts] + [L], reverse=True)),
              ", ".join("{:,}".format(x) for x in sorted(fr_ + [L], reverse=True)), ", ".join("{:,}".format(x) for x in fr_[:-1])]
        return tq("A linear DNA molecule of %s base pairs is cut by a restriction enzyme at positions %s. Which fragment sizes (bp) appear on the gel?" % ("{:,}".format(L), ", ".join("{:,}".format(c) for c in cuts)), ans,
                  [w for w in wr if w], "Subtract neighbouring positions (including 0 and %s): %s. The smallest fragments move furthest on the gel." % ("{:,}".format(L), ans))
    s = seq(ch([8, 10, 12]))
    c = "".join(COMP[x] for x in s)
    return tq("A DNA probe is needed to bind to the base sequence %s. What is the probe's sequence?" % s, c, [s, "".join(RNA[x] for x in s), c[::-1] if c[::-1] != c else s[::-1]],
              "A probe is a short single strand complementary to the target: A–T, G–C.")


GX = [("What is a stem cell?", "an undifferentiated cell that can divide and become specialised", ["a cell that cannot divide", "a fully specialised cell", "a cell with no DNA"], "Totipotent, pluripotent, multipotent and unipotent cells."),
      ("Which stem cells can become any type of cell, including placenta?", "totipotent cells", ["pluripotent cells", "multipotent cells", "unipotent cells"], "Found in the early embryo."),
      ("What are induced pluripotent stem cells (iPS cells)?", "adult cells reprogrammed to become pluripotent by switching on certain genes", ["cells from an embryo", "cells that cannot divide", "cancer cells"], "Transcription factors are used."),
      ("What is a transcription factor?", "a protein that binds to DNA and switches transcription of a gene on or off", ["an enzyme that joins amino acids", "a type of RNA", "a hormone receptor only"], "It binds near the gene's promoter."),
      ("How does oestrogen switch on a gene?", "it diffuses into the cell and binds to a receptor, releasing a transcription factor", ["it binds to mRNA", "it destroys DNA", "it blocks ribosomes"], "The factor can then bind to DNA."),
      ("What is RNA interference (RNAi)?", "small RNA molecules bind to mRNA and stop it being translated", ["RNA joins to DNA", "RNA speeds up translation", "RNA replaces DNA"], "siRNA and miRNA are involved."),
      ("What is epigenetics?", "heritable changes in gene function without changes to the base sequence", ["mutations in DNA bases", "changes in chromosome number", "crossing over"], "For example DNA methylation."),
      ("How does increased methylation of DNA affect a gene?", "it stops transcription factors binding, so the gene is switched off", ["it switches the gene on", "it changes the base sequence", "it removes introns"], "Methyl groups are added to cytosine."),
      ("How does decreased acetylation of histones affect a gene?", "the chromatin becomes more condensed, so transcription is inhibited", ["it makes transcription easier", "it causes a mutation", "it removes the histones"], "Acetylation loosens chromatin."),
      ("What is a tumour suppressor gene?", "a gene that slows cell division; if mutated, cells can divide uncontrollably", ["a gene that makes cells divide faster", "a gene in bacteria", "a gene that only works in plants"], "For example the gene for p53."),
      ("What is an oncogene?", "a mutated proto-oncogene that is permanently switched on", ["a gene that stops cell division", "a virus", "a non-coding sequence"], "It causes cells to divide too fast."),
      ("How might high oestrogen levels increase the risk of breast cancer?", "oestrogen can switch on genes that promote cell division", ["oestrogen kills cells", "oestrogen methylates all DNA", "oestrogen blocks mitosis"], "Fat tissue after the menopause makes oestrogen."),
      ("What is the difference between benign and malignant tumours?", "malignant tumours invade tissues and spread (metastasis)", ["benign tumours spread around the body", "malignant tumours grow slowly", "benign tumours are always fatal"], "Benign tumours are usually enclosed."),
      ("What is the genome of an organism?", "its complete set of DNA", ["its proteins", "its RNA only", "one chromosome"], "The proteome is the set of proteins it can make."),
      ("Why is it harder to find the proteome from the genome in complex organisms?", "non-coding DNA and regulatory genes make it hard to predict the proteins", ["they have no genes", "their DNA is circular", "they have no introns"], "Alternative splicing also adds proteins."),
      ("What is a gene mutation called that adds an extra base?", "an addition (insertion)", ["a substitution", "an inversion", "a translocation"], "It causes a frameshift."),
      ("What does an inversion mutation do?", "reverses a section of bases", ["adds a base", "swaps one base for another", "copies a gene"], "The bases are the same but in reverse order."),
       ("What is a unipotent stem cell?", "one that can only become one type of cell", ["one that can become any cell", "one from the early embryo", "a cancer cell"], "For example cardiomyocytes from heart stem cells."),
       ("What is an ethical issue with embryonic stem cells?", "embryos are destroyed to obtain them", ["they cannot divide", "they come from bone marrow", "they are always rejected"], "iPS cells avoid this."),
       ("Why can different cells in one body make different proteins?", "different genes are switched on (expressed) in each cell type", ["each cell has different DNA", "some cells have no genes", "proteins are inherited separately"], "All body cells have the same genome."),
       ("What does siRNA do?", "guides an enzyme to cut a complementary mRNA", ["joins amino acids", "binds to DNA", "carries amino acids"], "The mRNA cannot then be translated."),
       ("How can a substitution mutation stop a protein working?", "it may change an amino acid in the active site so the shape changes", ["it always makes the protein longer", "it removes all amino acids", "it never changes the protein"], "Or it may create a stop codon.")]
BIO = [("What do restriction endonucleases do?", "cut DNA at specific recognition sequences", ["join DNA fragments", "copy RNA into DNA", "add nucleotides"], "Many leave sticky ends."),
       ("What does reverse transcriptase do?", "makes cDNA from an mRNA template", ["cuts DNA", "joins sticky ends", "translates mRNA"], "Used to make genes without introns."),
       ("What does DNA ligase do?", "joins sugar–phosphate backbones of DNA fragments", ["cuts DNA", "unwinds DNA", "makes mRNA"], "It seals sticky ends together."),
       ("Why are the same restriction enzymes used to cut the gene and the plasmid?", "so they have complementary sticky ends", ["so they are the same length", "so the gene is destroyed", "so no ligase is needed"], "The ends can then base pair."),
       ("Why are marker genes used in genetic engineering?", "to identify cells that have taken up the recombinant DNA", ["to cut DNA", "to make the gene work faster", "to kill all bacteria"], "For example antibiotic resistance or fluorescence."),
       ("What is needed for PCR?", "DNA, primers, free nucleotides and Taq DNA polymerase", ["ribosomes and tRNA", "restriction enzymes and ligase only", "RNA polymerase and amino acids"], "A thermal cycler changes the temperature."),
       ("Why is PCR heated to about 95 °C?", "to separate the DNA strands by breaking hydrogen bonds", ["to attach primers", "to activate ligase", "to make mRNA"], "Primers anneal at about 55 °C; extension at 72 °C."),
       ("Why is Taq polymerase used in PCR?", "it is not denatured at high temperatures", ["it cuts DNA", "it works best at 37 °C", "it makes RNA"], "It comes from a bacterium in hot springs."),
       ("What are primers in PCR?", "short single strands of DNA that bind to the start of the target sequence", ["enzymes that cut DNA", "free nucleotides", "RNA molecules that carry amino acids"], "DNA polymerase starts from them."),
       ("How does gel electrophoresis separate DNA fragments?", "by size: smaller fragments move further towards the positive electrode", ["by colour", "by base sequence only", "larger fragments move further"], "DNA is negatively charged."),
       ("What is genetic fingerprinting based on?", "variable number tandem repeats (VNTRs), which differ between people", ["genes that are the same in everyone", "the number of chromosomes", "blood groups"], "The pattern of bands is compared."),
       ("Which is a use of genetic fingerprinting?", "paternity testing", ["curing cancer", "making insulin", "producing vaccines"], "Also forensics and checking breeding plans."),
       ("What is gene therapy?", "inserting a working allele into cells to treat a genetic disorder", ["removing a chromosome", "taking antibiotics", "using a vaccine"], "Somatic therapy is not passed to children."),
       ("What is a DNA probe used for?", "finding a specific allele by binding to a complementary sequence", ["cutting DNA", "copying DNA", "joining DNA"], "Probes are labelled with fluorescent or radioactive markers."),
       ("What is an ethical concern about genetically modified crops?", "genes could spread to wild plants, and there may be less biodiversity", ["they always cure disease", "they cannot be grown", "they contain no DNA"], "Benefits include higher yields and pest resistance."),
       ("How can genetically modified bacteria make human insulin?", "the human insulin gene is put into a plasmid and inserted into the bacteria", ["bacteria naturally make insulin", "insulin is injected into bacteria", "bacteria are fused with human cells"], "The bacteria are grown in fermenters."),
       ("What is personalised medicine?", "treatment chosen to suit a person's genome", ["the same drug for everyone", "treatment without diagnosis", "medicine from plants only"], "Genome sequencing makes it possible."),
       ("What does in vivo gene cloning use?", "vectors such as plasmids to put genes into host cells", ["PCR only", "gel electrophoresis", "restriction mapping only"], "In vitro cloning uses PCR."),
       ("What is a sticky end?", "a short single-stranded overhang left by some restriction enzymes", ["a blunt cut", "a primer", "a plasmid"], "Complementary sticky ends can join."),
       ("Why are bacteria treated with calcium ions and heat shock in genetic engineering?", "to make the cell wall and membrane more permeable to plasmids", ["to kill them", "to cut their DNA", "to make them grow faster"], "This is transformation."),
       ("What is genetic screening used for?", "finding people who carry particular alleles", ["making vaccines", "growing crops", "producing insulin"], "Genetic counselling then explains the risks."),
       ("Why is a promoter added with a gene in genetic engineering?", "so RNA polymerase can bind and the gene is transcribed", ["to cut the plasmid", "to mark the cell", "to stop transcription"], "A terminator is added to stop it.")]


# =================================================================== unit definitions
def UNITS(year):
    b = {n: once_maker(v) for n, v in [("mol", MOL), ("tests", TESTS), ("enz", ENZ), ("cells", CELLS), ("imm", IMM), ("gas", GAS), ("circ", CIRC), ("plant", PLANT),
                                        ("gene", GENE), ("var", VAR), ("photo", PHOTO), ("resp", RESP), ("cycle", CYCLE), ("nerve", NERVE), ("home", HOME), ("evo", EVO), ("gx", GX), ("bio", BIO)]}
    if year == 12:
        return [
            U("Biology", 1, "biological-molecules", "Biological molecules",
              "Monomers and polymers, carbohydrates, lipids, proteins and enzymes, nucleic acids and DNA replication, ATP, water and inorganic ions, and the biochemical tests for sugars, starch, lipids and proteins.",
              "Biological Molecules", "biological molecules",
              "Free Year 12 A level biology worksheets on biological molecules: carbohydrates, lipids, proteins, enzymes, DNA and RNA, ATP, water and food tests. 100 questions with answers.",
              "Condensation joins monomers; hydrolysis splits them.", "n monomers in a chain make n − 1 bonds and release n − 1 water molecules.",
              "<p>Large biological molecules are polymers built from monomers by condensation reactions, which release water; hydrolysis uses water to split them. Glucose makes starch, glycogen and cellulose (glycosidic bonds), amino acids make proteins (peptide bonds), and nucleotides make DNA and RNA (phosphodiester bonds).</p>"
              "<p>In DNA, A pairs with T and G with C, so %A = %T and %G = %C. Enzymes lower the activation energy; their active site is complementary to the substrate and can be denatured by heat or pH.</p>",
              [("A chain of 6 glucose molecules: how many water molecules were released?", ["6 monomers make 5 bonds"], "5"),
               ("DNA has 30% adenine. %G?", ["A + T = 60%", "G + C = 40%"], "20%")],
              ["Counting n instead of n − 1 bonds.", "Pairing A with G in DNA.", "Thinking enzymes are used up."],
              [("What is the difference between condensation and hydrolysis?", "Condensation joins two molecules and releases water; hydrolysis breaks a bond using water."),
               ("How do you test for a reducing sugar?", "Heat with Benedict's reagent: a colour change from blue to green, yellow, orange or brick-red shows reducing sugar.")],
              lambda: [("Carbohydrates and lipids", [(m_cond, 8), (b["mol"], 12)]), ("Proteins and enzymes", [(b["enz"], 12), (m_rate, 8)]),
                       ("Nucleic acids", [(m_chargaff, 12), (m_dna, 8)]), ("Biochemical tests", [(b["tests"], 12), (b["mol"], 8)]),
                       ("Calculations with molecules", [(m_cond, 10), (m_rate, 5), (m_chargaff, 5)])]),
            U("Biology", 2, "cells-and-the-immune-system", "Cells",
              "Eukaryotic and prokaryotic cell structure, viruses, microscopy and magnification, cell fractionation, mitosis and the cell cycle, transport across membranes and water potential, and the immune system, vaccines and antibodies.",
              "Cells, Transport and the Immune System", "cells and the immune system",
              "Free Year 12 A level biology worksheets on cells: organelles, magnification, mitotic index, diffusion, osmosis, active transport, antibodies, vaccines and HIV. 100 questions with answers.",
              "Magnification = image size ÷ actual size.", "1 mm = 1000 µm; change units before dividing.",
              "<p>Magnification = image size ÷ actual size, with both in the same unit (1 mm = 1,000 µm = 1,000,000 nm). Electron microscopes have a much higher resolution than light microscopes. The mitotic index is the percentage of cells in mitosis.</p>"
              "<p>Water moves by osmosis from a higher (less negative) to a lower (more negative) water potential. In the immune response, B cells become plasma cells that make antibodies, and memory cells give a faster secondary response.</p>",
              [("Image 40 mm, magnification ×2,000. Actual size?", ["40 ÷ 2,000 = 0.02 mm", "× 1,000"], "20 µm"),
               ("Cell X −300 kPa, solution −500 kPa. Water moves?", ["from higher to lower ψ"], "out of cell X")],
              ["Dividing mm by magnification and calling it µm.", "Thinking water moves to the less negative water potential.", "Confusing antibodies with antigens."],
              [("What is the difference between magnification and resolution?", "Magnification is how much bigger the image is; resolution is how well two close points can be seen as separate."),
               ("Why does a vaccine protect you?", "It contains antigens that cause memory cells to be made, so a later infection triggers a fast, strong secondary response.")],
              lambda: [("Cell structure", [(b["cells"], 12), (m_mag, 8)]), ("Microscopy and magnification", [(m_mag, 20)]), ("Transport across membranes", [(b["cells"], 6), (m_wp, 14)]),
                       ("Cell division", [(m_mitotic, 16), (b["cells"], 4)]), ("The immune system", [(b["imm"], 20)])]),
            U("Biology", 3, "exchange-and-transport", "Organisms exchange substances with their environment",
              "Surface area to volume ratio, gas exchange in single-celled organisms, insects, fish, plants and humans, digestion and absorption, haemoglobin and oxygen transport, the circulatory system and the heart, tissue fluid, and transport in plants.",
              "Exchange and Transport Systems", "exchange and transport",
              "Free Year 12 A level biology worksheets on exchange and transport: SA:V ratio, gas exchange, ventilation, digestion, haemoglobin, cardiac output, the heart and transpiration. 100 questions with answers.",
              "Cardiac output = stroke volume × heart rate.", "Pulmonary ventilation = tidal volume × breathing rate.",
              "<p>Large organisms have a small surface area to volume ratio, so they need specialised exchange surfaces with a large area, a short diffusion distance and a steep concentration gradient. Cardiac output = stroke volume × heart rate; pulmonary ventilation = tidal volume × breathing rate.</p>"
              "<p>Haemoglobin loads oxygen where the partial pressure is high and unloads it in respiring tissues; more CO₂ shifts the dissociation curve to the right (the Bohr effect). Water is pulled up the xylem by transpiration (cohesion–tension); sugars move in the phloem by mass flow.</p>",
              [("SV 70 cm³, HR 72. Cardiac output?", ["70 × 72 = 5,040 cm³ min⁻¹"], "5.04 dm³ min⁻¹"),
               ("SA:V of a 2 cm cube?", ["SA = 24 cm², V = 8 cm³"], "3 : 1")],
              ["Forgetting to change cm³ to dm³.", "Thinking bigger animals have a bigger SA:V.", "Saying phloem carries water up from the roots."],
              [("Why is the oxygen dissociation curve S-shaped?", "After one oxygen binds, haemoglobin changes shape and loads more oxygen easily (cooperative binding)."),
               ("What is the cohesion–tension theory?", "Water evaporating from leaves pulls a continuous column of water molecules, held by hydrogen bonds, up the xylem.")],
              lambda: [("Surface area and gas exchange", [(m_sav, 8), (b["gas"], 12)]), ("Breathing and digestion", [(K(m_cardiac, "vent", "tv"), 12), (b["gas"], 6), (m_sav, 2)]),
                       ("The heart", [(K(m_cardiac, "CO", "SV", "HR", "cycle"), 20)]), ("Haemoglobin and circulation", [(b["circ"], 14), (K(m_cardiac, "CO", "cycle"), 6)]),
                       ("Transport in plants", [(b["plant"], 10), (K(m_potometer, "transp"), 10)])]),
            U("Biology", 4, "genetic-information-and-variation", "Genetic information, variation and relationships between organisms",
              "DNA, genes and chromosomes, protein synthesis (transcription and translation), mutations and meiosis, genetic diversity and natural selection, species and classification, and measuring biodiversity.",
              "Genetic Information, Variation and Biodiversity", "genetic information and variation",
              "Free Year 12 A level biology worksheets on genetic information: the genetic code, transcription, translation, meiosis, mutation, classification and Simpson's index. 100 questions with answers.",
              "DNA → mRNA (transcription) → polypeptide (translation).", "Gamete combinations = 2ⁿ, where n is the number of chromosome pairs.",
              "<p>A gene is a sequence of bases coding for a polypeptide. In transcription, mRNA is made complementary to the template strand (U replaces T). In translation, tRNA anticodons pair with mRNA codons; each triplet codes for one amino acid. Only exons are translated.</p>"
              "<p>Meiosis makes four genetically different haploid cells through crossing over and independent segregation (2ⁿ combinations). Simpson's index D = 1 − Σn(n − 1)/N(N − 1) measures diversity: closer to 1 means more diverse.</p>",
              [("Template TAC GGA: mRNA?", ["complement with U for A"], "AUG CCU"),
               ("2n = 8. Gamete combinations?", ["n = 4", "2⁴"], "16")],
              ["Writing T instead of U in mRNA.", "Using 2n instead of n in 2ⁿ.", "Using N² instead of N(N − 1) in Simpson's index."],
              [("Why is the genetic code degenerate?", "Most amino acids are coded for by more than one triplet, so some base substitutions have no effect."),
               ("What does a high Simpson's index mean?", "The community is diverse: many species with similar numbers of individuals.")],
              lambda: [("DNA, genes and chromosomes", [(b["gene"], 8), (K(m_mrna, "aa"), 12)]), ("Protein synthesis", [(K(m_mrna, "mrna", "anti", "trip"), 14), (b["gene"], 6)]),
                       ("Meiosis and mutation", [(m_meiosis, 12), (b["var"], 8)]), ("Diversity and selection", [(b["var"], 8), (m_taxa, 4), (m_meiosis, 6), (m_simpson, 2)]),
                       ("Classification and biodiversity", [(m_simpson, 14), (m_taxa, 6)])]),
        ]
    return [
        U("Biology", 1, "photosynthesis-respiration-and-energy-transfer", "Energy transfers in and between organisms",
          "Light-dependent and light-independent reactions of photosynthesis, limiting factors, glycolysis, the link reaction, the Krebs cycle and oxidative phosphorylation, anaerobic respiration, respiratory quotient, energy transfer through ecosystems, productivity and nutrient cycles.",
          "Photosynthesis, Respiration and Energy Transfer", "photosynthesis and respiration",
          "Free Year 13 A level biology worksheets on energy transfers: photosynthesis, respiration, Rf values, respiratory quotient, GPP and NPP, efficiency, and the nitrogen cycle. 100 questions with answers.",
          "NPP = GPP − R.", "Efficiency = energy at next level ÷ energy at previous level × 100.",
          "<p>Photosynthesis: the light-dependent reaction on the thylakoids uses light to make ATP and reduced NADP and splits water (photolysis); the Calvin cycle in the stroma fixes CO₂ with rubisco. Respiration: glycolysis (cytoplasm), link reaction and Krebs cycle (matrix) and oxidative phosphorylation (cristae).</p>"
          "<p>Net primary production NPP = GPP − respiratory losses. Only about 10% of energy passes to the next trophic level. RQ = CO₂ given out ÷ O₂ taken in (1.0 for carbohydrate, 0.7 for lipid).</p>",
          [("GPP 20,000, R 12,000 kJ m⁻² year⁻¹. NPP?", ["20,000 − 12,000"], "8,000 kJ m⁻² year⁻¹"),
           ("O₂ in 30 cm³, CO₂ out 21 cm³. RQ?", ["21 ÷ 30"], "0.7")],
          ["Adding respiration to GPP to get NPP.", "Dividing O₂ by CO₂ for RQ.", "Putting glycolysis in the mitochondria."],
          [("What is the difference between GPP and NPP?", "GPP is the total chemical energy made by photosynthesis; NPP is what is left after the plant's own respiration."),
           ("Why does anaerobic respiration make so little ATP?", "Without oxygen the electron transfer chain and Krebs cycle stop, so only glycolysis makes ATP.")],
          lambda: [("Photosynthesis", [(b["photo"], 12), (K(m_energy, "rf"), 8)]), ("Respiration", [(b["resp"], 14), (K(m_energy, "rq"), 6)]),
                   ("Respirometers and RQ", [(K(m_potometer, "resp"), 12), (K(m_energy, "rq"), 8)]), ("Productivity", [(K(m_energy, "npp", "gpp"), 20)]),
                   ("Energy transfer and nutrient cycles", [(K(m_energy, "eff"), 12), (b["cycle"], 8)])]),
        U("Biology", 2, "response-and-homeostasis", "Organisms respond to changes in their environments",
          "Plant growth factors and tropisms, taxes and kineses, reflexes, receptors, control of heart rate, nerve impulses and synapses, skeletal muscle contraction, and homeostasis: control of blood glucose and of blood water potential by the kidney.",
          "Nervous Control, Muscles and Homeostasis", "response and homeostasis",
          "Free Year 13 A level biology worksheets on response and homeostasis: action potentials, synapses, muscle contraction, insulin and glucagon, the kidney, ADH and tropisms. 100 questions with answers.",
          "Speed = distance ÷ time (mm per ms = m s⁻¹).", "Homeostasis uses negative feedback.",
          "<p>An action potential happens when voltage-gated Na⁺ channels open (depolarisation) and then K⁺ channels open (repolarisation). Myelin gives saltatory conduction. At synapses, Ca²⁺ triggers release of neurotransmitter, which diffuses across the cleft. In muscle, Ca²⁺ exposes binding sites on actin and ATP drives the myosin heads.</p>"
          "<p>Insulin lowers blood glucose; glucagon raises it. In the kidney, ultrafiltration happens at the glomerulus, glucose is reabsorbed in the proximal tubule, and ADH makes the collecting duct more permeable to water.</p>",
          [("50 mm in 2.0 ms. Speed?", ["50 mm ÷ 2.0 ms"], "25 m s⁻¹"),
           ("Refractory period 2 ms. Maximum frequency?", ["1 ÷ 0.002 s"], "500 Hz")],
          ["Forgetting that 1 mm/ms = 1 m/s.", "Saying bigger stimuli give bigger action potentials.", "Mixing up insulin and glucagon."],
          [("What is saltatory conduction?", "In myelinated axons the impulse jumps from one node of Ranvier to the next, so it travels faster."),
           ("What does ADH do?", "It makes the walls of the collecting duct more permeable to water, so more water is reabsorbed and urine is more concentrated.")],
          lambda: [("Nerve impulses", [(b["nerve"], 10), (K(m_nerve, "speed"), 10)]), ("Synapses and muscles", [(b["nerve"], 8), (K(m_nerve, "freq"), 6), (K(m_nerve, "speed"), 6)]),
                   ("Blood glucose", [(b["home"], 8), (K(m_nerve, "gluc"), 12)]), ("The kidney", [(b["home"], 6), (K(m_nerve, "kid"), 14)]),
                   ("Mixed problems", [(b["home"], 6), (K(m_nerve, "speed", "freq"), 10), (K(m_nerve, "kid"), 4)])]),
        U("Biology", 3, "genetics-populations-and-evolution", "Genetics, populations, evolution and ecosystems",
          "Monohybrid and dihybrid crosses, codominance, multiple alleles, sex linkage, autosomal linkage and epistasis, the chi-squared test, the Hardy–Weinberg principle, natural selection, speciation, populations in ecosystems, sampling methods, succession and conservation.",
          "Genetics, Populations and Evolution", "genetics and populations",
          "Free Year 13 A level biology worksheets on genetics and populations: Punnett squares, sex linkage, chi-squared, Hardy–Weinberg, speciation, mark–release–recapture and quadrats. 100 questions with answers.",
          "p + q = 1 and p² + 2pq + q² = 1.", "χ² = Σ(O − E)²/E with (categories − 1) degrees of freedom.",
          "<p>Use a Punnett square to work out expected ratios. A 3 : 1 ratio comes from Aa × Aa, 9 : 3 : 3 : 1 from AaBb × AaBb. The chi-squared test compares observed and expected numbers; if χ² is less than the critical value, the difference is due to chance.</p>"
          "<p>Hardy–Weinberg: the recessive phenotype frequency is q²; take the square root for q, then p = 1 − q and carriers = 2pq. Mark–release–recapture estimates population size: N = n₁n₂/m.</p>",
          [("4% show a recessive trait. Carriers?", ["q² = 0.04, q = 0.2, p = 0.8", "2pq = 0.32"], "32%"),
           ("50 marked, 40 caught later with 5 marked. N?", ["50 × 40 ÷ 5"], "400")],
          ["Using q² as the allele frequency.", "Using the number of categories as the degrees of freedom.", "Dividing by O instead of E in χ²."],
          [("When is a chi-squared result significant?", "When χ² is greater than the critical value at p = 0.05 for the right degrees of freedom: the difference is not due to chance."),
           ("What does the Hardy–Weinberg principle assume?", "A large population with random mating and no mutation, migration or selection, so allele frequencies stay the same.")],
          lambda: [("Genetic crosses", [(m_cross, 20)]), ("The chi-squared test", [(m_chi, 20)]), ("Hardy–Weinberg", [(m_hw, 20)]),
                   ("Evolution and speciation", [(b["evo"], 12), (m_hw, 4), (m_cross, 4)]), ("Populations and sampling", [(m_pop, 16), (b["evo"], 4)])]),
        U("Biology", 4, "gene-expression-and-biotechnology", "The control of gene expression",
          "Gene mutations, stem cells, regulation of transcription and translation, epigenetics, gene expression and cancer, genome projects, recombinant DNA technology, PCR, DNA probes, genetic screening, gene therapy and genetic fingerprinting.",
          "Gene Expression and Biotechnology", "gene expression and biotechnology",
          "Free Year 13 A level biology worksheets on gene expression: stem cells, transcription factors, epigenetics, cancer, PCR, restriction enzymes, gel electrophoresis and genetic fingerprinting. 100 questions with answers.",
          "PCR doubles the DNA every cycle: copies = start × 2ⁿ.", "Small DNA fragments travel furthest in a gel.",
          "<p>Genes are switched on and off by transcription factors, RNA interference and epigenetic changes (DNA methylation, histone acetylation). Mutations in tumour suppressor genes and proto-oncogenes can cause uncontrolled cell division.</p>"
          "<p>Recombinant DNA: cut with restriction enzymes to leave sticky ends, join into a vector with DNA ligase, and use marker genes to find transformed cells. PCR copies DNA: start × 2ⁿ after n cycles. Gel electrophoresis separates fragments by size.</p>",
          [("10 molecules, 5 PCR cycles. Molecules?", ["10 × 2⁵"], "320"),
           ("1,000 bp cut at 300 and 700. Fragments?", ["300, 400, 300"], "400 and 300 bp")],
          ["Multiplying by 2 × n instead of 2ⁿ.", "Thinking large fragments move furthest.", "Thinking epigenetic changes alter the base sequence."],
          [("What is a transcription factor?", "A protein that binds to DNA near a gene and switches its transcription on or off."),
           ("Why is Taq polymerase used in PCR?", "It comes from bacteria in hot springs and is not denatured at the 95 °C used to separate DNA strands.")],
          lambda: [("Mutations and stem cells", [(b["gx"], 12), (K(m_mrna, "trip"), 8)]), ("Regulating gene expression", [(b["gx"], 8), (K(m_biotech, "probe"), 12)]),
                   ("Recombinant DNA", [(b["bio"], 12), (K(m_biotech, "gel"), 8)]), ("PCR", [(K(m_biotech, "pcr", "pcrn"), 16), (b["bio"], 4)]),
                   ("Genetic fingerprinting and screening", [(K(m_biotech, "gel"), 16), (b["bio"], 4)])]),
    ]
