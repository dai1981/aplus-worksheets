# -*- coding: utf-8 -*-
"""Class 9 Science, Unit III Motion, Force and Work: NCERT chapters 7–11 (question makers). g = 9.8 m/s² unless the question says 10."""
from fractions import Fraction as F
from uk_alsci import nf, nq, tq, once_maker
from in_sci import name, _R, U, K

MI = "−"


def ch(xs):
    return _R[0].choice(xs)


def sg(x):
    return (MI if x < 0 else "") + nf(abs(x))


# =================================================================== Chapter 7: motion
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (30, 40, 50), (60, 80, 100), (15, 20, 25), (20, 21, 29)]


def c_mot(k=None):
    R = _R[0]
    k = k or ch(["speed", "conv", "avg2", "disp", "acc", "eq1", "eq2", "eq3", "circ"])
    nm = name()
    if k == "speed":
        v, t = R.choice([30, 40, 45, 50, 60, 72, 80]), R.choice([2, 3, 4, 5, 1.5, 2.5])
        d = v * t
        veh = ch(["a bus", "a car", "a train", "a truck"])
        return nq("%s from Delhi covers %s km in %s hours. What is its average speed?" % (veh[0].upper() + veh[1:], nf(d), nf(t)), v, [d * t, t / d * 1000, d / (t + 1)], " km/h",
                  "Average speed = total distance ÷ total time = %s ÷ %s = <b>%s km/h</b>." % (nf(d), nf(t), nf(v)))
    if k == "conv":
        kmh = R.choice([18, 36, 54, 72, 90, 108, 126, 144, 180])
        ms = kmh * 5 // 18
        if R.random() < 0.5:
            return nq("Convert %d km/h into m/s." % kmh, ms, [kmh * 18 / 5, kmh * 1000, kmh / 60], " m/s", "Multiply by 5/18: %d × 5 ÷ 18 = <b>%d m/s</b>." % (kmh, ms))
        return nq("Convert %d m/s into km/h." % ms, kmh, [ms * 5 / 18, ms * 60, ms * 3600], " km/h", "Multiply by 18/5: %d × 18 ÷ 5 = <b>%d km/h</b>." % (ms, kmh))
    if k == "avg2":
        v1, v2 = R.sample([20, 30, 40, 60, 80, 120], 2)
        d = R.choice([60, 120, 240])
        if d % v1 or d % v2:
            return None
        avg = F(2 * d, F(d, v1) + F(d, v2))
        return nq("%s drives %d km from home to a city at %d km/h and returns the same way at %d km/h. What is the average speed for the whole trip?" % (nm, d, v1, v2), float(avg), [(v1 + v2) / 2, abs(v1 - v2), v1 + v2], " km/h",
                  "Time = %s h + %s h = %s h; average speed = %d ÷ %s = <b>%s km/h</b> (not the mean of the speeds)." % (nf(d / v1), nf(d / v2), nf(d / v1 + d / v2), 2 * d, nf(d / v1 + d / v2), nf(float(avg))))
    if k == "disp":
        a, b, c = ch(TRIPLES)
        if R.random() < 0.5:
            return nq("%s walks %d m east and then %d m north. What is the magnitude of the displacement?" % (nm, a, b), c, [a + b, abs(b - a), (a + b) / 2], " m",
                      "Displacement is the straight line from start to finish: √(%d² + %d²) = <b>%d m</b>; the distance walked is %d m." % (a, b, c, a + b))
        L = R.choice([100, 200, 300, 400])
        n = R.choice([1, 2, 3])
        return nq("An athlete runs %d complete round%s of a circular track of length %d m and stops at the starting point. What is the displacement?" % (n, "" if n == 1 else "s", L), 0, [n * L, L, n * L / 2], " m",
                  "The athlete ends where she started, so the displacement is <b>0 m</b>; the distance is %s m." % nf(n * L))
    if k == "acc":
        u, v, t = R.choice([0, 5, 10, 15, 20]), R.choice([10, 20, 25, 30, 40, 0]), R.choice([2, 4, 5, 8, 10])
        if u == v:
            return None
        a = (v - u) / t
        thing = "A car" if v > u else "A train braking"
        return nq("%s changes its velocity from %d m/s to %d m/s in %d s. What is its acceleration?" % (thing, u, v, t), a, [(u - v) / t, v / t, (v - u) * t, (u + v) / t], " m/s²",
                  "a = (v − u) ÷ t = (%d − %d) ÷ %d = <b>%s m/s²</b>%s." % (v, u, t, sg(a), " (a retardation)" if a < 0 else ""))
    if k == "eq1":
        u, a, t = R.choice([0, 2, 5, 10]), R.choice([1, 2, 3, 4, 0.5, 1.5]), R.choice([4, 5, 8, 10, 12])
        v = u + a * t
        return nq("A scooter starts with a velocity of %d m/s and accelerates at %s m/s² for %d s. What is its final velocity?" % (u, nf(a), t), v, [a * t, u * a * t if u else v + u + 5, u + a, u + a * t * t], " m/s",
                  "v = u + at = %d + %s × %d = <b>%s m/s</b>." % (u, nf(a), t, nf(v)))
    if k == "eq2":
        u, a, t = R.choice([0, 2, 4, 5]), R.choice([1, 2, 3, 4]), R.choice([2, 4, 5, 6, 10])
        s = u * t + a * t * t / 2
        return nq("A trolley starts at %d m/s and accelerates uniformly at %d m/s² for %d s. How far does it travel?" % (u, a, t), s, [u * t + a * t * t, u * t + a * t / 2, a * t * t / 2 + u, (u + a * t) * t], " m",
                  "s = ut + ½at² = %d × %d + ½ × %d × %d² = <b>%s m</b>." % (u, t, a, t, nf(s)))
    u, a = R.choice([10, 12, 15, 20, 25, 30]), R.choice([2, 3, 4, 5, 6])
    if k == "eq3":
        s = u * u / (2 * a)
        return nq("A car moving at %d m/s brakes with a uniform retardation of %d m/s². How far does it travel before it stops?" % (u, a), s, [u * u / a, u / a, u * a / 2, u * u * a / 2], " m",
                  "v² − u² = 2as: 0 − %d² = 2 × (−%d) × s, so s = <b>%s m</b>." % (u, a, nf(s)))
    r, t = R.choice([7, 14, 21, 35, 42, 70]), R.choice([2, 4, 5, 10, 11, 22])
    v = 2 * F(22, 7) * r / t
    return nq("A stone tied to a thread moves in a circle of radius %d m and makes one round in %d s. What is its speed? (π = 22/7)" % (r, t), float(v), [float(F(22, 7) * r / t), float(2 * F(22, 7) * r * t), float(F(22, 7) * r * r / t)], " m/s",
              "v = 2πr ÷ t = 2 × 22/7 × %d ÷ %d = <b>%s m/s</b>." % (r, t, nf(float(v))))


