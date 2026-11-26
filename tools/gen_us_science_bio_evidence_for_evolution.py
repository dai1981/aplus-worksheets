# -*- coding: utf-8 -*-
"""
US High School Biology: Evidence for Evolution (HS-LS4-1)
  python tools/gen_us_science_bio_evidence_for_evolution.py
Communicate scientific information that common ancestry and biological evolution are supported by multiple lines of
empirical evidence.
Homologous, analogous and vestigial structures; transitional fossils and rock layers; embryology; shared derived
traits; DNA and amino acid sequence comparisons.
Wrong answers come from real mistakes: "similar function means close relatives" (analogous), "humans evolved from
chimpanzees", "more differences means more closely related".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(90115)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


KINDS = ["homologous structures", "analogous structures", "vestigial structures", "transitional fossils"]
STRUCT = [("a human arm and a whale flipper", 0), ("a bat wing and a cat's front leg", 0), ("a bird wing and a human arm", 0),
          ("a frog's front leg and a lizard's front leg", 0), ("a dolphin flipper and a dog's front leg", 0), ("a horse's front leg and a bat wing", 0),
          ("a bird wing and a butterfly wing", 1), ("a shark fin and a dolphin flipper", 1), ("an octopus eye and a human eye", 1),
          ("a bat wing and a bee wing", 1), ("a penguin flipper and a fish fin", 1),
          ("tiny hip bones inside a whale", 2), ("the human tailbone", 2), ("the small eyes of a blind cave fish", 2),
          ("tiny leg bones inside a python", 2), ("the very small wings of a flightless kiwi", 2)]


def g_struct():
    s, k = R.choice(STRUCT)
    t = R.random() < 0.75
    if not once(("st", s, t)):
        return None
    if t:
        return item("What kind of structures are these: %s?" % s, KINDS[k], [x for x in KINDS if x != KINDS[k]],
                    ["Same bones in a different job: common ancestor.", "Same job, different build: no close common ancestor.", "Reduced and little or no use now."][k])
    if k == 0:
        return item("Scientists compare %s. They have the same bones in the same order. What does this suggest?" % s,
                    "The two species share a common ancestor.", ["The two species do the same job, so they are closely related.", "One species evolved from the other alive today.", "The bones formed by chance."],
                    "Homologous structures point to common ancestry.")
    if k == 1:
        return item("Scientists compare %s. They do the same job but are built very differently. What does this suggest?" % s,
                    "They evolved separately in similar environments.", ["The two species share a recent common ancestor.", "They are homologous structures.", "They are vestigial."],
                    "Analogous structures come from similar needs, not shared ancestry.")
    return item("Why do scientists count %s as evidence for evolution?" % s, "Such reduced parts are leftovers of structures that were useful in ancestors.",
                ["Such parts are new and will be used later.", "Such parts do the same job as in all relatives.", "Such parts prove the species never changed."], "Vestigial structures.")


TRANS = [("Tiktaalik", "fins with wrist-like bones, a neck and lungs", "fish to four-legged land animals"),
         ("Archaeopteryx", "feathers and wings, but also teeth, claws and a bony tail", "dinosaurs to birds"),
         ("Pakicetus and Ambulocetus", "land-mammal legs with ear bones like a whale's", "land mammals to whales"),
         ("early horse fossils such as Eohippus", "small bodies with several toes", "small forest animals to modern one-toed horses")]


def g_trans():
    n, f, t = R.choice(TRANS)
    k = R.random() < 0.5
    if not once(("tr", n, k)):
        return None
    if k:
        return item("Fossils of %s show %s. They are evidence of which change?" % (n, f), "from " + t, R.sample(["from " + x[2] for x in TRANS if x[2] != t], 3), "A transitional fossil mixes old and new traits.")
    return item("Which fossil shows the change from %s?" % t, n, R.sample([x[0] for x in TRANS if x[0] != n], 3), "It has traits of both groups.")


FOSS = ["trilobite", "sea lily", "armored fish", "tree fern", "ammonite", "dinosaur", "flowering plant", "early horse", "mammoth"]  # oldest -> youngest


def g_layer():
    who = P.next()[0]
    f = sorted(R.sample(FOSS, 4), key=FOSS.index, reverse=True)
    k = R.choice(["old", "young", "below", "order"])
    if not once(("ly", tuple(f), k)):
        return None
    rows = [["Layer %d (%s)" % (i + 1, ["top", "second", "third", "bottom"][i]), f[i]] for i in range(4)]
    tab = table(["Rock layer", "Fossil found"], rows)
    if k == "old":
        return item(tab + "%s studied undisturbed rock layers. Which fossil is the oldest?" % who, f[3], [f[0], f[1], f[2]], "Lower layers are older (superposition).")
    if k == "young":
        return item(tab + "In %s's undisturbed rock layers, which fossil is the youngest?" % who, f[0], [f[3], f[2], f[1]], "The top layer formed last.")
    if k == "below":
        i = R.randint(0, 2)
        return item(tab + "In %s's layers, which statement is true?" % who, "The %s is older than the %s." % (f[i + 1], f[i]),
                    ["The %s is older than the %s." % (f[i], f[i + 1]), "They are exactly the same age.", "Fossils in higher layers are always older."], "Deeper means older.")
    return item(tab + "From %s's layers, which list goes from oldest to youngest?" % who, ", ".join(f[::-1]),
                [", ".join(f), ", ".join([f[1], f[0], f[3], f[2]]), ", ".join([f[2], f[3], f[0], f[1]])], "Read from the bottom up.")


SPN = ["species A", "species B", "species C", "species D", "species E"]
PROT = ["cytochrome c", "hemoglobin", "a digestive enzyme", "a growth protein"]


TIER = [(["chimpanzee", "gorilla"], 0, 2), (["rhesus monkey"], 3, 5), (["dog", "horse", "rabbit"], 8, 13), (["kangaroo"], 14, 17),
        (["chicken", "snake"], 18, 23), (["frog"], 24, 28), (["tuna", "shark"], 30, 40)]


def g_seq():
    who = P.next()[0]
    pr = R.choice(PROT)
    ts = sorted(R.sample(range(len(TIER)), 4))
    names = [R.choice(TIER[t][0]) for t in ts]
    v = [R.randint(TIER[t][1], TIER[t][2]) for t in ts]
    o = list(range(4))
    R.shuffle(o)
    names, v = [names[i] for i in o], [v[i] for i in o]
    k = R.choice(["close", "far", "diff", "claim"])
    if not once(("sq", tuple(v), k)) or (k == "claim" and not once("sqc", 4)):
        return None
    tab = table(["Animal", "Amino acid differences from humans in %s" % pr], [[a, str(b)] for a, b in zip(names, v)])
    lo, hi = names[v.index(min(v))], names[v.index(max(v))]
    if k == "close":
        return item(tab + "Based on %s's data, which animal is most closely related to humans?" % who, lo, [n for n in names if n != lo], "Fewest differences = most recent common ancestor.")
    if k == "far":
        return item(tab + "Based on %s's data, which animal is least closely related to humans?" % who, hi, [n for n in names if n != hi], "Most differences = most distant relative.")
    if k == "diff":
        i, j = R.sample(range(4), 2)
        if v[i] < v[j]:
            i, j = j, i
        d = v[i] - v[j]
        return item(tab + "How many more amino acid differences does the %s have than the %s (%s's data)?" % (names[i], names[j], who), str(d), [str(v[i] + v[j]), str(v[i]), str(d + 2)],
                    "%d − %d = %d." % (v[i], v[j], d))
    return item(tab + "Which claim do %s's data support?" % who, "Humans share a more recent common ancestor with the %s than with the %s." % (lo, hi),
                ["Humans share a more recent common ancestor with the %s than with the %s." % (hi, lo), "Humans evolved from the %s alive today." % lo, "All the animals are equally related."],
                "Fewer differences mean a closer relationship.")


def mut(seq, n):
    s = list(seq)
    for i in R.sample(range(len(s)), n):
        s[i] = R.choice([b for b in "ACGT" if b != s[i]])
    return "".join(s)


def fmt(s):
    return " ".join(s[i:i + 4] for i in range(0, len(s), 4))


def g_dna():
    who = P.next()[0]
    ref = "".join(R.choice("ACGT") for _ in range(16))
    ns = R.sample(range(1, 7), 3)
    seqs = [mut(ref, n) for n in ns]
    k = R.choice(["close", "count", "far"])
    if not once(("dn", ref)):
        return None
    tab = table(["Species", "DNA sequence of one gene"], [["species X", fmt(ref)]] + [[SPN[i], fmt(s)] for i, s in enumerate(seqs)])
    if k == "count":
        i = R.randrange(3)
        return item(tab + "In %s's data, how many bases are different between species X and %s?" % (who, SPN[i]), str(ns[i]), [str(x) for x in ns if x != ns[i]] + [str(16 - ns[i])],
                    "Compare base by base.")
    i = ns.index(min(ns)) if k == "close" else ns.index(max(ns))
    word = "most" if k == "close" else "least"
    return item(tab + "In %s's data, which species is %s closely related to species X?" % (who, word), SPN[i], [SPN[j] for j in range(3) if j != i] + ["They are all equally related."],
                "It has the %s differences." % ("fewest" if k == "close" else "most"))


TRAITS = [("lamprey", []), ("trout", ["jaws"]), ("frog", ["jaws", "four legs"]), ("lizard", ["jaws", "four legs", "amniotic egg"]), ("mouse", ["jaws", "four legs", "amniotic egg", "hair"])]


def g_trait():
    k = R.choice(["close", "first", "share"])
    a = R.randint(1, 3) if k == "close" else (0 if k == "first" else R.randint(0, 3))
    if not once(("tt", k, a)):
        return None
    tr = ["jaws", "four legs", "amniotic egg", "hair"]
    rows = [[n] + ["yes" if t in ts else "no" for t in tr] for n, ts in TRAITS]
    tab = table(["Animal"] + tr, rows)
    names = [x[0] for x in TRAITS]
    if k == "close":
        b = names[a + 1]
        return item(tab + "All five animals have a backbone. Which animal is most closely related to the %s?" % names[a], b, [n for n in names if n not in (names[a], b)][:3],
                    "They share the most derived traits.")
    if k == "first":
        return item(tab + "All five animals have a backbone. Which trait evolved earliest?", "jaws", ["four legs", "amniotic egg", "hair"], "The trait shared by the most animals.")
    n = names[a + 1]
    c = len(TRAITS[a + 1][1])
    return item(tab + "How many of the four traits in the table does the %s have?" % n, str(c), [str(x) for x in range(5) if x != c][:3], "Count the yes answers.")


B1 = bank([
    ("What is a common ancestor?", "an earlier species that two or more living species evolved from", ["a species alive today that others came from", "the oldest living animal", "a fossil with no relatives"], "Branches share an ancestor."),
    ("Did humans evolve from chimpanzees?", "No. Humans and chimpanzees share a common ancestor.", ["Yes, directly.", "Yes, from gorillas.", "No, they are not related at all."], "Cousins, not parent and child."),
    ("What are homologous structures?", "body parts with similar bones because of a shared ancestor", ["parts that do the same job in unrelated species", "parts that no longer work", "parts found only in fossils"], "Arm, flipper, wing."),
    ("What are vestigial structures?", "reduced body parts with little or no use now", ["parts that do the same job", "new parts", "parts that only plants have"], "Whale hip bones."),
    ("Why are early embryos of fish, chickens and humans similar?", "They share a common ancestor and early developmental genes.", ["They will become the same animal.", "It is a coincidence.", "All embryos are fish."], "Gill slits and tails."),
    ("Which evidence uses DNA or proteins to compare species?", "molecular (biochemical) evidence", ["the fossil record", "embryology", "vestigial structures"], "Compare sequences."),
    ("What does the principle of superposition say?", "In undisturbed rock layers, lower layers are older.", ["Higher layers are older.", "All layers are the same age.", "Fossils move between layers."], "Layers pile up over time."),
    ("Why is evolution accepted by scientists?", "Many independent lines of evidence point to the same conclusions.", ["Because one fossil proves it.", "Because it was never tested.", "Because animals look alike."], "Fossils, anatomy, embryos and DNA agree."),
])
B5 = bank([
    ("Two species have similar wings but very different DNA. Which evidence is more reliable for relatedness?", "the DNA, because wings can evolve separately", ["the wings, because they look alike", "neither", "both say they are close relatives"], "Analogous traits can mislead."),
    ("A student says whales are fish because they swim. Which evidence shows whales are mammals?", "whale flipper bones and DNA match mammals", ["whales live in water", "whales have fins", "whales eat fish"], "Homologous bones and DNA."),
    ("DNA, fossils and anatomy all show birds are close to crocodiles. Why does this agreement matter?", "Independent evidence supports the same claim.", ["It shows the data are copied.", "It proves the fossils are wrong.", "It does not matter."], "Multiple lines of evidence."),
    ("Which finding would best support a common ancestor of two species?", "many shared DNA sequences and homologous bones", ["the same color", "living in the same place", "eating the same food"], "Shared inherited traits."),
    ("Why is a fossil with a mix of fish and amphibian traits important?", "It shows a transition between two groups.", ["It proves fish came from frogs.", "It shows no change happened.", "It is a fake fossil."], "Transitional forms."),
])


def body():
    think = ("<p><b>Many lines of evidence show common ancestry.</b></p>"
             "<ul><li>Anatomy: <b>homologous</b> structures (same bones, different jobs) and <b>vestigial</b> structures. Analogous structures do not show close relationship.</li>"
             "<li>Fossils: lower layers are older; transitional fossils mix traits of two groups.</li>"
             "<li>DNA and proteins: fewer differences mean a more recent common ancestor.</li></ul>")
    ex = [("Chimpanzee: 1 difference. Tuna: 21. Closer to humans?", ["Fewer differences = closer"], "chimpanzee"),
          ("Human arm and whale flipper have the same bones. What kind?", ["Same bones, different jobs"], "homologous")]
    mist = ["Thinking similar jobs (bird and insect wings) mean close relatives.", "Saying humans evolved from chimpanzees.", "Thinking more differences mean a closer relative."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Lines of evidence", B1 + [(g_struct, 8), (g_trans, 4)]),
        ("Anatomy and fossils", [(g_struct, 8), (g_trans, 2), (g_trait, 3), (g_layer, 7)]),
        ("Rock layers and shared traits", [(g_layer, 10), (g_trait, 3), (g_seq, 7)]),
        ("Molecular evidence", [(g_seq, 9), (g_dna, 11)]),
        ("Evaluating evidence", B5 + [(g_dna, 6), (g_seq, 5), (g_layer, 4)]),
    ])
    make("biology", "evidence-for-evolution", 15, "HS-LS4-1",
         "Communicate scientific information that common ancestry and biological evolution are supported by multiple lines of empirical evidence.",
         "Evidence for Evolution",
         "Evidence for Evolution Worksheets: Fossils, Anatomy and DNA (High School Biology)",
         "Evidence for Evolution",
         "Free high school biology worksheets on evidence for evolution (NGSS HS-LS4-1): homologous and vestigial structures, fossils, rock layers and DNA comparisons. 100 questions with answers.",
         "Many lines of evidence show common ancestry.",
         "Fossils, anatomy, embryos and DNA all point to the same family tree.",
         body(),
         [("What are the main lines of evidence for evolution?", "The fossil record, comparative anatomy (homologous and vestigial structures), embryology and DNA or protein sequences."),
          ("How do DNA comparisons show relationships?", "Species with fewer differences in their DNA or proteins share a more recent common ancestor."),
          ("What is the difference between homologous and analogous structures?", "Homologous structures have the same bones from a common ancestor. Analogous structures do the same job but evolved separately.")],
         sets)


if __name__ == "__main__":
    main()
