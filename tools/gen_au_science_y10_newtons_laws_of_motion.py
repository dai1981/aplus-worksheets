# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 10, AC9S10U05: Newton's three laws of motion, net force, F = ma, weight W = mg,
speed, velocity and acceleration, and stopping distances and car safety.
  python tools/gen_au_science_y10_newtons_laws_of_motion.py
Reuses the US Physics Newton's laws and kinematics makers, the US Grade 8 forces and Newton's third law makers and the UK
Year 11 forces and motion makers with Australian names, plus own questions on road safety and Australian contexts.
Wrong answers come from real mistakes: thinking a moving object needs a force to keep moving, thinking action-reaction forces
cancel, and confusing mass and weight.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 10, 5
U, R, P, src = AU(seed_of(YEAR, SORT))

NL = "gen_us_science_phys_newtons_laws_and_net_force"
KI = "gen_us_science_phys_motion_and_kinematics"
F8 = "gen_us_science_g8_forces_and_motion"
T8 = "gen_us_science_g8_newtons_third_law"
F11 = "gen_uk_science_y11_forces_and_motion"
NO = ["mph", "mile", "feet", "foot", "pound", " lb"]
n_fma = limit(src(NL, "g_fma", drop=NO), 8)
n_net = limit(src(NL, "g_net", drop=NO), 6)
n_law = src(NL, "g_law", drop=NO)
n_w = limit(src(NL, "g_weight", drop=NO), 5)
n_data = src(NL, "g_data", drop=NO)
n_b1 = src.B(NL, "B1", drop=NO)
n_b5 = src.B(NL, "B5", drop=NO)
k_acc = limit(src(KI, "g_acc", drop=NO), 6)
k_speed = limit(src(KI, "g_speed", drop=NO), 5)
k_data = limit(src(KI, "g_data", drop=NO), 4)
k_b1 = src.B(KI, "B1", drop=NO)
f_force = src(F8, "g_force", drop=NO)
f_mass = src(F8, "g_mass", drop=NO)
t_pair = src(T8, "g_pair", drop=NO)
t_size = src(T8, "g_size", drop=NO)
t_b1 = src.B(T8, "B1", drop=NO)
u_stop = limit(src(F11, "g_stop", drop=NO), 5)

POOL1 = pool(R, [
    ("What is Newton's first law?", "An object stays at rest or keeps moving at a constant velocity unless a net force acts on it.", ["Every moving object slows down by itself.", "Force equals mass times acceleration.", "Every action has an equal and opposite reaction."], "This is the law of inertia."),
    ("What is Newton's second law?", "The acceleration of an object is proportional to the net force and inversely proportional to its mass (F = ma).", ["Objects at rest stay at rest.", "Forces come in pairs.", "Heavier objects fall faster."], "Double the force, double the acceleration."),
    ("What is Newton's third law?", "When one object exerts a force on another, the second exerts an equal and opposite force on the first.", ["Forces always cancel out.", "Bigger objects push harder.", "Only moving objects exert forces."], "The two forces act on different objects."),
    ("Why do seatbelts help in a crash?", "They stop your body continuing forward because of inertia, and spread the force.", ["They make the car lighter.", "They push you forward.", "They stop the car."], "Your body keeps moving when the car stops."),
    ("What is the difference between mass and weight?", "Mass is the amount of matter (kg); weight is the force of gravity on it (N).", ["They are the same thing.", "Weight is measured in kg.", "Mass changes on the Moon."], "W = mg, with g = 9.8 N/kg on Earth."),
    ("A rocket pushes hot gas downwards. Why does it go up?", "The gas pushes back up on the rocket with an equal and opposite force.", ["The gas pulls the rocket.", "Air holds it up.", "Gravity pushes it up."], "Newton's third law."),
    ("A car moves at a constant 60 km/h on a straight road. What is the net force on it?", "zero", ["the engine force", "the weight of the car", "it cannot be known"], "Constant velocity means balanced forces."),
    ("Why is it harder to push a full trolley than an empty one with the same acceleration?", "More mass needs more force for the same acceleration.", ["The full trolley has less inertia.", "Friction disappears when empty.", "Mass does not matter."], "F = ma."),
    ("What happens to your stopping distance in the rain?", "It increases, because there is less friction between tyres and road.", ["It decreases.", "It stays the same.", "It becomes zero."], "Braking distance increases on wet roads."),
    ("What is reaction distance?", "the distance travelled while the driver reacts, before braking starts", ["the distance travelled while braking", "the total length of the car", "the distance to the next car"], "Tiredness, phones and alcohol increase reaction time."),
    ("What is acceleration?", "the rate of change of velocity", ["the distance travelled", "the speed at the end", "the force on an object"], "Measured in m/s²."),
    ("A bike speeds up from 2 m/s to 8 m/s in 3 s. What is its acceleration?", "2 m/s²", ["6 m/s²", "18 m/s²", "3 m/s²"], "(8 − 2) ÷ 3 = 2."),
])
POOL5 = pool(R, [
    ("Mia pulls a trolley with a force meter and doubles the force. The acceleration doubles. What does this support?", "Newton's second law: acceleration is proportional to force", ["Newton's first law only", "Newton's third law only", "no law"], "Keep the mass the same."),
    ("Jack adds masses to a trolley but keeps the pulling force the same. What happens to the acceleration?", "It decreases.", ["It increases.", "It stays the same.", "It becomes zero."], "a = F ÷ m."),
    ("Ruby uses light gates to measure a trolley's acceleration. Why are light gates better than a stopwatch?", "They remove human reaction-time error.", ["They make the trolley faster.", "They change the mass.", "They add friction."], "More accurate timing."),
    ("Kai designs an egg-drop capsule. Why does a crumple zone protect the egg?", "It increases the stopping time, so the force on the egg is smaller.", ["It makes the egg heavier.", "It speeds up the egg.", "It removes gravity."], "Car crumple zones work the same way."),
    ("Ella graphs force against acceleration for a trolley. The line is straight through the origin. What does the gradient show?", "the mass of the trolley", ["the speed", "the distance", "the friction only"], "F = ma, so gradient = m."),
    ("A 1500 kg car accelerates at 2 m/s². What net force acts on it?", "3000 N", ["750 N", "1502 N", "30 000 N"], "F = ma = 1500 × 2."),
    ("Noah's 50 kg mass weighs 490 N on Earth. What would it weigh on the Moon (g = 1.6 N/kg)?", "80 N", ["490 N", "50 N", "800 N"], "W = mg = 50 × 1.6. Its mass is still 50 kg."),
    ("Zara tests how a driver's reaction time changes when using a phone. What should she keep the same?", "the test, the person and the conditions, changing only phone use", ["the phone use", "nothing", "the reaction time"], "Only phone use should change."),
])


