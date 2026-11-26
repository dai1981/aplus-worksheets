# -*- coding: utf-8 -*-
"""
UK Year 2 science: Working Scientifically (key stage 1)
  python tools/gen_uk_science_y2_working_scientifically.py
Asking simple questions, observing closely with simple equipment, simple tests, identifying and classifying, and
gathering and recording data (tally charts and tables) to suggest answers. Uses the variable question of the Year 6
unit with simple Year 2 tests, and adds equipment, odd-one-out and tally questions.
"""
import uk_sci
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import gen_uk_science_y6_working_scientifically as W
import sci_kids as K

W.U = Unit(61212)
W.R = W.U.R
W.P = People(W.R)
uk_sci.USED.clear()
U, R, P = W.U, W.R, W.P

W.EXP = [("Which material keeps a teddy driest in the rain?", "the material", "how wet the teddy gets", "the same teddy and the same amount of water"),
         ("Does cress grow better in the light or the dark?", "the amount of light", "how tall the cress grows", "the same seeds, water and pots"),
         ("Which ball bounces highest?", "the kind of ball", "how high it bounces", "dropping each ball from the same height"),
         ("Which paper towel soaks up the most water?", "the kind of paper towel", "how much water it soaks up", "the same size of towel and the same amount of water"),
         ("Do woodlice like damp or dry places?", "how damp the place is", "how many woodlice go to each side", "the same tray and the same woodlice"),
         ("Which car rolls furthest down a ramp?", "the toy car", "how far it rolls", "the same ramp and the same surface"),
         ("Which elastic band stretches the most?", "the elastic band", "how long it stretches", "the same weight on each band"),
         ("Which fabric is best for a teddy's blanket on a cold night?", "the fabric", "how warm the teddy stays", "the same teddy, the same size of blanket and the same time")]

EQUIP = [("look closely at a tiny beetle", "a magnifying glass"), ("measure how long a worm is", "a ruler"), ("time how long an ice cube takes to melt", "a timer or stopwatch"),
         ("measure how much water to give a plant", "a measuring jug"), ("find out which apple is heaviest", "weighing scales"), ("measure how tall a sunflower is", "a tape measure"),
         ("look at the grains in some sand", "a magnifying glass"), ("time how long a toy car takes to roll down a ramp", "a timer or stopwatch")]
TOOLS = ["a magnifying glass", "a ruler", "a timer or stopwatch", "a measuring jug", "weighing scales", "a tape measure"]


def g_equip():
    j, t = R.choice(EQUIP)
    if not once(("eq", j)):
        return None
    w = [x for x in TOOLS if x != t and not ({x, t} == {"a ruler", "a tape measure"})]
    return item("Which equipment would you use to %s?" % j, t, R.sample(w, 3), "Choose the right tool for the job.")


ODD = [(["a dog", "a cat", "a rabbit"], "a rock", "The others are living things."), (["a daisy", "a rose", "a tulip"], "a ladybird", "The others are flowers."),
       (["glass", "metal", "plastic"], "a worm", "The others are materials."), (["a spoon", "a key", "a coin"], "a wooden ruler", "The others are made of metal."),
       (["a window", "a jar", "a mirror"], "a jumper", "The others are made of glass."), (["a robin", "a blue tit", "a sparrow"], "a frog", "The others are birds."),
       (["a trout", "a goldfish", "a shark"], "a duck", "The others are fish."), (["an apple", "a banana", "a pear"], "a carrot", "The others are fruits."),
       (["a sponge", "modelling clay", "a pillow"], "a brick", "The others can be squashed easily."), (["a kitten", "a puppy", "a lamb"], "a cow", "The others are baby animals."),
       (["an acorn", "a sunflower seed", "a bean"], "a stone", "The others are seeds."), (["a raincoat", "an umbrella", "wellington boots"], "a paper bag", "The others are waterproof.")]


def g_odd():
    grp, odd, why = R.choice(ODD)
    if not once(("od", odd)):
        return None
    o = sorted(grp + [odd])
    return item("Which is the odd one out: %s or %s?" % (", ".join(o[:3]), o[3]), odd, grp, why)


