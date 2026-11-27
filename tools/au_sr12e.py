# -*- coding: utf-8 -*-
"""Year 12 Earth and Environmental Science (Australian Curriculum: Senior Secondary, Units 3 and 4) for au_sr.build."""
import math
from au_sr import SR, nq

EES = "Earth and Environmental Science"


def ore_maker(R):
    def f():
        k = R.choice(["metal", "rock", "grade", "life", "life2"])
        if k == "metal":
            t = R.choice([1000, 2000, 5000, 10000, 20000, 50000])
            g, metal = R.choice([(1.5, "copper"), (0.8, "copper"), (2.5, "zinc"), (5.0, "lead"), (60, "iron"), (62, "iron"), (0.05, "uranium oxide"), (1.2, "nickel")])
            m = t * g / 100
            return nq("An ore body contains %d tonnes of ore with a grade of %g%% %s. How many tonnes of %s does it contain?" % (t, g, metal, metal), m,
                      [t * g, t / g, t * g / 10], " t", "Mass of metal = %d × %g ÷ 100 = <b>%g t</b>." % (t, g, m))
        if k == "rock":
            gpt = R.choice([2, 3, 4, 5, 6, 8])
            oz = R.choice([31.1, 62.2, 155.5, 311])
            t = oz / gpt
            return nq("A gold ore has a grade of %d g per tonne. How many tonnes of ore must be processed to obtain %g g of gold?" % (gpt, oz), t, [oz * gpt, gpt / oz, oz / gpt / 1000], " t",
                      "Ore = gold ÷ grade = %g ÷ %d = <b>%.3g t</b>." % (oz, gpt, t))
        if k == "grade":
            ore = R.choice([200, 400, 500, 800, 1000])
            metal = R.choice([2, 4, 5, 8, 10, 12])
            g = metal / ore * 100
            return nq("Processing %d t of ore produces %d t of copper. What is the ore grade, as a percentage?" % (ore, metal), g, [ore / metal, metal / ore, metal * ore / 100], "%",
                      "Grade = %d ÷ %d × 100 = <b>%.3g%%</b>." % (metal, ore, g))
        if k == "life":
            res = R.choice([100, 200, 300, 400, 600, 900, 1200])
            use = R.choice([5, 10, 15, 20, 25, 30])
            y = res / use
            return nq("A coal deposit has reserves of %d million tonnes. If %d million tonnes are mined each year, how long will the reserves last?" % (res, use), y,
                      [res * use, use / res, res - use], " years", "Lifetime = reserves ÷ rate = %d ÷ %d = <b>%.3g years</b>." % (res, use, y))
        res = R.choice([1000, 2000, 3000, 4000])
        use = R.choice([20, 40, 50, 80, 100])
        up = R.choice([2, 4, 5])
        y = res / (use * (1 + up / 100))
        return nq("A deposit holds %d million tonnes. Production is %d million tonnes a year, but a new mine will raise it by %d%%. Using the higher rate, about how long will the deposit last?" % (res, use, up),
                  y, [res / use, res / (use * up), res * up / use / 100], " years", "New rate = %d × %.2f = %.3g Mt per year; %d ÷ %.3g = <b>%.3g years</b>." % (use, 1 + up / 100, use * (1 + up / 100), res, use * (1 + up / 100), y))
    return f


def quake_maker(R):
    def f():
        k = R.choice(["amp", "energy", "tsu", "dist"])
        if k == "amp":
            a, b = R.sample([3.0, 4.0, 4.5, 5.0, 5.6, 6.0, 6.5, 7.0, 8.0, 9.1], 2)
            a, b = min(a, b), max(a, b)
            r = 10 ** (b - a)
            return nq("How many times larger is the ground motion (wave amplitude) of a magnitude %g earthquake than a magnitude %g earthquake?" % (b, a), r,
                      [b - a, 32 ** (b - a), (b - a) * 10], " times", "Each step of 1 is ×10 in amplitude: 10^(%g − %g) = <b>%.3g times</b>." % (b, a, r))
        if k == "energy":
            a = R.choice([4, 5, 6, 7])
            d = R.choice([1, 2, 3])
            r = 32 ** d
            return nq("About how many times more energy is released by a magnitude %d earthquake than a magnitude %d earthquake? (Each step of 1 is about 32 times the energy.)" % (a + d, a), r,
                      [10 ** d, 32 * d, d], " times", "32^%d = <b>%d times</b>." % (d, r))
        if k == "tsu":
            depth = R.choice([1000, 2000, 4000, 5000])
            dist = R.choice([1000, 1500, 2000, 3000, 4000])
            v = math.sqrt(9.8 * depth)
            t = dist * 1000 / v / 3600
            return nq("A tsunami crosses ocean %d m deep. Its speed is v = √(gd). How long does it take to travel %d km? (g = 9.8 m/s²)" % (depth, dist), t,
                      [dist * 1000 / (9.8 * depth) / 3600, dist / v, dist * 1000 / v / 60], " h", "v = √(9.8 × %d) = %.3g m/s; t = %d 000 ÷ %.3g = %.3g s = <b>%.3g h</b>." % (depth, v, dist, v, dist * 1000 / v, t))
        lag = R.choice([10, 20, 30, 40, 50, 60, 80])
        d = lag * 8
        return nq("At a seismic station the S-waves arrive %d s after the P-waves. Using 8 km of distance for each second of lag, how far away is the epicentre?" % lag, d,
                  [lag / 8, lag * 6, lag + 8], " km", "%d × 8 = <b>%d km</b>. Three stations are needed to locate the epicentre." % (lag, d))
    return f


