# -*- coding: utf-8 -*-
"""Class 6 Science (NCERT Curiosity, chapters 7–12): question makers and UNITS6b()."""
from uk_alsci import tq, nf, once_maker
from in_sci import pairs, _R, U, K
from in_sci6a import NS, LW, MT, PH, ES, odd_one, nq
import in_sci

# =================================================================== Chapter 7: temperature and its measurement
THER = [("a clinical thermometer", "measuring the temperature of the human body"), ("a laboratory thermometer", "measuring the temperature of water and other substances in experiments"),
        ("a digital thermometer", "showing the temperature as numbers on a screen, without mercury"), ("a maximum–minimum thermometer", "recording the highest and lowest temperatures of the day"),
        ("an infrared (non-contact) thermometer", "measuring body temperature without touching the skin")]
TEMP = [("What does temperature tell us?", "how hot or cold something is", ["how heavy something is", "how long something is", "how fast something moves"], "We measure it with a thermometer."),
        ("Why can we not always trust touch to judge temperature?", "the same water can feel warm or cold depending on what our hand touched before", ["touch is always exact", "our skin cannot feel heat", "touch only measures length"], "Try it with hot, cold and normal water."),
        ("What is the normal temperature of the human body?", "about 37 °C", ["about 100 °C", "about 0 °C", "about 25 °C"], "It can differ slightly from person to person."),
        ("What is the range of a clinical thermometer?", "35 °C to 42 °C", ["−10 °C to 110 °C", "0 °C to 100 °C", "20 °C to 60 °C"], "Body temperature stays within this range."),
        ("What is the range of a usual laboratory thermometer?", "−10 °C to 110 °C", ["35 °C to 42 °C", "0 °C to 37 °C", "50 °C to 500 °C"], "It can measure boiling water."),
        ("Why should a clinical thermometer not be used to measure the temperature of boiling water?", "its range goes only up to 42 °C and it may break", ["it measures only cold things", "it shows the time", "it has no scale"], "Use a laboratory thermometer."),
        ("Why does a clinical thermometer have a kink near the bulb?", "it stops the mercury from falling back so the reading can be read later", ["it makes the thermometer pretty", "it measures length", "it stops the glass from breaking"], "A laboratory thermometer has no kink."),
        ("What should you do before using a clinical thermometer with a liquid column?", "wash it and give it a few jerks so the level falls below 35 °C", ["heat it in a flame", "keep it in ice for an hour", "dip it in boiling water"], "Hold it by the end, not the bulb."),
        ("How should a laboratory thermometer be held when measuring water?", "upright, with the bulb in the water but not touching the bottom or sides", ["lying flat on the table", "with the bulb out of the water", "with the bulb touching the bottom"], "Read it while the bulb is still in the water."),
        ("Why are digital thermometers now preferred to mercury thermometers?", "mercury is poisonous and hard to dispose of if the thermometer breaks", ["digital ones are always cheaper", "mercury is too light", "mercury freezes at room temperature"], "Digital thermometers are safer."),
        ("What is the SI unit of temperature?", "the kelvin (K)", ["the degree Celsius only", "the metre", "the joule"], "We commonly use degrees Celsius (°C)."),
        ("What is the boiling point of pure water at sea level?", "100 °C", ["37 °C", "0 °C", "212 °C"], "Ice melts at 0 °C."),
        ("At what temperature does pure ice melt?", "0 °C", ["100 °C", "37 °C", "−10 °C"], "Water freezes at the same temperature."),
        ("Where should the clinical thermometer be kept to measure body temperature?", "under the tongue or in the armpit for about a minute", ["in the hand only", "on the forehead for a second", "in a cup of tea"], "Then read it at eye level."),
        ("How many divisions show one degree on a thermometer if each small division is 0.1 °C?", "10 divisions", ["1 division", "5 divisions", "100 divisions"], "Count the small marks between two numbers."),
        ("What does a weather report's 'maximum temperature' mean?", "the highest temperature during the day", ["the temperature at midnight", "the lowest temperature", "the body temperature"], "The minimum temperature is usually just before sunrise."),
        ("Why is the reading of a laboratory thermometer taken while it is still in the water?", "the level starts changing as soon as it is taken out", ["it shows nothing in the water", "it measures air only", "it is safer to drop it"], "It has no kink to hold the level."),
        ("A child's temperature is 39 °C. What does this show?", "the child has a fever", ["the child is very cold", "the temperature is normal", "the thermometer is broken"], "Normal is about 37 °C."),
        ("Which liquid other than mercury is often used in laboratory thermometers?", "coloured alcohol", ["water", "milk", "oil paint"], "It is safer than mercury."),
        ("Why should a thermometer not be held by its bulb?", "the heat of your hand changes the reading", ["the bulb is sharp", "the bulb is cold", "it makes the scale disappear"], "Hold it by the other end."),
        ("Why does the liquid in a thermometer rise when it is warmed?", "the liquid expands when heated", ["the liquid becomes heavier", "the glass shrinks", "air pushes it up"], "It contracts when cooled."),
        ("What is the temperature of a mixture of ice and water?", "0 °C", ["37 °C", "100 °C", "−10 °C"], "It stays at 0 °C while the ice melts."),
        ("Why is the bulb of a laboratory thermometer kept away from the bottom of a beaker being heated?", "the bottom may be hotter than the water", ["the bulb may freeze", "the scale may change", "it makes the water boil"], "We want the temperature of the water."),
        ("How should the reading of a thermometer be taken?", "with the eye level with the top of the liquid column", ["from above at an angle", "from below at an angle", "with eyes closed"], "This avoids errors."),
        ("Which instrument shows the temperature of a refrigerator or a room?", "a room (wall) thermometer", ["a clinical thermometer", "a rain gauge", "a compass"], "Its range is wider than a clinical thermometer's."),
        ("A cup of tea feels hot and a glass of cold drink feels cold. What is being compared?", "their temperatures", ["their masses", "their lengths", "their colours"], "Temperature tells how hot or cold."),
        ("Who gave his name to the Celsius scale?", "Anders Celsius", ["Isaac Newton", "C. V. Raman", "Galileo Galilei"], "On this scale water freezes at 0 and boils at 100."),
        ("What does 'normal temperature' of a healthy person depend on a little?", "the person, the time of day and how active they are", ["only the colour of the skin", "only their height", "nothing at all"], "Values close to 37 °C are normal."),
        ("Why should a clinical thermometer be washed with an antiseptic solution before use?", "to kill germs from the last user", ["to make the reading higher", "to cool the mercury", "to clean the scale markings"], "It may be used by many people."),
        ("What is one advantage of a digital thermometer?", "it is easy to read and does not contain mercury", ["it never needs batteries", "it measures length", "it shows the time of day"], "It beeps when the reading is ready.")]


def c_kelvin(k=None):
    R = _R[0]
    c = R.choice([0, 10, 15, 20, 25, 27, 30, 35, 37, 40, 50, 60, 80, 100, -10, -20, -40])
    if k == "back" or (k is None and R.random() < 0.4):
        K_ = c + 273.15
        return nq("Convert %.2f K into degrees Celsius." % K_, c, [K_ + 273.15, c + 273, -c, c + 100, c - 1], "°C",
                  "°C = K − 273.15 = %.2f − 273.15 = %d °C." % (K_, c), sf=5)
    v = c + 273.15
    return nq("Convert %d °C into kelvin." % c, v, [c - 273.15, c + 100, c + 273.15 + 100, 273.15 - c, c], "K", "K = °C + 273.15 = %d + 273.15 = %.2f K." % (c, v), sf=5)


def c_tdiff(k=None):
    R = _R[0]
    city = R.choice(in_sci.PLACES)
    lo = R.choice([8, 12, 14, 16, 18, 21, 23, 25, 26, 27])
    hi = lo + R.choice([5, 6, 7, 8, 9, 11, 12, 13])
    if R.random() < 0.5:
        return nq("In %s, the minimum temperature one day was %d °C and the maximum was %d °C. What was the difference?" % (city, lo, hi), hi - lo, [hi + lo, hi, lo, hi - lo + 10], "°C",
                  "Difference = %d − %d = %d °C." % (hi, lo, hi - lo))
    d = hi - lo
    return nq("The morning temperature in %s was %d °C. It rose by %d °C by afternoon. What was the afternoon temperature?" % (city, lo, d), hi, [lo - d, d, hi + d, lo], "°C",
              "%d + %d = %d °C." % (lo, d, hi))


