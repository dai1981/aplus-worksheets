# -*- coding: utf-8 -*-
"""Class 8 Science (NCERT Curiosity, chapters 1–7): question makers and UNITS8a()."""
from uk_alsci import tq, nf, once_maker
from in_sci import pairs, _R, U, K
from in_sci6a import NS, LW, MT, PH, ES, odd_one, nq, _cap
import in_sci

# =================================================================== Chapter 1: exploring the investigative world of science
INV = [("What is an investigation in science?", "a planned way of finding the answer to a question by collecting evidence", ["guessing an answer", "copying an answer from a friend", "reading only one book"], "It may include observing, measuring and experimenting."),
       ("What is the first thing to do when planning an investigation?", "decide the question to be answered", ["write the conclusion", "choose the result you want", "draw the graph"], "A clear question guides the plan."),
       ("Why do scientists keep a record of every step of an investigation?", "so that it can be checked and repeated by others", ["to make the work longer", "so nobody else can do it", "because results never change"], "Records also help find mistakes."),
       ("What is a variable?", "anything that can change in an investigation", ["something that never changes", "the name of the investigation", "the place where it is done"], "There are independent, dependent and controlled variables."),
       ("What is the independent variable?", "the one you change on purpose", ["the one you measure", "the ones you keep the same", "the final answer"], "In a plant test it might be the amount of light."),
       ("What is the dependent variable?", "the one you measure, which may change because of the independent variable", ["the one you change on purpose", "the one kept the same", "the scientist's name"], "In a plant test it might be the height of the plant."),
       ("What are controlled variables?", "the things kept the same so the test is fair", ["the things you change", "the results", "the conclusions"], "Pot size and amount of water could be controlled."),
       ("Why is a sample of many plants better than one plant in an experiment?", "one plant may behave unusually, so more plants give more reliable results", ["one plant is always enough", "more plants change the question", "it uses less soil"], "Bigger samples reduce chance effects."),
       ("Why do we take repeated readings and find the average?", "to reduce the effect of random errors", ["to make the result larger", "to change the result", "because the first reading is always wrong"], "The average is more reliable."),
       ("What is an inference?", "a conclusion drawn from observations and reasoning", ["a measurement", "a tool", "a question"], "Wet ground is an observation; 'it rained' is an inference."),
       ("Which is the best way to present how temperature changed over a day?", "a line graph", ["a single sentence", "a photograph of a thermometer", "a list of names"], "Line graphs show change over time."),
       ("Which is a good way to compare the number of students who like different fruits?", "a bar graph", ["a line graph of time", "a thermometer", "a map"], "Bar graphs compare categories."),
       ("Why should an investigation be safe?", "to avoid harm to people, animals and the environment", ["safety makes results wrong", "safety is only for adults", "it is not important"], "Wear goggles and follow your teacher."),
       ("What should be done with results that do not fit the pattern?", "check them carefully and repeat the measurement if possible", ["delete them without thinking", "change them to fit", "ignore the whole investigation"], "Odd results may show a mistake or something new."),
       ("What is a hypothesis?", "a testable explanation or prediction", ["a proven fact", "a graph", "a measuring tool"], "Experiments support or reject it."),
       ("Why is peer review important in science?", "other scientists check the work before it is accepted", ["it keeps results secret", "it makes experiments faster", "it stops new ideas"], "It helps catch errors."),
       ("A student finds that seeds sprout faster in warm water. What should she do next?", "repeat the test with more seeds to confirm it", ["stop and declare a new law", "change the result", "throw away her notes"], "Repetition builds confidence."),
       ("Why do scientists use units such as metres and seconds?", "so that everyone understands and can compare measurements", ["to make numbers bigger", "because they are pretty", "to confuse people"], "SI units are used all over the world."),
       ("Which of these is an observation rather than an inference?", "the leaves on the plant are drooping", ["the plant needs water", "the soil must be dry", "someone forgot to water it"], "An observation is what we notice directly."),
       ("What is a fair test?", "an investigation in which only one variable is changed and others are kept the same", ["a test with many changes", "a test with no measurements", "a guess"], "It shows the effect of one variable."),
       ("Which of these questions can be investigated scientifically?", "Does adding salt change the boiling point of water?", ["Is red the nicest colour?", "Which film is the best?", "Is Monday the worst day?"], "It can be answered by measuring."),
       ("What does 'reliable' mean for results?", "similar results are obtained when the test is repeated", ["the results are big numbers", "the results came first", "the results were guessed"], "Reliable results can be trusted."),
       ("What is an anomaly in a set of results?", "a result that does not fit the pattern of the others", ["the largest result", "the average", "the first result"], "Check how it happened."),
       ("Why is it useful to make a prediction before an experiment?", "it gives a clear idea to test", ["it guarantees the result", "it replaces the experiment", "it makes the experiment unnecessary"], "A wrong prediction still teaches us something."),
       ("What do we call a simplified picture or object that explains how something works?", "a model", ["a variable", "a sample", "a result"], "A globe is a model of the Earth.")]
VARS = [("Does the temperature of water change how much sugar dissolves?", "the temperature of the water", "the mass of sugar that dissolves", "the volume of water"),
        ("Does the length of a wire change how hot it gets when current flows?", "the length of the wire", "the rise in temperature of the wire", "the number of cells"),
        ("Does the number of turns in a coil change the strength of an electromagnet?", "the number of turns", "the number of pins it picks up", "the current and the iron core"),
        ("Does the surface change how far a toy car rolls?", "the type of surface", "the distance the car rolls", "the slope of the ramp"),
        ("Does the area of a brick's face change how deep it sinks into sand?", "the area of the face resting on the sand", "the depth of the dent in the sand", "the mass of the brick"),
        ("Does stirring change how fast salt dissolves?", "whether the water is stirred", "the time taken to dissolve", "the amount of salt and water"),
        ("Does the colour of light change how fast a pond plant gives off bubbles?", "the colour of the light", "the number of bubbles per minute", "the distance of the lamp"),
        ("Does the depth of water change the pressure it exerts?", "the depth of water", "how far water spurts from a hole", "the size of the hole"),
        ("Do bread moulds grow faster in warm places?", "the temperature", "the area covered by mould after three days", "the type and size of bread"),
        ("Does the mass of an object change the stretch of a spring?", "the mass hung on the spring", "the length of the spring", "the type of spring"),
        ("Does a salt solution conduct electricity better when more salt is added?", "the amount of salt", "the brightness of the bulb", "the amount of water"),
        ("Does the angle of a mirror change where the reflected light falls?", "the angle of the mirror", "the position of the light spot on the wall", "the torch used")]


def c_vars(k=None):
    R = _R[0]
    q, iv, dv, cv = R.choice(VARS)
    k = k or R.choice(["iv", "dv", "cv"])
    junk = R.choice(["the colour of the student's shirt", "the day of the week", "the name of the school"])
    if k == "iv":
        return tq("Investigation: <i>%s</i> What is the independent variable?" % q, iv, [dv, cv, junk], "Independent: %s. Dependent: %s. Controlled: %s." % (iv, dv, cv))
    if k == "dv":
        return tq("Investigation: <i>%s</i> What is the dependent variable?" % q, dv, [iv, cv, junk], "Independent: %s. Dependent: %s. Controlled: %s." % (iv, dv, cv))
    return tq("Investigation: <i>%s</i> Which should be a controlled variable?" % q, cv, [iv, dv, junk], "Independent: %s. Dependent: %s. Controlled: %s." % (iv, dv, cv))


def c_avg(k=None):
    R = _R[0]
    what, unit = R.choice([("the time for a ball to roll down a ramp", "s"), ("the height of a bean plant", "cm"), ("the temperature of water in a pot", "°C"),
                           ("the length of a spring", "cm"), ("the time for 20 swings of a pendulum", "s"), ("the mass of a potato", "g")])
    base = R.choice([12, 15, 18, 20, 24, 25, 30, 36, 40, 45])
    d = [R.choice([-2, -1, 0, 1, 2]) for _ in range(3)]
    d[2] = -d[0] - d[1]
    if abs(d[2]) > 3:
        return None
    vals = [base + x for x in d]
    s = sum(vals)
    return nq("A student measures %s three times: %s. What is the average?" % (what, ", ".join("%d %s" % (v, unit) if unit != "°C" else "%d °C" % v for v in vals)), base,
              [s, max(vals), min(vals), s / 2], unit, "Average = (%s) ÷ 3 = %d ÷ 3 = %d %s." % (" + ".join(str(v) for v in vals), s, base, unit))


OBSINF = {"an observation": ["The leaves of the plant are drooping.", "The thermometer reads 31 °C.", "The milk has turned sour and smells bad.", "There are bubbles on the leaf in water.",
                             "The nail has a brown coating.", "The ground is wet this morning.", "The bulb glows brightly."],
          "an inference": ["The plant has not been watered.", "It is a hot day.", "Microbes have acted on the milk.", "The leaf is giving off oxygen.",
                           "The nail has rusted because of moist air.", "It rained last night.", "The cell is new."]}

# =================================================================== Chapter 2: the invisible living world
MICG = {"a bacterium": ["Lactobacillus", "Rhizobium", "the germ that causes typhoid", "the germ that causes tuberculosis", "the germ that causes cholera", "E. coli"],
        "a fungus": ["yeast", "bread mould", "Penicillium", "a mushroom", "the fungus causing rust of wheat"],
        "a protozoan": ["Amoeba", "Paramecium", "Plasmodium, which causes malaria", "the protozoan causing amoebic dysentery"],
        "a virus": ["the virus causing polio", "the virus causing chickenpox", "the virus causing measles", "the virus causing COVID-19", "the virus causing the common cold"],
        "an alga": ["Spirogyra", "Chlamydomonas", "diatoms", "Volvox"]}