MIN = [
    ("What is an ore?", "rock containing a mineral in high enough concentration to be mined at a profit", ["any rock that contains metal", "a type of fossil fuel", "a pure metal found in nature"], "Whether a deposit is ore depends on price and cost."),
    ("What is ore grade?", "the concentration of the valuable mineral or metal in the ore", ["the colour of the ore", "the depth of the ore", "the hardness of the rock"], "Gold is measured in grams per tonne; iron as a percentage."),
    ("Why can a deposit that was not ore become ore?", "a rise in metal price or a cheaper mining method makes it profitable", ["the rock changes chemically", "the metal grows in the rock", "the deposit moves closer to the surface"], "Economics defines ore."),
    ("Where are Australia's largest iron ore mines?", "the Pilbara region of Western Australia", ["the Bowen Basin, Queensland", "Kalgoorlie, Western Australia", "the Hunter Valley, New South Wales"], "The ore formed from banded iron formations."),
    ("Which Australian deposit is one of the world's largest of copper, gold and uranium?", "Olympic Dam, South Australia", ["Weipa, Queensland", "Mount Isa only for coal", "the Latrobe Valley"], "It is mined underground."),
    ("Where is bauxite (aluminium ore) mined in Australia?", "Weipa (Queensland) and the Darling Range (Western Australia)", ["the Pilbara", "Broken Hill", "Bass Strait"], "Bauxite forms by deep tropical weathering."),
    ("How does bauxite form?", "intense weathering in a hot, wet climate leaches other minerals and leaves aluminium oxides", ["volcanic eruptions", "evaporation of sea water", "metamorphism of limestone"], "It is a residual deposit."),
    ("How did the gold of the Kalgoorlie 'Golden Mile' form?", "hot fluids carried dissolved gold through fractures and deposited it in quartz veins", ["gold fell from meteorites", "gold formed in coal swamps", "gold was carried by glaciers"], "These are hydrothermal deposits."),
    ("What is a placer deposit?", "heavy minerals such as gold concentrated by flowing water in river or beach sands", ["a deposit formed by magma", "a coal seam", "an oil trap"], "The 1850s Victorian gold rush was mostly placer gold."),
    ("Which method is used to explore for ore bodies by measuring small differences in gravity or magnetism?", "geophysical surveys", ["carbon dating", "pollen analysis", "weather radar"], "Drilling then confirms the ore."),
    ("What is the purpose of drilling core samples in exploration?", "to find the depth, size and grade of a possible ore body", ["to start mining at once", "to find fossils", "to measure rainfall"], "Assays of the core give the grade."),
    ("When is open-cut mining used rather than underground mining?", "when the ore is large and close to the surface", ["when the ore is very deep and narrow", "always, for every mine", "only for oil"], "The Super Pit at Kalgoorlie is open-cut."),
    ("How did black coal in the Bowen and Sydney Basins form?", "plant material from ancient swamps was buried and changed by heat and pressure over millions of years", ["from marine plankton", "from volcanic ash", "from limestone"], "Most is Permian, about 250–300 million years old."),
    ("How do oil and natural gas form?", "remains of marine plankton are buried, heated and changed into hydrocarbons, which collect in traps", ["from coal burning underground", "from magma cooling", "from rainwater"], "They need a source rock, reservoir rock and cap rock."),
    ("Why is a cap rock needed for an oil or gas reservoir?", "it is impermeable, so it stops the oil and gas escaping upwards", ["it produces oil", "it stores water", "it heats the oil"], "Shale and salt are common cap rocks."),
    ("What is liquefied natural gas (LNG)?", "natural gas cooled to about −162 °C so it becomes a liquid for transport", ["gas made from coal", "gas from landfill only", "a type of petrol"], "Australia is one of the largest LNG exporters."),
    ("Why are fossil fuels called non-renewable?", "they form over millions of years, far slower than we use them", ["they cannot burn", "they are found only in deserts", "they are made by people"], "Coal, oil and gas are non-renewable."),
    ("What is uranium used for in energy production?", "as fuel for nuclear fission reactors", ["as a fuel in coal power stations", "to make solar panels", "as a fertiliser"], "Australia has the world's largest uranium reserves but no nuclear power stations."),
    ("Why is lithium important for the energy transition?", "it is used in rechargeable batteries for electric vehicles and storage", ["it is burned for electricity", "it replaces coal in steel making", "it is a fuel for jet engines"], "Western Australia is a major lithium producer."),
    ("What is mineral processing (beneficiation)?", "crushing ore and separating the valuable mineral from the waste rock", ["drilling for oil", "rehabilitating a mine", "exploring with satellites"], "Flotation separates many sulfide minerals."),
]
REN = [
    ("What makes a resource renewable?", "it is replaced by natural processes as fast as, or faster than, it is used", ["it can be recycled", "it is cheap", "it is found everywhere"], "Overused renewables can run out."),
    ("Which energy source is renewable?", "solar energy", ["coal", "natural gas", "uranium"], "Australia has very high solar radiation."),
    ("How do solar photovoltaic (PV) cells produce electricity?", "light knocks electrons free in a semiconductor such as silicon, producing a current", ["sunlight heats water to make steam always", "they burn hydrogen", "they use wind"], "Australia has the highest rate of rooftop solar in the world."),
    ("What is a disadvantage of solar and wind power?", "their output varies with weather and time of day, so storage or backup is needed", ["they produce carbon dioxide", "they use fuel", "they cause acid rain"], "Batteries and pumped hydro store energy."),
    ("How does pumped hydro storage, such as Snowy 2.0, work?", "water is pumped uphill when electricity is cheap and released through turbines when it is needed", ["it burns water", "it melts snow for electricity", "it stores electricity in rocks"], "It works like a giant battery."),
    ("What is geothermal energy?", "heat from inside Earth used for heating or to generate electricity", ["energy from the Sun's heat on rocks", "energy from tides", "energy from wind"], "Iceland and New Zealand use a lot of it."),
    ("What is groundwater?", "water stored in pores and fractures of rock and sediment below the water table", ["water in rivers", "water vapour in the air", "water frozen in glaciers"], "Aquifers store groundwater."),
    ("What is the difference between porosity and permeability?", "porosity is how much open space a rock has; permeability is how easily water flows through it", ["they are the same", "porosity is how easily water flows", "permeability is the amount of water stored"], "Clay is porous but not permeable."),
    ("Why is the Great Artesian Basin so important to inland Australia?", "it supplies water for towns, farms and mines across a huge dry area", ["it is a source of salt", "it is a large lake", "it supplies Sydney's water"], "Bores capped since the 1990s save water."),
    ("What is an artesian aquifer?", "a confined aquifer in which pressure pushes water up a bore without pumping", ["an aquifer at the surface", "a lake on a mountain", "an aquifer filled with oil"], "It is trapped between impermeable layers."),
    ("What happens if groundwater is pumped faster than it is recharged?", "the water table falls and bores may run dry", ["the water table rises", "the aquifer grows", "nothing changes"], "This is groundwater mining."),
    ("What is sustainable yield?", "the amount of a resource that can be taken without reducing its long-term availability", ["the maximum amount that can be taken at once", "the yield of one crop", "the total amount of a resource"], "Used for fisheries, forests and water."),
    ("How does soil form?", "weathering of rock combined with organic matter from living things over long periods", ["from volcanic ash only", "from water evaporating", "from glaciers only"], "It can take hundreds of years to form a few centimetres."),
    ("Why is soil considered a non-renewable resource on human timescales?", "it forms extremely slowly but can be lost quickly by erosion", ["it never forms", "it is always being replaced faster than it is used", "it cannot be used"], "Australian soils are old and thin."),
    ("Which practice reduces soil erosion on farms?", "keeping ground cover, such as stubble retention and no-till farming", ["ploughing up and down slopes", "removing all trees", "overgrazing"], "Bare soil blows and washes away."),
    ("What caused the 'Dust Bowl'-like dust storms in Australia during droughts?", "dry, bare soil from overgrazing and clearing was picked up by strong winds", ["volcanic eruptions", "tsunamis", "too much rain"], "Ground cover holds soil."),
    ("What is the Murray–Darling Basin Plan?", "a plan to share water between farms, towns and the environment so the river system stays healthy", ["a plan to build a new river", "a plan for mining in the basin", "a plan to drain the rivers"], "It sets sustainable diversion limits."),
    ("Why are forests a renewable resource only if managed?", "trees regrow, but only if harvesting is slower than regrowth", ["trees never regrow", "forests are always non-renewable", "forests grow back in one year"], "Plantation forestry replants trees."),
    ("What is desalination?", "removing salt from sea water to make fresh water", ["adding salt to water", "filtering river water only", "making rain"], "Perth gets about half of its water from desalination."),
    ("Why does Perth rely on desalination and groundwater?", "rainfall in south-west Western Australia has fallen since the 1970s, reducing dam inflows", ["Perth has no ocean", "Perth gets too much rain", "the dams were never built"], "Climate change has reduced winter rainfall."),
]
IMP = [
    ("What is an environmental impact assessment (EIA)?", "a study of the likely effects of a project on the environment before it is approved", ["a test of the soil after a mine closes", "a weather report", "a count of tourists"], "It considers alternatives and ways to reduce harm."),
    ("What is acid mine drainage?", "acidic water formed when sulfide minerals in mine waste react with air and water", ["rain that falls on a mine", "drinking water from a mine", "water used to cool machines"], "It can carry toxic metals into rivers."),
    ("What are tailings?", "the fine waste left after the valuable mineral has been removed from ore", ["the trucks at a mine", "the ore itself", "the cap rock of an oil field"], "Tailings dams must be carefully managed."),
    ("What is mine rehabilitation?", "returning a mined area to a safe, stable landscape, often with native vegetation", ["opening a new mine", "storing tailings", "drilling for more ore"], "Ranger uranium mine in Kakadu is being rehabilitated."),
    ("Why is the rehabilitation of the Ranger uranium mine important?", "it is surrounded by Kakadu National Park, a World Heritage area and Aboriginal land", ["it is in a city", "it produced coal", "it is under the sea"], "The aim is a landscape that could be part of the park."),
    ("Which is an environmental impact of burning coal for electricity?", "greenhouse gas emissions and air pollution such as sulfur dioxide", ["ozone layer repair", "less carbon dioxide", "more rainfall"], "Coal is the most carbon-intensive fuel."),
    ("What are 'ecosystem services'?", "benefits people get from ecosystems, such as clean water, pollination and flood control", ["services provided by park rangers", "mining services", "bus services in national parks"], "They are often hard to value in money."),
    ("What is the precautionary principle?", "if an action might cause serious harm, lack of full scientific certainty should not delay preventing it", ["always wait for complete proof before acting", "projects must always go ahead", "only scientists can make decisions"], "It is part of Australian environmental law."),
    ("What is an ecological footprint?", "the area of land and water needed to supply a population's resources and absorb its wastes", ["the size of a person's shoe", "the area of a national park", "the number of species in an area"], "Australia's footprint per person is among the highest."),
    ("What is a biodiversity offset?", "protecting or restoring habitat elsewhere to make up for habitat lost to a development", ["killing pests", "building a zoo", "ignoring the habitat loss"], "Offsets are controversial because habitats are not identical."),
    ("Why does Traditional Owners' knowledge matter in managing land?", "Aboriginal and Torres Strait Islander peoples have tens of thousands of years of knowledge of country, such as cultural burning", ["it is only historical", "it replaces all science", "it is not used today"], "Indigenous rangers manage large areas."),
    ("What is cultural burning?", "cool, low-intensity burns lit by Traditional Owners to manage country and reduce fuel loads", ["very hot fires lit in summer", "burning rubbish", "fires caused by lightning"], "It creates a mosaic of burnt and unburnt land."),
    ("How do fisheries quotas help keep fish stocks sustainable?", "they limit the catch to below the rate at which the stock can replace itself", ["they increase the number of boats", "they remove all fish", "they stop fish from breeding"], "Overfishing can make a stock collapse."),
    ("Why do mining companies have to pay a bond to the government?", "so there is money to rehabilitate the site if the company does not", ["to pay workers", "to buy the ore", "to pay for exploration"], "This protects the public from costs."),
    ("What is life-cycle assessment?", "measuring the environmental impact of a product from raw materials to disposal", ["checking the age of rocks", "counting plants", "measuring rainfall"], "It shows where most impact occurs."),
    ("Why is recycling aluminium important?", "it uses only about 5% of the energy needed to make new aluminium from bauxite", ["aluminium cannot be recycled", "it uses more energy than mining", "it makes aluminium heavier"], "It also reduces mining and waste."),
]
HAZ = [
    ("What causes most earthquakes?", "sudden movement along faults as stress built up between plates is released", ["volcanic ash falling", "changes in the weather", "the Moon's gravity alone"], "The point of rupture is the focus."),
    ("What is the epicentre of an earthquake?", "the point on the surface directly above the focus", ["the deepest point of the fault", "the place with the most damage always", "the seismograph station"], "The focus (hypocentre) is underground."),
    ("Which seismic waves arrive first at a seismograph?", "P-waves (primary waves)", ["S-waves", "surface waves", "they all arrive together"], "P-waves are compressional and fastest."),
    ("Which waves usually cause the most damage in an earthquake?", "surface waves", ["P-waves", "S-waves only in the core", "sound waves"], "They have large amplitudes and travel along the surface."),
    ("Why do earthquakes happen in Australia even though it is far from plate boundaries?", "stress from plate movement builds up in the plate and is released on old faults", ["Australia is on a plate boundary", "they are caused by mining only", "they are caused by droughts"], "Examples: Meckering 1968, Newcastle 1989."),
    ("Why did the 1989 Newcastle earthquake cause so much damage despite a magnitude of only 5.6?", "it was shallow and close to a city, and some buildings were on soft sediments that amplified shaking", ["it was magnitude 9", "it caused a tsunami", "it was far from the city"], "Thirteen people died."),
    ("What is liquefaction?", "waterlogged sand or silt loses strength and behaves like a liquid during shaking", ["rock melting into lava", "rain flooding a city", "ice melting on mountains"], "Buildings can sink or tilt."),
    ("What causes a tsunami?", "a sudden movement of the sea floor, usually from a large undersea earthquake, which displaces water", ["strong winds", "the tide", "a heavy rainstorm"], "Landslides and volcanoes can also cause them."),
    ("Why do tsunamis become taller as they reach the coast?", "the wave slows in shallow water, so the water piles up", ["the wind pushes them up", "they gain energy from the beach", "the water gets warmer"], "Their speed is about √(gd)."),
    ("How is Australia warned about tsunamis?", "the Joint Australian Tsunami Warning Centre uses seismic data and ocean sensors", ["by satellites measuring rain", "by counting waves at the beach", "there is no warning system"], "It was set up after the 2004 Indian Ocean tsunami."),
    ("Which type of volcano has gentle slopes and runny basalt lava?", "a shield volcano", ["a stratovolcano", "a cinder cone always", "a caldera only"], "Hawaii's volcanoes are shield volcanoes."),
    ("Why are stratovolcanoes at subduction zones often explosive?", "their magma is viscous and rich in gas, so pressure builds up", ["their lava is very runny", "they have no gas", "they are under the sea"], "Mount Pinatubo and Mount St Helens erupted explosively."),
    ("What is a pyroclastic flow?", "a fast-moving, very hot flow of gas, ash and rock from an eruption", ["a slow lava flow", "a type of earthquake", "a mudslide caused by rain"], "It is one of the deadliest volcanic hazards."),
    ("How can a volcanic eruption cool the global climate?", "sulfur dioxide forms sulfate aerosols in the stratosphere that reflect sunlight", ["ash adds heat to the air", "lava warms the oceans", "it removes oxygen"], "Pinatubo (1991) cooled Earth by about 0.5 °C."),
    ("Which signs can warn that a volcano may erupt?", "small earthquakes, ground swelling and more gas emissions", ["heavy rain", "a drop in sea level", "colder weather"], "Monitoring reduces deaths."),
    ("What can trigger a landslide?", "heavy rain, earthquakes or removal of vegetation on steep slopes", ["cold weather only", "strong sunlight", "wind on flat ground"], "Thredbo (1997) was a landslide disaster."),
    ("What is the difference between hazard and risk?", "a hazard is a possible source of harm; risk combines how likely it is and how severe the consequences are", ["they mean the same", "risk is the cause and hazard is the result", "a hazard is always a disaster"], "Risk = likelihood × consequence."),
    ("Which is a way to reduce the risk of earthquake damage?", "building codes that require flexible, reinforced structures", ["building on soft sediments", "ignoring old faults", "building taller unreinforced brick buildings"], "Planning and drills also help."),
]
CLIM = [
    ("What evidence shows that Earth's climate is warming?", "rising average temperatures, melting ice, sea-level rise and earlier seasonal events", ["more volcanoes", "a stronger Moon", "the ozone hole only"], "Australia has warmed by about 1.5 °C since 1910."),
    ("What is the main cause of the current rapid global warming?", "increased greenhouse gases from burning fossil fuels and land clearing", ["changes in Earth's orbit", "more volcanic eruptions", "the Sun getting much brighter"], "Orbital changes act over tens of thousands of years."),
    ("What do ice cores tell scientists about past climates?", "air bubbles record past CO₂ levels, and isotopes record past temperatures", ["the age of the oceans", "the speed of glaciers today only", "the number of past earthquakes"], "Antarctic cores go back 800 000 years."),
    ("Why does sea level rise as the climate warms?", "warmer water expands, and land ice from glaciers and ice sheets melts into the ocean", ["sea ice melting is the main cause", "rivers carry more sand", "the ocean floor rises"], "Melting floating sea ice hardly changes sea level."),
    ("How is climate change expected to affect bushfire risk in south-eastern Australia?", "hotter, drier conditions increase the number of days with dangerous fire weather", ["fires will stop", "there will be no change", "fires will only happen in winter"], "The 2019–20 Black Summer fires burnt over 24 million hectares."),
    ("What conditions make a bushfire spread fastest?", "high temperature, low humidity, strong winds, dry fuel and uphill slopes", ["cool, humid and still weather", "wet ground and low wind", "flat ground after rain"], "The Forest Fire Danger Index combines these."),
    ("What is a tropical cyclone called in other parts of the world?", "a hurricane (Atlantic) or a typhoon (north-west Pacific)", ["a tornado", "a monsoon", "a front"], "They are the same kind of storm."),
    ("Which hazard usually causes the most damage when a cyclone crosses the coast?", "storm surge and flooding, as well as destructive winds", ["earthquakes", "frost", "dust storms"], "Cyclone Tracy destroyed much of Darwin in 1974."),
    ("Why do floods in Australia often follow La Niña years?", "La Niña brings above-average rainfall to eastern Australia", ["La Niña brings drought", "La Niña stops rain", "La Niña cools the land"], "The 2022 floods in Lismore were extreme."),
    ("What is a heatwave?", "three or more days of unusually high maximum and minimum temperatures for that location", ["one hot afternoon", "a warm winter day", "any day over 25 °C"], "Heatwaves cause more deaths in Australia than any other natural hazard."),
    ("How do urban heat islands form?", "dark roads and buildings absorb heat and there is less vegetation to cool the air", ["cities have more trees", "cities are closer to the Sun", "cities have more wind"], "Trees and light surfaces reduce the effect."),
    ("What is mitigation of climate change?", "reducing greenhouse gas emissions or removing them from the atmosphere", ["adapting to higher temperatures only", "building sea walls", "moving people inland"], "Renewable energy is a mitigation strategy."),
    ("What is adaptation to climate change?", "changing how we live to cope with its effects, such as building sea walls or planting heat-tolerant crops", ["reducing greenhouse gases", "stopping all emissions at once", "ignoring the changes"], "Both mitigation and adaptation are needed."),
    ("How does climate change threaten the Great Barrier Reef?", "warmer water causes mass coral bleaching, and acidification weakens skeletons", ["colder water kills the coral", "more fish eat the coral", "less sunlight reaches the reef"], "Mass bleaching happened in 2016, 2017, 2020, 2022 and 2024."),
    ("What is a climate model?", "a computer model that uses physics to simulate the climate and project future changes", ["a map of today's weather", "a physical model of a volcano", "a list of past temperatures only"], "Models are tested against past climate."),
    ("What is the difference between weather and climate?", "weather is short-term conditions; climate is the average pattern over decades", ["they are the same", "climate changes daily", "weather is measured over 30 years"], "Climate is often averaged over 30 years."),
    ("Which feedback could speed up warming in the Arctic?", "melting snow and ice exposes darker surfaces that absorb more sunlight", ["more clouds always cool", "more ice forms", "less water vapour"], "This is the ice–albedo feedback."),
    ("Why is drought a major hazard for Australian farming?", "rainfall is very variable, and long dry periods reduce crops, pasture and water supply", ["Australia has no droughts", "drought only affects cities", "drought increases crop yields"], "The Millennium Drought lasted from about 1997 to 2009."),
]


