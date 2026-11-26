# -*- coding: utf-8 -*-
"""Class 7 Science (NCERT Curiosity, chapters 1–6): question makers and UNITS7a()."""
from uk_alsci import tq, nf, once_maker
from in_sci import pairs, _R, U, K
from in_sci6a import NS, LW, MT, PH, ES, odd_one, nq, _cap
import in_sci

# =================================================================== Chapter 1: the ever-evolving world of science
EVOL = [("Why is science called 'ever-evolving'?", "ideas change and improve when new evidence is found", ["its ideas never change", "it is only about evolution of animals", "scientists stop asking questions"], "Old ideas are tested again with better tools."),
        ("People once believed the Sun went round the Earth. What changed this idea?", "careful observations and new evidence about the motion of planets", ["a vote", "a popular story", "a king's order"], "Copernicus and Galileo gave new evidence; ancient Indian astronomer Aryabhata also said the Earth spins."),
        ("Which ancient Indian astronomer said that the Earth spins on its axis?", "Aryabhata", ["C. V. Raman", "Charaka", "Sushruta"], "He lived about 1500 years ago."),
        ("Which ancient Indian physician is known for his work on medicine (Charaka Samhita)?", "Charaka", ["Aryabhata", "Bhaskara", "Varahamihira"], "Sushruta is known for surgery."),
        ("Which ancient Indian surgeon described many surgical tools?", "Sushruta", ["Aryabhata", "Charaka", "Brahmagupta"], "The Sushruta Samhita describes surgery."),
        ("What is evidence in science?", "observations and measurements that support or reject an idea", ["a guess with no reason", "a story", "something that cannot be checked"], "Scientists ask for evidence."),
        ("What should a scientist do if new evidence goes against an old idea?", "test the idea again and change it if needed", ["ignore the new evidence", "hide the evidence", "punish the person who found it"], "Science corrects itself."),
        ("How does new technology help science grow?", "better instruments let us observe things we could not see before", ["it makes questions unnecessary", "it replaces all thinking", "it stops experiments"], "The microscope showed cells; telescopes showed moons of Jupiter."),
        ("Which instrument helped Galileo see the moons of Jupiter?", "a telescope", ["a microscope", "a thermometer", "a compass"], "This showed that not everything goes round the Earth."),
        ("Which instrument made it possible to see cells?", "the microscope", ["the telescope", "the barometer", "the stethoscope"], "Robert Hooke saw cells in cork in 1665."),
        ("What is a scientific attitude?", "being curious, open-minded and asking for evidence", ["believing everything we hear", "refusing to change our mind ever", "copying others"], "It helps in daily life too."),
        ("Why do scientists work in teams and share data?", "others can check results and add new ideas", ["to keep work secret", "to avoid all mistakes by guessing", "because working alone is not allowed"], "Science is a group effort across the world."),
        ("Why must an experiment be described clearly?", "so that others can repeat it and check the results", ["so that nobody can repeat it", "to make it look long", "because it changes the result"], "Repeatable results are trusted more."),
        ("What is a superstition?", "a belief that is not supported by evidence", ["a tested scientific law", "a measurement", "an experiment"], "A black cat crossing the road does not cause bad luck."),
        ("How can you test the claim 'plants grow better with music'?", "grow two sets of the same plants, one with music and one without, and compare", ["ask one friend", "read a story about it", "believe it without testing"], "Keep everything else the same."),
        ("Which of these is an example of science changing our daily life?", "vaccines that protect us from diseases", ["the colour of our school bag", "our favourite song", "the name of our street"], "Mobile phones and clean water supply also come from science."),
        ("Why is it important to question even well-known ideas?", "testing them again can reveal mistakes or improve them", ["because all old ideas are wrong", "to disrespect scientists", "because questions are bad"], "Asking 'how do we know?' is the heart of science."),
        ("What did Edward Jenner develop that later led to the end of smallpox?", "the first vaccine", ["the telescope", "the electric bulb", "the steam engine"], "Smallpox was declared eradicated in 1980."),
        ("Which ISRO mission put a spacecraft in orbit around Mars in its first attempt?", "Mangalyaan (Mars Orbiter Mission)", ["Chandrayaan-1", "Aryabhata", "Aditya-L1"], "It reached Mars in 2014."),
        ("Why are mistakes useful in science?", "they show what does not work and lead to better tests", ["they should always be hidden", "they prove science is useless", "they end all research"], "Many discoveries came from unexpected results."),
        ("What is a model in science?", "a simple representation that helps explain how something works", ["an exact copy that never changes", "a toy for fun only", "a final answer"], "Models of the atom changed as evidence grew."),
        ("Why did the model of the atom change many times?", "new experiments gave new evidence", ["scientists liked new drawings", "atoms changed shape", "no one tested it"], "Thomson, Rutherford and Bohr each improved it."),
        ("Which is a testable question?", "Does salt water freeze at a lower temperature than plain water?", ["Is blue the best colour?", "Which song is the most beautiful?", "Are cats nicer than dogs?"], "It can be answered by measuring."),
        ("What does it mean to analyse data?", "to look for patterns and relationships in the results", ["to throw away the results", "to guess the results", "to copy results from a friend"], "Graphs make patterns easy to see."),
        ("Why do scientists repeat a measurement several times and take the average?", "to reduce the effect of small errors", ["to make the answer bigger", "to waste time", "because one reading is always wrong"], "The average is more reliable."),
        ("What is a control in an experiment?", "a set-up kept without the change, for comparison", ["the most expensive instrument", "the person in charge", "the final result"], "A pot without fertiliser is a control."),
        ("What is the best way to show how a plant's height changed each day?", "a line graph of height against day", ["a long paragraph", "a single number", "a drawing of the pot only"], "Graphs show trends."),
        ("What do we call the variable that we change on purpose in an experiment?", "the independent variable", ["the dependent variable", "the controlled variable", "the result"], "The dependent variable is what we measure."),
        ("What do we call the variable we measure in an experiment?", "the dependent variable", ["the independent variable", "the constant", "the hypothesis"], "It depends on the change we make."),
        ("A claim says a new drink makes you taller in a week. What should a scientist ask?", "what evidence supports this, and was it tested fairly?", ["how much it costs only", "what colour the bottle is", "nothing; believe it"], "Extraordinary claims need strong evidence."),
        ("How did the invention of the printing press help science?", "ideas and results could be shared widely and quickly", ["it made experiments unnecessary", "it stopped scientists working together", "it made books secret"], "Today the internet does the same."),
        ("Which of these is a scientific way to settle a disagreement about which cloth dries fastest?", "test the cloths fairly and compare the drying times", ["ask the oldest person", "toss a coin", "choose the prettiest cloth"], "Evidence settles the question."),
        ("Why should conclusions be based on many observations, not just one?", "one observation may be unusual or a mistake", ["one observation is always enough", "many observations change the truth", "it makes the work easier"], "More data gives more confidence."),
        ("What does it mean that scientific knowledge is tentative?", "it can change if new evidence is found", ["it is never true", "it is always fixed", "it is only a guess with no evidence"], "Good ideas survive many tests.")]
METHOD = [("making an observation", "noticing that iron gates rust faster near the sea"), ("asking a question", "wondering whether salt water makes iron rust faster"),
          ("forming a hypothesis", "suggesting that salt speeds up rusting"), ("testing with an experiment", "keeping iron nails in plain water and in salt water for a week"),
          ("analysing results", "comparing how much rust formed on each nail"), ("drawing a conclusion", "deciding that salt water does speed up rusting"),
          ("communicating results", "presenting the findings to the class with photographs")]
