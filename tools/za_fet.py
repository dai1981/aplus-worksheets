# -*- coding: utf-8 -*-
"""South Africa, CAPS FET (Grades 10-12): shared helpers, own makers and question pools for za_s10 / za_s11 / za_s12."""
import math
from za_sci import ZU
from au_sci import nq
import uk_alsci

PC, PP, LS = "Physical Sciences: Chemistry", "Physical Sciences: Physics", "Life Sciences"


def L(a, b):
    return "<p>%s</p><p>%s</p>" % (a, b)


def U(area, sort, slug, topic, std, title, short, what, kb, ks, a, b, ex, mist, faq, sets, grade, allow=()):
    subj = "Life Sciences" if area == LS else "Physical Sciences"
    meta = "Free Grade %d %s worksheets (CAPS): %s. 100 questions with answers." % (grade, subj, what)
    return ZU(area, sort, slug, topic, std, title, short, meta, kb, ks, L(a, b), ex, mist, faq, sets, allow)


def M(*parts, n=20):
    """share n questions between parts: "mod:slug:set" strings, makers, or GM lists [(maker, k)]"""
    flat = []
    for p in parts:
        if isinstance(p, list):
            flat += [f for f, _ in p]
        else:
            flat.append(p)
    k, r = divmod(n, len(flat))
    return [(p, k + (1 if i < r else 0)) for i, p in enumerate(flat)]


def g3(x):
    import au_sci
    return au_sci.trim(uk_alsci.nf(x))


# ---------------- own number makers ----------------

def share(R):
    """Grade 10 electrostatics: two identical conducting spheres touch and separate"""
    def f():
        q1 = R.choice([-1, 1]) * R.randint(2, 12) * 2
        q2 = R.choice([-1, 1]) * R.randint(1, 12) * 2
        if q1 + q2 == 0 or q1 == q2:
            return None
        qf = (q1 + q2) / 2
        if R.random() < 0.55:
            return nq("Two identical metal spheres carry charges of %+d nC and %+d nC. They touch and are then separated. What is the charge on each sphere now?" % (q1, q2),
                      qf, [q1 + q2, (q1 - q2) / 2, (abs(q1) + abs(q2)) / 2], " nC",
                      "Identical spheres share the total charge equally: Q = (Q₁ + Q₂)/2 = (%+d + %+d)/2 = <b>%+g nC</b>." % (q1, q2, qf))
        dq = abs(qf - q1) * 1e-9
        n = dq / 1.6e-19
        return nq("Two identical metal spheres carry %+d nC and %+d nC. They touch and separate. How many electrons are transferred? (e = 1.6 × 10⁻¹⁹ C)" % (q1, q2),
                  n, [abs(q1 + q2) * 1e-9 / 1.6e-19, dq * 1.6e-19, dq / 1.6e-19 * 2], " electrons",
                  "Each sphere ends with %+g nC, so the charge on the first sphere changes by %g nC. n = ΔQ/e = %g × 10⁻⁹ / 1.6 × 10⁻¹⁹ = <b>%s</b>." % (qf, abs(qf - q1), abs(qf - q1), g3(n)))
    return f


def vpm(R, kind=None):
    """Grade 12 vertical projectile motion (g = 9.8 m/s², upwards positive)"""
    g = 9.8

    def f():
        k = kind or R.choice(("h", "t", "tt", "v", "drop", "hit"))
        u = R.choice((5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24, 25, 30))
        if k == "h":
            h = u * u / (2 * g)
            return nq("A ball is thrown vertically upwards at %d m/s. Ignoring air resistance, what is its maximum height above the point of release?" % u,
                      h, [u * u / g, u / (2 * g), u * u / 20], " m", "At the top v = 0: v² = u² + 2aΔy → 0 = %d² − 2(9.8)Δy, so Δy = %d²/19.6 = <b>%s m</b>." % (u, u, g3(h)))
        if k == "t":
            t = u / g
            return nq("A stone is thrown straight up at %d m/s. How long does it take to reach its highest point?" % u,
                      t, [2 * u / g, u * g, u / 10 if u % 10 else u / 9], " s", "At the top v = 0: v = u + at → 0 = %d − 9.8t, so t = %d/9.8 = <b>%s s</b>." % (u, u, g3(t)))
        if k == "tt":
            t = 2 * u / g
            return nq("A ball is thrown vertically upwards at %d m/s and caught at the same height. How long is it in the air?" % u,
                      t, [u / g, 4 * u / g, u * u / (2 * g)], " s", "Time up = %d/9.8 s; the time down is the same, so the total is 2 × %d/9.8 = <b>%s s</b>." % (u, u, g3(t)))
        if k == "v":
            t = R.choice((0.5, 1, 1.5, 2, 2.5, 3))
            v = u - g * t
            if abs(v) < 0.5:
                return None
            d = "upwards" if v > 0 else "downwards"
            it = nq("A ball is thrown upwards at %d m/s. What is its speed %g s later?" % (u, t),
                    abs(v), [u + g * t, abs(u - 10 * t) if abs(u - 10 * t) > 0.1 else u, g * t], " m/s",
                    "v = u + at = %d − 9.8(%g) = %s m/s, so the speed is <b>%s m/s</b> and it is moving %s." % (u, t, g3(v), g3(abs(v)), d))
            return it
        if k == "drop":
            h = R.choice((5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 80))
            t = math.sqrt(2 * h / g)
            return nq("A stone is dropped from rest from a height of %d m. How long does it take to hit the ground?" % h,
                      t, [2 * h / g, math.sqrt(h / g), h / g], " s", "Δy = ½gt² → %d = 4.9t², so t = √(%d/4.9) = <b>%s s</b>." % (h, h, g3(t)))
        h = R.choice((5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 80))
        v = math.sqrt(2 * g * h)
        return nq("An object falls freely from rest through %d m. What is its speed just before it hits the ground?" % h,
                  v, [g * h, 2 * g * h, math.sqrt(g * h)], " m/s", "v² = u² + 2gΔy = 0 + 2(9.8)(%d) = %s, so v = <b>%s m/s</b>." % (h, g3(2 * g * h), g3(v)))
    return f


def doppler(R, kind=None):
    """Grade 12 Doppler effect for sound: f_L = (v ± v_L)/(v ± v_s) f_s, v = 340 m/s"""
    v = 340
    SRC = ("an ambulance siren", "a police car siren", "a train hooter", "a fire engine siren", "a car hooter", "a motorbike horn")

    def f():
        k = kind or R.choice(("app", "rec", "lis", "vs"))
        fs = R.choice((400, 450, 480, 500, 520, 600, 640, 700, 750, 800, 850, 900, 1000, 1200))
        vs = R.choice((10, 15, 17, 20, 25, 30, 34, 35, 40))
        s = R.choice(SRC)
        if k == "app":
            fl = v / (v - vs) * fs
            return nq("%s of frequency %d Hz moves towards a stationary listener at %d m/s. What frequency does the listener hear? (speed of sound 340 m/s)" % (s[0].upper() + s[1:], fs, vs),
                      fl, [v / (v + vs) * fs, (v + vs) / v * fs, fs], " Hz",
                      "f<sub>L</sub> = v/(v − v<sub>s</sub>) × f<sub>s</sub> = 340/(340 − %d) × %d = <b>%s Hz</b>. The source moves towards you, so the pitch is higher." % (vs, fs, g3(fl)))
        if k == "rec":
            fl = v / (v + vs) * fs
            return nq("%s of frequency %d Hz moves away from a stationary listener at %d m/s. What frequency does the listener hear? (speed of sound 340 m/s)" % (s[0].upper() + s[1:], fs, vs),
                      fl, [v / (v - vs) * fs, (v - vs) / v * fs if vs > 20 else fs * 0.9, fs], " Hz",
                      "f<sub>L</sub> = v/(v + v<sub>s</sub>) × f<sub>s</sub> = 340/(340 + %d) × %d = <b>%s Hz</b>. The source moves away, so the pitch is lower." % (vs, fs, g3(fl)))
        if k == "lis":
            vl = R.choice((10, 15, 20, 25, 30))
            fl = (v + vl) / v * fs
            return nq("A cyclist rides at %d m/s towards a stationary %s that emits %d Hz. What frequency does the cyclist hear? (speed of sound 340 m/s)" % (vl, s.split(" ", 1)[1], fs),
                      fl, [(v - vl) / v * fs, v / (v - vl) * fs, fs], " Hz",
                      "f<sub>L</sub> = (v + v<sub>L</sub>)/v × f<sub>s</sub> = (340 + %d)/340 × %d = <b>%s Hz</b>." % (vl, fs, g3(fl)))
        fl = v / (v - vs) * fs
        fl = round(fl)
        vs2 = v * (1 - fs / fl)
        return nq("%s emits %d Hz. A stationary listener hears %d Hz as it approaches. How fast is the source moving? (speed of sound 340 m/s)" % (s[0].upper() + s[1:], fs, fl),
                  vs2, [v * (fl / fs - 1), fl - fs, v * fs / fl], " m/s",
                  "%d = 340/(340 − v<sub>s</sub>) × %d → 340 − v<sub>s</sub> = 340 × %d/%d = %s, so v<sub>s</sub> = <b>%s m/s</b>." % (fl, fs, fs, fl, g3(v * fs / fl), g3(vs2)))
    return f


