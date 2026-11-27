# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Chemistry (6092), Topic 3: Chemical Bonding and Structure
  python tools/gen_sg_science_s3_chemical_bonding_and_structure.py
Ionic bonding (electron transfer, ions with noble gas configurations, formulae of ionic compounds), covalent bonding (shared
pairs, dot-and-cross diagrams of simple molecules), metallic bonding (positive ions in a sea of delocalised electrons), and
how structure explains properties: giant ionic lattices, simple molecular substances, giant covalent (diamond, graphite,
silicon dioxide), metals and alloys.
US and UK bonding makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "ionic compounds conduct when solid", "simple molecular substances have low melting
points because covalent bonds are weak", "graphite conducts because of its ions", "magnesium chloride is MgCl".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Chemistry", 15
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

NOPOL = lambda it: not any(w in it["q"] + it["c"][0] + it["e"] for w in ("polar", "electronegativ", "lone pair", "metalloid"))
us_bt = keep(src("gen_us_science_chem_chemical_bonding", "g_btype"), NOPOL)
us_form = keep(src("gen_us_science_chem_chemical_bonding", "g_formula"), NOPOL)
us_name = keep(src("gen_us_science_chem_chemical_bonding", "g_name"), NOPOL)
us_bp = keep(src("gen_us_science_chem_intermolecular_forces_and_properties", "g_bp"), NOPOL)
us_solid = keep(src("gen_us_science_chem_intermolecular_forces_and_properties", "g_solid"), NOPOL)
uk_str = src("gen_uk_science_y10_bonding_and_structure", "g_str")

IONS = [("sodium", "Na", 11, 1), ("magnesium", "Mg", 12, 2), ("aluminium", "Al", 13, 3), ("potassium", "K", 19, 1), ("calcium", "Ca", 20, 2), ("lithium", "Li", 3, 1),
        ("chlorine", "Cl", 17, -1), ("oxygen", "O", 8, -2), ("fluorine", "F", 9, -1), ("sulfur", "S", 16, -2), ("nitrogen", "N", 7, -3)]


def chg(c):
    return ("%d" % abs(c) if abs(c) > 1 else "") + ("+" if c > 0 else "−")


def g_ion():
    n, s, z, c = R.choice(IONS)
    k = R.choice(["how", "sym", "conf"])
    if k == "how":
        a = "It loses %d electron%s." % (c, "s" if c > 1 else "") if c > 0 else "It gains %d electron%s." % (-c, "s" if c < -1 else "")
        wr = ["It gains %d electron%s." % (abs(c), "s" if abs(c) > 1 else "") if c > 0 else "It loses %d electron%s." % (-c, "s" if c < -1 else ""),
              "It shares %d electron%s." % (abs(c), "s" if abs(c) > 1 else ""), "It gains %d protons." % abs(c) if abs(c) > 1 else "It gains a proton."]
        return tq("How does a %s atom (proton number %d) form an ion?" % (n, z), a, wr, "Atoms gain or lose electrons to reach a noble gas electronic configuration.")
    if k == "sym":
        a = s + "<sup>%s</sup>" % chg(c)
        wr = [s + "<sup>%s</sup>" % chg(-c), s + "<sup>%s</sup>" % chg(c + (1 if c > 0 else -1)), s + "<sup>%s</sup>" % chg(c - 1 if c > 1 else c + 1 if c < -1 else (2 if c > 0 else -2))]
        if len({a} | set(wr)) < 4:
            return None
        return tq("What is the formula of the ion formed by %s?" % n, a, wr, "%s (Z = %d) %s %d electron%s." % (n.capitalize(), z, "loses" if c > 0 else "gains", abs(c), "s" if abs(c) > 1 else ""))
    e = z - c
    conf = {2: "2", 10: "2, 8", 18: "2, 8, 8"}[e]
    return tq("What is the electronic configuration of the %s ion?" % (s + "<sup>%s</sup>" % chg(c)), conf, [x for x in ("2", "2, 8", "2, 8, 8", "2, 8, 1", "2, 8, 7") if x != conf][:3],
              "The ion has %d electrons, the same arrangement as a noble gas." % e)