FAIR7 = [("Does the amount of salt in water change how fast an iron nail rusts?", "the amount of salt", "the amount of rust after a week", "the size of the nail"),
         ("Does the colour of a cloth change how hot it gets in the sun?", "the colour of the cloth", "the temperature under the cloth", "the time kept in the sun"),
         ("Does the temperature of water change how fast sugar dissolves?", "the temperature of the water", "the time taken for the sugar to dissolve", "the amount of sugar"),
         ("Does the length of a pendulum change the time of one oscillation?", "the length of the string", "the time for 20 oscillations", "the mass of the bob"),
         ("Does the number of cells change how bright a bulb glows?", "the number of cells", "the brightness of the bulb", "the kind of bulb"),
         ("Does fertiliser make bean plants grow taller?", "whether fertiliser is added", "the height of the plants", "the amount of water given"),
         ("Does the height of a ramp change how far a toy car rolls?", "the height of the ramp", "the distance the car rolls", "the toy car used"),
         ("Does the thickness of a cloth change how long ice stays frozen when wrapped in it?", "the thickness of the cloth", "the time for the ice to melt", "the size of the ice cube"),
         ("Does stirring help salt dissolve faster?", "whether the water is stirred", "the time for the salt to dissolve", "the temperature of the water"),
         ("Does a plant lose more water in the wind?", "whether the plant is in the wind", "the mass of water lost in a day", "the size of the plant"),
         ("Does the amount of light change how fast pond plants make bubbles of oxygen?", "the amount of light", "the number of bubbles in one minute", "the kind of pond plant"),
         ("Does the material of a cup change how fast hot water cools?", "the material of the cup", "the temperature after 10 minutes", "the starting temperature of the water")]


def c_var(k=None):
    R = _R[0]
    q, ch, me, keep = R.choice(FAIR7)
    k = k or R.choice(["change", "measure", "keep"])
    extra = R.choice(["the name of the student", "the time of the school bell", "the colour of the notebook"])
    if k == "change":
        return tq("Investigation: <i>%s</i> Which variable is changed on purpose?" % q, ch, [me, keep, extra], "Change %s; measure %s; keep %s the same." % (ch, me, keep))
    if k == "measure":
        return tq("Investigation: <i>%s</i> Which variable is measured?" % q, me, [ch, keep, extra], "Change %s; measure %s; keep %s the same." % (ch, me, keep))
    return tq("Investigation: <i>%s</i> Which variable must be kept the same?" % q, keep, [ch, me, extra], "Change %s; measure %s; keep %s the same." % (ch, me, keep))


DISC = [("Aryabhata", "suggesting that the Earth spins on its axis"), ("C. V. Raman", "discovering the Raman effect in the scattering of light"),
        ("Jagadish Chandra Bose", "showing that plants respond to stimuli, using the crescograph"), ("Galileo Galilei", "seeing the moons of Jupiter through a telescope"),
        ("Robert Hooke", "seeing and naming cells in a thin slice of cork"), ("Edward Jenner", "developing the first vaccine, against smallpox"),
        ("Alexander Fleming", "discovering penicillin, the first antibiotic"), ("Isaac Newton", "describing the laws of motion and gravitation"),
        ("Marie Curie", "studying radioactivity and discovering radium"), ("Janaki Ammal", "breeding high-yielding varieties of sugarcane"),
        ("Asima Chatterjee", "developing medicines from plants against malaria and epilepsy"), ("Srinivasa Ramanujan", "making great discoveries in mathematics")]
CLAIM = {"a claim supported by evidence": ["Seeds kept without water did not germinate in our test.", "The thermometer showed that the water boiled at 100 °C.", "Ten repeated trials gave almost the same result.",
                                       "The plant kept in light grew taller in our measurements.", "Our graph shows that the pendulum's time does not depend on the mass of the bob."],
         "a superstition": ["A black cat crossing the road brings bad luck.", "Wearing a lucky shirt helps you score more marks.", "Breaking a mirror causes seven years of bad luck.",
                                      "Sneezing before leaving home makes the journey fail.", "Cutting nails at night brings bad luck."]}

# =================================================================== Chapter 2: acidic, basic and neutral
SUBST = {"acidic": ["lemon juice", "vinegar", "orange juice", "curd", "tamarind water", "amla juice", "tomato juice", "dilute hydrochloric acid"],
         "basic": ["baking soda solution", "soap solution", "lime water", "washing soda solution", "milk of magnesia", "toothpaste in water", "dilute sodium hydroxide"],
         "neutral": ["sugar solution", "common salt solution", "distilled water", "glucose solution"]}
ACIDS = [("lemon", "citric acid"), ("vinegar", "acetic acid"), ("curd", "lactic acid"), ("tamarind", "tartaric acid"), ("an ant sting", "formic acid"),
         ("amla", "ascorbic acid (vitamin C)"), ("our stomach", "hydrochloric acid"), ("spinach", "oxalic acid")]
IND = {"blue litmus": {"acidic": "turns red", "basic": "no change", "neutral": "no change"},
       "red litmus": {"acidic": "no change", "basic": "turns blue", "neutral": "no change"},
       "turmeric paper": {"acidic": "no change", "basic": "turns red", "neutral": "no change"},
       "china rose indicator": {"acidic": "turns dark pink (magenta)", "basic": "turns green", "neutral": "no change"}}
CH_ALL = ["turns red", "turns blue", "no change", "turns green", "turns dark pink (magenta)"]


def c_ind(k=None):
    R = _R[0]
    ind = R.choice(sorted(IND))
    kind = R.choice(sorted(SUBST))
    sub = R.choice(SUBST[kind])
    a = IND[ind][kind]
    return tq("A drop of %s is put on %s. What happens to the colour of the indicator?" % (sub, ind), a, R.sample([x for x in CH_ALL if x != a], 3),
              "%s is %s; %s %s in %s solutions." % (_cap(sub), kind, ind, a, kind))


def c_ind2(k=None):
    R = _R[0]
    ind = R.choice(["blue litmus", "red litmus", "china rose indicator", "turmeric paper"])
    kind = R.choice([x for x in ("acidic", "basic") if IND[ind][x] != "no change"])
    res = IND[ind][kind]
    return tq("A solution makes %s %s. What is the nature of the solution?" % (ind, res.replace("turns ", "turn ")), kind, [x for x in ("acidic", "basic", "neutral", "it cannot be tested") if x != kind],
              "%s %s in %s solutions." % (_cap(ind), res, kind))


