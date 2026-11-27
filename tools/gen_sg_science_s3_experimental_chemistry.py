# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Chemistry (6092), Topic 1: Experimental Chemistry
  python tools/gen_sg_science_s3_experimental_chemistry.py
Choosing apparatus to measure time, temperature, mass and volume (burette, pipette, measuring cylinder, gas syringe); methods
of collecting gases (by solubility and density) and drying them; separation and purification (filtration, crystallisation,
evaporation, simple and fractional distillation, separating funnel, paper chromatography and Rf values); using melting and
boiling points to judge purity.
UK and SG chromatography and separation makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "a measuring cylinder is the most accurate for 25.0 cm³", "collect ammonia over water",
"evaporate to dryness to get crystals of copper(II) sulfate", "an impure substance melts at a sharp, higher temperature",
"Rf = distance moved by solvent ÷ distance moved by spot".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Chemistry", 13
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_chrom = src("gen_uk_science_y11_chemical_analysis", "g_chrom")
uk_rf = src("gen_uk_science_y11_chemical_analysis", "g_rf")
uk_mp = src("gen_uk_science_y11_chemical_analysis", "g_mp")
sg_meth = src("gen_sg_science_s1_separation_techniques", "g_meth")
sg_prin = src("gen_sg_science_s1_separation_techniques", "g_prin")

APP = [("exactly 25.0 cm³ of an alkali to put in a conical flask", "a pipette"), ("the volume of acid added drop by drop in a titration", "a burette"),
       ("about 50 cm³ of water to dissolve a solid", "a measuring cylinder"), ("the volume of gas given off every 10 s", "a gas syringe"),
       ("the mass of a sample of salt", "an electronic balance"), ("the time taken for a precipitate to form", "a stopwatch"),
       ("the temperature change in a neutralisation", "a thermometer"), ("about 200 cm³ of water to heat in a water bath", "a beaker")]
g_app = rows(R, APP, "Which apparatus is best for measuring %s?", extra=["a test tube", "a filter funnel"])

def g_bur():
    k = R.choice(["titre", "titre", "avg"])
    if k == "titre":
        a = R.randint(0, 40) * 5 / 100
        t = R.randint(360, 520) * 5 / 100
        b = a + t
        return tq("A burette reads %.2f cm³ before a titration and %.2f cm³ at the end point. What volume of acid was added?" % (a, b), "%.2f cm³" % t,
                  ["%.2f cm³" % (a + b), "%.2f cm³" % b, "%.2f cm³" % (50 - b)], "Titre = final reading − initial reading = %.2f − %.2f = %.2f cm³." % (b, a, t))
    base = R.randint(200, 260) * 10 / 100
    xs = [base, base + 0.05, base - 0.05, base + R.choice([0.8, 1.0, 1.2])]
    R.shuffle(xs)
    good = sorted(xs)[:3]
    m = sum(good) / 3
    return tq("Four titres are %s cm³. Using only the concordant results (within 0.10 cm³), what is the average titre?" % ", ".join("%.2f" % x for x in xs), "%.2f cm³" % m,
              ["%.2f cm³" % (sum(xs) / 4), "%.2f cm³" % max(xs), "%.2f cm³" % (m + 0.10)], "Ignore the rough titre %.2f cm³ and average the other three." % max(xs))


GAS = [("ammonia", "very soluble in water and less dense than air", "upward delivery (downward displacement of air)"),
       ("hydrogen chloride", "very soluble in water and denser than air", "downward delivery (upward displacement of air)"),
       ("carbon dioxide", "slightly soluble in water and denser than air", "downward delivery, or over water"),
       ("hydrogen", "insoluble in water and less dense than air", "over water (displacement of water)"),
       ("oxygen", "insoluble in water", "over water (displacement of water)"),
       ("sulfur dioxide", "soluble in water and denser than air", "downward delivery (upward displacement of air)"),
       ("chlorine", "soluble in water and denser than air", "downward delivery (upward displacement of air)")]


