# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Waves: Amplitude and Wavelength (4-PS4-1)
  python tools/gen_us_science_g4_waves.py
Waves are regular patterns of motion. Amplitude = height of a crest from the rest line;
wavelength = distance from one crest to the next. A wave moves energy, not the water itself:
a floating object bobs up and down as the wave passes. Bigger amplitude = more energy.
Assessment boundary: no quantitative models of amplitude and wavelength beyond reading a diagram.
Wrong answers come from real mistakes: "wavelength is the height", "a wave carries the water along",
"amplitude is measured from trough to crest".
"""
import math
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, line, text, circle, People, INK, BLUE, RED, GRAY

U = Unit(40106)
R = U.R
P = People(R)


def wave(amp, wl, n=None, W=420, H=150, marks=(), label="a wave", cols=(BLUE,), amp2=None, wl2=None, two=False):
    """amp, wl in grid units (1 unit = 10 px). marks: 'amp', 'wl', 'rest', letters A-D."""
    u = 10
    mid = H // 2
    s = [line(20, mid, W - 10, mid, GRAY, 1, ) .replace("/>", " stroke-dasharray='4 4'/>") if "rest" in marks else ""]
    pts = []
    for x in range(0, W - 40):
        y = mid - amp * u * math.sin(2 * math.pi * x / (wl * u))
        pts.append("%d,%.1f" % (x + 20, y))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join(pts), cols[0]))
    q = wl * u / 4
    if "amp" in marks:
        x = 20 + q
        s.append(line(x, mid, x, mid - amp * u, RED, 2))
        s.append(text(x + 6, mid - amp * u / 2 + 4, "amplitude", 12, "start", col=RED, weight=400))
    if "wl" in marks:
        x0, x1 = 20 + q, 20 + q + wl * u
        y = mid - amp * u - 10
        s.append(line(x0, y, x1, y, RED, 2))
        s.append(line(x0, y - 5, x0, y + 5, RED, 2) + line(x1, y - 5, x1, y + 5, RED, 2))
        s.append(text((x0 + x1) / 2, y - 6, "wavelength", 12, col=RED, weight=400))
    for m in marks:
        if isinstance(m, tuple):
            lab, x0, y0, x1, y1 = m
            s.append(line(x0, y0, x1, y1, INK, 2) + line(x0 - 5, y0, x0 + 5, y0, INK, 2) * (x0 == x1) + line(x1 - 5, y1, x1 + 5, y1, INK, 2) * (x0 == x1)
                     + line(x0, y0 - 5, x0, y0 + 5, INK, 2) * (y0 == y1) + line(x1, y1 - 5, x1, y1 + 5, INK, 2) * (y0 == y1))
            left = x0 == x1 and abs(y1 - y0) < 55
            tx, ty = ((x0 + x1) / 2 + (-14 if left else 12), (y0 + y1) / 2 + 5) if x0 == x1 else ((x0 + x1) / 2, y0 - 6)
            s.append(text(tx, ty, lab, 14))
    return svg_wrap(W, H, "".join(s), label)


def labeled():
    """A wave with four measurements A-D; one is amplitude, one wavelength, two are mistakes."""
    amp = R.choice([3, 4, 5])
    wl = R.choice([14, 16, 18])
    U._last = (amp, wl)
    u = 10
    H = 2 * amp * u + 60
    mid = H // 2
    q = wl * u / 4
    xc = 20 + q            # first crest
    xt = 20 + 3 * q        # first trough
    top, bot = mid - amp * u, mid + amp * u
    ms = {"amp": ("vline", xc, mid, xc, top), "wl": ("hline", xc, top - 12, xc + wl * u, top - 12),
          "full": ("vline", xt + wl * u, top, xt + wl * u, bot), "half": ("hline", xc, bot + 14, xt, bot + 14)}
    # 'full' is crest-to-trough height (twice the amplitude), 'half' is crest to trough distance (half a wavelength)
    keys = ["amp", "wl", "full", "half"]
    R.shuffle(keys)
    letters = dict(zip(keys, "ABCD"))
    marks = []
    for k in keys:
        _, x0, y0, x1, y1 = ms[k]
        marks.append((letters[k], x0, y0, x1, y1))
    svg = wave(amp, wl, marks=["rest"] + marks, H=H, label="a wave with four measurements labeled A, B, C and D")
    return svg, letters


def g_label():
    svg, L = labeled()
    amp, wl = U._last
    val = {"amp": amp, "wl": wl, "full": 2 * amp, "half": wl // 2}
    where = R.choice(["on a rope", "in a pond", "on a long spring", "in a wave tank", "on the ocean"])
    meas = ", ".join("%s = %d cm" % (L[k], val[k]) for k in sorted(L, key=lambda k: L[k]))
    k = R.choice(["amp", "wl", "ampcm", "wlcm"])
    if k == "amp":
        return item(fig(svg) + "This diagram shows a wave %s. Which letter shows the amplitude of the wave?" % where, L["amp"], [L["full"], L["wl"], L["half"]],
                    "Amplitude is measured from the rest line (dashed) to the top of a crest. %s goes from crest to trough, which is twice the amplitude." % L["full"])
    if k == "wl":
        return item(fig(svg) + "This diagram shows a wave %s. Which letter shows one wavelength?" % where, L["wl"], [L["half"], L["amp"], L["full"]],
                    "A wavelength goes from one crest to the next crest. %s only goes from a crest to a trough, which is half a wavelength." % L["half"])
    vs = ["%d cm" % val[x] for x in ("amp", "wl", "full", "half")]
    if len(set(vs)) < 4:
        return None
    if k == "ampcm":
        return item(fig(svg) + "A wave %s was measured: %s. What is the amplitude?" % (where, meas), vs[0], vs[1:],
                    "The amplitude is %s, from the rest line to a crest (%s)." % (vs[0], L["amp"]))
    return item(fig(svg) + "A wave %s was measured: %s. What is the wavelength?" % (where, meas), vs[1], [vs[0], vs[2], vs[3]],
                "The wavelength is %s, from one crest to the next (%s)." % (vs[1], L["wl"]))


def g_compare():
    k = R.choice(["amp", "wl"])
    if k == "amp":
        a1, a2 = R.sample([2, 3, 4, 5], 2)
        wl = R.choice([12, 16])
        w1, w2 = wl, wl
    else:
        w1, w2 = R.sample([8, 12, 16, 20], 2)
        a1 = a2 = 3
    W = 300
    p1 = wave(a1, w1, W=W, H=2 * max(a1, a2) * 10 + 30, label="wave 1")
    p2 = wave(a2, w2, W=W, H=2 * max(a1, a2) * 10 + 30, label="wave 2", cols=(RED,))
    q = "<p><b>Wave 1</b></p>" + fig(p1) + "<p><b>Wave 2</b></p>" + fig(p2)
    if k == "amp":
        big = "Wave 1" if a1 > a2 else "Wave 2"
        ask = R.choice(["larger amplitude", "more energy"])
        return item(q + "Both waves are drawn at the same scale. Which wave has the %s?" % ask, big,
                    ["Wave 2" if big == "Wave 1" else "Wave 1", "They are the same.", "You cannot tell from a picture."],
                    "%s has taller crests, so it has a larger amplitude and carries more energy." % big)
    long_ = "Wave 1" if w1 > w2 else "Wave 2"
    return item(q + "Both waves are drawn at the same scale. Which wave has the longer wavelength?", long_,
                ["Wave 2" if long_ == "Wave 1" else "Wave 1", "They are the same.", "the wave with taller crests"],
                "In %s the crests are farther apart." % long_)


def g_count():
    n = R.choice([2, 3, 4])
    wl = {2: 18, 3: 12, 4: 9}[n]
    W = 20 + n * wl * 10 + 30
    svg = wave(3, wl, W=W, H=90, label="a wave")
    where = R.choice(["on a rope", "in a pond", "on a spring", "in a wave tank", "on a jump rope"])
    if R.random() < 0.4:
        return item(fig(svg) + "This picture shows a wave %s. How many complete wavelengths are shown?" % where, "%d" % n,
                    ["%d" % (n + 1), "%d" % (2 * n), "%d" % (n - 1)], "Count from one crest to the next crest. There are %d full up-and-down patterns." % n)
    L = R.choice([20, 30, 40, 50, 60])
    return item(fig(svg) + "This picture shows a wave %s. Each wavelength is %d cm. How long is the part of the wave shown?" % (where, L),
                "%d cm" % (n * L), ["%d cm" % L, "%d cm" % ((n + 1) * L), "%d cm" % (2 * n * L)],
                "There are %d wavelengths: %d × %d = %d cm." % (n, n, L, n * L))


def g_bob():
    obj = R.choice(["a rubber duck", "a leaf", "a fishing bobber", "a cork", "a small toy boat", "a seagull"])
    k = R.choice(["move", "carry"])
    if k == "move":
        return item("Waves pass under %s floating on a pond. How does it move?" % obj, "mostly up and down",
                    ["along with the waves all the way to the shore", "it does not move at all", "straight down to the bottom"],
                    "A wave moves energy, not the water. The water and the floating object go up and down as the wave passes.")
    return item("Waves move across a lake, but %s floating on the water stays in about the same place. What does this show?" % obj,
                "Waves carry energy, not the water itself.", ["Waves carry the water to the shore.", "The waves have no energy.", "%s is too heavy to float." % obj.capitalize()],
                "The water goes up and down in place while the wave's energy moves forward.")


def g_rope():
    p = P.next()
    k = R.choice(["amp", "wl", "energy"])
    if k == "amp":
        return item("%s shakes one end of a jump rope. How can %s make waves with a larger amplitude?" % (p[0], p[1]), "move the hand higher and lower",
                    ["move the hand faster without moving it farther", "hold the rope still", "use a shorter rope"],
                    "Bigger up-and-down motion makes taller crests.")
    if k == "wl":
        return item("%s shakes a rope up and down faster and faster. What happens to the wavelength?" % p[0], "It gets shorter.",
                    ["It gets longer.", "It stays the same.", "The waves disappear."], "Faster shaking puts the crests closer together.")
    return item("%s makes small waves and then big waves in a long spring. Which waves carry more energy?" % p[0], "the big waves with the larger amplitude",
                ["the small waves", "They carry the same energy.", "Neither wave carries energy."], "A larger amplitude means more energy.")


B1 = bank([
    ("What is a wave?", "a repeating up-and-down (or back-and-forth) motion that moves energy", ["a kind of matter that flows", "water moving to the shore", "a straight line"],
     "Water waves, sound waves and waves on a rope all move energy."),
    ("What is the top of a wave called?", "a crest", ["a trough", "the rest line", "a wavelength"], "The high point is a crest; the low point is a trough."),
    ("What is the bottom of a wave called?", "a trough", ["a crest", "the amplitude", "the top"], "The low point is the trough."),
    ("What is amplitude?", "the height of a wave from the rest line to a crest", ["the distance from crest to crest", "the speed of a wave", "the number of waves"],
     "Amplitude tells how tall the wave is."),
    ("What is wavelength?", "the distance from one crest to the next crest", ["the height of a crest", "the distance from crest to trough, up and down", "how loud a wave is"],
     "Wavelength is measured along the wave."),
    ("Which wave has more energy?", "a wave with a larger amplitude", ["a wave with a smaller amplitude", "a wave with no crests", "All waves have the same energy."],
     "Taller waves carry more energy. Big ocean waves can knock you over."),
    ("What does a wave move from place to place?", "energy", ["the water itself", "sand", "air bubbles only"], "The matter moves up and down; the energy moves forward."),
    ("Sound travels as a wave. What does a louder sound have?", "a larger amplitude", ["a smaller amplitude", "no wavelength", "no energy"],
     "Louder sounds have bigger vibrations and more energy."),
    ("What is the flat line through the middle of a wave called?", "the rest line", ["the crest", "the wavelength", "the trough"],
     "It shows where the water would be with no wave."),
])
B3 = bank([
    ("A stadium crowd does “the wave.” Each person stands up and sits down. Where does each person end up?", "in the same seat", ["at the other end of the stadium", "in the next row", "outside the stadium"],
     "The wave pattern travels around the stadium, but the people only move up and down."),
    ("You flick one end of a rope tied to a doorknob. What travels to the doorknob?", "the wave's energy", ["the rope itself", "your hand", "the air in the room"],
     "The rope moves up and down; the energy travels along it."),
    ("A ribbon is tied to the middle of a jump rope. Waves move along the rope. How does the ribbon move?", "up and down in place", ["along the rope to the end", "it stays perfectly still", "around in circles in the air"],
     "Each part of the rope moves up and down as the wave passes."),
    ("Why does a boat far from shore rise and fall instead of being pushed onto the beach?", "Waves move energy forward while the water moves up and down.", ["Boats are too heavy for waves.", "Waves only move at night.", "Water never moves."],
     "The water under the boat goes up and down as each wave passes."),
    ("A toy boat is at rest on a pool. A friend makes waves at the other end. What makes the boat start bobbing?", "energy carried by the waves", ["wind from the sun", "water flowing from the friend", "gravity pulling the boat sideways"],
     "Waves carry energy across the pool and make the boat move."),
    ("Which waves could knock over a sand castle at the beach?", "waves with a large amplitude", ["waves with a tiny amplitude", "waves with no energy", "a flat calm sea"],
     "Larger amplitude means more energy to push sand."),
    ("When a guitar string vibrates, the air carries a sound wave to your ear. What reaches your ear?", "energy from the vibration", ["air from the guitar", "pieces of the string", "light from the string"],
     "The air vibrates back and forth in place and passes the energy along."),
    ("A long spring is stretched on the floor and one end is pushed. Each coil moves", "back and forth in place as the wave passes", ["all the way to the other end", "up into the air", "nowhere"],
     "The wave moves along the spring; each coil moves only a little."),
])
B5 = bank([
    ("Why can big ocean waves wear away a beach faster than small waves?", "They have a larger amplitude and more energy.", ["They carry more water.", "They are colder.", "They have no wavelength."],
     "More energy can move more sand."),
    ("An earthquake makes waves in the ground. Which waves would shake buildings more?", "waves with a larger amplitude", ["waves with a smaller amplitude", "waves with no energy", "waves in the air only"],
     "Larger amplitude means more energy and more shaking."),
    ("Mia drops a pebble and then a big rock into a pond. Which makes taller waves?", "the big rock", ["the pebble", "They make the same waves.", "Neither makes waves."],
     "The big rock gives the water more energy, so the waves have a larger amplitude."),
    ("A wave pool machine pushes the water harder. What changes?", "The waves get a larger amplitude.", ["The waves stop.", "The water gets colder.", "The pool gets deeper."],
     "More energy in, bigger waves out."),
    ("Leo measures from the top of a crest to the bottom of a trough and says it is the amplitude. What is his mistake?", "That is twice the amplitude; amplitude is from the rest line to a crest.",
     ["That is the wavelength.", "Amplitude is measured sideways.", "There is no mistake."], "Measure amplitude from the middle (rest line)."),
])


def body():
    think = ("<p>A <b>wave</b> is a repeating pattern of motion that moves <b>energy</b> from place to place. The high points are <b>crests</b> and the low points are <b>troughs</b>.</p>"
             "<ul><li><b>Amplitude</b>: the height from the rest line to a crest. A larger amplitude means more energy.</li>"
             "<li><b>Wavelength</b>: the distance from one crest to the next crest.</li></ul>"
             + figure(wave(4, 16, marks=("rest", "amp", "wl"), H=130, label="a wave with amplitude and wavelength marked"), "Amplitude is measured up from the rest line. Wavelength is measured along the wave.")
             + "<p>A wave moves energy, not the water. A floating duck goes up and down as the wave passes, but it stays in about the same place.</p>")
    ex = [("Two waves have the same wavelength. Wave A's crests are taller. Which has more energy?", ["Taller crests = larger amplitude.", "Larger amplitude = more energy."], "Wave A"),
          ("A leaf floats on a pond as waves pass. How does it move?", ["Waves move energy, not water."], "up and down")]
    mist = ["Calling the height of a wave its wavelength.",
            "Measuring amplitude from the trough to the crest. That is twice the amplitude.",
            "Thinking waves carry the water (and floating things) to the shore."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a wave", B1 + [(g_label, 6), (g_count, 5)]),
        ("Amplitude and wavelength", [(g_label, 8), (g_compare, 8), (g_count, 4)]),
        ("Waves move energy, not water", B3 + [(g_bob, 4), (g_rope, 4), (g_compare, 4)]),
        ("Comparing waves", [(g_compare, 10), (g_label, 5), (g_rope, 5)]),
        ("Waves in the real world", B5 + [g_bob, g_rope, g_compare, g_count]),
    ])
    make("grade-4", "waves", 6, "4-PS4-1",
         "Develop a model of waves to describe patterns in terms of amplitude and wavelength and that waves can cause objects to move.",
         "Waves: Amplitude and Wavelength",
         "Grade 4 Waves Worksheets: Amplitude, Wavelength and How Waves Move Energy",
         "Waves",
         "Free Grade 4 science worksheets on waves (NGSS 4-PS4-1): crests and troughs, amplitude and wavelength on wave diagrams, and why a floating object bobs up and down. 100 practice questions with answers.",
         "Waves move energy, not matter.",
         "Amplitude is the height from the rest line to a crest. Wavelength is the distance from crest to crest.",
         body(),
         [("What is the difference between amplitude and wavelength?", "Amplitude is how tall a wave is, from the rest line to a crest. Wavelength is how long it is, from one crest to the next."),
          ("Do waves carry water to the shore?", "No. Waves carry energy. The water mostly moves up and down in place as the wave passes."),
          ("Which wave has more energy?", "The wave with the larger amplitude carries more energy.")],
         sets)


if __name__ == "__main__":
    main()
