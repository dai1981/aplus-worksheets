# -*- coding: utf-8 -*-
"""Ontario Science and Technology 2022, Grade 8 (B Cells, C Fluids, D Systems in Action, E Water Systems). Built by caon_sci.build."""
from caon_sci import CU, tq

AU8C, SG5C, SG1C, UK7C = "gen_au_science_y8_cells", "gen_sg_science_p5_cells", "gen_sg_science_s1_cells", "gen_uk_science_y7_cells"
UK7S, US6C, US6P, SG2T = ("gen_uk_science_y7_specialised_cells_and_organisation", "gen_us_science_g6_cells_and_cell_theory",
                          "gen_us_science_g6_parts_of_a_cell", "gen_sg_science_s2_transport_systems_in_living_things")
UK9P, SG2P, UK7P = "gen_uk_science_y9_pressure", "gen_sg_science_s2_forces_and_pressure", "gen_uk_science_y7_particles_and_states_of_matter"
UK9W, SG2W, US8F, UK5M = "gen_uk_science_y9_work_and_moments", "gen_sg_science_s2_energy_and_work_done", "gen_us_science_g8_forces_and_motion", "gen_uk_science_y5_levers_pulleys_and_gears"
AU4W, SG5W, UK4W = "gen_au_science_y4_the_water_cycle", "gen_sg_science_p5_the_water_cycle", "gen_uk_science_y4_the_water_cycle"
SG6M, US7H = "gen_sg_science_p6_mans_impact_on_the_environment", "gen_us_science_g7_human_impact_on_the_environment"
US5W, US6W, USEW = "gen_us_science_g5_water_on_earth", "gen_us_science_g6_the_water_cycle", "gen_us_science_ess_water_and_earth_materials"


def ul(*xs):
    return "".join("<li>%s</li>" % x for x in xs)


def L(lead, *xs):
    return "<p><b>%s</b></p><ul>%s</ul>" % (lead, ul(*xs))


def num(x):
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return s


def s_cells(X):
    pool = X.pool([
        ("What does the cell theory say?", "All living things are made of cells, cells are the basic unit of life, and new cells come from existing cells.", ["All cells are the same size.", "Only animals have cells.", "Cells come from non-living things."], "This is the cell theory."),
        ("Which part controls the activities of the cell?", "the nucleus", ["the cell membrane", "the vacuole", "the cytoplasm"], "The nucleus holds the DNA."),
        ("Which part controls what enters and leaves the cell?", "the cell membrane", ["the nucleus", "the cell wall", "the chloroplast"], "It is selectively permeable."),
        ("Which part is found in plant cells but not animal cells?", "the cell wall", ["the cell membrane", "the nucleus", "the cytoplasm"], "The cell wall gives plant cells a firm shape."),
        ("Where does photosynthesis happen in a plant cell?", "in the chloroplasts", ["in the nucleus", "in the cell wall", "in the vacuole"], "Chloroplasts contain green chlorophyll."),
        ("What does the large vacuole in a plant cell store?", "water and dissolved substances", ["DNA", "chlorophyll", "bones"], "A full vacuole keeps the plant firm."),
        ("Which part releases energy from food?", "the mitochondria", ["the cell wall", "the vacuole", "the nucleus"], "Cellular respiration happens in the mitochondria."),
        ("What is cytoplasm?", "the jelly-like fluid where most cell activities happen", ["the outer wall of a cell", "the control centre", "a green pigment"], "Organelles float in the cytoplasm."),
        ("Which scientist first named cells after looking at cork?", "Robert Hooke", ["Isaac Newton", "Marie Curie", "Charles Darwin"], "Hooke used an early microscope in 1665."),
        ("A microscope has a 10× eyepiece and a 40× objective lens. What is the total magnification?", "400×", ["50×", "40×", "4000×"], "10 × 40 = 400."),
        ("Which part of a microscope do you turn first to focus at low power?", "the coarse adjustment knob", ["the fine adjustment knob at high power", "the stage clips", "the light switch"], "Use coarse focus only with low power."),
        ("Which is a unicellular organism?", "an amoeba", ["a maple tree", "a frog", "a mushroom"], "Unicellular means one cell."),
        ("Why are cells so small?", "Small cells can move materials in and out quickly through their membrane.", ["Small cells are older.", "Large cells cannot have a nucleus.", "Cells are small because they are dead."], "Surface area matters."),
        ("Which is the correct order from smallest to largest?", "cell → tissue → organ → organ system → organism", ["organ → cell → tissue → organism", "tissue → cell → organ → system", "organism → organ → cell → tissue"], "Cells group into tissues, then organs."),
    ])
    return [
        ("The cell theory", [(pool, 6), (X.gen(US6C, "g_living"), 6), (X.gen(US6C, "g_uni"), 5), (X.gen(US6C, "g_type"), 3)]),
        ("Parts of a cell", [(X.gen(US6P, "g_label", n=6), 6), (X.gen(US6P, "g_job"), 5), (X.gen(SG5C, "g_func"), 5), (pool, 4)]),
        ("Plant and animal cells", [(X.gen(US6P, "g_plantanimal"), 6), (X.gen(SG5C, "g_has"), 6), (X.gen(UK7C, "g_where"), 4), (pool, 4)]),
        ("Microscopes", [(X.gen(UK7C, "g_mag", n=6), 6), (X.gen(US6C, "g_mag", n=5), 5), (X.gen(UK7C, "g_mic"), 5), (X.gen(US6C, "g_size", n=4), 4)]),
        ("Cell investigations", [(X.gen(UK7C, "g_pic", n=4), 4), (X.B(UK7C, "B5"), 4), (X.B(US6C, "B5"), 4), (X.gen(SG1C, "g_infer"), 4), (X.B(US6P, "B5"), 4)]),
    ]