MOT = [("Which is a vector quantity?", "displacement", ["distance", "speed", "time"], "It has both size and direction."),
       ("Can the displacement of an object be zero while the distance is not?", "yes, when it returns to its starting point", ["no, never", "only if it stops", "only on a straight road"], "A full lap of a track has zero displacement."),
       ("What does the slope of a distance–time graph give?", "the speed", ["the acceleration", "the distance", "the time"], "A steeper line means a faster object."),
       ("What does the slope of a velocity–time graph give?", "the acceleration", ["the speed", "the distance", "the displacement"], "A horizontal line means zero acceleration."),
       ("What does the area under a velocity–time graph give?", "the displacement (distance travelled)", ["the acceleration", "the speed", "the force"], "For a rectangle it is velocity × time."),
       ("What does a straight horizontal line on a distance–time graph show?", "the object is at rest", ["the object moves fast", "the object accelerates", "the object moves backwards"], "The distance is not changing."),
       ("What does a straight line sloping upwards on a distance–time graph show?", "uniform motion", ["the object is at rest", "non-uniform motion", "the object is slowing down"], "Equal distances are covered in equal times."),
       ("What is uniform motion?", "covering equal distances in equal intervals of time", ["moving in a circle", "speeding up steadily", "any kind of motion"], "Its distance–time graph is a straight line."),
       ("Why is uniform circular motion accelerated?", "the direction of motion keeps changing", ["the speed keeps increasing", "there is no force", "the distance is constant"], "Velocity includes direction."),
       ("What does the odometer of a car measure?", "the distance travelled", ["the speed", "the acceleration", "the displacement"], "The speedometer shows the instantaneous speed."),
       ("What is the SI unit of acceleration?", "m/s²", ["m/s", "m", "N"], "It is the change in velocity per second."),
       ("What is negative acceleration called?", "retardation (deceleration)", ["uniform motion", "displacement", "velocity"], "The object slows down."),
       ("An object moves in a straight line with a constant velocity. What is its acceleration?", "zero", ["positive", "negative", "9.8 m/s²"], "Velocity is not changing."),
       ("Which can be negative: distance or displacement?", "displacement", ["distance", "both", "neither"], "Distance is never negative."),
       ("What is velocity?", "speed in a given direction", ["distance travelled in total", "rate of change of acceleration", "time taken"], "Its unit is m/s."),
       ("When are average speed and the magnitude of average velocity equal?", "when the object moves in a straight line without turning back", ["always", "never", "only when at rest"], "Turning back makes displacement smaller than distance."),
       ("A car's speedometer shows a steady reading but the car goes round a bend. Is it accelerating?", "yes, because its direction is changing", ["no, the speed is constant", "only if it brakes", "only uphill"], "Velocity changes when direction changes."),
       ("What is the motion of the Moon around the Earth called?", "nearly uniform circular motion", ["uniform linear motion", "rest", "random motion"], "Its speed is almost constant but its direction changes."),
       ("What kind of graph line shows uniform acceleration on a velocity–time graph?", "a straight line sloping upwards", ["a horizontal line", "a curve", "a vertical line"], "The slope is constant."),
       ("Which equation links v, u, a and s?", "v² − u² = 2as", ["v = u + at", "s = ut + ½at²", "s = vt"], "It does not need time."),
       ("Why do we need a reference point to describe motion?", "position and motion are always measured relative to something", ["motion is the same everywhere", "objects at rest move", "time stops otherwise"], "A passenger is at rest relative to the bus but moving relative to the road."),
       ("A ball thrown upwards returns to the thrower's hand. What is its displacement?", "zero", ["twice the height", "the height", "it cannot be found"], "It ends where it started.")]


# =================================================================== Chapter 8: force and laws of motion
def c_force(k=None):
    R = _R[0]
    k = k or ch(["F", "a", "m", "p", "dp", "recoil", "stick", "stop"])
    nm = name()
    if k in ("F", "a", "m"):
        m, a = R.choice([2, 5, 10, 20, 50, 100, 500, 1000, 1200, 1500]), R.choice([0.2, 0.5, 1, 2, 3, 4, 5])
        f = m * a
        if k == "F":
            return nq("What force is needed to give a mass of %s kg an acceleration of %s m/s²?" % (nf(m), nf(a)), f, [m / a, a / m, m + a], " N", "F = ma = %s × %s = <b>%s N</b>." % (nf(m), nf(a), nf(f)))
        if k == "a":
            return nq("A force of %s N acts on a body of mass %s kg. What is its acceleration?" % (nf(f), nf(m)), a, [f * m, m / f, f - m], " m/s²", "a = F ÷ m = %s ÷ %s = <b>%s m/s²</b>." % (nf(f), nf(m), nf(a)))
        return nq("A force of %s N gives a body an acceleration of %s m/s². What is its mass?" % (nf(f), nf(a)), m, [f * a, a / f, f + a], " kg", "m = F ÷ a = %s ÷ %s = <b>%s kg</b>." % (nf(f), nf(a), nf(m)))
    if k == "p":
        g, v = R.choice([50, 100, 150, 200, 500, 800]), R.choice([5, 10, 20, 25, 30, 40])
        p = g / 1000 * v
        thing = ch(["a cricket ball", "a hockey ball", "a stone", "a toy car"])
        return nq("What is the momentum of %s of mass %d g moving at %d m/s?" % (thing, g, v), p, [g * v, g / v, v / g * 1000], " kg m/s",
                  "Change grams to kilograms: %s kg; p = mv = %s × %d = <b>%s kg m/s</b>." % (nf(g / 1000), nf(g / 1000), v, nf(p)))
    if k == "dp":
        g, v, t = R.choice([100, 150, 200]), R.choice([10, 20, 30]), R.choice([0.05, 0.1, 0.2, 0.5])
        f = g / 1000 * v / t
        return nq("A fielder catches a ball of mass %d g moving at %d m/s and stops it in %s s. What average force does the ball exert on the hands?" % (g, v, nf(t)), f, [g * v / t, g / 1000 * v * t, g / 1000 * v], " N",
                  "F = change of momentum ÷ time = %s × %d ÷ %s = <b>%s N</b>. Pulling the hands back makes t longer and F smaller." % (nf(g / 1000), v, nf(t), nf(f)))
    if k == "recoil":
        m, M, v = R.choice([10, 20, 25, 50]), R.choice([2, 2.5, 4, 5]), R.choice([100, 150, 200, 250, 400])
        rv = m / 1000 * v / M
        return nq("A bullet of mass %d g is fired from a gun of mass %s kg with a velocity of %d m/s. What is the recoil speed of the gun?" % (m, nf(M), v), rv, [m * v / M, M * v / m, v / M], " m/s",
                  "Momentum is conserved: %s × %d = %s × V, so V = <b>%s m/s</b> backwards." % (nf(m / 1000), v, nf(M), nf(rv)))
    if k == "stick":
        m1, m2, u1 = R.choice([1, 1.5, 2, 3, 5]), R.choice([1, 2, 3, 4, 5]), R.choice([2, 4, 6, 10, 12])
        v = m1 * u1 / (m1 + m2)
        return nq("A trolley of mass %s kg moving at %d m/s hits a stationary trolley of mass %s kg. They stick together. What is their common velocity?" % (nf(m1), u1, nf(m2)), v, [u1 / 2, m1 * u1 / m2, m2 * u1 / (m1 + m2)], " m/s",
                  "Total momentum before = %s × %d = %s kg m/s; v = %s ÷ %s = <b>%s m/s</b>." % (nf(m1), u1, nf(m1 * u1), nf(m1 * u1), nf(m1 + m2), nf(v)))
    m, u, t = R.choice([800, 1000, 1200, 1500]), R.choice([10, 15, 20, 25]), R.choice([2, 4, 5, 10])
    f = m * u / t
    return nq("A car of mass %s kg moving at %d m/s is brought to rest in %d s by the brakes. What is the braking force?" % (nf(m), u, t), f, [m * u * t, m * u, m * t / u], " N",
              "F = m(v − u) ÷ t = %s × (0 − %d) ÷ %d = %s N, so the braking force is <b>%s N</b>." % (nf(m), u, t, sg(-f), nf(f)))