PLACE_T = [("the body of a person with a fever", 39), ("the water in a bath bucket", 40), ("boiling water", 100), ("ice from a freezer", -5), ("melting ice", 0),
           ("tea in a cup", 70), ("water from a tap on a cool day", 22), ("the air in a classroom", 30), ("the flame of a candle", 1000), ("a healthy child's mouth", 37),
           ("warm water for a foot bath", 41), ("hot cooking oil", 180), ("water in a pond in winter", 12), ("milk just taken from the fridge", 5),
           ("a person who is very cold after swimming in icy water", 35), ("soup being served", 65), ("the air on a hot summer afternoon in Rajasthan", 46), ("water in a pressure cooker", 120),
           ("an ice cream", -12), ("the air in Leh on a winter night", -20), ("molten iron", 1500), ("warm milk for a baby", 38), ("a cold drink with ice", 2), ("the hot sand of a desert at noon", 60)]


def c_range(k=None):
    R = _R[0]
    what, t = R.choice(PLACE_T)
    cl, lab = 35 <= t <= 42, -10 <= t <= 110
    a = "either of them" if cl and lab else "a clinical thermometer" if cl else "a laboratory thermometer" if lab else "neither of them"
    return tq("A clinical thermometer reads 35–42 °C and a laboratory thermometer reads −10 to 110 °C. Which could measure %s, which is at about %d °C?" % (what, t), a,
              [x for x in ["either of them", "a clinical thermometer", "a laboratory thermometer", "neither of them"] if x != a],
              "%d °C is %s the clinical range and %s the laboratory range." % (t, "inside" if cl else "outside", "inside" if lab else "outside"))


def c_fever(k=None):
    R = _R[0]
    t = R.choice([35.2, 35.5, 35.8, 36.2, 36.4, 36.6, 36.8, 36.9, 37.0, 37.1, 37.2, 37.4, 37.8, 38.0, 38.2, 38.4, 38.6, 38.9, 39.0, 39.4, 39.8, 40.1, 40.5])
    if t >= 37.6:
        a = "a fever"
    elif t >= 36.1:
        a = "a normal temperature"
    else:
        a = "a temperature lower than normal"
    return tq("A clinical thermometer shows that a child's temperature is %.1f °C. What does this show?" % t, a,
              [x for x in ["a fever", "a normal temperature", "a temperature lower than normal", "that the thermometer must be a laboratory thermometer"] if x != a],
              "Normal body temperature is about 37 °C (roughly 36.1–37.5 °C).")


# =================================================================== Chapter 8: a journey through states of water
STATE = [("melting", "a solid changing into a liquid, such as ice into water"), ("freezing", "a liquid changing into a solid, such as water into ice"),
         ("evaporation", "a liquid slowly changing into vapour from its surface at any temperature"), ("condensation", "water vapour cooling and changing into liquid water"),
         ("boiling", "a liquid changing into vapour quickly throughout, at a fixed temperature"), ("the water cycle", "the continuous movement of water between the Earth's surface and the air")]
STEX = {"melting": ["ice cream softening on a hot day", "a block of ice turning into water", "butter turning runny in a hot pan", "snow on mountains turning into streams in summer"],
        "evaporation": ["wet clothes drying on a line", "a puddle disappearing after the rain", "salt being left behind when sea water dries in salt pans", "sweat drying on the skin"],
        "condensation": ["drops forming on the outside of a cold glass of water", "dew on grass in the morning", "a mirror misting up in the bathroom", "clouds forming high in the sky"],
        "freezing": ["water turning into ice in a freezer", "a pond's surface turning into ice in winter", "kulfi setting in the freezer"]}
EVAP = [("Which change increases the rate of evaporation?", "a higher temperature", ["more humidity in the air", "less wind", "a smaller surface area"], "Clothes dry faster on a hot day."),
        ("Why do clothes dry faster on a windy day?", "the wind carries away the water vapour", ["wind adds water to clothes", "wind cools the clothes down", "wind makes the air humid"], "Wind increases evaporation."),
        ("Why does water in a wide plate dry faster than in a narrow glass?", "it has a larger surface area", ["it is hotter", "it is heavier", "it has less water vapour"], "Evaporation happens at the surface."),
        ("Why do wet clothes dry slowly on a rainy day?", "the air is already full of water vapour (high humidity)", ["the temperature is too high", "the wind is too strong", "the clothes are too dry"], "Humid air takes in less vapour."),
        ("Why does water in an earthen pot (matka) stay cool?", "water seeps through tiny pores and evaporates, taking heat from the pot", ["clay is a refrigerator", "the pot is painted", "clay makes water cold by magic"], "Evaporation causes cooling."),
        ("Why do we feel cool after sweating?", "the sweat evaporates and takes heat from our body", ["sweat is cold water", "sweat stops blood flow", "the skin becomes thicker"], "Evaporation causes cooling."),
        ("Why do drops of water form on the outside of a glass of cold water?", "water vapour in the air condenses on the cold surface", ["water leaks through the glass", "the glass melts", "the ice evaporates"], "This shows that air contains water vapour."),
        ("Where does the water in clouds come from?", "water vapour that rose from oceans, lakes and plants and condensed", ["the Sun", "only from rivers", "the Moon"], "Clouds are made of tiny drops."),
        ("What brings water back to the land in the water cycle?", "rain, snow and hail (precipitation)", ["evaporation", "condensation only", "wind alone"], "Rivers then carry it to the sea."),
        ("How do plants add water vapour to the air?", "through tiny pores in their leaves (transpiration)", ["through their roots only", "by making clouds", "by burning"], "This is part of the water cycle."),
        ("Why is water present on Earth in all three states?", "the temperature varies from place to place", ["water is always solid", "the Sun is far away", "water does not change state"], "Ice on poles, liquid in seas and vapour in the air."),
        ("What happens to the particles of water when ice melts?", "they gain energy and move more freely", ["they stop moving", "they turn into salt", "they become heavier"], "In vapour they move fastest."),
        ("Which state of water has a fixed shape?", "solid (ice)", ["liquid water", "water vapour", "steam"], "A liquid takes the shape of its container."),
        ("What is the main difference between evaporation and boiling?", "evaporation happens at any temperature from the surface; boiling happens at a fixed temperature throughout", ["they are the same", "boiling happens at any temperature", "evaporation needs 100 °C"], "Water boils at 100 °C at sea level."),
        ("How is common salt obtained from sea water?", "sea water is left in shallow pans and the water evaporates", ["sea water is frozen", "sea water is filtered", "salt grows on trees"], "This is done in Gujarat and Tamil Nadu."),
        ("Why does the level of water in an open bowl go down over a few days?", "water evaporates into the air", ["water sinks into the bowl", "water turns into ice", "water becomes salt"], "Covering the bowl slows this."),
        ("Why are puddles gone after a few hours of sunshine?", "the heat of the Sun evaporates the water", ["the water freezes", "the water becomes air permanently without vapour", "the ground pushes it up"], "The vapour becomes part of the air."),
        ("Why do roads look wet in the morning after a cold night?", "water vapour condensed as dew", ["it rained heavily", "the roads melted", "the water rose from underground"], "Dew forms on cool surfaces."),
        ("What is water vapour?", "water in the gas state, which we cannot see", ["the white mist from a kettle", "tiny ice crystals", "clouds"], "The white mist is tiny drops of liquid water."),
        ("Why do we need to save water even though the water cycle goes on?", "clean fresh water that we can use is limited", ["the water cycle has stopped", "sea water is enough to drink", "rain never falls"], "Most of Earth's water is salty."),
        ("Why does a bottle of cold water taken out of the fridge get wet outside?", "water vapour in the air condenses on it", ["the bottle leaks", "the plastic sweats", "the cold water evaporates"], "The water comes from the air."),
        ("What happens to the temperature of water while it is boiling?", "it stays at 100 °C until all the water changes to steam", ["it keeps rising", "it falls to 0 °C", "it changes all the time"], "The heat is used to change the state."),
        ("Where on Earth is most water found frozen as ice?", "in the polar ice caps and glaciers", ["in rivers", "in clouds", "in wells"], "Glaciers feed rivers like the Ganga."),
        ("What is hail?", "small balls of ice falling from clouds", ["water vapour", "dew", "fog"], "It is a kind of precipitation."),
        ("Which change of state happens when a cloud forms?", "condensation of water vapour into tiny drops", ["melting of ice", "freezing of rain", "boiling of sea water"], "Air cools as it rises."),
        ("Why are drops seen on the inside of a lid covering a pan of hot water?", "steam condenses on the cooler lid", ["the lid leaks", "the lid melts", "the water freezes"], "Water vapour turns back to water."),
        ("What happens when ice is heated?", "it melts into water", ["it turns straight into salt", "it gets harder", "it becomes sand"], "Further heating changes water into vapour."),
        ("Why is a wet floor dried faster with a fan?", "moving air speeds up evaporation", ["the fan cools the floor", "the fan adds water", "the fan makes the air humid"], "Wind carries vapour away."),
        ("Which state of water has neither a fixed shape nor a fixed volume?", "water vapour", ["ice", "liquid water", "snow"], "A gas fills its container."),
        ("Which state of water has a fixed volume but no fixed shape?", "liquid water", ["ice", "water vapour", "steam"], "A liquid takes the shape of its container.")]

