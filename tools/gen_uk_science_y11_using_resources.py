# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Chemistry): Using Resources
  python tools/gen_uk_science_y11_using_resources.py
Natural, synthetic, finite and renewable resources, sustainable development, potable water (sterilising and
desalination), waste water treatment, alternative methods of extracting metals (phytomining and bioleaching, higher
tier), life cycle assessment, and reducing the use of resources by reusing and recycling.
Wrong answers come from real mistakes: "potable water is pure water", "filtering kills microbes", "recycling uses no
energy", "a life cycle assessment only looks at disposal".
"""
from uk_sci import item, bank, once, table
from uk_ks4 import U4, build

U, R, P, us = U4(62109)
SH, NR = "ess_sustainability_and_human_impact", "ess_natural_resources_and_hazards"
us_fish, us_sol = us(SH, "g_fish"), us(SH, "g_sol", drop=("plowing", "salmon"))
us_res = us(NR, "g_res")

RES = [("crude oil", "finite"), ("coal", "finite"), ("natural gas", "finite"), ("iron ore", "finite"), ("limestone", "finite"), ("copper ore", "finite"),
       ("timber from managed forests", "renewable"), ("cotton", "renewable"), ("wool", "renewable"), ("sugar cane", "renewable"), ("rapeseed oil", "renewable")]
NAT = [("wool", "natural"), ("cotton", "natural"), ("rubber from trees", "natural"), ("timber", "natural"), ("nylon", "synthetic"), ("polyester", "synthetic"),
       ("poly(ethene)", "synthetic"), ("synthetic rubber", "synthetic")]


def g_res():
    if R.random() < 0.55:
        r, a = R.choice(RES)
        if not once(("rs", r)):
            return None
        return item("Is %s a finite or a renewable resource?" % r, a, [x for x in ["finite", "renewable", "neither", "both"] if x != a],
                    "Finite resources will run out; renewable ones can be replaced as fast as we use them.")
    r, a = R.choice(NAT)
    if not once(("na", r)):
        return None
    return item("Is %s a natural or a synthetic material?" % r, a, [x for x in ["natural", "synthetic", "an element", "a fuel"] if x != a],
                "Synthetic materials are made by chemists, often from crude oil.")


POT = [("Why is fresh water passed through filter beds?", "to remove solid particles", ["to kill microbes", "to remove dissolved salts", "to add fluoride"]),
       ("Why is chlorine added to drinking water?", "to kill microbes (sterilise it)", ["to remove solids", "to remove salt", "to make it taste sweet"]),
       ("Which of these can sterilise water?", "ultraviolet light", ["sand filters", "a sieve", "sedimentation"]),
       ("Which of these can sterilise water?", "ozone", ["a sieve", "sand filters", "sedimentation"]),
       ("What is desalination?", "removing salt from sea water", ["adding chlorine", "removing solids with a filter", "heating water to kill microbes"]),
       ("Name a method of desalination.", "reverse osmosis using membranes", ["sedimentation", "chlorination", "screening"]),
       ("Name a method of desalination.", "distillation", ["filtering through sand", "adding chlorine", "screening"]),
       ("Why is desalination not used much in the UK?", "It needs large amounts of energy, and the UK has plenty of fresh water.", ["It does not work.", "Sea water is already potable.", "It makes the water salty."]),
       ("What is the main source of fresh water in the UK?", "rain that collects in rivers, lakes, reservoirs and underground rocks", ["sea water", "melted glaciers only", "bottled water"]),
       ("What is potable water?", "water that is safe to drink", ["pure water with nothing dissolved", "distilled water only", "sea water"]),
       ("Is potable water pure in the chemical sense?", "No. It contains dissolved substances, but in safe amounts.", ["Yes, always.", "Only if it is boiled.", "Only bottled water is potable."]),
       ("Which water source in the UK is often in underground rocks?", "ground water in aquifers", ["sea water", "waste water", "sewage"])]


def g_pot():
    q, a, w = R.choice(POT)
    if not once(("pt", q, a)):
        return None
    return item(q, a, w, "Potable water: choose a source, filter, sterilise (chlorine, ozone or UV).")


WW = ["screening and grit removal", "sedimentation to make sludge and effluent", "anaerobic digestion of the sludge", "aerobic biological treatment of the effluent"]
WQ = [("What does screening remove from sewage?", "large objects and grit", ["microbes", "dissolved salts", "organic matter in solution"]),
      ("What happens in sedimentation?", "Heavier solids sink to form sludge; the liquid above is effluent.", ["Microbes are killed with UV.", "Water is distilled.", "Chlorine is added."]),
      ("What is made by the anaerobic digestion of sludge?", "biogas (methane), which can be used as a fuel", ["oxygen", "drinking water", "salt"]),
      ("How is effluent treated?", "Air is bubbled through it so aerobic bacteria break down organic matter.", ["It is boiled.", "It is filtered through sand only.", "It is frozen."]),
      ("Why is sewage treated before it is released into rivers?", "to remove organic matter and harmful microbes", ["to add salt", "to make it potable", "to remove oxygen"]),
      ("Why does industrial waste water need more treatment?", "It may contain harmful chemicals.", ["It has no microbes.", "It is already pure.", "It is salty."])]


def g_ww():
    if R.random() < 0.45:
        i = R.randrange(3)
        if not once(("wo", i)):
            return None
        return item("In waste water treatment, which stage comes straight after %s?" % WW[i], WW[i + 1], [x for x in WW if x not in (WW[i], WW[i + 1])] + ["sterilising with chlorine"],
                    "Screening → sedimentation → sludge digested anaerobically, effluent treated aerobically.")
    q, a, w = R.choice(WQ)
    if not once(("wq", q)):
        return None
    return item(q, a, w, "Waste water is treated to remove organic matter and harmful microbes.")


LCA = ["extracting and processing raw materials", "manufacturing and packaging", "use during its lifetime", "disposal at the end of its life"]
PROD = [("plastic bag", "paper bag", (2, 6), (8, 16), (20, 40), (50, 90)), ("glass bottle", "plastic bottle", (14, 30), (5, 12), (150, 300), (60, 140)),
        ("cotton bag", "plastic bag", (40, 80), (2, 6), (300, 600), (20, 40)), ("china mug", "paper cup", (12, 20), (1, 4), (90, 160), (10, 30))]


def g_lca():
    if R.random() < 0.3:
        i = R.randrange(4)
        k = R.choice(["after", "first"]) if i == 0 else "after"
        if k == "first":
            if not once(("lf",)):
                return None
            return item("What is the first stage of a life cycle assessment?", LCA[0], LCA[1:], "Raw materials → manufacture → use → disposal.")
        if i == 3 or not once(("la", i)):
            return None
        return item("In a life cycle assessment, which stage comes straight after %s?" % LCA[i], LCA[i + 1], [x for x in LCA if x not in (LCA[i], LCA[i + 1])] + ["advertising the product"],
                    "Raw materials → manufacture → use → disposal.")
    a, b, ra, rb, qa, qb = R.choice(PROD)
    ea, eb = R.randint(*ra), R.randint(*rb)
    ca, cb = R.randint(*qa), R.randint(*qb)
    k = R.choice(["energy", "co2", "diff"])
    if not once(("lt", a, ea, eb, ca, cb, k)):
        return None
    tab = table(["", a, b], [["Energy used (MJ)", str(ea), str(eb)], ["Carbon dioxide released (g)", str(ca), str(cb)]])
    if k == "energy":
        x = a if ea < eb else b
        return item(tab + "This is part of a life cycle assessment (to make one of each) for a %s and a %s. Which uses less energy?" % (a, b), "the " + x,
                    ["the " + (b if x == a else a), "They use the same.", "You cannot tell from the data."], "Compare the energy row.")
    if k == "co2":
        x = a if ca < cb else b
        return item(tab + "This is part of a life cycle assessment (to make one of each) for a %s and a %s. Which releases less carbon dioxide?" % (a, b), "the " + x,
                    ["the " + (b if x == a else a), "They release the same.", "You cannot tell from the data."], "Compare the carbon dioxide row.")
    d = abs(ca - cb)
    return item(tab + "This is part of a life cycle assessment (to make one of each) for a %s and a %s. How much more carbon dioxide does one release than the other?" % (a, b), "%d g" % d,
                ["%d g" % (ca + cb), "%d g" % abs(ea - eb), "%d g" % max(ca, cb)] if len({d, ca + cb, abs(ea - eb), max(ca, cb)}) == 4 else ["%d g" % (ca + cb), "%d g" % max(ca, cb), "%d g" % (d + 10)],
                "%d − %d = %d g." % (max(ca, cb), min(ca, cb), d))


MET = [("aluminium", 95), ("copper", 85), ("steel", 70), ("paper", 40), ("glass", 30), ("plastic", 70)]


def g_rec():
    m, pc = R.choice(MET)
    e = R.choice([100, 120, 150, 200, 250, 300, 400, 500, 600, 800])
    k = R.choice(["use", "save"])
    if (e * pc) % 100 or not once(("rc", m, e, k)):
        return None
    sv = e * pc // 100
    if k == "save":
        return item("Making new %s from raw materials uses %d MJ. Recycling saves about %d%% of this energy. How much energy is saved?" % (m, e, pc), "%d MJ" % sv,
                    [x for x in ["%d MJ" % (e - sv), "%d MJ" % e, "%d MJ" % pc, "%d MJ" % (e + sv)] if x != "%d MJ" % sv][:3], "%d%% of %d = %d MJ." % (pc, e, sv))
    return item("Making new %s from raw materials uses %d MJ. Recycling saves about %d%% of this energy. How much energy does recycling use?" % (m, e, pc), "%d MJ" % (e - sv),
                [x for x in ["%d MJ" % sv, "%d MJ" % e, "%d MJ" % pc, "%d MJ" % (e + sv)] if x != "%d MJ" % (e - sv)][:3], "%d − %d = %d MJ." % (e, sv, e - sv))


B1 = bank([
    ("What is sustainable development?", "development that meets the needs of people today without stopping future generations meeting their own needs", ["using resources as fast as possible", "only using finite resources", "never using any resources"], "Chemists develop sustainable processes."),
    ("How do humans use Earth's resources?", "for warmth, shelter, food and transport", ["only for food", "only for fuel", "only for building"], "Natural resources are supplemented by agriculture and synthetic products."),
    ("Why is it important to use finite resources carefully?", "They will run out.", ["They grow back quickly.", "They are always cheap.", "They are renewable."], "For example, crude oil and metal ores."),
])
B2 = bank([
    ("What are the main steps to make UK fresh water potable?", "choose a source, filter it, then sterilise it", ["boil, freeze, then melt it", "add salt, then filter it", "distil it only"], "Sterilising agents: chlorine, ozone, ultraviolet light."),
    ("How could you test whether a water sample contains dissolved solids?", "Evaporate it and look for a solid residue.", ["Filter it.", "Smell it.", "Shake it."], "Also measure the pH."),
])
B3 = bank([
    ("Why is waste water treatment important?", "It stops harmful microbes and organic matter polluting rivers and the sea.", ["It makes sea water.", "It removes all salt.", "It adds nutrients for fish."], "Sewage and agricultural waste water."),
])
B4 = bank([
    ("Why is a life cycle assessment sometimes biased?", "Some values, such as pollution effects, are hard to measure and can be chosen selectively.", ["It uses no numbers.", "It is always perfect.", "It ignores energy."], "Selective LCAs can support advertising claims."),
    ("What is phytomining?", "growing plants on soil with metal compounds, then burning them to collect the metal from the ash", ["mining with explosives", "using bacteria in a solution", "melting rocks"], "Higher tier."),
    ("What is bioleaching?", "using bacteria to produce solutions (leachates) that contain metal compounds", ["burning plants", "electrolysis of ore", "melting scrap metal"], "Higher tier."),
])
B5 = bank([
    ("Why is reusing a glass bottle better than recycling it?", "Reusing only needs washing and sterilising; recycling needs crushing and melting.", ["Reusing needs more energy.", "Recycling uses no energy.", "Glass cannot be recycled."], "Less energy and fewer resources."),
    ("Why do we recycle metals?", "to save energy and finite ores, and reduce waste", ["because metals are renewable", "to make the metal weaker", "because mining uses no energy"], "Metals can be melted and recast."),
    ("Why is low-grade copper ore becoming more important?", "High-grade ores are running out.", ["It is richer in copper.", "It is renewable.", "It needs no processing."], "Phytomining and bioleaching use low-grade ores."),
    ("Which of these reduces the use of resources?", "reusing carrier bags", ["throwing away cans", "buying single-use bottles", "burning paper waste"], "Reduce, reuse, recycle."),
])

if __name__ == "__main__":
  build(U, 11, "using-resources", 9, "Chemistry", "Using resources",
      "Using the Earth's resources and sustainable development; potable water; waste water treatment; alternative methods of extracting metals (higher tier); life cycle assessment; ways of reducing the use of resources, including reuse and recycling.",
      "Using Resources", "Using Resources",
      "Free Year 11 GCSE Combined Science worksheets on using resources: finite and renewable resources, potable water, desalination, waste water treatment, life cycle assessment and recycling. 100 questions with answers.",
      "Potable water is safe to drink, not pure.",
      "Reduce, reuse, recycle saves energy and resources.",
      "<p><b>Chemists help us use Earth's resources sustainably.</b></p><ul><li>Potable water: filter to remove solids, then sterilise with chlorine, ozone or UV. Desalination removes salt from sea water.</li>"
      "<li>Waste water: screening, sedimentation, then sludge is digested anaerobically and effluent is treated aerobically.</li>"
      "<li>A life cycle assessment looks at raw materials, manufacture, use and disposal.</li></ul>",
      [("Recycling saves 95% of 200 MJ. Energy saved?", ["0.95 × 200"], "190 MJ"), ("What kills microbes in water?", ["Sterilising"], "chlorine, ozone or UV")],
      ["Thinking potable water is pure.", "Thinking filtering kills microbes.", "Thinking a life cycle assessment only looks at disposal."],
      [("How is drinking water made in the UK?", "Fresh water from rivers, reservoirs or ground water is filtered to remove solids and sterilised with chlorine, ozone or ultraviolet light."),
       ("What are the stages of a life cycle assessment?", "Extracting and processing raw materials, manufacturing and packaging, use during its lifetime, and disposal."),
       ("Why is recycling useful?", "It saves energy and finite resources and reduces waste and pollution.")],
      [("Resources", B1 + [(g_res, 14), (us_res, 3)]),
       ("Potable water", B2 + [(g_pot, 10), (g_res, 2), (g_rec, 6)]),
       ("Waste water", B3 + [(g_ww, 7), (g_lca, 8), (us_sol, 4)]),
       ("Life cycle assessment", B4 + [(g_lca, 14), (us_fish, 3)]),
       ("Reduce, reuse, recycle", B5 + [(g_rec, 14), (us_fish, 2)])])