FORCE = [("What is inertia?", "the tendency of an object to resist a change in its state of rest or motion", ["the force of gravity", "the speed of an object", "the friction on a surface"], "Mass is a measure of inertia."),
         ("Which has more inertia?", "a stone of mass 5 kg", ["a rubber ball of the same size", "a cricket ball", "a feather"], "More mass means more inertia."),
         ("Why do passengers fall forward when a bus stops suddenly?", "their bodies tend to keep moving because of inertia", ["the bus pushes them", "gravity pulls them forward", "the air pushes them"], "The lower body stops with the bus."),
         ("Why are seat belts used in cars?", "to stop passengers moving forward violently when the car stops suddenly", ["to make the car faster", "to reduce friction", "to increase inertia"], "They also spread the force over a longer time."),
         ("What does Newton's first law state?", "an object stays at rest or in uniform motion unless an unbalanced force acts on it", ["F = ma", "every action has an equal and opposite reaction", "momentum is always zero"], "It is also called the law of inertia."),
         ("What does Newton's second law state?", "the rate of change of momentum is proportional to the applied force, in its direction", ["objects stay at rest", "action equals reaction", "force is mass ÷ acceleration"], "This gives F = ma."),
         ("What does Newton's third law state?", "to every action there is an equal and opposite reaction", ["F = ma", "objects resist change", "momentum is lost in collisions"], "The forces act on different objects."),
         ("Why do action and reaction forces not cancel each other?", "they act on different bodies", ["they are unequal", "they act in the same direction", "they act at different times"], "Only forces on the same body can balance."),
         ("What is 1 newton?", "the force that gives a mass of 1 kg an acceleration of 1 m/s²", ["the weight of 1 kg", "the momentum of 1 kg", "1 kg × 1 m/s"], "1 N = 1 kg m/s²."),
         ("What is the SI unit of momentum?", "kg m/s", ["N", "kg m/s²", "J"], "p = mv."),
         ("When the net force on an object is zero, what are the forces called?", "balanced forces", ["unbalanced forces", "frictional forces", "action forces"], "The motion does not change."),
         ("Why does a fielder pull his hands back while catching a fast ball?", "to increase the time of impact and reduce the force on his hands", ["to increase the force", "to throw it faster", "to reduce the ball's mass"], "F = change in momentum ÷ time."),
         ("Why do high jumpers land on cushions or sand?", "to increase the time taken to stop and reduce the force", ["to bounce higher", "to reduce their mass", "to increase friction"], "The momentum change is the same, but the time is longer."),
         ("How does a rocket move upwards?", "hot gases pushed out backwards push the rocket forward (third law)", ["air pulls it up", "gravity pushes it up", "it has no mass"], "It works even in empty space."),
         ("When a gun is fired, why does it recoil?", "the bullet pushes back on the gun with an equal and opposite force", ["the gun is heavier", "air pushes the gun", "gravity acts on the gun"], "Momentum is conserved."),
         ("What is the law of conservation of momentum?", "the total momentum of a system stays the same if no external force acts", ["momentum is always lost", "momentum depends only on speed", "force is always conserved"], "It follows from Newton's third law."),
         ("Why does dust fly out when a carpet is beaten with a stick?", "the carpet moves but the dust tends to stay at rest due to inertia", ["the stick pulls the dust", "the dust is magnetic", "gravity pushes the dust out"], "This is inertia of rest."),
         ("Why do we stumble when a moving bus starts suddenly?", "the lower body moves with the bus while the upper body tends to stay at rest", ["the bus slows down", "the air pushes us forward", "our mass increases"], "We fall backwards."),
         ("Why is it easier to push an empty cart than a loaded one?", "the empty cart has less mass and less inertia", ["the empty cart has more friction", "the loaded cart has no inertia", "gravity is weaker"], "F = ma: the same force gives more acceleration."),
         ("What is friction?", "a force that opposes the motion of surfaces sliding against each other", ["a force that speeds things up", "the weight of an object", "the momentum of an object"], "It is why a rolling ball stops."),
         ("A truck and a bicycle move at the same speed. Which has more momentum?", "the truck", ["the bicycle", "both the same", "neither"], "It has much more mass."),
         ("A swimmer pushes water backwards. What makes her move forward?", "the water pushes her forward with an equal and opposite force", ["gravity", "her inertia", "the air above her"], "This is Newton's third law.")]


# =================================================================== Chapter 9: gravitation
G = 6.7e-11


