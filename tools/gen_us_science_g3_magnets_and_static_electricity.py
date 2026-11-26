# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Magnets and Static Electricity (3-PS2-3)
  python tools/gen_us_science_g3_magnets_and_static_electricity.py
Electric and magnetic forces act between objects that are not touching. Magnets: like poles repel,
unlike poles attract; magnets attract iron and steel (and nickel) but not plastic, wood, paper, glass,
aluminum or copper; the force is stronger when objects are closer. Static electricity: a rubbed balloon
attracts hair and small bits of paper; two rubbed balloons push apart.
Assessment boundary: no more than two objects at a time; qualitative distance and orientation only.
Wrong answers come from real mistakes: "magnets attract all metals", "N attracts N",
"magnets must touch to work", "distance does not matter".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, figure, svg_wrap, rect, text, arrow, People, INK, BLUE, RED

U = Unit(30103)
R = U.R
P = People(R)


def bar(x, y, left, right, w=110, h=30):
    """A bar magnet with poles labeled left/right ('N' or 'S'). N is red, S is blue."""
    col = {"N": RED, "S": BLUE}
    return (rect(x, y, w / 2, h, col[left], INK, 1.5) + rect(x + w / 2, y, w / 2, h, col[right], INK, 1.5)
            + text(x + w / 4, y + h / 2 + 6, left, 16, col="#fff") + text(x + 3 * w / 4, y + h / 2 + 6, right, 16, col="#fff"))


def pair(a, b, gap=40, label="two bar magnets"):
    W = 110 * 2 + gap + 20
    return svg_wrap(W, 50, bar(10, 10, *a) + bar(10 + 110 + gap, 10, *b), label)


def g_poles():
    a = R.choice([("N", "S"), ("S", "N")])
    b = R.choice([("N", "S"), ("S", "N")])
    facing = (a[1], b[0])
    att = facing[0] != facing[1]
    k = R.choice(["what", "why"])
    pic = fig(pair(a, b, label="two bar magnets with %s facing %s" % facing))
    p = P.next()
    if k == "what":
        return item(pic + p[0] + " puts two magnets on a table. The magnets are placed with the %s pole facing the %s pole. What will happen?" % facing,
                    "They will pull together (attract)." if att else "They will push apart (repel).",
                    ["They will push apart (repel)." if att else "They will pull together (attract).", "Nothing will happen.", "They will both spin in circles."],
                    ("Unlike poles (N and S) attract." if att else "Like poles (%s and %s) repel." % facing))
    return item(pic + "%s's magnets %s. Why?" % (p[0], "pull together" if att else "push apart"),
                "%s poles are facing each other." % ("Unlike" if att else "Like"), ["%s poles are facing each other." % ("Like" if att else "Unlike"), "Magnets only work when touching.", "The magnets are made of plastic."],
                "Like poles repel and unlike poles attract.")


MAG = ["an iron nail", "a steel paper clip", "a steel spoon", "a steel bottle cap", "iron filings", "a steel washer", "a steel pin", "a nickel ring"]
NOT = ["a plastic button", "a wooden pencil", "a rubber eraser", "an aluminum can", "a copper penny", "a glass marble", "a paper cup", "a cotton ball", "a gold ring", "a crayon"]


def g_attract():
    k = R.choice(["yes", "no"])
    where = R.choice(["a junk drawer", "a toolbox", "a pencil case", "a sewing box", "a kitchen drawer", "a craft table", "a backpack", "a desk drawer"])
    pre = "%s finds four objects in %s. " % (P.next()[0], where)
    if k == "yes":
        return item(pre + "Which object would a magnet attract?", R.choice(MAG), R.sample(NOT, 3), "Magnets attract objects that contain iron, steel or nickel.")
    return item("Which object would a magnet NOT attract?", R.choice(NOT), R.sample(MAG, 3), "Magnets do not attract plastic, wood, glass, paper, aluminum or copper.")


def g_metal():
    m = R.choice(["an aluminum can", "a copper penny", "a gold ring", "aluminum foil", "a brass key"])
    p = P.next()
    return item("%s says a magnet will pick up %s because it is metal. Is %s right?" % (p[0], m, p[1]), "No. Magnets only attract some metals, like iron and steel.",
                ["Yes. Magnets attract all metals.", "Yes, but only if it is shiny.", "No. Magnets never attract metal."], "%s is not attracted to a magnet." % (m[0].upper() + m[1:]))


