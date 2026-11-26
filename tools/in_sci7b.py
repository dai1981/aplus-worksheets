# -*- coding: utf-8 -*-
"""Class 7 Science (NCERT Curiosity, chapters 7–12): question makers and UNITS7b()."""
from uk_alsci import tq, nf, once_maker
from in_sci import pairs, _R, U, K
from in_sci6a import NS, LW, MT, PH, ES, odd_one, nq, _cap
import in_sci

# =================================================================== Chapter 7: heat transfer in nature
MODE = {"conduction": ["a steel spoon in hot tea getting hot at the handle", "the handle of a frying pan getting hot", "an iron rod heated at one end becoming hot at the other end",
                       "your hand warming when you hold a cup of hot milk", "ice melting faster on a metal plate than on a wooden board", "a tawa heating the roti placed on it"],
        "convection": ["warm air rising above a heater", "water at the bottom of a pan rising as it is heated", "a sea breeze blowing during the day",
                       "smoke rising from a chimney", "a land breeze blowing at night", "hot air balloons rising"],
        "radiation": ["feeling the warmth of the Sun", "feeling warm when sitting near a bonfire", "the Sun warming the Earth across empty space",
                      "the heat felt from a glowing electric heater a metre away", "a car parked in the sun getting hot inside", "drying clothes in sunlight"]}
HC = {"a good conductor of heat": ["copper", "aluminium", "iron", "steel", "silver", "brass", "gold", "a steel spoon", "an aluminium pan", "a copper vessel"],
      "a poor conductor (insulator) of heat": ["wood", "plastic", "air", "wool", "cork", "thermocol", "cloth", "rubber", "a clay pot", "a cotton quilt", "a wooden spatula"]}
HEATQ = [("What is conduction?", "heat moving from the hotter part to the colder part of a solid, without the solid itself moving", ["heat carried by moving liquids and gases", "heat travelling as rays through empty space", "heat stopping at the surface"], "It happens mainly in solids."),
         ("What is convection?", "heat carried by the movement of a heated liquid or gas", ["heat moving along a solid rod", "heat travelling through empty space", "heat stopping in water"], "Warm fluid rises and cooler fluid sinks."),
         ("What is radiation?", "heat travelling without needing any material in between", ["heat carried by water currents", "heat moving along a metal spoon", "heat stored in ice"], "The Sun's heat reaches us by radiation."),
         ("Why does a sea breeze blow during the day?", "land heats faster than the sea, warm air over land rises and cooler air from the sea moves in", ["the sea heats faster than land", "the wind comes from the mountains", "the Moon pulls the air"], "This is convection."),
         ("Why does a land breeze blow at night?", "land cools faster than the sea, so air over the sea is warmer and rises, and air from land moves out", ["land is warmer at night", "the sea freezes at night", "the Sun pulls the air"], "Fishermen use the land breeze to sail out."),
         ("Why do we wear light-coloured clothes in summer?", "light colours reflect more of the Sun's heat", ["light colours absorb more heat", "dark colours keep us cool", "colour has no effect"], "Dark colours absorb more heat."),
         ("Why do woollen clothes keep us warm in winter?", "wool traps air, which is a poor conductor of heat", ["wool produces heat", "wool is a good conductor", "wool absorbs cold"], "Two thin blankets keep us warmer than one thick one, because of the air between them."),
         ("Why are cooking pans made of metal with plastic or wooden handles?", "metal conducts heat to the food; plastic and wood do not, so the handle stays cool", ["plastic conducts heat well", "wood is a metal", "metal handles stay cool"], "Insulators protect our hands."),
         ("Why is the bottom of a cooking vessel sometimes coated with copper?", "copper is a very good conductor and spreads heat quickly", ["copper is an insulator", "copper is light", "copper keeps food cold"], "Food cooks evenly."),
         ("Why is a heater placed near the floor and an air conditioner near the ceiling?", "warm air rises and cool air sinks", ["warm air sinks", "cool air rises", "it does not matter"], "This uses convection currents."),
         ("Why are ventilators placed near the ceiling of rooms?", "warm air rises and goes out through them", ["cold air goes out", "light comes in", "to let rain in"], "Fresh cool air comes in from below."),
         ("How does heat from the Sun reach the Earth?", "by radiation", ["by conduction", "by convection", "it does not reach the Earth"], "Space has no air for conduction or convection."),
         ("Why does a black road feel hotter than a white wall in the sun?", "dark surfaces absorb more radiation", ["dark surfaces reflect more heat", "white walls make heat", "black roads are made of metal"], "Light surfaces reflect more."),
         ("Why are houses in hot places often painted white?", "white walls reflect sunlight and keep the house cooler", ["white walls absorb heat", "white paint is cheaper", "white paint makes heat"], "Dark roofs get much hotter."),
         ("What happens to water when it is heated from the bottom of a pan?", "warm water rises and cooler water sinks, forming convection currents", ["it stays still", "only the top gets hot", "it freezes"], "A few crystals of potassium permanganate show the currents."),
         ("Why do ice cubes melt faster on a steel plate than on a plastic plate?", "steel conducts heat from the room to the ice faster", ["plastic is warmer", "steel is colder", "plastic conducts heat better"], "Conductors carry heat quickly."),
         ("What is the water cycle?", "the continuous movement of water by evaporation, condensation and precipitation", ["water staying in the sea forever", "water only flowing in rivers", "the freezing of water"], "The Sun's heat drives it."),
         ("What is infiltration?", "rainwater seeping into the soil", ["water evaporating from leaves", "water freezing in clouds", "water flowing in pipes"], "It refills groundwater."),
         ("What is groundwater?", "water stored in the soil and rocks below the ground", ["water in clouds", "water in the sea", "water in a bucket"], "We draw it with wells and handpumps."),
         ("Why should we not let all rainwater run off into drains?", "letting it soak into the ground refills groundwater", ["drains need the water", "rainwater is harmful", "runoff makes soil better"], "Rainwater harvesting helps."),
         ("What is an aquifer?", "a layer of rock or soil underground that holds water", ["a type of cloud", "a water tank on a roof", "a dam"], "Wells tap aquifers."),
         ("Why is a vacuum flask able to keep tea hot for hours?", "its double walls with empty space and shiny surfaces reduce heat loss", ["it heats the tea", "it is made of copper", "it has a fire inside"], "It cuts down conduction, convection and radiation."),
         ("Why do birds fluff up their feathers in winter?", "to trap air, which keeps them warm", ["to look bigger", "to fly faster", "to cool down"], "Air is a poor conductor of heat."),
         ("Why is a mud house cool in summer?", "mud and thick walls are poor conductors of heat", ["mud is a metal", "mud makes cold air", "mud reflects all light"], "Thatched roofs also help.")]
BREEZE = [("a sunny afternoon on a beach", "a sea breeze, from the sea towards the land"), ("a clear night by the sea", "a land breeze, from the land towards the sea"),
          ("noon at a seaside town in Kerala", "a sea breeze, from the sea towards the land"), ("2 a.m. at a fishing village", "a land breeze, from the land towards the sea"),
          ("a hot summer day at Marina Beach in Chennai", "a sea breeze, from the sea towards the land"), ("early morning before sunrise on the Konkan coast", "a land breeze, from the land towards the sea"),
          ("a sunny morning at Puri beach", "a sea breeze, from the sea towards the land"), ("midnight at a port in Gujarat", "a land breeze, from the land towards the sea"),
          ("3 p.m. on a hot day in Goa", "a sea breeze, from the sea towards the land"), ("late night on the Andaman coast", "a land breeze, from the land towards the sea"),
          ("a bright afternoon at Visakhapatnam", "a sea breeze, from the sea towards the land"), ("before dawn at Kanyakumari", "a land breeze, from the land towards the sea")]


def c_breeze(k=None):
    R = _R[0]
    when, a = R.choice(BREEZE)
    w = [x for x in ["a sea breeze, from the sea towards the land", "a land breeze, from the land towards the sea", "no wind at all, ever", "a wind straight down from the sky"] if x != a]
    return tq("Which breeze usually blows in this situation: %s?" % when, a, w, "By day land heats faster, so air flows from sea to land; at night land cools faster, so air flows from land to sea.")


