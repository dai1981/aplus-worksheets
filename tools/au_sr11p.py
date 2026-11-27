# -*- coding: utf-8 -*-
"""Year 11 Physics (Australian Curriculum: Senior Secondary Physics, Units 1 and 2) for au_sr.build."""
from au_sr import SR, nq

PH = "Physics"
TH = "thermal-physics-and-ideal-gases"

HEAT = [
    ("What is temperature a measure of?", "the average kinetic energy of the particles", ["the total energy of the particles", "the amount of heat in an object", "the potential energy of the particles"], "Internal energy is the total kinetic and potential energy."),
    ("What is heat?", "energy transferred because of a temperature difference", ["the temperature of a hot object", "the total energy in an object", "a type of particle"], "Heat flows from hot to cold."),
    ("When are two objects in thermal equilibrium?", "when they are at the same temperature, so there is no net heat flow", ["when they have the same internal energy", "when they have the same mass", "when both are hot"], "This is the basis of the zeroth law."),
    ("What is internal energy?", "the total kinetic and potential energy of all the particles", ["the temperature in kelvin", "only the kinetic energy of the particles", "the energy needed to melt a substance"], "Melting increases potential energy at constant temperature."),
    ("Why does the temperature stay constant while ice is melting?", "the energy supplied breaks bonds (increases potential energy) rather than speeding up particles", ["no energy is being supplied", "the ice loses energy", "the thermometer stops working"], "This energy is the latent heat of fusion."),
    ("How is heat transferred through a metal spoon in hot soup?", "conduction: vibrating particles and free electrons pass on energy", ["convection currents in the metal", "radiation only", "evaporation"], "Metals conduct well because of free electrons."),
    ("How does heat spread through the air in a room from a heater?", "convection: warm air rises and cooler air sinks", ["conduction only", "radiation only", "evaporation"], "Fluids carry energy as they move."),
    ("How does energy from the Sun reach Earth?", "radiation (electromagnetic waves), which needs no medium", ["conduction through space", "convection through space", "sound waves"], "Space is a vacuum."),
    ("Why is a dull black surface best for a solar hot water panel?", "it is a good absorber of radiation", ["it reflects most radiation", "it is a good insulator", "it stops convection"], "Shiny surfaces reflect radiation."),
    ("Why do houses in hot Australian climates often have light-coloured roofs?", "light colours reflect more solar radiation, keeping the house cooler", ["light colours absorb more radiation", "dark roofs cost more", "light colours conduct heat into the house"], "Reflective roofs cut cooling costs."),
    ("Why does a wetsuit keep a surfer warm?", "it traps a thin layer of water that is warmed and stops heat being carried away", ["it heats the water", "it is a good conductor", "it reflects all radiation"], "Neoprene is also a poor conductor."),
    ("What is the first law of thermodynamics?", "the change in internal energy equals heat added minus work done by the system (ΔU = Q − W)", ["energy is lost in every change", "heat always flows from cold to hot", "temperature can never reach absolute zero"], "It is conservation of energy."),
    ("A gas is given 500 J of heat and does 200 J of work. What is the change in its internal energy?", "+300 J", ["+700 J", "−300 J", "+200 J"], "ΔU = Q − W = 500 − 200."),
    ("Why do coastal cities such as Perth have milder temperatures than inland towns?", "water has a high specific heat capacity, so the ocean warms and cools slowly", ["the sea is always hot", "water has a low specific heat capacity", "land cannot absorb heat"], "The sea moderates the nearby climate."),
    ("What is absolute zero?", "0 K (−273 °C), the lowest possible temperature", ["0 °C", "the temperature of space between galaxies", "the freezing point of water"], "Particles have minimum kinetic energy."),
    ("Which change of state releases energy to the surroundings?", "condensation", ["evaporation", "melting", "boiling"], "Steam burns are severe because of this."),
    ("Why does sweating cool you down?", "the fastest water molecules evaporate, carrying energy away from the skin", ["sweat is colder than the body", "sweat reflects heat", "sweating stops convection"], "Evaporation needs latent heat."),
    ("Convert 27 °C to kelvin.", "300 K", ["246 K", "27 K", "−246 K"], "T(K) = T(°C) + 273."),
]
NUC = [
    ("What is an alpha particle?", "a helium-4 nucleus: 2 protons and 2 neutrons", ["a fast electron", "a high-energy photon", "a single neutron"], "It has charge +2."),
    ("What is a beta-minus particle?", "a fast electron emitted when a neutron changes into a proton", ["a helium nucleus", "a photon", "a proton"], "The proton number goes up by 1."),
    ("What is gamma radiation?", "high-energy electromagnetic radiation from the nucleus", ["a stream of electrons", "a helium nucleus", "a stream of neutrons"], "It has no charge and no mass."),
    ("Which radiation is stopped by a sheet of paper?", "alpha", ["beta", "gamma", "X-rays"], "Alpha is the most ionising and least penetrating."),
    ("Which radiation needs several centimetres of lead to reduce it greatly?", "gamma", ["alpha", "beta", "infrared"], "Gamma is the most penetrating."),
    ("Which radiation is the most strongly ionising?", "alpha", ["gamma", "beta", "radio waves"], "Its large charge and mass cause many ionisations."),
    ("Why is alpha radiation most dangerous inside the body?", "it is very ionising and all its energy is absorbed by nearby cells", ["it passes straight through the body", "it cannot ionise", "it is stopped by skin outside the body, so it is safe inside"], "Outside the body skin stops it."),
    ("What is the half-life of a radioactive isotope?", "the time for half the nuclei in a sample to decay", ["half the time for all the nuclei to decay", "the time for the mass of the sample to halve because of heat", "the age of the isotope"], "It is constant for each isotope."),
    ("What is nuclear fission?", "a heavy nucleus such as uranium-235 splits into two smaller nuclei, releasing energy and neutrons", ["two light nuclei join together", "an electron leaves the atom", "a nucleus emits only gamma rays"], "Fission is used in nuclear reactors."),
    ("What is nuclear fusion?", "two light nuclei join to form a heavier nucleus, releasing energy", ["a heavy nucleus splits in two", "an atom loses electrons", "a neutron decays"], "Fusion powers the Sun."),
    ("What is a chain reaction?", "neutrons from one fission cause further fissions", ["electrons cause atoms to ionise one after another", "alpha particles join to make heavier nuclei", "a reaction that needs no fuel"], "Control rods absorb neutrons to control the rate."),
    ("Why do fission and fusion both release energy?", "the products have a higher binding energy per nucleon, so mass is converted to energy (E = mc²)", ["the products have more mass", "electrons are destroyed", "energy is created from nothing"], "The mass defect becomes energy."),
    ("What is mass defect?", "the difference between the mass of a nucleus and the total mass of its separate nucleons", ["the mass lost when an atom loses electrons", "the mass of the neutrons only", "an error in measuring mass"], "It is equivalent to the binding energy."),
    ("Which nucleus has the highest binding energy per nucleon?", "iron-56 (near the peak of the curve)", ["hydrogen-1", "uranium-235", "helium-3"], "Nuclei lighter than iron can release energy by fusion; heavier ones by fission."),
    ("Why does Australia's OPAL research reactor at Lucas Heights produce radioisotopes?", "for nuclear medicine, such as technetium-99m for medical scans", ["to generate most of the country's electricity", "to make weapons", "to power submarines"], "ANSTO supplies isotopes to hospitals."),
    ("Why is technetium-99m good for medical imaging?", "it emits gamma rays that leave the body and has a short half-life (about 6 hours)", ["it emits alpha particles", "it has a half-life of millions of years", "it is not radioactive"], "Short half-life means a low dose."),
    ("Which unit measures the activity of a radioactive source?", "becquerel (Bq), one decay per second", ["sievert (Sv)", "coulomb (C)", "joule (J)"], "Sieverts measure the effective dose."),
    ("Which isotope is used to date materials that were once alive, up to about 50 000 years old?", "carbon-14", ["uranium-238", "potassium-40", "iodine-131"], "Its half-life is about 5730 years."),
]
CIRC = [
    ("What is electric current?", "the rate of flow of charge, I = Q ÷ t", ["energy per unit charge", "the opposition to current", "the energy used per second"], "Measured in amperes (coulombs per second)."),
    ("What is potential difference?", "the energy transferred per unit charge, V = W ÷ q", ["the charge per second", "the resistance per metre", "the force on a charge"], "1 V = 1 J/C."),
    ("How is an ammeter connected?", "in series, and it has a very low resistance", ["in parallel, with a high resistance", "in series, with a high resistance", "across the power supply only"], "All the current must pass through it."),
    ("How is a voltmeter connected?", "in parallel across the component, and it has a very high resistance", ["in series with the component", "in parallel with a very low resistance", "in place of the component"], "It draws almost no current."),
    ("In a series circuit, what is the same through every component?", "the current", ["the potential difference", "the resistance", "the power"], "The voltages add up to the supply voltage."),
    ("In a parallel circuit, what is the same across every branch?", "the potential difference", ["the current", "the resistance", "the charge"], "The branch currents add up to the total."),
    ("Why are household appliances connected in parallel?", "each gets the full mains voltage and can be switched on or off by itself", ["to make the current the same in each", "to use less wire", "to increase the total resistance"], "Australian mains is 230 V AC."),
    ("What happens to the total resistance when another resistor is added in parallel?", "it decreases", ["it increases", "it stays the same", "it doubles"], "There are more paths for the current."),
    ("What is an ohmic conductor?", "one with a constant resistance, so I is proportional to V at constant temperature", ["one with zero resistance", "one whose resistance always falls with voltage", "a filament lamp"], "A filament lamp is non-ohmic: it gets hotter."),
    ("Why does the resistance of a filament lamp increase as the current increases?", "the filament gets hotter, so its ions vibrate more and impede the electrons", ["the filament gets longer", "the voltage falls", "the electrons slow down because of light"], "Its I–V graph is a curve."),
    ("What does a residual current device (RCD, safety switch) do?", "cuts the power quickly if current leaks to earth, for example through a person", ["increases the current", "stores charge", "measures energy use"], "RCDs are required in Australian homes."),
    ("What does a fuse or circuit breaker do?", "breaks the circuit if the current is too high", ["keeps the voltage constant", "stores energy", "converts AC to DC"], "It protects wiring from overheating."),
    ("A 2.0 kW heater runs for 3 hours. Electricity costs 30 cents per kWh. What does it cost?", "$1.80", ["$0.18", "$18.00", "$6.00"], "Energy = 2.0 × 3 = 6 kWh; 6 × 30c = 180c."),
    ("A 10 W LED globe is on for 5 hours a day for 30 days. How much energy does it use?", "1.5 kWh", ["15 kWh", "150 kWh", "0.15 kWh"], "10 W × 150 h = 1500 Wh."),
    ("Which equation gives electrical power?", "P = VI", ["P = V ÷ I", "P = IR", "P = Q ÷ V"], "Also P = I²R and P = V² ÷ R."),
]
MOT = [
    ("What is the difference between distance and displacement?", "displacement is the straight-line change in position with a direction; distance is the path length", ["they mean the same thing", "distance has a direction; displacement does not", "displacement is always larger"], "Displacement is a vector."),
    ("Which quantity is a vector?", "velocity", ["speed", "distance", "mass"], "Vectors have size and direction."),
    ("What does the gradient of a displacement–time graph give?", "velocity", ["acceleration", "displacement", "force"], "Steeper means faster."),
    ("What does the gradient of a velocity–time graph give?", "acceleration", ["displacement", "speed", "force"], "The area under it gives displacement."),
    ("What does the area under a velocity–time graph give?", "displacement", ["acceleration", "force", "velocity"], "Area = velocity × time."),
    ("What does Newton's first law state?", "an object stays at rest or moves at constant velocity unless a net force acts", ["force equals mass times acceleration", "every action has an equal and opposite reaction", "objects slow down naturally"], "This is inertia."),
    ("What does Newton's second law state?", "the net force equals mass times acceleration, F = ma", ["objects keep moving unless a force acts", "forces come in pairs", "weight equals mass"], "Acceleration is in the direction of the net force."),
    ("What does Newton's third law state?", "if A exerts a force on B, B exerts an equal and opposite force on A", ["F = ma", "an object at rest stays at rest", "momentum is always lost in collisions"], "The pair act on different objects."),
    ("A car brakes and a passenger without a seatbelt moves forwards. Why?", "the passenger's inertia keeps them moving forwards", ["a force pushes them forwards", "the seat pushes them", "gravity increases"], "Seatbelts provide the force to slow the passenger."),
    ("Why do airbags reduce injuries in a crash?", "they increase the time for the person to stop, so the force is smaller", ["they reduce the person's mass", "they increase the change in momentum", "they stop the car"], "Impulse: FΔt = Δp."),
    ("What is the weight of a 60 kg student on Earth? (g = 9.8 m/s²)", "588 N", ["60 N", "6.1 N", "588 kg"], "W = mg."),
    ("What is momentum?", "mass × velocity, a vector", ["mass × acceleration", "force × time only", "half mass × velocity²"], "Unit kg m/s."),
    ("In which kind of collision is kinetic energy conserved?", "an elastic collision", ["an inelastic collision", "every collision", "a collision in which objects stick together"], "Momentum is conserved in all collisions."),
    ("What is the work done when a 50 N force moves a box 4.0 m in the direction of the force?", "200 J", ["12.5 J", "54 J", "0.08 J"], "W = Fs."),
    ("A ball is dropped. Ignoring air resistance, what is its acceleration?", "9.8 m/s² downwards", ["0 m/s²", "9.8 m/s² upwards", "it increases as it falls"], "All objects fall with the same acceleration in a vacuum."),
    ("What is terminal velocity?", "the constant speed reached when air resistance balances weight", ["the fastest speed possible", "the speed when an object hits the ground", "the speed of light"], "Net force is zero."),
]
WAVE = [
    ("What is the difference between transverse and longitudinal waves?", "in transverse waves particles vibrate at right angles to the direction of travel; in longitudinal waves they vibrate along it", ["transverse waves need no medium", "longitudinal waves are always faster", "there is no difference"], "Sound is longitudinal; waves on a string are transverse."),
    ("Which type of wave is sound in air?", "longitudinal (compressions and rarefactions)", ["transverse", "electromagnetic", "it is not a wave"], "Sound needs a medium."),
    ("What is the amplitude of a wave?", "the maximum displacement from the rest position", ["the distance between two crests", "the number of waves per second", "the speed of the wave"], "Larger amplitude = more energy."),
    ("What is the wavelength of a wave?", "the distance between two neighbouring points in phase, such as two crests", ["the height of a crest", "the time for one wave", "the number of waves per second"], "Symbol λ, unit metres."),
    ("What does a wave transfer?", "energy, without transferring matter", ["matter from one place to another", "only sound", "only light"], "The particles vibrate about fixed positions."),
    ("What is resonance?", "large-amplitude vibration when a system is driven at its natural frequency", ["the reflection of a sound", "the bending of a wave", "a decrease in amplitude"], "A singer can shatter a glass by resonance."),
    ("What is a standing (stationary) wave?", "a wave pattern made when two identical waves travelling in opposite directions superpose", ["a wave that does not vibrate", "a wave with zero frequency", "a wave in a vacuum"], "It has fixed nodes and antinodes."),
    ("What is a node in a standing wave?", "a point that does not move", ["a point of maximum vibration", "the source of the wave", "the end of the medium"], "Antinodes have maximum amplitude."),
    ("What is refraction?", "the change in direction of a wave as it changes speed when it enters a new medium", ["the bouncing of a wave off a surface", "the spreading of a wave through a gap", "the addition of two waves"], "Light bends towards the normal entering glass."),
    ("What is diffraction?", "the spreading of a wave as it passes through a gap or around an obstacle", ["the change in speed of a wave", "the bouncing back of a wave", "the loss of energy of a wave"], "It is greatest when the gap is about one wavelength."),
    ("What happens to the pitch of a sound when its frequency increases?", "the pitch gets higher", ["the pitch gets lower", "it gets louder", "it gets softer"], "Loudness depends on amplitude."),
    ("What is the speed of sound in air at room temperature?", "about 340 m/s", ["about 3 × 10⁸ m/s", "about 34 m/s", "about 1500 m/s"], "Sound is faster in water (about 1500 m/s)."),
    ("What is the law of reflection?", "the angle of incidence equals the angle of reflection", ["the angle of reflection is always 90°", "light bends towards the normal", "light speeds up after reflection"], "Angles are measured from the normal."),
    ("What does the principle of superposition state?", "when waves meet, the total displacement is the sum of the individual displacements", ["waves cancel out completely", "waves bounce off each other", "only the larger wave survives"], "This explains interference."),
    ("What is the sound intensity level unit?", "decibel (dB)", ["hertz (Hz)", "watt (W)", "newton (N)"], "An increase of 10 dB is ten times the intensity."),
]


