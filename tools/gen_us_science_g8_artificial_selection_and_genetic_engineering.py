# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Artificial Selection and Genetic Engineering (MS-LS4-5)
  python tools/gen_us_science_g8_artificial_selection_and_genetic_engineering.py
Gather and synthesize information about the technologies that have changed the way humans influence the inheritance
of desired traits in organisms: artificial selection (selective breeding), genetic engineering (moving or editing genes),
gene therapy; benefits, risks and trade-offs; breeding data over generations.
Wrong answers come from real mistakes: "selective breeding creates brand-new genes on purpose", "genetic engineering is
the same as natural selection", "artificial selection happens in one generation".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(80117)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


METH = [("Farmers breed only the cows that give the most milk.", "artificial selection"),
        ("Scientists put the human insulin gene into bacteria to make insulin medicine.", "genetic engineering"),
        ("Dog breeders mate the calmest dogs to produce guide dogs.", "artificial selection"),
        ("A gene from a soil bacterium is added to corn so it makes its own insect poison (Bt corn).", "genetic engineering"),
        ("Over thousands of years, people planted seeds from the biggest teosinte plants, producing modern corn.", "artificial selection"),
        ("Scientists add genes to rice so it makes vitamin A (golden rice).", "genetic engineering"),
        ("Gardeners save seeds from the sweetest tomatoes each year.", "artificial selection"),
        ("Scientists use CRISPR to edit a gene in a crop so it resists a disease.", "genetic engineering"),
        ("Moths with dark wings survive better on sooty trees with no human choosing.", "natural selection"),
        ("Bacteria become resistant to an antibiotic in a hospital.", "natural selection"),
        ("Breeders choose the chickens that lay the most eggs.", "artificial selection"),
        ("A jellyfish gene for glowing protein is added to fish to make them glow.", "genetic engineering"),
        ("On an island, birds with stronger beaks survive a drought and reproduce.", "natural selection"),
        ("Horse breeders mate the fastest horses to produce racehorses.", "artificial selection")]


def g_meth():
    s, a = R.choice(METH)
    who = P.next()[0]
    if not once(("m", s)):
        return None
    return item("%s reads: “%s” Which process is this?" % (who, s), a, [x for x in ["artificial selection", "genetic engineering", "natural selection"] if x != a] + ["asexual budding"],
                {"artificial selection": "People choose which organisms reproduce.", "genetic engineering": "Scientists change or move genes directly.",
                 "natural selection": "The environment, not people, decides which individuals survive."}[a])


WILD = [("wild mustard", ["broccoli", "cabbage", "kale", "cauliflower", "Brussels sprouts"]), ("gray wolves", ["dog breeds like poodles, beagles and huskies"]),
        ("teosinte", ["modern corn with large ears"]), ("wild cabbage", ["kohlrabi"]), ("red junglefowl", ["modern chickens"]), ("wild aurochs", ["modern cattle"])]


def g_wild():
    w0, lst = R.choice(WILD)
    crop = R.choice(lst)
    who = P.next()[0]
    if not once(("w", crop)):
        return None
    return item("%s learns that %s came from %s. How did people get this result?" % (who, crop, w0), "by artificial selection: breeding the individuals with desired traits for many generations",
                ["by genetic engineering in a single year", "by natural selection with no human help", "by mixing chemicals into the soil"], "Selective breeding takes many generations.")


