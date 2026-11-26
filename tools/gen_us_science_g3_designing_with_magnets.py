# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Designing with Magnets (3-PS2-4)
  python tools/gen_us_science_g3_designing_with_magnets.py
Define a simple design problem that can be solved by applying ideas about magnets: a latch that keeps
a door closed, a sorter that separates steel cans from aluminum cans, a tool that picks up spilled pins,
a toy that moves without touching, a note holder. Criteria and constraints, testing and comparing designs.
Wrong answers come from real mistakes: "any magnet design works for aluminum", "a weaker magnet is
always better", "more magnets always solve the problem".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(30104)
R = U.R
P = People(R)

PROBLEMS = [("keep a cabinet door from swinging open", "a magnet on the door and a steel plate on the frame", ["a magnet on the door and a wooden block on the frame", "a sheet of paper taped to the door", "a plastic button on the door"],
             "The magnet pulls on the steel plate and holds the door shut."),
            ("separate steel cans from aluminum cans for recycling", "a strong magnet that lifts the steel cans out of the pile", ["a strong magnet that lifts the aluminum cans", "a fan that blows all cans away", "a net that catches all the cans"],
             "Steel is attracted to magnets; aluminum is not."),
            ("pick up spilled steel pins from a carpet", "a magnet wand moved over the carpet", ["a wooden ruler", "a plastic comb", "a sponge"],
             "The pins are steel, so the magnet pulls them up."),
            ("hang drawings on a metal fridge door", "small magnets that hold the paper against the door", ["glue on the fridge", "rubber bands", "aluminum foil"],
             "The magnets are attracted to the steel door through the paper."),
            ("make a toy car move without touching it", "a magnet on the car and another magnet held near it", ["a wooden stick taped to the car", "a feather near the car", "a cotton ball on the car"],
             "Magnets can push or pull from a distance."),
            ("find a lost steel key in the sand", "a magnet tied to a string and dragged through the sand", ["a paper cup", "a plastic shovel only", "a bucket of water"],
             "The steel key is pulled to the magnet."),
            ("keep a pencil case from spilling open in a backpack", "a magnetic clasp on the flap", ["a paper clip resting on the flap", "a plastic sticker", "a ribbon that is not tied"],
             "Two magnets in the clasp attract and hold the flap closed."),
            ("make a fishing game where paper fish can be caught", "steel paper clips on the fish and a magnet on the fishing line", ["plastic beads on the fish", "a wooden hook", "aluminum foil on the magnet"],
             "The magnet attracts the steel clips.")]


def g_design():
    goal, a, w, e = R.choice(PROBLEMS)
    p = P.next()
    return item("%s wants to %s. Which design would work best?" % (p[0], goal), a, w, e)


def g_why():
    goal, a, w, e = R.choice(PROBLEMS)
    p = P.next()
    return item("%s's design uses %s to %s. Why does it work?" % (p[0], a, goal), e,
                ["Magnets attract all materials.", "The magnet makes the objects lighter.", "Magnets only work when they are wet."], e)


def g_test():
    designs = ["Design A", "Design B", "Design C"]
    clips = R.sample(range(3, 25), 3)
    cost = R.sample([1, 2, 3, 4, 5, 6], 3)
    rows = [[d, "%d" % c, "$%d" % k] for d, c, k in zip(designs, clips, cost)]
    tab = table(["Latch", "Steel washers it can hold", "Cost"], rows)
    p = P.next()
    k = R.choice(["strong", "cheap", "both"])
    if k == "strong":
        best = designs[clips.index(max(clips))]
        return item(tab + "%s's team tested three magnet latches. Which latch is strongest?" % p[0], best, [d for d in designs if d != best] + ["They are all the same."],
                    "%s held the most washers (%d)." % (best, max(clips)))
    if k == "cheap":
        best = designs[cost.index(min(cost))]
        return item(tab + "%s's team tested three magnet latches. Which latch costs the least?" % p[0], best, [d for d in designs if d != best] + ["They all cost the same."],
                    "%s costs $%d." % (best, min(cost)))
    need = R.randint(min(clips) + 1, max(clips))
    budget = R.randint(min(cost), 6)
    ok = [d for d, c, kk in zip(designs, clips, cost) if c >= need and kk <= budget]
    if len(ok) != 1:
        return None
    return item(tab + "The latch must hold at least %d washers and cost no more than $%d. Which latch meets both rules?" % (need, budget), ok[0],
                [d for d in designs if d != ok[0]] + ["none of them"], "%s is the only one that is strong enough and cheap enough." % ok[0])


def g_crit():
    goal, a, w, e = R.choice(PROBLEMS)
    k = R.choice(["crit", "con"])
    crits = {"keep a cabinet door from swinging open": "The door must stay closed when the house shakes a little.",
             "separate steel cans from aluminum cans for recycling": "All the steel cans must be removed from the pile.",
             "pick up spilled steel pins from a carpet": "It must pick up every pin.",
             "hang drawings on a metal fridge door": "The drawings must not fall off.",
             "make a toy car move without touching it": "The car must move without being touched.",
             "find a lost steel key in the sand": "It must find the key in less than 10 minutes.",
             "keep a pencil case from spilling open in a backpack": "The case must stay closed when the backpack is shaken.",
             "make a fishing game where paper fish can be caught": "A player must be able to lift a fish off the floor."}
    cons = ["It must cost less than $5.", "It can only use materials found in the classroom.", "It must be built in one class period.", "It must fit in a shoebox."]
    p = P.next()
    if k == "crit":
        return item("%s's class will design something to %s. Which is a criterion (what the design must do)?" % (p[0], goal), crits[goal], R.sample(cons, 3),
                    "A criterion tells what the solution must do.")
    c = R.choice(cons)
    return item("%s's class will design something to %s. Which is a constraint (a limit on the design)?" % (p[0], goal), c, [crits[goal], "It must work every time it is used.", "It must do its job without breaking."],
                "A constraint is a limit, such as cost, time or materials.")