def g_formula():
    cat = R.choice([x for x in IONS if x[3] > 0])
    an = R.choice([x for x in IONS if x[3] < 0])
    names = {"Cl": "chloride", "O": "oxide", "F": "fluoride", "S": "sulfide", "N": "nitride"}
    a, b = cat[3], -an[3]
    from math import gcd
    g = gcd(a, b)
    nx, ny = b // g, a // g
    f = lambda s, n: s + ("<sub>%d</sub>" % n if n > 1 else "")
    ans = f(cat[1], nx) + f(an[1], ny)
    wr = {f(cat[1], ny) + f(an[1], nx), cat[1] + an[1], f(cat[1], a) + f(an[1], b) if (a, b) != (nx, ny) else f(cat[1], 1) + f(an[1], 2)}
    wr.discard(ans)
    extra = 1
    while len(wr) < 3:
        wr.add(f(cat[1], nx + extra) + f(an[1], ny))
        wr.discard(ans)
        extra += 1
    return tq("What is the formula of %s %s?" % (cat[0], names[an[1]]), ans, sorted(wr)[:3],
              "%s<sup>%s</sup> and %s<sup>%s</sup>: the charges must balance, so the formula is %s." % (cat[1], chg(cat[3]), an[1], chg(an[3]), ans))


MOL = [("H<sub>2</sub>", "hydrogen", 1, "single"), ("Cl<sub>2</sub>", "chlorine", 1, "single"), ("O<sub>2</sub>", "oxygen", 2, "double"), ("N<sub>2</sub>", "nitrogen", 3, "triple"),
       ("H<sub>2</sub>O", "water", 2, "two single"), ("NH<sub>3</sub>", "ammonia", 3, "three single"), ("CH<sub>4</sub>", "methane", 4, "four single"),
       ("CO<sub>2</sub>", "carbon dioxide", 4, "two double"), ("HCl", "hydrogen chloride", 1, "single"), ("C<sub>2</sub>H<sub>4</sub>", "ethene", 6, "one double and four single")]


def g_pairs():
    f, n, p, kind = R.choice(MOL)
    if R.random() < 0.6:
        return nq("How many pairs of electrons are shared in a molecule of %s (%s)?" % (n, f), p, [p + 1, p * 2, max(1, p - 1) if p > 1 else 3], "",
                  "%s has %s covalent bond%s: %d shared pair%s." % (n.capitalize(), kind, "" if kind == "single" else "s", p, "" if p == 1 else "s"))
    return tq("What type of covalent bonding is in a molecule of %s (%s)?" % (n, f), kind + " bond" + ("" if kind in ("single", "double", "triple") else "s"),
              [x + " bond" for x in ("single", "double", "triple") if x != kind][:2] + ["an ionic bond"], "Count the shared pairs in the dot-and-cross diagram.")


STR = [("sodium chloride", "giant ionic lattice"), ("magnesium oxide", "giant ionic lattice"), ("water", "simple molecular"), ("carbon dioxide", "simple molecular"),
       ("iodine", "simple molecular"), ("diamond", "giant covalent (macromolecular)"), ("graphite", "giant covalent (macromolecular)"), ("silicon dioxide (sand)", "giant covalent (macromolecular)"),
       ("copper", "giant metallic lattice"), ("brass (an alloy)", "giant metallic lattice"), ("methane", "simple molecular"), ("calcium chloride", "giant ionic lattice")]
g_str = rows(R, STR, "What is the structure of %s?", "Which substance has a %s structure?")

PROP = [("high melting point; conducts electricity when molten or dissolved but not when solid", "an ionic compound"),
        ("low melting and boiling points; does not conduct electricity", "a simple molecular substance"),
        ("very high melting point; very hard; does not conduct electricity", "a giant covalent substance such as diamond"),
        ("high melting point; conducts electricity when solid and when molten; malleable", "a metal"),
        ("very high melting point; soft and slippery; conducts electricity", "graphite"),
        ("high melting point; hard; insoluble; does not conduct; used for glass", "silicon dioxide")]
g_prop = rows(R, PROP, "Which type of substance has these properties: %s?")