# ---------------- hand-written pools: (question, answer, [wrong x3], explanation) ----------------

DOPPLER = [
    ("What is the Doppler effect?", "the change in observed frequency when the source and listener move relative to each other", ["the echo of sound off a wall", "the bending of waves around a corner", "the increase in loudness close to a source"], "It is the apparent change in frequency (or pitch) caused by relative motion."),
    ("An ambulance approaches you with its siren on. What do you hear?", "a higher pitch than the siren actually makes", ["a lower pitch than the siren makes", "the same pitch, only louder", "no change at all"], "Wavefronts are squashed together in front of the moving source, so the frequency is higher."),
    ("An ambulance passes you and drives away. What happens to the pitch you hear?", "it drops suddenly to a lower pitch", ["it rises to a higher pitch", "it stays the same", "it drops to zero"], "Behind the moving source the wavefronts are spread out, so the frequency is lower."),
    ("In front of a moving sound source, the wavelength is …", "shorter than when the source is at rest", ["longer than when the source is at rest", "the same as when the source is at rest", "zero"], "The source moves after each wavefront, so wavefronts in front are closer together."),
    ("Behind a moving sound source, the wavelength is …", "longer than when the source is at rest", ["shorter than when the source is at rest", "the same as when the source is at rest", "half the speed of sound"], "Wavefronts behind the source are spread out."),
    ("Does the speed of sound change when the source moves?", "no, it depends only on the medium", ["yes, it increases by the source's speed", "yes, it decreases", "only for loud sounds"], "The speed of sound depends on the medium; only the frequency and wavelength observed change."),
    ("Does the frequency emitted by the source change when it moves?", "no, only the frequency the listener detects changes", ["yes, the source vibrates faster", "yes, it doubles", "only when it moves away"], "The source still vibrates at the same rate; the listener detects a different frequency."),
    ("Which sign is used for v<sub>s</sub> in f<sub>L</sub> = v/(v ± v<sub>s</sub>) f<sub>s</sub> when the source moves towards the listener?", "minus (v − v<sub>s</sub>)", ["plus (v + v<sub>s</sub>)", "no sign; v<sub>s</sub> is left out", "multiply by v<sub>s</sub>"], "A smaller denominator gives a larger frequency, which is what happens as the source approaches."),
    ("Which sign is used for v<sub>L</sub> in f<sub>L</sub> = (v ± v<sub>L</sub>)/v f<sub>s</sub> when the listener moves towards the source?", "plus (v + v<sub>L</sub>)", ["minus (v − v<sub>L</sub>)", "no sign", "divide by v<sub>L</sub>"], "Moving towards the source, the listener meets wavefronts more often, so the frequency rises."),
    ("How do doctors use the Doppler effect?", "to measure the speed of blood flow and the heartbeat of a foetus", ["to take X-ray photographs of bones", "to kill bacteria", "to measure body temperature"], "Ultrasound reflected from moving blood cells changes frequency; the change gives the speed."),
    ("How does a traffic officer's speed trap use the Doppler effect?", "it measures the change in frequency of waves reflected from a moving car", ["it measures how loud the car is", "it times the car between two lines painted on the road", "it photographs the number plate only"], "The frequency shift of the reflected radar or laser waves gives the car's speed."),
    ("What is a red shift?", "light from a galaxy moving away is shifted to longer wavelengths", ["light from a hot star is red", "light bends towards red near the Sun", "red light travels faster than blue light"], "The Doppler effect for light: a receding source shows longer, redder wavelengths."),
    ("What is a blue shift?", "light from an approaching source is shifted to shorter wavelengths", ["light scattered by the sky", "light from a cold star", "light that has been reflected twice"], "An approaching source shows shorter wavelengths, towards the blue end."),
    ("Most distant galaxies show a red shift. What does this tell us?", "they are moving away from us, so the universe is expanding", ["they are moving towards us", "they are made of red stars", "they are very hot"], "The red shift of galaxies is evidence for an expanding universe."),
    ("Spectral lines from a star are shifted towards the red end. Is the star approaching or receding?", "receding (moving away)", ["approaching", "not moving at all", "it cannot be told from a spectrum"], "Red shift means the source is moving away."),
    ("A source of sound moves towards you. Does the loudness explain the change in pitch?", "no; pitch depends on frequency, which changes because of the motion", ["yes; louder sounds have a higher pitch", "yes; pitch and loudness are the same", "no; pitch depends on the speed of sound"], "Loudness depends on amplitude; pitch depends on frequency."),
    ("A listener and a source both stand still, but the wind blows. Is there a Doppler shift?", "no, there is no relative motion between source and listener", ["yes, the pitch rises", "yes, the pitch drops", "only if it is a strong wind"], "There must be relative motion between source and listener for a Doppler shift (in CAPS problems)."),
    ("Bats find insects using reflected sound. How can a bat tell that an insect is flying towards it?", "the echo comes back at a higher frequency", ["the echo is quieter", "the echo comes back at a lower frequency", "the echo takes longer to return"], "An approaching reflector returns a higher frequency."),
    ("Why does the pitch of a passing car change suddenly, not slowly, at the moment it passes?", "the car changes from approaching to moving away", ["the engine slows down", "the sound reflects off the road", "the air changes temperature"], "Before it passes the frequency is higher, after it passes it is lower."),
    ("What happens to the observed frequency if the source moves faster towards the listener?", "it increases further", ["it decreases", "it stays the same", "it becomes the same as the source frequency"], "A larger v<sub>s</sub> makes v − v<sub>s</sub> smaller, so f<sub>L</sub> is bigger."),
    ("In the Doppler formula, what does v stand for?", "the speed of sound in the medium", ["the speed of the source", "the speed of the listener", "the frequency of the source"], "v is the speed of the wave in air, often 340 m/s."),
    ("Which change shows that light from a galaxy is red-shifted?", "the absorption lines of hydrogen appear at longer wavelengths than in the laboratory", ["the galaxy looks brighter", "the lines appear at shorter wavelengths", "the galaxy looks smaller"], "The same element's lines are compared with lines measured at rest on Earth."),
    ("A siren of 800 Hz approaches you. Which value could you hear?", "850 Hz", ["800 Hz", "750 Hz", "400 Hz"], "An approaching source sounds higher than the frequency it emits."),
    ("A siren of 600 Hz moves away from you. Which value could you hear?", "570 Hz", ["600 Hz", "630 Hz", "1 200 Hz"], "A receding source sounds lower than the frequency it emits."),
]

