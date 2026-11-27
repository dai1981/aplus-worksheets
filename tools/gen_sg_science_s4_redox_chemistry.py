# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Chemistry (6092), Topic 7: Redox Chemistry
  python tools/gen_sg_science_s4_redox_chemistry.py
Oxidation and reduction in terms of oxygen, hydrogen, electrons and oxidation state; oxidising and reducing agents (acidified
potassium manganate(VII), potassium iodide); electrolysis of molten compounds and of aqueous solutions (selective discharge with
inert and copper electrodes), electroplating and the purification of copper; simple cells and the hydrogen fuel cell.
UK electrolysis makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "oxidation is gain of electrons", "the oxidising agent is oxidised", "sodium is formed at
the cathode in electrolysis of aqueous sodium chloride", "the object to be plated is the anode".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Chemistry", 9
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_elec = src("gen_uk_science_y10_chemical_changes", "g_elec")

OXS = [("S", "in SO₂", 4), ("S", "in H₂SO₄", 6), ("S", "in H₂S", -2), ("N", "in NH₃", -3), ("N", "in HNO₃", 5), ("N", "in NO₂", 4), ("Mn", "in KMnO₄", 7), ("Mn", "in MnO₂", 4),
       ("Fe", "in Fe₂O₃", 3), ("Fe", "in FeO", 2), ("Cr", "in K₂Cr₂O₇", 6), ("Cu", "in CuO", 2), ("Cu", "in Cu₂O", 1), ("C", "in CO₂", 4), ("C", "in CO", 2), ("Cl", "in Cl₂", 0),
       ("Cl", "in NaCl", -1), ("O", "in H₂O₂", -1), ("H", "in NaH", -1), ("S", "in SO₃²⁻", 4), ("S", "in SO₄²⁻", 6), ("C", "in CH₄", -4)]


def sgn(x):
    return "0" if x == 0 else ("+%d" % x if x > 0 else "−%d" % -x)


def g_os():
    e, where, v = R.choice(OXS)
    wr = {sgn(v + 2), sgn(-v) if v else "+2", sgn(v - 1)}
    wr.discard(sgn(v))
    while len(wr) < 3:
        wr.add(sgn(v + 4))
    return tq("What is the oxidation state of %s %s?" % (e, where), sgn(v), sorted(wr)[:3],
              "Oxygen is usually −2, hydrogen +1, Group 1 metals +1; the oxidation states add up to the overall charge.")


RX = [("2Mg + O₂ → 2MgO", "magnesium", "oxidised", "it gains oxygen"), ("CuO + H₂ → Cu + H₂O", "copper(II) oxide", "reduced", "it loses oxygen"),
      ("CuO + H₂ → Cu + H₂O", "hydrogen", "oxidised", "it gains oxygen"), ("Zn + Cu²⁺ → Zn²⁺ + Cu", "zinc", "oxidised", "it loses electrons"),
      ("Zn + Cu²⁺ → Zn²⁺ + Cu", "copper(II) ions", "reduced", "they gain electrons"), ("Cl₂ + 2Br⁻ → 2Cl⁻ + Br₂", "chlorine", "reduced", "it gains electrons"),
      ("Cl₂ + 2Br⁻ → 2Cl⁻ + Br₂", "bromide ions", "oxidised", "they lose electrons"), ("Fe₂O₃ + 3CO → 2Fe + 3CO₂", "iron(III) oxide", "reduced", "it loses oxygen"),
      ("Fe₂O₃ + 3CO → 2Fe + 3CO₂", "carbon monoxide", "oxidised", "it gains oxygen"), ("2Fe²⁺ + Cl₂ → 2Fe³⁺ + 2Cl⁻", "iron(II) ions", "oxidised", "their oxidation state rises from +2 to +3"),
      ("H₂S + Cl₂ → S + 2HCl", "hydrogen sulfide", "oxidised", "it loses hydrogen"), ("2Na + Cl₂ → 2NaCl", "sodium", "oxidised", "it loses an electron to form Na⁺")]