WHY = [("Why does sodium chloride have a high melting point?", "A lot of energy is needed to overcome the strong electrostatic forces between the oppositely charged ions in the giant lattice.",
        ["The covalent bonds in the molecules are strong.", "Its molecules are large.", "Its delocalised electrons hold it together."]),
       ("Why does solid sodium chloride not conduct electricity?", "Its ions are held in fixed positions and cannot move.", ["It has no ions.", "Its electrons are fixed.", "It is a covalent compound."]),
       ("Why does molten sodium chloride conduct electricity?", "Its ions are free to move and carry charge.", ["Its electrons become free.", "It becomes a metal.", "Its molecules break into atoms."]),
       ("Why do simple molecular substances have low melting points?", "Only weak intermolecular forces must be overcome, not the strong covalent bonds.",
        ["Their covalent bonds are weak.", "They contain ions.", "Their atoms are small."]),
       ("Why is diamond very hard?", "Each carbon atom is joined to four others by strong covalent bonds in a giant 3D structure.", ["It has delocalised electrons.", "It has weak forces between layers.", "It is an ionic lattice."]),
       ("Why does graphite conduct electricity?", "Each carbon atom uses three electrons in bonds, so one electron per atom is delocalised and free to move.", ["It contains ions.", "Its layers are metal.", "It has no electrons."]),
       ("Why is graphite soft and used as a lubricant?", "Its layers are held by weak forces and can slide over each other.", ["Its covalent bonds are weak.", "It is a metal.", "It has no layers."]),
       ("Why can metals conduct electricity?", "They have delocalised electrons that can move through the lattice.", ["They have mobile positive ions.", "They are shiny.", "Their atoms share pairs of electrons."]),
       ("Why are metals malleable?", "Layers of positive ions can slide over each other without breaking the metallic bonding.", ["Their ions repel each other.", "They are soft.", "They have weak covalent bonds."]),
       ("Why is an alloy harder than the pure metal?", "Atoms of different sizes disrupt the regular layers, so the layers cannot slide easily.", ["Alloys are compounds.", "Alloys have no delocalised electrons.", "Alloys are ionic."])]


def g_why():
    q, a, w = R.choice(WHY)
    return tq(q, a, w, "Properties depend on the particles and the forces between them.")


POOL1 = pool(R, [
    ("What happens in ionic bonding?", "Electrons are transferred from metal atoms to non-metal atoms, forming oppositely charged ions that attract.", ["Electrons are shared between two non-metals.", "Protons are transferred.", "Metal atoms share a sea of electrons."], "Ions get noble gas configurations."),
    ("What is a covalent bond?", "a shared pair of electrons between two non-metal atoms", ["the attraction between oppositely charged ions", "a transferred electron", "the attraction between metal ions and electrons"], "Each atom gains a full outer shell."),
    ("What is metallic bonding?", "the attraction between positive metal ions and a sea of delocalised electrons", ["sharing of electron pairs between metal atoms", "transfer of electrons from metals to non-metals", "attraction between neutral metal atoms"], "Explains conductivity and malleability."),
    ("Which pair of elements forms an ionic compound?", "sodium and chlorine", ["carbon and oxygen", "hydrogen and chlorine", "nitrogen and hydrogen"], "A metal and a non-metal."),
    ("Which pair of elements forms a covalent compound?", "carbon and hydrogen", ["sodium and oxygen", "magnesium and chlorine", "calcium and fluorine"], "Two non-metals."),
    ("Why do atoms form bonds?", "to achieve a stable noble gas electronic configuration", ["to gain protons", "to become radioactive", "to lose all their electrons"], "Usually a full outer shell of 8 (or 2)."),
    ("What is an alloy?", "a mixture of a metal with one or more other elements", ["a compound of two metals", "a pure metal that has been heated", "an ionic compound"], "Steel is iron with carbon."),
    ("Which statement about the ions in magnesium oxide is correct?", "Both Mg²⁺ and O²⁻ have the electronic configuration 2, 8.", ["Mg²⁺ has 12 electrons.", "O²⁻ has 6 electrons.", "They share electrons."], "Both have neon's arrangement."),
])
POOL5 = pool(R, [
    ("Magnesium oxide has a much higher melting point than sodium chloride. Why?", "Its ions carry larger charges (2+ and 2−), so the electrostatic attraction is stronger.", ["It has covalent bonds.", "Its ions are bigger.", "It contains delocalised electrons."], "Both are giant ionic lattices."),
    ("Why does silicon dioxide have a very high melting point?", "Many strong covalent bonds must be broken in its giant structure.", ["Its intermolecular forces are strong.", "It is ionic.", "It contains free electrons."], "It is macromolecular, like diamond."),
    ("Why are electrical wires made of copper rather than diamond?", "Copper has delocalised electrons that carry current; diamond has none.", ["Diamond melts easily.", "Copper is harder.", "Diamond has free ions."], "Copper is also ductile."),
    ("Why is steel used for building rather than pure iron?", "Steel is an alloy, so it is harder and stronger.", ["Pure iron is too hard.", "Steel is lighter than iron.", "Steel is a compound."], "Carbon atoms stop iron layers sliding."),
    ("Why does water have a much lower boiling point than sodium chloride?", "Water is simple molecular, with weak forces between molecules; sodium chloride has strong ionic bonds.", ["Water has weak covalent bonds.", "Sodium chloride is lighter.", "Water is ionic."], "Only intermolecular forces break when water boils."),
    ("A substance melts at 1600 °C, does not conduct when solid or molten, and is insoluble. What is its likely structure?", "giant covalent", ["giant ionic", "simple molecular", "metallic"], "It does not conduct even when molten, so it has no ions."),
    ("A substance melts at 80 °C and does not conduct electricity. What is its likely structure?", "simple molecular", ["giant ionic", "giant covalent", "metallic"], "Low melting point: weak intermolecular forces."),
    ("How many electrons does each atom share in the covalent bond in a chlorine molecule?", "one each, making one shared pair", ["two each", "none: chlorine is ionic", "seven each"], "Each chlorine atom gets 8 outer electrons."),
])


