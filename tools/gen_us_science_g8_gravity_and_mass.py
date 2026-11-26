# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Gravity and Mass (MS-PS2-4)
  python tools/gen_us_science_g8_gravity_and_mass.py
Construct and present arguments using evidence to support the claim that gravitational interactions are attractive
and depend on the masses of interacting objects. Gravity always pulls; more mass → stronger pull; farther → weaker;
mass vs. weight; weight on other worlds (Moon 1/6, Mars about 0.38, Jupiter about 2.5).
Wrong answers come from real mistakes: "there is no gravity in space", "mass changes on the Moon",
"heavier objects fall faster (ignoring air)", "gravity can push".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(80104)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# weight factor compared with Earth (rounded, accepted textbook values)
WORLD = {"the Moon": 0.17, "Mars": 0.38, "Mercury": 0.38, "Jupiter": 2.5, "Venus": 0.9, "Neptune": 1.1}


def g_weight():
    who = P.next()[0]
    w_earth = R.choice([300, 360, 420, 480, 540, 600, 660, 720])
    place = R.choice(["the Moon", "Mars", "Jupiter"])
    if place == "the Moon":
        ww = w_earth // 6 if w_earth % 6 == 0 else None
        rule = "about 1/6"
    elif place == "Mars":
        ww = round(w_earth * 0.38)
        rule = "about 0.38 times"
    else:
        ww = round(w_earth * 2.5)
        rule = "about 2.5 times"
    k = R.choice(["weight", "weight", "mass"])
    if ww is None or not once((w_earth, place, k)):
        return None
    if k == "weight":
        w = [str(w_earth) + " N", str(w_earth * 6 if place == "the Moon" else round(w_earth / 2.5) if place == "Jupiter" else round(w_earth / 0.38)) + " N", "0 N"]
        return item("An astronaut named %s weighs %d N on Earth. On %s, weight is %s Earth weight. What does %s weigh there?" % (who, w_earth, place, rule, who), "%d N" % ww, w,
                    "Weight = Earth weight × factor. Mass does not change.")
    m = w_earth // 10
    return item("%s has a mass of %d kg on Earth. What is %s's mass on %s?" % (who, m, who, place), "%d kg" % m, ["%d kg" % round(m * WORLD[place]) if round(m * WORLD[place]) != m else "%d kg" % (m + 5), "0 kg", "%d kg" % (m * 10)],
                "Mass is the amount of matter. It is the same everywhere; only weight changes.")


def g_compare():
    who = P.next()[0]
    pairs = [("Earth", "the Moon", "Earth"), ("the Sun", "Earth", "the Sun"), ("Jupiter", "Mars", "Jupiter"), ("a bowling ball", "a marble", "a bowling ball"), ("Earth", "a person", "Earth"),
             ("a large asteroid", "a small pebble", "a large asteroid"), ("Saturn", "Venus", "Saturn"), ("the Sun", "Jupiter", "the Sun"), ("a mountain", "a house", "a mountain"),
             ("a truck", "a bicycle", "a truck")]
    a, b, big = R.choice(pairs)
    t = R.random() < 0.5
    if not once((a, b, t)):
        return None
    if t:
        return item("%s compares %s and %s. Which has a stronger gravitational pull on objects near it at the same distance?" % (who, a, b), big[0].upper() + big[1:] + ", because it has more mass.",
                    [b[0].upper() + b[1:] + ", because it has less mass.", "They pull the same.", "Neither has gravity."], "More mass means stronger gravity.")
    return item("%s asks about the gravitational force between %s and %s. Which statement is correct?" % (who, a, b), "They pull on each other with forces of equal size.",
                ["Only %s pulls." % big, "%s pushes the other away." % (big[0].upper() + big[1:]), "There is no force between them."], "Gravity is a pair of attractive forces (Newton's third law).")