def c_grav(k=None):
    R = _R[0]
    k = k or ch(["ratio", "weight", "moon", "fall", "up", "press", "dens", "float", "upthrust"])
    nm = name()
    if k == "ratio":
        fm, fr = R.choice([(1, 2), (1, 3), (2, 1), (2, 2), (4, 2), (3, 1), (1, F(1, 2)), (2, F(1, 2)), (1, 4)])
        Fv = R.choice([20, 36, 40, 60, 80, 100, 120])
        new = Fv * F(fm) / (F(fr) ** 2)
        if F(new).denominator > 4:
            return None
        txt = []
        if fm != 1:
            txt.append("the mass of one object is made %d times" % fm)
        if fr != 1:
            txt.append("the distance between them is %s" % ("doubled" if fr == 2 else "tripled" if fr == 3 else "made four times" if fr == 4 else "halved"))
        return nq("The gravitational force between two objects is %d N. What is the force if %s?" % (Fv, " and ".join(txt)), float(new), [float(Fv * F(fm) / F(fr)), float(Fv * F(fm) * F(fr) ** 2), float(Fv * F(fm) / F(fr) ** 3)], " N",
                  "F ∝ m₁m₂ ÷ d²: %d × %d ÷ (%s)² = <b>%s N</b>." % (Fv, fm, nf(float(fr)), nf(float(new))))
    if k == "weight":
        m = R.choice([2, 5, 8, 10, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80])
        return nq("What is the weight of an object of mass %d kg on the Earth? (g = 9.8 m/s²)" % m, m * 9.8, [m, m / 9.8, m * 9.8 / 6], " N", "W = mg = %d × 9.8 = <b>%s N</b>." % (m, nf(m * 9.8)))
    if k == "moon":
        W = R.choice([60, 120, 180, 300, 360, 480, 540, 600, 720, 900])
        if R.random() < 0.5:
            return nq("An object weighs %d N on the Earth. What is its weight on the Moon? (The Moon's gravity is one-sixth of the Earth's.)" % W, W / 6, [W, W * 6, W / 9.8], " N",
                      "W(Moon) = %d ÷ 6 = <b>%s N</b>. Its mass does not change." % (W, nf(W / 6)))
        m = R.choice([12, 30, 45, 60])
        return nq("An astronaut has a mass of %d kg on the Earth. What is the astronaut's mass on the Moon?" % m, m, [m / 6, m * 6, m * 9.8 / 6], " kg",
                  "Mass is the amount of matter, so it stays <b>%d kg</b>; only the weight becomes one-sixth." % m)
    if k == "fall":
        t = R.choice([1, 1.5, 2, 2.5, 3, 4, 5, 6])
        if R.random() < 0.5:
            return nq("A stone is dropped from the top of a tower and reaches the ground in %s s. How tall is the tower? (g = 9.8 m/s²)" % nf(t), 4.9 * t * t, [9.8 * t * t, 9.8 * t, 4.9 * t, 4.9 * t * t / 2], " m",
                      "h = ½gt² = ½ × 9.8 × %s² = <b>%s m</b>." % (nf(t), nf(4.9 * t * t)))
        return nq("A stone is dropped from a cliff. What is its speed after %s s? (g = 9.8 m/s²)" % nf(t), 9.8 * t, [4.9 * t * t, 9.8 / t, 9.8 * t * t, 4.9 * t], " m/s", "v = u + gt = 0 + 9.8 × %s = <b>%s m/s</b>." % (nf(t), nf(9.8 * t)))
    if k == "up":
        u = R.choice([4.9, 9.8, 14.7, 19.6, 24.5, 29.4, 34.3, 39.2, 49, 58.8])
        if R.random() < 0.5:
            return nq("A ball is thrown vertically upwards with a velocity of %s m/s. What maximum height does it reach? (g = 9.8 m/s²)" % nf(u), u * u / 19.6, [u * u / 9.8, u / 9.8, u * 9.8], " m",
                      "At the top v = 0: h = u² ÷ 2g = %s² ÷ 19.6 = <b>%s m</b>." % (nf(u), nf(u * u / 19.6)))
        return nq("A ball is thrown vertically upwards with a velocity of %s m/s. How long does it take to reach the highest point? (g = 9.8 m/s²)" % nf(u), u / 9.8, [u * 9.8, 2 * u / 9.8, u / 4.9 * 2], " s",
                  "t = u ÷ g = %s ÷ 9.8 = <b>%s s</b>; the total time up and down is twice this." % (nf(u), nf(u / 9.8)))
    if k == "press":
        if R.random() < 0.5:
            f, a = R.choice([50, 100, 200, 500, 600, 1000]), R.choice([0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 2])
            return nq("A force (thrust) of %d N acts on an area of %s m². What is the pressure?" % (f, nf(a)), f / a, [f * a, a / f, f / a / 100], " Pa", "P = thrust ÷ area = %d ÷ %s = <b>%s Pa</b>." % (f, nf(a), nf(f / a)))
        l, w, h = R.choice([(0.4, 0.25, 0.1), (0.5, 0.2, 0.1), (0.4, 0.2, 0.1), (0.5, 0.4, 0.2)])
        m = R.choice([5, 10, 20, 40])
        wt = m * 9.8
        small = w * h
        big = l * w
        hi = R.random() < 0.5
        A = small if hi else big
        return nq("A wooden block of mass %d kg measures %s m × %s m × %s m. What is the %s pressure it can exert when it rests on a table? (g = 9.8 m/s²)" % (m, nf(l), nf(w), nf(h), "greatest" if hi else "least"), wt / A,
                  [wt / (big if hi else small), m / A, wt * A], " Pa", "Thrust = %d × 9.8 = %s N; the %s face has area %s m², so P = <b>%s Pa</b>." % (m, nf(wt), "smallest" if hi else "largest", nf(A), nf(wt / A)))
    if k in ("dens", "float"):
        mat, d = ch([("iron", 7870), ("aluminium", 2700), ("wood (teak)", 650), ("ice", 920), ("cork", 240), ("copper", 8960), ("glass", 2500), ("plastic (polythene)", 940), ("brick", 1800), ("wax", 900)])
        V = R.choice([0.001, 0.002, 0.005, 0.01, 0.02])
        m = d * V
        if k == "dens":
            if R.random() < 0.5:
                return nq("A block of %s has a mass of %s kg and a volume of %s m³. What is its density?" % (mat, nf(m), nf(V)), d, [m * V, V / m, d / 1000], " kg/m³", "Density = mass ÷ volume = %s ÷ %s = <b>%s kg/m³</b>." % (nf(m), nf(V), nf(d)))
            return nq("The density of %s is %s kg/m³. What is its relative density? (density of water = 1,000 kg/m³)" % (mat, nf(d)), d / 1000, [d * 1000, 1000 / d, d / 100], "",
                      "Relative density = %s ÷ 1,000 = <b>%s</b> (it has no unit)." % (nf(d), nf(d / 1000)))
        fl = d < 1000
        return tq("A block of %s has a mass of %s kg and a volume of %s m³. Will it float or sink in water? (density of water = 1,000 kg/m³)" % (mat, nf(m), nf(V)),
                  "it floats" if fl else "it sinks", ["it sinks" if fl else "it floats", "it stays half way down, whatever its density", "it dissolves"],
                  "Its density is %s kg/m³, %s than water, so <b>%s</b>." % (nf(d), "less" if fl else "more", "it floats" if fl else "it sinks"))
    V, W = R.choice([100, 200, 250, 400, 500]), R.choice([5, 8, 10, 12, 20])
    up = V / 1000 * 9.8
    if up >= W:
        return None
    return nq("A stone of weight %d N and volume %d cm³ is fully immersed in water. What is its apparent weight? (density of water = 1 g/cm³, g = 9.8 m/s²)" % (W, V), W - up, [W, up, W + up], " N",
              "Water displaced = %d g = %s kg, so upthrust = %s × 9.8 = %s N; apparent weight = %d − %s = <b>%s N</b>." % (V, nf(V / 1000), nf(V / 1000), nf(up), W, nf(up), nf(W - up)))


GRAV = [("Who gave the universal law of gravitation?", "Isaac Newton", ["Galileo Galilei", "Albert Einstein", "Johannes Kepler"], "Every two objects attract each other."),
        ("What is the value of the universal gravitational constant G?", "6.7 × 10⁻¹¹ N m²/kg²", ["9.8 m/s²", "6.7 × 10¹¹ N m²/kg²", "1.6 m/s²"], "Its value is the same everywhere."),
        ("What is the acceleration due to gravity on the Earth's surface?", "about 9.8 m/s²", ["6.7 × 10⁻¹¹ m/s²", "1.6 m/s²", "98 m/s²"], "It is written as g."),
        ("Why does g change from the poles to the equator?", "the Earth's radius is larger at the equator, so g is smaller there", ["the Earth is hotter at the equator", "the Moon pulls harder there", "the air is thinner at the poles"], "g is greatest at the poles."),
        ("What is the difference between mass and weight?", "mass is the amount of matter and stays the same; weight is the force of gravity and can change", ["they are the same", "weight never changes", "mass is measured in newtons"], "Weight W = mg is in newtons."),
        ("If a feather and a coin are dropped in a vacuum, which reaches the ground first?", "both reach together", ["the coin", "the feather", "neither falls"], "In a vacuum there is no air resistance."),
        ("What keeps the Moon moving around the Earth?", "the gravitational force of the Earth", ["the Sun's light", "magnetism", "air pressure"], "It provides the centripetal force."),
        ("Why do the tides rise and fall?", "mainly because of the Moon's gravitational pull on the oceans", ["because of the wind", "because of the Earth's heat", "because of fish"], "The Sun also has a smaller effect."),
        ("What is thrust?", "the force acting on an object perpendicular to its surface", ["the force per unit area", "the weight per unit volume", "the speed of an object"], "Pressure = thrust ÷ area."),
        ("What is the SI unit of pressure?", "pascal (Pa)", ["newton (N)", "joule (J)", "kg/m³"], "1 Pa = 1 N/m²."),
        ("Why do school bags have wide straps?", "a wider area reduces the pressure on the shoulders", ["to make the bag lighter", "to increase the pressure", "to look nice"], "P = F ÷ A."),
        ("Why are the blades of knives sharp?", "a small area gives a large pressure, so they cut easily", ["sharp blades are lighter", "to reduce pressure", "to increase the area"], "Nails have pointed tips for the same reason."),
        ("Why do camels walk easily on sand?", "their broad foot pads spread the weight over a large area, reducing pressure", ["their hooves are sharp", "they are light", "sand is hard"], "Tractors have wide tyres for the same reason."),
        ("What is buoyant force (upthrust)?", "the upward force a liquid exerts on an object in it", ["the weight of the object", "the downward pull of gravity", "the pressure of the air"], "It is why things seem lighter in water."),
        ("What does Archimedes' principle state?", "an object in a fluid feels an upthrust equal to the weight of fluid it displaces", ["all objects float", "pressure is the same everywhere", "heavy objects never float"], "It is used to design ships."),
        ("Why does a ship made of iron float?", "its shape displaces a weight of water equal to its own weight", ["iron is lighter than water", "ships have no weight", "the sea pushes it up without displacing water"], "Its average density is less than water's."),
        ("Why does an iron nail sink in water but a cork floats?", "iron is denser than water, while cork is less dense", ["iron is heavier than the whole bucket of water", "cork is magnetic", "water pulls iron down"], "Density decides floating."),
        ("What is relative density?", "the density of a substance divided by the density of water", ["mass divided by volume", "weight divided by mass", "density times volume"], "It has no unit."),
        ("Where is the weight of an object greatest?", "at the poles", ["at the equator", "on the Moon", "in space"], "g is greatest at the poles."),
        ("What is free fall?", "falling under the force of gravity alone", ["falling with a parachute", "moving horizontally", "floating in water"], "All objects fall with the same acceleration g."),
        ("Why does a lactometer work?", "it floats at different depths in milk of different densities, showing purity", ["it measures temperature", "it measures mass", "it sinks in pure milk"], "A hydrometer measures the density of liquids."),
        ("If the distance between two objects is doubled, what happens to the gravitational force?", "it becomes one-fourth", ["it doubles", "it halves", "it becomes four times"], "F ∝ 1/d²."),
        ("Why does the Earth not move towards a falling apple?", "the Earth has a huge mass, so its acceleration is extremely small", ["the apple does not pull the Earth", "the Earth is fixed", "gravity only acts on small things"], "Both pull each other with equal force.")]


