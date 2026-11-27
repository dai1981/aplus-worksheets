# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 11: Electromagnetic Spectrum
  python tools/gen_sg_science_s3_electromagnetic_spectrum.py
Properties of electromagnetic waves (transverse, same speed of 3.0 × 10⁸ m/s in a vacuum, transfer energy, no medium needed);
the order of the spectrum by wavelength and frequency; uses of each region; harmful effects and safety; v = fλ for light.
UK and US electromagnetic-spectrum makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "radio waves are sound waves", "gamma rays travel faster than radio waves",
"microwaves are not electromagnetic", "ultraviolet has a longer wavelength than visible light".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Physics", 11
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_order = src("gen_uk_science_y11_waves_and_the_electromagnetic_spectrum", "g_order")
uk_use = src("gen_uk_science_y11_waves_and_the_electromagnetic_spectrum", "g_use")
us_em = src("gen_us_science_phys_wave_properties", "g_em")
us_cmp = src("gen_us_science_phys_electromagnetic_radiation_and_matter", "g_cmp")
us_ion = src("gen_us_science_phys_electromagnetic_radiation_and_matter", "g_ion")

SPEC = ["radio waves", "microwaves", "infrared", "visible light", "ultraviolet", "X-rays", "gamma rays"]
USE = [("radio waves", "radio and television broadcasting"), ("microwaves", "satellite communication and mobile phone signals"), ("microwaves", "cooking food in a microwave oven"),
       ("infrared", "remote controls and thermal imaging cameras"), ("infrared", "intruder alarms and ear thermometers"), ("visible light", "optical fibres and photography"),
       ("ultraviolet", "sterilising water and detecting forged banknotes"), ("ultraviolet", "sunbeds and making fluorescent markings glow"),
       ("X-rays", "imaging broken bones and airport security scanners"), ("gamma rays", "killing cancer cells (radiotherapy) and sterilising medical equipment")]
HARM = [("ultraviolet", "sunburn, skin cancer and eye damage"), ("X-rays", "damage to cells and cancer after high or repeated doses"),
        ("gamma rays", "cell damage and cancer: it is the most penetrating and ionising"), ("microwaves", "internal heating of body tissue at high power")]


def g_use():
    w, u = R.choice(USE)
    if R.random() < 0.5:
        return tq("Which electromagnetic wave is used for %s?" % u, w, R.sample([x for x in SPEC if x != w], 3), "%s: %s." % (w[0].upper() + w[1:], u))
    others = sorted({uu for ww, uu in USE if ww != w})
    return tq("Which is a use of %s?" % w, u, R.sample(others, 3), "%s: %s." % (w[0].upper() + w[1:], u))


HW = {"ultraviolet": ["radio waves", "visible light", "microwaves"], "X-rays": ["radio waves", "visible light", "infrared"],
      "gamma rays": ["radio waves", "visible light", "microwaves"], "microwaves": ["visible light", "ultraviolet", "X-rays"]}


def g_harm():
    w, h = R.choice(HARM)
    return tq("Which electromagnetic wave can cause %s?" % h, w, HW[w], "%s: %s." % (w[0].upper() + w[1:], h))


def g_order():
    i, j = sorted(R.sample(range(7), 2))
    a, b = SPEC[i], SPEC[j]
    k = R.choice(["longer wavelength", "higher frequency", "lower frequency", "shorter wavelength"])
    ans = a if k in ("longer wavelength", "lower frequency") else b
    pair = [a, b] if R.random() < 0.5 else [b, a]
    return tq("Which has the %s: %s or %s?" % (k, pair[0], pair[1]), ans, [a if ans == b else b, "They are the same.", "It depends on the source."],
              "Order of increasing frequency (decreasing wavelength): radio, microwave, infrared, visible, ultraviolet, X-ray, gamma.")


def g_gap():
    i = R.randint(1, 5)
    seq = SPEC[:]
    blank = seq[i]
    seq[i] = "____"
    return tq("Which region is missing from the spectrum in order of increasing frequency? %s" % ", ".join(seq), blank, R.sample([x for x in SPEC if x != blank], 3),
              "Radio, microwave, infrared, visible, ultraviolet, X-ray, gamma.")