def g_table():
    who = P.next()[0]
    k = R.choice(["mass", "dist"])
    if k == "mass":
        base = R.choice([2, 3, 4, 5, 6, 7, 8, 9])
        rows = [["%d kg" % m, "%d units" % (base * m)] for m in [1, 2, 3, 4]]
        tab = table(["Mass of object B (object A stays the same)", "Gravitational force"], rows)
        q = R.choice(["pat", "pred", "pred"])
        if not once(("m", base, q)) or (q == "pat" and not once("pat", 3)):
            return None
        if q == "pat":
            return item(tab + "What does %s's model data show?" % who, "Doubling the mass doubles the gravitational force.", ["Doubling the mass halves the force.", "Mass has no effect.", "The force becomes zero."],
                        "Gravity depends on mass.")
        return item(tab + "Using %s's model, what is the force when object B has a mass of 6 kg?" % who, "%d units" % (base * 6), ["%d units" % (base * 4), "%d units" % (base * 5), "%d units" % (base * 12)],
                    "%d units per kg × 6 kg = %d units." % (base, base * 6))
    base = R.choice([36, 72, 144, 108, 180])
    rows = [["%d" % d, "%g units" % (base / (d * d))] for d in [1, 2, 3]]
    tab = table(["Distance between the objects", "Gravitational force"], rows)
    q = R.choice(["pat", "where"])
    if not once(("d", base, q)):
        return None
    if q == "where":
        return item(tab + "In %s's model, at which distance is the pull strongest?" % who, "1", ["2", "3", "The pull is the same at every distance."], "Closer objects pull harder.")
    return item(tab + "What does %s's model data show?" % who, "The force gets weaker as the objects get farther apart.", ["The force gets stronger as they move apart.", "Distance has no effect.", "The force pushes them apart."],
                "Gravity weakens with distance.")


def g_claim():
    who = P.next()[0]
    cases = [("Astronauts float in the space station.", "They are falling around Earth with the station; gravity is still pulling them.", "There is no gravity in space."),
             ("The Moon stays in orbit around Earth.", "Earth's gravity pulls on the Moon and keeps it in orbit.", "The Moon is too far for gravity."),
             ("Ocean tides rise and fall twice a day.", "The Moon's gravity pulls on Earth's oceans.", "Wind pushes the tides."),
             ("A dropped apple falls to the ground.", "Earth's gravity pulls the apple down.", "The air pushes the apple down."),
             ("Earth orbits the Sun.", "The Sun's huge mass pulls on Earth.", "Earth is pushed by sunlight."),
             ("A hammer and a feather hit the Moon's surface at the same time.", "Without air, gravity makes all objects fall at the same rate.", "The hammer is lighter on the Moon.")]
    s, a, w0 = R.choice(cases)
    if not once(s, 2):
        return None
    w = [w0, R.choice(["Gravity pushes objects away.", "Only heavy objects have gravity."]), "Magnets cause it."]
    return item("%s observes: “%s” Which explanation is best supported by evidence?" % (who, s), a, w, "Gravity is an attractive force between all masses.")


