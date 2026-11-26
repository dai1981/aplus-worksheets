# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Animals Living in Groups (3-LS2-1)
  python tools/gen_us_science_g3_animal_groups.py
Some animals form groups that help members survive: getting food (wolves hunting in packs), defense
(fish in schools, musk oxen in a circle, meerkat lookouts), coping with change (penguins huddling for warmth,
geese flying in a V), and dividing jobs (ants and bees).
Wrong answers come from real mistakes: "groups only help the leader", "animals in groups never compete",
"all animals live in groups".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(30106)
R = U.R
P = People(R)

# (animal, group word, what they do, benefit category, benefit sentence)
GROUPS = [("wolves", "pack", "hunt together", "getting food", "They can catch large prey like deer that one wolf could not catch alone."),
          ("lions", "pride", "hunt together and share food", "getting food", "Working together helps them catch big animals."),
          ("fish", "school", "swim close together", "staying safe", "It is hard for a predator to pick out one fish from a big, moving group."),
          ("zebras", "herd", "stay close together", "staying safe", "Many eyes watch for lions, and their stripes make it hard to pick out one zebra."),
          ("meerkats", "mob", "take turns as lookouts", "staying safe", "A lookout calls out when an eagle or jackal comes, so the others can hide."),
          ("musk oxen", "herd", "form a circle around their young", "staying safe", "The adults' horns face out to protect the calves from wolves."),
          ("emperor penguins", "huddle", "huddle together in winter", "surviving changes in the environment", "Huddling keeps them warm in freezing Antarctic winds."),
          ("Canada geese", "flock", "fly in a V shape", "surviving changes in the environment", "Flying in a V saves energy on long trips south for the winter."),
          ("honeybees", "colony", "split up jobs like gathering nectar, caring for young and guarding the hive", "dividing jobs", "Each bee does a job, so the whole colony gets food and stays safe."),
          ("ants", "colony", "split up jobs like finding food, building tunnels and caring for eggs", "dividing jobs", "Many ants working together can do much more than one ant."),
          ("elephants", "herd", "protect the young and lead the group to water", "surviving changes in the environment", "Older elephants remember where to find water in dry seasons."),
          ("dolphins", "pod", "work together to trap fish", "getting food", "They herd fish into a tight ball so they are easier to catch."),
          ("killer whales", "pod", "hunt together", "getting food", "Working as a team helps them catch seals and fish."),
          ("prairie dogs", "town", "bark warnings to each other", "staying safe", "Warning calls tell the others to dive into their burrows.")]
CATS = ["getting food", "staying safe", "surviving changes in the environment", "dividing jobs"]


def cap(s):
    return s[0].upper() + s[1:]


def g_benefit():
    an, grp, do, cat, why = R.choice(GROUPS)
    p = P.next()
    return item("%s reads that %s %s. How does living in a group mostly help them?" % (p[0], an, do), cat, [c for c in CATS if c != cat], why)


def g_why():
    an, grp, do, cat, why = R.choice(GROUPS)
    others = [g[4] for g in GROUPS if g[3] != cat]
    p = P.next()
    return item("%s sees in a nature video that %s %s. Why do they do this?" % (p[0], an, do), why, R.sample(others, 3), why)


def g_name():
    an, grp, do, cat, why = R.choice([g for g in GROUPS if g[1] not in ("mob", "town", "huddle")])
    w = [g for g in ["pack", "pride", "school", "herd", "flock", "colony", "pod"] if g != grp]
    return item("What is a group of %s called?" % an, "a " + grp, ["a " + x for x in R.sample(w, 3)], "A group of %s is called a %s." % (an, grp))


def g_hunt():
    alone = R.randint(1, 4)
    group = R.randint(alone + 3, 12)
    tries = 20
    an = R.choice([("lions", "lion"), ("wolves", "wolf"), ("hyenas", "hyena"), ("wild dogs", "wild dog")])
    ch = bar_chart(["alone", "in a group"], [alone, group], "successful hunts", "bar graph of hunting success", ymax=14, step=2, w=220)
    k = R.choice(["more", "diff", "claim"])
    if k == "more":
        return item(fig(ch) + "Scientists watched %d hunts by %s alone and %d hunts by %s in a group. Which way caught food more often?" % (tries, an[0], tries, an[0]), "hunting in a group",
                    ["hunting alone", "They were the same.", "Neither caught any food."], "%d successful hunts in a group vs. %d alone." % (group, alone))
    if k == "diff":
        return item(fig(ch) + "Out of %d hunts each, how many more successful hunts did the %s groups have than a %s alone?" % (tries, an[0], an[1]), "%d" % (group - alone),
                    ["%d" % group, "%d" % alone, "%d" % (group + alone)], "%d − %d = %d." % (group, alone, group - alone))
    return item(fig(ch) + "Which claim does this data about %s support?" % an[0], "Being in a group helps them get food.",
                ["Being in a group makes them get less food.", "Group size does not matter.", "They hunt only alone."], "Groups had more successful hunts.")


