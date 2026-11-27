# -*- coding: utf-8 -*-
"""Year 12 Physics (Australian Curriculum: Senior Secondary Physics, Units 3 and 4) for au_sr.build."""
import math
from au_sr import SR, nq
from uk_alsci import nf

PH = "Physics"
C = 3.00e8
X10 = " × 10<sup>%s</sup>"
SPEEDS = [0.500, 0.600, 0.700, 0.750, 0.800, 0.850, 0.900, 0.950, 0.980, 0.990, 0.995]


def gam(b):
    return 1 / math.sqrt(1 - b * b)


def fmt(b):
    return ("%.3f" % b).rstrip("0").rstrip(".")


def rel_makers(R):
    def dilate():
        b = R.choice(SPEEDS)
        g = gam(b)
        k = R.choice(["t", "t0", "g"])
        if k == "g":
            return nq("Calculate the Lorentz factor γ for a speed of %sc." % fmt(b), g, [1 - b * b, math.sqrt(1 - b * b), 1 / (1 - b * b)], "",
                      "γ = 1 ÷ √(1 − v²/c²) = 1 ÷ √(1 − %s²) = <b>%.3g</b>." % (fmt(b), g))
        unit, thing, t0 = R.choice([(" s", "the interval between two ticks of a clock", R.choice([2.0, 5.0, 10, 30, 60])), (" h", "an astronaut's sleep", R.choice([6.0, 7.0, 8.0, 9.0])),
                                    (" years", "the journey", R.choice([2, 4, 5, 10, 12, 20, 30])), (" min", "an experiment", R.choice([15, 20, 30, 45, 90]))])
        if k == "t":
            return nq("A spacecraft moves at %sc relative to Earth. On board, %s lasts %s%s. How long does it last as measured from Earth?" % (fmt(b), thing, ("%g" % t0), unit),
                      t0 * g, [t0 / g, t0 * (1 - b * b), t0 * b], unit,
                      "Moving clocks run slow: t = γt₀ = %.3g × %g = <b>%.3g%s</b>." % (g, t0, t0 * g, unit))
        t = t0 * g
        return nq("Observers on Earth measure %s on a spacecraft moving at %sc as %.3g%s. What is the proper time measured on board?" % (thing, fmt(b), t, unit),
                  t0, [t * g, t, t * b], unit,
                  "Proper time t₀ = t ÷ γ = %.3g ÷ %.3g = <b>%.3g%s</b>." % (t, g, t0, unit))

    def contract():
        b = R.choice(SPEEDS)
        g = gam(b)
        L0 = R.choice([10, 20, 50, 80, 100, 120, 150, 200, 500])
        k = R.choice(["L", "L0"])
        if k == "L":
            return nq("A spacecraft is %d m long when at rest. How long is it measured by an observer it passes at %sc?" % (L0, fmt(b)), L0 / g,
                      [L0 * g, L0 * (1 - b * b), L0 * b], " m", "Length contracts along the motion: L = L₀ ÷ γ = %d ÷ %.3g = <b>%.3g m</b>." % (L0, g, L0 / g))
        L = L0 / g
        return nq("A rod moving at %sc is measured as %.3g m long. What is its proper (rest) length?" % (fmt(b), L), L0, [L / g, L * (1 - b * b), L * b], " m",
                  "L₀ = γL = %.3g × %.3g = <b>%.3g m</b>." % (g, L, L0))

    def muon():
        b = R.choice([0.980, 0.990, 0.995, 0.998])
        g = gam(b)
        t0 = 2.2e-6
        k = R.choice(["no", "yes"])
        d_no = b * C * t0
        d_yes = d_no * g
        if k == "no":
            return nq("A muon (lifetime 2.2 µs in its own frame) moves at %sc. Ignoring relativity, how far would it travel in one lifetime?" % fmt(b), d_no,
                      [d_yes, C * t0 / b, d_no / 1000], " m", "d = vt = %s × 3.00 × 10⁸ × 2.2 × 10⁻⁶ = <b>%.3g m</b>." % (fmt(b), d_no))
        return nq("A muon (lifetime 2.2 µs in its own frame) moves at %sc. Taking time dilation into account, how far does it travel, as measured from Earth, in one lifetime?" % fmt(b),
                  d_yes, [d_no, d_yes * g, d_no / g], " m", "Earth time = γt₀ = %.3g × 2.2 µs; d = v × γt₀ = <b>%.3g m</b>. This is why muons from the upper atmosphere reach the ground." % (g, d_yes))

    def energy():
        k = R.choice(["E", "m", "p"])
        if k == "E":
            m = R.choice([1.0e-3, 2.0e-3, 5.0e-3, 0.010, 0.10, 1.0, 9.11e-31, 1.67e-27])
            E = m * C * C
            nm = {9.11e-31: "an electron (9.11 × 10⁻³¹ kg)", 1.67e-27: "a proton (1.67 × 10⁻²⁷ kg)"}.get(m, "%g kg of matter" % m)
            return nq("Calculate the rest energy of %s." % nm, E, [m * C, m * C * C / 2, m * 9e8], " J", "E = mc² = %g × (3.00 × 10⁸)² = <b>%.3g J</b>." % (m, E))
        if k == "m":
            E = R.choice([9.0e13, 4.5e16, 1.8e14, 3.6e15, 2.7e17, 9.0e10])
            m = E / C ** 2
            return nq("A nuclear reaction releases %s J. How much mass is converted into energy?" % nf(E), m, [E / C, E * C * C, E / (2 * C * C)], " kg",
                      "m = E ÷ c² = %.2g ÷ (9.00 × 10¹⁶) = <b>%.3g kg</b>." % (E, m))
        b = R.choice(SPEEDS)
        g = gam(b)
        m = 1.67e-27
        p = g * m * b * C
        return nq("Calculate the relativistic momentum of a proton (mass 1.67 × 10⁻²⁷ kg) moving at %sc." % fmt(b), p, [m * b * C, p * g, m * C], " kg m/s",
                  "p = γmv = %.3g × 1.67 × 10⁻²⁷ × %s × 3.00 × 10⁸ = <b>%.3g kg m/s</b>." % (g, fmt(b), p))
    return dilate, contract, muon, energy