B1 = bank([
    ("What is gravity?", "an attractive force between any two objects that have mass", ["a force that pushes objects apart", "a force only on Earth", "a magnetic force"], "All masses attract each other."),
    ("Does gravity ever push objects apart?", "No, gravity only attracts.", ["Yes, always.", "Only in space.", "Only for small objects."], "Gravity is always attractive."),
    ("What is the difference between mass and weight?", "Mass is the amount of matter; weight is the pull of gravity on it.", ["They are the same.", "Weight never changes.", "Mass changes on other planets."],
     "Weight is a force (N); mass is in kg."),
    ("Why do you weigh less on the Moon?", "The Moon has less mass than Earth, so its gravity is weaker.", ["Your mass is smaller there.", "The Moon has no gravity.", "The Moon is made of air."], "Less mass → weaker pull."),
    ("Is there gravity in space?", "Yes. Gravity reaches far into space and holds planets in orbit.", ["No, none.", "Only near the Sun.", "Only on Earth."], "Gravity weakens with distance but never stops."),
    ("Why does the Sun have the strongest gravity in the solar system?", "It has by far the most mass.", ["It is the hottest.", "It is the brightest.", "It is in the middle."], "Mass determines gravity."),
    ("You pull on Earth with gravity too. Why doesn't Earth move toward you noticeably?", "Earth's mass is enormous, so the same force barely changes its motion.", ["You do not pull on Earth.", "Earth has no mass.", "Gravity only works one way."],
     "Equal forces, very different masses."),
    ("What happens to the gravitational force if two objects move farther apart?", "It gets weaker.", ["It gets stronger.", "It stays the same.", "It turns into a push."], "Distance weakens gravity."),
])
B5 = bank([
    ("Ava claims that gravity depends on mass. Which evidence best supports her claim?", "Objects weigh less on the Moon, which has less mass than Earth.", ["Balloons float up.", "Magnets attract iron.", "Ice melts in the Sun."],
     "Weaker pull from a smaller mass."),
    ("Leo says astronauts are weightless because space has no gravity. What is a better argument?", "Gravity keeps the station in orbit; astronauts float because they are in free fall.", ["Leo is right.", "Astronauts have no mass.", "The station blocks gravity."],
     "Gravity is still strong in low orbit."),
    ("Mia's mass is 40 kg. A scale on Earth reads about 400 N. What would it read on the Moon?", "about 67 N", ["400 N", "2,400 N", "0 N"], "400 ÷ 6 ≈ 67 N."),
    ("Why are planets closer to the Sun pulled harder by it?", "Gravity is stronger at shorter distances.", ["They are smaller.", "They are hotter.", "They have more moons."], "Closer → stronger."),
    ("Two spacecraft of equal mass are near each other in deep space. What happens over time?", "They slowly pull toward each other.", ["They push apart.", "Nothing; space has no gravity.", "They start spinning."],
     "All masses attract."),
])


def body():
    think = ("<p><b>Gravity</b> is a force of <b>attraction</b> between any two objects with mass. It never pushes.</p>"
             "<ul><li><b>More mass</b> → stronger gravity. The Sun pulls harder than Earth; Earth pulls harder than the Moon.</li>"
             "<li><b>More distance</b> → weaker gravity.</li>"
             "<li>The two objects pull on each other with <b>equal</b> forces.</li></ul>"
             "<p><b>Mass</b> (kg) is the amount of matter and stays the same everywhere. <b>Weight</b> (N) is the pull of gravity and changes: on the Moon you weigh about 1/6 as much.</p>")
    ex = [("You weigh 540 N on Earth. What do you weigh on the Moon?", ["540 ÷ 6"], "90 N"),
          ("Your mass is 50 kg on Earth. What is it on Mars?", ["Mass does not change."], "50 kg")]
    mist = ["Thinking there is no gravity in space.",
            "Thinking mass changes on other planets. Only weight changes.",
            "Thinking gravity can push objects away."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What gravity is", B1 + [(g_compare, 10), (g_claim, 2)]),
        ("Mass and gravity", [(g_compare, 6), (g_table, 14)]),
        ("Mass and weight", [(g_weight, 16), (g_table, 4)]),
        ("Evidence for gravity", [(g_claim, 12), (g_weight, 8)]),
        ("Arguing from evidence", B5 + [g_claim, g_table, g_weight, g_compare]),
    ])
    make("grade-8", "gravity-and-mass", 4, "MS-PS2-4",
         "Construct and present arguments using evidence to support the claim that gravitational interactions are attractive and depend on the masses of interacting objects.",
         "Gravity and Mass",
         "Grade 8 Gravity Worksheets: Mass, Weight, Distance and Gravitational Attraction",
         "Gravity and Mass",
         "Free middle school science worksheets on gravity (NGSS MS-PS2-4): gravity as an attractive force, how mass and distance affect it, mass vs. weight, and weight on the Moon and other planets. 100 practice questions with answers.",
         "Gravity always pulls, and more mass pulls harder.",
         "Gravitational force grows with mass and shrinks with distance. Weight changes from world to world; mass does not.",
         body(),
         [("What does the strength of gravity depend on?", "The masses of the two objects and the distance between them. More mass makes it stronger; more distance makes it weaker."),
          ("What is the difference between mass and weight?", "Mass is the amount of matter in an object and stays the same everywhere. Weight is the force of gravity on that mass and changes on other planets."),
          ("Why do astronauts float in the space station?", "They and the station are falling around Earth together. Gravity is still pulling on them.")],
         sets)


if __name__ == "__main__":
    main()
