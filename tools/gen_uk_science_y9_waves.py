# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Physics): Waves
  python tools/gen_uk_science_y9_waves.py
Waves transferring energy, transverse and longitudinal waves, amplitude, wavelength and frequency (hertz), wave speed
= frequency × wavelength, sound needing a medium and light travelling through a vacuum, the speed of sound and of
light, echoes, the auditory range and ultrasound, and reflection, absorption and transmission of waves. Reuses the
wave and light-and-sound questions of the US Grade 8 units in British English.
Wrong answers come from real mistakes: "waves carry matter along", "sound travels through space",
"higher frequency means a louder sound", "an echo time is the one-way time".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61910)
R = U.R
P = People(R)
uk_sci.USED.clear()
WP = adopt_us("gen_us_science_g8_wave_properties", U)
LS = adopt_us("gen_us_science_g8_light_and_sound_waves", U)
us_read, us_rel, us_speed = ukm(WP.g_read), ukm(WP.g_rel), ukm(WP.g_speed)
us_sound, us_what = ukm(LS.g_sound), ukm(LS.g_what)

TYPE = [("light", "transverse"), ("ripples on water", "transverse"), ("sound", "longitudinal"), ("radio waves", "transverse"), ("a wave along a stretched slinky pushed back and forth", "longitudinal"),
        ("a wave on a rope shaken up and down", "transverse"), ("ultrasound", "longitudinal"), ("X-rays", "transverse")]


def g_type():
    w, t = R.choice(TYPE)
    if not once(("ty", w)):
        return None
    return item("Is %s a transverse or a longitudinal wave?" % w, t, [x for x in ["transverse", "longitudinal", "neither: it is not a wave", "both at once"] if x != t],
                "Transverse: vibrations at right angles to the direction of travel. Longitudinal: vibrations along it.")


def g_echo():
    who = P.next()[0]
    t = R.choice([0.2, 0.4, 0.5, 0.6, 1, 1.2, 1.5, 2, 3])
    v = R.choice([("in air", 340), ("in water (sonar)", 1500)])
    if not once(("ec", t, v[1])):
        return None
    d = v[1] * t / 2
    g = "{:,} m".format(int(d)) if d == int(d) else "{:,} m".format(d)
    return item("%s hears an echo %s s after making a sound %s. Sound travels at {:,} m/s %s. How far away is the reflecting surface?".format(v[1]) % (who, "{:g}".format(t), "" if v[0] == "in air" else "with a ship's sonar", v[0]), g,
                uniq(g, ["{:,} m".format(v[1] * t if v[1] * t != int(v[1] * t) else int(v[1] * t)), "{:,} m".format(int(v[1] / t)) if v[1] / t == int(v[1] / t) else "{:,} m".format(v[1]), "{:,} m".format(v[1]), "{:,} m".format(int(d) + 100)]),
                "The sound goes there and back: distance = speed × time ÷ 2 = {:,} × {:g} ÷ 2.".format(v[1], t))


HEAR = [("Which frequencies can most young humans hear?", "about 20 Hz to 20,000 Hz", ["about 1 Hz to 10 Hz", "about 20,000 Hz to 100,000 Hz", "all frequencies"]),
        ("What is ultrasound?", "sound with a frequency above about 20,000 Hz, too high for humans to hear", ["very loud sound", "sound below 20 Hz", "a type of light"]),
        ("What does a higher frequency sound like?", "a higher pitch", ["louder", "quieter", "a lower pitch"]),
        ("What does a bigger amplitude sound like?", "louder", ["higher pitched", "lower pitched", "faster"]),
        ("Why does the range of hearing get smaller as people get older?", "The ear is damaged over time, especially for high frequencies.", ["Sound gets quieter each year.", "The brain grows.", "Ears grow bigger."]),
        ("How do bats find insects in the dark?", "They send out ultrasound and listen for the echoes.", ["They use their eyes only.", "They smell the insects.", "They use light from the Moon."]),
        ("What is one medical use of ultrasound?", "scanning an unborn baby", ["X-ray images of bones", "killing bacteria in food", "heating soup"]),
        ("Why can loud music damage hearing?", "Large vibrations can damage the tiny hair cells in the inner ear.", ["It makes the ear canal shorter.", "It stops blood flow to the brain.", "It cools the eardrum."])]


def g_hear():
    q, a, w = R.choice(HEAR)
    if not once(("he", q)):
        return None
    return item(q, a, w, "Frequency → pitch; amplitude → loudness.")


def g_wspeed():
    fr = R.choice([2, 5, 10, 20, 50, 100, 200, 250, 500])
    wl = R.choice([0.5, 1, 1.5, 2, 3, 4])
    k = R.choice(["v", "l"])
    if not once(("ws", fr, wl, k)):
        return None
    v = fr * wl
    vs = "{:g}".format(v)
    if k == "v":
        g = "%s m/s" % vs
        return item("A wave has a frequency of %d Hz and a wavelength of %s m. What is its speed? (wave speed = frequency × wavelength)" % (fr, "{:g}".format(wl)), g,
                    uniq(g, ["%s m/s" % "{:g}".format(fr + wl), "%s m/s" % "{:g}".format(round(fr / wl, 2)), "%d m/s" % fr, "%s m/s" % "{:g}".format(v * 10)]), "%d × %s = %s m/s." % (fr, "{:g}".format(wl), vs))
    g = "%s m" % "{:g}".format(wl)
    return item("A wave travels at %s m/s with a frequency of %d Hz. What is its wavelength?" % (vs, fr), g,
                uniq(g, ["%s m" % "{:g}".format(v * fr), "%s m" % "{:g}".format(v - fr) if v > fr else "%s m" % "{:g}".format(wl * 2), "%d m" % fr, "%s m" % vs]), "wavelength = speed ÷ frequency = %s ÷ %d." % (vs, fr))