def u12(X):
    al = __import__("al_phys")
    return [
        ("Temperature, heat and internal energy", [(X.pool(HEAT), 12), (X.ch("in_s11p", "thermodynamics", 1), 4), (X.al(al.t_heat, "Q"), 4)]),
        ("Specific heat capacity", [(X.ch("al_phys", TH, 1, 13), 16), (X.pool(HEAT), 4)]),
        ("Latent heat and changes of state", [(X.ch("al_phys", TH, 2, 13), 16), (X.pool(HEAT), 4)]),
        ("Conduction, convection and radiation", [(X.ch("in_s11p", "thermal-properties-of-matter", 4), 12), (X.pool(HEAT), 6), (X.al(al.t_heat, "mix"), 2)]),
        ("Thermal energy problems", [(X.al(al.t_heat, "dT", "mix"), 10), (X.ch("in_s11p", "thermal-properties-of-matter", 4), 6), (X.ch("al_phys", TH, 2, 13), 4)]),
    ]


def u13(X):
    return [
        ("Alpha, beta and gamma radiation", [(X.pool(NUC), 12), (X.gen("gen_us_science_chem_nuclear_chemistry", "g_change"), 8)]),
        ("Nuclear equations", [(X.ch("al_phys", "nuclear-physics", 3, 13), 14), (X.gen("gen_us_science_chem_nuclear_chemistry", "g_change"), 6)]),
        ("Half-life", [(X.ch("al_phys", "nuclear-physics", 1, 13), 14), (X.gen("gen_us_science_chem_nuclear_chemistry", "g_half"), 6)]),
        ("Fission, fusion and E = mc²", [(X.pool(NUC), 6), (X.ch("in_s12p", "nuclei", 5), 10), (X.ch("al_phys", "nuclear-physics", 4, 13), 4)]),
        ("Binding energy and nuclear energy", [(X.ch("al_phys", "nuclear-physics", 4, 13), 10), (X.ch("in_s12p", "nuclei", 3), 10)]),
    ]


