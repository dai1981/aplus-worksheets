# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Biology): The Skeleton and Muscles
  python tools/gen_uk_science_y7_skeleton_and_muscles.py
The structure and functions of the human skeleton (support, protection, movement and making blood cells); joints
(hinge, ball and socket, fixed) with cartilage, ligaments and tendons; antagonistic muscle pairs; and the interaction
between skeleton and muscles, including measuring the force exerted by different muscles.
Reuses the bone question of the Year 3 unit (new seed).
Wrong answers come from real mistakes: "muscles push bones", "ligaments join muscle to bone", "the skull has
moving joints", "bones are not living tissue".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
import gen_uk_science_y3_skeletons_and_muscles as S3
from sci_phys import uniq

S3.U = Unit(61703)
S3.R = S3.U.R
S3.P = People(S3.R)
uk_sci.USED.clear()
U, R, P = S3.U, S3.R, S3.P

JOINT = [("the elbow", "a hinge joint"), ("the knee", "a hinge joint"), ("the shoulder", "a ball and socket joint"), ("the hip", "a ball and socket joint"),
         ("the joints between the bones of the skull", "a fixed joint"), ("the finger joints", "a hinge joint")]
JDESC = {"a hinge joint": "moves backwards and forwards in one direction, like a door", "a ball and socket joint": "moves in almost every direction",
         "a fixed joint": "does not move at all"}


def g_joint():
    k = R.random() < 0.6
    if k:
        p, j = R.choice(JOINT)
        if not once(("jo", p)):
            return None
        return item("What type of joint is %s?" % p, j, [x for x in JDESC if x != j] + ["a muscle joint"], "%s %s." % (j[0].upper() + j[1:], JDESC[j]))
    j = R.choice(sorted(JDESC))
    if not once(("jd", j)):
        return None
    return item("Which type of joint %s?" % JDESC[j], j, [x for x in JDESC if x != j] + ["a cartilage joint"], "Hinge: one direction. Ball and socket: almost every direction. Fixed: no movement.")


TIS = [("cartilage", "a smooth layer on the ends of bones that stops them rubbing"), ("ligaments", "strong bands that hold bones together at a joint"),
       ("tendons", "tough cords that attach muscles to bones"), ("synovial fluid", "an oily liquid that lubricates a joint"), ("bone marrow", "soft tissue inside some bones that makes blood cells")]


def g_tis():
    t, d = R.choice(TIS)
    k = R.random() < 0.5
    if not once(("ti", t, k)):
        return None
    if k:
        return item("What is %s?" % t, d, R.sample([x[1] for x in TIS if x[1] != d], 3), "Joints need cartilage, ligaments, tendons and fluid to work smoothly.")
    return item("Which part of the body is %s?" % d, t, R.sample([x[0] for x in TIS if x[0] != t], 3), "Joints need cartilage, ligaments, tendons and fluid to work smoothly.")


PAIR = [("biceps", "triceps", "bend the arm at the elbow", "straighten the arm"), ("triceps", "biceps", "straighten the arm", "bend the arm at the elbow"),
        ("hamstrings", "quadriceps", "bend the leg at the knee", "straighten the leg"), ("quadriceps", "hamstrings", "straighten the leg", "bend the leg at the knee")]


def g_antag():
    a, b, does, other = R.choice(PAIR)
    k = R.choice(["relax", "does", "pair"])
    if not once(("an", a, k)):
        return None
    if k == "relax":
        return item("When the %s contract to %s, what do the %s do?" % (a, does, b), "They relax.", ["They contract too.", "They push the bone.", "They turn into tendons."],
                    "Antagonistic muscles work in pairs: when one contracts, the other relaxes.")
    if k == "does":
        return item("What happens when the %s contract?" % a, "They %s." % does, ["They %s." % other, "They push the bone away.", "Nothing; muscles cannot move bones."],
                    "A contracting muscle pulls on a bone.")
    return item("Which muscle works as an antagonistic pair with the %s?" % a, "the " + b, ["the " + x for x in ["biceps", "triceps", "hamstrings", "quadriceps"] if x not in (a, b)] + ["the heart"],
                "Biceps–triceps and hamstrings–quadriceps are antagonistic pairs.")


def g_force():
    who = P.next()[0]
    mus = ["finger muscles (grip)", "biceps", "leg muscles (quadriceps)", "back muscles"]
    v = [R.choice([150, 200, 250, 300]), R.choice([80, 100, 120]), R.choice([400, 450, 500, 600]), R.choice([350, 380, 420])]
    k = R.choice(["most", "least", "read", "diff"])
    ri = R.randrange(4)
    if not once(("fo", tuple(v), k, ri if k == "read" else 0)):
        return None
    tab = table(["Muscles tested", "Force measured (N)"], [[m, str(x)] for m, x in zip(mus, v)])
    intro = tab + "%s used newton meters to compare the forces made by different muscles. " % who
    if k == "most":
        a = mus[v.index(max(v))]
        return item(intro + "Which muscles produced the biggest force?", "the " + a, ["the " + x for x in mus if x != a], "The biggest number of newtons.")
    if k == "least":
        a = mus[v.index(min(v))]
        return item(intro + "Which muscles produced the smallest force?", "the " + a, ["the " + x for x in mus if x != a], "The smallest number of newtons.")
    if k == "read":
        g = "%d N" % v[ri]
        return item(intro + "What force did the %s produce?" % mus[ri], g, uniq(g, ["%d N" % x for x in v]), "Read the row.")
    d = max(v) - min(v)
    g = "%d N" % d
    return item(intro + "How much bigger was the largest force than the smallest?", g, uniq(g, ["%d N" % max(v), "%d N" % min(v), "%d N" % (max(v) + min(v)), "%d N" % (d + 50)]),
                "%d − %d = %d N." % (max(v), min(v), d))