def g_rx():
    eq, sp, what, why = R.choice(RX)
    k = R.choice(["what", "agent"])
    if k == "what":
        return tq("In the reaction %s, what happens to %s?" % (eq, sp), "It is %s because %s." % (what, why) if not sp.endswith("ions") else "They are %s because %s." % (what, why),
                  [("It is %s because %s." if not sp.endswith("ions") else "They are %s because %s.") % ("reduced" if what == "oxidised" else "oxidised", why),
                   ("It is neither oxidised nor reduced." if not sp.endswith("ions") else "They are neither oxidised nor reduced."),
                   ("It is %s because it %s." if not sp.endswith("ions") else "They are %s because they %s.") % (what, "gains protons")],
                  "Oxidation: gain of oxygen, loss of hydrogen, loss of electrons, increase in oxidation state. Reduction is the opposite.")
    agent = "reducing agent" if what == "oxidised" else "oxidising agent"
    return tq("In the reaction %s, what is the role of %s?" % (eq, sp), "the %s" % agent, ["the %s" % ("oxidising agent" if agent == "reducing agent" else "reducing agent"), "a catalyst", "a spectator ion"],
              "The substance that is oxidised is the reducing agent; the substance that is reduced is the oxidising agent.")


ELEC = [("molten lead(II) bromide", "carbon", "lead", "bromine"), ("molten sodium chloride", "carbon", "sodium", "chlorine"), ("molten aluminium oxide", "carbon", "aluminium", "oxygen"),
        ("dilute sulfuric acid", "carbon", "hydrogen", "oxygen"), ("concentrated aqueous sodium chloride", "carbon", "hydrogen", "chlorine"),
        ("dilute aqueous sodium chloride", "carbon", "hydrogen", "oxygen"), ("aqueous copper(II) sulfate", "carbon", "copper", "oxygen"),
        ("aqueous copper(II) sulfate", "copper", "copper", "copper dissolves (no gas)"), ("aqueous sodium sulfate", "carbon", "hydrogen", "oxygen"),
        ("concentrated hydrochloric acid", "carbon", "hydrogen", "chlorine"), ("molten zinc chloride", "carbon", "zinc", "chlorine"), ("aqueous potassium iodide", "carbon", "hydrogen", "iodine")]
PRODS = ["lead", "bromine", "sodium", "chlorine", "aluminium", "oxygen", "hydrogen", "copper", "zinc", "iodine", "sulfur"]


def g_elec():
    e, el, cat, an = R.choice(ELEC)
    k = R.choice(["cat", "an"])
    elname = "inert carbon" if el == "carbon" else "copper"
    if k == "cat":
        return tq("%s is electrolysed with %s electrodes. What is formed at the cathode (negative electrode)?" % (e[0].upper() + e[1:], elname), cat,
                  R.sample([p for p in PRODS if p != cat and p != an], 3), "Positive ions go to the cathode. In aqueous solutions of reactive metals, hydrogen is discharged instead of the metal.")
    return tq("%s is electrolysed with %s electrodes. What happens at the anode (positive electrode)?" % (e[0].upper() + e[1:], elname),
              an if " " in an else "%s is formed" % an, ["%s is formed" % p for p in R.sample([p for p in PRODS if p not in (an, cat)], 3)],
              "Negative ions go to the anode. In dilute solutions OH⁻ is discharged (oxygen); concentrated chloride gives chlorine; a copper anode dissolves.")


HALF = [("at the cathode in molten sodium chloride", "Na⁺ + e⁻ → Na"), ("at the anode in molten sodium chloride", "2Cl⁻ → Cl₂ + 2e⁻"),
        ("at the cathode in aqueous copper(II) sulfate", "Cu²⁺ + 2e⁻ → Cu"), ("at the cathode in dilute sulfuric acid", "2H⁺ + 2e⁻ → H₂"),
        ("at the anode in dilute sulfuric acid", "4OH⁻ → O₂ + 2H₂O + 4e⁻"), ("at a copper anode in aqueous copper(II) sulfate", "Cu → Cu²⁺ + 2e⁻")]
g_half = rows(R, HALF, "Which half-equation shows the reaction %s?")

CELLS = [("zinc", "copper"), ("magnesium", "copper"), ("magnesium", "iron"), ("zinc", "iron"), ("magnesium", "zinc"), ("iron", "copper"), ("zinc", "silver"), ("aluminium", "copper")]
SERIES = ["magnesium", "aluminium", "zinc", "iron", "copper", "silver"]