# =================================================================== Chapter 10: work and energy
def c_work(k=None):
    R = _R[0]
    k = k or ch(["W", "ke", "ke2", "pe", "power", "climb", "kwh", "kwhJ", "cons"])
    nm = name()
    if k == "W":
        f, s = R.choice([5, 10, 20, 25, 50, 100, 140]), R.choice([2, 4, 5, 8, 10, 20])
        return nq("A force of %d N moves an object %d m in the direction of the force. How much work is done?" % (f, s), f * s, [f / s, s / f, f + s], " J", "W = F × s = %d × %d = <b>%s J</b>." % (f, s, nf(f * s)))
    if k == "ke":
        m, v = R.choice([2, 4, 5, 10, 15, 20, 50]), R.choice([2, 3, 4, 5, 6, 10])
        e = m * v * v / 2
        return nq("What is the kinetic energy of an object of mass %d kg moving at %d m/s?" % (m, v), e, [m * v * v, m * v / 2, m * v], " J", "KE = ½mv² = ½ × %d × %d² = <b>%s J</b>." % (m, v, nf(e)))
    if k == "ke2":
        m, kmh = R.choice([1000, 1200, 1500, 800]), R.choice([36, 54, 72, 90, 108])
        v = kmh * 5 // 18
        e = m * v * v / 2
        return nq("A car of mass %s kg is moving at %d km/h. What is its kinetic energy?" % (nf(m), kmh), e, [m * kmh * kmh / 2, m * v * v, m * v / 2], " J",
                  "%d km/h = %d m/s; KE = ½ × %s × %d² = <b>%s J</b>." % (kmh, v, nf(m), v, nf(e)))
    if k == "pe":
        m, h = R.choice([2, 5, 10, 12, 20, 25, 40]), R.choice([2, 3, 5, 6, 8, 10, 15])
        return nq("An object of mass %d kg is raised to a height of %d m. What is its potential energy? (Take g = 10 m/s².)" % (m, h), m * 10 * h, [m * h, m * 10 / h, m * h / 10], " J",
                  "PE = mgh = %d × 10 × %d = <b>%s J</b>." % (m, h, nf(m * 10 * h)))
    if k == "power":
        W, t = R.choice([600, 1000, 1200, 3000, 4500, 6000]), R.choice([5, 10, 20, 30, 60])
        return nq("A motor does %s J of work in %d s. What is its power?" % (nf(W), t), W / t, [W * t, t / W, W / t / 1000], " W", "P = W ÷ t = %s ÷ %d = <b>%s W</b>." % (nf(W), t, nf(W / t)))
    if k == "climb":
        m, h, t = R.choice([40, 45, 50, 55, 60]), R.choice([3, 4, 5, 6, 8]), R.choice([4, 5, 6, 8, 10])
        P = m * 10 * h / t
        return nq("%s, of mass %d kg, runs up a staircase %d m high in %d s. What power is developed? (Take g = 10 m/s².)" % (nm, m, h, t), P, [m * h / t, m * 10 * h, m * 10 * h * t], " W",
                  "Work = mgh = %d × 10 × %d = %s J; power = %s ÷ %d = <b>%s W</b>." % (m, h, nf(m * 10 * h), nf(m * 10 * h), t, nf(P)))
    if k == "kwh":
        P, h, d = R.choice([60, 100, 200, 250, 400, 500, 1000, 1500]), R.choice([2, 4, 5, 6, 8, 10]), R.choice([10, 20, 30])
        e = P * h * d / 1000
        return nq("A %s W appliance is used for %d hours every day. How many units (kWh) of energy does it use in %d days?" % (nf(P), h, d), e, [P * h * d, P * h / 1000, e * 3.6e6], " kWh",
                  "%s W × %d h × %d = %s Wh = <b>%s kWh</b>." % (nf(P), h, d, nf(P * h * d), nf(e)))
    if k == "kwhJ":
        e = R.choice([0.5, 1, 2, 3, 5, 10, 25])
        return nq("How many joules are there in %s kWh?" % nf(e), e * 3.6e6, [e * 1000, e * 3600, e * 3.6e5], " J", "1 kWh = 3.6 × 10<sup>6</sup> J, so %s kWh = <b>%s J</b>." % (nf(e), nf(e * 3.6e6)))
    m, h = R.choice([1, 2, 4, 5, 10]), R.choice([5, 20, 45, 80])
    v = (20 * h) ** 0.5
    if R.random() < 0.5:
        return nq("A ball of mass %d kg is dropped from a height of %d m. What is its kinetic energy just before it hits the ground? (Take g = 10 m/s², ignore air resistance.)" % (m, h), m * 10 * h, [m * h, m * 10 * h / 2, 0], " J",
                  "All the PE (mgh = %d × 10 × %d) becomes KE: <b>%s J</b>." % (m, h, nf(m * 10 * h)))
    return nq("A ball is dropped from a height of %d m. What is its speed just before it hits the ground? (Take g = 10 m/s², ignore air resistance.)" % h, v, [20 * h, 10 * h, v / 2], " m/s",
              "mgh = ½mv², so v = √(2gh) = √(2 × 10 × %d) = <b>%s m/s</b>." % (h, nf(v)))


