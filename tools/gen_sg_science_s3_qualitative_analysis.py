# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Chemistry (6092), Topic 6: Qualitative Analysis
  python tools/gen_sg_science_s3_qualitative_analysis.py
Tests for aqueous cations with aqueous sodium hydroxide and aqueous ammonia (Al³⁺, Ca²⁺, Cu²⁺, Fe²⁺, Fe³⁺, Zn²⁺, NH₄⁺),
tests for anions (carbonate, chloride, iodide, nitrate, sulfate) and tests for gases (ammonia, carbon dioxide, chlorine,
hydrogen, oxygen, sulfur dioxide), and deducing an unknown substance from several observations.
UK gas-test makers are reused (Singapore names); the rest are written from the O-Level qualitative analysis notes.
Wrong answers come from real mistakes: "Al³⁺ and Zn²⁺ both dissolve in excess aqueous ammonia", "Fe²⁺ gives a red-brown
precipitate", "add hydrochloric acid before testing for chloride", "carbon dioxide relights a glowing splint".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Chemistry", 18
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))


# cation: (name, NaOH few drops, NaOH excess, NH3 few drops, NH3 excess)
CAT = [("aluminium, Al³⁺", "white precipitate", "precipitate dissolves, giving a colourless solution", "white precipitate", "white precipitate is insoluble in excess"),
       ("calcium, Ca²⁺", "white precipitate", "white precipitate is insoluble in excess", "no precipitate (or a very slight white precipitate)", "no change"),
       ("copper(II), Cu²⁺", "light blue precipitate", "light blue precipitate is insoluble in excess", "light blue precipitate", "precipitate dissolves, giving a dark blue solution"),
       ("iron(II), Fe²⁺", "green precipitate", "green precipitate is insoluble in excess", "green precipitate", "green precipitate is insoluble in excess"),
       ("iron(III), Fe³⁺", "red-brown precipitate", "red-brown precipitate is insoluble in excess", "red-brown precipitate", "red-brown precipitate is insoluble in excess"),
       ("zinc, Zn²⁺", "white precipitate", "precipitate dissolves, giving a colourless solution", "white precipitate", "precipitate dissolves, giving a colourless solution"),
       ("ammonium, NH₄⁺", "no precipitate; on warming, ammonia gas is given off", "ammonia gas given off on warming", "—", "—")]


def g_cat():
    c = R.choice(CAT)
    name, n1, nx, a1, ax = c
    k = R.choice(["naoh", "nh3", "which", "which2"])
    if k == "naoh":
        if name.startswith("ammonium"):
            return tq("What is seen when aqueous sodium hydroxide is added to a solution containing ammonium ions and the mixture is warmed?",
                      "Ammonia gas is given off, which turns damp red litmus paper blue.", ["A white precipitate forms.", "A green precipitate forms.", "Hydrogen gas is given off."],
                      "NH₄⁺ + OH⁻ → NH₃ + H₂O on warming.")
        a = "%s; %s" % (n1, nx)
        wr = sorted({"%s; %s" % (x[1], x[2]) for x in CAT if x[0] != name and not x[0].startswith("ammonium")} - {a})
        return tq("Aqueous sodium hydroxide is added to a solution of %s ions, first a little and then in excess. What is seen?" % name.split(",")[0], a, R.sample(wr, 3),
                  "%s: with NaOH, %s; in excess, %s." % (name, n1, nx))
    if k == "nh3":
        if name.startswith("ammonium"):
            return None
        a = "%s; %s" % (a1, ax)
        wr = sorted({"%s; %s" % (x[3], x[4]) for x in CAT if x[0] != name and not x[0].startswith("ammonium")} - {a})
        return tq("Aqueous ammonia is added to a solution of %s ions, first a little and then in excess. What is seen?" % name.split(",")[0], a, R.sample(wr, 3),
                  "%s: with NH₃(aq), %s; in excess, %s." % (name, a1, ax))
    if name.startswith("ammonium") or name.startswith("calcium"):
        return None
    if k == "which":
        if sum(1 for x in CAT if x[1] == n1 and x[2] == nx) != 1:
            return None
        return tq("A solution gives a %s with aqueous sodium hydroxide, and in excess the %s. Which cation is present?" % (n1, nx), name,
                  R.sample([x[0] for x in CAT if x[0] != name], 3), "Only %s gives this result." % name)
    a = name
    ex_n = "dissolves in excess" if "dissolves" in nx else "does not dissolve in excess"
    ex_a = "dissolves in excess" if "dissolves" in ax else "does not dissolve in excess"
    return tq("A solution gives a %s with aqueous sodium hydroxide, which %s. With aqueous ammonia it gives a %s, which %s. Which cation is present?" % (n1, ex_n, a1, ex_a),
              a, R.sample([x[0] for x in CAT if x[0] != name], 3), "Use both reagents: %s." % name)