def u14(X):
    return [
        ("Charge, current and potential difference", [(X.ch("al_phys", "electricity", 1, 12), 14), (X.pool(CIRC), 6)]),
        ("Resistance and Ohm's law", [(X.ch("al_phys", "electricity", 2, 12), 14), (X.pool(CIRC), 6)]),
        ("Series and parallel circuits", [(X.ch("al_phys", "electricity", 3, 12), 16), (X.pool(CIRC), 4)]),
        ("Electrical power and energy", [(X.ch("al_phys", "electricity", 4, 12), 16), (X.pool(CIRC), 4)]),
        ("Circuits with real cells", [(X.ch("al_phys", "electricity", 5, 12), 18), (X.ch("al_phys", "electricity", 3, 12), 2)]),
    ]


def u15(X):
    al = __import__("al_phys")
    return [
        ("Describing motion", [(X.ch("in_s11p", "motion-in-a-straight-line", 1), 12), (X.pool(MOT), 6), (X.gen("gen_us_science_phys_motion_and_kinematics", "g_acc"), 2)]),
        ("Equations of motion", [(X.al(al.m_suvat, drop=[r"car speeds up from [0-9]+ m/s to ([5-9][0-9]|[1-9][0-9][0-9]) m/s"]), 16), (X.pool(MOT), 4)]),
        ("Newton's laws", [(X.gen("gen_us_science_phys_newtons_laws_and_net_force", "g_net"), 6), (X.gen("gen_us_science_phys_newtons_laws_and_net_force", "g_fma"), 6), (X.pool(MOT), 6), (X.ch("in_s11p", "laws-of-motion", 1), 2)]),
        ("Momentum and impulse", [(X.ch("in_s11p", "laws-of-motion", 2), 12), (X.gen("gen_us_science_phys_momentum_and_collisions", "g_stick"), 4), (X.pool(MOT), 4)]),
        ("Work, energy and power", [(X.al(al.m_energy), 14), (X.ch("in_s11p", "work-energy-and-power", 1), 6)]),
    ]


