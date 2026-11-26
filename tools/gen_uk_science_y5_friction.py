# -*- coding: utf-8 -*-
"""
UK Year 5 science: Friction (Forces)
  python tools/gen_uk_science_y5_friction.py
Friction between moving surfaces: which way it acts, rough and smooth surfaces, when friction is useful and when it is
a problem, ways to increase or reduce it, and surface investigations with newton meters and ramps.
Wrong answers come from real mistakes: "friction acts in the direction of movement", "friction is always bad",
"smooth surfaces have more friction", "friction only happens on the ground".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61511)
R = U.R
P = People(R)

SURF = {"ice": 1, "polished wood": 3, "plastic tray": 4, "tiles": 5, "carpet": 9, "rubber mat": 12, "sandpaper": 14, "grass": 10}


def g_pull():
    who = P.next()[0]
    s = R.sample(sorted(SURF), 4)
    v = [SURF[x] + R.choice([0, 0, 1]) for x in s]
    if len(set(v)) < 4:
        return None
    k = R.choice(["most", "least", "read", "diff"])
    ri = R.randrange(4)
    if not once(("pu", tuple(s), k, ri if k == "read" else 0)):
        return None
    tab = table(["Surface", "Force needed to pull the shoe (N)"], [[a, str(b)] for a, b in zip(s, v)])
    intro = tab + "%s pulled the same shoe across different surfaces with a newton meter. " % who
    if k == "most":
        a = s[v.index(max(v))]
        return item(intro + "Which surface had the most friction?", a, [x for x in s if x != a], "The biggest force was needed where friction was greatest.")
    if k == "least":
        a = s[v.index(min(v))]
        return item(intro + "Which surface had the least friction?", a, [x for x in s if x != a], "The smallest force means the least friction.")
    if k == "read":
        g = "%d N" % v[ri]
        return item(intro + "What force was needed on the %s?" % s[ri], g, uniq(g, ["%d N" % x for x in v] + ["%d N" % (v[ri] + 2)]), "Read the row.")
    d = max(v) - min(v)
    g = "%d N" % d
    return item(intro + "What is the difference between the largest and smallest forces?", g, uniq(g, ["%d N" % max(v), "%d N" % min(v), "%d N" % (max(v) + min(v)), "%d N" % (d + 2)]),
                "%d − %d = %d N." % (max(v), min(v), d))


def g_ramp():
    who = P.next()[0]
    s = R.sample(["carpet", "towel", "wood", "foil", "bubble wrap", "sandpaper"], 4)
    order = {"foil": 180, "wood": 150, "bubble wrap": 90, "carpet": 60, "towel": 45, "sandpaper": 35}
    v = [order[x] + R.choice([-5, 0, 5]) for x in s]
    k = R.choice(["far", "short", "why"])
    if not once(("ra", tuple(s), tuple(v), k)) or (k == "why" and not once(("rw",), 3)):
        return None
    tab = table(["Surface after the ramp", "Distance the car rolled (cm)"], [[a, str(b)] for a, b in zip(s, v)])
    intro = tab + "%s let a toy car roll down a ramp onto different surfaces. " % who
    if k == "far":
        a = s[v.index(max(v))]
        return item(intro + "On which surface did the car roll furthest?", a, [x for x in s if x != a], "Least friction lets the car roll furthest.")
    if k == "short":
        a = s[v.index(min(v))]
        return item(intro + "On which surface was there the most friction?", a, [x for x in s if x != a], "The car stopped soonest where friction was greatest.")
    return item(intro + "Why did the car roll different distances?", "Some surfaces were rougher, giving more friction to slow the car.", ["Gravity was different on each surface.", "The car got heavier.", "Smooth surfaces have more friction."],
                "Rough surfaces grip more.")


USE = [("the brakes on a bike", "helpful"), ("the grip of trainers on a running track", "helpful"), ("striking a match", "helpful"), ("walking without slipping", "helpful"),
       ("holding a pencil", "helpful"), ("car tyres gripping the road", "helpful"), ("parts rubbing inside a car engine", "unhelpful"), ("a rusty bike chain", "unhelpful"),
       ("a squeaky door hinge", "unhelpful"), ("a sledge slowing on wet grass", "unhelpful"), ("a skier wanting to go fast", "unhelpful"), ("a stiff, sticking drawer", "unhelpful")]


def g_use():
    u, h = R.choice(USE)
    if not once(("us", u)):
        return None
    return item("Is friction helpful or unhelpful here: %s?" % u, h, ["unhelpful" if h == "helpful" else "helpful", "there is no friction here", "friction only happens in space"],
                "Friction is useful for grip and stopping, but a problem when it slows things or wears them out.")


CHG = [("oiling a bike chain", "reduces friction"), ("putting wheels on a heavy box", "reduces friction"), ("waxing the bottom of a snowboard", "reduces friction"),
       ("using ball bearings in a skateboard wheel", "reduces friction"), ("polishing a slide", "reduces friction"), ("putting grit on an icy road", "increases friction"),
       ("deep treads on walking boots", "increases friction"), ("gymnasts putting chalk on their hands", "increases friction"), ("rubber grips on bike handles", "increases friction"),
       ("putting sand on a slippery path", "increases friction")]


def g_chg():
    c, e = R.choice(CHG)
    if not once(("ch", c)):
        return None
    return item("Does this increase or reduce friction: %s?" % c, "It " + e + ".", ["It " + ("increases friction" if e == "reduces friction" else "reduces friction") + ".", "It has no effect on friction.", "It turns friction into gravity."],
                "Lubricants, wheels and smooth surfaces reduce friction; rough or grippy surfaces increase it.")


DIRS = [("right", "left"), ("left", "right"), ("up a slope", "down the slope"), ("down a slope", "up the slope"), ("forwards", "backwards")]


def g_dir():
    m, f = R.choice(DIRS)
    obj = R.choice(["a box", "a sledge", "a book", "a toy car", "a wooden block", "a crate"])
    if not once(("di", m, obj)):
        return None
    mv = m.replace("a slope", "the slope")
    pool = {"right": ["right", "straight up", "straight down"], "left": ["left", "straight up", "straight down"]}.get(m)
    if pool is None:
        pool = [mv, "straight up", "sideways"]
    return item("%s is moving %s. Which way does friction act on it?" % (obj.capitalize(), m), f, pool, "Friction always acts against the direction of movement.")


B1 = bank([
    ("What is friction?", "a force between two surfaces that slows movement", ["a force that pulls things down", "a type of magnet", "the speed of an object"], "It acts where surfaces touch."),
    ("Which direction does friction act?", "against the direction of movement", ["in the same direction as movement", "always downwards", "always upwards"], "It opposes motion."),
    ("Which surface usually gives more friction?", "a rough surface", ["a smooth surface", "ice", "polished glass"], "Bumps catch on each other."),
    ("What happens when you rub your hands together quickly?", "They get warm because of friction.", ["They get cold.", "They get wet.", "Nothing happens."], "Friction produces heat."),
    ("What unit is force measured in?", "newtons (N)", ["kilograms", "metres", "seconds"], "Named after Isaac Newton."),
    ("Why is it hard to walk on ice?", "Ice is smooth, so there is very little friction to grip.", ["Ice has too much friction.", "Gravity is stronger on ice.", "Ice is magnetic."], "Low friction."),
    ("Why do car tyres have treads?", "to give grip and push water away, increasing friction", ["to make them look nice", "to reduce friction", "to make the car lighter"], "Safety in the wet."),
    ("Which measures the force needed to pull an object?", "a newton meter", ["a thermometer", "a ruler", "a stopwatch"], "A spring stretches more for bigger forces."),
])
B5 = bank([
    ("In a shoe-pulling test, why use the same shoe on every surface?", "so the only thing that changes is the surface", ["to save time", "shoes have no friction", "to make the test unfair"], "Fair test."),
    ("Why do we repeat the pull on each surface three times?", "to make the results more reliable", ["to wear the shoe out", "to change the surface", "it is not needed"], "Repeat readings."),
    ("Why do space rockets get very hot when they come back into the atmosphere?", "Friction with the air heats them.", ["The Sun heats them.", "They burn fuel.", "Space is hot."], "Air resistance is friction with air."),
    ("A pupil says friction is always bad. Which example shows it is useful?", "Brakes use friction to stop a bike safely.", ["Engines wear out.", "Doors squeak.", "Chains get stiff."], "Friction can be useful."),
    ("How could you test which floor is safest for a school corridor?", "Pull the same shoe across each floor sample and measure the force needed.", ["Look at the colour.", "Ask who likes each floor.", "Drop a ball on it."], "Measure friction."),
])


def body():
    think = ("<p><b>Friction is a force between surfaces that acts against movement.</b></p>"
             "<ul><li>Rough surfaces give more friction; smooth surfaces give less.</li>"
             "<li>Friction helps us grip and stop (shoes, brakes, tyres) but can waste energy and wear things out (engines, chains).</li>"
             "<li>Reduce it with oil, wheels and smooth surfaces; increase it with treads, grit and rubber.</li></ul>")
    ex = [("A box slides to the right. Friction acts?", ["Against the movement"], "to the left"),
          ("Carpet 9 N, ice 1 N. Most friction?", ["Bigger force needed"], "carpet")]
    mist = ["Thinking friction acts in the direction of movement.", "Thinking friction is always bad.", "Thinking smooth surfaces have more friction."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What friction is", B1 + [(g_dir, 8), (g_use, 4)]),
        ("Useful or not?", [(g_use, 8), (g_chg, 10), (g_dir, 2)]),
        ("Pulling test", [(g_pull, 20)]),
        ("Ramp test", [(g_ramp, 16), (g_dir, 4)]),
        ("Investigating friction", B5 + [(g_pull, 8), (g_ramp, 7)]),
    ])
    make_uk(5, "friction", 12, "Forces",
            "Identify the effects of air resistance, water resistance and friction, that act between moving surfaces.",
            "Friction",
            "Year 5 Science: Friction Worksheets (Surfaces, Grip and Newton Meters)",
            "Friction",
            "Free Year 5 science worksheets on friction: which way friction acts, rough and smooth surfaces, helpful and unhelpful friction, and surface investigations with newton meters and ramps. 100 questions with answers.",
            "Friction acts against movement.",
            "Rough surfaces grip and slow things; smooth or oiled surfaces slide.",
            body(),
            [("What is friction?", "A force that acts between two surfaces that are moving, or trying to move, across each other. It always acts against the movement."),
             ("Is friction good or bad?", "Both. It lets us walk, grip and stop with brakes, but it also slows machines down, wastes energy as heat and wears parts out."),
             ("How can you reduce friction?", "Use oil or grease, wheels or ball bearings, or make the surfaces smoother.")],
            sets)


if __name__ == "__main__":
    main()