AN = [("carbonate, CO₃²⁻", "add dilute acid", "effervescence; the gas (carbon dioxide) turns limewater milky"),
      ("chloride, Cl⁻", "acidify with dilute nitric acid, then add aqueous silver nitrate", "white precipitate"),
      ("iodide, I⁻", "acidify with dilute nitric acid, then add aqueous silver nitrate", "yellow precipitate"),
      ("nitrate, NO₃⁻", "add aqueous sodium hydroxide, then aluminium foil, and warm carefully", "ammonia gas is given off, turning damp red litmus blue"),
      ("sulfate, SO₄²⁻", "acidify with dilute nitric acid, then add aqueous barium nitrate", "white precipitate")]


def g_an():
    name, test, res = R.choice(AN)
    k = R.choice(["res", "which", "test"])
    if k == "res":
        others = sorted({x[2] for x in AN if x[2] != res} | {"no change", "a green precipitate"})
        return tq("A solution contains %s ions. The test is to %s. What is the positive result?" % (name.split(",")[0], test), res, R.sample(others, 3), "%s: %s → %s." % (name, test, res))
    if k == "which":
        cands = [x for x in AN if x[1] == test and x[2] == res]
        if len(cands) != 1:
            return None
        return tq("A solution is tested: %s. Result: %s. Which anion is present?" % (test, res), name, R.sample([x[0] for x in AN if x[0] != name], 3), "This is the test for %s." % name)
    return tq("Which test identifies %s ions?" % name.split(",")[0], test + " (%s)" % res, R.sample(sorted({x[1] + " (%s)" % x[2] for x in AN if x[0] != name}), 3),
              "%s: %s." % (name, test))


CN = {"aluminium, Al³⁺": "aluminium", "calcium, Ca²⁺": "calcium", "copper(II), Cu²⁺": "copper(II)", "iron(II), Fe²⁺": "iron(II)", "iron(III), Fe³⁺": "iron(III)",
      "zinc, Zn²⁺": "zinc", "ammonium, NH₄⁺": "ammonium"}
AN_N = {"carbonate, CO₃²⁻": "carbonate", "chloride, Cl⁻": "chloride", "iodide, I⁻": "iodide", "nitrate, NO₃⁻": "nitrate", "sulfate, SO₄²⁻": "sulfate"}


BAD = {"iron(III) iodide", "aluminium carbonate", "iron(III) carbonate", "ammonium nitrate"}