DIS = [("malaria", "a protozoan (Plasmodium)", "the bite of a female Anopheles mosquito"), ("dengue", "a virus", "the bite of an Aedes mosquito"),
       ("tuberculosis", "a bacterium", "air, through coughs and sneezes"), ("typhoid", "a bacterium", "contaminated food and water"),
       ("cholera", "a bacterium", "contaminated food and water"), ("polio", "a virus", "contaminated food and water"), ("chickenpox", "a virus", "air, through coughs and sneezes"),
       ("measles", "a virus", "air, through coughs and sneezes"), ("the common cold", "a virus", "air, through coughs and sneezes"), ("ringworm", "a fungus", "direct contact with infected skin or objects")]


def c_dis(k=None):
    R = _R[0]
    d, c, how = R.choice(DIS)
    if R.random() < 0.5:
        return tq("What kind of microorganism causes %s?" % d, c, R.sample(sorted({x for _, x, _ in DIS if x != c} | {"an alga"}), 3), "%s is caused by %s and spreads through %s." % (_cap(d), c, how))
    w = sorted({x for _, _, x in DIS if x != how})
    return tq("How does %s usually spread?" % d, how, R.sample(w, 3), "%s is caused by %s." % (_cap(d), c))


USEM = [("Lactobacillus", "turning milk into curd"), ("yeast", "making bread and idli dough rise"), ("Penicillium", "making the antibiotic penicillin"),
        ("Rhizobium", "fixing nitrogen in the root nodules of pulses"), ("decomposer bacteria and fungi", "breaking down dead plants and animals into simple substances"),
        ("bacteria in a biogas plant", "producing fuel gas from cow dung"), ("yeast in a factory", "producing alcohol from sugar by fermentation"), ("weakened or dead germs", "making vaccines")]
PRES = [("salting", "pickles, raw mangoes and fish"), ("adding sugar", "jams, jellies and squashes"), ("adding oil and vinegar", "pickles"),
        ("pasteurisation", "milk, heated to about 70 °C for a short time and then cooled quickly"), ("refrigeration", "vegetables, fruits and cooked food kept for a few days"),
        ("drying", "papads, raisins and dried fish"), ("airtight packing", "chips and biscuits")]
MICQ = [("What are microorganisms?", "living things too small to be seen without a microscope", ["very large animals", "plants that live in water only", "non-living particles"], "Bacteria and protozoa are microorganisms."),
        ("Which instrument is needed to see microorganisms?", "a microscope", ["a telescope", "a periscope", "a stethoscope"], "Antonie van Leeuwenhoek first saw them in the 1670s."),
        ("Why are viruses different from other microorganisms?", "they reproduce only inside the cells of a host", ["they can make their own food", "they are large enough to see", "they live only in soil"], "Outside a host they show no signs of life."),
        ("Why do antibiotics not cure the common cold?", "the cold is caused by a virus, and antibiotics do not work on viruses", ["the cold is caused by bacteria", "antibiotics are too strong", "the cold is not a disease"], "Take antibiotics only when a doctor prescribes them."),
        ("Why should a full course of antibiotics be completed?", "stopping early can leave some bacteria alive and make them resistant", ["it makes the medicine taste better", "it does not matter", "to finish the bottle"], "Misuse of antibiotics is a global problem."),
        ("What is a vaccine?", "a preparation of dead or weakened germs that trains the body to fight a disease", ["a medicine that kills all germs", "a vitamin", "a type of food"], "Vaccines protect against polio, measles and more."),
        ("Who developed the first vaccine?", "Edward Jenner", ["Alexander Fleming", "Louis Pasteur", "Robert Hooke"], "It was against smallpox, in 1796."),
        ("Who discovered penicillin?", "Alexander Fleming", ["Edward Jenner", "Robert Koch", "Isaac Newton"], "He noticed mould killing bacteria in 1928."),
        ("Why does idli batter rise after keeping it overnight?", "yeast and bacteria ferment it and release carbon dioxide", ["the rice grows", "air leaks in", "the salt melts"], "This is fermentation."),
        ("Why do we keep food in a refrigerator?", "the low temperature slows the growth of microbes", ["cold kills all germs instantly", "it adds vitamins", "it changes the food's colour"], "Food still spoils slowly."),
        ("Why does salt help to preserve pickles?", "it removes water and microbes cannot grow without water", ["salt is a vitamin", "salt adds bacteria", "salt makes food hot"], "Sugar works the same way in jams."),
        ("What is pasteurisation?", "heating milk to about 70 °C for a short time and then cooling it quickly to kill harmful microbes", ["freezing milk", "adding sugar to milk", "boiling milk for an hour"], "It was developed by Louis Pasteur."),
        ("How do microbes help in a compost pit?", "they decompose kitchen and garden waste into manure", ["they make plastic", "they stop rotting", "they make the pit smell sweet"], "Compost enriches soil."),
        ("What is a carrier of disease?", "an animal that spreads germs, such as a housefly or mosquito", ["a medicine", "a vaccine", "a doctor"], "Flies carry germs from waste to food."),
        ("Why should stagnant water be removed from coolers and pots?", "mosquitoes breed in it", ["it is too cold", "fish need it", "it becomes salty"], "This helps prevent malaria and dengue."),
        ("Why is the female Anopheles mosquito important to know about?", "it carries the malaria parasite", ["it carries dengue only", "it makes honey", "it is harmless"], "Use nets and repellents."),
        ("Which microorganism is used to make curd?", "Lactobacillus (a bacterium)", ["yeast only", "Plasmodium", "a virus"], "Add a little curd to warm milk."),
        ("Why is cooked food covered?", "to keep flies and dust carrying germs away", ["to make it colder", "to add flavour", "to make it grow"], "Uncovered food spoils faster."),
        ("How does Rhizobium help farmers?", "it fixes nitrogen from the air into the soil", ["it eats insects", "it makes the soil acidic", "it causes plant diseases"], "It lives in root nodules of pulses."),
        ("What is the role of decomposers in nature?", "they return nutrients from dead matter to the soil", ["they make food from sunlight", "they eat living animals", "they pollute water"], "Without them dead matter would pile up."),
        ("Which plant disease is caused by bacteria and spreads through air?", "citrus canker", ["rust of wheat", "yellow vein mosaic of bhindi", "malaria"], "Rust of wheat is caused by a fungus."),
        ("Which disease of bhindi (okra) is caused by a virus spread by insects?", "yellow vein mosaic", ["citrus canker", "rust of wheat", "tuberculosis"], "Insects carry the virus."),
        ("Which microorganisms make their own food by photosynthesis?", "algae", ["viruses", "fungi", "most bacteria of decay"], "Spirogyra is an alga."),
        ("What happens to bread left in a warm, damp place for a few days?", "a fuzzy mould (a fungus) grows on it", ["it turns into cheese", "it becomes harder only", "it turns into sugar"], "Do not eat mouldy food."),
        ("Why are microbes called both friends and foes?", "some help us, as in curd and medicines, while others cause diseases", ["they are always harmful", "they are always useful", "they do nothing"], "We must understand both sides."),
        ("What is the smallest unit of a living thing?", "the cell", ["the tissue", "the organ", "the virus"], "Bacteria are single cells."),
        ("Which part of a microscope holds the glass slide?", "the stage", ["the eyepiece", "the mirror", "the base only"], "Clips keep the slide in place."),
        ("Why is iodine or methylene blue added to a slide of cheek cells?", "to stain the cells so their parts can be seen", ["to kill the microscope", "to make the slide sticky", "to cool the cells"], "The nucleus takes up the stain.")]

# =================================================================== Chapter 3: health — the ultimate treasure
HSPREAD = {"a communicable disease (it spreads from person to person)": ["tuberculosis", "the common cold", "chickenpox", "measles", "COVID-19", "influenza", "cholera", "typhoid"],
           "a non-communicable disease (it does not spread from person to person)": ["diabetes", "high blood pressure", "most cancers", "asthma", "heart disease", "scurvy", "night blindness", "obesity"]}
SPREADBY = {"spread mainly through the air": ["tuberculosis", "the common cold", "measles", "influenza", "chickenpox"],
            "spread mainly through contaminated food and water": ["cholera", "typhoid", "hepatitis A (jaundice)", "diarrhoea"],
            "spread mainly by mosquitoes": ["malaria", "dengue", "chikungunya", "filariasis"],
            "spread mainly by direct contact": ["ringworm", "scabies", "conjunctivitis (eye flu)"]}
PREV = [("tuberculosis", "the BCG vaccine and covering coughs"), ("malaria", "using mosquito nets and removing stagnant water"), ("cholera", "drinking boiled or treated water"),
        ("polio", "the oral polio drops (vaccine)"), ("dengue", "preventing mosquito breeding in coolers, pots and tyres"), ("the common cold", "washing hands and avoiding close contact with sick people"),
        ("type 2 diabetes", "eating less sugar, staying active and keeping a healthy weight"), ("tooth decay", "brushing twice a day and eating fewer sweets"),
        ("anaemia", "eating iron-rich foods such as green leafy vegetables and jaggery"), ("goitre", "using iodised salt")]
