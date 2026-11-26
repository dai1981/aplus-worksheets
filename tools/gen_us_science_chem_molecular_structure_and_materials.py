# -*- coding: utf-8 -*-
"""
US High School Chemistry: Molecular Structure and Designed Materials (HS-PS2-6)
  python tools/gen_us_science_chem_molecular_structure_and_materials.py
Communicate scientific and technical information about why the molecular-level structure is important in the
functioning of designed materials.
How structure explains properties (metals, ionic solids, network solids, polymers, graphite and diamond), "like
dissolves like", polymers and monomers, and choosing materials for a job.
Wrong answers come from real mistakes: "graphite and diamond are different elements", "oil dissolves in water if
stirred hard", "all plastics conduct electricity".
"""
from sci_common import Unit, item, bank, lesson, make, People

U = Unit(90214)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


SP = [("Copper wire conducts electricity.", "Its electrons are free to move through the metal."),
      ("Gold can be hammered into very thin sheets.", "Layers of metal atoms can slide past each other without breaking the metallic bond."),
      ("Diamond is the hardest natural material.", "Each carbon atom is covalently bonded to four others in a rigid 3D network."),
      ("Graphite is slippery and used in pencils.", "Carbon atoms form flat layers that slide over each other."),
      ("Graphite conducts electricity but diamond does not.", "In graphite each carbon has one electron free to move along the layers."),
      ("Table salt shatters when hit with a hammer.", "Shifting the ions lines up like charges, which repel."),
      ("Rubber bands stretch and spring back.", "Long, tangled polymer chains straighten when pulled and coil again."),
      ("Kevlar in body armor is very strong.", "Its long, straight chains are held side by side by many hydrogen bonds."),
      ("A nonstick pan coating repels water and oil.", "Its polymer is covered in fluorine atoms that attract other molecules very weakly."),
      ("Soap removes grease from your hands.", "Each soap molecule has a water-loving end and a grease-loving end."),
      ("Silica aerogel is a very good insulator.", "It is mostly tiny pores of air held in a network of silicon and oxygen."),
      ("Superabsorbent polymers in diapers soak up water.", "Their chains have many charged groups that attract water molecules."),
      ("Water expands when it freezes.", "Hydrogen bonds hold the molecules in an open hexagonal pattern."),
      ("Wax melts in a candle flame.", "Wax molecules are held by weak London forces.")]


def g_sp():
    p, s = R.choice(SP)
    k = R.random() < 0.65
    if not once(("sp", p, k)):
        return None
    if k:
        return item("%s Which explanation at the molecular level is best?" % p, s, R.sample([x[1] for x in SP if x[1] != s], 3), "Structure explains the property.")
    return item("Which property is explained by this structure: “%s”" % s, p.rstrip("."), R.sample([x[0].rstrip(".") for x in SP if x[0] != p], 3), "Match structure to function.")


SOLUTE = [("table salt (NaCl)", "ionic"), ("sugar", "polar"), ("vegetable oil", "nonpolar"), ("candle wax", "nonpolar"), ("iodine (I₂)", "nonpolar"), ("ethanol", "polar"),
          ("motor oil", "nonpolar"), ("vitamin C", "polar"), ("vitamin A", "nonpolar"), ("ammonia", "polar"), ("potassium nitrate", "ionic"), ("butter", "nonpolar")]
SOLV = [("water", "polar"), ("hexane", "nonpolar"), ("gasoline", "nonpolar"), ("vinegar (mostly water)", "polar")]


def g_dis():
    a, ka = R.choice(SOLUTE)
    b, kb = R.choice(SOLV)
    if not once(("ds", a, b)):
        return None
    yes = (ka in ("ionic", "polar")) == (kb == "polar")
    ans = "Yes, it dissolves well." if yes else "No, it does not dissolve well."
    return item("Will %s dissolve well in %s (a %s solvent)?" % (a, b, kb) if "(" not in b else "Will %s dissolve well in %s, a polar solvent?" % (a, b), ans, ["No, it does not dissolve well." if yes else "Yes, it dissolves well.", "Only if it is stirred very hard.", "Only if the solvent is frozen."],
                "Like dissolves like: %s substances dissolve in %s solvents." % ("polar and ionic" if ka != "nonpolar" else "nonpolar", "polar" if ka != "nonpolar" else "nonpolar"))


