# -*- coding: utf-8 -*-
"""
US High School Physics: Wave Technologies (HS-PS4-5)
  python tools/gen_us_science_phys_wave_technologies.py
Communicate technical information about how some technological devices use the principles of wave behavior and wave
interactions with matter to transmit and capture information and energy.
Sonar, ultrasound and echolocation (d = vt ÷ 2), radar and GPS timing, fiber optics (total internal reflection),
noise-cancelling headphones (interference), solar cells, medical imaging and wireless communication.
Wrong answers come from real mistakes: "forget to halve the echo time", "fiber optics carry electricity",
"noise cancelling adds more sound", "radio signals travel at the speed of sound".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, sci, uniq, safe

U = Unit(90316)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


DEV = [("sonar on a ship", "sound waves that reflect off the sea floor"), ("a medical ultrasound scanner", "high-frequency sound that reflects at boundaries between tissues"),
       ("a fiber-optic internet cable", "light trapped by total internal reflection"), ("noise-cancelling headphones", "a sound wave that cancels noise by destructive interference"),
       ("a solar cell", "photons that free electrons in a semiconductor"), ("a TV remote control", "pulses of infrared light"), ("a cell phone", "radio waves (microwaves) carrying digital signals"),
       ("a GPS receiver", "timed radio signals from several satellites"), ("a radar speed gun", "microwaves that reflect off a car and change frequency (Doppler effect)"),
       ("an X-ray machine", "X-rays absorbed more by bone than by soft tissue"), ("a barcode scanner", "a laser beam reflected by black and white stripes"),
       ("a microwave oven", "microwaves absorbed by water molecules in food")]


@safe
def g_dev():
    d, w = R.choice(DEV)
    k = R.random() < 0.55
    if not once(("dv", d, k)):
        return None
    if k:
        return item("What does %s use to work?" % d, w, R.sample([x[1] for x in DEV if x[1] != w], 3), "Devices use waves to send or capture information and energy.")
    return item("Which device uses %s?" % w, d, R.sample([x[0] for x in DEV if x[0] != d], 3), "Match the device to the wave principle.")


@safe
def g_echo():
    who = P.next()[0]
    case = R.choice([("A ship's sonar pulse", "the sea floor", 1480), ("A bat's click", "a moth", 343), ("An ultrasound pulse in the body", "an organ", 1540), ("A dolphin's click", "a fish", 1480)])
    t = R.choice([0.02, 0.04, 0.1, 0.2, 0.5, 1, 2, 4]) if case[2] == 1480 else R.choice([0.01, 0.02, 0.04, 0.05, 0.1]) if case[2] == 343 else R.choice([0.0001, 0.0002, 0.00005])
    d = case[2] * t / 2
    if not once(("ec", case[0], t)):
        return None
    unit = "m" if d >= 1 else "cm"
    val = d if unit == "m" else d * 100
    g = "%s %s" % (num(val, 2), unit)
    w = [case[2] * t, case[2] / t, case[2] * t / 4, case[2] * t * 2]
    w = ["%s %s" % (num(x if unit == "m" else x * 100, 2), unit) for x in w]
    return item("%s returns as an echo from %s after %s s. The wave travels at %s m/s. How far away is %s?" % (case[0], case[1], num(t, 5), num(case[2]), "the " + case[1].split(" ", 1)[1] if case[1].startswith(("a ", "an ")) else case[1]), g, uniq(g, w),
                "d = v × t ÷ 2 = %s × %s ÷ 2 = %s %s (the wave goes there and back)." % (num(case[2]), num(t, 5), num(val, 2), unit))


@safe
def g_time():
    c = 3e8
    case = R.choice([("a GPS satellite", 20200), ("the Moon", 384000), ("a satellite in low orbit", 400), ("a geostationary satellite", 35800), ("a cell tower", 5), ("Mars (at its closest)", 56000000)])
    k = R.choice(["t", "x"])
    if not once(("tm", case[0], k)):
        return None
    d = case[1] * 1000
    t = d / c
    if k == "t":
        g = "%s s" % (num(t, 4) if t >= 0.0001 else sci(t))
        w = [d / 343, d * c, t * 2, t / 1000]
        w = ["%s s" % (num(x, 4) if 0.0001 <= x < 1e6 else sci(x)) for x in w]
        return item("A radio signal travels from %s to Earth, a distance of %s km. How long does it take? (c = 3.0 × 10<sup>8</sup> m/s)" % (case[0], num(case[1])), g, uniq(g, w),
                    "t = d ÷ c = %s m ÷ 3.0 × 10<sup>8</sup> m/s = %s s." % (sci(d), g[:-2]))
    if t < 0.01:
        return None
    g = "about %s s" % num(2 * t, 2)
    return item("A radar or laser pulse is sent to %s (%s km away) and reflects back. About how long until the echo returns?" % (case[0], num(case[1])), g,
                uniq(g, ["about %s s" % num(t, 2), "about %s s" % num(4 * t, 2), "about %s s" % num(2 * d / 343, 0), "instantly"]), "There and back: 2d ÷ c = %s s." % num(2 * t, 2))


@safe
def g_int():
    a1 = R.choice([1, 2, 3, 4, 5, 6])
    a2 = R.choice([1, 2, 3, 4, 5, 6])
    k = R.choice(["con", "des"])
    if not once(("ia", a1, a2, k)):
        return None
    if k == "con":
        g = "%d cm" % (a1 + a2)
        return item("Two waves with amplitudes %d cm and %d cm meet crest to crest. What is the amplitude where they overlap?" % (a1, a2), g, uniq(g, ["%d cm" % abs(a1 - a2), "%d cm" % max(a1, a2), "%d cm" % (a1 * a2), "0 cm"]),
                    "Constructive interference: add.")
    g = "%d cm" % abs(a1 - a2)
    return item("Two waves with amplitudes %d cm and %d cm meet crest to trough. What is the amplitude where they overlap?" % (a1, a2), g, uniq(g, ["%d cm" % (a1 + a2), "%d cm" % max(a1, a2), "%d cm" % (a1 * a2), "%d cm" % min(a1, a2)]),
                "Destructive interference: subtract.")


B1 = bank([
    ("How does an echo help find distance?", "Time the echo and use d = speed × time ÷ 2.", ["Measure how loud the echo is only.", "Count the waves.", "Use the color of the sound."], "There and back."),
    ("Why can light travel along a bent optical fiber?", "Total internal reflection keeps the light inside the glass.", ["The fiber carries electricity.", "Light bends around corners by itself.", "The fiber is hollow and full of air."], "Critical angle."),
    ("How do noise-cancelling headphones work?", "They make a sound wave that is the opposite of the noise, so the waves cancel.", ["They make the noise louder.", "They block all air.", "They use light waves."], "Destructive interference."),
    ("Why do doctors use ultrasound instead of X-rays to check on a growing baby?", "Ultrasound is non-ionizing and safe for the baby.", ["Ultrasound is ionizing.", "X-rays cannot pass through skin.", "Ultrasound is a type of light."], "Safety."),
    ("What do cell phones use to send calls?", "radio waves (microwaves) carrying digital signals", ["sound waves through the air", "X-rays", "visible light only"], "EM communication."),
    ("How does a solar cell capture energy?", "Photons of light free electrons in the material, making a current.", ["It burns the light.", "It reflects all light.", "It uses sound waves."], "Photoelectric effect."),
    ("How does GPS find your position?", "It times radio signals from several satellites to find distances.", ["It uses sound from satellites.", "It measures gravity.", "It uses cell-phone cameras."], "Timing and trilateration."),
    ("Why do fiber-optic cables carry more data than copper wires?", "Light has a very high frequency, so it can carry much more information.", ["Light is slower.", "Copper is lighter.", "Fibers carry sound."], "Bandwidth."),
])
B5 = bank([
    ("Why do ultrasound scanners use high frequencies (millions of Hz)?", "Shorter wavelengths show smaller details.", ["High frequencies are louder.", "They travel faster than light.", "They are ionizing."], "Resolution."),
    ("Why do submarines use sonar instead of radar underwater?", "Radio waves are absorbed by seawater, but sound travels well in water.", ["Sound is faster than light.", "Radar is too loud.", "Water blocks sound."], "Choose the right wave."),
    ("A team designs a cheaper hearing aid. Which wave behavior helps cut background noise?", "destructive interference", ["total internal reflection", "the photoelectric effect", "ionization"], "Apply wave principles."),
    ("Why do satellite dishes have a curved shape?", "The curve reflects incoming waves to one focus where the receiver sits.", ["To look nice.", "To block rain.", "To slow the waves."], "Reflection."),
    ("Why do signals from Mars rovers take minutes to arrive?", "Even at the speed of light, the distance is huge.", ["Radio waves are slow.", "Mars has no air.", "The rover waits before sending."], "Time = distance ÷ speed."),
])


def body():
    think = ("<p><b>Technology uses waves to carry information and energy.</b></p>"
             "<ul><li>Echoes (sonar, ultrasound, radar): distance = speed × time ÷ 2.</li>"
             "<li>Fiber optics trap light by total internal reflection; noise cancelling uses destructive interference.</li>"
             "<li>Radio, microwaves and light all travel at 3.0 × 10<sup>8</sup> m/s; sound is much slower.</li></ul>")
    ex = [("Sonar echo after 2 s in water (1,480 m/s)?", ["1,480 × 2 ÷ 2"], "1,480 m"),
          ("Amplitudes 4 cm and 3 cm, crest meets trough?", ["4 − 3"], "1 cm")]
    mist = ["Forgetting to halve the echo time.", "Thinking fiber optics carry electricity.", "Thinking radio waves travel at the speed of sound."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Waves in devices", B1 + [(g_dev, 12)]),
        ("Echoes and distance", [(g_echo, 14), (g_dev, 6)]),
        ("Signals at light speed", [(g_time, 7), (g_int, 13)]),
        ("Interference", [(g_int, 14), (g_dev, 4), (g_echo, 2)]),
        ("Communicating with waves", B5 + [(g_echo, 6), (g_int, 7), (g_time, 2)]),
    ])
    make("physics", "wave-technologies", 16, "HS-PS4-5",
         "Communicate technical information about how some technological devices use the principles of wave behavior and wave interactions with matter to transmit and capture information and energy.",
         "Wave Technologies",
         "Wave Technology Worksheets: Sonar, Fiber Optics, GPS and Noise Cancelling (Physics)",
         "Wave Technologies",
         "Free high school physics worksheets on wave technologies (NGSS HS-PS4-5): sonar and ultrasound echoes, radar and GPS timing, fiber optics, interference and solar cells. 100 questions with answers.",
         "Devices use waves to send information.",
         "Echoes measure distance; light, radio and interference carry and clean up signals.",
         body(),
         [("How does sonar measure distance?", "It times an echo. The sound goes to the object and back, so distance = speed × time ÷ 2."),
          ("How do fiber-optic cables work?", "Light reflects off the inside walls of the glass fiber again and again (total internal reflection), carrying data as flashes of light."),
          ("How do noise-cancelling headphones work?", "They record the noise and play an opposite wave. Crest meets trough, so the waves cancel by destructive interference.")],
         sets)


if __name__ == "__main__":
    main()