def s_cellproc(X):
    pool = X.pool([
        ("What is diffusion?", "the movement of particles from an area of high concentration to an area of low concentration", ["movement from low to high concentration only", "a kind of cell division", "the making of food by plants"], "Oxygen diffuses into cells."),
        ("What is osmosis?", "the diffusion of water across a cell membrane", ["the movement of food in the stomach", "the division of a cell", "the making of chlorophyll"], "Water moves toward the side with more dissolved substances."),
        ("A slice of potato is placed in very salty water. What happens?", "Water leaves the potato cells by osmosis, so the slice becomes soft and limp.", ["The potato gains water and swells.", "Nothing happens.", "The potato turns green."], "Water moves to the saltier side."),
        ("Why do wilted celery sticks become firm in fresh water?", "Water enters the cells by osmosis and fills the vacuoles.", ["Salt leaves the celery.", "The celery grows new cells in minutes.", "The water freezes inside."], "Turgor keeps plants firm."),
        ("What does 'selectively permeable' mean?", "lets some substances through but not others", ["lets nothing through", "lets everything through", "is made of glass"], "The cell membrane is selectively permeable."),
        ("Why do cells divide?", "for growth, repair and to replace old cells", ["to get smaller", "to stop living", "to make the body lighter"], "Skin cells are replaced every few weeks."),
        ("What is a tissue?", "a group of similar cells that do the same job", ["one single cell", "a whole organism", "a kind of organelle"], "Muscle tissue is made of muscle cells."),
        ("Why does a red blood cell have no nucleus?", "There is more space to carry oxygen.", ["It is a dead cell.", "It is a plant cell.", "It does not need oxygen."], "Its form suits its function."),
        ("Why are nerve cells long?", "to carry messages over long distances in the body", ["to store fat", "to make food", "to protect bones"], "Specialized cells have special shapes."),
        ("Why do root hair cells have long thin extensions?", "to increase surface area for taking in water", ["to make food by photosynthesis", "to protect the root from insects", "to store starch only"], "More surface area means more absorption."),
        ("Which is a way that cells help keep the body healthy?", "white blood cells destroy germs", ["red blood cells make bones", "skin cells digest food", "nerve cells pump blood"], "White blood cells are part of the immune system."),
        ("How has cell research helped medicine?", "Understanding cells led to vaccines, cancer treatments and stem-cell research.", ["It has not helped at all.", "It only made microscopes cheaper.", "It made cells bigger."], "Canadian researchers discovered stem cells in 1961."),
    ])
    return [
        ("Diffusion and osmosis", [(pool, 6), (X.gen(SG2T, "g_dif"), 6), (X.gen(SG2T, "g_sa"), 5), (X.gen(SG2T, "g_ex"), 3)]),
        ("Specialized cells", [(X.gen(UK7S, "g_spec"), 7), (X.gen(UK7S, "g_diff"), 6), (pool, 4), (X.gen(SG5C, "g_where"), 3)]),
        ("Cells, tissues and organs", [(X.gen(UK7S, "g_level", n=7), 7), (X.gen(UK7C, "g_org"), 6), (pool, 4), (X.B(UK7S, "B1"), 3)]),
        ("Unicellular and multicellular life", [(X.gen(US6C, "g_uni", n=5), 5), (X.gen(SG5C, "g_size"), 5), (X.B(SG5C, "B1"), 4), (X.B(SG5C, "B2"), 4), (pool, 2)]),
        ("Cells and health", [(pool, 6), (X.B(UK7S, "B5"), 4), (X.B(SG2T, "B5"), 4), (X.B(SG5C, "B5"), 3), (X.gen(SG2T, "g_ves"), 3)]),
    ]


LIQ = [("water", 1.0), ("vegetable oil", 0.92), ("corn syrup", 1.38), ("honey", 1.42), ("rubbing alcohol", 0.79), ("dish soap", 1.06), ("milk", 1.03), ("maple syrup", 1.33)]
SOL = [("a wood block", 0.6), ("a cork", 0.24), ("an ice cube", 0.92), ("a plastic bead", 1.2), ("a rubber eraser", 1.5), ("a steel bolt", 7.8), ("an aluminum nut", 2.7), ("a grape", 1.1), ("a candle wax chip", 0.9)]


def dens_calc(R):
    def f():
        v = R.choice([10, 20, 25, 40, 50, 80, 100, 125, 200])
        d = R.choice([0.4, 0.5, 0.6, 0.8, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 7.5])
        m = v * d
        if m != int(m):
            return None
        m = int(m)
        ans = d
        w = [v / m, m * v, m - v]
        w = ["%s g/cm³" % num(x) for x in w if abs(x - ans) > 1e-9 and x > 0]
        if len(set(w)) < 3:
            return None
        sink = "sinks" if d > 1 else "floats"
        return tq("An object has a mass of %d g and a volume of %d cm³. What is its density?" % (m, v), "%s g/cm³" % num(ans), w[:3],
                  "Density = mass ÷ volume = %d ÷ %d = %s g/cm³. In water (1 g/cm³) it %s." % (m, v, num(ans), sink))
    return f


def float_sink(R):
    def f():
        if R.random() < 0.5:
            o, d = R.choice(SOL)
            l, dl = R.choice(LIQ[:3] + LIQ[4:5])
            if abs(d - dl) < 0.05:
                return None
            ans = "it floats" if d < dl else "it sinks"
            return tq("%s has a density of %s g/cm³. %s has a density of %s g/cm³. What happens when %s is placed in %s?" % (
                o[0].upper() + o[1:], num(d), l[0].upper() + l[1:], num(dl), o, l), ans, ["it floats" if ans == "it sinks" else "it sinks", "it dissolves", "it changes into a gas"],
                "Objects float in a fluid that is denser than they are. %s < %s?" % (num(d), num(dl)) if False else
                "%s is %s dense than %s, so %s." % (o[0].upper() + o[1:], "less" if d < dl else "more", l, ans))
        a, b = R.sample(LIQ, 2)
        top = a if a[1] < b[1] else b
        bot = b if top is a else a
        return tq("%s (%s g/mL) and %s (%s g/mL) are poured into a tall glass. They do not mix. Which ends up on top?" % (
            a[0][0].upper() + a[0][1:], num(a[1]), b[0], num(b[1])), top[0], [bot[0], "they mix evenly", "neither, both sink"],
            "The less dense liquid (%s, %s g/mL) floats on the denser one." % (top[0], num(top[1])))
    return f


def pressure_calc(R):
    def f():
        F = R.choice([20, 40, 60, 100, 120, 200, 300, 400, 600, 800])
        A = R.choice([2, 4, 5, 10, 20])
        if F % A:
            return None
        p = F // A
        w = ["%d Pa" % x for x in (F * A, A, F + A) if x != p]
        return tq("A force of %d N pushes on an area of %d m². What is the pressure?" % (F, A), "%d Pa" % p, w[:3],
                  "Pressure = force ÷ area = %d ÷ %d = %d Pa (N/m²)." % (F, A, p))
    return f


