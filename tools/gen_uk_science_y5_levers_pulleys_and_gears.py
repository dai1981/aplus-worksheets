# -*- coding: utf-8 -*-
"""
UK Year 5 science: Levers, Pulleys and Gears (Forces)
  python tools/gen_uk_science_y5_levers_pulleys_and_gears.py
Mechanisms that let a smaller force have a greater effect: levers (pivot, effort, load; balancing a see-saw),
pulleys (more supporting ropes, less effort), gears (teeth, turns and direction), and everyday examples.
Wrong answers come from real mistakes: "a longer lever needs more effort", "a pulley makes the load lighter",
"two touching gears turn the same way", "a small gear turns more slowly than a big one".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq, num

U = Unit(61513)
R = U.R
P = People(R)


def g_lever():
    L = R.choice([60, 80, 90, 120, 150, 200, 240, 300])
    dl = R.choice([0.5, 1])
    de = R.choice([1, 1.5, 2, 3, 4])
    E = L * dl / de
    if de <= dl or E != int(E) or not once(("lv", L, dl, de)):
        return None
    g = "%d N" % E
    return item("A crowbar lifts a load of %d N that is %s m from the pivot. You push down %s m from the pivot. What force do you need? (effort × distance = load × distance)" % (L, num(dl, 2), num(de, 2)), g,
                uniq(g, ["%d N" % L, "%s N" % num(L * de / dl, 2), "%s N" % num(L - de, 2), "%s N" % num(E * 2, 2)]), "%d × %s ÷ %s = %d N." % (L, num(dl, 2), num(de, 2), E))


def g_seesaw():
    a, b = P.next()[0], P.next()[0]
    wa = R.choice([300, 320, 360, 400, 450])
    da = R.choice([1, 1.5, 2])
    wb = R.choice([240, 300, 360, 400, 480, 600])
    db = wa * da / wb
    if wa == wb or db * 4 != int(db * 4) or db > 3 or not once(("ss", wa, da, wb)):
        return None
    g = "%s m" % num(db, 2)
    return item("On a see-saw, %s (%d N) sits %s m from the pivot. Where must %s (%d N) sit on the other side to balance it?" % (a, wa, num(da, 2), b, wb), g,
                uniq(g, ["%s m" % num(da, 2), "%s m" % num(wb * da / wa, 2), "%s m" % num(db + 1, 2), "%s m" % num(db * 2, 2)]),
                "%d × %s = %d × distance, so distance = %s m. The heavier person sits closer." % (wa, num(da, 2), wb, num(db, 2)))


def g_pulley():
    L = R.choice([100, 120, 200, 240, 300, 400, 600])
    n = R.choice([1, 2, 3, 4])
    E = L / n
    if E != int(E) or not once(("pu", L, n)):
        return None
    g = "%d N" % E
    return item("A pulley system has %d rope%s holding up a load of %d N. Ignoring friction, what effort is needed to lift it?" % (n, "" if n == 1 else "s", L), g,
                uniq(g, ["%d N" % L, "%d N" % (L * n), "%d N" % (L - n), "%d N" % (E / 2 if E % 2 == 0 else E + 10)]), "%d ÷ %d = %d N. More ropes share the load." % (L, n, E))


def g_gear():
    a = R.choice([8, 10, 12, 15, 20])
    m = R.choice([2, 3, 4])
    b = a * m
    k = R.choice(["turns", "back", "dir"])
    n = R.choice([1, 2, 3, 4, 6])
    if not once(("ge", a, m, k, n if k != "dir" else 0)) or (k == "dir" and not once(("gd", a), 1)):
        return None
    if k == "turns":
        g = "%d turns" % (n * m)
        return item("A small gear with %d teeth drives a big gear with %d teeth. How many times does the small gear turn while the big gear turns %d time%s?" % (a, b, n, "" if n == 1 else "s"), g,
                    uniq(g, ["%d turns" % n, "%d turns" % (n + m), "%s turns" % num(n / m, 2), "%d turns" % (n * m * 2)]), "%d ÷ %d = %d small turns for each big turn." % (b, a, m))
    if k == "back":
        if (n * m) % m:
            return None
        g = "%d turn%s" % (n, "" if n == 1 else "s")
        return item("A small gear with %d teeth drives a big gear with %d teeth. The small gear turns %d times. How many times does the big gear turn?" % (a, b, n * m), g,
                    uniq(g, ["%d turns" % (n * m * m), "%d turns" % (n * m), "%d turns" % (n * m + m), "%s turns" % num(n + 1, 2)]), "%d ÷ %d = %d." % (n * m, m, n))
    return item("Gear A (%d teeth) turns clockwise and drives gear B (%d teeth). Which way does gear B turn?" % (a, b), "anticlockwise", ["clockwise", "it does not turn", "backwards and forwards"],
                "Two gears that touch turn in opposite directions.")


MECH = [("a crowbar", "lever"), ("scissors", "lever"), ("a wheelbarrow", "lever"), ("a bottle opener", "lever"), ("a see-saw", "lever"), ("tweezers", "lever"),
        ("a flagpole rope", "pulley"), ("a crane lifting steel", "pulley"), ("a well bucket on a rope", "pulley"), ("window blinds", "pulley"),
        ("a bicycle chain and sprockets", "gears"), ("a mechanical clock", "gears"), ("a hand-held egg whisk", "gears"), ("a tin opener's turning wheels", "gears")]


def g_mech():
    t, m = R.choice(MECH)
    if not once(("me", t)):
        return None
    return item("What kind of mechanism is used in %s?" % t, "a lever" if m == "lever" else "a pulley" if m == "pulley" else "gears",
                [x for x in ["a lever", "a pulley", "gears", "a magnet"] if x != ("a lever" if m == "lever" else "a pulley" if m == "pulley" else "gears")], "Levers, pulleys and gears are simple machines.")


B1 = bank([
    ("What is a mechanism?", "a device that makes a force have a bigger effect or changes its direction", ["a type of magnet", "a kind of fuel", "a source of light"], "Levers, pulleys and gears."),
    ("What is the pivot of a lever?", "the point it turns around", ["the load it lifts", "the force you push with", "the end of the handle"], "Also called the fulcrum."),
    ("How can you make a lever lift a load with less effort?", "push further from the pivot", ["push closer to the pivot", "use a shorter lever", "move the load further away"], "Longer distance, less force."),
    ("What does a single fixed pulley do?", "changes the direction of the force, so you pull down to lift up", ["makes the load lighter", "makes the load heavier", "stops the load moving"], "Flagpoles use this."),
    ("What happens when two gears touch and one turns?", "The other turns the opposite way.", ["The other turns the same way.", "Neither moves.", "The other stops."], "Teeth push each other."),
    ("Which famous Greek thinker said 'Give me a place to stand and I will move the Earth' about levers?", "Archimedes", ["Isaac Newton", "Galileo", "Copernicus"], "He studied levers."),
    ("Why does a big gear driven by a small gear turn more slowly?", "It has more teeth, so the small gear must turn more times for one big turn.", ["It is heavier.", "It has fewer teeth.", "Gears always turn at the same speed."], "Count the teeth."),
    ("In a pulley system, why does the effort get smaller with more ropes?", "The load is shared between the ropes.", ["The load gets lighter.", "Gravity is weaker.", "Ropes push the load up."], "But you pull more rope."),
])
B5 = bank([
    ("A bike has a big front gear and a small back gear. Why is this good for going fast?", "One turn of the pedals turns the back wheel several times.", ["It makes the bike lighter.", "It needs no effort.", "It stops the chain."], "Gears change speed."),
    ("Why do cranes use several pulleys?", "so a large load can be lifted with a smaller force", ["to make the load lighter", "to make the crane taller", "to change the colour"], "Mechanical advantage."),
    ("How could you test how the length of a lever affects the effort needed?", "Lift the same load with rulers of different lengths and measure the effort with a newton meter.", ["Use different loads each time.", "Guess the effort.", "Use one ruler only."], "Fair test."),
    ("Why do door handles sit far from the hinges?", "Pushing far from the pivot needs less force to open the door.", ["It looks nicer.", "Hinges are heavy.", "It makes the door lighter."], "Levers in daily life."),
    ("Why does a pulley system with less effort mean you pull more rope?", "You do the same work by using a smaller force over a longer distance.", ["Rope stretches.", "Pulleys add energy.", "The load gets lighter."], "No free lunch."),
])


def body():
    think = ("<p><b>Levers, pulleys and gears let a small force have a bigger effect.</b></p>"
             "<ul><li>Lever: effort × distance = load × distance. Push further from the pivot to lift more easily.</li>"
             "<li>Pulleys: a single pulley changes direction; more supporting ropes share the load (effort = load ÷ ropes).</li>"
             "<li>Gears: touching gears turn opposite ways; a small gear driving a big gear turns more times.</li></ul>")
    ex = [("Load 120 N at 1 m, effort at 3 m?", ["120 × 1 ÷ 3"], "40 N"),
          ("10-tooth gear drives 30-tooth gear. Turns of small for 1 big?", ["30 ÷ 10"], "3 turns")]
    mist = ["Thinking a longer lever needs more effort.", "Thinking a pulley makes the load lighter.", "Thinking touching gears turn the same way."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Simple machines", B1 + [(g_mech, 12)]),
        ("Levers", [(g_lever, 14), (g_seesaw, 6)]),
        ("Pulleys", [(g_pulley, 16), (g_mech, 2), (g_lever, 2)]),
        ("Gears", [(g_gear, 18), (g_seesaw, 2)]),
        ("Using mechanisms", B5 + [(g_seesaw, 6), (g_gear, 5), (g_lever, 4)]),
    ])
    make_uk(5, "levers-pulleys-and-gears", 13, "Forces",
            "Recognise that some mechanisms, including levers, pulleys and gears, allow a smaller force to have a greater effect.",
            "Levers, Pulleys and Gears",
            "Year 5 Science: Levers, Pulleys and Gears Worksheets (Mechanisms and Forces)",
            "Levers, Pulleys and Gears",
            "Free Year 5 science worksheets on levers, pulleys and gears: pivots and balancing, pulley ropes and effort, gear teeth and turns, and everyday mechanisms. 100 questions with answers.",
            "A small force, a big effect.",
            "Longer levers, more pulley ropes and the right gears all reduce the effort.",
            body(),
            [("How does a lever make lifting easier?", "Pushing further from the pivot means a smaller force can lift a heavier load. Effort × distance from pivot = load × distance from pivot."),
             ("How do pulleys help?", "A single pulley changes the direction of the pull. A system with more ropes holding the load shares it, so less effort is needed (but you pull more rope)."),
             ("Why do gears turn in opposite directions?", "Their teeth push against each other, so when one gear turns clockwise, the gear it touches turns anticlockwise.")],
            sets)


if __name__ == "__main__":
    main()
