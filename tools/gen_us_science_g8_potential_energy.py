# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Potential Energy (MS-PS3-2)
  python tools/gen_us_science_g8_potential_energy.py
Develop a model to describe that when the arrangement of objects interacting at a distance changes, different
amounts of potential energy are stored in the system. Gravitational PE = m × g × h (g ≈ 10 N/kg); stretched or
compressed springs and rubber bands; magnets and charges held apart or together; PE changing into KE.
Wrong answers come from real mistakes: "potential energy belongs to one object, not the system",
"a higher object has less PE", "pulling two attracting magnets apart lowers their PE", "PE = m × h without g".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(80106)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def J(x):
    return comma(int(x)) + " J" if x == int(x) else "%g J" % x


OBJ = [("a book", [1, 2]), ("a backpack", [3, 4, 5]), ("a bowling ball", [6, 7]), ("a watermelon", [5, 8]), ("a box of tiles", [10, 12]),
       ("a cat", [4, 5]), ("a flowerpot", [2, 3])]
PLACE = [("a shelf", [1, 2]), ("a table", [1]), ("a balcony", [3, 4, 5, 6]), ("a high shelf", [2, 3]), ("a ladder step", [2, 3]), ("a stage", [1, 2])]


def g_calc():
    o, ms = R.choice(OBJ)
    pl, hs = R.choice(PLACE)
    m, h = R.choice(ms), R.choice(hs)
    if not once(("c", m, h)):
        return None
    who = P.next()[0]
    pe = m * 10 * h
    return item("%s lifts %s with a mass of %d kg onto %s %d m above the floor. How much gravitational potential energy is stored? (PE = m × g × h, g = 10 N/kg)" % (who, o, m, pl, h), J(pe),
                [J(m * h), J(m * 10), J(pe * 2)], "PE = %d × 10 × %d = %s." % (m, h, J(pe)))


def g_compare():
    who = P.next()[0]
    k = R.choice(["height", "mass", "same"])
    m = R.choice([2, 4, 5])
    h = R.choice([2, 3])
    if not once(("cmp", k, m, h)):
        return None
    rows = {"height": [["A", "%d kg" % m, "%d m" % h], ["B", "%d kg" % m, "%d m" % (h * 2)]],
            "mass": [["A", "%d kg" % (m * 2), "%d m" % h], ["B", "%d kg" % m, "%d m" % h]],
            "same": [["A", "%d kg" % (m * 2), "%d m" % h], ["B", "%d kg" % m, "%d m" % (h * 2)]]}[k]
    tab = table(["Ball", "Mass", "Height"], rows)
    if k == "height":
        return item(tab + "Which ball in %s's table stores more gravitational potential energy?" % who, "Ball B, because it is higher.", ["Ball A, because it is lower.", "They store the same amount.", "Neither stores energy."],
                    "Same mass, twice the height → twice the PE.")
    if k == "mass":
        return item(tab + "Which ball in %s's table stores more gravitational potential energy?" % who, "Ball A, because it has more mass.", ["Ball B, because it has less mass.", "They store the same amount.", "Neither stores energy."],
                    "Same height, twice the mass → twice the PE.")
    return item(tab + "Which ball in %s's table stores more gravitational potential energy?" % who, "They store the same amount.", ["Ball A, because it is heavier.", "Ball B, because it is higher.", "Neither stores energy."],
                "%d × 10 × %d = %d × 10 × %d: both are %s." % (m * 2, h, m, h * 2, J(m * 2 * 10 * h)))