WORK = [("When is work said to be done?", "when a force moves an object in the direction of the force", ["whenever we feel tired", "when a force acts but nothing moves", "when an object is at rest"], "No displacement means no work."),
        ("A man pushes hard against a wall that does not move. How much work does he do on the wall?", "zero", ["a lot", "it depends on his mass", "negative work"], "The wall has no displacement."),
        ("When is the work done by a force negative?", "when the force acts opposite to the displacement", ["when the force is very small", "when the object is at rest", "when the force is along the motion"], "Friction often does negative work."),
        ("What is 1 joule?", "the work done when a force of 1 N moves an object 1 m along the force", ["1 N per metre", "1 watt for 1 hour", "1 kg × 1 m/s"], "It is the SI unit of work and energy."),
        ("What is the SI unit of power?", "watt (W)", ["joule (J)", "newton (N)", "kilowatt hour (kWh)"], "1 W = 1 J/s."),
        ("What happens to the kinetic energy if the speed of an object is doubled?", "it becomes four times", ["it doubles", "it halves", "it stays the same"], "KE ∝ v²."),
        ("What happens to the kinetic energy if the mass of an object is doubled at the same speed?", "it doubles", ["it becomes four times", "it halves", "it stays the same"], "KE ∝ m."),
        ("What is potential energy?", "energy stored because of position or shape", ["energy of motion", "energy of light", "energy of sound"], "A stretched bow and a raised stone have PE."),
        ("What does the law of conservation of energy say?", "energy can neither be created nor destroyed, only changed from one form to another", ["energy is always lost", "energy can be created", "energy only exists as heat"], "The total energy stays the same."),
        ("What energy change happens in an electric bulb?", "electrical energy into light and heat", ["light into electrical energy", "heat into chemical energy", "sound into light"], "Most of it becomes heat in an old filament bulb."),
        ("What energy change happens in a torch cell?", "chemical energy into electrical energy", ["electrical into chemical energy", "light into heat", "sound into electrical energy"], "The cell powers the bulb."),
        ("What energy change happens when a ball is thrown upwards?", "kinetic energy turns into potential energy as it rises", ["potential energy turns into kinetic energy as it rises", "heat turns into light", "no energy changes"], "At the top it has the most PE."),
        ("Does gravity do work on a satellite moving in a circular orbit?", "no, because the force is at right angles to the motion", ["yes, a lot", "yes, negative work", "only at night"], "The displacement has no part along the force."),
        ("What is the energy of a stretched rubber band called?", "elastic potential energy", ["kinetic energy", "heat energy", "sound energy"], "It is released when the band is let go."),
        ("What is power?", "the rate of doing work", ["the total work done", "the force on an object", "the energy stored"], "P = W ÷ t."),
        ("What is 1 kilowatt?", "1,000 watts", ["100 watts", "1,000 joules", "3,600 watts"], "1 kW = 1,000 J/s."),
        ("Which has kinetic energy?", "a moving bullet", ["a book on a shelf", "a stretched spring at rest", "a battery"], "Moving objects have KE."),
        ("What happens to the total mechanical energy of a freely falling body?", "it stays the same (if air resistance is ignored)", ["it increases", "it becomes zero", "it doubles"], "PE falls as KE rises."),
        ("An object is carried by a porter on his head while he walks on a level road. Does he do work against gravity?", "no, since the motion is at right angles to gravity", ["yes, a lot", "yes, negative work", "only if he runs"], "He does work to start and stop moving, but none against gravity."),
        ("Which energy is stored in food and fuels?", "chemical energy", ["kinetic energy", "sound energy", "nuclear energy"], "It is released when they are burnt or digested."),
        ("What happens to the energy of a moving car when it brakes?", "it changes mostly into heat in the brakes and tyres", ["it disappears", "it becomes potential energy", "it becomes light"], "Energy is conserved.")]


# =================================================================== Chapter 11: sound
def c_sound(k=None):
    R = _R[0]
    k = k or ch(["v", "f", "lam", "T", "echo", "echoT", "sonar", "thunder", "range", "min"])
    if k in ("v", "f", "lam"):
        v, med = R.choice([(330, "air"), (340, "air"), (344, "air"), (1500, "water")])
        f = R.choice([100, 110, 125, 165, 170, 200, 250, 300, 340, 344, 400, 440, 500, 660, 680, 750, 1000, 1500, 1700, 2000])
        lam = F(v, f)
        if (lam * 1000).denominator != 1 or not F(1, 20) <= lam <= 15:
            return None
        lam = float(lam)
        if k == "v":
            return nq("A sound wave in %s has a frequency of %s Hz and a wavelength of %s m. What is its speed?" % (med, nf(f), nf(lam, 4)), v, [f / lam, lam / f, f + lam, v * 2], " m/s", "v = fλ = %s × %s = <b>%s m/s</b>." % (nf(f), nf(lam, 4), nf(v)))
        if k == "f":
            return nq("Sound travels at %s m/s in %s and has a wavelength of %s m. What is its frequency?" % (nf(v), med, nf(lam, 4)), f, [v * lam, lam / v, v - lam, f * 2], " Hz", "f = v ÷ λ = %s ÷ %s = <b>%s Hz</b>." % (nf(v), nf(lam, 4), nf(f)))
        return nq("A sound of frequency %s Hz travels at %s m/s in %s. What is its wavelength?" % (nf(f), nf(v), med), lam, [v * f, f / v, lam * 10, lam / 2], " m", "λ = v ÷ f = %s ÷ %s = <b>%s m</b>." % (nf(v), nf(f), nf(lam, 4)), sf=4)
    if k == "T":
        f = R.choice([50, 100, 200, 250, 400, 500, 1000, 2000])
        return nq("What is the time period of a sound wave of frequency %d Hz?" % f, 1 / f, [f, f / 1000, 1 / f * 2], " s", "T = 1 ÷ f = 1 ÷ %d = <b>%s s</b>." % (f, nf(1 / f)))
    if k == "echo":
        v, t = R.choice([330, 340, 344, 346]), R.choice([1, 1.5, 2, 3, 4, 0.5])
        d = v * t / 2
        return nq("A person shouts near a cliff and hears the echo %s s later. How far away is the cliff? (speed of sound = %d m/s)" % (nf(t), v), d, [v * t, v / t, d / 2], " m",
                  "The sound goes to the cliff and back: 2d = vt, so d = %d × %s ÷ 2 = <b>%s m</b>." % (v, nf(t), nf(d)))
    if k == "echoT":
        v, d = R.choice([330, 340, 344]), R.choice([165, 170, 340, 510, 680, 172])
        t = 2 * d / v
        return nq("A wall is %d m away. After how long is the echo of a clap heard? (speed of sound = %d m/s)" % (d, v), t, [d / v, 2 * v / d, t * 2, v / d], " s", "t = 2d ÷ v = 2 × %d ÷ %d = <b>%s s</b>." % (d, v, nf(t)))
    if k == "sonar":
        t = R.choice([0.5, 0.8, 1, 1.2, 1.5, 2, 2.4, 3, 4, 5])
        d = 1500 * t / 2
        return nq("A ship sends an ultrasonic signal to the sea bed and receives the echo after %s s. How deep is the sea? (speed of sound in sea water = 1,500 m/s)" % nf(t), d, [1500 * t, 1500 / t, d / 2, 340 * t / 2], " m",
                  "Depth = vt ÷ 2 = 1,500 × %s ÷ 2 = <b>%s m</b>." % (nf(t), nf(d)))
    if k == "thunder":
        t = R.choice([2, 3, 4, 5, 6, 8, 10])
        return nq("Thunder is heard %d s after a lightning flash is seen. How far away is the lightning? (speed of sound in air = 340 m/s)" % t, 340 * t, [170 * t, 340 / t, 340 * t * 2], " m",
                  "Light arrives almost at once, so d = 340 × %d = <b>%s m</b>. (No factor of 2: there is no echo.)" % (t, nf(340 * t)))
    if k == "min":
        v = R.choice([330, 340, 344, 346, 350])
        d = v * 0.1 / 2
        return nq("The sensation of sound lasts about 0.1 s in our brain. What is the minimum distance to a wall for an echo to be heard if sound travels at %d m/s?" % v, d, [v * 0.1, v / 0.1, d / 2], " m",
                  "2d = v × 0.1, so d = %d × 0.1 ÷ 2 = <b>%s m</b>." % (v, nf(d)))
    f = R.choice([5, 10, 15, 50, 256, 1000, 5000, 12000, 18000, 25000, 30000, 40000, 100000])
    a = "infrasonic (below 20 Hz)" if f < 20 else "ultrasonic (above 20,000 Hz)" if f > 20000 else "audible to humans"
    src = R.choice(["a vibrating object", "a source"])
    return tq("%s produces sound of frequency %s Hz. What kind of sound is it?" % (src[0].upper() + src[1:], nf(f)), a, [x for x in ["infrasonic (below 20 Hz)", "ultrasonic (above 20,000 Hz)", "audible to humans", "electromagnetic, not sound"] if x != a],
              "Humans hear about 20 Hz to 20,000 Hz; %s Hz is <b>%s</b>." % (nf(f), a))


