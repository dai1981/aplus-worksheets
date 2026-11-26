# -*- coding: utf-8 -*-
"""
US High School Physics: Impulse and Collision Safety (HS-PS2-3)
  python tools/gen_us_science_phys_impulse_and_collision_safety.py
Apply scientific and engineering ideas to design, evaluate, and refine a device that minimizes the force on a
macroscopic object during a collision.
Impulse J = FΔt = Δp, force from change in momentum and stopping time, bouncing vs stopping, and safety devices
(air bags, helmets, crumple zones, mats) evaluated with test data and criteria.
Wrong answers come from real mistakes: "air bags reduce the change in momentum", "a harder surface is safer",
"bouncing has a smaller change in momentum", "a longer stopping time means a larger force".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90304)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def An(w):
    return ("An " if w[0] in "aeiou8" or w.startswith("18") else "A ") + w


@safe
def g_imp():
    o, m = R.choice([("70 kg crash-test dummy", 70), ("0.5 kg ball", 0.5), ("60 kg passenger", 60), ("2 kg melon", 2), ("0.06 kg egg", 0.06), ("80 kg skydiver", 80), ("5 kg bowling ball", 5)])
    v = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    dt = R.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.4, 0.5])
    dp = m * v
    F = dp / dt
    k = R.choice(["J", "F", "F", "t"])
    if F != round(F, 1) or not once(("im", o, v, dt, k)):
        return None
    if k == "J":
        g = "%s N·s" % num(dp, 2)
        return item("%s moving at %d m/s is brought to a stop. What impulse acts on it?" % (An(o), v), g, uniq(g, ["%s N·s" % num(m / v, 3), "%s N·s" % num(0.5 * m * v * v, 2), "%s N·s" % num(dp * 2, 2), "%s N·s" % num(m + v, 2)]),
                    "J = Δp = mv = %s × %d = %s N·s." % (num(m, 2), v, num(dp, 2)))
    if k == "F":
        g = "%s N" % num(F, 1)
        return item("%s moving at %d m/s stops in %s s. What average force acts on it?" % (An(o), v, num(dt)), g, uniq(g, ["%s N" % num(dp * dt, 3), "%s N" % num(dp, 2), "%s N" % num(m * v / dt / 9.8, 1), "%s N" % num(F * 2, 1)]),
                    "F = Δp ÷ Δt = %s ÷ %s = %s N." % (num(dp, 2), num(dt), num(F, 1)))
    g = "%s s" % num(dt)
    return item("%s moving at %d m/s is stopped by an average force of %s N. How long does the stop take?" % (An(o), v, num(F, 1)), g, uniq(g, ["%s s" % num(F / dp, 2), "%s s" % num(dp * F, 1), "%s s" % num(dt * 2), "%s s" % num(dt / 2, 3)]),
                "Δt = Δp ÷ F = %s ÷ %s = %s s." % (num(dp, 2), num(F, 1), num(dt)))


@safe
def g_ratio():
    t1 = R.choice([0.01, 0.02, 0.05, 0.1])
    r = R.choice([2, 3, 4, 5, 10])
    who = P.next()[0]
    if not once(("rt", t1, r)):
        return None
    s = R.choice(["a helmet's foam", "an air bag", "a crash mat", "a car's crumple zone", "bending the knees on landing"])
    g = "1/%d of the force" % r
    return item("%s finds that %s makes a stop take %s s instead of %s s. The change in momentum is the same. How does the force compare?" % (who, s, num(t1 * r), num(t1)), g,
                uniq(g, ["%d times the force" % r, "the same force", "1/%d of the force" % (r * r), "%d times the force" % (r * r)]), "F = Δp ÷ Δt: %d times the time → 1/%d of the force." % (r, r))


@safe
def g_bounce():
    m = R.choice([0.1, 0.2, 0.5, 1, 2])
    v = R.choice([2, 4, 5, 6, 8, 10])
    vb = R.choice([v, v // 2 if v > 2 else 1, v - 1])
    k = R.choice(["dp", "which"])
    if not once(("bn", m, v, vb, k)):
        return None
    if k == "dp":
        dp = m * (v + vb)
        g = "%s kg·m/s" % num(dp, 2)
        return item("A %s kg ball hits a wall at %d m/s and bounces straight back at %d m/s. What is the size of its change in momentum?" % (num(m), v, vb), g,
                    uniq(g, ["%s kg·m/s" % num(m * (v - vb), 2), "%s kg·m/s" % num(m * v, 2), "0 kg·m/s", "%s kg·m/s" % num(m * v * vb, 2)]),
                    "Δp = m(v + v_back) = %s × (%d + %d) = %s kg·m/s." % (num(m), v, vb, num(dp, 2)))
    return item("Two identical balls hit a wall at %d m/s for the same contact time. One stops; the other bounces back. Which feels the larger force?" % v, "the one that bounces back",
                ["the one that stops", "They feel the same force.", "Neither feels a force."], "Bouncing reverses the momentum, so Δp is larger.")


DEV = [("an air bag", "It inflates so the passenger takes longer to stop."), ("foam inside a bike helmet", "It crushes and spreads the stop over more time and area."),
       ("a car's crumple zone", "The front of the car crushes slowly, increasing stopping time."), ("a thick gymnastics mat", "It squashes so the gymnast stops over a longer time."),
       ("bending your knees when you land", "It increases the time to stop your body."), ("sand in a long-jump pit", "The jumper sinks in and stops more gradually."),
       ("a catcher pulling the mitt back", "It lengthens the time to stop the ball."), ("highway crash barrels filled with water", "They spread the stop of a car over more time.")]


@safe
def g_dev():
    d, w = R.choice(DEV)
    k = R.random() < 0.6
    if not once(("dv", d, k)):
        return None
    if k:
        return item("How does %s reduce the force in a collision?" % d, w, ["It reduces the change in momentum to zero.", "It makes the stop take less time.", "It makes the object heavier."],
                    "Same Δp over a longer Δt gives a smaller force.")
    return item("Which change would make %s work worse?" % d, "making it stiffer so the stop happens faster", ["making it softer so the stop takes longer", "making it thicker", "making it cover a larger area"],
                "Less stopping time → larger force.")


@safe
def g_test():
    who = P.next()[0]
    designs = R.sample(["foam cup", "bubble wrap", "parachute", "cotton balls", "straw frame", "balloon cushion", "sponge box", "paper springs"], 4)
    ts = R.sample([0.005, 0.01, 0.02, 0.04, 0.05, 0.08], 4)
    m, v = 0.06, 5
    Fs = [m * v / t for t in ts]
    k = R.choice(["best", "force", "why"])
    if not once(("ts", tuple(designs), k)) or (k == "why" and not once("tsw", 3)):
        return None
    tab = table(["Egg-drop design", "Stopping time (s)"], [[d, num(t, 3)] for d, t in zip(designs, ts)])
    i = ts.index(max(ts))
    if k == "best":
        return item(tab + "%s drops a 0.06 kg egg at 5 m/s onto each design. Which design gives the smallest force on the egg?" % who, designs[i],
                    [d for j, d in enumerate(designs) if j != i], "Longest stopping time → smallest force.")
    if k == "force":
        j = R.randrange(4)
        g = "%s N" % num(Fs[j], 1)
        return item(tab + "A 0.06 kg egg hits %s's %s at 5 m/s. What average force stops it?" % (who, designs[j]), g,
                    uniq(g, ["%s N" % num(0.3 * ts[j], 4), "0.3 N", "%s N" % num(Fs[j] * 2, 1), "%s N" % num(Fs[j] / 2, 1)]),
                    "F = Δp ÷ Δt = 0.3 ÷ %s = %s N." % (num(ts[j], 3), num(Fs[j], 1)))
    return item(tab + "Why should %s drop every design from the same height?" % who, "so every egg has the same change in momentum and the test is fair",
                ["to make the eggs heavier", "so the force is always zero", "to make the times longer"], "Control variables.")


B1 = bank([
    ("What is impulse?", "force multiplied by the time it acts", ["mass times acceleration", "force divided by time", "speed times time"], "J = FΔt."),
    ("Impulse equals the change in what?", "momentum", ["mass", "energy", "speed only"], "J = Δp."),
    ("Why is landing on a soft mat safer than on a hard floor?", "The stop takes longer, so the force is smaller.", ["The change in momentum is zero.", "The mat adds momentum.", "The floor is lighter."], "F = Δp ÷ Δt."),
    ("If the stopping time doubles and Δp stays the same, what happens to the force?", "It is cut in half.", ["It doubles.", "It stays the same.", "It becomes four times larger."], "Inverse relationship."),
    ("What are the units of impulse?", "N·s (same as kg·m/s)", ["N", "J", "W"], "Force × time."),
    ("Why do cars have crumple zones instead of rigid fronts?", "Crushing metal lengthens the collision time and absorbs energy.", ["Rigid fronts are too expensive.", "To make the car lighter.", "To make the car faster."], "Engineering for safety."),
    ("Does an air bag change the passenger's change in momentum?", "No. It changes the time, which lowers the force.", ["Yes, it makes it zero.", "Yes, it doubles it.", "It adds momentum."], "Same Δp."),
    ("A boxer moves his head back when punched. Why?", "It increases the time of contact and lowers the force.", ["It increases the force.", "It adds mass.", "It stops the punch completely."], "Riding the punch."),
])
B5 = bank([
    ("An engineer has two helmet foams: A stops a head in 0.006 s, B in 0.012 s. Both cost the same and weigh the same. Which is better?", "B, because the longer stop halves the force.",
     ["A, because it stops faster.", "Both are equal.", "Neither works."], "Use the criterion: lower force."),
    ("Which criterion matters most for a phone case?", "it lengthens the impact time when the phone hits the floor", ["it makes the phone heavier", "it is bright colored", "it is very hard and rigid"], "Design criteria."),
    ("Why are seat belts made of slightly stretchy webbing?", "Stretching increases the stopping time of the passenger.", ["To make them cheaper.", "To let the passenger fly forward.", "To add momentum."], "Gradual stop."),
    ("A design team tests a bumper and finds it reduces force but breaks after one hit. What should they do next?", "refine the design and test again against the criteria", ["give up", "make it rigid", "test it only once more without changes"], "Iterate."),
    ("Why does a falling cat land more safely when it lands on its feet and bends its legs?", "Bending spreads the stop over a longer time.", ["Cats have no momentum.", "Legs remove gravity.", "It stops faster."], "Impulse."),
])


def body():
    think = ("<p><b>Same change in momentum over a longer time means a smaller force.</b></p>"
             "<ul><li>Impulse J = FΔt = Δp. To stop an object, Δp = mv.</li>"
             "<li>Safety devices (air bags, helmets, crumple zones, mats) make Δt longer, so F = Δp ÷ Δt is smaller.</li>"
             "<li>Bouncing reverses momentum, so Δp (and the force) is larger than for stopping.</li></ul>")
    ex = [("60 kg at 10 m/s stops in 0.5 s. Force?", ["Δp = 600", "600 ÷ 0.5"], "1,200 N"),
          ("Stop takes 4 times longer. Force?", ["F = Δp ÷ Δt"], "1/4 as large")]
    mist = ["Thinking air bags reduce the change in momentum.", "Thinking a harder surface is safer.", "Thinking bouncing has a smaller change in momentum."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Impulse", B1 + [(g_imp, 12)]),
        ("Force and stopping time", [(g_imp, 10), (g_ratio, 10)]),
        ("Bouncing and stopping", [(g_bounce, 10), (g_dev, 10)]),
        ("Testing designs", [(g_test, 14), (g_ratio, 6)]),
        ("Designing safer collisions", B5 + [(g_dev, 4), (g_test, 6), (g_imp, 5)]),
    ])
    make("physics", "impulse-and-collision-safety", 4, "HS-PS2-3",
         "Apply scientific and engineering ideas to design, evaluate, and refine a device that minimizes the force on a macroscopic object during a collision.",
         "Impulse and Collision Safety",
         "Impulse Worksheets: FΔt = Δp, Air Bags, Helmets and Egg Drops (High School Physics)",
         "Impulse",
         "Free high school physics worksheets on impulse and collision safety (NGSS HS-PS2-3): FΔt = Δp, stopping time, bouncing and designing air bags, helmets and egg drops. 100 questions with answers.",
         "Longer stop, smaller force.",
         "Impulse FΔt = Δp: safety devices spread the stop over more time.",
         body(),
         [("What is impulse?", "Impulse is force times the time it acts (FΔt). It equals the change in momentum."),
          ("How do air bags and helmets protect people?", "They increase the time it takes to stop. With the same change in momentum, a longer time means a smaller force."),
          ("Why does bouncing cause a larger force?", "When an object bounces back, its momentum reverses, so the change in momentum is larger than if it just stopped.")],
         sets)


if __name__ == "__main__":
    main()
