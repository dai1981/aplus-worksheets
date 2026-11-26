# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Chemistry): Bonding, Structure and Properties
  python tools/gen_uk_science_y10_bonding_and_structure.py
Ionic, covalent and metallic bonding, formulae of ionic compounds, the three states of matter, giant ionic lattices,
simple molecules, giant covalent structures (diamond, graphite, graphene, fullerenes), metals and alloys, and how
structure explains melting point and conductivity. Reuses the bonding, formula, state and boiling-point questions of
the US Chemistry units in British English (electronegativity and polarity are left out).
Wrong answers come from real mistakes: "ionic compounds conduct when solid", "melting a simple molecule breaks
covalent bonds", "graphite does not conduct", "metals are held by ionic bonds".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62006)
CB = "chem_chemical_bonding"
IM = "chem_intermolecular_forces_and_properties"
nopol = ("electronegativ", "polar", "hydrogen bond", "dipole")
nopol2 = ("electronegativ", "polar", "dipole")
us_btype, us_cov, us_formula, us_name = [us(CB, "g_" + n, drop=nopol2) for n in ("btype", "cov", "formula", "name")]
us_bp, us_order, us_solid, us_state = [us(IM, "g_" + n, drop=nopol) for n in ("bp", "order", "solid", "state")]

STR = [("sodium chloride", "giant ionic lattice"), ("magnesium oxide", "giant ionic lattice"), ("water", "simple molecules"), ("carbon dioxide", "simple molecules"),
       ("methane", "simple molecules"), ("diamond", "giant covalent structure"), ("graphite", "giant covalent structure"), ("silicon dioxide (sand)", "giant covalent structure"),
       ("copper", "giant metallic lattice"), ("iron", "giant metallic lattice"), ("oxygen", "simple molecules"), ("potassium bromide", "giant ionic lattice")]
PROP = {"giant ionic lattice": "high melting point; conducts only when melted or dissolved",
        "simple molecules": "low melting point; does not conduct electricity",
        "giant covalent structure": "very high melting point; usually does not conduct (graphite does)",
        "giant metallic lattice": "high melting point; conducts when solid"}


def g_str():
    s, t = R.choice(STR)
    k = R.random() < 0.5
    if not once(("st", s, k)):
        return None
    if k:
        return item("What is the structure of %s?" % s, t, [x for x in PROP if x != t], "Ionic compounds, small molecules, giant covalent and metals.")
    return item("Which properties would you expect for %s (a %s)?" % (s, t), PROP[t], [v for x, v in PROP.items() if x != t], "Structure explains properties.")


CAR = [("diamond", "Each carbon is bonded to four others, so it is very hard and has a very high melting point."),
       ("graphite", "Each carbon is bonded to three others in layers that slide, and delocalised electrons let it conduct."),
       ("graphene", "a single layer of graphite: very strong and conducts electricity"),
       ("fullerenes", "hollow molecules of carbon atoms, such as C₆₀, used to deliver drugs"),
       ("carbon nanotubes", "cylindrical fullerenes with very high strength for their mass")]


def g_car():
    f, d = R.choice(CAR)
    if not once(("ca", f)):
        return None
    return item("Which form of carbon is described here? “%s”" % (d[0].upper() + d[1:] + ("" if d.endswith(".") else ".")), f, [x[0] for x in CAR if x[0] != f][:3], "Allotropes of carbon.")