HQ = [("What does good health mean?", "physical, mental and social well-being, not just the absence of disease", ["only having no fever", "only being tall", "only having money"], "This is how the World Health Organization describes it."),
      ("What is immunity?", "the body's ability to fight germs and resist disease", ["a type of medicine", "a disease of the skin", "a kind of food"], "White blood cells are part of the immune system."),
      ("How does a vaccine give immunity?", "it trains the immune system to recognise a germ before a real infection", ["it kills all germs in the body at once", "it replaces blood", "it is a vitamin"], "Booster doses may be needed."),
      ("What is a communicable disease?", "a disease that can spread from one person to another", ["a disease caused by a lack of vitamins", "a disease that never spreads", "an injury"], "Germs cause communicable diseases."),
      ("What is a lifestyle disease?", "a disease linked to habits such as poor diet, inactivity and smoking", ["a disease caught from a mosquito", "a disease caused by a virus only", "an injury in a game"], "Type 2 diabetes and high blood pressure are examples."),
      ("Why should we wash our hands with soap before eating?", "soap removes germs that could enter our body with food", ["soap adds vitamins", "it makes the food taste better", "it is not needed"], "Wash for at least 20 seconds."),
      ("Why should we cover our mouth while coughing or sneezing?", "to stop germs spreading through droplets in the air", ["to keep warm", "to stop the cough", "to look polite only"], "Use a tissue or your elbow."),
      ("Why are antibiotics not given for viral fevers?", "antibiotics kill bacteria but not viruses", ["viruses are too large", "antibiotics are vitamins", "fevers are never serious"], "Misuse makes bacteria resistant."),
      ("What is antibiotic resistance?", "bacteria no longer being killed by an antibiotic", ["the body refusing to eat", "a vaccine stopping working at once", "a kind of allergy to food"], "It is caused by misuse of antibiotics."),
      ("Why is regular exercise good for health?", "it strengthens the heart, muscles and bones and reduces stress", ["it weakens the body", "it causes diseases", "it stops growth"], "Children should be active for about an hour a day."),
      ("Why is yoga good for health?", "it improves flexibility, breathing and calmness", ["it causes injuries always", "it stops breathing", "it replaces food"], "21 June is International Day of Yoga."),
      ("Why is sleep important for health?", "the body and brain rest and repair during sleep", ["sleep wastes time", "sleep causes disease", "sleep makes muscles weak"], "Teenagers need 8–10 hours."),
      ("What is mental health?", "how we think, feel and cope with daily life", ["the size of the brain", "the number of marks we get", "a kind of exercise"], "Talking to trusted people helps."),
      ("Why should we not take medicines without a doctor's advice?", "the wrong medicine or dose can harm us", ["medicines are always harmless", "doctors do not know about medicines", "medicines are food"], "Always check the expiry date too."),
      ("What is a balanced diet?", "a diet with all nutrients in the right amounts", ["a diet with only proteins", "a diet with no fat", "eating only fruit"], "Include cereals, pulses, vegetables, fruits and milk."),
      ("How do mosquito nets help prevent malaria?", "they stop mosquitoes biting us while we sleep", ["they kill the malaria parasite in blood", "they cure malaria", "they cool the room"], "Insect repellents also help."),
      ("Why is clean drinking water important?", "dirty water can carry germs of cholera, typhoid and diarrhoea", ["it makes water tasty", "it adds salt", "it is not important"], "Boil or filter water."),
      ("What does ORS help with?", "replacing water and salts lost in diarrhoea", ["curing malaria", "healing broken bones", "growing taller"], "ORS is oral rehydration solution."),
      ("What is the role of white blood cells?", "fighting germs that enter the body", ["carrying oxygen", "helping blood clot only", "digesting food"], "They are part of the immune system."),
      ("Which national programme gives free vaccines to children in India?", "the Universal Immunisation Programme", ["the Green Revolution", "Project Tiger", "Swachh Bharat only"], "It protects against many diseases."),
      ("Why was India declared polio-free in 2014?", "because of large vaccination drives with oral polio drops", ["because polio germs disappeared by themselves", "because of antibiotics", "because people stopped eating"], "Pulse Polio campaigns reached every child."),
      ("What is a healthy way to deal with stress?", "exercise, talk to someone, sleep well and take breaks", ["skip meals", "stay awake all night", "keep everything to yourself"], "Stress is a normal part of life."),
      ("Why is smoking harmful?", "it damages the lungs and heart and can cause cancer", ["it builds strong lungs", "it improves breathing", "it prevents disease"], "Passive smoking harms others too."),
      ("How does a balanced diet help immunity?", "nutrients such as proteins and vitamins help the body fight infections", ["it has no effect", "it weakens the body", "only sugar helps immunity"], "Vitamin C and zinc are important."),
      ("What is a pandemic?", "a disease that spreads across many countries at the same time", ["a disease in one person", "a disease of plants only", "a cured disease"], "COVID-19 was a pandemic."),
      ("What is an epidemic?", "a sudden spread of a disease to many people in an area", ["a disease in one plant", "a cured disease", "a vitamin deficiency"], "Cholera epidemics followed floods in the past."),
      ("What is a vector of disease?", "an organism such as a mosquito or fly that carries germs to people", ["a vaccine", "a doctor", "a vitamin"], "Controlling vectors controls diseases."),
      ("Why should we eat food from clean places?", "food from dirty places may carry germs of diarrhoea and typhoid", ["clean food has no taste", "dirty food has more vitamins", "it does not matter"], "Cover food and keep flies away."),
      ("What is herd immunity?", "when most people are immune, so a disease cannot spread easily, protecting others too", ["immunity of cows only", "immunity from eating more", "a disease of herds"], "Vaccinating many people protects those who cannot be vaccinated."),
      ("Why do doctors ask us to finish all the doses of a vaccine?", "some vaccines need more than one dose to give full protection", ["one dose is too strong", "to use up stock", "it is not needed"], "Follow the vaccination schedule."),
      ("What is the main cause of type 2 diabetes in many people?", "an unhealthy diet, lack of exercise and being overweight", ["a mosquito bite", "a virus", "drinking water"], "It is a lifestyle disease."),
      ("Why should we reduce salt in our food?", "too much salt can raise blood pressure", ["salt builds bones", "salt is a vitamin", "salt cures fever"], "Eat fewer packaged snacks."),
      ("What is a symptom?", "a sign of a disease felt or seen, such as fever or cough", ["a medicine", "a vaccine", "a germ"], "Doctors use symptoms to diagnose."),
      ("Why should a person with a cold stay home and rest?", "to recover faster and avoid spreading the virus", ["to catch more germs", "to make it worse", "because colds are bacterial"], "Rest, fluids and good food help."),
      ("Which body defence traps dust and germs in the nose?", "hairs and mucus", ["the teeth", "the stomach acid", "the skin of the hands"], "Coughing and sneezing also expel germs.")]

