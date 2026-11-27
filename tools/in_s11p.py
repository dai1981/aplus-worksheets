# -*- coding: utf-8 -*-
"""Class 11 Physics (NCERT Physics Part I and II, 14 chapters): question makers and UNITS()."""
import math
from in_sci import _R
from in_srs import ch, A, N, B, SU, pairs, odd_one, tq, nf, al_phys as P

PH = "Physics"
g = 9.8


def r1(x):
    return round(x, 1)


def ri(a, b, step=1):
    return _R[0].randrange(a, b + 1, step)


def rf(a, b, step):
    """random multiple of step between a and b"""
    n = _R[0].randint(round(a / step), round(b / step))
    return round(n * step, 6)


# =================================================================== 1 units and measurements
DIM = [("velocity", "[M⁰ L T⁻¹]"), ("acceleration", "[M⁰ L T⁻²]"), ("force", "[M L T⁻²]"), ("work or energy", "[M L² T⁻²]"), ("power", "[M L² T⁻³]"),
       ("pressure", "[M L⁻¹ T⁻²]"), ("momentum", "[M L T⁻¹]"), ("density", "[M L⁻³ T⁰]"), ("frequency", "[M⁰ L⁰ T⁻¹]"), ("gravitational constant G", "[M⁻¹ L³ T⁻²]"),
       ("Planck's constant", "[M L² T⁻¹]"), ("surface tension", "[M L⁰ T⁻²]"), ("impulse", "[M L T⁻¹] (same as momentum)"), ("angular velocity", "[M⁰ L⁰ T⁻¹] (same as frequency)")]
DIM2 = [r for r in DIM if "same" not in r[1]]
SI = [("length", "metre (m)"), ("mass", "kilogram (kg)"), ("time", "second (s)"), ("electric current", "ampere (A)"), ("thermodynamic temperature", "kelvin (K)"),
      ("amount of substance", "mole (mol)"), ("luminous intensity", "candela (cd)")]
PREF = [("k (kilo)", "10³"), ("M (mega)", "10⁶"), ("G (giga)", "10⁹"), ("m (milli)", "10⁻³"), ("μ (micro)", "10⁻⁶"), ("n (nano)", "10⁻⁹"), ("p (pico)", "10⁻¹²"), ("c (centi)", "10⁻²")]
SF = [("0.007", 1), ("2.64 × 10²⁴", 3), ("0.2370", 4), ("6.320", 4), ("6.032", 4), ("0.0006032", 4), ("4.700 m", 4), ("1.003", 4), ("0.050", 2), ("23.08", 4),
      ("5000.0", 5), ("0.08060", 4), ("3.0 × 10⁸", 2), ("12.40", 4), ("0.00305", 3), ("101.0", 4), ("7.20 × 10⁻³", 3), ("40.050", 5)]


def _rsf():
    L = ri(2, 5)
    d = str(ri(1, 9)) + "".join(str(ri(0, 9)) for _ in range(L - 1))
    f = ri(0, 2)
    if f == 0:
        return "0." + "0" * ri(0, 3) + d, L
    p = ri(1, L - 1)
    if f == 1:
        return d[:p] + "." + d[p:], L
    return d[:p] + "." + d[p:] + "0", L + 1


def u_sf(k=None):
    s, n = ch(SF) if _R[0].random() < 0.3 else _rsf()
    return N("How many significant figures are there in %s?" % s, n, [n + 1, n - 1, len(s.replace(".", "").replace(" ", ""))], "",
             "Leading zeros never count; zeros between digits and trailing zeros after a decimal point do. So <b>%d</b>." % n)


def u_err(k=None):
    k = k or ch(["pct", "prod", "pow", "mean"])
    if k == "pct":
        d = ch([0.1, 0.2, 0.5, 1.0])
        L = ri(5, 100) * d * ch([2, 5, 10])
        return N("A length is measured as (%s ± %s) cm. What is the percentage error?" % (nf(L), nf(d)), d / L * 100, [d / L, L / d, d * 100], "%",
                 "Percentage error = (Δl/l) × 100 = %s/%s × 100 = <b>%s%%</b>." % (nf(d), nf(L), nf(d / L * 100)))
    if k == "prod":
        a, b = rf(0.5, 4, 0.5), rf(0.5, 4, 0.5)
        return N("Two quantities with percentage errors %s%% and %s%% are multiplied. What is the maximum percentage error in the product?" % (nf(a), nf(b)), a + b, [abs(a - b) or a * 3, a * b, (a + b) / 2], "%",
                 "In a product (or quotient) the relative errors add: %s%% + %s%% = <b>%s%%</b>." % (nf(a), nf(b), nf(a + b)))
    if k == "pow":
        n, p = 3, rf(0.5, 4, 0.5)
        return N("The radius of a sphere is measured with an error of %s%%. What is the percentage error in its volume (V = 4πr³/3)?" % nf(p), 3 * p, [p, 2 * p, p ** 3], "%",
                 "For V ∝ r³ the relative error is multiplied by 3: 3 × %s%% = <b>%s%%</b>." % (nf(p), nf(3 * p))) if n else None
    base = ri(150, 450)
    xs = [round((base + ri(-12, 12)) / 100, 2) for _ in range(5)]
    m = sum(xs) / len(xs)
    dm = sum(abs(x - m) for x in xs) / len(xs)
    return N("Five readings of a period are %s s. What is the mean absolute error?" % ", ".join(nf(x) for x in xs), dm, [max(xs) - min(xs), m, dm * 5], " s",
             "Mean = %s s. Mean absolute error = average of |a<sub>i</sub> − a<sub>mean</sub>| = <b>%s s</b>." % (nf(m), nf(dm)))


def u_conv(k=None):
    k = k or ch(["kmh", "ms", "g", "dens"])
    if k == "kmh":
        v = ch([18, 36, 54, 72, 90, 108, 126, 144, 180])
        return N("Convert %d km/h into m/s." % v, v * 5 / 18, [v * 18 / 5, v / 3.6 * 10, v / 60], " m/s", "1 km/h = 5/18 m/s, so %d × 5/18 = <b>%s m/s</b>." % (v, nf(v * 5 / 18)))
    if k == "ms":
        v = ch([5, 10, 15, 20, 25, 30, 35, 40])
        return N("Convert %d m/s into km/h." % v, v * 3.6, [v / 3.6, v * 5 / 18, v * 60], " km/h", "1 m/s = 3.6 km/h, so %d × 3.6 = <b>%s km/h</b>." % (v, nf(v * 3.6)))
    if k == "dens":
        d = ch([1, 2.7, 7.8, 8.9, 11.3, 13.6, 19.3, 0.8])
        return N("A density of %s g/cm³ is how many kg/m³?" % nf(d), d * 1000, [d / 1000, d * 100, d * 10 ** 6], " kg/m³", "1 g/cm³ = 1000 kg/m³, so <b>%s kg/m³</b>." % nf(d * 1000))
    a = ch([1, 2, 5, 10, 25, 50])
    return N("How many square metres are there in %d cm²?" % a, a * 1e-4, [a * 1e-2, a * 1e4, a * 1e-3], " m²", "1 cm² = 10⁻⁴ m², so <b>%s m²</b>." % nf(a * 1e-4))


B1 = [("Which of these is a fundamental (base) quantity in SI?", "electric current", ["force", "velocity", "energy"], "Current, length, mass, time, temperature, amount of substance and luminous intensity are the seven base quantities."),
      ("How many base units are there in the SI system?", "seven", ["three", "five", "ten"], "m, kg, s, A, K, mol and cd."),
      ("What is 1 light year?", "the distance light travels in one year", ["the time light takes to reach Earth", "one year measured with light", "the speed of light"], "It is a unit of distance, about 9.46 × 10¹⁵ m."),
      ("What is 1 astronomical unit (AU)?", "the average distance between the Earth and the Sun", ["the distance to the Moon", "the size of the Sun", "one light year"], "About 1.496 × 10¹¹ m."),
      ("Which method is used to measure the distance of a nearby star?", "the parallax method", ["the echo method", "a metre rule", "a vernier calliper"], "The star seems to shift against distant stars as Earth moves round the Sun."),
      ("Which is the correct way to write the SI unit of force?", "N (newton)", ["Newton", "N.", "newtons N"], "Unit symbols are not capitalised in words and take no full stop."),
      ("Which of these quantities has no dimensions?", "strain", ["force", "pressure", "velocity"], "Strain is a ratio of two lengths."),
      ("Why can the dimensional method not find a constant such as 2π in a formula?", "pure numbers have no dimensions", ["constants are too small", "it only works for mass", "constants change"], "Dimensional analysis checks the powers of M, L and T only."),
      ("A formula is dimensionally correct. Does this prove it is correct?", "no, but a dimensionally wrong formula must be wrong", ["yes, always", "only for mechanics", "only in SI units"], "Numbers and constants cannot be checked."),
      ("Which instrument measures the diameter of a thin wire most precisely?", "a screw gauge", ["a metre rule", "a measuring tape", "a beaker"], "Its least count is usually 0.01 mm."),
      ("What is the least count of a typical vernier calliper?", "0.01 cm (0.1 mm)", ["1 cm", "1 mm", "0.001 mm"], "1 MSD − 1 VSD = 0.1 mm."),
      ("Which kind of error is caused by a zero error in an instrument?", "a systematic error", ["a random error", "a least count error", "a gross error of reading the wrong scale"], "It shifts every reading in the same direction."),
      ("How can random errors be reduced?", "by taking many readings and using their mean", ["by using a bigger unit", "by rounding off", "by ignoring odd readings always"], "Random errors average out."),
      ("Which atomic clock standard defines the second?", "the caesium-133 atom", ["the hydrogen atom", "a quartz crystal", "the Earth's rotation"], "One second is 9 192 631 770 periods of a caesium radiation."),
      ("What is the result of 2.5 × 1.25 written to correct significant figures?", "3.1", ["3.125", "3.12", "3"], "The answer keeps the fewest significant figures in the data (2)."),
      ("What is 12.11 + 18.0 + 1.012 written to correct decimal places?", "31.1", ["31.122", "31.12", "31"], "In addition keep the least number of decimal places (one, from 18.0)."),
      ("Rounded to three significant figures, what is 2.746?", "2.75", ["2.74", "2.7", "2.746"], "The fourth digit 6 is more than 5, so round up."),
      ("Rounded to three significant figures, what is 2.745?", "2.74", ["2.75", "2.7", "2.745"], "NCERT rule: when the dropped digit is 5, the preceding even digit is kept."),
      ("Which pair has the same dimensions?", "work and torque", ["force and power", "velocity and acceleration", "pressure and force"], "Both are [M L² T⁻²]."),
      ("What is the dimensional formula of the gravitational constant G?", "[M⁻¹ L³ T⁻²]", ["[M L² T⁻²]", "[M L T⁻²]", "[M⁻¹ L² T⁻¹]"], "From F = Gm₁m₂/r², G = Fr²/(m₁m₂)."),
      ("Which is the SI unit of solid angle?", "steradian (sr)", ["radian", "degree", "metre"], "Plane angle is in radians.")]


# =================================================================== 2 motion in a straight line
def s_avg(k=None):
    k = k or ch(["speed", "two", "vel", "rel", "stop", "fall"])
    if k == "speed":
        t1, t2 = ri(5, 40, 5), ri(5, 40, 5)
        d1, d2 = t1 * ri(2, 8), t2 * ri(2, 8)
        if d1 * t2 == d2 * t1:
            return None
        v = (d1 + d2) / (t1 + t2)
        return N("A runner covers %d m in %d s and then %d m in %d s. What is the average speed?" % (d1, t1, d2, t2), v, [(d1 / t1 + d2 / t2) / 2, (d1 + d2) / t2, d1 / t1], " m/s",
                 "Average speed = total distance ÷ total time = %d ÷ %d = <b>%s m/s</b>." % (d1 + d2, t1 + t2, nf(v)))
    if k == "two":
        v1 = ri(20, 60, 10)
        v2 = ri(v1 + 10, 100, 10)
        v = 2 * v1 * v2 / (v1 + v2)
        return N("A car goes from A to B at %d km/h and returns at %d km/h. What is its average speed for the round trip?" % (v1, v2), v, [(v1 + v2) / 2, v2 - v1, v1 * v2 / 100], " km/h",
                 "Equal distances: average speed = 2v₁v₂/(v₁ + v₂) = <b>%s km/h</b>, not the simple mean." % nf(v))
    if k == "vel":
        d, t = ch([200, 400, 600, 800, 1000]), ri(40, 200, 10)
        return tq("A boy runs round a circular track of length %d m and comes back to the start in %d s. What is his average velocity?" % (d, t), "0 m/s",
                  ["%s m/s" % nf(d / t), "%s m/s" % nf(d / t / 2), "%s m/s" % nf(2 * d / t)], "Displacement is zero, so average velocity is <b>0</b>; average speed is %s m/s." % nf(d / t))
    if k == "rel":
        va = ri(50, 120, 5)
        vb = ri(30, va - 10, 5)
        same = ch([True, False])
        v = va - vb if same else va + vb
        return N("Two trains move on parallel tracks at %d km/h and %d km/h %s. What is the speed of one relative to the other?" % (va, vb, "in the same direction" if same else "towards each other"),
                 v, [va + vb if same else va - vb, (va + vb) / 2, va], " km/h", "Relative velocity = %s = <b>%d km/h</b>." % ("v₁ − v₂" if same else "v₁ + v₂", v))
    if k == "stop":
        u, a = ri(10, 30), ch([2, 4, 5])
        return N("A car moving at %d m/s brakes with a deceleration of %d m/s². How far does it travel before stopping?" % (u, a), u * u / (2 * a), [u * u / a, u / a, u * a], " m",
                 "v² = u² − 2as, so s = u²/(2a) = %d/%d = <b>%s m</b>." % (u * u, 2 * a, nf(u * u / (2 * a))))
    t = ri(1, 6)
    if _R[0].random() < 0.5:
        return N("A stone is dropped from rest. What is its speed after %d s? (g = 9.8 m/s²)" % t, g * t, [0.5 * g * t, g * t * t, g / t], " m/s", "v = gt = 9.8 × %d = <b>%s m/s</b>." % (t, nf(g * t)))
    return N("A stone is dropped from a tall tower. How far does it fall in the first %d s? (g = 9.8 m/s²)" % t, 0.5 * g * t * t, [g * t * t, g * t, 0.5 * g * t], " m",
             "h = ½gt² = ½ × 9.8 × %d² = <b>%s m</b>." % (t, nf(0.5 * g * t * t)))


