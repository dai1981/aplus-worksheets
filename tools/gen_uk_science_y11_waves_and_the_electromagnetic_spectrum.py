# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Physics): Waves and the Electromagnetic Spectrum
  python tools/gen_uk_science_y11_waves_and_the_electromagnetic_spectrum.py
Transverse and longitudinal waves, amplitude, wavelength, frequency and period, the wave equation v = fλ and T = 1/f,
the electromagnetic spectrum in order, properties and uses of each part, the hazards of ultraviolet, X-rays and gamma
rays, and (higher tier) refraction. Reuses the US Physics wave and electromagnetic radiation questions in British
English.
Wrong answers come from real mistakes: "sound is transverse", "radio waves are faster than light", "X-rays have a
longer wavelength than microwaves", "the wave moves the water along with it".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62111)
WP, EM = "phys_wave_properties", "phys_electromagnetic_radiation_and_matter"
us_vfl, us_period, us_em, us_medium = us(WP, "g_vfl"), us(WP, "g_period"), us(WP, "g_em"), us(WP, "g_medium")
PH = (("Per photon, which", "Which"), ("its photons can", "it can"), ("its photons have", "it has"), ("photon energy (frequency)", "frequency"), (" per photon", ""), ("light photons have", "light have"), ("frequency photons", "frequency waves"))
_cmp, us_ion = us(EM, "g_cmp", rep=PH), us(EM, "g_ion", rep=PH)


def us_cmp():
    it = _cmp()
    if it is None or not any(w in it["c"][it["a"]] for w in ("ultraviolet", "X-rays", "gamma")):
        return None
    return it

TL = [("light", "transverse"), ("ripples on water", "transverse"), ("radio waves", "transverse"), ("S-waves in an earthquake", "transverse"),
      ("waves on a guitar string", "transverse"), ("sound", "longitudinal"), ("P-waves in an earthquake", "longitudinal"), ("ultrasound", "longitudinal")]


def g_tl():
    w, a = R.choice(TL)
    if not once(("tl", w)):
        return None
    return item("Is %s a transverse or a longitudinal wave?" % w if w in ("light", "sound", "ultrasound") else "Are %s transverse or longitudinal waves?" % w, a,
                [x for x in ["transverse", "longitudinal", "neither", "both"] if x != a],
                "Transverse: vibrations at right angles to the direction of energy transfer. Longitudinal: vibrations parallel to it.")


PARTS = [("amplitude", "the maximum displacement of a point on the wave from its rest position"), ("wavelength", "the distance from a point on one wave to the same point on the next wave"),
         ("frequency", "the number of waves passing a point each second"), ("period", "the time for one complete wave to pass a point"),
         ("wave speed", "the speed at which energy is transferred through the medium")]


def g_parts():
    p, d = R.choice(PARTS)
    k = R.choice(["name", "def"])
    if not once(("pa", p, k)):
        return None
    if k == "name":
        return item("What is %s?" % d, "the " + p, ["the " + x[0] for x in PARTS if x[0] != p][:3], "Learn the wave words.")
    return item("What is the %s of a wave?" % p, d, R.sample([x[1] for x in PARTS if x[0] != p], 3), "Learn the wave words.")


SPEC = ["radio waves", "microwaves", "infrared", "visible light", "ultraviolet", "X-rays", "gamma rays"]


def g_order():
    k = R.choice(["long", "high", "between"])
    if k == "between":
        i = R.randrange(1, 6)
        if not once(("ob", i)):
            return None
        return item("In the electromagnetic spectrum, which comes between %s and %s?" % (SPEC[i - 1], SPEC[i + 1]), SPEC[i],
                    R.sample([x for j, x in enumerate(SPEC) if abs(j - i) > 1], 3), "Radio, microwave, infrared, visible, ultraviolet, X-ray, gamma.")
    i, j = sorted(R.sample(range(7), 2))
    if not once(("oo", i, j, k)):
        return None
    if k == "long":
        return item("Which has the longer wavelength: %s or %s?" % ((SPEC[i], SPEC[j]) if R.random() < 0.5 else (SPEC[j], SPEC[i])), SPEC[i],
                    [SPEC[j], "They have the same wavelength.", "It depends on their speed."], "Wavelength decreases from radio waves to gamma rays.")
    return item("Which has the higher frequency: %s or %s?" % ((SPEC[i], SPEC[j]) if R.random() < 0.5 else (SPEC[j], SPEC[i])), SPEC[j],
                [SPEC[i], "They have the same frequency.", "It depends on their speed."], "Frequency increases from radio waves to gamma rays.")


USES = [("radio waves", "television and radio broadcasting"), ("microwaves", "satellite communications and cooking food"),
        ("infrared", "electrical heaters and thermal imaging cameras"), ("visible light", "fibre optic communications"),
        ("ultraviolet", "energy-efficient lamps and sun tanning"), ("X-rays", "medical imaging of bones"), ("gamma rays", "sterilising medical equipment and treating cancer")]