FAST = [("a wet cloth spread out", "the same cloth folded", "a larger surface area"), ("water in a wide plate", "the same amount of water in a narrow glass", "a larger surface area"),
        ("clothes in the sun", "clothes in the shade", "a higher temperature"), ("clothes on a windy day", "clothes on a still day", "more wind"),
        ("clothes on a dry, sunny day", "clothes on a humid, rainy day", "less humidity in the air"), ("a puddle in the open", "a puddle under a tree", "more sunlight and wind"),
        ("a floor wiped and fanned", "a floor wiped with no fan", "more wind"), ("hair dried with warm air", "hair left to dry in a cool room", "a higher temperature"),
        ("spilt water spread thin on a table", "the same water in a small heap", "a larger surface area"), ("salt pans in the hot summer", "salt pans in the rainy season", "a higher temperature and less humidity")]


def c_fast(k=None):
    R = _R[0]
    a, b_, why = R.choice(FAST)
    x, y = (a, b_) if R.random() < 0.5 else (b_, a)
    return tq("Which dries (evaporates) faster: %s or %s?" % (x, y), a, [b_, "both at the same rate", "neither ever dries"], "The answer is %s, because of %s." % (a, why))


def c_wstate(k=None):
    R = _R[0]
    t = R.choice([-30, -25, -20, -18, -15, -10, -8, -5, -3, -2, -1, 1, 4, 10, 18, 25, 37, 45, 50, 60, 70, 80, 90, 95, 99, 101, 105, 110, 120, 130, 150, 200])
    a = "solid (ice)" if t < 0 else "liquid (water)" if t < 100 else "gas (steam)"
    return tq("At sea level, what is the state of pure water at %d °C?" % t, a, [x for x in ["solid (ice)", "liquid (water)", "gas (steam)", "a mixture of all three"] if x != a],
              "Water is ice below 0 °C, liquid between 0 °C and 100 °C and steam above 100 °C.")


# =================================================================== Chapter 9: methods of separation in everyday life
SEP = [("handpicking", "removing small stones from rice or dal by hand"), ("threshing", "beating harvested wheat stalks to separate the grain"),
       ("winnowing", "letting the wind blow away light husk from heavier grain"), ("sieving", "separating flour from bran using a sieve"),
       ("sedimentation", "letting heavier particles such as sand settle at the bottom of water"), ("decantation", "pouring off the clear water from above the settled sand"),
       ("filtration", "passing muddy water through filter paper or a cloth to remove solid particles"), ("evaporation", "heating salt water until the water goes, leaving the salt"),
       ("churning", "separating butter from curd by stirring it fast"), ("magnetic separation", "removing iron pins from sand using a magnet"),
       ("loading", "adding alum to muddy water so the mud settles faster"), ("condensation", "cooling steam to get back pure liquid water")]
MIX = [("stones mixed with rice", "handpicking"), ("husk and grain", "winnowing"), ("flour and bran", "sieving"), ("tea leaves and tea", "filtration"),
       ("salt dissolved in water", "evaporation"), ("iron filings and sand", "magnetic separation"), ("butter and buttermilk", "churning"),
       ("pebbles and sand at a building site", "sieving"), ("grain and stalks of wheat", "threshing"),
       ("oil floating on water", "decantation"), ("chalk powder in water", "filtration"), ("fine mud in river water that will not settle", "loading with alum"),
       ("curd and whey in making paneer", "filtration"), ("rotten tomatoes in a basket of good ones", "handpicking"),
       ("insects mixed with dal", "handpicking"), ("chaff and rice grains on a windy day", "winnowing"), ("small stones from wheat flour", "sieving"),
       ("sugar dissolved in water", "evaporation"), ("sawdust in water", "filtration"), ("iron nails mixed with wooden shavings", "magnetic separation"),
       ("cream from milk", "churning"), ("coarse gravel and fine sand", "sieving"),
       ("rice grains and rice stalks at harvest", "threshing"), ("salt from sea water in salt pans", "evaporation"), ("steel pins mixed with plastic beads", "magnetic separation"),
       ("green chillies mixed with peas", "handpicking"), ("fine clay in a pot of drinking water", "loading with alum"), ("water above settled rice before cooking", "decantation")]
SBASIS = [("handpicking", "the parts differ in size, colour or shape and are few"), ("winnowing", "one part is light and is blown away by the wind"),
          ("sieving", "the particles are of different sizes"), ("magnetic separation", "one part is attracted by a magnet"),
          ("filtration", "an insoluble solid is mixed with a liquid"), ("evaporation", "a solid is dissolved in a liquid"),
          ("sedimentation", "a heavy insoluble solid settles in a liquid"), ("churning", "lighter fat separates when the liquid is stirred fast"),
          ("threshing", "grains are firmly attached to stalks and must be beaten off"), ("decantation", "a clear liquid lies above a settled solid or another liquid")]
SEQ = [("How can you separate a mixture of sand, salt and iron filings?", "use a magnet, then dissolve the rest in water and filter, then evaporate the filtrate", ["filter it dry", "winnow it", "heat it until all of it melts"], "The magnet removes iron; filtering removes sand; evaporation gives salt."),
       ("How can you get clean sand and salt from a mixture of the two?", "dissolve in water, filter to get sand, then evaporate the solution to get salt", ["use a magnet", "sieve it", "winnow it"], "Salt dissolves; sand does not."),
       ("How can you get clear water from muddy water at home?", "let the mud settle, decant the water, then filter it", ["evaporate it", "use a magnet", "winnow it"], "Boil it too before drinking."),
       ("How is wheat made ready for the market after harvest?", "threshing, then winnowing, then handpicking any stones", ["churning, then sieving", "filtration, then evaporation", "magnetic separation"], "Each step removes a different part."),
       ("How can you separate chalk powder and sugar?", "add water, filter out the chalk, then evaporate the water to get sugar", ["use a magnet", "winnow them", "handpick them"], "Sugar dissolves; chalk does not."),
       ("How is butter got from milk at home?", "make curd from the milk, then churn the curd", ["filter the milk", "evaporate the milk", "use a magnet"], "The butter floats up."),
       ("How can you get pure water from salty water?", "boil it and condense the steam on a cold surface", ["filter it", "sieve it", "let it settle"], "Salt is left behind in the pan."),
       ("How can you separate oil from water?", "let them form two layers and pour off the oil carefully", ["filter them through paper", "use a magnet", "winnow them"], "Oil floats on water."),
       ("Why is tea strained after boiling with tea leaves?", "the tea leaves are insoluble and are removed by filtration", ["the leaves dissolve", "to make it sweet", "to add milk"], "A strainer is a filter."),
       ("How can you separate rice from dal when both are mixed with small stones?", "handpick the stones; rice and dal can also be picked apart or sieved if sizes differ", ["use a magnet", "evaporate them", "churn them"], "Choose by size and colour.")]
