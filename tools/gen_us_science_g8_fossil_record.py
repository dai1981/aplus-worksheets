# -*- coding: utf-8 -*-
"""
US Grade 8 Science: The Fossil Record (MS-LS4-1, MS-LS4-2)
  python tools/gen_us_science_g8_fossil_record.py
Analyze and interpret data for patterns in the fossil record that document the existence, diversity, extinction, and
change of life forms throughout the history of life on Earth, under the assumption that natural laws operate today as
in the past; apply scientific ideas to construct an explanation for the anatomical similarities and differences among
modern organisms and between modern and fossil organisms to infer evolutionary relationships.
Superposition (lower layers are older), fossil ranges, extinction, simple to complex, transitional fossils,
homologous structures (same bones, different jobs) vs. analogous structures.
Wrong answers come from real mistakes: "top layers are oldest", "homologous structures must do the same job",
"humans and dinosaurs lived at the same time", "the fossil record is complete".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, People
from gen_us_science_g4_rock_layers_and_fossils import layers

U = Unit(80114)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


KINDS = ["seashell", "fish", "fern", "dinosaur footprint", "coral", "shark tooth", "clam", "tree leaf"]


def g_layers():
    n = R.choice([4, 5])
    fos = R.sample(KINDS, n)
    if R.random() < 0.3:
        fos[R.randrange(n)] = None
    who = P.next()[0]
    k = R.choice(["oldest", "youngest", "order"])
    letters = "ABCDEF"[:n]           # top to bottom
    have = [i for i in range(n) if fos[i]]
    if len(have) < 3:
        return None
    if not once((tuple(fos), k)):
        return None
    svg = layers(fos, "rock layers with fossils, labeled A to %s from top to bottom" % letters[-1])
    name = lambda i: fos[i]
    if k == "oldest":
        a = name(min(have))
        if len(have) < 4:
            return None
        return item(fig(svg) + "%s studies these undisturbed rock layers. Which fossil is the oldest?" % who, "the " + a, ["the " + name(i) for i in R.sample([j for j in have if j != min(have)], 3)],
                    "In undisturbed layers, the lowest layer formed first, so its fossils are oldest.")
    if k == "youngest":
        a = name(max(have))
        if len(have) < 4:
            return None
        return item(fig(svg) + "%s studies these undisturbed rock layers. Which fossil is the youngest?" % who, "the " + a, ["the " + name(i) for i in R.sample([j for j in have if j != max(have)], 3)],
                    "The top layers formed last, so they are the youngest.")
    i, j = sorted(R.sample(have, 2))
    x, y, a, b = (j, i, "younger", "older") if R.random() < 0.5 else (i, j, "older", "younger")
    return item(fig(svg) + "In %s's rock layers, how does the %s compare in age with the %s?" % (who, name(x), name(y)), "The %s is %s." % (name(x), a),
                ["The %s is %s." % (name(x), b), "They are the same age.", "You cannot compare them."], "Layer %s is above layer %s, so it formed later." % (letters[n - 1 - j], letters[n - 1 - i]))


# approximate ranges in millions of years ago (first appearance, last appearance; 0 = still living)
RANGE = [("trilobites", 521, 252), ("dinosaurs (non-bird)", 233, 66), ("ammonites", 400, 66), ("sharks", 450, 0), ("flowering plants", 130, 0),
         ("mammoths", 5, 0.004), ("humans (Homo sapiens)", 0.3, 0), ("horseshoe crabs", 445, 0), ("pterosaurs", 228, 66), ("ferns", 360, 0)]


def fmt(x):
    if x == 0:
        return "still living"
    return ("%g" % x) + " million years ago" if x >= 1 else "about %s years ago" % "{:,}".format(int(x * 1_000_000))


def g_range():
    who = P.next()[0]
    rows = R.sample(RANGE, 4)
    tab = table(["Group", "First fossils", "Last fossils"], [[g, fmt(a), fmt(b)] for g, a, b in rows])
    k = R.choice(["extinct", "first", "overlap"])
    if not once((tuple(r[0] for r in rows), k)):
        return None
    if k == "extinct":
        ext = [r for r in rows if r[2] > 0]
        liv = [r for r in rows if r[2] == 0]
        if len(ext) == 1:
            a = ext[0][0]
            return item(tab + "Which group in %s's table is extinct?" % who, a, [r[0] for r in liv], "Its fossils stop appearing, and it is not alive today.")
        if len(liv) == 1:
            a = liv[0][0]
            return item(tab + "Which group in %s's table is still alive today?" % who, a, [r[0] for r in ext], "Its fossil record continues to the present.")
        return None
    if k == "first":
        a = max(rows, key=lambda r: r[1])[0]
        return item(tab + "Which group in %s's table appeared first in the fossil record?" % who, a, [r[0] for r in rows if r[0] != a], "The largest number of millions of years ago is the earliest.")
    pairs = [(x, y) for x in rows for y in rows if x[0] < y[0]]
    x, y = R.choice(pairs)
    both = max(x[2], y[2]) < min(x[1], y[1])
    a = "Yes, their time ranges overlap." if both else "No, their time ranges do not overlap."
    return item(tab + "Using %s's table, could %s and %s have lived at the same time?" % (who, x[0], y[0]), a,
                ["No, their time ranges do not overlap." if both else "Yes, their time ranges overlap.", "Only if they lived in the same place today.", "The table cannot show this."],
                "Compare the ranges: %s to %s and %s to %s." % (fmt(x[1]), fmt(x[2]), fmt(y[1]), fmt(y[2])))


HOMO = [("a human arm", "a bat wing", "homologous", "same bones (upper arm, forearm, wrist, fingers) used for different jobs"),
        ("a whale flipper", "a cat's front leg", "homologous", "same bones used for swimming and walking"),
        ("a bird wing", "a butterfly wing", "analogous", "same job (flying) but very different structures"),
        ("a horse's leg", "a human arm", "homologous", "same basic bone pattern adapted for running and grasping"),
        ("a shark fin", "a dolphin flipper", "analogous", "same job (swimming) but a fish and a mammal with different structures"),
        ("a penguin flipper", "a crocodile's front leg", "homologous", "same bone pattern from a shared ancestor"),
        ("an insect wing", "a bat wing", "analogous", "both fly, but an insect wing has no bones"),
        ("a mole's digging claw", "a human hand", "homologous", "the same bones adapted for digging or grasping")]


def g_homo():
    a, b, k, why = R.choice(HOMO)
    who = P.next()[0]
    t = R.random() < 0.5
    if not once((a, t)):
        return None
    if t:
        return item("%s compares %s and %s. What kind of structures are they?" % (who, a, b), k + " structures", ["analogous structures" if k == "homologous" else "homologous structures", "identical structures", "fossils"],
                    "They have the %s." % why if k == "homologous" else "They have the %s." % why)
    if k == "homologous":
        return item("%s compares %s and %s. What does their similar bone pattern suggest?" % (who, a, b), "The organisms share a common ancestor.", ["They do exactly the same job.", "They are the same species.", "They are not related at all."],
                    "Homologous structures are evidence of common ancestry.")
    return item("%s compares %s and %s. They do the same job. Does this show a close evolutionary relationship?" % (who, a, b), "No. They look different inside and evolved separately for the same job.",
                ["Yes, any similar job proves close relation.", "Yes, they are the same species.", "No, because neither has a function."], "Analogous structures do not show close ancestry.")


B1 = bank([
    ("What is the law of superposition?", "In undisturbed rock layers, the lowest layers are the oldest.", ["The top layers are the oldest.", "All layers are the same age.", "Layers form from the bottom up only in deserts."],
     "Newer sediment settles on top."),
    ("What is the fossil record?", "all the fossils found and the order in which they appear in rock layers", ["a list of living animals", "a music recording", "a map of volcanoes"], "It shows life's history."),
    ("What pattern does the fossil record show over time?", "Life has generally changed from simpler to more complex and diverse forms.", ["Life has never changed.", "All life appeared at once.", "Living things became fewer and simpler."],
     "The oldest fossils are single-celled."),
    ("What does it mean when a fossil group stops appearing in younger layers?", "The group likely went extinct.", ["It became invisible.", "It moved to the Moon.", "It became a rock."], "Extinction shows in the record."),
    ("Did humans and non-bird dinosaurs live at the same time?", "No. Non-bird dinosaurs died out about 66 million years before modern humans appeared.", ["Yes, often.", "Only in North America.", "Yes, humans hunted them."],
     "Their ranges do not overlap."),
    ("What are homologous structures?", "body parts with similar bones in different organisms, inherited from a common ancestor", ["parts that do the same job but have different structures", "parts made of metal", "parts that are always identical"],
     "Same structure, different uses."),
    ("What is a transitional fossil?", "a fossil with features of an older group and a newer group", ["a fossil of a living animal", "a fake fossil", "a fossil found on the surface only"], "For example, Archaeopteryx (dinosaur and bird features)."),
    ("Why is the fossil record incomplete?", "Most organisms decay before they can fossilize, and many fossils are destroyed or not found.", ["Scientists hide fossils.", "Only plants fossilize.", "It is complete."],
     "Fossils form only in special conditions."),
])
B5 = bank([
    ("Ava finds a fossil with feathers, teeth and a long bony tail. What could it show?", "a link between dinosaurs and birds", ["a modern bird", "a fish", "a mammal"], "Archaeopteryx is a transitional fossil."),
    ("Leo sees fossil whale ancestors with small hind legs. What does this suggest?", "Whales descended from land mammals with legs.", ["Whales always lived in the ocean.", "Whales walked on land last year.", "Legs are not related to whales."],
     "Transitional fossils show change over time."),
    ("Mia notices that the oldest layers have only simple sea life, and younger layers have land plants and animals. What pattern is this?", "Life became more diverse over time.", ["Life got simpler.", "Nothing changed.", "Layers were mixed."],
     "The fossil record shows change."),
    ("Why do scientists assume natural laws worked the same in the past as today?", "It lets them use present processes, like sediment settling, to explain past rock layers.", ["It is just a guess with no use.", "Laws change every year.", "They do not assume this."],
     "Uniformitarianism."),
    ("A fossil fish found high in a mountain rock layer suggests:", "the rock formed underwater and was later lifted up", ["fish climbed mountains", "the fossil fell from the sky", "fish lived on mountains"], "Rocks move over time."),
])


def body():
    think = ("<p>The <b>fossil record</b> shows the history of life. In undisturbed rock, <b>lower layers are older</b> (superposition), so fossils show <b>which organisms lived when</b>.</p>"
             "<ul><li>Patterns: life became <b>more diverse and complex</b>; many groups appeared and then went <b>extinct</b>.</li>"
             "<li><b>Transitional fossils</b> (like Archaeopteryx or walking whale ancestors) show features of older and newer groups.</li>"
             "<li><b>Homologous structures</b> (human arm, bat wing, whale flipper) have the same bones used for different jobs. They show a <b>common ancestor</b>. "
             "<b>Analogous structures</b> (bird and insect wings) do the same job but are built differently.</li></ul>")
    ex = [("A fern fossil is in the bottom layer, a shell in the top. Which is older?", ["Lower = older."], "the fern"),
          ("Human arm and bat wing: same bones. What does this suggest?", ["Homologous structures."], "a common ancestor")]
    mist = ["Thinking the top layers are the oldest.",
            "Thinking homologous structures must do the same job.",
            "Thinking humans lived with non-bird dinosaurs."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Reading the fossil record", B1 + [(g_layers, 12)]),
        ("Rock layers and age", [(g_layers, 14), (g_range, 6)]),
        ("Appearance and extinction", [(g_range, 16), (g_layers, 4)]),
        ("Comparing anatomy", [(g_homo, 14), (g_range, 6)]),
        ("Inferring relationships", B5 + [g_homo, g_range, g_layers]),
    ])
    make("grade-8", "fossil-record", 14, "MS-LS4-1",
         "Analyze and interpret data for patterns in the fossil record that document the existence, diversity, extinction, and change of life forms throughout the history of life on Earth under the assumption that natural laws operate today as in the past.",
         "The Fossil Record",
         "Grade 8 Fossil Record Worksheets: Rock Layers, Extinction and Homologous Structures",
         "Fossil Record",
         "Free middle school science worksheets on the fossil record (NGSS MS-LS4-1, MS-LS4-2): superposition, fossil time ranges, extinction, transitional fossils, and homologous vs. analogous structures. 100 practice questions with answers.",
         "Lower layers are older; fossils show change over time.",
         "The fossil record shows life becoming more diverse, with many groups going extinct. Shared bone patterns point to common ancestors.",
         body(),
         [("How do scientists know which fossils are older?", "In undisturbed rock layers, lower layers formed first, so the fossils in them are older (the law of superposition)."),
          ("What patterns does the fossil record show?", "Life has changed over time, generally becoming more diverse and complex, and many groups have appeared and then gone extinct."),
          ("What are homologous structures?", "Body parts in different organisms that have the same basic bones but may do different jobs, such as a human arm and a bat wing. They suggest a common ancestor.")],
         sets)


if __name__ == "__main__":
    main()