NEUT = [("What is neutralisation?", "the reaction of an acid with a base to give salt and water", ["the mixing of two acids", "the boiling of water", "the melting of salt"], "Heat is also given out."),
        ("What are the products of neutralisation?", "a salt and water (and heat)", ["only an acid", "only a base", "oxygen and hydrogen only"], "Acid + base → salt + water."),
        ("Why is an antacid such as milk of magnesia taken for acidity?", "it is a base that neutralises extra acid in the stomach", ["it is an acid that adds more acid", "it is neutral sugar", "it cools the stomach only"], "Too much stomach acid causes indigestion."),
        ("Why is baking soda rubbed on an ant sting?", "the sting injects formic acid, and baking soda (a base) neutralises it", ["baking soda is an acid", "it makes the sting deeper", "it kills the ant"], "Calamine also helps."),
        ("Why do farmers add quicklime or slaked lime to some soils?", "to neutralise soil that is too acidic", ["to make the soil more acidic", "to add sugar", "to kill earthworms"], "Most crops grow best in soil that is nearly neutral."),
        ("What is added to soil that is too basic?", "organic matter such as compost, which releases acids", ["quicklime", "slaked lime", "baking soda"], "Compost makes soil less basic."),
        ("Why is factory waste water neutralised before it is let into rivers?", "acids or bases in it would harm fish and plants", ["to make it hot", "to add colour", "to make it salty for fish"], "Neutralising protects water life."),
        ("Why should we never taste unknown substances to see if they are acids?", "strong acids and bases can burn and are harmful", ["acids are always sweet", "bases are always sour", "tasting is the best test"], "Use indicators instead."),
        ("What is an indicator?", "a substance that changes colour in acids or bases", ["a strong acid", "a kind of salt", "a thermometer"], "Litmus, turmeric and china rose are indicators."),
        ("Which natural substance is litmus made from?", "lichens", ["turmeric", "china rose petals", "red cabbage"], "Litmus is purple in water."),
        ("How do acids usually taste?", "sour", ["bitter and soapy", "sweet", "salty only"], "Lemon and tamarind taste sour; never taste lab acids."),
        ("How do bases usually feel?", "soapy (slippery) to touch", ["rough", "sticky like glue", "hot"], "Soap and baking soda solutions are basic."),
        ("Why does a turmeric stain on clothes turn red when washed with soap?", "soap is basic and turmeric turns red in bases", ["soap is acidic", "turmeric is a base", "water is red"], "The colour returns when the soap is washed away."),
        ("Which acid is found in our stomach and helps digest food?", "hydrochloric acid", ["acetic acid", "citric acid", "tartaric acid"], "It also kills germs in food."),
        ("What is the nature of distilled water?", "neutral", ["acidic", "basic", "strongly acidic"], "It does not change any indicator."),
        ("What happens to the temperature when an acid is neutralised by a base?", "it rises, because heat is given out", ["it falls to 0 °C", "it stays exactly the same", "it falls below zero"], "Neutralisation is exothermic."),
        ("What is an olfactory indicator?", "a substance whose smell changes in acids or bases", ["one that changes colour only", "a salt", "a type of litmus"], "Onion and clove oil are examples."),
        ("Which of these is a salt formed by neutralisation?", "sodium chloride (common salt)", ["vinegar", "lime water", "soap"], "Hydrochloric acid + sodium hydroxide → sodium chloride + water."),
        ("A farmer finds his soil is too acidic. What should he add?", "slaked lime", ["vinegar", "lemon juice", "compost only"], "Lime is basic."),
        ("Why is toothpaste basic?", "to neutralise the acid made by bacteria that causes tooth decay", ["to make teeth acidic", "to taste sour", "to add sugar"], "Acid damages tooth enamel."),
        ("Which of these is a strong acid used in laboratories?", "sulphuric acid", ["citric acid", "lactic acid", "tartaric acid"], "Handle laboratory acids carefully."),
        ("Why are acids stored in glass bottles, not metal cans?", "acids react with many metals", ["glass is cheaper", "metal cans are too heavy", "acids are attracted to magnets"], "Acid can eat through some metals."),
        ("How can you make an indicator at home from turmeric?", "make a paste of turmeric with water and dry it on paper", ["boil turmeric in oil", "mix turmeric with sugar", "burn turmeric"], "Turmeric paper turns red in bases."),
        ("How is china rose indicator prepared?", "by soaking china rose petals in warm water", ["by burning the petals", "by mixing petals with sand", "by freezing the petals"], "It is a natural indicator."),
        ("What colour is litmus solution in distilled water?", "purple", ["red", "blue", "green"], "It is neutral."),
        ("Which of these is the safest way to find out if a liquid is acidic?", "put a drop on blue litmus paper", ["taste a little", "smell it closely", "touch it with your finger"], "Indicators are safe to use."),
        ("Why does milk turn sour after some time?", "bacteria change it into lactic acid", ["it becomes basic", "it freezes", "it loses water"], "Curd also contains lactic acid."),
        ("What happens to a bee or ant sting when baking soda paste is applied?", "the acid in the sting is neutralised and the pain reduces", ["the sting becomes more acidic", "the skin turns blue", "nothing happens"], "Baking soda is a mild base."),
        ("What is formed when hydrochloric acid reacts with sodium hydroxide?", "sodium chloride and water", ["sugar and oxygen", "only hydrogen", "vinegar and soap"], "This is a neutralisation reaction.")]

# =================================================================== Chapter 3: electricity — circuits and their components
COMP = [("an electric cell", "providing electrical energy to a circuit"), ("a battery", "two or more cells joined together to give more energy"),
        ("a switch", "opening or closing a circuit"), ("a bulb", "giving light when current flows through its filament"),
        ("the filament", "the thin wire in a bulb that glows when current flows"), ("connecting wires", "carrying current between the parts of a circuit"),
        ("a fuse", "breaking the circuit when too much current flows"), ("an LED", "a small light that glows only when connected the right way round"),
        ("the positive terminal", "the end of a cell marked '+', usually the metal cap"), ("the negative terminal", "the end of a cell marked '−', the flat metal disc")]
COND = {"a conductor of electricity": ["a copper wire", "an iron nail", "an aluminium foil", "a steel spoon", "graphite (pencil lead)", "a brass key", "a silver coin", "a safety pin", "a gold ring", "a steel key"],
        "an insulator of electricity": ["a rubber eraser", "a plastic scale", "a piece of wood", "a glass rod", "dry cotton thread", "a paper strip", "a wax candle", "a clay cup", "a dry leaf", "a woollen thread"]}
CKT = [("A bulb, a cell and a switch are in a circuit. The switch is open. Does the bulb glow?", "no, because the circuit is incomplete", ["yes, brightly", "yes, dimly", "only if the cell is new"], "Current flows only in a closed circuit."),
       ("What is a closed circuit?", "a complete path through which current can flow", ["a circuit with a gap", "a circuit with no cell", "a broken wire"], "The switch must be ON."),
       ("What is an open circuit?", "a circuit with a gap, so no current flows", ["a complete circuit", "a circuit with two cells", "a circuit with a bright bulb"], "An OFF switch makes the circuit open."),
       ("Why does a fused bulb not glow?", "its filament is broken, so the circuit is incomplete", ["it has too much current", "the glass is dirty", "the cell is too strong"], "Replace the bulb."),
       ("Why are electric wires covered with plastic or rubber?", "plastic and rubber are insulators and protect us from shocks", ["they make the wire conduct better", "they make the wire glow", "they make the wire heavier"], "The copper inside is a conductor."),
       ("Why is the handle of an electrician's screwdriver made of plastic?", "plastic is an insulator", ["plastic is a conductor", "plastic is shiny", "plastic is heavy"], "It protects from electric shocks."),
       ("Why should we never touch switches with wet hands?", "water with impurities conducts electricity and can give a shock", ["water is an insulator", "it damages the switch only", "it makes the bulb brighter"], "Always dry hands first."),
       ("What happens to the brightness of a bulb when two cells are used in place of one (correctly joined)?", "it glows brighter", ["it stops glowing", "it glows dimmer", "it does not change"], "Two cells give more energy."),
       ("How should two cells be joined to make a battery?", "the positive terminal of one to the negative terminal of the next", ["positive to positive", "negative to negative", "both in a beaker of water"], "Otherwise they work against each other."),
       ("Which device converts chemical energy into electrical energy?", "an electric cell", ["a bulb", "a switch", "a fuse"], "A bulb converts electrical energy to light and heat."),
       ("Which part of a torch completes the circuit when you press it?", "the switch", ["the reflector", "the glass cover", "the plastic body"], "It joins the wires."),
       ("Why is it unsafe to experiment with the mains supply at home?", "it has a very high voltage that can kill", ["it is too weak to do anything", "it is the same as a cell", "it has no current"], "Use cells for experiments."),
       ("What is the symbol of an electric cell made of?", "a long thin line and a short thick line", ["a circle with a cross", "a zigzag line", "two parallel equal lines"], "The long line is the positive terminal."),
       ("What does the circuit symbol of a bulb look like?", "a circle with a cross inside", ["a long and a short line", "a gap in a line", "a straight line"], "The cross shows the filament."),
       ("Why does a bulb get hot after glowing for a while?", "the filament gets heated by the current", ["the glass makes heat", "cold air enters it", "the switch heats it"], "Some energy is lost as heat."),
       ("Why does a dry cell stop working after some time?", "the chemicals in it are used up", ["it fills with air", "it becomes a magnet", "the case melts"], "Dispose of used cells safely."),
       ("Which material is used for the filament of many bulbs?", "tungsten", ["copper", "plastic", "glass"], "It has a very high melting point."),
       ("Why are LED bulbs better than old filament bulbs?", "they use less electricity and last longer", ["they use more electricity", "they get hotter", "they need no current"], "LEDs save energy."),
       ("A circuit has a bulb but no cell. Will the bulb glow?", "no, there is no source of electricity", ["yes, always", "yes, if the switch is on", "only at night"], "A cell or battery is needed."),
       ("What is a 'tester' used for in a circuit?", "checking whether a material conducts electricity", ["measuring length", "measuring temperature", "measuring mass"], "Put the material in the gap; the bulb glows if it conducts.")]