B1 = bank([
    ("Why do some animals live in groups?", "Groups help them get food, stay safe and survive changes.", ["Groups make them slower.", "So they can fight each other all day.", "Every animal must live in a group."],
     "Group living has many benefits."),
    ("Do all animals live in groups?", "No. Some, like tigers and bears, mostly live alone.", ["Yes, all of them.", "Only insects live alone.", "Only fish live alone."],
     "Some animals live alone and some live in groups."),
    ("How does a school of fish confuse a shark?", "So many fish move together that the shark cannot pick out just one.", ["The fish hide inside the shark.", "The fish turn into rocks.", "The fish swim away one at a time."],
     "There is safety in numbers."),
    ("What is one problem with living in a group?", "Members may have to share food.", ["They never see predators.", "They are always cold.", "They can never find food."],
     "Group members compete for some things."),
    ("In a beehive, why does each bee have a job?", "Splitting up jobs helps the whole colony survive.", ["Bees like to be bored.", "Only the queen works.", "Jobs make bees bigger."],
     "Workers, guards and the queen all help."),
    ("How do emperor penguins survive very cold winters?", "They huddle close together and take turns in the middle.", ["They fly south.", "They dig deep holes.", "They grow thick fur."],
     "Huddling shares body heat."),
    ("Which animal mostly lives alone?", "a tiger", ["a wolf", "an ant", "a honeybee"], "Tigers hunt and live mostly alone."),
    ("Why do meerkats take turns as lookouts?", "so others can eat while one watches for danger", ["so the lookout can eat more", "because they cannot see well", "to scare away rain"],
     "The lookout gives a warning call."),
])
B5 = bank([
    ("Ava watches a flock of birds. When a hawk flies over, all the birds fly away at once. How does the group help?", "Many eyes spot the hawk sooner, and the flock warns everyone.", ["The hawk likes groups.", "Birds in groups are slower.", "The group makes the hawk bigger."],
     "Groups help detect predators."),
    ("Leo reads that wolves in a pack of 6 catch more food than a wolf alone. What evidence would support this claim?", "data comparing how often packs and lone wolves catch prey", ["a picture of one wolf", "the color of wolf fur", "how loud wolves howl"],
     "Data supports claims."),
    ("Mia sees a line of ants carrying crumbs back to their nest. What does this show?", "Ants work together to bring food to the colony.", ["Ants each eat alone.", "Ants never share.", "Ants only move at night."],
     "Many ants share the work."),
    ("Why might a herd of zebras be safer at a watering hole than one zebra?", "Some zebras watch for lions while others drink.", ["Lions never go to water.", "One zebra is harder to see.", "Zebras in herds are invisible."],
     "Taking turns keeps the group safe."),
    ("Elephants follow the oldest female to find water in a dry season. Why does this help?", "She remembers where water was in past dry seasons.", ["She is the fastest runner.", "She can make rain.", "She is the smallest."],
     "Older members share knowledge."),
])


def body():
    think = ("<p>Some animals live in <b>groups</b>. Being in a group can help each member survive:</p>"
             "<ul><li><b>Getting food</b>: wolves and lions hunt together to catch big prey.</li>"
             "<li><b>Staying safe</b>: fish swim in schools, zebras stay in herds and meerkats take turns as lookouts.</li>"
             "<li><b>Surviving changes</b>: penguins huddle in the cold; elephants lead the herd to water in dry seasons.</li>"
             "<li><b>Dividing jobs</b>: ants and bees share the work in a colony.</li></ul>"
             "<p>Not all animals live in groups. Tigers and bears mostly live alone.</p>")
    ex = [("How does hunting in a pack help wolves?", ["One wolf cannot catch a deer alone.", "A pack can."], "They catch bigger prey and get more food."),
          ("Why do fish swim in schools?", ["A predator cannot pick one fish out of a big group."], "to stay safe")]
    mist = ["Thinking all animals live in groups.",
            "Thinking groups help only the leader. Groups help many members.",
            "Forgetting that group members also share or compete for food."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Why animals live in groups", B1 + [(g_benefit, 6), (g_name, 6)]),
        ("How groups help", [(g_benefit, 12), (g_why, 8)]),
        ("Animal groups", [(g_why, 10), (g_name, 6), (g_benefit, 4)]),
        ("Group data", [(g_hunt, 12), (g_why, 8)]),
        ("Making arguments", B5 + [g_hunt, g_benefit, g_why]),
    ])
    make("grade-3", "animal-groups", 6, "3-LS2-1",
         "Construct an argument that some animals form groups that help members survive.",
         "Animals Living in Groups",
         "Grade 3 Animal Groups Worksheets: How Living in Groups Helps Animals Survive",
         "Animal Groups",
         "Free Grade 3 science worksheets on animals living in groups (NGSS 3-LS2-1): packs, herds, schools and colonies, how groups help animals get food, stay safe and survive, with hunting data. 100 practice questions with answers.",
         "Living in a group helps some animals survive.",
         "Groups help animals get food, stay safe, survive changes and share jobs.",
         body(),
         [("Why do some animals live in groups?", "Groups help them catch food, stay safe from predators, survive cold or dry seasons, and share jobs."),
          ("Do all animals live in groups?", "No. Some animals, like tigers and bears, mostly live alone."),
          ("How do bees and ants work together?", "They divide jobs. Some find food, some care for the young and some guard the nest, so the whole colony survives.")],
         sets)


if __name__ == "__main__":
    main()