DENS_ROWS = [
        ("What is a fluid?", "a substance that can flow, like a liquid or a gas", ["only liquids", "only solids", "anything that is cold"], "Air and water are both fluids."),
        ("What is viscosity?", "a fluid's resistance to flowing", ["how heavy a fluid is", "how hot a fluid is", "how clear a fluid is"], "Honey has a high viscosity."),
        ("Which fluid has the highest viscosity?", "honey", ["water", "rubbing alcohol", "air"], "Honey flows slowly."),
        ("What happens to the viscosity of maple syrup when it is warmed?", "It decreases, so it flows faster.", ["It increases.", "It stays the same.", "It becomes a solid."], "Warm particles move more freely."),
        ("Why does motor oil come in different viscosities for winter and summer?", "Cold makes oil thicker, so winter oil is thinner to flow easily when cold.", ["Winter oil is thicker.", "Oil does not change with temperature.", "Oil freezes in summer."], "Temperature affects viscosity."),
        ("What is density?", "the mass of a substance in a certain volume", ["how fast a fluid flows", "the temperature of a fluid", "the colour of a fluid"], "Density = mass ÷ volume."),
        ("Why does ice float on water?", "Ice is less dense than liquid water.", ["Ice is denser than water.", "Ice has no mass.", "Water pushes ice up because it is colder."], "This keeps lakes from freezing solid."),
        ("What is buoyancy?", "the upward force a fluid puts on an object", ["the downward pull of gravity", "the flow of a fluid", "the colour of the water"], "It is also called the buoyant force."),
        ("A steel ship floats, but a steel bolt sinks. Why?", "The ship's hollow shape displaces a lot of water, so its overall density is less than water.", ["Ships are made of wood.", "Steel floats when it is cold.", "Bolts are heavier than ships."], "Shape changes overall density."),
        ("What did Archimedes discover?", "The buoyant force equals the weight of the fluid an object pushes aside.", ["Light travels in straight lines.", "Earth orbits the Sun.", "Cells come from cells."], "This is Archimedes' principle."),
        ("Why is it easier to float in the Dead Sea than in Lake Ontario?", "Salty water is denser, so it gives more buoyant force.", ["Fresh water is denser.", "There is less gravity there.", "The water is warmer."], "Denser fluids push up harder."),
        ("Why are oil spills especially harmful to sea birds?", "Oil coats feathers so they lose buoyancy and warmth.", ["Oil makes birds heavier than air only.", "Oil cools the water.", "Oil helps birds float."], "Spills damage ecosystems."),
        ("How does a submarine dive?", "It lets water into its tanks to become denser than the water around it.", ["It turns off its lights.", "It pumps out all the air and floats.", "It uses wheels."], "To rise, it pushes the water out with air."),
]
PRES_ROWS = [
        ("What is a hydraulic system?", "a system that uses a liquid under pressure to move things", ["a system that uses air under pressure", "a system that uses only gears", "a kind of electric circuit"], "Car brakes and excavators use hydraulics."),
        ("What is a pneumatic system?", "a system that uses a gas (usually air) under pressure", ["a system that uses oil", "a system that uses water only", "a system with no fluid"], "Air brakes on buses and dentists' drills use pneumatics."),
        ("Why can gases be compressed but liquids hardly can?", "Gas particles have large spaces between them.", ["Gas particles are bigger.", "Liquids have no particles.", "Gases are always hot."], "This is why tires can be pumped up."),
        ("What does Pascal's law say?", "Pressure applied to a confined fluid is passed equally in all directions.", ["Pressure disappears in fluids.", "Fluids only push down.", "Gases cannot be pressed."], "It explains hydraulic lifts."),
        ("Why do your ears pop in an airplane?", "Air pressure changes as the plane climbs or descends.", ["The engines are loud.", "The air gets warmer.", "Gravity gets stronger."], "Pressure inside and outside the ear evens out."),
        ("Why are dams built thicker at the bottom?", "Water pressure increases with depth.", ["The top needs less paint.", "Fish live at the bottom.", "Wind is stronger at the bottom."], "Deeper water pushes harder."),
        ("A ketchup bottle is squeezed. What happens to the pressure of the ketchup inside?", "It increases, so the ketchup flows out.", ["It decreases.", "It stays at zero.", "It turns into gas."], "Applied force increases fluid pressure."),
        ("What is the unit of pressure?", "the pascal (Pa), which is one newton per square metre", ["the joule", "the kilogram", "the litre"], "1 Pa = 1 N/m²."),
        ("Why do snowshoes stop you sinking into deep snow?", "They spread your weight over a larger area, so the pressure is lower.", ["They make you lighter.", "They melt the snow.", "They increase the pressure."], "Same force, bigger area, less pressure."),
        ("Why does a sharp knife cut better than a blunt one?", "The force acts on a smaller area, so the pressure is greater.", ["A sharp knife is heavier.", "A blunt knife has more pressure.", "Sharpness reduces force."], "Pressure = force ÷ area."),
        ("Why do divers feel more pressure the deeper they go?", "There is more water above them pushing down.", ["Water gets lighter with depth.", "Gravity gets weaker underwater.", "The water is colder."], "Pressure increases with depth."),
        ("How does a hydraulic car lift raise a heavy car with a small force?", "A small force on a small piston makes pressure that pushes a large piston with a bigger force.", ["The oil gets lighter.", "The car becomes lighter.", "Air pushes the car up."], "Pascal's law in action."),
        ("Why does a drinking straw work?", "You lower the air pressure in the straw, and the air pressure on the drink pushes it up.", ["The straw sucks the liquid by magnetism.", "Gravity pushes the drink up.", "The drink is lighter than air."], "Atmospheric pressure pushes the liquid."),
        ("What does a barometer measure?", "air pressure", ["temperature", "wind speed", "rainfall"], "Falling pressure often means stormy weather."),
        ("Why do bike tires need the right air pressure?", "Too little pressure increases friction and can damage the tire; too much makes it burst more easily.", ["Pressure does not matter.", "Higher is always better.", "Tires work best flat."], "Check the number on the tire wall."),
        ("Which machine uses pneumatics?", "a jackhammer powered by compressed air", ["a hydraulic excavator", "a bicycle chain", "a water wheel"], "Compressed air drives it."),
        ("Which machine uses hydraulics?", "a backhoe arm moved by oil-filled cylinders", ["a sailboat", "a kite", "a balloon"], "Liquid under pressure moves the arm."),
        ("Why are hydraulic fluids usually oil instead of water?", "Oil does not freeze easily, lubricates parts and does not cause rust.", ["Oil is easier to compress.", "Water is too expensive.", "Oil is lighter than air."], "Oil suits the job."),
        ("What is one risk of hydraulic systems for the environment?", "Leaking fluid can pollute soil and water.", ["They make the air cleaner.", "They remove pollution.", "They have no risks."], "Biodegradable fluids reduce harm."),
        ("Why does a sealed bag of chips puff up at a high altitude?", "The air pressure outside is lower, so the air inside pushes the bag out.", ["The chips grow.", "The bag gets colder.", "Gravity pulls the bag up."], "Gases expand when outside pressure drops."),
]


