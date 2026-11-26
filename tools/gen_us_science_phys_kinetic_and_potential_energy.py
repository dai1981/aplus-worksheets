# -*- coding: utf-8 -*-
"""
US High School Physics: Kinetic and Potential Energy (HS-PS3-2)
  python tools/gen_us_science_phys_kinetic_and_potential_energy.py
Develop and use models to illustrate that energy at the macroscopic scale can be accounted for as a combination of
energy associated with the motions of particles (objects) and energy associated with the relative position of
particles (objects).
Kinetic energy ½mv², gravitational potential energy mgh, elastic potential energy ½kx², work W = Fd, power P = W/t,
and how changes in speed, mass and height change energy.
Wrong answers come from real mistakes: "double the speed doubles the kinetic energy", "forget the ½", "potential
energy depends on speed", "work is done holding a box still".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, uniq, safe

U = Unit(90308)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_ke():
    o, m = R.choice([("2 kg ball", 2), ("60 kg runner", 60), ("1,000 kg car", 1000), ("0.5 kg ball", 0.5), ("80 kg cyclist", 80), ("4 kg bowling ball", 4), ("0.2 kg puck", 0.2)])
    v = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    if o.startswith("60") or o.startswith("80"):
        v = R.choice([2, 3, 4, 5, 6, 8])
    k = R.choice(["ke", "ke", "v"])
    E = 0.5 * m * v * v
    if not once(("ke", o, v, k)):
        return None
    if k == "ke":
        g = "%s J" % num(E)
        return item("What is the kinetic energy of a %s moving at %d m/s?" % (o, v), g, uniq(g, ["%s J" % num(m * v * v), "%s J" % num(0.5 * m * v), "%s J" % num(m * v), "%s J" % num(E * 2)]),
                    "KE = ½mv² = ½ × %s × %d² = %s J." % (num(m), v, num(E)))
    g = "%d m/s" % v
    return item("A %s has %s J of kinetic energy. How fast is the %s moving?" % (o, num(E), o.split(" ", 2)[-1]), g, uniq(g, ["%s m/s" % num(2 * E / m), "%s m/s" % num(E / m), "%d m/s" % (v * 2), "%s m/s" % num((E / m) ** 0.5, 1)]),
                "v = √(2KE ÷ m) = √(2 × %s ÷ %s) = %d m/s." % (num(E), num(m), v))


@safe
def g_pe():
    m = R.choice([0.5, 1, 2, 5, 10, 20, 50, 60, 70])
    h = R.choice([1, 2, 3, 5, 10, 15, 20, 25, 30, 50])
    k = R.choice(["pe", "pe", "h"])
    E = m * 9.8 * h
    if not once(("pe", m, h, k)):
        return None
    if k == "pe":
        g = "%s J" % num(E, 1)
        return item("A %s kg object is lifted %d m. How much gravitational potential energy does it gain? (g = 9.8 m/s²)" % (num(m), h), g,
                    uniq(g, ["%s J" % num(m * h), "%s J" % num(0.5 * m * 9.8 * h, 1), "%s J" % num(m * 9.8, 1), "%s J" % num(E * 2, 1)]), "PE = mgh = %s × 9.8 × %d = %s J." % (num(m), h, num(E, 1)))
    g = "%d m" % h
    return item("A %s kg box on a shelf has %s J of gravitational potential energy. How high is the shelf? (g = 9.8 m/s²)" % (num(m), num(E, 1)), g,
                uniq(g, ["%s m" % num(E / m, 1), "%s m" % num(E * 9.8 * m, 1), "%d m" % (h * 2), "%s m" % num(E / 9.8, 1)]), "h = PE ÷ (mg) = %s ÷ (%s × 9.8) = %d m." % (num(E, 1), num(m), h))


@safe
def g_factor():
    k = R.choice(["v", "m", "h"])
    f = R.choice([2, 3, 4, 0.5])
    if not once(("fc", k, f)):
        return None
    word = {2: "doubled", 3: "tripled", 4: "made 4 times larger", 0.5: "halved"}[f]
    if k == "v":
        r = f * f
        g = "%s times as much" % num(r) if r >= 1 else "1/4 as much"
        w = ["%s times as much" % num(f) if f >= 1 else "1/2 as much", "the same", "%s times as much" % num(r * 2) if r >= 1 else "1/8 as much", "%s times as much" % num(f * 3) if f >= 1 else "2 times as much"]
        return item("A car's speed is %s. How does its kinetic energy change?" % word, g, uniq(g, w), "KE depends on v²: %s² = %s." % (num(f), num(r)))
    what = "mass" if k == "m" else "height"
    kind = "kinetic" if k == "m" and R.random() < 0.5 else "gravitational potential" if k == "h" else "kinetic"
    g = "%s times as much" % num(f) if f >= 1 else "1/2 as much"
    w = ["%s times as much" % num(f * f) if f >= 1 else "1/4 as much", "the same", "%s times as much" % num(f + 1) if f >= 1 else "2 times as much"]
    return item("An object's %s is %s and nothing else changes. How does its %s energy change?" % (what, word, kind), g, uniq(g, w), "The energy is proportional to %s." % what)


@safe
def g_work():
    who = P.next()[0]
    F = R.choice([10, 20, 25, 40, 50, 60, 80, 100, 150, 200])
    d = R.choice([2, 3, 4, 5, 8, 10, 12, 15, 20])
    t = R.choice([2, 4, 5, 8, 10, 20])
    k = R.choice(["w", "w", "p"])
    W = F * d
    if not once(("wk", F, d, t, k)):
        return None
    if k == "w":
        g = "%s J" % num(W)
        return item("%s pushes a crate with a force of %d N for %d m in the direction of the push. How much work is done?" % (who, F, d), g, uniq(g, ["%s J" % num(F / d, 2), "%s J" % num(F + d), "%s J" % num(W / 2), "%s J" % num(W * 9.8, 1)]),
                    "W = Fd = %d × %d = %s J." % (F, d, num(W)))
    P_ = W / t
    g = "%s W" % num(P_)
    return item("%s does %s J of work lifting boxes in %d s. What is the power?" % (who, num(W), t), g, uniq(g, ["%s W" % num(W * t), "%s W" % num(t / W, 3), "%s W" % num(W), "%s W" % num(P_ * 2)]),
                "P = W ÷ t = %s ÷ %d = %s W." % (num(W), t, num(P_)))


@safe
def g_spring():
    kk = R.choice([50, 100, 200, 250, 400, 500, 800, 1000])
    x = R.choice([0.05, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5])
    E = 0.5 * kk * x * x
    if E != round(E, 3) or not once(("sp", kk, x)):
        return None
    g = "%s J" % num(E, 3)
    return item("A spring with k = %d N/m is stretched %s m. How much elastic potential energy does it store? (PE = ½kx²)" % (kk, num(x)), g,
                uniq(g, ["%s J" % num(kk * x * x, 3), "%s J" % num(0.5 * kk * x, 3), "%s J" % num(kk * x, 3), "%s J" % num(E * 4, 3)]), "½ × %d × %s² = %s J." % (kk, num(x), num(E, 3)))


B1 = bank([
    ("What is kinetic energy?", "energy of motion", ["energy stored by position", "energy of heat only", "energy in food only"], "KE = ½mv²."),
    ("What is gravitational potential energy?", "energy stored because of an object's height in a gravitational field", ["energy of motion", "energy of sound", "energy from chemical bonds only"], "PE = mgh."),
    ("What is the SI unit of energy?", "the joule (J)", ["the watt (W)", "the newton (N)", "the volt (V)"], "1 J = 1 N·m."),
    ("At the particle level, what is thermal energy?", "the kinetic energy of the random motion of particles", ["the mass of the particles", "the potential energy from height", "a type of light"], "Macroscopic vs microscopic."),
    ("A stretched rubber band stores what kind of energy?", "elastic potential energy", ["kinetic energy", "nuclear energy", "sound energy"], "Energy of relative position of particles."),
    ("When you hold a heavy box still, how much work do you do on it?", "none, because it does not move", ["a lot, because it is heavy", "equal to its weight", "equal to its mass"], "W = Fd and d = 0."),
    ("What is power?", "the rate at which work is done or energy is transferred", ["the total energy", "the force on an object", "the speed of an object"], "P = W ÷ t."),
    ("Chemical energy in food is stored in what?", "the arrangement of atoms in molecules (a form of potential energy)", ["the motion of the food", "the color of the food", "the mass only"], "Position of particles in fields."),
])
B5 = bank([
    ("Why does doubling a car's speed make crashes much more dangerous?", "Kinetic energy becomes 4 times larger.", ["Kinetic energy doubles.", "Mass doubles.", "Momentum becomes 4 times larger."], "KE ∝ v²."),
    ("A bow is drawn back further. Why does the arrow fly faster?", "More elastic potential energy is stored and turned into kinetic energy.", ["The arrow gets heavier.", "Gravity is stronger.", "The bow loses mass."], "Energy transfer."),
    ("Two students climb the same stairs. One runs, one walks. Who does more work if they have the same weight?", "They do the same work; the runner has more power.", ["The runner does more work.", "The walker does more work.", "Neither does work."], "Work vs power."),
    ("Water behind a dam stores energy. What kind?", "gravitational potential energy", ["kinetic energy", "sound energy", "nuclear energy"], "Height."),
    ("A model of a gas shows faster-moving particles when it is heated. What does this represent?", "an increase in thermal (kinetic) energy of the particles", ["a decrease in energy", "particles getting larger", "the gas becoming a solid"], "Particle model."),
])


def body():
    think = ("<p><b>Energy is either motion (kinetic) or stored by position (potential).</b></p>"
             "<ul><li>KE = ½mv² (double the speed → 4 times the KE). Gravitational PE = mgh. Elastic PE = ½kx².</li>"
             "<li>Work W = Fd transfers energy; power P = W ÷ t.</li>"
             "<li>At the particle level, thermal energy is particle motion; chemical energy is stored in particle positions.</li></ul>")
    ex = [("KE of 2 kg at 3 m/s?", ["½ × 2 × 3²"], "9 J"),
          ("PE of 10 kg lifted 2 m?", ["10 × 9.8 × 2"], "196 J")]
    mist = ["Thinking doubling speed doubles kinetic energy.", "Forgetting the ½ in ½mv².", "Thinking work is done when nothing moves."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Forms of energy", B1 + [(g_ke, 6), (g_pe, 6)]),
        ("Kinetic energy", [(g_ke, 14), (g_factor, 6)]),
        ("Potential energy", [(g_pe, 12), (g_spring, 8)]),
        ("Work and power", [(g_work, 16), (g_factor, 4)]),
        ("Energy models", B5 + [(g_ke, 4), (g_pe, 4), (g_work, 4), (g_spring, 3)]),
    ])
    make("physics", "kinetic-and-potential-energy", 8, "HS-PS3-2",
         "Develop and use models to illustrate that energy at the macroscopic scale can be accounted for as a combination of energy associated with the motions of particles (objects) and energy associated with the relative position of particles (objects).",
         "Kinetic and Potential Energy",
         "Kinetic and Potential Energy Worksheets: ½mv², mgh, Work and Power (High School Physics)",
         "Kinetic and Potential Energy",
         "Free high school physics worksheets on kinetic and potential energy (NGSS HS-PS3-2): KE = ½mv², PE = mgh, elastic energy, work and power. 100 questions with answers.",
         "Energy is motion or position.",
         "KE = ½mv², PE = mgh; work moves energy from one form or object to another.",
         body(),
         [("How do you calculate kinetic energy?", "KE = ½mv². Because speed is squared, doubling the speed makes the kinetic energy four times larger."),
          ("How do you calculate gravitational potential energy?", "PE = mgh: mass × 9.8 m/s² × height."),
          ("What is the difference between work and power?", "Work is energy transferred by a force (W = Fd). Power is how fast the work is done (P = W ÷ t).")],
         sets)


if __name__ == "__main__":
    main()