FERT = [
    ("What do the letters N, P and K on a bag of fertiliser stand for?", "nitrogen, phosphorus and potassium", ["neon, potassium and krypton", "nitrogen, potassium and calcium", "sodium, phosphorus and potassium"], "These are the three primary nutrients plants need."),
    ("A bag of fertiliser is labelled 3:2:1 (25). What does the 25 mean?", "25% of the mass of the fertiliser is the nutrients N, P and K", ["the bag contains 25 kg", "the fertiliser lasts 25 days", "it contains 25% nitrogen only"], "The number in brackets is the total percentage of N, P and K."),
    ("Why do plants need nitrogen?", "to make proteins and chlorophyll, for leaf growth", ["to make strong roots and flowers only", "to open their stomata", "to absorb sunlight directly"], "Nitrogen is part of amino acids, proteins and chlorophyll."),
    ("Why do plants need phosphorus?", "for root growth, flowers and fruit, and to make ATP and DNA", ["only to make chlorophyll", "to make the leaves green", "to make cell walls of cellulose"], "Phosphorus is part of ATP, DNA and cell membranes."),
    ("Why do plants need potassium?", "for healthy flowers and fruit and for resistance to disease", ["to make proteins", "to make glucose directly", "to fix nitrogen from the air"], "Potassium helps with enzyme action, water balance, flowering and disease resistance."),
    ("Which industrial process makes ammonia?", "the Haber process", ["the Ostwald process", "the contact process", "fractional distillation"], "N₂ + 3H₂ ⇌ 2NH₃, with an iron catalyst."),
    ("Which industrial process makes nitric acid from ammonia?", "the Ostwald process", ["the Haber process", "the contact process", "electrolysis of brine"], "Ammonia is oxidised to NO, then NO₂, which reacts with water to make HNO₃."),
    ("Which industrial process makes sulfuric acid?", "the contact process", ["the Haber process", "the Ostwald process", "cracking"], "SO₂ is oxidised to SO₃ over V₂O₅, then made into H₂SO₄."),
    ("Which catalyst is used in the Haber process?", "iron", ["vanadium(V) oxide", "platinum", "nickel"], "Finely divided iron speeds up the reaction."),
    ("Which catalyst is used in the contact process?", "vanadium(V) oxide, V₂O₅", ["iron", "platinum–rhodium", "manganese dioxide"], "V₂O₅ catalyses 2SO₂ + O₂ ⇌ 2SO₃."),
    ("Which catalyst is used in the Ostwald process?", "platinum (with rhodium)", ["iron", "vanadium(V) oxide", "copper"], "Ammonia is oxidised to NO over a platinum gauze."),
    ("Where does the nitrogen for the Haber process come from?", "the air (by fractional distillation of liquid air)", ["natural gas", "sea water", "coal"], "Air is about 78% nitrogen."),
    ("Where does the hydrogen for the Haber process usually come from?", "natural gas or coal (methane and steam)", ["the air", "sulfur", "limestone"], "In South Africa, Sasol makes hydrogen from coal."),
    ("Ammonia reacts with nitric acid. Which fertiliser forms?", "ammonium nitrate, NH₄NO₃", ["ammonium sulfate", "potassium chloride", "calcium phosphate"], "NH₃ + HNO₃ → NH₄NO₃."),
    ("Ammonia reacts with sulfuric acid. Which fertiliser forms?", "ammonium sulfate, (NH₄)₂SO₄", ["ammonium nitrate", "urea", "superphosphate"], "2NH₃ + H₂SO₄ → (NH₄)₂SO₄."),
    ("How is a phosphate fertiliser such as superphosphate made?", "phosphate rock is treated with sulfuric acid", ["ammonia reacts with nitric acid", "nitrogen is fixed from the air", "potash is mined and crushed"], "Insoluble phosphate rock is made soluble with sulfuric acid."),
    ("Where is phosphate rock mined in South Africa?", "Phalaborwa in Limpopo", ["Sasolburg", "the Witwatersrand gold reef", "Saldanha Bay"], "Phalaborwa has large phosphate deposits."),
    ("What is eutrophication?", "excess nutrients in water cause algae to grow fast, then decompose and use up oxygen", ["water becoming more acidic from rain", "water evaporating from dams", "soil being washed away by wind"], "Fertiliser runoff adds nitrates and phosphates to rivers and dams."),
    ("Why do fish die in water affected by eutrophication?", "bacteria decomposing dead algae use up the dissolved oxygen", ["the fertiliser is poisonous to fish", "the water becomes too warm", "the algae eat the fish"], "Low oxygen levels kill fish and other animals."),
    ("Name one way farmers can reduce fertiliser runoff.", "apply only the amount needed, not before heavy rain", ["add more fertiliser at once", "spread fertiliser on the river banks", "water the crops straight after spreading too much"], "Careful use reduces runoff into rivers and dams."),
    ("Why do farmers need fertilisers?", "crops remove nutrients from the soil, which must be replaced", ["fertilisers kill all insects", "they make the soil less acidic in all cases", "plants need them for photosynthesis as an energy source"], "Harvesting crops removes N, P and K from the soil each season."),
    ("In the Haber process, N₂ + 3H₂ ⇌ 2NH₃ is exothermic. Why is a moderate temperature (about 450 °C) used?", "a compromise between a good yield and a fast enough rate", ["a high temperature gives the best yield", "the catalyst works only at 0 °C", "ammonia boils at 450 °C"], "A lower temperature gives more ammonia but the reaction would be too slow."),
    ("Why is a high pressure used in the Haber process?", "the forward reaction makes fewer moles of gas, so high pressure favours ammonia", ["high pressure lowers the cost", "high pressure slows the reaction", "high pressure stops the catalyst from working"], "4 mol of gas → 2 mol of gas; Le Chatelier's principle."),
    ("What is done with unreacted nitrogen and hydrogen in the Haber process?", "it is recycled back into the reactor", ["it is released into the air", "it is burnt as fuel", "it is dissolved in water"], "Recycling raises the overall yield."),
    ("What is the formula of urea, a nitrogen fertiliser?", "CO(NH₂)₂", ["NH₄NO₃", "(NH₄)₂SO₄", "KCl"], "Urea is made from ammonia and carbon dioxide."),
    ("Which fertiliser contains the highest percentage of nitrogen by mass?", "urea, CO(NH₂)₂ (about 47%)", ["ammonium sulfate (about 21%)", "potassium chloride (0%)", "ammonium nitrate (about 35%)"], "Urea has 28 g of N in 60 g, about 47%."),
    ("Which South African company makes ammonia and fertilisers from coal at Sasolburg and Secunda?", "Sasol", ["Eskom", "Transnet", "Telkom"], "Sasol uses coal to make hydrogen for ammonia."),
    ("Potassium for fertiliser is usually supplied as …", "potassium chloride (potash)", ["potassium nitrate made by the Haber process", "potassium sulfate from sea shells", "pure potassium metal"], "Potash is mined, mostly as KCl."),
    ("What is the first step of the Ostwald process?", "4NH₃ + 5O₂ → 4NO + 6H₂O over platinum", ["N₂ + 3H₂ → 2NH₃", "2SO₂ + O₂ → 2SO₃", "NH₃ + HNO₃ → NH₄NO₃"], "Ammonia is oxidised to nitrogen monoxide."),
    ("In the contact process, SO₃ is dissolved in concentrated H₂SO₄, not in water. Why?", "SO₃ and water react very exothermically and form a mist of acid", ["SO₃ does not react with water", "water would dilute the catalyst", "it makes the acid cheaper"], "SO₃ in H₂SO₄ gives oleum, H₂S₂O₇, which is then diluted."),
]