def s_fluids(X):
    pool = X.pool(DENS_ROWS)
    fs, dc = X.f(float_sink), X.f(dens_calc)
    return [
        ("Fluids and viscosity", [(pool, 12), (X.gen(UK7P, "g_state", n=4), 4), (X.gen(UK7P, "g_change", n=4), 4)]),
        ("Density", [(dc, 7), (X.gen(UK7P, "g_dens", n=6), 6), (fs, 4), (pool, 3)]),
        ("Floating, sinking and buoyancy", [(fs, 8), (X.gen(UK9P, "g_float"), 5), (pool, 5), (dc, 2)]),
        ("Viscosity in daily life", [(pool, 8), (X.gen(UK7P, "g_mp", n=4), 4), (fs, 4), (dc, 4)]),
        ("Density investigations", [(dc, 5), (fs, 5), (X.gen(UK7P, "g_dens", n=4), 4), (X.B(UK7P, "B5"), 3), (pool, 3)]),
    ]


def s_pressure(X):
    pool = X.pool(PRES_ROWS)
    pc = X.f(pressure_calc)
    return [
        ("What is pressure?", [(pc, 6), (pool, 6), (X.gen(SG2P, "g_p", n=5), 5), (X.gen(SG2P, "g_kind", n=3), 3)]),
        ("Pressure and depth", [(X.gen(UK9P, "g_depth"), 4), (X.gen(UK9P, "g_calc", n=6), 6), (pool, 5), (pc, 5)]),
        ("Hydraulics and pneumatics", [(pool, 10), (X.gen(UK9P, "g_gas"), 5), (pc, 5)]),
        ("Pressure in daily life", [(X.gen(UK9P, "g_ex"), 6), (pool, 6), (X.gen(SG2P, "g_eff"), 5), (X.gen(SG2P, "g_cmp"), 3)]),
        ("Fluid technology and society", [(pool, 6), (X.B(UK9P, "B5"), 5), (X.B(SG2P, "B5"), 4), (X.B(SG2P, "B1"), 3), (pc, 2)]),
    ]


def ma_calc(R):
    def f():
        k = R.choice(["ma", "eff", "work"])
        if k == "ma":
            e = R.choice([10, 20, 25, 40, 50, 100])
            m = R.choice([2, 3, 4, 5, 8])
            load = e * m
            return tq("A lever lifts a load of %d N with an effort of %d N. What is its mechanical advantage?" % (load, e), str(m),
                      [str(load - e), str(load * e), "%s" % num(e / load)], "Mechanical advantage = load ÷ effort = %d ÷ %d = %d." % (load, e, m))
        if k == "eff":
            wi = R.choice([100, 200, 400, 500, 800, 1000])
            pc = R.choice([20, 25, 40, 50, 60, 75, 80, 90])
            wo = wi * pc // 100
            ws = sorted({100 - pc, wi - wo, min(99, pc + 10)} - {pc})
            if len(ws) < 3:
                return None
            return tq("A machine uses %d J of energy (work in) and does %d J of useful work (work out). What is its efficiency?" % (wi, wo), "%d%%" % pc,
                      ["%d%%" % x if x < 100 else "%d J" % x for x in ws],
                      "Efficiency = work out ÷ work in × 100%% = %d ÷ %d × 100%% = %d%%." % (wo, wi, pc))
        F = R.choice([10, 20, 30, 40, 50, 60, 80, 100, 150])
        d = R.choice([2, 3, 4, 5, 10])
        return tq("A student pushes a box with a force of %d N for %d m. How much work is done?" % (F, d), "%d J" % (F * d),
                  ["%d J" % (F + d), "%s J" % num(F / d), "%d J" % (F * d * 10)], "Work = force × distance = %d N × %d m = %d J." % (F, d, F * d))

    def g():
        try:
            return f()
        except TypeError:
            return None
    return g