# =================================================================== Chapter 8: measurement of time and motion
CLOCKS = [("a sundial", "showing the time of day by the shadow of a stick or a raised edge"), ("a water clock (ghatika)", "measuring time by the steady flow of water into or out of a vessel"),
          ("an hourglass (sand clock)", "measuring a fixed time as sand flows through a narrow neck"), ("a pendulum clock", "keeping time by the regular swings of a pendulum"),
          ("a quartz clock", "keeping time by the very regular vibrations of a quartz crystal"), ("an atomic clock", "keeping extremely accurate time using atoms"),
          ("a stopwatch", "measuring short time intervals such as in races")]


def c_speed(k=None):
    R = _R[0]
    k = k or R.choice(["s", "d", "t"])
    who = R.choice(["A bus", "A car", "A train", "A cyclist", "A scooter", "A truck"])
    v = R.choice([20, 25, 30, 36, 40, 45, 48, 50, 54, 60, 72, 75, 80, 90])
    t = R.choice([2, 3, 4, 5, 6, 1.5, 2.5])
    d = v * t
    if k == "s":
        return nq("%s covers %s km in %s hours. What is its average speed?" % (who, nf(d), nf(t)), v, [d * t, d + t, v / 2, v * 2], "km/h", "Speed = distance ÷ time = %s ÷ %s = %s km/h." % (nf(d), nf(t), nf(v)))
    if k == "d":
        return nq("%s moves at a steady speed of %d km/h. How far does it go in %s hours?" % (who, v, nf(t)), d, [v / t, v + t, d / 2, d * 2], "km", "Distance = speed × time = %d × %s = %s km." % (v, nf(t), nf(d)))
    return nq("%s travels %s km at a steady speed of %d km/h. How long does it take?" % (who, nf(d), v), t, [t * 2, t + 1, t / 2, v / d], "h", "Time = distance ÷ speed = %s ÷ %d = %s h." % (nf(d), v, nf(t)))


def c_speed2(k=None):
    R = _R[0]
    who = R.choice(["A runner", "A student", "A dog", "A horse", "A tortoise", "A rabbit", "A ball rolling on the floor"])
    v = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 15])
    if who == "A tortoise":
        v = R.choice([0.1, 0.2, 0.5])
    t = R.choice([5, 10, 20, 25, 30, 40, 50, 60])
    d = v * t
    return nq("%s covers %s m in %d s. What is the speed in metres per second?" % (who, nf(d), t), v, [d * t, d + t, v * 10, v / 10], "m/s", "Speed = %s ÷ %d = %s m/s." % (nf(d), t, nf(v)))


def c_kmh(k=None):
    R = _R[0]
    ms = R.choice([5, 10, 15, 20, 25, 30])
    kmh = ms * 18 // 5
    if R.random() < 0.5:
        return nq("Convert %d km/h into m/s." % kmh, ms, [kmh * 18 / 5, kmh / 60, kmh * 1000, ms * 2], "m/s", "1 km/h = 1000 m ÷ 3600 s = 5/18 m/s, so %d × 5/18 = %d m/s." % (kmh, ms))
    return nq("Convert %d m/s into km/h." % ms, kmh, [ms * 5 / 18, ms * 60, ms * 3600, kmh * 2], "km/h", "1 m/s = 3.6 km/h, so %d × 3.6 = %d km/h." % (ms, kmh))


def c_pend(k=None):
    R = _R[0]
    n = R.choice([10, 20, 25, 30, 40, 50])
    T = R.choice([0.5, 0.8, 1, 1.2, 1.5, 2, 2.5])
    tot = n * T
    if R.random() < 0.6:
        return nq("A pendulum makes %d oscillations in %s seconds. What is its time period?" % (n, nf(tot)), T, [tot * n, n / tot, tot - n, T * 2], "s",
                  "Time period = total time ÷ number of oscillations = %s ÷ %d = %s s." % (nf(tot), n, nf(T)))
    return nq("A pendulum has a time period of %s s. How long does it take to make %d oscillations?" % (nf(T), n), tot, [n / T, n + T, tot / 2, tot * 2], "s",
              "Time = %d × %s = %s s." % (n, nf(T), nf(tot)))


