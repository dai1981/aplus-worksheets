# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 7, AC9S7U04: balanced and unbalanced forces, resultant (net) force, force diagrams,
and gravity as a force that acts at a distance (weight).
  python tools/gen_au_science_y7_balanced_and_unbalanced_forces.py
Reuses the UK Year 7 force makers (resultant force, springs, weight) and the US Grade 8 force-and-motion makers (force diagrams)
with Australian names, plus own questions in Australian contexts (tug of war, a ute towing a trailer, a skydiver, a footy kick).
Wrong answers come from real mistakes: thinking a moving object must have an unbalanced force, thinking balanced forces mean the
object is still, and mixing up mass (kg) and weight (N).
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 7, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

F7 = "gen_uk_science_y7_forces"
F8 = "gen_us_science_g8_forces_and_motion"
f_bal = src(F7, "g_bal")
f_name = src(F7, "g_name", rep=[(r"about 10 N/kg", "about 9.8 N/kg (often rounded to 10 N/kg)")])
f_res = limit(src(F7, "g_res"), 6)
f_spring = limit(src(F7, "g_spring"), 3)
f_weight = limit(src(F7, "g_weight"), 4)
f_b1 = src.B(F7, "B1", rep=[(r"about 10 N/kg", "about 9.8 N/kg (often rounded to 10 N/kg)")])
f_b5 = src.B(F7, "B5")
m_net = limit(src(F8, "g_net", drop=["acceleration", "m/s²"]), 5)
m_motion = src(F8, "g_motion")
m_mass = limit(src(F8, "g_mass", drop=["acceleration", "m/s²"]), 3)
m_b1 = src.B(F8, "B1", drop=["acceleration", "m/s²"])
m_b5 = src.B(F8, "B5", drop=["acceleration", "m/s²"])

SIT = [("In a tug of war, both teams pull with 600 N and the rope does not move.", "balanced"),
       ("A skydiver falls at a steady speed; air resistance equals her weight.", "balanced"),
       ("A ute tows a trailer along the highway at a steady 100 km/h.", "balanced"),
       ("A book rests on a desk.", "balanced"),
       ("A footy is kicked and speeds up away from the boot.", "unbalanced"),
       ("A cyclist brakes and slows down.", "unbalanced"),
       ("A car turns a corner at a steady speed.", "unbalanced"),
       ("A surfboard speeds up as a wave pushes it.", "unbalanced"),
       ("A boat floats still on a calm lake.", "balanced"),
       ("A dropped apple speeds up as it falls.", "unbalanced")]


def g_sit():
    st, k = R.choice(SIT)
    return tq("%s Are the forces balanced or unbalanced?" % st, k, [x for x in ["balanced", "unbalanced", "there are no forces", "only gravity acts"] if x != k],
              "Balanced forces: no change in motion (still, or steady speed in a straight line). Unbalanced: speeding up, slowing down or changing direction.")