JOB = [("electrical wiring", "copper (a metal)", ["glass (a network solid)", "salt (an ionic solid)", "wax (a molecular solid)"]),
       ("a cutting tool for stone", "diamond (a covalent network)", ["graphite", "lead", "polyethylene"]),
       ("a dry lubricant for a lock", "graphite (sliding layers)", ["diamond", "salt", "rubber"]),
       ("the handle of a frying pan", "a heat-resistant plastic that does not conduct heat well", ["copper", "aluminum", "iron"]),
       ("a raincoat", "a nonpolar polymer that water cannot soak into", ["cotton (absorbs water)", "paper", "salt crystals"]),
       ("a bulletproof vest", "Kevlar (strong hydrogen-bonded chains)", ["wax", "graphite", "table salt"]),
       ("a stretchy waistband", "rubber (elastic polymer chains)", ["glass", "diamond", "copper wire"]),
       ("a nonstick pan", "a fluorine-coated polymer (PTFE)", ["bare iron", "sugar glaze", "salt"]),
       ("a solar panel cell", "silicon (a semiconductor)", ["wood", "rubber", "wax"]),
       ("an airplane frame", "aluminum alloy (strong and light)", ["lead", "glass", "wax"])]


def g_job():
    j, a, w = R.choice(JOB)
    if not once(("jb", j)):
        return None
    return item("Which material is the best choice for %s?" % j, a, w, "Choose the structure whose properties fit the job.")


MON = [("ethylene", "polyethylene (plastic bags)"), ("glucose", "starch or cellulose"), ("amino acids", "proteins"), ("nucleotides", "DNA"),
       ("vinyl chloride", "PVC (pipes)"), ("styrene", "polystyrene (foam cups)"), ("isoprene", "natural rubber")]


def g_poly():
    k = R.choice(["mon", "mass"])
    if k == "mon":
        m, p = R.choice(MON)
        rev = R.random() < 0.5
        if not once(("pm", m, rev)):
            return None
        if rev:
            return item("Which monomer is linked to make %s?" % p, m, R.sample([x[0] for x in MON if x[0] != m], 3), "Polymers are chains of repeating monomers.")
        return item("Many %s monomers are linked in a long chain. Which polymer forms?" % m, p, R.sample([x[1] for x in MON if x[1] != p], 3), "Polymers are chains of repeating monomers.")
    n = R.choice([500, 1000, 2000, 5000, 10000, 20000])
    m, mm = R.choice([("ethylene (C₂H₄, 28 g/mol)", 28), ("propylene (C₃H₆, 42 g/mol)", 42), ("styrene (C₈H₈, 104 g/mol)", 104), ("vinyl chloride (C₂H₃Cl, 62.5 g/mol)", 62.5)])
    if not once(("ms", n, mm)):
        return None
    v = n * mm
    def c(x):
        return "{:,}".format(int(x)) if x == int(x) else "{:,}".format(x)
    return item("A polymer chain is made of %s units of %s. About what is its molar mass?" % (c(n), m), "%s g/mol" % c(v), ["%s g/mol" % c(mm), "%s g/mol" % c(n), "%s g/mol" % c(v * 10)],
                "%s × %s = %s g/mol." % (c(n), c(mm), c(v)))