def g_cell():
    a, b = R.choice(CELLS)
    k = R.choice(["neg", "volt", "flow"])
    if k == "neg":
        return tq("A simple cell is made from %s and %s dipped in an electrolyte. Which metal is the negative terminal?" % (a, b), a, [b, "both", "neither: cells need carbon"],
                  "The more reactive metal loses electrons more easily, so it is the negative terminal.")
    if k == "flow":
        return tq("In a simple cell made of %s and %s, in which direction do electrons flow in the external wire?" % (a, b), "from %s to %s" % (a, b),
                  ["from %s to %s" % (b, a), "through the electrolyte only", "they do not flow"], "Electrons flow from the more reactive metal (negative) to the less reactive metal.")
    c, d = R.sample(SERIES, 2)
    big = (c, d) if abs(SERIES.index(c) - SERIES.index(d)) >= 2 else None
    pairs = sorted([tuple(sorted((x, y), key=SERIES.index)) for x in SERIES for y in SERIES if SERIES.index(x) < SERIES.index(y)], key=lambda p: SERIES.index(p[1]) - SERIES.index(p[0]))
    best = pairs[-1]
    opts = R.sample(pairs[:-1], 3)
    return tq("Which pair of metals gives the largest voltage in a simple cell?", "%s and %s" % best, ["%s and %s" % p for p in opts],
              "The further apart the metals are in the reactivity series, the larger the voltage.")


POOL1 = pool(R, [
    ("What is oxidation in terms of electrons?", "loss of electrons", ["gain of electrons", "gain of protons", "loss of oxygen"], "OIL RIG: Oxidation Is Loss, Reduction Is Gain."),
    ("What is reduction in terms of oxygen?", "loss of oxygen", ["gain of oxygen", "loss of electrons", "gain of hydrogen ions only"], "Copper(II) oxide is reduced to copper."),
    ("What is a redox reaction?", "a reaction in which oxidation and reduction happen at the same time", ["a reaction that only oxidises", "a reaction with no electron transfer", "a neutralisation"], "One substance loses electrons as another gains them."),
    ("What is an oxidising agent?", "a substance that oxidises another substance and is itself reduced", ["a substance that is oxidised", "a catalyst", "a substance that loses electrons"], "It gains electrons."),
    ("What colour change shows that acidified potassium manganate(VII) has acted as an oxidising agent?", "purple to colourless", ["colourless to purple", "orange to green", "colourless to brown"], "It is reduced to Mn²⁺."),
    ("What colour change shows that aqueous potassium iodide has acted as a reducing agent?", "colourless to brown (iodine forms)", ["brown to colourless", "purple to colourless", "orange to green"], "Iodide ions are oxidised to iodine."),
    ("What is electrolysis?", "the decomposition of a compound (molten or in solution) by an electric current", ["dissolving a solid in water", "a reaction that produces electricity", "the burning of a metal"], "Ions move to the electrodes."),
    ("Why must an ionic compound be molten or dissolved for electrolysis?", "so that its ions are free to move to the electrodes", ["so that it becomes a metal", "to make it react with water", "so the electrons can move through it"], "Solid ions are fixed."),
    ("Which ions move to the cathode during electrolysis?", "positive ions (cations)", ["negative ions (anions)", "electrons", "all ions equally"], "The cathode is negative."),
    ("In electroplating a spoon with silver, which electrode is the spoon?", "the cathode", ["the anode", "either electrode", "it is the electrolyte"], "Silver ions are reduced onto the spoon."),
])
POOL5 = pool(R, [
    ("Why is hydrogen, not sodium, formed at the cathode when concentrated aqueous sodium chloride is electrolysed?", "Hydrogen ions are discharged in preference because hydrogen is less reactive than sodium.",
     ["Sodium is too heavy to move.", "Sodium ions are not present.", "Sodium reacts with chlorine."], "Selective discharge."),
    ("Why is chlorine, not oxygen, formed at the anode in concentrated aqueous sodium chloride?", "The chloride ions are at a high concentration, so they are discharged in preference.",
     ["Chlorine is lighter.", "There are no hydroxide ions.", "Oxygen dissolves."], "In dilute solution, oxygen forms instead."),
    ("How is impure copper purified by electrolysis?", "The impure copper is the anode and a thin pure copper strip is the cathode, in aqueous copper(II) sulfate.", ["Pure copper is the anode.", "Carbon electrodes are used.", "The electrolyte is sulfuric acid only."], "Copper dissolves at the anode and deposits on the cathode."),
    ("During the purification of copper, why does the blue colour of the electrolyte stay the same?", "Copper ions enter the solution at the anode as fast as they leave at the cathode.", ["No ions move.", "The solution is replaced.", "The current is too small."], "The concentration of Cu²⁺ stays constant."),
    ("What is formed in a hydrogen fuel cell?", "water only, with electrical energy", ["carbon dioxide and water", "hydrogen and oxygen", "sulfur dioxide"], "2H₂ + O₂ → 2H₂O."),
    ("Give one advantage of hydrogen fuel cells for buses.", "They produce no carbon dioxide at the point of use.", ["Hydrogen is easy to store.", "They produce sulfur dioxide.", "They need no fuel."], "But making and storing hydrogen is difficult."),
    ("Why does a copper(II) sulfate solution become paler when it is electrolysed with carbon electrodes?", "Copper ions are removed as copper metal at the cathode.", ["Water is added.", "Sulfate ions are removed.", "Carbon dissolves."], "Oxygen forms at the anode."),
    ("In 2KI + Cl₂ → 2KCl + I₂, which species is the oxidising agent?", "chlorine", ["iodide ions", "potassium ions", "iodine"], "Chlorine gains electrons."),
    ("What happens to the oxidation state of manganese when MnO₄⁻ becomes Mn²⁺?", "It decreases from +7 to +2, so manganese is reduced.", ["It increases from +2 to +7.", "It stays at +7.", "It decreases from +4 to +2."], "A decrease in oxidation state is reduction."),
    ("Which electrode reaction is an oxidation?", "2Cl⁻ → Cl₂ + 2e⁻", ["Cu²⁺ + 2e⁻ → Cu", "2H⁺ + 2e⁻ → H₂", "Na⁺ + e⁻ → Na"], "Electrons are lost at the anode."),
])