# =================================================================== Chapter 4: magnetic and heating effects of electric current
EMQ = [("What is an electromagnet?", "a coil of insulated wire wound on an iron core that becomes a magnet when current flows", ["a permanent magnet made of plastic", "a cell", "a fuse"], "It stops being a magnet when the current is switched off."),
       ("What happens to an electromagnet when the current is switched off?", "it loses most of its magnetism", ["it becomes stronger", "it melts", "it stays a strong magnet"], "This makes it useful in cranes and bells."),
       ("How can the strength of an electromagnet be increased?", "by increasing the number of turns or the current", ["by removing the iron core", "by using a plastic core", "by using fewer turns"], "An iron core also makes it stronger."),
       ("Why is a compass needle deflected near a wire carrying current?", "the current produces a magnetic field around the wire", ["the wire is hot", "the wire is made of iron", "the compass is broken"], "Hans Christian Oersted discovered this in 1820."),
       ("What happens to the poles of an electromagnet if the direction of current is reversed?", "the poles are reversed", ["the poles stay the same", "it loses all magnetism", "it melts"], "Its north pole becomes the south pole."),
       ("Where are electromagnets used?", "electric bells, cranes in scrapyards, motors and loudspeakers", ["only in pencils", "in wooden toys", "in glass windows"], "MRI machines use very strong electromagnets."),
       ("How does an electric bell work?", "an electromagnet attracts an iron strip that hits the gong and breaks the circuit, again and again", ["a magnet pushes a drum", "sound is stored in it", "a battery shakes it"], "This happens many times a second."),
       ("What is the heating effect of electric current?", "a wire gets hot when current flows through it", ["a wire gets cold", "a wire becomes a magnet only", "current makes light only"], "Heaters, irons and toasters use it."),
       ("Which appliances use the heating effect of current?", "an electric iron, a heater, a kettle and a toaster", ["a compass", "a pencil", "a bicycle"], "Their elements are often made of nichrome."),
       ("Why is nichrome used for heating elements?", "it gets very hot without melting and has a high resistance", ["it is an insulator", "it is very cheap plastic", "it is magnetic"], "It glows red when hot."),
       ("What is an electric fuse?", "a safety device with a thin wire that melts if too much current flows", ["a switch to turn on lights", "a kind of bulb", "a cell"], "It breaks the circuit and prevents fires."),
       ("Why does a fuse wire have a low melting point?", "so it melts quickly when the current becomes too high", ["so it never melts", "so it glows like a bulb", "so it becomes a magnet"], "A fuse protects the wiring."),
       ("What is an MCB?", "a miniature circuit breaker, a switch that turns off automatically when too much current flows", ["a type of bulb", "a cell", "a magnet"], "It can be reset easily."),
       ("Why should many high-power appliances not be connected to one socket?", "too much current can overheat the wires and cause a fire", ["they will work better", "they need no current", "it saves electricity"], "This is called overloading."),
       ("What is a short circuit?", "current taking a very easy path, for example when live and neutral wires touch, causing a large current", ["a very short wire", "a switched-off circuit", "a circuit with an LED"], "It can cause sparks and fire."),
       ("Why do filament bulbs waste energy?", "much of the electrical energy is changed to heat, not light", ["they make no heat", "they make too much light", "they use no electricity"], "LEDs waste much less energy."),
       ("Which metal is used for the filament of filament bulbs?", "tungsten", ["copper", "aluminium", "nichrome"], "It has a very high melting point."),
       ("What does ISI mark on electrical appliances show?", "that the appliance meets Indian safety standards", ["that it is cheap", "that it uses no electricity", "that it is foreign-made"], "Always buy ISI-marked appliances."),
       ("Why is the core of an electromagnet made of soft iron?", "it becomes magnetised strongly and loses magnetism easily", ["it never becomes magnetised", "it is an insulator", "it is very light"], "Steel would stay magnetised."),
       ("How are electromagnets used at scrapyards?", "a crane with an electromagnet lifts iron scrap and drops it when switched off", ["to melt the scrap", "to paint the scrap", "to wash the scrap"], "Non-magnetic metals are left behind."),
       ("What does an electric motor do?", "it changes electrical energy into motion using magnets and coils", ["it changes heat into light", "it stores current", "it makes magnets disappear"], "Fans and mixers have motors."),
       ("Why does a wire get hotter when more current flows through it?", "more electrical energy is changed into heat", ["less energy is used", "the wire becomes thinner", "the wire stops conducting"], "Heat increases quickly with current."),
       ("Why are electric wires at home made of copper?", "copper is a good conductor and does not heat up much", ["copper melts easily", "copper is an insulator", "copper is magnetic"], "They are covered with PVC insulation."),
       ("What is the purpose of the earth wire in house wiring?", "it carries leaked current safely to the ground and prevents shocks", ["it brings electricity from the power station", "it makes appliances work faster", "it measures current"], "Metal-bodied appliances are earthed."),
       ("Who discovered that a current-carrying wire deflects a compass needle?", "Hans Christian Oersted", ["Isaac Newton", "C. V. Raman", "Galileo Galilei"], "He noticed it in 1820."),
       ("Why is the wire of an electromagnet insulated?", "so the current flows along the whole coil instead of jumping between turns", ["to make it heavier", "to make it a conductor", "to make it glow"], "The iron core is inside the coil."),
       ("Why does an electric heater's element glow red?", "it becomes very hot because of the heating effect of current", ["it is painted red", "it is magnetic", "it contains red gas"], "Most of the energy becomes heat."),
       ("Why are LED bulbs cooler to touch than filament bulbs?", "they change more of the energy into light and less into heat", ["they use more current", "they have no electricity", "they are made of ice"], "They save electricity."),
       ("What will happen to the pins picked up by an electromagnet when the switch is opened?", "most of them drop off", ["they stick even harder", "they melt", "they become magnets for ever"], "The iron core loses its magnetism."),
       ("How is a fuse connected in a circuit?", "in series with the appliance, so all the current passes through it", ["away from the circuit", "only to the earth wire", "it is not connected"], "It breaks the circuit when it melts."),
       ("Which effect of current is used in an electric bell?", "the magnetic effect", ["the heating effect only", "the chemical effect", "no effect"], "An electromagnet pulls the hammer."),
       ("What is the main energy change in an electric heater?", "electrical energy to heat energy", ["heat to electrical energy", "light to sound", "sound to heat"], "In a fan it is electrical to motion.")]


def c_magnet(k=None):
    R = _R[0]
    t1, t2 = R.sample([20, 30, 40, 50, 60, 80, 100], 2)
    c1, c2 = R.choice([1, 2]), R.choice([1, 2])
    core = R.choice(["an iron nail", "an iron bolt", "a soft iron rod"])
    if c1 == c2:
        a = "Coil A, with %d turns" % t1 if t1 > t2 else "Coil B, with %d turns" % t2
        return tq("Two electromagnets are made on %s with the same current from %d cell%s. Coil A has %d turns and coil B has %d turns. Which picks up more pins?" % (core, c1, "" if c1 == 1 else "s", t1, t2),
                  a, [x for x in ["Coil A, with %d turns" % t1, "Coil B, with %d turns" % t2, "both pick up the same number", "neither picks up any pins"] if x != a], "More turns make a stronger electromagnet.")
    t = R.choice([30, 40, 50, 60])
    a = "the one with %d cells" % max(c1, c2)
    return tq("Two electromagnets each have %d turns on %s. One uses 1 cell and the other uses 2 cells. Which is stronger?" % (t, core), "the one with 2 cells",
              ["the one with 1 cell", "both are equally strong", "neither is magnetic"], "More current makes a stronger electromagnet.")


EAPP = {"an appliance that mainly uses the heating effect": ["an electric iron", "a room heater", "an electric kettle", "a toaster", "a water heater (geyser)", "a hair dryer's heating coil",
                                                            "an immersion rod", "an electric stove", "a soldering iron", "a rice cooker"],
        "a device that mainly uses the magnetic effect": ["an electric bell", "a scrapyard crane magnet", "an electric fan's motor", "a loudspeaker", "a mixer's motor", "a doorbell buzzer",
                                                          "a washing machine's motor", "an electric lock", "a relay switch", "a magnetic train (maglev)"]}
SAFE = {"a safe practice with electricity": ["using ISI-marked appliances", "switching off the mains before changing a bulb", "keeping wires away from water", "using the correct fuse or an MCB",
                                             "pulling the plug, not the wire, to unplug", "getting damaged wiring repaired by an electrician"],
        "an unsafe practice with electricity": ["touching switches with wet hands", "putting many plugs in one socket", "using a thick wire instead of a fuse wire", "flying kites near power lines",
                                                "poking metal objects into a socket", "using appliances with damaged cords"]}

# =================================================================== Chapter 5: exploring forces
FTYPE = {"a contact force": ["friction between a book and a table", "muscular force when you push a door", "the force of a hand squeezing a ball", "a hockey stick hitting a ball", "the push of a rope on a cart",
                             "a bullock pulling a cart", "your foot kicking a football", "the brake pads gripping a bicycle wheel", "a person lifting a bucket"],
         "a non-contact force": ["the pull of a magnet on an iron nail across a gap", "gravity pulling a falling apple", "a charged comb attracting bits of paper", "the Earth pulling the Moon", "magnets repelling each other",
                                 "a rubbed balloon pulling your hair", "the Sun pulling the Earth", "a raindrop falling to the ground", "a magnet moving a compass needle"]}
FEFF = [("a footballer kicks a ball at rest", "it makes the ball start moving"), ("a goalkeeper stops a moving ball", "it makes a moving object stop"),
        ("a batsman hits a ball coming towards him", "it changes the direction of motion"), ("you squeeze a lump of clay", "it changes the shape of an object"),
        ("a cyclist pedals harder", "it changes the speed of the bicycle"), ("you press a balloon between your hands", "it changes the shape of an object"),
        ("a fielder catches a fast ball", "it makes a moving object stop"), ("a girl pushes a stationary swing", "it makes the swing start moving"),
        ("the wind blows a kite to one side", "it changes the direction of motion"), ("a potter presses wet clay on a wheel", "it changes the shape of an object")]