def wien_maker(R):
    def f():
        b = 2.898e-3
        stars = [("Betelgeuse", 3500), ("the Sun", 5800), ("Sirius", 9900), ("Rigel", 12100), ("Proxima Centauri", 3000), ("Spica", 22000), ("Vega", 9600), ("Antares", 3400), ("Acrux", 28000), ("Alpha Centauri A", 5800)]
        name, T = R.choice(stars)
        lam = b / T
        if R.random() < 0.5:
            return nq("The surface temperature of %s is about %d K. Use Wien's law (λmax T = 2.898 × 10⁻³ m K) to find the peak wavelength in nm." % (name, T),
                      lam * 1e9, [b * T, lam * 1e6, T / b * 1e-9], " nm", "λmax = 2.898 × 10⁻³ ÷ %d = %.3g m = <b>%.3g nm</b>." % (T, lam, lam * 1e9))
        lnm = round(lam * 1e9, -1)
        return nq("A star's spectrum peaks at %d nm. Use Wien's law (λmax T = 2.898 × 10⁻³ m K) to estimate its surface temperature." % lnm, b / (lnm * 1e-9),
                  [b * lnm, b / lnm, b / (lnm * 1e-6)], " K", "T = 2.898 × 10⁻³ ÷ (%d × 10⁻⁹) = <b>%.3g K</b>." % (lnm, b / (lnm * 1e-9)))
    return f


def motor_maker(R):
    def f():
        k = R.choice(["F", "I", "torque"])
        B = R.choice([0.050, 0.10, 0.20, 0.25, 0.40, 0.50, 0.80])
        I = R.choice([0.5, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0])
        L = R.choice([0.05, 0.10, 0.20, 0.25, 0.30, 0.50])
        if k == "F":
            th = R.choice([90, 90, 30, 60])
            F = B * I * L * math.sin(math.radians(th))
            return nq("A wire %g m long carries %g A at %d° to a magnetic field of %g T. Calculate the force on the wire." % (L, I, th, B), F,
                      [B * I * L if th != 90 else B * I / L, B * I * L * math.cos(math.radians(th)) if th != 90 else B * L, B * I], " N",
                      "F = BIL sin θ = %g × %g × %g × sin %d° = <b>%.3g N</b>." % (B, I, L, th, F))
        if k == "I":
            F = B * I * L
            return nq("A wire %g m long at right angles to a %g T field feels a force of %.3g N. What current flows in it?" % (L, B, F), I, [F * B * L, F / B, B * L / F], " A",
                      "I = F ÷ (BL) = %.3g ÷ (%g × %g) = <b>%g A</b>." % (F, B, L, I))
        n = R.choice([10, 20, 50, 100])
        w = L
        tq = n * B * I * L * w
        return nq("A square coil of %d turns, side %g m, carries %g A in a %g T field with its plane parallel to the field. Calculate the maximum torque." % (n, L, I, B), tq,
                  [B * I * L * w, n * B * I * L, n * B * I * L * w / 2], " N m", "τ = nBIA = %d × %g × %g × %g² = <b>%.3g N m</b>." % (n, B, I, L, tq))
    return f