def g_dist():
    ds = [1, 2, 3, 4]
    clips = sorted(R.sample(range(1, 16), 4), reverse=True)
    p = P.next()
    rows = [["%d cm" % d, "%d" % c] for d, c in zip(ds, clips)]
    tab = table(["Distance from magnet", "Paper clips pulled"], rows)
    k = R.choice(["most", "pattern", "far"])
    if k == "most":
        return item(tab + "%s held a magnet at different distances from a pile of paper clips. At which distance was the magnetic force strongest?" % p[0], "1 cm",
                    ["2 cm", "3 cm", "4 cm"], "The magnet pulled the most clips (%d) at 1 cm." % clips[0])
    if k == "pattern":
        return item(tab + "What pattern does %s's data show?" % p[0], "The closer the magnet, the stronger the force.",
                    ["The farther the magnet, the stronger the force.", "Distance does not change the force.", "The magnet only works when touching."],
                    "From 1 cm to 4 cm the number of clips went from %d to %d." % (clips[0], clips[-1]))
    return item(tab + "Using %s's data, about how many paper clips would the magnet pull at 6 cm?" % p[0], "fewer than %d" % clips[-1],
                ["more than %d" % clips[0], "exactly %d" % clips[0], "between %d and %d" % (clips[1], clips[0])], "The force gets weaker as the distance gets bigger.")


STATIC = [("rubs a balloon on %s hair and holds it near %s head", "Hair is pulled toward the balloon.", "The rubbed balloon has a static electric charge that attracts the hair."),
          ("rubs a balloon on a wool sweater and holds it near small bits of paper", "The paper bits jump up to the balloon.", "Static electricity pulls the paper without touching it."),
          ("rubs two balloons on %s hair and hangs them next to each other", "The balloons push away from each other.", "Both balloons have the same kind of charge, so they repel."),
          ("rubs a plastic comb on %s hair and holds it near a thin stream of water", "The stream of water bends toward the comb.", "The charged comb attracts the water without touching it."),
          ("rubs a balloon on %s hair and holds it against a wall", "The balloon sticks to the wall.", "The charged balloon is attracted to the wall."),
          ("slides across a carpet in socks and touches a metal doorknob", "A small spark and a shock happen.", "Static charge built up and jumped to the doorknob.")]


def g_static():
    act, a, why = R.choice(STATIC)
    p = P.next()
    act = act.replace("%s", p[2])
    w = [x[1] for x in STATIC if x[1] != a]
    return item("%s %s. What happens?" % (p[0], act), a, R.sample(w, 2) + ["Nothing happens, because the objects are not touching."], why)


B1 = bank([
    ("What are the two ends of a magnet called?", "the north pole and the south pole", ["the top and the bottom", "the plus and the minus", "the hot end and the cold end"], "Every magnet has an N and an S pole."),
    ("What happens when two north poles face each other?", "They repel (push apart).", ["They attract.", "Nothing happens.", "They stick together."], "Like poles repel."),
    ("What happens when a north pole faces a south pole?", "They attract (pull together).", ["They repel.", "Nothing happens.", "They both turn into south poles."], "Unlike poles attract."),
    ("Do magnets need to touch an object to pull it?", "No. Magnetic forces can act from a distance.", ["Yes, always.", "Only in water.", "Only at night."], "Magnets can pull through air, paper and even water."),
    ("When is the pull of a magnet strongest?", "when the object is close to the magnet", ["when the object is far away", "always the same at every distance", "only when the magnet is wet"],
     "Magnetic force gets weaker with distance."),
    ("What is static electricity?", "an electric charge that builds up when some things are rubbed together", ["electricity in wall outlets", "a kind of magnet", "light from the sun"],
     "Rubbing a balloon on hair builds up charge."),
    ("Can static electricity pull objects without touching them?", "Yes, like a rubbed balloon pulling on hair.", ["No, never.", "Only if the objects are metal.", "Only if they are magnets."],
     "Electric forces act at a distance too."),
    ("Which can a magnet pull through?", "a sheet of paper", ["nothing at all", "only air", "only metal"], "Magnetic force passes through paper, plastic and water."),
])
B5 = bank([
    ("Ava puts one magnet in a cup and holds a paper clip above it. The clip moves when it is close. What does this show?", "Magnetic forces act without touching.", ["Magnets need to touch to work.", "Paper clips make magnets.", "Cups are magnetic."],
     "The clip moved before touching the magnet."),
    ("Leo wants to know if a magnet works through cardboard. What should he do?", "put cardboard between the magnet and a paper clip and see if the clip moves", ["paint the magnet", "drop the magnet", "put the magnet in the freezer"],
     "Test it directly."),
    ("Mia has a magnet with no labels and a magnet with N and S labeled. How can she find the north pole of the unlabeled magnet?", "Bring it near the labeled N pole. The end that is pushed away is N.", ["Look at the color.", "Weigh it.", "Taste it."],
     "Like poles repel."),
    ("Noah rubs a balloon on his hair. Then he rubs it more. What happens to how strongly it pulls the paper bits?", "It usually pulls more strongly.", ["It stops pulling.", "It pulls the same.", "It turns into a magnet."],
     "More rubbing builds up more charge."),
    ("Why do clothes sometimes stick together when they come out of a dryer?", "Static electricity builds up as they tumble and rub.", ["They are magnetic.", "They are still wet.", "Gravity is stronger in dryers."],
     "Rubbing builds up charge."),
])