def g_gas():
    g, prop, meth = R.choice(GAS)
    k = R.choice(["meth", "why"])
    if k == "meth":
        others = sorted({m for _, _, m in GAS if m != meth} | {"in a gas syringe only, never in a test tube"})
        return tq("%s is %s. How is it best collected?" % (g[0].upper() + g[1:], prop), meth, R.sample(others, 3),
                  "Soluble gases cannot be collected over water. Gases denser than air: downward delivery; less dense: upward delivery.")
    return tq("Why is %s collected by %s?" % (g, meth), "because it is %s" % prop, ["because it is %s" % p for _, p, m in GAS if m != meth and p != prop][:3],
              "The method depends on solubility in water and density compared with air.")


DRY = [("ammonia", "calcium oxide (quicklime)"), ("chlorine", "concentrated sulfuric acid"), ("hydrogen chloride", "concentrated sulfuric acid"), ("sulfur dioxide", "concentrated sulfuric acid"),
       ("carbon dioxide", "concentrated sulfuric acid"), ("hydrogen", "concentrated sulfuric acid")]


def g_dry():
    g, d = R.choice(DRY)
    if g == "ammonia":
        return tq("Which drying agent is used for ammonia?", d, ["concentrated sulfuric acid", "fused calcium chloride", "water"],
                  "Ammonia is alkaline, so it reacts with concentrated sulfuric acid (and with calcium chloride); calcium oxide is used.")
    return tq("Which drying agent is commonly used for %s?" % g, d, ["calcium oxide (quicklime)", "sodium hydroxide solution", "water"],
              "Acidic or neutral gases are dried with concentrated sulfuric acid; calcium oxide would react with acidic gases.")


SEP = [("sand from a mixture of sand and water", "filtration"), ("salt from salt solution", "evaporation to dryness"),
       ("hydrated copper(II) sulfate crystals from its solution", "crystallisation"), ("pure water from seawater", "simple distillation"),
       ("ethanol from a mixture of ethanol and water", "fractional distillation"), ("oil from a mixture of oil and water", "a separating funnel"),
       ("the dyes in a sample of ink", "paper chromatography"), ("the fractions of crude oil", "fractional distillation"),
       ("chalk (calcium carbonate) from water", "filtration"), ("nitrogen and oxygen from liquid air", "fractional distillation")]
g_sep = rows(R, SEP, "Which method is best for separating %s?", "What can be separated by %s?", extra=["sublimation"])


def g_rf():
    s = R.choice([2.5, 3.0, 3.6, 4.0, 4.5, 4.8, 5.4, 6.0, 7.2, 8.0])
    f = R.choice([0.2, 0.25, 0.3, 0.4, 0.45, 0.5, 0.6, 0.75, 0.8])
    d = round(s * f, 2)
    sol = R.choice([8.0, 9.0, 10.0, 12.0])
    d2 = round(sol * f, 2)
    k = R.choice(["rf", "dist"])
    if k == "rf":
        return nq("In paper chromatography, a spot moves %s cm and the solvent front moves %s cm from the base line. What is the Rf value?" % (N(d2), N(sol)), f, [sol / d2, d2 * sol, 1 - f], "",
                  "Rf = distance moved by the spot ÷ distance moved by the solvent = %s ÷ %s = %s." % (N(d2), N(sol), N(f)))
    return nq("A dye has an Rf value of %s. The solvent front moves %s cm. How far does the dye move?" % (N(f), N(sol)), d2, [sol / f, sol - f, sol * (1 - f)], " cm",
              "Distance = Rf × solvent distance = %s × %s = %s cm." % (N(f), N(sol), N(d2)))


PUR = [("Pure water boils at 100 °C at sea level. A sample boils at 102 °C.", "It contains a dissolved impurity, which raises the boiling point."),
       ("Pure ice melts at 0 °C. A sample of salty ice melts at −3 °C.", "It contains an impurity, which lowers the melting point."),
       ("A white solid melts sharply at 122 °C, the same as pure benzoic acid.", "It is probably pure benzoic acid."),
       ("A white solid melts over a range from 115 °C to 119 °C.", "It is impure: impurities lower the melting point and make it melt over a range."),
       ("A chromatogram of a food colouring shows one spot.", "It may be a pure dye (one substance in that solvent)."),
       ("A chromatogram of a food colouring shows three spots.", "It is a mixture of at least three dyes.")]
g_pur = rows(R, PUR, "%s What can you conclude?")

