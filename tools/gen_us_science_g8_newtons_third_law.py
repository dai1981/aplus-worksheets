# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Newton's Third Law (MS-PS2-1)
  python tools/gen_us_science_g8_newtons_third_law.py
Apply Newton's third law to design a solution to a problem involving the motion of two colliding objects.
For every action force there is an equal and opposite reaction force on the other object; the forces act on
different objects, so they do not cancel. In a collision both objects feel the same size force; the less massive
object changes speed more. Designs: bumpers, helmets, crumple zones, airbags (spreading force over time).
Wrong answers come from real mistakes: "the bigger object pushes harder", "action and reaction cancel so nothing moves",
"the reaction happens later".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(80101)
R = U.R
P = People(R)

PAIRS = [("A swimmer pushes water backward.", "The water pushes the swimmer forward."), ("A rocket pushes hot gas downward.", "The gas pushes the rocket upward."),
         ("A person steps off a small boat onto a dock.", "The boat is pushed backward away from the dock."), ("A skater pushes against a wall.", "The wall pushes the skater away."),
         ("A hammer hits a nail.", "The nail pushes back on the hammer with an equal force."), ("A bird's wings push air down.", "The air pushes the wings up."),
         ("A runner's foot pushes back on the ground.", "The ground pushes the runner forward."), ("A balloon lets air rush out the back.", "The air pushes the balloon forward."),
         ("A cannon fires a cannonball forward.", "The cannonball pushes the cannon backward (recoil)."), ("A car tire pushes back on the road.", "The road pushes the car forward.")]


def g_pair():
    a, b = R.choice(PAIRS)
    who = P.next()[0]
    w = [x[1] for x in PAIRS if x[1] != b]
    return item("%s writes an action force: “%s” What is the reaction force?" % (who, a), b, R.sample(w, 3), "Reaction forces are equal in size, opposite in direction and act on the other object.")


def g_size():
    m1 = R.choice([("a truck", "a small car"), ("a bowling ball", "a tennis ball"), ("an adult", "a child"), ("a large cart", "a small cart"), ("a football lineman", "a kicker")])
    big, small = m1
    who = P.next()[0]
    k = R.choice(["force", "speed"])
    if k == "force":
        return item("%s asks: when %s and %s collide, which one feels the bigger force?" % (who, big, small), "Both feel forces of the same size.",
                    ["%s feels a bigger force." % (big[0].upper() + big[1:]), "%s feels a bigger force." % (small[0].upper() + small[1:]), "Neither feels a force."],
                    "Newton's third law: the forces are equal and opposite.")
    return item("%s asks: when %s and %s collide, which one changes its speed more?" % (who, big, small), small[0].upper() + small[1:] + ", because it has less mass.",
                [big[0].upper() + big[1:] + ", because it has more mass.", "They change speed by the same amount.", "Neither changes speed."],
                "Equal forces, but the smaller mass accelerates more.")


def g_carts():
    m1 = R.choice([1, 2])
    m2 = m1 * R.choice([2, 3, 4])
    v = R.choice([2, 3, 4, 6])
    who = P.next()[0]
    rows = [["Cart A", "%d kg" % m1], ["Cart B", "%d kg" % m2]]
    tab = table(["Cart", "Mass"], rows)
    k = R.choice(["push", "which", "ratio"])
    if k == "push":
        return item(tab + "%s puts a compressed spring between two carts at rest and releases it. How do the forces on the carts compare?" % who, "They are equal in size and opposite in direction.",
                    ["Cart B gets a bigger force.", "Cart A gets a bigger force.", "Only one cart gets a force."], "The spring pushes both carts equally.")
    if k == "which":
        return item(tab + "After %s releases the spring, which cart moves faster?" % who, "Cart A", ["Cart B", "They move at the same speed.", "Neither moves."],
                    "Cart A has less mass, so the same force gives it a bigger change in speed.")
    r = m2 // m1
    return item(tab + "In %s's test, cart B has %d times the mass of cart A. Cart A rolls away at %d m/s. About how fast does cart B roll the other way?" % (who, r, v * r),
                "%d m/s" % v, ["%d m/s" % (v * r), "%d m/s" % (v * r * r), "0 m/s"], "Equal forces: %d times the mass gives 1/%d the speed: %d ÷ %d = %d m/s." % (r, r, v * r, r, v))


DESIGN = [("A bike helmet has a foam liner.", "The foam crushes and spreads the collision force over a longer time, so less force reaches the head."),
          ("Cars have crumple zones at the front.", "The front crumples slowly, which lengthens the collision time and lowers the force on passengers."),
          ("Airbags inflate in a crash.", "The airbag slows the person over a longer time and a larger area."),
          ("Gymnastics mats are thick and soft.", "They increase the stopping time, so the force on the gymnast is smaller."),
          ("Bumper cars have rubber bumpers.", "The rubber squishes, so the collision lasts longer and feels gentler."),
          ("Egg cartons have soft dividers.", "They spread and soften collision forces on each egg.")]


def g_design():
    s, a = R.choice(DESIGN)
    who = P.next()[0]
    return item("%s notices: “%s” How does this design protect people or objects?" % (who, s), a,
                ["It makes the reaction force bigger.", "It removes Newton's third law.", "It makes the object heavier so nothing moves."], "Spreading a collision over more time reduces the force.")