def g_c():
    k = R.choice(["f", "l", "t"])
    if k == "t":
        d = R.choice([3.0e8, 6.0e8, 1.5e11, 3.84e8, 3.6e7])
        what = {3.0e8: "a radio signal sent 3.0 × 10⁸ m", 6.0e8: "a laser pulse sent 6.0 × 10⁸ m", 1.5e11: "light from the Sun (1.5 × 10¹¹ m away)",
                3.84e8: "a radio signal to the Moon (3.84 × 10⁸ m away)", 3.6e7: "a microwave signal to a satellite 3.6 × 10⁷ m above the Earth"}[d]
        return nq("How long does %s take to travel that distance? (speed of light = 3.0 × 10⁸ m/s)" % what, d / 3e8, [d * 3e8, 3e8 / d, d / 3e8 * 2], " s",
                  "t = d ÷ v = %s ÷ 3.0 × 10⁸." % nf(d))
    w, f = R.choice([("a radio wave", 1.0e8), ("a radio wave", 1.5e6), ("a microwave", 2.4e9), ("a microwave", 1.0e10), ("infrared radiation", 3.0e13), ("visible light", 6.0e14), ("ultraviolet radiation", 1.5e15)])
    l = 3e8 / f
    if k == "l":
        return nq("%s has a frequency of %s Hz. What is its wavelength? (speed = 3.0 × 10⁸ m/s)" % (w[0].upper() + w[1:], nf(f, 2)), l, [3e8 * f, f / 3e8, l * 10], " m",
                  "λ = v ÷ f = 3.0 × 10⁸ ÷ %s." % nf(f, 2), sf=2)
    return nq("%s has a wavelength of %s m. What is its frequency? (speed = 3.0 × 10⁸ m/s)" % (w[0].upper() + w[1:], nf(l, 2)), f, [3e8 * l, l / 3e8, f / 10], " Hz",
              "f = v ÷ λ = 3.0 × 10⁸ ÷ %s." % nf(l, 2), sf=2)


POOL1 = pool(R, [
    ("Which property do all electromagnetic waves share?", "They travel at the same speed in a vacuum.", ["They have the same frequency.", "They are longitudinal.", "They need a medium."], "3.0 × 10⁸ m/s."),
    ("What type of wave are all electromagnetic waves?", "transverse", ["longitudinal", "sound waves", "both transverse and longitudinal"], "They are vibrations of electric and magnetic fields."),
    ("What is the speed of electromagnetic waves in a vacuum?", "3.0 × 10⁸ m/s", ["340 m/s", "3.0 × 10⁵ m/s", "1500 m/s"], "The speed of light."),
    ("Which part of the electromagnetic spectrum can we see?", "visible light", ["infrared", "ultraviolet", "microwaves"], "From red (longest) to violet (shortest)."),
    ("Which electromagnetic wave has the longest wavelength?", "radio waves", ["gamma rays", "visible light", "X-rays"], "Radio wavelengths can be kilometres long."),
    ("Which electromagnetic wave has the highest frequency?", "gamma rays", ["radio waves", "ultraviolet", "X-rays"], "Gamma rays have the most energy."),
    ("Do electromagnetic waves need a medium to travel?", "No, they can travel through a vacuum.", ["Yes, they need air.", "Yes, they need water.", "Only radio waves need a medium."], "Light reaches us from the Sun through space."),
    ("What do electromagnetic waves transfer?", "energy", ["matter", "air particles", "electric charge"], "Like all waves."),
    ("Which colour of visible light has the longest wavelength?", "red", ["violet", "green", "blue"], "Red is next to infrared."),
    ("Which radiation is just beyond violet light in the spectrum?", "ultraviolet", ["infrared", "X-rays", "microwaves"], "'Ultra' means beyond."),
])
POOL5 = pool(R, [
    ("Why do radiographers stand behind a lead screen when taking X-rays?", "to reduce their exposure to X-rays, which can damage cells", ["to keep warm", "to make the image clearer", "because X-rays need lead to travel"], "Lead absorbs X-rays."),
    ("Why is sunscreen recommended outdoors in Singapore?", "It absorbs ultraviolet radiation, which can cause sunburn and skin cancer.", ["It blocks infrared to stop sweating.", "It reflects radio waves.", "It cools the skin by evaporation."], "The UV index in Singapore is often very high."),
    ("Why do microwave ovens have a metal mesh in the door?", "to stop microwaves escaping while letting you see inside", ["to let microwaves out", "to cool the food", "to make the door stronger only"], "The holes are smaller than the wavelength."),
    ("A TV remote control does not work when a book is in the way. Which wave does it use?", "infrared", ["radio waves", "ultraviolet", "X-rays"], "Infrared does not pass through a book."),
    ("Why are gamma rays used to sterilise medical equipment?", "They kill bacteria and can pass through the packaging.", ["They clean off dirt.", "They heat the equipment to boiling.", "They are not harmful."], "Very penetrating radiation."),
    ("A thermal imaging camera shows people at night. Which radiation does it detect?", "infrared emitted by warm bodies", ["visible light reflected by bodies", "ultraviolet from the Moon", "microwaves from phones"], "All warm objects emit infrared."),
    ("Which wave is used to carry signals through optical fibres?", "visible light or infrared", ["radio waves", "gamma rays", "sound waves"], "Total internal reflection keeps it inside."),
    ("A radio station broadcasts at 95.0 MHz. What does 'MHz' tell you?", "The frequency is 95.0 million waves per second.", ["The wavelength is 95.0 m.", "The speed is 95.0 m/s.", "The power is 95.0 MW."], "Mega = 10⁶."),
    ("Why are X-rays useful for imaging bones?", "X-rays pass through soft tissue but are absorbed by dense bone.", ["Bones reflect radio waves.", "X-rays make bones glow.", "Bones emit X-rays."], "Bones show as white on the image."),
    ("Why are mobile phone signals carried by microwaves rather than visible light?", "Microwaves pass through walls and clouds that block light.", ["Microwaves travel faster than light.", "Light is too long a wavelength.", "Microwaves are sound waves."], "All EM waves travel at the same speed."),
])


