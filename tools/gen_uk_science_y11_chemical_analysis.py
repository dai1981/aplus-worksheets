# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Chemistry): Chemical Analysis
  python tools/gen_uk_science_y11_chemical_analysis.py
Pure substances and melting points, formulations, paper chromatography (reading chromatograms, Rf values, mobile and
stationary phases) and the tests for hydrogen, oxygen, carbon dioxide and chlorine. Chromatograms are drawn as SVG.
Wrong answers come from real mistakes: "pure means natural", "Rf = solvent distance ÷ spot distance", "a mixture
melts at one sharp temperature", "carbon dioxide relights a glowing splint".
"""
from uk_sci import item, bank, once, table
from uk_ks4 import U4, build
from ws_common import svg_wrap, text, line

U, R, P, us = U4(62107)
COLS = ["#d33", "#2a6fd6", "#2a9d4b", "#e0a400", "#8a3fc8"]


def chrom(lanes, front=0.9):
    """lanes: [(label, [rf, ...])]. Returns an SVG chromatogram."""
    w = 70 + 70 * len(lanes)
    h, base, top = 300, 260, 260 - 220 * front
    b = "<rect x='20' y='20' width='%d' height='260' fill='#fffdf5' stroke='#555' stroke-width='2'/>" % (w - 40)
    b += line(20, base, w - 20, base, "#555", 2, " stroke-dasharray='6 4'") + line(20, top, w - 20, top, "#2a6fd6", 2, " stroke-dasharray='3 3'")
    b += text(w - 22, base - 6, "start line", 12, "end", "#555", weight=400) + text(w - 22, top - 6, "solvent front", 12, "end", "#2a6fd6", weight=400)
    for i, (lab, rfs) in enumerate(lanes):
        x = 70 + 70 * i
        for rf in rfs:
            y = base - (base - top) * rf
            b += "<circle cx='%d' cy='%.1f' r='8' fill='%s' opacity='0.85'/>" % (x, y, COLS[[0.2, 0.35, 0.5, 0.65, 0.8].index(rf) if rf in (0.2, 0.35, 0.5, 0.65, 0.8) else 0])
        b += text(x, 296, lab, 15)
    return "<svg data-pf='lg'" + svg_wrap(w, h + 4, b, "paper chromatogram")[4:]


def g_rf():
    s = R.choice([3.0, 4.0, 4.5, 5.0, 6.0, 7.5, 8.0, 9.0, 10.0, 12.0])
    d = R.choice([x / 10 for x in range(5, int(s * 10), 5)])
    rf = d / s
    if abs(round(rf, 2) - rf) > 1e-9 or not once(("rf", s, d)):
        return None
    k = R.choice(["rf", "rf", "dist"])
    if k == "rf":
        return item("A spot moved %g cm. The solvent moved %g cm from the start line. What is the Rf value?" % (d, s), "%g" % round(rf, 2),
                    [x for x in ["%g" % round(s / d, 2), "%g" % round(s - d, 2), "%g" % round(d * s, 2), "%g" % round(1 - rf, 2)] if x != "%g" % round(rf, 2)][:3],
                    "Rf = distance moved by spot ÷ distance moved by solvent = %g ÷ %g." % (d, s))
    return item("A dye has an Rf value of %g. The solvent moved %g cm. How far did the dye move?" % (round(rf, 2), s), "%g cm" % d,
                [x for x in ["%g cm" % round(s / rf, 2), "%g cm" % round(s - d, 2), "%g cm" % round(rf, 2)] if x != "%g cm" % d][:3] + ["%g cm" % s],
                "Distance = Rf × solvent distance = %g × %g." % (round(rf, 2), s))


SAMP = ["a black felt-tip pen", "a green food colouring", "a brown sweet coating", "a purple ink", "an orange drink"]


def g_chrom():
    sm = R.choice(SAMP)
    pool = [0.2, 0.35, 0.5, 0.65, 0.8]
    inks = {k: sorted(R.sample(pool, R.choice([1, 2]))) for k in "ABC"}
    if len({tuple(v) for v in inks.values()}) < 3:
        return None
    k = R.choice(["which", "count", "pure"])
    if k == "which":
        x = sorted(set(inks["A"]) | set(inks[R.choice("BC")])) if R.random() < 0.5 else list(inks[R.choice("ABC")])
        ins = [n for n in "ABC" if set(inks[n]) <= set(x)]
        if not ins or not once(("cw", sm, tuple(tuple(inks[c]) for c in "ABC"), tuple(x))):
            return None
        a = " and ".join(ins)
        if len(set(x) - set().union(*[inks[n] for n in ins])):
            return None
        svg = chrom([(n, inks[n]) for n in "ABC"] + [("X", x)])
        opts = ["A only", "B only", "C only", "A and B", "A and C", "B and C"]
        opts = [o.replace(" only", "") for o in opts]
        lab = {"A": "A only", "B": "B only", "C": "C only"}.get(a, a)
        allo = ["A only", "B only", "C only", "A and B", "A and C", "B and C"]
        return item(svg + "X is %s. It was compared with inks A, B and C. Which inks are in X?" % sm, lab, R.sample([o for o in allo if o != lab], 3), "Spots at the same height are the same dye.")
    n = R.choice("ABC")
    if not once(("cc", sm, n, k)):
        return None
    svg = chrom([(m, inks[m]) for m in "ABC"])
    nm = "sample %s (from %s)" % (n, sm)
    if k == "count":
        c = len(inks[n])
        return item(svg + "How many dyes are in %s?" % nm, str(c), [str(x) for x in [1, 2, 3, 4] if x != c][:3], "Count the spots in the lane.")
    pure = len(inks[n]) == 1
    return item(svg + "Is %s a pure substance or a mixture?" % nm, "a pure substance" if pure else "a mixture",
                ["a mixture" if pure else "a pure substance", "an element", "you cannot tell"], "One spot (in all solvents) means pure; more than one means a mixture.")


MP = [("aspirin", 136), ("benzoic acid", 122), ("stearic acid", 69), ("naphthalene", 80), ("salicylic acid", 159), ("paracetamol", 169)]


def g_mp():
    sub, t = R.choice(MP)
    k = R.choice(["sharp", "range", "low"])
    if not once(("mp", sub, k)):
        return None
    if k == "sharp":
        q, a = "melts at exactly %d °C" % t, "pure"
    elif k == "range":
        q, a = "melts gradually from %d °C to %d °C" % (t - 6, t - 2), "impure (a mixture)"
    else:
        q, a = "melts at %d °C over a range of 3 °C" % (t - 5), "impure (a mixture)"
    return item("Pure %s melts at %d °C. A sample of %s %s. Is the sample pure?" % (sub, t, sub, q), a,
                [x for x in ["pure", "impure (a mixture)", "a compound that cannot melt", "an element"] if x != a][:3],
                "Pure substances melt at one fixed temperature. Impurities lower the melting point and make it melt over a range.")


GAS = [("hydrogen", "A lit splint gives a squeaky pop."), ("oxygen", "It relights a glowing splint."),
       ("carbon dioxide", "Limewater turns milky (cloudy)."), ("chlorine", "Damp litmus paper is bleached white.")]


USE = {"hydrogen": "a lit splint", "oxygen": "a glowing splint", "carbon dioxide": "limewater", "chlorine": "damp litmus paper"}


def g_gas():
    g, t = R.choice(GAS)
    k = R.choice(["test", "gas", "use"])
    if not once(("gs", g, k)):
        return None
    if k == "use":
        return item("What do you use to test for %s?" % g, USE[g], [v for kk, v in USE.items() if kk != g], "Each gas has its own test.")
    if k == "test":
        return item("What is the result of the test for %s?" % g, t, [x[1] for x in GAS if x[0] != g], "Learn the four gas tests.")
    return item("A gas is tested. Result: %s Which gas is it?" % t.lower().rstrip(".") + ".", g, [x[0] for x in GAS if x[0] != g], "Learn the four gas tests.")


DYES = ["E102", "E110", "E124", "E129", "E133", "E151"]


def g_dye():
    rfs = sorted(R.sample([0.15, 0.25, 0.3, 0.4, 0.45, 0.55, 0.6, 0.7, 0.75, 0.85], 4))
    ds = R.sample(DYES, 4)
    i = R.randrange(4)
    s = R.choice([4.0, 6.0, 8.0, 10.0, 12.0])
    d = round(rfs[i] * s, 2)
    if not once(("dy", tuple(rfs), tuple(ds), i, s)):
        return None
    tab = table(["Dye", "Rf value"], [[ds[j], "%g" % rfs[j]] for j in range(4)])
    return item(tab + "A spot moved %g cm and the solvent moved %g cm. Which dye is it?" % (d, s), ds[i], [ds[j] for j in range(4) if j != i],
                "Rf = %g ÷ %g = %g." % (d, s, rfs[i]))


B1 = bank([
    ("What does 'pure' mean in chemistry?", "a single element or compound, not mixed with anything else", ["natural, with nothing added", "clean and safe to eat", "made in a factory"], "In everyday language pure can mean natural."),
    ("What is a formulation?", "a mixture designed as a useful product, with each part in a measured amount", ["a pure element", "a chemical equation", "a waste product"], "Paints, medicines, fuels, cleaning agents, alloys, fertilisers."),
    ("Which of these is a formulation?", "paint", ["oxygen", "pure water", "copper"], "A mixture made to a recipe."),
])
B2 = bank([
    ("In paper chromatography, what is the stationary phase?", "the paper", ["the solvent", "the ink", "the beaker"], "The solvent is the mobile phase."),
    ("Why is the start line drawn in pencil?", "Pencil does not dissolve in the solvent.", ["Pencil is darker.", "Ink would be too faint.", "Pencil moves with the solvent."], "Ink would run."),
    ("Why must the start line be above the solvent level?", "so the spots do not dissolve into the solvent in the beaker", ["so the paper stays dry", "to make the solvent move faster", "so the Rf is bigger"], "The dyes would wash away."),
])

if __name__ == "__main__":
  build(U, 11, "chemical-analysis", 7, "Chemistry", "Chemical analysis",
      "Purity, formulations and chromatography: pure substances and melting points, formulations, paper chromatography and Rf values; identification of common gases (hydrogen, oxygen, carbon dioxide, chlorine).",
      "Chemical Analysis", "Chemical Analysis",
      "Free Year 11 GCSE Combined Science worksheets on chemical analysis: pure substances, melting points, formulations, paper chromatography, Rf values and the tests for gases. 100 questions with answers.",
      "Rf = distance moved by spot ÷ distance moved by solvent.",
      "A pure substance melts at one fixed temperature.",
      "<p><b>Chemists test whether a substance is pure and what is in it.</b></p><ul><li>A pure substance melts and boils at fixed temperatures; a mixture melts over a range.</li>"
      "<li>Chromatography: Rf = spot distance ÷ solvent distance. Spots at the same height are the same dye.</li>"
      "<li>Gas tests: hydrogen pops, oxygen relights a glowing splint, carbon dioxide turns limewater milky, chlorine bleaches damp litmus.</li></ul>",
      [("Spot 3 cm, solvent 6 cm. Rf?", ["3 ÷ 6"], "0.5"), ("Glowing splint relights. Gas?", ["The oxygen test"], "oxygen")],
      ["Thinking 'pure' means 'natural'.", "Dividing the solvent distance by the spot distance.", "Mixing up the oxygen and hydrogen tests."],
      [("How do you calculate an Rf value?", "Divide the distance moved by the spot by the distance moved by the solvent, both measured from the start line. Rf is always less than 1."),
       ("How can you tell if a substance is pure?", "A pure substance melts at one exact temperature. An impure substance melts at a lower temperature over a range."),
       ("What are the four gas tests?", "Hydrogen: squeaky pop with a lit splint. Oxygen: relights a glowing splint. Carbon dioxide: limewater turns milky. Chlorine: bleaches damp litmus paper.")],
      [("Pure substances", B1 + [(g_mp, 13), (g_gas, 2), (g_chrom, 2)]),
       ("Chromatograms", B2 + [(g_chrom, 14), (g_dye, 3)]),
       ("Rf values", [(g_rf, 14), (g_dye, 6)]),
       ("Testing for gases", [(g_gas, 8), (g_dye, 6), (g_mp, 4), (g_rf, 2)]),
       ("Analysis problems", [(g_chrom, 6), (g_rf, 7), (g_dye, 7)])])