POOL1 = pool(R, [
    ("Why is a pipette used instead of a measuring cylinder to measure 25.0 cm³ of solution in a titration?", "A pipette measures a fixed volume much more accurately.", ["A pipette holds more liquid.", "A measuring cylinder cannot measure 25 cm³.", "A pipette is easier to clean."], "Burettes and pipettes are precise to about 0.05–0.1 cm³."),
    ("How should you read the volume in a burette?", "at eye level, from the bottom of the meniscus", ["from the top of the meniscus", "from above, looking down", "only after the burette is empty"], "This avoids parallax error."),
    ("Why must a gas be collected only after the air in the apparatus has been pushed out?", "Otherwise the first gas collected is mostly air.", ["The gas is too hot at first.", "The first gas is always poisonous.", "The water must warm up."], "Let the first bubbles escape."),
    ("Why is a gas syringe used to measure the volume of a gas?", "It measures the volume of gas given off directly and accurately.", ["It dries the gas.", "It makes the gas react faster.", "It changes the gas into a liquid."], "Readings can be taken at time intervals."),
    ("What is the residue in filtration?", "the solid that stays on the filter paper", ["the liquid that passes through", "the dissolved solute", "the steam given off"], "The liquid that passes through is the filtrate."),
    ("Why is a solution heated only until it is saturated, and then cooled, to make crystals of copper(II) sulfate?", "Heating to dryness would drive off the water of crystallisation and decompose the crystals.",
     ["Crystals only form when boiling.", "Cooling makes the solution more concentrated.", "It is quicker than evaporating."], "Crystals form as the saturated solution cools."),
    ("In fractional distillation of ethanol and water, which liquid distils first?", "ethanol, because it has the lower boiling point (78 °C)", ["water, because it boils at 100 °C", "both together", "neither: they react"], "The fractionating column separates liquids with close boiling points."),
    ("Why is the base line in paper chromatography drawn in pencil, not ink?", "Pencil does not dissolve in the solvent, so it will not run up the paper.", ["Pencil lines are darker.", "Ink is too expensive.", "Pencil makes the spots move faster."], "Ink would separate like the sample."),
    ("Why must the base line be above the solvent level in chromatography?", "Otherwise the spots would dissolve into the solvent in the beaker.", ["So the paper stays dry.", "So the spots move faster.", "So the solvent evaporates."], "The solvent must carry the spots up the paper."),
    ("Colourless amino acids are separated by chromatography. How are their spots seen?", "by spraying a locating agent (such as ninhydrin) and drying the paper", ["by looking at the paper in the dark", "by heating the paper until it burns", "they cannot be seen"], "The locating agent turns the spots coloured."),
])
POOL5 = pool(R, [
    ("A student needs pure dry sodium chloride from rock salt (salt with sand). Which order of steps is correct?", "dissolve in water, filter, evaporate the filtrate", ["filter, dissolve, evaporate", "evaporate, dissolve, filter", "distil, filter, dissolve"], "Salt dissolves; sand does not."),
    ("Why does the thermometer bulb sit beside the side arm of the flask in distillation?", "to measure the boiling point of the vapour that is distilling over", ["to measure the temperature of the liquid in the flask", "to stop the vapour escaping", "to heat the vapour"], "The reading identifies the substance distilling."),
    ("Why does cold water enter the condenser at the bottom?", "so the condenser fills completely with water and cools the vapour efficiently", ["so the water flows faster", "so the vapour is heated", "so less water is used"], "Counter-current cooling."),
    ("Which is the best way to obtain pure water from a solution of ink?", "simple distillation", ["filtration", "chromatography", "crystallisation"], "Water boils off and is condensed; the dyes are left behind."),
    ("Two dyes have the same Rf value in the same solvent. What does this suggest?", "They may be the same substance.", ["They are definitely different.", "The paper is faulty.", "The solvent has evaporated."], "Compare with known substances."),
    ("Why is chromatography used in forensic science?", "to compare inks or dyes found at a crime scene with known samples", ["to measure the mass of evidence", "to find fingerprints by heating", "to dry samples"], "Matching spots suggest the same ink."),
    ("A solid is soluble in hot water but much less soluble in cold water. How can it be purified?", "by recrystallisation: dissolve it in hot water, filter while hot, then cool to form crystals", ["by simple distillation of the solid", "by burning off impurities", "by filtration of the cold mixture only"], "Impurities stay in solution."),
    ("How can a mixture of iodine and sand be separated?", "by heating: iodine sublimes and collects as a solid on a cold surface", ["by filtration", "by dissolving in water", "by chromatography"], "Sublimation: solid directly to gas."),
    ("Why must a liquid in a separating funnel be immiscible for the method to work?", "Immiscible liquids form separate layers, so the lower layer can be run off.", ["Miscible liquids react.", "Immiscible liquids are heavier.", "The tap only opens for oils."], "Oil and water are immiscible."),
    ("Why does a mixture have no fixed melting or boiling point?", "It contains different substances in variable proportions.", ["Mixtures cannot be heated.", "Mixtures are always gases.", "It is always pure."], "Pure substances have fixed melting and boiling points."),
])


