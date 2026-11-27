# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 6: Energy
  python tools/gen_sg_science_s3_energy.py
Energy stores and transfers, the principle of conservation of energy, kinetic energy ½mv², gravitational potential energy mgh
(g = 10 N/kg), work done = force × distance moved in the direction of the force, power = energy ÷ time, efficiency, and
energy resources (renewable and non-renewable, including how Singapore generates electricity).
US and UK work, power and efficiency makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "KE = mv²", "work is done when you hold a heavy box still", "efficiency can be more than
100%", "power is the total energy used".
"""
import math
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ans_num, ex

LV, SUBJ, SORT = 3, "Physics", 6
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

us_ke = src("gen_us_science_phys_kinetic_and_potential_energy", "g_ke")
us_work = src("gen_us_science_phys_kinetic_and_potential_energy", "g_work")
us_eff = src("gen_us_science_phys_energy_conversion_and_efficiency", "g_eff")
uk_pow = src("gen_uk_science_y10_energy", "g_pow")
uk_work = src("gen_uk_science_y9_work_and_moments", "g_work")
uk_eff = src("gen_uk_science_y8_energy_and_power", "g_eff")


def g_ke():
    k = R.choice(["E", "E", "v", "m", "x2"])
    m = R.choice([0.05, 0.2, 0.5, 2, 4, 10, 50, 60, 1000, 1200])
    v = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 20])
    if m >= 1000 and v < 5 or m <= 0.5 and v > 20:
        return None
    E = 0.5 * m * v * v
    if k == "E":
        return nq("What is the kinetic energy of a %s kg object moving at %d m/s?" % (N(m), v), E, [m * v * v, m * v / 2, 0.5 * m * v], " J", "KE = ½mv² = ½ × %s × %d² = %s J." % (N(m), v, N(E)))
    if k == "v":
        return nq("A %s kg object has %s J of kinetic energy. What is its speed?" % (N(m), N(E)), v, [E / m, 2 * E / m, math.sqrt(E / m)], " m/s",
                  "v = √(2KE ÷ m) = √(2 × %s ÷ %s) = %d m/s." % (N(E), N(m), v))
    if k == "m":
        return nq("An object moving at %d m/s has %s J of kinetic energy. What is its mass?" % (v, N(E)), m, [E / v ** 2, 2 * E / v, E * v * v / 2], " kg",
                  "m = 2KE ÷ v² = 2 × %s ÷ %d = %s kg." % (N(E), v * v, N(m)))
    return tq("The speed of a car doubles. What happens to its kinetic energy?", "It becomes four times as large.", ["It doubles.", "It stays the same.", "It halves."],
              "KE = ½mv², so doubling v multiplies KE by 2² = 4.")


def g_gpe():
    k = R.choice(["E", "E", "h", "m"])
    m = R.choice([0.2, 0.5, 2, 5, 10, 20, 50, 60, 70, 800])
    h = R.choice([0.5, 1.2, 2, 3, 5, 8, 10, 15, 25, 40])
    E = m * 10 * h
    if k == "E":
        return nq("A %s kg object is lifted through a height of %s m. What is the gain in its gravitational potential energy? (g = 10 N/kg)" % (N(m), N(h)), E, [m * h, m * 10 / h, 0.5 * m * 10 * h], " J",
                  "GPE = mgh = %s × 10 × %s = %s J." % (N(m), N(h), N(E)))
    if k == "h":
        return nq("A %s kg box gains %s J of gravitational potential energy when it is lifted. How high is it lifted? (g = 10 N/kg)" % (N(m), N(E)), h, [E / m, E * m * 10, E / 10], " m",
                  "h = GPE ÷ mg = %s ÷ (%s × 10) = %s m." % (N(E), N(m), N(h)))
    return nq("A load gains %s J of gravitational potential energy when it is raised %s m. What is its mass? (g = 10 N/kg)" % (N(E), N(h)), m, [E / h, E * h / 10, E / 10], " kg",
              "m = GPE ÷ gh = %s ÷ (10 × %s) = %s kg." % (N(E), N(h), N(m)))


def g_fall():
    """GPE at the top = KE at the bottom (no air resistance)"""
    h = R.choice([0.8, 1.25, 1.8, 3.2, 5, 7.2, 12.8, 20, 45])
    v = math.sqrt(20 * h)
    m = R.choice([0.1, 0.2, 0.5, 1, 2])
    if R.random() < 0.5:
        return nq("A %s kg ball falls from rest through %s m. Ignoring air resistance, what is its speed just before it hits the ground? (g = 10 N/kg)" % (N(m), N(h)), v,
                  [20 * h, 10 * h, math.sqrt(10 * h)], " m/s", "mgh = ½mv², so v = √(2gh) = √(2 × 10 × %s) = %s m/s." % (N(h), N(v)))
    return nq("A %s kg stone is thrown straight up at %s m/s. Ignoring air resistance, how high does it rise? (g = 10 N/kg)" % (N(m), N(v)), h, [v / 10, v * v / 10, v * v], " m",
              "½mv² = mgh, so h = v² ÷ 2g = %s ÷ 20 = %s m." % (N(v * v), N(h)))


def g_power():
    k = R.choice(["P", "t", "E", "lift"])
    if k == "lift":
        m = R.choice([40, 50, 60, 70])
        h = R.choice([3, 4, 5, 6, 8, 10, 12])
        t = R.choice([4, 5, 6, 8, 10, 12, 15, 20])
        Pw = m * 10 * h / t
        return nq("A %d kg student runs up stairs %d m high in %d s. What is her useful power output? (g = 10 N/kg)" % (m, h, t), Pw, [m * h / t, m * 10 * h, m * 10 * h * t], " W",
                  "Work = mgh = %d × 10 × %d = %s J. P = %s ÷ %d = %s W." % (m, h, N(m * 10 * h), N(m * 10 * h), t, N(Pw)))
    Pw = R.choice([40, 60, 100, 500, 800, 1000, 1500, 2000, 2400])
    t = R.choice([5, 10, 30, 60, 120, 300])
    E = Pw * t
    dev = {40: "an LED lamp", 60: "a ceiling fan", 100: "a television", 500: "a blender", 800: "a microwave oven", 1000: "an iron", 1500: "an air-conditioner",
           2000: "a kettle", 2400: "a water heater"}[Pw]
    if k == "P":
        return nq("%s transfers %s J of energy in %d s. What is its power?" % (dev[0].upper() + dev[1:], N(E), t), Pw, [E * t, t / E, E / 60], " W", "P = E ÷ t = %s ÷ %d = %d W." % (N(E), t, Pw))
    if k == "t":
        return nq("How long does a %d W device take to transfer %s J?" % (Pw, N(E)), t, [E * Pw, Pw / E, E / 1000], " s", "t = E ÷ P = %s ÷ %d = %d s." % (N(E), Pw, t))
    return nq("How much energy does %s (%d W) transfer in %d s?" % (dev, Pw, t), E, [Pw / t, Pw * t / 60, Pw + t], " J", "E = Pt = %d × %d = %s J." % (Pw, t, N(E)))


def g_eff():
    k = R.choice(["eff", "useful", "input"])
    inp = R.choice([100, 200, 400, 500, 800, 1000, 1200, 2000, 5000])
    e = R.choice([10, 20, 25, 30, 35, 40, 60, 75, 80, 90])
    out = inp * e / 100
    dev = R.choice(["A motor", "A filament lamp", "A car engine", "A kettle", "An electric fan", "A solar panel", "A power station"])
    if k == "eff":
        return nq("%s is supplied with %s J and gives %s J of useful energy. What is its efficiency?" % (dev, N(inp), N(out)), e, [100 - e, inp / out, out / inp], "%",
                  "Efficiency = useful output ÷ total input × 100%% = %s ÷ %s × 100%% = %d%%." % (N(out), N(inp), e))
    if k == "useful":
        return nq("%s has an efficiency of %d%%. It is supplied with %s J. How much useful energy does it give?" % (dev, e, N(inp)), out, [inp * (100 - e) / 100, inp, inp / e], " J",
                  "Useful = %d%% × %s = %s J." % (e, N(inp), N(out)))
    return nq("%s gives %s J of useful energy with an efficiency of %d%%. How much energy is supplied to it?" % (dev, N(out), e), inp, [out * e / 100, out + e, out * (100 - e) / 100], " J",
              "Input = useful ÷ efficiency = %s ÷ %s = %s J." % (N(out), N(e / 100), N(inp)))


CONV = [("a battery-powered torch", "chemical potential energy → electrical → light and thermal energy"), ("a hydroelectric power station", "gravitational potential energy → kinetic energy → electrical energy"),
        ("a solar cell", "light (radiant) energy → electrical energy"), ("a car braking to a stop", "kinetic energy → thermal energy (heating the brakes)"),
        ("a ball falling from a height", "gravitational potential energy → kinetic energy"), ("a stretched catapult firing a stone", "elastic potential energy → kinetic energy"),
        ("a gas-fired power station", "chemical potential energy → thermal → kinetic → electrical energy"), ("a person climbing stairs", "chemical potential energy → gravitational potential energy (and thermal)")]
g_conv = rows(R, CONV, "Which energy changes happen in %s?")

RES = [("solar energy", "renewable"), ("wind energy", "renewable"), ("hydroelectric energy", "renewable"), ("geothermal energy", "renewable"), ("tidal energy", "renewable"),
       ("biomass", "renewable"), ("natural gas", "non-renewable"), ("coal", "non-renewable"), ("oil", "non-renewable"), ("nuclear fuel (uranium)", "non-renewable")]


def g_res():
    r, a = R.choice(RES)
    return tq("Is %s a renewable or a non-renewable energy resource?" % r, a, ["renewable" if a != "renewable" else "non-renewable", "neither: it is not an energy resource", "both"],
              "A renewable resource is replaced naturally and will not run out; fossil fuels and nuclear fuel will run out.")


POOL1 = pool(R, [
    ("State the principle of conservation of energy.", "Energy cannot be created or destroyed; it can only be transferred from one store to another.", ["Energy is used up when work is done.", "Energy is always created in power stations.", "Energy stores always stay full."], "The total energy stays the same."),
    ("What is work done?", "force × distance moved in the direction of the force", ["force × time", "mass × distance", "force ÷ distance"], "W = Fd, in joules."),
    ("Is work done when you hold a heavy bag still?", "No: the bag does not move in the direction of the force.", ["Yes: you feel tired.", "Yes: a force acts.", "Only if the bag is very heavy."], "No distance moved, no work done (on the bag)."),
    ("What is power?", "the rate of work done or energy transferred", ["the total energy used", "force × distance", "energy × time"], "P = W ÷ t, in watts."),
    ("What is 1 watt?", "1 joule per second", ["1 joule per hour", "1 newton per metre", "1 newton per second"], "1 W = 1 J/s."),
    ("Which energy store does a moving car have?", "kinetic", ["gravitational potential", "elastic potential", "nuclear"], "Moving objects store kinetic energy."),
    ("Which energy store increases when a lift raises passengers?", "gravitational potential", ["kinetic", "chemical potential", "elastic potential"], "Higher position, more GPE."),
    ("Which energy store is in food and fuels?", "chemical potential", ["kinetic", "nuclear", "elastic potential"], "Released in chemical reactions."),
    ("A car engine is 30% efficient. Where does most of the wasted energy go?", "thermal energy to the surroundings", ["back into the fuel", "into extra kinetic energy", "it disappears"], "Wasted energy heats the surroundings."),
    ("Why can no machine be more than 100% efficient?", "Energy cannot be created, so useful output cannot exceed input.", ["Machines are too heavy.", "Friction creates energy.", "It is not allowed by law."], "Conservation of energy."),
])
POOL5 = pool(R, [
    ("Which fuel generates about 95% of Singapore's electricity?", "natural gas", ["coal", "oil", "nuclear fuel"], "Natural gas is the cleanest fossil fuel, but it is still non-renewable."),
    ("Which renewable energy resource is best suited to Singapore?", "solar energy", ["hydroelectric energy", "geothermal energy", "wind energy"], "Singapore has strong sunlight but no large rivers, volcanoes or steady strong winds."),
    ("Give one disadvantage of solar panels in Singapore.", "They need a lot of space and give no electricity at night.", ["They release carbon dioxide.", "Sunlight will run out.", "They need fuel."], "Floating solar farms on reservoirs save land."),
    ("Why is burning natural gas better for the environment than burning coal?", "It releases less carbon dioxide for the same energy.", ["It releases no carbon dioxide.", "It is renewable.", "It never runs out."], "But it still adds to global warming."),
    ("A 50 kg skateboarder rolls down a 2 m ramp from rest. Ignoring friction, what is her kinetic energy at the bottom? (g = 10 N/kg)", "1000 J", ["100 J", "500 J", "10 000 J"], "GPE lost = mgh = 50 × 10 × 2 = 1000 J."),
    ("A pendulum swings. At which point is its kinetic energy greatest?", "at the lowest point of the swing", ["at the highest point", "halfway up", "it is the same everywhere"], "GPE is smallest there, so KE is largest."),
    ("A ball dropped from 2 m bounces back to only 1.5 m. Why?", "Some energy is transferred to thermal energy and sound in the bounce.", ["Energy is destroyed.", "Gravity is weaker.", "The ball gains mass."], "Energy is conserved but some is wasted."),
    ("A crane lifts a 500 kg load 20 m in 40 s. What is its useful power? (g = 10 N/kg)", "2500 W", ["100 000 W", "250 W", "1000 W"], "mgh = 100 000 J; 100 000 ÷ 40 = 2500 W."),
    ("Two students of equal mass run up the same stairs. A takes 5 s and B takes 10 s. Which is true?", "Both do the same work, but A has twice the power.", ["A does twice as much work.", "B has more power.", "They have the same power."], "Same mgh; P = W ÷ t."),
    ("A cyclist pushes with 80 N and travels 500 m against an equal resistive force. How much work does she do?", "40 000 J", ["580 J", "6.25 J", "400 J"], "W = Fd = 80 × 500."),
])


def main():
    sets = U.sets([
        ("Energy stores and conservation", [POOL1, (g_conv, 6), (g_res, 4)]),
        ("Kinetic and potential energy", [(g_ke, 8), (g_gpe, 8), (us_ke, 4)]),
        ("Work done and power", [(g_power, 8), (us_work, 4), (uk_work, 4), (uk_pow, 4)]),
        ("Efficiency and energy resources", [(g_eff, 9), (us_eff, 3), (uk_eff, 2), (g_res, 4), POOL1]),
        ("Energy changes and exam-style questions", [(POOL5, 10), (g_fall, 6), (g_conv, 2), (g_power, 2)]),
    ])
    make_ol(LV, SUBJ, "energy", SORT, "Energy",
            "Show understanding that energy can be stored in different stores and transferred by mechanical work, electrical work, heating and radiation; state and apply "
            "the principle of conservation of energy; recall and apply kinetic energy = ½mv² and gravitational potential energy = mgh; recall and apply work done = force × "
            "distance moved in the direction of the force and power = work done ÷ time taken; calculate efficiency; describe renewable and non-renewable energy resources "
            "and their advantages and disadvantages (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Energy, Work and Power", "Energy",
            "Free Secondary 3 O-Level Physics worksheets on energy: energy stores, conservation of energy, kinetic and potential energy, work done, power, efficiency and energy "
            "resources. 100 questions with answers.",
            "Energy is never created or destroyed.", "KE = ½mv², GPE = mgh, W = Fd, P = E ÷ t.",
            "<p><b>Energy is transferred between stores but the total stays the same.</b></p><ul>"
            "<li>Kinetic energy = ½mv². Gravitational potential energy = mgh (g = 10 N/kg).</li>"
            "<li>Work done = force × distance moved in the direction of the force (J). Power = work done ÷ time (W = J/s).</li>"
            "<li>Efficiency = useful energy output ÷ total energy input × 100%. Wasted energy is usually thermal energy.</li>"
            "<li>Renewable resources (solar, wind, hydro) are replaced naturally; fossil fuels and nuclear fuel will run out. Singapore uses mainly natural gas.</li></ul>",
            [("A 2 kg ball moves at 6 m/s. KE?", ["½ × 2 × 6²"], "36 J"),
             ("A 5 kg box is lifted 3 m. Gain in GPE?", ["5 × 10 × 3"], "150 J"),
             ("A ball falls 5 m. Speed at the bottom?", ["mgh = ½mv²", "v = √(2 × 10 × 5)"], "10 m/s")],
            ["Writing KE = mv² and forgetting the ½.", "Saying work is done when an object does not move.",
             "Mixing up power and energy: power is energy per second.", "Giving an efficiency above 100% after dividing the wrong way round."],
            [("How do you calculate efficiency?", "Divide the useful energy (or power) output by the total energy (or power) input and multiply by 100%."),
             ("How do kinetic and potential energy change when an object falls?", "Gravitational potential energy is transferred to kinetic energy. Without air resistance, mgh lost = ½mv² gained."),
             ("Is solar energy useful in Singapore?", "Yes. Singapore is sunny all year, so solar panels on rooftops and floating on reservoirs are its main renewable resource, but most electricity still comes from natural gas.")],
            sets)


if __name__ == "__main__":
    main()