def s_systems(X):
    pool = X.pool([
        ("What is a system?", "a group of parts that work together to do a job", ["one single part", "a kind of energy", "a raw material"], "A bicycle is a mechanical system."),
        ("What is the input of a system?", "what goes into the system, like energy or effort", ["what comes out", "the waste only", "the finished product"], "Pedalling is the input to a bike."),
        ("What is the output of a system?", "the result the system produces", ["the energy put in", "the frame of the system", "the instructions"], "Forward motion is the output of a bike."),
        ("What is a subsystem?", "a smaller system that is part of a larger system", ["a system under the ground", "a broken system", "a system with no parts"], "The brakes are a subsystem of a car."),
        ("What is mechanical advantage?", "how many times a machine multiplies the input force", ["the speed of a machine", "the cost of a machine", "the colour of a machine"], "MA = load ÷ effort."),
        ("What is efficiency?", "the percentage of input energy that becomes useful output", ["how fast a machine works", "how big a machine is", "how old a machine is"], "No machine is 100% efficient."),
        ("Why can no machine be 100% efficient?", "Some energy is always lost, mostly as heat from friction.", ["Machines create energy.", "Energy disappears.", "Machines are too small."], "Lubrication reduces friction."),
        ("How can the efficiency of a bike be improved?", "oil the chain and pump up the tires", ["add sand to the gears", "let the tires go flat", "add weight to the frame"], "Less friction, more useful output."),
        ("In science, when is work done?", "when a force moves an object through a distance", ["whenever you think hard", "when you push a wall that does not move", "when an object stays still"], "Work = force × distance."),
        ("What is the unit of work and energy?", "the joule (J)", ["the newton (N)", "the metre (m)", "the watt (W)"], "1 J = 1 N × 1 m."),
        ("Which is an example of a social system?", "a school transit system", ["a pulley", "a lever", "a gear"], "Social systems are groups of people and things working together."),
        ("How has automation changed factories?", "Robots do repetitive jobs, raising output but changing the jobs people do.", ["It removed all machines.", "It made products slower to make.", "It has had no effect."], "Systems affect society."),
        ("What is feedback in a system?", "information from the output that is used to adjust the system", ["the noise a machine makes", "the input energy", "the waste product"], "A thermostat uses feedback."),
        ("A furnace system has a thermostat. What does the thermostat do?", "It senses the temperature and switches the furnace on or off.", ["It heats the air directly.", "It filters the water.", "It makes electricity."], "It controls the system with feedback."),
        ("Why do ramps make it easier to move a wheelchair up a step?", "A longer slope means less force is needed (but over a longer distance).", ["Ramps reduce the weight.", "Ramps use magnets.", "Ramps add friction only."], "Inclined planes trade distance for force."),
        ("Which simple machine is a wedge?", "an axe blade", ["a doorknob", "a flagpole pulley", "a seesaw"], "A wedge splits things apart."),
        ("Which simple machine is a screw?", "a jar lid", ["a ramp", "a seesaw", "a pulley"], "A screw is an inclined plane wrapped around a cylinder."),
        ("Which is an environmental cost of a transportation system?", "air pollution and greenhouse gases from vehicles", ["more trees growing", "cleaner rivers", "less noise"], "Public transit can reduce the cost."),
        ("Why might a city choose a light rail system?", "It moves many people with less traffic and pollution.", ["It needs no energy.", "It is free to build.", "It carries only freight."], "Systems are judged by many criteria."),
        ("What happens to the output of a system if one subsystem fails?", "The whole system may stop working or work poorly.", ["Nothing changes.", "The system works better.", "The system makes more energy."], "Subsystems depend on each other."),
    ])
    mc = X.f(ma_calc)
    return [
        ("What is a system?", [(pool, 12), (X.gen(UK5M, "g_mech", n=4), 4), (X.gen(SG2W, "g_conv", n=4), 4)]),
        ("Work and energy", [(mc, 6), (X.gen(UK9W, "g_work", n=5), 5), (X.gen(SG2W, "g_cons"), 5), (pool, 4)]),
        ("Mechanical advantage", [(mc, 8), (X.gen(UK9W, "g_moment", n=5), 5), (X.gen(UK9W, "g_bal", n=4), 4), (pool, 3)]),
        ("Efficiency", [(mc, 8), (pool, 6), (X.gen(SG2W, "g_form", n=3), 3), (X.gen(SG2W, "g_src"), 3)]),
        ("Systems and society", [(pool, 8), (X.B(UK9W, "B5"), 4), (X.B(SG2W, "B5"), 4), (mc, 4)]),
    ]


def s_water(X):
    pool = X.pool([
        ("About how much of Earth's water is fresh water?", "about 3%", ["about 50%", "about 97%", "about 75%"], "Most water is salty ocean water."),
        ("Where is most of Earth's fresh water?", "frozen in glaciers and ice caps", ["in lakes", "in rivers", "in the air"], "Only a tiny part is in lakes and rivers."),
        ("What is a watershed?", "an area of land that drains into a river, lake or other body of water", ["a shed for storing water", "a kind of dam", "a cloud"], "Every place on land is in a watershed."),
        ("What is groundwater?", "water stored underground in soil and rock", ["water in clouds", "ocean water", "water in a bathtub"], "Wells bring up groundwater."),
        ("What is an aquifer?", "a layer of rock or soil that holds groundwater", ["a water pipe", "a fish tank", "a waterfall"], "Many Ontario towns get water from aquifers."),
        ("The Great Lakes hold about what fraction of the world's surface fresh water?", "about one fifth (20%)", ["about one half", "about 1%", "almost all of it"], "Ontario borders four of the five Great Lakes."),
        ("What drives the water cycle?", "energy from the Sun and gravity", ["the Moon only", "wind only", "people"], "The Sun evaporates water; gravity brings rain down."),
        ("What is transpiration?", "water vapour released from plant leaves", ["rain falling", "snow melting", "water soaking into soil"], "Plants add water to the air."),
        ("What is runoff?", "water that flows over the land into streams and lakes", ["water that evaporates", "water stored in glaciers", "water in clouds"], "Runoff can carry pollution."),
        ("How do glaciers affect sea level?", "When they melt, sea level rises.", ["Melting lowers sea level.", "They have no effect.", "They make the oceans saltier only."], "Melting land ice adds water to the oceans."),
        ("Why does the ocean affect climate near coasts?", "Water heats and cools slowly, so coastal places have milder temperatures.", ["The ocean is always hot.", "The ocean blocks sunlight.", "The ocean has no effect."], "Lake effect snow also comes from the Great Lakes."),
        ("What causes lake-effect snow near the Great Lakes?", "Cold air picks up moisture from the warmer lake water and drops it as snow.", ["Snow rises from the lake.", "The lakes are frozen in summer.", "Wind blows snow from the Arctic only."], "Areas like Barrie and London get lots of it."),
    ])
    return [
        ("Water on Earth", [(pool, 5), (X.gen(US5W, "g_model", n=6), 6), (X.gen(US5W, "g_compare", n=5), 5), (X.gen(US5W, "g_fresh_model", n=4), 4)]),
        ("The water cycle", [(X.gen(US6W, "g_label", n=6), 6), (X.gen(US6W, "g_proc"), 6), (X.gen(UK4W, "g_name"), 4), (X.gen(US6W, "g_every"), 4)]),
        ("Water cycle processes", [(X.gen(UK4W, "g_next"), 5), (X.gen(UK4W, "g_eve"), 5), (X.gen(SG5W, "g_stage"), 5), (X.gen(AU4W, "g_sc"), 3), (pool, 2)]),
        ("Watersheds and groundwater", [(pool, 6), (X.gen(USEW, "g_poro"), 5), (X.gen(USEW, "g_perm"), 3), (X.gen(USEW, "g_prop", n=4), 4), (X.gen(USEW, "g_stream"), 2)]),
        ("Water and climate", [(X.gen(US6W, "g_drive"), 5), (X.gen(USEW, "g_expand", n=4), 4), (X.B(US6W, "B5"), 4), (X.B(US5W, "B5"), 4), (pool, 3)]),
    ]


