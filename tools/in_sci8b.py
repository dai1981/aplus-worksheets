# -*- coding: utf-8 -*-
"""Class 8 Science (NCERT Curiosity, chapters 8–13): question makers and UNITS8b()."""
from uk_alsci import tq, nf, once_maker
from in_sci import pairs, _R, U, K
from in_sci6a import NS, LW, MT, PH, ES, odd_one, nq, _cap
import in_sci

# =================================================================== Chapter 8: elements, compounds and mixtures
SYM = [("hydrogen", "H"), ("helium", "He"), ("carbon", "C"), ("nitrogen", "N"), ("oxygen", "O"), ("sodium", "Na"), ("magnesium", "Mg"), ("aluminium", "Al"),
       ("sulphur", "S"), ("chlorine", "Cl"), ("potassium", "K"), ("calcium", "Ca"), ("iron", "Fe"), ("copper", "Cu"), ("zinc", "Zn"), ("silver", "Ag"),
       ("gold", "Au"), ("mercury", "Hg"), ("lead", "Pb"), ("tin", "Sn"), ("iodine", "I"), ("phosphorus", "P")]
ECM = {"an element": ["iron", "oxygen", "gold", "carbon (graphite)", "copper", "sulphur", "hydrogen", "aluminium", "mercury", "helium"],
       "a compound": ["water", "carbon dioxide", "common salt (sodium chloride)", "sugar", "baking soda", "rust (iron oxide)", "chalk (calcium carbonate)", "ammonia"],
       "a mixture": ["air", "sea water", "brass", "soil", "milk", "lemonade", "steel", "muddy water", "a salad"]}
FORM = [("water", "H₂O"), ("carbon dioxide", "CO₂"), ("common salt (sodium chloride)", "NaCl"), ("ammonia", "NH₃"), ("methane", "CH₄"), ("oxygen gas", "O₂"),
        ("iron oxide (rust)", "Fe₂O₃"), ("calcium carbonate (chalk)", "CaCO₃"), ("hydrochloric acid", "HCl"), ("glucose", "C₆H₁₂O₆")]
HOMO = {"a homogeneous mixture (the same throughout)": ["salt dissolved in water", "sugar solution", "air", "brass", "vinegar", "a soft drink without bubbles"],
        "a heterogeneous mixture (not the same throughout)": ["sand and water", "oil and water", "a salad", "soil", "iron filings and sulphur powder", "muddy water"]}
ECQ = [("What is an element?", "a pure substance made of only one kind of atom", ["a mixture of two metals", "a substance made of two kinds of atoms joined", "any liquid"], "Gold and oxygen are elements."),
       ("What is a compound?", "a pure substance made of two or more elements chemically joined in a fixed ratio", ["a mixture of elements in any ratio", "a single kind of atom", "a solution of salt"], "Water is H₂O."),
       ("What is a mixture?", "two or more substances mixed in any proportion without forming a new substance", ["one pure substance", "elements joined in a fixed ratio", "a single element"], "Air is a mixture."),
       ("How is a compound different from a mixture?", "a compound has a fixed composition and new properties; a mixture keeps the properties of its parts", ["they are the same", "a mixture always has a fixed ratio", "a compound can be separated by a magnet"], "Iron and sulphur mixed vs iron sulphide."),
       ("A mixture of iron filings and sulphur powder is heated strongly. What forms?", "iron sulphide, a new compound that is not attracted by a magnet", ["the same mixture", "pure iron", "pure sulphur"], "Before heating, a magnet can separate the iron."),
       ("How can iron be separated from a mixture of iron filings and sulphur (before heating)?", "with a magnet", ["by filtration", "by heating", "by adding water"], "The mixture keeps the properties of iron."),
       ("Why is water a compound and not a mixture?", "hydrogen and oxygen are chemically joined in a fixed ratio and water has different properties", ["it can be separated by filtering", "it has no fixed ratio", "it is an element"], "Water can be split only by chemical means such as electrolysis."),
       ("What is an atom?", "the smallest particle of an element", ["a mixture of elements", "a drop of water", "a kind of cell"], "Atoms join to form molecules."),
       ("What is a molecule?", "two or more atoms joined together", ["a single atom only", "a mixture of gases", "a type of cell"], "An oxygen molecule is O₂."),
       ("How many atoms are there in one molecule of water (H₂O)?", "three: two hydrogen and one oxygen", ["two", "one", "four"], "The subscript 2 belongs to hydrogen."),
       ("How many atoms are there in one molecule of carbon dioxide (CO₂)?", "three: one carbon and two oxygen", ["two", "one", "five"], "Carbon dioxide is a compound."),
       ("Which of these is a metal that is liquid at room temperature?", "mercury", ["bromine", "sodium", "iron"], "Its symbol is Hg."),
       ("Why is air called a mixture?", "its gases are not chemically joined and their amounts can vary", ["it is a single gas", "it has a fixed formula", "it is an element"], "It contains nitrogen, oxygen, argon, carbon dioxide and water vapour."),
       ("What does a chemical symbol represent?", "an element, usually by one or two letters", ["a mixture", "a compound only", "a colour"], "Fe comes from the Latin name 'ferrum'."),
       ("Why is the symbol of sodium Na?", "it comes from its Latin name 'natrium'", ["it is a mistake", "it stands for 'natural'", "it means 'salt'"], "Potassium is K from 'kalium'."),
       ("Is pure gold an element, a compound or a mixture?", "an element", ["a compound", "a mixture", "none of these"], "22-carat gold is a mixture (alloy) with copper or silver."),
       ("Why is brass a mixture?", "it is copper and zinc mixed in varying proportions", ["it is a single element", "it is a compound with a formula", "it is a gas"], "Alloys are mixtures."),
       ("Which of these is a property of a compound?", "it can be broken down only by chemical methods", ["its parts can be separated by hand", "it has no fixed composition", "it keeps the properties of its elements"], "Electrolysis splits water into hydrogen and oxygen."),
       ("What is a pure substance?", "a substance with only one kind of particle, such as an element or a compound", ["any mixture", "a solution", "air"], "Distilled water is pure; tap water is a mixture."),
       ("Why is tap water not a pure substance?", "it contains dissolved salts and gases", ["it contains only H₂O", "it is an element", "it has no particles"], "Distilled water is pure."),
       ("Which gas makes up about 78% of the air?", "nitrogen", ["oxygen", "carbon dioxide", "argon"], "Oxygen is about 21%."),
       ("What is formed when hydrogen burns in oxygen?", "water", ["carbon dioxide", "salt", "ammonia"], "Hydrogen and oxygen combine chemically."),
       ("What are alloys?", "mixtures of metals, or of a metal with a non-metal", ["pure elements", "compounds with formulas", "gases"], "Steel is iron with a little carbon.")]

# =================================================================== Chapter 9: solutes, solvents and solutions
SOLW = [("the solute", "the substance that dissolves, such as sugar in sugar solution"), ("the solvent", "the substance in which the solute dissolves, such as water"),
        ("a solution", "a uniform mixture of a solute dissolved in a solvent"), ("a saturated solution", "a solution in which no more solute can dissolve at that temperature"),
        ("an unsaturated solution", "a solution in which more solute can still dissolve"), ("solubility", "the greatest amount of a solute that dissolves in a fixed amount of solvent at a given temperature"),
        ("a concentrated solution", "a solution with a large amount of solute"), ("a dilute solution", "a solution with only a small amount of solute"),
        ("density", "the mass of a substance per unit volume"), ("a universal solvent", "a name for water, because it dissolves so many substances")]