VERT = [
    ("A frog lays its eggs in water, where a male fertilises them. What type of fertilisation is this?", "external fertilisation", ["internal fertilisation", "self-fertilisation", "double fertilisation"], "Fertilisation happens outside the female's body."),
    ("In which group of animals is external fertilisation most common?", "fish and amphibians", ["birds and mammals", "reptiles and birds", "mammals only"], "These animals reproduce in water, where sperm can swim to the eggs."),
    ("What is internal fertilisation?", "the sperm fertilises the egg inside the female's body", ["the egg is fertilised in water", "an animal fertilises its own eggs", "the egg develops without fertilisation"], "Reptiles, birds and mammals have internal fertilisation."),
    ("Why is internal fertilisation an advantage on land?", "gametes do not dry out and more eggs are fertilised", ["animals can produce more eggs", "no mating is needed", "the eggs are bigger"], "The sperm swims in fluids inside the female's body."),
    ("Why do fish and frogs produce very many eggs?", "most eggs are not fertilised or are eaten, so many are needed for some to survive", ["the parents look after each egg", "their eggs have hard shells", "they reproduce only once in a lifetime"], "External fertilisation and little parental care mean a high loss of eggs."),
    ("What is ovipary?", "laying eggs that develop and hatch outside the mother's body", ["giving birth to live young fed by a placenta", "eggs that hatch inside the mother", "reproduction without eggs"], "Birds, most reptiles, fish and amphibians are oviparous."),
    ("What is vivipary?", "the embryo develops inside the mother and is fed through a placenta; live young are born", ["laying eggs with shells", "eggs that hatch inside the mother without a placenta", "fertilisation in water"], "Most mammals are viviparous."),
    ("What is ovovivipary?", "eggs are kept inside the mother and hatch there; the young are born alive", ["eggs are laid in a nest", "the embryo is fed through a placenta", "the eggs are fertilised outside the body"], "Some sharks and snakes are ovoviviparous: the embryo feeds on the yolk."),
    ("A chicken lays eggs with hard shells that hatch in a nest. This is …", "ovipary", ["vivipary", "ovovivipary", "external fertilisation"], "The egg develops outside the mother's body."),
    ("A dog gives birth to puppies that were fed through a placenta. This is …", "vivipary", ["ovipary", "ovovivipary", "external development"], "The placenta passes food and oxygen to the embryos."),
    ("Some sharks keep their eggs inside the body until they hatch. This is …", "ovovivipary", ["vivipary", "ovipary", "external fertilisation"], "The young feed on the yolk and are born alive."),
    ("What is an amniotic egg?", "an egg with a shell and membranes (such as the amnion) that keep the embryo moist on land", ["a jelly-covered egg laid in water", "an egg without any yolk", "an egg that is fertilised outside the body"], "Reptiles and birds lay amniotic eggs."),
    ("What does the amnion do?", "it surrounds the embryo with fluid that protects it from drying out and from shocks", ["it stores food for the embryo", "it collects waste", "it exchanges gases through the shell"], "The amniotic fluid acts as a cushion and keeps the embryo moist."),
    ("What does the yolk sac do?", "it stores food for the developing embryo", ["it stores wastes", "it lets air in", "it makes the shell"], "The yolk is rich in protein and fat."),
    ("What does the allantois do in a bird's egg?", "it stores wastes and helps with gaseous exchange", ["it stores food", "it holds the amniotic fluid", "it hardens the shell"], "The allantois also carries blood vessels close to the shell."),
    ("What does the chorion do in a bird's egg?", "it surrounds all the other membranes and allows gaseous exchange through the shell", ["it stores the yolk", "it makes the albumen", "it forms the beak"], "Oxygen and carbon dioxide diffuse through the porous shell and chorion."),
    ("Why is the shell of a bird's egg porous?", "so that oxygen can diffuse in and carbon dioxide out", ["so that water can flow in", "so that the yolk can leave", "so that it breaks easily"], "The embryo needs oxygen for respiration."),
    ("What are precocial young?", "young that are well developed at birth, with eyes open, and can move and feed soon", ["young that are born blind and helpless", "young that hatch from eggs inside the mother", "young that never leave the nest"], "Ducklings, chicks and antelope calves are precocial."),
    ("What are altricial young?", "young that are born helpless, often blind and without feathers or fur, and need parental care", ["young that can run soon after birth", "young that feed themselves at once", "young that hatch in water"], "Kittens, puppies and many songbirds are altricial."),
    ("A springbok calf runs with the herd within hours of birth. It is …", "precocial", ["altricial", "ovoviviparous", "fertilised externally"], "Running soon after birth helps it escape predators."),
    ("Newly hatched sparrows are blind and naked and are fed by their parents. They are …", "altricial", ["precocial", "oviparous adults", "viviparous"], "Altricial young need a lot of parental care."),
    ("Why do animals that give a lot of parental care produce fewer young?", "each young has a better chance of survival, so fewer are needed", ["they cannot make more gametes", "their eggs are fertilised outside the body", "they live only a short time"], "Energy is put into caring for a few young rather than making many."),
    ("Which is an example of parental care?", "a bird incubating its eggs and feeding its chicks", ["a fish laying millions of eggs and leaving", "a frog laying eggs in a pond and swimming away", "a turtle burying eggs on a beach and leaving"], "Parental care includes incubation, feeding and protection."),
    ("A turtle lays about 100 eggs in the sand and leaves. What do you expect?", "only a few hatchlings survive to adulthood", ["all the eggs survive", "the eggs hatch inside the turtle", "the mother returns to feed them"], "Many eggs and no parental care mean high losses."),
    ("Why do bird embryos need a lot of yolk but mammal embryos do not?", "a mammal embryo gets food from the mother through the placenta", ["mammal embryos do not need food", "bird embryos grow inside the mother", "mammals lay larger eggs"], "The placenta replaces the need for a large yolk store."),
    ("Which vertebrates have amniotic eggs?", "reptiles, birds and mammals (the embryo is surrounded by an amnion)", ["fish and amphibians", "only fish", "only amphibians"], "The amnion was an adaptation to life on land."),
]

HUMAN = [
    ("Which site near Johannesburg is called the Cradle of Humankind?", "the Sterkfontein, Swartkrans and Kromdraai caves area", ["the Kruger National Park", "Table Mountain", "the Drakensberg"], "It is a World Heritage Site with many hominid fossils."),
    ("Where was the Taung Child fossil found?", "at Taung in the North West province", ["in the Sterkfontein Caves", "in Ethiopia", "at Border Cave"], "Raymond Dart described it in 1925."),
    ("Which species is the Taung Child?", "<i>Australopithecus africanus</i>", ["<i>Homo sapiens</i>", "<i>Homo naledi</i>", "<i>Australopithecus sediba</i>"], "It was the first early hominid fossil found in Africa."),
    ("Who described the Taung Child?", "Raymond Dart", ["Robert Broom", "Lee Berger", "Charles Darwin"], "Dart named <i>Australopithecus africanus</i> in 1925."),
    ("What is 'Mrs Ples'?", "a skull of <i>Australopithecus africanus</i> found at Sterkfontein", ["a skeleton of <i>Homo naledi</i>", "a skull of <i>Homo erectus</i> from Asia", "a stone tool"], "Robert Broom found Mrs Ples in 1947."),
    ("What is 'Little Foot'?", "an almost complete <i>Australopithecus</i> skeleton from the Sterkfontein Caves", ["a fossil footprint from Kenya", "a <i>Homo sapiens</i> skull", "a fossil chimpanzee"], "Ron Clarke's team took many years to remove it from the rock."),
    ("Which hominid was found in the Rising Star Cave system?", "<i>Homo naledi</i>", ["<i>Australopithecus africanus</i>", "<i>Homo erectus</i>", "<i>Paranthropus robustus</i>"], "Lee Berger's team described it in 2015."),
    ("Which species was found at Malapa in the Cradle of Humankind?", "<i>Australopithecus sediba</i>", ["<i>Homo naledi</i>", "<i>Ardipithecus</i>", "<i>Homo habilis</i>"], "It was found in 2008 by Matthew Berger, aged nine."),
    ("What does 'bipedal' mean?", "walking upright on two legs", ["walking on four legs", "climbing trees with long arms", "having a large brain"], "Bipedalism is a key feature of hominids."),
    ("Where is the foramen magnum in a bipedal hominid?", "further forward, under the skull", ["at the back of the skull", "on top of the skull", "in the jaw"], "The spinal cord enters the skull from below when the body is upright."),
    ("How does the pelvis of humans differ from that of African apes?", "it is short and wide (basin-shaped)", ["it is long and narrow", "it is the same", "it is missing"], "A short, wide pelvis supports the body when walking upright."),
    ("How does the spine of humans differ from that of apes?", "it is S-shaped", ["it is C-shaped", "it is straight", "it has no vertebrae in the neck"], "The S-shaped spine keeps the body balanced over the legs."),
    ("Compared with apes, humans have …", "a larger brain and a flatter face", ["a smaller brain and a longer snout", "larger canine teeth", "a more prominent brow ridge"], "Brain size increased and the face became flatter in human evolution."),
    ("Which feature do humans share with other primates?", "eyes in front of the head giving stereoscopic (3D) vision", ["a tail", "hooves", "eyes on the sides of the head"], "Forward-facing eyes help judge distance."),
    ("Which feature do humans share with other primates?", "opposable thumbs that can grip", ["claws instead of nails", "a single toe on each foot", "no collarbone"], "Opposable thumbs give a precise grip."),
    ("What does the 'Out of Africa' hypothesis state?", "modern humans evolved in Africa and later spread to other continents", ["humans evolved separately on each continent", "humans evolved in Asia and moved to Africa", "humans did not evolve"], "Fossils and genetic evidence support an African origin."),
    ("Which kind of evidence supports the Out of Africa hypothesis?", "mitochondrial DNA shows the greatest diversity in African populations", ["all fossils are found in Europe", "humans in Africa have no DNA", "stone tools are found only in Asia"], "More genetic diversity means a population has existed longer."),
    ("Why is mitochondrial DNA useful in tracing human ancestry?", "it is inherited only from the mother and changes slowly", ["it is inherited only from the father", "it changes every generation", "it is found only in fossils"], "It can be traced back along the female line."),
    ("Which genus is the oldest of these?", "<i>Ardipithecus</i>", ["<i>Australopithecus</i>", "<i>Homo</i>", "<i>Homo sapiens</i>"], "Order: <i>Ardipithecus</i> → <i>Australopithecus</i> → <i>Homo</i>."),
    ("Which species was the first to leave Africa, according to the fossil record?", "<i>Homo erectus</i>", ["<i>Homo sapiens</i>", "<i>Australopithecus africanus</i>", "<i>Homo naledi</i>"], "Fossils of <i>Homo erectus</i> are found in Africa, Asia and Europe."),
    ("Which species is modern humans?", "<i>Homo sapiens</i>", ["<i>Homo erectus</i>", "<i>Homo habilis</i>", "<i>Australopithecus sediba</i>"], "We are the only surviving species of the genus <i>Homo</i>."),
    ("Why are stone tools evidence in human evolution?", "they show the skills and behaviour of early humans", ["they show the age of the Earth", "they contain DNA", "they show how fast animals ran"], "More complex tools appear later in the record."),
    ("What does the fossil footprint trail at Laetoli in Tanzania show?", "hominids walked upright about 3.7 million years ago", ["early humans used fire", "hominids could swim", "dinosaurs lived with humans"], "The footprints show a bipedal gait."),
    ("Humans have smaller canine teeth than apes. Why is this linked to evolution?", "a change in diet and less use of teeth for fighting", ["humans eat only meat", "apes do not eat", "small teeth are needed for walking"], "Hominids' diets and behaviour changed."),
    ("Which statement about humans and chimpanzees is correct?", "they share a common ancestor that lived millions of years ago", ["humans evolved from chimpanzees", "chimpanzees evolved from humans", "they are not related"], "They are separate branches of the same family tree."),
    ("What is a hominid?", "a member of the group that includes humans and their extinct bipedal ancestors", ["any primate with a tail", "a modern ape", "a kind of stone tool"], "Hominids include <i>Australopithecus</i> and <i>Homo</i>."),
    ("Why is Border Cave in KwaZulu-Natal important?", "it has evidence of early <i>Homo sapiens</i> and their tools", ["it has dinosaur fossils", "it is where gold was first found", "it is the oldest rock on Earth"], "Remains and artefacts there are among the oldest of modern humans."),
    ("Which change happened to the jaw during human evolution?", "it became smaller and less protruding", ["it became longer and larger", "it disappeared", "it gained more teeth"], "The face became flatter and the jaw smaller."),
]