def main():
    sets = U.sets([
        ("Newton's laws", [(POOL1, 6), (n_law, 6), (n_b1, 4), (f_force, 4)]),
        ("Net force and F = ma", [(n_net, 5), (n_fma, 7), (f_mass, 4), (POOL1, 2), (n_data, 2)]),
        ("Weight, speed and acceleration", [(n_w, 5), (k_acc, 6), (k_speed, 4), (POOL1, 2), (k_b1, 3)]),
        ("Action–reaction and road safety", [(t_pair, 5), (t_size, 4), (u_stop, 5), (t_b1, 3), (POOL1, 3)]),
        ("Investigations", [(POOL5, 7), (n_b5, 4), (k_data, 4), (n_fma, 2), (n_data, 3)]),
    ])
    make_au(YEAR, "newtons-laws-of-motion", SORT, "AC9S10U05", "Physical sciences",
            "Investigate Newton's laws of motion and quantitatively analyse the relationship between force, mass and acceleration "
            "of objects (summary of the Australian Curriculum v9.0 Science content description).",
            "Newton's Laws of Motion", "Newton's laws",
            "Free Year 10 science worksheets on Newton's laws of motion: inertia, net force, F = ma, weight and mass, acceleration, "
            "action–reaction pairs, and stopping distances and car safety. 100 questions with answers.",
            "F = ma", "A net force makes an object accelerate; more mass needs more force for the same acceleration.",
            "<p><b>Newton's three laws describe how forces change motion.</b></p><ul>"
            "<li>First law: without a net force, an object stays at rest or keeps moving at constant velocity (inertia).</li>"
            "<li>Second law: F = ma. Weight W = mg, with g = 9.8 N/kg on Earth. Acceleration = change in velocity ÷ time.</li>"
            "<li>Third law: forces come in equal and opposite pairs acting on different objects.</li></ul>",
            [("Net force 600 N on a 200 kg cart. Acceleration?", ["a = F ÷ m", "600 ÷ 200"], "3 m/s²"),
             ("A 60 kg student. Weight on Earth?", ["W = mg", "60 × 9.8"], "588 N")],
            ["Thinking a moving object needs a force to keep moving at constant speed.",
             "Thinking action–reaction forces cancel (they act on different objects).", "Mixing up mass (kg) and weight (N)."],
            [("Why don't action and reaction forces cancel?", "They act on different objects. Only forces acting on the same object can cancel each other."),
             ("How do car safety features use Newton's laws?", "Seatbelts and airbags stop your body continuing forward (first law) and increase the stopping time, so the force on you is smaller (second law)."),
             ("What affects stopping distance?", "Stopping distance = reaction distance + braking distance. Speed, tiredness, alcohol and phones increase reaction distance; wet roads and worn tyres increase braking distance.")],
            sets, allow=("meter",))


if __name__ == "__main__":
    main()
