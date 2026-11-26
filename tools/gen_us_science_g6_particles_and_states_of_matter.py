# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Particles and States of Matter (MS-PS1-4)
  python tools/gen_us_science_g6_particles_and_states_of_matter.py
Adding or removing thermal energy changes particle motion, temperature and state of a pure substance.
Solids: particles packed and vibrating in place; liquids: close but sliding past; gases: far apart and
moving fast. Melting, freezing, boiling/evaporation, condensation. Heating curves: temperature stays the
same while the state changes. Water: melts at 0 °C, boils at 100 °C (at sea level).
Wrong answers come from real mistakes: "particles stop moving in a solid", "particles get bigger when
heated", "temperature keeps rising while water boils", "gas particles are touching".
"""
import math
from sci_common import comma, Unit, item, bank, lesson, make, table, fig, figure, svg_wrap, rect, circle, text, People, INK, BLUE

U = Unit(60105)
R = U.R
P = People(R)


def particles(state, label=None):
    W, H = 130, 130
    s = [rect(5, 5, 120, 120, "#fff", INK, 2)]
    if state == "solid":
        for i in range(5):
            for j in range(5):
                s.append(circle(25 + 20 * i, 25 + 20 * j, 8.5, BLUE, INK, 1))
    elif state == "liquid":
        pts = [(20, 112), (38, 108), (56, 113), (74, 107), (92, 112), (110, 108), (28, 94), (46, 90), (64, 95), (82, 89), (100, 95), (115, 90),
               (20, 76), (40, 72), (58, 78), (77, 72), (96, 77), (112, 72), (30, 58), (50, 56), (70, 60)]
        for x, y in pts:
            s.append(circle(x, y, 8.5, BLUE, INK, 1))
    else:
        for x, y in [(25, 30), (95, 22), (60, 60), (105, 90), (30, 100), (75, 110), (40, 65), (100, 55)]:
            s.append(circle(x, y, 8.5, BLUE, INK, 1))
    return svg_wrap(W, H, "".join(s), label or "particles of a %s" % state)


def three(states, letters=("A", "B", "C")):
    g = ""
    for i, (st, L) in enumerate(zip(states, letters)):
        g += "<g transform='translate(%d 0)'>%s%s</g>" % (i * 145, particles(st).split(">", 1)[1].rsplit("</svg>", 1)[0], text(65, 148, L, 16))
    return svg_wrap(145 * len(states), 156, g, "three particle diagrams").replace("<svg ", "<svg data-pf='lg' ", 1)


def g_state():
    sts = ["solid", "liquid", "gas"]
    R.shuffle(sts)
    k = R.choice(sts)
    L = dict(zip(sts, "ABC"))
    q = {"solid": "particles packed tightly and vibrating in place", "liquid": "particles close together but able to slide past each other",
         "gas": "particles far apart and moving quickly in all directions"}
    sub = R.choice(["water", "wax", "iron", "butter", "chocolate", "aluminum"])
    if R.random() < 0.5:
        return item(fig(three(sts)) + "These diagrams show particles of %s. Which diagram shows the %s state?" % (sub, k), L[k], [L[x] for x in sts if x != k] + ["none of them"],
                    "A %s has %s." % (k, q[k]))
    return item(fig(three(sts)) + "Which diagram shows %s in the state where it has %s?" % (sub, q[k]), L[k], [L[x] for x in sts if x != k] + ["all of them"],
                "That is a %s." % k)


CHANGES = [("melting", "solid", "liquid", "added"), ("freezing", "liquid", "solid", "removed"), ("boiling", "liquid", "gas", "added"),
           ("evaporation", "liquid", "gas", "added"), ("condensation", "gas", "liquid", "removed")]
EX = {"melting": ["ice cubes turning to water in a glass", "a chocolate bar getting soft in a hot car", "butter in a hot pan", "snow on a sunny sidewalk"],
      "freezing": ["water in an ice-cube tray in the freezer", "a puddle turning to ice on a cold night", "melted wax hardening on a table", "juice becoming a frozen pop"],
      "boiling": ["water bubbling in a pot on the stove", "soup making big bubbles on high heat", "water in a kettle at 100 °C"],
      "evaporation": ["a puddle drying up on a sunny day", "wet clothes drying on a line", "sweat drying from your skin"],
      "condensation": ["water drops forming on a cold glass", "fog on a bathroom mirror after a shower", "dew on grass in the morning"]}


def g_change():
    name, a, b, e = R.choice(CHANGES)
    x = R.choice(EX[name])
    k = R.choice(["name", "energy", "particles"])
    p = P.next()
    if k == "name":
        w = [c[0] for c in CHANGES if c[0] != name and not {c[0], name} <= {"boiling", "evaporation"}]
        return item("%s observes %s. What change of state is this?" % (p[0], x), name, R.sample(w, 3), "%s: %s → %s, with thermal energy %s." % (name.capitalize(), a, b, e))
    if k == "energy":
        return item("%s observes %s. Is thermal energy being added or removed?" % (p[0], x), e, ["removed" if e == "added" else "added", "neither", "Energy is being destroyed."],
                    "%s happens when thermal energy is %s." % (name.capitalize(), e))
    faster = e == "added"
    return item("%s observes %s. What happens to the motion of the particles?" % (p[0], x), "They move faster." if faster else "They move slower.",
                ["They move slower." if faster else "They move faster.", "They stop moving completely.", "The particles get bigger." if faster else "The particles get smaller."],
                "Adding energy speeds particles up; removing energy slows them down.")


SUBS = [("water", 0, 100), ("ethanol", -114, 78), ("candle wax", 60, 370), ("lead", 327, 1749), ("butter", 32, None), ("iron", 1538, 2862)]


def T(t):
    return ("−" if t < 0 else "") + comma(abs(t)) + " °C"


def g_curve():
    name, mp, bp = R.choice([s for s in SUBS if s[2]])
    start = mp - R.choice([20, 30, 40])
    steps = [start, mp, mp, mp, mp + R.choice([20, 30]), bp, bp, bp]
    if steps[4] >= bp:
        return None
    rows = [["%d" % (2 * i), T(t)] for i, t in enumerate(steps)]
    p = P.next()
    tab = table(["Time (min)", "Temperature"], rows)
    k = R.choice(["melt", "boil", "flat"])
    if k == "melt":
        return item(tab + "%s heats a sample of %s at a steady rate. At what temperature does it melt?" % (p[0], name), T(mp),
                    [T(start), T(bp), T(steps[4])], "The temperature stays at %s while the solid melts." % T(mp))
    if k == "boil":
        return item(tab + "%s heats a sample of %s at a steady rate. At what temperature does it boil?" % (p[0], name), T(bp),
                    [T(mp), T(steps[4]), T(start)], "The temperature stays at %s while the liquid boils." % T(bp))
    return item(tab + "In %s's data for %s, why does the temperature stay at %s from 2 to 6 minutes even though heat is added?" % (p[0], name, T(mp)),
                "The energy is being used to change the solid into a liquid.", ["The heater was turned off.", "The particles stopped moving.", "The thermometer broke."],
                "During a change of state, added energy changes the arrangement of particles, not the temperature.")


B1 = bank([
    ("What happens to particles when thermal energy is added?", "They move faster.", ["They move slower.", "They get bigger.", "They stop moving."], "Faster particles mean a higher temperature."),
    ("Do the particles in a solid move?", "Yes. They vibrate in place.", ["No, they are completely still.", "Only at night.", "Only in metals."], "Particles are always moving."),
    ("In which state are particles farthest apart?", "gas", ["solid", "liquid", "They are the same in all states."], "Gas particles spread out to fill their container."),
    ("Why can a liquid be poured?", "Its particles can slide past each other.", ["Its particles are far apart.", "Its particles are locked in place.", "It has no particles."],
     "Liquids flow but keep the same volume."),
    ("What does temperature measure?", "the average motion (energy) of the particles", ["the size of the particles", "the number of particles", "the color of a substance"],
     "Higher temperature means faster particles."),
    ("At sea level, at what temperature does pure water boil?", "100 °C", ["0 °C", "50 °C", "212 °C"], "Water boils at 100 °C (212 °F)."),
    ("When water vapor touches a cold window and forms drops, what happens to the particles?", "They lose energy, slow down and come closer together.", ["They gain energy.", "They get bigger.", "They disappear."],
     "Condensation removes thermal energy."),
    ("Does heating make particles bigger?", "No. They move faster and spread apart, but each particle stays the same size.", ["Yes, they swell.", "Yes, but only in gases.", "They shrink."],
     "The spaces between particles change, not the particles."),
])
B5 = bank([
    ("Ava puts the same amount of water in a freezer and on a warm counter. Which has particles moving faster?", "the water on the counter", ["the water in the freezer", "They are the same.", "Neither has moving particles."],
     "Warmer means faster particles."),
    ("Leo puts a balloon over an empty bottle and sets it in hot water. The balloon inflates. Why?", "The air particles move faster and spread apart, pushing on the balloon.", ["The air particles get bigger.", "Water gets into the balloon.", "The bottle shrinks."],
     "Heating gas particles makes them move faster."),
    ("Mia drops food coloring into hot water and cold water. Where does it spread faster?", "in the hot water", ["in the cold water", "the same in both", "it does not spread"],
     "Faster-moving particles mix the color faster."),
    ("A thermometer in melting ice reads 0 °C for several minutes while the ice melts. What explains this?", "The added energy goes into changing ice to water, not raising the temperature.", ["The thermometer is broken.", "No heat is being added.", "Ice cannot melt at 0 °C."],
     "Temperature stays flat during a change of state."),
    ("Why do sidewalks have small gaps between the slabs?", "The slabs expand in summer heat as particles move faster and spread apart.", ["To let grass grow.", "To save concrete.", "To make walking louder."],
     "Thermal expansion."),
])


def body():
    think = ("<p>All matter is made of tiny <b>particles</b> that are always moving. <b>Adding thermal energy</b> makes them move faster; <b>removing</b> it makes them move slower.</p>"
             + figure(three(["solid", "liquid", "gas"]), "A: solid (packed, vibrating). B: liquid (close, sliding). C: gas (far apart, fast).")
             + "<p>When particles move fast enough, the state can change: <b>melting</b> and <b>boiling/evaporation</b> need energy added; <b>freezing</b> and <b>condensation</b> need energy removed. "
             "During a change of state the temperature stays the same: water stays at 0 °C while it melts and at 100 °C while it boils.</p>")
    ex = [("Water vapor forms drops on a cold can. Energy added or removed?", ["Gas → liquid is condensation."], "removed"),
          ("What happens to particles when ice melts?", ["Energy is added.", "Particles move faster and slide past each other."], "They move faster and are no longer fixed in place.")]
    mist = ["Thinking particles in a solid do not move.",
            "Thinking particles get bigger when heated.",
            "Thinking temperature keeps rising while water boils."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Particles in solids, liquids and gases", B1 + [(g_state, 6), (g_change, 6)]),
        ("Particle diagrams", [(g_state, 14), (g_change, 6)]),
        ("Changes of state", [(g_change, 16), (g_state, 4)]),
        ("Heating curves", [(g_curve, 14), (g_change, 6)]),
        ("Investigations", B5 + [g_curve, g_state, g_change]),
    ])
    make("grade-6", "particles-and-states-of-matter", 5, "MS-PS1-4",
         "Develop a model that predicts and describes changes in particle motion, temperature, and state of a pure substance when thermal energy is added or removed.",
         "Particles and States of Matter",
         "Grade 6 States of Matter Worksheets: Particle Motion, Changes of State and Heating Curves",
         "Particles and States of Matter",
         "Free middle school science worksheets on particles and states of matter (NGSS MS-PS1-4): particle diagrams of solids, liquids and gases, melting, boiling and condensation, and heating curve data. 100 practice questions with answers.",
         "Thermal energy changes how fast particles move.",
         "Adding energy speeds particles up and can melt or boil a substance. Removing energy slows them and can condense or freeze it.",
         body(),
         [("How do particles move in solids, liquids and gases?", "In solids they vibrate in place, in liquids they slide past each other, and in gases they move fast and far apart."),
          ("What happens to particles when a substance is heated?", "They move faster and spread out. The particles themselves do not get bigger."),
          ("Why does temperature stay the same while water boils?", "The added energy is used to change liquid water into gas, not to raise the temperature.")],
         sets)


if __name__ == "__main__":
    main()