def c_ckt(k=None):
    R = _R[0]
    n = R.choice([1, 2, 3])
    sw = R.choice(["ON (closed)", "OFF (open)"])
    gap = R.choice(["a copper wire", "a steel spoon", "an iron nail", "a rubber eraser", "a plastic ruler", "a wooden stick", "an aluminium key", "a glass bangle", "a pencil lead (graphite)", "a paper strip"])
    con = gap in ("a copper wire", "a steel spoon", "an iron nail", "an aluminium key", "a pencil lead (graphite)")
    a = "yes" if (sw.startswith("ON") and con) else "no"
    why = ("the switch is open" if sw.startswith("OFF") else "%s is an insulator" % gap) if a == "no" else "the circuit is complete and %s conducts" % gap
    return tq("A circuit has %d cell%s, a bulb and a switch that is %s. The two free ends of the wires touch %s. Does the bulb glow?" % (n, "" if n == 1 else "s", sw, gap), a,
              ["yes" if a == "no" else "no", "only if a magnet is near", "only in the dark"], "The bulb glows only if the circuit is closed and every part conducts. Here: %s." % why)


# =================================================================== Chapter 4: metals and non-metals
MET = {"a metal": ["iron", "copper", "aluminium", "gold", "silver", "zinc", "magnesium", "sodium", "mercury", "potassium", "calcium", "lead", "tin"],
       "a non-metal": ["carbon", "sulphur", "oxygen", "nitrogen", "phosphorus", "iodine", "chlorine", "hydrogen", "bromine", "helium", "neon"]}
PROPM = {"a property of most metals": ["they are lustrous (shiny)", "they can be beaten into sheets", "they can be drawn into wires", "they make a ringing sound when struck",
                                       "they conduct heat well", "they conduct electricity well"],
         "a property of most non-metals": ["they are dull", "they are brittle", "they do not conduct heat well", "they do not conduct electricity (except graphite)",
                                           "they form acidic oxides", "many of them are gases at room temperature"]}
PROPS = [("malleability", "being beaten into thin sheets"), ("ductility", "being drawn into thin wires"), ("lustre", "a shiny surface"),
         ("sonority", "making a ringing sound when struck"), ("conductivity", "letting heat and electricity pass through easily"), ("brittleness", "breaking into pieces when hammered")]
MUSE = [("aluminium", "making foil for wrapping food and bodies of aircraft"), ("copper", "making electric wires"), ("iron", "making rails, bridges and machines"),
        ("gold", "making jewellery that does not tarnish"), ("mercury", "a liquid metal once used in thermometers"), ("zinc", "coating iron to stop rusting (galvanisation)"),
        ("tungsten", "the filament of bulbs"), ("silver", "jewellery and the thin foil (varq) on sweets"), ("carbon (graphite)", "the lead of pencils"),
        ("oxygen", "breathing and burning"), ("sulphur", "making matches and medicines for skin"), ("chlorine", "making water safe to drink")]
MNM = [("Which metal is a liquid at room temperature?", "mercury", ["iron", "copper", "sodium"], "Bromine is a liquid non-metal."),
       ("Which non-metal is a good conductor of electricity?", "graphite (a form of carbon)", ["sulphur", "oxygen", "iodine"], "It is used in pencil leads and electrodes."),
       ("Which non-metal is lustrous?", "iodine", ["sulphur", "phosphorus", "nitrogen"], "Most non-metals are dull."),
       ("Which metal is so soft that it can be cut with a knife?", "sodium", ["iron", "copper", "gold"], "Potassium is also soft."),
       ("Why is sodium stored under kerosene?", "it reacts very fast with air and water", ["it is a liquid", "it melts easily", "it is a non-metal"], "It can catch fire in water."),
       ("Why is phosphorus stored in water?", "it catches fire when exposed to air", ["it reacts with water", "it melts in air", "it is a metal"], "Water keeps air away from it."),
       ("What forms when iron is exposed to moist air for a long time?", "rust (iron oxide)", ["copper sulphate", "salt", "sugar"], "Rusting needs both oxygen and water."),
       ("What two things are needed for iron to rust?", "oxygen (air) and water (moisture)", ["only sunlight", "only carbon dioxide", "only heat"], "Iron in dry air does not rust."),
       ("How can rusting of iron be prevented?", "by painting, oiling or galvanising it", ["by keeping it wet", "by heating it in water", "by salting it"], "These keep air and water away."),
       ("What is the nature of the oxide formed when magnesium burns?", "basic: it turns red litmus blue", ["acidic: it turns blue litmus red", "neutral", "it does not dissolve at all"], "Metal oxides are basic."),
       ("What is the nature of the oxide formed when sulphur burns?", "acidic: it turns blue litmus red", ["basic: it turns red litmus blue", "neutral", "it is a metal"], "Non-metal oxides are usually acidic."),
       ("What do you see when magnesium ribbon burns?", "a brilliant white flame and a white powder", ["a blue flame and a black liquid", "no flame at all", "a green gas"], "The white powder is magnesium oxide."),
       ("Why are cooking pots made of metal but handles of plastic or wood?", "metals conduct heat; plastic and wood do not", ["metals are insulators", "plastic conducts heat well", "wood is a metal"], "This protects our hands."),
       ("Why are bells made of metals?", "metals are sonorous", ["metals are brittle", "metals are dull", "metals are poor conductors"], "Wooden bells would not ring."),
       ("Why does gold jewellery stay shiny for years?", "gold does not react with air and water", ["gold reacts quickly", "gold is a non-metal", "gold is soft"], "Iron would rust."),
       ("What is galvanisation?", "coating iron with a thin layer of zinc to stop rusting", ["melting iron", "painting gold", "mixing copper and tin"], "Galvanised iron is used for buckets and pipes."),
       ("Which green coating forms on copper vessels over time?", "basic copper carbonate", ["rust", "salt", "silver oxide"], "It can be cleaned with lemon or tamarind."),
       ("Why are copper vessels cleaned with tamarind or lemon?", "their acids remove the green coating", ["they make the copper rust", "they add a coating", "they make it magnetic"], "Acids react with the basic coating."),
       ("What is an alloy?", "a mixture of a metal with other metals or non-metals", ["a pure metal", "a non-metal only", "a gas"], "Steel, brass and bronze are alloys."),
       ("Which alloy is made of copper and zinc?", "brass", ["bronze", "steel", "solder"], "Bronze is copper and tin."),
       ("Why is stainless steel used for kitchen sinks and spoons?", "it does not rust easily", ["it is very soft", "it conducts no heat", "it is a non-metal"], "It contains iron, chromium and nickel."),
       ("What happens when a non-metal is hammered?", "it usually breaks into pieces", ["it becomes a thin sheet", "it becomes a wire", "it starts to ring"], "Non-metals are brittle."),
       ("Which property allows copper to be made into electric wires?", "ductility", ["brittleness", "sonority only", "dullness"], "It is also a good conductor."),
       ("Which property allows aluminium to be made into thin foil?", "malleability", ["brittleness", "ductility only", "dullness"], "Metals can be beaten into sheets."),
       ("What happens when sodium is put in water?", "it reacts violently, giving off hydrogen gas", ["nothing happens", "it dissolves like sugar", "it turns into iron"], "Never do this without a teacher."),
       ("Why is aluminium used to make aircraft bodies?", "it is light and strong and does not rust", ["it is very heavy", "it is a non-metal", "it is a liquid"], "Its alloys are used too."),
       ("Which non-metal is essential for breathing?", "oxygen", ["sulphur", "carbon", "iodine"], "Living things need oxygen for respiration."),
       ("Which non-metal is used in a solution to disinfect wounds?", "iodine", ["sulphur", "phosphorus", "nitrogen"], "Tincture of iodine is an antiseptic."),
       ("Which form of carbon is the hardest natural substance?", "diamond", ["graphite", "coal", "charcoal"], "Graphite is soft and slippery."),
       ("What is the nature of the solution formed when the oxide of a metal dissolves in water?", "basic", ["acidic", "neutral", "it does not dissolve"], "Magnesium oxide gives magnesium hydroxide."),
       ("What do we call metals like gold and silver that do not react easily?", "noble metals", ["active metals", "non-metals", "alloys"], "They keep their shine.")]