def g_salt():
    c = R.choice(CAT)
    an = R.choice(AN)
    cname, aname = CN[c[0]], AN_N[an[0]]
    if aname == "carbonate" and cname not in ("ammonium",) and R.random() < 0.3:
        pass
    if aname == "nitrate" and cname == "ammonium":
        return None
    if cname == "ammonium":
        ctest = "warming the solution with aqueous sodium hydroxide gives a gas that turns damp red litmus blue"
    elif cname in ("aluminium", "zinc"):
        ctest = "aqueous ammonia gives a white precipitate that %s in excess" % ("dissolves" if cname == "zinc" else "does not dissolve")
    elif cname == "calcium":
        ctest = "aqueous sodium hydroxide gives a white precipitate that does not dissolve in excess, but aqueous ammonia gives no precipitate"
    else:
        ctest = "aqueous sodium hydroxide gives a %s" % c[1]
    atest = "%s: %s" % (an[1][0].upper() + an[1][1:], an[2])
    ans = "%s %s" % (cname, aname)
    wr = {"%s %s" % (cname, x) for x in AN_N.values() if x != aname} | {"%s %s" % (y, aname) for y in CN.values() if y != cname}
    wr = {w for w in wr if w not in BAD}
    if ans in BAD:
        return None
    return tq("Two tests are done on a substance X. Test 1: %s. Test 2: %s. What is X?" % (ctest[0].upper() + ctest[1:], atest), ans, R.sample(sorted(wr), 3),
              "The first test shows the %s ion and the second shows the %s ion." % (cname, aname))


COLS = [("copper(II) ions", "blue"), ("iron(II) ions", "pale green"), ("iron(III) ions", "yellow-brown"), ("zinc ions", "colourless"), ("aluminium ions", "colourless"), ("calcium ions", "colourless")]


def g_col():
    i, cl = R.choice(COLS)
    return tq("What colour is an aqueous solution containing %s (with a colourless anion)?" % i, cl, [x for x in ("blue", "pale green", "yellow-brown", "colourless", "purple") if x != cl][:3],
              "Transition metal ions are often coloured: Cu²⁺ blue, Fe²⁺ pale green, Fe³⁺ yellow-brown.")


GAS = [("ammonia", "turns damp red litmus paper blue"), ("carbon dioxide", "gives a white precipitate with limewater (turns it milky)"),
       ("chlorine", "bleaches damp litmus paper"), ("hydrogen", "burns with a 'pop' with a lighted splint"), ("oxygen", "relights a glowing splint"),
       ("sulfur dioxide", "turns acidified aqueous potassium manganate(VII) from purple to colourless")]
g_gas = rows(R, GAS, "What is the test result for %s?", "Which gas %s?")

GRX = [("zinc is added to dilute hydrochloric acid", "hydrogen"), ("marble chips are added to dilute hydrochloric acid", "carbon dioxide"),
       ("ammonium chloride is warmed with aqueous sodium hydroxide", "ammonia"), ("hydrogen peroxide is decomposed using manganese(IV) oxide", "oxygen"),
       ("concentrated hydrochloric acid is electrolysed", "chlorine (at the anode)"), ("sodium sulfite is warmed with dilute hydrochloric acid", "sulfur dioxide"),
       ("magnesium ribbon is added to dilute sulfuric acid", "hydrogen"), ("copper(II) carbonate is heated strongly", "carbon dioxide")]
g_grx = rows(R, GRX, "Which gas is given off when %s?", extra=["nitrogen"])