B1 = bank([
    ("What is a design problem?", "a need or want that people can solve by building something", ["a math fact", "a kind of magnet", "a picture of a magnet"],
     "Engineers solve design problems."),
    ("Which problem could a magnet help solve?", "picking up steel nails that fell in the grass", ["picking up spilled milk", "lifting a plastic cup", "drying wet paper"],
     "Magnets attract steel."),
    ("Why would a magnet NOT help sort plastic bottles from glass bottles?", "Magnets do not attract plastic or glass.", ["Magnets attract only glass.", "Magnets attract only plastic.", "Bottles are too heavy."],
     "Neither material is magnetic."),
    ("What does a magnetic door latch need on the other side to work?", "a piece of steel or another magnet", ["a piece of wood", "a sheet of paper", "a rubber band"],
     "A magnet must have something to attract."),
    ("Why do recycling centers use big magnets?", "to pull steel cans out of mixed trash", ["to melt plastic", "to wash glass", "to pull out paper"],
     "Steel is attracted; aluminum and plastic are not."),
    ("What should you do after you test your design?", "use the results to improve it and test again", ["throw it away", "never change it", "build a different design without looking at the results"],
     "Engineers test, improve and test again."),
    ("Some trains float above the track using magnets. What do the magnets do?", "repel the track to lift the train and push it forward", ["make the train heavier", "keep the train hot", "make loud sounds"],
     "Like poles repel."),
    ("Which part of a design problem tells what the solution must do?", "the criteria", ["the constraints", "the cost only", "the materials only"],
     "Criteria are goals; constraints are limits."),
])
B5 = bank([
    ("Ava's magnetic latch keeps opening when the door is bumped. What could she try?", "use a stronger magnet or move the magnet closer to the steel plate", ["use a weaker magnet", "move the magnet farther away", "replace the steel plate with wood"],
     "A closer or stronger magnet holds better."),
    ("Leo's magnet fishing game does not pick up the fish. The fish have aluminum foil on them. What should he change?", "put steel paper clips on the fish", ["add more foil", "use a longer string", "paint the fish"],
     "Aluminum is not attracted to magnets."),
    ("Mia tests her can sorter 3 times. It removes all the steel cans every time. What does this show?", "Her design is reliable.", ["Her design does not work.", "Magnets attract aluminum.", "She needs a weaker magnet."],
     "Repeated success shows reliability."),
    ("Noah's toy car moves when he pushes it with a magnet, but only from very close. How could he make it move from farther away?", "use a stronger magnet", ["use a wooden magnet", "add plastic to the car", "hold the magnet farther away"],
     "Stronger magnets act from farther away."),
    ("Why might two teams solve the same magnet problem in different ways?", "There can be more than one good solution.", ["Only one solution ever works.", "Magnets work differently for each team.", "Designs never need testing."],
     "Engineers compare many solutions."),
])


def body():
    think = ("<p>Engineers use what they know about magnets to <b>solve problems</b>:</p>"
             "<ul><li>Magnets attract iron and steel, so they can latch doors, hold notes and sort steel from aluminum.</li>"
             "<li>Magnets work without touching, so they can move toys or lift pins.</li>"
             "<li>Closer and stronger magnets pull harder.</li></ul>"
             "<p>A design has <b>criteria</b> (what it must do) and <b>constraints</b> (limits such as cost, time and materials). "
             "Test the design, look at the results and improve it.</p>")
    ex = [("You need to pick up spilled steel tacks. What tool could you build?", ["Steel is attracted to magnets."], "a magnet wand"),
          ("A latch must hold 10 washers and cost less than $3. Design A holds 12 and costs $2. Does it work?", ["12 ≥ 10", "$2 < $3"], "Yes, it meets both rules.")]
    mist = ["Using a magnet to pick up aluminum, plastic or paper.",
            "Choosing the strongest design without checking the constraints, like cost.",
            "Not testing a design more than once."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Problems magnets can solve", B1 + [(g_design, 6), (g_why, 6)]),
        ("Choosing a magnet design", [(g_design, 10), (g_why, 10)]),
        ("Criteria and constraints", [(g_crit, 14), (g_design, 6)]),
        ("Testing designs", [(g_test, 14), (g_crit, 6)]),
        ("Improving designs", B5 + [g_test, g_why, g_crit, g_design]),
    ])
    make("grade-3", "designing-with-magnets", 4, "3-PS2-4",
         "Define a simple design problem that can be solved by applying scientific ideas about magnets.",
         "Designing with Magnets",
         "Grade 3 Magnet Design Worksheets: Solving Problems with Magnets",
         "Designing with Magnets",
         "Free Grade 3 science worksheets on designing with magnets (NGSS 3-PS2-4): magnetic latches, can sorters and other magnet solutions, criteria and constraints, and testing designs with data. 100 practice questions with answers.",
         "Magnets can solve real problems.",
         "Use what you know about magnets: they pull iron and steel, work without touching, and pull harder when closer.",
         body(),
         [("What problems can magnets solve?", "Magnets can keep doors closed, hold notes on a fridge, sort steel cans from aluminum cans, pick up steel pins and move toys without touching."),
          ("What are criteria and constraints?", "Criteria are what a design must do. Constraints are limits such as cost, time and materials."),
          ("Why must you test a design?", "Testing shows if the design works. You can use the results to improve it.")],
         sets)


if __name__ == "__main__":
    main()