PLANT = [
    ("What is a tropism?", "a growth movement of a plant in response to a stimulus from one direction", ["a quick movement of an animal", "the closing of flowers at night", "a type of root"], "Plants grow towards or away from the stimulus."),
    ("A shoot grows towards light. This is …", "positive phototropism", ["negative phototropism", "positive geotropism", "negative geotropism"], "Phototropism is a response to light."),
    ("Roots grow downwards. This is …", "positive geotropism (gravitropism)", ["negative geotropism", "positive phototropism", "hydrotropism"], "Roots grow in the direction of gravity."),
    ("Shoots grow upwards, away from gravity. This is …", "negative geotropism", ["positive geotropism", "positive phototropism", "thigmotropism"], "Shoots grow against gravity."),
    ("Which hormone causes phototropism?", "auxin", ["gibberellin", "abscisic acid", "insulin"], "Auxin moves to the shaded side of the shoot."),
    ("Light shines on a shoot from the left. Where does auxin collect?", "on the right (shaded) side", ["on the left (lit) side", "at the root tip", "evenly on both sides"], "Auxin moves away from the light."),
    ("Why does a shoot bend towards light?", "cells on the shaded side elongate more because of more auxin", ["cells on the lit side grow faster", "the shoot shrinks on the shaded side", "light pulls the shoot"], "Uneven growth bends the shoot."),
    ("In roots, a high concentration of auxin …", "slows growth, so the root bends downwards", ["speeds up growth", "has no effect", "makes the root grow upwards"], "Roots are more sensitive to auxin than shoots."),
    ("What is apical dominance?", "the main shoot tip makes auxin that stops side buds from growing", ["side buds grow faster than the tip", "roots grow faster than shoots", "leaves fall off in autumn"], "Removing the tip lets side branches grow."),
    ("A gardener cuts the top off a plant to make it bushy. Why does this work?", "removing the tip removes the source of auxin, so side buds grow", ["it adds more auxin", "it kills the roots", "it makes the plant flower"], "This removes apical dominance."),
    ("Which hormone stimulates seed germination and stem elongation?", "gibberellin", ["abscisic acid", "ethylene", "adrenaline"], "Gibberellins break dormancy and make stems longer."),
    ("Which hormone causes stomata to close in dry conditions?", "abscisic acid", ["auxin", "gibberellin", "thyroxin"], "It reduces water loss during drought."),
    ("Which hormone keeps seeds and buds dormant?", "abscisic acid", ["gibberellin", "auxin", "cytokinin only in roots"], "It prevents germination at the wrong time."),
    ("How are auxins used in agriculture?", "as weedkillers and rooting powder for cuttings", ["to make seeds dormant", "to close stomata", "to stop fruit from ripening"], "Synthetic auxins kill broad-leaved weeds and help cuttings grow roots."),
    ("How are gibberellins used in agriculture?", "to produce larger, seedless grapes and to malt barley", ["as rooting powder", "to kill weeds", "to keep seeds dormant"], "They increase fruit size and speed up germination."),
    ("What does a thorn on an acacia tree do?", "it is a physical defence against grazing animals", ["it makes food by photosynthesis", "it absorbs water", "it attracts pollinators"], "Plants defend themselves physically and chemically."),
    ("Which is a chemical defence of a plant?", "making bitter or poisonous substances such as tannins", ["growing thorns", "having a thick bark", "having hairs on leaves"], "Chemicals make plants unpleasant or toxic to eat."),
    ("Some plants have stinging hairs. What kind of defence is this?", "a physical (mechanical) defence", ["a chemical defence only", "a type of tropism", "a way to absorb water"], "Hairs and spines are physical barriers."),
    ("Why do some acacias produce more tannin when giraffes browse them?", "tannins make the leaves bitter, so animals eat less", ["tannins attract more giraffes", "tannins help photosynthesis", "tannins are a food reserve"], "It is a chemical defence that is switched on by damage."),
    ("A seedling in a box with one hole grows towards the hole. Which factor is tested?", "light (phototropism)", ["gravity", "water", "touch"], "The shoot grows towards the light coming in."),
    ("In an experiment on phototropism, what is the control?", "an identical seedling with light from all sides (or from above)", ["a seedling with no water", "a dead seedling", "a seedling in the dark only, with no other plants"], "The control is the same but without one-sided light."),
    ("A seedling is placed on its side. After a few days the root bends down and the shoot up. Why?", "auxin collects on the lower side; it speeds up shoot growth but slows root growth", ["the light came from below", "the seedling was watered from above", "auxin collects on the upper side"], "Gravity makes auxin move to the lower side."),
    ("Tendrils of a pea plant coil around a stick. This response to touch is called …", "thigmotropism", ["phototropism", "geotropism", "hydrotropism"], "Tendrils respond to contact."),
    ("Why is it useful for roots to show positive geotropism?", "they grow down into the soil to anchor the plant and find water", ["they reach sunlight", "they attract pollinators", "they make seeds"], "Roots need water and minerals and must anchor the plant."),
]