def u19(X):
    return [
        ("Ores and mineral deposits", [(X.pool(MIN), 12), (X.gen("gen_us_science_g7_natural_resources", "g_origin"), 4), (X.gen("gen_au_science_y8_rock_cycle", "g_aur"), 4)]),
        ("Ore grade calculations", [(X.f(ore_maker), 16), (X.pool(MIN), 4)]),
        ("Exploration and mining", [(X.pool(MIN), 4), (X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_cb"), 10), (X.gen("gen_us_science_g7_natural_resources", "g_use"), 6)]),
        ("Fossil fuels and energy resources", [(X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_res"), 8), (X.f(ore_maker), 8), (X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_where"), 4)]),
        ("Weighing up resource decisions", [(X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_pay"), 12), (X.f(ore_maker), 8)]),
    ]


def u20(X):
    return [
        ("Renewable and non-renewable resources", [(X.pool(REN), 8), (X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_res"), 6), (X.gen("gen_us_science_ess_sustainability_and_human_impact", "g_sol"), 6)]),
        ("Groundwater and aquifers", [(X.pool(REN), 6), (X.gen("gen_us_science_ess_water_and_earth_materials", "g_poro"), 6), (X.gen("gen_us_science_ess_water_and_earth_materials", "g_perm"), 3), (X.gen("gen_us_science_ess_water_and_earth_materials", "g_prop"), 5)]),
        ("Soil as a resource", [(X.pool(REN), 4), (X.gen("gen_us_science_ess_landforms_and_earth_processes", "g_rate"), 11), (X.gen("gen_us_science_ess_water_and_earth_materials", "g_wth"), 5)]),
        ("Renewable energy", [(X.pool(REN), 2), (X.gen("gen_us_science_phys_energy_conversion_and_efficiency", "g_eff"), 12), (X.gen("gen_us_science_phys_energy_conversion_and_efficiency", "g_power"), 6)]),
        ("Sustainable use of resources", [(X.gen("gen_us_science_ess_sustainability_and_human_impact", "g_fish"), 12), (X.gen("gen_us_science_ess_sustainability_and_human_impact", "g_pop"), 8)]),
    ]


def u21(X):
    return [
        ("Impacts of resource use", [(X.pool(IMP), 6), (X.gen("gen_us_science_g7_human_impact_on_the_environment", "g_impact"), 10), (X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_cb"), 4)]),
        ("Managing mine sites", [(X.pool(IMP), 4), (X.gen("gen_us_science_g7_human_impact_on_the_environment", "g_total"), 10), (X.gen("gen_us_science_ess_sustainability_and_human_impact", "g_red"), 6)]),
        ("Ecological footprints", [(X.gen("gen_us_science_ess_sustainability_and_human_impact", "g_foot"), 16), (X.pool(IMP), 4)]),
        ("Reducing human impacts", [(X.gen("gen_us_science_ess_sustainability_and_human_impact", "g_red"), 12), (X.gen("gen_us_science_ess_sustainability_and_human_impact", "g_sol"), 7), (X.pool(IMP), 1)]),
        ("Evaluating management strategies", [(X.gen("gen_us_science_ess_sustainability_and_human_impact", "g_fish"), 11), (X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_pay"), 8), (X.pool(IMP), 1)]),
    ]


def u22(X):
    return [
        ("Earthquakes", [(X.pool(HAZ), 10), (X.gen("gen_us_science_ess_earths_interior_and_mantle_convection", "g_lag"), 6), (X.f(quake_maker), 4)]),
        ("Measuring and locating earthquakes", [(X.f(quake_maker), 12), (X.gen("gen_us_science_ess_earths_interior_and_mantle_convection", "g_travel"), 8)]),
        ("Tsunamis and volcanoes", [(X.pool(HAZ), 6), (X.f(quake_maker), 6), (X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_haz"), 8)]),
        ("Hazard, risk and preparation", [(X.pool(HAZ), 2), (X.gen("gen_us_science_g8_forecasting_natural_hazards", "g_sign"), 6), (X.gen("gen_us_science_g8_forecasting_natural_hazards", "g_tech"), 6), (X.gen("gen_us_science_ess_landforms_and_earth_processes", "g_scale"), 6)]),
        ("Interpreting hazard data", [(X.f(quake_maker), 10), (X.gen("gen_us_science_ess_landforms_and_earth_processes", "g_rate"), 10)]),
    ]


def u23(X):
    return [
        ("Evidence for climate change", [(X.pool(CLIM), 6), (X.gen("gen_us_science_ess_climate_change_data_and_models", "g_rate"), 6), (X.gen("gen_us_science_ess_climate_and_energy_flow", "g_ice"), 8)]),
        ("Causes and feedbacks", [(X.pool(CLIM), 4), (X.gen("gen_us_science_g6_global_temperature_and_climate_change", "g_cause"), 6), (X.gen("gen_us_science_g6_global_temperature_and_climate_change", "g_co2"), 6), (X.gen("gen_us_science_ess_feedbacks_in_earth_systems", "g_fb"), 4)]),
        ("Bushfires, cyclones, floods and heatwaves", [(X.pool(CLIM), 6), (X.gen("gen_us_science_ess_climate_change_data_and_models", "g_imp"), 10), (X.gen("gen_us_science_ess_natural_resources_and_hazards", "g_haz"), 4)]),
        ("Sea level and climate projections", [(X.gen("gen_us_science_ess_climate_change_data_and_models", "g_sea"), 12), (X.gen("gen_us_science_ess_climate_change_data_and_models", "g_scen"), 6), (X.pool(CLIM), 2)]),
        ("Mitigation and adaptation", [(X.gen("gen_us_science_ess_climate_change_data_and_models", "g_fc"), 12), (X.gen("gen_us_science_ess_carbon_cycle_and_earth_systems", "g_budget"), 8)]),
    ]


def UNITS():
    return [
        SR(EES, 3, 19, "mineral-and-energy-resources", "Use of non-renewable Earth resources",
           "How mineral and energy resources form (magmatic, hydrothermal, sedimentary and residual deposits, coal, oil and gas); ore and ore grade; exploration and mining methods; Australian resources; reserves and the lifetime of non-renewable resources.",
           "Mineral and Energy Resources", "mineral and energy resources",
           "Free Year 12 Earth and Environmental Science worksheets on mineral and energy resources: ores, ore grade, exploration, mining, coal, oil, gas, uranium, lithium and Australian deposits. 100 questions with answers.",
           "Ore = a deposit that can be mined at a profit.", "Mass of metal = mass of ore × grade.",
           "<p>Minerals become concentrated by geological processes: crystallisation of magma, hot (hydrothermal) fluids, weathering (bauxite), sedimentation (banded iron, placer gold) and burial of organic matter (coal, oil and gas). Whether a deposit is <b>ore</b> depends on its grade, size, depth and the price of the metal.</p>"
           "<p>Deposits are found by geological mapping, geophysics and drilling, then mined by open-cut or underground methods. Australia is a world leader in iron ore, coal, LNG, gold, bauxite, uranium and lithium. Non-renewable reserves last only as long as reserves ÷ rate of use.</p>",
           [("5000 t of ore at 1.2% copper. Copper?", ["5000 × 1.2 ÷ 100"], "60 t"),
            ("Reserves 600 Mt, use 20 Mt per year. Lifetime?", ["600 ÷ 20"], "30 years")],
           ["Calling any metal-bearing rock an ore.", "Forgetting to divide the percentage by 100.", "Thinking fossil fuels form in a human lifetime."],
           [("Why does Western Australia have so much iron ore?", "Banded iron formations laid down 2.5 billion years ago in the Hamersley Basin were later enriched by weathering to very high-grade ore."),
            ("Why are reserves estimates always changing?", "New discoveries, better technology and changing prices change how much of a deposit can be mined profitably.")],
           u19, allow=("grade", "mile")),
        SR(EES, 3, 20, "water-soil-and-renewable-resources", "Use of renewable Earth resources",
           "Renewable resources and sustainable yield; groundwater, aquifers, porosity and permeability; the Great Artesian Basin and Murray–Darling Basin; soil formation, erosion and salinity; solar, wind, hydro and geothermal energy and energy storage.",
           "Water, Soil and Renewable Resources", "water, soil and renewable resources",
           "Free Year 12 Earth and Environmental Science worksheets on renewable resources: groundwater, aquifers, porosity, the Great Artesian Basin, soil erosion, salinity, solar, wind and pumped hydro. 100 questions with answers.",
           "Renewable only if used no faster than it is replaced.", "Porosity stores water; permeability lets it flow.",
           "<p>A resource is renewable if natural processes replace it as fast as it is used. Water, soil, forests and fish can all be overused. <b>Groundwater</b> fills the pores of aquifers; porosity is the space for water and permeability how easily it flows. The Great Artesian Basin supplies much of inland Australia.</p>"
           "<p>Soil forms very slowly from weathered rock and organic matter but is quickly lost by erosion; clearing can also cause dryland salinity. Solar, wind and hydro energy are renewable, but their output varies, so storage such as batteries and pumped hydro (Snowy 2.0) is needed.</p>",
           [("Recharge 50 GL/yr, extraction 70 GL/yr. Water table?", ["extraction > recharge"], "falls by 20 GL of storage each year"),
            ("A 5 kW solar system gives 20 kWh/day. Mean output hours at full power?", ["20 ÷ 5"], "4 hours")],
           ["Thinking a porous rock must be permeable (clay is porous but not permeable).", "Calling all water renewable no matter how fast it is used.", "Saying solar panels work at full output at night."],
           [("What is sustainable yield?", "The amount of a renewable resource that can be taken each year without reducing the amount available in the future."),
            ("Why is soil sometimes called non-renewable?", "It takes hundreds to thousands of years to form a few centimetres but can be eroded in a single storm.")],
           u20),
        SR(EES, 3, 21, "managing-environmental-impacts", "Living on Earth – managing Earth resources",
           "Environmental impacts of extracting and using resources (land clearing, acid mine drainage, tailings, emissions); environmental impact assessment; rehabilitation; ecological footprints; ecosystem services; the precautionary principle; Aboriginal and Torres Strait Islander land management.",
           "Managing Environmental Impacts of Resource Use", "managing environmental impacts",
           "Free Year 12 Earth and Environmental Science worksheets on environmental impacts: acid mine drainage, tailings, rehabilitation, EIA, ecological footprints, fisheries, offsets and cultural burning. 100 questions with answers.",
           "Plan, reduce, rehabilitate.", "EIA before approval; rehabilitation after closure.",
           "<p>Extracting and using resources can clear habitat, pollute water (acid mine drainage, tailings), release greenhouse gases and change landscapes. An <b>environmental impact assessment</b> predicts these effects before a project is approved and sets conditions to reduce them.</p>"
           "<p>Management includes rehabilitation (as at the Ranger uranium mine in Kakadu), recycling, quotas, offsets, the precautionary principle and the knowledge of Traditional Owners, such as cultural burning. Ecological footprints measure how much land and water a population needs.</p>",
           [("Footprint 6.8 global ha per person; Earth can supply 1.6. How many Earths?", ["6.8 ÷ 1.6"], "about 4.3 Earths"),
            ("Recycled aluminium uses 5% of the energy. Energy saved?", ["100% − 5%"], "95%")],
           ["Thinking rehabilitation restores exactly the original ecosystem.", "Saying ecosystem services are free and unlimited.", "Forgetting that impacts can continue long after a mine closes."],
           [("What makes acid mine drainage so hard to stop?", "Once sulfide minerals in waste rock are exposed to air and water they keep forming acid, sometimes for centuries, so waste must be covered or treated."),
            ("Why is Indigenous land management important?", "Traditional Owners have managed country for tens of thousands of years; practices such as cultural burning reduce fuel loads and protect biodiversity.")],
           u21),
        SR(EES, 4, 22, "geological-hazards", "Earth processes and hazards",
           "Earthquakes, faults and seismic waves; magnitude and locating epicentres; intraplate earthquakes in Australia; tsunamis; volcano types and volcanic hazards; landslides and liquefaction; hazard, risk, monitoring and mitigation.",
           "Geological Hazards: Earthquakes, Tsunamis and Volcanoes", "geological hazards",
           "Free Year 12 Earth and Environmental Science worksheets on geological hazards: earthquakes, seismic waves, magnitude, locating epicentres, tsunamis, volcanoes, landslides and risk. 100 questions with answers.",
           "Risk = likelihood × consequence.", "Each step of 1 in magnitude: ×10 amplitude, about ×32 energy.",
           "<p>Earthquakes release stress built up at plate boundaries and inside plates; P-waves arrive first, then S-waves and destructive surface waves. The S–P lag at three stations locates the epicentre. Magnitude is logarithmic: each step of 1 means 10 times the amplitude and about 32 times the energy.</p>"
           "<p>Undersea earthquakes can cause tsunamis, whose speed is about √(gd). Volcanoes range from gentle shield volcanoes to explosive stratovolcanoes with pyroclastic flows. Monitoring, building codes, warning systems and land-use planning reduce risk.</p>",
           [("Magnitude 7 vs 5: amplitude ratio?", ["10^(7 − 5)"], "100 times"),
            ("S–P lag of 25 s (8 km per s). Distance?", ["25 × 8"], "200 km")],
           ["Thinking magnitude 6 is twice as strong as magnitude 3.", "Saying tsunamis are caused by wind.", "Thinking Australia has no earthquakes."],
           [("Why is the damage from an earthquake not decided by magnitude alone?", "Depth, distance from towns, soil type (soft sediments amplify shaking), building quality and time of day all matter."),
            ("Why did the 2004 Indian Ocean tsunami lead to a warning centre in Australia?", "It showed that tsunamis can cross whole oceans in hours; seismic and sea-level sensors now give warnings to the Australian coast.")],
           u22),
        SR(EES, 4, 23, "climate-change-and-weather-hazards", "Natural and human-induced climate change",
           "Evidence for climate change (temperature records, ice cores, sea level); causes and feedbacks; climate models and projections; weather and climate hazards in Australia (bushfires, cyclones, floods, droughts, heatwaves); mitigation and adaptation.",
           "Climate Change and Weather Hazards", "climate change and weather hazards",
           "Free Year 12 Earth and Environmental Science worksheets on climate change and hazards: evidence, ice cores, feedbacks, sea-level rise, bushfires, cyclones, floods, heatwaves, mitigation and adaptation. 100 questions with answers.",
           "More greenhouse gases → enhanced greenhouse effect → warming.", "Mitigation reduces emissions; adaptation copes with the effects.",
           "<p>Thermometer records, ice cores, ocean heat, shrinking ice and rising sea level all show warming. The main cause of recent warming is the increase in greenhouse gases from fossil fuels and land clearing; feedbacks such as ice–albedo and water vapour amplify it.</p>"
           "<p>In Australia a warmer climate brings more extreme heat and dangerous fire weather, heavier downpours, longer droughts in some regions and coral bleaching. Responses are <b>mitigation</b> (cutting emissions, renewable energy) and <b>adaptation</b> (planning, building standards, heat plans).</p>",
           [("Sea level rose 20 cm from 1900 to 2020. Mean rate?", ["200 mm ÷ 120 years"], "about 1.7 mm per year"),
            ("CO₂ was 280 ppm before 1800 and is 420 ppm now. % increase?", ["(420 − 280) ÷ 280 × 100"], "50%")],
           ["Confusing weather (days) with climate (decades).", "Saying melting sea ice is the main cause of sea-level rise.", "Thinking the ozone hole causes global warming."],
           [("How do scientists know CO₂ was lower in the past?", "Air bubbles trapped in Antarctic ice cores record CO₂ levels over 800 000 years; levels never went above about 300 ppm before industrialisation."),
            ("Is a hot summer proof of climate change?", "No single event proves it, but the long-term trend in temperatures and the increase in extreme heat are clear evidence.")],
           u23),
    ]
