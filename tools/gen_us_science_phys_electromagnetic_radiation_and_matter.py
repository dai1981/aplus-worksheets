# -*- coding: utf-8 -*-
"""
US High School Physics: Electromagnetic Radiation and Matter (HS-PS4-4)
  python tools/gen_us_science_phys_electromagnetic_radiation_and_matter.py
Evaluate the validity and reliability of claims in published materials of the effects that different frequencies of
electromagnetic radiation have when absorbed by matter.
Ionizing vs non-ionizing radiation, what radio, microwave, infrared, visible, ultraviolet, X-ray and gamma radiation do
when absorbed, intensity and distance (inverse square), and how to judge claims (sources, controls, sample size,
correlation vs cause).
Wrong answers come from real mistakes: "all radiation causes cancer", "microwaves make food radioactive",
"higher intensity means higher photon energy", "one person's story proves a claim".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, uniq, safe

U = Unit(90315)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


EFF = [("radio waves", "mostly pass through the body with very little energy absorbed"), ("microwaves", "make water molecules move faster, which heats food"),
       ("infrared radiation", "warms the skin and objects it hits"), ("visible light", "is absorbed by the eye's retina and by chlorophyll in plants"),
       ("ultraviolet (UV) radiation", "can damage DNA in skin cells and cause sunburn"), ("X-rays", "pass through soft tissue but are absorbed by bone"),
       ("gamma rays", "can ionize atoms deep in the body and kill cells")]
NONION = ["radio waves", "microwaves", "infrared radiation", "visible light"]
ION = ["X-rays", "gamma rays"]


@safe
def g_eff():
    r, e = R.choice(EFF)
    k = R.random() < 0.5
    if not once(("ef", r, k)):
        return None
    if k:
        return item("What do %s mainly do when absorbed by matter?" % r, e, R.sample([x[1] for x in EFF if x[1] != e], 3), "Higher frequency → more energy per photon → more damage.")
    return item("Which type of radiation %s?" % e, r, R.sample([x[0] for x in EFF if x[0] != r], 3), "Match the effect to the frequency.")


@safe
def g_ion():
    k = R.choice(["which", "not", "yn"])
    if k == "yn":
        r = R.choice([x[0] for x in EFF])
        if not once(("yn", r)):
            return None
        ion = r in ION or r.startswith("ultra")
        g = "Yes, its photons can knock electrons off atoms." if ion else "No, its photons have too little energy to ionize atoms."
        return item("Is %s ionizing radiation?" % r, g, ["No, its photons have too little energy to ionize atoms." if ion else "Yes, its photons can knock electrons off atoms.",
                                                         "Only when it is very bright.", "Only inside a microwave oven."], "Ionizing depends on photon energy (frequency), not brightness.")
    if k == "which":
        a = R.choice(ION)
        w = R.sample(NONION, 3)
        if not once(("io", a, tuple(sorted(w)))):
            return None
        return item("Which of these can ionize atoms (knock electrons off) in living cells?", a, w, "Only high-frequency radiation (X-rays, gamma rays, and some UV) carries enough energy per photon.")
    a = R.choice(NONION)
    w = R.sample(ION + ["ultraviolet (UV) radiation"], 3)
    if not once(("ni", a, tuple(sorted(w)))):
        return None
    return item("Which of these is non-ionizing radiation?", a, w, "Radio, microwave, infrared and visible light photons have too little energy to ionize atoms.")


@safe
def g_int():
    who = P.next()[0]
    I = R.choice([40, 80, 100, 160, 200, 360, 400, 900, 1000])
    a = R.choice([1, 2, 3])
    b = R.choice([2, 3, 4, 5, 6, 10])
    if b <= a or not once(("in", I, a, b)):
        return None
    I2 = I * a * a / (b * b)
    if I2 != round(I2, 1):
        return None
    g = "%s W/m²" % num(I2, 1)
    return item("A heat lamp gives an intensity of %s W/m² at %d m in %s's test. What is the intensity at %d m? (intensity ∝ 1 ÷ distance²)" % (num(I), a, who, b), g,
                uniq(g, ["%s W/m²" % num(I * a / b, 1), "%s W/m²" % num(I), "%s W/m²" % num(I * b * b / (a * a), 1), "%s W/m²" % num(I / b, 1)]),
                "%s × (%d ÷ %d)² = %s W/m²." % (num(I), a, b, num(I2, 1)))


CLAIMS = [("A website selling crystals says they 'block harmful phone radiation.' It cites no studies.", "It is not reliable: there is no evidence, and the seller benefits."),
          ("A peer-reviewed study of 50,000 people found no link between phone use and brain cancer.", "It is fairly reliable: large sample and reviewed by other scientists."),
          ("A blogger says he felt dizzy near a Wi-Fi router, so Wi-Fi causes dizziness.", "It is weak evidence: one person's story with no control or measurement."),
          ("An ad claims a sunscreen 'blocks 100% of UV forever'.", "It is not believable: no sunscreen blocks all UV, and it wears off."),
          ("A study found people who own more microwaves have more headaches.", "It shows a correlation, not that microwaves cause headaches."),
          ("Health agencies set limits on X-ray doses based on many studies.", "It is reliable: based on lots of data from many sources."),
          ("A video says microwave ovens make food radioactive.", "It is false: microwaves only heat water molecules and do not make food radioactive."),
          ("A study that tested a UV-blocking fabric had no control fabric.", "It is weak: without a control, the effect cannot be compared.")]


@safe
def g_claim():
    s, a = R.choice(CLAIMS)
    if not once(("cl", s)):
        return None
    return item("%s How should you judge this claim?" % s, a, R.sample([x[1] for x in CLAIMS if x[1] != a], 3), "Check the source, data, controls and whether it shows cause.")


@safe
def g_cmp():
    i, j = sorted(R.sample(range(7), 2))
    if not once(("cp", i, j)):
        return None
    a, b = EFF[i][0], EFF[j][0]
    return item("Per photon, which is more likely to damage living cells: %s or %s?" % (a, b), b, [a, "They are equally harmful.", "Neither can affect cells."],
                "Higher frequency photons carry more energy.")


B1 = bank([
    ("What makes some electromagnetic radiation 'ionizing'?", "Its photons have enough energy to knock electrons off atoms.", ["It is very bright.", "It is very loud.", "It travels slowly."], "X-rays, gamma, some UV."),
    ("Why do dentists put a lead apron on you for X-rays?", "Lead absorbs X-rays and protects other tissues.", ["Lead makes X-rays brighter.", "To keep you warm.", "Lead reflects microwaves."], "Shielding."),
    ("Does a microwave oven make food radioactive?", "No. It only makes water molecules move faster, heating the food.", ["Yes, always.", "Only frozen food.", "Only metal containers."], "Non-ionizing."),
    ("Why does sunscreen protect skin?", "It absorbs or reflects UV radiation before it reaches skin cells.", ["It blocks all visible light.", "It cools the skin.", "It adds vitamins."], "UV protection."),
    ("Why does moving farther from a radiation source reduce exposure?", "Intensity drops with the square of the distance.", ["Radiation slows down.", "Photons lose frequency.", "Air makes it ionizing."], "Inverse square."),
    ("Is brighter (more intense) light made of higher-energy photons?", "No. It has more photons; photon energy depends on frequency.", ["Yes, always.", "Only for red light.", "Only at night."], "Intensity vs frequency."),
    ("Which radiation is used to treat some cancers?", "gamma rays (or high-energy X-rays)", ["radio waves", "infrared", "visible light"], "Targeted cell damage."),
    ("What does a reliable scientific claim usually have?", "data from careful studies that others have checked", ["a celebrity endorsement", "one personal story", "a product to sell"], "Peer review."),
])
B5 = bank([
    ("A news article says cell towers cause illness but quotes only one unnamed source. What should a reader do?", "look for peer-reviewed studies and health-agency reports", ["believe it right away", "share it widely", "ignore all science"], "Evaluate sources."),
    ("Why are tanning beds considered risky?", "They give strong doses of UV, which can damage DNA.", ["They use X-rays.", "They are too cold.", "They use radio waves only."], "UV exposure."),
    ("Which study design best tests whether a fabric blocks UV?", "compare UV meters under the fabric and under a plain control fabric, many times", ["ask people how sunburned they feel", "test it once with no control", "look at the fabric's color"], "Controlled, repeated."),
    ("Airport scanners use very low-energy radiation. Why is this a reasonable choice?", "It can make images while giving a tiny dose with little risk.", ["It gives a large dose.", "It makes passengers radioactive.", "It uses gamma rays."], "Risk vs benefit."),
    ("A company says its phone case 'reduces radiation by 99%' but the phone then boosts its signal. What is a flaw?", "Blocking the signal can make the phone transmit harder, so exposure may not drop.", ["There is no flaw.", "Phones do not transmit.", "Cases add radiation."], "Think about the whole system."),
])


def body():
    think = ("<p><b>What radiation does depends on its frequency (photon energy).</b></p>"
             "<ul><li>Low frequency (radio, microwave, infrared, visible): non-ionizing; mostly heating or no effect.</li>"
             "<li>High frequency (UV, X-rays, gamma): can ionize atoms and damage DNA.</li>"
             "<li>Intensity falls as 1 ÷ distance². Judge claims by their source, data, controls and whether they show cause.</li></ul>")
    ex = [("100 W/m² at 1 m. At 2 m?", ["100 × (1 ÷ 2)²"], "25 W/m²"),
          ("Microwaves or X-rays: more harmful per photon?", ["Higher frequency"], "X-rays")]
    mist = ["Thinking all radiation causes cancer.", "Thinking microwave ovens make food radioactive.", "Thinking brighter light has higher-energy photons."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Ionizing and non-ionizing", B1 + [(g_ion, 6), (g_cmp, 6)]),
        ("Effects of radiation", [(g_eff, 12), (g_cmp, 8)]),
        ("Intensity and distance", [(g_int, 18), (g_ion, 2)]),
        ("Judging claims", [(g_claim, 7), (g_cmp, 4), (g_int, 9)]),
        ("Evaluating published claims", B5 + [(g_ion, 6), (g_int, 7), (g_eff, 2)]),
    ])
    make("physics", "electromagnetic-radiation-and-matter", 15, "HS-PS4-4",
         "Evaluate the validity and reliability of claims in published materials of the effects that different frequencies of electromagnetic radiation have when absorbed by matter.",
         "Electromagnetic Radiation and Matter",
         "EM Radiation Worksheets: Ionizing Radiation, UV, X-Rays and Health Claims (Physics)",
         "EM Radiation and Matter",
         "Free high school physics worksheets on electromagnetic radiation and matter (NGSS HS-PS4-4): ionizing and non-ionizing radiation, effects on the body, intensity and evaluating health claims. 100 questions with answers.",
         "Higher frequency, more damage.",
         "UV, X-rays and gamma rays can ionize atoms; radio and microwaves mainly heat or pass through.",
         body(),
         [("What is the difference between ionizing and non-ionizing radiation?", "Ionizing radiation (X-rays, gamma rays, some UV) has enough photon energy to knock electrons off atoms. Non-ionizing radiation (radio, microwave, infrared, visible) does not."),
          ("Are cell phones and microwaves dangerous?", "They use non-ionizing radiation. Microwaves heat food by making water molecules move faster; they do not make food radioactive."),
          ("How do you judge a claim about radiation?", "Check who made it, whether there is data from controlled studies, whether others reviewed it, and whether it shows cause or only a correlation.")],
         sets)


if __name__ == "__main__":
    main()
