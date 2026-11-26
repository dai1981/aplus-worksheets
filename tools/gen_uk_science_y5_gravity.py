# -*- coding: utf-8 -*-
"""
UK Year 5 science: Gravity (Forces)
  python tools/gen_uk_science_y5_gravity.py
Unsupported objects fall towards the Earth because of gravity; mass and weight; weight in newtons (about 10 N for each
kilogram on Earth); weight on the Moon and other planets; Isaac Newton and Galileo.
Wrong answers come from real mistakes: "mass and weight are the same", "weight is measured in kilograms",
"heavier objects always fall faster", "there is no gravity on the Moon", "mass changes on the Moon".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq, num

U = Unit(61510)
R = U.R
P = People(R)

G = {"Earth": 10, "the Moon": 1.6, "Mars": 3.7, "Jupiter": 25}


def g_w():
    who = P.next()[0]
    thing = R.choice([("a bag of apples", [1, 2, 3]), ("a dog", [8, 12, 20, 25]), ("a bike", [9, 12, 15]), ("a schoolbag", [3, 4, 5, 6]),
                      ("a pupil", [30, 35, 38, 40, 42]), ("a bag of flour", [1, 1.5, 2]), ("a suitcase", [15, 18, 20, 23])])
    m = R.choice(thing[1])
    if not once(("w", thing[0], m)):
        return None
    W = m * 10
    g = "%s N" % num(W, 2)
    return item("%s has %s with a mass of %s kg. On Earth, each kilogram weighs about 10 N. What is its weight?" % (who, thing[0], num(m, 2)), g,
                uniq(g, ["%s kg" % num(m, 2), "%s N" % num(m, 2), "%s N" % num(m + 10, 2), "%s N" % num(m * 100, 2)]), "%s × 10 = %s N." % (num(m, 2), num(W, 2)))


def g_m():
    W = R.choice([20, 50, 80, 120, 250, 300, 350, 400, 450, 600, 750])
    if not once(("m", W)):
        return None
    g = "%s kg" % num(W / 10, 2)
    return item("An object weighs %d N on Earth (about 10 N for every kilogram). What is its mass?" % W, g,
                uniq(g, ["%d kg" % W, "%s N" % num(W / 10, 2), "%s kg" % num(W / 100, 2), "%s kg" % num(W * 10, 2)]), "%d ÷ 10 = %s kg." % (W, num(W / 10, 2)))


def g_moon():
    who = P.next()[0]
    m = R.choice([30, 36, 42, 48, 60, 72, 90, 120])
    k = R.choice(["mass", "weight"])
    if not once(("mo", m, k)):
        return None
    if k == "mass":
        g = "%d kg" % m
        return item("An astronaut's mass is %d kg on Earth. What is the astronaut's mass on the Moon?" % m, g, uniq(g, ["%d kg" % (m // 6), "0 kg", "%d kg" % (m * 6), "%d N" % (m * 10)]),
                    "Mass is the amount of matter; it does not change. Only weight changes.")
    W = m * 10
    g = "%d N" % (W // 6)
    if W % 6:
        return None
    return item("%s weighs %d N on Earth. Gravity on the Moon is about one-sixth as strong. About what would %s weigh on the Moon?" % (who, W, who), g,
                uniq(g, ["%d N" % W, "%s N" % format(W * 6, ","), "0 N", "%d N" % (W - 6)]), "%d ÷ 6 = %d N." % (W, W // 6))


def g_planet():
    m = R.choice([2, 5, 10, 20, 50])
    pl = R.choice(sorted(G))
    k = R.choice(["calc", "most", "least"])
    if not once(("pl", m, pl if k == "calc" else 0, k)) or (k != "calc" and not once(("pk", k), 2)):
        return None
    tab = table(["Place", "Pull of gravity on each kilogram (N)"], [[p, num(v, 2)] for p, v in G.items()])
    if k == "calc":
        W = m * G[pl]
        g = "%s N" % num(W, 2)
        return item(tab + "What would a %d kg box weigh on %s?" % (m, pl), g, uniq(g, ["%s N" % num(m * 10, 2), "%d kg" % m, "%s N" % num(m + G[pl], 2), "%s N" % num(W * 2, 2)]),
                    "%d × %s = %s N." % (m, num(G[pl], 2), num(W, 2)))
    if k == "most":
        return item(tab + "Where would a %d kg box weigh the most?" % m, "Jupiter", ["Earth", "the Moon", "Mars"], "Jupiter has the strongest pull of gravity in the table.")
    return item(tab + "Where would a %d kg box weigh the least?" % m, "the Moon", ["Earth", "Jupiter", "Mars"], "The Moon has the weakest pull of gravity in the table.")


def g_meter():
    who = P.next()[0]
    n = R.choice([2, 4, 5, 6, 8, 12, 15, 18])
    obj = R.choice(["a shoe", "a book", "a water bottle", "a pencil case", "a bag of sugar", "a tin of beans", "an apple", "a football"])
    if not once(("me", obj, n)):
        return None
    g = "%d N" % n
    return item("%s hangs %s on a newton meter. The pointer shows %d. What is the weight of the %s?" % (who, obj, n, obj.split(" ", 1)[1]), g, uniq(g, ["%d kg" % n, "%d g" % n, "%d N" % (n * 10), "%d cm" % n]),
                "A newton meter measures force (including weight) in newtons, N.")


B1 = bank([
    ("Why does a ball fall when you let go of it?", "Gravity pulls it towards the Earth.", ["Air pushes it down.", "The ball wants to fall.", "The Earth's magnetism pulls it."], "Unsupported objects fall."),
    ("What is the difference between mass and weight?", "Mass is the amount of matter; weight is the pull of gravity on it.", ["They are the same thing.", "Weight is in kg, mass is in N.", "Mass changes on the Moon."], "Weight in N, mass in kg."),
    ("What unit is weight measured in?", "newtons (N)", ["kilograms (kg)", "metres (m)", "litres (l)"], "Weight is a force."),
    ("Which scientist explained gravity, inspired, the story says, by a falling apple?", "Isaac Newton", ["Charles Darwin", "Mary Anning", "Alexander Fleming"], "Published in 1687."),
    ("Which way does gravity pull objects on Earth?", "towards the centre of the Earth", ["away from the Earth", "towards the Sun only", "sideways"], "Down is towards the centre."),
    ("Is there gravity on the Moon?", "Yes, but it is about one-sixth as strong as on Earth.", ["No, none at all.", "Yes, six times stronger.", "Only at night."], "Astronauts can jump high."),
    ("What keeps the Moon in orbit around the Earth?", "gravity", ["magnetism", "friction", "air resistance"], "Gravity holds orbits."),
    ("What does a newton meter measure?", "force, such as weight", ["length", "temperature", "time"], "It contains a spring."),
])
B5 = bank([
    ("Galileo is said to have dropped two balls of different mass from a tower. What did he find?", "They landed at about the same time.", ["The heavier one landed much sooner.", "The lighter one landed first.", "Neither fell."], "Mass does not change how fast things fall without air."),
    ("On the Moon, an astronaut dropped a hammer and a feather together. What happened?", "They hit the ground at the same time, because there is no air.", ["The hammer landed first.", "The feather floated away.", "Neither fell."], "Apollo 15, 1971."),
    ("Why does a feather fall more slowly than a stone on Earth?", "Air resistance slows the feather much more.", ["Gravity does not pull feathers.", "Feathers have no mass.", "Stones are magnetic."], "Air resistance matters."),
    ("Why would you weigh less on the Moon but still have the same mass?", "The Moon's gravity is weaker, but the amount of matter in you is the same.", ["You lose matter in space.", "Your mass becomes zero.", "The Moon has stronger gravity."], "Weight depends on gravity."),
    ("How could you test if heavier balls fall faster?", "Drop balls of the same size but different mass from the same height and time them.", ["Throw them at different speeds.", "Use different heights.", "Drop one ball only."], "Fair test."),
])


def body():
    think = ("<p><b>Gravity pulls unsupported objects towards the centre of the Earth.</b></p>"
             "<ul><li>Mass is the amount of matter (kg). Weight is the pull of gravity on that mass, a force measured in newtons (N).</li>"
             "<li>On Earth, each kilogram weighs about 10 N. On the Moon, gravity is about one-sixth as strong, so weight is less but mass is the same.</li>"
             "<li>Without air, all objects fall at the same rate (Galileo, Newton).</li></ul>")
    ex = [("Mass 4 kg on Earth. Weight?", ["4 × 10"], "40 N"),
          ("Weighs 600 N on Earth. On the Moon?", ["600 ÷ 6"], "100 N")]
    mist = ["Mixing up mass and weight.", "Writing weight in kilograms.", "Thinking heavier objects always fall faster."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What gravity is", B1 + [(g_meter, 6), (g_w, 6)]),
        ("Mass and weight", [(g_w, 10), (g_m, 10)]),
        ("Weight on the Moon", [(g_moon, 14), (g_meter, 6)]),
        ("Gravity on other planets", [(g_planet, 16), (g_m, 1), (g_w, 3)]),
        ("Thinking about falling", B5 + [(g_planet, 6), (g_moon, 5), (g_w, 4)]),
    ])
    make_uk(5, "gravity", 10, "Forces",
            "Explain that unsupported objects fall towards the Earth because of the force of gravity acting between the Earth and the falling object.",
            "Gravity",
            "Year 5 Science: Gravity Worksheets (Mass, Weight and Newtons)",
            "Gravity",
            "Free Year 5 science worksheets on gravity: why objects fall, mass and weight, newtons, weight on the Moon and other planets, and Newton and Galileo. 100 questions with answers.",
            "Gravity pulls things down.",
            "Weight is the pull of gravity, in newtons; mass stays the same everywhere.",
            body(),
            [("What is gravity?", "A force of attraction between objects. The Earth's gravity pulls unsupported objects towards its centre, which is why things fall."),
             ("What is the difference between mass and weight?", "Mass is the amount of matter in an object, in kilograms. Weight is the force of gravity on it, in newtons. On Earth, 1 kg weighs about 10 N."),
             ("Would I weigh less on the Moon?", "Yes. The Moon's gravity is about one-sixth of the Earth's, so your weight would be about one-sixth. Your mass would stay the same.")],
            sets)


if __name__ == "__main__":
    main()
