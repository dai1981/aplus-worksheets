# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 10: General Wave Properties (including sound)
  python tools/gen_sg_science_s3_general_wave_properties.py
Waves transfer energy without transferring matter; transverse and longitudinal waves; amplitude, wavelength, frequency, period,
speed and wavefront; v = fλ and f = 1/T; displacement-distance and displacement-time graphs; sound as a longitudinal wave with
compressions and rarefactions, needing a medium; the speed of sound in solids, liquids and gases; echoes; the range of human
hearing and ultrasound; pitch and loudness.
UK and US wave makers are reused (Singapore names); wave graphs draw their own SVG.
Wrong answers come from real mistakes: "waves carry water along with them", "the amplitude is the height from trough to crest",
"sound travels fastest in air", "forgetting to halve the echo distance", "a higher pitch means a louder sound".
"""
import math
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, fig, ex
from sci_common import svg_wrap, text, line, BLUE, RED, INK

LV, SUBJ, SORT = 3, "Physics", 10
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_wv = src("gen_uk_science_y9_waves", "g_wspeed")
us_vfl = src("gen_us_science_phys_wave_properties", "g_vfl")
us_per = src("gen_us_science_phys_wave_properties", "g_period")
uk_echo = src("gen_uk_science_y7_sound", "g_echo")
uk_tl = src("gen_uk_science_y11_waves_and_the_electromagnetic_spectrum", "g_tl")


def wave_svg(amp_cm, wl_cm, xlab="distance / cm", n=2.0):
    """sine wave on a grid: amplitude amp_cm, wavelength wl_cm, shown for n wavelengths"""
    W, H = 440, 236
    L, Tp, gw, gh = 56, 20, 360, 170
    xmax = wl_cm * n
    ymax = amp_cm * 1.5
    X = lambda x: L + gw * x / xmax
    Y = lambda y: Tp + gh / 2 - (gh / 2) * y / ymax
    s = []
    steps = 8
    for i in range(steps + 1):
        x = xmax * i / steps
        s.append(line(X(x), Tp, X(x), Tp + gh, col="#ddd", w=1) + text(X(x), Tp + gh + 16, trim("%.4f" % x), fs=11, weight=400))
    for v in (-amp_cm, 0, amp_cm):
        s.append(line(L, Y(v), L + gw, Y(v), col="#ddd" if v else INK, w=1 if v else 1.5) + text(L - 6, Y(v) + 4, trim("%.2f" % v).replace("-", "−"), fs=11, anchor="end", weight=400))
    s.append(line(L, Tp, L, Tp + gh, w=2))
    pts = " ".join("%.1f,%.1f" % (X(xmax * i / 200), Y(amp_cm * math.sin(2 * math.pi * (xmax * i / 200) / wl_cm))) for i in range(201))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (pts, BLUE))
    s.append(text(L + gw / 2, H - 2, xlab, fs=12, weight=400))
    s.append("<text x='14' y='%.1f' font-size='12' text-anchor='middle' transform='rotate(-90 14 %.1f)'>displacement / cm</text>" % (Tp + gh / 2, Tp + gh / 2))
    return svg_wrap(W, H, "".join(s), "wave graph").replace("<svg ", "<svg data-pf='lg' ", 1)


def g_graph():
    amp = R.choice([1, 2, 3, 4, 5])
    if R.random() < 0.5:
        wl = R.choice([4, 6, 8, 10, 12, 16, 20])
        svg = wave_svg(amp, wl, "distance / cm")
        k = R.choice(["A", "wl", "v"])
        q = fig(svg) + "The graph shows a wave at one instant. "
        if k == "A":
            return nq(q + "What is the amplitude?", amp, [2 * amp, wl, wl / 2], " cm", "Amplitude = maximum displacement from the rest position = %d cm." % amp)
        if k == "wl":
            return nq(q + "What is the wavelength?", wl, [wl / 2, 2 * amp, wl * 2], " cm", "One complete wave (crest to crest) spans %d cm." % wl)
        f = R.choice([2, 5, 10, 20, 25])
        return nq(q + "The frequency of the wave is %d Hz. What is its speed?" % f, f * wl / 100, [f * wl, f * wl / 200, wl / f], " m/s",
                  "v = fλ = %d × %s m = %s m/s." % (f, N(wl / 100), N(f * wl / 100)))
    T = R.choice([0.02, 0.04, 0.05, 0.1, 0.2, 0.25, 0.5])
    svg = wave_svg(amp, T, "time / s")
    q = fig(svg) + "The graph shows how the displacement of one point on a wave changes with time. "
    if R.random() < 0.5:
        return nq(q + "What is the period of the wave?", T, [T / 2, 2 * T, 1 / T], " s", "One complete cycle takes %s s." % N(T))
    return nq(q + "What is the frequency of the wave?", 1 / T, [T, 1 / (2 * T), 2 / T], " Hz", "f = 1 ÷ T = 1 ÷ %s = %s Hz." % (N(T), N(1 / T)))


def g_vfl():
    k = R.choice(["v", "f", "l", "T"])
    what, f, l = R.choice([("water wave in a ripple tank", R.choice([2, 4, 5, 8, 10]), R.choice([0.01, 0.015, 0.02, 0.03, 0.05])),
                           ("sound wave in air", R.choice([170, 200, 250, 340, 500, 680, 1000]), None),
                           ("wave on a rope", R.choice([1, 2, 3, 4, 5]), R.choice([0.4, 0.5, 0.8, 1.2, 2])),
                           ("ocean wave", R.choice([0.1, 0.2, 0.25]), R.choice([10, 20, 30, 40]))])
    if l is None:
        l = 340 / f
    v = f * l
    if k == "v":
        return nq("A %s has a frequency of %s Hz and a wavelength of %s m. What is its speed?" % (what, N(f), N(l)), v, [f / l, l / f, f + l], " m/s", "v = fλ = %s × %s = %s m/s." % (N(f), N(l), N(v)))
    if k == "f":
        return nq("A %s travels at %s m/s with a wavelength of %s m. What is its frequency?" % (what, N(v), N(l)), f, [v * l, l / v, v - l], " Hz", "f = v ÷ λ = %s ÷ %s = %s Hz." % (N(v), N(l), N(f)))
    if k == "l":
        return nq("A %s travels at %s m/s with a frequency of %s Hz. What is its wavelength?" % (what, N(v), N(f)), l, [v * f, f / v, v - f], " m", "λ = v ÷ f = %s ÷ %s = %s m." % (N(v), N(f), N(l)))
    return nq("A %s has a frequency of %s Hz. What is its period?" % (what, N(f)), 1 / f, [f, 2 / f, f / 2], " s", "T = 1 ÷ f = 1 ÷ %s = %s s." % (N(f), N(1 / f)))


def g_echo():
    k = R.choice(["d", "d", "t", "v", "sonar"])
    v = 340
    if k == "sonar":
        t = R.choice([0.2, 0.4, 0.5, 0.8, 1, 1.2, 2])
        d = 1500 * t / 2
        return nq("A ship's sonar sends an ultrasound pulse to the seabed. The echo returns after %s s. Sound travels at 1500 m/s in seawater. How deep is the sea?" % N(t), d,
                  [1500 * t, 1500 / t, d / 2], " m", "Distance there and back = 1500 × %s = %s m; depth = half = %s m." % (N(t), N(1500 * t), N(d)))
    d = R.choice([17, 34, 51, 68, 85, 102, 170, 255, 340])
    t = 2 * d / v
    if k == "d":
        return nq("A student claps in front of a tall wall and hears the echo %s s later. The speed of sound in air is 340 m/s. How far away is the wall?" % N(t), d, [v * t, v / t, d / 2], " m",
                  "Sound travels to the wall and back: 2d = 340 × %s, so d = %s m." % (N(t), N(d)))
    if k == "t":
        return nq("A wall is %d m away. How long after a shout is the echo heard? (speed of sound = 340 m/s)" % d, t, [d / v, v / d, t * 2], " s", "t = 2d ÷ v = %d ÷ 340 = %s s." % (2 * d, N(t)))
    vv = R.choice([320, 330, 340, 350])
    t2 = round(2 * d / vv, 3)
    return nq("A student stands %d m from a cliff. The echo of her clap is heard %s s later. What is the speed of sound?" % (d, N(t2)), 2 * d / t2, [d / t2, t2 / d, 2 * d * t2], " m/s",
              "v = 2d ÷ t = %d ÷ %s = %s m/s." % (2 * d, N(t2), nf(2 * d / t2)))


MED = [("steel", 5000), ("water", 1500), ("air", 340)]


def g_med():
    k = R.choice(["fast", "slow", "why", "vac"])
    if k == "fast":
        return tq("In which medium does sound travel fastest: air, water, steel or a vacuum?", "steel", ["air", "water", "a vacuum"], "Sound is fastest in solids, slower in liquids, slowest in gases, and cannot travel in a vacuum.")
    if k == "slow":
        return tq("In which of these does sound travel slowest: steel, concrete, water or air?", "air", ["steel", "concrete", "water"], "Gas particles are far apart, so vibrations pass on slowly.")
    if k == "why":
        return tq("Why does sound travel faster in solids than in gases?", "The particles are closer together, so vibrations are passed on more quickly.", ["Solids are hotter.", "Sound is a transverse wave.", "Gases have no particles."], "Sound needs particles to vibrate.")
    return tq("A ringing bell is placed in a jar and the air is pumped out. What happens to the sound heard?", "It becomes fainter until it can hardly be heard.", ["It becomes louder.", "Its pitch rises.", "It does not change."], "Sound cannot travel through a vacuum.")


TL = [("the vibrations are perpendicular to the direction of wave travel", "transverse"), ("the vibrations are parallel to the direction of wave travel", "longitudinal"),
      ("it has crests and troughs", "transverse"), ("it has compressions and rarefactions", "longitudinal"), ("sound waves", "longitudinal"), ("light waves", "transverse"),
      ("water ripples", "transverse"), ("waves on a slinky pushed back and forth along its length", "longitudinal"), ("radio waves", "transverse"), ("ultrasound", "longitudinal")]


def g_tl():
    q, a = R.choice(TL)
    return tq("Is this a transverse or a longitudinal wave: %s?" % q, a, ["transverse" if a == "longitudinal" else "longitudinal", "both", "neither: it is not a wave"],
              "Transverse: vibration at right angles to travel. Longitudinal: vibration along the direction of travel.")


PL = [("a higher frequency", "a higher pitch"), ("a larger amplitude", "a louder sound"), ("a lower frequency", "a lower pitch"), ("a smaller amplitude", "a softer sound")]
g_pl = rows(R, PL, "What does %s of a sound wave give?", "Which change to a sound wave gives %s?")

POOL1 = pool(R, [
    ("What do waves transfer?", "energy, without transferring matter", ["matter, without energy", "both matter and energy", "only sound"], "A cork on a pond bobs up and down but stays in place."),
    ("What is the amplitude of a wave?", "the maximum displacement of a point from its rest position", ["the distance from crest to trough", "the distance between two crests", "the number of waves per second"], "Measured from the middle line."),
    ("What is the wavelength of a wave?", "the shortest distance between two points in phase, such as two neighbouring crests", ["the height of a crest", "the time for one wave", "the distance from crest to trough"], "Symbol λ, unit m."),
    ("What is the frequency of a wave?", "the number of complete waves produced per second", ["the time for one wave", "the length of one wave", "the speed of the wave"], "Unit: hertz (Hz)."),
    ("What is the period of a wave?", "the time taken to produce one complete wave", ["the number of waves per second", "the distance travelled in one second", "the height of a wave"], "T = 1 ÷ f."),
    ("What is a wavefront?", "a line joining points on a wave that are in phase, such as all the crests", ["the front edge of the water", "the fastest part of a wave", "the direction of the wave"], "Wavefronts are perpendicular to the direction of travel."),
    ("What is a compression in a sound wave?", "a region where the air particles are closer together and the pressure is higher", ["a region where particles are far apart", "the top of a crest", "a silent region"], "Rarefactions are where particles are further apart."),
    ("Why can sound not travel through outer space?", "Space is a vacuum with no particles to pass on the vibrations.", ["Space is too cold.", "Sound is too slow.", "Space is too dark."], "Sound needs a medium."),
    ("What is the range of frequencies a healthy young person can hear?", "about 20 Hz to 20 000 Hz", ["about 2 Hz to 200 Hz", "about 200 Hz to 2000 Hz", "about 20 000 Hz to 200 000 Hz"], "Above 20 kHz is ultrasound."),
    ("What is ultrasound?", "sound with a frequency above 20 000 Hz", ["sound below 20 Hz", "very loud sound", "sound that travels faster than light"], "Used in medical scans and sonar."),
])
POOL5 = pool(R, [
    ("A student watches a firework 680 m away. How long after the flash does she hear the bang? (speed of sound = 340 m/s)", "2 s", ["4 s", "0.5 s", "1 s"], "Light arrives almost at once; t = 680 ÷ 340."),
    ("Why do doctors use ultrasound rather than X-rays to scan an unborn baby?", "Ultrasound is not ionising, so it is safer for the baby.", ["Ultrasound travels faster.", "X-rays cannot pass through skin.", "Ultrasound is cheaper to see."], "Echoes from tissue boundaries build up an image."),
    ("Two notes have the same loudness. Note A has a frequency of 500 Hz and note B 1000 Hz. Which is true?", "B has a higher pitch.", ["A has a higher pitch.", "B is louder.", "They have the same pitch."], "Higher frequency, higher pitch."),
    ("A wave's frequency doubles while its speed stays the same. What happens to its wavelength?", "It halves.", ["It doubles.", "It stays the same.", "It becomes four times as long."], "λ = v ÷ f."),
    ("A cork floats on a pond as ripples pass. How does it move?", "up and down, staying in about the same place", ["along with the ripples to the edge", "in a circle across the pond", "it does not move"], "The water does not travel with the wave."),
    ("Why is an echo not heard from a wall only 5 m away?", "The echo returns too quickly (in about 0.03 s) to be heard separately from the original sound.", ["Sound cannot reflect from walls.", "The wall absorbs all the sound.", "5 m is too far."], "The ear needs about 0.1 s between sounds."),
    ("A guitar string is plucked harder. What changes?", "The amplitude increases, so the sound is louder.", ["The frequency increases.", "The pitch falls.", "The speed of sound increases."], "Pitch depends on frequency, loudness on amplitude."),
    ("A dolphin's click has a frequency of 150 000 Hz. Can a person hear it?", "No, it is ultrasound (above 20 000 Hz).", ["Yes, it is very loud.", "Yes, it is in the normal range.", "No, it is below 20 Hz."], "Humans hear about 20 Hz to 20 kHz."),
    ("Ten wave crests pass a point in 2 s. What is the frequency?", "5 Hz", ["20 Hz", "0.2 Hz", "10 Hz"], "f = 10 ÷ 2."),
    ("Why do you see lightning before you hear thunder?", "Light travels much faster than sound.", ["Thunder happens later.", "Sound is reflected by clouds.", "Light is louder."], "Light: 3 × 10⁸ m/s; sound in air: about 340 m/s."),
])


def main():
    sets = U.sets([
        ("Describing waves", [POOL1, (g_tl, 6), (uk_tl, 3), (g_pl, 2)]),
        ("Wave graphs", [(g_graph, 14), POOL1, (g_tl, 2)]),
        ("Wave speed: v = fλ", [(g_vfl, 10), (uk_wv, 4), (us_vfl, 3), (us_per, 3)]),
        ("Sound", [(g_med, 4), (g_pl, 5), (g_echo, 6), (uk_echo, 3), POOL1]),
        ("Echoes and exam-style questions", [(POOL5, 10), (g_echo, 5), (g_vfl, 3), (g_graph, 2)]),
    ])
    make_ol(LV, SUBJ, "general-wave-properties", SORT, "General Wave Properties",
            "Describe what is meant by wave motion and show understanding that waves transfer energy without transferring matter; define speed, frequency, wavelength, "
            "period and amplitude and recall and apply v = fλ; compare transverse and longitudinal waves; interpret displacement-distance and displacement-time graphs; "
            "describe sound as a longitudinal wave made of compressions and rarefactions that needs a medium; compare the speed of sound in solids, liquids and gases; "
            "describe echoes and the use of ultrasound; relate loudness to amplitude and pitch to frequency (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "General Wave Properties", "Waves and sound",
            "Free Secondary 3 O-Level Physics worksheets on general wave properties: transverse and longitudinal waves, amplitude, wavelength, frequency, v = fλ, wave graphs, "
            "sound, echoes and ultrasound. 100 questions with answers.",
            "Wave speed = frequency × wavelength", "Waves transfer energy, not matter.",
            "<p><b>A wave transfers energy without transferring matter.</b></p><ul>"
            "<li>Transverse waves (light, water ripples) vibrate at right angles to the direction of travel; longitudinal waves (sound) vibrate along it.</li>"
            "<li>v = fλ and f = 1 ÷ T. Amplitude is measured from the rest position.</li>"
            "<li>Sound needs a medium: fastest in solids, slowest in gases, none in a vacuum (about 340 m/s in air). For an echo, distance = speed × time ÷ 2.</li>"
            "<li>Larger amplitude: louder. Higher frequency: higher pitch. Humans hear about 20 Hz to 20 kHz; above that is ultrasound.</li></ul>",
            [("f = 50 Hz, λ = 0.4 m. Speed?", ["v = 50 × 0.4"], "20 m/s"),
             ("An echo returns after 1.5 s (v = 340 m/s). Distance to the wall?", ["2d = 340 × 1.5 = 510", "d = 510 ÷ 2"], "255 m")],
            ["Measuring the amplitude from crest to trough. It is from the middle line to a crest.", "Forgetting to halve the distance in echo questions.",
             "Saying sound is fastest in air. It is fastest in solids.", "Mixing up pitch (frequency) and loudness (amplitude)."],
            [("What is the wave equation?", "v = fλ: wave speed (m/s) = frequency (Hz) × wavelength (m). Also f = 1 ÷ T."),
             ("What is the difference between transverse and longitudinal waves?", "In transverse waves the particles vibrate at right angles to the direction the wave travels; in longitudinal waves they vibrate along that direction."),
             ("How do you find a distance from an echo?", "Multiply the speed of sound by the echo time to get the distance there and back, then divide by 2.")],
            sets)


if __name__ == "__main__":
    main()