def s_wquality(X):
    pool = X.pool([
        ("Which is a source of water pollution?", "fertilizer and manure washing off farm fields", ["planting trees by rivers", "protecting wetlands", "using less road salt"], "Runoff carries nutrients and chemicals."),
        ("What is a point source of pollution?", "pollution from one clear place, like a factory pipe", ["pollution from a whole city's roads", "rain falling on a forest", "a natural spring"], "Non-point sources come from many places."),
        ("What is non-point source pollution?", "pollution from many spread-out places, like lawns and roads", ["pollution from one pipe", "clean rainwater", "a waterfall"], "It is harder to control."),
        ("Why should you never pour paint or oil down a storm drain?", "Storm drains usually flow straight to rivers and lakes without treatment.", ["Storm drains clean everything.", "It makes the drain work better.", "It turns into water."], "Many drains are marked 'Drains to the lake.'"),
        ("What happened in Walkerton, Ontario, in 2000?", "E. coli bacteria got into the town's drinking water and many people became sick.", ["A dam broke.", "A new lake formed.", "A drought dried up all wells."], "It led to stronger water safety laws in Ontario."),
        ("Why do many First Nations communities in Canada have boil-water advisories?", "Their water systems do not always provide safe drinking water.", ["They prefer warm water.", "Their water is too cold.", "Boiling makes water taste better."], "Safe water is a human right that Canada is working to provide."),
        ("What does a water treatment plant do?", "removes particles and germs to make water safe to drink", ["adds pollution", "makes water salty", "freezes water for storage"], "Steps include filtering and disinfecting."),
        ("What does a wastewater treatment plant do?", "cleans used water from homes before it returns to lakes and rivers", ["makes drinking water from the ocean", "stores rainwater", "makes ice"], "Sewage must be treated."),
        ("Which indicator suggests a stream is healthy?", "many mayfly and stonefly larvae living in it", ["lots of foam and a bad smell", "no living things", "thick green algae everywhere"], "Some insects need clean water."),
        ("Which action conserves water at home?", "fixing leaky taps and taking shorter showers", ["watering the lawn at noon", "running the tap while brushing teeth", "washing a car with a running hose"], "Small changes save a lot of water."),
        ("Why do Indigenous water walkers walk around the Great Lakes?", "to honour water as sacred and raise awareness about protecting it", ["to measure the lakes' depth", "to race each other", "to collect fish"], "Josephine Mandamin led many water walks."),
        ("How does climate change affect Ontario's water systems?", "It changes rain and snow patterns, causing more floods and droughts and warmer lakes.", ["It has no effect on water.", "It makes all lakes freeze longer.", "It removes all pollution."], "Warmer lakes can grow more harmful algae."),
        ("What is a harmful algal bloom?", "a fast growth of algae that can make water unsafe and lower oxygen", ["a flower show by a lake", "a type of fish", "a kind of ice"], "Lake Erie has had large blooms."),
        ("What is one way to reduce farm runoff?", "leave strips of plants (buffers) along streams", ["plough right up to the stream", "add more fertilizer", "remove all trees by the stream"], "Plants trap soil and nutrients."),
        ("Why are wetlands important to water systems?", "They filter pollutants, store floodwater and recharge groundwater.", ["They make water dirtier.", "They have no role.", "They only make mosquitoes."], "Protecting wetlands protects water."),
        ("Which household product is safest for the water system?", "a biodegradable, phosphate-free soap", ["a drain cleaner poured down the sink every day", "old medicine flushed down the toilet", "motor oil poured on the driveway"], "Choose products that break down safely."),
        ("Why should old medicines be returned to a pharmacy instead of flushed?", "Treatment plants cannot remove all medicines, so they end up in lakes.", ["Medicines clean the water.", "Flushing is safer.", "Pharmacies sell them again."], "Take-back programs protect water."),
        ("How does road salt affect water systems?", "It washes into streams and groundwater and can harm plants and animals.", ["It makes water cleaner.", "It evaporates completely.", "It only stays on the road."], "Use only as much salt as needed."),
        ("What does pH measure in water?", "how acidic or basic the water is", ["how deep the water is", "how cold the water is", "how fast the water flows"], "Most aquatic life needs a pH near 7."),
        ("Which test result suggests water has a lot of pollution from fertilizer?", "high levels of nitrates and phosphates", ["a pH of 7", "clear water with many mayflies", "cold, fast-flowing water"], "Nutrients feed algae blooms."),
        ("Why does warm water hold less life in a lake?", "Warm water holds less dissolved oxygen.", ["Warm water has more oxygen.", "Fish prefer hot water.", "Temperature does not matter."], "Thermal pollution lowers oxygen."),
        ("What is a rain garden?", "a planted dip that soaks up runoff from roofs and driveways", ["a garden that only grows in rain", "a greenhouse", "a water tower"], "Rain gardens reduce flooding and pollution."),
        ("How do permeable pavers help water systems?", "They let rainwater soak into the ground instead of running off.", ["They block all water.", "They heat the water.", "They add salt to the water."], "More infiltration recharges groundwater."),
        ("Which uses the most water in a typical Canadian home?", "toilets, showers and baths", ["drinking water", "watering one houseplant", "making ice cubes"], "Low-flow fixtures save water."),
        ("What is a low-flow showerhead?", "a showerhead that uses less water per minute", ["a showerhead with no water", "a hot-water tank", "a water filter"], "It saves water and the energy to heat it."),
        ("Why is it best to water lawns in the early morning?", "Less water evaporates before it soaks in.", ["Grass sleeps at noon.", "Water is cleaner in the morning.", "It is the law everywhere."], "Smart watering conserves water."),
        ("What is a conservation authority in Ontario?", "an agency that manages and protects a watershed", ["a police force", "a bottled water company", "a weather station"], "Ontario has 36 conservation authorities."),
        ("Why do some industries reuse cooling water?", "to save water and reduce thermal pollution", ["to make water hotter for rivers", "to waste more water", "to add chemicals to lakes"], "Recycling water saves resources."),
        ("What is desalination?", "removing salt from seawater to make fresh water", ["adding salt to water", "freezing lakes", "making rain"], "It uses a lot of energy."),
    ])
    return [
        ("Water pollution", [(pool, 8), (X.gen(SG6M, "g_pol", n=6), 6), (X.gen(US7H, "g_impact", n=3), 3), (X.B(USEW, "B1"), 3)]),
        ("Safe drinking water", [(pool, 10), (X.B(UK4W, "B1"), 4), (X.B(AU4W, "POOL1"), 3), (X.gen(SG6M, "g_cause", n=3), 3)]),
        ("Conserving water", [(X.gen(SG5W, "g_save", n=6), 6), (pool, 6), (X.gen(UK4W, "g_dry"), 4), (X.gen(UK4W, "g_dish", n=4), 4)]),
        ("Water and the environment", [(pool, 8), (X.gen(USEW, "g_wth"), 4), (X.B(SG5W, "B2"), 4), (X.B(SG5W, "B3"), 4)]),
        ("Water investigations", [(X.B(UK4W, "B5"), 5), (X.B(SG5W, "B5"), 5), (X.B(USEW, "B5"), 4), (pool, 4), (X.B(AU4W, "POOL5"), 2)]),
    ]