FQ = [("What is a force?", "a push or a pull on an object", ["the mass of an object", "the speed of an object", "the colour of an object"], "Forces can change motion and shape."),
      ("What is the SI unit of force?", "the newton (N)", ["the kilogram", "the metre", "the pascal"], "It is named after Isaac Newton."),
      ("What is friction?", "a force that opposes motion between two surfaces in contact", ["a force that speeds things up", "a magnetic force", "the pull of the Earth"], "Rough surfaces have more friction."),
      ("Why do we slip on a wet marble floor?", "water reduces friction between our soles and the floor", ["water increases friction", "the floor becomes magnetic", "gravity becomes stronger"], "Shoes with grooves give a better grip."),
      ("Why are tyres made with treads (grooves)?", "to increase friction and grip on the road", ["to reduce friction", "to make them lighter", "to make them shine"], "Worn tyres are dangerous."),
      ("Why is oil put on the moving parts of a machine?", "to reduce friction and wear", ["to increase friction", "to make it heavier", "to make it noisy"], "This is lubrication."),
      ("How do ball bearings help in machines?", "they reduce friction by rolling instead of sliding", ["they increase friction", "they add weight", "they make heat"], "They are used in cycles and fans."),
      ("What is gravity?", "the force by which the Earth pulls objects towards it", ["a force that pushes things up", "a magnetic force", "friction"], "Every object attracts every other object."),
      ("What is weight?", "the force of gravity acting on an object", ["the amount of matter only", "the volume of an object", "the speed of an object"], "Weight is measured in newtons."),
      ("What is mass?", "the amount of matter in an object", ["the pull of gravity on it", "its speed", "its length"], "Mass is measured in kilograms and does not change from place to place."),
      ("Why would you weigh less on the Moon?", "the Moon's gravity is about one-sixth of the Earth's", ["your mass becomes smaller", "the Moon has no gravity", "the Moon has more air"], "Your mass stays the same."),
      ("Which instrument measures force?", "a spring balance", ["a thermometer", "a measuring tape", "a barometer"], "Its spring stretches more with more force."),
      ("What is an electrostatic force?", "a force between charged objects", ["a force of rubbing", "a force of muscles", "a magnetic force only"], "A comb rubbed in dry hair attracts paper bits."),
      ("Why does a ball rolling on grass stop sooner than on a smooth floor?", "grass gives more friction", ["grass has less friction", "the floor pulls the ball", "gravity is less on the floor"], "Friction slows moving objects."),
      ("What is muscular force?", "the force we apply using our muscles", ["the force of a magnet", "the force of gravity", "the force of friction only"], "Animals also use muscular force."),
      ("What happens when two equal forces act on an object in opposite directions?", "they balance and the motion does not change", ["the object speeds up", "the object changes shape always", "the object becomes heavier"], "Like an equal tug of war."),
      ("Two teams pull a rope with 300 N and 250 N in opposite directions. What is the net force?", "50 N towards the stronger team", ["550 N", "0 N", "300 N"], "Subtract forces in opposite directions."),
      ("Why is it easier to pull a heavy box on wheels than to drag it?", "rolling friction is much less than sliding friction", ["wheels increase friction", "wheels make it lighter", "wheels remove gravity"], "That is why suitcases have wheels."),
      ("Why do athletes wear spiked shoes?", "to increase friction for a better grip", ["to reduce friction", "to run slower", "to make shoes heavier"], "They help in pushing off the ground."),
      ("What does a force do to a moving cricket ball when it is caught?", "it stops the ball", ["it speeds the ball up", "it makes the ball heavier", "nothing"], "The fielder's hands apply the force."),
      ("Why do things fall to the ground when dropped?", "the Earth's gravity pulls them down", ["air pushes them down", "they are magnetic", "the ground pulls only metals"], "In the absence of air, a feather and a coin fall together."),
      ("What is the weight of an object on the Moon compared with the Earth?", "about one-sixth", ["six times more", "the same", "zero"], "The Moon is smaller and has weaker gravity."),
      ("Which force keeps the planets moving around the Sun?", "gravity", ["friction", "magnetic force", "muscular force"], "Gravity acts across space."),
      ("Why are streamlined shapes used for aeroplanes and fish?", "they reduce air or water resistance (drag)", ["they increase drag", "they make them heavier", "they reduce gravity"], "Drag is friction in fluids."),
      ("Why does a match light when rubbed on the side of the box?", "friction produces heat", ["friction makes it cold", "magnetism lights it", "gravity lights it"], "Rubbing hands also warms them."),
      ("Why do our hands feel warm when we rub them together?", "friction changes motion into heat", ["the air is warm", "blood stops flowing", "hands are magnetic"], "Friction produces heat."),
      ("Why would walking be very hard on a perfectly frictionless floor?", "our shoes need friction to push against the ground", ["we would be too heavy", "gravity would stop", "the floor would be magnetic"], "Friction helps us walk."),
      ("What is fluid friction (drag)?", "the friction force that liquids and air exert on objects moving through them", ["friction between two solids only", "a magnetic force", "a force of gravity"], "It is why parachutes slow down a fall."),
      ("Why does a parachute fall slowly?", "its large surface experiences a lot of air resistance", ["it has no weight", "gravity does not act on it", "it is magnetic"], "Air resistance opposes its fall."),
      ("Which force makes a stretched rubber band return to its shape?", "elastic force", ["magnetic force", "gravity", "electrostatic force"], "Springs also exert elastic force.")]