def main():
    sets = U.sets([
        ("Measuring apparatus", [(g_app, 7), (g_bur, 6), POOL1]),
        ("Collecting and drying gases", [(g_gas, 10), (g_dry, 5), POOL1]),
        ("Separation methods", [(g_sep, 10), (sg_meth, 5), (sg_prin, 3), POOL1]),
        ("Chromatography and purity", [(g_rf, 6), (uk_chrom, 4), (uk_rf, 2), (g_pur, 5), (uk_mp, 3)]),
        ("Exam-style questions", [(POOL5, 10), (g_bur, 3), (g_gas, 2), (g_sep, 2), (g_rf, 2), (uk_chrom, 1)]),
    ])
    make_ol(LV, SUBJ, "experimental-chemistry", SORT, "Experimental Chemistry",
            "Name appropriate apparatus for measuring time, temperature, mass and volume, including burettes, pipettes, measuring cylinders and gas syringes; suggest "
            "methods of collecting gases based on their solubility and density and of drying them; describe methods of separation and purification (filtration, "
            "crystallisation, evaporation, simple and fractional distillation, use of a separating funnel, paper chromatography) and interpret chromatograms using Rf "
            "values and locating agents; deduce the purity of a substance from its melting or boiling point (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Experimental Chemistry", "Experimental chemistry",
            "Free Secondary 3 O-Level Chemistry worksheets on experimental chemistry: measuring apparatus, collecting and drying gases, separation methods, chromatography, Rf "
            "values and purity. 100 questions with answers.",
            "Choose the method by the properties.", "Rf = distance moved by spot ÷ distance moved by solvent.",
            "<p><b>Choose apparatus and methods to suit the substances.</b></p><ul>"
            "<li>Accurate volumes: pipette (fixed volume) and burette (variable). Gas volume: gas syringe.</li>"
            "<li>Gases: insoluble ones over water; soluble ones by downward delivery (denser than air) or upward delivery (less dense). Dry ammonia with calcium oxide, most other gases with concentrated sulfuric acid.</li>"
            "<li>Separation: filtration (insoluble solid), crystallisation, evaporation, distillation, fractional distillation, separating funnel, paper chromatography.</li>"
            "<li>A pure substance has a sharp, fixed melting point. Impurities lower the melting point (over a range) and raise the boiling point.</li></ul>",
            [("Spot 4.2 cm, solvent 7.0 cm. Rf?", ["4.2 ÷ 7.0"], "0.60"),
             ("How do you collect dry ammonia?", ["dry with calcium oxide", "less dense than air, very soluble"], "upward delivery")],
            ["Using a measuring cylinder when an accurate volume is needed.", "Collecting very soluble gases such as ammonia over water.",
             "Heating copper(II) sulfate solution to dryness instead of crystallising it.", "Dividing the solvent distance by the spot distance for Rf."],
            [("How do you choose a method to collect a gas?", "If it is insoluble in water, collect it over water. If it is soluble, use downward delivery if it is denser than air or upward delivery if it is less dense."),
             ("How do you calculate an Rf value?", "Divide the distance moved by the spot by the distance moved by the solvent front, both measured from the base line. Rf is always less than 1."),
             ("How can you tell if a substance is pure?", "A pure substance melts and boils at fixed temperatures. Impurities lower the melting point and make it melt over a range of temperatures.")],
            sets)


if __name__ == "__main__":
    main()