ARR = [("Two magnets with opposite poles facing are pulled apart.", "increases", "Attracting objects store more PE when they are farther apart."),
       ("Two magnets with like poles facing are pushed closer together.", "increases", "Repelling objects store more PE when they are pushed closer."),
       ("Two attracting magnets snap together.", "decreases", "The stored energy changes into kinetic energy and sound."),
       ("A rubber band is stretched farther.", "increases", "A more stretched band stores more elastic PE."),
       ("A spring is squeezed more tightly.", "increases", "A more compressed spring stores more elastic PE."),
       ("A stretched rubber band is released and goes slack.", "decreases", "The PE changes into kinetic energy."),
       ("A ball is carried up a flight of stairs.", "increases", "Moving an object farther from Earth stores more gravitational PE."),
       ("A roller coaster car rolls down a hill.", "decreases", "Gravitational PE changes into kinetic energy."),
       ("Two positive charges are pushed closer together.", "increases", "Like charges repel, so pushing them together stores PE."),
       ("A negative and a positive charge are pulled apart.", "increases", "Opposite charges attract, so pulling them apart stores PE."),
       ("A bow string is pulled back farther.", "increases", "The bent bow stores more elastic PE."),
       ("A book falls from a shelf to the floor.", "decreases", "The book-Earth system loses gravitational PE."),
       ("A climber moves from the bottom of a cliff to the top.", "increases", "More height means more gravitational PE in the climber-Earth system."),
       ("A compressed spring in a toy pops up and stretches out.", "decreases", "The spring's elastic PE changes into kinetic energy."),
       ("Two repelling magnets are let go and fly apart.", "decreases", "Repelling objects lose PE as they move apart."),
       ("A charged balloon is pulled away from a wall it was stuck to.", "increases", "The balloon and wall attract, so separating them stores PE."),
       ("A trampoline sags as a jumper lands on it.", "increases", "The stretched trampoline stores elastic PE."),
       ("Water flows from a high reservoir down to a lower one.", "decreases", "The water-Earth system loses gravitational PE."),
       ("An elevator lifts a box from the 1st floor to the 5th floor.", "increases", "Raising the box stores more gravitational PE."),
       ("A wound-up toy's spring unwinds as the toy moves.", "decreases", "Elastic PE changes into kinetic energy.")]


def g_arr():
    s, d, e = R.choice(ARR)
    who = P.next()[0]
    if not once(("a", s)):
        return None
    opp = "decreases" if d == "increases" else "increases"
    return item("%s's model: “%s” What happens to the potential energy stored in the system?" % (who, s), "It %s." % d, ["It %s." % opp, "It stays the same.", "It disappears from the universe."], e)


def g_trans():
    who = P.next()[0]
    m = R.choice([1, 2, 4, 5])
    h = R.choice([2, 4, 5, 10])
    k = R.choice(["top", "half", "bottom"])
    if not once(("t", m, h, k)):
        return None
    pe = m * 10 * h
    if k == "top":
        return item("%s holds a %d kg ball %d m above the ground. How much gravitational PE does the ball-Earth system have (g = 10 N/kg)?" % (who, m, h), J(pe), [J(m * h), "0 J", J(pe / 2)],
                    "PE = %d × 10 × %d = %s." % (m, h, J(pe)))
    if k == "half":
        return item("%s drops a %d kg ball from %d m. It started with %s of PE. Ignoring air, how much kinetic energy does it have halfway down?" % (who, m, h, J(pe)), J(pe / 2), [J(pe), "0 J", J(pe * 2)],
                    "Half the PE has changed into KE.")
    return item("%s drops a %d kg ball from %d m. It started with %s of PE. Ignoring air, how much kinetic energy does it have just before it hits the ground?" % (who, m, h, J(pe)), J(pe),
                [J(pe / 2), "0 J", J(pe * 2)], "All the PE has changed into KE.")