SEPQ = [("What is a mixture?", "two or more substances mixed together that can be separated", ["a single pure substance", "only water", "only a solid"], "Sand in water is a mixture."),
        ("Why do we separate substances?", "to remove unwanted or harmful parts, or to get a useful part", ["to make them heavier", "to make them dirty", "because they cannot be mixed again"], "We remove stones from rice."),
        ("Why does winnowing work?", "the wind carries away light husk while the heavy grain falls nearby", ["the grain is lighter than husk", "wind dissolves husk", "husk sticks to the grain"], "Farmers winnow from a height."),
        ("Why does sedimentation work?", "heavier insoluble particles settle down under gravity", ["particles float to the top", "the water evaporates", "a magnet pulls them down"], "Then we can decant the water."),
        ("Which method removes very fine particles from water better than decantation?", "filtration", ["handpicking", "threshing", "winnowing"], "Filter paper has very fine pores."),
        ("Can salt dissolved in water be removed by filtration?", "no; dissolved salt passes through the filter paper", ["yes, always", "only with a magnet", "only by winnowing"], "Use evaporation instead."),
        ("Which two methods are used to get pure water from salt water?", "evaporation and condensation", ["sieving and winnowing", "threshing and handpicking", "churning and loading"], "Heating makes vapour; cooling makes it liquid again."),
        ("Why is alum added to muddy water?", "it makes the fine mud particles stick together and settle faster", ["it gives the water a colour", "it makes water salty", "it removes salt"], "This is called loading."),
        ("Which method is used at a flour mill to remove bran and husk?", "sieving", ["magnetic separation", "evaporation", "churning"], "Bigger pieces stay on the sieve."),
        ("Why is threshing done?", "to separate the grains from the stalks after harvest", ["to grind grain into flour", "to wash the grain", "to plant seeds"], "It can be done by hand, by animals or by machines."),
        ("How does a scrap dealer separate iron from other waste?", "using a big magnet", ["using water", "by winnowing", "by sieving"], "Iron is attracted to magnets."),
        ("A mixture of sand and salt is stirred in water. What is the next step to get the sand?", "filter the mixture; the sand stays on the filter paper", ["evaporate it first", "use a magnet", "winnow it"], "The salt solution passes through; evaporate it to get the salt."),
        ("Why should drinking water from a river be boiled even after filtering?", "filtering does not remove germs", ["boiling makes water salty", "filtering adds germs", "boiling removes all salt"], "Boiling kills most germs."),
        ("Which method is used to separate cream from milk in a dairy?", "churning in a machine", ["winnowing", "handpicking", "magnetic separation"], "Butter is separated from curd by churning too."),
        ("Which household tool is used for filtration in the kitchen?", "a tea strainer", ["a rolling pin", "a knife", "a spoon"], "A sieve is used for sieving flour."),
        ("What is the clear liquid that passes through a filter paper called?", "the filtrate", ["the residue", "the sediment", "the husk"], "The solid left on the paper is the residue."),
        ("What is the solid left behind on a filter paper called?", "the residue", ["the filtrate", "the solution", "the vapour"], "The liquid that passes through is the filtrate."),
        ("Why do farmers winnow grain from a raised platform?", "the falling mixture is spread by the wind so the husk blows farther", ["to dry the grain in the sun only", "to count the grain", "to wash the grain"], "Heavy grain falls in a heap below."),
        ("Why is a sieve not useful to separate salt from water?", "dissolved salt passes through the holes with the water", ["the salt is too big", "the sieve rusts", "water does not pass through a sieve"], "Use evaporation."),
        ("Which separation method is used when making ghee from butter?", "heating and then filtering out the solid residue", ["winnowing", "magnetic separation", "threshing"], "The clear ghee is poured off."),
        ("Why do we wash rice and pour away the water before cooking?", "to remove dust and husk that float or mix with the water", ["to make the rice dissolve", "to add salt", "to make it sticky"], "This uses decantation."),
        ("Which is a mixture we use every day?", "lemonade (water, sugar, lemon juice and salt)", ["pure water", "pure gold", "pure sugar"], "Air is also a mixture."),
        ("What happens if we try to winnow a mixture of sugar and salt?", "it will not separate, as both are similar in weight", ["salt flies away", "sugar dissolves", "both melt"], "Winnowing needs parts of very different weight.")]

# =================================================================== Chapter 10: living creatures
CHAR = [("growth", "an increase in size and mass, as when a seedling becomes a plant"), ("respiration", "taking in oxygen and releasing energy from food"),
        ("nutrition", "taking in food to get energy and materials"), ("excretion", "getting rid of wastes from the body"),
        ("response to stimuli", "reacting to changes around, such as touch, light or heat"), ("reproduction", "producing young ones of the same kind"),
        ("movement", "changing position; plants move their parts, as when a sunflower turns towards the Sun")]
LIV = {"living": ["a mushroom", "a seed that can germinate", "an earthworm", "a moss on a wall", "a tadpole", "a mango tree", "a snail", "yeast", "a lizard", "a grass plant"],
       "non-living": ["a stone", "a toy car", "a cloud", "a candle flame", "a robot", "a running river", "a ballpoint pen", "a bicycle", "the wind", "a plastic doll"]}
CHEX = {"growth": ["a seedling becoming a tall plant", "a puppy becoming a dog", "a baby's height increasing each year", "a tadpole getting bigger"],
        "respiration": ["a fish taking in oxygen from water through its gills", "a person breathing faster after running", "a plant taking in oxygen at night", "an earthworm breathing through its moist skin"],
        "excretion": ["sweating and passing urine", "a plant losing extra water through its leaves", "a fish giving out ammonia into water", "a person breathing out carbon dioxide"],
        "response to stimuli": ["a cat's eyes narrowing in bright light", "a snail pulling into its shell when touched", "the leaves of a touch-me-not folding up", "a dog running when it hears a cracker"],
        "reproduction": ["a hen laying eggs", "a mango tree making seeds", "a cat giving birth to kittens", "a potato sprouting new plants from its eyes"]}
STIM = [("touching the leaves of a touch-me-not (Mimosa) plant", "the leaves fold up"), ("putting a finger on a hot plate", "we pull the hand away quickly"),
        ("bright light falling on our eyes", "we blink or close our eyes"), ("smelling tasty food", "our mouth starts to water"),
        ("a sunflower plant in the morning sun", "the flower turns to face the Sun"), ("a plant kept near a window", "its stem bends towards the light"),
        ("a sudden loud sound near a dog", "the dog runs or barks"), ("touching an earthworm", "it curls up and moves away"),
        ("a cat seeing a mouse", "it runs to catch it"), ("a dark room suddenly lit by a bulb", "we narrow our eyes"),
        ("an insect landing on a Venus flytrap leaf", "the leaf closes around it"), ("the smell of a flower reaching a bee", "the bee flies towards the flower"),
        ("touching a snail's feelers", "it pulls them in"), ("cold winter air", "we shiver and our skin gets goosebumps")]
LIFE = [("the frog", "egg → tadpole → froglet → adult frog"), ("the mosquito", "egg → larva → pupa → adult mosquito"),
        ("the butterfly", "egg → caterpillar (larva) → pupa → adult butterfly"), ("the silk moth", "egg → larva (silkworm) → pupa (cocoon) → adult moth"),
        ("a hen", "egg → chick → adult hen"), ("a bean plant", "seed → seedling → young plant → plant with flowers and seeds")]