MINE = [
    ("Where is most of South Africa's gold found?", "in the Witwatersrand Basin", ["in the Karoo", "along the Wild Coast", "in the Kalahari Desert"], "Gold was discovered on the Witwatersrand in 1886."),
    ("In which kind of rock is Witwatersrand gold found?", "conglomerate (reef) in sedimentary layers", ["granite", "basalt lava", "limestone caves"], "The gold-bearing conglomerate layers are called reefs."),
    ("Why must South African gold mines be very deep?", "the gold-bearing reefs slope down to depths of several kilometres", ["gold is only found in the mantle", "it is cooler deep down", "deep mines are cheaper"], "Some mines are more than 3 km deep."),
    ("What is an ore?", "a rock from which a metal can be extracted at a profit", ["any rock with metal in it", "pure metal found in the ground", "a type of fossil fuel"], "Whether a rock is an ore depends on price and grade."),
    ("Which steps are used to get gold from ore, in order?", "crushing and milling, then leaching with cyanide, then recovery of gold", ["smelting, then crushing, then cyanide", "leaching, then mining, then crushing", "electrolysis, then crushing, then smelting"], "The ore is ground fine so that the cyanide can reach the gold."),
    ("Why is cyanide used in gold extraction?", "it forms a soluble complex with gold, so gold dissolves out of the ore", ["it makes gold magnetic", "it melts the rock", "it turns gold into a gas"], "Gold dissolves as [Au(CN)₂]⁻ in the presence of oxygen."),
    ("How is gold recovered from the cyanide solution?", "by adding zinc (or using activated carbon), which displaces the gold", ["by boiling off the gold", "by adding more cyanide", "by freezing the solution"], "Zinc is more reactive and displaces gold from solution."),
    ("In the reaction 2[Au(CN)₂]⁻ + Zn → 2Au + [Zn(CN)₄]²⁻, what is oxidised?", "zinc", ["gold", "cyanide", "nothing"], "Zinc loses electrons to become Zn²⁺."),
    ("What are mine dumps?", "large heaps of waste rock and tailings left after extraction", ["piles of pure gold", "underground water stores", "storage tanks for cyanide"], "The dumps around Johannesburg are mine waste."),
    ("What is acid mine drainage?", "acidic water containing heavy metals flowing from old mines", ["clean rainwater collected in mines", "water used to cool the miners", "a type of fertiliser"], "Pyrite reacts with water and air to form sulfuric acid."),
    ("Which mineral reacts with air and water to cause acid mine drainage?", "pyrite (iron sulfide)", ["quartz", "gold", "calcite"], "Oxidised pyrite forms sulfuric acid."),
    ("Name one effect of acid mine drainage.", "it pollutes rivers and kills fish and plants", ["it makes soil more fertile", "it cleans river water", "it raises the price of gold"], "The acid and dissolved metals harm living things."),
    ("How can acid mine drainage be treated?", "by neutralising it with lime (calcium hydroxide)", ["by adding more acid", "by pumping it into dams without treatment", "by adding cyanide"], "Lime raises the pH and makes metals settle out."),
    ("Why is dust from mine dumps a health problem?", "fine dust can damage lungs and may contain toxic or radioactive metals", ["the dust is pure gold", "the dust has too much oxygen", "the dust makes rain more acidic only"], "Some dumps contain uranium and heavy metals."),
    ("Which is a positive effect of mining on South Africa's economy?", "it provides jobs and export income", ["it always improves the environment", "it reduces water use", "it removes the need for roads"], "Mining is a major employer and earns foreign exchange."),
    ("Which is a negative effect of mining on the environment?", "loss of habitat and pollution of water and air", ["more biodiversity", "cleaner rivers", "more rainfall"], "Mining disturbs land and can pollute water."),
    ("What is rehabilitation of a mine site?", "restoring the land after mining, for example by covering dumps with soil and plants", ["opening a new mine nearby", "digging the mine deeper", "selling the waste rock"], "Plants stop dust and erosion."),
    ("What is the lithosphere?", "the crust and the upper part of the mantle", ["the layer of air around the Earth", "all the water on Earth", "only the inner core"], "Minerals are mined from the lithosphere."),
    ("Which metal is extracted from bauxite?", "aluminium", ["iron", "gold", "copper"], "Bauxite is aluminium oxide ore."),
    ("Which metal is extracted from haematite?", "iron", ["aluminium", "platinum", "zinc"], "Haematite is iron(III) oxide, Fe₂O₃."),
    ("South Africa has the world's largest reserves of which metals?", "the platinum group metals", ["copper and tin", "lead and mercury", "lithium and cobalt"], "They are found in the Bushveld Complex."),
    ("In which kind of mining is ore removed from a large pit at the surface?", "open-cast (open-pit) mining", ["deep-level mining", "shaft mining", "offshore drilling"], "Open-cast mining is used when the ore is near the surface."),
    ("In which kind of mining are shafts and tunnels dug to reach the ore?", "underground (shaft) mining", ["open-cast mining", "strip mining", "dredging"], "Gold on the Witwatersrand is mined underground."),
    ("Why is iron extracted in a blast furnace with carbon (coke)?", "carbon is more reactive than iron and removes oxygen from the iron oxide", ["carbon is less reactive than iron", "iron needs no reduction", "carbon makes the iron magnetic"], "Fe₂O₃ is reduced to Fe by carbon monoxide."),
]


def gold_grade(R):
    """grams of gold per tonne of ore"""
    def f():
        g = R.choice((3, 4, 5, 6, 8, 10))
        t = R.choice((200, 500, 800, 1000, 1500, 2000, 2500, 5000))
        if R.random() < 0.5:
            m = g * t
            return nq("An ore contains %d g of gold per tonne. How much gold can be extracted from %d tonnes of ore?" % (g, t),
                      m / 1000, [m, g * t / 100, t / g], " kg", "Mass = %d g/t × %d t = %d g = <b>%g kg</b>." % (g, t, m, m / 1000))
        m = g * t
        return nq("A mine extracts %g kg of gold from %d tonnes of ore. What is the grade of the ore?" % (m / 1000, t),
                  g, [m / t / 1000, t / m, m / t * 10], " g/t", "Grade = %d g ÷ %d t = <b>%d g per tonne</b>." % (m, t, g))
    return f

SKEL = [
    ("Which animal has an exoskeleton?", "a locust", ["a frog", "an earthworm", "a dog"], "Insects have a hard outer skeleton made of chitin."),
    ("Which animal has a hydrostatic skeleton?", "an earthworm", ["a beetle", "a lizard", "a cow"], "Fluid under pressure inside the body gives support."),
    ("Which animal has an endoskeleton?", "a lizard", ["a crab", "a spider", "an earthworm"], "Vertebrates have an internal skeleton of bone and cartilage."),
    ("What is a disadvantage of an exoskeleton?", "the animal must moult to grow and is soft for a while", ["it cannot protect the body", "it is made of living bone", "it grows with the animal"], "The exoskeleton cannot grow, so it is shed."),
    ("What is an advantage of an endoskeleton?", "it grows with the animal and can support a large body", ["it never breaks", "it protects every organ fully", "it is shed often"], "Bone is living tissue that grows."),
    ("Exoskeletons are made of …", "chitin", ["bone", "cartilage", "keratin only"], "Chitin is a tough polysaccharide."),
    ("Which part of the skeleton belongs to the axial skeleton?", "the vertebral column", ["the femur", "the scapula", "the pelvic girdle"], "The axial skeleton is the skull, vertebral column, ribs and sternum."),
    ("Which part of the skeleton belongs to the appendicular skeleton?", "the humerus", ["the skull", "the sternum", "the ribs"], "The appendicular skeleton is the limbs and the girdles."),
    ("Which bone is in the upper arm?", "the humerus", ["the femur", "the tibia", "the radius"], "The radius and ulna are in the forearm."),
    ("Which bone is in the thigh?", "the femur", ["the humerus", "the fibula", "the ulna"], "The femur is the longest bone in the body."),
    ("Which bones protect the heart and lungs?", "the ribs and sternum", ["the pelvis", "the skull", "the scapula"], "The rib cage surrounds the chest."),
    ("Where are red blood cells made?", "in the red bone marrow", ["in the cartilage", "in the tendons", "in the joints"], "Red marrow in spongy bone makes blood cells."),
    ("Which mineral makes bone hard?", "calcium phosphate", ["sodium chloride", "iron oxide", "potassium nitrate"], "Calcium salts make bone hard; collagen makes it slightly flexible."),
    ("What is cartilage?", "a firm but flexible connective tissue, found at the ends of bones and in the ear and nose", ["a type of muscle", "a nerve", "a hard mineral without cells"], "Cartilage cushions joints."),
    ("What joins bone to bone at a joint?", "a ligament", ["a tendon", "cartilage", "a muscle"], "Ligaments are strong and slightly elastic."),
    ("What does synovial fluid do?", "it lubricates the joint and reduces friction", ["it makes blood cells", "it joins muscle to bone", "it makes the bone hard"], "It is found in freely movable joints."),
    ("Which type of joint is found in the skull?", "an immovable (fixed) joint, or suture", ["a ball-and-socket joint", "a hinge joint", "a pivot joint"], "The skull bones are joined by sutures."),
    ("Which joint lets you turn your head from side to side?", "a pivot joint", ["a hinge joint", "a fixed joint", "a ball-and-socket joint"], "The atlas turns on the axis vertebra."),
    ("Which joint is found at the elbow and knee?", "a hinge joint", ["a ball-and-socket joint", "a pivot joint", "a fixed joint"], "It allows movement in one plane only."),
    ("Which joint is found at the hip?", "a ball-and-socket joint", ["a hinge joint", "a pivot joint", "a gliding joint"], "It allows movement in all directions."),
    ("What is osteoporosis?", "a disease in which bones lose minerals and become weak and break easily", ["inflammation of a joint", "a broken ligament", "a muscle cramp"], "It is common in older people; calcium and exercise help prevent it."),
    ("What is arthritis?", "inflammation of the joints, making them painful and stiff", ["weak bones that break easily", "a lack of red blood cells", "a torn tendon"], "Cartilage in the joint may wear away."),
    ("What is rickets?", "soft, bent bones in children, caused by too little vitamin D or calcium", ["a disease of the lungs", "a type of arthritis in old age", "an infection of the muscles"], "Vitamin D is needed to absorb calcium."),
    ("Why do muscles work in antagonistic pairs?", "muscles can only pull (contract), so another muscle is needed to move the bone back", ["muscles can push and pull", "one muscle is always resting", "bones move by themselves"], "For example the biceps and triceps."),
    ("When the biceps contracts, what happens to the arm?", "it bends at the elbow", ["it straightens", "it rotates at the shoulder", "nothing happens"], "The triceps relaxes at the same time."),
    ("Which type of muscle is attached to the skeleton?", "skeletal (striated) muscle", ["smooth muscle", "cardiac muscle", "involuntary muscle only"], "Skeletal muscle is under voluntary control."),
    ("Which type of muscle is found in the walls of the intestine?", "smooth muscle", ["skeletal muscle", "cardiac muscle", "striated voluntary muscle"], "Smooth muscle is involuntary."),
    ("Why do bones of older people break more easily?", "they lose calcium and become less dense", ["they become more flexible", "they have more cartilage", "they contain more collagen"], "Bone density decreases with age."),
]

