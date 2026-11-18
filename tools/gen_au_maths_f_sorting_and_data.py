# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Sorting and Data (Australian Curriculum v9.0, AC9MFST01)
  python3 tools/gen_au_maths_f_sorting_and_data.py
Sort a mixed collection and count one kind, sort by a rule (what belongs and what does not), read a picture
graph, compare the rows of a picture graph, and ask and answer investigative questions about the class.
Wrong answers come from real mistakes: counting every object instead of one kind, reading the longest row
as the fewest, giving one of the two counts instead of how many more, and asking a question nobody can
answer by collecting data.
"""
import random
from k_pics import mixed_svg, name, KINDS
from f_common import Kids, mcq, finish, make, fig, figure, mistakes, pictograph_svg

R = random.Random(100201)


# ------------------------------------------------------------ set 1: sort and count
def set_count(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        ks = rnd.sample(KINDS, 3)
        counts = [rnd.randint(2, 7) for _ in ks]
        if sum(counts) > 24 or len(set(counts)) < 3:
            continue
        j = len(its) % 3
        key = (tuple(ks), tuple(counts), j)
        if key in seen:
            continue
        seen.add(key)
        svg = mixed_svg(list(zip(ks, counts)), 4000 + len(its))
        k, n = ks[j], counts[j]
        q = fig(svg) + "Sort the things. How many <b>%s</b> are there?" % name(k)
        its.append(mcq(q, n, [sum(counts), counts[(j + 1) % 3], n + 1, n - 1, n + 2], "Find only the %s and count each one once: <b>%d</b>." % (name(k), n)))
    return {"title": "Sort and count", "items": its}


# ------------------------------------------------------------ set 2: sorting rules
GROUPS = {"fruit": ["apple", "banana", "orange", "pear", "grapes", "mango"], "pets": ["dog", "cat", "rabbit", "goldfish", "guinea pig", "budgie"],
          "things that fly": ["kite", "hot air balloon", "rocket", "drone", "paper plane", "frisbee"], "clothes": ["hat", "sock", "shirt", "shoe", "jumper", "skirt"],
          "things with wheels": ["car", "bike", "bus", "skateboard", "pram", "truck"], "sea animals": ["shark", "whale", "crab", "octopus", "dolphin", "jellyfish"]}


def set_rules(rnd):
    its = []
    seen = set()
    cats = list(GROUPS)
    while len(its) < 20:
        g = cats[len(its) % len(cats)]
        other = rnd.choice([c for c in cats if c != g])
        three = rnd.sample(GROUPS[g], 3)
        odd = rnd.choice([x for x in GROUPS[other] if x not in GROUPS[g]])
        key = (tuple(sorted(three)), odd)
        if key in seen:
            continue
        seen.add(key)
        if len(its) % 2 == 0:
            items = three + [odd]
            rnd.shuffle(items)
            q = "These things are being sorted into <b>%s</b>: %s. Which one does <b>not</b> belong?" % (g, ", ".join(items))
            wr = [x for x in items if x != odd] + ["They all belong"]
            its.append(mcq(q, odd, wr, "%s %s is not one of the %s. The others are. <b>%s</b> does not belong." % ("An" if odd[0] in "aeiou" else "A", odd, g, odd.capitalize())))
        else:
            q = "%s, %s and %s are in one group. What is the sorting rule?" % tuple(x.capitalize() if i == 0 else x for i, x in enumerate(three))
            ans = g.capitalize()
            wr = [c.capitalize() for c in cats if c != g and not set(three) & set(GROUPS[c])][:3] + ["Things that are red", "Things that are big"]
            its.append(mcq(q, ans, wr, "All three are %s. The rule is <b>%s</b>." % (g, g)))
    return {"title": "Sorting rules", "items": its}


# ------------------------------------------------------------ set 3: read a picture graph
FRUITS = ["apple", "star", "duck", "ball", "fish", "flower", "heart", "cup", "bug", "button"]


def set_read(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        ks = rnd.sample(FRUITS, 3)
        ns = rnd.sample(range(1, 9), 3)
        kind = len(its) % 4
        key = (tuple(ks), tuple(ns), kind)
        if key in seen:
            continue
        seen.add(key)
        svg = pictograph_svg(list(zip(ks, ns)))
        pre = fig(svg) + "Children chose their favourite picture. Each picture in a row shows one child. "
        if kind in (0, 1):
            j = rnd.randrange(3)
            q = pre + "How many children chose the <b>%s</b>?" % name(ks[j], 1)
            its.append(mcq(q, ns[j], [sum(ns), ns[(j + 1) % 3], ns[j] + 1, ns[j] - 1, ns[j] + 2], "Count the pictures in the %s row: <b>%d</b>." % (name(ks[j], 1), ns[j])))
        elif kind == 2:
            j = ns.index(max(ns))
            q = pre + "Which picture did the <b>most</b> children choose?"
            ans = "The " + name(ks[j], 1)
            its.append(mcq(q, ans, ["The " + name(k, 1) for k in ks if k != ks[j]] + ["They are all the same"], "The %s row is the longest, with %d. <b>%s</b>." % (name(ks[j], 1), ns[j], ans)))
        else:
            j = ns.index(min(ns))
            q = pre + "Which picture did the <b>fewest</b> children choose?"
            ans = "The " + name(ks[j], 1)
            its.append(mcq(q, ans, ["The " + name(k, 1) for k in ks if k != ks[j]] + ["They are all the same"], "The %s row is the shortest, with %d. <b>%s</b>." % (name(ks[j], 1), ns[j], ans)))
    return {"title": "Read a picture graph", "items": its}


# ------------------------------------------------------------ set 4: compare
def set_compare(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        ks = rnd.sample(FRUITS, 3)
        ns = rnd.sample(range(2, 10), 3)
        kind = len(its) % 4
        key = (tuple(ks), tuple(ns), kind)
        if key in seen:
            continue
        seen.add(key)
        svg = pictograph_svg(list(zip(ks, ns)))
        pre = fig(svg) + "Each picture shows one child's vote. "
        a, b = 0, 1
        A, B = name(ks[a], 1), name(ks[b], 1)
        if kind == 0:
            d = abs(ns[a] - ns[b])
            big, small = (A, B) if ns[a] > ns[b] else (B, A)
            q = pre + "How many more children chose the %s than the %s?" % (big, small)
            its.append(mcq(q, d, [max(ns[a], ns[b]), min(ns[a], ns[b]), d + 1, ns[a] + ns[b], d + 2], "Line up the rows. The %s row has <b>%d</b> more." % (big, d)))
        elif kind == 1:
            q = pre + "How many children voted altogether?"
            t = sum(ns)
            its.append(mcq(q, t, [max(ns), t - 1, t + 1, len(ns)], "Add the rows: %s make <b>%d</b>." % (" and ".join(str(n) for n in ns), t)))
        elif kind == 2:
            q = pre + "Did more children choose the %s or the %s?" % (A, B)
            ans = "The " + (A if ns[a] > ns[b] else B)
            its.append(mcq(q, ans, ["The " + (B if ns[a] > ns[b] else A), "The same number", "We cannot tell"], "The %s row has %d and the %s row has %d. <b>%s</b>." % (A, ns[a], B, ns[b], ans)))
        else:
            order = sorted(range(3), key=lambda j: -ns[j])
            q = pre + "Put the choices in order, <b>most</b> votes first."
            ans = ", ".join(name(ks[j], 1) for j in order)
            wr = [", ".join(name(ks[j], 1) for j in order[::-1]), ", ".join(name(k, 1) for k in ks) if [0, 1, 2] != order else ", ".join(name(ks[j], 1) for j in [1, 0, 2]),
                  ", ".join(name(ks[j], 1) for j in [order[1], order[0], order[2]]), ", ".join(name(ks[j], 1) for j in [order[0], order[2], order[1]])]
            its.append(mcq(q, ans, wr, "Longest row first: <b>%s</b>." % ans))
    return {"title": "Compare the data", "items": its}


# ------------------------------------------------------------ set 5: investigative questions
EXPL = ['A good question asks everyone the same thing about fruit, and each answer can be counted.', 'Ask everyone the same question, then sort and count the answers.', '12 is more than 8, so more children said yes.', '12 and 8 make 20 children.', '9 is more than 6, so Spot wins.', '9 take away 6 is 3: Spot gets 3 more votes.', 'You can ask your classmates about their favourite colour and count the answers.', '7 is the biggest number, so swimming is the favourite.', '3 is the smallest number, so the fewest chose cricket.', '11 and 7 make 18 lunches.', 'Sorting and counting helps us answer a question and compare groups.', '6 is the biggest number, so red is the most common.', 'Red has 6 and blue has 2. 6 take away 2 is 4.', '10 and 10 are the same, so the same number said yes and no.', 'Each child votes once, so every vote can be counted fairly.', '16 take away 9 leaves 7 who chose green.', 'Lining up each group makes them easy to count and compare.', '8 friends, 3 say yes, so 8 take away 3 is 5 say no.', 'You can look at your classmates and count, so this data can be collected in the classroom.', '8 and 8 are the same number of votes, so it is a tie.']


def set_questions(rnd):
    K = Kids(rnd)
    its = []
    plan = [("The class wants to find out which fruit is the class favourite. Which is the best question to ask everyone?", "Which fruit do you like best?",
             ["Do you like school?", "How old is your teacher?", "What is 2 and 2?"]),
            ("The class wants to know how children get to school. What should they do?", "Ask every child how they get to school and count the answers",
             ["Ask only one child", "Guess", "Count the cars in the car park"]),
            ("{n} asks the class: Do you have a pet? 12 say yes and 8 say no. Did more children say yes or no?", "Yes", ["No", "The same number", "We cannot tell"]),
            ("{n} asks: Do you have a pet? 12 say yes and 8 say no. How many children were asked?", "20", ["12", "8", "4"]),
            ("The class votes for a class pet name: Spot gets 9 votes and Max gets 6. Which name wins?", "Spot", ["Max", "Both names", "Neither name"]),
            ("Spot gets 9 votes and Max gets 6. How many more votes does Spot get?", "3", ["9", "6", "15"]),
            ("Which question could you answer by asking your classmates?", "What colour is your favourite?", ["How far away is the Moon?", "What will the weather be next year?", "How many fish are in the sea?"]),
            ("{n} wants to know the class's favourite sport. 5 chose footy, 7 chose swimming and 3 chose cricket. Which sport is the favourite?", "Swimming", ["Footy", "Cricket", "All the same"]),
            ("5 chose footy, 7 chose swimming and 3 chose cricket. Which sport did the fewest choose?", "Cricket", ["Footy", "Swimming", "All the same"]),
            ("The class sorts their lunches into sandwiches and wraps. There are 11 sandwiches and 7 wraps. How many lunches altogether?", "18", ["11", "7", "4"]),
            ("Why do we sort and count data?", "To answer a question and compare groups", ["To make the room messy", "Because counting is only for numbers", "To guess the answer"]),
            ("{n} counts the colours of the cars in the car park: 4 white, 6 red and 2 blue. Which colour is most common?", "Red", ["White", "Blue", "Green"]),
            ("4 white, 6 red and 2 blue cars. How many fewer blue cars than red cars?", "4", ["2", "6", "8"]),
            ("{n} asks: Do you like rain? 10 say yes and 10 say no. What can {he} say?", "The same number said yes and no", ["More said yes", "More said no", "Nobody answered"]),
            ("The class wants to know which day of the week is the favourite. What should each child do?", "Choose one day and vote once", ["Vote for every day", "Not vote", "Vote 5 times"]),
            ("16 children voted for their favourite colour. Blue got 9 votes and the rest chose green. How many chose green?", "7", ["9", "16", "25"]),
            ("The class sorts the toys box into balls and blocks. How should they show how many of each?", "Put each group in a line and count", ["Mix them all up", "Count only the balls", "Throw them in the box"]),
            ("{n} asks 8 friends: Do you walk to school? 3 say yes. How many say no?", "5", ["3", "8", "11"]),
            ("Which data could you collect in your classroom?", "How many children have brown hair", ["How many people live in Sydney", "How many stars are in the sky", "How tall a giraffe is"]),
            ("The class votes for a book to read. Possum Magic gets 8 votes and the other book gets 8 votes. What can they say?", "It is a tie", ["Possum Magic wins", "The other book wins", "Nobody voted"])]
    for (t, ans, wr), e in zip(plan, EXPL):
        kid = K.next()
        q = t.format(n=kid["n"], he=kid["he"])
        its.append(mcq(q, ans, wr, "%s <b>%s</b>." % (e, ans)))
    return {"title": "Asking questions and using data", "items": its}


def body():
    return (
        "<h2>Sort, then count</h2>"
        "<p>To answer a question, <b>collect</b> the data (ask, look or count), <b>sort</b> it into groups, then <b>count</b> each group.</p>"
        + figure(mixed_svg([("apple", 4), ("star", 3), ("duck", 5)], 77), "Sort into apples, stars and ducks, then count each kind.")
        + "<h2>Picture graphs</h2><p>A picture graph shows each answer as one picture. The longest row has the most. The shortest row has the fewest.</p>"
        + figure(pictograph_svg([("apple", 6), ("star", 3), ("duck", 4)]), "6 chose the apple, 3 the star and 4 the duck. The apple is the favourite.")
        + mistakes([["Counting everything instead of one kind", "Sort first, then count one group"],
                    ["Reading the longest row as the fewest", "Longest row means the most"],
                    ["Giving one of the counts for 'how many more'", "Find the difference between the rows"]]))


FAQ = [("What data do Foundation students learn about?",
        "They collect, sort and compare data shown with objects and pictures to answer simple questions about familiar things, like the class's favourite fruit (AC9MFST01)."),
       ("What is a picture graph?",
        "A graph where each picture stands for one thing or one person. Rows of pictures make it easy to see which group has the most."),
       ("What is an investigative question?",
        "A question you can answer by collecting data, such as: What is our class's favourite colour? or How do we get to school?"),
       ("How can I practise data at home?",
        "Sort the washing by colour, count the cars that go past by colour, or vote on dinner with family members and line up the votes.")]


def build():
    sets = [set_count(R), set_rules(R), set_read(R), set_compare(R), set_questions(R)]
    finish(sets, R, max_num=30)
    make("sorting-and-data", 12, "AC9MFST01", "Statistics",
         "Sorting and Data: Picture Graphs",
         "Foundation Data Worksheets: Sorting, Counting and Picture Graphs (Free, with Answers)",
         "Sorting and data",
         "Collect, sort and compare data represented by objects and images in response to given investigative questions that relate to familiar situations.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on sorting and data, matched to the Australian Curriculum (AC9MFST01): sort and count, sorting rules, picture graphs, most and fewest, and asking questions. 100 picture questions with answers.",
         "Collect, sort, then count to answer a question.",
         "In a picture graph each picture is one thing. The longest row has the most.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