def body():
    think = ("<p>Some forces can push or pull without touching: <b>magnetic forces</b> and <b>electric forces</b>.</p>"
             "<ul><li>Every magnet has a <b>north (N)</b> and a <b>south (S)</b> pole. Like poles <b>repel</b>; unlike poles <b>attract</b>.</li>"
             "<li>Magnets attract iron and steel, but not plastic, wood, glass, paper, aluminum or copper.</li>"
             "<li>The force is <b>stronger when the objects are closer</b>.</li>"
             "<li><b>Static electricity</b>: a balloon rubbed on hair can pull hair or paper bits without touching them.</li></ul>"
             + figure(pair(("N", "S"), ("N", "S")), "S faces N, so these magnets attract."))
    ex = [("Two magnets have S facing S. What happens?", ["Like poles repel."], "They push apart."),
          ("Will a magnet pick up an aluminum can?", ["Aluminum is a metal, but not iron or steel."], "No.")]
    mist = ["Thinking magnets attract all metals. They attract iron, steel and nickel.",
            "Thinking like poles attract. Like poles repel.",
            "Thinking magnets and static electricity only work when touching."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Magnetic poles", B1 + [(g_poles, 6), (g_attract, 6)]),
        ("Attract or repel?", [(g_poles, 12), (g_attract, 8)]),
        ("What magnets attract", [(g_attract, 12), (g_metal, 5), (g_poles, 3)]),
        ("Distance and static electricity", [(g_dist, 10), (g_static, 10)]),
        ("Investigations", B5 + [g_dist, g_static, g_poles, g_metal]),
    ])
    make("grade-3", "magnets-and-static-electricity", 3, "3-PS2-3",
         "Ask questions to determine cause and effect relationships of electric or magnetic interactions between two objects not in contact with each other.",
         "Magnets and Static Electricity",
         "Grade 3 Magnets Worksheets: Poles, Attract and Repel, and Static Electricity",
         "Magnets and Static Electricity",
         "Free Grade 3 science worksheets on magnets and static electricity (NGSS 3-PS2-3): north and south poles, attract and repel, magnetic materials, distance and force, and charged balloons. 100 practice questions with answers.",
         "Magnets and static electricity can push or pull without touching.",
         "Like poles repel and unlike poles attract. Magnets pull iron and steel, and they pull harder when they are closer.",
         body(),
         [("What happens when you put two magnets together?", "If unlike poles (N and S) face each other, they attract. If like poles (N and N, or S and S) face each other, they repel."),
          ("Do magnets attract all metals?", "No. Magnets attract iron, steel and nickel, but not aluminum, copper, gold or silver."),
          ("What is static electricity?", "It is an electric charge that builds up when some things rub together. A rubbed balloon can pull on hair or paper without touching it.")],
         sets)


if __name__ == "__main__":
    main()