GERM = [("What does a seed need to germinate?", "water, air and a suitable temperature", ["only soil", "only sunlight", "salt and sugar"], "Most seeds germinate without light."),
        ("In an experiment, seeds kept dry did not germinate. What does this show?", "seeds need water to germinate", ["seeds need darkness", "seeds need cold", "seeds need soil only"], "Seeds kept moist germinated."),
        ("Seeds kept under boiled, cooled water (with no air) did not germinate. What does this show?", "seeds need air to germinate", ["seeds need salt", "seeds need sunlight", "seeds need cold water"], "Boiling removes dissolved air."),
        ("Moist seeds kept in a refrigerator did not germinate. What does this show?", "seeds need a suitable warm temperature", ["seeds need cold", "seeds need no water", "seeds need darkness"], "Too cold slows life processes."),
        ("Why is a seed called living even though it seems not to grow?", "it can germinate and grow into a new plant when conditions are right", ["it is made of stone", "it moves from place to place", "it can talk"], "It is in a resting state."),
        ("What comes out first when a seed germinates?", "the root", ["the flower", "the fruit", "the seed coat"], "Then the shoot grows upwards."),
        ("Which of these is a sign that a car is not living, even though it moves?", "it cannot grow or reproduce", ["it uses fuel", "it makes noise", "it has wheels"], "Living things show all the life processes."),
        ("Why do we breathe faster after running?", "the body needs more oxygen to release energy", ["the lungs become smaller", "we are cold", "we need less air"], "Respiration releases energy from food."),
        ("Do plants respire?", "yes, all living things respire, day and night", ["no, only animals respire", "only at night", "only in sunlight"], "They take in oxygen and give out carbon dioxide."),
        ("How do plants get rid of excess water?", "through tiny pores on their leaves", ["through their flowers only", "they cannot", "through the fruit"], "This is called transpiration."),
        ("What is a stimulus?", "a change in the surroundings that a living thing responds to", ["a kind of food", "a type of seed", "a waste product"], "Light, heat and touch are stimuli."),
        ("What does a tadpole breathe with?", "gills", ["lungs only", "skin only", "its tail"], "Adult frogs breathe with lungs and skin."),
        ("Which stage of the mosquito lives in water and wriggles about?", "the larva", ["the adult", "the egg", "the pupa that flies"], "That is why stagnant water must be removed."),
        ("Why should we not let water collect in coolers and pots?", "mosquitoes lay eggs in still water", ["it makes the water salty", "frogs drink it", "it evaporates too fast"], "Mosquitoes spread malaria and dengue."),
        ("What is the life span of a living thing?", "the time from its birth to its death", ["its size", "its food", "its colour"], "A mosquito lives for weeks; a tortoise for many years."),
        ("Which characteristic is shown when a chick hatches from an egg and becomes a hen?", "growth", ["excretion only", "response only", "no characteristic"], "Living things grow and develop."),
        ("Which of these shows that a plant responds to gravity?", "its roots always grow downwards", ["its leaves are green", "its flowers smell", "it gives oxygen"], "Shoots grow upwards towards light."),
        ("Why are fresh green peas soaked before sowing?", "soaking softens the seed coat and starts germination", ["to make them sweet", "to kill the seed", "to change their colour"], "Seeds take in water and swell."),
        ("What does a germinating seed use for food before it has leaves?", "food stored inside the seed", ["food from the soil", "sunlight only", "air only"], "Leaves make food later."),
        ("Why do we say that a plant moves?", "its parts move, such as leaves turning to light or a tendril coiling", ["it walks from place to place", "it flies", "it swims"], "Plants are fixed in one place."),
        ("Which of these is not a characteristic shared by all living things?", "moving from place to place", ["growing", "respiring", "reproducing"], "Most plants stay in one place."),
        ("How does a fish breathe?", "it takes in oxygen dissolved in water through its gills", ["it breathes air through its nose", "it does not breathe", "through its scales"], "Gills are its breathing organs."),
        ("Why is the life cycle of a frog an example of metamorphosis?", "the young (tadpole) looks very different from the adult", ["the frog never changes", "the egg is very large", "the frog lives only on land"], "Insects such as butterflies also go through metamorphosis."),
        ("What happens to a tadpole's tail as it becomes a froglet?", "it slowly disappears", ["it becomes longer", "it turns into a leg", "it falls off in one day"], "It grows legs at the same time."),
        ("Which stage of a mosquito does not feed and is inside a case?", "the pupa", ["the larva", "the adult", "the egg laid on dry land"], "The adult comes out of the pupa.")]

# =================================================================== Chapter 11: nature's treasures
RES = {"a renewable resource": ["sunlight", "wind", "water in rivers", "forests (if replanted)", "air", "solar energy", "rainwater", "bamboo (if replanted)", "wind energy", "flowing water in streams"],
       "a non-renewable resource": ["coal", "petroleum", "natural gas", "iron ore", "copper ore", "mica", "bauxite", "limestone", "gold"]}
RRR = {"reducing": ["switching off fans and lights when leaving a room", "carrying a cloth bag instead of taking a new plastic bag", "turning off the tap while brushing", "using both sides of a sheet of paper"],
       "reusing": ["using an old jam bottle to store spices", "giving old books to younger children", "using a used carton as a pen stand", "using old clothes as dusters"],
       "recycling": ["sending old newspapers to be made into new paper", "melting old glass bottles to make new ones", "making compost from vegetable peels", "melting aluminium cans to make new cans"]}
NATMAN = {"a natural resource": ["coal", "wood", "sunlight", "soil", "water", "iron ore", "air"],
          "a human-made material": ["plastic", "glass", "paper", "cement", "nylon", "steel", "brick"]}
USES = [("the wind", "turning windmills to make electricity and pushing sailing boats"), ("sunlight", "plants making food and solar panels making electricity"),
        ("forests", "giving wood, fruits, medicines and homes for animals"), ("soil", "growing crops and holding water for plants"),
        ("coal", "a fuel burnt in thermal power stations"), ("petroleum", "making petrol, diesel and kerosene"), ("natural gas", "a cleaner fuel used as CNG in vehicles"),
        ("water", "drinking, farming and making hydroelectricity"), ("air", "giving oxygen for breathing and carbon dioxide for plants")]
NAT = [("What are natural resources?", "useful things that we get from nature, such as air, water, soil, sunlight and minerals", ["things made in factories", "only money", "only plastic"], "We must use them wisely."),
       ("Which gas makes up most of the air?", "nitrogen (about 78%)", ["oxygen (about 78%)", "carbon dioxide (about 50%)", "hydrogen"], "Oxygen is about 21%."),
       ("About how much of the air is oxygen?", "about 21%", ["about 78%", "about 1%", "about 50%"], "Nitrogen is about 78%."),
       ("Why are coal and petroleum called fossil fuels?", "they formed from the remains of living things buried millions of years ago", ["they were made last year", "they come from the Sun", "they are made of rocks only"], "They take millions of years to form."),
       ("Why should we use less coal and petroleum?", "they will run out and they pollute the air", ["they grow back quickly", "they are renewable", "they are clean fuels"], "Use solar and wind energy where possible."),
       ("What is the difference between a renewable and a non-renewable resource?", "a renewable resource is replaced naturally; a non-renewable one runs out", ["they are the same", "renewable resources run out fast", "non-renewable resources grow back"], "Sunlight is renewable; coal is not."),
       ("Why is soil important?", "plants grow in it and it holds water and nutrients", ["it gives us petrol", "it makes rain", "it makes the Sun shine"], "It takes hundreds of years to form."),
       ("What is the main source of energy for the Earth?", "the Sun", ["the Moon", "coal", "the wind"], "Wind and rain are also driven by the Sun."),
       ("How can we save water at home?", "close the tap while brushing and reuse water for plants", ["leave taps running", "wash cars with a running pipe", "throw waste into rivers"], "Every drop counts."),
       ("What happens to soil when trees are cut down?", "it can be washed or blown away more easily", ["it becomes more fertile", "it turns into rock", "nothing happens"], "Tree roots hold the soil."),
       ("Why are forests called the lungs of the Earth?", "trees take in carbon dioxide and give out oxygen", ["forests make rain stop", "forests breathe like animals", "forests make coal"], "They also keep the air clean."),
       ("What do the 3 Rs stand for?", "reduce, reuse and recycle", ["read, write and recite", "run, rest and relax", "rain, river and road"], "They help save resources."),
       ("Which of these is an example of reuse?", "using an old jam bottle to store spices", ["throwing a bottle in the river", "burning plastic", "buying a new bottle every day"], "Reuse means using something again."),
       ("What is a mineral?", "a natural substance found in rocks, such as iron ore or mica", ["a kind of plant", "a type of air", "a food made in a factory"], "India has many minerals."),
       ("Why is air important for living things?", "it gives oxygen for breathing", ["it gives food", "it makes rocks", "it makes metals"], "Plants also need carbon dioxide from the air."),
       ("Which of these is a way the wind helps us?", "drying clothes and turning windmills", ["making coal", "making soil from nothing", "making iron"], "It also helps in winnowing."),
        ("How does sunlight help plants?", "plants use it to make their food", ["it makes them fall over", "it melts the leaves", "it gives them water"], "This process is photosynthesis."),
        ("Which gas in the air do plants use to make food?", "carbon dioxide", ["nitrogen", "oxygen", "helium"], "They give out oxygen."),
        ("Which gas do we need for breathing?", "oxygen", ["nitrogen", "carbon dioxide", "neon"], "Fires also need oxygen to burn."),
        ("How much of the Earth's water is fresh water that we can use easily?", "very little; most is salty sea water or ice", ["almost all of it", "exactly half", "none of it"], "That is why we must save water."),
        ("What is rainwater harvesting?", "collecting and storing rainwater for later use", ["making rain with machines", "throwing rainwater into drains", "boiling rainwater"], "It also refills groundwater."),
        ("Which fuel is used in many kitchens and comes from petroleum or natural gas?", "LPG", ["coal tar", "wood only", "solar light"], "LPG stands for liquefied petroleum gas."),
        ("Why is solar energy a good choice for the future?", "it is renewable and does not pollute the air", ["it will run out soon", "it pollutes rivers", "it is a fossil fuel"], "Solar panels change sunlight into electricity."),
        ("Which renewable source is used in windmills?", "wind energy", ["coal", "petroleum", "natural gas"], "Large wind farms are found in Tamil Nadu and Gujarat."),
        ("What is a forest's role in the water cycle?", "trees release water vapour and help bring rain", ["forests stop all rain", "forests dry up rivers", "forests make salt water"], "Forests also hold soil."),
        ("Which mineral is used to make aluminium?", "bauxite", ["mica", "coal", "limestone"], "Aluminium is used for utensils and aircraft."),
        ("Which mineral is used in making cement?", "limestone", ["bauxite", "copper ore", "gold"], "Cement is used in buildings."),
        ("What happens if we pump out groundwater faster than rain refills it?", "the water table falls and wells may dry up", ["the water table rises", "the soil becomes richer", "rivers grow bigger"], "Use groundwater wisely.")]

