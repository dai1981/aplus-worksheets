# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 4, AC9S4U03: contact forces - pushes, pulls, friction and air and water resistance.
  python tools/gen_au_science_y4_friction_and_contact_forces.py
Reuses the UK Year 3 pushes-and-pulls makers and the UK Year 5 friction and resistance makers with Australian names, plus own
questions on Australian contexts (surf lifesaving, cricket, footy boots, sand on a beach path, a wombat's burrow).
Wrong answers come from real mistakes: thinking friction always acts against the push you give (it acts against the motion),
thinking smooth surfaces have no friction at all, and thinking friction is always unhelpful.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 4, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

F5 = "gen_uk_science_y5_friction"
PP = "gen_uk_science_y3_pushes_pulls_and_surfaces"
AR = "gen_uk_science_y5_air_and_water_resistance"
f_chg = src(F5, "g_chg")
f_dir = limit(src(F5, "g_dir"), 4)
f_ramp = limit(src(F5, "g_ramp"), 3)
f_use = src(F5, "g_use")
f_b1 = src.B(F5, "B1")
f_b5 = src.B(F5, "B5")
p_contact = src(PP, "g_contact")
p_do = src(PP, "g_do")
p_pp = src(PP, "g_pp")
p_surf = limit(src(PP, "g_surf"), 2)
p_b1 = src.B(PP, "B1")
a_chute = limit(src(AR, "g_chute"), 3)
a_dir = src(AR, "g_dir")
a_stream = src(AR, "g_stream", drop=["sycamore", "penguin swimming"])
a_b1 = src.B(AR, "B1")

POOL1 = pool(R, [
    ("What is friction?", "a force between two surfaces that slows or stops movement", ["a force that only pulls things down", "a force that makes things lighter", "a kind of magnet"], "Friction acts where surfaces rub."),
    ("Why do footy boots have studs?", "to increase friction and grip on the grass", ["to make the boots lighter", "to reduce friction so players slide", "to keep feet warm"], "More grip helps players turn and stop."),
    ("Why do cricketers rub the ball on their trousers?", "to keep one side smooth and shiny, changing how air flows past it", ["to make it heavier", "to make it bounce higher", "to warm it up"], "Air resistance acts differently on smooth and rough sides."),
    ("Why do surf lifesavers' boards have wax on top?", "Wax increases friction so their feet do not slip.", ["Wax makes boards float.", "Wax makes boards faster on the sand.", "Wax keeps boards cool."], "More friction means more grip."),
    ("Why is it hard to walk on soft, dry sand?", "Your feet slide and sink, so it takes more force to move.", ["Sand has no friction at all.", "Sand pulls you down like a magnet.", "Sand is slippery like ice."], "Loose sand moves under your feet."),
    ("Which surface gives the most friction for a toy car?", "carpet", ["ice", "a polished floor", "a wet tile"], "Rough surfaces give more friction."),
    ("What happens to your hands when you rub them together quickly?", "They get warm because friction makes heat.", ["They get cold.", "They get wet.", "Nothing happens."], "Friction changes movement energy into heat."),
    ("Which is a non-contact force?", "gravity pulling a ball down", ["a hand pushing a door", "friction slowing a bike", "a rope pulling a boat"], "Non-contact forces act from a distance."),
    ("Why do mountain bike tyres have deep tread?", "to grip loose dirt and mud", ["to make the bike quieter", "to make it lighter", "to stop the tyres being round"], "Tread increases friction."),
    ("A wombat pushes soil out of its burrow. What kind of force is this?", "a push (a contact force)", ["a pull from a distance", "magnetism", "gravity only"], "The wombat touches the soil."),
])
POOL5 = pool(R, [
    ("Mia pulls a shoe across different floors with a spring balance: tiles 2 N, carpet 6 N, wood 3 N. Which floor has the most friction?", "carpet", ["tiles", "wood", "all the same"], "The biggest force was needed on carpet."),
    ("In Mia's test, what should stay the same?", "the shoe and the way she pulls it", ["the floor", "the force reading", "nothing"], "Only the floor should change."),
    ("Jack rolls a car down a ramp onto sand, grass and concrete. It goes 20 cm on sand, 60 cm on grass and 150 cm on concrete. Which surface has the least friction?", "concrete", ["sand", "grass", "they are equal"], "Less friction, further travel."),
    ("Ruby says, 'A ball rolling on a smooth floor has no friction.' Why is this not right?", "There is still a little friction, so the ball slowly stops.", ["Smooth floors have the most friction.", "Balls cannot roll on smooth floors.", "Friction only acts on rough surfaces."], "Friction is smaller on smooth surfaces but not zero."),
    ("Kai drops paper parachutes of different sizes from the same height. What should he measure?", "the time each takes to fall", ["the colour of each", "the height of the room only", "the size of each"], "He changes the size and measures the time."),
    ("Noah wants to know which shoe sole grips best on a wet floor. Which plan is fair?", "pull each shoe with the same mass inside across the same wet floor and measure the force", ["use a different floor for each shoe", "pull each shoe at a different speed and guess", "test only one shoe"], "Change only the shoe sole."),
])


def main():
    sets = U.sets([
        ("Pushes and pulls", [(p_pp, 6), (p_do, 5), (p_contact, 5), (p_b1, 2), (POOL1, 2)]),
        ("Friction", [(POOL1, 5), (f_dir, 4), (f_b1, 4), (p_surf, 4), (f_chg, 3)]),
        ("Helpful or unhelpful?", [(f_use, 8), (f_chg, 5), (POOL1, 3), (p_surf, 1), (f_b1, 3)]),
        ("Air and water resistance", [(a_dir, 5), (a_stream, 6), (a_b1, 5), (a_chute, 2), (p_contact, 2)]),
        ("Investigations", [(POOL5, 6), (f_b5, 4), (f_ramp, 3), (a_chute, 1), (p_contact, 2), (f_use, 2), (a_stream, 2)]),
    ])
    make_au(YEAR, "friction-and-contact-forces", SORT, "AC9S4U03", "Physical sciences",
            "Identify that forces can be exerted by one object on another by direct contact, such as pushes, pulls and friction, or from a "
            "distance (summary of the Australian Curriculum v9.0 Science content description).",
            "Friction and Contact Forces", "Friction and contact forces",
            "Free Year 4 science worksheets on pushes, pulls, friction and air and water resistance, with examples from footy, cricket, "
            "surfing and bike riding. 100 questions with answers.",
            "Friction slows things down where surfaces touch.", "Contact forces act when objects touch; friction acts against the movement.",
            "<p><b>Contact forces happen when objects touch: pushes, pulls and friction.</b></p><ul>"
            "<li>A force can start an object moving, stop it, speed it up, slow it down, change its direction or change its shape.</li>"
            "<li>Friction acts between surfaces, against the direction of movement. Rough surfaces give more friction than smooth ones.</li>"
            "<li>Air resistance and water resistance are kinds of friction. Streamlined shapes reduce them; parachutes increase air resistance.</li></ul>",
            [("A box slides to the right. Which way does friction act?", ["friction acts against the movement"], "to the left"),
             ("Why do footy boots have studs?", ["studs dig into the grass", "more grip"], "more friction")],
            ["Thinking smooth surfaces have no friction at all.", "Thinking friction is always unhelpful (we need it to walk and to brake).",
             "Thinking friction acts in the same direction as the movement."],
            [("What is friction?", "Friction is a force between two surfaces that rub together. It acts against the movement and slows things down."),
             ("How can we increase or reduce friction?", "Rough surfaces, treads and grippy materials increase friction. Smooth surfaces, oil, wax on skis and wheels reduce it."),
             ("Is air resistance a kind of friction?", "Yes. Air resistance is friction between a moving object and the air. Water resistance is friction with water.")],
            sets)


if __name__ == "__main__":
    main()