def c_weight(k=None):
    R = _R[0]
    m = R.choice([2, 5, 8, 10, 12, 15, 20, 25, 30, 40, 45, 50, 60])
    g = 10
    if R.random() < 0.45:
        return nq("Taking g = 10 m/s², what is the weight on Earth of an object of mass %d kg?" % m, m * g, [m, m + g, m * g / 6, m / g], "N", "Weight = mass × g = %d × 10 = %d N." % (m, m * g))
    if R.random() < 0.5:
        w = m * g
        return nq("Taking g = 10 m/s², an object weighs %d N on Earth. What is its mass?" % w, m, [w * g, w, w - g, m * 6], "kg", "Mass = weight ÷ g = %d ÷ 10 = %d kg." % (w, m))
    w = R.choice([60, 120, 180, 240, 300, 360, 420, 480, 540, 600])
    return nq("An astronaut weighs %d N on Earth. About how much would she weigh on the Moon, where gravity is one-sixth as strong?" % w, w // 6, [w * 6, w, w - 6, w // 10], "N",
              "%d ÷ 6 = %d N. Her mass stays the same." % (w, w // 6))


def c_net(k=None):
    R = _R[0]
    a, b_ = R.sample([50, 80, 100, 120, 150, 200, 250, 300, 350, 400], 2)
    if R.random() < 0.5:
        return nq("Two children push a box in the same direction with forces of %d N and %d N. What is the net force?" % (a, b_), a + b_, [abs(a - b_), a * b_ / 100, max(a, b_), 0], "N",
                  "Forces in the same direction add: %d + %d = %d N." % (a, b_, a + b_))
    return nq("Two teams pull a rope in opposite directions with %d N and %d N. What is the size of the net force?" % (a, b_), abs(a - b_), [a + b_, max(a, b_), 0, (a + b_) / 2], "N",
              "Forces in opposite directions subtract: %d − %d = %d N, towards the stronger team." % (max(a, b_), min(a, b_), abs(a - b_)))


FRIC = {"a way to increase friction": ["putting treads on tyres", "wearing shoes with spikes", "sprinkling sand on a slippery road", "using chalk powder on a gymnast's hands", "putting grooves on soles of shoes",
                                      "applying brakes on a bicycle", "using rubber mats in the bathroom", "wearing gloves with a rough grip"],
        "a way to reduce friction": ["oiling the hinges of a door", "using ball bearings in a cycle", "polishing a surface smooth", "putting wheels on a suitcase", "sprinkling powder on a carrom board",
                                     "greasing the axles of a cart", "giving aeroplanes a streamlined shape", "waxing the bottom of a sledge"]}

# =================================================================== Chapter 6: pressure, winds, storms and cyclones
PRQ = [("What is pressure?", "the force acting on a unit area of a surface", ["the mass of an object", "the force acting on a whole object only", "the speed of the wind"], "Pressure = force ÷ area."),
       ("What is the SI unit of pressure?", "the pascal (Pa), which is one newton per square metre", ["the newton", "the kilogram", "the joule"], "1 Pa = 1 N/m²."),
       ("Why does a sharp knife cut better than a blunt one?", "its thin edge has a small area, so the pressure is large", ["it has a large area", "it is heavier", "it is colder"], "The same force on a small area gives a large pressure."),
       ("Why do school bags have wide straps?", "wide straps spread the weight over a larger area, reducing pressure on the shoulders", ["to make bags heavier", "to increase pressure", "for decoration only"], "Thin straps dig into the shoulders."),
       ("Why do camels walk easily on sand?", "their broad, padded soles spread their weight and reduce pressure", ["their soles are narrow", "they are very light", "sand is hard"], "They do not sink much into the sand."),
       ("How does the pressure of water change with depth?", "it increases as depth increases", ["it decreases", "it stays the same", "it becomes zero"], "Water spurts farther from a lower hole."),
       ("Why is the wall of a dam thicker at the bottom?", "water pressure is greatest at the bottom", ["water is lighter at the bottom", "to save cement", "to stop fish"], "Pressure increases with depth."),
       ("What is atmospheric pressure?", "the pressure exerted by the air around us", ["the pressure of water only", "the weight of a person", "the pressure inside a tyre only"], "At sea level it is about 100,000 Pa."),
       ("Why don't we feel the huge atmospheric pressure on our bodies?", "the pressure inside our bodies balances it", ["there is no air pressure on Earth", "air has no weight", "our skin is too thick"], "Air pressure acts in all directions."),
       ("How does atmospheric pressure change as we go up a mountain?", "it decreases", ["it increases", "it stays the same", "it doubles"], "There is less air above us."),
       ("Why do our ears sometimes feel blocked in an aeroplane taking off?", "the air pressure outside changes faster than inside the ear", ["the plane is noisy", "the air is cold", "the seats are tight"], "Swallowing helps balance it."),
       ("Which instrument measures atmospheric pressure?", "a barometer", ["a thermometer", "an anemometer", "a rain gauge"], "Weather offices use barometers."),
       ("Which instrument measures wind speed?", "an anemometer", ["a barometer", "a thermometer", "a hygrometer"], "Its cups spin in the wind."),
       ("In which direction does wind blow?", "from a region of high pressure to a region of low pressure", ["from low pressure to high pressure", "always from north to south", "only upwards"], "Bigger differences give stronger winds."),
       ("Why does warm air rise?", "it expands and becomes lighter than the cool air around it", ["it becomes heavier", "it is pulled by the Sun", "it is magnetic"], "This creates low pressure near the ground."),
       ("What brings the monsoon rains to India?", "moist winds blowing from the sea towards the hot land", ["dry winds from deserts", "winds from the North Pole", "winds made by trains"], "Low pressure over the hot land pulls in sea air."),
       ("What is a cyclone?", "a huge storm with very strong winds spinning around a centre of low pressure", ["a small breeze", "a dry dust cloud only", "an earthquake"], "Its calm centre is called the eye."),
       ("What is the calm centre of a cyclone called?", "the eye", ["the tail", "the wall only", "the root"], "The strongest winds are around the eye."),
       ("Which part of India is most often hit by cyclones?", "the coasts, especially of Odisha, Andhra Pradesh, Tamil Nadu and West Bengal", ["the Thar desert", "Ladakh", "the middle of Madhya Pradesh"], "They form over warm seas."),
       ("Which organisation gives cyclone warnings in India?", "the India Meteorological Department (IMD)", ["ISRO only", "the Indian Railways", "the Reserve Bank"], "Satellites help track cyclones."),
       ("What should people do when a cyclone warning is given?", "move to a safe shelter and follow official instructions", ["go to the beach to watch", "go fishing", "stay on the roof"], "Keep emergency supplies ready."),
       ("What is a thunderstorm?", "a storm with lightning, thunder, strong winds and heavy rain", ["a quiet drizzle", "a sunny day", "a snowfall only"], "It forms when warm moist air rises fast."),
       ("Why should you not stand under a tall tree during lightning?", "lightning tends to strike tall objects", ["trees attract rain only", "trees are always safe", "lightning avoids trees"], "Crouch low in an open area away from tall objects, or go indoors."),
       ("Why does a balloon get pushed up when filled with hot air?", "hot air inside is lighter than the cooler air outside", ["hot air is heavier", "the balloon is magnetic", "the Sun pulls it"], "This is how hot air balloons fly."),
       ("Why does a drinking straw work?", "when we suck, air pressure on the liquid in the glass pushes it up the straw", ["the straw pulls the liquid", "the liquid boils", "gravity pushes it up"], "We lower the pressure inside the straw."),
       ("Why are tsunamis different from cyclones?", "tsunamis are caused by undersea earthquakes, not by winds", ["they are the same", "tsunamis are caused by the Sun", "cyclones are caused by earthquakes"], "Both can flood coasts.")]


def c_press(k=None):
    R = _R[0]
    F = R.choice([20, 40, 50, 60, 80, 100, 120, 150, 200, 300, 400, 500, 600])
    A = R.choice([0.5, 1, 2, 4, 5, 10, 0.1, 0.2, 0.25])
    P = F / A
    if P != int(P) or P > 100000:
        return None
    k = k or R.choice(["P", "F", "A"])
    if k == "P":
        return nq("A force of %d N acts on an area of %s m². What is the pressure?" % (F, nf(A)), P, [F * A, F + A, P / 10, P * 10], "Pa", "Pressure = force ÷ area = %d ÷ %s = %s Pa." % (F, nf(A), nf(P)))
    if k == "F":
        return nq("A pressure of %s Pa acts on an area of %s m². What is the force?" % (nf(P), nf(A)), F, [P / A, P + A, F * 10, F / 10], "N", "Force = pressure × area = %s × %s = %d N." % (nf(P), nf(A), F))
    return nq("A force of %d N produces a pressure of %s Pa. What is the area?" % (F, nf(P)), A, [F * P, P / F, A * 10, A / 10], "m²", "Area = force ÷ pressure = %d ÷ %s = %s m²." % (F, nf(P), nf(A)))


def c_press2(k=None):
    R = _R[0]
    who = R.choice(["A brick", "A wooden block", "A box", "A tin of paint", "A school bag"])
    w = R.choice([20, 30, 40, 60, 80, 100, 120])
    a1, a2 = R.sample([0.01, 0.02, 0.04, 0.05, 0.1, 0.2], 2)
    big, small = max(a1, a2), min(a1, a2)
    return tq("%s weighing %d N can rest on a face of area %s m² or %s m². On which face does it exert more pressure on the floor?" % (who, w, nf(a1), nf(a2)), "the face of area %s m²" % nf(small),
              ["the face of area %s m²" % nf(big), "the same pressure on both faces", "no pressure on either face"], "The same force on a smaller area gives a larger pressure: %d ÷ %s = %s Pa." % (w, nf(small), nf(w / small)))


STORM = {"a safety step during a cyclone": ["move to a cyclone shelter or a strong building away from the coast", "store drinking water and dry food", "keep a battery radio for warnings",
                                         "do not go fishing when a warning is given", "stay away from the seashore"],
         "a safety step during a thunderstorm": ["stay indoors and away from windows", "do not shelter under a tall, lonely tree", "unplug electrical appliances", "stay away from water bodies",
                                                 "if caught outside, crouch low away from tall objects"]}
WEATHER = [("a barometer", "atmospheric pressure"), ("an anemometer", "wind speed"), ("a rain gauge", "the amount of rainfall"), ("a wind vane", "the direction of the wind"),
           ("a thermometer", "air temperature"), ("a weather satellite", "the movement of clouds and cyclones from space")]

# =================================================================== Chapter 7: particulate nature of matter
PART = {"true of solids": ["they have a fixed shape", "their particles only vibrate in place", "the attraction between their particles is strongest", "they are hard to compress", "a stone and an ice cube are examples"],
        "true of liquids": ["they take the shape of their container", "they have a fixed volume but no fixed shape", "their particles can slide past each other", "water and milk are examples", "they can flow"],
        "true of gases": ["they fill the whole container", "they can be compressed easily", "their particles move fastest and are farthest apart", "air and steam are examples", "they have no fixed volume"]}
PMQ = [("What is matter made of?", "tiny particles that are too small to see", ["one big solid piece", "only air", "only water"], "These particles are atoms and molecules."),
       ("What happens when a crystal of potassium permanganate is put in water?", "the purple colour slowly spreads through all the water", ["the water turns solid", "nothing happens", "it floats on top for ever"], "Particles of the crystal mix with water particles."),
       ("What is diffusion?", "the spreading and mixing of particles of one substance among another", ["the freezing of water", "the melting of a solid", "the burning of a fuel"], "The smell of incense spreads by diffusion."),
       ("Why does the smell of hot food reach us faster than cold food?", "particles move faster at higher temperature, so diffusion is faster", ["cold food has no smell", "hot food is heavier", "air is thicker near hot food"], "Heat gives particles more energy."),
       ("In which state is diffusion fastest?", "gases", ["solids", "liquids", "it is the same in all"], "Gas particles move fastest and are far apart."),
       ("Why can we compress a gas but hardly a solid?", "gas particles have large spaces between them", ["gas particles are larger", "solids have large spaces", "gases have no particles"], "This is why gas is stored in cylinders."),
       ("Why does sugar seem to disappear when stirred in water?", "its particles spread into the spaces between water particles", ["it is destroyed", "it turns into air", "it sinks and hides"], "The water tastes sweet."),
       ("What happens to particles when a solid is heated?", "they gain energy and vibrate faster", ["they stop moving", "they lose energy", "they become larger"], "At the melting point they break free."),
       ("What is the melting point of a solid?", "the temperature at which it changes into a liquid", ["the temperature at which it boils", "the temperature at which it freezes into a gas", "its mass"], "Ice melts at 0 °C."),
       ("What is the boiling point of a liquid?", "the temperature at which it changes into a gas throughout", ["the temperature at which it freezes", "the temperature of the room", "its mass"], "Water boils at 100 °C at sea level."),
       ("Why does the level of water not rise when a little salt is dissolved in a full glass?", "salt particles fit into the spaces between water particles", ["salt has no particles", "water disappears", "salt turns into gas"], "This shows particles have spaces between them."),
       ("Why do solids have a fixed shape?", "their particles are held strongly in fixed positions", ["their particles move freely", "they have no particles", "they are always cold"], "Liquids and gases flow."),
       ("What does interparticle attraction mean?", "the force that holds particles of a substance together", ["the force of gravity on Earth", "a magnetic force", "friction"], "It is strongest in solids."),
       ("Why does a gas fill any container?", "its particles move freely in all directions with weak attraction", ["its particles are fixed", "it is heavier than air", "it has no particles"], "Gases spread out completely."),
       ("What happens to the spaces between particles when a liquid turns into a gas?", "they become much larger", ["they become smaller", "they stay the same", "they disappear"], "That is why steam takes up much more space than water."),
       ("Why can we smell perfume from across a room?", "perfume particles diffuse through the air", ["the perfume bottle walks", "air carries no particles", "the perfume freezes"], "They move randomly and spread."),
       ("Which change of state happens when steam touches a cold mirror?", "condensation: gas to liquid", ["melting: solid to liquid", "boiling", "freezing"], "Particles lose energy and come closer."),
       ("What happens to the particles of water when it freezes?", "they lose energy and settle into fixed positions", ["they gain energy", "they move faster", "they break apart"], "Water freezes at 0 °C."),
       ("What is sublimation?", "a solid changing directly into a gas without becoming a liquid", ["a liquid changing into a solid", "a gas changing into a liquid", "a solid dissolving in water"], "Camphor and naphthalene balls sublime."),
       ("Why does camphor left in an open dish get smaller over time?", "it sublimes into vapour", ["it melts into water", "it is eaten by ants", "it dissolves in air as a liquid"], "It changes directly from solid to gas."),
       ("Why does a balloon filled with air shrink in a cold room?", "the air particles move slower and take up less space", ["the balloon breathes", "air leaks out always", "cold air enters"], "Warm it and it expands again."),
       ("Why are gaps left between railway rails?", "the rails expand in summer heat", ["to save iron", "to make noise", "to let water flow"], "Particles vibrate more and take up more space when hot."),
       ("Why do we dry clothes faster on a hot day, in terms of particles?", "water particles gain more energy and escape faster as vapour", ["particles stop moving", "the clothes become heavier", "air particles push water in"], "This is evaporation."),
       ("What happens to the particles of a liquid at its boiling point?", "they gain enough energy to escape as gas throughout the liquid", ["they freeze", "they stop moving", "they become larger"], "Bubbles of vapour form inside."),
       ("Why does a drop of ink spread faster in hot water than in cold water?", "particles move faster in hot water", ["hot water has no particles", "ink is heavier in cold water", "cold water is magnetic"], "Diffusion increases with temperature."),
       ("Which has the strongest attraction between its particles: ice, water or steam?", "ice", ["water", "steam", "all are the same"], "Solids have the strongest attraction."),
       ("Why can a liquid flow but not a solid?", "liquid particles can slide past one another", ["liquid particles are fixed", "solids have no particles", "liquids are always hot"], "Solids hold their shape."),
       ("What are the particles of an element called?", "atoms (or molecules made of atoms)", ["cells", "crystals only", "drops"], "Atoms are the smallest particles of an element."),
       ("Why does a metal spoon get hot all over when one end is in hot tea?", "the vibrating particles pass energy to their neighbours", ["the tea climbs the spoon", "particles move along the spoon", "air carries the heat only"], "This is conduction."),
       ("What happens to the volume of most substances when they are heated?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "Thermometers use this.")]


MPBP = [("water", 0, 100), ("ethanol (alcohol)", -114, 78), ("iron", 1538, 2862), ("mercury", -39, 357), ("oxygen", -218, -183), ("nitrogen", -210, -196),
        ("common salt", 801, 1413), ("naphthalene", 80, 218), ("sulphur", 115, 445), ("lead", 327, 1749), ("gold", 1064, 2856), ("aluminium", 660, 2519)]


def c_mp(k=None):
    R = _R[0]
    nm, mp, bp = R.choice(MPBP)
    T = R.choice([-200, -150, -100, -50, -20, 0, 25, 50, 90, 150, 300, 500, 1000, 1200, 2000, 3000])
    if T in (mp, bp):
        return None
    a = "solid" if T < mp else "liquid" if T < bp else "gas"
    return tq("The melting point of %s is %d °C and its boiling point is %d °C. In which state is it at %d °C?" % (nm, mp, bp, T), a,
              [x for x in ["solid", "liquid", "gas", "it cannot exist at that temperature"] if x != a],
              "Below %d °C it is solid; between %d °C and %d °C it is liquid; above %d °C it is a gas." % (mp, mp, bp, bp))


def UNITS8a():
    b = {k: once_maker(v) for k, v in [("inv", INV), ("mic", MICQ), ("h", HQ), ("em", EMQ), ("f", FQ), ("pr", PRQ), ("pm", PMQ)]}
    obsinf = odd_one(OBSINF, "Which of these is %s?", "Which of these is not %s?")
    micg = odd_one(MICG, "Which of these is %s?", "Which of these is not %s?")
    usem = pairs(USEM, "How is %s useful to us?", "Which microorganism is used for %s?")
    pres = pairs(PRES, "Which foods are usually preserved by %s?", "Which method is used to preserve %s?")
    hspread = odd_one(HSPREAD, "Which of these is %s?", "Which of these is not %s?")
    spreadby = odd_one(SPREADBY, "Which of these diseases is %s?", "Which of these diseases is not %s?")
    prev = pairs(PREV, "Which is a good way to prevent %s?", "Which disease or condition can be prevented by %s?")
    eapp = odd_one(EAPP, "Which of these is %s?", "Which of these is not %s?")
    safe = odd_one(SAFE, "Which of these is %s?", "Which of these is not %s?")
    ftype = odd_one(FTYPE, "Which of these is an example of %s?", "Which of these is not an example of %s?")
    feff = pairs(FEFF, "What does the force do when %s?")
    fric = odd_one(FRIC, "Which of these is %s?", "Which of these is not %s?")
    weather = pairs(WEATHER, "What does %s measure or show?", "Which instrument is used for %s?")
    storm = odd_one(STORM, "Which of these is %s?", "Which of these is not %s?")

    part = odd_one(PART, "Which of these is %s?", "Which of these is not %s?")
    return [
        U(1, "exploring-the-investigative-world-of-science", 1, NS,
          "Investigating like a scientist: asking testable questions, planning fair investigations with independent, dependent and controlled variables, sampling and repeating measurements, recording data in tables and graphs, observations and inferences, and drawing evidence-based conclusions (summary of NCERT Curiosity Chapter 1).",
          "Exploring the Investigative World of Science", "the investigative world of science",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 1: planning investigations, independent, dependent and controlled variables, repeat readings and averages, observations and inferences, and graphs. 100 questions with answers.",
          "Change one variable, measure another, keep the rest the same.", "Repeat, average and look for patterns.",
          "<p>A scientific investigation starts with a testable question. In a fair test we change one variable on purpose (the independent variable), measure what happens (the dependent variable) and keep everything else the same (controlled variables). Repeating measurements and using bigger samples make results more reliable.</p>"
          "<p>We record data in tables and graphs and look for patterns. An observation is what we notice directly; an inference is what we conclude from it. Conclusions must be based on evidence, and other scientists check the work before it is accepted.</p>",
          [("More turns, more pins picked up. Independent variable?", ["the thing changed on purpose"], "the number of turns"), ("Readings 14, 15, 16 s. Average?", ["45 ÷ 3"], "15 s")],
          ["Mixing up the independent and dependent variables.", "Changing two variables at once.", "Calling an inference an observation."],
          [("What is the difference between independent and dependent variables?", "The independent variable is changed on purpose; the dependent variable is measured to see how it responds."),
           ("Why repeat measurements?", "Repeating and averaging reduces the effect of random errors and makes results more reliable.")],
          lambda: [("Asking questions and planning", [(b["inv"], 12), (c_avg, 8)]), ("Variables", [(K(c_vars, "iv"), 6), (K(c_vars, "dv"), 6), (K(c_vars, "cv"), 6), (b["inv"], 2)]),
                   ("Observations and inferences", [(obsinf, 14), (b["inv"], 4), (c_avg, 2)]), ("Data and averages", [(c_avg, 14), (c_vars, 6)]), ("Mixed problems", [(obsinf, 6), (c_avg, 12), (c_vars, 2)])]),
        U(2, "the-invisible-living-world-beyond-our-naked-eye", 2, LW,
          "Microorganisms: bacteria, fungi, protozoa, algae and viruses; seeing them with a microscope; useful microorganisms (curd, bread, antibiotics, nitrogen fixation, decomposition) and harmful ones (diseases of humans, animals and plants); food preservation (summary of NCERT Curiosity Chapter 2).",
          "The Invisible Living World: Beyond Our Naked Eye", "the invisible living world",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 2: bacteria, fungi, protozoa, algae and viruses, microbes in curd, bread and medicines, diseases and their carriers, and food preservation. 100 questions with answers.",
          "Microbes are too small to see but are everywhere.", "Some make curd and medicines; some cause disease.",
          "<p>Microorganisms are living things too small to see without a microscope: bacteria, fungi, protozoa, algae and viruses (which reproduce only inside living cells). Many are useful: Lactobacillus makes curd, yeast makes dough rise, Penicillium gives penicillin, Rhizobium fixes nitrogen and decomposers recycle dead matter.</p>"
          "<p>Some cause diseases: tuberculosis and typhoid (bacteria), malaria (a protozoan spread by the female Anopheles mosquito), polio and chickenpox (viruses). Antibiotics work against bacteria, not viruses; vaccines prevent many diseases. Salting, sugar, oil, pasteurisation, drying and refrigeration stop microbes from spoiling food.</p>",
          [("Which microbe sets curd?", ["a bacterium in milk"], "Lactobacillus"), ("Does an antibiotic cure a cold?", ["the cold is viral"], "no")],
          ["Thinking all microbes are harmful.", "Taking antibiotics for viral infections.", "Saying malaria is caused by a virus."],
          [("How do microbes help us?", "They make curd, bread and medicines, fix nitrogen in soil and decompose waste into manure."),
           ("What is pasteurisation?", "Heating milk to about 70 °C for a short time and then cooling it quickly, so that harmful microbes are killed.")],
          lambda: [("Kinds of microorganisms", [(micg, 14), (b["mic"], 6)]), ("Useful microorganisms", [(usem, 12), (b["mic"], 8)]), ("Microorganisms and disease", [(c_dis, 14), (b["mic"], 6)]),
                   ("Food preservation", [(pres, 10), (micg, 10)]), ("Mixed problems", [(micg, 16), (c_dis, 2), (b["mic"], 2)])]),
        U(3, "health-the-ultimate-treasure", 3, LW,
          "Health as physical, mental and social well-being; communicable and non-communicable diseases; how diseases spread and how they can be prevented; immunity and vaccination; antibiotics and their responsible use; healthy habits, diet, exercise, sleep and mental health (summary of NCERT Curiosity Chapter 3).",
          "Health: The Ultimate Treasure", "health",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 3: communicable and non-communicable diseases, how diseases spread and are prevented, immunity and vaccines, antibiotics, and healthy habits. 100 questions with answers.",
          "Health is physical, mental and social well-being.", "Prevention is better than cure.",
          "<p>Good health is physical, mental and social well-being. Communicable diseases such as tuberculosis, measles and the common cold spread from person to person through air, water, food, contact or carriers like mosquitoes. Non-communicable diseases such as diabetes and high blood pressure do not spread, but are linked to diet and lifestyle.</p>"
          "<p>We prevent diseases with clean water, hand-washing, covering coughs, mosquito control, a balanced diet, exercise and sleep. Vaccines train the immune system before infection; antibiotics fight bacteria only and must be taken as prescribed, or bacteria become resistant.</p>",
          [("Is diabetes communicable?", ["it does not spread from person to person"], "no: non-communicable"), ("How to prevent dengue?", ["Aedes mosquitoes breed in stored water"], "remove stagnant water")],
          ["Using antibiotics for viral fevers.", "Thinking only physical fitness is health.", "Stopping an antibiotic course early."],
          [("How do vaccines work?", "They contain weakened or dead germs (or parts of them), which train the immune system to fight the real disease quickly."),
           ("What is the difference between communicable and non-communicable diseases?", "Communicable diseases spread from person to person through germs; non-communicable diseases do not spread.")],
          lambda: [("What is health?", [(b["h"], 14), (hspread, 6)]), ("Communicable and non-communicable diseases", [(hspread, 14), (b["h"], 6)]), ("Preventing diseases", [(prev, 12), (spreadby, 8)]),
                   ("Immunity and medicines", [(b["h"], 8), (c_dis, 6), (spreadby, 6)]), ("Mixed problems", [(spreadby, 6), (c_dis, 10), (prev, 4)])]),
        U(4, "electricity-magnetic-and-heating-effects", 4, PH,
          "Magnetic effect of electric current; electromagnets and how to make them stronger; uses of electromagnets such as the electric bell and cranes; heating effect of current and its uses; fuses, MCBs and electrical safety; energy-efficient lighting (summary of NCERT Curiosity Chapter 4).",
          "Electricity: Magnetic and Heating Effects", "magnetic and heating effects of current",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 4: the magnetic effect of current, electromagnets, the electric bell, the heating effect, heaters and fuses, MCBs and electrical safety. 100 questions with answers.",
          "Current makes a wire hot and makes a coil a magnet.", "More turns or more current: a stronger electromagnet.",
          "<p>A wire carrying current behaves like a magnet and deflects a compass. A coil of insulated wire wound on a soft iron core becomes an electromagnet when current flows; it is stronger with more turns or more current, and its poles reverse when the current reverses. Electric bells, scrapyard cranes, motors and loudspeakers use electromagnets.</p>"
          "<p>Current also heats a wire. Heaters, irons and kettles use nichrome elements. A fuse has a thin wire that melts if the current is too large; an MCB switches off automatically. Avoid overloading sockets and use ISI-marked appliances.</p>",
          [("Coil A: 50 turns; coil B: 100 turns; same current. Stronger?", ["more turns"], "coil B"), ("Why does a fuse wire melt?", ["too much current heats it"], "it protects the circuit")],
          ["Thinking an electromagnet stays magnetic after switching off.", "Using a thick copper wire as a fuse.", "Thinking heating is the only effect of current."],
          [("How can an electromagnet be made stronger?", "Increase the number of turns, increase the current or use a soft iron core."),
           ("Why is a fuse used in a circuit?", "Its thin wire melts when too much current flows, breaking the circuit and preventing fires.")],
          lambda: [("Magnetic effect of current", [(b["em"], 10), (c_magnet, 10)]), ("Electromagnets and their uses", [(eapp, 14), (b["em"], 6)]), ("Heating effect of current", [(eapp, 10), (c_magnet, 6), (b["em"], 4)]),
                   ("Fuses and safety", [(safe, 14), (b["em"], 6)]), ("Mixed problems", [(c_magnet, 14), (eapp, 6)])]),
        U(5, "exploring-forces", 5, PH,
          "Force as a push or a pull; effects of force on motion and shape; contact forces (muscular force, friction) and non-contact forces (gravitational, magnetic, electrostatic); increasing and reducing friction; mass and weight; net force (summary of NCERT Curiosity Chapter 5).",
          "Exploring Forces", "exploring forces",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 5: effects of force, contact and non-contact forces, friction and how to change it, gravity, mass and weight, and net force. 100 questions with answers.",
          "A force is a push or a pull.", "Weight = mass × g; friction opposes motion.",
          "<p>A force is a push or a pull measured in newtons. It can start or stop motion, change speed or direction, and change shape. Contact forces need touching (muscular force, friction); non-contact forces act at a distance (gravity, magnetic and electrostatic forces).</p>"
          "<p>Friction opposes motion between surfaces: treads and spikes increase it, while oil, ball bearings and wheels reduce it. Weight is the pull of gravity: weight = mass × g (about 10 N for each kilogram on Earth), and on the Moon it is about one-sixth. Forces in the same direction add; opposite forces subtract.</p>",
          [("Weight of a 30 kg child (g = 10)?", ["W = m × g"], "300 N"), ("Pulls of 400 N and 350 N in opposite directions. Net force?", ["400 − 350"], "50 N")],
          ["Confusing mass (kg) with weight (N).", "Thinking friction always helps motion.", "Adding forces that act in opposite directions."],
          [("What is the difference between mass and weight?", "Mass is the amount of matter (kg) and does not change; weight is the force of gravity on it (N) and changes from place to place."),
           ("How can friction be reduced?", "By lubricating with oil or grease, using ball bearings or wheels, and making surfaces smooth.")],
          lambda: [("What forces do", [(feff, 7), (b["f"], 13)]), ("Contact and non-contact forces", [(ftype, 16), (b["f"], 4)]), ("Friction", [(fric, 14), (b["f"], 6)]),
                   ("Mass and weight", [(c_weight, 14), (c_net, 6)]), ("Mixed problems", [(c_net, 6), (c_weight, 4), (ftype, 4), (fric, 4), (b["f"], 2)])]),
        U(6, "pressure-winds-storms-and-cyclones", 6, ES,
          "Pressure as force per unit area; pressure in liquids and its increase with depth; atmospheric pressure; air moving from high to low pressure; winds, monsoons, thunderstorms and cyclones; weather instruments and safety during storms (summary of NCERT Curiosity Chapter 6).",
          "Pressure, Winds, Storms and Cyclones", "pressure, winds and cyclones",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 6: pressure = force ÷ area, pressure in liquids, atmospheric pressure, winds from high to low pressure, thunderstorms, cyclones and safety. 100 questions with answers.",
          "Pressure = force ÷ area.", "Wind blows from high pressure to low pressure.",
          "<p>Pressure is the force acting on a unit area: pressure = force ÷ area, measured in pascals (N/m²). The same force on a smaller area gives more pressure, which is why knives are sharp and bag straps are wide. Liquid pressure increases with depth, so dams are thicker at the bottom. Air also exerts pressure, which falls as we go higher.</p>"
          "<p>Warm air rises, leaving low pressure, and wind blows from high pressure to low pressure. Uneven heating of land and sea brings the monsoon. A cyclone is a huge storm spinning around a low-pressure eye; the IMD gives warnings, and people should move to safe shelters.</p>",
          [("100 N on 0.5 m²?", ["P = F ÷ A"], "200 Pa"), ("Which hole spurts water farthest?", ["pressure increases with depth"], "the lowest hole")],
          ["Thinking a larger area gives more pressure.", "Saying wind blows from low to high pressure.", "Watching a cyclone from the beach."],
          [("Why does a sharp knife cut better?", "Its thin edge has a very small area, so the same force produces a much greater pressure."),
           ("What is a cyclone?", "A very large storm in which strong winds spiral around a centre of very low pressure called the eye.")],
          lambda: [("What is pressure?", [(K(c_press, "P"), 10), (c_press2, 6), (b["pr"], 4)]), ("Pressure in liquids and air", [(b["pr"], 10), (K(c_press, "F"), 5), (K(c_press, "A"), 5)]),
                   ("Winds and air pressure", [(b["pr"], 7), (weather, 9), (c_press2, 4)]), ("Thunderstorms and cyclones", [(storm, 16), (c_press2, 4)]), ("Mixed problems", [(c_press, 10), (c_press2, 10)])]),
        U(7, "particulate-nature-of-matter", 7, MT,
          "Matter is made of tiny particles with spaces between them; particles are always moving and attract each other; diffusion and the effect of temperature; arrangement and movement of particles in solids, liquids and gases; changes of state, melting and boiling points; sublimation; expansion on heating (summary of NCERT Curiosity Chapter 7).",
          "Particulate Nature of Matter", "particulate nature of matter",
          "Free CBSE Class 8 Science worksheets for NCERT Curiosity Chapter 7: particles and spaces in matter, diffusion, solids, liquids and gases, interparticle attraction, melting and boiling points and sublimation. 100 questions with answers.",
          "Matter is made of tiny, moving particles.", "Solids: close and fixed. Liquids: close and sliding. Gases: far apart and free.",
          "<p>All matter is made of tiny particles with spaces between them. The particles are always moving and attract one another. They spread and mix by diffusion, which is fastest in gases and faster when it is hotter: a crystal of potassium permanganate colours all the water, and the smell of hot food travels quickly.</p>"
          "<p>In solids particles are packed closely and only vibrate, so solids have a fixed shape and volume. In liquids they slide past one another, so liquids flow. In gases they move freely and far apart, so gases fill their container and can be compressed. Heating gives particles energy, causing melting, boiling and expansion; camphor sublimes directly into vapour.</p>",
          [("Where is diffusion fastest?", ["gas particles move fastest"], "in gases"), ("Can a gas be compressed?", ["large spaces between particles"], "yes, easily")],
          ["Thinking dissolved sugar is destroyed.", "Saying particles stop moving in solids.", "Thinking a liquid has a fixed shape."],
          [("What is diffusion?", "The spreading and mixing of the particles of one substance among the particles of another; it is faster at higher temperatures."),
           ("Why do gases fill their container?", "Their particles are far apart, attract each other weakly and move freely in all directions.")],
          lambda: [("Particles of matter", [(b["pm"], 14), (part, 6)]), ("Diffusion", [(b["pm"], 8), (part, 12)]), ("Solids, liquids and gases", [(part, 14), (c_mp, 6)]),
                   ("Changes of state", [(c_mp, 17), (b["pm"], 3)]), ("Mixed problems", [(c_mp, 16), (part, 4)])]),
    ]