POOL1 = pool(R, [
    ("Why is dilute nitric acid added before aqueous silver nitrate in the chloride test?", "to remove carbonate ions, which would also give a precipitate", ["to make the precipitate dissolve", "to provide chloride ions", "to change the colour of the solution"], "Hydrochloric acid cannot be used because it contains Cl⁻."),
    ("Why must hydrochloric acid not be used to acidify a sample before testing for chloride ions?", "It contains chloride ions, which would give a white precipitate anyway.", ["It reacts with silver nitrate to give hydrogen.", "It is too weak.", "It makes the solution blue."], "Use dilute nitric acid."),
    ("Which two cations give white precipitates with aqueous sodium hydroxide that dissolve in excess?", "aluminium and zinc", ["calcium and zinc", "copper(II) and iron(II)", "aluminium and calcium"], "Use aqueous ammonia to tell them apart."),
    ("How can aluminium ions be distinguished from zinc ions?", "With excess aqueous ammonia, the zinc hydroxide precipitate dissolves but the aluminium hydroxide precipitate does not.",
     ["With sodium hydroxide only.", "By their colours in solution.", "Aluminium gives a blue precipitate."], "Both are white precipitates at first."),
    ("A green precipitate with sodium hydroxide slowly turns brown at the surface on standing. Why?", "Iron(II) hydroxide is oxidised by air to iron(III) hydroxide.", ["It dissolves in excess.", "Copper forms.", "It reacts with light to make chlorine."], "Fe²⁺ → Fe³⁺."),
    ("Which cation gives a dark blue solution with excess aqueous ammonia?", "copper(II), Cu²⁺", ["iron(II), Fe²⁺", "zinc, Zn²⁺", "calcium, Ca²⁺"], "A light blue precipitate forms first."),
    ("Which cation gives no precipitate with aqueous ammonia but a white precipitate with aqueous sodium hydroxide that does not dissolve in excess?", "calcium, Ca²⁺", ["zinc, Zn²⁺", "aluminium, Al³⁺", "iron(III), Fe³⁺"], "Calcium hydroxide is insoluble in excess NaOH."),
    ("What is the colour of the precipitate formed by iodide ions with acidified silver nitrate?", "yellow", ["white", "blue", "green"], "Silver iodide is yellow; silver chloride is white."),
])
POOL5 = pool(R, [
    ("A white solid X gives a white precipitate with aqueous sodium hydroxide that dissolves in excess, no precipitate with acidified barium nitrate, and a white precipitate with acidified silver nitrate. What is X?", "zinc chloride or aluminium chloride",
     ["zinc sulfate", "calcium chloride", "copper(II) chloride"], "Al³⁺ or Zn²⁺ with Cl⁻; use aqueous ammonia to decide."),
    ("A solution gives a red-brown precipitate with sodium hydroxide and a white precipitate with acidified barium nitrate. What is it?", "iron(III) sulfate", ["iron(II) sulfate", "iron(III) chloride", "copper(II) sulfate"], "Fe³⁺ and SO₄²⁻."),
    ("A solid fizzes with dilute acid, giving a gas that turns limewater milky. The solution gives a light blue precipitate with aqueous ammonia that dissolves in excess to form a dark blue solution. What is the solid?", "copper(II) carbonate",
     ["copper(II) sulfate", "zinc carbonate", "calcium carbonate"], "CO₃²⁻ and Cu²⁺."),
    ("When sodium hydroxide and aluminium foil are warmed with a solution, a gas turns damp red litmus blue. Which anion is present?", "nitrate, NO₃⁻", ["sulfate, SO₄²⁻", "chloride, Cl⁻", "carbonate, CO₃²⁻"], "The nitrate is reduced to ammonia."),
    ("Why must the solution be warmed when testing for ammonium ions?", "to drive the ammonia gas out of the solution so it can be detected", ["to make a precipitate form", "to stop the reaction", "to make the litmus red"], "Hold damp red litmus at the mouth of the tube."),
    ("A gas bleaches damp blue litmus paper after first turning it red. Which gas is it?", "chlorine", ["sulfur dioxide", "ammonia", "oxygen"], "Chlorine is acidic and a bleach."),
    ("Which reagent can distinguish between sodium chloride and sodium iodide solutions?", "acidified aqueous silver nitrate", ["aqueous sodium hydroxide", "aqueous ammonia", "limewater"], "White precipitate for chloride, yellow for iodide."),
    ("Which reagent can distinguish between iron(II) sulfate and iron(III) sulfate solutions?", "aqueous sodium hydroxide", ["acidified barium nitrate", "acidified silver nitrate", "dilute nitric acid"], "Green precipitate for Fe²⁺, red-brown for Fe³⁺."),
])