B1 = bank([
    ("What is potential energy?", "stored energy due to the arrangement or position of objects that interact", ["energy of motion", "energy from sound only", "the mass of an object"], "Position and arrangement store energy."),
    ("Where is gravitational potential energy stored when you lift a book?", "in the book-Earth system", ["only in the book", "only in your hand", "nowhere"], "Two objects interacting at a distance make a system."),
    ("What three things does gravitational PE depend on?", "mass, gravitational field strength and height", ["color, mass and speed", "speed only", "temperature only"], "PE = m × g × h."),
    ("Which stores more elastic potential energy?", "a rubber band stretched 20 cm", ["a rubber band stretched 5 cm", "a slack rubber band", "a cut rubber band"], "More stretch, more stored energy."),
    ("Two magnets attract each other. When do they store the most potential energy?", "when they are held far apart", ["when they are touching", "when they are moving together", "never"], "Pulling attracting objects apart takes work."),
    ("What happens to PE as a skier goes down a slope?", "It decreases as it changes to kinetic energy.", ["It increases.", "It stays the same.", "It turns into mass."], "Energy changes form."),
    ("What unit is used for potential energy?", "joule (J)", ["newton (N)", "kilogram (kg)", "meter (m)"], "All energy is measured in joules."),
    ("A ball sits on the floor. Is the gravitational PE of the ball-Earth system zero?", "Only if the floor is chosen as the zero height.", ["Yes, always.", "No, it is infinite.", "PE does not exist on floors."], "Heights are measured from a chosen level."),
])
B5 = bank([
    ("Ava pulls a toy car's spring back 2 cm, then 4 cm. Which launch goes farther?", "the 4 cm pull", ["the 2 cm pull", "They go the same distance.", "Neither moves."], "More compression stores more PE."),
    ("Leo models two attracting magnets as balls connected by a stretched spring. Why?", "The spring shows that pulling them apart stores energy.", ["Magnets are made of springs.", "Springs are magnetic.", "It shows the magnets repel."], "A good model shows energy storage."),
    ("Mia lifts a 3 kg box to a 2 m shelf, then to a 4 m shelf. How much more PE is stored at 4 m?", "60 J more", ["30 J more", "120 J more", "the same"], "3 × 10 × 2 = 60 J more."),
    ("A pendulum swings. Where does the bob have the most PE?", "at the highest points of its swing", ["at the lowest point", "in the middle", "it never has PE"], "Highest position → most PE."),
    ("Why does a water tower store energy?", "Water held high has gravitational PE that can push water through pipes.", ["Water is hot.", "The tower is magnetic.", "Water has no mass."], "Height stores energy."),
])


def body():
    think = ("<p><b>Potential energy</b> is energy stored in a <b>system</b> of objects that push or pull on each other at a distance. Changing their <b>arrangement</b> changes the stored energy.</p>"
             "<ul><li><b>Gravitational PE</b>: lifting an object higher stores more energy. <b>PE = m × g × h</b> (g = 10 N/kg on Earth).</li>"
             "<li><b>Elastic PE</b>: stretching or squeezing a spring or rubber band stores energy.</li>"
             "<li><b>Magnetic and electric PE</b>: pulling attracting objects apart, or pushing repelling objects together, stores energy.</li></ul>"
             "<p>When the objects are released, the PE changes into kinetic energy.</p>")
    ex = [("A 2 kg book is on a 1.5 m shelf. PE?", ["2 × 10 × 1.5"], "30 J"),
          ("Two attracting magnets are pulled apart. What happens to PE?", ["Work is done to separate them."], "It increases.")]
    mist = ["Thinking PE belongs to one object. It is stored in the system.",
            "Forgetting g: PE = m × g × h, not m × h.",
            "Thinking pulling attracting magnets apart lowers PE."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stored energy", B1 + [(g_calc, 12)]),
        ("Gravitational potential energy", [(g_calc, 12), (g_compare, 8)]),
        ("Changing the arrangement", [(g_arr, 12), (g_compare, 8)]),
        ("Potential to kinetic", [(g_trans, 14), (g_arr, 6)]),
        ("Modeling energy", B5 + [g_trans, g_arr, g_calc, g_compare]),
    ])
    make("grade-8", "potential-energy", 6, "MS-PS3-2",
         "Develop a model to describe that when the arrangement of objects interacting at a distance changes, different amounts of potential energy are stored in the system.",
         "Potential Energy",
         "Grade 8 Potential Energy Worksheets: Gravitational, Elastic and Magnetic Potential Energy",
         "Potential Energy",
         "Free middle school science worksheets on potential energy (NGSS MS-PS3-2): PE = mgh, elastic and magnetic potential energy, how arrangement changes stored energy, and PE changing into KE. 100 practice questions with answers.",
         "Changing the arrangement changes stored energy.",
         "Lifting, stretching, or pulling attracting objects apart stores potential energy in the system: PE = m × g × h.",
         body(),
         [("How do you calculate gravitational potential energy?", "PE = m × g × h. On Earth, g is about 10 N/kg, mass is in kilograms and height is in meters."),
          ("Where is potential energy stored?", "In the system of interacting objects, such as a book and Earth, or two magnets, not in one object alone."),
          ("How does potential energy change into kinetic energy?", "When objects are released, the stored energy changes into motion. A falling ball loses PE and gains the same amount of KE, ignoring air.")],
         sets)


if __name__ == "__main__":
    main()
