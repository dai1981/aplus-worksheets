# -*- coding: utf-8 -*-
"""
US High School Biology: Carbon and Macromolecules (HS-LS1-6)
  python tools/gen_us_science_bio_carbon_and_macromolecules.py
Construct and revise an explanation based on evidence for how carbon, hydrogen, and oxygen from sugar molecules may
combine with other elements to form amino acids and/or other large carbon-based molecules.
Carbohydrates, lipids, proteins and nucleic acids: monomers, elements (CHO, CHON, CHONP), examples, counting atoms in
formulas, and dehydration synthesis (n monomers release n - 1 water molecules).
Wrong answers come from real mistakes: "fats are made of amino acids", "proteins have only C, H and O",
"joining 10 monomers releases 10 water molecules".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
import re

U = Unit(90106)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


MAC = {"carbohydrates": ("monosaccharides (simple sugars like glucose)", "C, H and O"), "proteins": ("amino acids", "C, H, O and N (some also S)"),
       "lipids": ("fatty acids and glycerol", "C, H and O"), "nucleic acids": ("nucleotides", "C, H, O, N and P")}


def g_mono():
    m = R.choice(sorted(MAC))
    k = R.choice(["mono", "rev"])
    if not once((m, k)):
        return None
    if k == "mono":
        return item("What are the building blocks (monomers) of %s?" % m, MAC[m][0], [MAC[x][0] for x in MAC if x != m], "%s are built from %s." % (m.capitalize(), MAC[m][0]))
    return item("Many %s join to form which kind of molecule?" % MAC[m][0], m, [x for x in MAC if x != m], "%s → %s." % (MAC[m][0], m))


def g_elem():
    m = R.choice(sorted(MAC))
    if m in ("lipids",):      # lipids and carbohydrates share CHO; ask only the distinct ones
        return None
    if not once(("e", m)):
        return None
    w = ["C, H and O only" if m != "carbohydrates" else "C, H, O and N (some also S)", "C, H, O, N and P" if m != "nucleic acids" else "C, H and O only", "only C and H"]
    a = MAC[m][1] if m != "carbohydrates" else "C, H and O only"
    return item("Which elements make up %s?" % m, a, w, "Nitrogen comes in with amino acids; phosphorus with nucleotides.")


EXM = [("starch in a potato", "carbohydrates"), ("cellulose in plant cell walls", "carbohydrates"), ("glycogen stored in the liver", "carbohydrates"), ("table sugar (sucrose)", "carbohydrates"),
       ("an enzyme such as amylase", "proteins"), ("hemoglobin in red blood cells", "proteins"), ("keratin in hair", "proteins"), ("antibodies", "proteins"), ("muscle fibers (actin and myosin)", "proteins"),
       ("olive oil", "lipids"), ("butter", "lipids"), ("the phospholipids in a cell membrane", "lipids"), ("wax on a leaf", "lipids"), ("cholesterol", "lipids"),
       ("DNA", "nucleic acids"), ("mRNA", "nucleic acids"), ("tRNA", "nucleic acids")]


def g_ex():
    e, m = R.choice(EXM)
    if not once(e):
        return None
    return item("Which kind of macromolecule is %s?" % e, m, [x for x in MAC if x != m], "%s is one of the %s." % (e[0].upper() + e[1:], m))


FORM = [("glucose", "C6H12O6"), ("fructose", "C6H12O6"), ("sucrose", "C12H22O11"), ("glycine (an amino acid)", "C2H5NO2"), ("alanine (an amino acid)", "C3H7NO2"),
        ("glycerol", "C3H8O3"), ("ribose", "C5H10O5"), ("palmitic acid (a fatty acid)", "C16H32O2"), ("cysteine (an amino acid)", "C3H7NO2S"), ("ethanol", "C2H6O")]


def parse(f):
    return [(el, int(n) if n else 1) for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", f)]


def show(f):
    return re.sub(r"(\d+)", r"<sub>\1</sub>", f)


def g_atoms():
    nm, f = R.choice(FORM)
    parts = parse(f)
    k = R.choice(["total", "el", "N"])
    if not once((nm, k)):
        return None
    tot = sum(n for _, n in parts)
    if k == "total":
        return item("The formula of %s is %s. How many atoms are in one molecule?" % (nm, show(f)), str(tot), [str(len(parts)), str(tot + 2), str(tot - 1)],
                    "Add the subscripts: %s = %d." % (" + ".join(str(n) for _, n in parts), tot))
    if k == "el":
        el, n = R.choice(parts)
        nmz = {"C": "carbon", "H": "hydrogen", "O": "oxygen", "N": "nitrogen", "S": "sulfur"}[el]
        w = list(dict.fromkeys([str(x) for _, x in parts if x != n] + [str(n + 1), str(n * 2), str(max(1, n - 1))]))
        w = [x for x in w if x != str(n)][:3]
        return item("The formula of %s is %s. How many %s atoms are in one molecule?" % (nm, show(f), nmz), str(n), w, "Read the subscript after %s." % el)
    has = any(el == "N" for el, _ in parts)
    return item("The formula of %s is %s. Does it contain nitrogen?" % (nm, show(f)), "yes" if has else "no", ["no" if has else "yes", "only when heated", "only in plants"],
                "Amino acids contain N; sugars and fats do not.")


def g_dehyd():
    n = R.randint(2, 60)
    m = R.choice(["glucose molecules", "amino acids", "nucleotides"])
    k = R.choice(["water", "bonds"])
    if not once((n, k)):
        return None
    poly = {"glucose molecules": "a starch chain", "amino acids": "a protein chain", "nucleotides": "a DNA strand"}[m]
    if k == "water":
        return item("%d %s join by dehydration synthesis to form %s. How many water molecules are released?" % (n, m, poly), str(n - 1), [str(n), str(n + 1), str(2 * n)],
                    "One water per bond: %d − 1 = %d." % (n, n - 1))
    return item("How many bonds join %d %s in one straight chain?" % (n, m), str(n - 1), [str(n), str(n + 1), str(n // 2)], "A chain of %d units has %d links." % (n, n - 1))


B1 = bank([
    ("Why is carbon so important for life?", "Each carbon atom can form four bonds, making chains and rings.", ["Carbon is a metal.", "Carbon has no bonds.", "Carbon is only in rocks."], "Backbone of biomolecules."),
    ("Where do plants get the carbon to build amino acids?", "from sugars made in photosynthesis (from CO<sub>2</sub>)", ["from the soil", "from oxygen", "from light"], "Sugar's C, H, O are rearranged."),
    ("What extra element must be added to a sugar's C, H and O to make an amino acid?", "nitrogen", ["iron", "sodium", "helium"], "Plants take nitrate from soil."),
    ("What extra elements are found in nucleic acids?", "nitrogen and phosphorus", ["iron and calcium", "only carbon", "helium and neon"], "Phosphate groups."),
    ("What is the main job of carbohydrates?", "quick energy and structure (like cellulose)", ["carrying genetic code", "speeding reactions as enzymes", "storing hereditary information"], "Sugars and starches."),
    ("What is the main job of lipids?", "long-term energy storage and cell membranes", ["copying DNA", "carrying oxygen", "making ribosomes"], "Fats, oils, phospholipids."),
    ("What is a main job of proteins?", "enzymes, structure, transport and defense", ["storing genetic code", "being the main fuel in cell walls", "forming the cell wall of plants"], "Many shapes, many jobs."),
    ("What is the main job of nucleic acids?", "storing and carrying genetic information", ["insulating the body", "giving quick energy", "forming hair"], "DNA and RNA."),
])
B5 = bank([
    ("A student tests foods: iodine turns a potato blue-black. Which macromolecule is present?", "starch (a carbohydrate)", ["protein", "fat", "DNA"], "Iodine test for starch."),
    ("Biuret solution turns purple with egg white. What is in egg white?", "protein", ["starch", "simple sugar only", "DNA only"], "Biuret test for protein."),
    ("A brown paper bag turns see-through where a food sample is rubbed. What is in the food?", "lipids (fat)", ["protein", "starch", "water only"], "Grease spot test."),
    ("Benedict's solution turns orange when heated with juice. What is present?", "simple sugars like glucose", ["protein", "fat", "DNA"], "Benedict's test."),
    ("A plant is given radioactive carbon in CO<sub>2</sub>. Later the carbon is found in its proteins. What does this show?", "Carbon from sugar is used to build amino acids and proteins.", ["Proteins come from soil.", "Carbon cannot move.", "Proteins have no carbon."], "Tracing atoms."),
])


def body():
    think = ("<p><b>Small units join into big molecules.</b> Sugars made in photosynthesis supply C, H and O; adding N (and P, S) makes the other molecules.</p>"
             "%s") % table(["Macromolecule", "Monomer", "Elements"], [[m, MAC[m][0], MAC[m][1]] for m in MAC])
    ex = [("10 amino acids join. Water released?", ["One water per bond", "10 − 1"], "9"),
          ("Glycine is C2H5NO2. How many atoms?", ["2 + 5 + 1 + 2"], "10")]
    mist = ["Thinking fats are made of amino acids. They are made of fatty acids and glycerol.", "Thinking proteins have only C, H and O. They also have N.",
            "Counting n water molecules for n monomers. It is n − 1."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The four macromolecules", B1 + [(g_mono, 6), (g_elem, 3), (g_ex, 3)]),
        ("Monomers and examples", [(g_mono, 2), (g_ex, 14), (g_atoms, 4)]),
        ("Counting atoms", [(g_atoms, 14), (g_dehyd, 6)]),
        ("Building big molecules", [(g_dehyd, 14), (g_atoms, 6)]),
        ("Food tests and evidence", B5 + [(g_dehyd, 15)]),
    ])
    make("biology", "carbon-and-macromolecules", 6, "HS-LS1-6",
         "Construct and revise an explanation based on evidence for how carbon, hydrogen, and oxygen from sugar molecules may combine with other elements to form amino acids and/or other large carbon-based molecules.",
         "Carbon and Macromolecules",
         "Macromolecules Worksheets: Carbohydrates, Lipids, Proteins and Nucleic Acids (Biology)",
         "Macromolecules",
         "Free high school biology worksheets on macromolecules (NGSS HS-LS1-6): carbohydrates, lipids, proteins and nucleic acids, monomers, elements and dehydration synthesis. 100 questions with answers.",
         "Small units build big molecules.",
         "C, H and O from sugar, plus N and P, build proteins, fats and nucleic acids.",
         body(),
         [("What are the four macromolecules?", "Carbohydrates, lipids, proteins and nucleic acids."),
          ("How do sugars become amino acids?", "Cells rearrange the C, H and O from sugars and add nitrogen (and sometimes sulfur) to build amino acids."),
          ("What is dehydration synthesis?", "Joining two monomers by removing a water molecule. A chain of n monomers releases n − 1 waters.")],
         sets)


if __name__ == "__main__":
    main()