GRAV = [
    ("Why does a projectile follow a parabolic path (ignoring air resistance)?", "its horizontal velocity is constant while its vertical velocity changes at a steady rate (g)", ["gravity acts horizontally", "its speed is constant", "air resistance pulls it down"], "The two motions are independent."),
    ("At the top of its path, what is the vertical velocity of a projectile?", "zero", ["equal to its launch speed", "9.8 m/s", "the same as its horizontal velocity"], "Its horizontal velocity is unchanged."),
    ("Which launch angle gives the greatest range on level ground, ignoring air resistance?", "45°", ["30°", "60°", "90°"], "Complementary angles (30° and 60°) give equal ranges."),
    ("How does air resistance change the path of a cricket ball?", "it reduces both the range and the maximum height", ["it increases the range", "it has no effect", "it makes the path a straight line"], "Real paths are not perfect parabolas."),
    ("What provides the centripetal force for a car turning on a flat road?", "friction between the tyres and the road", ["gravity", "the engine", "air resistance"], "On a wet road there is less friction."),
    ("In which direction does the net force act on an object in uniform circular motion?", "towards the centre of the circle", ["along the direction of motion", "away from the centre", "there is no net force"], "Centripetal means centre-seeking."),
    ("Why are curves on racetracks and highways often banked?", "the normal force has a component towards the centre, providing centripetal force", ["to make cars go slower", "to increase friction", "to drain rain only"], "At the design speed no friction is needed."),
    ("What provides the centripetal force for a satellite in orbit?", "the gravitational force of the planet", ["the satellite's engines", "air resistance", "the Moon"], "The satellite is in free fall."),
    ("Why do astronauts on the International Space Station feel weightless?", "they and the station are both in free fall around Earth", ["there is no gravity at that height", "the station shields them from gravity", "they are too far from Earth"], "g there is still about 8.7 m/s²."),
    ("What is a geostationary orbit?", "an orbit above the Equator with a period of 24 hours, so the satellite stays over one point", ["an orbit over the poles", "an orbit that takes 90 minutes", "any orbit near the Moon"], "Used for communications and weather satellites."),
    ("What happens to the gravitational force between two masses if the distance between them doubles?", "it becomes one quarter", ["it halves", "it doubles", "it stays the same"], "Inverse square law."),
    ("What is the gravitational field strength at Earth's surface?", "about 9.8 N/kg", ["about 6.67 × 10⁻¹¹ N/kg", "about 1.6 N/kg", "about 98 N/kg"], "On the Moon it is about 1.6 N/kg."),
    ("What does Kepler's third law state?", "the square of a planet's orbital period is proportional to the cube of its mean orbital radius", ["planets move in circles", "all planets have the same period", "the period is proportional to the radius"], "T² ∝ r³."),
    ("Why does a satellite in a lower orbit move faster?", "gravity is stronger closer to the planet, so it needs a higher speed to stay in orbit", ["it has less mass", "it is further from Earth", "air resistance pushes it"], "v = √(GM/r)."),
    ("What is the period of the Moon's orbit around Earth?", "about 27.3 days", ["about 24 hours", "about 365 days", "about 90 minutes"], "Its distance is about 384 000 km."),
    ("Why is the gravitational field strength on the Moon smaller than on Earth?", "the Moon has much less mass, even though its radius is also smaller", ["the Moon has no atmosphere", "the Moon is further from the Sun", "the Moon spins faster"], "g(Moon) ≈ 1.6 N/kg."),
    ("What is the escape velocity from Earth?", "about 11.2 km/s", ["about 7.9 km/s", "about 340 m/s", "about 3 × 10⁸ m/s"], "It does not depend on the mass of the object."),
    ("Why is the Woomera range in South Australia useful for testing rockets?", "it is a large, remote and sparsely populated area", ["it is close to the Equator", "it has no gravity", "it is at high altitude"], "Rocket launches need large safety zones."),
]
EM = [
    ("What is the direction of the force on a current-carrying wire in a magnetic field?", "at right angles to both the current and the field (right-hand rule)", ["along the wire", "along the field", "towards the north pole"], "The force is greatest when the wire is at 90° to the field."),
    ("Why does a charged particle move in a circle in a uniform magnetic field?", "the magnetic force is always at right angles to its velocity", ["the field pulls it towards the centre of the magnet", "the force is along its velocity", "its charge keeps changing"], "r = mv ÷ (qB)."),
    ("What is magnetic flux?", "the product of field strength and the area at right angles to it, Φ = BA", ["the force on a wire", "the current in a coil", "the speed of a magnet"], "Measured in webers (Wb)."),
    ("What does Faraday's law state?", "the induced e.m.f. equals the rate of change of magnetic flux linkage", ["a current makes a magnetic field", "like poles repel", "current equals voltage over resistance"], "ε = −N ΔΦ/Δt."),
    ("What does Lenz's law state?", "the induced current flows in a direction that opposes the change producing it", ["the induced current always helps the change", "induced currents are always zero", "flux never changes"], "It follows from conservation of energy."),
    ("Why is no e.m.f. induced when a magnet is held still inside a coil?", "the magnetic flux through the coil is not changing", ["the magnet has no field", "the coil is not a conductor", "the coil is too short"], "Only a change of flux induces an e.m.f."),
    ("How does a DC electric motor keep turning in one direction?", "a split-ring commutator reverses the current in the coil every half turn", ["slip rings keep the current the same", "the magnets move", "the coil has no current"], "The forces on the sides of the coil form a turning effect."),
    ("How does an AC generator produce a current?", "a coil rotates in a magnetic field, so the flux through it changes and an e.m.f. is induced", ["current flows from the magnets", "the coil is heated", "it stores charge"], "Slip rings connect the coil to the circuit."),
    ("Why does a transformer work only with alternating current?", "a changing current is needed to produce a changing magnetic flux in the core", ["DC is too large", "the core melts with DC", "DC has no voltage"], "Vs/Vp = Ns/Np."),
    ("Why is electricity transmitted over long distances at very high voltage?", "for the same power the current is smaller, so less energy is lost as heat (P = I²R)", ["high voltage travels faster", "it increases resistance", "it makes the wires cooler in summer only"], "Step-down transformers reduce it for homes."),
    ("Why does a transformer core use thin, insulated laminations?", "they reduce eddy currents and the energy lost as heat", ["they increase the voltage", "they make the transformer lighter only", "they store charge"], "Eddy currents oppose the changing flux."),
    ("How does magnetic braking on a roller coaster work?", "magnets induce eddy currents in metal fins, and these currents oppose the motion", ["magnets attract the cars to the track", "friction pads press on the wheels", "electric motors run backwards"], "There is no contact, so no wear."),
    ("What is the direction of an electric field?", "the direction of the force on a positive test charge", ["the direction of the force on a negative charge", "towards positive charges", "always downwards"], "Field lines go from + to −."),
    ("Between two parallel charged plates, what is the electric field like?", "uniform, with E = V ÷ d", ["zero everywhere", "strongest at the centre only", "it varies as 1/r²"], "The field lines are parallel and evenly spaced."),
    ("Which force does an electron feel moving parallel to a magnetic field?", "no magnetic force", ["the largest possible force", "a force along its motion", "a force towards the north pole"], "F = qvB sin θ and θ = 0."),
    ("What are the right-hand rules used for?", "finding the directions of fields, currents and forces in electromagnetism", ["measuring current", "measuring resistance", "finding the speed of light"], "Use conventional current (positive charge)."),
]
REL = [
    ("What are the two postulates of special relativity?", "the laws of physics are the same in all inertial frames, and the speed of light in a vacuum is the same for all observers", ["time is absolute and space is absolute", "mass is always conserved and energy is not", "light needs a medium"], "Einstein, 1905."),
    ("What is an inertial frame of reference?", "a frame that is not accelerating", ["a frame that is rotating", "any frame on Earth's surface accelerating upwards", "a frame moving faster than light"], "Newton's first law holds in it."),
    ("What did the Michelson–Morley experiment show?", "no evidence of an 'aether', supporting a constant speed of light", ["that light is a particle", "that the Earth is flat", "that the speed of light changes with direction"], "It found no change in light speed with Earth's motion."),
    ("What is proper time?", "the time between two events measured by an observer for whom they happen at the same place", ["the time on a clock in a moving frame seen from outside", "the time it takes light to travel 1 m", "the age of the universe"], "Proper time is the shortest measured time."),
    ("What is proper length?", "the length of an object measured in its own rest frame", ["the length seen by a moving observer", "the length of a light year", "the length after it is heated"], "Moving observers measure a shorter length."),
    ("What happens to a clock that moves fast relative to an observer?", "the observer sees it run slow (time dilation)", ["it runs fast", "it stops", "it is unaffected"], "t = γt₀."),
    ("In which direction does length contraction happen?", "only along the direction of motion", ["in all directions", "at right angles to the motion only", "it does not happen"], "Widths and heights are unchanged."),
    ("Why do muons made high in the atmosphere reach Earth's surface?", "their lifetime is dilated in Earth's frame (or the distance is contracted in theirs)", ["they travel faster than light", "they are not radioactive", "the atmosphere speeds them up"], "This is direct evidence for time dilation."),
    ("Why must GPS satellites correct their clocks for relativity?", "their clocks run at a different rate from clocks on the ground because of their speed and weaker gravity", ["the satellites are too hot", "the speed of light changes in space", "satellite clocks have no batteries"], "Without corrections, positions would drift by kilometres a day."),
    ("What is the Lorentz factor γ at speeds much less than the speed of light?", "very close to 1, so relativistic effects are tiny", ["close to 0", "infinite", "exactly 2"], "Relativity agrees with Newton at low speed."),
    ("Why can no object with mass reach the speed of light?", "its relativistic momentum and energy would become infinite", ["air resistance prevents it", "light pushes it back", "it would lose all its mass"], "Particle accelerators get very close but never reach c."),
    ("What does E = mc² mean?", "mass and energy are equivalent: a mass m has a rest energy mc²", ["energy equals mass times speed", "mass is destroyed in every reaction", "light has a mass of c²"], "Nuclear reactions convert a little mass into a lot of energy."),
    ("Two events are simultaneous for one observer. Are they simultaneous for an observer moving past?", "not necessarily: simultaneity is relative", ["always yes", "never", "only if they are far apart"], "This follows from the constant speed of light."),
    ("What is the speed of light in a vacuum?", "3.00 × 10⁸ m/s", ["3.00 × 10⁶ m/s", "340 m/s", "it depends on the observer's speed"], "It is the same in every inertial frame."),
]
QUA = [
    ("What problem in physics led Planck to propose quanta of energy?", "the shape of the black-body radiation spectrum, which classical physics could not explain", ["the speed of sound", "the orbit of the Moon", "the colour of the sky"], "Classical theory predicted the 'ultraviolet catastrophe'."),
    ("What does Wien's law describe?", "the peak wavelength of black-body radiation gets shorter as temperature rises", ["the speed of light in glass", "the force between charges", "the half-life of an isotope"], "λmax T = 2.898 × 10⁻³ m K."),
    ("Why do hotter stars look blue and cooler stars look red?", "the peak of their emission shifts to shorter wavelengths at higher temperatures", ["blue stars are closer", "red stars are moving towards us", "cooler stars are larger only"], "Wien's law."),
    ("Which observation of the photoelectric effect could the wave model of light NOT explain?", "no electrons are emitted below a threshold frequency, however bright the light", ["more light gives more electrons", "electrons have negative charge", "metals conduct electricity"], "Einstein explained it with photons."),
    ("What does increasing the intensity of light above the threshold frequency do in the photoelectric effect?", "it increases the number of photoelectrons but not their maximum kinetic energy", ["it increases their maximum kinetic energy", "it stops the emission", "it changes the work function"], "Kinetic energy depends on frequency."),
    ("What is the work function of a metal?", "the minimum energy needed to free an electron from its surface", ["the energy of a photon", "the maximum kinetic energy of an electron", "the voltage of a cell"], "hf = φ + Ek(max)."),
    ("What evidence shows that electrons can behave as waves?", "electron diffraction patterns", ["the photoelectric effect", "beta decay", "electric current in a wire"], "λ = h ÷ (mv)."),
    ("Why do atoms produce line spectra?", "electrons can only occupy fixed energy levels, so only photons of certain energies are emitted", ["electrons spiral into the nucleus", "atoms emit all wavelengths equally", "the nucleus splits"], "Bohr's model explained hydrogen's lines."),
    ("Why did Bohr's model need to replace Rutherford's model of the atom?", "in Rutherford's model, orbiting electrons should radiate energy and spiral into the nucleus", ["Rutherford's model had no nucleus", "Rutherford's model had no electrons", "Bohr found the neutron"], "Bohr's electrons have fixed, stable orbits."),
    ("What is wave–particle duality?", "light and matter show both wave and particle properties", ["light is only a wave", "electrons are only particles", "waves and particles are the same size"], "Which one we see depends on the experiment."),
    ("What does the Australian Synchrotron in Melbourne produce?", "intense beams of light, from infrared to X-rays, made by electrons moving in a ring", ["nuclear electricity", "antimatter for fuel", "gravitational waves"], "Researchers use it to study materials and proteins."),
    ("Who explained the photoelectric effect using photons, winning the 1921 Nobel Prize?", "Albert Einstein", ["Max Planck", "Niels Bohr", "Isaac Newton"], "Planck had introduced quanta in 1900."),
    ("What is the value of Planck's constant?", "6.63 × 10⁻³⁴ J s", ["3.00 × 10⁸ m/s", "1.60 × 10⁻¹⁹ C", "6.67 × 10⁻¹¹ N m² kg⁻²"], "E = hf."),
    ("What is a photon?", "a quantum (packet) of electromagnetic energy, E = hf", ["an electron in orbit", "a nucleus", "a sound wave"], "Photons have no mass and travel at c."),
]
STD = [
    ("What are the fundamental particles of matter in the Standard Model?", "six quarks and six leptons", ["protons, neutrons and electrons", "atoms and molecules", "photons only"], "Protons and neutrons are made of quarks."),
    ("What is a proton made of?", "two up quarks and one down quark (uud)", ["one up and two down quarks", "three down quarks", "an electron and a neutrino"], "Its charge is +2/3 + 2/3 − 1/3 = +1."),
    ("What is a neutron made of?", "one up quark and two down quarks (udd)", ["two up and one down quark", "a proton and an electron", "three up quarks"], "Its charge is +2/3 − 1/3 − 1/3 = 0."),
    ("What is the charge of an up quark?", "+2/3 e", ["−1/3 e", "+1 e", "0"], "A down quark is −1/3 e."),
    ("What is a baryon?", "a hadron made of three quarks, such as a proton", ["a particle made of a quark and an antiquark", "a lepton", "a force-carrying particle"], "Mesons are quark–antiquark pairs."),
    ("What is a meson?", "a hadron made of a quark and an antiquark, such as a pion", ["a particle made of three quarks", "a type of lepton", "a photon"], "Mesons are unstable."),
    ("Which particle is a lepton?", "the electron", ["the proton", "the neutron", "the pion"], "Leptons do not feel the strong force."),
    ("Which particle carries the electromagnetic force?", "the photon", ["the gluon", "the W boson", "the Higgs boson"], "Exchange particles are gauge bosons."),
    ("Which particles carry the strong force between quarks?", "gluons", ["photons", "W and Z bosons", "neutrinos"], "Gluons hold quarks together in hadrons."),
    ("Which particles carry the weak force?", "W⁺, W⁻ and Z bosons", ["gluons", "photons", "gravitons, which have been detected"], "The weak force causes beta decay."),
    ("What does the Higgs boson explain?", "how some fundamental particles get their mass", ["why quarks have colour", "how light travels", "why gravity is weak"], "It was found at CERN's Large Hadron Collider in 2012."),
    ("What is an antiparticle?", "a particle with the same mass but opposite charge and other quantum numbers", ["a particle with no mass", "a heavier copy of a particle", "a particle that moves backwards"], "The positron is the antielectron."),
    ("What happens when a particle meets its antiparticle?", "they annihilate, turning their mass into energy such as gamma photons", ["they bounce apart", "they form a new atom", "nothing happens"], "PET scans detect annihilation gamma rays."),
    ("Which quantity is always conserved in particle interactions?", "charge (also baryon number and lepton number)", ["the number of particles", "kinetic energy", "strangeness in weak interactions"], "Use conservation laws to check if a reaction is possible."),
    ("In beta-minus decay, a down quark changes into which quark?", "an up quark, emitting a W⁻ boson that decays to an electron and an antineutrino", ["a strange quark", "a top quark", "a gluon"], "A neutron becomes a proton."),
    ("Why are quarks never seen on their own?", "the strong force between them grows as they separate (colour confinement)", ["they are too small to see", "they move faster than light", "they have no charge"], "They are always found in hadrons."),
    ("Which force is NOT part of the Standard Model?", "gravity", ["the strong force", "the weak force", "the electromagnetic force"], "No theory yet unites gravity with the others."),
    ("Is the decay n → p + e⁻ + ν̄ (antineutrino) allowed?", "yes: charge, baryon number and lepton number are all conserved", ["no: charge is not conserved", "no: baryon number is not conserved", "no: lepton number is not conserved"], "Lepton number: 0 → 0 + 1 − 1."),
    ("Is the reaction p → n + e⁻ allowed?", "no: charge is not conserved", ["yes, it happens in the Sun", "yes: all quantities are conserved", "no: only energy is not conserved"], "+1 → 0 + (−1) = −1."),
    ("Which particle is the antiparticle of the electron?", "the positron, e⁺", ["the proton", "the neutrino", "the photon"], "Same mass, opposite charge."),
    ("How many gamma photons are usually produced when an electron and a positron annihilate at rest?", "two, moving in opposite directions", ["one", "none", "three, all in the same direction"], "Momentum must be conserved."),
    ("What is the lepton number of an electron neutrino?", "+1", ["0", "−1", "+1/3"], "Antileptons have −1."),
    ("What is the baryon number of a quark?", "+1/3", ["+1", "0", "−1"], "Three quarks make a baryon with B = 1."),
    ("What is a neutrino?", "a lepton with no charge and a very small mass that hardly interacts with matter", ["a heavy quark", "a type of photon", "a neutron"], "Trillions pass through you every second from the Sun."),
]