B1 = bank([
    ("What does Newton's third law say?", "For every action force, there is an equal and opposite reaction force.", ["Heavier objects push harder.", "Forces only act on one object.", "Objects at rest stay at rest."],
     "Forces always come in pairs."),
    ("Why don't action and reaction forces cancel out?", "They act on different objects.", ["They are different sizes.", "They act at different times.", "They do cancel, so nothing moves."], "You can only cancel forces on the same object."),
    ("When you push on a wall, what does the wall do?", "It pushes back on you with the same size force.", ["Nothing.", "It pushes back harder.", "It pulls you toward it."], "That is why you can feel the wall."),
    ("How does a rocket move in space where there is no air to push on?", "It pushes gas out the back, and the gas pushes the rocket forward.", ["It pushes on the air.", "It is pulled by stars.", "It cannot move in space."],
     "No air is needed."),
    ("A mosquito hits a car windshield. Which feels the larger force?", "Both feel the same force; the mosquito has much less mass, so it is affected more.", ["The car.", "The mosquito.", "Neither."],
     "Equal forces, different effects."),
    ("Do action and reaction forces happen at the same time?", "Yes, at exactly the same time.", ["No, the reaction comes later.", "Only in collisions.", "Only for heavy objects."], "They are simultaneous."),
    ("Why does a gun or cannon recoil?", "The bullet or cannonball pushes back on it with an equal and opposite force.", ["It is too heavy.", "Air pushes it.", "Gravity pulls it backward."], "Recoil is a reaction force."),
    ("What is a good criterion for a car bumper design?", "It reduces the force on passengers in a collision.", ["It makes the car look shiny.", "It makes the car heavier.", "It increases the force."],
     "Designs aim to reduce forces on people."),
])
B5 = bank([
    ("Ava drops an egg onto a pillow and onto the floor from the same height. The pillow egg survives. Why?", "The pillow increases the stopping time, so the force is smaller.", ["The pillow makes no force.", "Eggs are stronger on pillows.", "Gravity is weaker over pillows."],
     "Longer collision time, smaller force."),
    ("Leo designs a cart bumper and tests it with a force sensor. Which result shows the best design?", "the smallest peak force when the cart hits the wall", ["the loudest crash", "the largest peak force", "the fastest bounce"],
     "Lower force means more protection."),
    ("Mia sits on a skateboard and throws a heavy ball forward. What happens to her?", "She rolls backward.", ["She rolls forward.", "Nothing happens.", "She rises up."], "The ball pushes back on her."),
    ("Why should two carts of different mass be tested several times in a collision experiment?", "to get reliable results", ["to make the carts heavier", "to change Newton's law", "to waste time"], "Repeat trials."),
    ("A student says the heavier cart pushed harder in the collision. How would you correct this?", "Both carts pushed with equal force; the lighter cart changed speed more.", ["The lighter cart pushed harder.", "Neither cart pushed.", "The student is right."],
     "Newton's third law."),
])


def body():
    think = ("<p><b>Newton's third law</b>: for every action force there is an <b>equal and opposite</b> reaction force. The two forces act on <b>different objects</b> at the same time, so they do not cancel.</p>"
             "<p>In a collision, both objects feel forces of the <b>same size</b>. The object with <b>less mass</b> changes its speed more.</p>"
             "<p>Engineers use this to design safer collisions: helmets, airbags, bumpers and crumple zones <b>spread the force over a longer time</b>, so the force on people is smaller.</p>")
    ex = [("A truck and a car collide. Which feels a bigger force?", ["Third law: equal forces."], "Neither; the forces are equal."),
          ("A swimmer pushes water back. What pushes the swimmer forward?", ["Reaction force."], "the water")]
    mist = ["Thinking the bigger object pushes harder.",
            "Thinking action and reaction cancel out. They act on different objects.",
            "Thinking the reaction happens after the action."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Action and reaction", B1 + [(g_pair, 12)]),
        ("Force pairs", [(g_pair, 12), (g_size, 8)]),
        ("Collisions and mass", [(g_size, 10), (g_carts, 10)]),
        ("Designing for collisions", [(g_design, 12), (g_carts, 8)]),
        ("Testing designs", B5 + [g_carts, g_design, g_size, g_pair]),
    ])
    make("grade-8", "newtons-third-law", 1, "MS-PS2-1",
         "Apply Newton's Third Law to design a solution to a problem involving the motion of two colliding objects.",
         "Newton's Third Law",
         "Grade 8 Newton's Third Law Worksheets: Action-Reaction Forces and Collisions",
         "Newton's Third Law",
         "Free middle school science worksheets on Newton's third law (NGSS MS-PS2-1): action-reaction force pairs, collisions between objects of different mass, and designing bumpers, helmets and airbags. 100 practice questions with answers.",
         "Every action has an equal and opposite reaction.",
         "Colliding objects push on each other with equal forces. The lighter object changes speed more.",
         body(),
         [("What is Newton's third law?", "For every action force there is an equal and opposite reaction force acting on the other object."),
          ("In a collision, which object feels the bigger force?", "Neither. Both feel forces of the same size, but the object with less mass changes its speed more."),
          ("How do helmets and airbags use physics?", "They make a collision last longer, which spreads out the force and reduces the force on a person.")],
         sets)


if __name__ == "__main__":
    main()