def tally(n):
    return " ".join(["<s>||||</s>"] * (n // 5) + (["|" * (n % 5)] if n % 5 else []))


def g_tally():
    who = P.next()[0]
    things = R.sample(["robins", "blackbirds", "pigeons", "sparrows", "magpies", "blue tits"], 3)
    v = R.sample(range(2, 13), 3)
    k = R.choice(["read", "most", "least", "total"])
    ri = R.randrange(3)
    if not once(("ta", tuple(things), tuple(v), k)):
        return None
    tab = table(["Bird", "Tally"], [[t, tally(x)] for t, x in zip(things, v)])
    intro = tab + "%s made a tally chart of birds seen in the school garden. " % who
    if k == "read":
        g = str(v[ri])
        return item(intro + "How many %s were seen?" % things[ri], g, [str(x) for x in (v[ri] + 1, v[ri] - 1, v[ri] + 5, v[ri] - 5) if x > 0 and x != v[ri]][:3], "A crossed group of 5, then count the single lines.")
    if k == "most":
        a = things[v.index(max(v))]
        return item(intro + "Which bird was seen most?", a, [x for x in things if x != a] + ["They were all seen the same number of times."], "The longest tally.")
    if k == "least":
        a = things[v.index(min(v))]
        return item(intro + "Which bird was seen least?", a, [x for x in things if x != a] + ["They were all seen the same number of times."], "The shortest tally.")
    t = sum(v)
    g = str(t)
    return item(intro + "How many birds were seen altogether?", g, [str(x) for x in (t + 1, t - 1, t + 5) if x != t], "%d + %d + %d = %d." % (v[0], v[1], v[2], t))


B1 = bank([
    ("What is a good science question?", "a question you can answer by looking or testing, like 'Which ball bounces highest?'", ["a question with no answer", "a question about your favourite colour", "any question at all"], "Testable questions."),
    ("What does 'observe' mean?", "look very carefully", ["guess", "shout", "close your eyes"], "Use your senses."),
    ("What is a fair test?", "a test where you change only one thing", ["a test where everything changes", "a test that you always win", "a test done once without looking"], "Change one thing."),
    ("Why do we write results in a table?", "so we can remember and compare them", ["to make them longer", "to hide them", "to change them later"], "Record as you go."),
    ("What does 'sort' or 'classify' mean?", "put things into groups that are alike", ["throw things away", "count things only", "colour things in"], "Group by what is the same."),
    ("What is a tally chart?", "a quick way to count by drawing lines", ["a kind of map", "a type of plant", "a weather report"], "Every fifth line crosses four."),
    ("What does a prediction mean?", "what you think will happen", ["what did happen", "the equipment", "the title"], "Before the test."),
    ("What should you do after a test?", "say what you found out", ["forget the results", "throw away the table", "change the question"], "Answer the question."),
])
B5 = bank([
    ("Leo dropped one ball from high up and another from low down. Was it fair?", "No. Both balls should be dropped from the same height.", ["Yes, it was fair.", "Yes, if the balls were red.", "No, he should drop them in the dark."], "Keep it fair."),
    ("Why should you do a test more than once?", "to check the results", ["to use up time", "to make it unfair", "to change the answer"], "Check results."),
    ("A pupil finds 20 woodlice under a log and 1 on the path. What might they say?", "Woodlice like the dark, damp place under the log.", ["Woodlice like paths.", "Woodlice live in trees.", "There are no woodlice."], "Use evidence."),
    ("How could you find out which bird visits the garden most?", "Watch for the same time each day and keep a tally.", ["Guess.", "Ask a bird.", "Look for one second."], "Gather data."),
    ("Why is it good to use a ruler instead of guessing how long a worm is?", "You get a measurement you can compare.", ["Rulers make worms longer.", "Guessing is always right.", "Rulers count birds."], "Measure carefully."),
])


def body():
    pic = K.row(["mirror", "rock", "leaf"], words=["observe", "test", "record"], size=90, label="observe, test and record")
    ex = [("Look at a beetle closely with?", ["Makes things look bigger"], "a magnifying glass"),
          ("Dog, cat, rabbit, rock: odd one out?", ["Not living"], "the rock")]
    mist = ["Changing two things at once in a test.", "Guessing instead of looking carefully.", "Forgetting to write the results down."]
    return kid_lesson(pic, "Scientists ask, look, test and record.",
                      ["Ask a question you can test.", "Observe closely and measure with the right equipment.", "Sort things into groups and record results in tables and tally charts."], ex, mist)


def main():
    sets = U.sets([
        ("Asking and observing", B1 + [(g_equip, 8), (g_odd, 4)]),
        ("Simple tests", [(W.g_var, 14), (g_odd, 6)]),
        ("Sorting and grouping", [(g_odd, 2), (W.g_var, 8), (g_tally, 10)]),
        ("Tally charts", [(g_tally, 20)]),
        ("Thinking scientifically", B5 + [(g_tally, 15)]),
    ])
    make_uk(2, "working-scientifically", 12, "Working scientifically",
            "Ask simple questions and recognise that they can be answered in different ways; observe closely, using simple equipment; perform simple tests; identify and classify; "
            "use their observations and ideas to suggest answers to questions; gather and record data to help in answering questions.",
            "Working Scientifically",
            "Year 2 Science: Working Scientifically Worksheets (Questions, Tests and Tally Charts)",
            "Working Scientifically",
            "Free Year 2 science worksheets on working scientifically: asking questions, observing with simple equipment, fair tests, sorting into groups and tally charts. 100 questions with answers.",
            "Ask, look, test, record.",
            "Change one thing in a test and write down what you find.",
            body(),
            [("What does working scientifically mean?", "Asking questions, looking carefully, doing simple tests, sorting things into groups and recording what you find."),
             ("What is a fair test?", "A test where you change only one thing, so you know what made the difference."),
             ("How do I read a tally chart?", "Each line is one. Four lines with a line across them make a group of five. Count the fives, then the single lines.")],
            sets)


if __name__ == "__main__":
    main()