def u13(X):
    return [
        ("Projectile motion", [(X.ch("al_phys", "mechanics-and-materials", 3, 12, only=[0]), 10), (X.ch("in_s11p", "motion-in-a-plane", 2), 6), (X.pool(GRAV), 4)]),
        ("Range and launch angle", [(X.ch("in_s11p", "motion-in-a-plane", 3), 14), (X.pool(GRAV), 6)]),
        ("Uniform circular motion", [(X.ch("in_s11p", "motion-in-a-plane", 4), 12), (X.ch("al_phys", "circular-motion-and-oscillations", 1, 13), 8)]),
        ("Centripetal force", [(X.ch("al_phys", "circular-motion-and-oscillations", 2, 13), 16), (X.pool(GRAV), 4)]),
        ("Vectors and inclined planes", [(X.ch("in_s11p", "motion-in-a-plane", 1), 14), (X.al(__import__("al_phys").m_resolve), 6)]),
    ]


def u14(X):
    return [
        ("Newton's law of gravitation", [(X.ch("al_phys", "gravitational-and-electric-fields", 1, 13), 10), (X.ch("in_s11p", "gravitation", 2), 6), (X.pool(GRAV), 4)]),
        ("Gravitational field strength", [(X.ch("in_s11p", "gravitation", 3), 10), (X.al(__import__("al_phys").f_grav, "g", "h"), 6), (X.pool(GRAV), 4)]),
        ("Satellites and orbits", [(X.ch("al_phys", "gravitational-and-electric-fields", 2, 13), 12), (X.ch("in_s11p", "gravitation", 4), 6), (X.pool(GRAV), 2)]),
        ("Kepler's laws", [(X.ch("in_s11p", "gravitation", 1), 8), (X.gen("gen_us_science_ess_keplers_laws_and_orbits", "g_k3"), 8), (X.gen("gen_us_science_ess_keplers_laws_and_orbits", "g_table"), 4)]),
        ("Gravity problems", [(X.ch("in_s11p", "gravitation", 5), 16), (X.pool(GRAV), 4)]),
    ]