POOL1 = pool(R, [
    ("What is a resultant (net) force?", "the single force that has the same effect as all the forces acting together", ["the biggest force only", "the force of gravity only", "the force you push with"], "Add forces in the same direction; subtract opposite ones."),
    ("An object is moving at a steady speed in a straight line. What can you say about the forces?", "They are balanced.", ["They are unbalanced.", "There are no forces.", "Only gravity acts."], "Balanced forces do not change motion."),
    ("What is the difference between mass and weight?", "Mass is the amount of matter (kg); weight is the force of gravity on it (N).", ["They are the same.", "Weight is measured in kg.", "Mass changes on the Moon."], "Weight changes with gravity; mass does not."),
    ("Which force acts at a distance?", "gravity", ["friction", "air resistance", "a push from a hand"], "Gravity, magnetism and electrostatic forces act at a distance."),
    ("What is the unit of force?", "the newton (N)", ["the kilogram (kg)", "the metre (m)", "the second (s)"], "Named after Isaac Newton."),
    ("Why does a ball rolling on grass slow down and stop?", "Friction is an unbalanced force acting against the motion.", ["It runs out of force.", "Gravity pushes it backwards.", "Balanced forces stop it."], "An unbalanced force changes motion."),
    ("A 50 kg student stands on the floor. What is her weight on Earth (g = 9.8 N/kg)?", "490 N", ["50 N", "50 kg", "5 N"], "Weight = mass × g = 50 × 9.8 = 490 N."),
    ("What would happen to a 50 kg student's mass on the Moon?", "It stays 50 kg.", ["It becomes about 8 kg.", "It becomes 0 kg.", "It becomes 300 kg."], "Mass does not change; weight does."),
    ("In a force diagram, what does a longer arrow show?", "a bigger force", ["a faster object", "a heavier object", "a longer time"], "Arrow length shows size; direction shows direction."),
    ("A ute pulls a trailer with 2000 N; friction and drag are 2000 N. What happens?", "The ute and trailer keep the same speed.", ["They speed up.", "They stop at once.", "They go backwards."], "Balanced forces mean no change in motion."),
])
POOL5 = pool(R, [
    ("Mia hangs masses on a spring: 100 g stretches it 2 cm, 200 g stretches it 4 cm. Predict the stretch for 300 g.", "6 cm", ["3 cm", "8 cm", "2 cm"], "The stretch increases by 2 cm for each 100 g."),
    ("Jack pulls a block across different surfaces with a spring balance. Readings: wood 3 N, carpet 7 N, ice 1 N. Which surface gives the most friction?", "carpet", ["wood", "ice", "all equal"], "The biggest force was needed on carpet."),
    ("Ruby drops a ball and a crumpled sheet of paper of the same mass. The ball lands first. Why?", "The paper has more air resistance.", ["The ball is heavier.", "Gravity pulls paper less.", "Paper has no mass."], "Same mass, same weight; air resistance differs."),
    ("Kai pushes a trolley with the same force but adds bricks each time. What happens to how quickly it speeds up?", "It speeds up less as the mass increases.", ["It speeds up more.", "It stays the same.", "It goes backwards."], "More mass needs more force for the same change."),
    ("Why should a spring balance be read at eye level and zeroed before use?", "to get accurate readings", ["to make the force bigger", "to change the mass", "it is not important"], "Avoid reading errors."),
    ("Ella measures the force to pull a shoe: 4.0 N, 4.2 N, 3.9 N, 6.5 N. What should she do with 6.5 N?", "check it by repeating the test", ["use it as the main result", "delete all results", "add 2 N to the others"], "It does not fit the pattern."),
])


def main():
    sets = U.sets([
        ("Forces", [(f_name, 6), (POOL1, 5), (f_b1, 5), (m_b1, 4)]),
        ("Balanced or unbalanced?", [(g_sit, 10), (f_bal, 6), (m_motion, 4)]),
        ("Resultant force", [(f_res, 6), (m_net, 5), (POOL1, 3), (f_bal, 4), (m_b1, 2)]),
        ("Gravity and weight", [(f_weight, 4), (POOL1, 2), (f_spring, 3), (m_mass, 3), (f_bal, 3), (f_b1, 3), (f_name, 2)]),
        ("Investigations", [(POOL5, 6), (f_b5, 5), (m_b5, 5), (g_sit, 2), (m_motion, 2)]),
    ])
    make_au(YEAR, "balanced-and-unbalanced-forces", SORT, "AC9S7U04", "Physical sciences",
            "Investigate the effects of balanced and unbalanced forces, including Earth's gravitational force, on the motion of objects "
            "(summary of the Australian Curriculum v9.0 Science content description).",
            "Balanced and Unbalanced Forces", "Balanced and unbalanced forces",
            "Free Year 7 science worksheets on balanced and unbalanced forces, resultant force, force diagrams, gravity, mass and weight. "
            "100 questions with answers.",
            "Unbalanced forces change motion.", "Balanced forces: still or steady speed. Unbalanced: speeding up, slowing down or turning.",
            "<p><b>The resultant (net) force decides what happens to an object's motion.</b></p><ul>"
            "<li>Balanced forces (resultant 0 N): the object stays still or keeps moving at a steady speed in a straight line.</li>"
            "<li>Unbalanced forces: the object speeds up, slows down or changes direction.</li>"
            "<li>Gravity pulls masses together. Weight (N) = mass (kg) × 9.8 N/kg on Earth; mass does not change on the Moon.</li></ul>",
            [("Forces: 30 N right, 10 N left. Resultant?", ["30 − 10 = 20"], "20 N to the right"),
             ("A car at a steady 60 km/h. Forces?", ["no change in speed or direction"], "balanced")],
            ["Thinking a moving object must have an unbalanced force.", "Thinking balanced forces mean an object must be still.",
             "Mixing up mass (kg) and weight (N)."],
            [("What are balanced forces?", "Forces are balanced when they are equal in size and opposite in direction, so the resultant force is zero and the motion does not change."),
             ("How do I find a resultant force?", "Add forces acting in the same direction and subtract forces acting in opposite directions. The answer has a size and a direction."),
             ("What is the difference between mass and weight?", "Mass is the amount of matter in an object, measured in kilograms. Weight is the force of gravity on that mass, measured in newtons.")],
            sets, allow=("meter",))


if __name__ == "__main__":
    main()
