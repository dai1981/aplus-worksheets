# -*- coding: utf-8 -*-
"""
US High School Physics: Wave Properties (HS-PS4-1)
  python tools/gen_us_science_phys_wave_properties.py
Use mathematical representations to support a claim regarding relationships among the frequency, wavelength, and speed
of waves traveling in various media.
v = fλ, period T = 1/f, transverse and longitudinal waves, what changes when a wave enters a new medium (speed and
wavelength change, frequency stays), the speed of sound and light, and the electromagnetic spectrum.
Wrong answers come from real mistakes: "a higher frequency makes a wave faster in the same medium", "frequency changes
when a wave enters a new medium", "sound travels in a vacuum", "v = f ÷ λ".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, sci, uniq, safe

U = Unit(90312)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_vfl():
    k = R.choice(["v", "f", "l"])
    case = R.choice(["water", "string", "sound"])
    if case == "water":
        f = R.choice([0.2, 0.25, 0.5, 1, 2])
        l = R.choice([2, 4, 5, 8, 10, 20])
        desc = "ocean waves"
    elif case == "string":
        f = R.choice([50, 100, 200, 250, 400, 500])
        l = R.choice([0.2, 0.4, 0.5, 0.8, 1, 1.2])
        desc = "a wave on a guitar string"
    else:
        f = R.choice([170, 343, 686, 1372, 100, 200])
        l = 343 / f
        desc = "a sound wave in air"
    v = f * l
    if v != round(v, 2) or l != round(l, 3) or not once(("vf", case, f, l, k)):
        return None
    if k == "v":
        g = "%s m/s" % num(v)
        return item("For %s, the frequency is %s Hz and the wavelength is %s m. What is the wave speed?" % (desc, num(f), num(l, 3)), g,
                    uniq(g, ["%s m/s" % num(f / l, 2), "%s m/s" % num(l / f, 4), "%s m/s" % num(f + l, 2), "%s m/s" % num(v * 2)]), "v = fλ = %s × %s = %s m/s." % (num(f), num(l, 3), num(v)))
    if k == "f":
        g = "%s Hz" % num(f)
        return item("For %s, the speed is %s m/s and the wavelength is %s m. What is the frequency?" % (desc, num(v), num(l, 3)), g,
                    uniq(g, ["%s Hz" % num(v * l, 2), "%s Hz" % num(l / v, 4), "%s Hz" % num(f * 2), "%s Hz" % num(v)]), "f = v ÷ λ = %s ÷ %s = %s Hz." % (num(v), num(l, 3), num(f)))
    g = "%s m" % num(l, 3)
    return item("For %s, the speed is %s m/s and the frequency is %s Hz. What is the wavelength?" % (desc, num(v), num(f)), g,
                uniq(g, ["%s m" % num(v * f, 2), "%s m" % num(f / v, 3), "%s m" % num(l * 2, 3), "%s m" % num(v, 2)]), "λ = v ÷ f = %s ÷ %s = %s m." % (num(v), num(f), num(l, 3)))


@safe
def g_period():
    k = R.choice(["T", "f"])
    f = R.choice([0.5, 1, 2, 4, 5, 10, 20, 25, 50, 100])
    T = 1 / f
    if not once(("pd", f, k)):
        return None
    if k == "T":
        g = "%s s" % num(T, 3)
        return item("A wave has a frequency of %s Hz. What is its period?" % num(f), g, uniq(g, ["%s s" % num(f), "%s s" % num(T * 2, 3), "%s s" % num(f * 2), "1 s"]), "T = 1 ÷ f = 1 ÷ %s = %s s." % (num(f), num(T, 3)))
    g = "%s Hz" % num(f)
    return item("A buoy bobs up and down once every %s s. What is the frequency of the waves?" % num(T, 3), g, uniq(g, ["%s Hz" % num(T, 3), "%s Hz" % num(f * 2), "%s Hz" % num(f / 2, 2), "1 Hz"]),
                "f = 1 ÷ T = 1 ÷ %s = %s Hz." % (num(T, 3), num(f)))


MED = [("air", 343), ("water", 1480), ("steel", 5960), ("glass", 4540), ("wood", 3850), ("helium", 965)]


@safe
def g_medium():
    (a, va), (b, vb) = R.sample(MED, 2)
    f = R.choice([100, 200, 250, 400, 500, 1000])
    k = R.choice(["l", "f", "which"])
    if not once(("md", a, b, f, k)):
        return None
    la, lb = va / f, vb / f
    if k == "f":
        g = "%s Hz (it does not change)" % num(f)
        return item("A %s Hz sound goes from %s (%s m/s) into %s (%s m/s). What is its frequency in %s?" % (num(f), a, num(va), b, num(vb), b), g,
                    uniq(g, ["%s Hz" % num(f * vb / va, 1), "%s Hz" % num(f * va / vb, 1), "0 Hz"]), "The source sets the frequency; speed and wavelength change.")
    if k == "l":
        g = "%s m" % num(lb, 3)
        return item("A %s Hz sound wave goes from %s (%s m/s) into %s (%s m/s). What is its wavelength in %s?" % (num(f), a, num(va), b, num(vb), b), g,
                    uniq(g, ["%s m" % num(la, 3), "%s m" % num(vb * f, 0), "%s m" % num(f / vb, 4), "%s m" % num(lb * 2, 3)]), "λ = v ÷ f = %s ÷ %s = %s m." % (num(vb), num(f), num(lb, 3)))
    longer = b if vb > va else a
    return item("The same %s Hz sound travels through %s (%s m/s) and %s (%s m/s). In which does it have the longer wavelength?" % (num(f), a, num(va), b, num(vb)), longer,
                [a if longer == b else b, "They have the same wavelength.", "Sound has no wavelength."], "Same frequency: faster speed → longer wavelength.")


EMS = ["radio waves", "microwaves", "infrared", "visible light", "ultraviolet", "X-rays", "gamma rays"]


@safe
def g_em():
    a, b = sorted(R.sample(range(7), 2))
    k = R.choice(["f", "l", "e"])
    if not once(("em", a, b, k)):
        return None
    if k == "f":
        return item("Which has a higher frequency: %s or %s?" % (EMS[a], EMS[b]), EMS[b], [EMS[a], "They have the same frequency.", "It depends on their speed."], "Order: radio → microwave → infrared → visible → UV → X-ray → gamma.")
    if k == "l":
        return item("Which has a longer wavelength: %s or %s?" % (EMS[b], EMS[a]), EMS[a], [EMS[b], "They have the same wavelength.", "Neither has a wavelength."], "Lower frequency → longer wavelength.")
    return item("In a vacuum, how do the speeds of %s and %s compare?" % (EMS[a], EMS[b]), "They are the same (3.0 × 10<sup>8</sup> m/s).", ["%s are faster." % EMS[b].capitalize(), "%s are faster." % EMS[a].capitalize(), "Neither can travel in a vacuum."],
                "All EM waves travel at the speed of light in a vacuum.")


def fm(x):
    return num(x, 3) if 0.01 <= x < 100000 else sci(x)


@safe
def g_light():
    k = R.choice(["f", "l"])
    c = 3e8
    if k == "f":
        l = R.choice([1, 2, 3, 5, 10, 100, 0.1, 0.03, 300])
        f = c / l
        if not once(("lf", l)):
            return None
        g = "%s Hz" % sci(f)
        return item("A radio or microwave signal has a wavelength of %s m. What is its frequency? (c = 3.0 × 10<sup>8</sup> m/s)" % num(l), g,
                    uniq(g, ["%s Hz" % fm(c * l), "%s Hz" % fm(l / c), "%s Hz" % fm(f * 10), "%s Hz" % fm(f / 10)]), "f = c ÷ λ = 3.0 × 10<sup>8</sup> ÷ %s = %s Hz." % (num(l), fm(f)))
    f = R.choice([1e6, 1e8, 3e8, 6e8, 1e9, 2.4e9, 5e9, 1.5e10, 3e12])
    l = c / f
    if not once(("ll", f)):
        return None
    g = "%s m" % fm(l)
    return item("A signal has a frequency of %s Hz. What is its wavelength? (c = 3.0 × 10<sup>8</sup> m/s)" % fm(f), g,
                uniq(g, ["%s m" % fm(c * f), "%s m" % fm(f / c), "%s m" % fm(l * 10), "%s m" % fm(l / 10)]),
                "λ = c ÷ f = %s m." % fm(l))


B1 = bank([
    ("What does the frequency of a wave measure?", "the number of waves that pass a point each second", ["the height of the wave", "the distance between crests", "the speed of the wave"], "Units: hertz (Hz)."),
    ("What is wavelength?", "the distance from one crest to the next", ["the height of a crest", "the time for one wave", "the number of waves per second"], "Symbol λ."),
    ("What is the equation that links wave speed, frequency and wavelength?", "v = fλ", ["v = f ÷ λ", "v = λ ÷ f", "v = f + λ"], "Speed = frequency × wavelength."),
    ("What is amplitude a measure of?", "how much energy the wave carries (its height from the rest position)", ["its speed", "its frequency", "its wavelength"], "Bigger amplitude = louder or brighter."),
    ("Which is a longitudinal wave?", "a sound wave in air", ["a wave on a rope shaken up and down", "light", "a ripple seen from above as up and down motion only"], "Particles vibrate along the direction of travel."),
    ("Why can't sound travel through space?", "Sound needs a medium (particles) to travel through.", ["Space is too cold.", "Sound is too fast.", "Sound is light."], "Mechanical wave."),
    ("In the same medium, what happens to wavelength if frequency doubles?", "It is cut in half.", ["It doubles.", "It stays the same.", "It becomes zero."], "Speed is fixed by the medium."),
    ("Which travels fastest?", "light in a vacuum", ["sound in steel", "sound in air", "ocean waves"], "3.0 × 10⁸ m/s."),
])
B5 = bank([
    ("You see lightning and hear thunder 3 s later. About how far away was the strike? (sound: 343 m/s)", "about 1 km", ["about 3 km", "about 100 m", "about 343 km"], "343 × 3 ≈ 1,029 m."),
    ("Why do whales communicate over long distances using low-frequency sounds?", "Low-frequency sound travels farther in water with less loss.", ["Low sounds travel faster.", "High sounds cannot exist in water.", "Whales cannot make high sounds."], "Attenuation."),
    ("A student measures waves in a ripple tank: 5 waves pass in 2 s and the wavelength is 4 cm. What is the speed?", "10 cm/s", ["20 cm/s", "2.5 cm/s", "40 cm/s"], "f = 2.5 Hz; 2.5 × 4."),
    ("Why does light bend when it enters water from air?", "Its speed changes in the new medium.", ["Its frequency changes.", "Water absorbs all the light.", "Light stops in water."], "Refraction."),
    ("Doctors use ultrasound for images of babies. Why high frequency?", "Short wavelengths show small details.", ["It is louder.", "It travels in a vacuum.", "It is slower than light."], "Resolution."),
])


def body():
    think = ("<p><b>Wave speed = frequency × wavelength (v = fλ).</b></p>"
             "<ul><li>The medium sets the speed. In one medium, higher frequency means shorter wavelength.</li>"
             "<li>When a wave enters a new medium, its speed and wavelength change, but its frequency stays the same.</li>"
             "<li>Period T = 1 ÷ f. All electromagnetic waves travel at 3.0 × 10<sup>8</sup> m/s in a vacuum.</li></ul>")
    ex = [("Sound: 343 m/s, 686 Hz. λ?", ["343 ÷ 686"], "0.5 m"),
          ("Frequency 4 Hz. Period?", ["1 ÷ 4"], "0.25 s")]
    mist = ["Thinking a higher frequency makes a wave faster in the same medium.", "Thinking frequency changes when a wave enters a new medium.", "Writing v = f ÷ λ."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Describing waves", B1 + [(g_period, 6), (g_vfl, 6)]),
        ("v = fλ", [(g_vfl, 16), (g_period, 4)]),
        ("Waves in different media", [(g_medium, 14), (g_vfl, 6)]),
        ("The electromagnetic spectrum", [(g_em, 12), (g_light, 8)]),
        ("Waves in the real world", B5 + [(g_light, 5), (g_medium, 5), (g_em, 5)]),
    ])
    make("physics", "wave-properties", 12, "HS-PS4-1",
         "Use mathematical representations to support a claim regarding relationships among the frequency, wavelength, and speed of waves traveling in various media.",
         "Wave Properties",
         "Wave Worksheets: v = fλ, Frequency, Wavelength and the EM Spectrum (High School Physics)",
         "Wave Properties",
         "Free high school physics worksheets on wave properties (NGSS HS-PS4-1): v = fλ, period, waves in different media, sound and light, and the electromagnetic spectrum. 100 questions with answers.",
         "Speed = frequency × wavelength.",
         "The medium sets the speed; in a new medium the wavelength changes but the frequency stays.",
         body(),
         [("How are wave speed, frequency and wavelength related?", "v = fλ. If the speed stays the same, a higher frequency means a shorter wavelength."),
          ("What changes when a wave enters a new medium?", "Its speed and wavelength change. Its frequency stays the same because it is set by the source."),
          ("How fast do electromagnetic waves travel?", "All electromagnetic waves travel at 3.0 × 10⁸ m/s in a vacuum.")],
         sets)


if __name__ == "__main__":
    main()