B1 = bank([
    ("Why are graphite and diamond so different even though both are pure carbon?", "Their atoms are arranged and bonded differently.", ["They are different elements.", "Diamond has more protons.", "Graphite is a metal."], "Allotropes."),
    ("What is a polymer?", "a very large molecule made of many repeating units", ["a single small molecule", "a type of metal", "an ion"], "Monomers linked in chains."),
    ("What does 'like dissolves like' mean?", "Polar solvents dissolve polar or ionic substances; nonpolar dissolves nonpolar.", ["Everything dissolves in water.", "Only metals dissolve.", "Heavy things dissolve light things."], "Similar forces."),
    ("Why are metals good conductors of electricity?", "They have delocalized electrons that can move.", ["They have no electrons.", "Their ions cannot move.", "They are always hot."], "Sea of electrons."),
    ("Why do ionic compounds conduct when melted but not as solids?", "In the liquid, the ions are free to move.", ["Melting creates electrons.", "Solids have no ions.", "Liquids are metals."], "Mobile charges."),
    ("What is a semiconductor used for?", "computer chips and solar cells", ["cooking pans", "rubber tires", "window glass"], "Silicon."),
    ("Why is water a good solvent for many substances?", "Water molecules are polar and attract ions and polar molecules.", ["Water is nonpolar.", "Water is a metal.", "Water has no charge."], "Universal solvent."),
    ("What makes a material 'designed'?", "Its molecular structure is chosen or engineered to give useful properties.", ["It is found only in nature.", "It has no structure.", "It is always metal."], "Engineering at the molecular level."),
])
B5 = bank([
    ("Engineers add carbon atoms to iron to make steel. Why is steel harder than pure iron?", "Carbon atoms block layers of iron atoms from sliding.", ["Carbon makes iron lighter.", "Steel has no metallic bonds.", "Carbon conducts electricity."], "Alloys."),
    ("Why are medicines often made as salts (ionic forms)?", "Ionic forms dissolve better in water, so the body absorbs them.", ["Salts taste better.", "Ionic forms are nonpolar.", "Salts never dissolve."], "Solubility."),
    ("Why does a plastic bag not rot quickly in a landfill?", "Microbes cannot easily break its long, stable polymer chains.", ["It is a metal.", "It dissolves in rain.", "It has no bonds."], "Persistent polymers."),
    ("A scientist designs a biodegradable plastic. What structural change helps?", "bonds in the chain that microbes or water can break", ["stronger carbon-carbon bonds", "adding more fluorine", "making it ionic"], "Design for breakdown."),
    ("Why are electrical wires coated with plastic?", "Plastic is a nonconductor that keeps current in the metal wire.", ["Plastic conducts better.", "Plastic makes wires heavier.", "Plastic melts the wire."], "Insulation."),
])


def body():
    think = ("<p><b>Structure at the particle level decides how a material behaves.</b></p>"
             "<ul><li>Metals: sea of electrons → conduct and bend. Ionic solids: hard, brittle, conduct when melted or dissolved. Network solids: very hard.</li>"
             "<li>Polymers: long chains of monomers; chain shape and forces give stretch, strength or water resistance.</li>"
             "<li>Like dissolves like: polar or ionic in water; nonpolar in nonpolar solvents.</li></ul>")
    ex = [("Why does graphite conduct but diamond does not?", ["Graphite has free electrons in its layers"], "free-moving electrons"),
          ("Will oil dissolve in water?", ["Oil nonpolar, water polar"], "no")]
    mist = ["Thinking graphite and diamond are different elements.", "Thinking stirring makes oil dissolve in water.", "Thinking all solids conduct electricity."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Structure and properties", B1 + [(g_sp, 12)]),
        ("Why materials behave as they do", [(g_sp, 10), (g_dis, 10)]),
        ("Like dissolves like", [(g_dis, 14), (g_poly, 6)]),
        ("Polymers", [(g_poly, 14), (g_job, 6)]),
        ("Choosing materials", B5 + [(g_job, 2), (g_dis, 6), (g_poly, 5), (g_sp, 2)]),
    ])
    make("chemistry", "molecular-structure-and-materials", 14, "HS-PS2-6",
         "Communicate scientific and technical information about why the molecular-level structure is important in the functioning of designed materials.",
         "Molecular Structure and Designed Materials",
         "Materials Chemistry Worksheets: Structure, Polymers and Solubility (High School Chemistry)",
         "Materials and Structure",
         "Free high school chemistry worksheets on molecular structure and designed materials (NGSS HS-PS2-6): metals, ionic and network solids, polymers, solubility and choosing materials. 100 questions with answers.",
         "Structure decides properties.",
         "How particles are arranged and bonded explains why a material conducts, stretches or dissolves.",
         body(),
         [("Why does molecular structure matter for materials?", "The way atoms are bonded and arranged decides properties such as strength, conductivity, flexibility and solubility."),
          ("What is a polymer?", "A very large molecule made by linking many small units called monomers, such as ethylene in polyethylene."),
          ("What does like dissolves like mean?", "Polar and ionic substances dissolve in polar solvents such as water; nonpolar substances dissolve in nonpolar solvents.")],
         sets)


if __name__ == "__main__":
    main()
