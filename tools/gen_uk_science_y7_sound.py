# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Physics): Sound
  python tools/gen_uk_science_y7_sound.py
Sound as vibrations travelling through a medium as pressure waves; frequencies of sound waves in hertz; loudness and
amplitude, pitch and frequency; echoes, reflection and absorption of sound; speed of sound in air, water and solids;
sound needs a medium (no sound in a vacuum); the ear and auditory range of humans and animals; echo and distance
calculations.
Wrong answers come from real mistakes: "sound travels fastest in air", "sound can travel through space",
"a louder sound has a higher frequency", "the echo time is the time to reach the wall".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61711)
R = U.R
P = People(R)


def C(n):
    return "{:,}".format(n)


def g_echo():
    v = R.choice([330, 340])
    t = R.choice([0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0])
    k = R.random() < 0.5
    if not once(("ec", v, t, k)):
        return None
    if k:
        d = round(v * t)
        g = "%s m" % C(d)
        return item("Sound travels at %d m/s in air. How far does sound travel in %g s?" % (v, t), g, uniq(g, ["%s m" % C(round(d / 2)), "%s m" % C(round(v / t)), "%g m" % t, "%s m" % C(d * 2)]),
                    "Distance = speed × time = %d × %g = %s m." % (v, t, C(d)))
    d = round(v * t / 2)
    g = "%s m" % C(d)
    return item("A pupil claps near a wall and hears the echo %g s later. Sound travels at %d m/s. How far away is the wall?" % (t, v), g,
                uniq(g, ["%s m" % C(round(v * t)), "%s m" % C(round(v / t)), "%s m" % C(d + 10), "%g m" % t]),
                "The sound goes there and back: %d × %g = %s m, so the wall is %s m away." % (v, t, C(round(v * t)), C(d)))


RANGE = [("humans", 20, 20000), ("dogs", 40, 60000), ("cats", 50, 80000), ("bats", 2000, 110000), ("elephants", 5, 12000), ("dolphins", 75, 150000)]


def g_range():
    a, lo, hi = R.choice(RANGE)
    f = R.choice([10, 30, 1000, 15000, 25000, 70000, 100000, 130000])
    can = lo <= f <= hi
    if not once(("ra", a, f)):
        return None
    tab = table(["Animal", "Hearing range (Hz)"], [[x[0], "%s–%s" % (C(x[1]), C(x[2]))] for x in RANGE])
    return item(tab + "Can %s hear a sound with a frequency of %s Hz?" % (a, C(f)), "Yes" if can else "No",
                ["No" if can else "Yes", "Only if it is loud enough to see", "Only under water"], "Check whether %s Hz is inside the range %s–%s Hz." % (C(f), C(lo), C(hi)))


def g_wave():
    a1, a2 = R.sample([2, 3, 4, 5, 6, 8], 2)
    f1, f2 = R.sample([100, 200, 256, 440, 500, 800, 1000], 2)
    k = R.choice(["loud", "pitch", "quiet", "low"])
    if not once(("wa", a1, a2, f1, f2, k)):
        return None
    tab = table(["Sound", "Amplitude (mm on the screen)", "Frequency (Hz)"], [["A", str(a1), C(f1)], ["B", str(a2), C(f2)]])
    if k == "loud":
        a = "A" if a1 > a2 else "B"
        return item(tab + "Which sound is louder?", "sound " + a, ["sound " + ("B" if a == "A" else "A"), "they are equally loud", "you cannot tell"], "A bigger amplitude means a louder sound.")
    if k == "quiet":
        a = "A" if a1 < a2 else "B"
        return item(tab + "Which sound is quieter?", "sound " + a, ["sound " + ("B" if a == "A" else "A"), "they are equally loud", "you cannot tell"], "A smaller amplitude means a quieter sound.")
    if k == "pitch":
        a = "A" if f1 > f2 else "B"
        return item(tab + "Which sound has the higher pitch?", "sound " + a, ["sound " + ("B" if a == "A" else "A"), "they have the same pitch", "the louder one"], "A higher frequency means a higher pitch.")
    a = "A" if f1 < f2 else "B"
    return item(tab + "Which sound has the lower pitch?", "sound " + a, ["sound " + ("B" if a == "A" else "A"), "they have the same pitch", "the quieter one"], "A lower frequency means a lower pitch.")


EAR = [("the eardrum", "vibrates when sound waves reach it"), ("the ossicles (small ear bones)", "passes the vibrations on and makes them bigger"),
       ("the cochlea", "turns vibrations into electrical signals"), ("the auditory nerve", "carries the signals to the brain"), ("the outer ear", "collects sound and funnels it into the ear canal")]


def g_ear():
    p, d = R.choice(EAR)
    k = R.random() < 0.5
    if not once(("ea", p, k)):
        return None
    if k:
        return item("What does %s do?" % p, "It " + d + ".", ["It " + x[1] + "." for x in R.sample([x for x in EAR if x[0] != p], 3)], "Outer ear → eardrum → ossicles → cochlea → auditory nerve → brain.")
    return item("Which part of the ear %s?" % d, p, R.sample([x[0] for x in EAR if x[0] != p], 3), "Outer ear → eardrum → ossicles → cochlea → auditory nerve → brain.")


MED = [("steel", 5000), ("water", 1500), ("air", 340), ("wood", 3800), ("glass", 4500)]