def u16(X):
    al = __import__("al_phys")
    return [
        ("Properties of waves", [(X.pool(WAVE), 10), (X.gen("gen_us_science_phys_wave_properties", "g_medium"), 6), (X.gen("gen_us_science_phys_wave_properties", "g_period"), 4)]),
        ("The wave equation", [(X.ch("al_phys", "waves-and-optics", 1, 12), 16), (X.pool(WAVE), 4)]),
        ("Sound, resonance and standing waves", [(X.ch("in_s11p", "waves", 2), 10), (X.ch("in_s11p", "waves", 4), 6), (X.pool(WAVE), 4)]),
        ("Reflection and refraction of light", [(X.ch("al_phys", "waves-and-optics", 2, 12), 16), (X.pool(WAVE), 4)]),
        ("Superposition and interference", [(X.al(al.w_phase), 8), (X.ch("in_s11p", "waves", 3), 6), (X.al(al.w_stationary), 6)]),
    ]


def UNITS():
    return [
        SR(PH, 1, 12, "heating-processes", "Heating processes",
           "Temperature, heat and internal energy; thermal equilibrium; heat transfer by conduction, convection and radiation; specific heat capacity and latent heat; the first law of thermodynamics.",
           "Heating Processes: Specific Heat and Latent Heat", "heating processes",
           "Free Year 11 Physics worksheets on heating processes: temperature, internal energy, conduction, convection, radiation, Q = mcΔT, latent heat and the first law of thermodynamics. 100 questions with answers.",
           "Q = mcΔT changes temperature; Q = mL changes state.", "Heat flows from hot to cold until thermal equilibrium.",
           "<p><b>Temperature</b> measures the average kinetic energy of particles; <b>internal energy</b> is their total kinetic and potential energy; <b>heat</b> is energy transferred because of a temperature difference. Energy moves by conduction, convection and radiation.</p>"
           "<p>To change temperature: Q = mcΔT. To change state at constant temperature: Q = mL (L is the specific latent heat). The first law of thermodynamics is conservation of energy: ΔU = Q − W.</p>",
           [("Heat needed to warm 2.0 kg of water by 15 K (c = 4180 J kg⁻¹ K⁻¹)?", ["Q = 2.0 × 4180 × 15"], "1.25 × 10⁵ J"),
            ("Energy to melt 0.50 kg of ice (L = 3.34 × 10⁵ J/kg)?", ["Q = mL = 0.50 × 3.34 × 10⁵"], "1.67 × 10⁵ J")],
           ["Using Q = mcΔT during a change of state.", "Saying cold flows into an object: heat flows out of it.", "Forgetting to convert grams to kilograms."],
           [("Why does the temperature stay the same while water boils?", "The energy supplied is used to separate the particles (increase their potential energy), not to speed them up, so the temperature stays at 100 °C."),
            ("Why is water good for storing heat?", "It has a high specific heat capacity (4180 J kg⁻¹ K⁻¹), so it takes in a lot of energy for a small temperature rise.")],
           u12),
        SR(PH, 1, 13, "ionising-radiation-and-nuclear-reactions", "Ionising radiation and nuclear reactions",
           "The nucleus, isotopes and radioactive decay; alpha, beta and gamma radiation and their properties; nuclear equations; half-life and activity; fission, fusion, mass defect, binding energy and E = mc²; uses of radioisotopes.",
           "Ionising Radiation, Half-life and Nuclear Energy", "ionising radiation and nuclear reactions",
           "Free Year 11 Physics worksheets on nuclear physics: alpha, beta and gamma radiation, nuclear equations, half-life, fission, fusion, binding energy and E = mc². 100 questions with answers.",
           "After n half-lives, (½)ⁿ of the nuclei remain.", "E = mc²: a tiny mass gives a huge energy.",
           "<p>Unstable nuclei decay by emitting <b>alpha</b> (⁴₂He), <b>beta</b> (an electron or positron) or <b>gamma</b> radiation. In a nuclear equation the nucleon numbers and proton numbers balance on each side.</p>"
           "<p>The <b>half-life</b> is the time for half the nuclei to decay. Fission splits heavy nuclei; fusion joins light nuclei. Both release energy because the products are more tightly bound; the lost mass becomes energy, E = mc².</p>",
           [("Iodine-131 (half-life 8 days): fraction left after 24 days?", ["24 ÷ 8 = 3 half-lives", "(½)³"], "1/8"),
            ("Energy from 1.0 g of mass?", ["E = 0.001 × (3.0 × 10⁸)²"], "9.0 × 10¹³ J")],
           ["Thinking half-life means half the time for complete decay.", "Forgetting that beta-minus decay raises the proton number by 1.", "Saying gamma radiation changes the nucleon number."],
           [("Why does a nucleus emit radiation?", "Its combination of protons and neutrons is unstable; decay moves it towards a more stable arrangement."),
            ("Why can both fission and fusion release energy?", "In both, the products have a higher binding energy per nucleon than the reactants, so some mass is converted into energy.")],
           u13),
        SR(PH, 1, 14, "electrical-circuits", "Electrical circuits",
           "Charge, current and potential difference; resistance and Ohm's law; series and parallel circuits; electrical power and energy, the kilowatt-hour; e.m.f. and internal resistance; electrical safety.",
           "Electrical Circuits: Current, Resistance and Power", "electrical circuits",
           "Free Year 11 Physics worksheets on electric circuits: current, potential difference, Ohm's law, resistivity, series and parallel circuits, power, kWh and internal resistance. 100 questions with answers.",
           "V = IR and P = VI.", "Series: resistances add. Parallel: reciprocals add.",
           "<p>Current is the rate of flow of charge (I = Q ÷ t); potential difference is energy per unit charge (V = W ÷ q); resistance R = V ÷ I. In <b>series</b> the current is the same and R = R₁ + R₂; in <b>parallel</b> the voltage is the same and 1/R = 1/R₁ + 1/R₂.</p>"
           "<p>Power P = VI = I²R = V² ÷ R. Energy bills use kilowatt-hours: E (kWh) = P (kW) × t (h). A real cell has internal resistance: ε = V + Ir.</p>",
           [("Two 6 Ω resistors in parallel?", ["1/R = 1/6 + 1/6", "R = 3 Ω"], "3 Ω"),
            ("A 230 V kettle draws 8.0 A. Power?", ["P = VI = 230 × 8.0"], "1840 W")],
           ["Adding parallel resistances like series ones.", "Connecting a voltmeter in series.", "Using watts with hours without converting to kilowatts for kWh."],
           [("Why does adding a resistor in parallel lower the total resistance?", "It gives the current another path, so more current flows for the same voltage."),
            ("What is a kilowatt-hour?", "The energy used by a 1 kW appliance in 1 hour: 3.6 × 10⁶ J. Electricity bills charge per kWh.")],
           u14),
        SR(PH, 2, 15, "linear-motion-and-force", "Linear motion and force",
           "Scalars and vectors; displacement, velocity and acceleration; motion graphs; equations for uniformly accelerated motion; Newton's three laws; momentum and impulse; work, energy and power.",
           "Linear Motion, Newton's Laws and Momentum", "linear motion and force",
           "Free Year 11 Physics worksheets on linear motion: velocity, acceleration, motion graphs, the equations of motion, Newton's laws, F = ma, momentum, impulse, work and energy. 100 questions with answers.",
           "v = u + at; s = ut + ½at²; v² = u² + 2as.", "F = ma; p = mv; impulse FΔt = Δp.",
           "<p>Displacement, velocity and acceleration are vectors. On a displacement–time graph the gradient is velocity; on a velocity–time graph the gradient is acceleration and the area is displacement. For constant acceleration use the equations of motion.</p>"
           "<p>Newton's laws: no net force means constant velocity; F = ma; forces come in equal and opposite pairs. Momentum p = mv is conserved in collisions; impulse FΔt = Δp explains seatbelts and airbags. Work W = Fs; kinetic energy ½mv²; gravitational potential energy mgh.</p>",
           [("Car from 0 to 20 m/s in 8.0 s. Acceleration?", ["a = (20 − 0) ÷ 8.0"], "2.5 m/s²"),
            ("1200 kg car accelerates at 2.5 m/s². Net force?", ["F = ma = 1200 × 2.5"], "3000 N")],
           ["Mixing up distance (scalar) and displacement (vector).", "Thinking a moving object needs a net force to keep moving.", "Putting the two forces of a Newton's third law pair on the same object."],
           [("Why does a seatbelt reduce injury?", "It stretches a little, increasing the stopping time; for the same change in momentum, a longer time means a smaller force (FΔt = Δp)."),
            ("When can you use the equations of motion?", "Only when the acceleration is constant, such as free fall without air resistance.")],
           u15),
        SR(PH, 2, 16, "waves", "Waves",
           "Mechanical waves: transverse and longitudinal; amplitude, wavelength, frequency, period and v = fλ; sound, resonance and standing waves; reflection, refraction (Snell's law) and total internal reflection; diffraction, superposition and interference.",
           "Waves: Sound, Light and Interference", "waves",
           "Free Year 11 Physics worksheets on waves: transverse and longitudinal waves, v = fλ, sound, resonance, standing waves, refraction, Snell's law, total internal reflection and interference. 100 questions with answers.",
           "v = fλ and f = 1/T.", "n₁ sin θ₁ = n₂ sin θ₂.",
           "<p>A wave transfers energy without transferring matter. In <b>transverse</b> waves particles vibrate at right angles to the direction of travel; in <b>longitudinal</b> waves (sound) they vibrate along it. For all waves v = fλ and f = 1/T.</p>"
           "<p>Waves reflect, refract (change speed and direction), diffract and superpose. Two waves travelling in opposite directions make a standing wave with nodes and antinodes; driving a system at its natural frequency causes resonance. Light refracts according to Snell's law; beyond the critical angle there is total internal reflection.</p>",
           [("Sound at 340 m/s, frequency 680 Hz. Wavelength?", ["λ = v ÷ f = 340 ÷ 680"], "0.50 m"),
            ("Light goes from air into glass (n = 1.50) at 30°. Angle of refraction?", ["sin r = sin 30° ÷ 1.50 = 0.333"], "19.5°")],
           ["Thinking the frequency changes when a wave enters a new medium: speed and wavelength change.", "Measuring angles from the surface instead of the normal.", "Saying sound can travel through a vacuum."],
           [("Why can you hear around a corner but not see around it?", "Sound waves have wavelengths of about a metre, similar to doorways, so they diffract a lot; light's wavelength is far too small."),
            ("What is total internal reflection used for?", "Optical fibres carry internet and phone signals as light that reflects inside the glass core; it is also used in endoscopes.")],
           u16),
    ]