def u15(X):
    return [
        ("Electric fields", [(X.ch("al_phys", "gravitational-and-electric-fields", 3, 13), 10), (X.ch("al_phys", "gravitational-and-electric-fields", 4, 13), 6), (X.pool(EM), 4)]),
        ("Magnetic forces on currents and charges", [(X.f(motor_maker), 10), (X.ch("al_phys", "capacitors-and-magnetic-fields", 3, 13), 6), (X.pool(EM), 4)]),
        ("Electromagnetic induction", [(X.ch("in_s12p", "electromagnetic-induction", 2), 10), (X.ch("in_s12p", "electromagnetic-induction", 3), 6), (X.pool(EM), 4)]),
        ("Motors, generators and transformers", [(X.ch("al_phys", "capacitors-and-magnetic-fields", 4, 13), 14), (X.pool(EM), 4), (X.f(motor_maker), 2)]),
        ("Electromagnetism problems", [(X.ch("in_s12p", "moving-charges-and-magnetism", 3), 8), (X.ch("al_phys", "capacitors-and-magnetic-fields", 3, 13), 8), (X.f(motor_maker), 4)]),
    ]


def u16(X):
    dil, con, mu, en = rel_makers(X.R)
    return [
        ("Postulates and frames of reference", [(X.pool(REL), 10), (X.w(dil), 6), (X.w(en), 4)]),
        ("Time dilation", [(X.w(dil), 16), (X.pool(REL), 4)]),
        ("Length contraction", [(X.w(con), 16), (X.w(mu), 4)]),
        ("Muons and evidence for relativity", [(X.w(mu), 12), (X.w(dil), 4), (X.w(con), 4)]),
        ("Mass–energy equivalence and momentum", [(X.w(en), 18), (X.w(con), 2)]),
    ]


