# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Energy in Collisions (4-PS3-3)
  python tools/gen_us_science_g4_collisions.py
When objects collide, energy moves between them: the moving object slows down and the object it hits
speeds up. Some energy changes into sound and heat, and objects can change shape.
Faster collisions move more energy (louder sounds, bigger dents, objects pushed farther).
Assessment boundary: qualitative changes only, no calculations of energy.
Wrong answers come from real mistakes: "energy disappears in a crash", "the hit object gets no energy",
"sound has nothing to do with energy".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, figure, svg_wrap, circle, line, arrow, text, People, INK, BLUE, RED

U = Unit(40105)
R = U.R
P = People(R)
# (mover, object hit, short name of the object hit, observations [(what you notice, energy form)])
PAIRS = [("a rolling marble", "a marble at rest", "the second marble", [("you hear a click", "sound"), ("the second marble rolls away", "motion")]),
         ("a cue ball", "a pool ball", "the pool ball", [("you hear a clack", "sound"), ("the pool ball rolls into a pocket", "motion")]),
         ("a bowling ball", "a pin", "the pin", [("you hear a crash", "sound"), ("the pin flies to the side", "motion")]),
         ("a bumper car", "a parked bumper car", "the parked car", [("you hear a bump", "sound"), ("the parked car rolls forward", "motion")]),
         ("a kicking foot", "a soccer ball", "the ball", [("the ball squashes for a moment", "shape"), ("the ball flies down the field", "motion"), ("you hear a thump", "sound")]),
         ("a hammer", "a nail", "the nail", [("the nail goes into the wood", "motion"), ("you hear a bang", "sound"), ("the nail feels warm", "heat")]),
         ("a rolling toy truck", "a block tower", "the tower", [("the blocks fall over", "motion"), ("you hear the blocks clatter", "sound")]),
         ("a baseball bat", "a baseball", "the baseball", [("you hear a crack", "sound"), ("the ball flies into the outfield", "motion")]),
         ("a golf club", "a golf ball", "the golf ball", [("you hear a click", "sound"), ("the ball flies far", "motion")]),
         ("a moving cart", "a cardboard box", "the box", [("the box slides across the floor", "motion"), ("the box gets a dent", "shape")]),
         ("a car", "a wall", "the wall", [("the bumper bends", "shape"), ("you hear a loud crunch", "sound"), ("the metal gets warm", "heat")]),
         ("a falling apple", "the ground", "the ground", [("the apple gets a bruise", "shape"), ("you hear a thud", "sound")]),
         ("a tennis racket", "a tennis ball", "the ball", [("the ball squashes for a moment", "shape"), ("you hear a pop", "sound"), ("the ball flies over the net", "motion")])]
FORM = {"sound": "Some energy changed into sound.", "heat": "Some energy changed into heat.",
        "motion": "Energy was transferred to the other object and made it move.", "shape": "Some energy went into changing the object's shape."}
BAD = ["Energy was destroyed.", "The objects made new energy.", "The objects got heavier.", "No energy was involved."]


def cap(s):
    return s[0].upper() + s[1:]


def the(s):
    return "the " + s.split(" ", 1)[1] if s.startswith(("a ", "an ")) else s


def marbles(label="a moving marble about to hit a marble at rest"):
    s = [line(10, 70, 350, 70, INK, 2), circle(80, 56, 13, BLUE, INK, 1.5), circle(220, 56, 13, RED, INK, 1.5),
         arrow(100, 56, 150, 56, INK, 2.5, 9), text(80, 92, "moving", 12, weight=400), text(220, 92, "at rest", 12, weight=400)]
    return svg_wrap(360, 100, "".join(s), label)


def g_after():
    a, b, bn, _ = R.choice(PAIRS)
    if b in ("a wall", "the ground"):
        return None
    if R.random() < 0.5:
        return item("%s hits %s. What happens to %s?" % (cap(a), b, bn),
                    "It gets energy and starts to move.", ["Nothing happens; it gets no energy.", "It gives all its energy to %s." % the(a), "It moves backward toward %s." % the(a)],
                    "Energy is transferred from the moving object to the object it hits.")
    return item("%s hits %s. What happens to %s right after the collision?" % (cap(a), b, the(a)),
                "It slows down because it gave some of its energy away.", ["It speeds up.", "It gets energy from %s." % bn, "Its speed does not change at all."],
                "The moving object transfers energy, so it has less energy of motion and slows down.")


def g_obs():
    a, b, bn, obs = R.choice(PAIRS)
    o, f = R.choice(obs)
    return item("%s hits %s, and %s. What does this show?" % (cap(a), b, o), FORM[f],
                R.sample(BAD, 3),
                "When objects collide, energy moves to the other object or changes into sound, heat or a change of shape.")