def main():
    sets = U.sets([
        ("Tests for cations with sodium hydroxide", [(g_cat, 9), (g_col, 5), POOL1]),
        ("Tests for cations with aqueous ammonia", [(g_cat, 8), (g_salt, 6), POOL1]),
        ("Tests for anions", [(g_an, 12), (g_salt, 4), POOL1]),
        ("Tests for gases", [(g_gas, 10), (g_grx, 6), (g_col, 1), (POOL5, 3)]),
        ("Identifying unknowns: exam-style questions", [(POOL5, 7), (g_salt, 10), (g_cat, 3)]),
    ])
    make_ol(LV, SUBJ, "qualitative-analysis", SORT, "Qualitative Analysis",
            "Describe and use tests to identify the aqueous cations aluminium, ammonium, calcium, copper(II), iron(II), iron(III) and zinc using aqueous sodium hydroxide and "
            "aqueous ammonia; the anions carbonate (by reaction with dilute acid and then limewater), chloride and iodide (with acidified silver nitrate), nitrate (by "
            "reduction with aluminium in alkaline solution) and sulfate (with acidified barium nitrate); and the gases ammonia, carbon dioxide, chlorine, hydrogen, oxygen "
            "and sulfur dioxide; deduce the identity of unknown substances from observations (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Qualitative Analysis", "Qualitative analysis",
            "Free Secondary 3 O-Level Chemistry worksheets on qualitative analysis: tests for cations with sodium hydroxide and ammonia, tests for anions and gases, and "
            "identifying unknown salts. 100 questions with answers.",
            "Use NaOH and NH₃ to identify cations.", "Al³⁺ and Zn²⁺: tell them apart with excess NH₃.",
            "<p><b>Each ion gives a characteristic result with a reagent.</b></p><ul>"
            "<li>NaOH: Al³⁺, Zn²⁺ white, soluble in excess; Ca²⁺ white, insoluble; Cu²⁺ light blue; Fe²⁺ green; Fe³⁺ red-brown; NH₄⁺ gives ammonia on warming.</li>"
            "<li>NH₃(aq): Zn²⁺ white, dissolves in excess; Al³⁺ white, does not; Cu²⁺ light blue, dissolves to a dark blue solution; Ca²⁺ no precipitate.</li>"
            "<li>Anions: CO₃²⁻ fizzes with acid (CO₂); Cl⁻ white and I⁻ yellow with acidified AgNO₃; SO₄²⁻ white with acidified Ba(NO₃)₂; NO₃⁻ gives NH₃ with NaOH and Al.</li>"
            "<li>Gases: H₂ pops, O₂ relights a glowing splint, CO₂ turns limewater milky, NH₃ turns red litmus blue, Cl₂ bleaches litmus, SO₂ decolourises acidified KMnO₄.</li></ul>",
            [("White precipitate with NaOH, dissolves in excess; with excess NH₃ it stays. Cation?", ["Al³⁺ or Zn²⁺ from NaOH", "Zn²⁺ would dissolve in NH₃"], "Al³⁺"),
             ("Acidified Ba(NO₃)₂ gives a white precipitate. Anion?", [], "sulfate")],
            ["Mixing up Al³⁺ and Zn²⁺: only Zn(OH)₂ dissolves in excess aqueous ammonia.", "Writing a red-brown precipitate for Fe²⁺ (it is green; Fe³⁺ is red-brown).",
             "Acidifying with hydrochloric acid before the chloride test.", "Saying carbon dioxide relights a glowing splint (that is oxygen)."],
            [("How do you tell aluminium ions from zinc ions?", "Both give white precipitates that dissolve in excess sodium hydroxide. With excess aqueous ammonia, only the zinc precipitate dissolves."),
             ("How do you test for chloride and sulfate ions?", "Acidify with dilute nitric acid. Add aqueous silver nitrate: a white precipitate shows chloride. Add aqueous barium nitrate: a white precipitate shows sulfate."),
             ("What are the tests for common gases?", "Hydrogen pops with a lighted splint, oxygen relights a glowing splint, carbon dioxide turns limewater milky, ammonia turns damp red litmus blue, chlorine bleaches damp litmus and sulfur dioxide decolourises acidified potassium manganate(VII).")],
            sets)


if __name__ == "__main__":
    main()