# =================================================================== Chapter 12: beyond Earth
PLANETS = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
PFACT = [("Mercury", "nearest to the Sun and the smallest of the eight planets"), ("Venus", "the hottest planet and the brightest object in the night sky after the Moon"),
         ("Earth", "the only planet known to have life"), ("Mars", "the red planet"), ("Jupiter", "the largest planet"),
         ("Saturn", "famous for its bright, beautiful rings"), ("Neptune", "farthest from the Sun")]


def c_order(k=None):
    R = _R[0]
    i = R.randrange(8)
    k = k or R.choice(["pos", "after", "before"])
    ords = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"]
    if k == "pos":
        return tq("Which planet is %s from the Sun?" % ords[i], PLANETS[i], R.sample([p for p in PLANETS if p != PLANETS[i]], 3),
                  "Order from the Sun: " + ", ".join(PLANETS) + ".")
    if k == "after" and i < 7:
        return tq("Which planet comes just after %s, going outwards from the Sun?" % PLANETS[i], PLANETS[i + 1], R.sample([p for p in PLANETS if p not in (PLANETS[i], PLANETS[i + 1])], 3),
                  "Order from the Sun: " + ", ".join(PLANETS) + ".")
    if k == "before" and i > 0:
        return tq("Which planet comes just before %s, going outwards from the Sun?" % PLANETS[i], PLANETS[i - 1], R.sample([p for p in PLANETS if p not in (PLANETS[i], PLANETS[i - 1])], 3),
                  "Order from the Sun: " + ", ".join(PLANETS) + ".")
    return None


SB = [("a meteor", "a streak of light seen when a small piece of rock burns up in the air (a shooting star)"), ("an asteroid", "a small rocky body going round the Sun, mostly between Mars and Jupiter"),
      ("a comet", "an icy body that grows a bright tail when it comes near the Sun"), ("a dwarf planet", "a small round body such as Pluto that shares its orbit with other bodies"),
      ("a galaxy", "a huge group of billions of stars, gas and dust"), ("the Milky Way", "the galaxy to which our Sun belongs"), ("an orbit", "the path along which a planet or satellite moves")]
CONS = [("Ursa Major (the Big Dipper, Saptarishi)", "a group of seven bright stars shaped like a big ladle or a question mark"),
        ("Orion (Mriga)", "a hunter-shaped group with three bright stars in a line forming its belt"),
        ("Cassiopeia", "a group of five bright stars shaped like the letter W or M"), ("the Pole Star (Dhruva Tara)", "a star that seems to stay fixed in the northern sky"),
        ("Leo", "a constellation shaped like a lion"), ("Scorpius", "a constellation shaped like a scorpion"), ("Sirius", "the brightest star in the night sky, near Orion"), ("Crux (the Southern Cross)", "a small group of four bright stars forming a cross, seen low in the southern sky")]
SKY = {"a planet": ["Mars", "Jupiter", "Venus", "Saturn", "Neptune", "Mercury", "Uranus"], "a star": ["the Sun", "the Pole Star", "Sirius", "Proxima Centauri", "Alpha Centauri A", "Betelgeuse"],
       "a natural satellite": ["the Moon", "Titan (a moon of Saturn)", "Ganymede (a moon of Jupiter)", "Phobos (a moon of Mars)", "Europa (a moon of Jupiter)"],
       "an artificial satellite": ["Aryabhata", "the International Space Station", "an INSAT weather satellite", "a GPS satellite"]}
SPACE = [("Why do stars seem to move from east to west across the night sky?", "the Earth spins (rotates) from west to east", ["the stars are walking", "the Sun pulls them", "the Moon pushes them"], "The Sun seems to move the same way in the day."),
         ("Why does the Pole Star seem not to move?", "it lies almost exactly above the Earth's axis in the north", ["it is the nearest star", "it is a planet", "it is very small"], "It helps us find north."),
         ("What is a constellation?", "a group of stars that seems to form a pattern in the sky", ["a single planet", "a group of planets", "a type of comet"], "Ursa Major and Orion are constellations."),
         ("Why can we not see stars during the day?", "the bright sunlight hides them", ["stars disappear in the day", "stars go behind the Earth's core", "stars switch off"], "They are in the sky all the time."),
         ("Which is the nearest star to the Earth?", "the Sun", ["the Pole Star", "Sirius", "the Moon"], "After the Sun, the nearest is Proxima Centauri."),
         ("Does the Moon have its own light?", "no; it shines by reflecting sunlight", ["yes, like a star", "only on full moon day", "only during an eclipse"], "Planets also reflect sunlight."),
         ("How do we tell a planet from a star in the night sky?", "planets usually shine steadily while stars twinkle", ["planets twinkle and stars do not", "planets are always red", "stars move faster"], "Planets also change position against the stars."),
         ("What is the solar system?", "the Sun and the planets, moons, asteroids and comets that move around it", ["all the stars in the sky", "only the Earth and the Moon", "a group of stars"], "The Sun is at the centre."),
         ("Where is the asteroid belt?", "between the orbits of Mars and Jupiter", ["between Earth and Venus", "beyond Neptune only", "inside the Sun"], "Asteroids are small rocky bodies."),
         ("What is a comet?", "a ball of ice and dust that grows a long glowing tail near the Sun", ["a planet with rings", "a moon of Mars", "a kind of star"], "Halley's comet returns about every 76 years."),
         ("Why is Pluto no longer called a planet?", "it was reclassified as a dwarf planet in 2006", ["it disappeared", "it crashed into Neptune", "it became a star"], "It is small and shares its orbit with other bodies."),
         ("Which was India's first artificial satellite?", "Aryabhata", ["Chandrayaan-1", "Mangalyaan", "Aditya-L1"], "It was launched in 1975."),
         ("Which Indian mission landed near the south pole of the Moon in 2023?", "Chandrayaan-3", ["Aryabhata", "Mangalyaan", "Chandrayaan-1"], "23 August is now celebrated as National Space Day."),
         ("Which Indian mission was sent to study the Sun?", "Aditya-L1", ["Chandrayaan-3", "Aryabhata", "Mangalyaan"], "It was launched in 2023."),
         ("What are artificial satellites used for?", "weather forecasting, communication, TV and navigation", ["making the Moon shine", "growing crops in space", "making stars"], "They are made and launched by people."),
         ("What is a natural satellite?", "a body that moves around a planet naturally, such as the Moon", ["a machine sent into space", "a star", "a comet"], "Jupiter and Saturn have many moons."),
         ("Why do the stars of Ursa Major appear in different positions at different times of the night?", "the Earth keeps rotating", ["the stars move very fast", "the Moon hides them", "the clouds move them"], "They seem to go round the Pole Star."),
         ("How can you find the Pole Star using Ursa Major?", "follow the line of the two end stars of the ladle", ["look near the Moon", "look at the brightest star", "look towards the south"], "The two pointer stars lead to it."),
         ("Why is the Earth special among the planets?", "it has liquid water, air with oxygen and a suitable temperature for life", ["it is the largest planet", "it has rings", "it is nearest to the Sun"], "It is the only planet known to have life."),
         ("Which planets are called the giant planets?", "Jupiter, Saturn, Uranus and Neptune", ["Mercury, Venus, Earth and Mars", "only the Earth", "the Moon and the Sun"], "The inner planets are small and rocky."),
         ("Why does the Moon look different on different days?", "we see different amounts of its sunlit half as it goes round the Earth", ["it changes its size", "clouds cover parts of it", "it makes its own light some days"], "These are the phases of the Moon."),
         ("How long does the Moon take to go once round the Earth?", "about 27 days", ["one day", "one year", "one hour"], "We see the same face of the Moon.")]