B1 = bank([
    ("What do waves transfer?", "energy (and information), not matter", ["matter from one place to another", "only water", "mass"], "The medium vibrates in place."),
    ("What is the amplitude of a wave?", "the maximum distance a point moves from its rest position", ["the distance between two peaks", "the number of waves each second", "the speed of the wave"], "Bigger amplitude, more energy."),
    ("What is the wavelength of a wave?", "the distance from one peak to the next", ["the height of a peak", "the time for one wave", "the number of waves per second"], "Measured in metres."),
    ("What is the frequency of a wave?", "the number of waves passing a point each second", ["the height of the wave", "the distance between peaks", "the speed of sound"], "Measured in hertz (Hz)."),
    ("Why can sound not travel through space?", "Sound needs particles (a medium) to vibrate, and space is a vacuum.", ["Space is too cold.", "Sound is too slow.", "Space is too bright."], "Light can travel through a vacuum."),
])
B5 = bank([
    ("Which is faster: light or sound?", "light (about 300,000,000 m/s compared with about 340 m/s)", ["sound", "they are the same", "it depends on the colour"], "Lightning before thunder."),
    ("Why do you see lightning before you hear thunder?", "Light travels much faster than sound.", ["Sound starts later.", "Thunder is quieter.", "Light is louder."], "Count the seconds."),
    ("Does sound travel faster in air or in steel?", "in steel", ["in air", "the same in both", "it cannot travel in steel"], "Particles are closer together in solids."),
    ("What happens when a wave hits a surface?", "It can be reflected, absorbed or transmitted.", ["It always stops.", "It always speeds up.", "It turns into matter."], "Depends on the material."),
    ("Why are soft materials used to soundproof rooms?", "They absorb sound instead of reflecting it.", ["They reflect sound.", "They make sound faster.", "They create echoes."], "Absorption."),
])


def body():
    think = ("<p><b>Waves transfer energy without carrying matter along.</b></p>"
             "<ul><li>Transverse waves (light, water ripples) vibrate at right angles; longitudinal waves (sound) vibrate along the direction of travel.</li>"
             "<li>Amplitude → loudness; frequency (Hz) → pitch. wave speed = frequency × wavelength.</li>"
             "<li>Sound needs a medium (about 340 m/s in air); light can cross a vacuum. Echo distance = speed × time ÷ 2.</li></ul>")
    ex = [("50 Hz, 2 m wavelength. Speed?", ["50 × 2"], "100 m/s"),
          ("Echo after 2 s in air (340 m/s). Distance?", ["340 × 2 ÷ 2"], "340 m")]
    mist = ["Thinking waves carry matter along.", "Thinking sound travels through space.", "Forgetting to halve the echo time."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Describing waves", B1 + [(g_type, 7), (us_read, 3), (us_rel, 4), (g_wspeed, 1)]),
        ("Wave speed", [(g_wspeed, 14), (us_speed, 6)]),
        ("Sound", [(g_hear, 7), (us_sound, 6), (us_rel, 3), (us_read, 2), (g_wspeed, 2)]),
        ("Echoes", [(g_echo, 14), (us_what, 6)]),
        ("Light and sound", B5 + [(us_what, 6), (us_speed, 5), (us_sound, 4)]),
    ])
    make_ks3(9, "waves", 10, "Physics", "Waves",
             "Waves on water as undulations which travel through water with transverse motion; these waves can be reflected, and add or cancel – superposition; frequencies of sound waves, measured in hertz (Hz); echoes, reflection and absorption of sound; sound needs a medium to travel, the speed of sound in air, in water, in solids; sound produced by vibrations of objects, in loudspeakers, detected by their effects on microphone diaphragm and the ear drum; sound waves are longitudinal; auditory range of humans and animals; the similarities and differences between light waves and waves in matter; light waves travelling through a vacuum; speed of light.",
             "Waves",
             "Year 9 Science: Waves Worksheets (Amplitude, Frequency, Wave Speed, Echoes)",
             "Waves",
             "Free Year 9 science worksheets on waves: transverse and longitudinal waves, amplitude, wavelength and frequency, wave speed, sound, hearing range, ultrasound, echoes and the speed of light. 100 questions with answers.",
             "wave speed = frequency × wavelength",
             "Sound is longitudinal and needs a medium; light is transverse and crosses a vacuum.",
             body(),
             [("What is the difference between transverse and longitudinal waves?", "In transverse waves, such as light, the vibrations are at right angles to the direction the wave travels. In longitudinal waves, such as sound, they are along it."),
              ("How do you calculate wave speed?", "Multiply the frequency (Hz) by the wavelength (m): wave speed = frequency × wavelength, in m/s."),
              ("How do you work out distance from an echo?", "The sound travels there and back, so distance = speed × time ÷ 2.")],
             sets)


if __name__ == "__main__":
    main()