def main():
    sets = U.sets([
        ("Ionic bonding", [POOL1, (g_ion, 8), (g_formula, 4)]),
        ("Formulae of ionic compounds", [(g_formula, 8), (us_form, 5), (us_name, 5), (g_ion, 2)]),
        ("Covalent bonding", [(g_pairs, 8), (us_bt, 5), POOL1, (POOL5, 2)]),
        ("Structure and properties", [(g_str, 6), (g_prop, 5), (g_why, 6), (us_solid, 3)]),
        ("Exam-style questions", [(POOL5, 7), (g_why, 4), (us_bp, 4), (uk_str, 3), (g_prop, 2)]),
    ])
    make_ol(LV, SUBJ, "chemical-bonding-and-structure", SORT, "Chemical Bonding and Structure",
            "Describe the formation of ions by electron loss or gain and the formation of ionic bonds between metals and non-metals; deduce the formulae of ionic "
            "compounds; describe covalent bonding as the sharing of pairs of electrons and draw dot-and-cross diagrams for simple molecules; describe metallic bonding "
            "as positive ions in a sea of delocalised electrons; relate the physical properties of giant ionic, simple molecular and giant covalent substances (diamond, "
            "graphite, silicon dioxide), metals and alloys to their structure and bonding (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Chemical Bonding and Structure", "Bonding and structure",
            "Free Secondary 3 O-Level Chemistry worksheets on chemical bonding and structure: ionic, covalent and metallic bonding, formulae, dot-and-cross diagrams, giant and "
            "simple structures, diamond, graphite and alloys. 100 questions with answers.",
            "Ionic: transfer. Covalent: sharing. Metallic: sea of electrons.", "Structure explains melting point and conductivity.",
            "<p><b>Atoms bond to reach a noble gas electronic configuration.</b></p><ul>"
            "<li>Ionic (metal + non-metal): electrons transferred; giant lattice of ions; high melting point; conducts only when molten or dissolved.</li>"
            "<li>Covalent (non-metals): shared pairs. Simple molecules have weak intermolecular forces (low melting point); giant covalent structures (diamond, SiO₂) have very high melting points.</li>"
            "<li>Metallic: positive ions in a sea of delocalised electrons; conducts when solid; malleable. Alloys are harder.</li>"
            "<li>Formula of an ionic compound: balance the charges (Al³⁺ and O²⁻ give Al₂O₃).</li></ul>",
            [("Formula of calcium chloride?", ["Ca²⁺ and Cl⁻", "two Cl⁻ balance one Ca²⁺"], "CaCl₂"),
             ("Shared pairs in N₂?", ["each N needs 3 more electrons"], "3 (a triple bond)")],
            ["Saying solid ionic compounds conduct electricity.", "Saying covalent bonds break when a simple molecular substance melts.",
             "Thinking graphite conducts because it has ions.", "Forgetting to balance the charges in a formula (writing MgCl instead of MgCl₂)."],
            [("How do you work out the formula of an ionic compound?", "Write the charges of the two ions, then use enough of each ion so the total positive and negative charges cancel."),
             ("Why do ionic compounds conduct only when molten or in solution?", "In the solid the ions are held in fixed positions; when molten or dissolved the ions are free to move and carry the charge."),
             ("Why does graphite conduct electricity but diamond does not?", "In graphite each carbon atom forms three bonds, leaving one delocalised electron; in diamond all four outer electrons are used in bonds.")],
            sets)


if __name__ == "__main__":
    main()