B2 = [("What does the slope of a position–time graph give?", "velocity", ["acceleration", "displacement", "distance"], "Slope = change in position ÷ time."),
      ("What does the slope of a velocity–time graph give?", "acceleration", ["displacement", "velocity", "jerk only"], "Slope = Δv/Δt."),
      ("What does the area under a velocity–time graph give?", "displacement", ["acceleration", "speed", "force"], "Area = v × t."),
      ("Can a body have zero velocity and non-zero acceleration?", "yes, at the top of its flight when thrown up", ["no, never", "only in space", "only for light bodies"], "At the top v = 0 but a = g downwards."),
      ("A ball is thrown straight up. What is its acceleration at the highest point?", "9.8 m/s² downwards", ["zero", "9.8 m/s² upwards", "it changes direction"], "Gravity acts all the time."),
      ("When is average speed equal to the magnitude of average velocity?", "when the body moves in one direction along a straight line", ["always", "never", "only in a circle"], "Then distance = displacement."),
      ("Which of these is a scalar?", "distance", ["displacement", "velocity", "acceleration"], "Distance has magnitude only."),
      ("Which equation has no time in it?", "v² = u² + 2as", ["v = u + at", "s = ut + ½at²", "s = vt"], "Use it when t is not given."),
      ("A position–time graph is a horizontal line. What does it show?", "the body is at rest", ["uniform velocity", "uniform acceleration", "free fall"], "Position does not change."),
      ("A velocity–time graph is a straight line sloping up. What is the motion?", "uniformly accelerated", ["at rest", "uniform velocity", "decelerating"], "Constant slope means constant acceleration."),
      ("Two balls, one heavy and one light, are dropped together in a vacuum. Which reaches the ground first?", "both together", ["the heavy one", "the light one", "it depends on colour"], "All bodies fall with the same g when there is no air resistance."),
      ("What is meant by uniform motion?", "equal displacements in equal intervals of time", ["equal accelerations", "motion in a circle", "zero displacement"], "Velocity is constant."),
      ("A car's speedometer reads 60 km/h. What does it show?", "the instantaneous speed", ["the average speed", "the displacement", "the acceleration"], "It shows speed at that moment."),
      ("What is the sign of acceleration when a car moving in the +x direction slows down?", "negative", ["positive", "zero", "it has no sign"], "Acceleration opposes velocity."),
      ("A body moves with constant velocity. What is its acceleration?", "zero", ["9.8 m/s²", "equal to velocity", "infinite"], "Velocity does not change."),
      ("Can the distance travelled ever be less than the magnitude of displacement?", "no", ["yes, always", "yes, in circular motion", "yes, when slowing down"], "Distance ≥ |displacement|."),
      ("In the equation s = ut + ½at², what does s stand for?", "displacement", ["speed", "time", "acceleration"], "s is the displacement in time t."),
      ("What is reaction time?", "the time a person takes to respond after seeing something", ["the time to stop a car", "the time of a chemical reaction", "the time of free fall"], "It can be found by catching a falling ruler.")]


# =================================================================== 3 motion in a plane
def pl(k=None):
    k = k or ch(["res", "comp", "H", "T", "R", "circ", "w", "river"])
    if k == "res":
        a, b = [ri(1, 5) * x for x in ch([(3, 4), (5, 12), (8, 15), (4, 3), (12, 5)])]
        return N("Two forces of %d N and %d N act at right angles. What is their resultant?" % (a, b), math.hypot(a, b), [a + b, abs(b - a), (a + b) / 2], " N",
                 "R = √(a² + b²) = √(%d + %d) = <b>%s N</b>." % (a * a, b * b, nf(math.hypot(a, b))))
    if k == "comp":
        F, th = ch([10, 20, 40, 50, 100]), ch([30, 60])
        c = ch(["x", "y"])
        v = F * (math.cos if c == "x" else math.sin)(math.radians(th))
        o = F * (math.sin if c == "x" else math.cos)(math.radians(th))
        return N("A vector of magnitude %d units makes %d° with the x-axis. What is its %s-component?" % (F, th, c), v, [o, F, F * th / 90], " units",
                 "A<sub>%s</sub> = A %s θ = %d × %s %d° = <b>%s</b>." % (c, "cos" if c == "x" else "sin", F, "cos" if c == "x" else "sin", th, nf(v)))
    u, th = ri(10, 50, 2), ch([30, 45, 60])
    s = math.sin(math.radians(th))
    if k == "H":
        H = u * u * s * s / (2 * g)
        return N("A ball is projected at %d m/s at %d° to the horizontal. Find its maximum height. (g = 9.8 m/s²)" % (u, th), H, [u * u * s / (2 * g), u * u / (2 * g), u * u * s * s / g], " m",
                 "H = u² sin²θ/(2g) = <b>%s m</b>." % nf(H))
    if k == "T":
        T = 2 * u * s / g
        return N("A ball is projected at %d m/s at %d° to the horizontal. Find its time of flight. (g = 9.8 m/s²)" % (u, th), T, [u * s / g, 2 * u / g, 2 * u * math.cos(math.radians(th)) / g], " s",
                 "T = 2u sin θ/g = <b>%s s</b>." % nf(T))
    if k == "R":
        Rr = u * u * math.sin(math.radians(2 * th)) / g
        return N("A ball is projected at %d m/s at %d° to the horizontal. Find its horizontal range. (g = 9.8 m/s²)" % (u, th), Rr, [u * u / g, u * u * s / g, u * u * math.sin(math.radians(2 * th)) / (2 * g)], " m",
                 "R = u² sin 2θ/g = <b>%s m</b>." % nf(Rr))
    if k == "circ":
        v, r = ri(4, 40, 2), ri(5, 200, 5)
        return N("A car moves round a circular track of radius %d m at a constant speed of %d m/s. What is its centripetal acceleration?" % (r, v), v * v / r, [v / r, v * r, v * v * r], " m/s²",
                 "a = v²/r = %d/%d = <b>%s m/s²</b>." % (v * v, r, nf(v * v / r)))
    if k == "w":
        n = ri(30, 1200, 30)
        return N("A wheel makes %d revolutions per minute. What is its angular speed?" % n, 2 * math.pi * n / 60, [n / 60, 2 * math.pi * n, math.pi * n / 60], " rad/s",
                 "ω = 2πf = 2π × %d/60 = <b>%s rad/s</b>." % (n, nf(2 * math.pi * n / 60)))
    w, vb = ri(60, 400, 20), ri(2, 6)
    vr = ri(1, vb - 1)
    return N("A swimmer crosses a %d m wide river, swimming at %d m/s straight across while the river flows at %d m/s. How long does the crossing take?" % (w, vb, vr), w / vb,
             [w / math.hypot(vb, vr), w / (vb - vr), w / (vb + vr)], " s", "Only the across-the-river velocity matters: t = %d ÷ %d = <b>%s s</b>." % (w, vb, nf(w / vb)))


B3 = [("For which angle of projection is the horizontal range maximum?", "45°", ["30°", "60°", "90°"], "sin 2θ is greatest (1) at θ = 45°."),
      ("Which two angles of projection give the same range?", "30° and 60°", ["30° and 45°", "20° and 80°", "45° and 90°"], "Complementary angles give the same range."),
      ("What is the path of a projectile (no air resistance)?", "a parabola", ["a straight line", "a circle", "a hyperbola"], "y = x tan θ − gx²/(2u²cos²θ)."),
      ("At the highest point of a projectile, what is its velocity?", "u cos θ, horizontal", ["zero", "u", "u sin θ, vertical"], "Only the vertical component becomes zero."),
      ("In uniform circular motion, which quantity stays constant?", "speed", ["velocity", "acceleration vector", "displacement"], "The direction of velocity keeps changing."),
      ("In which direction does centripetal acceleration point?", "towards the centre of the circle", ["along the tangent", "away from the centre", "upwards"], "a = v²/r towards the centre."),
      ("What is a unit vector?", "a vector of magnitude one that shows a direction", ["a vector of zero magnitude", "a scalar", "any small vector"], "î, ĵ and k̂ are unit vectors."),
      ("What is the null (zero) vector?", "a vector of zero magnitude", ["a unit vector", "a negative vector", "a scalar"], "A + (−A) = 0."),
      ("Two vectors of 3 and 4 units are added. Which of these cannot be the magnitude of the resultant?", "8 units", ["1 unit", "5 units", "7 units"], "The resultant lies between 1 and 7."),
      ("What does the law of parallelogram of vectors give?", "the resultant of two vectors", ["the dot product", "the speed of light", "the angle of projection"], "The diagonal from the common point is the resultant."),
      ("What is relative velocity of B with respect to A?", "v<sub>B</sub> − v<sub>A</sub>", ["v<sub>A</sub> + v<sub>B</sub>", "v<sub>A</sub> − v<sub>B</sub>", "v<sub>A</sub>v<sub>B</sub>"], "It is B's velocity as seen by A."),
      ("Rain falls vertically. Why does a man running hold his umbrella tilted forward?", "relative to him, the rain comes slanting from the front", ["to look stylish", "because of wind only", "the rain is horizontal"], "v<sub>rain, man</sub> = v<sub>rain</sub> − v<sub>man</sub>."),
      ("Which is a vector?", "displacement", ["mass", "time", "temperature"], "It has magnitude and direction."),
      ("Two projectiles are thrown with the same speed at 30° and 60°. Which stays in the air longer?", "the one at 60°", ["the one at 30°", "both the same", "it depends on mass"], "T = 2u sin θ/g is larger for larger θ."),
      ("What is the horizontal acceleration of a projectile (no air resistance)?", "zero", ["g", "g/2", "it changes"], "No horizontal force acts."),
      ("Is uniform circular motion accelerated motion?", "yes, because the direction of velocity changes", ["no, speed is constant", "only if speed changes", "only for planets"], "Change of direction is a change of velocity.")]