def u17(X):
    al = __import__("al_phys")
    return [
        ("Black-body radiation", [(X.w(wien_maker(X.R)), 12), (X.pool(QUA), 4), (X.ch("in_s12p", "electromagnetic-waves", 4), 4)]),
        ("Photons", [(X.ch("al_phys", "particles-and-quantum-phenomena", 2, 12), 16), (X.pool(QUA), 4)]),
        ("The photoelectric effect", [(X.ch("al_phys", "particles-and-quantum-phenomena", 3, 12), 12), (X.ch("in_s12p", "dual-nature-of-radiation-and-matter", 4), 6), (X.pool(QUA), 2)]),
        ("Energy levels and line spectra", [(X.ch("in_s12p", "atoms", 3), 8), (X.ch("in_s12p", "atoms", 4), 8), (X.pool(QUA), 2), (X.al(al.p_levels, "lam"), 2)]),
        ("Wave–particle duality", [(X.ch("al_phys", "particles-and-quantum-phenomena", 4, 12), 16), (X.w(wien_maker(X.R)), 4)]),
    ]


def u18(X):
    al = __import__("al_phys")
    return [
        ("Quarks and leptons", [(X.pool(STD), 10), (X.ch("al_phys", "particles-and-quantum-phenomena", 5, 12), 10)]),
        ("Hadrons: baryons and mesons", [(X.pool(STD), 4), (X.ch("al_phys", "particles-and-quantum-phenomena", 5, 12), 10), (X.al(al.p_nucleus), 6)]),
        ("Forces and exchange particles", [(X.pool(STD), 4), (X.ch("al_phys", "particles-and-quantum-phenomena", 5, 12), 6), (X.gen("gen_us_science_ess_stars_and_the_origin_of_elements", "g_fuse"), 10)]),
        ("Antimatter and conservation laws", [(X.pool(STD), 4), (X.w(rel_makers(X.R)[3]), 10), (X.al(al.p_photon), 6)]),
        ("Particle accelerators and the early universe", [(X.gen("gen_us_science_ess_the_big_bang", "g_ev"), 10), (X.gen("gen_us_science_ess_the_big_bang", "g_shift"), 10)]),
    ]