SOUND = [("How is sound produced?", "by vibrating objects", ["by light", "by heat only", "by magnets"], "A plucked string vibrates."),
         ("Why can sound not travel through a vacuum?", "it needs a medium (solid, liquid or gas) to travel through", ["it is too slow", "a vacuum is too cold", "light blocks it"], "Astronauts talk by radio on the Moon."),
         ("What kind of wave is sound in air?", "a longitudinal wave", ["a transverse wave", "an electromagnetic wave", "a light wave"], "The particles vibrate along the direction of travel."),
         ("What is a compression?", "a region where the particles of the medium are crowded together (high pressure)", ["a region of low pressure", "the top of a water wave", "a vacuum"], "A rarefaction is a region of low pressure."),
         ("What is a rarefaction?", "a region where the particles are spread out (low pressure)", ["a region of high pressure", "the bottom of a ripple", "an echo"], "Compressions and rarefactions alternate."),
         ("What decides the pitch of a sound?", "its frequency", ["its amplitude", "its speed", "its wavelength alone"], "A higher frequency gives a higher pitch."),
         ("What decides the loudness of a sound?", "its amplitude", ["its frequency", "its pitch", "its time period"], "A bigger amplitude carries more energy."),
         ("In which medium does sound travel fastest?", "solids (such as steel)", ["gases", "liquids", "a vacuum"], "About 5,960 m/s in steel, 1,500 m/s in water, 340 m/s in air."),
         ("Why do we see lightning before we hear thunder?", "light travels much faster than sound", ["sound travels faster", "thunder happens later", "our eyes are closer to the clouds"], "Light travels at 3 × 10⁸ m/s."),
         ("What is an echo?", "a reflected sound heard after the original sound", ["a sound that never stops", "a very loud sound", "a sound in a vacuum"], "The wall must be at least about 17 m away."),
         ("What is reverberation?", "the persistence of sound in a big hall due to repeated reflections", ["a single echo", "the speed of sound", "the pitch of sound"], "It is reduced by curtains and fibreboard."),
         ("Why are the ceilings of concert halls curved?", "to reflect sound so it reaches every corner", ["to look nice", "to absorb all sound", "to stop echoes completely"], "A soundboard behind the stage does the same."),
         ("What is the audible range of the human ear?", "about 20 Hz to 20,000 Hz", ["about 2 Hz to 200 Hz", "about 200 Hz to 2,000,000 Hz", "all frequencies"], "Children can hear up to about 25 kHz."),
         ("Which animals can hear ultrasound?", "dogs, bats and dolphins", ["only humans", "only fish", "elephants only"], "Elephants and whales use infrasound."),
         ("How do bats find their way in the dark?", "they send out ultrasonic squeaks and listen for the echoes", ["they see very well in the dark", "they smell the walls", "they use magnets"], "Porpoises do the same."),
         ("What is SONAR used for?", "finding the depth of the sea and locating underwater objects", ["seeing stars", "measuring temperature", "making electricity"], "It sends ultrasound and times the echo."),
         ("Which medical tool uses ultrasound to form images of organs?", "ultrasonography (an ultrasound scanner)", ["an X-ray machine only", "a thermometer", "a stethoscope only"], "It is used to check a baby in the womb."),
         ("How does the speed of sound in air change when temperature rises?", "it increases", ["it decreases", "it stays the same", "sound stops"], "At 22 °C it is about 344 m/s."),
         ("What is the SI unit of frequency?", "hertz (Hz)", ["metre", "second", "decibel"], "1 Hz = one oscillation per second."),
         ("Which part of the ear vibrates when sound waves reach it?", "the eardrum", ["the cochlea only", "the pinna only", "the auditory nerve"], "Three bones in the middle ear pass on the vibrations."),
         ("What does a stethoscope use to carry sound?", "multiple reflections of sound inside the tube", ["electricity", "light", "radio waves"], "Megaphones and horns also use reflection."),
         ("Which sound has a higher pitch: a woman's or a man's voice (usually)?", "a woman's voice", ["a man's voice", "both the same", "neither has pitch"], "A higher frequency gives a higher pitch.")]