def g_med():
    ms = R.sample(MED, 3)
    k = R.choice(["fast", "slow"])
    if not once(("me", tuple(m[0] for m in ms), k)):
        return None
    tab = table(["Material", "Speed of sound (m/s)"], [[m, C(v)] for m, v in ms])
    if k == "fast":
        a = max(ms, key=lambda m: m[1])[0]
        return item(tab + "In which material does sound travel fastest?", a, [m[0] for m in ms if m[0] != a] + ["in a vacuum"], "Sound usually travels fastest in solids, then liquids, then gases.")
    a = min(ms, key=lambda m: m[1])[0]
    return item(tab + "In which material does sound travel slowest?", a, [m[0] for m in ms if m[0] != a] + ["in a vacuum"], "Particles are furthest apart in gases.")


B1 = bank([
    ("What causes sound?", "vibrations", ["light", "magnets", "heat only"], "Something must vibrate."),
    ("Can sound travel through space?", "No. Space is a vacuum with no particles to carry the vibrations.", ["Yes, very fast.", "Yes, but only loud sounds.", "Only near the Sun."], "Sound needs a medium."),
    ("What is the unit of frequency?", "hertz (Hz)", ["newtons (N)", "metres (m)", "decibels per second"], "Vibrations per second."),
    ("What does the frequency of a sound affect?", "its pitch", ["its loudness", "its speed in air", "its colour"], "High frequency, high pitch."),
    ("What does the amplitude of a sound wave affect?", "its loudness", ["its pitch", "its speed", "its direction"], "Bigger amplitude, louder."),
    ("What is an echo?", "a sound reflected from a hard surface", ["a sound absorbed by curtains", "a very high-pitched sound", "a sound in a vacuum"], "Reflection of sound."),
    ("What is the range of human hearing?", "about 20 Hz to 20,000 Hz", ["about 1 Hz to 100 Hz", "about 20,000 Hz to 100,000 Hz", "all frequencies"], "It shrinks as we age."),
    ("What is ultrasound?", "sound with a frequency above 20,000 Hz", ["sound below 20 Hz", "a very loud sound", "light we cannot see"], "Used to scan babies."),
])
B5 = bank([
    ("Why are cinemas and music studios lined with soft materials?", "Soft materials absorb sound and stop echoes.", ["They reflect sound better.", "They make sound faster.", "They make it quieter outside only."], "Absorption."),
    ("Why do you see lightning before you hear thunder?", "Light travels much faster than sound.", ["Thunder happens later.", "Sound travels faster than light.", "Your ears are slower than your eyes."], "Speeds differ."),
    ("How do bats find their food in the dark?", "They make high-pitched sounds and listen for the echoes.", ["They see with infrared.", "They smell everything.", "They use magnets."], "Echolocation."),
    ("A bell ringing inside a jar goes quiet as the air is pumped out. Why?", "With less air there are fewer particles to carry the sound.", ["The bell stops vibrating.", "Glass blocks all sound.", "The bell gets cold."], "Sound needs a medium."),
    ("Why should people wear ear defenders near loud machines?", "Very loud sounds can damage the ear permanently.", ["To hear the machines better.", "To keep their ears warm.", "To make sounds higher."], "Protect hearing."),
])


def body():
    think = ("<p><b>Sound is a vibration that travels through a medium as a pressure wave.</b></p>"
             "<ul><li>Bigger amplitude: louder. Higher frequency (Hz): higher pitch. Humans hear about 20–20,000 Hz.</li>"
             "<li>Sound travels fastest in solids and cannot travel through a vacuum. In air it is about 340 m/s.</li>"
             "<li>Echoes are reflected sound. For an echo, the sound goes there and back, so halve the distance.</li></ul>")
    ex = [("Echo after 2 s at 340 m/s. Wall distance?", ["340 × 2 = 680 m there and back"], "340 m"),
          ("Which is louder: amplitude 6 mm or 3 mm?", ["Bigger amplitude"], "6 mm")]
    mist = ["Thinking sound travels fastest in air.", "Thinking sound can travel through space.", "Thinking a louder sound has a higher frequency."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Vibrations and waves", B1 + [(g_wave, 12)]),
        ("Loudness and pitch", [(g_wave, 10), (g_ear, 5), (g_med, 5)]),
        ("Hearing", [(g_range, 12), (g_ear, 4), (g_med, 4)]),
        ("Echoes and speed", [(g_echo, 20)]),
        ("Thinking about sound", B5 + [(g_echo, 8), (g_range, 7)]),
    ])
    make_ks3(7, "sound", 11, "Physics", "Waves",
             "Frequencies of sound waves, measured in hertz (Hz); echoes, reflection and absorption of sound; sound needs a medium to travel, the speed of sound in air, in water, in solids; sound produced by vibrations of objects, in loudspeakers, detected by their effects on microphone diaphragm and the ear drum; sound waves are longitudinal; auditory range of humans and animals; pressure waves transferring energy.",
             "Sound",
             "Year 7 Science: Sound Worksheets (Frequency, Amplitude, Echoes, Hearing)",
             "Sound",
             "Free Year 7 science worksheets on sound: vibrations, frequency and pitch, amplitude and loudness, the speed of sound, echoes, the ear and hearing ranges of animals. 100 questions with answers.",
             "Sound is vibrations travelling through a medium.",
             "Amplitude sets loudness; frequency sets pitch. No sound in a vacuum.",
             body(),
             [("How does sound travel?", "A vibrating object makes the particles next to it vibrate, and the vibrations pass from particle to particle as a pressure wave. Sound cannot travel through a vacuum."),
              ("What is the difference between pitch and loudness?", "Pitch depends on frequency (how many vibrations per second). Loudness depends on amplitude (how big the vibrations are)."),
              ("How do you work out distance from an echo?", "Multiply the speed of sound by the time to get the distance there and back, then halve it.")],
             sets)


if __name__ == "__main__":
    main()