def UNITS():
    return [
        SR(PH, 3, 13, "projectile-and-circular-motion", "Gravity and motion",
           "Vectors and their components; projectile motion with independent horizontal and vertical motion; launch angle and range; uniform circular motion, centripetal acceleration and force; banked curves.",
           "Projectile and Circular Motion", "projectile and circular motion",
           "Free Year 12 Physics worksheets on projectile and circular motion: vectors, time of flight, range, maximum height, centripetal acceleration, centripetal force and banked curves. 100 questions with answers.",
           "Projectiles: horizontal velocity constant; vertical acceleration g.", "Circular motion: a = v²/r and F = mv²/r towards the centre.",
           "<p>Treat projectile motion as two independent motions: horizontally the velocity is constant; vertically the acceleration is g = 9.8 m/s² downwards. Time links them. On level ground, maximum range is at 45° (ignoring air resistance).</p>"
           "<p>An object moving in a circle at constant speed accelerates towards the centre: a = v²/r. The net (centripetal) force F = mv²/r can be friction, tension, gravity or a component of the normal force on a banked curve.</p>",
           [("Ball rolls off a 1.25 m table at 3.0 m/s. Time to land?", ["1.25 = ½ × 9.8 × t²"], "0.505 s"),
            ("1200 kg car, 20 m/s, curve radius 50 m. Centripetal force?", ["F = mv²/r = 1200 × 400 ÷ 50"], "9600 N")],
           ["Letting the horizontal velocity change during flight.", "Drawing a 'centrifugal' force outwards in a free-body diagram.", "Using the diameter instead of the radius."],
           [("Why does a ball dropped and a ball thrown horizontally land at the same time?", "Both start with zero vertical velocity and have the same vertical acceleration, g; the horizontal motion does not affect the vertical motion."),
            ("What provides centripetal force on a banked curve?", "The horizontal component of the normal force (plus friction if the speed is not the design speed).")],
           u13),
        SR(PH, 3, 14, "gravitational-fields-and-orbits", "Gravity and motion",
           "Newton's law of universal gravitation; gravitational field strength and its variation with distance; satellite motion and orbital speed and period; geostationary orbits; Kepler's laws.",
           "Gravitational Fields, Satellites and Orbits", "gravitational fields and orbits",
           "Free Year 12 Physics worksheets on gravity: Newton's law of gravitation, field strength, orbital speed and period, geostationary orbits and Kepler's third law. 100 questions with answers.",
           "F = GMm/r²; g = GM/r².", "For orbits: v = √(GM/r) and T² ∝ r³.",
           "<p>Every mass attracts every other mass: F = GMm ÷ r², with G = 6.67 × 10⁻¹¹ N m² kg⁻². The gravitational field strength g = GM ÷ r² falls with the square of the distance from the centre.</p>"
           "<p>For a satellite, gravity provides the centripetal force: GMm/r² = mv²/r, so v = √(GM/r) and T = 2πr/v. Lower orbits are faster. Kepler's third law: T² ∝ r³. A geostationary satellite orbits above the Equator with T = 24 h.</p>",
           [("Distance doubles. New force?", ["F ∝ 1/r²", "(1/2)² = 1/4"], "one quarter"),
            ("Planet with r 4 times Earth's (1 AU). Period?", ["T² = 4³ = 64"], "8 years")],
           ["Using the height above the surface instead of the distance from the centre.", "Thinking there is no gravity in orbit.", "Saying a heavier satellite needs a faster orbital speed."],
           [("Why do astronauts float in the ISS?", "They are in free fall together with the station; gravity there is still about 90% of its surface value."),
            ("Does the orbital speed depend on the satellite's mass?", "No: v = √(GM/r) depends only on the planet's mass and the orbit radius.")],
           u14),
        SR(PH, 3, 15, "electromagnetism", "Electromagnetism",
           "Electric fields and forces on charges; magnetic fields; forces on current-carrying conductors and moving charges; magnetic flux, Faraday's and Lenz's laws; DC motors, AC generators, transformers and power transmission.",
           "Electromagnetism: Fields, Forces and Induction", "electromagnetism",
           "Free Year 12 Physics worksheets on electromagnetism: electric fields, F = BIL, F = qvB, magnetic flux, Faraday's and Lenz's laws, motors, generators and transformers. 100 questions with answers.",
           "F = BIL sin θ; F = qvB sin θ.", "ε = −N ΔΦ/Δt; Vs/Vp = Ns/Np.",
           "<p>An electric field exerts a force F = qE on a charge; between parallel plates E = V/d. A magnetic field exerts a force on a current (F = BIL) and on a moving charge (F = qvB), at right angles to the motion: this drives electric motors and bends charged particles into circles.</p>"
           "<p>A changing magnetic flux induces an e.m.f. (Faraday's law), in a direction that opposes the change (Lenz's law). Generators and transformers use induction; high-voltage transmission reduces I²R losses.</p>",
           [("Wire 0.20 m, 3.0 A, at 90° to 0.50 T. Force?", ["F = BIL = 0.50 × 3.0 × 0.20"], "0.30 N"),
            ("Transformer: 240 V, 1000 primary turns, 50 secondary turns. Vs?", ["Vs = 240 × 50 ÷ 1000"], "12 V")],
           ["Using the left hand instead of the right hand for the rule.", "Thinking a steady magnetic field induces a current.", "Thinking a transformer works with DC."],
           [("Why is power transmitted at high voltage?", "P = VI, so a higher voltage means a smaller current for the same power, and the heat lost in the lines (I²R) is much smaller."),
            ("What does Lenz's law tell us?", "The induced current always opposes the change in flux that caused it, which is why you must do work to push a magnet into a coil.")],
           u15),
        SR(PH, 4, 16, "special-relativity", "Special relativity",
           "Inertial frames and Einstein's postulates; the constant speed of light; relativity of simultaneity; time dilation and length contraction; evidence from muons, GPS and particle accelerators; relativistic momentum and mass–energy equivalence.",
           "Special Relativity: Time Dilation and E = mc²", "special relativity",
           "Free Year 12 Physics worksheets on special relativity: Einstein's postulates, the Lorentz factor, time dilation, length contraction, muons, GPS, relativistic momentum and E = mc². 100 questions with answers.",
           "γ = 1 ÷ √(1 − v²/c²).", "t = γt₀; L = L₀ ÷ γ; E = mc².",
           "<p>Einstein's postulates: the laws of physics are the same in all inertial frames, and the speed of light is the same for every observer. As a result, a moving clock runs slow (<b>time dilation</b>, t = γt₀) and a moving object is shorter along its motion (<b>length contraction</b>, L = L₀/γ).</p>"
           "<p>γ is close to 1 at everyday speeds but grows without limit as v approaches c, so no object with mass can reach light speed. Muons reaching the ground and GPS clock corrections confirm relativity. Mass and energy are equivalent: E = mc².</p>",
           [("γ at 0.8c?", ["1 − 0.64 = 0.36", "√0.36 = 0.6", "1 ÷ 0.6"], "1.67"),
            ("At 0.8c a 2.0 s tick (on board) seen from Earth?", ["t = γt₀ = 1.67 × 2.0"], "3.33 s")],
           ["Applying length contraction at right angles to the motion.", "Mixing up proper time and dilated time.", "Thinking the speed of light changes for a moving observer."],
           [("Is time dilation real or an illusion?", "It is real and measured: fast-moving muons live longer in our frame, and clocks flown on aircraft and satellites run at measurably different rates."),
            ("Why can't we notice relativity in daily life?", "At everyday speeds γ is extremely close to 1, so the effects are far too small to see.")],
           u16),
        SR(PH, 4, 17, "quantum-theory", "Quantum theory",
           "Black-body radiation, Wien's law and Planck's quanta; photons and E = hf; the photoelectric effect, work function and threshold frequency; energy levels and line spectra in the Bohr model; de Broglie waves and wave–particle duality.",
           "Quantum Theory: Photons, Spectra and Matter Waves", "quantum theory",
           "Free Year 12 Physics worksheets on quantum theory: black-body radiation, Wien's law, E = hf, the photoelectric effect, energy levels, line spectra and de Broglie wavelength. 100 questions with answers.",
           "E = hf = hc/λ; hf = φ + Ek(max).", "λ = h/(mv) for moving particles.",
           "<p>Hot objects emit a black-body spectrum that peaks at λmax = 2.898 × 10⁻³ ÷ T (Wien's law). Planck explained the spectrum by assuming energy comes in quanta; Einstein extended this to photons, E = hf.</p>"
           "<p>In the photoelectric effect one photon frees one electron if hf exceeds the work function φ. Electrons in atoms have fixed energy levels, so atoms emit and absorb photons of particular energies (line spectra). Matter also behaves as waves: λ = h/(mv).</p>",
           [("Peak wavelength of a 5800 K star?", ["λ = 2.898 × 10⁻³ ÷ 5800"], "500 nm"),
            ("Photon of 3.0 eV on a metal with φ = 2.0 eV. Ek(max)?", ["3.0 − 2.0"], "1.0 eV")],
           ["Thinking brighter light gives faster photoelectrons.", "Forgetting to convert eV to joules (× 1.60 × 10⁻¹⁹).", "Thinking only light can show wave behaviour."],
           [("What is the 'ultraviolet catastrophe'?", "Classical physics predicted that a black body would emit infinite energy at short wavelengths; Planck's quantum idea fixed this."),
            ("What is a photon's energy in eV for visible light?", "About 1.8 eV (red) to 3.1 eV (violet).")],
           u17),
        SR(PH, 4, 18, "the-standard-model", "The Standard Model",
           "Fundamental particles: six quarks and six leptons; hadrons (baryons and mesons); the four fundamental forces and their exchange particles; antimatter and annihilation; conservation of charge, baryon number and lepton number; particle accelerators and evidence for the Big Bang.",
           "The Standard Model of Particle Physics", "the Standard Model",
           "Free Year 12 Physics worksheets on the Standard Model: quarks, leptons, baryons, mesons, exchange particles, the Higgs boson, antimatter, conservation laws and particle accelerators. 100 questions with answers.",
           "Matter = quarks + leptons; forces = exchange bosons.", "Charge, baryon number and lepton number are always conserved.",
           "<p>The Standard Model describes matter with six <b>quarks</b> (up, down, charm, strange, top, bottom) and six <b>leptons</b> (electron, muon, tau and their neutrinos). Quarks combine into hadrons: baryons (three quarks: proton uud, neutron udd) and mesons (a quark and an antiquark).</p>"
           "<p>Forces are carried by exchange bosons: photons (electromagnetic), gluons (strong), W and Z bosons (weak). The Higgs boson gives some particles mass. Every particle has an antiparticle; they annihilate into energy. Reactions must conserve charge, baryon number and lepton number.</p>",
           [("Charge of uud?", ["+2/3 + 2/3 − 1/3"], "+1 (a proton)"),
            ("Is p → n + e⁺ + ν possible for a free proton?", ["charge, baryon and lepton numbers balance", "but the neutron has more mass"], "not for a free proton (energy)")],
           ["Thinking protons and neutrons are fundamental particles.", "Calling a meson a baryon.", "Saying gravity is carried by a detected particle in the Standard Model."],
           [("Why is the Higgs boson important?", "Its field gives mass to the W and Z bosons and to the quarks and leptons; finding it at CERN in 2012 completed the Standard Model."),
            ("What does the Standard Model not explain?", "Gravity, dark matter, dark energy and why there is more matter than antimatter.")],
           u18),
    ]