# =================================================================== Chapter 5: physical and chemical changes
CHG = {"a physical change": ["melting of ice", "dissolving sugar in water", "tearing paper", "folding a cloth", "breaking a glass", "freezing water", "chopping wood", "stretching a rubber band", "boiling water", "crushing a can", "melting butter", "making a paper boat", "grinding wheat into flour", "mixing sand and water", "condensing steam"],
       "a chemical change": ["burning of paper", "rusting of iron", "cooking an egg", "curdling of milk", "ripening of fruit", "baking a cake", "digestion of food", "burning a candle wick", "souring of milk", "a cut apple turning brown", "burning of coal", "frying a papad", "making curd from milk", "fermenting idli batter", "burning a cracker"]}
SPEED = {"a slow change": ["rusting of iron", "ripening of mangoes", "growth of a tree", "formation of soil from rocks", "souring of milk"],
         "a fast change": ["burning of a matchstick", "bursting of a cracker", "lighting a gas stove", "popping of a balloon", "breaking of a glass"]}
DES = {"a desirable change": ["cooking food", "digestion of food", "ripening of fruit", "making curd", "growth of crops", "baking bread", "making compost", "germination of seeds"],
       "an undesirable change": ["rusting of a gate", "spoiling of food", "fading of paint on a wall", "forest fires", "decay of teeth", "rotting of fruit in storage", "tarnishing of silver", "spread of mould on bread"]}
SIGN = {"a sign of a chemical change": ["a new substance is formed", "a gas is given off, as when vinegar and baking soda mix", "heat or light is given out, as in burning",
                                       "a permanent colour change, as when an apple slice turns brown", "a new smell is produced, as when food goes bad", "a solid forms when two solutions are mixed"],
        "true of a physical change": ["only the shape, size or state changes", "no new substance is formed", "it can usually be reversed easily, as when ice melts",
                                      "the substance keeps its chemical properties", "it happens when sugar dissolves in water", "it happens when wax melts"]}
PCQ = [("What forms when vinegar is added to baking soda?", "carbon dioxide gas (bubbles)", ["oxygen gas only", "hydrogen gas only", "no gas at all"], "Carbon dioxide turns lime water milky."),
       ("What happens when carbon dioxide is passed through lime water?", "the lime water turns milky", ["it turns blue", "it boils", "nothing happens"], "Calcium carbonate forms."),
       ("What is crystallisation?", "getting pure crystals of a substance from its solution", ["burning a substance", "rusting of iron", "breaking glass"], "Large crystals of copper sulphate can be made this way."),
       ("Why is crystallisation better than evaporation for getting pure salt?", "impurities stay in the solution and crystals are pure", ["it is faster", "it uses no water", "it gives coloured salt"], "Evaporation leaves impurities with the salt."),
       ("What colour is the deposit formed on an iron nail kept in copper sulphate solution?", "brownish (copper)", ["silver", "green", "white"], "The blue solution turns green."),
       ("What happens to the blue colour of copper sulphate solution when an iron nail is dipped in it?", "it turns green", ["it turns red", "it becomes colourless at once", "it turns black"], "Iron sulphate forms."),
       ("Why is rusting called an undesirable change?", "it weakens iron objects and wastes iron", ["it makes iron stronger", "it is a physical change", "it is easily reversed"], "Bridges and ships must be protected."),
       ("Which is a desirable chemical change?", "cooking food", ["rusting of a gate", "spoiling of food", "the fading of paint"], "It makes food tasty and easier to digest."),
       ("Which change is slow?", "rusting of iron", ["burning of a matchstick", "bursting of a cracker", "lighting a gas stove"], "It takes days or weeks."),
       ("Which change is fast?", "burning of a matchstick", ["rusting of iron", "growing of a tree", "ripening of mangoes"], "It happens in a second."),
       ("Why is the melting of wax a physical change, while burning wax is a chemical change?", "melted wax can become solid again, but burning forms new gases", ["both form new substances", "neither changes anything", "melting forms carbon dioxide"], "A candle shows both changes."),
       ("Why is the curdling of milk a chemical change?", "curd is a new substance with different properties", ["milk only changes its shape", "it can easily become milk again", "no change happens"], "Curd tastes sour."),
       ("Why is dissolving sugar in water a physical change?", "the sugar can be got back by evaporating the water", ["it forms a new gas", "it releases light", "it cannot be reversed"], "No new substance forms."),
       ("What is a reversible change?", "a change that can be undone, such as freezing water", ["a change that always forms a new substance", "burning paper", "cooking rice"], "Most physical changes are reversible."),
       ("Which of these changes is irreversible?", "baking bread", ["melting butter", "freezing water", "folding paper"], "We cannot get back the dough."),
       ("What is the gas used by fire extinguishers made from vinegar and baking soda?", "carbon dioxide", ["oxygen", "nitrogen", "hydrogen"], "It does not support burning."),
       ("Why does a cut apple turn brown?", "substances in it react with oxygen in the air", ["it absorbs water", "it melts", "it freezes"], "Lemon juice slows this."),
       ("Why is the formation of a cloud a physical change?", "water vapour changes into tiny drops; no new substance forms", ["water burns", "new gases form", "it cannot be reversed"], "Only the state changes."),
       ("Why does iron rust faster in coastal areas?", "the air is moist and contains salt", ["the air is very dry", "there is no oxygen", "the Sun is weaker"], "Salt speeds up rusting."),
       ("What is the chemical name of rust?", "iron oxide", ["iron sulphate", "copper oxide", "calcium carbonate"], "It forms from iron, oxygen and water."),
       ("Why do we see bubbles when lemon juice is added to baking soda?", "a gas (carbon dioxide) is formed", ["the juice boils", "oxygen leaves the lemon", "the soda melts"], "It is a chemical change."),
       ("Which change happens when a glass of water is left in the freezer?", "a physical change: water freezes into ice", ["a chemical change: ice is a new substance", "no change", "rusting"], "Ice can melt back to water."),
       ("Which crystals can be grown at home from a strong solution of alum or sugar?", "large, clear crystals", ["rust", "carbon dioxide", "charcoal"], "Cooling the hot solution slowly helps."),
       ("Why is burning a candle both a physical and a chemical change?", "the wax melts (physical) and burns to form new gases (chemical)", ["it is only physical", "it is only chemical", "it is neither"], "Both happen at once.")]


def c_chg(k=None):
    R = _R[0]
    lab = R.choice(sorted(CHG))
    x = R.choice(CHG[lab])
    other = "a chemical change" if lab == "a physical change" else "a physical change"
    return tq("Is %s a physical change or a chemical change?" % x, lab, [other, "neither a physical nor a chemical change", "both a physical and a chemical change"],
              "%s: %s, because %s." % (_cap(x), lab, "a new substance forms" if lab == "a chemical change" else "no new substance forms"))