def g_data():
    who = P.next()[0]
    k = R.choice(["milk", "corn", "eggs"])
    if k == "milk":
        a, st, un, lab = R.choice([4000, 5000, 6000]), R.choice([500, 1000, 1500]), "kg of milk per cow per year", "Average milk"
    elif k == "corn":
        a, st, un, lab = R.choice([8, 10, 12]), R.choice([2, 3, 4]), "cm ear length", "Average ear length"
    else:
        a, st, un, lab = R.choice([150, 180, 200]), R.choice([20, 25, 30]), "eggs per hen per year", "Average eggs"
    gens = [1, 5, 10, 15]
    vals = [a + st * i for i in range(4)]
    q = R.choice(["change", "pred", "why"])
    if not once((k, a, st, q)) or (q == "why" and not once("why", 4)):
        return None
    tab = table(["Generation of selective breeding", "%s (%s)" % (lab, un)], [[str(g), comma(v)] for g, v in zip(gens, vals)])
    if q == "change":
        return item(tab + "In %s's breeding data, how much did the average increase from generation 1 to generation 15?" % who, "%s %s" % (comma(vals[3] - vals[0]), un),
                    ["%s %s" % (comma(vals[3]), un), "%s %s" % (comma(st), un), "%s %s" % (comma(vals[3] + vals[0]), un)], "%s − %s = %s." % (comma(vals[3]), comma(vals[0]), comma(vals[3] - vals[0])))
    if q == "pred":
        return item(tab + "If %s's trend continues, what is the best prediction for generation 20?" % who, "%s %s" % (comma(vals[3] + st), un),
                    ["%s %s" % (comma(vals[3]), un), "%s %s" % (comma(vals[0]), un), "%s %s" % (comma(vals[3] + st * 5), un)], "It rises by %s every 5 generations." % comma(st))
    return item(tab + "What best explains %s's data?" % who, "Breeders chose parents with the desired trait each generation, so the trait increased.",
                ["The animals or plants changed on purpose.", "The trait increased because of the weather only.", "A single gene was edited in generation 15."], "This is artificial selection.")


PROCON = [("Bt corn", "fewer insecticide sprays are needed", "insects may evolve resistance to the Bt toxin"),
          ("selective breeding of one banana variety", "every banana tastes and looks the same", "low genetic variation means one disease could wipe out the crop"),
          ("insulin made by engineered bacteria", "cheaper, safer insulin for people with diabetes", "factories must keep the bacteria contained"),
          ("dog breeds with very flat faces", "a look some owners like", "many have breathing problems"),
          ("drought-resistant engineered crops", "more food in dry regions", "genes could spread to wild relatives"),
          ("gene therapy for an inherited disease", "it may treat the cause of the disease", "it is expensive and can have unexpected side effects")]


def g_pro():
    t, pro, con = R.choice(PROCON)
    who = P.next()[0]
    k = R.random() < 0.5
    if not once((t, k)):
        return None
    if k:
        return item("%s is writing about %s. What is a benefit?" % (who, t), pro, [x[2] for x in R.sample([p for p in PROCON if p[0] != t], 2)] + [con], "Every technology has benefits and risks.")
    return item("%s is writing about %s. What is a possible risk?" % (who, t), con, [x[1] for x in R.sample([p for p in PROCON if p[0] != t], 2)] + [pro], "Weigh trade-offs with evidence.")


B1 = bank([
    ("What is artificial selection?", "humans choosing which organisms reproduce to increase desired traits", ["the environment choosing survivors", "editing DNA in a lab", "random mutation"], "Also called selective breeding."),
    ("What is genetic engineering?", "directly changing an organism's genes, often by adding a gene from another organism", ["breeding the best animals", "natural selection", "giving animals vitamins"], "Done in a lab."),
    ("How is artificial selection different from natural selection?", "People, not the environment, choose which traits are passed on.", ["They are the same.", "Artificial selection uses no genes.", "Natural selection needs a lab."], "Who does the selecting."),
    ("Why does selective breeding take many generations?", "Desired traits become more common a little at a time with each generation.", ["It always works in one generation.", "Animals must learn the traits.", "Genes are added slowly by hand."],
     "Gradual change."),
    ("Can artificial selection create a trait that has no genetic variation at all?", "No. It can only select from traits that already vary.", ["Yes, always.", "Only in plants.", "Only with dogs."], "It needs existing variation."),
    ("What is one advantage of genetic engineering over selective breeding?", "A specific gene can be added in one generation, even from another species.", ["It needs many generations.", "It never has risks.", "It only works in animals."], "Faster and more precise."),
    ("What is gene therapy?", "treating a disease by changing or replacing a faulty gene in a person's cells", ["breeding healthy people", "giving vitamins", "a type of surgery on bones"], "A medical technology."),
    ("Why might farmers want crops with less genetic variation?", "The crops are uniform in size, taste and harvest time.", ["They are always healthier.", "They resist every disease.", "They need no water."], "But there is a risk."),
])
B5 = bank([
    ("Ava wants tomatoes that taste sweeter. Without a lab, what should she do?", "Save and plant seeds only from the sweetest tomatoes each year.", ["Add sugar to the soil.", "Plant random seeds.", "Wait for natural selection."], "Selective breeding."),
    ("Leo reads that all Cavendish bananas are clones. Why is this a concern?", "A single disease could infect them all because they have no variation.", ["They taste the same.", "They are too big.", "Clones grow too fast."], "Low variation is a risk."),
    ("Mia compares insulin from engineered bacteria with insulin from pig organs. What is a benefit of the engineered insulin?", "It is identical to human insulin and can be made in large amounts.", ["It comes from pigs.", "It is made by selective breeding.", "It has no protein."],
     "A real medical advance."),
    ("Which question is most useful when judging a new genetically engineered crop?", "What evidence shows its benefits and risks to people and ecosystems?", ["What color is the packaging?", "Is the farm large?", "How old is the scientist?"], "Base decisions on evidence."),
    ("Over 30 generations, a cattle breeder's herd got larger muscles. What technology was used?", "selective breeding", ["gene therapy", "cloning by budding", "natural selection only"], "Choosing parents each generation."),
])


