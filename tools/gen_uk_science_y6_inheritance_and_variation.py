# -*- coding: utf-8 -*-
"""
UK Year 6 science: Inheritance and Variation (Evolution and inheritance)
  python tools/gen_uk_science_y6_inheritance_and_variation.py
Offspring are the same kind as their parents but not identical; inherited and environmental characteristics;
variation within a species shown in data (hand span, height); selective breeding; Gregor Mendel.
Wrong answers come from real mistakes: "a scar can be passed on to children", "brothers and sisters are identical",
"variation means a different species", "dyed hair colour is inherited".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once, fig, bar_chart
from sci_phys import uniq

U = Unit(61608)
R = U.R
P = People(R)

A_INH = "inherited from parents"
A_ENV = "caused by the environment or choices"
A_BOTH = "both inherited and affected by the environment"
CH = [("natural eye colour", A_INH), ("blood group", A_INH), ("whether you have dimples", A_INH), ("natural hair colour", A_INH),
      ("the shape of your ear lobes", A_INH), ("naturally curly hair", A_INH), ("a scar from a fall", A_ENV), ("speaking French", A_ENV),
      ("dyed blue hair", A_ENV), ("pierced ears", A_ENV), ("being able to ride a bike", A_ENV), ("a broken arm", A_ENV),
      ("a suntan", A_ENV), ("a favourite food", A_ENV), ("height", A_BOTH), ("body mass", A_BOTH), ("muscle strength", A_BOTH)]


def g_inh():
    c, a = R.choice(CH)
    if not once(("ch", c)):
        return None
    e = {A_INH: "Passed on in the genes from the parents.", A_ENV: "This is not in the genes, so it cannot be passed on to children.",
         A_BOTH: "Genes set a range, but food, exercise and health also affect it."}[a]
    return item("Is %s inherited or caused by the environment?" % c, a, [x for x in (A_INH, A_ENV, A_BOTH) if x != a] + ["neither, it happens by magic"], e)


def g_pick():
    k = R.choice([A_INH, A_ENV])
    a = R.choice([c for c, x in CH if x == k])
    w = R.sample([c for c, x in CH if x != k and x != A_BOTH], 3)
    if not once(("pk", a)):
        return None
    q = "Which characteristic is inherited from parents?" if k == A_INH else "Which characteristic is NOT inherited, so cannot be passed on to children?"
    return item(q, a, w, "Inherited characteristics come from genes; others come from life and choices.")


def g_hand():
    who = P.next()[0]
    labs = ["14 cm", "15 cm", "16 cm", "17 cm", "18 cm", "19 cm"]
    vals = [R.choice([1, 2, 3]), R.choice([3, 4, 5]), R.choice([6, 7, 8]), R.choice([5, 6, 7]), R.choice([2, 3, 4]), R.choice([1, 2])]
    if len(set(vals)) < 4 or vals.count(max(vals)) > 1:
        return None
    k = R.choice(["most", "read", "total", "more", "why"])
    if not once(("ha", tuple(vals), k)) or (k == "why" and not once(("hw",), 2)) or (k in ("most", "total") and not once(("hk", k), 5)):
        return None
    pic = fig(bar_chart(labs, vals, label="bar chart of hand spans", title="Hand spans in %s's class" % who, ymax=8, step=2))
    if k == "most":
        a = labs[vals.index(max(vals))]
        return item(pic + "Which hand span was the most common?", a, R.sample([x for x in labs if x != a], 3), "The tallest bar shows the most common hand span.")
    if k == "read":
        i = R.randrange(6)
        a = "%d" % vals[i]
        return item(pic + "How many pupils had a hand span of %s?" % labs[i], a, uniq(a, [str(v) for v in vals] + [str(vals[i] + 1)]), "Read the bar for %s." % labs[i])
    if k == "total":
        a = "%d" % sum(vals)
        return item(pic + "How many pupils were measured altogether?", a, uniq(a, [str(sum(vals) - 2), str(len(vals)), str(max(vals)), str(sum(vals) + 3)]), "Add all the bars.")
    if k == "more":
        i, j = R.sample(range(6), 2)
        if vals[i] <= vals[j]:
            return None
        d = vals[i] - vals[j]
        a = "%d" % d
        return item(pic + "How many more pupils had a hand span of %s than %s?" % (labs[i], labs[j]), a, uniq(a, [str(vals[i]), str(vals[j]), str(vals[i] + vals[j]), str(d + 2)]),
                    "%d − %d = %d." % (vals[i], vals[j], d))
    return item(pic + "What does the chart show about the pupils?", "There is variation: hand spans differ, with most in the middle.",
                ["Everyone has the same hand span.", "Only the tallest pupils were measured.", "Hand span is caused by a scar."], "Members of the same species vary.")


BREED = [("Farmers want cows that give more milk.", "breed from the cows that give the most milk"),
         ("Growers want wheat with bigger grains.", "plant seeds only from the plants with the biggest grains"),
         ("Shepherds wanted dogs good at herding sheep.", "breed from the dogs that were best at herding"),
         ("Gardeners want roses with a strong scent.", "cross the roses with the strongest scent"),
         ("Farmers want sheep with thicker wool.", "breed from the sheep with the thickest wool"),
         ("Growers want tomatoes that resist disease.", "keep seeds from the plants that stayed healthy")]


def g_breed():
    s, a = R.choice(BREED)
    if not once(("br", s)):
        return None
    w = R.sample([x[1] for x in BREED if x[1] != a], 2) + ["choose at random and hope"]
    return item("%s What should they do?" % s, a, w, "Selective breeding: people choose parents with the characteristic they want, generation after generation.")


OFF = [("Two pet rabbits have babies.", "rabbits that look similar to their parents but not exactly the same"),
       ("A sunflower makes seeds that are planted.", "sunflowers that vary a little from the parent plant"),
       ("A black cat and a ginger cat have kittens.", "kittens that may have different coat colours from each other"),
       ("Two Labrador dogs have puppies.", "Labrador puppies that are similar but not identical")]


def g_off():
    s, a = R.choice(OFF)
    if not once(("of", s)):
        return None
    return item("%s What will the offspring be?" % s, a, ["exact copies of one parent", "a completely different kind of animal or plant", "identical to each other in every way"],
                "Living things produce offspring of the same kind, but offspring normally vary.")


B1 = bank([
    ("What are offspring?", "the young that living things produce", ["the parents of an animal", "the food an animal eats", "a type of habitat"], "Kittens are a cat's offspring."),
    ("What does inherited mean?", "passed on from parents to their offspring", ["learned at school", "found in the environment", "caught from a friend"], "Through genes."),
    ("What is variation?", "differences between living things of the same kind", ["the same features in every animal", "a change in the weather", "a type of fossil"], "No two people are exactly alike."),
    ("Why do brothers and sisters look similar but not identical?", "Each child gets a different mix of characteristics from the parents.", ["They have different parents.", "They are all identical.", "Characteristics are not inherited."], "A new mix each time."),
    ("Which people can be almost identical in their inherited characteristics?", "identical twins", ["cousins", "best friends", "neighbours"], "They come from one fertilised egg."),
    ("Who studied pea plants to find out how characteristics are inherited?", "Gregor Mendel", ["Mary Anning", "Isaac Newton", "Alexander Fleming"], "He is called the father of genetics."),
    ("Can a scar be passed on to a person's children?", "No. Scars are caused by the environment, not genes.", ["Yes, always.", "Yes, if it is large.", "Only to sons."], "Only inherited characteristics pass on."),
    ("Where is the information for inherited characteristics stored?", "in genes inside cells", ["in the blood only", "in the hair only", "in the air we breathe"], "Genes are made of DNA."),
])
B5 = bank([
    ("A pupil says, 'Tall parents always have tall children.' How could you test this?", "Measure the heights of many parents and their grown-up children and look for a pattern.", ["Ask one family.", "Measure only pets.", "Guess from photographs."], "Use lots of data."),
    ("Why might identical twins have different body mass as adults?", "Their diet and exercise can be different.", ["Their genes are different.", "One is older by years.", "Twins never change."], "Environment matters."),
    ("Why do all Dalmatian puppies grow up with spots but each pattern is different?", "Spots are inherited, but the exact pattern varies.", ["Spots come from mud.", "Puppies copy each other.", "The pattern is painted on."], "Inheritance and variation."),
    ("Why is variation important for a species?", "Some individuals may survive changes in the environment better than others.", ["It makes all individuals the same.", "It stops animals having young.", "It has no effect at all."], "Leads to adaptation."),
    ("Why do dog breeds look so different when they are all one species?", "People chose which dogs to breed for thousands of years.", ["Each breed is a different species.", "Dogs changed by eating different food.", "It happened by accident last year."], "Selective breeding."),
])


def body():
    think = ("<p><b>Offspring are the same kind as their parents, but they vary.</b></p>"
             "<ul><li>Inherited characteristics (eye colour, blood group) are passed on in genes. Environmental ones (a scar, a language you learn) are not.</li>"
             "<li>Some, such as height, depend on both genes and the environment.</li>"
             "<li>Variation means individuals of the same species are different. People use it in selective breeding.</li></ul>")
    ex = [("Dyed purple hair: inherited?", ["It comes from a choice, not genes"], "No, environmental"),
          ("Farmers want more milk. What do they do?", ["Choose the best milk cows as parents"], "selective breeding")]
    mist = ["Thinking a scar or a skill can be passed on to children.", "Thinking brothers and sisters are identical.", "Thinking variation means a different species."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Offspring and inheritance", B1 + [(g_off, 4), (g_inh, 8)]),
        ("Inherited or not?", [(g_inh, 9), (g_pick, 7), (g_breed, 4)]),
        ("Variation in data", [(g_hand, 20)]),
        ("Selective breeding", [(g_breed, 2), (g_hand, 12), (g_pick, 6)]),
        ("Thinking scientifically", B5 + [(g_hand, 14), (g_pick, 1)]),
    ])
    make_uk(6, "inheritance-and-variation", 8, "Evolution and inheritance",
            "Recognise that living things produce offspring of the same kind, but normally offspring vary and are not identical to their parents.",
            "Inheritance and Variation",
            "Year 6 Science: Inheritance and Variation Worksheets (Offspring, Genes, Selective Breeding)",
            "Inheritance and Variation",
            "Free Year 6 science worksheets on inheritance and variation: offspring, inherited and environmental characteristics, variation data, selective breeding and Gregor Mendel. 100 questions with answers.",
            "Like their parents, but never identical.",
            "Genes pass on characteristics; the environment changes others.",
            body(),
            [("What is inheritance?", "Passing characteristics, such as eye colour, from parents to offspring through genes."),
             ("Why are offspring not identical to their parents?", "Each offspring gets a different mix of genes from its two parents, so there is variation even within one family."),
             ("What is selective breeding?", "Choosing parents with a wanted characteristic, such as high milk yield, and breeding them over many generations so the characteristic becomes more common.")],
            sets)


if __name__ == "__main__":
    main()
