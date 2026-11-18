# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Adding and Taking Away to 10 (Australian Curriculum v9.0, AC9MFN05)
  python3 tools/gen_au_maths_f_adding_and_taking_away.py
Joining groups (how many now?), taking away (how many are left?), counting on and back on a number line,
deciding whether to add or take away, and everyday stories within 10.
Wrong answers come from real mistakes: counting the starting number again when counting on, giving the
number taken away instead of the number left, adding when things go away, and an off-by-one count.
"""
import random
from k_pics import two_groups_svg, crossed_row_svg, hop_line_svg, row_svg, name, KINDS
from f_common import Kids, mcq, finish, make, fig, figure, mistakes

R = random.Random(99501)


# ------------------------------------------------------------ set 1: join
def set_join(rnd):
    K = Kids(rnd)
    its = []
    plan = [(3, 1, "duck", "{a} ducks are in the pond. {b} more duck swims over."), (2, 2, "apple", "{n} has {a} apples. {He} gets {b} more."),
            (4, 1, "fish", "{a} fish are in the tank. {b} more fish is put in."), (1, 3, "star", "{n} has {a} star sticker. {He} gets {b} more."),
            (5, 2, "ball", "There are {a} balls in the basket. {n} adds {b} more."), (3, 3, "flower", "{n} picks {a} flowers, then {b} more."),
            (6, 1, "bug", "{a} ladybirds are on a leaf. {b} more ladybird lands."), (4, 3, "cup", "There are {a} cups on the table. {n} puts out {b} more."),
            (2, 5, "heart", "{n} draws {a} hearts, then {b} more."), (5, 4, "button", "{n} has {a} buttons. {He} finds {b} more."),
            (7, 2, "duck", "{a} ducks are on the grass. {b} more ducks walk over."), (6, 3, "apple", "There are {a} apples in a bowl. {n} adds {b} more."),
            (1, 1, "fish", "{a} fish is in the bowl. {b} more fish is put in."), (8, 1, "star", "{n} has {a} stars. {He} draws {b} more."),
            (3, 5, "ball", "{a} balls are on the grass. {b} more roll over."), (4, 4, "flower", "{n} plants {a} flowers, then {b} more."),
            (7, 3, "button", "{n} has {a} buttons. {He} gets {b} more."), (2, 6, "cup", "There are {a} cups. {n} brings {b} more."),
            (5, 5, "heart", "{n} cuts out {a} hearts, then {b} more."), (6, 4, "bug", "{a} ladybirds are on a log. {b} more fly over.")]
    for a, b, k, t in plan:
        kid = K.next()
        s = t.format(a=a, b=b, n=kid["n"], He=kid["He"])
        q = fig(two_groups_svg(a, k, b, k, "and")) + s + " How many now?"
        n = a + b
        its.append(mcq(q, n, [a, b, n - 1, n + 1, n + 2], "Start with %d and count on %d: %s. There are <b>%d</b> now." % (a, b, ", ".join(str(v) for v in range(a + 1, n + 1)), n)))
    return {"title": "Join: how many now?", "items": its}


# ------------------------------------------------------------ set 2: take away
def set_take(rnd):
    K = Kids(rnd)
    its = []
    plan = [(4, 1, "duck", "{a} ducks are in the pond. {b} swims away."), (5, 2, "apple", "{n} has {a} apples. {He} eats {b}."),
            (3, 1, "fish", "There are {a} fish. {b} swims off."), (6, 3, "star", "{n} has {a} stickers. {He} gives {b} away."),
            (7, 2, "ball", "There are {a} balls. {b} roll away."), (5, 4, "flower", "{a} flowers are in a vase. {b} are taken out."),
            (8, 3, "bug", "{a} ladybirds are on a leaf. {b} fly away."), (6, 1, "cup", "There are {a} cups. {n} takes {b}."),
            (9, 4, "heart", "{n} has {a} hearts. {He} gives away {b}."), (4, 4, "button", "{n} has {a} buttons. {He} loses {b}."),
            (10, 5, "duck", "{a} ducks are on the grass. {b} walk away."), (7, 4, "apple", "There are {a} apples. {n} eats {b}."),
            (8, 6, "fish", "There are {a} fish. {b} swim away."), (9, 2, "star", "{n} draws {a} stars. {He} rubs out {b}."),
            (6, 5, "ball", "There are {a} balls. {b} are put away."), (10, 3, "flower", "{a} flowers grow. {n} picks {b}."),
            (5, 1, "button", "There are {a} buttons. {b} falls on the floor."), (9, 7, "cup", "There are {a} cups. {b} are used."),
            (3, 2, "heart", "{n} has {a} hearts. {He} gives {b} away."), (10, 8, "bug", "{a} ladybirds are on a rock. {b} fly away.")]
    for a, b, k, t in plan:
        kid = K.next()
        s = t.format(a=a, b=b, n=kid["n"], He=kid["He"])
        q = fig(crossed_row_svg(a, k, b)) + s + " How many are left?"
        n = a - b
        e = "Start with %d. Take away %d. Count the ones not crossed out: <b>%d</b>%s." % (a, b, n, " (none are left)" if n == 0 else "")
        its.append(mcq(q, n, [b, a, a + b, n + 1, n - 1], e, allow_zero=True))
    return {"title": "Take away: how many are left?", "items": its}


# ------------------------------------------------------------ set 3: number line
def set_line(rnd):
    its = []
    plan = [(2, 3), (5, 2), (4, 4), (1, 5), (6, 3), (3, 1), (7, 2), (0, 4), (5, 5), (8, 2),
            (6, -2), (9, -3), (4, -1), (7, -4), (10, -5), (5, -3), (8, -6), (3, -3), (10, -2), (6, -5)]
    for s, h in plan:
        e_ = s + h
        q = fig(hop_line_svg(s, h)) + "Start at %d. Make %d hop%s %s. Where do you land?" % (s, abs(h), "" if abs(h) == 1 else "s", "forward" if h > 0 else "back")
        if h > 0:
            e = "Count on from %d: %s. You land on <b>%d</b>. Do not count the start." % (s, ", ".join(str(v) for v in range(s + 1, e_ + 1)), e_)
            wr = [e_ - 1, e_ + 1, s - h, h, e_ + 2]
        else:
            e = "Count back from %d: %s. You land on <b>%d</b>." % (s, ", ".join(str(v) for v in range(s - 1, e_ - 1, -1)), e_)
            wr = [e_ + 1, e_ - 1, s - h, abs(h), e_ + 2]
        its.append(mcq(q, e_, wr, e, allow_zero=True))
    return {"title": "Count on and count back", "items": its}


# ------------------------------------------------------------ set 4: add or take away?
def set_which(rnd):
    K = Kids(rnd)
    its = []
    plan = [("{n} has {a} crayons. {He} gets {b} more.", 4, 2, "+"), ("{n} has {a} crayons. {He} gives {b} away.", 6, 2, "-"),
            ("There are {a} birds. {b} fly away.", 7, 3, "-"), ("There are {a} birds. {b} more land.", 5, 3, "+"),
            ("{n} has {a} biscuits. {He} eats {b}.", 8, 4, "-"), ("{n} has {a} biscuits. Mum gives {him} {b} more.", 3, 4, "+"),
            ("{a} children are on the bus. {b} get off.", 9, 5, "-"), ("{a} children are on the bus. {b} get on.", 6, 2, "+"),
            ("{n} builds a tower of {a} blocks. {He} adds {b}.", 5, 4, "+"), ("{n} builds a tower of {a} blocks. {b} fall off.", 8, 2, "-"),
            ("{a} frogs sit on a log. {b} jump into the water.", 7, 5, "-"), ("{a} frogs sit on a log. {b} more jump on.", 2, 5, "+"),
            ("{n} has {a} balloons. {b} pop.", 6, 1, "-"), ("{n} has {a} balloons. {He} buys {b} more.", 6, 3, "+"),
            ("There are {a} cars in the car park. {b} drive away.", 10, 4, "-"), ("There are {a} cars in the car park. {b} more arrive.", 3, 6, "+"),
            ("{n} has {a} shells. {He} finds {b} more.", 1, 7, "+"), ("{n} has {a} shells. {He} drops {b}.", 9, 6, "-"),
            ("{a} kids play in the sandpit. {b} go home.", 5, 5, "-"), ("{a} kids play in the sandpit. {b} more come.", 4, 6, "+")]
    for t, a, b, op in plan:
        kid = K.next()
        s = t.format(a=a, b=b, n=kid["n"], He=kid["He"], him="her" if kid["he"] == "she" else "him")
        n = a + b if op == "+" else a - b
        other = a - b if op == "+" else a + b
        right = ("Add. There are %d now." % n) if op == "+" else ("Take away. There are %d left." % n)
        wr = [("Take away. There are %d left." % other) if op == "+" and other >= 0 else ("Take away. There are %d left." % b) if op == "+" else ("Add. There are %d now." % other),
              ("Add. There are %d now." % (n + 1)) if op == "+" else ("Take away. There are %d left." % b if b != n else "Take away. There are %d left." % (n + 1)),
              ("Take away. There are %d left." % a) if op == "+" else ("Add. There are %d now." % (n + 1))]
        e = ("Things are joined, so we add: %d and %d make <b>%d</b>." % (a, b, n)) if op == "+" else ("Things go away, so we take away: %d take away %d leaves <b>%d</b>." % (a, b, n))
        its.append(mcq(s + " Do we add or take away? How many?", right, wr, e))
    return {"title": "Add or take away?", "items": its}


# ------------------------------------------------------------ set 5: stories
def set_story(rnd):
    K = Kids(rnd)
    its = []
    stories = [("{n} has 4 toy cars. {He} gets 3 more for {his} birthday. How many cars does {he} have now?", 7, [4, 3, 6, 8]),
               ("There are 9 muffins. The class eats 4. How many muffins are left?", 5, [4, 9, 13, 6]),
               ("{n} sees 2 koalas in one tree and 3 koalas in another tree. How many koalas?", 5, [2, 3, 4, 6]),
               ("There are 6 boats on the river. 6 sail away. How many boats are left?", 0, [6, 12, 1, 2]),
               ("{n} has 5 pencils. {He} finds 5 more. How many pencils now?", 10, [5, 9, 11, 0]),
               ("{n} blows 8 bubbles. 2 pop. How many bubbles are left?", 6, [2, 8, 10, 5]),
               ("There are 3 eggs in a nest. 3 more eggs are laid. How many eggs now?", 6, [3, 5, 7, 0]),
               ("{n} has 10 grapes. {He} eats 7. How many grapes are left?", 3, [7, 10, 17, 4]),
               ("{n} has 1 dog and 2 cats. How many pets does {he} have?", 3, [1, 2, 4, 12]),
               ("There are 7 children on the slide. 1 goes down and runs away. How many are still on the slide?", 6, [1, 7, 8, 5]),
               ("{n} puts 6 forks on the table. Then {he} puts 2 more. How many forks?", 8, [6, 2, 7, 9]),
               ("There are 5 pegs on the line. The wind blows 3 away. How many pegs are left?", 2, [3, 5, 8, 1]),
               ("{n} reads 2 books on Monday and 2 books on Tuesday. How many books does {he} read?", 4, [2, 3, 5, 22]),
               ("There are 10 seats. 4 children sit down. How many seats are empty?", 6, [4, 10, 14, 5]),
               ("{n} catches 3 fish, then 4 more. How many fish does {he} catch?", 7, [3, 4, 6, 8]),
               ("There are 8 crayons in a box. {n} takes out 5. How many are still in the box?", 3, [5, 8, 13, 2]),
               ("{n} has 0 stickers. {He} gets 4. How many stickers now?", 4, [0, 3, 5, 1]),
               ("There are 9 ants. 9 go into the hole. How many ants are outside?", 0, [9, 18, 1, 8]),
               ("{n} jumps 5 times, then 3 more times. How many jumps?", 8, [5, 3, 7, 9]),
               ("There are 7 lollies. {n} gives 2 to a friend. How many are left?", 5, [2, 7, 9, 4])]
    for t, ans, wr in stories:
        kid = K.next()
        q = t.format(n=kid["n"], He=kid["He"], he=kid["he"], his=kid["his"])
        joined = any(w in t for w in ["more", " and ", "gets", "puts", "catches"]) and "left" not in t and "empty" not in t and "outside" not in t and "still" not in t
        e = ("We join the groups and count on: <b>%d</b>." % ans) if joined else ("We take away and count what is left: <b>%d</b>." % ans)
        its.append(mcq(q, ans, wr, e, allow_zero=True))
    return {"title": "Adding and taking away stories", "items": its}


def body():
    return (
        "<h2>Adding: join and count on</h2>"
        "<p>When more things come, the group gets <b>bigger</b>. Start with the first number and count on.</p>"
        + figure(two_groups_svg(5, "duck", 2, "duck", "and"), "5 ducks and 2 more: 6, 7. There are 7 now.")
        + "<h2>Taking away: what is left?</h2><p>When things go away, the group gets <b>smaller</b>. Cross them out and count the rest.</p>"
        + figure(crossed_row_svg(6, "apple", 2), "6 apples, 2 are eaten: 4 are left.")
        + "<h2>Use a number line</h2><p>Hop forward to add. Hop back to take away. Do not count the number you start on.</p>"
        + figure(hop_line_svg(4, 3), "Start at 4, hop 3 forward: 5, 6, 7.")
        + mistakes([["Counting the starting number again", "Start on the number, then count the hops"],
                    ["Giving the number taken away", "Count the ones that are left"],
                    ["Adding when things go away", "Ask: does the group get bigger or smaller?"]]))


FAQ = [("How do Foundation students learn to add and subtract?",
        "They act out and draw everyday situations with objects, fingers and number lines, and use counting on, counting back or subitising (AC9MFN05). Symbols like + and − are not needed yet."),
       ("What is counting on?",
        "Starting from the first number and counting forward. For 5 and 3, say 5 in your head, then 6, 7, 8."),
       ("Why does my child get 7 instead of 6 for 4 and 2?",
        "They may be counting the starting number again (4, 5, 6, 7). Show that you start on 4 and then count 2 more: 5, 6."),
       ("How can I practise adding and taking away at home?",
        "Use snacks, toys or bath toys: put out 5, add 2, ask how many now. Eat or hide some and ask how many are left.")]


def build():
    sets = [set_join(R), set_take(R), set_line(R), set_which(R), set_story(R)]
    finish(sets, R, max_num=22)
    make("adding-and-taking-away", 5, "AC9MFN05", "Number",
         "Adding and Taking Away to 10",
         "Foundation Addition and Subtraction Worksheets: Adding and Taking Away to 10 (Free, with Answers)",
         "Adding and taking away",
         "Represent practical situations involving addition, subtraction and quantification with physical and virtual materials and use counting or subitising strategies.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on adding and taking away to 10, matched to the Australian Curriculum (AC9MFN05): join groups, take away, count on and back on a number line, and everyday stories. 100 picture questions with answers.",
         "Adding makes the group bigger. Taking away makes it smaller.",
         "Count on from the first number to add. Count what is left to take away.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
