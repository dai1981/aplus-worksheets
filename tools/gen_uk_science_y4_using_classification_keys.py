# -*- coding: utf-8 -*-
"""
UK Year 4 science: Using Classification Keys (Living things and their habitats)
  python tools/gen_uk_science_y4_using_classification_keys.py
Explore and use branching keys to identify garden minibeasts and local animals. Reuses the key-building question
makers of the Year 6 unit (new seed, keys of four animals) with Year 4 questions about using keys.
Wrong answers come from real mistakes: "following the wrong branch", "questions that are opinions",
"starting in the middle of the key".
"""
import uk_sci
from uk_sci import Unit, bank, lesson, make_uk
import gen_uk_science_y6_classification_keys as K

K.U = Unit(61402)
K.R = K.U.R
uk_sci.USED.clear()
U, R = K.U, K.R
_new_key = K.new_key
K.new_key = lambda k=None: _new_key(4)     # Year 4: keys of four animals


B1 = bank([
    ("Where do you start when using a branching key?", "at the first question", ["at the bottom", "at any question you like", "at the animal you think it is"], "Always start at question 1."),
    ("What do you do after answering a question in a key?", "follow the Yes or No branch to the next question", ["go back to the start", "guess the animal", "skip to the last question"], "One step at a time."),
    ("What tells you that you have finished using a key?", "You reach the name of one living thing.", ["You run out of time.", "You reach a question.", "You have answered three questions."], "The end of a branch."),
    ("Why are keys useful on a nature walk?", "They help you name living things you do not know.", ["They catch animals.", "They make animals tame.", "They count animals."], "Identification."),
    ("Which is a good question for a key to minibeasts?", "Does it have wings?", ["Is it nice?", "Is it scary?", "Do I like it?"], "Facts, not opinions."),
    ("Which tool helps you look closely at a minibeast's legs?", "a magnifying glass", ["a thermometer", "a stopwatch", "a ruler only"], "Observe carefully."),
    ("What does a branching key look like?", "a set of yes/no questions that split into branches", ["a long list of names", "a bar chart", "a map"], "Like the branches of a tree."),
    ("If two minibeasts give the same answer to a question, what happens?", "They follow the same branch to the next question.", ["The key stops.", "They are the same animal.", "You choose one."], "More questions split them."),
])
B5 = bank([
    ("A key asks 'Is it big?'. Why could this confuse people?", "Different people have different ideas of big.", ["Big animals are rare.", "It has too few words.", "It is a perfect question."], "Use exact features."),
    ("How could you make a key for four leaves you collected?", "Choose features such as shape or edge, and ask yes/no questions that split them.", ["Sort them by which you like best.", "Weigh them only.", "Name them at random."], "Make your own key."),
    ("Why do keys for birds often ask about beak shape?", "Beak shape is easy to see and differs between birds.", ["Beaks are all the same.", "Birds have no other features.", "Beaks change every day."], "Choose clear features."),
    ("Your key leads to the wrong animal. What should you check?", "whether you followed the right branch at each question", ["whether the animal is lying", "the weather", "the colour of the paper"], "Check each step."),
    ("Why should a key have one name at the end of each branch?", "so each living thing can be identified exactly", ["to save paper", "to make it harder", "names are not needed"], "One branch, one name."),
])


def body():
    think = ("<p><b>A branching key uses yes/no questions to name a living thing.</b></p>"
             "<ul><li>Start at question 1. Answer yes or no, then follow that branch.</li>"
             "<li>Keep going until you reach one name.</li>"
             "<li>Good questions ask about features you can see or count: legs, wings, a shell.</li></ul>")
    ex = [("Snail or slug: which question?", ["Only one has a shell"], "Does it have a shell?"),
          ("Spider: Does it have legs? Yes. More than six? Yes.", ["Follow both Yes branches"], "spider")]
    mist = ["Following the wrong branch.", "Using opinion questions.", "Starting in the middle of the key."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Using a key", B1 + [(K.g_pair, 12)]),
        ("Following a key", [(K.g_follow, 16), (K.g_pair, 4)]),
        ("What the key tells you", [(K.g_facts, 12), (K.g_follow, 8)]),
        ("Comparing animals", [(K.g_split, 14), (K.g_count, 6)]),
        ("Making keys", B5 + [(K.g_count, 5), (K.g_split, 5), (K.g_facts, 5)]),
    ])
    make_uk(4, "using-classification-keys", 2, "Living things and their habitats",
            "Explore and use classification keys to help group, identify and name a variety of living things in their local and wider environment.",
            "Using Classification Keys",
            "Year 4 Science: Using Classification Keys Worksheets (Minibeasts and Animals)",
            "Classification Keys",
            "Free Year 4 science worksheets on using classification keys: follow a branching key to name minibeasts and animals, and choose good yes/no questions. 100 questions with answers.",
            "Answer yes or no, step by step.",
            "Start at question 1 and follow the branches to one name.",
            body(),
            [("How do I use a classification key?", "Start at the first question, answer yes or no about the living thing, and follow that branch until you reach its name."),
             ("What makes a good key question?", "A question with a clear yes or no answer about a feature you can see, such as 'Does it have wings?'"),
             ("Why do scientists use keys?", "To identify living things quickly and correctly, even ones they have never seen before.")],
            sets)


if __name__ == "__main__":
    main()
