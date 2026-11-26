# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Biology): Infection and Response
  python tools/gen_uk_science_y10_infection_and_response.py
Pathogens (viruses, bacteria, fungi, protists) and the diseases they cause, how diseases spread and are prevented,
the body's defences, white blood cells (phagocytosis, antibodies, antitoxins), vaccination and herd immunity,
antibiotics and painkillers, antibiotic resistance, bacterial growth by doubling, and the development of new drugs.
Wrong answers come from real mistakes: "antibiotics kill viruses", "vaccines contain antibodies",
"all bacteria are harmful", "painkillers cure the disease".
"""
from uk_sci import item, bank, table, once
from uk_ks4 import U4, build
from sci_phys import uniq

U, R, P, us = U4(62004)

DIS = [("measles", "a virus", "droplets from sneezes and coughs", "a red skin rash and fever"), ("HIV", "a virus", "sexual contact and exchange of body fluids", "flu-like illness, then damage to the immune system"),
       ("tobacco mosaic virus (TMV)", "a virus", "contact between plants", "a mosaic pattern of discoloured leaves"), ("salmonella food poisoning", "a bacterium", "eating undercooked or contaminated food", "fever, stomach cramps, vomiting and diarrhoea"),
       ("gonorrhoea", "a bacterium", "sexual contact", "a thick yellow or green discharge and pain when urinating"), ("rose black spot", "a fungus", "spores carried by wind or water", "purple or black spots on leaves"),
       ("malaria", "a protist", "bites from infected mosquitoes", "recurring fever")]


def g_dis():
    d, p, s, sym = R.choice(DIS)
    k = R.choice(["path", "spread", "sym"])
    if not once(("di", d, k)):
        return None
    if k == "path":
        return item("What type of pathogen causes %s?" % d, p, [x for x in ["a virus", "a bacterium", "a fungus", "a protist"] if x != p], "Viruses, bacteria, fungi and protists.")
    if k == "spread":
        return item("How is %s spread?" % d, s, R.sample([x[2] for x in DIS if x[2] != s], 3), "Know how to stop the spread.")
    return item("Which symptom is linked to %s?" % d, sym, R.sample([x[3] for x in DIS if x[3] != sym], 3), "Symptoms help diagnosis.")


DEF = [("the skin", "acts as a barrier and makes antimicrobial secretions"), ("hairs and mucus in the nose", "trap particles that may contain pathogens"),
       ("cilia in the trachea and bronchi", "move mucus with trapped pathogens up to the throat"), ("acid in the stomach", "kills pathogens in food and drink"),
       ("phagocytes (white blood cells)", "engulf and digest pathogens"), ("antibodies", "attach to antigens on pathogens so they can be destroyed"),
       ("antitoxins", "neutralise toxins made by bacteria")]


def g_def():
    p, j = R.choice(DEF)
    k = R.random() < 0.5
    if not once(("de", p, k)):
        return None
    PL = ("hairs and mucus in the nose", "cilia in the trachea and bronchi", "phagocytes (white blood cells)", "antibodies", "antitoxins")
    sv = lambda x: ("They " if x[0] in PL else "It ") + x[1] + "."
    if k:
        return item("How does %s help defend the body?" % p if p not in PL else "How do %s help defend the body?" % p, sv((p, j)),
                    [sv(x) for x in R.sample([x for x in DEF if x[0] != p], 3)], "First and second lines of defence.")
    return item("Which part of the body's defences does this: “%s”?" % (j[0].upper() + j[1:]), p, R.sample([x[0] for x in DEF if x[0] != p], 3), "First and second lines of defence.")


def g_grow():
    t = R.choice([20, 30])
    hrs = R.choice([1, 2, 3, 4])
    start = R.choice([1, 2, 5, 10, 100])
    n = hrs * 60 // t
    end = start * 2 ** n
    if end > 10 ** 7 or not once(("gr", t, hrs, start)):
        return None
    g = "{:,}".format(end)
    return item("A bacterium divides every %d minutes. Starting with %s bacteria, how many will there be after %d hour%s?" % (t, "{:,}".format(start), hrs, "" if hrs == 1 else "s"), g,
                uniq(g, ["{:,}".format(start * 2 * n), "{:,}".format(start * 2 ** (n - 1)), "{:,}".format(start * 2 ** (n + 1)), "{:,}".format(start * n)]),
                "%d hour%s = %d divisions. %s × 2<sup>%d</sup> = %s." % (hrs, "" if hrs == 1 else "s", n, "{:,}".format(start), n, g))


def fm(v):
    v = round(v, 1)
    return ("{:,}".format(int(v)) if v == int(v) else "{:,}".format(v)) + " mm²"


def g_zone():
    who = P.next()[0]
    ab = ["A", "B", "C", "D"]
    d = R.sample([0, 6, 8, 10, 12, 14, 16, 18, 20], 4)
    k = R.choice(["best", "none", "area"])
    if not once(("zo", tuple(d), k)) or not once(("zo", k), 10):
        return None
    tab = table(["Antibiotic disc", "Diameter of clear zone (mm)"], [[a, str(x)] for a, x in zip(ab, d)])
    intro = tab + "%s placed antibiotic discs on a plate of bacteria. " % who
    if k == "best":
        b = ab[d.index(max(d))]
        return item(intro + "Which antibiotic was most effective?", "antibiotic " + b, ["antibiotic " + a for a in ab if a != b], "The biggest clear zone.")
    if k == "none":
        if 0 not in d:
            return None
        b = ab[d.index(0)]
        return item(intro + "What does a clear zone of 0 mm for antibiotic %s show?" % b, "The bacteria are resistant to it (it did not kill them).", ["It is the strongest antibiotic.", "The disc was too big.", "It killed all the bacteria."], "No zone, no effect.")
    x = max(d)
    r = x / 2
    a = round(3.14 * r * r, 1)
    g = fm(a)
    return item(intro + "Using πr² with π = 3.14, what is the area of the largest clear zone?", g, uniq(g, [fm(3.14 * x * x), fm(3.14 * x), fm(2 * 3.14 * r), fm(x * x)]),
                "r = %g mm, so 3.14 × %g² = %s." % (r, r, g))


B1 = bank([
    ("What is a pathogen?", "a microorganism that causes disease", ["any bacterium", "a type of white blood cell", "a medicine"], "Viruses, bacteria, fungi, protists."),
    ("How do viruses make us ill?", "They live and reproduce inside cells, damaging them.", ["They make toxins outside cells only.", "They eat our food.", "They block arteries."], "Cell damage."),
    ("How do bacteria make us ill?", "They reproduce quickly and may make toxins that damage tissues.", ["They live only inside cells.", "They change our DNA.", "They are always harmless."], "Toxins."),
    ("Which is a way to reduce the spread of disease?", "hand washing, vaccination and isolating infected people", ["sharing towels", "eating undercooked meat", "never washing"], "Hygiene."),
])
B5 = bank([
    ("How does a vaccine work?", "It contains dead or inactive pathogens, so white blood cells make antibodies and memory cells without illness.", ["It contains antibodies from another person.", "It kills all bacteria.", "It is a painkiller."], "Fast response next time."),
    ("Why do antibiotics not work against viruses?", "Viruses live inside cells, and antibiotics only kill bacteria.", ["Viruses are too big.", "Antibiotics are too weak.", "Viruses have no DNA."], "Use antivirals or let the immune system fight."),
    ("How does antibiotic resistance spread?", "Resistant bacteria survive treatment and reproduce, so resistant strains become common.", ["Bacteria decide to resist.", "Antibiotics turn into bacteria.", "People become resistant."], "Natural selection."),
    ("What do painkillers do?", "relieve symptoms but do not kill pathogens", ["kill bacteria", "kill viruses", "make antibodies"], "Treat symptoms only."),
    ("In a drug trial, what is a double-blind trial?", "Neither the patients nor the doctors know who has the drug or the placebo.", ["Only the patients know.", "The drug is given twice.", "Patients are blindfolded."], "Avoids bias."),
    ("Which plant produces digitalis, used to treat heart conditions?", "foxglove", ["willow", "rose", "potato"], "Aspirin came from willow."),
    ("Who discovered penicillin?", "Alexander Fleming", ["Louis Pasteur", "Edward Jenner", "Charles Darwin"], "From Penicillium mould."),
])

if __name__ == "__main__":
  build(U, 10, "infection-and-response", 4, "Biology", "Infection and response",
      "Communicable diseases caused by viruses, bacteria, fungi and protists, how they are spread and how their spread can be reduced; non-specific defences and the immune system; vaccination; antibiotics and painkillers; antibiotic resistance; the discovery and development of drugs, including clinical trials.",
      "Infection and Response", "Infection and Response",
      "Free Year 10 GCSE Combined Science worksheets on infection and response: pathogens and diseases, the body's defences, white blood cells, vaccination, antibiotics, resistance and drug trials. 100 questions with answers.",
      "Antibiotics kill bacteria, not viruses.",
      "White blood cells engulf pathogens and make antibodies and antitoxins.",
      "<p><b>Pathogens are microorganisms that cause disease.</b></p><ul><li>Viruses damage cells from inside; bacteria may make toxins; fungi and protists cause diseases such as rose black spot and malaria.</li>"
      "<li>The body's defences: skin, mucus, cilia, stomach acid, then white blood cells (phagocytosis, antibodies, antitoxins).</li>"
      "<li>Vaccines give immunity without illness. Antibiotics kill bacteria only; overuse leads to resistance.</li></ul>",
      [("Bacteria double every 20 min. After 1 hour from 1?", ["3 divisions", "2 × 2 × 2"], "8"), ("Measles: pathogen type?", ["Spread by droplets"], "a virus")],
      ["Thinking antibiotics kill viruses.", "Thinking vaccines contain antibodies.", "Thinking painkillers cure diseases."],
      [("What is the difference between viruses and bacteria?", "Viruses are much smaller and reproduce inside cells, damaging them. Bacteria are living cells that can reproduce on their own and may make toxins. Antibiotics only work on bacteria."),
       ("How does vaccination work?", "A vaccine contains dead or inactive pathogens. White blood cells make antibodies and memory cells, so if the real pathogen enters, the body responds quickly."),
       ("Why is antibiotic resistance a problem?", "Some bacteria survive antibiotics and reproduce, so resistant strains such as MRSA spread and become harder to treat.")],
      [("Pathogens and disease", B1 + [(g_dis, 16)]),
       ("How diseases spread", [(g_dis, 4), (g_grow, 16)]),
       ("Defences", [(g_def, 12), (g_grow, 8)]),
       ("Antibiotics", [(g_zone, 14), (g_def, 2), (g_grow, 4)]),
       ("Vaccines and drugs", B5 + [(g_zone, 7), (g_grow, 6)])])