PHYLA = [("a sponge", "Porifera"), ("a jellyfish", "Cnidaria"), ("a sea anemone", "Cnidaria"), ("a bluebottle", "Cnidaria"), ("a coral polyp", "Cnidaria"),
         ("a tapeworm", "Platyhelminthes"), ("a planarian", "Platyhelminthes"), ("a liver fluke", "Platyhelminthes"),
         ("an earthworm", "Annelida"), ("a leech", "Annelida"), ("a bristleworm", "Annelida"),
         ("a locust", "Arthropoda"), ("a spider", "Arthropoda"), ("a crab", "Arthropoda"), ("a scorpion", "Arthropoda"), ("a millipede", "Arthropoda"),
         ("a shark", "Chordata"), ("a frog", "Chordata"), ("a lizard", "Chordata"), ("a sunbird", "Chordata"), ("a human", "Chordata")]
PFEAT = [("Porifera", "no symmetry and no true tissues; the body has many pores"), ("Cnidaria", "radial symmetry, two germ layers and stinging cells"),
         ("Platyhelminthes", "bilateral symmetry, three germ layers, a flat body and no coelom"), ("Annelida", "a segmented body with a true coelom"),
         ("Arthropoda", "jointed legs and an exoskeleton made of chitin"), ("Chordata", "a notochord and a dorsal nerve cord at some stage of life")]
BODY = [
    ("What is radial symmetry?", "the body can be cut into similar halves along many planes through the centre", ["the body can be cut into two mirror halves along one plane only", "the body has no symmetry", "the body has a head and a tail"], "Cnidaria such as jellyfish are radially symmetrical."),
    ("What is bilateral symmetry?", "the body can be divided into two mirror-image halves along one plane only", ["the body can be cut into halves along many planes", "the body has no shape", "the body is round like a ball"], "Most animals, including humans, are bilaterally symmetrical."),
    ("Why is bilateral symmetry linked to cephalisation?", "animals moving forward have a head end where sense organs and nerve cells collect", ["it lets animals stay attached to rocks", "it means there is no brain", "it stops animals from moving"], "Cephalisation is the development of a head."),
    ("Diploblastic animals have …", "two germ layers: ectoderm and endoderm", ["three germ layers", "no germ layers", "four germ layers"], "Cnidaria are diploblastic."),
    ("Triploblastic animals have …", "three germ layers: ectoderm, mesoderm and endoderm", ["two germ layers", "only one germ layer", "no germ layers"], "The mesoderm forms muscles and organs."),
    ("What is a coelom?", "a fluid-filled body cavity inside the mesoderm", ["the hole that forms the mouth", "the hard outer covering", "a group of nerve cells"], "The coelom gives room for organs to develop and move."),
    ("Which phylum is triploblastic but has no coelom (acoelomate)?", "Platyhelminthes", ["Annelida", "Chordata", "Arthropoda"], "Flatworms have solid bodies without a cavity."),
    ("What is the advantage of a through-gut (mouth and anus)?", "food moves in one direction, so digestion and absorption can happen at the same time in different parts", ["food can leave through the mouth", "no digestion is needed", "it makes the animal radially symmetrical"], "A blind sac gut has only one opening."),
    ("Which phylum has a blind sac gut (one opening)?", "Cnidaria", ["Annelida", "Arthropoda", "Chordata"], "Food enters and waste leaves through the same opening."),
    ("Why are insects successful on land?", "they have an exoskeleton that prevents water loss and jointed legs for movement", ["they have moist skin", "they breathe with gills", "they have a hydrostatic skeleton"], "The waterproof exoskeleton reduces drying out."),
    ("Why is a flat body an advantage for a flatworm?", "it gives a large surface area for gaseous exchange by diffusion", ["it lets it run faster", "it stores more food", "it protects it from predators"], "Flatworms have no lungs or gills."),
    ("Which phylum includes the largest number of species?", "Arthropoda", ["Porifera", "Cnidaria", "Annelida"], "Insects alone have over a million known species."),
    ("How do earthworms help farmers?", "they make burrows that aerate and drain the soil and they mix organic matter into it", ["they eat crops", "they spread disease", "they make the soil acidic"], "Earthworms improve soil fertility."),
    ("Why are coral reefs important?", "they support a very high biodiversity of marine life", ["they produce most of the world's fresh water", "they stop the tides", "they are made of plants"], "Corals are Cnidaria that build limestone skeletons."),
]
PGROUP = [("moss", "bryophytes"), ("liverwort", "bryophytes"), ("fern", "pteridophytes"), ("tree fern", "pteridophytes"), ("horsetail", "pteridophytes"),
          ("pine tree", "gymnosperms"), ("cycad", "gymnosperms"), ("yellowwood tree", "gymnosperms"), ("welwitschia", "gymnosperms"),
          ("protea", "angiosperms"), ("maize plant", "angiosperms"), ("rose bush", "angiosperms"), ("sunflower", "angiosperms"), ("baobab tree", "angiosperms")]
PFEAT2 = [("bryophytes", "no vascular tissue, and they need water for fertilisation"), ("pteridophytes", "vascular tissue, but they reproduce by spores"),
          ("gymnosperms", "seeds that are not enclosed in fruits, usually in cones"), ("angiosperms", "flowers, and seeds enclosed in fruits")]
LAND = [
    ("Why are mosses small and found in damp places?", "they have no vascular tissue and need water for fertilisation", ["they have very deep roots", "they make seeds in cones", "they grow only in deserts"], "Water must carry the sperm to the egg."),
    ("What is the advantage of vascular tissue?", "water and food can be carried long distances, so plants can grow tall", ["it lets plants live only in water", "it makes seeds", "it attracts pollinators"], "Xylem and phloem support and transport."),
    ("What does the cuticle on a leaf do?", "it is a waxy layer that reduces water loss", ["it absorbs water from the air", "it makes food", "it carries water up the stem"], "It is an adaptation to life on land."),
    ("What is alternation of generations?", "a life cycle with a haploid gametophyte stage and a diploid sporophyte stage", ["a plant that changes colour each season", "two plants that live together", "a plant that reproduces only asexually"], "In mosses the gametophyte is dominant; in ferns and seed plants the sporophyte is."),
    ("In which group is the gametophyte the dominant generation?", "bryophytes (mosses)", ["angiosperms", "gymnosperms", "pteridophytes"], "The green moss plant is the gametophyte."),
    ("Why are seeds an advantage over spores?", "a seed has an embryo, a food store and a protective coat", ["seeds are smaller", "seeds need water to fertilise", "seeds have no food store"], "Seeds can stay dormant until conditions are good."),
    ("Why is pollen an advantage for seed plants on land?", "the male gametes can reach the egg without water", ["pollen makes the plant tall", "pollen stores water", "pollen carries out photosynthesis"], "Pollen is carried by wind or animals."),
    ("Which part of a flower becomes the fruit?", "the ovary", ["the ovule", "the anther", "the petal"], "The ovule becomes the seed."),
    ("Which part of a flower becomes the seed?", "the ovule", ["the ovary", "the stigma", "the sepal"], "The ovary becomes the fruit."),
    ("Which kind of flower is pollinated by wind?", "small, dull flowers with feathery stigmas and lots of light pollen", ["large, bright flowers with nectar", "flowers with a strong scent", "flowers with sticky pollen"], "Grasses and maize are wind-pollinated."),
    ("Why are plants important to humans?", "they provide food, oxygen, medicines, building materials and fuel", ["they use up all the oxygen", "they cause soil erosion", "they have no economic value"], "Many medicines come from indigenous plants."),
    ("Why do sunbirds visit proteas?", "they drink nectar and carry pollen from flower to flower", ["they eat the seeds only", "they build nests in the flowers", "they eat the leaves"], "Birds are important pollinators of proteas."),
    ("Which plants have both seeds and vascular tissue but no flowers?", "gymnosperms", ["angiosperms", "bryophytes", "pteridophytes"], "Gymnosperms have naked seeds."),
    ("Which plant group produces spores but has vascular tissue?", "pteridophytes (ferns)", ["bryophytes", "gymnosperms", "angiosperms"], "Ferns have spores on the underside of their fronds."),
]