def UNITS():
    return [
        CU("B", 1, "cells-and-cell-theory", "B2.1, B2.2, B2.3",
           "Describe the cell theory; identify the organelles of plant and animal cells and their functions; use a microscope to "
           "observe cells and calculate magnification.",
           "Cells and the Cell Theory", "Cells and the cell theory",
           "Free Grade 8 science worksheets on the cell theory, organelles, plant and animal cells, and microscopes. "
           "100 questions with answers.",
           "All living things are made of cells.", "The nucleus controls the cell; the membrane controls what goes in and out; plant cells also have walls and chloroplasts.",
           L("The cell theory: all living things are made of cells, cells are the basic unit of life, and cells come from other cells.",
             "Animal and plant cells: nucleus, cell membrane, cytoplasm, mitochondria, vacuoles.",
             "Plant cells also have a cell wall, chloroplasts and one large vacuole.",
             "Total magnification = eyepiece × objective (10× × 40× = 400×)."),
           [("A microscope has a 10× eyepiece and a 4× objective. What is the magnification?", ["10 × 4 = 40"], "40×"),
            ("Which organelle makes food in plants?", ["it contains chlorophyll"], "the chloroplast")],
           ["Thinking only animals are made of cells.", "Mixing up the cell wall and the cell membrane.", "Adding the two magnifications instead of multiplying."],
           [("What is the cell theory?", "All living things are made of one or more cells, the cell is the basic unit of life, and all cells come from existing cells."),
            ("What is the difference between plant and animal cells?", "Plant cells have a cell wall, chloroplasts and a large vacuole. Animal cells do not."),
            ("How do you calculate magnification?", "Multiply the eyepiece power by the objective lens power.")],
           s_cells),
        CU("B", 2, "cell-processes-and-organization", "B2.4, B2.5, B2.6, B1.1",
           "Explain diffusion and osmosis across the cell membrane; describe specialized cells and how cells form tissues, organs "
           "and organ systems; assess how cell research has contributed to health and medicine.",
           "Cell Processes and Organization", "Cell processes",
           "Free Grade 8 science worksheets on diffusion, osmosis, specialized cells, tissues and organs, and cells and health. "
           "100 questions with answers.",
           "Particles move from high to low concentration.", "Osmosis moves water across membranes; specialized cells form tissues, organs and systems.",
           L("Diffusion: particles move from where there are many to where there are few.",
             "Osmosis: water diffuses across a selectively permeable membrane.",
             "Specialized cells have shapes that fit their jobs (nerve, red blood, root hair cells).",
             "Cells → tissues → organs → organ systems → organism."),
           [("A potato slice is put in salty water. What happens?", ["water moves to the saltier side"], "it loses water and goes limp"),
            ("Why do root hair cells have long extensions?", ["more surface area"], "to absorb more water")],
           ["Thinking osmosis moves salt instead of water.", "Thinking all cells look the same.", "Thinking diffusion needs energy from the cell."],
           [("What is the difference between diffusion and osmosis?", "Diffusion is the movement of any particles from high to low concentration. Osmosis is the diffusion of water across a membrane."),
            ("What is a specialized cell?", "A cell with a special shape or parts for its job, like a long nerve cell or a red blood cell with no nucleus."),
            ("Why is cell research important?", "It has led to vaccines, cancer treatments and stem-cell therapies. Stem cells were discovered by Canadian scientists in Toronto.")],
           s_cellproc),
        CU("C", 3, "fluids-density-and-buoyancy", "C2.1, C2.2, C2.3, C2.4",
           "Describe the properties of fluids, including viscosity and density; calculate density; explain buoyancy and why "
           "objects float or sink, using the particle theory.",
           "Fluids, Density and Buoyancy", "Fluids, density and buoyancy",
           "Free Grade 8 science worksheets on fluids, viscosity, density calculations, floating and sinking, and buoyancy. "
           "100 questions with answers.",
           "Density = mass ÷ volume.", "Objects float in fluids that are denser than they are; viscosity is resistance to flow.",
           L("A fluid is anything that flows: liquids and gases.",
             "Viscosity is a fluid's resistance to flow (honey is viscous); warming usually lowers viscosity.",
             "Density = mass ÷ volume. Water is 1 g/cm³ (1 g/mL).",
             "An object floats if it is less dense than the fluid. Buoyant force pushes up."),
           [("A block has a mass of 60 g and a volume of 100 cm³. Will it float in water?", ["60 ÷ 100 = 0.6 g/cm³", "0.6 < 1"], "yes, it floats"),
            ("Oil and water are poured in a glass. Which is on top?", ["oil is less dense"], "oil")],
           ["Mixing up viscosity and density.", "Thinking heavy objects always sink (density matters, not weight).", "Dividing volume by mass instead of mass by volume."],
           [("What is the difference between viscosity and density?", "Viscosity is how easily a fluid flows. Density is how much mass is packed into a volume."),
            ("Why does a steel ship float?", "Its hollow shape holds lots of air, so the ship's overall density is less than water."),
            ("How do you calculate density?", "Divide the mass by the volume. For example, 50 g ÷ 25 cm³ = 2 g/cm³.")],
           s_fluids),
        CU("C", 4, "fluid-pressure-and-technology", "C2.5, C2.6, C1.1, C1.2",
           "Describe pressure in fluids and how it changes with depth; explain how hydraulic and pneumatic systems use fluids under "
           "pressure; assess the environmental and social effects of fluid technologies.",
           "Fluid Pressure, Hydraulics and Pneumatics", "Fluid pressure and technology",
           "Free Grade 8 science worksheets on pressure, Pascal's law, hydraulics, pneumatics, submarines and fluid technology. "
           "100 questions with answers.",
           "Pressure = force ÷ area.", "Fluids pass pressure in all directions; hydraulics use liquids and pneumatics use gases.",
           L("Pressure is force on an area: pressure = force ÷ area, in pascals (Pa).",
             "Pressure in a fluid increases with depth.",
             "Pascal's law: pressure on a confined fluid is passed equally in all directions.",
             "Hydraulic systems (brakes, excavators) use liquids; pneumatic systems (air brakes, nail guns) use compressed air."),
           [("A 200 N force acts on 4 m². What is the pressure?", ["200 ÷ 4"], "50 Pa"),
            ("Why are dams thicker at the bottom?", ["pressure increases with depth"], "to hold back the greater pressure")],
           ["Thinking pressure is the same as force.", "Thinking liquids are easy to compress.", "Thinking fluid pressure only pushes down."],
           [("What is the difference between hydraulics and pneumatics?", "Hydraulic systems use liquids such as oil. Pneumatic systems use gases such as air."),
            ("Why does a sharp knife cut better?", "The force acts on a smaller area, so the pressure is greater."),
            ("Why do your ears pop?", "The air pressure outside changes quickly, and the pressure inside your ear adjusts.")],
           s_pressure),
        CU("D", 5, "systems-and-mechanical-advantage", "D2.1, D2.2, D2.3, D2.4",
           "Describe systems in terms of inputs, outputs, components and subsystems; calculate work, mechanical advantage and "
           "efficiency; explain how friction and design affect a system's efficiency.",
           "Systems, Work and Mechanical Advantage", "Systems in action",
           "Free Grade 8 science worksheets on systems, inputs and outputs, work, mechanical advantage, efficiency and simple "
           "machines. 100 questions with answers.",
           "Systems turn inputs into outputs.", "Work = force × distance; MA = load ÷ effort; efficiency = output ÷ input × 100%.",
           L("A system is a set of parts working together. It has inputs, outputs and often subsystems.",
             "Work = force × distance, measured in joules (J).",
             "Mechanical advantage = load ÷ effort. A ramp, lever or pulley can give MA greater than 1.",
             "Efficiency = useful work out ÷ work in × 100%. Friction lowers efficiency."),
           [("A lever lifts 300 N with 50 N of effort. What is the MA?", ["300 ÷ 50"], "6"),
            ("A motor uses 500 J and does 400 J of useful work. Efficiency?", ["400 ÷ 500 × 100%"], "80%")],
           ["Thinking machines reduce the work needed (they reduce the force, not the work).", "Thinking a machine can be more than 100% efficient.", "Calling it work when nothing moves."],
           [("What is mechanical advantage?", "The number of times a machine multiplies your effort force: load ÷ effort."),
            ("Why is no machine 100% efficient?", "Some input energy is always lost, mainly as heat from friction and as sound."),
            ("What are examples of systems?", "A bicycle, a furnace with a thermostat, a school, the TTC transit system and the human body.")],
           s_systems),
        CU("E", 6, "water-on-earth-and-the-water-cycle", "E2.1, E2.2, E2.3, E2.4",
           "Describe the distribution of water on Earth; explain the water cycle and the factors that drive it; describe watersheds, "
           "groundwater and how water systems affect climate.",
           "Water on Earth and the Water Cycle", "Water on Earth and the water cycle",
           "Free Grade 8 science worksheets on fresh and salt water, the water cycle, watersheds, groundwater, the Great Lakes and "
           "water and climate. 100 questions with answers.",
           "Only about 3% of Earth's water is fresh.", "The Sun and gravity drive the water cycle; every place on land is in a watershed.",
           L("About 97% of Earth's water is salt water; most fresh water is frozen in ice or underground.",
             "The water cycle: evaporation, transpiration, condensation, precipitation, runoff and infiltration.",
             "A watershed is all the land that drains into one body of water.",
             "Large bodies of water like the Great Lakes moderate climate and cause lake-effect snow."),
           [("What drives evaporation?", ["energy from the Sun"], "solar energy"),
            ("Where is most fresh water?", ["glaciers and ice caps"], "frozen in ice")],
           ["Thinking most of Earth's water is fresh.", "Thinking groundwater is an underground lake.", "Thinking a watershed is a building."],
           [("What is a watershed?", "All the land that drains into one river, lake or ocean. Ontario has many watersheds that flow to the Great Lakes, Hudson Bay or the St. Lawrence."),
            ("Why are the Great Lakes important?", "They hold about one fifth of the world's surface fresh water and supply drinking water to millions of people."),
            ("What drives the water cycle?", "Energy from the Sun evaporates water, and gravity pulls precipitation and runoff back down.")],
           s_water),
        CU("E", 7, "water-quality-and-conservation", "E1.1, E1.2, E2.5",
           "Assess the effects of human activities on the quality and quantity of water; describe how water is treated and how "
           "communities, including First Nations, work to protect water; evaluate ways to conserve water.",
           "Water Quality and Conservation", "Water quality and conservation",
           "Free Grade 8 science worksheets on water pollution, drinking water treatment, Walkerton, boil-water advisories, water "
           "walks and conserving water. 100 questions with answers.",
           "Clean water must be protected.", "Runoff and waste pollute water; treatment, wetlands and conservation keep it safe.",
           L("Human activities affect the quality and amount of water.",
             "Point sources (a pipe) and non-point sources (lawns, roads, farms) pollute water.",
             "Water treatment plants make water safe to drink; wastewater plants clean used water.",
             "Conserve water: fix leaks, take shorter showers, plant native gardens, use less salt and fertilizer."),
           [("What kind of source is runoff from many farms?", ["spread over a large area"], "non-point source"),
            ("Why do mayfly larvae show a healthy stream?", ["they need clean, oxygen-rich water"], "they are indicator species")],
           ["Thinking water is unlimited because it falls as rain.", "Thinking storm drains go to treatment plants.", "Thinking clear water is always safe to drink."],
           [("How is drinking water made safe?", "It is settled, filtered and disinfected (usually with chlorine) at a treatment plant, and tested often."),
            ("Why are there boil-water advisories in some First Nations communities?", "Some communities do not have reliable water treatment, so water must be boiled to be safe. Governments and communities are working to fix this."),
            ("How can students conserve water?", "Turn off the tap while brushing, take shorter showers, report leaks and keep pollution out of storm drains.")],
           s_wquality),
    ]