SOLQ = [("What happens to the solubility of most solids in water when the water is heated?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "More sugar dissolves in hot water."),
        ("What happens to the amount of oxygen that can dissolve in water as the water gets warmer?", "it decreases", ["it increases", "it stays the same", "it doubles"], "This is why fish may suffer in warm, still water."),
        ("Why do fish need water with dissolved oxygen?", "they take in dissolved oxygen through their gills", ["they breathe air above the water only", "oxygen makes water heavier", "they do not need oxygen"], "Gases dissolve in water too."),
        ("How can you tell when a solution is saturated?", "extra solute added stays undissolved at the bottom", ["it changes colour", "it starts boiling", "it freezes"], "Heating may dissolve more."),
        ("What happens when a hot saturated solution of sugar is cooled?", "some sugar comes out as crystals", ["more sugar dissolves", "it turns into steam", "nothing happens"], "Solubility falls as it cools."),
        ("Why is water called a universal solvent?", "it dissolves a very large number of substances", ["it dissolves everything", "it dissolves nothing", "it is found everywhere"], "Oil and sand do not dissolve in water."),
        ("Which solvent is used to remove nail polish?", "acetone", ["water", "milk", "salt solution"], "Some substances dissolve in solvents other than water."),
        ("Which solvent can remove grease from hands when water alone cannot?", "kerosene or soapy water", ["pure water", "sugar solution", "vinegar alone"], "Grease does not dissolve in water."),
        ("Why does a sugar cube dissolve faster when crushed?", "the powder has a larger surface in contact with water", ["crushing makes it hotter", "powder is heavier", "crushing adds water"], "Stirring and hot water also speed it up."),
        ("Which factors make a solid dissolve faster?", "stirring, heating and breaking it into smaller pieces", ["cooling and leaving it still", "adding more solute", "using a bigger lump"], "They increase contact or particle speed."),
        ("What is the density of pure water?", "about 1 g/cm³", ["about 10 g/cm³", "about 0.1 g/cm³", "about 100 g/cm³"], "1 cm³ of water has a mass of about 1 g."),
        ("Why does oil float on water?", "oil is less dense than water", ["oil is denser than water", "oil dissolves in water", "oil is a solid"], "Less dense substances float on denser liquids."),
        ("Why does ice float on water?", "ice is less dense than liquid water", ["ice is denser than water", "ice is a gas", "ice dissolves at once"], "Water expands when it freezes."),
        ("Why does an iron nail sink in water while a big iron ship floats?", "the ship's hollow shape makes its average density less than water", ["iron floats when it is big", "the sea pulls the ship up", "the nail is magnetic"], "The ship pushes aside a lot of water."),
        ("Why is it easier to float in the Dead Sea than in a swimming pool?", "the very salty water is denser", ["the water is warmer", "there are no waves", "salt makes people lighter"], "Denser liquids give more upward push."),
        ("An egg sinks in plain water. What happens when a lot of salt is dissolved in the water?", "the egg floats", ["the egg sinks faster", "the egg dissolves", "nothing changes"], "Salt water is denser."),
        ("What is concentration of a solution?", "the amount of solute present in a given amount of solution", ["the colour of the solution", "the temperature of the solution", "the volume of the container"], "A sweeter drink is more concentrated."),
        ("How can a concentrated solution be made dilute?", "by adding more solvent", ["by adding more solute", "by heating it until it is dry", "by freezing it"], "Adding water dilutes juice."),
        ("Is air a solution?", "yes, it is a uniform mixture of gases", ["no, it is an element", "no, it is a compound", "no, it is a solid"], "Nitrogen is the solvent; oxygen and others are solutes."),
        ("Which solution has a solid dissolved in a liquid?", "salt water", ["air", "soda water", "brass"], "Soda water has a gas (carbon dioxide) in a liquid."),
        ("Why do bubbles come out when a bottle of soda is opened?", "the pressure falls and dissolved carbon dioxide escapes", ["the soda boils", "air enters", "sugar turns into gas"], "Gases dissolve more under high pressure."),
        ("Which of these does not dissolve in water?", "sand", ["salt", "sugar", "copper sulphate"], "Sand settles at the bottom.")]


def c_dens(k=None):
    R = _R[0]
    k = k or R.choice(["d", "m", "float"])
    if k == "float":
        sub, d = R.choice([("cooking oil", 0.92), ("ice", 0.92), ("dry wood", 0.6), ("iron", 7.9), ("aluminium", 2.7), ("cork", 0.25), ("glass", 2.5), ("rubber", 1.2), ("honey", 1.4), ("kerosene", 0.8), ("copper", 8.9), ("wax", 0.9)])
        a = "it floats" if d < 1 else "it sinks"
        return tq("The density of %s is about %s g/cm³. Water is about 1 g/cm³. What happens when %s is placed in water?" % (sub, nf(d), sub), a,
                  [x for x in ["it floats", "it sinks", "it dissolves completely", "it boils"] if x != a], "Less dense than water floats; denser than water sinks.")
    V = R.choice([2, 4, 5, 8, 10, 20, 25, 40, 50, 100])
    d = R.choice([0.5, 0.8, 1, 1.5, 2, 2.5, 3, 4, 7.5, 8])
    m = d * V
    if k == "d":
        return nq("A block has a mass of %s g and a volume of %s cm³. What is its density?" % (nf(m), V), d, [m * V, V / m, m - V, d * 10], "g/cm³", "Density = mass ÷ volume = %s ÷ %d = %s g/cm³." % (nf(m), V, nf(d)))
    return nq("A liquid has a density of %s g/cm³. What is the mass of %d cm³ of it?" % (nf(d), V), m, [V / d, d + V, m / 10, m * 10], "g", "Mass = density × volume = %s × %d = %s g." % (nf(d), V, nf(m)))


def c_conc(k=None):
    R = _R[0]
    s = R.choice([5, 10, 15, 20, 25, 30, 40, 50])
    w = R.choice([45, 90, 95, 100, 150, 180, 200, 230, 250])
    tot = s + w
    if (100 * s) % tot:
        return None
    pc = 100 * s // tot
    return nq("%d g of sugar is dissolved in %d g of water. What is the concentration of the solution as a percentage by mass?" % (s, w), pc, [100 * s / w, s, s + w, 100 - pc], "%",
              "Mass of solution = %d + %d = %d g; %d ÷ %d × 100 = %d%%." % (s, w, tot, s, tot, pc))


def c_satur(k=None):
    R = _R[0]
    sol = R.choice([("common salt", 36), ("potassium nitrate", 32), ("sugar", 200), ("copper sulphate", 32), ("alum", 12), ("baking soda", 10)])
    nm, lim = sol
    add = R.choice([lim - 6, lim - 2, lim + 4, lim + 10]) if lim > 10 else R.choice([lim - 4, lim + 3, lim + 6])
    if add <= 0:
        return None
    a = "an unsaturated solution, with no solid left" if add <= lim else "a saturated solution with %d g left undissolved" % (add - lim)
    w = [x for x in ["an unsaturated solution, with no solid left", "a saturated solution with %d g left undissolved" % abs(add - lim), "a saturated solution with %d g left undissolved" % add, "a solution with no %s in it at all" % nm] if x != a]
    return tq("At room temperature, about %d g of %s can dissolve in 100 g of water. A student stirs %d g of it into 100 g of water. What does she get?" % (lim, nm, add), a, w,
              "Up to %d g dissolves; %s." % (lim, "all of it dissolves" if add <= lim else "%d − %d = %d g is left at the bottom" % (add, lim, add - lim)))


SOLUP = [("sugar in water", "sugar", "water"), ("salt in water", "salt", "water"), ("carbon dioxide in soda water", "carbon dioxide", "water"),
         ("iodine in alcohol (tincture of iodine)", "iodine", "alcohol"), ("oxygen in air", "oxygen", "nitrogen"), ("copper sulphate in water", "copper sulphate", "water"),
         ("lemon juice and sugar in water (nimbu pani)", "lemon juice and sugar", "water"), ("zinc in copper (brass)", "zinc", "copper")]


def c_solup(k=None):
    R = _R[0]
    s, a, b_ = R.choice(SOLUP)
    if R.random() < 0.5:
        return tq("In the solution of %s, which is the solute?" % s, a, [b_] + R.sample(sorted({x for _, x, y in SOLUP if x != a} - {b_}), 2), "The solute dissolves in the solvent (%s)." % b_)
    return tq("In the solution of %s, which is the solvent?" % s, b_, [a] + R.sample(sorted({y for _, x, y in SOLUP if y != b_} | {"salt"} - {a}), 2), "The solvent (%s) dissolves the solute (%s)." % (b_, a))


# =================================================================== Chapter 10: light — mirrors and lenses
MIR = {"used as a concave mirror": ["the reflector of a torch", "a dentist's mirror", "a shaving mirror", "the reflector in a vehicle's headlight", "a solar cooker's reflector",
                                    "a make-up mirror that enlarges the face", "the inside of a shiny steel spoon", "a big telescope's main mirror"],
       "used as a convex mirror": ["a rear-view mirror in a car", "a mirror at a sharp turn on a hill road", "a security mirror in a shop", "the back of a shiny steel spoon",
                                   "a side mirror of a motorbike", "a mirror at a bus door for the driver", "a mirror at the exit of a car park"]}
LENS = {"a convex (converging) lens": ["a magnifying glass", "a camera", "the human eye", "spectacles for long-sightedness", "a slide projector", "a microscope", "a reading glass"],
        "a concave (diverging) lens": ["spectacles for short-sightedness (myopia)", "a door peephole", "a torch that spreads its beam widely", "a Galilean telescope's eyepiece", "some laser pointers that spread the beam", "some beam-spreading lamp covers"]}
REFR = {"an effect of refraction (bending of light)": ["a pencil looking bent in a glass of water", "a pond looking shallower than it really is", "a coin in a bowl seeming to rise when water is poured in",
                                                      "a lens forming an image", "a rainbow after rain", "a prism splitting white light into colours"],
        "an effect of reflection": ["seeing yourself in a plane mirror", "seeing the Moon at night", "a periscope letting you see over a wall", "a kaleidoscope's patterns",
                                    "a torch reflector sending out a beam", "the shine on a polished steel plate"]}
MLQ = [("What is a concave mirror?", "a curved mirror whose reflecting surface curves inwards like a cave", ["a flat mirror", "a mirror curved outwards", "a lens"], "It can form real and virtual images."),
       ("What is a convex mirror?", "a curved mirror whose reflecting surface bulges outwards", ["a mirror curved inwards", "a flat mirror", "a prism"], "It always forms smaller, upright images."),
       ("What kind of image does a convex mirror always form?", "upright, smaller and virtual", ["upside down and larger", "real and larger", "the same size and upside down"], "It gives a wide view."),
       ("What is a real image?", "an image that can be formed on a screen", ["an image seen only in a plane mirror", "an image that cannot be caught on a screen", "a drawing"], "Real images are upside down."),
       ("What is a virtual image?", "an image that cannot be formed on a screen", ["an image on a cinema screen", "an image made by a projector", "an upside-down image on paper"], "The image in a plane mirror is virtual."),
       ("Why does a concave mirror make a good shaving mirror?", "held close, it gives an enlarged upright image", ["it makes the face smaller", "it gives an upside-down image", "it absorbs light"], "Dentists use it for the same reason."),
       ("Why is a convex mirror used as a rear-view mirror?", "it gives a wide field of view and upright images", ["it makes cars look larger", "it forms upside-down images", "it is cheaper only"], "Objects look smaller than they are."),
       ("What does a convex lens do to parallel rays of sunlight?", "it brings them together at a point (converges them)", ["it spreads them apart", "it reflects them back", "it stops them completely"], "Paper at the focus can start to burn."),
       ("What does a concave lens do to parallel rays of light?", "it spreads them apart (diverges them)", ["it brings them together", "it reflects them", "it makes them coloured"], "It is thinner in the middle."),
       ("How can you tell a convex lens by touch?", "it is thicker in the middle than at the edges", ["it is thinner in the middle", "it is flat", "it has holes"], "A concave lens is thinner in the middle."),
       ("What image does a magnifying glass give of a small object held close to it?", "an enlarged, upright image", ["a smaller, upside-down image", "no image", "an image the same size"], "A magnifying glass is a convex lens."),
       ("What happens to the image of a distant tree seen through a convex lens on a screen?", "a small, upside-down, real image forms", ["an upright enlarged image forms", "no image forms", "the tree disappears"], "Cameras use this."),
       ("Which lens is used in a camera?", "a convex lens", ["a concave lens", "a plane glass", "no lens"], "It forms a real image on the sensor."),
       ("What is the focus of a concave mirror?", "the point where reflected parallel rays meet", ["the centre of the mirror's surface", "the edge of the mirror", "any point behind the mirror"], "Torches place the bulb near the focus."),
       ("Why is the bulb of a torch placed at the focus of a concave reflector?", "the reflected light comes out as a strong parallel beam", ["to make the bulb hot", "to make light spread everywhere", "to save the battery"], "Headlights work the same way."),
       ("What is dispersion of light?", "white light splitting into its seven colours", ["light bouncing off a mirror", "light passing straight through glass", "light becoming dim"], "A prism shows dispersion."),
       ("What are the colours of a rainbow, in order?", "violet, indigo, blue, green, yellow, orange, red (VIBGYOR)", ["red, white, blue", "black, white, grey", "only red and green"], "Raindrops act like tiny prisms."),
       ("Why does a straw look bent in a glass of water?", "light bends (refracts) as it passes from water to air", ["the straw really bends", "water reflects the straw", "the glass is curved"], "This bending is called refraction."),
       ("What happens to light when it passes from air into glass at an angle?", "it bends", ["it stops", "it changes into sound", "it becomes coloured always"], "Lenses work because of this bending."),
       ("Which type of mirror is used in solar cookers?", "a concave mirror", ["a convex mirror", "a plane mirror only", "no mirror"], "It concentrates sunlight."),
       ("A person cannot see distant objects clearly. Which lens is used in their spectacles?", "a concave lens", ["a convex lens", "a plane glass", "a prism"], "This defect is short-sightedness (myopia)."),
       ("A person cannot read a book held close. Which lens is used in their spectacles?", "a convex lens", ["a concave lens", "a plane glass", "a prism"], "This defect is long-sightedness (hypermetropia)."),
       ("Why should we never look at the Sun through a lens?", "the lens focuses sunlight and can burn the eye", ["it makes the Sun dim", "it is boring", "lenses block light"], "Never use lenses to look at the Sun."),
       ("Which part of the eye works like a convex lens?", "the eye lens", ["the iris", "the eyelid", "the eyebrow"], "It forms an image on the retina."),
       ("On which part of the eye is the image formed?", "the retina", ["the cornea", "the eyelid", "the iris"], "The optic nerve carries signals to the brain."),
       ("What kind of image does the eye lens form on the retina?", "real and upside down", ["virtual and upright", "enlarged and upright", "no image"], "The brain turns it the right way up."),
       ("What happens when white light passes through a glass prism?", "it splits into a band of seven colours called a spectrum", ["it turns black", "it stops", "it becomes one colour"], "Newton studied this."),
       ("How is a rainbow formed?", "raindrops refract and disperse sunlight into colours", ["clouds paint the sky", "the Sun gives off coloured rays only after rain", "the Moon reflects colours"], "The Sun must be behind you."),
       ("Which colour bends the most in a prism?", "violet", ["red", "green", "yellow"], "Red bends the least."),
       ("What is the focal length of a lens?", "the distance from the lens to its focus", ["the thickness of the lens", "the width of the lens", "the colour of the lens"], "Thicker convex lenses have shorter focal lengths."),
       ("Why does a swimming pool look shallower than it is?", "light from the bottom bends as it leaves the water", ["water reflects the bottom", "the pool shrinks", "our eyes are tired"], "This is refraction.")]
IMG = [("a plane mirror", "upright, the same size and virtual"), ("a convex mirror", "upright, smaller and virtual"), ("a concave mirror with the object very close", "upright, enlarged and virtual"),
       ("a concave mirror with a distant object", "upside down, smaller and real"), ("a convex lens with a distant object", "upside down, smaller and real"),
       ("a convex lens with the object very close", "upright, enlarged and virtual"), ("a concave lens", "upright, smaller and virtual")]

# =================================================================== Chapter 11: keeping time with the skies
CAL = [("a day", "the time the Earth takes to spin once on its axis"), ("a lunar month", "the time from one new moon to the next, about 29.5 days"),
       ("a solar year", "the time the Earth takes to go once round the Sun, about 365¼ days"), ("a lunar year", "twelve lunar months, about 354 days"),
       ("a leap year", "a year with 366 days, with 29 days in February"), ("an extra month (adhik maas)", "a month added about every three years to keep a lunisolar calendar in step with the seasons"),
       ("a lunisolar calendar", "a calendar whose months follow the Moon while its years are kept in step with the Sun"), ("a week", "seven days, a unit not based on the Sun or Moon directly")]
CALQ = [("Which motion gives us the length of a day?", "the Earth's rotation", ["the Moon's revolution", "the Earth's revolution", "the Sun's rotation"], "One rotation is about 24 hours."),
        ("Which motion gives us the length of a year?", "the Earth's revolution round the Sun", ["the Earth's rotation", "the Moon's rotation", "the Sun's revolution"], "It takes about 365¼ days."),
        ("Why does a leap year come every four years?", "the solar year is about 365¼ days, so the extra quarters add up to one day", ["the Moon slows down", "the Earth stops for a day", "to make February longer for fun"], "February gets 29 days."),
        ("Why is a lunar year shorter than a solar year?", "twelve lunar months make only about 354 days", ["the Moon moves faster each year", "the Sun is far away", "it is the same"], "The difference is about 11 days."),
        ("Why do festivals of a purely lunar calendar such as Eid move earlier each year in the Gregorian calendar?", "the lunar year is about 11 days shorter than the solar year", ["the Earth spins faster", "the Moon is changing size", "they are fixed dates"], "The Hijri calendar is purely lunar."),
        ("Why do many Indian calendars add an extra month every few years?", "to keep the lunar months in step with the seasons and the solar year", ["to make the year shorter", "because of eclipses", "to remove a festival"], "This extra month is called adhik maas."),
        ("What is the national calendar of India based on?", "the Saka era, adopted officially in 1957", ["the Gregorian calendar only", "a purely lunar calendar", "the Chinese calendar"], "Its first month is Chaitra."),
        ("On which date does Chaitra 1 of the Indian national calendar usually fall?", "22 March (21 March in a leap year)", ["1 January", "15 August", "2 October"], "It is near the spring equinox."),
        ("Why were the Moon's phases useful for ancient calendars?", "they repeat regularly and are easy to see", ["they never change", "they happen once a year", "they cannot be seen"], "A month comes from the Moon."),
        ("Which calendar is used in most of the world for daily life?", "the Gregorian calendar", ["the Saka calendar", "the Hijri calendar", "the Roman calendar of Julius Caesar"], "It adds leap years with a century rule."),
        ("Why is the year 1900 not a leap year in the Gregorian calendar?", "century years are leap years only if divisible by 400", ["the year 1900 is not divisible by 4", "it was a mistake", "all even years are leap years"], "2000 was a leap year."),
        ("How do farmers traditionally know when to sow certain crops?", "by the seasons, linked to the position of the Sun and the stars", ["by the day of the week", "by the phases of the Moon only", "by random choice"], "Calendars help plan farming."),
        ("What is a sidereal day?", "the time for the Earth to spin once relative to the distant stars, about 23 hours 56 minutes", ["exactly 25 hours", "one lunar month", "one year"], "A solar day is about 24 hours."),
        ("Which ancient Indian text describes the Indian lunisolar calendar?", "the Surya Siddhanta", ["the Charaka Samhita", "the Panchatantra", "the Arthashastra"], "It gives methods for astronomy."),
        ("Why do we see different constellations at different times of the year?", "the Earth's position in its orbit changes, so the night side faces different stars", ["the stars move away", "the Moon hides them", "the Sun changes colour"], "This helped ancient people track the year."),
        ("What is the tropical (solar) year?", "the time from one spring equinox to the next, about 365.24 days", ["exactly 360 days", "about 354 days", "about 29.5 days"], "Seasons repeat with this year."),
        ("Why is a month about 30 days long?", "it is based on the Moon's cycle of phases of about 29.5 days", ["it is based on the Earth's rotation", "it was chosen at random", "it is the time of a solar eclipse"], "The word 'month' comes from 'moon'."),
        ("How many days are there in a common (non-leap) year of the Gregorian calendar?", "365", ["366", "354", "360"], "A leap year has 366."),
        ("What is the purpose of the 'panchang' used in India?", "a traditional almanac giving dates, phases of the Moon and festival days", ["a train timetable", "a weather map", "a list of rivers"], "It uses the Sun and the Moon."),
        ("What is a tithi in the Indian calendar?", "a lunar day, based on the Moon's position relative to the Sun", ["a solar month", "a week", "a leap year"], "A lunar month has 30 tithis."),
        ("What is amavasya?", "the new moon day", ["the full moon day", "the longest day", "an eclipse"], "Purnima is the full moon."),
        ("What is purnima?", "the full moon day", ["the new moon day", "the shortest day", "a solar eclipse"], "Many festivals fall on purnima."),
        ("Why is Makar Sankranti celebrated on nearly the same date (14 or 15 January) each year?", "it is based on the Sun's apparent movement into Makara (Capricorn)", ["it follows the Moon", "it is chosen at random", "it is based on the stars of Orion"], "Most other festivals follow the Moon."),
        ("Who introduced the leap year rule of the Julian calendar?", "Julius Caesar", ["Pope Gregory", "Aryabhata", "Akbar"], "The Gregorian calendar corrected it in 1582."),
        ("Why was the Julian calendar replaced by the Gregorian calendar?", "it added slightly too many leap years and drifted from the seasons", ["it had no leap years", "it was based on the Moon", "it had 13 months"], "Pope Gregory XIII introduced the change."),
        ("How did ancient people use the stars to know the season?", "certain stars rise just before the Sun at certain times of the year", ["stars change colour each season", "stars disappear in winter", "stars show the time of day"], "Farmers watched for these risings."),
        ("Why do we have 24 hours in a day?", "it is based on the time the Earth takes to turn once in relation to the Sun", ["it is based on the Moon", "it was a random choice", "it is the time for a year"], "Hours and minutes divide this time.")]


ORIGIN = {"based mainly on the Moon": ["a lunar month", "the months of the Hijri calendar", "the date of Eid", "the tithis in a panchang", "Diwali falling on an amavasya (new moon)", "Purnima (full moon) festivals"],
          "based mainly on the Sun": ["the solar year", "the months of the Gregorian calendar", "the date of Makar Sankranti", "the seasons", "the year of the Indian national calendar", "leap years"]}
WDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def c_week(k=None):
    R = _R[0]
    d = R.randrange(7)
    n = R.choice([3, 5, 8, 9, 10, 12, 15, 20, 25, 30, 45, 50, 100])
    a = WDAYS[(d + n) % 7]
    return tq("Today is %s. Which day of the week will it be after %d days?" % (WDAYS[d], n), a, R.sample([x for x in WDAYS if x != a], 3),
              "%d = %d weeks and %d days, so count %d day%s on from %s: %s." % (n, n // 7, n % 7, n % 7, "" if n % 7 == 1 else "s", WDAYS[d], a))


def c_leap(k=None):
    R = _R[0]
    y = R.choice([1600, 1700, 1800, 1900, 2000, 2100, 2400, 1996, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 2001, 2010, 2019, 2023, 2026, 2030, 1998, 2002, 2015])
    leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0
    a = "yes, it is a leap year" if leap else "no, it is not a leap year"
    why = "the year %d is divisible by 400" % y if y % 400 == 0 else "the year %d is a century year not divisible by 400" % y if y % 100 == 0 else "the year %d is divisible by 4" % y if leap else "the year %d is not divisible by 4" % y
    return tq("In the Gregorian calendar, is the year %s a leap year?" % y, a, [x for x in ["yes, it is a leap year", "no, it is not a leap year", "only in India", "only every hundred years"] if x != a], "%s." % _cap(why))


def c_days(k=None):
    R = _R[0]
    n = R.choice([2, 3, 4, 5, 6, 8, 10, 12])
    if R.random() < 0.5:
        return nq("About how many days shorter are %d lunar years than %d solar years (taking 11 days per year)?" % (n, n), 11 * n, [n, 354 * n, 365 * n, 11], "days", "Each lunar year is about 11 days shorter, so %d × 11 = %d days." % (n, 11 * n))
    m = R.choice([2, 3, 4, 6, 8, 10, 12])
    return nq("Taking a lunar month as 29.5 days, how many days are there in %d lunar months?" % m, 29.5 * m, [30 * m, 28 * m, 29.5 + m, 29 * m], "days", "%d × 29.5 = %s days." % (m, nf(29.5 * m)))


# =================================================================== Chapter 12: how nature works in harmony
ROLE = {"a producer": ["grass", "a mango tree", "algae in a pond", "a neem tree", "phytoplankton in the sea", "a paddy plant"],
        "a primary consumer (herbivore)": ["a grasshopper", "a deer", "a rabbit", "a goat", "a caterpillar", "an elephant"],
        "a secondary or higher consumer (carnivore)": ["a frog eating insects", "a tiger", "a snake", "an eagle", "a lion", "a crocodile"],
        "a decomposer": ["a mushroom", "bacteria in the soil", "bread mould", "fungi on a fallen log"]}
CHAINS = [["grass", "grasshopper", "frog", "snake", "eagle"], ["algae", "small fish", "big fish", "heron"], ["grass", "deer", "tiger"],
          ["plant leaves", "caterpillar", "sparrow", "hawk"], ["phytoplankton", "zooplankton", "small fish", "seal"], ["grass", "rabbit", "fox"],
          ["paddy", "rat", "snake", "owl"], ["wheat", "mouse", "cat"]]


def c_chain(k=None):
    R = _R[0]
    ch = R.choice(CHAINS)
    allx = sorted({x for c in CHAINS for x in c} - set(ch))
    if R.random() < 0.6:
        i = R.randrange(len(ch) - 1) + 1
        s = " → ".join(ch[:i] + ["?"] + ch[i + 1:])
        pool = [x for x in ch if x != ch[i]] + R.sample(allx, 3)
        return tq("Fill the gap in this food chain: %s" % s, ch[i], R.sample(pool, 3), "The full chain is %s." % " → ".join(ch))
    w = R.sample(ch[1:] + R.sample(allx, 2), 3)
    return tq("In the food chain %s, which is the producer?" % " → ".join(ch), ch[0], w, "Food chains begin with a producer, a green plant or alga.")


PARKS = [("Jim Corbett National Park", "India's first national park (1936), in Uttarakhand, known for tigers"), ("Kaziranga National Park", "in Assam, famous for the one-horned rhinoceros"),
         ("Gir National Park", "in Gujarat, the last home of the Asiatic lion"), ("the Sundarbans", "mangrove forests of West Bengal, home of the Bengal tiger"),
         ("Keoladeo National Park", "in Bharatpur, Rajasthan, famous for migratory birds"), ("Periyar Tiger Reserve", "in Kerala, known for elephants and tigers"),
         ("Pachmarhi Biosphere Reserve", "in Madhya Pradesh, with Satpura National Park inside it"), ("the Nilgiri Biosphere Reserve", "India's first biosphere reserve (1986), in the Western Ghats"),
         ("Silent Valley National Park", "in Kerala, an untouched tropical rainforest home to the lion-tailed macaque"), ("Hemis National Park", "in Ladakh, a home of the snow leopard"),
         ("Bandipur National Park", "in Karnataka, known for elephants and tigers"), ("Chilika Lake", "in Odisha, a large lagoon visited by many migratory birds")]
HARM = [("What is an ecosystem?", "living things and their non-living surroundings working together", ["only the animals in a forest", "only the soil and water", "a single plant"], "A pond and a forest are ecosystems."),
        ("What are producers?", "green plants and algae that make their own food using sunlight", ["animals that eat plants", "fungi", "animals that eat meat"], "All food chains start with producers."),
        ("What do decomposers do?", "break down dead plants and animals and return nutrients to the soil", ["make food from sunlight", "hunt animals", "pollute water"], "Fungi and bacteria are decomposers."),
        ("What is a food web?", "many food chains linked together", ["a single food chain", "a spider's web", "a list of plants"], "Most animals eat more than one kind of food."),
        ("Where does the energy in a food chain come from first?", "the Sun", ["the soil", "water", "decomposers"], "Plants capture sunlight."),
        ("Why are there fewer tigers than deer in a forest?", "energy is lost at each step of the food chain, so fewer animals can be supported at the top", ["tigers do not eat", "deer eat tigers", "tigers live longer"], "Only about a tenth of energy passes on."),
        ("What would happen if all the frogs in a field were removed?", "insects might increase and snakes might decrease", ["nothing would change", "grass would vanish at once", "snakes would increase"], "Living things depend on each other."),
        ("How do bees help plants?", "they carry pollen from flower to flower (pollination)", ["they eat the roots", "they make the soil", "they give water"], "In return they get nectar."),
        ("What is symbiosis?", "two different organisms living together and benefiting each other", ["one animal hunting another", "a plant making food", "a fight between animals"], "Lichens are a fungus and an alga together."),
        ("What is a habitat?", "the natural home of an organism", ["its food", "its colour", "its size"], "The Sundarbans is the habitat of the Bengal tiger."),
        ("What is biodiversity?", "the variety of living things in an area", ["the number of rivers", "the weather of a place", "the height of mountains"], "The Western Ghats are rich in biodiversity."),
        ("What is deforestation?", "the cutting down of forests", ["planting trees", "watering trees", "studying trees"], "It harms wildlife and soil."),
        ("What is an endemic species?", "a species found only in a particular area", ["a species found everywhere", "an extinct species", "a domestic animal"], "The lion-tailed macaque is endemic to the Western Ghats."),
        ("What is an endangered species?", "a species whose numbers are so low that it may become extinct", ["a species that is increasing", "a pet animal", "a common weed"], "The great Indian bustard is endangered."),
        ("What is the Red Data Book?", "a record of endangered plants and animals", ["a book of recipes", "a train timetable", "a history book"], "It is kept by the IUCN."),
        ("What was Project Tiger, started in 1973?", "a programme to protect tigers and their habitats in India", ["a plan to hunt tigers", "a tiger zoo in every city", "a film"], "Tiger numbers have since increased."),
        ("What is a national park?", "a protected area where wildlife and their habitats are conserved", ["a city garden", "a zoo", "a farm"], "Grazing and hunting are not allowed."),
        ("What is migration?", "the regular movement of animals from one place to another, often with the seasons", ["animals sleeping in winter", "animals changing colour", "plants losing leaves"], "Siberian cranes once came to Bharatpur."),
        ("What is reforestation?", "planting trees where forests were cut down", ["cutting more trees", "burning forests", "building roads"], "Van Mahotsav encourages tree planting."),
        ("Why are earthworms called friends of farmers?", "they loosen the soil and add nutrients", ["they eat crops", "they spread diseases", "they make soil hard"], "They help air and water reach roots."),
        ("How do plants and animals depend on each other for gases?", "plants give oxygen that animals breathe, and animals give carbon dioxide that plants use", ["they do not exchange gases", "animals give oxygen to plants", "plants use oxygen only"], "This keeps the balance of gases in air."),
        ("What happens to energy at each step of a food chain?", "much of it is used or lost as heat, so less passes on", ["it increases", "it stays exactly the same", "it all goes to decomposers first"], "Food chains are usually short."),
        ("What are the non-living (abiotic) parts of an ecosystem?", "sunlight, air, water, soil and temperature", ["plants and animals", "fungi and bacteria", "only rocks"], "Living parts are called biotic."),
        ("What are the living (biotic) parts of an ecosystem?", "plants, animals and microorganisms", ["air and water", "rocks and soil", "sunlight"], "They interact with abiotic parts."),
        ("How do birds that eat fruits help plants?", "they spread the seeds to new places", ["they destroy all seeds", "they pollute the soil", "they stop plants growing"], "This is seed dispersal."),
        ("What happens when a non-native species takes over an area?", "it can crowd out local species and harm the ecosystem", ["the ecosystem always improves", "nothing happens", "all animals become happier"], "Lantana and water hyacinth are invasive in India."),
        ("Why are vultures important in nature?", "they clean up dead animals and prevent the spread of disease", ["they hunt elephants", "they pollinate flowers", "they make soil"], "Their numbers fell sharply because of a cattle drug."),
        ("What is a biosphere reserve?", "a large protected area for conserving biodiversity and the way of life of local people", ["a city zoo", "a private farm", "a botanical garden only"], "Nilgiri was the first in India."),
        ("Why do we celebrate Van Mahotsav?", "to encourage planting trees", ["to cut down forests", "to celebrate the monsoon only", "to build dams"], "It is held in the first week of July."),
        ("What is the 'balance of nature'?", "living things in an ecosystem kept in steady numbers by their relationships", ["having equal numbers of every animal", "no animals in a forest", "only plants in a forest"], "Removing predators can upset it.")]

# =================================================================== Chapter 13: our home Earth
EARTH = [("What makes the Earth suitable for life?", "liquid water, air with oxygen, a suitable temperature and protection from harmful rays", ["only its large size", "having rings", "being closest to the Sun"], "No other planet is known to have life."),
         ("What is the 'habitable zone' around the Sun?", "the region where a planet could have liquid water on its surface", ["the area inside the Sun", "the asteroid belt", "the region beyond Neptune"], "The Earth is in this zone."),
         ("How much of the Earth's surface is covered by water?", "about 71%", ["about 10%", "about 50%", "about 99%"], "Most of it is salty ocean water."),
         ("Why is fresh water precious?", "only a small part of Earth's water is fresh and easy to use", ["fresh water is everywhere", "sea water is fine to drink", "rain never falls"], "Much fresh water is frozen in ice caps."),
         ("What does the ozone layer do?", "it absorbs much of the Sun's harmful ultraviolet rays", ["it makes rain", "it gives oxygen for breathing", "it causes earthquakes"], "It is in the stratosphere."),
         ("Which chemicals damaged the ozone layer?", "CFCs (chlorofluorocarbons) used in old refrigerators and sprays", ["oxygen and nitrogen", "water vapour", "salt"], "The Montreal Protocol (1987) phased them out."),
         ("What is the greenhouse effect?", "gases in the air trapping heat and keeping the Earth warm", ["the cooling of glass houses", "plants growing faster", "the ozone hole"], "Without it, the Earth would be very cold."),
         ("Which gases are called greenhouse gases?", "carbon dioxide, methane and water vapour", ["oxygen and nitrogen only", "helium and neon", "hydrogen only"], "Their amounts are rising because of human activity."),
         ("What is global warming?", "the rise in the Earth's average temperature due to more greenhouse gases", ["the cooling of the Earth", "the heating of the Sun", "the warming of houses"], "Burning fossil fuels and cutting forests add to it."),
         ("What is one effect of global warming?", "melting glaciers and rising sea levels", ["more ice on the poles", "a colder climate everywhere", "shorter summers"], "Extreme weather also becomes more common."),
         ("Why does the Earth's atmosphere matter to life?", "it gives oxygen and carbon dioxide, keeps the temperature steady and protects from harmful rays", ["it has no use", "it only makes clouds", "it pushes the Moon"], "It also burns up most meteors."),
         ("What protects the Earth from charged particles streaming from the Sun?", "the Earth's magnetic field", ["the Moon", "the clouds", "the oceans"], "It causes auroras near the poles."),
         ("Which layer of the atmosphere do we live in?", "the troposphere", ["the stratosphere", "the mesosphere", "the thermosphere"], "Weather happens in this layer."),
         ("Why is soil important for life?", "plants grow in it and it holds water and nutrients", ["it gives us oxygen directly", "it makes rain", "it has no use"], "It takes hundreds of years to form a few centimetres."),
         ("What is sustainable development?", "meeting our needs without harming the ability of future generations to meet theirs", ["using up all resources quickly", "stopping all development", "cutting all forests"], "Use resources wisely."),
         ("Which of these helps reduce global warming?", "using public transport, solar energy and planting trees", ["burning more coal", "cutting forests", "leaving lights on"], "Every small action helps."),
         ("Why are wetlands important?", "they store water, reduce floods and are home to many birds and fish", ["they are wasteland", "they cause drought", "they pollute rivers"], "Chilika Lake is a famous wetland."),
         ("What is air pollution?", "harmful substances such as smoke and dust in the air", ["fresh air", "clouds", "oxygen"], "It harms lungs and the environment."),
         ("What is water pollution?", "harmful substances such as sewage and chemicals getting into water", ["rain falling into rivers", "fish living in water", "water evaporating"], "Polluted water spreads diseases."),
         ("What is the average temperature that makes liquid water possible on Earth?", "about 15 °C", ["about −100 °C", "about 200 °C", "about 1000 °C"], "Venus is far too hot and Mars too cold."),
         ("Why does the Moon have very hot days and very cold nights?", "it has no atmosphere to hold heat", ["it is close to the Sun", "it has oceans", "it spins very fast"], "The Earth's air acts like a blanket."),
         ("What is biodiversity's role on Earth?", "it keeps ecosystems stable and provides food, medicines and clean air and water", ["it has no role", "it causes pollution", "it uses up oxygen"], "Losing species weakens ecosystems."),
         ("Why is Venus much hotter than the Earth?", "its thick carbon dioxide atmosphere traps a great deal of heat", ["it is farther from the Sun", "it has oceans", "it has no atmosphere"], "This is a runaway greenhouse effect."),
         ("Why is Mars too cold for liquid water on its surface?", "it is farther from the Sun and has a very thin atmosphere", ["it is closest to the Sun", "it has thick clouds", "it has a large ocean"], "Water on Mars is mostly frozen."),
         ("What fraction of the Earth's water is salty sea water?", "about 97%", ["about 3%", "about 50%", "about 10%"], "Only about 3% is fresh water."),
         ("Where is most of the Earth's fresh water found?", "frozen in glaciers and ice caps", ["in rivers", "in clouds", "in wells"], "Groundwater holds much of the rest."),
         ("Why do auroras appear near the poles?", "charged particles from the Sun are guided by the Earth's magnetic field into the air there", ["the poles are hot", "the Moon shines there", "volcanoes erupt"], "They are seen as coloured lights in the sky."),
         ("Which gas in the atmosphere supports burning and breathing?", "oxygen", ["nitrogen", "carbon dioxide", "argon"], "It is about 21% of the air."),
         ("How do forests help to reduce global warming?", "trees absorb carbon dioxide for photosynthesis", ["they give out carbon dioxide only", "they heat the air", "they make the ozone hole"], "Forests are carbon sinks."),
         ("What was the Montreal Protocol of 1987?", "an international agreement to stop using chemicals that damage the ozone layer", ["a treaty on fishing", "a space mission", "a football league"], "The ozone layer is slowly recovering."),
         ("What is climate?", "the average weather of a place over many years", ["the weather today", "the time of day", "the height of mountains"], "Weather changes daily; climate over decades."),
         ("Why are coral reefs in danger from rising sea temperatures?", "warm water causes corals to lose their algae and bleach", ["corals like hot water", "corals are plants", "corals live on land"], "Coral reefs are home to many sea creatures.")]
GG = {"a greenhouse gas": ["carbon dioxide", "methane", "water vapour", "nitrous oxide", "CFCs"], "not a greenhouse gas": ["nitrogen", "oxygen", "argon", "helium", "neon"]}
POLL = {"a cause of air pollution": ["smoke from vehicles", "burning of crop stubble", "smoke from factory chimneys", "burning of plastic and garbage", "dust from construction"],
        "a cause of water pollution": ["sewage flowing into rivers", "factory waste dumped in lakes", "oil spills at sea", "washing clothes and cattle in ponds", "fertilisers washed into rivers by rain"],
        "a cause of soil pollution": ["overuse of pesticides", "throwing plastic bags on land", "dumping old batteries", "leaking garbage dumps", "too much chemical fertiliser"]}
ACT = {"an action that helps the Earth": ["planting trees", "using a cloth bag", "switching off unused lights", "using public transport", "harvesting rainwater", "composting kitchen waste", "using solar panels", "repairing things instead of throwing them away"],
       "an action that harms the Earth": ["burning plastic", "cutting forests", "dumping waste in rivers", "leaving taps running", "using single-use plastic", "burning crop stubble", "wasting food", "keeping the engine running while waiting"]}
SPHERE = [("the atmosphere", "the layer of air around the Earth"), ("the hydrosphere", "all the water on the Earth: oceans, rivers, lakes, ice and groundwater"),
          ("the lithosphere", "the solid rocky outer layer of the Earth"), ("the biosphere", "the zone where life exists, on land, in water and in the air"),
          ("the ozone layer", "a layer high in the atmosphere that absorbs ultraviolet rays"), ("the troposphere", "the lowest layer of the atmosphere, where weather happens"),
          ("the stratosphere", "the layer of the atmosphere above the troposphere, which contains the ozone layer"), ("the magnetic field", "the invisible shield that turns aside charged particles from the Sun"),
          ("the habitable zone", "the region around a star where a planet can have liquid water"), ("the greenhouse effect", "the trapping of heat by gases in the atmosphere")]


def UNITS8b():
    b = {k: once_maker(v) for k, v in [("ec", ECQ), ("sol", SOLQ), ("ml", MLQ), ("cal", CALQ), ("h", HARM), ("e", EARTH)]}
    sym = pairs(SYM, "What is the chemical symbol of %s?", "Which element has the symbol %s?")
    ecm = odd_one(ECM, "Which of these is %s?", "Which of these is not %s?")
    form = pairs(FORM, "What is the chemical formula of %s?", "Which substance has the formula %s?")
    homo = odd_one(HOMO, "Which of these is %s?", "Which of these is not %s?")
    solw = pairs(SOLW, "What is %s?", "What do we call %s?")
    mir = odd_one(MIR, "Which of these is %s?", "Which of these is not %s?")
    lens = odd_one(LENS, "Which of these uses %s?", "Which of these does not use %s?")
    img = pairs(IMG, "What kind of image is formed by %s?", "What forms an image that is %s?")
    refr = odd_one(REFR, "Which of these is %s?", "Which of these is not %s?")
    cal = pairs(CAL, "What is %s?", "What do we call %s?")
    origin = odd_one(ORIGIN, "Which of these is %s?", "Which of these is not %s?")
    role = odd_one(ROLE, "Which of these is %s?", "Which of these is not %s?")
    parks = pairs(PARKS, "What is %s known for?", "Which protected area is %s?")
    gg = odd_one(GG, "Which of these is %s?", "Which of these is not %s?")
    poll = odd_one(POLL, "Which of these is %s?", "Which of these is not %s?")
    act = odd_one(ACT, "Which of these is %s?", "Which of these is not %s?")
    sph = pairs(SPHERE, "What is %s?", "What do we call %s?")
    return [
        U(8, "nature-of-matter-elements-compounds-and-mixtures", 8, MT,
          "Pure substances and mixtures; elements, their symbols and atoms; compounds, molecules and formulas; properties of compounds compared with mixtures; homogeneous and heterogeneous mixtures; alloys (summary of NCERT Curiosity Chapter 8).",
          "Nature of Matter: Elements, Compounds and Mixtures", "elements, compounds and mixtures",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 8: elements and their symbols, compounds and formulas, mixtures, homogeneous and heterogeneous mixtures, and how compounds differ from mixtures. 100 questions with answers.",
          "Elements have one kind of atom; compounds join elements in a fixed ratio.", "Mixtures keep the properties of their parts.",
          "<p>An element is made of only one kind of atom and is shown by a symbol, such as O for oxygen and Fe for iron. A compound is made of two or more elements chemically joined in a fixed ratio, such as water (H₂O) and carbon dioxide (CO₂); it has new properties and can be broken down only by chemical methods.</p>"
          "<p>A mixture contains substances mixed in any proportion without a chemical change, so its parts keep their properties and can be separated by physical methods. Mixtures are homogeneous (the same throughout, like salt water) or heterogeneous (like sand and water). Alloys such as brass and steel are mixtures.</p>",
          [("Symbol of copper?", ["from the Latin 'cuprum'"], "Cu"), ("Iron and sulphur, not heated: element, compound or mixture?", ["a magnet can remove the iron"], "a mixture")],
          ["Calling air a compound.", "Calling brass an element.", "Thinking a compound keeps the properties of its elements."],
          [("What is the difference between a compound and a mixture?", "A compound has elements chemically joined in a fixed ratio with new properties; a mixture has parts that are not chemically joined and keep their own properties."),
           ("Why is the symbol of iron Fe?", "It comes from 'ferrum', the Latin name for iron.")],
          lambda: [("Elements and symbols", [(sym, 16), (b["ec"], 4)]), ("Compounds and formulas", [(form, 12), (b["ec"], 8)]), ("Elements, compounds or mixtures", [(ecm, 16), (b["ec"], 4)]),
                   ("Kinds of mixtures", [(homo, 14), (b["ec"], 2), (ecm, 4)]), ("Mixed problems", [(ecm, 8), (sym, 6), (homo, 4), (form, 2)])]),
        U(9, "the-amazing-world-of-solutes-solvents-and-solutions", 9, MT,
          "Solutions, solutes and solvents; water as a universal solvent; saturated and unsaturated solutions; solubility and the effect of temperature; concentration; dissolving of gases in water; density, floating and sinking (summary of NCERT Curiosity Chapter 9).",
          "The Amazing World of Solutes, Solvents and Solutions", "solutes, solvents and solutions",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 9: solutes, solvents and solutions, saturated solutions, solubility and temperature, concentration, gases in water, and density, floating and sinking. 100 questions with answers.",
          "Solute + solvent → solution.", "Density = mass ÷ volume; less dense than water floats.",
          "<p>In a solution, the solute (such as sugar) dissolves in the solvent (such as water). Water dissolves so many substances that it is called the universal solvent. A saturated solution can dissolve no more solute at that temperature; the most solute that can dissolve is its solubility. Solids usually dissolve more in hot water, but gases such as oxygen dissolve less.</p>"
          "<p>Concentration tells how much solute is in a solution: adding solvent makes it more dilute. Density is mass per unit volume (g/cm³). Water has a density of about 1 g/cm³, so oil, ice and wood float on it while iron and stone sink; salt water is denser, so an egg floats in it.</p>",
          [("Salt in water: solute?", ["the substance that dissolves"], "salt"), ("Mass 40 g, volume 20 cm³. Density?", ["40 ÷ 20"], "2 g/cm³")],
          ["Thinking more of every substance dissolves in hot water, including gases.", "Mixing up solute and solvent.", "Thinking heavy objects always sink."],
          [("What is a saturated solution?", "A solution in which no more solute can dissolve at that temperature; extra solute stays undissolved."),
           ("Why does ice float on water?", "Ice is less dense than liquid water, because water expands when it freezes.")],
          lambda: [("Solutes, solvents and solutions", [(c_solup, 10), (solw, 10)]), ("Saturated solutions and solubility", [(c_satur, 12), (b["sol"], 8)]), ("Concentration", [(c_conc, 8), (solw, 4), (b["sol"], 8)]),
                   ("Density, floating and sinking", [(K(c_dens, "float"), 8), (K(c_dens, "d"), 6), (K(c_dens, "m"), 6)]), ("Mixed problems", [(K(c_dens, "d"), 8), (K(c_dens, "m"), 8), (c_satur, 2), (b["sol"], 2)])]),
        U(10, "light-mirrors-and-lenses", 10, PH,
          "Reflection from curved mirrors; concave and convex mirrors and their uses; real and virtual images; convex and concave lenses and their uses; the magnifying glass; refraction and dispersion of light; correcting defects of vision (summary of NCERT Curiosity Chapter 10).",
          "Light: Mirrors and Lenses", "mirrors and lenses",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 10: concave and convex mirrors and lenses, real and virtual images, uses of mirrors and lenses, refraction and the colours of white light. 100 questions with answers.",
          "Concave mirrors and convex lenses converge light.", "Convex mirrors and concave lenses spread light out.",
          "<p>A concave mirror curves inwards: held close it gives an enlarged upright image (shaving and dentist's mirrors), and it sends out a strong beam from a bulb at its focus (torches). A convex mirror bulges outwards and always gives a smaller, upright image with a wide view (rear-view mirrors). Real images can be caught on a screen; virtual images cannot.</p>"
          "<p>A convex lens is thicker in the middle and brings light together; it is used in magnifying glasses, cameras and our eyes. A concave lens is thinner in the middle and spreads light out. Light bends (refracts) as it enters glass or water, and a prism splits white light into seven colours.</p>",
          [("Rear-view mirror of a car?", ["wide view, upright image"], "a convex mirror"), ("A magnifying glass is…", ["thicker in the middle"], "a convex lens")],
          ["Mixing up concave and convex mirrors.", "Thinking a virtual image can be caught on a screen.", "Calling a magnifying glass a concave lens."],
          [("What is the difference between a real and a virtual image?", "A real image can be formed on a screen and is upside down; a virtual image cannot be formed on a screen."),
           ("Why is a convex mirror used as a rear-view mirror?", "It always gives an upright, smaller image and shows a wide area behind the vehicle.")],
          lambda: [("Concave and convex mirrors", [(mir, 12), (b["ml"], 8)]), ("Images", [(img, 10), (b["ml"], 10)]), ("Lenses", [(lens, 12), (b["ml"], 4), (refr, 4)]),
                   ("Uses of mirrors and lenses", [(mir, 8), (lens, 8), (refr, 4)]), ("Mixed problems", [(refr, 12), (mir, 4), (b["ml"], 4)])]),
        U(11, "keeping-time-with-the-skies", 11, ES,
          "Days, months and years from the motions of the Earth and Moon; lunar, solar and lunisolar calendars; leap years; the extra month in Indian calendars; the Indian national (Saka) calendar; the panchang and ancient Indian astronomy (summary of NCERT Curiosity Chapter 11).",
          "Keeping Time with the Skies", "keeping time with the skies",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 11: days, months and years, lunar and solar calendars, leap years, lunisolar calendars and the extra month, and the Indian national calendar. 100 questions with answers.",
          "The Earth's spin gives the day; the Moon the month; the orbit the year.", "A leap year every 4 years keeps the calendar in step.",
          "<p>A day comes from the Earth's rotation, a month from the Moon's cycle of phases (about 29.5 days) and a year from the Earth's revolution (about 365¼ days). The extra quarter days add up to a leap day every four years; in the Gregorian calendar a century year is a leap year only if it is divisible by 400.</p>"
          "<p>Twelve lunar months make about 354 days, about 11 days less than a solar year, so festivals of a purely lunar calendar move earlier each year. Indian lunisolar calendars add an extra month (adhik maas) about every three years. India's national calendar is the Saka calendar, adopted in 1957, which begins on 22 March (21 March in a leap year).</p>",
          [("Is 1900 a leap year?", ["century year not divisible by 400"], "no"), ("12 lunar months ≈ ?", ["12 × 29.5"], "354 days")],
          ["Thinking every year divisible by 4 is a leap year, even 1900.", "Mixing up the lunar month and the solar year.", "Thinking festivals of lunar calendars fall on the same date each year."],
          [("Why do we need leap years?", "The solar year is about 365¼ days; adding one day every four years keeps the calendar in step with the seasons."),
           ("What is a lunisolar calendar?", "A calendar whose months follow the Moon but which adds an extra month now and then to stay in step with the solar year.")],
          lambda: [("Days, months and years", [(cal, 10), (b["cal"], 10)]), ("Leap years", [(c_leap, 16), (cal, 2), (b["cal"], 2)]), ("Lunar and solar calendars", [(origin, 12), (c_days, 8)]),
                   ("Indian calendars", [(b["cal"], 10), (c_week, 10)]), ("Mixed problems", [(c_week, 8), (c_leap, 4), (c_days, 4), (origin, 4)])]),
        U(12, "how-nature-works-in-harmony", 12, LW,
          "Ecosystems and their living and non-living parts; producers, consumers and decomposers; food chains and food webs; energy flow; interdependence, pollination and symbiosis; biodiversity, endangered and endemic species; conservation and protected areas in India (summary of NCERT Curiosity Chapter 12).",
          "How Nature Works in Harmony", "how nature works in harmony",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 12: ecosystems, producers, consumers and decomposers, food chains and food webs, interdependence, biodiversity, endangered species and protected areas of India. 100 questions with answers.",
          "Producers, consumers and decomposers depend on each other.", "Food chains start with plants; energy comes from the Sun.",
          "<p>An ecosystem is made of living things and their non-living surroundings. Producers (green plants and algae) make food using sunlight; herbivores eat them, carnivores eat other animals, and decomposers such as fungi and bacteria return nutrients to the soil. Linked food chains form a food web, and energy decreases at each step.</p>"
          "<p>Living things depend on each other: bees pollinate flowers, lichens are a partnership of fungus and alga, and removing one species affects others. We protect biodiversity in national parks such as Jim Corbett and Kaziranga, through Project Tiger and biosphere reserves such as the Nilgiris.</p>",
          [("grass → ? → frog → snake", ["eats grass, eaten by frogs"], "grasshopper"), ("Mushroom: producer, consumer or decomposer?", ["feeds on dead matter"], "decomposer")],
          ["Starting a food chain with an animal.", "Thinking decomposers are useless.", "Thinking removing one species affects nothing."],
          [("What is the role of decomposers?", "They break down dead plants and animals, returning nutrients to the soil for producers to use."),
           ("Why are food chains usually short?", "A lot of energy is lost at each step, so there is not enough left to support many levels.")],
          lambda: [("Ecosystems", [(b["h"], 12), (role, 8)]), ("Producers, consumers and decomposers", [(role, 18), (b["h"], 2)]), ("Food chains and webs", [(c_chain, 16), (b["h"], 4)]),
                   ("Conservation", [(parks, 16), (b["h"], 4)]), ("Mixed problems", [(role, 10), (c_chain, 8), (b["h"], 2)])]),
        U(13, "our-home-earth-a-unique-life-sustaining-planet", 13, ES,
          "What makes the Earth suitable for life: water, the atmosphere, a suitable temperature and protection from harmful radiation; the atmosphere, hydrosphere, lithosphere and biosphere; the ozone layer; the greenhouse effect and global warming; pollution and sustainable living (summary of NCERT Curiosity Chapter 13).",
          "Our Home: Earth, a Unique Life-Sustaining Planet", "Earth, our home",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 13: why the Earth supports life, the atmosphere and hydrosphere, the ozone layer, the greenhouse effect, global warming, pollution and sustainable living. 100 questions with answers.",
          "Water, air and the right temperature make Earth special.", "Protect the ozone layer; reduce greenhouse gases.",
          "<p>The Earth is the only planet known to support life. It is in the Sun's habitable zone, has liquid water covering about 71% of its surface, an atmosphere with oxygen that keeps temperatures steady, an ozone layer that absorbs ultraviolet rays and a magnetic field that shields it from charged particles from the Sun.</p>"
          "<p>Greenhouse gases such as carbon dioxide and methane keep the Earth warm, but burning fuels and cutting forests add more of them and cause global warming, melting glaciers and rising seas. We can help by saving energy and water, planting trees, reducing waste and using renewable energy: this is sustainable living.</p>",
          [("Which layer absorbs UV rays?", ["high in the atmosphere"], "the ozone layer"), ("Is oxygen a greenhouse gas?", ["it does not trap heat"], "no")],
          ["Confusing the ozone hole with global warming.", "Thinking all of the Earth's water is fresh.", "Thinking greenhouse gases are only harmful."],
          [("What is the greenhouse effect?", "Gases such as carbon dioxide, methane and water vapour trap heat from the Sun and keep the Earth warm enough for life."),
           ("Why is the ozone layer important?", "It absorbs most of the Sun's harmful ultraviolet rays, protecting living things.")],
          lambda: [("Why the Earth supports life", [(b["e"], 14), (sph, 6)]), ("The atmosphere and the ozone layer", [(sph, 10), (gg, 5), (b["e"], 5)]), ("The greenhouse effect", [(gg, 3), (b["e"], 5), (poll, 12)]),
                   ("Protecting our planet", [(act, 16), (poll, 4)]), ("Mixed problems", [(act, 10), (poll, 8), (b["e"], 2)])]),
    ]
