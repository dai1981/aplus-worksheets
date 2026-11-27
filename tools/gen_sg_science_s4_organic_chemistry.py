# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Chemistry (6092), Topic 11: Organic Chemistry
  python tools/gen_sg_science_s4_organic_chemistry.py
Fuels and crude oil (fractional distillation, cracking), homologous series (alkanes, alkenes, alcohols, carboxylic acids, esters),
general formulae, structural isomerism, reactions (combustion, substitution, addition of bromine, hydrogen and steam, fermentation,
oxidation of ethanol, esterification), addition and condensation polymers, and the disposal of plastics.
UK KS4 organic makers are reused (Singapore names); series, ester, reaction and polymer makers are written here.
Wrong answers come from real mistakes: CnH2n for alkanes, naming an ester alcohol-last ("propyl ethanoate" for ethyl propanoate),
"alkanes decolourise bromine water", "addition polymers lose water", "the carboxylic acid with 2 C is methanoic acid".
"""
from sg_ol import OL, seed_of, make_ol, item, tq, rows, pool

LV, SUBJ, SORT = 4, "Chemistry", 13
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_formula = src("gen_uk_science_y11_organic_chemistry", "g_formula")
uk_prop = src("gen_uk_science_y11_organic_chemistry", "g_prop")
uk_use = src("gen_uk_science_y11_organic_chemistry", "g_use")
uk_comb = src("gen_uk_science_y11_organic_chemistry", "g_comb")
uk_crack = src("gen_uk_science_y11_organic_chemistry", "g_crack")
uk_test = src("gen_uk_science_y11_organic_chemistry", "g_test")

ST = ["meth", "eth", "prop", "but", "pent", "hex"]
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def f(s):
    """C2H6 -> C₂H₆ (digits after letters or ')' become subscripts)"""
    out, sub = "", False
    for i, ch in enumerate(s):
        sub = ch.isdigit() and i > 0 and (s[i - 1].isalpha() or s[i - 1] == ")" or sub)
        out += ch.translate(SUB) if sub else ch
    return out


def cf(c, h, tail=""):
    return f(("C" if c == 1 else "C%d" % c) + ("H" if h == 1 else ("H%d" % h if h else "")) + tail)


def formula(series, n):
    if series == "alkane":
        return cf(n, 2 * n + 2)
    if series == "alkene":
        return cf(n, 2 * n)
    if series == "alcohol":
        return cf(n, 2 * n + 1, "OH")
    return f("HCOOH") if n == 1 else cf(n - 1, 2 * n - 1, "COOH")


def name(series, n):
    return ST[n - 1] + {"alkane": "ane", "alkene": "ene", "alcohol": "anol", "acid": "anoic acid"}[series]


def g_series():
    s = R.choice(["alkane", "alkene", "alcohol", "acid"])
    n = R.randint(2 if s == "alkene" else 1, 4 if s == "acid" else 5)
    a = formula(s, n)
    wr = set()
    for s2 in ["alkane", "alkene", "alcohol", "acid"]:
        if s2 != s and not (s2 == "alkene" and n == 1):
            wr.add(formula(s2, n))
    if s == "acid" and n > 1:
        wr.add(cf(n, 2 * n + 1, "COOH"))
    wr.discard(a)
    wr = sorted(wr)
    if len(wr) < 3:
        return None
    if R.random() < 0.5:
        return tq("What is the molecular formula of %s?" % name(s, n), a, R.sample(wr, 3),
                  "%s has %d carbon atom%s (%s-). %s" % (name(s, n)[0].upper() + name(s, n)[1:], n, "" if n == 1 else "s", ST[n - 1],
                   {"alkane": "Alkanes are CₙH₂ₙ₊₂.", "alkene": "Alkenes are CₙH₂ₙ.", "alcohol": "Alcohols are CₙH₂ₙ₊₁OH.",
                    "acid": "Carboxylic acids are CₙH₂ₙ₊₁COOH, and the carbon in –COOH is counted in the name."}[s]))
    wn = sorted({name(s2, n) for s2 in ["alkane", "alkene", "alcohol", "acid"] if s2 != s and not (s2 == "alkene" and n == 1)} |
                ({name(s, n + 1)} if n < 5 else set()) | ({name(s, n - 1)} if n > 1 and not (s == "alkene" and n == 2) else set()))
    if len(wn) < 3:
        return None
    return tq("Which compound has the formula %s?" % a, name(s, n), R.sample(wn, 3),
              "Count the carbon atoms (%d: %s-) and look at the functional group." % (n, ST[n - 1]))


GEN = [("alkanes", "CₙH₂ₙ₊₂", "C–C single bonds only"), ("alkenes", "CₙH₂ₙ", "the C=C double bond"),
       ("alcohols", "CₙH₂ₙ₊₁OH", "the –OH (hydroxyl) group"), ("carboxylic acids", "CₙH₂ₙ₊₁COOH", "the –COOH (carboxyl) group")]


def g_gen():
    s, gf, fg = R.choice(GEN)
    if R.random() < 0.5:
        return tq("What is the general formula of the %s?" % s, gf, [g for x, g, _ in GEN if x != s], "Each member differs from the next by CH₂.")
    return tq("What is the functional group of the %s?" % s, fg, [g for x, _, g in GEN if x != s], "The functional group decides the chemical reactions of the series.")


ACIDS = ["methanoic", "ethanoic", "propanoic", "butanoic"]
ALCS = ["methanol", "ethanol", "propanol", "butanol"]


def g_ester():
    i, j = R.randrange(4), R.randrange(4)
    acid, alc = ACIDS[i], ALCS[j]
    est = "%syl %sanoate" % (ST[j], ST[i])
    swap = "%syl %sanoate" % (ST[i], ST[j])
    wr = [x for x in (swap, "%sanoyl %s" % (ST[i], alc), "%syl %sanoate" % (ST[j], ST[(i + 1) % 4]), "%syl %sanoate" % (ST[(j + 1) % 4], ST[i])) if x != est]
    wr = list(dict.fromkeys(wr))
    if R.random() < 0.5:
        return tq("Which ester is made when %s acid reacts with %s?" % (acid, alc), est, wr[:3],
                  "The alcohol gives the first part (%syl) and the acid gives the second part (%sanoate). Water is also made." % (ST[j], ST[i]))
    wr2 = ["%s acid and %s" % (ACIDS[j], ALCS[i]), "%s acid and %s" % (acid, ALCS[(j + 1) % 4]), "%s acid and %s" % (ACIDS[(i + 1) % 4], alc)]
    wr2 = [x for x in dict.fromkeys(wr2) if x != "%s acid and %s" % (acid, alc)]
    if len(wr2) < 3:
        return None
    return tq("Which two compounds react to make %s?" % est, "%s acid and %s" % (acid, alc), wr2,
              "%syl- comes from %s; -%sanoate comes from %s acid." % (ST[j].capitalize(), alc, ST[i], acid))


RXN = [("ethene + bromine (aqueous)", "1,2-dibromoethane; the orange bromine water is decolourised"),
       ("ethene + hydrogen (nickel catalyst, about 200 °C)", "ethane"),
       ("ethene + steam (phosphoric(V) acid catalyst, 300 °C, 60 atm)", "ethanol"),
       ("glucose + yeast (about 37 °C, no oxygen)", "ethanol and carbon dioxide"),
       ("ethanol + acidified potassium manganate(VII), warmed", "ethanoic acid; the purple solution turns colourless"),
       ("ethanoic acid + ethanol (concentrated sulfuric acid catalyst, warmed)", "ethyl ethanoate and water"),
       ("methane + chlorine in ultraviolet light", "chloromethane and hydrogen chloride"),
       ("ethanoic acid + sodium carbonate", "sodium ethanoate, water and carbon dioxide"),
       ("ethanol burned in excess oxygen", "carbon dioxide and water"),
       ("long-chain alkane over hot aluminium oxide (cracking)", "a shorter alkane and an alkene")]
g_rxn = rows(R, RXN, "What is made in this reaction? %s", "Which reaction gives this result? “%s”")

RTYPE = [("ethene reacting with bromine", "addition"), ("methane reacting with chlorine in UV light", "substitution"),
         ("ethanol changing to ethanoic acid with acidified potassium manganate(VII)", "oxidation"), ("ethanoic acid reacting with ethanol", "esterification (condensation)"),
         ("glucose changing to ethanol with yeast", "fermentation"), ("decane breaking into octane and ethene", "cracking"),
         ("ethene molecules joining to make poly(ethene)", "addition polymerisation"), ("ethene reacting with hydrogen to make ethane", "addition (hydrogenation)"),
         ("making nylon from a diamine and a dicarboxylic acid", "condensation polymerisation"), ("propane burning in air", "combustion")]
g_rtype = rows(R, RTYPE, "What type of reaction is this: %s?", "Which is an example of %s?")

POLY = [("ethene", "CH₂=CH₂", "poly(ethene)", "plastic bags and cling film"), ("propene", "CH₂=CHCH₃", "poly(propene)", "ropes and food containers"),
        ("chloroethene", "CH₂=CHCl", "poly(chloroethene) (PVC)", "water pipes and cable insulation"), ("tetrafluoroethene", "CF₂=CF₂", "poly(tetrafluoroethene) (PTFE)", "non-stick coatings on pans"),
        ("phenylethene (styrene)", "CH₂=CHC₆H₅", "poly(phenylethene) (polystyrene)", "packaging and disposable cups")]


def g_poly():
    m, fm, pn, use = R.choice(POLY)
    k = R.choice(["name", "mono", "use", "form"])
    others = [x for x in POLY if x[0] != m]
    if k == "name":
        return tq("Which addition polymer is made from the monomer %s?" % m, pn, [x[2] for x in R.sample(others, 3)], "Put “poly” and brackets around the monomer name.")
    if k == "mono":
        return tq("What is the monomer of %s?" % pn, m, [x[0] for x in R.sample(others, 3)], "Remove “poly” and the brackets to find the monomer.")
    if k == "form":
        return tq("Which monomer, %s, is used to make an addition polymer? Choose its formula." % m, fm, [x[1] for x in R.sample(others, 3)],
                  "Every addition monomer has a C=C double bond.")
    return tq("Which polymer is used for %s?" % use, pn, [x[2] for x in R.sample(others, 3)], "%s: %s." % (pn[0].upper() + pn[1:], use))


ISO = [("butane, C₄H₁₀", "2"), ("pentane, C₅H₁₂", "3"), ("hexane, C₆H₁₄", "5"), ("butene, C₄H₈ (straight and branched alkenes)", "3"), ("propanol, C₃H₇OH (alcohols only)", "2")]


def g_iso():
    c, n = R.choice(ISO)
    return tq("How many structural isomers are there of %s?" % c, n, [x for x in ("1", "2", "3", "4", "5", "6") if x != n and abs(int(x) - int(n)) <= 3][:3],
              "Isomers have the same molecular formula but different structural formulae (a different chain or position of the functional group).")


POOL1 = pool(R, [
    ("What is a homologous series?", "a family of compounds with the same general formula and functional group, and similar chemical properties",
     ["compounds with the same molecular formula", "compounds made from the same element", "compounds with the same boiling point"], "Physical properties change gradually down the series."),
    ("How does the boiling point change as alkanes get longer?", "It increases.", ["It decreases.", "It stays the same.", "It rises, then falls."], "Larger molecules have stronger forces of attraction between them."),
    ("How is crude oil separated into fractions?", "by fractional distillation", ["by filtration", "by cracking", "by chromatography"], "Fractions with different boiling points condense at different heights in the column."),
    ("Where in the fractionating column do the fractions with the lowest boiling points come out?", "at the top", ["at the bottom", "in the middle", "they stay in the furnace"], "The column is coolest at the top."),
    ("Why are alkanes described as saturated?", "They contain only C–C single bonds.", ["They contain C=C double bonds.", "They dissolve in water.", "They contain oxygen."], "No more atoms can be added."),
    ("How can you tell an alkene from an alkane?", "Add bromine water: the alkene decolourises it, the alkane does not.", ["Add limewater: the alkene turns it milky.", "Add water: the alkene dissolves.", "Smell them."], "The C=C bond reacts by addition."),
    ("What are isomers?", "compounds with the same molecular formula but different structural formulae", ["compounds with the same structural formula", "atoms with different numbers of neutrons", "polymers made of different monomers"], "For example butane and methylpropane."),
    ("Why is hydrogenation of vegetable oils used to make margarine?", "Adding hydrogen to C=C bonds makes the oil more saturated, so it becomes a solid at room temperature.", ["It makes the oil a liquid.", "It removes carbon.", "It adds water to the oil."], "Nickel is the catalyst."),
    ("What is the main use of ethanol made by fermentation?", "as a fuel and in alcoholic drinks", ["to make plastic bags", "as a catalyst", "to neutralise acids"], "It is renewable because sugar comes from plants."),
    ("Which property do esters often have?", "sweet, fruity smells", ["a sour taste and pH 1", "they decolourise bromine water", "they are gases at room temperature"], "Used in flavourings and perfumes."),
    ("Ethanoic acid is a weak acid. What does this mean?", "It only partly ionises in water.", ["It is very dilute.", "It does not react with metals.", "It has a pH of 7."], "Vinegar is a dilute solution of ethanoic acid."),
    ("Why is cracking important in industry?", "It turns long-chain fractions, which are in low demand, into petrol and alkenes, which are in high demand.", ["It makes crude oil from plants.", "It separates crude oil into fractions.", "It removes sulfur from fuel."], "Alkenes are used to make polymers."),
])
POOL5 = pool(R, [
    ("Nylon and PET are condensation polymers. What else forms when they are made?", "water (a small molecule)", ["nothing else", "hydrogen", "carbon dioxide"], "Monomers with two functional groups join and lose a small molecule each time."),
    ("Which statement about addition polymerisation is correct?", "The polymer is the only product.", ["Water is also formed.", "The monomers have no double bonds.", "Two different monomers are always needed."], "The C=C bonds open and join into a long chain."),
    ("Why do plastics cause pollution when thrown away?", "Most are non-biodegradable, so they stay in landfills and the sea for a very long time.", ["They dissolve in rainwater.", "They decompose quickly into acids.", "They are made from renewable plants."], "Plastic waste harms marine life."),
    ("What is a problem with burning plastic waste?", "It can release toxic gases such as hydrogen chloride from PVC, and carbon dioxide.", ["It produces only water.", "It makes the plastic biodegradable.", "It uses up nitrogen in the air."], "Incinerators need gas cleaning."),
    ("Which is an advantage of recycling plastics?", "It saves crude oil and reduces plastic waste.", ["It uses no energy at all.", "It makes plastics biodegradable.", "Every plastic can be recycled many times without change."], "Plastics must first be sorted by type."),
    ("Which pair of compounds are isomers?", "butane and methylpropane", ["ethane and ethene", "ethanol and ethanoic acid", "propane and butane"], "Both are C₄H₁₀."),
    ("A compound C₃H₆ decolourises bromine water. What is it?", "propene", ["propane", "propanol", "propanoic acid"], "C₃H₆ fits CₙH₂ₙ, the alkenes."),
    ("A compound reacts with magnesium to give hydrogen and has the formula C₂H₅COOH. What is its name?", "propanoic acid", ["ethanoic acid", "ethanol", "propanol"], "There are 3 carbon atoms, including the one in –COOH."),
    ("Ethanol can be made by fermentation or from ethene and steam. Which is an advantage of using ethene?", "It is a fast, continuous process that gives pure ethanol.", ["Ethene comes from a renewable resource.", "It needs no energy.", "It works at room temperature."], "Fermentation uses renewable sugar but is slow and gives dilute ethanol."),
    ("Which polymer is made by condensation polymerisation?", "nylon", ["poly(ethene)", "poly(propene)", "PVC"], "Nylon is a polyamide made from a diamine and a dicarboxylic acid."),
])


def main():
    sets = U.sets([
        ("Fuels and crude oil", [(uk_use, 6), (uk_comb, 5), (uk_crack, 5), (POOL1, 4)]),
        ("Homologous series and formulae", [(g_series, 9), (g_gen, 5), (uk_formula, 3), (g_iso, 3)]),
        ("Reactions of organic compounds", [(g_rxn, 7), (uk_test, 4), (uk_prop, 4), (g_rtype, 5)]),
        ("Alcohols, acids and esters", [(g_ester, 9), (g_series, 4), (g_rxn, 3), (POOL1, 4)]),
        ("Polymers and exam-style questions", [(g_poly, 8), (POOL5, 8), (g_rtype, 4)]),
    ])
    make_ol(LV, SUBJ, "organic-chemistry", SORT, "Organic Chemistry",
            "Describe crude oil as a mixture of hydrocarbons separated by fractional distillation and state the uses of its fractions; describe cracking; describe a "
            "homologous series and state the general formulae and functional groups of alkanes, alkenes, alcohols and carboxylic acids; draw and name structural "
            "isomers; describe combustion and substitution of alkanes, addition reactions of alkenes with bromine, hydrogen and steam, the manufacture of ethanol, "
            "oxidation of ethanol and the formation of esters; describe addition and condensation polymerisation and the problems of disposing of plastics "
            "(summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Organic Chemistry", "Organic chemistry",
            "Free Secondary 4 O-Level Chemistry worksheets on organic chemistry: crude oil, cracking, alkanes, alkenes, alcohols, carboxylic acids, esters, isomers and "
            "polymers. 100 questions with answers.",
            "Same functional group = same reactions.", "Alkanes CₙH₂ₙ₊₂, alkenes CₙH₂ₙ, alcohols –OH, acids –COOH.",
            "<p><b>Count the carbons for the name; find the functional group for the reactions.</b></p><ul>"
            "<li>meth- 1, eth- 2, prop- 3, but- 4, pent- 5. Alkanes -ane, alkenes -ene, alcohols -anol, acids -anoic acid (the –COOH carbon counts).</li>"
            "<li>Alkenes add bromine (decolourised), hydrogen (Ni) and steam (H₃PO₄) across C=C. Alkanes only burn or substitute in UV light.</li>"
            "<li>Ethanol is oxidised to ethanoic acid; acid + alcohol → ester + water (alcohol part first: ethyl ethanoate).</li>"
            "<li>Addition polymers come from C=C monomers with no other product; condensation polymers (nylon, PET) also give water.</li></ul>",
            [("Name the ester from propanoic acid and methanol.", ["alcohol part first: methyl", "acid part: propanoate"], "methyl propanoate"),
             ("Formula of butene?", ["alkene CₙH₂ₙ, n = 4"], "C₄H₈")],
            ["Using CₙH₂ₙ for alkanes.", "Naming esters with the acid first.", "Forgetting the –COOH carbon (C₂H₅COOH is propanoic acid).",
             "Saying alkanes decolourise bromine water.", "Saying addition polymers give water."],
            [("How do you name an ester?", "The alcohol gives the first word ending in -yl and the acid gives the second word ending in -anoate: ethanol + propanoic acid gives ethyl propanoate."),
             ("What is the difference between addition and condensation polymers?", "Addition polymers form from monomers with C=C bonds and nothing else is made. Condensation polymers form from monomers with two functional groups and a small molecule such as water is lost each time."),
             ("What is the test for an alkene?", "Shake with bromine water: an alkene turns it from orange to colourless; an alkane leaves it orange.")],
            sets)


if __name__ == "__main__":
    main()
