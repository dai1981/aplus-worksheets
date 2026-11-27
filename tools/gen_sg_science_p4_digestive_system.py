# -*- coding: utf-8 -*-
"""
Singapore Primary 4 science: Digestive system (Systems)
  python tools/gen_sg_science_p4_digestive_system.py
Food passes through the mouth, gullet, stomach, small intestine and large intestine; undigested food leaves through the anus.
Digestion (breaking food into simpler substances) happens in the mouth, stomach and small intestine with digestive juices;
digested food is absorbed into the blood in the small intestine; water is absorbed in the large intestine.
The gullet and large intestine do not digest food. UK Year 4 and Year 6 questions are reused with Singapore terms (gullet).
Wrong answers come from real mistakes: "digestion starts in the stomach", "food is absorbed in the stomach",
"the large intestine digests food", "the gullet makes digestive juices".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63402)
R = U.R
P = People(R)
REP = [(r"\boesophagus\b", "gullet"), (r"\bOesophagus\b", "Gullet")]
DROP = ["rectum", "villi", "kidney", "liver", "pancreas", "enzyme", "urine", "acid", "orange juice", "windpipe"]
DG = use(U, "gen_uk_science_y4_the_digestive_system", rep=REP, drop=DROP)
TN = use(U, "gen_uk_science_y6_transporting_nutrients_and_water", rep=REP, drop=DROP + ["blood vessel", "heart", "teeth", "molar", "incisor"])

ORG = ["mouth", "gullet", "stomach", "small intestine", "large intestine", "anus"]
DIGESTS = {"mouth": True, "gullet": False, "stomach": True, "small intestine": True, "large intestine": False}
FUNC = {"mouth": ["Teeth chew food into smaller pieces and saliva makes it soft.", "Digestion starts here."],
        "gullet": ["It carries food from the mouth to the stomach.", "It squeezes food down; no digestion takes place here."],
        "stomach": ["It churns food and mixes it with digestive juices.", "Food stays here for a few hours and is partly digested."],
        "small intestine": ["Digestion is completed here.", "Digested food is absorbed into the blood here."],
        "large intestine": ["Water is absorbed from the undigested food here.", "Undigested food is stored here until it leaves the body."]}


def g_next():
    i = R.randrange(len(ORG) - 1)
    k = R.choice(["after", "before"])
    if not once(("nx", i, k)):
        return None
    if k == "after":
        a, s0 = ORG[i + 1], ORG[i]
        q = "Food leaves the %s. Where does it go next?" % s0
    else:
        a, s0 = ORG[i], ORG[i + 1]
        q = "Food reaches the %s. Where has it just come from?" % s0
    w = [x for x in ORG if x not in (a, s0)]
    return item(q, "the " + a, ["the " + x for x in R.sample(w, 3)], "mouth → gullet → stomach → small intestine → large intestine → anus.")


def g_func():
    o = R.choice(list(FUNC))
    f = R.choice(FUNC[o])
    if not once(("fn", f)):
        return None
    w = [x for x in FUNC if x != o]
    return item("In which part of the digestive system does this happen?<br><i>%s</i>" % f, "the " + o, ["the " + x for x in R.sample(w, 3)], f)


def g_digest():
    o = R.choice(list(DIGESTS))
    if not once(("dg", o)):
        return None
    if DIGESTS[o]:
        return item("Does digestion take place in the %s?" % o, "Yes. Food is broken down here with the help of digestive juices.",
                    ["No. Food only passes through.", "No. Only water is absorbed here.", "Only when we are asleep."],
                    "Digestion takes place in the mouth, stomach and small intestine.")
    return item("Does digestion take place in the %s?" % o, "No. %s" % ("Food only passes through to the stomach." if o == "gullet" else "Water is absorbed here, but food is not digested."),
                ["Yes, most digestion happens here.", "Yes, it makes the most digestive juices.", "Yes, digested food is absorbed here."],
                "Digestion takes place in the mouth, stomach and small intestine only.")


def g_which():
    k = R.choice(["juice", "absorb", "water", "nodig", "long", "start", "end"])
    if not once(("wh", k)):
        return None
    rows = {"juice": ("Which of these parts does NOT produce digestive juices?", "the gullet", ["the mouth", "the stomach", "the small intestine"], "The gullet only moves food to the stomach."),
            "absorb": ("Where is digested food absorbed into the blood?", "the small intestine", ["the stomach", "the gullet", "the mouth"], "The small intestine is long and has a large surface."),
            "water": ("Where is most water absorbed from undigested food?", "the large intestine", ["the gullet", "the mouth", "the stomach"], "The leftover food becomes more solid."),
            "nodig": ("In which two parts does NO digestion take place?", "the gullet and the large intestine", ["the mouth and the stomach", "the stomach and the small intestine", "the mouth and the small intestine"], "They do not produce digestive juices."),
            "long": ("Which part of the digestive system is the longest?", "the small intestine", ["the stomach", "the gullet", "the large intestine"], "The small intestine is about 6 m long in an adult."),
            "start": ("Where does digestion begin?", "the mouth", ["the stomach", "the gullet", "the small intestine"], "Teeth chew food and saliva starts to digest it."),
            "end": ("Where is digestion completed?", "the small intestine", ["the stomach", "the large intestine", "the anus"], "Food is fully digested in the small intestine.")}
    return item(*rows[k])


def g_bread():
    t = R.choice([1, 2, 3])
    k = R.choice(["sweet", "why", "var", "ctrl"])
    if not once(("br", k)):
        return None
    nm, he, his = P.next()
    q0 = "%s chewed a piece of plain bread for %d minute%s without swallowing it." % (nm, t, "" if t == 1 else "s")
    if k == "sweet":
        return item(q0 + " What did %s notice?" % he, "It began to taste slightly sweet.", ["It became saltier.", "It became harder.", "Nothing changed at all."],
                    "Saliva breaks down some of the starch in bread into sugar.")
    if k == "why":
        return item(q0 + " Why did it begin to taste sweet?", "Saliva started to digest the starch into sugar.", ["Teeth add sugar.", "The gullet makes sugar.", "The bread was already sweet."],
                    "Digestion begins in the mouth.")
    if k == "var":
        return item(q0 + " What does this show?", "Digestion begins in the mouth.", ["Digestion begins in the stomach.", "The mouth absorbs food.", "Bread cannot be digested."],
                    "The digestive juice in the mouth is saliva.")
    return item(q0 + " %s then left a piece" % he.capitalize() + " of bread in water in a dish for the same time. Why?", "to compare and see that saliva caused the change",
                ["to make the bread grow", "to dry the bread", "to add more sugar"], "The bread in water is the control.")


B1 = bank([
    ("What is digestion?", "breaking down food into simpler substances that the body can absorb", ["swallowing food", "chewing food only", "removing waste from the blood"], "Digested food is small enough to pass into the blood."),
    ("Which shows the correct path of food?", "mouth → gullet → stomach → small intestine → large intestine", ["mouth → stomach → gullet → small intestine → large intestine", "mouth → gullet → large intestine → small intestine → stomach", "mouth → small intestine → stomach → large intestine → gullet"], "Food passes through the organs in this order."),
    ("What do the teeth do in digestion?", "They cut and grind food into smaller pieces.", ["They absorb food.", "They make digestive juices.", "They store food."], "Smaller pieces are easier to digest."),
    ("What does saliva do?", "It makes food soft and starts to digest it.", ["It absorbs water.", "It carries food to the stomach.", "It removes waste."], "Saliva is the digestive juice in the mouth."),
    ("Why do we need a digestive system?", "to break down food so the body can use it for energy and growth", ["to pump blood around the body", "to take in oxygen", "to hold the body up"], "The body cannot use big pieces of food."),
    ("What leaves the body through the anus?", "undigested food", ["digested food", "blood", "saliva"], "Food that cannot be digested is removed."),
    ("What does the stomach do?", "It churns food and mixes it with digestive juices.", ["It absorbs most of the water.", "It chews food.", "It carries food to the mouth."], "The stomach has strong muscular walls."),
    ("Which part connects the mouth to the stomach?", "the gullet", ["the small intestine", "the large intestine", "the anus"], "The gullet is a muscular tube."),
])
B2 = bank([
    ("Where does digested food go after it is absorbed in the small intestine?", "into the blood, which carries it to all parts of the body", ["into the large intestine", "into the stomach", "out of the body"], "The blood carries digested food to the cells."),
    ("Why is the small intestine very long?", "There is more time and surface for digested food to be absorbed.", ["So that food moves faster.", "To store undigested food.", "To make the body taller."], "A long small intestine absorbs more food."),
    ("Which statement about the gullet is correct?", "It moves food to the stomach by squeezing.", ["It digests food.", "It absorbs food.", "It makes saliva."], "No digestion takes place in the gullet."),
    ("Which statement about the large intestine is correct?", "It absorbs water from undigested food.", ["It digests most of the food.", "It produces saliva.", "It connects the mouth to the stomach."], "The large intestine does not digest food."),
    ("Why should we drink enough water and eat fibre?", "to help undigested food move through the large intestine easily", ["to stop digestion", "to make the stomach smaller", "to grow more teeth"], "Fibre and water prevent constipation."),
    ("Which organ system works with the digestive system to carry digested food around the body?", "the circulatory system", ["the skeletal system", "the muscular system only", "no other system"], "The blood carries digested food."),
    ("Which parts produce digestive juices?", "the mouth, the stomach and the small intestine", ["the gullet and the large intestine", "the anus and the gullet", "the large intestine only"], "Digestive juices break food down."),
    ("Why is food in the large intestine more solid than food in the small intestine?", "Water has been absorbed from it.", ["It has been chewed more.", "More saliva was added.", "It has been digested more."], "The large intestine absorbs water."),
])
B3 = bank([
    ("Why should we not talk or laugh while swallowing?", "Food may go down the wrong way into the windpipe instead of the gullet.", ["Food will be digested too fast.", "The stomach will stop working.", "Saliva will dry up."], "The windpipe leads to the lungs."),
    ("Ahmad ate a plate of chicken rice. Which part will his food reach last?", "the large intestine", ["the gullet", "the stomach", "the small intestine"], "It reaches the large intestine before leaving the body."),
    ("A pupil says that food is absorbed in the stomach. What is the correct idea?", "Most digested food is absorbed in the small intestine.", ["Food is absorbed in the gullet.", "Food is absorbed in the mouth.", "Food is never absorbed."], "The stomach only partly digests food."),
    ("Why is it important to chew food properly?", "Smaller pieces are easier to swallow and digest.", ["Chewing stops digestion.", "Chewing makes food heavier.", "Chewing removes all the water."], "Digestive juices work faster on small pieces."),
    ("How is the digestive system like a factory line?", "Each part does a different job in turn to break down food.", ["Every part does the same job.", "Food goes round and round in a circle.", "Only one part does all the work."], "The organs work together as a system."),
    ("Which part of the body is NOT part of the digestive system?", "the heart", ["the stomach", "the gullet", "the small intestine"], "The heart is part of the circulatory system."),
])
B5 = bank([
    ("Siti put a cracker and water in a bag and squeezed it for 5 minutes to model the stomach. What does the squeezing show?", "the stomach muscles churning the food", ["the teeth chewing", "the blood absorbing food", "the large intestine absorbing water"], "Churning mixes food with digestive juices."),
    ("In a model, mashed food was pushed through a stocking with holes into a bowl. What does the liquid passing through the stocking show?", "digested food being absorbed into the blood", ["food being chewed", "food being swallowed", "undigested food leaving the body"], "Small digested particles pass through the walls of the small intestine."),
    ("In the same model, what does the food left inside the stocking represent?", "undigested food that moves to the large intestine", ["digested food in the blood", "saliva", "food in the mouth"], "Undigested food cannot pass into the blood."),
    ("A pupil chewed bread and timed how long it took to taste sweet. Why did she use the same kind and size of bread each time?", "to make the test fair", ["to make it sweeter", "to make it digest faster", "to stop the saliva"], "Only one thing should be changed."),
    ("Ravi wants to find out if chewing longer makes bread taste sweeter. What should he change?", "the time he chews the bread", ["the type of bread", "the size of the bread", "the person chewing"], "Change one variable only."),
    ("Mei Ling's grandfather has had part of his large intestine removed. Which problem is he most likely to have?", "He cannot absorb as much water from undigested food.", ["He cannot chew food.", "He cannot swallow.", "He cannot digest food in his mouth."], "The large intestine absorbs water."),
])


def body():
    think = ("<p><b>The digestive system breaks down food into simpler substances that the body can absorb.</b></p>"
             "<p>mouth → gullet → stomach → small intestine → large intestine → anus</p>"
             "<ul><li><b>Digestion</b> happens in the mouth, stomach and small intestine, with digestive juices.</li>"
             "<li>Digested food is <b>absorbed into the blood</b> in the small intestine.</li>"
             "<li>Water is absorbed in the large intestine. Undigested food leaves through the anus.</li>"
             "<li>No digestion takes place in the gullet or the large intestine.</li></ul>")
    ex = [("Where does digestion start?", ["Teeth chew the food", "Saliva starts to digest it"], "In the mouth."),
          ("Where is digested food absorbed?", ["Digestion is completed in the small intestine", "Digested food passes into the blood there"], "In the small intestine.")]
    mist = ["Thinking digestion starts in the stomach. It starts in the mouth.",
            "Thinking food is absorbed in the stomach. It is absorbed in the small intestine.",
            "Thinking the large intestine digests food. It absorbs water.",
            "Mixing up the order: the stomach comes before the small intestine."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The path of food", B1 + [(g_next, 6), (DG.g_time, 3), (TN.g_next, 3)]),
        ("What each part does", B2 + [(g_func, 5), (g_digest, 4), (TN.g_org, 3)]),
        ("Digestion and absorption", B3 + [(g_which, 6), (g_func, 4), (g_digest, 1), (DG.B1[0], 1), (TN.g_org, 2)]),
        ("Taking care of our digestive system", DG.B5 + TN.B1 + [(g_func, 2), (g_next, 3), (g_which, 1), (DG.g_sum, 3)]),
        ("PSLE-style models and experiments", B5 + [(g_bread, 4), (DG.g_model, 4), (DG.g_sum, 3), (g_which, 2), (TN.g_org, 1)]),
    ])
    make_sg(4, "digestive-system", 2, "Systems", "Human system (Digestive system)",
            "Identify the organs of the human digestive system (mouth, gullet, stomach, small intestine, large intestine) and describe their functions. "
            "Recognise that digestion is the breakdown of food into simpler substances, which takes place in the mouth, stomach and small intestine, "
            "and that digested food is absorbed in the small intestine (summary of the MOE Primary Science Syllabus).",
            "The Digestive System",
            "Primary 4 Science: Digestive System Worksheets (with Answers)",
            "Digestive system",
            "Free Primary 4 science worksheets for Singapore pupils on the human digestive system: mouth, gullet, stomach, small and large intestines, digestion and absorption. 100 questions with answers.",
            "Food is broken down so the body can use it.",
            "Digestion: mouth, stomach, small intestine.",
            body(),
            [("Where does digestion take place?", "In the mouth, the stomach and the small intestine. No digestion takes place in the gullet or the large intestine."),
             ("Where is digested food absorbed?", "In the small intestine. The digested food passes into the blood, which carries it around the body."),
             ("What does the large intestine do?", "It absorbs water from the undigested food. The undigested food then leaves the body through the anus.")],
            sets)


if __name__ == "__main__":
    main()