def body():
    think = ("<p>People influence which traits are inherited in two main ways:</p><ul>"
             "<li><b>Artificial selection</b> (selective breeding): people choose parents with desired traits, generation after generation. Dogs from wolves, corn from teosinte and broccoli from wild mustard were made this way.</li>"
             "<li><b>Genetic engineering</b>: scientists change genes directly, often by adding a gene from another species (insulin-making bacteria, Bt corn, golden rice) or editing a gene (CRISPR). <b>Gene therapy</b> uses this to treat diseases.</li></ul>"
             "<p>These technologies have <b>benefits</b> (more food, medicine) and <b>risks</b> (low variation, resistance, health problems in some breeds).</p>")
    ex = [("Breeders mate the fastest horses. Process?", ["People choose parents."], "artificial selection"),
          ("A gene for insulin is added to bacteria. Process?", ["Genes changed directly."], "genetic engineering")]
    mist = ["Thinking selective breeding creates brand-new genes on purpose.",
            "Thinking genetic engineering and natural selection are the same.",
            "Thinking artificial selection works in one generation."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Changing inheritance", B1 + [(g_meth, 12)]),
        ("Selective breeding", [(g_wild, 8), (g_data, 12)]),
        ("Breeding data", [(g_data, 16), (g_meth, 2), (g_wild, 2)]),
        ("Benefits and risks", [(g_pro, 12), (g_data, 8)]),
        ("Evaluating technologies", B5 + [g_pro, g_data, g_meth]),
    ])
    make("grade-8", "artificial-selection-and-genetic-engineering", 17, "MS-LS4-5",
         "Gather and synthesize information about the technologies that have changed the way humans influence the inheritance of desired traits in organisms.",
         "Artificial Selection and Genetic Engineering",
         "Grade 8 Artificial Selection and Genetic Engineering Worksheets: Breeding and Genes",
         "Artificial Selection",
         "Free middle school science worksheets on artificial selection and genetic engineering (NGSS MS-LS4-5): selective breeding, breeding data over generations, genetic engineering and gene therapy, and their benefits and risks. 100 practice questions with answers.",
         "People can choose which traits are passed on.",
         "Selective breeding chooses parents over many generations. Genetic engineering changes genes directly. Both have benefits and risks.",
         body(),
         [("What is the difference between artificial selection and genetic engineering?", "In artificial selection, people choose which organisms reproduce over many generations. In genetic engineering, scientists change an organism's genes directly."),
          ("What are examples of artificial selection?", "Dog breeds from wolves, modern corn from teosinte, and broccoli, cabbage and kale from wild mustard."),
          ("What are some risks of these technologies?", "Low genetic variation can make crops vulnerable to disease, pests can evolve resistance, and some breeds have health problems.")],
         sets)


if __name__ == "__main__":
    main()