# =================================================================== 4 laws of motion
def lm(k=None):
    k = k or ch(["Fma", "fric", "lift", "atw", "recoil", "circ", "imp"])
    if k == "Fma":
        m, a = ch([2, 5, 10, 20, 50, 1000, 1500]), ch([0.5, 2, 3, 4, 1.5])
        return N("What force gives a %d kg body an acceleration of %s m/s²?" % (m, nf(a)), m * a, [m / a, a / m, m + a], " N", "F = ma = %d × %s = <b>%s N</b>." % (m, nf(a), nf(m * a)))
    if k == "fric":
        m, mu = ch([2, 5, 10, 20, 40, 50]), ch([0.1, 0.2, 0.25, 0.3, 0.4, 0.5])
        return N("A %d kg block rests on a horizontal floor (μ<sub>s</sub> = %s). What is the least horizontal force needed to start it moving? (g = 9.8 m/s²)" % (m, nf(mu)), mu * m * g,
                 [mu * m, m * g, m * g / mu], " N", "f<sub>max</sub> = μN = μmg = %s × %d × 9.8 = <b>%s N</b>." % (nf(mu), m, nf(mu * m * g)))
    if k == "lift":
        m, a = ch([40, 50, 60, 70, 80]), ch([1, 2, 2.2, 3, 4])
        up = ch([True, False])
        W = m * (g + a if up else g - a)
        return N("A person of mass %d kg stands on a weighing machine in a lift accelerating %s at %s m/s². What is the reading (normal force)? (g = 9.8 m/s²)" % (m, "upwards" if up else "downwards", nf(a)),
                 W, [m * g, m * (g - a if up else g + a), m * a], " N", "N = m(g %s a) = %d × %s = <b>%s N</b>." % ("+" if up else "−", m, nf(g + a if up else g - a), nf(W)))
    if k == "atw":
        m1 = ri(2, 10)
        m2 = ri(1, m1 - 1)
        a = (m1 - m2) * g / (m1 + m2)
        return N("Masses of %d kg and %d kg hang over a light frictionless pulley. What is their acceleration? (g = 9.8 m/s²)" % (m1, m2), a, [(m1 - m2) * g / m1, g, (m1 + m2) * g / (m1 - m2)], " m/s²",
                 "a = (m₁ − m₂)g/(m₁ + m₂) = %d × 9.8/%d = <b>%s m/s²</b>." % (m1 - m2, m1 + m2, nf(a)))
    if k == "recoil":
        M, m, v = ri(2, 10), ch([0.01, 0.02, 0.025, 0.05]), ri(200, 600, 50)
        return N("A %s kg gun fires a %s kg bullet at %d m/s. What is the recoil speed of the gun?" % (nf(M), nf(m), v), m * v / M, [M * v / m, v, m * v], " m/s",
                 "Momentum is conserved: MV = mv, V = %s × %d ÷ %s = <b>%s m/s</b>." % (nf(m), v, nf(M), nf(m * v / M)))
    if k == "circ":
        m, v, r = ch([0.5, 2, 5, 800, 1000, 1500]), ri(2, 20), ri(1, 50)
        return N("A %s kg body moves in a circle of radius %s m at %d m/s. What centripetal force is needed?" % (nf(m), nf(r), v), m * v * v / r, [m * v / r, m * v * v * r, m * v * v], " N",
                 "F = mv²/r = <b>%s N</b>." % nf(m * v * v / r))
    m, u, t = ch([0.15, 0.4, 0.5, 2]), ri(5, 30, 5), ch([0.01, 0.02, 0.05, 0.1])
    v = -ri(0, u // 5) * 5
    dp = abs(m * (v - u))
    return N("A %s kg ball moving at %d m/s is %s in %s s. What is the average force on it?" % (nf(m), u, "stopped" if v == 0 else "sent back at %d m/s" % abs(v), nf(t)), dp / t,
             [m * u / t if v else 2 * m * u / t, dp * t, m * abs(u + v) / t if (u + v) else m * u / (2 * t)], " N", "F = Δp/Δt = %s ÷ %s = <b>%s N</b>." % (nf(dp), nf(t), nf(dp / t)))


B4 = [("Which law of motion defines force?", "Newton's first law", ["Newton's third law", "the law of gravitation", "Hooke's law"], "A force is what changes the state of rest or uniform motion."),
      ("What does Newton's first law describe?", "inertia", ["momentum conservation", "action and reaction", "gravitation"], "A body keeps its state unless a net external force acts."),
      ("Why do passengers fall forward when a bus stops suddenly?", "inertia of motion", ["inertia of rest", "friction", "gravity"], "The body tends to keep moving."),
      ("What is the SI unit of impulse?", "N s", ["N/s", "N m", "kg m/s²"], "Impulse = FΔt = Δp."),
      ("Why does a cricketer pull his hands back while catching a ball?", "to increase the time and reduce the force", ["to increase the force", "to reduce the momentum change", "to look good"], "F = Δp/Δt."),
      ("Action and reaction forces act on…", "different bodies", ["the same body", "only one body at a time", "no body"], "So they never cancel each other."),
      ("A horse pulls a cart. Why does the cart move if the cart pulls the horse back equally?", "the forces act on different bodies; friction from the ground pushes the horse forward", ["the horse's pull is bigger", "Newton's third law fails", "the cart has no mass"], "Consider forces on each body separately."),
      ("Which law gives conservation of momentum directly?", "Newton's third law", ["Newton's first law", "Hooke's law", "Ohm's law"], "Equal and opposite impulses cancel in a closed system."),
      ("Which friction is the largest?", "limiting static friction", ["kinetic friction", "rolling friction", "they are all equal"], "μ<sub>s</sub> > μ<sub>k</sub> > rolling."),
      ("Why are ball bearings used in machines?", "rolling friction is much less than sliding friction", ["they increase friction", "they are decorative", "they add weight"], "They reduce wear and energy loss."),
      ("Does friction depend on the area of contact (for the same normal force)?", "no", ["yes, directly", "yes, inversely", "only for rough surfaces"], "f = μN."),
      ("What provides the centripetal force for a car turning on a level road?", "static friction between the tyres and road", ["gravity", "the engine", "air resistance"], "Without friction the car skids."),
      ("Why are roads banked on curves?", "a part of the normal force provides centripetal force", ["to drain rain only", "to slow cars", "to increase friction"], "tan θ = v²/(rg) for no friction."),
      ("What is the apparent weight of a person in a freely falling lift?", "zero", ["mg", "2mg", "mg/2"], "N = m(g − g) = 0."),
      ("A body is in equilibrium. What is the net force on it?", "zero", ["equal to its weight", "equal to friction", "infinite"], "ΣF = 0 for equilibrium."),
      ("How does a rocket move forward?", "hot gases pushed backward push the rocket forward", ["it pushes on the air", "gravity pulls it", "it floats"], "Newton's third law and momentum conservation."),
      ("What is the momentum of a body of mass m moving with velocity v?", "mv", ["½mv²", "m/v", "mg"], "Momentum is a vector, p = mv.")]


# =================================================================== 5 work, energy and power
def we(k=None):
    k = k or ch(["W", "spring", "Fv", "elastic", "pe2"])
    if k == "W":
        F, d, th = ch([10, 20, 50, 100]), ch([2, 5, 10, 20]), ch([0, 60, 90, 180])
        W = F * d * math.cos(math.radians(th))
        W = round(W, 6)
        return N("A force of %d N moves a body %d m. The force makes %d° with the displacement. How much work is done?" % (F, d, th), W if W else 0,
                 [F * d if th else F * d / 2, F * d * math.sin(math.radians(th)) or F * d * 2, F / d], " J", "W = Fd cos θ = %d × %d × cos %d° = <b>%s J</b>." % (F, d, th, nf(W) if W else "0")) if th != 90 else \
            tq("A force of %d N acts at right angles to the %d m displacement of a body. How much work does it do?" % (F, d), "0 J", ["%d J" % (F * d), "%d J" % (F * d // 2), "%d J" % (F + d)], "cos 90° = 0, so no work is done.")
    if k == "spring":
        kk, x = ch([100, 200, 500, 800, 1000, 2000]), ch([0.02, 0.05, 0.1, 0.2])
        return N("A spring of constant %d N/m is stretched by %s m. How much energy is stored in it?" % (kk, nf(x)), 0.5 * kk * x * x, [kk * x * x, 0.5 * kk * x, kk * x], " J",
                 "U = ½kx² = ½ × %d × %s² = <b>%s J</b>." % (kk, nf(x), nf(0.5 * kk * x * x)))
    if k == "Fv":
        F, v = ch([500, 1000, 1500, 2000, 3000]), ch([10, 15, 20, 25, 30])
        return N("A car's engine exerts a forward force of %d N at a steady speed of %d m/s. What is its power?" % (F, v), F * v, [F / v, F * v / 1000, 0.5 * F * v], " W", "P = Fv = <b>%s W</b>." % nf(F * v))
    if k == "elastic":
        m1, m2, u = ri(1, 5), ri(1, 5), ri(2, 10)
        v1, v2 = (m1 - m2) * u / (m1 + m2), 2 * m1 * u / (m1 + m2)
        return N("A %d kg ball moving at %d m/s hits a stationary %d kg ball in a perfectly elastic head-on collision. What is the speed of the second ball afterwards?" % (m1, u, m2), v2,
                 [m1 * u / (m1 + m2), abs(v1) or u / 2, u * m2 / m1], " m/s", "v₂ = 2m₁u/(m₁ + m₂) = <b>%s m/s</b>." % nf(v2))
    m, h = ch([1, 2, 5, 10, 20, 50]), ch([2, 5, 10, 15, 20])
    return N("A %d kg body falls freely from rest through %d m. What is its kinetic energy just before it lands? (g = 9.8 m/s²)" % (m, h), m * g * h, [m * h, 0.5 * m * g * h, m * g / h], " J",
             "Loss of PE = gain of KE = mgh = <b>%s J</b>." % nf(m * g * h))


B5 = [("What is the work done by the centripetal force on a body in uniform circular motion?", "zero", ["mv²", "mv²/r × 2πr", "negative"], "The force is always perpendicular to the motion."),
      ("What does the work–energy theorem state?", "the work done by the net force equals the change in kinetic energy", ["work equals power", "energy is always lost", "work equals momentum"], "W<sub>net</sub> = ΔK."),
      ("What is the SI unit of power?", "watt (J/s)", ["joule", "newton", "N s"], "1 W = 1 J/s."),
      ("How many joules make one kilowatt hour?", "3.6 × 10⁶ J", ["1000 J", "3600 J", "3.6 × 10³ J"], "1000 W × 3600 s."),
      ("What is 1 horsepower in watts?", "746 W", ["1000 W", "100 W", "550 W"], "1 hp ≈ 746 W."),
      ("In which collision is kinetic energy conserved?", "a perfectly elastic collision", ["a perfectly inelastic collision", "every collision", "no collision"], "Momentum is conserved in all collisions."),
      ("Two bodies stick together after a collision. What kind of collision is this?", "perfectly inelastic", ["perfectly elastic", "super-elastic", "explosive"], "Maximum KE is lost."),
      ("What is a conservative force?", "one whose work does not depend on the path", ["one that always does negative work", "friction", "one that is always zero"], "Gravity and spring forces are conservative."),
      ("Which of these is a non-conservative force?", "friction", ["gravity", "the spring force", "the electrostatic force"], "Work against friction depends on the path."),
      ("What happens to the kinetic energy of a body if its speed is doubled?", "it becomes four times", ["it doubles", "it halves", "it stays the same"], "K = ½mv²."),
      ("When is the work done by a force negative?", "when the force opposes the displacement", ["when the force is large", "when the body is at rest", "never"], "cos θ < 0 for θ > 90°."),
      ("In an elastic collision of two equal masses with one at rest, what happens?", "they exchange velocities", ["both stop", "they stick together", "both move together"], "The moving ball stops and the other moves on."),
      ("What is the potential energy of a spring compressed by x?", "½kx²", ["kx", "kx²", "½kx"], "Same as when stretched by x."),
      ("Which statement is true for a body thrown up (no air resistance)?", "the sum of kinetic and potential energy stays constant", ["kinetic energy stays constant", "potential energy stays constant", "total energy increases"], "Mechanical energy is conserved."),
      ("What is the dimensional formula of power?", "[M L² T⁻³]", ["[M L² T⁻²]", "[M L T⁻²]", "[M L² T⁻¹]"], "Power = work/time.")]


# =================================================================== 6 system of particles and rotational motion
def ro(k=None):
    k = k or ch(["cm", "tq", "I", "L", "Krot", "cons", "roll"])
    if k == "cm":
        m1, m2, d = ri(1, 6), ri(1, 6), ri(2, 12)
        if m1 == m2:
            return None
        x = m2 * d / (m1 + m2)
        return N("Masses of %d kg and %d kg are %d m apart. How far is the centre of mass from the %d kg mass?" % (m1, m2, d, m1), x, [m1 * d / (m1 + m2), d / 2, m2 * d / m1], " m",
                 "x = m₂d/(m₁ + m₂) = %d × %d ÷ %d = <b>%s m</b> (closer to the heavier mass)." % (m2, d, m1 + m2, nf(x)))
    if k == "tq":
        F, r, th = ch([10, 20, 30, 50]), ch([0.2, 0.25, 0.4, 0.5, 1]), ch([30, 90, 60])
        t = F * r * math.sin(math.radians(th))
        return N("A force of %d N acts %s m from a hinge at %d° to the line from the hinge. What is the torque?" % (F, nf(r), th), t, [F * r if th != 90 else F * r / 2, F / r, F * r * math.cos(math.radians(th)) or F * r * 2], " N m",
                 "τ = rF sin θ = %s × %d × sin %d° = <b>%s N m</b>." % (nf(r), F, th, nf(t)))
    if k == "I":
        M, Rr = ch([1, 2, 3, 4, 5, 10]), ch([0.1, 0.2, 0.3, 0.5, 1])
        body, f, nm = ch([("thin ring", 1, "MR²"), ("uniform disc", 0.5, "½MR²"), ("solid sphere", 0.4, "(2/5)MR²"), ("hollow sphere", 2 / 3, "(2/3)MR²")])
        return N("Find the moment of inertia of a %s of mass %d kg and radius %s m about its central axis (through the centre, perpendicular to the plane for the ring and disc, or any diameter for the spheres)." % (body, M, nf(Rr)),
                 f * M * Rr * Rr, [M * Rr * Rr if f != 1 else 0.5 * M * Rr * Rr, f * M * Rr, 0.4 * M * Rr * Rr if f != 0.4 else 0.5 * M * Rr * Rr], " kg m²", "I = %s = <b>%s kg m²</b>." % (nm, nf(f * M * Rr * Rr)))
    if k == "L":
        I, n = ch([0.5, 1, 2, 4, 0.2]), ch([60, 120, 300, 600])
        w = 2 * math.pi * n / 60
        return N("A wheel with moment of inertia %s kg m² spins at %d rpm. What is its angular momentum?" % (nf(I), n), I * w, [I * n, I * n / 60, 0.5 * I * w * w], " kg m²/s", "ω = 2π × %d/60 = %s rad/s; L = Iω = <b>%s kg m²/s</b>." % (n, nf(w), nf(I * w)))
    if k == "Krot":
        I, w = ch([0.1, 0.5, 1, 2, 5]), ch([2, 4, 5, 10, 20])
        return N("A flywheel with I = %s kg m² rotates at %d rad/s. What is its rotational kinetic energy?" % (nf(I), w), 0.5 * I * w * w, [I * w * w, I * w, 0.5 * I * w], " J", "K = ½Iω² = <b>%s J</b>." % nf(0.5 * I * w * w))
    if k == "cons":
        w1, f = rf(1, 6, 0.5), ch([1.5, 2, 2.5, 3, 4])
        return N("A skater spinning at %s rev/s pulls in her arms, so her moment of inertia becomes 1/%s of the value before. What is her new rate of spin?" % (nf(w1), nf(f)), w1 * f, [w1 / f, w1, w1 * f * f], " rev/s",
                 "Angular momentum is conserved: I₁ω₁ = I₂ω₂, so ω₂ = %s × %s = <b>%s rev/s</b>." % (nf(w1), nf(f), nf(w1 * f)))
    body, f = ch([("solid sphere", 2 / 5), ("disc (solid cylinder)", 1 / 2), ("ring (hollow cylinder)", 1)])
    return tq("A %s rolls without slipping. What fraction of its total kinetic energy is rotational?" % body, "%s" % {0.4: "2/7", 0.5: "1/3", 1: "1/2"}[f],
              [x for x in ["2/7", "1/3", "1/2", "2/5", "1/4"] if x != {0.4: "2/7", 0.5: "1/3", 1: "1/2"}[f]], "K<sub>rot</sub>/K<sub>total</sub> = (k²/R²)/(1 + k²/R²) with k²/R² = %s." % {0.4: "2/5", 0.5: "1/2", 1: "1"}[f])


B6 = [("What is the rotational analogue of mass?", "moment of inertia", ["torque", "angular momentum", "angular velocity"], "It measures resistance to change in rotation."),
      ("What is the rotational analogue of force?", "torque", ["moment of inertia", "angular momentum", "power"], "τ = r × F."),
      ("When is the angular momentum of a system conserved?", "when no external torque acts", ["when no external force acts", "always", "when it rotates fast"], "dL/dt = τ<sub>ext</sub>."),
      ("Why does a diver tuck in her legs and arms during a somersault?", "to reduce the moment of inertia and spin faster", ["to increase friction", "to fall faster", "to increase mass"], "Iω stays constant."),
      ("What are the conditions for a rigid body to be in mechanical equilibrium?", "net force and net torque are both zero", ["only net force is zero", "only net torque is zero", "the body must be at rest"], "Translational and rotational equilibrium."),
      ("The theorem of parallel axes is I = I<sub>cm</sub> + …", "Md²", ["MR²", "½Md²", "Md"], "d is the distance between the axes."),
      ("The theorem of perpendicular axes applies to…", "plane (flat) bodies", ["all solid bodies", "only spheres", "only rods"], "I<sub>z</sub> = I<sub>x</sub> + I<sub>y</sub>."),
      ("What is the moment of inertia of a thin rod of mass M and length L about an axis through its centre, perpendicular to it?", "ML²/12", ["ML²/3", "ML²", "ML²/2"], "About one end it is ML²/3."),
      ("Where can the centre of mass of a ring be?", "at its centre, where there is no mass", ["on the ring only", "at the top", "anywhere"], "The centre of mass need not lie inside the body."),
      ("Which rolls down an incline fastest from rest: a ring, a disc or a solid sphere (same mass and radius)?", "the solid sphere", ["the ring", "the disc", "all together"], "Smaller k²/R² means more energy goes into translation."),
      ("What is the SI unit of torque?", "N m", ["J", "N/m", "kg m²"], "It is not written as joule even though the dimensions match."),
      ("What is the relation between torque and angular momentum?", "torque = rate of change of angular momentum", ["torque = angular momentum × time", "they are equal", "torque = L²"], "τ = dL/dt."),
      ("What is a couple?", "two equal and opposite forces with different lines of action", ["two forces in the same direction", "a single force", "action and reaction"], "It produces rotation without translation."),
      ("In the principle of moments for a lever, what balances?", "the clockwise and anticlockwise moments", ["the masses on each side", "the lengths of the arms", "the forces only"], "Load × load arm = effort × effort arm.")]


# =================================================================== 7 gravitation
def gr(k=None):
    k = k or ch(["esc", "gh", "kep", "depth", "weight"])
    if k == "esc":
        gg, Rr, nm = ch([(9.8, 6.4e6, "the Earth"), (1.6, 1.74e6, "the Moon"), (3.7, 3.4e6, "Mars")])
        v = math.sqrt(2 * gg * Rr)
        return N("For %s, g = %s m/s² and R = %s m. What is the escape speed?" % (nm, nf(gg), nf(Rr)), v / 1000, [math.sqrt(gg * Rr) / 1000, 2 * gg * Rr / 1e6, v / 1000 * 2], " km/s",
                 "v<sub>e</sub> = √(2gR) = <b>%s km/s</b>." % nf(v / 1000))
    if k == "gh":
        f = ch([(1, 2), (2, 3), (1, 4), (1, 1), (2, 1), (3, 1), (1, 3), (3, 4), (1, 5), (3, 2)])
        h = ("%dR/%d" % f if f[1] > 1 else "%dR" % f[0]).replace("1R", "R")
        val = 9.8 / (1 + f[0] / f[1]) ** 2
        return N("What is g at a height of %s above the Earth's surface? (g = 9.8 m/s² at the surface)" % h, val, [9.8 / (1 + f[0] / f[1]), 9.8 * (1 - 2 * f[0] / f[1]) if f[0] / f[1] < 0.5 else 9.8 / 2 ** 3, 9.8], " m/s²",
                 "g<sub>h</sub> = g/(1 + h/R)² = 9.8/(%s)² = <b>%s m/s²</b>." % (nf(1 + f[0] / f[1]), nf(val)))
    if k == "kep":
        n = ch([4, 9, 16, 25, 0.25, 1.5, 2.25, 6.25, 36, 0.36])
        T = n ** 1.5
        return N("A planet's orbit has a radius %s times the Earth's orbit. Using Kepler's third law, what is its period in years?" % nf(n), T, [n, n * n, math.sqrt(n)], " years",
                 "T² ∝ r³, so T = %s<sup>3/2</sup> = <b>%s years</b>." % (nf(n), nf(T)))
    if k == "depth":
        f = ri(2, 10)
        return N("What is g at a depth of R/%d below the Earth's surface? (g = 9.8 m/s² at the surface)" % f, 9.8 * (1 - 1 / f), [9.8 / (1 + 1 / f) ** 2, 9.8 / f, 9.8], " m/s²",
                 "g<sub>d</sub> = g(1 − d/R) = 9.8 × %s = <b>%s m/s²</b>." % (nf(1 - 1 / f), nf(9.8 * (1 - 1 / f))))
    m = ri(30, 96, 6)
    return N("A person has a mass of %d kg. What is his weight on the Moon, where g is one-sixth of 9.8 m/s²?" % m, m * 9.8 / 6, [m / 6, m * 9.8, m], " N",
             "Mass stays %d kg; weight = m × g/6 = <b>%s N</b>." % (m, nf(m * 9.8 / 6)))


B7 = [("What does Kepler's first law state?", "planets move in elliptical orbits with the Sun at one focus", ["planets move in circles", "planets stand still", "the Sun moves round the Earth"], "The law of orbits."),
      ("What does Kepler's second law state?", "the line from the Sun to a planet sweeps equal areas in equal times", ["orbits are circles", "T² ∝ r³", "planets have equal speeds"], "It follows from conservation of angular momentum."),
      ("Where does a planet move fastest in its orbit?", "at perihelion, closest to the Sun", ["at aphelion", "everywhere the same", "halfway"], "Equal areas in equal times."),
      ("What is the value of G?", "6.67 × 10⁻¹¹ N m² kg⁻²", ["9.8 m/s²", "6.67 × 10¹¹ N m² kg⁻²", "3 × 10⁸ m/s"], "Measured first by Cavendish."),
      ("How does g change as we go towards the centre of the Earth?", "it decreases and becomes zero at the centre", ["it increases", "it stays the same", "it becomes infinite"], "g<sub>d</sub> = g(1 − d/R)."),
      ("What is the escape speed from the Earth?", "about 11.2 km/s", ["about 7.9 km/s", "about 3 km/s", "about 340 m/s"], "√(2gR)."),
      ("What is the orbital speed of a satellite close to the Earth's surface?", "about 7.9 km/s", ["about 11.2 km/s", "about 1 km/s", "about 30 km/s"], "v = √(gR)."),
      ("What is the period of a geostationary satellite?", "24 hours", ["12 hours", "1 hour", "1 month"], "It turns with the Earth."),
      ("At what height above the equator do geostationary satellites orbit?", "about 36,000 km", ["about 300 km", "about 6,400 km", "about 384,000 km"], "They are used for communication."),
      ("Why do astronauts in an orbiting spacecraft feel weightless?", "they and the craft fall freely together", ["there is no gravity in space", "they have no mass", "the Earth repels them"], "Both have the same acceleration."),
      ("What is the gravitational potential energy of a mass m at distance r from the centre of the Earth (mass M)?", "−GMm/r", ["GMm/r", "mgr", "GMm/r²"], "It is zero at infinity and negative everywhere else."),
      ("If the distance between two masses is doubled, the gravitational force becomes…", "one-fourth", ["half", "double", "four times"], "F ∝ 1/r²."),
      ("Which quantity is the same on the Earth and on the Moon?", "mass", ["weight", "g", "the escape speed"], "Weight = mg changes."),
      ("Does the escape speed depend on the mass of the body escaping?", "no", ["yes, it increases with mass", "yes, it decreases with mass", "only for rockets"], "v<sub>e</sub> = √(2GM/R).")]


# =================================================================== 9 fluids
def fl(k=None):
    k = k or ch(["P", "hyd", "cont", "cap", "drop", "term"])
    if k == "P":
        rho, nm = ch([(1000, "water"), (1030, "sea water"), (800, "oil")])
        h = ri(2, 100)
        p = rho * g * h
        return N("What is the pressure due to a column of %s %s m deep (ρ = %d kg/m³)? Ignore atmospheric pressure. (g = 9.8 m/s²)" % (nm, nf(h), rho), p, [rho * h, rho * g / h, rho * g * h / 2], " Pa",
                 "p = ρgh = %d × 9.8 × %s = <b>%s Pa</b>." % (rho, nf(h), nf(p)))
    if k == "hyd":
        F1, a1, a2 = ri(20, 200, 10), ch([2, 4, 5, 10]), ri(100, 2000, 100)
        return N("In a hydraulic lift, a force of %d N is applied on a piston of area %d cm². What force acts on the bigger piston of area %d cm²?" % (F1, a1, a2), F1 * a2 / a1, [F1 * a1 / a2, F1, F1 * a2], " N",
                 "Pascal's law: F₂ = F₁ × A₂/A₁ = <b>%s N</b>." % nf(F1 * a2 / a1))
    if k == "cont":
        v1, r2 = rf(0.5, 3, 0.5), ch([1, 1.5, 2])
        r1 = r2 * ch([1.5, 2, 2.5, 3])
        v2 = v1 * (r1 / r2) ** 2
        return N("Water flows at %s m/s in a pipe of radius %s cm that narrows to %s cm. What is its speed in the narrow part?" % (nf(v1), nf(r1), nf(r2)), v2, [v1 * r1 / r2, v1 * r2 / r1, v1], " m/s",
                 "A₁v₁ = A₂v₂, so v₂ = v₁(r₁/r₂)² = <b>%s m/s</b>." % nf(v2))
    if k == "cap":
        r = ch([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5])
        T = 0.073
        h = 2 * T / (r * 1e-3 * 1000 * g)
        return N("How high does water rise in a clean glass capillary tube of radius %s mm? (surface tension 0.073 N/m, angle of contact 0°, g = 9.8 m/s²)" % nf(r), h * 100, [h * 50, h * 1000, T / (r * 1e-3 * 1000 * g) * 1000], " cm",
                 "h = 2T/(rρg) = 2 × 0.073 ÷ (%s × 10⁻³ × 1000 × 9.8) = <b>%s cm</b>." % (nf(r), nf(h * 100)))
    if k == "drop":
        T, r = ch([0.073, 0.465]), ch([0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
        return N("What is the excess pressure inside a liquid drop of radius %s mm if the surface tension is %s N/m?" % (nf(r), nf(T)), 2 * T / (r * 1e-3), [4 * T / (r * 1e-3), T / (r * 1e-3), 2 * T * r * 1e-3], " Pa",
                 "For a drop, p = 2T/r (a soap bubble with two surfaces has 4T/r) = <b>%s Pa</b>." % nf(2 * T / (r * 1e-3)))
    r = rf(0.05, 0.5, 0.05)
    rr = r * 1e-3
    mat, rho = ch([("aluminium", 2700), ("steel", 7800), ("glass", 2500)])
    v = 2 * rr * rr * (rho - 1000) * g / (9 * 1.0e-3)
    return N("A small %s ball (ρ = %d kg/m³) of radius %s mm falls through water (ρ = 1000 kg/m³, η = 1.0 × 10⁻³ Pa s). Using Stokes' law, what is its terminal velocity?" % (mat, rho, nf(r)), v,
             [2 * rr * rr * rho * g / (9e-3), rr * rr * (rho - 1000) * g / 9e-3, 2 * rr * (rho - 1000) * g / 9e-3], " m/s", "v<sub>t</sub> = 2r²(ρ − σ)g/(9η) = <b>%s m/s</b>." % nf(v))


B9 = [("What does Pascal's law state?", "pressure applied to an enclosed fluid is passed on equally in all directions", ["pressure is zero in fluids", "fluids cannot be compressed", "pressure depends on shape"], "Used in hydraulic lifts and brakes."),
      ("What does Bernoulli's principle say about a fluid flowing faster?", "its pressure is lower", ["its pressure is higher", "its density increases", "it stops flowing"], "p + ½ρv² + ρgh is constant along a streamline."),
      ("How does an aeroplane wing get lift?", "air flows faster over the top, so pressure above is lower", ["the engine pushes it up", "the wing is light", "air pushes only from below at rest"], "Pressure difference gives upward force."),
      ("What is viscosity?", "the internal friction of a fluid", ["the density of a fluid", "the surface tension", "the pressure of a fluid"], "Honey is more viscous than water."),
      ("How does the viscosity of a liquid change when it is heated?", "it decreases", ["it increases", "it stays the same", "it becomes infinite"], "Hot oil flows more easily."),
      ("What is terminal velocity?", "the constant speed reached when the drag balances the net downward force", ["the highest speed of light", "zero speed", "the speed at the start"], "Raindrops reach terminal velocity."),
      ("What is surface tension?", "the force per unit length on the surface of a liquid", ["the pressure inside a liquid", "the weight of a liquid", "the viscosity"], "Its unit is N/m."),
      ("Why are small drops of water spherical?", "surface tension makes the surface area as small as possible", ["gravity pulls them round", "air pushes them", "water is round"], "A sphere has the least area for a given volume."),
      ("Why does mercury fall (depression) in a glass capillary tube?", "its angle of contact with glass is more than 90°", ["it is heavy", "it is a metal", "it has no surface tension"], "Cohesion is greater than adhesion."),
      ("What happens to surface tension when detergent is added to water?", "it decreases", ["it increases", "it stays the same", "it doubles"], "This helps water wet greasy cloth."),
      ("What is the SI unit of the coefficient of viscosity?", "Pa s (poiseuille)", ["N/m", "Pa", "N s"], "1 poise = 0.1 Pa s."),
      ("What does Reynolds number tell us?", "whether flow is streamlined or turbulent", ["the density of a fluid", "the pressure", "the surface tension"], "Low values mean streamline flow."),
      ("Why is a bubble's excess pressure 4T/r but a drop's only 2T/r?", "a bubble has two surfaces", ["a bubble is lighter", "a drop is bigger", "air has more tension"], "Inside and outside surfaces of the film."),
      ("Atmospheric pressure at sea level is about…", "1.01 × 10⁵ Pa", ["1 Pa", "760 Pa", "9.8 × 10⁵ Pa"], "It equals 76 cm of mercury.")]


# =================================================================== 10 thermal properties
def th(k=None):
    k = k or ch(["lin", "K", "wien", "area", "cond"])
    if k == "lin":
        a, nm = ch([(1.2e-5, "steel rail"), (2.3e-5, "aluminium rod"), (1.7e-5, "copper rod"), (1.9e-5, "brass rod")])
        L, dT = ri(1, 30), ri(20, 100, 10)
        d = L * a * dT
        return N("A %s %d m long (α = %s K⁻¹) is heated through %d K. By how much does it expand?" % (nm, L, nf(a), dT), d * 1000, [d, L * a * 1000, d * 2000], " mm",
                 "ΔL = αLΔT = %s × %d × %d = %s m = <b>%s mm</b>." % (nf(a), L, dT, nf(d), nf(d * 1000)))
    if k == "K":
        c = ri(-80, 400, 5)
        return N("Convert %d °C into kelvin." % c, c + 273.15, [c - 273.15, c + 273, c * 273.15 / 100], " K", "T(K) = t(°C) + 273.15 = <b>%s K</b>." % nf(c + 273.15, 5))
    if k == "wien":
        T, nm = ch([(5800, "the Sun's surface"), (3000, "a red star"), (3500, "a red star"), (10000, "a hot blue star"), (20000, "a hot blue star"), (310, "the human body"), (1500, "a hot stove ring"), (2900, "a lamp filament")])
        lam = 2.9e-3 / T
        return N("Using Wien's law (λ<sub>m</sub>T = 2.9 × 10⁻³ m K), at what wavelength does %s (about %d K) radiate most strongly?" % (nm, T), lam * 1e9, [lam * 1e6, T / 2.9e-3, lam * 1e9 * 2], " nm",
                 "λ<sub>m</sub> = 2.9 × 10⁻³ ÷ %d = <b>%s nm</b>." % (T, nf(lam * 1e9)))
    if k == "area":
        a = ch([1.2e-5, 1.7e-5, 2.3e-5])
        return tq("A metal has a coefficient of linear expansion α = %s K⁻¹. What is its coefficient of volume expansion?" % nf(a), nf(3 * a) + " K⁻¹", [nf(a) + " K⁻¹", nf(2 * a) + " K⁻¹", nf(a ** 3) + " K⁻¹"],
                  "γ = 3α for an isotropic solid (and β = 2α for area).")
    kk, A, d, dT = ch([400, 200, 50, 0.8]), ch([0.01, 0.02, 0.05, 1, 2]), ch([0.1, 0.2, 0.25, 0.5]), ri(10, 100, 10)
    H = kk * A * dT / d
    return N("A slab of area %s m² and thickness %s m (thermal conductivity %s W m⁻¹ K⁻¹) has a temperature difference of %d K across it. What is the rate of heat flow?" % (nf(A), nf(d), nf(kk), dT), H,
             [kk * A * dT * d, kk * dT / d, kk * A / d], " W", "H = KAΔT/d = <b>%s W</b>." % nf(H))


B10 = [("Why does a thick glass tumbler crack when hot tea is poured into it?", "the inner surface expands more than the outer surface", ["glass contracts when heated", "tea is too heavy", "glass melts"], "Glass is a poor conductor."),
       ("What is the anomalous expansion of water?", "water contracts on heating from 0 °C to 4 °C", ["water expands from 0 °C to 4 °C", "water never expands", "ice sinks"], "Water is densest at 4 °C."),
       ("Why do lakes freeze from the top down?", "water is densest at 4 °C, so colder water stays on top", ["heat rises from below", "ice is heavier", "fish warm the bottom"], "Aquatic life survives below the ice."),
       ("Which mode of heat transfer needs no medium?", "radiation", ["conduction", "convection", "evaporation"], "Heat reaches us from the Sun through space."),
       ("Sea breezes during the day are an example of…", "convection", ["conduction", "radiation", "insulation"], "Air over land heats and rises."),
       ("What is the specific heat capacity of water?", "about 4186 J kg⁻¹ K⁻¹", ["about 100 J kg⁻¹ K⁻¹", "about 1 J kg⁻¹ K⁻¹", "about 41 860 J kg⁻¹ K⁻¹"], "This is why water heats and cools slowly."),
       ("What is the latent heat of fusion of ice?", "about 3.34 × 10⁵ J/kg", ["about 2.26 × 10⁶ J/kg", "about 4186 J/kg", "about 334 J/kg"], "Heat needed to melt 1 kg of ice at 0 °C."),
       ("What happens to the temperature of water while it boils?", "it stays the same", ["it keeps rising", "it falls", "it rises and falls"], "The heat is used as latent heat."),
       ("Why does a pressure cooker cook food faster?", "higher pressure raises the boiling point of water", ["it lowers the boiling point", "it uses less heat", "steam is cold"], "Water boils above 100 °C inside."),
       ("Which law states that the rate of cooling is proportional to the temperature difference with the surroundings?", "Newton's law of cooling", ["Stefan's law", "Wien's law", "Hooke's law"], "For small temperature differences."),
       ("The Stefan–Boltzmann law says the power radiated by a body is proportional to…", "T⁴", ["T", "T²", "1/T"], "T is the absolute temperature."),
       ("What is a black body?", "a body that absorbs all radiation falling on it", ["a body painted black only", "a body that reflects all radiation", "a cold body"], "It is also the best emitter."),
       ("At what temperature are the Celsius and Kelvin scales differing by 273.15?", "at every temperature", ["only at 0 °C", "only at 100 °C", "never"], "T = t + 273.15."),
       ("What is the triple point of water?", "273.16 K, where ice, water and vapour coexist", ["373 K", "0 K", "4 °C"], "Used to define the kelvin."),
       ("Why are railway tracks laid with small gaps?", "to allow for expansion in summer", ["to save steel", "for drainage", "to make noise"], "Prevents buckling.")]


# =================================================================== 11 thermodynamics
def td(k=None):
    k = k or ch(["dU", "W", "carnot", "cop", "iso"])
    if k == "dU":
        Q = ri(300, 1500, 100)
        W = ri(100, Q - 100, 50)
        return N("A gas absorbs %d J of heat and does %d J of work on its surroundings. What is the change in its internal energy?" % (Q, W), Q - W, [Q + W, W - Q if W != Q else Q, Q], " J",
                 "First law: ΔU = Q − W = <b>%d J</b>." % (Q - W)) if Q != W else \
            tq("A gas absorbs 600 J of heat and does 600 J of work. What is the change in its internal energy?", "0 J", ["1200 J", "600 J", "−600 J"], "ΔU = Q − W = 0 (as in an isothermal change of an ideal gas).")
    if k == "W":
        p, v1 = ri(1, 5) * 1e5, rf(0.5, 4, 0.5)
        v2 = v1 + rf(0.5, 4, 0.5)
        return N("A gas expands at a constant pressure of %s Pa from %s m³ to %s m³. How much work does it do?" % (nf(p), nf(v1), nf(v2)), p * (v2 - v1), [p * v2, p * v1, p / (v2 - v1)], " J",
                 "W = pΔV = %s × %s = <b>%s J</b>." % (nf(p), nf(v2 - v1), nf(p * (v2 - v1))))
    if k == "carnot":
        T2 = ri(250, 400, 50)
        T1 = ri(T2 + 100, 1200, 100)
        return N("A Carnot engine works between %d K and %d K. What is its efficiency?" % (T1, T2), (1 - T2 / T1) * 100, [T2 / T1 * 100, (T1 - T2) / T2 * 100, (1 - T2 / T1)], "%",
                 "η = 1 − T₂/T₁ = 1 − %d/%d = <b>%s%%</b>." % (T2, T1, nf((1 - T2 / T1) * 100)))
    if k == "cop":
        T1, T2 = ri(295, 315, 5), ri(240, 275, 5)
        return N("An ideal refrigerator keeps its inside at %d K in a room at %d K. What is its coefficient of performance?" % (T2, T1), T2 / (T1 - T2), [T1 / (T1 - T2), (T1 - T2) / T2, T1 / T2], "",
                 "α = T₂/(T₁ − T₂) = %d/%d = <b>%s</b>." % (T2, T1 - T2, nf(T2 / (T1 - T2))))
    p = ch([("isothermal", "temperature"), ("isobaric", "pressure"), ("isochoric", "volume"), ("adiabatic", "no heat flows in or out")])
    return tq("What stays constant (or happens) in an %s process?" % p[0], p[1], [x[1] for x in [("i", "temperature"), ("i", "pressure"), ("i", "volume"), ("a", "no heat flows in or out")] if x[1] != p[1]],
              "In an %s process: %s." % (p[0], p[1]))


B11 = [("What does the zeroth law of thermodynamics lead to?", "the idea of temperature", ["the idea of entropy", "energy conservation", "the efficiency of engines"], "Bodies each in equilibrium with a third are in equilibrium with each other."),
       ("The first law of thermodynamics is a statement of…", "conservation of energy", ["conservation of momentum", "increase of entropy", "zero temperature"], "Q = ΔU + W."),
       ("For an ideal gas, internal energy depends only on…", "temperature", ["pressure", "volume", "shape of the container"], "So ΔU = 0 in an isothermal change."),
       ("In which process is no work done by a gas?", "isochoric (constant volume)", ["isobaric", "isothermal", "adiabatic"], "W = pΔV = 0."),
       ("Why does a gas cool when it expands adiabatically?", "it does work using its own internal energy", ["heat leaves it", "pressure rises", "it gains energy"], "Q = 0, so ΔU = −W."),
       ("Can a heat engine have 100% efficiency?", "no, the second law forbids it", ["yes, if it is ideal", "yes, at high temperature", "only a Carnot engine"], "Some heat must go to the cold reservoir."),
       ("What does the Kelvin–Planck statement say?", "no engine can convert all the heat it takes in into work", ["heat flows from cold to hot by itself", "energy is created", "work is always zero"], "A form of the second law."),
       ("What does the Clausius statement say?", "heat cannot flow from a colder to a hotter body by itself", ["all heat becomes work", "temperature is energy", "energy is not conserved"], "A refrigerator needs work to do it."),
       ("Which engine is the most efficient between two given temperatures?", "a reversible Carnot engine", ["a diesel engine", "a petrol engine", "a steam engine"], "Carnot's theorem."),
       ("On a p–V diagram, what gives the work done by a gas?", "the area under the curve", ["the slope", "the intercept", "the length of the curve"], "W = ∫p dV."),
       ("What is a quasi-static process?", "an infinitely slow process in which the system stays almost in equilibrium", ["a very fast process", "an explosion", "a process with no heat"], "Needed for a reversible process."),
       ("What is the ratio γ = C<sub>p</sub>/C<sub>v</sub> for a monatomic ideal gas?", "5/3", ["7/5", "4/3", "1"], "C<sub>v</sub> = 3R/2, C<sub>p</sub> = 5R/2."),
       ("Why is C<sub>p</sub> greater than C<sub>v</sub> for a gas?", "at constant pressure the gas also does work as it expands", ["the gas is heavier", "pressure is lower", "it is not; they are equal"], "C<sub>p</sub> − C<sub>v</sub> = R (Mayer's relation)."),
       ("What is the equation for an adiabatic change of an ideal gas?", "pV<sup>γ</sup> = constant", ["pV = constant", "p/T = constant", "V/T = constant"], "γ = C<sub>p</sub>/C<sub>v</sub>.")]


# =================================================================== 12 kinetic theory
DOF = [("a monatomic gas such as helium", "3 (translational only)"), ("a rigid diatomic gas such as oxygen", "5 (3 translational + 2 rotational)"), ("a rigid non-linear polyatomic gas such as methane", "6 (3 translational + 3 rotational)")]
B12 = [("How many degrees of freedom does %s have at ordinary temperatures?" % a, b, [x for x in ["3", "5", "6", "7"] if x != b][:3], "Translational and rotational motions each count.") for a, b in [(x, y.split()[0]) for x, y in DOF]] + [("According to kinetic theory, what is the pressure of a gas due to?", "molecules hitting the walls and changing momentum", ["the weight of the gas", "attraction between molecules", "heat"], "p = ⅓ρv²<sub>rms</sub>."),
       ("The average kinetic energy of a gas molecule depends only on…", "absolute temperature", ["pressure", "volume", "the type of container"], "Average KE = (3/2)kT."),
       ("What happens to the rms speed if the absolute temperature is made four times?", "it doubles", ["it becomes four times", "it halves", "it stays the same"], "v<sub>rms</sub> ∝ √T."),
       ("What does the law of equipartition of energy say?", "each degree of freedom has an average energy of ½kT", ["all molecules have equal speeds", "energy is lost in collisions", "pressure is constant"], "Applied to translational, rotational and vibrational motion."),
       ("What is the mean free path?", "the average distance a molecule travels between collisions", ["the size of a molecule", "the length of the container", "the speed of a molecule"], "It is longer at low pressure."),
       ("What is Avogadro's number?", "6.02 × 10²³ per mole", ["6.02 × 10⁻²³", "8.31", "1.38 × 10⁻²³"], "Particles in one mole."),
       ("What is the Boltzmann constant k?", "R/N<sub>A</sub> = 1.38 × 10⁻²³ J/K", ["8.31 J mol⁻¹ K⁻¹", "6.63 × 10⁻³⁴ J s", "9.8 N/kg"], "Gas constant per molecule."),
       ("Under which conditions do real gases behave most like an ideal gas?", "low pressure and high temperature", ["high pressure and low temperature", "low pressure and low temperature", "always"], "Molecules are far apart and fast."),
       ("Equal volumes of all gases at the same temperature and pressure contain…", "equal numbers of molecules", ["equal masses", "equal densities", "equal speeds"], "Avogadro's hypothesis."),
       ("What is the molar volume of an ideal gas at STP (273 K, 1 atm)?", "about 22.4 L", ["about 1 L", "about 8.31 L", "about 100 L"], "pV = nRT."),
       ("Which law relates the total pressure of a gas mixture to the pressures of its parts?", "Dalton's law of partial pressures", ["Boyle's law", "Charles's law", "Graham's law"], "p = p₁ + p₂ + …"),
       ("What does C<sub>v</sub> equal for one mole of a monatomic ideal gas?", "(3/2)R", ["(5/2)R", "3R", "R"], "Three translational degrees of freedom.")]


# =================================================================== 13 oscillations
def sh(k=None):
    k = k or ch(["wT", "v", "phase", "spring2", "pend2"])
    if k == "wT":
        T = ch([0.1, 0.2, 0.25, 0.4, 0.5, 0.8, 1, 1.25, 2, 2.5, 4, 5])
        return N("An oscillator has a period of %s s. What is its angular frequency?" % nf(T), 2 * math.pi / T, [1 / T, 2 * math.pi * T, math.pi / T], " rad/s", "ω = 2π/T = <b>%s rad/s</b>." % nf(2 * math.pi / T))
    if k == "v":
        A, w = ch([0.05, 0.1, 0.2, 0.25]), ri(2, 20)
        x = round(A * ch([0.6, 0.8]), 4)
        v = w * math.sqrt(A * A - x * x)
        return N("A particle in SHM has amplitude %s m and ω = %d rad/s. What is its speed when x = %s m?" % (nf(A), w, nf(x)), v, [w * A, w * x, w * (A - x)], " m/s",
                 "v = ω√(A² − x²) = %d × √(%s − %s) = <b>%s m/s</b>." % (w, nf(A * A), nf(x * x), nf(v)))
    if k == "spring2":
        f = ch([4, 9, 16, 25, 2, 3, 36, 0.25])
        return N("The mass on a spring is made %d times as large. By what factor does the period change?" % f, math.sqrt(f), [f, f * f, 1 / math.sqrt(f)], " times",
                 "T = 2π√(m/k) ∝ √m, so the period becomes √%d = <b>%s times</b>." % (f, nf(math.sqrt(f))))
    if k == "pend2":
        L = rf(0.2, 3, 0.1)
        T = 2 * math.pi * math.sqrt(L / 1.6)
        return N("What is the period of a %s m simple pendulum on the Moon (g = 1.6 m/s²)?" % nf(L), T, [2 * math.pi * math.sqrt(L / 9.8), 2 * math.pi * L / 1.6, math.sqrt(L / 1.6)], " s", "T = 2π√(L/g) = <b>%s s</b>." % nf(T))
    ph = ch([("x = A", "zero", "maximum"), ("x = 0", "maximum", "zero")])
    return tq("In SHM, what is the acceleration of the particle at %s?" % ph[0], ph[2], [ph[1], "equal to g", "equal to the velocity"], "a = −ω²x, so it is %s at %s." % (ph[2], ph[0]))


B13 = [("What is the condition for simple harmonic motion?", "acceleration is proportional to displacement and directed towards the mean position", ["acceleration is constant", "velocity is constant", "displacement is constant"], "a = −ω²x."),
       ("Where is the speed of a particle in SHM greatest?", "at the mean position", ["at the extreme positions", "halfway", "everywhere the same"], "All the energy is kinetic there."),
       ("Does the period of a simple pendulum depend on the mass of the bob?", "no", ["yes, heavier bobs swing faster", "yes, lighter bobs swing faster", "only for large amplitudes"], "T = 2π√(L/g)."),
       ("What happens to the period of a pendulum taken to the Moon?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "g is smaller there."),
       ("What is the length of a seconds pendulum (period 2 s) on the Earth?", "about 1 m", ["about 2 m", "about 0.5 m", "about 9.8 m"], "L = gT²/4π² ≈ 0.99 m."),
       ("In SHM, total mechanical energy is…", "constant and equal to ½kA²", ["zero", "greatest at the mean position only", "proportional to x"], "KE and PE keep exchanging."),
       ("What is the phase difference between displacement and velocity in SHM?", "π/2", ["π", "zero", "2π"], "v = Aω cos ωt when x = A sin ωt."),
       ("What is the phase difference between displacement and acceleration in SHM?", "π", ["π/2", "zero", "π/4"], "a = −ω²x."),
       ("What is periodic motion?", "motion that repeats after equal intervals of time", ["motion in a straight line", "motion with constant speed", "random motion"], "SHM is a special case."),
       ("Is uniform circular motion simple harmonic?", "no, but its projection on a diameter is", ["yes", "only for small circles", "never related"], "The shadow of a particle on a circle moves in SHM."),
       ("What is the frequency of oscillation of kinetic energy in SHM of frequency f?", "2f", ["f", "f/2", "4f"], "KE is maximum twice in each cycle."),
       ("What is the SI unit of the spring constant?", "N/m", ["N m", "J", "kg"], "F = −kx.")]


# =================================================================== 14 waves
def wv(k=None):
    k = k or ch(["str", "open", "closed", "beat", "air"])
    if k == "str":
        T, mu = ri(20, 200, 10), ch([0.001, 0.002, 0.005, 0.01, 0.02])
        return N("A string under a tension of %d N has a mass per unit length of %s kg/m. What is the speed of a transverse wave on it?" % (T, nf(mu)), math.sqrt(T / mu), [T / mu, math.sqrt(T * mu), math.sqrt(mu / T)], " m/s",
                 "v = √(T/μ) = <b>%s m/s</b>." % nf(math.sqrt(T / mu)))
    if k in ("open", "closed"):
        L = ch([0.17, 0.25, 0.34, 0.4, 0.5, 0.68, 0.8, 0.85, 1, 1.7])
        v = 340
        f = v / (2 * L) if k == "open" else v / (4 * L)
        return N("What is the fundamental frequency of a pipe %s m long, %s? (speed of sound 340 m/s)" % (nf(L), "open at both ends" if k == "open" else "closed at one end"), f,
                 [v / (4 * L) if k == "open" else v / (2 * L), v / L, v * L], " Hz", "%s: f = v/(%sL) = <b>%s Hz</b>." % ("Open pipe" if k == "open" else "Closed pipe", "2" if k == "open" else "4", nf(f)))
    if k == "beat":
        f1 = ch([256, 288, 320, 384, 440, 480, 512])
        f2 = f1 + ch([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
        return N("Two tuning forks of %d Hz and %d Hz are sounded together. How many beats are heard each second?" % (f1, f2), abs(f1 - f2), [f1 + f2, (f1 + f2) // 2, abs(f1 - f2) * 2], "",
                 "Beat frequency = |f₁ − f₂| = <b>%d</b>." % abs(f1 - f2))
    T = ri(280, 420, 10)
    return N("The speed of sound in air is 332 m/s at 273 K. What is it at %d K?" % T, 332 * math.sqrt(T / 273), [332 * T / 273, 332 + 0.61 * (T - 273) * 10, 332 * math.sqrt(273 / T)], " m/s",
             "v ∝ √T, so v = 332 × √(%d/273) = <b>%s m/s</b>." % (T, nf(332 * math.sqrt(T / 273)))) if T != 273 else None


B14 = [("What kind of wave is sound in air?", "longitudinal", ["transverse", "electromagnetic", "stationary only"], "Air particles move along the direction of the wave."),
       ("What kind of wave travels on a stretched string?", "transverse", ["longitudinal", "electromagnetic", "sound"], "Particles move at right angles to the wave."),
       ("Can sound travel through a vacuum?", "no, it needs a medium", ["yes", "only at night", "only high notes"], "Mechanical waves need matter."),
       ("What is the distance between two neighbouring nodes in a stationary wave?", "λ/2", ["λ", "λ/4", "2λ"], "A node and the next antinode are λ/4 apart."),
       ("Which harmonics are present in a pipe closed at one end?", "only odd harmonics", ["only even harmonics", "all harmonics", "no harmonics"], "f, 3f, 5f, …"),
       ("Which harmonics are present in a pipe open at both ends?", "all harmonics", ["only odd harmonics", "only even harmonics", "only the fundamental"], "f, 2f, 3f, …"),
       ("What happens when a wave is reflected at a fixed end?", "it suffers a phase change of π", ["no phase change", "it disappears", "its frequency doubles"], "A crest returns as a trough."),
       ("What are beats?", "regular rise and fall of loudness when two close frequencies are heard together", ["echoes", "very loud sounds", "high-pitched sounds"], "Used to tune instruments."),
       ("Does the speed of sound in air depend on pressure (at constant temperature)?", "no", ["yes, it increases with pressure", "yes, it decreases", "only in water"], "p/ρ stays constant."),
       ("How does humidity affect the speed of sound?", "humid air is less dense, so sound travels faster", ["it slows sound", "no effect", "it stops sound"], "Water vapour is lighter than dry air."),
       ("Who corrected Newton's formula for the speed of sound in air?", "Laplace", ["Doppler", "Huygens", "Bernoulli"], "He used the adiabatic modulus γp."),
       ("What is the principle of superposition of waves?", "the resultant displacement is the sum of the individual displacements", ["waves cancel always", "waves bounce off each other", "only one wave exists at a time"], "It explains interference and beats.")]


def UNITS():
    b = {k: B(v) for k, v in [(1, B1), (2, B2), (3, B3), (4, B4), (5, B5), (6, B6), (7, B7), (9, B9), (10, B10), (11, B11), (12, B12), (13, B13), (14, B14)]}
    dim = pairs(DIM2, "What is the dimensional formula of %s?", "Which quantity has the dimensional formula %s?")
    si = pairs(SI, "What is the SI base unit of %s?", "The %s is the SI base unit of which quantity?")
    pref = pairs([(x, y, "%s stands for %s." % (x, y)) for x, y in PREF], "What power of ten does the prefix %s stand for?", "Which SI prefix stands for %s?")
    K = lambda f, *k: (lambda: f(ch(k)))
    return [
        SU(PH, 1, "units-and-measurements", 1,
           "The international system of units; measurement of length, mass and time; accuracy and precision of instruments; errors in measurement; significant figures; dimensions of physical quantities, dimensional formulae and dimensional analysis and its applications.",
           "Units and Measurements", "units and measurements",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 1 Units and Measurements: SI units, prefixes, significant figures, errors, unit conversion and dimensional analysis. 100 questions with answers.",
           "Every measurement = number × unit, with an error.", "Check formulae with dimensions [M L T].",
           "<p>SI has seven base units: metre, kilogram, second, ampere, kelvin, mole and candela; all others are derived. Every measurement has an uncertainty: random errors fall when we average many readings, systematic errors (such as a zero error) do not. Significant figures show how precisely a value is known.</p>"
           "<p>Relative errors add when quantities are multiplied or divided, and multiply by n for a power n. Dimensions write a quantity in terms of M, L and T: force is [M L T⁻²]. A formula must have the same dimensions on both sides, but dimensions cannot find pure numbers like 2π.</p>",
           [("Significant figures in 0.02040?", ["leading zeros do not count", "2, 0, 4, 0"], "4"), ("% error in V = r³ if r has 1% error?", ["3 × 1%"], "3%")],
           ["Counting leading zeros as significant.", "Adding absolute errors instead of relative errors in a product.", "Thinking dimensional analysis proves a formula right."],
           [("What are the seven SI base units?", "Metre, kilogram, second, ampere, kelvin, mole and candela."),
            ("How do errors combine in a product?", "The relative (percentage) errors add: if Z = AB, ΔZ/Z = ΔA/A + ΔB/B.")],
           lambda: [("SI units and prefixes", [(si, 8), (pref, 12)]), ("Significant figures", [(u_sf, 16), (b[1], 4)]), ("Errors in measurement", [(K(u_err, "pct", "prod", "pow"), 14), (K(u_err, "mean"), 4), (b[1], 2)]),
                    ("Dimensions", [(dim, 16), (b[1], 4)]), ("Unit conversion and mixed problems", [(u_conv, 14), (b[1], 4), (u_sf, 2)])]),
        SU(PH, 2, "motion-in-a-straight-line", 2,
           "Frame of reference, motion in a straight line, elementary concepts of differentiation and integration for describing motion, uniform and non-uniform motion, average speed and instantaneous velocity, uniformly accelerated motion, velocity–time and position–time graphs, relations for uniformly accelerated motion, relative velocity.",
           "Motion in a Straight Line", "motion in a straight line",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 2 Motion in a Straight Line: average speed and velocity, equations of motion, free fall, graphs and relative velocity. 100 questions with answers.",
           "v = u + at, s = ut + ½at², v² = u² + 2as.", "Slope of x–t is v; slope of v–t is a; area under v–t is s.",
           "<p>Displacement is the change of position; distance is the length of the path. Average velocity = displacement ÷ time, average speed = distance ÷ time. For uniform acceleration: v = u + at, s = ut + ½at² and v² = u² + 2as. In free fall a = g = 9.8 m/s² downwards.</p>"
           "<p>On a position–time graph the slope is the velocity; on a velocity–time graph the slope is the acceleration and the area is the displacement. Relative velocity of B with respect to A is v<sub>B</sub> − v<sub>A</sub>.</p>",
           [("u = 0, a = 2 m/s², t = 5 s. Find s.", ["s = ½ × 2 × 25"], "25 m"), ("Average speed: 30 km/h there, 60 km/h back?", ["2 × 30 × 60 ÷ 90"], "40 km/h")],
           ["Taking the simple mean of two speeds over equal distances.", "Saying acceleration is zero at the top of a throw.", "Mixing up distance and displacement."],
           [("What does the area under a v–t graph give?", "The displacement in that time."), ("What is relative velocity?", "The velocity of one body as seen from another: v<sub>BA</sub> = v<sub>B</sub> − v<sub>A</sub>.")],
           lambda: [("Speed, velocity and graphs", [(b[2], 5), (K(s_avg, "speed", "vel"), 15)]), ("Equations of motion", [(A(P.m_suvat, "v", "s"), 12), (A(P.m_suvat, "a"), 8)]),
                    ("Free fall", [(K(s_avg, "fall"), 6), (A(P.m_suvat, "t"), 6), (b[2], 3), (K(s_avg, "stop"), 5)]), ("Average speed and stopping", [(K(s_avg, "two", "stop"), 17), (b[2], 3)]),
                    ("Relative velocity and mixed problems", [(K(s_avg, "rel"), 12), (b[2], 3), (A(P.m_suvat, "v", "s", "a"), 5)])]),
        SU(PH, 3, "motion-in-a-plane", 3,
           "Scalar and vector quantities, position and displacement vectors, general vectors and notation, equality of vectors, multiplication of vectors by a real number, addition and subtraction of vectors, unit vectors, resolution of a vector, rectangular components, motion in a plane, projectile motion, uniform circular motion.",
           "Motion in a Plane", "motion in a plane",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 3 Motion in a Plane: vectors, resolution, projectile motion (height, time and range), relative velocity and uniform circular motion. 100 questions with answers.",
           "Treat horizontal and vertical motion separately.", "R = u² sin 2θ/g; H = u² sin²θ/2g; a = v²/r.",
           "<p>Vectors add by the triangle or parallelogram law and can be resolved into components A cos θ and A sin θ. Two perpendicular vectors give a resultant √(a² + b²). In projectile motion the horizontal velocity u cos θ stays constant while the vertical motion has acceleration g.</p>"
           "<p>Time of flight T = 2u sin θ/g, maximum height H = u² sin²θ/(2g) and range R = u² sin 2θ/g, greatest at 45°. In uniform circular motion speed is constant but the acceleration v²/r = ω²r points to the centre.</p>",
           [("u = 20 m/s, θ = 45°. Range?", ["400 × 1 ÷ 9.8"], "40.8 m"), ("3 N and 4 N at right angles?", ["√(9 + 16)"], "5 N")],
           ["Using sin θ instead of sin 2θ for the range.", "Thinking velocity is zero at the top of a projectile.", "Calling uniform circular motion unaccelerated."],
           [("Which angle gives the maximum range?", "45°, because sin 2θ is then 1."), ("Why is uniform circular motion accelerated?", "The direction of velocity keeps changing; the centripetal acceleration v²/r points to the centre.")],
           lambda: [("Vectors", [(K(pl, "res", "comp"), 16), (b[3], 4)]), ("Projectiles: height and time", [(K(pl, "H", "T"), 16), (b[3], 4)]), ("Projectiles: range", [(K(pl, "R"), 10), (A(P.m_proj, "t", "x", "vy"), 10)]),
                    ("Uniform circular motion", [(K(pl, "circ", "w"), 16), (b[3], 4)]), ("Relative velocity and mixed problems", [(K(pl, "river"), 10), (A(P.m_proj, "angle"), 6), (K(pl, "R", "H"), 4)])]),
        SU(PH, 4, "laws-of-motion", 4,
           "Intuitive concept of force, inertia, Newton's first law of motion, momentum and Newton's second law of motion, impulse, Newton's third law, law of conservation of linear momentum and its applications, equilibrium of concurrent forces, static and kinetic friction, laws of friction, rolling friction, lubrication, dynamics of uniform circular motion, centripetal force, examples of circular motion.",
           "Laws of Motion", "laws of motion",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 4 Laws of Motion: Newton's laws, impulse, conservation of momentum, friction, lifts, pulleys and centripetal force. 100 questions with answers.",
           "F = ma = Δp/Δt.", "Action and reaction act on different bodies.",
           "<p>Newton's first law describes inertia. The second law says the net force equals the rate of change of momentum, F = ma. Impulse FΔt equals the change in momentum, so a longer stopping time means a smaller force. The third law pairs act on different bodies; with no external force, total momentum is conserved.</p>"
           "<p>Limiting friction is μN; kinetic friction is a little less. In a lift accelerating upward the reading is m(g + a). On a curve, friction or banking supplies the centripetal force mv²/r.</p>",
           [("10 kg, μ = 0.3. Force to start sliding?", ["0.3 × 10 × 9.8"], "29.4 N"), ("4 kg gun, 0.02 kg bullet at 400 m/s. Recoil?", ["0.02 × 400 ÷ 4"], "2 m/s")],
           ["Thinking action and reaction cancel.", "Forgetting that friction depends on the normal force, not area.", "Using mg as the reading in an accelerating lift."],
           [("Why do we pull our hands back when catching a ball?", "It increases the time of impact, so the force F = Δp/Δt is smaller."),
            ("What is the law of conservation of momentum?", "With no external force, the total momentum of a system stays constant.")],
           lambda: [("Newton's first and second laws", [(K(lm, "Fma"), 12), (b[4], 8)]), ("Impulse and momentum", [(K(lm, "imp", "recoil"), 12), (A(P.m_momentum, "stick", "p"), 8)]),
                    ("Friction", [(K(lm, "fric"), 12), (b[4], 5), (K(lm, "Fma"), 3)]), ("Lifts and pulleys", [(K(lm, "lift", "atw"), 20)]),
                    ("Circular motion and mixed problems", [(K(lm, "circ"), 12), (K(lm, "fric", "recoil", "atw"), 8)])]),
        SU(PH, 5, "work-energy-and-power", 5,
           "Work done by a constant force and a variable force, kinetic energy, work–energy theorem, power, potential energy, potential energy of a spring, conservative forces, conservation of mechanical energy, non-conservative forces, motion in a vertical circle, elastic and inelastic collisions in one and two dimensions.",
           "Work, Energy and Power", "work, energy and power",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 5 Work, Energy and Power: work by a force, kinetic and potential energy, springs, power, conservation of energy and collisions. 100 questions with answers.",
           "W = Fd cos θ; W(net) = ΔK.", "Momentum is conserved in all collisions; KE only in elastic ones.",
           "<p>Work W = Fd cos θ is zero when the force is perpendicular to the motion. The work–energy theorem says the net work equals the change in kinetic energy ½mv². Potential energy is mgh near the Earth and ½kx² for a spring. Without friction, mechanical energy is conserved.</p>"
           "<p>Power is the rate of doing work, P = W/t = Fv (1 hp = 746 W). In every collision momentum is conserved; kinetic energy is conserved only in elastic collisions. Equal masses in an elastic head-on collision exchange velocities.</p>",
           [("k = 200 N/m, x = 0.1 m. Energy stored?", ["½ × 200 × 0.01"], "1 J"), ("F = 1000 N at 20 m/s. Power?", ["P = Fv"], "20,000 W")],
           ["Using Fd when the force is at an angle.", "Thinking kinetic energy is conserved in all collisions.", "Doubling KE when speed doubles (it becomes four times)."],
           [("What is the work–energy theorem?", "The work done by the net force on a body equals its change in kinetic energy."),
            ("What is an elastic collision?", "A collision in which both momentum and kinetic energy are conserved.")],
           lambda: [("Work done by a force", [(K(we, "W"), 15), (b[5], 5)]), ("Kinetic and potential energy", [(A(P.m_energy, "ke", "gpe"), 12), (K(we, "spring"), 8)]),
                    ("Conservation of energy", [(A(P.m_energy, "v"), 6), (K(we, "pe2"), 10), (b[5], 4)]), ("Power and efficiency", [(A(P.m_energy, "power", "eff"), 12), (K(we, "Fv"), 8)]),
                    ("Collisions", [(K(we, "elastic"), 10), (b[5], 3), (A(P.m_momentum, "stick"), 7)])]),
        SU(PH, 6, "system-of-particles-and-rotational-motion", 6,
           "Centre of mass of a two-particle system and a rigid body, momentum conservation and centre of mass motion, moment of a force, torque, angular momentum, law of conservation of angular momentum and its applications, equilibrium of rigid bodies, rigid body rotation and equations of rotational motion, moment of inertia, radius of gyration, values of moments of inertia for simple geometrical objects.",
           "System of Particles and Rotational Motion", "rotational motion",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 6 System of Particles and Rotational Motion: centre of mass, torque, moment of inertia, angular momentum, rolling and conservation of angular momentum. 100 questions with answers.",
           "τ = Iα; L = Iω; K(rot) = ½Iω².", "With no external torque, Iω stays constant.",
           "<p>The centre of mass of two masses lies on the line joining them, closer to the heavier one: x = m₂d/(m₁ + m₂). Torque τ = rF sin θ turns a body; moment of inertia I (ring MR², disc ½MR², solid sphere 2/5 MR², rod about its centre ML²/12) resists that turning.</p>"
           "<p>Angular momentum L = Iω is conserved when no external torque acts, so a skater who pulls in her arms spins faster. Rotational kinetic energy is ½Iω². A rolling body has both translational and rotational energy, so a solid sphere rolls down a slope faster than a ring.</p>",
           [("1 kg and 3 kg, 4 m apart. CM from 1 kg?", ["3 × 4 ÷ 4"], "3 m"), ("Disc, M = 2 kg, R = 0.5 m. I?", ["½ × 2 × 0.25"], "0.25 kg m²")],
           ["Thinking the centre of mass must be inside the body.", "Using MR² for every shape.", "Forgetting sin θ in torque."],
           [("When is angular momentum conserved?", "When the net external torque on the system is zero."),
            ("What is the theorem of parallel axes?", "I = I<sub>cm</sub> + Md², where d is the distance between the parallel axes.")],
           lambda: [("Centre of mass", [(K(ro, "cm"), 16), (b[6], 4)]), ("Torque and equilibrium", [(K(ro, "tq"), 14), (b[6], 2), (A(P.m_moment), 4)]), ("Moment of inertia", [(K(ro, "I"), 18), (b[6], 2)]),
                    ("Angular momentum", [(K(ro, "L", "cons"), 18), (b[6], 2)]), ("Rotational energy and rolling", [(K(ro, "Krot"), 12), (K(ro, "roll"), 1), (b[6], 1), (K(ro, "I"), 6)])]),
        SU(PH, 7, "gravitation", 7,
           "Kepler's laws of planetary motion, universal law of gravitation, acceleration due to gravity and its variation with altitude and depth, gravitational potential energy and gravitational potential, escape speed, orbital velocity of a satellite.",
           "Gravitation", "gravitation",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 7 Gravitation: Kepler's laws, Newton's law of gravitation, g with height and depth, potential energy, orbital and escape speed. 100 questions with answers.",
           "F = Gm₁m₂/r².", "Escape speed √(2gR); orbital speed √(gR) near the surface.",
           "<p>Kepler found that planets move in ellipses, sweep equal areas in equal times and have T² ∝ r³. Newton's law F = Gm₁m₂/r² explains them, with G = 6.67 × 10⁻¹¹ N m² kg⁻². At the surface g = GM/R² = 9.8 m/s²; it falls with height, g/(1 + h/R)², and with depth, g(1 − d/R).</p>"
           "<p>Gravitational potential energy is −GMm/r. A body must reach the escape speed √(2gR) ≈ 11.2 km/s to leave the Earth, while a satellite close to the surface needs √(gR) ≈ 7.9 km/s. Geostationary satellites orbit once in 24 hours.</p>",
           [("g at height R?", ["9.8/2²"], "2.45 m/s²"), ("Orbit 4 times Earth's radius. Period?", ["4^(3/2)"], "8 years")],
           ["Thinking there is no gravity on astronauts in orbit.", "Using g(1 − d/R) for height.", "Thinking escape speed depends on the body's mass."],
           [("Why do astronauts feel weightless?", "They and their spacecraft fall freely together around the Earth."),
            ("What is Kepler's third law?", "The square of a planet's period is proportional to the cube of its mean distance from the Sun: T² ∝ r³.")],
           lambda: [("Kepler's laws", [(K(gr, "kep"), 7), (b[7], 9), (K(gr, "weight"), 4)]), ("The law of gravitation", [(A(P.f_grav, "F"), 14), (b[7], 2), (K(gr, "weight"), 4)]),
                    ("g with height and depth", [(K(gr, "gh", "depth"), 12), (A(P.f_grav, "g", "h"), 8)]), ("Satellites and escape speed", [(A(P.f_grav, "orbitv", "orbitT"), 15), (K(gr, "esc"), 2), (A(P.f_grav, "V"), 3)]),
                    ("Mixed problems", [(A(P.f_grav, "F", "g", "orbitv"), 20)])]),
        SU(PH, 8, "mechanical-properties-of-solids", 8,
           "Elasticity, stress–strain relationship, Hooke's law, Young's modulus, bulk modulus, shear modulus of rigidity (qualitative idea only), Poisson's ratio, elastic energy.",
           "Mechanical Properties of Solids", "mechanical properties of solids",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 8 Mechanical Properties of Solids: stress, strain, Hooke's law, Young's modulus, elastic energy and the stress–strain curve. 100 questions with answers.",
           "Stress = F/A; strain = ΔL/L; Y = stress/strain.", "Hooke's law holds up to the limit of proportionality.",
           "<p>When a force deforms a body, stress = F/A and strain = ΔL/L. Within the elastic limit stress is proportional to strain (Hooke's law), and the constant is a modulus: Young's modulus Y for stretching, bulk modulus B for change of volume and shear modulus G for twisting. Steel has a larger Y than rubber, so it is more elastic.</p>"
           "<p>The elastic potential energy stored in a stretched wire is ½ × stress × strain × volume. On a stress–strain curve we find the proportional limit, yield point, ultimate strength and fracture point. Poisson's ratio is lateral strain ÷ longitudinal strain.</p>",
           [("Stress 2 × 10⁸ Pa, strain 0.001. Y?", ["stress ÷ strain"], "2 × 10¹¹ Pa"), ("Steel or rubber: more elastic?", ["larger Y"], "steel")],
           ["Thinking rubber is more elastic than steel.", "Using the diameter as radius in the area.", "Forgetting to convert mm² to m²."],
           [("What is Young's modulus?", "The ratio of tensile stress to tensile strain within the limit of proportionality."),
            ("Why is steel more elastic than rubber?", "For the same stress, steel is strained much less, so its modulus is much greater.")],
           lambda: [("Stress and strain", [(A(P.m_materials, "stress", "strain"), 20)]), ("Hooke's law", [(A(P.m_materials, "hooke"), 16), (B(B8), 4)]), ("Young's modulus", [(A(P.m_materials, "E"), 20)]),
                    ("Elastic energy", [(A(P.m_materials, "energy"), 17), (B(B8), 3)]), ("Moduli and mixed problems", [(B(B8), 2), (A(P.m_materials, "E", "stress"), 18)])]),
        SU(PH, 9, "mechanical-properties-of-fluids", 9,
           "Pressure due to a fluid column, Pascal's law and its applications (hydraulic lift and hydraulic brakes), effect of gravity on fluid pressure, viscosity, Stokes' law, terminal velocity, streamline and turbulent flow, critical velocity, Bernoulli's theorem and its simple applications, surface energy and surface tension, angle of contact, excess of pressure across a curved surface, application of surface tension ideas to drops, bubbles and capillary rise.",
           "Mechanical Properties of Fluids", "mechanical properties of fluids",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 9 Mechanical Properties of Fluids: pressure, Pascal's law, continuity, Bernoulli's principle, viscosity, terminal velocity, surface tension and capillary rise. 100 questions with answers.",
           "p = ρgh; A₁v₁ = A₂v₂.", "Faster flow means lower pressure (Bernoulli).",
           "<p>Pressure in a liquid at depth h is ρgh above the surface pressure. Pascal's law lets a hydraulic lift multiply force: F₂ = F₁A₂/A₁. In steady flow A₁v₁ = A₂v₂, so liquid speeds up in a narrow pipe; Bernoulli's principle says the pressure there is lower.</p>"
           "<p>Viscosity is fluid friction; a small sphere reaches terminal velocity v = 2r²(ρ − σ)g/9η (Stokes' law). Surface tension pulls drops into spheres; the excess pressure is 2T/r in a drop and 4T/r in a bubble, and water rises h = 2T cos θ/(rρg) in a capillary.</p>",
           [("10 m of water. Pressure?", ["1000 × 9.8 × 10"], "98,000 Pa"), ("F₁ = 100 N, A₂/A₁ = 100. F₂?", ["100 × 100"], "10,000 N")],
           ["Forgetting the 2 in 2T/r for a drop.", "Thinking pressure is higher where flow is faster.", "Leaving cm² unconverted in Pascal's law (only the ratio matters)."],
           [("What is Bernoulli's principle?", "Along a streamline p + ½ρv² + ρgh is constant, so where a fluid flows faster its pressure is lower."),
            ("Why does water rise in a thin glass tube?", "Surface tension and adhesion to glass pull it up: h = 2T cos θ/(rρg).")],
           lambda: [("Pressure in fluids", [(K(fl, "P"), 16), (b[9], 4)]), ("Pascal's law", [(K(fl, "hyd"), 17), (b[9], 3)]), ("Flow and Bernoulli", [(K(fl, "cont"), 18), (b[9], 2)]),
                    ("Viscosity", [(K(fl, "term"), 12), (b[9], 2), (K(fl, "P", "hyd"), 6)]), ("Surface tension", [(K(fl, "cap", "drop"), 18), (K(fl, "term"), 2)])]),
        SU(PH, 10, "thermal-properties-of-matter", 10,
           "Heat, temperature, thermal expansion of solids, liquids and gases, anomalous expansion of water, specific heat capacity, Cp and Cv, calorimetry, change of state, latent heat capacity, heat transfer by conduction, convection and radiation, thermal conductivity, qualitative ideas of black body radiation, Wien's displacement law, Stefan's law.",
           "Thermal Properties of Matter", "thermal properties of matter",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 10 Thermal Properties of Matter: temperature scales, thermal expansion, specific heat, calorimetry, latent heat, conduction and radiation laws. 100 questions with answers.",
           "Q = mcΔT; Q = mL.", "ΔL = αLΔT; γ = 3α.",
           "<p>Heat flows because of a temperature difference. Solids expand by ΔL = αLΔT, and the volume coefficient is about 3α. Water is unusual: it contracts when heated from 0 °C to 4 °C, so lakes freeze from the top. Heat needed to warm a body is mcΔT; to change its state at constant temperature it is mL.</p>"
           "<p>Heat moves by conduction (H = KAΔT/d), convection and radiation. A black body absorbs all radiation; it radiates power ∝ T⁴ (Stefan) and its peak wavelength obeys λ<sub>m</sub>T = 2.9 × 10⁻³ m K (Wien).</p>",
           [("2 kg water from 20 °C to 70 °C?", ["2 × 4186 × 50"], "4.19 × 10⁵ J"), ("Sun at 5800 K. Peak λ?", ["2.9 × 10⁻³ ÷ 5800"], "500 nm")],
           ["Adding 273 to temperature differences.", "Thinking temperature rises while water boils.", "Using α for volume expansion."],
           [("Why is water densest at 4 °C?", "Between 0 °C and 4 °C water contracts on heating (anomalous expansion), so it is densest at 4 °C."),
            ("What is Wien's displacement law?", "λ<sub>m</sub>T = constant (2.9 × 10⁻³ m K): hotter bodies radiate most strongly at shorter wavelengths.")],
           lambda: [("Temperature and expansion", [(K(th, "K", "lin", "area"), 17), (b[10], 3)]), ("Specific heat and calorimetry", [(A(P.t_heat, "Q", "dT", "mix"), 17), (b[10], 3)]),
                    ("Change of state", [(A(P.t_heat, "latent", "melt"), 9), (b[10], 2), (A(P.t_heat, "Q", "dT"), 9)]), ("Conduction", [(K(th, "cond"), 17), (b[10], 3)]), ("Radiation", [(K(th, "wien"), 6), (b[10], 1), (K(th, "lin", "cond"), 13)])]),
        SU(PH, 11, "thermodynamics", 11,
           "Thermal equilibrium and definition of temperature, zeroth law of thermodynamics, heat, work and internal energy, first law of thermodynamics, isothermal and adiabatic processes, second law of thermodynamics, reversible and irreversible processes, heat engines and refrigerators.",
           "Thermodynamics", "thermodynamics",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 11 Thermodynamics: zeroth and first laws, work done by a gas, isothermal and adiabatic processes, the second law, heat engines and refrigerators. 100 questions with answers.",
           "Q = ΔU + W.", "Carnot efficiency η = 1 − T₂/T₁ (in kelvin).",
           "<p>The zeroth law gives us temperature. The first law is energy conservation: heat supplied Q = ΔU + W, where W is the work done by the gas (pΔV at constant pressure). For an ideal gas ΔU depends only on temperature, so ΔU = 0 in an isothermal change; in an adiabatic change Q = 0 and pV<sup>γ</sup> is constant.</p>"
           "<p>The second law says no engine can turn all its heat into work and heat does not flow from cold to hot by itself. The best engine between T₁ and T₂ is a Carnot engine, η = 1 − T₂/T₁; an ideal refrigerator has coefficient of performance T₂/(T₁ − T₂).</p>",
           [("Q = 800 J, W = 300 J. ΔU?", ["800 − 300"], "500 J"), ("Carnot between 600 K and 300 K?", ["1 − 300/600"], "50%")],
           ["Using °C in the Carnot formula.", "Thinking an ideal engine can be 100% efficient.", "Confusing isothermal (ΔT = 0) and adiabatic (Q = 0)."],
           [("What is the first law of thermodynamics?", "Heat supplied to a system equals the increase in internal energy plus the work done by the system: Q = ΔU + W."),
            ("Why can no engine be 100% efficient?", "The second law says some heat must always be given out to a colder reservoir.")],
           lambda: [("The first law", [(K(td, "dU"), 17), (b[11], 3)]), ("Work done by a gas", [(K(td, "W"), 17), (b[11], 3)]), ("Thermodynamic processes", [(K(td, "iso"), 2), (b[11], 3), (K(td, "dU", "W"), 15)]),
                    ("Heat engines", [(K(td, "carnot"), 18), (b[11], 2)]), ("Refrigerators and mixed problems", [(K(td, "cop"), 14), (K(td, "carnot"), 4), (K(td, "W"), 2)])]),
        SU(PH, 12, "kinetic-theory", 12,
           "Equation of state of a perfect gas, work done in compressing a gas, kinetic theory of gases: assumptions, concept of pressure, kinetic interpretation of temperature, rms speed of gas molecules, degrees of freedom, law of equi-partition of energy and application to specific heat capacities of gases, concept of mean free path, Avogadro's number.",
           "Kinetic Theory", "kinetic theory",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 12 Kinetic Theory: the ideal gas equation, gas laws, pressure from molecules, rms speed, equipartition of energy and degrees of freedom. 100 questions with answers.",
           "pV = nRT = NkT.", "Average KE of a molecule = (3/2)kT.",
           "<p>An ideal gas obeys pV = nRT (R = 8.31 J mol⁻¹ K⁻¹), which includes Boyle's and Charles's laws. Kinetic theory explains pressure as molecules hitting the walls: p = ⅓ρv²<sub>rms</sub>. The average kinetic energy of a molecule is (3/2)kT, so temperature measures molecular motion.</p>"
           "<p>Each degree of freedom has an average energy of ½kT (equipartition). A monatomic gas has 3 and C<sub>v</sub> = 3R/2; a rigid diatomic gas has 5 and C<sub>v</sub> = 5R/2. The mean free path is the average distance between collisions.</p>",
           [("v(rms) when T becomes 4T?", ["v ∝ √T"], "doubles"), ("Degrees of freedom of O₂?", ["3 + 2"], "5")],
           ["Using °C instead of kelvin in pV = nRT.", "Thinking rms speed is proportional to T.", "Giving a diatomic gas 3 degrees of freedom."],
           [("How does kinetic theory explain temperature?", "The absolute temperature is proportional to the average kinetic energy of the molecules: (3/2)kT."),
            ("What is the law of equipartition of energy?", "In equilibrium each degree of freedom of a molecule has an average energy of ½kT.")],
           lambda: [("The ideal gas equation", [(A(P.t_gas, "pV", "n"), 17), (b[12], 3)]), ("Gas laws", [(A(P.t_gas, "boyle", "charles"), 17), (b[12], 3)]), ("Pressure and temperature", [(A(P.t_gas, "ke"), 6), (b[12], 2), (A(P.t_gas, "rms"), 12)]),
                    ("rms speed", [(A(P.t_gas, "rms"), 8), (b[12], 2), (A(P.t_gas, "boyle", "charles"), 10)]), ("Degrees of freedom and mixed problems", [(b[12], 2), (A(P.t_gas, "pV", "n", "rms"), 18)])]),
        SU(PH, 13, "oscillations", 13,
           "Periodic motion, time period, frequency, displacement as a function of time, periodic functions and their applications, simple harmonic motion and its equation, phase, oscillations of a loaded spring, restoring force and force constant, energy in SHM (kinetic and potential energies), simple pendulum and derivation of its time period.",
           "Oscillations", "oscillations",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 13 Oscillations: simple harmonic motion, period and frequency, spring–mass systems, simple pendulums, velocity and energy in SHM. 100 questions with answers.",
           "a = −ω²x in SHM.", "T = 2π√(m/k); T = 2π√(L/g).",
           "<p>Simple harmonic motion has an acceleration proportional to the displacement and directed towards the mean position: a = −ω²x, with x = A sin(ωt + φ) and ω = 2π/T. Speed is greatest (ωA) at the mean position and zero at the extremes; acceleration is the other way round.</p>"
           "<p>A mass on a spring has T = 2π√(m/k); a simple pendulum has T = 2π√(L/g), independent of the mass. The total energy ½kA² stays constant while kinetic and potential energy exchange.</p>",
           [("Spring: m = 0.5 kg, k = 200 N/m. T?", ["2π√(0.0025)"], "0.314 s"), ("Pendulum L = 1 m on Earth?", ["2π√(1/9.8)"], "2.01 s")],
           ["Thinking a heavier bob swings faster.", "Saying speed is greatest at the extremes.", "Mixing up ω and f (ω = 2πf)."],
           [("What is simple harmonic motion?", "Periodic motion in which the restoring acceleration is proportional to the displacement from the mean position and opposite to it."),
            ("Does a pendulum's period depend on its mass?", "No. For small swings T = 2π√(L/g) depends only on the length and g.")],
           lambda: [("Period and frequency", [(A(P.c_shm, "f"), 4), (K(sh, "wT"), 9), (b[13], 3), (K(sh, "v"), 4)]), ("Displacement, velocity and acceleration", [(K(sh, "v", "phase"), 10), (A(P.c_shm, "vmax", "amax", "x"), 10)]),
                    ("Spring–mass systems", [(A(P.c_shm, "spring"), 14), (K(sh, "spring2"), 4), (b[13], 2)]), ("Simple pendulums", [(A(P.c_shm, "pend"), 5), (K(sh, "pend2"), 15)]),
                    ("Energy in SHM and mixed problems", [(b[13], 4), (A(P.c_shm, "spring", "vmax"), 16)])]),
        SU(PH, 14, "waves", 14,
           "Wave motion, transverse and longitudinal waves, speed of travelling wave, displacement relation for a progressive wave, principle of superposition of waves, reflection of waves, standing waves in strings and organ pipes, fundamental mode and harmonics, beats.",
           "Waves", "waves",
           "Free CBSE Class 11 Physics worksheets for NCERT Chapter 14 Waves: transverse and longitudinal waves, v = fλ, wave speed on a string, sound in air, standing waves in strings and pipes, and beats. 100 questions with answers.",
           "v = fλ; on a string v = √(T/μ).", "Open pipe f = v/2L; closed pipe f = v/4L (odd harmonics only).",
           "<p>A wave carries energy without carrying matter. In transverse waves (strings) particles move at right angles to the wave; in longitudinal waves (sound) they move along it. For every wave v = fλ; on a string v = √(T/μ), and sound in air speeds up as √T.</p>"
           "<p>Waves superpose. Reflected waves form standing waves with nodes λ/2 apart. A string or open pipe has all harmonics f = nv/2L; a pipe closed at one end has only odd harmonics f = nv/4L. Two close frequencies give beats at |f₁ − f₂| per second.</p>",
           [("Closed pipe 0.85 m, v = 340 m/s?", ["340 ÷ (4 × 0.85)"], "100 Hz"), ("256 Hz and 260 Hz together?", ["260 − 256"], "4 beats/s")],
           ["Using v/2L for a closed pipe.", "Thinking sound travels in a vacuum.", "Thinking a closed pipe has even harmonics."],
           [("What are beats?", "Periodic changes in loudness when two sounds of slightly different frequency are heard together; the beat frequency is |f₁ − f₂|."),
            ("Why does a closed pipe give only odd harmonics?", "Its closed end must be a node and the open end an antinode, so L = λ/4, 3λ/4, 5λ/4, …")],
           lambda: [("Wave speed", [(A(P.w_vfl, "sound", "light", "water", "string"), 16), (b[14], 4)]), ("Waves on strings", [(K(wv, "str"), 14), (A(P.w_stationary), 6)]),
                    ("Sound in air", [(K(wv, "air"), 10), (b[14], 3), (A(P.w_vfl, "sound"), 7)]), ("Organ pipes", [(K(wv, "open", "closed"), 13), (K(wv, "beat"), 7)]), ("Beats and mixed problems", [(K(wv, "beat"), 8), (K(wv, "str"), 8), (b[14], 2), (K(wv, "air"), 2)])]),
    ]


B8 = [("Which material is more elastic, steel or rubber?", "steel", ["rubber", "both the same", "neither"], "Steel has a far greater Young's modulus."),
      ("What is the SI unit of stress?", "N/m² (pascal)", ["N", "N m", "no unit"], "Stress = force ÷ area."),
      ("What is the unit of strain?", "it has no unit", ["N/m²", "m", "N"], "It is a ratio of lengths."),
      ("What does Hooke's law state?", "within the elastic limit, stress is proportional to strain", ["stress is always equal to strain", "strain is zero", "stress is inversely proportional to strain"], "The constant is a modulus of elasticity."),
      ("Which modulus describes a change in volume?", "bulk modulus", ["Young's modulus", "shear modulus", "Poisson's ratio"], "B = −p/(ΔV/V)."),
      ("Which modulus describes a change of shape at constant volume?", "shear modulus (modulus of rigidity)", ["bulk modulus", "Young's modulus", "elastic limit"], "Shearing stress ÷ shearing strain."),
      ("What is Poisson's ratio?", "lateral strain ÷ longitudinal strain", ["stress ÷ strain", "force ÷ area", "longitudinal strain ÷ lateral strain"], "It has no unit."),
      ("Beyond which point on a stress–strain curve does a wire not return to its original length?", "the elastic limit (yield point)", ["the origin", "the proportional limit only", "it always returns"], "Beyond it the deformation is plastic."),
      ("What is the stress at which a wire breaks called?", "the fracture (breaking) point", ["the yield point", "Young's modulus", "the strain"], "Just before it is the ultimate tensile strength."),
      ("Why are bridges designed so that the stress stays well below the elastic limit?", "so that they do not deform permanently or break", ["to save steel", "to make them heavy", "for decoration"], "A safety factor is used."),
      ("Why are girders made with an I-shaped section?", "it resists bending well while using less material", ["it is easier to paint", "it is heavier", "it looks nice"], "Bending depends on depth more than width."),
      ("Which is the most compressible: a solid, a liquid or a gas?", "a gas", ["a solid", "a liquid", "all the same"], "Gases have the smallest bulk modulus.")]
