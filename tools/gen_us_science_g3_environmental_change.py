# -*- coding: utf-8 -*-
"""
US Grade 3 Science: When Environments Change (3-LS4-4)
  python tools/gen_us_science_g3_environmental_change.py
When the environment changes, some organisms survive and reproduce, some move to new locations, some
move into the changed environment, and some die. Students judge the merit of solutions to problems
caused by environmental change: wildlife crossings over highways, cleaning a polluted pond, planting
trees after a fire, removing invasive plants, building nest boxes, protecting wetlands.
Wrong answers come from real mistakes: "all animals simply adapt right away", "a change only affects one
kind of animal", "a solution with no evidence is just as good".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(30112)
R = U.R
P = People(R)

# (change, problem it causes, good solution, poor solutions)
PROBS = [("A new highway is built through a forest.", "Deer and foxes are hit by cars when they cross.", "build a wildlife bridge or tunnel so animals can cross safely",
          ["make the highway wider", "remove all the trees near the road", "put up bright lights"]),
         ("Trash and oil wash into a pond.", "Fish and frogs get sick and die.", "clean up the pond and stop trash from washing in",
          ["add more trash cans inside the pond", "move all the fish to a parking lot", "paint the water blue"]),
         ("A forest fire burns many trees.", "Birds and squirrels lose their homes and food.", "plant new trees and protect the area while it grows back",
          ["build a parking lot there", "cut down the trees that are left", "do nothing ever"]),
         ("A wetland is filled in to build houses.", "Ducks and frogs lose the water they need.", "protect another wetland nearby and build a pond",
          ["fill in more wetlands", "pave the rest of the land", "put the ducks in a zoo"]),
         ("Dead trees are cleared from a park.", "Woodpeckers and owls have fewer places to nest.", "put up nest boxes for the birds",
          ["cut down more trees", "put out cat food", "build a fence around the birds"]),
         ("A new plant from far away spreads in a field.", "It crowds out the flowers bees and butterflies use.", "remove the new plant and plant native flowers",
          ["plant more of the new plant", "spray all the flowers with paint", "let the field turn to dirt"]),
         ("A river is dammed for a reservoir.", "Salmon cannot swim upstream to lay eggs.", "build a fish ladder so salmon can get past the dam",
          ["make the dam taller", "catch all the salmon", "pour sand into the river"]),
         ("Lights from a new beach hotel shine on the sand at night.", "Baby sea turtles walk toward the lights instead of the ocean.", "turn off or shield the lights during nesting season",
          ["add more lights", "build a road on the beach", "move the ocean"]),
         ("Farm fields replace a grassland.", "Bees and butterflies lose flowers to feed on.", "plant strips of wildflowers along the field edges",
          ["pave the field edges", "plant only grass", "remove all the flowers"])]


def g_solution():
    ch, prob, good, bad = R.choice(PROBS)
    p = P.next()
    return item("%s's class reads: “%s %s” Which solution would help most?" % (p[0], ch, prob),
                good, bad, "This solution fixes the problem the change caused.")


def g_problem():
    ch, prob, good, bad = R.choice(PROBS)
    others = [x[1] for x in PROBS if x[1] != prob]
    p = P.next()
    return item("%s learns that “%s” What problem might this cause for living things?" % (p[0], ch), prob, R.sample(others, 3),
                "Changes in the environment can harm the plants and animals that live there.")


RESP = [("A pond slowly dries up during a drought.", ["Frogs move to a nearby stream.", "Some fish die.", "Birds that eat fish fly away to find food."]),
        ("A new forest grows on an old farm field.", ["Deer and squirrels move into the new forest.", "Grassland birds move away.", "New kinds of trees start to grow."]),
        ("Winters become warmer in an area.", ["Some birds stay all winter instead of flying south.", "Animals that need cold move north.", "New plants that like warmth grow there."]),
        ("A flood covers a field with mud.", ["Worms move up out of the wet soil.", "Some plants die under the mud.", "Ducks move into the flooded area."])]


def g_resp():
    ch, rs = R.choice(RESP)
    a = R.choice(rs)
    p = P.next()
    return item("%s observes that %s Which is a way living things might respond?" % (p[0], ch[0].lower() + ch[1:]), a,
                ["All the animals change their bodies overnight.", "Nothing happens to any living thing.", "Every plant gets up and walks away."],
                "When the environment changes, some living things survive, some move away, some move in and some die.")


def g_data():
    ch, prob, good, bad = R.choice(PROBS[:3] + PROBS[4:5] + PROBS[6:7])
    animal = {0: "deer hit by cars", 1: "frogs counted", 2: "birds counted", 4: "owls nesting", 6: "salmon counted"}[PROBS.index((ch, prob, good, bad))]
    before = R.randint(4, 15)
    after = R.randint(before + 5, before + 30) if "hit" not in animal else R.randint(1, before - 2)
    ch_svg = bar_chart(["before", "after"], [before, after], animal, "bar graph before and after a solution", ymax=50 if after > 25 else 30, step=10 if after > 25 else 5, w=220)
    p = P.next()
    hit = "hit" in animal
    if R.random() < 0.5:
        return item(fig(ch_svg) + "%s's town tried this solution: %s. The graph shows %s before and after. Did the solution help?" % (p[0], good, animal),
                    "Yes. The data shows the problem got better.", ["No. The data shows the problem got worse.", "The data shows nothing changed.", "You cannot use data to judge a solution."],
                    "Before: %d. After: %d. %s" % (before, after, "Fewer deer were hit." if hit else "There are more of them now."))
    d = abs(after - before)
    return item(fig(ch_svg) + "%s's town tried this solution: %s. What is the difference between the numbers before and after?" % (p[0], good),
                "%d" % d, ["%d" % before, "%d" % after, "%d" % (before + after)], "%d − %d = %d." % (max(before, after), min(before, after), d))


def g_merit():
    ch, prob, good, bad = R.choice(PROBS)
    p = P.next()
    return item("Two classes suggest solutions for this problem: “%s” %s's class says: %s. Another class says: %s. Which solution has more merit, and why?" % (prob, p[0], good, bad[0]),
                "%s's solution, because it fixes the cause of the problem" % p[0],
                ["the other class's solution, because it is bigger", "Both are equally good.", "Neither, because problems cannot be solved."],
                "A good solution helps the plants and animals affected by the change.")


B1 = bank([
    ("What can happen to living things when their environment changes?", "Some survive, some move away, some move in and some die.", ["They all stay exactly the same.", "They all change their bodies right away.", "Only plants are affected."],
     "Changes can help some living things and harm others."),
    ("Which is an example of an environmental change?", "a forest is cut down to build a mall", ["a bird sings a song", "a squirrel eats a nut", "a child reads a book"],
     "Changes can be caused by people or by nature."),
    ("Which change is caused by nature?", "a drought that dries up a lake", ["building a new road", "cutting down trees for houses", "building a dam"], "Droughts, floods and fires can be natural."),
    ("Why do some animals move when their habitat changes?", "to find food, water and shelter somewhere else", ["because they are bored", "to get exercise", "to visit friends"],
     "Animals need their needs met."),
    ("What does a wildlife crossing do?", "lets animals cross a road safely", ["makes cars go faster", "feeds animals", "keeps animals in cages"], "Bridges and tunnels help animals cross."),
    ("How can people help a polluted stream?", "pick up trash and keep chemicals out of the water", ["dump more trash in it", "pave over it", "cut down the trees beside it"],
     "Clean water helps fish and frogs."),
    ("What is a good way to judge if a solution works?", "collect data before and after and compare", ["guess", "ask which one is bigger", "choose the most expensive one"],
     "Evidence shows if a solution helps."),
    ("Why do people put up nest boxes?", "to give birds places to nest when trees are gone", ["to keep birds out", "to feed squirrels", "to collect rain"], "Nest boxes replace lost homes."),
])
B5 = bank([
    ("Ava's town builds a tunnel under a road for turtles. How can the town find out if it works?", "count turtles hit on the road before and after", ["paint the tunnel", "count the cars", "measure the tunnel's length only"],
     "Data shows whether fewer turtles are hurt."),
    ("Leo says planting trees after a fire is a good idea. Which evidence would best support his claim?", "Birds and squirrels returned after the trees grew.", ["The trees are green.", "The fire was hot.", "People like trees."],
     "Evidence about the animals supports the claim."),
    ("Mia's class compares two plans to help bees. Plan A plants wildflowers; Plan B mows all the flowers. Which plan has more merit?", "Plan A", ["Plan B", "They are the same.", "neither plan"],
     "Bees need flowers."),
    ("A beaver dam floods part of a stream. Which animals might move in?", "ducks and frogs", ["camels", "polar bears", "cactus wrens"], "New ponds attract water animals."),
    ("Why might a solution help one animal but hurt another?", "Changes in a habitat affect many living things in different ways.", ["Solutions never affect animals.", "All animals need the same things.", "Animals do not live together."],
     "Think about all the living things in the habitat."),
])


def body():
    think = ("<p>Environments can <b>change</b>. Nature causes floods, droughts and fires. People build roads, houses and dams.</p>"
             "<p>When an environment changes, some plants and animals <b>survive</b>, some <b>move away</b>, some new ones <b>move in</b> and some <b>die</b>.</p>"
             "<p>People can design <b>solutions</b> to help: wildlife bridges over highways, cleaning polluted water, planting trees, nest boxes and fish ladders. "
             "We judge a solution by its <b>merit</b>: does it fix the problem? Data from before and after is the best evidence.</p>")
    ex = [("A new road cuts through a forest and deer are hit by cars. Name a solution.", ["Deer need to cross safely."], "a wildlife bridge or tunnel"),
          ("After a solution, frog counts go from 8 to 30. Did it help?", ["More frogs live there now."], "Yes.")]
    mist = ["Thinking all animals change their bodies right away when the environment changes.",
            "Thinking a change affects only one kind of living thing.",
            "Choosing a solution without checking the evidence."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Environments change", B1 + [(g_problem, 6), (g_resp, 6)]),
        ("How living things respond", [(g_resp, 10), (g_problem, 10)]),
        ("Choosing solutions", [(g_solution, 12), (g_merit, 8)]),
        ("Using data to judge solutions", [(g_data, 12), (g_merit, 8)]),
        ("Making claims about solutions", B5 + [g_solution, g_data, g_resp, g_merit]),
    ])
    make("grade-3", "environmental-change", 12, "3-LS4-4",
         "Make a claim about the merit of a solution to a problem caused when the environment changes and the types of plants and animals that live there may change.",
         "When Environments Change",
         "Grade 3 Environmental Change Worksheets: How Living Things Respond and Solutions That Help",
         "Environmental Change",
         "Free Grade 3 science worksheets on environmental change (NGSS 3-LS4-4): how plants and animals respond to changes, problems caused by roads, pollution and fire, and judging solutions with data. 100 practice questions with answers.",
         "When environments change, living things are affected.",
         "Some survive, some move away and some die. People can design solutions, like wildlife bridges, and use data to see if they work.",
         body(),
         [("What happens to animals when their environment changes?", "Some survive, some move to new places, some new animals move in, and some die."),
          ("How can people help when an environment changes?", "They can build wildlife crossings, clean polluted water, plant trees, put up nest boxes and protect wetlands."),
          ("How do you know if a solution works?", "Collect data before and after the solution, such as animal counts, and compare.")],
         sets)


if __name__ == "__main__":
    main()
