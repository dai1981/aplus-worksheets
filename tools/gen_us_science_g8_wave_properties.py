# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Wave Properties (MS-PS4-1)
  python tools/gen_us_science_g8_wave_properties.py
Use mathematical representations to describe a simple model for waves that includes how the amplitude of a wave is
related to the energy in a wave. Amplitude, wavelength, frequency (Hz), period, wave speed = frequency × wavelength,
larger amplitude → more energy (the energy grows with the square of the amplitude).
Wrong answers come from real mistakes: "longer wavelength means more energy for the same wave", "amplitude is the
crest-to-trough height", "wave speed = frequency + wavelength", "waves carry matter along".
"""
from sci_common import Unit, item, bank, lesson, make, fig, table, People
from gen_us_science_g4_waves import wave

U = Unit(80108)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def g_speed():
    who = P.next()[0]
    f = R.choice([1, 2, 3, 4, 5, 10, 20, 50, 100, 200])
    lam = R.choice([0.25, 0.5, 1, 1.5, 2, 3, 4, 5])
    v = f * lam
    if v != int(v):
        return None
    k = R.choice(["v", "f", "lam"])
    if not once(("s", f, lam, k)):
        return None
    ctx = R.choice(["on a rope", "on a spring toy", "on a pond", "in a wave tank", "on a guitar string"])
    if (ctx in ("on a pond", "in a wave tank") and v > 5) or (ctx in ("on a rope", "on a spring toy") and v > 20) or (ctx == "on a guitar string" and v < 50):
        return None
    L = "%g m" % lam
    if k == "v":
        return item("%s measures a wave %s with a frequency of %d Hz and a wavelength of %s. What is the wave speed? (speed = frequency × wavelength)" % (who, ctx, f, L), "%g m/s" % v,
                    ["%g m/s" % (f + lam), "%g m/s" % round(f / lam, 2), "%g m/s" % (v * 2)], "%d × %s = %g m/s." % (f, L, v))
    if k == "f":
        return item("A wave %s travels at %g m/s with a wavelength of %s. What frequency did %s calculate? (frequency = speed ÷ wavelength)" % (ctx, v, L, who), "%d Hz" % f,
                    ["%g Hz" % (v * lam), "%g Hz" % (v + lam), "%g Hz" % (v - lam) if v != lam and v - lam != f else "%d Hz" % (f * 2)], "%g ÷ %s = %d Hz." % (v, L, f))
    return item("A wave %s travels at %g m/s with a frequency of %d Hz. What wavelength did %s calculate? (wavelength = speed ÷ frequency)" % (ctx, v, f, who), L,
                ["%g m" % (v * f), "%g m" % (v + f), "%g m" % (lam * 2)], "%g ÷ %d = %s." % (v, f, L))


def g_amp():
    who = P.next()[0]
    a1 = R.choice([1, 2, 3])
    k = R.choice([2, 3])
    a2 = a1 * k
    if not once(("a", a1, k)):
        return None
    q = R.choice(["more", "times"])
    if q == "more":
        return item("%s makes two waves on a rope with the same wavelength. Wave A has an amplitude of %d cm and wave B has an amplitude of %d cm. Which carries more energy?" % (who, a1, a2),
                    "Wave B, because it has a larger amplitude.", ["Wave A, because it has a smaller amplitude.", "They carry the same energy.", "You cannot tell without the color."],
                    "Larger amplitude means more energy.")
    return item("%s changes the amplitude of a wave. If the amplitude becomes %d times as large, the energy becomes about how many times as large? (energy grows with amplitude squared)" % (who, k),
                "%d times" % (k * k), ["%d times" % k, "%d times" % (k * 2 + 1) if k * 2 + 1 != k * k else "%d times" % (k + 10), "the same"], "%d² = %d." % (k, k * k))


def g_read():
    who = P.next()[0]
    amp = R.choice([2, 3, 4])
    wl = R.choice([10, 12, 16])
    H = 2 * amp * 10 + 60
    svg = wave(amp, wl, H=H, marks=["rest", "amp"], label="a wave with its amplitude marked")
    k = R.choice(["amp", "crest"])
    n = R.choice([2, 3, 4])
    if not once(("r2", amp, wl, k, n if k == "crest" else 0)):
        return None
    if k == "amp":
        return item(fig(svg) + "%s measures the wave on a rope. From the top of a crest to the bottom of a trough is %d cm. What is the amplitude?" % (who, amp * 2), "%d cm" % amp,
                    ["%d cm" % (amp * 2), "%d cm" % (amp * 4), "%d cm" % wl], "Amplitude is half the crest-to-trough height: %d ÷ 2 = %d cm." % (amp * 2, amp))
    return item(fig(svg) + "%s counts %d full waves along %d cm of a rope. What is the wavelength?" % (who, n, wl * n), "%d cm" % wl,
                ["%d cm" % (wl * n), "%d cm" % (wl * n + n), "%g cm" % (wl / 2)], "%d cm ÷ %d waves = %d cm." % (wl * n, n, wl))


def g_rel():
    who = P.next()[0]
    cases = [("The frequency of a wave increases while the speed stays the same.", "The wavelength gets shorter.", ["The wavelength gets longer.", "The wavelength stays the same.", "The amplitude doubles."]),
             ("The frequency of a wave decreases while the speed stays the same.", "The wavelength gets longer.", ["The wavelength gets shorter.", "The speed doubles.", "The wave stops."]),
             ("A wave's period is 0.5 s.", "Its frequency is 2 Hz.", ["Its frequency is 0.5 Hz.", "Its frequency is 5 Hz.", "Its wavelength is 2 m."]),
             ("A wave's period is 0.25 s.", "Its frequency is 4 Hz.", ["Its frequency is 0.25 Hz.", "Its frequency is 25 Hz.", "Its amplitude is 4 cm."]),
             ("A wave has a frequency of 10 Hz.", "Ten waves pass a point each second.", ["One wave passes every 10 seconds.", "The wave is 10 m long.", "The wave moves 10 cm."]),
             ("A wave on a rope gets a bigger shake from the hand.", "The amplitude and energy increase.", ["The wavelength must double.", "The wave slows down.", "The wave carries the rope away."]),
             ("A buoy bobs as ocean waves pass.", "The buoy moves up and down but is not carried along with the wave.", ["The buoy moves with the wave to shore.", "The buoy has no energy.", "The water flows to the beach."]),
             ("Two waves travel at the same speed; wave A has twice the wavelength of wave B.", "Wave A has half the frequency of wave B.", ["Wave A has twice the frequency.", "They have the same frequency.", "Wave A has no frequency."])]
    s, a, w = R.choice(cases)
    if not once(("rel", s)):
        return None
    return item("%s's model: “%s” What follows?" % (who, s), a, w, "speed = frequency × wavelength, frequency = 1 ÷ period.")


B1 = bank([
    ("What does a wave carry from place to place?", "energy", ["matter", "air only", "water only"], "Waves transfer energy, not matter."),
    ("What is amplitude?", "the height of a wave from the rest line to a crest", ["the distance between crests", "the number of waves per second", "the speed of the wave"], "Not crest to trough."),
    ("What is wavelength?", "the distance from one crest to the next crest", ["the height of a crest", "the time for one wave", "the speed of the wave"], "Or trough to trough."),
    ("What is frequency?", "the number of waves that pass a point each second", ["the height of a wave", "the length of a wave", "the energy of a wave"], "Measured in hertz (Hz)."),
    ("How is the amplitude of a wave related to its energy?", "A larger amplitude carries more energy.", ["A larger amplitude carries less energy.", "Amplitude has no effect.", "Only wavelength matters."], "Energy grows with amplitude squared."),
    ("What is the equation for wave speed?", "speed = frequency × wavelength", ["speed = frequency + wavelength", "speed = amplitude × frequency", "speed = wavelength ÷ amplitude"], "v = f × λ."),
    ("What unit is used for frequency?", "hertz (Hz)", ["meter (m)", "joule (J)", "newton (N)"], "1 Hz = 1 wave per second."),
    ("What is the period of a wave?", "the time for one full wave to pass a point", ["the height of the wave", "the number of crests", "the speed of the wave"], "Period = 1 ÷ frequency."),
])
B5 = bank([
    ("Ava sends waves down a slinky with a small shake and a big shake. Which wave can move a cup at the far end more?", "the big-shake wave", ["the small-shake wave", "both the same", "neither"], "More amplitude, more energy."),
    ("Leo's wave tank makes 3 waves per second with a wavelength of 0.2 m. What is the wave speed?", "0.6 m/s", ["3.2 m/s", "15 m/s", "0.06 m/s"], "3 × 0.2 = 0.6 m/s."),
    ("Mia doubles the frequency of a rope wave. The speed stays the same. What happens to the wavelength?", "It is cut in half.", ["It doubles.", "It stays the same.", "It becomes zero."], "λ = v ÷ f."),
    ("Why do bigger earthquake waves cause more damage?", "They have larger amplitudes and carry more energy.", ["They have shorter names.", "They move slower.", "They carry rocks with them."], "Amplitude relates to energy."),
    ("A graph shows wave energy rising faster and faster as amplitude increases. What relationship fits?", "Energy depends on amplitude squared.", ["Energy equals amplitude.", "Energy does not depend on amplitude.", "Energy falls as amplitude rises."],
     "Doubling amplitude makes energy 4 times."),
])


def body():
    svg = wave(3, 14, H=120, marks=["rest", "amp", "wl"], label="a wave with amplitude and wavelength marked")
    think = ("<p>A <b>wave</b> carries <b>energy</b> from place to place without carrying matter along.</p>"
             "<div class='qfig'>" + svg + "</div>"
             "<ul><li><b>Amplitude</b>: rest line to crest. A larger amplitude carries <b>more energy</b> (energy grows with amplitude squared).</li>"
             "<li><b>Wavelength</b> (λ): crest to crest. <b>Frequency</b> (f): waves per second, in Hz. <b>Period</b> = 1 ÷ frequency.</li>"
             "<li><b>Wave speed = frequency × wavelength</b>. At the same speed, higher frequency means shorter wavelength.</li></ul>")
    ex = [("f = 5 Hz, λ = 2 m. Speed?", ["5 × 2"], "10 m/s"),
          ("The amplitude doubles. Energy?", ["2² = 4"], "4 times as much")]
    mist = ["Measuring amplitude from crest to trough. That is twice the amplitude.",
            "Adding frequency and wavelength instead of multiplying.",
            "Thinking waves carry water or air along with them."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a wave", B1 + [(g_read, 12)]),
        ("Reading wave models", [(g_read, 8), (g_rel, 6), (g_amp, 6)]),
        ("Wave speed", [(g_speed, 16), (g_rel, 4)]),
        ("Amplitude and energy", [(g_amp, 10), (g_speed, 10)]),
        ("Using wave math", B5 + [g_speed, g_amp, g_rel, g_read]),
    ])
    make("grade-8", "wave-properties", 8, "MS-PS4-1",
         "Use mathematical representations to describe a simple model for waves that includes how the amplitude of a wave is related to the energy in a wave.",
         "Wave Properties",
         "Grade 8 Wave Properties Worksheets: Amplitude, Wavelength, Frequency and Wave Speed",
         "Wave Properties",
         "Free middle school science worksheets on wave properties (NGSS MS-PS4-1): amplitude, wavelength, frequency and period, wave speed = frequency × wavelength, and how amplitude relates to energy. 100 practice questions with answers.",
         "Bigger amplitude, more energy.",
         "Wave speed = frequency × wavelength. A larger amplitude carries more energy.",
         body(),
         [("How is amplitude related to the energy of a wave?", "A wave with a larger amplitude carries more energy. Doubling the amplitude gives about four times the energy."),
          ("How do you find wave speed?", "Multiply the frequency by the wavelength: speed = frequency × wavelength."),
          ("Do waves carry matter?", "No. Waves carry energy. The matter they travel through moves back and forth or up and down but stays in place.")],
         sets)


if __name__ == "__main__":
    main()
