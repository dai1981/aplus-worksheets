# -*- coding: utf-8 -*-
"""
UK Year 3 science: Skeletons and Muscles (Animals, including humans)
  python tools/gen_uk_science_y3_skeletons_and_muscles.py
Humans and some other animals have skeletons and muscles for support, protection and movement: the main bones and
what they protect, joints, muscles working in pairs (biceps and triceps), skeletons inside and outside the body and
animals with no skeleton, and a simple investigation (arm span and height, or leg length and jumping).
Wrong answers come from real mistakes: "muscles push bones", "bones are not alive", "all animals have a skeleton like
ours", "the skull protects the heart".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61306)
R = U.R
P = People(R)

BONE = [("the skull", "the head", "protects the brain"), ("the ribs (rib cage)", "the chest", "protect the heart and lungs"),
        ("the spine (backbone)", "the back", "protects the spinal cord and holds the body upright"), ("the pelvis", "the hips", "supports the body and protects organs in the lower belly"),
        ("the femur (thigh bone)", "the upper leg", "is the longest bone and helps us stand and walk"), ("the humerus", "the upper arm", "lets the arm lift and move"),
        ("the kneecap", "the front of the knee", "protects the knee joint"), ("the jaw bone", "the lower face", "holds the bottom teeth and lets us chew")]


def g_bone():
    b, where, job = R.choice(BONE)
    k = R.choice(["where", "job", "name"])
    if not once(("bo", b, k)):
        return None
    if k == "where":
        return item("Where in the body is %s?" % b, "in " + where, ["in " + x[1] for x in R.sample([x for x in BONE if x[0] != b], 3)], "Learn the main bones and where they are.")
    if k == "job":
        return item("What does %s do?" % b, "It " + job + ".", ["It " + x[2] + "." for x in R.sample([x for x in BONE if x[0] != b], 3)], "Many bones protect soft organs.")
    return item("Which bone %s?" % job.replace("protects", "protects").replace("is the longest", "is the longest"), b, R.sample([x[0] for x in BONE if x[0] != b], 3), "Match the bone to its job.")


JOB = [("support", "holding the body up and giving it shape"), ("protection", "keeping soft organs such as the brain and heart safe"), ("movement", "working with muscles so we can move")]


def g_job():
    j, d = R.choice(JOB)
    ex = {"support": ["The spine keeps us upright.", "Leg bones carry our weight when we stand.", "The skeleton gives the body its shape.", "The pelvis holds up the top half of the body."],
          "protection": ["The skull surrounds the brain.", "The ribs surround the heart and lungs.", "The spine surrounds the spinal cord.", "A helmet of bone covers the brain."],
          "movement": ["Muscles pull on arm bones to bend the elbow.", "Leg bones and muscles let us run and jump.", "Finger bones and muscles let us write and grip.", "The knee joint lets the leg bend when we kick a ball."]}
    e = R.choice(ex[j])
    if not once(("jb", e)):
        return None
    return item("%s Which job of the skeleton is this?" % e, j, [x[0] for x in JOB if x[0] != j] + ["digestion"], "The skeleton supports, protects and helps us move.")


MUS = [("When you bend your arm, what does your biceps (front of the upper arm) do?", "It contracts (gets shorter) and pulls the lower arm up.", ["It pushes the arm down.", "It relaxes and gets longer.", "Nothing, bones move by themselves."]),
       ("When you straighten your arm, what does your triceps (back of the upper arm) do?", "It contracts and pulls the lower arm straight.", ["It pushes the arm up.", "It relaxes and does nothing.", "It turns into bone."]),
       ("When the biceps contracts, what does the triceps do?", "It relaxes.", ["It contracts too.", "It disappears.", "It pushes the biceps."]),
       ("Why do muscles work in pairs?", "Muscles can only pull, so one pulls a bone one way and the other pulls it back.", ["Muscles can only push.", "One muscle is a spare.", "Muscles are always both pulling at once."]),
       ("What does a muscle do when it contracts?", "It gets shorter and fatter and pulls on a bone.", ["It gets longer and pushes a bone.", "It turns hard like bone.", "It lets go of the bone."]),
       ("What joins muscles to bones?", "tendons", ["joints", "nails", "skin"]),
       ("Which organ is a muscle that never stops working?", "the heart", ["the skull", "the femur", "the kneecap"]),
       ("What happens to muscles that are exercised often?", "They get stronger.", ["They get weaker.", "They turn into bone.", "They stop working."]),
       ("Can a muscle push a bone?", "No. Muscles can only pull.", ["Yes, muscles only push.", "Yes, but only leg muscles.", "Only when they are relaxed."]),
       ("When you kick a ball, the muscle at the front of your thigh contracts. What does it do?", "It pulls the lower leg forwards to straighten the knee.", ["It pushes the foot backwards.", "It relaxes and gets longer.", "It holds the skull still."]),
       ("Why do athletes warm up before a race?", "Warm muscles stretch and contract better and are less likely to be hurt.", ["To make their bones longer.", "To make their muscles push.", "To stop their heart beating."]),
       ("Which muscles are working when you smile?", "small muscles in the face", ["the biceps", "the heart only", "the thigh muscles"])]


def g_mus():
    q, a, w = R.choice(MUS)
    if not once(("mu", q)):
        return None
    return item(q, a, w, "Muscles pull bones by contracting. They work in pairs: when one contracts, the other relaxes.")


ANI = [("a human", "an internal skeleton (endoskeleton)"), ("a dog", "an internal skeleton (endoskeleton)"), ("a fish", "an internal skeleton (endoskeleton)"),
       ("a frog", "an internal skeleton (endoskeleton)"), ("a snake", "an internal skeleton (endoskeleton)"), ("a bird", "an internal skeleton (endoskeleton)"),
       ("a crab", "an external skeleton (exoskeleton)"), ("a beetle", "an external skeleton (exoskeleton)"), ("a woodlouse", "an external skeleton (exoskeleton)"),
       ("an ant", "an external skeleton (exoskeleton)"), ("a lobster", "an external skeleton (exoskeleton)"), ("a spider", "an external skeleton (exoskeleton)"),
       ("an earthworm", "no skeleton"), ("a slug", "no skeleton"), ("a jellyfish", "no skeleton"), ("an octopus", "no skeleton")]
SK = ["an internal skeleton (endoskeleton)", "an external skeleton (exoskeleton)", "no skeleton"]


def g_ani():
    a, s = R.choice(ANI)
    if not once(("an", a)):
        return None
    return item("What kind of skeleton does %s have?" % a, s, [x for x in SK if x != s] + ["a skeleton made of wood"],
                "Vertebrates have bones inside; insects, spiders and crabs have a hard case outside; worms, slugs and jellyfish have no skeleton.")


def g_span():
    who = P.next()[0]
    names = R.sample(["Ava", "Leo", "Isla", "Noah", "Ruby", "Kai", "Maya", "Theo", "Zara", "Arjun"], 4)
    h = R.sample(range(122, 140), 4)
    s = [x + R.choice([-2, -1, 0, 1, 2]) for x in h]
    k = R.choice(["tall", "span", "pattern", "diff"])
    ri = R.randrange(4)
    if not once(("sp", tuple(h), k)) or (k == "pattern" and not once(("spp",), 3)):
        return None
    tab = table(["Pupil", "Height (cm)", "Arm span (cm)"], [[n, str(a), str(b)] for n, a, b in zip(names, h, s)])
    intro = tab + "%s's class measured their height and their arm span. " % who
    if k == "tall":
        a = names[h.index(max(h))]
        return item(intro + "Who is the tallest?", a, [x for x in names if x != a], "Find the biggest height.")
    if k == "span":
        g = "%d cm" % s[ri]
        return item(intro + "What is %s's arm span?" % names[ri], g, uniq(g, ["%d cm" % h[ri]] + ["%d cm" % x for x in s]), "Read across the row.")
    if k == "diff":
        d = max(h) - min(h)
        g = "%d cm" % d
        return item(intro + "How much taller is the tallest pupil than the shortest?", g, uniq(g, ["%d cm" % max(h), "%d cm" % min(h), "%d cm" % (d + 10), "%d cm" % (d + 2)]),
                    "%d − %d = %d cm." % (max(h), min(h), d))
    return item(intro + "What do the results suggest?", "A person's arm span is about the same as their height.", ["Arm span is always double the height.", "Taller people have shorter arm spans.", "Arm span and height are not linked."],
                "The two numbers are close for each pupil.")


B1 = bank([
    ("What is a skeleton?", "the frame of bones inside the body", ["the muscles in the arm", "the skin on the outside", "the food we eat"], "Humans have about 206 bones."),
    ("About how many bones does an adult human have?", "about 206", ["about 20", "about 2,000", "exactly 12"], "Babies have more, which join as they grow."),
    ("What are the three main jobs of the skeleton?", "support, protection and movement", ["eating, sleeping and talking", "seeing, hearing and smelling", "breathing only"], "Remember: support, protect, move."),
    ("What is a joint?", "a place where two bones meet so the body can bend", ["a kind of muscle", "the middle of a bone", "a kind of skin"], "Knees, elbows and shoulders."),
    ("Which bone protects the brain?", "the skull", ["the ribs", "the femur", "the kneecap"], "A hard helmet of bone."),
    ("What do muscles do?", "pull on bones to make them move", ["make blood", "protect the brain", "hold food"], "They contract."),
    ("Are bones alive?", "Yes. They grow and can mend when broken.", ["No, they are like stone.", "Only in babies.", "Only the skull is alive."], "Living tissue."),
    ("Which food and drink help to keep bones strong?", "milk, cheese and yoghurt", ["sweets and fizzy drinks", "crisps", "chips"], "They contain calcium."),
])
B5 = bank([
    ("Why is the skull one hard piece but the spine is made of many small bones?", "The skull protects the brain; the spine must bend as we move.", ["The spine is not important.", "The skull needs to bend.", "Both are just one bone."], "Shape fits the job."),
    ("A beetle's exoskeleton does not grow. How does a growing insect manage?", "It sheds (moults) its old exoskeleton and grows a new, bigger one.", ["It stops growing.", "It grows bones inside.", "It borrows another shell."], "Moulting."),
    ("How does a jellyfish keep its shape without a skeleton?", "The water around it supports its body.", ["It has bones inside.", "It has a shell.", "It never has a shape."], "Water supports it."),
    ("Why do doctors put a broken arm in a cast?", "to keep the bone still so it can mend", ["to make the arm bend more", "to make the muscles weaker", "to stop the bone being alive"], "Bones heal."),
    ("A pupil asks: do people with longer legs jump further? How could they test it fairly?", "Measure each person's leg length and jump using the same kind of jump and the same start line.", ["Let everyone jump however they like.", "Measure only one person.", "Measure arm length instead."], "Fair test."),
])


def body():
    think = ("<p><b>A skeleton supports the body, protects organs and helps it move.</b></p>"
             "<ul><li>The skull protects the brain; the ribs protect the heart and lungs; the spine holds us upright.</li>"
             "<li>Muscles pull on bones by contracting. They work in pairs, like the biceps and triceps.</li>"
             "<li>Some animals have a skeleton inside, some have a hard skeleton outside, and some have none.</li></ul>")
    ex = [("Which bone protects the brain?", ["Head"], "the skull"),
          ("Bending the arm: which muscle contracts?", ["Front of the upper arm"], "the biceps")]
    mist = ["Thinking muscles push bones.", "Thinking bones are not alive.", "Thinking all animals have a skeleton like ours."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The skeleton", B1 + [(g_bone, 7), (g_job, 5)]),
        ("Bones and their jobs", [(g_bone, 11), (g_job, 3), (g_mus, 6)]),
        ("Muscles", [(g_mus, 3), (g_bone, 3), (g_ani, 8), (g_span, 6)]),
        ("Skeletons of animals", [(g_ani, 7), (g_span, 9), (g_job, 4)]),
        ("Thinking about bodies", B5 + [(g_span, 10), (g_bone, 2), (g_mus, 3)]),
    ])
    make_uk(3, "skeletons-and-muscles", 6, "Animals, including humans",
            "Identify that humans and some other animals have skeletons and muscles for support, protection and movement.",
            "Skeletons and Muscles",
            "Year 3 Science: Skeletons and Muscles Worksheets (Bones, Joints and Muscles)",
            "Skeletons and Muscles",
            "Free Year 3 science worksheets on skeletons and muscles: the main bones, support, protection and movement, muscles working in pairs, and animal skeletons. 100 questions with answers.",
            "Support, protect, move.",
            "Muscles pull on bones; they work in pairs.",
            body(),
            [("What does the skeleton do?", "It supports the body and gives it shape, protects soft organs such as the brain, heart and lungs, and works with muscles so we can move."),
             ("How do muscles move bones?", "A muscle contracts (gets shorter) and pulls on a bone. Muscles work in pairs: when the biceps pulls the arm up, the triceps relaxes, and the triceps pulls it straight again."),
             ("Do all animals have a skeleton?", "No. Vertebrates such as humans, fish and birds have bones inside. Insects, spiders and crabs have a hard outer skeleton. Worms, slugs and jellyfish have no skeleton.")],
            sets)


if __name__ == "__main__":
    main()