def g_evidence():
    a, b, bn, obs = R.choice(PAIRS)
    f = R.choice(["sound", "heat", "shape", "motion"])
    match = [o for o, x in obs if x == f]
    if not match:
        return None
    others = ["%s changes color" % bn, "the air gets colder", "%s gets heavier" % bn, "the sun gets brighter", "%s disappears" % the(a)]
    ask = {"sound": "energy changed into sound", "heat": "energy changed into heat", "shape": "energy went into changing a shape",
           "motion": "energy was transferred to %s" % bn}[f]
    return item("%s hits %s. Which observation is evidence that %s?" % (cap(a), b, ask), match[0], R.sample(others, 3),
                "Sound, warmth, dents and motion are evidence of energy changes in a collision.")


def g_speed():
    a, b, bn, obs = R.choice(PAIRS)
    if b == "the ground":
        return None
    k = R.choice(["louder", "farther", "dent"])
    if k == "farther" and b == "a wall":
        return None
    if k == "dent" and "shape" not in [x for _, x in obs]:
        return None
    q = {"louder": "Which collision makes a louder sound?", "farther": "After which collision does %s move farther?" % bn,
         "dent": "Which collision is more likely to dent or bend something?"}[k]
    return item("%s hits %s two times, once slowly and once quickly. %s" % (cap(a), b, q), "the fast collision",
                ["the slow collision", "Both are exactly the same.", "Speed does not matter in a collision."],
                "The faster object has more energy, so more energy moves and changes form in the collision.")


def g_table():
    speeds = ["slow", "medium", "fast"]
    ds = sorted(R.sample(range(8, 70), 3))
    obj = R.choice(["marble", "toy car", "ball"])
    tgt = R.choice(["block", "cup", "box"])
    rows = [[s_, "%d cm" % d] for s_, d in zip(speeds, ds)]
    k = R.choice(["most", "pattern", "least", "sound"])
    p = P.next()
    tab = table(["Speed of the %s" % obj, "How far the %s moved" % tgt], rows)
    if k == "most":
        return item(tab + "%s rolled a %s into a %s at three speeds. In which trial did the %s get the most energy?" % (p[0], obj, tgt, tgt),
                    "fast", ["slow", "medium", "All trials gave the same energy."], "The %s moved farthest (%d cm) after the fast collision." % (tgt, ds[2]))
    if k == "least":
        return item(tab + "%s rolled a %s into a %s at three speeds. In which trial did the %s get the least energy?" % (p[0], obj, tgt, tgt),
                    "slow", ["fast", "medium", "All trials gave the same energy."], "The %s moved the shortest distance (%d cm) after the slow collision." % (tgt, ds[0]))
    if k == "pattern":
        return item(tab + "%s rolled a %s into a %s. What does the data show?" % (p[0], obj, tgt), "A faster %s transfers more energy to the %s." % (obj, tgt),
                    ["A slower %s transfers more energy." % obj, "Speed does not change the energy transferred.", "The %s gives energy to the %s." % (tgt, obj)],
                    "From slow to fast, the distance grew from %d cm to %d cm." % (ds[0], ds[2]))
    return item(tab + "%s rolled a %s into a %s. In which trial would the crash most likely sound the loudest?" % (p[0], obj, tgt), "fast", ["slow", "medium", "They all sound the same."],
                "The fastest collision has the most energy, and more energy changes into sound.")


def g_pic():
    k = R.choice(["red", "blue", "sound", "energy"])
    if k == "red":
        return item(fig(marbles()) + "The blue marble hits the red marble, which was at rest. What happens to the red marble?",
                    "It starts moving to the right.", ["It stays still.", "It moves to the left toward the blue marble.", "It sinks into the floor."],
                    "The blue marble transfers some energy to the red marble, which moves in the same direction.")
    if k == "blue":
        return item(fig(marbles()) + "The blue marble hits the red marble. What happens to the blue marble's speed?",
                    "It slows down or stops.", ["It speeds up.", "It stays exactly the same.", "It doubles."],
                    "It gave some of its energy to the red marble.")
    if k == "energy":
        return item(fig(marbles()) + "Before the collision, which marble has energy of motion?", "only the blue marble",
                    ["only the red marble", "both marbles", "neither marble"], "Only the blue marble is moving, so only it has energy of motion.")
    return item(fig(marbles()) + "The marbles click when they hit. What does the click show?", "Some energy changed into sound.",
                ["Energy was destroyed.", "The marbles made new energy.", "The marbles got lighter."], "Sound is one way energy leaves a collision.")