def c_time(k=None):
    R = _R[0]
    k = k or R.choice(["min", "h", "day"])
    if k == "min":
        m = R.choice([2, 3, 4, 5, 7, 8, 10, 12, 15])
        return nq("How many seconds are there in %d minutes?" % m, m * 60, [m * 100, m * 10, m + 60, m * 3600], "s", "1 min = 60 s, so %d × 60 = %d s." % (m, m * 60))
    if k == "h":
        h = R.choice([2, 3, 4, 5, 6])
        return nq("How many minutes are there in %d hours?" % h, h * 60, [h * 100, h * 3600, h + 60, h * 24], "min", "1 h = 60 min, so %d × 60 = %d min." % (h, h * 60))
    s = R.choice([120, 180, 240, 300, 600, 900, 1800, 3600])
    return nq("Convert %d seconds into minutes." % s, s // 60, [s // 100, s * 60, s // 10, s // 3600 if s >= 3600 else s // 30], "min", "%d ÷ 60 = %d min." % (s, s // 60))


UNI = {"uniform motion": ["a car moving at a steady 60 km/h on an empty highway", "the tip of a clock's second hand moving round at a steady rate", "a train running at a constant speed on a straight track",
                          "a conveyor belt moving at a steady speed", "a ceiling fan turning at a steady speed", "a metro train cruising at a steady speed between stations", "an escalator carrying people up"],
       "non-uniform motion": ["a bus in city traffic", "a ball rolling down a slope and slowing on grass", "a child running and stopping in a playground",
                              "a car slowing down at a red light", "a train leaving a station", "a ball thrown up in the air", "a cyclist going uphill and then downhill", "an auto-rickshaw in a busy market"]}
TIMEQ = [("What is the SI unit of time?", "the second (s)", ["the minute", "the hour", "the day"], "Other units are built from it."),
         ("What is one oscillation of a simple pendulum?", "the bob moving from one end to the other and back", ["the bob moving from the centre to one end", "the bob staying still", "the string breaking"], "Time period is the time for one oscillation."),
         ("What is the time period of a pendulum?", "the time taken for one complete oscillation", ["the length of its string", "the mass of its bob", "the number of swings in a day"], "It is measured in seconds."),
         ("Does the time period of a pendulum change if a heavier bob is used (same length)?", "no, it stays nearly the same", ["yes, it doubles", "yes, it becomes zero", "yes, it halves"], "It depends on the length."),
         ("What happens to the time period of a pendulum if its string is made longer?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "Longer pendulums swing more slowly."),
         ("Why do we time 20 oscillations instead of one to find the time period?", "it reduces the error in timing", ["it makes the pendulum heavier", "one oscillation cannot be seen", "the rule says so"], "Divide the total time by 20."),
         ("What is speed?", "the distance travelled in one unit of time", ["the time taken for one unit of distance", "the mass of an object", "the length of a path"], "Speed = distance ÷ time."),
         ("What is the SI unit of speed?", "metres per second (m/s)", ["kilometres", "seconds", "kilograms"], "km/h is also common."),
         ("What does a speedometer show?", "the speed of a vehicle at that moment", ["the distance between towns", "the time of day", "the fuel used"], "The odometer shows the distance travelled."),
         ("What does an odometer measure?", "the distance travelled by a vehicle", ["its speed", "its mass", "the time"], "It is next to the speedometer."),
         ("What is average speed?", "the total distance divided by the total time", ["the highest speed", "the speed at the start", "the number of stops"], "Speed usually changes during a trip."),
         ("Which is faster: 20 m/s or 54 km/h?", "20 m/s", ["54 km/h", "both are the same", "it cannot be told"], "54 km/h = 15 m/s."),
         ("What is uniform motion?", "motion along a straight line at a constant speed", ["motion with changing speed", "standing still", "moving in circles at changing speed"], "Equal distances in equal times."),
         ("How did people in ancient India measure time with water?", "a bowl with a small hole (ghatika) that slowly sank in water", ["with a quartz watch", "with an atomic clock", "with a digital phone"], "One ghatika was about 24 minutes."),
         ("What is a leap year?", "a year with 366 days, which comes every four years", ["a year with 365 days", "a year with 360 days", "a year with no February"], "It adds an extra day in February."),
         ("What does the slope of a distance–time graph show?", "the speed: a steeper line means faster motion", ["the mass", "the temperature", "the time only"], "A flat line means the object is at rest."),
         ("What does a horizontal line on a distance–time graph mean?", "the object is not moving", ["it moves very fast", "it moves backwards", "it is speeding up"], "Distance stays the same."),
         ("Why are atomic clocks used to set the standard time?", "they are extremely accurate", ["they are cheap", "they are made of sand", "they use the Sun"], "India's standard time is kept by the National Physical Laboratory."),
         ("How long does it take for the Earth to spin once?", "about 24 hours (one day)", ["one month", "one year", "one hour"], "This gives day and night."),
         ("Which Indian organisation keeps the national standard of time (Indian Standard Time)?", "the CSIR–National Physical Laboratory, New Delhi", ["ISRO", "the Indian Railways", "the Reserve Bank of India"], "It uses atomic clocks.")]

# =================================================================== Chapter 9: life processes in animals
DIG = [("the mouth", "chewing food and mixing it with saliva"), ("the oesophagus (food pipe)", "carrying food from the mouth to the stomach"),
       ("the stomach", "churning food with acid and digestive juices that break down proteins"), ("the small intestine", "completing digestion and absorbing nutrients into the blood"),
       ("the large intestine", "absorbing water and some salts from undigested food"), ("the liver", "making bile, which helps digest fats"),
       ("the pancreas", "making pancreatic juice that digests carbohydrates, proteins and fats"), ("the rectum", "storing undigested waste for a short time"),
       ("the anus", "removing undigested waste from the body (egestion)"), ("the salivary glands", "making saliva, which begins to digest starch")]
TEETH = [("incisors", "cutting and biting food"), ("canines", "tearing food"), ("premolars", "chewing and grinding food"), ("molars", "grinding food with their broad surfaces")]
BREATH = [("fish", "gills"), ("an earthworm", "its moist skin"), ("a cockroach", "spiracles and air tubes (tracheae)"), ("a human", "lungs"),
          ("a frog", "lungs and its moist skin"), ("a whale", "lungs, through a blowhole"), ("a grasshopper", "spiracles and air tubes (tracheae)"), ("a cow", "lungs"),
          ("a tadpole", "gills"), ("a dolphin", "lungs, through a blowhole")]
ANQ = [("What is digestion?", "breaking down complex food into simple substances the body can absorb", ["taking food into the mouth", "removing waste from the body", "breathing in air"], "It happens in the digestive tract."),
       ("Where does the digestion of starch begin?", "in the mouth, by saliva", ["in the stomach", "in the large intestine", "in the liver"], "Chew a piece of roti for a while; it tastes sweet."),
       ("Why does a piece of roti taste sweet after chewing it for a while?", "saliva breaks starch into sugar", ["the roti contains sugar crystals", "the teeth make sugar", "it gets hot"], "This shows digestion begins in the mouth."),
       ("Why does the stomach make hydrochloric acid?", "it kills germs and helps digestive juices act on proteins", ["it digests starch", "it makes bile", "it absorbs water"], "Mucus protects the stomach wall from the acid."),
       ("What does bile do?", "it breaks fats into tiny droplets so they are digested easily", ["it digests proteins", "it absorbs water", "it makes sugar"], "Bile is made in the liver and stored in the gall bladder."),
       ("What are villi?", "finger-like projections in the small intestine that absorb digested food", ["teeth in the stomach", "parts of the lungs", "hairs on the skin"], "They give a large surface area."),
       ("Which is the longest part of the digestive tract?", "the small intestine", ["the stomach", "the oesophagus", "the large intestine"], "It is about 7.5 m long in adults."),
       ("What is absorption?", "digested food passing into the blood through the intestine wall", ["taking food into the mouth", "removing waste", "breaking down food"], "It happens mainly in the small intestine."),
       ("What is assimilation?", "the body using absorbed food to build new parts and get energy", ["chewing food", "swallowing food", "removing waste"], "Cells use glucose and amino acids."),
       ("What is egestion?", "removing undigested food from the body through the anus", ["taking in food", "absorbing food", "breathing out"], "It is the last step of digestion."),
       ("How does an Amoeba take in food?", "it surrounds the food with finger-like projections (pseudopodia) and forms a food vacuole", ["it chews with teeth", "it uses a tongue", "it makes food in sunlight"], "Digestion happens in the food vacuole."),
       ("What is a ruminant?", "a grass-eating animal that swallows food quickly and later chews the cud", ["an animal that eats only meat", "an insect", "a fish"], "Cows, buffaloes and goats are ruminants."),
       ("What is the cud?", "partly digested food brought back from the rumen to the mouth for chewing", ["the milk of a cow", "a kind of tooth", "the waste of an animal"], "Ruminants chew the cud while resting."),
       ("Why can cows digest grass but humans cannot?", "bacteria in their stomach break down cellulose", ["cows have more teeth", "humans have no stomach", "grass has no nutrients"], "Humans pass cellulose out as fibre."),
       ("What is the role of the tongue in digestion?", "it mixes food with saliva and pushes it back for swallowing", ["it digests fats", "it absorbs water", "it makes bile"], "It also tastes the food."),
       ("Why should we chew food properly?", "small pieces mix better with saliva and are digested easily", ["it makes food cold", "it makes the food bigger", "it is not needed"], "Chewing is the first step of digestion."),
       ("What happens when we breathe in?", "the chest expands, the diaphragm moves down and air fills the lungs", ["the chest becomes smaller", "the diaphragm moves up", "air leaves the lungs"], "This is inhalation."),
       ("What happens when we breathe out?", "the diaphragm moves up, the chest becomes smaller and air is pushed out", ["the chest expands", "the diaphragm moves down", "air enters the lungs"], "This is exhalation."),
       ("How is exhaled air different from inhaled air?", "it has more carbon dioxide and water vapour and less oxygen", ["it has more oxygen", "it has no carbon dioxide", "it is exactly the same"], "Breathe on a mirror to see the water vapour."),
       ("What happens when exhaled air is bubbled through lime water?", "the lime water turns milky", ["it turns blue", "it boils", "nothing happens"], "This shows carbon dioxide in exhaled air."),
       ("What is cellular respiration?", "the breaking down of food in cells to release energy", ["breathing air in and out", "eating food", "removing waste"], "It needs oxygen in most living things."),
       ("Why do we breathe faster after running?", "the muscles need more oxygen to release more energy", ["the lungs get smaller", "we are hungry", "we need less air"], "The breathing rate rises with exercise."),
       ("Why do we sometimes get cramps after hard exercise?", "muscles release energy without enough oxygen and lactic acid builds up", ["muscles get too much oxygen", "bones break", "the heart stops"], "Rest and a gentle massage help."),
       ("What is the windpipe called?", "the trachea", ["the oesophagus", "the diaphragm", "the alveolus"], "It carries air to the lungs."),
       ("Why does the nose have hairs and mucus?", "to trap dust and germs from the air we breathe", ["to smell better only", "to make air hot", "to store oxygen"], "Breathe through the nose, not the mouth."),
       ("Why do we sneeze?", "to push out dust or irritants from the nose", ["to take in more oxygen", "because of hunger", "to digest food"], "Cover your mouth when you sneeze."),
       ("What is the breathing rate of an adult at rest?", "about 15–18 breaths per minute", ["about 1 breath per minute", "about 100 breaths per minute", "about 500 breaths per minute"], "It increases during exercise."),
       ("Which muscular sheet below the lungs helps in breathing?", "the diaphragm", ["the stomach", "the liver", "the heart"], "It moves down when we breathe in."),
       ("Which teeth are the sharpest for tearing meat?", "canines", ["molars", "premolars", "incisors"], "Lions and dogs have large canines."),
       ("How many sets of teeth does a human get in a lifetime?", "two: milk teeth and permanent teeth", ["one", "three", "four"], "Milk teeth fall out and permanent teeth replace them.")]


JUICE = [("saliva", "starch, changing it into sugar"), ("gastric juice in the stomach", "proteins"), ("bile", "fats, by breaking them into tiny droplets"),
         ("pancreatic juice", "carbohydrates, proteins and fats"), ("intestinal juice", "the final breakdown of all kinds of food into simple substances")]
AIR = {"true of the air we breathe in": ["it has about 21% oxygen", "it has very little carbon dioxide", "it does not turn lime water milky quickly", "it is usually cooler than our body", "it has less water vapour than exhaled air"],
       "true of the air we breathe out": ["it has more carbon dioxide", "it turns lime water milky", "it has more water vapour", "it is warm", "it has less oxygen"]}


def c_breaths(k=None):
    R = _R[0]
    r = R.choice([12, 14, 15, 16, 18, 20, 24, 30])
    m = R.choice([5, 10, 15, 30, 60])
    who = R.choice(in_sci.GIRLS + in_sci.BOYS)
    act = R.choice(["at rest", "after a short walk", "after skipping", "after running"])
    return nq("%s takes %d breaths per minute %s. How many breaths is that in %d minutes, at the same rate?" % (who, r, act, m), r * m, [r + m, r * m / 2, r * 60, m * 60], "breaths",
              "%d × %d = %d breaths." % (r, m, r * m)) if m != 60 else nq("At a rate of %d breaths per minute, how many breaths are taken in one hour?" % r, r * 60, [r + 60, r * 24, r * 100, r * 6], "breaths",
                                                                          "1 hour = 60 minutes, so %d × 60 = %d breaths." % (r, r * 60))


# =================================================================== Chapter 10: life processes in plants
PLQ = [("What is photosynthesis?", "the process by which green plants make food from carbon dioxide and water using sunlight", ["the breaking down of food to release energy", "the loss of water from leaves", "the movement of water up the stem"], "Chlorophyll captures sunlight."),
       ("Which gas do plants take in for photosynthesis?", "carbon dioxide", ["oxygen", "nitrogen", "hydrogen"], "They give out oxygen."),
       ("Which gas is given out during photosynthesis?", "oxygen", ["carbon dioxide", "nitrogen", "methane"], "Animals use this oxygen."),
       ("What is the green pigment in leaves called?", "chlorophyll", ["haemoglobin", "melanin", "keratin"], "It traps the energy of sunlight."),
       ("Where in a leaf is chlorophyll found?", "in chloroplasts inside the leaf cells", ["in the stomata only", "in the veins only", "in the roots"], "Leaves are green because of it."),
       ("What are stomata?", "tiny pores on leaves through which gases enter and leave", ["roots of a plant", "seeds", "flowers"], "Guard cells open and close them."),
       ("What is the food made in photosynthesis stored as?", "starch", ["protein", "fat only", "salt"], "Iodine turns starch blue-black."),
       ("Why is a leaf boiled in alcohol before testing it for starch?", "to remove the green chlorophyll so the colour change can be seen", ["to add starch", "to kill the iodine", "to make it green"], "The leaf becomes pale."),
       ("A leaf from a plant kept in the dark for two days gives no blue-black colour with iodine. Why?", "no starch was made without sunlight", ["the leaf had too much starch", "iodine does not work on leaves", "the leaf was too green"], "Light is needed for photosynthesis."),
       ("In a variegated leaf, which parts turn blue-black with iodine?", "only the green parts", ["only the white parts", "the whole leaf", "no part"], "Chlorophyll is needed for photosynthesis."),
       ("What is transpiration?", "the loss of water as vapour from the leaves, mainly through stomata", ["the making of food", "the absorption of water by roots", "the movement of food"], "It cools the plant and pulls water up."),
       ("How does transpiration help a plant?", "it pulls water up from the roots and cools the leaves", ["it makes food", "it makes seeds", "it removes all water"], "A tall tree pulls water many metres up."),
       ("What do xylem vessels carry?", "water and minerals from the roots to the leaves", ["food from the leaves to all parts", "air into the roots", "seeds to the soil"], "Phloem carries food."),
       ("What does phloem carry?", "food made in the leaves to other parts of the plant", ["water from the roots", "air", "soil"], "Xylem carries water."),
       ("What are root hairs for?", "absorbing water and minerals from the soil", ["making food", "breathing only", "making flowers"], "They increase the surface for absorption."),
       ("Do plants respire?", "yes, all parts respire day and night", ["only at night", "only in sunlight", "no, never"], "They use oxygen and give out carbon dioxide."),
       ("Why do plants give out more oxygen than they use during the day?", "photosynthesis is faster than respiration in bright light", ["they stop respiring", "they absorb no carbon dioxide", "they make no food"], "At night they only respire."),
       ("What is an autotroph?", "a living thing that makes its own food", ["one that eats other living things", "a decomposer only", "a parasite"], "Green plants are autotrophs."),
       ("What is a heterotroph?", "a living thing that depends on others for food", ["one that makes its own food", "a green plant", "a stone"], "Animals and fungi are heterotrophs."),
       ("How does a pitcher plant get extra nutrients?", "it traps and digests insects", ["it eats soil", "it steals from other plants", "it absorbs dead leaves only"], "It lives in soil poor in nitrogen."),
       ("What is Cuscuta (amarbel)?", "a parasitic plant that takes food from its host plant", ["an insect-eating plant", "a fungus", "a fern"], "It has no chlorophyll."),
       ("What is a saprotroph?", "an organism that feeds on dead and decaying matter", ["a green plant", "a parasite on animals", "an insect-eating plant"], "Mushrooms and bread mould are saprotrophs."),
       ("What is symbiosis?", "two different organisms living together and helping each other", ["one organism killing another", "a plant eating insects", "a plant making food"], "Lichens are an alga and a fungus together."),
       ("Why do farmers grow pulses in fields?", "Rhizobium bacteria in their root nodules fix nitrogen in the soil", ["pulses take nitrogen out", "pulses kill bacteria", "pulses need no soil"], "This reduces the need for fertilisers."),
       ("What would happen to a potted plant if it were covered with a polythene bag in sunlight?", "drops of water would collect inside the bag", ["the bag would fill with soil", "the plant would grow roots in the bag", "nothing at all"], "This shows transpiration."),
       ("Which raw materials do plants need for photosynthesis?", "carbon dioxide, water and sunlight, with chlorophyll", ["oxygen and sugar", "soil and sand", "nitrogen only"], "Glucose and oxygen are made."),
       ("What happens to the glucose made in leaves?", "it is used for energy or changed into starch and stored", ["it is thrown away", "it turns into water", "it becomes oxygen"], "Potatoes store starch."),
       ("Why are leaves usually broad and flat?", "to capture more sunlight", ["to store water only", "to look pretty", "to hold soil"], "Thin leaves also let gases reach the cells quickly."),
       ("Why do the leaves of some plants look red or yellow but still make food?", "they have chlorophyll hidden by other pigments", ["they make food without chlorophyll", "they eat insects", "they get food from soil"], "Crotons are an example."),
       ("Why do desert plants such as cactus have spines instead of leaves?", "to reduce water loss by transpiration", ["to make more food", "to attract insects", "to breathe faster"], "The green stem makes food."),
       ("When do stomata usually open?", "during the day, when light is available for photosynthesis", ["only at night", "never", "only in winter"], "They close to save water."),
       ("What would happen to a plant kept in a sealed jar with no carbon dioxide?", "it could not make food by photosynthesis", ["it would grow faster", "it would make more oxygen", "nothing would change"], "Carbon dioxide is a raw material."),
       ("Why are the roots of a plant not green?", "they grow in the dark soil and have no chlorophyll", ["they make the most food", "they are dead", "they are covered in paint"], "They store food made in the leaves."),
       ("How does water reach the top of a tall coconut tree?", "transpiration from the leaves pulls water up through the xylem", ["the roots push it up like a pump only", "rain falls on top", "the bark carries it"], "Water travels in thin tubes.")]
PHOTO = {"a raw material or requirement for photosynthesis": ["sunlight", "carbon dioxide", "water", "chlorophyll"],
         "a product of photosynthesis": ["oxygen", "glucose", "starch (made from glucose)"]}
NUTMODE = {"an autotroph": ["a mango tree", "grass", "a tulsi plant", "algae in a pond", "a rose plant"],
           "a parasite": ["Cuscuta (amarbel)", "a tapeworm", "a louse", "a mosquito feeding on blood"],
           "a saprotroph": ["a mushroom", "bread mould", "yeast feeding on dead matter", "bacteria of decay"],
           "an insectivorous plant": ["the pitcher plant", "the Venus flytrap", "the sundew", "the bladderwort"]}
PPART = [("roots", "absorbing water and minerals and holding the plant in the soil"), ("the stem", "carrying water and food and holding up the leaves"),
         ("leaves", "making food by photosynthesis"), ("stomata", "letting carbon dioxide in and oxygen and water vapour out"), ("xylem", "carrying water up from the roots"),
         ("phloem", "carrying food from the leaves"), ("chlorophyll", "trapping the energy of sunlight"), ("root nodules of pulses", "housing bacteria that fix nitrogen")]

# =================================================================== Chapter 11: light — shadows and reflections
LUM = {"a luminous object (gives its own light)": ["the Sun", "a candle flame", "a glowing bulb", "a firefly", "a burning matchstick", "a star", "a lit diya", "a glowing tube light", "a campfire", "a torch that is switched on"],
       "a non-luminous object (seen by reflected light)": ["the Moon", "a mirror", "a book", "a tree", "the Earth", "a wall", "a steel plate", "a switched-off bulb", "a cloud", "your hand"]}
LQ = [("How does light travel?", "in straight lines", ["in curves only", "in circles", "only through water"], "This is why shadows form."),
      ("Why do shadows form?", "opaque objects block light, which travels in straight lines", ["light bends around objects", "transparent objects block light", "objects make dark rays"], "A shadow needs a source of light, an opaque object and a screen."),
      ("What three things are needed to see a shadow?", "a source of light, an opaque object and a screen", ["a mirror, a lens and a prism", "only an object", "only the Sun"], "The ground or a wall can act as a screen."),
      ("What colour is a shadow?", "always dark, whatever the colour of the object", ["the same colour as the object", "white", "rainbow-coloured"], "A red ball casts a dark shadow."),
      ("What happens to the size of a shadow when the object is moved closer to the light source?", "it becomes bigger", ["it becomes smaller", "it stays the same", "it disappears"], "Move the object away and the shadow shrinks."),
      ("Why is your shadow shortest at noon?", "the Sun is high overhead", ["the Sun is low", "there is no Sun", "the ground moves"], "Shadows are long in the morning and evening."),
      ("What kind of image does a pinhole camera form?", "an upside-down (inverted) image", ["an upright image", "no image", "a coloured shadow"], "Light rays cross at the pinhole."),
      ("What happens to the image in a pinhole camera if the hole is made very large?", "it becomes blurred", ["it becomes sharper", "it becomes upright", "it becomes coloured"], "A small hole gives a sharp image."),
      ("What is reflection?", "light bouncing back from a surface", ["light passing through glass", "light being made", "light being absorbed only"], "Mirrors reflect light very well."),
      ("What is the angle of incidence equal to when light is reflected from a plane mirror?", "the angle of reflection", ["twice the angle of reflection", "90°", "zero always"], "This is a law of reflection."),
      ("What is the normal in reflection?", "a line drawn at right angles to the mirror where the ray hits it", ["the mirror itself", "the reflected ray", "a line parallel to the mirror"], "Angles are measured from the normal."),
      ("How far behind a plane mirror is the image of an object?", "as far behind as the object is in front", ["twice as far", "half as far", "on the mirror surface"], "The image is the same size as the object."),
      ("What is lateral inversion?", "the left and right sides of an image appearing swapped in a mirror", ["the image being upside down", "the image being larger", "the image being coloured"], "Raise your right hand: the image raises its left."),
      ("Why is 'AMBULANCE' written in reverse on the front of ambulances?", "drivers ahead see it the right way round in their rear-view mirrors", ["to look beautiful", "because of a printing mistake", "to confuse people"], "Mirrors cause lateral inversion."),
      ("What kind of image does a plane mirror form?", "upright, the same size and laterally inverted", ["upside down and smaller", "upright and larger", "upside down and the same size"], "It is behind the mirror."),
      ("What is a periscope used for?", "seeing over obstacles, using two mirrors", ["making things bigger", "measuring time", "splitting light into colours"], "Submarines use periscopes."),
      ("How are the mirrors in a simple periscope placed?", "parallel to each other, each at 45° to the tube", ["at right angles to each other", "both flat on the bottom", "face to face at 90°"], "Light turns 90° at each mirror."),
      ("What makes the patterns in a kaleidoscope?", "repeated reflections from mirrors set at an angle", ["coloured lights inside", "a lens", "a battery"], "Small coloured pieces make the designs."),
      ("Why can you see yourself in a steel plate but not in a wooden board?", "smooth shiny surfaces reflect light regularly", ["wood absorbs all light", "steel gives out light", "wood is transparent"], "Rough surfaces scatter light."),
      ("What image does the back (outer) side of a shiny steel spoon form?", "an upright, smaller image", ["an upside-down, larger image", "no image", "an image the same size"], "It acts as a convex mirror."),
      ("Why are convex mirrors used as rear-view mirrors in vehicles?", "they give a wide view of the traffic behind", ["they make things larger", "they form upside-down images", "they need no light"], "The images are smaller and upright."),
      ("What kind of mirror is used by dentists to see teeth?", "a concave mirror", ["a convex mirror", "a plane mirror", "no mirror"], "It gives a magnified image when held close."),
      ("Why do we see the Moon?", "it reflects sunlight towards us", ["it makes its own light", "it is a star", "it burns"], "The Moon is non-luminous."),
      ("What is an eclipse in terms of shadows?", "one body moving into the shadow of another", ["a star exploding", "a cloud covering the Sun", "the Sun switching off"], "Shadows also cause eclipses in space."),
      ("Why can we see things around us?", "light from them enters our eyes", ["our eyes send out light", "objects give out sound", "air carries the picture"], "Non-luminous objects reflect light into our eyes.")]
SYMLET = list("AHIMOTUVWXY")
ASYM = list("BCDEFGJKLNPQRSZ")


def c_mirror(k=None):
    R = _R[0]
    k = k or R.choice(["angle", "dist", "between", "letter"])
    if k == "angle":
        i = R.choice([15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
        if R.random() < 0.5:
            return nq("A ray of light falls on a plane mirror. The angle of incidence is %d°. What is the angle of reflection?" % i, i, [90 - i, 2 * i, 180 - i, i / 2], "°",
                      "Angle of reflection = angle of incidence = %d°." % i)
        g = 90 - i
        return nq("A ray of light makes an angle of %d° with the surface of a plane mirror. What is the angle of reflection?" % g, i, [g, 2 * g, 180 - g, 90 + g], "°",
                  "Angles are measured from the normal: 90° − %d° = %d°, so the angle of reflection is %d°." % (g, i, i))
    if k == "dist":
        d = R.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80, 90, 100, 120, 125, 150, 175, 200])
        return nq("An object is placed %d cm in front of a plane mirror. How far behind the mirror is its image?" % d, d, [2 * d, d / 2, d + 10, 0], "cm",
                  "The image is as far behind the mirror as the object is in front: %d cm." % d)
    if k == "between":
        d = R.choice([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6])
        return nq("A boy stands %s m in front of a plane mirror. What is the distance between the boy and his image?" % nf(d), 2 * d, [d, d / 2, 4 * d, d + 1], "m",
                  "The image is %s m behind the mirror, so the distance is %s + %s = %s m." % (nf(d), nf(d), nf(d), nf(2 * d)))
    if R.random() < 0.5:
        a = R.choice(SYMLET)
        w = R.sample(ASYM, 3)
        return tq("Which of these capital letters looks the same when seen in a plane mirror held upright beside it: %s?" % ", ".join(sorted([a] + w)), a, w, "%s has a vertical line of symmetry." % a)
    a = R.choice(ASYM)
    sym = R.sample(SYMLET, 3)
    return tq("Which of these capital letters looks different (reversed) in a plane mirror held upright beside it: %s?" % ", ".join(sorted([a] + sym)), a, sym, "%s has no vertical line of symmetry, so lateral inversion changes it." % a)


# =================================================================== Chapter 12: Earth, Moon and the Sun
EMS = [("rotation", "the Earth spinning on its axis once in about 24 hours"), ("revolution", "the Earth going round the Sun once in about 365¼ days"),
       ("the axis", "an imaginary line through the North and South Poles about which the Earth spins"), ("the equator", "an imaginary line around the middle of the Earth"),
       ("an orbit", "the path of the Earth around the Sun or the Moon around the Earth"), ("a solar eclipse", "the Moon coming between the Sun and the Earth, blocking the Sun's light"),
       ("a lunar eclipse", "the Earth coming between the Sun and the Moon, so the Earth's shadow falls on the Moon"),
       ("the phases of the Moon", "the changing shapes of the lit part of the Moon that we see"), ("a new moon", "the phase when the Moon's lit side faces away from us and we cannot see it"),
       ("a full moon", "the phase when we see the whole lit face of the Moon"), ("a solstice", "a day when the day is the longest or the shortest of the year"), ("an equinox", "a day when day and night are nearly equal everywhere")]
PHASES = ["new moon", "waxing crescent", "first quarter", "waxing gibbous", "full moon", "waning gibbous", "last quarter", "waning crescent"]


def c_phase(k=None):
    R = _R[0]
    i = R.randrange(8)
    if R.random() < 0.5:
        a = PHASES[(i + 1) % 8]
        return tq("Which phase of the Moon comes just after the %s?" % PHASES[i], a, R.sample([p for p in PHASES if p not in (a, PHASES[i])], 3), "The order is " + " → ".join(PHASES) + " → new moon.")
    a = PHASES[(i - 1) % 8]
    return tq("Which phase of the Moon comes just before the %s?" % PHASES[i], a, R.sample([p for p in PHASES if p not in (a, PHASES[i])], 3), "The order is " + " → ".join(PHASES) + " → new moon.")


ECL = {"true of a solar eclipse": ["the Moon is between the Sun and the Earth", "it can happen only on a new moon day", "it must never be watched with the naked eye", "the Moon's shadow falls on the Earth",
                                   "it is seen only from a narrow strip of the Earth at a time", "the sky can turn dark during the day"],
       "true of a lunar eclipse": ["the Earth is between the Sun and the Moon", "it can happen only on a full moon night", "it is safe to watch with the naked eye", "the Earth's shadow falls on the Moon",
                                   "it can be seen from the whole night side of the Earth", "the Moon may look reddish"]}
DAYQ = {"caused by the Earth's rotation": ["day and night", "the Sun appearing to rise in the east and set in the west", "stars appearing to move across the night sky in a few hours",
                                          "a place facing the Sun having daytime", "shadows changing direction from morning to evening"],
        "caused by the Earth's revolution with its tilted axis": ["the seasons", "summer days being longer than winter days", "different constellations being seen in different months",
                                                                 "the noon Sun being higher in summer than in winter", "the change in the length of shadows at noon over the year"]}
HEMI = [("India", "N"), ("Japan", "N"), ("Egypt", "N"), ("the United Kingdom", "N"), ("Australia", "S"), ("South Africa", "S"), ("Argentina", "S"), ("New Zealand", "S")]


def c_hemi(k=None):
    R = _R[0]
    place, h = R.choice(HEMI)
    mon = R.choice(["June", "December"])
    summer = (h == "N") == (mon == "June")
    a = "summer" if summer else "winter"
    return tq("In %s, the North Pole is tilted %s the Sun. Which season is it in %s?" % (mon, "towards" if mon == "June" else "away from", place), a,
              [x for x in ["summer", "winter", "no season at all", "it is always spring"] if x != a],
              "%s is in the %s hemisphere, which is tilted %s the Sun in %s." % (_cap(place), "northern" if h == "N" else "southern", "towards" if summer else "away from", mon))
EQ = [("Why do we have day and night?", "the Earth rotates on its axis, so each place faces the Sun for part of the time", ["the Sun goes round the Earth every day", "the Moon blocks the Sun at night", "the Sun switches off at night"], "One rotation takes about 24 hours."),
      ("In which direction does the Earth rotate?", "from west to east", ["from east to west", "from north to south", "it does not rotate"], "So the Sun seems to rise in the east."),
      ("Why does the Sun appear to rise in the east?", "the Earth rotates from west to east", ["the Sun moves from east to west", "the east is warmer", "the Moon pushes the Sun"], "The stars seem to move the same way."),
      ("By how much is the Earth's axis tilted?", "about 23.5°", ["about 90°", "0°", "about 45°"], "The tilt causes the seasons."),
      ("What causes the seasons?", "the tilt of the Earth's axis as it goes round the Sun", ["the changing distance of the Moon", "the speed of rotation", "clouds"], "Places get more direct sunlight in summer."),
      ("Why are days longer in summer?", "our hemisphere is tilted towards the Sun", ["the Earth spins slower", "the Sun is bigger in summer", "the Moon is far away"], "Nights are longer in winter."),
      ("When it is summer in India (June), which season is it in Australia?", "winter", ["summer", "spring only", "there are no seasons there"], "The southern hemisphere is tilted away then."),
      ("Why do we see phases of the Moon?", "we see different amounts of its sunlit half as it moves round the Earth", ["the Earth's shadow covers it each night", "the Moon changes its size", "clouds cover parts of it"], "Half the Moon is always lit by the Sun."),
      ("How long does the Moon take to go from one full moon to the next?", "about 29.5 days", ["about 7 days", "about 365 days", "about 24 hours"], "This is the basis of many calendars."),
      ("Why do we always see the same face of the Moon?", "it takes the same time to spin once as to go round the Earth once", ["it does not rotate", "the Earth hides the other side", "it is flat"], "The far side was first photographed by spacecraft."),
      ("Why should we never look directly at the Sun during a solar eclipse?", "the strong light can damage our eyes", ["the Sun is cold then", "it is too dark to see", "it makes the eclipse end"], "Use special filters or a pinhole projector."),
      ("Why does a lunar eclipse not happen every full moon?", "the Moon's orbit is slightly tilted, so it usually passes above or below the Earth's shadow", ["the Earth stops moving", "the Moon is not lit", "the Sun is too far"], "Eclipses happen only when they line up."),
      ("How long does the Earth take to go once round the Sun?", "about 365¼ days", ["24 hours", "29.5 days", "100 years"], "The extra quarter day gives a leap year every four years."),
      ("What is the shape of the Earth's orbit around the Sun?", "nearly circular (a slightly stretched circle)", ["a square", "a straight line", "a zigzag"], "It is an ellipse that is almost a circle."),
      ("What would happen if the Earth stopped rotating?", "one side would have very long day and the other very long night", ["nothing would change", "seasons would stop only", "the Moon would vanish"], "Rotation gives day and night."),
      ("What is the Tropic of Cancer?", "the line of latitude at about 23.5° N where the Sun is overhead at noon around 21 June", ["the equator", "the North Pole", "a constellation"], "It passes through India."),
      ("When is the longest day of the year in India?", "around 21 June", ["around 21 December", "around 1 January", "around 15 August"], "This is the summer solstice."),
      ("What are equinoxes?", "the two days in a year when day and night are nearly equal everywhere", ["the longest days", "days with eclipses", "days with no Sun"], "They come around 21 March and 23 September."),
      ("What is the Moon?", "the Earth's natural satellite", ["a star", "a planet", "a comet"], "It has no light of its own."),
      ("Why are there no seasons on the Moon like on Earth?", "its axis is hardly tilted and it has no air", ["it is too small to be seen", "it moves too fast", "it is made of ice"], "Its days and nights are about two weeks long."),
      ("Which line of latitude divides the Earth into the northern and southern hemispheres?", "the equator", ["the Tropic of Cancer", "the Tropic of Capricorn", "the Arctic Circle"], "India is in the northern hemisphere."),
      ("When is the shortest day of the year in India?", "around 22 December", ["around 21 June", "around 21 March", "around 2 October"], "This is the winter solstice."),
      ("Why is it hotter at noon than in the early morning?", "the Sun's rays fall more directly at noon", ["the Sun is closer at noon", "the Earth stops at noon", "the Moon is far at noon"], "Slanting rays spread their heat."),
      ("Why are the polar regions cold even in their summer?", "the Sun's rays fall on them at a very slant angle", ["they never get sunlight", "they are closest to the Sun", "they have no air"], "They get months of daylight in summer."),
      ("What is a lunar eclipse sometimes called when the Moon looks red?", "a 'blood moon'", ["a blue moon", "a new moon", "a half moon"], "Sunlight bent by the Earth's air reaches it."),
      ("How long does a total solar eclipse last at one place?", "only a few minutes", ["several days", "a whole month", "a whole year"], "The Moon's shadow moves fast over the Earth."),
      ("What is the Tropic of Capricorn?", "the line of latitude at about 23.5° S where the Sun is overhead at noon around 22 December", ["the equator", "the South Pole", "a star group"], "It passes through Australia and Brazil."),
      ("Why does the Moon rise about 50 minutes later each day?", "it moves along its orbit round the Earth", ["the Earth stops", "the Moon grows bigger", "clouds slow it"], "It takes about a month to go round."),
      ("Which phase of the Moon is seen when the Moon is on the opposite side of the Earth from the Sun?", "full moon", ["new moon", "first quarter", "last quarter"], "Its whole lit side faces us."),
      ("What is a 'waxing' Moon?", "the lit part we see is growing night by night", ["the lit part is shrinking", "the Moon is hidden", "the Moon is red"], "Waning means shrinking.")]


def UNITS7b():
    b = {k: once_maker(v) for k, v in [("heat", HEATQ), ("time", TIMEQ), ("an", ANQ), ("pl", PLQ), ("light", LQ), ("ems", EQ)]}
    mode = odd_one(MODE, "Which of these is an example of heat transfer by %s?", "Which of these is not an example of heat transfer by %s?")
    hc = odd_one(HC, "Which of these is %s?", "Which of these is not %s?")
    clocks = pairs(CLOCKS, "How does %s work?", "Which time-keeping device works by %s?")
    uni = odd_one(UNI, "Which of these is an example of %s?", "Which of these is not an example of %s?")
    dig = pairs(DIG, "What is the job of %s in digestion?", "Which part of the digestive system is responsible for %s?")
    teeth = pairs(TEETH, "What are %s used for?", "Which teeth are used for %s?")
    breath = pairs(BREATH, "Which organ does %s breathe with?")
    juice = pairs(JUICE, "Which kind of food does %s act on?", "Which digestive juice acts on %s?")
    air = odd_one(AIR, "Which of these is %s?", "Which of these is not %s?")
    nmode = odd_one(NUTMODE, "Which of these is %s?", "Which of these is not %s?")
    ppart = pairs(PPART, "What is the role of %s in a plant?", "Which part of a plant is responsible for %s?")
    photo = odd_one(PHOTO, "Which of these is %s?", "Which of these is not %s?")
    lum = odd_one(LUM, "Which of these is %s?", "Which of these is not %s?")
    ems = pairs(EMS, "What is %s?", "What do we call %s?")
    ecl = odd_one(ECL, "Which of these is %s?", "Which of these is not %s?")
    dayq = odd_one(DAYQ, "Which of these is %s?", "Which of these is not %s?")
    return [
        U(7, "heat-transfer-in-nature", 7, PH,
          "Transfer of heat by conduction, convection and radiation; good and poor conductors of heat; sea breeze and land breeze; clothes for summer and winter; the water cycle, infiltration and groundwater (summary of NCERT Curiosity Chapter 7).",
          "Heat Transfer in Nature", "heat transfer in nature",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 7: conduction, convection and radiation, conductors and insulators of heat, sea and land breezes, choosing clothes, and the water cycle and groundwater. 100 questions with answers.",
          "Heat moves by conduction, convection and radiation.", "Sea breeze by day, land breeze by night.",
          "<p>Heat always flows from a hotter object to a colder one. In solids it moves by conduction: metals are good conductors, while wood, plastic, wool and air are poor conductors (insulators). In liquids and gases, heated parts rise and cooler parts sink, carrying heat by convection. Heat from the Sun reaches us by radiation, which needs no material.</p>"
          "<p>By day the land heats faster than the sea, so a cool sea breeze blows towards the land; at night the land cools faster and a land breeze blows out to sea. Dark surfaces absorb more radiation, so we wear light colours in summer. The Sun's heat also drives the water cycle, and rainwater seeps into the ground to refill groundwater.</p>",
          [("A spoon in hot tea gets hot. How?", ["heat moves along the solid"], "conduction"), ("Noon at the beach: which breeze?", ["land is hotter by day"], "a sea breeze")],
          ["Mixing up sea breeze and land breeze.", "Thinking dark clothes keep us cool.", "Thinking radiation needs air."],
          [("Why do woollen clothes keep us warm?", "Wool traps air, a poor conductor, so less body heat escapes."),
           ("How does the Sun's heat reach the Earth?", "By radiation, which can travel through empty space.")],
          lambda: [("Conduction", [(mode, 8), (hc, 12)]), ("Convection and breezes", [(mode, 8), (c_breeze, 6), (b["heat"], 6)]), ("Radiation", [(mode, 10), (b["heat"], 10)]),
                   ("Conductors and insulators in daily life", [(hc, 14), (b["heat"], 4), (c_breeze, 2)]), ("Mixed problems", [(mode, 10), (hc, 8), (c_breeze, 2)])]),
        U(8, "measurement-of-time-and-motion", 8, PH,
          "Measuring time: sundials, water clocks, sand clocks, pendulum and quartz clocks; the simple pendulum and its time period; the SI unit of time; speed, units of speed and average speed; uniform and non-uniform motion; distance–time graphs (summary of NCERT Curiosity Chapter 8).",
          "Measurement of Time and Motion", "measurement of time and motion",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 8: ancient and modern clocks, the simple pendulum and its time period, speed = distance ÷ time, km/h and m/s, and uniform and non-uniform motion. 100 questions with answers.",
          "Speed = distance ÷ time.", "Time period = total time ÷ number of oscillations.",
          "<p>People measured time with sundials, water clocks (ghatika) and hourglasses; today we use pendulum, quartz and atomic clocks. The SI unit of time is the second. One oscillation of a pendulum is a full swing to one side and back; the time for one oscillation is its time period, which depends on the length of the string, not on the mass of the bob.</p>"
          "<p>Speed is the distance travelled per unit time: speed = distance ÷ time, in m/s or km/h (1 m/s = 3.6 km/h). Motion with a constant speed in a straight line is uniform; motion with changing speed is non-uniform. On a distance–time graph, a steeper line means a higher speed.</p>",
          [("A bus covers 120 km in 2 h. Speed?", ["120 ÷ 2"], "60 km/h"), ("20 oscillations in 30 s. Time period?", ["30 ÷ 20"], "1.5 s")],
          ["Multiplying distance and time to get speed.", "Timing just one swing of a pendulum.", "Thinking a heavier bob swings faster."],
          [("What is the time period of a pendulum?", "The time taken for one complete oscillation; it depends on the length of the pendulum."),
           ("What is the difference between uniform and non-uniform motion?", "In uniform motion an object covers equal distances in equal times; in non-uniform motion its speed changes.")],
          lambda: [("Measuring time", [(clocks, 10), (c_time, 6), (b["time"], 4)]), ("The simple pendulum", [(c_pend, 12), (b["time"], 8)]), ("Speed", [(K(c_speed, "s"), 8), (c_speed2, 8), (c_kmh, 4)]),
                   ("Uniform and non-uniform motion", [(uni, 14), (b["time"], 4), (c_time, 2)]), ("Mixed problems", [(K(c_speed, "d"), 6), (K(c_speed, "t"), 6), (c_pend, 4), (c_kmh, 4)])]),
        U(9, "life-processes-in-animals", 9, LW,
          "Nutrition in animals: the human digestive system, teeth, digestion, absorption, assimilation and egestion; feeding in Amoeba and in ruminants; breathing and respiration, inhaled and exhaled air, breathing organs in different animals (summary of NCERT Curiosity Chapter 9).",
          "Life Processes in Animals", "life processes in animals",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 9: the digestive system, teeth, saliva, bile and villi, Amoeba and ruminants, breathing in and out, exhaled air and breathing organs of animals. 100 questions with answers.",
          "Digestion breaks food into simple substances.", "Respiration releases energy from food.",
          "<p>Food passes from the mouth through the oesophagus, stomach and small intestine to the large intestine. Saliva starts digesting starch; the stomach's acid and juices act on proteins; bile from the liver breaks fats into droplets; pancreatic juice completes digestion. Villi in the small intestine absorb digested food; the large intestine absorbs water, and waste leaves through the anus.</p>"
          "<p>When we breathe in, the diaphragm moves down and air fills the lungs; exhaled air has more carbon dioxide and turns lime water milky. Cells break down food to release energy (respiration). Fish breathe with gills, earthworms through their skin and insects through spiracles and air tubes.</p>",
          [("Where are nutrients absorbed?", ["villi of the small intestine"], "the small intestine"), ("How does an earthworm breathe?", ["no lungs"], "through its moist skin")],
          ["Thinking digestion starts in the stomach.", "Thinking exhaled air is pure carbon dioxide.", "Saying bile digests proteins."],
          [("What is the role of villi?", "They are finger-like folds of the small intestine that give a large surface to absorb digested food into the blood."),
           ("How is exhaled air different from inhaled air?", "It has less oxygen and more carbon dioxide and water vapour.")],
          lambda: [("The digestive system", [(dig, 12), (b["an"], 8)]), ("Teeth and digestion", [(teeth, 6), (juice, 8), (b["an"], 6)]), ("Feeding in other animals", [(b["an"], 8), (breath, 4), (dig, 6), (air, 2)]),
                   ("Breathing and respiration", [(air, 10), (breath, 4), (c_breaths, 6)]), ("Mixed problems", [(c_breaths, 10), (air, 6), (b["an"], 4)])]),
        U(10, "life-processes-in-plants", 10, LW,
          "Photosynthesis: raw materials, chlorophyll, sunlight, stomata and the products; testing leaves for starch; modes of nutrition in plants: autotrophic, parasitic, saprotrophic, insectivorous and symbiotic; transport of water and food; transpiration; respiration in plants (summary of NCERT Curiosity Chapter 10).",
          "Life Processes in Plants", "life processes in plants",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 10: photosynthesis, chlorophyll and stomata, the starch test for leaves, parasites, saprotrophs and insect-eating plants, xylem and phloem, transpiration and respiration in plants. 100 questions with answers.",
          "Green plants make food by photosynthesis.", "Carbon dioxide + water → glucose + oxygen, with sunlight and chlorophyll.",
          "<p>Green plants are autotrophs. In their leaves, chlorophyll traps sunlight, and carbon dioxide (taken in through stomata) and water make glucose, giving out oxygen. The glucose is stored as starch, which turns blue-black with iodine after the leaf is boiled in alcohol to remove chlorophyll.</p>"
          "<p>Some plants get food in other ways: Cuscuta is a parasite, mushrooms are saprotrophs and the pitcher plant traps insects. Xylem carries water up from the roots and phloem carries food from the leaves. Water evaporates from leaves (transpiration), which pulls water up and cools the plant. Plants respire all the time.</p>",
          [("Which parts of a variegated leaf make starch?", ["chlorophyll is needed"], "only the green parts"), ("Which tissue carries water?", ["from roots to leaves"], "xylem")],
          ["Thinking plants do not respire.", "Saying phloem carries water.", "Forgetting to remove chlorophyll before the iodine test."],
          [("What are the raw materials and products of photosynthesis?", "Carbon dioxide and water are used, with sunlight and chlorophyll; glucose (stored as starch) and oxygen are made."),
           ("What is transpiration?", "The loss of water vapour from the leaves, mainly through stomata; it pulls water up the plant and cools it.")],
          lambda: [("Photosynthesis", [(b["pl"], 10), (photo, 6), (ppart, 4)]), ("Testing leaves for starch", [(b["pl"], 8), (photo, 4), (nmode, 8)]), ("Other modes of nutrition", [(nmode, 16), (b["pl"], 4)]),
                   ("Transport and transpiration", [(ppart, 6), (b["pl"], 4), (nmode, 10)]), ("Mixed problems", [(nmode, 12), (ppart, 4), (photo, 2), (b["pl"], 2)])]),
        U(11, "light-shadows-and-reflections", 11, PH,
          "Luminous and non-luminous objects; light travels in straight lines; transparent, translucent and opaque materials; shadows; the pinhole camera; reflection from plane mirrors, the laws of reflection and lateral inversion; periscope and kaleidoscope; curved mirrors in daily life (summary of NCERT Curiosity Chapter 11).",
          "Light: Shadows and Reflections", "shadows and reflections",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 11: luminous objects, shadows, the pinhole camera, reflection from a plane mirror, angles of incidence and reflection, lateral inversion and the periscope. 100 questions with answers.",
          "Light travels in straight lines.", "Angle of incidence = angle of reflection.",
          "<p>Luminous objects such as the Sun and a candle flame give their own light; we see other objects because they reflect light into our eyes. Light travels in straight lines, so an opaque object blocks it and casts a dark shadow. A pinhole camera forms an upside-down image.</p>"
          "<p>A plane mirror reflects light so that the angle of incidence equals the angle of reflection (both measured from the normal). Its image is upright, the same size, as far behind the mirror as the object is in front, and laterally inverted. Two mirrors at 45° make a periscope; the back of a spoon acts as a convex mirror.</p>",
          [("Light hits a mirror at 35° to the normal. Angle of reflection?", ["equal to the angle of incidence"], "35°"), ("Stand 2 m from a mirror. Distance to your image?", ["image is 2 m behind"], "4 m")],
          ["Measuring angles from the mirror instead of the normal.", "Thinking a coloured object has a coloured shadow.", "Saying the image in a pinhole camera is upright."],
          [("What is lateral inversion?", "In a mirror, the left and right sides of the image are swapped, so writing looks reversed."),
           ("Why does a pinhole camera give an upside-down image?", "Light travels in straight lines, so rays from the top of the object pass through the hole to the bottom of the screen, and the other way round.")],
          lambda: [("Light and shadows", [(lum, 12), (b["light"], 8)]), ("The pinhole camera", [(b["light"], 6), (lum, 8), (K(c_mirror, "letter"), 6)]), ("Reflection from a plane mirror", [(K(c_mirror, "angle"), 10), (b["light"], 6), (K(c_mirror, "dist"), 4)]),
                   ("Images in a plane mirror", [(K(c_mirror, "dist"), 6), (K(c_mirror, "between"), 5), (K(c_mirror, "letter"), 5), (K(c_mirror, "angle"), 4)]), ("Mixed problems", [(K(c_mirror, "angle"), 6), (K(c_mirror, "letter"), 6), (lum, 4), (K(c_mirror, "dist"), 4)])]),
        U(12, "earth-moon-and-the-sun", 12, ES,
          "Rotation and revolution of the Earth; day and night; the tilt of the Earth's axis and the seasons; phases of the Moon; solar and lunar eclipses (summary of NCERT Curiosity Chapter 12).",
          "Earth, Moon and the Sun", "Earth, Moon and the Sun",
          "Free CBSE Class 7 Science worksheets for NCERT Curiosity Chapter 12: rotation and revolution, day and night, the tilted axis and seasons, the phases of the Moon, and solar and lunar eclipses. 100 questions with answers.",
          "Rotation gives day and night; tilt and revolution give seasons.", "Solar eclipse: Moon between. Lunar eclipse: Earth between.",
          "<p>The Earth rotates on its axis from west to east once in about 24 hours, giving day and night, and revolves round the Sun once in about 365¼ days. Its axis is tilted by about 23.5°, so each hemisphere gets more direct sunlight and longer days for part of the year: these are the seasons.</p>"
          "<p>The Moon goes round the Earth, and we see different amounts of its sunlit half: the phases, from new moon to full moon and back in about 29.5 days. When the Moon comes between the Sun and the Earth, there is a solar eclipse (on a new moon day); when the Earth comes between the Sun and the Moon, there is a lunar eclipse (on a full moon night).</p>",
          [("Which phase comes after the first quarter?", ["the lit part keeps growing"], "waxing gibbous"), ("June in India: season in Australia?", ["opposite hemisphere"], "winter")],
          ["Thinking seasons come from changing distance to the Sun.", "Mixing up solar and lunar eclipses.", "Thinking the Earth's shadow causes the phases."],
          [("Why do we have seasons?", "Because the Earth's axis is tilted, so as it revolves, each hemisphere is tilted towards the Sun for part of the year."),
           ("When can a solar eclipse happen?", "Only on a new moon day, when the Moon is between the Sun and the Earth.")],
          lambda: [("Rotation and revolution", [(ems, 8), (b["ems"], 8), (dayq, 4)]), ("Day, night and seasons", [(b["ems"], 8), (dayq, 6), (c_hemi, 6)]), ("Phases of the Moon", [(c_phase, 12), (ems, 4), (b["ems"], 4)]),
                   ("Eclipses", [(ecl, 14), (b["ems"], 4), (ems, 2)]), ("Mixed problems", [(c_hemi, 6), (dayq, 6), (ecl, 4), (ems, 2), (b["ems"], 2)])]),
    ]