# =================================================================== Chapter 6: adolescence
ADOL = [("What is adolescence?", "the stage of life between childhood and adulthood, from about 11 to 19 years", ["the first year of life", "old age", "the time before birth"], "It is often called the teenage years."),
        ("What is puberty?", "the time when the body begins to change towards an adult body", ["the end of growth", "an illness", "a kind of food"], "It happens at different ages for different people."),
        ("Why should adolescents not worry if they grow at a different pace from their friends?", "everyone's body changes at its own pace", ["growth stops after age 10", "only boys grow", "growth depends only on clothes"], "Differences are normal."),
        ("What is a growth spurt?", "a period of very fast increase in height", ["a disease of bones", "a loss of weight", "a kind of exercise"], "It often happens in early adolescence."),
        ("Why does the voice of many boys become deeper in adolescence?", "the voice box (larynx) grows bigger", ["they shout more", "they drink cold water", "their teeth fall out"], "The growing voice box can be seen as the Adam's apple."),
        ("Which chemical messengers bring about the changes of puberty?", "hormones", ["vitamins", "enzymes in food", "minerals in water"], "They are made by glands and carried in blood."),
        ("Why do pimples (acne) often appear in adolescence?", "skin glands become more active", ["eating too much fruit", "drinking water", "sleeping early"], "Washing the face gently helps."),
        ("Why is personal hygiene especially important in adolescence?", "sweat glands become more active and body odour can develop", ["the body stops sweating", "germs cannot grow on teenagers", "bathing is harmful"], "Bathe daily and wear clean clothes."),
        ("Why do adolescents need a balanced diet rich in protein, iron and calcium?", "their bodies are growing quickly", ["they stop growing", "they need only sugar", "they need no food"], "Milk, pulses, green vegetables and fruits help."),
        ("Why is iron especially important in an adolescent's diet?", "it helps make blood and prevents anaemia", ["it makes bones soft", "it causes pimples", "it gives no benefit"], "Green leafy vegetables, jaggery and dates have iron."),
        ("What is a good way to deal with mood changes in adolescence?", "talking to parents, teachers or trusted adults and staying active", ["keeping all worries secret", "skipping meals", "staying awake all night"], "Feelings change because of hormones and growth."),
        ("Why should adolescents say no to tobacco, alcohol and drugs?", "they damage health and can become habits that are hard to stop", ["they make people taller", "they improve memory", "they are part of a balanced diet"], "Seek help from a trusted adult if pressured."),
        ("Why is regular exercise good for adolescents?", "it builds strong muscles and bones and improves mood", ["it stops growth", "it causes acne", "it makes bones weak"], "Outdoor games are a good choice."),
        ("Why is enough sleep important during adolescence?", "the body grows and repairs itself during sleep", ["sleep stops growth", "sleep is not needed by teenagers", "sleep causes illness"], "About 8–10 hours is good for teenagers."),
        ("What is peer pressure?", "the influence of friends to do something", ["the pressure of air", "a kind of exercise", "a type of food"], "It can be good or bad; think before you act."),
        ("Why is junk food not good for growing adolescents?", "it is high in fat, salt and sugar and low in nutrients", ["it is rich in protein", "it has all vitamins", "it makes bones stronger"], "Choose fruits, nuts and home-cooked food."),
        ("Which of these is a change seen in both boys and girls during adolescence?", "an increase in height", ["a deeper voice in everyone", "no change at all", "loss of teeth"], "Both grow taller and gain weight."),
        ("Why do adolescents often feel more independent?", "the brain and emotions are developing as they grow up", ["they stop learning", "they have no feelings", "they are adults already"], "This is a normal part of growing up."),
        ("Where can an adolescent get reliable information about body changes?", "parents, teachers, doctors and school health programmes", ["rumours from strangers", "random social media posts", "nowhere"], "Ask trusted adults."),
        ("Why should we be kind and not tease friends about their body changes?", "everyone goes through changes and teasing hurts", ["changes are funny", "teasing helps growth", "only some people change"], "Respect and support each other."),
        ("What is the life stage after adolescence?", "adulthood", ["infancy", "childhood", "toddlerhood"], "Growth slows down in adulthood."),
        ("Which mineral is needed for strong bones during the growth spurt?", "calcium", ["sodium", "iodine only", "fluorine only"], "Milk, ragi and curd are rich in calcium."),
        ("Why should adolescents drink plenty of water?", "it keeps the body healthy and helps it work properly", ["it stops growth", "it gives a lot of fat", "it causes pimples"], "Avoid too many sugary drinks."),
        ("Which gland makes the growth hormone?", "the pituitary gland", ["the stomach", "the lungs", "the teeth"], "It is at the base of the brain."),
        ("How are hormones carried around the body?", "in the blood", ["through the air we breathe", "in the bones", "in the food pipe only"], "They act on organs far from where they are made."),
        ("Why should acne not be squeezed?", "it can cause infection and leave marks", ["it makes the skin smooth", "it cures it faster", "it is a good habit"], "Keep the face clean instead."),
        ("Why do growing adolescents often feel very hungry?", "the body needs more energy and nutrients for growth", ["their stomach is smaller", "they need less food", "they are always ill"], "Choose nutritious snacks."),
        ("What should an adolescent do if a friend offers tobacco or drugs?", "say no firmly and tell a trusted adult", ["try it once", "keep it a secret", "pass it on to others"], "Real friends respect your choice."),
        ("Why is too much screen time unhealthy for adolescents?", "it reduces sleep and physical activity", ["it improves eyesight", "it makes muscles stronger", "it gives vitamins"], "Take breaks and play outdoors."),
        ("Which of these helps keep teeth healthy in adolescence?", "brushing twice a day and eating less sugar", ["eating sweets at night", "never brushing", "drinking cold drinks often"], "Visit a dentist regularly."),
        ("Why is breakfast important for adolescents?", "it gives energy to study and play after the night's fast", ["it makes them sleepy", "it stops growth", "it has no use"], "Include fruit, milk or sprouts."),
        ("How do feelings often change during adolescence?", "moods can change quickly, and new feelings of independence grow", ["feelings stop completely", "adolescents feel nothing", "only happiness is felt"], "This is normal; talking helps."),
        ("What is the role of a school counsellor?", "to listen and give guidance on worries and feelings", ["to give marks", "to punish students", "to teach only maths"], "Asking for help is a sign of strength."),
        ("Why do the shoulders of boys and the hips of girls often broaden in adolescence?", "the body shape changes as it grows towards an adult body", ["they eat more sugar", "they stop exercising", "they sleep less"], "These are normal changes of puberty."),
        ("Why is it important to change out of sweaty clothes after sports?", "germs that cause odour and skin infections grow in sweat", ["sweat is good for clothes", "it makes muscles grow", "it saves water"], "Wash sports clothes regularly."),
        ("Which food helps an adolescent get protein?", "pulses, milk, eggs, soybean or paneer", ["sugar", "oil", "candies"], "Protein builds muscles and tissues."),
        ("Why should adolescents avoid crash diets?", "growing bodies need regular, balanced meals", ["crash diets add nutrients", "growth stops at 12", "skipping meals builds muscles"], "Eat a variety of foods."),
        ("What is a good way to manage stress before exams?", "plan study time, sleep well, exercise and talk to someone", ["stay awake all night", "skip meals", "keep worries to yourself"], "Breaks help the brain."),
        ("Why does height increase faster during adolescence?", "the long bones grow quickly during the growth spurt", ["bones stop growing", "muscles turn into bones", "the skull grows"], "Most growth in height ends by the late teens."),
        ("Why should adolescents not compare their height with friends and worry?", "height depends on genes, food and the age when growth starts", ["height depends only on shoes", "everyone grows by the same amount", "height never changes"], "Most people catch up."),
        ("Which of these is a healthy snack for a growing teenager?", "a handful of roasted chana and a fruit", ["a packet of chips", "a sugary cold drink", "a chocolate bar every hour"], "It gives protein, fibre and vitamins."),
        ("Why does the body sweat more during adolescence?", "sweat glands become more active", ["the body stops sweating", "teenagers drink less water", "the skin becomes thicker"], "Daily bathing helps."),
        ("What is the main reason adolescents may feel sleepy in class after staying up late?", "the body did not get enough rest to grow and repair", ["they ate too much fruit", "they exercised too much", "they drank too much water"], "Sleep at a regular time."),
        ("Which of these is a sign of good emotional health?", "being able to talk about feelings and ask for help", ["hiding all feelings", "never trusting anyone", "staying alone all the time"], "Friends and family can support you."),
        ("Why do adolescents need more energy than younger children?", "they grow fast and are usually more active", ["they grow slower", "they rest all day", "they need no food"], "Choose energy-giving whole grains."),
        ("Why is outdoor play good for adolescents?", "it builds fitness, gives sunlight for vitamin D and reduces stress", ["it stops growth", "it causes acne", "it weakens bones"], "Try to play every day.")]
FOODS = [("milk, curd and ragi", "calcium for strong bones"), ("green leafy vegetables and jaggery", "iron for healthy blood"), ("pulses, eggs and paneer", "protein for growth of muscles and tissues"),
         ("amla, guava and oranges", "vitamin C for healthy gums and skin"), ("whole grains and millets", "energy and fibre"), ("iodised salt", "iodine for the thyroid gland"),
         ("sunlight on the skin", "vitamin D for bones"), ("plenty of water", "keeping the body cool and removing wastes"), ("nuts and seeds such as groundnuts", "healthy fats and protein"), ("carrots and papaya", "vitamin A for good eyesight")]