B1 = bank([
    ("What is a collision?", "when two objects hit each other", ["when an object stops by itself", "when an object is at rest", "when two objects never touch"],
     "Balls, cars and bowling pins collide when they hit each other."),
    ("When a moving ball hits a ball at rest, energy moves", "from the moving ball to the ball at rest", ["from the ball at rest to the moving ball", "out of both balls and disappears", "only into the floor"],
     "The moving ball has energy of motion and passes some of it on."),
    ("Where does some energy go when two cars bump?", "into sound, heat and bending the metal", ["nowhere; it disappears", "into making the cars heavier", "into light from the sun"],
     "Energy is not destroyed; it changes into other forms."),
    ("Why do your hands feel warm after clapping hard?", "Some energy of motion changes into heat.", ["Clapping makes cold air.", "Your hands get heavier.", "Sound is warm."],
     "Collisions change some energy into heat."),
    ("Which collision would make the loudest sound?", "a fast car hitting a wall", ["a slow car touching a wall", "a car parked by a wall", "a feather landing on a wall"],
     "More energy in the collision means more energy can change into sound."),
    ("Is energy destroyed in a collision?", "No. It moves to other objects or changes into sound and heat.", ["Yes, all of it.", "Yes, half of it.", "Only in fast collisions."],
     "Energy changes form or moves; it is not destroyed."),
    ("A hammer hits a nail. Where does the hammer's energy go?", "into pushing the nail into the wood, sound and heat", ["back into your arm only", "into the air as light", "nowhere"],
     "The nail moves, you hear a bang and the nail gets warm."),
    ("Why do car bumpers crumple in a crash?", "Changing shape uses up some of the energy, so less reaches the people inside.", ["To make the car lighter.", "To make the crash louder.", "To add energy."],
     "Crumple zones turn energy into changing the car's shape."),
])
B5 = bank([
    ("Ava rolls a ball into a cup from three ramp heights. What is she testing?", "how the ball's speed changes the energy it gives the cup", ["how heavy the cup is", "how big the ramp is", "the color of the ball"],
     "Higher starts make faster balls; she measures how far the cup moves."),
    ("Leo designs a bumper for a toy car so it hits a wall gently. Which material would work best?", "a soft foam pad", ["a hard steel plate", "a glass sheet", "nothing at all"],
     "Foam changes shape and slows the car over a longer time."),
    ("Why do helmets have foam inside?", "The foam squeezes and takes in energy so less reaches your head.", ["Foam makes the helmet heavier.", "Foam stores electricity.", "Foam makes the helmet louder."],
     "The foam changes shape during a hit."),
    ("In a game of marbles, a fast shot knocks a marble out of the circle, but a slow shot does not. What does this show?", "A faster marble transfers more energy.", ["Slow marbles have more energy.", "Marbles have no energy.", "Only big marbles transfer energy."],
     "More speed, more energy to pass on."),
    ("A ball dropped on the floor bounces lower each time. Why?", "Some energy changes into sound and heat each bounce.", ["Energy is destroyed.", "The floor gets lighter.", "The ball gets heavier."],
     "Each bounce changes some energy into other forms, so less is left for motion."),
])


def body():
    think = ("<p>When objects <b>collide</b>, energy moves between them. The moving object slows down, and the object it hits gets energy and starts to move.</p>"
             "<p>Some energy also changes into <b>sound</b> (a bang or click), <b>heat</b> (things get a little warmer) and <b>changes of shape</b> (dents). "
             "Energy is not destroyed. A <b>faster</b> collision moves more energy: louder sounds, bigger dents and objects pushed farther.</p>"
             + figure(marbles(), "The blue marble gives some of its energy to the red marble."))
    ex = [("A cue ball hits a pool ball at rest. What happens?", ["Energy moves from the cue ball to the pool ball.", "The cue ball slows; the pool ball moves."], "The pool ball moves and the cue ball slows down."),
          ("Two cars bump. You hear a crash. What does the sound show?", ["Some energy changed into sound."], "Energy changed form.")]
    mist = ["Thinking energy disappears in a crash. It moves or changes form.",
            "Thinking the object that is hit gets no energy.",
            "Forgetting sound and heat as ways energy leaves a collision."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What happens in a collision", B1 + [(g_pic, 4), (g_after, 4), (g_obs, 4)]),
        ("Energy moves between objects", [(g_after, 8), (g_pic, 4), (g_evidence, 4), (g_obs, 4)]),
        ("Where the energy goes", [(g_obs, 8), (g_evidence, 8), (g_speed, 4)]),
        ("Faster collisions and data", [(g_table, 10), (g_speed, 10)]),
        ("Designs and investigations", B5 + [g_table, g_speed, g_evidence, g_obs]),
    ])
    make("grade-4", "collisions", 5, "4-PS3-3",
         "Ask questions and predict outcomes about the changes in energy that occur when objects collide.",
         "Energy in Collisions",
         "Grade 4 Collisions Worksheets: How Energy Moves When Objects Hit",
         "Collisions",
         "Free Grade 4 science worksheets on energy in collisions (NGSS 4-PS3-3): energy moving between objects, sound, heat and changes of shape, and faster collisions with data tables. 100 practice questions with answers.",
         "In a collision, energy moves between the objects.",
         "The moving object slows down and the object it hits speeds up. Some energy changes into sound and heat.",
         body(),
         [("What happens to energy when objects collide?", "Energy moves from the moving object to the object it hits. Some changes into sound, heat and changes of shape. None is destroyed."),
          ("Why does a faster collision make a louder sound?", "A faster object has more energy, so more energy can change into sound."),
          ("Why do helmets and bumpers have soft parts?", "Soft materials change shape and take in energy, so less energy reaches your head or the people in a car.")],
         sets)


if __name__ == "__main__":
    main()