PLANT2 = [
    ("Where is auxin made in a shoot?", "in the growing tip (apex) of the shoot", ["in the roots only", "in the flowers", "in the seeds only"], "It moves down from the tip to the region of elongation."),
    ("What does auxin do to cells in a shoot?", "it makes them elongate (grow longer)", ["it makes them shrink", "it kills them", "it stops them from dividing forever"], "More auxin on one side makes that side grow faster."),
    ("A shoot tip is covered with a foil cap and lit from one side. What happens?", "the shoot grows straight up and does not bend", ["it bends towards the light", "it bends away from the light", "it stops growing at once"], "The tip detects the light; covered, it cannot respond."),
    ("A shoot tip is cut off and the shoot is lit from one side. What happens?", "it does not bend, because the source of auxin is removed", ["it bends sharply towards the light", "it bends away from the light", "it grows faster"], "Without the tip there is no auxin to move."),
    ("A seedling is placed on a slowly turning clinostat in the dark. How does it grow?", "straight, because gravity acts on all sides equally", ["it bends down", "it bends up", "it grows in a circle"], "The clinostat cancels the effect of one-sided gravity."),
    ("What is the stimulus in phototropism?", "light from one direction", ["gravity", "water", "touch"], "Photo- means light."),
    ("What is the stimulus in geotropism?", "gravity", ["light", "water", "chemicals"], "Geo- means earth."),
    ("Name a plant hormone that ripens fruit.", "ethylene", ["auxin", "abscisic acid", "insulin"], "Ethylene gas speeds up ripening; one ripe banana ripens others nearby."),
    ("Why are unripe fruits sometimes stored with a ripe banana?", "the banana gives off ethylene, which speeds up ripening", ["the banana makes them colder", "the banana absorbs water", "the banana kills bacteria"], "Ethylene is a gaseous plant hormone."),
    ("Which hormone helps barley seeds produce enzymes when they germinate?", "gibberellin", ["abscisic acid", "auxin", "ethylene"], "Gibberellin makes the aleurone layer release amylase."),
    ("Why is abscisic acid called a stress hormone?", "it is made when the plant is short of water and closes the stomata", ["it makes the plant grow fast", "it attracts insects", "it makes fruit ripen"], "It helps the plant survive drought."),
    ("Which hormone inhibits the growth of side buds?", "auxin from the shoot tip", ["gibberellin", "abscisic acid only in roots", "ethylene"], "This is apical dominance."),
    ("Rooting powder is used on cuttings. Which hormone does it contain?", "auxin", ["abscisic acid", "ethylene", "adrenalin"], "Auxin stimulates roots to form."),
    ("Why do selective weedkillers kill broad-leaved weeds but not grass?", "broad leaves absorb more synthetic auxin, which makes them grow out of control and die", ["grass has no cells", "weeds have no roots", "grass makes its own weedkiller"], "The weeds grow too fast and die."),
    ("What is the difference between a plant hormone and an animal hormone?", "plant hormones are made in many tissues and often act nearby; animal hormones come from glands and travel in the blood", ["plant hormones travel in blood", "animal hormones only act in plants", "there is no difference"], "Plants have no endocrine glands."),
    ("Why do plants need to respond to their environment?", "to get enough light, water and nutrients and to protect themselves", ["so that they can move from place to place", "to change their species", "to avoid photosynthesis"], "Responses improve survival."),
    ("Which plant has spines instead of leaves to reduce water loss and to defend itself?", "a cactus", ["a water lily", "a maize plant", "a fern"], "Spines protect it from animals and lose little water."),
    ("Why do some plants have a strong smell or bitter taste?", "the chemicals discourage animals from eating them", ["to attract all herbivores", "to absorb more light", "to store water"], "This is a chemical defence."),
    ("Some plants make chemicals that attract wasps when caterpillars eat them. Why?", "the wasps attack the caterpillars", ["the wasps pollinate the flowers", "the wasps eat the leaves", "the chemicals feed the plant"], "Plants can 'call for help' from predators of their pests."),
    ("Why does a thick bark help a tree?", "it protects the tree from insects, fire and drying out", ["it makes food by photosynthesis", "it absorbs water from the air", "it helps the tree to flower"], "Bark is a physical barrier."),
    ("Which describes the growth of a pollen tube down the style to the ovule?", "chemotropism (a response to chemicals)", ["phototropism", "geotropism", "thigmotropism"], "The tube grows towards chemicals from the ovule."),
    ("Roots grow towards water in the soil. This is …", "positive hydrotropism", ["negative hydrotropism", "phototropism", "thigmotropism"], "Hydro- means water."),
    ("Why do seeds of some fynbos plants germinate only after a fire?", "chemicals in the smoke break their dormancy, so they grow when there is less competition", ["fire adds water to the soil", "the seeds need the heat to photosynthesise", "fire kills all insects for ever"], "Smoke-stimulated germination is an adaptation to fire."),
    ("What happens to a shoot if auxin is placed on its left side only?", "it bends to the right", ["it bends to the left", "it stays straight", "it stops growing"], "The left side grows faster, so the shoot bends away from that side."),
    ("Why do shoots in the dark grow tall and pale?", "they use stored food to grow quickly upwards to reach light, and make no chlorophyll", ["they have too much light", "they make extra chlorophyll", "they stop growing"], "This is called etiolation."),
    ("What is the advantage of positive phototropism?", "leaves get more light for photosynthesis", ["roots find more water", "flowers are hidden from insects", "the plant loses less water"], "More light means more food."),
]

PLANT3 = [
    ("In a phototropism investigation, which is the independent variable?", "the direction of the light", ["the height of the shoot", "the type of soil used", "the time of day the results are recorded"], "The investigator changes the direction of light and observes the response."),
    ("In a phototropism investigation, which is the dependent variable?", "the direction or angle of bending of the shoots", ["the direction of the light", "the volume of water given", "the type of seed"], "It is what is measured."),
    ("Why are many seedlings used in a tropism investigation, not just one?", "to make the results more reliable", ["to make the seedlings grow faster", "so that the experiment is quicker", "because one seedling cannot bend"], "Repeating reduces the effect of chance differences."),
    ("Which factor must be kept the same in a phototropism investigation?", "the type of seedling, water and temperature", ["the direction of the light", "the result of the experiment", "the bending of the shoot"], "Controlled variables keep the test fair."),
    ("Bean seedlings in a box with a slit on one side all bend towards the slit. What can you conclude?", "the shoots show positive phototropism", ["the shoots show negative geotropism only", "light has no effect", "the roots show phototropism"], "They grow towards the light coming through the slit."),
    ("A germinating bean is pinned sideways. After two days the root bends down. What does this show?", "the root is positively geotropic", ["the root is negatively geotropic", "the root is phototropic", "the root is dead"], "Roots grow in the direction of gravity."),
    ("Why are tropism experiments with roots often done in the dark?", "to make sure the response is to gravity and not to light", ["roots grow faster in the dark only", "light kills roots", "auxin is destroyed in the dark"], "Removing light removes a second stimulus."),
    ("Why does an agar block that held a shoot tip make a decapitated shoot bend when placed on one side?", "auxin from the tip diffused into the agar and then into one side of the shoot", ["agar is a fertiliser", "agar blocks light", "agar contains gibberellin from the soil"], "This experiment showed that a chemical messenger is involved."),
    ("Which defence do grasses have against grazing animals?", "silica in their leaves, which makes them tough and wears down teeth", ["thorns on their roots", "stinging hairs", "a bitter nectar"], "Silica is a physical defence."),
    ("Why do some plants grow sharp thorns only on low branches?", "the low branches are the ones animals can reach", ["low branches get more light", "thorns help low branches photosynthesise", "thorns store water"], "Defence is put where it is most needed."),
    ("Which is a physical defence of a plant?", "a waxy cuticle and thick cell walls that stop fungi entering", ["producing nicotine", "producing tannins", "releasing a bad smell"], "Physical barriers stop pathogens and insects."),
    ("Which is a chemical defence of a plant?", "producing nicotine or caffeine that is toxic to insects", ["growing thorns", "having thick bark", "having hairs on the leaves"], "Many such chemicals are used as natural insecticides."),
    ("How do some plants defend themselves when they are wounded?", "they produce chemicals that slow down the growth of fungi and bacteria", ["they grow new flowers", "they stop photosynthesis forever", "they open all their stomata"], "Wounds are entry points for pathogens."),
    ("Why do farmers in South Africa plant crops that resist insects?", "the crops need less pesticide, which is cheaper and better for the environment", ["the crops grow without water", "the crops do not need sunlight", "the crops never flower"], "Resistant crops have strong natural defences."),
]
