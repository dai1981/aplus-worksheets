# -*- coding: utf-8 -*-
"""
UK Year 6 science: Classification Keys (Living things and their habitats)
  python tools/gen_uk_science_y6_classification_keys.py
Branching (yes/no) keys built from the features of real animals: follow a key to name an animal, find the question
that separates two animals, count the questions needed, and choose good key questions.
Every key is built new from a random set of animals, so questions do not repeat.
Wrong answers come from real mistakes: "following the Yes branch when the answer is No", "questions that are opinions
(Is it pretty?)", "questions that do not split the group".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, once

U = Unit(61602)
R = U.R

Q = {"legs": "Does it have legs?", "wings": "Does it have wings?", "many": "Does it have more than six legs?",
     "shell": "Does it have a shell?", "fur": "Does it have fur?", "feathers": "Does it have feathers?",
     "water": "Does it live mostly in water?", "scales": "Does it have scales?", "eight": "Does it have exactly eight legs?",
     "rings": "Is its body made of rings?", "spots": "Does it have spots?", "stripes": "Does it have stripes?"}
SHORT = {"legs": "has legs", "wings": "has wings", "many": "has more than six legs", "shell": "has a shell", "fur": "has fur",
         "feathers": "has feathers", "water": "lives mostly in water", "scales": "has scales", "eight": "has exactly eight legs",
         "rings": "has a body made of rings", "spots": "has spots", "stripes": "has stripes"}
NOT = {"legs": "has no legs", "wings": "has no wings", "many": "has six legs or fewer", "shell": "has no shell", "fur": "has no fur",
       "feathers": "has no feathers", "water": "does not live mostly in water", "scales": "has no scales", "eight": "does not have exactly eight legs",
       "rings": "does not have a body made of rings", "spots": "has no spots", "stripes": "has no stripes"}

MINI = {"snail": dict(legs=0, wings=0, many=0, shell=1, eight=0, rings=0, spots=0, stripes=0),
        "slug": dict(legs=0, wings=0, many=0, shell=0, eight=0, rings=0, spots=0, stripes=0),
        "spider": dict(legs=1, wings=0, many=1, shell=0, eight=1, rings=0, spots=0, stripes=0),
        "ladybird": dict(legs=1, wings=1, many=0, shell=0, eight=0, rings=0, spots=1, stripes=0),
        "ant": dict(legs=1, wings=0, many=0, shell=0, eight=0, rings=0, spots=0, stripes=0),
        "centipede": dict(legs=1, wings=0, many=1, shell=0, eight=0, rings=0, spots=0, stripes=0),
        "bee": dict(legs=1, wings=1, many=0, shell=0, eight=0, rings=0, spots=0, stripes=1),
        "woodlouse": dict(legs=1, wings=0, many=1, shell=1, eight=0, rings=0, spots=0, stripes=0),
        "earthworm": dict(legs=0, wings=0, many=0, shell=0, eight=0, rings=1, spots=0, stripes=0),
        "butterfly": dict(legs=1, wings=1, many=0, shell=0, eight=0, rings=0, spots=0, stripes=0)}
VERT = {"fox": dict(fur=1, feathers=0, wings=0, water=0, scales=0, legs=1), "robin": dict(fur=0, feathers=1, wings=1, water=0, scales=0, legs=1),
        "trout": dict(fur=0, feathers=0, wings=0, water=1, scales=1, legs=0), "frog": dict(fur=0, feathers=0, wings=0, water=0, scales=0, legs=1),
        "snake": dict(fur=0, feathers=0, wings=0, water=0, scales=1, legs=0), "bat": dict(fur=1, feathers=0, wings=1, water=0, scales=0, legs=1),
        "duck": dict(fur=0, feathers=1, wings=1, water=1, scales=0, legs=1), "otter": dict(fur=1, feathers=0, wings=0, water=1, scales=0, legs=1),
        "lizard": dict(fur=0, feathers=0, wings=0, water=0, scales=1, legs=1), "shark": dict(fur=0, feathers=0, wings=0, water=1, scales=1, legs=0)}


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def build(names, pool):
    """Branching key: returns (nodes, path) where nodes = [(feature, yes, no)] with yes/no = int (node) or str (animal)."""
    feats = list(pool[names[0]].keys())
    nodes = []
    path = {}

    def go(group, steps):
        if len(group) == 1:
            path[group[0]] = steps
            return group[0]
        good = []
        for f in feats:
            y = [g for g in group if pool[g][f]]
            if 0 < len(y) < len(group):
                good.append((abs(2 * len(y) - len(group)), f))
        if not good:
            raise ValueError("cannot split")
        best = min(b for b, _ in good)
        f = R.choice([f for b, f in good if b == best])
        idx = len(nodes)
        nodes.append(None)
        y = [g for g in group if pool[g][f]]
        n = [g for g in group if not pool[g][f]]
        yes = go(y, steps + [(f, 1, idx)])
        no = go(n, steps + [(f, 0, idx)])
        nodes[idx] = (f, yes, no)
        return idx

    go(list(names), [])
    return nodes, path


def render(nodes):
    def t(x):
        return "go to %d" % (x + 1) if isinstance(x, int) else "<b>%s</b>" % x
    return table(["", "Question", "Yes", "No"], [[str(k + 1), Q[f], t(y), t(n)] for k, (f, y, n) in enumerate(nodes)])


def new_key(k=None):
    pool = R.choice([MINI, VERT])
    names = R.sample(sorted(pool), k or R.choice([4, 4, 5]))
    nodes, path = build(names, pool)
    return pool, names, nodes, path


def g_follow():
    pool, names, nodes, path = new_key()
    a = R.choice(names)
    steps = path[a]
    desc = " and ".join("%s to question %d" % ("Yes" if v else "No", i + 1) for f, v, i in steps)
    if not once(("fo", tuple(sorted(names)), a)):
        return None
    w = [x for x in names if x != a]
    if len(w) < 3:
        return None
    return item(render(nodes) + "Use the key. An animal gets these answers: %s. Which animal is it?" % desc, a, R.sample(w, 3),
                "Follow the Yes or No branch at each question: it ends at the %s." % a)


def g_facts():
    pool, names, nodes, path = new_key()
    a = R.choice(names)
    if not once(("fa", tuple(sorted(names)), a)):
        return None
    steps = path[a]
    def J(xs):
        return ", ".join(xs[:-1]) + " and " + xs[-1]
    good = J([(SHORT if v else NOT)[f] for f, v, i in steps])
    flip = [((NOT if v else SHORT)[f]) for f, v, i in steps]
    wrong = []
    for j in range(len(steps)):
        alt = [(SHORT if v else NOT)[f] for f, v, i in steps]
        alt[j] = flip[j]
        wrong.append(J(alt))
    if len(steps) == 1:
        return None
    wrong.append(J(flip))
    wrong = list(dict.fromkeys(w for w in wrong if w != good))
    if len(wrong) < 3:
        return None
    return item(render(nodes) + "Use the key. What does the key tell you about the %s?" % a, "It %s." % good, ["It %s." % w for w in R.sample(wrong, 3)],
                "Read every answer on the path to the %s." % a)


def g_split():
    pool, names, nodes, path = new_key()
    a, b = R.sample(names, 2)
    pa, pb = path[a], path[b]
    k = 0
    while pa[k][2] == pb[k][2] and pa[k][1] == pb[k][1]:
        k += 1
    f = pa[k][0]
    others = [Q[x] for x in pool[a] if pool[a][x] == pool[b][x]] + ["Is it nice to look at?"]
    if len(others) < 3 or not once(("sp", tuple(sorted(names)), tuple(sorted((a, b))))):
        return None
    return item(render(nodes) + "Which question in the key separates the %s from the %s?" % (a, b), Q[f], R.sample(others, 3),
                "This is the first question where the %s and the %s take different branches." % (a, b))


def g_count():
    pool, names, nodes, path = new_key(5)
    a = R.choice(names)
    n = len(path[a])
    if not once(("co", tuple(sorted(names)), a)):
        return None
    w = [str(x) for x in (1, 2, 3, 4, 5) if x != n]
    return item(render(nodes) + "How many questions do you answer to identify the %s with this key?" % a, str(n), R.sample(w, 3),
                "Count the questions on the path from question 1 to the %s." % a)


def g_pair():
    pool = R.choice([MINI, VERT])
    a, b = R.sample(sorted(pool), 2)
    diff = [f for f in pool[a] if pool[a][f] != pool[b][f]]
    same = [f for f in pool[a] if pool[a][f] == pool[b][f]]
    if not diff or len(same) < 2 or not once(("pa", tuple(sorted((a, b))))):
        return None
    f = R.choice(diff)
    w = [Q[x] for x in R.sample(same, min(2, len(same)))] + ["Is it nice to look at?"]
    return item("Which question could you use in a key to separate %s from %s?" % (an(a), an(b)), Q[f], w,
                "A good key question has a clear yes or no answer that is different for the two animals.")


B1 = bank([
    ("What is a classification key?", "a set of questions that helps you identify a living thing", ["a key that opens a zoo", "a list of animal names in order of size", "a map of habitats"], "Keys sort living things step by step."),
    ("What kind of questions should a branching key use?", "questions with a clear yes or no answer", ["questions about opinions", "questions with many possible answers", "questions about the weather"], "Anyone should get the same answer."),
    ("Which is a bad question for a key?", "Is it cute?", ["Does it have wings?", "Does it have six legs?", "Does it have a shell?"], "Opinions differ from person to person."),
    ("Why do scientists use keys?", "to identify living things they do not know quickly and reliably", ["to make animals tame", "to count animals", "to give animals names they like"], "Keys work in the field."),
    ("In a key, what should each question do?", "split the group into two smaller groups", ["leave the group the same", "add new animals", "name every animal at once"], "Each question narrows the choices."),
    ("You reach the end of a branch in a key. What is there?", "the name of one living thing", ["another full key", "a blank space", "a list of all the animals"], "Each branch ends with one name."),
    ("Which feature is best for a key to minibeasts?", "the number of legs", ["its favourite food", "how happy it looks", "the time you saw it"], "Easy to observe and count."),
    ("A key has 6 animals. What is the fewest number of questions it needs?", "5", ["1", "2", "6"], "Each question separates one more group: 6 animals need 5 questions."),
])
B5 = bank([
    ("Two animals reach the same end of a key. What does this show?", "The key needs another question to separate them.", ["They are the same animal.", "The key is finished.", "Keys never work."], "Improve the key."),
    ("Maya's key asks 'Is it big?' Why is this a poor question?", "Big is not exact, so different people may answer differently.", ["Big animals cannot be classified.", "It has too many words.", "It is a perfect question."], "Use measurable features."),
    ("How could you improve the question 'Does it have lots of legs?'", "Change it to 'Does it have more than six legs?'", ["Change it to 'Is it scary?'", "Remove all questions.", "Ask 'Does it have legs or not legs?'"], "Make it precise."),
    ("Why might a key for garden minibeasts not work for sea creatures?", "It was built only from features of the garden animals.", ["Sea creatures have no features.", "Keys only work on land.", "Sea creatures are not living."], "A key fits its group."),
    ("A key for trees uses leaf shape. Why is this useful in winter for evergreen trees but not oak trees?", "Oak trees lose their leaves in autumn.", ["Oak trees have no leaves ever.", "Evergreen trees have no leaves.", "Leaf shape changes every day."], "Choose features you can see."),
])


def body():
    think = ("<p><b>A key asks yes/no questions that split a group again and again until one living thing is left.</b></p>"
             "<ul><li>Start at question 1. Follow Yes or No to the next question.</li>"
             "<li>Good questions are about features you can see or count: legs, wings, a shell, fur, feathers.</li>"
             "<li>Bad questions are opinions (Is it pretty?) or vague (Is it big?).</li></ul>")
    ex = [("Snail, slug, spider, bee. First question: Does it have legs?", ["Yes: spider, bee. No: snail, slug"], "It splits the group into two."),
          ("Snail or slug? Which question?", ["Only one has a shell"], "Does it have a shell?")]
    mist = ["Following the Yes branch when the answer is No.", "Using opinion questions.", "Asking a question that does not split the group."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What keys are for", B1 + [(g_pair, 12)]),
        ("Following a key", [(g_follow, 16), (g_pair, 4)]),
        ("Reading a key", [(g_facts, 12), (g_follow, 8)]),
        ("Separating animals", [(g_split, 14), (g_count, 6)]),
        ("Making better keys", B5 + [(g_count, 6), (g_split, 5), (g_facts, 4)]),
    ])
    make_uk(6, "classification-keys", 2, "Living things and their habitats",
            "Describe how living things are classified into broad groups according to common observable characteristics and based on similarities and differences, including micro-organisms, plants and animals. "
            "Give reasons for classifying plants and animals based on specific characteristics.",
            "Classification Keys",
            "Year 6 Science: Classification Keys Worksheets (Branching Keys for Animals)",
            "Classification Keys",
            "Free Year 6 science worksheets on classification keys: follow a branching key, find the question that separates two animals and write good key questions. 100 questions with answers.",
            "Yes or no, branch by branch.",
            "Each question splits the group until one living thing is left.",
            body(),
            [("How do you use a classification key?", "Start at the first question, answer yes or no, and follow that branch to the next question until you reach the name of one living thing."),
             ("What makes a good key question?", "It has a clear yes or no answer about a feature you can see or count, such as legs, wings or a shell, and it splits the group into two."),
             ("Why do keys use yes/no questions?", "Two choices make each step simple and mean that anyone using the key gets the same answer.")],
            sets)


if __name__ == "__main__":
    main()