B1 = bank([
    ("What happens in ionic bonding?", "Electrons are transferred from a metal atom to a non-metal atom, making oppositely charged ions.", ["Electrons are shared between non-metals.", "Electrons are delocalised in a metal.", "Protons are transferred."], "Metal + non-metal."),
    ("What happens in covalent bonding?", "Non-metal atoms share pairs of electrons.", ["Metals give electrons to non-metals.", "Ions attract each other.", "Electrons move freely in a sea."], "Non-metal + non-metal."),
    ("What is metallic bonding?", "attraction between positive metal ions and a sea of delocalised electrons", ["sharing electrons between two non-metals", "transfer of electrons to a non-metal", "attraction between molecules"], "Explains conductivity."),
    ("Why do ionic compounds have high melting points?", "Strong electrostatic forces between oppositely charged ions in all directions need lots of energy to overcome.", ["The molecules are large.", "They have weak forces.", "They contain metals only."], "Giant lattice."),
    ("Why does melting a simple molecular substance need little energy?", "Only the weak forces between molecules are overcome, not the covalent bonds.", ["Covalent bonds are weak.", "The molecules break apart into atoms.", "Ionic bonds break."], "Intermolecular forces."),
])
B5 = bank([
    ("Why do ionic compounds conduct electricity when molten but not when solid?", "When molten the ions are free to move and carry charge.", ["Electrons are free in the solid.", "Solids have no ions.", "Melting makes new electrons."], "Mobile ions."),
    ("Why are alloys harder than pure metals?", "Different-sized atoms distort the layers so they cannot slide easily.", ["Alloys have no layers.", "Alloys are compounds.", "Alloys contain ions."], "Steel, brass."),
    ("Why do metals conduct electricity?", "Delocalised electrons can move through the structure.", ["Their ions move freely in the solid.", "They have no electrons.", "Their atoms share electrons in pairs."], "Free electrons."),
    ("What is the formula of the compound formed between Mg²⁺ and Cl⁻ ions?", "MgCl₂", ["MgCl", "Mg₂Cl", "Mg₂Cl₂"], "Charges must balance."),
    ("Why is graphene useful in electronics?", "It is very strong, light and conducts electricity.", ["It is an insulator.", "It is very heavy.", "It melts easily."], "One layer thick."),
    ("Which change of state happens at the boiling point?", "liquid to gas", ["solid to liquid", "gas to solid", "liquid to solid"], "Evaporation throughout the liquid."),
])

if __name__ == "__main__":
  build(U, 10, "bonding-and-structure", 6, "Chemistry", "Bonding, structure and the properties of matter",
      "Ionic, covalent and metallic bonding; the formation of ions and ionic compounds and their formulae; the three states of matter and changes of state; the properties of ionic compounds, small molecules, polymers, giant covalent structures and metals and alloys; diamond, graphite, graphene and fullerenes; how structure and bonding explain melting and boiling points and electrical conductivity.",
      "Bonding, Structure and Properties", "Bonding and Structure",
      "Free Year 10 GCSE Combined Science worksheets on bonding and structure: ionic, covalent and metallic bonding, formulae, giant lattices, simple molecules, diamond, graphite and graphene. 100 questions with answers.",
      "Structure explains melting point and conductivity.",
      "Ionic: transfer electrons. Covalent: share electrons. Metallic: sea of electrons.",
      "<p><b>The type of bonding decides a substance's properties.</b></p><ul><li>Ionic (metal + non-metal): giant lattice, high melting point, conducts only when molten or dissolved.</li>"
      "<li>Covalent (non-metals): small molecules with low melting points, or giant covalent structures such as diamond and graphite.</li>"
      "<li>Metallic: positive ions in a sea of delocalised electrons, so metals conduct and are malleable.</li></ul>",
      [("Na⁺ and O²⁻. Formula?", ["Two Na⁺ balance one O²⁻"], "Na₂O"), ("Low melting point, does not conduct. Structure?", ["Weak forces between molecules"], "simple molecules")],
      ["Thinking ionic compounds conduct when solid.", "Thinking melting a simple molecule breaks covalent bonds.", "Thinking graphite cannot conduct."],
      [("What is the difference between ionic and covalent bonding?", "In ionic bonding electrons are transferred from metal to non-metal atoms, forming ions. In covalent bonding non-metal atoms share pairs of electrons."),
       ("Why does graphite conduct electricity but diamond does not?", "In graphite each carbon bonds to three others, leaving one delocalised electron per atom that can move. In diamond all four outer electrons are in bonds."),
       ("Why do simple molecular substances have low melting points?", "Only the weak intermolecular forces need to be overcome; the strong covalent bonds inside the molecules do not break.")],
      [("Types of bonding", B1 + [(us_btype, 10), (us_cov, 5)]),
       ("Formulae and names", [(us_formula, 10), (us_name, 10)]),
       ("Structures", [(g_str, 14), (us_solid, 6)]),
       ("States and boiling points", [(us_state, 8), (us_bp, 6), (us_order, 6)]),
       ("Carbon and metals", B5 + [(g_car, 4), (g_str, 7), (us_btype, 3)])])