def main():
    sets = U.sets([
        ("Oxidation and reduction", [POOL1, (g_rx, 8), (g_os, 4)]),
        ("Oxidation states and redox agents", [(g_os, 9), (g_rx, 6), POOL1, (POOL5, 2)]),
        ("Electrolysis", [(g_elec, 12), (uk_elec, 4), (g_half, 4)]),
        ("Electroplating, purification and cells", [(g_cell, 8), (g_half, 2), POOL1, (POOL5, 5)]),
        ("Exam-style questions", [(POOL5, 7), (g_elec, 6), (g_os, 3), (g_cell, 2), (g_rx, 2)]),
    ])
    make_ol(LV, SUBJ, "redox-chemistry", SORT, "Redox Chemistry",
            "Define oxidation and reduction in terms of oxygen, hydrogen, electron transfer and changes in oxidation state; identify redox reactions, oxidising agents and "
            "reducing agents, including the use of acidified potassium manganate(VII) and potassium iodide; describe electrolysis of molten compounds and aqueous "
            "solutions using inert and copper electrodes, including selective discharge; describe electroplating and the purification of copper; describe simple cells "
            "and the hydrogen fuel cell (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Redox Chemistry", "Redox chemistry",
            "Free Secondary 4 O-Level Chemistry worksheets on redox chemistry: oxidation and reduction, oxidation states, oxidising and reducing agents, electrolysis, "
            "electroplating, simple cells and fuel cells. 100 questions with answers.",
            "OIL RIG: oxidation is loss, reduction is gain (of electrons).", "Cathode: cations reduced. Anode: anions oxidised.",
            "<p><b>Oxidation and reduction always happen together.</b></p><ul>"
            "<li>Oxidation: gain of oxygen, loss of hydrogen, loss of electrons, increase in oxidation state. Reduction is the opposite.</li>"
            "<li>The oxidising agent is reduced; the reducing agent is oxidised. KMnO₄ turns purple → colourless; KI turns colourless → brown.</li>"
            "<li>Electrolysis: cations go to the cathode (reduced), anions to the anode (oxidised). In aqueous solutions of reactive metals hydrogen forms; dilute solutions give oxygen at the anode.</li>"
            "<li>Simple cell: the more reactive metal is the negative terminal; further apart in the reactivity series gives a larger voltage.</li></ul>",
            [("Oxidation state of S in H₂SO₄?", ["2(+1) + S + 4(−2) = 0"], "+6"),
             ("Electrolysis of dilute H₂SO₄ with carbon electrodes. Products?", ["cathode: H⁺ → H₂", "anode: OH⁻ → O₂"], "hydrogen and oxygen (2 : 1 by volume)")],
            ["Saying oxidation is gain of electrons.", "Saying the oxidising agent is oxidised.",
             "Writing sodium at the cathode for aqueous sodium chloride.", "Making the object to be plated the anode."],
            [("How do you work out an oxidation state?", "Use the rules: oxygen is −2, hydrogen +1, Group 1 metals +1, and the oxidation states in a compound add up to zero (or to the charge of an ion)."),
             ("What decides the products of electrolysis of an aqueous solution?", "At the cathode, the less reactive of the metal and hydrogen is discharged. At the anode, oxygen forms from dilute solutions, but concentrated chloride or iodide gives chlorine or iodine; a copper anode dissolves."),
             ("How does electroplating work?", "The object is the cathode and the plating metal is the anode, in a solution of the plating metal's ions. Metal ions are reduced onto the object.")],
            sets)


if __name__ == "__main__":
    main()