def g_use():
    w, u = R.choice(USES)
    k = R.choice(["use", "wave"])
    if not once(("us", w, k)):
        return None
    if k == "use":
        return item("What is a use of %s?" % w, u, R.sample([x[1] for x in USES if x[0] != w], 3), "Each part of the spectrum has uses that match its properties.")
    return item("Which electromagnetic waves are used for %s?" % u, w, R.sample([x[0] for x in USES if x[0] != w], 3), "Each part of the spectrum has uses that match its properties.")


B1 = bank([
    ("What do waves transfer?", "energy, not matter", ["matter, not energy", "both matter and energy", "only water"], "A cork on a ripple bobs up and down but does not move along."),
    ("What is the unit of frequency?", "hertz (Hz)", ["metres (m)", "seconds (s)", "newtons (N)"], "1 Hz = 1 wave per second."),
    ("How could you measure the speed of sound in air?", "Measure the time for an echo from a wall and the distance travelled.", ["Weigh the air.", "Use a thermometer.", "Count the waves with a ruler."], "speed = distance ÷ time."),
])
B4 = bank([
    ("What do all electromagnetic waves have in common?", "They are transverse and travel at the same speed in a vacuum.", ["They are longitudinal.", "They need a medium.", "They have the same frequency."], "3 × 10⁸ m/s."),
    ("Why are radio waves useful for communication?", "They can travel long distances and are not very harmful.", ["They are ionising.", "They cannot be detected.", "They travel faster than light."], "They can be produced by oscillations in electrical circuits."),
    ("Why are X-rays used to image bones?", "They pass through soft tissue but are absorbed by bone.", ["They are absorbed by skin.", "They bend around bones.", "They are visible."], "Ionising, so exposure is limited."),
])
B5 = bank([
    ("What harm can ultraviolet do?", "It can age the skin and increase the risk of skin cancer.", ["It cooks food.", "It makes bones stronger.", "It has no effects."], "Use sun cream."),
    ("Why are X-rays and gamma rays dangerous?", "They are ionising and can cause mutations and cancer.", ["They are too slow.", "They are visible.", "They only heat skin."], "Radiographers stand behind a screen."),
    ("What is refraction?", "a change of direction when a wave changes speed as it crosses a boundary", ["the reflection of a wave", "a wave getting louder", "a wave stopping"], "Higher tier: the wave changes speed."),
    ("Light enters glass from air. What happens to its speed?", "It slows down.", ["It speeds up.", "It stays the same.", "It stops."], "So it bends towards the normal."),
    ("What is the radiation dose measured in?", "sieverts (Sv)", ["hertz (Hz)", "joules (J)", "watts (W)"], "Often in millisieverts (mSv)."),
])

if __name__ == "__main__":
  build(U, 11, "waves-and-the-electromagnetic-spectrum", 11, "Physics", "Waves",
      "Transverse and longitudinal waves; properties of waves (amplitude, wavelength, frequency, period) and the wave equation; measuring wave speed; the electromagnetic spectrum; properties and uses of electromagnetic waves; hazards of ultraviolet, X-rays and gamma rays; (higher tier) refraction.",
      "Waves and the Electromagnetic Spectrum", "Waves and EM Spectrum",
      "Free Year 11 GCSE Combined Science worksheets on waves: transverse and longitudinal waves, v = fλ, period, the electromagnetic spectrum, uses and hazards of EM waves and refraction. 100 questions with answers.",
      "Wave speed = frequency × wavelength (v = fλ).",
      "Radio waves have the longest wavelength; gamma rays the shortest.",
      "<p><b>Waves transfer energy without moving matter along.</b></p><ul><li>Transverse waves vibrate at right angles to the direction of travel; longitudinal waves (sound) vibrate along it.</li>"
      "<li>v = fλ and T = 1 ÷ f.</li>"
      "<li>Electromagnetic spectrum: radio, microwave, infrared, visible, ultraviolet, X-ray, gamma. All travel at 3 × 10⁸ m/s in a vacuum.</li></ul>",
      [("f = 50 Hz, λ = 2 m. Speed?", ["v = fλ = 50 × 2"], "100 m/s"), ("Which is longer: microwaves or X-rays?", ["Radio end is longer"], "microwaves")],
      ["Thinking sound is transverse.", "Thinking radio waves are faster than light in a vacuum.", "Thinking the water moves along with the wave."],
      [("What is the wave equation?", "Wave speed = frequency × wavelength (v = fλ). Speed in m/s, frequency in Hz and wavelength in m."),
       ("What is the order of the electromagnetic spectrum?", "Radio waves, microwaves, infrared, visible light, ultraviolet, X-rays, gamma rays. Wavelength decreases and frequency increases along this list."),
       ("Which electromagnetic waves are harmful?", "Ultraviolet can damage skin. X-rays and gamma rays are ionising and can cause mutations and cancer.")],
      [("Wave basics", B1 + [(g_tl, 6), (g_parts, 7), (us_period, 4)]),
       ("Wave speed", [(us_vfl, 11), (us_period, 4), (us_medium, 5)]),
       ("The electromagnetic spectrum", [(g_order, 14), (us_em, 6)]),
       ("Uses of EM waves", B4 + [(g_use, 11), (us_cmp, 4), (us_em, 2)]),
       ("Hazards and refraction", B5 + [(us_ion, 5), (g_order, 6), (us_cmp, 4)])])