HYG = [("after playing a sweaty game", "take a bath and change into clean clothes"), ("when pimples appear on the face", "wash the face gently and do not squeeze them"),
       ("when you feel worried or confused", "talk to a parent, teacher or counsellor"), ("before eating food", "wash hands with soap and water"),
       ("at bedtime", "keep phones away and sleep for 8–10 hours"), ("when a friend offers tobacco", "say no and walk away"),
       ("when feeling tired and low on energy", "eat balanced meals and check iron intake"), ("on a hot day of sports practice", "drink plenty of water"),
       ("after using the toilet", "wash hands with soap"), ("when your hair feels oily", "wash it regularly with a mild shampoo"),
       ("after a meal at night", "brush your teeth before sleeping"), ("when you have to sit and study for hours", "take short breaks to stretch and move"),
       ("if you feel pressured by friends to do something harmful", "think for yourself and say no"), ("when choosing snacks", "pick fruits, nuts or sprouts instead of fried food")]
STAGE = [("infancy", "the first year or so of life"), ("toddlerhood", "about 1 to 3 years, when a child learns to walk and talk"), ("childhood", "from about 3 years until puberty begins"), ("adolescence", "about 11 to 19 years, between childhood and adulthood"),
         ("adulthood", "after adolescence, when growth is complete"), ("old age", "the later years of adult life")]
HEALTH = {"a healthy habit for an adolescent": ["eating fruits and green vegetables", "bathing every day", "sleeping 8–10 hours", "playing outdoor games", "drinking plenty of water",
                                                "talking to a trusted adult about worries", "brushing teeth twice a day", "wearing clean, dry clothes", "washing hands before meals", "taking breaks from screens", "eating sprouts and pulses"],
          "an unhealthy habit for an adolescent": ["skipping breakfast", "eating junk food every day", "staying up late on a phone", "trying tobacco", "sitting for hours without moving",
                                                  "skipping baths", "drinking sugary cold drinks often", "keeping all worries secret", "eating fried snacks every evening", "sleeping at very irregular times", "squeezing pimples"]}


