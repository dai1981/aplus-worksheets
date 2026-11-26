# -*- coding: utf-8 -*-
"""
US Grade 6 Science: The Water Cycle (MS-ESS2-4)
  python tools/gen_us_science_g6_the_water_cycle.py
Water cycles among land, ocean and atmosphere, driven by energy from the sun and by gravity:
evaporation, transpiration, condensation, precipitation, runoff, infiltration (groundwater), and storage
in ice and snow. A labeled model (A-D).
Assessment boundary: no latent heat or quantitative cycle.
Wrong answers come from real mistakes: "clouds are water vapor (gas)", "gravity causes evaporation",
"the water cycle has a start and an end", "rain only comes from the ocean".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, line, circle, text, arrow, sun, People, INK, BLUE

U = Unit(60108)
R = U.R
P = People(R)

PROC = {"evaporation": "liquid water turns into water vapor and rises from oceans, lakes and puddles",
        "transpiration": "plants release water vapor from their leaves",
        "condensation": "water vapor cools and turns into tiny liquid droplets that form clouds",
        "precipitation": "water falls from clouds as rain, snow, sleet or hail",
        "runoff": "water flows over the land into streams, rivers and the ocean",
        "infiltration": "water soaks into the ground and becomes groundwater"}
DRIVE = {"evaporation": "the sun", "transpiration": "the sun", "condensation": "cooling as air rises", "precipitation": "gravity", "runoff": "gravity", "infiltration": "gravity"}


def cycle_svg(marks):
    """marks: {process: letter} for evaporation, condensation, precipitation, runoff, transpiration, infiltration."""
    W, H = 440, 260
    s = [rect(0, 0, W, H, "#eef6fd", "none", 0), sun(395, 35, 16),
         "<path d='M0 200 L180 200 L230 150 L300 110 L360 150 L440 160 L440 260 L0 260 Z' fill='#cbb48a' stroke='%s' stroke-width='1.5'/>" % INK,
         rect(0, 200, 180, 60, "#7fb6e0", INK, 1.5), text(80, 240, "ocean", 13, weight=400),
         "<ellipse cx='210' cy='50' rx='55' ry='22' fill='#fff' stroke='%s' stroke-width='1.5'/>" % INK,
         line(330, 150, 330, 120, "#6b4f2a", 4), circle(330, 112, 14, "#4f9a45", INK, 1)]
    pos = {"evaporation": ((90, 190), (130, 85)), "condensation": None, "precipitation": ((240, 75), (260, 135)), "runoff": ((300, 160), (200, 195)),
           "transpiration": ((330, 98), (260, 60)), "infiltration": ((380, 175), (380, 235))}
    for pr, L in marks.items():
        if pr == "condensation":
            s.append(text(210, 55, L, 18))
            continue
        (x1, y1), (x2, y2) = pos[pr]
        s.append(arrow(x1, y1, x2, y2, BLUE, 3, 10))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(circle(mx + 12, my, 11, "#fff", INK, 1) + text(mx + 12, my + 5, L, 14))
    return svg_wrap(W, H, "".join(s), "a water cycle model with processes labeled " + ", ".join(sorted(marks.values()))).replace("<svg ", "<svg data-pf='lg' ", 1)


PICK = ["evaporation", "condensation", "precipitation", "runoff", "transpiration", "infiltration"]


def g_label():
    ps = R.sample(PICK, 4)
    L = dict(zip(ps, "ABCD"))
    p = R.choice(ps)
    who = P.next()[0]
    if R.random() < 0.5:
        return item(fig(cycle_svg(L)) + "%s labeled this water cycle model. Which letter shows %s?" % (who, p), L[p], [L[x] for x in ps if x != p],
                    "%s: %s." % (p.capitalize(), PROC[p]))
    return item(fig(cycle_svg(L)) + "In %s's water cycle model, what process does %s show?" % (who, L[p]), p, [x for x in ps if x != p], "%s: %s." % (p.capitalize(), PROC[p]))


def g_proc():
    p = R.choice(PICK)
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s reads: “%s.” Which process is this?" % (who, PROC[p][0].upper() + PROC[p][1:]), p, R.sample([x for x in PICK if x != p], 3), "That describes %s." % p)
    return item("%s asks: what happens during %s?" % (who, p), PROC[p][0].upper() + PROC[p][1:] + ".", [PROC[x][0].upper() + PROC[x][1:] + "." for x in R.sample([x for x in PICK if x != p], 3)],
                "%s: %s." % (p.capitalize(), PROC[p]))


def g_drive():
    p = R.choice(PICK)
    d = DRIVE[p]
    opts = ["the sun", "gravity", "cooling as air rises", "the moon"]
    return item("%s's class is studying %s. What mainly drives this part of the water cycle?" % (P.next()[0], p), d, [o for o in opts if o != d],
                "Energy from the sun drives evaporation and transpiration; gravity pulls water down as precipitation and runoff; cooling causes condensation.")


EVERYDAY = [("A puddle disappears on a sunny afternoon.", "evaporation"), ("Drops form on the outside of a cold glass of lemonade.", "condensation"),
            ("Snow falls on the mountains.", "precipitation"), ("Rainwater flows down a street into a storm drain.", "runoff"),
            ("A plastic bag tied over a leafy branch fills with water drops.", "transpiration"), ("Rain soaks into a garden and the soil gets wet below the surface.", "infiltration"),
            ("Fog forms over a lake on a cool morning.", "condensation"), ("Wet laundry dries on a clothesline.", "evaporation"),
            ("Hail bounces on the sidewalk.", "precipitation"), ("A muddy stream carries rainwater down a hill.", "runoff")]


def g_every():
    s, p = R.choice(EVERYDAY)
    who = P.next()[0]
    return item("%s notices this: %s Which water cycle process is it?" % (who, s), p, R.sample([x for x in PICK if x != p], 3), "%s: %s." % (p.capitalize(), PROC[p]))


B1 = bank([
    ("What provides the energy that drives the water cycle?", "the sun", ["the moon", "wind turbines", "Earth's core only"], "Sunlight heats water so it evaporates."),
    ("What force pulls rain down and makes rivers flow to the ocean?", "gravity", ["magnetism", "friction only", "sunlight"], "Gravity pulls water downhill."),
    ("Are clouds made of water vapor?", "No. Clouds are tiny drops of liquid water or ice crystals.", ["Yes, clouds are a gas.", "Clouds are made of smoke.", "Clouds are made of dust only."],
     "Water vapor is invisible; clouds form when it condenses."),
    ("Where is most of Earth's water?", "in the oceans", ["in clouds", "in rivers", "in lakes"], "About 97% of Earth's water is salty ocean water."),
    ("Does the water cycle have a beginning and an end?", "No. It is a continuous cycle.", ["Yes, it starts in the ocean and ends in clouds.", "It ends when it rains.", "It begins in winter."],
     "Water keeps moving among the ocean, air and land."),
    ("What happens to water vapor as it rises and cools?", "It condenses into droplets.", ["It evaporates more.", "It turns into salt.", "It disappears."], "Cooler air holds less water vapor."),
    ("What is groundwater?", "water that has soaked into the ground and fills spaces in soil and rock", ["water in clouds", "water in the ocean", "frozen water on mountains"],
     "Wells pump up groundwater."),
    ("Water from the ocean evaporates. What is left behind?", "salt", ["sand", "clouds", "nothing at all"], "Evaporation leaves salt behind, so rain is fresh water."),
])
B5 = bank([
    ("Ava puts plastic wrap over a bowl of water in the sun with a cold cup on top. Drops form under the wrap. What two processes does this model show?", "evaporation and condensation",
     ["runoff and infiltration", "precipitation and runoff", "transpiration and infiltration"], "Water evaporates, then condenses on the cool plastic."),
    ("Leo pours water on two trays: one with bare soil and one with grass. More water runs off the bare soil. What does this show?", "Plants help water soak into the ground.", ["Grass makes rain.", "Bare soil soaks up more water.", "Runoff does not depend on the land."],
     "Plant roots help infiltration."),
    ("Why do puddles dry faster on hot, sunny days?", "More energy from the sun makes water evaporate faster.", ["Gravity is stronger on hot days.", "The ground drinks faster.", "Clouds suck up the water."],
     "More thermal energy, faster evaporation."),
    ("A city paves over a large field. What will most likely happen to runoff after rain?", "Runoff will increase because water cannot soak into pavement.", ["Runoff will decrease.", "There will be no runoff.", "Runoff will turn into groundwater."],
     "Pavement blocks infiltration."),
    ("Mia weighs a potted plant in a sealed bag for 3 days. The bag gets foggy. What process caused this?", "transpiration", ["precipitation", "runoff", "infiltration"], "Plants release water vapor from their leaves."),
])


def body():
    think = ("<p>Water moves in a continuous <b>cycle</b> among the oceans, the atmosphere and the land. Energy from the <b>sun</b> and the pull of <b>gravity</b> drive it.</p><ul>"
             + "".join("<li><b>%s</b>: %s.</li>" % (k.capitalize(), v) for k, v in PROC.items()) + "</ul>"
             + figure(cycle_svg({"evaporation": "A", "condensation": "B", "precipitation": "C", "runoff": "D"}), "A evaporation, B condensation (clouds), C precipitation, D runoff."))
    ex = [("What drives evaporation?", ["Liquid water needs energy to become a gas."], "energy from the sun"),
          ("Drops form on a cold can. Which process?", ["Water vapor in the air cools."], "condensation")]
    mist = ["Thinking clouds are water vapor. They are liquid droplets or ice.",
            "Thinking gravity causes evaporation. The sun does.",
            "Thinking the water cycle has a start and an end."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Water cycle processes", B1 + [(g_proc, 6), (g_drive, 6)]),
        ("What happens in each process?", [(g_proc, 12), (g_every, 8)]),
        ("Water cycle models", [(g_label, 16), (g_drive, 4)]),
        ("The water cycle around you", [(g_every, 12), (g_label, 8)]),
        ("Investigations", B5 + [g_every, g_label, g_proc, g_drive]),
    ])
    make("grade-6", "the-water-cycle", 8, "MS-ESS2-4",
         "Develop a model to describe the cycling of water through Earth’s systems driven by energy from the sun and the force of gravity.",
         "The Water Cycle",
         "Grade 6 Water Cycle Worksheets: Evaporation, Condensation, Precipitation and Runoff",
         "The Water Cycle",
         "Free middle school science worksheets on the water cycle (NGSS MS-ESS2-4): evaporation, transpiration, condensation, precipitation, runoff and infiltration, the roles of the sun and gravity, and labeled models. 100 practice questions with answers.",
         "The sun and gravity drive the water cycle.",
         "Water evaporates, condenses into clouds, falls as precipitation, and flows or soaks back to the ocean, again and again.",
         body(),
         [("What drives the water cycle?", "Energy from the sun causes evaporation and transpiration, and gravity pulls water down as precipitation and runoff."),
          ("What are clouds made of?", "Tiny droplets of liquid water or ice crystals that formed when water vapor cooled and condensed."),
          ("What is the difference between runoff and infiltration?", "Runoff flows over the land into streams and rivers. Infiltration soaks into the ground and becomes groundwater.")],
         sets)


if __name__ == "__main__":
    main()
