# -*- coding: utf-8 -*-
"""
US High School Biology: Group Behavior and Survival (HS-LS2-8)
  python tools/gen_us_science_bio_group_behavior.py
Evaluate evidence for the role of group behavior on individual and species' chances to survive and reproduce.
Flocking, schooling, herding, pack hunting, huddling, sentinels and alarm calls, division of labor in colonies,
migration in groups; costs of group living; predator-success and vigilance data.
Wrong answers come from real mistakes: "animals form groups to be friendly", "group living has no costs",
"bigger groups always mean less food competition".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(90112)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


BEH = [("Fish swim together in a tight school.", "It confuses predators and lowers each fish's chance of being caught."),
       ("Wolves hunt in a pack.", "They can catch large prey that one wolf could not."),
       ("Emperor penguins huddle in winter.", "They share body heat and save energy."),
       ("Geese fly in a V formation.", "Each bird saves energy in the air flow of the bird ahead."),
       ("Honeybees do a waggle dance in the hive.", "They tell other bees where to find food."),
       ("A meerkat stands guard while others feed.", "It warns the group of predators so more survive."),
       ("Musk oxen form a circle around their calves.", "Adults face predators and protect the young."),
       ("Worker ants, soldiers and a queen share colony jobs.", "Division of labor helps the colony survive and reproduce."),
       ("Vervet monkeys give different alarm calls for eagles and leopards.", "Group members know which escape to use."),
       ("Zebras gather in large herds on the savanna.", "More eyes spot predators sooner."),
       ("Starlings form huge swirling flocks.", "It is hard for a falcon to single out one bird."),
       ("Elephants travel in family herds led by an old female.", "The leader remembers where water is in a drought.")]


def g_ben():
    s, a = R.choice(BEH)
    k = R.random() < 0.6
    if not once((s, k)):
        return None
    if k:
        return item("%s How does this behavior help them survive?" % s, a, R.sample([x[1] for x in BEH if x[1] != a], 3), "Group behavior raises the chance to survive and reproduce.")
    return item("Which behavior best matches this benefit: “%s”" % a, s.rstrip("."), R.sample([x[0].rstrip(".") for x in BEH if x[1] != a], 3), "Match the behavior to the benefit.")


def g_pred():
    who = P.next()[0]
    sizes = [1, 5, 10, 20, 40]
    v = sorted(R.sample(range(5, 80), 5), reverse=True)
    k = R.choice(["best", "trend", "diff", "claim"])
    if not once((tuple(v), k)) or not once(("pk", k), {"best": 4, "trend": 3, "claim": 3, "diff": 30}[k]):
        return None
    tab = table(["Group size (animals)", "Hawk attacks that succeed (%)"], [[str(a), "%d%%" % b] for a, b in zip(sizes, v)])
    if k == "best":
        return item(tab + "%s studied pigeons attacked by hawks. Which group size was safest?" % who, "40", ["1", "5", "10"], "Lowest success rate for the hawk.")
    if k == "trend":
        return item(tab + "What pattern do %s's data show?" % who, "Larger groups make hawk attacks less successful.", ["Larger groups make attacks more successful.", "Group size has no effect.", "Only single pigeons survive."],
                    "The percent drops as group size grows.")
    if k == "claim":
        return item(tab + "Which claim do %s's data support?" % who, "Flocking increases each pigeon's chance to survive.", ["Flocking attracts more hawks.", "Pigeons flock to stay warm.", "Hawks prefer large flocks."],
                    "Fewer successful attacks.")
    i, j = sorted(R.sample(range(5), 2))
    return item(tab + "How many percentage points lower was hawk success for groups of %d than groups of %d?" % (sizes[j], sizes[i]), str(v[i] - v[j]), [str(v[j]), str(v[i]), str(v[i] - v[j] + 5)],
                "%d − %d = %d." % (v[i], v[j], v[i] - v[j]))


def g_vig():
    who = P.next()[0]
    sizes = [1, 3, 6, 12]
    v = sorted(R.sample(range(10, 70), 4), reverse=True)
    k = R.choice(["feed", "why", "read"])
    if not once((tuple(v), k)) or not once(("vk", k), {"feed": 3, "why": 3, "read": 30}[k]):
        return None
    tab = table(["Group size (deer)", "% of time each deer spends watching for danger"], [[str(a), "%d%%" % b] for a, b in zip(sizes, v)])
    if k == "feed":
        return item(tab + "From %s's data, how does being in a big group help each deer?" % who, "It can spend more time eating.", ["It spends more time watching.", "It never has to watch.", "It eats less."],
                    "Less watching, more feeding.")
    if k == "why":
        return item(tab + "Why does each deer watch less in larger groups (%s's study)?" % who, "Many eyes share the job of spotting predators.", ["Larger groups have no predators.", "Deer in groups cannot see.", "The deer are sleeping."],
                    "Shared vigilance.")
    i = R.randrange(4)
    return item(tab + "In %s's data, what percent of time does each deer watch for danger in a group of %d?" % (who, sizes[i]), "%d%%" % v[i], ["%d%%" % v[(i + 1) % 4], "%d%%" % (100 - v[i]), "%d%%" % (v[i] + 5)],
                "Read the row for %d deer." % sizes[i])


COST = [("Many birds nesting close together", "Diseases and parasites spread more easily."), ("A big herd grazing in one field", "Individuals compete for food."),
        ("A large group of lions", "Each lion gets a smaller share of a kill."), ("A crowded colony of seals", "Pups can be crushed or lost in the crowd."),
        ("A large, noisy flock", "It can be easier for predators to find.")]


def g_cost():
    s, a = R.choice(COST)
    if not once(s):
        return None
    return item("%s: what is a cost of group living?" % s, a, R.sample([x[1] for x in BEH], 2) + ["There are no costs to living in groups."], "Group living has benefits and costs.")


B1 = bank([
    ("Why do many animals live in groups?", "to improve their chances of surviving and reproducing", ["to be friendly only", "because they cannot see", "to avoid eating"], "Evolution favors helpful behaviors."),
    ("What is a 'selfish herd'?", "each animal moves toward the middle to be less likely to be eaten", ["animals that share all food", "a herd with no leader", "a herd of one"], "Safety in numbers."),
    ("What is cooperative hunting?", "animals working together to catch prey", ["hunting alone", "animals hiding from prey", "eating only plants"], "Wolves, lions, orcas."),
    ("Why can a worker bee's behavior help its genes even though it does not reproduce?", "It helps its relatives (the queen's offspring) survive.", ["It has no genes.", "Workers lay most eggs.", "It cannot help."], "Kin selection."),
    ("What is an alarm call?", "a sound that warns others of danger", ["a mating song", "a sound to find food only", "a sleep sound"], "Meerkats, monkeys, birds."),
    ("Which is a benefit of migrating in a group?", "sharing navigation and saving energy", ["getting lost more often", "flying slower alone", "eating more alone"], "Geese, wildebeest."),
    ("What is a cost of living in a group?", "more competition and disease", ["more food for everyone always", "no predators ever", "warmer weather"], "Trade-offs."),
    ("How does huddling help penguins?", "It reduces heat loss in cold weather.", ["It makes them faster swimmers.", "It helps them fly.", "It hides them from the sun."], "Shared warmth."),
])
B5 = bank([
    ("A scientist claims lions hunt better in groups. Which evidence best supports the claim?", "Groups catch prey more often per hunt than single lions.", ["Lions sleep a lot.", "Lions have manes.", "Lions live in Africa."], "Data on success."),
    ("Ants that work together build a raft to survive floods. What does this show?", "Group behavior helps the colony survive changes.", ["Ants cannot swim.", "Floods help ants.", "Each ant survives alone."], "Collective behavior."),
    ("Why might a fish leave its school?", "When food is scarce, competition in the school is high.", ["Schools are always better.", "Fish dislike water.", "Predators prefer single fish."], "Costs can outweigh benefits."),
    ("Researchers remove the sentinels from a meerkat group. What is the likely result?", "More meerkats are caught by predators.", ["Fewer are caught.", "Nothing changes.", "They grow faster."], "Sentinels warn others."),
    ("How could a student test whether flocking protects birds?", "compare predator success on single birds and on flocks", ["count the colors of birds", "measure wing length only", "listen to songs"], "Design a comparison."),
])


def body():
    think = ("<p><b>Groups help individuals survive and reproduce.</b></p>"
             "<ul><li>Benefits: spotting predators, confusing them, hunting big prey, sharing warmth and information.</li>"
             "<li>Costs: more competition for food and faster spread of disease.</li>"
             "<li>Use data (for example, predator success vs group size) to judge a claim.</li></ul>")
    ex = [("Hawk success: 1 bird 70%, 40 birds 10%. Safer?", ["Lower success = safer"], "the flock of 40"),
          ("Why do geese fly in a V?", ["Air flow behind the leader"], "to save energy")]
    mist = ["Thinking animals form groups just to be friendly.", "Forgetting that group living has costs.", "Thinking bigger groups always mean less competition."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Why live in groups?", B1 + [(g_ben, 8), (g_cost, 4)]),
        ("Benefits of group behavior", [(g_ben, 14), (g_cost, 1), (g_vig, 5)]),
        ("Predator data", [(g_pred, 16), (g_vig, 4)]),
        ("Watching for danger", [(g_vig, 14), (g_pred, 6)]),
        ("Evaluating evidence", B5 + [(g_pred, 9), (g_vig, 6)]),
    ])
    make("biology", "group-behavior", 12, "HS-LS2-8",
         "Evaluate evidence for the role of group behavior on individual and species' chances to survive and reproduce.",
         "Group Behavior and Survival",
         "Group Behavior Worksheets: Flocks, Herds, Packs and Survival (High School Biology)",
         "Group Behavior",
         "Free high school biology worksheets on group behavior (NGSS HS-LS2-8): flocking, schooling, pack hunting, alarm calls, costs of group living and predator data. 100 questions with answers.",
         "Groups help animals survive.",
         "Flocks, herds and packs raise each animal's chance to survive and reproduce.",
         body(),
         [("Why do animals live in groups?", "Groups help them spot and confuse predators, hunt larger prey, stay warm and share information about food."),
          ("Are there costs to group living?", "Yes. Group members compete for food and mates, and diseases and parasites spread more easily."),
          ("How can students evaluate evidence?", "Look at data such as predator success or time spent watching for danger at different group sizes.")],
         sets)


if __name__ == "__main__":
    main()