def c_stage(k=None):
    R = _R[0]
    who, seq = R.choice(LIFE)
    st = seq.split(" → ")
    i = R.randrange(len(st) - 1)
    allst = sorted({x for _, q in LIFE for x in q.split(" → ")} - {st[i + 1]})
    w = [x for x in st if x not in (st[i], st[i + 1])] + R.sample([x for x in allst if x not in st], 3)
    return tq("In the life cycle of %s, which stage comes just after the stage '%s'?" % (who, st[i]), st[i + 1], w[:3], "The life cycle is %s." % seq)


def UNITS6b():
    b = {k: once_maker(v) for k, v in [("temp", TEMP), ("evap", EVAP), ("sep", SEPQ), ("germ", GERM), ("nat", NAT), ("space", SPACE)]}
    ther = pairs(THER, "What is %s used for?", "Which thermometer is used for %s?")
    state = pairs(STATE, "What is %s?", "What is the name for %s?")
    stex = odd_one(STEX, "Which of these is an example of %s?", "Which of these is not an example of %s?")
    sep = pairs(SEP, "What is %s?", "Which method of separation is used for %s?")
    mix = pairs(MIX, "Which method is best to separate %s?")
    sbas = pairs(SBASIS, "When is %s used to separate a mixture?", "Which method of separation is used when %s?")
    import in_sci6a
    sol = odd_one(in_sci6a.SOL, "Which of these is %s?", "Which of these is not %s?")
    seq = once_maker(SEQ)
    char = pairs(CHAR, "What is %s, as a characteristic of living things?", "Which characteristic of living things is %s?")
    liv = odd_one(LIV, "Which of these is %s?", "Which of these is not %s?")
    stim = pairs(STIM, "What happens when there is this stimulus: %s?")
    life = pairs(LIFE, "Which is the correct life cycle of %s?", "Whose life cycle is this: %s?")
    chex = odd_one(CHEX, "Which of these is an example of %s?", "Which of these is not an example of %s?")
    res = odd_one(RES, "Which of these is %s?", "Which of these is not %s?")
    uses = pairs(USES, "How is %s useful to us?", "Which natural resource is used for %s?")
    pf = pairs(PFACT, "Which statement describes %s?", "Which planet is %s?")
    cons = pairs(CONS, "What does %s look like?", "Which star or constellation is %s?")
    sky = odd_one(SKY, "Which of these is %s?", "Which of these is not %s?")
    rrr = odd_one(RRR, "Which of these is an example of %s?", "Which of these is not an example of %s?")
    natman = odd_one(NATMAN, "Which of these is %s?", "Which of these is not %s?")
    sb = pairs(SB, "What is %s?", "What do we call %s?")
    return [
        U(7, "temperature-and-its-measurement", 7, PH,
          "Hot and cold; temperature; measuring temperature with clinical, laboratory and digital thermometers; the Celsius scale and the kelvin; ranges and precautions; normal body temperature (summary of NCERT Curiosity Chapter 7).",
          "Temperature and its Measurement", "temperature and its measurement",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 7: clinical, laboratory and digital thermometers, their ranges and precautions, body temperature, °C and kelvin. 100 questions with answers.",
          "A thermometer measures how hot or cold something is.", "Clinical: 35–42 °C. Laboratory: −10 to 110 °C.",
          "<p>Our sense of touch can mislead us, so we measure temperature with a thermometer. A clinical thermometer (35 °C to 42 °C) measures body temperature, which is normally about 37 °C. A laboratory thermometer (−10 °C to 110 °C) measures the temperature of water and other substances.</p>"
          "<p>Hold a thermometer by its end, not by the bulb. Keep a laboratory thermometer upright with the bulb in the liquid, not touching the container, and read it there. Digital thermometers are safer than mercury ones. The SI unit of temperature is the kelvin: K = °C + 273.15.</p>",
          [("Convert 27 °C into kelvin.", ["K = °C + 273.15"], "300.15 K"), ("Which thermometer for boiling water?", ["needs to read 100 °C"], "a laboratory thermometer")],
          ["Using a clinical thermometer for hot water.", "Taking a laboratory thermometer out of the water before reading it.", "Holding the thermometer by its bulb."],
          [("Why does a clinical thermometer have a kink?", "It stops the liquid from falling back, so the reading stays after the thermometer is taken out of the mouth."),
           ("What is normal human body temperature?", "About 37 °C; it varies a little from person to person.")],
          lambda: [("Hot, cold and thermometers", [(ther, 6), (b["temp"], 12), (c_range, 2)]), ("Clinical thermometers", [(c_fever, 8), (b["temp"], 6), (c_range, 6)]), ("Laboratory thermometers", [(b["temp"], 6), (c_range, 8), (c_tdiff, 6)]),
                   ("Celsius and kelvin", [(c_kelvin, 16), (c_tdiff, 4)]), ("Mixed problems", [(c_kelvin, 6), (c_tdiff, 4), (c_range, 4), (c_fever, 6)])]),
        U(8, "a-journey-through-states-of-water", 8, MT,
          "Three states of water; melting, freezing, evaporation, condensation and boiling; factors affecting evaporation; cooling by evaporation; the water cycle (summary of NCERT Curiosity Chapter 8).",
          "A Journey through States of Water", "states of water",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 8: ice, water and water vapour, melting, freezing, evaporation, condensation, what speeds up evaporation, and the water cycle. 100 questions with answers.",
          "Water can be solid, liquid or gas.", "Heat, wind and a large surface speed up evaporation.",
          "<p>Water exists as ice (solid), water (liquid) and water vapour (gas). Ice melts into water at 0 °C, and water freezes at 0 °C. Water changes into vapour by evaporation at any temperature, and quickly by boiling at 100 °C. Vapour cools and changes back to water by condensation, as on a cold glass.</p>"
          "<p>Evaporation is faster when it is hotter, windier and drier, and when the surface is larger. Evaporation cools things, which is why water in a matka stays cool. Evaporation, condensation and rain together make the water cycle.</p>",
          [("Drops form outside a cold glass. Why?", ["water vapour in the air cools"], "condensation"), ("Clothes dry faster on a windy day. Why?", ["wind carries vapour away"], "faster evaporation")],
          ["Thinking drops on a cold glass come through the glass.", "Thinking evaporation happens only at 100 °C.", "Calling the white mist from a kettle water vapour."],
          [("What is the water cycle?", "Water evaporates from seas, lakes and plants, condenses into clouds and falls back as rain or snow, again and again."),
           ("Why does a matka keep water cool?", "Water seeps through its pores and evaporates from the outside, taking heat away.")],
          lambda: [("Three states of water", [(state, 6), (c_wstate, 10), (b["evap"], 4)]), ("Melting and freezing", [(stex, 12), (state, 2), (c_wstate, 6)]), ("Evaporation", [(c_fast, 10), (b["evap"], 10)]),
                   ("Condensation and the water cycle", [(stex, 12), (b["evap"], 8)]), ("Mixed problems", [(stex, 10), (c_fast, 6), (b["evap"], 2), (c_wstate, 2)])]),
        U(9, "methods-of-separation-in-everyday-life", 9, MT,
          "Mixtures and the need to separate them; handpicking, threshing, winnowing, sieving, sedimentation, decantation, filtration, evaporation, condensation, churning and magnetic separation (summary of NCERT Curiosity Chapter 9).",
          "Methods of Separation in Everyday Life", "methods of separation",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 9: handpicking, threshing, winnowing, sieving, sedimentation, decantation, filtration, evaporation, churning and using a magnet. 100 questions with answers.",
          "Choose the method that suits the mixture.", "Insoluble solids: filter. Dissolved salt: evaporate.",
          "<p>A mixture can be separated in different ways. We handpick stones from rice, thresh stalks to get grain, winnow to blow away husk, sieve flour, churn curd to get butter and use a magnet to pick out iron.</p>"
          "<p>Heavy insoluble particles settle in water (sedimentation) and the clear water is poured off (decantation); filtration removes finer particles. A dissolved substance such as salt passes through a filter, so we evaporate the water to get the salt and condense the vapour to get pure water.</p>",
          [("Salt and sand: first step?", ["only salt dissolves"], "add water and filter"), ("Iron filings in sand?", ["iron is magnetic"], "use a magnet")],
          ["Trying to filter out dissolved salt.", "Mixing up sedimentation and decantation.", "Thinking winnowing needs water."],
          [("What is the difference between sedimentation and decantation?", "Sedimentation is the settling of heavy particles; decantation is pouring off the clear liquid above them."),
           ("How do we get salt from sea water?", "Sea water is left in shallow pans; the Sun evaporates the water and the salt is left behind.")],
          lambda: [("Mixtures and handpicking", [(b["sep"], 4), (mix, 8), (sol, 8)]), ("Threshing, winnowing and sieving", [(sep, 10), (sbas, 6), (b["sep"], 4)]),
                   ("Sedimentation, decantation and filtration", [(mix, 8), (sbas, 6), (sol, 6)]), ("Evaporation and condensation", [(sep, 8), (seq, 6), (mix, 6)]),
                   ("Mixed problems", [(sol, 8), (b["sep"], 10), (sbas, 2)])]),
        U(10, "living-creatures-exploring-their-characteristics", 10, LW,
          "Characteristics of living things: growth, nutrition, respiration, excretion, response to stimuli, movement and reproduction; conditions for seed germination; life cycles of plants and animals such as the frog and the mosquito (summary of NCERT Curiosity Chapter 10).",
          "Living Creatures: Exploring their Characteristics", "living creatures",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 10: living and non-living things, growth, respiration, excretion, response to stimuli, reproduction, seed germination and life cycles. 100 questions with answers.",
          "Living things grow, breathe, respond and reproduce.", "Seeds need water, air and warmth to germinate.",
          "<p>Living things share characteristics: they need food, respire, excrete wastes, respond to stimuli such as touch and light, grow, move and reproduce. A car moves and uses fuel, but it cannot grow or reproduce, so it is not living. A seed is alive but resting.</p>"
          "<p>Seeds germinate only with water, air and a suitable temperature. Living things go through a life cycle: a frog goes from egg to tadpole to froglet to adult; a mosquito from egg to larva to pupa to adult.</p>",
          [("Seeds under boiled, cooled water do not germinate. Why?", ["boiling removes air"], "seeds need air"), ("Mimosa leaves fold when touched. Which characteristic?", ["reaction to touch"], "response to stimuli")],
          ["Calling something living just because it moves.", "Thinking seeds need sunlight to germinate.", "Thinking plants do not respire."],
          [("Is a seed living?", "Yes. It is in a resting state and grows into a new plant when it gets water, air and warmth."),
           ("What is the life cycle of a frog?", "Egg → tadpole (breathes with gills) → froglet → adult frog (breathes with lungs and skin).")],
          lambda: [("Living and non-living", [(liv, 14), (char, 6)]), ("Characteristics of living things", [(chex, 14), (stim, 6)]), ("Seeds and germination", [(b["germ"], 12), (char, 4), (stim, 4)]),
                   ("Life cycles", [(life, 8), (c_stage, 8), (b["germ"], 4)]), ("Mixed problems", [(liv, 6), (chex, 8), (b["germ"], 4), (c_stage, 2)])]),
        U(11, "natures-treasures", 11, ES,
          "Natural resources: air, water, sunlight, soil, forests, minerals and fossil fuels; renewable and non-renewable resources; their uses; conserving resources with reduce, reuse and recycle (summary of NCERT Curiosity Chapter 11).",
          "Nature's Treasures", "nature's treasures",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 11: air, water, sunlight, soil, forests, minerals and fossil fuels, renewable and non-renewable resources and how to conserve them. 100 questions with answers.",
          "Nature gives us air, water, soil and energy.", "Renewable resources are replaced; non-renewable ones run out.",
          "<p>Natural resources are useful things we get from nature: air (about 78% nitrogen and 21% oxygen), water, sunlight, wind, soil, forests and minerals. Sunlight, wind and water are renewable, but coal, petroleum and natural gas are fossil fuels that took millions of years to form and will run out.</p>"
          "<p>We must use resources wisely: reduce, reuse and recycle, save water and electricity, plant trees and use solar and wind energy where we can.</p>",
          [("Is coal renewable?", ["it took millions of years to form"], "no: non-renewable"), ("Main gas in the air?", ["about 78%"], "nitrogen")],
          ["Thinking oxygen is the main gas in air.", "Calling petroleum renewable.", "Thinking resources never run out."],
          [("Why are coal and petroleum called fossil fuels?", "They formed from the buried remains of plants and animals over millions of years."),
           ("How can we conserve natural resources?", "By reducing use, reusing and recycling, saving water and electricity, planting trees and using renewable energy.")],
          lambda: [("Natural resources", [(natman, 12), (uses, 4), (b["nat"], 4)]), ("Air, water and sunlight", [(b["nat"], 8), (uses, 4), (res, 8)]), ("Soil, forests and minerals", [(b["nat"], 4), (natman, 8), (uses, 4), (rrr, 4)]),
                   ("Renewable and non-renewable", [(res, 14), (b["nat"], 4), (rrr, 2)]), ("Reduce, reuse and recycle", [(rrr, 20)])]),
        U(12, "beyond-earth", 12, ES,
          "Stars, constellations and the Pole Star; the apparent motion of stars; the Sun as a star; the solar system: planets, moons, asteroids and comets; artificial satellites and Indian space missions (summary of NCERT Curiosity Chapter 12).",
          "Beyond Earth", "beyond Earth",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 12: stars and constellations, the Pole Star, the order of the planets, moons, asteroids and comets, and India's space missions. 100 questions with answers.",
          "The Sun is a star; planets go round it.", "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.",
          "<p>Stars are huge balls of hot gas that give their own light; the Sun is the nearest star. Groups of stars that make patterns are constellations, such as Ursa Major (Saptarishi), Orion and Cassiopeia. Stars seem to move from east to west because the Earth rotates, but the Pole Star seems fixed in the north.</p>"
          "<p>Eight planets go round the Sun: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune. Planets and moons shine by reflected sunlight. Asteroids lie between Mars and Jupiter, and comets grow tails near the Sun. India's Chandrayaan-3 landed near the Moon's south pole in 2023.</p>",
          [("Which planet is fifth from the Sun?", ["Mercury, Venus, Earth, Mars, Jupiter"], "Jupiter"), ("Why do stars seem to move west?", ["the Earth spins"], "the Earth rotates from west to east")],
          ["Calling the Moon a star.", "Thinking stars disappear in the day.", "Calling Pluto the ninth planet."],
          [("How can you tell a planet from a star?", "Stars twinkle, while planets usually shine steadily; planets also move slowly against the stars over many nights."),
           ("Why does the Pole Star seem not to move?", "It lies almost directly above the Earth's North Pole, along the axis about which the Earth turns.")],
          lambda: [("Stars and constellations", [(cons, 10), (b["space"], 10)]), ("The Sun and the planets", [(K(c_order, "pos"), 6), (pf, 8), (sky, 6)]), ("Order of the planets", [(K(c_order, "after"), 5), (K(c_order, "before"), 5), (sky, 10)]),
                   ("Moons, asteroids and comets", [(sb, 10), (sky, 6), (b["space"], 4)]), ("Space missions and mixed problems", [(b["space"], 4), (sky, 12), (cons, 2), (pf, 2)])]),
    ]