def UNITS7a():
    b = {k: once_maker(v) for k, v in [("evol", EVOL), ("neut", NEUT), ("ckt", CKT), ("mnm", MNM), ("pcq", PCQ), ("adol", ADOL)]}
    meth = pairs(METHOD, "A student is %s. Which example fits this step?", "Which step of the scientific method is this: %s?")
    claim = odd_one(CLAIM, "Which of these is %s?", "Which of these is not %s?")
    disc = pairs(DISC, "What is %s known for?", "Which scientist is known for %s?")
    subst = odd_one(SUBST, "Which of these is %s?", "Which of these is not %s?")
    acids = pairs(ACIDS, "Which acid is found in %s?", "Which of these contains %s?")
    comp = pairs(COMP, "What is the job of %s in a circuit?", "Which part of a circuit is described here: %s?")
    cond = odd_one(COND, "Which of these is %s?", "Which of these is not %s?")
    met = odd_one(MET, "Which of these elements is %s?", "Which of these elements is not %s?")
    props = pairs(PROPS, "What is %s?", "Which property means %s?")
    muse = pairs(MUSE, "What is %s used for?", "Which element is used for %s?")
    sign = odd_one(SIGN, "Which of these is %s?", "Which of these is not %s?")
    chg = odd_one(CHG, "Which of these is %s?", "Which of these is not %s?")
    stage = pairs(STAGE, "When is %s?", "Which stage of life is %s?")
    health = odd_one(HEALTH, "Which of these is %s?", "Which of these is not %s?")
    foods = pairs(FOODS, "What do %s mainly give a growing body?", "Which foods give %s?")
    hyg = pairs(HYG, "What is a good thing to do %s?")
    propm = odd_one(PROPM, "Which of these is %s?", "Which of these is not %s?")
    speed = odd_one(SPEED, "Which of these is %s?", "Which of these is not %s?")
    des = odd_one(DES, "Which of these is %s?", "Which of these is not %s?")
    return [
        U(1, "the-ever-evolving-world-of-science", 1, NS,
          "Science as a process that keeps growing and changing with new evidence; observation, questions, hypotheses, experiments, analysis and conclusions; contributions of scientists including those from India; scientific attitude and evidence versus belief (summary of NCERT Curiosity Chapter 1).",
          "The Ever-Evolving World of Science", "the ever-evolving world of science",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 1: the scientific method, evidence, how scientific ideas change, Indian scientists and a scientific attitude. 100 questions with answers.",
          "Scientific ideas change when new evidence is found.", "Observe, question, hypothesise, test, analyse, conclude.",
          "<p>Science is not a fixed list of facts. Scientists observe, ask questions, form a hypothesis, test it with experiments, analyse the results and draw conclusions. When new evidence appears, ideas are tested again and improved, as when the idea that the Sun goes round the Earth was replaced.</p>"
          "<p>New instruments such as the telescope and the microscope opened new worlds. A scientific attitude means being curious, open-minded and asking for evidence, so we can tell tested claims from superstitions.</p>",
          [("'A black cat brings bad luck.' Is there evidence?", ["it has never been shown by fair tests"], "no: it is a superstition"), ("Keeping nails in salt water and plain water for a week is…", ["a fair test"], "an experiment")],
          ["Thinking scientific ideas never change.", "Treating a popular belief as evidence.", "Changing results to fit a hypothesis."],
          [("Why does science keep changing?", "New observations, better instruments and new experiments give evidence that can confirm, improve or replace old ideas."),
           ("What is a hypothesis?", "A possible explanation that can be tested by an experiment.")],
          lambda: [("Science keeps evolving", [(b["evol"], 14), (claim, 6)]), ("The scientific method", [(meth, 8), (c_var, 12)]), ("Evidence and claims", [(claim, 8), (b["evol"], 6), (disc, 6)]),
                   ("Scientists and discoveries", [(disc, 14), (b["evol"], 4), (c_var, 2)]), ("Mixed problems", [(c_var, 14), (meth, 2), (b["evol"], 4)])]),
        U(2, "exploring-substances-acidic-basic-and-neutral", 2, MT,
          "Acids, bases and neutral substances in daily life; natural and laboratory indicators such as litmus, turmeric and china rose; neutralisation and its uses in daily life: indigestion, ant bites, soil treatment and factory waste (summary of NCERT Curiosity Chapter 2).",
          "Exploring Substances: Acidic, Basic and Neutral", "acidic, basic and neutral substances",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 2: acids, bases and neutral substances, litmus, turmeric and china rose indicators, and neutralisation in daily life. 100 questions with answers.",
          "Acids turn blue litmus red; bases turn red litmus blue.", "Acid + base → salt + water + heat.",
          "<p>Acidic substances such as lemon juice, vinegar and curd taste sour; basic substances such as soap and baking soda feel soapy. Neutral substances such as sugar solution and distilled water are neither. We never taste unknown substances; we test them with indicators.</p>"
          "<p>Acids turn blue litmus red and china rose dark pink; bases turn red litmus blue, turmeric red and china rose green. An acid and a base neutralise each other to form a salt and water, giving out heat. We use this for indigestion (antacids), ant stings (baking soda) and acidic soil (lime).</p>",
          [("Soap solution on turmeric paper?", ["soap is basic"], "it turns red"), ("Soil is too acidic. Add…", ["a base neutralises it"], "slaked lime or quicklime")],
          ["Thinking turmeric changes colour in acids.", "Saying red litmus turns blue in acid.", "Tasting a substance to test it."],
          [("What is neutralisation?", "The reaction between an acid and a base, which gives a salt and water and releases heat."),
           ("Why is baking soda rubbed on an ant sting?", "The sting contains formic acid; baking soda is a base and neutralises it.")],
          lambda: [("Acidic, basic and neutral", [(subst, 14), (acids, 6)]), ("Natural acids around us", [(acids, 4), (subst, 8), (b["neut"], 8)]), ("Indicators", [(c_ind, 18), (c_ind2, 2)]),
                   ("Neutralisation in daily life", [(b["neut"], 14), (c_ind, 6)]), ("Mixed problems", [(c_ind, 14), (subst, 6)])]),
        U(3, "electricity-circuits-and-their-components", 3, PH,
          "Electric cell and battery, bulb and its filament, switch, closed and open circuits; circuit diagrams with symbols; conductors and insulators; safety with electricity; LEDs (summary of NCERT Curiosity Chapter 3).",
          "Electricity: Circuits and their Components", "electric circuits",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 3: cells, batteries, bulbs, switches, open and closed circuits, circuit symbols, conductors and insulators and electrical safety. 100 questions with answers.",
          "Current flows only in a closed circuit.", "Conductors let current pass; insulators do not.",
          "<p>An electric cell has a positive and a negative terminal. When a cell, wires, a switch and a bulb make a complete path, the circuit is closed and current flows, so the bulb's filament glows. If there is a gap (an open switch or a broken filament), the circuit is open and no current flows.</p>"
          "<p>Metals such as copper, iron and aluminium, and graphite, are conductors; rubber, plastic, wood and glass are insulators. Two cells joined positive to negative make a battery and a brighter bulb. Never touch switches with wet hands or play with the mains supply.</p>",
          [("Switch OFF: does the bulb glow?", ["the circuit is open"], "no"), ("A rubber eraser in the gap?", ["rubber is an insulator"], "the bulb does not glow")],
          ["Thinking a bulb glows when the circuit has a gap.", "Calling graphite an insulator.", "Joining cells positive to positive."],
          [("What is the difference between an open and a closed circuit?", "A closed circuit is a complete path, so current flows; an open circuit has a gap, so no current flows."),
           ("Why are wires covered with plastic?", "Plastic is an insulator and protects us from electric shocks.")],
          lambda: [("Cells, bulbs and switches", [(comp, 14), (b["ckt"], 6)]), ("Open and closed circuits", [(c_ckt, 12), (b["ckt"], 8)]), ("Conductors and insulators", [(cond, 16), (c_ckt, 4)]),
                   ("Circuit diagrams and safety", [(cond, 8), (c_ckt, 10), (comp, 2)]), ("Mixed problems", [(c_ckt, 14), (cond, 4), (b["ckt"], 2)])]),
        U(4, "the-world-of-metals-and-non-metals", 4, MT,
          "Physical properties of metals and non-metals: lustre, hardness, malleability, ductility, sonority and conductivity; reactions with oxygen (basic and acidic oxides) and with water; rusting and its prevention; uses of metals and non-metals (summary of NCERT Curiosity Chapter 4).",
          "The World of Metals and Non-metals", "metals and non-metals",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 4: properties of metals and non-metals, malleability and ductility, metal and non-metal oxides, rusting and its prevention, and their uses. 100 questions with answers.",
          "Metals are shiny, malleable, ductile and conduct.", "Metal oxides are basic; non-metal oxides are acidic.",
          "<p>Metals such as iron, copper and aluminium are usually lustrous, hard, malleable (beaten into sheets), ductile (drawn into wires), sonorous and good conductors of heat and electricity. Non-metals such as sulphur, carbon and oxygen are usually dull and brittle, and do not conduct (graphite is an exception).</p>"
          "<p>Metals burn to form basic oxides (magnesium oxide turns red litmus blue); non-metals form acidic oxides (sulphur dioxide turns blue litmus red). Iron rusts in moist air; painting, oiling and galvanising prevent rusting.</p>",
          [("Copper is drawn into wires. Which property?", ["drawn into thin wires"], "ductility"), ("Burning sulphur: nature of the oxide?", ["non-metal oxide"], "acidic")],
          ["Thinking all non-metals are gases.", "Calling metal oxides acidic.", "Thinking iron rusts in dry air."],
          [("What is the difference between malleability and ductility?", "Malleability is being beaten into thin sheets; ductility is being drawn into thin wires."),
           ("How can rusting be prevented?", "By keeping air and moisture away: painting, oiling, greasing or coating with zinc (galvanising).")],
          lambda: [("Metals and non-metals", [(met, 14), (b["mnm"], 6)]), ("Physical properties", [(props, 8), (propm, 12)]), ("Reactions with oxygen and water", [(b["mnm"], 12), (propm, 8)]),
                   ("Uses of metals and non-metals", [(muse, 18), (met, 2)]), ("Mixed problems", [(met, 12), (b["mnm"], 6), (muse, 2)])]),
        U(5, "changes-around-us-physical-and-chemical", 5, MT,
          "Physical and chemical changes in daily life; signs of a chemical change; reversible and irreversible changes; crystallisation; rusting; desirable and undesirable, slow and fast changes (summary of NCERT Curiosity Chapter 5).",
          "Changes Around Us: Physical and Chemical", "physical and chemical changes",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 5: physical and chemical changes, signs of a chemical change, reversible and irreversible changes, crystallisation, rusting and the reaction of vinegar with baking soda. 100 questions with answers.",
          "A chemical change makes a new substance.", "A physical change alters only shape, size or state.",
          "<p>In a physical change, only properties such as shape, size or state change and no new substance forms: ice melts, paper is torn, sugar dissolves. In a chemical change, a new substance forms, often with a gas, heat, light, a colour change or a smell: paper burns, iron rusts, milk curdles.</p>"
          "<p>Vinegar and baking soda give carbon dioxide, which turns lime water milky. Pure crystals can be got from a solution by crystallisation. Some changes are desirable (cooking), some undesirable (rusting); some are slow, some fast.</p>",
          [("Is cooking an egg physical or chemical?", ["it cannot become a raw egg again", "new substances form"], "chemical"), ("CO₂ through lime water?", ["calcium carbonate forms"], "it turns milky")],
          ["Calling every reversible change chemical.", "Thinking dissolving is a chemical change.", "Forgetting that burning a candle shows both changes."],
          [("How can you tell a chemical change?", "A new substance forms, often shown by a gas, heat or light, a colour change or a new smell."),
           ("Why is the melting of wax physical but its burning chemical?", "Melted wax can become solid again; burning makes new substances such as carbon dioxide and water vapour.")],
          lambda: [("Physical changes", [(chg, 10), (c_chg, 10)]), ("Chemical changes", [(chg, 10), (sign, 6), (b["pcq"], 4)]), ("Signs of a chemical change", [(sign, 10), (b["pcq"], 4), (c_chg, 6)]),
                   ("Crystallisation and rusting", [(b["pcq"], 10), (des, 10)]), ("Slow, fast, desirable and undesirable", [(speed, 14), (des, 6)])]),
        U(6, "adolescence-a-stage-of-growth-and-change", 6, LW,
          "Adolescence and puberty; changes in the body during adolescence such as growth in height and changes in voice; role of hormones; personal hygiene; nutrition, exercise and sleep for adolescents; emotional health; saying no to harmful substances (summary of NCERT Curiosity Chapter 6).",
          "Adolescence: A Stage of Growth and Change", "adolescence",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 6: adolescence and puberty, growth spurts and voice changes, hormones, personal hygiene, healthy diet, exercise and sleep, and emotional health. 100 questions with answers.",
          "Adolescence is the bridge from childhood to adulthood.", "Hormones bring changes; everyone grows at their own pace.",
          "<p>Adolescence is the stage between childhood and adulthood, roughly from 11 to 19 years. During puberty, hormones bring changes such as a growth spurt, changes in the voice and more active skin and sweat glands. These changes happen at different ages in different people, and that is normal.</p>"
          "<p>Growing bodies need a balanced diet with protein, iron and calcium, regular exercise, enough sleep and good personal hygiene. Feelings may change quickly; talking to trusted adults helps. Say no to tobacco, alcohol and drugs.</p>",
          [("Why do pimples appear?", ["skin glands become more active"], "changes during puberty"), ("Which mineral prevents anaemia?", ["helps make blood"], "iron")],
          ["Thinking everyone should change at the same age.", "Skipping meals during the growth spurt.", "Keeping all worries secret."],
          [("What is adolescence?", "The stage of growth between childhood and adulthood, about 11 to 19 years, when the body and mind change."),
           ("Why is hygiene important in adolescence?", "Sweat and skin glands become more active, so daily bathing and clean clothes keep the body healthy and fresh.")],
          lambda: [("What is adolescence?", [(stage, 7), (b["adol"], 13)]), ("Changes during puberty", [(b["adol"], 12), (foods, 8)]),
                   ("Healthy habits", [(health, 14), (hyg, 6)]), ("Diet and well-being", [(foods, 4), (hyg, 4), (b["adol"], 8), (health, 4)]), ("Mixed problems", [(health, 8), (b["adol"], 6), (stage, 2), (hyg, 1), (foods, 3)])]),
    ]