B1 = bank([
    ("What are the four main functions of the skeleton?", "support, protection, movement and making blood cells", ["digestion, breathing, seeing and hearing", "only movement", "storing food and water"], "Bone marrow makes blood cells."),
    ("Where are red and white blood cells made?", "in the bone marrow", ["in the heart", "in the stomach", "in the skin"], "Inside some bones."),
    ("Which bones protect the brain?", "the skull", ["the ribs", "the pelvis", "the femur"], "A bony case."),
    ("Which bones protect the heart and lungs?", "the ribs", ["the skull", "the femur", "the kneecap"], "A rib cage."),
    ("What is the longest bone in the body?", "the femur (thigh bone)", ["the humerus", "the spine", "the skull"], "In the upper leg."),
    ("Why are muscles found in antagonistic pairs?", "Muscles can only pull, so a pair is needed to move a bone both ways.", ["Muscles can only push.", "One is a spare.", "They take turns to rest."], "Pull and pull back."),
    ("What do tendons join?", "muscles to bones", ["bones to bones", "skin to muscles", "nerves to bones"], "Ligaments join bone to bone."),
    ("What do ligaments join?", "bones to bones", ["muscles to bones", "skin to bone", "blood to bone"], "They hold joints together."),
])
B5 = bank([
    ("Why can old age or sport injuries make joints painful?", "Cartilage can wear away so bones rub together.", ["Ligaments grow too long.", "Bones become muscles.", "Joints fill with air."], "Worn cartilage."),
    ("How could you measure the force of different muscles fairly?", "Use the same newton meter and the same method for each muscle, and repeat.", ["Use a different newton meter each time.", "Test only once.", "Guess the force."], "Fair test."),
    ("Why does exercise help keep bones and muscles healthy?", "It makes muscles stronger and bones denser.", ["It weakens bones.", "It stops blood cells being made.", "It makes joints fixed."], "Use them or lose them."),
    ("A footballer tears a ligament in the knee. Why is the knee unstable?", "Ligaments hold the bones of the joint together.", ["Ligaments make blood cells.", "Ligaments attach muscles to bone.", "The knee has no bones."], "Function of ligaments."),
    ("Why is the spine made of many small bones (vertebrae)?", "so the back can bend while still protecting the spinal cord", ["so it can be fixed", "to make blood only", "so it is lighter than air"], "Flexible protection."),
])


def body():
    think = ("<p><b>The skeleton supports, protects, helps us move and makes blood cells.</b></p>"
             "<ul><li>Joints let bones move: hinge joints (elbow, knee), ball and socket joints (hip, shoulder), fixed joints (skull).</li>"
             "<li>Cartilage cushions, ligaments join bone to bone, tendons join muscle to bone.</li>"
             "<li>Antagonistic muscles work in pairs: when one contracts, the other relaxes.</li></ul>")
    ex = [("Shoulder joint type?", ["Moves in almost every direction"], "ball and socket"),
          ("Biceps contract. Triceps?", ["Antagonistic pair"], "relax")]
    mist = ["Thinking muscles push bones.", "Thinking ligaments join muscle to bone.", "Thinking bones are not living tissue."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Functions of the skeleton", B1 + [(S3.g_bone, 12)]),
        ("Joints", [(g_joint, 8), (g_tis, 9), (S3.g_bone, 3)]),
        ("Antagonistic muscles", [(g_antag, 11), (S3.g_mus, 8), (S3.g_bone, 1)]),
        ("Measuring muscle forces", [(g_force, 20)]),
        ("Thinking about movement", B5 + [(g_force, 12), (S3.g_bone, 3)]),
    ])
    make_ks3(7, "skeleton-and-muscles", 3, "Biology", "Skeletal and muscular systems",
             "The structure and functions of the human skeleton, to include support, protection, movement and making blood cells; biomechanics: the interaction between skeleton and muscles, including the measurement of force exerted by different muscles; the function of muscles and examples of antagonistic muscles.",
             "The Skeleton and Muscles",
             "Year 7 Science: Skeleton and Muscles Worksheets (Joints and Antagonistic Muscles)",
             "Skeleton and Muscles",
             "Free Year 7 science worksheets on the skeleton and muscles: functions of the skeleton, joints, cartilage, ligaments and tendons, antagonistic muscles and measuring muscle forces. 100 questions with answers.",
             "Support, protect, move, make blood cells.",
             "Antagonistic muscles work in pairs: one contracts while the other relaxes.",
             body(),
             [("What does the skeleton do?", "It supports the body, protects organs, allows movement with muscles, and makes blood cells in the bone marrow."),
              ("What are antagonistic muscles?", "Pairs of muscles that move a bone in opposite directions, such as the biceps and triceps. When one contracts, the other relaxes."),
              ("What is the difference between a ligament and a tendon?", "Ligaments join bone to bone at a joint. Tendons join muscle to bone.")],
             sets)


if __name__ == "__main__":
    main()