def UNITS9c():
    MF = "Motion, Force and Work"
    b = {n: once_maker(v) for n, v in [("mot", MOT), ("force", FORCE), ("grav", GRAV), ("work", WORK), ("snd", SOUND)]}
    return [
        U(7, "motion", 7, MF,
          "Motion: Distance and displacement, velocity; uniform and non-uniform motion along a straight line; acceleration, distance-time and velocity-time graphs for uniform motion and uniformly accelerated motion, elementary idea of uniform circular motion.",
          "Motion", "motion",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 7: distance and displacement, speed and velocity, km/h and m/s, acceleration, the three equations of motion, graphs and uniform circular motion. 100 questions with answers.",
          "v = u + at; s = ut + ½at²; v² − u² = 2as.", "Displacement is the straight line from start to finish.",
          "<p>Distance is the total path length; displacement is the shortest distance from the start to the finish in a given direction, so it can be zero. Speed is distance ÷ time; velocity is speed in a given direction. To change km/h into m/s, multiply by 5/18.</p>"
          "<p>Acceleration is the change in velocity per second: a = (v − u) ÷ t. For uniform acceleration the equations of motion are v = u + at, s = ut + ½at² and v² − u² = 2as. On a velocity–time graph the slope is the acceleration and the area under the line is the displacement. Uniform circular motion is accelerated because the direction keeps changing.</p>",
          [("72 km/h in m/s?", ["72 × 5/18"], "20 m/s"), ("u = 0, a = 2 m/s², t = 5 s. Distance?", ["s = ½ × 2 × 25"], "25 m")],
          ["Taking the average of two speeds as the average speed.", "Forgetting that a returning object has zero displacement.", "Using km/h and seconds in the same equation."],
          [("What is the difference between speed and velocity?", "Speed has only size; velocity is speed in a given direction, so it can change when only the direction changes."),
           ("What does the area under a velocity–time graph show?", "The displacement (distance travelled) in that time.")],
          lambda: [("Distance, displacement and speed", [(K(c_mot, "speed", "disp"), 14), (b["mot"], 6)]), ("Units and average speed", [(K(c_mot, "conv", "avg2"), 20)]),
                   ("Acceleration", [(K(c_mot, "acc", "eq1"), 20)]), ("Equations of motion", [(K(c_mot, "eq2", "eq3"), 20)]),
                   ("Graphs and circular motion", [(b["mot"], 12), (K(c_mot, "circ"), 8)])]),
        U(8, "force-and-laws-of-motion", 8, MF,
          "Force and Newton’s laws: Force and Motion, Newton’s Laws of Motion, Action and Reaction forces, Inertia of a body, Inertia and mass, Momentum, Force and Acceleration. Elementary idea of conservation of momentum.",
          "Force and Laws of Motion", "force and laws of motion",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 8: balanced and unbalanced forces, inertia, Newton's three laws, F = ma, momentum, impulse, recoil and conservation of momentum. 100 questions with answers.",
          "F = ma; momentum p = mv.", "Action and reaction act on different bodies.",
          "<p>An unbalanced force changes the state of rest or motion of an object. Inertia is the tendency to resist such a change, and mass measures it (Newton's first law). The second law says force equals the rate of change of momentum, so F = ma and F = (mv − mu) ÷ t.</p>"
          "<p>The third law says every action has an equal and opposite reaction, acting on a different body. Because of this, the total momentum of colliding or exploding objects stays the same when no outside force acts, which explains the recoil of a gun.</p>",
          [("Force on 1,000 kg with a = 2 m/s²?", ["F = ma"], "2,000 N"), ("20 g bullet at 200 m/s from a 4 kg gun. Recoil?", ["0.02 × 200 = 4 × V"], "1 m/s")],
          ["Forgetting to change grams into kilograms.", "Thinking action and reaction cancel each other.", "Saying a moving object needs a force to keep moving at constant velocity."],
          [("Why does a fielder draw his hands back when catching?", "It makes the time of impact longer, so the force needed to stop the ball is smaller."),
           ("What is the law of conservation of momentum?", "The total momentum of two or more objects stays the same if no external force acts on them.")],
          lambda: [("Inertia and the first law", [(b["force"], 12), (K(c_force, "F"), 8)]), ("Force and acceleration", [(K(c_force, "F", "a", "m"), 20)]),
                   ("Momentum and impulse", [(K(c_force, "p", "dp"), 20)]), ("Action, reaction and recoil", [(K(c_force, "recoil", "stick"), 14), (b["force"], 6)]),
                   ("Mixed problems", [(K(c_force, "stop"), 12), (K(c_force, "stick", "dp"), 6), (b["force"], 2)])]),
        U(9, "gravitation", 9, MF,
          "Gravitation: Universal Law of Gravitation, Force of Gravitation of the earth (gravity), Acceleration due to Gravity; Mass and Weight; Free fall. Floatation: Thrust and Pressure. Archimedes’ Principle; Buoyancy.",
          "Gravitation", "gravitation",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 9: the universal law of gravitation, g, free fall, mass and weight, weight on the Moon, thrust and pressure, buoyancy, Archimedes' principle and relative density. 100 questions with answers.",
          "Every two objects attract each other: F = Gm₁m₂ ÷ d².", "W = mg; on the Moon weight is one-sixth.",
          "<p>The gravitational force between two masses is F = Gm₁m₂ ÷ d², so doubling the distance makes it one-fourth. Near the Earth all objects fall with the same acceleration g ≈ 9.8 m/s², so the equations of motion apply with a = g. Weight is the force of gravity, W = mg; mass stays the same everywhere.</p>"
          "<p>Thrust is a force at right angles to a surface; pressure = thrust ÷ area, in pascals. A fluid pushes up on an object (buoyancy), and by Archimedes' principle the upthrust equals the weight of fluid displaced. An object floats if its density is less than that of the liquid.</p>",
          [("Weight of 10 kg on the Earth?", ["W = 10 × 9.8"], "98 N"), ("Distance doubled: force?", ["F ∝ 1/d²"], "one-fourth")],
          ["Saying mass changes on the Moon.", "Using d instead of d² in the law of gravitation.", "Thinking heavy objects fall faster in a vacuum."],
          [("Why does a ship float although iron sinks?", "Its hollow shape displaces a weight of water equal to its own weight, so its average density is less than water's."),
           ("What is the difference between g and G?", "g is the acceleration due to gravity (about 9.8 m/s² on the Earth); G is the universal constant 6.7 × 10⁻¹¹ N m²/kg², the same everywhere.")],
          lambda: [("The law of gravitation", [(K(c_grav, "ratio"), 12), (b["grav"], 8)]), ("Free fall", [(K(c_grav, "fall", "up"), 20)]),
                   ("Mass and weight", [(K(c_grav, "weight", "moon"), 14), (b["grav"], 6)]), ("Thrust and pressure", [(K(c_grav, "press"), 16), (b["grav"], 4)]),
                   ("Buoyancy and density", [(K(c_grav, "dens", "float", "upthrust"), 20)])]),
        U(10, "work-and-energy", 10, MF,
          "Work, Energy and Power: Work done by a Force, Energy, power; Kinetic and Potential energy; Law of conservation of energy (excluding commercial unit of Energy).",
          "Work and Energy", "work and energy",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 10: work done by a force, kinetic and potential energy, conservation of energy and power. 100 questions with answers.",
          "W = F × s; KE = ½mv²; PE = mgh.", "Energy changes form but is never created or destroyed.",
          "<p>Work is done when a force moves an object in its direction: W = F × s, in joules. If there is no displacement, or the force is at right angles to it, no work is done; a force against the motion does negative work.</p>"
          "<p>Kinetic energy is ½mv² and gravitational potential energy is mgh. As a ball falls, its PE changes into KE while the total stays the same. Power is the rate of doing work, P = W ÷ t, in watts (1 W = 1 J/s).</p>",
          [("KE of 5 kg at 4 m/s?", ["½ × 5 × 16"], "40 J"), ("10 kg raised 5 m (g = 10)?", ["10 × 10 × 5"], "500 J")],
          ["Forgetting to square the speed in KE.", "Saying holding a heavy bag still does work on it.", "Using minutes instead of seconds when finding power."],
          [("Does a person carrying a load on a level road do work against gravity?", "No, the force of gravity is at right angles to the motion, so no work is done against it."),
           ("What happens to KE when the speed is doubled?", "It becomes four times, because KE depends on v².")],
          lambda: [("Work done by a force", [(K(c_work, "W"), 14), (b["work"], 6)]), ("Kinetic energy", [(K(c_work, "ke", "ke2"), 20)]), ("Potential energy and conservation", [(K(c_work, "pe", "cons"), 20)]),
                   ("Power", [(K(c_work, "power", "climb"), 16), (b["work"], 4)]), ("Mixed problems", [(K(c_work, "W", "ke", "pe", "climb", "cons"), 14), (b["work"], 6)])]),
        U(11, "sound", 11, MF,
          "Sound: Nature of sound and its propagation in various media, speed of sound, range of hearing in humans; ultrasound; reflection of sound; echo.",
          "Sound", "sound",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 11: how sound is produced and travels, compressions and rarefactions, v = fλ, pitch and loudness, the range of hearing, echo, reverberation, ultrasound and SONAR. 100 questions with answers.",
          "Speed = frequency × wavelength.", "For an echo, the sound travels twice the distance.",
          "<p>Sound is made by vibrating objects and travels as a longitudinal wave of compressions and rarefactions through a medium; it cannot travel through a vacuum. It is fastest in solids and slowest in gases. Its speed is v = fλ, and the time period is T = 1 ÷ f. Frequency sets the pitch and amplitude sets the loudness.</p>"
          "<p>Sound reflects from hard surfaces; an echo is heard if the reflector is at least about 17 m away. Humans hear 20 Hz to 20,000 Hz; higher frequencies are ultrasound, used in SONAR and medical scans. In echo problems, distance = speed × time ÷ 2.</p>",
          [("f = 500 Hz, λ = 0.68 m. Speed?", ["v = fλ"], "340 m/s"), ("Echo after 2 s, v = 340 m/s. Distance?", ["2d = 340 × 2"], "340 m")],
          ["Forgetting to halve the distance in echo and SONAR problems.", "Mixing up pitch (frequency) and loudness (amplitude).", "Saying sound travels faster in air than in water."],
          [("Why can we not hear sound on the Moon?", "There is no air (no medium) to carry the sound waves."),
           ("What is the difference between an echo and reverberation?", "An echo is a single reflected sound heard separately; reverberation is the sound lasting in a hall because of many repeated reflections.")],
          lambda: [("How sound travels", [(b["snd"], 12), (K(c_sound, "range"), 8)]), ("Speed, frequency and wavelength", [(K(c_sound, "v", "f", "lam"), 14), (K(c_sound, "T"), 6)]),
                   ("Echo", [(K(c_sound, "echo", "echoT", "min"), 20)]), ("Ultrasound and SONAR", [(K(c_sound, "sonar"), 8), (K(c_sound, "range"), 6), (b["snd"], 4), (K(c_sound, "thunder"), 2)]),
                   ("Mixed problems", [(K(c_sound, "thunder", "v", "f", "lam", "echo"), 20)])]),
    ]