def main():
    sets = U.sets([
        ("Properties of electromagnetic waves", [POOL1, (g_gap, 5), (g_order, 5)]),
        ("Order of the spectrum", [(g_order, 8), (uk_order, 5), (us_em, 4), (g_gap, 3)]),
        ("Uses of electromagnetic waves", [(g_use, 12), (uk_use, 5), (POOL5, 3)]),
        ("Dangers and v = fλ", [(g_harm, 4), (us_ion, 4), (us_cmp, 3), (g_c, 9)]),
        ("Exam-style questions", [(POOL5, 9), (g_c, 4), (g_use, 4), POOL1]),
    ])
    make_ol(LV, SUBJ, "electromagnetic-spectrum", SORT, "Electromagnetic Spectrum",
            "State that all electromagnetic waves are transverse, travel with the same high speed of 3.0 × 10⁸ m/s in a vacuum and transfer energy; describe the main "
            "components of the electromagnetic spectrum in order of wavelength and frequency; describe typical uses of each region (radio and television, "
            "satellite and mobile communication, remote controls and thermal imaging, optical fibres, sterilisation, X-ray imaging and radiotherapy); describe the "
            "harmful effects of over-exposure and how to reduce them (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Electromagnetic Spectrum", "EM spectrum",
            "Free Secondary 3 O-Level Physics worksheets on the electromagnetic spectrum: properties of EM waves, the order of the spectrum, uses and dangers of radio, "
            "microwaves, infrared, light, UV, X-rays and gamma rays. 100 questions with answers.",
            "All EM waves travel at 3.0 × 10⁸ m/s in a vacuum.", "Radio, micro, IR, visible, UV, X-ray, gamma: frequency rises.",
            "<p><b>Electromagnetic waves are transverse waves that travel at 3.0 × 10⁸ m/s in a vacuum.</b></p><ul>"
            "<li>In order of increasing frequency (decreasing wavelength): radio waves, microwaves, infrared, visible light, ultraviolet, X-rays, gamma rays.</li>"
            "<li>Higher frequency means more energy: UV, X-rays and gamma rays can damage cells and cause cancer.</li>"
            "<li>v = fλ also works for light, with v = 3.0 × 10⁸ m/s.</li></ul>",
            [("Which has a shorter wavelength: infrared or ultraviolet?", ["UV is further along the order"], "ultraviolet"),
             ("A microwave has f = 1.0 × 10¹⁰ Hz. Wavelength?", ["λ = 3.0 × 10⁸ ÷ 1.0 × 10¹⁰"], "0.030 m")],
            ["Thinking higher-frequency waves travel faster. All EM waves have the same speed in a vacuum.", "Calling radio waves sound waves. They are electromagnetic.",
             "Getting the order of ultraviolet and infrared the wrong way round.", "Thinking all EM radiation is dangerous. Radio waves and visible light are low-energy."],
            [("What is the order of the electromagnetic spectrum?", "Radio waves, microwaves, infrared, visible light, ultraviolet, X-rays and gamma rays, in order of increasing frequency and decreasing wavelength."),
             ("What do all electromagnetic waves have in common?", "They are transverse, transfer energy, need no medium and travel at 3.0 × 10⁸ m/s in a vacuum."),
             ("Which electromagnetic waves are harmful?", "Ultraviolet, X-rays and gamma rays carry enough energy to damage cells; high-power microwaves and infrared can heat and burn tissue.")],
            sets)


if __name__ == "__main__":
    main()
